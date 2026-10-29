import sys
import os


def ler_grafo(caminho):
    with open(caminho) as arq:
        nums = arq.read().split()
    n, m = int(nums[0]), int(nums[1])
    arestas = []
    for i in range(m):
        u = int(nums[2 + 2 * i])
        v = int(nums[3 + 2 * i])
        arestas.append((u, v))
    return n, arestas


def montar_adj(n, arestas):
    adj = [[] for _ in range(n + 1)]
    ja_vistas = set()
    for u, v in arestas:
        if not (1 <= u <= n and 1 <= v <= n):
            raise ValueError(f"vertice fora de 1..{n}: {u} {v}")
        if u == v:
            raise ValueError(f"laco em {u}: o grafo tem que ser simples")
        e = frozenset((u, v))
        if e in ja_vistas:
            raise ValueError(f"aresta repetida {u}-{v}: o grafo tem que ser simples")
        ja_vistas.add(e)
        adj[u].append(v)
        adj[v].append(u)
    return adj


def renomeia(valores, n):
    # cada valor vira a sua posicao na lista ordenada dos valores distintos
    distintos = sorted(set(valores[1:]))
    posicao = {x: i for i, x in enumerate(distintos)}
    novo = [0] * (n + 1)
    for v in range(1, n + 1):
        novo[v] = posicao[valores[v]]
    return novo, len(distintos)


def rodada(adj, c, n):
    # assinatura = (cor antiga, multiconjunto das cores dos vizinhos)
    sig = [None] * (n + 1)
    for v in range(1, n + 1):
        sig[v] = (c[v], tuple(sorted(c[u] for u in adj[v])))
    return sig


def refinar(n, arestas):
    adj = montar_adj(n, arestas)
    graus = [0] + [len(adj[v]) for v in range(1, n + 1)]
    c, k = renomeia(graus, n)
    hist = [c]
    while True:
        sig = rodada(adj, c, n)
        c2, k2 = renomeia(sig, n)
        if k2 == k:  # nenhuma classe se dividiu
            break
        c, k = c2, k2
        hist.append(c)
    return c, len(hist) - 1, hist


def formata(cores, rodadas, n):
    linhas = [f"rodadas: {rodadas}",
              f"classes: {len(set(cores[1:]))}",
              "cores: " + " ".join(str(cores[v]) for v in range(1, n + 1))]
    return "\n".join(linhas)


def main():
    if len(sys.argv) < 2:
        print("uso: python refinamento.py entradas/arquivo.txt")
        return
    caminho = sys.argv[1]
    n, arestas = ler_grafo(caminho)
    cores, rodadas, hist = refinar(n, arestas)
    texto = formata(cores, rodadas, n)
    print(texto)

    pasta = os.path.join(os.path.dirname(os.path.abspath(__file__)), "saidas")
    os.makedirs(pasta, exist_ok=True)
    nome = os.path.splitext(os.path.basename(caminho))[0] + ".out"
    with open(os.path.join(pasta, nome), "w") as arq:
        arq.write(texto + "\n")


if __name__ == "__main__":
    main()
