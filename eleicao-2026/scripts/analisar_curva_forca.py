"""T35 do pré-registro (Adendo 15): perda dos próprios eleitores do 1º turno por faixa de força local do adversário.
Para cada ano, nas mesmas seções: faixa do local de votação pela fatia do adversário no 1º turno (entre os válidos do
local); em cada faixa, a regressão do T8 sem grupos para os dois finalistas, empilhada (efeito fixo de local por
candidato, erro agrupado por local), e d = próprio(direita) - próprio(esquerda). A = média de d pelo inverso da variância
sobre as faixas em que os dois têm pelo menos 30 locais.
Uso: python3 -I analisar_curva_forca.py <secoes2026.json.gz> <secoes2022.json.gz> <secoes2018.json.gz> [--chaves lista.txt]
"""
import os as _os, sys as _sys
_sys.path.insert(0, _os.path.dirname(_os.path.abspath(__file__)))
import collections, json, sys
import numpy as np
from lib import carregar, chave_local
from analisar_pres_gov import ols_cluster

FAIXAS = [(0, .35), (.35, .50), (.50, .65), (.65, 1.01)]
NOMES = ['outros_1T', 'queda_branco_nulo', 'var_comparecimento', 'adversario_1T', 'proprio_1T']


def linhas(d, chaves):
    out = []
    for k in chaves:
        v = d.get(k)
        if not v or '1' not in v or '2' not in v:
            continue
        a, b = v['1'], v['2']
        out.append((k, chave_local(k, b), a, b))
    return out


def faixa_do_local(rows, c):
    """Fatia do adversário de c no 1º turno entre os válidos do local (o 28 de 2026 sai dos válidos)."""
    adv = 'R' if c == 'L' else 'L'
    num, den = collections.Counter(), collections.Counter()
    for _, loc, a, _ in rows:
        num[loc] += a[adv]; den[loc] += a['L'] + a['R'] + a['O'] - a.get('c28', 0)
    return {loc: num[loc] / den[loc] for loc in den if den[loc] > 0}


def x_t8(a, b, c):
    adv = 'R' if c == 'L' else 'L'
    return b[c] - a[c], [a['O'], (a['B'] + a['N']) - (b['B'] + b['N']), b['comp'] - a['comp'], a[adv], a[c]]


def ano(d, chaves):
    rows = linhas(d, chaves)
    fx = {c: faixa_do_local(rows, c) for c in 'LR'}
    res = {}
    for i, (lo, hi) in enumerate(FAIXAS):
        bloco = {}
        for c in 'LR':
            sel = [r for r in rows if r[1] in fx[c] and lo <= fx[c][r[1]] < hi]
            bloco[c] = sel
        nl = {c: sum(1 for n in collections.Counter(r[1] for r in bloco[c]).values() if n >= 2) for c in 'LR'}
        item = {'faixa': f'{lo:.2f}-{min(hi, 1):.2f}', 'secoes_L': len(bloco['L']), 'secoes_R': len(bloco['R']),
                'locais_L': nl['L'], 'locais_R': nl['R']}
        if min(nl.values()) < 30:
            item['fora'] = 'menos de 30 locais'; res[i] = item; continue
        ys, Xs, fe, cl = [], [], [], []
        for j, c in enumerate('LR'):
            for k, loc, a, b in bloco[c]:
                y, x = x_t8(a, b, c); z = [0.0] * 10; z[5 * j:5 * j + 5] = x
                ys.append(y); Xs.append(z); fe.append(loc + '|' + c); cl.append(loc)
        bb, V, N, G = ols_cluster(np.array(ys, float), np.array(Xs, float), fe, cl)
        item['proprio_L'] = [float(bb[4]), float(np.sqrt(V[4, 4]))]
        item['proprio_R'] = [float(bb[9]), float(np.sqrt(V[9, 9]))]
        item['d'] = [float(bb[9] - bb[4]), float(np.sqrt(V[4, 4] + V[9, 9] - 2 * V[4, 9]))]
        res[i] = item
    ds = [r['d'] for r in res.values() if 'd' in r]
    if ds:
        w = np.array([1 / s ** 2 for _, s in ds]); m = np.array([x for x, _ in ds])
        A = [float((w * m).sum() / w.sum()), float(1 / np.sqrt(w.sum()))]
    else:
        A = None
    return {'secoes': len(rows), 'faixas': list(res.values()), 'A': A}


def main():
    d26, d22, d18 = (carregar(p) for p in sys.argv[1:4])
    if '--chaves' in sys.argv:
        chaves = open(sys.argv[sys.argv.index('--chaves') + 1]).read().split()
    else:
        chaves = [k for k, v in d26.items() if '1' in v and '2' in v]
    out = {'2026': ano(d26, chaves), '2022': ano(d22, chaves), '2018': ano(d18, chaves)}
    A26, A18 = out['2026']['A'], out['2018']['A']
    if A26 and A18:
        dif = [A26[0] - A18[0], float(np.hypot(A26[1], A18[1]))]
        out['A2026_menos_A2018'] = dif
        sinal = A26[0] <= -0.03 and -A26[0] / A26[1] > 2.5 and dif[0] <= -0.03 and -dif[0] / dif[1] > 2.5
        sem = abs(A26[0]) <= 0.015 and abs(dif[0]) <= 0.015
        out['veredito'] = 'SINAL' if sinal else 'SEM SINAL' if sem else 'INCONCLUSIVO'
    print(json.dumps(out, ensure_ascii=False, indent=1))


if __name__ == '__main__':
    main()
