"""Sorteia a amostra do 2º turno (semente fixa) a partir das listas de seções do 2º turno (-cs.json)
e da base do 1º turno (para o local de votação).

Estratos:
  M: 120 municípios inteiros (sorteio simples entre municípios com até 1.500 seções), com bu, rdv e log
  L: 1.500 locais de votação com 2 ou mais seções, no país (fora de M)
  G: metade dos locais com 2 ou mais seções nos 6 estados com 2º turno de governador (fora de M e L)
Uso: python3 -I sortear_amostra.py <pasta_cs2t> <secoes2026_1t.json.gz> <pasta_saida>
"""
import collections, json, os, random, sys
from lib import carregar, chave_local

SEMENTE = 20261026
GOV = {'AC', 'AM', 'DF', 'ES', 'RN', 'TO'}

pasta_cs, base1t, saida = sys.argv[1], sys.argv[2], sys.argv[3]
d1 = carregar(base1t)
secoes2t = []  # seções principais (com urna própria) no 2º turno
agregadas = 0
for f in sorted(os.listdir(pasta_cs)):
    cs = json.load(open(os.path.join(pasta_cs, f)))
    for e in cs['abr']:
        uf = e['cd'].upper()
        for m in e['mu']:
            for z in m['zon']:
                for s in z['sec']:
                    if s.get('nsp'):
                        agregadas += 1; continue
                    secoes2t.append(f"{uf}|{int(m['cd'])}|{int(z['cd'])}|{int(s['ns'])}")
print('secoes principais no 2T', len(secoes2t), 'agregadas', agregadas)
sem1t = [k for k in secoes2t if k not in d1 or '1' not in d1[k]]
print('sem par no 1T', len(sem1t))

mun = collections.defaultdict(list); loc = collections.defaultdict(list)
for k in secoes2t:
    uf, m, z, s = k.split('|')
    mun[(uf, m)].append(k)
    if k in d1 and '1' in d1[k]:
        loc[chave_local(k, d1[k]['1'])].append(k)

rng = random.Random(SEMENTE)
cand_m = sorted(m for m, ks in mun.items() if len(ks) <= 1500)
M = sorted(rng.sample(cand_m, 120))
setM = set(M)
cand_l = sorted(l for l, ks in loc.items() if len(ks) >= 2 and tuple(l.split('|')[:2]) not in setM)
L = sorted(rng.sample(cand_l, 1500))
setL = set(L)
cand_g = sorted(l for l in cand_l if l.split('|')[0] in GOV and l not in setL)
G = sorted(rng.sample(cand_g, len(cand_g) // 2))

os.makedirs(saida, exist_ok=True)
lm = [k for m in M for k in sorted(mun[m])]
ll = [k for l in L for k in sorted(loc[l])]
lg = [k for l in G for k in sorted(loc[l])]
open(os.path.join(saida, 'estrato_M.txt'), 'w').write('\n'.join(lm) + '\n')
open(os.path.join(saida, 'estrato_L.txt'), 'w').write('\n'.join(ll) + '\n')
open(os.path.join(saida, 'estrato_G.txt'), 'w').write('\n'.join(lg) + '\n')
json.dump({'semente': SEMENTE, 'municipios_M': ['|'.join(m) for m in M], 'locais_L': L, 'locais_G': G}, open(os.path.join(saida, 'amostra.json'), 'w'))
print('M', len(M), 'municipios', len(lm), 'secoes | L', len(L), 'locais', len(ll), 'secoes | G', len(G), 'locais', len(lg), 'secoes')
print('estados em M', collections.Counter(m[0] for m in M).most_common())
