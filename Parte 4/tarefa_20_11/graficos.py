import time
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from desenho import desenha, circ
from coloracao import colorir
from grafos import petersen, completo, kmn
from verificador import reproduz


def figA():
    n, E = petersen()
    cor, log, st = colorir(n, E, "vizing")
    pos = circ(5) + circ(5, .5)
    n6, E6 = completo(6)
    cor6, _, _ = colorir(n6, E6, "vizing")
    fig, ax = plt.subplots(1, 2, figsize=(11, 5.5))
    desenha(ax[0], E, cor, pos, tit=f"Petersen: {len(set(cor))} cores (chi'=4)")
    desenha(ax[1], E6, cor6, circ(6), tit=f"K6: {len(set(cor6))} cores (chi'=5; Vizing pode gastar uma a mais)")
    plt.savefig("figuras/figA_cores.png", dpi=90)
    plt.close(fig)


def figB():
    n, E = 6, [(2, 4), (1, 5), (0, 5), (1, 3), (0, 4)]
    pos = {2: (0, 0), 4: (1, .3), 0: (2, 0), 5: (3, .3), 1: (4, 0), 3: (5, .3)}
    pos = [pos[v] for v in range(n)]
    cor, log, st = colorir(n, E, "konig")
    tr = [l for l in log if l[0] == "TROCA"][0]
    P = tr[3:]
    a, b = tr[1:3]
    ant, _, _ = colorir(n, E[:-1], "konig", C=2)
    ant = ant + [0]   # estado antes de inserir a ultima aresta
    fig, ax = plt.subplots(2, 1, figsize=(9, 5))
    desenha(ax[0], E, ant, pos, P, f"antes: x=0 tem cor {b}, y=4 tem cor {a}; componente ({a},{b}) de x "
                                   f"em destaque; aresta 0-4 sem cor")
    desenha(ax[1], E, cor, pos, P, f"depois da troca {a}<->{b}: cor {b} livre em x e em y; 0-4 recebe {b}")
    plt.tight_layout()
    plt.savefig("figuras/figB_konig.png", dpi=90)
    plt.close(fig)


def figC():
    n, E = 5, [(3, 0), (0, 1), (0, 4), (3, 4), (4, 1), (4, 2)]   # x=4, leque y0=2,y1=3,y2=0,y3=1 (j=1, k=3)
    pos = [(0, 2.2), (2.2, 2), (0, -2), (-2.2, 2), (0, 0)]
    cor, log, st = colorir(n, E, "vizing")
    C = st["C"]
    ini = log.index(("INS", 5, 4, 2))
    L = [" ".join(map(str, l)) for l in log]
    it = [i for i in range(ini, len(log)) if log[i][0] == "TROCA"][0]
    P = log[it][3:]
    estados = [("antes (xy0 sem cor)", ini + 1, ()), ("apos 1o deslocamento ate y_j", it, P),
               ("apos a troca alfa<->beta em P", it + 1, ()), ("final: segundo deslocamento + cor beta", len(log), ())]
    fig, ax = plt.subplots(2, 2, figsize=(10, 8))
    for a, (t, i, d) in zip(ax.flat, estados):
        c = reproduz(n, E, C, L[:i])
        desenha(a, E, c, pos, d, t)
    plt.tight_layout()
    plt.savefig("figuras/figC_leque.png", dpi=90)
    plt.close(fig)


def figD():
    def tempo(modo, N, E):
        t0 = time.perf_counter()
        colorir(N, E, modo)
        return time.perf_counter() - t0
    res = {}
    for modo, fam, ns in [("konig", lambda s: kmn(s, s), [8, 12, 16, 24, 32, 48, 64]),
                          ("vizing", completo, [10, 14, 20, 28, 40, 56, 80])]:
        M, T = [], []
        for s in ns:
            N, E = fam(s)
            M.append(len(E))
            T.append(min(tempo(modo, N, E) for _ in range(3)))
        res[modo] = (M, T, np.polyfit(np.log(M), np.log(T), 1)[0])
    plt.figure()
    for modo, (M, T, a) in res.items():
        print(f"{modo}: expoente {a:.2f}")
        plt.loglog(M, T, "o-", label=f"{modo}: expoente {a:.2f}")
    plt.xlabel("m")
    plt.ylabel("segundos")
    plt.legend()
    plt.savefig("figuras/figD_tempo.png", dpi=90)
    plt.close()


if __name__ == "__main__":
    figA()
    figB()
    figC()
    figD()
    print("figuras gravadas em figuras/")
