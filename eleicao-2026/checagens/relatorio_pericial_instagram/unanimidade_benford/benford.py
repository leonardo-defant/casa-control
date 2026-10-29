"""Capítulo 5: Lei de Benford, primeiro dígito (1BL), segundo dígito (2BL, Mebane) e último dígito (Beber e Scacco),
nos votos por seção de cada candidato. Placebos: eleitores aptos por seção e votos sintéticos gerados por um processo
limpo por construção (binomial com a fatia do local de votação ou do município, sem nenhuma manipulação na seção).
Uso: python3 -I benford.py <pasta_npz> <saida.json>"""
import json, os, sys, collections
import numpy as np
from scipy.stats import chi2

pasta, saida = sys.argv[1:3]
d1 = np.log10(1 + 1 / np.arange(1, 10))
d2 = np.array([sum(np.log10(1 + 1 / (10 * k + d)) for k in range(1, 10)) for d in range(10)])
MEDIA_2BL = float((np.arange(10) * d2).sum())


def digitos(x):
    x = np.asarray(x, np.int64)
    s = x.astype(str)
    return s


def teste(x, nome):
    x = np.asarray(x, np.int64)
    out = {'n_total': int(len(x)), 'zeros': int((x == 0).sum()), 'mediana': float(np.median(x)),
           'p10_p90': [float(np.percentile(x, 10)), float(np.percentile(x, 90))]}
    # 1BL
    a = x[x > 0]; f = a // 10 ** np.floor(np.log10(a)).astype(np.int64)
    obs = np.bincount(f, minlength=10)[1:10]; n = obs.sum(); p = obs / n
    c = float((((obs - n * d1) ** 2) / (n * d1)).sum())
    mad = float(np.abs(p - d1).mean())
    out['1BL'] = {'n': int(n), 'obs_pct': [round(100 * v, 2) for v in p], 'benford_pct': [round(100 * v, 2) for v in d1],
                  'qui2': round(c, 1), 'gl': 8, 'p': float(chi2.sf(c, 8)), 'MAD': round(mad, 4),
                  'Nigrini': 'conformidade próxima' if mad <= .006 else 'aceitável' if mad <= .012 else 'marginal' if mad <= .015 else 'não conformidade'}
    # 2BL (x >= 10)
    b = x[x >= 10]; sd = (b // 10 ** (np.floor(np.log10(b)).astype(np.int64) - 1)) % 10
    obs = np.bincount(sd, minlength=10); n = obs.sum(); p = obs / n
    c = float((((obs - n * d2) ** 2) / (n * d2)).sum())
    mad = float(np.abs(p - d2).mean())
    m = float(sd.mean()); ep = float(sd.std() / np.sqrt(n))
    out['2BL'] = {'n': int(n), 'obs_pct': [round(100 * v, 2) for v in p], 'benford_pct': [round(100 * v, 2) for v in d2],
                  'qui2': round(c, 1), 'gl': 9, 'p': float(chi2.sf(c, 9)), 'MAD': round(mad, 4),
                  'Nigrini': 'conformidade próxima' if mad <= .008 else 'aceitável' if mad <= .010 else 'marginal' if mad <= .012 else 'não conformidade',
                  'media': round(m, 4), 'media_esperada': round(MEDIA_2BL, 4), 'ep_media': round(ep, 4), 'z_media': round((m - MEDIA_2BL) / ep, 1)}
    # último dígito (x >= 10), uniforme
    u = x[x >= 10] % 10; obs = np.bincount(u, minlength=10); n = obs.sum()
    c = float((((obs - n / 10) ** 2) / (n / 10)).sum())
    out['ultimo_digito'] = {'n': int(n), 'obs_pct': [round(100 * v / n, 2) for v in obs], 'qui2': round(c, 1), 'gl': 9, 'p': float(chi2.sf(c, 9))}
    return out


rng = np.random.default_rng(20261029)
R = {'esperado_1BL_pct': [round(100 * v, 2) for v in d1], 'esperado_2BL_pct': [round(100 * v, 2) for v in d2], 'media_2BL': MEDIA_2BL}
for rot, nome, cand in (('2026_t2', '2026_2T', ('Lula', 'Flávio')), ('2026_t1', '2026_1T', ('Lula', 'Flávio')),
                        ('2022_t2', '2022_2T', ('Lula', 'Bolsonaro')), ('2018_t2', '2018_2T', ('Haddad', 'Bolsonaro'))):
    z = np.load(os.path.join(pasta, rot + '.npz'))
    L, Rr, O, apt, comp = z['L'], z['R'], z['O'], z['apt'], z['comp']
    ch = z['chave']
    p = np.array([k.split('|') for k in ch]); mun = p[:, 0] + '|' + p[:, 1]
    loc = np.char.add(np.char.add(np.char.add(mun, '|'), p[:, 2]), np.char.add('|', z['loc'].astype(str)))
    ok = (L + Rr + O) > 0
    res = {cand[0]: teste(L[ok], cand[0]), cand[1]: teste(Rr[ok], cand[1]), 'placebo_aptos': teste(apt[ok], 'apt')}
    # sintéticos limpos por construção
    V = L + Rr + O
    for nivel, g in (('local', loc), ('municipio', mun)):
        _, gi = np.unique(g, return_inverse=True)
        sL = np.bincount(gi, weights=L) / np.maximum(np.bincount(gi, weights=V), 1)
        sR = np.bincount(gi, weights=Rr) / np.maximum(np.bincount(gi, weights=V), 1)
        pL = sL[gi]; pR = np.where(pL < 1, sR[gi] / np.maximum(1 - pL, 1e-12), 0)
        sintL = rng.binomial(V, np.clip(pL, 0, 1))
        sintR = rng.binomial(V - sintL, np.clip(pR, 0, 1))
        res[f'sintetico_{nivel}_{cand[0]}'] = teste(sintL[ok], 's')
        res[f'sintetico_{nivel}_{cand[1]}'] = teste(sintR[ok], 's')
    # quanto do primeiro dígito é ditado pela faixa de tamanho
    for c_, x in ((cand[0], L[ok]), (cand[1], Rr[ok])):
        res[f'faixas_{c_}'] = {'1-9': round(100 * float(((x >= 1) & (x <= 9)).mean()), 2), '10-99': round(100 * float(((x >= 10) & (x <= 99)).mean()), 2),
                               '100-999': round(100 * float((x >= 100).mean()), 2), 'zero': round(100 * float((x == 0).mean()), 2), 'max': int(x.max())}
    res['aptos_max'] = int(apt.max()); res['aptos_p99'] = float(np.percentile(apt, 99))
    R[nome] = res
    print(nome, flush=True)
with open(saida, 'w') as f:
    json.dump(R, f, ensure_ascii=False, indent=1)
