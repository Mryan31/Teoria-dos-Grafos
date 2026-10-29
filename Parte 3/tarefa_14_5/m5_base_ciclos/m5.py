"""M5 - base esparsa do espaco de ciclos (Mac Lane, Aula 13 P4-P5).
Vetores de F2^m guardados como inteiros: bit j = j-esima aresta de edges_of; soma = XOR."""
from collections import deque
from common.graphs import edges_of


def _eid(adj):
    return {e: j for j, e in enumerate(edges_of(adj))}


def _vetor(ciclo, eid):
    v = 0
    for a, b in zip(ciclo, ciclo[1:] + ciclo[:1]):
        v ^= 1 << eid[(min(a, b), max(a, b))]
    return v


def face_basis(adj, faces, outer=0):
    """Fronteiras de todas as faces menos a externa (P4(a)-(b) da Aula 13)."""
    eid = _eid(adj)
    vecs = [_vetor(list(f), eid) for j, f in enumerate(faces) if j != outer]
    return vecs, eid


def rank_f2(vecs):
    pivo = {}
    for v in vecs:
        while v:
            h = v.bit_length() - 1
            if h in pivo:
                v ^= pivo[h]
            else:
                pivo[h] = v
                break
    return len(pivo)


def verify_basis(adj, vecs, eid):
    """Aceita <=> (i) todo vetor tem grau par em todo vertice; (ii) #vetores = posto = m - n + 1;
    (iii) cada aresta aparece em no maximo 2 vetores."""
    arestas = sorted(eid, key=eid.get)
    even = True
    for v in vecs:
        grau = {}
        for e, j in eid.items():
            if v >> j & 1:
                for w in e:
                    grau[w] = grau.get(w, 0) + 1
        if any(g % 2 for g in grau.values()):
            even = False
    uso = [sum(v >> j & 1 for v in vecs) for j in range(len(arestas))]
    n, m = len(adj), len(arestas)
    r = dict(even=even, rank=rank_f2(vecs), expected=m - n + 1, count=len(vecs),
             maxuse=max(uso) if uso else 0)
    r["ok"] = r["even"] and r["count"] == r["rank"] == r["expected"] and r["maxuse"] <= 2
    return r


def fundamental_basis(adj, root):
    """Ciclos fundamentais de uma arvore BFS (base, mas em geral nao esparsa)."""
    eid = _eid(adj)
    pai = {root: None}
    fila = deque([root])
    while fila:
        u = fila.popleft()
        for w in sorted(adj[u]):
            if w not in pai:
                pai[w] = u
                fila.append(w)

    def ate_raiz(v):
        out = [v]
        while pai[out[-1]] is not None:
            out.append(pai[out[-1]])
        return out
    vecs = []
    for u, w in edges_of(adj):
        if pai.get(w) == u or pai.get(u) == w:
            continue
        pu, pw = ate_raiz(u), ate_raiz(w)
        comum = set(pu) & set(pw)
        lado_u = [v for v in pu if v not in comum] + [next(v for v in pu if v in comum)]
        lado_w = [v for v in pw if v not in comum]
        vecs.append(_vetor(lado_u + lado_w[::-1], eid))
    return vecs, eid


def tem_base_esparsa(adj):
    """Forca bruta (m <= 15): existe base do espaco de ciclos com cada aresta em <= 2 vetores? (P5(d))"""
    eid = _eid(adj)
    m = len(eid)
    dim = m - len(adj) + 1
    pares = {}
    for e, j in eid.items():
        for w in e:
            pares.setdefault(w, []).append(j)

    def par(mask):
        return all(sum(mask >> j & 1 for j in js) % 2 == 0 for js in pares.values())
    ciclos = [mask for mask in range(1, 1 << m) if par(mask)]
    uso = [0] * m

    def rec(ini, escolhidos):
        if len(escolhidos) == dim:
            return True
        for idx in range(ini, len(ciclos)):
            c = ciclos[idx]
            bits = [j for j in range(m) if c >> j & 1]
            if any(uso[j] >= 2 for j in bits):
                continue
            if rank_f2(escolhidos + [c]) < len(escolhidos) + 1:
                continue
            for j in bits:
                uso[j] += 1
            if rec(idx + 1, escolhidos + [c]):
                return True
            for j in bits:
                uso[j] -= 1
        return False
    return rec(0, [])
