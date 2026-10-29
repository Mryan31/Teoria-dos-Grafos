# Tarefa 3.8 - Imersão de uma árvore em G com δ(G) ≥ |V(T)| − 1

## Como rodar

```
python imersao_arvore.py entradas/p4_k5.txt   # imprime e grava saidas/p4_k5.out
python testes.py
python graficos.py
```

## Entrada e saída

T e G ficam no mesmo arquivo, com rótulos independentes:

```
t r           <- tamanho da arvore e a raiz
(t-1 linhas com as arestas de T, rotulos 1..t)
n m x         <- G e o vertice prescrito
(m linhas com as arestas de G, rotulos 1..n)
```

Saída:

```
ordem: 1 2 3 4
pai: 2->1 3->2 4->3
phi: 1->3 2->1 3->2 4->4
livres por passo (i=2..t): 4 3 2
```

O programa também imprime δ(G) e t − 1, e avisa quando a hipótese não vale. Nesse caso
ele continua e, se faltar vizinho, mostra em que passo falhou.

## Como funciona

1. **Ordem de crescimento** (Proposição 3.6): enquanto sobrar mais que r, remove a folha
   de menor rótulo diferente de r e guarda como `pai` o único vizinho dela que ainda não
   foi removido. A ordem é `[r]` seguida das remoções invertidas.
2. **Imersão** (Corolário 3.7): φ(r) = x. Para cada u_i (i ≥ 2), φ(u_i) é o menor vizinho
   de φ(pai(u_i)) em G que ainda não foi usado.

**Livres** é quantos vizinhos de φ(pai(u_i)) ainda estavam livres no passo i. Pela prova,
esse número é sempre ≥ t − i + 1 ≥ 1 quando δ(G) ≥ t − 1.

Desempates: folha de menor rótulo na remoção e menor vizinho livre na imersão. O programa
chama `verifica_ordem` e `verifica_imersao` (injetiva, φ(r) = x, arestas preservadas)
antes de imprimir.

## O que foi testado (`testes.py`)

- As 13 linhas da tabela, incluindo t = 1, t = 2 e o caso com a hipótese violada (estrela
  no caminho 1-2-3-4-5, que falha no passo i = 3). Nesse caso o `GraphMatcher` do networkx
  confirma que realmente não existe cópia da estrela.
- Exaustivo: todas as árvores rotuladas com t ≤ 6 (contagem 1, 1, 3, 16, 125, 1296),
  todas as raízes e G aleatório com δ(G) ≥ t − 1 e n ∈ {t, t+1, t+2}. Foram 25.431
  combinações e nenhuma falhou. Em todas valem a folga livres ≥ t − i + 1, os prefixos
  da ordem conexos e um único vizinho anterior igual ao pai.
- 300 casos aleatórios conferidos com networkx (a imagem é árvore e é isomorfa a T).

## Figuras

- `imersao.png`: a cópia de P4 dentro do grafo de Petersen (arestas vermelhas), com a raiz
  no vértice prescrito x = 6 (amarelo).
- `folga.png`: em 5 grafos aleatórios com δ ≥ 8 (t = 9), o número de vizinhos livres fica
  sempre sobre a reta t − i + 1 ou acima dela.
- `ordem.png`: a árvore binária com a raiz na folha 4; cada vértice se pendura num vizinho
  de posição menor.

## Saídas

Em `saidas/` está a saída de cada linha da tabela.
