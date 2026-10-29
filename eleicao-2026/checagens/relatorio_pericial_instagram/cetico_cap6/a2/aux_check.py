import json, sys, os, collections
from datetime import datetime, timezone
raiz = sys.argv[1]
n=0; dgs=[]; drs=[]; mt=[]; keys=collections.Counter(); sem_bu=0; tipos=collections.Counter()
ex=None
for d, _, fs in os.walk(raiz):
    for f in fs:
        p=os.path.join(d,f)
        mt.append((os.stat(p).st_mtime, f.split('-')[-1]))
    if 'aux.json' in fs:
        j=json.load(open(os.path.join(d,'aux.json'),encoding='utf-8'))
        if ex is None: ex=j
        n+=1
        keys.update(j.keys())
        dgs.append(datetime.strptime(j['dg']+' '+j['hg'],'%d/%m/%Y %H:%M:%S'))
        for h in j.get('hashes',[]):
            drs.append(datetime.strptime(h['dr']+' '+h['hr'],'%d/%m/%Y %H:%M:%S'))
            pass
        if not any(x.endswith('bu.dat') for x in fs): sem_bu+=1
print('aux', n, 'sem bu.dat', sem_bu)
print('chaves aux', dict(keys))
print('exemplo aux', json.dumps(ex, ensure_ascii=False)[:800])
print('dg min/max', min(dgs), max(dgs))
print('dr min/max', min(drs), max(drs))
c=collections.Counter(x.strftime('%d/%m %H') for x in drs); print('dr por hora', sorted(c.items()))
mt.sort()
print('mtime mais antigo (UTC):', datetime.fromtimestamp(mt[0][0], timezone.utc), mt[0][1])
for suf in ['bu.dat','log.jez','rdv.dat','vota.vsc','aux.json']:
    m=[t for t,s in mt if s==suf]
    if m: print(suf, len(m), 'mtime min', datetime.fromtimestamp(min(m),timezone.utc), 'max', datetime.fromtimestamp(max(m),timezone.utc))
