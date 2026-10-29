import sys
import os
import glob
from collections import deque


class Rede:
    """Rede residual com entradas pareadas: o arco original k gera as entradas
    2k (direta, capacidade residual c - f) e 2k+1 (reversa, capacidade residual f)."""

    def __init__(self, n):
        self.n = n
        self.para = []
        self.cap = []
        self.adj = [[] for _ in range(n)]

    def add_arc(self, u, v, c):
        k = len(self.para) // 2
        self.para += [v, u]
        self.cap += [c, 0]
        self.adj[u].append(2 * k)
        self.adj[v].append(2 * k + 1)
        return k


def edmonds_karp(n, arcos, s, t, f0=None, checar=False, trilhas=None):
    """Devolve (valor, f, S, log). f[k] = fluxo no arco original k,
    S = alcancaveis a partir de s na rede residual final,
    log = [(comprimento do caminho, gargalo), ...]."""
    if s == t:
        raise ValueError("s e t precisam ser diferentes")
    if not (0 <= s < n and 0 <= t < n):
        raise ValueError("s ou t fora de [0, n)")
    R = Rede(n)
    for u, v, c in arcos:
        if not (0 <= u < n and 0 <= v < n):
            raise ValueError(f"vertice fora de [0, n) no arco {u}->{v}")
        if u == v:
            raise ValueError(f"laco {u}->{v} nao e permitido")
        if c < 0:
            raise ValueError(f"capacidade negativa no arco {u}->{v}")
        R.add_arc(u, v, c)
    valor = 0
    if f0 is not None:
        for k, (u, v, c) in enumerate(arcos):
            if not (0 <= f0[k] <= c):
                raise ValueError("f0 nao respeita 0 <= f0 <= c")
            R.cap[2 * k] = c - f0[k]
            R.cap[2 * k + 1] = f0[k]
            if u == s:
                valor += f0[k]
            if v == s:
                valor -= f0[k]
    log = []
    while True:
        # BFS so por entradas com capacidade residual positiva
        pred = [-1] * n
        visto = [False] * n
        visto[s] = True
        fila = deque([s])
        while fila and not visto[t]:
            u = fila.popleft()
            for i in R.adj[u]:
                v = R.para[i]
                if R.cap[i] > 0 and not visto[v]:
                    visto[v] = True
                    pred[v] = i
                    fila.append(v)
        if not visto[t]:
            break  # esta ultima BFS foi completa: S = visto
        # gargalo
        caminho = []
        v = t
        while v != s:
            i = pred[v]
            caminho.append(i)
            v = R.para[i ^ 1]
        caminho.reverse()
        eps = min(R.cap[i] for i in caminho)
        for i in caminho:
            R.cap[i] -= eps
            R.cap[i ^ 1] += eps
        valor += eps
        log.append((len(caminho), eps))
        if trilhas is not None:
            trilhas.append(caminho)
        if checar:
            for k, (_, _, c) in enumerate(arcos):
                assert R.cap[2 * k] + R.cap[2 * k + 1] == c
    f = [R.cap[2 * k + 1] for k in range(len(arcos))]
    S = {v for v in range(n) if visto[v]}
    return valor, f, S, log


def verificar(n, arcos, s, t, valor, f, S):
    for k, (u, v, c) in enumerate(arcos):
        assert 0 <= f[k] <= c
    saldo = [0] * n
    for k, (u, v, c) in enumerate(arcos):
        saldo[u] += f[k]
        saldo[v] -= f[k]
    for v in range(n):
        if v == s:
            assert saldo[v] == valor
        elif v == t:
            assert saldo[v] == -valor
        else:
            assert saldo[v] == 0
    assert s in S and t not in S
    assert valor == sum(c for u, v, c in arcos if u in S and v not in S)


def ler_entrada(caminho):
    with open(caminho) as arq:
        linhas = [l.split() for l in arq if l.strip()]
    n, m, s, t = map(int, linhas[0])
    arcos = [tuple(map(int, linhas[1 + i])) for i in range(m)]
    f0 = None
    for l in linhas[1 + m:]:
        if l[0] == "f0":
            f0 = [int(x) for x in l[1:]]
    return n, arcos, s, t, f0


def roda_arquivo(caminho):
    n, arcos, s, t, f0 = ler_entrada(caminho)
    valor, f, S, log = edmonds_karp(n, arcos, s, t, f0)
    verificar(n, arcos, s, t, valor, f, S)
    corte = sum(c for u, v, c in arcos if u in S and v not in S)
    texto = (f"valor {valor}\nfluxo " + " ".join(map(str, f)) +
             "\nS " + " ".join(map(str, sorted(S))) + f"\ncorte {corte}")
    pasta = os.path.join(os.path.dirname(os.path.abspath(__file__)), "saidas")
    os.makedirs(pasta, exist_ok=True)
    nome = os.path.splitext(os.path.basename(caminho))[0] + ".out"
    with open(os.path.join(pasta, nome), "w") as arq:
        arq.write(texto + "\n")
    return texto


def main():
    if len(sys.argv) > 1:
        arquivos = sys.argv[1:]
    else:
        aqui = os.path.dirname(os.path.abspath(__file__))
        arquivos = sorted(glob.glob(os.path.join(aqui, "entradas", "*.txt")))
    for caminho in arquivos:
        if len(arquivos) > 1:
            print("==", os.path.basename(caminho))
        print(roda_arquivo(caminho))


if __name__ == "__main__":
    main()
