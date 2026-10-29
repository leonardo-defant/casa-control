import json, sys, os, collections
raiz = sys.argv[1]
dg = collections.Counter(); dr = collections.Counter(); n = 0; err = 0
dgmax = None; drmax = None; dgmin=None
from datetime import datetime
for d, _, fs in os.walk(raiz):
    for f in fs:
        if not f.endswith('aux.json'): continue
        try:
            j = json.load(open(os.path.join(d, f), encoding='utf-8'))
        except Exception:
            err += 1; continue
        n += 1
        t = datetime.strptime(j['dg'] + ' ' + j['hg'], '%d/%m/%Y %H:%M:%S')
        dg[t.strftime('%d/%m %H')] += 1
        dgmax = t if dgmax is None or t > dgmax else dgmax
        dgmin = t if dgmin is None or t < dgmin else dgmin
        for h in j.get('hashes', []):
            r = datetime.strptime(h['dr'] + ' ' + h['hr'], '%d/%m/%Y %H:%M:%S')
            dr[r.strftime('%d/%m %H')] += 1
            drmax = r if drmax is None or r > drmax else drmax
print('aux lidos', n, 'erros', err)
print('geracao do aux (dg/hg): min', dgmin, 'max', dgmax)
print('recebimento (dr/hr) max', drmax)
print('dg por hora:', sorted(dg.items()))
print('dr por hora:', sorted(dr.items()))
