# Tarefa 16.8 - De resíduos a um fluxo inteiro (Tutte, 16.6)

## Como rodar

```
python fluxo.py < entradas/ex16_7.txt
python testes.py
python graficos.py        # grava figuras/fig1_petersen.png, fig2_K.png, fig3_tempo.png
```

## Entrada e saída

Vértices 0..n−1. Primeira linha `n m k`, depois `m` linhas `pe cab val`: arco do pé `pe`
à cabeça `cab` (D tem +1 no pé e −1 na cabeça) e o valor em Z_k (qualquer inteiro; é
reduzido com `val % k`). Paralelos e laços são permitidos.

```
entrada            saída
2 3 3              K0 6
0 1 1              correcoes 1
0 1 1              f -2 1 1
0 1 1
```

Os valores de f saem na orientação **original**, na ordem das linhas. Entrada ruim gera
uma linha e código de saída 1:

- `ERRO valor-zero`: algum valor ≡ 0 (mod k);
- `ERRO conservacao v1 v2 ...`: vértices com b(v) ≢ 0 (mod k).

## Como funciona

- `pe`, `cab`, `val`: orientação e valor atuais (val sempre em 1..k−1); `virou[e]` é a
  paridade das inversões de e.
- b(v) = (soma dos valores dos arcos que saem de v) − (soma dos que entram), sem contar
  laços. K = Σ|b(v)|. Os dois são atualizados incrementalmente (b(s) −= k, b(t) += k,
  K −= 2k), e um `assert` compara com o recálculo do zero.
- `inc[v]` são listas de incidência estáticas. Na BFS só se segue e quando `pe[e] == u`,
  isto é, quando o arco sai de u na orientação atual. Assim a BFS custa O(n + m) sem
  reconstruir nada.
- Para cada correção: s = menor vértice com b(s) > 0, BFS em ordem crescente de id, para
  no primeiro w com b(w) < 0. O caminho P é invertido, cada arco troca val por k − val, e
  o caminho vai para o log.
- No fim, f[e] = −val[e] se `virou[e]`, senão val[e] (inverter o arco e negar o valor
  preserva o fluxo), e `confere` verifica (16.1) na orientação original.

**Regra de desempate**: s = menor vértice com b > 0; `inc[u]` em ordem crescente de id; a
BFS para ao descobrir o primeiro w com b(w) < 0.

**Por que a BFS sempre encontra t**: seja R o conjunto dos alcançáveis a partir de s.
Nenhum arco sai de R, então Σ_{v∈R} b(v) = −(soma dos arcos que entram em R) ≤ 0. Como
b(s) > 0, existe t ∈ R com b(t) < 0.

## Provas

**K(f) ≤ 2m(k − 1).**
(i) |b(v)| = |Σ_{pe(e)=v} f(e) − Σ_{cab(e)=v} f(e)| ≤ Σ_{e∋v, e não laço} f(e).
(ii) Somando sobre v, cada aresta que não é laço aparece duas vezes (uma por extremidade):
K(f) ≤ 2 Σ_e f(e).
(iii) Como 1 ≤ f(e) ≤ k − 1, K(f) ≤ 2m(k − 1).

**Menos de m correções.** Pela conservação modular, todo b(v) é múltiplo de k. Em cada
correção, b(s) é múltiplo positivo de k (logo ≥ k) e cai k; b(t) ≤ −k e sobe k; os
vértices internos de P não mudam (entra e sai a mesma troca de valor). Então K cai
exatamente 2k a cada correção, é sempre ≥ 0 e termina em 0. O número de correções é
c = K0/(2k) ≤ 2m(k − 1)/(2k) = m(k − 1)/k < m, se m ≥ 1.

**Tempo O(m(n + m)).** Montar b e `inc` custa O(n + m). Em cada correção: achar s em
O(n); a BFS em O(n + m) (cada vértice sai da fila uma vez e cada lista `inc` é percorrida
uma vez, com Σ deg = 2m); P tem ≤ n − 1 arestas, e inverter custa O(n). Total:
O(n + m) + c · O(n + m) = O(m(n + m)) operações aritméticas.

**Exercício 16.9.** Se G tem Z_k-circulação nunca zero, o Teor. 16.6 dá um k-fluxo inteiro
g (Dg = 0, 0 < |g(e)| < k ≤ ℓ). Reduzido módulo ℓ, g é uma Z_ℓ-circulação (Dg = 0) e
nunca zero, porque 0 < |g(e)| < ℓ implica g(e) ≢ 0 (mod ℓ). Ou seja: um k-fluxo é também
um ℓ-fluxo.

## Testes (`testes.py`)

| # | caso | K0 | correções | f | passou |
|---|------|----|-----------|---|--------|
| 1 | Ex. 16.7, k = 3 | 6 | 1: 0→1, [e0] | −2 1 1 | sim |
| 2 | C4, k = 3 | 6 | 1: 0→3, [e3] | 1 1 1 −1 | sim |
| 3 | C4, k = 2 | 4 | 1: 0→2, [e0, e1] | −1 −1 1 1 | sim |
| 4 | C5, k = 2 | 4 | 1: 0→4, [e4] | 1 1 1 1 −1 | sim |
| 5 | 4 arcos 0→1, k = 5 | 10 | 1: [e0] | −4 1 1 2 | sim |
| 6 | n = 2, k = 2, com laço | 4 | 1: [e0] | −1 1 1 | sim |
| 7 | K4, k = 4 (2,3,3,3,3,2) | 24 | 3; K = 16, 8, 0 | 2 −1 −1 3 −1 2 | sim |
| 8 | K4, k = 4 (3,2,3,1,2,3) | 16 | 2 | −1 2 −1 1 −2 3 | sim |
| 9 | Petersen, k = 5 | 30 | 3; K = 20, 10, 0 | 3 4 1 3 2 −2 1 1 −1 2 −1 −1 3 −2 1 | sim |
| — | ponte `0 1 1`, k = 3 | — | — | `ERRO conservacao 0 1` | sim |
| — | K4, k = 3, tudo 1 | — | — | `ERRO conservacao 1 2` | sim |
| — | valor 0 ou 3 com k = 3 | — | — | `ERRO valor-zero` | sim |

Também testei os representantes: (4, −2, 7) com k = 3 dá a mesma saída do caso 1.

**Aleatórios**: 3000 instâncias geradas por `gerar` (n ≤ 12, k ≤ 7), somando 6189
correções. Em todas valeram: (1) conservação modular na entrada e (16.1) na saída;
(2) f(e) ≡ val(e) (mod k); (3) K cai exatamente 2k e b(v) segue múltiplo de k;
(4) K0 ≤ 2m(k − 1), nº de correções = K0/(2k) < m; (5) reorientar um arco mantém uma
circulação válida e a nova saída também passa em (16.1).

**Teor. 16.10 (contagem)**: o número de Z_k-circulações nunca zero do K4 é 0, 6, 24 para
k = 3, 4, 5, e o do Petersen é 0 (k = 4) e 240 (k = 5). Cada uma delas levantou para um
k-fluxo. A contagem escolhe os valores das arestas fora de uma árvore geradora (o resto
fica determinado), em vez de testar todas as m arestas.

## Figuras

- `fig1_petersen.png`: Petersen (caso 9). À esquerda, os resíduos iniciais (laranja
  b > 0, azul b < 0) e o caminho da 1ª correção em vermelho; à direita, o fluxo final com
  b = 0 e 0 < |f| < 5.
- `fig2_K.png`: K em cada correção (Petersen e um aleatório com n = 30). Todos os degraus
  têm altura 2k = 10, sobre a reta de inclinação −2k, e K0 ≤ 2m(k − 1).
- `fig3_tempo.png`: tempo × m em log-log. O expoente medido foi **1,77** (esperado entre 1
  e 2). As operações contadas ficaram sempre abaixo de 0,007·m(n + m), ou seja, limitadas
  pela cota.
