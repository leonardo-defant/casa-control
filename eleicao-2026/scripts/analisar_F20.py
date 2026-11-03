"""F20 (Adendo 23, H2 de resultados/CACA_AO_FURO.txt): governador na mesma urna nas UFs com 2º turno de governador.

Registro (PRE-REGISTRO-2026-10-26.md, Adendo 23, commit 863a34e, 03/11/2026 01:13:05 UTC):
- Classificação, gravada com fonte antes de calcular, em AC, AM, DF, ES, RN e TO: qual finalista do 2º turno de
  governador é do campo de Flávio (apoio declarado a Flávio no 2º turno ou partido ou coligação do PL) e qual do campo
  de Lula. UF sem um finalista claramente do campo de Flávio fica de fora.
- Estatística: a mesma função t22b de scripts/analisar_pres_gov.py, sem mudança, nas UFs classificadas, empilhada e por
  UF. Calibração: D com troca simulada só no voto de presidente de 3,6% dos votos de Flávio (t22b_com_troca de
  scripts/analisar_T22.py).
- Critério do T22b sem mudança: SINAL se D <= -0,03 a mais de 2,5 EP; SEM SINAL se -0,015 <= D <= +0,015; entre os
  dois, INCONCLUSIVO. Acrescentado: EXCLUSÃO se o D observado ficar acima do D simulado com 3,6% a mais de 4 EP
  (soma das variâncias): a troca só no presidente do tamanho que vira a eleição fica excluída nessas UFs.
- Descritivo: o espelho (coeficiente próprio de Lula menos o do governador do campo de Lula).

Classificação: resultados/F20_classificacao_governadores.json, gravada às 01:19 UTC de 03/11/2026, antes de escrever
este script e antes de abrir qualquer base por seção nesta tarefa. Resultado: AC 11 Mailza, AM 22 Maria do Carmo,
DF 11 Celina Leão, ES 10 Pazolini, TO 44 Dorinha; RN fora (nenhum finalista do campo de Flávio). Campo de Lula: AM 55,
DF 13 (e RN 13, fora do F20).

Decisões tomadas antes de calcular (pontos que a letra não fixa; todas declaradas como desvio):
D1. "Campo de Flávio" = atende a (a) apoio ou voto declarado em Flávio no 2º turno, ou (b) filiado ao PL ou com o PL na
    coligação registrada. Basta uma (a letra diz "ou").
D2. Em AC e TO os dois finalistas atendem a (a). A letra só exclui a UF SEM finalista do campo de Flávio, e o t22b
    precisa de um aliado por UF. Regra: entra o único finalista que atende a (a) e (b) ao mesmo tempo; se os dois ou
    nenhum atendem a (b), a UF sai. AC -> 11 Mailza (PL na coligação Avança Acre); TO -> 44 Dorinha (PL na coligação
    União pelo Tocantins). Robustez descritiva: o outro finalista como aliado (AC 10, TO 45).
D3. "Campo de Lula" (só para o espelho) = finalista que declarou apoio ou voto em Lula, ou teve apoio declarado de
    Lula, e não está no campo de Flávio. Nas UFs do F20: AM 55 e DF 13.
D4. "Sem mudança" na função: t22b e t22b_com_troca são chamadas como estão. As UFs e os aliados entram trocando, em
    tempo de execução, o dicionário ALIADO_FLAVIO do módulo analisar_pres_gov (FINALISTAS já traz AC e TO). O código
    das duas funções não é tocado. O mínimo de 30 seções por UF da função fica como está.
D5. Base: a mesma montagem do analisar_T22.py (secoes2026.json.gz, 6 UFs; votos por candidato a governador no 2º
    turno lidos dos zips bweb do 2º turno, cargo 3, pela função extrai_gov2 do mesmo script; só seções com 1º e 2º
    turno de presidente e de governador). Conferência dos zips contra a base em B, N, V e comp.
D6. EXCLUSÃO: z = (D_obs - D_sim) / raiz(EP_obs^2 + EP_sim^2), com D_sim e EP_sim da t22b_com_troca(s = 0,036).
    EXCLUSÃO se z > 4. O veredito usa o D empilhado das UFs classificadas. Por UF: os mesmos limiares, relatados como
    descritivo, sem veredito próprio.
D7. Espelho: mesma especificação do t22b com os papéis trocados. Presidente: ganho de Lula entre turnos contra demais
    candidatos no 1º turno, queda do branco+nulo, variação do comparecimento, votos de Flávio no 1º turno (adversário)
    e votos de Lula no 1º turno (próprio). Governador: ganho do finalista do campo de Lula contra os demais do 1º turno,
    queda do branco+nulo de governador, variação do comparecimento de governador, votos do outro finalista (adversário)
    e os próprios. Empilhado, efeito fixo de local por cargo, erro agrupado por local, pela ols_cluster do mesmo
    módulo. Espelho = próprio(Lula) - próprio(governador do campo de Lula). Conferência: com dois finalistas e a soma
    dos votos fechando, próprio(Lula) = -adversário_1T da regressão de Flávio; o script compara as duas contas.
    RN (Cadu 13) vai só como contexto fora do registro.
D8. Robustezas descritivas, fora do critério: (i) só AM, DF e ES (o conjunto do Adendo 14; deve reproduzir o T22b de
    resultados/T22_bweb.json); (ii) aliado trocado em AC (10) e TO (45); (iii) tirando uma UF por vez do conjunto
    principal; (iv) tamanho de troca que o D empilhado separaria a 4 EP (busca por bisseção na t22b_com_troca).
D9. Contexto descritivo por UF: fatias agregadas (votos) de Flávio e do aliado no comparecimento de cada turno.

ACRESCENTADO DEPOIS DE VER O RESULTADO (descritivo, fora do registro, não entra no veredito):
P1. Nas UFs com um finalista de cada campo (AM e DF), o contraste C = D - espelho, tirado de uma regressão só (a do
    t22b refeita aqui com a mesma montagem de linhas; pela identidade da soma dos votos, espelho = adversário_1T do
    aliado - adversário_1T de Flávio, então C = (próprio + adversário de Flávio) - (próprio + adversário do aliado)),
    com EP pela matriz de covariância agrupada. Motivo: a troca só no presidente desloca D em cerca de -s(1+próprio)
    e quase não mexe no espelho (deslocamento +s vezes adversário_1T, perto de 0,001), então o espelho serve de
    referência de comportamento na mesma urna que a troca não contamina. Sem troca e com comportamento simétrico,
    C perto de 0; com troca de 3,6%, C perto de -0,035. Relatado com e sem a troca simulada.
P2. O espelho recalculado com a troca simulada de 3,6% (conferência de que ele não se move).

Uso: python3 -I analisar_F20.py <secoes2026.json.gz> <pasta_zips2t> <candidatos_gov_2026_1t_6ufs.json.gz>
                                 <F20_classificacao_governadores.json> <saida.json> <saida.txt>
"""
import os as _os, sys as _sys
_sys.path.insert(0, _os.path.dirname(_os.path.abspath(__file__)))
import collections, gc, glob, json, os, sys
from multiprocessing import Pool
import numpy as np
from lib import carregar, chave_local
import analisar_pres_gov as APG
import analisar_T22 as T22

UFS6 = ('AC', 'AM', 'DF', 'ES', 'RN', 'TO')
S_TROCA = 0.036


# ---------------------------------------------------------------- base (como analisar_T22.main, passos 1 e 2)
def montar_base(p26, pzips, pgov1):
    zips = sorted(z for uf in UFS6 for z in glob.glob(os.path.join(pzips, f'bweb_2t_{uf}_*.zip')))
    assert len(zips) == 6, zips
    gov2, tipos = {}, {}
    with Pool(3) as pool:
        for nome, o, tp in pool.imap_unordered(T22.extrai_gov2, zips):
            gov2.update(o); tipos[nome] = tp
    d = carregar(p26)
    cp = collections.defaultdict(lambda: np.zeros(2))
    for k, v in d.items():
        if '1' in v and '2' in v:
            cp[k.split('|')[0]] += (v['1']['comp'], v['2']['comp'])
    tot = sum(cp.values())
    var_comp = {u: float(cp[u][1] / cp[u][0] - 1) for u in UFS6}
    var_comp['Brasil_com_exterior'] = float(tot[1] / tot[0] - 1)
    base = {k: v for k, v in d.items() if k.split('|')[0] in UFS6}
    del d; gc.collect()
    gov1 = carregar(pgov1)['secoes']
    conf = collections.Counter(); fin = collections.defaultdict(collections.Counter)
    for k, v in base.items():
        g = gov2.get(k)
        if '2g' not in v:
            conf['base_sem_2g'] += 1; continue
        if g is None:
            conf['zip_sem_secao'] += 1; continue
        conf['igual' if all(v['2g'][c] == g[c] for c in ('B', 'N', 'V', 'comp')) else 'diferente'] += 1
        if sum(g['cand'].values()) != g['V']:
            conf['V_diferente_soma_nominal'] += 1
        fin[k.split('|')[0]].update(g['cand'])
        v['2g'] = dict(v['2g']); v['2g']['cand'] = g['cand']
    conf['secoes_zip_fora_da_base'] = sum(1 for k in gov2 if k not in base)
    conf['secoes_sem_candidatos_gov_1t'] = sum(1 for k in base if k not in gov1)
    base = {k: v for k, v in base.items() if all(t in v for t in ('1', '2', '1g', '2g'))}
    info = {'tipos_votavel_governador_2t': tipos, 'conferencia_governador_2t_zip_contra_base': dict(conf),
            'votos_governador_2t_por_numero': {uf: dict(c) for uf, c in sorted(fin.items())},
            'secoes_com_1t_e_2t_pres_e_gov': dict(collections.Counter(k.split('|')[0] for k in base)),
            'variacao_relativa_comparecimento_presidente_1t_2t': var_comp}
    return base, gov1, info


# ---------------------------------------------------------------- t22b sem mudança, com as UFs e aliados do F20
def veredito_t22b(D, se):
    # mesma regra escrita dentro de APG.t22b
    return 'SINAL' if D <= -0.03 and -D / se > 2.5 else 'SEM SINAL' if abs(D) <= 0.015 else 'INCONCLUSIVO'


def rodar(base, gov1, aliados, s=S_TROCA):
    antigo = APG.ALIADO_FLAVIO
    APG.ALIADO_FLAVIO = dict(aliados)
    try:
        sub = {k: v for k, v in base.items() if k.split('|')[0] in aliados}
        obs = APG.t22b(sub, None, gov1)
        sim = T22.t22b_com_troca(sub, gov1, s)
    finally:
        APG.ALIADO_FLAVIO = antigo
    D, se = obs['D_proprio_Flavio_menos_aliado']; Ds, ses = sim['D_proprio_Flavio_menos_aliado']
    z = (D - Ds) / np.sqrt(se ** 2 + ses ** 2)
    out = {'aliados': dict(aliados), 'observado': obs,
           'simulado_troca_so_presidente': {'s': s, 'D': [Ds, ses], 'veredito_t22b_se_fosse_observado': veredito_t22b(Ds, ses),
                                           'proprio_Flavio': sim['presidente_Flavio']['proprio_1T'],
                                           'por_uf_D': {u: r['D'] for u, r in sim['por_uf'].items()}},
           'D': [D, se], 'veredito_t22b': obs['veredito'],
           'deslocamento_pela_troca': float(D - Ds),
           'z_exclusao': float(z), 'exclusao': bool(z > 4),
           'D_natural_que_esconderia_a_troca': float(D + (D - Ds))}
    pu = {}
    for u, r in obs['por_uf'].items():
        d_, e_ = r['D']; rs = sim['por_uf'].get(u)
        zz = float((d_ - rs['D'][0]) / np.sqrt(e_ ** 2 + rs['D'][1] ** 2)) if rs else None
        pu[u] = {'secoes': r['secoes'], 'locais': r['locais'], 'proprio_Flavio': r['proprio_Flavio'],
                 'proprio_aliado': r['proprio_aliado'], 'D': r['D'], 'D_sim': rs['D'] if rs else None,
                 'leitura_t22b_descritiva': veredito_t22b(d_, e_), 'z_exclusao': zz,
                 'exclusao_descritiva': (zz is not None and zz > 4)}
    out['por_uf'] = pu
    return out


def troca_minima_4ep(base, gov1, aliados, D, se):
    """Menor s em que (D - D_sim(s)) / raiz(se^2 + se_sim^2) = 4, por bisseção (descritivo)."""
    antigo = APG.ALIADO_FLAVIO
    APG.ALIADO_FLAVIO = dict(aliados)
    try:
        sub = {k: v for k, v in base.items() if k.split('|')[0] in aliados}
        def z(s):
            Ds, ses = T22.t22b_com_troca(sub, gov1, s)['D_proprio_Flavio_menos_aliado']
            return (D - Ds) / np.sqrt(se ** 2 + ses ** 2)
        lo, hi = 0.0, S_TROCA
        if z(hi) < 4:
            return None
        for _ in range(14):
            mid = (lo + hi) / 2
            if z(mid) >= 4:
                hi = mid
            else:
                lo = mid
        return float(hi)
    finally:
        APG.ALIADO_FLAVIO = antigo


# ---------------------------------------------------------------- espelho (D7)
def espelho(base, gov1, campo_lula):
    linhas_p, linhas_g = [], []
    for k, v in base.items():
        uf = k.split('|')[0]
        if uf not in campo_lula or '1' not in v or '1g' not in v:
            continue
        a, b, ag, bg = v['1'], v['2'], v['1g'], v['2g']
        loc = chave_local(k, b)
        bn1, bn2 = a['B'] + a['N'], b['B'] + b['N']
        linhas_p.append((loc, b['L'] - a['L'], [a['O'], bn1 - bn2, b['comp'] - a['comp'], a['R'], a['L']]))
        cl = campo_lula[uf]; op = [x for x in APG.FINALISTAS[uf] if x != cl][0]
        c1 = gov1.get(k, {}); l1 = c1.get(cl, 0); o1 = c1.get(op, 0); out1 = sum(q for n, q in c1.items() if n not in (cl, op))
        l2 = bg.get('cand', {}).get(cl, 0)
        gbn1, gbn2 = ag['B'] + ag['N'], bg['B'] + bg['N']
        linhas_g.append((loc, l2 - l1, [out1, gbn1 - gbn2, bg['comp'] - ag['comp'], o1, l1]))
    nomes = ['outros_1T', 'queda_branco_nulo', 'var_comparecimento', 'adversario_1T', 'proprio_1T']
    n = len(linhas_p)
    y = np.array([r[1] for r in linhas_p] + [r[1] for r in linhas_g], float)
    X = np.zeros((2 * n, 10))
    X[:n, :5] = np.array([r[2] for r in linhas_p], float); X[n:, 5:] = np.array([r[2] for r in linhas_g], float)
    fe = [r[0] + '|p' for r in linhas_p] + [r[0] + '|g' for r in linhas_g]
    cl_ = [r[0] for r in linhas_p] + [r[0] for r in linhas_g]
    b, V, N, G = APG.ols_cluster(y, X, fe, cl_)
    E = b[4] - b[9]; seE = float(np.sqrt(V[4, 4] + V[9, 9] - 2 * V[4, 9]))
    out = {'campo_lula': dict(campo_lula), 'secoes': n, 'linhas': N, 'locais': G,
           'presidente_Lula': {nm: [float(b[i]), float(np.sqrt(V[i, i]))] for i, nm in enumerate(nomes)},
           'governador_campo_lula': {nm: [float(b[5 + i]), float(np.sqrt(V[5 + i, 5 + i]))] for i, nm in enumerate(nomes)},
           'espelho_proprio_Lula_menos_gov_campo_Lula': [float(E), seE]}
    por = {}
    for uf in campo_lula:
        idx = [i for i, r in enumerate(linhas_p) if r[0].startswith(uf + '|')]
        if len(idx) < 30:
            continue
        ii = np.array(idx + [n + i for i in idx])
        bb, VV, NN, GG = APG.ols_cluster(y[ii], X[ii], [fe[i] for i in ii], [cl_[i] for i in ii])
        por[uf] = {'secoes': len(idx), 'locais': GG, 'proprio_Lula': [float(bb[4]), float(np.sqrt(VV[4, 4]))],
                   'proprio_gov_campo_Lula': [float(bb[9]), float(np.sqrt(VV[9, 9]))],
                   'espelho': [float(bb[4] - bb[9]), float(np.sqrt(VV[4, 4] + VV[9, 9] - 2 * VV[4, 9]))]}
    out['por_uf'] = por
    return out


# ---------------------------------------------------------------- pós-resultado (P1, P2)
def com_troca(base, ufs, s):
    """Mesma troca da t22b_com_troca (s dos votos de Flávio no 2º turno para Lula, só presidente)."""
    b2 = {}
    for k, v in base.items():
        if k.split('|')[0] not in ufs:
            continue
        w = dict(v); w['2'] = dict(v['2'])
        r = w['2']['R']; w['2']['R'] = r * (1 - s); w['2']['L'] = w['2']['L'] + r * s
        b2[k] = w
    return b2


def contraste_C(base, gov1, aliados):
    """Refaz as linhas do APG.t22b (mesmo código de montagem) e devolve D e C = D - espelho com EP agrupado."""
    linhas_p, linhas_g = [], []
    for k, v in base.items():
        uf = k.split('|')[0]
        if uf not in aliados or '1' not in v or '1g' not in v:
            continue
        a, b, ag, bg = v['1'], v['2'], v['1g'], v['2g']
        loc = chave_local(k, b)
        bn1, bn2 = a['B'] + a['N'], b['B'] + b['N']
        linhas_p.append((loc, b['R'] - a['R'], [a['O'], bn1 - bn2, b['comp'] - a['comp'], a['L'], a['R']]))
        al = aliados[uf]; op = [x for x in APG.FINALISTAS[uf] if x != al][0]
        c1 = gov1.get(k, {}); a1 = c1.get(al, 0); o1 = c1.get(op, 0); out1 = sum(q for n, q in c1.items() if n not in (al, op))
        a2 = bg.get('cand', {}).get(al, 0)
        gbn1, gbn2 = ag['B'] + ag['N'], bg['B'] + bg['N']
        linhas_g.append((loc, a2 - a1, [out1, gbn1 - gbn2, bg['comp'] - ag['comp'], o1, a1]))
    n = len(linhas_p)
    y = np.array([r[1] for r in linhas_p] + [r[1] for r in linhas_g], float)
    X = np.zeros((2 * n, 10))
    X[:n, :5] = np.array([r[2] for r in linhas_p], float); X[n:, 5:] = np.array([r[2] for r in linhas_g], float)
    fe = [r[0] + '|p' for r in linhas_p] + [r[0] + '|g' for r in linhas_g]
    cl_ = [r[0] for r in linhas_p] + [r[0] for r in linhas_g]
    b, V, N, G = APG.ols_cluster(y, X, fe, cl_)
    cD = np.zeros(10); cD[4], cD[9] = 1, -1
    cE = np.zeros(10); cE[8], cE[3] = 1, -1      # espelho = adv_aliado - adv_Flavio
    cC = cD - cE
    est = lambda c: [float(c @ b), float(np.sqrt(c @ V @ c))]
    return {'secoes': n, 'D': est(cD), 'espelho_pela_identidade': est(cE), 'C_D_menos_espelho': est(cC)}


def pos_resultado(base, gov1, aliados_polar, campo_lula):
    ufs = set(aliados_polar)
    sub = {k: v for k, v in base.items() if k.split('|')[0] in ufs}
    sem = contraste_C(sub, gov1, aliados_polar)
    com = contraste_C(com_troca(sub, ufs, S_TROCA), gov1, aliados_polar)
    por = {}
    for u in sorted(ufs):
        s1 = {k: v for k, v in sub.items() if k.startswith(u + '|')}
        a = {u: aliados_polar[u]}
        por[u] = {'sem_troca': contraste_C(s1, gov1, a), 'com_troca_3_6': contraste_C(com_troca(s1, {u}, S_TROCA), gov1, a)}
    E_troca = espelho(com_troca(sub, ufs, S_TROCA), gov1, campo_lula)
    return {'aviso': 'Acrescentado depois de ver o resultado. Descritivo, fora do registro, não entra no veredito.',
            'ufs': dict(aliados_polar), 'P1_sem_troca': sem, 'P1_com_troca_3_6': com, 'P1_por_uf': por,
            'P2_espelho_com_troca_3_6': E_troca['espelho_proprio_Lula_menos_gov_campo_Lula'],
            'P2_espelho_com_troca_3_6_por_uf': {u: r['espelho'] for u, r in E_troca['por_uf'].items()}}


# ---------------------------------------------------------------- contexto (D9)
def contexto(base, gov1, aliados):
    res = {}
    for uf, al in aliados.items():
        t = collections.Counter()
        for k, v in base.items():
            if not k.startswith(uf + '|'):
                continue
            a, b, ag, bg = v['1'], v['2'], v['1g'], v['2g']
            t['R1'] += a['R']; t['R2'] += b['R']; t['L1'] += a['L']; t['L2'] += b['L']
            t['c1'] += a['comp']; t['c2'] += b['comp']
            t['g1'] += gov1.get(k, {}).get(al, 0); t['g2'] += bg['cand'].get(al, 0)
            t['gc1'] += ag['comp']; t['gc2'] += bg['comp']
        res[uf] = {'aliado': al,
                   'Flavio_pct_comp_1t': 100 * t['R1'] / t['c1'], 'Flavio_pct_comp_2t': 100 * t['R2'] / t['c2'],
                   'aliado_pct_comp_1t': 100 * t['g1'] / t['gc1'], 'aliado_pct_comp_2t': 100 * t['g2'] / t['gc2'],
                   'Flavio_votos_1t': t['R1'], 'Flavio_votos_2t': t['R2'], 'aliado_votos_1t': t['g1'], 'aliado_votos_2t': t['g2'],
                   'Flavio_variacao_relativa': t['R2'] / t['R1'] - 1, 'aliado_variacao_relativa': t['g2'] / t['g1'] - 1,
                   'virada_Lula_finalistas_pontos': 100 * (t['L2'] / (t['L2'] + t['R2']) - t['L1'] / (t['L1'] + t['R1']))}
    return res


# ---------------------------------------------------------------- texto
def f(x, d=4):
    return f'{x:+.{d}f}'.replace('.', ',')


def g(x, d=4):
    return f'{x:.{d}f}'.replace('.', ',')


def texto(out):
    P = out['principal']; L = []
    L.append('F20 (Adendo 23, H2): governador na mesma urna nas UFs com 2º turno de governador')
    L.append('Rodado em 03/11/2026. Classificação gravada antes: resultados/F20_classificacao_governadores.json')
    L.append('')
    L.append('UFs e aliados de Flávio: ' + ', '.join(f'{u} {n}' for u, n in P['aliados'].items()) + '. RN fora (nenhum finalista do campo de Flávio).')
    c = out['base']['conferencia_governador_2t_zip_contra_base']
    L.append(f"Base: {sum(out['base']['secoes_com_1t_e_2t_pres_e_gov'].values())} seções das 6 UFs com presidente e governador nos dois turnos; "
             f"governador do 2º turno por candidato lido dos zips, igual à base em {c.get('igual', 0)} seções, diferente em {c.get('diferente', 0)}.")
    o = P['observado']
    L.append('')
    L.append(f"PRINCIPAL (empilhado, {o['secoes']} seções, {o['linhas']} linhas, {o['locais']} locais)")
    L.append(f"  próprio Flávio {f(o['presidente_Flavio']['proprio_1T'][0])} (EP {g(o['presidente_Flavio']['proprio_1T'][1])}); "
             f"próprio aliado {f(o['governador_aliado']['proprio_1T'][0])} (EP {g(o['governador_aliado']['proprio_1T'][1])})")
    L.append(f"  D observado {f(P['D'][0])} (EP {g(P['D'][1])}); critério do T22b: {P['veredito_t22b']}")
    s = P['simulado_troca_so_presidente']
    L.append(f"  D com troca simulada de 3,6% só no presidente {f(s['D'][0])} (EP {g(s['D'][1])}); deslocamento {f(P['deslocamento_pela_troca'])}")
    L.append(f"  z da exclusão {g(P['z_exclusao'], 2)} (limiar 4): {'EXCLUSÃO' if P['exclusao'] else 'sem exclusão'}")
    L.append(f"  D natural que uma troca de 3,6% deixaria igual ao observado: {f(P['D_natural_que_esconderia_a_troca'])}")
    if out.get('troca_minima_4ep_principal') is not None:
        L.append(f"  menor troca que o D separaria a 4 EP (descritivo): {g(100 * out['troca_minima_4ep_principal'], 2)}% dos votos de Flávio")
    L.append('')
    L.append('Por UF (descritivo, mesmos limiares):')
    for u, r in P['por_uf'].items():
        L.append(f"  {u}: {r['secoes']} seções; próprio Flávio {f(r['proprio_Flavio'][0])} ({g(r['proprio_Flavio'][1])}), "
                 f"aliado {f(r['proprio_aliado'][0])} ({g(r['proprio_aliado'][1])}); D {f(r['D'][0])} ({g(r['D'][1])}) [{r['leitura_t22b_descritiva']}]; "
                 f"D 3,6% {f(r['D_sim'][0])}; z {g(r['z_exclusao'], 2)}")
    L.append('')
    L.append('Robustezas (descritivas):')
    for nome, r in out['robustez'].items():
        L.append(f"  {nome}: D {f(r['D'][0])} ({g(r['D'][1])}) [{r['veredito_t22b']}]; D 3,6% {f(r['simulado_troca_so_presidente']['D'][0])}; "
                 f"z {g(r['z_exclusao'], 2)} [{'EXCLUSÃO' if r['exclusao'] else 'sem exclusão'}]")
    E = out['espelho']
    L.append('')
    L.append(f"Espelho (AM 55, DF 13): próprio Lula {f(E['presidente_Lula']['proprio_1T'][0])} ({g(E['presidente_Lula']['proprio_1T'][1])}), "
             f"governador do campo de Lula {f(E['governador_campo_lula']['proprio_1T'][0])} ({g(E['governador_campo_lula']['proprio_1T'][1])}); "
             f"espelho {f(E['espelho_proprio_Lula_menos_gov_campo_Lula'][0])} ({g(E['espelho_proprio_Lula_menos_gov_campo_Lula'][1])})")
    for u, r in E['por_uf'].items():
        L.append(f"  {u}: próprio Lula {f(r['proprio_Lula'][0])}, governador {f(r['proprio_gov_campo_Lula'][0])}, espelho {f(r['espelho'][0])} ({g(r['espelho'][1])})")
    ck = out['espelho_conferencia_identidade']
    L.append(f"  conferência: próprio Lula pela regressão espelhada {f(ck['proprio_Lula_espelho'], 6)} contra -adversário_1T da regressão de Flávio {f(ck['menos_adversario_na_reg_Flavio'], 6)}")
    R = out['espelho_RN_fora_do_registro']['por_uf'].get('RN')
    if R:
        L.append(f"  RN (fora do registro, Cadu 13): próprio Lula {f(R['proprio_Lula'][0])}, Cadu {f(R['proprio_gov_campo_Lula'][0])}, espelho {f(R['espelho'][0])} ({g(R['espelho'][1])})")
    vc = out['base']['variacao_relativa_comparecimento_presidente_1t_2t']
    L.append('')
    L.append('Variação do comparecimento entre turnos (presidente): ' +
             '; '.join(f"{u} {f(100 * x, 2)}%" for u, x in vc.items()))
    L.append('Contexto agregado por UF (% do comparecimento de cada cargo):')
    for u, r in out['contexto_por_uf'].items():
        L.append(f"  {u}: Flávio {g(r['Flavio_pct_comp_1t'], 1)} -> {g(r['Flavio_pct_comp_2t'], 1)} ({f(100 * r['Flavio_variacao_relativa'], 1)}% dos votos); "
                 f"aliado {r['aliado']} {g(r['aliado_pct_comp_1t'], 1)} -> {g(r['aliado_pct_comp_2t'], 1)} ({f(100 * r['aliado_variacao_relativa'], 1)}% dos votos); "
                 f"virada de Lula {f(r['virada_Lula_finalistas_pontos'], 2)} pontos")
    pr = out.get('pos_resultado_descritivo')
    if pr:
        L.append('')
        L.append('DEPOIS DE VER O RESULTADO (descritivo, fora do registro), AM e DF:')
        for nome, r in (('sem troca', pr['P1_sem_troca']), ('com troca simulada de 3,6%', pr['P1_com_troca_3_6'])):
            L.append(f"  {nome}: D {f(r['D'][0])} ({g(r['D'][1])}); espelho {f(r['espelho_pela_identidade'][0])} ({g(r['espelho_pela_identidade'][1])}); "
                     f"C = D - espelho {f(r['C_D_menos_espelho'][0])} ({g(r['C_D_menos_espelho'][1])})")
        for u, r in pr['P1_por_uf'].items():
            L.append(f"  {u}: C sem troca {f(r['sem_troca']['C_D_menos_espelho'][0])} ({g(r['sem_troca']['C_D_menos_espelho'][1])}); "
                     f"com troca {f(r['com_troca_3_6']['C_D_menos_espelho'][0])}")
        L.append(f"  espelho recalculado com a troca de 3,6%: {f(pr['P2_espelho_com_troca_3_6'][0])} ({g(pr['P2_espelho_com_troca_3_6'][1])})")
    L.append('')
    L.append('VEREDITO PELA LETRA: ' + out['veredito'])
    return '\n'.join(L) + '\n'


# ---------------------------------------------------------------- principal
def main():
    p26, pzips, pgov1, pclass, saida, saida_txt = sys.argv[1:7]
    cls = json.load(open(pclass, encoding='utf-8'))
    aliados = {u: n for u, n in cls['resumo']['ufs_no_F20'].items()}
    campo_lula = {u: n for u, n in cls['resumo']['campo_de_Lula_para_o_espelho'].items()}
    troca_ali = cls['resumo']['robustez_aliado_trocado']
    for u, n in aliados.items():
        assert n in APG.FINALISTAS[u], (u, n)
    out = {'arquivos': {'base_2026': p26, 'zips_2t': pzips, 'gov_1t': pgov1, 'classificacao': pclass},
           'registro': 'PRE-REGISTRO-2026-10-26.md, Adendo 23 (commit 863a34e), F20'}
    base, gov1, info = montar_base(p26, pzips, pgov1)
    out['base'] = info

    P = rodar(base, gov1, aliados)
    out['principal'] = P
    out['troca_minima_4ep_principal'] = troca_minima_4ep(base, gov1, aliados, *P['D'])

    rob = {}
    rob['so_AM_DF_ES_adendo14'] = rodar(base, gov1, {u: aliados[u] for u in ('AM', 'DF', 'ES')})
    alt = dict(aliados); alt.update(troca_ali)
    rob['aliado_trocado_AC10_TO45'] = rodar(base, gov1, alt)
    for u in aliados:
        rob[f'sem_{u}'] = rodar(base, gov1, {k: v for k, v in aliados.items() if k != u})
    for r in rob.values():  # enxuga: os coeficientes completos ficam só no principal
        r['observado'] = {k: r['observado'][k] for k in ('secoes', 'linhas', 'locais', 'D_proprio_Flavio_menos_aliado', 'veredito')}
    out['robustez'] = rob

    E = espelho(base, gov1, campo_lula)
    out['espelho'] = E
    antigo = APG.ALIADO_FLAVIO
    APG.ALIADO_FLAVIO = {u: aliados[u] for u in campo_lula}
    try:
        ref = APG.t22b({k: v for k, v in base.items() if k.split('|')[0] in campo_lula}, None, gov1)
    finally:
        APG.ALIADO_FLAVIO = antigo
    out['espelho_conferencia_identidade'] = {
        'proprio_Lula_espelho': E['presidente_Lula']['proprio_1T'][0],
        'menos_adversario_na_reg_Flavio': -ref['presidente_Flavio']['adversario_1T'][0],
        'proprio_gov_campo_Lula_espelho': E['governador_campo_lula']['proprio_1T'][0],
        'menos_adversario_na_reg_aliado': -ref['governador_aliado']['adversario_1T'][0]}
    out['espelho_RN_fora_do_registro'] = espelho(base, gov1, {'RN': '13'})
    out['contexto_por_uf'] = contexto(base, gov1, aliados)
    pr = pos_resultado(base, gov1, {u: aliados[u] for u in campo_lula}, campo_lula)
    # a regressão refeita tem de dar o mesmo D da t22b sem mudança
    assert abs(pr['P1_sem_troca']['D'][0] - rodar(base, gov1, {u: aliados[u] for u in campo_lula})['D'][0]) < 1e-12
    out['pos_resultado_descritivo'] = pr

    v = P['veredito_t22b']
    out['veredito'] = (f"{v} pelo critério do T22b (D = {f(P['D'][0])}, EP {g(P['D'][1])}); "
                       f"{'EXCLUSÃO' if P['exclusao'] else 'SEM EXCLUSÃO'} pelo acréscimo do Adendo 23 (z = {g(P['z_exclusao'], 2)}, limiar 4)")
    with open(saida, 'w', encoding='utf-8') as fh:
        json.dump(out, fh, ensure_ascii=False, indent=1)
    with open(saida_txt, 'w', encoding='utf-8') as fh:
        fh.write(texto(out))
    print('ok', saida, saida_txt)


if __name__ == '__main__':
    main()
