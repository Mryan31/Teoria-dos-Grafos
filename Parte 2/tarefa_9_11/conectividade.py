import sys
import os
from collections import deque


# ---------------------------------------------------------------------------
# copiado da tarefa 6.19 (mesma interface; entradas pareadas 2k / 2k+1)
# ---------------------------------------------------------------------------
def edmonds_karp(n, arcos, s, t, f0=None):
    if s == t:
        raise ValueError("s e t precisam ser diferentes")
    para, cap = [], []
    adj = [[] for _ in range(n)]
    for k, (u, v, c) in enumerate(arcos):
        para += [v, u]
        cap += [c, 0]
        adj[u].append(2 * k)
        adj[v].append(2 * k + 1)
    valor = 0
    if f0 is not None:
        for k, (u, v, c) in enumerate(arcos):
            cap[2 * k], cap[2 * k + 1] = c - f0[k], f0[k]
            valor += f0[k] * ((u == s) - (v == s))
    log = []
    while True:
        pred = [-1] * n
        visto = [False] * n
        visto[s] = True
        fila = deque([s])
        while fila and not visto[t]:
            u = fila.popleft()
            for i in adj[u]:
                v = para[i]
                if cap[i] > 0 and not visto[v]:
                    visto[v] = True
                    pred[v] = i
                    fila.append(v)
        if not visto[t]:
            break
        caminho = []
        v = t
        while v != s:
            caminho.append(pred[v])
            v = para[pred[v] ^ 1]
        eps = min(cap[i] for i in caminho)
        for i in caminho:
            cap[i] -= eps
            cap[i ^ 1] += eps
        valor += eps
        log.append((len(caminho), eps))
    f = [cap[2 * k + 1] for k in range(len(arcos))]
    S = {v for v in range(n) if visto[v]}
    return valor, f, S, log
# ---------------------------------------------------------------------------


def valida(n, arestas):
    if n < 2:
        raise ValueError("precisa de n >= 2")
    vistas = set()
    for u, v in arestas:
        if u == v or not (0 <= u < n and 0 <= v < n):
            raise ValueError(f"aresta invalida {u}-{v}")
        e = frozenset((u, v))
        if e in vistas:
            raise ValueError(f"aresta repetida {u}-{v}")
        vistas.add(e)


def decompor(arcos_com_fluxo, s, t, val):
    """arcos_com_fluxo: lista de (u, v) com fluxo 1. Devolve val caminhos de s a t."""
    saida = {}
    for u, v in arcos_com_fluxo:
        saida.setdefault(u, []).append([v, 1])
    caminhos = []
    for _ in range(val):
        caminho = [s]
        usados = []          # entrada de saida[] usada em cada passo do caminho
        pos = {s: 0}
        while caminho[-1] != t:
            u = caminho[-1]
            ent = next(e for e in saida[u] if e[1] > 0)
            v = ent[0]
            if v in pos:
                # ciclo: apaga os arcos de v ... u -> v e volta o caminho ate v
                k = pos[v]
                for e in usados[k:]:
                    e[1] -= 1
                ent[1] -= 1
                caminho = caminho[:k + 1]
                usados = usados[:k]
                pos = {w: i for i, w in enumerate(caminho)}
            else:
                caminho.append(v)
                usados.append(ent)
                pos[v] = len(caminho) - 1
        for e in usados:
            e[1] -= 1
        caminhos.append(caminho)
    return caminhos


def conectividade_aresta(n, arestas, x, y):
    arcos = []
    for u, v in arestas:
        arcos += [(u, v, 1), (v, u, 1)]   # arcos 2k e 2k+1, independentes
    val, f, S, _ = edmonds_karp(n, arcos, x, y)
    for k in range(len(arestas)):
        if f[2 * k] == 1 and f[2 * k + 1] == 1:   # sentidos opostos se cancelam
            f[2 * k] = f[2 * k + 1] = 0
    corte = [(u, v) for u, v in arestas if (u in S) != (v in S)]
    usados = [(arcos[j][0], arcos[j][1]) for j in range(len(arcos)) if f[j] == 1]
    caminhos = decompor(usados, x, y, val)
    return val, caminhos, corte


def conectividade_vertice(n, arestas, x, y):
    if x == y:
        raise ValueError("x e y precisam ser diferentes")
    if frozenset((x, y)) in {frozenset(e) for e in arestas}:
        raise ValueError("x e y adjacentes: nao existe separador (Cor. 9.8)")
    N = n + 1
    # v- = 2v, v+ = 2v+1; os n primeiros arcos sao os centrais
    arcos = [(2 * v, 2 * v + 1, N if v in (x, y) else 1) for v in range(n)]
    for u, v in arestas:
        arcos += [(2 * u + 1, 2 * v, N), (2 * v + 1, 2 * u, N)]
    val, f, S, _ = edmonds_karp(2 * n, arcos, 2 * x, 2 * y + 1)
    sep = [v for v in range(n) if 2 * v in S and 2 * v + 1 not in S]
    usados = []
    for j in range(n, len(arcos)):
        if f[j] >= 1:
            usados.append((arcos[j][0] // 2, arcos[j][1] // 2))   # u+ -> v-  vira  u -> v
    caminhos = decompor(usados, x, y, val)
    return val, caminhos, sep


def lambda_G(n, arestas):
    return min(conectividade_aresta(n, arestas, x, y)[0] for x in range(n) for y in range(x + 1, n))


def kappa_G(n, arestas):
    E = {frozenset(e) for e in arestas}
    if len(E) == n * (n - 1) // 2:
        return n - 1   # completo
    return min(conectividade_vertice(n, arestas, x, y)[0]
               for x in range(n) for y in range(x + 1, n) if frozenset((x, y)) not in E)


def delta_G(n, arestas):
    g = [0] * n
    for u, v in arestas:
        g[u] += 1
        g[v] += 1
    return min(g)


def ler_grafo(caminho):
    with open(caminho) as arq:
        nums = [int(x) for x in arq.read().split()]
    n, m = nums[0], nums[1]
    arestas = [(nums[2 + 2 * i], nums[3 + 2 * i]) for i in range(m)]
    valida(n, arestas)
    return n, arestas


def fmt_caminhos(cams):
    return " | ".join("-".join(map(str, c)) for c in cams) if cams else "(nenhum)"


def main():
    if len(sys.argv) < 2:
        print("uso: python conectividade.py entradas/arquivo.txt [x y]")
        return
    caminho = sys.argv[1]
    n, arestas = ler_grafo(caminho)
    E = {frozenset(e) for e in arestas}
    if len(sys.argv) >= 4:
        x, y = int(sys.argv[2]), int(sys.argv[3])
    else:
        # primeiro par nao adjacente (ou 0 1 se for completo)
        pares = [(a, b) for a in range(n) for b in range(a + 1, n) if frozenset((a, b)) not in E]
        x, y = pares[0] if pares else (0, 1)
    k, l, d = kappa_G(n, arestas), lambda_G(n, arestas), delta_G(n, arestas)
    assert k <= l <= d
    linhas = [f"kappa {k}", f"lambda {l}", f"delta {d}"]
    val, cams, corte = conectividade_aresta(n, arestas, x, y)
    linhas += [f"aresta {x} {y}: valor {val}",
               f"  caminhos: {fmt_caminhos(cams)}",
               "  corte: " + " ".join(f"{u}-{v}" for u, v in corte)]
    if frozenset((x, y)) in E:
        linhas.append(f"vertice {x} {y}: adjacentes (sem separador)")
    else:
        val, cams, sep = conectividade_vertice(n, arestas, x, y)
        linhas += [f"vertice {x} {y}: valor {val}",
                   f"  caminhos: {fmt_caminhos(cams)}",
                   "  separador: " + " ".join(map(str, sep))]
    texto = "\n".join(linhas)
    print(texto)

    pasta = os.path.join(os.path.dirname(os.path.abspath(__file__)), "saidas")
    os.makedirs(pasta, exist_ok=True)
    nome = os.path.splitext(os.path.basename(caminho))[0] + ".out"
    with open(os.path.join(pasta, nome), "w") as arq:
        arq.write(texto + "\n")


if __name__ == "__main__":
    main()
