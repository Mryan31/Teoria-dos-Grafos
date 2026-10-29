"""M6 (opcional) - desenho baricentrico de Tutte (Obs. 14.6)."""
import numpy as np


def tutte_positions(adj, face_externa):
    """borda = vertices da face externa num poligono regular (na ordem ciclica da face);
    cada vertice interior e o baricentro dos vizinhos: L_II P_I = -L_IB P_B (14.3)-(14.4)."""
    V = sorted(adj)
    idx = {v: i for i, v in enumerate(V)}
    n = len(V)
    L = np.zeros((n, n))
    for v in V:
        L[idx[v], idx[v]] = len(adj[v])
        for w in adj[v]:
            L[idx[v], idx[w]] = -1
    borda = list(face_externa)
    interior = [v for v in V if v not in set(borda)]
    P = np.zeros((n, 2))
    F = len(borda)
    for k, v in enumerate(borda):
        P[idx[v]] = (np.cos(2 * np.pi * k / F), np.sin(2 * np.pi * k / F))
    if interior:
        I = [idx[v] for v in interior]
        Bi = [idx[v] for v in borda]
        P[I] = np.linalg.solve(L[np.ix_(I, I)], -L[np.ix_(I, Bi)] @ P[Bi])
    return {v: P[idx[v]] for v in V}


def _cross(a, b, c):
    return (b[0] - a[0]) * (c[1] - a[1]) - (b[1] - a[1]) * (c[0] - a[0])


def _cruzam(p1, p2, p3, p4):
    d1, d2 = _cross(p3, p4, p1), _cross(p3, p4, p2)
    d3, d4 = _cross(p1, p2, p3), _cross(p1, p2, p4)
    return d1 * d2 < 0 and d3 * d4 < 0


def verify_tutte(adj, pos, faces, outer_idx):
    """(i) residuo do baricentro nos interiores; (ii) cruzamentos entre arestas nao incidentes;
    (iii) menor curva cross(p_i, p_i+1, p_i+2) nas faces internas (com o sinal da maioria); (iv) menor distancia."""
    externa = set(faces[outer_idx]) if outer_idx is not None else set()
    res = 0.0
    for v in adj:
        if v not in externa:
            bar = sum(pos[w] for w in adj[v]) / len(adj[v])
            res = max(res, float(np.max(np.abs(pos[v] - bar))))
    E = sorted((u, v) for u in adj for v in adj[u] if u < v)
    cruz = 0
    for i in range(len(E)):
        for j in range(i + 1, len(E)):
            a, b = E[i]
            c, d = E[j]
            if len({a, b, c, d}) == 4 and _cruzam(pos[a], pos[b], pos[c], pos[d]):
                cruz += 1
    curvas = []
    for j, f in enumerate(faces):
        if j == outer_idx:
            continue
        L = len(f)
        curvas.append([_cross(pos[f[t]], pos[f[(t + 1) % L]], pos[f[(t + 2) % L]]) for t in range(L)])
    sinal = 1 if sum(sum(c) > 0 for c in curvas) * 2 >= len(curvas) else -1
    min_turn = min((sinal * x for c in curvas for x in c), default=0.0)
    V = list(adj)
    min_dist = min((float(np.linalg.norm(pos[V[i]] - pos[V[j]]))
                    for i in range(len(V)) for j in range(i + 1, len(V))), default=0.0)
    return dict(barycentre=res, crossings=cruz, min_turn=min_turn, min_dist=min_dist)
