# Tarefa 9.11 - Conectividade por arestas e por vértices via fluxo

## Como rodar

```
python conectividade.py entradas/dois_k4.txt        # consulta local no 1o par nao adjacente
python conectividade.py entradas/c6.txt 0 3         # consulta local no par (0, 3)
python testes.py
python graficos.py
```

## Entrada e saída

Entrada: `n m` e `m` linhas `u v` (grafo simples, vértices 0..n−1, n ≥ 2). Laços e
arestas repetidas são rejeitados.

```
kappa 2
lambda 3
delta 3
aresta 0 4: valor 3
  caminhos: 0-1-2-4 | 0-2-5-4 | 0-3-4
  corte: 0-1 0-2 0-3
vertice 0 4: valor 2
  caminhos: 0-2-4 | 0-3-4
  separador: 2 3
```

Interfaces:
- `conectividade_aresta(n, arestas, x, y) -> (valor, caminhos, corte)`
- `conectividade_vertice(n, arestas, x, y) -> (valor, caminhos, separador)`
- `lambda_G(n, arestas)`, `kappa_G(n, arestas)`

## Edmonds–Karp copiado da 6.19

A função `edmonds_karp(n, arcos, s, t, f0=None) -> (valor, f, S, log)` foi copiada da
tarefa 6.19 para o início de `conectividade.py`, com a mesma interface e as mesmas
entradas pareadas 2k/2k+1. A única mudança é que a cópia não usa a classe `Rede`, para
ficar numa função só. Não existe `import` de outra pasta. Como cada arco tem o seu par de
entradas, u → v e v → u são independentes, e é isso que o modelo de arestas precisa.

## Modelagem

- **Arestas** (Teorema 9.6): cada aresta k = {u, v} vira os arcos 2k = (u, v) e
  2k+1 = (v, u), com capacidade 1. Se os dois sentidos ficam com fluxo 1, os dois são
  zerados. O corte é F = arestas com exatamente uma ponta em S (os alcançáveis do resíduo
  final).
- **Vértices** (Teorema 9.7 / Cor. 9.8): v vira v⁻ = 2v e v⁺ = 2v+1. O arco central
  (v⁻, v⁺) tem capacidade 1 se v ∉ {x, y} e N = n + 1 em x e y. Cada aresta {u, v} vira
  (u⁺, v⁻) e (v⁺, u⁻) com capacidade N. A fonte é x⁻ e o sorvedouro y⁺. O separador é
  {v : v⁻ ∈ S, v⁺ ∉ S}. Se x e y são adjacentes, a função levanta erro.
- **Caminhos**: o fluxo 0/1 é decomposto andando de s pelos arcos com fluxo restante.
  Quando a caminhada repete um vértice, o ciclo é apagado. No modelo de vértices, o arco
  u⁺ → v⁻ é projetado em u → v.
- Como S é sempre o menor lado da fonte entre os cortes mínimos, corte e separador saem
  determinísticos.
- λ(G) = mínimo sobre todos os pares. κ(G) = n − 1 se G é completo; senão, o mínimo sobre
  os pares não adjacentes.

## O que foi testado (`testes.py`)

- Tabela global (κ, λ, δ conferidos com `node_connectivity`/`edge_connectivity`) e tabela
  local com caminhos, corte e separador iguais aos do guia, inclusive os pares adjacentes.
- Em todo caso: κ ≤ λ ≤ δ, |caminhos| = valor = |corte|, caminhos de x a y com arestas
  existentes, disjuntos em arestas (ou internamente disjuntos em vértices), e remover o
  corte/separador desconecta x de y.
- 400 grafos G(n, 0,45) com n ∈ [2, 7], incluindo desconexos (κ = λ = 0). Os tamanhos
  foram comparados com uma enumeração exaustiva (menor F e menor S, local e global), e
  λ fixando x = 0 deu o mesmo que todos os pares.
- Famílias: Pn e Cn até 12, Kn até 8, Kr,s (κ = λ = min(r, s)) e Qd até d = 4.
- Sanidade: com capacidade grande em todos os arcos centrais, o valor de κ(0, 4) no "dois
  K4" passa de 2 para 7, então o teste detecta o erro.

## Figuras

- `kappa_lambda_delta.png`: barras κ, λ, δ por grafo. Vale κ ≤ λ ≤ δ em todos, e o único
  caso com κ < λ é o "dois K4" (2 < 3 = 3).
- `separadores.png`: no "dois K4", par (0, 4). À esquerda, os 2 caminhos internamente
  disjuntos e o separador {2, 3}. À direita, os 3 caminhos disjuntos em arestas e o corte
  (as 3 arestas de 0). Cada separador corta cada caminho exatamente uma vez.
- `dispersao.png`: 150 grafos aleatórios. Nenhum ponto fica abaixo da diagonal em κ × λ
  nem em λ × δ.

## Saídas

Em `saidas/` estão as saídas de dois_k4, c6 (0, 3), q3 (0, 7), k23 (0, 1), p5 (0, 4),
k5, k33, petersen e dois triângulos.
