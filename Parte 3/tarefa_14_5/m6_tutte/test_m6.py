import random
import numpy as np
import networkx as nx
from common.graphs import edges_of, wheel, cube, prism, octahedron, dodecahedron, random_planar_3conn
from m6_tutte.m6 import tutte_positions, verify_tutte


def faces_nx(adj):
    ok, emb = nx.check_planarity(nx.Graph(edges_of(adj)))
    visto = set()
    out = []
    for u, v in emb.edges():
        if (u, v) not in visto:
            out.append(tuple(emb.traverse_face(u, v, mark_half_edges=visto)))
    return out


def perto(p, q):
    return np.allclose(p, q, atol=1e-4)


def teste_tabela():
    for k in (4, 5, 6):
        adj = wheel(k)
        F = faces_nx(adj)
        o = next(j for j, f in enumerate(F) if 0 not in f)
        pos = tutte_positions(adj, F[o])
        assert perto(pos[0], (0, 0))
    adj = cube()
    F = faces_nx(adj)
    for o in range(len(F)):
        pos = tutte_positions(adj, F[o])
        r = verify_tutte(adj, pos, F, o)
        internos = [v for v in adj if v not in F[o]]
        assert all(abs(np.linalg.norm(pos[v]) - 1 / 3) < 1e-9 for v in internos)
        assert r["crossings"] == 0 and abs(r["min_turn"] - 0.2222) < 1e-3 and r["barycentre"] < 1e-9
    pos = tutte_positions(prism(), (0, 1, 2))
    for v, p in zip(range(6), [(1, 0), (-.5, .866), (-.5, -.866), (.25, 0), (-.125, .2165), (-.125, -.2165)]):
        assert perto(pos[v], p)
    pos = tutte_positions(octahedron(), (0, 1, 2))
    for v, p in zip((3, 4, 5), [(-.2, 0), (.1, -.1732), (.1, .1732)]):
        assert perto(pos[v], p)
    adj = dodecahedron()
    F = faces_nx(adj)
    o = 0
    pos = tutte_positions(adj, F[o])
    r = verify_tutte(adj, pos, F, o)
    assert r["crossings"] == 0 and r["barycentre"] < 1e-12 and abs(r["min_turn"] - 0.023) < 1e-3
    V = sorted(adj)
    I = [v for v in V if v not in F[o]]
    L = np.array([[len(adj[a]) if a == b else (-1 if b in adj[a] else 0) for b in I] for a in I], float)
    print(f"tabela M6 ok; dodecaedro: min_turn {r['min_turn']:.4f}, det L_II = {np.linalg.det(L):.4g}")


def teste_aleatorios():
    rng = random.Random(3)
    for _ in range(200):
        n = rng.randint(5, 29)
        adj = random_planar_3conn(n, seed=rng.random())
        F = faces_nx(adj)
        o = rng.randrange(len(F))
        pos = tutte_positions(adj, F[o])
        r = verify_tutte(adj, pos, F, o)
        escala = max(len(f) for f in F)
        assert r["crossings"] == 0 and r["min_turn"] > 0 and r["barycentre"] < 1e-9 * escala, r
    print("200 planares 3-conexos aleatorios: 0 cruzamentos, curvas > 0, residuo < 1e-9")


def teste_negativo():
    adj = cube()
    pos = tutte_positions(adj, (0, 1, 3, 7, 6, 4))   # ciclo induzido mas nao periferico
    assert np.linalg.norm(pos[2] - pos[5]) < 1e-12
    print("negativo ok: com ciclo nao periferico, 2 e 5 caem no mesmo ponto")


if __name__ == "__main__":
    teste_tabela()
    teste_aleatorios()
    teste_negativo()
    print("OK")
