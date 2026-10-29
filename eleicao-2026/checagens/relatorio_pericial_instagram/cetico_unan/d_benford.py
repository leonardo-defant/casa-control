import pickle, json
import numpy as np
from scipy.stats import chi2
P = '/tmp/claude-0/-home-user-casa-control/ce2a8c88-e5ad-504f-8950-6f5ee14ae721/scratchpad/relatorio_pericial/cetico_unan/'
B1 = np.log10(1 + 1/np.arange(1, 10))
B2 = np.array([sum(np.log10(1 + 1/(10*k + d)) for k in range(1, 10)) for d in range(10)])
M2 = float((np.arange(10)*B2).sum())
def fd(x):
    x = x[x > 0]; s = np.char.str_len(x.astype(str))  # dígitos
    f = x // 10**(s-1)
    o = np.bincount(f, minlength=10)[1:]; return o / o.sum(), o
def sd(x):
    x = x[x >= 10]; s = np.char.str_len(x.astype(str))
    d = (x // 10**(s-2)) % 10
    return d
def res(x):
    p, o = fd(x); n = o.sum()
    q = float(((o - n*B1)**2/(n*B1)).sum())
    d = sd(x); u = x[x >= 10] % 10; ou = np.bincount(u, minlength=10); nu = ou.sum()
    qu = float(((ou - nu/10)**2/(nu/10)).sum())
    return {'d1_pct': round(100*p[0], 2), 'MAD1': round(float(np.abs(p - B1).mean()), 4), 'p1': float(chi2.sf(q, 8)),
            'media2BL': round(float(d.mean()), 3), 'z2BL': round((d.mean()-M2)/(d.std()/np.sqrt(len(d))), 1),
            'p_ultimo': round(float(chi2.sf(qu, 9)), 3), '1-9': round(100*float(((x>=1)&(x<=9)).mean()), 2),
            '10-99': round(100*float(((x>=10)&(x<=99)).mean()), 2), '100+': round(100*float((x>=100).mean()), 2), 'zero': round(100*float((x==0).mean()),2)}
rng = np.random.default_rng(1)
out = {'media2BL_esperada': M2}
for a, t in (('2026', '2'), ('2026', '1'), ('2022', '2'), ('2018', '2')):
    s = pickle.load(open(P + f'{a}.pkl', 'rb'))[t]
    L, R, O = s['L'], s['R'], s['O']; V = L + R + O; ok = V > 0
    r = {'L': res(L[ok]), 'R': res(R[ok]), 'apt': res(s['apt'][ok])}
    # sintético com a fatia NACIONAL (sem informação local), mesmo V por seção
    pL = L.sum()/V.sum(); pR = R.sum()/V.sum()
    sL = rng.binomial(V, pL); sR = rng.binomial(V - sL, pR/(1-pL))
    r['sintNac_L'] = res(sL[ok]); r['sintNac_R'] = res(sR[ok])
    # sintético com fatia da UF
    uf = np.array([k.split('|')[0] for k in s['k']]); _, g = np.unique(uf, return_inverse=True)
    fl = np.bincount(g, weights=L)/np.bincount(g, weights=V); fr = np.bincount(g, weights=R)/np.bincount(g, weights=V)
    sL = rng.binomial(V, fl[g]); sR = rng.binomial(V - sL, np.clip(fr[g]/(1-fl[g]), 0, 1))
    r['sintUF_L'] = res(sL[ok]); r['sintUF_R'] = res(sR[ok])
    if a == '2026' and t == '2':
        r['apt_mediana'] = float(np.median(s['apt'])); r['apt_p99'] = float(np.percentile(s['apt'], 99)); r['apt_max'] = int(s['apt'].max())
    out[f'{a}_{t}T'] = r
    print(a, t, json.dumps(r, ensure_ascii=False), flush=True)
json.dump(out, open(P + 'd_benford.json', 'w'), indent=1, ensure_ascii=False)
