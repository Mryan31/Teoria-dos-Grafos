import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import networkx as nx
from common.graphs import dodecahedron, edges_of
from m2_contracao.m2 import contraction_trace, contract

adj = dodecahedron()
trace, _ = contraction_trace(adj)
pos = nx.spring_layout(nx.Graph(edges_of(adj)), seed=4)
fig, ax = plt.subplots(1, 3, figsize=(12, 4))
for a, (x, y, A, B) in zip(ax, trace[:3]):
    g = nx.Graph(edges_of(adj))
    cor = ["tab:red" if v in (x, y) else "tab:purple" if v in A and v in B else
           "tab:blue" if v in A else "tab:green" if v in B else "white" for v in g]
    nx.draw(g, {v: pos[v] for v in g}, ax=a, with_labels=True, node_color=cor, edgecolors="k")
    a.set_title(f"x={x}, y={y}  A(azul)={A}  B(verde)={B}", fontsize=8)
    adj = contract(adj, x, y)
fig.savefig("figs/m2_vizinhancas.png", dpi=110)
