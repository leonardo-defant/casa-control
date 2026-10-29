"""T21 do pré-registro (Adendo 9), partes (a) e (b), com o bweb completo dos dois turnos de 2026.

Campo usado: QT_ELEI_BIOM_SEM_HABILITACAO do bweb ("Quantidade de eleitoras e eleitores com biometria, mas que não
foram habilitados por meio dela", leiame do TSE). Aqui: NH = liberações sem biometria de quem tem biometria cadastrada.
O bweb não separa, dentro de comparecimento - NH, quem foi habilitado pela digital de quem não tem biometria
cadastrada; por isso a variação "com biometria" é a variação de (comparecimento - NH).

(a) Totais nacionais (27 UFs, exterior e soma) de NH e do comparecimento nos dois turnos de 2026; variação de NH
    contra a variação do comparecimento; NH esperado no 2º turno se NH acompanhasse o comparecimento na proporção do
    1º turno. Por UF, o mesmo. Descritivo dentro do local: variação de NH na variação do comparecimento (em votos,
    efeito fixo de local, como o T9). Referência de 2022: o campo equivalente (QT_ELEITORES_BIOMETRIA_NH) exige o bweb
    de 2022, que não está nos arquivos locais; a base secoes2022.json.gz não tem o campo. O script grava, para cada
    leitura possível de "esperado pela proporção de 2022", o valor de 2022 que levaria o excesso a 400 mil.
(b) Por seção (todas as seções com os dois turnos e comparecimento do 1º turno acima de zero):
    y = (L2 - L1) / C1; x_sem = (NH2 - NH1) / C1; x_com = [(C2 - NH2) - (C1 - NH1)] / C1.
    Efeito fixo de local, sem peso, erro agrupado por local (CR1, lib.fe_ols). Diferença x_sem - x_com e seu
    erro-padrão pela reparametrização y = (b_sem - b_com) x_sem + b_com (x_sem + x_com).
    Robustez, fixada aqui antes de rodar e relatada ao lado, sem substituir a principal:
      R1 em votos, sem divisão (a especificação do T9: ganho de Lula nas variações em votos);
      R2 denominador = comparecimento do 2º turno;
      R3 principal com peso C1;
      R4 principal só com seções apuradas por urna nos dois turnos e sem agregação em nenhum dos dois.

Uso: python3 -I analisar_T21.py <pasta zips bweb 1T> <pasta zips bweb 2T> <secoes2026.json.gz> <cache.json.gz>
        <saida.json> <saida.txt>
O cache guarda, por seção e turno, [loc, comp, apt, NH, tipo, agregadas] lidos dos zips (serve também ao T27).
"""
import os as _os, sys as _sys
_sys.path.insert(0, _os.path.dirname(_os.path.abspath(__file__)))
import collections, csv, glob, gzip, io, json, sys, time, zipfile, warnings
from multiprocessing import Pool
import numpy as np
from lib import carregar, chave_local, fe_ols
warnings.filterwarnings('ignore')

CAMPO = 'QT_ELEI_BIOM_SEM_HABILITACAO'
LIMIAR_EXCESSO = 400_000


def ler_zip(zpath):
    """Linhas de Presidente (cargo 1) de um zip bweb: uma entrada por seção, com checagem de consistência."""
    out = {}; incons = 0; nulos = collections.Counter()
    z = zipfile.ZipFile(zpath)
    nome = [n for n in z.namelist() if n.lower().endswith('.csv')][0]
    with z.open(nome) as fh:
        cab = next(csv.reader([fh.readline().decode('latin1')], delimiter=';'))
        ix = {c.strip().replace('SG_ UF', 'SG_UF'): i for i, c in enumerate(cab)}
        iuf, imun, izon, isec, iloc = (ix[c] for c in ('SG_UF', 'CD_MUNICIPIO', 'NR_ZONA', 'NR_SECAO', 'NR_LOCAL_VOTACAO'))
        icar, icomp, iapt, inh, itipo = (ix[c] for c in ('CD_CARGO_PERGUNTA', 'QT_COMPARECIMENTO', 'QT_APTOS', CAMPO, 'DS_TIPO_URNA'))
        iagr = ix.get('DS_SECOES_AGREGADAS')
        for linha in fh:
            if b';1;"Presidente";' not in linha:
                continue
            r = next(csv.reader([linha.decode('latin1')], delimiter=';'))
            if r[icar] != '1':
                continue
            k = f"{r[iuf]}|{int(r[imun])}|{int(r[izon])}|{int(r[isec])}"
            nh_txt = r[inh].strip()
            try:
                nh = int(nh_txt)
                if nh < 0:
                    nulos[nh_txt] += 1; nh = None
            except ValueError:
                nulos[nh_txt] += 1; nh = None
            agr = r[iagr] if iagr is not None else ''
            agr = '' if agr in ('', '#NULO#') else agr
            reg = [int(r[iloc]), int(r[icomp]), int(r[iapt]), nh, r[itipo], agr]
            if k in out:
                if out[k] != reg:
                    incons += 1
            else:
                out[k] = reg
    return zpath, out, incons, dict(nulos)


def extrair(pasta, pool):
    zips = sorted(glob.glob(_os.path.join(pasta, '*.zip')), key=lambda p: -_os.path.getsize(p))
    tudo = {}; incons = 0; nulos = collections.Counter()
    for zp, out, inc, nul in pool.imap_unordered(ler_zip, zips):
        print('  lido', _os.path.basename(zp), len(out), 'seções', flush=True)
        tudo.update(out); incons += inc; nulos.update(nul)
    return tudo, incons, dict(nulos), [_os.path.basename(z) for z in zips]


def resumo_reg(r, nomes):
    return {'n': r['n'], 'locais': r['grupos'], 'coef': {k: r['coef'][k] for k in nomes}, 'ep': {k: r['ep'][k] for k in nomes}}


def regressao(y, xs, xc, loc, w=None):
    """b_sem, b_com e a diferença (com erro-padrão) pela reparametrização."""
    r = fe_ols(y, np.column_stack([xs, xc]), loc, w, ['sem_biometria', 'com_biometria'])
    r2 = fe_ols(y, np.column_stack([xs, xs + xc]), loc, w, ['diferenca_sem_menos_com', 'comparecimento'])
    out = resumo_reg(r, ['sem_biometria', 'com_biometria'])
    out['diferenca_sem_menos_com'] = {'coef': r2['coef']['diferenca_sem_menos_com'], 'ep': r2['ep']['diferenca_sem_menos_com']}
    d = out['diferenca_sem_menos_com']
    d['z'] = d['coef'] / d['ep'] if d['ep'] > 0 else float('nan')
    return out


def main():
    p1, p2, base, cache, saida_json, saida_txt = sys.argv[1:7]
    t0 = time.time()
    if _os.path.exists(cache):
        c = carregar(cache); s1, s2, meta = c['1'], c['2'], c['meta']
        print('cache lido', cache, flush=True)
    else:
        with Pool(3) as pool:
            print('lendo 1º turno', flush=True)
            s1, inc1, nul1, z1 = extrair(p1, pool)
            print('lendo 2º turno', flush=True)
            s2, inc2, nul2, z2 = extrair(p2, pool)
        meta = {'zips_1t': z1, 'zips_2t': z2, 'linhas_inconsistentes_1t': inc1, 'linhas_inconsistentes_2t': inc2,
                'valores_invalidos_do_campo_1t': nul1, 'valores_invalidos_do_campo_2t': nul2}
        with gzip.open(cache, 'wt') as f:
            json.dump({'meta': meta, '1': s1, '2': s2}, f, separators=(',', ':'))
    print(f'extração: {time.time() - t0:.0f}s; seções 1T {len(s1)}, 2T {len(s2)}', flush=True)

    # base conferida (votos de Lula); confere comparecimento seção a seção
    d = carregar(base)
    difcomp = collections.Counter(); faltam = collections.Counter()
    for k, v in d.items():
        for t, s in (('1', s1), ('2', s2)):
            if t not in v:
                continue
            if k not in s:
                faltam[t] += 1
            elif s[k][1] != v[t]['comp']:
                difcomp[t] += 1
    for t, s in (('1', s1), ('2', s2)):
        faltam['no_bweb_e_nao_na_base_' + t] = sum(1 for k in s if k not in d or t not in d[k])
    conferencia = {'secoes_base': len(d), 'comparecimento_diferente_da_base': dict(difcomp),
                   'secoes_faltando': dict(faltam)}
    print('conferência com a base:', conferencia, flush=True)

    # ---------- (a) totais ----------
    def soma(s, filtro):
        C = NH = n = nnul = 0
        for k, r in s.items():
            if not filtro(k):
                continue
            n += 1; C += r[1]
            if r[3] is None:
                nnul += 1
            else:
                NH += r[3]
        return {'secoes': n, 'comparecimento': C, 'NH': NH, 'secoes_sem_valor_do_campo': nnul,
                'pct_NH_do_comparecimento': 100 * NH / C if C else float('nan')}

    escopos = {'Brasil (27 UFs)': lambda k: not k.startswith('ZZ|'), 'Exterior': lambda k: k.startswith('ZZ|'),
               'Total': lambda k: True}
    ufs = sorted({k.split('|')[0] for k in s2})
    tot = {}
    for nome, f in list(escopos.items()) + [(u, (lambda u: lambda k: k.startswith(u + '|'))(u)) for u in ufs]:
        a, b = soma(s1, f), soma(s2, f)
        dC, dNH = b['comparecimento'] - a['comparecimento'], b['NH'] - a['NH']
        prop = a['NH'] / a['comparecimento'] if a['comparecimento'] else float('nan')
        esp = prop * b['comparecimento']
        tot[nome] = {'turno1': a, 'turno2': b, 'var_comparecimento': dC, 'var_NH': dNH,
                     'var_NH_sobre_var_comparecimento': dNH / dC if dC else None,
                     'var_NH_sobre_comparecimento_1t_pct': 100 * dNH / a['comparecimento'] if a['comparecimento'] else None,
                     'var_pct_NH_pontos': b['pct_NH_do_comparecimento'] - a['pct_NH_do_comparecimento'],
                     'NH_2t_esperado_na_proporcao_do_1t': esp, 'excesso_sobre_proporcao_do_1t': b['NH'] - esp,
                     'variacao_relativa_NH_pct': 100 * dNH / a['NH'] if a['NH'] else None,
                     'variacao_relativa_comparecimento_pct': 100 * dC / a['comparecimento'] if a['comparecimento'] else None}

    # limiar de 2022 para o excesso de 400 mil, em cada leitura de "esperado pela proporção de 2022"
    B = tot['Brasil (27 UFs)']; Tt = tot['Total']
    lim = {}
    for nome, T in (('Brasil (27 UFs)', B), ('Total', Tt)):
        NH1, NH2 = T['turno1']['NH'], T['turno2']['NH']; C1, C2 = T['turno1']['comparecimento'], T['turno2']['comparecimento']
        dNH, dC = NH2 - NH1, C2 - C1
        lim[nome] = {
            'leitura_1_esperado_igual_var_comparecimento_2026_vezes_razao_dNH_dC_de_2022':
                {'excesso_400mil_se_razao_2022_abaixo_de': (dNH - LIMIAR_EXCESSO) / dC if dC else None},
            'leitura_2_esperado_igual_NH1_2026_vezes_razao_NH2_NH1_de_2022':
                {'excesso_400mil_se_razao_2022_abaixo_de': (NH2 - LIMIAR_EXCESSO) / NH1 if NH1 else None},
            'leitura_3_esperado_igual_C2_2026_vezes_fatia_NH_2t_de_2022':
                {'excesso_400mil_se_fatia_NH_2t_2022_pct_abaixo_de': 100 * (NH2 - LIMIAR_EXCESSO) / C2},
            'leitura_4_esperado_igual_NH1_2026_mais_var_comparecimento_2026_vezes_fatia_NH_1t_de_2022':
                {'excesso_400mil_se_fatia_NH_1t_2022_pct_abaixo_de': 100 * (dNH - LIMIAR_EXCESSO) / dC if dC else None},
            # com razão ou fatia de 2022 não negativas e dC > 0, o excesso máximo das leituras 1 e 4 é dNH
            # (2022 com razão zero) e o das leituras 2 e 3 é NH2
            'excesso_maximo_leituras_1_e_4_com_2022_nao_negativo': dNH if dC > 0 else None,
            'excesso_maximo_leituras_2_e_3_com_2022_nao_negativo': NH2}

    # ---------- (b) regressão por seção ----------
    linhas = []
    excl = collections.Counter()
    for k, v in d.items():
        if '1' not in v or '2' not in v:
            excl['sem_os_dois_turnos'] += 1; continue
        if k not in s1 or k not in s2:
            excl['fora_do_bweb'] += 1; continue
        a, b = s1[k], s2[k]
        if a[3] is None or b[3] is None:
            excl['campo_sem_valor'] += 1; continue
        C1, C2, NH1, NH2 = v['1']['comp'], v['2']['comp'], a[3], b[3]
        if C1 <= 0:
            excl['comparecimento_1t_zero'] += 1; continue
        limpa = (a[4] == 'Apurada' and b[4] == 'Apurada' and not a[5] and not b[5])
        linhas.append((chave_local(k, v['2']), C1, C2, NH1, NH2, v['1']['L'], v['2']['L'], limpa))
    loc = np.array([r[0] for r in linhas])
    A = np.array([r[1:] for r in linhas], float)
    C1, C2, NH1, NH2, L1, L2, limpa = A.T
    limpa = limpa.astype(bool)
    dL, dNH = L2 - L1, NH2 - NH1
    dB = (C2 - NH2) - (C1 - NH1)
    dC = C2 - C1
    print(f'seções na regressão: {len(linhas)}; fora: {dict(excl)}', flush=True)

    reg = {}
    reg['principal'] = regressao(dL / C1, dNH / C1, dB / C1, loc)
    reg['R1_em_votos'] = regressao(dL, dNH, dB, loc)
    ok2 = C2 > 0
    reg['R2_denominador_comparecimento_2t'] = regressao((dL / np.where(ok2, C2, 1))[ok2], (dNH / np.where(ok2, C2, 1))[ok2],
                                                        (dB / np.where(ok2, C2, 1))[ok2], loc[ok2])
    reg['R3_peso_comparecimento_1t'] = regressao(dL / C1, dNH / C1, dB / C1, loc, C1)
    reg['R4_so_apuradas_sem_agregacao'] = regressao((dL / C1)[limpa], (dNH / C1)[limpa], (dB / C1)[limpa], loc[limpa])
    # descritivo do (a) dentro do local: fração dos eleitores a mais liberados sem biometria (em votos, como o T9)
    r = fe_ols(dNH, dC[:, None], loc, None, ['var_comparecimento'])
    dentro = {'coef': r['coef']['var_comparecimento'], 'ep': r['ep']['var_comparecimento'], 'n': r['n'], 'locais': r['grupos'],
              'fatia_NH_1t_nas_mesmas_secoes': float(NH1.sum() / C1.sum())}
    rr = fe_ols(dNH / C1, (dC / C1)[:, None], loc, None, ['var_comparecimento_sobre_C1'])
    dentro['em_taxa'] = {'coef': rr['coef']['var_comparecimento_sobre_C1'], 'ep': rr['ep']['var_comparecimento_sobre_C1']}
    descr = {'secoes': int(len(linhas)), 'secoes_limpas_R4': int(limpa.sum()),
             'media_x_sem_pct': float(100 * np.mean(dNH / C1)), 'media_x_com_pct': float(100 * np.mean(dB / C1)),
             'media_y_pct': float(100 * np.mean(dL / C1)),
             'soma_dNH': float(dNH.sum()), 'soma_dB': float(dB.sum()), 'soma_dL': float(dL.sum()), 'soma_dC': float(dC.sum()),
             'pct_secoes_dNH_positivo': float(100 * np.mean(dNH > 0)), 'pct_secoes_dNH_negativo': float(100 * np.mean(dNH < 0)),
             'percentis_x_sem_pct': {p: float(100 * np.percentile(dNH / C1, p)) for p in (1, 5, 25, 50, 75, 95, 99)}}

    # ---------- critério ----------
    P = reg['principal']
    bs, bc = P['coef']['sem_biometria'], P['coef']['com_biometria']
    dif, epd = P['diferenca_sem_menos_com']['coef'], P['diferenca_sem_menos_com']['ep']
    cond_coef_sinal = bs > 0.9 and dif > 3 * epd
    cond_coef_sem = abs(bs - bc) <= 0.15
    # proporcionalidade dentro de 2026: NH dos eleitores a mais contra a fatia de base
    z_prop = (dentro['coef'] - dentro['fatia_NH_1t_nas_mesmas_secoes']) / dentro['ep']
    crit = {'coef_sem_acima_de_0.9': bs > 0.9, 'diferenca_acima_de_3_ep': dif > 3 * epd,
            'parte_coeficientes_do_sinal': cond_coef_sinal, 'parte_coeficientes_do_sem_sinal': cond_coef_sem,
            'parte_2022_do_sinal': 'sem dado nesta rodada (bweb de 2022 não está nos arquivos locais)',
            'parte_2022_do_sem_sinal': 'sem dado nesta rodada (bweb de 2022 não está nos arquivos locais)',
            'proporcionalidade_2026_dentro_do_local': {'NH_por_eleitor_a_mais': dentro['coef'], 'ep': dentro['ep'],
                                                       'fatia_de_base': dentro['fatia_NH_1t_nas_mesmas_secoes'],
                                                       'razao': dentro['coef'] / dentro['fatia_NH_1t_nas_mesmas_secoes'],
                                                       'z_da_diferenca': z_prop},
            'proporcionalidade_2026_nacional': {'var_NH_sobre_var_comparecimento': B['var_NH_sobre_var_comparecimento'],
                                                'fatia_NH_1t': B['turno1']['NH'] / B['turno1']['comparecimento'],
                                                'excesso_sobre_proporcao_do_1t': B['excesso_sobre_proporcao_do_1t']}}
    # veredito pela letra: o sinal é uma conjunção; basta uma parte falhar para não haver sinal.
    # O sem sinal pede também "liberações proporcionais ao aumento do comparecimento, como em 2022", que exige 2022.
    if cond_coef_sinal:
        veredito = 'INCONCLUSIVO'
        motivo = 'parte dos coeficientes do sinal atendida; a parte de 2022 (400 mil acima do esperado) não pode ser medida nesta rodada'
    elif cond_coef_sem:
        veredito = 'INCONCLUSIVO'
        motivo = ('sinal descartado pela parte dos coeficientes; parte dos coeficientes do sem sinal atendida; a parte '
                  '"proporcionais ao aumento do comparecimento, como em 2022" não pode ser certificada sem a referência de 2022')
    else:
        veredito = 'INCONCLUSIVO'
        motivo = 'sinal descartado pela parte dos coeficientes; coeficientes a mais de 0,15 um do outro'
    crit['veredito'] = veredito; crit['motivo'] = motivo

    out = {'teste': 'T21 (a) e (b), bweb completo de 2026', 'campo': CAMPO, 'meta_extracao': meta,
           'conferencia_com_base': conferencia, 'a_totais': tot, 'a_limiares_2022_para_400mil': lim,
           'a_dentro_do_local': dentro, 'b_descritivo': descr, 'b_regressoes': reg, 'b_exclusoes': dict(excl),
           'criterio': crit}
    json.dump(out, open(saida_json, 'w'), ensure_ascii=False, indent=1)

    # ---------- texto ----------
    L = []
    w = L.append
    w('T21. Liberação sem biometria em todo o país, partes (a) e (b), com o bweb completo dos dois turnos de 2026')
    w(f'Campo: {CAMPO} (eleitores com biometria que não foram habilitados por meio dela). NH abaixo.')
    w(f'Conferência com a base por seção: {json.dumps(conferencia, ensure_ascii=False)}')
    w(f'Extração: {json.dumps({k: v for k, v in meta.items() if not k.startswith("zips")}, ensure_ascii=False)}')
    w('')
    w('(a) Totais nacionais')
    w(f'{"escopo":<16}{"NH 1T":>11}{"NH 2T":>11}{"var NH":>10}{"var comp":>11}{"%NH 1T":>8}{"%NH 2T":>8}{"var pts":>8}{"exc. prop 1T":>13}')
    for nome in ['Brasil (27 UFs)', 'Exterior', 'Total'] + ufs:
        T = tot[nome]
        w(f'{nome:<16}{T["turno1"]["NH"]:>11,}{T["turno2"]["NH"]:>11,}{T["var_NH"]:>+10,}{T["var_comparecimento"]:>+11,}'
          f'{T["turno1"]["pct_NH_do_comparecimento"]:>8.3f}{T["turno2"]["pct_NH_do_comparecimento"]:>8.3f}'
          f'{T["var_pct_NH_pontos"]:>+8.3f}{T["excesso_sobre_proporcao_do_1t"]:>+13,.0f}'.replace(',', '.'))
        if nome == 'Total':
            w('')
    w('')
    w(f'Dentro do local (em votos, como o T9): variação de NH por eleitor a mais = {dentro["coef"]:.4f} '
      f'(ep {dentro["ep"]:.4f}); fatia de NH no 1º turno nas mesmas seções = {dentro["fatia_NH_1t_nas_mesmas_secoes"]:.4f}; '
      f'{dentro["n"]} seções, {dentro["locais"]} locais. Em taxa (dividido por C1): {dentro["em_taxa"]["coef"]:.4f} '
      f'(ep {dentro["em_taxa"]["ep"]:.4f}).')
    w('Referência de 2022: sem dado nesta rodada (o bweb de 2022, com QT_ELEITORES_BIOMETRIA_NH, não está nos arquivos')
    w('locais; secoes2022.json.gz não tem o campo; a regra desta rodada proíbe baixar).')
    w('Valor de 2022 que levaria o excesso nacional (27 UFs) a mais de 400 mil, em cada leitura do registro:')
    for kk, vv in lim['Brasil (27 UFs)'].items():
        w(f'  {kk}: {vv}')
    w('')
    w('(b) Regressão do ganho de Lula nas variações sem e com biometria, efeito fixo de local, erro agrupado por local')
    w(f'Seções: {descr["secoes"]} (fora: {dict(excl)}); média de x_sem {descr["media_x_sem_pct"]:+.3f}% de C1, '
      f'x_com {descr["media_x_com_pct"]:+.3f}%, y {descr["media_y_pct"]:+.3f}%.')
    for nome, R in reg.items():
        c, e, df = R['coef'], R['ep'], R['diferenca_sem_menos_com']
        w(f'  {nome:<34} sem {c["sem_biometria"]:+.4f} ({e["sem_biometria"]:.4f})  com {c["com_biometria"]:+.4f} '
          f'({e["com_biometria"]:.4f})  dif {df["coef"]:+.4f} ({df["ep"]:.4f}, z {df["z"]:+.2f})  n {R["n"]} locais {R["locais"]}')
    w('')
    w(f'Critério (principal): coef. sem biometria > 0,9? {crit["coef_sem_acima_de_0.9"]}; diferença > 3 ep? '
      f'{crit["diferenca_acima_de_3_ep"]}; coeficientes a até 0,15 um do outro? {crit["parte_coeficientes_do_sem_sinal"]}.')
    pr, pn = crit['proporcionalidade_2026_dentro_do_local'], crit['proporcionalidade_2026_nacional']
    milhar = lambda x: f'{x:+,.0f}'.replace(',', '.')
    w(f'Proporcionalidade em 2026 (sem 2022): no país, var NH / var comparecimento = {pn["var_NH_sobre_var_comparecimento"]:.4f} '
      f'contra a fatia de NH do 1º turno {pn["fatia_NH_1t"]:.4f}; excesso sobre a proporção do 1º turno '
      f'{milhar(pn["excesso_sobre_proporcao_do_1t"])}. Dentro do local: {pr["NH_por_eleitor_a_mais"]:.4f} (ep {pr["ep"]:.4f}) '
      f'contra {pr["fatia_de_base"]:.4f}, razão {pr["razao"]:.2f}, z {pr["z_da_diferenca"]:+.1f}.')
    w(f'Veredito pela letra: {veredito}. Motivo: {motivo}.')
    w('')
    lb = lim['Brasil (27 UFs)']
    w('Leitura:')
    w(f'- Por liberação sem biometria a mais, Lula ganhou {bs:.3f} voto; por eleitor a mais habilitado de outro modo, {bc:.3f}. '
      f'A diferença é {dif:+.4f} (ep {epd:.4f}). Se as liberações a mais fossem votos inseridos para Lula, o coeficiente '
      f'ficaria perto de 1; o registro pede mais de 0,9.')
    w(f'- Liberações sem biometria no país (27 UFs): {milhar(B["var_NH"])} entre os turnos, para {milhar(B["var_comparecimento"])} '
      f'no comparecimento. Cresceram {B["variacao_relativa_NH_pct"]:.2f}% contra {B["variacao_relativa_comparecimento_pct"]:.2f}% '
      f'do comparecimento: um pouco mais que a proporção, {milhar(B["excesso_sobre_proporcao_do_1t"])} acima dela.')
    w(f'- 400 mil: nas leituras que comparam variações (1, 2 e 4), se as liberações sem biometria de 2022 não caíram entre '
      f'os turnos, o excesso de 2026 fica no máximo em {milhar(B["var_NH"])}. Passaria de 400 mil só se, em 2022, elas '
      f'tivessem caído entre os turnos: razão NH2/NH1 abaixo de '
      f'{lb["leitura_2_esperado_igual_NH1_2026_vezes_razao_NH2_NH1_de_2022"]["excesso_400mil_se_razao_2022_abaixo_de"]:.4f} '
      f'(leitura 2) ou var NH / var comparecimento abaixo de '
      f'{lb["leitura_1_esperado_igual_var_comparecimento_2026_vezes_razao_dNH_dC_de_2022"]["excesso_400mil_se_razao_2022_abaixo_de"]:.4f} '
      f'(leitura 1).')
    w('- Limites: o bweb não separa, entre os habilitados sem NH, quem usou a digital de quem não tem biometria cadastrada, '
      'então a variação "com biometria" mistura os dois. Regressão ecológica entre seções do mesmo local. O campo é '
      'escrito pelo mesmo programa que grava o voto: um programa malicioso poderia gravar NH coerente.')
    open(saida_txt, 'w').write('\n'.join(L) + '\n')
    print('\n'.join(L))
    print(f'tempo total {time.time() - t0:.0f}s')


if __name__ == '__main__':
    main()
