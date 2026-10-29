import math
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt


def desenha(ax, E, cor, pos, dest=(), tit=""):
    # aresta sem cor sai pontilhada cinza; aresta em dest sai grossa; cada aresta leva o numero da cor
    for e, (u, v) in enumerate(E):
        ax.plot(*zip(pos[u], pos[v]), color=plt.cm.tab10(cor[e] - 1) if cor[e] else "gray",
                ls="-" if cor[e] else ":", lw=5 if e in dest else 2, zorder=1)
        ax.text(*[(a + b) / 2 for a, b in zip(pos[u], pos[v])], cor[e] or "?", fontsize=8,
                ha="center", va="center", bbox=dict(fc="w", ec="none", pad=.5), zorder=3)
    for v, p in enumerate(pos):
        ax.text(*p, v, ha="center", va="center", fontsize=9, bbox=dict(boxstyle="circle", fc="w"), zorder=4)
    ax.set_title(tit, fontsize=9)
    ax.axis("off")
    ax.set_aspect("equal")
    ax.margins(.15)


def circ(n, r=1):
    return [(r * math.cos(math.pi / 2 + 2 * math.pi * i / n), r * math.sin(math.pi / 2 + 2 * math.pi * i / n))
            for i in range(n)]
