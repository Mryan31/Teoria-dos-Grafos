import itertools
import os
import random
import subprocess
import sys
from corte import listas, corte_guloso, tamanho_corte, ler

AQUI = os.path.dirname(os.path.abspath(__file__))

# (arquivo, corte, lados, 2 x esperancas, corte maximo)
TABELA = [
    ("k3", 2, [0, 1, 0], [3, 3, 4, 4], 2),
    ("c4", 4, [0, 1, 0, 1], [4, 4, 5, 6, 8], 4),
    ("c5", 4, [0, 1, 0, 1, 0], [5, 5, 6, 7, 8, 8], 4),
    ("p5", 4, [0, 1, 0, 1, 0], [4, 4, 5, 6, 7, 8], 4),
    ("k4", 4, [0, 1, 0, 1], [6, 6, 7, 7, 8], 4),
    ("k5", 6, [0, 1, 0, 1, 0], [10, 10, 11, 11, 12, 12], 6),
    ("k33", 9, [0, 0, 0, 1, 1, 1], [9, 9, 9, 9, 12, 15, 18], 9),
    ("estrela", 5, [0, 1, 1, 1, 1, 1], [5, 5, 6, 7, 8, 9, 10], 5),
    ("cubo", 12, [0, 1, 1, 0, 1, 0, 0, 1], [12, 12, 13, 14, 16, 17, 19, 21, 24], 12),
    ("petersen", 12, [0, 1, 0, 1, 0, 1, 0, 0, 0, 1], [15, 15, 16, 17, 18, 18, 19, 20, 20, 21, 24], 12),
    ("paralelas", 4, [0, 1, 0], [4, 4, 7, 8], 4),
    ("sem_arestas", 0, [0, 0, 0, 0], [0, 0, 0, 0, 0], 0),
    ("p4_ordem_ruim", 2, [0, 0, 1, 0], [3, 3, 3, 4, 4], 3),
]


def le(nome):
    with open(os.path.join(AQUI, "entradas", nome + ".txt")) as f:
        return ler(f.read())


def roda(nome):
    with open(os.path.join(AQUI, "entradas", nome + ".txt")) as f:
        p = subprocess.run([sys.executable, os.path.join(AQUI, "corte.py")], stdin=f,
                           capture_output=True, text=True)
    return p.returncode, p.stdout.strip()


def corte_maximo(n, E):
    # forca bruta; fixa o vertice n-1 no lado 0 (o corte e simetrico)
    melhor = 0
    for mask in range(1 << max(n - 1, 0)):
        lado = [(mask >> i) & 1 for i in range(n)]
        melhor = max(melhor, tamanho_corte(E, lado))
    return melhor


def teste_tabela():
    for nome, c, lado, E2, cmax in TABELA:
        n, E = le(nome)
        l, e2, ops = corte_guloso(n, listas(n, E))
        assert (tamanho_corte(E, l), l, e2) == (c, lado, E2), (nome, l, e2)
        assert corte_maximo(n, E) == cmax, nome
        assert ops == 2 * len(E)
        cod, saida = roda(nome)
        assert cod == 0 and saida.splitlines()[0] == f"corte {c}", saida
    cod, saida = roda("ruim_laco")
    assert cod == 1 and saida == "ERRO laco"
    print(f"tabela ok ({len(TABELA)} casos + 1 rejeicao)")


def esperanca_bruta(n, E, lado, fixos):
    """2 x E[corte | lados de 'fixos'], fazendo a media sobre TODAS as escolhas dos livres.
    Serve pra conferir o item (a) sem usar a formula."""
    livres = [v for v in range(n) if v not in fixos]
    soma = 0
    for bits in itertools.product((0, 1), repeat=len(livres)):
        l = list(lado)
        for v, b in zip(livres, bits):
            l[v] = b
        soma += tamanho_corte(E, l)
    return 2 * soma / 2 ** len(livres)


def teste_esperanca():
    # (a): a esperanca condicional por enumeracao bate com garantidas + (abertas)/2 em cada passo
    # (b): a escolha do algoritmo nunca e pior que a outra
    rng = random.Random(24)
    for _ in range(300):
        n = rng.randint(1, 8)
        E = [e for e in itertools.combinations(range(n), 2) if rng.random() < 0.5]
        ordem = list(range(n))
        rng.shuffle(ordem)
        lado, E2, _ = corte_guloso(n, listas(n, E), ordem)
        for i in range(n + 1):
            fixos = set(ordem[:i])
            assert esperanca_bruta(n, E, lado, fixos) == E2[i]
            if i < n:
                v = ordem[i]
                outro = list(lado)
                outro[v] = 1 - lado[v]
                assert esperanca_bruta(n, E, outro, fixos | {v}) <= E2[i + 1]
    print("itens (a) e (b) conferidos por enumeracao em 300 grafos")


def teste_aleatorios():
    rng = random.Random(6)
    total = otimos = 0
    razao = []
    for _ in range(2000):
        n = rng.randint(1, 12)
        p = rng.random()
        E = [e for e in itertools.combinations(range(n), 2) if rng.random() < p]
        # algumas paralelas de vez em quando
        if E and rng.random() < 0.2:
            E += rng.sample(E, rng.randint(1, len(E)))
        ordem = list(range(n))
        if rng.random() < 0.5:
            rng.shuffle(ordem)
        lado, E2, ops = corte_guloso(n, listas(n, E), ordem)
        c = tamanho_corte(E, lado)
        m = len(E)
        assert 2 * c >= m                                         # pelo menos m/2
        assert E2[0] == m and E2[-1] == 2 * c                     # comeca em m/2, termina no corte
        assert all(E2[i] <= E2[i + 1] for i in range(n))          # nunca cai
        assert ops == 2 * m                                       # cada lista lida uma vez
        assert set(lado) <= {0, 1}
        cmax = corte_maximo(n, E)
        assert c <= cmax
        otimos += c == cmax
        if cmax:
            razao.append(c / cmax)
        total += 1
    print(f"{total} grafos aleatorios ok (n <= 12): corte >= m/2 sempre, otimo em {otimos}, "
          f"pior razao corte/maximo {min(razao):.3f}")


def compara_aleatorias(nome, n, E, rng, vezes=2000):
    lado, _, _ = corte_guloso(n, listas(n, E))
    c = tamanho_corte(E, lado)
    cortes = [tamanho_corte(E, [rng.randint(0, 1) for _ in range(n)]) for _ in range(vezes)]
    media = sum(cortes) / vezes
    melhores = sum(1 for x in cortes if x > c) / vezes
    iguais = sum(1 for x in cortes if x == c) / vezes
    return c, len(E) / 2, media, iguais, melhores, corte_maximo(n, E)


def teste_comparacao():
    rng = random.Random(0)
    print("arquivo        guloso  m/2   media aleat.  %aleat = guloso  %aleat > guloso  maximo")
    for nome, *_ in TABELA:
        n, E = le(nome)
        if not E:
            continue
        c, meio, media, ig, mel, cmax = compara_aleatorias(nome, n, E, rng)
        print(f"{nome:14s} {c:5d}  {meio:5.1f}  {media:8.2f}      {100 * ig:8.1f}       {100 * mel:8.1f}"
              f"        {cmax:3d}")
        assert abs(media - meio) < 0.1 * len(E) + 0.5        # a media das moedas fica perto de m/2


if __name__ == "__main__":
    teste_tabela()
    teste_esperanca()
    teste_aleatorios()
    teste_comparacao()
    print("todos os testes passaram")
