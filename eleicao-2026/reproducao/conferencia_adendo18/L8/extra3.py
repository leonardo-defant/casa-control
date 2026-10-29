"""Conferência L8: virada de Lula nas seções tardias com efeito fixo de zona e de município (inclui os locais todos tardios,
que o efeito fixo de local descarta). Erro agrupado pelo mesmo nível do efeito fixo. Leitura minha, fora do registro."""
import datetime as dt, json, os, sys
import numpy as np
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from conferir import ler, P, DIA, fe_cluster
from extra import desloc
T = {1: ler(sys.argv[1]), 2: ler(sys.argv[2])}
lims = {'17h15m59': DIA[2].replace(hour=17, minute=15, second=59), '18h59m59': DIA[2].replace(hour=18, minute=59, second=59)}
y, w, gz, gm, gl, X = [], [], [], [], [], {n: [] for n in lims}
for k, s2 in T[2].items():
    if k.startswith('ZZ') or k not in T[1]:
        continue
    s1 = T[1][k]
    if s1['L'] + s1['R'] == 0 or s2['L'] + s2['R'] == 0:
        continue
    e = P(s2['enc']) + dt.timedelta(hours=desloc(k))
    y.append(100 * (s2['L'] / (s2['L'] + s2['R']) - s1['L'] / (s1['L'] + s1['R']))); w.append(s2['L'] + s2['R'])
    uf, mu, z, _ = k.split('|'); gz.append(f'{uf}|{mu}|{z}'); gm.append(f'{uf}|{mu}'); gl.append(f'{uf}|{mu}|{z}|{s2["loc"]}')
    for n, l in lims.items():
        X[n].append(float(e > l))
R = {}
for n in lims:
    for nome, g in (('local', gl), ('zona', gz), ('municipio', gm)):
        R[f'{n}|{nome}'] = fe_cluster(y, np.array(X[n])[:, None], np.array(g), w)
json.dump(R, open(sys.argv[3], 'w'), indent=1)
print(json.dumps(R))
