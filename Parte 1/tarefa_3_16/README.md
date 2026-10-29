# Tarefa 3.16 - Codificação e decodificação de Prüfer

## Como rodar

```
python prufer.py cod entradas/arvore_3_12.txt   # grava saidas/arvore_3_12_cod.out
python prufer.py dec entradas/codigo_3_12.txt   # grava saidas/codigo_3_12_dec.out
python testes.py
python graficos.py
```

## Formatos

- **Codificar**: o arquivo tem `n` e depois `n − 1` linhas `u v`. A saída tem uma linha
  com a1 ... a_{n−2} (vazia se n = 2) e outra com as folhas removidas x1 ... x_{n−2}.
- **Decodificar**: o arquivo tem uma linha com a1 ... a_{n−2} (n = tamanho + 2). A saída
  são as n − 1 arestas `u v` com u < v, em ordem lexicográfica.

Exemplo 3.12: a árvore 1-4, 3-4, 4-2, 2-6, 5-6, 6-7 vira `4 4 2 6 6` (folhas 1 3 4 2 5),
e a decodificação de `4 4 2 6 6` devolve a mesma árvore.

## Como funciona e complexidade

- **Codificar** (Definição 3.11): `adj[v]` é um conjunto, então o grau é `len(adj[v])`.
  As folhas atuais ficam num `heapq`. Repete n − 2 vezes: tira a menor folha x, registra
  o único vizinho a e apaga x. Se a passar a ter grau 1, entra no heap.
- **Decodificar** (Teorema 3.13): `mult[v]` = número de ocorrências de v no sufixo
  corrente. Os vértices com `mult = 0` ficam num `heapq`. No passo i liga a menor folha
  x_i a a_i, decrementa `mult[a_i]` e, se zerar, a_i vira folha. No fim sobram
  exatamente dois vértices no heap, que são ligados.
- Dois fatos da prova explicam por que as duas rotinas são inversas passo a passo:
  (i) no estágio i, deg(v) = 1 + (ocorrências de v no sufixo), então as folhas são os
  rótulos ativos ausentes do sufixo; (ii) as duas rotinas escolhem sempre a menor delas.
- Cada vértice entra e sai do heap O(1) vezes, a O(log n) cada: total **O(n log n)**.

O codificador valida a entrada antes (n − 1 arestas, sem ciclo, rótulos em 1..n), e o
decodificador rejeita valores fora de 1..n. Para n = 1 a entrada é rejeitada.

## O que foi testado (`testes.py`)

- As duas tabelas do guia (8 árvores e 8 códigos).
- Exaustivo para n = 2..7: as árvores foram enumeradas de forma independente
  (subconjuntos de arestas de K_n sem ciclo, por union-find), com contagem
  1, 3, 16, 125, 1296, 16807 = n^(n−2) (Cayley). Para toda palavra a,
  decodificar(a) está na lista e codificar(decodificar(a)) = a. Para toda árvore T,
  decodificar(codificar(T)) = T. Os n^(n−2) códigos são distintos.
- deg_T(v) = 1 + ocorrências de v no código, em 300 árvores aleatórias.
- networkx: em 300 árvores aleatórias (n ≤ 30, com rótulos embaralhados), comparação com
  `to_prufer_sequence` e `from_prufer_sequence`, somando e subtraindo 1 nos rótulos.
- Entradas inválidas (ciclo, desconexa, número errado de arestas, código fora de 1..n)
  levantam erro.

## Figuras

- `prufer_arvore.png`: a árvore do Exemplo 3.12 com as folhas marcadas x1..x5 na ordem de
  remoção e os dois vértices finais em amarelo.
- `grau_vs_codigo.png`: para uma árvore aleatória com n = 40, as barras grau(v) e
  1 + ocorrências coincidem em todo v.
- `tempo_prufer.png`: inclinações medidas de **1,13** (codificar) e **1,20**
  (decodificar), coerentes com n log n.
