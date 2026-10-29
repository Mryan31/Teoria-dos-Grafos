import random
import networkx as nx
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from dilworth import dilworth

elementos = "a b c d e f".split()
relacoes = [("a", "c"), ("b", "d"), ("c", "e"), ("c", "f"), ("d", "e"), ("d", "f")]


def fig_hasse():
    plt.figure(figsize=(6, 4))
    cadeias, T, M, K = dilworth(elementos, relacoes)
    D = nx.DiGraph(relacoes)
    D.add_nodes_from(elementos)
    H = nx.transitive_reduction(D)   # diagrama de Hasse (so para desenhar)
    nivel = {}
    for x in nx.topological_sort(H):
        nivel[x] = 1 + max((nivel[p] for p in H.predecessors(x)), default=-1)
    colunas = {}
    pos = {}
    for x in elementos:
        k = colunas.get(nivel[x], 0)
        colunas[nivel[x]] = k + 1
        pos[x] = (k, nivel[x])
    cor = {x: plt.cm.tab10(i) for i, c in enumerate(cadeias) for x in c}
    nx.draw_networkx_edges(H, pos, edge_color="lightgray", arrows=False)
    for c in cadeias:
        nx.draw_networkx_edges(H, pos, edgelist=list(zip(c, c[1:])), width=4, edge_color=[cor[c[0]]], arrows=False)
    nx.draw_networkx_nodes(H, pos, nodelist=list(H), node_color=[cor[x] for x in H],
                           edgecolors=["black" if x in T else "none" for x in H], linewidths=3)
    nx.draw_networkx_labels(H, pos)
    plt.title(f"{len(cadeias)} cadeias (cores); anticadeia T = {T} (borda preta)")
    plt.axis("off")
    plt.savefig("figuras/hasse.png", dpi=120)
    plt.close()


def fig_BP():
    plt.subplots(figsize=(6, 4))
    cadeias, T, M, K = dilworth(elementos, relacoes)
    n = len(elementos)
    G = nx.Graph()
    fecho = nx.transitive_closure(nx.DiGraph(relacoes))
    G.add_edges_from((x + "-", y + "+") for x, y in fecho.edges())
    G.add_nodes_from([x + "-" for x in elementos] + [x + "+" for x in elementos])
    pos = {x + "-": (0, -i) for i, x in enumerate(elementos)}
    pos.update({x + "+": (1, -i) for i, x in enumerate(elementos)})
    Kn = {x + s for s, x in K}
    nx.draw(G, pos, with_labels=True, node_color=["tomato" if v in Kn else "lightblue" for v in G],
            edge_color="lightgray", node_size=600)
    nx.draw_networkx_edges(G, pos, edgelist=[(x + "-", y + "+") for x, y in M], width=4, edge_color="royalblue")
    plt.title(f"|M| = {len(M)} (azul), |K| = {len(K)} (vermelho), n - |M| = {n - len(M)} cadeias")
    plt.savefig("figuras/BP.png", dpi=120)
    plt.close()


def fig_largura():
    rng = random.Random(2)
    xs, ys = [], []
    for _ in range(80):
        n = rng.randint(3, 11)
        el = [str(i) for i in range(n)]
        rel = [(el[i], el[j]) for i in range(n) for j in range(i + 1, n) if rng.random() < 0.3]
        cadeias, T, M, K = dilworth(el, rel)
        D = nx.DiGraph()
        D.add_nodes_from(el)
        D.add_edges_from(rel)
        w = max(len(a) for a in nx.algorithms.dag.antichains(D))
        xs.append(w + rng.uniform(-.12, .12))
        ys.append(len(cadeias) + rng.uniform(-.12, .12))
    plt.figure()
    plt.scatter(xs, ys, s=14, alpha=.6)
    m = max(max(xs), max(ys))
    plt.plot([0, m], [0, m], "r--")
    plt.xlabel("largura w(P) (forca bruta, networkx)")
    plt.ylabel("numero de cadeias devolvido")
    plt.title("Dilworth: todos os pontos na diagonal")
    plt.savefig("figuras/largura.png", dpi=120)
    plt.close()


if __name__ == "__main__":
    fig_hasse()
    fig_BP()
    fig_largura()
    print("figuras gravadas em figuras/")
