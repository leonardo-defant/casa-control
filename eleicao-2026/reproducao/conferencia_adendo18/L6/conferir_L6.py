"""Conferência independente do L6 (Adendo 18). Código próprio; não importa lib.py nem analisar_L6.py.

Fontes de dados: bweb lido direto dos zips por ler_bweb.py (presidente nos dois turnos, governador no 1º);
base por seção só para conferir os totais e para comparecimento/aptos nas sensibilidades de peso.
Uso: python3 -I conferir_L6.py <bweb1t.json.gz> <bweb2t.json.gz> <secoes2026.json.gz> <lista.json> <saida.json>
"""
import collections, gzip, hashlib, itertools, json, math, sys
import numpy as np

TODAS = ['AC', 'AL', 'AM', 'AP', 'BA', 'CE', 'DF', 'ES', 'GO', 'MA', 'MG', 'MS', 'MT', 'PA', 'PB', 'PE', 'PI', 'PR',
         'RJ', 'RN', 'RO', 'RR', 'RS', 'SC', 'SE', 'SP', 'TO']


def gz(p):
    with gzip.open(p, 'rt') as f:
        return json.load(f)


def media_p(v, w):
    v = np.asarray(v, float); w = np.asarray(w, float)
    return float((v * w).sum() / w.sum())


def sanduiche(y, X, w):
    """MQP; devolve coef, ep clássico, HC0, HC1, HC2, HC3 (implementação própria)."""
    y = np.asarray(y, float); X = np.asarray(X, float); w = np.asarray(w, float)
    n, k = X.shape
    A = X * w[:, None]
    XtWX = X.T @ A
    Bi = np.linalg.inv(XtWX)
    b = Bi @ (A.T @ y)
    e = y - X @ b
    h = w * np.einsum('ij,jk,ik->i', X, Bi, X)
    s2 = (w * e * e).sum() / (n - k)
    out = {'b': b, 'classico': np.sqrt(np.diag(Bi) * s2)}
    for nome, ee in (('HC0', e), ('HC1', e * math.sqrt(n / (n - k))), ('HC2', e / np.sqrt(1 - h)), ('HC3', e / (1 - h))):
        M = (A * ee[:, None]).T @ (A * ee[:, None])
        out[nome] = np.sqrt(np.diag(Bi @ M @ Bi))
    return out


def comparar(F, O, V, W, perm=True):
    vF = [V[u] for u in F]; wF = [W[u] for u in F]; vO = [V[u] for u in O]; wO = [W[u] for u in O]
    d = media_p(vF, wF) - media_p(vO, wO)
    ds = float(np.mean(vF) - np.mean(vO))
    y = np.array(vF + vO); w = np.array(wF + wO); D = np.r_[np.ones(len(F)), np.zeros(len(O))]
    X = np.column_stack([np.ones(len(y)), D])
    s = sanduiche(y, X, w); su = sanduiche(y, X, np.ones(len(y)))
    r = {'n_F': len(F), 'n_O': len(O), 'media_F': media_p(vF, wF), 'media_O': media_p(vO, wO), 'dif': d,
         'dif_conf_regressao': float(s['b'][1]),
         'ep': {k: float(s[k][1]) for k in ('classico', 'HC0', 'HC1', 'HC2', 'HC3')},
         'dif_sem_peso': ds, 'ep_sem_peso': {k: float(su[k][1]) for k in ('classico', 'HC1', 'HC3')}}
    r['leitura'] = 'INCOERÊNCIA' if d >= 0 else ('COERENTE' if d <= -1 else 'INCONCLUSIVO')
    r['leitura_sem_peso'] = 'INCOERÊNCIA' if ds >= 0 else ('COERENTE' if ds <= -1 else 'INCONCLUSIVO')
    if perm:
        todos = F + O; n = len(todos); nf = len(F)
        if math.comb(n, nf) <= 2_000_000:
            v = np.array([V[u] for u in todos]); ww = np.array([W[u] for u in todos])
            combos = np.array(list(itertools.combinations(range(n), nf)), dtype=np.int16)
            sw = ww[combos].sum(1); svw = (v * ww)[combos].sum(1)
            dist = svw / sw - ((v * ww).sum() - svw) / (ww.sum() - sw)
            r['perm'] = {'n': int(len(dist)), 'p_maior_igual': float((dist >= d - 1e-12).mean()),
                         'n_maior_igual': int((dist >= d - 1e-12).sum())}
    return r


def main():
    p1, p2, pbase, plista, saida = sys.argv[1:6]
    raw = open(plista, 'rb').read()
    lista = json.loads(raw)
    sha = hashlib.sha256(raw).hexdigest()
    apoio = {g['uf']: g['apoio_2t'] for g in lista['governadores']}
    imprensa = {g['uf']: g['voto_1t_pct_validos_imprensa'] for g in lista['governadores']}
    b1 = gz(p1); b2 = gz(p2)
    res = {'lista_sha256': sha, 'apoio': apoio}

    # --- totais por UF a partir do bweb
    T = {}
    for uf in TODAS:
        L1 = sum(v[0] for v in b1[uf]['pres'].values()); R1 = sum(v[1] for v in b1[uf]['pres'].values())
        O1 = sum(v[2] for v in b1[uf]['pres'].values())
        L2 = sum(v[0] for v in b2[uf]['pres'].values()); R2 = sum(v[1] for v in b2[uf]['pres'].values())
        O2 = sum(v[2] for v in b2[uf]['pres'].values())
        f1 = L1 / (L1 + R1); f2 = L2 / (L2 + R2)
        T[uf] = {'L1': L1, 'R1': R1, 'O1': O1, 'L2': L2, 'R2': R2, 'O2_deve_ser_0': O2, 'f1': 100 * f1, 'f2': 100 * f2,
                 'virada': 100 * (f2 - f1), 'secoes1': len(b1[uf]['pres']), 'secoes2': len(b2[uf]['pres'])}

    # --- conferência com a base por seção (somas por UF) e comparecimento/aptos para pesos alternativos
    base = gz(pbase)
    B = collections.defaultdict(collections.Counter)
    for k, v in base.items():
        uf = k.split('|')[0]
        for t in ('1', '2'):
            if t in v:
                for c in ('L', 'R', 'O', 'comp', 'apt'):
                    B[uf][c + t] += v[t][c]
    del base
    for uf in TODAS:
        T[uf]['base_igual_bweb'] = all(B[uf][a] == T[uf][a] for a in ('L1', 'R1', 'O1', 'L2', 'R2'))
        T[uf]['comp2'] = B[uf]['comp2']; T[uf]['apt2'] = B[uf]['apt2']; T[uf]['comp1'] = B[uf]['comp1']
        T[uf]['validos1'] = T[uf]['L1'] + T[uf]['R1'] + T[uf]['O1']
        T[uf]['elim_pct_validos1'] = 100 * T[uf]['O1'] / T[uf]['validos1']
        T[uf]['perda_frac_base_F'] = 100 * (T[uf]['f2'] - T[uf]['f1']) / (100 - T[uf]['f1'])
        T[uf]['ganho_frac_base_L'] = 100 * (T[uf]['f2'] - T[uf]['f1']) / T[uf]['f1']
    res['por_uf'] = T

    # --- governador no 1º turno pelo bweb
    G = {}
    for uf in apoio:
        tot = collections.Counter()
        for sec in b1[uf]['gov'].values():
            tot.update(sec)
        nomes = b1[uf]['gov_nomes']
        excl = [n for n, s in nomes.items() if uf == 'RJ' and 'GAROTINHO' in s.upper()]
        nom = sum(q for n, q in tot.items() if n not in excl)
        ven = max((n for n in tot if n not in excl), key=tot.get)
        G[uf] = {'vencedor': nomes[ven], 'pct_bweb': 100 * tot[ven] / nom, 'pct_imprensa': imprensa[uf],
                 'excluidos': [nomes[n] for n in excl], 'numero': ven}
    res['governador_bweb'] = G

    F = sorted(u for u in apoio if apoio[u] == 'Flavio')
    Lu = sorted(u for u in apoio if apoio[u] == 'Lula')
    Ne = sorted(u for u in apoio if apoio[u] == 'neutro')
    fora = [u for u in TODAS if u not in apoio]
    res['grupos'] = {'Flavio': F, 'Lula': Lu, 'neutro': Ne, 'fora_da_lista': fora}
    V = {u: T[u]['virada'] for u in TODAS}
    pesos = {
        'L2+R2 (registro lido como no L2)': {u: T[u]['L2'] + T[u]['R2'] for u in TODAS},
        'L1+R1': {u: T[u]['L1'] + T[u]['R1'] for u in TODAS},
        'comparecimento 2T': {u: T[u]['comp2'] for u in TODAS},
        'aptos 2T': {u: T[u]['apt2'] for u in TODAS},
        'validos 1T (inclui eliminados)': {u: T[u]['validos1'] for u in TODAS},
    }
    W = pesos['L2+R2 (registro lido como no L2)']
    C = {}
    C['principal'] = comparar(F, Lu + Ne, V, W)
    C['pesos_alternativos'] = {k: {kk: vv for kk, vv in comparar(F, Lu + Ne, V, pw, perm=False).items() if kk in ('dif', 'leitura', 'ep')}
                               for k, pw in pesos.items()}
    C['sem_RJ'] = comparar([u for u in F if u != 'RJ'], Lu + Ne, V, W)
    C['demais_todas_UFs'] = comparar(F, Lu + Ne + fora, V, W)
    C['contra_pro_Lula'] = comparar(F, Lu, V, W)
    C['contra_neutras'] = comparar(F, Ne, V, W)
    C['MG_MT_neutros'] = comparar([u for u in F if u not in ('MG', 'MT')], Lu + Ne + ['MG', 'MT'], V, W)
    C['sem_SP'] = comparar([u for u in F if u != 'SP'], Lu + Ne, V, W)
    C['sem_SP_RJ'] = comparar([u for u in F if u not in ('SP', 'RJ')], Lu + Ne, V, W)
    C['so_fora_do_Nordeste_e_AP_contra_resto_fora_NE'] = None
    # leave-one-out: menor diferença ao tirar uma UF qualquer da lista
    loo = {}
    for u in F + Lu + Ne:
        loo[u] = comparar([x for x in F if x != u], [x for x in Lu + Ne if x != u], V, W, perm=False)['dif']
    C['deixa_um_fora'] = {'min': min(loo.values()), 'uf_do_min': min(loo, key=loo.get), 'max': max(loo.values())}
    # simetria
    C['pro_Lula_contra_demais'] = comparar(Lu, F + Ne, V, W)
    # outras escalas (descritivo)
    C['escala_fracao_base_Flavio'] = comparar(F, Lu + Ne, {u: T[u]['perda_frac_base_F'] for u in TODAS}, W)
    C['escala_fracao_base_Lula'] = comparar(F, Lu + Ne, {u: T[u]['ganho_frac_base_L'] for u in TODAS}, W)
    lg = lambda p: math.log(p / (100 - p))
    C['escala_logito'] = comparar(F, Lu + Ne, {u: lg(T[u]['f2']) - lg(T[u]['f1']) for u in TODAS}, W)
    del C['so_fora_do_Nordeste_e_AP_contra_resto_fora_NE']
    res['comparacoes'] = C

    # --- votação do governador (o registro pede a virada "contra a votação do governador"; sem limiar)
    sinal = {'Flavio': 1, 'Lula': -1, 'neutro': 0}
    ul = F + Lu + Ne
    y = np.array([V[u] for u in ul]); w = np.array([W[u] for u in ul])
    gsig = np.array([sinal[apoio[u]] * G[u]['pct_imprensa'] for u in ul])
    s = sanduiche(y, np.column_stack([np.ones(len(ul)), gsig]), w)
    res['votacao_governador'] = {'com_sinal': {'coef': float(s['b'][1]), 'HC1': float(s['HC1'][1]), 'HC3': float(s['HC3'][1])}}
    for nome, grp in (('so_pro_Flavio', F), ('so_pro_Lula', Lu)):
        yy = np.array([V[u] for u in grp]); ww = np.array([W[u] for u in grp]); gg = np.array([G[u]['pct_imprensa'] for u in grp])
        s = sanduiche(yy, np.column_stack([np.ones(len(grp)), gg]), ww)
        res['votacao_governador'][nome] = {'coef': float(s['b'][1]), 'HC1': float(s['HC1'][1]), 'HC3': float(s['HC3'][1])}

    # --- descritivo: controle pela fatia de Lula no 1º turno, com as 27 UFs (mais graus de liberdade que só a lista)
    desc = {}
    for nome, univ in (('lista_21', ul), ('todas_27', TODAS)):
        yy = np.array([V[u] for u in univ]); ww = np.array([W[u] for u in univ])
        D = np.array([1.0 if apoio.get(u) == 'Flavio' else 0.0 for u in univ])
        DL = np.array([1.0 if apoio.get(u) == 'Lula' else 0.0 for u in univ])
        f1 = np.array([T[u]['f1'] for u in univ]); el = np.array([T[u]['elim_pct_validos1'] for u in univ])
        for rot, cols in (('fatia_Lula_1T', [f1]), ('fatia_Lula_1T_quadratica', [f1, f1 ** 2]),
                          ('fatia_e_eliminados', [f1, el])):
            s = sanduiche(yy, np.column_stack([np.ones(len(univ)), D] + cols), ww)
            desc[f'{nome}|{rot}|D_proFlavio'] = {'coef': float(s['b'][1]), 'HC1': float(s['HC1'][1]), 'HC3': float(s['HC3'][1])}
            if nome == 'todas_27':
                s = sanduiche(yy, np.column_stack([np.ones(len(univ)), D, DL] + cols), ww)
                desc[f'{nome}|{rot}|D_proFlavio_e_D_proLula'] = {
                    'coef_F': float(s['b'][1]), 'HC1_F': float(s['HC1'][1]), 'HC3_F': float(s['HC3'][1]),
                    'coef_L': float(s['b'][2]), 'HC1_L': float(s['HC1'][2]), 'HC3_L': float(s['HC3'][2])}
    res['descritivo_controles'] = desc
    json.dump(res, open(saida, 'w'), ensure_ascii=False, indent=1)

    # resumo na tela
    print('lista sha256', sha)
    print('base = bweb em todas as UFs:', all(T[u]['base_igual_bweb'] for u in TODAS), '; votos de outros no 2T:', sum(T[u]['O2_deve_ser_0'] for u in TODAS))
    for u in F + Lu + Ne + fora:
        g = G.get(u)
        print(f"{u} {apoio.get(u, '-'):7s} f1 {T[u]['f1']:6.2f} f2 {T[u]['f2']:6.2f} virada {T[u]['virada']:+.3f}  frac.base F {T[u]['perda_frac_base_F']:5.2f}"
              + (f"  gov {g['vencedor'][:28]:28s} bweb {g['pct_bweb']:6.2f} imprensa {g['pct_imprensa']:6.2f}" if g else ''))
    for k, v in C.items():
        if isinstance(v, dict) and 'dif' in v:
            print(f"[{k}] F {v['media_F']:+.3f} O {v['media_O']:+.3f} dif {v['dif']:+.4f} (reg {v['dif_conf_regressao']:+.4f}) ep HC1 {v['ep']['HC1']:.3f} HC2 {v['ep']['HC2']:.3f} HC3 {v['ep']['HC3']:.3f} clássico {v['ep']['classico']:.3f}"
                  f" | sem peso {v['dif_sem_peso']:+.3f} -> {v['leitura']}/{v['leitura_sem_peso']}" + (f" | perm {v['perm']['n_maior_igual']}/{v['perm']['n']} = {v['perm']['p_maior_igual']:.4f}" if 'perm' in v else ''))
        else:
            print(f'[{k}]', json.dumps(v, ensure_ascii=False))
    print(json.dumps(res['votacao_governador'], ensure_ascii=False))
    for k, v in desc.items():
        print(k, json.dumps({a: round(b, 3) for a, b in v.items()}))


if __name__ == '__main__':
    main()
