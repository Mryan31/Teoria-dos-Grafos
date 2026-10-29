"""Coloracao de arestas inserindo uma aresta por vez: Konig (bipartido, Delta cores) e
Vizing (simples, Delta + 1 cores).
Uso: python coloracao.py konig|vizing trocas.log < g.txt"""
import sys
from collections import deque


class Estado:
    """cor[e] em 0..C (0 = sem cor); T[v][c] = id da aresta de cor c em v, ou -1."""

    def __init__(self, n, E, C):
        self.n, self.E, self.C = n, E, C
        self.cor = [0] * len(E)
        self.T = [[-1] * (C + 1) for _ in range(n)]
        self.log = []

    def outro(self, e, v):
        u, w = self.E[e]
        return w if u == v else u

    def atribui(self, e, c):
        u, v = self.E[e]
        assert self.cor[e] == 0 and self.T[u][c] == -1 and self.T[v][c] == -1
        self.cor[e] = c
        self.T[u][c] = e
        self.T[v][c] = e

    def remove(self, e):
        u, v = self.E[e]
        c = self.cor[e]
        self.T[u][c] = -1
        self.T[v][c] = -1
        self.cor[e] = 0

    def falta(self, v):
        # menor cor ausente em v: O(C)
        for c in range(1, self.C + 1):
            if self.T[v][c] == -1:
                return c
        return None

    def caminho(self, x, a, b):
        """Componente (a, b) de x, com a ausente em x: comeca pela cor b e alterna.
        Cada vertice tem no maximo uma aresta de cada cor, entao e um caminho (Lema 20.5)."""
        P = []
        V = [x]
        v, c = x, b
        while self.T[v][c] != -1:
            e = self.T[v][c]
            P.append(e)
            v = self.outro(e, v)
            V.append(v)
            c = a if c == b else b
        return P, V

    def troca(self, P, a, b):
        old = [self.cor[e] for e in P]
        for e in P:                  # apaga tudo antes: reescrever no lugar colide em T[v][a] / T[v][b]
            self.remove(e)
        for e, c in zip(P, old):
            self.atribui(e, a if c == b else b)
        self.log.append(("TROCA", a, b) + tuple(P))

    def desloca(self, es):
        """es = [e0..et] arestas de x, e0 sem cor: c_novo(e_{i-1}) = c_antigo(e_i); e_t fica sem cor."""
        if len(es) <= 1:
            return
        old = [self.cor[e] for e in es]   # guarda as cores antigas antes de mexer
        for e in es[1:]:
            self.remove(e)
        for i in range(1, len(es)):
            self.atribui(es[i - 1], old[i])
        self.log.append(("DESLOCA",) + tuple(es))

    def pinta(self, e, c):
        self.atribui(e, c)
        self.log.append(("COR", e, c))


def konig_insere(S, e, stats):
    # Teor. 20.6 / Lema 20.5
    x, y = S.E[e]
    S.log.append(("INS", e, x, y))
    for c in range(1, S.C + 1):
        if S.T[x][c] == -1 and S.T[y][c] == -1:
            S.pinta(e, c)
            return
    a = S.falta(x)
    b = S.falta(y)
    P, V = S.caminho(x, a, b)
    assert y not in V, "caminho chegou em y: o grafo nao e bipartido"
    S.troca(P, a, b)
    S.pinta(e, b)
    stats["trocas"] += 1
    stats["maxP"] = max(stats["maxP"], len(P))


def vizing_insere(S, e, stats):
    # Lema 20.8 / Teor. 20.9
    x, y0 = S.E[e]
    S.log.append(("INS", e, x, y0))
    alfa = S.falta(x)               # fixado antes de qualquer deslocamento
    leque = [y0]
    arestas = [e]
    pos = {y0: 0}
    while True:
        yk = leque[-1]
        beta = S.falta(yk)
        eb = S.T[x][beta]
        if eb == -1:                # beta tambem falta em x
            S.desloca(arestas)
            S.pinta(arestas[-1], beta)
            return
        z = S.outro(eb, x)
        if z in pos:                # beta = c_{j+1}, z = y_{j+1}
            j = pos[z] - 1
            k = len(leque) - 1
            assert 0 <= j <= k - 2
            S.desloca(arestas[:j + 1])          # deslocamento 1: x y_j fica sem cor
            P, V = S.caminho(x, alfa, beta)
            S.troca(P, alfa, beta)
            stats["trocas"] += 1
            stats["maxP"] = max(stats["maxP"], len(P))
            if leque[j] not in V:   # caso A
                S.pinta(arestas[j], beta)
                stats["A"] += 1
            else:                   # caso B
                assert leque[k] not in V
                S.desloca(arestas[j:k + 1])     # deslocamento 2, com as cores ATUAIS
                S.pinta(arestas[k], beta)
                stats["B"] += 1
            return
        leque.append(z)
        arestas.append(eb)
        pos[z] = len(leque) - 1


def grau_maximo(n, E):
    g = [0] * n
    for u, v in E:
        g[u] += 1
        g[v] += 1
    return max(g, default=0)


def bipartido(n, E):
    adj = [[] for _ in range(n)]
    for u, v in E:
        adj[u].append(v)
        adj[v].append(u)
    lado = [-1] * n
    for s in range(n):
        if lado[s] != -1:
            continue
        lado[s] = 0
        fila = deque([s])
        while fila:
            u = fila.popleft()
            for w in adj[u]:
                if lado[w] == -1:
                    lado[w] = 1 - lado[u]
                    fila.append(w)
                elif lado[w] == lado[u]:
                    return False
    return True


def colorir(n, E, modo, C=None):
    """Devolve (cor, log, stats). A paleta e fixada uma vez pelo Delta do grafo inteiro."""
    if any(u == v for u, v in E):
        raise ValueError("nao-simples" if modo == "vizing" else "laco")
    if modo == "konig":
        if not bipartido(n, E):
            raise ValueError("nao-bipartido")
        C = grau_maximo(n, E) if C is None else C
        insere = konig_insere
    else:
        if len({frozenset(e) for e in E}) != len(E):
            raise ValueError("nao-simples")
        C = grau_maximo(n, E) + 1 if C is None else C
        insere = vizing_insere
    if not E:
        C = 0
    S = Estado(n, E, C)
    stats = dict(trocas=0, A=0, B=0, maxP=0, C=C)
    for e in range(len(E)):
        insere(S, e, stats)
    return S.cor, S.log, stats


def main():
    if len(sys.argv) < 2 or sys.argv[1] not in ("konig", "vizing"):
        print("uso: python coloracao.py konig|vizing [trocas.log] < g.txt")
        return 0
    modo = sys.argv[1]
    nums = [int(x) for x in sys.stdin.read().split()]
    n, m = nums[0], nums[1]
    E = [(nums[2 + 2 * i], nums[3 + 2 * i]) for i in range(m)]
    try:
        cor, log, stats = colorir(n, E, modo)
    except ValueError as erro:
        msg = str(erro)
        print("ERRO " + ("nao-simples" if msg in ("laco", "nao-simples") else msg))
        return 1
    print(f"paleta {stats['C']}")
    print(f"usadas {len(set(cor))}")
    print(" ".join(map(str, cor)))
    if len(sys.argv) > 2:
        with open(sys.argv[2], "w") as arq:
            for linha in log:
                arq.write(" ".join(map(str, linha)) + "\n")
    return 0


if __name__ == "__main__":
    sys.exit(main())
