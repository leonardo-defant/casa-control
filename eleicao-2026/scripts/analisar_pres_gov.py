"""Adendo 14: presidente contra governador na mesma urna (estrato G, 2º turno de 2026).

1) Decodifica os -bu.dat do 2º turno da pasta e junta com o 1º turno (presidente e governador, com votos por candidato).
2) T5 no 2º turno: beta do branco+nulo de presidente contra o de governador (analisar_pres_gov_nivel.py sobre a base salva), nas 6 UFs.
3) T22 descritivo (AM e DF): variação da fatia de Lula contra a variação da fatia do governador do campo de Lula.
4) T22b: perda dos próprios eleitores do 1º turno, Flávio contra o candidato a governador do campo dele, nas mesmas
   seções (AM 22, DF 11, ES 10). Mesma especificação do T8 para cada cargo, empilhada, com efeito fixo de local por cargo
   e erro agrupado por local (as duas linhas de uma seção caem no mesmo grupo). D = proprio(Flávio) - proprio(aliado).
Uso: python3 -I analisar_pres_gov.py <pasta_bu_2t> <secoes2026_1t.json.gz> <candidatos2026_1t.json.gz> <candidatos_gov_1t.json.gz> <saida_base.json.gz>
"""
import os as _os, sys as _sys
_sys.path.insert(0, _os.path.dirname(_os.path.abspath(__file__)))
import collections, gzip, json, os, sys
import numpy as np
from decodificar import ler_bu, bu_para_secao
from lib import carregar, chave_local

ALIADO_FLAVIO = {'AM': '22', 'DF': '11', 'ES': '10'}
CAMPO_LULA = {'AM': '55', 'DF': '13'}
FINALISTAS = {'AM': ('22', '55'), 'DF': ('11', '13'), 'ES': ('10', '15'), 'RN': ('13', '44'), 'TO': ('44', '45'), 'AC': ('10', '11')}


def secoes(pasta):
    for uf in sorted(os.listdir(pasta)):
        for m in sorted(os.listdir(os.path.join(pasta, uf))):
            for z in sorted(os.listdir(os.path.join(pasta, uf, m))):
                for s in sorted(os.listdir(os.path.join(pasta, uf, m, z))):
                    yield f'{uf.upper()}|{int(m)}|{int(z)}|{int(s)}', os.path.join(pasta, uf, m, z, s)


def montar(pasta, d1):
    base = {}; sem = 0
    for k, p in secoes(pasta):
        bus = sorted(f for f in os.listdir(p) if f.endswith('-bu.dat'))
        if not bus or k not in d1:
            sem += 1; continue
        s, g = bu_para_secao(ler_bu(os.path.join(p, bus[-1])))
        if s is None or g is None:
            sem += 1; continue
        v = dict(d1[k]); v['2'] = s; v['2g'] = g
        base[k] = v
    return base, sem


def ols_cluster(y, X, fe, cl):
    """Efeito fixo por desvio da média do grupo fe; erro CR1 agrupado por cl."""
    _, g = np.unique(fe, return_inverse=True)
    def dm(M):
        out = np.empty_like(M, dtype=float)
        for j in range(M.shape[1]):
            m = np.bincount(g, weights=M[:, j]) / np.bincount(g)
            out[:, j] = M[:, j] - m[g]
        return out
    keep = np.bincount(g)[g] >= 2
    y, X, g2, cl = y[keep], X[keep], g[keep], np.asarray(cl)[keep]
    _, g = np.unique(g2, return_inverse=True)
    Z = dm(np.column_stack([y, X])); yd, Xd = Z[:, 0], Z[:, 1:]
    XtX = Xd.T @ Xd; b = np.linalg.solve(XtX, Xd.T @ yd); e = yd - Xd @ b
    _, c = np.unique(cl, return_inverse=True); G = c.max() + 1
    S = np.zeros((G, X.shape[1]))
    for j in range(X.shape[1]):
        S[:, j] = np.bincount(c, weights=Xd[:, j] * e, minlength=G)
    inv = np.linalg.inv(XtX); N, k = Xd.shape
    V = G / (G - 1) * (N - 1) / (N - k) * inv @ (S.T @ S) @ inv
    return b, V, int(N), int(G)


def t22b(base, cand1, gov1):
    linhas_p, linhas_g = [], []
    for k, v in base.items():
        uf = k.split('|')[0]
        if uf not in ALIADO_FLAVIO or '1' not in v or '1g' not in v:
            continue
        a, b, ag, bg = v['1'], v['2'], v['1g'], v['2g']
        loc = chave_local(k, b)
        # presidente (Flávio = R)
        others_p = a['O']; bn1, bn2 = a['B'] + a['N'] + a.get('c28', 0), b['B'] + b['N']
        dcomp = b['comp'] - a['comp']
        linhas_p.append((loc, b['R'] - a['R'], [others_p, max(0, bn1 - bn2), dcomp, a['L'], a['R']]))
        # governador (aliado de Flávio)
        al, op = ALIADO_FLAVIO[uf], [x for x in FINALISTAS[uf] if x != ALIADO_FLAVIO[uf]][0]
        c1 = gov1.get(k, {}); a1 = c1.get(al, 0); o1 = c1.get(op, 0); out1 = sum(q for n, q in c1.items() if n not in (al, op))
        a2 = bg.get('cand', {}).get(al, 0)
        gbn1, gbn2 = ag['B'] + ag['N'], bg['B'] + bg['N']
        linhas_g.append((loc, a2 - a1, [out1, max(0, gbn1 - gbn2), bg['comp'] - ag['comp'], o1, a1]))
    nomes = ['outros_1T', 'queda_branco_nulo', 'var_comparecimento', 'adversario_1T', 'proprio_1T']
    n = len(linhas_p)
    y = np.array([r[1] for r in linhas_p] + [r[1] for r in linhas_g], float)
    Xp = np.array([r[2] for r in linhas_p], float); Xg = np.array([r[2] for r in linhas_g], float)
    X = np.zeros((2 * n, 10)); X[:n, :5] = Xp; X[n:, 5:] = Xg
    fe = [r[0] + '|p' for r in linhas_p] + [r[0] + '|g' for r in linhas_g]
    cl = [r[0] for r in linhas_p] + [r[0] for r in linhas_g]
    b, V, N, G = ols_cluster(y, X, fe, cl)
    D = b[4] - b[9]; seD = float(np.sqrt(V[4, 4] + V[9, 9] - 2 * V[4, 9]))
    out = {'secoes': n, 'linhas': N, 'locais': G,
           'presidente_Flavio': {nm: [float(b[i]), float(np.sqrt(V[i, i]))] for i, nm in enumerate(nomes)},
           'governador_aliado': {nm: [float(b[5 + i]), float(np.sqrt(V[5 + i, 5 + i]))] for i, nm in enumerate(nomes)},
           'D_proprio_Flavio_menos_aliado': [float(D), seD],
           'veredito': ('SINAL' if D <= -0.03 and -D / seD > 2.5 else 'SEM SINAL' if abs(D) <= 0.015 else 'INCONCLUSIVO')}
    por_uf = {}
    for uf in ALIADO_FLAVIO:
        idx = [i for i, r in enumerate(linhas_p) if r[0].startswith(uf + '|')]
        if len(idx) < 30:
            continue
        ii = np.array(idx + [n + i for i in idx])
        bb, VV, NN, GG = ols_cluster(y[ii], X[ii], [fe[i] for i in ii], [cl[i] for i in ii])
        por_uf[uf] = {'secoes': len(idx), 'locais': GG, 'proprio_Flavio': [float(bb[4]), float(np.sqrt(VV[4, 4]))],
                      'proprio_aliado': [float(bb[9]), float(np.sqrt(VV[9, 9]))],
                      'D': [float(bb[4] - bb[9]), float(np.sqrt(VV[4, 4] + VV[9, 9] - 2 * VV[4, 9]))]}
    out['por_uf'] = por_uf
    return out


def t22(base, gov1):
    res = {}
    for uf, lula_gov in CAMPO_LULA.items():
        fl = ALIADO_FLAVIO[uf]; ys, xs, locs = [], [], []
        for k, v in base.items():
            if not k.startswith(uf + '|') or '1' not in v:
                continue
            a, b, bg = v['1'], v['2'], v['2g']; c1 = gov1.get(k, {})
            g1 = c1.get(lula_gov, 0) + c1.get(fl, 0); g2 = bg.get('cand', {}).get(lula_gov, 0) + bg.get('cand', {}).get(fl, 0)
            if a['L'] + a['R'] <= 0 or b['L'] + b['R'] <= 0 or g1 <= 0 or g2 <= 0:
                continue
            ys.append(100 * (b['L'] / (b['L'] + b['R']) - a['L'] / (a['L'] + a['R'])))
            xs.append(100 * (bg['cand'].get(lula_gov, 0) / g2 - c1.get(lula_gov, 0) / g1)); locs.append(chave_local(k, b))
        y, x = np.array(ys), np.array(xs)
        bcoef, V, N, G = ols_cluster(y, x.reshape(-1, 1), locs, locs)
        res[uf] = {'secoes': len(ys), 'virada_media_lula': float(y.mean()), 'virada_media_governador_campo_lula': float(x.mean()),
                   'inclinacao': float(bcoef[0]), 'ep': float(np.sqrt(V[0, 0])), 'correlacao_bruta': float(np.corrcoef(x, y)[0, 1])}
    return res


def main():
    pasta, base1, cand1, gov1p, saida = sys.argv[1:6]
    d1 = carregar(base1); c1 = carregar(cand1)['secoes']; g1 = carregar(gov1p)['secoes']
    base, sem = montar(pasta, d1)
    with gzip.open(saida, 'wt') as f:
        json.dump(base, f, separators=(',', ':'))
    out = {'secoes_com_bu': len(base), 'secoes_sem_bu_ou_sem_1t': sem,
           'por_uf': dict(collections.Counter(k.split('|')[0] for k in base))}
    import subprocess
    r = subprocess.run([sys.executable, '-I', os.path.join(os.path.dirname(os.path.abspath(__file__)), 'analisar_pres_gov_nivel.py'),
                        saida, '2'], capture_output=True, text=True)
    out['T5_2turno'] = json.loads(r.stdout) if r.returncode == 0 else f'erro: {r.stderr[-500:]}'
    out['T22_descritivo'] = t22(base, g1)
    out['T22b'] = t22b(base, c1, g1)
    print(json.dumps(out, ensure_ascii=False, indent=1))


if __name__ == '__main__':
    main()
