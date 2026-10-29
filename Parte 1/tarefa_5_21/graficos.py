import time
import random
import numpy as np
import networkx as nx
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from prim import prim


def grafo_ponderado_conexo(n, extra=None):
    # arvore aleatoria + arestas extras com pesos aleatorios
    if extra is None:
        extra = random.randint(0, n)
    E = [(random.randint(1, i - 1), i, random.randint(1, 9)) for i in range(2, n + 1)]
    for _ in range(extra):
        u, v = random.sample(range(1, n + 1), 2)
        E.append((u, v, random.randint(1, 9)))
    return n, E


def fig_passos():
    n, E = 6, [(1, 2, 4), (1, 3, 2), (2, 3, 1), (2, 4, 5), (3, 4, 8), (3, 5, 10), (4, 5, 2), (4, 6, 6), (5, 6, 3)]
    F, log = prim(n, E, 1)
    G = nx.Graph()
    G.add_nodes_from(range(1, n + 1))
    G.add_edges_from((u, v) for u, v, w in E)
    pos = nx.spring_layout(G, seed=4)
    fig, axs = plt.subplots(2, 3, figsize=(15, 8))
    estilo = {"esc": ("#2ca02c", 5), "corte": ("#d62728", 2), "arv": ("#1f77b4", 3), "": ("#cccccc", 1)}
    for k, (ax, (S, corte, esc)) in enumerate(zip(axs.flat, log)):
        def cat(j):
            if j == esc:
                return "esc"
            if j in corte:
                return "corte"
            if j in F[:k]:
                return "arv"
            return ""
        nx.draw_networkx_nodes(G, pos, ax=ax, node_color=["#9fd3a8" if v in S else "#ddd" for v in G])
        nx.draw_networkx_labels(G, pos, ax=ax)
        for j, (u, v, w) in enumerate(E, 1):
            cor, larg = estilo[cat(j)]
            nx.draw_networkx_edges(G, pos, ax=ax, edgelist=[(u, v)], edge_color=cor, width=larg)
        nx.draw_networkx_edge_labels(G, pos, ax=ax, edge_labels={(u, v): w for u, v, w in E}, font_size=8)
        ax.set_title(f"passo {k + 1}: S={S}, escolhida e{esc}")
        ax.axis("off")
    for ax in axs.flat[len(log):]:
        ax.axis("off")
    fig.savefig("figuras/prim_passos.png", dpi=130, bbox_inches="tight")
    plt.close(fig)


def fig_corte_minimo():
    random.seed(1)
    pts = []
    for _ in range(40):
        n, E = grafo_ponderado_conexo(random.randint(5, 9))
        F, log = prim(n, E, 1)
        for S, corte, esc in log:
            pts.append((min(E[j - 1][2] for j in corte), E[esc - 1][2]))
    plt.figure()
    plt.scatter(*zip(*pts), alpha=.4)
    m = max(max(p) for p in pts)
    plt.plot([0, m], [0, m], "k--")
    plt.xlabel("peso minimo de dS (recalculado por varredura)")
    plt.ylabel("peso da aresta escolhida pelo Prim")
    plt.axis("equal")
    plt.savefig("figuras/corte_minimo.png", dpi=150)
    plt.close()


def fig_tempo():
    random.seed(0)
    ns = [10**3, 3 * 10**3, 10**4, 3 * 10**4, 10**5]
    ts = []
    for n in ns:
        n_, E = grafo_ponderado_conexo(n, extra=4 * n)
        t0 = time.perf_counter()
        prim(n_, E, 1, registrar=False)
        ts.append(time.perf_counter() - t0)
    s, _ = np.polyfit(np.log(ns), np.log(ts), 1)
    print(f"tempo: inclinacao {s:.2f}")
    plt.figure()
    plt.loglog(ns, ts, "o-", label=f"inclinacao {s:.2f}  (m log n => ~1.1)")
    plt.xlabel("n (m ~ 5n)")
    plt.ylabel("tempo (s)")
    plt.legend()
    plt.savefig("figuras/tempo_prim.png", dpi=150)
    plt.close()


if __name__ == "__main__":
    fig_passos()
    fig_corte_minimo()
    fig_tempo()
    print("figuras gravadas em figuras/")
