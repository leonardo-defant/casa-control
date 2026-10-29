"""L7 do Adendo 18: o que uma fraude no programa teria de driblar (pesquisa, sem critério numérico).

Registro (PRE-REGISTRO-2026-10-26.md, Adendo 18, L7, antes de rodar):
  "Como funcionou o teste de integridade do 2º turno de 2026 (quantas urnas, se usa eleitores reais e biometria, se a
  urna consegue saber que está em teste), o que dizem os relatórios e as auditorias de partidos, inclusive do PL. Lista
  do que uma fraude no programa precisaria fazer para passar por cada controle. Relatado como argumento, sem veredito."

O L7 é pesquisa. Este script junta a parte que os dados locais conseguem conferir; tudo aqui é DESCRITIVO, fora do
registro, sem limiar e sem veredito. Especificação fixada neste arquivo antes de calcular a virada de qualquer grupo:

  D1. Pegada do teste de integridade no bweb. Pela regra (guia do TRE-RJ, TRE-RR, Agência Brasil 24/10/2026), a urna da
      seção sorteada no sábado vai para o teste e a seção vota numa urna nova, com carga nova e lacre no mesmo sábado.
      Grupo S = seções com NR_URNA_EFETIVADA do 2º turno diferente da do 1º turno e DT_CARGA_URNA_EFETIVADA no dia
      2026-10-24 (véspera do 2º turno). Contagem por UF, comparada com os números de urnas anunciados pelos TREs
      (dicionário ANUNCIADO, com a fonte de cada um). Conferência nominal com a lista publicada de Alagoas (LISTA_AL):
      as 20 seções de integridade (18 + 2 com biometria) têm de estar em S e as 3 de autenticidade, fora (o teste de
      autenticidade não troca urna). No 1º turno, mesma contagem pela data de carga 2026-10-03, se o cache do 1º turno
      existir (sem a troca de urna, que não tem turno anterior).
  D2. A urna consegue saber que está em teste? Na modalidade em ambiente controlado de 2026 a urna é habilitada pelo
      caderno de votação, sem eleitor presente: nenhuma habilitação biométrica no dia. Na modalidade com biometria, só
      voluntários, todos habilitados pela digital. Medida nas urnas reais da amostra de logs do 2º turno (3.897 urnas,
      dia 25/10/2026): por urna, habilitações ('Eleitor foi habilitado') e habilitações biométricas ('Tipo de
      habilitação do eleitor [biométrica]'); conta urnas com 0% de biometria, com 100%, e com poucos eleitores e quase
      tudo biométrico (até 100 habilitações e 95% ou mais biométricas). No país inteiro (bweb), o campo
      QT_ELEI_BIOM_SEM_HABILITACAO ("eleitores com biometria que não foram habilitados por meio dela") dá um piso da
      parte não biométrica: seções com QT_ELEI_BIOM_SEM_HABILITACAO >= comparecimento > 0 certamente não tiveram nenhuma
      habilitação biométrica. A relação entre o campo e o log é conferida na amostra.
  D3. Se o programa usasse "nenhuma biometria" para reconhecer o teste e ficar honesto, as seções reais com essa marca
      ficariam sem o desvio, e a virada de Lula nelas seria menor que a das outras seções do mesmo local. Grupos por
      r = QT_ELEI_BIOM_SEM_HABILITACAO / comparecimento: r >= 1 (nenhuma biometria, certo), r >= 0,9, r >= 0,5.
      y = 100 L2/(L2+R2) - 100 L1/(L1+R1); efeito fixo de local; peso L2+R2; erro agrupado por local (lib.fe_ols),
      como no L2. Régua de leitura, não limiar: um desvio que mudasse o resultado tira de Flávio e dá a Lula cerca de
      margem/(2 V) dos votos dos finalistas (V = L2+R2 no país), ou seja, a virada nas seções poupadas ficaria menor
      nessa quantidade (em pontos). Com menos de 30 seções do grupo em locais onde o grupo varia, só a contagem.
  D4. Escala: com n urnas no teste (n = 500, 640 e o teto do D1), a chance de nenhuma urna adulterada cair no teste se o
      programa adulterasse uma fração p das urnas ao acaso, sem reconhecer o teste, para mover margem/2 votos com k
      votos por urna (k = 10, 25, 50, 100 e todos os votos dos finalistas da urna média); e, para um desvio espalhado em
      todas as urnas, quantos votos divergentes o teste esperaria ver com 195 votos digitados por urna (389 em 2 urnas
      no TSE, 2º turno) e com 75 por urna (média de 70 a 80 voluntários no teste com biometria de SP, 1º turno).

Uso: python3 -I analisar_L7.py <secoes2026.json.gz> <zips2t_dir> <cache_1t.json.gz|-> <amostra_arq_2t|-> <saida.json> <saida.txt>
"""
import os as _os, sys as _sys
_sys.path.insert(0, _os.path.dirname(_os.path.abspath(__file__)))
import collections, glob, gzip, json, math, os, sys, time, zipfile
from multiprocessing import Pool
import numpy as np
from lib import carregar, chave_local, fe_ols

VESPERA_2T, VESPERA_1T = '2026-10-24', '2026-10-03'
CAMPOS = ['NR_URNA_EFETIVADA', 'DT_CARGA_URNA_EFETIVADA', 'QT_ELEI_BIOM_SEM_HABILITACAO', 'QT_COMPARECIMENTO',
          'NM_MUNICIPIO', 'NR_JUNTA_APURADORA']

# Urnas do Teste de Integridade do 2º turno anunciadas pelos TREs (integridade, com e sem biometria; sem autenticidade).
ANUNCIADO = {
    'SP': (33, '30 sem e 3 com biometria; TRE-SP 25/10 (página 403, trecho do buscador): https://www.tre-sp.jus.br/comunicacao/noticias/2026/Outubro/teste-de-integridade-das-urnas-no-2o-turno-e-concluido-sem-divergencias-em-sao-paulo'),
    'MG': (33, 'Agência Brasil 24/10 16h13: https://agenciabrasil.ebc.com.br/justica/noticia/2026-10/tribunais-eleitorais-definem-urnas-que-serao-auditadas-no-2o-turno'),
    'RJ': (33, 'Agência Brasil 24/10'), 'BA': (33, 'Agência Brasil 24/10'),
    'PR': (27, 'Agência Brasil 24/10 (2 com biometria, TRE-PR)'), 'RS': (27, 'Agência Brasil 24/10'),
    'PE': (27, 'Agência Brasil 24/10'), 'CE': (27, 'Agência Brasil 24/10'), 'RR': (20, 'Agência Brasil 24/10'),
    'DF': (20, '16 na CLDF, 2 no TSE, 2 com biometria; Agência CLDF via https://bombabomba.com.br/urnas-eletronicas-sao-aprovadas-em-teste-de-integridade-realizado-na-cldf-no-2o-turno/'),
    'AL': (20, '18 + 2 com biometria; lista nominal: https://francesnews.com.br/post/2026/10/26/43576-treal-sorteia-23-urnas-eletronicas-para-auditoria-no-segundo-turno-das-eleicoes-2026'),
    'MT': (20, '19 + 1 com biometria; TRE-MT (página 403, trecho do buscador)'),
    'PB': (20, '19 + 1 com biometria; https://www.paraibamix.com.br/eleicoes-2026-confira-as-secoes-eleitorais-da-paraiba-selecionadas-para-auditoria-no-2o-turno/'),
    'ES': (18, 'em ambiente controlado; TRE-ES (página 403, trecho do buscador); com biometria não informado'),
}
# Alagoas, 2º turno: (município, zona, seção, tipo) com tipo B = integridade com biometria, I = integridade, A = autenticidade.
LISTA_AL = [('MACEIÓ', 2, 365, 'B'), ('MACEIÓ', 2, 355, 'B'), ('MACEIÓ', 1, 375, 'I'), ('TRAIPU', 20, 84, 'I'),
            ('MACEIÓ', 54, 566, 'I'), ('MARECHAL DEODORO', 26, 29, 'I'), ('SANTANA DO IPANEMA', 19, 234, 'I'),
            ('BRANQUINHA', 9, 12, 'I'), ('MONTEIRÓPOLIS', 29, 76, 'I'), ('POÇO DAS TRINCHEIRAS', 50, 37, 'I'),
            ('ÁGUA BRANCA', 39, 63, 'I'), ('GIRAU DO PONCIANO', 44, 32, 'I'), ('CORURIPE', 7, 150, 'I'),
            ('MARAGOGI', 14, 129, 'I'), ('FEIRA GRANDE', 49, 80, 'I'), ('PÃO DE AÇÚCAR', 11, 15, 'I'),
            ('JOAQUIM GOMES', 53, 5, 'I'), ('SÃO JOSÉ DA TAPERA', 51, 90, 'I'), ('IGREJA NOVA', 37, 187, 'I'),
            ('TEOTÔNIO VILELA', 34, 96, 'I'), ('SÃO LUÍS DO QUITUNDE', 17, 150, 'A'), ('JEQUIÁ DA PRAIA', 18, 187, 'A'),
            ('ARAPIRACA', 22, 519, 'A')]


def log(msg):
    print(time.strftime('%H:%M:%S'), msg, flush=True)


def ler_zip(zpath):
    """Uma linha por seção (presidente ou seção sem voto): campos da urna, da carga e da biometria."""
    z = zipfile.ZipFile(zpath)
    nome = [n for n in z.namelist() if n.lower().endswith('.csv')][0]
    out = {}
    pres = b';1;"Presidente";'; semvoto = b';-1;"#NULO#";-1;'
    with z.open(nome) as fh:
        cab = [c.strip().strip('"') for c in fh.readline().decode('latin1').strip().split(';')]
        ix = {c: i for i, c in enumerate(cab)}
        for linha in fh:
            if pres not in linha and semvoto not in linha:
                continue
            p = [x.strip('"') for x in linha.decode('latin1').rstrip('\r\n').split(';')]
            k = f"{p[ix['SG_UF']]}|{int(p[ix['CD_MUNICIPIO']])}|{int(p[ix['NR_ZONA']])}|{int(p[ix['NR_SECAO']])}"
            v = {c: p[ix[c]] for c in CAMPOS}
            if k in out and out[k] != v:
                out[k]['_conflito'] = True
            out.setdefault(k, v)
    return os.path.basename(zpath), out


def ler_logs(pasta):
    """Por urna da amostra: habilitações e habilitações biométricas no dia do 2º turno."""
    from decodificar import _linhas_log
    rows = {}
    for raiz, dirs, arqs in os.walk(pasta):
        logs = [a for a in arqs if a.endswith('-log.jez')]
        if not logs:
            continue
        uf, m, z, s = raiz.split('arq/')[-1].split('/')
        k = f'{uf.upper()}|{int(m)}|{int(z)}|{int(s)}'
        c = collections.Counter()
        for bloco in _linhas_log(os.path.join(raiz, sorted(logs)[-1])):
            for l in bloco:
                p = l.split('\t')
                if len(p) < 5 or p[0][:10] != '25/10/2026':
                    continue
                if p[4] == 'Eleitor foi habilitado': c['hab'] += 1
                elif p[4] == 'Tipo de habilitação do eleitor [biométrica]': c['bio'] += 1
                elif p[4] == 'O voto do eleitor foi computado': c['comp'] += 1
        rows[k] = dict(c)
    return rows


def fmt(x, nd=2):
    return f'{x:,.{nd}f}'.replace(',', 'X').replace('.', ',').replace('X', '.')


def inteiro(x):
    return f'{int(x):,}'.replace(',', '.')


def main():
    base_p, zdir, cache1t, amostra, saida_json, saida_txt = sys.argv[1:7]
    base = carregar(base_p)
    log(f'base: {len(base)} seções')
    zips = sorted(glob.glob(os.path.join(zdir, '*.zip')))
    with Pool(min(8, len(zips))) as P:
        partes = P.map(ler_zip, zips)
    bw = {}
    conflitos = 0
    for nome, d in partes:
        for k, v in d.items():
            conflitos += bool(v.pop('_conflito', False))
            bw[k] = v
    log(f'bweb 2º turno: {len(bw)} seções, {len(zips)} zips, conflitos {conflitos}')
    out = {'registro': 'PRE-REGISTRO-2026-10-26.md, Adendo 18, L7 (pesquisa, sem critério numérico, sem veredito)',
           'veredito': 'DESCRITIVO', 'zips_2t': [os.path.basename(z) for z in zips], 'secoes_bweb_2t': len(bw),
           'conflitos_campos_mesma_secao': conflitos}

    # ---------------- D1: pegada do teste de integridade
    S = {}
    vespera_mesma_urna = []
    for k, v in bw.items():
        if v['DT_CARGA_URNA_EFETIVADA'][:10] != VESPERA_2T:
            continue
        s = base.get(k, {})
        if '1' in s and '2' in s and s['1'].get('urna') != s['2'].get('urna'):
            S[k] = v
        else:
            vespera_mesma_urna.append(k)
    por_uf = collections.Counter(k.split('|')[0] for k in S)
    # uma seção por zona é a regra do teste convencional; o teste com biometria concentra seções num local
    zonas = collections.defaultdict(collections.Counter)
    locais = collections.defaultdict(collections.Counter)
    for k in S:
        uf, m, z, se = k.split('|')
        zonas[uf][(m, z)] += 1
        locais[uf][(m, z, base[k]['2']['loc'])] += 1
    tab = {}
    for uf in sorted(set(por_uf) | set(ANUNCIADO)):
        a = ANUNCIADO.get(uf)
        tab[uf] = {'bweb_S': por_uf.get(uf, 0), 'anunciado': a[0] if a else None, 'fonte': a[1] if a else None,
                   'zonas': len(zonas[uf]), 'zonas_com_mais_de_1': sum(1 for x in zonas[uf].values() if x > 1),
                   'locais_com_mais_de_1': sum(1 for x in locais[uf].values() if x > 1)}
    out['D1'] = {'S_total': len(S), 'vespera_mesma_urna': sorted(vespera_mesma_urna), 'por_uf': tab}
    # Alagoas, nominal
    cod = {}
    for k, v in bw.items():
        if k.startswith('AL|'):
            cod[v['NM_MUNICIPIO']] = int(k.split('|')[1])
    al = []
    for m, z, se, t in LISTA_AL:
        k = f'AL|{cod.get(m)}|{z}|{se}'
        s = base.get(k, {})
        al.append({'secao': k, 'municipio': m, 'tipo': t, 'em_S': k in S,
                   'carga_2t': bw.get(k, {}).get('DT_CARGA_URNA_EFETIVADA'),
                   'urna_1t': s.get('1', {}).get('urna'), 'urna_2t': s.get('2', {}).get('urna')})
    S_al = {k for k in S if k.startswith('AL|')}
    lista_al = {x['secao'] for x in al}
    out['D1']['alagoas'] = {'lista': al,
                            'integridade_em_S': sum(1 for x in al if x['tipo'] in 'BI' and x['em_S']),
                            'integridade_total': sum(1 for x in al if x['tipo'] in 'BI'),
                            'autenticidade_em_S': sum(1 for x in al if x['tipo'] == 'A' and x['em_S']),
                            'S_fora_da_lista': sorted(S_al - lista_al)}
    # 1º turno, pela data de carga
    if cache1t != '-' and os.path.exists(cache1t):
        c1 = carregar(cache1t)['secoes']
        v1 = collections.Counter(k.split('|')[0] for k, v in c1.items() if v[0][4][:10] == VESPERA_1T)
        out['D1']['primeiro_turno_carga_na_vespera'] = {'total': sum(v1.values()), 'por_uf': dict(sorted(v1.items()))}
    log(f'D1: S = {len(S)}; Alagoas {out["D1"]["alagoas"]["integridade_em_S"]}/{out["D1"]["alagoas"]["integridade_total"]}')

    # ---------------- D2: marca da biometria nas urnas reais
    d2 = {}
    if amostra != '-' and os.path.isdir(amostra):
        lg = ler_logs(amostra)
        rows = []
        for k, c in lg.items():
            v = bw.get(k)
            if not v or not c.get('hab'):
                continue
            rows.append((k, c.get('hab', 0), c.get('bio', 0), c.get('comp', 0), int(v['QT_COMPARECIMENTO']),
                         int(v['QT_ELEI_BIOM_SEM_HABILITACAO'])))
        hab = np.array([r[1] for r in rows], float); bio = np.array([r[2] for r in rows], float)
        comp_log = np.array([r[3] for r in rows]); comp_bw = np.array([r[4] for r in rows]); sem = np.array([r[5] for r in rows], float)
        share = bio / hab
        nb = hab - bio
        d2 = {'urnas': len(rows), 'comp_log_igual_bweb': int((comp_log == comp_bw).sum()),
              'habilitacoes': int(hab.sum()), 'biometricas': int(bio.sum()), 'pct_biometrica': float(100 * bio.sum() / hab.sum()),
              'urnas_0pct_bio': int((bio == 0).sum()), 'urnas_100pct_bio': int((bio == hab).sum()),
              'urnas_ate_100_hab_e_95pct_bio': int(((hab <= 100) & (share >= 0.95)).sum()),
              'urnas_ate_100_hab': int((hab <= 100).sum()),
              'share_bio_quantis': {q: float(np.quantile(share, q / 100)) for q in (0, 1, 5, 50, 95, 99, 100)},
              'hab_quantis': {q: float(np.quantile(hab, q / 100)) for q in (0, 1, 5, 10, 50, 90)},
              'urnas_share_bio_ge_098': int((share >= 0.98).sum()),
              'campo_bweb_contra_log': {
                  'sem_hab_igual_nao_bio': int((sem == nb).sum()),
                  'sem_hab_menor_que_nao_bio': int((sem < nb).sum()),
                  'sem_hab_maior_que_nao_bio': int((sem > nb).sum()),
                  'nao_bio_total': int(nb.sum()), 'sem_hab_total': int(sem.sum())}}
        log(f'D2: {len(rows)} urnas; 0% bio {d2["urnas_0pct_bio"]}; 100% bio {d2["urnas_100pct_bio"]}')
    out['D2_amostra_logs'] = d2

    # país inteiro pelo bweb
    keys, Y, W, LOC, R = [], [], [], [], []
    sem_bio_certo = []
    nac = collections.Counter()
    V2 = L2t = R2t = 0
    for k, s in base.items():
        if '1' not in s or '2' not in s:
            continue
        a, b = s['1'], s['2']
        V2 += b['L'] + b['R']; L2t += b['L']; R2t += b['R']
        v = bw.get(k)
        if v is None:
            continue
        comp = int(v['QT_COMPARECIMENTO']); sh = int(v['QT_ELEI_BIOM_SEM_HABILITACAO'])
        if comp > 0:
            nac['com_comparecimento'] += 1
            if sh >= comp:
                sem_bio_certo.append(k)
        if a['L'] + a['R'] <= 0 or b['L'] + b['R'] <= 0 or comp <= 0:
            continue
        keys.append(k)
        Y.append(100 * b['L'] / (b['L'] + b['R']) - 100 * a['L'] / (a['L'] + a['R']))
        W.append(b['L'] + b['R'])
        LOC.append(chave_local(k, b))
        R.append(sh / comp)
    Y = np.array(Y); W = np.array(W, float); LOC = np.array(LOC); R = np.array(R)
    margem = L2t - R2t
    regua = 100 * (margem / 2) / V2
    uf_sem = collections.Counter(k.split('|')[0] for k in sem_bio_certo)
    out['D2_bweb_pais'] = {'secoes_com_comparecimento': nac['com_comparecimento'],
                           'secoes_sem_nenhuma_biometria_certo': len(sem_bio_certo),
                           'por_uf': dict(sorted(uf_sem.items())), 'lista': sorted(sem_bio_certo)[:200],
                           'r_quantis': {q: float(np.quantile(R, q / 100)) for q in (50, 90, 99, 99.9, 100)}}
    log(f'bweb: {len(sem_bio_certo)} seções sem nenhuma biometria (certo)')

    # ---------------- D3: virada nas seções com a marca do teste
    d3 = {'regua_pontos': regua, 'margem': int(margem), 'V2': int(V2)}
    _, gi = np.unique(LOC, return_inverse=True)
    for nome, lim in (('r>=1', 1.0), ('r>=0,9', 0.9), ('r>=0,5', 0.5)):
        g = (R >= lim).astype(float)
        n_g = int(g.sum())
        # seções do grupo em locais onde o grupo varia
        soma = np.bincount(gi, weights=g); cnt = np.bincount(gi)
        varia = (soma[gi] > 0) & (soma[gi] < cnt[gi])
        n_id = int((varia & (g == 1)).sum())
        item = {'secoes_grupo': n_g, 'identificam': n_id,
                'virada_media_grupo': float(np.average(Y[g == 1], weights=W[g == 1])) if n_g else None,
                'virada_media_resto': float(np.average(Y[g == 0], weights=W[g == 0]))}
        if n_id >= 30:
            r = fe_ols(Y, g[:, None], LOC, W, ['grupo'])
            item.update({'coef': r['coef']['grupo'], 'ep': r['ep']['grupo'], 'n': r['n'], 'locais': r['grupos']})
            rp = fe_ols(np.array([100 * base[k]['1']['L'] / (base[k]['1']['L'] + base[k]['1']['R']) for k in keys]),
                        g[:, None], LOC, W, ['grupo'])
            item['placebo_fatia_lula_1t'] = {'coef': rp['coef']['grupo'], 'ep': rp['ep']['grupo']}
        d3[nome] = item
    out['D3'] = d3
    log('D3: ' + json.dumps({k: (v.get('coef'), v.get('ep'), v['identificam']) for k, v in d3.items() if isinstance(v, dict)}))

    # ---------------- D4: escala
    mover = margem / 2
    media_urna = V2 / len(keys)
    tetos = sorted({500, 640, len(S)})
    esc = {'mover': mover, 'fracao_votos_finalistas': mover / V2, 'votos_finalistas_por_secao': media_urna, 'cenarios': []}
    for k_ in (10, 25, 50, 100, media_urna):
        urnas = mover / k_
        p = urnas / len(keys)
        esc['cenarios'].append({'k_votos_por_urna': k_, 'urnas_adulteradas': urnas, 'p': p,
                                'P_nenhuma_no_teste': {str(n): (1 - p) ** n if p < 1 else 0.0 for n in tetos}})
    esc['espalhado'] = {'votos_digitados_por_urna': {'195': 195 * mover / V2, '75': 75 * mover / V2},
                        'em_n_urnas': {str(n): {'195': n * 195 * mover / V2, '75': n * 75 * mover / V2} for n in tetos}}
    out['D4'] = esc
    json.dump(out, open(saida_json, 'w'), ensure_ascii=False, indent=1)
    log(f'gravado {saida_json}')
    escrever_txt(out, saida_txt)


def escrever_txt(o, caminho):
    """O texto do L7 (pesquisa) vem do arquivo L7_teste_integridade_pesquisa.txt; aqui só a parte dos dados."""
    L = []
    d1 = o['D1']; al = d1['alagoas']
    L.append('L7, parte dos dados (descritivo, fora do registro). Script: scripts/analisar_L7.py.')
    L.append(f"D1. Seções do 2º turno com urna trocada e carga no sábado {VESPERA_2T}: {inteiro(d1['S_total'])}"
             f" (mais {len(d1['vespera_mesma_urna'])} com carga no sábado e a mesma urna).")
    for uf, t in d1['por_uf'].items():
        L.append(f"  {uf}: bweb {t['bweb_S']}; anunciado {t['anunciado'] if t['anunciado'] is not None else '-'};"
                 f" zonas {t['zonas']} (com mais de uma: {t['zonas_com_mais_de_1']}); locais com mais de uma: {t['locais_com_mais_de_1']}")
    L.append(f"  Alagoas, lista nominal: {al['integridade_em_S']} de {al['integridade_total']} seções de integridade no grupo; "
             f"{al['autenticidade_em_S']} das 3 de autenticidade no grupo; seções do grupo fora da lista: {len(al['S_fora_da_lista'])}.")
    if 'primeiro_turno_carga_na_vespera' in d1:
        L.append(f"  1º turno, carga em {VESPERA_1T}: {inteiro(d1['primeiro_turno_carga_na_vespera']['total'])} seções.")
    d2 = o['D2_amostra_logs']
    if d2:
        L.append(f"D2. Amostra de logs do 2º turno: {inteiro(d2['urnas'])} urnas, {inteiro(d2['habilitacoes'])} habilitações, "
                 f"{fmt(d2['pct_biometrica'], 1)}% biométricas. Urnas com 0% de biometria: {d2['urnas_0pct_bio']}; com 100%: "
                 f"{d2['urnas_100pct_bio']}; com 98% ou mais: {d2['urnas_share_bio_ge_098']}; até 100 habilitações e 95% ou mais "
                 f"biométricas: {d2['urnas_ate_100_hab_e_95pct_bio']} (até 100 habilitações: {d2['urnas_ate_100_hab']}).")
        q = d2['share_bio_quantis']
        L.append(f"  Parte biométrica por urna: mínimo {fmt(100*q[0],1)}%, p1 {fmt(100*q[1],1)}%, p5 {fmt(100*q[5],1)}%, "
                 f"mediana {fmt(100*q[50],1)}%, p99 {fmt(100*q[99],1)}%, máximo {fmt(100*q[100],1)}%.")
    b = o['D2_bweb_pais']
    L.append(f"  País (bweb): {inteiro(b['secoes_sem_nenhuma_biometria_certo'])} de {inteiro(b['secoes_com_comparecimento'])} seções "
             f"com comparecimento sem nenhuma habilitação biométrica (certo pelo campo).")
    d3 = o['D3']
    L.append(f"D3. Régua: um desvio que mudasse o resultado move {fmt(d3['regua_pontos'])} ponto da fatia de Lula.")
    for nome in ('r>=1', 'r>=0,9', 'r>=0,5'):
        it = d3[nome]
        s = f"  {nome}: {inteiro(it['secoes_grupo'])} seções, {inteiro(it['identificam'])} identificam"
        if 'coef' in it:
            s += f"; diferença {fmt(it['coef'])} ponto (ep {fmt(it['ep'])}); placebo {fmt(it['placebo_fatia_lula_1t']['coef'])} (ep {fmt(it['placebo_fatia_lula_1t']['ep'])})"
        L.append(s)
    e = o['D4']
    L.append(f"D4. Votos a mover para mudar o resultado: {inteiro(e['mover'])} ({fmt(100*e['fracao_votos_finalistas'])}% dos votos dos finalistas).")
    for c in e['cenarios']:
        L.append(f"  k = {fmt(c['k_votos_por_urna'],0)} votos por urna: {inteiro(c['urnas_adulteradas'])} urnas ({fmt(100*c['p'],1)}%); "
                 + '; '.join(f"P(nenhuma no teste, n={n}) = {v:.1e}" for n, v in c['P_nenhuma_no_teste'].items()))
    open(caminho, 'w').write('\n'.join(L) + '\n')


if __name__ == '__main__':
    main()
