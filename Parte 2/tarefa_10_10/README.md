# Tarefa 10.10 - Decomposição de Birkhoff–von Neumann

## Como rodar

```
python birkhoff.py entradas/ex108.txt   # um arquivo
python birkhoff.py                      # todos de entradas/, grava saidas/*.out
python testes.py
python graficos.py
```

## Entrada e saída

Entrada: `n` e depois n linhas com n números racionais, escritos como `a/b`, inteiros
ou decimais finitos (`0.25`). Tudo é lido como texto com `Fraction("...")`, nunca via
`float`.

```
termos 2
1/3 : 0 1 2
2/3 : 1 2 0
soma 1
```

Cada linha é `alfa : σ(0) σ(1) ... σ(n−1)`, com índices a partir de 0. A entrada é
validada antes: matriz quadrada, entradas ≥ 0 e somas exatamente 1. Se falhar, a
mensagem diz qual linha ou coluna está errada.

Interface: `birkhoff(X) -> (termos, hist)`, com `termos = [(alfa, sigma), ...]` e
`hist = [(entradas > 0 de R antes do passo, alfa, r depois do passo), ...]`.

## Emparelhamento copiado da 7.11

`emparelhamento_maximo(nA, nB, adj)` foi copiada da tarefa 7.11 para o começo de
`birkhoff.py`, junto com as duas auxiliares que ela chama (`busca` e `aumenta`), sem
alterações. Aqui nA = nB = n e `adj[i]` = colunas j com R[i][j] > 0, e só o `mateA` é
usado. Não existe `import` de outra pasta.

**Convenção** (é ela que faz as permutações saírem como na tabela): raízes em ordem
crescente de linha, colunas em ordem crescente e BFS FIFO, como na 7.11. A decomposição
não é única, então com outra ordem só as propriedades devem ser comparadas.

## Algoritmo (prova do Teorema 10.7)

R ← X, r ← 1. Enquanto r > 0: monta o grafo bipartido das posições positivas de R, acha
um emparelhamento perfeito σ (existe pelo argumento de Hall da prova; há um `assert`),
α = min R[i][σ(i)], R ← R − αP_σ, r ← r − α.

Tudo é exato com `Fraction`. Com `float`, a entrada que deveria zerar ficaria em 10⁻¹⁷ e
o emparelhamento perfeito deixaria de existir.

A cada passo o programa confere: R ≥ 0, todas as somas de linhas e colunas iguais a r e
pelo menos uma entrada positiva a menos. No fim confere R = 0, Σα = 1 e ΣαP_σ = X
exatamente.

## O que foi testado (`testes.py`)

- Tabela: Exemplo 10.8 (2 termos, 1/3 e 2/3), permutação, J/3, J/4 (4 termos de 1/4), I4,
  dois blocos, W4 e Z9 (5 termos, o máximo (n−1)² + 1 para n = 3). Os termos são iguais
  aos da tabela.
- Em todo teste: α > 0, Σα = 1, ΣαP = X exato, cada σ só usa posições positivas de R no
  momento do passo, entradas positivas estritamente decrescentes,
  q ≤ nz(X) − n + 1 ≤ n² e r termina em 0.
- Generalização (Ex. 10.9): 5·Z9, com todas as somas iguais a 5, dá Σα = 5.
- 300 matrizes aleatórias exatas (n ≤ 6, combinação de até 6 permutações).
- Corolário 10.11: no exemplo fixo W = [[4,1,3],[2,0,5],[3,2,2]] e X = J/3 vale
  5 ≤ 6 ≤ 22/3, e em 200 casos aleatórios ótimo ≤ c_dec ≤ ⟨W, X⟩ (ótimo por força bruta
  nas n! permutações).
- Entradas inválidas são rejeitadas. Os testes também mostram que `Fraction(0.1)` é
  diferente de 1/10 e que `Fraction("0.1")` é igual.

## Figuras

- `decomposicao.png`: Z9 e os 5 termos α_j P_j. Somados célula a célula, os painéis dão
  X, e cada P_j só cobre posições positivas.
- `passos.png`: o número de entradas positivas cai estritamente a cada passo, e r vai de
  1 a 0.
- `custos.png`: em 60 matrizes de B₅, os pontos ficam abaixo da diagonal y = x e acima da
  linha do ótimo da atribuição.
