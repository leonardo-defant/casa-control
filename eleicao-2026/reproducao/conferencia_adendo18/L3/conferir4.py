"""O que cada estimador enxerga: dados sintéticos com X real e y gerado por regras conhecidas.
DGP1: o eleitor de Flávio que votou no PL para deputado nunca troca; os demais eleitores de Flávio trocam 8%.
DGP2: perda plana de 4% (o que uma fração fixa desviada, sem comportamento, deixaria).
DGP3: sem efeito do partido; a perda cresce com a força de Lula no local (contexto): 12% x fatia de Lula no local.
Em todos: ganhos dos outros grupos fixos (Binomial) e o mesmo resto. Compara as regressões separadas por quintil
(leitura registrada) com o empilhado de efeito fixo de local comum.
Também: regressão dentro do local com os votos do PL para deputado como regressor extra (dados reais).
Uso: python3 -I conferir4.py <conferir_B.pkl> <saida.json>
"""
import json, sys
import numpy as np
import pandas as pd

B = pd.read_pickle(sys.argv[1])
rng = np.random.default_rng(20261029)
out = {}


def X_de(sub, cand='R'):
    adv = 'R' if cand == 'L' else 'L'
    return pd.DataFrame({'Cury': sub.Cury, 'Renan': sub.Renan, 'Caiado': sub.Caiado, 'Zema': sub.Zema,
                         'demais': sub.O1 - sub.Cury - sub.Renan - sub.Caiado - sub.Zema,
                         'qbn': (sub.B1 + sub.N1) - (sub.B2 + sub.N2), 'dcomp': sub.comp2 - sub.comp1,
                         'adv': sub[adv + '1'], 'prop': sub[cand + '1']}, index=sub.index).astype(float)


def ols_fe(X, y, g):
    keep = g.map(g.value_counts()) >= 2
    X, y, g = X[keep], y[keep], g[keep]
    Xm = (X - X.groupby(g).transform('mean')).values
    ym = (y - y.groupby(g).transform('mean')).values
    ok = np.abs(Xm).sum(0) > 1e-9
    Xm = Xm[:, ok]; names = list(np.array(X.columns)[ok])
    XtX = Xm.T @ Xm
    beta = np.linalg.solve(XtX, Xm.T @ ym)
    e = ym - Xm @ beta
    sc = pd.DataFrame(Xm * e[:, None]).groupby(g.values).sum().values
    inv = np.linalg.inv(XtX)
    N, k = Xm.shape; G = sc.shape[0]
    V = G / (G - 1) * (N - 1) / (N - k) * inv @ (sc.T @ sc) @ inv
    return dict(zip(names, beta)), dict(zip(names, np.sqrt(np.diag(V))))


def ver(P1, P5, e5):
    inc = P5 <= -0.03 and P5 / e5 < -3 and abs(P1) - abs(P5) <= 0.01
    return 'INCOERÊNCIA' if inc else ('COERENTE' if abs(P5) <= 0.5 * abs(P1) else 'INCONCLUSIVO')


cPL = np.quantile(B.fPL, [.2, .4, .6, .8]); q = np.searchsorted(cPL, B.fPL.values, side='left')
X0 = X_de(B)


def separados(y):
    Q = []
    for j in range(5):
        m = q == j
        b, e = ols_fe(X0[m], y[m], B.loc2[m]); Q.append((b['prop'], e['prop']))
    return Q


def empilhado(y):
    cols = {f'{c}_{j}': X0[c] * (q == j) for c in X0.columns for j in range(5)}
    b, e = ols_fe(pd.DataFrame(cols, index=B.index), y, B.loc2)
    return [(b[f'prop_{j}'], e[f'prop_{j}']) for j in range(5)]


R1 = B.R1.values.astype(np.int64)
Pp = np.minimum(R1, B.pl.values.astype(np.int64))       # eleitores de Flávio que votaram no PL (no máximo R1)
agg = B.groupby('loc2')[['L1', 'R1', 'O1']].sum(); fLloc = (agg.L1 / (agg.L1 + agg.R1 + agg.O1)).reindex(B.loc2).values


def resto():
    g = rng.binomial(B.O1.values.astype(np.int64), 0.45) + rng.binomial(np.maximum(B.L1.values, 0).astype(np.int64), 0.0)
    qbn = ((B.B1 + B.N1) - (B.B2 + B.N2)).values; dc = (B.comp2 - B.comp1).values
    return g + 0.4 * qbn + 0.45 * dc + rng.normal(0, 3, len(B))


DGP = {
    'DGP1_PL_nunca_troca_demais_8pct': lambda: -rng.binomial(R1 - Pp, 0.08) + resto(),
    'DGP2_plano_4pct': lambda: -rng.binomial(R1, 0.04) + resto(),
    'DGP3_contexto_12pct_x_fatia_Lula_no_local': lambda: -rng.binomial(R1, np.clip(0.12 * fLloc, 0, 1)) + resto(),
}
for nome, f in DGP.items():
    y = pd.Series(f().astype(float), index=B.index)
    s = separados(y); e = empilhado(y)
    out[nome] = {'separados': s, 'empilhado_FE_comum': e,
                 'veredito_separados': ver(s[0][0], s[4][0], s[4][1]), 'veredito_empilhado': ver(e[0][0], e[4][0], e[4][1])}
    print(f"{nome}\n  separados (registrado): {out[nome]['veredito_separados']} " + ' | '.join(f'{p:+.4f}' for p, _ in s) +
          f"\n  empilhado FE comum:     {out[nome]['veredito_empilhado']} " + ' | '.join(f'{p:+.4f}' for p, _ in e), flush=True)

# dados reais: votos do PL para deputado como regressor extra, dentro do local
y = (B.R2 - B.R1).astype(float)
X = X0.copy(); X['pl_dep'] = B.pl.astype(float)
b, e = ols_fe(X, y, B.loc2)
out['real_com_votos_PL'] = {'prop': [b['prop'], e['prop']], 'pl_dep': [b['pl_dep'], e['pl_dep']]}
print(f"real, dentro do local, com votos do PL para deputado: prop {b['prop']:+.4f} ({e['prop']:.4f}); pl_dep {b['pl_dep']:+.4f} ({e['pl_dep']:.4f})", flush=True)
for lo, hi in ((0, .35), (.35, .50), (.50, .65), (.65, 1.01)):
    m = ((B.fL1 >= lo) & (B.fL1 < hi)).values
    b, e = ols_fe(X[m], y[m], B.loc2[m])
    out[f'real_com_votos_PL_faixa_Lula_{lo}-{hi}'] = {'prop': [b['prop'], e['prop']], 'pl_dep': [b['pl_dep'], e['pl_dep']]}
    print(f"  faixa Lula {lo}-{hi}: prop {b['prop']:+.4f} ({e['prop']:.4f}); pl_dep {b['pl_dep']:+.4f} ({e['pl_dep']:.4f})", flush=True)
# o mesmo no sintético DGP1 (onde se sabe que pl_dep protege 0,08)
y1 = pd.Series(DGP['DGP1_PL_nunca_troca_demais_8pct']().astype(float), index=B.index)
b, e = ols_fe(X, y1, B.loc2)
print(f"DGP1 sintético, mesmo modelo: prop {b['prop']:+.4f}; pl_dep {b['pl_dep']:+.4f} (verdade: -0,08 e +0,08)", flush=True)
out['DGP1_com_votos_PL'] = {'prop': b['prop'], 'pl_dep': b['pl_dep']}
# variância da fatia do PL dentro do local contra a variância binomial esperada
grp = B.groupby('loc2')
dev = B.fPL - grp.fPL.transform('mean'); nloc = grp.fPL.transform('size')
m = nloc >= 2
var_obs = float((dev[m] ** 2 * nloc[m] / (nloc[m] - 1)).mean())
pl_loc = grp.pl.transform('sum') / grp.validos.transform('sum')
var_bin = float((pl_loc[m] * (1 - pl_loc[m]) / B.validos[m]).mean())
print(f'variância da fatia do PL dentro do local: observada {var_obs:.5f}, binomial esperada {var_bin:.5f}, razão {var_bin/var_obs:.2f}', flush=True)
out['variancia_dentro_do_local'] = {'observada': var_obs, 'binomial': var_bin}
with open(sys.argv[2], 'w') as f:
    json.dump(out, f, ensure_ascii=False, indent=1, default=float)
