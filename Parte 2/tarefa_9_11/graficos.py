import random
import itertools
import networkx as nx
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from conectividade import conectividade_aresta, conectividade_vertice, kappa_G, lambda_G, delta_G

DOIS_K4 = [(0, 1), (0, 2), (0, 3), (1, 2), (1, 3), (2, 3), (2, 4), (2, 5), (3, 4), (3, 5), (4, 5)]


def fig_barras():
    dois_k4 = nx.Graph(DOIS_K4)
    familia = {"P5": nx.path_graph(5), "C6": nx.cycle_graph(6), "K5": nx.complete_graph(5),
               "K3,3": nx.complete_bipartite_graph(3, 3), "Q3": nx.hypercube_graph(3),
               "Petersen": nx.petersen_graph(), "2xK4": dois_k4}
    dados = []
    for G in familia.values():
        H = nx.convert_node_labels_to_integers(G)
        E = list(H.edges())
        n = len(H)
        dados.append((kappa_G(n, E), lambda_G(n, E), delta_G(n, E)))
    plt.figure(figsize=(9, 4))
    for j, rot in enumerate(["kappa", "lambda", "delta"]):
        plt.bar([i + 0.27 * (j - 1) for i in range(len(dados))], [d[j] for d in dados], 0.27, label=rot)
    plt.xticks(range(len(dados)), list(familia))
    plt.legend()
    plt.title("kappa <= lambda <= delta em cada grafo")
    plt.savefig("figuras/kappa_lambda_delta.png", dpi=120)
    plt.close()


def fig_separadores():
    n, E, x, y = 6, DOIS_K4, 0, 4
    pos = {0: (0, 1), 1: (0, -1), 2: (1.5, .6), 3: (1.5, -.6), 4: (3, 1), 5: (3, -1)}
    G = nx.Graph(E)
    fig, axs = plt.subplots(1, 2, figsize=(10, 3.5))
    cores = ["tab:green", "tab:orange", "tab:purple", "tab:brown"]
    paineis = [("vertices: separador em vermelho", conectividade_vertice(n, E, x, y)),
               ("arestas: corte em vermelho", conectividade_aresta(n, E, x, y))]
    for ax, (tit, (val, cams, sep)) in zip(axs, paineis):
        nx.draw(G, pos, ax=ax, with_labels=True, edge_color="lightgray", node_color=["lightblue"] * n, node_size=500)
        for c, cam in zip(cores, cams):
            nx.draw_networkx_edges(G, pos, edgelist=list(zip(cam, cam[1:])), width=3, edge_color=c, ax=ax)
        if tit.startswith("vertices"):
            nx.draw_networkx_nodes(G, pos, nodelist=sep, node_color="red", node_size=500, ax=ax)
        else:
            nx.draw_networkx_edges(G, pos, edgelist=sep, width=1.5, style="dashed", edge_color="red", ax=ax)
        ax.set_title(f"{tit}\nvalor = {val} = {len(cams)} caminhos")
    plt.savefig("figuras/separadores.png", dpi=120)
    plt.close()


def fig_dispersao():
    rng = random.Random(0)
    pts_kl, pts_ld = [], []
    for _ in range(150):
        n = rng.randint(4, 9)
        E = [e for e in itertools.combinations(range(n), 2) if rng.random() < 0.5]
        k, l, d = kappa_G(n, E), lambda_G(n, E), delta_G(n, E)
        r1, r2 = rng.uniform(-.15, .15), rng.uniform(-.15, .15)
        pts_kl.append((k + r1, l + r2))
        pts_ld.append((l + r1, d + r2))
    fig, (a1, a2) = plt.subplots(1, 2, figsize=(9, 4))
    for ax, pts, xl, yl in ((a1, pts_kl, "kappa", "lambda"), (a2, pts_ld, "lambda", "delta")):
        ax.scatter(*zip(*pts), s=12, alpha=.6)
        m = max(max(p) for p in pts)
        ax.plot([0, m], [0, m], "r--")
        ax.set_xlabel(xl)
        ax.set_ylabel(yl)
        ax.set_title(f"{xl} x {yl}: nenhum ponto abaixo da diagonal")
    plt.tight_layout()
    plt.savefig("figuras/dispersao.png", dpi=120)
    plt.close()


if __name__ == "__main__":
    fig_barras()
    fig_separadores()
    fig_dispersao()
    print("figuras gravadas em figuras/")
