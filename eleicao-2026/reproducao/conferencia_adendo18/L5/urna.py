import gzip, json, sys
d = json.load(gzip.open(sys.argv[1], 'rt'))
c = json.load(gzip.open(sys.argv[2], 'rt'))['secoes']
ELIM = ['70','14','55','30','80','16','27','21','35','29']
def z(): return dict(apt=0,comp=0,L=0,R=0,O=0,B=0,N=0)
T1a, T2a = z(), z()          # todas as seções de cada turno
T1, T2 = z(), z()            # só com os dois turnos
E = {k:0 for k in ELIM}; Ea = {k:0 for k in ELIM}; n28=0; n28a=0; other=set()
ns = 0; only = []
for k, v in d.items():
    for t, acc in (('1', T1a), ('2', T2a)):
        if t in v:
            for f in acc: acc[f] += v[t][f]
    cv = c.get(k, {})
    for x in cv:
        if x not in ELIM and x not in ('13','22','28'): other.add(x)
    if '1' in v:
        for x in ELIM: Ea[x] += cv.get(x,0)
        n28a += cv.get('28',0)
    if '1' in v and '2' in v:
        ns += 1
        for f in T1: T1[f] += v['1'][f]; T2[f] += v['2'][f]
        for x in ELIM: E[x] += cv.get(x,0)
        n28 += cv.get('28',0)
    else:
        only.append((k, list(v.keys())))
print('secoes com os dois turnos', ns, 'fora', only[:5])
print('outros numeros no arquivo de candidatos', other)
for nome, A, B, EE, x28 in (('ambos', T1, T2, E, n28), ('todas', T1a, T2a, Ea, n28a)):
    el = sum(EE.values())
    print(nome, 'O1 =', A['O'], 'soma elim + 28 =', el + x28, 'soma elim', el)
    v1 = A['L'] + A['R'] + el
    print(nome, '1T valid', v1, 'F %.4f L %.4f elim %.4f' % (100*A['R']/v1, 100*A['L']/v1, 100*el/v1))
    v2 = B['L'] + B['R']
    print(nome, '2T valid', v2, 'F %.4f L %.4f' % (100*B['R']/v2, 100*B['L']/v2), 'L2', B['L'], 'R2', B['R'])
    print(nome, 'ganhos L %d F %d' % (B['L']-A['L'], B['R']-A['R']))
    bn1 = A['B'] + A['N'] + x28; bn2 = B['B'] + B['N']
    print(nome, 'queda BN', bn1-bn2, 'aumento comp', B['comp']-A['comp'], 'abst1 %.3f abst2 %.3f' % (100*(1-A['comp']/A['apt']), 100*(1-B['comp']/B['apt'])))
    print(nome, 'identidade', (B['L']-A['L'])+(B['R']-A['R']) - (el + bn1-bn2 + B['comp']-A['comp']))
json.dump({'T1':T1,'T2':T2,'E':E,'n28':n28}, open('urna_totais.json','w'))
