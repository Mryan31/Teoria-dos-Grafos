import time
import random
import numpy as np
import networkx as nx
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from edmonds_karp import edmonds_karp


def rede_aleatoria(n, m, seed):
    rng = random.Random(seed)
    arcos = []
    # um caminho 0 -> n-1 para garantir algum fluxo
    for v in range(n - 1):
        arcos.append((v, v + 1, rng.randint(1, 20)))
    while len(arcos) < m:
        u, v = rng.sample(range(n), 2)
        arcos.append((u, v, rng.randint(1, 20)))
    return arcos


def fig_rede():
    n, s, t = 6, 0, 5
    arcos = [(0, 1, 16), (0, 2, 13), (1, 2, 10), (2, 1, 4), (1, 3, 12), (3, 2, 9), (2, 4, 14),
             (4, 3, 7), (3, 5, 20), (4, 5, 4)]
    val, f, S, log = edmonds_karp(n, arcos, s, t)
    lista = [(u, v) for u, v, c in arcos]
    G = nx.DiGraph(lista)
    pos = {0: (0, 1), 1: (1, 2), 2: (1, 0), 3: (2, 2), 4: (2, 0), 5: (3, 1)}
    cor = ["red" if u in S and v not in S else "gray" for u, v, c in arcos]
    plt.figure(figsize=(8, 5))
    nx.draw_networkx_nodes(G, pos, node_color=["orange" if v in S else "lightblue" for v in G])
    nx.draw_networkx_labels(G, pos)
    nx.draw_networkx_edges(G, pos, edgelist=lista, edge_color=cor, connectionstyle="arc3,rad=0.1")
    rot = {(u, v): f"{f[k]}/{c}" for k, (u, v, c) in enumerate(arcos)}
    nx.draw_networkx_edge_labels(G, pos, rot, label_pos=0.3, font_size=8, connectionstyle="arc3,rad=0.1")
    plt.title(f"val = {val}   S = {sorted(S)}   c(d+(S)) = {sum(c for u, v, c in arcos if u in S and v not in S)}")
    plt.axis("off")
    plt.savefig("figuras/rede_fluxo.png", dpi=120)
    plt.close()


def fig_tempo():
    ns, ts = [20, 40, 80, 160, 320, 640], []
    for n in ns:
        arcos = rede_aleatoria(n, 4 * n, seed=n)
        t0 = time.perf_counter()
        edmonds_karp(n, arcos, 0, n - 1)
        ts.append(time.perf_counter() - t0)
    a, b = np.polyfit(np.log(ns), np.log(ts), 1)
    print(f"tempo: inclinacao {a:.2f}")
    plt.figure()
    plt.loglog(ns, ts, "o-", label=f"medido: inclinacao {a:.2f}")
    plt.loglog(ns, np.exp(b) * np.array(ns, dtype=float) ** 3, "--", label="referencia n^3")
    plt.xlabel("n (m = 4n)")
    plt.ylabel("tempo (s)")
    plt.legend()
    plt.savefig("figuras/tempo_loglog.png", dpi=120)
    plt.close()


def fig_distancias():
    arcos = rede_aleatoria(200, 800, seed=7)
    val, f, S, log = edmonds_karp(200, arcos, 0, 199)
    fig, (a1, a2) = plt.subplots(1, 2, figsize=(10, 3.5))
    a1.step(range(len(log)), [c for c, e in log], where="post")
    a1.set_xlabel("aumento")
    a1.set_ylabel("comprimento do caminho")
    a1.set_title("nunca decresce (Prop. 6.18)")
    a2.plot(np.cumsum([e for c, e in log]))
    a2.set_xlabel("aumento")
    a2.set_ylabel("valor acumulado")
    a2.set_title(f"valor final = {val}")
    plt.tight_layout()
    plt.savefig("figuras/distancias.png", dpi=120)
    plt.close()


if __name__ == "__main__":
    fig_rede()
    fig_tempo()
    fig_distancias()
    print("figuras gravadas em figuras/")
