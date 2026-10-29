import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import networkx as nx
from common.graphs import cube, edges_of
from common.draw import positions, fill_faces
from m2_contracao.m2 import contraction_trace, contract
from m3_faces.m3 import k4_faces, boundary_cycle, interval_test, insert_xy

adj = cube()
trace, k4 = contraction_trace(adj)
K = 1
Js = [adj]
for x, y, A, B in trace:
    Js.append(contract(Js[-1], x, y))
faces = k4_faces(*sorted(k4))
for k in range(len(trace) - 1, K - 1, -1):   # desfaz ate o passo K; guarda faces antes/depois
    x, y, A, B = trace[k]
    C = boundary_cycle(faces, x)
    i, Ao = interval_test(C, A, B)
    antes, faces = faces, insert_xy(faces, x, x, y, C, Ao, B, i)
pos = positions(Js[K])
fig, ax = plt.subplots(1, 2, figsize=(9, 4.5))
for a, g, f, hl in [(ax[0], Js[K + 1], antes, {x}), (ax[1], Js[K], faces, {x, y})]:
    nx.draw(nx.Graph(edges_of(g)), {v: pos[v] for v in g}, ax=a, with_labels=True,
            node_color="white", edgecolors="k")
    fill_faces(a, pos, f, hl)
ax[0].set_title(f"H: faces em z={x}")
ax[1].set_title(f"J: novas faces com x={x}, y={y}")
fig.savefig("figs/m3_antes_depois.png", dpi=110)
