import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import networkx as nx
from common.graphs import cube, dodecahedron, edges_of
from planar_contract import decidir
from m6_tutte.m6 import tutte_positions

fig, ax = plt.subplots(1, 2, figsize=(10, 5))
for a, (nome, adj) in zip(ax, [("cubo", cube()), ("dodecaedro", dodecahedron())]):
    faces = decidir(adj)["faces"]
    o = max(range(len(faces)), key=lambda j: len(faces[j]))
    pos = tutte_positions(adj, faces[o])
    g = nx.Graph(edges_of(adj))
    nx.draw(g, pos, ax=a, node_size=90, node_color=["tab:red" if v in faces[o] else "white" for v in g],
            edgecolors="k")
    a.set_title(f"Tutte: {nome} (externa de {len(faces[o])} vertices)")
    a.set_aspect("equal")
fig.savefig("figs/m6_tutte.png", dpi=110)
