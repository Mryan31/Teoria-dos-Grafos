import sys
import os


def ordena(lista):
    # grau decrescente, rotulo crescente no empate
    return sorted(lista, key=lambda p: (-p[0], p[1]))


def havel_hakimi(d):
    """d[0..n-1] em qualquer ordem; o vertice i (1..n) tem grau pedido d[i-1].
    Devolve (grafica, arestas, passos, obstrucao)."""
    for x in d:
        if x < 0:
            raise ValueError("grau negativo na entrada")
    cur = ordena([(d[i], i + 1) for i in range(len(d))])
    E = []
    passos = []
    k = 0
    while True:
        passos.append([g for g, _ in cur])
        if len(cur) == 0:
            return True, E, passos, None
        r, v = cur[0]
        resto = list(cur[1:])
        if r == 0:
            return True, E, passos, None
        if r >= len(cur):
            return False, E, passos, (k, "r >= n", r, len(cur))
        for j in range(r):
            x, u = resto[j]
            if x - 1 < 0:
                return False, E, passos, (k, "entrada negativa", u)
            resto[j] = (x - 1, u)
            E.append((v, u))
        cur = ordena(resto)
        k += 1


def graus_da_realizacao(n, E):
    g = [0] * (n + 1)
    for a, b in E:
        g[a] += 1
        g[b] += 1
    return g[1:]


def formata(d, resultado):
    grafica, E, passos, obs = resultado
    linhas = ["entrada: " + " ".join(map(str, d))]
    linhas.append("GRAFICA" if grafica else "NAO GRAFICA")
    for k, p in enumerate(passos):
        linhas.append(f"passo {k}: " + " ".join(map(str, p)))
    if grafica:
        if E:
            linhas.append("arestas: " + " ".join(f"{a}-{b}" for a, b in E))
        else:
            linhas.append("arestas: (nenhuma)")
    elif obs[1] == "r >= n":
        linhas.append(f"obstrucao: passo {obs[0]}, r >= n (r={obs[2]}, n={obs[3]})")
    else:
        linhas.append(f"obstrucao: passo {obs[0]}, entrada negativa (vertice {obs[2]})")
    return "\n".join(linhas)


def main():
    if len(sys.argv) < 2:
        print("uso: python havel_hakimi.py entradas/arquivo.txt")
        return
    caminho = sys.argv[1]
    with open(caminho) as arq:
        d = [int(x) for x in arq.read().split()]
    res = havel_hakimi(d)
    if res[0]:
        # confere a realizacao antes de imprimir
        E = res[1]
        assert graus_da_realizacao(len(d), E) == d
        assert all(a != b for a, b in E)
        assert len({frozenset(e) for e in E}) == len(E)
    texto = formata(d, res)
    print(texto)

    pasta = os.path.join(os.path.dirname(os.path.abspath(__file__)), "saidas")
    os.makedirs(pasta, exist_ok=True)
    nome = os.path.splitext(os.path.basename(caminho))[0] + ".out"
    with open(os.path.join(pasta, nome), "w") as arq:
        arq.write(texto + "\n")


if __name__ == "__main__":
    main()
