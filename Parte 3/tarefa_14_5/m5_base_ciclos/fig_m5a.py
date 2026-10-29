import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import networkx as nx
from common.graphs import cube, edges_of
from common.draw import positions
from planar_contract import decidir
from m5_base_ciclos.m5 import face_basis

adj = cube()
r = decidir(adj)
vecs, eid = face_basis(adj, r["faces"], outer=0)
g = nx.Graph(edges_of(adj))
pos = positions(adj)
E = sorted(eid, key=eid.get)
fig, ax = plt.subplots(1, len(vecs), figsize=(3 * len(vecs), 3))
for a, v in zip(ax, vecs):
    em = [e for e in E if v >> eid[e] & 1]
    nx.draw(g, pos, ax=a, node_size=120, edge_color="lightgray", node_color="white", edgecolors="k")
    nx.draw_networkx_edges(g, pos, edgelist=em, ax=a, width=4, edge_color="tab:red")
fig.suptitle("Cubo: as 5 faces internas (a 6a e a externa)")
fig.savefig("figs/m5_base_cubo.png", dpi=110)
