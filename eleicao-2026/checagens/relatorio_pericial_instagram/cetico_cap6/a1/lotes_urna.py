import json, sys, os
from datetime import datetime, timedelta, timezone
d = sys.argv[1]
BRT = timezone(timedelta(hours=-3))
casos = [
 ('resultados-2026-arquivos-transmitidos-para-totalizacao.json', '_2026_2t_', {'17h 25/10/26': datetime(2026,10,25,17,tzinfo=BRT), '19h 25/10/26': datetime(2026,10,25,19,tzinfo=BRT), '21h09 25/10/26': datetime(2026,10,25,21,9,tzinfo=BRT)}),
 ('resultados-2026-arquivos-transmitidos-para-totalizacao.json', '_2026_1t_', {'17h 04/10/26': datetime(2026,10,4,17,tzinfo=BRT)}),
 ('resultados-2022-arquivos-transmitidos-para-totalizacao.json', '_2022_2t_', {'17h 30/10/22': datetime(2022,10,30,17,tzinfo=BRT)}),
 ('resultados-2022-arquivos-transmitidos-para-totalizacao.json', '_2022_1t_', {'17h 02/10/22': datetime(2022,10,2,17,tzinfo=BRT)}),
]
for f, tag, marcos in casos:
    rs = [r for r in json.load(open(os.path.join(d, f)))['result']['resources'] if tag in r['url']]
    cr = sorted(datetime.fromisoformat(r['created']).replace(tzinfo=timezone.utc) for r in rs)
    s = f'{tag.strip("_")}: {len(rs)} arquivos (BU+imagem BU+log+RDV+assinaturas por UF); catalogados {cr[0].astimezone(BRT):%a %d/%m/%Y %H:%M}-{cr[-1].astimezone(BRT):%H:%M} BRT;'
    for k, m in marcos.items(): s += f' {(cr[0]-m).total_seconds()/3600:.1f} h desde {k};'
    print(s)
