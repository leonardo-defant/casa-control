"""T7 do pré-registro: ganho do candidato que mais ganhou, por seção, contra o bolo disponível na seção.
bolo = outros do 1º turno + queda do branco+nulo (se positiva) + aumento do comparecimento (se positivo)
Uso: python3 -I analisar_fluxos.py <secoes.json.gz> <campo L|R> [--chaves lista.txt]
"""
import json, sys
from lib import carregar

d = carregar(sys.argv[1]); c = sys.argv[2]; adv = 'R' if c == 'L' else 'L'
chaves = set(open(sys.argv[sys.argv.index('--chaves') + 1]).read().split()) if '--chaves' in sys.argv else None
n = pos = 0; ganho = exc = 0; ganho_pos = 0; sem_bolo_ganho = 0; n_sem_bolo = 0
bolo_tot = 0; perda_adv_secoes = 0
for k, v in d.items():
    if '1' not in v or '2' not in v or (chaves is not None and k not in chaves): continue
    a, b = v['1'], v['2']
    g = b[c] - a[c]
    bolo = a['O'] + max(0, (a['B'] + a['N']) - (b['B'] + b['N'])) + max(0, b['comp'] - a['comp'])
    e = g - bolo
    n += 1; ganho += g; bolo_tot += bolo
    if e > 0: pos += 1; exc += e
    if b[adv] < a[adv]: perda_adv_secoes += 1
    if bolo <= 2: n_sem_bolo += 1; sem_bolo_ganho += g
print(json.dumps({'secoes': n, 'ganho_total': ganho, 'bolo_total': bolo_tot,
                  'pct_secoes_excesso': 100 * pos / n, 'excesso_total': exc, 'pct_ganho_em_excesso': 100 * exc / ganho if ganho else None,
                  'pct_secoes_adversario_perdeu_votos': 100 * perda_adv_secoes / n,
                  'secoes_sem_bolo': n_sem_bolo, 'ganho_nas_secoes_sem_bolo': sem_bolo_ganho}))
