import time
import random
import collections
import numpy as np
import networkx as nx
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from prufer import codificar, decodificar


def fig_arvore():
    n, E = 7, [(1, 4), (3, 4), (4, 2), (2, 6), (5, 6), (6, 7)]
    codigo, folhas = codificar(n, E)
    T = nx.Graph(E)
    passo = {x: i for i, x in enumerate(folhas, 1)}
    rot = {v: f"{v}\n" + (f"x{passo[v]}" if v in passo else "fim") for v in T}
    plt.figure()
    nx.draw(T, nx.kamada_kawai_layout(T), labels=rot, font_size=8, node_size=800,
            node_color=["#9fd3a8" if v in passo else "#f6c85f" for v in T])
    plt.title(f"folhas removidas em ordem x1..x5; P(T) = {tuple(codigo)}")
    plt.savefig("figuras/prufer_arvore.png", dpi=150, bbox_inches="tight")
    plt.close()


def fig_grau():
    random.seed(1)
    n = 40
    E = [(random.randint(1, i - 1), i) for i in range(2, n + 1)]
    codigo, _ = codificar(n, E)
    grau = collections.Counter(v for e in E for v in e)
    ocorr = collections.Counter(codigo)
    xs = range(1, n + 1)
    plt.figure(figsize=(10, 4))
    plt.bar([v - .2 for v in xs], [grau[v] for v in xs], .4, label="grau de v em T")
    plt.bar([v + .2 for v in xs], [1 + ocorr[v] for v in xs], .4, label="1 + ocorrencias de v em P(T)")
    plt.xlabel("vertice v")
    plt.legend()
    plt.savefig("figuras/grau_vs_codigo.png", dpi=150)
    plt.close()


def fig_tempo():
    random.seed(0)
    ns = [10**3, 3 * 10**3, 10**4, 3 * 10**4, 10**5, 3 * 10**5]
    te, td = [], []
    for n in ns:
        E = [(random.randint(1, i - 1), i) for i in range(2, n + 1)]
        t0 = time.perf_counter()
        a, _ = codificar(n, E)
        te.append(time.perf_counter() - t0)
        t0 = time.perf_counter()
        decodificar(a)
        td.append(time.perf_counter() - t0)
    plt.figure()
    for nome, ts in [("codificar", te), ("decodificar", td)]:
        s, _ = np.polyfit(np.log(ns), np.log(ts), 1)
        print(f"{nome}: inclinacao {s:.2f}")
        plt.loglog(ns, ts, "o-", label=f"{nome}: inclinacao {s:.2f}")
    plt.xlabel("n")
    plt.ylabel("tempo (s)")
    plt.legend()
    plt.savefig("figuras/tempo_prufer.png", dpi=150)
    plt.close()


if __name__ == "__main__":
    fig_arvore()
    fig_grau()
    fig_tempo()
    print("figuras gravadas em figuras/")
