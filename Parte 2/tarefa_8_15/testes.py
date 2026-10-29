import itertools
import random
import networkx as nx
from edmonds import edmonds, busca, aumente, verificar, tamanho


def adj_de(n, E):
    adj = [[] for _ in range(n)]
    for u, v in E:
        adj[u].append(v)
        adj[v].append(u)
    return [sorted(l) for l in adj]


def C(n):
    return [(i, (i + 1) % n) for i in range(n)]


def K(n):
    return list(itertools.combinations(range(n), 2))


PET = [(0, 1), (1, 2), (2, 3), (3, 4), (4, 0), (0, 5), (1, 6), (2, 7), (3, 8), (4, 9),
       (5, 7), (7, 9), (9, 6), (6, 8), (8, 5)]
FLOR = [(0, 1), (1, 2), (2, 3), (3, 4), (4, 5), (5, 6), (6, 2), (6, 7)]

TABELA = [
    ("C3", 3, C(3), 1), ("C5", 5, C(5), 2), ("C7", 7, C(7), 3), ("C9", 9, C(9), 4),
    ("K2", 2, K(2), 1), ("K3", 3, K(3), 1), ("K4", 4, K(4), 2), ("K5", 5, K(5), 2),
    ("K6", 6, K(6), 3), ("K7", 7, K(7), 3),
    ("Petersen", 10, PET, 5),
    ("gravata", 5, [(0, 1), (1, 2), (2, 0), (2, 3), (3, 4), (4, 2)], 2),
    ("2 triangulos + ponte", 6, [(0, 1), (1, 2), (2, 0), (3, 4), (4, 5), (5, 3), (2, 3)], 3),
    ("estrela K1,3", 4, [(0, 1), (0, 2), (0, 3)], 1),
    ("aranha", 7, [(0, 1), (1, 2), (0, 3), (3, 4), (0, 5), (5, 6)], 3),
    ("sol", 10, C(5) + [(i, i + 5) for i in range(5)], 5),
    ("P4 + isolado", 5, [(0, 1), (1, 2), (2, 3)], 2),
    ("sem arestas", 4, [], 0),
    ("flor", 8, FLOR, 4),
]


def nu_exaustivo(n, E):
    # percorre os subconjuntos de arestas que sao emparelhamentos (inclui / nao inclui cada aresta)
    melhor = 0
    usado = [False] * n

    def rec(i, k):
        nonlocal melhor
        if k + (len(E) - i) <= melhor:
            return
        if i == len(E):
            melhor = max(melhor, k)
            return
        u, v = E[i]
        if not usado[u] and not usado[v]:
            usado[u] = usado[v] = True
            rec(i + 1, k + 1)
            usado[u] = usado[v] = False
        rec(i + 1, k)
    rec(0, 0)
    return melhor


def tutte_berge(n, E):
    # n - 2 nu = max_S (odd(G - S) - |S|)
    adj = adj_de(n, E)
    melhor = 0
    for mask in range(1 << n):
        fora = [(mask >> v) & 1 for v in range(n)]
        visto = list(fora)
        impares = 0
        for s in range(n):
            if visto[s]:
                continue
            visto[s] = 1
            pilha = [s]
            tam = 0
            while pilha:
                u = pilha.pop()
                tam += 1
                for w in adj[u]:
                    if not visto[w]:
                        visto[w] = 1
                        pilha.append(w)
            impares += tam % 2
        melhor = max(melhor, impares - sum(fora))
    return (n - melhor) // 2


def teste_tabela():
    for nome, n, E, nu in TABELA:
        adj = adj_de(n, E)
        mate = edmonds(n, adj)
        verificar(adj, mate)
        assert tamanho(mate) == nu, (nome, tamanho(mate))
    print("tabela ok (19 grafos)")


def teste_flor():
    n = 8
    adj = adj_de(n, FLOR)
    mate0 = [-1, 2, 1, 4, 3, 6, 5, -1]
    eventos = []
    z, parent, base, tipo = busca(0, adj, mate0, eventos)
    assert parent == [-1, 0, -1, 2, 5, 4, 2, 6]
    assert base == [0, 1, 2, 2, 2, 2, 2, 7]
    assert ["-IE"[t] for t in tipo] == ["E", "I", "E", "E", "E", "E", "E", "-"]
    assert z == 7
    contracoes = [e for e in eventos if e[2] == "d"]
    assert contracoes == [(4, 5, "d", 2)]
    # caminho percorrido por AUMENTE: 7, 6, 5, 4, 3, 2, 1, 0
    percurso = []
    zz = z
    while zz != -1:
        x = parent[zz]
        percurso += [zz, x]
        zz = mate0[x]
    assert percurso == [7, 6, 5, 4, 3, 2, 1, 0]
    mate = aumente(z, parent, list(mate0))
    assert mate == [1, 0, 3, 2, 5, 4, 7, 6]
    assert edmonds(n, adj, mate0) == mate
    print("rastro do exemplo do texto (flor) ok: uma contracao, CONTRAIA(4, 5, 2)")


def teste_aleatorios():
    rng = random.Random(15)
    for _ in range(3000):
        n = rng.randint(1, 9)
        p = rng.choice([0.2, 0.35, 0.5])
        E = [(u, v) for u, v in itertools.combinations(range(n), 2) if rng.random() < p]
        adj = adj_de(n, E)
        mate = edmonds(n, adj)
        verificar(adj, mate)
        nu = tamanho(mate)
        if len(E) <= 14:
            assert nu == nu_exaustivo(n, E)
        assert nu == tutte_berge(n, E)
        G = nx.Graph()
        G.add_nodes_from(range(n))
        G.add_edges_from(E)
        assert nu == len(nx.max_weight_matching(G, maxcardinality=True))
    print("3000 aleatorios ok (exaustivo, Tutte-Berge, networkx)")


def teste_familias():
    for k in range(1, 21):
        n = 2 * k + 1
        assert tamanho(edmonds(n, adj_de(n, C(n)))) == k
    for n in range(0, 13):
        assert tamanho(edmonds(n, adj_de(n, K(n)))) == n // 2
    print("familias ok: C_{2k+1} (k <= 20), K_n (n <= 12)")


if __name__ == "__main__":
    teste_tabela()
    teste_flor()
    teste_familias()
    teste_aleatorios()
    print("todos os testes passaram")
