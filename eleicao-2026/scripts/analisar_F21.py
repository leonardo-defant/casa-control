"""F21 (H4) do pré-registro, Adendo 23 (commit 863a34e, 03/11/2026 01:13:05 UTC): "se repete há várias eleições".
Série descritiva, sem veredito de fraude (Adendo 18). Escrito antes de extrair 2014 e antes de calcular qualquer A.

O QUE O REGISTRO FIXA
- Anos: 2014 (se o bweb de 2014 estiver publicado e der para ligar as seções), 2018, 2022 e 2026.
- (a) A(ano) do T35 pela função de scripts/analisar_curva_forca.py SEM MUDANÇA (aqui a função ano() é importada de lá,
  não copiada), sempre nas mesmas seções entre os anos.
- (b) erro da última pesquisa Datafolha e Ibope/Ipec do 2º turno na fatia do candidato do PT (urna menos pesquisa), da
  série já conferida em resultados/contexto_virada_2t.txt (lida de resultados/contexto_virada_2t.json, mesmos números).
- Leitura: "consistente com o mesmo mecanismo a favor do PT" se, em pelo menos 3 dos anos com dado, A(ano) ficar a favor
  do candidato do PT (o candidato do PT perde menos, A de +0,015 ou mais no sentido do PT) E a urna ficar acima da
  pesquisa para o candidato do PT; "inconsistente" se isso falhar em pelo menos 2 dos anos anteriores a 2026.

O QUE O REGISTRO NÃO FIXA, DECIDIDO AQUI ANTES DE CALCULAR (declarado como desvio no resultado)
D1. Fonte de 2014. O TSE publica o bweb de 2014 (conjunto "Resultados - 2014 - Boletim de Urna" do dadosabertos.tse.jus.br,
    arquivos bweb_1t_UF_14102014*.zip e bweb_2t_UF_28102014*.zip em cdn.tse.jus.br, 27 UFs e exterior, com .sha1). O arquivo
    não tem cabeçalho; as colunas seguem o LEIAME_BUWEB.pdf de dentro do zip (31 campos, posição 0 a 30). Cada zip é
    conferido contra o .sha1 publicado. Base de 2014 montada como a de 2018 e 2022 (extrair_bweb.py): só presidente
    (cargo 1); L = 13 (Dilma, PT), R = 45 (Aécio), O = demais nominais, B = tipo de votável 2, N = tipo 3, apt, comp, loc =
    número do local de votação, urna = número da urna efetivada, tipo = descrição do tipo de urna. Não há c28 em 2014: o 28
    era Levy Fidelix, candidato válido (o c28 de 2026 é o candidato com votos anulados). Conferência: soma das seções
    contra o total oficial de contexto_virada_2t.py (Dilma, Aécio, válidos, comparecimento, branco, nulo, nos dois turnos).
D2. Ligação das seções: a mesma chave UF|município|zona|seção das bases de 2018 e 2022. Regra fixada antes de calcular A,
    para dizer se "dá para ligar" 2014:
    (i) a interseção dos quatro anos (seções com 1º e 2º turno em todos) guarda pelo menos 50% das seções de 2026 com os
        dois turnos; e
    (ii) a ligação 2014-2018 não é muito pior que a 2018-2022, que o T35 já aceitou: a correlação entre seções, dentro do
        município (fatia do PT nos válidos do 1º turno, menos a média do município, sem peso), entre 2014 e 2018 é pelo
        menos 0,8 vez a mesma correlação entre 2018 e 2022, nas seções ligadas de cada par.
    Se (i) ou (ii) falhar, 2014 fica fora da série principal e a série segue com 2018, 2022 e 2026; o A de 2014 é relatado
    só como descritivo. Também relatados (sem entrar na regra): fração das seções ligadas com o mesmo número de local nos
    dois anos e mediana da razão de aptos.
D3. "Mesmas seções entre os anos": as chaves presentes, com os dois turnos, em todos os anos da série principal. A
    função ano() recebe essa lista; cada ano usa os próprios votos e o próprio local (a faixa do local é calculada pela
    função com as seções da lista). O exterior (ZZ) entra se estiver na interseção, como no T35. Robustez fixada antes:
    (r1) interseção só de 2018, 2022 e 2026; (r2) o universo do T35 original (cada ano com as suas seções entre as chaves
    de 2026), que serve também para conferir que a função importada reproduz resultados/T35_curva_forca_bweb.json.
D4. Sentido de A. Na função, d = próprio(direita) - próprio(esquerda) e A é a média de d; o candidato do PT é sempre o
    da esquerda (L = 13) nos quatro anos. "A no sentido do PT" = -A: positivo quando o candidato do PT perde menos dos
    próprios eleitores que o da direita. Condição do ano: -A >= 0,015 pela estimativa pontual (o registro não pede
    número de erros-padrão); o erro-padrão é relatado.
D5. "Urna acima da pesquisa para o candidato do PT" num ano: a média dos erros (urna menos pesquisa, em pontos dos
    válidos) dos institutos disponíveis entre Datafolha e Ibope/Ipec fica acima de zero. Robustez: cada instituto em
    separado. Em 2026 só há Datafolha (Ipsos-Ipec não fez pesquisa nacional de 2º turno em outubro, contexto_virada_2t.txt).
    O erro do líder do 1º turno é o simétrico do erro do 2º colocado (duas candidaturas, soma 100 nos válidos).
D6. "Ano com dado": ano com A calculado na série principal e pelo menos uma das duas pesquisas.
D7. Se nem "consistente" nem "inconsistente" valerem, a leitura é "entre os dois" (o registro não nomeia esse caso).
D8. Disco: o 1º turno de 2014 tem todos os cargos (cerca de 760 MB em zip). Cada zip vai para uma pasta nova e vazia em
    /home/user/trabalho-eleicao/adendo23/F21_2014/, é conferido pelo .sha1, lido em fluxo (sem descompactar no disco) e o
    zip do 1º turno é apagado depois da extração; os do 2º turno ficam. Os SHA1 ficam no JSON de saída.

Uso:
  python3 -I analisar_F21.py extrair <turno 1|2> <saida_parcial.json.gz> <zip>
  python3 -I analisar_F21.py juntar <secoes2014.json.gz> <parcial.json.gz> [...]
  python3 -I analisar_F21.py analisar <secoes2014.json.gz|-> <secoes2018.json.gz> <secoes2022.json.gz> <secoes2026.json.gz>
          <contexto_virada_2t.json> <T35_curva_forca_bweb.json> <hashes2014.txt|-> <saida.json> <saida.txt>
"""
import os as _os, sys as _sys
_sys.path.insert(0, _os.path.dirname(_os.path.abspath(__file__)))
import collections, gzip, io, json, sys, zipfile
import numpy as np

ESQ14, DIR14 = 13, 45
LIMIAR_A = 0.015
OFICIAL_2014 = {  # contexto_virada_2t.py, E[2014] ([CAND 2014] e [DET 2014], TSE dados abertos)
    '1': {'L': 43267668, 'R': 34897211, 'validos': 104023802, 'comp': 115122883, 'B': 4420489, 'N': 6678592},
    '2': {'L': 54501118, 'R': 51041155, 'validos': 105542273, 'comp': 112683879, 'B': 1921819, 'N': 5219787},
}
PT = {2014: 'lider', 2018: 'segundo', 2022: 'lider', 2026: 'segundo'}  # posição do candidato do PT no 1º turno
INST = {2014: ('Datafolha', 'Ibope'), 2018: ('Datafolha', 'Ibope'), 2022: ('Datafolha', 'Ipec'),
        2026: ('Datafolha', 'Ipsos-Ipec')}


# ------------------------------------------------------------------------------------------------ extração de 2014
def extrair(turno, saida, zpath):
    z = zipfile.ZipFile(zpath)
    nome = [n for n in z.namelist() if n.lower().endswith(('.txt', '.csv'))][0]
    out, ruins, linhas, dup = {}, 0, 0, 0
    vistos = set()
    with z.open(nome) as fh:
        for raw in io.TextIOWrapper(fh, encoding='latin1', newline=''):
            if '"PRESIDENTE"' not in raw:
                continue
            f = raw.rstrip('\r\n')
            if not (f.startswith('"') and f.endswith('"')):
                ruins += 1; continue
            f = f[1:-1].split('";"')
            if len(f) != 31 or f[5] != '1':
                ruins += 1; continue
            linhas += 1
            k = f"{f[4]}|{int(f[12])}|{int(f[7])}|{int(f[8])}"
            tv, nv, q = int(f[24]), int(f[21]), int(f[23])
            if (k, nv) in vistos:
                dup += 1
            vistos.add((k, nv))
            s = out.setdefault(k, {}).get(turno)
            if s is None:
                s = out[k][turno] = {'loc': int(f[9]), 'urna': int(f[25] or 0), 'tipo': f[20], 'apt': int(f[15]),
                                     'comp': int(f[17]), 'L': 0, 'R': 0, 'O': 0, 'B': 0, 'N': 0}
            if tv == 2: s['B'] += q
            elif tv == 3: s['N'] += q
            elif tv == 1:
                if nv == ESQ14: s['L'] += q
                elif nv == DIR14: s['R'] += q
                else: s['O'] += q
            else:
                s.setdefault('outros_tipos', {}); s['outros_tipos'][str(tv)] = s['outros_tipos'].get(str(tv), 0) + q
    with gzip.open(saida, 'wt') as g:
        json.dump(out, g, separators=(',', ':'))
    print(json.dumps({'zip': _os.path.basename(zpath), 'secoes': len(out), 'linhas_presidente': linhas,
                      'linhas_ruins': ruins, 'votavel_repetido_na_secao': dup}))


def juntar(saida, parciais):
    tudo = {}
    for p in parciais:
        with gzip.open(p, 'rt') as f:
            for k, v in json.load(f).items():
                for t, s in v.items():
                    if t in tudo.setdefault(k, {}):
                        raise SystemExit(f'seção repetida entre arquivos: {k} turno {t}')
                    tudo[k][t] = s
    with gzip.open(saida, 'wt') as f:
        json.dump(tudo, f, separators=(',', ':'))
    print('secoes', len(tudo))


# ------------------------------------------------------------------------------------------------ análise
def soma(d):
    tot = {t: collections.Counter() for t in '12'}
    for v in d.values():
        for t in '12':
            if t in v:
                s = v[t]
                for c in ('L', 'R', 'O', 'B', 'N', 'comp', 'apt'):
                    tot[t][c] += s[c]
                tot[t]['validos'] += s['L'] + s['R'] + s['O']
                tot[t]['secoes'] += 1
                for tv, q in s.get('outros_tipos', {}).items():
                    tot[t]['outros_tipos_' + tv] += q
    return {t: dict(c) for t, c in tot.items()}


def ambos(d):
    return {k for k, v in d.items() if '1' in v and '2' in v}


def fatia_pt(s):
    v = s['L'] + s['R'] + s['O']
    return s['L'] / v if v > 0 else None


def diag_ligacao(da, db, ka, kb):
    """Diagnóstico da ligação por chave entre dois anos (seções com os dois turnos nos dois anos)."""
    com = sorted(ka & kb)
    mesmo_loc = sum(1 for k in com if da[k]['1']['loc'] == db[k]['1']['loc'])
    razao = [db[k]['1']['apt'] / da[k]['1']['apt'] for k in com if da[k]['1']['apt'] > 0]
    xs, ys, mun = [], [], []
    for k in com:
        a, b = fatia_pt(da[k]['1']), fatia_pt(db[k]['1'])
        if a is None or b is None:
            continue
        xs.append(a); ys.append(b); mun.append('|'.join(k.split('|')[:2]))
    xs, ys = np.array(xs), np.array(ys)
    _, g = np.unique(mun, return_inverse=True)
    n = np.bincount(g)
    xd = xs - (np.bincount(g, xs) / n)[g]
    yd = ys - (np.bincount(g, ys) / n)[g]
    ok = n[g] >= 2
    r_dentro = float(np.corrcoef(xd[ok], yd[ok])[0, 1])
    r_bruta = float(np.corrcoef(xs, ys)[0, 1])
    return {'ligadas': len(com), 'frac_mesmo_local': mesmo_loc / len(com) if com else None,
            'mediana_razao_aptos': float(np.median(razao)) if razao else None,
            'p10_p90_razao_aptos': [float(np.percentile(razao, 10)), float(np.percentile(razao, 90))] if razao else None,
            'corr_fatia_pt_1t_bruta': r_bruta, 'corr_fatia_pt_1t_dentro_do_municipio': r_dentro,
            'secoes_na_correlacao': int(ok.sum())}


def pesquisas(ctx):
    out = {}
    for ano in (2014, 2018, 2022, 2026):
        e = ctx['eleicoes'][str(ano)]
        pq = e.get('pesquisas') or {}
        urna_pt = e['pct_validos']['s2'] if PT[ano] == 'segundo' else e['pct_validos']['l2']
        cand = e['segundo_1t'] if PT[ano] == 'segundo' else e['lider_1t']
        item = {'candidato_pt': cand, 'posicao_1t': PT[ano], 'urna_pt_validos_2t': urna_pt, 'institutos': {}}
        for inst in INST[ano]:
            p = pq.get(inst)
            if not p:
                item['institutos'][inst] = None; continue
            pesq_pt = p['segundo'] if PT[ano] == 'segundo' else p['lider']
            erro = p['erro_segundo'] if PT[ano] == 'segundo' else -p['erro_segundo']
            assert abs(erro - (urna_pt - pesq_pt)) < 1e-9
            item['institutos'][inst] = {'pesquisa_pt': pesq_pt, 'erro_pt': erro, 'campo': p['campo'], 'fonte': p['fonte']}
        erros = [x['erro_pt'] for x in item['institutos'].values() if x]
        item['erro_medio_pt'] = float(np.mean(erros)) if erros else None
        item['urna_acima'] = (item['erro_medio_pt'] > 0) if erros else None
        item['urna_acima_em_cada_instituto'] = all(x > 0 for x in erros) if erros else None
        if ano == 2026:
            item['nota'] = e.get('pesquisas_nota') or ''
        out[ano] = item
    return out


def leitura(anos, A, pq, chave_pesq='urna_acima'):
    com_dado = [a for a in anos if A.get(a) and A[a]['A'] is not None and pq[a][chave_pesq] is not None]
    cond = {a: bool(-A[a]['A'][0] >= LIMIAR_A and pq[a][chave_pesq]) for a in com_dado}
    ok = sum(cond.values())
    falha_ant = sum(1 for a in com_dado if a < 2026 and not cond[a])
    if ok >= 3:
        r = 'consistente com o mesmo mecanismo a favor do PT'
    elif falha_ant >= 2:
        r = 'inconsistente'
    else:
        r = 'entre os dois (nem consistente nem inconsistente)'
    return {'anos_com_dado': com_dado, 'condicao_por_ano': {str(a): cond[a] for a in com_dado},
            'anos_que_cumprem': ok, 'anos_anteriores_que_falham': falha_ant, 'leitura': r}


def analisar(argv):
    from lib import carregar
    from analisar_curva_forca import ano as t35_ano  # função do T35, sem mudança
    p14, p18, p22, p26, pctx, pt35, phash, sj, st = argv
    d = {2018: carregar(p18), 2022: carregar(p22), 2026: carregar(p26)}
    if p14 != '-':
        d[2014] = carregar(p14)
    K = {a: ambos(x) for a, x in d.items()}
    out = {'teste': 'F21 (H4), Adendo 23', 'secoes_com_dois_turnos': {str(a): len(k) for a, k in K.items()},
           'c28_presente': {str(a): sum(1 for v in x.values() for t in '12' if t in v and 'c28' in v[t]) for a, x in d.items()}}
    # conferência de 2014
    if 2014 in d:
        s14 = soma(d[2014])
        out['conferencia_2014'] = {t: {c: {'base': s14[t].get(c, 0), 'oficial': OFICIAL_2014[t][c],
                                           'dif': s14[t].get(c, 0) - OFICIAL_2014[t][c]} for c in OFICIAL_2014[t]}
                                   for t in '12'}
        out['conferencia_2014']['secoes_por_turno'] = {t: s14[t]['secoes'] for t in '12'}
        out['conferencia_2014']['outros_tipos_de_votavel'] = {t: {c: q for c, q in s14[t].items()
                                                                  if c.startswith('outros_tipos')} for t in '12'}
        if phash != '-':
            out['sha1_2014'] = [l.split() for l in open(phash).read().splitlines() if l.strip()]
    # ligação
    lig = {}
    pares = [(2018, 2022), (2022, 2026), (2018, 2026)] + ([(2014, 2018), (2014, 2026)] if 2014 in d else [])
    for a, b in pares:
        lig[f'{a}-{b}'] = diag_ligacao(d[a], d[b], K[a], K[b])
    out['ligacao'] = lig
    n26 = len(K[2026])
    k3 = K[2018] & K[2022] & K[2026]
    regra = None
    if 2014 in d:
        k4 = k3 & K[2014]
        c_i = len(k4) / n26 >= 0.5
        r1418 = lig['2014-2018']['corr_fatia_pt_1t_dentro_do_municipio']
        r1822 = lig['2018-2022']['corr_fatia_pt_1t_dentro_do_municipio']
        c_ii = r1418 >= 0.8 * r1822
        regra = {'intersecao_4_anos': len(k4), 'frac_das_secoes_2026': len(k4) / n26, 'cumpre_i': c_i,
                 'corr_dentro_2014_2018': r1418, 'corr_dentro_2018_2022': r1822, 'razao': r1418 / r1822,
                 'cumpre_ii': c_ii, 'liga_2014': bool(c_i and c_ii)}
    out['regra_2014'] = regra
    liga14 = bool(regra and regra['liga_2014'])
    anos_princ = [2014, 2018, 2022, 2026] if liga14 else [2018, 2022, 2026]
    chaves_princ = sorted(k4 if liga14 else k3)
    out['serie_principal'] = {'anos': anos_princ, 'secoes': len(chaves_princ), 'frac_das_secoes_2026': len(chaves_princ) / n26}
    A = {}
    for a in anos_princ:
        A[a] = t35_ano(d[a], chaves_princ)
    out['A_serie_principal'] = {str(a): A[a] for a in anos_princ}
    # robustez r1: só 2018, 2022, 2026
    if liga14:
        Ar1 = {a: t35_ano(d[a], sorted(k3)) for a in (2018, 2022, 2026)}
    else:
        Ar1 = A
    out['A_r1_intersecao_2018_2022_2026'] = {str(a): Ar1[a] for a in (2018, 2022, 2026)}
    # robustez r2: universo do T35 original (chaves de 2026 com os dois turnos; cada ano usa as que tiver)
    ch26 = [k for k, v in d[2026].items() if '1' in v and '2' in v]
    Ar2 = {a: t35_ano(d[a], ch26) for a in d}
    out['A_r2_universo_T35'] = {str(a): Ar2[a] for a in sorted(Ar2)}
    t35 = json.load(open(pt35))
    out['conferencia_T35'] = {a: {'A_aqui': Ar2[int(a)]['A'], 'A_T35': t35[a]['A'], 'secoes_aqui': Ar2[int(a)]['secoes'],
                                  'secoes_T35': t35[a]['secoes'],
                                  'igual': abs(Ar2[int(a)]['A'][0] - t35[a]['A'][0]) < 1e-12}
                              for a in ('2018', '2022', '2026')}
    if 2014 in d and not liga14:
        out['A_2014_descritivo_intersecao_4_anos'] = t35_ano(d[2014], sorted(k3 & K[2014]))
    # pesquisas
    pq = pesquisas(json.load(open(pctx)))
    out['pesquisas'] = {str(a): v for a, v in pq.items()}
    # séries e leitura
    serie = []
    for a in (2014, 2018, 2022, 2026):
        x = A.get(a)
        serie.append({'ano': a, 'A': x['A'] if x else None, 'A_no_sentido_do_PT': (-x['A'][0] if x and x['A'] else None),
                      'A_favorece_PT': (bool(-x['A'][0] >= LIMIAR_A) if x and x['A'] else None),
                      'erro_medio_pesquisa_pt': pq[a]['erro_medio_pt'], 'urna_acima_da_pesquisa_pt': pq[a]['urna_acima']})
    out['serie'] = serie
    out['leitura'] = leitura(anos_princ, A, pq)
    out['leitura_robustez_cada_instituto'] = leitura(anos_princ, A, pq, 'urna_acima_em_cada_instituto')
    out['leitura_robustez_r1'] = leitura([2018, 2022, 2026], Ar1, pq)
    out['leitura_robustez_r2'] = leitura(sorted(Ar2), Ar2, pq)
    out['desvios'] = DESVIOS
    json.dump(out, open(sj, 'w'), ensure_ascii=False, indent=1)
    open(st, 'w').write(texto(out))
    print(texto(out))


def f(x, n=4):
    return 'n/d' if x is None else f'{x:+.{n}f}'.replace('.', ',')


def dc(x, n=3):
    return 'n/d' if x is None else f'{x:.{n}f}'.replace('.', ',')


def nb(i):
    return f'{i:,}'.replace(',', '.')


def simnao(x):
    return 'n/d' if x is None else ('sim' if x else 'não')


DESVIOS = [
    'D1. 2014 pelo bweb do TSE (publicado, 56 zips com .sha1, todos conferidos); colunas pelo LEIAME do zip; L = 13, R = 45, sem c28.',
    'D2. Regra para "dá para ligar" 2014, fixada antes de calcular A: interseção dos 4 anos com 50% ou mais das seções de 2026 e '
    'correlação dentro do município 2014-2018 de pelo menos 0,8 vez a de 2018-2022.',
    'D3. "Mesmas seções" = interseção das chaves com os dois turnos em todos os anos da série; robustez r1 (2018-2022-2026) e r2 '
    '(universo do T35 original).',
    'D4. "No sentido do PT" = -A (o PT é sempre a esquerda na função); condição pela estimativa pontual, sem exigir erros-padrão.',
    'D5. Urna acima da pesquisa = média dos erros de Datafolha e Ibope/Ipec acima de zero; robustez: cada instituto. 2026 só Datafolha.',
    'D6. Ano com dado = A calculado e pelo menos uma pesquisa.',
    'D7. Caso intermediário chamado "entre os dois" (o registro não o nomeia).',
    'D8. Zips do 1º turno de 2014 apagados depois da extração, por falta de disco; SHA1 guardados no JSON.',
    'Ocorrência: dois downloads (bweb_2t_MS e bweb_2t_SC) vieram como página "Access Denied" da CDN na rodada com 3 downloads '
    'em paralelo; o SHA1 não bateu, o arquivo foi descartado e baixado de novo, um por vez, com o mesmo curl, sem mudar user agent nem cabeçalho; '
    'os dois conferiram com o SHA1 publicado.',
]


def texto(o):
    L = []
    w = L.append
    w('F21 (H4, Adendo 23): "se repete há várias eleições". Série descritiva, sem veredito de fraude (Adendo 18).')
    w('Registro: PRE-REGISTRO-2026-10-26.md, Adendo 23, commit 863a34e (03/11/2026 01:13:05 UTC), antes de rodar.')
    w('Script: scripts/analisar_F21.py (python3 -I). Números completos: resultados/F21_serie_anos.json.')
    w('')
    if 'conferencia_2014' in o:
        c = o['conferencia_2014']
        w('1. Base de 2014: bweb do TSE (dadosabertos.tse.jus.br, "Resultados - 2014 - Boletim de Urna"; cdn.tse.jus.br/estatistica/'
          'sead/eleicoes/eleicoes2014/buweb/), 1º turno gerado em 14/10/2014, 2º em 28/10/2014, 27 UFs e exterior; 56 zips, '
          'cada um conferido pelo .sha1 publicado. Soma das seções contra o oficial:')
        for t in '12':
            w(f"   turno {t}: {nb(c['secoes_por_turno'][t])} seções; " + '; '.join(
                f"{k} {nb(c[t][k]['base'])} (oficial {nb(c[t][k]['oficial'])}, dif {c[t][k]['dif']:+d})"
                for k in ('L', 'R', 'validos', 'comp', 'B', 'N')))
        w('')
    w('2. Ligação das seções pela chave UF|município|zona|seção (seções com os dois turnos nos dois anos)')
    for p, x in o['ligacao'].items():
        w(f"   {p}: {nb(x['ligadas'])} ligadas; mesmo número de local {dc(100 * x['frac_mesmo_local'], 1)}%; mediana "
          f"aptos(2º ano)/aptos(1º ano) {dc(x['mediana_razao_aptos'])}; correlação da fatia do PT no 1º turno: bruta "
          f"{dc(x['corr_fatia_pt_1t_bruta'])}, dentro do município {dc(x['corr_fatia_pt_1t_dentro_do_municipio'])}")
    r = o['regra_2014']
    if r:
        w(f"   Regra fixada para 2014: (i) interseção dos 4 anos {nb(r['intersecao_4_anos'])} seções = "
          f"{dc(100 * r['frac_das_secoes_2026'], 1)}% das de 2026 (mínimo 50%): {'cumpre' if r['cumpre_i'] else 'falha'}; "
          f"(ii) correlação dentro do município 2014-2018 {dc(r['corr_dentro_2014_2018'])} contra 2018-2022 "
          f"{dc(r['corr_dentro_2018_2022'])}, razão {dc(r['razao'])} (mínimo 0,8): {'cumpre' if r['cumpre_ii'] else 'falha'}. "
          f"2014 {'ENTRA' if r['liga_2014'] else 'NÃO ENTRA'} na série principal.")
    w('')
    sp = o['serie_principal']
    w(f"3. Série principal: anos {', '.join(map(str, sp['anos']))}, nas mesmas {nb(sp['secoes'])} seções "
      f"({dc(100 * sp['frac_das_secoes_2026'], 1)}% das de 2026), função ano() do T35 importada sem mudança.")
    w('   A = média, pelo inverso da variância, de d = próprio(direita) - próprio(esquerda) pelas faixas; o PT é sempre a esquerda.')
    w('   "No sentido do PT" = -A (positivo: o candidato do PT perde menos dos próprios eleitores). Limiar: +0,015.')
    w('   ano  | A (ep)             | sentido do PT | A favorece PT | erro médio da pesquisa no PT | urna acima')
    for s in o['serie']:
        a = s['A']
        w(f"   {s['ano']} | {f(a[0]) if a else 'n/d'} ({dc(a[1], 4) if a else 'n/d'}) | {f(s['A_no_sentido_do_PT']):>13} | "
          f"{simnao(s['A_favorece_PT']):>13} | {f(s['erro_medio_pesquisa_pt'], 2):>28} | {simnao(s['urna_acima_da_pesquisa_pt'])}")
    w('')
    w('   Faixas (fatia do adversário no local, 1º turno): coeficiente dos próprios votos do PT e da direita, e d')
    for a, x in o['A_serie_principal'].items():
        for fx in x['faixas']:
            fa = fx['faixa'].replace('.', ',')
            if 'd' in fx:
                w(f"   {a} {fa}: PT {f(fx['proprio_L'][0])} ({dc(fx['proprio_L'][1], 4)}), direita {f(fx['proprio_R'][0])} "
                  f"({dc(fx['proprio_R'][1], 4)}), d {f(fx['d'][0])} ({dc(fx['d'][1], 4)}); locais {nb(fx['locais_L'])}/{nb(fx['locais_R'])}")
            else:
                w(f"   {a} {fa}: fora ({fx.get('fora')})")
    w('')
    w('4. Pesquisas (urna menos pesquisa na fatia do candidato do PT, pontos dos válidos; resultados/contexto_virada_2t)')
    for a, p in o['pesquisas'].items():
        partes = []
        for inst, x in p['institutos'].items():
            partes.append(f"{inst} {x['pesquisa_pt']} -> {f(x['erro_pt'], 2)} ({x['campo']})" if x else f"{inst} sem pesquisa")
        w(f"   {a} {p['candidato_pt']} (urna {dc(p['urna_pt_validos_2t'], 2)}): " + '; '.join(partes))
    w('')
    le = o['leitura']
    w(f"5. Leitura fixada antes: {le['leitura'].upper()} (sem veredito de fraude)")
    cond = ', '.join(f"{a} {simnao(v)}" for a, v in le['condicao_por_ano'].items())
    w(f"   Anos com dado: {', '.join(map(str, le['anos_com_dado']))}. Condição (A no sentido do PT de +0,015 ou mais E urna acima "
      f"da pesquisa) por ano: {cond}. Cumprem {le['anos_que_cumprem']} (consistente pede 3). Anos anteriores a 2026 que "
      f"falham: {le['anos_anteriores_que_falham']} (2 bastam para inconsistente).")
    for nome, chave in (('cada instituto em separado', 'leitura_robustez_cada_instituto'),
                        ('r1, só 2018-2022-2026 nas mesmas seções', 'leitura_robustez_r1'),
                        ('r2, universo do T35 original', 'leitura_robustez_r2')):
        cond = ', '.join(f"{a} {simnao(v)}" for a, v in o[chave]['condicao_por_ano'].items())
        w(f"   Robustez ({nome}): {o[chave]['leitura']} ({cond})")
    w('')
    w('6. Conferência da função do T35 (universo original contra resultados/T35_curva_forca_bweb.json)')
    for a, x in o['conferencia_T35'].items():
        w(f"   {a}: A aqui {f(x['A_aqui'][0], 6)}, no T35 {f(x['A_T35'][0], 6)}, seções {nb(x['secoes_aqui'])} e "
          f"{nb(x['secoes_T35'])}: {'igual' if x['igual'] else 'DIFERENTE'}")
    w('   Sensibilidade de A ao conjunto de seções (A e erro-padrão):')
    for a in ('2014', '2018', '2022', '2026'):
        partes = []
        for nome, chave in (('principal', 'A_serie_principal'), ('r1', 'A_r1_intersecao_2018_2022_2026'), ('r2', 'A_r2_universo_T35')):
            x = o[chave].get(a)
            if x and x['A']:
                partes.append(f"{nome} {f(x['A'][0])} ({dc(x['A'][1], 4)}; {nb(x['secoes'])} seções)")
        w(f"   {a}: " + '; '.join(partes))
    if 'A_2014_descritivo_intersecao_4_anos' in o:
        x = o['A_2014_descritivo_intersecao_4_anos']
        w(f"   2014 só descritivo (fora da série principal): A {f(x['A'][0]) if x['A'] else 'n/d'}")
    w('')
    # interpretação, gerada a partir dos números
    S = {s['ano']: s for s in o['serie']}
    sens = {a: [o[c][a]['A'][0] for c in ('A_serie_principal', 'A_r1_intersecao_2018_2022_2026', 'A_r2_universo_T35')
                if a in o[c] and o[c][a]['A']] for a in ('2014', '2018', '2022', '2026')}
    amp = {a: (max(v) - min(v)) for a, v in sens.items() if len(v) > 1}
    w('7. O que isso significa')
    w('   A leitura registrada pede o mesmo sinal a favor do PT, nas duas séries, em pelo menos 3 anos. Isso só acontece em 2026.')
    w(f"   Pesquisas: a urna ficou ABAIXO da última Datafolha e da última Ibope/Ipec para o candidato do PT em 2014 "
      f"({f(S[2014]['erro_medio_pesquisa_pt'], 2)} em média), 2018 ({f(S[2018]['erro_medio_pesquisa_pt'], 2)}) e 2022 "
      f"({f(S[2022]['erro_medio_pesquisa_pt'], 2)}); só em 2026 ficou acima ({f(S[2026]['erro_medio_pesquisa_pt'], 2)}, Datafolha). "
      'Uma distância urna x pesquisa a favor do PT "que se repete" não existe na série: 2026 é o único ano com esse sinal.')
    w(f"   A do T35: em 2018 ({f(S[2018]['A'][0])}) e 2022 ({f(S[2022]['A'][0])}) o candidato do PT perdeu MAIS dos próprios "
      f"eleitores que o da direita; em 2014 os dois perderam o mesmo na média ({f(S[2014]['A'][0])}); em 2026 Flávio perdeu mais "
      f"({f(S[2026]['A'][0])}). Também não há um sinal a favor do PT que se repita.")
    w(f"   2026 passa no limiar por pouco: {f(S[2026]['A_no_sentido_do_PT'])} contra +0,0150 nas {nb(sp['secoes'])} seções da série; "
      f"com só 2018-2022-2026 (r1) dá {f(-o['A_r1_intersecao_2018_2022_2026']['2026']['A'][0])} e não passaria; no universo do "
      f"T35 dá {f(-o['A_r2_universo_T35']['2026']['A'][0])}. Isso não muda a leitura (os três anos anteriores falham nos dois "
      'critérios).')
    w(f"   Cético nos dois sentidos: (a) a leitura INCONSISTENTE diz que o padrão de 2026 não aparece em 2014, 2018 e 2022; não "
      'diz que 2026 é limpa nem que é fraudada. Pelo Adendo 18, a série não serve de régua. (b) O erro-padrão de A (cerca de '
      f"0,001) subestima a incerteza real: só trocar o conjunto de seções muda A em até {dc(max(amp.values()), 4)} "
      f"(2018: de {f(min(sens['2018']))} a {f(max(sens['2018']))}), oito a dez vezes o erro-padrão. Diferenças de A menores que "
      'uns 0,01 entre anos não devem ser lidas. (c) São quatro eleições: uma série, não uma distribuição.')
    w('')
    w('8. Pistas (descritivas, vistas depois de rodar; nada aqui foi registrado antes)')
    fx = {a: [z['d'][0] for z in o['A_serie_principal'][a]['faixas'] if 'd' in z] for a in o['A_serie_principal']}
    w('   d por faixa de força do adversário (menos de 35%, 35-50%, 50-65%, 65% ou mais), mesmas seções:')
    for a, v in fx.items():
        w(f"   {a}: " + ', '.join(f(x) for x in v))
    w('   (1) O formato da curva de 2026 (a direita perde cada vez mais que o PT conforme o PT é mais forte no local) já existia '
      'em 2014, com Aécio, e mais forte: na faixa de 65% ou mais, Aécio perdeu '
      f"{dc(-100 * o['A_serie_principal']['2014']['faixas'][3]['proprio_R'][0], 1)}% dos próprios eleitores e Dilma "
      f"{dc(-100 * o['A_serie_principal']['2014']['faixas'][3]['proprio_L'][0], 1)}%; em 2026, Flávio "
      f"{dc(-100 * o['A_serie_principal']['2026']['faixas'][3]['proprio_R'][0], 1)}% e Lula "
      f"{dc(-100 * o['A_serie_principal']['2026']['faixas'][3]['proprio_L'][0], 1)}%. O A de 2014 dá perto de zero só porque a faixa "
      'de menos de 35%, a de mais locais e menor erro-padrão, vai no sentido oposto e pesa mais na média. Em 2014 a urna ficou '
      'abaixo das pesquisas para o PT. Ou seja: a assinatura (b)/(c) de H2 apareceu numa eleição em que o PT ficou abaixo das '
      'pesquisas; ela não é exclusiva de 2026 e não anda junto com o erro das pesquisas.')
    w('   (2) O sentido de d nas faixas de 35% para cima acompanha quem estava no governo, nos quatro anos (o A de 2014, perto de zero, não): 2014 (Dilma, PT, no governo): a direita perde mais '
      'nas faixas de 35% para cima; 2018 (sem candidato à reeleição): quase igual, fora da faixa de menos de 35%; 2022 (Bolsonaro '
      'no governo): o PT perde mais em todas as faixas; 2026 (Lula no governo): a direita perde mais. Isso é post hoc e são '
      'quatro pontos. É compatível com uma vantagem natural de quem governa e também com um mecanismo "a favor do governo", '
      'que não é a hipótese H4 registrada (a favor do PT). Separar as duas pede anos com o governo de um lado e o PT do outro '
      'antes de 2014 (2002: Serra no governo) e com o PT no governo (2006, 2010); o TSE publica votação por seção desses anos '
      '(votacao_secao), não bweb, e a ligação com 2014 teria de ser testada como aqui, com critério registrado antes.')
    w('   (3) Pesquisas no candidato do governo: 2014 Dilma ' + f(S[2014]['erro_medio_pesquisa_pt'], 2) +
      ', 2022 Bolsonaro ' + f(-S[2022]['erro_medio_pesquisa_pt'], 2) + ', 2026 Lula ' + f(S[2026]['erro_medio_pesquisa_pt'], 2) +
      ' (urna menos pesquisa). Duas vezes acima e uma abaixo: também não há regularidade.')
    w('')
    w('9. Decisões não fixadas no registro, tomadas antes de calcular A (escritas no docstring do script)')
    for x in DESVIOS:
        w('   ' + x)
    txt = '\n'.join(L) + '\n'
    for ch in (chr(0x2014), chr(0x2013)):
        assert ch not in txt
    return txt

if __name__ == '__main__':
    import os
    cmd = sys.argv[1]
    if cmd == 'extrair':
        extrair(sys.argv[2], sys.argv[3], sys.argv[4])
    elif cmd == 'juntar':
        juntar(sys.argv[2], sys.argv[3:])
    elif cmd == 'analisar':
        analisar(sys.argv[2:])
    else:
        raise SystemExit(__doc__)
