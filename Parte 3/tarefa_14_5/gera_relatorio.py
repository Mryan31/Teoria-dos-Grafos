"""Gera relatorio.pdf (texto + figuras) so com matplotlib. Rode da raiz depois dos fig_*.py."""
import textwrap
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
from matplotlib.backends.backend_pdf import PdfPages

PAGINA1 = """
Tarefa 14.5 — Teste de planaridade por contrações (relatório)

1. Representação
- Grafo: dict[int, set[int]]. contract(adj, x, y) devolve um grafo novo; o vértice contraído fica com o rótulo de x.
- Trilha: lista de (x, y, A, B) com A = N_J(x) − {y} e B = N_J(y) − {x}, registrados ANTES de contrair (14.1).
  Regra de desempate: primeira aresta contraível em ordem lexicográfica. A contraibilidade usa o Lema 11.11
  (G/xy é 3-conexo ⇔ nenhum {x, y, z} separa G), sem reconstruir G/xy.
- Faces: tuplas cíclicas, todas no mesmo sentido (cada dart (u, v) em exatamente uma face). O K4 final começa
  com (a,b,c) (a,c,d) (a,d,b) (b,d,c). Um juiz interno (check_embedding) confere darts, Euler e a rotação em
  cada vértice.
- Certificado: tk = (tipo, classes, caminhos) dentro de J_k. O modelo em G é obtido absorvendo os interiores
  dos caminhos e expandindo cada vértice de J_k pelos seus conjuntos de ramificação (branch_sets). Um
  conferidor independente (verify_minor, Def. 13.3) checa conjuntos não vazios, disjuntos, conexos e as
  arestas entre eles.
- Base de ciclos: vetores de F2^m guardados como inteiros (bit j = j-ésima aresta); posto por eliminação
  com XOR.

2. Decisões sobre as armadilhas e os pontos em aberto
- A não vem ordenado ao longo de C: interval_test ordena A pela posição em C antes de definir os arcos P_i.
- "B ⊆ V(P_i)" inclui os extremos (teste (pos(b) − s) mod L ≤ vão). Quando vários i servem, fica o primeiro.
- O vértice contraído z é o próprio x, então o ciclo C sai do encadeamento dos caminhos (z, p0..pk) das
  faces de z.
- Entrada não 3-conexa é rejeitada com um separador de ≤ 2 vértices (código de saída 2).
- Certificado: a tarefa fala em "contrações e remoções" sem dizer menor ou subdivisão. Devolvo um MENOR
  (modelo), porque em geral só ele existe em G (Ex. 13.7: o j137 dá um K5 com o conjunto {0, 1}).
  certificate_ops lista as remoções de vértices, as remoções de arestas internas fora de uma árvore geradora
  de cada conjunto, as contrações das árvores e, no K3,3, as remoções das arestas entre conjuntos do mesmo
  lado. Nos testes o grafo final é conferido por isomorfismo com K5 / K3,3.
- Nomes: no Tutte uso "borda" e "interior" para não confundir com os A, B de (14.1).
  W5 = wheel(4) (ciclo abcd + o).

3. Complexidade
- is_contractible: O(n(n + m)) (uma BFS para cada z). Achar uma aresta contraível custa no pior caso
  O(m·n(n + m)), mas na prática a primeira ou a segunda aresta testada já serve. A trilha tem n − 4 passos.
- Reconstrução: cada passo percorre as faces de z e o ciclo C, em O(n + m). Total O(n(n + m)).
- Tempos medidos: dodecaedro 0,002 s; planar aleatório com n = 40 em 0,02 s e com n = 60 em 0,06 s.
"""

PAGINA2 = """
4. Testes (todos passam: python -m mK_....test_mK e python test_integrador.py)

M1  Tabela do guia (W5: 4/8 contraíveis, prisma 3/9, K5−e 6/9, j137 9/11; separadores de P5, C5, K4
    subdividido e dois K4). Atlas n = 4..7: 1, 3, 17, 136 grafos 3-conexos, iguais ao networkx; 2196 arestas
    com contraibilidade igual a node_connectivity(G/xy) ≥ 3; mínimo de arestas contraíveis 4, 3, 5 (nunca 0,
    Teor. 11.12).
M2  Trilhas da tabela (W5, prisma, cubo, K5, K3,3, j137, Petersen, dodecaedro) iguais, também com um
    escolhedor feito só com networkx. Todo J_k é 3-conexo, uncontract de trás para frente devolve G
    exatamente e branch_sets particiona V(G). 156 grafos do atlas + 60 aleatórios de 8 a 13 vértices.
M3  As 9 linhas do teste de intervalo puro. Passo único no atlas: 788 passos (320 aceitos, 468 rejeitados,
    962 ignorados por H não planar), igual à referência, com as faces novas iguais às do networkx.
    Reconstrução do cubo passo a passo como na tabela; 6 faces no cubo e 12 pentágonos no dodecaedro.
    Rejeições de K5, K3,3, Petersen e j137 no passo e com o C esperados. Veredito em massa: atlas
    (planares/não planares) 4: 1/0, 5: 2/1, 6: 7/10, 7: 34/102, e 600 aleatórios de 8 a 13 vértices,
    sem divergência.
M4  Casos abstratos (a), (a), (b), (c). Nos 113 não planares do atlas, verify_minor aceita e as operações
    levam a um grafo isomorfo a K5/K3,3; casos 55 (c), 45 (a), 13 (b), igual à referência. Mais 237
    aleatórios. O conferidor rejeita conjunto vazio, conjuntos fundidos, conjunto desconexo e aresta
    faltando.
M5  W5, prisma, cubo, octaedro, K5−e e dodecaedro: m − n + 1 vetores, posto cheio, cada aresta em ≤ 2.
    Contrastes rejeitados: base fundamental do cubo e de K5 (uso 3), face repetida, vetor com grau ímpar.
    Força bruta (P5(d)): K4 e W5 têm base esparsa; K3,3 e K5 não.
M6  W_k com o centro na origem; cubo com os internos a distância 1/3 e menor curva 0,222; prisma e octaedro
    com as coordenadas do guia; dodecaedro com det L_II = 4,03·10^5 e menor curva 0,023; 200 planares
    aleatórios sem cruzamentos; contraexemplo com ciclo não periférico (dois vértices no mesmo ponto).
Integrador: atlas inteiro com faces iguais às do networkx e base verificada (planares) ou menor verificado
    (não planares); 900 aleatórios gnm 3-conexos (n = 8..13) e 440 planares + 440 com arestas extras
    (n = 5..15); os 9 arquivos de exemplos/ pela linha de comando.

Pergunta do checklist: trocar a regra de desempate das arestas muda o veredito ou o número de faces?
Não. O veredito vem do Lema 14.2, e o mergulho de um grafo 3-conexo é único (Whitney, Teor. 12.12).
Mudam só C, Ao, i e o certificado.
"""


def pagina_texto(pdf, texto):
    fig = plt.figure(figsize=(8.27, 11.69))
    linhas = []
    for l in texto.strip("\n").split("\n"):
        linhas += textwrap.wrap(l, 112, subsequent_indent="    ") or [""]
    fig.text(0.06, 0.96, "\n".join(linhas), va="top", ha="left", family="DejaVu Sans Mono", fontsize=7.8,
             linespacing=1.35)
    pdf.savefig(fig)
    plt.close(fig)


def pagina_figuras(pdf, arquivos, legendas):
    fig, axs = plt.subplots(len(arquivos), 1, figsize=(8.27, 11.69))
    for ax, arq, leg in zip(axs, arquivos, legendas):
        ax.imshow(mpimg.imread(arq))
        ax.axis("off")
        ax.set_title(leg, fontsize=9)
    plt.tight_layout()
    pdf.savefig(fig)
    plt.close(fig)


if __name__ == "__main__":
    with PdfPages("relatorio.pdf") as pdf:
        pagina_texto(pdf, PAGINA1)
        pagina_texto(pdf, PAGINA2)
        pagina_figuras(pdf, ["figs/m2_sequencia_cubo.png", "figs/m3_intervalo.png", "figs/m4_petersen.png"],
                       ["Trilha de contrações do cubo até o K4",
                        "Teste de intervalo no passo 9 do dodecaedro: B (azul) cabe no arco P_1 (laranja)",
                        "Petersen: menor K3,3, um conjunto de ramificação por cor"])
        pagina_figuras(pdf, ["figs/m5_uso_arestas.png", "figs/m6_tutte.png"],
                       ["Uso de cada aresta: base de faces (máx. 2) × base fundamental (máx. 3)",
                        "Desenho de Tutte do cubo e do dodecaedro"])
    print("relatorio.pdf gravado")
