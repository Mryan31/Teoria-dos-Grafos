import sys
import os
import heapq


def ler_grafo(caminho):
    with open(caminho) as arq:
        nums = arq.read().split()
    n, m = int(nums[0]), int(nums[1])
    arestas = [(int(nums[2 + 2 * i]), int(nums[3 + 2 * i])) for i in range(m)]
    return n, arestas


def montar_adj(n, arestas):
    adj = [set() for _ in range(n + 1)]
    for u, v in arestas:
        if not (1 <= u <= n and 1 <= v <= n):
            raise ValueError(f"vertice fora de 1..{n}")
        if u == v or v in adj[u]:
            raise ValueError(f"aresta {u}-{v} invalida: o grafo tem que ser simples")
        adj[u].add(v)
        adj[v].add(u)
    return adj


def nucleo(n, arestas):
    """Prova do Teorema 2.8: enquanto houver v com d(v) <= grau_medio(F)/2, remove v.
    Devolve (H, mH, log) com log = [(v, grau em F, mF, nF), ...] na ordem de remocao."""
    adj = montar_adj(n, arestas)
    m = len(arestas)
    if m == 0:
        raise ValueError("o Teorema 2.8 exige ao menos uma aresta")
    d = [len(adj[v]) for v in range(n + 1)]
    vivo = [True] * (n + 1)
    nF, mF = n, m
    heap = [(d[v], v) for v in range(1, n + 1)]
    heapq.heapify(heap)
    log = []
    while heap:
        dv, v = heap[0]
        if not vivo[v] or dv != d[v]:  # entrada velha
            heapq.heappop(heap)
            continue
        # d <= grau_medio/2  <=>  d <= mF/nF  <=>  d*nF <= mF   (so inteiros)
        if dv * nF > mF:
            break
        heapq.heappop(heap)
        log.append((v, dv, mF, nF))
        vivo[v] = False
        mF -= dv
        nF -= 1
        for u in adj[v]:
            if vivo[u]:
                d[u] -= 1
                heapq.heappush(heap, (d[u], u))
    H = [v for v in range(1, n + 1) if vivo[v]]
    return H, mF, log


def main():
    if len(sys.argv) < 2:
        print("uso: python nucleo_denso.py entradas/arquivo.txt")
        return
    caminho = sys.argv[1]
    n, arestas = ler_grafo(caminho)
    m = len(arestas)
    linhas = [f"n={n} m={m} grau_medio(G)={2 * m / n:.3f}"]
    try:
        H, mH, log = nucleo(n, arestas)
    except ValueError as e:
        linhas.append(f"erro: {e}")
    else:
        adj = montar_adj(n, arestas)
        conjH = set(H)
        deltaH = min(len(adj[v] & conjH) for v in H)
        # Teorema 2.8: delta(H) > grau_medio(H)/2 >= grau_medio(G)/2
        assert len(H) > 0
        assert deltaH * len(H) > mH
        assert mH * n >= m * len(H)
        if log:
            rem = " ".join(f"{v}:{g}" for v, g, _, _ in log)
        else:
            rem = "nenhum"
        linhas.append(f"removidos (vertice:grau): {rem}")
        linhas.append("H = " + " ".join(map(str, H)) + f"     |E(H)|={mH}")
        linhas.append(f"grau_medio(H)={2 * mH / len(H):.3f}  delta(H)={deltaH}")
    texto = "\n".join(linhas)
    print(texto)

    pasta = os.path.join(os.path.dirname(os.path.abspath(__file__)), "saidas")
    os.makedirs(pasta, exist_ok=True)
    nome = os.path.splitext(os.path.basename(caminho))[0] + ".out"
    with open(os.path.join(pasta, nome), "w") as arq:
        arq.write(texto + "\n")


if __name__ == "__main__":
    main()
