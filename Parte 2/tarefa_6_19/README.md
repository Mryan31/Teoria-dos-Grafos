# Tarefa 6.19 - Edmonds–Karp para multigrafos dirigidos

## Como rodar

```
python edmonds_karp.py entradas/ex612.txt   # um arquivo
python edmonds_karp.py                      # todos os arquivos de entradas/, grava saidas/*.out
python testes.py
python graficos.py
```

## Entrada e saída

Entrada: primeira linha `n m s t`, depois `m` linhas `u v c` (arco u → v, capacidade
inteira ≥ 0) na ordem a1, ..., am. Vértices vão de 0 a n−1. Uma linha opcional
`f0 x1 ... xm` dá um fluxo inicial (usado só no Exemplo 6.12 (b)).

```
valor 2
fluxo 1 1 0 1 1
S 0
corte 2
```

`fluxo` tem um valor por arco original, na ordem da entrada. `S` são os vértices
alcançáveis a partir de s na rede residual final, e `corte` = c(∂⁺(S)).

Interface: `edmonds_karp(n, arcos, s, t, f0=None) -> (valor, f, S, log)`, com
`log = [(comprimento do caminho, gargalo), ...]`.

## Modelagem

- O arco original k = (u, v, c) gera a entrada `2k` (direta, de u para v, capacidade
  residual c − f) e a entrada `2k+1` (reversa, de v para u, capacidade residual f). A
  parceira da entrada i é `i ^ 1`. Então f_k = `cap[2k+1]`, sem estrutura extra.
- Arcos paralelos e opostos viram pares independentes. Não existe matriz n × n.
- `pred[v]` guarda o índice da entrada, e não o vértice, porque com arcos paralelos o
  vértice não identifica a entrada.
- BFS FIFO, com a adjacência na ordem de criação das entradas. A BFS que não alcança t é
  completa, e o que ela visitou é o S.
- Laços, s = t, capacidade negativa e vértice fora de [0, n) levantam erro.

## O que foi testado (`testes.py`)

- Tabela: ex612, ex612 com f0, clrs (valor 23), paralelos, antiparalelos, capacidade
  zero, desconexo, diamante (M = 1000, só 2 aumentos) e "usa arco reverso". Em cada um
  são conferidos valor, f, S e o número de aumentos.
- Exemplo 6.12: (a) partindo de f = 0; (b) partindo do fluxo da figura, a BFS acha um
  único caminho, com entradas [2, 5, 6], que usa uma entrada reversa (índice ímpar);
  (c) os quatro lados da fonte têm capacidades 2, 3, 2, 2, e nos cortes mínimos f = c nos
  arcos que saem e f = 0 nos que entram.
- Em todo teste: `verificar()` (0 ≤ f ≤ c, conservação Mf = val(f)(e_s − e_t) e
  val(f) = c(∂⁺(S))), o invariante `cap[2k] + cap[2k+1] = c_k` depois de cada aumento,
  comprimentos de caminho não decrescentes e nº de aumentos ≤ nm.
- 500 redes aleatórias (n ≤ 7, m ≤ 14, c ∈ [0, 5], com paralelos e opostos): o mínimo da
  enumeração de todos os cortes é igual ao valor, S é minimizante e é o de menor
  cardinalidade. O valor bate com `networkx.maximum_flow_value`.
- Teste dos testes: removi o `cap[i ^ 1] += eps` numa cópia, e o teste do invariante
  falhou.

## Figuras

- `rede_fluxo.png`: a rede clrs com cada arco rotulado f/c, S em laranja e ∂⁺(S) em
  vermelho. Todo arco vermelho está cheio, os que entram em S têm f = 0, e
  12 + 7 + 4 = 23 = valor.
- `tempo_loglog.png`: redes aleatórias com m = 4n. A inclinação medida foi **1,07**, bem
  abaixo da cota O(nm²).
- `distancias.png`: o comprimento do caminho aumentante nunca decresce (Prop. 6.18), e o
  valor acumulado ao lado.
