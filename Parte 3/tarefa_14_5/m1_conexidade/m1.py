"""M1 - 3-conexidade e aresta contraivel."""
from common.graphs import edges_of


def conn_sem(adj, S):
    """G - S e conexo? (BFS ignorando S; o grafo vazio conta como conexo)"""
    resto = [v for v in adj if v not in S]
    if not resto:
        return True
    visto = {resto[0]}
    fila = [resto[0]]
    while fila:
        u = fila.pop()
        for w in adj[u]:
            if w not in S and w not in visto:
                visto.add(w)
                fila.append(w)
    return len(visto) == len(resto)


def find_separator(adj):
    """Devolve um separador com <= 2 vertices (lista ordenada) ou None.
    Ordem: vazio, depois vertices sozinhos, depois pares lexicograficos."""
    V = sorted(adj)
    if not conn_sem(adj, set()):
        return []
    for v in V:
        if not conn_sem(adj, {v}):
            return [v]
    for i, u in enumerate(V):
        for w in V[i + 1:]:
            if len(V) > 3 and not conn_sem(adj, {u, w}):
                return [u, w]
    return None


def is_3connected(adj):
    # Def. 11.9: |V| >= 4 e G - S conexo para todo S com |S| <= 2 (Prop. 11.10 da delta >= 3)
    return len(adj) >= 4 and find_separator(adj) is None


def is_contractible(adj, x, y):
    # Lema 11.11: com |V| >= 5, G/xy e 3-conexo <=> nenhum {x, y, z} separa G
    assert len(adj) >= 5
    return all(conn_sem(adj, {x, y, z}) for z in adj if z not in (x, y))


def contractible_edges(adj):
    return [(x, y) for x, y in edges_of(adj) if is_contractible(adj, x, y)]


def find_contractible_edge(adj):
    """Primeira aresta contraivel na ordem lexicografica (Teor. 11.12 garante que existe)."""
    for x, y in edges_of(adj):
        if is_contractible(adj, x, y):
            return x, y
    raise ValueError("nenhuma aresta contraivel: o grafo nao e 3-conexo?")
