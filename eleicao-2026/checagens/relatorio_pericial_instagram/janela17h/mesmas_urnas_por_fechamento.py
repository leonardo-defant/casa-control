"""Urnas que ficaram abertas depois das 17h no 2º turno de 2026: vantagem de Lula nelas no 1º e no 2º turno.

Pergunta (Léo, 30/10/2026): o relatório quis dizer que as urnas que ficaram abertas depois das 17h, e não os
votos dados depois das 17h, dão ampla vantagem a Lula. Aqui as seções são agrupadas pela hora de encerramento do
2º turno, em hora de Brasília, e para as MESMAS seções se mostra o voto do 1º turno (sem prorrogação) e do 2º.
Fuso de cada município: hora de abertura mais comum no 2º turno (8h = Brasília). Exterior fora (a liminar valia no
Brasil). Virada = fatia de Lula entre os dois finalistas, 2º turno menos 1º. Comparação dentro do município e dentro
do local de votação: média ponderada (votos dos finalistas no 2º turno) da virada de cada grupo depois de tirar a
média do município (ou do local), igual ao estimador de efeito fixo com só uma variável de grupo.
Uso: python3 -I mesmas_urnas_por_fechamento.py <secoes2026.json.gz> <saida.json>
"""
import collections, gzip, json, sys


def seg(h):
    return int(h[0:2]) * 3600 + int(h[3:5]) * 60 + int(h[6:8])


GRUPOS = [('ate_17h00m59', 0, 17 * 3600 + 60), ('17h01_17h02_antes_da_liminar', 17 * 3600 + 60, 17 * 3600 + 180),
          ('17h03_17h48_liminar_sem_ordem_do_TSE', 17 * 3600 + 180, 17 * 3600 + 49 * 60),
          ('17h49_18h59', 17 * 3600 + 49 * 60, 19 * 3600), ('19h_ou_mais', 19 * 3600, 99 * 3600)]


def main():
    base = json.load(gzip.open(sys.argv[1]))
    ab = collections.defaultdict(collections.Counter)
    for k, s in base.items():
        uf, mun = k.split('|')[:2]
        if uf != 'ZZ' and '2' in s and s['2'].get('ab'):
            ab[(uf, mun)][int(s['2']['ab'][:2])] += 1
    desloc = {m: 8 - c.most_common(1)[0][0] for m, c in ab.items()}
    linhas = []
    for k, s in base.items():
        uf, mun = k.split('|')[:2]
        if uf == 'ZZ' or '1' not in s or '2' not in s or not s['2'].get('enc'):
            continue
        a, b = s['1'], s['2']
        if a['L'] + a['R'] == 0 or b['L'] + b['R'] == 0:
            continue
        t = seg(b['enc']) + desloc[(uf, mun)] * 3600
        g = next(n for n, i, f in GRUPOS if i <= t < f)
        linhas.append({'g': g, 'mun': (uf, mun), 'loc': (uf, mun, k.split('|')[2], b['loc']),
                       'L1': a['L'], 'R1': a['R'], 'L2': b['L'], 'R2': b['R'], 'comp2': b['comp'], 'w': b['L'] + b['R'],
                       'v': 100 * b['L'] / (b['L'] + b['R']) - 100 * a['L'] / (a['L'] + a['R'])})
    out = {'secoes': len(linhas), 'grupos': {}}
    tot = collections.Counter()
    for n, *_ in GRUPOS:
        x = [r for r in linhas if r['g'] == n]
        c = collections.Counter()
        for r in x:
            for q in ('L1', 'R1', 'L2', 'R2', 'comp2'):
                c[q] += r[q]
        tot.update(c)
        f1 = 100 * c['L1'] / (c['L1'] + c['R1']); f2 = 100 * c['L2'] / (c['L2'] + c['R2'])
        out['grupos'][n] = {'secoes': len(x), 'votantes_2t': c['comp2'], 'lula_1t_pct_dois': round(f1, 2),
                            'lula_2t_pct_dois': round(f2, 2), 'virada_pts': round(f2 - f1, 2),
                            'margem_lula_1t': c['L1'] - c['R1'], 'margem_lula_2t': c['L2'] - c['R2'],
                            'margem_2t_se_votassem_com_a_fatia_do_1t': round((2 * f1 / 100 - 1) * (c['L2'] + c['R2']))}
    out['brasil'] = {'margem_lula_1t': tot['L1'] - tot['R1'], 'margem_lula_2t': tot['L2'] - tot['R2'],
                     'lula_1t_pct_dois': round(100 * tot['L1'] / (tot['L1'] + tot['R1']), 2),
                     'lula_2t_pct_dois': round(100 * tot['L2'] / (tot['L2'] + tot['R2']), 2)}
    depois = [n for n, *_ in GRUPOS if n != 'ate_17h00m59']
    c = collections.Counter()
    for r in linhas:
        if r['g'] in depois:
            for q in ('L1', 'R1', 'L2', 'R2', 'comp2'):
                c[q] += r[q]
    out['abertas_depois_das_17h00m59'] = {'secoes': sum(1 for r in linhas if r['g'] in depois), 'votantes_2t': c['comp2'],
                                         'lula_1t_pct_dois': round(100 * c['L1'] / (c['L1'] + c['R1']), 2),
                                         'lula_2t_pct_dois': round(100 * c['L2'] / (c['L2'] + c['R2']), 2),
                                         'margem_lula_1t': c['L1'] - c['R1'], 'margem_lula_2t': c['L2'] - c['R2']}
    for nivel in ('mun', 'loc'):
        sw = collections.defaultdict(float); sv = collections.defaultdict(float)
        for r in linhas:
            sw[r[nivel]] += r['w']; sv[r[nivel]] += r['w'] * r['v']
        res = collections.defaultdict(lambda: [0.0, 0.0, 0])
        grupos_por = collections.defaultdict(set)
        for r in linhas:
            grupos_por[r[nivel]].add(r['g'])
        for r in linhas:
            if len(grupos_por[r[nivel]]) < 2:
                continue
            d = r['v'] - sv[r[nivel]] / sw[r[nivel]]
            res[r['g']][0] += r['w'] * d; res[r['g']][1] += r['w']; res[r['g']][2] += 1
        out[f'virada_menos_media_do_{nivel}'] = {g: {'pts': round(a / b, 3), 'secoes': n} for g, (a, b, n) in res.items()}
    json.dump(out, open(sys.argv[2], 'w'), ensure_ascii=False, indent=1)
    print(json.dumps(out, ensure_ascii=False, indent=1))


if __name__ == '__main__':
    main()
