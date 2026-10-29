import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import networkx as nx
from common.graphs import petersen, edges_of
from planar_contract import decidir

adj = petersen()
g = nx.Graph(edges_of(adj))
r = decidir(adj)
cor = {}
for j, S in enumerate(r["model"].values()):
    for v in S:
        cor[v] = plt.cm.tab10.colors[j]
pos = nx.shell_layout(g, [[0, 1, 2, 3, 4], [5, 6, 7, 8, 9]])
dentro = [e for e in g.edges() if cor[e[0]] == cor[e[1]]]
plt.figure(figsize=(6, 6))
nx.draw(g, pos, node_color=[cor[v] for v in g], with_labels=True, edge_color="lightgray")
nx.draw_networkx_edges(g, pos, edgelist=dentro, width=4)
plt.title(f"Petersen: menor {r['kind']} (um conjunto de ramificacao por cor)")
plt.savefig("figs/m4_petersen.png", dpi=110)
