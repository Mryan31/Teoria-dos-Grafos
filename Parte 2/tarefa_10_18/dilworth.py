import sys
import os
import glob
from collections import deque


# ---------------------------------------------------------------------------
# copiado da tarefa 7.11: emparelhamento_maximo (com as auxiliares busca/aumenta)
# ---------------------------------------------------------------------------
def busca(nA, nB, adj, mateA, mateB):
    vistoA = [False] * nA
    vistoB = [False] * nB
    predB = [-1] * nB
    fila = deque()
    for a in range(nA):
        if mateA[a] == -1:
            vistoA[a] = True
            fila.append(a)
    while fila:
        a = fila.popleft()
        for b in adj[a]:
            if mateA[a] == b or vistoB[b]:
                continue
            vistoB[b] = True
            predB[b] = a
            if mateB[b] == -1:
                caminho = []
                while b != -1:
                    a2 = predB[b]
                    caminho += [b, a2]
                    b = mateA[a2]
                return caminho[::-1], None, None
            a2 = mateB[b]
            if not vistoA[a2]:
                vistoA[a2] = True
                fila.append(a2)
    RA = [a for a in range(nA) if vistoA[a]]
    RB = [b for b in range(nB) if vistoB[b]]
    return None, RA, RB


def aumenta(caminho, mateA, mateB):
    for i in range(0, len(caminho), 2):
        a, b = caminho[i], caminho[i + 1]
        mateA[a] = b
        mateB[b] = a


def emparelhamento_maximo(nA, nB, adj):
    mateA = [-1] * nA
    mateB = [-1] * nB
    while True:
        caminho, RA, RB = busca(nA, nB, adj, mateA, mateB)
        if caminho is None:
            break
        aumenta(caminho, mateA, mateB)
    sRA = set(RA)
    K = [("A", a) for a in range(nA) if a not in sRA] + [("B", b) for b in RB]
    return mateA, mateB, RA, RB, K
# ---------------------------------------------------------------------------


def fecho(n, pares):
    """Warshall. R[i][j] = True se x_i < x_j (estrito)."""
    R = [[False] * n for _ in range(n)]
    for i, j in pares:
        R[i][j] = True
    for k in range(n):
        for i in range(n):
            if R[i][k]:
                for j in range(n):
                    if R[k][j]:
                        R[i][j] = True
    for i in range(n):
        if R[i][i]:
            raise ValueError("ciclo: nao e ordem parcial")
    return R


def construir_BP(n, R):
    # aresta i- -- j+  <=>  x_i < x_j  (todas as comparacoes estritas)
    return [[j for j in range(n) if R[i][j]] for i in range(n)]


def dilworth_indices(n, pares):
    R = fecho(n, pares)
    adj = construir_BP(n, R)
    mateA, mateB, RA, RB, K = emparelhamento_maximo(n, n, adj)
    cadeias = []
    for j in range(n):
        if mateB[j] == -1:          # sem predecessor: comeca uma cadeia
            c = [j]
            while mateA[c[-1]] != -1:
                c.append(mateA[c[-1]])
            cadeias.append(c)
    sK = set(K)
    T = [i for i in range(n) if ("A", i) not in sK and ("B", i) not in sK]
    M = [(i, mateA[i]) for i in range(n) if mateA[i] != -1]
    return R, cadeias, T, M, K


def dilworth(elementos, relacoes):
    """Devolve (cadeias, T, M, K) com nomes; K = [('-', x) / ('+', y), ...]."""
    idx = {}
    for i, x in enumerate(elementos):
        if x in idx:
            raise ValueError(f"nome repetido: {x}")
        idx[x] = i
    pares = set()
    for x, y in relacoes:
        if x not in idx or y not in idx:
            raise ValueError(f"nome desconhecido em {x} < {y}")
        if x == y:
            raise ValueError(f"relacao {x} < {x} nao vale numa ordem estrita")
        pares.add((idx[x], idx[y]))   # repeticoes sao ignoradas
    n = len(elementos)
    R, cad, T, M, K = dilworth_indices(n, sorted(pares))
    verificar(n, R, cad, T, M, K)
    nome = elementos
    return ([[nome[i] for i in c] for c in cad], [nome[i] for i in T],
            [(nome[i], nome[j]) for i, j in M],
            [("-" if l == "A" else "+", nome[i]) for l, i in K])


def verificar(n, R, cadeias, T, M, K):
    todos = [v for c in cadeias for v in c]
    assert sorted(todos) == list(range(n))                   # particao
    for c in cadeias:
        for u, v in zip(c, c[1:]):
            assert R[u][v]                                    # cadeia (transitividade cobre o resto)
    for u in T:
        for v in T:
            assert not R[u][v]                                # anticadeia
    assert len(T) == len(cadeias) == n - len(M)
    sK = set(K)
    for i in range(n):
        for j in range(n):
            if R[i][j]:
                assert ("A", i) in sK or ("B", j) in sK
    assert len(K) == len(M)


def ler_entrada(caminho):
    with open(caminho) as arq:
        linhas = [l.split() for l in arq if l.strip()]
    n, m = int(linhas[0][0]), int(linhas[0][1])
    elementos = linhas[1] if n > 0 else []
    relacoes = [(linhas[2 + i][0], linhas[2 + i][1]) for i in range(m)]
    return elementos, relacoes


def roda_arquivo(caminho):
    elementos, relacoes = ler_entrada(caminho)
    cadeias, T, M, K = dilworth(elementos, relacoes)
    linhas = [f"cadeias {len(cadeias)}"]
    linhas += [" ".join(c) for c in cadeias]
    linhas.append(f"largura {len(T)}")
    linhas.append("T " + (" ".join(T) if T else "-"))
    linhas.append("M " + (" ".join(f"{x}-{y}" for x, y in M) if M else "-"))
    linhas.append("K " + (" ".join(f"{x}{s}" for s, x in K) if K else "-"))
    texto = "\n".join(linhas)
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
