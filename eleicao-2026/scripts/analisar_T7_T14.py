"""T7 e T14 com o bweb completo do 2º turno de 2026 (Adendos 3, 4 e 8), T37 com o bweb (Adendos 16 e 17) e T38 por UF e
município (Adendo 16, descritivo).

T7 (Adendo 3), igual a analisar_fluxos.py: por seção com os dois turnos,
  bolo = outros do 1º turno + queda do branco+nulo (se positiva) + aumento do comparecimento (se positivo);
  excesso = ganho do candidato que mais ganhou (2026 Lula; 2018 Haddad; 2022 Bolsonaro) menos o bolo.
  (a) % das seções com excesso positivo; (b) soma dos excessos positivos como % do ganho total.
  Erro-padrão (o registro não pede; sai ao lado): linearização agrupada por local de votação.
T14 (Adendo 8): coeficiente dos votos do adversário no 1º turno na regressão do T8 (analisar_fluxo_regressao.py), com efeito
  fixo de local, sem peso, erro agrupado por local (lib.fe_ols). Principal: eliminados separados (Cury 70, Renan 14, Caiado 55,
  Zema 30 e demais), como o T8 de 2026 foi registrado; ao lado, outros agregados, como as referências.
T37 (Adendo 16, com a correção do Adendo 17): regressão do T8 com grupos para Lula e Flávio, empilhada (efeito fixo de local por
  candidato, erro agrupado por local), como analisar_eliminados.py; contra a mediana declarada pelos institutos.
T38 (Adendo 16): ganho de Lula e de Flávio entre turnos, em votos e em pontos da fatia dos válidos, por UF e por município, somando
  as seções do bweb; corte pela fatia de Caiado, Renan, Cury e Zema no 1º turno do município.

Uso: python3 -I analisar_T7_T14.py <secoes2026.json.gz> <candidatos2026_1t.json.gz> <secoes2018.json.gz> <secoes2022.json.gz>
        <pasta locais_votacao 2026> <chaves da amostra do 2T> <resultados/> <saida.json> > saida.txt
"""
import os as _os, sys as _sys
_sys.path.insert(0, _os.path.dirname(_os.path.abspath(__file__)))
import collections, csv, gc, glob, json, re, sys, time, warnings
import numpy as np
from lib import carregar, chave_local, fe_ols
from analisar_pres_gov import ols_cluster
import analisar_eliminados as ELIM
warnings.filterwarnings('ignore')

GRUPOS = ELIM.GRUPOS            # [('Cury','70'), ('Renan','14'), ('Caiado','55'), ('Zema','30')]
SEMENTE = 20261029
TROCAS_CAL = [0.0, 0.01, 0.02, 0.035, 0.06]
TABELA_ADENDO4 = {0.0: (5.27, 1.09), 0.01: (8.83, 1.51), 0.02: (12.43, 2.09), 0.035: (19.81, 3.40), 0.06: (35.76, 6.92)}
# colunas da matriz A
C = {n: i for i, n in enumerate(['L1', 'R1', 'O1', 'B1', 'N1', 'comp1', 'L2', 'R2', 'B2', 'N2', 'comp2', 'c28_1', 'O2'])}


def log(*a):
    print('#', time.strftime('%H:%M:%S'), *a, file=sys.stderr, flush=True)


# ---------------------------------------------------------------- dados
def montar(d, cand=None):
    """Matriz por seção com os dois turnos (a mesma regra dos scripts do T7 e do T8) e somas por UF e município com todas as seções
    de cada turno (para o T38)."""
    rows, locs, ufs, keys, grp = [], [], [], [], []
    agg = collections.defaultdict(lambda: np.zeros(8, np.int64))   # L1 R1 V1 L2 R2 elim1 comp1 comp2
    agg_g = collections.defaultdict(lambda: np.zeros(len(GRUPOS), np.int64))
    for k, v in d.items():
        uf, mun = k.split('|')[:2]
        chave_m = (uf, int(mun))
        if '1' in v:
            a = v['1']; s = agg[chave_m]
            s[0] += a['L']; s[1] += a['R']; s[2] += a['L'] + a['R'] + a['O'] - a.get('c28', 0); s[6] += a['comp']
            if cand is not None:
                cv = cand.get(k, {}); gg = [cv.get(n, 0) for _, n in GRUPOS]
                agg_g[chave_m] += gg; s[5] += sum(gg)
        if '2' in v:
            b = v['2']; s = agg[chave_m]; s[3] += b['L']; s[4] += b['R']; s[7] += b['comp']
        if '1' not in v or '2' not in v:
            continue
        a, b = v['1'], v['2']
        rows.append([a['L'], a['R'], a['O'], a['B'], a['N'], a['comp'], b['L'], b['R'], b['B'], b['N'], b['comp'],
                     a.get('c28', 0), b['O']])
        if cand is not None:
            cv = cand.get(k, {}); grp.append([cv.get(n, 0) for _, n in GRUPOS])
        locs.append(chave_local(k, b)); ufs.append(uf); keys.append(k)
    A = np.array(rows, np.int64)
    _, loc_id = np.unique(np.array(locs), return_inverse=True)
    out = {'A': A, 'loc': loc_id, 'uf': np.array(ufs), 'keys': np.array(keys), 'agg': dict(agg), 'agg_g': dict(agg_g)}
    if cand is not None:
        out['G'] = np.array(grp, np.int64)
    return out


# ---------------------------------------------------------------- T7
def se_cluster_ratio(num, den, cl):
    """Erro-padrão por linearização agrupada de R = soma(num)/soma(den)."""
    R = num.sum() / den.sum()
    G = cl.max() + 1
    u = np.bincount(cl, weights=num - R * den, minlength=G)
    u = u[np.bincount(cl, minlength=G) > 0]; g = len(u)
    return float(np.sqrt(g / (g - 1) * (u ** 2).sum()) / den.sum())


def t7(B, c, mask=None, extra=None):
    """Igual a analisar_fluxos.py. extra: votos somados ao ganho do candidato no 2T (troca simulada)."""
    A, cl = B['A'], B['loc']
    if mask is not None:
        A, cl = A[mask], cl[mask]
    adv = 'R' if c == 'L' else 'L'
    g = (A[:, C[c + '2']] - A[:, C[c + '1']]).astype(float)
    if extra is not None:
        g = g + (extra if mask is None else extra[mask])
    queda = (A[:, C['B1']] + A[:, C['N1']]) - (A[:, C['B2']] + A[:, C['N2']])
    aum = A[:, C['comp2']] - A[:, C['comp1']]
    bolo = A[:, C['O1']] + np.maximum(0, queda) + np.maximum(0, aum)
    e = g - bolo
    pos = e > 0
    n = len(g); ganho = g.sum(); exc = e[pos].sum()
    _, cl = np.unique(cl, return_inverse=True)
    r = {'secoes': int(n), 'ganho_total': float(ganho), 'bolo_total': int(bolo.sum()),
         'pct_secoes_excesso': 100 * pos.sum() / n, 'excesso_total': float(exc),
         'pct_ganho_em_excesso': 100 * exc / ganho if ganho else None,
         'pct_secoes_adversario_perdeu_votos': 100 * (A[:, C[adv + '2']] < A[:, C[adv + '1']]).sum() / n,
         'secoes_sem_bolo': int((bolo <= 2).sum()), 'ganho_nas_secoes_sem_bolo': float(g[bolo <= 2].sum())}
    r['ep_pct_secoes_excesso'] = 100 * se_cluster_ratio(pos.astype(float), np.ones(n), cl)
    r['ep_pct_ganho_em_excesso'] = 100 * se_cluster_ratio(np.where(pos, e, 0.0), g, cl) if ganho else None
    return r


def t7_por_faixa(B, c, mask=None):
    """Descritivo: (a) e (b) por faixa da fatia do adversário nos votos válidos do 1º turno da seção."""
    A = B['A'] if mask is None else B['A'][mask]
    adv = 'R' if c == 'L' else 'L'
    val = A[:, C['L1']] + A[:, C['R1']] + A[:, C['O1']] - A[:, C['c28_1']]
    fat = np.where(val > 0, A[:, C[adv + '1']] / np.maximum(val, 1), np.nan)
    out = {}
    for lo, hi in [(0, .35), (.35, .50), (.50, .65), (.65, 1.01)]:
        m = (fat >= lo) & (fat < hi)
        mm = m if mask is None else _expand(mask, m)
        r = t7(B, c, mm)
        out[f'{int(100*lo)}-{int(100*hi) if hi < 1 else 100}'] = {k: r[k] for k in ('secoes', 'pct_secoes_excesso', 'ep_pct_secoes_excesso',
                                                                                  'pct_ganho_em_excesso', 'ep_pct_ganho_em_excesso')}
    return out


def _expand(mask, sub):
    full = np.zeros(len(mask), bool); full[np.where(mask)[0][sub]] = True
    return full


def calibracao_t7(B, c, rng):
    """Adendo 4, refeito para conferir a tabela registrada: troca uniforme de uma fração s dos votos do adversário no 2T para o
    candidato. Duas versões: valor esperado (s vezes os votos) e sorteio binomial por seção."""
    adv = 'R' if c == 'L' else 'L'
    adv2 = B['A'][:, C[adv + '2']]
    out = {}
    for s in TROCAS_CAL:
        r_e = t7(B, c, extra=s * adv2.astype(float))
        r_b = t7(B, c, extra=rng.binomial(adv2, s).astype(float))
        out[f'{s:.3f}'] = {'valor_esperado': [r_e['pct_secoes_excesso'], r_e['pct_ganho_em_excesso']],
                           'binomial': [r_b['pct_secoes_excesso'], r_b['pct_ganho_em_excesso']],
                           'tabela_registrada': list(TABELA_ADENDO4[s])}
    return out


# ---------------------------------------------------------------- T8 / T14
def t8(B, c, grupos, mask=None):
    A = B['A']; adv = 'R' if c == 'L' else 'L'
    y = A[:, C[c + '2']] - A[:, C[c + '1']]
    rabo = [(A[:, C['B1']] + A[:, C['N1']]) - (A[:, C['B2']] + A[:, C['N2']]), A[:, C['comp2']] - A[:, C['comp1']],
            A[:, C[adv + '1']], A[:, C[c + '1']]]
    if grupos:
        Gm = B['G']
        X = np.column_stack([Gm, A[:, C['O1']] - Gm.sum(1)] + rabo)
        nomes = [g for g, _ in GRUPOS] + ['demais_outros']
    else:
        X = np.column_stack([A[:, C['O1']]] + rabo); nomes = ['outros_1T']
    nomes += ['queda_branco_nulo', 'var_comparecimento', 'adversario_1T', 'proprio_1T']
    loc = B['loc']
    if mask is not None:
        y, X, loc = y[mask], X[mask], loc[mask]
    r = fe_ols(y.astype(float), X.astype(float), loc, None, nomes)
    return {'candidato': c, 'secoes': int(len(y)), 'n_informativas': r['n'], 'locais': r['grupos'], 'coef': r['coef'], 'ep': r['ep']}


# ---------------------------------------------------------------- T37
def t37_urna(B, mask=None):
    """Igual a analisar_eliminados.py (linhas empilhadas em outra ordem, o que não muda a estimativa)."""
    A, Gm, loc = B['A'], B['G'], B['loc']
    if mask is not None:
        A, Gm, loc = A[mask], Gm[mask], loc[mask]
    K = len(ELIM.NOMES); n = len(A)
    base = np.column_stack([Gm, A[:, C['O1']] - Gm.sum(1), (A[:, C['B1']] + A[:, C['N1']]) - (A[:, C['B2']] + A[:, C['N2']]),
                            A[:, C['comp2']] - A[:, C['comp1']]]).astype(float)
    XL = np.column_stack([base, A[:, C['R1']], A[:, C['L1']]]); XR = np.column_stack([base, A[:, C['L1']], A[:, C['R1']]])
    X = np.zeros((2 * n, 2 * K)); X[:n, :K] = XL; X[n:, K:] = XR
    y = np.concatenate([A[:, C['L2']] - A[:, C['L1']], A[:, C['R2']] - A[:, C['R1']]]).astype(float)
    fe = np.concatenate([2 * loc, 2 * loc + 1]); cl = np.concatenate([loc, loc])
    bb, V, N, Gc = ols_cluster(y, X, fe, cl)
    peso = Gm.sum(0).astype(float)
    out = {'linhas': N, 'locais': Gc, 'por_grupo': {}, '_V': V}
    for i, (nm, _) in enumerate(GRUPOS):
        out['por_grupo'][nm] = {'b_L': [float(bb[i]), float(np.sqrt(V[i, i]))], 'b_F': [float(bb[K + i]), float(np.sqrt(V[K + i, K + i]))],
                                'nenhum_urna': float(1 - bb[i] - bb[K + i])}
    w = peso / peso.sum()
    for lado, off in (('b_L', 0), ('b_F', K)):
        idx = [off + i for i in range(len(GRUPOS))]
        out[lado + '_somado'] = [float(w @ bb[idx]), float(np.sqrt(w @ V[np.ix_(idx, idx)] @ w))]
    out['pesos_1T'] = dict(zip([g for g, _ in GRUPOS], [float(x) for x in w]))
    out['votos_1T_grupos'] = dict(zip([g for g, _ in GRUPOS], [int(x) for x in peso]))
    out['outros_coef'] = {('L:' if j == 0 else 'F:') + nm: [float(bb[j * K + i]), float(np.sqrt(V[j * K + i, j * K + i]))]
                          for j in (0, 1) for i, nm in enumerate(ELIM.NOMES) if i >= len(GRUPOS)}
    return out


# Cruzamentos voto no 1º turno x intenção no 2º turno, do arquivo verificado (resultados/contexto_2t_2026_pesquisa_verificada.json):
# para cada instituto, a última rodada antes de 25/10 que publicou o cruzamento por candidato eliminado; (f, l) em fração.
DECLARADO = {
    'PoderData 23-24/10': {'Cury': (.58, .29), 'Renan': (.43, .33), 'Caiado': (.46, .30)},
    'Quaest 17-20/10': {'Cury': (.33, .48), 'Renan': (.51, .25), 'Caiado': (.57, .21)},
    'AtlasIntel 13-18/10': {'Cury': (.424, .521), 'Renan': (.335, .319), 'Caiado': (.698, .245)},
    'Ipespe 13-15/10': {'Cury': (.50, .31), 'Renan': (.40, .20), 'Caiado': (.59, .18)},
    'Nexus 10-12/10': {'Caiado': (.55, .27), 'Zema': (.80, .12)},
}
IDEIA = {'Ideia (rodada não confirmada)': {'Cury': (.36, .48)}}
DATAFOLHA_AGREGADO = ('Datafolha 13-14/10 (só o agregado dos quatro)', .46, .27)


def mediana_declarada(fontes):
    med = {}
    for g, _ in GRUPOS:
        vals = [v[g] for v in fontes.values() if g in v]
        if vals:
            f = np.median([x[0] for x in vals]); l = np.median([x[1] for x in vals]); n = np.median([1 - x[0] - x[1] for x in vals])
            med[g] = {'f': float(f), 'l': float(l), 'n': float(n), 'institutos': [k for k, v in fontes.items() if g in v]}
    return med


def t37_letra(urna, med):
    """Medidas do registro, com os quatro grupos somados pelo voto do 1º turno. Grupo sem dado declarado sai e os pesos são
    renormalizados (declarado e urna com os mesmos grupos)."""
    K = len(ELIM.NOMES)
    gs = [g for g, _ in GRUPOS if g in med]
    w = np.array([urna['pesos_1T'][g] for g in gs]); w = w / w.sum()
    bL = np.array([urna['por_grupo'][g]['b_L'][0] for g in gs]); bF = np.array([urna['por_grupo'][g]['b_F'][0] for g in gs])
    l = float(w @ [med[g]['l'] for g in gs]); f = float(w @ [med[g]['f'] for g in gs]); n = float(w @ [med[g]['n'] for g in gs])
    V = urna['_V']; idx = [ [g for g, _ in GRUPOS].index(x) for x in gs]
    seL = float(np.sqrt(w @ V[np.ix_(idx, idx)] @ w)); seF = float(np.sqrt(w @ V[np.ix_([K + i for i in idx], [K + i for i in idx])] @ w))
    dL = float(w @ bL) - l; dF = float(w @ bF) - f
    zL0, zF0 = dL / seL, dF / seF
    # leituras de "a mais de 2,5 erros-padrão": de zero (principal) e do próprio limiar (ao lado)
    A_ = abs(dF) <= 0.07 and dL >= 0.15 and zL0 > 2.5
    B_ = dF <= -0.07 and dL >= 0.07 and zF0 < -2.5 and zL0 > 2.5
    S_ = abs(dF) <= 0.07 and abs(dL) <= 0.07
    letra = 'padrão da forma A' if A_ else 'padrão da forma B' if B_ else 'sem padrão de fraude' if S_ else 'inconclusivo'
    A2 = abs(dF) <= 0.07 and dL >= 0.15 and (dL - 0.15) / seL > 2.5
    B2 = dF <= -0.07 and dL >= 0.07 and (dF + 0.07) / seF < -2.5 and (dL - 0.07) / seL > 2.5
    letra2 = 'padrão da forma A' if A2 else 'padrão da forma B' if B2 else 'sem padrão de fraude' if S_ else 'inconclusivo'
    return {'grupos_usados': gs, 'pesos': dict(zip(gs, w.tolist())), 'b_L': float(w @ bL), 'ep_b_L': seL, 'b_F': float(w @ bF), 'ep_b_F': seF,
            'l_declarado': l, 'f_declarado': f, 'n_declarado': n, 'dL': dL, 'dF': dF, 'z_dL_de_zero': zL0, 'z_dF_de_zero': zF0,
            'z_dL_do_limiar_0.15': (dL - 0.15) / seL, 'z_dL_do_limiar_0.07': (dL - 0.07) / seL, 'z_dF_do_limiar_-0.07': (dF + 0.07) / seF,
            'letra_z_de_zero': letra, 'letra_z_do_limiar': letra2, 'soma_dL_dF': dL + dF}


def t37_post_hoc(urna, fontes):
    """Comparação post hoc (Adendo 17): fatia de Lula entre os que escolheram um finalista, por instituto, pesos do 1º turno."""
    out = {}
    for inst, v in fontes.items():
        gs = [g for g, _ in GRUPOS if g in v]
        w = np.array([urna['pesos_1T'][g] for g in gs]); w = w / w.sum()
        l = w @ [v[g][1] for g in gs]; f = w @ [v[g][0] for g in gs]
        bL = w @ [urna['por_grupo'][g]['b_L'][0] for g in gs]
        out[inst] = {'grupos': gs, 'declarado_lula_entre_finalistas': float(l / (l + f)), 'urna_mesmos_grupos': float(bL)}
    return out


# ---------------------------------------------------------------- T38
def nomes_municipios(pasta):
    nomes = {}
    for f in sorted(glob.glob(_os.path.join(pasta, 'eleitorado_local_votacao_2026_??.csv'))):
        with open(f, encoding='latin1', newline='') as fh:
            r = csv.reader(fh, delimiter=';'); h = next(r); iu, ic, im = h.index('SG_UF'), h.index('CD_MUNICIPIO'), h.index('NM_MUNICIPIO')
            for row in r:
                nomes[(row[iu], int(row[ic]))] = row[im]
    return nomes


def ols_simples(y, X, w=None, cl=None):
    X = np.column_stack([np.ones(len(y)), X]); w = np.ones(len(y)) if w is None else w
    sw = np.sqrt(w); Xw, yw = X * sw[:, None], y * sw
    XtX = Xw.T @ Xw; b = np.linalg.solve(XtX, Xw.T @ yw); e = y - X @ b
    inv = np.linalg.inv(XtX); N, k = X.shape
    if cl is None:
        S = (Xw * (e * sw)[:, None]); meat = S.T @ S; c = N / (N - k)
    else:
        _, g = np.unique(cl, return_inverse=True); G = g.max() + 1
        S = np.zeros((G, k))
        for j in range(k):
            S[:, j] = np.bincount(g, weights=w * X[:, j] * e, minlength=G)
        meat = S.T @ S; c = G / (G - 1) * (N - 1) / (N - k)
    V = c * inv @ meat @ inv
    return b, np.sqrt(np.diag(V))


def t38(B, nomes, cand_ok):
    agg, agg_g = B['agg'], B['agg_g']
    # por UF (com o exterior como ZZ)
    por_uf = collections.defaultdict(lambda: np.zeros(8, np.int64)); por_uf_g = collections.defaultdict(lambda: np.zeros(len(GRUPOS), np.int64))
    for (uf, m), s in agg.items():
        por_uf[uf] += s
        if cand_ok and (uf, m) in agg_g:
            por_uf_g[uf] += agg_g[(uf, m)]
    def linha(s, gg):
        L1, R1, V1, L2, R2, E1 = (float(x) for x in s[:6])
        pL = 100 * (L2 / (L2 + R2) - L1 / V1); pR = 100 * (R2 / (L2 + R2) - R1 / V1)
        r = {'L1': int(L1), 'R1': int(R1), 'V1': int(V1), 'L2': int(L2), 'R2': int(R2), 'gL': int(L2 - L1), 'gR': int(R2 - R1),
             'pL': pL, 'pR': pR, 'F_menos_L_pontos': pR - pL, 'elim_pct_V1': 100 * E1 / V1,
             'comp1': int(s[6]), 'comp2': int(s[7])}
        if gg is not None:
            r['grupos_pct_V1'] = {g: 100 * float(x) / V1 for (g, _), x in zip(GRUPOS, gg)}
        return r
    ufs = {uf: linha(s, por_uf_g.get(uf)) for uf, s in por_uf.items()}
    # por município (só o Brasil, como no T38 anterior)
    mun = []
    for (uf, m), s in agg.items():
        if uf == 'ZZ' or s[2] <= 0 or s[3] + s[4] <= 0:
            continue
        r = linha(s, agg_g.get((uf, m)) if cand_ok else None); r.update({'uf': uf, 'mun': m, 'nome': nomes.get((uf, m), '')})
        mun.append(r)
    n = len(mun)
    mais_votos = [r for r in mun if r['gR'] > r['gL']]; mais_pontos = [r for r in mun if r['pR'] > r['pL']]
    vir_L = [r for r in mun if r['R1'] > r['L1'] and r['L2'] > r['R2']]; vir_F = [r for r in mun if r['L1'] > r['R1'] and r['R2'] > r['L2']]
    res = {'por_UF': dict(sorted(ufs.items(), key=lambda kv: kv[1]['F_menos_L_pontos'], reverse=True)),
           'UFs_flavio_mais_votos': [u for u, r in ufs.items() if r['gR'] > r['gL']],
           'UFs_flavio_mais_pontos': [u for u, r in ufs.items() if r['pR'] > r['pL']],
           'UFs_flavio_perdeu_votos': {u: r['gR'] for u, r in ufs.items() if r['gR'] < 0},
           'municipios': n, 'soma_L2': sum(r['L2'] for r in mun), 'soma_R2': sum(r['R2'] for r in mun),
           'flavio_mais_votos_que_lula': len(mais_votos), 'lula_mais_votos_que_flavio': sum(r['gL'] > r['gR'] for r in mun),
           'empates_no_ganho': sum(r['gL'] == r['gR'] for r in mun), 'flavio_mais_pontos_que_lula': len(mais_pontos),
           'viraram_de_flavio_para_lula': len(vir_L), 'viraram_de_lula_para_flavio': len(vir_F),
           'lista_viraram_para_flavio': [{k: r[k] for k in ('uf', 'mun', 'nome', 'L1', 'R1', 'L2', 'R2')} for r in vir_F],
           'saldo_flavio_nas_cidades_em_que_ganhou_mais_votos': sum(r['gR'] - r['gL'] for r in mais_votos),
           'por_UF_municipios_[n,mais_votos,mais_pontos,viraram_p_Lula,viraram_p_Flavio]': {},
           'lista_flavio_mais_pontos': sorted(({k: r[k] for k in ('uf', 'mun', 'nome', 'gL', 'gR', 'pL', 'pR')} for r in mais_pontos),
                                              key=lambda r: r['pL'] - r['pR'])}
    pu = collections.defaultdict(lambda: [0, 0, 0, 0, 0])
    for r in mun:
        u = pu[r['uf']]; u[0] += 1; u[1] += r['gR'] > r['gL']; u[2] += r['pR'] > r['pL']
        u[3] += r['R1'] > r['L1'] and r['L2'] > r['R2']; u[4] += r['L1'] > r['R1'] and r['R2'] > r['L2']
    res['por_UF_municipios_[n,mais_votos,mais_pontos,viraram_p_Lula,viraram_p_Flavio]'] = dict(sorted(pu.items()))
    if cand_ok:
        dif = np.array([r['F_menos_L_pontos'] for r in mun]); el = np.array([r['elim_pct_V1'] for r in mun])
        V1 = np.array([r['V1'] for r in mun], float); ufm = np.array([r['uf'] for r in mun])
        faixas = {}
        for lo, hi in [(0, 4), (4, 6), (6, 8), (8, 10), (10, 15), (15, 101)]:
            m = (el >= lo) & (el < hi)
            if m.sum():
                faixas[f'{lo}-{hi if hi < 101 else 100}'] = {'cidades': int(m.sum()), 'media_F_menos_L': float(dif[m].mean()),
                                                              'media_ponderada_V1': float((dif[m] * V1[m]).sum() / V1[m].sum()),
                                                              'pct_flavio_mais_pontos': float(100 * (dif[m] > 0).mean())}
        q = np.quantile(el, [0, .2, .4, .6, .8, 1.0]); quint = {}
        for i in range(5):
            m = (el >= q[i]) & ((el < q[i + 1]) if i < 4 else (el <= q[i + 1]))
            quint[f'Q{i+1} ({q[i]:.1f} a {q[i+1]:.1f})'] = {'cidades': int(m.sum()), 'media_F_menos_L': float(dif[m].mean()),
                                                           'media_ponderada_V1': float((dif[m] * V1[m]).sum() / V1[m].sum()),
                                                           'pct_flavio_mais_pontos': float(100 * (dif[m] > 0).mean())}
        b1, s1 = ols_simples(dif, el[:, None], cl=ufm); b2, s2 = ols_simples(dif, el[:, None], w=V1, cl=ufm)
        Xg = np.array([[r['grupos_pct_V1'][g] for g, _ in GRUPOS] + [100 * r['R1'] / r['V1']] for r in mun])
        b3, s3 = ols_simples(dif, Xg, cl=ufm)
        m15 = el >= 15
        por_uf15 = collections.Counter(ufm[m15].tolist())
        res['cidades_eliminados_15pct_ou_mais_por_UF'] = dict(por_uf15.most_common())
        res['corte_eliminados_municipio'] = {
            'faixas_fixas_pct_V1': faixas, 'quintis': quint, 'correlacao': float(np.corrcoef(dif, el)[0, 1]),
            'inclinacao_sem_peso_por_ponto': [float(b1[1]), float(s1[1])], 'inclinacao_peso_V1_por_ponto': [float(b2[1]), float(s2[1])],
            'multipla_sem_peso_[Cury,Renan,Caiado,Zema,Flavio1T]': {'coef': b3[1:].tolist(), 'ep_agrupado_UF': s3[1:].tolist()}}
        u_ = [r for u, r in ufs.items() if u != 'ZZ']
        res['corte_eliminados_UF_correlacao'] = float(np.corrcoef([r['F_menos_L_pontos'] for r in u_], [r['elim_pct_V1'] for r in u_])[0, 1])
    return res


# ---------------------------------------------------------------- critérios
def veredito_t7(a, b, amax, bmax):
    if a > amax + 5 and b > bmax + 5:
        return 'SINAL'
    if a <= amax + 2 and b <= bmax + 2:
        return 'SEM SINAL'
    return 'INCONCLUSIVO'


def veredito_t14(b, se):
    if b > 0.071 and (b - 0.071) / se > 3:
        return 'SINAL'
    if b <= 0.051:
        return 'SEM SINAL'
    return 'INCONCLUSIVO'


def interp_troca(v, col):
    """Descritivo: troca equivalente pela tabela do Adendo 4 (calibração de 2022), interpolação linear."""
    ss = sorted(TABELA_ADENDO4); ys = [TABELA_ADENDO4[s][col] for s in ss]
    if v <= ys[0]:
        return 0.0
    return float(np.interp(v, ys, ss)) if v <= ys[-1] else float('nan')


def main():
    a26, cand26, a18, a22, pasta_locais, chaves_am, pasta_res, saida = sys.argv[1:9]
    rng = np.random.default_rng(SEMENTE)
    res = {'teste': 'T7_T14 (mais T37 e T38)', 'registro': 'PRE-REGISTRO-2026-10-26.md, Adendos 3, 4, 8, 16 e 17', 'semente': SEMENTE,
           'referencias': {}}
    # 1) referências
    for ano, arq, c, outro in (('2018', a18, 'L', 'R'), ('2022', a22, 'R', 'L')):
        log('carregando', ano); d = carregar(arq); B = montar(d); del d; gc.collect()
        r = {'T7_ganhador': t7(B, c), 'T7_outro_finalista_descritivo': t7(B, outro), 'T7_por_faixa_adversario': t7_por_faixa(B, c),
             'T8_ganhador_sem_grupos': t8(B, c, False)}
        if ano == '2022':
            r['T7_calibracao_troca_refeita'] = calibracao_t7(B, c, rng)
        res['referencias'][ano] = r
        log(ano, 'T7', round(r['T7_ganhador']['pct_secoes_excesso'], 3), round(r['T7_ganhador']['pct_ganho_em_excesso'], 3),
            'T14', round(r['T8_ganhador_sem_grupos']['coef']['adversario_1T'], 4))
        del B; gc.collect()
    # 2) 2026
    log('carregando 2026'); cand = carregar(cand26)['secoes']; d = carregar(a26)
    B = montar(d, cand); del d, cand; gc.collect()
    zz = B['uf'] == 'ZZ'
    am = set(open(chaves_am).read().split()); mam = np.array([k in am for k in B['keys']])
    r26 = {'secoes_com_os_dois_turnos': int(len(B['A'])), 'secoes_amostra_encontradas': int(mam.sum())}
    r26['T7_Lula'] = t7(B, 'L')
    r26['T7_Lula_sem_exterior'] = t7(B, 'L', ~zz)
    r26['T7_Lula_amostra_conferencia'] = t7(B, 'L', mam)
    r26['T7_Flavio_descritivo'] = t7(B, 'R')
    r26['T7_por_faixa_adversario'] = t7_por_faixa(B, 'L')
    r26['T7_por_UF'] = {u: {k: v for k, v in t7(B, 'L', B['uf'] == u).items() if k in ('secoes', 'pct_secoes_excesso', 'pct_ganho_em_excesso',
                                                                                       'ganho_total', 'excesso_total')}
                        for u in sorted(set(B['uf']))}
    log('T7 2026', round(r26['T7_Lula']['pct_secoes_excesso'], 3), round(r26['T7_Lula']['pct_ganho_em_excesso'], 3))
    r26['T14_com_grupos'] = t8(B, 'L', True)
    r26['T14_sem_grupos'] = t8(B, 'L', False)
    r26['T14_com_grupos_sem_exterior'] = t8(B, 'L', True, ~zz)
    r26['T14_com_grupos_amostra_conferencia'] = t8(B, 'L', True, mam)
    r26['T8_Flavio_com_grupos'] = t8(B, 'R', True)
    log('T14 2026', r26['T14_com_grupos']['coef']['adversario_1T'], r26['T14_com_grupos']['ep']['adversario_1T'])
    # T37
    u = t37_urna(B)
    ua = t37_urna(B, mam)
    fontes = dict(DECLARADO)
    med = mediana_declarada(fontes); med_ideia = mediana_declarada({**fontes, **IDEIA}); med_pd = mediana_declarada({'PoderData 23-24/10': DECLARADO['PoderData 23-24/10']})
    r26['T37'] = {'urna': {k: v for k, v in u.items() if k != '_V'}, 'urna_amostra_conferencia': {k: v for k, v in ua.items() if k != '_V'},
                  'declarado_fontes': {k: {g: {'f': x[0], 'l': x[1], 'n': round(1 - x[0] - x[1], 3)} for g, x in v.items()} for k, v in fontes.items()},
                  'mediana_declarada': med,
                  'letra_principal': t37_letra(u, med),
                  'letra_com_Ideia': t37_letra(u, med_ideia),
                  'letra_so_PoderData_final': t37_letra(u, med_pd),
                  'post_hoc_lula_entre_finalistas': t37_post_hoc(u, {**fontes, **IDEIA}),
                  'post_hoc_datafolha_agregado': {'declarado': DATAFOLHA_AGREGADO[2] / (DATAFOLHA_AGREGADO[1] + DATAFOLHA_AGREGADO[2]),
                                                   'urna_quatro_grupos': u['b_L_somado'][0]}}
    log('T37', u['b_L_somado'], u['b_F_somado'])
    # T38
    nomes = nomes_municipios(pasta_locais)
    r26['T38'] = t38(B, nomes, True)
    del B; gc.collect()
    res['2026'] = r26

    # 3) conferências com resultados anteriores
    conf = {}
    ref_txt = open(_os.path.join(pasta_res, 'T7_referencias.txt')).read()
    for ano, nm in (('2018', 'Haddad'), ('2022', 'Bolsonaro')):
        reg = json.loads(re.search(rf'{ano} {nm}: (\{{.*\}})', ref_txt).group(1))
        mine = res['referencias'][ano]['T7_ganhador']
        conf[f'T7_{ano}_igual_ao_registrado'] = all(abs(reg[k] - mine[k]) < 1e-9 for k in reg)
    am_txt = open(_os.path.join(pasta_res, 'T7_T8_T14_amostra.txt')).read()
    reg_am = json.loads(am_txt.split('== T7')[1].strip().splitlines()[0])
    conf['T7_amostra_igual'] = all(abs(reg_am[k] - r26['T7_Lula_amostra_conferencia'][k]) < 1e-9 for k in reg_am)
    t37a = json.load(open(_os.path.join(pasta_res, 'T37_eliminados_urna_amostra.json')))
    conf['T37_amostra_b_L_somado'] = [t37a['b_L_somado'][0], ua['b_L_somado'][0]]
    conf['T14_amostra_com_grupos_registrado_0.0507'] = r26['T14_com_grupos_amostra_conferencia']['coef']['adversario_1T']
    conf['T14_2018_calibracao_0.0063'] = res['referencias']['2018']['T8_ganhador_sem_grupos']['coef']['adversario_1T']
    conf['T14_2022_calibracao_0.0377'] = res['referencias']['2022']['T8_ganhador_sem_grupos']['coef']['adversario_1T']
    t38a = json.load(open(_os.path.join(pasta_res, 'T38_municipios.json')))
    chk = ('municipios', 'soma_L2', 'soma_R2', 'flavio_mais_votos_que_lula', 'flavio_mais_pontos_que_lula', 'viraram_de_flavio_para_lula',
           'viraram_de_lula_para_flavio')
    conf['T38_municipios_igual_ao_oficial'] = {k: [t38a[k], r26['T38'][k]] for k in chk}
    uf_txt = open(_os.path.join(pasta_res, 'T38_pontos_por_uf.txt')).read()
    dif_uf = []
    for m in re.finditer(r'^([A-Z]{2}) \| ([+-][\d,]+) \| ([+-][\d,]+) \|', uf_txt, re.M):
        uf, gl, gr = m.group(1), int(m.group(2).replace(',', '')), int(m.group(3).replace(',', ''))
        x = r26['T38']['por_UF'][uf]
        if (x['gL'], x['gR']) != (gl, gr):
            dif_uf.append([uf, gl, gr, x['gL'], x['gR']])
    conf['T38_UF_diferencas_contra_totais_oficiais'] = dif_uf
    res['conferencias'] = conf

    # 4) critérios
    R = res['referencias']
    amax = max(R[a]['T7_ganhador']['pct_secoes_excesso'] for a in R); bmax = max(R[a]['T7_ganhador']['pct_ganho_em_excesso'] for a in R)
    t = r26['T7_Lula']
    v7 = veredito_t7(t['pct_secoes_excesso'], t['pct_ganho_em_excesso'], amax, bmax)
    b14, s14 = r26['T14_com_grupos']['coef']['adversario_1T'], r26['T14_com_grupos']['ep']['adversario_1T']
    v14 = veredito_t14(b14, s14)
    b14s, s14s = r26['T14_sem_grupos']['coef']['adversario_1T'], r26['T14_sem_grupos']['ep']['adversario_1T']
    res['criterios'] = {'T7': {'maior_a_ref': amax, 'maior_b_ref': bmax, 'limite_sinal_a': amax + 5, 'limite_sinal_b': bmax + 5,
                               'limite_sem_sinal_a': amax + 2, 'limite_sem_sinal_b': bmax + 2, 'a_2026': t['pct_secoes_excesso'],
                               'b_2026': t['pct_ganho_em_excesso'], 'veredito': v7,
                               'veredito_sem_exterior': veredito_t7(r26['T7_Lula_sem_exterior']['pct_secoes_excesso'],
                                                                    r26['T7_Lula_sem_exterior']['pct_ganho_em_excesso'], amax, bmax),
                               'troca_equivalente_tabela_adendo4_pela_a': interp_troca(t['pct_secoes_excesso'], 0),
                               'troca_equivalente_tabela_adendo4_pela_b': interp_troca(t['pct_ganho_em_excesso'], 1)},
                        'T14': {'coef': b14, 'ep': s14, 'z_acima_de_0.071': (b14 - 0.071) / s14, 'veredito': v14,
                                'coef_sem_grupos': b14s, 'ep_sem_grupos': s14s, 'veredito_sem_grupos': veredito_t14(b14s, s14s),
                                'coef_sem_exterior': r26['T14_com_grupos_sem_exterior']['coef']['adversario_1T'],
                                'troca_equivalente_contra_2018': (b14 - 0.0063) / ((0.0709 - 0.0063) / 6.5),
                                'troca_equivalente_contra_2022': (b14 - 0.0377) / ((0.1002 - 0.0377) / 6.5)},
                        'T37': {'letra_principal': r26['T37']['letra_principal']['letra_z_de_zero'],
                                'veredito': 'INCONCLUSIVO (Adendo 17: a medida registrada não se interpreta, b_L + b_F = 1 por identidade)'},
                        'T38': {'veredito': 'DESCRITIVO'}}
    json.dump(res, open(saida, 'w'), ensure_ascii=False, indent=1, default=float)
    log('gravado', saida)


# ---------------------------------------------------------------- relatório em texto
def fn(x, nd=2, sinal=False):
    if x is None or (isinstance(x, float) and x != x):
        return 'n/d'
    t = f'{x:+.{nd}f}' if sinal else f'{x:.{nd}f}'
    return t.replace('.', ',')


def fi(n, sinal=False):
    t = f'{int(n):+,}' if sinal else f'{int(n):,}'
    return t.replace(',', '.')


def texto(res):
    R, r, cr, cf = res['referencias'], res['2026'], res['criterios'], res['conferencias']
    t7r = {a: R[a]['T7_ganhador'] for a in R}; t = r['T7_Lula']; c7 = cr['T7']; c14 = cr['T14']
    o = []; w = o.append
    w('T7 e T14 com o bweb completo do 2º turno de 2026 (Adendos 3, 4 e 8), mais T37 com o bweb (Adendos 16 e 17) e T38 por UF e')
    w('município (Adendo 16, descritivo).')
    w('Script: scripts/analisar_T7_T14.py (python3 -I analisar_T7_T14.py ... para os números; --texto <json> para este texto).')
    w('Números completos: resultados/T7_T14_bweb.json. Rodado em 29/10/2026 com secoes2026.json.gz (bweb do 1º e do 2º turno; a soma')
    w('dos boletins do 2º turno bate voto a voto com o total oficial, T15), candidatos2026_1t.json.gz e as bases de 2018 e 2022 por seção.')
    w('')
    w('Critérios registrados (PRE-REGISTRO-2026-10-26.md, antes dos dados):')
    w('- T7 (Adendo 3): "bolo = votos dos outros candidatos no 1º turno + queda do branco+nulo (se houver) + aumento do comparecimento')
    w('  (se houver). Excesso do candidato que mais ganhou = ganho dele na seção menos o bolo. [...] Estatísticas: (a) % das seções com')
    w('  excesso positivo; (b) soma dos excessos positivos como % do ganho total do candidato. Referências: 2018 (Haddad [...]) e 2022')
    w('  (Bolsonaro [...]). 2026: Lula. Sinal: (a) e (b) de 2026 acima do maior valor das referências em mais de 5 pontos. Sem sinal: (a)')
    w('  e (b) até 2 pontos acima do maior valor das referências. Entre os dois: inconclusivo."')
    w('- Adendo 4 (leitura): "um resultado perto de 35% das seções e 7% do ganho seria compatível com a troca que a Veritá implica; perto')
    w('  de 5% a 9% das seções e 1% a 1,5% do ganho, incompatível. O critério do adendo 3 continua valendo."')
    w('- T14 (Adendo 8): coeficiente dos votos do adversário no 1º turno na regressão do T8 (mesmo local), "com todas as seções do bweb:')
    w('  Sinal: coeficiente acima de 0,071 [...] e a mais de 3 erros-padrão disso. Compatível com a troca que a pesquisa Veritá implicaria')
    w('  (cerca de 6,5%): 0,10 ou mais. Sem sinal: até 0,051. Entre os dois: inconclusivo."')
    w('- T37 (Adendo 16): dF = b_F - f; dL = b_L - l (quatro grupos somados pelo voto do 1º turno; f e l = mediana dos institutos). "Padrão')
    w('  da forma A: |dF| até 0,07 e dL de 0,15 ou mais, a mais de 2,5 erros-padrão [...]. Padrão da forma B: dF de -0,07 ou menos e dL de')
    w('  +0,07 ou mais, os dois a mais de 2,5 erros-padrão. Sem padrão de fraude: |dF| e |dL| até 0,07. Qualquer outro resultado:')
    w('  inconclusivo." Adendo 17: "na especificação do T8, b_L + b_F = 1 por identidade, e a urna não identifica o \'nenhum\' dos eleitores')
    w('  dos eliminados. O veredito pela letra é inconclusivo, e a comparação corrigida [...] é post hoc."')
    w('- T38 (Adendo 16): descritivo, sem critério.')
    w('')
    w('VEREDITOS PELA LETRA')
    w(f'  T7:  {c7["veredito"]}. (a) {fn(c7["a_2026"])}% fica entre o limite de sem sinal ({fn(c7["limite_sem_sinal_a"])}%) e o de sinal')
    w(f'       ({fn(c7["limite_sinal_a"])}%); (b) {fn(c7["b_2026"])}% fica abaixo do limite de sem sinal ({fn(c7["limite_sem_sinal_b"])}%). Sinal e sem sinal')
    w('       pedem as duas medidas; com uma em cada faixa, o resultado é inconclusivo.')
    w(f'  T14: {c14["veredito"]}. Coeficiente {fn(c14["coef"], 4)} (ep {fn(c14["ep"], 4)}), abaixo do limite de sem sinal (0,051).')
    w(f'  T37: INCONCLUSIVO (Adendo 17). Os limiares do Adendo 16, aplicados mecanicamente, caem no "{cr["T37"]["letra_principal"]}", mas esse')
    w('       padrão sai da identidade b_L + b_F = 1 e do "nenhum" declarado pelas pesquisas, não dos dados (seção 3).')
    w('  T38: DESCRITIVO.')
    w('')
    w('Conferências (o código reproduz os números já registrados antes de relatar):')
    w(f'  T7 de 2018 e 2022 iguais a resultados/T7_referencias.txt em todos os campos: {"sim" if cf["T7_2018_igual_ao_registrado"] and cf["T7_2022_igual_ao_registrado"] else "NÃO"}.')
    w(f'  T7 nas 3.897 seções da amostra, lidas do bweb: igual a resultados/T7_T8_T14_amostra.txt em todos os campos: {"sim" if cf["T7_amostra_igual"] else "NÃO"}.')
    w(f'  T14 da amostra (com grupos) pelo bweb: {fn(cf["T14_amostra_com_grupos_registrado_0.0507"], 4)} (registrado 0,0507). T14 sem troca: 2018 {fn(cf["T14_2018_calibracao_0.0063"], 4)}')
    w(f'  (registrado 0,0063), 2022 {fn(cf["T14_2022_calibracao_0.0377"], 4)} (registrado 0,0377). T37 da amostra: b_L somado {fn(cf["T37_amostra_b_L_somado"][1], 4)} (registrado {fn(cf["T37_amostra_b_L_somado"][0], 4)}).')
    ok38 = all(a == b for a, b in cf['T38_municipios_igual_ao_oficial'].values()) and not cf['T38_UF_diferencas_contra_totais_oficiais']
    w(f'  T38 pelo bweb igual ao T38 feito com os totais oficiais por município e por UF (contagens, somas e ganhos): {"sim" if ok38 else "NÃO"}.')
    cal = R['2022']['T7_calibracao_troca_refeita']
    okc = all(abs(round(v['valor_esperado'][0], 2) - v['tabela_registrada'][0]) < 0.006 and abs(round(v['valor_esperado'][1], 2) - v['tabela_registrada'][1]) < 0.006 for v in cal.values())
    w(f'  Tabela do Adendo 4 refeita em 2022 (troca pelo valor esperado, s vezes os votos do adversário no 2º turno): igual a 2 casas: {"sim" if okc else "NÃO"}.')
    w('')
    w('1. T7, ganho além do bolo da seção')
    w(f'  Seções com os dois turnos: 2018 {fi(t7r["2018"]["secoes"])}, 2022 {fi(t7r["2022"]["secoes"])}, 2026 {fi(t["secoes"])}.')
    w('  (erro-padrão por linearização agrupada por local de votação; o registro não pede erro, e o critério compara os valores)')
    w('  candidato              | (a) % seções com excesso | (b) % do ganho em excesso | ganho total   | excesso somado')
    for nome, x in (('2018 Haddad', t7r['2018']), ('2022 Bolsonaro', t7r['2022']), ('2026 Lula', t)):
        w(f'  {nome:<22} | {fn(x["pct_secoes_excesso"]):>6} (ep {fn(x["ep_pct_secoes_excesso"])})        | {fn(x["pct_ganho_em_excesso"]):>5} (ep {fn(x["ep_pct_ganho_em_excesso"])})          | {fi(x["ganho_total"]):>12}  | {fi(x["excesso_total"])}')
    w(f'  Maior referência: (a) {fn(c7["maior_a_ref"])}% e (b) {fn(c7["maior_b_ref"])}%, as duas de 2022. Limites: sinal (a) > {fn(c7["limite_sinal_a"])} e (b) > {fn(c7["limite_sinal_b"])};')
    w(f'  sem sinal (a) <= {fn(c7["limite_sem_sinal_a"])} e (b) <= {fn(c7["limite_sem_sinal_b"])}. 2026: (a) {fn(c7["a_2026"])}, {fn(c7["a_2026"] - c7["maior_a_ref"])} pontos acima de 2022; (b) {fn(c7["b_2026"])}, {fn(c7["b_2026"] - c7["maior_b_ref"])} ponto acima.')
    sx = r['T7_Lula_sem_exterior']
    w(f'  Sem o exterior: (a) {fn(sx["pct_secoes_excesso"])}%, (b) {fn(sx["pct_ganho_em_excesso"])}%; veredito {c7["veredito_sem_exterior"]}.')
    w(f'  Seções em que Flávio perdeu votos entre os turnos: {fn(t["pct_secoes_adversario_perdeu_votos"], 1)}% (2022, Lula: {fn(t7r["2022"]["pct_secoes_adversario_perdeu_votos"], 1)}%; 2018, Bolsonaro: {fn(t7r["2018"]["pct_secoes_adversario_perdeu_votos"], 1)}%).')
    w(f'  Seções sem bolo (bolo de até 2 votos): {fi(t["secoes_sem_bolo"])}, com ganho somado de Lula de {fi(t["ganho_nas_secoes_sem_bolo"], True)} votos.')
    w('  Leitura registrada no Adendo 4 (calibração em 2022, troca uniforme de Flávio para Lula; tabela refeita, valores iguais):')
    w('    troca | (a) | (b)')
    for k, v in cal.items():
        w(f'    {fn(100*float(k), 1):>4}% | {fn(v["valor_esperado"][0])} | {fn(v["valor_esperado"][1])}')
    w(f'    2026: (a) {fn(c7["a_2026"])}% e (b) {fn(c7["b_2026"])}% ficam na faixa que o Adendo 4 chamou de incompatível com a troca da Veritá (5% a 9% e')
    w(f'    1% a 1,5%), longe de 35% e 7%. Interpolando a tabela (descritivo): (a) equivale a {fn(100*c7["troca_equivalente_tabela_adendo4_pela_a"], 1)}% de troca sobre a base de 2022 e (b)')
    w(f'    a {fn(100*c7["troca_equivalente_tabela_adendo4_pela_b"], 1)}%. A conta supõe que, sem troca, 2026 teria o mesmo nível de 2022; 2018 sem troca deu (a) 0,34% e (b) 0,02%, o que mostra')
    w('    que esse nível varia muito entre eleições.')
    w('  Descritivo, fora do critério: (a) e (b) por faixa da fatia do adversário nos válidos do 1º turno da seção.')
    w('    faixa   | 2026 (adversário Flávio)  | 2022 (adversário Lula)    | 2018 (adversário Bolsonaro)')
    for fx in r['T7_por_faixa_adversario']:
        a6, a2, a8 = r['T7_por_faixa_adversario'][fx], R['2022']['T7_por_faixa_adversario'][fx], R['2018']['T7_por_faixa_adversario'][fx]
        w(f'    {fx+"%":<7} | {fn(a6["pct_secoes_excesso"]):>5} e {fn(a6["pct_ganho_em_excesso"]):>4} ({fi(a6["secoes"])} seç.) | {fn(a2["pct_secoes_excesso"]):>5} e {fn(a2["pct_ganho_em_excesso"]):>4} ({fi(a2["secoes"])}) | {fn(a8["pct_secoes_excesso"]):>5} e {fn(a8["pct_ganho_em_excesso"]):>4} ({fi(a8["secoes"])})')
    w('    Numa troca proporcional aos votos de Flávio, o ganho extra por seção é maior onde Flávio tem mais votos. Em 2026 o excesso se concentra onde')
    f22 = R['2022']['T7_por_faixa_adversario']
    w('    Flávio era fraco no 1º turno (abaixo de 35%) e é menor onde ele era forte, nas duas medidas. Em 2022, (a) era quase igual nas')
    w(f'    quatro faixas e (b) crescia com a força do adversário (de {fn(f22["0-35"]["pct_ganho_em_excesso"])} a {fn(f22["65-100"]["pct_ganho_em_excesso"])}), o desenho que uma troca reforçaria.')
    uf = r['T7_por_UF']; ordem = sorted((u for u in uf if u != 'ZZ'), key=lambda u: -uf[u]['pct_secoes_excesso'])
    w('  Por UF (descritivo; (a) e (b) em %): ' + '; '.join(f'{u} {fn(uf[u]["pct_secoes_excesso"], 1)} e {fn(uf[u]["pct_ganho_em_excesso"], 1)}' for u in ordem[:9]) + ';')
    w('    ' + '; '.join(f'{u} {fn(uf[u]["pct_secoes_excesso"], 1)} e {fn(uf[u]["pct_ganho_em_excesso"], 1)}' for u in ordem[9:18]) + ';')
    w('    ' + '; '.join(f'{u} {fn(uf[u]["pct_secoes_excesso"], 1)} e {fn(uf[u]["pct_ganho_em_excesso"], 1)}' for u in ordem[18:]) + f'; exterior {fn(uf["ZZ"]["pct_secoes_excesso"], 1)} e {fn(uf["ZZ"]["pct_ganho_em_excesso"], 1)}.')
    fl = r['T7_Flavio_descritivo']
    w(f'  O mesmo cálculo para Flávio (descritivo): (a) {fn(fl["pct_secoes_excesso"])}% e (b) {fn(fl["pct_ganho_em_excesso"])}%. Para quem ganhou menos em 2022 (Lula): {fn(R["2022"]["T7_outro_finalista_descritivo"]["pct_secoes_excesso"])}% e {fn(R["2022"]["T7_outro_finalista_descritivo"]["pct_ganho_em_excesso"])}%;')
    w(f'  em 2018 (Bolsonaro): {fn(R["2018"]["T7_outro_finalista_descritivo"]["pct_secoes_excesso"])}% e {fn(R["2018"]["T7_outro_finalista_descritivo"]["pct_ganho_em_excesso"])}%.')
    am = r['T7_Lula_amostra_conferencia']
    w(f'  Amostra (preliminar, 3.897 seções): (a) {fn(am["pct_secoes_excesso"])}% (ep {fn(am["ep_pct_secoes_excesso"])}) e (b) {fn(am["pct_ganho_em_excesso"])}% (ep {fn(am["ep_pct_ganho_em_excesso"])}); com o bweb completo, {fn(t["pct_secoes_excesso"])}% e {fn(t["pct_ganho_em_excesso"])}%.')
    w('  O veredito da amostra (inconclusivo) se mantém.')
    w('  Limite registrado: o T7 não testa a conversão de branco e nulo (ela aparece como queda do branco+nulo, que está dentro do bolo).')
    w('  Excesso positivo também aparece por troca de eleitores entre os turnos (quem votou no 1º e faltou no 2º, substituído por quem')
    w('  faltou no 1º e votou no 2º), sem fraude.')
    w('')
    g, sg = r['T14_com_grupos'], r['T14_sem_grupos']; fx = r['T8_Flavio_com_grupos']
    w('2. T14, marca de troca de votos por seção')
    w(f'  Regressão do T8, Lula, efeito fixo de local, erro agrupado por local: {fi(g["secoes"])} seções, {fi(g["n_informativas"])} em {fi(g["locais"])} locais com 2 ou mais seções.')
    w(f'  Principal (eliminados separados, como o T8 de 2026 foi registrado): coeficiente dos votos de Flávio no 1º turno {fn(g["coef"]["adversario_1T"], 4)} (ep {fn(g["ep"]["adversario_1T"], 4)}).')
    w(f'  Outros agregados (como as referências): {fn(sg["coef"]["adversario_1T"], 4)} (ep {fn(sg["ep"]["adversario_1T"], 4)}), veredito {c14["veredito_sem_grupos"]}. Sem o exterior: {fn(c14["coef_sem_exterior"], 4)}.')
    w(f'  Limites: sem sinal até 0,051; sinal acima de 0,071 a mais de 3 ep (z = {fn(c14["z_acima_de_0.071"], 1)}); Veritá 0,10 ou mais.')
    w(f'  Intervalo de 95%: {fn(g["coef"]["adversario_1T"] - 1.96*g["ep"]["adversario_1T"], 4)} a {fn(g["coef"]["adversario_1T"] + 1.96*g["ep"]["adversario_1T"], 4)}, inteiro abaixo de 0,051.')
    w('  Referências sem troca (recalculadas, iguais à calibração do Adendo 8): 2018 Haddad 0,0063 (0,0007); 2022 Bolsonaro 0,0377 (0,0006).')
    w('  Calibração registrada: cada ponto de troca sobe o coeficiente cerca de 0,0099 (2018) e 0,0096 (2022).')
    w(f'  Leitura sem suavizar: 2026 fica no nível de 2022 sem troca (troca equivalente de {fn(c14["troca_equivalente_contra_2022"], 2)}% sobre a base de 2022), mas acima de 2018')
    w(f'  sem troca (troca equivalente de {fn(c14["troca_equivalente_contra_2018"], 1)}% sobre a base de 2018). O limite de sem sinal registrado (0,051) aceita, sobre a base de 2018,')
    w(f'  troca de até cerca de {fn((0.051 - 0.0063) / ((0.0709 - 0.0063) / 6.5), 1)}%, e sobre a de 2022, de até cerca de {fn((0.051 - 0.0377) / ((0.1002 - 0.0377) / 6.5), 1)}%. O teste exclui a troca de 6,5% que a Veritá implicaria sobre')
    w('  qualquer das duas bases. Sobre a base de 2022, a troca equivalente é de 0,17% (ep de cerca de 0,07 ponto de troca); sobre a')
    w('  de 2018, sobram 3,3%, perto dos cerca de 3,6% de troca que a aritmética exige para virar o resultado (Adendo 9). Qual base vale não')
    w('  se sabe: sem troca, o coeficiente variou de 0,006 a 0,041 entre os candidatos de 2018 e 2022 (Adendo 8), e 2026 fica dentro dessa faixa.')
    w(f'  Amostra (preliminar): 0,0507 (ep 0,0070), no limite; com o bweb completo, {fn(g["coef"]["adversario_1T"], 4)}. O T16 (piso por UF, resultados/T16_bweb.txt) mostra a')
    w('  variação entre UFs: de +0,006 (SC) a +0,096 (PI).')
    cg = g['coef']; eg = g['ep']
    w('  Demais coeficientes (Lula; ep entre parênteses): ' + ', '.join(f'{k} {fn(cg[k], 3)} ({fn(eg[k], 3)})' for k in cg if k != 'adversario_1T') + '.')
    w(f'  Contexto, mesma regressão para Flávio: próprios votos do 1º turno {fn(fx["coef"]["proprio_1T"], 4)} (ep {fn(fx["ep"]["proprio_1T"], 4)}), o mesmo número com sinal trocado, por')
    r18, r22 = R['2018']['T8_ganhador_sem_grupos']['coef'], R['2022']['T8_ganhador_sem_grupos']['coef']
    w(f'  identidade. Lula perdeu {fn(-g["coef"]["proprio_1T"]*100, 1)}% dos próprios (ep {fn(g["ep"]["proprio_1T"]*100, 1)}). Nas referências, quem ganhou terreno tirou do adversário')
    w(f'  {fn(100*r18["adversario_1T"], 1)}% (2018) e {fn(100*r22["adversario_1T"], 1)}% (2022); Lula em 2026, {fn(100*g["coef"]["adversario_1T"], 1)}%. A perda líquida de Flávio é do tamanho da perda do PT')
    w(f'  nas duas eleições anteriores (Haddad {fn(-100*r18["proprio_1T"], 1)}% em 2018, Lula {fn(100*r22["adversario_1T"], 1)}% em 2022), com os papéis trocados. Isso também é o que a troca de')
    w('  eleitores entre os turnos produz; o T14 não separa as duas.')
    w('')
    t37 = r['T37']; u = t37['urna']; lp = t37['letra_principal']; md = t37['mediana_declarada']
    w('3. T37, eleitores dos eliminados: urna contra o declarado')
    w(f'  Urna (regressão do T8 com grupos, Lula e Flávio empilhados, efeito fixo de local por candidato, erro agrupado por local;')
    w(f'  {fi(u["linhas"])} linhas, {fi(u["locais"])} locais). Fração dos votos do 1º turno de cada grupo que a urna põe em Lula (b_L) e em Flávio (b_F):')
    for nm, x in u['por_grupo'].items():
        w(f'    {nm:<7} b_L {fn(x["b_L"][0], 3)} ({fn(x["b_L"][1], 3)}) | b_F {fn(x["b_F"][0], 3)} ({fn(x["b_F"][1], 3)}) | "nenhum" {fn(x["nenhum_urna"], 3)} | {fi(u["votos_1T_grupos"][nm])} votos no 1º turno')
    w(f'    somados pelo voto do 1º turno: b_L {fn(u["b_L_somado"][0], 3)} ({fn(u["b_L_somado"][1], 3)}), b_F {fn(u["b_F_somado"][0], 3)} ({fn(u["b_F_somado"][1], 3)}). Amostra: b_L 0,522 (0,017).')
    w('  Declarado: para cada instituto, a última rodada antes de 25/10 que publicou o cruzamento por candidato eliminado')
    w('  (resultados/contexto_2t_2026_pesquisa_verificada.json, valores conferidos pelo verificador):')
    for inst, v in t37['declarado_fontes'].items():
        w(f'    {inst}: ' + '; '.join(f'{gname} f {fn(x["f"], 3)} l {fn(x["l"], 3)} n {fn(x["n"], 3)}' for gname, x in v.items()))
    w('    Mediana por grupo: ' + '; '.join(f'{gname} f {fn(x["f"], 3)} l {fn(x["l"], 3)} n {fn(x["n"], 3)} ({len(x["institutos"])} inst.)' for gname, x in md.items()) + '.')
    w(f'  Medidas do registro: l = {fn(lp["l_declarado"], 3)}, f = {fn(lp["f_declarado"], 3)}; dL = {fn(lp["dL"], 3, True)} (z {fn(lp["z_dL_de_zero"], 0)}), dF = {fn(lp["dF"], 3, True)} (z {fn(lp["z_dF_de_zero"], 0)}).')
    w(f'  Pelos limiares: |dF| <= 0,07 e dL >= 0,15 a mais de 2,5 ep, isto é, "{lp["letra_z_de_zero"]}" (igual lendo os 2,5 ep a partir do limiar: "{lp["letra_z_do_limiar"]}").')
    lpi, lpd = t37['letra_com_Ideia'], t37['letra_so_PoderData_final']
    w(f'  Com a Ideia (rodada não confirmada): dL {fn(lpi["dL"], 3, True)}, dF {fn(lpi["dF"], 3, True)}, "{lpi["letra_z_de_zero"]}". Só o PoderData de 23-24/10 (única última rodada com')
    w(f'  cruzamento; sem Zema): dL {fn(lpd["dL"], 3, True)}, dF {fn(lpd["dF"], 3, True)}, "{lpd["letra_z_de_zero"]}".')
    w(f'  Por que o padrão não se interpreta: como b_L + b_F = 1 na urna, dL + dF = 1 - l - f = {fn(lp["soma_dL_dF"], 3)}, a fatia que os eleitores dos')
    w('  eliminados declararam para nenhum dos dois. Com b_F perto de f, dL fica perto desse "nenhum", acima de 0,15, haja ou não conversão.')
    w('  O registro supunha que a urna mostraria o "nenhum"; ela não mostra (Adendo 17). Veredito: INCONCLUSIVO.')
    w('  Comparação post hoc (Adendo 17; feita depois de ver b_F na amostra): fatia de Lula entre os que escolheram um finalista, mesmos grupos.')
    for inst, v in t37['post_hoc_lula_entre_finalistas'].items():
        w(f'    {inst} ({", ".join(v["grupos"])}): declarado {fn(100*v["declarado_lula_entre_finalistas"], 1)}%, urna {fn(100*v["urna_mesmos_grupos"], 1)}%')
    dfa = t37['post_hoc_datafolha_agregado']
    w(f'    Datafolha 13-14/10 (agregado dos quatro): declarado {fn(100*dfa["declarado"], 1)}%, urna {fn(100*dfa["urna_quatro_grupos"], 1)}%')
    ph = {k: 100 * (v['urna_mesmos_grupos'] - v['declarado_lula_entre_finalistas']) for k, v in t37['post_hoc_lula_entre_finalistas'].items() if 'Ideia' not in k}
    kmin, kmax = min(ph, key=ph.get), max(ph, key=ph.get); vt = sum(u['votos_1T_grupos'].values()); esc = vt * (1 - lp['n_declarado'])
    idv = [v for k, v in t37['post_hoc_lula_entre_finalistas'].items() if 'Ideia' in k][0]
    w(f'    A urna fica de {fn(ph[kmin], 1)} ({kmin.split()[0]}) a {fn(ph[kmax], 1)} pontos ({kmax.split()[0]}) acima dos institutos confirmados; só a Ideia, com rodada não')
    w(f'    confirmada e só Cury, fica perto ({fn(100*idv["declarado_lula_entre_finalistas"], 1)}% contra {fn(100*idv["urna_mesmos_grupos"], 1)}%). Com cerca de {fn(esc/1e6, 1)} milhões de eleitores dos eliminados')
    w(f'    escolhendo um finalista ({fn(vt/1e6, 2)} milhões menos o "nenhum" declarado de {fn(lp["n_declarado"], 2)}), cada 10 pontos são cerca de {fn(esc/1e7, 1)} milhão de votos para Lula.')
    w('    É regressão ecológica (inclui a troca de eleitores entre os turnos) contra subamostras pequenas e instáveis das pesquisas; o mesmo')
    w('    desenho aparece se houve voto escondido ou decisão tardia nesse grupo. Por grupo, a ordem da urna e das pesquisas é a mesma (Cury')
    w('    mais Lula, Zema mais Flávio).')
    w('')
    t38 = r['T38']; cm = t38['corte_eliminados_municipio']
    w('4. T38, pontos ganhos entre turnos por UF e por município (descritivo), agora somando as seções do bweb nos dois turnos')
    w(f'  UFs (27 e exterior): Flávio ganhou mais votos que Lula em {len(t38["UFs_flavio_mais_votos"])} e mais pontos em {len(t38["UFs_flavio_mais_pontos"])}. Flávio perdeu votos em ' +
      ', '.join(f'{k} {fi(v, True)}' for k, v in sorted(t38['UFs_flavio_perdeu_votos'].items(), key=lambda kv: kv[1])) + '.')
    w('  UF | ganho Lula | ganho Flávio | pontos Lula | pontos Flávio | Flávio - Lula | eliminados % dos válidos do 1º turno (Caiado, Renan, Cury, Zema)')
    for ufn, x in t38['por_UF'].items():
        gp = x['grupos_pct_V1']
        w(f'  {ufn} | {fi(x["gL"], True)} | {fi(x["gR"], True)} | {fn(x["pL"], 2, True)} | {fn(x["pR"], 2, True)} | {fn(x["F_menos_L_pontos"], 2, True)} | {fn(x["elim_pct_V1"], 1)} ({fn(gp["Caiado"], 1)}, {fn(gp["Renan"], 1)}, {fn(gp["Cury"], 1)}, {fn(gp["Zema"], 1)})')
    w(f'  Correlação entre UFs (sem o exterior) de Flávio - Lula com a fatia dos eliminados: {fn(t38["corte_eliminados_UF_correlacao"], 2, True)}.')
    w(f'  Municípios ({fi(t38["municipios"])}): Lula ganhou mais votos em {fi(t38["lula_mais_votos_que_flavio"])}, Flávio em {t38["flavio_mais_votos_que_lula"]} ({fn(100*t38["flavio_mais_votos_que_lula"]/t38["municipios"], 1)}%), {t38["empates_no_ganho"]} empates;')
    w(f'  Flávio ganhou mais pontos em {t38["flavio_mais_pontos_que_lula"]}; saldo de Flávio nas {t38["flavio_mais_votos_que_lula"]} cidades em que ganhou mais votos: {fi(t38["saldo_flavio_nas_cidades_em_que_ganhou_mais_votos"], True)}.')
    w(f'  Viraram de Flávio para Lula: {t38["viraram_de_flavio_para_lula"]}; de Lula para Flávio: {t38["viraram_de_lula_para_flavio"]} (' + ', '.join(f'{v["uf"]} {v["nome"]}' for v in t38['lista_viraram_para_flavio']) + ').')
    w('  Os números são os mesmos do T38 feito com os totais oficiais por município (resultados/T38_municipios.txt).')
    w('  Corte por força dos eliminados (fatia de Caiado, Renan, Cury e Zema nos válidos do 1º turno do município; faixas escolhidas aqui):')
    w('    faixa (%) | cidades | média Flávio - Lula (pontos) | média ponderada pelos válidos | % com Flávio mais pontos')
    for k, v in cm['faixas_fixas_pct_V1'].items():
        w(f'    {k:<9} | {v["cidades"]:>7} | {fn(v["media_F_menos_L"], 2, True):>6} | {fn(v["media_ponderada_V1"], 2, True):>6} | {fn(v["pct_flavio_mais_pontos"], 1)}')
    w('    quintis: ' + '; '.join(f'{k.replace(".", ",")}: {fn(v["media_F_menos_L"], 2, True)}, {fn(v["pct_flavio_mais_pontos"], 1)}%' for k, v in cm['quintis'].items()) + '.')
    w('    Cidades com 15% ou mais: ' + ', '.join(f'{k} {v}' for k, v in t38['cidades_eliminados_15pct_ou_mais_por_UF'].items()) + '.')
    b1, b2 = cm['inclinacao_sem_peso_por_ponto'], cm['inclinacao_peso_V1_por_ponto']; mp = cm['multipla_sem_peso_[Cury,Renan,Caiado,Zema,Flavio1T]']
    w(f'    Correlação {fn(cm["correlacao"], 2, True)}; inclinação {fn(b1[0], 3, True)} ponto por ponto (ep agrupado por UF {fn(b1[1], 3)}); ponderada pelos válidos {fn(b2[0], 3, True)} ({fn(b2[1], 3)}).')
    w('    Regressão múltipla, por ponto de fatia no 1º turno (ep agrupado por UF): ' + ', '.join(f'{nm} {fn(c, 3, True)} ({fn(e, 3)})' for nm, c, e in zip(['Cury', 'Renan', 'Caiado', 'Zema', 'Flávio'], mp['coef'], mp['ep_agrupado_UF'])) + '.')
    ff = cm['faixas_fixas_pct_V1']; ate15 = [v['media_F_menos_L'] for k, v in ff.items() if not k.startswith('15')]
    c15 = t38['cidades_eliminados_15pct_ou_mais_por_UF']
    w(f'    Leitura: a virada para Lula foi quase igual nas faixas até 15% (de {fn(max(ate15), 1, True)} a {fn(min(ate15), 1, True)} pontos); nas {sum(c15.values())} cidades com 15% ou mais')
    w(f'    ({c15.get("GO", 0)} em Goiás, terra de Caiado), {fn(ff["15-100"]["media_F_menos_L"], 1, True)}: ali Flávio foi relativamente melhor. Onde Cury era forte, Lula foi relativamente')
    w('    melhor, o que combina com a urna (b_L de Cury 0,60) e com parte das pesquisas (Quaest, AtlasIntel e Ideia davam Cury mais Lula).')
    w('')
    w('Escolhas e desvios do registro')
    w('  - Ordem: o bweb de 2026 já tinha sido aberto por outros testes antes deste script. O coeficiente nacional do T14 já tinha aparecido')
    w('    (0,039 sem grupos em resultados/T8_2026_bweb_L.json; 0,0402 com grupos e sem o exterior em resultados/T16_bweb.txt). O T7, o T37 e o')
    w('    corte do T38 por força dos eliminados não tinham sido calculados com o bweb.')
    w('  - T14: principal com os eliminados separados, porque o T8 de 2026 foi registrado assim (Adendo 3) e porque foi a versão relatada na')
    w('    amostra (0,0507). As referências de 2018 e 2022 só têm os outros somados; a versão agregada sai ao lado e dá o mesmo veredito.')
    w('  - Exterior incluído no T7 e no T14, como na amostra, nas referências e no T8 já rodado; sem o exterior, os vereditos não mudam.')
    w('  - T7: votos do candidato 28 (candidatura anulada) contados entre os outros do 1º turno, como em analisar_fluxos.py e na amostra; são')
    w('    5.246 votos em 5.145 seções e não mexem no resultado. O erro-padrão do T7 não estava no registro.')
    w('  - Adendo 4: a tabela foi refeita pelo valor esperado da troca (s vezes os votos do adversário), que reproduz a tabela registrada; com')
    w('    sorteio binomial os valores de (a) ficam 1 a 2 pontos menores. A troca equivalente de 2026 é interpolação descritiva.')
    w('  - T37, declarado: "a última pesquisa de cada instituto que publicar esse cruzamento" lido como a última rodada de cada instituto, antes')
    w('    de 25/10, que publicou o cruzamento por candidato eliminado: PoderData 23-24/10, Quaest 17-20/10, AtlasIntel 13-18/10, Ipespe 13-15/10')
    w('    e Nexus 10-12/10. A Ideia (rodada não confirmada pelo verificador) sai da principal e entra numa variante. O Datafolha só publicou o')
    w('    agregado dos quatro e não entra na mediana por grupo. Zema só aparece separado na Nexus (e no PoderData de 5-7/10, que não é a última')
    w('    rodada do instituto). Grupo sem dado sai da soma, com os pesos renormalizados. A pesquisa entra como fixa, como o registro diz.')
    w('  - T37: "a mais de 2,5 erros-padrão" lido a partir de zero; a leitura a partir do limiar dá o mesmo.')
    w('  - T37, veredito: os limiares do Adendo 16 dão "padrão da forma A", mas o Adendo 17 (registrado em 27/10, antes do bweb) diz que a')
    w('    medida não se interpreta e que o veredito pela letra é inconclusivo. Fica INCONCLUSIVO, com o resultado mecânico relatado acima.')
    w('  - Seções: o T7, o T14 e o T37 usam as 499.205 seções com os dois turnos na base; ficam fora uma seção do exterior só com 1º turno')
    w('    (ZZ|30686|1|443, 2 votantes) e a seção do exterior sem votante que a base não tem (T15). No T38 cada turno soma todas as suas seções.')
    w('  - T38: 2º turno somado das seções do bweb (antes vinha dos totais oficiais por município; dão o mesmo). Município só no Brasil (o')
    w('    exterior entra como linha ZZ na tabela por UF). As faixas do corte por força dos eliminados não estavam no registro.')
    w('')
    w(f'Veredito pela letra: T7 {c7["veredito"]}; T14 {c14["veredito"]}; T37 INCONCLUSIVO; T38 DESCRITIVO.')
    return '\n'.join(o)


if __name__ == '__main__':
    if len(sys.argv) > 2 and sys.argv[1] == '--texto':
        print(texto(json.load(open(sys.argv[2]))))
    else:
        main()
