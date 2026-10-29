import pickle, json, math, collections
import numpy as np
P = '/tmp/claude-0/-home-user-casa-control/ce2a8c88-e5ad-504f-8950-6f5ee14ae721/scratchpad/relatorio_pericial/cetico_unan/'
D = {a: pickle.load(open(P + f'{a}.pkl', 'rb')) for a in ('2026', '2022', '2018')}
out = {}
def conta(s, todos=False, so_apurada=False):
    L, R, O = s['L'].astype(float), s['R'].astype(float), s['O'].astype(float)
    V = L + R + (O if todos else 0)
    ok = V > 0
    if so_apurada:
        ok &= np.char.upper(s['tipo']) == 'APURADA'
    sL = np.where(ok, L / np.where(V > 0, V, 1), np.nan); sR = np.where(ok, R / np.where(V > 0, V, 1), np.nan)
    ext = np.array([k.startswith('ZZ|') for k in s['k']])
    r = {'secoes': int(len(L)), 'com_valido': int(ok.sum()),
         'L100': int((ok & (L == V)).sum()), 'R100': int((ok & (R == V)).sum()),
         'L>=90': int((sL >= .9).sum()), 'R>=90': int((sR >= .9).sum()),
         'L>90': int((sL > .9).sum()), 'R>90': int((sR > .9).sum()),
         'L>=90_semZZ': int(((sL >= .9) & ~ext).sum()), 'R>=90_semZZ': int(((sR >= .9) & ~ext).sum()),
         'L100_ZZ': int((ok & (L == V) & ext).sum()), 'R100_ZZ': int((ok & (R == V) & ext).sum()),
         'L>=90_ZZ': int(((sL >= .9) & ext).sum()), 'R>=90_ZZ': int(((sR >= .9) & ext).sum()),
         'fatia_nac_L': float(L.sum() / V.sum()), 'L_tot': int(L.sum()), 'R_tot': int(R.sum()), 'margem': int(L.sum() - R.sum()),
         'comp_tot': int(s['comp'].sum())}
    # >90% do comparecimento
    c = s['comp'].astype(float)
    r['L>90comp'] = int(((c > 0) & (L / np.maximum(c, 1) > .9)).sum()); r['R>90comp'] = int(((c > 0) & (R / np.maximum(c, 1) > .9)).sum())
    x = sL[~np.isnan(sL)]
    mu, sd = x.mean(), x.std()
    r['media'] = mu; r['dp'] = sd; r['assim'] = float(((x-mu)**3).mean()/sd**3); r['curt_exc'] = float(((x-mu)**4).mean()/sd**4-3)
    n = len(x)
    r['normal_L>=90'] = n*0.5*math.erfc((0.9-mu)/sd/math.sqrt(2)); r['normal_R>=90'] = n*0.5*math.erfc((mu-0.1)/sd/math.sqrt(2))
    # saldo líquido nas seções extremas
    mL = sL >= .9; mR = sR >= .9
    r['saldo_L_nas_L90'] = int((L - R)[mL].sum()); r['saldo_R_nas_R90'] = int((R - L)[mR].sum())
    r['saldo_liquido_extremos'] = r['saldo_L_nas_L90'] - r['saldo_R_nas_R90']
    return r, sL, ok
for a in D:
    for t in ('1', '2'):
        s = D[a][t]
        r, sL, ok = conta(s)
        out[f'{a}_{t}T_dois'] = r
        if t == '1':
            out[f'{a}_{t}T_todos'] = conta(s, todos=True)[0]
        if a != '2026':
            out[f'{a}_{t}T_dois_soApurada'] = {k: v for k, v in conta(s, so_apurada=True)[0].items() if k in ('L100', 'R100', 'L>=90', 'R>=90')}
# detalhes 2026 2T
s2 = D['2026']['2']; s1 = D['2026']['1']
L, R = s2['L'], s2['R']; V = L + R
m106 = (V > 0) & (R == 0); m4 = (V > 0) & (L == 0)
out['106'] = {'n': int(m106.sum()), 'comp_mediano': float(np.median(s2['comp'][m106])), 'comp_mediano_pais': float(np.median(s2['comp'])),
              'L_soma': int(L[m106].sum()), 'pct_margem': 100*L[m106].sum()/(L.sum()-R.sum()),
              'UF': collections.Counter([k.split('|')[0] for k in s2['k'][m106]]).most_common(8),
              'min_valid': int(V[m106].min()), 'n_valid<=20': int((V[m106] <= 20).sum())}
out['4'] = {'chaves': s2['k'][m4].tolist(), 'votos': [(int(a), int(b), int(c)) for a, b, c in zip(L[m4], R[m4], s2['comp'][m4])]}
# persistência no 1T (mesma chave)
i1 = {k: i for i, k in enumerate(s1['k'])}
V1 = s1['L'] + s1['R'] + s1['O']
f1 = []
for k in s2['k'][m106]:
    i = i1[k]; f1.append(s1['L'][i] / V1[i] if V1[i] > 0 else np.nan)
f1 = np.array(f1)
out['106_no_1T'] = {'n': len(f1), '>=90': int((f1 >= .9).sum()), 'mediana': float(np.nanmedian(f1)), 'min': float(np.nanmin(f1))}
# casamento com 2022 e 2018 por chave
def casar(a, mask):
    s = D[a]['2']; ix = {k: i for i, k in enumerate(s['k'])}
    VV = s['L'] + s['R']
    fs = []
    for k in s2['k'][mask]:
        if k in ix and VV[ix[k]] > 0:
            fs.append(s['L'][ix[k]] / VV[ix[k]])
    fs = np.array(fs)
    return {'casadas': len(fs), '>=90': int((fs >= .9).sum()), '>=80': int((fs >= .8).sum()), 'mediana': float(np.median(fs)) if len(fs) else None}
sL2 = np.where(V > 0, L / np.maximum(V, 1), np.nan)
out['106_vs_2022'] = casar('2022', m106); out['106_vs_2018'] = casar('2018', m106)
out['6899_vs_2022'] = casar('2022', sL2 >= .9)
# correlação seção a seção 2022-2026
s22 = D['2022']['2']; ix = {k: i for i, k in enumerate(s22['k'])}
a_, b_ = [], []
for j, k in enumerate(s2['k']):
    i = ix.get(k)
    if i is not None and s22['L'][i] + s22['R'][i] > 0 and V[j] > 0:
        a_.append(s22['L'][i] / (s22['L'][i] + s22['R'][i])); b_.append(sL2[j])
a_, b_ = np.array(a_), np.array(b_)
out['corr_2022_2026'] = {'n': len(a_), 'r': float(np.corrcoef(a_, b_)[0, 1]), 'mudanca_media_pp': float(100*(b_ - a_).mean())}
# mesmo local de votação? checa se loc bate
json.dump(out, open(P + 'b_contagens.json', 'w'), indent=1, ensure_ascii=False, default=float)
for k, v in out.items():
    print(k, json.dumps(v, ensure_ascii=False, default=float))
