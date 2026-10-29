import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import networkx as nx
from common.graphs import random_planar_3conn, edges_of
from common.draw import fill_faces
from planar_contract import decidir
from m6_tutte.m6 import tutte_positions, verify_tutte

adj = random_planar_3conn(14, seed=37)
faces = decidir(adj)["faces"]
fig, ax = plt.subplots(1, 2, figsize=(10, 5))
escolhas = [min(range(len(faces)), key=lambda j: len(faces[j])),
            max(range(len(faces)), key=lambda j: len(faces[j]))]
for a, o in zip(ax, escolhas):   # duas escolhas de face externa
    pos = tutte_positions(adj, faces[o])
    r = verify_tutte(adj, pos, faces, o)
    nx.draw(nx.Graph(edges_of(adj)), pos, ax=a, node_size=60, node_color="white", edgecolors="k")
    fill_faces(a, pos, faces, hl=set(range(99)), cor="lightskyblue")
    a.set_aspect("equal")
    a.set_title(f"externa {o} ({len(faces[o])} vertices): cruzamentos={r['crossings']}, "
                f"menor curva={r['min_turn']:.1e}", fontsize=9)
fig.savefig("figs/m6_tutte_aleatorio.png", dpi=110)
