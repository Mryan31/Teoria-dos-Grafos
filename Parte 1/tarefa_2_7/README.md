# Tarefa 2.7 - Havel–Hakimi

## Como rodar

```
python havel_hakimi.py entradas/s1_ex25.txt   # imprime e grava saidas/s1_ex25.out
python testes.py
python graficos.py
```

## Entrada e saída

Entrada: uma linha com n inteiros em qualquer ordem. O vértice i é o i-ésimo número.
Graus negativos são rejeitados na leitura. A lista vazia é tratada como gráfica (grafo
vazio).

Saída: `GRAFICA` ou `NAO GRAFICA`, uma linha `passo k:` para cada sequência visitada e,
no fim, as arestas da realização (`v-u`, com v o pivô do passo) ou a obstrução.

```
entrada: 4 4 3 2 1 0
NAO GRAFICA
passo 0: 4 4 3 2 1 0
passo 1: 3 2 1 0 0
obstrucao: passo 1, entrada negativa (vertice 5)
```

## Desempate e obstrução

- A lista corrente guarda pares `(grau, rótulo)` e é reordenada a cada passo por
  (grau decrescente, rótulo crescente). O rótulo acompanha o grau, então a realização
  respeita a ordem da entrada mesmo quando ela vem fora de ordem (ex.: `2 1 1 2`).
- **Primeira obstrução**: é o primeiro passo k em que (a) o grau r do pivô é ≥ ao tamanho
  da lista corrente (`r >= n`), ou (b) ao subtrair 1 dos r seguintes algum grau fica
  negativo (`entrada negativa`, informando o vértice).
- Antes de imprimir, o programa confere com `assert` que a realização tem exatamente os
  graus pedidos, sem laços nem arestas repetidas.

## O que foi testado (`testes.py`)

- Tabela do guia: 8 sequências gráficas e 5 não gráficas, incluindo as cadeias do
  Exemplo 2.5 e do Exercício 2.6.
- Exaustivo para n = 1..7: em toda sequência não crescente com entradas em {0..n-1},
  Havel–Hakimi aceita ⇔ Erdős–Gallai aceita. As contagens foram 1, 2, 4, 11, 31, 102, 342,
  e o resultado também coincide com `nx.is_graphical` (métodos `hh` e `eg`).
- Força bruta para n ≤ 6: as sequências de graus de todos os 2^C(n,2) grafos são
  exatamente as aceitas.
- Sensibilidade: a versão que não reordena rejeita **32** sequências gráficas com n ≤ 6,
  a menor delas (2, 2, 1, 1). Por isso a reordenação é essencial.
- Permutar a entrada não muda a decisão, e soma ímpar nunca é gráfica.

## Figuras

- `realizacoes.png`: as realizações de três sequências, todas com vértices verdes (grau
  desenhado = grau pedido).
- `contagem_graficas.png`: as barras HH e EG são idênticas (2, 4, 11, 31, 102, 342).
- `tempo_hh.png`: a inclinação medida foi **1,99**, que corresponde a O(n² log n) por
  causa da reordenação a cada passo.

## Saídas

Em `saidas/` está a saída de todas as entradas da tabela, incluindo as quatro sequências
do Exemplo 2.5 e do Exercício 2.6 (`s1_ex25`, `s3_nao`, `s5_nao`, `s6_nao`).
