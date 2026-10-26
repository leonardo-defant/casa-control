"""T4 do pré-registro: excesso de seções com branco+nulo de presidente zerado (Z0) ou no máximo 1 (Z1).

Esperado por seção: beta-binomial com média igual à taxa das outras seções do mesmo local
(ou do município, se o local tiver uma seção só) e superdispersão rho por método dos momentos.
Uso: python3 -I analisar_zeros.py <secoes.json.gz> <turno 1|2> [--ufs AC,AM] [--chaves lista.txt]
"""
import collections, json, math, sys
import numpy as np
from lib import carregar, chave_local

MINCOMP = 50


def lbeta(a, b):
    return math.lgamma(a) + math.lgamma(b) - math.lgamma(a + b)


def calcular(d, turno, ufs=None, chaves=None):
    sec = []
    for k, v in d.items():
        if turno not in v: continue
        if ufs and k.split('|')[0] not in ufs: continue
        if chaves is not None and k not in chaves: continue
        s = v[turno]
        if s['comp'] < MINCOMP: continue
        sec.append((k, chave_local(k, s), '|'.join(k.split('|')[:2]), s['B'] + s['N'], s['comp']))
    bn = np.array([x[3] for x in sec], float); n = np.array([x[4] for x in sec], float)
    def loo(idx_key):
        sb = collections.Counter(); sn = collections.Counter(); c = collections.Counter()
        for x in sec: sb[x[idx_key]] += x[3]; sn[x[idx_key]] += x[4]; c[x[idx_key]] += 1
        return sb, sn, c
    sbL, snL, cL = loo(1); sbM, snM, cM = loo(2)
    p = np.empty(len(sec)); nout = np.empty(len(sec))
    for i, x in enumerate(sec):
        if cL[x[1]] >= 2:
            p[i] = (sbL[x[1]] - x[3]) / (snL[x[1]] - x[4]); nout[i] = snL[x[1]] - x[4]
        elif cM[x[2]] >= 2:
            p[i] = (sbM[x[2]] - x[3]) / (snM[x[2]] - x[4]); nout[i] = snM[x[2]] - x[4]
        else:
            p[i] = np.nan; nout[i] = np.nan
    ok = np.isfinite(p)
    bn, n, p, nout = bn[ok], n[ok], p[ok], nout[ok]
    # superdispersão pelo método dos momentos, descontando o erro de estimar p
    q = p * (1 - p)
    resid = (bn - n * p) ** 2 - n * q - n ** 2 * q / nout
    rho = max(float(resid.sum() / (n * (n - 1) * q).sum()), 1e-6)
    P0 = np.empty(len(n)); P1 = np.empty(len(n))
    for i in range(len(n)):
        pi, ni = p[i], int(n[i])
        if pi <= 0:
            P0[i], P1[i] = 1.0, 0.0; continue
        if pi >= 1:
            P0[i], P1[i] = 0.0, 0.0; continue
        a = pi * (1 / rho - 1); b = (1 - pi) * (1 / rho - 1)
        lb = lbeta(a, b)
        P0[i] = math.exp(lbeta(a, b + ni) - lb)
        P1[i] = math.exp(math.log(ni) + lbeta(a + 1, b + ni - 1) - lb)
    z0 = (bn == 0).sum(); z1 = (bn <= 1).sum()
    e0 = P0.sum(); e1 = (P0 + P1).sum()
    return {'secoes': int(len(n)), 'bn_medio': float(100 * bn.sum() / n.sum()), 'rho': rho,
            'Z0_obs': int(z0), 'Z0_esp': float(e0), 'R0': float(z0 / e0),
            'Z1_obs': int(z1), 'Z1_esp': float(e1), 'R1': float(z1 / e1)}


if __name__ == '__main__':
    d = carregar(sys.argv[1]); turno = sys.argv[2]
    ufs = set(sys.argv[sys.argv.index('--ufs') + 1].split(',')) if '--ufs' in sys.argv else None
    chaves = set(open(sys.argv[sys.argv.index('--chaves') + 1]).read().split()) if '--chaves' in sys.argv else None
    print(json.dumps(calcular(d, turno, ufs, chaves)))
