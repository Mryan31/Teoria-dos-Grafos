import random
import networkx as nx
from common.graphs import (from_edges, edges_of, wheel, prism, cube, octahedron, k5_minus_e, dodecahedron,
                           k5, k33, petersen, j137, random_planar_3conn)
from m1_conexidade.m1 import contractible_edges
from m2_contracao.m2 import contraction_trace, contract
from m3_faces.m3 import boundary_cycle, interval_test, insert_xy, check_embedding, reconstruct, rotacionar


def faces_nx(adj):
    ok, emb = nx.check_planarity(nx.Graph(edges_of(adj)))
    visto = set()
    out = []
    for u, v in emb.edges():
        if (u, v) not in visto:
            out.append(tuple(emb.traverse_face(u, v, mark_half_edges=visto)))
    return out


def arestas_das_faces(F):
    return {frozenset(frozenset(p) for p in zip(f, f[1:] + f[:1])) for f in F}


def mesmo_ciclo(a, b):
    a, b = list(a), list(b)
    if set(a) != set(b):
        return False
    r = list(rotacionar(b, a[0]))
    return r == a or [r[0]] + r[1:][::-1] == a


def teste_intervalo():
    C = list(range(6))
    tabela = [([4, 0, 2], [0, 1], [0, 2, 4], 0), ([0, 2, 4], [0, 5], [0, 2, 4], 2),
              ([0, 2, 4], [0, 2], [0, 2, 4], 0), ([0, 3], [0, 3], [0, 3], 0),
              ([0, 2, 4], [1, 3], [0, 2, 4], None), ([0, 3], [1, 4], [0, 3], None),
              ([0, 2, 4], [2, 4, 5], [0, 2, 4], None), ([0, 1, 2, 3], [0, 2], [0, 1, 2, 3], None),
              ([0, 2, 4], [0, 2, 4], [0, 2, 4], None)]
    for A, B, Ao, i in tabela:
        assert interval_test(C, A, B) == (i, Ao), (A, B)
    print("teste de intervalo puro ok (9 linhas)")


def teste_passo_unico():
    aceitos = rejeitados = ignorados = 0
    for g in nx.graph_atlas_g():
        if len(g) < 5 or nx.node_connectivity(g) < 3:
            continue
        J = from_edges(g.edges(), n=len(g))
        planar_J = nx.check_planarity(g)[0]
        for x, y in contractible_edges(J):
            H = contract(J, x, y)
            if not nx.check_planarity(nx.Graph(edges_of(H)))[0]:
                ignorados += 1
                continue
            A, B = sorted(J[x] - {y}), sorted(J[y] - {x})
            F = faces_nx(H)
            C = boundary_cycle(F, x)
            i, Ao = interval_test(C, A, B)
            assert (i is not None) == planar_J
            assert (interval_test(C, B, A)[0] is not None) == planar_J   # papeis trocados
            if i is None:
                rejeitados += 1
                continue
            novas = insert_xy(F, x, x, y, C, Ao, B, i)
            assert check_embedding(J, novas) is None
            assert arestas_das_faces(novas) == arestas_das_faces(faces_nx(J))
            aceitos += 1
    print(f"passo unico no atlas: {aceitos + rejeitados} passos ({aceitos} aceitos, {rejeitados} rejeitados; "
          f"{ignorados} ignorados por H nao planar)")
    assert (aceitos, rejeitados, ignorados) == (320, 468, 962)


def teste_reconstrucao():
    t, k4 = contraction_trace(wheel(4))
    log = []
    F, _ = reconstruct(t, k4, log)
    assert log[0][:7] == (0, 1, 2, [3, 0, 4], [0, 4], [0, 3], 1)
    assert sorted(len(f) for f in F) == [3, 3, 3, 3, 4]
    t, k4 = contraction_trace(cube())
    log = []
    F, _ = reconstruct(t, k4, log)
    esperado = [((4, 5), [6, 0, 7], [6, 0], [0, 7], 1), ((0, 2), [6, 7, 5, 4], [5, 4], [6, 7], 1),
                ((2, 3), [0, 4, 6, 7, 5], [0, 6], [0, 7], 1), ((0, 1), [5, 4, 6, 2, 3, 7], [4, 2], [3, 5], 1)]
    for item, (xy, C, Ao, B, i) in zip(log, esperado):
        assert item[1:3] == xy and mesmo_ciclo(item[3], C) and item[4:7] == (Ao, B, i)
    assert sorted(len(f) for f in F) == [4] * 6
    for adj, tam in ((prism(), [3, 3, 4, 4, 4]), (octahedron(), [3] * 8), (k5_minus_e(), [3] * 6),
                     (dodecahedron(), [5] * 12)):
        t, k4 = contraction_trace(adj)
        F, falha = reconstruct(t, k4)
        assert falha is None and sorted(len(f) for f in F) == tam
        assert check_embedding(adj, F) is None
    print("reconstrucao completa ok (W5, cubo, prisma, octaedro, K5-e, dodecaedro)")


def teste_rejeicoes():
    esperado = [(k5(), 0, [2, 3, 4], [2, 3, 4]), (k33(), 0, [2, 5, 1, 4], [5, 4]),
                (petersen(), 2, [7, 9, 4, 3, 8, 5], [7, 4, 3, 5]), (j137(), 1, [3, 4, 5], [3, 4, 5])]
    for adj, k, C, Ao in esperado:
        t, k4 = contraction_trace(adj)
        F, falha = reconstruct(t, k4)
        assert F is None and falha[0] == k and mesmo_ciclo(falha[1], C) and falha[2] == Ao, falha
    print("vereditos de rejeicao ok (K5, K3,3, Petersen, j137)")


def veredito(adj):
    t, k4 = contraction_trace(adj)
    F, falha = reconstruct(t, k4)
    if F is not None:
        assert check_embedding(adj, F) is None
    return F is not None


def teste_massa():
    conta = {}
    for g in nx.graph_atlas_g():
        if len(g) >= 4 and nx.node_connectivity(g) >= 3:
            adj = from_edges(g.edges(), n=len(g))
            p = veredito(adj)
            assert p == nx.check_planarity(g)[0]
            c = conta.setdefault(len(g), [0, 0])
            c[0 if p else 1] += 1
    assert conta == {4: [1, 0], 5: [2, 1], 6: [7, 10], 7: [34, 102]}, conta
    rng = random.Random(5)
    plan = nplan = 0
    for _ in range(300):
        n = rng.randint(8, 13)
        adj = random_planar_3conn(n, seed=rng.random())
        assert veredito(adj)
        plan += 1
        for _ in range(rng.randint(1, 3)):
            u, v = rng.sample(range(n), 2)
            adj[u].add(v)
            adj[v].add(u)
        p = veredito(adj)
        assert p == nx.check_planarity(nx.Graph(edges_of(adj)))[0]
        plan += p
        nplan += not p
    print(f"veredito em massa ok: atlas {conta}; aleatorios {plan} planares e {nplan} nao planares")


if __name__ == "__main__":
    teste_intervalo()
    teste_passo_unico()
    teste_reconstrucao()
    teste_rejeicoes()
    teste_massa()
    print("OK")
