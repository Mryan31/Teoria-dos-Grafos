import itertools
import random
import networkx as nx
from edmonds_karp import edmonds_karp, verificar

EX612 = [(0, 1, 1), (0, 2, 1), (1, 2, 1), (1, 3, 1), (2, 3, 1)]

# (nome, n, s, t, arcos, f0, valor, f, S, aumentos)
TABELA = [
    ("ex612", 4, 0, 3, EX612, None, 2, [1, 1, 0, 1, 1], {0}, 2),
    ("ex612 f0", 4, 0, 3, EX612, [1, 0, 1, 0, 1], 2, [1, 1, 0, 1, 1], {0}, 1),
    ("clrs", 6, 0, 5, [(0, 1, 16), (0, 2, 13), (1, 2, 10), (2, 1, 4), (1, 3, 12), (3, 2, 9), (2, 4, 14),
                       (4, 3, 7), (3, 5, 20), (4, 5, 4)], None, 23, [12, 11, 0, 0, 12, 0, 11, 7, 19, 4], {0, 1, 2, 4}, 3),
    ("paralelos", 2, 0, 1, [(0, 1, 2), (0, 1, 3)], None, 5, [2, 3], {0}, 2),
    ("antiparalelos", 3, 0, 2, [(0, 1, 3), (1, 0, 5), (1, 2, 2), (2, 1, 4)], None, 2, [2, 0, 2, 0], {0, 1}, 1),
    ("capacidade zero", 4, 0, 3, [(0, 1, 0), (1, 3, 5), (0, 2, 4), (2, 3, 0)], None, 0, [0, 0, 0, 0], {0, 2}, 0),
    ("desconexo", 4, 0, 3, [(0, 1, 3), (2, 3, 5)], None, 0, [0, 0], {0, 1}, 0),
    ("diamante", 4, 0, 3, [(0, 1, 1000), (0, 2, 1000), (1, 2, 1), (1, 3, 1000), (2, 3, 1000)], None,
     2000, [1000, 1000, 0, 1000, 1000], {0}, 2),
    ("usa arco reverso", 6, 0, 5, [(1, 5, 1), (4, 5, 1), (3, 4, 1), (3, 2, 2), (2, 1, 1), (0, 3, 1), (1, 4, 2),
                                   (2, 5, 2), (0, 1, 2), (0, 1, 2)], None, 3, [1, 1, 0, 1, 0, 1, 1, 1, 2, 0], {0, 1, 4}, 3),
]


def corte_valor(arcos, X):
    return sum(c for u, v, c in arcos if u in X and v not in X)


def enumera_cortes(n, arcos, s, t):
    outros = [v for v in range(n) if v not in (s, t)]
    cortes = []
    for r in range(len(outros) + 1):
        for extra in itertools.combinations(outros, r):
            X = {s, *extra}
            cortes.append((corte_valor(arcos, X), X))
    return cortes


def confere_tudo(n, arcos, s, t, f0=None):
    valor, f, S, log = edmonds_karp(n, arcos, s, t, f0, checar=True)
    verificar(n, arcos, s, t, valor, f, S)
    comp = [c for c, e in log]
    assert all(comp[i] <= comp[i + 1] for i in range(len(comp) - 1))   # Prop. 6.18
    assert len(log) <= n * max(1, len(arcos))
    return valor, f, S, log


def teste_tabela():
    for nome, n, s, t, arcos, f0, val, fesp, Sesp, aum in TABELA:
        valor, f, S, log = confere_tudo(n, arcos, s, t, f0)
        assert (valor, f, S, len(log)) == (val, fesp, Sesp, aum), (nome, valor, f, S, len(log))
    print("tabela ok (9 testes)")


def teste_ex612():
    # (b) partindo do fluxo da figura: um unico caminho, que usa uma entrada reversa
    trilhas = []
    valor, f, S, log = edmonds_karp(4, EX612, 0, 3, f0=[1, 0, 1, 0, 1], trilhas=trilhas)
    assert len(trilhas) == 1 and trilhas[0] == [2, 5, 6]
    assert any(i % 2 == 1 for i in trilhas[0])
    assert f == [1, 1, 0, 1, 1] and valor == 2
    # (c) Exercicio 6.13: os quatro lados da fonte (s=0, a=1, b=2)
    caps = {frozenset(X): corte_valor(EX612, X) for X in ({0}, {0, 1}, {0, 2}, {0, 1, 2})}
    assert caps == {frozenset({0}): 2, frozenset({0, 1}): 3, frozenset({0, 2}): 2, frozenset({0, 1, 2}): 2}
    for X, c in caps.items():
        if c == valor:  # corte minimo: (6.6) f = c nos arcos que saem, f = 0 nos que entram
            for k, (u, v, cap) in enumerate(EX612):
                if u in X and v not in X:
                    assert f[k] == cap
                if v in X and u not in X:
                    assert f[k] == 0
    print("Exemplo 6.12 (a), (b), (c) ok")


def teste_cortes_e_networkx():
    rng = random.Random(1)
    for _ in range(500):
        n = rng.randint(2, 7)
        m = rng.randint(0, 14)
        arcos = []
        for _ in range(m):
            u, v = rng.sample(range(n), 2)
            arcos.append((u, v, rng.randint(0, 5)))
        s, t = rng.sample(range(n), 2)
        valor, f, S, log = confere_tudo(n, arcos, s, t)
        cortes = enumera_cortes(n, arcos, s, t)
        minimo = min(c for c, X in cortes)
        assert minimo == valor
        minimizantes = [X for c, X in cortes if c == minimo]
        assert S in minimizantes
        assert len(S) == min(len(X) for X in minimizantes)
        G = nx.DiGraph()
        G.add_nodes_from(range(n))
        for u, v, c in arcos:
            if G.has_edge(u, v):
                G[u][v]["capacity"] += c
            else:
                G.add_edge(u, v, capacity=c)
        assert nx.maximum_flow_value(G, s, t) == valor
    print("500 aleatorios ok (enumeracao de cortes e networkx)")


def teste_erros():
    casos = [
        (2, [(0, 1, 1)], 0, 0),       # s = t
        (2, [(0, 1, -1)], 0, 1),      # capacidade negativa
        (2, [(0, 5, 1)], 0, 1),       # vertice fora
        (2, [(0, 0, 1)], 0, 1),       # laco
    ]
    for n, arcos, s, t in casos:
        try:
            edmonds_karp(n, arcos, s, t)
            assert False, arcos
        except ValueError:
            pass
    print("erros levantados corretamente")


if __name__ == "__main__":
    teste_tabela()
    teste_ex612()
    teste_cortes_e_networkx()
    teste_erros()
    print("todos os testes passaram")
