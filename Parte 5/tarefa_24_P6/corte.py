"""Corte com pelo menos m/2 arestas sem aleatoriedade (esperancas condicionais).
Uso: python corte.py [-v] < g.txt"""
import sys


def listas(n, E):
    adj = [[] for _ in range(n)]
    for u, v in E:
        adj[u].append(v)
        adj[v].append(u)
    return adj


def corte_guloso(n, adj, ordem=None):
    """Fixa os vertices na ordem dada (padrao 0..n-1), cada um no lado oposto a maioria dos
    vizinhos ja posicionados (empate -> lado 0).
    Devolve (lado, E2, ops): E2[i] = 2 x esperanca condicional depois de fixar i vertices
    (inteiro pra nao usar fracao), ops = itens examinados nas listas."""
    if ordem is None:
        ordem = range(n)
    m = sum(len(l) for l in adj) // 2
    lado = [-1] * n
    garantidas = 0      # arestas com as duas pontas fixas e em lados diferentes
    abertas = m         # arestas com pelo menos uma ponta ainda livre
    E2 = [m]            # no inicio a esperanca e m/2
    ops = 0
    for v in ordem:
        c = [0, 0]
        for w in adj[v]:
            ops += 1
            if lado[w] != -1:
                c[lado[w]] += 1
        lado[v] = 1 if c[0] > c[1] else 0
        # as c[0] + c[1] arestas de v pra vizinhos fixos fecham agora; as do outro lado entram
        garantidas += c[1 - lado[v]]
        abertas -= c[0] + c[1]
        E2.append(2 * garantidas + abertas)
        assert E2[-1] >= E2[-2], "esperanca caiu"
    assert abertas == 0 and E2[-1] == 2 * garantidas
    return lado, E2, ops


def tamanho_corte(E, lado):
    # conta direto pela lista de arestas, sem usar nada do algoritmo
    return sum(1 for u, v in E if lado[u] != lado[v])


def ler(texto):
    nums = [int(x) for x in texto.split()]
    n, m = nums[0], nums[1]
    return n, [(nums[2 + 2 * i], nums[3 + 2 * i]) for i in range(m)]


def main():
    n, E = ler(sys.stdin.read())
    if any(u == v for u, v in E):
        print("ERRO laco")
        return 1
    lado, E2, _ = corte_guloso(n, listas(n, E))
    c = tamanho_corte(E, lado)
    assert 2 * c >= len(E) and 2 * c == E2[-1]
    print(f"corte {c}")
    print(f"m {len(E)}")
    print("lados " + " ".join(map(str, lado)) if lado else "lados")
    if "-v" in sys.argv:
        print("esperanca " + " ".join(f"{x / 2:g}" for x in E2))
    return 0


if __name__ == "__main__":
    sys.exit(main())
