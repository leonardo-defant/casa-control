import json, sys, os
from datetime import datetime, timedelta
d = sys.argv[1]
BRT = timedelta(hours=-3)
casos = [  # (ano, turno, arquivo, data do pleito, tag)
    ('2026', '2t', 'pkg2026.json', datetime(2026, 10, 25, 17, 0), 'bweb_2t'),
    ('2026', '1t', 'pkg2026.json', datetime(2026, 10, 4, 17, 0), 'bweb_1t'),
    ('2022', '2t', 'pkg2022.json', datetime(2022, 10, 30, 17, 0), 'bweb_2t'),
    ('2022', '1t', 'pkg2022.json', datetime(2022, 10, 2, 17, 0), 'bweb_1t'),
]
for ano, t, arq, fim, tag in casos:
    j = json.load(open(os.path.join(d, arq)))
    rs = [r for r in j['result']['resources'] if tag in r['url']]
    cs = sorted(datetime.fromisoformat(r['created']) for r in rs)
    ini, ult = cs[0] + BRT, cs[-1] + BRT
    nome = sorted(set(r['url'].split('/')[-1].split('_')[-1].split('.')[0] for r in rs))
    h = (ini - fim).total_seconds() / 3600
    print(f'{ano} {t}: {len(rs)} recursos; catalogados de {ini:%a %d/%m/%Y %H:%M} a {ult:%H:%M} (Brasília); '
          f'{h:.1f} h depois das 17h do dia da eleição; carimbo no nome do arquivo {nome}')
proc = datetime(2026, 10, 25, 21, 9)
ini26 = min(datetime.fromisoformat(r['created']) for r in json.load(open(os.path.join(d, 'pkg2026.json')))['result']['resources'] if 'bweb_2t' in r['url']) + BRT
print(f'2026 2t: da confirmação do TSE (21h09 de 25/10, segundo O Globo) à catalogação: {(ini26 - proc).total_seconds()/3600:.1f} h')
print(f'2026 2t: das 19h de 25/10 (fim da prorrogação) à catalogação: {(ini26 - datetime(2026,10,25,19,0)).total_seconds()/3600:.1f} h')
print(f'Relatório: 72 h; "manhã de quarta-feira, 28/10". Até 08h de 28/10 seriam {(datetime(2026,10,28,8,0)-proc).total_seconds()/3600:.1f} h desde 21h09')
