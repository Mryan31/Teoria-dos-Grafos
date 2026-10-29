import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from common.draw import draw_interval
from m3_faces.m3 import interval_test
from m4_certificado.m4 import obstruction

C = list(range(6))
A = [0, 2, 4]
B = [1, 3]
x, y = "x", "y"   # b em B\A e b' fora de P_i: K3,3
i, Ao = interval_test(C, A, B)
tk = obstruction(C, x, y, A, B, Ao)
plt.figure(figsize=(5, 5))
P = draw_interval(C, x, y, A, B, i, Ao)
for (u, w), p in tk["paths"].items():   # os 9 caminhos do TK3,3
    plt.plot(*zip(*[P[v] for v in p]), lw=3, alpha=.5)
plt.title(f"{tk['kind']}: classes {[sorted(map(str, c)) for c in tk['classes']]}")
plt.savefig("figs/m4_caso1.png", dpi=110)
