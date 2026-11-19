"""Simetrizacao (Zykov) com certificado: devolve uma clique de ordem r + 1 em G ou a
particao que mostra G ~ T_r(n).
Uso: python simetrizacao.py [-v] < g.txt"""
import sys


def turan(n, r):
    # tamanhos das partes de T_r(n) (as primeiras n % r tem uma a mais) e t_r(n)
    q, s = divmod(n, r)
    tam = [q + 1] * s + [q] * (r - s)
    return tam, n * (n - 1) // 2 - sum(t * (t - 1) // 2 for t in tam)


def matriz(n, E):
    A = [[False] * n for _ in range(n)]
    for u, v in E:
        A[u][v] = A[v][u] = True
    return A


def classes(n, A):
    """Tenta separar V nas classes da relacao 'nao adjacente'. Devolve (partes, None) se a
    relacao for de equivalencia (G multipartido completo), senao (None, (a, v, b)) com
    a ~/~ v, v ~/~ b e a ~ b. Custo O(n^2)."""
    dono = [-1] * n
    partes = []
    for v in range(n):
        if dono[v] != -1:
            continue
        C = [v] + [u for u in range(v + 1, n) if dono[u] == -1 and not A[v][u]]
        for u in C:
            dono[u] = len(partes)
        partes.append(C)
    for i, C in enumerate(partes):
        # dentro da classe ninguem pode ser adjacente
        for x in range(1, len(C)):
            for y in range(x + 1, len(C)):
                if A[C[x]][C[y]]:
                    return None, (C[x], C[0], C[y])
        # entre classes tudo tem que ser adjacente; se u (de uma classe anterior j) nao ve
        # w desta classe, entao w ~ rep_j (senao teria entrado na classe j) e u != rep_j
        for j in range(i):
            for u in partes[j]:
                for w in C:
                    if not A[u][w]:
                        return None, (partes[j][0], u, w)
    return partes, None


def copia(A, grau, x, y):
    # x passa a ter a vizinhanca de y (x e y nao adjacentes, entao y nao entra em N(x)); O(n)
    for w in range(len(A)):
        if w == x:
            continue
        novo = A[y][w]
        if A[x][w] != novo:
            A[x][w] = A[w][x] = novo
            d = 1 if novo else -1
            grau[w] += d
            grau[x] += d


def simetriza(n, E):
    """Aplica as operacoes da prova ate G ficar multipartido completo.
    log[i] = (caso, copias, m): copias = [(x, y), ...] com 'x virou copia de y' (na ordem em
    que foram feitas) e m = arestas depois da operacao."""
    A = matriz(n, E)
    grau = [sum(l) for l in A]
    m = len(E)
    log = []
    while True:
        partes, tri = classes(n, A)
        if partes is not None:
            return partes, log, A
        a, v, b = tri
        if grau[v] < grau[a]:
            caso, copias = 1, [(v, a)]
        elif grau[v] < grau[b]:
            caso, copias = 1, [(v, b)]
        else:
            # d(v) >= d(a), d(b): a e b viram copias de v. A primeira copia pode nao mudar
            # nada (d(a) = d(v)), mas a segunda ganha a aresta ab perdida: o par sobe >= 1
            caso, copias = 2, [(a, v), (b, v)]
        antes = m
        for x, y in copias:
            m += grau[y] - grau[x]
            copia(A, grau, x, y)
        assert m == sum(grau) // 2
        assert m > antes, "numero de arestas nao subiu"
        log.append((caso, copias, m))


def desfaz(Q, log):
    # volta pelas copias, da ultima pra primeira: se a copia x esta na clique, troca por y
    Q = list(Q)
    for _, copias, _ in reversed(log):
        for x, y in reversed(copias):
            if x in Q:
                assert y not in Q
                Q[Q.index(x)] = y
    return sorted(Q)


def eh_clique(A, Q):
    return all(A[Q[i]][Q[j]] for i in range(len(Q)) for j in range(i + 1, len(Q)))


def certifica_turan(n, r, E, partes):
    # confere que G e exatamente o multipartido completo das partes, com tamanhos de T_r(n)
    tam, _ = turan(n, r)
    if sorted((len(P) for P in partes), reverse=True) != [t for t in tam if t > 0]:
        return False
    dono = {}
    for i, P in enumerate(partes):
        for v in P:
            dono[v] = i
    arestas = {(min(u, v), max(u, v)) for u, v in E}
    todas = {(u, v) for u in range(n) for v in range(u + 1, n) if dono[u] != dono[v]}
    return arestas == todas


def resolve(n, r, E):
    """Devolve ('clique', Q, log) ou ('turan', partes, log)."""
    partes, log, _ = simetriza(n, E)
    G = matriz(n, E)
    if len(partes) >= r + 1:
        Q = [P[0] for P in partes[:r + 1]]
        Q0 = desfaz(Q, log)
        assert len(Q0) == r + 1 and eh_clique(G, Q0)
        return "clique", Q0, log
    # no maximo r partes: nenhuma operacao pode ter ocorrido (ver README)
    assert not log
    assert certifica_turan(n, r, E, partes)
    return "turan", partes, log


def ler(texto):
    nums = [int(x) for x in texto.split()]
    n, m, r = nums[0], nums[1], nums[2]
    E = [(nums[3 + 2 * i], nums[4 + 2 * i]) for i in range(m)]
    return n, r, E


def main():
    n, r, E = ler(sys.stdin.read())
    if r < 1:
        print("ERRO r < 1")
        return 1
    vistas = set()
    for u, v in E:
        if u == v or (min(u, v), max(u, v)) in vistas:
            print("ERRO nao-simples")
            return 1
        vistas.add((min(u, v), max(u, v)))
    _, t = turan(n, r)
    if len(E) < t:
        print(f"ERRO poucas-arestas {len(E)} < {t}")
        return 1
    tipo, cert, log = resolve(n, r, E)
    print(f"arestas {len(E)} tr {t}")
    print(f"operacoes {len(log)}")
    if "-v" in sys.argv:
        for caso, copias, m in log:
            print(f"caso {caso} " + " ".join(f"{x}<-{y}" for x, y in copias) + f" m {m}")
    if tipo == "clique":
        print("clique " + " ".join(map(str, cert)))
    else:
        print("turan " + " | ".join(" ".join(map(str, P)) for P in cert))
    return 0


if __name__ == "__main__":
    sys.exit(main())
