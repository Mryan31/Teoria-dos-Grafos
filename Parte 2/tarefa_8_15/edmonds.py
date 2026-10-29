import sys
import os
import glob
from collections import deque

NAO_ALCANCADO, INT, EXT = 0, 1, 2


def lca(x, y, base, mate, parent, n):
    # base comum: marca as bases subindo de x ate a raiz, depois sobe de y ate achar uma marcada
    marca = [False] * n
    u = x
    while True:
        u = base[u]
        marca[u] = True
        if mate[u] == -1:
            break  # chegou na raiz
        u = parent[mate[u]]
    u = y
    while True:
        u = base[u]
        if marca[u]:
            return u
        u = parent[mate[u]]


def contraia(x, y, b, base, mate, parent, tipo, fila, n):
    inb = [False] * n
    for u, w in ((x, y), (y, x)):  # sobe pelos dois lados do ciclo ate a base b
        while base[u] != b:
            inb[base[u]] = True
            inb[base[mate[u]]] = True
            parent[u] = w  # u passa a apontar "pelo outro lado do ciclo"
            u, w = parent[mate[u]], mate[u]
    for v in range(n):
        if inb[base[v]]:
            base[v] = b
            if tipo[v] != EXT:  # internos viram externos e entram na fila
                tipo[v] = EXT
                fila.append(v)


def busca(r, adj, mate, eventos=None):
    """BUSCA(r). Devolve (z, parent, base, tipo); z = -1 se falhou."""
    n = len(adj)
    parent = [-1] * n
    base = list(range(n))
    tipo = [NAO_ALCANCADO] * n
    tipo[r] = EXT
    fila = deque([r])
    while fila:
        x = fila.popleft()  # x e externo
        for y in adj[x]:
            if base[x] == base[y] or mate[x] == y:  # (a)
                if eventos is not None:
                    eventos.append((x, y, "a"))
                continue
            if tipo[y] == NAO_ALCANCADO:  # (b)
                if eventos is not None:
                    eventos.append((x, y, "b"))
                parent[y] = x
                if mate[y] == -1:
                    return y, parent, base, tipo  # caminho aumentante
                tipo[y] = INT
                tipo[mate[y]] = EXT
                fila.append(mate[y])
            elif tipo[y] == INT:  # (c)
                if eventos is not None:
                    eventos.append((x, y, "c"))
                continue
            else:  # (d) y externo: blossom
                b = lca(x, y, base, mate, parent, n)
                if eventos is not None:
                    eventos.append((x, y, "d", b))
                contraia(x, y, b, base, mate, parent, tipo, fila, n)
    return -1, parent, base, tipo


def aumente(z, parent, mate):
    while z != -1:
        x = parent[z]
        w = mate[x]
        mate[x] = z
        mate[z] = x
        z = w
    return mate


def tamanho(mate):
    return sum(1 for v in range(len(mate)) if mate[v] > v)


def verificar(adj, mate):
    for v in range(len(mate)):
        if mate[v] != -1:
            assert mate[mate[v]] == v
            assert mate[v] in adj[v]


def edmonds(n, adj, mate0=None):
    mate = list(mate0) if mate0 is not None else [-1] * n
    while True:
        aumentou = False
        for r in range(n):
            if mate[r] == -1:
                z, parent, base, tipo = busca(r, adj, mate)
                if z != -1:
                    antes = tamanho(mate)
                    aumente(z, parent, mate)
                    verificar(adj, mate)
                    assert tamanho(mate) == antes + 1
                    aumentou = True
                    break  # reinicia a varredura das raizes
        if not aumentou:
            return mate


def ler_grafo(caminho):
    with open(caminho) as arq:
        linhas = [l.split() for l in arq if l.strip()]
    n, m = int(linhas[0][0]), int(linhas[0][1])
    adj = [[] for _ in range(n)]
    for i in range(m):
        u, v = int(linhas[1 + i][0]), int(linhas[1 + i][1])
        if u == v or not (0 <= u < n and 0 <= v < n) or v in adj[u]:
            raise ValueError(f"aresta invalida {u}-{v}: o grafo tem que ser simples")
        adj[u].append(v)
        adj[v].append(u)
    for v in range(n):
        adj[v].sort()
    mate0 = None
    for l in linhas[1 + m:]:
        if l[0] == "M":
            if mate0 is None:
                mate0 = [-1] * n
            u, v = int(l[1]), int(l[2])
            mate0[u], mate0[v] = v, u
    return n, adj, mate0


def roda_arquivo(caminho):
    n, adj, mate0 = ler_grafo(caminho)
    if mate0 is not None:
        verificar(adj, mate0)
    mate = edmonds(n, adj, mate0)
    texto = f"nu {tamanho(mate)}\nmate " + " ".join(map(str, mate))
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
