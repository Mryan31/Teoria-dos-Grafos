import sys
import os
import heapq
import itertools


def ler_grafo(caminho):
    with open(caminho) as arq:
        nums = arq.read().split()
    n, m = int(nums[0]), int(nums[1])
    arestas = []
    for i in range(m):
        u, v, w = int(nums[2 + 3 * i]), int(nums[3 + 3 * i]), int(nums[4 + 3 * i])
        arestas.append((u, v, w))
    return n, arestas


def prim(n, arestas, r=1, registrar=True):
    """Prim com heapq. Devolve (F, log): F = ids escolhidos em ordem,
    log[k] = (S ordenado, ids do corte, id escolhido) registrado ANTES de S crescer."""
    if not (1 <= r <= n):
        raise ValueError("raiz fora de 1..n")
    adj = [[] for _ in range(n + 1)]
    for i, (u, v, w) in enumerate(arestas, start=1):
        if not (1 <= u <= n and 1 <= v <= n):
            raise ValueError(f"vertice fora de 1..n na aresta {i}")
        if u == v:
            continue  # laco nunca cruza o corte
        adj[u].append((w, i, v))
        adj[v].append((w, i, u))
    S = [False] * (n + 1)
    S[r] = True
    tam = 1
    fila = list(adj[r])
    heapq.heapify(fila)
    F = []
    log = []
    while tam < n:
        if not fila:
            raise ValueError("grafo desconexo")
        w, i, v = heapq.heappop(fila)
        if S[v]:
            continue  # aresta ja nao esta no corte
        if registrar:
            # corte calculado por varredura, independente da fila
            corte = [j for j, (a, b, _) in enumerate(arestas, start=1) if S[a] != S[b]]
            menor = min(arestas[j - 1][2] for j in corte)
            assert i in corte and w == menor
            log.append(([x for x in range(1, n + 1) if S[x]], corte, i))
        F.append(i)
        S[v] = True
        tam += 1
        for item in adj[v]:
            if not S[item[2]]:
                heapq.heappush(fila, item)
    return F, log


def msts(n, arestas):
    """Forca bruta (m pequeno): devolve (peso minimo, lista de MSTs como frozensets, nº de arvores geradoras)."""
    m = len(arestas)
    melhor = None
    lista = []
    total = 0
    for T in itertools.combinations(range(1, m + 1), n - 1):
        pai = list(range(n + 1))

        def acha(x):
            while pai[x] != x:
                x = pai[x]
            return x
        aciclica = True
        for i in T:
            u, v, _ = arestas[i - 1]
            a, b = acha(u), acha(v)
            if a == b:
                aciclica = False
                break
            pai[a] = b
        if not aciclica:
            continue
        total += 1
        p = sum(arestas[i - 1][2] for i in T)
        if melhor is None or p < melhor:
            melhor = p
            lista = [frozenset(T)]
        elif p == melhor:
            lista.append(frozenset(T))
    return melhor, lista, total


def verifica_prop_5_20(F, lista):
    return all(any(set(F[:k]) <= T for T in lista) for k in range(1, len(F) + 1))


def fmt(arestas, j):
    u, v, w = arestas[j - 1]
    return f"e{j}({u}-{v},{w})"


def main():
    if len(sys.argv) < 2:
        print("uso: python prim.py entradas/arquivo.txt [raiz]")
        return
    caminho = sys.argv[1]
    r = int(sys.argv[2]) if len(sys.argv) > 2 else 1
    n, arestas = ler_grafo(caminho)
    linhas = []
    try:
        F, log = prim(n, arestas, r)
    except ValueError as e:
        linhas.append(f"erro: {e}")
    else:
        for k, (S, corte, esc) in enumerate(log, 1):
            linhas.append(f"passo {k}: S={{{','.join(map(str, S))}}} corte=[" +
                          " ".join(fmt(arestas, j) for j in corte) + f"] escolhida={fmt(arestas, esc)}")
        peso = sum(arestas[i - 1][2] for i in F)
        linhas.append("arvore: " + " ".join(f"e{i}" for i in F) + f"   peso={peso}")
        if len(arestas) <= 12:
            melhor, lista, total = msts(n, arestas)
            ok = (n == 1 or peso == melhor) and verifica_prop_5_20(F, lista)
            linhas.append(f"arvores geradoras: {total}   MSTs: {len(lista)} (peso {melhor if melhor is not None else 0})"
                          f"   verificacao: {'OK' if ok else 'FALHOU'}")
    texto = "\n".join(linhas)
    print(texto)

    pasta = os.path.join(os.path.dirname(os.path.abspath(__file__)), "saidas")
    os.makedirs(pasta, exist_ok=True)
    nome = os.path.splitext(os.path.basename(caminho))[0] + f"_r{r}.out"
    with open(os.path.join(pasta, nome), "w") as arq:
        arq.write(texto + "\n")


if __name__ == "__main__":
    main()
