"""Presidente contra governador na mesma urna, seção por seção (estados com 2º turno de governador).

y = virada do 13 na fatia entre os dois finalistas (pontos)
x = queda do branco+nulo de presidente menos queda do branco+nulo de governador (pontos do comparecimento)
Efeito fixo de município (reproduz a referência de 2022 do documento, +0,04) e, como checagem, de local de votação.
Peso = votos no 13 + direita no 2º turno; erro agrupado pelo grupo do efeito fixo.
--simular f: injeta no 2º turno a conversão de uma fração f do branco+nulo de presidente de cada seção para o 13.
Uso: python3 -I analisar_gov.py <secoes.json.gz> <ano> [--simular f1,f2] [--ufs AC,AM,...]
"""
import os as _os, sys as _sys
_sys.path.insert(0, _os.path.dirname(_os.path.abspath(__file__)))
import json, sys, warnings
import numpy as np
from lib import carregar, chave_local, fe_ols
warnings.filterwarnings('ignore')


def montar(d, ufs=None):
    sel = [(k, chave_local(k, v['2']), v['1'], v['2'], v['1g'], v['2g']) for k, v in d.items()
           if all(t in v for t in ('1', '2', '1g', '2g')) and (ufs is None or k.split('|')[0] in ufs)]
    f = lambda i, c: np.array([s[i][c] for s in sel], float)
    A = {c + '1': f(2, c) for c in 'L R O B N comp'.split()}
    A.update({c + '2': f(3, c) for c in 'L R O B N comp'.split()})
    A.update({'g' + c + '1': f(4, c) for c in 'B N comp'.split()})
    A.update({'g' + c + '2': f(5, c) for c in 'B N comp'.split()})
    A['local'] = np.array([s[1] for s in sel])
    A['municipio'] = np.array(['|'.join(s[0].split('|')[:2]) for s in sel])
    return A


def rodar(A, conv=0.0):
    L1, R1, B1, N1, C1 = A['L1'], A['R1'], A['B1'], A['N1'], A['comp1']
    B2, N2, C2 = A['B2'], A['N2'], A['comp2']
    L2 = A['L2'] + conv * (B2 + N2); R2 = A['R2']
    B2e, N2e = B2 * (1 - conv), N2 * (1 - conv)
    ok = (C1 > 0) & (C2 > 0) & (A['gcomp1'] > 0) & (A['gcomp2'] > 0) & (L1 + R1 > 0) & (L2 + R2 > 0)
    y = 100 * (L2 / (L2 + R2) - L1 / (L1 + R1))
    qp = 100 * ((B1 + N1) / C1 - (B2e + N2e) / C2)
    qg = 100 * ((A['gB1'] + A['gN1']) / A['gcomp1'] - (A['gB2'] + A['gN2']) / A['gcomp2'])
    x = (qp - qg)[:, None]
    out = {}
    for fe in ('municipio', 'local'):
        r = fe_ols(y[ok], x[ok], A[fe][ok], (L2 + R2)[ok], ['rel'])
        out[fe] = {'n': r['n'], 'grupos': r['grupos'], 'coef': r['coef']['rel'], 'ep': r['ep']['rel']}
    out['convertidos'] = float((conv * (B2 + N2))[ok].sum())
    return out


if __name__ == '__main__':
    d = carregar(sys.argv[1]); ano = sys.argv[2]
    ufs = set(sys.argv[sys.argv.index('--ufs') + 1].split(',')) if '--ufs' in sys.argv else None
    A = montar(d, ufs)
    res = {'ano': ano, 'base': rodar(A)}
    if '--simular' in sys.argv:
        res['simulacao'] = {f: rodar(A, float(f)) for f in sys.argv[sys.argv.index('--simular') + 1].split(',')}
    print(json.dumps(res, ensure_ascii=False, indent=1))
