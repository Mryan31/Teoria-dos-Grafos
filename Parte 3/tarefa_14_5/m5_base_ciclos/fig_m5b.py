import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import networkx as nx
from common.graphs import cube, edges_of
from common.draw import positions
from planar_contract import decidir
from m5_base_ciclos.m5 import face_basis, fundamental_basis

adj = cube()
g = nx.Graph(edges_of(adj))
pos = positions(adj)
fig, ax = plt.subplots(1, 2, figsize=(9, 4))
bases = {"faces (esparsa)": face_basis(adj, decidir(adj)["faces"])[0],
         "ciclos fundamentais (arvore BFS de 0)": fundamental_basis(adj, root=0)[0]}
for a, (nome, vecs) in zip(ax, bases.items()):
    eid = {e: i for i, e in enumerate(edges_of(adj))}
    uso = {e: sum(v >> i & 1 for v in vecs) for e, i in eid.items()}
    nx.draw(g, pos, ax=a, node_size=100, node_color="white", edgecolors="k",
            edge_color=[uso[tuple(sorted(e))] for e in g.edges()],
            edge_cmap=plt.cm.coolwarm, edge_vmin=0, edge_vmax=3, width=3)
    a.set_title(f"{nome}: uso max. {max(uso.values())}", fontsize=9)
fig.savefig("figs/m5_uso_arestas.png", dpi=110)
