import time
import random
import numpy as np
import networkx as nx
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from bipartido import busca, aumenta, emparelhamento_maximo


def monta(nA, texto):
    adj = [[] for _ in range(nA)]
    for e in texto.split():
        a, b = e.split("-")
        adj[int(a[1:])].append(int(b[1:]))
    return [sorted(l) for l in adj]


def posicoes(nA, nB):
    pos = {("A", a): (0, -a) for a in range(nA)}
    pos.update({("B", b): (1, -b) for b in range(nB)})
    return pos


def fig_aumento():
    nA, nB = 4, 4
    adj = monta(nA, "a0-b0 a0-b1 a1-b0 a2-b1 a2-b2 a3-b2 a3-b3")

    def desenha(ax, mateA, cam, titulo):
        G = nx.Graph([(("A", a), ("B", b)) for a in range(nA) for b in adj[a]])
        pos = posicoes(nA, nB)
        M = [(("A", a), ("B", mateA[a])) for a in range(nA) if mateA[a] != -1]
        P = []
        if cam:
            for i, (x, y) in enumerate(zip(cam, cam[1:])):
                P.append((("A", x), ("B", y)) if i % 2 == 0 else (("A", y), ("B", x)))
        nx.draw(G, pos, ax=ax, labels={v: v[0].lower() + str(v[1]) for v in G}, node_size=500,
                node_color="lightblue", edge_color="lightgray")
        nx.draw_networkx_edges(G, pos, edgelist=M, width=4, edge_color="royalblue", ax=ax)
        nx.draw_networkx_edges(G, pos, edgelist=P, width=2, edge_color="red", style="dashed", ax=ax)
        ax.set_title(titulo)

    mA, mB, hist = [-1] * nA, [-1] * nB, []
    while True:
        r = busca(nA, nB, adj, mA, mB)
        if r[0] is None:
            break
        hist.append((list(mA), r[0]))
        aumenta(r[0], mA, mB)
    fig, axs = plt.subplots(1, 2, figsize=(9, 4))
    desenha(axs[0], *hist[-1], "antes: M (azul), caminho (vermelho)")
    desenha(axs[1], mA, None, "depois: |M| + 1")
    plt.savefig("figuras/aumento.png", dpi=120)
    plt.close()


def fig_certificado():
    nA, nB = 5, 5
    adj = monta(nA, "a0-b0 a0-b1 a1-b0 a1-b1 a2-b0 a2-b1 a3-b2 a4-b2 a4-b3")
    plt.subplots(figsize=(6, 4))
    mA, mB, RA, RB, K = emparelhamento_maximo(nA, nB, adj)
    G = nx.Graph([(("A", a), ("B", b)) for a in range(nA) for b in adj[a]])
    G.add_nodes_from(("B", b) for b in range(nB))
    pos = posicoes(nA, nB)
    R = {("A", a) for a in RA} | {("B", b) for b in RB}
    M = [(("A", a), ("B", mA[a])) for a in range(nA) if mA[a] != -1]
    nx.draw(G, pos, labels={v: v[0].lower() + str(v[1]) for v in G}, node_size=500, edge_color="lightgray",
            node_color=["tomato" if v in K else "lightblue" for v in G],
            edgecolors=["black" if v in R else "none" for v in G], linewidths=2)
    nx.draw_networkx_edges(G, pos, edgelist=M, width=4, edge_color="royalblue")
    plt.title(f"|M| = {len(M)} (azul)   |K| = {len(K)} (vermelho)   borda preta = RA u RB")
    plt.savefig("figuras/certificado.png", dpi=120)
    plt.close()


def fig_tempo():
    ns, ts = [100, 200, 400, 800, 1600, 3200], []
    for n in ns:
        rng = random.Random(n)
        adj = [sorted(rng.sample(range(n), 4)) for _ in range(n)]
        t0 = time.perf_counter()
        emparelhamento_maximo(n, n, adj)
        ts.append(time.perf_counter() - t0)
    a, b = np.polyfit(np.log(ns), np.log(ts), 1)
    print(f"tempo: inclinacao {a:.2f}")
    plt.figure()
    plt.loglog(ns, ts, "o-", label=f"medido: inclinacao {a:.2f}")
    plt.loglog(ns, np.exp(b) * np.array(ns, dtype=float) ** 2, "--", label="referencia n^2")
    plt.xlabel("n = |A| = |B| (grau 4 em A)")
    plt.ylabel("tempo (s)")
    plt.legend()
    plt.savefig("figuras/tempo_loglog.png", dpi=120)
    plt.close()


if __name__ == "__main__":
    fig_aumento()
    fig_certificado()
    fig_tempo()
    print("figuras gravadas em figuras/")
