# Teoria dos Grafos — Exercícios de Implementação

Aluno: Mateus Ryan de Castro Lima

Implementações das tarefas propostas nas aulas 1 a 25 da disciplina de Teoria dos Grafos
(Prof. Gabriel Coutinho), organizadas nas cinco partes dos enunciados. Cada tarefa fica
em uma pasta própria e não depende das outras: quando uma tarefa reaproveita um
algoritmo anterior (por exemplo, o emparelhamento bipartido da 7.11 nas tarefas 10.10 e
10.18), a função foi copiada para dentro da pasta.

## Requisitos

- Python 3.10 ou mais recente (testado com 3.13).
- `matplotlib` e `numpy` para os gráficos; `networkx` só nos testes, como conferência
  independente, e nos desenhos de algumas figuras.

```
pip install matplotlib numpy networkx
```

Os algoritmos em si usam apenas a biblioteca padrão. A única exceção é o desenho de
Tutte da tarefa 14.5, que resolve um sistema linear com `numpy`.

## Organização de cada tarefa

Com exceção da tarefa 14.5 (ver abaixo), todas as pastas seguem o mesmo formato:

| arquivo / pasta | conteúdo |
|-----------------|----------|
| programa principal (`*.py`) | o algoritmo, a leitura da entrada e a verificação do resultado |
| `testes.py` | casos da tabela do enunciado, testes aleatórios, força bruta e comparação com networkx |
| `graficos.py` | gera as figuras em `figuras/` |
| `entradas/` | exemplos de entrada usados nos testes e no README |
| `saidas/` ou `logs/` | saídas geradas a partir de `entradas/` (Partes 1, 2 e tarefa 20.11) |
| `README.md` | como rodar, formato de entrada e saída, explicação, provas pedidas, tabela de testes e figuras |

Os comandos devem ser executados **de dentro da pasta da tarefa**, pois os caminhos de
`entradas/` e `figuras/` são relativos a ela. Por exemplo:

```
cd "Parte 4/tarefa_16_8"
python fluxo.py < entradas/ex16_7.txt
python testes.py
python graficos.py
```

Entradas inválidas são rejeitadas com uma mensagem de erro em vez de um resultado
incorreto. O formato exato de cada programa está descrito no README da tarefa.

## Tarefas

### Parte 1 — Aulas 1 a 5

| tarefa | tema | programa |
|--------|------|----------|
| [1.21](Parte%201/tarefa_1_21) | Refinamento de cores (1-WL): refina a coloração por grau até estabilizar | `refinamento.py` |
| [2.7](Parte%201/tarefa_2_7) | Havel–Hakimi: decide se uma sequência é gráfica e constrói uma realização | `havel_hakimi.py` |
| [2.11](Parte%201/tarefa_2_11) | Remoção de vértices de grau baixo (Teorema 2.8), com heap | `nucleo_denso.py` |
| [3.8](Parte%201/tarefa_3_8) | Imersão de uma árvore T em G com δ(G) ≥ \|V(T)\| − 1 | `imersao_arvore.py` |
| [3.16](Parte%201/tarefa_3_16) | Codificação e decodificação de Prüfer em O(n log n) | `prufer.py` |
| [4.7](Parte%201/tarefa_4_7) | Hierholzer para multigrafos (laços e arestas paralelas) | `hierholzer.py` |
| [5.21](Parte%201/tarefa_5_21) | Prim com registro de S, ∂(S) e da aresta escolhida | `prim.py` |

### Parte 2 — Aulas 6 a 10

| tarefa | tema | programa |
|--------|------|----------|
| [6.19](Parte%202/tarefa_6_19) | Edmonds–Karp para multigrafos dirigidos, com certificado de corte mínimo | `edmonds_karp.py` |
| [7.11](Parte%202/tarefa_7_11) | Caminhos aumentantes em bipartidos e cobertura de König | `bipartido.py` |
| [8.15](Parte%202/tarefa_8_15) | Algoritmo de Edmonds com contração de blossoms | `edmonds.py` |
| [9.11](Parte%202/tarefa_9_11) | Conectividade por arestas e por vértices via fluxo (Menger) | `conectividade.py` |
| [10.10](Parte%202/tarefa_10_10) | Decomposição de Birkhoff–von Neumann em aritmética exata | `birkhoff.py` |
| [10.18](Parte%202/tarefa_10_18) | Dilworth: partição mínima em cadeias e anticadeia máxima | `dilworth.py` |

### Parte 3 — Aulas 11 a 15

| tarefa | tema | programa |
|--------|------|----------|
| [14.5](Parte%203/tarefa_14_5) | Teste de planaridade por contrações: faces e base de ciclos se planar, menor K5 ou K3,3 se não | `planar_contract.py` |

A tarefa 14.5 foi dividida em seis etapas (`m1_conexidade` a `m6_tutte`), cada uma com
seu próprio teste, e tem um relatório curto em `relatorio.pdf` (gerado por
`gera_relatorio.py`). Os comandos estão no README da pasta; os testes das etapas rodam
com `python -m m1_conexidade.test_m1` etc., e o teste geral com
`python test_integrador.py`.

### Parte 4 — Aulas 16 a 20

| tarefa | tema | programa |
|--------|------|----------|
| [16.8](Parte%204/tarefa_16_8) | De uma Z_k-circulação nunca zero a um k-fluxo inteiro (Tutte, Teor. 16.6) | `fluxo.py` |
| [20.11](Parte%204/tarefa_20_11) | König e Vizing: coloração de arestas inserindo uma aresta por vez, com verificador independente | `coloracao.py` |

### Parte 5 — Aulas 21 a 25

| tarefa | tema | programa |
|--------|------|----------|
| [21.9](Parte%205/tarefa_21_9) | Simetrização de Zykov com certificado: uma K_{r+1} em G ou a prova de que G ≅ T_r(n) | `simetrizacao.py` |
| [24 P6](Parte%205/tarefa_24_P6) | Corte com pelo menos m/2 arestas sem aleatoriedade (esperanças condicionais) | `corte.py` |

## Como os resultados foram conferidos

Na maioria das tarefas, o programa principal confere o próprio resultado antes de
imprimir (por exemplo, que o fluxo conserva, que a coloração é própria, que a clique
devolvida é de fato uma clique em G). Os arquivos de teste vão além disso:

- reproduzem os exemplos e tabelas dos enunciados;
- comparam com força bruta em instâncias pequenas e com networkx em instâncias
  aleatórias;
- verificam as propriedades que as provas garantem (cotas, invariantes, número de
  iterações) em centenas ou milhares de instâncias aleatórias com semente fixa, de modo
  que os números citados nos READMEs são reproduzíveis.

Os gráficos de tempo são medições em uma máquina comum e servem para confirmar o
crescimento polinomial previsto; os expoentes medidos podem variar um pouco de uma
execução para outra.

Para rodar todos os testes de uma vez (Git Bash ou Linux), a partir desta pasta:

```
for d in Parte*/tarefa_*; do
  echo "== $d"
  if [ -f "$d/testes.py" ]; then (cd "$d" && python testes.py | tail -1)
  else (cd "$d" && python test_integrador.py | tail -1); fi
done
```
