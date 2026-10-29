import time
import random
import numpy as np
import networkx as nx
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from nucleo_denso import nucleo

K4 = [(1, 2), (1, 3), (1, 4), (2, 3), (2, 4), (3, 4)]
K5b = [(a, b) for i, a in enumerate([1, 3, 4, 5, 7]) for b in [1, 3, 4, 5, 7][i + 1:]]

casos = {
    "K4 + cauda": (7, K4 + [(4, 5), (5, 6), (6, 7)]),
    "K5 + isolado + grau 2": (7, K5b + [(6, 3), (6, 5)]),
    "K4 + estrela": (8, K4 + [(4, 5), (5, 6), (5, 7), (5, 8)]),
}


def grafo_aleatorio(n, fator):
    E = set()
    while len(E) < fator * n:
        a, b = random.sample(range(1, n + 1), 2)
        E.add((min(a, b), max(a, b)))
    return list(E)


def fig_subgrafo():
    fig, axs = plt.subplots(1, 3, figsize=(15, 4))
    for ax, (nome, (n, E)) in zip(axs, casos.items()):
        H, mH, log = nucleo(n, E)
        ordem = {v: i for i, (v, *_) in enumerate(log, 1)}
        G = nx.Graph()
        G.add_nodes_from(range(1, n + 1))
        G.add_edges_from(E)
        rot = {v: (f"{v}\n#{ordem[v]}" if v in ordem else str(v)) for v in G}
        cor = ["#9fd3a8" if v in H else "#cccccc" for v in G]
        ec = ["#1b7f3b" if a in H and b in H else "#aaaaaa" for a, b in G.edges]
        nx.draw(G, nx.spring_layout(G, seed=2), ax=ax, labels=rot, font_size=8, node_color=cor,
                edge_color=ec, node_size=650)
        ax.set_title(f"{nome}: |H|={len(H)}")
    fig.savefig("figuras/subgrafo_H.png", dpi=150, bbox_inches="tight")
    plt.close(fig)


def fig_densidade():
    n, E = casos["K5 + isolado + grau 2"]
    H, mH, log = nucleo(n, E)
    dens = [mF / nF for (_, _, mF, nF) in log] + [mH / len(H)]
    graus = [d for (_, d, _, _) in log]
    plt.figure()
    plt.step(range(len(dens)), dens, where="post", marker="o", label="m_F / n_F (= grau medio / 2)")
    plt.plot(range(len(graus)), graus, "s--", label="grau do vertice removido (<= m_F / n_F)")
    plt.xlabel("vertices removidos")
    plt.legend()
    plt.savefig("figuras/densidade.png", dpi=150)
    plt.close()


def fig_tempo():
    random.seed(0)
    ns = [1000, 2000, 4000, 8000, 16000]
    ts = []
    for n in ns:
        E = grafo_aleatorio(n, 3)
        t0 = time.perf_counter()
        nucleo(n, E)
        ts.append(time.perf_counter() - t0)
    a, b = np.polyfit(np.log(ns), np.log(ts), 1)
    print(f"tempo: inclinacao {a:.2f}")
    plt.figure()
    plt.loglog(ns, ts, "o-", label=f"inclinacao {a:.2f}")
    plt.xlabel("n (m = 3n)")
    plt.ylabel("tempo (s)")
    plt.legend()
    plt.savefig("figuras/tempo_nucleo.png", dpi=150)
    plt.close()


if __name__ == "__main__":
    fig_subgrafo()
    fig_densidade()
    fig_tempo()
    print("figuras gravadas em figuras/")
