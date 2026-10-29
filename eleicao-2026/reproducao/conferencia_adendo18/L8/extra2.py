"""Conferência L8, mais três leituras minhas: lacunas do recebimento do 1º turno por UF; quantas seções tardias estão em
locais mistos (as únicas que informam o efeito fixo de local); as 125.624 seções encerradas até 17:00:59 no 1º turno."""
import collections, datetime as dt, json, os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from conferir import ler, P, DIA
from extra import desloc
T = {1: ler(sys.argv[1]), 2: ler(sys.argv[2])}
R = {}
for nome, a, b in (('18h01_18h08', (18, 1, 1), (18, 8, 46)), ('19h31_19h59', (19, 31, 51), (19, 59, 21))):
    ta = DIA[1].replace(hour=a[0], minute=a[1], second=a[2]); tb = DIA[1].replace(hour=b[0], minute=b[1], second=b[2])
    dentro = collections.Counter(k.split('|')[0] for k, s in T[1].items() if ta <= P(s['rec']) <= tb)
    ufs_depois = collections.Counter(k.split('|')[0] for k, s in T[1].items() if P(s['rec']) > tb)
    R[nome] = {'recebidos_na_lacuna': sum(dentro.values()), 'ufs_com_boletins_pendentes': len(ufs_depois)}
EB = {t: {k: P(s['enc']) + dt.timedelta(hours=desloc(k)) for k, s in T[t].items() if not k.startswith('ZZ') and P(s['enc'])} for t in (1, 2)}
for nome, lim in (('17h15m59', DIA[2].replace(hour=17, minute=15, second=59)), ('18h59m59', DIA[2].replace(hour=18, minute=59, second=59))):
    loc = collections.defaultdict(list)
    for k, v in EB[2].items():
        uf, mu, z, _ = k.split('|'); loc[f'{uf}|{mu}|{z}|{T[2][k]["loc"]}'].append(v > lim)
    tarde_mistos = sum(sum(v) for v in loc.values() if 0 < sum(v) < len(v))
    tarde_todos = sum(sum(v) for v in loc.values() if sum(v) == len(v))
    R[f'locais_{nome}'] = {'tardias_em_locais_mistos': tarde_mistos, 'tardias_em_locais_todos_tardios': tarde_todos,
                          'locais_mistos': sum(1 for v in loc.values() if 0 < sum(v) < len(v)),
                          'locais_todos_tardios': sum(1 for v in loc.values() if sum(v) == len(v))}
lim = DIA[2].replace(hour=17, minute=0, second=59)
ks = [k for k, v in EB[2].items() if v <= lim and k in T[1]]
outros = [k for k, v in EB[2].items() if v > lim and k in T[1]]
def sh(t, kk):
    L = sum(T[t][k]['L'] for k in kk); Rr = sum(T[t][k]['R'] for k in kk); return round(100 * L / (L + Rr), 2)
R['cedo_2t_mesmas_secoes'] = {'n': len(ks), 'L_1t': sh(1, ks), 'L_2t': sh(2, ks), 'demais_L_1t': sh(1, outros), 'demais_L_2t': sh(2, outros),
                              'uf_top': collections.Counter(k.split('|')[0] for k in ks).most_common(8)}
json.dump(R, open(sys.argv[3], 'w'), ensure_ascii=False, indent=1)
print(json.dumps(R, ensure_ascii=False))
