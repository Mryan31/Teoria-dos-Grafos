import random
from fractions import Fraction
import networkx as nx
from nucleo_denso import nucleo, montar_adj

K4 = [(1, 2), (1, 3), (1, 4), (2, 3), (2, 4), (3, 4)]
K5 = [(a, b) for a in range(1, 6) for b in range(a + 1, 6)]
K5b = [(a, b) for i, a in enumerate([1, 3, 4, 5, 7]) for b in [1, 3, 4, 5, 7][i + 1:]]
PETERSEN = [(1, 2), (2, 3), (3, 4), (4, 5), (5, 1), (1, 6), (2, 7), (3, 8), (4, 9), (5, 10),
            (6, 8), (8, 10), (10, 7), (7, 9), (9, 6)]
K4_2 = [(a + 4, b + 4) for a, b in K4]

# (nome, n, arestas, removidos, H, mH, delta)
TABELA = [
    ("triangulo + pendente", 4, [(1, 2), (2, 3), (1, 3), (3, 4)], [(4, 1)], [1, 2, 3], 3, 2),
    ("K4 + cauda", 7, K4 + [(4, 5), (5, 6), (6, 7)], [(7, 1), (6, 1), (5, 1)], [1, 2, 3, 4], 6, 3),
    ("K5 + 1-6 + 2-7", 7, K5 + [(1, 6), (2, 7)], [(6, 1), (7, 1)], [1, 2, 3, 4, 5], 10, 4),
    ("limiar sobe", 7, K5b + [(6, 3), (6, 5)], [(2, 0), (6, 2)], [1, 3, 4, 5, 7], 10, 4),
    ("dois K4 + ponte + folha", 9, K4 + K4_2 + [(4, 5), (8, 9)], [(9, 1)], list(range(1, 9)), 13, 3),
    ("K4 + estrela", 8, K4 + [(4, 5), (5, 6), (5, 7), (5, 8)], [(6, 1), (7, 1), (8, 1), (5, 1)], [1, 2, 3, 4], 6, 3),
    ("P5", 5, [(1, 2), (2, 3), (3, 4), (4, 5)], [], [1, 2, 3, 4, 5], 4, 1),
    ("K1,5", 6, [(1, i) for i in range(2, 7)], [], list(range(1, 7)), 5, 1),
    ("Petersen", 10, PETERSEN, [], list(range(1, 11)), 15, 3),
    ("C6 + corda", 6, [(1, 2), (2, 3), (3, 4), (4, 5), (5, 6), (6, 1), (1, 4)], [], list(range(1, 7)), 7, 2),
]


def nucleo_ingenuo(n, arestas):
    # varre os vivos a cada rodada; mesma regra de desempate (menor grau, menor rotulo)
    adj = montar_adj(n, arestas)
    vivos = set(range(1, n + 1))
    mF, nF = len(arestas), n
    log = []
    while True:
        melhor = None
        for v in sorted(vivos):
            d = len(adj[v] & vivos)
            if melhor is None or d < melhor[0]:
                melhor = (d, v)
        d, v = melhor
        if d * nF > mF:
            break
        log.append((v, d, mF, nF))
        vivos.remove(v)
        mF -= d
        nF -= 1
    return sorted(vivos), mF, log


def nucleo_menor_rotulo(n, arestas):
    # outra regra: remove o removivel de menor rotulo
    adj = montar_adj(n, arestas)
    vivos = set(range(1, n + 1))
    mF, nF = len(arestas), n
    while True:
        achou = False
        for v in sorted(vivos):
            d = len(adj[v] & vivos)
            if d * nF <= mF:
                vivos.remove(v)
                mF -= d
                nF -= 1
                achou = True
                break
        if not achou:
            return sorted(vivos), mF


def arestas_induzidas(arestas, H):
    s = set(H)
    return sum(1 for u, v in arestas if u in s and v in s)


def confere(n, arestas, H, mH, log):
    m = len(arestas)
    adj = montar_adj(n, arestas)
    s = set(H)
    assert len(H) > 0
    assert mH == arestas_induzidas(arestas, H)
    delta = min(len(adj[v] & s) for v in H)
    assert delta * len(H) > mH                         # delta(H) > grau_medio(H)/2
    assert Fraction(mH, len(H)) >= Fraction(m, n)      # grau_medio(H) >= grau_medio(G)
    dens = [Fraction(mF, nF) for _, _, mF, nF in log] + [Fraction(mH, len(H))]
    assert all(dens[i] <= dens[i + 1] for i in range(len(dens) - 1))
    for _, d, mF, nF in log:
        assert d * nF <= mF
    k = (2 * m // n) // 2                              # floor(grau_medio/2)
    if k >= 1:
        assert delta >= k + 1                          # Corolario 2.9
    return delta


def teste_tabela():
    for nome, n, E, rem, Hesp, mesp, desp in TABELA:
        H, mH, log = nucleo(n, E)
        assert [(v, d) for v, d, _, _ in log] == rem, (nome, log)
        assert H == Hesp, (nome, H)
        assert mH == mesp, nome
        assert confere(n, E, H, mH, log) == desp, nome
    try:
        nucleo(3, [])
        assert False
    except ValueError:
        pass
    print("tabela ok (11 linhas)")


def teste_aleatorios():
    random.seed(3)
    feitos = 0
    while feitos < 500:
        n = random.randint(2, 14)
        p = random.choice([0.15, 0.3, 0.5, 0.7])
        E = [(u, v) for u in range(1, n + 1) for v in range(u + 1, n + 1) if random.random() < p]
        if not E:
            continue
        H, mH, log = nucleo(n, E)
        confere(n, E, H, mH, log)
        H2, mH2, log2 = nucleo_ingenuo(n, E)
        assert (H, mH, log) == (H2, mH2, log2)
        H3, mH3 = nucleo_menor_rotulo(n, E)
        confere(n, E, H3, mH3, [])
        G = nx.Graph(E)
        S = G.subgraph(H)
        assert S.number_of_edges() == mH
        assert min(dict(S.degree()).values()) * len(H) > mH
        feitos += 1
    print("500 aleatorios ok (propriedades, versao ingenua, outra regra, networkx)")


if __name__ == "__main__":
    teste_tabela()
    teste_aleatorios()
    print("todos os testes passaram")
