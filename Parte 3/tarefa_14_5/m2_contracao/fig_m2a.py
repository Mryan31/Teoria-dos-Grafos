import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import networkx as nx
from common.graphs import cube, edges_of
from m2_contracao.m2 import contraction_trace, contract

adj = cube()
trace, k4 = contraction_trace(adj)
pos = nx.spring_layout(nx.Graph(edges_of(adj)), seed=1)
fig, ax = plt.subplots(1, len(trace) + 1, figsize=(3.2 * (len(trace) + 1), 3.4))
for k, a in enumerate(ax):
    g = nx.Graph(edges_of(adj))
    xy = trace[k][:2] if k < len(trace) else ()
    nx.draw(g, {v: pos[v] for v in g}, ax=a, with_labels=True, edgecolors="k",
            node_color=["orange" if v in xy else "white" for v in g],
            edge_color=["red" if set(e) == set(xy) else "gray" for e in g.edges()])
    a.set_title(f"J{len(g)}" + (f": contrair {xy}" if xy else " = K4"), fontsize=9)
    if xy:
        adj = contract(adj, *xy)
fig.savefig("figs/m2_sequencia_cubo.png", dpi=110)
