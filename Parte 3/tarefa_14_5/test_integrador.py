import os
import sys
import time
import random
import subprocess
import networkx as nx
from common.graphs import from_edges, edges_of, random_planar_3conn, dodecahedron
from m1_conexidade.m1 import is_3connected
from m3_faces.m3 import check_embedding
from m4_certificado.m4 import verify_minor, certificate_ops
from m5_base_ciclos.m5 import face_basis, verify_basis
from planar_contract import decidir

AQUI = os.path.dirname(os.path.abspath(__file__))


def faces_nx(adj):
    ok, emb = nx.check_planarity(nx.Graph(edges_of(adj)))
    visto = set()
    out = []
    for u, v in emb.edges():
        if (u, v) not in visto:
            out.append(tuple(emb.traverse_face(u, v, mark_half_edges=visto)))
    return out


def arestas_das_faces(F):
    return {frozenset(frozenset(p) for p in zip(f, f[1:] + f[:1])) for f in F}


def confere(adj):
    g = nx.Graph(edges_of(adj))
    g.add_nodes_from(adj)
    r = decidir(adj)
    assert r["planar"] == nx.check_planarity(g)[0]
    if r["planar"]:
        assert check_embedding(adj, r["faces"]) is None
        assert arestas_das_faces(r["faces"]) == arestas_das_faces(faces_nx(adj))
        vecs, eid = face_basis(adj, r["faces"])
        assert verify_basis(adj, vecs, eid)["ok"]
    else:
        assert verify_minor(adj, r["model"], r["kind"]) is None
        _, H = certificate_ops(adj, r["model"], r["kind"])
        alvo = nx.complete_graph(5) if r["kind"] == "K5" else nx.complete_bipartite_graph(3, 3)
        assert nx.is_isomorphic(nx.Graph(edges_of(H)), alvo)
    return r["planar"]


def teste_atlas():
    conta = {}
    for g in nx.graph_atlas_g():
        if 4 <= len(g) <= 7 and nx.node_connectivity(g) >= 3:
            p = confere(from_edges(g.edges(), n=len(g)))
            c = conta.setdefault(len(g), [0, 0])
            c[0 if p else 1] += 1
    assert conta == {4: [1, 0], 5: [2, 1], 6: [7, 10], 7: [34, 102]}, conta
    print("atlas ok (planares, nao planares):", conta)


def teste_aleatorios():
    rng = random.Random(14)
    total = {"gnm": 0, "planar": 0, "planar+extras": 0}
    for n in range(8, 14):
        feitos = 0
        while feitos < 150:
            g = nx.gnm_random_graph(n, rng.randint(int(1.5 * n), 3 * n), seed=rng.randint(0, 10 ** 9))
            adj = from_edges(g.edges(), n=n)
            if not is_3connected(adj):
                continue
            confere(adj)
            feitos += 1
        total["gnm"] += feitos
    for n in range(5, 16):
        for _ in range(40):
            adj = random_planar_3conn(n, seed=rng.random())
            assert confere(adj)
            total["planar"] += 1
            for _ in range(rng.randint(1, 3)):
                u, v = rng.sample(range(n), 2)
                adj[u].add(v)
                adj[v].add(u)
            confere(adj)
            total["planar+extras"] += 1
    print("aleatorios ok:", total)


def teste_exemplos():
    esperado = {"w5": "PLANAR", "prisma": "PLANAR", "cubo": "PLANAR", "dodecaedro": "PLANAR",
                "k5": "NAO PLANAR", "k33": "NAO PLANAR", "petersen": "NAO PLANAR", "j137": "NAO PLANAR",
                "k4sub": "ENTRADA INVALIDA"}
    for nome, veredito in esperado.items():
        p = subprocess.run([sys.executable, "planar_contract.py", f"exemplos/{nome}.txt"],
                           cwd=AQUI, capture_output=True, text=True)
        primeira = p.stdout.splitlines()[0]
        assert primeira.startswith(veredito), (nome, primeira)
        assert p.returncode == (2 if veredito == "ENTRADA INVALIDA" else 0)
    print("os 9 exemplos pela linha de comando ok")


def teste_desempenho():
    t0 = time.perf_counter()
    decidir(dodecahedron())
    t1 = time.perf_counter() - t0
    tempos = {}
    for n in (40, 60):
        adj = random_planar_3conn(n, seed=n)
        t0 = time.perf_counter()
        decidir(adj)
        tempos[n] = time.perf_counter() - t0
    print(f"tempo: dodecaedro {t1:.3f} s, n=40 {tempos[40]:.2f} s, n=60 {tempos[60]:.2f} s")


if __name__ == "__main__":
    teste_atlas()
    teste_exemplos()
    teste_aleatorios()
    teste_desempenho()
    print("OK")
