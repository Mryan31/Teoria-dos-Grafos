"""M3 - faces como listas ciclicas orientadas e o teste de intervalo (Lema 14.2).
Convencao: todas as faces no mesmo sentido, ou seja, cada dart (u, v) aparece em exatamente uma face."""


def k4_faces(a, b, c, d):
    return [(a, b, c), (a, c, d), (a, d, b), (b, d, c)]


def rotacionar(f, v):
    i = f.index(v)
    return tuple(f[i:]) + tuple(f[:i])


def arco(C, u, v):
    """Vertices de C de u ate v no sentido de C, extremos incluidos (u == v da a volta inteira)."""
    L = len(C)
    s = C.index(u)
    e = C.index(v)
    tam = (e - s) % L or L
    return [C[(s + t) % L] for t in range(tam + 1)]


def boundary_cycle(faces, z):
    """Ciclo C de H - z que limitava a face onde estava z (Obs. 14.1), ja orientado como as faces."""
    caminho = {}
    for f in faces:
        if z in f:
            g = rotacionar(f, z)          # (z, p0, ..., pk)
            caminho[g[1]] = list(g[1:])   # p0 -> [p0, ..., pk]
    ini = next(iter(caminho))
    C = []
    cur = ini
    while True:
        p = caminho[cur]
        C += p[:-1]
        cur = p[-1]
        if cur == ini:
            return C


def interval_test(C, A, B):
    """Lema 14.2: J e planar <=> B esta contido em algum arco P_i (extremos incluidos).
    Devolve (i, Ao) com Ao = A ordenado ao longo de C; i = None se falhar."""
    pos = {v: j for j, v in enumerate(C)}
    L = len(C)
    Ao = sorted(A, key=pos.get)   # A chega ordenado por rotulo, nao ao longo de C
    k = len(Ao)
    for i in range(k):
        s = pos[Ao[i]]
        vao = (pos[Ao[(i + 1) % k]] - s) % L
        if all((pos[b] - s) % L <= vao for b in B):
            return i, Ao
    return None, Ao


def insert_xy(faces, z, x, y, C, Ao, B, i):
    """A face de z e fatiada: x fica com os arcos P_j (j != i) e y entra no arco P_i."""
    novas = [f for f in faces if z not in f]
    for j in range(len(Ao)):
        Pj = arco(C, Ao[j], Ao[(j + 1) % len(Ao)])
        if j != i:
            novas.append(tuple(Pj) + (x,))
        else:
            b = sorted(B, key=Pj.index)   # b_1..b_t ao longo de P_i
            novas.append(tuple(Pj[:Pj.index(b[0]) + 1]) + (y, x))
            for u, w in zip(b, b[1:]):
                novas.append(tuple(Pj[Pj.index(u):Pj.index(w) + 1]) + (y,))
            novas.append(tuple(Pj[Pj.index(b[-1]):]) + (x, y))
    return novas


def check_embedding(adj, faces):
    """None se as faces formam um mergulho planar de adj; senao uma mensagem.
    (a) cada dart e aresta e aparece uma vez; (b) Euler (Teor. 12.15); (c) rotacao valida em cada vertice."""
    darts = {}
    for f in faces:
        for u, v in zip(f, f[1:] + f[:1]):
            if v not in adj.get(u, ()):
                return f"dart {u}->{v} nao e aresta"
            if (u, v) in darts:
                return f"dart {u}->{v} aparece duas vezes"
            darts[(u, v)] = f
    m = sum(len(adj[v]) for v in adj) // 2
    if len(darts) != 2 * m:
        return f"{len(darts)} darts, esperado {2 * m}"
    n = len(adj)
    if n - m + len(faces) != 2:
        return f"Euler falhou: n - m + f = {n - m + len(faces)}"
    # chega em v por (u, v) e a mesma face sai por (v, w): sucessor de u em torno de v e w
    suc = {v: {} for v in adj}
    for f in faces:
        L = len(f)
        for i in range(L):
            u, v, w = f[i - 1], f[i], f[(i + 1) % L]
            suc[v][u] = w
    for v in adj:
        if set(suc[v]) != adj[v]:
            return f"rotacao incompleta em {v}"
        u0 = next(iter(adj[v]))
        u, passos = u0, 0
        while True:
            u = suc[v][u]
            passos += 1
            if u == u0:
                break
        if passos != len(adj[v]):
            return f"rotacao em {v} nao e um ciclo unico"
    return None


def reconstruct(trace, k4, log=None):
    """Desfaz as contracoes de tras para frente, testando o intervalo em cada passo.
    Devolve (faces, None) se planar, ou (None, (k, C, Ao)) no passo em que falhou."""
    faces = k4_faces(*sorted(k4))
    for k in range(len(trace) - 1, -1, -1):
        x, y, A, B = trace[k]
        C = boundary_cycle(faces, x)   # o vertice contraido levou o rotulo z = x
        i, Ao = interval_test(C, A, B)
        if log is not None:
            log.append((k, x, y, C, Ao, B, i))
        if i is None:
            return None, (k, C, Ao)
        faces = insert_xy(faces, x, x, y, C, Ao, B, i)
        if log is not None:
            log[-1] = log[-1] + (len(faces),)
    return faces, None
