"""Quanto do degrau do L3 cada mecanismo explica (dados sintéticos com X real).
DGP_PL: y = ajuste do modelo dentro do local com votos do PL para deputado (inclinação comum, efeito fixo de local) mais
        o resíduo embaralhado dentro do local: só o partidarismo (e o nível do local) varia entre seções.
DGP_ctx: perda de cada eleitor de Flávio = 0,23 x (fatia de Lula na seção)^2, calibrada nas faixas do T35/L3, sem partido.
DGP_ctx_desvio: DGP_ctx com um desvio uniforme de 3,56% por cima.
DGP_PL_desvio: DGP_PL com um desvio uniforme de 3,56% por cima, e o modelo com votos do PL nos dados com desvio.
Uso: python3 -I conferir5.py <conferir_B.pkl> <saida.json>
"""
import json, sys
import numpy as np
import pandas as pd

B = pd.read_pickle(sys.argv[1])
rng = np.random.default_rng(29102026)
out = {}


def X_de(sub):
    return pd.DataFrame({'Cury': sub.Cury, 'Renan': sub.Renan, 'Caiado': sub.Caiado, 'Zema': sub.Zema,
                         'demais': sub.O1 - sub.Cury - sub.Renan - sub.Caiado - sub.Zema,
                         'qbn': (sub.B1 + sub.N1) - (sub.B2 + sub.N2), 'dcomp': sub.comp2 - sub.comp1,
                         'adv': sub.L1, 'prop': sub.R1}, index=sub.index).astype(float)


def ols_fe(X, y, g, resid=False):
    keep = g.map(g.value_counts()) >= 2
    X, y, g = X[keep], y[keep], g[keep]
    Xg = X.groupby(g).transform('mean'); yg = y.groupby(g).transform('mean')
    Xm = (X - Xg).values; ym = (y - yg).values
    XtX = Xm.T @ Xm
    beta = np.linalg.solve(XtX, Xm.T @ ym)
    e = ym - Xm @ beta
    if resid:
        return beta, e, keep, (yg.values - Xg.values @ beta)
    sc = pd.DataFrame(Xm * e[:, None]).groupby(g.values).sum().values
    inv = np.linalg.inv(XtX)
    N, k = Xm.shape; G = sc.shape[0]
    V = G / (G - 1) * (N - 1) / (N - k) * inv @ (sc.T @ sc) @ inv
    return dict(zip(X.columns, beta)), dict(zip(X.columns, np.sqrt(np.diag(V))))


def ver(P1, P5, e5):
    inc = P5 <= -0.03 and P5 / e5 < -3 and abs(P1) - abs(P5) <= 0.01
    return 'INCOERÊNCIA' if inc else ('COERENTE' if abs(P5) <= 0.5 * abs(P1) else 'INCONCLUSIVO')


cPL = np.quantile(B.fPL, [.2, .4, .6, .8]); q = np.searchsorted(cPL, B.fPL.values, side='left')
X0 = X_de(B)


def separados(nome, y):
    Q = []
    for j in range(5):
        m = q == j
        b, e = ols_fe(X0[m], y[m], B.loc2[m]); Q.append((b['prop'], e['prop']))
    v = ver(Q[0][0], Q[4][0], Q[4][1])
    out[nome] = {'Q': Q, 'veredito': v, 'razao': abs(Q[4][0]) / abs(Q[0][0])}
    print(f'{nome}: {v} |P5|/|P1|={abs(Q[4][0]) / abs(Q[0][0]):.2f} ' + ' | '.join(f'{p:+.4f} ({s:.4f})' for p, s in Q), flush=True)


y = (B.R2 - B.R1).astype(float)
XP = X0.copy(); XP['pl_dep'] = B.pl.astype(float)
beta, e, keep, fe = ols_fe(XP, y, B.loc2, resid=True)
print('modelo com PL: ' + ', '.join(f'{c} {b:+.4f}' for c, b in zip(XP.columns, beta)), flush=True)
sub = B[keep]
g = sub.loc2.values
# embaralha o resíduo dentro do local
eb = pd.Series(e, index=sub.index)
perm = eb.groupby(g).transform(lambda s: rng.permutation(s.values))
ypl = pd.Series(np.nan, index=B.index)
ypl[keep] = XP[keep].values @ beta + fe + perm.values
# seções fora (locais de uma seção) ficam com y real; não entram nas regressões separadas se forem únicas no quintil
ypl[~keep] = y[~keep]
separados('real (reprodução)', y)
separados('DGP_PL (só partidarismo dentro do local + nível do local)', ypl)
# sem o termo do PL (mesmo ajuste, pl_dep zerado): o que sobra é o nível do local
ip = list(XP.columns).index('pl_dep'); b0 = beta.copy(); b0[ip] = 0
ypl0 = ypl.copy(); ypl0[keep] = XP[keep].values @ b0 + fe + perm.values
separados('DGP_PL sem o termo do PL (só nível do local)', ypl0)
# contexto calibrado
fl = B.fL1.fillna(0).values
loss = np.clip(0.23 * fl ** 2, 0, 1)
R1 = B.R1.values.astype(np.int64)


def resto():
    gO = rng.binomial(B.O1.values.astype(np.int64), 0.45)
    return gO + 0.4 * ((B.B1 + B.N1) - (B.B2 + B.N2)).values + 0.45 * (B.comp2 - B.comp1).values + rng.normal(0, 3, len(B))


yc = pd.Series(-rng.binomial(R1, loss) + resto(), index=B.index).astype(float)
separados('DGP_ctx (perda 0,23 x fatia de Lula^2, sem partido)', yc)
s = 0.03557927305546972
R2c = R1 + yc   # 2º turno sintético de Flávio
separados('DGP_ctx + desvio uniforme 3,56%', yc - s * R2c)
R2p = B.R1 + ypl
separados('DGP_PL + desvio uniforme 3,56%', ypl - s * R2p)
# modelo com PL nos dados reais com desvio uniforme (o termo do PL some?)
yd = (B.R2 * (1 - s) - B.R1).astype(float)
b, se = ols_fe(XP, yd, B.loc2)
print(f"real + desvio uniforme 3,56%, modelo com PL: prop {b['prop']:+.4f}; pl_dep {b['pl_dep']:+.4f} ({se['pl_dep']:.4f})", flush=True)
out['real_desvio_modelo_PL'] = {'prop': b['prop'], 'pl_dep': [b['pl_dep'], se['pl_dep']]}
with open(sys.argv[2], 'w') as f:
    json.dump(out, f, ensure_ascii=False, indent=1, default=float)
