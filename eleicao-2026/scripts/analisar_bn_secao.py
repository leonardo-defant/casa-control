"""Pista do branco/nulo por seção: virada do 13 entre turnos contra o branco/nulo do 1º turno
da própria seção, dentro do mesmo local de votação.

Especificação (reproduz as referências do documento: 2018 -0,060; 2022 -0,071):
  y  = 100 * (13 / (13 + direita)) no 2º turno menos o mesmo no 1º turno (fatia entre os dois finalistas)
  x  = branco+nulo, outros candidatos e 13 no 1º turno, em % do comparecimento do 1º turno
  efeito fixo do local de votação, peso = votos no 13 + direita no 2º turno, erro agrupado por local.

Uso: python3 -I analisar_bn_secao.py <secoes.json.gz> <ano> [--simular f1,f2,...]
--simular injeta no 2º turno uma conversão de uma fração f do branco+nulo de cada seção para o 13
(calibração do tamanho do sinal).
"""
import json, sys, warnings
import numpy as np
from lib import carregar, chave_local, fe_ols
warnings.filterwarnings('ignore')


def montar(d):
    rows = []
    for k, v in d.items():
        if '1' not in v or '2' not in v:
            continue
        a, b = v['1'], v['2']
        rows.append((chave_local(k, a), a['L'], a['R'], a['O'], a['B'], a['N'], a['comp'],
                     b['L'], b['R'], b['O'], b['B'], b['N'], b['comp']))
    loc = np.array([r[0] for r in rows])
    A = np.array([r[1:] for r in rows], float).T
    return loc, A


def rodar(loc, A, conv=0.0):
    L1, R1, O1, B1, N1, C1, L2, R2, O2, B2, N2, C2 = A
    L2 = L2 + conv * (B2 + N2)
    ok = (C1 > 0) & (C2 > 0) & (L1 + R1 > 0) & (L2 + R2 > 0)
    y = 100 * (L2 / (L2 + R2) - L1 / (L1 + R1))
    X = np.column_stack([100 * (B1 + N1) / C1, 100 * O1 / C1, 100 * L1 / C1])
    r = fe_ols(y[ok], X[ok], loc[ok], (L2 + R2)[ok], ['branco_nulo_1t', 'outros_1t', 'fatia13_1t'])
    r['bn_medio_1t'] = float(100 * (B1 + N1)[ok].sum() / C1[ok].sum())
    r['convertidos'] = float((conv * (B2 + N2))[ok].sum())
    return r


if __name__ == '__main__':
    d = carregar(sys.argv[1]); ano = sys.argv[2]
    loc, A = montar(d)
    res = {'ano': ano, 'base': rodar(loc, A)}
    if '--simular' in sys.argv:
        fs = [float(x) for x in sys.argv[sys.argv.index('--simular') + 1].split(',')]
        res['simulacao'] = {str(f): rodar(loc, A, f) for f in fs}
    print(json.dumps(res, ensure_ascii=False, indent=1))
