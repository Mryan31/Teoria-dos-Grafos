import sys
from collections import deque


def residuos(n, pe, cab, val):
    # b(v) = soma dos valores dos arcos que saem de v - soma dos que entram (lacos nao contam)
    b = [0] * n
    for e in range(len(pe)):
        if pe[e] != cab[e]:
            b[pe[e]] += val[e]
            b[cab[e]] -= val[e]
    return b


def circulacao_modular(n, pe, cab, val, k):
    b = residuos(n, pe, cab, val)
    return [v for v in range(n) if b[v] % k != 0]


def corrigir(n, pe, cab, val, k):
    """Ida da prova do Teor. 16.6: enquanto houver b(s) > 0, acha por BFS um caminho dirigido
    s -> t com b(t) < 0, inverte o caminho e troca val por k - val.
    Devolve (f, log, K0) com f na orientacao ORIGINAL."""
    m = len(pe)
    pe, cab, val = list(pe), list(cab), list(val)
    virou = [0] * m
    inc = [[] for _ in range(n)]          # estatico: a orientacao muda, as listas nao
    for e in range(m):
        if pe[e] != cab[e]:
            inc[pe[e]].append(e)
            inc[cab[e]].append(e)
    b = residuos(n, pe, cab, val)
    K = sum(abs(x) for x in b)
    K0 = K
    log = []
    while True:
        s = next((v for v in range(n) if b[v] > 0), None)
        if s is None:
            break
        visto = [False] * n
        pai = [-1] * n
        visto[s] = True
        fila = deque([s])
        t = None
        ops = 0
        while fila and t is None:
            u = fila.popleft()
            for e in inc[u]:
                ops += 1
                if pe[e] == u:            # so arcos que SAEM de u na orientacao atual
                    w = cab[e]
                    if not visto[w]:
                        visto[w] = True
                        pai[w] = e
                        if b[w] < 0:
                            t = w
                            break
                        fila.append(w)
        # o conjunto R dos alcancaveis nao tem arco saindo, entao soma de b em R <= 0; como b(s) > 0, t existe
        assert t is not None, "BFS nao achou t: bug"
        P = []
        v = t
        while v != s:
            e = pai[v]
            P.append(e)
            v = pe[e]
        P.reverse()
        for e in P:
            pe[e], cab[e] = cab[e], pe[e]
            val[e] = k - val[e]
            virou[e] ^= 1
            assert 0 < val[e] < k
        b[s] -= k
        b[t] += k
        K -= 2 * k
        assert K == sum(abs(x) for x in b)
        log.append(dict(s=s, t=t, P=P, K=K, ops=ops))
    f = [-val[e] if virou[e] else val[e] for e in range(m)]
    return f, log, K0


def confere(n, pe0, cab0, f, k):
    # (16.1) na orientacao original: Df = 0 e 0 < |f(e)| < k
    return all(0 < abs(x) < k for x in f) and all(x == 0 for x in residuos(n, pe0, cab0, f))


def ler(texto):
    nums = [int(x) for x in texto.split()]
    n, m, k = nums[0], nums[1], nums[2]
    pe, cab, val = [], [], []
    for i in range(m):
        pe.append(nums[3 + 3 * i])
        cab.append(nums[4 + 3 * i])
        val.append(nums[5 + 3 * i])
    return n, k, pe, cab, val


def main():
    n, k, pe, cab, val = ler(sys.stdin.read())
    if k < 2:
        print("ERRO k < 2")
        return 1
    val = [x % k for x in val]
    if any(x == 0 for x in val):
        print("ERRO valor-zero")
        return 1
    ruins = circulacao_modular(n, pe, cab, val, k)
    if ruins:
        print("ERRO conservacao " + " ".join(map(str, ruins)))
        return 1
    f, log, K0 = corrigir(n, pe, cab, val, k)
    assert confere(n, pe, cab, f, k)
    print(f"K0 {K0}")
    print(f"correcoes {len(log)}")
    print("f " + " ".join(map(str, f)) if f else "f")
    return 0


if __name__ == "__main__":
    sys.exit(main())
