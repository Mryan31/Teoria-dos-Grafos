import itertools
import random
import collections
import networkx as nx
from prufer import codificar, decodificar


def conj(E):
    return {frozenset(e) for e in E}


COD = [  # (n, arestas, codigo, folhas)
    (7, [(1, 4), (3, 4), (4, 2), (2, 6), (5, 6), (6, 7)], [4, 4, 2, 6, 6], [1, 3, 4, 2, 5]),
    (5, [(1, 2), (2, 3), (3, 4), (4, 5)], [2, 3, 4], [1, 2, 3]),
    (5, [(1, 2), (1, 3), (1, 4), (1, 5)], [1, 1, 1], [2, 3, 4]),
    (6, [(2, 1), (2, 3), (2, 4), (2, 5), (2, 6)], [2, 2, 2, 2], [1, 3, 4, 5]),
    (2, [(1, 2)], [], []),
    (3, [(1, 2), (2, 3)], [2], [1]),
    (3, [(1, 3), (3, 2)], [3], [1]),
    (8, [(1, 2), (1, 3), (2, 4), (2, 5), (3, 6), (3, 7), (7, 8)], [2, 2, 1, 3, 3, 7], [4, 5, 2, 1, 6, 3]),
]

DEC = [  # (codigo, arestas)
    ([3, 3, 3], [(1, 3), (2, 3), (3, 4), (3, 5)]),
    ([1, 2, 3, 4], [(1, 2), (1, 5), (2, 3), (3, 4), (4, 6)]),
    ([4, 3, 2, 1], [(1, 2), (1, 6), (2, 3), (3, 4), (4, 5)]),
    ([2, 2], [(1, 2), (2, 3), (2, 4)]),
    ([1], [(1, 2), (1, 3)]),
    ([], [(1, 2)]),
    ([7, 7, 7, 7, 7], [(1, 7), (2, 7), (3, 7), (4, 7), (5, 7), (6, 7)]),
    ([1, 2, 1, 2, 1, 2], [(1, 2), (1, 3), (1, 5), (1, 7), (2, 4), (2, 6), (2, 8)]),
]


def teste_tabelas():
    for n, E, cod, folhas in COD:
        P, X = codificar(n, E)
        assert P == cod and X == folhas, (E, P, X)
    for cod, E in DEC:
        assert conj(decodificar(cod)) == conj(E), cod
    print("tabelas ok (8 + 8 linhas)")


def todas_as_arvores(n):
    # independente do Prufer: subconjuntos de n-1 arestas de K_n sem ciclo (union-find)
    pares = list(itertools.combinations(range(1, n + 1), 2))
    for sub in itertools.combinations(pares, n - 1):
        pai = list(range(n + 1))

        def acha(x):
            while pai[x] != x:
                x = pai[x]
            return x
        ok = True
        for u, v in sub:
            a, b = acha(u), acha(v)
            if a == b:
                ok = False
                break
            pai[a] = b
        if ok:
            yield frozenset(frozenset(e) for e in sub)


def teste_exaustivo():
    for n in range(2, 8):
        arvores = set(todas_as_arvores(n))
        assert len(arvores) == n ** (n - 2), (n, len(arvores))
        codigos = set()
        for a in itertools.product(range(1, n + 1), repeat=n - 2):
            T = conj(decodificar(list(a)))
            assert T in arvores
            assert codificar(n, [tuple(e) for e in T])[0] == list(a)
        for T in arvores:
            E = [tuple(e) for e in T]
            P, _ = codificar(n, E)
            assert conj(decodificar(P)) == T
            codigos.add(tuple(P))
        assert len(codigos) == n ** (n - 2)   # injetividade
    print("exaustivo n=2..7 ok (Cayley, ida e volta, injetividade)")


def teste_grau():
    random.seed(4)
    for _ in range(300):
        n = random.randint(2, 40)
        E = [(random.randint(1, i - 1), i) for i in range(2, n + 1)]
        P, _ = codificar(n, E)
        grau = collections.Counter(v for e in E for v in e)
        oc = collections.Counter(P)
        for v in range(1, n + 1):
            assert grau[v] == 1 + oc[v]
    print("grau = 1 + ocorrencias ok")


def teste_networkx():
    random.seed(9)
    for _ in range(300):
        n = random.randint(2, 30)
        E = [(random.randint(1, i - 1), i) for i in range(2, n + 1)]
        perm = list(range(1, n + 1))
        random.shuffle(perm)
        E = [(perm[u - 1], perm[v - 1]) for u, v in E]
        P, _ = codificar(n, E)
        T = nx.Graph([(u - 1, v - 1) for u, v in E])
        assert [a + 1 for a in nx.to_prufer_sequence(T)] == P
        T2 = nx.from_prufer_sequence([a - 1 for a in P])
        assert conj((u + 1, v + 1) for u, v in T2.edges()) == conj(decodificar(P))
    print("comparacao com networkx ok (300 arvores)")


def teste_invalidas():
    ruins = [
        (4, [(1, 2), (2, 3), (3, 1)]),           # ciclo
        (4, [(1, 2), (3, 4)]),                   # desconexa (e poucas arestas)
        (4, [(1, 2), (2, 3), (3, 4), (4, 1)]),   # arestas demais
        (1, []),
    ]
    for n, E in ruins:
        try:
            codificar(n, E)
            assert False, E
        except ValueError:
            pass
    for P in ([0, 1], [5, 1]):
        try:
            decodificar(P)
            assert False, P
        except ValueError:
            pass
    print("entradas invalidas rejeitadas")


if __name__ == "__main__":
    teste_tabelas()
    teste_exaustivo()
    teste_grau()
    teste_networkx()
    teste_invalidas()
    print("todos os testes passaram")
