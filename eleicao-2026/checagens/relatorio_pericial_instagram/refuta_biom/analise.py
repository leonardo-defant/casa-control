"""Conferência independente das afirmações sobre biometria (NH = QT_ELEI_BIOM_SEM_HABILITACAO).
Lê: extratos próprios do bweb (t1/*.tsv, t2/*.tsv), base por seção 2026 (só para conferir),
bases 2022 e 2018 (placebo). Cada base é lida uma vez."""
import glob, gzip, json, sys, os
import numpy as np

D = os.path.dirname(os.path.abspath(__file__))
S = '/tmp/claude-0/-home-user-casa-control/ce2a8c88-e5ad-504f-8950-6f5ee14ae721/scratchpad'
out = {}


def say(*a):
    print(*a, flush=True)


def ler_tsv(t):
    d = {}
    for f in sorted(glob.glob(f'{D}/{t}/*.tsv')):
        with open(f) as fh:
            h = fh.readline().rstrip('\n').split('\t')
            for line in fh:
                r = dict(zip(h, line.rstrip('\n').split('\t')))
                k = f"{r['uf']}|{r['mun']}|{r['zona']}|{r['secao']}"
                assert k not in d, k
                d[k] = {x: int(r[x]) for x in ('loc', 'apt', 'comp', 'NH', 'L', 'R', 'O', 'B', 'N', 'diff')}
                d[k]['urna'] = r['urna']
    return d


T1 = ler_tsv('t1'); T2 = ler_tsv('t2')
say('secoes T1', len(T1), 'T2', len(T2))
say('diff!=0 T1', sum(1 for v in T1.values() if v['diff']), 'T2', sum(1 for v in T2.values() if v['diff']))
say('urnas T1', {u: sum(1 for v in T1.values() if v['urna'] == u) for u in set(v['urna'] for v in T1.values())})

# conferência com a base por seção
base = json.load(gzip.open(f'{S}/trab2t/secoes2026.json.gz', 'rt'))
dif = {'1': 0, '2': 0}; falta = {'1': 0, '2': 0}
for k, v in base.items():
    for t, TT in (('1', T1), ('2', T2)):
        if t not in v: continue
        if k not in TT: falta[t] += 1; continue
        a, b = v[t], TT[k]
        if any(a[x] != b[x] for x in ('comp', 'L', 'R', 'B', 'N', 'apt')) or (t == '1' and a['O'] != b['O']):
            dif[t] += 1
say('base: secoes', len(base), 'diferentes', dif, 'faltando no bweb', falta,
    'bweb fora da base', sum(1 for k in T1 if k not in base), sum(1 for k in T2 if k not in base))
out['conferencia_base'] = {'dif': dif, 'falta': falta}
del base


def tot(TT, filtro=lambda k: True):
    s = {x: 0 for x in ('comp', 'NH', 'L', 'R', 'O', 'B', 'N', 'apt')}
    n = 0
    for k, v in TT.items():
        if filtro(k):
            n += 1
            for x in s: s[x] += v[x]
    s['secoes'] = n
    return s


br = lambda k: not k.startswith('ZZ')
for t, TT in (('1', T1), ('2', T2)):
    a = tot(TT); b = tot(TT, br)
    V = a['L'] + a['R'] + a['O']
    r = {'total': a, 'brasil': b, 'pctNH_total': 100 * a['NH'] / a['comp'], 'pctNH_brasil': 100 * b['NH'] / b['comp'],
         'L_menos_R': a['L'] - a['R'], 'pctL_validos': 100 * a['L'] / V, 'pctR_validos': 100 * a['R'] / V,
         'razao_NH_margem': a['NH'] / abs(a['L'] - a['R']), 'NH_exterior': a['NH'] - b['NH']}
    out['tot' + t] = r
    say('T' + t, json.dumps(r))
a1, a2 = out['tot1']['total'], out['tot2']['total']
virada = (a2['L'] - a2['R']) - (a1['L'] - a1['R'])
say('var NH', a2['NH'] - a1['NH'], 'cresc NH %', 100 * (a2['NH'] / a1['NH'] - 1), 'cresc comp %', 100 * (a2['comp'] / a1['comp'] - 1),
    'virada', virada, 'varNH/virada', (a2['NH'] - a1['NH']) / virada)

# limiar de inversão: retirar todos os NH
V2 = a2['L'] + a2['R']
validos_NH = a2['NH'] * V2 / a2['comp']
lim = (validos_NH + (a2['L'] - a2['R'])) / 2 / validos_NH
lim_todos_validos = (a2['NH'] + (a2['L'] - a2['R'])) / 2 / a2['NH']
say('limiar de fatia de Lula entre os NH para inverter: %.4f (válidos NH na taxa nacional) / %.4f (todos os NH válidos)' % (lim, lim_todos_validos))
out['limiar'] = [lim, lim_todos_validos]

# UFs: vencedor e taxa
ufs = sorted(set(k.split('|')[0] for k in T2))
uft = {}
for t, TT in (('1', T1), ('2', T2)):
    for uf in ufs:
        s = tot(TT, lambda k, uf=uf: k.startswith(uf + '|'))
        uft.setdefault(uf, {})[t] = {'pctNH': round(100 * s['NH'] / s['comp'], 3), 'Lmenos R': s['L'] - s['R'],
                                     'venc': 'L' if s['L'] > s['R'] else 'R'}
for t in '12':
    rk = sorted([u for u in ufs if u != 'ZZ'], key=lambda u: -uft[u][t]['pctNH'])
    say('ranking T' + t, [(u, uft[u][t]['pctNH'], uft[u][t]['venc']) for u in rk[:8]])
    say('  Flávio à frente T' + t, sorted(u for u in ufs if u != 'ZZ' and uft[u][t]['venc'] == 'R'))
out['uf'] = uft

# municípios
for t, TT in (('1', T1), ('2', T2)):
    m = {}
    for k, v in TT.items():
        if not br(k): continue
        mk = '|'.join(k.split('|')[:2])
        e = m.setdefault(mk, [0, 0, 0, 0, 0])
        e[0] += v['L']; e[1] += v['R']; e[2] += v['apt']; e[3] += v['NH']; e[4] += v['comp']
    nf = sum(1 for e in m.values() if e[1] > e[0]); nl = sum(1 for e in m.values() if e[0] > e[1])
    say('T' + t, 'municipios', len(m), 'Flavio a frente', nf, 'Lula a frente', nl, 'empate', len(m) - nf - nl)
    # porte por aptos do município (do próprio turno)
    faixas = [(0, 10000), (10000, 10**10)]
    for lo, hi in faixas:
        es = [e for e in m.values() if lo <= e[2] < hi]
        say('   porte', lo, hi, 'munic', len(es), 'pctNH %.3f' % (100 * sum(e[3] for e in es) / sum(e[4] for e in es)))
    out['mun' + t] = {'n': len(m), 'F': nf, 'L': nl}

# matriz por seção no Brasil com os dois turnos e comparecimento > 0
ks = [k for k in T2 if br(k) and k in T1 and T1[k]['comp'] > 0 and T2[k]['comp'] > 0]
say('secoes Brasil com os dois turnos', len(ks))


def arr(TT, f):
    return np.array([f(TT[k]) for k in ks], float)


C1 = arr(T1, lambda v: v['comp']); C2 = arr(T2, lambda v: v['comp'])
NH1 = arr(T1, lambda v: v['NH']); NH2 = arr(T2, lambda v: v['NH'])
L1 = arr(T1, lambda v: v['L']); R1 = arr(T1, lambda v: v['R']); O1 = arr(T1, lambda v: v['O'])
L2 = arr(T2, lambda v: v['L']); R2 = arr(T2, lambda v: v['R'])
x1 = NH1 / C1; x2 = NH2 / C2
loc = np.array(['|'.join(k.split('|')[:3]) + '|' + str(T2[k]['loc']) for k in ks])
_, g = np.unique(loc, return_inverse=True)
cnt = np.bincount(g); multi = cnt[g] >= 2
say('locais', g.max() + 1, 'secoes em locais com 2+', int(multi.sum()))


def corr(a, b, m=None):
    if m is None: m = np.isfinite(a) & np.isfinite(b)
    return float(np.corrcoef(a[m], b[m])[0, 1])


def dem(a, m):
    gg = g[m]; aa = a[m]
    mu = np.bincount(gg, weights=aa, minlength=g.max() + 1) / np.maximum(np.bincount(gg, minlength=g.max() + 1), 1)
    return aa - mu[gg]


def corr_fe(a, b):
    m = multi & np.isfinite(a) & np.isfinite(b)
    # grupos precisam ter 2+ entre os válidos
    c = np.bincount(g[m], minlength=g.max() + 1)
    m = m & (c[g] >= 2)
    return float(np.corrcoef(dem(a, m), dem(b, m))[0, 1]), int(m.sum())


say('corr taxa T1 x T2 entre seções %.4f' % corr(x1, x2))
out['corr_x1_x2'] = corr(x1, x2)
with np.errstate(invalid='ignore', divide='ignore'):
    y1 = L1 / (L1 + R1); y2 = L2 / (L2 + R2)
for nome, x, y in (('T1', x1, y1), ('T2', x2, y2)):
    say(nome, 'corr nivel taxa x L/(L+R): entre %.4f, dentro do local %.4f (n %d)' % ((corr(x, y),) + corr_fe(x, y)))
dx = x2 - x1; dy = y2 - y1
say('variacao: corr(dx,dy) entre %.4f dentro %.4f (n %d)' % ((corr(dx, dy),) + corr_fe(dx, dy)))
for lo, hi in ((-1, -.05), (-.05, -.02), (-.02, .02), (.02, .05), (.05, 1.01)):
    m = (dx >= lo) & (dx < hi) & np.isfinite(dy)
    agg = 100 * (L2[m].sum() / (L2[m] + R2[m]).sum() - L1[m].sum() / (L1[m] + R1[m]).sum())
    say('  faixa dx [%.2f,%.2f) secoes %d media dy %.3f pp agregado %.3f pp' % (lo, hi, m.sum(), 100 * np.nanmean(dy[m]), agg))

# faixas de taxa, 2T e 1T
for nome, x, L, R, NH in (('T2', x2, L2, R2, NH2), ('T1', x1, L1, R1, NH1)):
    say('faixas', nome)
    for lo, hi in ((0, .05), (.05, .10), (.10, .15), (.15, .20), (.20, .30), (.30, .50), (.50, 1.01)):
        m = (x >= lo) & (x < hi)
        say('  [%.2f,%.2f) secoes %6d comp %9d NH %8d (%.2f%% do NH) L/(L+R) %.2f%%' % (
            lo, hi, m.sum(), (C2 if nome == 'T2' else C1)[m].sum(), NH[m].sum(), 100 * NH[m].sum() / NH.sum(),
            100 * L[m].sum() / (L[m] + R[m]).sum()))
    m = x >= .20
    say('  >=20%%: secoes %d, NH %.2f%% do total' % (m.sum(), 100 * NH[m].sum() / NH.sum()))


# regressões com efeito fixo de local e erro agrupado (implementação própria)
def fe_reg(y, X, w=None):
    m = multi & np.all(np.isfinite(X), axis=1) & np.isfinite(y)
    c = np.bincount(g[m], minlength=g.max() + 1); m = m & (c[g] >= 2)
    gg = np.unique(g[m], return_inverse=True)[1]
    G = gg.max() + 1
    def dm(a):
        mu = np.bincount(gg, weights=a, minlength=G) / np.bincount(gg, minlength=G)
        return a - mu[gg]
    yd = dm(y[m]); Xd = np.column_stack([dm(X[m, j]) for j in range(X.shape[1])])
    XtX = Xd.T @ Xd; b = np.linalg.solve(XtX, Xd.T @ yd); e = yd - Xd @ b
    Sg = np.column_stack([np.bincount(gg, weights=Xd[:, j] * e, minlength=G) for j in range(X.shape[1])])
    inv = np.linalg.inv(XtX); N = len(yd); k = X.shape[1]
    V = G / (G - 1) * (N - 1) / (N - k) * inv @ (Sg.T @ Sg) @ inv
    return b, np.sqrt(np.diag(V)), N, G


dNH = NH2 - NH1; dOut = (C2 - NH2) - (C1 - NH1)
for nome, yv in (('Lula', L2 - L1), ('Flavio', R2 - R1)):
    b, se, N, G = fe_reg(yv, np.column_stack([dNH, dOut]))
    say('var votos %s: dNH %.4f (%.4f) dOutros %.4f (%.4f) n %d locais %d' % (nome, b[0], se[0], b[1], se[1], N, G))
    b, se, N, G = fe_reg(yv, np.column_stack([dNH, dOut, O1, C1]))
    say('   com controles O1 e C1: dNH %.4f (%.4f) dOutros %.4f (%.4f)' % (b[0], se[0], b[1], se[1]))
# nível no 2T
res = {}
for nome, yv in (('Lula', L2), ('Flavio', R2)):
    b, se, N, G = fe_reg(yv, np.column_stack([NH2, C2 - NH2]))
    res[nome] = b
    say('nivel T2 %s: por NH %.4f (%.4f) por nao-NH %.4f (%.4f)' % (nome, b[0], se[0], b[1], se[1]))
sal = res['Lula'][0] - res['Flavio'][0]
say('fatia Lula entre NH %.4f; saldo por NH %.4f; saldo total %.0f; margem restante %.0f' % (
    res['Lula'][0] / (res['Lula'][0] + res['Flavio'][0]), sal, sal * a2['NH'], (a2['L'] - a2['R']) - sal * a2['NH']))
# o mesmo no 1T (controle: turno vencido por Flávio)
for nome, yv in (('Lula', L1), ('Flavio', R1)):
    b, se, N, G = fe_reg(yv, np.column_stack([NH1, C1 - NH1]))
    say('nivel T1 %s: por NH %.4f (%.4f) por nao-NH %.4f (%.4f)' % (nome, b[0], se[0], b[1], se[1]))

# quase unânimes no 2T (todas as seções, inclusive exterior)
allk = list(T2.keys())
def qu(cond, ext=True):
    return [k for k in allk if (ext or br(k)) and (T2[k]['L'] + T2[k]['R']) > 0 and cond(T2[k])]
fr = lambda v: v['L'] / (v['L'] + v['R'])
for nome, cond in (('L100', lambda v: v['R'] == 0 and v['L'] > 0), ('R100', lambda v: v['L'] == 0 and v['R'] > 0),
                   ('L>=90', lambda v: 10 * v['L'] >= 9 * (v['L'] + v['R'])), ('L>90', lambda v: 10 * v['L'] > 9 * (v['L'] + v['R'])),
                   ('R>=90', lambda v: 10 * v['R'] >= 9 * (v['L'] + v['R'])), ('R>90', lambda v: 10 * v['R'] > 9 * (v['L'] + v['R']))):
    a = qu(cond); b_ = qu(cond, False)
    say(nome, 'total', len(a), 'brasil', len(b_), 'exterior', len(a) - len(b_))
# taxa NH nas quase unânimes do Brasil, com esperado pela UF
ufrate = {u: tot(T2, lambda k, u=u: k.startswith(u + '|')) for u in ufs}
ufr = {u: s['NH'] / s['comp'] for u, s in ufrate.items()}
def perfil(kk):
    nh = sum(T2[k]['NH'] for k in kk); c = sum(T2[k]['comp'] for k in kk)
    esp = sum(T2[k]['comp'] * ufr[k.split('|')[0]] for k in kk) / c
    taxas = np.array([T2[k]['NH'] / T2[k]['comp'] for k in kk])
    return {'n': len(kk), 'pctNH': round(100 * nh / c, 3), 'esperado_UF': round(100 * esp, 3), 'mediana': round(100 * float(np.median(taxas)), 3),
            'pct_com_taxa_20+': round(100 * float((taxas >= .2).mean()), 2)}
Lm90 = qu(lambda v: 10 * v['L'] > 9 * (v['L'] + v['R']), False)
Rm90 = qu(lambda v: 10 * v['R'] > 9 * (v['L'] + v['R']), False)
L100 = qu(lambda v: v['R'] == 0 and v['L'] > 0, False)
for nome, kk in (('Lula>90', Lm90), ('Flavio>90', Rm90), ('Lula100', L100)):
    say(nome, perfil(kk))
# 1% de taxa mais alta (Brasil, 2T)
kb = [k for k in allk if br(k) and T2[k]['comp'] > 0]
tx = np.array([T2[k]['NH'] / T2[k]['comp'] for k in kb])
lim1 = np.quantile(tx, .99)
top = [k for k, t in zip(kb, tx) if t >= lim1]
sL = set(Lm90)
say('1%% mais alto: limiar %.4f secoes %d Lula>90 entre elas %d' % (lim1, len(top), sum(1 for k in top if k in sL)))
# as mesmas seções Lula>90 no T1
nh1 = sum(T1[k]['NH'] for k in Lm90 if k in T1); c1 = sum(T1[k]['comp'] for k in Lm90 if k in T1)
l1 = sum(T1[k]['L'] for k in Lm90 if k in T1); v1 = sum(T1[k]['L'] + T1[k]['R'] + T1[k]['O'] for k in Lm90 if k in T1)
say('Lula>90 no T1: pctNH %.3f, L/validos T1 %.3f' % (100 * nh1 / c1, 100 * l1 / v1))
out['Lm90'] = Lm90

# placebo 2022 e 2018
x2d = dict(zip(ks, x2)); y2d = dict(zip(ks, y2))
for ano in ('2022', '2018'):
    P = json.load(gzip.open(f'{S}/dados2t/secoes{ano}.json.gz', 'rt'))
    kk = [k for k in ks if k in P and '2' in P[k] and (P[k]['2']['L'] + P[k]['2']['R']) > 0]
    xp = np.array([x2d[k] for k in kk]); yp = np.array([P[k]['2']['L'] / (P[k]['2']['L'] + P[k]['2']['R']) for k in kk])
    yc = np.array([y2d[k] for k in kk])
    Lp = np.array([P[k]['2']['L'] for k in kk], float); Rp = np.array([P[k]['2']['R'] for k in kk], float)
    say(ano, 'secoes casadas', len(kk), 'corr taxa2026 x fatia %s: %.4f ; 2026 nas mesmas: %.4f' % (ano, corr(xp, yp), corr(xp, yc)))
    # dentro do local (local de 2026)
    idx = {k: i for i, k in enumerate(ks)}
    sel = np.zeros(len(ks), bool); yy = np.full(len(ks), np.nan)
    for k, v in zip(kk, yp): sel[idx[k]] = True; yy[idx[k]] = v
    say('   dentro do local: placebo %.4f (n %d); 2026 mesmas %.4f' % (corr_fe(np.where(sel, x2, np.nan), yy) + (corr_fe(np.where(sel, x2, np.nan), np.where(sel, y2, np.nan))[0],)))
    for lo, hi in ((0, .05), (.50, 1.01)):
        m = (xp >= lo) & (xp < hi)
        say('   faixa [%.2f,%.2f) secoes %d fatia %s %.2f%%' % (lo, hi, m.sum(), ano, 100 * Lp[m].sum() / (Lp[m] + Rp[m]).sum()))
    q = [k for k in Lm90 if k in P and '2' in P[k] and (P[k]['2']['L'] + P[k]['2']['R']) > 0]
    lq = sum(P[k]['2']['L'] for k in q); vq = sum(P[k]['2']['L'] + P[k]['2']['R'] for k in q)
    a90 = sum(1 for k in q if P[k]['2']['L'] > .9 * (P[k]['2']['L'] + P[k]['2']['R']))
    say('   Lula>90 2026 em %s: casadas %d, fatia %.2f%%, acima de 90%% %.1f%%' % (ano, len(q), 100 * lq / vq, 100 * a90 / len(q)))
    del P
json.dump({k: v for k, v in out.items() if k != 'Lm90'}, open(f'{D}/resultado.json', 'w'), indent=1, default=str)
say('fim')
