import math
import random
import time
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from corte import listas, corte_guloso, tamanho_corte

PET = [(i, (i + 1) % 5) for i in range(5)] + [(5 + i, 5 + (i + 2) % 5) for i in range(5)] + \
      [(i, 5 + i) for i in range(5)]
CUBO = [(v, v ^ (1 << b)) for v in range(8) for b in range(3) if v < v ^ (1 << b)]


def aleatorio(n, m, rng):
    E = set()
    while len(E) < m:
        u, v = rng.sample(range(n), 2)
        E.add((min(u, v), max(u, v)))
    return sorted(E)


def fig1():
    n = 10
    lado, E2, _ = corte_guloso(n, listas(n, PET))
    c = tamanho_corte(PET, lado)
    ang = [math.pi / 2 + 2 * math.pi * (i % 5) / 5 for i in range(n)]
    pos = [((1 if i < 5 else .5) * math.cos(a), (1 if i < 5 else .5) * math.sin(a)) for i, a in enumerate(ang)]
    fig, ax = plt.subplots(figsize=(6, 6))
    for u, v in PET:
        no = lado[u] != lado[v]
        ax.plot(*zip(pos[u], pos[v]), color="crimson" if no else "gray", lw=2.5 if no else 1,
                ls="-" if no else "--", zorder=1)
    for v in range(n):
        ax.text(*pos[v], v, ha="center", va="center", fontsize=10, zorder=3,
                bbox=dict(boxstyle="circle", fc="#f4a582" if lado[v] == 0 else "#92c5de"))
    ax.set_title(f"Petersen: corte {c} de m = {len(PET)} (m/2 = 7.5, maximo = 12)\n"
                 f"laranja = lado 0, azul = lado 1, vermelho = aresta no corte", fontsize=9)
    ax.axis("off")
    ax.set_aspect("equal")
    plt.savefig("figuras/fig1_petersen.png", dpi=90)
    plt.close(fig)


def fig2():
    rng = random.Random(3)
    Ea = aleatorio(30, 90, rng)
    fig, ax = plt.subplots(1, 3, figsize=(13, 4))
    for a, (nome, n, E) in zip(ax, [("Petersen", 10, PET), ("cubo Q3", 8, CUBO), ("aleatorio n=30, m=90", 30, Ea)]):
        lado, E2, _ = corte_guloso(n, listas(n, E))
        esp = [x / 2 for x in E2]
        a.step(range(len(esp)), esp, where="post", marker="o", ms=3, label="esperanca condicional")
        a.axhline(len(E) / 2, ls="--", c="C1", label="m/2")
        a.axhline(len(E), ls=":", c="k", lw=1, label="m")
        a.set(title=f"{nome}: corte final {esp[-1]:g}", xlabel="vertices fixados", ylabel="E[corte | fixados]")
        a.legend(fontsize=8)
    plt.tight_layout()
    plt.savefig("figuras/fig2_esperanca.png", dpi=90)
    plt.close(fig)


def fig3():
    rng = random.Random(5)
    n = 40
    E = aleatorio(n, 160, rng)
    lado, _, _ = corte_guloso(n, listas(n, E))
    c = tamanho_corte(E, lado)
    cortes = [tamanho_corte(E, [rng.randint(0, 1) for _ in range(n)]) for _ in range(5000)]
    acima = sum(1 for x in cortes if x >= c)
    fig, ax = plt.subplots(1, 2, figsize=(11, 4))
    ax[0].hist(cortes, bins=range(min(cortes), max(max(cortes), c) + 2), color="#92c5de", ec="w")
    ax[0].axvline(len(E) / 2, ls="--", c="C1", label=f"m/2 = {len(E) / 2:g}")
    ax[0].axvline(c, c="crimson", lw=2, label=f"guloso = {c}")
    ax[0].set(title=f"n=40, m=160: 5000 particoes aleatorias ({acima} chegaram ao guloso)",
              xlabel="tamanho do corte", ylabel="particoes")
    ax[0].title.set_fontsize(9)
    ax[0].legend()
    NM, T, OPS = [], [], []
    for n in [1000, 2000, 4000, 8000, 16000, 32000, 64000, 128000]:
        r = random.Random(n)
        m = 3 * n
        Eg = [(r.randrange(n), r.randrange(n)) for _ in range(m)]
        Eg = [(u, v) for u, v in Eg if u != v]
        adj = listas(n, Eg)
        t0 = time.perf_counter()
        _, _, ops = corte_guloso(n, adj)
        T.append(time.perf_counter() - t0)
        NM.append(n + len(Eg))
        OPS.append(ops + n)
    a, _ = np.polyfit(np.log(NM), np.log(T), 1)
    print(f"fig3: guloso {c}, m/2 = {len(E) / 2}, {acima} de 5000 aleatorias >= guloso; expoente do tempo {a:.2f}")
    ax[1].loglog(NM, T, "o-", label=f"medido, expoente {a:.2f}")
    ax[1].loglog(NM, [T[0] * x / NM[0] for x in NM], ":", label="inclinacao 1")
    ax[1].set(xlabel="n + m", ylabel="s", title="tempo (m = 3n)")
    ax[1].legend()
    plt.tight_layout()
    plt.savefig("figuras/fig3_aleatorias_tempo.png", dpi=90)
    plt.close(fig)


if __name__ == "__main__":
    fig1()
    fig2()
    fig3()
    print("figuras gravadas em figuras/")
