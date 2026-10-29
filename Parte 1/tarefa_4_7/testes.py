import random
import networkx as nx
from hierholzer import hierholzer, diagnostico, verificar, montar_incidencia

# (n, arestas, s, vertices, ids) ou (n, arestas, None, motivo, None)
TABELA = [
    (3, [(1, 2), (2, 3), (3, 1)], None, [1, 2, 3, 1], [1, 2, 3]),
    (2, [(1, 2), (1, 2)], None, [1, 2, 1], [1, 2]),
    (1, [(1, 1)], None, [1, 1], [1]),
    (5, [(1, 2), (2, 3), (3, 1), (1, 4), (4, 5), (5, 1)], None, [1, 2, 3, 1, 4, 5, 1], [1, 2, 3, 4, 5, 6]),
    (3, [(1, 2), (2, 3), (3, 1), (1, 1)], None, [1, 2, 3, 1, 1], [1, 2, 3, 4]),
    (3, [(1, 2), (1, 2), (2, 3), (2, 3), (2, 2), (1, 3), (1, 3)], None, [1, 2, 1, 3, 2, 2, 3, 1], [1, 2, 6, 3, 5, 4, 7]),
    (4, [(1, 2), (1, 2), (2, 3), (3, 4), (4, 2), (2, 2)], None, [1, 2, 3, 4, 2, 2, 1], [1, 3, 4, 5, 6, 2]),
    (3, [(1, 2), (2, 3), (3, 1)], 2, [2, 1, 3, 2], [1, 3, 2]),
    (5, [(1, 2), (2, 3), (3, 1)], None, [1, 2, 3, 1], [1, 2, 3]),
]
REJEICOES = [
    (4, [(1, 2), (1, 2), (1, 3), (1, 3), (1, 4), (2, 4), (3, 4)], "graus impares em 1 2 3 4"),
    (6, [(1, 2), (2, 3), (3, 1), (4, 5), (5, 6), (6, 4)], "suporte desconexo"),
    (3, [(1, 2), (2, 3)], "graus impares em 1 3"),
    (3, [], "sem arestas"),
]


def teste_tabela():
    for n, E, s, V_esp, ids_esp in TABELA:
        V, ids = hierholzer(n, E, s)
        verificar(E, V, ids)
        assert V == V_esp and ids == ids_esp, (E, V, ids)
    for n, E, motivo in REJEICOES:
        assert diagnostico(n, E) == motivo, (E, diagnostico(n, E))
        try:
            hierholzer(n, E)
            assert False
        except ValueError:
            pass
    print("tabela ok (13 linhas)")


def teste_laco():
    adj = montar_incidencia(3, [(1, 2), (2, 3), (3, 1), (1, 1)])
    assert len(adj[1]) == 4          # 2 + 2: o laco conta duas vezes
    print("convencao do laco ok (grau de 1 no triangulo + laco = 4)")


def multigrafo_ciclos(n, rng):
    # uniao de passeios fechados aleatorios: todos os graus ficam pares
    E = []
    for _ in range(rng.randint(1, 4)):
        k = rng.randint(1, 5)
        pts = [rng.randint(1, n) for _ in range(k)]
        for i in range(k):
            E.append((pts[i], pts[(i + 1) % k]))
    rng.shuffle(E)
    return E


def suporte_nx(n, E):
    G = nx.MultiGraph()
    for i, (u, v) in enumerate(E, 1):
        G.add_edge(u, v, key=i)
    return G


def teste_aleatorios():
    rng = random.Random(42)
    conexos = 0
    for _ in range(2000):
        n = rng.randint(1, 8)
        E = multigrafo_ciclos(n, rng)
        mot = diagnostico(n, E)
        assert mot is None or mot == "suporte desconexo"
        assert (mot is None) == nx.is_eulerian(suporte_nx(n, E))
        if mot is None:
            conexos += 1
            V, ids = hierholzer(n, E)
            verificar(E, V, ids)
            # perturbacao 1: troca uma ponta de uma aresta (quebra a paridade)
            j = rng.randrange(len(E))
            u, v = E[j]
            outros = [w for w in range(1, n + 2) if w != v]
            w = rng.choice(outros)
            E2 = list(E)
            E2[j] = (u, w)
            if u != v and w != u:
                assert diagnostico(max(n, w), E2) is not None
            # perturbacao 2: triangulo disjunto
            E3 = E + [(n + 1, n + 2), (n + 2, n + 3), (n + 3, n + 1)]
            assert diagnostico(n + 3, E3) == "suporte desconexo"
    print(f"2000 aleatorios ok ({100 * conexos / 2000:.0f}% com suporte conexo), perturbacoes ok")


if __name__ == "__main__":
    teste_tabela()
    teste_laco()
    teste_aleatorios()
    print("todos os testes passaram")
