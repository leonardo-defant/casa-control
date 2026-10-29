import sys, numpy as np, pandas as pd
sys.path.insert(0, sys.argv[1])
from conf_L4 import reg, GRUPOS, CASA
nomes = list(GRUPOS) + ['dem', 'qbn', 'dcomp', 'adv', 'prop']
for uf, c in CASA.items():
    m = pd.read_csv(f'{sys.argv[1]}/extr/base_{uf}.csv.gz', index_col=0)
    dem = m['O1'] - m[list(GRUPOS)].sum(axis=1); qbn = (m['B1'] + m['N1']) - (m['B2'] + m['N2']); dc = m['comp2'] - m['comp1']
    base = np.column_stack([m[list(GRUPOS)].values, dem, qbn, dc]).astype(float)
    XL = np.column_stack([base, m['R1'], m['L1']]); XF = np.column_stack([base, m['L1'], m['R1']])
    yL = (m['L2'] - m['L1']).values.astype(float); yF = (m['R2'] - m['R1']).values.astype(float)
    V1 = (m['L1'] + m['R1'] + m['O1']).values
    sh = np.where(V1 > 0, m[c].values / np.where(V1 > 0, V1, 1), 0)
    q1, q2 = np.quantile(sh, [1/3, 2/3]); lk = m['lockey'].values
    out = []
    for sel in (sh <= q1, (sh > q1) & (sh <= q2), sh > q2):
        bl, el, *_ = reg(yL[sel], XL[sel], lk[sel], nomes); bf, *_ = reg(yF[sel], XF[sel], lk[sel], nomes)
        out.append(f'{100*bl[c]/(bl[c]+bf[c]):.1f} ({100*el[c]:.2f})')
    # peso pelo comparecimento do 1º turno (WLS within ponderado)
    w = m['comp1'].values.astype(float)
    def wreg(y, X):
        d = pd.DataFrame(np.column_stack([y, X])); g = pd.Series(lk)
        cnt = g.map(g.value_counts()).values; ok = cnt >= 2
        d, ww, gg = d[ok].reset_index(drop=True), w[ok], g[ok].reset_index(drop=True)
        dw = d.mul(ww, axis=0); mu = dw.groupby(gg).transform('sum').div(pd.Series(ww).groupby(gg).transform('sum'), axis=0)
        Z = (d - mu).values; s = np.sqrt(ww)
        return np.linalg.lstsq(Z[:, 1:] * s[:, None], Z[:, 0] * s, rcond=None)[0]
    i = list(GRUPOS).index(c); bLw = wreg(yL, XL)[i]; bFw = wreg(yF, XF)[i]
    # Renan na UF para comparação de distância
    bl, *_ = reg(yL, XL, lk, nomes); bf, *_ = reg(yF, XF, lk, nomes)
    print(uf, c, 'tercos', out, 'cortes', round(100*q1, 1), round(100*q2, 1), 'peso', round(100*bLw/(bLw+bFw), 1), 'Renan', round(100*bl['Renan']/(bl['Renan']+bf['Renan']), 1))
