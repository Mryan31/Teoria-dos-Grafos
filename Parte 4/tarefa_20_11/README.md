# Tarefa 20.11 - König e Vizing: colorir arestas inserindo uma por vez

## Como rodar

```
python coloracao.py konig logs/p6_konig.log < entradas/p6.txt > logs/p6_konig.out
python verificador.py entradas/p6.txt logs/p6_konig.out konig logs/p6_konig.log    # -> OK
python coloracao.py vizing logs/petersen_vizing.log < entradas/petersen.txt
python testes.py
python graficos.py          # figuras/figA..figD
```

Arquivos: `coloracao.py` (estado, König, Vizing), `verificador.py` (independente),
`grafos.py` (geradores), `exato.py` (χ′ por backtracking), `desenho.py`, `testes.py`,
`graficos.py`. Em `logs/` estão a saída e o log de cada entrada de `entradas/`.

## Entrada, saída e log

Entrada: `n m` e `m` linhas `u v` (vértices 0..n−1). A ordem das linhas é a ordem de
inserção, com x = u e y₀ = v. O König aceita multigrafo bipartido (paralelas); o Vizing
exige grafo simples; laço é sempre rejeitado (`ERRO nao-bipartido`, `ERRO nao-simples`).

```
paleta 2
usadas 2
1 2 1 1 2
```

Log (um passo por linha, permite reproduzir tudo):

| linha | significado |
|-------|-------------|
| `INS e u v` | começa a inserção da aresta e = uv |
| `COR e c` | atribui c a e (que estava sem cor) |
| `TROCA a b e1 ... eL` | troca a ↔ b nas arestas listadas (a componente inteira) |
| `DESLOCA e0 ... et` | arestas xy₀..xy_t, e0 sem cor: c(e_{i−1}) ← c_antiga(e_i) ao mesmo tempo; e_t fica sem cor |

Exemplo (P6 = 2-4-0-5-1-3, König): `INS 4 0 4 / TROCA 1 2 2 1 3 / COR 4 2`. O verificador
reaplica essas linhas do zero com `reproduz` e reconstrói `1 2 1 1 2`.

A paleta é fixada uma vez pelo Δ do grafo inteiro: C = Δ (König) ou C = Δ + 1 (Vizing).

**Regras de desempate**: arestas na ordem da entrada; x = u; "cor livre comum" = a menor;
α = menor cor ausente em x; β = menor ausente em y (König) ou em y_k (Vizing).

## (c) A tabela, a componente de duas cores e os limites

**Tabela.** `T[v][c]` guarda o **id** da aresta de cor c em v, ou −1. Tem n(C + 1)
posições. Guardar o id (e não o vizinho) é o que faz funcionar com arestas paralelas no
König. M(v) = {c : T[v][c] = −1}, e a "menor cor ausente" é uma varredura da linha de v,
em O(C).

**Percorrer a componente (α, β) de x** (com α ausente em x):

```
v <- x; c <- beta
enquanto T[v][c] != -1:
    e <- T[v][c]; P.append(e); v <- outro extremo de e
    c <- (alfa se c = beta senao beta)
```

Cada passo é O(1). Como cada vértice tem no máximo uma aresta de cada cor (Lema 20.5), a
componente é um caminho com vértices distintos. Então |P| ≤ n − 1 e o laço para: O(n).

**Atualizar T.** Em `troca` e em `desloca`, primeiro guardo as cores antigas, depois
**apago** todas as arestas envolvidas de `cor` e de `T`, e só então reescrevo. Reescrever
uma aresta por vez sobrescreveria T[v][a] ou T[v][b] de uma vizinha que ainda não foi
trocada. Custo: 2 escritas na tabela por aresta, O(|P|) na troca e O(t) no deslocamento.

**König: O(m(n + Δ)).** Por inserção: procurar uma cor comum O(C), achar α e β O(C), o
caminho e a troca O(n). Total O(m(n + Δ)) ⊆ O(m(n + m)), mais O(nΔ) para criar a tabela.

**Vizing: O(m(Δ² + n)) ⊆ O(mn²).** O leque tem ≤ Δ vizinhos distintos de x, e cada extensão
custa O(C) (menor ausente) + O(1) (`pos` e T[x][β]): O(Δ²). Dois deslocamentos O(Δ), um
caminho com troca O(n). Por inserção O(Δ² + n); total O(m(Δ² + n)) ⊆ O(mn²), já que Δ < n.

## Verificador (`verificador.py`)

Não importa `coloracao.py`. Ele recalcula Δ por conta própria, confere |cor| = m, cores em
1..C, C = Δ (König) ou Δ + 1 (Vizing) e simplicidade no Vizing. Também confere que em
cada vértice as cores das arestas são distintas, usando `Counter` sobre a lista de
arestas, sem usar a tabela T. `reproduz(n, E, C, linhas)` reaplica o log do zero e
confere a coloração parcial depois de **cada** operação. Ele exige também que toda TROCA
seja uma componente inteira (nenhuma aresta de cor a ou b fora de P toca um vértice de P)
e que as cores finais sejam iguais à saída.

## Testes (`testes.py`) - todos passaram

**König** (C = Δ, sempre usa exatamente Δ cores):

| grafo | m | Δ | usadas | trocas | máx \|P\| | passou |
|-------|---|---|--------|--------|-----------|--------|
| K1,1 / K1,5 | 1 / 5 | 1 / 5 | 1 / 5 | 0 | 0 | sim |
| K2,3 / K3,3 / K3,5 | 6 / 9 / 15 | 3 / 3 / 5 | 3 / 3 / 5 | 1 | 1 | sim |
| K4,4 | 16 | 4 | 4 | 0 | 0 | sim |
| K5,7 / K6,6 | 35 / 36 | 7 / 6 | 7 / 6 | 5 / 3 | 5 / 3 | sim |
| K10,12 | 120 | 12 | 12 | 14 | 7 | sim |
| C6, C8, C20 | 6, 8, 20 | 2 | 2 | 0 | 0 | sim |
| Q3 / Q4 / grade 4×4 | 12 / 32 / 24 | 3 / 4 / 4 | 3 / 4 / 4 | 0 | 0 | sim |

Vetores completos iguais aos do guia: C4, C6, K2,3 (com `TROCA 3 1 4`), K3,3, P6 (com
`TROCA 1 2 2 1 3`), 3 paralelas (1 2 3) e o multigrafo com n = 5 (1 2 2 3 1, com
`TROCA 2 1 1`).

**Vizing** (C = Δ + 1):

| grafo | n | m | Δ | usadas | trocas | A | B | passou |
|-------|---|---|---|--------|--------|---|---|--------|
| K3 / K4 / K5 | 3 / 4 / 5 | 3 / 6 / 10 | 2 / 3 / 4 | 3 / 4 / 5 | 0 / 1 / 4 | 0 / 1 / 3 | 0 / 0 / 1 | sim |
| K6 / K7 / K8 / K9 | 6..9 | 15 / 21 / 28 / 36 | 5..8 | 6 / 7 / 8 / 9 | 6 / 10 / 15 / 22 | 6 / 10 / 14 / 22 | 0 / 0 / 1 / 0 | sim |
| C4, C6, C3, C5, C7, C9 | | | 2 | 3 | 0 | 0 | 0 | sim |
| Petersen | 10 | 15 | 3 | 4 | 1 | 0 | 1 | sim |
| Petersen − vértice 0 | 9 | 12 | 3 | 4 | 0 | 0 | 0 | sim |
| K5 − {0,1} | 5 | 9 | 4 | 5 | 2 | 2 | 0 | sim |
| W3 / W5 / W7 | 4 / 6 / 8 | 6 / 10 / 14 | 3 / 5 / 7 | 4 / 5 / 7 | 1 | 1 | 0 | sim |
| W4 / W6 / W8 | 5 / 7 / 9 | 8 / 12 / 16 | 4 / 6 / 8 | 4 / 6 / 8 | 0 | 0 | 0 | sim |
| K3,3 / K4,4 / Q3 | 6 / 8 / 8 | 9 / 16 / 12 | 3 / 4 / 3 | 3 / 4 / 4 | 1 / 3 / 1 | 1 / 3 / 1 | 0 | sim |

Vetores completos iguais aos do guia: C4 (2 3 2 1), C5, K4, K5, Petersen e W4.

**Traços dourados**, reproduzidos linha a linha:

| nome | log da inserção | cores finais |
|------|-----------------|--------------|
| T-A (caso A, j = 0) | `INS 2 0 2 / TROCA 3 1 0 / COR 2 1` | 3 2 1 1 |
| T-A2 (caso A, j ≥ 1) | `INS 4 3 4 / DESLOCA 4 1 / TROCA 4 2 2 / COR 1 2` | 1 2 4 3 1 |
| T-B (caso B, j = 0, k = 2) | `INS 4 0 2 / TROCA 3 1 2 1 / DESLOCA 4 2 3 / COR 3 1` | 4 1 2 1 3 |
| T-C (caso B, j = 1, k = 3) | `INS 5 4 2 / DESLOCA 5 3 / TROCA 4 2 2 0 / DESLOCA 3 2 4 / COR 4 2` | 2 1 3 4 2 1 |

**Rejeições**: König em C5, K4 e Petersen → `ERRO nao-bipartido`; Vizing com aresta
repetida ou laço → `ERRO nao-simples`; m = 0 → paleta 0.

**Aleatórios**: 20.000 grafos simples (n ≤ 12, ordem e orientação aleatórias) pelo Vizing
e 20.000 multigrafos bipartidos pelo König. Todos passaram no verificador e na reprodução
do log. O Vizing usou entre Δ e Δ + 1 cores e o König exatamente Δ. A cobertura foi de
**23.189 inserções no caso A e 2.895 no caso B**. Uma parte também foi conferida com
`networkx.line_graph` (arestas adjacentes têm cores diferentes).

**Exato** (`exato.chi`, n ≤ 8): o Vizing usou χ′ ou χ′ + 1 em 300 grafos aleatórios.
Petersen, K3 e K5 são de classe 2; K4, K6 e K8 de classe 1. K7 e K9 são de classe 2 pela
contagem do Probl. 20.P3(c): cada cor cobre ≤ (n−1)/2 arestas, e m > Δ(n−1)/2.

**Invariância**: embaralhar 200 vezes a ordem das arestas (Petersen, K6, W5) sempre deu
coloração própria com ≤ Δ + 1 cores.

## Figuras

- `figA_cores.png`: Petersen com 4 cores (é de classe 2) e K6 com 6 cores, embora χ′(K6) = 5.
  É o "+1" que o Vizing pode gastar.
- `figB_konig.png`: troca de König no P6. Antes, x = 0 tem a cor 2 e y = 4 tem a cor 1, e
  a componente (1, 2) de x não chega em y (y ∉ P). Depois da troca, a cor 2 fica livre nos
  dois e 0-4 recebe 2.
- `figC_leque.png`: o traço T-C reconstruído pelo `reproduz` em quatro momentos: antes, o
  1º deslocamento com P em destaque (caso B), a troca, e o 2º deslocamento usando as cores
  atuais.
- `figD_tempo.png`: tempo × m em log-log. Expoentes medidos de **1,20** (König em K_{s,s})
  e **1,29** (Vizing em K_s): crescimento polinomial, abaixo das cotas.

## Observação

K4, Petersen e os ciclos ímpares não são bipartidos, então só passam pelo Vizing. K4 e K6
mostram o "+1" do Vizing (usam Δ + 1 cores, mas χ′ = Δ).
