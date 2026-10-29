import gzip, json, sys, collections
d = json.load(gzip.open(sys.argv[1], 'rt'))
OFF = {'AC': 2, 'AM': 1, 'RO': 1, 'RR': 1, 'MT': 1, 'MS': 1}  # horas a somar ao relogio local para chegar a Brasilia (AM: maioria UTC-4)
tot = {t: collections.Counter() for t in '12'}
enc = collections.Counter()
for k, s in d.items():
    uf = k.split('|')[0]
    for t in '12':
        x = s.get(t)
        if not x: continue
        c = tot[t]; c['secoes'] += 1
        for f in ('apt', 'comp', 'L', 'R', 'O', 'B', 'N'):
            v = x.get(f)
            if isinstance(v, (int, float)): c[f] += v
        if t == '2' and x.get('enc') and uf != 'ZZ':
            hh, mm = map(int, x['enc'][-8:-3].split(':'))
            hb = hh + OFF.get(uf, 0)
            m = hb * 60 + mm
            faixa = 'ate 17:00' if m <= 17*60 else ('17:01-17:15' if m <= 17*60+15 else ('17:16-18:59' if m < 19*60 else '19:00+'))
            enc[faixa] += 1; enc['v_' + faixa] += x['L'] + x['R'] + x.get('B', 0) + x.get('N', 0)
for t in '12':
    c = tot[t]
    val = c['L'] + c['R'] + c['O']
    print(f"turno {t}: secoes {c['secoes']}, aptos {c['apt']}, comparecimento {c['comp']}, abst {100*(1-c['comp']/c['apt']):.2f}%, "
          f"L {c['L']}, R {c['R']}, O {c['O']}, B {c['B']}, N {c['N']}, validos {val}, L% {100*c['L']/val:.2f}, margem L-R {c['L']-c['R']}, total L+R+B+N {c['L']+c['R']+c['B']+c['N']+c['O']}")
print('encerramento 2t (convertido para Brasilia, sem ZZ):', dict(enc))
c = tot['2']
for v in (34300, 35000, 35500, 6000):
    print(f'{v} votos = {100*v/c["comp"]:.4f}% do comparecimento do 2t; {100*v/(c["L"]-c["R"]):.2f}% da margem')
