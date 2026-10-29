import random
import networkx as nx
from common.graphs import from_edges, edges_of, k5, k33, j137, petersen, random_planar_3conn
from m2_contracao.m2 import contraction_trace, branch_sets
from m3_faces.m3 import reconstruct, interval_test
from m4_certificado.m4 import (obstruction, verifica_tk, model_from_tk, lift_model, verify_minor,
                               certificate_ops)


def J_abstrato(C, A, B):
    # ciclo C + x ligado a A + y ligado a B + xy
    adj = {v: set() for v in C + ["x", "y"]}
    for u, w in zip(C, C[1:] + C[:1]):
        adj[u].add(w)
        adj[w].add(u)
    for a in A:
        adj["x"].add(a)
        adj[a].add("x")
    for b in B:
        adj["y"].add(b)
        adj[b].add("y")
    adj["x"].add("y")
    adj["y"].add("x")
    return adj


def teste_abstratos():
    C = list(range(6))
    casos = [([0, 2, 4], [1, 3], "K33", ({"x", 1, 3}, {"y", 0, 2})),
             ([0, 2, 4], [2, 4, 5], "K33", ({"x", 5, 2}, {"y", 4, 0})),
             ([0, 1, 2, 3], [0, 2], "K33", ({"x", 0, 2}, {"y", 1, 3})),
             ([0, 2, 4], [0, 2, 4], "K5", ({"x", "y", 0, 2, 4},))]
    for A, B, kind, classes in casos:
        i, Ao = interval_test(C, A, B)
        assert i is None
        tk = obstruction(C, "x", "y", A, B, Ao)
        assert tk["kind"] == kind and tuple(tk["classes"]) == classes, tk["classes"]
        assert verifica_tk(J_abstrato(C, A, B), tk) is None
        assert len(tk["paths"]) == (9 if kind == "K33" else 10)
    print("casos abstratos ok (a, a, b, c)")


def certificado(adj):
    trace, k4 = contraction_trace(adj)
    F, falha = reconstruct(trace, k4)
    assert F is None
    k, C, Ao = falha
    x, y, A, B = trace[k]
    tk = obstruction(C, x, y, A, B, Ao)
    conj = branch_sets(trace, k, list(adj))
    J = {v: set() for v in conj}
    for u in conj:
        for w in conj:
            if u != w and any(b in adj[a] for a in conj[u] for b in conj[w]):
                J[u].add(w)
    assert verifica_tk(J, tk) is None
    model = lift_model(model_from_tk(tk), conj)
    assert verify_minor(adj, model, tk["kind"]) is None
    ops, H = certificate_ops(adj, model, tk["kind"])
    alvo = nx.complete_graph(5) if tk["kind"] == "K5" else nx.complete_bipartite_graph(3, 3)
    assert nx.is_isomorphic(nx.Graph(edges_of(H)), alvo)
    return k, tk, model, ops


def teste_tabela():
    k, tk, model, ops = certificado(k5())
    assert k == 0 and tk["caso"] == "c" and sorted(map(sorted, model.values())) == [[0], [1], [2], [3], [4]] and ops == []
    k, tk, model, ops = certificado(k33())
    assert k == 0 and tk["caso"] == "a" and ops == []
    assert {frozenset().union(*(model[v] for v in c)) for c in tk["classes"]} == {frozenset({0, 1, 2}), frozenset({3, 4, 5})}
    k, tk, model, ops = certificado(j137())
    assert k == 1 and tk["kind"] == "K5" and sorted(map(sorted, model.values())) == [[0, 1], [2], [3], [4], [5]]
    assert ops == [("contract", 0, 1)]
    k, tk, model, ops = certificado(petersen())
    assert k == 2 and tk["kind"] == "K33" and tk["caso"] == "a"
    assert sorted(map(sorted, model.values())) == [[0, 1, 2], [3], [4, 7, 9], [5], [6], [8]]
    print("tabela M4 ok (K5, K3,3, j137, Petersen); Petersen:", ops)


def teste_massa():
    casos = {"a": 0, "b": 0, "c": 0}
    total = 0
    for g in nx.graph_atlas_g():
        if len(g) >= 5 and nx.node_connectivity(g) >= 3 and not nx.check_planarity(g)[0]:
            _, tk, _, _ = certificado(from_edges(g.edges(), n=len(g)))
            casos[tk["caso"]] += 1
            total += 1
    assert total == 113
    print(f"atlas: {total} nao planares, casos {casos}")
    rng = random.Random(9)
    feitos = 0
    while feitos < 237:
        n = rng.randint(8, 13)
        adj = random_planar_3conn(n, seed=rng.random())
        for _ in range(rng.randint(1, 3)):
            u, v = rng.sample(range(n), 2)
            adj[u].add(v)
            adj[v].add(u)
        if nx.check_planarity(nx.Graph(edges_of(adj)))[0]:
            continue
        _, tk, _, _ = certificado(adj)
        casos[tk["caso"]] += 1
        feitos += 1
    print(f"+ {feitos} aleatorios nao planares: casos acumulados {casos}")
    assert all(c > 0 for c in casos.values())


def teste_conferidor_nao_cego():
    adj = k5()
    bom = {v: {v} for v in range(5)}
    assert verify_minor(adj, bom, "K5") is None
    ruins = [{**bom, 0: set()},              # conjunto vazio
             {0: {0, 1}, 2: {2}, 3: {3}, 4: {4}},   # dois conjuntos fundidos (so sobram 4)
             {**bom, 0: {0, 1}},             # nao disjunto (1 aparece duas vezes)
             ]
    for m in ruins:
        assert verify_minor(adj, m, "K5") is not None
    sem_aresta = {v: set(adj[v]) for v in adj}
    sem_aresta[0].discard(1)
    sem_aresta[1].discard(0)
    assert verify_minor(sem_aresta, bom, "K5") is not None
    P = petersen()
    assert verify_minor(P, {"a": {0, 2}, "b": {1}, "c": {3}, "d": {4}, "e": {5}}, "K5") is not None  # {0,2} desconexo
    print("conferidor rejeita conjunto vazio, fundido, desconexo e aresta faltando")


if __name__ == "__main__":
    teste_abstratos()
    teste_tabela()
    teste_massa()
    teste_conferidor_nao_cego()
    print("OK")
