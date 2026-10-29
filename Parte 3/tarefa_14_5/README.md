# Tarefa 14.5 - Teste de planaridade por contrações

Entrada: um grafo 3-conexo. O programa contrai arestas mantendo a 3-conexidade até chegar
no K4, depois desfaz as contrações de trás para frente aplicando o teste de intervalo
(Lema 14.2) e atualizando as faces. No fim:

- se o grafo é **planar**, imprime as faces e uma base esparsa do espaço de ciclos (Mac
  Lane), verificada;
- se **não é planar**, imprime um menor K5 ou K3,3 (conjuntos de ramificação e a lista de
  contrações/remoções), verificado por um conferidor independente.

O relatório curto está em `relatorio.pdf` (gerado por `gera_relatorio.py`).

## Como rodar (sempre a partir desta pasta)

```
python planar_contract.py exemplos/cubo.txt     # integrador
python -m m1_conexidade.test_m1                 # um teste por marco (cada um termina com OK)
python -m m2_contracao.test_m2
python -m m3_faces.test_m3
python -m m4_certificado.test_m4
python -m m5_base_ciclos.test_m5
python -m m6_tutte.test_m6
python test_integrador.py
python -m m3_faces.fig_m3a                      # figuras: python -m mK_....fig_mKx (gravam em figs/)
python gera_relatorio.py                        # relatorio.pdf (depois das figuras)
```

Não há `__init__.py`: as pastas são pacotes de namespace do Python 3.

## Estrutura

| pasta / arquivo       | conteúdo |
|-----------------------|----------|
| `common/graphs.py`    | `from_edges`, `edges_of`, `copy`, `ler`, fixtures (`wheel`, `prism`, `cube`, `octahedron`, `petersen`, `k5`, `k33`, `k5_minus_e`, `dodecahedron`, `j137`, `k4_sub`) e `random_planar_3conn` |
| `common/draw.py`      | `positions`, `fill_faces`, `draw_interval` (só para figuras) |
| `m1_conexidade/`      | 3-conexidade, separador, aresta contraível (Def. 11.9, Lema 11.11, Teor. 11.12) |
| `m2_contracao/`       | `contract`, `contraction_trace`, `uncontract`, `branch_sets` |
| `m3_faces/`           | `k4_faces`, `boundary_cycle`, `interval_test`, `insert_xy`, `check_embedding`, `reconstruct` |
| `m4_certificado/`     | `obstruction` (casos a/b/c), `model_from_tk`, `lift_model`, `verify_minor`, `certificate_ops` |
| `m5_base_ciclos/`     | `face_basis`, `rank_f2`, `verify_basis`, `fundamental_basis`, `tem_base_esparsa` |
| `m6_tutte/`           | (opcional) `tutte_positions`, `verify_tutte` |
| `planar_contract.py`  | integrador (`decidir` + saída) |
| `exemplos/`           | w5, prisma, cubo, dodecaedro, k5, k33, petersen, j137, k4sub |

O `networkx` não aparece em nenhum `m*.py` nem em `planar_contract.py`. Ele só é usado
nos testes, nas figuras e em `common/draw.py`. O dodecaedro foi copiado como lista de
arestas de `nx.dodecahedral_graph()`, então nem `common/graphs.py` depende do networkx.

## Entrada e saída

Entrada: linhas vazias e comentários `#` são ignorados; `n m` e depois `m` linhas `u v`
(vértices 0..n−1, grafo simples).

```
$ python planar_contract.py exemplos/petersen.txt
NAO PLANAR
contracoes: 6
  passo 0: contrai (0,1)  N(x)-y=[4, 5]  N(y)-x=[2, 6]  ->  9 vertices, 3-conexo: sim
  ...
reconstrucao:
  passo 5: (3,5) C=[7, 0, 9] Ao=[0, 9] B=[0, 7] i=1 -> 5 faces
  ...
  passo 2: (0,6) C=[7, 9, 4, 3, 8, 5] Ao=[7, 4, 3, 5] B=[8, 9] -> FALHA no teste de intervalo
falhou no passo 2 (teste de intervalo); menor K33 (caso a)
C = 7 9 4 3 8 5 | A = 7 4 3 5 | B = 8 9
operacoes: contract 0 1 / contract 0 2 / contract 4 9 / contract 4 7 / del_edge 0 4
conjuntos: {0,1,2} {8} {4,7,9} {3} {5} {6}
verificacao: ok
```

Para um grafo planar, o programa imprime as faces (uma por linha) e a linha da base
esparsa (`posto F2 = m-n+1`, `max aresta em 2`). Uma entrada que não é 3-conexa dá
`ENTRADA INVALIDA` com o separador e código de saída 2.

## Resultados dos testes

- **M1**: tabela do guia; atlas n = 4..7 com 1, 3, 17, 136 grafos 3-conexos; 2196 arestas
  com contraibilidade igual à do networkx; mínimo de arestas contraíveis 4, 3, 5.
- **M2**: todas as trilhas da tabela; mesma trilha com um escolhedor feito só com
  networkx; `uncontract` devolve G; `branch_sets` correto.
- **M3**: teste de intervalo puro (9 linhas); passo único no atlas com **788 passos (320
  aceitos, 468 rejeitados, 962 ignorados)**, exatamente como a referência; reconstrução do
  cubo passo a passo; vereditos do atlas 1/0, 2/1, 7/10, 34/102; 600 aleatórios.
- **M4**: casos abstratos; os 113 não planares do atlas com certificado verificado (casos
  **55 (c), 45 (a), 13 (b)**, igual à referência) + 237 aleatórios; conferidor não cego.
- **M5**: tabela do guia, contrastes rejeitados (base fundamental com uso 3, face repetida,
  grau ímpar) e força bruta de Mac Lane (K4 e W5 sim; K3,3 e K5 não).
- **M6**: coordenadas do guia para W_k, cubo, prisma, octaedro e dodecaedro
  (det L_II = 4,03·10⁵); 200 planares aleatórios sem cruzamentos; contraexemplo com ciclo
  não periférico.
- **Integrador**: atlas inteiro, 900 gnm 3-conexos (n = 8..13), 440 planares + 440 com
  arestas extras (n = 5..15) e os 9 exemplos pela linha de comando. Sem divergência com
  `nx.check_planarity`.

## Figuras (`figs/`)

| figura | o que mostra |
|--------|--------------|
| `m1_contraiveis.png` | no prisma só as 3 "colunas" são contraíveis; na roda, só o aro |
| `m1_separadores.png` | entradas rejeitadas com o separador em vermelho |
| `m2_sequencia_cubo.png` | a trilha J8 → ... → K4 do cubo |
| `m2_vizinhancas.png` | A, B e A ∩ B nos 3 primeiros passos do dodecaedro |
| `m3_intervalo.png` | passo 9 do dodecaedro: x = 3, y = 15, i = 1; B cabe em P_1 |
| `m3_antes_depois.png` | faces em volta de z = 2 antes e depois da inserção (cubo, passo 1) |
| `m4_caso1.png` | caso (a) abstrato com os 9 caminhos do TK3,3 |
| `m4_petersen.png` | Petersen com um conjunto de ramificação por cor (6 cores) |
| `m5_base_cubo.png` | as 5 faces internas do cubo, que formam a base |
| `m5_uso_arestas.png` | uso máximo 2 na base de faces contra 3 na base fundamental |
| `m6_tutte.png` | desenho de Tutte do cubo e do dodecaedro |
| `m6_tutte_aleatorio.png` | mesmo grafo com a menor e a maior face como externa |
