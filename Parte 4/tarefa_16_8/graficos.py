import math
import random
import time
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from fluxo import residuos, corrigir
from testes import gerar

PT = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 0, 1, 2, 3, 4]
PH = [1, 2, 3, 4, 0, 7, 8, 9, 5, 6, 5, 6, 7, 8, 9]
PV = [3, 4, 1, 3, 2, 3, 1, 1, 4, 2, 4, 4, 3, 3, 1]


def fig1():
    n, k = 10, 5
    f, log, K0 = corrigir(n, PT, PH, PV, k)
    ang = [math.pi / 2 + 2 * math.pi * (i % 5) / 5 for i in range(n)]
    pos = [((1 if i < 5 else .5) * math.cos(a), (1 if i < 5 else .5) * math.sin(a)) for i, a in enumerate(ang)]

    def desenha(ax, T, H, w, b, P, tit):
        for e in range(len(T)):
            c, lw = ("crimson", 3) if e in P else ("gray", 1)
            ax.annotate("", pos[H[e]], pos[T[e]],
                        arrowprops=dict(arrowstyle="-|>", color=c, lw=lw, shrinkA=12, shrinkB=12))
            ax.text(*[(p + q) / 2 for p, q in zip(pos[T[e]], pos[H[e]])], w[e], fontsize=8, ha="center",
                    bbox=dict(fc="w", ec="none", pad=.5))
        for v in range(n):
            ax.text(*pos[v], f"{v}\nb={b[v]}", ha="center", va="center", fontsize=7,
                    bbox=dict(boxstyle="circle", fc="#f4a582" if b[v] > 0 else "#92c5de" if b[v] < 0 else "#eee"))
        ax.set_title(tit)
        ax.axis("off")
        ax.set_xlim(-1.3, 1.3)
        ax.set_ylim(-1.3, 1.3)

    fig, ax = plt.subplots(1, 2, figsize=(11, 5.5))
    desenha(ax[0], PT, PH, PV, residuos(n, PT, PH, PV), log[0]["P"], f"inicio: K={K0}; P da 1a correcao")
    T = [h if x < 0 else t for t, h, x in zip(PT, PH, f)]
    H = [t if x < 0 else h for t, h, x in zip(PT, PH, f)]
    desenha(ax[1], T, H, [abs(x) for x in f], [0] * n, (), "fim: b=0 e 0<|f|<5")
    plt.savefig("figuras/fig1_petersen.png", dpi=90)
    plt.close(fig)


def fig2():
    rng = random.Random(1)
    n, k = 30, 5
    t, h, v = gerar(n, 25, k, rng, maxlen=8)
    fig, ax = plt.subplots(1, 2, figsize=(10, 4))
    for a, (N, T, H, V, kk, nome) in zip(ax, [(10, PT, PH, PV, 5, "Petersen, Z_5"),
                                              (n, t, h, v, k, "aleatorio, n=30, Z_5")]):
        f, log, K0 = corrigir(N, T, H, V, kk)
        Ks = [K0] + [l["K"] for l in log]
        a.step(range(len(Ks)), Ks, where="post", marker="o")
        a.plot([0, len(Ks) - 1], [K0, 0], "--", c="C1", label="reta de inclinacao -2k")
        a.set(title=f"{nome}: {len(log)} correcoes, K0={K0}<=2m(k-1)={2 * len(T) * (kk - 1)}",
              xlabel="correcao", ylabel="K(f)")
        a.title.set_fontsize(9)
        a.legend()
    plt.tight_layout()
    plt.savefig("figuras/fig2_K.png", dpi=90)
    plt.close(fig)


def fig3():
    M, T, OPS, B = [], [], [], []
    for c in [100, 200, 400, 800, 1600, 3200, 6400, 12800]:
        rng = random.Random(c)
        n = c // 2
        t, h, v = gerar(n, c, 5, rng, maxlen=4)
        m = len(t)
        t0 = time.perf_counter()
        f, log, K0 = corrigir(n, t, h, v, 5)
        T.append(time.perf_counter() - t0)
        M.append(m)
        OPS.append(sum(l["ops"] for l in log) + m)
        B.append(m * (n + m))
    a, b = np.polyfit(np.log(M), np.log(T), 1)
    razao = [o / x for o, x in zip(OPS, B)]
    print(f"fig3: expoente medido {a:.2f}; razao operacoes / m(n+m) entre {min(razao):.3f} e {max(razao):.3f}")
    fig, ax = plt.subplots(1, 2, figsize=(10, 4))
    ax[0].loglog(M, T, "o-", label=f"medido, expoente {a:.2f}")
    ax[0].loglog(M, [T[0] * (x / M[0]) ** 2 for x in M], ":", label="inclinacao 2")
    ax[0].set(xlabel="m", ylabel="s")
    ax[0].legend()
    ax[1].loglog(M, OPS, "o-", label="operacoes contadas")
    ax[1].loglog(M, B, ":", label="m(n+m)")
    ax[1].set(xlabel="m")
    ax[1].legend()
    plt.tight_layout()
    plt.savefig("figuras/fig3_tempo.png", dpi=90)
    plt.close(fig)


if __name__ == "__main__":
    fig1()
    fig2()
    fig3()
    print("figuras gravadas em figuras/")
