import sys
import os
import heapq


def arvore_valida(n, arestas):
    if n < 2:
        raise ValueError("Prufer so faz sentido para n >= 2")
    if len(arestas) != n - 1:
        raise ValueError(f"uma arvore com {n} vertices tem {n - 1} arestas, vieram {len(arestas)}")
    # union-find simples para achar ciclo (com n-1 arestas, sem ciclo => conexa)
    pai = list(range(n + 1))

    def acha(x):
        while pai[x] != x:
            pai[x] = pai[pai[x]]
            x = pai[x]
        return x

    for u, v in arestas:
        if not (1 <= u <= n and 1 <= v <= n) or u == v:
            raise ValueError(f"aresta invalida {u}-{v}")
        a, b = acha(u), acha(v)
        if a == b:
            raise ValueError("as arestas formam ciclo: nao e arvore")
        pai[a] = b


def codificar(n, arestas):
    """Definicao 3.11. Devolve (codigo, folhas removidas)."""
    arvore_valida(n, arestas)
    adj = [set() for _ in range(n + 1)]
    for u, v in arestas:
        adj[u].add(v)
        adj[v].add(u)
    folhas = [v for v in range(1, n + 1) if len(adj[v]) == 1]
    heapq.heapify(folhas)
    P, X = [], []
    for _ in range(n - 2):
        x = heapq.heappop(folhas)
        a = next(iter(adj[x]))       # unico vizinho
        P.append(a)
        X.append(x)
        adj[a].remove(x)
        adj[x].clear()
        if len(adj[a]) == 1:
            heapq.heappush(folhas, a)
    return P, X


def decodificar(P):
    """Teorema 3.13. Devolve a lista de arestas."""
    n = len(P) + 2
    mult = [0] * (n + 1)
    for a in P:
        if not (1 <= a <= n):
            raise ValueError(f"valor {a} fora de 1..{n}")
        mult[a] += 1
    folhas = [v for v in range(1, n + 1) if mult[v] == 0]
    heapq.heapify(folhas)
    E = []
    for a in P:
        x = heapq.heappop(folhas)
        E.append((x, a))
        mult[a] -= 1
        if mult[a] == 0:
            heapq.heappush(folhas, a)
    E.append((heapq.heappop(folhas), heapq.heappop(folhas)))   # sobram exatamente dois
    assert not folhas
    return E


def normaliza(E):
    return sorted((min(u, v), max(u, v)) for u, v in E)


def main():
    if len(sys.argv) < 3 or sys.argv[1] not in ("cod", "dec"):
        print("uso: python prufer.py cod arquivo   |   python prufer.py dec arquivo")
        return
    modo, caminho = sys.argv[1], sys.argv[2]
    with open(caminho) as arq:
        nums = [int(x) for x in arq.read().split()]
    if modo == "cod":
        n = nums[0]
        E = [(nums[1 + 2 * i], nums[2 + 2 * i]) for i in range(n - 1)]
        P, X = codificar(n, E)
        texto = " ".join(map(str, P)) + "\n" + "folhas: " + " ".join(map(str, X))
    else:
        E = decodificar(nums)
        texto = "\n".join(f"{u} {v}" for u, v in normaliza(E))
    print(texto)

    pasta = os.path.join(os.path.dirname(os.path.abspath(__file__)), "saidas")
    os.makedirs(pasta, exist_ok=True)
    nome = os.path.splitext(os.path.basename(caminho))[0] + "_" + modo + ".out"
    with open(os.path.join(pasta, nome), "w") as arq:
        arq.write(texto + "\n")


if __name__ == "__main__":
    main()
