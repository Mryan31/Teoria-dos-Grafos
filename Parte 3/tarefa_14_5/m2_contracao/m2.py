"""M2 - sequencia de contracoes ate o K4, registrando (x, y, N(x), N(y))."""
from common.graphs import copy


def contract(adj, x, y):
    """G/xy: y some, x herda os vizinhos de y (lacos e paralelas descartados)."""
    H = copy(adj)
    for w in H.pop(y):
        H[w].discard(y)
        if w != x:
            H[w].add(x)
            H[x].add(w)
    H[x].discard(x)
    return H


def contraction_trace(adj, escolher=None):
    """Teor. 11.12/11.14: sempre existe aresta contraivel, entao chega no K4.
    trace[k] = (x, y, A, B) com A = N_J(x) - {y}, B = N_J(y) - {x} (14.1), J = grafo antes."""
    if escolher is None:
        from m1_conexidade.m1 import find_contractible_edge
        escolher = find_contractible_edge
    trace = []
    J = copy(adj)
    while len(J) > 4:
        x, y = escolher(J)
        trace.append((x, y, sorted(J[x] - {y}), sorted(J[y] - {x})))
        J = contract(J, x, y)
    return trace, J


def uncontract(H, passo):
    """Desfaz um passo no grafo (so para teste): x ligado a A + {y}, y ligado a B + {x}."""
    x, y, A, B = passo
    J = copy(H)
    for w in J[x]:
        J[w].discard(x)
    J[x] = set(A) | {y}
    J[y] = set(B) | {x}
    for w in A:
        J[w].add(x)
    for w in B:
        J[w].add(y)
    return J


def branch_sets(trace, k, V):
    """Vertices de G representados por cada vertice de J_k (depois das k primeiras contracoes)."""
    S = {v: {v} for v in V}
    for x, y, _, _ in trace[:k]:
        S[x] |= S.pop(y)
    return S
