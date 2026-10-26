"""T9 do pré-registro: os eleitores a mais do 2º turno foram habilitados por biometria?
Usa o log do 2º turno, que traz também o dia do 1º turno da mesma urna.
Uso: python3 -I analisar_biometria.py <pasta_arq_2t> <secoes2026_amostra.json.gz> <saida.json>
"""
import os as _os, sys as _sys
_sys.path.insert(0, _os.path.dirname(_os.path.abspath(__file__)))
import collections, json, os, sys
import numpy as np
from decodificar import _linhas_log
from lib import carregar, chave_local, fe_ols

D1, D2 = '04/10/2026', '25/10/2026'
pasta, base, saida = sys.argv[1:4]
d = carregar(base)
rows = []; tot = collections.Counter()
for raiz, dirs, arqs in os.walk(pasta):
    logs = [a for a in arqs if a.endswith('-log.jez')]
    if not logs: continue
    uf, m, z, s = raiz.split('arq/')[-1].split('/')
    k = f'{uf.upper()}|{int(m)}|{int(z)}|{int(s)}'
    c = collections.Counter()
    for bloco in _linhas_log(os.path.join(raiz, sorted(logs)[-1])):
        for l in bloco:
            p = l.split('\t')
            if len(p) < 5: continue
            dia = p[0][:10]
            if dia not in (D1, D2): continue
            t = '1' if dia == D1 else '2'
            if p[4] == 'Eleitor foi habilitado': c['hab' + t] += 1
            elif p[4] == 'Tipo de habilitação do eleitor [biométrica]': c['bio' + t] += 1
            elif p[4] == 'O voto do eleitor foi computado': c['comp' + t] += 1
    v = d.get(k, {})
    if '1' not in v or '2' not in v or not c['hab1']: continue
    # só urnas cujo log cobre o dia do 1º turno inteiro (mesma urna nos dois turnos)
    if c['comp1'] != v['1']['comp'] or c['comp2'] != v['2']['comp']: continue
    nb1, nb2 = c['hab1'] - c['bio1'], c['hab2'] - c['bio2']
    rows.append((chave_local(k, v['2']), c['bio1'], nb1, c['bio2'], nb2, v['1']['comp'], v['2']['comp'], v['1']['L'], v['2']['L'], v['1']['R'], v['2']['R']))
    for x in ('hab1', 'bio1', 'hab2', 'bio2'): tot[x] += c[x]
A = np.array([r[1:] for r in rows], float); loc = np.array([r[0] for r in rows])
b1, nb1, b2, nb2, C1, C2, L1, L2, R1, R2 = A.T
dC, dNB, dB, dL = C2 - C1, nb2 - nb1, b2 - b1, L2 - L1
out = {'secoes': len(rows), 'totais': dict(tot),
       'pct_bio_1t': 100 * tot['bio1'] / tot['hab1'], 'pct_bio_2t': 100 * tot['bio2'] / tot['hab2'],
       'var_comparecimento': float(dC.sum()), 'var_biometricos': float(dB.sum()), 'var_nao_biometricos': float(dNB.sum())}
# dentro do mesmo local: a variação do não biométrico acompanha a do comparecimento e o ganho de Lula?
r1 = fe_ols(dNB, dC[:, None], loc, None, ['var_comparecimento'])
r2 = fe_ols(dL, np.column_stack([dNB, dB]), loc, None, ['var_nao_biometricos', 'var_biometricos'])
out['nao_bio_por_eleitor_a_mais'] = {'coef': r1['coef']['var_comparecimento'], 'ep': r1['ep']['var_comparecimento'], 'n': r1['n'], 'locais': r1['grupos']}
out['ganho_lula_por_habilitacao'] = {'coef': r2['coef'], 'ep': r2['ep'], 'n': r2['n']}
json.dump(out, open(saida, 'w'), ensure_ascii=False, indent=1)
print(json.dumps(out, ensure_ascii=False, indent=1))
