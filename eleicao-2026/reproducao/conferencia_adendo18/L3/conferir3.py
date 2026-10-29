"""Por que o empilhado com efeito fixo de local comum (A6) dá perfil plano e as regressões separadas por quintil dão degrau?
Variantes: locais puros x mistos, quintis pela fatia do local, empilhado com intercepto por quintil, empilhado só com o
próprio interagido.
Uso: python3 -I conferir3.py <conferir_B.pkl> <saida.json>
"""
import json, sys
import numpy as np
import pandas as pd

B = pd.read_pickle(sys.argv[1])
out = {}
BASE = ['Cury', 'Renan', 'Caiado', 'Zema', 'demais', 'qbn', 'dcomp', 'adv', 'prop']


def X_de(sub, cand):
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
    return dict(zip(names, beta)), dict(zip(names, np.sqrt(np.diag(V)))), N, G


def ver(P1, P5, e5):
    inc = P5 <= -0.03 and P5 / e5 < -3 and abs(P1) - abs(P5) <= 0.01
    return 'INCOERÊNCIA' if inc else ('COERENTE' if abs(P5) <= 0.5 * abs(P1) else 'INCONCLUSIVO')


def separados(nome, sub, q, cand='R', g='loc2'):
    y = (sub[cand + '2'] - sub[cand + '1']).astype(float); X = X_de(sub, cand)
    Q = []
    for j in range(5):
        m = q == j
        b, e, N, G = ols_fe(X[m], y[m], sub[g][m])
        Q.append({'P': b['prop'], 'ep': e['prop'], 'n': N, 'G': G})
    v = ver(Q[0]['P'], Q[4]['P'], Q[4]['ep'])
    print(f'{nome}: {v} ' + ' | '.join(f"Q{i+1} {x['P']:+.4f} ({x['ep']:.4f}) n={x['n']}" for i, x in enumerate(Q)), flush=True)
    out[nome] = {'Q': Q, 'veredito': v}


def empilhado(nome, sub, q, cand='R', intercepto=False, so_proprio=False):
    y = (sub[cand + '2'] - sub[cand + '1']).astype(float); X0 = X_de(sub, cand)
    cols = {}
    for c in X0.columns:
        if so_proprio and c != 'prop':
            cols[c] = X0[c]
            continue
        for j in range(5):
            cols[f'{c}_{j}'] = X0[c] * (q == j)
    if intercepto:
        for j in range(1, 5):
            cols[f'd_{j}'] = (q == j).astype(float)
    X = pd.DataFrame(cols, index=sub.index)
    b, e, N, G = ols_fe(X, y, sub.loc2)
    Q = [{'P': b[f'prop_{j}'], 'ep': e[f'prop_{j}']} for j in range(5)]
    v = ver(Q[0]['P'], Q[4]['P'], Q[4]['ep'])
    print(f'{nome}: {v} ' + ' | '.join(f"Q{i+1} {x['P']:+.4f} ({x['ep']:.4f})" for i, x in enumerate(Q)) + f' N={N} G={G}', flush=True)
    out[nome] = {'Q': Q, 'veredito': v}


cPL = np.quantile(B.fPL, [.2, .4, .6, .8])
q = pd.Series(np.searchsorted(cPL, B.fPL.values, side='left'), index=B.index)
B['q'] = q
nq = B.groupby('loc2').q.nunique(); B['puro'] = B.loc2.map(nq) == 1
print('secoes em locais puros', int(B.puro.sum()), 'mistos', int((~B.puro).sum()),
      'por quintil, fracao em local puro', B.groupby('q').puro.mean().round(3).tolist(), flush=True)
out['puros'] = {'secoes_puro': int(B.puro.sum()), 'fracao_puro_por_quintil': B.groupby('q').puro.mean().tolist()}

separados('S0 separados (reproducao)', B, q.values)
Bp = B[B.puro]; separados('S1 separados, so locais puros', Bp, Bp.q.values)
Bm = B[~B.puro]; separados('S2 separados, so locais mistos', Bm, Bm.q.values)
empilhado('E0 empilhado FE comum, tudo interagido', B, q.values)
empilhado('E1 empilhado FE comum + intercepto por quintil', B, q.values, intercepto=True)
empilhado('E2 empilhado FE comum, so o proprio interagido', B, q.values, so_proprio=True)
empilhado('E3 empilhado FE comum, so locais mistos', Bm, Bm.q.values)
# quintis pela fatia do PL no local (agregada), todas as seções do local no mesmo quintil
agg = B.groupby('loc2')[['pl', 'validos']].sum(); fl = agg.pl / agg.validos
B['fPL_loc'] = B.loc2.map(fl)
cl = np.quantile(B.fPL_loc, [.2, .4, .6, .8])
ql = np.searchsorted(cl, B.fPL_loc.values, side='left')
separados('L1 quintis pela fatia do PL no local (cortes por secao)', B, ql)
# quintis pela fatia do PL no município
aggm = B.assign(mun=B.index.str.rsplit('|', n=2).str[0]).groupby('mun')[['pl', 'validos']].sum()
B['mun'] = B.index.str.rsplit('|', n=2).str[0]
B['fPL_mun'] = B.mun.map(aggm.pl / aggm.validos)
cm = np.quantile(B.fPL_mun, [.2, .4, .6, .8])
separados('L2 quintis pela fatia do PL no municipio', B, np.searchsorted(cm, B.fPL_mun.values, side='left'))
# desvio da fatia da secao em relacao ao local: quintis do residuo (PL relativo dentro do local)
B['fPL_rel'] = B.fPL - B.fPL_loc
cr = np.quantile(B.fPL_rel, [.2, .4, .6, .8])
separados('L3 quintis da fatia do PL relativa ao local', B, np.searchsorted(cr, B.fPL_rel.values, side='left'))
with open(sys.argv[2], 'w') as f:
    json.dump(out, f, ensure_ascii=False, indent=1, default=float)
