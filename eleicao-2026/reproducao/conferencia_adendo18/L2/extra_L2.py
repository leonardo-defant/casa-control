"""Extras da conferência do L2: urnas reaproveitadas de outra seção (81), juntas no grupo U, U e C no mesmo modelo,
subgrupos de U pela data de carga. Leitura própria do bweb.
Uso: python3 -I extra_L2.py <bweb1t.pkl.gz> <bweb2t.pkl.gz>
"""
import gzip, math, pickle, sys
import numpy as np
import pandas as pd

B1 = pickle.load(gzip.open(sys.argv[1], 'rb'))['secoes']
B2 = pickle.load(gzip.open(sys.argv[2], 'rb'))['secoes']
um = lambda s: next(iter(s['campos']))
urna1 = {}
for k, s in B1.items():
    urna1.setdefault(um(s)[0], []).append(k)
rec = []
for k, s2 in B2.items():
    s1 = B1.get(k)
    if s1 is None or s1['pres'] == 0 or s2['pres'] == 0 or s1['L'] + s1['R'] == 0 or s2['L'] + s2['R'] == 0:
        continue
    f1, f2 = um(s1), um(s2)
    uf, mun, zona, _ = k.split('|')
    outra = [o for o in urna1.get(f2[0], []) if o != k]
    rec.append(dict(k=k, loc=f'{uf}|{mun}|{zona}|{int(f2[10])}', L1=s1['L'], R1=s1['R'], L2=s2['L'], R2=s2['R'],
                    U=float(f1[0] != f2[0]), junta=float(f1[8] != '-1' or f2[8] != '-1'), dt2=f2[4],
                    reuso=float(f1[0] != f2[0] and len(outra) > 0)))
df = pd.DataFrame(rec)
df['y'] = 100 * df.L2 / (df.L2 + df.R2) - 100 * df.L1 / (df.L1 + df.R1)
df['w'] = (df.L2 + df.R2).astype(float)
df['dia2'] = df.dt2.str[:10]


def fe(d, cols, g='loc'):
    """MQP com efeito fixo (within), vários regressores, erro agrupado CR1 (G/(G-1))."""
    x = d[['y', 'w', g] + cols].copy()
    x = x[x.groupby(g)['y'].transform('size') >= 2]
    sw = x.groupby(g)['w'].transform('sum')
    Z = {}
    for c in ['y'] + cols:
        Z[c] = x[c] - (x.w * x[c]).groupby(x[g]).transform('sum') / sw
    X = np.column_stack([Z[c].values for c in cols]); Y = Z['y'].values; W = x.w.values
    XtX = (X * W[:, None]).T @ X
    b = np.linalg.solve(XtX, (X * W[:, None]).T @ Y)
    e = Y - X @ b
    S = pd.DataFrame(X * (W * e)[:, None]).groupby(x[g].values).sum().values
    G = x[g].nunique()
    inv = np.linalg.inv(XtX)
    V = G / (G - 1) * inv @ (S.T @ S) @ inv
    return {c: (round(float(b[i]), 3), round(math.sqrt(V[i, i]), 3), int(x[c].sum())) for i, c in enumerate(cols)}


print('U total', int(df.U.sum()), 'U com junta em algum turno', int((df.U * df.junta).sum()), 'reuso', int(df.reuso.sum()))
print('U e C juntos: precisa do C; aqui U e reuso')
print('reuso (81):', fe(df, ['reuso']))
print('U sem juntas:', fe(df[df.junta == 0], ['U']))
df['U_pre'] = df.U * (df.dia2 < '2026-10-04'); df['U_pos'] = df.U * (df.dia2 > '2026-10-04')
df['M_pos'] = (1 - df.U) * (df.dia2 > '2026-10-04')
print('U pre 1T:', fe(df, ['U_pre'])); print('U pos 1T:', fe(df, ['U_pos'])); print('mesma urna, carga depois do 1T:', fe(df, ['M_pos']))
print('U_pre, U_pos e M_pos juntos:', fe(df, ['U_pre', 'U_pos', 'M_pos']))
