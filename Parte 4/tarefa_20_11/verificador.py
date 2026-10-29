"""Verificador independente da coloracao (NAO importa coloracao.py).
Uso: python verificador.py g.txt saida.txt konig|vizing [trocas.log]  ->  OK  ou  FALHOU: motivo"""
import sys
from collections import Counter


def delta(n, E):
    g = Counter()
    for u, v in E:
        g[u] += 1
        g[v] += 1
    return max(g.values(), default=0)


def propria(n, E, cores, C, parcial=False):
    """Devolve None ou o motivo. Cores calculadas por Counter a partir da lista de arestas."""
    if len(cores) != len(E):
        return f"{len(cores)} cores para {len(E)} arestas"
    vistas = Counter()
    for (u, v), c in zip(E, cores):
        if c == 0 and parcial:
            continue
        if not (1 <= c <= C):
            return f"cor {c} fora de 1..{C}"
        vistas[(u, c)] += 1
        vistas[(v, c)] += 1
    for (v, c), q in vistas.items():
        if q > 1:
            return f"vertice {v} tem {q} arestas de cor {c}"
    return None


def verifica(n, E, cores, modo, C=None):
    if any(u == v for u, v in E):
        return "laco"
    D = delta(n, E)
    if modo == "vizing" and len({frozenset(e) for e in E}) != len(E):
        return "grafo nao simples"
    esperado = D if modo == "konig" else (D + 1 if E else 0)
    if C is not None and C != esperado:
        return f"paleta {C}, esperado {esperado}"
    return propria(n, E, cores, esperado)


def reproduz(n, E, C, linhas):
    """Reaplica COR / TROCA / DESLOCA a partir do zero, conferindo a coloracao parcial a cada
    operacao. Devolve as cores finais (levanta AssertionError se algo estiver errado)."""
    cor = [0] * len(E)
    for linha in linhas:
        p = linha.split() if isinstance(linha, str) else [str(x) for x in linha]
        if not p:
            continue
        op = p[0]
        args = [int(x) for x in p[1:]]
        if op == "INS":
            continue
        if op == "COR":
            e, c = args
            assert cor[e] == 0, f"COR em aresta ja colorida ({e})"
            cor[e] = c
        elif op == "TROCA":
            a, b = args[0], args[1]
            P = args[2:]
            assert all(cor[e] in (a, b) for e in P), "TROCA com aresta de outra cor"
            # componente inteira: nenhuma aresta de cor a/b fora de P toca um vertice de P
            V = {v for e in P for v in E[e]}
            fora = [e for e in range(len(E)) if e not in P and cor[e] in (a, b) and (E[e][0] in V or E[e][1] in V)]
            assert not fora, f"TROCA nao e componente inteira (aresta {fora[0]})"
            for e in P:
                cor[e] = a if cor[e] == b else b
        elif op == "DESLOCA":
            es = args
            assert cor[es[0]] == 0, "DESLOCA com e0 colorida"
            old = [cor[e] for e in es]
            for i in range(1, len(es)):
                cor[es[i - 1]] = old[i]
            cor[es[-1]] = 0
        else:
            raise AssertionError(f"operacao desconhecida {op}")
        msg = propria(n, E, cor, C, parcial=True)
        assert msg is None, f"depois de '{' '.join(p)}': {msg}"
    return cor


def ler_grafo(caminho):
    with open(caminho) as arq:
        nums = [int(x) for x in arq.read().split()]
    n, m = nums[0], nums[1]
    return n, [(nums[2 + 2 * i], nums[3 + 2 * i]) for i in range(m)]


def main():
    if len(sys.argv) < 4:
        print("uso: python verificador.py g.txt saida.txt konig|vizing [trocas.log]")
        return 2
    n, E = ler_grafo(sys.argv[1])
    with open(sys.argv[2]) as arq:
        linhas = arq.read().split("\n")
    C = int(linhas[0].split()[1])
    cores = [int(x) for x in linhas[2].split()] if len(linhas) > 2 else []
    msg = verifica(n, E, cores, sys.argv[3], C)
    if msg is None and len(sys.argv) > 4:
        with open(sys.argv[4]) as arq:
            try:
                final = reproduz(n, E, C, arq.read().split("\n"))
                if final != cores:
                    msg = "a reproducao do log nao da as mesmas cores"
            except AssertionError as erro:
                msg = f"log: {erro}"
    print("OK" if msg is None else "FALHOU: " + msg)
    return 0 if msg is None else 1


if __name__ == "__main__":
    sys.exit(main())
