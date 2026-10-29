# Tarefa 5.21 - Prim com registro de S, ∂(S) e aresta escolhida

## Como rodar

```
python prim.py entradas/g1.txt 1     # raiz 1 (padrao); grava saidas/g1_r1.out
python prim.py entradas/g1.txt 4
python testes.py
python graficos.py
```

## Entrada e saída

Entrada: `n m` e `m` linhas `u v w` (pesos inteiros). O id da aresta é o número da linha.
A raiz vem como argumento (o padrão é 1).

```
passo 1: S={1} corte=[e1(1-2,4) e2(1-3,2)] escolhida=e2(1-3,2)
...
arvore: e2 e3 e4 e7 e9   peso=13
arvores geradoras: 55   MSTs: 1 (peso 13)   verificacao: OK
```

Cada entrada do corte é `e<id>(u-v,w)`, em ordem de id. A linha `passo k` é registrada
**antes** de S receber o novo vértice. A última linha (enumeração das MSTs) só aparece
quando m ≤ 12. Grafo desconexo dá `erro: grafo desconexo`.

## Modelagem

- `adj[v]` guarda tuplas `(peso, id, vizinho)`. Laços são ignorados, porque nunca cruzam
  o corte. Arestas paralelas ficam com ids diferentes.
- A fila é um `heapq` de `(peso, id, v)`: menor peso primeiro e, no empate, menor id. Como
  o id é único, o terceiro campo nunca é comparado. A remoção é preguiçosa: se v já está
  em S, a aresta saiu do corte e é descartada.
- O corte do log é recalculado por **varredura** de todas as arestas (exatamente uma ponta
  em S), sem usar a fila. Assim ele serve para auditar a fila: o programa faz `assert` de
  que a escolhida está no corte e tem o peso mínimo dele.
- Custo do Prim O(m log n). O registro custa O(nm), por isso `registrar=False` nas
  medições de tempo.
- `msts` enumera todas as combinações de n − 1 ids, guarda as acíclicas (union-find) e
  fica com as de menor peso. `verifica_prop_5_20` confere que, para todo k, alguma MST
  contém as k primeiras arestas escolhidas.

## O que foi testado (`testes.py`)

- As 9 linhas da tabela: G1 com r = 1 e r = 4, triângulo, K4 com tudo 1, quadrado +
  diagonal, paralelas, laço, K4 com pesos e grafo desconexo. Também n = 1.
- Em cada etapa: |S_k| = k, corte igual ao recalculado, escolhida no corte com peso
  mínimo, F árvore geradora de peso mínimo e Proposição 5.20.
- Desempate aleatório: em 300 grafos com n ≤ 6, m ≤ 11 e pesos em {1, 2, 3}, 5 execuções
  cada, escolhendo ao acaso entre as arestas mínimas do corte. Resultado: **0 violações
  em 1500 execuções**.
- Teste do teste: a regra errada "escolher a mais pesada do corte" foi reprovada pelo
  verificador em **89%** das instâncias (o guia mediu 82% com outros grafos).
- networkx: o peso coincide com `minimum_spanning_tree` e não muda com a raiz.

## Figuras

- `prim_passos.png`: os 5 passos de Prim em G1 (S em verde, árvore em azul, corte em
  vermelho, escolhida em verde grosso). Em cada painel a escolhida é a mais leve das
  vermelhas.
- `corte_minimo.png`: em todas as etapas de 40 instâncias aleatórias, o peso da escolhida
  é igual ao mínimo do corte, então todos os pontos caem na diagonal.
- `tempo_prim.png`: a inclinação medida foi **1,32** (m ≈ 5n; o guia espera entre 1 e 1,3 e mediu 1,3, contando
  o custo de alocação do Python).

## Saídas

Em `saidas/` está o log completo de G1 com r = 1 e r = 4, e o dos casos com empate.
