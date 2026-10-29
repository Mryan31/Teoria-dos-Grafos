"""chi'(G) exato por backtracking (so para n pequeno)."""


def colorivel(n, E, k):
    m = len(E)
    if m == 0:
        return True
    # arestas em ordem de "mais vizinhas primeiro" ajuda a podar
    ordem = sorted(range(m), key=lambda e: -sum(1 for f in range(m) if set(E[e]) & set(E[f])))
    usado = [set() for _ in range(n)]
    cor = [0] * m

    def rec(i, maior):
        if i == m:
            return True
        e = ordem[i]
        u, v = E[e]
        for c in range(1, min(k, maior + 1) + 1):   # quebra de simetria: no maximo uma cor nova
            if c not in usado[u] and c not in usado[v]:
                usado[u].add(c)
                usado[v].add(c)
                cor[e] = c
                if rec(i + 1, max(maior, c)):
                    return True
                usado[u].discard(c)
                usado[v].discard(c)
        return False
    return rec(0, 0)


def chi(n, E):
    g = [0] * n
    for u, v in E:
        g[u] += 1
        g[v] += 1
    D = max(g, default=0)
    if D == 0:
        return 0
    return D if colorivel(n, E, D) else D + 1   # Vizing: chi' e Delta ou Delta + 1
