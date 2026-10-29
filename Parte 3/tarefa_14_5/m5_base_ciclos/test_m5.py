import time
import networkx as nx
from common.graphs import from_edges, edges_of, wheel, prism, cube, octahedron, k5_minus_e, dodecahedron, k5, k33
from m5_base_ciclos.m5 import face_basis, rank_f2, verify_basis, fundamental_basis, tem_base_esparsa


def faces_nx(adj):
    ok, emb = nx.check_planarity(nx.Graph(edges_of(adj)))
    visto = set()
    out = []
    for u, v in emb.edges():
        if (u, v) not in visto:
            out.append(tuple(emb.traverse_face(u, v, mark_half_edges=visto)))
    return out


def teste_tabela():
    tabela = [(wheel(4), 5, 8, 5), (prism(), 6, 9, 5), (cube(), 8, 12, 6), (octahedron(), 6, 12, 8),
              (k5_minus_e(), 5, 9, 6), (dodecahedron(), 20, 30, 12)]
    for adj, n, m, f in tabela:
        F = faces_nx(adj)   # faces prontas (M5 nao depende de M3)
        assert (len(adj), len(edges_of(adj)), len(F)) == (n, m, f)
        vecs, eid = face_basis(adj, F, outer=0)
        r = verify_basis(adj, vecs, eid)
        assert r["ok"] and r["count"] == m - n + 1 and r["maxuse"] == 2, r
        # com a externa: toda aresta em exatamente 2 vetores e o XOR de todos e 0
        todos, _ = face_basis(adj, F, outer=None)
        x = 0
        for v in todos:
            x ^= v
        assert x == 0
        assert all(sum(v >> j & 1 for v in todos) == 2 for j in range(m))
        uso1 = {j for j in range(m) if sum(v >> j & 1 for v in vecs) == 1}
        assert len(uso1) == len(F[0])   # arestas de uso 1 = as da face externa
    print("tabela M5 ok (6 grafos)")


def teste_contrastes():
    adj = cube()
    vecs, eid = fundamental_basis(adj, 0)
    r = verify_basis(adj, vecs, eid)
    assert r["rank"] == 5 and r["maxuse"] == 3 and not r["ok"]
    K5 = k5()
    vecs, eid = fundamental_basis(K5, 0)
    r = verify_basis(K5, vecs, eid)
    assert r["rank"] == 6 and r["maxuse"] == 3 and not r["ok"]
    F = faces_nx(adj)
    vecs, eid = face_basis(adj, F)
    repetida = vecs[:-1] + [vecs[0]]
    assert verify_basis(adj, repetida, eid)["rank"] == 4 and not verify_basis(adj, repetida, eid)["ok"]
    impar = vecs[:-1] + [1]   # uma aresta sozinha: dois vertices de grau impar
    r = verify_basis(adj, impar, eid)
    assert not r["even"] and not r["ok"]
    print("contrastes rejeitados: base fundamental do cubo (uso 3), de K5 (uso 3), face repetida, grau impar")


def teste_mac_lane():
    K4 = from_edges([(0, 1), (0, 2), (0, 3), (1, 2), (1, 3), (2, 3)])
    assert tem_base_esparsa(K4) and tem_base_esparsa(wheel(4))
    assert not tem_base_esparsa(k33())
    t0 = time.perf_counter()
    assert not tem_base_esparsa(k5())
    print(f"Mac Lane por forca bruta ok: K4 e W5 sim, K3,3 e K5 nao (K5 em {time.perf_counter() - t0:.2f} s)")


if __name__ == "__main__":
    teste_tabela()
    teste_contrastes()
    teste_mac_lane()
    print("OK")
