"""Teste por modelo de urna dentro do mesmo local de votação (critério da seção 7).

Locais com 2 ou mais modelos no 2º turno; dummies de modelo contra a referência (2022: UE2020; 2026: UE2022);
efeito fixo de local, peso pelos votos no 13 + direita no 2º turno, erro agrupado por local.
Desfechos: virada do 13 (fatia entre os finalistas, mesma seção e mesmo modelo nos dois turnos), variação do
branco+nulo (% do comparecimento, mesma seção e mesmo modelo) e fatia do 13 no 2º turno.
Reproduz 2022 do documento: 10.748 locais, 82.758 seções; virada -0,16 a -0,18 (0,12); fatia +0,24 a +0,37 (0,30).
Uso: python3 -I analisar_modelos.py <secoes.json.gz> <ano> [--chaves lista.txt]
"""
import os as _os, sys as _sys
_sys.path.insert(0, _os.path.dirname(_os.path.abspath(__file__)))
import collections, json, sys, warnings
import numpy as np
from lib import carregar, chave_local, fe_ols
from modelos import modelo
warnings.filterwarnings('ignore')

d = carregar(sys.argv[1]); ano = int(sys.argv[2])
chaves = set(open(sys.argv[sys.argv.index('--chaves') + 1]).read().split()) if '--chaves' in sys.argv else None
ref = 'UE2020' if ano == 2022 else 'UE2022'
rows = []
for k, v in d.items():
    if '1' not in v or '2' not in v or (chaves is not None and k not in chaves): continue
    a, b = v['1'], v['2']
    rows.append((chave_local(k, b), modelo(a['urna'], ano), modelo(b['urna'], ano), a, b))
porloc = collections.defaultdict(set)
for r in rows:
    if r[2] is not None: porloc[r[0]].add(r[2])
sel = [r for r in rows if len(porloc[r[0]]) >= 2 and r[2] is not None]
mods = sorted({r[2] for r in sel} - {ref})
loc = np.array([r[0] for r in sel])
D = np.array([[1.0 if r[2] == m else 0.0 for m in mods] for r in sel])
g = lambda i, c: np.array([r[i][c] for r in sel], float)
L1, R1, B1, N1, C1 = [g(3, c) for c in 'L R B N comp'.split()]
L2, R2, B2, N2, C2 = [g(4, c) for c in 'L R B N comp'.split()]
mm = np.array([r[1] == r[2] for r in sel])
V2 = L2 + R2
ok = (C1 > 0) & (C2 > 0) & (L1 + R1 > 0) & (V2 > 0)
saida = {'ano': ano, 'referencia': ref, 'locais_mistos': int(len({r[0] for r in sel})), 'secoes': int(len(sel)),
         'contagem_modelos_2T': dict(collections.Counter(r[2] for r in sel)), 'desfechos': {}}
for nome, y, filtro in [('virada', 100 * (L2 / V2 - L1 / (L1 + R1)), mm),
                        ('var_branco_nulo', 100 * ((B2 + N2) / C2 - (B1 + N1) / C1), mm),
                        ('fatia13_2T', 100 * L2 / V2, np.ones(len(sel), bool))]:
    o = ok & filtro & np.isfinite(y)
    r = fe_ols(y[o], D[o], loc[o], V2[o], mods)
    saida['desfechos'][nome] = {'n': r['n'], 'locais': r['grupos'], 'coef': r['coef'], 'ep': r['ep']}
# critério: virada > 0,5 e > 3 ep, ou queda de branco+nulo > 0,5 (coef < -0,5) e > 3 ep
bandeira = []
for m in mods:
    v = saida['desfechos']['virada']; b = saida['desfechos']['var_branco_nulo']
    if v['coef'][m] > 0.5 and v['coef'][m] > 3 * v['ep'][m]: bandeira.append(f'{m}: virada')
    if b['coef'][m] < -0.5 and -b['coef'][m] > 3 * b['ep'][m]: bandeira.append(f'{m}: queda do branco+nulo')
saida['bandeira_vermelha'] = bandeira
print(json.dumps(saida, ensure_ascii=False, indent=1))
