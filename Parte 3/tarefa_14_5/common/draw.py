"""Funcoes de desenho (so para as figuras; aqui o networkx e permitido)."""
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import networkx as nx


def positions(adj):
    g = nx.Graph([(u, v) for u in adj for v in adj[u]])
    ok, emb = nx.check_planarity(g)
    if ok:
        return nx.combinatorial_embedding_to_pos(emb)
    return nx.spring_layout(g, seed=1)


def fill_faces(ax, pos, faces, hl=(), cor="gold"):
    def area(f):
        return sum(pos[a][0] * pos[b][1] - pos[b][0] * pos[a][1] for a, b in zip(f, f[1:] + f[:1]))
    sgn = 1 if sum(area(f) > 0 for f in faces) * 2 > len(faces) else -1
    for f in faces:
        f = list(f)
        if area(f) * sgn > 0 and any(v in hl for v in f):
            ax.fill([pos[v][0] for v in f], [pos[v][1] for v in f], color=cor, alpha=.5, zorder=0)


def draw_interval(C, x, y, A, B, i=None, Ao=None, ax=None):
    """C no circulo; x, y no centro; A em vermelho, B em azul; P_i em laranja (se i nao e None)."""
    ax = ax or plt.gca()
    L = len(C)
    ax.axis("off")
    P = {v: (np.cos(2 * np.pi * j / L), np.sin(2 * np.pi * j / L)) for j, v in enumerate(C)}
    P[x], P[y] = (-.3, .15), (.3, -.15)
    ax.plot(*zip(P[x], P[y]), "k", lw=2)
    for u, w in zip(C, C[1:] + C[:1]):
        ax.plot(*zip(P[u], P[w]), "gray", lw=1)
    for a in A:
        ax.plot(*zip(P[x], P[a]), "r--", lw=1)
    for b in B:
        ax.plot(*zip(P[y], P[b]), "b--", lw=1)
    if i is not None:
        s, e = C.index(Ao[i]), C.index(Ao[(i + 1) % len(Ao)])
        pts = [P[C[(s + t) % L]] for t in range(((e - s) % L or L) + 1)]
        ax.plot(*zip(*pts), "orange", lw=6, alpha=.6)
    for v, p in P.items():
        ax.text(*p, v, ha="center", va="center", bbox=dict(boxstyle="circle", fc="white"))
    return P
