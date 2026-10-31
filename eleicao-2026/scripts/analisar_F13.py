"""F13 do Adendo 21 (PRE-REGISTRO-2026-10-26.md, commit 913af7a): pesquisas independentes da urna.

Texto registrado (letra):
  "Pesquisas feitas depois da eleição com a lembrança do voto nos dois turnos, boca de urna do dia 25/10 e os relatórios finais
  completos (com tabelas cruzadas) dos institutos. Para cada uma: fatia de Lula entre os eleitores dos eliminados que escolheram um
  finalista. Descritivo, com a régua: 'confere com a urna' se ficar a 5 pontos ou menos de 52% a 54%; 'confere com as pesquisas de
  antes' se ficar entre 32% e 44%; entre os dois, intermediário."

Decisões tomadas ANTES de buscar e de calcular (31/10/2026, 11h49 UTC), onde o registro não fixa. Cada uma é desvio declarado:

D1. Fontes do F13 (com veredito): (i) pesquisas com campo começando em 26/10/2026 ou depois, que perguntaram o voto lembrado no
    1º e no 2º turno; (ii) boca de urna de 25/10/2026; (iii) a última rodada de cada instituto antes de 25/10 (campo terminando
    entre 21 e 24/10), quando houver relatório completo ou tabela publicada com o voto no 2º turno cruzado pelo voto no 1º.
    Rodadas anteriores (campo terminando até 20/10) entram só como referência descritiva, sem régua: são elas que formam a faixa
    "pesquisas de antes".
D2. Eliminados = todos os candidatos do 1º turno menos 13 e 22. Medida principal:
       s = soma_k w_k L_k / soma_k w_k (L_k + F_k)
    k = colunas publicadas de eleitores de eliminados (por candidato, agregado, ou "outro(s) candidato(s)"); L_k e F_k = % de Lula e
    de Flávio no 2º turno nessa coluna; w_k = votos oficiais do 1º turno dos candidatos que a coluna representa (coluna "outro(s)"
    representa os eliminados que a pesquisa não separou). Coluna que mistura eleitor de eliminado com branco, nulo ou ausente fica
    fora. Se só há o agregado dos eliminados, usa o agregado. Votos oficiais do 1º turno (bweb, candidatos_1t_2026_totais.txt):
    Cury 3.448.569; Renan 2.675.887; Caiado 2.605.148; Zema 326.488; esquerda (Hertz, Edmilson, Rui Costa Pimenta) 80.820;
    demais (Samara, Clariana, Wilson Grassi) 179.835; total 9.316.747.
    Sensibilidades (sem veredito): (a) só as colunas com candidato nomeado (sem "outro(s)"); (b) pesos pela lembrança do 1º turno
    na própria pesquisa, quando publicada; (c) média simples das colunas nomeadas.
D3. Faixas da régua (pela estimativa pontual, sem arredondar): "confere com a urna" se 47 <= s <= 59; "confere com as pesquisas de
    antes" se 32 <= s <= 44; "intermediário" se 44 < s < 47. O registro não diz o que fazer fora disso; fica: s < 32 "abaixo das
    pesquisas de antes"; s > 59 "acima da urna".
D4. Erro amostral (descritivo, não muda a classificação): n do grupo = n da pesquisa x fatia dos eleitores dos eliminados na
    amostra (lembrança publicada; sem ela, a fatia oficial: 9.316.747 / 158.744.977 aptos = 5,87% para amostra de eleitores,
    9.316.747 / 125.275.833 = 7,44% para amostra só de quem votou); n efetivo = n do grupo x (L + F) / 100;
    ep = raiz(s(1 - s) / n efetivo) x raiz(efeito de desenho), com efeito de desenho 1 e 2. Relata o intervalo de 95% e em quantas
    faixas da régua ele toca.
D5. Pesquisa pós-eleição: relata também, como medida da própria pesquisa, a lembrança contra o oficial (2º turno: fatia de Lula nos
    válidos lembrados contra 51,79%; 1º turno: fatias lembradas contra as oficiais nos válidos: Flávio 47,03%, Lula 45,16%,
    eliminados 7,81%). s não é corrigido por isso (nada registrado); a diferença é relatada ao lado.
D6. Boca de urna: s só se houver cruzamento pelo voto no 1º turno. Sem isso, só o total contra a urna, descritivo, sem régua.
D7. Quem deixou de votar ou passou a votar: relatar se alguma pesquisa pós-eleição cruza o comparecimento nos dois turnos, com os
    números, sem critério.
D8. Fonte aceita: número lido no relatório do instituto (PDF ou página) ou em matéria que atribui o número ao instituto com a rodada
    identificada. Confiança alta (relatório primário), média (matéria com ficha) ou baixa (agregador, Wikipedia, rodada inferida).
    Só confiança alta ou média recebe a régua; baixa fica descritiva.
D9. Resumo do F13: contagem das fontes por faixa. Sem nenhuma fonte elegível com cruzamento: "SEM DADOS" pela letra.
D10. Regra do Adendo 18: nenhuma eleição anterior como régua. O viés de lembrança é medido só dentro da própria pesquisa (D5).
D11. Arquivos baixados: cada download numa pasta nova e vazia em /home/user/trabalho-eleicao/adendo21/F13_dl_<nome>/; textos
    extraídos com pdftotext; este script não lê nada dessas pastas, só a tabela abaixo, digitada com a fonte de cada número.

Uso: python3 -I analisar_F13.py <saida.json> <saida.txt>
"""
import json, math, sys

# ------------------------------------------------------------------ urna (números oficiais e regressões já rodadas)
VOTOS_1T = {'Cury': 3448569, 'Renan': 2675887, 'Caiado': 2605148, 'Zema': 326488, 'esquerda': 80820, 'demais': 179835}
ELIMINADOS = sum(VOTOS_1T.values())            # 9.316.747
APTOS_1T = 158744977
COMP_1T = 125275833
VALIDOS_1T = 119300788
OFICIAL_2T_L = 51.79                          # % de Lula nos válidos do 2º turno (64.256.232 / 124.082.273)
OFICIAL_1T = {'Flavio': 47.03, 'Lula': 45.16, 'eliminados': 7.81}
# fatia de Lula entre os eleitores de cada grupo que a urna põe num finalista (regressão do T8 com grupos, mesmo local):
# resultados/T7_T14_bweb.json, 2026/T37/urna/por_grupo (bweb inteiro) e urna_amostra_conferencia (amostra do T37).
URNA_BWEB = {'Cury': (59.64, 0.27), 'Renan': (54.22, 0.29), 'Caiado': (48.80, 0.31), 'Zema': (36.10, 0.86)}
URNA_AMOSTRA = {'Cury': (54.00, 2.96), 'Renan': (49.31, 3.07), 'Caiado': (54.18, 3.31), 'Zema': (41.82, 8.37)}
URNA_TODOS_ELIMINADOS = {'bweb, todos os eliminados num grupo (L5, so_urna_regressao)': (54.07, 0.17),
                         'amostra do T37, quatro grupos somados pelos votos do 1º turno': (52.20, 1.74)}

# o que cada coluna publicada representa (D2)
GRUPOS_COLUNA = {
    'Cury': ['Cury'], 'Renan': ['Renan'], 'Caiado': ['Caiado'], 'Zema': ['Zema'],
    'outro_sem_zema': ['esquerda', 'demais'],                         # coluna "outro(s)" quando Zema já está separado
    'outro_com_zema': ['Zema', 'esquerda', 'demais'],                 # coluna "outro(s)" quando Zema não está separado
    'outro_nexus': ['Cury', 'Renan', 'esquerda', 'demais'],           # Nexus 10-12/10: "outros candidatos" sem Zema e Caiado
    'agregado_4': ['Cury', 'Renan', 'Caiado', 'Zema'],                # Datafolha: "Cury, Renan, Caiado ou Zema"
}
NOMEADAS = {'Cury', 'Renan', 'Caiado', 'Zema'}

# ------------------------------------------------------------------ fontes
# cada coluna: (nome, chave em GRUPOS_COLUNA, L %, F %). amostra_tipo: 'eleitores' (inclui quem não votou) ou 'votantes'.
FONTES = [
    # ---------------- F13 (iii): última rodada de cada instituto, campo terminando entre 21 e 24/10, com cruzamento publicado
    dict(id='PoderData 23-24/10', papel='F13', instituto='PoderData', campo='23 e 24/10/2026', registro='BR-02828/2026',
         n=4000, metodo='telefone IVR', amostra_tipo='eleitores', confianca='alta',
         fonte='https://static.poder360.com.br/uploads/2026/10/Relatorio-PoderData-Eleitoral-24out26-1.pdf',
         arquivo='/home/user/trabalho-eleicao/adendo21/F13_dl_poderdata24out/pd24out.pdf (sha256 9c41cf86fa7c7e72aee800c181781ce226acd369f680861301330fd235f38450), p. 10',
         colunas=[('Augusto Cury', 'Cury', 29, 58), ('Renan Santos', 'Renan', 33, 43), ('Ronaldo Caiado', 'Caiado', 30, 46),
                  ('Outro candidato', 'outro_com_zema', 15, 65)],
         nota='tabela "Voto no 1º turno"; branco/nulo e não sabe: Cury 11 e 2, Renan 19 e 5, Caiado 20 e 4, Outro 0 e 20; '
              'ponderação inclui "resultado do 1º turno"; não publica o tamanho das subamostras nem a lembrança por candidato'),
    dict(id='Colectta 23/10', papel='F13', instituto='Colectta (Brazil Economy)', campo='23/10/2026', registro='BR-05601/2026',
         n=3000, metodo='presencial, 101 municípios', amostra_tipo='eleitores', confianca='média',
         fonte='https://brazileconomy.com.br/mais-lidas/2026/10/lula-tem-503-dos-votos-validos-e-flavio-497-aponta-pesquisa-brazil-economycolectta/',
         arquivo='matéria de 24/10/2026 10h49 (atualizada 26/10 21h47), lida por WebFetch em 31/10/2026; trechos literais no JSON',
         colunas=[('Augusto Cury', 'Cury', 33.4, 37.5), ('Renan Santos', 'Renan', 30.4, 40.9), ('Ronaldo Caiado', 'Caiado', 30.7, 35.9)],
         nota='"Dos que escolheram Augusto Cury, 37,5% pretendem votar no senador, contra 33,4% em Lula." / "Entre os apoiadores de '
              'Renan Santos, os percentuais são de 40,9% e 30,4%, respectivamente." / "No eleitorado de Ronaldo Caiado, Flávio '
              'registra 35,9%, ante 30,7% do presidente." Sem Zema e sem outros; sem branco/nulo por coluna; relatório não achado'),
    dict(id='AtlasIntel 18-23/10', papel='F13', instituto='AtlasIntel/Bloomberg', campo='18 a 23/10/2026', registro='BR-06380/2026',
         n=4990, metodo='recrutamento digital aleatório', amostra_tipo='eleitores', confianca='média',
         fonte='https://www.bloomberglinea.com.br/brasil/pesquisas-indicam-cenario-acirrado-com-flavio-e-lula-empatados-dentro-da-margem-de-erro/',
         arquivo='matéria da Bloomberg Línea de 24/10/2026 22h53, lida por WebFetch em 31/10/2026',
         colunas=[('Renan Santos', 'Renan', 30.7, 40.8)],
         nota='"Entre os eleitores de Renan Santos no primeiro turno, 40,8% declaram voto no senador, 30,7% no presidente" '
              '(branco, nulo ou indeciso 28,6%). Só Renan publicado; Cury, Caiado e outros não aparecem; relatório não achado'),
    # ---------------- referência descritiva (rodadas anteriores, já conferidas em resultados/contexto_2t_2026_pesquisa_verificada.json)
    dict(id='PoderData 19-21/10', papel='ref', instituto='PoderData', campo='19 a 21/10', registro='BR-07926/2026', n=4000,
         amostra_tipo='eleitores', confianca='alta', fonte='https://static.poder360.com.br/uploads/2026/10/Relatorio-PoderData-Eleitoral-21out26-2.pdf',
         colunas=[('Cury', 'Cury', 48, 42), ('Renan', 'Renan', 34, 49), ('Caiado', 'Caiado', 30, 49), ('Outro', 'outro_com_zema', 20, 70)]),
    dict(id='Quaest 17-20/10', papel='ref', instituto='Quaest', campo='17 a 20/10', registro='BR-08535/2026', n=2154,
         amostra_tipo='eleitores', confianca='média',
         fonte='https://www.diariodepernambuco.com.br/politica/2026/10/11727201-quaest-48-dos-eleitores-de-augusto-cury-migram-para-lula-e-33-para-flavio.html',
         colunas=[('Cury', 'Cury', 48, 33), ('Renan', 'Renan', 25, 51), ('Caiado', 'Caiado', 21, 57)]),
    dict(id='AtlasIntel 13-18/10', papel='ref', instituto='AtlasIntel/Bloomberg', campo='13 a 18/10', registro='BR-02418/2026', n=4998,
         amostra_tipo='eleitores', confianca='média',
         fonte='https://www.infomoney.com.br/politica/atlasintel-para-onde-foram-os-votos-de-caiado-renan-zema-e-cury-no-2o-turno/',
         colunas=[('Cury', 'Cury', 52.1, 42.4), ('Renan', 'Renan', 31.9, 33.5), ('Caiado', 'Caiado', 24.5, 69.8),
                  ('Outros (inclui Zema)', 'outro_com_zema', 30.7, 61.3)]),
    dict(id='Ipespe 13-15/10', papel='ref', instituto='Ipespe/Abrapel', campo='13 a 15/10', registro='BR-00223/2026', n=1500,
         amostra_tipo='eleitores', confianca='alta', fonte='https://static.poder360.com.br/uploads/2026/10/pesquisa-ipespe-17out2026.pdf',
         lembranca={'Cury': 2, 'Caiado': 2, 'Renan': 2, 'outro_com_zema': 1},
         colunas=[('Cury', 'Cury', 31, 50), ('Caiado', 'Caiado', 18, 59), ('Renan', 'Renan', 20, 40), ('Outros', 'outro_com_zema', 27, 55)]),
    dict(id='Datafolha 13-14/10', papel='ref', instituto='Datafolha', campo='13 e 14/10', registro='BR-00466/2026', n=2520,
         amostra_tipo='eleitores', confianca='alta', fonte='https://static.poder360.com.br/uploads/2026/10/datafolha-15out2026-pesquisa-nacional.pdf',
         colunas=[('Cury, Renan, Caiado ou Zema', 'agregado_4', 27, 46)]),
    dict(id='Quaest 10-13/10', papel='ref', instituto='Quaest', campo='10 a 13/10', registro='BR-08729/2026', n=2154,
         amostra_tipo='eleitores', confianca='média',
         fonte='https://www.opovo.com.br/noticias/politica/eleicoes/2026/10/16/quaest-traz-transferencia-de-voto-no-2-turno-a-flavio-e-lula.html',
         colunas=[('Cury', 'Cury', 34, 30), ('Renan', 'Renan', 14, 40), ('Caiado', 'Caiado', 23, 42), ('Outros', 'outro_com_zema', 33, 38)]),
    dict(id='Nexus 10-12/10', papel='ref', instituto='Nexus/BTG', campo='10 a 12/10', registro='BR-07997/2026', n=2002,
         amostra_tipo='eleitores', confianca='média',
         fonte='https://tribunadejundiai.com.br/politica/eleicoes-2026/pesquisa-btg-nexus-flavio-bolsonaro-lula-segundo-turno/',
         colunas=[('Zema', 'Zema', 12, 80), ('Caiado', 'Caiado', 27, 55), ('Outros candidatos', 'outro_nexus', 32, 45)]),
    dict(id='AtlasIntel 3-8/10', papel='ref', instituto='AtlasIntel/Bloomberg', campo='3 a 8/10', registro='BR-03663/2026', n=5026,
         amostra_tipo='eleitores', confianca='média', fonte='https://tvtnews.com.br/?p=805894',
         colunas=[('Cury', 'Cury', 50.4, 38.9), ('Renan', 'Renan', 28.1, 40.3), ('Caiado', 'Caiado', 26.9, 54.9),
                  ('Demais candidatos', 'outro_com_zema', 14.8, 83.4)]),
    dict(id='Ipespe 6-8/10', papel='ref', instituto='Ipespe/Abrapel', campo='6 a 8/10', registro='BR-00933/2026', n=1500,
         amostra_tipo='eleitores', confianca='alta', fonte='https://static.poder360.com.br/uploads/2026/10/pesquisa-ipespe-abrapel-10out2026.pdf',
         lembranca={'Cury': 2, 'Caiado': 2, 'Renan': 2},
         colunas=[('Cury', 'Cury', 29, 50), ('Caiado', 'Caiado', 15, 56), ('Renan', 'Renan', 20, 36), ('Outros', 'outro_com_zema', 40, 40)]),
    dict(id='Datafolha 6-7/10', papel='ref', instituto='Datafolha', campo='6 e 7/10', registro='BR-02949/2026', n=2520,
         amostra_tipo='eleitores', confianca='média',
         fonte='https://www.diariodepernambuco.com.br/politica/2026/10/11726210-datafolha-46-dos-eleitores-de-candidatos-derrotados-no-1-turno-migram-para-flavio-bolsonaro.html',
         colunas=[('Cury, Renan, Caiado ou Zema', 'agregado_4', 32, 46)]),
    dict(id='PoderData 5-7/10', papel='ref', instituto='PoderData', campo='5 a 7/10', registro='BR-08134/2026', n=3000,
         amostra_tipo='eleitores', confianca='alta', fonte='https://static.poder360.com.br/uploads/2026/10/Relatorio-PoderData-Eleitoral-8out26-final.pdf',
         colunas=[('Cury', 'Cury', 27, 56), ('Renan', 'Renan', 25, 48), ('Caiado', 'Caiado', 19, 57), ('Zema', 'Zema', 10, 72),
                  ('Outro', 'outro_sem_zema', 39, 19)]),
]

# fontes procuradas e sem o cruzamento (D1 ii e iii) ou sem a pesquisa (D1 i)
SEM_CRUZAMENTO = [
    ('Nexus/BTG 23-24/10 (BR-08234/2026, n 2.000)', 'só "votou no 1º turno" (Flávio 51,2 x Lula 48,8 nos válidos) e "não compareceu" (Lula 53,2 x Flávio 46,8); nenhuma coluna de eliminados (Bloomberg Línea 24/10; Tribuna de Jundiaí); relatório não achado (static.poder360: 404 nos nomes do padrão da rodada de 19/10)'),
    ('Quaest 23-24/10 (BR-09158/2026, n 3.702)', 'cruzamento não publicado na imprensa achada; o PDF baixado de static.poder360.com.br/uploads/2026/10/Pesquisa-Quaest-Nacional-24-out.pdf é a impressão da matéria do g1 sobre aprovação, sem tabelas; g1 bloqueado para a ferramenta de leitura'),
    ('Datafolha 23-24/10 (BR-09540/2026, n 4.050)', 'só total, válidos e propensão de comparecer (alta 76%: Flávio 52 x 48; média ou baixa 24%: Lula 52 x 48); relatório não achado (404 nos nomes do padrão do relatório de 15/10)'),
    ('Ipespe/Abrapel 20-22/10 (n 1.500)', 'matérias (Midiamax, SBT) sem o recall; PDF não achado (404 nos nomes do padrão das rodadas anteriores)'),
    ('Futura 23-24/10 (BR-09726/2026, n 2.000)', 'Gazeta do Povo sem cruzamento'),
    ('Gerp 22-24/10 (BR-09327/2026, n 2.400)', 'CNN diz "confira a íntegra abaixo", mas o documento não está na página lida'),
    ('CNT/MDA 21-23/10, Palver 22-24/10, Veritá 19-23/10, Instituto França 21-23/10, Vetor 23/10, 100% Cidades 24/10, Vox Brasil 20-22/10, Real Time Big Data 19-22/10, Alfa 19-22/10', 'nenhum cruzamento por voto no 1º turno achado'),
]
NAO_ACHADO = {
    'pos_eleicao': 'Nenhuma pesquisa nacional com campo depois de 25/10/2026 achada até 31/10/2026 (Placar das Pesquisas lista a última nacional em 24/10; '
                   'a lista da Wikipedia em inglês também). A BBC News Brasil (reproduzida pelo Em Dia ES em 27/10, 17h15) cita especialistas que '
                   'sugerem reentrevistar quem participou das pesquisas e checar se votou e se manteve o voto, como proposta, não como estudo feito.',
    'boca_de_urna': 'Nenhuma boca de urna nacional de presidente em 25/10/2026 achada (Wikipedia e Placar não listam; buscas por Ipec, AtlasIntel, '
                    'Quaest e Datafolha sem resultado). A AtlasIntel diz (TMC, 26 ou 27/10) que teve um "último tracking, com campo encerrado às 8h '
                    'do dia da eleição" com Lula em 49,7%; é pesquisa de véspera estendida, não boca de urna, e o cruzamento não foi achado.',
    'quem_deixou_ou_passou_a_votar': 'Nenhuma pesquisa pós-eleição mede quem deixou de votar ou passou a votar. O que existe é de antes do 2º turno: '
                    'PoderData 23-24/10 (11% da amostra não votou no 1º turno; entre eles Lula 50, Flávio 35, branco/nulo 15; com certeza vai '
                    'votar 65%), Colectta 23/10 (7,4% da amostra ponderada não votou; Lula 51,8 x Flávio 34,3), Nexus 23-24/10 (não compareceu: '
                    'Lula 53,2 x 46,8 nos válidos) e Datafolha 23-24/10 (propensão média ou baixa, 24%: Lula 52 x 48). A AtlasIntel explica o erro '
                    'pela volta de eleitores ao 2º turno, sem número de pesquisa feita depois.',
}

PISTAS = [
    'Distância urna x pesquisa cresce do eliminado mais ao centro para o mais à direita: Cury 9,5 pontos, Renan 13,2, Caiado 15,9, Zema '
    '23,5 (urna no bweb menos a mediana das rodadas; item por_grupo_descritivo deste JSON). O L4 viu o mesmo dentro das UFs de origem '
    '(GO Caiado 45,9 x 26,9; MG Zema 34,7 x 12,6; SP Cury 57,8 x 46,7; resultados/L4_bweb.txt). O padrão cabe em três leituras que estes '
    'dados não separam: viés ecológico (a regressão dá ao eleitor de Caiado e Zema o movimento dos vizinhos), mudança tardia ou '
    'abstenção desses eleitores depois da pesquisa, ou votos movidos de Flávio para Lula em proporção parecida em todo lugar.',
    'Institutos discordam muito sobre os eleitores de Cury (maior grupo, 37% dos eliminados): de 32,5% (PoderData 5-7/10) a 59,3% '
    '(Quaest 17-20/10); o PoderData foi de 53,3% (19-21/10) para 33,3% (23-24/10) em três dias. Quaest 17-20/10 e AtlasIntel 13-18/10 '
    '(59,3 e 55,1) ficam perto da urna para Cury (59,6); a diferença urna x pesquisa fica sobretudo em Renan, Caiado e Zema.',
    'Quem não votou no 1º turno: PoderData final 58,8% para Lula entre os que escolhem (50 x 35), Colectta 60,2% (51,8 x 34,3), Nexus '
    '53,2%; a regressão da urna no aumento do comparecimento dá 56,4% (L5). Bate; a diferença não está nos que passaram a votar.',
    'A AtlasIntel diz ter feito um "último tracking, com campo encerrado às 8h do dia da eleição" (Lula 49,7%; TMC, '
    'https://tmc.com.br/politica/atlasintel-pesquisas-subestimaram-comparecimento-lula-2turno-2026). É a medida mais próxima do voto que '
    'existe; o cruzamento por voto no 1º turno não foi publicado.',
    'Relatórios completos que podem existir e não foram lidos: Quaest e Datafolha de 23-24/10 (o g1 cita "página especial com todos os '
    'detalhes"; g1 bloqueado para a ferramenta), Nexus 23-24/10, Gerp 22-24/10 (CNN diz "confira a íntegra"), Ipespe 20-22/10. Dá para '
    'abrir num navegador comum, sem pedir nada a ninguém; o registro no PesqEle do TSE (BR-09158, BR-09540, BR-08234, BR-09327) também.',
    'Ipespe 20-22/10 aparece com o mesmo registro da rodada de 13-15/10 (BR-00223/2026, Midiamax e SeuDinheiro); a Gazeta do Povo grafa '
    'o Datafolha final como "BR-BR-09540/2026". Detalhes de registro a conferir no PesqEle.',
    'O "Relatório Pericial Independente" que circula desde 28/10 (Aos Fatos, 29/10, '
    'https://aosfatos.org/noticias/relatorio-fraude-eleitoral-distorce-dados-omite-fatos; o TSE também checou) já foi conferido neste '
    'repositório (checagens/relatorio_pericial_instagram, commit a4e44b8): não é pista nova para o F13.',
    'Flávio não reconheceu o resultado alegando a extensão do horário de votação (Wikipedia em inglês, seção Aftermath); liga com o F14 '
    '(17 seções da zona 90 de Volta Redonda mantidas abertas) e com o L1.',
    'Nenhuma pesquisa pós-eleição mediu quem deixou de votar ou passou a votar; a BBC (27/10) registra a sugestão de especialistas de '
    'reentrevistar quem respondeu às pesquisas. Um painel desses (pedir aos institutos) é o teste que separa as leituras acima.',
]


def faixa(s):
    """D3: régua do Adendo 21 pela estimativa pontual."""
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
    cols = f['colunas']
    W = [peso(c[1]) for c in cols]
    num = sum(w * c[2] for w, c in zip(W, cols))
    den = sum(w * (c[2] + c[3]) for w, c in zip(W, cols))
    s = 100 * num / den
    cobertura = sum(W) / ELIMINADOS
    # D4: erro amostral
    frac = (sum(W) / APTOS_1T) if f['amostra_tipo'] == 'eleitores' else (sum(W) / COMP_1T)
    n_grupo = f['n'] * frac
    escolhe = den / sum(W) / 100                     # fração do grupo que escolhe um finalista
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
    # sensibilidades (D2)
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
    # a urna com as mesmas colunas nomeadas e os mesmos pesos (comparação descritiva)
    if nom:
        for nome, U in (('bweb', URNA_BWEB), ('amostra_T37', URNA_AMOSTRA)):
            ws = [(VOTOS_1T[c[1]], U[c[1]][0]) for _, c in nom]
            res['urna_mesmas_colunas_' + nome] = round(sum(w * u for w, u in ws) / sum(w for w, _ in ws), 2)
    res['por_coluna'] = [dict(coluna=c[0], representa=GRUPOS_COLUNA[c[1]], L=c[2], F=c[3],
                              fatia_L=round(100 * c[2] / (c[2] + c[3]), 1), peso_votos_1T=w) for w, c in zip(W, cols)]
    return res


def main(saida_json, saida_txt):
    out = dict(teste='F13 do Adendo 21: pesquisas independentes da urna', data='31/10/2026',
               registro='PRE-REGISTRO-2026-10-26.md, Adendo 21, commit 913af7a (31/10/2026 10:36:29 UTC)',
               regua='confere com a urna: 47 a 59 (52 a 54 mais ou menos 5); confere com as pesquisas de antes: 32 a 44; intermediário: entre 44 e 47 (D3)',
               decisoes_antes='docstring deste script; cópia em /home/user/trabalho-eleicao/adendo21/F13_scripts/decisoes_antes_de_buscar.py, '
                              'sha256 f11d8b3c9dd07e913071d8af884e92343073c8e6dfa0ae74923641b052b4e08c, 31/10/2026 11h49 UTC',
               urna=dict(por_grupo_bweb=URNA_BWEB, por_grupo_amostra_T37=URNA_AMOSTRA, todos=URNA_TODOS_ELIMINADOS,
                         oficial_2T_L_validos=OFICIAL_2T_L, oficial_1T_validos=OFICIAL_1T),
               fontes=[], referencias=[], sem_cruzamento=[dict(fonte=a, situacao=b) for a, b in SEM_CRUZAMENTO], nao_achado=NAO_ACHADO, pistas=PISTAS)
    for f in FONTES:
        r = calcula(f)
        item = {k: v for k, v in f.items() if k != 'colunas'}
        item.update(r)
        (out['fontes'] if f['papel'] == 'F13' else out['referencias']).append(item)
    regua = [x for x in out['fontes'] if x['confianca'] in ('alta', 'média')]
    cont = {}
    for x in regua:
        cont[x['faixa']] = cont.get(x['faixa'], 0) + 1
    out['resumo'] = dict(
        fontes_com_regua=len(regua), por_faixa=cont,
        pos_eleicao_com_lembranca=0, boca_de_urna=0,
        veredito=('Pela letra: nenhuma pesquisa pós-eleição e nenhuma boca de urna achadas (essas partes ficam SEM DADOS). Relatórios '
                  'finais com cruzamento: ' + '; '.join('%s %s%% (%s)' % (x['id'], br(x['s']), x['faixa']) for x in regua) + '.'),
    )
    refs = [x['s'] for x in out['referencias']]
    out['resumo']['referencias_min_max'] = [min(refs), max(refs)]
    out['resumo']['combinado_pos_hoc'] = combinado(out['fontes'])
    out['resumo']['por_grupo_descritivo'] = por_grupo(out['fontes'] + out['referencias'])
    json.dump(out, open(saida_json, 'w'), ensure_ascii=False, indent=1)
    escrever_txt(out, saida_txt)


def br(x, casas=1):
    """número com vírgula decimal."""
    return ('%.' + str(casas) + 'f') % x if x is None else (('%.' + str(casas) + 'f') % x).replace('.', ',')


def combinado(fontes):
    """Descritivo pós-hoc (não registrado, sem régua): média das fontes do F13 com cobertura de 90% ou mais, pesos 1/ep^2."""
    sel = [x for x in fontes if x['cobertura_dos_eliminados'] >= 0.9 and x['confianca'] in ('alta', 'média')]
    out = {}
    for deff in (1, 2):
        ws = [(1 / x['deff%d' % deff]['ep'] ** 2, x['s']) for x in sel]
        W = sum(a for a, _ in ws)
        m = sum(a * b for a, b in ws) / W
        ep = 1 / math.sqrt(W)
        out['deff%d' % deff] = dict(s=round(m, 2), ep=round(ep, 2), ic95=[round(m - 1.96 * ep, 1), round(m + 1.96 * ep, 1)],
                                    faixas_tocadas=faixas_tocadas(m - 1.96 * ep, m + 1.96 * ep))
    out['fontes'] = [x['id'] for x in sel]
    if len(sel) == 2:
        a, b = sel
        d = b['s'] - a['s']
        e = math.sqrt(a['deff1']['ep'] ** 2 + b['deff1']['ep'] ** 2)
        out['diferenca_entre_as_duas'] = dict(dif=round(d, 2), ep_deff1=round(e, 2), z=round(d / e, 2))
    return out


def por_grupo(todas):
    """Descritivo pós-hoc: fatia de Lula por candidato eliminado, em todas as rodadas que separam o candidato, contra a urna."""
    out = {}
    for g in ('Cury', 'Renan', 'Caiado', 'Zema'):
        vals = [(x['id'], c['fatia_L']) for x in todas for c in x['por_coluna'] if c['representa'] == [g]]
        if not vals:
            continue
        v = sorted(b for _, b in vals)
        med = v[len(v) // 2] if len(v) % 2 else (v[len(v) // 2 - 1] + v[len(v) // 2]) / 2
        out[g] = dict(n_rodadas=len(v), minimo=v[0], mediana=round(med, 1), maximo=v[-1], urna_bweb=URNA_BWEB[g][0],
                      urna_amostra_T37=URNA_AMOSTRA[g][0], urna_menos_mediana=round(URNA_BWEB[g][0] - med, 1), rodadas=vals)
    return out


def escrever_txt(o, caminho):
    L = []
    w = L.append
    F = o['fontes']
    w('F13 do Adendo 21: pesquisas independentes da urna. Rodado em 31/10/2026.')
    w('Script: scripts/analisar_F13.py. Números: resultados/F13_pesquisas_independentes.json.')
    w('')
    w('Critério registrado (Adendo 21, commit 913af7a, antes de rodar):')
    w('  "Pesquisas feitas depois da eleição com a lembrança do voto nos dois turnos, boca de urna do dia 25/10 e os relatórios finais')
    w('  completos (com tabelas cruzadas) dos institutos. Para cada uma: fatia de Lula entre os eleitores dos eliminados que escolheram')
    w('  um finalista. Descritivo, com a régua: confere com a urna se ficar a 5 pontos ou menos de 52% a 54%; confere com as pesquisas')
    w('  de antes se ficar entre 32% e 44%; entre os dois, intermediário."')
    w('  Decisões onde o registro não fixa (D1 a D11, desvios declarados): docstring do script, escrita às 11h49 UTC de 31/10, antes')
    w('  de qualquer busca; cópia com sha256 em /home/user/trabalho-eleicao/adendo21/F13_scripts/decisoes_antes_de_buscar.*.')
    w('  Faixas (D3): urna 47 a 59; pesquisas de antes 32 a 44; intermediário entre 44 e 47; fora disso, "abaixo das pesquisas de')
    w('  antes" (< 32) ou "acima da urna" (> 59). Tomadas depois de ver números, também desvios: (1) no erro amostral de uma coluna só')
    w('  (AtlasIntel, só Renan), o n do grupo usa a fatia daquele candidato; (2) a média combinada do item 2 é pós-hoc e não recebe régua.')
    w('')
    w('VEREDITO PELA LETRA')
    w('  (i) Pesquisa feita depois da eleição com a lembrança do voto nos dois turnos: SEM DADOS. Nenhuma achada até 31/10/2026.')
    w('  (ii) Boca de urna nacional de presidente em 25/10: SEM DADOS. Nenhuma achada.')
    w('  (iii) Relatórios finais (última rodada de cada instituto, campo terminando de 21 a 24/10) com o 2º turno cruzado pelo voto')
    w('       no 1º turno: três fontes, nenhuma com o relatório completo além do PoderData.')
    for x in F:
        w('      %-22s s = %5s%%  -> %s  (cobertura %s%% dos votos dos eliminados; confiança %s)' % (
            x['id'], br(x['s']), x['faixa'].upper(), br(100 * x['cobertura_dos_eliminados'], 0), x['confianca']))
    urna = [x for x in F if x['faixa'] == 'confere com a urna']
    w('  Nenhuma das três fica na faixa da urna (47 a 59).' if not urna else '  Na faixa da urna: ' + ', '.join(x['id'] for x in urna) + '.')
    for x in F:
        w('  %s: IC95 de %s a %s (deff 1), de %s a %s (deff 2); toca: %s.' % (
            x['id'], br(x['deff1']['ic95'][0]), br(x['deff1']['ic95'][1]), br(x['deff2']['ic95'][0]), br(x['deff2']['ic95'][1]),
            '; '.join(x['deff2']['faixas_tocadas'])))
    w('')
    w('1. Por fonte (fatia de Lula entre os que escolheram um finalista; pesos = votos oficiais do 1º turno de cada grupo, D2)')
    for x in F + o['referencias']:
        w('  %s | %s | campo %s | %s | n %s | confiança %s | %s' % (
            x['id'], x['instituto'], x['campo'], x['registro'], format(x['n'], ',').replace(',', '.'), x['confianca'],
            'F13' if x['papel'] == 'F13' else 'referência (rodada anterior, sem régua)'))
        for c in x['por_coluna']:
            w('      %-30s L %5s  F %5s  fatia L %5s%%  (representa %s; %s votos no 1º turno)' % (
                c['coluna'], br(c['L']), br(c['F']), br(c['fatia_L']), '+'.join(c['representa']),
                format(c['peso_votos_1T'], ',').replace(',', '.')))
        d1, d2 = x['deff1'], x['deff2']
        w('      s = %s%% -> %s. Cobertura %s%%. n do grupo ~%s, n efetivo ~%s. ep %s (IC95 %s a %s) com efeito de desenho 1; '
          'ep %s (IC95 %s a %s) com 2.' % (br(x['s']), x['faixa'], br(100 * x['cobertura_dos_eliminados'], 0), br(x['n_grupo_estimado'], 0),
                                           br(x['n_efetivo'], 0), br(d1['ep']), br(d1['ic95'][0]), br(d1['ic95'][1]), br(d2['ep']),
                                           br(d2['ic95'][0]), br(d2['ic95'][1])))
        for k, v in x['sensibilidade'].items():
            w('      sensibilidade %s: %s%% (%s)' % (k, br(v['s']), v['faixa']))
        if 'urna_mesmas_colunas_bweb' in x:
            w('      urna com as mesmas colunas nomeadas e os mesmos pesos: %s%% (bweb), %s%% (amostra do T37)' % (
                br(x['urna_mesmas_colunas_bweb']), br(x['urna_mesmas_colunas_amostra_T37'])))
        if x.get('nota'):
            w('      nota: ' + x['nota'])
        if x.get('arquivo'):
            w('      lido em: ' + x['arquivo'])
        w('      fonte: ' + x['fonte'])
    w('')
    w('2. O que os números significam')
    lo, hi = o['resumo']['referencias_min_max']
    w('  - Rodadas anteriores (5 a 21/10), mesmo cálculo: de %s%% a %s%%, com uma abaixo de 32 (PoderData 5-7/10). Coerente com a faixa' % (br(lo), br(hi)))
    w('    "pesquisas de antes" do registro (32 a 44).')
    w('  - Urna (regressão do T8 com grupos, mesmo local; regressão ecológica): Cury 59,6, Renan 54,2, Caiado 48,8, Zema 36,1 (bweb);')
    w('    todos os eliminados num grupo 54,1 (ep 0,2); amostra do T37 52,2 (ep 1,7).')
    difs = []
    for x in F:
        if 'urna_mesmas_colunas_bweb' in x:
            base = x['sensibilidade'].get('a_so_colunas_nomeadas', {'s': x['s']})['s']
            difs.append((x['id'], x['urna_mesmas_colunas_bweb'] - base, x['urna_mesmas_colunas_amostra_T37'] - base))
    w('  - Distância da urna, com as mesmas colunas nomeadas e os mesmos pesos (urna menos pesquisa, bweb / amostra): ' +
      '; '.join('%s %s / %s pontos' % (a, br(b), br(c)) for a, b, c in difs) + '.')
    c = o['resumo']['combinado_pos_hoc']
    w('  - Média combinada pós-hoc (sem régua; %s; pesos 1/ep^2): %s%% (ep %s; IC95 %s a %s) com deff 1; %s%% (IC95 %s a %s) com deff 2.' % (
        ' e '.join(c['fontes']), br(c['deff1']['s']), br(c['deff1']['ep']), br(c['deff1']['ic95'][0]), br(c['deff1']['ic95'][1]),
        br(c['deff2']['s']), br(c['deff2']['ic95'][0]), br(c['deff2']['ic95'][1])))
    if 'diferenca_entre_as_duas' in c:
        d = c['diferenca_entre_as_duas']
        w('    Diferença entre as duas: %s pontos (ep %s, z %s): presencial (Colectta) e telefone automático (PoderData) não se distinguem' % (
            br(d['dif']), br(d['ep_deff1']), br(d['z'], 2)))
        w('    pelo erro amostral.')
    w('  - Por candidato, todas as rodadas que o separam (descritivo pós-hoc; mediana das pesquisas e urna no bweb):')
    for g, v in o['resumo']['por_grupo_descritivo'].items():
        w('      %-7s %2d rodadas, de %s a %s, mediana %s; urna %s (amostra %s); urna menos mediana %s pontos' % (
            g, v['n_rodadas'], br(v['minimo']), br(v['maximo']), br(v['mediana']), br(v['urna_bweb']), br(v['urna_amostra_T37']),
            br(v['urna_menos_mediana'])))
    w('  - Leitura: as pesquisas de véspera que publicaram o cruzamento repetem o que as rodadas anteriores diziam (eleitores dos')
    w('    eliminados com Flávio na frente entre os que escolhem), e ficam abaixo do que a urna implica. A diferença urna x pesquisa nos')
    w('    eliminados, que o T37 e o L5 já tinham, continua. Não há medida feita depois do voto (lembrança ou boca de urna) que diga se')
    w('    os eleitores dos eliminados mudaram nos últimos dias, se a pesquisa os mediu mal, ou se a regressão da urna os atribui mal.')
    w('  - Poder: o grupo é pequeno (5,9% dos aptos). Uma fonte sozinha tem ep de 3,5 a 6,4 pontos (deff 1) e não separa 40 de 50.')
    w('    No próprio PoderData, a fatia de Lula entre os eleitores de Cury foi de 53,3% (19-21/10) para 33,3% (23-24/10) em três dias,')
    w('    o que mostra o ruído das subamostras; a coluna "Outro candidato" do PoderData final (Flávio 65, Lula 15, branco/nulo 0, não')
    w('    sabe 20) é de umas 15 entrevistas.')
    w('')
    w('3. O que não foi achado')
    for k, v in o['nao_achado'].items():
        w('  %s: %s' % (k, v))
    w('  Relatórios finais sem cruzamento achado:')
    for s_ in o['sem_cruzamento']:
        w('    - %s: %s' % (s_['fonte'], s_['situacao']))
    w('')
    w('4. Limites')
    w('  - Pesquisa de véspera mede intenção, não voto. Quem decidiu ou mudou no dia, e quem não ia votar e votou, fica de fora.')
    w('  - Subamostras pequenas e não publicadas; o n foi estimado pela fatia oficial dos eliminados (D4).')
    w('  - O PoderData pondera pelo resultado do 1º turno; a ponderação acerta o tamanho do grupo, não a escolha dentro dele.')
    w('  - Colectta e AtlasIntel finais vêm de matéria, não do relatório (confiança média). A AtlasIntel cobre só Renan (29% dos')
    w('    eliminados); a urna para Renan é 54,2 (bweb) ou 49,3 (amostra do T37), as duas acima dos 42,9 da AtlasIntel.')
    w('  - A urna aqui é regressão ecológica entre seções do mesmo local; erra se o eleitor de um eliminado mora junto de outro tipo de')
    w('    eleitor (limite já escrito no L4).')
    w('  - Regra do Adendo 18: nenhuma eleição anterior foi usada como régua.')
    w('')
    w('5. Pistas (fora do critério)')
    for k, t in enumerate(o['pistas'], 1):
        w('  %d. %s' % (k, t))
    open(caminho, 'w').write('\n'.join(L) + '\n')


if __name__ == '__main__':
    main(sys.argv[1], sys.argv[2])
