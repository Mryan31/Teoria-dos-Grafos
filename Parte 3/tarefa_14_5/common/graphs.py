"""Grafos como dict[int, set[int]] e as fixtures usadas nos testes.
Nada aqui usa networkx (o dodecaedro foi copiado de nx.dodecahedral_graph())."""
import random


def from_edges(edges, n=None):
    adj = {}
    if n is not None:
        for v in range(n):
            adj[v] = set()
    for u, v in edges:
        if u == v:
            raise ValueError(f"laco em {u}")
        adj.setdefault(u, set()).add(v)
        adj.setdefault(v, set()).add(u)
    return adj


def edges_of(adj):
    return sorted((u, v) for u in adj for v in adj[u] if u < v)


def copy(adj):
    return {v: set(adj[v]) for v in adj}


def ler(caminho):
    """Formato de exemplos/*.txt: '#' comenta, linhas vazias ignoradas; 'n m' e m linhas 'u v'."""
    nums = []
    with open(caminho) as arq:
        for linha in arq:
            linha = linha.split("#")[0].strip()
            if linha:
                nums += [int(x) for x in linha.split()]
    n, m = nums[0], nums[1]
    E = [(nums[2 + 2 * i], nums[3 + 2 * i]) for i in range(m)]
    vistas = set()
    for u, v in E:
        if u == v or not (0 <= u < n and 0 <= v < n) or frozenset((u, v)) in vistas:
            raise ValueError(f"aresta invalida {u} {v}: o grafo tem que ser simples")
        vistas.add(frozenset((u, v)))
    return from_edges(E, n)


# ----------------------------------------------------------------- fixtures
def wheel(k):
    E = [(0, i) for i in range(1, k + 1)] + [(i, i % k + 1) for i in range(1, k + 1)]
    return from_edges(E)


def prism():
    return from_edges([(0, 1), (1, 2), (0, 2), (3, 4), (4, 5), (3, 5), (0, 3), (1, 4), (2, 5)])


def cube():
    return from_edges([(u, u ^ (1 << b)) for u in range(8) for b in range(3) if u < u ^ (1 << b)])


def octahedron():
    return from_edges([(i, j) for i in range(6) for j in range(i + 1, 6) if abs(i - j) != 3])


def petersen():
    E = [(i, (i + 1) % 5) for i in range(5)] + [(i, i + 5) for i in range(5)] + \
        [(5 + i, 5 + (i + 2) % 5) for i in range(5)]
    return from_edges(E)


def k5():
    return from_edges([(i, j) for i in range(5) for j in range(i + 1, 5)])


def k33():
    return from_edges([(a, b) for a in (0, 1, 2) for b in (3, 4, 5)])


def k5_minus_e():
    return from_edges([(i, j) for i in range(5) for j in range(i + 1, 5) if (i, j) != (0, 1)])


DODECAEDRO = [(0, 1), (0, 10), (0, 19), (1, 2), (1, 8), (2, 3), (2, 6), (3, 4), (3, 19), (4, 5),
              (4, 17), (5, 6), (5, 15), (6, 7), (7, 8), (7, 14), (8, 9), (9, 10), (9, 13), (10, 11),
              (11, 12), (11, 18), (12, 13), (12, 16), (13, 14), (14, 15), (15, 16), (16, 17), (17, 18),
              (18, 19)]


def dodecahedron():
    return from_edges(DODECAEDRO)


def j137():
    # Exemplo 13.7: x, y, a, b, c, d = 0..5
    E = [(0, 1), (0, 2), (0, 3), (1, 4), (1, 5)]
    E += [(i, j) for i in range(2, 6) for j in range(i + 1, 6)]
    return from_edges(E)


def k4_sub():
    # K4 em {0,1,2,3} com a aresta 01 trocada por 0-4-1
    return from_edges([(0, 2), (0, 3), (1, 2), (1, 3), (2, 3), (0, 4), (4, 1)])


# ----------------------------------------------------- gerador aleatorio
def _conexo_sem(adj, S):
    resto = [v for v in adj if v not in S]
    if not resto:
        return True
    visto = {resto[0]}
    pilha = [resto[0]]
    while pilha:
        u = pilha.pop()
        for w in adj[u]:
            if w not in S and w not in visto:
                visto.add(w)
                pilha.append(w)
    return len(visto) == len(resto)


def _tres_conexo(adj):
    V = list(adj)
    if len(V) < 4 or not _conexo_sem(adj, set()):
        return False
    for i, u in enumerate(V):
        if not _conexo_sem(adj, {u}):
            return False
        for w in V[i + 1:]:
            if not _conexo_sem(adj, {u, w}):
                return False
    return True


def random_planar_3conn(n, seed=None, apagar=0.5):
    """Comeca no K4, insere cada vertice novo dentro de uma face triangular (fica triangulacao),
    depois tenta apagar arestas sem perder a 3-conexidade. Sempre planar e 3-conexo."""
    rng = random.Random(seed)
    adj = from_edges([(0, 1), (0, 2), (0, 3), (1, 2), (1, 3), (2, 3)])
    faces = [(0, 1, 2), (0, 2, 3), (0, 3, 1), (1, 3, 2)]
    for v in range(4, n):
        a, b, c = faces.pop(rng.randrange(len(faces)))
        adj[v] = set()
        for w in (a, b, c):
            adj[v].add(w)
            adj[w].add(v)
        faces += [(a, b, v), (b, c, v), (c, a, v)]
    E = edges_of(adj)
    rng.shuffle(E)
    for u, v in E:
        if rng.random() < apagar and len(adj[u]) > 3 and len(adj[v]) > 3:
            adj[u].discard(v)
            adj[v].discard(u)
            if not _tres_conexo(adj):
                adj[u].add(v)
                adj[v].add(u)
    return adj
