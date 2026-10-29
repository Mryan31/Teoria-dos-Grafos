import sys
import os
import heapq


def ler_entrada(caminho):
    with open(caminho) as arq:
        nums = [int(x) for x in arq.read().split()]
    pos = 0
    t, r = nums[0], nums[1]
    pos = 2
    arestasT = []
    for _ in range(t - 1):
        arestasT.append((nums[pos], nums[pos + 1]))
        pos += 2
    n, m, x = nums[pos], nums[pos + 1], nums[pos + 2]
    pos += 3
    arestasG = []
    for _ in range(m):
        arestasG.append((nums[pos], nums[pos + 1]))
        pos += 2
    return t, arestasT, r, n, arestasG, x


def valida_arvore(t, arestasT):
    if len(arestasT) != t - 1:
        raise ValueError("T precisa ter t-1 arestas")
    adj = [set() for _ in range(t + 1)]
    for u, v in arestasT:
        if not (1 <= u <= t and 1 <= v <= t) or u == v or v in adj[u]:
            raise ValueError(f"aresta invalida em T: {u}-{v}")
        adj[u].add(v)
        adj[v].add(u)
    # conexa?
    visto = {1}
    pilha = [1]
    while pilha:
        u = pilha.pop()
        for w in adj[u]:
            if w not in visto:
                visto.add(w)
                pilha.append(w)
    if len(visto) != t:
        raise ValueError("T nao e conexa")
    return adj


def ordem_de_crescimento(t, arestasT, r):
    """Remove folhas diferentes de r ate sobrar r; a ordem e [r] + remocoes invertidas."""
    adjT = valida_arvore(t, arestasT)
    grau = [len(adjT[v]) for v in range(t + 1)]
    removido = [False] * (t + 1)
    folhas = [v for v in range(1, t + 1) if grau[v] == 1 and v != r]
    heapq.heapify(folhas)
    remov = []
    pai = {}
    for _ in range(t - 1):
        v = heapq.heappop(folhas)
        p = None
        for w in adjT[v]:
            if not removido[w]:
                p = w
                break
        pai[v] = p
        remov.append(v)
        removido[v] = True
        grau[p] -= 1
        if grau[p] == 1 and p != r:
            heapq.heappush(folhas, p)
    return [r] + remov[::-1], pai


def imersao(t, arestasT, r, n, arestasG, x, avisar=False):
    """Corolario 3.7. Devolve (phi, ordem, pai, livres).
    Se faltar vizinho livre, phi = None e o ultimo valor de livres e 0."""
    if not (1 <= r <= t) or not (1 <= x <= n):
        raise ValueError("r ou x fora da faixa")
    adjG = [set() for _ in range(n + 1)]
    for u, v in arestasG:
        if not (1 <= u <= n and 1 <= v <= n) or u == v or v in adjG[u]:
            raise ValueError(f"aresta invalida em G: {u}-{v}")
        adjG[u].add(v)
        adjG[v].add(u)
    adjG = [sorted(s) for s in adjG]
    if avisar and min(len(adjG[v]) for v in range(1, n + 1)) < t - 1:
        print("aviso: hipotese delta(G) >= |V(T)|-1 violada")

    ordem, pai = ordem_de_crescimento(t, arestasT, r)
    phi = {r: x}
    usados = {x}
    livres = []
    for i in range(1, t):
        u = ordem[i]
        cand = [w for w in adjG[phi[pai[u]]] if w not in usados]
        livres.append(len(cand))
        if not cand:
            return None, ordem, pai, livres
        phi[u] = cand[0]
        usados.add(cand[0])
    return phi, ordem, pai, livres


def verifica_ordem(t, arestasT, ordem, pai, r):
    assert ordem[0] == r
    assert sorted(ordem) == list(range(1, t + 1))
    adj = valida_arvore(t, arestasT)
    for i in range(1, t):
        u = ordem[i]
        anteriores = [w for w in adj[u] if w in ordem[:i]]
        assert anteriores == [pai[u]]


def verifica_imersao(t, arestasT, r, n, arestasG, x, phi):
    E = {frozenset(e) for e in arestasG}
    assert phi[r] == x
    assert len(phi) == t
    assert len(set(phi.values())) == t   # injetiva
    for a, b in arestasT:
        assert frozenset((phi[a], phi[b])) in E


def formata(t, ordem, pai, phi, livres):
    linhas = ["ordem: " + " ".join(map(str, ordem))]
    if t > 1:
        linhas.append("pai: " + " ".join(f"{u}->{pai[u]}" for u in ordem[1:]))
    else:
        linhas.append("pai: (raiz sozinha)")
    if phi is None:
        i = len(livres) + 1
        linhas.append(f"FALHA no passo i={i} (u={ordem[i - 1]}): nenhum vizinho livre")
    else:
        linhas.append("phi: " + " ".join(f"{u}->{phi[u]}" for u in range(1, t + 1)))
    linhas.append("livres por passo (i=2..t): " + " ".join(map(str, livres)))
    return "\n".join(linhas)


def main():
    if len(sys.argv) < 2:
        print("uso: python imersao_arvore.py entradas/arquivo.txt")
        return
    caminho = sys.argv[1]
    t, TE, r, n, GE, x = ler_entrada(caminho)
    graus = [0] * (n + 1)
    for u, v in GE:
        graus[u] += 1
        graus[v] += 1
    print(f"delta(G) = {min(graus[1:])}, t-1 = {t - 1}")
    phi, ordem, pai, livres = imersao(t, TE, r, n, GE, x, avisar=True)
    verifica_ordem(t, TE, ordem, pai, r)
    if phi is not None:
        verifica_imersao(t, TE, r, n, GE, x, phi)
    texto = formata(t, ordem, pai, phi, livres)
    print(texto)

    pasta = os.path.join(os.path.dirname(os.path.abspath(__file__)), "saidas")
    os.makedirs(pasta, exist_ok=True)
    nome = os.path.splitext(os.path.basename(caminho))[0] + ".out"
    with open(os.path.join(pasta, nome), "w") as arq:
        arq.write(texto + "\n")


if __name__ == "__main__":
    main()
