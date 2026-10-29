import itertools
import random
import networkx as nx
from conectividade import (edmonds_karp, conectividade_aresta, conectividade_vertice,
                           lambda_G, kappa_G, delta_G)


def P(n):
    return [(i, i + 1) for i in range(n - 1)]


def C(n):
    return [(i, (i + 1) % n) for i in range(n)]


def K(n):
    return list(itertools.combinations(range(n), 2))


def Krs(r, s):
    return [(a, r + b) for a in range(r) for b in range(s)]


def Q(d):
    return [(u, u ^ (1 << b)) for u in range(1 << d) for b in range(d) if u < u ^ (1 << b)]


DOIS_K4 = [(0, 1), (0, 2), (0, 3), (1, 2), (1, 3), (2, 3), (2, 4), (2, 5), (3, 4), (3, 5), (4, 5)]
PET = [(0, 1), (1, 2), (2, 3), (3, 4), (4, 0), (0, 5), (1, 6), (2, 7), (3, 8), (4, 9),
       (5, 7), (7, 9), (9, 6), (6, 8), (8, 5)]

GLOBAIS = [  # (nome, n, arestas, kappa, lambda, delta)
    ("P2", 2, P(2), 1, 1, 1), ("P5", 5, P(5), 1, 1, 1), ("C6", 6, C(6), 2, 2, 2),
    ("K5", 5, K(5), 4, 4, 4), ("K2,3", 5, Krs(2, 3), 2, 2, 2), ("K3,3", 6, Krs(3, 3), 3, 3, 3),
    ("Q3", 8, Q(3), 3, 3, 3), ("Q4", 16, Q(4), 4, 4, 4), ("dois K4", 6, DOIS_K4, 2, 3, 3),
    ("Petersen", 10, PET, 3, 3, 3), ("dois triangulos", 6, [(0, 1), (1, 2), (2, 0), (3, 4), (4, 5), (5, 3)], 0, 0, 2),
]

LOCAIS = [  # (n, arestas, x, y, lambda, caminhos aresta, corte, kappa, caminhos vertice, separador)
    (6, DOIS_K4, 0, 4, 3, "0-1-2-4 | 0-2-5-4 | 0-3-4", "0-1 0-2 0-3", 2, "0-2-4 | 0-3-4", "2 3"),
    (6, DOIS_K4, 1, 5, 3, "1-0-2-4-5 | 1-2-5 | 1-3-5", "0-1 1-2 1-3", 2, "1-2-5 | 1-3-5", "2 3"),
    (6, DOIS_K4, 0, 1, 3, "0-1 | 0-2-1 | 0-3-1", "0-1 0-2 0-3", None, None, None),
    (6, DOIS_K4, 2, 3, 5, "2-0-3 | 2-1-3 | 2-3 | 2-4-3 | 2-5-3", "0-2 1-2 2-3 2-4 2-5", None, None, None),
    (6, C(6), 0, 3, 2, "0-1-2-3 | 0-5-4-3", "0-1 5-0", 2, "0-1-2-3 | 0-5-4-3", "1 5"),
    (8, Q(3), 0, 7, 3, "0-1-3-7 | 0-2-6-7 | 0-4-5-7", "0-1 0-2 0-4", 3, "0-1-3-7 | 0-2-6-7 | 0-4-5-7", "1 2 4"),
    (5, Krs(2, 3), 0, 1, 3, "0-2-1 | 0-3-1 | 0-4-1", "0-2 0-3 0-4", 3, "0-2-1 | 0-3-1 | 0-4-1", "2 3 4"),
    (5, P(5), 0, 4, 1, "0-1-2-3-4", "0-1", 1, "0-1-2-3-4", "1"),
]


def fmt(cams):
    return " | ".join("-".join(map(str, c)) for c in cams)


def conexos(n, arestas, x, y, sem_v=(), sem_e=()):
    sem_e = {frozenset(e) for e in sem_e}
    adj = [[] for _ in range(n)]
    for u, v in arestas:
        if frozenset((u, v)) not in sem_e and u not in sem_v and v not in sem_v:
            adj[u].append(v)
            adj[v].append(u)
    visto = {x}
    pilha = [x]
    while pilha:
        u = pilha.pop()
        for w in adj[u]:
            if w not in visto:
                visto.add(w)
                pilha.append(w)
    return y in visto


def confere_caminhos(n, arestas, x, y, val, cams, tipo):
    E = {frozenset(e) for e in arestas}
    assert len(cams) == val
    usadas = []
    internos = []
    for c in cams:
        assert c[0] == x and c[-1] == y
        assert len(set(c)) == len(c)
        for a, b in zip(c, c[1:]):
            assert frozenset((a, b)) in E
            usadas.append(frozenset((a, b)))
        internos += c[1:-1]
    if tipo == "aresta":
        assert len(usadas) == len(set(usadas))
    else:
        assert len(internos) == len(set(internos))


def confere_local(n, arestas, x, y):
    val, cams, corte = conectividade_aresta(n, arestas, x, y)
    confere_caminhos(n, arestas, x, y, val, cams, "aresta")
    assert len(corte) == val
    assert not conexos(n, arestas, x, y, sem_e=corte)
    adjacentes = frozenset((x, y)) in {frozenset(e) for e in arestas}
    if not adjacentes:
        k, cams2, sep = conectividade_vertice(n, arestas, x, y)
        confere_caminhos(n, arestas, x, y, k, cams2, "vertice")
        assert len(sep) == k and x not in sep and y not in sep
        assert not conexos(n, arestas, x, y, sem_v=set(sep))
        return val, corte, k, sep
    return val, corte, None, None


def teste_tabelas():
    for nome, n, E, k, l, d in GLOBAIS:
        assert (kappa_G(n, E), lambda_G(n, E), delta_G(n, E)) == (k, l, d), nome
        G = nx.Graph(E)
        assert nx.node_connectivity(G) == k and nx.edge_connectivity(G) == l, nome
    for n, E, x, y, l, ca, co, k, cv, se in LOCAIS:
        val, cams, corte = conectividade_aresta(n, E, x, y)
        assert (val, fmt(cams), " ".join(f"{u}-{v}" for u, v in corte)) == (l, ca, co), (x, y)
        if k is not None:
            val, cams, sep = conectividade_vertice(n, E, x, y)
            assert (val, fmt(cams), " ".join(map(str, sep))) == (k, cv, se), (x, y)
        else:
            try:
                conectividade_vertice(n, E, x, y)
                assert False
            except ValueError:
                pass
        confere_local(n, E, x, y)
    print("tabelas global (11) e local (8) ok")


def menor_corte_arestas(n, E, x=None, y=None):
    for k in range(len(E) + 1):
        for F in itertools.combinations(E, k):
            if x is None:
                if any(not conexos(n, E, a, b, sem_e=F) for a in range(n) for b in range(a + 1, n)):
                    return k
            elif not conexos(n, E, x, y, sem_e=F):
                return k


def menor_separador(n, E, x=None, y=None):
    resto = [v for v in range(n) if v not in (x, y)]
    for k in range(n + 1):
        for S in itertools.combinations(resto, k):
            if x is None:
                vivos = [v for v in range(n) if v not in S]
                if len(vivos) >= 2 and any(not conexos(n, E, a, b, sem_v=set(S))
                                           for a in vivos for b in vivos if a < b):
                    return k
            elif not conexos(n, E, x, y, sem_v=set(S)):
                return k


def teste_aleatorios():
    rng = random.Random(21)
    for _ in range(400):
        n = rng.randint(2, 7)
        E = [e for e in K(n) if rng.random() < 0.45]
        k, l, d = kappa_G(n, E), lambda_G(n, E), delta_G(n, E)
        assert k <= l <= d
        # lambda fixando x = 0 da o mesmo que todos os pares
        assert l == min(conectividade_aresta(n, E, 0, y)[0] for y in range(1, n))
        G = nx.Graph()
        G.add_nodes_from(range(n))
        G.add_edges_from(E)
        assert k == nx.node_connectivity(G) and l == nx.edge_connectivity(G)
        if len(E) <= 14:
            assert l == menor_corte_arestas(n, E)
            if len(E) < n * (n - 1) // 2:
                assert k == menor_separador(n, E)
            x, y = rng.sample(range(n), 2)
            val, corte, kv, sep = confere_local(n, E, x, y)
            assert val == menor_corte_arestas(n, E, x, y)
            if kv is not None:
                assert kv == menor_separador(n, E, x, y)
    print("400 aleatorios ok (kappa <= lambda <= delta, enumeracao exaustiva, networkx)")


def teste_familias():
    for n in range(2, 13):
        assert (kappa_G(n, P(n)), lambda_G(n, P(n))) == (1, 1)
        if n >= 3:
            assert (kappa_G(n, C(n)), lambda_G(n, C(n))) == (2, 2)
    for n in range(2, 9):
        assert (kappa_G(n, K(n)), lambda_G(n, K(n))) == (n - 1, n - 1)
    for r in range(1, 4):
        for s in range(1, 4):
            assert kappa_G(r + s, Krs(r, s)) == lambda_G(r + s, Krs(r, s)) == min(r, s)
    for d in range(1, 5):
        assert kappa_G(1 << d, Q(d)) == lambda_G(1 << d, Q(d)) == d
    print("familias ok (Pn, Cn ate 12, Kn ate 8, Kr,s, Qd ate 4)")


def teste_sanidade():
    # modelo errado: capacidade grande em TODOS os arcos centrais -> o valor explode
    n, E, x, y = 6, DOIS_K4, 0, 4
    N = n + 1
    arcos = [(2 * v, 2 * v + 1, N) for v in range(n)]
    for u, v in E:
        arcos += [(2 * u + 1, 2 * v, N), (2 * v + 1, 2 * u, N)]
    errado = edmonds_karp(2 * n, arcos, 2 * x, 2 * y + 1)[0]
    certo = conectividade_vertice(n, E, x, y)[0]
    assert errado != certo
    print(f"sanidade: modelo errado da {errado}, o certo da {certo} (o teste pega o erro)")


if __name__ == "__main__":
    teste_tabelas()
    teste_familias()
    teste_sanidade()
    teste_aleatorios()
    print("todos os testes passaram")
