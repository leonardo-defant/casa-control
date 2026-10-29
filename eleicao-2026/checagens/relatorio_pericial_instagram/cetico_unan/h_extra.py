import pickle, collections, json
import numpy as np
Q = '/tmp/claude-0/-home-user-casa-control/ce2a8c88-e5ad-504f-8950-6f5ee14ae721/scratchpad/relatorio_pericial/cetico_unan/'
LOC, nsl = pickle.load(open(Q + 'locais.pkl', 'rb'))
s = pickle.load(open(Q + '2026.pkl', 'rb'))['2']
ks = s['k']; L, R = s['L'], s['R']; V = L + R; sL = L/np.maximum(V, 1); sR = R/np.maximum(V, 1)
uf = np.array([k.split('|')[0] for k in ks])
print('L>=90 UF', collections.Counter(uf[sL >= .9]).most_common(6))
print('R>=90 UF', collections.Counter(uf[(V > 0) & (sR >= .9)]).most_common(6))
mPA = (V > 0) & (sR >= .9) & (uf == 'PA')
print('PA R>=90 por município', collections.Counter(LOC[k][0] for k in ks[mPA]).most_common(12))
a = s['apt']; f = a // 10**(np.char.str_len(a.astype(str)) - 1)
print('aptos 1o digito %', {d: round(100*float((f == d).mean()), 1) for d in range(1, 10)})
# comp nas L>=90 e excesso de NH vs taxa nacional
print('comp L>=90 BR', int(s['comp'][(sL >= .9) & (uf != 'ZZ')].sum()))
