# Tarefa 7.11 - Caminhos aumentantes em grafos bipartidos

## Como rodar

```
python bipartido.py entradas/escada.txt   # um arquivo
python bipartido.py                       # todos de entradas/, grava saidas/*.out
python testes.py
python graficos.py
```

## Entrada e saída

Entrada: `nA nB m` e depois `m` linhas `a b`, com 0 ≤ a < nA e 0 ≤ b < nB. Os índices de
A e de B são independentes (a0 e b0 são vértices diferentes). Arestas repetidas ou fora
do intervalo dão erro.

```
tamanho 4
M 0-1 1-0 2-2 3-3
RA -
RB -
K a0 a1 a2 a3
```

`M` lista os pares a-b. `RA`/`RB` são os vértices alcançados pela última busca (a que
falhou), ou `-` se vazios. `K` é a cobertura mínima.

## Interface (copiada pelas tarefas 10.10 e 10.18)

`emparelhamento_maximo(nA, nB, adj) -> (mateA, mateB, RA, RB, K)`

- `adj[a]` = lista ordenada dos vizinhos de a em B
- `mateX[v] = -1` se v está exposto
- `K` = lista de pares `('A', a)` / `('B', b)`

Funções auxiliares: `busca(nA, nB, adj, mateA, mateB) -> (caminho, RA, RB)`, com
`caminho = [a0, b1, a1, ..., bk]` ou `None`, e `aumenta(caminho, mateA, mateB)`.

## Como funciona

- Em cada iteração, **todos** os vértices expostos de A entram na fila como raízes.
- De a ∈ A só se usam arestas fora de M (ignora `b == mateA[a]`). De b ∈ B só se segue a
  aresta de M (`mateB[b]`). Isso é a orientação (7.3).
- Basta guardar `predB[b]`, o a de onde se chegou a b. A aresta pela qual um a foi
  alcançado sai de `mateA`.
- Ao achar b exposto, o caminho é reconstruído voltando até uma raiz (a com
  `mateA[a] == -1`), e `aumenta` alterna a pertinência das arestas do caminho.
- Quando a busca falha, ela esgota a fila: RA e RB são os vistos, e
  K = (A \ RA) ∪ RB (Teorema 7.15).
- Custo: uma busca O(|V| + |E|), no máximo min(|A|, |B|) aumentos.

**Convenção de ordem**: raízes em ordem crescente, vizinhos em ordem crescente, fila FIFO
e a busca para no primeiro b exposto. Com outra ordem, M e K podem mudar, mas ν e as
propriedades continuam valendo.

## O que foi testado (`testes.py`)

- As 12 linhas da tabela: P6, P7, C6, C8, K3,3, K2,3, K3,2, isolados, sem arestas,
  caminho longo, escada e Hall violado. Em cada uma são conferidos ν, M, RA, RB, K e o
  nº de aumentos.
- Na escada, os caminhos de cada iteração: [0,0], [2,1], [3,2] e, na 4ª,
  [1,0,0,1,2,2,3,3] (comprimento 7).
- Em todo teste: M é emparelhamento (mateA e mateB inversos, arestas existem), toda
  aresta tem extremo em K, |K| = |M|, e depois de cada aumento |M| sobe exatamente 1 com
  os dois extremos do caminho saturados.
- 1000 grafos aleatórios (nA, nB ∈ [0, 6], p = 0,35), comparados com força bruta (m ≤ 12),
  com a fórmula (7.2) ν = |A| − max(|S| − |N(S)|) e com
  `networkx.bipartite.hopcroft_karp_matching`.
- Bordas: nA = 0, nB = 0, sem arestas e vértices isolados em A (ficam em RA e fora de K).

## Figuras

- `aumento.png`: a escada antes e depois da última iteração. O caminho a1 b0 a0 b1 a2 b2
  a3 b3 alterna entre fora e dentro de M, e |M| sobe 1.
- `certificado.png`: no "Hall violado", K em vermelho e RA ∪ RB com borda preta. Toda
  aresta tem uma ponta vermelha, e cada aresta azul tem exatamente uma.
- `tempo_loglog.png`: com |A| = |B| = n e grau 4 em A, a inclinação medida foi **1,99**,
  dentro da cota O(n(n + m)).
