import random
import itertools
import networkx as nx
from coloracao import colorir, grau_maximo
from verificador import verifica, reproduz
from grafos import kmn, ciclo, caminho, completo, petersen, roda, cubo, grade
from exato import chi


def confere(n, E, modo):
    cor, log, st = colorir(n, E, modo)
    assert verifica(n, E, cor, modo, st["C"]) is None
    assert reproduz(n, E, st["C"], log) == cor
    return cor, log, st


def trecho(log, e):
    # operacoes da insercao da aresta e (ate a proxima INS)
    i = next(j for j, l in enumerate(log) if l[0] == "INS" and l[1] == e)
    fim = next((j for j in range(i + 1, len(log)) if log[j][0] == "INS"), len(log))
    return " / ".join(" ".join(map(str, l)) for l in log[i:fim])


def teste_konig():
    tabela = [  # (nome, (n, E), m, Delta, usadas, trocas, max|P|)
        ("K1,1", kmn(1, 1), 1, 1, 1, 0, 0), ("K1,5", kmn(1, 5), 5, 5, 5, 0, 0),
        ("K2,3", kmn(2, 3), 6, 3, 3, 1, 1), ("K3,3", kmn(3, 3), 9, 3, 3, 1, 1),
        ("K3,5", kmn(3, 5), 15, 5, 5, 1, 1), ("K4,4", kmn(4, 4), 16, 4, 4, 0, 0),
        ("K5,7", kmn(5, 7), 35, 7, 7, 5, 5), ("K6,6", kmn(6, 6), 36, 6, 6, 3, 3),
        ("K10,12", kmn(10, 12), 120, 12, 12, 14, 7),
        ("C6", ciclo(6), 6, 2, 2, 0, 0), ("C8", ciclo(8), 8, 2, 2, 0, 0), ("C20", ciclo(20), 20, 2, 2, 0, 0),
        ("Q3", cubo(3), 12, 3, 3, 0, 0), ("Q4", cubo(4), 32, 4, 4, 0, 0), ("grade 4x4", grade(4, 4), 24, 4, 4, 0, 0),
    ]
    for nome, (n, E), m, D, usadas, trocas, maxP in tabela:
        cor, log, st = confere(n, E, "konig")
        assert (len(E), grau_maximo(n, E), len(set(cor)), st["trocas"], st["maxP"]) == (m, D, usadas, trocas, maxP), \
            (nome, len(set(cor)), st)
    assert colorir(*ciclo(4), "konig")[0] == [1, 2, 1, 2]
    assert colorir(*ciclo(6), "konig")[0] == [1, 2, 1, 2, 1, 2]
    cor, log, _ = colorir(*kmn(2, 3), "konig")
    assert cor == [1, 2, 3, 2, 3, 1] and ("TROCA", 3, 1, 4) in log
    assert colorir(*kmn(3, 3), "konig")[0] == [1, 2, 3, 2, 3, 1, 3, 1, 2]
    cor, log, _ = colorir(6, [(2, 4), (1, 5), (0, 5), (1, 3), (0, 4)], "konig")
    assert cor == [1, 2, 1, 1, 2] and trecho(log, 4) == "INS 4 0 4 / TROCA 1 2 2 1 3 / COR 4 2"
    assert confere(2, [(0, 1)] * 3, "konig")[0] == [1, 2, 3]
    cor, log, _ = confere(5, [(1, 4), (0, 3), (1, 2), (0, 2), (0, 2)], "konig")
    assert cor == [1, 2, 2, 3, 1] and log[-2] == ("TROCA", 2, 1, 1)
    print("tabela Konig ok (15 grafos + vetores completos)")


def sem_vertice_0_petersen():
    n, E = petersen()
    return 9, [(u - 1, v - 1) for u, v in E if 0 not in (u, v)]


def teste_vizing():
    tabela = [  # (nome, (n, E), n, m, Delta, C, usadas, trocas, A, B)
        ("K3", completo(3), 3, 3, 2, 3, 3, 0, 0, 0), ("K4", completo(4), 4, 6, 3, 4, 4, 1, 1, 0),
        ("K5", completo(5), 5, 10, 4, 5, 5, 4, 3, 1), ("K6", completo(6), 6, 15, 5, 6, 6, 6, 6, 0),
        ("K7", completo(7), 7, 21, 6, 7, 7, 10, 10, 0), ("K8", completo(8), 8, 28, 7, 8, 8, 15, 14, 1),
        ("K9", completo(9), 9, 36, 8, 9, 9, 22, 22, 0),
        ("Petersen", petersen(), 10, 15, 3, 4, 4, 1, 0, 1),
        ("Petersen - v0", sem_vertice_0_petersen(), 9, 12, 3, 4, 4, 0, 0, 0),
        ("K5 - 01", (5, [e for e in completo(5)[1] if e != (0, 1)]), 5, 9, 4, 5, 5, 2, 2, 0),
        ("W3", roda(3), 4, 6, 3, 4, 4, 1, 1, 0), ("W5", roda(5), 6, 10, 5, 6, 5, 1, 1, 0),
        ("W7", roda(7), 8, 14, 7, 8, 7, 1, 1, 0),
        ("W4", roda(4), 5, 8, 4, 5, 4, 0, 0, 0), ("W6", roda(6), 7, 12, 6, 7, 6, 0, 0, 0),
        ("W8", roda(8), 9, 16, 8, 9, 8, 0, 0, 0),
        ("K3,3", kmn(3, 3), 6, 9, 3, 4, 3, 1, 1, 0), ("K4,4", kmn(4, 4), 8, 16, 4, 5, 4, 3, 3, 0),
        ("Q3", cubo(3), 8, 12, 3, 4, 4, 1, 1, 0),
    ]
    for k in (4, 6):
        tabela.append((f"C{k}", ciclo(k), k, k, 2, 3, 3, 0, 0, 0))
    for k in (3, 5, 7, 9):
        tabela.append((f"C{k}", ciclo(k), k, k, 2, 3, 3, 0, 0, 0))
    for nome, (n, E), nn, m, D, C, usadas, trocas, A, B in tabela:
        cor, log, st = confere(n, E, "vizing")
        got = (n, len(E), grau_maximo(n, E), st["C"], len(set(cor)), st["trocas"], st["A"], st["B"])
        assert got == (nn, m, D, C, usadas, trocas, A, B), (nome, got)
    vetores = [(ciclo(4), [2, 3, 2, 1]), (ciclo(5), [2, 3, 2, 3, 1]), (completo(4), [4, 2, 1, 1, 2, 3]),
               (completo(5), [5, 2, 1, 3, 4, 3, 2, 5, 1, 4]),
               (petersen(), [2, 4, 3, 4, 3, 2, 2, 3, 3, 1, 1, 3, 1, 1, 2]), (roda(4), [4, 1, 2, 3, 1, 2, 3, 4])]
    for (n, E), esperado in vetores:
        assert colorir(n, E, "vizing")[0] == esperado
    print(f"tabela Vizing ok ({len(tabela)} grafos + vetores completos)")


def teste_tracos():
    tracos = [
        ("T-A", 4, [(1, 0), (3, 0), (0, 2), (1, 3)], 2, "INS 2 0 2 / TROCA 3 1 0 / COR 2 1", [3, 2, 1, 1]),
        ("T-A2", 5, [(1, 0), (3, 2), (3, 0), (1, 3), (3, 4)], 4,
         "INS 4 3 4 / DESLOCA 4 1 / TROCA 4 2 2 / COR 1 2", [1, 2, 4, 3, 1]),
        ("T-B", 4, [(3, 1), (3, 2), (3, 0), (1, 0), (0, 2)], 4,
         "INS 4 0 2 / TROCA 3 1 2 1 / DESLOCA 4 2 3 / COR 3 1", [4, 1, 2, 1, 3]),
        ("T-C", 5, [(3, 0), (0, 1), (0, 4), (3, 4), (4, 1), (4, 2)], 5,
         "INS 5 4 2 / DESLOCA 5 3 / TROCA 4 2 2 0 / DESLOCA 3 2 4 / COR 4 2", [2, 1, 3, 4, 2, 1]),
    ]
    for nome, n, E, e, esperado, cores in tracos:
        cor, log, st = confere(n, E, "vizing")
        assert trecho(log, e) == esperado, (nome, trecho(log, e))
        assert cor == cores, (nome, cor)
    print("tracos dourados T-A, T-A2, T-B, T-C reproduzidos linha a linha")


def teste_rejeicoes():
    for n, E in (ciclo(5), completo(4), petersen()):
        try:
            colorir(n, E, "konig")
            assert False
        except ValueError as e:
            assert str(e) == "nao-bipartido"
    for E in ([(0, 1), (0, 1)], [(0, 0)]):
        try:
            colorir(2, E, "vizing")
            assert False
        except ValueError as e:
            assert str(e) == "nao-simples"
    cor, log, st = colorir(3, [], "vizing")
    assert cor == [] and st["C"] == 0
    print("rejeicoes ok (C5, K4, Petersen no Konig; paralela e laco no Vizing; m = 0)")


def teste_aleatorios():
    rng = random.Random(20)
    A = B = 0
    for _ in range(20000):
        n = rng.randint(2, 12)
        p = rng.random()
        E = [e for e in itertools.combinations(range(n), 2) if rng.random() < p]
        rng.shuffle(E)
        E = [(v, u) if rng.random() < .5 else (u, v) for u, v in E]
        cor, log, st = confere(n, E, "vizing")
        D = grau_maximo(n, E)
        assert D <= len(set(cor)) <= D + 1 or not E
        A += st["A"]
        B += st["B"]
        if E and rng.random() < 0.05:
            L = nx.line_graph(nx.Graph([tuple(sorted(e)) for e in E]))
            idx = {tuple(sorted(e)): i for i, e in enumerate(E)}
            assert all(cor[idx[tuple(sorted(a))]] != cor[idx[tuple(sorted(b))]] for a, b in L.edges())
    assert A > 0 and B > 0
    multi = 0
    for _ in range(20000):
        a, b = rng.randint(1, 5), rng.randint(1, 5)
        E = [(rng.randrange(a), a + rng.randrange(b)) for _ in range(rng.randint(0, 12))]
        E = [(v, u) if rng.random() < .5 else (u, v) for u, v in E]
        cor, log, st = confere(a + b, E, "konig")
        if E:
            assert len(set(cor)) == grau_maximo(a + b, E)
        multi += 1
    print(f"aleatorios ok: 20000 simples (Vizing; cobertura A = {A}, B = {B}) e {multi} multigrafos bipartidos (Konig)")


def teste_exato():
    rng = random.Random(7)
    for _ in range(300):
        n = rng.randint(2, 8)
        E = [e for e in itertools.combinations(range(n), 2) if rng.random() < .5]
        cor, _, _ = colorir(n, E, "vizing")
        x = chi(n, E)
        assert len(set(cor)) in (x, x + 1)
    assert chi(*petersen()) == 4          # classe 2
    assert chi(*completo(3)) == 3 and chi(*completo(5)) == 5
    assert chi(*completo(4)) == 3 and chi(*completo(6)) == 5 and chi(*completo(8)) == 7
    # K7 e K9 (Probl. 20.P3(c)): cada classe de cor tem <= (n-1)/2 arestas, e m > Delta (n-1)/2
    for n in (7, 9):
        m = n * (n - 1) // 2
        assert m > (n - 1) * ((n - 1) // 2)
    print("comparacao com chi' exato ok (Petersen e K_{2r+1} classe 2, K_{2r} classe 1)")


def teste_invariancia():
    rng = random.Random(1)
    for n, E in (petersen(), completo(6), roda(5)):
        for _ in range(200):
            F = list(E)
            rng.shuffle(F)
            cor, _, _ = confere(n, F, "vizing")
            assert len(set(cor)) <= grau_maximo(n, F) + 1
    print("invariancia: 200 ordens embaralhadas sempre dao coloracao propria com <= Delta + 1")


if __name__ == "__main__":
    teste_konig()
    teste_vizing()
    teste_tracos()
    teste_rejeicoes()
    teste_exato()
    teste_invariancia()
    teste_aleatorios()
    print("todos os testes passaram")
