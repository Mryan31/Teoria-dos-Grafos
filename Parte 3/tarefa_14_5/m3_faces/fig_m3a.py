import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from common.graphs import dodecahedron
from common.draw import draw_interval
from m2_contracao.m2 import contraction_trace
from m3_faces.m3 import k4_faces, boundary_cycle, interval_test, insert_xy

trace, k4 = contraction_trace(dodecahedron())
faces = k4_faces(*sorted(k4))
PASSO = 9
for k in range(len(trace) - 1, PASSO - 1, -1):
    x, y, A, B = trace[k]
    C = boundary_cycle(faces, x)
    i, Ao = interval_test(C, A, B)
    if k > PASSO:
        faces = insert_xy(faces, x, x, y, C, Ao, B, i)
plt.figure(figsize=(5, 5))
draw_interval(C, x, y, A, B, i, Ao)
plt.title(f"passo {PASSO}: x={x}, y={y}, i={i}  A=vermelho  B=azul")
plt.savefig("figs/m3_intervalo.png", dpi=110)
