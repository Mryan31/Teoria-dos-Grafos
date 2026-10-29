import itertools
import random
from fractions import Fraction
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from birkhoff import birkhoff

Z9 = [[Fraction(x, 9) for x in l] for l in [[6, 2, 1], [2, 5, 2], [1, 2, 6]]]


def ds_aleatoria(n, k, seed):
    rng = random.Random(seed)
    pesos = [rng.randint(1, 9) for _ in range(k)]
    tot = sum(pesos)
    X = [[Fraction(0)] * n for _ in range(n)]
    for p in pesos:
        s = list(range(n))
        rng.shuffle(s)
        for i in range(n):
            X[i][s[i]] += Fraction(p, tot)
    return X


def fig_decomposicao():
    X = Z9
    termos, hist = birkhoff(X)
    n, q = len(X), len(termos)

    def perm(al, s):
        P = np.zeros((n, n))
        P[range(n), s] = float(al)
        return P
    mats = [np.array(X, dtype=float)] + [perm(al, s) for al, s in termos]
    tits = ["X"] + [f"{al} . P{j + 1}" for j, (al, s) in enumerate(termos)]
    fig, axs = plt.subplots(1, q + 1, figsize=(2.3 * (q + 1), 2.6))
    for ax, Mt, t in zip(axs, mats, tits):
        ax.imshow(Mt, cmap="Blues", vmin=0, vmax=1)
        ax.set_title(t, fontsize=9)
        ax.set_xticks([])
        ax.set_yticks([])
        for i in range(n):
            for j in range(n):
                ax.text(j, i, f"{Mt[i, j]:.2f}", ha="center", va="center", fontsize=7)
    plt.tight_layout()
    plt.savefig("figuras/decomposicao.png", dpi=120)
    plt.close()


def fig_passos():
    X = Z9
    termos, hist = birkhoff(X)
    passos = range(1, len(hist) + 1)
    fig, (a1, a2) = plt.subplots(1, 2, figsize=(8, 3))
    a1.plot(passos, [h[0] for h in hist], "o-")
    a1.set_title("entradas positivas (estritamente decrescente)")
    a1.set_ylim(bottom=0)
    a2.plot([0] + list(passos), [1.0] + [float(h[2]) for h in hist], "s-")
    a2.set_title("r = soma de cada linha/coluna de R")
    for ax in (a1, a2):
        ax.set_xlabel("passo")
    plt.tight_layout()
    plt.savefig("figuras/passos.png", dpi=120)
    plt.close()


def fig_custos():
    n = 5
    rng = random.Random(0)
    W = [[rng.randint(0, 9) for _ in range(n)] for _ in range(n)]

    def custo(s):
        return sum(W[i][s[i]] for i in range(n))
    otimo = min(custo(s) for s in itertools.permutations(range(n)))
    cX, cP = [], []
    for sem in range(60):
        X = ds_aleatoria(n, 6, sem)
        termos, _ = birkhoff(X)
        cX.append(float(sum(W[i][j] * X[i][j] for i in range(n) for j in range(n))))
        cP.append(min(custo(s) for _, s in termos))
    plt.figure()
    plt.scatter(cX, cP, s=12, label="<W,X> x melhor permutacao da decomposicao")
    plt.plot([min(cX), max(cX)], [min(cX), max(cX)], "r--", label="y = x")
    plt.axhline(otimo, color="k", ls=":", label=f"otimo da atribuicao = {otimo}")
    plt.legend(fontsize=8)
    plt.xlabel("custo fracionario <W,X>")
    plt.ylabel("melhor custo dentro da decomposicao")
    plt.savefig("figuras/custos.png", dpi=120)
    plt.close()


if __name__ == "__main__":
    fig_decomposicao()
    fig_passos()
    fig_custos()
    print("figuras gravadas em figuras/")
