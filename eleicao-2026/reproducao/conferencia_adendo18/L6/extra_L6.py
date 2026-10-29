"""Conferência L6, extras (descritivos, post hoc; não mudam o veredito pela letra):
 1) robustez a reclassificação: todas as 3^4 atribuições dos 4 neutros e as 3^2 de MG e MT;
 2) quantas UFs pró-Flávio é preciso mover para neutro para a diferença ficar negativa (pior caso);
 3) fração da base de Flávio sem peso, com ep;
 4) RJ com e sem os votos de Garotinho;
 5) dentro de cada UF, seção por seção: virada contra a votação do governador, com controle pela fatia de Lula
    no 1º turno, efeito fixo de município, peso L2+R2, erro agrupado por município.
Uso: python3 -I extra_L6.py <bweb1t.json.gz> <bweb2t.json.gz> <conferencia_L6.json> <saida.json>
"""
import collections, gzip, itertools, json, math, sys
import numpy as np


def gz(p):
    with gzip.open(p, 'rt') as f:
        return json.load(f)


def wm(v, w):
    return float(np.dot(v, w) / np.sum(w))


def dif(F, O, V, W):
    return wm([V[u] for u in F], [W[u] for u in F]) - wm([V[u] for u in O], [W[u] for u in O])


def fe_cluster(y, X, g, w):
    """MQP com efeito fixo (within) e erro agrupado CR1 pelo mesmo grupo. Implementação própria."""
    _, gi = np.unique(g, return_inverse=True)
    G = gi.max() + 1
    sw = np.bincount(gi, weights=w, minlength=G)
    def dm(z):
        m = np.bincount(gi, weights=w * z, minlength=G) / np.where(sw > 0, sw, 1)
        return z - m[gi]
    yd = dm(y); Xd = np.column_stack([dm(X[:, j]) for j in range(X.shape[1])])
    A = Xd * w[:, None]
    Bi = np.linalg.inv(Xd.T @ A)
    b = Bi @ (A.T @ yd)
    e = yd - Xd @ b
    S = np.column_stack([np.bincount(gi, weights=A[:, j] * e, minlength=G) for j in range(X.shape[1])])
    n, k = Xd.shape
    c = G / (G - 1) * (n - 1) / (n - k - G)
    V = c * Bi @ (S.T @ S) @ Bi
    return b, np.sqrt(np.diag(V)), int(n), int(G)


def main():
    p1, p2, pc, saida = sys.argv[1:5]
    b1 = gz(p1); b2 = gz(p2); C = json.load(open(pc))
    T = C['por_uf']; apoio = C['apoio']; G = C['governador_bweb']
    V = {u: T[u]['virada'] for u in T}; W = {u: T[u]['L2'] + T[u]['R2'] for u in T}
    F0 = [u for u in apoio if apoio[u] == 'Flavio']; L0 = [u for u in apoio if apoio[u] == 'Lula']
    N0 = [u for u in apoio if apoio[u] == 'neutro']
    out = {}

    # 1) reclassificações
    difs = []
    mov = N0 + ['MG', 'MT']
    for atr in itertools.product(['Flavio', 'Lula', 'neutro'], repeat=len(mov)):
        a = dict(apoio); a.update(dict(zip(mov, atr)))
        F = [u for u in a if a[u] == 'Flavio']; O = [u for u in a if a[u] != 'Flavio']
        difs.append((dif(F, O, V, W), atr))
    mn = min(difs)
    out['reclassificacao_neutros_MG_MT'] = {'n': len(difs), 'min_dif': mn[0], 'atribuicao_do_min': dict(zip(mov, mn[1])),
                                            'max_dif': max(difs)[0]}

    # 2) pior caso: mover k UFs pró-Flávio (as de maior virada) para o outro grupo
    pior = {}
    for k in range(1, len(F0)):
        best = None
        for sub in itertools.combinations(F0, k):
            F = [u for u in F0 if u not in sub]; O = L0 + N0 + list(sub)
            d = dif(F, O, V, W)
            if best is None or d < best[0]:
                best = (d, sub)
        pior[k] = {'min_dif': best[0], 'movidas': list(best[1])}
        if best[0] < 0:
            break
    out['pior_caso_mover_pro_Flavio_para_demais'] = pior

    # 3) fração da base de Flávio, sem peso
    fr = {u: T[u]['perda_frac_base_F'] for u in T}
    a = np.array([fr[u] for u in F0]); b = np.array([fr[u] for u in L0 + N0])
    se = math.sqrt(a.var(ddof=1) / len(a) + b.var(ddof=1) / len(b))
    out['fracao_base_Flavio_sem_peso'] = {'media_F': float(a.mean()), 'media_O': float(b.mean()), 'dif': float(a.mean() - b.mean()),
                                          'ep_welch': se, 'sem_SP_RJ_pond': dif([u for u in F0 if u not in ('SP', 'RJ')], L0 + N0, fr, W)}

    # 4) RJ
    tot = collections.Counter()
    for s in b1['RJ']['gov'].values():
        tot.update(s)
    nomes = b1['RJ']['gov_nomes']
    ruas = [n for n, s in nomes.items() if 'RUAS' in s.upper()][0]
    gar = [n for n, s in nomes.items() if 'GAROTINHO' in s.upper()]
    out['RJ'] = {'Ruas_com_Garotinho': 100 * tot[ruas] / sum(tot.values()),
                 'Ruas_sem_Garotinho': 100 * tot[ruas] / (sum(tot.values()) - sum(tot[n] for n in gar)),
                 'Garotinho_pct': 100 * sum(tot[n] for n in gar) / sum(tot.values())}

    # 5) dentro da UF, seção por seção
    dentro = {}
    for uf in sorted(apoio):
        nr = G[uf]['numero']
        ys, gs, fs, ws, ms = [], [], [], [], []
        P1 = b1[uf]['pres']; P2 = b2[uf]['pres']; GV = b1[uf]['gov']
        for k, v1 in P1.items():
            v2 = P2.get(k); gv = GV.get(k)
            if not v2 or not gv:
                continue
            t1 = v1[0] + v1[1]; t2 = v2[0] + v2[1]; tg = sum(q for n, q in gv.items() if not (uf == 'RJ' and 'GAROTINHO' in b1[uf]['gov_nomes'][n].upper()))
            if t1 < 20 or t2 < 20 or tg < 20:
                continue
            f1 = v1[0] / t1
            ys.append(100 * (v2[0] / t2 - f1)); fs.append(100 * f1); gs.append(100 * gv.get(nr, 0) / tg)
            ws.append(t2); ms.append(k.split('|')[1])
        y = np.array(ys); X = np.column_stack([np.array(gs), np.array(fs)]); w = np.array(ws, float)
        bb, ee, n, ng = fe_cluster(y, X, np.array(ms), w)
        dentro[uf] = {'apoio': apoio[uf], 'coef_gov_por_ponto': float(bb[0]), 'ep': float(ee[0]),
                      'coef_fatia_Lula_1T': float(bb[1]), 'n_secoes': n, 'n_municipios': ng}
    out['dentro_da_UF'] = dentro
    # combinação por grupo (média ponderada pelo inverso da variância)
    comb = {}
    for grp in ('Flavio', 'Lula', 'neutro'):
        cs = [(v['coef_gov_por_ponto'], v['ep']) for v in dentro.values() if v['apoio'] == grp]
        wi = np.array([1 / e ** 2 for _, e in cs]); bi = np.array([c for c, _ in cs])
        comb[grp] = {'coef': float((wi * bi).sum() / wi.sum()), 'ep': float(1 / math.sqrt(wi.sum())), 'n_UFs': len(cs),
                     'n_negativos': int((bi < 0).sum())}
    out['dentro_da_UF_combinado'] = comb
    json.dump(out, open(saida, 'w'), ensure_ascii=False, indent=1)
    print(json.dumps({k: v for k, v in out.items() if k != 'dentro_da_UF'}, ensure_ascii=False, indent=1))
    for uf, v in dentro.items():
        print(f"{uf} {v['apoio']:7s} gov {v['coef_gov_por_ponto']:+.4f} (ep {v['ep']:.4f})  fatiaL1 {v['coef_fatia_Lula_1T']:+.4f}  n {v['n_secoes']} mun {v['n_municipios']}")


if __name__ == '__main__':
    main()
