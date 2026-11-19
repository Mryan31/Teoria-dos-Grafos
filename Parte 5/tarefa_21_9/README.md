# Tarefa 21.9 - Simetrização com certificado

## Como rodar

```
python simetrizacao.py < entradas/misto_r2.txt
python simetrizacao.py -v < entradas/misto_r2.txt     # mostra também cada operação
python testes.py
python graficos.py        # grava figuras/fig1_simetrizacao.png, fig2_arestas.png, fig3_tempo.png
```

## Entrada e saída

Vértices 0..n−1. Primeira linha `n m r`, depois `m` linhas `u v`. O grafo tem que ser
simples e ter pelo menos t_r(n) arestas.

```
entrada            saída (-v)
6 9 2              arestas 9 tr 9
0 2                operacoes 2
0 3                caso 2 1<-0 4<-0 m 10
0 5                caso 1 3<-2 m 11
1 2                clique 0 2 5
1 4
1 5
2 5
3 4
4 5
```

A última linha é o certificado: `clique v1 ... v_{r+1}` (uma K_{r+1} em G) ou
`turan P1 | P2 | ...` (as partes de G ≅ T_r(n)). Com `-v`, cada operação aparece como
`caso c x<-y ... m M`: x virou cópia de y, e M é o número de arestas depois da operação.
Entrada ruim gera uma linha e código de saída 1:

- `ERRO poucas-arestas m < t`: menos de t_r(n) arestas;
- `ERRO nao-simples`: laço ou aresta repetida;
- `ERRO r < 1`.

## Como funciona

- O grafo fica numa matriz de adjacência `A` (n × n) com os graus em `grau[]`, porque a
  operação de cópia reescreve uma linha inteira.
- **Cópia** `copia(A, grau, x, y)`, com x e y não adjacentes: x perde suas arestas e passa
  a ser adjacente a N(y). Como y ∉ N(y), x continua não adjacente a y. O número de arestas
  muda de d(y) − d(x). Custo O(n).
- **Busca da tripla** `classes(n, A)`: tenta separar V nas classes da relação "não
  adjacente". Pega o menor vértice v ainda sem classe e junta a ele todos os vértices sem
  classe não adjacentes a v. Depois confere que cada classe é independente e que entre
  classes diferentes está tudo ligado. Se der certo, G é multipartido completo e as classes
  são as partes. Se falhar, sai uma tripla (a, v, b) com a ≁ v, v ≁ b e a ∼ b:
  - dois vértices a, b da classe de v adjacentes entre si: (a, v, b);
  - u de uma classe anterior (representante w) não adjacente a x de uma classe depois:
    x ∼ w (senão x teria entrado na classe de w), então u ≠ w e a tripla é (w, u, x).

  Custo O(n²).
- **Operação** (a prova): com a tripla (a, v, b),
  - caso 1: se d(v) < d(a), v vira cópia de a; senão, se d(v) < d(b), v vira cópia de b.
    As arestas sobem d(a) − d(v) ≥ 1 (ou d(b) − d(v) ≥ 1);
  - caso 2: se d(v) ≥ d(a) e d(v) ≥ d(b), a e b viram cópias de v. A primeira cópia muda
    d(v) − d(a) ≥ 0. Depois dela a não é mais vizinho de b (porque v ≁ b), então b perdeu
    uma aresta e a segunda cópia muda d(v) − (d(b) − 1) ≥ 1. No total sobe
    2d(v) − d(a) − d(b) + 1 ≥ 1.

  Cada operação vai para o log com as cópias na ordem em que foram feitas. Um `assert`
  confere que m subiu estritamente e que bate com Σ grau / 2.
- O laço repete até `classes` não achar tripla. Aí a não adjacência é uma relação de
  equivalência e G virou multipartido completo, com as classes como partes.
- Se houver pelo menos r + 1 partes, a clique é o menor vértice de cada uma das r + 1
  primeiras partes, e `desfaz` volta pelas cópias de trás pra frente trocando x por y
  sempre que a cópia x estiver na clique. No fim, um `assert` confere a clique em G.
- Se houver no máximo r partes, `certifica_turan` confere que G é exatamente o multipartido
  completo dessas partes, com os tamanhos de T_r(n).

**Regra de desempate**: v = menor vértice sem classe; a tripla é a primeira violação
encontrada na ordem descrita acima; no caso 1 testa a antes de b; a clique usa o menor
vértice de cada parte, com as partes em ordem do menor vértice.

## Provas

**Recuperação da clique.** Seja G' o grafo depois da cópia "x vira cópia de y" e Q uma
clique de G'. As arestas que não tocam x são as mesmas em G e G'.
- Se x ∉ Q, Q só usa arestas que não tocam x, e é clique em G.
- Se x ∈ Q, então y ∉ Q, porque x ≁ y em G'. Os outros vértices de Q são vizinhos de x
  em G', ou seja, estão em N_G(y). Entre eles as arestas são as mesmas de G. Então
  Q − x + y é clique em G, com o mesmo tamanho.

Fazendo isso cópia por cópia, da última pra primeira (no caso 2, primeiro desfaz a cópia
de b e depois a de a), a clique de ordem r + 1 do grafo final vira uma clique de ordem
r + 1 em G. Escolher um vértice de cada parte dá uma clique no final, porque partes
diferentes estão completamente ligadas.

**Quando termina.** Se não há tripla a ≁ v ≁ b com a ∼ b, a relação "u = w ou u ≁ w" é
transitiva, e então é de equivalência (reflexiva e simétrica sempre). Vértices na mesma
classe não são adjacentes e de classes diferentes são, então G é multipartido completo.

**No máximo r partes ⇒ nenhuma operação e G ≅ T_r(n).** Primeiro: um multipartido
completo com no máximo r partes tem no máximo t_r(n) arestas, e só T_r(n) chega lá.
- Se duas partes têm tamanhos p ≥ q + 2, passar um vértice da maior pra menor muda as
  arestas de (p − 1) − q ≥ 1.
- Se há menos de r partes não vazias e alguma tem tamanho ≥ 2, tirar um vértice dela
  numa parte nova soma p − 1 ≥ 1 arestas.

Então o máximo só é atingido com as partes balanceadas em r partes (com n < r, cada
vértice sozinho), que é T_r(n).

Agora, cada operação sobe pelo menos uma aresta, então m_final ≥ m0 + (nº de operações)
≥ t_r(n) + (nº de operações). Se o final tem no máximo r partes, m_final ≤ t_r(n). Logo o
nº de operações é 0, m0 = t_r(n), e G já era o grafo final: multipartido completo com no
máximo r partes e t_r(n) arestas, ou seja, G ≅ T_r(n), e as classes são a partição que
certifica isso.

**Tempo polinomial.** O número de arestas sobe estritamente a cada operação e nunca passa
de C(n,2), então há no máximo C(n,2) − m0 ≤ C(n,2) operações. Cada operação custa O(n²)
(busca da tripla) + O(n) (no máximo duas cópias). Total: O(n²) para montar a matriz +
C(n,2) · O(n²) = O(n⁴). O desfazer olha no máximo 2 · C(n,2) cópias com uma clique de r + 1
≤ n vértices: O(n³). A conferência final do certificado é O(n²).

## Testes (`testes.py`)

| arquivo | n, r | m / t_r(n) | operações | saída | passou |
|---------|------|-----------|-----------|-------|--------|
| c4_r2 | 4, 2 | 4 / 4 | 0 | turan 0 2 \| 1 3 | sim |
| k33_r2 (C6 + diagonais) | 6, 2 | 9 / 9 | 0 | turan 0 2 4 \| 1 3 5 | sim |
| t3_7_r3 (T_3(7) embaralhado) | 7, 3 | 16 / 16 | 0 | turan 0 3 5 \| 1 6 \| 2 4 | sim |
| k3_r5 (n < r) | 3, 5 | 3 / 3 | 0 | turan 0 \| 1 \| 2 | sim |
| vazio_r1 | 4, 1 | 0 / 0 | 0 | turan 0 1 2 3 | sim |
| k4_r3 | 4, 3 | 6 / 5 | 0 | clique 0 1 2 3 | sim |
| t3_7_mais_r3 (T_3(7) + aresta 1-6) | 7, 3 | 17 / 16 | 0 | clique 0 1 2 6 | sim |
| aresta_r1 | 3, 1 | 1 / 0 | 1 (caso 1) | clique 0 1 | sim |
| c5_cordas_r2 | 5, 2 | 7 / 6 | 1 (caso 1) | clique 0 1 2 | sim |
| caso2_r2 | 5, 2 | 6 / 6 | 1 (caso 2) | clique 0 2 4 | sim |
| k33_movida_r2 (K3,3 − 01 + 02) | 6, 2 | 9 / 9 | 1 (caso 2) | clique 0 2 3 | sim |
| misto_r2 | 6, 2 | 9 / 9 | 2 (caso 2, caso 1) | clique 0 2 5 | sim |
| triangulo_pendente_r2 | 4, 2 | 4 / 4 | 1 (caso 1) | clique 1 2 3 | sim |
| ruim_c5_r2 | 5, 2 | 5 / 6 | — | `ERRO poucas-arestas 5 < 6` | sim |
| ruim_laco, ruim_paralela | 3, 1 | — | — | `ERRO nao-simples` | sim |

O `triangulo_pendente_r2` (arestas 02, 12, 13, 23) é o exemplo pequeno em que desfazer
muda a clique: a tripla é (1, 0, 3), d(0) = 1 < d(1) = 2, então 0 vira cópia de 1 e fica
com N(0) = {2, 3}. O final tem partes {0, 1}, {2}, {3} e a clique 0 2 3; desfazendo
"0 <- 1", o 0 vira 1 e sai 1 2 3, que é o triângulo de G.

**Aleatórios**: 4000 grafos com n ≤ 10, r ≤ 5 e m sorteado entre t_r(n) e C(n,2), mais
1000 grafos de Turán com rótulos embaralhados (n ≤ 12), cada um também com uma aresta a
mais e com uma aresta movida (as propriedades rodaram em 5760 grafos). Em todos valeu:
- o grafo final é multipartido completo, m sobe estritamente e o nº de operações é
  ≤ C(n,2) − m0;
- quando sai clique, ela tem r + 1 vértices, é clique em G e ω(G) ≥ r + 1 (conferido com
  `networkx.find_cliques`);
- quando sai partição, ω(G) ≤ r, não houve operação e G é isomorfo a
  `networkx.turan_graph(n, r)`;
- Turán embaralhado sempre dá partição e Turán + 1 aresta sempre dá clique. Com uma
  aresta movida, 631 deram clique; os outros continuaram isomorfos a T_r(n) (ex.: em
  T_2(3) = P3, trocar ab por bc dá outra P3).

Cobertura: 3642 operações no caso 1 e 374 no caso 2; o desfazer trocou algum vértice da
clique em 983 grafos. A busca da tripla foi testada sozinha em 3000 grafos (a tripla
devolvida sempre tem a ≁ v ≁ b e a ∼ b).

## Figuras

- `fig1_simetrizacao.png`: o `misto_r2`. À esquerda G com a clique recuperada em vermelho;
  à direita o multipartido final (uma coluna por parte, cores = partes) depois de
  "1<-0 4<-0" (caso 2) e "3<-2" (caso 1).
- `fig2_arestas.png`: arestas depois de cada operação em 5 grafos aleatórios com n = 14 e
  r = 3, começando em t_3(14) = 65 ou um pouco acima. A escada só sobe e fica abaixo de
  C(14,2).
- `fig3_tempo.png`: tempo × n em log-log (r = 4, m0 = t_4(n)). O expoente medido foi
  **2,13**, bem abaixo da cota O(n⁴): o nº de operações feitas ficou muito longe de
  C(n,2) − m0 (46 contra 760 com n = 80), e a busca da tripla costuma parar cedo.
