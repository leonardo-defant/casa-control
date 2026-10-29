"""Conferência independente das contas do L7 (Adendo 18). Código próprio: leitura do bweb (ler_bweb2t.py), dos logs
(logs_bio.py) e regressão com efeito fixo escrita aqui, sem lib.fe_ols.
Uso: python3 -I conferir_L7.py <secoes2026.json.gz> <bweb2t_pres.json.gz> <logs_bio.json> <bweb1t_urna_carga.json.gz|-> <saida.json>"""
import collections, gzip, json, math, sys
import numpy as np

base_p, bw_p, logs_p, b1_p, saida = sys.argv[1:6]
base = json.load(gzip.open(base_p, 'rt'))
bw = json.load(gzip.open(bw_p, 'rt'))
lg = json.load(open(logs_p))
out = {}


def fe(y, x, g, w):
    """y = b x + efeito fixo de g, MQP; erro agrupado por g (CR1). Retorna b, ep, n, grupos usados."""
    y = np.asarray(y, float); x = np.asarray(x, float); w = np.asarray(w, float)
    _, gi = np.unique(g, return_inverse=True)
    cnt = np.bincount(gi)
    ok = cnt[gi] >= 2
    y, x, w, gi = y[ok], x[ok], w[ok], gi[ok]
    _, gi = np.unique(gi, return_inverse=True)
    G = gi.max() + 1
    sw = np.bincount(gi, weights=w, minlength=G)
    yd = y - (np.bincount(gi, weights=w * y, minlength=G) / sw)[gi]
    xd = x - (np.bincount(gi, weights=w * x, minlength=G) / sw)[gi]
    sxx = np.sum(w * xd * xd)
    b = np.sum(w * xd * yd) / sxx
    e = yd - b * xd
    sc = np.bincount(gi, weights=w * xd * e, minlength=G)
    N = len(y)
    V = (G / (G - 1)) * ((N - 1) / (N - 1)) * np.sum(sc ** 2) / sxx ** 2  # k = 1 regressor
    return float(b), float(math.sqrt(V)), int(N), int(G)


# ---------- conferência da leitura: votos do bweb contra a base
dif = sum(1 for k, v in bw.items() if k in base and '2' in base[k] and (base[k]['2']['L'], base[k]['2']['R']) != (v['L'], v['R']))
out['leitura'] = {'secoes_bweb': len(bw), 'secoes_base': len(base), 'votos_diferentes_da_base': dif,
                  'bweb_fora_da_base': sum(1 for k in bw if k not in base)}

# ---------- D1
S = {}
vesp_mesma = []
for k, v in bw.items():
    if v['carga'][:10] != '2026-10-24':
        continue
    s = base.get(k, {})
    u1 = s.get('1', {}).get('urna')
    if u1 is not None and str(u1) != v['urna']:
        S[k] = v
    else:
        vesp_mesma.append((k, v['urna'], u1, v['tipo']))
por_uf = collections.Counter(k.split('|')[0] for k in S)
out['D1'] = {'S': len(S), 'por_uf': dict(sorted(por_uf.items())), 'vespera_mesma_urna': vesp_mesma}
# Alagoas nominal
AL = [('MACEIÓ', 2, 365, 'B'), ('MACEIÓ', 2, 355, 'B'), ('MACEIÓ', 1, 375, 'I'), ('TRAIPU', 20, 84, 'I'),
      ('MACEIÓ', 54, 566, 'I'), ('MARECHAL DEODORO', 26, 29, 'I'), ('SANTANA DO IPANEMA', 19, 234, 'I'),
      ('BRANQUINHA', 9, 12, 'I'), ('MONTEIRÓPOLIS', 29, 76, 'I'), ('POÇO DAS TRINCHEIRAS', 50, 37, 'I'),
      ('ÁGUA BRANCA', 39, 63, 'I'), ('GIRAU DO PONCIANO', 44, 32, 'I'), ('CORURIPE', 7, 150, 'I'),
      ('MARAGOGI', 14, 129, 'I'), ('FEIRA GRANDE', 49, 80, 'I'), ('PÃO DE AÇÚCAR', 11, 15, 'I'),
      ('JOAQUIM GOMES', 53, 5, 'I'), ('SÃO JOSÉ DA TAPERA', 51, 90, 'I'), ('IGREJA NOVA', 37, 187, 'I'),
      ('TEOTÔNIO VILELA', 34, 96, 'I'), ('SÃO LUÍS DO QUITUNDE', 17, 150, 'A'), ('JEQUIÁ DA PRAIA', 18, 187, 'A'),
      ('ARAPIRACA', 22, 519, 'A')]
cod = collections.defaultdict(set)
for k, v in bw.items():
    if k.startswith('AL|'):
        cod[v['mun']].add(int(k.split('|')[1]))
al = []
for m, z, se, t in AL:
    cs = cod.get(m, set())
    ks = [f'AL|{c}|{z}|{se}' for c in cs if f'AL|{c}|{z}|{se}' in bw]
    k = ks[0] if len(ks) == 1 else None
    al.append({'mun': m, 'z': z, 's': se, 'tipo': t, 'chave': k, 'achou': len(ks), 'em_S': k in S if k else None,
               'carga2': bw[k]['carga'] if k else None, 'urna2': bw[k]['urna'] if k else None,
               'urna1': base.get(k, {}).get('1', {}).get('urna') if k else None})
SAL = {k for k in S if k.startswith('AL|')}
out['D1']['AL'] = {'integridade_em_S': sum(1 for a in al if a['tipo'] in 'BI' and a['em_S']),
                   'integridade': sum(1 for a in al if a['tipo'] in 'BI'),
                   'autenticidade_em_S': sum(1 for a in al if a['tipo'] == 'A' and a['em_S']),
                   'S_fora_lista': sorted(SAL - {a['chave'] for a in al}), 'lista': al}
if b1_p != '-':
    b1 = json.load(gzip.open(b1_p, 'rt'))
    v1 = collections.Counter(k.split('|')[0] for k, (u, c) in b1.items() if c[:10] == '2026-10-03')
    # urna do 1º turno lida direto do bweb do 1º turno, contra a base
    dif_urna = sum(1 for k, (u, c) in b1.items() if k in base and '1' in base[k] and str(base[k]['1']['urna']) != u)
    S_b1 = sum(1 for k, v in bw.items() if v['carga'][:10] == '2026-10-24' and k in b1 and b1[k][0] != v['urna'])
    out['D1']['1t'] = {'carga_vespera_1t': sum(v1.values()), 'por_uf': dict(sorted(v1.items())),
                       'urna_1t_base_diferente_do_bweb1t': dif_urna, 'S_com_urna_do_bweb1t': S_b1,
                       'AL_carga1t_autenticidade': [b1.get(a['chave']) for a in al if a['tipo'] == 'A' and a['chave']]}

# ---------- D2 logs
rows = []
for k, d in lg.items():
    c = d['c']
    if not c.get('hab') or k not in bw:
        continue
    bio = sum(v for t, v in d['tipos'].items() if 'biométrica' in t)
    rows.append((k, c['hab'], bio, c.get('mesario_habilitou', 0), c.get('comp', 0), bw[k]['comp'], bw[k]['biomsem']))
hab = np.array([r[1] for r in rows], float); bio = np.array([r[2] for r in rows], float)
mes = np.array([r[3] for r in rows], float); comp_l = np.array([r[4] for r in rows]); comp_b = np.array([r[5] for r in rows])
sem = np.array([r[6] for r in rows], float)
sh = bio / hab
out['D2'] = {'urnas': len(rows), 'urnas_no_log': len(lg), 'hab': int(hab.sum()), 'bio': int(bio.sum()),
             'pct_bio': float(100 * bio.sum() / hab.sum()), 'zero_bio': int((bio == 0).sum()), 'cem_bio': int((bio == hab).sum()),
             'ge98': int((sh >= 0.98).sum()), 'ate100_ge95': int(((hab <= 100) & (sh >= 0.95)).sum()), 'ate100': int((hab <= 100).sum()),
             'q_share': {q: float(np.quantile(sh, q / 100)) for q in (0, 1, 5, 50, 99, 100)},
             'q_hab': {q: float(np.quantile(hab, q / 100)) for q in (0, 1, 50)},
             'comp_log_igual_bweb': int((comp_l == comp_b).sum()),
             'manual_mesario_total': int(mes.sum()), 'hab_menos_bio_total': int((hab - bio).sum()),
             'campo_bweb_vs_nao_bio': {'igual': int((sem == hab - bio).sum()), 'menor': int((sem < hab - bio).sum()),
                                       'maior': int((sem > hab - bio).sum())},
             'regra_de_3_pct': 300 / len(rows), 'regra_de_3_secoes': 3 / len(rows) * len(bw),
             'menor_share_secao': min(rows, key=lambda r: r[2] / r[1])[0]}

# ---------- país: r = biomsem/comp
keys, Y, W, LOC, R, Y1 = [], [], [], [], [], []
V2 = Lt = Rt = 0
sem_certo = 0
ncomp = 0
for k, s in base.items():
    if '1' not in s or '2' not in s:
        continue
    a, b = s['1'], s['2']
    V2 += b['L'] + b['R']; Lt += b['L']; Rt += b['R']
    v = bw.get(k)
    if v is None:
        continue
    if v['comp'] > 0:
        ncomp += 1
        if v['biomsem'] >= v['comp']:
            sem_certo += 1
    if a['L'] + a['R'] <= 0 or b['L'] + b['R'] <= 0 or v['comp'] <= 0:
        continue
    uf, m, z, _ = k.split('|')
    keys.append(k)
    Y.append(100 * b['L'] / (b['L'] + b['R']) - 100 * a['L'] / (a['L'] + a['R']))
    Y1.append(100 * a['L'] / (a['L'] + a['R']))
    W.append(b['L'] + b['R'])
    LOC.append(f"{uf}|{m}|{z}|{v['loc']}")
    R.append(v['biomsem'] / v['comp'])
Y = np.array(Y); W = np.array(W, float); LOC = np.array(LOC); R = np.array(R); Y1 = np.array(Y1)
ZZ = np.array([k.startswith('ZZ|') for k in keys])
margem = Lt - Rt
out['pais'] = {'V2': int(V2), 'L': int(Lt), 'R': int(Rt), 'margem': int(margem), 'regua': 100 * margem / 2 / V2,
               'secoes_comp': ncomp, 'sem_bio_certo': sem_certo,
               'r_ge_09': int((R >= 0.9).sum()), 'r_ge_05': int((R >= 0.5).sum()),
               'r_ge_09_brasil': int(((R >= 0.9) & ~ZZ).sum()), 'r_ge_05_brasil': int(((R >= 0.5) & ~ZZ).sum()),
               'ZZ_secoes_reg': int(ZZ.sum()), 'ZZ_biomsem_total': int(sum(bw[k]['biomsem'] for k in bw if k.startswith('ZZ|'))),
               'ZZ_secoes_bweb': sum(1 for k in bw if k.startswith('ZZ|'))}

# ---------- D3
d3 = {}
for nome, lim in (('r>=0,9', 0.9), ('r>=0,5', 0.5), ('r>=0,3', 0.3)):
    g = (R >= lim).astype(float)
    b, ep, n, G = fe(Y, g, LOC, W)
    bp, epp, _, _ = fe(Y1, g, LOC, W)
    bu, epu, _, _ = fe(Y, g, LOC, np.ones_like(W))
    d3[nome] = {'n_grupo': int(g.sum()), 'coef': b, 'ep': ep, 'n': n, 'locais': G, 'placebo': bp, 'ep_placebo': epp,
                'sem_peso': bu, 'ep_sem_peso': epu}
# contínua: virada contra r
b, ep, n, G = fe(Y, R, LOC, W)
d3['continuo_r'] = {'coef_por_unidade_de_r': b, 'ep': ep}
out['D3'] = d3

# ---------- exterior
def agreg(ks, t):
    L = sum(base[k][t]['L'] for k in ks); Rr = sum(base[k][t]['R'] for k in ks)
    return L, Rr, 100 * L / (L + Rr)
kz = [k for k, s in base.items() if k.startswith('ZZ|') and '1' in s and '2' in s]
kb = [k for k, s in base.items() if not k.startswith('ZZ|') and '1' in s and '2' in s]
z1, z2 = agreg(kz, '1'), agreg(kz, '2')
b1_, b2_ = agreg(kb, '1'), agreg(kb, '2')
compz = (sum(base[k]['2']['comp'] for k in kz) / sum(base[k]['1']['comp'] for k in kz) - 1) * 100
compb = (sum(base[k]['2']['comp'] for k in kb) / sum(base[k]['1']['comp'] for k in kb) - 1) * 100
# perda líquida proporcional: Flávio 2T/1T e Lula 2T/1T
out['exterior'] = {'secoes': len(kz), 'lula_1t': z1[2], 'lula_2t': z2[2], 'virada': z2[2] - z1[2],
                   'brasil_lula_1t': b1_[2], 'brasil_lula_2t': b2_[2], 'virada_brasil': b2_[2] - b1_[2],
                   'comp_var_pct_ext': compz, 'comp_var_pct_br': compb,
                   'ext_L1': z1[0], 'ext_R1': z1[1], 'ext_L2': z2[0], 'ext_R2': z2[1],
                   'ext_O1': sum(base[k]['1']['O'] for k in kz), 'ext_BN1': sum(base[k]['1']['B'] + base[k]['1']['N'] for k in kz)}
# Comparação: seções do Brasil com fatia de Lula no 1º turno e fatia de outros parecidas com as do exterior
oz = out['exterior']['ext_O1'] / sum(base[k]['1']['L'] + base[k]['1']['R'] + base[k]['1']['O'] for k in kz)
sel = []
for k in kb:
    a, b = base[k]['1'], base[k]['2']
    v1 = a['L'] + a['R'] + a['O']
    if a['L'] + a['R'] <= 0 or b['L'] + b['R'] <= 0 or v1 <= 0:
        continue
    fl = 100 * a['L'] / (a['L'] + a['R'])
    fo = a['O'] / v1
    if abs(fl - z1[2]) <= 3 and abs(fo - oz) <= 0.03:
        sel.append(k)
s1, s2 = agreg(sel, '1'), agreg(sel, '2')
out['exterior']['brasil_parecido'] = {'secoes': len(sel), 'lula_1t': s1[2], 'lula_2t': s2[2], 'virada': s2[2] - s1[2],
                                       'fatia_outros_ext': oz}
# por UF (agregado)
uf_v = {}
por = collections.defaultdict(list)
for k in kb:
    por[k.split('|')[0]].append(k)
for uf, ks in por.items():
    a1, a2 = agreg(ks, '1'), agreg(ks, '2')
    uf_v[uf] = a2[2] - a1[2]
out['exterior']['viradas_uf'] = dict(sorted(uf_v.items(), key=lambda x: x[1]))

# ---------- D4
mover = margem / 2
nsec = len(keys)
media = V2 / nsec
cen = {}
for kk in (25, media):
    p = (mover / kk) / nsec
    cen[f'{kk:.0f}'] = {'p': p, 'P640': (1 - p) ** 640, 'P500': (1 - p) ** 500, 'P706': (1 - p) ** 706}
# concentração máxima: o programa tira todos os votos de Flávio que viraram de Lula... no limite, o desvio numa seção não
# passa dos votos de Lula registrados nela. Menor número de seções que somam 2,215 milhões de votos de Lula.
Ls = np.sort(np.array([base[k]['2']['L'] for k in keys]))[::-1]
cs = np.cumsum(Ls)
N_min = int(np.searchsorted(cs, mover) + 1)
p_min = N_min / nsec
# hipergeométrica exata (amostra sem reposição) para n testadas
def p_nenhuma(Ntot, A, n):
    lp = 0.0
    for i in range(n):
        lp += math.log((Ntot - A - i) / (Ntot - i))
    return math.exp(lp)
cen['concentracao_maxima'] = {'secoes': N_min, 'p': p_min, 'votos_lula_na_ultima': int(Ls[N_min - 1]),
                              'P640_binom': (1 - p_min) ** 640, 'P640_hiper': p_nenhuma(len(bw), N_min, 640),
                              'P500_hiper': p_nenhuma(len(bw), N_min, 500), 'P706_hiper': p_nenhuma(len(bw), N_min, 706)}
# metade dos votos de Lula da seção (mais plausível que zerar Lula)
Lh = Ls / 2
ch = np.cumsum(Lh)
N_h = int(np.searchsorted(ch, mover) + 1)
cen['metade_lula_das_maiores'] = {'secoes': N_h, 'p': N_h / nsec, 'P640': (1 - N_h / nsec) ** 640}
out['D4'] = {'mover': mover, 'frac': mover / V2, 'media_por_secao': media, 'secoes_reg': nsec, 'cenarios': cen,
             'espalhado_195': 195 * mover / V2, 'espalhado_640x195': 640 * 195 * mover / V2, 'espalhado_75': 75 * mover / V2}

# ---------- S (pegada do teste): virada nas seções que votaram em urna reserva carregada no sábado, contra o local
gS = np.array([k in S for k in keys], float)
b, ep, n, G = fe(Y, gS, LOC, W)
out['S_virada_vs_local'] = {'n_S': int(gS.sum()), 'coef': b, 'ep': ep}

json.dump(out, open(saida, 'w'), ensure_ascii=False, indent=1, default=str)
for k in ('leitura', 'pais', 'D2', 'D3', 'exterior', 'D4', 'S_virada_vs_local'):
    print(k, json.dumps(out[k], ensure_ascii=False, default=str)[:1500])
print('D1', out['D1']['S'], out['D1']['por_uf'], out['D1']['vespera_mesma_urna'])
print('AL', {k: v for k, v in out['D1']['AL'].items() if k != 'lista'})
for a in out['D1']['AL']['lista']:
    print(' ', a)
if '1t' in out['D1']:
    print('1t', out['D1']['1t'])
