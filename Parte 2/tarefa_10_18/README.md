# Tarefa 10.18 - Partição mínima em cadeias e anticadeia máxima (Dilworth)

## Como rodar

```
python dilworth.py entradas/ex1015.txt   # um arquivo
python dilworth.py                       # todos de entradas/, grava saidas/*.out
python testes.py
python graficos.py
```

## Entrada e saída

```
n m
nome1 nome2 ... nome_n
x y        <- m linhas, cada uma significa x < y
```

As relações podem ser comparações quaisquer ou só os arcos de um DAG, porque o programa
calcula o fecho. Repetições e relações redundantes são ignoradas. Ciclo, relação x < x
ou nome desconhecido dão erro.

```
cadeias 2
a c e
b d f
largura 2
T e f
M a-c b-d c-e d-f
K a- b- c- d-
```

`M` lista os pares x-y da aresta x⁻y⁺. Em `K`, `x-` é x⁻ e `y+` é y⁺.

Interface: `dilworth(elementos, relacoes) -> (cadeias, T, M, K)`.

## Emparelhamento copiado da 7.11

`emparelhamento_maximo(nA, nB, adj)` foi copiada da tarefa 7.11 para o começo de
`dilworth.py`, junto com `busca` e `aumenta`, sem alterações. Aqui A = P⁻, B = P⁺ e
nA = nB = n. Não existe `import` de outra pasta.

## Algoritmo

1. **Fecho transitivo** (Warshall, O(n³)) das relações dadas. Se R[i][i] fica verdadeiro,
   há ciclo e não é ordem parcial.
2. **B_P**: aresta i⁻ — j⁺ para **toda** comparação estrita x_i < x_j (não só o diagrama
   de Hasse).
3. **(M, K)** por `emparelhamento_maximo`. Pelo Teorema 7.15, K = (A \ RA) ∪ RB é cobertura
   mínima com |K| = |M|.
4. **Cadeias** (Lema 10.13): se x_i⁻ x_j⁺ ∈ M, então j é o sucessor de i. Cada elemento sem
   predecessor (x⁺ livre em M) começa uma cadeia, que segue os sucessores. São n − |M|
   cadeias.
5. **Anticadeia** (Teorema 10.14): T = {x : x⁻ ∉ K e x⁺ ∉ K}.

O programa chama `verificar` sempre: as cadeias particionam P, pares consecutivos são
comparáveis, T é anticadeia, |T| = nº de cadeias = n − |M| e K cobre B_P com |K| = |M|.

## Nota: K e T diferentes do texto

O texto do Exemplo 10.15 mostra K = {a⁻, b⁻, e⁺, f⁺} e T = {c, d}. A cobertura da Aula 7,
que busca a partir dos expostos de A = P⁻ (e⁻ e f⁻ são raízes isoladas), devolve
K = {a⁻, b⁻, c⁻, d⁻} e, por isso, T = {e, f}. As duas são coberturas mínimas (tamanho 4)
e as duas anticadeias têm tamanho 2 = w(P). Em `testes.py`, `verificar_certificados`
aceita tanto os certificados do texto quanto os do programa.

## O que foi testado (`testes.py`)

- Tabela: Ex. 10.15, ordem total 1 < ... < 5, sem comparações (4 elementos), "N", B3,
  divisibilidade em {1..12}, armadilha do DAG e relações redundantes/duplicadas. São
  conferidos cadeias, T, M e K.
- O fecho do Ex. 10.15 tem 10 pares, e o M é exatamente o do texto.
- Armadilha do DAG: com os arcos 0→2, 1→2, 2→3, 2→4, o programa devolve 2 cadeias
  (0 2 4 | 1 3, que usa 1 < 3 por transitividade), e não 3.
- 80 ordens aleatórias (n ∈ [3, 11], nomes embaralhados): nº de cadeias = |T| = largura
  por força bruta = maior anticadeia de `nx.algorithms.dag.antichains`; o fecho bate com
  `nx.transitive_closure`; T calculado de duas formas (fora de K, e x⁻ ∈ RA e x⁺ ∉ RB);
  cadeias crescentes na ordem.
- Erdős–Szekeres: em 100 sequências de rs + 1 números distintos, sempre há cadeia ≥ r + 1
  ou anticadeia ≥ s + 1.
- Bordas: n = 0 (0 cadeias, T = ∅), n = 1, ciclo, x < x, nome desconhecido.

## Figuras

- `hasse.png`: o diagrama de Hasse do Ex. 10.15 colorido por cadeia, com T de borda
  preta. As cadeias cobrem todos os pontos e T tem um elemento em cada cadeia.
- `BP.png`: B_P com todas as comparações estritas, M em azul e K em vermelho. Toda aresta
  tem uma ponta vermelha, e |M| = |K| = 4, dando 6 − 4 = 2 cadeias.
- `largura.png`: nº de cadeias × largura em 80 ordens aleatórias. Todos os pontos ficam na
  diagonal.
