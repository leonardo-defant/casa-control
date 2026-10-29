"""Conferência do L3, leituras alternativas (fora do critério; só para ver se alguma leitura razoável muda o veredito).
Usa a matriz B gravada por conferir.py e as funções de lá (código meu).
Uso: python3 -I conferir2.py <conferir_B.pkl> <saida.json>
"""
import json, sys
import numpy as np
import pandas as pd

B = pd.read_pickle(sys.argv[1])
out = {}


def fe_reg(sub, cand, loc='loc2', y=None, inter=None):
    adv = 'R' if cand == 'L' else 'L'
    X = pd.DataFrame({'Cury': sub.Cury, 'Renan': sub.Renan, 'Caiado': sub.Caiado, 'Zema': sub.Zema,
                      'demais': sub.O1 - sub.Cury - sub.Renan - sub.Caiado - sub.Zema,
                      'qbn': (sub.B1 + sub.N1) - (sub.B2 + sub.N2), 'dcomp': sub.comp2 - sub.comp1,
                      'adv': sub[adv + '1'], 'prop': sub[cand + '1']}, index=sub.index).astype(float)
    if inter is not None:   # todos os coeficientes por quintil, efeito fixo de local comum
        cols = {}
        for j in range(5):
            m = (inter == j).astype(float)
            for c in X.columns:
                cols[f'{c}_{j}'] = X[c] * m
        X = pd.DataFrame(cols, index=sub.index)
    yv = (sub[cand + '2'] - sub[cand + '1']).astype(float) if y is None else y.loc[sub.index].astype(float)
    g = sub[loc]
    keep = g.map(g.value_counts()) >= 2
    X, yv, g = X[keep], yv[keep], g[keep]
    Xm = (X - X.groupby(g).transform('mean')).values
    ym = (yv - yv.groupby(g).transform('mean')).values
    ok = np.abs(Xm).sum(0) > 0
    Xm = Xm[:, ok]; names = list(np.array(X.columns)[ok])
    XtX = Xm.T @ Xm
    beta = np.linalg.solve(XtX, Xm.T @ ym)
    e = ym - Xm @ beta
    sc = pd.DataFrame(Xm * e[:, None]).groupby(g.values).sum().values
    inv = np.linalg.inv(XtX)
    N, k = Xm.shape; G = sc.shape[0]
    V = G / (G - 1) * (N - 1) / (N - k) * inv @ (sc.T @ sc) @ inv
    if inter is not None:
        return [{'P': float(beta[names.index(f'prop_{j}')]), 'ep': float(np.sqrt(V[names.index(f'prop_{j}')] [names.index(f'prop_{j}')]))}
                for j in range(5)]
    j = names.index('prop')
    return {'P': float(beta[j]), 'ep': float(np.sqrt(V[j, j])), 'n': int(N), 'G': int(G)}


def veredito(P1, P5, ep5):
    inc = P5 <= -0.03 and P5 / ep5 < -3 and abs(P1) - abs(P5) <= 0.01
    coe = abs(P5) <= 0.5 * abs(P1)
    return 'INCOERÊNCIA' if inc else ('COERENTE' if coe else 'INCONCLUSIVO')


def cortes_de(f, w=None):
    if w is None:
        return np.quantile(f, [.2, .4, .6, .8])
    o = np.argsort(f.values, kind='stable'); cw = np.cumsum(w.values[o]) / w.values.sum()
    return np.array([f.values[o][np.searchsorted(cw, p)] for p in (.2, .4, .6, .8)])


def quintis(nome, cand, f, sub=None, cortes=None, w=None, loc='loc2', y=None, por_uf=False):
    sub = B if sub is None else sub
    f = f.loc[sub.index]
    if por_uf:
        q = pd.Series(0, index=sub.index)
        for uf, idx in sub.groupby('uf').groups.items():
            c = np.quantile(f.loc[idx], [.2, .4, .6, .8]); q.loc[idx] = np.searchsorted(c, f.loc[idx].values, side='left')
        q = q.values
    else:
        c = cortes_de(f, None if w is None else w.loc[sub.index]) if cortes is None else cortes
        q = np.searchsorted(c, f.values, side='left')
    Q = []
    for j in range(5):
        m = q == j
        if m.sum() < 50:
            Q.append({'P': None, 'ep': None, 'secoes': int(m.sum())}); continue
        r = fe_reg(sub[m], cand, loc, y); r['secoes'] = int(m.sum()); Q.append(r)
    v = veredito(Q[0]['P'], Q[4]['P'], Q[4]['ep']) if Q[0]['P'] is not None and Q[4]['P'] is not None else 'n/d'
    rz = abs(Q[4]['P']) / abs(Q[0]['P']) if v != 'n/d' else None
    print(f"{nome}: {v} |P5|/|P1|={rz if rz is None else round(rz,3)}  " +
          ' | '.join(f"Q{i+1} {x['P']:+.4f} ({x['ep']:.4f})" if x['P'] is not None else f'Q{i+1} n/d' for i, x in enumerate(Q)), flush=True)
    out[nome] = {'Q': Q, 'veredito': v, 'razao': rz}
    return q


fPL, fPT = B.fPL, B.fPT
q0 = quintis('A0 principal (reproducao)', 'R', fPL)
quintis('A1 cortes pesados pelo comparecimento de deputado', 'R', fPL, w=B.comp_max)
quintis('A2 fatia do PL sobre o comparecimento (inclui branco e nulo)', 'R', B.pl / B.comp_max)
quintis('A3 efeito fixo pelo local do 1o turno', 'R', fPL, loc='loc1')
quintis('A4 quintis dentro de cada UF', 'R', fPL, por_uf=True)
mesma = B.urna1 == B.urna2
quintis('A5 so secoes com a mesma urna nos dois turnos', 'R', fPL, sub=B[mesma], cortes=np.quantile(fPL, [.2, .4, .6, .8]))
# A6: efeito fixo de local comum, todos os coeficientes por quintil
r = fe_reg(B, 'R', inter=pd.Series(q0, index=B.index))
v = veredito(r[0]['P'], r[4]['P'], r[4]['ep'])
print('A6 empilhado com efeito fixo de local comum (todos os coef. por quintil):', v, round(abs(r[4]['P'])/abs(r[0]['P']), 3),
      ' | '.join(f"Q{i+1} {x['P']:+.4f} ({x['ep']:.4f})" for i, x in enumerate(r)), flush=True)
out['A6 empilhado FE comum'] = {'Q': r, 'veredito': v}
# A7: só voto de legenda do PL (o eleitor que digitou só o 22): medida mais pura de partidarismo
quintis('A7 fatia da legenda do PL nos validos (fora do registro)', 'R', B.pl_leg / B.validos)
# A8: espelho com PT
quintis('A8 Lula x PT (espelho)', 'L', fPT)

# faixas pela força do adversário na seção (o que o outro agente relatou como ponto em aberto)
fx = {}
for cand, fa in (('R', B.fL1), ('L', B.fR1)):
    for lo, hi in ((0, .35), (.35, .50), (.50, .65), (.65, 1.01)):
        m = (fa >= lo) & (fa < hi)
        rr = fe_reg(B[m], cand); fx[f'{cand}_{lo}-{hi}'] = rr
        print(f'faixa adversario {cand} {lo}-{hi}: {rr["P"]:+.4f} ({rr["ep"]:.4f}) n={rr["n"]}', flush=True)
out['faixas_adversario'] = fx
# PL dentro das faixas de Lula
cPL = np.quantile(fPL, [.2, .4, .6, .8])
for lo, hi in ((0, .35), (.35, .50), (.50, .65), (.65, 1.01)):
    m = (B.fL1 >= lo) & (B.fL1 < hi)
    quintis(f'B faixa Lula {lo}-{hi}, quintis nacionais do PL', 'R', fPL, sub=B[m], cortes=cPL)
# calibração: desvio uniforme de 3,56% e concentrado
R2, L2 = B.R2.astype(float), B.L2.astype(float)
marg = L2.sum() - R2.sum(); s = (marg / 2) / (R2.sum() + marg / 2)
print('s que vira', s, 'margem', marg, flush=True)
yR = (R2 * (1 - s)) - B.R1
quintis(f'C1 desvio uniforme {100*s:.2f}%', 'R', fPL, y=yR)
mL = (B.L1 / (B.L1 + B.R1).clip(lower=1)).fillna(0)
wv = mL * R2; desv = wv * (s * R2.sum() / wv.sum())
quintis('C2 desvio concentrado onde Lula e forte, mesmo total', 'R', fPL, y=(R2 - desv) - B.R1)
quintis('C3 desvio uniforme 1%', 'R', fPL, y=(R2 * 0.99) - B.R1)
with open(sys.argv[2], 'w') as f:
    json.dump(out, f, ensure_ascii=False, indent=1)
