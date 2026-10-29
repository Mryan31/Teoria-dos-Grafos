"""Geradores de grafos: cada um devolve (n, E) com E na ordem de insercao."""


def kmn(m, n):
    return m + n, [(i, m + j) for i in range(m) for j in range(n)]


def ciclo(n):
    return n, [(i, (i + 1) % n) for i in range(n)]


def caminho(n):
    return n, [(i, i + 1) for i in range(n - 1)]


def completo(n):
    return n, [(i, j) for i in range(n) for j in range(i + 1, n)]


def petersen():
    E = [(i, (i + 1) % 5) for i in range(5)] + [(5 + i, 5 + (i + 2) % 5) for i in range(5)] + \
        [(i, 5 + i) for i in range(5)]
    return 10, E


def roda(r):
    # r raios, centro = r
    return r + 1, [(i, (i + 1) % r) for i in range(r)] + [(i, r) for i in range(r)]


def cubo(d):
    return 1 << d, [(v, v ^ (1 << b)) for v in range(1 << d) for b in range(d) if v < v ^ (1 << b)]


def grade(a, b):
    E = []
    for i in range(a):
        for j in range(b):
            if j + 1 < b:
                E.append((i * b + j, i * b + j + 1))
            if i + 1 < a:
                E.append((i * b + j, (i + 1) * b + j))
    return a * b, E
