import itertools
import random
import networkx as nx
from bipartido import busca, aumenta, emparelhamento_maximo, verificar


def monta(nA, nB, texto):
    adj = [[] for _ in range(nA)]
    for e in texto.split():
        a, b = e.split("-")
        adj[int(a[1:])].append(int(b[1:]))
    return [sorted(l) for l in adj]


# (nome, nA, nB, arestas, nu, M, RA, RB, K, aumentos)
TABELA = [
    ("P6", 3, 3, "a0-b0 a1-b0 a1-b1 a2-b1 a2-b2", 3, "a0-b0 a1-b1 a2-b2", "", "", "a0 a1 a2", 3),
    ("P7", 4, 3, "a0-b0 a1-b0 a1-b1 a2-b1 a2-b2 a3-b2", 3, "a0-b0 a1-b1 a2-b2", "a0 a1 a2 a3", "b0 b1 b2", "b0 b1 b2", 3),
    ("C6", 3, 3, "a0-b0 a1-b1 a2-b2 a0-b2 a1-b0 a2-b1", 3, "a0-b0 a1-b1 a2-b2", "", "", "a0 a1 a2", 3),
    ("C8", 4, 4, "a0-b0 a1-b1 a2-b2 a3-b3 a0-b3 a1-b0 a2-b1 a3-b2", 4, "a0-b0 a1-b1 a2-b2 a3-b3", "", "", "a0 a1 a2 a3", 4),
    ("K3,3", 3, 3, "a0-b0 a0-b1 a0-b2 a1-b0 a1-b1 a1-b2 a2-b0 a2-b1 a2-b2", 3, "a0-b0 a1-b1 a2-b2", "", "", "a0 a1 a2", 3),
    ("K2,3", 2, 3, "a0-b0 a0-b1 a0-b2 a1-b0 a1-b1 a1-b2", 2, "a0-b0 a1-b1", "", "", "a0 a1", 2),
    ("K3,2", 3, 2, "a0-b0 a0-b1 a1-b0 a1-b1 a2-b0 a2-b1", 2, "a0-b0 a1-b1", "a0 a1 a2", "b0 b1", "b0 b1", 2),
    ("isolados", 4, 3, "a0-b0 a2-b1", 2, "a0-b0 a2-b1", "a1 a3", "", "a0 a2", 2),
    ("sem arestas", 3, 2, "", 0, "", "a0 a1 a2", "", "", 0),
    ("caminho longo", 2, 2, "a0-b0 a0-b1 a1-b0", 2, "a0-b1 a1-b0", "", "", "a0 a1", 2),
    ("escada", 4, 4, "a0-b0 a0-b1 a1-b0 a2-b1 a2-b2 a3-b2 a3-b3", 4, "a0-b1 a1-b0 a2-b2 a3-b3", "", "", "a0 a1 a2 a3", 4),
    ("Hall violado", 5, 5, "a0-b0 a0-b1 a1-b0 a1-b1 a2-b0 a2-b1 a3-b2 a4-b2 a4-b3", 4,
     "a0-b0 a1-b1 a3-b2 a4-b3", "a0 a1 a2", "b0 b1", "a3 a4 b0 b1", 4),
]


def roda_contando(nA, nB, adj):
    # mesmo laco de emparelhamento_maximo, mas conferindo cada aumento
    mateA, mateB = [-1] * nA, [-1] * nB
    caminhos = []
    while True:
        cam, RA, RB = busca(nA, nB, adj, mateA, mateB)
        if cam is None:
            break
        antes = sum(1 for x in mateA if x != -1)
        aumenta(cam, mateA, mateB)
        depois = sum(1 for x in mateA if x != -1)
        assert depois == antes + 1
        assert mateA[cam[0]] != -1 and mateB[cam[-1]] != -1
        caminhos.append(cam)
    return caminhos


def teste_tabela():
    for nome, nA, nB, ar, nu, M, RA, RB, K, aum in TABELA:
        adj = monta(nA, nB, ar)
        mateA, mateB, rA, rB, k = emparelhamento_maximo(nA, nB, adj)
        assert verificar(nA, nB, adj, mateA, mateB, k) == nu, nome
        assert " ".join(f"a{a}-b{mateA[a]}" for a in range(nA) if mateA[a] != -1) == M, nome
        assert " ".join(f"a{a}" for a in rA) == RA, nome
        assert " ".join(f"b{b}" for b in rB) == RB, nome
        assert " ".join(f"{l.lower()}{x}" for l, x in k) == K, (nome, k)
        assert len(roda_contando(nA, nB, adj)) == aum, nome
    cams = roda_contando(4, 4, monta(4, 4, TABELA[10][3]))
    assert cams == [[0, 0], [2, 1], [3, 2], [1, 0, 0, 1, 2, 2, 3, 3]], cams
    print("tabela ok (12 testes), caminhos da escada ok")


def nu_forca_bruta(nA, adj):
    E = [(a, b) for a in range(nA) for b in adj[a]]
    for k in range(len(E), 0, -1):
        for sub in itertools.combinations(E, k):
            if len({a for a, _ in sub}) == k and len({b for _, b in sub}) == k:
                return k
    return 0


def nu_formula_72(nA, adj):
    # nu = |A| - max_{S ⊆ A} (|S| - |N(S)|)
    pior = 0
    for r in range(nA + 1):
        for S in itertools.combinations(range(nA), r):
            viz = set()
            for a in S:
                viz.update(adj[a])
            pior = max(pior, len(S) - len(viz))
    return nA - pior


def teste_aleatorios():
    rng = random.Random(3)
    for _ in range(1000):
        nA, nB = rng.randint(0, 6), rng.randint(0, 6)
        adj = [sorted(b for b in range(nB) if rng.random() < 0.35) for _ in range(nA)]
        roda_contando(nA, nB, adj)
        mateA, mateB, RA, RB, K = emparelhamento_maximo(nA, nB, adj)
        nu = verificar(nA, nB, adj, mateA, mateB, K)
        m = sum(len(l) for l in adj)
        if m <= 12:
            assert nu == nu_forca_bruta(nA, adj)
        assert nu == nu_formula_72(nA, adj)
        G = nx.Graph()
        G.add_nodes_from(("A", a) for a in range(nA))
        G.add_nodes_from(("B", b) for b in range(nB))
        G.add_edges_from((("A", a), ("B", b)) for a in range(nA) for b in adj[a])
        hk = nx.bipartite.hopcroft_karp_matching(G, top_nodes=[("A", a) for a in range(nA)])
        assert len(hk) // 2 == nu
    print("1000 aleatorios ok (forca bruta, formula 7.2, networkx)")


def teste_bordas():
    for nA, nB in ((0, 3), (3, 0), (0, 0)):
        adj = [[] for _ in range(nA)]
        mateA, mateB, RA, RB, K = emparelhamento_maximo(nA, nB, adj)
        assert verificar(nA, nB, adj, mateA, mateB, K) == 0 and K == []
        assert RA == list(range(nA))
    print("casos de borda ok (nA = 0, nB = 0)")


if __name__ == "__main__":
    teste_tabela()
    teste_aleatorios()
    teste_bordas()
    print("todos os testes passaram")
