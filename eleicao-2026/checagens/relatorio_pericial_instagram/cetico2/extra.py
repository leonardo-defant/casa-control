import gzip, json, collections
S = '/tmp/claude-0/-home-user-casa-control/ce2a8c88-e5ad-504f-8950-6f5ee14ae721/scratchpad'
OUT = S + '/relatorio_pericial/cetico2'
def ts(h):
    a, b, c = h.split(':'); return int(a)*3600+int(b)*60+int(c)
z = json.load(gzip.open(OUT + '/zips2t_secoes.json.gz', 'rt'))
z = {k: s for k, s in z.items() if len(s['enc']) >= 19}
for s in z.values():
    s['t'] = ts(s['enc'][11:]); s['nhv'] = int(s['nh']) if s['nh'].lstrip('-').isdigit() and int(s['nh']) > 0 else 0
cab = collections.defaultdict(collections.Counter)
for s in z.values(): cab[(s['uf'], s['mun'])][int(s['ab'][11:13])] += 1
off = {m: (0 if m[0] == 'ZZ' else 8 - c.most_common(1)[0][0]) for m, c in cab.items()}
for s in z.values(): s['tb'] = s['t'] + 3600*off[(s['uf'], s['mun'])]
res = {}
J3 = lambda s: s['t'] >= ts('19:00:00'); POS = lambda s: s['t'] > ts('17:00:59'); J23 = lambda s: s['t'] >= ts('17:16:00')
# NH padronizada: taxa do resto do grupo ponderada pelo comparecimento do alvo
def nh_pad(gf, alvo):
    g = collections.defaultdict(lambda: [0, 0, 0, 0])
    for k, s in z.items():
        q = g[gf(k, s)]
        if alvo(s): q[0] += s['nhv']; q[1] += s['comp']
        else: q[2] += s['nhv']; q[3] += s['comp']
    A = [0, 0]; num = 0
    for q in g.values():
        if q[1] and q[3]:
            A[0] += q[0]; A[1] += q[1]; num += q[1]*q[2]/q[3]
    return {'alvo': round(100*A[0]/A[1], 3), 'resto_padronizado': round(100*num/A[1], 3)}
UF = lambda k, s: s['uf']; MUN = lambda k, s: (s['uf'], s['mun']); LOC = lambda k, s: (s['uf'], s['mun'], k.split('|')[2], s['loc'])
res['nh_padronizado'] = {f'{an}_{gn}': nh_pad(g, a) for an, a in (('J3', J3), ('J23', J23), ('pos17', POS)) for gn, g in (('uf', UF), ('mun', MUN), ('loc', LOC))}
# diferenca de nivel 2T (depois - ate 17h00) dentro da UF, varias ponderacoes
for nome, cond in (('local', POS), ('bras', lambda s: s['tb'] > ts('17:00:59'))):
    g = collections.defaultdict(lambda: [0, 0, 0, 0])
    for s in z.values():
        q = g[s['uf']]
        if cond(s): q[0] += s['L']; q[1] += s['R']
        else: q[2] += s['L']; q[3] += s['R']
    out = {}
    for wn in ('total', 'depois', 'antes', 'harm'):
        num = den = 0
        for q in g.values():
            if q[0]+q[1] and q[2]+q[3]:
                d = 100*q[0]/(q[0]+q[1]) - 100*q[2]/(q[2]+q[3])
                a, b = q[0]+q[1], q[2]+q[3]
                w = {'total': a+b, 'depois': a, 'antes': b, 'harm': a*b/(a+b)}[wn]
                num += w*d; den += w
        out[wn] = round(num/den, 3)
    out['ufs'] = {u: round(100*q[0]/(q[0]+q[1]) - 100*q[2]/(q[2]+q[3]), 2) for u, q in g.items() if q[0]+q[1] and q[2]+q[3]}
    res['nivel_dentro_uf_' + nome] = out
# comparecimento: variacao 1T->2T por janela e dentro do municipio
b = json.load(gzip.open(S + '/trab2t/secoes2026.json.gz', 'rt'))
W = collections.defaultdict(lambda: [0, 0, 0, 0])
def jan(t):
    return 'J0' if t <= ts('17:00:59') else 'J1' if t <= ts('17:15:59') else 'J2' if t <= ts('18:59:59') else 'J3'
gm = collections.defaultdict(lambda: {'a': [0, 0, 0, 0], 'r': [0, 0, 0, 0]})
for k, s in z.items():
    t1 = b.get(k, {}).get('1')
    if not t1 or not t1.get('apt') or not s['apt']: continue
    for key in (jan(s['t']), 'tudo'):
        q = W[key]; q[0] += t1['comp']; q[1] += t1['apt']; q[2] += s['comp']; q[3] += s['apt']
    q = gm[(s['uf'], s['mun'])]['a' if J3(s) else 'r']; q[0] += t1['comp']; q[1] += t1['apt']; q[2] += s['comp']; q[3] += s['apt']
res['comparecimento_1t_2t_por_janela'] = {k: {'1t': round(100*q[0]/q[1], 3), '2t': round(100*q[2]/q[3], 3), 'var_pts': round(100*(q[2]/q[3]-q[0]/q[1]), 3), 'comp_2t_menos_1t': q[2]-q[0]} for k, q in sorted(W.items())}
num = den = 0
for v in gm.values():
    a, r = v['a'], v['r']
    if a[1] and r[1]:
        da = a[2]/a[3]-a[0]/a[1]; dr = r[2]/r[3]-r[0]/r[1]; num += a[3]*(da-dr); den += a[3]
res['comparecimento_J3_menos_resto_mun_pts'] = round(100*num/den, 3)
# amostra de logs: composicao por janela e UF
lg = json.load(open(S + '/todos_logs/amostra/T3_logs.json'))['2']
cj = collections.Counter(); cu = collections.Counter(); pu = collections.Counter(s['uf'] for s in z.values())
for k in lg:
    if k in z: cj[jan(z[k]['t'])] += 1; cu[z[k]['uf']] += 1
    else: cj['fora'] += 1
n = sum(cj.values())
pop = collections.Counter(jan(s['t']) for s in z.values())
res['amostra_logs_por_janela'] = {j: {'amostra': cj[j], 'esperado_se_aleatoria': round(n*pop[j]/len(z), 1)} for j in ('J0', 'J1', 'J2', 'J3')}
res['amostra_logs_por_uf'] = {u: [cu[u], round(n*pu[u]/len(z), 1)] for u in sorted(pu)}
res['amostra_logs_municipios'] = len({tuple(k.split('|')[:2]) for k in lg})
# J3 da amostra: votos e horarios
res['amostra_J3'] = [(k, lg[k].get('computados'), lg[k].get('ultimo_voto'), lg[k].get('encerramento'), z[k]['enc'], {kk: vv for kk, vv in lg[k].items() if kk.startswith('A')}) for k in lg if k in z and J3(z[k])]
# Noronha
res['noronha'] = sorted((k, s['ab'][11:], s['enc'][11:]) for k, s in z.items() if s['nmun'].startswith('FERNANDO DE NORONHA'))
# ocidentais no J0 local: quantas fecharam no minuto 17:00 de Brasilia
w = collections.Counter()
for s in z.values():
    if s['uf'] != 'ZZ' and off[(s['uf'], s['mun'])] > 0 and s['t'] <= ts('17:00:59'):
        w[jan(s['tb'])] += 1
res['ocidentais_J0local_por_janela_brasilia'] = w
json.dump(res, open(OUT + '/extra.json', 'w'), ensure_ascii=False, indent=1, default=str)
for k, v in res.items():
    if k in ('amostra_logs_por_uf',): continue
    print(k, json.dumps(v, ensure_ascii=False, default=str)[:1500])
print('amostra_logs_por_uf', {u: v for u, v in res['amostra_logs_por_uf'].items() if u in ('RJ','SP','BA','PE','PB','MG','RS','AC','MT')})
