"""Conferencia independente: janelas de encerramento, fuso, contrafactuais, biometria. Le cada base uma vez."""
import gzip, json, sys, collections, math
S = '/tmp/claude-0/-home-user-casa-control/ce2a8c88-e5ad-504f-8950-6f5ee14ae721/scratchpad'
OUT = S + '/relatorio_pericial/cetico2'
res = {}

def ts(hms):
    h, m, s = hms.split(':'); return int(h)*3600 + int(m)*60 + int(s)

def janela(t):
    if t <= ts('17:00:59'): return 'J0'
    if t <= ts('17:15:59'): return 'J1'
    if t <= ts('18:59:59'): return 'J2'
    return 'J3'

def agg():
    return {'n': 0, 'comp': 0, 'apt': 0, 'L': 0, 'R': 0, 'O': 0, 'nh': 0}

def add(a, s, nh=0):
    a['n'] += 1; a['comp'] += s['comp']; a['apt'] += s.get('apt', 0); a['L'] += s['L']; a['R'] += s['R']; a['O'] += s.get('O', 0); a['nh'] += nh

def fin(a):
    v = a['L'] + a['R'] + a['O']
    o = dict(a)
    o['pctL_validos'] = round(100*a['L']/v, 3) if v else None
    o['pctR_validos'] = round(100*a['R']/v, 3) if v else None
    o['pctL_2cand'] = round(100*a['L']/(a['L']+a['R']), 3) if a['L']+a['R'] else None
    o['frente_L'] = a['L'] - a['R']
    if a['nh']: o['taxa_nh'] = round(100*a['nh']/a['comp'], 3)
    return o

def offsets(base, turno):
    """deslocamento em horas (local + d = Brasilia) pela hora de abertura mais comum em cada municipio."""
    c = collections.defaultdict(collections.Counter)
    for k, s in base.items():
        t = s.get(turno)
        if not t or not t.get('ab'): continue
        uf, mun = k.split('|')[:2]
        c[(uf, mun)][int(t['ab'][:2])] += 1
    off = {}
    for m, cc in c.items():
        h = cc.most_common(1)[0][0]
        off[m] = 0 if m[0] == 'ZZ' else 8 - h
    return off

# ---------------- 2026 2T dos zips (independente) -----------------
z = json.load(gzip.open(OUT + '/zips2t_secoes.json.gz', 'rt'))
semenc = {k: s for k, s in z.items() if len(s['enc']) < 19}
res['z_sem_encerramento'] = {'n': len(semenc), 'comp': sum(s['comp'] for s in semenc.values()), 'frente_L': sum(s['L']-s['R'] for s in semenc.values()), 'ufs': collections.Counter(s['uf'] for s in semenc.values())}
z = {k: s for k, s in z.items() if len(s['enc']) >= 19}
datas = collections.Counter(s['enc'][:10] for s in z.values())
res['z_datas_enc'] = datas
res['z_total'] = {'secoes': len(z), 'comp': sum(s['comp'] for s in z.values()), 'L': sum(s['L'] for s in z.values()), 'R': sum(s['R'] for s in z.values()),
                  'nh_soma': sum(int(s['nh']) for s in z.values() if s['nh'].lstrip('-').isdigit() and int(s['nh']) > 0),
                  'nh_nulo': sum(1 for s in z.values() if not s['nh'].lstrip('-').isdigit()),
                  'nh_neg': sum(1 for s in z.values() if s['nh'].lstrip('-').isdigit() and int(s['nh']) < 0)}
for s in z.values():
    s['t'] = ts(s['enc'][11:]) + (86400 if s['enc'][:10] > '2026-10-25' else 0)
    s['tab'] = ts(s['ab'][11:])
    s['nhv'] = int(s['nh']) if s['nh'].lstrip('-').isdigit() and int(s['nh']) > 0 else 0
# deslocamento 2T
cab = collections.defaultdict(collections.Counter)
for s in z.values(): cab[(s['uf'], s['mun'])][int(s['ab'][11:13])] += 1
off2 = {}
for m, cc in cab.items(): off2[m] = 0 if m[0] == 'ZZ' else 8 - cc.most_common(1)[0][0]
res['offsets_2t_contagem'] = collections.Counter(off2.values())
res['offsets_2t_por_uf'] = {}
for (uf, mun), o in off2.items():
    if o != 0: res['offsets_2t_por_uf'].setdefault(f'{uf}:{o}', []).append(mun)
res['offsets_2t_por_uf'] = {k: len(v) for k, v in res['offsets_2t_por_uf'].items()}
# municipios com mistura de horas de abertura (possivel erro de deslocamento)
mist = []
for m, cc in cab.items():
    tot = sum(cc.values()); top = cc.most_common(1)[0][1]
    if tot - top > 0.2*tot: mist.append((m, dict(cc)))
res['mun_abertura_misturada'] = mist[:30]; res['n_mun_abertura_misturada'] = len(mist)
for s in z.values(): s['tb'] = s['t'] + 3600*off2[(s['uf'], s['mun'])]

# janelas local e Brasilia
W = collections.defaultdict(agg); WB = collections.defaultdict(agg)
for s in z.values():
    add(W[janela(s['t'])], s, s['nhv']); add(WB[janela(s['tb'])], s, s['nhv'])
    add(W['tudo'], s, s['nhv'])
    add(W['depois_17h00m59' if s['t'] > ts('17:00:59') else 'ate_17h00m59'], s, s['nhv'])
    add(WB['depois_17h00m59' if s['tb'] > ts('17:00:59') else 'ate_17h00m59'], s, s['nhv'])
    add(WB['antes_17h00m00' if s['tb'] < ts('17:00:00') else 'desde_17h00m00'], s)
    add(WB['ate_17h02m59' if s['tb'] <= ts('17:02:59') else 'depois_17h02m59'], s)
    add(WB['ate_17h48m59' if s['tb'] <= ts('17:48:59') else 'depois_17h48m59'], s)
    add(WB['ate_17h00m59_semZZ' if (s['tb'] <= ts('17:00:59') and s['uf'] != 'ZZ') else 'x'], s)
    if ts('17:01:00') <= s['tb'] <= ts('17:02:59'): add(WB['17h01_17h02m59'], s)
    if s['t'] >= ts('19:00:00') and s['t'] <= ts('19:59:59'): add(W['hora19'], s)
    if s['t'] >= ts('20:00:00'): add(W['20h_ou_mais'], s)
    if s['uf'] == 'ZZ': add(W['ZZ'], s)
res['2026_2t_local'] = {k: fin(v) for k, v in sorted(W.items())}
res['2026_2t_brasilia'] = {k: fin(v) for k, v in sorted(WB.items()) if k != 'x'}
# composicao do J0 local: secoes com deslocamento != 0
comp0 = collections.defaultdict(agg)
for s in z.values():
    if janela(s['t']) == 'J0':
        o = off2[(s['uf'], s['mun'])]
        add(comp0['ZZ' if s['uf'] == 'ZZ' else f'desloc{o}'], s)
res['2026_2t_J0_local_composicao'] = {k: fin(v) for k, v in comp0.items()}
# minutos Brasilia
mins = collections.Counter(); minsL = collections.Counter()
for s in z.values():
    if s['uf'] == 'ZZ': continue
    if ts('17:00:00') <= s['tb'] < ts('17:16:00'): mins[(s['tb']-ts('17:00:00'))//60] += 1
res['2026_2t_brasilia_por_minuto_semZZ'] = dict(sorted(mins.items()))
mins2 = collections.Counter()
for s in z.values():
    if ts('17:00:00') <= s['tb'] < ts('17:16:00'): mins2[(s['tb']-ts('17:00:00'))//60] += 1
res['2026_2t_brasilia_por_minuto_comZZ'] = dict(sorted(mins2.items()))
res['2026_2t_brasilia_min_tb'] = min(s['tb'] for s in z.values() if s['uf'] != 'ZZ')
res['2026_2t_brasilia_antes17_semZZ'] = sum(1 for s in z.values() if s['uf'] != 'ZZ' and s['tb'] < ts('17:00:00'))
# horas >= 20
res['2026_2t_20h_ou_mais'] = sorted([(k, s['nmun'], s['enc'], s['comp']) for k, s in z.items() if s['t'] >= ts('20:00:00')])
# J3 por UF (>=19h e hora 19)
U = collections.defaultdict(agg); U19 = collections.defaultdict(agg); UT = collections.defaultdict(agg)
for k, s in z.items():
    add(UT[s['uf']], s)
    if s['t'] >= ts('19:00:00'): add(U[s['uf']], s)
    if ts('19:00:00') <= s['t'] <= ts('19:59:59'): add(U19[s['uf']], s)
res['2026_2t_J3_por_uf'] = {k: fin(v) for k, v in sorted(U.items(), key=lambda x: -x[1]['n'])}
res['2026_2t_hora19_por_uf'] = {k: fin(v) for k, v in sorted(U19.items(), key=lambda x: -x[1]['n'])}
res['2026_2t_uf_total'] = {k: fin(v) for k, v in UT.items()}
# J3 por municipio (top) e capital x resto
M3 = collections.defaultdict(agg); MR = collections.defaultdict(agg)
for k, s in z.items():
    m = (s['uf'], s['mun'], s['nmun'])
    if s['t'] >= ts('19:00:00'): add(M3[m], s)
    else: add(MR[m], s)
res['2026_2t_J3_municipios_top'] = [(f'{m[0]} {m[2]}', fin(M3[m]), fin(MR[m])) for m in sorted(M3, key=lambda m: -M3[m]['n'])[:12]]

# ---------------- base 2026 (1T e 2T) -----------------
b = json.load(gzip.open(S + '/trab2t/secoes2026.json.gz', 'rt'))
# conferir base 2T contra zips
dif = 0; falta = 0
for k, s in z.items():
    t = b.get(k, {}).get('2')
    if not t: falta += 1; continue
    if (t['L'], t['R'], t['comp'], t['enc']) != (s['L'], s['R'], s['comp'], s['enc'][11:]): dif += 1
res['base_vs_zips_2t'] = {'faltam_na_base': falta, 'divergentes': dif, 'so_na_base': [k for k in b if k not in z][:5]}
# 1T: janelas local
off1 = offsets(b, '1')
W1 = collections.defaultdict(agg); W1B = collections.defaultdict(agg)
for k, x in b.items():
    t = x.get('1')
    if not t or not t.get('enc'): continue
    tl = ts(t['enc']); uf, mun = k.split('|')[:2]
    tb = tl + 3600*off1[(uf, mun)]
    add(W1[janela(tl)], t); add(W1B[janela(tb)], t); add(W1['tudo'], t)
    add(W1['ate_17h00m59' if tl <= ts('17:00:59') else 'depois_17h00m59'], t)
    add(W1B['ate_17h00m59' if tb <= ts('17:00:59') else 'depois_17h00m59'], t)
    if tl >= ts('17:16:00'): add(W1['J2J3'], t)
res['2026_1t_local'] = {k: fin(v) for k, v in sorted(W1.items())}
res['2026_1t_brasilia'] = {k: fin(v) for k, v in sorted(W1B.items())}
U1 = collections.defaultdict(agg)
for k, x in b.items():
    t = x.get('1')
    if t and t.get('enc') and ts(t['enc']) >= ts('19:00:00'): add(U1[k.split('|')[0]], t)
res['2026_1t_J3_por_uf'] = {k: fin(v) for k, v in U1.items() if k in ('BA', 'PE', 'MA', 'SP', 'RJ', 'PB')}

# mesmas secoes: variacao 1T->2T por janela 2T local
def sw(a):  # a: L1,R1,L2,R2
    return 100*(a[2]/(a[2]+a[3]) - a[0]/(a[0]+a[1]))
SW = collections.defaultdict(lambda: [0, 0, 0, 0]); SWB = collections.defaultdict(lambda: [0, 0, 0, 0])
pares = []
for k, s in z.items():
    t1 = b.get(k, {}).get('1')
    if not t1 or t1['L'] + t1['R'] == 0 or s['L'] + s['R'] == 0: continue
    j = janela(s['t'])
    for key in (j, 'tudo'):
        a = SW[key]; a[0] += t1['L']; a[1] += t1['R']; a[2] += s['L']; a[3] += s['R']
    a = SWB[janela(s['tb'])]; a[0] += t1['L']; a[1] += t1['R']; a[2] += s['L']; a[3] += s['R']
    pares.append((k, s, t1))
res['swing_por_janela_local'] = {k: round(sw(v), 3) for k, v in sorted(SW.items())}
res['swing_por_janela_brasilia'] = {k: round(sw(v), 3) for k, v in sorted(SWB.items())}
res['nivel_1t_2cand_por_janela_local'] = {k: round(100*v[0]/(v[0]+v[1]), 3) for k, v in sorted(SW.items())}
# swing dentro do municipio e do local: J3 x resto
def dentro(chave_fn, alvo):
    g = collections.defaultdict(lambda: {'a': [0, 0, 0, 0], 'r': [0, 0, 0, 0]})
    for k, s, t1 in pares:
        q = g[chave_fn(k, s)]['a' if alvo(s) else 'r']
        q[0] += t1['L']; q[1] += t1['R']; q[2] += s['L']; q[3] += s['R']
    num = den = 0; ng = 0
    for v in g.values():
        if v['a'][2]+v['a'][3] > 0 and v['r'][2]+v['r'][3] > 0:
            wgt = v['a'][2] + v['a'][3]
            num += wgt*(sw(v['a']) - sw(v['r'])); den += wgt; ng += 1
    return {'grupos': ng, 'dif_swing_ponderada': round(num/den, 3) if den else None}
isJ3 = lambda s: s['t'] >= ts('19:00:00')
isJ23 = lambda s: s['t'] >= ts('17:16:00')
isPos = lambda s: s['t'] > ts('17:00:59')
res['swing_dentro'] = {
    'J3_mun': dentro(lambda k, s: (s['uf'], s['mun']), isJ3),
    'J3_local': dentro(lambda k, s: (s['uf'], s['mun'], k.split('|')[2], s['loc']), isJ3),
    'J23_mun': dentro(lambda k, s: (s['uf'], s['mun']), isJ23),
    'pos17_mun_local': dentro(lambda k, s: (s['uf'], s['mun']), isPos),
    'pos17_uf_local': dentro(lambda k, s: s['uf'], isPos),
}
# diferenca de nivel 2T entre depois e ate 17h00 dentro da UF (relogio local)
def nivel_dentro(chave_fn, alvo, peso_alvo=True):
    g = collections.defaultdict(lambda: {'a': [0, 0], 'r': [0, 0]})
    for k, s in z.items():
        q = g[chave_fn(k, s)]['a' if alvo(s) else 'r']; q[0] += s['L']; q[1] += s['R']
    num = den = 0
    for v in g.values():
        if sum(v['a']) and sum(v['r']):
            wgt = sum(v['a']) + sum(v['r'])
            num += wgt*(100*v['a'][0]/sum(v['a']) - 100*v['r'][0]/sum(v['r'])); den += wgt
    return round(num/den, 3)
res['nivel_2t_pos17_menos_ate17_dentro_uf'] = nivel_dentro(lambda k, s: s['uf'], isPos)
res['nivel_2t_pos17_menos_ate17_dentro_uf_brasilia'] = nivel_dentro(lambda k, s: s['uf'], lambda s: s['tb'] > ts('17:00:59'))
res['nivel_2t_pos17_menos_ate17_dentro_mun'] = nivel_dentro(lambda k, s: (s['uf'], s['mun']), isPos)
# fatia J0 por UF (local)
fat = collections.defaultdict(lambda: [0, 0]); fatB = collections.defaultdict(lambda: [0, 0])
for s in z.values():
    fat[s['uf']][1] += 1; fatB[s['uf']][1] += 1
    if janela(s['t']) == 'J0': fat[s['uf']][0] += 1
    if janela(s['tb']) == 'J0': fatB[s['uf']][0] += 1
res['fatia_J0_por_uf_local'] = {k: round(100*v[0]/v[1], 1) for k, v in sorted(fat.items())}
res['fatia_J0_por_uf_brasilia'] = {k: round(100*v[0]/v[1], 1) for k, v in sorted(fatB.items())}
# contrafactuais
tot = W['tudo']; lead = tot['L'] - tot['R']
j23 = [ (s, t1) for k, s, t1 in pares if isJ23(s)]
lead23 = sum(s['L'] - s['R'] for s in z.values() if isJ23(s))
cf = 0
for s, t1 in j23:
    v2 = s['L'] + s['R']; sh = t1['L']/(t1['L']+t1['R'])
    cf += sh*v2 - (1-sh)*v2
n23 = sum(1 for s in z.values() if isJ23(s))
res['contrafactual'] = {'frente_total': lead, 'n_J23': n23, 'n_J23_com_1t': len(j23), 'frente_J23': lead23, 'sem_J23': lead - lead23,
                        'J23_revertidas_ao_1t': round(lead - lead23 + cf), 'J23_sem_par_1t_mantidas_como_2t': sum(s['L']-s['R'] for k, s in z.items() if isJ23(s) and not (b.get(k, {}).get('1')))}
# todas as secoes depois de 17:02:59 Brasilia revertidas ao 1T
cf2 = 0; base_lead = 0
for k, s, t1 in pares:
    v2 = s['L'] + s['R']; sh = t1['L']/(t1['L']+t1['R'])
    if s['tb'] > ts('17:02:59'): cf2 += (2*sh - 1)*v2
    else: base_lead += s['L'] - s['R']
res['contrafactual']['pos_17h02m59_brasilia_revertidas_ao_1t'] = round(base_lead + cf2)
# cruzamento janela 1T x 2T para J3 2T
cx = collections.Counter()
for k, s in z.items():
    if isJ3(s):
        t1 = b.get(k, {}).get('1')
        cx[janela(ts(t1['enc'])) if t1 and t1.get('enc') else 'sem1t'] += 1
res['cruzamento_J3_2t_janela_1t'] = cx
# recebimento do BU para hora 19
rb = collections.Counter(); em = collections.Counter()
for s in z.values():
    if ts('19:00:00') <= s['t'] <= ts('19:59:59'):
        em[s['emi'][11:13]] += 1; rb[s['rec'][11:13]] += 1
res['hora19_emissao_hora'] = em; res['hora19_recebimento_hora'] = rb

# ---------------- biometria -----------------
nhw = {k: v.get('taxa_nh') for k, v in res['2026_2t_local'].items()}
res['nh_por_janela_local'] = nhw
res['nh_por_janela_brasilia'] = {k: v.get('taxa_nh') for k, v in res['2026_2t_brasilia'].items()}
def nh_dentro(chave_fn, alvo):
    g = collections.defaultdict(lambda: {'a': [0, 0], 'r': [0, 0]})
    for k, s in z.items():
        q = g[chave_fn(k, s)]['a' if alvo(s) else 'r']; q[0] += s['nhv']; q[1] += s['comp']
    A = [0, 0]; R = [0, 0]
    for v in g.values():
        if v['a'][1] and v['r'][1]:
            A[0] += v['a'][0]; A[1] += v['a'][1]; R[0] += v['r'][0]; R[1] += v['r'][1]
    return {'alvo': round(100*A[0]/A[1], 3), 'resto_mesmos_grupos': round(100*R[0]/R[1], 3)}
res['nh_dentro'] = {
    'J3_uf': nh_dentro(lambda k, s: s['uf'], isJ3), 'J3_mun': nh_dentro(lambda k, s: (s['uf'], s['mun']), isJ3),
    'J3_local': nh_dentro(lambda k, s: (s['uf'], s['mun'], k.split('|')[2], s['loc']), isJ3),
    'pos17_local_uf': nh_dentro(lambda k, s: s['uf'], isPos), 'pos17_local_mun': nh_dentro(lambda k, s: (s['uf'], s['mun']), isPos),
    'pos17_bras_uf': nh_dentro(lambda k, s: s['uf'], lambda s: s['tb'] > ts('17:00:59')),
    'pos17_bras_mun': nh_dentro(lambda k, s: (s['uf'], s['mun']), lambda s: s['tb'] > ts('17:00:59')),
    'J23_mun': nh_dentro(lambda k, s: (s['uf'], s['mun']), isJ23),
}
def corr(chave_fn, alvo):
    g = collections.defaultdict(lambda: [0, 0, 0, 0])  # nh, comp, comp_alvo
    for k, s in z.items():
        q = g[chave_fn(k, s)]; q[0] += s['nhv']; q[1] += s['comp']
        if alvo(s): q[2] += s['comp']
    xs = []; 
    for v in g.values():
        if v[1] > 0: xs.append((v[0]/v[1], v[2]/v[1], v[1]))
    W_ = sum(w for _, _, w in xs); mx = sum(x*w for x, _, w in xs)/W_; my = sum(y*w for _, y, w in xs)/W_
    cxy = sum(w*(x-mx)*(y-my) for x, y, w in xs); cxx = sum(w*(x-mx)**2 for x, y, w in xs); cyy = sum(w*(y-my)**2 for x, y, w in xs)
    return {'n': len(xs), 'r_ponderado': round(cxy/math.sqrt(cxx*cyy), 3)}
zona = lambda k, s: (s['uf'], k.split('|')[2]); munf = lambda k, s: (s['uf'], s['mun'])
res['corr_nh'] = {'zona_J23': corr(zona, isJ23), 'mun_J23': corr(munf, isJ23), 'zona_pos17_local': corr(zona, isPos), 'mun_pos17_local': corr(munf, isPos),
                  'zona_pos17_bras': corr(zona, lambda s: s['tb'] > ts('17:00:59')), 'mun_pos17_bras': corr(munf, lambda s: s['tb'] > ts('17:00:59')),
                  'zona_J3': corr(zona, isJ3)}
del b

# ---------------- 2022 -----------------
d = json.load(gzip.open(S + '/dados2t/secoes2022.json.gz', 'rt'))
o22 = offsets(d, '2'); o221 = offsets(d, '1')
W2 = collections.defaultdict(agg); W2B = collections.defaultdict(agg); mm = collections.Counter(); W21 = collections.defaultdict(agg)
for k, x in d.items():
    uf, mun = k.split('|')[:2]
    t = x.get('2')
    if t and t.get('enc'):
        tl = ts(t['enc']); tb = tl + 3600*o22[(uf, mun)]
        add(W2[janela(tl)], t); add(W2['tudo'], t); add(W2B[janela(tb)], t)
        add(W2['ate_17h00m59' if tl <= ts('17:00:59') else 'depois_17h00m59'], t)
        add(W2B['ate_17h00m59' if tb <= ts('17:00:59') else 'depois_17h00m59'], t)
        if tl >= ts('17:16:00'): add(W2['J2J3'], t)
        if uf != 'ZZ' and ts('17:00:00') <= tb < ts('17:04:00'): mm[(tb - ts('17:00:00'))//60] += 1
    t = x.get('1')
    if t and t.get('enc'):
        tl = ts(t['enc'])
        add(W21[janela(tl)], t)
        if tl >= ts('17:16:00'): add(W21['J2J3'], t)
res['2022_2t_local'] = {k: fin(v) for k, v in sorted(W2.items())}
res['2022_2t_brasilia'] = {k: fin(v) for k, v in sorted(W2B.items())}
res['2022_2t_brasilia_por_minuto_semZZ'] = dict(sorted(mm.items()))
res['2022_1t_local'] = {k: fin(v) for k, v in sorted(W21.items())}
SW2 = collections.defaultdict(lambda: [0, 0, 0, 0])
for k, x in d.items():
    t1, t2 = x.get('1'), x.get('2')
    if not t1 or not t2 or not t2.get('enc') or t1['L']+t1['R'] == 0 or t2['L']+t2['R'] == 0: continue
    a = SW2[janela(ts(t2['enc']))]; a[0] += t1['L']; a[1] += t1['R']; a[2] += t2['L']; a[3] += t2['R']
res['2022_swing_por_janela_local'] = {k: round(sw(v), 3) for k, v in sorted(SW2.items())}
del d
# ---------------- 2018 -----------------
d = json.load(gzip.open(S + '/dados2t/secoes2018.json.gz', 'rt'))
W8 = collections.defaultdict(agg)
res['2018_sem_enc'] = sum(1 for x in d.values() if x.get('2') and not (x['2'].get('enc') and x['2']['enc'].count(':') == 2))
for k, x in d.items():
    t = x.get('2')
    if t and t.get('enc') and t['enc'].count(':') == 2:
        add(W8[janela(ts(t['enc']))], t); add(W8['tudo'], t)
res['2018_2t_local'] = {k: fin(v) for k, v in sorted(W8.items())}
del d
json.dump(res, open(OUT + '/resultado_cetico2.json', 'w'), ensure_ascii=False, indent=1, default=str)
print('ok')
