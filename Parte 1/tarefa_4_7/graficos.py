import time
import random
import numpy as np
import networkx as nx
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from hierholzer import hierholzer


def euler_aleatorio(n, m):
    # um ciclo por todos os vertices (garante conexao) + ciclos aleatorios ate ~m arestas
    E = [(i, i % n + 1) for i in range(1, n + 1)]
    while len(E) < m:
        k = min(random.randint(2, 6), m - len(E))
        if k < 2:
            k = 2
        pts = [random.randint(1, n) for _ in range(k)]
        for i in range(k):
            E.append((pts[i], pts[(i + 1) % k]))
    return E


def fig_circuito():
    n, E = 3, [(1, 2), (1, 2), (2, 3), (2, 3), (2, 2), (1, 3), (1, 3)]
    V, ids = hierholzer(n, E)
    passo = {e: k for k, e in enumerate(ids, 1)}
    G = nx.MultiDiGraph()
    G.add_nodes_from(range(1, n + 1))
    pos = nx.circular_layout(G)
    plt.figure()
    nx.draw_networkx_nodes(G, pos, node_color="#dddddd", node_size=700)
    nx.draw_networkx_labels(G, pos)
    vistas = {}
    for e, (u, v) in enumerate(E, 1):
        par = frozenset((u, v))
        k = vistas.get(par, 0)
        vistas[par] = k + 1
        rad = 0.25 * (k + 1) * (1 if k % 2 == 0 else -1) if u != v else 0.0
        nx.draw_networkx_edges(G, pos, edgelist=[(u, v)], arrows=True, arrowstyle="-", width=2.5,
                               connectionstyle=f"arc3,rad={rad}",
                               edge_color=[plt.cm.viridis(passo[e] / len(E))])
    plt.title("cor das arestas = ordem no circuito; ids na ordem: " + " ".join(map(str, ids)))
    plt.axis("off")
    plt.savefig("figuras/circuito.png", dpi=150, bbox_inches="tight")
    plt.close()


def fig_pilha():
    random.seed(3)
    n = 60
    E = euler_aleatorio(n, 400)
    traco = []
    hierholzer(n, E, traco=traco)
    plt.figure()
    plt.plot(traco, lw=1)
    plt.xlabel("iteracao do laco principal")
    plt.ylabel("tamanho da pilha S")
    plt.title(f"m = {len(E)}: a pilha sobe em excursoes e desce ao desempilhar")
    plt.savefig("figuras/pilha.png", dpi=150)
    plt.close()
    print(f"pilha: {len(traco) - 1} iteracoes para m = {len(E)} (2m+1 = {2 * len(E) + 1})")


def fig_tempo():
    random.seed(0)
    ms = [10**3, 3 * 10**3, 10**4, 3 * 10**4, 10**5, 3 * 10**5]
    ts = []
    for m in ms:
        n = max(2, m // 5)
        E = euler_aleatorio(n, m)
        t0 = time.perf_counter()
        hierholzer(n, E)
        ts.append(time.perf_counter() - t0)
    s, _ = np.polyfit(np.log(ms), np.log(ts), 1)
    print(f"tempo: inclinacao {s:.2f}")
    plt.figure()
    plt.loglog(ms, ts, "o-", label=f"inclinacao {s:.2f} (esperado 1)")
    plt.xlabel("m")
    plt.ylabel("tempo (s)")
    plt.legend()
    plt.savefig("figuras/tempo_hierholzer.png", dpi=150)
    plt.close()


if __name__ == "__main__":
    fig_circuito()
    fig_pilha()
    fig_tempo()
    print("figuras gravadas em figuras/")
