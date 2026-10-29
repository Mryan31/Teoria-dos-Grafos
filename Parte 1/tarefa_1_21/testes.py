import random
import warnings
import networkx as nx
from refinamento import refinar, montar_adj

warnings.filterwarnings("ignore")  # aviso do networkx sobre mudanca nos hashes (v3.5)

# (nome, n, arestas, rodadas, classes, cores esperadas)
TABELA = [
    ("P5", 5, [(1, 2), (2, 3), (3, 4), (4, 5)], 1, 3, [0, 1, 2, 1, 0]),
    ("P7", 7, [(i, i + 1) for i in range(1, 7)], 2, 4, [0, 1, 2, 3, 2, 1, 0]),
    ("vassoura", 8, [(1, 2), (2, 3), (3, 4), (4, 5), (5, 6), (5, 7), (5, 8)], 1, 6, [0, 2, 3, 4, 5, 1, 1, 1]),
    ("T1", 6, [(1, 2), (1, 3), (1, 4), (2, 5), (3, 6)], 1, 4, [3, 2, 2, 1, 0, 0]),
    ("T2", 6, [(1, 2), (1, 3), (1, 4), (2, 5), (5, 6)], 1, 5, [4, 3, 1, 1, 2, 0]),
    ("estrela K1,4", 5, [(1, 2), (1, 3), (1, 4), (1, 5)], 0, 2, [1, 0, 0, 0, 0]),
    ("K3,3", 6, [(a, b) for a in (1, 2, 3) for b in (4, 5, 6)], 0, 1, [0] * 6),
    ("prisma", 6, [(1, 2), (2, 3), (1, 3), (4, 5), (5, 6), (4, 6), (1, 4), (2, 5), (3, 6)], 0, 1, [0] * 6),
    ("paw", 4, [(1, 2), (2, 3), (1, 3), (3, 4)], 0, 3, [1, 1, 2, 0]),
    ("C5", 5, [(1, 2), (2, 3), (3, 4), (4, 5), (5, 1)], 0, 1, [0] * 5),
    ("K4", 4, [(1, 2), (1, 3), (1, 4), (2, 3), (2, 4), (3, 4)], 0, 1, [0] * 4),
    ("3 isolados", 3, [], 0, 1, [0] * 3),
    ("n=1", 1, [], 0, 1, [0]),
    ("so 1-2", 3, [(1, 2)], 0, 2, [1, 1, 0]),
]


def grafo_aleatorio(n, p=0.35):
    return [(u, v) for u in range(1, n + 1) for v in range(u + 1, n + 1) if random.random() < p]


def particao(cores, n):
    # "mesma cor" como conjunto de pares, para comparar sem olhar os nomes
    return {(u, v) for u in range(1, n + 1) for v in range(u + 1, n + 1) if cores[u] == cores[v]}


def teste_tabela():
    for nome, n, E, rod, cl, esperado in TABELA:
        cores, rodadas, hist = refinar(n, E)
        assert cores[1:] == esperado, (nome, cores[1:])
        assert rodadas == rod, (nome, rodadas)
        assert len(set(cores[1:])) == cl, nome
    print("tabela ok")


def confere_propriedades(n, E):
    cores, rodadas, hist = refinar(n, E)
    adj = montar_adj(n, E)
    # refinamento: cada c_{i+1} refina c_i e o numero de classes cresce
    for i in range(len(hist) - 1):
        a, b = hist[i], hist[i + 1]
        for u in range(1, n + 1):
            for v in range(1, n + 1):
                if b[u] == b[v]:
                    assert a[u] == a[v]
        assert len(set(b[1:])) > len(set(a[1:]))
    # estabilidade da coloracao final
    for u in range(1, n + 1):
        for v in range(1, n + 1):
            if cores[u] == cores[v]:
                assert len(adj[u]) == len(adj[v])
                assert sorted(cores[x] for x in adj[u]) == sorted(cores[x] for x in adj[v])
    return cores, rodadas, hist


def teste_propriedades_e_lema():
    random.seed(1)
    for _ in range(300):
        n = random.randint(1, 12)
        E = grafo_aleatorio(n)
        cores, rodadas, _ = confere_propriedades(n, E)
        # Lema 1.20: renomeia os vertices por uma permutacao pi
        pi = list(range(1, n + 1))
        random.shuffle(pi)
        pi = [0] + pi
        E2 = [(pi[u], pi[v]) for u, v in E]
        cores2, rodadas2, _ = refinar(n, E2)
        for v in range(1, n + 1):
            assert cores2[pi[v]] == cores[v]
        assert rodadas2 == rodadas
    print("propriedades e Lema 1.20 ok (300 grafos)")


def teste_networkx():
    random.seed(2)
    for _ in range(200):
        n = random.randint(1, 12)
        E = grafo_aleatorio(n)
        cores, rodadas, hist = refinar(n, E)
        G = nx.Graph()
        G.add_nodes_from(range(1, n + 1))
        G.add_edges_from(E)
        for i in range(len(hist)):
            h = nx.weisfeiler_lehman_subgraph_hashes(G, iterations=i + 1)
            rotulo = [None] + [h[v][i] for v in range(1, n + 1)]
            assert particao(rotulo, n) == particao(hist[i], n)
    # hashes de grafo inteiro: T1 != T2, K3,3 == prisma
    def H(E):
        return nx.weisfeiler_lehman_graph_hash(nx.Graph(E))
    t1, t2, k33, prisma = (TABELA[3][2], TABELA[4][2], TABELA[6][2], TABELA[7][2])
    assert H(t1) != H(t2)
    assert H(k33) == H(prisma)
    print("comparacao com networkx ok")


def teste_entrada_invalida():
    for E in ([(1, 1)], [(1, 2), (2, 1)]):
        try:
            refinar(2, E)
            assert False, "deveria rejeitar"
        except ValueError:
            pass
    print("entradas invalidas rejeitadas")


if __name__ == "__main__":
    teste_tabela()
    teste_propriedades_e_lema()
    teste_networkx()
    teste_entrada_invalida()
    print("todos os testes passaram")
