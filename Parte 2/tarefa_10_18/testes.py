import itertools
import random
import networkx as nx
from dilworth import dilworth, dilworth_indices, fecho, construir_BP, emparelhamento_maximo

EX1015 = ("a b c d e f".split(), [("a", "c"), ("b", "d"), ("c", "e"), ("c", "f"), ("d", "e"), ("d", "f")])
B3 = (["e", "1", "2", "3", "12", "13", "23", "123"],
      [("e", "1"), ("e", "2"), ("e", "3"), ("1", "12"), ("1", "13"), ("2", "12"), ("2", "23"),
       ("3", "13"), ("3", "23"), ("12", "123"), ("13", "123"), ("23", "123")])
DIV = ([str(i) for i in range(1, 13)], [(str(a), str(b)) for a in range(1, 13) for b in range(a + 1, 13) if b % a == 0])

TABELA = [  # (nome, poset, cadeias, T, M, K)
    ("Ex. 10.15", EX1015, "a c e | b d f", "e f", "a-c b-d c-e d-f", "a- b- c- d-"),
    ("ordem total", ("1 2 3 4 5".split(), [("1", "2"), ("2", "3"), ("3", "4"), ("4", "5")]),
     "1 2 3 4 5", "5", "1-2 2-3 3-4 4-5", "1- 2- 3- 4-"),
    ("sem comparacoes", ("w x y z".split(), []), "w | x | y | z", "w x y z", "", ""),
    ("N", ("a b c d".split(), [("a", "c"), ("b", "c"), ("b", "d")]), "a c | b d", "c d", "a-c b-d", "a- b-"),
    ("B3", B3, "e 1 12 123 | 2 23 | 3 13", "12 13 23", "e-1 1-12 2-23 3-13 12-123", "e- 1- 2- 3- 123+"),
    ("divisibilidade", DIV, "1 2 4 8 | 3 6 12 | 5 10 | 7 | 9 | 11", "7 8 9 10 11 12",
     "1-2 2-4 3-6 4-8 5-10 6-12", "1- 2- 3- 4- 5- 6-"),
    ("DAG-armadilha", ("0 1 2 3 4".split(), [("0", "2"), ("1", "2"), ("2", "3"), ("2", "4")]),
     "0 2 4 | 1 3", "3 4", "0-2 1-3 2-4", "0- 1- 2-"),
    ("redundantes", ("a b c".split(), [("a", "b"), ("a", "b"), ("b", "c"), ("a", "c")]), "a b c", "c", "a-b b-c", "a- b-"),
]


def verificar_certificados(R, M, K, T):
    """Confere certificados quaisquer (indices): M emparelhamento em B_P, K cobertura com |K| = |M|,
    T anticadeia com |T| = n - |M|."""
    n = len(R)
    assert all(R[i][j] for i, j in M)
    assert len({i for i, _ in M}) == len(M) == len({j for _, j in M})
    sK = set(K)
    for i in range(n):
        for j in range(n):
            if R[i][j]:
                assert ("A", i) in sK or ("B", j) in sK
    assert len(K) == len(M)
    for u in T:
        for v in T:
            assert not R[u][v]
    assert len(T) == n - len(M)
    return True


def largura_forca_bruta(n, R):
    melhor = 0
    for mask in range(1 << n):
        S = [i for i in range(n) if mask >> i & 1]
        if len(S) > melhor and all(not R[u][v] for u in S for v in S):
            melhor = len(S)
    return melhor


def teste_tabela():
    for nome, (el, rel), cad, T, M, K in TABELA:
        c, t, m, k = dilworth(el, rel)
        assert " | ".join(" ".join(x) for x in c) == cad, (nome, c)
        assert " ".join(t) == T, (nome, t)
        assert " ".join(f"{x}-{y}" for x, y in m) == M, (nome, m)
        assert " ".join(f"{x}{s}" for s, x in k) == K, (nome, k)
    print("tabela ok (8 posets)")


def teste_ex1015_texto():
    el, rel = EX1015
    idx = {x: i for i, x in enumerate(el)}
    R = fecho(6, [(idx[x], idx[y]) for x, y in rel])
    assert sum(map(sum, R)) == 10   # a<c,e,f; b<d,e,f; c<e,f; d<e,f
    a, b, c, d, e, f = range(6)
    M = [(a, c), (b, d), (c, e), (d, f)]
    # certificados do texto: K = {a-, b-, e+, f+}, T = {c, d}
    assert verificar_certificados(R, M, [("A", a), ("A", b), ("B", e), ("B", f)], [c, d])
    # os nossos: K = {a-, b-, c-, d-}, T = {e, f}
    _, cad, T, M2, K = dilworth_indices(6, [(idx[x], idx[y]) for x, y in rel])
    assert M2 == M
    assert verificar_certificados(R, M2, K, T)
    print("Ex. 10.15 ok: certificados do texto e os do programa aceitos")


def ordem_aleatoria(rng):
    n = rng.randint(3, 11)
    nomes = [f"v{i}" for i in range(n)]
    rng.shuffle(nomes)
    rel = [(nomes[i], nomes[j]) for i in range(n) for j in range(i + 1, n) if rng.random() < 0.3]
    return nomes, rel


def teste_aleatorios():
    rng = random.Random(6)
    for _ in range(80):
        el, rel = ordem_aleatoria(rng)
        n = len(el)
        idx = {x: i for i, x in enumerate(el)}
        pares = [(idx[x], idx[y]) for x, y in rel]
        R, cad, T, M, K = dilworth_indices(n, pares)
        w = largura_forca_bruta(n, R)
        assert len(cad) == len(T) == w
        D = nx.DiGraph()
        D.add_nodes_from(range(n))
        D.add_edges_from(pares)
        C = nx.transitive_closure(D, reflexive=False)
        assert {(i, j) for i in range(n) for j in range(n) if R[i][j]} == set(C.edges())
        assert max(len(a) for a in nx.algorithms.dag.antichains(D)) == w
        # T de outra forma: K = (A \ RA) u RB, entao x fora de K <=> x- em RA e x+ fora de RB
        _, _, RA, RB, _ = emparelhamento_maximo(n, n, construir_BP(n, R))
        assert T == [x for x in range(n) if x in RA and x not in RB]
        for c in cad:
            for i in range(len(c)):
                for j in range(i + 1, len(c)):
                    assert R[c[i]][c[j]]
    print("80 ordens aleatorias ok (forca bruta, networkx fecho e antichains)")


def teste_erdos_szekeres():
    rng = random.Random(12)
    for _ in range(100):
        r, s = rng.randint(1, 4), rng.randint(1, 4)
        N = r * s + 1
        a = rng.sample(range(100), N)
        pares = [(i, j) for i in range(N) for j in range(i + 1, N) if a[i] <= a[j]]
        R, cad, T, M, K = dilworth_indices(N, pares)
        maior_cadeia = max(len(c) for c in cad)
        assert maior_cadeia >= r + 1 or len(T) >= s + 1
    print("Erdos-Szekeres ok (100 sequencias)")


def teste_bordas():
    assert dilworth([], []) == ([], [], [], [])
    assert dilworth(["x"], []) == ([["x"]], ["x"], [], [])
    for el, rel in ((["a", "b"], [("a", "b"), ("b", "a")]),     # ciclo
                    (["a"], [("a", "a")]),                      # x < x
                    (["a"], [("a", "z")])):                     # nome desconhecido
        try:
            dilworth(el, rel)
            assert False
        except ValueError:
            pass
    print("bordas ok (n = 0, n = 1, ciclo, x < x, nome desconhecido)")


if __name__ == "__main__":
    teste_tabela()
    teste_ex1015_texto()
    teste_aleatorios()
    teste_erdos_szekeres()
    teste_bordas()
    print("todos os testes passaram")
