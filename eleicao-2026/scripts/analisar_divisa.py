"""T34 do pré-registro (Adendo 15): salto na divisa entre UFs da fatia de Lula no 2º turno, depois de descontar o 1º turno.
Unidade: local de votação do arquivo de locais de 2026 (2º turno), com as seções somadas pela chave UF|município|zona|seção.
Para cada divisa (UF a, UF b): faixa = locais de a a até 100 km de um local de b e vice-versa; modelo linear ponderado pelos
votos nominais do 2º turno, fatia m2 = L2/(L2+R2) contra as fatias do comparecimento do 1º turno (L, R, demais; branco+nulo é a
base) e o log do eleitorado, sem variável de UF; pares = cada local de um lado com o mais próximo do outro a até 20 km (pares
repetidos uma vez); J = média de r(b) - r(a) ponderada pelos votos nominais do par; erro-padrão por bootstrap de municípios de a.
Uso: python3 -I analisar_divisa.py <secoes.json.gz> <pasta_csv_locais_2026> <saida.json> [--divisas PR-SP,PR-MS,...] [--reps 2000]
"""
import os as _os, sys as _sys
_sys.path.insert(0, _os.path.dirname(_os.path.abspath(__file__)))
import collections, csv, json, os, sys
import numpy as np
from scipy.spatial import cKDTree
from lib import carregar

SUL_NAO_SUL = 'PR-SP+MS'  # a divisa do teste; PR-SP e PR-MS saem também em separado, descritivas
DESCRITIVAS = ['PR-SP', 'PR-MS']
PLACEBO = ['PR-SC', 'SC-RS', 'SP-MS', 'SP-MG', 'SP-RJ', 'MS-MT', 'MS-GO', 'MS-MG', 'MG-GO', 'GO-MT', 'MG-RJ']
R_TERRA = 6371.0


def ler_locais(pasta, ufs):
    """chave da seção -> id do local; id do local -> (lat, lon, município)."""
    sec, loc = {}, {}
    for uf in ufs:
        with open(os.path.join(pasta, f'eleitorado_local_votacao_2026_{uf}.csv'), encoding='latin1') as f:
            r = csv.reader(f, delimiter=';'); h = next(r); ix = {c: i for i, c in enumerate(h)}
            for row in r:
                if row[ix['NR_TURNO']] != '2':
                    continue
                try:
                    lat = float(row[ix['NR_LATITUDE']].replace(',', '.')); lon = float(row[ix['NR_LONGITUDE']].replace(',', '.'))
                except ValueError:
                    continue
                if lat == -1 or lon == -1:
                    continue
                mun, z, s, lv = (int(row[ix[c]]) for c in ('CD_MUNICIPIO', 'NR_ZONA', 'NR_SECAO', 'NR_LOCAL_VOTACAO'))
                lid = f'{uf}|{mun}|{z}|{lv}'
                sec[f'{uf}|{mun}|{z}|{s}'] = lid; loc[lid] = (lat, lon, f'{uf}|{mun}')
    return sec, loc


def somar(d, sec):
    soma = collections.defaultdict(lambda: np.zeros(8))
    for k, v in d.items():
        if k not in sec or '1' not in v or '2' not in v:
            continue
        a, b = v['1'], v['2']
        soma[sec[k]] += [a['L'], a['R'], a['O'], a['B'] + a['N'], a['comp'], b['L'], b['R'], b.get('apt', a.get('apt', 0))]
    return soma


def xyz(lat, lon):
    la, lo = np.radians(lat), np.radians(lon)
    return np.column_stack([np.cos(la) * np.cos(lo), np.cos(la) * np.sin(lo), np.sin(la)])


def corda(km):
    return 2 * np.sin(km / (2 * R_TERRA))


def divisa(ua, ub, soma, loc, reps, rng):
    """ua e ub: UFs de cada lado, separadas por + (ex.: 'SP+MS')."""
    ids = {u: [l for l in soma if l.split('|')[0] in u.split('+') and soma[l][5] + soma[l][6] >= 100 and soma[l][4] > 0]
           for u in (ua, ub)}
    if not ids[ua] or not ids[ub]:
        return {'pares': 0}
    P = {u: xyz(np.array([loc[l][0] for l in ids[u]]), np.array([loc[l][1] for l in ids[u]])) for u in (ua, ub)}
    T = {u: cKDTree(P[u]) for u in (ua, ub)}
    faixa = []
    for u, o in ((ua, ub), (ub, ua)):
        dist, _ = T[o].query(P[u])
        faixa += [l for l, dd in zip(ids[u], dist) if dd <= corda(100)]
    if len(faixa) < 20:
        return {'pares': 0, 'faixa': len(faixa)}
    M = np.array([soma[l] for l in faixa])
    comp1 = M[:, 4]; nom2 = M[:, 5] + M[:, 6]
    X = np.column_stack([np.ones(len(M)), M[:, 0] / comp1, M[:, 1] / comp1, M[:, 2] / comp1, np.log(np.maximum(M[:, 7], 1))])
    y = M[:, 5] / nom2; sw = np.sqrt(nom2)
    beta = np.linalg.lstsq(X * sw[:, None], y * sw, rcond=None)[0]
    res = dict(zip(faixa, y - X @ beta)); peso = dict(zip(faixa, nom2))
    pares = set()
    for u, o in ((ua, ub), (ub, ua)):
        dist, j = T[o].query(P[u])
        for l, dd, jj in zip(ids[u], dist, j):
            if dd <= corda(20):
                m = ids[o][jj]
                pares.add((l, m) if u == ua else (m, l))
    pares = sorted(pares)
    if len(pares) < 50:
        return {'pares': len(pares), 'faixa': len(faixa), 'fora': 'menos de 50 pares'}
    dif = np.array([res[b] - res[a] for a, b in pares]); w = np.array([peso[a] + peso[b] for a, b in pares])
    J = float((w * dif).sum() / w.sum())
    mun = np.array([loc[a][2] for a, _ in pares]); um, g = np.unique(mun, return_inverse=True)
    sw_g = np.bincount(g, weights=w); sd_g = np.bincount(g, weights=w * dif)
    boot = []
    for _ in range(reps):
        c = np.bincount(rng.integers(0, len(um), len(um)), minlength=len(um))
        boot.append((c * sd_g).sum() / (c * sw_g).sum())
    return {'pares': len(pares), 'faixa': len(faixa), 'municipios_lado_a': len(um), 'J': J, 'ep': float(np.std(boot, ddof=1)),
            'r2_modelo': float(1 - np.average((y - X @ beta) ** 2, weights=nom2) / np.average((y - np.average(y, weights=nom2)) ** 2, weights=nom2))}


def main():
    secoes, pasta, saida = sys.argv[1:4]
    arg = lambda f, pad: sys.argv[sys.argv.index(f) + 1] if f in sys.argv else pad
    divs = arg('--divisas', ','.join([SUL_NAO_SUL] + DESCRITIVAS + PLACEBO)).split(','); reps = int(arg('--reps', '2000'))
    ufs = sorted({u for dv in divs for lado in dv.split('-') for u in lado.split('+')})
    sec, loc = ler_locais(pasta, ufs)
    soma = somar(carregar(secoes), sec)
    rng = np.random.default_rng(20261026)
    out = {'locais_com_votos': len(soma), 'divisas': {}}
    for dv in divs:
        ua, ub = dv.split('-')
        out['divisas'][dv] = divisa(ua, ub, soma, loc, reps, rng)
        print(dv, out['divisas'][dv], flush=True)
    r = out['divisas'].get(SUL_NAO_SUL, {})
    if 'J' in r:
        out['J_sul_nao_sul'] = [r['J'], r['ep']]
    pl = [abs(out['divisas'][d]['J']) for d in PLACEBO if 'J' in out['divisas'].get(d, {})]
    out['mediana_abs_J_placebo'] = float(np.median(pl)) if pl else None
    json.dump(out, open(saida, 'w'), ensure_ascii=False, indent=1)
    print(json.dumps({k: out[k] for k in ('J_sul_nao_sul', 'mediana_abs_J_placebo') if k in out}))


if __name__ == '__main__':
    main()
