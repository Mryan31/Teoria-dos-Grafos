import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import networkx as nx
from common.graphs import k4_sub, edges_of, from_edges
from m1_conexidade.m1 import find_separator

dois_k4 = from_edges([(0, 1), (0, 2), (0, 3), (1, 2), (1, 3), (2, 3), (3, 4), (3, 5), (3, 6), (4, 5), (4, 6), (5, 6)])
fig, ax = plt.subplots(1, 2, figsize=(9, 4))
for a, (nome, adj) in zip(ax, [("subdivisao de K4", k4_sub()), ("dois K4 num vertice", dois_k4)]):
    g = nx.Graph(edges_of(adj))
    S = find_separator(adj)
    nx.draw(g, nx.spring_layout(g, seed=2), ax=a, with_labels=True, edgecolors="k",
            node_color=["tab:red" if v in S else "white" for v in g])
    a.set_title(f"{nome}: separador {S}")
fig.savefig("figs/m1_separadores.png", dpi=110)
