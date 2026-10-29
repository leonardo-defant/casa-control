"""T16 do pré-registro (Adendo 9): piso da troca uniforme, cauda inferior do coeficiente de troca por estrato.

Regressão do T8/T14 (analisar_fluxo_regressao.py): y = votos(2T) - votos(1T) do candidato que ganhou terreno;
X = votos dos outros candidatos no 1T (em 2026, separados: Cury 70, Renan 14, Caiado 55, Zema 30 e demais),
queda do branco+nulo, variação do comparecimento, votos do adversário no 1T e do próprio no 1T.
Efeito fixo de local, sem peso (a regressão é em votos), erro agrupado por local (CR1, lib.fe_ols).
Coeficiente de interesse: adversario_1T (Flávio em 2026; Bolsonaro em 2018, com Haddad; Lula em 2022, com Bolsonaro).

Estratos: cada uma das 27 UFs (sem o exterior) e, no país, capital contra interior.
Q10 = 10º percentil ponderado por seções (seções da UF com os dois turnos) dos 27 coeficientes por UF:
o menor coeficiente cuja fração acumulada do peso, em ordem crescente, chega a 10%.
Secundária: o menor coeficiente entre as UFs com 5.000 seções ou mais.
Referências 2018 e 2022 sem troca e com troca uniforme simulada: uma fração s dos votos do adversário no 2T
passa para o candidato no 2T, em todas as seções (valor esperado s vezes os votos, sem sorteio). O 1T fica intacto.
Erro-padrão do Q10: bootstrap paramétrico (cada coeficiente por UF sorteado da normal com o seu erro CR1; as UFs são
conjuntos disjuntos de locais, portanto independentes), 20.000 sorteios, semente fixa.

Uso: python3 -I analisar_T16.py <secoes2026.json.gz> <candidatos2026_1t.json.gz> <secoes2018.json.gz>
        <secoes2022.json.gz> <pasta locais_votacao 2026> <saida.json> > saida.txt
As referências são calculadas e gravadas (<saida>.referencias.json) antes de a base de 2026 ser lida.
"""
import os as _os, sys as _sys
_sys.path.insert(0, _os.path.dirname(_os.path.abspath(__file__)))
import csv, gc, glob, json, sys, time, unicodedata, warnings
import numpy as np
from lib import carregar, chave_local, fe_ols
warnings.filterwarnings('ignore')

TROCAS = [0.0, 0.01, 0.02, 0.03, 0.036]   # 1%, 2% e 3,6% registrados; 3% porque o critério de sinal cita 3%
GRUPOS_2026 = [('Cury', '70'), ('Renan', '14'), ('Caiado', '55'), ('Zema', '30')]
CAPITAIS = {'AC': 'RIO BRANCO', 'AL': 'MACEIO', 'AP': 'MACAPA', 'AM': 'MANAUS', 'BA': 'SALVADOR', 'CE': 'FORTALEZA',
            'DF': 'BRASILIA', 'ES': 'VITORIA', 'GO': 'GOIANIA', 'MA': 'SAO LUIS', 'MT': 'CUIABA', 'MS': 'CAMPO GRANDE',
            'MG': 'BELO HORIZONTE', 'PA': 'BELEM', 'PB': 'JOAO PESSOA', 'PR': 'CURITIBA', 'PE': 'RECIFE',
            'PI': 'TERESINA', 'RJ': 'RIO DE JANEIRO', 'RN': 'NATAL', 'RS': 'PORTO ALEGRE', 'RO': 'PORTO VELHO',
            'RR': 'BOA VISTA', 'SC': 'FLORIANOPOLIS', 'SP': 'SAO PAULO', 'SE': 'ARACAJU', 'TO': 'PALMAS'}
UFS = sorted(CAPITAIS)
NBOOT, SEMENTE = 20000, 20261028
PISO_SECOES = 5000


def sem_acento(s):
    return ''.join(ch for ch in unicodedata.normalize('NFD', s) if unicodedata.category(ch) != 'Mn').upper().strip()


def codigos_capitais(pasta):
    cod = {}
    for uf, nome in CAPITAIS.items():
        achados = set()
        with open(_os.path.join(pasta, f'eleitorado_local_votacao_2026_{uf}.csv'), encoding='latin1', newline='') as f:
            r = csv.reader(f, delimiter=';')
            cab = next(r); iu, ic, im = cab.index('SG_UF'), cab.index('CD_MUNICIPIO'), cab.index('NM_MUNICIPIO')
            for lin in r:
                if lin[iu] == uf and sem_acento(lin[im]) == nome:
                    achados.add(int(lin[ic]))
        if len(achados) != 1:
            raise SystemExit(f'capital de {uf} não identificada: {achados}')
        cod[uf] = achados.pop()
    return cod


def montar(caminho, c, cand=None):
    """Arrays por seção (só seções com os dois turnos), como em analisar_fluxo_regressao.py."""
    adv = 'R' if c == 'L' else 'L'
    d = carregar(caminho)
    linhas, adv2, locs, ufs, muns = [], [], [], [], []
    for k, v in d.items():
        if '1' not in v or '2' not in v: continue
        a, b = v['1'], v['2']
        x = []
        if cand is not None:
            cv = cand.get(k, {}); usados = 0
            for _, nums in GRUPOS_2026:
                q = sum(cv.get(n, 0) for n in nums.split(',')); x.append(q); usados += q
            x.append(a['O'] - usados)
        x.append(a['O'])   # versão sem grupos (comparável com as referências); última coluna dos grupos é removida abaixo
        x += [(a['B'] + a['N']) - (b['B'] + b['N']), b['comp'] - a['comp'], a[adv], a[c]]
        linhas.append([b[c] - a[c]] + x); adv2.append(b[adv]); locs.append(chave_local(k, b))
        p = k.split('|'); ufs.append(p[0]); muns.append(int(p[1]))
    del d; gc.collect()
    A = np.array(linhas, float)
    return {'y': A[:, 0], 'X': A[:, 1:], 'adv2': np.array(adv2, float), 'loc': np.array(locs),
            'uf': np.array(ufs), 'mun': np.array(muns), 'grupos': cand is not None}


def colunas(base, com_grupos):
    """Índices das colunas de X e nomes, para a versão com grupos (só 2026) ou sem grupos."""
    rabo = ['queda_branco_nulo', 'var_comparecimento', 'adversario_1T', 'proprio_1T']
    if base['grupos']:
        ng = len(GRUPOS_2026) + 1   # grupos + demais_outros; depois vem outros_1T agregado
        if com_grupos:
            idx = list(range(ng)) + list(range(ng + 1, ng + 5))
            nomes = [g for g, _ in GRUPOS_2026] + ['demais_outros'] + rabo
        else:
            idx = [ng] + list(range(ng + 1, ng + 5)); nomes = ['outros_1T'] + rabo
    else:
        idx = list(range(5)); nomes = ['outros_1T'] + rabo
    return idx, nomes


def regressao(base, mask, s, com_grupos):
    idx, nomes = colunas(base, com_grupos)
    y = base['y'][mask] + s * base['adv2'][mask]
    r = fe_ols(y, base['X'][mask][:, idx], base['loc'][mask], None, nomes)
    return {'n_informativas': r['n'], 'locais': r['grupos'], 'secoes': int(mask.sum()),
            'coef': r['coef']['adversario_1T'], 'ep': r['ep']['adversario_1T'],
            'proprio_1T': r['coef']['proprio_1T'], 'ep_proprio_1T': r['ep']['proprio_1T']}


def q_ponderado(b, w, q=0.10):
    o = np.argsort(b, kind='stable'); bs, ws = np.asarray(b)[o], np.asarray(w)[o]
    F = np.cumsum(ws) / ws.sum()
    return float(bs[np.searchsorted(F, q - 1e-12)])


def q_interpolado(b, w, q=0.10):
    """Robustez: pontos médios das massas acumuladas, interpolação linear."""
    o = np.argsort(b, kind='stable'); bs, ws = np.asarray(b)[o], np.asarray(w)[o]
    P = (np.cumsum(ws) - ws / 2) / ws.sum()
    return float(np.interp(q, P, bs))


def resumo_ufs(por_uf, rng):
    b = np.array([por_uf[u]['coef'] for u in UFS]); se = np.array([por_uf[u]['ep'] for u in UFS])
    w = np.array([por_uf[u]['secoes'] for u in UFS], float)
    q10 = q_ponderado(b, w)
    grandes = [i for i, u in enumerate(UFS) if por_uf[u]['secoes'] >= PISO_SECOES]
    imin = min(grandes, key=lambda i: b[i])
    Z = rng.standard_normal((NBOOT, len(b))); B = b + Z * se
    o = np.argsort(B, axis=1); Bs = np.take_along_axis(B, o, 1); Ws = w[o]
    F = np.cumsum(Ws, 1) / w.sum(); j = (F < 0.10 - 1e-12).sum(1)
    q10b = Bs[np.arange(NBOOT), j]
    minb = B[:, grandes].min(1)
    # UF que ocupa o Q10 e a fração do peso abaixo dela
    ordem = np.argsort(b, kind='stable'); Fp = np.cumsum(w[ordem]) / w.sum()
    jq = int(np.searchsorted(Fp, 0.10 - 1e-12))
    return {'Q10': q10, 'ep_Q10': float(q10b.std(ddof=1)),
            'Q10_ic95_bootstrap': [float(np.percentile(q10b, 2.5)), float(np.percentile(q10b, 97.5))],
            'UF_no_Q10': UFS[ordem[jq]], 'peso_acumulado_ate_a_UF_do_Q10': float(Fp[jq]),
            'UFs_abaixo_do_Q10': [UFS[i] for i in ordem[:jq]],
            'Q10_interpolado_robustez': q_interpolado(b, w),
            'min_UFs_5000': float(b[imin]), 'ep_min_UFs_5000': float(se[imin]), 'UF_do_min': UFS[imin],
            'ep_min_bootstrap': float(minb.std(ddof=1)), 'n_UFs_5000': len(grandes),
            'media_ponderada_UFs': float((b * w).sum() / w.sum())}


def rodar(base, rotulo, cap, com_grupos, trocas):
    out = {}
    rng = np.random.default_rng(SEMENTE)
    capital = np.array([cap.get(u) == m for u, m in zip(base['uf'], base['mun'])])
    no_pais = base['uf'] != 'ZZ'
    for s in trocas:
        t0 = time.time()
        por_uf = {u: regressao(base, base['uf'] == u, s, com_grupos) for u in UFS}
        r = {'por_UF': por_uf, **resumo_ufs(por_uf, rng)}
        r['pais'] = regressao(base, no_pais, s, com_grupos)
        # conferência com o T8/T14 (que inclui o exterior): resultados/T8_*.txt e T14_calibracao.txt
        r['pais_com_exterior_conferencia'] = regressao(base, np.ones(len(base['y']), bool), s, com_grupos)
        r['capitais'] = regressao(base, no_pais & capital, s, com_grupos)
        r['interior'] = regressao(base, no_pais & ~capital, s, com_grupos)
        r['capital_menos_interior'] = r['capitais']['coef'] - r['interior']['coef']
        r['ep_capital_menos_interior'] = float(np.hypot(r['capitais']['ep'], r['interior']['ep']))
        out[f'{s:.3f}'] = r
        print(f'# {rotulo} troca {100*s:.1f}%: Q10 {r["Q10"]:+.4f} (ep {r["ep_Q10"]:.4f}, {r["UF_no_Q10"]}); '
              f'min UFs 5000+ {r["min_UFs_5000"]:+.4f} ({r["UF_do_min"]}); país {r["pais"]["coef"]:+.4f}; '
              f'{time.time()-t0:.0f}s', file=sys.stderr, flush=True)
    return out


def f4(x): return f'{x:+.4f}'


def main():
    a26, cand26, a18, a22, pasta_locais, saida = sys.argv[1:7]
    saida_ref = sys.argv[7] if len(sys.argv) > 7 else saida + '.referencias.json'
    cap = codigos_capitais(pasta_locais)
    res = {'teste': 'T16', 'registro': 'PRE-REGISTRO-2026-10-26.md, Adendo 9', 'capitais_codigo_TSE': cap,
           'trocas_simuladas': TROCAS, 'bootstrap': {'sorteios': NBOOT, 'semente': SEMENTE}, 'referencias': {}}
    # 1) referências, gravadas antes de ler 2026
    for ano, arq, c, nome in (('2018', a18, 'L', 'Haddad'), ('2022', a22, 'R', 'Bolsonaro')):
        base = montar(arq, c)
        res['referencias'][ano] = {'candidato': nome, 'campo': c, 'resultados': rodar(base, f'{ano} {nome}', cap, False, TROCAS)}
        del base; gc.collect()
    json.dump(res, open(saida_ref, 'w'), ensure_ascii=False, indent=1)
    res['referencias_gravadas_utc'] = time.strftime('%Y-%m-%d %H:%M:%S', time.gmtime())
    print(f'# referências gravadas em {saida_ref} às {time.strftime("%H:%M:%S", time.gmtime())} UTC', file=sys.stderr, flush=True)
    # 2) 2026, Lula como candidato, Flávio como adversário
    cand = carregar(cand26)['secoes']
    base = montar(a26, 'L', cand); del cand; gc.collect()
    res['2026'] = {'candidato': 'Lula', 'campo': 'L',
                   'com_grupos_principal': rodar(base, '2026 com grupos', cap, True, [0.0])['0.000'],
                   'sem_grupos_comparavel': rodar(base, '2026 sem grupos', cap, False, [0.0])['0.000']}
    del base; gc.collect()

    # 3) critério
    R = res['referencias']
    q2 = {a: R[a]['resultados']['0.020']['Q10'] for a in R}
    q3 = {a: R[a]['resultados']['0.030']['Q10'] for a in R}
    q36 = {a: R[a]['resultados']['0.036']['Q10'] for a in R}
    lim_sem = min(q2.values()); lim_sinal = max(q3.values()); lim_sinal36 = max(q36.values())
    ref_sem_ano = min(q2, key=q2.get); ref_sinal_ano = max(q3, key=q3.get)
    crit = {}
    for versao in ('com_grupos_principal', 'sem_grupos_comparavel'):
        r = res['2026'][versao]; q, se = r['Q10'], r['ep_Q10']
        se_ref_sem = R[ref_sem_ano]['resultados']['0.020']['ep_Q10']
        se_ref_sin = R[ref_sinal_ano]['resultados']['0.030']['ep_Q10']
        z_sem = (lim_sem - q) / se; z_sinal = (q - lim_sinal) / se
        if z_sem > 2: v = 'SEM SINAL'
        elif z_sinal > 2: v = 'SINAL'
        else: v = 'INCONCLUSIVO'
        crit[versao] = {'Q10_2026': q, 'ep': se, 'limite_sem_sinal_min_Q10_2pct': lim_sem, 'ano_do_limite_sem_sinal': ref_sem_ano,
                        'z_abaixo_do_limite_sem_sinal': z_sem, 'limite_sinal_max_Q10_3pct': lim_sinal,
                        'ano_do_limite_sinal': ref_sinal_ano, 'z_acima_do_limite_sinal': z_sinal,
                        'limite_sinal_com_3_6pct_robustez': lim_sinal36, 'z_acima_3_6pct': (q - lim_sinal36) / se,
                        'z_sem_sinal_somando_ep_da_referencia_robustez': (lim_sem - q) / float(np.hypot(se, se_ref_sem)),
                        'z_sinal_somando_ep_da_referencia_robustez': (q - lim_sinal) / float(np.hypot(se, se_ref_sin)),
                        'veredito_pela_letra': v}
    res['criterio'] = crit
    res['veredito'] = crit['com_grupos_principal']['veredito_pela_letra']
    # leituras descritivas, fora do critério registrado
    desc = {}
    for versao in ('com_grupos_principal', 'sem_grupos_comparavel'):
        r = res['2026'][versao]; dv = {'troca_equivalente_pct': {}, 'secundaria': {}}
        for ano in R:
            rr = R[ano]['resultados']; inc = (rr['0.036']['Q10'] - rr['0.000']['Q10']) / 3.6   # por ponto percentual
            dv['troca_equivalente_pct'][ano] = {'s': (r['Q10'] - rr['0.000']['Q10']) / inc, 'ep': r['ep_Q10'] / inc,
                                                'inclinacao_Q10_por_ponto_de_troca': inc}
        m2 = {a: R[a]['resultados']['0.020']['min_UFs_5000'] for a in R}
        m3 = {a: R[a]['resultados']['0.030']['min_UFs_5000'] for a in R}
        se = r['ep_min_bootstrap']
        dv['secundaria'] = {'min_2026': r['min_UFs_5000'], 'UF': r['UF_do_min'], 'ep_bootstrap': se,
                            'refs_min_sem_troca': {a: R[a]['resultados']['0.000']['min_UFs_5000'] for a in R},
                            'refs_min_2pct': m2, 'refs_min_3pct': m3,
                            'z_abaixo_do_menor_min_2pct': (min(m2.values()) - r['min_UFs_5000']) / se,
                            'z_acima_do_maior_min_3pct': (r['min_UFs_5000'] - max(m3.values())) / se}
        desc[versao] = dv
    res['descritivo_fora_do_criterio'] = desc
    json.dump(res, open(saida, 'w'), ensure_ascii=False, indent=1)

    # 4) texto
    P = print
    P('T16. Piso da troca uniforme: Q10 do coeficiente de troca por UF (bweb completo do 2º turno de 2026)')
    P('Coeficiente: votos do adversário no 1º turno na regressão do ganho do candidato (T8/T14), efeito fixo de local,')
    P('erro agrupado por local. 2026: Lula, com os eliminados separados (Cury, Renan, Caiado, Zema, demais).')
    P('Referências: 2018 Haddad e 2022 Bolsonaro, outros do 1º turno agregados (as bases não têm voto por candidato).')
    P('Q10 = 10º percentil ponderado pelas seções da UF; ep por bootstrap paramétrico (20.000 sorteios).')
    P()
    P('Referências (Q10 | ep | UF no Q10 | menor coef. entre UFs com 5.000+ seções | país | capitais | interior):')
    for ano in R:
        for s, r in R[ano]['resultados'].items():
            P(f'  {ano} {R[ano]["candidato"]:9s} troca {100*float(s):4.1f}%: Q10 {f4(r["Q10"])} | {r["ep_Q10"]:.4f} | {r["UF_no_Q10"]} | '
              f'{f4(r["min_UFs_5000"])} ({r["UF_do_min"]}, ep {r["ep_min_UFs_5000"]:.4f}) | {f4(r["pais"]["coef"])} | '
              f'{f4(r["capitais"]["coef"])} ({r["capitais"]["ep"]:.4f}) | {f4(r["interior"]["coef"])} ({r["interior"]["ep"]:.4f})')
    P()
    for versao, rot in (('com_grupos_principal', '2026 Lula, eliminados separados (principal)'),
                        ('sem_grupos_comparavel', '2026 Lula, outros agregados (como as referências)')):
        r = res['2026'][versao]
        P(f'{rot}:')
        P(f'  Q10 {f4(r["Q10"])} (ep {r["ep_Q10"]:.4f}; IC95 bootstrap {f4(r["Q10_ic95_bootstrap"][0])} a {f4(r["Q10_ic95_bootstrap"][1])}); '
          f'UF no Q10: {r["UF_no_Q10"]}; UFs abaixo: {", ".join(r["UFs_abaixo_do_Q10"]) or "nenhuma"}')
        P(f'  Q10 interpolado (robustez): {f4(r["Q10_interpolado_robustez"])}; média ponderada das UFs: {f4(r["media_ponderada_UFs"])}')
        P(f'  Menor coeficiente entre as {r["n_UFs_5000"]} UFs com 5.000+ seções: {f4(r["min_UFs_5000"])} ({r["UF_do_min"]}, ep {r["ep_min_UFs_5000"]:.4f})')
        P(f'  País: {f4(r["pais"]["coef"])} ({r["pais"]["ep"]:.4f}); capitais {f4(r["capitais"]["coef"])} ({r["capitais"]["ep"]:.4f}); '
          f'interior {f4(r["interior"]["coef"])} ({r["interior"]["ep"]:.4f}); diferença {f4(r["capital_menos_interior"])} ({r["ep_capital_menos_interior"]:.4f})')
        P('  Por UF (coef, ep, seções, locais informativos):')
        for u in sorted(UFS, key=lambda u: r['por_UF'][u]['coef']):
            x = r['por_UF'][u]
            P(f'    {u} {f4(x["coef"])} ({x["ep"]:.4f}) {x["secoes"]:6d} seções, {x["locais"]:5d} locais')
        c = crit[versao]
        P('  (z sem sinal = (limite - Q10)/ep e z sinal = (Q10 - limite)/ep; cada um precisa passar de 2)')
        P(f'  Critério: sem sinal se Q10 < {f4(c["limite_sem_sinal_min_Q10_2pct"])} (menor Q10 com 2%, {c["ano_do_limite_sem_sinal"]}) por mais de 2 ep: '
          f'z = {c["z_abaixo_do_limite_sem_sinal"]:+.2f}')
        P(f'            sinal se Q10 > {f4(c["limite_sinal_max_Q10_3pct"])} (maior Q10 com 3%, {c["ano_do_limite_sinal"]}) a mais de 2 ep: '
          f'z = {c["z_acima_do_limite_sinal"]:+.2f} (com 3,6%: limite {f4(c["limite_sinal_com_3_6pct_robustez"])}, z = {c["z_acima_3_6pct"]:+.2f})')
        P(f'            robustez com o ep da referência somado: z sem sinal {c["z_sem_sinal_somando_ep_da_referencia_robustez"]:+.2f}; '
          f'z sinal {c["z_sinal_somando_ep_da_referencia_robustez"]:+.2f}')
        P(f'  Veredito pela letra: {c["veredito_pela_letra"]}')
        dv = desc[versao]
        P('  Descritivo, fora do critério registrado:')
        for ano, t in dv['troca_equivalente_pct'].items():
            P(f'    troca uniforme equivalente medida contra {ano} sem troca: {t["s"]:+.2f}% (ep {t["ep"]:.2f}; o Q10 de {ano} sobe '
              f'{t["inclinacao_Q10_por_ponto_de_troca"]:.4f} por ponto de troca)')
        sc = dv['secundaria']
        P(f'    secundária (o registro não fixou limiar para ela): {f4(sc["min_2026"])} ({sc["UF"]}, ep {sc["ep_bootstrap"]:.4f}); '
          f'referências sem troca {", ".join(a + " " + f4(x) for a, x in sc["refs_min_sem_troca"].items())}; '
          f'com 2% {", ".join(a + " " + f4(x) for a, x in sc["refs_min_2pct"].items())}; '
          f'com 3% {", ".join(a + " " + f4(x) for a, x in sc["refs_min_3pct"].items())}')
        P(f'      z abaixo do menor mínimo com 2%: {sc["z_abaixo_do_menor_min_2pct"]:+.2f}; z acima do maior mínimo com 3%: {sc["z_acima_do_maior_min_3pct"]:+.2f}')
        P()
    P('Escolhas e desvios do registro:')
    for t in DESVIOS: P('  - ' + t)
    P()
    P(f'Veredito pela letra (versão principal): {res["veredito"]}')


DESVIOS = [
    'Ordem: o registro pede as referências antes de abrir 2026. Neste script elas são calculadas e gravadas antes de a '
    'base de 2026 ser lida, mas o bweb de 2026 já tinha sido aberto por outros testes (o coeficiente nacional do T8, '
    '0,039, já estava em resultados/T8_2026_bweb_L.json). Os coeficientes por UF de 2026 não tinham sido vistos.',
    'Referências sem os eliminados separados: as bases de 2018 e 2022 só têm os outros candidatos somados (campo O). '
    'Em 2026 a versão principal separa Cury, Renan, Caiado, Zema e demais, como o registro diz; a versão com os outros '
    'agregados, igual à das referências, sai ao lado e dá o mesmo veredito.',
    'Troca de 3%: o registro manda simular 1%, 2% e 3,6%, mas o critério de sinal cita o Q10 simulado com 3%. Pela letra '
    'do critério, a troca de 3% foi simulada também; o limite com 3,6% sai ao lado.',
    'Troca simulada pelo valor esperado (s vezes os votos do adversário no 2º turno de cada seção, sem arredondar nem '
    'sortear), o que reproduz a calibração do T14 (2018: 0,0063 e 0,0261 com 2%; 2022: 0,0377 e 0,0569).',
    'Erro-padrão do Q10 (o registro não diz como): bootstrap paramétrico dos 27 coeficientes com os seus erros CR1. '
    'O limite das referências entra como valor fixo, como no T14; a versão com o erro da referência somado sai ao lado.',
    'Peso "por seções": seções da UF com os dois turnos na base. Com o peso pelas seções que entram na regressão '
    '(locais com 2 ou mais seções), o Q10 de 2026 e o limite de sem sinal (2018 com 2%, +0,0109) não mudam; o Q10 de '
    '2022 sobe (sem troca +0,0237 em vez de +0,0207; com 3%, +0,0530 em vez de +0,0501, o que sobe o limite de sinal). '
    'O veredito não muda.',
    'Percentil ponderado: o menor coeficiente cuja fração acumulada do peso chega a 10%. A versão interpolada sai ao lado.',
    'Exterior fora das 27 UFs e fora de capital contra interior. Capital contra interior: duas regressões nacionais '
    'separadas, descritivas (o registro não fixou critério para elas).',
]

if __name__ == '__main__':
    main()
