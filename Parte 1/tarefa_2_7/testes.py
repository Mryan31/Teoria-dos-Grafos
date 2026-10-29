import itertools
import random
import networkx as nx
from havel_hakimi import havel_hakimi, graus_da_realizacao


def erdos_gallai(d):
    # Teorema 2.15
    d = sorted(d, reverse=True)
    n = len(d)
    if sum(d) % 2 == 1:
        return False
    for k in range(1, n + 1):
        esq = sum(d[:k])
        dir_ = k * (k - 1) + sum(min(x, k) for x in d[k:])
        if esq > dir_:
            return False
    return True


def hh_sem_reordenar(d):
    # versao "errada": ordena so no inicio e nunca mais
    cur = sorted(d, reverse=True)
    while cur:
        r = cur[0]
        cur = cur[1:]
        if r == 0:
            return True
        if r > len(cur):
            return False
        for j in range(r):
            cur[j] -= 1
            if cur[j] < 0:
                return False
    return True


def sequencias(n):
    # nao crescentes, entradas em 0..n-1
    for d in itertools.combinations_with_replacement(range(n - 1, -1, -1), n):
        yield list(d)


def confere_realizacao(d, E):
    assert graus_da_realizacao(len(d), E) == list(d)
    assert all(a != b for a, b in E)
    assert len({frozenset(e) for e in E}) == len(E)
    assert 2 * len(E) == sum(d)


TABELA = [
    ([4, 3, 3, 2, 2, 2], True, [(1, 2), (1, 3), (1, 4), (1, 5), (2, 3), (2, 6), (3, 4), (5, 6)]),
    ([5, 4, 3, 3, 2, 1], True, [(1, 2), (1, 3), (1, 4), (1, 5), (1, 6), (2, 3), (2, 4), (2, 5), (3, 4)]),
    ([4, 4, 3, 2, 1, 0], False, None),
    ([3, 3, 3, 3, 2, 2], True, [(1, 2), (1, 3), (1, 4), (2, 3), (2, 4), (5, 6), (5, 3), (4, 6)]),
    ([3, 3, 3, 1], False, None),
    ([3, 3, 1, 1], False, None),
    ([2, 2, 1], False, None),
    ([1], False, None),
    ([0, 0, 0], True, []),
    ([2, 1, 1, 2], True, [(1, 4), (1, 2), (3, 4)]),
    ([6, 1, 1, 1, 1, 1, 1], True, [(1, i) for i in range(2, 8)]),
    ([5, 5, 5, 5, 5, 5], True, None),
    ([2, 2, 1, 1], True, None),
]


def teste_tabela():
    for d, esperado, arestas in TABELA:
        ok, E, passos, obs = havel_hakimi(d)
        assert ok == esperado, d
        if ok:
            confere_realizacao(d, E)
            if arestas is not None:
                assert {frozenset(e) for e in E} == {frozenset(e) for e in arestas}, d
    # cadeias e obstrucoes que o guia mostra
    assert havel_hakimi([4, 3, 3, 2, 2, 2])[2] == [[4, 3, 3, 2, 2, 2], [2, 2, 2, 1, 1], [1, 1, 1, 1], [1, 1, 0], [0, 0]]
    ok, E, passos, obs = havel_hakimi([4, 4, 3, 2, 1, 0])
    assert passos[1] == [3, 2, 1, 0, 0] and obs == (1, "entrada negativa", 5)
    assert havel_hakimi([3, 3, 3, 1])[2][1] == [2, 2, 0]
    assert havel_hakimi([3, 3, 1, 1])[2][1] == [2, 0, 0]
    assert havel_hakimi([1])[3] == (0, "r >= n", 1, 1)
    assert len(havel_hakimi([5] * 6)[1]) == 15
    print("tabela ok")


def teste_exaustivo():
    contagem = []
    for n in range(1, 8):
        c = 0
        for d in sequencias(n):
            ok, E, _, _ = havel_hakimi(d)
            assert ok == erdos_gallai(d), d
            assert ok == nx.is_graphical(d, method="hh") == nx.is_graphical(d, method="eg")
            if ok:
                confere_realizacao(d, E)
                c += 1
        contagem.append(c)
    assert contagem == [1, 2, 4, 11, 31, 102, 342], contagem
    print("exaustivo n<=7 ok:", contagem)


def teste_forca_bruta():
    for n in range(1, 7):
        pares = list(itertools.combinations(range(n), 2))
        achadas = set()
        for mask in range(1 << len(pares)):
            g = [0] * n
            for i, (a, b) in enumerate(pares):
                if mask >> i & 1:
                    g[a] += 1
                    g[b] += 1
            achadas.add(tuple(sorted(g, reverse=True)))
        aceitas = {tuple(d) for d in sequencias(n) if havel_hakimi(d)[0]}
        assert achadas == aceitas, n
    print("forca bruta n<=6 ok")


def teste_sensibilidade():
    rejeitadas = []
    for n in range(1, 7):
        for d in sequencias(n):
            if havel_hakimi(d)[0] and not hh_sem_reordenar(d):
                rejeitadas.append(d)
    menor = min(rejeitadas, key=lambda d: (len(d), d))
    print(f"sem reordenar: {len(rejeitadas)} sequencias graficas rejeitadas, menor {menor}")
    assert len(rejeitadas) == 32
    assert menor == [2, 2, 1, 1]


def teste_invariancia():
    random.seed(5)
    for _ in range(500):
        n = random.randint(1, 8)
        d = [random.randint(0, n - 1) for _ in range(n)]
        ok = havel_hakimi(d)[0]
        p = list(d)
        random.shuffle(p)
        assert havel_hakimi(p)[0] == ok
        if sum(d) % 2 == 1:
            assert not ok
    print("invariancia por permutacao e soma impar ok")


if __name__ == "__main__":
    teste_tabela()
    teste_exaustivo()
    teste_forca_bruta()
    teste_sensibilidade()
    teste_invariancia()
    print("todos os testes passaram")
