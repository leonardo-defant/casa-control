"""F17 do Adendo 22 (PRE-REGISTRO-2026-10-26.md, commit f12121e, 31/10/2026 14:52:48 UTC): relatórios completos das pesquisas finais.

Texto registrado (letra):
  "Procurar os relatórios completos (PDF ou tabela) com o voto no 2º turno por voto no 1º turno das pesquisas de 20 a 24/10
  (Quaest, Datafolha, AtlasIntel, Nexus, CNT/MDA, Palver, Ipespe, Gerp e outras) e as rodadas anteriores que faltaram no F13.
  Mesma conta e mesma régua do F13."
Régua do F13 (Adendo 21): "fatia de Lula entre os eleitores dos eliminados que escolheram um finalista. Descritivo, com a régua:
  'confere com a urna' se ficar a 5 pontos ou menos de 52% a 54%; 'confere com as pesquisas de antes' se ficar entre 32% e 44%;
  entre os dois, intermediário."

Decisões tomadas ANTES de buscar e de calcular (31/10/2026, 14h56 UTC), onde o registro não fixa. Cada uma é desvio declarado.
Cópia com sha256 e hora: /home/user/trabalho-eleicao/adendo22/F17_scripts/decisoes_antes_de_buscar.py (sha256 e5ee3824...).
As decisões D1 a D11 do F13 (scripts/analisar_F13.py) valem onde não forem mudadas aqui.

E1. Universo.
    Grupo A ("pesquisas de 20 a 24/10"): rodadas nacionais de presidente com campo terminando entre 20/10/2026 e 24/10/2026,
    inclusive. Entram de novo as rodadas de A que já estavam no F13 (PoderData 23-24/10, Colectta 23/10, AtlasIntel 18-23/10,
    PoderData 19-21/10, Quaest 17-20/10): se o relatório completo for achado, os números dele substituem os da matéria (os dois
    ficam relatados lado a lado); se não, ficam os números do F13, marcados "do F13".
    Grupo B ("rodadas anteriores que faltaram no F13"): rodadas nacionais com campo terminando entre 05/10 e 19/10/2026 que não
    estão nas fontes nem nas referências do F13 (F13_pesquisas_independentes.json).
    Fora dos dois grupos: pesquisas estaduais; campo terminando em 25/10 ou depois (o tracking da AtlasIntel encerrado às 8h de
    25/10, se o cruzamento aparecer, é relatado à parte, com s calculado e sem entrar na contagem da régua).
E2. Régua: a do F13 (D3), pela estimativa pontual, sem arredondar, aplicada a cada cruzamento achado, em A e em B, como manda a
    letra ("mesma régua"). Faixas: "confere com a urna" se 47 <= s <= 59; "confere com as pesquisas de antes" se 32 <= s <= 44;
    "intermediário" se 44 < s < 47; s < 32 "abaixo das pesquisas de antes"; s > 59 "acima da urna". Em B a régua é circular
    (essas rodadas são as "pesquisas de antes"); fica relatada, mas o resumo principal é o do grupo A.
E3. Conta: a mesma do F13 (função calcula copiada sem mudança): s = soma_k w_k L_k / soma_k w_k (L_k + F_k), w_k = votos oficiais
    do 1º turno dos candidatos que a coluna representa; coluna que mistura eleitor de eliminado com branco, nulo, não votou ou
    não lembra fica fora; "outro(s)" = eliminados que a pesquisa não separou; sensibilidades (a) só nomeadas, (b) pesos pela
    lembrança da própria pesquisa, (c) média simples; erro amostral do D4 (n do grupo pela fatia oficial, efeito de desenho 1 e
    2); urna com as mesmas colunas nomeadas e os mesmos pesos. Candidato menor separado sozinho numa coluna: peso pelos votos
    dele (base/candidatos2026_1t.json.gz: Samara 122.911; Hertz 43.103; Clariana 40.043; Edmilson 22.693; Wilson Grassi 16.881;
    Rui Costa Pimenta 15.024). Se o relatório publica a base (entrevistas) de cada coluna, calculo também um erro com essas bases,
    descritivo, que não muda a classificação.
E4. Pergunta usada: voto estimulado no 2º turno (Lula x Flávio) cruzado pelo voto declarado no 1º turno. Se houver tabela de
    total e de válidos, uso a de total (L/(L+F) é o mesmo na mesma base). Se só houver válidos, uso válidos.
E5. Fonte e confiança (D8 do F13): alta = tabela lida por mim no relatório do instituto (PDF, página ou planilha do instituto,
    inclusive cópia do PDF do instituto no static.poder360 ou no PesqEle, ou publicação na conta oficial do instituto); média =
    matéria que atribui o número ao instituto com a rodada identificada (data de campo ou registro); baixa = agregador, Wikipedia,
    rede social que não é do instituto, ou rodada inferida. Só alta e média recebem a régua; baixa fica descritiva.
E6. Mais de uma fonte para a mesma rodada: relatório antes de matéria; entre matérias, a com mais colunas de eliminados.
    Divergência entre fontes da mesma rodada é relatada e vai para as pistas.
E7. Resumo: contagem por faixa no grupo A (todas as fontes com régua e só as com cobertura de 90% ou mais dos votos dos
    eliminados) e no grupo B; lista do que foi procurado e não achado, com o que foi tentado. Média combinada só descritiva,
    pós-hoc, sem régua (mesma do F13: cobertura de 90% ou mais, confiança alta ou média, pesos 1/ep^2). Sem nenhum cruzamento
    novo achado: "SEM DADOS NOVOS" pela letra. O F17 não tem critério de sinal.
E8. Urna: os mesmos números do F13 (regressão do T8 com grupos no bweb: Cury 59,64; Renan 54,22; Caiado 48,80; Zema 36,10;
    todos os eliminados 54,07; amostra do T37). A especificação do conferente do F13 (Cury 60,0; Renan 52,0; Caiado 47,2;
    Zema 31,7; todos 53,9) fica só como sensibilidade descritiva.
E9. Downloads: cada um numa pasta nova e vazia /home/user/trabalho-eleicao/adendo22/F17_dl_<nome>/; textos extraídos com
    pdftotext em /home/user/trabalho-eleicao/adendo22/F17_texto/; scripts em /home/user/trabalho-eleicao/adendo22/F17_scripts/
    e em scripts/analisar_F17.py, que não lê nada das pastas baixadas, só a tabela digitada com a fonte de cada número.
    python3 -I. Sem user agent falso; se o PesqEle ou outro site der 403, exigir navegador com JavaScript ou captcha, não contorno
    e relato.
E10. Regra do Adendo 18: nenhuma eleição anterior como régua.

Decisões tomadas DEPOIS de começar a ler os relatórios (desvios declarados, nenhuma muda limiar nem a conta):
P1. Relatórios achados de rodadas do F13 que não são do grupo A (Datafolha 6-7 e 13-14/10, Quaest 10-13/10, AtlasIntel 3-8/10,
    Nexus 10-12/10) entram numa seção "conferência das rodadas do F13", descritiva. Quatro confirmam o F13; a do Nexus 10-12/10
    não confere (o F13 leu 12% de Lula entre os eleitores de Zema, que é branco/nulo no gráfico, e tratou a coluna agregada de
    todos os eliminados como "outros candidatos"); o valor corrigido é relatado ao lado, sem mudar o veredito do F13.
P2. A média da Quaest no blog do instituto (22/10: eliminados 37% Lula, 43% Flávio) não diz a rodada; pela E5 é "rodada inferida"
    e fica com confiança baixa, descritiva.
P3. Os números das cores dos gráficos (Nexus, Ideia, Palver, AtlasIntel) foram lidos nas páginas renderizadas, não só no texto
    extraído; a legenda de cada gráfico define a cor de cada candidato.
P4. O agregado publicado de todos os eliminados (Nexus "eleitor de outros candidatos" na página anterior ao detalhamento; Ideia
    "os quatro somados") fica como sensibilidade descritiva; a medida principal usa as colunas por candidato (D2 do F13).
P5. Pós-hoc, sem régua: média combinada com teste de heterogeneidade (Q de Cochran), agrupamento por método de coleta (online,
    telefone, presencial) sobre todas as rodadas do F13 e do F17, e fatia por candidato sobre todas as rodadas. Nenhum candidato
    menor apareceu sozinho numa coluna (a regra de peso da E3 para isso não foi usada).

Uso: python3 -I analisar_F17.py <saida.json> <saida.txt>
"""
import json, math, sys

# ------------------------------------------------------------------ urna (mesmos números do F13, E8)
VOTOS_1T = {'Cury': 3448569, 'Renan': 2675887, 'Caiado': 2605148, 'Zema': 326488, 'esquerda': 80820, 'demais': 179835}
ELIMINADOS = sum(VOTOS_1T.values())            # 9.316.747
APTOS_1T = 158744977
COMP_1T = 125275833
URNA_BWEB = {'Cury': (59.64, 0.27), 'Renan': (54.22, 0.29), 'Caiado': (48.80, 0.31), 'Zema': (36.10, 0.86)}
URNA_AMOSTRA = {'Cury': (54.00, 2.96), 'Renan': (49.31, 3.07), 'Caiado': (54.18, 3.31), 'Zema': (41.82, 8.37)}
URNA_CONFERENTE_F13 = {'Cury': 60.0, 'Renan': 52.0, 'Caiado': 47.2, 'Zema': 31.7, 'todos': 53.9}
URNA_TODOS = 54.07

GRUPOS_COLUNA = {
    'Cury': ['Cury'], 'Renan': ['Renan'], 'Caiado': ['Caiado'], 'Zema': ['Zema'],
    'outro_sem_zema': ['esquerda', 'demais'],
    'outro_com_zema': ['Zema', 'esquerda', 'demais'],
    'outro_nexus': ['Cury', 'Renan', 'esquerda', 'demais'],
    'agregado_4': ['Cury', 'Renan', 'Caiado', 'Zema'],
    'agregado_todos': ['Cury', 'Renan', 'Caiado', 'Zema', 'esquerda', 'demais'],
}
NOMEADAS = {'Cury', 'Renan', 'Caiado', 'Zema'}
DL = '/home/user/trabalho-eleicao/adendo22/'
SHA = {  # sha256 dos PDFs (F17_scripts/sha256_usados.txt)
    'pd12': '0f4e4418d633cbcf30f6364b48a728b67267a18ba649f81b5ef1879048c15ffa',
    'pd15': '61804db6a0c000a4fe06a5d001dc956f0c16d63f78d38df33393794c4ef3fc92',
    'pd18': '49d00ff66ff81342274af5c18ec09ae2ef154ab7316136a648bf1a3cfcaea6b2',
    'ideia': '9f99a207468f4a2973cd4fcb9e5768bd2434ea79b60640ebaab2790162d995a3',
    'df2022': 'c548241d08d526ce1ceecc87e64cd1ba989634130ba165b9660fbab4219321d4',
    'df2324': '41f91c3495dc96da9e51e130fcd74b8078e7c4a31d4bda894b400b847b70c1d0',
    'df0607': '9b95078c8f04e961b48719c166a303b354c4366eb59b633642ef0fc0de7aafcb',
    'df1314': 'b86d9106bbdb9deb074f03e57522365ff9d5a7222f16ff0c8f7b36480cdd9b81',
}

# ------------------------------------------------------------------ fontes
# colunas: (nome, chave em GRUPOS_COLUNA, L %, F %); bases: entrevistas por coluna, quando publicadas (E3)
FONTES = [
    # ======================= grupo A: campo terminando de 20 a 24/10
    dict(id='PoderData 23-24/10', grupo='A', status='do F13 (relatório já lido no F13)', instituto='PoderData',
         campo='23 e 24/10/2026', registro='BR-02828/2026', n=4000, metodo='telefone IVR', amostra_tipo='eleitores', confianca='alta',
         fonte='https://static.poder360.com.br/uploads/2026/10/Relatorio-PoderData-Eleitoral-24out26-1.pdf',
         arquivo='lido no F13 (/home/user/trabalho-eleicao/adendo21/F13_dl_poderdata24out/pd24out.pdf, p. 10)',
         colunas=[('Augusto Cury', 'Cury', 29, 58), ('Renan Santos', 'Renan', 33, 43), ('Ronaldo Caiado', 'Caiado', 30, 46),
                  ('Outro candidato', 'outro_com_zema', 15, 65)]),
    dict(id='Colectta 23/10', grupo='A', status='do F13 (relatório não achado)', instituto='Colectta (Brazil Economy)',
         campo='23/10/2026', registro='BR-05601/2026', n=3000, metodo='presencial', amostra_tipo='eleitores', confianca='média',
         fonte='https://brazileconomy.com.br/mais-lidas/2026/10/lula-tem-503-dos-votos-validos-e-flavio-497-aponta-pesquisa-brazil-economycolectta/',
         arquivo='matéria lida no F13',
         colunas=[('Augusto Cury', 'Cury', 33.4, 37.5), ('Renan Santos', 'Renan', 30.4, 40.9), ('Ronaldo Caiado', 'Caiado', 30.7, 35.9)]),
    dict(id='AtlasIntel 18-23/10', grupo='A', status='relatório achado: substitui a matéria do F13 (que tinha só Renan, s 42,9)',
         instituto='AtlasIntel/Bloomberg', campo='18 a 23/10/2026', registro='BR-06380/2026', n=4990,
         metodo='recrutamento digital aleatório', amostra_tipo='eleitores', confianca='alta',
         fonte='https://static.poder360.com.br/uploads/2026/10/atlasintel-nacional-2oturno-24.out_.2026-1.pdf',
         arquivo=DL + 'F17_dl_p360_atlasintel-nacional-2oturno-24.out_.2026-1/relatorio.pdf (sha256 12a840b19b32253dc06182711b9a001dc004393678cb75247bcbcebb495f5f85), p. 9, bloco "VOTO PRESIDENTE - 1º TURNO 2026"',
         colunas=[('Escritor Augusto Cury', 'Cury', 52.2, 45.5), ('Renan Santos', 'Renan', 30.7, 40.8),
                  ('Ronaldo Caiado', 'Caiado', 48.8, 41.5), ('Outro', 'outro_com_zema', 33.5, 51.7)],
         nota='branco/nulo/não sei: Cury 2,3; Renan 28,6; Caiado 9,7; Outro 14,9. Renan confere com a matéria usada no F13 (30,7 x 40,8).'),
    dict(id='Nexus 23-24/10', grupo='A', status='novo (F13 não achou o relatório)', instituto='Nexus/BTG Pactual', campo='23 e 24/10/2026',
         registro='BR-08234/2026', n=2000, metodo='telefone', amostra_tipo='eleitores', confianca='alta',
         fonte='https://static.poder360.com.br/uploads/2026/10/BTG_Nexus_Eleicoes_2026_Rodada_19_versao_completa_24_out_2026.pdf',
         arquivo=DL + 'F17_dl_p360_BTG_Nexus_Eleicoes_2026_Rodada_19_versao_completa_24_out_2026/relatorio.pdf (sha256 be0f443c6782cfae...), p. 23 (detalhado) e p. 22 (agregado)',
         colunas=[('Eleitor do Escritor Augusto Cury', 'Cury', 40.6, 41.8), ('Eleitor de Renan Santos', 'Renan', 24.7, 54.6),
                  ('Eleitor de Ronaldo Caiado', 'Caiado', 35.3, 47.6), ('Eleitor de Zema', 'Zema', 18.5, 65.9),
                  ('Eleitor de outros candidatos', 'outro_sem_zema', 49.3, 0.0)],
         agregado_publicado=('Eleitor de outros candidatos (p. 22, todos os eliminados)', 32.1, 48.5),
         nota='nenhum/branco/nulo e NS: Cury 17,4 e 0,2; Renan 20,6 e 0; Caiado 3,9 e 13,2; Zema 0 e 15,6; outros 0 e 50,7. '
              'Rodada 19, versão completa, divulgada em 24/10.'),
    dict(id='Ipespe 20-22/10', grupo='A', status='novo (F13 não achou o PDF)', instituto='Ipespe/Abrapel', campo='20 a 22/10/2026',
         registro='BR-04350/2026', n=1500, metodo='telefone', amostra_tipo='eleitores', confianca='alta',
         fonte='https://static.poder360.com.br/uploads/2026/10/ipespe-pesquisa2oturno-23out2026.pdf',
         arquivo=DL + 'F17_dl_p360_ipespe-pesquisa2oturno-23out2026/relatorio.pdf (sha256 f366ff06fd1f3cc4...), p. 7 "2º turno x recall do voto no 1º turno"',
         lembranca={'Cury': 2, 'Caiado': 2, 'Renan': 2, 'outro_com_zema': 0},
         colunas=[('Augusto Cury (2%)', 'Cury', 31, 56), ('Ronaldo Caiado (2%)', 'Caiado', 19, 64), ('Renan Santos (2%)', 'Renan', 13, 38),
                  ('Outros (0%)', 'outro_com_zema', 0, 50)],
         nota='branco/nulo e NS/NR: Cury 11 e 3; Caiado 6 e 11; Renan 38 e 13; Outros 50 e 0. O registro no PDF é BR-04350/2026 '
              '(a imprensa grafou BR-00223/2026, que é o da rodada de 13-15/10).'),
    dict(id='Datafolha 20-22/10', grupo='A', status='novo (rodada que não estava no F13)', instituto='Datafolha', campo='20 a 22/10/2026',
         registro='BR-09709/2026', n=2520, metodo='presencial', amostra_tipo='eleitores', confianca='alta',
         fonte='https://media.folha.uol.com.br/datafolha/2026/10/23/xruy9kxbaieozsbhp0lxbvdrv6cvlf5iuxgfkw04tre.pdf',
         arquivo=DL + 'F17_dl_datafolha_20a22out/relatorio.pdf (sha256 ' + SHA['df2022'] + '), p. 5 (Relatório)',
         colunas=[('Cury, Renan, Caiado ou Zema', 'agregado_4', 26, 47)],
         nota='"Entre quem votou em Escritor Augusto Cury (Avante), Renan Santos (Missão), Ronaldo Caiado (PSD) ou Zema (Novo) no '
              'primeiro turno, 47% migram para Flávio Bolsonaro no 2º turno, 26% para Lula, 21% optam pelo branco ou nulo, e 6% desses '
              'eleitores estão indecisos." As tabelas do relatório não cruzam pelo voto no 1º turno.'),
    dict(id='PoderData 19-21/10', grupo='A', status='do F13 (estava como referência; relatório já lido)', instituto='PoderData',
         campo='19 a 21/10/2026', registro='BR-07926/2026', n=4000, metodo='telefone IVR', amostra_tipo='eleitores', confianca='alta',
         fonte='https://static.poder360.com.br/uploads/2026/10/Relatorio-PoderData-Eleitoral-21out26-2.pdf', arquivo='lido no F13',
         colunas=[('Cury', 'Cury', 48, 42), ('Renan', 'Renan', 34, 49), ('Caiado', 'Caiado', 30, 49), ('Outro', 'outro_com_zema', 20, 70)]),
    dict(id='Palver 18-20/10', grupo='A', status='novo (rodada que não estava no F13)', instituto='Palver (onda 8)', campo='18 a 20/10/2026',
         registro='BR-04612/2026', n=5000, metodo='online, recrutamento por anúncios, calibrada (n efetivo 1.745)', amostra_tipo='eleitores',
         confianca='alta', fonte='https://static.poder360.com.br/uploads/2026/10/pesquisaPalver-presidente-21out2026_compressed-compactado.pdf',
         arquivo=DL + 'F17_dl_p360_pesquisaPalver-presidente-21out2026_compressed-compactado/relatorio.pdf (sha256 988ab9257ee2556b...), p. 27 "Transferência de voto"',
         bases={'Renan': 113, 'Cury': 99, 'Caiado': 57},
         colunas=[('Eleitor de Renan Santos (n=113)', 'Renan', 39, 42), ('Eleitor de Augusto Cury (n=99)', 'Cury', 52, 43),
                  ('Eleitor de Ronaldo Caiado (n=57)', 'Caiado', 44, 44)],
         nota='branco/nulo ou não votaria e indecisos: Renan 12 e 7; Cury 5 e 0; Caiado 11 e 1. Nota do instituto: "As bases são '
              'pequenas (n efetivo entre 29 e 63), e os intervalos, largos." Sem Zema e sem outros.'),
    dict(id='Quaest 17-20/10', grupo='A', status='do F13 (relatório não achado; matéria)', instituto='Quaest', campo='17 a 20/10/2026',
         registro='BR-08535/2026', n=2154, metodo='presencial domiciliar', amostra_tipo='eleitores', confianca='média',
         fonte='https://www.diariodepernambuco.com.br/politica/2026/10/11727201-quaest-48-dos-eleitores-de-augusto-cury-migram-para-lula-e-33-para-flavio.html',
         arquivo='matéria lida no F13; relida em 31/10 (DGABC e Diario de Pernambuco, mesmo texto)',
         colunas=[('Cury', 'Cury', 48, 33), ('Renan', 'Renan', 25, 51), ('Caiado', 'Caiado', 21, 57)],
         nota='BPMoney e SpaceMoney (21/10, citando InfoMoney) dão Caiado 25 x 51, mas o "antes" que elas dão para Caiado (15 x 40, '
              'branco 43) é o de Renan no relatório da rodada anterior (Caiado era 23 x 42, branco 33): erro de cópia nessas matérias.'),
    # ======================= grupo B: campo terminando de 05 a 19/10, rodadas que faltaram no F13
    dict(id='PoderData 16-18/10', grupo='B', status='novo', instituto='PoderData', campo='16 a 18/10/2026', registro='BR-02586/2026',
         n=3000, metodo='telefone IVR', amostra_tipo='eleitores', confianca='alta',
         fonte='https://static.poder360.com.br/uploads/2026/10/Relatorio-PoderData-Eleitoral-18out26.pdf',
         arquivo=DL + 'F17_dl_poderdata_18out26/relatorio.pdf (sha256 ' + SHA['pd18'] + '), p. 10',
         colunas=[('Augusto Cury', 'Cury', 31, 56), ('Renan Santos', 'Renan', 29, 36), ('Ronaldo Caiado', 'Caiado', 19, 46),
                  ('Outro candidato', 'outro_com_zema', 31, 36)],
         nota='branco/nulo e não sabe: Cury 9 e 4; Renan 29 e 6; Caiado 25 e 11; Outro 24 e 9.'),
    dict(id='Nexus 16-18/10', grupo='B', status='novo', instituto='Nexus/BTG Pactual', campo='16 a 18/10/2026', registro='BR-04499/2026',
         n=2002, metodo='telefone', amostra_tipo='eleitores', confianca='alta',
         fonte='https://static.poder360.com.br/uploads/2026/10/Pesquisa-presidencial-BTG-Nexus-19out2026.pdf',
         arquivo=DL + 'F17_dl_p360_Pesquisa-presidencial-BTG-Nexus-19out2026/relatorio.pdf (sha256 f6ee08157b9906a8...), p. 28 (detalhado) e p. 27 (agregado)',
         colunas=[('Eleitor do Escritor Augusto Cury', 'Cury', 38.0, 44.2), ('Eleitor de Renan Santos', 'Renan', 33.6, 43.7),
                  ('Eleitor de Ronaldo Caiado', 'Caiado', 21.6, 68.3), ('Eleitor de Zema', 'Zema', 13.4, 67.7),
                  ('Eleitor de outros candidatos', 'outro_sem_zema', 100.0, 0.0)],
         agregado_publicado=('Eleitor de outros candidatos (p. 27, todos os eliminados)', 32.4, 50.5)),
    dict(id='Ideia 15-19/10', grupo='B', status='novo', instituto='Meio/Ideia', campo='15 a 19/10/2026', registro='BR-08251/2026',
         n=1500, metodo='telefone', amostra_tipo='eleitores', confianca='alta',
         fonte='https://www.canalmeio.com.br/wp-content/uploads/2026/10/Pesquisa-Meio_Ideia-Outubro.pdf (mesmo arquivo no static.poder360)',
         arquivo=DL + 'F17_dl_ideia_15a19out/ideia.pdf (sha256 ' + SHA['ideia'] + '), p. 10 (cruzamento) e p. 31 (lembrança)',
         lembranca={'Cury': 3.9, 'Caiado': 2.6, 'Renan': 2.2, 'Zema': 1.2},
         bases={'Cury': 58, 'Caiado': 39, 'Zema': 18, 'Renan': 33},
         colunas=[('Augusto Cury (58)', 'Cury', 48.3, 36.2), ('Ronaldo Caiado (39)', 'Caiado', 30.8, 53.8),
                  ('Romeu Zema (18)', 'Zema', 22.2, 77.8), ('Renan Santos (33)', 'Renan', 9.1, 90.9)],
         agregado_publicado=('Os quatro somados (148)', 31.8, 58.1),
         nota='lembrança do 1º turno na amostra: Flávio 34,7; Lula 33,8; Cury 3,9; Caiado 2,6; Renan 2,2; Zema 1,2; menores 0,8; '
              'ninguém/branco/nulo 11,6; não sabe 9. Zema aparece com 1,2% da amostra, contra 0,21% dos aptos na urna (cerca de 5 vezes).'),
    dict(id='PoderData 13-15/10', grupo='B', status='novo', instituto='PoderData', campo='13 a 15/10/2026', registro='BR-04258/2026',
         n=3000, metodo='telefone IVR', amostra_tipo='eleitores', confianca='alta',
         fonte='https://static.poder360.com.br/uploads/2026/10/Relatorio-PoderData-Eleitoral-15out26.pdf (versão -1 com a mesma tabela)',
         arquivo=DL + 'F17_dl_poderdata_15out26/relatorio.pdf (sha256 ' + SHA['pd15'] + '), p. 10',
         colunas=[('Augusto Cury', 'Cury', 36, 47), ('Renan Santos', 'Renan', 24, 46), ('Ronaldo Caiado', 'Caiado', 30, 50),
                  ('Outro candidato', 'outro_com_zema', 24, 32)],
         nota='branco/nulo e não sabe: Cury 13 e 5; Renan 24 e 5; Caiado 10 e 10; Outro 23 e 22.'),
    dict(id='Palver 10-13/10', grupo='B', status='novo (o conferente do F13 citou pela imprensa)', instituto='Palver (onda 7)',
         campo='10 a 13/10/2026', registro='BR-08028/2026', n=5000, metodo='online, recrutamento por anúncios, calibrada (n efetivo 1.783)',
         amostra_tipo='eleitores', confianca='alta',
         fonte='https://static.poder360.com.br/uploads/2026/10/pesquisa-palver-presidente-nacional-15out2026-1.pdf',
         arquivo=DL + 'F17_dl_p360_pesquisa-palver-presidente-nacional-15out2026-1/relatorio.pdf (sha256 bc5b3c942027a5ed...), p. 26',
         bases={'Renan': 134, 'Cury': 109, 'Caiado': 54},
         colunas=[('Eleitor de Renan Santos (n=134)', 'Renan', 41, 41), ('Eleitor de Augusto Cury (n=109)', 'Cury', 64, 32),
                  ('Eleitor de Ronaldo Caiado (n=54)', 'Caiado', 35, 61)],
         nota='branco/nulo ou não votaria e indecisos: Renan 18 e 0; Cury 2 e 2; Caiado 2 e 1. Registro BR-08028/2026 no relatório '
              '(a Exame grafou BR-00198, que é o da onda 6). "n efetivo entre 29 e 51".'),
    dict(id='PoderData 10-12/10', grupo='B', status='novo', instituto='PoderData', campo='10 a 12/10/2026', registro='BR-01209/2026',
         n=3000, metodo='telefone IVR', amostra_tipo='eleitores', confianca='alta',
         fonte='https://static.poder360.com.br/uploads/2026/10/Relatorio-PoderData-Eleitoral-12out26.pdf',
         arquivo=DL + 'F17_dl_poderdata_12out26/relatorio.pdf (sha256 ' + SHA['pd12'] + '), p. 10',
         colunas=[('Augusto Cury', 'Cury', 43, 45), ('Renan Santos', 'Renan', 33, 38), ('Ronaldo Caiado', 'Caiado', 30, 44),
                  ('Outro candidato', 'outro_com_zema', 17, 57)],
         nota='branco/nulo e não sabe: Cury 8 e 4; Renan 27 e 2; Caiado 14 e 12; Outro 17 e 9.'),
    # ======================= conferência de rodadas do F13 que não são do grupo A (P1)
    dict(id='Nexus 10-12/10', grupo='conferencia', status='relatório não confere com o F13 (F13: s 37,9 com Zema 12 x 80 e "outros" 32 x 45)',
         instituto='Nexus/BTG Pactual', campo='10 a 12/10/2026', registro='BR-07997/2026', n=2002, metodo='telefone',
         amostra_tipo='eleitores', confianca='alta',
         fonte='https://static.poder360.com.br/uploads/2026/10/BTG-Nexus-Eleicoes-2026-Rodada-17-13.out_.2026.pdf',
         arquivo=DL + 'F17_dl_p360_BTG-Nexus-Eleicoes-2026-Rodada-17-13.out_.2026/relatorio.pdf (sha256 122e3f2052c72c3d...), p. 26 e p. 25',
         colunas=[('Eleitor do Escritor Augusto Cury', 'Cury', 41, 43), ('Eleitor de Renan Santos', 'Renan', 30, 37),
                  ('Eleitor de Ronaldo Caiado', 'Caiado', 27, 55), ('Eleitor de Zema', 'Zema', 0, 80),
                  ('Eleitor de outros candidatos', 'outro_sem_zema', 100, 0)],
         agregado_publicado=('Eleitor de outros candidatos (p. 25, todos os eliminados)', 32, 45),
         nota='no gráfico, Zema é 80 Flávio, 12 nenhum/branco/nulo (preto) e 8 NS/NR; não há barra de Lula. O "32 x 45" que o F13 usou '
              'como "outros candidatos" é o agregado de todos os eliminados da p. 25.'),
]

CONFERIDAS_IGUAIS = [
    ('Datafolha 6-7/10 (BR-02949/2026)', 'relatório (media.folha.uol.com.br/datafolha/2026/10/13/zefhrq....pdf, p. 5): Cury, Renan, Caiado ou Zema '
     '32 Lula x 46 Flávio, 15 branco/nulo; igual ao F13 (que tinha matéria). sha256 ' + SHA['df0607']),
    ('Datafolha 13-14/10 (BR-00466/2026)', 'relatório (media.folha.uol.com.br/datafolha/2026/10/16/2sq1uh....pdf, p. 5): 27 x 46, 23 branco/nulo, '
     '5 indecisos; igual ao F13. O agrupamento inclui Zema, como o F13 rotulou (o conferente do F13 tinha visto "Cury, Renan e Caiado" '
     'numa matéria). sha256 ' + SHA['df1314']),
    ('Quaest 10-13/10 (BR-08729/2026)', 'relatório (static.poder360 quaest-presidencial-2oturno-outubro_compressed.pdf, p. 19, '
     '"Transferência de voto"): Caiado 23 x 42, Renan 14 x 40, Cury 34 x 30, Outros (menos de 1%, inclui Zema) 33 x 38; igual ao F13.'),
    ('AtlasIntel 3-8/10 (BR-03663/2026)', 'relatório (static.poder360 Pesquisa-Atlas_Bloomberg-Nacional-261009.pdf, p. 9): Renan 28,1 x 40,3, '
     'Cury 50,4 x 38,9, Caiado 26,9 x 54,9, Outro 14,8 x 83,4; igual ao F13.'),
]

QUAEST_BLOG = dict(fonte='https://quaest.com.br/segundo-turno-2026-votos-brancos-nulos/ (Felipe Nunes, 22/10/2026)',
                   texto='"esse grupo [eleitores de Cury, Caiado, Renan ou Zema] transfere 43% das intenções de voto para Flávio e 37% para Lula"',
                   L=37, F=43, confianca='baixa (a rodada não é dita; deve ser a de 17-20/10)')

SEM_CRUZAMENTO = [
    ('Quaest 23-24/10 (BR-09158/2026, n 3.702)', 'relatório não achado. O site da Quaest só entrega relatórios depois de um cadastro com nome e e-mail '
     '(não preenchi: seria pedir algo); o static.poder360 tem só a impressão de matérias do g1; nenhuma matéria com o cruzamento achada. '
     'O blog do instituto (30/10) diz que "na pesquisa da véspera, os eleitores que tinham faltado no 1º turno eram mais jovens, mais pobres '
     'e mais favoráveis a Lula, e a parcela deles que dizia que iria votar subiu 12 pontos em uma semana".'),
    ('Datafolha 23-24/10 (BR-09540/2026, n 4.050)', 'relatório lido (media.folha.uol.com.br/datafolha/2026/10/26/ufvbq-yncrbmtg7zhclmra.pdf): '
     'tabelas só por gênero, idade, escolaridade, renda, ocupação, religião, região e natureza do município; o texto não dá a migração dos '
     'eliminados nesta rodada (dá só que 82% deles estão totalmente decididos).'),
    ('CNT/MDA 21-23/10 (BR-02136/2026, n 2.032) e 13-15/10 (BR-00652/2026, n 2.014)', 'relatórios lidos (static.poder360): estratificação só '
     'por sexo, idade, renda, escolaridade, região e religião. Ponderados "pelo voto declarado no 1º turno", sem publicar o cruzamento.'),
    ('Gerp 22-24/10 (BR-09327), 19-21/10 (BR-03835), 14-16/10 (BR-05187), 8-12/10 (BR-07877)', 'relatórios lidos: nas três primeiras rodadas '
     'o relatório diz "Ficam fora deste relatório as perguntas 4, 5a, 5b e 5c, sobre o voto no 1º turno"; o de 22-24/10 usa a "migração do '
     'voto declarado no 1º turno" só dentro de uma projeção (Flávio 51% corrigido pela urna) e não publica a tabela.'),
    ('Verità 12-16/10 (BR-01107/2026, n 15.554)', 'relatório lido: publica a lembrança do 1º turno (Cury 2,2%; Renan 1,5%; Caiado 0,9%; outro 0,5%; '
     'ausente 8,1%) e o 2º turno por perfil, sem cruzar um pelo outro. Rodadas de 15-19, 18-22 e 19-23/10 não achadas.'),
    ('Futura 23-24/10, 19-20/10 (BR-06614), 16-17/10 (BR-06715), 13-15/10 (BR-03764), 7-10/10 (BR-00650)', 'relatórios lidos: nenhum cruza pelo voto no 1º turno.'),
    ('Real Time Big Data 19-22/10 (BR-09670) e 15-19/10 (BR-02952)', 'relatórios lidos: segmentos por gênero, idade, renda, religião e região.'),
    ('Alfa 18-22/10 (BR-08496)', 'relatório lido: sem cruzamento pelo 1º turno.'),
    ('Vox Brasil 20-22/10 (BR-03259), 15-17/10 (BR-04332), 5-7/10 (BR-09623)', 'relatórios lidos: por região, gênero, idade, instrução, renda e religião.'),
    ('DataTrends 15-17/10 (BR-04454) e 7-9/10 (BR-03576)', 'relatórios lidos: sem cruzamento pelo 1º turno. A rodada de 19-21/10 não foi achada.'),
    ('Instituto França 21-23/10 (BR-04863) e 16-20/10 (BR-07896)', 'relatórios lidos: sem cruzamento pelo 1º turno.'),
    ('Indexa 20-21/10 (BR-02348) e 13-14/10 (BR-04629)', 'os PDFs no static.poder360 são impressões de matérias do Broadcast; cruzam só pelo voto de 2022.'),
    ('Palver 22-24/10 (n 5.000)', 'relatório não achado (nomes do padrão das ondas 7 e 8 dão 404 no static.poder360; busca sem resultado).'),
    ('Colectta 23/10', 'relatório não achado; fica a matéria do F13.'),
    ('AtlasIntel, tracking encerrado às 8h de 25/10', 'cruzamento não publicado (fora da janela pela E1 de qualquer forma).'),
    ('PesqEle do TSE', 'pesqele-divulgacao.tse.jus.br e divulgacandcontas.tse.jus.br responderam 403 (Access Denied) ao curl comum em 31/10; não contornei.'),
]


def faixa(s):
    """D3 do F13: régua do Adendo 21 pela estimativa pontual."""
    if 47 <= s <= 59:
        return 'confere com a urna'
    if 32 <= s <= 44:
        return 'confere com as pesquisas de antes'
    if 44 < s < 47:
        return 'intermediário'
    return 'abaixo das pesquisas de antes' if s < 32 else 'acima da urna'


def faixas_tocadas(lo, hi):
    out = []
    for nome, a, b in (('abaixo das pesquisas de antes', -1e9, 32), ('confere com as pesquisas de antes', 32, 44),
                       ('intermediário', 44, 47), ('confere com a urna', 47, 59), ('acima da urna', 59, 1e9)):
        if hi >= a and lo <= b:
            out.append(nome)
    return out


def peso(chave):
    return sum(VOTOS_1T[g] for g in GRUPOS_COLUNA[chave])


def calcula(f):
    """Copiada do F13 sem mudança (E3)."""
    cols = f['colunas']
    W = [peso(c[1]) for c in cols]
    num = sum(w * c[2] for w, c in zip(W, cols))
    den = sum(w * (c[2] + c[3]) for w, c in zip(W, cols))
    s = 100 * num / den
    cobertura = sum(W) / ELIMINADOS
    frac = (sum(W) / APTOS_1T) if f['amostra_tipo'] == 'eleitores' else (sum(W) / COMP_1T)
    n_grupo = f['n'] * frac
    escolhe = den / sum(W) / 100
    n_ef = n_grupo * escolhe
    p = s / 100
    ep1 = 100 * math.sqrt(p * (1 - p) / n_ef)
    res = dict(s=round(s, 2), faixa=faixa(s), cobertura_dos_eliminados=round(cobertura, 4),
               grupos_cobertos=sorted({g for c in cols for g in GRUPOS_COLUNA[c[1]]}),
               n_grupo_estimado=round(n_grupo, 1), fracao_que_escolhe_finalista=round(escolhe, 3), n_efetivo=round(n_ef, 1))
    for deff in (1, 2):
        ep = ep1 * math.sqrt(deff)
        lo, hi = s - 1.96 * ep, s + 1.96 * ep
        res['deff%d' % deff] = dict(ep=round(ep, 2), ic95=[round(lo, 1), round(hi, 1)], faixas_tocadas=faixas_tocadas(lo, hi))
    nom = [(w, c) for w, c in zip(W, cols) if c[1] in NOMEADAS]
    sens = {}
    if nom and len(nom) < len(cols):
        sa = 100 * sum(w * c[2] for w, c in nom) / sum(w * (c[2] + c[3]) for w, c in nom)
        sens['a_so_colunas_nomeadas'] = dict(s=round(sa, 2), faixa=faixa(sa))
    if f.get('lembranca'):
        lw = [f['lembranca'].get(c[1], 0) for c in cols]
        if sum(lw) > 0:
            sb = 100 * sum(w * c[2] for w, c in zip(lw, cols)) / sum(w * (c[2] + c[3]) for w, c in zip(lw, cols))
            sens['b_pesos_pela_lembranca_da_pesquisa'] = dict(s=round(sb, 2), faixa=faixa(sb), pesos=f['lembranca'])
    if nom:
        sc = sum(100 * c[2] / (c[2] + c[3]) for _, c in nom) / len(nom)
        sens['c_media_simples_das_nomeadas'] = dict(s=round(sc, 2), faixa=faixa(sc))
    res['sensibilidade'] = sens
    if nom:
        for nome, U in (('bweb', URNA_BWEB), ('amostra_T37', URNA_AMOSTRA)):
            ws = [(VOTOS_1T[c[1]], U[c[1]][0]) for _, c in nom]
            res['urna_mesmas_colunas_' + nome] = round(sum(w * u for w, u in ws) / sum(w for w, _ in ws), 2)
    res['por_coluna'] = [dict(coluna=c[0], representa=GRUPOS_COLUNA[c[1]], L=c[2], F=c[3],
                              fatia_L=round(100 * c[2] / (c[2] + c[3]), 1), peso_votos_1T=w) for w, c in zip(W, cols)]
    return res


def ep_bases(f):
    """E3: erro descritivo com as bases publicadas de cada coluna (sem efeito de desenho), mesma combinação de pesos do s."""
    if not f.get('bases'):
        return None
    cols = [c for c in f['colunas'] if c[1] in f['bases']]
    W = [peso(c[1]) for c in cols]
    den = sum(w * (c[2] + c[3]) / 100 for w, c in zip(W, cols))
    v = 0.0
    for w, c in zip(W, cols):
        p = c[2] / (c[2] + c[3])
        ne = f['bases'][c[1]] * (c[2] + c[3]) / 100
        v += (w * (c[2] + c[3]) / 100 / den) ** 2 * p * (1 - p) / ne
    ep = 100 * math.sqrt(v)
    s = calcula(dict(f, colunas=cols))['s']
    return dict(ep=round(ep, 2), ic95=[round(s - 1.96 * ep, 1), round(s + 1.96 * ep, 1)],
                faixas_tocadas=faixas_tocadas(s - 1.96 * ep, s + 1.96 * ep), bases=f['bases'])


def combinado(fontes):
    """Descritivo pós-hoc (como no F13, sem régua): fontes com cobertura de 90% ou mais, confiança alta ou média, pesos 1/ep^2."""
    sel = [x for x in fontes if x['cobertura_dos_eliminados'] >= 0.9 and x['confianca'] in ('alta', 'média')]
    out = {'fontes': [x['id'] for x in sel]}
    for deff in (1, 2):
        ws = [(1 / x['deff%d' % deff]['ep'] ** 2, x['s']) for x in sel]
        W = sum(a for a, _ in ws)
        m = sum(a * b for a, b in ws) / W
        ep = 1 / math.sqrt(W)
        out['deff%d' % deff] = dict(s=round(m, 2), ep=round(ep, 2), ic95=[round(m - 1.96 * ep, 1), round(m + 1.96 * ep, 1)],
                                    faixas_tocadas=faixas_tocadas(m - 1.96 * ep, m + 1.96 * ep))
    # heterogeneidade (Cochran Q com deff 1): as fontes se distinguem entre si além do erro amostral?
    m = out['deff1']['s']
    Q = sum((x['s'] - m) ** 2 / x['deff1']['ep'] ** 2 for x in sel)
    Q2 = Q / 2
    out['heterogeneidade_deff1'] = dict(Q=round(Q, 1), gl=len(sel) - 1, p=round(chi2_sf(Q, len(sel) - 1), 4))
    out['heterogeneidade_deff2'] = dict(Q=round(Q2, 1), gl=len(sel) - 1, p=round(chi2_sf(Q2, len(sel) - 1), 4))
    return out


def por_grupo(todas):
    """Descritivo pós-hoc: fatia de Lula por eliminado, em todas as rodadas (A e B) que o separam, contra a urna."""
    out = {}
    for g in ('Cury', 'Renan', 'Caiado', 'Zema'):
        vals = [(x['id'], c['fatia_L']) for x in todas for c in x['por_coluna'] if c['representa'] == [g]]
        if not vals:
            continue
        v = sorted(b for _, b in vals)
        med = v[len(v) // 2] if len(v) % 2 else (v[len(v) // 2 - 1] + v[len(v) // 2]) / 2
        out[g] = dict(n_rodadas=len(v), minimo=v[0], mediana=round(med, 1), maximo=v[-1], urna_bweb=URNA_BWEB[g][0],
                      urna_conferente_F13=URNA_CONFERENTE_F13[g], urna_menos_mediana=round(URNA_BWEB[g][0] - med, 1), rodadas=vals)
    return out


def chi2_sf(x, gl):
    """P(Qui-quadrado com gl graus > x), gl inteiro (forma fechada)."""
    h = x / 2.0
    if gl % 2 == 0:
        return math.exp(-h) * sum(h ** k / math.factorial(k) for k in range(gl // 2))
    s = math.erfc(math.sqrt(h))
    for k in range(1, (gl + 1) // 2):
        s += math.exp(-h) * h ** (k - 0.5) / math.gamma(k + 0.5)
    return s


METODO = {'PoderData': 'telefone', 'Nexus': 'telefone', 'Ipespe': 'telefone', 'Meio/Ideia': 'telefone',
          'AtlasIntel': 'online', 'Palver': 'online', 'Datafolha': 'presencial', 'Quaest': 'presencial', 'Colectta': 'presencial'}
F13_JSON = __import__('os').path.join(__import__('os').path.dirname(__import__('os').path.abspath(__file__)), '..', 'resultados',
                                      'F13_pesquisas_independentes.json')


def todas_as_rodadas(o):
    """Pós-hoc: F17 (A, B, Nexus 10-12 corrigido) mais as referências do F13 que o F17 não repete. Lê só o JSON do F13 do repositório."""
    f13 = json.load(open(F13_JSON))
    ja = {x['id'] for x in o['grupo_A'] + o['grupo_B'] + o['conferencia_F13']}
    out = [dict(id=x['id'], instituto=x['instituto'], s=x['s'], ep1=x['deff1']['ep'], cob=x['cobertura_dos_eliminados'],
                confianca=x['confianca'], por_coluna=x['por_coluna'], origem='F17') for x in o['grupo_A'] + o['grupo_B'] + o['conferencia_F13']]
    for x in f13['referencias'] + f13['fontes']:
        if x['id'] in ja:
            continue
        out.append(dict(id=x['id'], instituto=x['instituto'], s=x['s'], ep1=x['deff1']['ep'], cob=x['cobertura_dos_eliminados'],
                        confianca=x['confianca'], por_coluna=x['por_coluna'], origem='F13'))
    return out


def por_metodo(rodadas):
    """Pós-hoc, descritivo: média 1/ep^2 por método de coleta, só cobertura de 90% ou mais."""
    out = {}
    for m in ('online', 'telefone', 'presencial'):
        sel = [x for x in rodadas if x['cob'] >= 0.9 and METODO[[k for k in METODO if x['instituto'].startswith(k)][0]] == m]
        W = sum(1 / x['ep1'] ** 2 for x in sel)
        mm = sum(x['s'] / x['ep1'] ** 2 for x in sel) / W
        ep = 1 / math.sqrt(W)
        out[m] = dict(n_rodadas=len(sel), s=round(mm, 2), ep_deff1=round(ep, 2), ic95=[round(mm - 1.96 * ep, 1), round(mm + 1.96 * ep, 1)],
                      minimo=min(x['s'] for x in sel), maximo=max(x['s'] for x in sel),
                      rodadas=sorted([(x['id'], x['s']) for x in sel], key=lambda t: t[1]))
    a, b = out['online'], out['telefone']
    out['online_menos_telefone'] = dict(dif=round(a['s'] - b['s'], 2), z=round((a['s'] - b['s']) / math.hypot(a['ep_deff1'], b['ep_deff1']), 2))
    c = out['presencial']
    out['online_menos_presencial'] = dict(dif=round(a['s'] - c['s'], 2), z=round((a['s'] - c['s']) / math.hypot(a['ep_deff1'], c['ep_deff1']), 2))
    return out


def br(x, casas=1):
    return (('%.' + str(casas) + 'f') % x).replace('.', ',')


def main(saida_json, saida_txt):
    out = dict(teste='F17 do Adendo 22: relatórios completos das pesquisas finais', data='31/10/2026',
               registro='PRE-REGISTRO-2026-10-26.md, Adendo 22, commit f12121e (31/10/2026 14:52:48 UTC)',
               regua='a do F13: confere com a urna 47 a 59; confere com as pesquisas de antes 32 a 44; intermediário entre 44 e 47',
               decisoes_antes='docstring deste script (E1 a E10); cópia em /home/user/trabalho-eleicao/adendo22/F17_scripts/'
                              'decisoes_antes_de_buscar.py, sha256 e5ee38243e3fe7a2535e1df6ae56a553b09c55d62f377b7065134cec3f0291e3, '
                              '31/10/2026 14:56:19 UTC',
               urna=dict(por_grupo_bweb=URNA_BWEB, por_grupo_amostra_T37=URNA_AMOSTRA, todos_os_eliminados_bweb=URNA_TODOS,
                         conferente_F13=URNA_CONFERENTE_F13),
               grupo_A=[], grupo_B=[], conferencia_F13=[], conferidas_iguais_ao_F13=[dict(rodada=a, situacao=b) for a, b in CONFERIDAS_IGUAIS],
               quaest_blog_baixa=QUAEST_BLOG, sem_cruzamento=[dict(fonte=a, situacao=b) for a, b in SEM_CRUZAMENTO])
    for f in FONTES:
        r = calcula(f)
        item = {k: v for k, v in f.items() if k != 'colunas'}
        item.update(r)
        eb = ep_bases(f)
        if eb:
            item['erro_com_bases_publicadas'] = eb
        if f.get('agregado_publicado'):
            nome, L, F = f['agregado_publicado']
            sa = 100 * L / (L + F)
            item['agregado_publicado'] = dict(coluna=nome, L=L, F=F, s=round(sa, 2), faixa=faixa(sa))
        {'A': out['grupo_A'], 'B': out['grupo_B'], 'conferencia': out['conferencia_F13']}[f['grupo']].append(item)
    qb = 100 * QUAEST_BLOG['L'] / (QUAEST_BLOG['L'] + QUAEST_BLOG['F'])
    out['quaest_blog_baixa']['s'] = round(qb, 2)
    out['quaest_blog_baixa']['faixa_nao_contada'] = faixa(qb)
    resumo = {}
    for g in ('A', 'B'):
        lst = out['grupo_' + g]
        reg = [x for x in lst if x['confianca'] in ('alta', 'média')]
        cont, cont90 = {}, {}
        for x in reg:
            cont[x['faixa']] = cont.get(x['faixa'], 0) + 1
            if x['cobertura_dos_eliminados'] >= 0.9:
                cont90[x['faixa']] = cont90.get(x['faixa'], 0) + 1
        resumo['grupo_' + g] = dict(fontes_com_regua=len(reg), por_faixa=cont, por_faixa_cobertura_90=cont90,
                                    novas=[x['id'] for x in lst if not x['status'].startswith('do F13')],
                                    valores=[(x['id'], x['s'], x['faixa'], round(x['cobertura_dos_eliminados'], 2), x['confianca']) for x in lst])
    resumo['combinado_A_pos_hoc'] = combinado(out['grupo_A'])
    resumo['combinado_B_pos_hoc'] = combinado(out['grupo_B'])
    resumo['por_grupo_A_e_B'] = por_grupo(out['grupo_A'] + out['grupo_B'])
    tod = todas_as_rodadas(out)
    resumo['por_grupo_todas_as_rodadas_F13_e_F17'] = por_grupo([dict(id=x['id'], por_coluna=x['por_coluna']) for x in tod])
    resumo['por_metodo_todas_as_rodadas_pos_hoc'] = por_metodo(tod)
    A = out['grupo_A']
    novas_A = [x['id'] for x in A if x['status'].startswith('novo')]
    resumo['novas_A'] = novas_A
    resumo['veredito'] = ('Pela letra: achados relatórios completos com o cruzamento de %d rodadas que o F13 não tinha (%d do grupo A, de 20 a 24/10, '
                          'e %d do grupo B, anteriores), mais o relatório da AtlasIntel 18-23/10 que substitui a matéria. Grupo A, %d fontes com '
                          'régua: %s.' % (len(novas_A) + len(out['grupo_B']), len(novas_A),
                                         len(out['grupo_B']), resumo['grupo_A']['fontes_com_regua'],
                                         '; '.join('%s %s%% (%s)' % (x['id'], br(x['s']), x['faixa']) for x in A)))
    out['resumo'] = resumo
    out['leitura'] = LEITURA
    out['limites'] = LIMITES
    out['pistas'] = PISTAS
    json.dump(out, open(saida_json, 'w'), ensure_ascii=False, indent=1)
    escrever_txt(out, saida_txt)


def linha_fonte(w, x):
    w('  %s | %s | campo %s | %s | n %s | %s | confiança %s' % (
        x['id'], x['instituto'], x['campo'], x['registro'], format(x['n'], ',').replace(',', '.'), x['metodo'], x['confianca']))
    w('      situação: %s' % x['status'])
    for c in x['por_coluna']:
        w('      %-36s L %5s  F %5s  fatia L %5s%%  (representa %s; %s votos no 1º turno)' % (
            c['coluna'], br(c['L']), br(c['F']), br(c['fatia_L']), '+'.join(c['representa']),
            format(c['peso_votos_1T'], ',').replace(',', '.')))
    d1, d2 = x['deff1'], x['deff2']
    w('      s = %s%% -> %s. Cobertura %s%%. n do grupo ~%s, n efetivo ~%s. ep %s (IC95 %s a %s) com efeito de desenho 1; ep %s '
      '(IC95 %s a %s) com 2.' % (br(x['s']), x['faixa'].upper(), br(100 * x['cobertura_dos_eliminados'], 0), br(x['n_grupo_estimado'], 0),
                                 br(x['n_efetivo'], 0), br(d1['ep']), br(d1['ic95'][0]), br(d1['ic95'][1]), br(d2['ep']),
                                 br(d2['ic95'][0]), br(d2['ic95'][1])))
    if x.get('erro_com_bases_publicadas'):
        e = x['erro_com_bases_publicadas']
        w('      erro com as bases publicadas (E3, descritivo): ep %s, IC95 %s a %s; toca: %s.' % (
            br(e['ep']), br(e['ic95'][0]), br(e['ic95'][1]), '; '.join(e['faixas_tocadas'])))
    for k, v in x['sensibilidade'].items():
        w('      sensibilidade %s: %s%% (%s)' % (k, br(v['s']), v['faixa']))
    if x.get('agregado_publicado'):
        a = x['agregado_publicado']
        w('      agregado publicado pelo instituto (%s): L %s F %s -> %s%% (%s)' % (a['coluna'], br(a['L']), br(a['F']), br(a['s']), a['faixa']))
    if 'urna_mesmas_colunas_bweb' in x:
        w('      urna com as mesmas colunas nomeadas e os mesmos pesos: %s%% (bweb), %s%% (amostra do T37)' % (
            br(x['urna_mesmas_colunas_bweb']), br(x['urna_mesmas_colunas_amostra_T37'])))
    if x.get('nota'):
        w('      nota: ' + x['nota'])
    w('      lido em: ' + x['arquivo'])
    w('      fonte: ' + x['fonte'])


def escrever_txt(o, caminho):
    L = []
    w = L.append
    R = o['resumo']
    A, B = o['grupo_A'], o['grupo_B']
    w('F17 do Adendo 22: relatórios completos das pesquisas finais. Rodado em 31/10/2026.')
    w('Script: scripts/analisar_F17.py. Números: resultados/F17_relatorios_pesquisas.json.')
    w('')
    w('Critério registrado (Adendo 22, commit f12121e, antes de rodar):')
    w('  "Procurar os relatórios completos (PDF ou tabela) com o voto no 2º turno por voto no 1º turno das pesquisas de 20 a 24/10')
    w('  (Quaest, Datafolha, AtlasIntel, Nexus, CNT/MDA, Palver, Ipespe, Gerp e outras) e as rodadas anteriores que faltaram no F13.')
    w('  Mesma conta e mesma régua do F13." Régua do F13: confere com a urna 47 a 59; confere com as pesquisas de antes 32 a 44;')
    w('  intermediário entre 44 e 47; fora disso, "abaixo das pesquisas de antes" (< 32) ou "acima da urna" (> 59).')
    w('  Decisões onde o registro não fixa (E1 a E10, desvios declarados): docstring do script, escritas às 14h56 UTC de 31/10, antes')
    w('  de qualquer busca; cópia com sha256 em /home/user/trabalho-eleicao/adendo22/F17_scripts/decisoes_antes_de_buscar.*.')
    w('  Grupo A = campo terminando de 20 a 24/10; grupo B = campo terminando de 5 a 19/10 e ausente do F13. Tomadas depois de começar')
    w('  a ler (P1 a P5, também desvios): conferência das rodadas do F13 com relatório; blog da Quaest como confiança baixa; leitura')
    w('  das cores nos gráficos renderizados; agregados publicados só como sensibilidade; média combinada, heterogeneidade, divisão')
    w('  por método e fatia por candidato como descritivos pós-hoc, sem régua.')
    w('')
    w('VEREDITO PELA LETRA (descritivo; o F17 não tem critério de sinal)')
    w('  Relatórios completos achados com o cruzamento: %d rodadas novas (%d no grupo A, %d no grupo B) e o relatório da AtlasIntel' % (
        len(R['novas_A']) + len(B), len(R['novas_A']), len(B)))
    w('  18-23/10, que troca a matéria do F13 (só Renan) pela tabela completa.')
    w('  Grupo A (pesquisas de 20 a 24/10), %d fontes com régua:' % R['grupo_A']['fontes_com_regua'])
    for x in A:
        w('      %-22s s = %5s%%  -> %-34s (cobertura %s%%; %s; %s)' % (
            x['id'], br(x['s']), x['faixa'].upper(), br(100 * x['cobertura_dos_eliminados'], 0), x['confianca'], x['status'].split(' (')[0]))
    w('    Contagem: ' + '; '.join('%s %d' % (k, v) for k, v in sorted(R['grupo_A']['por_faixa'].items())) +
      '. Só cobertura de 90% ou mais: ' + '; '.join('%s %d' % (k, v) for k, v in sorted(R['grupo_A']['por_faixa_cobertura_90'].items())) + '.')
    w('  Grupo B (rodadas anteriores que faltaram no F13), %d fontes com régua (régua circular aqui, E2):' % R['grupo_B']['fontes_com_regua'])
    for x in B:
        w('      %-22s s = %5s%%  -> %-34s (cobertura %s%%; %s)' % (
            x['id'], br(x['s']), x['faixa'].upper(), br(100 * x['cobertura_dos_eliminados'], 0), x['confianca']))
    w('    Contagem: ' + '; '.join('%s %d' % (k, v) for k, v in sorted(R['grupo_B']['por_faixa'].items())) + '.')
    w('  Sem cruzamento publicado (relatório lido ou não achado): Quaest 23-24/10, Datafolha 23-24/10, CNT/MDA, Gerp, Futura, Real Time,')
    w('  Alfa, Vox, DataTrends, Verità, Instituto França, Indexa, Palver 22-24/10 (lista e motivo no item 4).')
    w('')
    w('1. Grupo A, por fonte (fatia de Lula entre os que escolheram um finalista; pesos = votos oficiais do 1º turno de cada grupo, D2 do F13)')
    for x in A:
        linha_fonte(w, x)
    w('')
    w('2. Grupo B, por fonte')
    for x in B:
        linha_fonte(w, x)
    w('')
    w('3. Conferência das rodadas do F13 com os relatórios achados (P1, descritivo)')
    for x in o['conferencia_F13']:
        linha_fonte(w, x)
    for c in o['conferidas_iguais_ao_F13']:
        w('  %s: %s' % (c['rodada'], c['situacao']))
    q = o['quaest_blog_baixa']
    w('  Quaest, blog do instituto (confiança baixa, P2): %s; L %d F %d -> %s%% (%s, não contado). Fonte: %s' % (
        q['texto'], q['L'], q['F'], br(q['s']), q['faixa_nao_contada'], q['fonte']))
    w('')
    w('4. Procurado e sem o cruzamento')
    for s_ in o['sem_cruzamento']:
        w('  - %s: %s' % (s_['fonte'], s_['situacao']))
    w('')
    w('5. O que os números significam')
    ca = R['combinado_A_pos_hoc']
    w('  - Média combinada pós-hoc do grupo A (sem régua; %s; pesos 1/ep^2): %s%% (ep %s; IC95 %s a %s) com deff 1; IC95 %s a %s' % (
        ', '.join(ca['fontes']), br(ca['deff1']['s']), br(ca['deff1']['ep']), br(ca['deff1']['ic95'][0]), br(ca['deff1']['ic95'][1]),
        br(ca['deff2']['ic95'][0]), br(ca['deff2']['ic95'][1])))
    h1, h2 = ca['heterogeneidade_deff1'], ca['heterogeneidade_deff2']
    w('    com deff 2. As fontes discordam entre si além do erro amostral: Q de Cochran %s com %d graus de liberdade (p %s) com deff 1;' % (
        br(h1['Q']), h1['gl'], br(h1['p'], 4)))
    w('    Q %s (p %s) com deff 2. Uma média única esconde essa discordância.' % (br(h2['Q']), br(h2['p'], 3)))
    cb = R['combinado_B_pos_hoc']
    w('  - Mesma conta no grupo B (%s): %s%% (IC95 %s a %s, deff 1); Q %s com %d gl (p %s).' % (
        ', '.join(cb['fontes']), br(cb['deff1']['s']), br(cb['deff1']['ic95'][0]), br(cb['deff1']['ic95'][1]),
        br(cb['heterogeneidade_deff1']['Q']), cb['heterogeneidade_deff1']['gl'], br(cb['heterogeneidade_deff1']['p'], 4)))
    pm = R['por_metodo_todas_as_rodadas_pos_hoc']
    w('  - Por método de coleta, todas as rodadas com cruzamento do F13 e do F17 (pós-hoc, sem régua; cobertura de 90% ou mais; Nexus')
    w('    10-12/10 corrigido; pesos 1/ep^2 com deff 1):')
    for m in ('online', 'telefone', 'presencial'):
        v = pm[m]
        w('      %-10s %2d rodadas, de %s a %s; média %s%% (IC95 %s a %s): %s' % (
            m, v['n_rodadas'], br(v['minimo']), br(v['maximo']), br(v['s']), br(v['ic95'][0]), br(v['ic95'][1]),
            ', '.join('%s %s' % (a, br(b)) for a, b in v['rodadas'])))
    w('    Online menos telefone: %s pontos (z %s); online menos presencial: %s pontos (z %s).' % (
        br(pm['online_menos_telefone']['dif']), br(pm['online_menos_telefone']['z'], 2),
        br(pm['online_menos_presencial']['dif']), br(pm['online_menos_presencial']['z'], 2)))
    w('  - Por candidato (pós-hoc; urna no bweb, e a do conferente do F13 entre parênteses):')
    for rot, chave in (('só as rodadas de A e B', 'por_grupo_A_e_B'), ('todas as rodadas do F13 e do F17', 'por_grupo_todas_as_rodadas_F13_e_F17')):
        w('    %s:' % rot)
        for g, v in R[chave].items():
            w('      %-7s %2d rodadas, de %s a %s, mediana %s; urna %s (%s); urna menos mediana %s pontos (%s com a urna do conferente)' % (
                g, v['n_rodadas'], br(v['minimo']), br(v['maximo']), br(v['mediana']), br(v['urna_bweb']), br(v['urna_conferente_F13']),
                br(v['urna_menos_mediana']), br(v['urna_conferente_F13'] - v['mediana'])))
    for t in LEITURA:
        w(t)
    w('')
    w('6. Limites')
    for t in LIMITES:
        w(t)
    w('')
    w('7. Pistas (fora do critério)')
    for k, t in enumerate(PISTAS, 1):
        w('  %d. %s' % (k, t))
    open(caminho, 'w').write('\n'.join(L) + '\n')


LEITURA = [
    '  - Leitura: os relatórios completos mudam o retrato do F13. O F13 tinha três fontes finais, nenhuma na faixa da urna. Com os',
    '    relatórios, o grupo A tem nove fontes com cruzamento: duas na faixa da urna (AtlasIntel 18-23/10, 50,3, agora com todas as',
    '    colunas; Palver 18-20/10, 51,5), cinco na faixa das pesquisas de antes, uma intermediária (Colectta) e uma abaixo (Ipespe',
    '    20-22/10, 28,0). As pesquisas não formam um bloco único: discordam entre si mais do que o erro amostral explica com deff 1, e',
    '    a discordância segue o método de coleta. As duas de recrutamento online calibrado ficam perto do que a urna implica; as de',
    '    telefone e as presenciais ficam de 28 a 45. A faixa "pesquisas de antes" (32 a 44) do registro descreve as de telefone e as',
    '    presenciais, não todas.',
    '  - Isso pesa contra ler a diferença urna x pesquisa como prova de votos movidos: se parte das pesquisas, com outro método, mede',
    '    o eleitor dos eliminados perto da urna, a diferença pode estar no método de quem mede (cobertura do telefone, quem responde,',
    '    lembrança errada do voto no 1º turno). Também não é prova do contrário: as pesquisas online não são probabilísticas, são',
    '    calibradas pelo voto declarado no 1º turno, e a AtlasIntel tinha 43 nas duas rodadas anteriores (o salto para 50,3 vem do',
    '    eleitor de Caiado, de 26,0 para 54,0). Nenhuma medida feita depois do voto existe para separar as leituras.',
    '  - O gradiente do F13 (distância urna x pesquisa crescendo de Cury para Zema: 9,5; 13,2; 15,9; 23,5) enfraquece com mais',
    '    rodadas: com todas as rodadas do F13 e do F17, 10,7; 13,1; 13,4; 19,6 (urna do bweb) ou 11,1; 10,9; 11,8; 15,2 (urna do',
    '    conferente). Para Zema sobram cinco rodadas, uma delas o Nexus 10-12/10 corrigido (0% de Lula), e a lembrança do voto em',
    '    Zema nas pesquisas é inflada (Ideia: 1,2% da amostra, contra 0,26% dos votantes na urna).',
    '  - Poder: cada fonte sozinha tem erro-padrão de 3 a 6 pontos (deff 1) e não separa 40 de 50; a Palver avisa que as bases',
    '    efetivas são de 29 a 63 entrevistas por coluna. O que tem força é o conjunto: a média do grupo A (43,6) fica abaixo de 47',
    '    com deff 1 (IC95 41,0 a 46,2) e encosta em 47,3 com deff 2; a separação por método (online 48,1; telefone 38,0; presencial',
    '    40,2) tem z de 5,4 e 3,3 com deff 1 (3,8 e 2,3 com deff 2).',
]
LIMITES = [
    '  - Pesquisa de véspera mede intenção, não voto; quem decidiu no dia, quem não ia votar e votou (o comparecimento subiu quase',
    '    5 milhões, segundo a Quaest em 30/10) e quem mentiu na lembrança do 1º turno ficam de fora.',
    '  - "Eleitor de Cury" na pesquisa é quem diz ter votado em Cury. A lembrança erra: Ideia tem Zema com 1,2% da amostra (cerca',
    '    de 5 vezes a fatia real), Verità tem Caiado com 0,9% da amostra (cerca de metade da fatia real). Coluna com lembrança errada',
    '    mistura outro tipo de eleitor.',
    '  - A classificação usa a estimativa pontual; quase todos os intervalos tocam duas ou três faixas.',
    '  - Os cruzamentos de Datafolha (agregado dos quatro) e de Palver (três candidatos) cobrem 94% a 97% dos votos dos eliminados.',
    '  - Agrupamento por método é pós-hoc e confunde método com instituto (online = AtlasIntel e Palver; telefone = PoderData, Nexus,',
    '    Ipespe, Ideia; presencial = Datafolha, Quaest, Colectta); rodadas do mesmo instituto não são independentes no viés.',
    '  - A urna aqui é regressão ecológica entre seções do mesmo local (limite já escrito no L4 e no F13).',
    '  - Regra do Adendo 18: nenhuma eleição anterior foi usada como régua.',
]
PISTAS = [
    'Método de coleta separa as pesquisas: online (AtlasIntel 18-23/10 50,3; Palver 18-20/10 51,5; Palver 10-13/10 52,7) contra '
    'telefone (Ipespe 28,0 a 33,0; PoderData 30,9 a 44,5; Nexus 39,6 a 43,3; Ideia 34,3) e presencial (Datafolha 35,6 a 41,0; Quaest '
    '40,6 e 41,9; Colectta 45,4). Q de Cochran do grupo A 25,4 com 8 gl (p 0,001) com deff 1, mas p 0,12 com deff 2. Vale pedir aos '
    'institutos as bases e os pesos por coluna; com isso dá para testar se a diferença é do método ou da calibração pelo 1º turno.',
    'AtlasIntel: 43,0 (3-8/10), 43,3 (13-18/10), 50,3 (18-23/10). O salto vem do eleitor de Caiado: 32,9; 26,0; 54,0 de '
    'fatia de Lula. A coluna de Caiado oscila em todos os institutos (Nexus 24,0 em 16-18/10 e 42,6 em 23-24/10; Palver 36,5 e 50,0; '
    'PoderData 40,5; 37,5; 29,2; 38,0; 39,5 nas cinco rodadas de 10 a 24/10). É a coluna menos estável entre institutos e entre rodadas.',
    'Nexus 10-12/10 no F13 estava errado: o 12% atribuído a Lula entre eleitores de Zema é branco/nulo no gráfico (Lula 0), e o '
    '"32 x 45" que o F13 rotulou como "outros candidatos" é o agregado de todos os eliminados. Corrigido: 43,3 (F13: 37,9), mesma '
    'faixa. A mediana de Zema do F13 (12,6) usava esse 13,0 errado.',
    'Ipespe 20-22/10 dá 28,0 (Renan 13 x 38; Caiado 19 x 64), a fonte mais baixa; as três rodadas do Ipespe ficam entre 28 e 33, '
    'sempre abaixo dos outros institutos de telefone. Registro no PDF: BR-04350/2026 (a imprensa grafou BR-00223, da rodada anterior).',
    'Ideia 15-19/10: Renan 9,1 x 90,9 (33 entrevistas). É o valor mais extremo de todas as rodadas para Renan (as outras vão de 25,5 '
    'a 50,0). Com bases tão pequenas, uma coluna sozinha não serve para nada; o agregado do instituto (31,8 x 58,1) dá 35,4.',
    'Quaest 23-24/10 (BR-09158): o relatório da véspera existe e fica atrás de um cadastro com nome e e-mail no site da Quaest '
    '(quaest.com.br/relatorios-quaest). Basta o Léo preencher; é a principal fonte final que falta. A Quaest escreveu em 30/10 que, '
    'na véspera, os que faltaram no 1º turno eram mais jovens, mais pobres e mais pró-Lula, e que a parcela deles que dizia que ia '
    'votar subiu 12 pontos em uma semana.',
    'Gerp 22-24/10 usa a "migração do voto declarado no 1º turno" numa projeção (Flávio 51% "corrigida pela urna do 1º turno") e '
    'diz que as perguntas sobre o voto no 1º turno ficam fora do relatório. O dado existe no instituto; pedir.',
    'Matérias com erro de cópia: BPMoney e SpaceMoney (21/10) dão Quaest 17-20/10 com Caiado 25 x 51, mas o "antes" delas é o de '
    'Renan; DGABC e Diario de Pernambuco (mesmo texto) dão 21 x 57, que o F13 usou. Sem o relatório não dá para fechar.',
    'Blog da Quaest (22/10) dá o agregado dos eliminados, sem dizer a rodada, como 37 Lula x 43 Flávio (46,3). Com as colunas por '
    'candidato da rodada de 17-20/10 (matéria), pesos oficiais dão 41,9 e pesos iguais dão 40,0; nenhum peso razoável chega a 46,3. '
    'Ou a rodada é outra, ou o agregado inclui Zema e outros com fatia alta, ou uma das fontes está errada. Só o relatório fecha.',
    'PesqEle do TSE respondeu 403 ao curl comum (31/10); num navegador comum, os registros BR-09158 (Quaest), BR-09540 (Datafolha), '
    'BR-09327 (Gerp), BR-02136 (CNT/MDA) e BR-04612/BR-08028 (Palver) mostram o questionário e o plano amostral, que dizem se o '
    'cruzamento foi perguntado.',
]

if __name__ == '__main__':
    main(sys.argv[1], sys.argv[2])
