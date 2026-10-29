import random
import networkx as nx
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from imersao_arvore import imersao, ordem_de_crescimento

petersen = [(1, 2), (2, 3), (3, 4), (4, 5), (5, 1), (1, 6), (2, 7), (3, 8), (4, 9), (5, 10),
            (6, 8), (8, 10), (10, 7), (7, 9), (9, 6)]


def grafo_com_grau_minimo(n, k):
    E = [(a, b) for a in range(1, n + 1) for b in range(a + 1, n + 1)]
    random.shuffle(E)
    grau = [n - 1] * (n + 1)
    fica = []
    for a, b in E:
        if grau[a] > k and grau[b] > k and random.random() < 0.5:
            grau[a] -= 1
            grau[b] -= 1
        else:
            fica.append((a, b))
    return fica


def fig_imersao():
    t, TE, r, n, GE, x = 4, [(1, 2), (2, 3), (3, 4)], 1, 10, petersen, 6
    phi, ordem, pai, livres = imersao(t, TE, r, n, GE, x)
    G = nx.Graph()
    G.add_nodes_from(range(1, n + 1))
    G.add_edges_from(GE)
    imagem = {phi[u]: u for u in phi}
    rot = {v: (f"{v}\n(u={imagem[v]})" if v in imagem else str(v)) for v in G}
    cor = ["#f6c85f" if v == x else "#9fd3a8" if v in imagem else "#dddddd" for v in G]
    usadas = {frozenset((phi[a], phi[b])) for a, b in TE}
    ec = ["#d62728" if frozenset(e) in usadas else "#bbbbbb" for e in G.edges]
    lw = [3.5 if frozenset(e) in usadas else 1 for e in G.edges]
    plt.figure()
    nx.draw(G, nx.kamada_kawai_layout(G), labels=rot, font_size=7, node_color=cor, edge_color=ec,
            width=lw, node_size=650)
    plt.title(f"phi(r)=x={x}; copia de T em vermelho")
    plt.savefig("figuras/imersao.png", dpi=150, bbox_inches="tight")
    plt.close()


def fig_folga():
    t = 9
    plt.figure()
    for sem in range(5):
        random.seed(sem)
        n = 12
        # arvore aleatoria com t vertices
        TE = [(random.randint(1, i - 1), i) for i in range(2, t + 1)]
        GE = grafo_com_grau_minimo(n, t - 1)
        _, ordem, pai, livres = imersao(t, TE, 1, n, GE, random.randint(1, n))
        plt.plot(range(2, t + 1), livres, "o-", alpha=.7)
    plt.plot(range(2, t + 1), [t - i + 1 for i in range(2, t + 1)], "k--", lw=2, label="cota da prova: t - i + 1")
    plt.xlabel("passo i (vertice u_i)")
    plt.ylabel("vizinhos livres de phi(pai(u_i))")
    plt.legend()
    plt.savefig("figuras/folga.png", dpi=150)
    plt.close()


def fig_ordem():
    t, TE, r = 7, [(1, 2), (1, 3), (2, 4), (2, 5), (3, 6), (3, 7)], 4
    ordem, pai = ordem_de_crescimento(t, TE, r)
    pos_i = {u: i for i, u in enumerate(ordem, 1)}
    T = nx.Graph(TE)
    rot = {u: f"u{u}\n#{pos_i[u]}" for u in T}
    plt.figure()
    nx.draw(T, nx.kamada_kawai_layout(T), labels=rot, font_size=8, node_size=800,
            node_color=["#f6c85f" if u == r else "#9fd3a8" for u in T])
    plt.title("ordem de crescimento (#) = remocao de folhas invertida; amarelo = raiz")
    plt.savefig("figuras/ordem.png", dpi=150, bbox_inches="tight")
    plt.close()


if __name__ == "__main__":
    fig_imersao()
    fig_folga()
    fig_ordem()
    print("figuras gravadas em figuras/")
