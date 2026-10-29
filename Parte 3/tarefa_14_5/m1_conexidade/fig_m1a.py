import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import networkx as nx
from common.graphs import prism, wheel, edges_of
from m1_conexidade.m1 import contractible_edges

fig, ax = plt.subplots(1, 2, figsize=(9, 4))
for a, (nome, adj) in zip(ax, [("prisma", prism()), ("roda, aro 5", wheel(5))]):
    g = nx.Graph(edges_of(adj))
    ce = set(contractible_edges(adj))
    cor = ["tab:green" if tuple(sorted(e)) in ce else "lightgray" for e in g.edges()]
    nx.draw(g, nx.spring_layout(g, seed=3), ax=a, with_labels=True, edge_color=cor,
            width=4, node_color="white", edgecolors="k")
    a.set_title(f"{nome}: {len(ce)} de {g.number_of_edges()} arestas contraiveis")
fig.savefig("figs/m1_contraiveis.png", dpi=110)
