import sys
import os
import glob
from collections import deque


def busca(nA, nB, adj, mateA, mateB):
    """BFS alternante a partir de todos os expostos de A.
    Devolve (caminho, None, None) se achar b exposto, com caminho = [a0, b1, a1, ..., bk];
    senao (None, RA, RB) com os alcancados."""
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
                continue  # so arestas fora de M
            vistoB[b] = True
            predB[b] = a
            if mateB[b] == -1:
                # reconstroi o caminho voltando ate uma raiz
                caminho = []
                while b != -1:
                    a2 = predB[b]
                    caminho += [b, a2]
                    b = mateA[a2]
                return caminho[::-1], None, None
            a2 = mateB[b]  # de b segue so a aresta de M
            if not vistoA[a2]:
                vistoA[a2] = True
                fila.append(a2)
    RA = [a for a in range(nA) if vistoA[a]]
    RB = [b for b in range(nB) if vistoB[b]]
    return None, RA, RB


def aumenta(caminho, mateA, mateB):
    # alterna a pertinencia: as arestas (a_i, b_{i+1}) entram, as outras saem sozinhas
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


def verificar(nA, nB, adj, mateA, mateB, K):
    tam = 0
    for a in range(nA):
        b = mateA[a]
        if b != -1:
            assert b in adj[a] and mateB[b] == a
            tam += 1
    for b in range(nB):
        if mateB[b] != -1:
            assert mateA[mateB[b]] == b
    sK = set(K)
    for a in range(nA):
        for b in adj[a]:
            assert ("A", a) in sK or ("B", b) in sK
    assert len(K) == tam
    return tam


def ler_grafo(caminho):
    with open(caminho) as arq:
        nums = [int(x) for x in arq.read().split()]
    nA, nB, m = nums[0], nums[1], nums[2]
    adj = [[] for _ in range(nA)]
    vistas = set()
    for i in range(m):
        a, b = nums[3 + 2 * i], nums[4 + 2 * i]
        if not (0 <= a < nA and 0 <= b < nB):
            raise ValueError(f"aresta fora do intervalo: a{a}-b{b}")
        if (a, b) in vistas:
            raise ValueError(f"aresta repetida: a{a}-b{b}")
        vistas.add((a, b))
        adj[a].append(b)
    for a in range(nA):
        adj[a].sort()
    return nA, nB, adj


def roda_arquivo(caminho):
    nA, nB, adj = ler_grafo(caminho)
    mateA, mateB, RA, RB, K = emparelhamento_maximo(nA, nB, adj)
    tam = verificar(nA, nB, adj, mateA, mateB, K)
    M = " ".join(f"{a}-{mateA[a]}" for a in range(nA) if mateA[a] != -1)
    texto = "\n".join([
        f"tamanho {tam}",
        "M " + (M if M else "-"),
        "RA " + (" ".join(f"a{a}" for a in RA) if RA else "-"),
        "RB " + (" ".join(f"b{b}" for b in RB) if RB else "-"),
        "K " + (" ".join(f"{l.lower()}{x}" for l, x in K) if K else "-"),
    ])
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
