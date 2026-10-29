import time
import random
import itertools
import numpy as np
import networkx as nx
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from havel_hakimi import havel_hakimi
from testes import erdos_gallai


def grafo_aleatorio(n, fator):
    # grafo simples com m = fator * n arestas
    E = set()
    while len(E) < fator * n:
        a, b = random.sample(range(1, n + 1), 2)
        E.add((min(a, b), max(a, b)))
    return list(E)


def fig_realizacoes():
    fig, axs = plt.subplots(1, 3, figsize=(13, 4))
    for ax, d in zip(axs, [(4, 3, 3, 2, 2, 2), (5, 4, 3, 3, 2, 1), (3, 3, 3, 3, 2, 2)]):
        ok, E, passos, obs = havel_hakimi(list(d))
        G = nx.Graph()
        G.add_nodes_from(range(1, len(d) + 1))
        G.add_edges_from(E)
        rot = {v: f"{v}\nd={d[v - 1]}" for v in G}
        cor = ["#9fd3a8" if G.degree(v) == d[v - 1] else "#f19999" for v in G]  # verde = grau certo
        nx.draw(G, nx.circular_layout(G), ax=ax, labels=rot, font_size=8, node_size=800, node_color=cor)
        ax.set_title(f"{d}  passos: {len(passos)}")
    fig.savefig("figuras/realizacoes.png", dpi=150, bbox_inches="tight")
    plt.close(fig)


def fig_contagem():
    ns = range(2, 8)
    cont = {"HH": [], "EG": []}
    for n in ns:
        seqs = [d for d in itertools.product(range(n), repeat=n) if list(d) == sorted(d, reverse=True)]
        cont["HH"].append(sum(havel_hakimi(list(d))[0] for d in seqs))
        cont["EG"].append(sum(erdos_gallai(list(d)) for d in seqs))
    print("HH:", cont["HH"], " EG:", cont["EG"])
    x = list(ns)
    plt.figure()
    plt.bar([i - 0.2 for i in x], cont["HH"], 0.4, label="Havel-Hakimi")
    plt.bar([i + 0.2 for i in x], cont["EG"], 0.4, label="Erdos-Gallai")
    plt.yscale("log")
    plt.xlabel("n")
    plt.ylabel("sequencias graficas (nao crescentes, entradas < n)")
    plt.legend()
    plt.savefig("figuras/contagem_graficas.png", dpi=150)
    plt.close()


def fig_tempo():
    random.seed(0)
    ns = [250, 500, 1000, 2000, 4000]
    ts = []
    for n in ns:
        grau = [0] * n
        for a, b in grafo_aleatorio(n, 4):
            grau[a - 1] += 1
            grau[b - 1] += 1
        t0 = time.perf_counter()
        havel_hakimi(grau)
        ts.append(time.perf_counter() - t0)
    a, b = np.polyfit(np.log(ns), np.log(ts), 1)
    print(f"tempo: inclinacao {a:.2f}")
    plt.figure()
    plt.loglog(ns, ts, "o-", label=f"inclinacao {a:.2f}")
    plt.xlabel("n")
    plt.ylabel("tempo (s)")
    plt.legend()
    plt.savefig("figuras/tempo_hh.png", dpi=150)
    plt.close()


if __name__ == "__main__":
    fig_realizacoes()
    fig_contagem()
    fig_tempo()
    print("figuras gravadas em figuras/")
