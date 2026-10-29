import itertools
import random
from fractions import Fraction as F
from birkhoff import birkhoff, verificar, emparelhamento_maximo, positivas


def perm_matriz(s):
    n = len(s)
    return [[F(1) if s[i] == j else F(0) for j in range(n)] for i in range(n)]


def combina(pesos_perms, n):
    X = [[F(0)] * n for _ in range(n)]
    for a, s in pesos_perms:
        for i in range(n):
            X[i][s[i]] += a
    return X


def M(linhas, den=1):
    return [[F(x, den) for x in l] for l in linhas]


TABELA = [  # (nome, X, nz, termos esperados)
    ("Exemplo 10.8", M([[1, 2, 0], [0, 1, 2], [2, 0, 1]], 3), 6, [(F(1, 3), [0, 1, 2]), (F(2, 3), [1, 2, 0])]),
    ("permutacao", perm_matriz([1, 2, 0]), 3, [(F(1), [1, 2, 0])]),
    ("J/3", M([[1] * 3] * 3, 3), 9, [(F(1, 3), [0, 1, 2]), (F(1, 3), [1, 2, 0]), (F(1, 3), [2, 0, 1])]),
    ("J/4", M([[1] * 4] * 4, 4), 16, [(F(1, 4), [0, 1, 2, 3]), (F(1, 4), [1, 0, 3, 2]),
                                       (F(1, 4), [2, 3, 0, 1]), (F(1, 4), [3, 2, 1, 0])]),
    ("I4", perm_matriz([0, 1, 2, 3]), 4, [(F(1), [0, 1, 2, 3])]),
    ("dois blocos", combina([(F(1, 2), [0, 1, 2, 3]), (F(1, 2), [1, 0, 3, 2])], 4), 8,
     [(F(1, 2), [0, 1, 2, 3]), (F(1, 2), [1, 0, 3, 2])]),
    ("W4", combina([(F(1, 2), [0, 1, 2, 3]), (F(1, 4), [1, 0, 3, 2]), (F(1, 4), [2, 3, 0, 1])], 4), 12,
     [(F(1, 2), [0, 1, 2, 3]), (F(1, 4), [1, 0, 3, 2]), (F(1, 4), [2, 3, 0, 1])]),
    ("Z9", M([[6, 2, 1], [2, 5, 2], [1, 2, 6]], 9), 9,
     [(F(5, 9), [0, 1, 2]), (F(1, 9), [0, 2, 1]), (F(1, 9), [1, 0, 2]), (F(1, 9), [1, 2, 0]), (F(1, 9), [2, 0, 1])]),
]


def confere(X, termos, hist, soma=1):
    verificar(X, termos, soma)
    n = len(X)
    nz = positivas(X)
    # cada sigma so usava posicoes positivas de R no momento do passo
    R = [[F(x) for x in l] for l in X]
    for a, s in termos:
        assert all(R[i][s[i]] > 0 for i in range(n))
        for i in range(n):
            R[i][s[i]] -= a
    npos = [h[0] for h in hist]
    assert all(npos[i] > npos[i + 1] for i in range(len(npos) - 1))
    assert len(termos) <= nz - n + 1 <= n * n
    assert hist[-1][2] == 0


def teste_tabela():
    for nome, X, nz, esperado in TABELA:
        assert positivas(X) == nz, nome
        termos, hist = birkhoff(X)
        assert termos == esperado, (nome, termos)
        confere(X, termos, hist)
    # um passo do Exemplo 10.8: sigma = (0,1,2), alfa = 1/3, R = (1/3)[[0,2,0],[0,0,2],[2,0,0]]
    termos, hist = birkhoff(TABELA[0][1])
    assert hist[0] == (6, F(1, 3), F(2, 3))
    assert {a for a, _ in termos} == {F(1, 3), F(2, 3)}
    print("tabela ok (8 matrizes), Exemplo 10.8 ok")


def teste_emparelhamento_copiado():
    adj = [[0], [1], [2]]
    assert emparelhamento_maximo(3, 3, adj)[0] == [0, 1, 2]
    adj = [[0, 1, 2]] * 3
    assert sorted(emparelhamento_maximo(3, 3, adj)[0]) == [0, 1, 2]
    print("emparelhamento_maximo copiado da 7.11 ok")


def teste_generalizacao():
    X = [[5 * x for x in l] for l in TABELA[7][1]]   # 5 * Z9: somas iguais a 5
    termos, hist = birkhoff(X, soma=5)
    confere(X, termos, hist, soma=5)
    assert sum(a for a, _ in termos) == 5
    print("generalizacao (Ex. 10.9) ok: 5*Z9 da soma dos alfas = 5")


def ds_aleatoria(n, k, rng):
    pesos = [rng.randint(1, 9) for _ in range(k)]
    tot = sum(pesos)
    perms = []
    for _ in range(k):
        s = list(range(n))
        rng.shuffle(s)
        perms.append(s)
    return combina([(F(p, tot), s) for p, s in zip(pesos, perms)], n)


def teste_aleatorios():
    rng = random.Random(10)
    for _ in range(300):
        n = rng.randint(1, 6)
        X = ds_aleatoria(n, rng.randint(1, 6), rng)
        termos, hist = birkhoff(X)
        confere(X, termos, hist)
    print("300 aleatorios exatos ok")


def custo(W, s):
    return sum(W[i][s[i]] for i in range(len(s)))


def teste_corolario():
    W = [[4, 1, 3], [2, 0, 5], [3, 2, 2]]
    custos = {s: custo(W, s) for s in itertools.permutations(range(3))}
    assert [custos[s] for s in sorted(custos)] == [6, 11, 5, 9, 7, 6]
    X = M([[1] * 3] * 3, 3)
    termos, _ = birkhoff(X)
    cX = sum(W[i][j] * X[i][j] for i in range(3) for j in range(3))
    cdec = min(custo(W, s) for _, s in termos)
    assert (min(custos.values()), cdec, cX) == (5, 6, F(22, 3))
    rng = random.Random(4)
    for _ in range(200):
        n = rng.randint(1, 6)
        W = [[rng.randint(0, 9) for _ in range(n)] for _ in range(n)]
        X = ds_aleatoria(n, rng.randint(1, 6), rng)
        termos, _ = birkhoff(X)
        otimo = min(custo(W, s) for s in itertools.permutations(range(n)))
        cdec = min(custo(W, s) for _, s in termos)
        cX = sum(W[i][j] * X[i][j] for i in range(n) for j in range(n))
        assert otimo <= cdec <= cX
    print("Corolario 10.11 ok (exemplo fixo 5 <= 6 <= 22/3 e 200 aleatorios)")


def teste_invalidas():
    for X in ([[F(1, 2), F(1, 2)], [F(1, 2), F(1, 3)]], [[F(2), F(-1)], [F(-1), F(2)]], [[F(1), F(0)]]):
        try:
            birkhoff(X)
            assert False
        except ValueError:
            pass
    assert F("0.1") == F(1, 10) and F(0.1) != F(1, 10)
    print("entradas invalidas rejeitadas")


if __name__ == "__main__":
    teste_emparelhamento_copiado()
    teste_tabela()
    teste_generalizacao()
    teste_aleatorios()
    teste_corolario()
    teste_invalidas()
    print("todos os testes passaram")
