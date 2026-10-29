"""L5 do Adendo 18 (PRE-REGISTRO-2026-10-26.md): pesquisas, que não passam pela urna.

(a) Para cada instituto com pesquisa final nos dois turnos de 2026: erro de Flávio (urna menos pesquisa, nos válidos) no 1º e no
    2º turno. Incoerência: em pelo menos 6 institutos, Flávio acima da pesquisa no 1º turno e abaixo dela no 2º, com virada média
    de 4 pontos ou mais. Coerente: sinais iguais nos dois turnos na maioria.
(b) Saldo de quem não votou num finalista no 1º turno (branco, nulo, abstenção e eleitor de eliminado que as pesquisas davam como
    "nenhum"): pela urna e pelas transferências declaradas, a fatia desse saldo que foi para Lula (conta de
    resultados/decomposicao_fluxos_2026.txt). Comparar com a divisão entre Lula e Flávio dos indecisos, brancos, nulos e "não vai
    votar" nas pesquisas finais do 2º turno, quando o instituto publicar. Incoerência: fatia de Lula pela urna acima da maior fatia
    das pesquisas em 30 pontos ou mais. Sem a divisão publicada, só descritivo.

Números das pesquisas: resultados/nacionais_2026_pesquisas_verificadas.txt e resultados/contexto_2t_2026_pesquisa_verificada.json
(conferidos), mais o que a busca de 29/10/2026 achou (fontes no próprio dado). Urna: base por seção do bweb dos dois turnos.
Coeficientes da regressão do T8 com grupos: resultados/T7_T14_bweb.json (não refeitos aqui).

Uso: python3 -I analisar_L5.py <secoes2026.json.gz> <candidatos2026_1t.json.gz> <T7_T14_bweb.json> <saida.json>
     python3 -I analisar_L5.py --texto <saida.json>   (escreve o relatório em texto)
"""
import os as _os, sys as _sys
_sys.path.insert(0, _os.path.dirname(_os.path.abspath(__file__)))
import json, sys
import numpy as np

SEMENTE = 2026
SORTEIOS = 20000

# ---------------------------------------------------------------- (a) pesquisas finais de cada turno
# (instituto, F1, L1, n1, fonte1, nota1, F2, L2, n2, fonte2, nota2); F e L nos válidos publicados (ou derivados, marcado na nota).
# n: amostra publicada; None = não publicada (usa 2.000 no erro amostral, declarado).
A = [
    ('Datafolha', 42.0, 45.0, 4006, 'https://www.em.com.br/politica/2026/10/7513948-datafolha-lula-tem-45-dos-votos-validos-e-flavio-42.html',
     'campo 2 e 3/10 (o EM diz 29/9 a 1/10)', 51.0, 49.0, 4050,
     'https://www.terra.com.br/noticias/brasil/politica/pesquisa-datafolha-flavio-tem-51-e-lula-49-dos-votos-validos-na-vespera-do-2-turno,954a528e7c927a25fd2571e523c53ea1ohmk9co0.html', 'campo 23 e 24/10'),
    ('Quaest', 45.0, 46.0, 3702, 'https://viva.com.br/politica/quaest-lula-tem-46-e-flavio-45-dos-votos-validos-no-primeiro-turno.html',
     'campo 2 e 3/10; totais (40 x 38) não fecham com os válidos', 51.0, 49.0, 3702,
     'https://exame.com/brasil/pesquisa-quaest-na-vespera-do-2o-turno-flavio-bolsonaro-tem-51-e-lula-49/', 'campo 23 e 24/10; válidos pelo modelo de eleitor provável'),
    ('AtlasIntel', 44.1, 47.0, None, 'https://www.diariodepernambuco.com.br/politica/2026/10/11725710-atlasintel-lula-tem-47-e-flavio-bolsonaro-441-de-votos-validos-no-primeiro-turno.html',
     'campo 27/9 a 2/10; a TVT traz 43,1 (os totais 43,8 de 99,4 dão 44,1)', 50.8, 49.2, 4990,
     'https://www.cartacapital.com.br/politica/atlasintel-na-vespera-do-2o-turno-flavio-bolsonaro-508-lula-492/', 'campo 18 a 23/10'),
    ('CNT/MDA', 42.1, 47.8, None, 'https://tvtnews.com.br/pesquisa-cnt-mda-na-vespera-da-eleicao-1-turno/',
     'campo 30/9 a 2/10', 50.7, 49.3, 2032,
     'https://exame.com/brasil/pesquisa-para-presidente-cnt-mda-flavio-bolsonaro-tem-507-e-lula-493-dos-votos-valdios/', 'campo 21 a 23/10'),
    ('PoderData', 43.0, 45.0, None, 'https://sbtnews.sbt.com.br/noticia/eleicoes/poder-data-aya-lula-tem-42-e-flavio-41-no-1-turno',
     'campo 30/9 a 2/10', 51.0, 49.0, 4000,
     'https://static.poder360.com.br/uploads/2026/10/Relatorio-PoderData-Eleitoral-24out26-1.pdf', 'campo 23 e 24/10 (divulgada às 11h04 de 25/10); a rodada de 19 a 21/10 também dá 51 x 49'),
    ('Nexus/BTG', 39.0, 44.0, None, 'https://moneytimes.com.br/pesquisa-btg-pactual-nexus-28-de-setembro-gaep/',
     'campo 25 a 27/9 (última rodada achada antes do 1º turno)', 50.5, 49.5, 2000,
     'https://www.bloomberglinea.com.br/brasil/pesquisas-indicam-cenario-acirrado-com-flavio-e-lula-empatados-dentro-da-margem-de-erro/', 'campo 23 e 24/10'),
    ('Real Time Big Data', 41.0, 46.0, None, 'https://www.gazetadopovo.com.br/eleicoes/2026/pesquisa-eleitoral-2026/real-time-big-data-presidente-outubro-2026-segundo-turno-2/',
     'campo 26 a 30/9; válidos da Gazeta do Povo (totais 39 x 43)', 52.0, 48.0, 2000,
     'https://www.gazetadopovo.com.br/eleicoes/2026/pesquisa-eleitoral-2026/real-time-big-data-presidente-outubro-2026-segundo-turno-2/', 'campo 19 a 22/10'),
    ('Futura', 44.8, 42.6, None, 'https://www.cartacapital.com.br/politica/pesquisa-futura-que-se-aproximou-do-resultado-no-1o-turno-mostra-empate-entre-flavio-bolsonaro-e-lula/',
     'publicada 3/10; campo e amostra não achados', 50.1, 49.9, 2000,
     'https://www.gazetadopovo.com.br/eleicoes/2026/pesquisa-eleitoral-2026/futura-inteligencia-presidente-outubro-2026-vespera-segundo-turno/', 'campo 23 e 24/10'),
    ('Gerp', 46.0, 44.0, None, 'https://www.poder360.com.br/poder-eleicoes-2026/flavio-tem-49-contra-44-de-lula-no-2o-turno-diz-gerp/',
     'campo 30/9 a 2/10', 52.0, 48.0, None,
     'https://www.cnnbrasil.com.br/eleicoes/gerp-flavio-tem-52-dos-votos-validos-no-2o-turno-lula-48-2/', 'campo 22 a 24/10'),
    ('Veritá', 47.0, 45.0, None, 'https://revistaforum.com.br/politica/verita-aproximou-resultado-1o-turno-lula/',
     'última rodada segundo a Revista Fórum, sem ficha; a rodada de 20 a 25/9 (40,5 mil) deu 45,14 x 44,65', 51.56, 48.44, None,
     'https://exame.com/brasil/pesquisa-verita-flavio-bolsonaro-tem-5156-e-lula-4844-no-2o-turno/', 'campo 19 a 23/10'),
    ('Vox Brasil', round(100 * 41.2 / (100 - 3.2 - 7.0), 2), round(100 * 40.4 / (100 - 3.2 - 7.0), 2), None,
     'https://www.cnnbrasil.com.br/eleicoes/vox-flavio-registra-482-no-2o-turno-lula-452/',
     'campo 29/9 a 1/10; válidos não publicados, derivados dos totais 41,2 x 40,4 sem branco/nulo (3,2) e indecisos (7) (desvio)', 49.4, 50.6, None,
     'https://www.terra.com.br/noticias/eleicoes/pesquisas/em-votos-validos-lula-tem-506-contra-494-de-flavio-mostra-pesquisa-vox-brasil,3ca7e3efc2f58872a88257dcc7797ce6jtw3t5vc.html', 'campo 20 a 22/10'),
]
FORA_A = {
    'Ipespe/Abrapel': 'sem pesquisa nacional de 1º turno antes de 4/10 (a série de 2º turno começa em 6 a 8/10; placardaspesquisas.com.br/institutos/ipespe e busca de 29/10)',
    'Paraná Pesquisas': 'sem pesquisa nacional de presidente em nenhum dos dois turnos (últimas nacionais de fevereiro e março)',
    'Ipsos-Ipec': 'sem pesquisa nacional de 2º turno em outubro',
}
ALTERNATIVAS_A = {'Veritá': ('F1', 45.14, 'rodada de 20 a 25/9 com ficha técnica'), 'AtlasIntel': ('F1', 43.1, 'número da TVT News')}
N_PADRAO = 2000
VALIDOS_FRAC = 0.93  # fração da amostra nos válidos, quando não publicada, para o erro amostral

# ---------------------------------------------------------------- (b) transferências declaradas
# por grupo do 1º turno: (Flávio, Lula, nenhum), nenhum = branco, nulo e não sabe. Grupos da urna: Cury, Renan, Caiado, Zema,
# esquerda (PSTU, PCB, PCO), demais (Samara, Clariana, Grassi). 'fid': fidelidade declarada dos eleitores de Flávio e de Lula,
# como (fica, vai para o adversário, nenhum). n = entrevistas; votou = fração que votou no 1º turno.
GR = ['Cury', 'Renan', 'Caiado', 'Zema', 'esquerda', 'demais']
NUM = {'Cury': ['70'], 'Renan': ['14'], 'Caiado': ['55'], 'Zema': ['30'], 'esquerda': ['16', '21', '29'], 'demais': ['80', '27', '35']}


def tr(f, l):
    return (f, l, round(1 - f - l, 4))


TRANSF = {
    'PoderData 23-24/10 (final)': dict(final=True, n=4000, votou=0.89, url='https://static.poder360.com.br/uploads/2026/10/Relatorio-PoderData-Eleitoral-24out26-1.pdf',
        g={'Cury': tr(.58, .29), 'Renan': tr(.43, .33), 'Caiado': tr(.46, .30), 'Zema': tr(.65, .15), 'esquerda': tr(.65, .15), 'demais': tr(.65, .15)},
        fid={'F': (.94, .05, .01), 'L': (.94, .05, .01)}, nota='Zema, esquerda e demais pela coluna "Outro candidato"'),
    'PoderData 19-21/10': dict(final=False, n=4000, votou=0.90, url='https://static.poder360.com.br/uploads/2026/10/Relatorio-PoderData-Eleitoral-21out26-2.pdf',
        g={'Cury': tr(.42, .48), 'Renan': tr(.49, .34), 'Caiado': tr(.49, .30), 'Zema': tr(.70, .20), 'esquerda': tr(.70, .20), 'demais': tr(.70, .20)},
        fid={'F': (.96, .03, .01), 'L': (.95, .04, .01)}, nota='"Outro candidato" para Zema, esquerda e demais'),
    'PoderData 5-7/10': dict(final=False, n=3000, votou=0.89, url='https://static.poder360.com.br/uploads/2026/10/Relatorio-PoderData-Eleitoral-8out26-final.pdf',
        g={'Cury': tr(.56, .27), 'Renan': tr(.48, .25), 'Caiado': tr(.57, .19), 'Zema': tr(.72, .10), 'esquerda': tr(.19, .39), 'demais': tr(.19, .39)},
        fid={'F': (.94, .05, .01), 'L': (.92, .05, .03)}, nota='"Outro" para esquerda e demais'),
    'Quaest 17-20/10': dict(final=False, n=2154, votou=0.90, url='https://exame.com/brasil/para-onde-vao-os-votos-de-cury-caiado-e-renan-no-2o-turno-pesquisa-quaest-responde/',
        g={'Cury': tr(.33, .48), 'Renan': tr(.51, .25), 'Caiado': tr(.57, .21)}, fid=None, nota='Zema, esquerda e demais não publicados (mediana dos outros institutos); fidelidade não publicada (100%)'),
    'Quaest 10-13/10': dict(final=False, n=2154, votou=0.90, url='https://www.opovo.com.br/noticias/politica/eleicoes/2026/10/16/quaest-traz-transferencia-de-voto-no-2-turno-a-flavio-e-lula.html',
        g={'Cury': tr(.30, .34), 'Renan': tr(.40, .14), 'Caiado': tr(.42, .23), 'Zema': tr(.38, .33), 'esquerda': tr(.38, .33), 'demais': tr(.38, .33)},
        fid=None, nota='"Outros" para Zema, esquerda e demais; fidelidade não publicada (100%)'),
    'AtlasIntel 13-18/10': dict(final=False, n=4998, votou=0.90, url='https://www.infomoney.com.br/politica/atlasintel-para-onde-foram-os-votos-de-caiado-renan-zema-e-cury-no-2o-turno/',
        g={'Cury': tr(.424, .521), 'Renan': tr(.335, .319), 'Caiado': tr(.698, .245), 'Zema': tr(.613, .307), 'esquerda': tr(.613, .307), 'demais': tr(.613, .307)},
        fid=None, nota='"Outros (inclui Zema)" para Zema, esquerda e demais; fidelidade não publicada (100%)'),
    'AtlasIntel 3-8/10': dict(final=False, n=5026, votou=0.90, url='https://tvtnews.com.br/?p=805894',
        g={'Cury': tr(.389, .504), 'Renan': tr(.403, .281), 'Caiado': tr(.549, .269), 'Zema': tr(.834, .148), 'esquerda': tr(.834, .148), 'demais': tr(.834, .148)},
        fid=None, nota='"Demais candidatos" para Zema, esquerda e demais; fidelidade não publicada (100%)'),
    'Ipespe 13-15/10': dict(final=False, n=1500, votou=0.93, url='https://static.poder360.com.br/uploads/2026/10/pesquisa-ipespe-17out2026.pdf',
        g={'Cury': tr(.50, .31), 'Renan': tr(.40, .20), 'Caiado': tr(.59, .18), 'Zema': tr(.55, .27), 'esquerda': tr(.55, .27), 'demais': tr(.55, .27)},
        fid={'F': (.97, .02, .01), 'L': (.96, .01, .03)}, nota='"Outros" para Zema, esquerda e demais'),
    'Ipespe 6-8/10': dict(final=False, n=1500, votou=0.92, url='https://static.poder360.com.br/uploads/2026/10/pesquisa-ipespe-abrapel-10out2026.pdf',
        g={'Cury': tr(.50, .29), 'Renan': tr(.36, .20), 'Caiado': tr(.56, .15), 'Zema': tr(.40, .40), 'esquerda': tr(.40, .40), 'demais': tr(.40, .40)},
        fid={'F': (.97, .01, .02), 'L': (.97, .01, .02)}, nota='"Outros" para Zema, esquerda e demais'),
    'Datafolha 13-14/10': dict(final=False, n=2520, votou=0.93, url='https://static.poder360.com.br/uploads/2026/10/datafolha-15out2026-pesquisa-nacional.pdf',
        g={k: tr(.46, .27) for k in ['Cury', 'Renan', 'Caiado', 'Zema']}, fid=None,
        nota='só o agregado dos quatro; esquerda e demais pela mediana dos outros institutos; fidelidade não publicada (100%)'),
    'Datafolha 6-7/10': dict(final=False, n=2520, votou=0.93, url='https://www.diariodepernambuco.com.br/politica/2026/10/11726210-datafolha-46-dos-eleitores-de-candidatos-derrotados-no-1-turno-migram-para-flavio-bolsonaro.html',
        g={k: tr(.46, .32) for k in ['Cury', 'Renan', 'Caiado', 'Zema']}, fid=None,
        nota='só o agregado dos quatro (os percentuais publicados somam 94; o resto vai para nenhum); esquerda e demais pela mediana'),
    'Nexus 10-12/10': dict(final=False, n=2002, votou=0.90, url='https://tribunadejundiai.com.br/politica/eleicoes-2026/pesquisa-btg-nexus-flavio-bolsonaro-lula-segundo-turno/',
        g={'Zema': tr(.80, .12), 'Caiado': tr(.55, .27), 'Cury': tr(.45, .32), 'Renan': tr(.45, .32), 'esquerda': tr(.45, .32), 'demais': tr(.45, .32)},
        fid=None, nota='Cury, Renan, esquerda e demais pelo agregado "outros candidatos"; fidelidade de 98% sem divisão do resto (100%)'),
}
# número original de decomposicao_fluxos_2026.txt (taxas atribuídas à Quaest que a verificação não confirmou): totais impressos
DECOMP_ORIGINAL = {'F_dos_outros': 3.59e6, 'L_dos_outros': 2.53e6, 'nenhum_dos_outros': 3.20e6}

# divisão entre Lula e Flávio, nas pesquisas, de quem não escolheu finalista no 1º turno (o análogo publicado; desvio declarado).
# (pesquisa, grupo, Lula, Flávio, n aproximado do grupo, final?, url)
ANALOGO = [
    ('PoderData 23-24/10', 'votou branco/nulo no 1º turno', 50, 26, 170, True, 'https://static.poder360.com.br/uploads/2026/10/Relatorio-PoderData-Eleitoral-24out26-1.pdf'),
    ('PoderData 23-24/10', 'não votou no 1º turno', 50, 35, 440, True, 'https://static.poder360.com.br/uploads/2026/10/Relatorio-PoderData-Eleitoral-24out26-1.pdf'),
    ('Nexus 23-24/10', 'não compareceu no 1º turno (só a Bloomberg Línea)', 53.2, 46.8, 200, True,
     'https://www.bloomberglinea.com.br/brasil/pesquisas-indicam-cenario-acirrado-com-flavio-e-lula-empatados-dentro-da-margem-de-erro/'),
    ('Datafolha 23-24/10', 'propensão média ou baixa de comparecer (24% da amostra)', 52, 48, 970, True,
     'https://www.bloomberglinea.com.br/brasil/pesquisas-indicam-cenario-acirrado-com-flavio-e-lula-empatados-dentro-da-margem-de-erro/'),
    ('PoderData 19-21/10', 'votou branco/nulo no 1º turno', 46, 23, 170, False, 'https://static.poder360.com.br/uploads/2026/10/Relatorio-PoderData-Eleitoral-21out26-2.pdf'),
    ('PoderData 19-21/10', 'não votou no 1º turno', 48, 39, 400, False, 'https://static.poder360.com.br/uploads/2026/10/Relatorio-PoderData-Eleitoral-21out26-2.pdf'),
    ('Quaest 17-20/10', 'não votou ou votou branco/nulo no 1º turno', 40, 36, 300, False, 'https://bpmoney.com.br/politica/quaest-votos-caiado-renan-cury-segundo-turno/'),
    ('AtlasIntel 13-18/10', 'não compareceu no 1º turno', 55.7, 40.2, 500, False, 'https://www.infomoney.com.br/politica/atlasintel-para-onde-foram-os-votos-de-caiado-renan-zema-e-cury-no-2o-turno/'),
    ('AtlasIntel 13-18/10', 'votou branco/nulo no 1º turno', 21.1, 38.7, 250, False, 'https://www.infomoney.com.br/politica/atlasintel-para-onde-foram-os-votos-de-caiado-renan-zema-e-cury-no-2o-turno/'),
    ('Ipespe 13-15/10', 'branco/nulo ou não votou no 1º turno', 60, 15, 75, False, 'https://static.poder360.com.br/uploads/2026/10/pesquisa-ipespe-17out2026.pdf'),
    ('Ipespe 6-8/10', 'branco/nulo ou não votou no 1º turno', 17, 30, 90, False, 'https://static.poder360.com.br/uploads/2026/10/pesquisa-ipespe-abrapel-10out2026.pdf'),
    ('AtlasIntel 3-8/10', 'não votou no 1º turno', 63.1, 21.8, 500, False, 'https://tvtnews.com.br/?p=805894'),
    ('AtlasIntel 3-8/10', 'votou branco/nulo no 1º turno', 22.5, 46.2, 250, False, 'https://tvtnews.com.br/?p=805894'),
    ('PoderData 5-7/10', 'votou branco/nulo no 1º turno', 18, 22, 130, False, 'https://static.poder360.com.br/uploads/2026/10/Relatorio-PoderData-Eleitoral-8out26-final.pdf'),
    ('PoderData 5-7/10', 'não votou no 1º turno', 34, 42, 330, False, 'https://static.poder360.com.br/uploads/2026/10/Relatorio-PoderData-Eleitoral-8out26-final.pdf'),
    ('Quaest 10-13/10', 'ausente ou branco/nulo no 1º turno', 43, 38, 300, False, 'https://www.opovo.com.br/noticias/politica/eleicoes/2026/10/16/quaest-traz-transferencia-de-voto-no-2-turno-a-flavio-e-lula.html'),
]

# intenção de comparecimento e eleitor provável nas pesquisas finais (descritivo)
COMPARECIMENTO = [
    ('PoderData 23-24/10', 'com certeza vai votar 94%, pode ir sem certeza 3%, não vai 2%, não sabe 1%; com certeza entre quem vota em Flávio 96%, em Lula 94%, '
     'branco/nulo 52%, não sabe 56%; entre quem votou no 1º turno 97% (não vai 1%), entre quem não votou 65% (pode ir 19%, não vai 15%)',
     'https://static.poder360.com.br/uploads/2026/10/Relatorio-PoderData-Eleitoral-24out26-1.pdf'),
    ('Datafolha 23-24/10', 'alta propensão de comparecer (76% da amostra): Flávio 52 x Lula 48 nos válidos; média ou baixa (24%): Lula 52 x Flávio 48; amostra inteira 51 x 49',
     'https://www.bloomberglinea.com.br/brasil/pesquisas-indicam-cenario-acirrado-com-flavio-e-lula-empatados-dentro-da-margem-de-erro/'),
    ('Nexus 23-24/10', 'modelo de eleitor provável (tira os 21% menos propensos): Flávio 52,4 x Lula 47,6; amostra inteira 50,5 x 49,5; quem votou no 1º turno 51,2 x 48,8, quem não votou Lula 53,2 x 46,8',
     'https://www.bloomberglinea.com.br/brasil/pesquisas-indicam-cenario-acirrado-com-flavio-e-lula-empatados-dentro-da-margem-de-erro/'),
    ('Quaest 23-24/10', 'válidos 51 x 49 pelo modelo de eleitor provável; totais 46 x 45 com 8% de branco, nulo e "não vai votar" e 1% de indecisos (50,5 x 49,5 sem o modelo)',
     'https://exame.com/brasil/pesquisa-quaest-na-vespera-do-2o-turno-flavio-bolsonaro-tem-51-e-lula-49/'),
    ('CNT/MDA 21-23/10', 'ajuste pelos que declararam comparecimento, sem número publicado; 7,3% ainda podem mudar; ponderação pelo voto declarado no 1º turno',
     'https://www.oliberal.com/politica/cnt-mda-flavio-tem-50-7-dos-votos-validos-e-lula-49-3-mulheres-s-o-maioria-entre-indecisos-1.1186349'),
]
# divisão dos indecisos, brancos, nulos e "não vai votar" do próprio 2º turno: o que cada pesquisa final publicou
DIVISAO_LITERAL = {
    'Datafolha 23-24/10': 'não publicada (branco/nulo 3, indecisos 2)',
    'Quaest 23-24/10': 'não publicada (branco, nulo e não vai votar 8, indecisos 1; 92% dos que escolheram dizem que o voto é definitivo)',
    'AtlasIntel 18-23/10': 'não publicada (indecisos, brancos e nulos 1,7 somados)',
    'CNT/MDA 21-23/10': 'não publicada (branco/nulo 5,8, indecisos 2,9; só o perfil por sexo)',
    'PoderData 23-24/10': 'não publicada (branco/nulo 3, não sabe 1; 28% do branco/nulo diz que ainda pode mudar, sem dizer para quem)',
    'Nexus 23-24/10': 'não publicada',
    'Ipespe 20-22/10': 'não publicada (branco/nulo 3, não sabem 2)',
    'Real Time Big Data 19-22/10': 'não publicada (branco/nulo 5, não sabe 1)',
    'Veritá 19-23/10': 'não publicada (branco/nulo 1,43, não sabe 2,67)',
    'Vox Brasil 20-22/10': 'não publicada (branco, nulo e nenhum 6, indecisos 4,3)',
    'Futura 23-24/10': 'não publicada (só a espontânea: ninguém/branco/nulo 2,3, não sabe 3,7)',
    'Gerp 22-24/10': 'não publicada (espontânea: não sabe 8)',
}


def carregar_urna(secoes, cand):
    from lib import carregar
    d = carregar(secoes)
    c = carregar(cand)['secoes']
    t = {k: 0 for k in ['apt1', 'comp1', 'L1', 'F1', 'O1', 'B1', 'N1', 'apt2', 'comp2', 'L2', 'F2', 'B2', 'N2']}
    g = {k: 0 for k in GR}; n28 = 0; nsec = 0
    for k, v in d.items():
        if '1' not in v or '2' not in v:
            continue
        a, b = v['1'], v['2']; nsec += 1
        t['apt1'] += a['apt']; t['comp1'] += a['comp']; t['L1'] += a['L']; t['F1'] += a['R']; t['O1'] += a['O']
        t['B1'] += a['B']; t['N1'] += a['N']
        t['apt2'] += b['apt']; t['comp2'] += b['comp']; t['L2'] += b['L']; t['F2'] += b['R']; t['B2'] += b['B']; t['N2'] += b['N']
        cv = c.get(k, {})
        for nm in GR:
            g[nm] += sum(cv.get(x, 0) for x in NUM[nm])
        n28 += cv.get('28', 0)
    del d, c
    t['secoes'] = nsec; t['grupos'] = g; t['voto_28_como_nulo'] = n28
    return t


def parte_a(u):
    v1 = u['F1'] + u['L1'] + sum(u['grupos'].values())
    F1r = 100 * u['F1'] / v1; L1r = 100 * u['L1'] / v1
    F2r = 100 * u['F2'] / (u['F2'] + u['L2']); L2r = 100 - F2r
    out = {'real': {'F1': F1r, 'L1': L1r, 'outros1': 100 - F1r - L1r, 'F2': F2r, 'L2': L2r, 'validos1': v1, 'validos2': u['F2'] + u['L2']},
           'institutos': [], 'fora': FORA_A}

    def se(p, n):
        nv = (n or N_PADRAO) * VALIDOS_FRAC
        return 100 * np.sqrt((p / 100) * (1 - p / 100) / nv)

    for nome, f1, l1, n1, u1, nt1, f2, l2, n2, u2, nt2 in A:
        e1 = F1r - f1; e2 = F2r - f2; s1 = se(f1, n1); s2 = se(f2, n2)
        out['institutos'].append({
            'instituto': nome, 'F1_pesquisa': f1, 'L1_pesquisa': l1, 'outros1_pesquisa': round(100 - f1 - l1, 2), 'n1': n1, 'fonte1': u1, 'nota1': nt1,
            'F2_pesquisa': f2, 'L2_pesquisa': l2, 'n2': n2, 'fonte2': u2, 'nota2': nt2,
            'erro_F1': e1, 'ep_F1': s1, 'erro_F2': e2, 'ep_F2': s2, 'virada': e2 - e1, 'ep_virada': float(np.hypot(s1, s2)),
            'erro_L1': L1r - l1, 'erro_L2': L2r - l2, 'erro_outros1': (100 - F1r - L1r) - (100 - f1 - l1),
            'padrao_acima_1T_abaixo_2T': bool(e1 > 0 and e2 < 0), 'mesmo_sinal': bool(np.sign(e1) == np.sign(e2)),
            'padrao_a_2ep': bool(e1 > 2 * s1 and e2 < -2 * s2)})
    I = out['institutos']; k = len(I)
    vir = np.array([x['virada'] for x in I]); sev = np.array([x['ep_virada'] for x in I])
    padrao = [x for x in I if x['padrao_acima_1T_abaixo_2T']]
    vp = np.array([x['virada'] for x in padrao]) if padrao else np.array([np.nan])
    out['resumo'] = {
        'institutos': k, 'com_padrao': len(padrao), 'com_padrao_a_2ep': sum(x['padrao_a_2ep'] for x in I),
        'mesmo_sinal': sum(x['mesmo_sinal'] for x in I),
        'virada_media_todos': float(vir.mean()), 'ep_amostral_media': float(np.sqrt((sev ** 2).sum()) / k),
        'ep_entre_institutos': float(vir.std(ddof=1) / np.sqrt(k)), 'dp_viradas': float(vir.std(ddof=1)),
        'virada_media_com_padrao': float(vp.mean()), 'mediana_virada': float(np.median(vir)),
        'erro_F1_medio': float(np.mean([x['erro_F1'] for x in I])), 'erro_F2_medio': float(np.mean([x['erro_F2'] for x in I])),
        'erro_L1_medio': float(np.mean([x['erro_L1'] for x in I])), 'erro_L2_medio': float(np.mean([x['erro_L2'] for x in I])),
        'erro_outros1_medio': float(np.mean([x['erro_outros1'] for x in I])),
    }
    r = out['resumo']
    if r['com_padrao'] >= 6 and abs(r['virada_media_com_padrao']) >= 4:
        ver = 'INCOERÊNCIA'
    elif r['mesmo_sinal'] > k / 2:
        ver = 'COERENTE'
    else:
        ver = 'INCONCLUSIVO'
    out['veredito'] = ver
    # sensibilidade: alternativas do 1º turno
    alt = {}
    for nome, (campo, val, nota) in ALTERNATIVAS_A.items():
        x = next(y for y in I if y['instituto'] == nome)
        e1 = F1r - val
        alt[nome] = {'F1': val, 'nota': nota, 'erro_F1': e1, 'virada': x['erro_F2'] - e1, 'padrao': bool(e1 > 0 and x['erro_F2'] < 0)}
    vir_alt = [alt[x['instituto']]['virada'] if x['instituto'] in alt else x['virada'] for x in I]
    out['sensibilidade'] = {'alternativas': alt, 'virada_media_com_alternativas': float(np.mean(vir_alt)),
                            'com_padrao_com_alternativas': sum((alt[x['instituto']]['padrao'] if x['instituto'] in alt else x['padrao_acima_1T_abaixo_2T']) for x in I)}
    # decomposição da virada: parte que vem do 1º turno (Flávio contra os eliminados) e parte do 2º turno
    out['decomposicao_virada'] = {'media_erro_F1': r['erro_F1_medio'], 'media_erro_F2': r['erro_F2_medio'],
                                  'parte_do_1T_ligada_aos_eliminados': -r['erro_outros1_medio'], 'parte_do_1T_ligada_a_Lula': -r['erro_L1_medio']}
    return out


def mediana_grupo(g):
    vals = [v['g'][g] for k, v in TRANSF.items() if g in v['g'] and not k.startswith('Datafolha')]
    return tuple(float(np.median([x[i] for x in vals])) for i in range(3))


def fatia_saldo(u, taxas, fid):
    """Conta de decomposicao_fluxos_2026.txt: ganho real de cada finalista menos o que as pesquisas dizem que veio dos eliminados
    (e, com fid, da troca entre os finalistas); o que sobra veio do saldo (branco, nulo, abstenção e o 'nenhum' dos eliminados)."""
    gL = u['L2'] - u['L1']; gF = u['F2'] - u['F1']
    eF = sum(taxas[g][0] * u['grupos'][g] for g in GR); eL = sum(taxas[g][1] * u['grupos'][g] for g in GR)
    eN = sum(taxas[g][2] * u['grupos'][g] for g in GR)
    rL = gL - eL; rF = gF - eF; extra = 0.0
    if fid is not None:
        # Lula perde para Flávio e para nenhum uma parte dos próprios, ganha uma parte dos de Flávio; idem Flávio
        fF, fFL, fFN = fid['F']; lL, lLF, lLN = fid['L']
        rL += u['L1'] * (lLF + lLN) - u['F1'] * fFL
        rF += u['F1'] * (fFL + fFN) - u['L1'] * lLF
        extra = u['F1'] * fFN + u['L1'] * lLN
    saldo = rL + rF
    return {'do_saldo_L': rL, 'do_saldo_F': rF, 'saldo': saldo, 'fatia_L': rL / saldo, 'dos_eliminados_F': eF, 'dos_eliminados_L': eL,
            'nenhum_dos_eliminados': eN, 'finalistas_para_nenhum': extra}


def sorteio(u, chave, rng, deff):
    """Erro da fatia pela incerteza amostral das subamostras da pesquisa (multinomial; deff divide o n)."""
    p = TRANSF[chave]; comp1 = u['comp1']; nv = p['n'] * p['votou'] / deff
    tam = {g: max(5, int(round(nv * u['grupos'][g] / comp1))) for g in GR}
    # grupos que dividem a mesma coluna da pesquisa usam a mesma subamostra
    colunas = {}
    for g in GR:
        colunas.setdefault(p['g'].get(g, ('med',) + tuple(mediana_grupo(g))), []).append(g)
    nF = nv * u['F1'] / comp1; nL = nv * u['L1'] / comp1
    res = []; res100 = []
    for _ in range(SORTEIOS):
        taxas = {}
        for col, gs in colunas.items():
            pr = np.array(col[-3:], float); pr = np.clip(pr, 0, None); pr = pr / pr.sum()
            m = sum(tam[g] for g in gs)
            q = rng.multinomial(m, pr) / m
            for g in gs:
                taxas[g] = tuple(q)
        fid = None
        if p['fid'] is not None:
            fid = {}
            for lado, nn in (('F', nF), ('L', nL)):
                pr = np.array(p['fid'][lado], float); pr = pr / pr.sum()
                fid[lado] = tuple(rng.multinomial(int(round(nn)), pr) / int(round(nn)))
        res.append(fatia_saldo(u, taxas, fid)['fatia_L'])
        res100.append(fatia_saldo(u, taxas, None)['fatia_L'])
    out = {'deff': deff, 'tamanhos_subamostra': tam}
    for nome, r in (('fid_100', np.array(res100)), ('fid_declarada', np.array(res))):
        out[nome] = {'ep': float(r.std(ddof=1)), 'p2_5': float(np.percentile(r, 2.5)), 'p97_5': float(np.percentile(r, 97.5))}
    return out


def parte_b(u, t714):
    out = {'urna': {}, 'por_pesquisa': {}, 'analogo': [], 'divisao_literal': DIVISAO_LITERAL, 'comparecimento': COMPARECIMENTO}
    gL = u['L2'] - u['L1']; gF = u['F2'] - u['F1']
    bn1 = u['B1'] + u['N1'] + u['voto_28_como_nulo']; bn2 = u['B2'] + u['N2']
    elim = sum(u['grupos'].values())
    out['urna'] = {'ganho_L': gL, 'ganho_F': gF, 'eliminados_1T': elim, 'grupos': u['grupos'], 'branco_nulo_1T_com_28': bn1, 'branco_nulo_2T': bn2,
                   'queda_branco_nulo': bn1 - bn2, 'aumento_comparecimento': u['comp2'] - u['comp1'],
                   'abstencao_1T_pct': 100 * (1 - u['comp1'] / u['apt1']), 'abstencao_2T_pct': 100 * (1 - u['comp2'] / u['apt2']),
                   'identidade_ganhos': gL + gF - (elim + (bn1 - bn2) + (u['comp2'] - u['comp1']))}
    # conferência com o arquivo antigo (totais impressos)
    s_ant = gL + gF - DECOMP_ORIGINAL['F_dos_outros'] - DECOMP_ORIGINAL['L_dos_outros']
    out['conferencia_decomposicao_antiga'] = {'fatia_L': (gL - DECOMP_ORIGINAL['L_dos_outros']) / s_ant, 'saldo': s_ant,
                                              'registrado': 0.98, 'nota': 'taxas atribuídas à Quaest que a verificação não confirmou'}
    rng = np.random.default_rng(SEMENTE)
    for chave, p in TRANSF.items():
        taxas = {g: p['g'].get(g, mediana_grupo(g)) for g in GR}
        r100 = fatia_saldo(u, taxas, None)
        rfid = fatia_saldo(u, taxas, p['fid']) if p['fid'] is not None else None
        item = {'final': p['final'], 'url': p['url'], 'nota': p['nota'], 'taxas': taxas, 'fid': p['fid'], 'fidelidade_100': r100, 'fidelidade_declarada': rfid}
        if p['final']:
            item['erro_amostral'] = [sorteio(u, chave, rng, 1.0), sorteio(u, chave, rng, 2.0)]
        out['por_pesquisa'][chave] = item
    # a mesma conta com a mediana dos institutos por grupo (não final, descritivo)
    tmed = {g: mediana_grupo(g) for g in GR}
    out['mediana_institutos'] = {'taxas': tmed, 'fidelidade_100': fatia_saldo(u, tmed, None)}
    # análogo publicado
    for nome, grupo, l, f, n, fin, url in ANALOGO:
        s = l / (l + f); n_esc = n * (l + f) / 100
        out['analogo'].append({'pesquisa': nome, 'grupo': grupo, 'L': l, 'F': f, 'fatia_L': s, 'ep': float(np.sqrt(s * (1 - s) / n_esc)),
                               'n_aprox': n, 'final': fin, 'url': url})
    fin = [x for x in out['analogo'] if x['final']]
    out['maior_fatia_final'] = max(fin, key=lambda x: x['fatia_L'])
    out['maior_fatia_qualquer_rodada'] = max(out['analogo'], key=lambda x: x['fatia_L'])
    # só urna: regressão do T8 com grupos (T7_T14_bweb.json), fatia de Lula na queda do branco+nulo e no aumento do comparecimento
    c = t714['2026']['T14_com_grupos']['coef']; e = t714['2026']['T14_com_grupos']['ep']
    qb = u['B1'] + u['N1'] - bn2; dc = u['comp2'] - u['comp1']
    s = (c['queda_branco_nulo'] * qb + c['var_comparecimento'] * dc) / (qb + dc)
    ep = np.hypot(e['queda_branco_nulo'] * qb, e['var_comparecimento'] * dc) / (qb + dc)
    elim_L = t714['2026']['T37']['urna']
    out['so_urna_regressao'] = {'coef_L_queda_branco_nulo': [c['queda_branco_nulo'], e['queda_branco_nulo']],
                                'coef_L_var_comparecimento': [c['var_comparecimento'], e['var_comparecimento']],
                                'fatia_L_branco_nulo_e_abstencao': float(s), 'ep_sem_covariancia': float(ep),
                                'b_L_eliminados_somado': elim_L.get('b_L_somado'),
                                'coef_L_votos_Flavio_1T': [c['adversario_1T'], e['adversario_1T']], 'coef_L_proprios_1T': [c['proprio_1T'], e['proprio_1T']],
                                'nota': 'a urna não identifica o "nenhum" dos eleitores dos eliminados (b_L + b_F = 1, Adendo 17)'}
    # quanto do excesso da fatia equivale ao erro do 2º turno: se o saldo tivesse se dividido como a maior fatia final
    pf = out['por_pesquisa']['PoderData 23-24/10 (final)']['fidelidade_declarada']
    m = out['maior_fatia_final']['fatia_L']
    L_sim = u['L2'] - pf['do_saldo_L'] + m * pf['saldo']; F_sim = u['F2'] - pf['do_saldo_F'] + (1 - m) * pf['saldo']
    out['equivalencia_com_erro_2T'] = {'L_validos_se_saldo_como_pesquisa': 100 * L_sim / (L_sim + F_sim),
                                       'L_validos_urna': 100 * u['L2'] / (u['L2'] + u['F2']), 'L_validos_PoderData_final': 49.0,
                                       'votos_de_diferenca_na_margem': (u['L2'] - u['F2']) - (L_sim - F_sim),
                                       'ganho_esperado_L': L_sim - u['L1'], 'ganho_esperado_F': F_sim - u['F1'],
                                       'ganho_real_L': u['L2'] - u['L1'], 'ganho_real_F': u['F2'] - u['F1']}
    out['eliminados_F_passa_ganho_real_F'] = sorted(k for k, v in out['por_pesquisa'].items() if v['fidelidade_100']['dos_eliminados_F'] > gF)
    out['eliminados_F_nao_passa'] = sorted(k for k, v in out['por_pesquisa'].items() if v['fidelidade_100']['dos_eliminados_F'] <= gF)
    # veredito pela letra
    out['veredito'] = 'DESCRITIVO'
    prim = out['por_pesquisa']['PoderData 23-24/10 (final)']
    lim_f = out['maior_fatia_final']['fatia_L'] + 0.30; lim_q = out['maior_fatia_qualquer_rodada']['fatia_L'] + 0.30
    out['leitura_analogo'] = {
        'fatia_urna_PoderData_final_fid100': prim['fidelidade_100']['fatia_L'],
        'fatia_urna_PoderData_final_fid_declarada': prim['fidelidade_declarada']['fatia_L'],
        'limite_maior_final_mais_30': lim_f, 'limite_maior_qualquer_mais_30': lim_q,
        'passa_limite_final': bool(prim['fidelidade_100']['fatia_L'] >= lim_f and prim['fidelidade_declarada']['fatia_L'] >= lim_f),
        'passa_limite_qualquer_rodada': bool(prim['fidelidade_100']['fatia_L'] >= lim_q and prim['fidelidade_declarada']['fatia_L'] >= lim_q),
        'pesquisas_com_fatia_acima_do_limite_final': sorted(k for k, v in out['por_pesquisa'].items()
                                                             if min(v['fidelidade_100']['fatia_L'], (v['fidelidade_declarada'] or v['fidelidade_100'])['fatia_L']) >= lim_f),
        'so_urna_menos_maior_final_pontos': 100 * (out['so_urna_regressao']['fatia_L_branco_nulo_e_abstencao'] - out['maior_fatia_final']['fatia_L']),
    }
    # distância ao limite em erros-padrão (erro da fatia pela urna, das subamostras, e da fatia da pesquisa)
    epp = out['maior_fatia_final']['ep']; z = {}
    for e in prim['erro_amostral']:
        for nome, chave in (('fid_100', 'fidelidade_100'), ('fid_declarada', 'fidelidade_declarada')):
            z[f'{nome}_deff{int(e["deff"])}'] = (prim[chave]['fatia_L'] - lim_f) / float(np.hypot(e[nome]['ep'], epp))
    out['leitura_analogo']['z_acima_do_limite_final'] = z
    return out


def rodar(argv):
    secoes, cand, t714p, saida = argv
    u = carregar_urna(secoes, cand)
    t714 = json.load(open(t714p))
    res = {'teste': 'L5 (Adendo 18)', 'semente': SEMENTE, 'sorteios': SORTEIOS, 'urna_totais': {k: v for k, v in u.items()},
           'a': parte_a(u), 'b': parte_b(u, t714)}
    json.dump(res, open(saida, 'w'), ensure_ascii=False, indent=1)
    print(json.dumps({'a': res['a']['veredito'], 'a_resumo': res['a']['resumo'], 'b': res['b']['veredito'], 'b_leitura': res['b']['leitura_analogo']}, ensure_ascii=False, indent=1))


def br(x, d=2):
    return f'{x:,.{d}f}'.replace(',', 'X').replace('.', ',').replace('X', '.')


def mi(x):
    return br(x / 1e6, 2) + ' mi'


def texto(p):
    R = json.load(open(p)); a = R['a']; b = R['b']; u = R['urna_totais']; L = []
    P = L.append
    P('L5 do Adendo 18: pesquisas, que não passam pela urna (2026, sem outras eleições como régua).')
    P('Script: scripts/analisar_L5.py. Números: resultados/L5_pesquisas.json. Rodado em 29/10/2026 com secoes2026.json.gz (bweb dos dois')
    P(f'turnos, {br(u["secoes"], 0)} seções com os dois), candidatos2026_1t.json.gz e os coeficientes já registrados em resultados/T7_T14_bweb.json.')
    P('Pesquisas: resultados/nacionais_2026_pesquisas_verificadas.txt e contexto_2t_2026_pesquisa_verificada.json (conferidos), mais a busca')
    P('de 29/10 (WebSearch/WebFetch); cada número leva a fonte no JSON.')
    P('')
    P('Critério registrado (PRE-REGISTRO-2026-10-26.md, Adendo 18, antes de rodar):')
    P('  (a) "Para cada instituto com pesquisa final nos dois turnos: erro de Flávio (urna menos pesquisa, nos válidos) no 1º e no 2º turno.')
    P('      Incoerência: em pelo menos 6 dos institutos, Flávio acima da pesquisa no 1º turno e abaixo dela no 2º, com virada média de 4')
    P('      pontos ou mais. Coerente: sinais iguais nos dois turnos na maioria."')
    P('  (b) "O saldo de quem não votou num finalista no 1º turno (branco, nulo, abstenção e eleitor de eliminado que as pesquisas davam como')
    P('      nenhum): pela urna e pelas transferências declaradas, a fatia desse saldo que foi para Lula. Comparar com a divisão entre Lula e')
    P('      Flávio dos indecisos, brancos, nulos e não vai votar nas pesquisas finais do 2º turno, quando o instituto publicar. Incoerência:')
    P('      fatia de Lula pela urna acima da maior fatia das pesquisas em 30 pontos ou mais. Sem a divisão publicada, só descritivo."')
    P('  Transparência: o Adendo 18 foi escrito depois do T12 (erros das pesquisas por instituto) e do T37; o desenho de (a) já era')
    P('  conhecido em parte (T12 tinha 7 institutos). Não é um teste cego.')
    P('')
    P('VEREDITOS PELA LETRA')
    r = a['resumo']
    P(f'  (a) {a["veredito"]}. {r["com_padrao"]} de {r["institutos"]} institutos com Flávio acima da pesquisa no 1º turno e abaixo no 2º; virada média')
    P(f'      {br(r["virada_media_todos"])} pontos (erro-padrão {br(r["ep_entre_institutos"])} pela dispersão entre institutos, {br(r["ep_amostral_media"])} só amostral).')
    lb = b['leitura_analogo']
    P(f'  (b) {b["veredito"]}. Nenhuma pesquisa final publicou a divisão entre Lula e Flávio dos seus indecisos, brancos, nulos e "não vai votar".')
    P(f'      Desvio declarado, só descritivo: contra o análogo publicado (voto no 2º turno de quem votou branco/nulo ou faltou no 1º), a fatia')
    P(f'      pela urna com as transferências da pesquisa final do PoderData é {br(100 * lb["fatia_urna_PoderData_final_fid100"], 1)}% (fidelidade 100%) e {br(100 * lb["fatia_urna_PoderData_final_fid_declarada"], 1)}% (fidelidade')
    P(f'      declarada), acima do limite de {br(100 * lb["limite_maior_final_mais_30"], 1)}% (maior fatia final, {br(100 * b["maior_fatia_final"]["fatia_L"], 1)}%, mais 30). Pela regressão da própria urna, a fatia de Lula')
    P(f'      no branco/nulo e na abstenção é {br(100 * b["so_urna_regressao"]["fatia_L_branco_nulo_e_abstencao"], 1)}%, {br(lb["so_urna_menos_maior_final_pontos"], 1)} pontos da maior fatia final.')
    P('')
    P('1. (a) Erro de Flávio por instituto, nos válidos (urna menos pesquisa; positivo = Flávio teve mais que a pesquisa)')
    rr = a['real']
    P(f'  Urna: 1º turno Flávio {br(rr["F1"])}%, Lula {br(rr["L1"])}%, eliminados {br(rr["outros1"])}% (válidos sem o 28); 2º turno Flávio {br(rr["F2"])}%, Lula {br(rr["L2"])}%.')
    P('  instituto            | 1T pesq. | erro 1T (ep)  | 2T pesq. | erro 2T (ep)  | virada (ep)    | padrão | a 2 ep')
    for x in a['institutos']:
        P(f'  {x["instituto"]:20s} | {br(x["F1_pesquisa"]):>8s} | {br(x["erro_F1"]):>6s} ({br(x["ep_F1"])}) | {br(x["F2_pesquisa"]):>8s} | {br(x["erro_F2"]):>6s} ({br(x["ep_F2"])}) | '
          f'{br(x["virada"]):>6s} ({br(x["ep_virada"])}) | {"sim" if x["padrao_acima_1T_abaixo_2T"] else "não":6s} | {"sim" if x["padrao_a_2ep"] else "não"}')
    P(f'  Com o padrão: {r["com_padrao"]} de {r["institutos"]} (limite: 6). Mesmo sinal nos dois turnos: {r["mesmo_sinal"]} de {r["institutos"]}. Com o padrão a 2 erros-padrão')
    P(f'  nos dois turnos: {r["com_padrao_a_2ep"]}. Virada média {br(r["virada_media_todos"])}, mediana {br(r["mediana_virada"])}, desvio entre institutos {br(r["dp_viradas"])}.')
    P(f'  Distância ao limite de 4 pontos: {br(abs(r["virada_media_todos"]) - 4)} pontos, {br((abs(r["virada_media_todos"]) - 4) / r["ep_entre_institutos"], 1)} erros-padrão entre institutos.')
    P('  Erro amostral: amostra simples com a amostra publicada (2.000 quando não publicada, marcado n=None no JSON); não inclui efeito de')
    P('  desenho nem viés de casa, por isso o erro-padrão pela dispersão entre institutos é o que vale para a média.')
    s = a['sensibilidade']
    P(f'  Sensibilidade (1º turno alternativo): Veritá 45,14 e AtlasIntel 43,1: padrão em {s["com_padrao_com_alternativas"]} de {r["institutos"]}, virada média {br(s["virada_media_com_alternativas"])}.')
    P(f'  Fora de (a): ' + '; '.join(f'{k}: {v}' for k, v in a['fora'].items()) + '.')
    P('  Notas por instituto (campo e fonte no JSON): ' + '; '.join(f'{x["instituto"]}: {x["nota1"]} / {x["nota2"]}' for x in a['institutos'] if 'desvio' in x['nota1'] or 'Fórum' in x['nota1']) + '.')
    P('')
    P('  De onde vem a virada (descritivo):')
    P(f'    1º turno, erro médio: Flávio {br(r["erro_F1_medio"])}, Lula {br(r["erro_L1_medio"])}, eliminados {br(r["erro_outros1_medio"])} pontos. O erro do 1º turno')
    P('    foi quase todo entre Flávio e os eliminados (as pesquisas davam aos eliminados mais do que tiveram); Lula ficou, na média, onde as')
    P('    pesquisas diziam.')
    P(f'    2º turno, erro médio: Flávio {br(r["erro_F2_medio"])}, Lula {br(r["erro_L2_medio"])}. Medida em Lula, a virada é de {br(r["erro_L2_medio"] - r["erro_L1_medio"])} pontos')
    P(f'    (de {br(r["erro_L1_medio"])} para {br(r["erro_L2_medio"])}); os outros {br(abs(r["virada_media_todos"]) - (r["erro_L2_medio"] - r["erro_L1_medio"]))} pontos da virada de Flávio vêm do 1º turno.')
    P('    Lula por instituto, erro 1T / 2T: ' + '; '.join(f'{x["instituto"]} {br(x["erro_L1"])} / {br(x["erro_L2"])}' for x in a['institutos']) + '.')
    P('')
    P('2. (b) Saldo de quem não votou num finalista no 1º turno')
    ub = b['urna']
    P(f'  Urna (seções com os dois turnos): Lula +{br(ub["ganho_L"], 0)}, Flávio +{br(ub["ganho_F"], 0)}. Fontes: eliminados {br(ub["eliminados_1T"], 0)},')
    P(f'  queda do branco+nulo {br(ub["queda_branco_nulo"], 0)} (o 28 conta como nulo), aumento do comparecimento {br(ub["aumento_comparecimento"], 0)}')
    P(f'  (abstenção {br(ub["abstencao_1T_pct"])}% no 1º turno, {br(ub["abstencao_2T_pct"])}% no 2º). Identidade ganhos = fontes: diferença {br(ub["identidade_ganhos"], 0)}.')
    cf = b['conferencia_decomposicao_antiga']
    P(f'  Conferência: com os totais impressos em decomposicao_fluxos_2026.txt (taxas atribuídas à Quaest, não confirmadas), a mesma conta')
    P(f'  dá {br(100 * cf["fatia_L"], 1)}% (registrado 98%).')
    P('')
    P('  2.1 Fatia do saldo que foi para Lula, pela urna e pelas transferências declaradas de cada pesquisa (a conta do arquivo antigo):')
    P('  pesquisa                      | dos eliminados F / L / nenhum      | do saldo F / L        | saldo     | fatia L fid. 100% | fatia L fid. declarada')
    for k, v in b['por_pesquisa'].items():
        f = v['fidelidade_100']; d = v['fidelidade_declarada']
        P(f'  {k:29s} | {mi(f["dos_eliminados_F"])} / {mi(f["dos_eliminados_L"])} / {mi(f["nenhum_dos_eliminados"])} | {mi(f["do_saldo_F"])} / {mi(f["do_saldo_L"])} | '
          f'{mi(f["saldo"])} | {br(100 * f["fatia_L"], 1):>6s}%           | {(br(100 * d["fatia_L"], 1) + "%") if d else "não publicada"}')
    m = b['mediana_institutos']['fidelidade_100']
    P(f'  mediana dos institutos por grupo (fid. 100%): Flávio dos eliminados {mi(m["dos_eliminados_F"])}, fatia {br(100 * m["fatia_L"], 1)}%.')
    pf = b['por_pesquisa']['PoderData 23-24/10 (final)']
    for e in pf['erro_amostral']:
        P(f'  erro da fatia do PoderData final pela amostra (sorteio multinomial das subamostras), efeito de desenho {br(e["deff"], 0)}: '
          f'fid. 100% ep {br(100 * e["fid_100"]["ep"], 1)} (95%: {br(100 * e["fid_100"]["p2_5"], 1)} a {br(100 * e["fid_100"]["p97_5"], 1)}); '
          f'fid. declarada ep {br(100 * e["fid_declarada"]["ep"], 1)} (95%: {br(100 * e["fid_declarada"]["p2_5"], 1)} a {br(100 * e["fid_declarada"]["p97_5"], 1)})')
    P('    subamostras estimadas pela fatia do 1º turno (efeito de desenho 1): ' + ', '.join(f'{g} {n}' for g, n in pf['erro_amostral'][0]['tamanhos_subamostra'].items()))
    P('  Notas: ' + '; '.join(f'{k}: {v["nota"]}' for k, v in b['por_pesquisa'].items()) + '.')
    P(f'  O que os eleitores dos eliminados declararam para Flávio passa do ganho inteiro dele na urna (+{mi(ub["ganho_F"])}) em '
      f'{len(b["eliminados_F_passa_ganho_real_F"])} de {len(b["por_pesquisa"])} pesquisas')
    P(f'  (só não passa em: {", ".join(b["eliminados_F_nao_passa"]) or "nenhuma"}). Então Flávio fica negativo no saldo e a fatia de Lula passa de 100%:')
    P('  pelas transferências declaradas, a conta não fecha.')
    P('')
    P('  2.2 O que as pesquisas finais publicaram sobre a divisão dos seus indecisos, brancos, nulos e "não vai votar" (critério literal):')
    for k, v in b['divisao_literal'].items():
        P(f'    {k}: {v}')
    P('')
    P('  2.3 Análogo publicado (desvio declarado): voto no 2º turno de quem não escolheu finalista no 1º, fatia de Lula entre os que')
    P('  escolhem um dos dois (ep aproximado, com o tamanho do grupo estimado):')
    for x in b['analogo']:
        P(f'    {"final" if x["final"] else "antes":5s} | {x["pesquisa"]:20s} | {x["grupo"]:55s} | L {br(x["L"], 1)} F {br(x["F"], 1)} | fatia {br(100 * x["fatia_L"], 1)}% (ep {br(100 * x["ep"], 1)})')
    mf = b['maior_fatia_final']; mq = b['maior_fatia_qualquer_rodada']
    P(f'  Maior fatia nas pesquisas finais: {br(100 * mf["fatia_L"], 1)}% ({mf["pesquisa"]}, {mf["grupo"]}); limite do critério {br(100 * lb["limite_maior_final_mais_30"], 1)}%.')
    P(f'  Maior em qualquer rodada: {br(100 * mq["fatia_L"], 1)}% ({mq["pesquisa"]}); limite {br(100 * lb["limite_maior_qualquer_mais_30"], 1)}%.')
    P(f'  Pesquisas cuja fatia pela urna fica acima do limite final nas duas fidelidades: {", ".join(lb["pesquisas_com_fatia_acima_do_limite_final"]) or "nenhuma"}.')
    P(f'  Com o limite de qualquer rodada ({br(100 * lb["limite_maior_qualquer_mais_30"], 1)}%), o PoderData final {"passa" if lb["passa_limite_qualquer_rodada"] else "não passa"}.')
    zz = lb['z_acima_do_limite_final']
    P('  Distância do PoderData final ao limite de ' + br(100 * lb['limite_maior_final_mais_30'], 1) + '%, em erros-padrão (urna e pesquisa): '
      + '; '.join(f'{k.replace("_deff", ", efeito de desenho ")} {br(v, 1)}' for k, v in zz.items()) + '.')
    P('')
    so = b['so_urna_regressao']
    P('  2.4 Só a urna (regressão do T8 com grupos, mesmo local; T7_T14_bweb.json):')
    P(f'    fatia de Lula na queda do branco+nulo {br(100 * so["coef_L_queda_branco_nulo"][0], 1)}% (ep {br(100 * so["coef_L_queda_branco_nulo"][1], 1)}), no aumento do comparecimento '
      f'{br(100 * so["coef_L_var_comparecimento"][0], 1)}% (ep {br(100 * so["coef_L_var_comparecimento"][1], 1)});')
    P(f'    somadas pelo tamanho: {br(100 * so["fatia_L_branco_nulo_e_abstencao"], 1)}% (ep {br(100 * so["ep_sem_covariancia"], 1)}, sem a covariância). Eleitores dos eliminados para Lula:')
    P(f'    {br(100 * so["b_L_eliminados_somado"][0], 1)}% (ep {br(100 * so["b_L_eliminados_somado"][1], 1)}). Lula leva {br(100 * so["coef_L_votos_Flavio_1T"][0], 1)}% dos votos de Flávio do 1º turno e Flávio leva '
      f'{br(-100 * so["coef_L_proprios_1T"][0], 1)}% dos de Lula (líquido, no mesmo local; na PoderData final, 5% e 5%).')
    P('    Pela regressão da urna, o branco/nulo e a abstenção se dividiram perto do que as pesquisas finais dizem (PoderData 65,8% e 58,8%,')
    P('    Nexus 53,2%). A diferença entre urna e pesquisa fica nos eleitores dos eliminados (urna 54% para Lula; pesquisas de 30% a 44% entre')
    P('    os que escolheram, T37) e na troca entre os eleitores de Flávio e de Lula. É regressão ecológica entre seções do mesmo local.')
    P('    ' + so['nota'] + '.')
    P('')
    eq = b['equivalencia_com_erro_2T']
    P('  2.5 O que a fatia acima de 100% mede: se o saldo tivesse se dividido como a maior fatia final, com as transferências e a fidelidade')
    P(f'  do PoderData final, Lula teria {br(eq["L_validos_se_saldo_como_pesquisa"])}% dos válidos (o PoderData final dava {br(eq["L_validos_PoderData_final"], 0)}%; a urna deu {br(eq["L_validos_urna"])}%).')
    P(f'  A diferença na margem é de {mi(eq["votos_de_diferenca_na_margem"])}. Por essa tabela, Flávio ganharia {mi(eq["ganho_esperado_F"])} entre os turnos (ganhou '
      f'{mi(eq["ganho_real_F"])}) e Lula {mi(eq["ganho_esperado_L"])} (ganhou {mi(eq["ganho_real_L"])}).')
    P('  É o mesmo erro do 2º turno visto em (a), escrito como fluxo: a fatia acima de 100% não traz informação independente de (a).')
    P('')
    P('  2.6 Intenção de comparecimento nas pesquisas finais (descritivo):')
    for nome, txt, url in b['comparecimento']:
        P(f'    {nome}: {txt}')
    P('    Em todas as que mediram, os mais propensos a votar davam mais Flávio. Passar do eleitor provável para a amostra inteira tira de')
    P('    Flávio de 0,5 (Quaest) a 1,9 ponto (Nexus); com a amostra inteira votando, as pesquisas ainda davam Flávio à frente (Datafolha 51,')
    P('    Nexus 50,5, Quaest 50,5). Pela própria pesquisa, comparecimento maior não leva ao resultado da urna.')
    P(f'    Na urna, o comparecimento subiu {mi(ub["aumento_comparecimento"])}; com a fatia de {br(100 * so["coef_L_var_comparecimento"][0], 1)}% da regressão, isso dá a Lula uma margem de')
    P(f'    cerca de {mi(ub["aumento_comparecimento"] * (2 * so["coef_L_var_comparecimento"][0] - 1))}, pouco perto da diferença de {mi(eq["votos_de_diferenca_na_margem"])}.')
    P('')
    P('3. O que isso significa (leitura, nos dois sentidos)')
    P(f'  - (a) cumpre a letra: as 11 pesquisas erraram para lados opostos nos dois turnos. Mas a virada de {br(abs(r["virada_media_todos"]))} pontos junta duas coisas.')
    P(f'    No 1º turno, o erro foi entre Flávio e os eliminados (Lula ficou na pesquisa, erro médio {br(r["erro_L1_medio"])}). No 2º turno, as pesquisas')
    P(f'    deram a Lula {br(r["erro_L2_medio"])} pontos a menos, todas na mesma direção, com métodos diferentes (telefone automático, presencial, internet).')
    P('    É esse erro do 2º turno, e não o do 1º, que uma fraude no 2º turno produziria. Ele também é o que um erro comum das pesquisas')
    P('    produziria; o teste não separa as duas coisas. Uma fraude a favor de Lula que valesse também no 1º turno teria posto Lula acima')
    P(f'    das pesquisas no 1º turno; ele ficou nelas (erro médio {br(r["erro_L1_medio"])}), e quem passou da pesquisa foi Flávio.')
    f100 = [v['fidelidade_100']['fatia_L'] for v in b['por_pesquisa'].values()]
    fdc = [v['fidelidade_declarada']['fatia_L'] for v in b['por_pesquisa'].values() if v['fidelidade_declarada']]
    P(f'  - (b) pela letra é descritivo. A conta "pela urna e pelas transferências declaradas" passa de 100% em {sum(x > 1 for x in f100)} de {len(f100)} pesquisas')
    P(f'    com fidelidade 100% (de {br(100 * min(f100), 1)}% a {br(100 * max(f100), 1)}%) e fica entre {br(100 * min(fdc), 1)}% e {br(100 * max(fdc), 1)}% com a fidelidade declarada, porque o que os')
    P('    eleitores dos eliminados disseram que dariam a Flávio já é mais do que ele ganhou. Isso é real e é a "conta que não fecha". Mas é o')
    P('    mesmo erro do 2º turno em outra forma (2.5): com a divisão da pesquisa, o resultado volta a ser o da pesquisa. Não é um segundo')
    P('    indício, e o tamanho dele depende de qual pesquisa se usa (erro de 4 a 10 pontos só pela amostra).')
    P('  - Onde está a diferença, pela regressão da própria urna: não no branco, nulo e abstenção (que se dividiram como as pesquisas finais')
    P('    dizem), e sim nos eleitores dos eliminados e na troca entre eleitores de Flávio e de Lula. É aí que outros testes (L3, L4, T14, T37)')
    P('    olham; uma troca proporcional de votos de Flávio para Lula apareceria lá, e o T14 não a achou acima do limite registrado.')
    P('  - Comparecimento: as pesquisas finais diziam que o eleitor mais provável era mais de Flávio, e o comparecimento subiu; mesmo com')
    P('    todos os entrevistados votando, elas davam Flávio à frente. Essa explicação comum ("o eleitor de Lula foi votar") cobre pouco do erro.')
    P('')
    P('O que ficou de fora: as tabelas cruzadas da Quaest, Datafolha, AtlasIntel, Nexus e CNT/MDA das rodadas finais (não publicadas na')
    P('imprensa nem achadas em PDF); o tamanho real das subamostras (estimado pela fatia do 1º turno); efeito de desenho das pesquisas;')
    P('a Veritá e a AtlasIntel do 1º turno têm duas versões (sensibilidade acima); Ipespe, Paraná Pesquisas e Ipsos-Ipec sem os dois turnos.')
    return '\n'.join(L)


if __name__ == '__main__':
    if sys.argv[1] == '--texto':
        print(texto(sys.argv[2]))
    else:
        rodar(sys.argv[1:])
