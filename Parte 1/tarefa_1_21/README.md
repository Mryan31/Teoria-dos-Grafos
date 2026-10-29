# Tarefa 1.21 - Refinamento de cores (1-WL)

## Como rodar

```
python refinamento.py entradas/p5.txt   # imprime e grava saidas/p5.out
python testes.py
python graficos.py                      # grava figuras/*.png
```

## Entrada e saída

Entrada: primeira linha `n m`, depois `m` linhas `u v` (vértices de 1 a n). Laços e
arestas repetidas são rejeitados, porque a tarefa pede grafo simples.

Saída:

```
rodadas: 1
classes: 3
cores: 0 1 2 1 0
```

`cores` é a cor de v1, ..., vn.

## Convenções

- c0(v) = posição do grau de v na lista ordenada dos graus distintos.
- Em cada rodada a assinatura de v é `(c[v], tupla ordenada das cores dos vizinhos)`.
  As assinaturas distintas são ordenadas e a nova cor é a posição nessa lista. Assim a
  numeração não depende dos rótulos, e grafos isomorfos dão as mesmas cores.
- **rodadas** = número de rodadas que dividiram alguma classe. A última rodada, que só
  confirma que nada mudou, não é contada. Como a cor antiga faz parte da assinatura, a
  nova partição sempre refina a anterior, então basta comparar o número de classes para
  saber se parou.

## O que foi testado (`testes.py`)

- As 14 linhas da tabela do guia (P5, P7, vassoura, T1, T2, estrela, K3,3, prisma, paw,
  C5, K4, isolados, n=1, uma aresta).
- Em 300 grafos aleatórios (n ≤ 12): cada c_{i+1} refina c_i, o número de classes cresce
  estritamente e a coloração final é estável (mesma cor ⇒ mesmo grau e mesmo multiconjunto
  de cores vizinhas).
- Lema 1.20: aplicando uma permutação aleatória π, cor de π(v) em π(G) = cor de v em G,
  com o mesmo número de rodadas.
- Comparação com `nx.weisfeiler_lehman_subgraph_hashes` (só a relação "mesmo hash ⇔ mesma
  cor" em cada rodada) e com `weisfeiler_lehman_graph_hash`: T1 ≠ T2 e K3,3 = prisma.
- Laço e aresta repetida são rejeitados.

## Figuras

- `classes_finais.png`: P5 tem 3 classes simétricas, T1 e T2 terminam com 4 e 5 classes
  (então são distinguidos), e o K3,3 fica todo de uma cor, o que mostra a incompletude
  do método.
- `classes_por_rodada.png`: o número de classes sobe em degraus e para quando a curva
  fica plana.
- `tempo.png`: no caminho (pior caso) a inclinação medida foi **2,01**; nos grafos
  aleatórios com m = 2n, **1,09**.
