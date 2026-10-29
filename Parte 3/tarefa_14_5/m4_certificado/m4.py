"""M4 - certificado de nao planaridade (passo de Kuratowski-Wagner da prova do Teor. 13.12).
Quando o teste de intervalo falha em J = J_k, J tem um TK5 ou TK3,3 e J e menor de G."""
from itertools import combinations
from common.graphs import copy, edges_of


def _arco(C, u, v, sentido=1):
    # vertices de C de u ate v andando no sentido dado (1 = sentido de C, -1 = contrario)
    L = len(C)
    pos = {w: j for j, w in enumerate(C)}
    out = [u]
    j = pos[u]
    while C[j] != v:
        j = (j + sentido) % L
        out.append(C[j])
    return out


def _interior(C, u, v):
    return _arco(C, u, v)[1:-1]


def obstruction(C, x, y, A, B, Ao):
    """Devolve tk = dict(kind, classes, paths) com um TK5/TK3,3 dentro de J (ciclo C + x ligado a A
    + y ligado a B + xy). paths[(u, w)] = [u, ..., w]."""
    k = len(Ao)
    fora = [b for b in B if b not in A]
    if fora:
        # caso (a): b fica no interior de um unico P_i; como o teste falhou, algum b2 de B esta fora de P_i
        b = fora[0]
        i = next(j for j in range(k) if b in _interior(C, Ao[j], Ao[(j + 1) % k]))
        ai, ai1 = Ao[i], Ao[(i + 1) % k]
        Pi = _arco(C, ai, ai1)
        b2 = next(v for v in B if v not in Pi)
        paths = {(x, y): [x, y], (x, ai): [x, ai], (x, ai1): [x, ai1],
                 (b, y): [b, y], (b2, y): [b2, y],
                 (b, ai): _arco(C, b, ai, -1), (b, ai1): _arco(C, b, ai1, 1),
                 (b2, ai): _arco(C, b2, ai, 1), (b2, ai1): _arco(C, b2, ai1, -1)}
        return dict(kind="K33", classes=({x, b, b2}, {y, ai, ai1}), paths=paths, caso="a")
    if len(B) == 2:
        # caso (b): B = {b, b'} dentro de A mas nao consecutivos em Ao
        b, b2 = sorted(B, key=C.index)
        a = next(v for v in _interior(C, b, b2) if v in A)
        a2 = next(v for v in _interior(C, b2, b) if v in A)
        paths = {(x, y): [x, y], (x, a): [x, a], (x, a2): [x, a2],
                 (b, y): [b, y], (b2, y): [b2, y],
                 (b, a): _arco(C, b, a, 1), (b2, a): _arco(C, b2, a, -1),
                 (b2, a2): _arco(C, b2, a2, 1), (b, a2): _arco(C, b, a2, -1)}
        return dict(kind="K33", classes=({x, b, b2}, {y, a, a2}), paths=paths, caso="b")
    # caso (c): B dentro de A com |B| >= 3 -> TK5
    p, q, r = sorted(B, key=C.index)[:3]
    paths = {(x, y): [x, y]}
    for v in (p, q, r):
        paths[(x, v)] = [x, v]
        paths[(y, v)] = [y, v]
    paths[(p, q)] = _arco(C, p, q)
    paths[(q, r)] = _arco(C, q, r)
    paths[(r, p)] = _arco(C, r, p)
    return dict(kind="K5", classes=({x, y, p, q, r},), paths=paths, caso="c")


def verifica_tk(J, tk):
    """Cada caminho existe em J e os interiores sao disjuntos entre si e dos vertices de ramificacao."""
    ram = set().union(*tk["classes"])
    usados = set()
    for (u, w), p in tk["paths"].items():
        if p[0] != u or p[-1] != w:
            return f"caminho {u}-{w} com extremos errados"
        for a, b in zip(p, p[1:]):
            if b not in J[a]:
                return f"aresta {a}-{b} nao existe"
        for v in p[1:-1]:
            if v in ram or v in usados:
                return f"interior repetido em {v}"
            usados.add(v)
    return None


def model_from_tk(tk):
    # cada interior e absorvido pelo primeiro extremo do seu caminho
    S = {v: {v} for c in tk["classes"] for v in c}
    for (u, w), p in tk["paths"].items():
        S[u] |= set(p[1:-1])
    return S


def lift_model(S_J, conjuntos_J):
    # B_v = uniao dos conjuntos de G representados pelos vertices de S[v]
    return {v: set().union(*(conjuntos_J[u] for u in S)) for v, S in S_J.items()}


def _conexo(adj, S):
    S = set(S)
    ini = next(iter(S))
    visto = {ini}
    pilha = [ini]
    while pilha:
        u = pilha.pop()
        for w in adj[u]:
            if w in S and w not in visto:
                visto.add(w)
                pilha.append(w)
    return visto == S


def _ligados(adj, S, T):
    return any(w in T for u in S for w in adj[u])


def verify_minor(adj, model, kind):
    """Conferidor independente (Def. 13.3): None se o modelo e de K5 / K3,3 em G; senao mensagem."""
    conj = [set(s) for s in model.values()]
    precisa = 5 if kind == "K5" else 6
    if len(conj) != precisa:
        return f"{len(conj)} conjuntos, esperado {precisa}"
    for s in conj:
        if not s:
            return "conjunto vazio"
        if not s <= set(adj):
            return "vertice fora de G"
        if not _conexo(adj, s):
            return f"conjunto desconexo {sorted(s)}"
    for s, t in combinations(conj, 2):
        if s & t:
            return "conjuntos nao disjuntos"
    if kind == "K5":
        for s, t in combinations(conj, 2):
            if not _ligados(adj, s, t):
                return "falta aresta entre dois conjuntos"
        return None
    for lado in combinations(range(6), 3):
        outro = [j for j in range(6) if j not in lado]
        if all(_ligados(adj, conj[a], conj[b]) for a in lado for b in outro):
            return None
    return "nenhuma divisao 3+3 tem todas as arestas"


def _divisao_33(adj, model):
    nomes = list(model)
    for lado in combinations(nomes, 3):
        outro = [v for v in nomes if v not in lado]
        if all(_ligados(adj, model[a], model[b]) for a in lado for b in outro):
            return set(lado), set(outro)


def certificate_ops(adj, model, kind):
    """Sequencia de remocoes e contracoes que leva G a K5 ou K3,3. Devolve (ops, grafo final).
    Os rotulos nas operacoes sao os rotulos vivos (ao contrair (a, b), b vira a)."""
    H = copy(adj)
    ops = []
    todos = set().union(*model.values())
    for v in sorted(H):
        if v not in todos:
            for w in H.pop(v):
                H[w].discard(v)
            ops.append(("del_vertex", v))
    raizes = {}
    for nome, S in model.items():
        r = min(S)
        raizes[nome] = r
        # arvore geradora por BFS dentro de S
        pai = {r: None}
        ordem = [r]
        for u in ordem:
            for w in sorted(H[u]):
                if w in S and w not in pai:
                    pai[w] = u
                    ordem.append(w)
        arv = {frozenset((w, p)) for w, p in pai.items() if p is not None}
        for u, w in edges_of({v: H[v] for v in S}):
            if w in S and frozenset((u, w)) not in arv:
                H[u].discard(w)
                H[w].discard(u)
                ops.append(("del_edge", u, w))
        for w in ordem[1:]:   # pais ja foram absorvidos por r
            for z in H.pop(w):
                H[z].discard(w)
                if z != r:
                    H[z].add(r)
                    H[r].add(z)
            H[r].discard(r)
            ops.append(("contract", r, w))
    if kind == "K33":
        lado, outro = _divisao_33(adj, model)
        for a, b in combinations(list(lado), 2):
            ra, rb = raizes[a], raizes[b]
            if rb in H[ra]:
                H[ra].discard(rb)
                H[rb].discard(ra)
                ops.append(("del_edge", ra, rb))
        for a, b in combinations(list(outro), 2):
            ra, rb = raizes[a], raizes[b]
            if rb in H[ra]:
                H[ra].discard(rb)
                H[rb].discard(ra)
                ops.append(("del_edge", ra, rb))
    return ops, H
