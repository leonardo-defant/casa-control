"""L3 do Adendo 18: o núcleo do PL perde eleitor para Lula? (bweb completo dos dois turnos de 2026)

Registro (PRE-REGISTRO-2026-10-26.md, Adendo 18, commit bc7decb de 2026-10-29 05:13:35 UTC, antes de rodar):
  - Lógica: o eleitor mais partidário é o que menos troca de lado. Se Flávio perdeu eleitores por comportamento, a
    perda tem de ser pequena onde o PL é muito forte. Se uma fração fixa dos votos dele foi desviada, a perda fica
    parecida em todo lugar.
  - Força do PL na seção: fatia do PL (nominal mais legenda, número 22) nos votos válidos para deputado federal no 1º
    turno de 2026, na mesma urna. Quintis de seções por essa fatia.
  - Em cada quintil, a regressão do T8 (ganho de Flávio contra os votos de cada grupo no 1º turno, a queda do
    branco+nulo e a variação do comparecimento; efeito fixo de local; erro agrupado por local); guarda o coeficiente
    dos próprios votos de Flávio (P1 a P5). O mesmo para Lula com a fatia do PT para deputado federal.
  - Incoerência a favor da tese: P5 (núcleo do PL) de -0,03 ou menos, a mais de 3 erros-padrão, e P5 não menor que P1
    em valor absoluto por mais de 0,01. Coerente com comportamento: |P5| até metade de |P1|. Entre os dois:
    inconclusivo.

Especificação fixada neste arquivo antes de calcular qualquer coeficiente por quintil (o que o registro não fixou; tudo
listado também no texto de saída como leitura ou desvio):
  1. Deputado federal do 1º turno: linhas CD_CARGO_PERGUNTA 6 dos 28 zips do bweb do 1º turno (05/10, 14h03). Por
     seção: nominal (CD_TIPO_VOTAVEL 1), legenda (4), branco (2), nulo (3); do partido p, nominal com NR_PARTIDO p mais
     legenda com NR_PARTIDO p. Válidos = nominal + legenda, como o bweb os traz (voto em candidato com registro
     anulado depois continua nominal no arquivo; o bweb não separa). Conferências: comparecimento das linhas de
     deputado federal igual ao da base (presidente) e nominal + legenda + branco + nulo igual ao comparecimento.
  2. Universo: seções da base com os dois turnos e com válidos para deputado federal maiores que zero. O exterior (ZZ)
     não vota para deputado e fica de fora.
  3. Fatia do PL = (nominal 22 + legenda 22) / válidos. Fatia do PT = (nominal 13 + legenda 13) / válidos.
  4. Quintis: pontos de corte nos percentis 20, 40, 60 e 80 da fatia entre as seções do universo, sem peso
     (numpy.quantile linear). Q1: fatia <= p20; Q2: p20 < fatia <= p40; ...; Q5: fatia > p80. Os mesmos cortes para
     Lula com a fatia do PT. Q5 é o núcleo do partido.
  5. Regressão do T8 como registrada para 2026 (analisar_fluxo_regressao.py e analisar_T7_T14.t8): y = votos do
     candidato no 2º turno menos no 1º; X = votos de Cury (70), Renan (14), Caiado (55), Zema (30) e demais no 1º
     turno, queda do branco+nulo (1º menos 2º, sem truncar), variação do comparecimento (2º menos 1º), votos do
     adversário no 1º turno e votos do próprio no 1º turno; efeito fixo de local (UF|município|zona|local do 2º
     turno, lib.chave_local), sem peso, erro agrupado por local (lib.fe_ols, CR1). Rodada separadamente dentro de
     cada quintil: locais com uma seção só dentro do quintil saem (não informam).
  6. P_q = coeficiente dos próprios votos no 1º turno (proprio_1T) no quintil q.
  7. Veredito (PL): INCOERÊNCIA se P5 <= -0,03, P5/ep(P5) < -3 e |P1| - |P5| <= 0,01. COERENTE se |P5| <= |P1|/2.
     Senão INCONCLUSIVO. "A mais de 3 erros-padrão" lido de zero (principal, leitura mais literal); ao lado, a leitura
     do próprio limiar ((P5 + 0,03)/ep < -3). As duas condições de INCOERÊNCIA e COERENTE não podem valer juntas
     (exigiriam |P1| <= 0,02 e |P5| >= 0,03 ao mesmo tempo).
  8. Lula com o PT: as mesmas regras, relatadas como espelho (o registro escreve o critério para o núcleo do PL; a tese
     é de desvio contra Flávio).
  Fora do critério (não muda o veredito), escolhido antes de ver P1 a P5:
  - covariância conjunta dos cinco quintis (empilhados, efeito fixo de local por quintil, erro agrupado por local) para
    o erro-padrão de |P1| - |P5| e de P5 - P1;
  - T8 sem grupos (outros agregados); topo de 10% e de 5% da fatia; fatia da federação do PT (13, 65 e 43) para Lula;
  - P por quintil do PL dentro de faixas da fatia de Lula no 1º turno da seção (35%, 50%, 65%), para separar a força
    do partido da força local do adversário (o T35 já mostrou que a perda de Flávio cresce com a força de Lula);
  - P por quintil da fatia do próprio Flávio no 1º turno (comparação);
  - calibração: desvio simulado de uma fração fixa s dos votos de Flávio no 2º turno para Lula, por cima dos dados
    (s = 1% e s que vira o resultado), e desvio do mesmo total concentrado onde Lula é forte (proporcional à fatia de
    Lula no 1º turno da seção), para ver o que o teste consegue e o que não consegue separar.

Uso: python3 -I analisar_L3.py <secoes2026.json.gz> <candidatos2026_1t.json.gz> <zips1t_dir> <cache_df.json.gz>
        <saida.json> <saida.txt>
"""
import os as _os, sys as _sys
_sys.path.insert(0, _os.path.dirname(_os.path.abspath(__file__)))
import csv, gc, glob, gzip, io, json, os, sys, time, zipfile
from multiprocessing import Pool
import numpy as np
from lib import carregar, chave_local, fe_ols
from analisar_pres_gov import ols_cluster

GRUPOS = [('Cury', '70'), ('Renan', '14'), ('Caiado', '55'), ('Zema', '30')]
NOMES = [g for g, _ in GRUPOS] + ['demais_outros', 'queda_branco_nulo', 'var_comparecimento', 'adversario_1T', 'proprio_1T']
NOMES_SG = ['outros_1T', 'queda_branco_nulo', 'var_comparecimento', 'adversario_1T', 'proprio_1T']
LIM_P5, Z_P5, TOL, METADE = -0.03, 3.0, 0.01, 0.5
# colunas do vetor de deputado federal por seção
DF = ['comp', 'nom', 'leg', 'bra', 'nul', 'pl_nom', 'pl_leg', 'pt_nom', 'pt_leg', 'pcdob', 'pv', 'linhas', 'comp_varia',
      'part_incoerente']
IDF = {c: i for i, c in enumerate(DF)}


def log(msg):
    print(time.strftime('%H:%M:%S'), msg, file=sys.stderr, flush=True)


# ---------------------------------------------------------------- leitura do deputado federal (1º turno)

def ler_zip(zpath):
    z = zipfile.ZipFile(zpath)
    nome = [n for n in z.namelist() if n.lower().endswith('.csv')][0]
    out = {}; linhas = 0; passaram = 0; fallback = 0; por_numero = {}
    pat = b';6;"Deputado Federal";'
    with z.open(nome) as fh:
        cab = [c.strip().strip('"') for c in fh.readline().decode('latin1').strip().split(';')]
        cab = [c.replace('SG_ UF', 'SG_UF') for c in cab]
        ix = {c: i for i, c in enumerate(cab)}; nc = len(cab)
        iu, im, iz, iS = ix['SG_UF'], ix['CD_MUNICIPIO'], ix['NR_ZONA'], ix['NR_SECAO']
        icg, ip, ico, it, iv, iq = (ix['CD_CARGO_PERGUNTA'], ix['NR_PARTIDO'], ix['QT_COMPARECIMENTO'], ix['CD_TIPO_VOTAVEL'],
                                    ix['NR_VOTAVEL'], ix['QT_VOTOS'])
        for linha in fh:
            linhas += 1
            if pat not in linha:
                continue
            f = linha.decode('latin1').rstrip('\r\n').split(';')
            if len(f) != nc:
                f = next(csv.reader([linha.decode('latin1')], delimiter=';')); fallback += 1
            else:
                f = [x[1:-1] if len(x) >= 2 and x[0] == '"' and x[-1] == '"' else x for x in f]
            if f[icg] != '6':
                continue
            passaram += 1
            k = f"{f[iu]}|{int(f[im])}|{int(f[iz])}|{int(f[iS])}"
            s = out.get(k)
            comp = int(f[ico])
            if s is None:
                s = out[k] = [0] * len(DF); s[0] = comp
            elif s[0] != comp:
                s[IDF['comp_varia']] = 1
            s[IDF['linhas']] += 1
            tv = f[it]; q = int(f[iq]); p = f[ip]; nv = f[iv]
            ch = f[iu] + '|' + nv
            por_numero[ch] = por_numero.get(ch, 0) + q
            if tv == '1' or tv == '4':
                s[IDF['nom' if tv == '1' else 'leg']] += q
                if not nv.startswith(p):
                    s[IDF['part_incoerente']] += 1
                if p == '22':
                    s[IDF['pl_nom' if tv == '1' else 'pl_leg']] += q
                elif p == '13':
                    s[IDF['pt_nom' if tv == '1' else 'pt_leg']] += q
                elif p == '65':
                    s[IDF['pcdob']] += q
                elif p == '43':
                    s[IDF['pv']] += q
            elif tv == '2':
                s[IDF['bra']] += q
            elif tv == '3':
                s[IDF['nul']] += q
            else:
                s[IDF['part_incoerente']] += 1000000   # tipo inesperado: marca
    return os.path.basename(zpath), out, {'linhas': linhas, 'deputado_federal': passaram, 'fallback_csv': fallback,
                                          'votos_por_numero': por_numero}


def extrair(zdir, cache):
    if os.path.exists(cache):
        log(f'cache {cache}')
        with gzip.open(cache, 'rt') as f:
            return json.load(f)
    zips = sorted(glob.glob(os.path.join(zdir, '*.zip')), key=lambda p: -os.path.getsize(p))
    tudo = {}; meta = {}
    with Pool(4) as pool:
        for nome, out, m in pool.imap_unordered(ler_zip, zips):
            log(f'{nome}: {m["deputado_federal"]} linhas de deputado federal, {len(out)} seções')
            meta[nome] = m
            for k, v in out.items():
                if k in tudo:
                    meta.setdefault('_duplicadas', []).append(k)
                tudo[k] = v
    res = {'colunas': DF, 'secoes': tudo, 'meta': meta}
    os.makedirs(os.path.dirname(cache), exist_ok=True)
    with gzip.open(cache, 'wt') as f:
        json.dump(res, f, separators=(',', ':'))
    return res


# ---------------------------------------------------------------- matriz por seção

COL = ['L1', 'R1', 'O1', 'B1', 'N1', 'comp1', 'L2', 'R2', 'B2', 'N2', 'comp2']
C = {n: i for i, n in enumerate(COL)}


def montar(d, cand, dfe):
    rows, G, locs, ufs, keys, dfr = [], [], [], [], [], []
    conf = {'secoes_dois_turnos': 0, 'exterior': 0, 'sem_deputado_federal': 0, 'validos_df_zero': 0,
            'comp_df_diferente_da_base': 0, 'soma_df_diferente_do_comp': 0, 'comp_varia_entre_linhas': 0,
            'linhas_partido_incoerente': 0, 'secoes_df_fora_da_base': 0}
    exemplos = {'comp_df_diferente_da_base': [], 'soma_df_diferente_do_comp': []}
    dif_comp = []; dif_uf = {}
    base_keys = set()
    for k, v in d.items():
        base_keys.add(k)
        if '1' not in v or '2' not in v:
            continue
        conf['secoes_dois_turnos'] += 1
        uf = k.split('|')[0]
        if uf == 'ZZ':
            conf['exterior'] += 1; continue
        s = dfe.get(k)
        if s is None:
            conf['sem_deputado_federal'] += 1; continue
        a, b = v['1'], v['2']
        if s[IDF['comp']] != a['comp']:
            conf['comp_df_diferente_da_base'] += 1
            dif_comp.append(a['comp'] - s[IDF['comp']]); dif_uf[uf] = dif_uf.get(uf, 0) + 1
            if len(exemplos['comp_df_diferente_da_base']) < 10:
                exemplos['comp_df_diferente_da_base'].append([k, s[IDF['comp']], a['comp']])
        soma = s[IDF['nom']] + s[IDF['leg']] + s[IDF['bra']] + s[IDF['nul']]
        if soma != s[IDF['comp']]:
            conf['soma_df_diferente_do_comp'] += 1
            if len(exemplos['soma_df_diferente_do_comp']) < 10:
                exemplos['soma_df_diferente_do_comp'].append([k, soma, s[IDF['comp']]])
        conf['comp_varia_entre_linhas'] += s[IDF['comp_varia']]
        conf['linhas_partido_incoerente'] += s[IDF['part_incoerente']]
        if s[IDF['nom']] + s[IDF['leg']] <= 0:
            conf['validos_df_zero'] += 1; continue
        cv = cand.get(k, {})
        rows.append([a['L'], a['R'], a['O'], a['B'], a['N'], a['comp'], b['L'], b['R'], b['B'], b['N'], b['comp']])
        G.append([cv.get(n, 0) for _, n in GRUPOS])
        dfr.append(s[:11]); locs.append(chave_local(k, b)); ufs.append(uf); keys.append(k)
    conf['secoes_df_fora_da_base'] = sum(1 for k in dfe if k not in base_keys)
    dc = np.array(dif_comp) if dif_comp else np.zeros(1)
    conf['diferenca_comp_presidente_menos_deputado'] = {
        'secoes_deputado_menor': int((dc > 0).sum()), 'secoes_deputado_maior': int((dc < 0).sum()),
        'eleitores_a_mais_no_presidente': int(dc[dc > 0].sum()), 'mediana': float(np.median(dc)), 'maximo': int(dc.max()),
        'por_UF': dict(sorted(dif_uf.items(), key=lambda kv: -kv[1]))}
    A = np.array(rows, np.int64); Gm = np.array(G, np.int64); D = np.array(dfr, np.int64)
    _, loc = np.unique(np.array(locs), return_inverse=True)
    return {'A': A, 'G': Gm, 'D': D, 'loc': loc, 'uf': np.array(ufs), 'keys': np.array(keys)}, conf, exemplos


def matriz_t8(B, c, grupos=True, A=None):
    A = B['A'] if A is None else A
    adv = 'R' if c == 'L' else 'L'
    y = (A[:, C[c + '2']] - A[:, C[c + '1']]).astype(float)
    rabo = [(A[:, C['B1']] + A[:, C['N1']]) - (A[:, C['B2']] + A[:, C['N2']]), A[:, C['comp2']] - A[:, C['comp1']],
            A[:, C[adv + '1']], A[:, C[c + '1']]]
    if grupos:
        X = np.column_stack([B['G'], A[:, C['O1']] - B['G'].sum(1)] + rabo).astype(float); nomes = NOMES
    else:
        X = np.column_stack([A[:, C['O1']]] + rabo).astype(float); nomes = NOMES_SG
    return y, X, nomes


def t8(B, c, mask, grupos=True, A=None, y=None):
    y0, X, nomes = matriz_t8(B, c, grupos, A)
    y = y0 if y is None else y
    r = fe_ols(y[mask], X[mask], B['loc'][mask], None, nomes)
    return {'secoes': int(mask.sum()), 'n_informativas': r['n'], 'locais': r['grupos'],
            'P': r['coef']['proprio_1T'], 'ep': r['ep']['proprio_1T'], 'coef': r['coef'], 'ep_todos': r['ep']}


def quintis(x, cortes):
    return np.searchsorted(cortes, x, side='left')   # x <= c0 -> 0; c0 < x <= c1 -> 1; ...; x > c3 -> 4


def conjunto(B, c, q, grupos=True):
    """Os cinco quintis empilhados: efeito fixo de local por quintil, todos os coeficientes por quintil, erro agrupado
    por local. Os pontos são os mesmos das regressões separadas; dá a covariância entre quintis."""
    y, X, nomes = matriz_t8(B, c, grupos)
    k = X.shape[1]; n = len(y)
    XX = np.zeros((n, 5 * k))
    for j in range(5):
        m = q == j
        XX[m, j * k:(j + 1) * k] = X[m]
    fe = B['loc'] * 5 + q
    b, V, N, Gc = ols_cluster(y, XX, fe, B['loc'])
    ip = [j * k + nomes.index('proprio_1T') for j in range(5)]
    P = b[ip]; Vp = V[np.ix_(ip, ip)]
    s1 = np.sign(P[0]); s5 = np.sign(P[4])
    g = np.zeros(5); g[0] = s1; g[4] = -s5          # |P1| - |P5| (sinais fixos no ponto)
    h = np.zeros(5); h[4] = 1; h[0] = -1           # P5 - P1
    return {'P': P.tolist(), 'ep': np.sqrt(np.diag(Vp)).tolist(), 'linhas': N, 'locais': Gc,
            'absP1_menos_absP5': [float(abs(P[0]) - abs(P[4])), float(np.sqrt(g @ Vp @ g))],
            'P5_menos_P1': [float(P[4] - P[0]), float(np.sqrt(h @ Vp @ h))],
            'correlacao_P1_P5': float(Vp[0, 4] / np.sqrt(Vp[0, 0] * Vp[4, 4])),
            'correlacoes': (Vp / np.sqrt(np.outer(np.diag(Vp), np.diag(Vp)))).round(4).tolist()}


def veredito(P1, P5, ep5):
    inc = P5 <= LIM_P5 and P5 / ep5 < -Z_P5 and abs(P1) - abs(P5) <= TOL
    inc_lim = P5 <= LIM_P5 and (P5 - LIM_P5) / ep5 < -Z_P5 and abs(P1) - abs(P5) <= TOL
    coe = abs(P5) <= METADE * abs(P1)
    v = 'INCOERÊNCIA' if inc else 'COERENTE' if coe else 'INCONCLUSIVO'
    v2 = 'INCOERÊNCIA' if inc_lim else 'COERENTE' if coe else 'INCONCLUSIVO'
    return {'veredito_z_de_zero': v, 'veredito_z_do_limiar': v2,
            'condicoes': {'P5<=-0,03': bool(P5 <= LIM_P5), 'z_P5_de_zero': P5 / ep5, 'z_P5_do_limiar': (P5 - LIM_P5) / ep5,
                          '|P1|-|P5|': abs(P1) - abs(P5), '|P5|/|P1|': abs(P5) / abs(P1) if P1 else None,
                          '|P5|<=|P1|/2': bool(coe)}}


def descr(B, m, c, fat):
    A = B['A'][m]
    V1 = (A[:, C['L1']] + A[:, C['R1']] + A[:, C['O1']]).sum()
    adv = 'R' if c == 'L' else 'L'
    D = B['D'][m]; val = (D[:, IDF['nom']] + D[:, IDF['leg']]).sum()
    return {'secoes': int(m.sum()), 'fatia_min': float(fat[m].min()), 'fatia_max': float(fat[m].max()),
            'fatia_media_secoes': float(fat[m].mean()),
            'fatia_agregada': float(((D[:, IDF['pl_nom']] + D[:, IDF['pl_leg']]) if c == 'R' else
                                     (D[:, IDF['pt_nom']] + D[:, IDF['pt_leg']])).sum() / val),
            'proprio_pct_validos_pres_1T': float(100 * A[:, C[c + '1']].sum() / V1),
            'adversario_pct_validos_pres_1T': float(100 * A[:, C[adv + '1']].sum() / V1),
            'proprio_pct_finalistas_2T': float(100 * A[:, C[c + '2']].sum() / (A[:, C['L2']] + A[:, C['R2']]).sum()),
            'votos_proprio_1T': int(A[:, C[c + '1']].sum()), 'votos_proprio_2T': int(A[:, C[c + '2']].sum()),
            'ganho_bruto': int((A[:, C[c + '2']] - A[:, C[c + '1']]).sum())}


def bloco(B, c, fat, cortes, rotulo, A=None, y=None, grupos=True, extra_mask=None):
    q = quintis(fat, cortes)
    out = []
    for j in range(5):
        m = q == j
        if extra_mask is not None:
            m = m & extra_mask
        if m.sum() < 50:
            out.append({'quintil': j + 1, 'secoes': int(m.sum()), 'P': None, 'ep': None}); continue
        try:
            r = t8(B, c, m, grupos, A, y)
        except Exception as e:  # noqa
            out.append({'quintil': j + 1, 'secoes': int(m.sum()), 'P': None, 'ep': None, 'erro': str(e)}); continue
        out.append({'quintil': j + 1, **{kk: r[kk] for kk in ('secoes', 'n_informativas', 'locais', 'P', 'ep')}})
    return out


def main():
    a26, cand26, zdir, cache, saida_json, saida_txt = sys.argv[1:7]
    t0 = time.time()
    log('lendo deputado federal do 1º turno')
    ex = extrair(zdir, cache)
    dfe = ex['secoes']
    log(f'{len(dfe)} seções com deputado federal')
    d = carregar(a26); cand = carregar(cand26)['secoes']
    B, conf, exemplos = montar(d, cand, dfe)
    del d, cand; gc.collect()
    n = len(B['A']); log(f'universo {n} seções')
    D = B['D']; val = (D[:, IDF['nom']] + D[:, IDF['leg']]).astype(float)
    fPL = (D[:, IDF['pl_nom']] + D[:, IDF['pl_leg']]) / val
    fPT = (D[:, IDF['pt_nom']] + D[:, IDF['pt_leg']]) / val
    fFED = (D[:, IDF['pt_nom']] + D[:, IDF['pt_leg']] + D[:, IDF['pcdob']] + D[:, IDF['pv']]) / val
    A = B['A']
    Vp1 = (A[:, C['L1']] + A[:, C['R1']] + A[:, C['O1']]).astype(float)
    fL1 = np.where(Vp1 > 0, A[:, C['L1']] / np.maximum(Vp1, 1), np.nan)
    fR1 = np.where(Vp1 > 0, A[:, C['R1']] / np.maximum(Vp1, 1), np.nan)
    cPL = np.quantile(fPL, [.2, .4, .6, .8]); cPT = np.quantile(fPT, [.2, .4, .6, .8])
    qPL = quintis(fPL, cPL); qPT = quintis(fPT, cPT)
    res = {'teste': 'L3', 'registro': 'PRE-REGISTRO-2026-10-26.md, Adendo 18 (commit bc7decb, 2026-10-29 05:13:35 UTC)',
           'conferencias': conf, 'exemplos_conferencia': exemplos, 'leitura_zips': ex['meta'], 'universo_secoes': n,
           'universo_locais': int(len(np.unique(B['loc'])))}
    tot = D.sum(0)
    res['totais_deputado_federal_universo'] = {c: int(tot[i]) for i, c in enumerate(DF[:11])}
    tot_all = np.array([v[:11] for v in dfe.values()], np.int64).sum(0)
    res['totais_deputado_federal_bweb_todas_as_secoes'] = {c: int(tot_all[i]) for i, c in enumerate(DF[:11])}
    res['cortes'] = {'PL': cPL.tolist(), 'PT': cPT.tolist()}
    res['contagem_quintis'] = {'PL': np.bincount(qPL, minlength=5).tolist(), 'PT': np.bincount(qPT, minlength=5).tolist()}
    res['correlacoes_secao'] = {'fatia_PL_x_fatia_Flavio_1T': float(np.corrcoef(fPL, np.nan_to_num(fR1))[0, 1]),
                                'fatia_PT_x_fatia_Lula_1T': float(np.corrcoef(fPT, np.nan_to_num(fL1))[0, 1]),
                                'fatia_PL_x_fatia_PT': float(np.corrcoef(fPL, fPT)[0, 1])}
    todos = np.ones(n, bool)
    # ------------------------------------------------ principal
    principal = {}
    for c, fat, cortes, q, nome in (('R', fPL, cPL, qPL, 'Flavio_PL'), ('L', fPT, cPT, qPT, 'Lula_PT')):
        log(f'principal {nome}')
        geral = t8(B, c, todos)
        qs = []
        for j in range(5):
            m = q == j
            r = t8(B, c, m)
            qs.append({'quintil': j + 1, **{kk: r[kk] for kk in ('secoes', 'n_informativas', 'locais', 'P', 'ep')},
                       'coef': r['coef'], 'ep_todos': r['ep_todos'], 'descritivo': descr(B, m, c, fat)})
            log(f'  Q{j+1}: P {r["P"]:+.4f} ({r["ep"]:.4f}) n {r["n_informativas"]} locais {r["locais"]}')
        P1, P5, ep5 = qs[0]['P'], qs[4]['P'], qs[4]['ep']
        principal[nome] = {'geral_universo': {kk: geral[kk] for kk in ('secoes', 'n_informativas', 'locais', 'P', 'ep')},
                           'quintis': qs, 'veredito': veredito(P1, P5, ep5), 'conjunto': conjunto(B, c, q)}
        # perda líquida em votos por quintil (P x votos próprios do 1º turno das seções informativas aproximadas pelo quintil)
        principal[nome]['perda_liquida_votos_aprox'] = [float(-x['P'] * x['descritivo']['votos_proprio_1T']) for x in qs]
    res['principal'] = principal
    # ------------------------------------------------ robustez
    rob = {}
    log('robustez: sem grupos')
    rob['sem_grupos_PL'] = bloco(B, 'R', fPL, cPL, 'PL', grupos=False)
    rob['sem_grupos_PT'] = bloco(B, 'L', fPT, cPT, 'PT', grupos=False)
    log('robustez: topo')
    for c, fat, nome in (('R', fPL, 'PL'), ('L', fPT, 'PT')):
        for p in (0.90, 0.95):
            corte = float(np.quantile(fat, p)); m = fat > corte
            r = t8(B, c, m); rob[f'topo_{int(round(100*(1-p)))}pct_{nome}'] = {'corte': corte, **{kk: r[kk] for kk in ('secoes', 'n_informativas', 'locais', 'P', 'ep')}, 'descritivo': descr(B, m, c, fat)}
        for p in (0.10, 0.05):
            corte = float(np.quantile(fat, p)); m = fat <= corte
            r = t8(B, c, m); rob[f'base_{int(round(100*p))}pct_{nome}'] = {'corte': corte, **{kk: r[kk] for kk in ('secoes', 'n_informativas', 'locais', 'P', 'ep')}, 'descritivo': descr(B, m, c, fat)}
    log('robustez: federação do PT')
    cFED = np.quantile(fFED, [.2, .4, .6, .8]); rob['federacao_PT_cortes'] = cFED.tolist()
    rob['federacao_PT'] = bloco(B, 'L', fFED, cFED, 'FED')
    log('robustez: faixas de Lula')
    faixas = {}
    for lo, hi in ((0, .35), (.35, .50), (.50, .65), (.65, 1.01)):
        fm = (fL1 >= lo) & (fL1 < hi)
        faixas[f'{int(100*lo)}-{min(100, int(100*hi))}'] = {'secoes': int(fm.sum()),
                                                            'contagem_quintis_PL': np.bincount(qPL[fm], minlength=5).tolist(),
                                                            'P_por_quintil_PL': bloco(B, 'R', fPL, cPL, 'PL', extra_mask=fm)}
    rob['Flavio_por_quintil_PL_dentro_da_faixa_de_Lula_na_secao'] = faixas
    faixasR = {}
    for lo, hi in ((0, .35), (.35, .50), (.50, .65), (.65, 1.01)):
        fm = (fR1 >= lo) & (fR1 < hi)
        faixasR[f'{int(100*lo)}-{min(100, int(100*hi))}'] = {'secoes': int(fm.sum()),
                                                             'contagem_quintis_PT': np.bincount(qPT[fm], minlength=5).tolist(),
                                                             'P_por_quintil_PT': bloco(B, 'L', fPT, cPT, 'PT', extra_mask=fm)}
    rob['Lula_por_quintil_PT_dentro_da_faixa_de_Flavio_na_secao'] = faixasR
    agreg = {}
    for c, fa in (('R', fL1), ('L', fR1)):
        for lo, hi in ((0, .35), (.35, .50), (.50, .65), (.65, 1.01)):
            fm = (fa >= lo) & (fa < hi)
            r = t8(B, c, fm)
            agreg[f"{'Flavio' if c == 'R' else 'Lula'}_adversario_{int(100*lo)}-{min(100, int(100*hi))}"] = {
                kk: r[kk] for kk in ('secoes', 'n_informativas', 'locais', 'P', 'ep')}
    rob['P_por_faixa_do_adversario_na_secao_todos_os_quintis'] = agreg
    log('robustez: quintis da fatia do próprio candidato')
    cR = np.quantile(fR1, [.2, .4, .6, .8]); cL = np.quantile(fL1, [.2, .4, .6, .8])
    rob['Flavio_por_quintil_da_propria_fatia_1T'] = {'cortes': cR.tolist(), 'q': bloco(B, 'R', fR1, cR, 'F')}
    rob['Lula_por_quintil_da_propria_fatia_1T'] = {'cortes': cL.tolist(), 'q': bloco(B, 'L', fL1, cL, 'L')}
    res['robustez'] = rob
    # ------------------------------------------------ calibração
    log('calibração')
    R2 = A[:, C['R2']].astype(float); L2 = A[:, C['L2']].astype(float)
    margem = L2.sum() - R2.sum()
    s_vira = (margem / 2) / (R2.sum() + margem / 2)
    cal = {'margem_universo': float(margem), 'R2_universo': float(R2.sum()), 'L2_universo': float(L2.sum()),
           's_que_vira_o_resultado_sobre_o_universo': float(s_vira), 'cenarios': {}}
    def com_desvio(desv):
        A2 = A.astype(float).copy(); A2[:, C['R2']] -= desv; A2[:, C['L2']] += desv
        return A2
    m_L = np.nan_to_num(A[:, C['L1']] / np.maximum(A[:, C['L1']] + A[:, C['R1']], 1))
    for nome, desv in (('uniforme_1pct', 0.01 * R2), (f'uniforme_que_vira_{100*s_vira:.2f}pct', s_vira * R2),
                       ('concentrado_onde_Lula_e_forte_mesmo_total_que_vira', None)):
        if desv is None:
            w = m_L * R2; desv = w * (s_vira * R2.sum() / w.sum())
        A2 = com_desvio(desv)
        cen = {'votos_desviados': float(desv.sum())}
        for c, fat, cortes, rot in (('R', fPL, cPL, 'Flavio_PL'), ('L', fPT, cPT, 'Lula_PT')):
            qq = bloco(B, c, fat, cortes, rot, A=A2)
            cen[rot] = [{'quintil': x['quintil'], 'P': x['P'], 'ep': x['ep'],
                         'deslocamento': x['P'] - res['principal'][rot]['quintis'][i]['P']} for i, x in enumerate(qq)]
            cen[rot + '_veredito'] = veredito(qq[0]['P'], qq[4]['P'], qq[4]['ep'])
        cal['cenarios'][nome] = cen
        log(f'  {nome}: PL ' + ' '.join(f"{x['P']:+.4f}" for x in cen['Flavio_PL']))
    # inclinação: deslocamento de P5 por ponto de desvio uniforme e limite de desvio uniforme compatível com P5 >= 0
    dsl = cal['cenarios']['uniforme_1pct']['Flavio_PL'][4]['deslocamento'] / 0.01
    P5, ep5 = res['principal']['Flavio_PL']['quintis'][4]['P'], res['principal']['Flavio_PL']['quintis'][4]['ep']
    cal['deslocamento_de_P5_por_unidade_de_s'] = dsl
    cal['s_uniforme_maximo_se_o_nucleo_nao_perde_nada'] = {
        'ponto': float(max(0.0, -P5) / -dsl), 'com_2_ep': float(max(0.0, -P5 + 2 * ep5) / -dsl),
        'premissa': 'P5 verdadeiro (sem desvio) >= 0, isto é, o núcleo do PL não perde eleitor líquido para Lula'}
    res['calibracao'] = cal
    # referência já calculada no T35 (faixa de menos de 35% do adversário no local), só para o texto
    t35p = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'resultados', 'T35_curva_forca_bweb.json')
    if os.path.exists(t35p):
        with open(t35p) as f:
            t35 = json.load(f)['2026']['faixas'][0]
        res['referencia_T35_faixa_0_35'] = {'faixa': t35['faixa'], 'R': t35['proprio_R'], 'L': t35['proprio_L'],
                                            'fonte': 'resultados/T35_curva_forca_bweb.json'}
    t8p = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'resultados', 'T7_T14_bweb.json')
    if os.path.exists(t8p):
        with open(t8p) as f:
            t8r = json.load(f)['2026']['T8_Flavio_com_grupos']
        res['referencia_T8_registrado'] = [t8r['coef']['proprio_1T'], t8r['ep']['proprio_1T']]
    res['segundos'] = time.time() - t0
    with open(saida_json, 'w') as f:
        json.dump(res, f, ensure_ascii=False, indent=1)
    escrever_txt(res, saida_txt)
    log('fim')


# ---------------------------------------------------------------- texto

def br(x, nd=3, sinal=False):
    if x is None:
        return 'n/d'
    s = f'{x:+,.{nd}f}' if sinal else f'{x:,.{nd}f}'
    return s.replace(',', '#').replace('.', ',').replace('#', '.')


def bi(x):
    return f'{int(x):,}'.replace(',', '.')


NIKOLAS_IMPRENSA = (3119318, 'imprensa de 05/10/2026, achado por busca na web: gazetasp.com.br e congressoemfoco.com.br')


def pc(x, nd=1):
    return br(100 * x, nd)


def escrever_txt(res, caminho):
    L = []; w = L.append
    pr = res['principal']; F = pr['Flavio_PL']; T = pr['Lula_PT']; rob = res['robustez']; cal = res['calibracao']
    cf = res['conferencias']; tot = res['totais_deputado_federal_bweb_todas_as_secoes']
    qF = F['quintis']; qT = T['quintis']
    P1, P5, e1, e5 = qF[0]['P'], qF[4]['P'], qF[0]['ep'], qF[4]['ep']
    vF = F['veredito']; vT = T['veredito']; cj = F['conjunto']; cjT = T['conjunto']
    cPL, cPT = res['cortes']['PL'], res['cortes']['PT']
    cen = cal['cenarios']; nomes_cen = list(cen)
    cu1, cuv, cco = cen[nomes_cen[0]], cen[nomes_cen[1]], cen[nomes_cen[2]]
    sv = cal['s_que_vira_o_resultado_sobre_o_universo']
    ag = rob['P_por_faixa_do_adversario_na_secao_todos_os_quintis']
    fx = rob['Flavio_por_quintil_PL_dentro_da_faixa_de_Lula_na_secao']
    smax = cal['s_uniforme_maximo_se_o_nucleo_nao_perde_nada']
    dsl = -cal['deslocamento_de_P5_por_unidade_de_s']
    PT5 = qT[4]['P']
    s_ref_pt = max(0.0, (-P5) - (-PT5)) / dsl
    s_ref_pt2 = max(0.0, (-P5 + 2 * e5) - (-PT5 - 2 * qT[4]['ep'])) / dsl
    fl35, lu35 = ag['Flavio_adversario_0-35'], ag['Lula_adversario_0-35']
    t35 = res.get('referencia_T35_faixa_0_35')
    niko = None
    for z, m in res['leitura_zips'].items():
        if z.startswith('_'):
            continue
        if 'MG' in z:
            niko = m.get('votos_por_numero', {}).get('MG|2222')
    val = tot['nom'] + tot['leg']; pl = tot['pl_nom'] + tot['pl_leg']; pt = tot['pt_nom'] + tot['pt_leg']
    linhas_df = sum(m['deputado_federal'] for z, m in res['leitura_zips'].items() if not z.startswith('_'))
    fb = sum(m['fallback_csv'] for z, m in res['leitura_zips'].items() if not z.startswith('_'))
    dcp = cf['diferenca_comp_presidente_menos_deputado']
    dif_faixa = {b: (v['P_por_quintil_PL'][4]['P'] - v['P_por_quintil_PL'][0]['P']) for b, v in fx.items()
                 if v['P_por_quintil_PL'][0]['P'] is not None and v['P_por_quintil_PL'][4]['P'] is not None}
    dmin, dmax = min(dif_faixa.values()), max(dif_faixa.values())
    t8reg = res.get('referencia_T8_registrado')

    w('L3. O núcleo do PL: quem é do PL perde eleitor para Lula? (Adendo 18), com o bweb completo dos dois turnos de 2026')
    w('Script: scripts/analisar_L3.py. Números completos: resultados/L3_bweb.json.')
    w('Rodado em 2026-10-29 com a base por seção dos dois turnos (secoes2026.json.gz), os votos por candidato a presidente no 1º')
    w('turno por seção (candidatos2026_1t.json.gz) e as linhas de deputado federal dos 28 zips do bweb do 1º turno (05/10, 14h03),')
    w('sem baixar nada. Nenhuma outra eleição entra (Adendo 18).')
    w('')
    w('Critério registrado (PRE-REGISTRO-2026-10-26.md, Adendo 18, commit bc7decb de 29/10 05h13 UTC, antes de rodar):')
    w('- Lógica: o eleitor mais partidário é o que menos troca de lado. Se Flávio perdeu eleitores por comportamento, a perda tem')
    w('  de ser pequena onde o PL é muito forte. Se uma fração fixa dos votos dele foi desviada, a perda fica parecida em todo lugar.')
    w('- Força do PL na seção: fatia do PL (nominal mais legenda, número 22) nos válidos para deputado federal no 1º turno, na')
    w('  mesma urna. Quintis de seções por essa fatia. Em cada quintil, a regressão do T8, efeito fixo de local, erro agrupado por')
    w('  local; P1 a P5 = coeficiente dos próprios votos de Flávio. O mesmo para Lula com a fatia do PT.')
    w('- INCOERÊNCIA (a favor da tese): P5 de -0,03 ou menos, a mais de 3 erros-padrão, e P5 não menor que P1 em valor absoluto')
    w('  por mais de 0,01. COERENTE com comportamento: |P5| até metade de |P1|. Entre os dois: INCONCLUSIVO.')
    w('')
    w(f'VEREDITO PELA LETRA: {vF["veredito_z_de_zero"]}')
    w(f'- P1 (PL mais fraco) = {br(P1, 4, True)} (ep {br(e1, 4)}); P5 (núcleo do PL) = {br(P5, 4, True)} (ep {br(e5, 4)}).')
    w(f'  |P5| é {pc(abs(P5) / abs(P1), 0)}% de |P1|, abaixo da metade: COERENTE.')
    c_ = vF['condicoes']
    w(f'- Condições de INCOERÊNCIA: (a) P5 <= -0,03? {"sim" if c_["P5<=-0,03"] else "não"}, P5 fica {br(c_["z_P5_do_limiar"], 1)} ep acima do limiar.')
    w(f'  (b) |P1| - |P5| <= 0,01? {"sim" if c_["|P1|-|P5|"] <= TOL else "não"}, a diferença é {br(c_["|P1|-|P5|"], 4)} (ep {br(cj["absP1_menos_absP5"][1], 4)}, covariância conjunta dos')
    w(f'  cinco quintis). Mesmo que P5 passasse do limiar de -0,03, a condição (b) falharia por {br((c_["|P1|-|P5|"] - TOL) / cj["absP1_menos_absP5"][1], 0)} erros-padrão.')
    w(f'- "A mais de 3 erros-padrão" lido a partir do limiar (e não de zero): {vF["veredito_z_do_limiar"]}, o mesmo veredito.')
    w(f'- Espelho, Lula com a fatia do PT (mesma regra): {vT["veredito_z_de_zero"]}. P1 = {br(qT[0]["P"], 4, True)} (ep {br(qT[0]["ep"], 4)}),')
    w(f'  P5 = {br(PT5, 4, True)} (ep {br(qT[4]["ep"], 4)}): Lula perdeu pouco em todo lugar e o núcleo do PT perdeu quase o mesmo que o resto.')
    w('')
    w('Resumo')
    d1, d5 = qF[0]['descritivo'], qF[4]['descritivo']
    w(f'- Onde o PL é fraco para deputado (até {pc(cPL[0])}% dos válidos; Lula com {br(d1["adversario_pct_validos_pres_1T"], 0)}% no 1º turno), Flávio perdeu,')
    w(f'  em termos líquidos, {pc(-P1)}% dos próprios eleitores do 1º turno. Onde o PL é o núcleo (acima de {pc(cPL[3])}%, média de')
    w(f'  {pc(d5["fatia_agregada"], 0)}%; Lula com {br(d5["adversario_pct_validos_pres_1T"], 0)}%), perdeu {pc(-P5)}%. A perda cai de forma contínua de um quintil para o')
    w('  outro. Uma fração fixa desviada em todo lugar deixaria a perda parecida nos cinco quintis; não é o que aparece.')
    w('- Mas o próprio teste mostra dois limites, e eles pesam:')
    w(f'  (1) A maior parte do degrau vem da força local de Lula, não do partido. Dentro de faixas de força de Lula na seção, a')
    w(f'      diferença entre Q5 e Q1 vai de {br(100 * dmin, 1, True)} a {br(100 * dmax, 1, True)} pontos, contra {br(100 * (P5 - P1), 1, True)} sem controlar (item 4).')
    w(f'  (2) Um desvio em fração fixa somado ao comportamento não achata o degrau, só o desloca. Simulado por cima dos dados, um desvio')
    w(f'      uniforme de {pc(sv, 2)}% dos votos de Flávio (o tamanho que vira o resultado) dá {cuv["Flavio_PL_veredito"]["veredito_z_de_zero"]} pela letra, não INCOERÊNCIA;')
    w(f'      o mesmo total concentrado onde Lula é forte dá {cco["Flavio_PL_veredito"]["veredito_z_de_zero"]}. COERENTE quer dizer "os dados têm o formato que o')
    w('      comportamento prevê". Não quer dizer "não houve desvio".')
    w('- O que o resultado ainda limita (leituras com premissa, fora do critério, item 5):')
    w(f'  se o núcleo do PL de fato não perdesse ninguém, o P5 observado comportaria um desvio uniforme de até {pc(smax["ponto"])}%')
    w(f'  ({pc(smax["com_2_ep"])}% com 2 erros-padrão), abaixo dos {pc(sv, 2)}% que viram o resultado. Se o núcleo de um partido perde')
    w(f'  naturalmente o que o núcleo do PT perdeu ({pc(-PT5)}%), sobra espaço para cerca de {pc(s_ref_pt)}% ({pc(s_ref_pt2)}% no limite de 2 ep).')
    w(f'  Onde Lula tem menos de 35% na seção, Flávio perde {pc(-fl35["P"])}% (ep {pc(fl35["ep"])}); onde Flávio tem menos de 35%, Lula perde')
    w(f'  {pc(-lu35["P"])}% (ep {pc(lu35["ep"])}). Nos redutos de cada um, os dois perdem o mesmo. Para caber um desvio uniforme do tamanho')
    w(f'  que vira o resultado, Flávio teria de ter, nos redutos dele, um desempenho real {br(100 * (dsl * sv + fl35["P"] - lu35["P"]), 1)} pontos melhor que o')
    w('  de Lula nos redutos de Lula (premissa: os dois campos se comportam igual onde dominam).')
    w(f'- O que fica em aberto: com a mesma força do adversário na seção, Flávio perde mais que Lula, e a diferença cresce com a força')
    w(f'  de Lula: {"; ".join(f"adversário {b.replace(chr(45), " a ")}%: Flávio {pc(-ag[f"Flavio_adversario_{b}"]["P"])}%, Lula {pc(-ag[f"Lula_adversario_{b}"]["P"])}%" for b in ("35-50", "50-65", "65-100"))}.')
    w('  É o que o T35 já tinha registrado. Tem o formato de um comportamento diferente entre os campos e também o de um desvio')
    w('  regulado pela força local de Lula, que poupa os redutos de Flávio. Este teste não separa os dois, nem o T35.')
    w('')
    w('1. Dados e conferências')
    w(f'- Linhas de deputado federal lidas: {bi(linhas_df)} (leitura pelo csv em {bi(fb)} linhas com ponto e vírgula dentro de um campo).')
    w('  Os zips do 1º turno e a base por seção já tinham sido conferidos antes (total oficial, testes anteriores).')
    w(f'- Seções com os dois turnos na base: {bi(cf["secoes_dois_turnos"])}; do exterior (sem deputado): {bi(cf["exterior"])}; sem linhas de deputado')
    w(f'  federal: {bi(cf["sem_deputado_federal"])}; com válidos zero: {bi(cf["validos_df_zero"])}. Universo: {bi(res["universo_secoes"])} seções em {bi(res["universo_locais"])} locais.')
    w(f'- Em todas as seções, nominal + legenda + branco + nulo de deputado federal = comparecimento das linhas de deputado')
    w(f'  ({bi(cf["soma_df_diferente_do_comp"])} diferenças). Número do votável começa com o número do partido em todas as linhas nominais e de')
    w(f'  legenda ({bi(cf["linhas_partido_incoerente"])} exceções). Comparecimento igual em todas as linhas da mesma seção ({bi(cf["comp_varia_entre_linhas"])} exceções).')
    ufs_ = ', '.join(f'{u} {bi(n)}' for u, n in list(dcp['por_UF'].items())[:5])
    w(f'- Comparecimento de deputado federal menor que o de presidente em {bi(dcp["secoes_deputado_menor"])} seções ({bi(dcp["eleitores_a_mais_no_presidente"])} eleitores')
    w(f'  ao todo, mediana {br(dcp["mediana"], 0)} por seção, máximo {bi(dcp["maximo"])}); maior em {bi(dcp["secoes_deputado_maior"])}. É o eleitor em trânsito de outra UF, que')
    w(f'  só vota para presidente ({ufs_}). A fatia do partido conta só quem votou para deputado; a regressão usa os')
    w('  votos de presidente, como registrado.')
    w(f'- Totais de deputado federal no bweb: válidos {bi(val)} (nominal {bi(tot["nom"])}, legenda {bi(tot["leg"])}); PL {bi(pl)}')
    w(f'  ({pc(pl / val, 2)}%); PT {bi(pt)} ({pc(pt / val, 2)}%); branco {bi(tot["bra"])}; nulo {bi(tot["nul"])}.')
    if niko is not None:
        w(f'- Conferência externa: Nikolas Ferreira (PL-MG, 2222) soma {bi(niko)} votos no bweb; publicado: {bi(NIKOLAS_IMPRENSA[0])}')
        w(f'  ({NIKOLAS_IMPRENSA[1]}). {"Igual." if niko == NIKOLAS_IMPRENSA[0] else "DIFERENTE."}')
    w(f'- Correlação entre seções: fatia do PL x fatia de Flávio no 1º turno {br(res["correlacoes_secao"]["fatia_PL_x_fatia_Flavio_1T"], 2)}; fatia do PT x fatia de')
    w(f'  Lula {br(res["correlacoes_secao"]["fatia_PT_x_fatia_Lula_1T"], 2)}. O voto no PT para deputado marca o eleitor de Lula bem menos do que o voto no PL marca o de Flávio.')
    w('')
    w('2. Flávio por quintil da fatia do PL (o teste)')
    w('   Quintil  fatia do PL (faixa; média)   Flávio/Lula 1T   seções  na regr.  locais   P (ep)              perda líquida aprox.')
    cortes = [0.0] + cPL + [1.0]
    for i, q in enumerate(qF):
        d = q['descritivo']
        w(f'   Q{q["quintil"]}       {pc(d["fatia_min"])} a {pc(d["fatia_max"])}%; {pc(d["fatia_agregada"])}%'.ljust(43) +
          f'{br(d["proprio_pct_validos_pres_1T"], 0)}% / {br(d["adversario_pct_validos_pres_1T"], 0)}%'.ljust(17) +
          f'{bi(q["secoes"])}'.rjust(7) + f'{bi(q["n_informativas"])}'.rjust(9) + f'{bi(q["locais"])}'.rjust(8) +
          f'   {br(q["P"], 4, True)} ({br(q["ep"], 4)})'.ljust(22) + f'{bi(F["perda_liquida_votos_aprox"][i])} votos')
    g = F['geral_universo']
    w(f'- Universo inteiro, mesma regressão: {br(g["P"], 4, True)} (ep {br(g["ep"], 4)}).' + (f' O T8 registrado, com o exterior, deu {br(t8reg[0], 4, True)} (ep {br(t8reg[1], 4)}).' if t8reg else ''))
    w(f'- Empilhado (covariância conjunta): P5 - P1 = {br(cj["P5_menos_P1"][0], 4, True)} (ep {br(cj["P5_menos_P1"][1], 4)}, z {br(cj["P5_menos_P1"][0] / cj["P5_menos_P1"][1], 1)}).')
    w(f'  A perda cai a cada quintil: {" > ".join(pc(-q["P"], 1) + "%" for q in qF)}.')
    w('- "Perda líquida aprox." = -P vezes os votos de Flávio no 1º turno do quintil (inclui as seções que saem da regressão).')
    w('- Conferência por outro caminho (feita à mão em 29/10, fora deste script): as listas de seções do Q1 e do Q5 refeitas por código')
    w('  separado e rodadas no script registrado do T8 (analisar_fluxo_regressao.py, R, com os grupos Cury, Renan, Caiado e Zema)')
    w('  dão P1 = -0,081 (ep 0,002; 86.171 seções, 19.911 locais) e P5 = -0,029 (ep 0,001; 93.573 seções, 15.363 locais), os mesmos.')
    w('')
    w('3. Lula por quintil da fatia do PT (espelho, mesma regra)')
    for i, q in enumerate(qT):
        d = q['descritivo']
        w(f'   Q{q["quintil"]}       {pc(d["fatia_min"])} a {pc(d["fatia_max"])}%; {pc(d["fatia_agregada"])}%'.ljust(43) +
          f'{br(d["proprio_pct_validos_pres_1T"], 0)}% / {br(d["adversario_pct_validos_pres_1T"], 0)}%'.ljust(17) +
          f'{bi(q["secoes"])}'.rjust(7) + f'{bi(q["n_informativas"])}'.rjust(9) + f'{bi(q["locais"])}'.rjust(8) +
          f'   {br(q["P"], 4, True)} ({br(q["ep"], 4)})'.ljust(22) + f'{bi(T["perda_liquida_votos_aprox"][i])} votos')
    w('   (colunas: fatia do PT; Lula/Flávio no 1º turno)')
    g = T['geral_universo']
    w(f'- Universo inteiro: {br(g["P"], 4, True)} (ep {br(g["ep"], 4)}). P5 - P1 = {br(cjT["P5_menos_P1"][0], 4, True)} (ep {br(cjT["P5_menos_P1"][1], 4)}).')
    w(f'- Leitura: {vT["veredito_z_de_zero"]} pela régua. Lula perde pouco em todos os quintis e o núcleo do PT não protege mais que o resto. Como o')
    w('  voto no PT para deputado marca pouco o eleitor de Lula (item 1), o espelho diz pouco sobre partidarismo. Ele serve de outra')
    w('  forma: um desvio de votos de Flávio para Lula quase não mexe no coeficiente próprio de Lula (item 5), então a perda do')
    w('  núcleo do PT é uma referência, dentro de 2026, de quanto o núcleo de um partido perde sem desvio contra o seu candidato.')
    w('')
    w('4. Partido ou força local de Lula? (fora do critério, escolhido antes de ver P1 a P5)')
    w('- P de Flávio por quintil do PL (mesmos cortes), dentro de faixas da fatia de Lula nos válidos de presidente do 1º turno da seção:')
    for b, v in fx.items():
        s_ = ' | '.join(f'Q{x["quintil"]} {br(x["P"], 3, True)} ({br(x["ep"], 3)})' if x['P'] is not None else f'Q{x["quintil"]} n/d' for x in v['P_por_quintil_PL'])
        w(f'   Lula {b.replace("-", " a ")}% ({bi(v["secoes"])} seções): {s_}')
    w('- Faixa inteira (todos os quintis juntos), P do candidato pela fatia do adversário na seção:')
    for k, v in ag.items():
        nm, b = k.split('_adversario_')
        w(f'   {nm.replace("Flavio", "Flávio")}, adversário com {b.replace("-", " a ")}%: {br(v["P"], 4, True)} (ep {br(v["ep"], 4)}), {bi(v["n_informativas"])} seções na regressão')
    if t35:
        w(f'  O T35 (faixas pela fatia do adversário no local) deu, na faixa de menos de 35%: Flávio {br(t35["R"][0], 4, True)}, Lula {br(t35["L"][0], 4, True)}.')
    w('- P5 - P1 dentro de cada faixa (pontos): ' + '; '.join(f'Lula {b.replace("-", " a ")}% {br(100 * x, 1, True)}' for b, x in dif_faixa.items()) + '.')
    w(f'- Leitura: com a força de Lula parecida, o degrau do PL encolhe (de {br(100 * dmin, 1, True)} a {br(100 * dmax, 1, True)} pontos, contra {br(100 * (P5 - P1), 1, True)}). A maior')
    w(f'  parte da diferença entre Q1 e Q5 vem de o PL ser fraco justamente onde Lula é forte (Lula com {br(d1["adversario_pct_validos_pres_1T"], 0)}% no Q1 e')
    w(f'  {br(d5["adversario_pct_validos_pres_1T"], 0)}% no Q5). O comportamento explica isso (o eleitor se aproxima da maioria do lugar, como no T35). Um')
    w('  desvio regulado pela força local de Lula também explicaria. Este teste não separa as duas coisas. Algumas células têm poucas')
    w('  seções e erro-padrão grande (Q1 da faixa de menos de 35%; Q3 a Q5 da faixa de 65% ou mais).')
    pf = rob['Flavio_por_quintil_da_propria_fatia_1T']['q']; plq = rob['Lula_por_quintil_da_propria_fatia_1T']['q']
    w(f'- Pela fatia do próprio candidato no 1º turno (quintis): Flávio {" ; ".join(br(x["P"], 3, True) for x in pf)}; Lula {" ; ".join(br(x["P"], 3, True) for x in plq)}.')
    w('  Onde é mais fraco, Flávio perde bem mais que Lula onde Lula é mais fraco; onde cada um é mais forte, perdem parecido.')
    w('')
    w('5. Calibração: o que um desvio faria com P1 a P5 (fora do critério)')
    w(f'- Desvio simulado por cima dos dados: uma parte dos votos de Flávio no 2º turno passa para Lula em cada seção. Universo:')
    w(f'  Flávio {bi(cal["R2_universo"])}, Lula {bi(cal["L2_universo"])}, margem {bi(cal["margem_universo"])}; o desvio que vira o resultado é de {pc(sv, 2)}% dos votos de')
    w(f'  Flávio ({bi(cuv["votos_desviados"])} votos).')
    for nome, cc in cen.items():
        rot = ('uniforme de 1%' if nome == 'uniforme_1pct' else
               f'uniforme de {pc(sv, 2)}% (o que vira o resultado)' if nome.startswith('uniforme_que_vira') else
               'concentrado onde Lula é forte (proporcional à fatia de Lula entre os finalistas no 1º turno da seção), mesmo total')
        w(f'  {rot} ({bi(cc["votos_desviados"])} votos): P {" ; ".join(br(x["P"], 3, True) for x in cc["Flavio_PL"])}')
        w(f'     deslocamento {" ; ".join(br(x["deslocamento"], 4, True) for x in cc["Flavio_PL"])}; veredito pela letra: {cc["Flavio_PL_veredito"]["veredito_z_de_zero"]}.')
        w(f'     Lula (PT): deslocamento {" ; ".join(br(x["deslocamento"], 4, True) for x in cc["Lula_PT"])}.')
    w(f'- Um desvio uniforme desloca os cinco P quase igual (cerca de {br(dsl, 2)} por unidade de fração desviada) e mantém o degrau. A')
    w('  régua de INCOERÊNCIA pede um perfil plano (|P1| - |P5| até 0,01). Ela só acende se o desvio for quase toda a perda e o')
    w('  comportamento quase nada. Contra "comportamento mais desvio uniforme", o teste tem pouco poder. Contra desvio concentrado')
    w('  onde Lula é forte, nenhum.')
    w(f'- Limite com premissa: se o núcleo do PL de verdade não perde eleitor líquido (P5 sem desvio >= 0), o desvio uniforme cabe até')
    w(f'  {pc(smax["ponto"])}% ({pc(smax["com_2_ep"])}% no limite de 2 ep). Com a perda do núcleo do PT como natural ({pc(-PT5)}%), até cerca de {pc(s_ref_pt)}%')
    w(f'  ({pc(s_ref_pt2)}% no limite de 2 ep). As duas premissas não se provam com estes dados.')
    w('')
    w('6. Robustez (fora do critério; não muda o veredito)')
    w(f'- T8 sem os grupos dos eliminados (outros somados): PL {" ; ".join(br(x["P"], 4, True) for x in rob["sem_grupos_PL"])}; PT {" ; ".join(br(x["P"], 4, True) for x in rob["sem_grupos_PT"])}.')
    for k in ('topo_10pct_PL', 'topo_5pct_PL', 'base_10pct_PL', 'base_5pct_PL', 'topo_10pct_PT', 'topo_5pct_PT', 'base_10pct_PT', 'base_5pct_PT'):
        v = rob[k]; d = v['descritivo']; lado = 'acima de' if k.startswith('topo') else 'até'
        w(f'- {k.split("_")[0]} {k.split("_")[1].replace("pct", "%")} da fatia do {k.split("_")[2]} ({lado} {pc(v["corte"])}%): P {br(v["P"], 4, True)} (ep {br(v["ep"], 4)}), {bi(v["n_informativas"])} seções na')
        w(f'  regressão; próprio/adversário no 1º turno {br(d["proprio_pct_validos_pres_1T"], 0)}% / {br(d["adversario_pct_validos_pres_1T"], 0)}%.')
    w(f'- Fatia da federação do PT (13, 65 e 43) para Lula: {" ; ".join(br(x["P"], 4, True) for x in rob["federacao_PT"])}.')
    w('- O topo de 5% do PL (onde o PL tem metade ou mais dos votos para deputado) não perde menos que o Q5. Uma explicação possível,')
    w('  não testada aqui, é o voto pessoal num candidato do PL da cidade, que eleva a fatia sem ser voto partidário.')
    w('')
    w('7. Desvios e leituras declaradas')
    w('- "A mais de 3 erros-padrão": lido de zero (principal, mais literal); pelo limiar, o mesmo veredito.')
    w('- A regressão é a do T8 registrado para 2026: grupos Cury, Renan, Caiado, Zema e demais, queda do branco+nulo, variação do')
    w('  comparecimento, votos do adversário e votos do próprio no 1º turno. O texto do Adendo 18 cita os grupos, o branco+nulo e o')
    w('  comparecimento; adversário e próprio estão no T8 e o próprio é a medida, então entram.')
    w(f'- Quintis sem peso, cortes nos percentis 20, 40, 60 e 80 das seções do universo (PL: {", ".join(pc(x) + "%" for x in cPL)}; PT:')
    w(f'  {", ".join(pc(x) + "%" for x in cPT)}). Regressão separada em cada quintil, com efeito fixo de local: o local que cai em dois quintis')
    w(f'  fica dividido, e a seção que fica sozinha no seu quintil sai ({bi(cj["linhas"])} das {bi(res["universo_secoes"])} seções entram nas cinco regressões do PL).')
    w('- Válidos = nominal + legenda como o bweb traz; voto em candidato com registro anulado depois continua como nominal no arquivo.')
    w('- O exterior fica de fora (não vota para deputado). Por isso o P do universo inteiro difere um pouco do T8 registrado.')
    w('- O espelho de Lula usa a mesma régua; o registro escreve o critério para o núcleo do PL, e é esse o veredito do teste.')
    w('- PT só com o número 13, como registrado; a federação entra só como robustez.')
    w('')
    w('8. O que ficou de fora e limites')
    w('- Inferência ecológica: o coeficiente diz quanto o ganho de Flávio cai a cada eleitor dele no 1º turno na seção, com os outros')
    w('  grupos e a variação do comparecimento fixos. Mistura quem mudou de voto com a troca de eleitores entre os turnos (quem votou')
    w('  no 1º e faltou no 2º, substituído por quem faltou no 1º e votou no 2º), e não é comportamento individual.')
    w('- A fatia do PL para deputado mede partidarismo e também voto pessoal em candidato local. O núcleo do PL não é só gente do PL:')
    w(f'  no Q5, Lula ainda teve {br(d5["adversario_pct_validos_pres_1T"], 0)}% no 1º turno.')
    w('- O teste não separa comportamento de um desvio regulado pela força local de Lula, ou por qualquer outra coisa que a urna saiba')
    w('  da própria seção. Isso só se testa fora da contagem da urna: teste de integridade, boletim impresso contra o transmitido,')
    w('  inspeção do código. O L3 não faz nada disso.')
    w('- Nenhuma eleição anterior foi usada. Sem elas, não há régua externa para o tamanho "normal" da perda; as referências usadas')
    w('  (núcleo do PT, redutos de cada candidato) são de 2026, e o texto diz em cada caso qual premissa está por trás.')
    with open(caminho, 'w') as f:
        f.write('\n'.join(L) + '\n')


if __name__ == '__main__':
    if len(sys.argv) > 1 and sys.argv[1] == '--texto':
        with open(sys.argv[2]) as f:
            escrever_txt(json.load(f), sys.argv[3])
    else:
        main()
