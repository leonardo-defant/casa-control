"""T4 do pré-registro: excesso de seções com branco+nulo de presidente zerado (Z0) ou no máximo 1 (Z1).

Esperado por seção: beta-binomial com média igual à taxa das outras seções do mesmo local
(ou do município, se o local tiver uma seção só) e superdispersão rho por método dos momentos.
Leitura calibrada (adendo 6): o mesmo estimador aplicado a dados simulados sob a hipótese nula dá R_nulo;
Rc = R / R_nulo. Votos do 28 (candidatura anulada) contam como nulos.
Uso: python3 -I analisar_zeros.py <secoes.json.gz> <turno 1|2> [--ufs AC,AM] [--chaves lista.txt] [--sims 5]
"""
import os as _os, sys as _sys
_sys.path.insert(0, _os.path.dirname(_os.path.abspath(__file__)))
import json, math, sys
import numpy as np
from scipy.special import gammaln
from lib import carregar, chave_local

MINCOMP = 50


def lbeta(a, b):
    return gammaln(a) + gammaln(b) - gammaln(a + b)


def grupos_ids(chaves):
    _, g = np.unique(np.array(chaves), return_inverse=True)
    return g


def estimar(bn, n, gL, gM):
    """Devolve p (leave-one-out), nout e a máscara das seções com média definida."""
    sbL = np.bincount(gL, weights=bn); snL = np.bincount(gL, weights=n); cL = np.bincount(gL)
    sbM = np.bincount(gM, weights=bn); snM = np.bincount(gM, weights=n); cM = np.bincount(gM)
    usaL = cL[gL] >= 2; usaM = (~usaL) & (cM[gM] >= 2)
    p = np.full(len(n), np.nan); nout = np.full(len(n), np.nan)
    p[usaL] = (sbL[gL] - bn)[usaL] / (snL[gL] - n)[usaL]; nout[usaL] = (snL[gL] - n)[usaL]
    p[usaM] = (sbM[gM] - bn)[usaM] / (snM[gM] - n)[usaM]; nout[usaM] = (snM[gM] - n)[usaM]
    return p, nout, usaL | usaM


def calcular_arrays(bn, n, gL, gM):
    p, nout, ok = estimar(bn, n, gL, gM)
    bn, n, p, nout = bn[ok], n[ok], p[ok], nout[ok]
    q = p * (1 - p)
    resid = (bn - n * p) ** 2 - n * q - n ** 2 * q / nout
    rho = max(float(resid.sum() / (n * (n - 1) * q).sum()), 1e-6)
    P0 = np.zeros(len(n)); P1 = np.zeros(len(n))
    meio = (p > 0) & (p < 1)
    P0[p <= 0] = 1.0
    a = p[meio] * (1 / rho - 1); b = (1 - p[meio]) * (1 / rho - 1); nn = n[meio]
    lb = lbeta(a, b)
    P0[meio] = np.exp(lbeta(a, b + nn) - lb)
    P1[meio] = np.exp(np.log(nn) + lbeta(a + 1, b + nn - 1) - lb)
    z0 = int((bn == 0).sum()); z1 = int((bn <= 1).sum()); e0 = float(P0.sum()); e1 = float((P0 + P1).sum())
    return {'secoes': int(len(n)), 'bn_medio': float(100 * bn.sum() / n.sum()), 'rho': rho,
            'Z0_obs': z0, 'Z0_esp': e0, 'R0': z0 / e0, 'Z1_obs': z1, 'Z1_esp': e1, 'R1': z1 / e1}


def simular(bn, n, gL, gM, rho, rng):
    """Branco+nulo sob a nula: beta-binomial em torno da taxa do local (ou do município, se local de seção única)."""
    sbL = np.bincount(gL, weights=bn); snL = np.bincount(gL, weights=n); cL = np.bincount(gL)
    sbM = np.bincount(gM, weights=bn); snM = np.bincount(gM, weights=n)
    pt = np.where(cL[gL] >= 2, sbL[gL] / snL[gL], sbM[gM] / snM[gM])
    pt = np.clip(pt, 1e-6, 1 - 1e-6)
    a = pt * (1 / rho - 1); b = (1 - pt) * (1 / rho - 1)
    return rng.binomial(n.astype(np.int64), rng.beta(a, b)).astype(float)


def calcular(d, turno, ufs=None, chaves=None, sims=5, semente=20261026):
    sec = []
    for k, v in d.items():
        if turno not in v: continue
        if ufs and k.split('|')[0] not in ufs: continue
        if chaves is not None and k not in chaves: continue
        s = v[turno]
        if s['comp'] < MINCOMP: continue
        sec.append((chave_local(k, s), '|'.join(k.split('|')[:2]), s['B'] + s['N'] + s.get('c28', 0), s['comp']))
    gL = grupos_ids([x[0] for x in sec]); gM = grupos_ids([x[1] for x in sec])
    bn = np.array([x[2] for x in sec], float); n = np.array([x[3] for x in sec], float)
    obs = calcular_arrays(bn, n, gL, gM)
    if not sims:
        return obs
    rng = np.random.default_rng(semente)
    # ajusta o rho verdadeiro para que o estimador nos dados simulados reproduza o rho observado
    rho_v = obs['rho']
    for _ in range(3):
        r_sim = calcular_arrays(simular(bn, n, gL, gM, rho_v, rng), n, gL, gM)['rho']
        rho_v = max(rho_v * obs['rho'] / r_sim, 1e-6)
    nul = [calcular_arrays(simular(bn, n, gL, gM, rho_v, rng), n, gL, gM) for _ in range(sims)]
    R0n = float(np.mean([x['R0'] for x in nul])); R1n = float(np.mean([x['R1'] for x in nul]))
    obs.update({'rho_verdadeiro_ajustado': rho_v, 'R0_nulo': R0n, 'R1_nulo': R1n,
                'R0_nulo_dp': float(np.std([x['R0'] for x in nul])), 'Rc0': obs['R0'] / R0n, 'Rc1': obs['R1'] / R1n,
                'excesso_Z0_vs_nulo': obs['Z0_obs'] - obs['Z0_esp'] * R0n})
    return obs


if __name__ == '__main__':
    d = carregar(sys.argv[1]); turno = sys.argv[2]
    arg = lambda f: sys.argv[sys.argv.index(f) + 1] if f in sys.argv else None
    ufs = set(arg('--ufs').split(',')) if arg('--ufs') else None
    chaves = set(open(arg('--chaves')).read().split()) if arg('--chaves') else None
    print(json.dumps(calcular(d, turno, ufs, chaves, int(arg('--sims') or 5))))
