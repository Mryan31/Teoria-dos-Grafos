# Tarefa 24 P6 - Retirar a aleatoriedade do corte

## Como rodar

```
python corte.py < entradas/petersen.txt
python corte.py -v < entradas/petersen.txt     # mostra também a esperança a cada vértice
python testes.py
python graficos.py        # grava figuras/fig1_petersen.png, fig2_esperanca.png, fig3_aleatorias_tempo.png
```

## Entrada e saída

Vértices 0..n−1. Primeira linha `n m`, depois `m` linhas `u v`. Arestas paralelas são
aceitas (cada uma conta no corte); laço dá `ERRO laco` e código de saída 1, porque um laço
nunca está no corte e aí a cota m/2 não vale.

```
entrada            saída (-v)
4 4                corte 4
0 1                m 4
1 2                lados 0 1 0 1
2 3                esperanca 2 2 2.5 3 4
3 0
```

`lados` dá o lado (0 ou 1) de cada vértice, e a partição é {v : lado 0} e {v : lado 1}.
Com `-v`, a linha `esperanca` traz E[corte | fixados] depois de fixar 0, 1, ..., n vértices.

## Como funciona

- Listas de adjacência `adj[v]` (com repetição se houver paralelas).
- Os vértices são fixados na ordem 0..n−1 (`corte_guloso` aceita outra `ordem`). Para v,
  percorre `adj[v]` contando quantos vizinhos já fixados estão em cada lado (c0, c1) e põe
  v no lado oposto à maioria: lado 1 se c0 > c1, senão lado 0 (empate vai pro 0).
- Mantém dois contadores: `garantidas` (arestas com as duas pontas fixas em lados
  diferentes) e `abertas` (arestas com pelo menos uma ponta livre). Ao fixar v, as
  c0 + c1 arestas para vizinhos fixos fecham; as que foram para o outro lado entram em
  `garantidas`.
- A esperança condicional é `garantidas + abertas/2`. Guardo o dobro dela (`E2`) pra ficar
  em inteiro, e um `assert` confere que ela nunca cai.
- No fim todo mundo está fixo, abertas = 0 e a esperança é o próprio corte. O `main`
  recalcula o corte direto da lista de arestas (`tamanho_corte`) e confere 2·corte ≥ m.

## Provas

**(a) Esperança condicional.** Seja F o conjunto de vértices já fixados e os outros
escolhidos por moedas independentes e honestas. Pela linearidade,
E[corte | F] = Σ_e P(e no corte | F).
- Se as duas pontas de e estão em F, a probabilidade é 1 se estão em lados diferentes e 0
  se não; somando, dá o número de arestas já garantidas no corte.
- Se alguma ponta u de e está livre, condicionando no lado da outra ponta (fixo ou
  sorteado, independente da moeda de u), u cai no lado oposto com probabilidade 1/2.

Então E[corte | F] = (garantidas) + ½ · (arestas com pelo menos uma ponta livre).
Com F = ∅ isso é m/2, que é a prova original do corte.

**(b) Uma das escolhas não diminui.** A moeda do próximo vértice v é honesta e independente,
então E[corte | F] = ½ E[corte | F, v → 0] + ½ E[corte | F, v → 1], e o maior dos dois é
≥ E[corte | F]. Pra ver qual: sejam c_s os vizinhos de v já fixados no lado s. Ao pôr v no
lado s, as arestas de v para vizinhos livres continuam valendo ½; as c_{1−s} para o outro
lado passam de ½ para 1; as c_s para o mesmo lado passam de ½ para 0. A variação é
(c_{1−s} − c_s)/2, que é ≥ 0 exatamente quando c_{1−s} ≥ c_s, isto é, quando v vai para
o lado oposto à maioria dos vizinhos já posicionados.

Como a esperança começa em m/2 e nunca cai, quando todos estão fixos ela vale o corte
(sem moedas, a esperança é o próprio valor), e então corte ≥ m/2.

**(c) Tempo O(n + m).** Montar as listas custa O(n + m). Cada vértice é fixado uma vez, e
sua lista é percorrida uma vez com O(1) por item (olhar `lado[w]`, somar no contador).
Como Σ deg(v) = 2m, a varredura toda custa O(n + 2m), e atualizar `garantidas`, `abertas`
e `E2` é O(1) por vértice. Total O(n + m). Nos testes o número de itens examinados é
exatamente 2m.

## Testes (`testes.py`)

| arquivo | m | corte | lados | esperança (×2) | máximo | passou |
|---------|---|-------|-------|----------------|--------|--------|
| k3 | 3 | 2 | 0 1 0 | 3 3 4 4 | 2 | sim |
| c4 | 4 | 4 | 0 1 0 1 | 4 4 5 6 8 | 4 | sim |
| c5 | 5 | 4 | 0 1 0 1 0 | 5 5 6 7 8 8 | 4 | sim |
| p5 | 4 | 4 | 0 1 0 1 0 | 4 4 5 6 7 8 | 4 | sim |
| k4 | 6 | 4 | 0 1 0 1 | 6 6 7 7 8 | 4 | sim |
| k5 | 10 | 6 | 0 1 0 1 0 | 10 10 11 11 12 12 | 6 | sim |
| k33 | 9 | 9 | 0 0 0 1 1 1 | 9 9 9 9 12 15 18 | 9 | sim |
| estrela (K1,5) | 5 | 5 | 0 1 1 1 1 1 | 5 5 6 7 8 9 10 | 5 | sim |
| cubo (Q3) | 12 | 12 | 0 1 1 0 1 0 0 1 | 12 12 13 14 16 17 19 21 24 | 12 | sim |
| petersen | 15 | 12 | 0 1 0 1 0 1 0 0 0 1 | 15 15 16 17 18 18 19 20 20 21 24 | 12 | sim |
| paralelas (01 três vezes, 12) | 4 | 4 | 0 1 0 | 4 4 7 8 | 4 | sim |
| sem_arestas | 0 | 0 | 0 0 0 0 | 0 0 0 0 0 | 0 | sim |
| p4_ordem_ruim (0-2-3-1) | 3 | 2 | 0 0 1 0 | 3 3 3 4 4 | 3 | sim |
| ruim_laco | — | — | — | `ERRO laco` | — | sim |

O "máximo" é o corte máximo por força bruta. O `p4_ordem_ruim` é um caminho 0-2-3-1: o 1
é fixado antes de ter vizinho fixo (vai pro lado 0) e depois o 3 empata, também vai pro
0, e a aresta 3-1 fica fora. O método garante m/2, não o ótimo.

**Itens (a) e (b) por enumeração**: em 300 grafos aleatórios (n ≤ 8, ordem embaralhada),
para cada prefixo fixado calculei E[corte | fixados] fazendo a média sobre todas as
2^(livres) escolhas, e bateu com garantidas + abertas/2. Também conferi que a escolha
contrária à do algoritmo nunca dá esperança maior.

**Aleatórios**: 2000 grafos com n ≤ 12 (densidade sorteada, 20% com paralelas, metade
com ordem embaralhada). Em todos: 2·corte ≥ m, a esperança começa em m/2, nunca cai e
termina no corte, e foram examinados exatamente 2m itens. O guloso achou o corte máximo
em 1451 dos 2000; a pior razão corte/máximo foi 0,600.

**Comparação com partições aleatórias** (2000 partições com moedas por grafo):

| arquivo | guloso | m/2 | média aleatória | % aleatórias = guloso | % aleatórias > guloso | máximo |
|---------|--------|-----|-----------------|-----------------------|-----------------------|--------|
| k3 | 2 | 1,5 | 1,50 | 75,2 | 0,0 | 2 |
| c4 | 4 | 2,0 | 2,01 | 12,6 | 0,0 | 4 |
| c5 | 4 | 2,5 | 2,47 | 29,8 | 0,0 | 4 |
| p5 | 4 | 2,0 | 2,00 | 6,8 | 0,0 | 4 |
| k4 | 4 | 3,0 | 2,98 | 37,4 | 0,0 | 4 |
| k5 | 6 | 5,0 | 5,03 | 62,5 | 0,0 | 6 |
| k33 | 9 | 4,5 | 4,51 | 2,9 | 0,0 | 9 |
| estrela | 5 | 2,5 | 2,52 | 3,6 | 0,0 | 5 |
| cubo | 12 | 6,0 | 6,04 | 1,0 | 0,0 | 12 |
| petersen | 12 | 7,5 | 7,47 | 0,8 | 0,0 | 12 |
| paralelas | 4 | 2,0 | 2,02 | 24,9 | 0,0 | 4 |
| p4_ordem_ruim | 2 | 1,5 | 1,53 | 38,3 | 13,1 | 3 |

A média das partições aleatórias fica em m/2, como na prova. Nesses exemplos pequenos o
guloso chegou no máximo em todos menos no `p4_ordem_ruim`, e só lá alguma partição
aleatória foi melhor (13% delas acharam o 3).

## Figuras

- `fig1_petersen.png`: a partição do guloso no Petersen (laranja = lado 0, azul = lado 1),
  com as 12 arestas do corte em vermelho; 12 é o máximo do Petersen.
- `fig2_esperanca.png`: E[corte | fixados] a cada vértice fixado, no Petersen, no cubo e num
  aleatório com n = 30, m = 90. A escada começa em m/2, nunca desce e termina no corte.
- `fig3_aleatorias_tempo.png`: à esquerda, histograma de 5000 partições aleatórias num
  grafo com n = 40, m = 160 (concentradas em volta de m/2 = 80); o guloso deu 111 e
  nenhuma delas chegou lá. À direita, tempo × (n + m) em log-log com m = 3n: expoente
  medido **1,19**, perto de 1 (o desvio vem de cache/memória com listas grandes).
