"""T37 do pré-registro (Adendo 16), lado da urna: fração dos eleitores de cada eliminado no 1º turno que a urna põe em Lula e em
Flávio no 2º. Regressão do T8 com grupos para os dois finalistas, empilhada (efeito fixo de local por candidato, erro agrupado por
local), com os quatro grupos somados pelo voto do 1º turno (média ponderada, erro pela covariância).
Uso: python3 -I analisar_eliminados.py <secoes2026.json.gz> <candidatos2026_1t.json.gz> [--chaves lista.txt]
"""
import os as _os, sys as _sys
_sys.path.insert(0, _os.path.dirname(_os.path.abspath(__file__)))
import json, sys
import numpy as np
from lib import carregar, chave_local
from analisar_pres_gov import ols_cluster

GRUPOS = [('Cury', '70'), ('Renan', '14'), ('Caiado', '55'), ('Zema', '30')]
NOMES = [g for g, _ in GRUPOS] + ['demais_outros', 'queda_branco_nulo', 'var_comparecimento', 'adversario_1T', 'proprio_1T']


def main():
    d = carregar(sys.argv[1]); cand = carregar(sys.argv[2])['secoes']
    chaves = set(open(sys.argv[sys.argv.index('--chaves') + 1]).read().split()) if '--chaves' in sys.argv else None
    K = len(NOMES); ys, Xs, fe, cl = [], [], [], []
    peso = np.zeros(len(GRUPOS))
    for k, v in d.items():
        if '1' not in v or '2' not in v or (chaves is not None and k not in chaves):
            continue
        a, b = v['1'], v['2']; cv = cand.get(k, {}); loc = chave_local(k, b)
        g = [cv.get(n, 0) for _, n in GRUPOS]; peso += g
        base = g + [a['O'] - sum(g), (a['B'] + a['N']) - (b['B'] + b['N']), b['comp'] - a['comp']]
        for j, c in enumerate('LR'):
            adv = 'R' if c == 'L' else 'L'
            z = [0.0] * (2 * K); z[j * K:(j + 1) * K] = base + [a[adv], a[c]]
            ys.append(b[c] - a[c]); Xs.append(z); fe.append(loc + '|' + c); cl.append(loc)
    bb, V, N, G = ols_cluster(np.array(ys, float), np.array(Xs, float), fe, cl)
    out = {'linhas': N, 'locais': G, 'por_grupo': {}}
    for i, (nm, _) in enumerate(GRUPOS):
        out['por_grupo'][nm] = {'b_L': [float(bb[i]), float(np.sqrt(V[i, i]))], 'b_F': [float(bb[K + i]), float(np.sqrt(V[K + i, K + i]))],
                                'nenhum_urna': float(1 - bb[i] - bb[K + i])}
    w = peso / peso.sum()
    for lado, off in (('b_L', 0), ('b_F', K)):
        idx = [off + i for i in range(len(GRUPOS))]
        m = float(w @ bb[idx]); se = float(np.sqrt(w @ V[np.ix_(idx, idx)] @ w))
        out[lado + '_somado'] = [m, se]
    out['pesos_1T'] = dict(zip([g for g, _ in GRUPOS], [float(x) for x in w]))
    out['outros_coef'] = {('L:' if j == 0 else 'F:') + n: [float(bb[j * K + i]), float(np.sqrt(V[j * K + i, j * K + i]))]
                          for j in (0, 1) for i, n in enumerate(NOMES) if i >= len(GRUPOS)}
    print(json.dumps(out, ensure_ascii=False, indent=1))


if __name__ == '__main__':
    main()
