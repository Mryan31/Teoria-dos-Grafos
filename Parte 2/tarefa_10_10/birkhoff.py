import sys
import os
import glob
from fractions import Fraction
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


def valida(X, soma=1):
    n = len(X)
    for i, linha in enumerate(X):
        if len(linha) != n:
            raise ValueError(f"a matriz nao e quadrada (linha {i})")
        for j, x in enumerate(linha):
            if x < 0:
                raise ValueError(f"entrada negativa em ({i}, {j})")
    for i in range(n):
        if sum(X[i]) != soma:
            raise ValueError(f"a linha {i} soma {sum(X[i])}, devia ser {soma}")
    for j in range(n):
        s = sum(X[i][j] for i in range(n))
        if s != soma:
            raise ValueError(f"a coluna {j} soma {s}, devia ser {soma}")


def positivas(R):
    return sum(1 for linha in R for x in linha if x > 0)


def birkhoff(X, soma=1):
    """Algoritmo da prova do Teorema 10.7. Devolve (termos, hist):
    termos = [(alfa, sigma), ...], hist = [(entradas > 0 antes do passo, alfa, r depois), ...]."""
    X = [[Fraction(x) for x in linha] for linha in X]
    valida(X, soma)
    n = len(X)
    R = [list(linha) for linha in X]
    r = Fraction(soma)
    termos = []
    hist = []
    while r > 0:
        adj = [[j for j in range(n) if R[i][j] > 0] for i in range(n)]
        mateA, _, _, _, _ = emparelhamento_maximo(n, n, adj)
        assert all(mateA[i] != -1 for i in range(n)), "sem emparelhamento perfeito (Hall)"
        sigma = list(mateA)
        alfa = min(R[i][sigma[i]] for i in range(n))
        assert alfa > 0
        npos = positivas(R)
        for i in range(n):
            R[i][sigma[i]] -= alfa
        r -= alfa
        # invariantes: R >= 0, todas as somas iguais a r, alguma entrada sumiu
        assert all(x >= 0 for linha in R for x in linha)
        assert all(sum(R[i]) == r for i in range(n))
        assert all(sum(R[i][j] for i in range(n)) == r for j in range(n))
        assert positivas(R) < npos
        termos.append((alfa, sigma))
        hist.append((npos, alfa, r))
    assert all(x == 0 for linha in R for x in linha)
    return termos, hist


def verificar(X, termos, soma=1):
    X = [[Fraction(x) for x in linha] for linha in X]
    n = len(X)
    assert all(a > 0 for a, _ in termos)
    assert sum(a for a, _ in termos) == soma
    Y = [[Fraction(0)] * n for _ in range(n)]
    for a, s in termos:
        assert sorted(s) == list(range(n))
        for i in range(n):
            Y[i][s[i]] += a
    assert Y == X


def ler_matriz(caminho):
    with open(caminho) as arq:
        partes = arq.read().split()
    n = int(partes[0])
    vals = [Fraction(p) for p in partes[1:1 + n * n]]   # le como texto, nunca via float
    return [vals[i * n:(i + 1) * n] for i in range(n)]


def roda_arquivo(caminho):
    X = ler_matriz(caminho)
    termos, hist = birkhoff(X)
    verificar(X, termos)
    linhas = [f"termos {len(termos)}"]
    for a, s in termos:
        linhas.append(f"{a} : " + " ".join(map(str, s)))
    linhas.append(f"soma {sum(a for a, _ in termos)}")
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
