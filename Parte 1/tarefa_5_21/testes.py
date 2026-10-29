import random
import networkx as nx
from prim import prim, msts, verifica_prop_5_20

G1 = [(1, 2, 4), (1, 3, 2), (2, 3, 1), (2, 4, 5), (3, 4, 8), (3, 5, 10), (4, 5, 2), (4, 6, 6), (5, 6, 3)]
K4_1 = [(1, 2, 1), (1, 3, 1), (1, 4, 1), (2, 3, 1), (2, 4, 1), (3, 4, 1)]

# (nome, n, arestas, raiz, nº arvores, peso, nº MSTs, F esperado)
TABELA = [
    ("G1", 6, G1, 1, 55, 13, 1, [2, 3, 4, 7, 9]),
    ("G1 r=4", 6, G1, 4, 55, 13, 1, [7, 9, 4, 3, 2]),
    ("triangulo", 3, [(1, 2, 1), (2, 3, 1), (1, 3, 1)], 1, 3, 2, 3, [1, 2]),
    ("K4 tudo 1", 4, K4_1, 1, 16, 3, 16, [1, 2, 3]),
    ("quadrado + diagonal", 4, [(1, 2, 1), (2, 3, 1), (3, 4, 1), (4, 1, 1), (1, 3, 2)], 1, 8, 3, 4, [1, 2, 3]),
    ("paralelas", 3, [(1, 2, 5), (1, 2, 3), (2, 3, 4), (2, 3, 4)], 1, 4, 7, 2, [2, 3]),
    ("com laco", 3, [(1, 1, 0), (1, 2, 2), (2, 3, 1), (1, 3, 3)], 1, 3, 3, 1, [2, 3]),
    ("K4 pesos", 4, [(1, 2, 3), (1, 3, 1), (1, 4, 4), (2, 3, 2), (2, 4, 6), (3, 4, 5)], 1, 16, 7, 1, [2, 4, 3]),
]


def peso(arestas, F):
    return sum(arestas[i - 1][2] for i in F)


def corte(arestas, S):
    return [j for j, (a, b, _) in enumerate(arestas, 1) if (a in S) != (b in S)]


def eh_arvore_geradora(n, arestas, F):
    if len(F) != n - 1:
        return False
    pai = list(range(n + 1))

    def acha(x):
        while pai[x] != x:
            x = pai[x]
        return x
    for i in F:
        u, v, _ = arestas[i - 1]
        a, b = acha(u), acha(v)
        if a == b:
            return False
        pai[a] = b
    return True


def confere(n, arestas, r, F, log, melhor, lista):
    assert eh_arvore_geradora(n, arestas, F)
    assert peso(arestas, F) == melhor
    for k, (S, c, esc) in enumerate(log, 1):
        assert len(S) == k
        assert c == corte(arestas, set(S))                        # auditoria da fila
        assert esc in c and arestas[esc - 1][2] == min(arestas[j - 1][2] for j in c)
    assert verifica_prop_5_20(F, lista)


def teste_tabela():
    for nome, n, E, r, narv, p, nm, Fesp in TABELA:
        F, log = prim(n, E, r)
        assert F == Fesp, (nome, F)
        melhor, lista, total = msts(n, E)
        assert (total, melhor, len(lista)) == (narv, p, nm), (nome, total, melhor, len(lista))
        confere(n, E, r, F, log, melhor, lista)
    try:
        prim(4, [(1, 2, 1), (3, 4, 1)], 1)
        assert False
    except ValueError:
        pass
    F, log = prim(1, [], 1)
    assert F == [] and log == []
    print("tabela ok (9 linhas)")


def grafo_ponderado_conexo(n, extra, pesos=(1, 2, 3), rng=random):
    E = [(rng.randint(1, i - 1), i, rng.choice(pesos)) for i in range(2, n + 1)]
    for _ in range(extra):
        u, v = rng.sample(range(1, n + 1), 2)
        E.append((u, v, rng.choice(pesos)))
    rng.shuffle(E)
    return n, E


def prim_regra(n, arestas, r, escolhe, rng):
    # variante sem fila: varre o corte e deixa "escolhe" decidir
    S = {r}
    F = []
    while len(S) < n:
        c = corte(arestas, S)
        j = escolhe(c, rng)
        F.append(j)
        u, v, _ = arestas[j - 1]
        S.add(v if u in S else u)
    return F


def teste_desempate_e_regra_errada():
    rng = random.Random(8)
    violacoes = 0
    reprovadas = 0
    total = 0
    for _ in range(300):
        n = rng.randint(2, 6)
        extra = rng.randint(0, 11 - (n - 1))
        n, E = grafo_ponderado_conexo(n, extra, rng=rng)
        melhor, lista, _ = msts(n, E)
        F, log = prim(n, E, 1)
        confere(n, E, 1, F, log, melhor, lista)

        def aleatoria(c, rng):
            mn = min(E[j - 1][2] for j in c)
            return rng.choice([j for j in c if E[j - 1][2] == mn])

        def pesada(c, rng):
            mx = max(E[j - 1][2] for j in c)
            return min(j for j in c if E[j - 1][2] == mx)

        for _ in range(5):
            F2 = prim_regra(n, E, 1, aleatoria, rng)
            if not verifica_prop_5_20(F2, lista):
                violacoes += 1
        F3 = prim_regra(n, E, 1, pesada, rng)
        if not (verifica_prop_5_20(F3, lista) and peso(E, F3) == melhor):
            reprovadas += 1
        total += 1
    assert violacoes == 0
    print(f"desempate aleatorio: {violacoes} violacoes em 1500 execucoes")
    print(f"regra errada (mais pesada) reprovada em {100 * reprovadas / total:.0f}% das instancias")
    assert reprovadas > 0.5 * total


def teste_networkx():
    rng = random.Random(5)
    for _ in range(200):
        n = rng.randint(2, 12)
        n, E = grafo_ponderado_conexo(n, rng.randint(0, 2 * n), pesos=range(1, 20), rng=rng)
        # networkx so com grafos simples: fica a aresta mais leve de cada par
        G = nx.Graph()
        for u, v, w in E:
            if u != v and (not G.has_edge(u, v) or G[u][v]["w"] > w):
                G.add_edge(u, v, w=w)
        esperado = nx.minimum_spanning_tree(G, weight="w").size(weight="w")
        pesos = set()
        for r in range(1, n + 1):
            F, _ = prim(n, E, r, registrar=False)
            pesos.add(peso(E, F))
        assert pesos == {esperado}
    print("comparacao com networkx e independencia da raiz ok")


if __name__ == "__main__":
    teste_tabela()
    teste_desempate_e_regra_errada()
    teste_networkx()
    print("todos os testes passaram")
