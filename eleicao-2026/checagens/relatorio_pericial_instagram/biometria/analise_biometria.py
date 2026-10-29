"""Capítulo 3 e anexo do "Relatório Pericial Independente": liberação sem biometria (QT_ELEI_BIOM_SEM_HABILITACAO).

Entradas: base por seção 2026 (votos), cache do T21 com NH por seção nos dois turnos de 2026 (lido dos zips do bweb;
conferido de novo, seção a seção, por conferir_bweb.py), base 2022 e base 2018 (placebo: o voto na mesma seção antes).
Cada base é lida uma vez.

Definições por seção: x = NH / comparecimento (taxa sem biometria); y = L / (L + R) (fatia de Lula nos votos dos dois
finalistas; no 2º turno é a fatia dos válidos). Exterior (ZZ) fica fora das correlações (lá não há biometria).

Uso: python3 -I analise_biometria.py <secoes2026> <cache_t21> <secoes2022> <secoes2018> <lib_dir> <saida.json>
"""
import gzip, json, sys, collections
import numpy as np

base26, cache_p, base22, base18, libdir, saida = sys.argv[1:7]
sys.path.insert(0, libdir)
from lib import fe_ols  # noqa: E402

R = {}


def carregar(p):
    with gzip.open(p, 'rt') as f:
        return json.load(f)


# ---------------- 2026 ----------------
d = carregar(base26)
c = carregar(cache_p)
c1, c2 = c['1'], c['2']
del c

chaves = []
cols = collections.defaultdict(list)
tot = {t: collections.Counter() for t in ('1', '2')}
uf_tot = collections.defaultdict(collections.Counter)
mun_tot = collections.defaultdict(collections.Counter)
for k, v in d.items():
    uf, mun, zona, _ = k.split('|')
    for t, cc in (('1', c1), ('2', c2)):
        s = v.get(t)
        if s is None:
            continue
        nh = cc[k][3] if k in cc and cc[k][3] is not None else 0
        T = tot[t]
        T['secoes'] += 1; T['comp'] += s['comp']; T['NH'] += nh; T['L'] += s['L']; T['R'] += s['R']; T['O'] += s.get('O', 0)
        T['B'] += s['B']; T['N'] += s['N']; T['apt'] += s['apt']
        if uf != 'ZZ':
            U = uf_tot[(uf, t)]
            U['comp'] += s['comp']; U['NH'] += nh; U['L'] += s['L']; U['R'] += s['R']; U['O'] += s.get('O', 0)
            M = mun_tot[(uf + '|' + mun, t)]
            M['comp'] += s['comp']; M['NH'] += nh; M['L'] += s['L']; M['R'] += s['R']; M['O'] += s.get('O', 0); M['apt'] += s['apt']
    if uf == 'ZZ':
        continue
    s1, s2 = v.get('1'), v.get('2')
    a1, a2 = c1.get(k), c2.get(k)
    chaves.append(k)
    cols['uf'].append(uf)
    cols['loc2'].append(f"{uf}|{mun}|{zona}|{s2['loc']}" if s2 else '')
    cols['loc1'].append(f"{uf}|{mun}|{zona}|{s1['loc']}" if s1 else '')
    cols['mun'].append(uf + '|' + mun)
    for t, s, a in (('1', s1, a1), ('2', s2, a2)):
        ok = s is not None and a is not None and a[3] is not None
        cols['ok' + t].append(ok)
        cols['C' + t].append(s['comp'] if ok else 0)
        cols['NH' + t].append(a[3] if ok else 0)
        cols['L' + t].append(s['L'] if ok else 0)
        cols['R' + t].append(s['R'] if ok else 0)
        cols['O' + t].append(s.get('O', 0) if ok else 0)
        cols['apt' + t].append(s['apt'] if ok else 0)
del d, c1, c2

A = {k: np.array(v) for k, v in cols.items()}
del cols
chaves = np.array(chaves)
n = len(chaves)
print('seções no Brasil (27 UFs):', n, flush=True)

# ---------------- (a) totais ----------------
for t in ('1', '2'):
    T = tot[t]
    T['pct_NH_comp'] = 100 * T['NH'] / T['comp']
    T['L_menos_R'] = T['L'] - T['R']
    T['pct_L_validos'] = 100 * T['L'] / (T['L'] + T['R'] + T['O'])
    T['pct_R_validos'] = 100 * T['R'] / (T['L'] + T['R'] + T['O'])
    T['pct_L_dos_dois'] = 100 * T['L'] / (T['L'] + T['R'])
R['totais'] = {t: dict(v) for t, v in tot.items()}
R['totais']['razao_NH2_sobre_margem2'] = tot['2']['NH'] / tot['2']['L_menos_R']
R['totais']['NH_total_dos_dois_turnos'] = tot['1']['NH'] + tot['2']['NH']

# 1º turno: onde Flávio teve mais votos que Lula
uf_venc = {}
for t in ('1', '2'):
    ufs = sorted({u for (u, tt) in uf_tot if tt == t})
    uf_venc[t] = {'UFs_Flavio_a_frente': [u for u in ufs if uf_tot[(u, t)]['R'] > uf_tot[(u, t)]['L']],
                  'UFs_Lula_a_frente': [u for u in ufs if uf_tot[(u, t)]['L'] > uf_tot[(u, t)]['R']]}
    muns = [m for (m, tt) in mun_tot if tt == t]
    uf_venc[t]['municipios'] = len(muns)
    uf_venc[t]['municipios_Flavio_a_frente'] = sum(1 for m in muns if mun_tot[(m, t)]['R'] > mun_tot[(m, t)]['L'])
    uf_venc[t]['municipios_Lula_a_frente'] = sum(1 for m in muns if mun_tot[(m, t)]['L'] > mun_tot[(m, t)]['R'])
    ok = A['ok' + t]
    uf_venc[t]['secoes_Flavio_a_frente'] = int(((A['R' + t] > A['L' + t]) & ok).sum())
    uf_venc[t]['secoes_Lula_a_frente'] = int(((A['L' + t] > A['R' + t]) & ok).sum())
    uf_venc[t]['secoes'] = int(ok.sum())
    # eleitores (comparecimento) nas UFs em que Flávio ficou à frente
    cf = sum(uf_tot[(u, t)]['comp'] for u in uf_venc[t]['UFs_Flavio_a_frente'])
    ct = sum(uf_tot[(u, t)]['comp'] for u in ufs)
    uf_venc[t]['pct_comparecimento_nas_UFs_Flavio_a_frente'] = 100 * cf / ct
R['quem_a_frente'] = uf_venc

# por UF: taxa NH e fatia de Lula, nos dois turnos; correlação entre UFs
uf_tab = {}
for t in ('1', '2'):
    xs, ys, ws = [], [], []
    for (u, tt), U in sorted(uf_tot.items()):
        if tt != t:
            continue
        x = 100 * U['NH'] / U['comp']; y = 100 * U['L'] / (U['L'] + U['R'])
        uf_tab.setdefault(u, {})[t] = {'pct_NH': round(x, 3), 'pct_L_dos_dois': round(y, 2)}
        xs.append(x); ys.append(y); ws.append(U['comp'])
    uf_tab.setdefault('_corr', {})[t] = float(np.corrcoef(xs, ys)[0, 1])
R['por_UF'] = uf_tab


# ---------------- ferramentas ----------------
def wcorr(x, y, w=None):
    w = np.ones_like(x) if w is None else w
    mx, my = np.average(x, weights=w), np.average(y, weights=w)
    cov = np.average((x - mx) * (y - my), weights=w)
    return float(cov / np.sqrt(np.average((x - mx) ** 2, weights=w) * np.average((y - my) ** 2, weights=w)))


def demean(v, g, w):
    sw = np.bincount(g, weights=w)
    m = np.bincount(g, weights=w * v) / np.where(sw > 0, sw, 1)
    return v - m[g]


def within_corr(x, y, grupos, w=None):
    w = np.ones_like(x, dtype=float) if w is None else w.astype(float)
    _, g = np.unique(grupos, return_inverse=True)
    cnt = np.bincount(g); ok = cnt[g] >= 2
    x, y, w, g = x[ok], y[ok], w[ok], g[ok]
    _, g = np.unique(g, return_inverse=True)
    return wcorr(demean(x, g, w), demean(y, g, w), w), int(ok.sum()), int(g.max() + 1)


def ols_cluster(y, x, grupos, w=None):
    """y = a + b x, erro agrupado (CR1)."""
    w = np.ones_like(x, dtype=float) if w is None else w.astype(float)
    X = np.column_stack([np.ones_like(x), x])
    Xw = X * w[:, None]
    XtX = X.T @ Xw
    b = np.linalg.solve(XtX, Xw.T @ y)
    e = y - X @ b
    _, g = np.unique(grupos, return_inverse=True)
    G = g.max() + 1
    S = np.column_stack([np.bincount(g, weights=w * X[:, j] * e, minlength=G) for j in range(2)])
    inv = np.linalg.inv(XtX)
    N = len(y)
    V = G / (G - 1) * (N - 1) / (N - 2) * inv @ (S.T @ S) @ inv
    return float(b[1]), float(np.sqrt(V[1, 1]))


def bateria(x, y, loc, w, nome):
    """Correlação e inclinação: entre seções (sem efeito fixo) e dentro do local (efeito fixo de local)."""
    out = {'n': int(len(x))}
    out['corr_sem_EF'] = wcorr(x, y)
    out['corr_sem_EF_peso_comp'] = wcorr(x, y, w)
    b, se = ols_cluster(y, x, loc)
    out['incl_sem_EF'] = {'b': b, 'ep_agrupado_local': se}
    r, nn, G = within_corr(x, y, loc)
    out['corr_EF_local'] = r; out['n_EF'] = nn; out['locais_EF'] = G
    out['corr_EF_local_peso_comp'] = within_corr(x, y, loc, w)[0]
    f = fe_ols(y, x, loc, None, ['x'])
    out['incl_EF_local'] = {'b': f['coef']['x'], 'ep': f['ep']['x']}

    print(nome, json.dumps({k: (round(v, 4) if isinstance(v, float) else v) for k, v in out.items() if not isinstance(v, dict)}), flush=True)
    return out


A_mun_sel = [None]

# ---------------- (c) correlação em nível, cada turno ----------------
cor = {}
for t in ('1', '2'):
    C, NH, L, Rr, O = (A[c + t].astype(float) for c in ('C', 'NH', 'L', 'R', 'O'))
    sel = A['ok' + t] & (C > 0) & (L + Rr > 0)
    x = NH[sel] / C[sel]; y = L[sel] / (L[sel] + Rr[sel])
    loc = A['loc' + t][sel]
    cor[t] = {'y_fatia_dos_dois': bateria(x, y, loc, C[sel], f'nivel T{t} L/(L+R)')}
    if t == '1':
        yv = L[sel] / (L[sel] + Rr[sel] + O[sel])
        cor[t]['y_fatia_dos_validos'] = bateria(x, yv, loc, C[sel], 'nivel T1 L/validos')
    # dentro do município (efeito fixo de município)
    cor[t]['corr_EF_municipio'] = within_corr(x, y, A['mun'][sel])[0]
    cor[t]['corr_EF_UF'] = within_corr(x, y, A['uf'][sel])[0]
R['correlacao_nivel'] = cor

# ---------------- variação entre turnos ----------------
sel = A['ok1'] & A['ok2'] & (A['C1'] > 0) & (A['C2'] > 0) & (A['L1'] + A['R1'] > 0) & (A['L2'] + A['R2'] > 0)
C1, C2 = A['C1'][sel].astype(float), A['C2'][sel].astype(float)
x1, x2 = A['NH1'][sel] / C1, A['NH2'][sel] / C2
y1 = A['L1'][sel] / (A['L1'][sel] + A['R1'][sel]); y2 = A['L2'][sel] / (A['L2'][sel] + A['R2'][sel])
yv1 = A['L1'][sel] / (A['L1'][sel] + A['R1'][sel] + A['O1'][sel])
loc = A['loc2'][sel]
dx = x2 - x1
var = {'dy_fatia_dos_dois': bateria(dx, y2 - y1, loc, C2, 'var dx x d(L/(L+R))'),
       'dy_fatia_validos_1t_para_2t': bateria(dx, y2 - yv1, loc, C2, 'var dx x d(L/validos)')}
# variação em votos (contas do T21 refeitas aqui em versão simples): dL contra dNH e d(C-NH), EF local
dL = (A['L2'][sel] - A['L1'][sel]).astype(float); dR = (A['R2'][sel] - A['R1'][sel]).astype(float)
dNH = (A['NH2'][sel] - A['NH1'][sel]).astype(float); dCom = (C2 - A['NH2'][sel]) - (C1 - A['NH1'][sel])
fL = fe_ols(dL, np.column_stack([dNH, dCom]), loc, None, ['dNH', 'dCom'])
fR = fe_ols(dR, np.column_stack([dNH, dCom]), loc, None, ['dNH', 'dCom'])
var['votos_por_variacao_EF_local'] = {'Lula': fL, 'Flavio': fR}
# faixas de variação da taxa
fx = [(-1, -0.05), (-0.05, -0.02), (-0.02, 0.02), (0.02, 0.05), (0.05, 1.01)]
tab = []
for lo, hi in fx:
    m = (dx >= lo) & (dx < hi)
    tab.append({'faixa_dx_pp': f'[{100*lo:.0f},{100*hi:.0f})', 'secoes': int(m.sum()),
                'media_dy_pp': float(100 * (y2[m] - y1[m]).mean()),
                'dy_agregado_pp': float(100 * (A['L2'][sel][m].sum() / (A['L2'][sel][m] + A['R2'][sel][m]).sum()
                                         - A['L1'][sel][m].sum() / (A['L1'][sel][m] + A['R1'][sel][m]).sum()))})
var['faixas_dx'] = tab
var['n'] = int(sel.sum())
var['media_x1_pct'] = float(100 * A['NH1'][sel].sum() / C1.sum()); var['media_x2_pct'] = float(100 * A['NH2'][sel].sum() / C2.sum())
var['corr_x1_x2_entre_secoes'] = wcorr(x1, x2)
R['correlacao_variacao'] = var

# estimativa ecológica em nível (2º turno): votos de Lula e de Flávio por eleitor NH e por eleitor não NH, EF local
s2 = A['ok2'] & (A['C2'] > 0)
NH2 = A['NH2'][s2].astype(float); Com2 = A['C2'][s2] - NH2
fL2 = fe_ols(A['L2'][s2].astype(float), np.column_stack([NH2, Com2]), A['loc2'][s2], None, ['NH', 'naoNH'])
fR2 = fe_ols(A['R2'][s2].astype(float), np.column_stack([NH2, Com2]), A['loc2'][s2], None, ['NH', 'naoNH'])
liq = fL2['coef']['NH'] - fR2['coef']['NH']
R['ecologico_nivel_T2'] = {'Lula': fL2, 'Flavio': fR2, 'saldo_Lula_por_eleitor_NH': liq,
                           'saldo_Lula_por_eleitor_naoNH': fL2['coef']['naoNH'] - fR2['coef']['naoNH'],
                           'saldo_atribuivel_aos_NH_votos': liq * tot['2']['NH'],
                           'margem': tot['2']['L_menos_R']}

# ---------------- faixas de taxa (afirmação c) ----------------
faixas = [(0, .05), (.05, .10), (.10, .15), (.15, .20), (.20, .30), (.30, .50), (.50, 1.01)]
fx_tab = {}
for t in ('1', '2'):
    C, NH, L, Rr, O = (A[c + t].astype(float) for c in ('C', 'NH', 'L', 'R', 'O'))
    sel = A['ok' + t] & (C > 0) & (L + Rr > 0)
    x = NH / np.where(C > 0, C, 1)
    y = L / np.where(L + Rr > 0, L + Rr, 1)
    # desvio da fatia em relação à média do local (dentro do local)
    _, g = np.unique(A['loc' + t][sel], return_inverse=True)
    dev = np.zeros(n); dev[sel] = demean(y[sel], g, np.ones(sel.sum()))
    cnt = np.bincount(g); multi = np.zeros(n, bool); multi[sel] = cnt[g] >= 2
    rows = []
    for lo, hi in faixas:
        m = sel & (x >= lo) & (x < hi)
        r = {'faixa_pct': f'[{100*lo:.0f},{100*hi:.0f})', 'secoes': int(m.sum()), 'comparecimento': int(C[m].sum()),
             'NH': int(NH[m].sum()), 'pct_do_NH_total': float(100 * NH[m].sum() / NH[sel].sum()),
             'pct_L_dos_dois_agregado': float(100 * L[m].sum() / (L[m] + Rr[m]).sum()) if m.any() else None,
             'pct_L_validos_agregado': float(100 * L[m].sum() / (L[m] + Rr[m] + O[m]).sum()) if m.any() else None,
             'desvio_medio_da_fatia_no_local_pp': float(100 * dev[m & multi].mean()) if (m & multi).any() else None,
             'secoes_com_local_multi': int((m & multi).sum())}
        rows.append(r)
    fx_tab[t] = rows
    # Lula > 61% na faixa? quantas seções acima de 20/30/50
    fx_tab[t + '_acima'] = {f'>= {p}%': {'secoes': int((sel & (x >= p / 100)).sum()), 'NH': int(NH[sel & (x >= p / 100)].sum()),
                                         'pct_L_dos_dois': float(100 * L[sel & (x >= p / 100)].sum() / (L + Rr)[sel & (x >= p / 100)].sum())}
                            for p in (20, 30, 50)}
R['faixas_taxa'] = fx_tab

# porte do município (proxy rural): taxa NH e fatia Lula por faixa de aptos do município, 2º turno
mun_apt = collections.Counter()
for (m, t), M in mun_tot.items():
    if t == '2':
        mun_apt[m] = M['apt']
porte = []
for lo, hi in [(0, 10000), (10000, 50000), (50000, 200000), (200000, 1000000), (1000000, 10 ** 9)]:
    ms = [m for m, a in mun_apt.items() if lo <= a < hi]
    nh = sum(mun_tot[(m, '2')]['NH'] for m in ms); cc = sum(mun_tot[(m, '2')]['comp'] for m in ms)
    l = sum(mun_tot[(m, '2')]['L'] for m in ms); r = sum(mun_tot[(m, '2')]['R'] for m in ms)
    nh1 = sum(mun_tot[(m, '1')]['NH'] for m in ms); cc1 = sum(mun_tot[(m, '1')]['comp'] for m in ms)
    porte.append({'aptos_municipio': f'{lo}-{hi}', 'municipios': len(ms), 'pct_NH_T2': 100 * nh / cc, 'pct_NH_T1': 100 * nh1 / cc1,
                  'pct_L_dos_dois_T2': 100 * l / (l + r)})
R['porte_municipio'] = porte

# ---------------- (d) seções quase unânimes ----------------
un = {}
for t in ('2', '1'):
    C, NH, L, Rr, O = (A[c + t].astype(float) for c in ('C', 'NH', 'L', 'R', 'O'))
    V = L + Rr + O
    sel = A['ok' + t] & (C > 0) & (V > 0)
    x = NH / np.where(C > 0, C, 1)
    xs_sorted = np.sort(x[sel])
    tx_uf = {u: uf_tot[(u, t)]['NH'] / uf_tot[(u, t)]['comp'] for (u, tt) in uf_tot if tt == t}
    esp_uf = np.array([tx_uf.get(u, 0) for u in A['uf']])
    _, g = np.unique(A['loc' + t][sel], return_inverse=True)
    devx = np.zeros(n); devx[sel] = demean(x[sel], g, np.ones(sel.sum()))
    cnt = np.bincount(g); multi = np.zeros(n, bool); multi[sel] = cnt[g] >= 2
    grupos = {'Lula_100': sel & (L == V), 'Flavio_100': sel & (Rr == V),
              'Lula_mais_90': sel & (L > 0.9 * V), 'Flavio_mais_90': sel & (Rr > 0.9 * V),
              'Lula_90_ou_mais': sel & (L >= 0.9 * V), 'Flavio_90_ou_mais': sel & (Rr >= 0.9 * V), 'todas': sel}
    out = {}
    for nome, m in grupos.items():
        if not m.any():
            out[nome] = {'secoes': 0}; continue
        pct = np.searchsorted(xs_sorted, x[m], side='right') / len(xs_sorted)
        out[nome] = {'secoes': int(m.sum()), 'comparecimento_mediano': float(np.median(C[m])),
                     'pct_NH_agregado': float(100 * NH[m].sum() / C[m].sum()),
                     'pct_NH_esperado_pela_UF': float(100 * (esp_uf[m] * C[m]).sum() / C[m].sum()),
                     'taxa_mediana_secao_pct': float(100 * np.median(x[m])),
                     'percentil_medio_da_taxa_no_pais': float(100 * pct.mean()),
                     'pct_das_secoes_com_taxa_20_ou_mais': float(100 * (x[m] >= .2).mean()),
                     'pct_das_secoes_no_1pct_mais_alto': float(100 * (pct > 0.99).mean()),
                     'desvio_medio_da_taxa_no_local_pp': float(100 * devx[m & multi].mean()) if (m & multi).any() else None,
                     'secoes_com_local_multi': int((m & multi).sum()),
                     'UFs_top': collections.Counter(A['uf'][m]).most_common(6)}
    # entre as seções de taxa >= 20%: quantas são quase unânimes
    alta = sel & (x >= .2)
    out['entre_secoes_taxa_20_ou_mais'] = {'secoes': int(alta.sum()), 'Lula_mais_90': int((alta & (L > .9 * V)).sum()),
                                           'Flavio_mais_90': int((alta & (Rr > .9 * V)).sum()),
                                           'pct_L_validos': float(100 * L[alta].sum() / V[alta].sum())}
    top1 = sel & (x >= xs_sorted[int(.99 * len(xs_sorted))])
    out['entre_1pct_secoes_taxa_mais_alta'] = {'limiar_pct': float(100 * xs_sorted[int(.99 * len(xs_sorted))]), 'secoes': int(top1.sum()),
                                               'Lula_mais_90': int((top1 & (L > .9 * V)).sum()), 'Flavio_mais_90': int((top1 & (Rr > .9 * V)).sum())}
    un[t] = out
    if t == '2':
        m90 = grupos['Lula_mais_90']
        # as mesmas seções no 1º turno: taxa NH, fatia de Lula, variação da taxa
        ok1 = m90 & A['ok1'] & (A['C1'] > 0)
        un['secoes_Lula_mais_90_T2_no_T1'] = {
            'secoes': int(ok1.sum()),
            'pct_NH_T1': float(100 * A['NH1'][ok1].sum() / A['C1'][ok1].sum()),
            'pct_NH_T2': float(100 * A['NH2'][ok1].sum() / A['C2'][ok1].sum()),
            'pct_L_validos_T1': float(100 * A['L1'][ok1].sum() / (A['L1'] + A['R1'] + A['O1'])[ok1].sum()),
            'pct_L_dos_dois_T1': float(100 * A['L1'][ok1].sum() / (A['L1'] + A['R1'])[ok1].sum()),
            'pct_L_T2': float(100 * A['L2'][ok1].sum() / (A['L2'] + A['R2'])[ok1].sum())}
        okall = A['ok1'] & A['ok2'] & (A['C1'] > 0) & (A['C2'] > 0)
        un['todas_as_secoes_variacao_pp'] = float(100 * (A['NH2'][okall].sum() / A['C2'][okall].sum() - A['NH1'][okall].sum() / A['C1'][okall].sum()))
R['quase_unanimes'] = un


# ---------------- placebo: mesma seção em 2022 e 2018 ----------------
def placebo(path, rotulo):
    b = carregar(path)
    Lp = np.zeros(n); Rp = np.zeros(n); Op1 = np.zeros(n); Lp1 = np.zeros(n); Rp1 = np.zeros(n); okp = np.zeros(n, bool)
    for i, k in enumerate(chaves):
        v = b.get(k)
        if v and '2' in v and '1' in v:
            okp[i] = True
            Lp[i] = v['2']['L']; Rp[i] = v['2']['R']; Lp1[i] = v['1']['L']; Rp1[i] = v['1']['R']; Op1[i] = v['1']['O']
    del b
    out = {'secoes_casadas_pela_chave': int(okp.sum())}
    C, NH = A['C2'].astype(float), A['NH2'].astype(float)
    sel = okp & A['ok2'] & (C > 0) & (Lp + Rp > 0) & (A['L2'] + A['R2'] > 0)
    x = NH[sel] / C[sel]; yp = Lp[sel] / (Lp[sel] + Rp[sel])
    out['taxa_NH_2026_T2_x_fatia_L_2T_' + rotulo] = bateria(x, yp, A['loc2'][sel], C[sel], f'placebo {rotulo} 2T x NH2026')
    y26 = A['L2'][sel] / (A['L2'][sel] + A['R2'][sel])
    out['comparacao_mesmas_secoes_2026'] = bateria(x, y26, A['loc2'][sel], C[sel], f'2026 nas secoes casadas com {rotulo}')
    # faixas
    rows = []
    xall = NH / np.where(C > 0, C, 1)
    for lo, hi in faixas:
        m = sel & (xall >= lo) & (xall < hi)
        rows.append({'faixa_pct_NH_2026': f'[{100*lo:.0f},{100*hi:.0f})', 'secoes': int(m.sum()),
                     'pct_L_dos_dois_' + rotulo + '_2T': float(100 * Lp[m].sum() / (Lp[m] + Rp[m]).sum()) if m.any() else None,
                     'pct_L_dos_dois_2026_2T': float(100 * A['L2'][m].sum() / (A['L2'][m] + A['R2'][m]).sum()) if m.any() else None})
    out['faixas'] = rows
    # variação da taxa NH entre turnos de 2026 contra a variação de Lula 1T->2T no ano placebo (deve ser ~0)
    sel2 = sel & A['ok1'] & (A['C1'] > 0) & (Lp1 + Rp1 > 0)
    dx = NH[sel2] / C[sel2] - A['NH1'][sel2] / A['C1'][sel2]
    dyp = Lp[sel2] / (Lp[sel2] + Rp[sel2]) - Lp1[sel2] / (Lp1[sel2] + Rp1[sel2])
    out['dx_2026_x_dy_' + rotulo] = bateria(dx, dyp, A['loc2'][sel2], C[sel2], f'placebo var {rotulo}')
    # quase unânimes 2026 (Lula > 90% no 2T) na mesma seção no ano placebo
    V2 = (A['L2'] + A['R2']).astype(float)
    m90 = okp & A['ok2'] & (V2 > 0) & (A['L2'] > .9 * V2) & (Lp + Rp > 0)
    out['secoes_Lula_mais_90_2026_no_' + rotulo] = {'secoes': int(m90.sum()),
                                                     'pct_L_dos_dois_' + rotulo: float(100 * Lp[m90].sum() / (Lp[m90] + Rp[m90]).sum()),
                                                     'pct_secoes_com_L_mais_90_em_' + rotulo: float(100 * (Lp[m90] > .9 * (Lp[m90] + Rp[m90])).mean())}
    return out


R['placebo_2022'] = placebo(base22, '2022')
R['placebo_2018'] = placebo(base18, '2018')


def limpar(o):
    if isinstance(o, dict):
        return {str(k): limpar(v) for k, v in o.items()}
    if isinstance(o, (list, tuple)):
        return [limpar(v) for v in o]
    if isinstance(o, (np.integer,)):
        return int(o)
    if isinstance(o, (np.floating,)):
        return float(o)
    return o


json.dump(limpar(R), open(saida, 'w'), indent=1, ensure_ascii=False)
print('gravado', saida)
