"""Conferência do 'fora de casa', do país e da calibração com regressão própria (reg de conf_L4.py) sobre a base por seção."""
import gzip, json, sys
import numpy as np
sys.path.insert(0, sys.argv[3])
from conf_L4 import reg, GRUPOS, CASA
d = json.load(gzip.open(sys.argv[1], 'rt')); cand = json.load(gzip.open(sys.argv[2], 'rt'))['secoes']
rows, uf, loc = [], [], []
for k, v in d.items():
    if '1' not in v or '2' not in v: continue
    a, b = v['1'], v['2']; cv = cand.get(k, {})
    g = [cv.get(str(n), 0) for n in GRUPOS.values()]
    rows.append(g + [a['O'] - sum(g), (a['B'] + a['N']) - (b['B'] + b['N']), b['comp'] - a['comp'], a['L'], a['R'], b['L'], b['R']])
    u, m, z, _ = k.split('|'); uf.append(u); loc.append(f'{u}|{m}|{z}|{b["loc"]}')
M = np.array(rows, float); uf = np.array(uf); loc = np.array(loc)
nomes = list(GRUPOS) + ['dem', 'qbn', 'dcomp', 'adv', 'prop']
def s_de(mask, L2=None, R2=None):
    X = M[mask]; L1, R1 = X[:, 7], X[:, 8]
    L2 = X[:, 9] if L2 is None else L2[mask]; R2 = X[:, 10] if R2 is None else R2[mask]
    base = X[:, :7]
    bl, el, *_ = reg(L2 - L1, np.column_stack([base, R1, L1]), loc[mask], nomes)
    bf, ef, *_ = reg(R2 - R1, np.column_stack([base, L1, R1]), loc[mask], nomes)
    return {g: (bl[g] / (bl[g] + bf[g]), el[g]) for g in GRUPOS}
out = {'secoes': int(len(uf))}
out['pais'] = s_de(np.ones(len(uf), bool))
print('país', {g: (round(a, 4), round(b, 4)) for g, (a, b) in out['pais'].items()}, flush=True)
for u, c in CASA.items():
    fo = s_de(uf != u)[c]; out['fora_' + c] = fo
    print('fora', c, round(fo[0], 4), round(fo[1], 4), flush=True)
L2, R2 = M[:, 9], M[:, 10]
f = (L2.sum() - R2.sum()) / (2 * R2.sum()); out['f_vira'] = f
print('f_vira', f, 'Lula 2T nacional', L2.sum(), 'Flavio', R2.sum())
for u, c in CASA.items():
    for nome, ff in (('1pct', 0.01), ('vira', f), ('menos_vira', -f)):
        x = s_de(uf == u, L2 + ff * R2, R2 - ff * R2)[c]
        out[f'calib_{nome}_{u}'] = x
        print('calib', nome, u, round(x[0], 4), flush=True)
json.dump(out, open(sys.argv[4], 'w'), indent=1, default=float)
