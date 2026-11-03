"""Conferência PAINEL, passo 8: robustez do passo 5 com a virada (y2 - y1) como variável dependente, em vez de y1 como
controle (coeficiente forçado a 1). Mesmos dados, pesos e agrupamento do passo 5 (importa as funções de lá).
Decisão fixada antes de rodar: efeito fixo de município e de local; regressores f_cm, f_na, f_dn, f_S e, à parte, f_sb.
Também a soma nacional de sm1 e sm2 (SemMes 1º e 2º turno) e de c - b nos dois turnos, só nas seções pareadas (par = 1).
Uso: python3 -I p8_virada.py <tabela.html.gz> <secoes2026.json.gz>
"""
import gzip, json, re, sys
sys.path.insert(0, '/home/user/trabalho-eleicao/conferencia_adendo24/PAINEL/scripts')
import numpy as np
from p5_regressoes import ler, fe_wls

rows = ler(sys.argv[1], sys.argv[2])
a = np.array([[np.nan if x is None else x for x in r] for r in rows], dtype=float)
uf, mun, loc, c2, b2, cm2, sm2, na2, dn2, L2, R2, L1, R1, p13_1 = [a[:, j] for j in range(14)]
y2 = L2 / (L2 + R2); y1 = L1 / (L1 + R1); w = L2 + R2
X = np.column_stack([cm2 / c2, na2 / c2, dn2 / c2, (c2 - b2 - cm2 - sm2) / c2])
gm = uf * 100000 + mun; gl = gm * 100000 + loc
out = {}
for nome, g in (('virada_mun', gm), ('virada_local', gl)):
    b, ep = fe_wls(y2 - y1, X, w, g, gm)
    out[nome] = {n: [round(float(b[j]), 4), round(float(ep[j]), 4)] for j, n in enumerate(['f_cm', 'f_na', 'f_dn', 'f_S'])}
    b, ep = fe_wls(y2 - y1, ((c2 - b2) / c2)[:, None], w, g, gm)
    out[nome]['f_sb_sozinha'] = [round(float(b[0]), 4), round(float(ep[0]), 4)]
print(json.dumps(out, indent=1))
src = gzip.open(sys.argv[1], 'rb').read().decode('utf-8', errors='replace')
m = re.search(r'<script id="raw-data" type="text/plain">', src)
corpo = src[m.end():src.find('</script>', m.end())].strip('\n')
s = dict(sm1=0, sm2=0, c1b1=0, c2b2=0, n=0)
for ln in corpo.split('\n'):
    p = ln.strip().split(',')
    if len(p) != 40 or p[7] != '1':
        continue
    s['n'] += 1; s['sm1'] += int(p[23]); s['sm2'] += int(p[24])
    s['c1b1'] += int(p[8]) - int(p[17]); s['c2b2'] += int(p[9]) - int(p[18])
print(s)
