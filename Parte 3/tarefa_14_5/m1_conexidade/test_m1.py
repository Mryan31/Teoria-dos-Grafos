import networkx as nx
from common.graphs import (from_edges, edges_of, wheel, prism, cube, octahedron, petersen, k5, k33,
                           k5_minus_e, dodecahedron, j137, k4_sub)
from m1_conexidade.m1 import (is_3connected, is_contractible, contractible_edges,
                              find_contractible_edge, find_separator)

K4 = from_edges([(0, 1), (0, 2), (0, 3), (1, 2), (1, 3), (2, 3)])
DOIS_K4_VERTICE = from_edges([(0, 1), (0, 2), (0, 3), (1, 2), (1, 3), (2, 3), (3, 4), (3, 5), (3, 6),
                              (4, 5), (4, 6), (5, 6)])
DOIS_K4_ARESTA = from_edges([(0, 1), (0, 2), (0, 3), (1, 2), (1, 3), (2, 3), (2, 4), (2, 5), (3, 4),
                             (3, 5), (4, 5)])


def atlas(nmin, nmax):
    for g in nx.graph_atlas_g():
        if nmin <= len(g) <= nmax:
            yield g, from_edges(g.edges(), n=len(g))


def teste_tabela():
    assert is_3connected(K4)
    casos = [
        (wheel(4), [(1, 2), (1, 4), (2, 3), (3, 4)]),
        (prism(), [(0, 3), (1, 4), (2, 5)]),
        (k5_minus_e(), [(0, 2), (0, 3), (0, 4), (1, 2), (1, 3), (1, 4)]),
    ]
    for g, esperado in casos:
        assert is_3connected(g)
        assert contractible_edges(g) == esperado
    for g, k in ((wheel(5), 5), (wheel(6), 6)):
        ce = contractible_edges(g)
        assert len(ce) == k and all(0 not in e for e in ce)   # so o aro
    ce = contractible_edges(j137())
    assert len(ce) == 9 and (2, 3) not in ce and (4, 5) not in ce
    for g, m, primeira in ((cube(), 12, (0, 1)), (octahedron(), 12, (0, 1)), (k5(), 10, (0, 1)),
                           (k33(), 9, (0, 3)), (petersen(), 15, (0, 1)), (dodecahedron(), 30, (0, 1))):
        assert is_3connected(g)
        assert len(contractible_edges(g)) == m
        assert find_contractible_edge(g) == primeira
    P5 = from_edges([(0, 1), (1, 2), (2, 3), (3, 4)])
    C5 = from_edges([(i, (i + 1) % 5) for i in range(5)])
    for g, sep in ((P5, [1]), (C5, [0, 2]), (k4_sub(), [0, 1]), (DOIS_K4_VERTICE, [3]), (DOIS_K4_ARESTA, [2, 3])):
        assert not is_3connected(g)
        assert find_separator(g) == sep, find_separator(g)
    print("tabela M1 ok")


def teste_atlas():
    conta = {}
    arestas = 0
    menor = {}
    for g, adj in atlas(4, 7):
        tres = is_3connected(adj)
        assert tres == (nx.node_connectivity(g) >= 3)
        if not tres:
            continue
        n = len(g)
        conta[n] = conta.get(n, 0) + 1
        if n >= 5:
            ce = contractible_edges(adj)
            for x, y in edges_of(adj):
                h = nx.contracted_nodes(g, x, y, self_loops=False)
                assert is_contractible(adj, x, y) == (nx.node_connectivity(h) >= 3)
                arestas += 1
            menor[n] = min(menor.get(n, 99), len(ce))
            assert find_contractible_edge(adj) == ce[0]
    assert conta == {4: 1, 5: 3, 6: 17, 7: 136}, conta
    assert menor == {5: 4, 6: 3, 7: 5}, menor
    print(f"atlas ok: 3-conexos {conta}, {arestas} arestas conferidas, minimo de contraiveis {menor}")


if __name__ == "__main__":
    teste_tabela()
    teste_atlas()
    print("OK")
