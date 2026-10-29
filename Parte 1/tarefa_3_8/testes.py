import itertools
import random
import networkx as nx
from imersao_arvore import imersao, ordem_de_crescimento, verifica_ordem, verifica_imersao


def K(n):
    return [(a, b) for a in range(1, n + 1) for b in range(a + 1, n + 1)]


K33 = [(a, b) for a in (1, 2, 3) for b in (4, 5, 6)]
PET = [(1, 2), (2, 3), (3, 4), (4, 5), (5, 1), (1, 6), (2, 7), (3, 8), (4, 9), (5, 10),
       (6, 8), (8, 10), (10, 7), (7, 9), (9, 6)]
C6 = [(1, 2), (2, 3), (3, 4), (4, 5), (5, 6), (6, 1)]
P4 = [(1, 2), (2, 3), (3, 4)]
EST = [(1, 2), (1, 3), (1, 4)]
BIN = [(1, 2), (1, 3), (2, 4), (2, 5), (3, 6), (3, 7)]

# (t, T, r, n, G, x, ordem, phi(1..t) ou None, livres)
TABELA = [
    (4, P4, 1, 5, K(5), 3, [1, 2, 3, 4], [3, 1, 2, 4], [4, 3, 2]),
    (4, P4, 2, 5, K(5), 5, [2, 3, 4, 1], [3, 5, 1, 2], [4, 3, 2]),
    (4, EST, 1, 4, K(4), 2, [1, 4, 3, 2], [2, 4, 3, 1], [3, 2, 1]),
    (4, EST, 2, 4, K(4), 4, [2, 1, 4, 3], [1, 4, 3, 2], [3, 2, 1]),
    (4, P4, 1, 6, K33, 1, [1, 2, 3, 4], [1, 4, 2, 5], [3, 2, 2]),
    (4, EST, 3, 6, K33, 5, [3, 1, 4, 2], [1, 6, 5, 4], [3, 2, 1]),
    (4, P4, 1, 10, PET, 1, [1, 2, 3, 4], [1, 2, 3, 4], [3, 2, 2]),
    (5, [(1, 2), (1, 3), (3, 4), (3, 5)], 4, 5, K(5), 2, [4, 3, 5, 1, 2], [4, 5, 1, 2, 3], [4, 3, 2, 1]),
    (3, [(1, 2), (2, 3)], 2, 6, C6, 4, [2, 3, 1], [5, 4, 3], [2, 1]),
    (7, BIN, 1, 7, K(7), 4, [1, 3, 7, 6, 2, 5, 4], [4, 5, 1, 7, 6, 3, 2], [6, 5, 4, 3, 2, 1]),
    (1, [], 1, 4, K(4), 3, [1], [3], []),
    (2, [(1, 2)], 2, 4, K(4), 3, [2, 1], [1, 3], [3]),
    (4, EST, 1, 5, [(1, 2), (2, 3), (3, 4), (4, 5)], 1, [1, 4, 3, 2], None, [1, 0]),
]


def grafo_com_grau_minimo(n, k, rng=random):
    # comeca em K_n e apaga arestas so se as duas pontas continuam com grau >= k
    E = K(n)
    rng.shuffle(E)
    grau = [n - 1] * (n + 1)
    fica = []
    for a, b in E:
        if grau[a] > k and grau[b] > k and rng.random() < 0.5:
            grau[a] -= 1
            grau[b] -= 1
        else:
            fica.append((a, b))
    return fica


def arvores_rotuladas(t):
    pares = list(itertools.combinations(range(1, t + 1), 2))
    for sub in itertools.combinations(pares, t - 1):
        G = nx.Graph()
        G.add_nodes_from(range(1, t + 1))
        G.add_edges_from(sub)
        if nx.is_connected(G):
            yield list(sub)


def confere_networkx(t, TE, phi, GE):
    G = nx.Graph(GE)
    imagens = [(phi[a], phi[b]) for a, b in TE]
    T = nx.Graph()
    T.add_nodes_from(range(1, t + 1))
    T.add_edges_from(TE)
    if t > 1:
        img = G.edge_subgraph(imagens)
        assert nx.is_tree(img)
        assert nx.is_isomorphic(T, img)


def teste_tabela():
    for t, TE, r, n, GE, x, ordem, phi_esp, livres_esp in TABELA:
        phi, o, pai, livres = imersao(t, TE, r, n, GE, x)
        assert o == ordem, (TE, r, o)
        assert livres == livres_esp, (TE, r, livres)
        verifica_ordem(t, TE, o, pai, r)
        if phi_esp is None:
            assert phi is None
        else:
            assert [phi[u] for u in range(1, t + 1)] == phi_esp, (TE, r, phi)
            verifica_imersao(t, TE, r, n, GE, x, phi)
            confere_networkx(t, TE, phi, GE)
    # no caso violado existe outra copia de T em G? (o algoritmo falhar nao prova que nao existe)
    G = nx.Graph([(1, 2), (2, 3), (3, 4), (4, 5)])
    T = nx.Graph(EST)
    existe = nx.isomorphism.GraphMatcher(G, T).subgraph_is_monomorphic()
    print("tabela ok (13 linhas); caso violado: existe alguma copia da estrela no caminho?", existe)


def teste_exaustivo():
    rng = random.Random(7)
    contagens = []
    combinacoes = 0
    for t in range(1, 7):
        arvores = list(arvores_rotuladas(t)) if t > 1 else [[]]
        contagens.append(len(arvores))
        for TE in arvores:
            for r in range(1, t + 1):
                ordem, pai = ordem_de_crescimento(t, TE, r)
                verifica_ordem(t, TE, ordem, pai, r)
                # cada prefixo da ordem induz subarvore conexa
                for i in range(1, t + 1):
                    pref = set(ordem[:i])
                    H = nx.Graph()
                    H.add_nodes_from(pref)
                    H.add_edges_from(e for e in TE if e[0] in pref and e[1] in pref)
                    assert nx.is_connected(H)
                for n in (t, t + 1, t + 2):
                    GE = grafo_com_grau_minimo(n, t - 1, rng)
                    x = rng.randint(1, n)
                    phi, o, p, livres = imersao(t, TE, r, n, GE, x)
                    assert phi is not None
                    verifica_imersao(t, TE, r, n, GE, x, phi)
                    for i, l in enumerate(livres, start=2):
                        assert l >= t - i + 1          # folga da prova
                    combinacoes += 1
    assert contagens == [1, 1, 3, 16, 125, 1296], contagens
    print(f"exaustivo t<=6 ok: arvores {contagens}, {combinacoes} combinacoes")


def teste_networkx_aleatorio():
    rng = random.Random(11)
    for _ in range(300):
        t = rng.randint(2, 9)
        TE = [(rng.randint(1, i - 1), i) for i in range(2, t + 1)]
        n = rng.randint(t, t + 4)
        GE = grafo_com_grau_minimo(n, t - 1, rng)
        r, x = rng.randint(1, t), rng.randint(1, n)
        phi, o, p, livres = imersao(t, TE, r, n, GE, x)
        verifica_imersao(t, TE, r, n, GE, x, phi)
        confere_networkx(t, TE, phi, GE)
    print("300 aleatorios conferidos com networkx")


if __name__ == "__main__":
    teste_tabela()
    teste_exaustivo()
    teste_networkx_aleatorio()
    print("todos os testes passaram")
