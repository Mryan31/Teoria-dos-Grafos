import time
import random
import numpy as np
import networkx as nx
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from refinamento import refinar

casos = {
    "P5": (5, [(1, 2), (2, 3), (3, 4), (4, 5)]),
    "T1": (6, [(1, 2), (1, 3), (1, 4), (2, 5), (3, 6)]),
    "T2": (6, [(1, 2), (1, 3), (1, 4), (2, 5), (5, 6)]),
    "K3,3": (6, [(a, b) for a in (1, 2, 3) for b in (4, 5, 6)]),
}


def grafo_aleatorio(n):
    # arvore aleatoria + arestas extras sem repeticao ate m = 2n
    E = set()
    for v in range(2, n + 1):
        u = random.randint(1, v - 1)
        E.add((u, v))
    while len(E) < 2 * n:
        u, v = random.sample(range(1, n + 1), 2)
        E.add((min(u, v), max(u, v)))
    return list(E)


def fig_classes_finais():
    fig, axs = plt.subplots(1, 4, figsize=(16, 4))
    for ax, (nome, (n, E)) in zip(axs, casos.items()):
        cores, rod, hist = refinar(n, E)
        G = nx.Graph()
        G.add_nodes_from(range(1, n + 1))
        G.add_edges_from(E)
        rot = {v: f"{v}\nc={cores[v]}" for v in G}
        nx.draw(G, nx.spring_layout(G, seed=3), ax=ax, labels=rot, font_size=8, node_size=700,
                node_color=[cores[v] for v in G], cmap=plt.cm.Set2, vmin=0, vmax=7)
        ax.set_title(f"{nome}: {len(set(cores[1:]))} classes, {rod} rodadas")
    fig.savefig("figuras/classes_finais.png", dpi=150, bbox_inches="tight")
    plt.close(fig)


def fig_classes_por_rodada():
    mais = dict(casos)
    mais["P7"] = (7, [(i, i + 1) for i in range(1, 7)])
    mais["vassoura"] = (8, [(1, 2), (2, 3), (3, 4), (4, 5), (5, 6), (5, 7), (5, 8)])
    mais["P12"] = (12, [(i, i + 1) for i in range(1, 12)])
    plt.figure()
    for nome, (n, E) in mais.items():
        _, rod, hist = refinar(n, E)
        plt.step(range(len(hist)), [len(set(c[1:])) for c in hist], where="post", marker="o", label=nome)
    plt.xlabel("rodada i (c_0 = grau)")
    plt.ylabel("numero de classes de c_i")
    plt.legend()
    plt.savefig("figuras/classes_por_rodada.png", dpi=150)
    plt.close()


def fig_tempo():
    random.seed(0)
    ns = [100, 200, 400, 800, 1600]

    def medir(gera):
        ts = []
        for n in ns:
            E = gera(n)
            t0 = time.perf_counter()
            refinar(n, E)
            ts.append(time.perf_counter() - t0)
        return ts

    curvas = {"caminho (pior caso)": medir(lambda n: [(i, i + 1) for i in range(1, n)]),
              "aleatorio, m = 2n": medir(grafo_aleatorio)}
    plt.figure()
    for nome, ts in curvas.items():
        a, b = np.polyfit(np.log(ns), np.log(ts), 1)
        print(f"{nome}: inclinacao {a:.2f}")
        plt.loglog(ns, ts, "o-", label=f"{nome}: inclinacao {a:.2f}")
    plt.xlabel("n")
    plt.ylabel("tempo (s)")
    plt.legend()
    plt.savefig("figuras/tempo.png", dpi=150)
    plt.close()


if __name__ == "__main__":
    fig_classes_finais()
    fig_classes_por_rodada()
    fig_tempo()
    print("figuras gravadas em figuras/")
