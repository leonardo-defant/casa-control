"""T8 do pré-registro: ganho de votos do candidato na seção contra as fontes possíveis, dentro do mesmo local.
y = votos(2T) - votos(1T) do candidato; X = votos de cada grupo de outros candidatos no 1T, queda do branco+nulo,
variação do comparecimento, votos do adversário no 1T e do próprio candidato no 1T.
Efeito fixo de local, sem peso (a regressão é em votos), erro agrupado por local.
Uso: python3 -I analisar_fluxo_regressao.py <secoes.json.gz> <L|R> [--chaves lista] [--candidatos cand.json.gz --grupos 'Renan:30;Caiado:55;...']
"""
import os as _os, sys as _sys
_sys.path.insert(0, _os.path.dirname(_os.path.abspath(__file__)))
import json, sys, warnings
import numpy as np
from lib import carregar, chave_local, fe_ols
warnings.filterwarnings('ignore')

d = carregar(sys.argv[1]); c = sys.argv[2]; adv = 'R' if c == 'L' else 'L'
arg = lambda f: sys.argv[sys.argv.index(f) + 1] if f in sys.argv else None
chaves = set(open(arg('--chaves')).read().split()) if arg('--chaves') else None
cand = carregar(arg('--candidatos'))['secoes'] if arg('--candidatos') else None
grupos = [g.split(':') for g in arg('--grupos').split(';')] if arg('--grupos') else []
rows = []; locs = []
for k, v in d.items():
    if '1' not in v or '2' not in v or (chaves is not None and k not in chaves): continue
    a, b = v['1'], v['2']
    x = []
    if grupos:
        cv = cand.get(k, {}); usados = 0
        for nome, nums in grupos:
            q = sum(cv.get(n, 0) for n in nums.split(',')); x.append(q); usados += q
        x.append(a['O'] - usados)
    else:
        x.append(a['O'])
    x += [(a['B'] + a['N']) - (b['B'] + b['N']), b['comp'] - a['comp'], a[adv], a[c]]
    rows.append([b[c] - a[c]] + x); locs.append(chave_local(k, b))
A = np.array(rows, float)
nomes = ([g[0] for g in grupos] + ['demais_outros'] if grupos else ['outros_1T']) + ['queda_branco_nulo', 'var_comparecimento', 'adversario_1T', 'proprio_1T']
r = fe_ols(A[:, 0], A[:, 1:], np.array(locs), None, nomes)
print(json.dumps({'candidato': c, 'n': r['n'], 'locais': r['grupos'], 'coef': {k: round(v, 3) for k, v in r['coef'].items()},
                  'ep': {k: round(v, 3) for k, v in r['ep'].items()}}, ensure_ascii=False))
