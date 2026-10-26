"""T33(a) do pré-registro (adendo 9): o candidato de direita em votos totais nas pesquisas finais do 2º turno.

Previsto = votos totais do candidato + sua parte proporcional dos indecisos (os que declaram branco/nulo ficam fora).
Comparado com o voto real dele em % do comparecimento. Distância = real menos previsto.
Dados: resultados/nacionais_2026_pesquisas_verificadas.txt e resultados/nacionais_2018_2022_pesquisas_verificadas.txt.
Quando a pesquisa publica indecisos e branco/nulo somados, ou não publica o resto, o previsto vai como faixa
(todo o resto como indeciso ou todo como branco/nulo) e a leitura usa o ponto médio, marcada como ambígua.
"""
REAL = {2018: 49.85, 2022: 46.85, 2026: 46.65}  # direita em % do comparecimento (bweb 2018 e 2022; TSE 2026)

# (instituto, ano, direita, esquerda, branco_nulo, indecisos); None = não publicado
PESQ = [
    ('Datafolha', 2018, 47, 39, 8, 5), ('Ibope/Ipec', 2018, 47, 41, 10, 2), ('CNT/MDA', 2018, 48.5, 37, 10.3, 4.2),
    ('Parana Pesquisas', 2018, 53, 34.4, 8.6, 3.9), ('PoderData', 2018, 57, 31, 9, 3),
    ('Datafolha', 2022, 45, 49, 4, 2), ('Ibope/Ipec', 2022, 43, 50, 5, 2), ('Quaest', 2022, 43, 46, None, None),
    ('AtlasIntel', 2022, 45.7, 52.4, None, None), ('CNT/MDA', 2022, 44.9, 46.9, 5.6, 2.6),
    ('Parana Pesquisas', 2022, 46.3, 47.1, 3.4, 3.2), ('PoderData', 2022, 44, 49, 5, 2),
    ('Futura', 2022, 47.2, 46.6, 3.7, 2.4), ('Gerp', 2022, 47, 43, None, None), ('Verita', 2022, 47.8, 45.9, 3.2, 3.1),
    ('Datafolha', 2026, 48, 47, 3, 2), ('Quaest', 2026, 46, 45, 8, 1), ('AtlasIntel', 2026, 49.9, 48.4, None, None),
    ('CNT/MDA', 2026, 46.3, 45.0, 5.8, 2.9), ('Verita', 2026, 49.44, 46.46, 1.43, 2.67), ('Ipespe', 2026, 48, 47, 3, 2),
    ('Nexus', 2026, 47, 46, None, None), ('Real Time Big Data', 2026, 49, 45, 5, 1), ('Vox Brasil', 2026, 44.3, 45.4, 6, 4.3),
]


def previsto(d, e, bn, ind):
    if bn is not None and ind is not None:
        v = d + ind * d / (d + e)
        return v, v, False
    resto = max(0.0, 100 - d - e)
    return d, d + resto * d / (d + e), True


def main():
    dist = {}
    print('distância = voto real em % do comparecimento menos o previsto pela pesquisa (negativo: abaixo da pesquisa)')
    for nome, ano, d, e, bn, ind in PESQ:
        lo, hi, amb = previsto(d, e, bn, ind)
        m = (lo + hi) / 2
        dist[(nome, ano)] = REAL[ano] - m
        faixa = f' (faixa {REAL[ano] - hi:+.2f} a {REAL[ano] - lo:+.2f}, ambígua)' if amb else ''
        print(f'  {ano} {nome:20s} previsto {m:6.2f} real {REAL[ano]:6.2f} distância {REAL[ano] - m:+.2f}{faixa}')
    hist = [v for (n, a), v in dist.items() if a < 2026]
    media_hist = sum(hist) / len(hist)
    print(f'\ndistância histórica (2018 e 2022, {len(hist)} pesquisas): média {media_hist:+.2f}, '
          f'mínimo {min(hist):+.2f}, máximo {max(hist):+.2f}')
    print('\n2026, distância além da histórica do mesmo instituto (ou da média geral se não houver histórico):')
    abaixo3 = 0; ate1 = 0; n = 0
    for (nome, ano), v in dist.items():
        if ano != 2026:
            continue
        h = [x for (nn, a), x in dist.items() if nn == nome and a < 2026]
        ref = sum(h) / len(h) if h else media_hist
        ex = v - ref; n += 1
        abaixo3 += ex <= -3; ate1 += abs(ex) <= 1
        print(f'  {nome:20s} distância {v:+.2f} referência {ref:+.2f} ({"mesmo instituto" if h else "média geral"}) além da histórica {ex:+.2f}')
    print(f'\ninstitutos de 2026 com Flávio 3 pontos ou mais abaixo, além da histórica: {abaixo3} de {n} '
          f'(critério: pelo menos 5 => conversão pura de branco/nulo não explica o resultado)')
    print(f'institutos a até 1 ponto da histórica: {ate1} de {n}')


if __name__ == '__main__':
    main()
