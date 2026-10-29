# Tarefa 8.15 - Algoritmo de Edmonds (blossoms virtuais)

## Como rodar

```
python edmonds.py entradas/c5.txt   # um arquivo
python edmonds.py                   # todos de entradas/, grava saidas/*.out
python testes.py
python graficos.py
```

## Entrada e saída

Entrada: `n m`, depois `m` linhas `u v` (vértices 0..n−1, grafo simples; laços e arestas
repetidas são rejeitados). Linhas opcionais `M u v` dão um emparelhamento inicial (usado
para reproduzir o exemplo da flor do texto).

```
nu 4
mate 1 0 3 2 5 4 7 6
```

`mate[v] = -1` significa exposto.

## Onde está cada estrutura do enunciado

| Enunciado     | Código (`edmonds.py`)                                                    |
|---------------|--------------------------------------------------------------------------|
| `mate[v]`     | lista `mate`, −1 = ⊥                                                     |
| `parent[v]`   | lista `parent`, recriada em cada BUSCA                                   |
| `base[v]`     | lista `base`, recriada em cada BUSCA (contração virtual)                 |
| `type[v]`     | lista `tipo`: 0 não alcançado, 1 interno (`INT`), 2 externo (`EXT`)      |
| fila          | `deque` dentro de `busca`                                                |
| `inBlossom`   | lista `inb` em `contraia`, recriada em cada contração                    |
| BUSCA(r)      | `busca(r, adj, mate)`, que devolve `(z, parent, base, tipo)`             |
| CONTRAIA      | `contraia(x, y, b, ...)`                                                 |
| AUMENTE(z)    | `aumente(z, parent, mate)`                                               |
| laço principal| `edmonds(n, adj, mate0=None)`                                            |

A busca é enraizada em um único vértice exposto. Depois de cada aumento, a varredura das
raízes recomeça do vértice 0.

## Nota sobre o LCA

O enunciado não diz como achar a base comum b. Fiz assim: subindo de x, marco as bases
(`u = base[u]`, depois `u = parent[mate[u]]`) até chegar na raiz (exposta). Depois subo
de y pelo mesmo caminho até achar a primeira base marcada. A subida é sempre via
`base[]`, porque, depois da primeira contração, usar o vértice cru dá errado.

## O que foi testado (`testes.py`)

- ν(C_{2k+1}) = k para C3..C9 e até k = 20; ν(K_n) = ⌊n/2⌋ para n ≤ 12;
  ν(Petersen) = 5. Também gravata, dois triângulos + ponte, estrela, aranha, sol, P4 +
  isolado e grafo sem arestas.
- **Rastro do exemplo do texto** (flor, com M inicial {pb, wz, yx}, raiz r = 0): depois
  da busca, `parent = [-1,0,-1,2,5,4,2,6]`, `base = [0,1,2,2,2,2,2,7]`,
  `tipo = E I E E E E E -` e z = 7. Houve exatamente uma contração, CONTRAIA(4, 5, 2).
  AUMENTE percorre 7, 6, 5, 4, 3, 2, 1, 0 (o caminho rpbwzyxt do texto) e o resultado é
  `mate = [1,0,3,2,5,4,7,6]`.
- Depois de **cada** aumento (dentro de `edmonds`): `mate[mate[v]] == v`, pares
  adjacentes e |M| subiu exatamente 1.
- 3000 grafos aleatórios (n ∈ [1, 9], densidade 0,2 / 0,35 / 0,5), comparados com busca
  exaustiva sobre os subconjuntos de arestas que formam emparelhamento (m ≤ 14), com a
  fórmula de Tutte–Berge n − 2ν = max_S (odd(G − S) − |S|), enumerando os 2^n conjuntos
  S, e com `networkx.max_weight_matching(maxcardinality=True)`.

## Figuras

- `blossom.png`: à esquerda, a flor com M em azul, o blossom em dourado e o caminho
  aumentante em vermelho. À direita, o grafo contraído (cada valor distinto de `base` vira
  um vértice), em que o caminho r p c t aparece.
- `petersen.png`: o emparelhamento perfeito do Petersen, |M| = 5 = n/2.
- `tempo_loglog.png`: grafos aleatórios com m = 3n. A inclinação medida foi **1,68**,
  bem abaixo da referência n³.
