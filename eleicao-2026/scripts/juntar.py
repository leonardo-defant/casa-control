"""Junta bases por turno: python3 -I juntar.py <saida.json.gz> <base1.json.gz> <base2.json.gz> ..."""
import gzip, json, sys
from lib import carregar
tudo = {}
for p in sys.argv[2:]:
    for k, v in carregar(p).items():
        tudo.setdefault(k, {}).update(v)
with gzip.open(sys.argv[1], 'wt') as f:
    json.dump(tudo, f, separators=(',', ':'))
print('secoes', len(tudo))
