import math
import random
import itertools
import time
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from simetrizacao import turan, simetriza, resolve


def circ(n, r=1):
    return [(r * math.cos(math.pi / 2 + 2 * math.pi * i / n), r * math.sin(math.pi / 2 + 2 * math.pi * i / n))
            for i in range(n)]


def desenha(ax, n, E, pos, Q, cores, tit):
    sQ = set(Q)
    for u, v in E:
        dest = u in sQ and v in sQ
        ax.plot(*zip(pos[u], pos[v]), color="crimson" if dest else "gray", lw=3 if dest else 1, zorder=1)
    for v in range(n):
        ax.text(*pos[v], v, ha="center", va="center", fontsize=10, zorder=3,
                bbox=dict(boxstyle="circle", fc=cores[v], ec="crimson" if v in sQ else "k",
                          lw=2 if v in sQ else 1))
    ax.set_title(tit, fontsize=9)
    ax.axis("off")
    ax.set_aspect("equal")
    ax.margins(.15)


def fig1():
    # misto_r2: um caso 2 e depois um caso 1
    n, r = 6, 2
    E = [(0, 2), (0, 3), (0, 5), (1, 2), (1, 4), (1, 5), (2, 5), (3, 4), (4, 5)]
    partes, log, A = simetriza(n, E)
    _, Q0, _ = resolve(n, r, E)
    Q = [P[0] for P in partes[:r + 1]]
    pal = ["#f4a582", "#92c5de", "#b8e186", "#fddbc7"]
    dono = {v: i for i, P in enumerate(partes) for v in P}
    cores = [pal[dono[v]] for v in range(n)]
    Ef = [(u, v) for u in range(n) for v in range(u + 1, n) if A[u][v]]
    # no final, cada parte numa coluna
    pos = [None] * n
    for i, P in enumerate(partes):
        for j, v in enumerate(P):
            pos[v] = (i, -j)
    ops = "; ".join(" ".join(f"{x}<-{y}" for x, y in c) for _, c, _ in log)
    fig, ax = plt.subplots(1, 2, figsize=(11, 5))
    desenha(ax[0], n, E, circ(n), Q0, cores, f"G (m={len(E)}, t_2(6)=9): clique recuperada {Q0}")
    desenha(ax[1], n, Ef, pos, Q, cores, f"depois de {ops}: multipartido com {len(partes)} partes, m={len(Ef)}")
    plt.tight_layout()
    plt.savefig("figuras/fig1_simetrizacao.png", dpi=90)
    plt.close(fig)


def fig2():
    fig, ax = plt.subplots(figsize=(8, 4.5))
    n, r = 14, 3
    _, t = turan(n, r)
    tot = n * (n - 1) // 2
    todas = list(itertools.combinations(range(n), 2))
    for s in range(5):
        rng = random.Random(s)
        E = rng.sample(todas, t + s)
        _, log, _ = simetriza(n, E)
        ms = [len(E)] + [l[2] for l in log]
        ax.step(range(len(ms)), ms, where="post", marker="o", ms=3, label=f"m0 = t+{s}: {len(log)} operacoes")
    ax.axhline(t, ls="--", c="k", lw=1, label=f"t_3(14) = {t}")
    ax.axhline(tot, ls=":", c="k", lw=1, label=f"C(14,2) = {tot}")
    ax.set(xlabel="operacao", ylabel="arestas", title="n = 14, r = 3: cada operacao sobe pelo menos 1 aresta")
    ax.legend(fontsize=8)
    plt.tight_layout()
    plt.savefig("figuras/fig2_arestas.png", dpi=90)
    plt.close(fig)


def fig3():
    N, T, OPS, COTA = [], [], [], []
    for n in [10, 14, 20, 28, 40, 56, 80]:
        rng = random.Random(n)
        r = 4
        _, t = turan(n, r)
        todas = list(itertools.combinations(range(n), 2))
        E = rng.sample(todas, t)
        t0 = time.perf_counter()
        _, log, _ = simetriza(n, E)
        T.append(time.perf_counter() - t0)
        N.append(n)
        OPS.append(len(log))
        COTA.append(n * (n - 1) // 2 - t)
    a, _ = np.polyfit(np.log(N), np.log(T), 1)
    print(f"fig3: expoente medido {a:.2f}; operacoes {OPS}; cota C(n,2) - m0 {COTA}")
    fig, ax = plt.subplots(1, 2, figsize=(10, 4))
    ax[0].loglog(N, T, "o-", label=f"medido, expoente {a:.2f}")
    ax[0].loglog(N, [T[0] * (x / N[0]) ** 4 for x in N], ":", label="inclinacao 4 (cota O(n^4))")
    ax[0].set(xlabel="n", ylabel="s", title="tempo, r = 4, m0 = t_4(n)")
    ax[0].legend()
    ax[1].plot(N, OPS, "o-", label="operacoes feitas")
    ax[1].plot(N, COTA, ":", label="C(n,2) - m0")
    ax[1].set(xlabel="n", title="nº de operacoes")
    ax[1].legend()
    plt.tight_layout()
    plt.savefig("figuras/fig3_tempo.png", dpi=90)
    plt.close(fig)


if __name__ == "__main__":
    fig1()
    fig2()
    fig3()
    print("figuras gravadas em figuras/")
