import itertools
import random
from fluxo import residuos, circulacao_modular, corrigir, confere

PET_PE = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 0, 1, 2, 3, 4]
PET_CAB = [1, 2, 3, 4, 0, 7, 8, 9, 5, 6, 5, 6, 7, 8, 9]
K4_PE = [0, 0, 0, 1, 1, 2]
K4_CAB = [1, 2, 3, 2, 3, 3]

# (n, k, pe, cab, val, b inicial, K0, [(s, t, P)], K depois de cada correcao, f esperado)
TABELA = [
    (2, 3, [0, 0, 0], [1, 1, 1], [1, 1, 1], [3, -3], 6, [(0, 1, [0])], None, [-2, 1, 1]),
    (4, 3, [0, 1, 2, 0], [1, 2, 3, 3], [1, 1, 1, 2], [3, 0, 0, -3], 6, [(0, 3, [3])], None, [1, 1, 1, -1]),
    (4, 2, [0, 1, 3, 0], [1, 2, 2, 3], [1, 1, 1, 1], [2, 0, -2, 0], 4, [(0, 2, [0, 1])], None, [-1, -1, 1, 1]),
    (5, 2, [0, 1, 2, 3, 0], [1, 2, 3, 4, 4], [1] * 5, [2, 0, 0, 0, -2], 4, [(0, 4, [4])], None, [1, 1, 1, 1, -1]),
    (2, 5, [0] * 4, [1] * 4, [1, 1, 1, 2], [5, -5], 10, [(0, 1, [0])], None, [-4, 1, 1, 2]),
    (2, 2, [0, 0, 0], [1, 1, 0], [1, 1, 1], [2, -2], 4, [(0, 1, [0])], None, [-1, 1, 1]),
    (4, 4, K4_PE, K4_CAB, [2, 3, 3, 3, 3, 2], [8, 4, -4, -8], 24, [(0, 2, [1]), (0, 3, [2]), (1, 3, [4])],
     [16, 8, 0], [2, -1, -1, 3, -1, 2]),
    (4, 4, K4_PE, K4_CAB, [3, 2, 3, 1, 2, 3], [8, 0, 0, -8], 16, [(0, 3, [2]), (0, 3, [0, 4])], None,
     [-1, 2, -1, 1, -2, 3]),
    (10, 5, PET_PE, PET_CAB, [3, 4, 1, 3, 2, 3, 1, 1, 4, 2, 4, 4, 3, 3, 1], [5, 5, 0, 5, 0, -5, -5, -5, 0, 0], 30,
     [(0, 5, [10]), (1, 6, [11]), (3, 7, [13, 8, 5])], [20, 10, 0],
     [3, 4, 1, 3, 2, -2, 1, 1, -1, 2, -1, -1, 3, -2, 1]),
]


def teste_tabela():
    for n, k, pe, cab, val, b0, K0esp, corr, Ks, fesp in TABELA:
        assert residuos(n, pe, cab, val) == b0
        assert circulacao_modular(n, pe, cab, val, k) == []
        f, log, K0 = corrigir(n, pe, cab, val, k)
        assert K0 == K0esp
        assert [(l["s"], l["t"], l["P"]) for l in log] == corr, log
        if Ks:
            assert [l["K"] for l in log] == Ks
        assert f == fesp, f
        assert confere(n, pe, cab, f, k)
    print("tabela ok (9 casos)")


def teste_rejeicoes():
    assert circulacao_modular(2, [0], [1], [1], 3) == [0, 1]
    assert circulacao_modular(4, K4_PE, K4_CAB, [1] * 6, 3) == [1, 2]
    assert residuos(4, K4_PE, K4_CAB, [1] * 6) == [3, 1, -1, -3]
    # representantes: (4, -2, 7) com k = 3 e o mesmo que (1, 1, 1)
    val = [x % 3 for x in (4, -2, 7)]
    assert val == [1, 1, 1]
    assert corrigir(2, [0, 0, 0], [1, 1, 1], val, 3)[0] == [-2, 1, 1]
    print("rejeicoes e representantes ok")


def gerar(n, ciclos, k, rng, maxlen=None):
    """Uniao de ciclos dirigidos com valor constante c (conserva exatamente); depois cada arco e
    invertido com prob. 1/2 trocando val por k - val (conserva so modulo k). Ordem embaralhada."""
    arcos = []
    for _ in range(ciclos):
        L = rng.randint(2, min(n, maxlen or n))
        vs = rng.sample(range(n), L)
        c = rng.randint(1, k - 1)
        for i in range(L):
            arcos.append((vs[i], vs[(i + 1) % L], c))
    out = []
    for a, b, c in arcos:
        if rng.random() < 0.5:
            out.append((b, a, k - c))
        else:
            out.append((a, b, c))
    rng.shuffle(out)
    return [a for a, _, _ in out], [b for _, b, _ in out], [c for _, _, c in out]


def propriedades(n, pe, cab, val, k, rng):
    m = len(pe)
    assert circulacao_modular(n, pe, cab, val, k) == []
    f, log, K0 = corrigir(n, pe, cab, val, k)
    assert confere(n, pe, cab, f, k)                                   # (16.1)
    assert all((f[e] - val[e]) % k == 0 for e in range(m))             # levantamento
    Ks = [K0] + [l["K"] for l in log]
    assert all(Ks[i] - Ks[i + 1] == 2 * k for i in range(len(log)))    # cai exatamente 2k
    assert K0 % (2 * k) == 0
    assert K0 <= 2 * m * (k - 1)
    assert len(log) == K0 // (2 * k)
    if m >= 1:
        assert len(log) < m
    # invariancia: reorientar um arco (val -> k - val) continua valido
    if m:
        e = rng.randrange(m)
        pe2, cab2, val2 = list(pe), list(cab), list(val)
        pe2[e], cab2[e] = cab2[e], pe2[e]
        val2[e] = k - val2[e]
        assert circulacao_modular(n, pe2, cab2, val2, k) == []
        f2, _, _ = corrigir(n, pe2, cab2, val2, k)
        assert confere(n, pe2, cab2, f2, k)
    return len(log)


def teste_aleatorios():
    rng = random.Random(16)
    total = 0
    corr = 0
    for _ in range(3000):
        n = rng.randint(2, 12)
        k = rng.randint(2, 7)
        pe, cab, val = gerar(n, rng.randint(1, 6), k, rng, maxlen=rng.choice([None, 3, 5]))
        corr += propriedades(n, pe, cab, val, k, rng)
        total += 1
    print(f"{total} instancias aleatorias ok (propriedades 1-5), {corr} correcoes no total")


def conta_circulacoes(n, pe, cab, k):
    """Numero de Z_k-circulacoes nunca zero: escolhe os valores das arestas fora de uma arvore
    geradora (o resto fica determinado) e confere se nenhuma aresta zera."""
    m = len(pe)
    pai = list(range(n))

    def acha(x):
        while pai[x] != x:
            x = pai[x]
        return x
    arvore, fora = [], []
    for e in range(m):
        a, b = acha(pe[e]), acha(cab[e])
        if a != b:
            pai[a] = b
            arvore.append(e)
        else:
            fora.append(e)
    conta = 0
    for escolha in itertools.product(range(1, k), repeat=len(fora)):
        val = [0] * m
        for e, x in zip(fora, escolha):
            val[e] = x
        # resolve as arestas da arvore tirando folhas
        b = residuos(n, pe, cab, val)
        resto = set(arvore)
        while resto:
            grau = {}
            for e in resto:
                grau[pe[e]] = grau.get(pe[e], 0) + 1
                grau[cab[e]] = grau.get(cab[e], 0) + 1
            e = next(e for e in resto if grau[pe[e]] == 1 or grau[cab[e]] == 1)
            folha = pe[e] if grau[pe[e]] == 1 else cab[e]
            x = (-b[folha]) % k if folha == pe[e] else b[folha] % k
            val[e] = x
            b[pe[e]] += x
            b[cab[e]] -= x
            resto.remove(e)
        if all(v % k for v in val):
            assert circulacao_modular(n, pe, cab, val, k) == []
            f, _, _ = corrigir(n, pe, cab, val, k)
            assert confere(n, pe, cab, f, k)
            conta += 1
    return conta


def teste_contagem():
    k4 = [conta_circulacoes(4, K4_PE, K4_CAB, k) for k in (3, 4, 5)]
    pet = [conta_circulacoes(10, PET_PE, PET_CAB, k) for k in (4, 5)]
    assert k4 == [0, 6, 24] and pet == [0, 240], (k4, pet)
    print(f"Teor. 16.10: K4 com k = 3, 4, 5 -> {k4}; Petersen com k = 4, 5 -> {pet}; todas levantaram")


if __name__ == "__main__":
    teste_tabela()
    teste_rejeicoes()
    teste_aleatorios()
    teste_contagem()
    print("todos os testes passaram")
