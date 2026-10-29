# Tarefa 2.11 - Remoção de vértices de grau baixo

## Como rodar

```
python nucleo_denso.py entradas/limiar_sobe.txt   # imprime e grava saidas/limiar_sobe.out
python testes.py
python graficos.py
```

## Entrada e saída

Entrada: `n m` e depois `m` linhas `u v` (vértices 1..n; vértices isolados são permitidos).
O grafo tem que ser simples.

```
n=4 m=4 grau_medio(G)=2.000
removidos (vertice:grau): 4:1
H = 1 2 3     |E(H)|=3
grau_medio(H)=2.000  delta(H)=2
```

Sem arestas, o programa imprime `erro: o Teorema 2.8 exige ao menos uma aresta`.

## Ideia e regra de desempate

É a prova do Teorema 2.8: enquanto o grafo corrente F tiver um vértice v com
d_F(v) ≤ grau_medio(F)/2, remove v. O grau médio é recalculado a cada remoção.

O teste usa só inteiros:

d ≤ grau_medio(F)/2 = (2 m_F / n_F)/2 = m_F / n_F  ⇔  d · n_F ≤ m_F.

Se algum vértice é removível, o de menor grau também é. Por isso o programa sempre olha
o de menor grau, usando um `heapq` de pares (grau, rótulo) com remoção preguiçosa (as
entradas velhas são descartadas quando chegam ao topo). Desempate: menor grau, depois
menor rótulo. Custo O((n + m) log n).

No fim, o programa confere com `assert` que δ(H)·|H| > m_H e que m_H/|H| ≥ m/n.

## O que foi testado (`testes.py`)

- As 11 linhas da tabela, inclusive o caso "limiar sobe": o vértice 6 (grau 2) não é
  removível no começo (2·7 > 12), mas depois de tirar o isolado 2 passa a ser
  (2·6 ≤ 12).
- 500 grafos aleatórios com n ≤ 14: H ≠ ∅, m_H é o número de arestas induzidas,
  δ(H) > grau_medio(H)/2, grau_medio(H) ≥ grau_medio(G) (com `Fraction`), m_F/n_F nunca
  diminui ao longo do log, cada removido satisfazia d ≤ m_F/n_F e vale o Corolário 2.9.
- A versão ingênua (varre todos os vivos a cada passo) devolve o mesmo H e o mesmo log.
  Outra regra (remover o removível de menor rótulo) pode dar outro H, mas com as mesmas
  propriedades.
- Conferência com `networkx` (`G.subgraph(H)`).

## Figuras

- `subgrafo_H.png`: H em verde. Os removidos ficam em cinza, com a ordem de remoção
  (#1, #2, ...); caudas e pendentes saem primeiro.
- `densidade.png`: no caso "limiar sobe", m_F/n_F só sobe, e o grau de cada removido fica
  abaixo da curva ou sobre ela.
- `tempo_nucleo.png`: a inclinação medida foi **1,23** (esperado ≈ 1, O((n+m) log n)).

## Saídas

Em `saidas/` está a saída de cada grafo da tabela.
