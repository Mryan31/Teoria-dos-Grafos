import itertools
import os
import random
import subprocess
import sys
import networkx as nx
from simetrizacao import turan, matriz, classes, simetriza, desfaz, eh_clique, resolve, certifica_turan, ler

AQUI = os.path.dirname(os.path.abspath(__file__))

# (arquivo, saida esperada; para clique a lista, para turan as partes, e o nº de operacoes)
TABELA = [
    ("c4_r2", "turan", [[0, 2], [1, 3]], 0),
    ("k33_r2", "turan", [[0, 2, 4], [1, 3, 5]], 0),
    ("t3_7_r3", "turan", [[0, 3, 5], [1, 6], [2, 4]], 0),
    ("k3_r5", "turan", [[0], [1], [2]], 0),
    ("vazio_r1", "turan", [[0, 1, 2, 3]], 0),
    ("k4_r3", "clique", [0, 1, 2, 3], 0),
    ("t3_7_mais_r3", "clique", [0, 1, 2, 6], 0),
    ("aresta_r1", "clique", [0, 1], 1),
    ("c5_cordas_r2", "clique", [0, 1, 2], 1),
    ("caso2_r2", "clique", [0, 2, 4], 1),
    ("k33_movida_r2", "clique", [0, 2, 3], 1),
    ("misto_r2", "clique", [0, 2, 5], 2),
    ("triangulo_pendente_r2", "clique", [1, 2, 3], 1),   # aqui o desfazer troca 0 por 1
]

REJEITADAS = [
    ("ruim_c5_r2", "ERRO poucas-arestas 5 < 6"),
    ("ruim_laco", "ERRO nao-simples"),
    ("ruim_paralela", "ERRO nao-simples"),
]


def le(nome):
    with open(os.path.join(AQUI, "entradas", nome + ".txt")) as f:
        return ler(f.read())


def roda(nome):
    with open(os.path.join(AQUI, "entradas", nome + ".txt")) as f:
        p = subprocess.run([sys.executable, os.path.join(AQUI, "simetrizacao.py")], stdin=f,
                           capture_output=True, text=True)
    return p.returncode, p.stdout.strip()


def teste_turan():
    # t_r(n) contra a formula fechada (1 - 1/r) n^2 / 2 quando r divide n, e alguns valores conhecidos
    assert turan(6, 2)[1] == 9 and turan(7, 3)[1] == 16 and turan(5, 2)[1] == 6
    assert turan(10, 4)[1] == 37 and turan(3, 5)[1] == 3 and turan(4, 1)[1] == 0
    for r in range(1, 6):
        for q in range(0, 5):
            assert turan(q * r, r)[1] * 2 * r == (r - 1) * (q * r) ** 2
    print("t_r(n) ok")


def teste_tabela():
    for nome, tipo, cert, nops in TABELA:
        n, r, E = le(nome)
        t, c, log = resolve(n, r, E)
        assert (t, c, len(log)) == (tipo, cert, nops), (nome, t, c, log)
        cod, saida = roda(nome)
        assert cod == 0
        ult = saida.splitlines()[-1]
        if tipo == "clique":
            assert ult == "clique " + " ".join(map(str, cert)), saida
        else:
            assert ult == ("turan " + " | ".join(" ".join(map(str, P)) for P in cert)).strip(), saida
    for nome, esp in REJEITADAS:
        cod, saida = roda(nome)
        assert cod == 1 and saida == esp, (nome, saida)
    print(f"tabela ok ({len(TABELA)} casos + {len(REJEITADAS)} rejeicoes)")


def multipartido(n, A, partes):
    dono = [0] * n
    for i, P in enumerate(partes):
        for v in P:
            dono[v] = i
    return all(A[u][v] == (dono[u] != dono[v]) for u in range(n) for v in range(n) if u != v)


def grafo_turan(n, r, rng):
    tam, _ = turan(n, r)
    vs = list(range(n))
    rng.shuffle(vs)
    dono = {}
    i = 0
    for p, t in enumerate(tam):
        for v in vs[i:i + t]:
            dono[v] = p
        i += t
    return [(u, v) for u in range(n) for v in range(u + 1, n) if dono[u] != dono[v]]


def propriedades(n, r, E, cont):
    m0 = len(E)
    partes, log, A = simetriza(n, E)
    assert multipartido(n, A, partes)                       # terminou em multipartido completo
    ms = [m0] + [l[2] for l in log]
    assert all(ms[i] < ms[i + 1] for i in range(len(log)))  # sobe estritamente
    assert len(log) <= n * (n - 1) // 2 - m0                # limitado por C(n,2)
    for caso, _, _ in log:
        cont[caso] += 1
    G = nx.Graph()
    G.add_nodes_from(range(n))
    G.add_edges_from(E)
    omega = max((len(c) for c in nx.find_cliques(G)), default=0)
    tipo, cert, _ = resolve(n, r, E)
    if tipo == "clique":
        assert len(cert) == r + 1 and eh_clique(matriz(n, E), cert)
        Q = [P[0] for P in partes[:r + 1]]
        if desfaz(Q, log) != sorted(Q):
            cont["troca"] += 1
        assert omega >= r + 1
    else:
        assert omega <= r and not log
        # networkx so aceita r <= n; com r > n, T_r(n) e o K_n
        assert nx.is_isomorphic(G, nx.turan_graph(n, min(r, n)) if n else nx.empty_graph(0))
        assert certifica_turan(n, r, E, partes)


def teste_aleatorios():
    rng = random.Random(21)
    cont = {1: 0, 2: 0, "troca": 0}
    total = turans = movidas = 0
    for _ in range(4000):
        n = rng.randint(1, 10)
        r = rng.randint(1, 5)
        _, t = turan(n, r)
        todas = list(itertools.combinations(range(n), 2))
        m = rng.randint(t, len(todas))
        E = rng.sample(todas, m)
        propriedades(n, r, E, cont)
        total += 1
    # grafos de Turan com rotulos embaralhados, e Turan com uma aresta a mais ou movida
    for _ in range(1000):
        n = rng.randint(2, 12)
        r = rng.randint(2, 5)
        T = grafo_turan(n, r, rng)
        assert resolve(n, r, T)[0] == "turan"
        turans += 1
        propriedades(n, r, T, cont)
        total += 1
        fora = [(u, v) for u in range(n) for v in range(u + 1, n) if (u, v) not in set(T)]
        if fora:
            extra = rng.choice(fora)
            assert resolve(n, r, T + [extra])[0] == "clique"
            # tira uma aresta e poe outra: continua com t_r(n) arestas; se nao for mais T_r(n)
            # tem que aparecer K_{r+1} (propriedades confere com networkx). Ex.: em T_2(3) = P3
            # trocar ab por bc da P3 de novo, entao nao da pra exigir clique sempre
            sai = rng.randrange(len(T))
            E2 = T[:sai] + T[sai + 1:] + [extra]
            if resolve(n, r, E2)[0] == "clique":
                movidas += 1
            propriedades(n, r, E2, cont)
            total += 1
    print(f"propriedades ok em {total} grafos ({turans} Turan embaralhados); operacoes caso 1: {cont[1]}, "
          f"caso 2: {cont[2]}; desfazer trocou vertice da clique em {cont['troca']} grafos; "
          f"{movidas} Turan com aresta movida deram clique")


def teste_classes():
    # a busca da tripla tem que achar a ~/~ v ~/~ b com a ~ b sempre que nao for multipartido
    rng = random.Random(3)
    for _ in range(3000):
        n = rng.randint(1, 8)
        E = [e for e in itertools.combinations(range(n), 2) if rng.random() < 0.6]
        A = matriz(n, E)
        partes, tri = classes(n, A)
        if partes is None:
            a, v, b = tri
            assert len({a, v, b}) == 3 and not A[a][v] and not A[v][b] and A[a][b]
        else:
            assert multipartido(n, A, partes)
            assert sorted(v for P in partes for v in P) == list(range(n))
    print("busca da tripla ok (3000 grafos)")


if __name__ == "__main__":
    teste_turan()
    teste_tabela()
    teste_classes()
    teste_aleatorios()
    print("todos os testes passaram")
