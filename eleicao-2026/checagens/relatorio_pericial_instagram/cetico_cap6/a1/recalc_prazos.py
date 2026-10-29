import json, sys, os, collections
from datetime import datetime, timedelta, timezone
d = sys.argv[1]
BRT = timezone(timedelta(hours=-3))
def load(f): return json.load(open(os.path.join(d, f)))['result']['resources']
for ano, f, tag, marcos in [
    ('2026', 'pkg2026.json', 'bweb_2t', {'17h 25/10': datetime(2026,10,25,17,0,tzinfo=BRT), '19h 25/10': datetime(2026,10,25,19,0,tzinfo=BRT), '21h09 25/10': datetime(2026,10,25,21,9,tzinfo=BRT)}),
    ('2026', 'pkg2026.json', 'bweb_1t', {'17h 04/10': datetime(2026,10,4,17,0,tzinfo=BRT)}),
    ('2022', 'pkg2022.json', 'bweb_2t', {'17h 30/10/22': datetime(2022,10,30,17,0,tzinfo=BRT)}),
    ('2022', 'pkg2022.json', 'bweb_1t', {'17h 02/10/22': datetime(2022,10,2,17,0,tzinfo=BRT)}),
]:
    rs = [r for r in load(f) if tag in r['url'] or tag in r['name'].lower() or (tag.endswith('2t') and 'Segundo turno' in r['name']) or (tag.endswith('1t') and 'Primeiro turno' in r['name'])]
    urls = [r['url'].split('/')[-1] for r in rs]
    zips = [u for u in urls if u.endswith('.zip')]
    shas = [u for u in urls if u.endswith('.sha512')]
    ufs = sorted(set(u.split('_')[2] for u in urls))
    names_bu = [r['name'] for r in rs if 'Boletim de Urna' in r['name']]
    cr = sorted(datetime.fromisoformat(r['created']) for r in rs)
    print(f'{ano} {tag}: recursos {len(rs)}, urls .zip {len(zips)}, urls .sha512 {len(shas)}, UFs distintas {len(ufs)} {ufs}, recursos nomeados BU {len(names_bu)}')
    for interp, tz in [('created=UTC', timezone.utc), ('created=BRT', BRT)]:
        a = cr[0].replace(tzinfo=tz); b = cr[-1].replace(tzinfo=tz)
        s = f'  {interp}: {a.astimezone(BRT):%a %d/%m/%Y %H:%M}-{b.astimezone(BRT):%H:%M} BRT;'
        for k, m in marcos.items():
            s += f' desde {k}: {(a-m).total_seconds()/3600:.1f} h;'
        print(s)
