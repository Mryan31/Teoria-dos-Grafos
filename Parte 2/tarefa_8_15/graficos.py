import time
import random
import numpy as np
import networkx as nx
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from edmonds import edmonds, busca, aumente


def fig_blossom():
    n, r = 8, 0
    E = [(0, 1), (1, 2), (2, 3), (3, 4), (4, 5), (5, 6), (6, 2), (6, 7)]
    mate0 = [-1, 2, 1, 4, 3, 6, 5, -1]
    adj = [[] for _ in range(n)]
    for u, v in E:
        adj[u].append(v)
        adj[v].append(u)
    adj = [sorted(l) for l in adj]
    pos = {0: (0, 0), 1: (1, 0), 2: (2, 0), 3: (2.8, 1), 4: (4, .6), 5: (4, -.6), 6: (2.8, -1), 7: (2.8, -2.2)}

    z, parent, base, tipo = busca(r, adj, mate0)
    mate1 = aumente(z, parent, list(mate0))

    def arest(mt):
        return {frozenset((u, mt[u])) for u in range(n) if mt[u] != -1}
    rec = [tuple(e) for e in arest(mate0) ^ arest(mate1)]  # diferenca simetrica = caminho
    G = nx.Graph(E)
    fig, axs = plt.subplots(1, 2, figsize=(10, 4))
    bl = {v for v in range(n) if base[v] != v or base.count(v) > 1}
    nx.draw(G, pos, ax=axs[0], with_labels=True, node_color=["gold" if v in bl else "lightblue" for v in G],
            edge_color="gray")
    nx.draw_networkx_edges(G, pos, edgelist=[tuple(e) for e in arest(mate0)], width=4,
                           edge_color="royalblue", ax=axs[0])
    nx.draw_networkx_edges(G, pos, edgelist=rec, width=2, style="dashed", edge_color="red", ax=axs[0])
    axs[0].set_title("G: M (azul), blossom (dourado), caminho (vermelho)")
    H = nx.Graph([(base[u], base[v]) for u, v in E if base[u] != base[v]])
    pH = {b: tuple(sum(pos[v][i] for v in range(n) if base[v] == b) / base.count(b) for i in (0, 1)) for b in H}
    nx.draw(H, pH, ax=axs[1], with_labels=True, node_color="lightblue", edge_color="gray")
    nx.draw_networkx_edges(H, pH, edgelist=[(base[u], base[v]) for u, v in map(tuple, arest(mate0))
                                            if base[u] != base[v]], width=4, edge_color="royalblue", ax=axs[1])
    axs[1].set_title("contraido: o blossom virou um vertice (rotulo = base)")
    plt.savefig("figuras/blossom.png", dpi=120)
    plt.close()


def fig_petersen():
    plt.subplots(figsize=(6, 4))
    G = nx.petersen_graph()
    n = 10
    adj = [sorted(G[v]) for v in range(n)]
    mate = edmonds(n, adj)
    M = [(u, mate[u]) for u in range(n) if mate[u] > u]
    pos = nx.shell_layout(G, [[0, 1, 2, 3, 4], [5, 6, 7, 8, 9]])
    nx.draw(G, pos, with_labels=True, node_color="lightblue", edge_color="lightgray")
    nx.draw_networkx_edges(G, pos, edgelist=M, width=4, edge_color="royalblue")
    plt.title(f"Petersen: |M| = {len(M)} (esperado 5, perfeito)")
    plt.savefig("figuras/petersen.png", dpi=120)
    plt.close()


def fig_tempo():
    ns, ts = [25, 50, 100, 200, 400], []
    for n in ns:
        rng = random.Random(n)
        S = set()
        while len(S) < 3 * n:
            u, v = rng.sample(range(n), 2)
            S.add((min(u, v), max(u, v)))
        adj = [[] for _ in range(n)]
        for u, v in S:
            adj[u].append(v)
            adj[v].append(u)
        adj = [sorted(l) for l in adj]
        t0 = time.perf_counter()
        edmonds(n, adj)
        ts.append(time.perf_counter() - t0)
    a, b = np.polyfit(np.log(ns), np.log(ts), 1)
    print(f"tempo: inclinacao {a:.2f}")
    plt.figure()
    plt.loglog(ns, ts, "o-", label=f"medido: inclinacao {a:.2f}")
    plt.loglog(ns, np.exp(b) * np.array(ns, dtype=float) ** 3, "--", label="referencia n^3")
    plt.xlabel("n (m = 3n)")
    plt.ylabel("tempo (s)")
    plt.legend()
    plt.savefig("figuras/tempo_loglog.png", dpi=120)
    plt.close()


if __name__ == "__main__":
    fig_blossom()
    fig_petersen()
    fig_tempo()
    print("figuras gravadas em figuras/")
