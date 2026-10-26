"""T5 do pré-registro: dentro do mesmo local, inclinação do branco+nulo de presidente (beta) e da fatia do 13 (gama)
contra o branco+nulo de governador na mesma urna. Peso pelo comparecimento, erro agrupado por local.
Uso: python3 -I analisar_pres_gov_nivel.py <secoes.json.gz> <turno 1|2> [--ufs AC,AM] [--chaves lista.txt]
"""
import os as _os, sys as _sys
_sys.path.insert(0, _os.path.dirname(_os.path.abspath(__file__)))
import json, sys, warnings
import numpy as np
from lib import carregar, chave_local, fe_ols
warnings.filterwarnings('ignore')

d = carregar(sys.argv[1]); t = sys.argv[2]
ufs = set(sys.argv[sys.argv.index('--ufs') + 1].split(',')) if '--ufs' in sys.argv else None
chaves = set(open(sys.argv[sys.argv.index('--chaves') + 1]).read().split()) if '--chaves' in sys.argv else None
sel = [(chave_local(k, v[t]), v[t], v[t + 'g']) for k, v in d.items() if t in v and t + 'g' in v
       and (ufs is None or k.split('|')[0] in ufs) and (chaves is None or k in chaves)]
loc = np.array([s[0] for s in sel])
C = np.array([s[1]['comp'] for s in sel], float); gC = np.array([s[2]['comp'] for s in sel], float)
BNp = np.array([s[1]['B'] + s[1]['N'] for s in sel], float); L = np.array([s[1]['L'] for s in sel], float)
BNg = np.array([s[2]['B'] + s[2]['N'] for s in sel], float)
ok = (C > 0) & (gC > 0)
x = (100 * BNg / gC)[:, None]
rb = fe_ols((100 * BNp / C)[ok], x[ok], loc[ok], C[ok], ['bn_gov'])
rg = fe_ols((100 * L / C)[ok], x[ok], loc[ok], C[ok], ['bn_gov'])
print(json.dumps({'turno': t, 'n': rb['n'], 'locais': rb['grupos'],
                  'bn_pres_medio': float(100 * BNp[ok].sum() / C[ok].sum()), 'bn_gov_medio': float(100 * BNg[ok].sum() / gC[ok].sum()),
                  'beta': rb['coef']['bn_gov'], 'beta_ep': rb['ep']['bn_gov'],
                  'gama': rg['coef']['bn_gov'], 'gama_ep': rg['ep']['bn_gov']}))
