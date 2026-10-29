"""Checagens extras (post hoc, fora do registro) da conferência do L7:
A. virada de Lula contra r = biometria sem habilitação / comparecimento, contínuo e em faixas, com controles, dentro do local;
B. na amostra de logs, a parte não biométrica verdadeira contra a virada, dentro do local;
C. o exterior (sem biometria) contra seções do Brasil com composição parecida no 1º turno."""
import collections, gzip, json, math, sys
import numpy as np

base = json.load(gzip.open(sys.argv[1], 'rt'))
bw = json.load(gzip.open(sys.argv[2], 'rt'))
lg = json.load(open(sys.argv[3]))
saida = sys.argv[4]
out = {}


def fe_multi(y, X, g, w, cl=None):
    y = np.asarray(y, float); X = np.asarray(X, float); w = np.asarray(w, float)
    if X.ndim == 1: X = X[:, None]
    _, gi = np.unique(g, return_inverse=True)
    cnt = np.bincount(gi); ok = cnt[gi] >= 2
    y, X, w, gi = y[ok], X[ok], w[ok], gi[ok]
    cl = gi if cl is None else np.unique(np.asarray(cl)[ok], return_inverse=True)[1]
    _, gi = np.unique(gi, return_inverse=True)
    G = gi.max() + 1
    sw = np.bincount(gi, weights=w, minlength=G)
    def dm(v):
        return v - (np.bincount(gi, weights=w * v, minlength=G) / sw)[gi]
    yd = dm(y); Xd = np.column_stack([dm(X[:, j]) for j in range(X.shape[1])])
    A = (Xd * w[:, None]).T @ Xd
    b = np.linalg.solve(A, (Xd * w[:, None]).T @ yd)
    e = yd - Xd @ b
    C = cl.max() + 1
    S = np.column_stack([np.bincount(cl, weights=w * Xd[:, j] * e, minlength=C) for j in range(X.shape[1])])
    inv = np.linalg.inv(A)
    N, k = len(y), X.shape[1]
    V = (C / (C - 1)) * ((N - 1) / (N - k)) * inv @ (S.T @ S) @ inv
    return b, np.sqrt(np.diag(V)), N, G


keys, Y, W, LOC, R, L1, O1, BN1, DC, Y1 = [], [], [], [], [], [], [], [], [], []
for k, s in base.items():
    if k.startswith('ZZ|') or '1' not in s or '2' not in s:
        continue
    a, b = s['1'], s['2']
    v = bw.get(k)
    if v is None or a['L'] + a['R'] <= 0 or b['L'] + b['R'] <= 0 or v['comp'] <= 0 or a['comp'] <= 0:
        continue
    uf, m, z, _ = k.split('|')
    keys.append(k)
    Y.append(100 * b['L'] / (b['L'] + b['R']) - 100 * a['L'] / (a['L'] + a['R']))
    W.append(b['L'] + b['R'])
    LOC.append(f"{uf}|{m}|{z}|{v['loc']}")
    R.append(v['biomsem'] / v['comp'])
    tot1 = a['L'] + a['R'] + a['O'] + a['B'] + a['N']
    L1.append(100 * a['L'] / (a['L'] + a['R'])); O1.append(100 * a['O'] / tot1); BN1.append(100 * (a['B'] + a['N']) / tot1)
    DC.append(100 * (b['comp'] / a['comp'] - 1))
Y, W, LOC, R, L1, O1, BN1, DC = map(np.array, (Y, W, LOC, R, L1, O1, BN1, DC))
W = W.astype(float)

# A. contínuo, com e sem controles; placebo
A = {}
b, se, N, G = fe_multi(Y, R, LOC, W); A['so_r'] = (b[0], se[0])
b, se, N, G = fe_multi(L1, R, LOC, W); A['placebo_L1_em_r'] = (b[0], se[0])
b, se, N, G = fe_multi(O1, R, LOC, W); A['placebo_O1_em_r'] = (b[0], se[0])
b, se, N, G = fe_multi(DC, R, LOC, W); A['placebo_dcomp_em_r'] = (b[0], se[0])
X = np.column_stack([R, L1, L1 ** 2 / 100, O1, BN1, DC])
b, se, N, G = fe_multi(Y, X, LOC, W); A['com_controles'] = {'r': (b[0], se[0]), 'L1': (b[1], se[1]), 'O1': (b[3], se[3]),
                                                              'BN1': (b[4], se[4]), 'DC': (b[5], se[5])}
# faixas de r (base: r < 0,05)
cortes = [0.05, 0.10, 0.15, 0.20, 0.30, 0.50]
fx = np.digitize(R, cortes)
D = np.column_stack([(fx == j).astype(float) for j in range(1, len(cortes) + 1)])
b, se, N, G = fe_multi(Y, D, LOC, W)
bc, sec, _, _ = fe_multi(Y, np.column_stack([D, L1, L1 ** 2 / 100, O1, BN1, DC]), LOC, W)
nomes = ['[0,05;0,10)', '[0,10;0,15)', '[0,15;0,20)', '[0,20;0,30)', '[0,30;0,50)', '>=0,50']
A['faixas'] = {n: {'secoes': int((fx == j + 1).sum()), 'coef': b[j], 'ep': se[j], 'coef_ctrl': bc[j], 'ep_ctrl': sec[j]}
               for j, n in enumerate(nomes)}
A['faixa_base_secoes'] = int((fx == 0).sum())
A['r_media'] = float(np.average(R, weights=W))
out['A'] = A

# B. amostra de logs: parte não biométrica verdadeira
Bk = {}
for k, d in lg.items():
    c = d['c']
    if c.get('hab'):
        bio = sum(v for t, v in d['tipos'].items() if 'biom' in t)
        Bk[k] = 1 - bio / c['hab']
ix = {k: i for i, k in enumerate(keys)}
sel = [ix[k] for k in Bk if k in ix]
nb = np.array([Bk[keys[i]] for i in sel])
yb, wb, lb, rb = Y[sel], W[sel], LOC[sel], R[sel]
cntl = collections.Counter(lb)
B = {'urnas': len(sel), 'locais_com_2_ou_mais': sum(1 for v in cntl.values() if v >= 2),
     'urnas_em_locais_com_2_ou_mais': sum(v for v in cntl.values() if v >= 2)}
try:
    b, se, N, G = fe_multi(yb, nb, lb, wb); B['virada_em_nao_bio_log'] = (b[0], se[0], N, G)
    b, se, N, G = fe_multi(yb, rb, lb, wb); B['virada_em_r_mesma_amostra'] = (b[0], se[0])
    b, se, N, G = fe_multi(nb, rb, lb, wb); B['nao_bio_em_r'] = (b[0], se[0])
    b, se, N, G = fe_multi(L1[sel], nb, lb, wb); B['placebo_L1_em_nao_bio'] = (b[0], se[0])
    Xs = np.column_stack([nb, L1[sel], L1[sel] ** 2 / 100, O1[sel], BN1[sel], DC[sel]])
    b, se, N, G = fe_multi(yb, Xs, lb, wb); B['virada_em_nao_bio_com_controles'] = (b[0], se[0])
except Exception as e:
    B['erro'] = str(e)
# sem efeito fixo de local: por município (amostra por conglomerados)
mun = np.array(['|'.join(keys[i].split('|')[:2]) for i in sel])
try:
    b, se, N, G = fe_multi(yb, nb, mun, wb); B['virada_em_nao_bio_fe_municipio'] = (b[0], se[0], N, G)
except Exception as e:
    B['erro_mun'] = str(e)
out['B'] = B

# C. exterior
kz = [k for k, s in base.items() if k.startswith('ZZ|') and '1' in s and '2' in s]
def tot(ks, t, c):
    return sum(base[k][t][c] for k in ks)
zL1, zR1, zO1, zB1, zN1 = (tot(kz, '1', c) for c in 'LRONB')[0:5] if False else (tot(kz, '1', 'L'), tot(kz, '1', 'R'), tot(kz, '1', 'O'), tot(kz, '1', 'B'), tot(kz, '1', 'N'))
zL2, zR2 = tot(kz, '2', 'L'), tot(kz, '2', 'R')
zc1, zc2 = tot(kz, '1', 'comp'), tot(kz, '2', 'comp')
ext = {'L1': zL1, 'R1': zR1, 'O1': zO1, 'BN1': zB1 + zN1, 'L2': zL2, 'R2': zR2, 'comp1': zc1, 'comp2': zc2,
       'fatiaL1': 100 * zL1 / (zL1 + zR1), 'fatiaL2': 100 * zL2 / (zL2 + zR2)}
ext['virada'] = ext['fatiaL2'] - ext['fatiaL1']
ext['O1_pct'] = 100 * zO1 / (zL1 + zR1 + zO1 + zB1 + zN1)
ext['BN1_pct'] = 100 * (zB1 + zN1) / (zL1 + zR1 + zO1 + zB1 + zN1)
ext['dcomp'] = 100 * (zc2 / zc1 - 1)
ext['R2_sobre_R1'] = zR2 / zR1; ext['L2_sobre_L1'] = zL2 / zL1
bL1, bR1 = sum(base[k]['1']['L'] for k in keys), sum(base[k]['1']['R'] for k in keys)
bL2, bR2 = sum(base[k]['2']['L'] for k in keys), sum(base[k]['2']['R'] for k in keys)
ext['brasil_R2_sobre_R1'] = bR2 / bR1; ext['brasil_L2_sobre_L1'] = bL2 / bL1
# previsão do Brasil (MQP sem efeito fixo, seções do Brasil) para a composição do exterior
Xb = np.column_stack([np.ones_like(L1), L1, L1 ** 2 / 100, O1, BN1, DC])
sw = np.sqrt(W)
coef, *_ = np.linalg.lstsq(Xb * sw[:, None], Y * sw, rcond=None)
xz = np.array([1, ext['fatiaL1'], ext['fatiaL1'] ** 2 / 100, ext['O1_pct'], ext['BN1_pct'], ext['dcomp']])
ext['previsto_pelo_brasil'] = float(xz @ coef)
# o mesmo sem a variação do comparecimento
coef2, *_ = np.linalg.lstsq(Xb[:, :5] * sw[:, None], Y * sw, rcond=None)
ext['previsto_sem_dcomp'] = float(xz[:5] @ coef2)
# previsão seção a seção do exterior (média ponderada), com a composição de cada seção do exterior
pz = []
for k in kz:
    a, b = base[k]['1'], base[k]['2']
    if a['L'] + a['R'] <= 0 or b['L'] + b['R'] <= 0 or a['comp'] <= 0:
        continue
    t1 = a['L'] + a['R'] + a['O'] + a['B'] + a['N']
    l1 = 100 * a['L'] / (a['L'] + a['R'])
    x = np.array([1, l1, l1 ** 2 / 100, 100 * a['O'] / t1, 100 * (a['B'] + a['N']) / t1, 100 * (b['comp'] / a['comp'] - 1)])
    y = 100 * b['L'] / (b['L'] + b['R']) - l1
    pz.append((k, y, float(x @ coef), b['L'] + b['R']))
yz = np.array([p[1] for p in pz]); pp = np.array([p[2] for p in pz]); wz = np.array([p[3] for p in pz], float)
res = yz - pp
cid = np.array(['|'.join(p[0].split('|')[:2]) for p in pz])
# erro agrupado por cidade do exterior
m = np.average(res, weights=wz)
cl = np.unique(cid, return_inverse=True)[1]
sc = np.bincount(cl, weights=wz * (res - m))
C = cl.max() + 1
se_m = math.sqrt(C / (C - 1) * np.sum(sc ** 2)) / wz.sum()
ext['secao_a_secao'] = {'secoes': len(pz), 'cidades': int(C), 'virada_media': float(np.average(yz, weights=wz)),
                        'prevista_media': float(np.average(pp, weights=wz)), 'diferenca': float(m), 'ep_cidade': se_m}
# o mesmo resíduo no Brasil por UF (para ver a faixa normal de uma "região" inteira)
resb = Y - Xb @ coef
uf = np.array([k.split('|')[0] for k in keys])
ext['residuo_medio_por_uf'] = dict(sorted({u: float(np.average(resb[uf == u], weights=W[uf == u])) for u in set(uf)}.items(), key=lambda x: x[1]))
out['C'] = ext
json.dump(out, open(saida, 'w'), ensure_ascii=False, indent=1, default=float)
print(json.dumps(out, ensure_ascii=False, indent=1, default=float))
