"""T22 (Adendo 9, com as UFs claras do Adendo 14), T22b (Adendo 14) e T39 (Adendo 16) com o bweb completo do 2º turno de 2026.

Dados:
- base 2026 por seção (1º e 2º turno, presidente e governador com B, N, V, comp): secoes2026.json.gz
- votos por candidato a governador no 2º turno: lidos aqui dos zips bweb do 2º turno das 6 UFs (cargo 3, tipo nominal)
- votos por candidato a governador no 1º turno: candidatos_gov_2026_1t_6ufs.json.gz
- referências do T39: secoes2018.json.gz e secoes2022.json.gz (governador do 2º turno com B, N, V, comp)

T22 (registro): nas UFs alinhadas (AM e DF, Adendo 14), regressão com efeito fixo de local da variação da fatia de Lula
  entre os dois finalistas (pontos) na variação da fatia do governador do campo de Lula entre os dois finalistas (pontos)
  e na composição do 1º turno. Leitura literal escolhida para "composição do 1º turno": fatias do comparecimento do 1º
  turno de Lula, Flávio e demais candidatos a presidente (branco+nulo é a categoria omitida, porque as quatro somam 100 e
  o efeito fixo já tem constante). Sem peso, erro agrupado por local (como a função t22 de analisar_pres_gov.py, fixada
  antes de abrir o estrato G). Leituras ao lado: sem covariáveis (a do Adendo 14), com peso L2+R2 (convenção do T17) e com
  a composição do governador no 1º turno.
  "Virada de Lula não acompanhada": média da virada de Lula menos a inclinação vezes a média da variação do governador
  (na média simples das seções e no agregado da UF), com erro-padrão por bootstrap de locais; e a diferença 1 para 1.
T22b (registro): função t22b de analisar_pres_gov.py, sem mudança, nas seções de AM, DF e ES.
T39 (registro, descritivo): R(t) = branco+nulo de presidente / branco+nulo de governador (em % do comparecimento de cada
  cargo), nas mesmas seções, 1º e 2º turno, por UF; erro-padrão por linearização agrupada por local.

Uso: python3 -I analisar_T22.py <secoes2026.json.gz> <pasta_zips2t> <candidatos_gov_2026_1t_6ufs.json.gz>
                                 <secoes2018.json.gz> <secoes2022.json.gz> <saida.json>
"""
import os as _os, sys as _sys
_sys.path.insert(0, _os.path.dirname(_os.path.abspath(__file__)))
import collections, csv, gc, glob, io, json, os, sys, zipfile
from multiprocessing import Pool
import numpy as np
from lib import carregar, chave_local, fe_ols
import analisar_pres_gov as APG

UFS6 = ('AC', 'AM', 'DF', 'ES', 'RN', 'TO')
CAMPO_T22 = {'AM': {'lula': '55', 'flavio': '22'}, 'DF': {'lula': '13', 'flavio': '11'}}  # Adendo 14
SEMENTE = 20261029
NBOOT = 1000


# ---------------------------------------------------------------- extração do governador do 2º turno por candidato
def extrai_gov2(zpath):
    out = {}; tipos = collections.Counter()
    z = zipfile.ZipFile(zpath)
    nome = [n for n in z.namelist() if n.lower().endswith('.csv')][0]
    with z.open(nome) as fh:
        rd = csv.reader(io.TextIOWrapper(fh, encoding='latin1', newline=''), delimiter=';')
        cab = next(rd)
        ix = {c.strip().replace('SG_ UF', 'SG_UF'): i for i, c in enumerate(cab)}
        iC, iU, iM, iZ, iS = ix['CD_CARGO_PERGUNTA'], ix['SG_UF'], ix['CD_MUNICIPIO'], ix['NR_ZONA'], ix['NR_SECAO']
        iT, iN, iQ, iCo = ix['CD_TIPO_VOTAVEL'], ix['NR_VOTAVEL'], ix['QT_VOTOS'], ix['QT_COMPARECIMENTO']
        for r in rd:
            if r[iC] != '3':
                continue
            k = f"{r[iU]}|{int(r[iM])}|{int(r[iZ])}|{int(r[iS])}"
            s = out.get(k)
            if s is None:
                s = out[k] = {'B': 0, 'N': 0, 'V': 0, 'comp': int(r[iCo]), 'cand': {}}
            tv, nv, q = int(r[iT]), r[iN].strip(), int(r[iQ])
            tipos[tv] += q
            if tv == 2:
                s['B'] += q
            elif tv == 3:
                s['N'] += q
            else:
                s['V'] += q
                if tv == 1:
                    s['cand'][str(int(nv))] = s['cand'].get(str(int(nv)), 0) + q
    return os.path.basename(zpath), out, dict(tipos)


# ---------------------------------------------------------------- utilidades
def fe_mask(g):
    _, gi = np.unique(g, return_inverse=True)
    return np.bincount(gi)[gi] >= 2


def fe_coef(y, X, g, w=None):
    """Só o coeficiente (para o bootstrap): MQO within com pesos opcionais."""
    _, gi = np.unique(g, return_inverse=True)
    w = np.ones(len(y)) if w is None else w
    Z = np.column_stack([y, X])
    sw = np.bincount(gi, weights=w)
    out = np.empty_like(Z)
    for j in range(Z.shape[1]):
        m = np.bincount(gi, weights=w * Z[:, j]) / sw
        out[:, j] = Z[:, j] - m[gi]
    yd, Xd = out[:, 0], out[:, 1:]
    s = np.sqrt(w)
    return np.linalg.lstsq(Xd * s[:, None], yd * s, rcond=None)[0]


def media_cluster(v, g):
    """Média simples e erro-padrão agrupado (CR1) de uma média."""
    _, gi = np.unique(g, return_inverse=True); G = gi.max() + 1; n = len(v)
    m = v.mean(); S = np.bincount(gi, weights=v - m, minlength=G)
    return float(m), float(np.sqrt(G / (G - 1) * (S ** 2).sum()) / n)


# ---------------------------------------------------------------- T22
def linhas_t22(base, gov1, uf):
    cl, cf = CAMPO_T22[uf]['lula'], CAMPO_T22[uf]['flavio']
    R = collections.defaultdict(list); n_uf = n_fora = 0
    for k, v in base.items():
        if not k.startswith(uf + '|') or not all(t in v for t in ('1', '2', '1g', '2g')):
            continue
        n_uf += 1
        a, b, ag, bg = v['1'], v['2'], v['1g'], v['2g']; c1 = gov1.get(k, {}); c2 = bg.get('cand', {})
        g1 = c1.get(cl, 0) + c1.get(cf, 0); g2 = c2.get(cl, 0) + c2.get(cf, 0)
        if a['L'] + a['R'] <= 0 or b['L'] + b['R'] <= 0 or g1 <= 0 or g2 <= 0 or a['comp'] <= 0 or ag['comp'] <= 0:
            n_fora += 1
            continue
        R['y'].append(100 * (b['L'] / (b['L'] + b['R']) - a['L'] / (a['L'] + a['R'])))
        R['x'].append(100 * (c2.get(cl, 0) / g2 - c1.get(cl, 0) / g1))
        R['L1'].append(a['L']); R['R1'].append(a['R']); R['L2'].append(b['L']); R['R2'].append(b['R'])
        R['gl1'].append(c1.get(cl, 0)); R['gf1'].append(c1.get(cf, 0)); R['gl2'].append(c2.get(cl, 0)); R['gf2'].append(c2.get(cf, 0))
        R['pL'].append(100 * a['L'] / a['comp']); R['pR'].append(100 * a['R'] / a['comp']); R['pO'].append(100 * a['O'] / a['comp'])
        gout = sum(q for n, q in c1.items() if n not in (cl, cf))
        R['qL'].append(100 * c1.get(cl, 0) / ag['comp']); R['qF'].append(100 * c1.get(cf, 0) / ag['comp'])
        R['qO'].append(100 * gout / ag['comp'])
        R['loc'].append(chave_local(k, b))
    A = {c: np.array(vv, float) for c, vv in R.items() if c != 'loc'}
    A['loc'] = np.array(R['loc'])
    A['_contagem'] = (n_uf, n_fora)
    return A


def t22_uf(A, rng):
    n_uf, n_fora = A.pop('_contagem')
    m = fe_mask(A['loc'])
    A = {c: v[m] for c, v in A.items()}
    y, x, loc, w = A['y'], A['x'], A['loc'], A['L2'] + A['R2']
    comp_p = np.column_stack([A['pL'], A['pR'], A['pO']])
    comp_g = np.column_stack([A['qL'], A['qF'], A['qO']])
    specs = {
        'principal_composicao_presidente_1T': (np.column_stack([x, comp_p]), None, ['dgov', 'L1', 'R1', 'O1']),
        'sem_covariaveis_como_adendo14': (x[:, None], None, ['dgov']),
        'principal_com_peso_L2_R2': (np.column_stack([x, comp_p]), w, ['dgov', 'L1', 'R1', 'O1']),
        'principal_mais_composicao_governador_1T': (np.column_stack([x, comp_p, comp_g]), None,
                                                    ['dgov', 'L1', 'R1', 'O1', 'gL1', 'gF1', 'gO1']),
    }
    out = {'secoes': int(len(y)), 'locais': int(len(np.unique(loc))), 'secoes_na_uf': n_uf,
           'excluidas_sem_voto_nos_finalistas': n_fora, 'excluidas_local_de_uma_secao': int((~m).sum())}
    # agregados da UF (votos)
    dL_agr = 100 * (A['L2'].sum() / (A['L2'] + A['R2']).sum() - A['L1'].sum() / (A['L1'] + A['R1']).sum())
    dG_agr = 100 * (A['gl2'].sum() / (A['gl2'] + A['gf2']).sum() - A['gl1'].sum() / (A['gl1'] + A['gf1']).sum())
    my, se_my = media_cluster(y, loc); mx, se_mx = media_cluster(x, loc); md, se_md = media_cluster(y - x, loc)
    out['virada_media_lula_secoes'] = [my, se_my]
    out['variacao_media_governador_campo_lula_secoes'] = [mx, se_mx]
    out['virada_lula_agregado_uf'] = float(dL_agr)
    out['variacao_governador_campo_lula_agregado_uf'] = float(dG_agr)
    out['diferenca_1_para_1_secoes'] = [md, se_md]
    out['diferenca_1_para_1_agregado_uf'] = float(dL_agr - dG_agr)
    out['correlacao_bruta'] = float(np.corrcoef(x, y)[0, 1])
    # bootstrap de locais para a parte não acompanhada (especificação principal)
    _, gi = np.unique(loc, return_inverse=True); G = gi.max() + 1
    idx_por = [np.flatnonzero(gi == c) for c in range(G)]
    Xp, _, _ = specs['principal_composicao_presidente_1T']
    for nome, (X, ww, nomes) in specs.items():
        r = fe_ols(y, X, loc, ww, nomes)
        b = r['coef']['dgov']
        if ww is None:
            na = my - b * mx
        else:
            na = float(np.average(y, weights=ww) - b * np.average(x, weights=ww))
        out[nome] = {'n': r['n'], 'locais': r['grupos'], 'inclinacao': [b, r['ep']['dgov']],
                     'coef': {k: [r['coef'][k], r['ep'][k]] for k in nomes},
                     'nao_acompanhada_media_secoes': float(na),
                     'nao_acompanhada_agregado_uf': float(dL_agr - b * dG_agr)}
    # bootstrap só da principal
    bs_na, bs_agr, bs_b = [], [], []
    for _ in range(NBOOT):
        sel = rng.integers(0, G, G)
        ii = np.concatenate([idx_por[c] for c in sel])
        gg = np.concatenate([np.full(len(idx_por[c]), j) for j, c in enumerate(sel)])
        bb = fe_coef(y[ii], Xp[ii], gg)[0]
        yy, xx = y[ii], x[ii]
        L1, R1, L2, R2 = A['L1'][ii], A['R1'][ii], A['L2'][ii], A['R2'][ii]
        a1, f1, a2, f2 = A['gl1'][ii], A['gf1'][ii], A['gl2'][ii], A['gf2'][ii]
        dl = 100 * (L2.sum() / (L2 + R2).sum() - L1.sum() / (L1 + R1).sum())
        dg = 100 * (a2.sum() / (a2 + f2).sum() - a1.sum() / (a1 + f1).sum())
        bs_b.append(bb); bs_na.append(yy.mean() - bb * xx.mean()); bs_agr.append(dl - bb * dg)
    p = out['principal_composicao_presidente_1T']
    p['nao_acompanhada_media_secoes'] = [p['nao_acompanhada_media_secoes'], float(np.std(bs_na, ddof=1))]
    p['nao_acompanhada_agregado_uf'] = [p['nao_acompanhada_agregado_uf'], float(np.std(bs_agr, ddof=1))]
    p['inclinacao_ep_bootstrap'] = float(np.std(bs_b, ddof=1))
    return out


# ---------------------------------------------------------------- T22b com calibração
def t22b_com_troca(base, gov1, s):
    """Mesma função t22b, com troca simulada de uma fração s dos votos de Flávio no 2º turno para Lula (só presidente)."""
    b2 = {}
    for k, v in base.items():
        if k.split('|')[0] not in APG.ALIADO_FLAVIO:
            continue
        w = dict(v); w['2'] = dict(v['2'])
        r = w['2']['R']; w['2']['R'] = r * (1 - s); w['2']['L'] = w['2']['L'] + r * s
        b2[k] = w
    return APG.t22b(b2, None, gov1)


# ---------------------------------------------------------------- T39
def t39(d, ufs=None):
    """R(t) por UF e no total, nas seções com presidente e governador nos dois turnos."""
    por = collections.defaultdict(lambda: collections.defaultdict(list))
    for k, v in d.items():
        uf = k.split('|')[0]
        if (ufs is not None and uf not in ufs) or not all(t in v for t in ('1', '2', '1g', '2g')):
            continue
        a, b, ag, bg = v['1'], v['2'], v['1g'], v['2g']
        if min(a['comp'], b['comp'], ag['comp'], bg['comp']) <= 0:
            continue
        P = por[uf]
        P['p1'].append(a['B'] + a['N']); P['c1'].append(a['comp']); P['g1'].append(ag['B'] + ag['N']); P['gc1'].append(ag['comp'])
        P['p2'].append(b['B'] + b['N']); P['c2'].append(b['comp']); P['g2'].append(bg['B'] + bg['N']); P['gc2'].append(bg['comp'])
        P['loc'].append(chave_local(k, b))

    def resumo(P):
        loc = np.array(P['loc']); _, gi = np.unique(loc, return_inverse=True); G = gi.max() + 1
        S = {c: np.bincount(gi, weights=np.array(P[c], float), minlength=G) for c in ('p1', 'c1', 'g1', 'gc1', 'p2', 'c2', 'g2', 'gc2')}
        T = {c: S[c].sum() for c in S}
        o = {'secoes': len(loc), 'locais': int(G)}
        for t in ('1', '2'):
            o['bn_pres_' + t] = float(100 * T['p' + t] / T['c' + t]); o['bn_gov_' + t] = float(100 * T['g' + t] / T['gc' + t])
            o['R' + t] = o['bn_pres_' + t] / o['bn_gov_' + t]
        def ep_log(termos):
            z = sum(sg * S[c] / T[c] for c, sg in termos)
            return float(np.sqrt(G / (G - 1) * (z ** 2).sum()))
        e1 = ep_log([('p1', 1), ('c1', -1), ('g1', -1), ('gc1', 1)])
        e2 = ep_log([('p2', 1), ('c2', -1), ('g2', -1), ('gc2', 1)])
        er = ep_log([('p2', 1), ('c2', -1), ('g2', -1), ('gc2', 1), ('p1', -1), ('c1', 1), ('g1', 1), ('gc1', -1)])
        o['R1_ep'] = o['R1'] * e1; o['R2_ep'] = o['R2'] * e2
        o['R2_sobre_R1'] = o['R2'] / o['R1']; o['R2_sobre_R1_ep'] = o['R2_sobre_R1'] * er
        return o

    res = {uf: resumo(P) for uf, P in sorted(por.items())}
    todos = collections.defaultdict(list)
    for uf, P in por.items():
        for c, vv in P.items():
            todos[c] += vv
    if todos:
        res['todas'] = resumo(todos)
    return res


# ---------------------------------------------------------------- principal
def main():
    p26, pzips, pgov1, p18, p22, saida = sys.argv[1:7]
    out = {'arquivos': {'base_2026': p26, 'zips_2t': pzips, 'gov_1t': pgov1, 'ref_2018': p18, 'ref_2022': p22}}

    # 1) governador do 2º turno por candidato, dos zips das 6 UFs
    zips = sorted(z for uf in UFS6 for z in glob.glob(os.path.join(pzips, f'bweb_2t_{uf}_*.zip')))
    assert len(zips) == 6, zips
    gov2 = {}; tipos = {}
    with Pool(3) as pool:
        for nome, o, tp in pool.imap_unordered(extrai_gov2, zips):
            gov2.update(o); tipos[nome] = tp
    out['tipos_votavel_governador_2t'] = tipos

    # 2) base 2026 das 6 UFs (carregada uma vez)
    d = carregar(p26)
    # contexto fora do registro: virada de Lula entre os dois finalistas por UF, agregada (todas as seções com os dois turnos)
    ag = collections.defaultdict(lambda: np.zeros(4))
    for k, v in d.items():
        if '1' in v and '2' in v:
            ag[k.split('|')[0]] += (v['1']['L'], v['1']['R'], v['2']['L'], v['2']['R'])
    tot = sum(ag.values())
    vir = lambda a: float(100 * (a[2] / (a[2] + a[3]) - a[0] / (a[0] + a[1])))
    out['contexto_virada_lula_por_uf'] = {uf: vir(a) for uf, a in sorted(ag.items())}
    out['contexto_virada_lula_brasil_com_exterior'] = vir(tot)
    base = {k: v for k, v in d.items() if k.split('|')[0] in UFS6}
    del d; gc.collect()
    gov1 = carregar(pgov1)['secoes']

    # conferência do que foi lido dos zips contra a base (B, N, V, comp do governador no 2º turno)
    conf = collections.Counter(); finalistas = collections.defaultdict(collections.Counter)
    for k, v in base.items():
        g = gov2.get(k)
        if '2g' not in v:
            conf['base_sem_2g'] += 1; continue
        if g is None:
            conf['zip_sem_secao'] += 1; continue
        if all(v['2g'][c] == g[c] for c in ('B', 'N', 'V', 'comp')):
            conf['igual'] += 1
        else:
            conf['diferente'] += 1
        if sum(g['cand'].values()) != g['V']:
            conf['V_diferente_soma_nominal'] += 1
        finalistas[k.split('|')[0]].update(g['cand'])
        v['2g'] = dict(v['2g']); v['2g']['cand'] = g['cand']
    conf['secoes_zip_fora_da_base'] = sum(1 for k in gov2 if k not in base)
    out['conferencia_governador_2t'] = dict(conf)
    out['votos_governador_2t_por_numero'] = {uf: dict(c) for uf, c in sorted(finalistas.items())}
    out['secoes_por_uf'] = dict(collections.Counter(k.split('|')[0] for k in base))
    out['secoes_com_1t_e_2t_governador'] = dict(collections.Counter(
        k.split('|')[0] for k, v in base.items() if all(t in v for t in ('1', '2', '1g', '2g'))))
    out['secoes_sem_candidatos_gov_1t'] = sum(1 for k in base if k not in gov1)

    base = {k: v for k, v in base.items() if all(t in v for t in ('1', '2', '1g', '2g'))}

    # 3) T22
    rng = np.random.default_rng(SEMENTE)
    out['T22'] = {'ufs': CAMPO_T22, 'por_uf': {uf: t22_uf(linhas_t22(base, gov1, uf), rng) for uf in CAMPO_T22}}
    out['T22']['funcao_adendo14_sem_mudanca'] = APG.t22(base, gov1)

    # 4) T22b (função do Adendo 14 sem mudança) e calibração com troca simulada
    out['T22b'] = APG.t22b(base, None, gov1)
    out['T22b_calibracao_troca_so_presidente'] = {}
    for s in (0.02, 0.036):
        r = t22b_com_troca(base, gov1, s)
        out['T22b_calibracao_troca_so_presidente'][str(s)] = {'D': r['D_proprio_Flavio_menos_aliado'],
                                                               'proprio_Flavio': r['presidente_Flavio']['proprio_1T']}

    # 5) T39 em 2026
    out['T39'] = {'2026': t39(base, set(UFS6))}
    del base; gc.collect()
    for ano, p in (('2018', p18), ('2022', p22)):
        d = carregar(p)
        out['T39'][ano] = t39(d)
        del d; gc.collect()

    # 6) T5 nas 6 UFs, 1º e 2º turno, pelo script existente sem mudança (ler junto, Adendo 9)
    import subprocess
    sc = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'analisar_pres_gov_nivel.py')
    out['T5_rodado_aqui'] = {}
    for t in ('1', '2'):
        r = subprocess.run([sys.executable, '-I', sc, p26, t, '--ufs', ','.join(UFS6)], capture_output=True, text=True)
        out['T5_rodado_aqui'][t] = json.loads(r.stdout) if r.returncode == 0 else 'erro: ' + r.stderr[-300:]
    p5 = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'resultados', 'T5_2026_2t.json')
    if os.path.exists(p5):
        out['T5_2turno_bweb_lido_de'] = p5
        out['T5_2turno_bweb'] = json.load(open(p5))

    with open(saida, 'w') as f:
        json.dump(out, f, ensure_ascii=False, indent=1)
    print('ok', saida)


if __name__ == '__main__':
    main()
