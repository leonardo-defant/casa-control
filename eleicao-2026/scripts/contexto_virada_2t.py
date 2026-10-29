#!/usr/bin/env python3
# Contexto da virada do 2º turno de 2026 contra os 2º turnos presidenciais de 1989 a 2022.
# Rodar com: python3 -I scripts/contexto_virada_2t.py [secoes2018.json.gz] [secoes2022.json.gz]
# Só biblioteca padrão. Os números oficiais estão escritos abaixo, com a fonte de cada um em comentário.
# Saídas: resultados/contexto_virada_2t.json e resultados/contexto_virada_2t.txt
#
# Fontes oficiais usadas (TSE, baixadas em 29/10/2026):
#  [CAND aaaa] https://cdn.tse.jus.br/estatistica/sead/odsele/votacao_candidato_munzona/votacao_candidato_munzona_aaaa.zip,
#              arquivo votacao_candidato_munzona_aaaa_BR.csv (cargo Presidente, soma de QT_VOTOS_NOMINAIS por candidato e turno;
#              só esse arquivo foi baixado, por leitura parcial do zip; CRC32 conferido com o diretório do zip)
#  [DET aaaa]  https://cdn.tse.jus.br/estatistica/sead/odsele/detalhe_votacao_munzona/detalhe_votacao_munzona_aaaa.zip,
#              arquivo detalhe_votacao_munzona_aaaa_BR.csv (cargo Presidente: QT_APTOS, QT_COMPARECIMENTO,
#              QT_TOTAL_VOTOS_VALIDOS, QT_VOTOS_BRANCOS, QT_VOTOS_NULOS)
#  [CAND 1989] https://cdn.tse.jus.br/estatistica/sead/odsele/votacao_candidato_uf/votacao_candidato_uf_1989.zip (soma das UFs)
#  [DET 1989]  https://cdn.tse.jus.br/estatistica/sead/odsele/detalhe_votacao_uf/detalhe_votacao_uf_1989.zip (soma das UFs)
#  [2026]      resultados/candidatos_1t_2026_totais.txt (1º turno, soma do bweb), resultados/soma_oficial_2t.json (2º turno,
#              total oficial do TSE igual à soma dos boletins), resultados/pesquisa_externa_verificada.txt item 39
#              (comparecimento, brancos e nulos do 1º turno), resultados/T15_bweb.txt (aptos)
import datetime
import gzip
import json
import os
import re
import sys

AQUI = os.path.dirname(os.path.abspath(__file__))
RAIZ = os.path.dirname(AQUI)
RES = os.path.join(RAIZ, 'resultados')
SCRATCH = '/tmp/claude-0/-home-user-casa-control/ce2a8c88-e5ad-504f-8950-6f5ee14ae721/scratchpad/dados2t'

# ----------------------------------------------------------------------------------------------------------------
# Dados oficiais por eleição.
# l = líder do 1º turno, s = 2º colocado do 1º turno. Votos nominais do candidato; válidos = QT_TOTAL_VOTOS_VALIDOS.
# ----------------------------------------------------------------------------------------------------------------
E = {}

E[1989] = dict(
    # datas: TSE não traz DT_ELEICAO no arquivo de 1989; datas de pt.wikipedia.org/wiki/Eleição_presidencial_no_Brasil_em_1989
    # (fonte secundária) e de periodicos.ufsc.br/index.php/revistacfh/article/download/23526/21184/76460
    t1='1989-11-15', t2='1989-12-17',
    l='Collor', s='Lula',
    l1=20611030, s1=11622321,          # [CAND 1989], 1º turno (pt.wikipedia traz os mesmos números)
    l2=35090206, s2=31075803,          # [CAND 1989], 2º turno (pt.wikipedia igual)
    v1=67625886, v2=66166009,          # [DET 1989] QTD_VOTOS_NOMINAIS (em 1989 não havia voto de legenda para presidente)
    c1=72290216, c2=70260701,          # [DET 1989] QTD_COMPARECIMENTO
    b1=1176367, b2=986460,             # [DET 1989] QTD_VOTOS_BRANCOS
    n1=3487963, n2=3108232,            # [DET 1989] QTD_VOTOS_NULOS
    aptos=82074718,                    # [DET 1989] QTD_APTOS (igual nos dois turnos)
    reeleicao='não (não havia reeleição; Sarney não concorria)', incumbente_no_2t=None,
    eliminados=[('Brizola', 11167665), ('Mário Covas', 7790381), ('Maluf', 5986585), ('Afif', 3272520),
                ('Ulysses Guimarães', 3204996)],  # [CAND 1989]
)
E[2002] = dict(
    t1='2002-10-06', t2='2002-10-27',  # [CAND 2002] DT_ELEICAO
    l='Lula', s='Serra',
    l1=39455233, s1=19705445,          # [CAND 2002]
    l2=52793364, s2=33370739,          # [CAND 2002]
    v1=84952512, v2=86164103,          # [DET 2002] (igual à soma dos candidatos em [CAND 2002])
    c1=94805583, c2=91664259,          # [DET 2002]
    b1=2873753, b2=1727760,            # [DET 2002]
    n1=6976685, n2=3772138,            # [DET 2002]
    aptos=115253816,                   # [DET 2002]
    reeleicao='não (FHC não concorria; Serra era o candidato do governo)', incumbente_no_2t=None,
    eliminados=[('Garotinho', 15180097), ('Ciro Gomes', 10170882), ('Zé Maria', 402236)],  # [CAND 2002]
)
E[2006] = dict(
    t1='2006-10-01', t2='2006-10-29',  # [CAND 2006]
    l='Lula', s='Alckmin',
    l1=46662365, s1=39968369,          # [CAND 2006]
    l2=58295042, s2=37543178,          # [CAND 2006]
    v1=95996733, v2=95838220,          # [DET 2006]
    c1=104820459, c2=101998221,        # [DET 2006]
    b1=2866205, b2=1351448,            # [DET 2006]
    n1=5957521, n2=4808553,            # [DET 2006] QT_VOTOS_NULOS (QT_TOTAL_VOTOS_NULOS traz 18.876 a menos nos dois turnos)
    aptos=125913235,                   # [DET 2006]
    reeleicao='sim: Lula, líder do 1º turno', incumbente_no_2t='l',
    eliminados=[('Heloísa Helena', 6575393), ('Cristovam Buarque', 2538844)],  # [CAND 2006]
)
E[2010] = dict(
    t1='2010-10-03', t2='2010-10-31',  # [CAND 2010]
    l='Dilma', s='Serra',
    l1=47651434, s1=33132283,          # [CAND 2010]
    l2=55752529, s2=43711388,          # [CAND 2010]
    v1=101590153, v2=99463917,         # [DET 2010]
    c1=111193747, c2=106606214,        # [DET 2010]
    b1=3479340, b2=2452597,            # [DET 2010]
    n1=6124254, n2=4689428,            # [DET 2010]
    aptos=135804433,                   # [DET 2010]
    reeleicao='não (Lula não concorria; Dilma era a candidata do governo)', incumbente_no_2t=None,
    eliminados=[('Marina Silva', 19636359), ('Plínio de Arruda Sampaio', 886816)],  # [CAND 2010]
)
E[2014] = dict(
    t1='2014-10-05', t2='2014-10-26',  # [CAND 2014]
    l='Dilma', s='Aécio',
    l1=43267668, s1=34897211,          # [CAND 2014]
    l2=54501118, s2=51041155,          # [CAND 2014]
    v1=104023802, v2=105542273,        # [DET 2014]
    c1=115122883, c2=112683879,        # [DET 2014]
    b1=4420489, b2=1921819,            # [DET 2014]
    n1=6678592, n2=5219787,            # [DET 2014]
    aptos=142822046,                   # [DET 2014]
    reeleicao='sim: Dilma, líder do 1º turno', incumbente_no_2t='l',
    eliminados=[('Marina Silva', 22176619), ('Luciana Genro', 1612186), ('Pastor Everaldo', 780513),
                ('Eduardo Jorge', 630099), ('Levy Fidelix', 446878)],  # [CAND 2014]
)
E[2018] = dict(
    t1='2018-10-07', t2='2018-10-28',  # [CAND 2018]
    l='Bolsonaro', s='Haddad',
    l1=49277010, s1=31342051,          # [CAND 2018] (a base local por seção dá 49.276.990 e 31.342.005; ver teste f)
    l2=57797847, s2=47040906,          # [CAND 2018]
    v1=107050749, v2=104838753,        # [DET 2018]
    c1=117364654, c2=115933451,        # [DET 2018]
    b1=3106937, b2=2486593,            # [DET 2018]
    n1=7206222, n2=8608105,            # [DET 2018]
    aptos=147306295,                   # [DET 2018] 1º turno (2º turno: 147.306.294)
    reeleicao='não (Temer não concorria; o MDB lançou Meirelles)', incumbente_no_2t=None,
    eliminados=[('Ciro Gomes', 13344371), ('Alckmin', 5096350), ('Amoêdo', 2679745), ('Cabo Daciolo', 1348323),
                ('Meirelles', 1288950), ('Marina Silva', 1069578), ('Alvaro Dias', 859601), ('Boulos', 617122)],  # [CAND 2018]
)
E[2022] = dict(
    t1='2022-10-02', t2='2022-10-30',  # [CAND 2022]
    l='Lula', s='Bolsonaro',
    l1=57259504, s1=51072345,          # [CAND 2022]
    l2=60345999, s2=58206354,          # [CAND 2022]
    v1=118229719, v2=118552353,        # [DET 2022]
    c1=123682372, c2=124252796,        # [DET 2022]
    b1=1964779, b2=1769678,            # [DET 2022]
    n1=3487874, n2=3930765,            # [DET 2022]
    aptos=156454011,                   # [DET 2022]
    reeleicao='sim: Bolsonaro, 2º colocado do 1º turno', incumbente_no_2t='s',
    eliminados=[('Simone Tebet', 4915423), ('Ciro Gomes', 3599287), ('Soraya Thronicke', 600955),
                ("Felipe d'Avila", 559708), ('Padre Kelmon', 81129)],  # [CAND 2022]
)
E[2026] = dict(
    t1='2026-10-04', t2='2026-10-25',  # tarefa e resultados/README.md
    l='Flávio', s='Lula',
    l1=56104503, s1=53879538,          # resultados/candidatos_1t_2026_totais.txt
    l2=59826041, s2=64256232,          # resultados/soma_oficial_2t.json (oficial = boletins)
    v1=119300788,                      # resultados/candidatos_1t_2026_totais.txt (válidos sem o 28)
    v2=124082273,                      # soma dos dois finalistas (soma_oficial_2t.json)
    c1=125275835, c2=128236074,        # pesquisa_externa_verificada.txt item 39; soma_oficial_2t.json
    b1=2300798, b2=1430496,            # idem
    n1=3674249, n2=2723305,            # idem (o 28, 5.246 votos, conta como nulo no 1º turno)
    aptos=158745502,                   # resultados/T15_bweb.txt
    reeleicao='sim: Lula, 2º colocado do 1º turno', incumbente_no_2t='s',
    eliminados=[('Augusto Cury', 3448569), ('Renan Santos', 2675887), ('Ronaldo Caiado', 2605148), ('Zema', 326488),
                ('Samara', 122911)],  # resultados/candidatos_1t_2026_totais.txt
)

# ----------------------------------------------------------------------------------------------------------------
# Últimas pesquisas do 2º turno (votos válidos), na ordem (líder do 1º turno, 2º colocado). None = não achada/confirmada.
# ----------------------------------------------------------------------------------------------------------------
PESQ = {
    1989: {'nota': 'não confirmada: a busca apontou registros do CESOP/Unicamp (Datafolha de 15 e 16/12/1989, Collor à frente), '
                   'mas as páginas deram 404; sem número publicado nos válidos conferido'},
    2002: {'nota': 'última pesquisa não achada; a primeira Datafolha do 2º turno (cerca de 11/10/2002) dava Lula 64 x 36 nos '
                   'válidos, só por resumo de busca de um recorte do Correio no acervo do Senado '
                   '(www2.senado.leg.br/jspui/bitstream/id/928006/1/Eleicao_presidencial_P137_R0360.pdf), não aberto'},
    2006: {'Datafolha': (61, 39, '27 e 28/10/2006', 'https://www.congressoemfoco.com.br/noticia/97223/pesquisas-apontam-vitoria-de-lula'),
           'Ibope': (61, 39, '27 e 28/10/2006', 'https://www.congressoemfoco.com.br/noticia/97223/pesquisas-apontam-vitoria-de-lula')},
    2010: {'Datafolha': (55, 45, 'divulgada 30/10/2010 (BR 37.903/2010)', 'https://www.congressoemfoco.com.br/noticia/82633/veja-ultimos-numeros-do-ibope-e-datafolha'),
           'Ibope': (56, 44, 'divulgada 30/10/2010 (BR 37.917/2010)', 'https://www.congressoemfoco.com.br/noticia/82633/veja-ultimos-numeros-do-ibope-e-datafolha')},
    2014: {'Datafolha': (52, 48, '24 e 25/10/2014', 'https://tribunademinas.com.br/?p=9520 e https://www.congressoemfoco.com.br/noticia/123322/ha-12-anos-datafolha-dava-a-aecio-e-dilma-os-indices-de-flavio-e-lula'),
           'Ibope': (53, 47, 'divulgada 25/10/2014 (a matéria escreve "24 e 25 de setembro", erro de digitação)', 'https://tribunademinas.com.br/?p=9520')},
    2018: {'Datafolha': (55, 45, '26 e 27/10/2018', 'resultados/nacionais_2018_2022_pesquisas_verificadas.txt item 6'),
           'Ibope': (54, 46, '26 e 27/10/2018', 'resultados/nacionais_2018_2022_pesquisas_verificadas.txt item 7')},
    2022: {'Datafolha': (52, 48, '28 e 29/10/2022', 'resultados/nacionais_2018_2022_pesquisas_verificadas.txt item 21'),
           'Ipec': (54, 46, '27 a 29/10/2022', 'resultados/nacionais_2018_2022_pesquisas_verificadas.txt item 22 (pelos totais 50 x 43: 53,76 para Lula, erro_pesquisas_2t.txt)')},
    2026: {'Datafolha': (51, 49, '23 e 24/10/2026', 'resultados/nacionais_2026_pesquisas_verificadas.txt item 1 (pelos totais 48 x 47: Lula 49,47, erro_pesquisas_2t.txt)'),
           'Ipsos-Ipec': None,
           'nota': 'Ipsos-Ipec sem pesquisa nacional de 2º turno em outubro (resultados/L5_pesquisas.txt); 11 de 12 institutos davam '
                   'Flávio à frente nos válidos, de 50,1 a 52 (resultados/nacionais_2026_pesquisas_verificadas.txt, linha 4)'},
}

# ----------------------------------------------------------------------------------------------------------------
# Apoios no 2º turno dos principais eliminados (texto com fonte).
# ----------------------------------------------------------------------------------------------------------------
APOIOS = {
    1989: ['Brizola (3º) e Covas (4º): Lula. "Mário Covas e ... Leonel Brizola decidiram apoiar Lula no segundo turno contra '
           'Collor" (https://www.gazetadopovo.com.br/vozes/certas-palavras/fhc-e-lula/)',
           'Maluf (5º), Afif e Ulysses: não confirmado nas fontes abertas'],
    2002: ['Garotinho (3º): Lula, depois de hesitar; Ciro (4º): Lula. "com o apoio dado por Ciro e Garotinho a Lula, Serra ficou '
           'isolado" (pt.wikipedia.org/wiki/Eleição_presidencial_no_Brasil_em_2002, fonte secundária)'],
    2006: ['Heloísa Helena (3º): PSOL não apoiou nem Lula nem Alckmin (https://www.congressoemfoco.com.br/noticia/3463/heloisa-helena-diz-que-nao-apoiara-ninguem-no-2-turno)',
           'Cristovam (4º): disse que a decisão seria do PDT; posição final não confirmada '
           '(https://www.cooperativa.cl/noticias/site/artic/20061002/pags-amp/20061002104455.html)'],
    2010: ['Marina Silva (3º): PV e Marina declararam "independência" (neutros) '
           '(https://www.congressoemfoco.com.br/noticia/76752/pv-resolve-ficar-neutro-no-segundo-turno; '
           'https://www.gazetadopovo.com.br/vida-publica/eleicoes/2010/marina-e-pv-anunciam-independencia-no-segundo-turno-1civ2wth3jylw0sfhw0zq79se/)',
           'Plínio (4º): não confirmado'],
    2014: ['Marina Silva (3º): Aécio, em 12/10 (https://www.em.com.br/app/noticia/politica/2014/10/12/interna_politica,578917/marina-silva-declara-apoio-a-aecio-neves-no-segundo-turno.shtml); '
           'PSB e PPS também (pt.wikipedia, com links do G1)',
           'Luciana Genro (4º): PSOL neutro, contra o voto em Aécio; PV e Eduardo Jorge: Aécio; Levy Fidelix: Aécio '
           '(pt.wikipedia.org/wiki/Eleição_presidencial_no_Brasil_em_2014, seção Apoios no segundo turno, links do G1); Pastor Everaldo: não confirmado'],
    2018: ['Ciro (3º): PDT deu "apoio crítico" a Haddad (https://ultimosegundo.ig.com.br/politica/2018-10-10/pdt-de-ciro-apoia-haddad.html, via pt.wikipedia)',
           'Alckmin (4º): PSDB neutro (http://agenciabrasil.ebc.com.br/politica/noticia/2018-10/psdb-decide-que-ficara-neutro-no-segundo-turno)',
           'Amoêdo (5º): Novo neutro (https://www.moneytimes.com.br/novo-e-pp-descartam-apoio-a-candidatos-ao-segundo-turno)',
           'Daciolo (Patriota) e Meirelles (MDB): partidos na lista de neutros da pt.wikipedia, sem link',
           'Marina (8º): "voto crítico" em Haddad; Boulos e PSOL: Haddad; Alvaro Dias: Podemos neutro (pt.wikipedia, links do G1, Veja e R7)'],
    2022: ['Simone Tebet (3º): Lula (https://oglobo.globo.com/politica/eleicoes-2022/noticia/2022/10/tebet-anuncia-apoio-a-lula-para-o-segundo-turno-das-eleicoes.ghtml, via pt.wikipedia; '
           'https://www.bloomberglinea.com.br/2022/10/05/simone-tebet-do-mdb-declara-apoio-a-lula-no-2-turno/)',
           'Ciro (4º): Lula, PDT por unanimidade (https://noticias.uol.com.br/eleicoes/2022/10/04/sem-citar-lula-ciro-anuncia-apoio-ao-petista-no-2-turno-ultima-saida.htm, via pt.wikipedia)',
           "Soraya (5º): nenhum dos dois; Felipe d'Avila (6º): Novo neutro (pt.wikipedia, links do Correio Braziliense e O Antagonista)"],
    2026: ['Zema, Caiado, Clariana, Cury (condicionado a 8 compromissos) e Grassi: Flávio; Renan Santos liberou os eleitores; '
           'Samara, Hertz e Edmilson: Lula (voto crítico); PCO: nulo (resultados/contexto_2t_2026_e_onde_estaria_a_fraude.txt, '
           'conferido com fontes em contexto_2t_2026_pesquisa_verificada.json)'],
}


def dias(a, b):
    return (datetime.date.fromisoformat(b) - datetime.date.fromisoformat(a)).days


def contas(y, e):
    l1, s1, l2, s2, v1, v2 = e['l1'], e['s1'], e['l2'], e['s2'], e['v1'], e['v2']
    elim = v1 - l1 - s1
    gl, gs = l2 - l1, s2 - s1
    bolo = gl + gs
    nv1, nv2 = e['c1'] - v1, e['c2'] - v2          # não válidos (branco, nulo e anulados) = comparecimento menos válidos
    r = dict(
        ano=y, dias=dias(e['t1'], e['t2']), lider_1t=e['l'], segundo_1t=e['s'],
        votos=dict(l1=l1, s1=s1, l2=l2, s2=s2, validos1=v1, validos2=v2, eliminados=elim,
                   comparecimento1=e['c1'], comparecimento2=e['c2'], brancos1=e['b1'], brancos2=e['b2'],
                   nulos1=e['n1'], nulos2=e['n2'], aptos=e['aptos']),
        pct_validos=dict(l1=100 * l1 / v1, s1=100 * s1 / v1, eliminados1=100 * elim / v1, l2=100 * l2 / v2, s2=100 * s2 / v2),
        ganho=dict(lider=gl, segundo=gs, segundo_pct_validos1=100 * gs / v1, lider_pct_validos1=100 * gl / v1,
                   segundo_sobre_eliminados=gs / elim),
        bolo=bolo,
        bolo_pct_validos1=100 * bolo / v1,
        fatia_bolo_segundo=100 * gs / bolo,
        decomposicao_bolo=dict(eliminados=elim, aumento_comparecimento=e['c2'] - e['c1'], queda_nao_validos=nv1 - nv2,
                               identidade=elim + (e['c2'] - e['c1']) + (nv1 - nv2) - bolo),
        fatia2_segundo_1t=100 * s1 / (l1 + s1), fatia2_segundo_2t=100 * s2 / (l2 + s2),
        margem1_pontos_validos=100 * (l1 - s1) / v1,
        abstencao1=100 * (e['aptos'] - e['c1']) / e['aptos'], abstencao2=100 * (e['aptos'] - e['c2']) / e['aptos'],
        reeleicao=e['reeleicao'], vencedor=e['l'] if l2 > s2 else e['s'],
    )
    r['virada2'] = r['fatia2_segundo_2t'] - r['fatia2_segundo_1t']
    # quanto a diferença entre os dois mudou a favor do 2º colocado, em votos (ganho do 2º menos ganho do líder)
    r['virada_diferenca_votos'] = gs - gl
    r['virada_diferenca_pct_validos1'] = 100 * (gs - gl) / v1
    r['margem1_pontos_fatia2'] = 100 - 2 * r['fatia2_segundo_1t']
    r['virada_necessaria'] = 50 - r['fatia2_segundo_1t']
    r['fatia_minima_bolo'] = 100 * (bolo + (l1 - s1)) / (2 * bolo)
    # pesquisas: erro na fatia do 2º colocado (urna menos pesquisa)
    pe = {}
    for inst, val in PESQ.get(y, {}).items():
        if inst == 'nota' or val is None:
            continue
        pl, ps, campo, fonte = val
        pe[inst] = dict(lider=pl, segundo=ps, campo=campo, fonte=fonte, erro_segundo=r['pct_validos']['s2'] - ps,
                        lider_da_pesquisa=e['l'] if pl > ps else (e['s'] if ps > pl else 'empate'))
    r['pesquisas'] = pe
    r['pesquisas_nota'] = PESQ.get(y, {}).get('nota')
    r['apoios'] = APOIOS[y]
    r['principais_eliminados'] = e['eliminados']
    return r


def contrafactuais(r26, anteriores):
    v = r26['votos']
    L1, F1, B = v['s1'], v['l1'], r26['bolo']
    V2 = L1 + F1 + B
    out = dict(fatia_minima_bolo=r26['fatia_minima_bolo'], virada_necessaria=r26['virada_necessaria'],
               real=dict(fatia_bolo=r26['fatia_bolo_segundo'], virada=r26['virada2'], lula_pct=r26['pct_validos']['s2']),
               mesma_fatia_do_bolo={}, mesma_virada={})
    for r in anteriores:
        s = r['fatia_bolo_segundo'] / 100
        L2 = L1 + s * B
        F2 = F1 + (1 - s) * B
        out['mesma_fatia_do_bolo'][r['ano']] = dict(fatia=100 * s, lula=round(L2), flavio=round(F2),
                                                     lula_pct=100 * L2 / V2, margem_lula=round(L2 - F2),
                                                     vencedor='Lula' if L2 > F2 else 'Flávio')
        p = r26['fatia2_segundo_1t'] + r['virada2']
        out['mesma_virada'][r['ano']] = dict(virada=r['virada2'], lula_pct=p, lula=round(p / 100 * V2),
                                             flavio=round((100 - p) / 100 * V2), margem_lula=round((2 * p - 100) / 100 * V2),
                                             vencedor='Lula' if p > 50 else 'Flávio')
    return out


def somar_secoes(path):
    with gzip.open(path, 'rt') as f:
        d = json.load(f)
    tot = {t: dict(apt=0, comp=0, L=0, R=0, O=0, B=0, N=0, secoes=0) for t in ('1', '2')}
    for v in d.values():
        for t in ('1', '2'):
            s = v.get(t)
            if not s:
                continue
            tot[t]['secoes'] += 1
            for c in ('apt', 'comp', 'L', 'R', 'O', 'B', 'N'):
                tot[t][c] += s.get(c, 0) or 0
    return tot


def teste_secoes(ano, path, e):
    if not os.path.exists(path):
        return dict(arquivo=path, erro='arquivo não encontrado')
    tot = somar_secoes(path)
    # Na base, L = candidato de esquerda (Haddad/Lula) e R = candidato de direita (Bolsonaro)
    if ano == 2018:
        of = {'1': dict(L=e['s1'], R=e['l1'], O=e['v1'] - e['l1'] - e['s1'], B=e['b1'], N=e['n1'], comp=e['c1'], apt=e['aptos']),
              '2': dict(L=e['s2'], R=e['l2'], O=0, B=e['b2'], N=e['n2'], comp=e['c2'], apt=147306294)}  # [DET 2018] aptos 2T
    else:
        of = {'1': dict(L=e['l1'], R=e['s1'], O=e['v1'] - e['l1'] - e['s1'], B=e['b1'], N=e['n1'], comp=e['c1'], apt=e['aptos']),
              '2': dict(L=e['l2'], R=e['s2'], O=0, B=e['b2'], N=e['n2'], comp=e['c2'], apt=e['aptos'])}
    out = dict(arquivo=path, secoes={t: tot[t]['secoes'] for t in tot}, turnos={})
    for t in ('1', '2'):
        out['turnos'][t] = {c: dict(base=tot[t][c], oficial=of[t][c], diferenca=tot[t][c] - of[t][c])
                            for c in ('L', 'R', 'O', 'B', 'N', 'comp', 'apt')}
        vb = tot[t]['L'] + tot[t]['R'] + tot[t]['O']
        vo = of[t]['L'] + of[t]['R'] + of[t]['O']
        out['turnos'][t]['validos'] = dict(base=vb, oficial=vo, diferenca=vb - vo)
    return out


def conferir_transferencia(resultados):
    # Confere as linhas "aaaa: +x mi de y mi" de resultados/transferencia_2022_x_2026.txt (candidato de direita)
    p = os.path.join(RES, 'transferencia_2022_x_2026.txt')
    if not os.path.exists(p):
        return None
    txt = open(p, encoding='utf-8').read()
    out = {}
    for ano, ganho, base in re.findall(r'^\s*(\d{4}): \+([\d.]+) mi de ([\d.]+) mi', txt, re.M):
        ano = int(ano)
        r = resultados[ano]
        g_dir = r['ganho']['lider'] if ano in (2018, 2026) else r['ganho']['segundo']  # direita: Bolsonaro 2018, Bolsonaro 2022, Flávio 2026
        out[ano] = dict(arquivo_ganho_mi=float(ganho), arquivo_eliminados_mi=float(base),
                        aqui_ganho_mi=round(g_dir / 1e6, 2), aqui_eliminados_mi=round(r['votos']['eliminados'] / 1e6, 2))
    return out


def br(x, nd=0):
    s = f'{x:,.{nd}f}'
    return s.replace(',', 'X').replace('.', ',').replace('X', '.')


def mi(x):
    return br(x / 1e6, 2)


def main():
    a18 = sys.argv[1] if len(sys.argv) > 1 else os.path.join(SCRATCH, 'secoes2018.json.gz')
    a22 = sys.argv[2] if len(sys.argv) > 2 else os.path.join(SCRATCH, 'secoes2022.json.gz')
    R = {y: contas(y, E[y]) for y in sorted(E)}
    ant = [R[y] for y in sorted(R) if y < 2026]
    cf = contrafactuais(R[2026], ant)
    secoes = {2018: teste_secoes(2018, a18, E[2018]), 2022: teste_secoes(2022, a22, E[2022])}
    transf = conferir_transferencia(R)

    fatias = sorted(r['fatia_bolo_segundo'] for r in ant)
    viradas = sorted(r['virada2'] for r in ant)
    resumo = dict(
        fatia_bolo_2026=R[2026]['fatia_bolo_segundo'],
        fatia_bolo_anteriores=[(r['ano'], round(r['fatia_bolo_segundo'], 2)) for r in ant],
        fatia_bolo_maior_anterior=max(fatias), fatia_bolo_mediana_anterior=fatias[len(fatias) // 2],
        virada_2026=R[2026]['virada2'], virada_anteriores=[(r['ano'], round(r['virada2'], 2)) for r in ant],
        virada_mediana_anterior=viradas[len(viradas) // 2],
        anos_em_que_a_virada_daria_vitoria_a_lula=[y for y, c in cf['mesma_virada'].items() if c['vencedor'] == 'Lula'],
        anos_em_que_a_fatia_do_bolo_daria_vitoria_a_lula=[y for y, c in cf['mesma_fatia_do_bolo'].items() if c['vencedor'] == 'Lula'],
        lider_1t_perdeu=[r['ano'] for r in R.values() if r['vencedor'] != r['lider_1t']],
    )
    saida = dict(gerado_em='29/10/2026', eleicoes=R, contrafactuais_2026=cf, teste_secoes=secoes,
                 conferencia_transferencia_2022_x_2026=transf, resumo=resumo)
    with open(os.path.join(RES, 'contexto_virada_2t.json'), 'w', encoding='utf-8') as f:
        json.dump(saida, f, ensure_ascii=False, indent=1)

    L = []
    w = L.append
    w('Contexto da virada do 2º turno de 2026: série oficial dos 2º turnos presidenciais (1989 a 2022) contra 2026.')
    w('Script: scripts/contexto_virada_2t.py (python3 -I, só biblioteca padrão). Números: resultados/contexto_virada_2t.json.')
    w('Fontes: TSE, dados abertos (votacao_candidato_munzona_aaaa_BR.csv e detalhe_votacao_munzona_aaaa_BR.csv; 1989 pelos arquivos por UF),')
    w('baixados em 29/10/2026; 2026 pelos arquivos já conferidos do repositório. A fonte de cada número está em comentário no script.')
    w('"Líder" = 1º colocado do 1º turno; "2º" = 2º colocado do 1º turno. Percentuais sobre votos válidos.')
    w('')
    w('1. Série oficial')
    w('ano  | dias | líder x 2º           | 1T líder      %     | 1T 2º         %     | 2T líder      %     | 2T 2º         %     | válidos 1T   | válidos 2T   | eliminados  %')
    for r in R.values():
        v, p = r['votos'], r['pct_validos']
        w(f"{r['ano']} | {r['dias']:4d} | {r['lider_1t'] + ' x ' + r['segundo_1t']:20s} | {br(v['l1']):>11s} {br(p['l1'], 2):>6s} | "
          f"{br(v['s1']):>11s} {br(p['s1'], 2):>6s} | {br(v['l2']):>11s} {br(p['l2'], 2):>6s} | {br(v['s2']):>11s} {br(p['s2'], 2):>6s} | "
          f"{br(v['validos1']):>12s} | {br(v['validos2']):>12s} | {br(v['eliminados']):>10s} {br(p['eliminados1'], 2):>5s}")
    w('')
    w('2. Ganhos entre os turnos, bolo e virada de dois candidatos')
    w('ano  | ganho líder | ganho 2º  | 2º em % dos válidos 1T | 2º / eliminados | bolo      | fatia do bolo do 2º | fatia 2º 1T | fatia 2º 2T | virada | margem 1T (fatia) | margem 1T (válidos) | diferença virada (votos, % válidos 1T) | vencedor')
    for r in R.values():
        g = r['ganho']
        w(f"{r['ano']} | {mi(g['lider']):>9s} mi | {mi(g['segundo']):>6s} mi | {br(g['segundo_pct_validos1'], 1):>21s}% | "
          f"{br(100 * g['segundo_sobre_eliminados'], 0):>14s}% | {mi(r['bolo']):>6s} mi | {br(r['fatia_bolo_segundo'], 1):>18s}% | "
          f"{br(r['fatia2_segundo_1t'], 2):>10s} | {br(r['fatia2_segundo_2t'], 2):>10s} | {br(r['virada2'], 2):>6s} | "
          f"{br(r['margem1_pontos_fatia2'], 2):>17s} | {br(r['margem1_pontos_validos'], 2):>19s} | "
          f"{mi(r['virada_diferenca_votos']):>8s} mi ({br(r['virada_diferenca_pct_validos1'], 2):>5s}) | {r['vencedor']}")
    w('')
    w('3. De onde vem o bolo (identidade: bolo = eliminados + aumento do comparecimento + queda dos não válidos)')
    w('ano  | bolo      | eliminados | aumento do comparecimento | queda de branco+nulo+anulados | abstenção 1T | abstenção 2T | conferência')
    for r in R.values():
        d = r['decomposicao_bolo']
        w(f"{r['ano']} | {mi(r['bolo']):>6s} mi | {mi(d['eliminados']):>7s} mi | {mi(d['aumento_comparecimento']):>22s} mi | "
          f"{mi(d['queda_nao_validos']):>26s} mi | {br(r['abstencao1'], 2):>11s}% | {br(r['abstencao2'], 2):>11s}% | {d['identidade']}")
    w('')
    w('4. Últimas pesquisas do 2º turno (válidos; erro = urna menos pesquisa na fatia do 2º colocado do 1º turno)')
    for r in R.values():
        partes = []
        for inst, q in r['pesquisas'].items():
            partes.append(f"{inst} {q['campo']}: {r['lider_1t']} {q['lider']} x {r['segundo_1t']} {q['segundo']} "
                          f"(liderava {q['lider_da_pesquisa']}; erro no 2º {br(q['erro_segundo'], 2)})")
        if r['pesquisas_nota']:
            partes.append(r['pesquisas_nota'])
        w(f"  {r['ano']}: " + '; '.join(partes))
    w('')
    w('5. Reeleição e apoios dos eliminados')
    for r in R.values():
        w(f"  {r['ano']}: reeleição: {r['reeleicao']}.")
        for a in r['apoios']:
            w(f"        {a}")
    w('')
    w('6. 2026 contra a série')
    c = cf
    w(f"  Fatia mínima do bolo que Lula precisava: {br(c['fatia_minima_bolo'], 2)}% (teve {br(c['real']['fatia_bolo'], 2)}%).")
    w(f"  Virada mínima de dois candidatos: {br(c['virada_necessaria'], 2)} ponto (teve {br(c['real']['virada'], 2)}).")
    w('  Se Lula tivesse a mesma fatia do bolo que o 2º colocado de cada ano:')
    for y, q in c['mesma_fatia_do_bolo'].items():
        w(f"    {y}: fatia {br(q['fatia'], 1)}% -> Lula {br(q['lula'])} ({br(q['lula_pct'], 2)}%), Flávio {br(q['flavio'])}; "
          f"margem de Lula {br(q['margem_lula'])}; vence {q['vencedor']}")
    w('  Se a virada de dois candidatos de Lula fosse a do 2º colocado de cada ano:')
    for y, q in c['mesma_virada'].items():
        w(f"    {y}: virada {br(q['virada'], 2)} -> Lula {br(q['lula_pct'], 2)}% ({br(q['lula'])} x {br(q['flavio'])}); "
          f"margem de Lula {br(q['margem_lula'])}; vence {q['vencedor']}")
    w(f"  Resumo: fatia do bolo de Lula {br(resumo['fatia_bolo_2026'], 2)}%, a maior da série (a maior anterior é "
      f"{br(resumo['fatia_bolo_maior_anterior'], 2)}%, 2022, Bolsonaro, também candidato à reeleição em 2º lugar); virada de "
      f"{br(resumo['virada_2026'], 2)} pontos, abaixo da mediana anterior ({br(resumo['virada_mediana_anterior'], 2)}).")
    w(f"  Com a virada de qualquer ano anterior, Lula venceria em: {resumo['anos_em_que_a_virada_daria_vitoria_a_lula']}.")
    w(f"  Com a fatia do bolo de qualquer ano anterior, Lula venceria em: {resumo['anos_em_que_a_fatia_do_bolo_daria_vitoria_a_lula']}.")
    w(f"  Líder do 1º turno que perdeu o 2º: {resumo['lider_1t_perdeu']}.")
    w('')
    w('7. Teste de sanidade: soma das seções da base local contra o oficial (L = esquerda, R = direita, O = demais)')
    for ano, t in secoes.items():
        if 'erro' in t:
            w(f"  {ano}: {t['erro']} ({t['arquivo']})")
            continue
        w(f"  {ano}: {t['arquivo']} ({t['secoes']['1']} seções no 1º turno, {t['secoes']['2']} no 2º)")
        for tt, q in t['turnos'].items():
            w('    turno ' + tt + ': ' + '; '.join(f"{k} base {br(x['base'])} oficial {br(x['oficial'])} dif {br(x['diferenca'])}"
                                                for k, x in q.items()))
    if transf:
        w('')
        w('8. Conferência com resultados/transferencia_2022_x_2026.txt (ganho do candidato de direita e votos dos eliminados)')
        for ano, q in transf.items():
            w(f"  {ano}: arquivo +{q['arquivo_ganho_mi']} mi de {q['arquivo_eliminados_mi']} mi; aqui +{q['aqui_ganho_mi']} mi de {q['aqui_eliminados_mi']} mi")
    w('')
    w('Ressalvas: o bolo mistura eleitores dos eliminados, branco e nulo, abstenção e troca entre as bases dos finalistas; a')
    w('composição muda de ano para ano (nº de candidatos, tamanho dos eliminados, comparecimento). Fatia do bolo e virada são')
    w('contas de saldo líquido, não fluxos de eleitores. São 7 eleições anteriores: a série não dá uma distribuição.')
    w('Em 2006 o 2º colocado (Alckmin) perdeu votos e a fatia do bolo dele é negativa; o contrafactual com ela só mostra o extremo.')
    w('1989 teve 32 dias entre os turnos e 35,4 mi de votos nos eliminados (52% dos válidos), outro contexto.')
    txt = '\n'.join(L) + '\n'
    for ch in (chr(0x2014), chr(0x2013)):  # travessões proibidos na saída
        assert ch not in txt, 'travessão na saída'
    with open(os.path.join(RES, 'contexto_virada_2t.txt'), 'w', encoding='utf-8') as f:
        f.write(txt)
    print(txt)


if __name__ == '__main__':
    main()
