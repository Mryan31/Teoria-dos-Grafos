# Tarefa 4.7 - Hierholzer para multigrafos

## Como rodar

```
python hierholzer.py entradas/paralelas_e_laco.txt      # vertice inicial padrao
python hierholzer.py entradas/triangulo.txt 2           # comecando no vertice 2
python testes.py
python graficos.py
```

## Entrada e saída

Entrada: `n m` e `m` linhas `u v`. O **id** da aresta é o número da linha (1..m), e
`u = v` é um laço. Arestas paralelas são arestas diferentes, cada uma com seu id.

```
EULERIANO
vertices: 1 2 3 1
arestas: 1 2 3
```

Mensagens de rejeição, testadas nesta ordem:

- `sem arestas: nada a percorrer` (m = 0)
- `NAO EULERIANO: suporte desconexo`
- `NAO EULERIANO: graus impares em ...`

O vértice inicial padrão é o menor vértice de grau positivo.

## Modelagem

- `adj[v]` é uma lista de pares `(vizinho, id)` em ordem de id. Um laço u-u entra **duas
  vezes** em `adj[u]`, então conta 2 no grau. A segunda ocorrência é pulada depois porque
  o id já está usado.
- `usada[id]` marca por id, e não por par de vértices, para não fundir paralelas.
- `ptr[v]` é um cursor na lista de v que só anda para frente. Por isso o total é O(n + m).
- A pilha guarda `(vertice, id da aresta usada para chegar)`, e a pilha é explícita (sem
  recursão). Ao desempilhar, guarda o vértice e o id. No fim as duas listas são
  invertidas, e o id 0 do vértice inicial é descartado.
- Suporte conexo: uma busca a partir de um vértice de grau positivo precisa alcançar
  todos os vértices de grau positivo. Vértices isolados não atrapalham.

Antes de imprimir, o programa chama `verificar`: circuito fechado, cada id exatamente uma
vez e a aresta e_k ligando v_{k−1} a v_k.

## O que foi testado (`testes.py`)

- As 13 linhas da tabela (triângulo, paralelas, laço, oito, triângulo + laço, paralelas e
  laço, borboleta, início em 2, isolados, Königsberg, dois triângulos, caminho, sem
  arestas).
- Convenção do laço: no triângulo + laço em 1, o grau do vértice 1 é 4.
- 2000 multigrafos aleatórios (n ≤ 8) gerados como união de passeios fechados, todos com
  graus pares. Cerca de 84% saem com suporte conexo e os outros são rejeitados por
  desconexão. A decisão coincide com `nx.is_eulerian` no `MultiGraph` do suporte, e todo
  circuito passa por `verificar`.
- Perturbações: trocar uma ponta de uma aresta faz o grafo ser rejeitado, e acrescentar
  um triângulo disjunto faz ser rejeitado por suporte desconexo.

## Figuras

- `circuito.png`: o caso "paralelas e laço", com arcos separados para as paralelas e a cor
  dando a posição no circuito. Os 7 ids aparecem uma vez cada.
- `pilha.png`: tamanho da pilha num multigrafo euleriano aleatório (n = 60). Sobe nas
  excursões, desce ao desempilhar e termina em 0 depois de 2m + 1 = 801 iterações.
- `tempo_hierholzer.png`: a inclinação medida foi **1,18** (esperado ≈ 1, O(n + m)).

## Saídas

Em `saidas/` está a saída de cada caso da tabela, incluindo as rejeições
(`triangulo_s2.out` é o triângulo começando no vértice 2).
