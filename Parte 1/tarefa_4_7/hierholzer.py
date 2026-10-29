import sys
import os


def ler_grafo(caminho):
    with open(caminho) as arq:
        nums = arq.read().split()
    n, m = int(nums[0]), int(nums[1])
    arestas = [(int(nums[2 + 2 * i]), int(nums[3 + 2 * i])) for i in range(m)]
    return n, arestas


def montar_incidencia(n, arestas):
    # adj[v] = pares (vizinho, id); laco entra duas vezes em adj[u] (conta 2 no grau)
    adj = [[] for _ in range(n + 1)]
    for i, (u, v) in enumerate(arestas, start=1):
        if not (1 <= u <= n and 1 <= v <= n):
            raise ValueError(f"vertice fora de 1..{n} na aresta {i}")
        adj[u].append((v, i))
        adj[v].append((u, i))
    return adj


def diagnostico(n, arestas):
    """Devolve None se for euleriano, senao uma string com o motivo."""
    if len(arestas) == 0:
        return "sem arestas"
    adj = montar_incidencia(n, arestas)
    com_grau = [v for v in range(1, n + 1) if len(adj[v]) > 0]
    # suporte conexo: busca a partir de um vertice de grau positivo
    visto = [False] * (n + 1)
    visto[com_grau[0]] = True
    pilha = [com_grau[0]]
    while pilha:
        u = pilha.pop()
        for w, _ in adj[u]:
            if not visto[w]:
                visto[w] = True
                pilha.append(w)
    if any(not visto[v] for v in com_grau):
        return "suporte desconexo"
    impares = [v for v in com_grau if len(adj[v]) % 2 == 1]
    if impares:
        return "graus impares em " + " ".join(map(str, impares))
    return None


def hierholzer(n, arestas, s=None, traco=None):
    """Proposicao 4.6 com ids de arestas e cursor em cada lista de incidencia.
    Devolve (vertices, ids). Levanta ValueError se nao for euleriano."""
    motivo = diagnostico(n, arestas)
    if motivo is not None:
        raise ValueError(motivo)
    adj = montar_incidencia(n, arestas)
    m = len(arestas)
    if s is None:
        s = min(v for v in range(1, n + 1) if adj[v])
    elif not adj[s]:
        raise ValueError("vertice inicial sem arestas")
    usada = [False] * (m + 1)
    ptr = [0] * (n + 1)
    S = [(s, 0)]          # (vertice, id da aresta usada para chegar nele)
    RV, RE = [], []
    while S:
        if traco is not None:
            traco.append(len(S))
        v, e = S[-1]
        while ptr[v] < len(adj[v]) and usada[adj[v][ptr[v]][1]]:
            ptr[v] += 1
        if ptr[v] < len(adj[v]):
            w, i = adj[v][ptr[v]]
            ptr[v] += 1
            usada[i] = True
            S.append((w, i))
        else:
            S.pop()
            RV.append(v)
            RE.append(e)
    if traco is not None:
        traco.append(0)
    return RV[::-1], RE[:-1][::-1]


def verificar(arestas, V, ids):
    m = len(arestas)
    assert len(V) == m + 1 and len(ids) == m and V[0] == V[m]
    assert sorted(ids) == list(range(1, m + 1))     # cada id uma vez
    for k in range(m):
        u, v = arestas[ids[k] - 1]
        assert {V[k], V[k + 1]} == {u, v}


def main():
    if len(sys.argv) < 2:
        print("uso: python hierholzer.py entradas/arquivo.txt [vertice_inicial]")
        return
    caminho = sys.argv[1]
    s = int(sys.argv[2]) if len(sys.argv) > 2 else None
    n, arestas = ler_grafo(caminho)
    motivo = diagnostico(n, arestas)
    if motivo == "sem arestas":
        texto = "sem arestas: nada a percorrer"
    elif motivo is not None:
        texto = "NAO EULERIANO: " + motivo
    else:
        V, ids = hierholzer(n, arestas, s)
        verificar(arestas, V, ids)
        texto = ("EULERIANO\nvertices: " + " ".join(map(str, V)) +
                 "\narestas: " + " ".join(map(str, ids)))
    print(texto)

    pasta = os.path.join(os.path.dirname(os.path.abspath(__file__)), "saidas")
    os.makedirs(pasta, exist_ok=True)
    nome = os.path.splitext(os.path.basename(caminho))[0]
    if s is not None:
        nome += f"_s{s}"
    with open(os.path.join(pasta, nome + ".out"), "w") as arq:
        arq.write(texto + "\n")


if __name__ == "__main__":
    main()
