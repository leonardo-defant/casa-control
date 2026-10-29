"""Conferência independente do L3 (Adendo 18). Código próprio: matriz montada do zero a partir da base por seção,
dos votos por candidato do 1º turno e da minha leitura do deputado federal (ler_df.py); efeito fixo por demeaning com
pandas groupby e erro agrupado CR1 calculado à parte (não usa lib.fe_ols nem ols_cluster).
Uso: python3 -I conferir.py <secoes2026.json.gz> <candidatos2026_1t.json.gz> <df_meu.csv.gz> <saida.json>
"""
import gzip, json, sys, time
import numpy as np
import pandas as pd

t0 = time.time()
sec_p, cand_p, df_p, out_p = sys.argv[1:5]
with gzip.open(sec_p, 'rt') as f:
    d = json.load(f)
with gzip.open(cand_p, 'rt') as f:
    cand = json.load(f)['secoes']
DF = pd.read_csv(df_p, index_col=0)

rows = []
for k, v in d.items():
    if '1' not in v or '2' not in v:
        continue
    uf, mun, zona, sec = k.split('|')
    a, b = v['1'], v['2']
    cv = cand.get(k, {})
    rows.append((k, uf, f"{uf}|{mun}|{zona}|{b['loc']}", f"{uf}|{mun}|{zona}|{a['loc']}",
                 a['L'], a['R'], a['O'], a['B'], a['N'], a['comp'], b['L'], b['R'], b['B'], b['N'], b['comp'],
                 cv.get('70', 0), cv.get('14', 0), cv.get('55', 0), cv.get('30', 0), a['urna'], b['urna']))
del d, cand
B = pd.DataFrame(rows, columns=['k', 'uf', 'loc2', 'loc1', 'L1', 'R1', 'O1', 'B1', 'N1', 'comp1', 'L2', 'R2', 'B2', 'N2',
                                'comp2', 'Cury', 'Renan', 'Caiado', 'Zema', 'urna1', 'urna2']).set_index('k')
res = {'secoes_dois_turnos': int(len(B)), 'exterior': int((B.uf == 'ZZ').sum())}
B = B[B.uf != 'ZZ'].join(DF, how='left')
res['sem_df'] = int(B.validos.isna().sum())
B = B[B.validos.notna() & (B.validos > 0)].copy()
res['universo'] = int(len(B)); res['locais'] = int(B.loc2.nunique())
# conferências da minha leitura
res['conf'] = {
    'soma_df_dif_comp': int(((B.validos + B.bra + B.nul) != B.comp_max).sum()),
    'comp_varia_na_secao': int((B.comp_min != B.comp_max).sum()),
    'outro_tipo_votos': int(B.outro_tipo.sum()),
    'pl_partido_dif_prefixo': int((B.pl != B.pl_prefixo).sum()),
    'pt_partido_dif_prefixo': int((B.pt != B.pt_prefixo).sum()),
    'comp_df_menor_que_pres': int((B.comp_max < B.comp1).sum()),
    'comp_df_maior_que_pres': int((B.comp_max > B.comp1).sum()),
    'eleitores_a_mais_pres': int((B.comp1 - B.comp_max).clip(lower=0).sum()),
    'tot_validos': int(B.validos.sum()), 'tot_pl': int(B.pl.sum()), 'tot_pt': int(B.pt.sum()),
    'tot_leg': int(B.leg.sum()), 'tot_bra': int(B.bra.sum()), 'tot_nul': int(B.nul.sum()),
}
B['fPL'] = B.pl / B.validos
B['fPT'] = B.pt / B.validos
V1 = B.L1 + B.R1 + B.O1
B['fL1'] = B.L1 / V1.where(V1 > 0)
B['fR1'] = B.R1 / V1.where(V1 > 0)
res['corr'] = {'PL_Flavio': float(B.fPL.corr(B.fR1)), 'PT_Lula': float(B.fPT.corr(B.fL1))}


def fe_reg(sub, cand, loc='loc2', ycol=None, extra=None):
    """y = votos 2T - 1T do candidato; X = grupos, demais, queda B+N, var comp, adversário 1T, próprio 1T.
    Efeito fixo de local por demeaning (pandas), CR1 agrupado por local."""
    adv = 'R' if cand == 'L' else 'L'
    X = pd.DataFrame({'Cury': sub.Cury, 'Renan': sub.Renan, 'Caiado': sub.Caiado, 'Zema': sub.Zema,
                      'demais': sub.O1 - sub.Cury - sub.Renan - sub.Caiado - sub.Zema,
                      'qbn': (sub.B1 + sub.N1) - (sub.B2 + sub.N2), 'dcomp': sub.comp2 - sub.comp1,
                      'adv': sub[adv + '1'], 'prop': sub[cand + '1']}, index=sub.index).astype(float)
    y = (sub[cand + '2'] - sub[cand + '1']).astype(float) if ycol is None else ycol.loc[sub.index].astype(float)
    g = sub[loc]
    n_g = g.map(g.value_counts())
    keep = n_g >= 2
    X, y, g = X[keep], y[keep], g[keep]
    Xd = X - X.groupby(g).transform('mean')
    yd = y - y.groupby(g).transform('mean')
    Xm, ym = Xd.values, yd.values
    XtX = Xm.T @ Xm
    beta = np.linalg.solve(XtX, Xm.T @ ym)
    e = ym - Xm @ beta
    sc = pd.DataFrame(Xm * e[:, None]).groupby(g.values).sum().values
    inv = np.linalg.inv(XtX)
    N, k = Xm.shape; G = sc.shape[0]
    V = G / (G - 1) * (N - 1) / (N - k) * inv @ (sc.T @ sc) @ inv
    j = list(X.columns).index('prop')
    return {'P': float(beta[j]), 'ep': float(np.sqrt(V[j, j])), 'n': int(N), 'G': int(G)}


def veredito(P1, P5, ep5):
    inc = P5 <= -0.03 and P5 / ep5 < -3 and abs(P1) - abs(P5) <= 0.01
    coe = abs(P5) <= 0.5 * abs(P1)
    return 'INCOERÊNCIA' if inc else ('COERENTE' if coe else 'INCONCLUSIVO')


def por_quintil(cand, fat, cortes=None, peso=None, loc='loc2', mask=None, ycol=None):
    sub = B if mask is None else B[mask]
    f = sub[fat]
    if cortes is None:
        if peso is None:
            cortes = np.quantile(B[fat] if mask is None else f, [.2, .4, .6, .8])
        else:
            o = np.argsort(f.values); cw = np.cumsum(sub[peso].values[o]) / sub[peso].values.sum()
            cortes = [float(f.values[o][np.searchsorted(cw, p)]) for p in (.2, .4, .6, .8)]
    q = np.searchsorted(cortes, f.values, side='left')
    out = []
    for j in range(5):
        r = fe_reg(sub[q == j], cand, loc, ycol)
        r['secoes'] = int((q == j).sum())
        out.append(r)
    return {'cortes': [float(c) for c in cortes], 'Q': out, 'veredito': veredito(out[0]['P'], out[4]['P'], out[4]['ep']),
            'razao_P5_P1': abs(out[4]['P']) / abs(out[0]['P'])}


def resumo(nome, r):
    s = ' | '.join(f"Q{i+1} {x['P']:+.4f} ({x['ep']:.4f}) n={x['n']} G={x['G']}" for i, x in enumerate(r['Q']))
    print(f"{nome}: {r['veredito']} |P5|/|P1|={r['razao_P5_P1']:.3f} cortes={[round(c,4) for c in r['cortes']]}\n   {s}",
          flush=True)


R = {}
R['principal_Flavio_PL'] = por_quintil('R', 'fPL'); resumo('Flávio x PL (principal)', R['principal_Flavio_PL'])
R['principal_Lula_PT'] = por_quintil('L', 'fPT'); resumo('Lula x PT (espelho)', R['principal_Lula_PT'])
R['geral_Flavio'] = fe_reg(B, 'R'); R['geral_Lula'] = fe_reg(B, 'L')
print('geral', R['geral_Flavio'], R['geral_Lula'], flush=True)
res['R'] = R
res['segundos'] = time.time() - t0
B.to_pickle(out_p.replace('.json', '_B.pkl'))
with open(out_p, 'w') as f:
    json.dump(res, f, ensure_ascii=False, indent=1)
print(json.dumps({k: v for k, v in res.items() if k != 'R'}, ensure_ascii=False, indent=1))
