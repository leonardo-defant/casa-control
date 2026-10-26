"""Soma dos boletins contra o total oficial (Brasil e por UF), critério 1 da seção 7.
Uso: python3 -I somar_oficial.py <secoes.json.gz> <turno 1|2>
Consulta os arquivos oficiais no site de resultados do TSE (Brasil e 27 UFs mais exterior).
"""
import collections, json, os, ssl, sys, time, urllib.request
from lib import carregar
CTX = ssl.create_default_context(cafile='/root/.ccr/ca-bundle.crt')
ELE = {'1': '6257', '2': '6258'}


def oficial(uf, ele):
    u = f'https://resultados.tse.jus.br/oficial/ele2026/{ele}/dados/{uf}/{uf}-c0001-e{int(ele):06d}-u.json'
    with urllib.request.urlopen(u, timeout=60, context=CTX) as r:
        d = json.load(r)
    c = {x['n']: int(x['vap']) for a in d['carg'][0]['agr'] for p in a['par'] for x in p['cand']}
    return {'L': c.get('13', 0), 'R': c.get('22', 0), 'B': int(d['v']['vb']), 'N': int(d['v']['tvn']), 'comp': int(d['e']['c']),
            'secoes_tot': int(d['s']['st']), 'hora': d.get('hg')}


d = carregar(sys.argv[1]); t = sys.argv[2]
soma = collections.defaultdict(collections.Counter)
for k, v in d.items():
    if t not in v: continue
    uf = k.split('|')[0]
    for c in ('L', 'R', 'B', 'N', 'comp'):
        soma[uf][c] += v[t][c]; soma['BR'][c] += v[t][c]
    soma[uf]['n28'] += v[t].get('c28', 0); soma['BR']['n28'] += v[t].get('c28', 0)
res = {}
for uf in ['br'] + sorted(u.lower() for u in soma if u != 'BR'):
    o = oficial(uf, ELE[t]); s = soma['BR' if uf == 'br' else uf.upper()]
    dif = {c: s[c] - o[c] for c in ('L', 'R', 'B', 'N', 'comp')}
    res[uf] = {'boletins': {c: s[c] for c in ('L', 'R', 'B', 'N', 'comp', 'n28')}, 'oficial': o, 'diferenca': dif}
    print(uf, 'diferenca', dif, 'nulos do 28 nos boletins', s['n28'], flush=True)
    time.sleep(0.5)
json.dump(res, open(os.environ.get('SAIDA', f'soma_oficial_{t}t.json'), 'w'), ensure_ascii=False, indent=1)
