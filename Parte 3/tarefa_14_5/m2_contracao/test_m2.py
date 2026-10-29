import random
import networkx as nx
from common.graphs import (from_edges, edges_of, wheel, prism, cube, k5, k33, j137, petersen,
                           dodecahedron, random_planar_3conn)
from m2_contracao.m2 import contraction_trace, contract, uncontract, branch_sets


def escolher_nx(J):
    # oraculo independente de M1
    for x, y in edges_of(J):
        h = nx.contracted_nodes(nx.Graph(edges_of(J)), x, y, self_loops=False)
        if nx.node_connectivity(h) >= 3:
            return (x, y)


TABELA = [
    (wheel(4), [(1, 2, [0, 4], [0, 3])], {0, 1, 3, 4}),
    (prism(), [(0, 3, [1, 2], [4, 5]), (1, 2, [0, 4], [0, 5])], {0, 1, 4, 5}),
    (cube(), [(0, 1, [2, 4], [3, 5]), (2, 3, [0, 6], [0, 7]), (0, 2, [4, 5], [6, 7]), (4, 5, [0, 6], [0, 7])], {0, 4, 6, 7}),
    (k5(), [(0, 1, [2, 3, 4], [2, 3, 4])], {0, 2, 3, 4}),
    (k33(), [(0, 3, [4, 5], [1, 2]), (1, 4, [0, 5], [0, 2])], {0, 1, 2, 5}),
    (j137(), [(0, 1, [2, 3], [4, 5]), (0, 2, [3, 4, 5], [3, 4, 5])], {0, 3, 4, 5}),
    (petersen(), [(0, 1, [4, 5], [2, 6]), (0, 2, [4, 5, 6], [3, 7]), (0, 6, [3, 4, 5, 7], [8, 9]),
                  (3, 4, [0, 8], [0, 9]), (3, 8, [0, 9], [0, 5]), (3, 5, [0, 9], [0, 7])], {0, 3, 7, 9}),
]


def confere(adj):
    trace, k4 = contraction_trace(adj)
    n = len(adj)
    assert len(trace) == n - 4
    assert len(k4) == 4 and len(edges_of(k4)) == 6
    J = adj
    Js = [J]
    for k, (x, y, A, B) in enumerate(trace):
        assert len(A) >= 2 and len(B) >= 2 and len(J[x]) >= 3 and len(J[y]) >= 3
        J = contract(J, x, y)
        Js.append(J)
        assert len(J) == n - k - 1
        assert nx.node_connectivity(nx.Graph(edges_of(J))) >= 3
    # uncontract de tras para frente devolve G
    H = k4
    for k in range(len(trace) - 1, -1, -1):
        H = uncontract(H, trace[k])
        assert H == Js[k]
    # branch_sets: particao de V(G) em conjuntos conexos que reproduz J_k
    for k in range(len(trace) + 1):
        S = branch_sets(trace, k, list(adj))
        assert set(S) == set(Js[k])
        tudo = [v for s in S.values() for v in s]
        assert sorted(tudo) == sorted(adj)
        for s in S.values():
            assert nx.is_connected(nx.Graph(adj).subgraph(s)) if len(s) > 1 else True
        for u in S:
            for w in S:
                if u < w:
                    liga = any(b in adj[a] for a in S[u] for b in S[w])
                    assert liga == (w in Js[k][u])
    return trace


def teste_tabela():
    for adj, esperado, final in TABELA:
        trace, k4 = contraction_trace(adj)
        assert trace == esperado, trace
        assert set(k4) == final
        assert contraction_trace(adj, escolher=escolher_nx)[0] == esperado
        confere(adj)
    trace, k4 = contraction_trace(dodecahedron())
    assert trace[:4] == [(0, 1, [10, 19], [2, 8]), (0, 2, [8, 10, 19], [3, 6]),
                         (0, 6, [3, 8, 10, 19], [5, 7]), (0, 5, [3, 7, 8, 10, 19], [4, 15])]
    assert len(trace) == 16 and set(k4) == {0, 3, 11, 18}
    print("tabela M2 ok")


def teste_atlas_e_aleatorios():
    total = 0
    for g in nx.graph_atlas_g():
        if len(g) >= 5 and nx.node_connectivity(g) >= 3:
            adj = from_edges(g.edges(), n=len(g))
            trace = confere(adj)
            assert trace == contraction_trace(adj, escolher=escolher_nx)[0]
            total += 1
    rng = random.Random(2)
    aleat = 0
    while aleat < 60:
        n = rng.randint(8, 13)
        if aleat % 2:
            adj = random_planar_3conn(n, seed=rng.random())
        else:
            g = nx.gnm_random_graph(n, rng.randint(2 * n, 4 * n), seed=rng.randint(0, 10 ** 6))
            if nx.node_connectivity(g) < 3:
                continue
            adj = from_edges(g.edges(), n=n)
        confere(adj)
        aleat += 1
    print(f"atlas ({total} grafos 3-conexos com n >= 5) e {aleat} aleatorios de 8 a 13 vertices ok")


if __name__ == "__main__":
    teste_tabela()
    teste_atlas_e_aleatorios()
    print("OK")
