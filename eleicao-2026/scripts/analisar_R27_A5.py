"""R27 A5 (Adendo 27, Onda A): EXTERIOR E RELÓGIO ABSOLUTO.

Fragilidade "F19 (exterior sem biometria) e o contrapeso do L7 e do F6" de
registro/adendo27/equipe_vermelha_relatorio.json (commit 2748895, 10/11/2026 00:16:42 UTC), aplicada pela letra, sem
mudar limiar. Três partes:
  (a) diferença em diferenças por cidade do exterior, de 2022 para 2026, com o mesmo pareamento nos dois anos;
  (b) dose por fuso: o desvio D de cada cidade contra a fração da janela local de votação (8h às 17h locais) que cai
      antes das 8h de Brasília, com placebo em 2022 e 2018;
  (c) no Brasil, as seções com zero habilitação biométrica de fato contra as vizinhas.

Hipóteses. H1 (do F19): um programa que fica honesto quando a urna não faz nenhuma habilitação por biometria; o exterior
vota sem biometria, então o exterior viraria MENOS para Lula do que seções do Brasil de composição igual (D negativo).
H-relógio (da equipe vermelha): um gatilho por relógio absoluto, que só age depois que o Brasil abre (8h de Brasília);
pouparia as cidades do exterior que votam antes disso (Ásia e Oceania inteiras, parte da Europa, da África e do Oriente
Médio) e agiria nas Américas como no Brasil: D mais negativo quanto maior a fração da janela local antes das 8h de
Brasília, e D perto de zero nas Américas.

Aviso do próprio registro: os retestes da equipe vermelha foram escritos por quem já conhecia os resultados antigos. O
critério é novo, mas a escolha do que retestar é posterior ao dado (o desenho por fuso foi sugerido pela lista de D por
cidade do F19: Japão, Austrália e Líbano os mais negativos, EUA perto de zero).

CRITÉRIO DO REGISTRO (campo criterio_proposto, copiado)
  "SINAL: diferença em diferenças de -1,0 ou menos a mais de 3 ep (por país) ou inclinação da dose de -1,0 ponto ou
  menos por unidade de fração a mais de 3 ep, ausente em 2022 (|inclinação| abaixo de 0,4). SEM SINAL: |diferença em
  diferenças| abaixo de 0,4 com ep até 0,2 e inclinação abaixo de 0,4 em valor absoluto. Seções brasileiras sem
  biometria: sinal com -1,0 ou menos a mais de 4 ep em pelo menos 100 seções; sem sinal com |d| abaixo de 0,4 e ep até
  0,2; com menos de 100 seções, declarar SEM PODER e não usar como contrapeso."

Este docstring foi escrito ANTES de calcular qualquer resultado com votos. Cópia com data e SHA-256 em
/home/user/trabalho-eleicao/adendo27/R27_A5/docstring_antes_de_rodar.txt. Não havia execução anterior deste teste em
disco (nem script, nem pasta de trabalho) quando este arquivo foi criado (o aviso de reinício do container foi
conferido: nada a reaproveitar).

O QUE EU JÁ CONHECIA AO ESCREVER (tudo de arquivos já publicados ou de estrutura, sem voto calculado por mim)
  - Do F19 publicado (resultados/F19_exterior_pareado.txt): D de 2026 = -0,65 (ep 0,16 por cidade); a lista de D de
    2026 por cidade; D de 2022 = +0,12 e de 2018 = +0,90 no agregado. Eu NÃO conhecia D por cidade de 2022 nem de 2018,
    nenhuma diferença em diferenças e nenhuma inclinação por fuso.
  - Estrutura, sem votos: (i) bweb do 2º turno, UF ZZ: abertura às 8h e encerramento às 17h no relógio da urna em todas
    as cidades com horário; DT_BU_RECEBIDO das cidades a leste do Brasil é 17:05 de Brasília para todas (não ajuda a
    conferir fuso); nas Américas o recebimento respeita o limite inferior do fuso da tabela. (ii) Boletins em disco
    (8.099 do 2º turno): campo [S, B, M] soma o comparecimento e M é igual ao campo do bweb em todos; só 1 tem B = 0.
    (iii) Perfil do eleitorado por seção (516.785 seções, 158.745.463 eleitores, 141.301.540 com biometria): NENHUMA
    seção do Brasil tem zero eleitor com biometria no perfil; 2 seções têm NH maior ou igual ao número de eleitores com
    biometria. (iv) Cadastro de locais: 243 seções em local do tipo "Preso provisório" (inclui unidades de internação)
    no bweb do 2º turno, sem perfil (eleitores transferidos); os 100 primeiros boletins baixados dessas seções têm
    todos B > 0, isto é, a seção de presos habilita por biometria.

DECISÕES QUE O REGISTRO NÃO FIXA (tomadas aqui, antes de qualquer conta com votos; relatadas como desvios)

Pareamento (o do F19, reescrito aqui; o mesmo nos três anos)
  P1. Universo por ano: seções com os dois turnos na base, comparecimento e aptos positivos nos dois, votos nos
      finalistas positivos nos dois. Exterior = UF ZZ com L2+R2 >= 30. Candidatas a par = seções fora do ZZ com o mesmo
      piso. L = candidato do PT (Lula em 2026 e 2022, Haddad em 2018); R = adversário (Flávio, Bolsonaro, Bolsonaro).
  P2. Variáveis: f1 = 100 L1/(L1+R1); outros = 100 O1/(L1+R1+O1); bn = 100 (B1+N1)/C1; dc = 100 (C2/A2 - C1/A1).
      Padronização: média e desvio-padrão (sem peso, ddof 1) das candidatas do mesmo ano. 20 pares de menor distância
      euclidiana, com reposição, empate pela ordem da chave. Virada y = 100 L2/(L2+R2) - f1. Contrafactual m_i = média
      de y dos 20 pares ponderada por L2+R2 do par. dif_i = y_i - m_i. D de um conjunto = soma w_i dif_i / soma w_i, com
      w_i = L2+R2 da seção do exterior. Conferência do código: D agregado de 2026, 2022 e 2018 contra o F19 publicado.
  P3. País de cada cidade e fuso: tabela FUSOS deste arquivo (código do município no TSE, nome no bweb, país, zona IANA).
      Guiana Francesa, Hong Kong e Palestina contam como país próprio no bootstrap (comunidades distintas das da
      metrópole). Semente de todo sorteio: 20261110. Bootstrap: 2.000 réplicas, países sorteados com reposição, pares
      fixos; ep = desvio-padrão das réplicas (ddof 1); ao lado, o erro agrupado por país pela fórmula (CR1).

Parte (a), diferença em diferenças
  A1. "Pareamento dentro do país" lido assim: a cidade de 2026 é comparada com ela mesma em 2022; se a cidade não tem
      seção com piso em 2022 (cidade nova, como Orlando, Edimburgo e Marselha), a referência é o conjunto das cidades do
      mesmo país em 2022; sem cidade do país em 2022, a cidade sai e é contada. (A outra leitura possível, parear o
      exterior com seções "de dentro do país", é o próprio pareamento P1-P2.)
  A2. Principal: DiD = soma w_c (D_c,2026 - D_ref(c),2022) / soma w_c, com w_c = votos nos finalistas da cidade no
      2º turno de 2026. ep por bootstrap de países (P3). "A mais de 3 ep" = |DiD| > 3 ep.
  A3. Leitura: SINAL se DiD <= -1,0 e |DiD| > 3 ep. SEM SINAL (parte a) se |DiD| < 0,4 e ep <= 0,2. O resto,
      INCONCLUSIVO. O veredito desta parte depende, por construção, da comparação com 2022, ano de que o Léo também
      suspeita; por isso o valor bruto de 2026 (D de nível, com ep por país) sai ao lado e isso é dito no veredito.
  A4. Ao lado, sem mudar o veredito: só cidades com seção nos dois anos; por país (D do país em cada ano, peso de 2026);
      diferença simples dos D agregados (cada ano com os seus pesos e todas as cidades); média sem peso das cidades;
      10 e 50 pares; sem a variação do comparecimento; tirando um país de cada vez (mínimo e máximo); placebo
      2018 para 2022 pela mesma conta (peso de 2022) e a diferença tripla (2026-2022) - (2022-2018).

Parte (b), dose por fuso
  B1. Fuso: deslocamento UTC da zona IANA da cidade ao meio-dia local do dia do 2º turno (25/10/2026, 30/10/2022,
      28/10/2018), lido do banco tz do sistema (tzdata 2026e) com zoneinfo. Brasília pelo mesmo banco (America/Sao_Paulo,
      -3 nas três datas). Fração f = min(1, max(0, (o_cidade - o_Brasília)/9)): parte da janela 8h às 17h locais que
      cai antes das 8h de Brasília. A zona é a da sede (cidade do nome); onde o cadastro de locais do TSE mostra local
      de votação em outro fuso (Los Angeles/Utah, Vancouver/Calgary, Toronto/Winnipeg, Miami/Porto Rico,
      Camberra/Melbourne e Perth, Sydney/Brisbane), a fração é a mesma (0 ou 1) e nada muda. Trípoli vota na embaixada
      em Túnis (cadastro) e usa o fuso de Túnis.
  B2. Regressão por cidade: D_c contra f_c, com constante, mínimos quadrados ponderados por w_c (votos nos finalistas
      da cidade no 2º turno do ano). Inclinação b. ep por bootstrap de países (P3); ao lado, CR1 por país e
      permutação de f entre países (2.000). "A mais de 3 ep" = |b| > 3 ep do bootstrap.
  B3. Leitura: SINAL se b(2026) <= -1,0, |b| > 3 ep e |b(2022)| < 0,4. SEM SINAL (parte b) se |b(2026)| < 0,4.
      Se b(2026) passa do limiar mas |b(2022)| >= 0,4, a letra não dá sinal: INCONCLUSIVO, e isso é dito.
      Veredito conjunto do exterior pela letra: SINAL se (a) ou (b) der sinal; SEM SINAL se as duas condições de sem
      sinal valerem; o resto, INCONCLUSIVO.
  B4. Ao lado, sem mudar o veredito: a mesma regressão em 2018; média de D por grupo de dose (f = 0; 0 < f < 1; f = 1);
      dose sobre a diferença em diferenças (D_c,2026 - D_ref,2022 contra f); com controle da fatia de Lula no 1º turno
      da cidade; forma proporcional (D contra f x fatia do adversário no 1º turno, o que uma troca de s% dos votos do
      adversário prevê: inclinação de -3,57 se s = 3,57%); sem peso; tirando um país de cada vez; sem o Japão (a
      exclusão que o F19 fez depois do resultado, aqui só para mostrar o quanto pesa).
  B5. Espelho da dose: g = fração da janela local que cai DEPOIS das 17h de Brasília = min(1, max(0, (o_Brasília -
      o_cidade)/9)), maior que zero só nas Américas a oeste. Um gatilho que começa às 8h de Brasília não prevê nada
      para g; se D cair com g tanto quanto com f, a dose é geografia e não relógio.

Parte (c), seções do Brasil sem habilitação biométrica
  C1. Contadores: campo [2:1] do boletim de urna, três inteiros [S, B, M] (S = eleitores sem biometria cadastrada,
      B = habilitados por biometria, M = com biometria liberados sem ela, igual ao QT_ELEI_BIOM_SEM_HABILITACAO do
      bweb). Lido de todos os boletins do 2º turno em disco antes do Adendo 27 (amostra2t/arq, arq_G, arq_t17,
      arq_t17b, adendo21/F14_arq, adendo24/C3_arq) e dos baixados agora pela regra C2. A amostra aleatória nova do
      Adendo 27 (adendo27/aas) não é usada: download em curso e pertence à Onda D. Boletim cuja soma difere do
      comparecimento do bweb ou cujo M difere do campo do bweb é excluído e contado.
  C2. Download (desvio declarado: a tarefa fala em "boletim da amostra"; com 1 seção em 8.099 a amostra não basta).
      Só o boletim (poucos KB), 1 requisição por segundo, do site de resultados do TSE, na ordem: P = todas as 243
      seções de local do tipo "Preso provisório"; C = seções do Brasil em que o perfil permite zero habilitação,
      Bmin = comparecimento - NH - (eleitores sem biometria no perfil, somadas as seções agregadas) <= 5 (708 seções;
      a folga de 5 existe porque em 4,5% dos boletins em disco S passa o número do perfil, quase sempre por 1 a 5);
      T = 152 seções de "Voto em trânsito"; X = 12 seções do exterior, só para documentar o campo. A lista
      (lista_bu.txt, SHA-256 7de8a6da...) foi fixada só com estrutura. O que estiver baixado na hora da conta é usado;
      a cobertura de cada estrato é relatada.
  C3. Grupo do veredito, Z = seções do Brasil com B = 0 no boletim e comparecimento positivo ("zero habilitação
      biométrica de fato", S + M igual ao comparecimento). Seções de presos entram em Z se tiverem B = 0. Pelo perfil
      sozinho o grupo é vazio (nenhuma seção sem eleitor com biometria), e isso é relatado como resultado.
      Ao lado, sem decidir: P = todas as seções de "Preso provisório" (pelo tipo e nome do local), tenham ou não
      biometria; Q = espelho, seções da lista C com boletim e B > 0 (pouca biometria, mas não zero: pela hipótese não
      deveriam diferir das vizinhas).
  C4. Universo: seções das 27 UFs com os dois turnos, votos nos finalistas positivos nos dois. y e peso como em P2.
      Estimadores: (local) y contra o indicador do grupo com efeito fixo de local de votação (UF, município, zona,
      local do 2º turno), peso L2+R2, erro agrupado por local (lib.fe_ols); (zona) o mesmo com efeito fixo de zona
      (UF e zona) e erro agrupado por zona. Seções "que informam" = as do grupo em local (ou zona) que também tem
      seção fora do grupo. Ao lado: com as covariáveis do pareamento (f1, outros, bn, dc); o pareamento P2 aplicado
      ao grupo (20 pares entre as seções do Brasil fora de Z, P e Q, com piso de 30 só nas candidatas; ep por
      bootstrap de municípios); permutação do indicador dentro da zona.
  C5. Leitura: se pelo menos 100 seções de Z informam o estimador de local, vale ele; senão, se pelo menos 100 informam
      o de zona, vale o de zona; senão SEM PODER (a letra). SINAL: d <= -1,0 e |d| > 4 ep. SEM SINAL: |d| < 0,4 e
      ep <= 0,2. O resto, INCONCLUSIVO. P é lido pelo mesmo critério, mas só vale como "condição" se os boletins
      mostrarem B = 0; com B > 0 é só a comparação de presos com vizinhos.

Calibração por efeito plantado (obrigatória), sempre por cima dos dados de 2026
  K1. Tamanho: delta = 1,785 ponto (a troca uniforme que vira o resultado; régua do L7 e do F19) como principal e
      1,0 ponto (o limiar do critério) ao lado. Forma uniforme: em cada seção atingida, x ~ Binomial(L2+R2, delta/100),
      limitado a R2, sai de R2 e entra em L2. Forma proporcional ao lado: x ~ Binomial(R2, 0,0357).
  K2. (a): todas as candidatas do Brasil atingidas, exterior intacto (H1). Deslocamento esperado da DiD: -delta.
      (b): Brasil atingido por inteiro; cada seção do exterior atingida na fração (1 - f) da cidade (H-relógio).
      Deslocamento esperado da inclinação: -delta. (c): todas as seções do Brasil fora de Z atingidas, Z intacto.
  K3. "O teste enxerga": PODER DE MEDIDA se o plantio desloca a estatística em pelo menos 80% do esperado e o
      deslocamento passa de 3 ep (4 ep na parte c). PODER PLENO se, além disso, as condições numéricas de SINAL
      disparam com o plantio. Sem poder de medida com delta = 1,785, o veredito da parte é SEM PODER, qualquer que
      seja a letra. Ao lado: o menor efeito que o critério enxergaria numa base sem desvio, max(1,0; 3 ep).
  K4. Espelho: (i) a mesma conta para o lado contrário (critério com o sinal trocado, +1,0 a mais de 3 ep);
      (ii) onde a troca de votos entre finalistas não deveria dar nada: a mesma conta com o desfecho
      variação do branco e nulo, 100 ((B2+N2)/C2 - (B1+N1)/C1), mesmos pares; (iii) B5 e o grupo Q de C3;
      (iv) placebos de 2022 e 2018, com a ressalva do Adendo 18.
  K5. Tradução em votos: um desvio de x pontos na fatia de Lula entre os finalistas, se valesse para as seções do
      Brasil, são x/100 vezes os votos nos finalistas do Brasil no 2º turno (votos trocados); a margem muda o dobro.
      Margem oficial 4.430.191; vira com 1,785 ponto. O exterior inteiro é relatado em votos: ele não muda o resultado,
      só serve de pista do mecanismo.

Uso (sempre python3 -I):
  python3 -I scripts/analisar_R27_A5.py estrutura   perfil por seção, tipo de local, S/B/M dos boletins (sem votos)
  python3 -I scripts/analisar_R27_A5.py             roda as três partes; grava resultados/R27_A5_exterior_fuso.json e .txt
  python3 -I scripts/analisar_R27_A5.py texto       só reescreve o .txt a partir do .json
Auxiliares de estrutura e download, sem votos, guardados em /home/user/trabalho-eleicao/adendo27/R27_A5/:
  estrutura_perfil.py, estrutura_bu.py, montar_lista_bu.py, baixar_bu.py, explorar_*.py.

ACRESCENTADO DEPOIS DE VER RESULTADOS (exploratório; não muda nenhum veredito): ver a seção EXPLORATÓRIO no fim deste
docstring, preenchida só depois da primeira rodada completa.

EXPLORATÓRIO (escrito em 10/11/2026, DEPOIS da primeira rodada completa, que deu: DiD -0,78 com ep 0,21; inclinação de
2026 -1,47 com ep 0,91, de 2022 -0,74 e de 2018 -2,42; Z com 1 seção). O texto acima deste bloco é o registrado
(SHA-256 cce8de2c... em docstring_antes_de_rodar.txt) e não foi mudado. Correções de código feitas depois da primeira
rodada, sem mexer em decisão: formatação de valores sem erro-padrão e a linha de veredito que mostra a leitura pela
letra ao lado do veredito com a regra K3.
  X1. Estabilidade dos códigos de município do exterior entre 2014 e 2026 (nomes do bweb de 2014 contra a tabela FUSOS).
  X2. 2014 como quarto ano (base dados/secoes2014.json.gz, Dilma contra Aécio): D de nível, inclinação da dose, média por
      grupo de dose e DiD de 2014 para 2018. Em 26/10/2014 Brasília estava em horário de verão (UTC-2, pelo banco tz).
      Códigos que só existem em 2014 entram pela tabela FUSOS_2014 (nomes do bweb de 2014). Sorteios próprios
      (semente + 50), para não mexer nos erros-padrão das partes registradas.
  X3. D por país e ano, nos 12 países com mais votos em 2026.
  X4. D sem peso e por tamanho da cidade, por ano (para ler a média sem peso da DiD, bem mais negativa que a ponderada).
  X5. DiD por tamanho da cidade, com o bootstrap de países das partes registradas, e a mesma conta no placebo de 2018
      para 2022 (acrescentado depois de ver X4).
  X6. 2026 com pareamento mais fino (acrescentado depois de ver X5): no lugar da fatia total dos "outros", as fatias de
      Cury (70), Renan (14), Caiado (55) e do resto, com f1, bn e dc; 7 variáveis padronizadas, 20 pares. Pergunta: o D
      de 2026 vem da composição dos eleitores dos eliminados, que o pareamento registrado não vê? Só existe para 2026
      (as bases de 2022 e 2018 não trazem voto por candidato), então não entra na diferença em diferenças.
  X7. Dose pela força do adversário (acrescentado depois de ver X6): D da cidade contra a fatia do adversário no
      1º turno, por ano, e a DiD contra a mesma fatia; contagem de cidades com DiD negativa em 2026 e no placebo.
  X8. Parte (c), depois de ver o grupo Q com os 708 boletins (d no local -0,21, ep 0,11; pareado -0,64, ep 0,12): dose de
      habilitação sem biometria dentro do local, nb = (S + M)/comparecimento, exato onde há boletim e aproximado pelo
      perfil nas outras seções (fator S/S_hat medido na amostra amostra2t/arq); nos locais de Q e no país, com placebo
      de nível. Pergunta: a troca pouparia o voto habilitado sem biometria (versão de dose da H1)? Previsão: -1,785 por
      unidade de nb. Também: os 12 boletins do exterior não trazem o campo de habilitações.
  X9. As mesmas seções do grupo Q em 2022 e 2018 contra as vizinhas de local daquele ano (acrescentado depois de X8):
      se já viravam menos antes, é traço da seção e não efeito de 2026.
  A frase de leitura (o que pesa a favor e contra) é escrita depois dos números e fica marcada como interpretação.
"""
import os as _os, sys as _sys
_sys.path.insert(0, _os.path.dirname(_os.path.abspath(__file__)))
import collections, csv, datetime, gc, glob, gzip, hashlib, io, json, os, sys, time, zipfile, zoneinfo
import numpy as np
from lib import carregar, fe_ols

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DADOS = os.path.join(REPO, 'dados')
TRAB = '/home/user/trabalho-eleicao'
W = os.path.join(TRAB, 'adendo27', 'R27_A5')
SAIDA_JSON = os.path.join(REPO, 'resultados', 'R27_A5_exterior_fuso.json')
SAIDA_TXT = os.path.join(REPO, 'resultados', 'R27_A5_exterior_fuso.txt')
PERFIL_DIR = os.path.join(TRAB, 'adendo21', 'F15_dl_perfil_secao')
LOCAIS_ZIP = os.path.join(TRAB, 'adendo21', 'F14_dl_locais', 'eleitorado_local_votacao_2026.zip')
ESTRUTURA_2T = os.path.join(TRAB, 'adendo27', 'desenho_D1', 'estrutura_2t.json.gz')
PASTAS_BU = [os.path.join(TRAB, p) for p in ('amostra2t/arq', 'amostra2t/arq_G', 'amostra2t/arq_t17', 'amostra2t/arq_t17b',
                                             'adendo21/F14_arq', 'adendo24/C3_arq')] + [os.path.join(W, 'dl_bu')]

SEMENTE, NBOOT = 20261110, 2000
PISO, K_PRINC = 30, 20
VARS = ['f1', 'outros', 'bn', 'dc']
REGUA, LIMIAR = 1.785, 1.0
MARGEM = 4430191
DATAS = {'2026': (2026, 10, 25), '2022': (2022, 10, 30), '2018': (2018, 10, 28)}
PUBLICADO_F19 = {'2026': -0.6486475152247274, '2022': 0.12284051203619031, '2018': 0.8971475434552486}

# Tabela de fusos: código do município no TSE (UF ZZ) -> (nome no bweb/perfil, país, zona IANA).
# Fonte do deslocamento em cada data: banco de fusos IANA (tzdata 2026e do sistema), lido com zoneinfo.
# Fonte da zona de cada cidade: nome da cidade no bweb e endereço do local no cadastro de locais de votação do TSE
# (eleitorado_local_votacao_2026, UF ZZ); a zona IANA é a da sede.
FUSOS = {
    29254: ('ABIDJÃ', 'Costa do Marfim', 'Africa/Abidjan'), 29262: ('ABU DHABI', 'Emirados Árabes Unidos', 'Asia/Dubai'),
    99198: ('ABUJA', 'Nigéria', 'Africa/Lagos'), 29270: ('ACCRA', 'Gana', 'Africa/Accra'),
    99325: ('ADIS ABEBA', 'Etiópia', 'Africa/Addis_Ababa'), 30457: ('AMSTERDÃ', 'Países Baixos', 'Europe/Amsterdam'),
    29289: ('AMÃ', 'Jordânia', 'Asia/Amman'), 29297: ('ANCARA', 'Turquia', 'Europe/Istanbul'),
    29300: ('ARGEL', 'Argélia', 'Africa/Algiers'), 29319: ('ARTIGAS', 'Uruguai', 'America/Montevideo'),
    29327: ('ASSUNÇÃO', 'Paraguai', 'America/Asuncion'), 39241: ('ASTANA', 'Cazaquistão', 'Asia/Almaty'),
    29335: ('ATENAS', 'Grécia', 'Europe/Athens'), 39080: ('ATLANTA', 'Estados Unidos', 'America/New_York'),
    99171: ('BAGDÁ', 'Iraque', 'Asia/Baghdad'), 39128: ('BAKU', 'Azerbaijão', 'Asia/Baku'),
    99350: ('BAMAKO', 'Mali', 'Africa/Bamako'), 29343: ('BANGKOK', 'Tailândia', 'Asia/Bangkok'),
    29351: ('BARCELONA', 'Espanha', 'Europe/Madrid'), 99473: ('BAREIN', 'Bahrein', 'Asia/Bahrain'),
    29360: ('BEIRUTE', 'Líbano', 'Asia/Beirut'), 29378: ('BELGRADO', 'Sérvia', 'Europe/Belgrade'),
    38881: ('BELMOPAN', 'Belize', 'America/Belize'), 29386: ('BERLIM', 'Alemanha', 'Europe/Berlin'),
    29394: ('BISSAU', 'Guiné-Bissau', 'Africa/Bissau'), 29408: ('BOGOTÁ', 'Colômbia', 'America/Bogota'),
    29416: ('BOSTON', 'Estados Unidos', 'America/New_York'), 39209: ('BRATISLAVA', 'Eslováquia', 'Europe/Bratislava'),
    39187: ('BRAZZAVILLE', 'Congo', 'Africa/Brazzaville'), 29424: ('BRIDGETOWN', 'Barbados', 'America/Barbados'),
    29432: ('BRUXELAS', 'Bélgica', 'Europe/Brussels'), 29440: ('BUCARESTE', 'Romênia', 'Europe/Bucharest'),
    29459: ('BUDAPESTE', 'Hungria', 'Europe/Budapest'), 29467: ('BUENOS AIRES', 'Argentina', 'America/Argentina/Buenos_Aires'),
    29475: ('CAIENA', 'Guiana Francesa', 'America/Cayenne'), 29483: ('CAIRO', 'Egito', 'Africa/Cairo'),
    29491: ('CAMBERRA', 'Austrália', 'Australia/Sydney'), 30651: ('CANTÃO', 'China', 'Asia/Shanghai'),
    29505: ('CARACAS', 'Venezuela', 'America/Caracas'), 99384: ('CASTRIES', 'Santa Lúcia', 'America/St_Lucia'),
    29513: ('CHICAGO', 'Estados Unidos', 'America/Chicago'), 29521: ('CHUY', 'Uruguai', 'America/Montevideo'),
    29530: ('CIDADE DO CABO', 'África do Sul', 'Africa/Johannesburg'), 29556: ('CIUDAD DEL ESTE', 'Paraguai', 'America/Asuncion'),
    29564: ('CIUDAD GUAYANA', 'Venezuela', 'America/Caracas'), 99210: ('COBIJA', 'Bolívia', 'America/La_Paz'),
    29572: ('COCHABAMBA', 'Bolívia', 'America/La_Paz'), 30929: ('COLOMBO', 'Sri Lanka', 'Asia/Colombo'),
    38903: ('CONACRI', 'Guiné', 'Africa/Conakry'), 29580: ('CONCEPCIÓN', 'Paraguai', 'America/Asuncion'),
    29599: ('COPENHAGUE', 'Dinamarca', 'Europe/Copenhagen'), 38920: ('COTONOU', 'Benin', 'Africa/Porto-Novo'),
    29602: ('CÓRDOBA', 'Argentina', 'America/Argentina/Cordoba'), 29610: ('DACAR', 'Senegal', 'Africa/Dakar'),
    29629: ('DACCA', 'Bangladesh', 'Asia/Dhaka'), 29637: ('DAMASCO', 'Síria', 'Asia/Damascus'),
    38962: ('DAR ES SALAAM', 'Tanzânia', 'Africa/Dar_es_Salaam'), 29653: ('DOHA', 'Catar', 'Asia/Qatar'),
    29661: ('DUBLIN', 'Irlanda', 'Europe/Dublin'), 29645: ('DÍLI', 'Timor-Leste', 'Asia/Dili'),
    99503: ('EDIMBURGO', 'Reino Unido', 'Europe/London'), 29670: ('ENCARNACIÓN', 'Paraguai', 'America/Asuncion'),
    29688: ('ESTOCOLMO', 'Suécia', 'Europe/Stockholm'), 30961: ('FARO', 'Portugal', 'Europe/Lisbon'),
    29696: ('FRANKFURT', 'Alemanha', 'Europe/Berlin'), 30669: ('GABORONE', 'Botsuana', 'Africa/Gaborone'),
    29700: ('GENEBRA', 'Suíça', 'Europe/Zurich'), 29718: ('GEORGETOWN', 'Guiana', 'America/Guyana'),
    98000: ('GUATEMALA', 'Guatemala', 'America/Guatemala'), 29742: ('HAMAMATSU', 'Japão', 'Asia/Tokyo'),
    29750: ('HANÓI', 'Vietnã', 'Asia/Ho_Chi_Minh'), 29769: ('HARARE', 'Zimbábue', 'Africa/Harare'),
    30902: ('HARTFORD', 'Estados Unidos', 'America/New_York'), 29777: ('HAVANA', 'Cuba', 'America/Havana'),
    29785: ('HELSINQUE', 'Finlândia', 'Europe/Helsinki'), 29793: ('HONG KONG', 'Hong Kong', 'Asia/Hong_Kong'),
    29807: ('HOUSTON', 'Estados Unidos', 'America/Chicago'), 29815: ('IAUNDÊ', 'Camarões', 'Africa/Douala'),
    38989: ('IEREVAN', 'Armênia', 'Asia/Yerevan'), 29823: ('IQUITOS', 'Peru', 'America/Lima'),
    29831: ('ISLAMABADE', 'Paquistão', 'Asia/Karachi'), 39306: ('ISTAMBUL', 'Turquia', 'Europe/Istanbul'),
    29840: ('JACARTA', 'Indonésia', 'Asia/Jakarta'), 29173: ('KATMANDU', 'Nepal', 'Asia/Kathmandu'),
    29858: ('KIEV', 'Ucrânia', 'Europe/Kyiv'), 99430: ('KINGSTON-JAMAICA', 'Jamaica', 'America/Jamaica'),
    29874: ('KINSHASA', 'República Democrática do Congo', 'Africa/Kinshasa'), 29882: ('KUAITE', 'Kuwait', 'Asia/Kuwait'),
    29890: ('KUALA LUMPUR', 'Malásia', 'Asia/Kuala_Lumpur'), 29904: ('LA PAZ', 'Bolívia', 'America/La_Paz'),
    29912: ('LAGOS', 'Nigéria', 'Africa/Lagos'), 29939: ('LIBREVILLE', 'Gabão', 'Africa/Libreville'),
    99341: ('LILONGUE', 'Malawi', 'Africa/Blantyre'), 29947: ('LIMA', 'Peru', 'America/Lima'),
    29955: ('LISBOA', 'Portugal', 'Europe/Lisbon'), 39160: ('LIUBLIANA', 'Eslovênia', 'Europe/Ljubljana'),
    29963: ('LOMÉ', 'Togo', 'Africa/Lome'), 29971: ('LONDRES', 'Reino Unido', 'Europe/London'),
    29980: ('LOS ANGELES', 'Estados Unidos', 'America/Los_Angeles'), 29998: ('LUANDA', 'Angola', 'Africa/Luanda'),
    99287: ('LUSACA', 'Zâmbia', 'Africa/Lusaka'), 30066: ('MADRI', 'Espanha', 'Europe/Madrid'),
    39263: ('MALABO', 'Guiné Equatorial', 'Africa/Malabo'), 30082: ('MANILA', 'Filipinas', 'Asia/Manila'),
    30074: ('MANÁGUA', 'Nicarágua', 'America/Managua'), 30090: ('MAPUTO', 'Moçambique', 'Africa/Maputo'),
    99511: ('MARSELHA', 'França', 'Europe/Paris'), 39102: ('MASCATE', 'Omã', 'Asia/Muscat'),
    39004: ('MENDOZA', 'Argentina', 'America/Argentina/Mendoza'), 30104: ('MEXICO', 'México', 'America/Mexico_City'),
    30112: ('MIAMI', 'Estados Unidos', 'America/New_York'), 30120: ('MILÃO', 'Itália', 'Europe/Rome'),
    30147: ('MONTEVIDÉU', 'Uruguai', 'America/Montevideo'), 30155: ('MONTREAL', 'Canadá', 'America/Toronto'),
    30163: ('MOSCOU', 'Rússia', 'Europe/Moscow'), 30171: ('MUMBAI', 'Índia', 'Asia/Kolkata'),
    30180: ('MUNIQUE', 'Alemanha', 'Europe/Berlin'), 30198: ('NAGÓIA', 'Japão', 'Asia/Tokyo'),
    30201: ('NAIRÓBI', 'Quênia', 'Africa/Nairobi'), 99180: ('NASSAU', 'Bahamas', 'America/Nassau'),
    39322: ('NICOSIA', 'Chipre', 'Asia/Nicosia'), 30210: ('NOVA DELHI', 'Índia', 'Asia/Kolkata'),
    30228: ('NOVA YORK', 'Estados Unidos', 'America/New_York'), 99490: ('ORLANDO', 'Estados Unidos', 'America/New_York'),
    30244: ('OSLO', 'Noruega', 'Europe/Oslo'), 30252: ('OTTAWA', 'Canadá', 'America/Toronto'),
    30260: ('PANAMA', 'Panamá', 'America/Panama'), 30279: ('PARAMARIBO', 'Suriname', 'America/Paramaribo'),
    30287: ('PARIS', 'França', 'Europe/Paris'), 30295: ('PASO LOS LIBRES', 'Argentina', 'America/Argentina/Cordoba'),
    30309: ('PEDRO JUAN CABALLERO', 'Paraguai', 'America/Asuncion'), 30317: ('PEQUIM', 'China', 'Asia/Shanghai'),
    30325: ('PORT OF SPAIN', 'Trinidad e Tobago', 'America/Port_of_Spain'), 30341: ('PORTO', 'Portugal', 'Europe/Lisbon'),
    30333: ('PORTO PRÍNCIPE', 'Haiti', 'America/Port-au-Prince'), 30350: ('PRAGA', 'República Tcheca', 'Europe/Prague'),
    30368: ('PRAIA', 'Cabo Verde', 'Atlantic/Cape_Verde'), 30376: ('PRETÓRIA', 'África do Sul', 'Africa/Johannesburg'),
    99155: ('PUERTO IGUAZÚ', 'Argentina', 'America/Argentina/Cordoba'), 99236: ('PUERTO QUIJARRO', 'Bolívia', 'America/La_Paz'),
    99295: ('PYONGYANG', 'Coreia do Norte', 'Asia/Pyongyang'), 30392: ('QUITO', 'Equador', 'America/Guayaquil'),
    30406: ('RABAT', 'Marrocos', 'Africa/Casablanca'), 30414: ('RAMALLAH', 'Palestina', 'Asia/Hebron'),
    30422: ('RIADE', 'Arábia Saudita', 'Asia/Riyadh'), 30430: ('RIO BRANCO', 'Uruguai', 'America/Montevideo'),
    99244: ('RIVERA', 'Uruguai', 'America/Montevideo'), 30449: ('ROMA', 'Itália', 'Europe/Rome'),
    99147: ('SAINT JOHNS', 'Antígua e Barbuda', 'America/Antigua'), 30465: ('SALTO DEL GUAIRÁ', 'Paraguai', 'America/Asuncion'),
    30473: ('SANTA CRUZ DE LA SIERRA', 'Bolívia', 'America/La_Paz'), 99279: ('SANTA ELENA DE UAIRÉN', 'Venezuela', 'America/Caracas'),
    30481: ('SANTIAGO', 'Chile', 'America/Santiago'), 30988: ('SARAJEVO', 'Bósnia e Herzegovina', 'Europe/Sarajevo'),
    30538: ('SEUL', 'Coreia do Sul', 'Asia/Seoul'), 29548: ('SINGAPURA', 'Singapura', 'Asia/Singapore'),
    99333: ('ST GEORGES DE LOYAPOCK', 'Guiana Francesa', 'America/Cayenne'), 30562: ('SYDNEY', 'Austrália', 'Australia/Sydney'),
    30490: ('SÃO DOMINGOS', 'República Dominicana', 'America/Santo_Domingo'), 30503: ('SÃO FRANCISCO', 'Estados Unidos', 'America/Los_Angeles'),
    30511: ('SÃO JOSÉ', 'Costa Rica', 'America/Costa_Rica'), 30520: ('SÃO SALVADOR', 'El Salvador', 'America/El_Salvador'),
    39225: ('SÃO TOMÉ', 'São Tomé e Príncipe', 'Africa/Sao_Tome'), 30546: ('SÓFIA', 'Bulgária', 'Europe/Sofia'),
    30570: ('TAIPÉ', 'Taiwan', 'Asia/Taipei'), 99317: ('TALIN', 'Estônia', 'Europe/Tallinn'),
    99104: ('TBILISI', 'Geórgia', 'Asia/Tbilisi'), 30597: ('TEERÃ', 'Irã', 'Asia/Tehran'),
    30600: ('TEGUCIGALPA', 'Honduras', 'America/Tegucigalpa'), 30619: ('TEL AVIV', 'Israel', 'Asia/Jerusalem'),
    99139: ('TIRANA', 'Albânia', 'Europe/Tirane'), 30635: ('TORONTO', 'Canadá', 'America/Toronto'),
    30686: ('TRÍPOLI', 'Líbia (vota em Túnis)', 'Africa/Tunis'), 30708: ('TUNIS', 'Tunísia', 'Africa/Tunis'),
    30627: ('TÓQUIO', 'Japão', 'Asia/Tokyo'), 39284: ('UAGADUGU', 'Burkina Faso', 'Africa/Ouagadougou'),
    39063: ('VANCOUVER', 'Canadá', 'America/Vancouver'), 30740: ('VARSÓVIA', 'Polônia', 'Europe/Warsaw'),
    30767: ('VIENA', 'Áustria', 'Europe/Vienna'), 30783: ('WASHINGTON', 'Estados Unidos', 'America/New_York'),
    30805: ('WELLINGTON', 'Nova Zelândia', 'Pacific/Auckland'), 30821: ('WINDHOEK', 'Namíbia', 'Africa/Windhoek'),
    30848: ('XANGAI', 'China', 'Asia/Shanghai'), 99376: ('YANGON', 'Mianmar', 'Asia/Yangon'),
    39020: ('ZAGREB', 'Croácia', 'Europe/Zagreb'), 30864: ('ZURIQUE', 'Suíça', 'Europe/Zurich'),
}


def log(*a):
    print(time.strftime('%H:%M:%S'), *a, file=sys.stderr, flush=True)


def _limpo(o):
    """Troca NaN e infinito por None e tipos do numpy por tipos do Python, para o JSON sair válido."""
    if isinstance(o, dict):
        return {str(k): _limpo(v) for k, v in o.items()}
    if isinstance(o, (list, tuple)):
        return [_limpo(v) for v in o]
    if hasattr(o, 'item') and not isinstance(o, (str, bytes)):
        try:
            o = o.item()
        except Exception:
            return str(o)
    if isinstance(o, float) and (o != o or o in (float('inf'), float('-inf'))):
        return None
    return o


def salvar_json(obj, caminho):
    tmp = caminho + '.part'
    with open(tmp, 'w') as f:
        json.dump(_limpo(obj), f, ensure_ascii=False, indent=1, allow_nan=False, default=str)
    os.replace(tmp, caminho)


# ------------------------------------------------------------------------------------------------ fusos
def versao_tzdata():
    for p in zoneinfo.TZPATH:
        q = os.path.join(p, 'tzdata.zi')
        if os.path.exists(q):
            return open(q).readline().strip().lstrip('# ').strip()
    return 'desconhecida'


def deslocamento(zona, data):
    t = datetime.datetime(*data, 12, 0, tzinfo=zoneinfo.ZoneInfo(zona))
    return t.utcoffset().total_seconds() / 3600.0


def fracoes(cod, ano):
    """(deslocamento UTC, f = fração da janela 8h-17h local antes das 8h de Brasília, g = fração depois das 17h de Brasília)."""
    data = DATAS[ano]
    o = deslocamento(FUSOS[cod][2], data)
    ob = deslocamento('America/Sao_Paulo', data)
    f = min(1.0, max(0.0, (o - ob) / 9.0))
    g = min(1.0, max(0.0, (ob - o) / 9.0))
    return o, f, g


# ------------------------------------------------------------------------------------------------ estrutura (sem votos)
def chave_ord(k):
    a = k.split('|')
    return (a[0], int(a[1]), int(a[2]), int(a[3]))


def _perfil_zip(zp):
    z = zipfile.ZipFile(zp)
    nome = [n for n in z.namelist() if n.lower().endswith('.csv')][0]
    out = {}
    with z.open(nome) as fh:
        cab = [c.strip().strip('"') for c in fh.readline().decode('latin1').strip().split(';')]
        assert cab[3:8] == ['SG_UF', 'CD_MUNICIPIO', 'NM_MUNICIPIO', 'NR_ZONA', 'NR_SECAO'], cab
        assert cab[-4:] == ['QT_ELEITORES', 'QT_ELEITORES_BIOMETRIA', 'QT_ELEITORES_DEFICIENCIA', 'QT_ELEITORES_NOME_SOCIAL'], cab
        for linha in fh:
            a = linha.split(b';', 8)
            b = linha.rstrip(b'\r\n').rsplit(b';', 4)
            k = (a[3].strip(b'"'), int(a[4].strip(b'"')), int(a[6]), int(a[7]))
            r = out.get(k)
            if r is None:
                r = out[k] = [0, 0]
            r[0] += int(b[1]); r[1] += int(b[2])
    return {f"{k[0].decode()}|{k[1]}|{k[2]}|{k[3]}": v for k, v in out.items()}


def _ler_bu_sbm(p):
    from ber import parse
    partes = p.split(os.sep)
    k = f'{partes[-5].upper()}|{int(partes[-4])}|{int(partes[-3])}|{int(partes[-2])}'
    try:
        env = parse(open(p, 'rb').read())[0][2]
        octet = [n for n in env if (n[0], n[1]) == (0, 4)][-1][2]
        bu = parse(octet)[0][2]
        ctx = [[int.from_bytes(c[2], 'big') for c in n[2]] for n in bu
               if (n[0], n[1]) == (2, 1) and isinstance(n[2], list) and len(n[2]) == 3 and all((c[0], c[1]) == (0, 2) for c in n[2])]
        return k, ctx
    except Exception as e:
        return k, repr(e)


def estrutura():
    """Arquivos de estrutura (sem votos) em W: perfil_secao.json.gz, locais_tipo.json.gz, bu_sbm_final.json."""
    from multiprocessing import Pool
    os.makedirs(W, exist_ok=True)
    pf = os.path.join(W, 'perfil_secao.json.gz')
    if not os.path.exists(pf):
        zs = sorted(glob.glob(os.path.join(PERFIL_DIR, 'perfil_eleitor_secao_2026_*.zip')), key=lambda p: -os.path.getsize(p))
        tudo = {}
        with Pool(3) as P:
            for out in P.imap_unordered(_perfil_zip, zs):
                tudo.update(out)
        with gzip.open(pf, 'wt') as f:
            json.dump({'secoes': tudo}, f, separators=(',', ':'))
        log('perfil', len(tudo))
    lt = os.path.join(W, 'locais_tipo.json.gz')
    if not os.path.exists(lt):
        z = zipfile.ZipFile(LOCAIS_ZIP); out = {}
        with z.open('eleitorado_local_votacao_2026_BRASIL.csv') as fh:
            rd = csv.reader(io.TextIOWrapper(fh, encoding='latin1', newline=''), delimiter=';')
            cab = next(rd); ix = {c: i for i, c in enumerate(cab)}
            for r in rd:
                if r[ix['NR_TURNO']] == '2' and r[ix['DS_TIPO_LOCAL']] != 'Convencional':
                    out[f"{r[ix['SG_UF']]}|{int(r[ix['CD_MUNICIPIO']])}|{int(r[ix['NR_ZONA']])}|{int(r[ix['NR_SECAO']])}"] = \
                        [r[ix['DS_TIPO_LOCAL']], r[ix['NM_LOCAL_VOTACAO']]]
        with gzip.open(lt, 'wt') as f:
            json.dump(out, f, ensure_ascii=False, separators=(',', ':'))
        log('locais não convencionais', len(out))
    sbm = {}; info = {}
    with Pool(3) as P:
        for pasta in PASTAS_BU:
            bus = sorted(glob.glob(os.path.join(pasta, '*', '*', '*', '*', '*-bu.dat')))
            n0 = len(sbm)
            for k, ctx in P.imap_unordered(_ler_bu_sbm, bus, chunksize=50):
                if isinstance(ctx, list) and len(ctx) == 1 and k not in sbm:
                    sbm[k] = ctx[0] + [os.path.relpath(pasta, TRAB)]
            info[os.path.relpath(pasta, TRAB)] = {'arquivos': len(bus), 'secoes_novas': len(sbm) - n0}
    salvar_json({'info': info, 'secoes': sbm}, os.path.join(W, 'bu_sbm_final.json'))
    log('boletins lidos', len(sbm), info)


# ------------------------------------------------------------------------------------------------ bases e pareamento
def montar(d):
    """Arrays das seções com os dois turnos válidos (P1), em ordem de chave."""
    ks, rows = [], []
    for k in sorted(d):
        v = d[k]
        a, b = v.get('1'), v.get('2')
        if not a or not b:
            continue
        if a['comp'] <= 0 or b['comp'] <= 0 or a['L'] + a['R'] <= 0 or b['L'] + b['R'] <= 0 or a['apt'] <= 0 or b['apt'] <= 0:
            continue
        loc = b.get('loc')
        ks.append(k)
        rows.append((a['L'], a['R'], a['O'], a['B'] + a['N'], a['comp'], a['apt'], b['L'], b['R'], b['B'] + b['N'], b['comp'], b['apt'],
                     loc if isinstance(loc, int) else -1))
    A = np.array(rows, float)
    L1, R1, O1, BN1, C1, A1, L2, R2, BN2, C2, A2, loc = A.T
    T = {'k': np.array(ks), 'uf': np.array([k.split('|')[0] for k in ks]), 'mun': np.array([int(k.split('|')[1]) for k in ks]),
         'zona': np.array([int(k.split('|')[2]) for k in ks]), 'loc': loc.astype(np.int64),
         'f1': 100 * L1 / (L1 + R1), 'outros': 100 * O1 / (L1 + R1 + O1), 'bn': 100 * BN1 / C1, 'dc': 100 * (C2 / A2 - C1 / A1),
         'w': L2 + R2, 'L2': L2, 'R2': R2, 'C2': C2}
    T['y'] = 100 * L2 / (L2 + R2) - T['f1']
    T['ybn'] = 100 * (BN2 / C2 - BN1 / C1)
    return T


def sub(T, m):
    return {c: v[m] for c, v in T.items()}


def vizinhos(Zb, Ze, K):
    idx = np.empty((Ze.shape[0], K), np.int64); dist = np.empty((Ze.shape[0], K))
    for i in range(Ze.shape[0]):
        dd = ((Zb - Ze[i]) ** 2).sum(1)
        t = np.partition(dd, K - 1)[K - 1]
        cand = np.flatnonzero(dd <= t)
        o = cand[np.lexsort((cand, dd[cand]))][:K]
        idx[i] = o; dist[i] = np.sqrt(dd[o])
    return idx, dist


def contraf(valB, wB, idx):
    wj = wB[idx]
    return (wj * valB[idx]).sum(1) / wj.sum(1)


def preparar_ano(ano):
    """Carrega a base, monta, pareia (50 pares; 10 e 20 por prefixo) e devolve E (exterior), B (Brasil), índices."""
    d = carregar(os.path.join(DADOS, f'secoes{ano}.json.gz'))
    tot = {'L2': sum(v['2']['L'] for v in d.values() if v.get('2')), 'R2': sum(v['2']['R'] for v in d.values() if v.get('2')),
           'L2_zz': sum(v['2']['L'] for k, v in d.items() if v.get('2') and k.startswith('ZZ|')),
           'R2_zz': sum(v['2']['R'] for k, v in d.items() if v.get('2') and k.startswith('ZZ|')),
           'comp2_zz': sum(v['2']['comp'] for k, v in d.items() if v.get('2') and k.startswith('ZZ|')),
           'apt2_zz': sum(v['2']['apt'] for k, v in d.items() if v.get('2') and k.startswith('ZZ|')),
           'secoes_zz': sum(1 for k, v in d.items() if v.get('2') and k.startswith('ZZ|'))}
    T = montar(d)
    del d; gc.collect()
    ext = T['uf'] == 'ZZ'; piso = T['w'] >= PISO
    E = sub(T, ext & piso); B = sub(T, (~ext) & piso)
    X = np.column_stack([B[c] for c in VARS])
    mu, sd = X.mean(0), X.std(0, ddof=1)
    cache = os.path.join(W, f'pares_{ano}.npz')
    Zb = (X - mu) / sd; Ze = (np.column_stack([E[c] for c in VARS]) - mu) / sd
    if os.path.exists(cache) and np.load(cache)['idx50'].shape[0] == len(E['w']):
        z = np.load(cache); idx50, idx3 = z['idx50'], z['idx3']
    else:
        idx50, _ = vizinhos(Zb, Ze, 50)
        idx3, _ = vizinhos(Zb[:, :3], Ze[:, :3], K_PRINC)
        np.savez_compressed(cache, idx50=idx50, idx3=idx3)
    cont = {'exterior_dois_turnos_validos': int(ext.sum()), 'exterior_com_piso_30': int((ext & piso).sum()),
            'brasil_dois_turnos_validos': int((~ext).sum()), 'brasil_com_piso_30': int(((~ext) & piso).sum())}
    return {'T': T, 'E': E, 'B': B, 'idx50': idx50, 'idx3': idx3, 'mu': mu, 'sd': sd, 'cont': cont, 'tot': tot}


# ------------------------------------------------------------------------------------------------ estatística
def sorteios(G, semente=SEMENTE, n=NBOOT):
    rng = np.random.default_rng(semente)
    C = np.zeros((n, G))
    for r in range(n):
        C[r] = np.bincount(rng.integers(0, G, G), minlength=G)
    return C


def media_pond(d, w, g, C):
    """Média ponderada de d com bootstrap de grupos (C: réplicas x grupos) e CR1 por grupo."""
    d = np.asarray(d, float); w = np.asarray(w, float)
    G = C.shape[1]
    est = float((w * d).sum() / w.sum())
    S = np.bincount(g, weights=w * d, minlength=G); Wg = np.bincount(g, weights=w, minlength=G)
    num, den = C @ S, C @ Wg
    ok = den > 0
    bs = num[ok] / den[ok]
    eg = np.bincount(g, weights=w * (d - est), minlength=G)
    Gu = int((Wg > 0).sum())
    cr1 = float(np.sqrt(Gu / (Gu - 1) * (eg ** 2).sum()) / w.sum()) if Gu > 1 else None
    ep = float(bs.std(ddof=1))
    return {'est': est, 'ep': ep, 'z': est / ep if ep > 0 else None, 'ep_cr1': cr1,
            'ic95': [float(np.percentile(bs, 2.5)), float(np.percentile(bs, 97.5))], 'grupos': Gu, 'n': int(len(d)), 'peso': float(w.sum())}


def wls_cluster(y, X, w, g):
    """MQP com constante; devolve coeficientes e CR1 por grupo. X: (n, k) sem a constante."""
    y = np.asarray(y, float); w = np.asarray(w, float)
    Xc = np.column_stack([np.ones(len(y)), X])
    XtW = Xc.T * w
    inv = np.linalg.inv(XtW @ Xc)
    b = inv @ (XtW @ y)
    e = y - Xc @ b
    _, gi = np.unique(g, return_inverse=True)
    G = gi.max() + 1; k = Xc.shape[1]
    Sg = np.zeros((G, k))
    for j in range(k):
        Sg[:, j] = np.bincount(gi, weights=w * Xc[:, j] * e, minlength=G)
    c = G / (G - 1) * (len(y) - 1) / (len(y) - k)
    V = c * inv @ (Sg.T @ Sg) @ inv
    return b, np.sqrt(np.diag(V))


def dose(D, f, w, g, C, nome='f'):
    """Inclinação de D contra f (MQP por w), bootstrap de grupos, CR1 por grupo, permutação de f entre grupos."""
    D = np.asarray(D, float); f = np.asarray(f, float); w = np.asarray(w, float)
    b, se = wls_cluster(D, f[:, None], w, g)
    G = C.shape[1]
    A = np.column_stack([w, w * f, w * D, w * f * f, w * f * D])
    S = np.zeros((G, 5))
    for j in range(5):
        S[:, j] = np.bincount(g, weights=A[:, j], minlength=G)
    R = C @ S
    den = R[:, 0] * R[:, 3] - R[:, 1] ** 2
    ok = den > 1e-9 * (R[:, 0] ** 2).clip(1e-12)
    bs = (R[ok, 0] * R[ok, 4] - R[ok, 1] * R[ok, 2]) / den[ok]
    ep = float(bs.std(ddof=1))
    # permutação de f entre grupos: cada grupo recebe o vetor de f de outro grupo só quando f é constante no grupo;
    # aqui a permutação é do valor médio ponderado de f do grupo (os grupos são países, quase todos com um fuso só).
    fg = np.bincount(g, weights=w * f, minlength=G) / np.where(np.bincount(g, weights=w, minlength=G) > 0, np.bincount(g, weights=w, minlength=G), 1)
    usados = np.flatnonzero(np.bincount(g, weights=w, minlength=G) > 0)
    rng = np.random.default_rng(SEMENTE + 7)
    cont = 0; nper = 2000; perms = np.empty(nper)
    for r in range(nper):
        p = fg.copy(); p[usados] = fg[rng.permutation(usados)]
        fp = p[g]
        s0, s1, s2, s3, s4 = w.sum(), (w * fp).sum(), (w * D).sum(), (w * fp * fp).sum(), (w * fp * D).sum()
        perms[r] = (s0 * s4 - s1 * s2) / (s0 * s3 - s1 ** 2)
    # a estatística de referência da permutação usa f médio do país (igual a f quando o país tem um fuso só)
    fpais = fg[g]
    s0, s1, s2, s3, s4 = w.sum(), (w * fpais).sum(), (w * D).sum(), (w * fpais * fpais).sum(), (w * fpais * D).sum()
    b_pais = (s0 * s4 - s1 * s2) / (s0 * s3 - s1 ** 2)
    p_perm = float((np.abs(perms) >= abs(b_pais)).mean())
    return {'variavel': nome, 'constante': float(b[0]), 'inclinacao': float(b[1]), 'ep': ep, 'z': float(b[1] / ep) if ep > 0 else None,
            'ep_cr1_pais': float(se[1]), 'ic95': [float(np.percentile(bs, 2.5)), float(np.percentile(bs, 97.5))],
            'replicas_validas': int(ok.sum()), 'p_permutacao_entre_paises': p_perm, 'inclinacao_com_f_medio_do_pais': float(b_pais),
            'cidades': int(len(D)), 'paises': int((np.bincount(g, weights=w, minlength=G) > 0).sum())}


def por_cidade(E, dif, extra=None):
    """Agrega por cidade: D, peso, f1, seções."""
    cods = sorted(set(E['mun'].tolist()))
    pos = {c: j for j, c in enumerate(cods)}
    gi = np.array([pos[c] for c in E['mun']])
    w = E['w']
    Wc = np.bincount(gi, weights=w)
    out = {'cod': np.array(cods), 'W': Wc, 'D': np.bincount(gi, weights=w * dif) / Wc,
           'f1': np.bincount(gi, weights=w * E['f1']) / Wc, 'y': np.bincount(gi, weights=w * E['y']) / Wc,
           'n': np.bincount(gi).astype(int), 'gi': gi}
    for nome, v in (extra or {}).items():
        out[nome] = np.bincount(gi, weights=w * v) / Wc
    return out


def did_cidades(cur, ref, paises_idx, C, campo='D'):
    """DiD da regra A1/A2. cur e ref: saídas de por_cidade para o ano de cima e o de referência."""
    ref_pos = {int(c): j for j, c in enumerate(ref['cod'])}
    pais_ref = collections.defaultdict(list)
    for j, c in enumerate(ref['cod']):
        pais_ref[FUSOS[int(c)][1]].append(j)
    d, w, g, modo, cods = [], [], [], [], []
    fora = []
    for j, c in enumerate(cur['cod']):
        c = int(c); pais = FUSOS[c][1]
        if c in ref_pos:
            r = ref[campo][ref_pos[c]]; m = 'mesma cidade'
        elif pais_ref.get(pais):
            jj = pais_ref[pais]
            r = float((ref['W'][jj] * ref[campo][jj]).sum() / ref['W'][jj].sum()); m = 'país'
        else:
            fora.append(c); continue
        d.append(cur[campo][j] - r); w.append(cur['W'][j]); g.append(paises_idx[pais]); modo.append(m); cods.append(c)
    d, w, g = np.array(d), np.array(w), np.array(g)
    return {'d': d, 'w': w, 'g': g, 'modo': modo, 'cods': cods, 'fora': fora, 'res': media_pond(d, w, g, C)}


# ------------------------------------------------------------------------------------------------ plantio
def plantar(L2, R2, frac, rng, forma='uniforme'):
    """Votos que saem de R2 e entram em L2. frac: escalar ou vetor (em fração: delta/100 para a forma uniforme)."""
    n = (L2 + R2).astype(np.int64); r = R2.astype(np.int64)
    p = np.clip(np.broadcast_to(np.asarray(frac, float), n.shape), 0, 1)
    x = rng.binomial(n, p) if forma == 'uniforme' else rng.binomial(r, p)
    return np.minimum(x, r).astype(float)


def y_plantado(S, x):
    return 100 * (S['L2'] + x) / S['w'] - S['f1']


# ------------------------------------------------------------------------------------------------ leituras
def ler_a(est, ep):
    if est <= -LIMIAR and abs(est) > 3 * ep:
        return 'SINAL'
    if abs(est) < 0.4 and ep <= 0.2:
        return 'SEM SINAL'
    return 'INCONCLUSIVO'


def ler_b(b26, ep26, b22):
    if b26 <= -LIMIAR and abs(b26) > 3 * ep26 and abs(b22) < 0.4:
        return 'SINAL'
    if abs(b26) < 0.4:
        return 'SEM SINAL'
    return 'INCONCLUSIVO'


def ler_c(d, ep, n):
    if n < 100:
        return 'SEM PODER'
    if d <= -LIMIAR and abs(d) > 4 * ep:
        return 'SINAL'
    if abs(d) < 0.4 and ep <= 0.2:
        return 'SEM SINAL'
    return 'INCONCLUSIVO'


def poder(obs, plantado, ep, delta, n_ep, dispara):
    desloc = plantado - obs
    rec = desloc / (-delta)
    medida = bool(rec >= 0.8 and abs(desloc) > n_ep * ep)
    return {'delta': delta, 'estatistica_com_plantio': plantado, 'deslocamento': desloc, 'recuperacao': rec,
            'deslocamento_em_ep': abs(desloc) / ep if ep > 0 else None, 'poder_de_medida': medida,
            'criterio_de_sinal_dispara_com_plantio': bool(dispara), 'poder_pleno': bool(medida and dispara)}


# ------------------------------------------------------------------------------------------------ partes (a) e (b)
CTX = {}


def partes_ab(out):
    anos = ['2026', '2022', '2018']
    paises = sorted({v[1] for v in FUSOS.values()})
    pidx = {p: j for j, p in enumerate(paises)}
    C = sorteios(len(paises))
    dados = {}; cid = {}; res_ano = {}
    for ano in anos:
        log('ano', ano)
        A = preparar_ano(ano)
        E, B = A['E'], A['B']
        faltam = sorted({int(c) for c in E['mun']} - set(FUSOS))
        if faltam:
            raise SystemExit(f'cidade sem fuso na tabela: {faltam}')
        idx = A['idx50'][:, :K_PRINC]
        m = contraf(B['y'], B['w'], idx); dif = E['y'] - m
        mbn = contraf(B['ybn'], B['w'], idx); difbn = E['ybn'] - mbn
        ext = {'difbn': difbn}
        for K in (10, 50):
            ext[f'difK{K}'] = E['y'] - contraf(B['y'], B['w'], A['idx50'][:, :K])
        ext['dif3'] = E['y'] - contraf(B['y'], B['w'], A['idx3'])
        c = por_cidade(E, dif, {n: v for n, v in ext.items()})
        c['pais'] = np.array([pidx[FUSOS[int(x)][1]] for x in c['cod']])
        fr = [fracoes(int(x), ano) for x in c['cod']]
        c['o'] = np.array([t[0] for t in fr]); c['f'] = np.array([t[1] for t in fr]); c['g'] = np.array([t[2] for t in fr])
        cid[ano] = c
        gsec = np.array([pidx[FUSOS[int(x)][1]] for x in E['mun']])
        nivel = media_pond(dif, E['w'], gsec, C)
        # ep por cidade (como o F19), só para comparar
        cods = sorted(set(E['mun'].tolist())); pc = {x: j for j, x in enumerate(cods)}
        Ccid = sorteios(len(cods), SEMENTE + 1)
        nivel_cid = media_pond(dif, E['w'], np.array([pc[x] for x in E['mun']]), Ccid)
        eq = {}
        for v, s in zip(VARS, A['sd']):
            me = float((E['w'] * E[v]).sum() / E['w'].sum()); mp = float((E['w'] * contraf(B[v], B['w'], idx)).sum() / E['w'].sum())
            eq[v] = {'exterior': me, 'pares': mp, 'dif_em_dp': (me - mp) / float(s)}
        res_ano[ano] = {
            'contagens': A['cont'], 'cidades_com_secao': int(len(c['cod'])), 'paises_com_secao': int(len(set(c['pais'].tolist()))),
            'votos_finalistas_exterior_com_piso': float(E['w'].sum()),
            'virada_exterior': float((E['w'] * E['y']).sum() / E['w'].sum()), 'virada_pares': float((E['w'] * m).sum() / E['w'].sum()),
            'virada_brasil_candidatas': float((B['w'] * B['y']).sum() / B['w'].sum()),
            'D_nivel': nivel['est'], 'ep_por_pais': nivel['ep'], 'ep_cr1_por_pais': nivel['ep_cr1'], 'ic95_por_pais': nivel['ic95'],
            'ep_por_cidade': nivel_cid['ep'], 'D_publicado_F19': PUBLICADO_F19[ano], 'diferenca_para_o_F19': nivel['est'] - PUBLICADO_F19[ano],
            'D_branco_nulo_espelho': media_pond(difbn, E['w'], gsec, C), 'equilibrio': eq, 'totais': A['tot'],
            'padronizacao': {v: {'media': float(a), 'dp': float(b)} for v, a, b in zip(VARS, A['mu'], A['sd'])}}
        log(f"  D {nivel['est']:.4f} (F19 {PUBLICADO_F19[ano]:.4f}) ep país {nivel['ep']:.3f} ep cidade {nivel_cid['ep']:.3f}")
        dados[ano] = {'E': E, 'dif': dif, 'gsec': gsec, 'idx': idx,
                      'B': {k: B[k] for k in ('y', 'w', 'L2', 'R2', 'f1')} if ano == '2026' else None}
        if ano == '2026':
            out['brasil_2026'] = {'votos_finalistas_brasil_2t': float(A['tot']['L2'] + A['tot']['R2'] - A['tot']['L2_zz'] - A['tot']['R2_zz']),
                                  'votos_finalistas_total_2t': float(A['tot']['L2'] + A['tot']['R2']),
                                  'margem_total': float(A['tot']['L2'] - A['tot']['R2']),
                                  'regua_recalculada': 100 * (A['tot']['L2'] - A['tot']['R2']) / 2 / (A['tot']['L2'] + A['tot']['R2'])}
            T26 = A['T']; mu26, sd26 = A['mu'], A['sd']
        del A; gc.collect()
    out['niveis_por_ano'] = res_ano
    salvar_json(out, os.path.join(W, 'parcial_ab.json'))

    # ------------------------------------------------------------ (a) diferença em diferenças
    a = {}
    did = did_cidades(cid['2026'], cid['2022'], pidx, C)
    P = did['res']
    a['principal'] = {'DiD': P['est'], 'ep_por_pais': P['ep'], 'z': P['z'], 'ic95': P['ic95'], 'ep_cr1_por_pais': P['ep_cr1'],
                      'cidades': P['n'], 'paises': P['grupos'], 'peso_votos_2026': P['peso'],
                      'cidades_pareadas_pela_mesma_cidade': sum(1 for x in did['modo'] if x == 'mesma cidade'),
                      'cidades_pareadas_pelo_pais': [FUSOS[c][0] for c, x in zip(did['cods'], did['modo']) if x == 'país'],
                      'cidades_fora_sem_referencia': [FUSOS[c][0] for c in did['fora']],
                      'peso_fora': float(sum(cid['2026']['W'][list(cid['2026']['cod']).index(c)] for c in did['fora'])),
                      'leitura': ler_a(P['est'], P['ep'])}
    lado = {}
    # só cidades nos dois anos
    comuns = [c for c in did['cods'] if did['modo'][did['cods'].index(c)] == 'mesma cidade']
    mk = np.array([m_ == 'mesma cidade' for m_ in did['modo']])
    lado['so_cidades_nos_dois_anos'] = media_pond(did['d'][mk], did['w'][mk], did['g'][mk], C)
    # por país
    def por_pais(c):
        G = len(paises)
        Wp = np.bincount(c['pais'], weights=c['W'], minlength=G); Dp = np.bincount(c['pais'], weights=c['W'] * c['D'], minlength=G) / np.where(Wp > 0, Wp, 1)
        return Wp, Dp
    W26, D26p = por_pais(cid['2026']); W22, D22p = por_pais(cid['2022']); W18, D18p = por_pais(cid['2018'])
    amb = (W26 > 0) & (W22 > 0)
    lado['por_pais'] = media_pond((D26p - D22p)[amb], W26[amb], np.flatnonzero(amb), C)
    # diferença simples dos agregados, com bootstrap conjunto de países
    def boot_dif(ca, cb):
        G = len(paises)
        Sa = np.bincount(ca['pais'], weights=ca['W'] * ca['D'], minlength=G); Wa = np.bincount(ca['pais'], weights=ca['W'], minlength=G)
        Sb = np.bincount(cb['pais'], weights=cb['W'] * cb['D'], minlength=G); Wb = np.bincount(cb['pais'], weights=cb['W'], minlength=G)
        est = Sa.sum() / Wa.sum() - Sb.sum() / Wb.sum()
        na, da, nb, db = C @ Sa, C @ Wa, C @ Sb, C @ Wb
        ok = (da > 0) & (db > 0)
        bs = na[ok] / da[ok] - nb[ok] / db[ok]
        return {'est': float(est), 'ep': float(bs.std(ddof=1)), 'ic95': [float(np.percentile(bs, 2.5)), float(np.percentile(bs, 97.5))]}
    lado['diferenca_simples_dos_agregados'] = boot_dif(cid['2026'], cid['2022'])
    lado['media_sem_peso_das_cidades'] = media_pond(did['d'], np.ones(len(did['d'])), did['g'], C)
    lado['mediana_das_cidades'] = float(np.median(did['d']))
    for nome, campo in (('10_pares', 'difK10'), ('50_pares', 'difK50'), ('sem_variacao_do_comparecimento', 'dif3'), ('espelho_branco_nulo', 'difbn')):
        lado[nome] = did_cidades(cid['2026'], cid['2022'], pidx, C, campo)['res']
    loo = {}
    for p in sorted(set(did['g'].tolist())):
        s = did['g'] != p
        loo[paises[p]] = float((did['w'][s] * did['d'][s]).sum() / did['w'][s].sum())
    pmin = min(loo, key=loo.get); pmax = max(loo, key=loo.get)
    lado['tirando_um_pais'] = {'minimo': loo[pmin], 'sem_o_pais_min': pmin, 'maximo': loo[pmax], 'sem_o_pais_max': pmax}
    # por grupo de dose
    f26 = {int(c): f for c, f in zip(cid['2026']['cod'], cid['2026']['f'])}
    fd = np.array([f26[c] for c in did['cods']])
    grupos_f = {}
    for nome, s in (('f = 0 (Américas)', fd == 0), ('0 < f < 1', (fd > 0) & (fd < 1)), ('f = 1 (Ásia e Oceania)', fd >= 1)):
        if s.sum() > 0:
            grupos_f[nome] = media_pond(did['d'][s], did['w'][s], did['g'][s], C)
    lado['DiD_por_grupo_de_dose'] = grupos_f
    # placebo 2018 -> 2022 e tripla
    pl = did_cidades(cid['2022'], cid['2018'], pidx, C)
    lado['placebo_2018_para_2022'] = dict(pl['res'], leitura_pelo_mesmo_criterio=ler_a(pl['res']['est'], pl['res']['ep']),
                                           cidades_pareadas_pelo_pais=[FUSOS[c][0] for c, x in zip(pl['cods'], pl['modo']) if x == 'país'])
    G = len(paises)
    def somas(dd):
        return np.bincount(dd['g'], weights=dd['w'] * dd['d'], minlength=G), np.bincount(dd['g'], weights=dd['w'], minlength=G)
    S1, W1 = somas(did); S2, W2 = somas(pl)
    n1, d1, n2, d2 = C @ S1, C @ W1, C @ S2, C @ W2
    ok = (d1 > 0) & (d2 > 0)
    bs = n1[ok] / d1[ok] - n2[ok] / d2[ok]
    lado['tripla_(2026-2022)-(2022-2018)'] = {'est': float(P['est'] - pl['res']['est']), 'ep': float(bs.std(ddof=1)),
                                              'ic95': [float(np.percentile(bs, 2.5)), float(np.percentile(bs, 97.5))]}
    lado['diferenca_simples_2022_menos_2018'] = boot_dif(cid['2022'], cid['2018'])
    a['ao_lado'] = lado
    a['espelho'] = {'criterio_com_sinal_trocado_dispara': bool(P['est'] >= LIMIAR and abs(P['est']) > 3 * P['ep']),
                    'desfecho_branco_nulo': lado['espelho_branco_nulo']}
    out['parte_a'] = a
    log(f"(a) DiD {P['est']:.3f} ep {P['ep']:.3f} -> {a['principal']['leitura']}")

    # ------------------------------------------------------------ (b) dose por fuso
    b = {}
    reg = {}
    for ano in anos:
        c = cid[ano]
        reg[ano] = dose(c['D'], c['f'], c['W'], c['pais'], C)
        reg[ano]['media_ponderada_de_f'] = float((c['W'] * c['f']).sum() / c['W'].sum())
        gr = {}
        for nome, s in (('f = 0', c['f'] == 0), ('0 < f < 1', (c['f'] > 0) & (c['f'] < 1)), ('f = 1', c['f'] >= 1)):
            if s.sum():
                r = media_pond(c['D'][s], c['W'][s], c['pais'][s], C)
                gr[nome] = {'D': r['est'], 'ep_por_pais': r['ep'], 'cidades': int(s.sum()), 'paises': r['grupos'], 'votos': r['peso'],
                            'f1_medio': float((c['W'][s] * c['f1'][s]).sum() / c['W'][s].sum())}
        reg[ano]['por_grupo_de_dose'] = gr
    b26, b22, b18 = reg['2026'], reg['2022'], reg['2018']
    b['principal'] = {'inclinacao_2026': b26['inclinacao'], 'ep_por_pais': b26['ep'], 'z': b26['z'], 'ic95': b26['ic95'],
                      'ep_cr1_por_pais': b26['ep_cr1_pais'], 'p_permutacao_entre_paises': b26['p_permutacao_entre_paises'],
                      'constante_2026': b26['constante'], 'cidades': b26['cidades'], 'paises': b26['paises'],
                      'inclinacao_2022': b22['inclinacao'], 'ep_2022': b22['ep'], 'inclinacao_2018': b18['inclinacao'], 'ep_2018': b18['ep'],
                      'leitura': ler_b(b26['inclinacao'], b26['ep'], b22['inclinacao']),
                      'leitura_com_ep_cr1': ler_b(b26['inclinacao'], b26['ep_cr1_pais'], b22['inclinacao'])}
    b['regressao_por_ano'] = reg
    lado = {}
    c26 = cid['2026']
    # dose sobre a DiD
    gd = did['g']
    lado['dose_sobre_a_DiD_2026_menos_2022'] = dose(did['d'], fd, did['w'], gd, C)
    fpl = {int(c): f for c, f in zip(cid['2022']['cod'], cid['2022']['f'])}
    lado['dose_sobre_a_DiD_2022_menos_2018_placebo'] = dose(pl['d'], np.array([fpl[c] for c in pl['cods']]), pl['w'], pl['g'], C)
    # controle de f1
    for ano in anos:
        c = cid[ano]
        bb, se = wls_cluster(c['D'], np.column_stack([c['f'], c['f1']]), c['W'], c['pais'])
        lado[f'com_controle_de_f1_{ano}'] = {'inclinacao_f': float(bb[1]), 'ep_cr1_pais': float(se[1]), 'coef_f1': float(bb[2]), 'ep_f1': float(se[2])}
        zprop = c['f'] * (100 - c['f1']) / 100
        lado[f'forma_proporcional_{ano}'] = dose(c['D'], zprop, c['W'], c['pais'], C, 'f x fatia do adversário no 1º turno')
        lado[f'sem_peso_{ano}'] = dose(c['D'], c['f'], np.ones(len(c['D'])), c['pais'], C)
        lado[f'espelho_g_depois_das_17h_{ano}'] = dose(c['D'], c['g'], c['W'], c['pais'], C, 'g')
        bb, se = wls_cluster(c['D'], np.column_stack([c['f'], c['g']]), c['W'], c['pais'])
        lado[f'f_e_g_juntos_{ano}'] = {'inclinacao_f': float(bb[1]), 'ep_cr1_f': float(se[1]), 'inclinacao_g': float(bb[2]), 'ep_cr1_g': float(se[2])}
        lado[f'espelho_branco_nulo_{ano}'] = dose(c['difbn'], c['f'], c['W'], c['pais'], C)
        sj = np.array([FUSOS[int(x)][1] != 'Japão' for x in c['cod']])
        lado[f'sem_o_Japao_{ano}'] = dose(c['D'][sj], c['f'][sj], c['W'][sj], c['pais'][sj], C)
        for K, campo in ((10, 'difK10'), (50, 'difK50')):
            lado[f'{K}_pares_{ano}'] = dose(c[campo], c['f'], c['W'], c['pais'], C)
    loo = {}
    for p in sorted(set(c26['pais'].tolist())):
        s = c26['pais'] != p
        bb, _ = wls_cluster(c26['D'][s], c26['f'][s][:, None], c26['W'][s], c26['pais'][s])
        loo[paises[p]] = float(bb[1])
    pmin = min(loo, key=loo.get); pmax = max(loo, key=loo.get)
    lado['tirando_um_pais_2026'] = {'minimo': loo[pmin], 'sem_o_pais_min': pmin, 'maximo': loo[pmax], 'sem_o_pais_max': pmax}
    b['ao_lado'] = lado
    b['espelho'] = {'criterio_com_sinal_trocado_dispara': bool(b26['inclinacao'] >= LIMIAR and abs(b26['inclinacao']) > 3 * b26['ep']),
                    'dose_g_2026': lado['espelho_g_depois_das_17h_2026'], 'desfecho_branco_nulo_2026': lado['espelho_branco_nulo_2026']}
    out['parte_b'] = b
    log(f"(b) inclinação 2026 {b26['inclinacao']:.3f} ep {b26['ep']:.3f}; 2022 {b22['inclinacao']:.3f}; 2018 {b18['inclinacao']:.3f} -> {b['principal']['leitura']}")
    va, vb = a['principal']['leitura'], b['principal']['leitura']
    out['veredito_exterior_conjunto'] = 'SINAL' if 'SINAL' in (va, vb) and (va == 'SINAL' or vb == 'SINAL') else \
        ('SEM SINAL' if va == 'SEM SINAL' and vb == 'SEM SINAL' else 'INCONCLUSIVO')
    salvar_json(out, os.path.join(W, 'parcial_ab.json'))

    # ------------------------------------------------------------ calibração (a) e (b)
    E, Bz = dados['2026']['E'], dados['2026']['B']
    idx = dados['2026']['idx']; gi = cid['2026']['gi']; Wc = cid['2026']['W']
    fsec = cid['2026']['f'][gi]
    cal = {'a': {}, 'b': {}}
    cenarios = [('uniforme_1,785', 'uniforme', REGUA / 100, REGUA), ('uniforme_1,0', 'uniforme', LIMIAR / 100, LIMIAR),
                ('proporcional_3,57%_de_R', 'proporcional', 0.0357, None)]
    D22ref = {c: r for c, r in zip(did['cods'], [cid['2026']['D'][list(cid['2026']['cod']).index(c)] - d_ for c, d_ in zip(did['cods'], did['d'])])}
    pos26 = {int(c): j for j, c in enumerate(cid['2026']['cod'])}
    for i, (nome, forma, frac, delta) in enumerate(cenarios):
        rng = np.random.default_rng(SEMENTE + 100 + i)
        xB = plantar(Bz['L2'], Bz['R2'], frac, rng, forma)
        yB = 100 * (Bz['L2'] + xB) / Bz['w'] - Bz['f1']
        mB = contraf(yB, Bz['w'], idx)
        esperado_secao = contraf(100 * xB / Bz['w'], Bz['w'], idx)       # quanto o plantio subiu os pares de cada seção
        esp_a = -float((E['w'] * esperado_secao).sum() / E['w'].sum())
        # (a): exterior intacto
        difA = E['y'] - mB
        DcA = np.bincount(gi, weights=E['w'] * difA) / Wc
        dA = np.array([DcA[pos26[c]] - D22ref[c] for c in did['cods']])
        rA = media_pond(dA, did['w'], did['g'], C)
        dl = delta if delta is not None else -esp_a
        cal['a'][nome] = dict(poder(P['est'], rA['est'], rA['ep'], dl, 3, ler_a(rA['est'], rA['ep']) == 'SINAL'),
                              ep_com_plantio=rA['ep'], votos_plantados_no_brasil=float(xB.sum()), deslocamento_esperado=esp_a if delta is None else -delta)
        # (b): exterior atingido na fração (1 - f)
        xE = plantar(E['L2'], E['R2'], frac * (1 - fsec), rng, forma)
        yE = 100 * (E['L2'] + xE) / E['w'] - E['f1']
        difB = yE - mB
        DcB = np.bincount(gi, weights=E['w'] * difB) / Wc
        rB = dose(DcB, cid['2026']['f'], Wc, cid['2026']['pais'], C)
        # deslocamento esperado da inclinação: regressão do efeito esperado por cidade
        efeito = np.bincount(gi, weights=E['w'] * (100 * xE / E['w'] - esperado_secao)) / Wc
        besp, _ = wls_cluster(efeito, cid['2026']['f'][:, None], Wc, cid['2026']['pais'])
        dlb = delta if delta is not None else -float(besp[1])
        cal['b'][nome] = dict(poder(b26['inclinacao'], rB['inclinacao'], rB['ep'], dlb, 3,
                                    ler_b(rB['inclinacao'], rB['ep'], b22['inclinacao']) == 'SINAL'),
                              ep_com_plantio=rB['ep'], inclinacao_do_efeito_plantado=float(besp[1]),
                              condicoes_de_2026_disparam_com_plantio=bool(rB['inclinacao'] <= -LIMIAR and abs(rB['inclinacao']) > 3 * rB['ep']))
    cal['a']['menor_efeito_que_o_criterio_enxerga_em_base_sem_desvio'] = max(LIMIAR, 3 * P['ep'])
    cal['b']['menor_efeito_que_o_criterio_enxerga_em_base_sem_desvio'] = max(LIMIAR, 3 * b26['ep'])
    out['calibracao_ab'] = cal
    for parte, chave in (('parte_a', 'a'), ('parte_b', 'b')):
        pm = cal[chave]['uniforme_1,785']['poder_de_medida']
        out[parte]['principal']['poder_de_medida_com_1,785'] = pm
        out[parte]['principal']['poder_pleno_com_1,785'] = cal[chave]['uniforme_1,785']['poder_pleno']
        out[parte]['leitura_pela_letra'] = out[parte]['principal']['leitura']
        out[parte]['veredito'] = out[parte]['principal']['leitura'] if pm else 'SEM PODER'
    # tabela de cidades
    tab = []
    p22 = {int(c): j for j, c in enumerate(cid['2022']['cod'])}; p18 = {int(c): j for j, c in enumerate(cid['2018']['cod'])}
    dd = {c: d_ for c, d_ in zip(did['cods'], did['d'])}
    for j, c in enumerate(cid['2026']['cod']):
        c = int(c)
        tab.append({'codigo': c, 'cidade': FUSOS[c][0], 'pais': FUSOS[c][1], 'zona_iana': FUSOS[c][2], 'utc_2026': float(cid['2026']['o'][j]),
                    'f': float(cid['2026']['f'][j]), 'g': float(cid['2026']['g'][j]), 'secoes': int(cid['2026']['n'][j]),
                    'votos_finalistas': float(Wc[j]), 'f1': float(cid['2026']['f1'][j]), 'virada': float(cid['2026']['y'][j]),
                    'D_2026': float(cid['2026']['D'][j]),
                    'D_2022': float(cid['2022']['D'][p22[c]]) if c in p22 else None, 'votos_2022': float(cid['2022']['W'][p22[c]]) if c in p22 else None,
                    'D_2018': float(cid['2018']['D'][p18[c]]) if c in p18 else None, 'DiD': float(dd[c]) if c in dd else None})
    tab.sort(key=lambda x: -x['votos_finalistas'])
    out['cidades_2026'] = tab
    out['fusos'] = {'fonte': f'banco de fusos IANA, {versao_tzdata()} (tzdata do sistema), lido com zoneinfo; zona atribuída pela sede da cidade '
                             '(nome no bweb e endereço no cadastro de locais do TSE)',
                    'brasilia': {a: deslocamento('America/Sao_Paulo', DATAS[a]) for a in anos},
                    'tabela': [{'codigo': c, 'cidade': v[0], 'pais': v[1], 'zona_iana': v[2],
                                **{f'utc_{a}': fracoes(c, a)[0] for a in anos}, **{f'f_{a}': fracoes(c, a)[1] for a in anos}}
                               for c, v in sorted(FUSOS.items(), key=lambda t: t[1][0])]}
    salvar_json(out, os.path.join(W, 'parcial_ab.json'))
    CTX.update({'cid': cid, 'did': did, 'pl': pl, 'C': C, 'pidx': dict(pidx)})
    return T26, mu26, sd26


# ------------------------------------------------------------------------------------------------ parte (c)
def parte_c(out, T, mu, sd):
    est = json.load(gzip.open(ESTRUTURA_2T, 'rt'))
    perf = json.load(gzip.open(os.path.join(W, 'perfil_secao.json.gz'), 'rt'))['secoes']
    tipo = json.load(gzip.open(os.path.join(W, 'locais_tipo.json.gz'), 'rt'))
    sb = json.load(open(os.path.join(W, 'bu_sbm_final.json')))
    sbm, info_bu = sb['secoes'], sb['info']
    lista = {}
    lp = os.path.join(W, 'lista_bu.txt')
    if os.path.exists(lp):
        lista = dict(l.rstrip('\n').split('\t') for l in open(lp) if l.strip())
    c = {'boletins_lidos_por_pasta': info_bu}
    # consistência do boletim com o bweb
    ok_bu = {}; ruins = 0
    for k, v in sbm.items():
        e = est.get(k)
        if e is None or not e[12].lstrip('-').isdigit() or sum(v[:3]) != int(e[14]) or v[2] != int(e[12]):
            ruins += 1; continue
        ok_bu[k] = v
    n_ext_bu = len(glob.glob(os.path.join(W, 'dl_bu', 'zz', '*', '*', '*', '*-bu.dat')))
    c['boletins'] = {'secoes_com_boletim': len(sbm), 'coerentes_com_o_bweb': len(ok_bu), 'excluidos_por_discordancia': ruins,
                     'do_exterior': {k: v[:3] for k, v in sbm.items() if k.startswith('ZZ|')},
                     'boletins_do_exterior_baixados': n_ext_bu,
                     'boletins_do_exterior_com_o_campo_de_habilitacoes': sum(1 for k in sbm if k.startswith('ZZ|'))}
    # estrutura do perfil
    n_br = n_zero = n_cert = 0; cand = 0
    for k, e in est.items():
        if k.startswith('ZZ|') or not e[12].lstrip('-').isdigit() or int(e[14]) <= 0:
            continue
        uf, mun, zona, sec = k.split('|')
        agr = [] if e[15] in ('', '#NULO#') else [int(x) for x in e[15].replace('/', ' ').split()]
        el = bio = 0
        for s in [int(sec)] + agr:
            p = perf.get(f'{uf}|{mun}|{zona}|{s}')
            if p:
                el += p[0]; bio += p[1]
        n_br += 1
        if el > 0 and bio == 0:
            n_zero += 1
        if el > 0 and bio > 0 and int(e[12]) >= bio:
            n_cert += 1
        if el > 0 and int(e[14]) - int(e[12]) - (el - bio) <= 5:
            cand += 1
    presos = {k for k, v in tipo.items() if v[0] == 'Preso provisório' and k in est}
    transito = {k for k, v in tipo.items() if v[0] == 'Voto em trânsito' and k in est}
    Zs = {k for k, v in ok_bu.items() if v[1] == 0 and not k.startswith('ZZ|')}
    Qs = {k for k, v in ok_bu.items() if v[1] > 0 and lista.get(k) == 'C'} | \
         {k for k, v in ok_bu.items() if v[1] > 0 and k not in lista and not k.startswith('ZZ|') and _bmin(k, est, perf) is not None and _bmin(k, est, perf) <= 5}
    cob = collections.Counter(); cobz = collections.Counter()
    for k, estrato in lista.items():
        cob[estrato + ' na lista'] += 1
        if k in ok_bu:
            cob[estrato + ' com boletim'] += 1
            if ok_bu[k][1] == 0:
                cobz[estrato + ' com B = 0'] += 1
    c['estrutura'] = {'secoes_do_brasil_no_bweb_2t_com_comparecimento': n_br, 'secoes_sem_nenhum_eleitor_com_biometria_no_perfil': n_zero,
                      'secoes_com_NH_maior_ou_igual_aos_eleitores_com_biometria': n_cert, 'secoes_com_Bmin_ate_5_pelo_perfil': cand,
                      'secoes_de_preso_provisorio_no_bweb_2t': len(presos), 'secoes_de_voto_em_transito_no_bweb_2t': len(transito),
                      'cobertura_da_lista_de_download': dict(cob), 'B_igual_a_zero_por_estrato_da_lista': dict(cobz),
                      'presos_com_boletim': sum(1 for k in presos if k in ok_bu), 'presos_com_B_zero': sum(1 for k in presos if k in Zs),
                      'presos_soma_S_B_M': [int(sum(ok_bu[k][j] for k in presos if k in ok_bu)) for j in range(3)],
                      'transito_com_boletim': sum(1 for k in transito if k in ok_bu), 'transito_com_B_zero': sum(1 for k in transito if k in Zs),
                      'transito_soma_S_B_M': [int(sum(ok_bu[k][j] for k in transito if k in ok_bu)) for j in range(3)],
                      'Z_total': len(Zs), 'Z_lista': sorted(Zs, key=chave_ord),
                      'Z_detalhe': {k: {'S': ok_bu[k][0], 'B': ok_bu[k][1], 'M': ok_bu[k][2], 'tipo_do_local': tipo.get(k, ['Convencional'])[0],
                                        'origem_do_boletim': ok_bu[k][3]} for k in sorted(Zs, key=chave_ord)},
                      'Q_total': len(Qs)}
    log('(c) estrutura', {k: v for k, v in c['estrutura'].items() if not isinstance(v, (list, dict))})
    # universo com votos
    br = T['uf'] != 'ZZ'
    S = sub(T, br)
    kk = S['k']
    inZ = np.array([k in Zs for k in kk]); inP = np.array([k in presos for k in kk]); inQ = np.array([k in Qs for k in kk])
    g_local = np.array([f"{u}|{m}|{z}|{l}" for u, m, z, l in zip(S['uf'], S['mun'], S['zona'], S['loc'])])
    g_zona = np.array([f"{u}|{z}" for u, z in zip(S['uf'], S['zona'])])
    g_mun = np.array([f"{u}|{m}" for u, m in zip(S['uf'], S['mun'])])
    cov = np.column_stack([S[v] for v in VARS])
    VB = float(out['brasil_2026']['votos_finalistas_brasil_2t'])

    def informam(t, g):
        n1 = collections.Counter(g[t]); n0 = collections.Counter(g[~t])
        return int(sum(v for gr, v in n1.items() if n0.get(gr, 0) > 0))

    def fe(t, g, y, com_cov=False):
        if informam(t, g) == 0:
            return None
        gs = set(g[t].tolist())
        m = np.array([x in gs for x in g])                       # só grupos com seção do grupo (os outros não informam d)
        X = t[m].astype(float)[:, None]
        nomes = ['d']
        if com_cov:
            m = np.ones(len(g), bool); X = np.column_stack([t.astype(float), cov]); nomes = ['d'] + VARS
        r = fe_ols(y[m], X, g[m], S['w'][m], nomes)
        return {'d': r['coef']['d'], 'ep': r['ep']['d'], 'z': r['coef']['d'] / r['ep']['d'] if r['ep']['d'] > 0 else None,
                'n_regressao': r['n'], 'grupos': r['grupos']}

    def perm_zona(t, y, n=2000):
        gs = sorted(set(g_zona[t].tolist()))
        m = np.array([x in set(gs) for x in g_zona])
        gg = np.unique(g_zona[m], return_inverse=True)[1]; tt = t[m].astype(float); yy = y[m]; ww = S['w'][m]
        def coef(tv):
            sw = np.bincount(gg, weights=ww)
            tb = np.bincount(gg, weights=ww * tv) / sw; yb = np.bincount(gg, weights=ww * yy) / sw
            td = tv - tb[gg]; yd = yy - yb[gg]
            den = (ww * td * td).sum()
            return (ww * td * yd).sum() / den if den > 0 else np.nan
        obs = coef(tt)
        rng = np.random.default_rng(SEMENTE + 9)
        ordem = np.argsort(gg, kind='stable'); lim = np.flatnonzero(np.diff(gg[ordem])) + 1
        blocos = np.split(ordem, lim)
        vals = np.empty(n)
        for r in range(n):
            tv = tt.copy()
            for bl in blocos:
                if tt[bl].sum() > 0:
                    tv[bl] = tt[bl][rng.permutation(len(bl))]
            vals[r] = coef(tv)
        vals = vals[np.isfinite(vals)]
        return {'d_observado': float(obs), 'p_bilateral': float((np.abs(vals) >= abs(obs)).mean()), 'dp_da_permutacao': float(vals.std(ddof=1))}

    def pareado(t, y):
        """Pareamento P2 aplicado ao grupo: 20 pares entre seções do Brasil fora de Z, P e Q com piso de 30."""
        candm = (~inZ) & (~inP) & (~inQ) & (S['w'] >= PISO)
        if t.sum() == 0:
            return None
        Zb = (cov[candm] - mu) / sd; Ze = (cov[t] - mu) / sd
        idx, dist = vizinhos(Zb, Ze, K_PRINC)
        m_ = contraf(y[candm], S['w'][candm], idx)
        dif = y[t] - m_
        mm = g_mun[t]; um, gi = np.unique(mm, return_inverse=True)
        Cm = sorteios(len(um), SEMENTE + 3)
        r = media_pond(dif, S['w'][t], gi, Cm) if len(um) > 1 else {'est': float((S['w'][t] * dif).sum() / S['w'][t].sum()), 'ep': None, 'grupos': 1}
        return {'D': r['est'], 'ep_por_municipio': r['ep'], 'municipios': r['grupos'], 'secoes': int(t.sum()),
                'distancia_mediana_ao_20o_par': float(np.median(dist[:, -1])),
                'virada_grupo': float((S['w'][t] * y[t]).sum() / S['w'][t].sum()), 'virada_pares': float((S['w'][t] * m_).sum() / S['w'][t].sum())}

    def bloco(t, y, rot):
        r = {'secoes_no_universo': int(t.sum()), 'votos_finalistas_2t': float(S['w'][t].sum()),
             'informam_local': informam(t, g_local), 'informam_zona': informam(t, g_zona)}
        if t.sum() == 0:
            return r
        r['bruto'] = {'virada_grupo': float((S['w'][t] * y[t]).sum() / S['w'][t].sum()),
                      'virada_brasil': float((S['w'][~t] * y[~t]).sum() / S['w'][~t].sum()),
                      'f1_grupo': float((S['w'][t] * S['f1'][t]).sum() / S['w'][t].sum()),
                      'f1_brasil': float((S['w'][~t] * S['f1'][~t]).sum() / S['w'][~t].sum()),
                      'fatia_lula_2t_grupo': float(100 * S['L2'][t].sum() / S['w'][t].sum())}
        r['local'] = fe(t, g_local, y); r['zona'] = fe(t, g_zona, y)
        poucas = t.sum() < 10                                    # com menos de 10 seções não há erro-padrão que valha
        r['zona_com_covariaveis'] = None if poucas else fe(t, g_zona, y, True)
        r['local_com_covariaveis'] = None if poucas or not r['informam_local'] else fe(t, g_local, y, True)
        r['pareado_como_o_exterior'] = pareado(t, y)
        if r['informam_zona'] and 10 <= t.sum() <= 2000:
            r['permutacao_na_zona'] = perm_zona(t, y)
        if poucas:
            r['aviso'] = 'menos de 10 seções: os números são só descrição, sem erro-padrão válido'
        log(f"(c) {rot}: n {r['secoes_no_universo']} local {r['local']} zona {r['zona']}")
        return r

    y = S['y']
    c['Z'] = bloco(inZ, y, 'Z')
    c['P_presos'] = bloco(inP, y, 'P')
    c['Q_espelho'] = bloco(inQ, y, 'Q')
    c['Z_nao_presos'] = bloco(inZ & ~inP, y, 'Z fora de presos')
    # leitura
    def leitura(r):
        if r.get('informam_local', 0) >= 100 and r.get('local'):
            return 'local', ler_c(r['local']['d'], r['local']['ep'], r['informam_local'])
        if r.get('informam_zona', 0) >= 100 and r.get('zona'):
            return 'zona', ler_c(r['zona']['d'], r['zona']['ep'], r['informam_zona'])
        return None, 'SEM PODER'
    c['Z']['estimador_do_veredito'], c['Z']['leitura'] = leitura(c['Z'])
    c['P_presos']['estimador_da_leitura'], c['P_presos']['leitura_pelo_mesmo_criterio'] = leitura(c['P_presos'])
    c['Q_espelho']['estimador_da_leitura'], c['Q_espelho']['leitura_pelo_mesmo_criterio'] = leitura(c['Q_espelho'])
    # calibração: plantio em todas as seções do Brasil fora do grupo
    cal = {}
    for nome_g, t in (('Z', inZ), ('P_presos', inP)):
        if t.sum() == 0:
            continue
        cal[nome_g] = {}
        for i, (nome, forma, frac, delta) in enumerate((('uniforme_1,785', 'uniforme', REGUA / 100, REGUA), ('uniforme_1,0', 'uniforme', LIMIAR / 100, LIMIAR))):
            rng = np.random.default_rng(SEMENTE + 200 + i)
            x = plantar(S['L2'], S['R2'], frac, rng, forma); x[t] = 0
            yp = 100 * (S['L2'] + x) / S['w'] - S['f1']
            cal[nome_g][nome] = {}
            for est_nome, g in (('local', g_local), ('zona', g_zona)):
                r0 = c[nome_g][est_nome]
                if not r0:
                    continue
                r1 = fe(t, g, yp)
                n_inf = c[nome_g]['informam_' + est_nome]
                cal[nome_g][nome][est_nome] = dict(poder(r0['d'], r1['d'], r1['ep'], delta, 4, ler_c(r1['d'], r1['ep'], n_inf) == 'SINAL'),
                                                   ep_com_plantio=r1['ep'], secoes_que_informam=n_inf)
    c['calibracao'] = cal
    est_v = c['Z'].get('estimador_do_veredito')
    if est_v and cal.get('Z', {}).get('uniforme_1,785', {}).get(est_v) and not cal['Z']['uniforme_1,785'][est_v]['poder_de_medida']:
        c['veredito'] = 'SEM PODER'
    else:
        c['veredito'] = c['Z']['leitura']
    c['votos_do_brasil_para_traducao'] = VB
    # ---- X8 (EXPLORATÓRIO, depois de ver o resultado do grupo Q): dose de habilitação sem biometria dentro do local
    # nb = (S + M)/comparecimento: exato onde há boletim; nas outras seções, (NH + c x S_hat)/comparecimento, com
    # S_hat = comparecimento x (eleitores sem biometria / eleitores) do perfil e c = soma de S / soma de S_hat nos boletins.
    comp_a = np.zeros(len(kk)); nh_a = np.zeros(len(kk)); shat = np.full(len(kk), np.nan); nbx = np.full(len(kk), np.nan)
    for i, k in enumerate(kk):
        e_ = est.get(k)
        if e_ is None or not e_[12].lstrip('-').isdigit() or int(e_[14]) <= 0:
            continue
        comp_a[i] = int(e_[14]); nh_a[i] = int(e_[12])
        uf, mun, zona, sec = k.split('|')
        agr = [] if e_[15] in ('', '#NULO#') else [int(x) for x in e_[15].replace('/', ' ').split()]
        el = bio = 0
        for s_ in [int(sec)] + agr:
            p_ = perf.get(f'{uf}|{mun}|{zona}|{s_}')
            if p_:
                el += p_[0]; bio += p_[1]
        if el > 0:
            shat[i] = comp_a[i] * (el - bio) / el
        v = ok_bu.get(k)
        if v:
            nbx[i] = (v[0] + v[2]) / comp_a[i]
    tem_bu = np.isfinite(nbx) & np.isfinite(shat)
    S_exato = np.array([ok_bu[k][0] if k in ok_bu else 0 for k in kk], float)
    amostra_m = np.array([k in ok_bu and ok_bu[k][3] == 'amostra2t/arq' for k in kk]) & np.isfinite(shat)
    cfat = float(S_exato[amostra_m].sum() / shat[amostra_m].sum())
    nb = np.where(np.isfinite(nbx), nbx, np.clip((nh_a + cfat * shat) / np.where(comp_a > 0, comp_a, 1), 0, 1))
    okx = np.isfinite(nb) & (comp_a > 0)
    x8 = {'aviso': 'exploratório, decidido depois de ver o resultado do grupo Q', 'fator_c_S_sobre_S_hat_na_amostra': cfat,
          'nb_medio_Q_exato': float((S['w'][inQ] * nb[inQ]).sum() / S['w'][inQ].sum()),
          'B_sobre_comparecimento_Q_exato': float(1 - (S['w'][inQ] * nb[inQ]).sum() / S['w'][inQ].sum()),
          'nb_medio_presos_exato': float((S['w'][inP] * nb[inP]).sum() / S['w'][inP].sum()),
          'nb_medio_brasil_aprox': float((S['w'][okx] * nb[okx]).sum() / S['w'][okx].sum())}
    locQ = set(g_local[inQ].tolist())
    mQ = np.array([g in locQ for g in g_local]) & okx
    viz = mQ & ~inQ
    x8['nb_medio_vizinhas_de_local_de_Q_aprox'] = float((S['w'][viz] * nb[viz]).sum() / S['w'][viz].sum()) if viz.sum() else None
    r = fe_ols(y[mQ], nb[mQ][:, None], g_local[mQ], S['w'][mQ], ['nb'])
    x8['dose_dentro_do_local_nos_locais_de_Q'] = {'inclinacao_por_unidade': r['coef']['nb'], 'ep': r['ep']['nb'], 'n': r['n'], 'locais': r['grupos']}
    r = fe_ols(y[mQ], np.column_stack([nb[mQ], cov[mQ]]), g_local[mQ], S['w'][mQ], ['nb'] + VARS)
    x8['dose_nos_locais_de_Q_com_covariaveis'] = {'inclinacao_por_unidade': r['coef']['nb'], 'ep': r['ep']['nb']}
    r = fe_ols(S['f1'][mQ], nb[mQ][:, None], g_local[mQ], S['w'][mQ], ['nb'])
    x8['placebo_nivel_f1_nos_locais_de_Q'] = {'inclinacao_por_unidade': r['coef']['nb'], 'ep': r['ep']['nb']}
    # só seções com boletim (nb exato dos dois lados), em locais com duas ou mais seções com boletim
    mb = np.isfinite(nbx) & okx
    try:
        r = fe_ols(y[mb], nb[mb][:, None], g_local[mb], S['w'][mb], ['nb'])
        x8['dose_dentro_do_local_so_com_boletim_nb_exato'] = {'inclinacao_por_unidade': r['coef']['nb'], 'ep': r['ep']['nb'], 'n': r['n'], 'locais': r['grupos']}
    except Exception as e_:
        x8['dose_dentro_do_local_so_com_boletim_nb_exato'] = {'erro': repr(e_)}
    r = fe_ols(y[okx], nb[okx][:, None], g_local[okx], S['w'][okx], ['nb'])
    x8['dose_dentro_do_local_no_pais'] = {'inclinacao_por_unidade': r['coef']['nb'], 'ep': r['ep']['nb'], 'n': r['n'], 'locais': r['grupos']}
    r = fe_ols(S['f1'][okx], nb[okx][:, None], g_local[okx], S['w'][okx], ['nb'])
    x8['placebo_nivel_f1_dentro_do_local_no_pais'] = {'inclinacao_por_unidade': r['coef']['nb'], 'ep': r['ep']['nb']}
    r = fe_ols(y[okx], np.column_stack([nb[okx], cov[okx]]), g_local[okx], S['w'][okx], ['nb'] + VARS)
    x8['dose_dentro_do_local_no_pais_com_covariaveis'] = {'inclinacao_por_unidade': r['coef']['nb'], 'ep': r['ep']['nb']}
    if x8['nb_medio_vizinhas_de_local_de_Q_aprox'] is not None and c['Q_espelho'].get('local'):
        dif_nb = x8['nb_medio_Q_exato'] - x8['nb_medio_vizinhas_de_local_de_Q_aprox']
        x8['d_previsto_para_Q_se_a_troca_poupasse_o_voto_sem_biometria'] = -REGUA * dif_nb
        x8['d_observado_Q_local'] = c['Q_espelho']['local']['d']; x8['ep_observado_Q_local'] = c['Q_espelho']['local']['ep']
    c['X8_exploratorio_dose_sem_biometria'] = x8
    CTX['Qs'] = set(Qs)
    out['parte_c'] = c
    salvar_json(out, os.path.join(W, 'parcial_abc.json'))


def _bmin(k, est, perf):
    e = est.get(k)
    if e is None or not e[12].lstrip('-').isdigit():
        return None
    uf, mun, zona, sec = k.split('|')
    agr = [] if e[15] in ('', '#NULO#') else [int(x) for x in e[15].replace('/', ' ').split()]
    el = bio = 0
    for s in [int(sec)] + agr:
        p = perf.get(f'{uf}|{mun}|{zona}|{s}')
        if p:
            el += p[0]; bio += p[1]
    if el == 0:
        return None
    return int(e[14]) - int(e[12]) - (el - bio)


# ------------------------------------------------------------------------------------------------ exploratório (pós-resultado)
FUSOS_2014 = {  # códigos que só existem na base de 2014; nomes do bweb do 2º turno de 2014 (adendo23/F21_2014/bweb_2t_ZZ)
    29726: ('GUATEMALA (código de 2014)', 'Guatemala', 'America/Guatemala'), 29866: ('KINGSTON (código de 2014)', 'Jamaica', 'America/Jamaica'),
    30139: ('MITSUKAIDO', 'Japão', 'Asia/Tokyo'), 30236: ('OIZUMI', 'Japão', 'Asia/Tokyo'), 30554: ('SUZUKA', 'Japão', 'Asia/Tokyo'),
    30589: ('TAKAOKA', 'Japão', 'Asia/Tokyo'), 30643: ('TOYOHASHI', 'Japão', 'Asia/Tokyo'), 30724: ('UEDA', 'Japão', 'Asia/Tokyo'),
    30880: ('DONGGUAN', 'China', 'Asia/Shanghai'), 30945: ('NOUAKCHOTT', 'Mauritânia', 'Africa/Nouakchott'),
    30384: ('PUERTO SUAREZ', 'Bolívia', 'America/La_Paz')}
BWEB_2014_ZZ = os.path.join(TRAB, 'adendo23', 'F21_2014', 'bweb_2t_ZZ', 'bweb_2t_ZZ_28102014133904.zip')


def exploratorio(out):
    """Tudo aqui foi decidido DEPOIS de ver a primeira rodada completa. Não muda veredito."""
    import unicodedata
    ex = {'aviso': 'exploratório: escolhido depois de ver os resultados das partes (a), (b) e (c); não muda nenhum veredito'}
    cid = CTX['cid']
    # E1: estabilidade dos códigos de município do exterior entre 2014 e 2026 (só nomes, sem votos)
    def norm(x):
        return ''.join(ch for ch in unicodedata.normalize('NFD', x) if unicodedata.category(ch) != 'Mn').upper()[:4]
    nomes14 = {}
    if os.path.exists(BWEB_2014_ZZ):
        z = zipfile.ZipFile(BWEB_2014_ZZ)
        with z.open([n for n in z.namelist() if n.lower().endswith('.txt')][0]) as fh:
            for linha in fh:
                q = [x.strip('"') for x in linha.decode('latin1').strip().split(';')]
                nomes14[int(q[12])] = q[13]
    comuns = [c for c in nomes14 if c in FUSOS]
    dif = [(c, nomes14[c], FUSOS[c][0]) for c in comuns if norm(nomes14[c]) != norm(FUSOS[c][0])]
    ex['E1_codigos_2014_x_2026'] = {'codigos_comuns': len(comuns), 'nomes_com_as_4_primeiras_letras_diferentes': dif}
    # E2: 2014 como quarto ano (Dilma x Aécio; 2º turno em 26/10/2014, Brasília em horário de verão, UTC-2)
    FUSOS.update(FUSOS_2014); DATAS['2014'] = (2014, 10, 26)
    paises = sorted({v[1] for v in FUSOS.values()}); pidx = {p_: j for j, p_ in enumerate(paises)}
    C = sorteios(len(paises), SEMENTE + 50)
    A = preparar_ano('2014')
    E, B = A['E'], A['B']
    falt = sorted({int(c) for c in E['mun']} - set(FUSOS))
    if falt:
        ex['E2_2014'] = {'erro': f'cidades de 2014 sem fuso: {falt}'}
    else:
        idx = A['idx50'][:, :K_PRINC]
        d14 = E['y'] - contraf(B['y'], B['w'], idx)
        c14 = por_cidade(E, d14)
        c14['pais'] = np.array([pidx[FUSOS[int(x)][1]] for x in c14['cod']])
        fr = [fracoes(int(x), '2014') for x in c14['cod']]
        c14['f'] = np.array([t[1] for t in fr]); c14['g'] = np.array([t[2] for t in fr])
        gsec = np.array([pidx[FUSOS[int(x)][1]] for x in E['mun']])
        niv = media_pond(d14, E['w'], gsec, C)
        ds = dose(c14['D'], c14['f'], c14['W'], c14['pais'], C)
        gr = {}
        for nome, sel in (('f = 0', c14['f'] == 0), ('0 < f < 1', (c14['f'] > 0) & (c14['f'] < 1)), ('f = 1', c14['f'] >= 1)):
            if sel.sum():
                r = media_pond(c14['D'][sel], c14['W'][sel], c14['pais'][sel], C)
                gr[nome] = {'D': r['est'], 'ep_por_pais': r['ep'], 'cidades': int(sel.sum()), 'votos': r['peso']}
        # DiD 2014 -> 2018 pela regra A1/A2, com os índices de país deste bloco
        c18 = dict(cid['2018']); c18['pais'] = np.array([pidx[FUSOS[int(x)][1]] for x in c18['cod']])
        d1418 = did_cidades(c18, c14, pidx, C)
        ex['E2_2014'] = {'brasilia_utc': deslocamento('America/Sao_Paulo', DATAS['2014']), 'contagens': A['cont'],
                         'D_nivel': niv['est'], 'ep_por_pais': niv['ep'], 'cidades': int(len(c14['cod'])), 'votos': float(E['w'].sum()),
                         'virada_exterior': float((E['w'] * E['y']).sum() / E['w'].sum()),
                         'dose': {k: ds[k] for k in ('inclinacao', 'ep', 'ep_cr1_pais', 'constante', 'p_permutacao_entre_paises', 'cidades', 'paises')},
                         'por_grupo_de_dose': gr,
                         'DiD_2014_para_2018': {k: d1418['res'][k] for k in ('est', 'ep', 'ic95', 'n', 'grupos')}}
    del A; gc.collect()
    # E3: D por país e ano, 12 países com mais votos em 2026
    P26 = collections.Counter()
    for c_, w_ in zip(cid['2026']['cod'], cid['2026']['W']):
        P26[FUSOS[int(c_)][1]] += w_
    tab = {}
    series = dict(cid)
    if 'E2_2014' in ex and 'erro' not in ex['E2_2014']:
        series['2014'] = c14
    for pais, _ in P26.most_common(12):
        tab[pais] = {}
        for ano, c in sorted(series.items()):
            sel = np.array([FUSOS[int(x)][1] == pais for x in c['cod']])
            if sel.sum():
                tab[pais][ano] = {'D': float((c['W'][sel] * c['D'][sel]).sum() / c['W'][sel].sum()), 'votos': float(c['W'][sel].sum()),
                                  'f1': float((c['W'][sel] * c['f1'][sel]).sum() / c['W'][sel].sum())}
    ex['E3_D_por_pais_e_ano'] = tab
    # E4: sem peso e por tamanho de cidade, por ano
    e4 = {}
    for ano, c in sorted(series.items()):
        r = {'media_sem_peso': float(c['D'].mean()), 'mediana': float(np.median(c['D']))}
        for nome, sel in (('menos de 500 votos', c['W'] < 500), ('500 a 4.999', (c['W'] >= 500) & (c['W'] < 5000)), ('5.000 ou mais', c['W'] >= 5000)):
            if sel.sum():
                r[nome] = {'D': float((c['W'][sel] * c['D'][sel]).sum() / c['W'][sel].sum()), 'cidades': int(sel.sum()), 'votos': float(c['W'][sel].sum()),
                           'f1': float((c['W'][sel] * c['f1'][sel]).sum() / c['W'][sel].sum())}
        e4[ano] = r
    ex['E4_sem_peso_e_por_tamanho'] = e4
    # E5: DiD por tamanho da cidade (peso do ano de cima), com bootstrap de países, e o mesmo no placebo
    e5 = {}
    for rot, dd in (('2022_para_2026', CTX['did']), ('2018_para_2022_placebo', CTX['pl'])):
        r5 = {'sem_peso': {k: v for k, v in media_pond(dd['d'], np.ones(len(dd['d'])), dd['g'], CTX['C']).items() if k in ('est', 'ep', 'n')}}
        for nome, sel in (('menos de 500 votos', dd['w'] < 500), ('500 a 4.999', (dd['w'] >= 500) & (dd['w'] < 5000)), ('5.000 ou mais', dd['w'] >= 5000)):
            if sel.sum():
                r = media_pond(dd['d'][sel], dd['w'][sel], dd['g'][sel], CTX['C'])
                r5[nome] = {'est': r['est'], 'ep': r['ep'], 'n': r['n'], 'votos': r['peso']}
        e5[rot] = r5
    ex['E5_DiD_por_tamanho'] = e5
    # E7: dose pela força do adversário (o que uma troca proporcional aos votos do adversário prevê sob a H1)
    e7 = {}
    for ano in ('2018', '2022', '2026'):
        c = cid[ano]
        e7[ano] = {k: v for k, v in dose(c['D'], (100 - c['f1']) / 100, c['W'], c['pais'], CTX['C'], 'fatia do adversário no 1º turno').items()
                   if k in ('inclinacao', 'ep', 'ep_cr1_pais', 'constante', 'p_permutacao_entre_paises')}
    dd = CTX['did']
    f1d = {int(c_): v for c_, v in zip(cid['2026']['cod'], cid['2026']['f1'])}
    e7['DiD_2022_para_2026'] = {k: v for k, v in dose(dd['d'], np.array([(100 - f1d[c_]) / 100 for c_ in dd['cods']]), dd['w'], dd['g'], CTX['C']).items()
                                if k in ('inclinacao', 'ep', 'ep_cr1_pais', 'constante')}
    n7s = sum(1 for d_ in dd['d'] if d_ < 0)
    e7['cidades_com_DiD_negativa'] = {'negativas': int(n7s), 'total': int(len(dd['d'])), 'peso_negativo': float(dd['w'][dd['d'] < 0].sum() / dd['w'].sum())}
    pl_ = CTX['pl']
    e7['cidades_com_DiD_negativa_placebo_2018_2022'] = {'negativas': int((pl_['d'] < 0).sum()), 'total': int(len(pl_['d'])), 'peso_negativo': float(pl_['w'][pl_['d'] < 0].sum() / pl_['w'].sum())}
    ex['E7_dose_pela_forca_do_adversario'] = e7
    # E9: o grupo Q (pouca biometria em 2026, B > 0) em 2022 e 2018, contra as vizinhas de local daquele ano
    e9 = {}
    for ano in ('2022', '2018'):
        dd_ = carregar(os.path.join(DADOS, f'secoes{ano}.json.gz'))
        Ty = montar(dd_); del dd_; gc.collect()
        m_ = Ty['uf'] != 'ZZ'
        Sy = sub(Ty, m_); del Ty
        tq = np.array([k in CTX.get('Qs', ()) for k in Sy['k']])
        gl = np.array([f"{u}|{m2}|{z}|{l}" for u, m2, z, l in zip(Sy['uf'], Sy['mun'], Sy['zona'], Sy['loc'])])
        gs = set(gl[tq].tolist()); mm = np.array([x in gs for x in gl])
        r9 = {'secoes_de_Q_presentes': int(tq.sum())}
        if tq.sum() >= 10:
            r = fe_ols(Sy['y'][mm], tq[mm].astype(float)[:, None], gl[mm], Sy['w'][mm], ['d'])
            r9.update({'d_local': r['coef']['d'], 'ep': r['ep']['d'], 'n': r['n'], 'locais': r['grupos']})
            r = fe_ols(Sy['y'][mm], np.column_stack([tq[mm].astype(float)] + [Sy[v][mm] for v in VARS]), gl[mm], Sy['w'][mm], ['d'] + VARS)
            r9.update({'d_local_com_covariaveis': r['coef']['d'], 'ep_com_covariaveis': r['ep']['d']})
        e9[ano] = r9
        del Sy; gc.collect()
    ex['E9_grupo_Q_em_outros_anos'] = e9
    # E6: 2026 com pareamento mais fino, pela composição dos "outros" do 1º turno (Cury 70, Renan 14, Caiado 55, resto)
    A = preparar_ano('2026')
    E, B = A['E'], A['B']
    cand = carregar(os.path.join(DADOS, 'candidatos2026_1t.json.gz'))['secoes']
    def fatias(T_):
        M = np.zeros((len(T_['k']), 4))
        for i, k in enumerate(T_['k']):
            v = cand.get(k, {})
            tot = sum(v.values())
            if tot > 0:
                a70, a14, a55 = v.get('70', 0), v.get('14', 0), v.get('55', 0)
                M[i] = (100 * a70 / tot, 100 * a14 / tot, 100 * a55 / tot, 100 * (tot - v.get('13', 0) - v.get('22', 0) - a70 - a14 - a55) / tot)
        return M
    XB = np.column_stack([B['f1'], fatias(B), B['bn'], B['dc']]); XE = np.column_stack([E['f1'], fatias(E), E['bn'], E['dc']])
    del cand; gc.collect()
    mu7, sd7 = XB.mean(0), XB.std(0, ddof=1)
    cache = os.path.join(W, 'pares_2026_fino.npz')
    if os.path.exists(cache) and np.load(cache)['idx'].shape[0] == len(E['w']):
        idx7 = np.load(cache)['idx']; dist7 = np.load(cache)['dist']
    else:
        idx7, dist7 = vizinhos((XB - mu7) / sd7, (XE - mu7) / sd7, K_PRINC)
        np.savez_compressed(cache, idx=idx7, dist=dist7)
    dif7 = E['y'] - contraf(B['y'], B['w'], idx7)
    dif4 = E['y'] - contraf(B['y'], B['w'], A['idx50'][:, :K_PRINC])
    gsec = np.array([CTX['pidx'][FUSOS[int(x)][1]] for x in E['mun']])
    c7 = por_cidade(E, dif7); c7['pais'] = np.array([CTX['pidx'][FUSOS[int(x)][1]] for x in c7['cod']])
    c7['f'] = np.array([fracoes(int(x), '2026')[1] for x in c7['cod']])
    n7 = media_pond(dif7, E['w'], gsec, CTX['C'])
    ds7 = dose(c7['D'], c7['f'], c7['W'], c7['pais'], CTX['C'])
    nomes7 = ['f1', 'Cury', 'Renan', 'Caiado', 'resto dos outros', 'bn', 'dc']
    eq7 = {}
    for j, nome in enumerate(nomes7):
        me = float((E['w'] * XE[:, j]).sum() / E['w'].sum())
        mp4 = float((E['w'] * contraf(XB[:, j], B['w'], A['idx50'][:, :K_PRINC])).sum() / E['w'].sum())
        mp7 = float((E['w'] * contraf(XB[:, j], B['w'], idx7)).sum() / E['w'].sum())
        eq7[nome] = {'exterior': me, 'pares_do_pareamento_registrado': mp4, 'pares_do_pareamento_fino': mp7, 'media_brasil': float(mu7[j])}
    e6 = {'variaveis': nomes7, 'D_2026_pareamento_registrado': float((E['w'] * dif4).sum() / E['w'].sum()),
          'D_2026_pareamento_fino': n7['est'], 'ep_por_pais': n7['ep'], 'ic95': n7['ic95'],
          'media_sem_peso_das_cidades': float(c7['D'].mean()), 'dose': {k: ds7[k] for k in ('inclinacao', 'ep', 'ep_cr1_pais', 'constante')},
          'distancia_mediana_ao_20o_par': float(np.median(dist7[:, -1])), 'equilibrio': eq7, 'por_grupo_de_dose': {}, 'por_tamanho': {}, 'por_pais': {}}
    for nome, sel in (('f = 0', c7['f'] == 0), ('0 < f < 1', (c7['f'] > 0) & (c7['f'] < 1)), ('f = 1', c7['f'] >= 1)):
        r = media_pond(c7['D'][sel], c7['W'][sel], c7['pais'][sel], CTX['C']); e6['por_grupo_de_dose'][nome] = {'D': r['est'], 'ep': r['ep'], 'cidades': int(sel.sum())}
    for nome, sel in (('menos de 500 votos', c7['W'] < 500), ('500 a 4.999', (c7['W'] >= 500) & (c7['W'] < 5000)), ('5.000 ou mais', c7['W'] >= 5000)):
        r = media_pond(c7['D'][sel], c7['W'][sel], c7['pais'][sel], CTX['C']); e6['por_tamanho'][nome] = {'D': r['est'], 'ep': r['ep'], 'cidades': int(sel.sum())}
    for pais in ('Japão', 'Estados Unidos', 'Portugal', 'Reino Unido'):
        sel = np.array([FUSOS[int(x)][1] == pais for x in c7['cod']])
        e6['por_pais'][pais] = float((c7['W'][sel] * c7['D'][sel]).sum() / c7['W'][sel].sum())
    ex['E6_pareamento_fino_2026'] = e6
    del A; gc.collect()
    # texto
    T = []
    e1 = ex['E1_codigos_2014_x_2026']
    T.append(f"E1. Códigos de município do exterior: {e1['codigos_comuns']} códigos comuns ao bweb de 2014 e à tabela de 2026; nomes diferentes nas 4 primeiras letras: "
             + ('; '.join(f'{c} {a} / {b}' for c, a, b in e1['nomes_com_as_4_primeiras_letras_diferentes']) or 'nenhum') + '.')
    e2 = ex.get('E2_2014', {})
    if 'D_nivel' in e2:
        T.append(f"E2. 2014 (Dilma x Aécio; Brasília em UTC{fz(e2['brasilia_utc'], 0)}): D = {fz(e2['D_nivel'])} (ep por país {fz(e2['ep_por_pais'])}; {e2['cidades']} cidades, {fi(e2['votos'])} votos);"
                 f" inclinação da dose {fz(e2['dose']['inclinacao'])} (ep {fz(e2['dose']['ep'])}); por grupo: " +
                 '; '.join(f"{n}: {fz(g['D'])} (ep {fz(g['ep_por_pais'])}), {g['cidades']} cidades" for n, g in e2['por_grupo_de_dose'].items()) +
                 f"; DiD 2014 para 2018: {fz(e2['DiD_2014_para_2018']['est'])} (ep {fz(e2['DiD_2014_para_2018']['ep'])}).")
    T.append('E3. D por país e ano (votos de 2026 em ordem; D de 2014, 2018, 2022, 2026): ' + '; '.join(
        f"{p_}: " + ' / '.join(fz(v[a]['D']) if a in v else 'n/d' for a in ('2014', '2018', '2022', '2026')) for p_, v in tab.items()))
    T.append('E4. D sem peso e por tamanho da cidade: ' + '; '.join(
        f"{ano}: média sem peso {fz(r['media_sem_peso'])}, mediana {fz(r['mediana'])}, " + ', '.join(f"{n} {fz(r[n]['D'])} ({r[n]['cidades']} cidades)" for n in ('menos de 500 votos', '500 a 4.999', '5.000 ou mais') if n in r)
        for ano, r in e4.items()))
    T.append('E5. DiD por tamanho da cidade (ep por país): ' + '; '.join(
        f"{rot.replace('_', ' ')}: sem peso {fz(r['sem_peso']['est'])} (ep {fz(r['sem_peso']['ep'])}), " +
        ', '.join(f"{n} {fz(r[n]['est'])} (ep {fz(r[n]['ep'])}; {r[n]['n']} cidades, {fi(r[n]['votos'])} votos)" for n in ('menos de 500 votos', '500 a 4.999', '5.000 ou mais') if n in r)
        for rot, r in e5.items()))
    T.append(f"E6. 2026 com pareamento mais fino (f1, Cury, Renan, Caiado, resto dos outros, bn, dc; 20 pares): D = {fz(e6['D_2026_pareamento_fino'])} (ep por país {fz(e6['ep_por_pais'])};"
             f" IC 95% {fz(e6['ic95'][0])} a {fz(e6['ic95'][1])}) contra {fz(e6['D_2026_pareamento_registrado'])} do pareamento registrado; média sem peso {fz(e6['media_sem_peso_das_cidades'])};"
             f" inclinação da dose {fz(e6['dose']['inclinacao'])} (ep {fz(e6['dose']['ep'])}); por grupo: " + '; '.join(f"{n} {fz(r['D'])} (ep {fz(r['ep'])})" for n, r in e6['por_grupo_de_dose'].items()) +
             '; por tamanho: ' + '; '.join(f"{n} {fz(r['D'])} (ep {fz(r['ep'])})" for n, r in e6['por_tamanho'].items()) +
             '; por país: ' + '; '.join(f"{n} {fz(v)}" for n, v in e6['por_pais'].items()) +
             '. Composição (exterior / pares registrados / pares finos / média do Brasil): ' +
             '; '.join(f"{n} {fz(v['exterior'], 1)} / {fz(v['pares_do_pareamento_registrado'], 1)} / {fz(v['pares_do_pareamento_fino'], 1)} / {fz(v['media_brasil'], 1)}" for n, v in e6['equilibrio'].items()) + '.')
    T.append('E7. D da cidade contra a fatia do adversário no 1º turno (fração; uma troca de 3,57% dos votos do adversário só no Brasil prevê inclinação de -3,57 e constante zero): ' +
             '; '.join(f"{a}: inclinação {fz(e7[a]['inclinacao'])} (ep {fz(e7[a]['ep'])}), constante {fz(e7[a]['constante'])}" for a in ('2018', '2022', '2026')) +
             f"; sobre a DiD de 2022 para 2026: {fz(e7['DiD_2022_para_2026']['inclinacao'])} (ep {fz(e7['DiD_2022_para_2026']['ep'])}), constante {fz(e7['DiD_2022_para_2026']['constante'])}."
             f" Cidades com DiD negativa: {e7['cidades_com_DiD_negativa']['negativas']} de {e7['cidades_com_DiD_negativa']['total']} ({fz(100 * e7['cidades_com_DiD_negativa']['peso_negativo'], 0)}% dos votos);"
             f" no placebo de 2018 para 2022: {e7['cidades_com_DiD_negativa_placebo_2018_2022']['negativas']} de {e7['cidades_com_DiD_negativa_placebo_2018_2022']['total']}"
             f" ({fz(100 * e7['cidades_com_DiD_negativa_placebo_2018_2022']['peso_negativo'], 0)}% dos votos).")
    T.append('E9. As seções do grupo Q (pouca biometria em 2026) contra as vizinhas de local em outros anos, virada do candidato do PT: ' + '; '.join(
        f"{a}: {r.get('secoes_de_Q_presentes')} seções presentes, d {fz(r.get('d_local'))} (ep {fz(r.get('ep'))}), com covariáveis {fz(r.get('d_local_com_covariaveis'))} (ep {fz(r.get('ep_com_covariaveis'))})" for a, r in e9.items()) +
             f". Em 2026: {fz(out['parte_c']['Q_espelho']['local']['d'])} (ep {fz(out['parte_c']['Q_espelho']['local']['ep'])}).")
    ex['texto'] = T
    out['exploratorio'] = ex


def leitura(out):
    """Interpretação, escrita DEPOIS dos números (não é critério). Montada dos próprios números do JSON."""
    A, Bp, Cc = out['parte_a'], out['parte_b'], out['parte_c']
    pa, pb = A['principal'], Bp['principal']; la, lb = A['ao_lado'], Bp['ao_lado']
    N = out['niveis_por_ano']; cal = out['calibracao_ab']; tr = out['traducao_em_votos']; ex = out.get('exploratorio', {})
    e2 = ex.get('E2_2014', {}); e3 = ex.get('E3_D_por_pais_e_ano', {}); e5 = ex.get('E5_DiD_por_tamanho', {})
    reg = Bp['regressao_por_ano']; e = Cc['estrutura']
    e6x = ex.get('E6_pareamento_fino_2026', {}); e7x = ex.get('E7_dose_pela_forca_do_adversario', {})
    jp = e3.get('Japão', {}); us = e3.get('Estados Unidos', {})
    def serie(v):
        return ' / '.join(fz(v[a]['D']) if a in v else 'n/d' for a in ('2014', '2018', '2022', '2026'))
    c26 = out['cidades_2026']
    fr_jp = sum(c['votos_finalistas'] for c in c26 if c['pais'] == 'Japão') / sum(c['votos_finalistas'] for c in c26 if c['f'] >= 1)
    favor = [
        f"A diferença em diferenças é negativa, como a tese prevê: {fz(pa['DiD'])} ponto, a {fz(abs(pa['z']), 1)} ep de zero (ep por país {fz(pa['ep_por_pais'])}), em {pa['cidades']} cidades de {pa['paises']} países."
        f" Não depende de um país (tirando um de cada vez fica entre {fz(la['tirando_um_pais']['minimo'])} e {fz(la['tirando_um_pais']['maximo'])}) nem do número de pares ({fz(la['10_pares']['est'])} com 10, {fz(la['50_pares']['est'])} com 50)."
        f" O valor bruto de 2026, sem comparar com outro ano, é {fz(N['2026']['D_nivel'])} (ep por país {fz(N['2026']['ep_por_pais'])})." +
        (f" A DiD é negativa em {e7x['cidades_com_DiD_negativa']['negativas']} de {e7x['cidades_com_DiD_negativa']['total']} cidades ({fz(100 * e7x['cidades_com_DiD_negativa']['peso_negativo'], 0)}% dos votos)." if e7x else '') +
        (f" Com pareamento mais fino pela composição dos eliminados (exploratório), o D de 2026 quase não muda: {fz(e6x['D_2026_pareamento_fino'])} (ep {fz(e6x['ep_por_pais'])})." if e6x else ''),
        f"Sem peso, cada cidade valendo o mesmo, a diferença em diferenças é {fz(la['media_sem_peso_das_cidades']['est'])} (ep {fz(la['media_sem_peso_das_cidades']['ep'])}) e a mediana das cidades é {fz(la['mediana_das_cidades'])}:"
        " passaria do limiar numérico de -1,0. O estimador registrado é o ponderado; o desvio maior está nos postos pequenos" +
        (f" (cidades com menos de 500 votos: {fz(e5['2022_para_2026']['menos de 500 votos']['est'])}, ep {fz(e5['2022_para_2026']['menos de 500 votos']['ep'])}, {fi(e5['2022_para_2026']['menos de 500 votos']['votos'])} votos; com 5.000 ou mais: {fz(e5['2022_para_2026']['5.000 ou mais']['est'])}, ep {fz(e5['2022_para_2026']['5.000 ou mais']['ep'])}); no placebo de 2018 para 2022 os postos pequenos dão {fz(e5['2018_para_2022_placebo']['menos de 500 votos']['est'])} (ep {fz(e5['2018_para_2022_placebo']['menos de 500 votos']['ep'])}). Recorte feito depois do resultado, sem explicação testada." if e5 else '.'),
        f"A dose por fuso tem o sinal previsto: inclinação de {fz(pb['inclinacao_2026'])} ponto por unidade de fração; o grupo que vota inteiro antes de o Brasil abrir (f = 1) tem D de {fz(reg['2026']['por_grupo_de_dose']['f = 1']['D'])}"
        f" (ep {fz(reg['2026']['por_grupo_de_dose']['f = 1']['ep_por_pais'])}) contra {fz(reg['2026']['por_grupo_de_dose']['f = 0']['D'])} nas Américas.",
        f"A condição 'nenhuma habilitação biométrica' não pôde ser testada dentro do Brasil: em {fi(Cc['boletins']['coerentes_com_o_bweb'])} boletins lidos há {e['Z_total']} seção(ões) com B = 0, nenhuma seção tem zero eleitor com biometria no perfil,"
        f" e as {e['secoes_de_preso_provisorio_no_bweb_2t']} seções de presos e internação habilitam por biometria ({fz(100 * e['presos_soma_S_B_M'][1] / max(1, sum(e['presos_soma_S_B_M'])), 1)}% do comparecimento)."
        " Isto não é evidência a favor; só tira o contrapeso: o que os relatórios antigos chamavam de contrapeso (as 97 seções) não mede a condição, e este teste mostra que ela quase não ocorre no Brasil.",
    ]
    contra = [
        f"Pela letra nenhum critério de sinal foi atingido. A diferença em diferenças fica acima de -1,0 e o intervalo de 95% ({fz(pa['ic95'][0])} a {fz(pa['ic95'][1])}) não chega a -1,785, o tamanho que viraria o resultado:"
        f" mesmo o extremo inferior, se valesse para o Brasil inteiro, seriam {fi(tr['DiD_ic95_inferior']['votos_trocados_se_valesse_para_o_brasil'])} votos trocados e {fi(tr['DiD_ic95_inferior']['efeito_na_margem'])} de margem, contra 4.430.191.",
        f"A mesma conta dá {fz(la['placebo_2018_para_2022']['est'])} (ep {fz(la['placebo_2018_para_2022']['ep'])}) de 2018 para 2022" +
        (f" e {fz(e2['DiD_2014_para_2018']['est'])} (ep {fz(e2['DiD_2014_para_2018']['ep'])}) de 2014 para 2018 (exploratório). O D de nível do mesmo pareamento foi {fz(e2['D_nivel'])} em 2014," if 'D_nivel' in e2 else '. O D de nível foi')
        + f" {fz(N['2018']['D_nivel'])} em 2018, {fz(N['2022']['D_nivel'])} em 2022 e {fz(N['2026']['D_nivel'])} em 2026: o desvio do exterior contra os pares muda de 1 a 6 pontos de uma eleição para outra; a mudança de 2022 para 2026 é do tamanho da de 2018 para 2022 ({fz(la['diferenca_simples_2022_menos_2018']['est'])} pela diferença simples dos agregados) e muito menor que a de 2014 para 2018."
        f" A diferença tripla é {fz(la['tripla_(2026-2022)-(2022-2018)']['est'])} (ep {fz(la['tripla_(2026-2022)-(2022-2018)']['ep'])}). Ressalva do Adendo 18: o Léo suspeita desses anos, então isto não é régua limpa; mas, pela lógica da própria H1, um D perto de zero em 2022 diria que 2022 foi limpa.",
        f"A dose por fuso não passa de 3 ep ({fz(abs(pb['z']), 1)} ep) e não está ausente nos placebos: {fz(pb['inclinacao_2022'])} em 2022 e {fz(pb['inclinacao_2018'])} em 2018" +
        (f", {fz(e2['dose']['inclinacao'])} em 2014" if 'dose' in e2 else '') +
        f". O Japão, que é {fz(100 * fr_jp, 0)}% dos votos do grupo f = 1, fica abaixo dos Estados Unidos nas quatro eleições (D do Japão em 2014, 2018, 2022, 2026: {serie(jp)}; dos EUA: {serie(us)})."
        f" Sem o Japão a inclinação de 2026 é {fz(lb['sem_o_Japao_2026']['inclinacao'])} (ep {fz(lb['sem_o_Japao_2026']['ep'])}); a dose sobre a diferença em diferenças é {fz(lb['dose_sobre_a_DiD_2026_menos_2022']['inclinacao'])} (ep {fz(lb['dose_sobre_a_DiD_2026_menos_2022']['ep'])}).",
        "Um gatilho por relógio absoluto prevê diferença em diferenças perto de zero nas Américas; ela é " +
        '; '.join(f"{fz(r['est'])} (ep {fz(r['ep'])}) em {n}" for n, r in la['DiD_por_grupo_de_dose'].items()) +
        ". O desvio não cresce da América para a Europa. Já a H1 (exterior inteiro limpo) prevê o maior desvio onde o adversário é forte; nos Estados Unidos, com Lula a " +
        (f"{fz(us['2026']['f1'], 0)}% no 1º turno, D é {fz(us['2026']['D'])}." if '2026' in us else 'menos de 40% no 1º turno, D é perto de zero.'),
        f"A calibração mostra que a parte (b) não tem poder: plantando 1,785 ponto com o desenho do relógio, a inclinação anda {fz(cal['b']['uniforme_1,785']['deslocamento'])}, só {fz(cal['b']['uniforme_1,785']['deslocamento_em_ep'], 1)} ep;"
        f" o critério só enxergaria {fz(cal['b']['menor_efeito_que_o_criterio_enxerga_em_base_sem_desvio'])} ponto ou mais. A parte (a) tem poder (o mesmo plantio anda {fz(cal['a']['uniforme_1,785']['deslocamento_em_ep'], 1)} ep e dispara o critério).",
    ]
    P_, Q_ = Cc['P_presos'], Cc['Q_espelho']
    x8 = Cc.get('X8_exploratorio_dose_sem_biometria', {}); e9 = ex.get('E9_grupo_Q_em_outros_anos', {})
    bo = Cc['boletins']
    if bo.get('boletins_do_exterior_baixados'):
        favor.append(f"O boletim do exterior não traz o campo de habilitações ({bo['boletins_do_exterior_com_o_campo_de_habilitacoes']} de {bo['boletins_do_exterior_baixados']} lidos): a urna de lá roda sem o módulo de biometria,"
                     " condição que não aparece em nenhum boletim do Brasil. A H1 fica sem teste direto no país; também não é evidência a favor.")
    if P_.get('zona'):
        favor.append(f"Pelo tipo e nome do local, como a tarefa pediu, as {P_['secoes_no_universo']} seções de presos e internação viraram {fz(P_['zona']['d'])} ponto contra as vizinhas de zona (ep {fz(P_['zona']['ep'])}): pelo número do critério seria sinal."
                     " Mas não é a condição da H1 (ver o lado contra).")
        contra.append(f"As seções de presos NÃO são seções sem biometria: os {e['presos_com_boletim']} boletins mostram {fi(e['presos_soma_S_B_M'][1])} habilitações por biometria em {fi(sum(e['presos_soma_S_B_M']))} ({fz(100 * e['presos_soma_S_B_M'][1] / max(1, sum(e['presos_soma_S_B_M'])), 1)}%) e nenhuma seção com B = 0."
                      f" Pela H1 elas deveriam virar como as vizinhas; a diferença bruta de {fz(P_['zona']['d'])} vem da composição (Lula a {fz(P_['bruto']['f1_grupo'], 1)}% no 1º turno, sem espaço para subir) e cai para {fz(P_['zona_com_covariaveis']['d'])} (ep {fz(P_['zona_com_covariaveis']['ep'])}) com as covariáveis do pareamento."
                      " Um d muito negativo num grupo com biometria mostra que d negativo, sozinho, não identifica a condição.")
    if x8.get('dose_dentro_do_local_nos_locais_de_Q'):
        dq = x8['dose_dentro_do_local_nos_locais_de_Q']
        favor.append(f"Exploratório (versão de dose da H1): nos {fi(dq['locais'])} locais que têm seção de pouca biometria, a virada cai com a fração de habilitação sem biometria, {fz(dq['inclinacao_por_unidade'])} por unidade (ep {fz(dq['ep'])});"
                     f" com covariáveis {fz(x8['dose_nos_locais_de_Q_com_covariaveis']['inclinacao_por_unidade'])} (ep {fz(x8['dose_nos_locais_de_Q_com_covariaveis']['ep'])}). A previsão da dose seria -1,785. Recorte feito depois do resultado.")
    if P_.get('pareado_como_o_exterior') and Q_.get('pareado_como_o_exterior'):
        contra.append(
            f"O mesmo pareamento, aplicado a seções do Brasil que TÊM biometria, também dá D negativo: {fz(P_['pareado_como_o_exterior']['D'])} (ep {fz(P_['pareado_como_o_exterior']['ep_por_municipio'])}) nas {P_['secoes_no_universo']} seções de presos"
            f" e {fz(Q_['pareado_como_o_exterior']['D'])} (ep {fz(Q_['pareado_como_o_exterior']['ep_por_municipio'])}) nas {Q_['secoes_no_universo']} seções de pouca biometria com B > 0, o mesmo tamanho do D do exterior ({fz(N['2026']['D_nivel'])})."
            " Um D desse tamanho aparece, portanto, em populações incomuns sem a condição da H1."
            f" Contra as vizinhas de local, o grupo de pouca biometria dá {fz(Q_['local']['d'])} (ep {fz(Q_['local']['ep'])})" +
            (f"; as mesmas seções deram {fz(e9['2022'].get('d_local'))} (ep {fz(e9['2022'].get('ep'))}) em 2022 e {fz(e9['2018'].get('d_local'))} (ep {fz(e9['2018'].get('ep'))}) em 2018 (exploratório)." if e9 else '.'))
    if x8.get('dose_dentro_do_local_no_pais'):
        contra.append(f"A versão de dose da H1 (a troca pouparia o voto habilitado sem biometria) prevê -1,785 por unidade; no país inteiro, dentro do local, a dose é {fz(x8['dose_dentro_do_local_no_pais']['inclinacao_por_unidade'])}"
                      f" (ep {fz(x8['dose_dentro_do_local_no_pais']['ep'])}) e {fz(x8['dose_dentro_do_local_no_pais_com_covariaveis']['inclinacao_por_unidade'])} (ep {fz(x8['dose_dentro_do_local_no_pais_com_covariaveis']['ep'])}) com covariáveis;"
                      f" só com boletins (fração exata dos dois lados) {fz(x8['dose_dentro_do_local_so_com_boletim_nb_exato'].get('inclinacao_por_unidade'))} (ep {fz(x8['dose_dentro_do_local_so_com_boletim_nb_exato'].get('ep'))})."
                      f" Nos locais de pouca biometria o placebo de nível não é zero ({fz(x8['placebo_nivel_f1_nos_locais_de_Q']['inclinacao_por_unidade'])}, ep {fz(x8['placebo_nivel_f1_nos_locais_de_Q']['ep'])}): as seções comparadas já eram diferentes no 1º turno."
                      f" O grupo de pouca biometria tem {fz(100 * x8['nb_medio_Q_exato'], 0)}% de habilitação sem biometria e ficou {fz(x8.get('d_observado_Q_local'))} abaixo das vizinhas, contra {fz(x8.get('d_previsto_para_Q_se_a_troca_poupasse_o_voto_sem_biometria'))} previstos pela dose. (Exploratório.)")
    x = tr['exterior_inteiro']
    contra.append(f"O exterior inteiro são {fi(x['votos_finalistas_2t'])} votos nos finalistas ({fz(100 * x['votos_finalistas_como_fracao_do_total'], 2)}% do total, {fz(100 * x['votos_finalistas_como_fracao_da_margem'], 1)}% da margem)."
                  f" Se todos fossem de Flávio a margem de Lula ainda seria {fi(x['margem_nacional_se_todo_voto_do_exterior_fosse_de_flavio'])}. O exterior não decide nada; só serve para saber se as seções do Brasil carregam um desvio que o exterior não tem.")
    out['leitura'] = (['A FAVOR DA TESE:'] + ['  ' + t for t in favor] + ['CONTRA A TESE:'] + ['  ' + t for t in contra] +
                      ['Testes com critério nesta rodada: 3 (a, b, c). Com limiares de 3 e 4 ep, o acaso daria menos de 0,01 sinal. Nenhum disparou.',
                       'Nos blocos exploratórios (X1 a X9, dezenas de recortes olhados depois do resultado) há números a mais de 3 ep (postos pequenos, dose nos locais de pouca biometria). '
                       'Com tantos recortes, parte disso é esperada por acaso; nenhum conta como sinal sem registro prévio e conferência independente.'])
    out['leitura_a_favor'] = favor; out['leitura_contra'] = contra


# ------------------------------------------------------------------------------------------------ principal
def main():
    os.makedirs(W, exist_ok=True)
    out = {'teste': 'R27 A5: exterior e relógio absoluto (fragilidade "F19 (exterior sem biometria) e o contrapeso do L7 e do F6")',
           'registro': 'PRE-REGISTRO-2026-10-26.md, Adendo 27 (commit 2748895, 10/11/2026 00:16:42 UTC); registro/adendo27/equipe_vermelha_relatorio.json',
           'aviso_do_registro': 'reteste escrito por quem já conhecia os resultados antigos; o critério é novo, a escolha do que retestar é posterior ao dado',
           'criterio': {'exterior_sinal': 'DiD <= -1,0 a mais de 3 ep (por país) OU inclinação <= -1,0 a mais de 3 ep com |inclinação de 2022| < 0,4',
                        'exterior_sem_sinal': '|DiD| < 0,4 com ep <= 0,2 E |inclinação| < 0,4',
                        'brasil_sem_biometria': 'sinal: d <= -1,0 a mais de 4 ep em pelo menos 100 seções; sem sinal: |d| < 0,4 e ep <= 0,2; menos de 100 seções: SEM PODER'},
           'semente': SEMENTE, 'replicas': NBOOT, 'regua': REGUA, 'limiar': LIMIAR, 'margem_oficial': MARGEM,
           'docstring_sha256_registrado_antes_de_rodar': 'cce8de2cc71be02da95057645db59c62b71047ba169149ceae1b874e039b19f3',
           'docstring_sha256_atual_com_o_bloco_exploratorio': hashlib.sha256(__doc__.encode()).hexdigest()}
    T26, mu26, sd26 = partes_ab(out)
    parte_c(out, T26, mu26, sd26)
    traducao(out)
    del T26; gc.collect()
    salvar_json(out, SAIDA_JSON)
    exploratorio(out)
    leitura(out)
    salvar_json(out, SAIDA_JSON)
    escrever_txt(out, SAIDA_TXT)
    log('gravado', SAIDA_JSON, SAIDA_TXT)


def traducao(out):
    VB = out['brasil_2026']['votos_finalistas_brasil_2t']
    def votos(x):
        return {'pontos': x, 'votos_trocados_se_valesse_para_o_brasil': -x / 100 * VB, 'efeito_na_margem': -2 * x / 100 * VB,
                'fracao_da_margem_oficial': -2 * x / 100 * VB / MARGEM, 'fracao_da_regua_1,785': -x / REGUA}
    t = {'DiD_parte_a': votos(out['parte_a']['principal']['DiD']),
         'DiD_ic95_inferior': votos(out['parte_a']['principal']['ic95'][0]), 'DiD_ic95_superior': votos(out['parte_a']['principal']['ic95'][1]),
         'D_nivel_2026': votos(out['niveis_por_ano']['2026']['D_nivel']),
         'inclinacao_parte_b': votos(out['parte_b']['principal']['inclinacao_2026'])}
    z = out['parte_c']['Z']
    ev = z.get('estimador_do_veredito')
    if ev and z.get(ev):
        t['d_parte_c_' + ev] = votos(z[ev]['d'])
    else:
        out['traducao_parte_c'] = ('sem tradução: Z tem %d seção(ões), abaixo das 100 que o critério exige; um número de votos tirado daí não teria '
                                   'erro-padrão' % z['secoes_no_universo'])
    tot = out['niveis_por_ano']['2026']['totais']
    t['exterior_inteiro'] = {'secoes_2t': tot['secoes_zz'], 'aptos_2t': tot['apt2_zz'], 'comparecimento_2t': tot['comp2_zz'],
                             'lula_2t': tot['L2_zz'], 'flavio_2t': tot['R2_zz'], 'votos_finalistas_2t': tot['L2_zz'] + tot['R2_zz'],
                             'margem_de_lula_no_exterior': tot['L2_zz'] - tot['R2_zz'],
                             'votos_finalistas_como_fracao_do_total': (tot['L2_zz'] + tot['R2_zz']) / (tot['L2'] + tot['R2']),
                             'votos_finalistas_como_fracao_da_margem': (tot['L2_zz'] + tot['R2_zz']) / MARGEM,
                             'margem_nacional_sem_o_exterior': (tot['L2'] - tot['R2']) - (tot['L2_zz'] - tot['R2_zz']),
                             'margem_nacional_se_todo_voto_do_exterior_fosse_de_flavio': (tot['L2'] - tot['R2']) - (tot['L2_zz'] - tot['R2_zz']) - (tot['L2_zz'] + tot['R2_zz'])}
    out['traducao_em_votos'] = t


# ------------------------------------------------------------------------------------------------ texto
def fz(x, c=2):
    if x is None or (isinstance(x, float) and x != x):
        return 'n/d'
    s = f'{x:,.{c}f}'
    return s.replace(',', 'X').replace('.', ',').replace('X', '.')


def fi(x):
    return f'{int(round(x)):,}'.replace(',', '.')


def escrever_txt(o, caminho):
    L = []; w = L.append
    A, Bp, Cc = o['parte_a'], o['parte_b'], o['parte_c']
    N = o['niveis_por_ano']; cal = o['calibracao_ab']; tr = o['traducao_em_votos']
    pa, pb = A['principal'], Bp['principal']
    w('R27 A5 (Adendo 27, Onda A): EXTERIOR E RELÓGIO ABSOLUTO')
    w(f"Registro: {o['registro']}. Script: scripts/analisar_R27_A5.py. Semente {o['semente']}, {fi(o['replicas'])} réplicas, bootstrap de países.")
    w(f"Aviso do registro: {o['aviso_do_registro']}.")
    w('')
    w('VEREDITOS PELA LETRA')
    w(f"  (a) diferença em diferenças 2022 para 2026: {A['veredito']} (pela letra: {A['leitura_pela_letra']}). DiD = {fz(pa['DiD'])} ponto (ep por país {fz(pa['ep_por_pais'])}; z {fz(pa['z'], 1)};"
      f" IC 95% {fz(pa['ic95'][0])} a {fz(pa['ic95'][1])}; {pa['cidades']} cidades, {pa['paises']} países). Depende da comparação com 2022.")
    w(f"  (b) dose por fuso: {Bp['veredito']} (pela letra: {Bp['leitura_pela_letra']}; a calibração decide). Inclinação de 2026 = {fz(pb['inclinacao_2026'])} ponto por unidade de fração (ep por país {fz(pb['ep_por_pais'])};"
      f" z {fz(pb['z'], 1)}; IC 95% {fz(pb['ic95'][0])} a {fz(pb['ic95'][1])}); 2022: {fz(pb['inclinacao_2022'])} (ep {fz(pb['ep_2022'])});"
      f" 2018: {fz(pb['inclinacao_2018'])} (ep {fz(pb['ep_2018'])}).")
    w(f"  Exterior, conjunto pela letra: {o['veredito_exterior_conjunto']}.")
    z = Cc['Z']
    w(f"  (c) seções do Brasil com zero habilitação biométrica: {Cc['veredito']}. Z tem {z['secoes_no_universo']} seção(ões)"
      f" ({z['informam_local']} com vizinha no local, {z['informam_zona']} com vizinha na zona); o critério exige 100.")
    w('')
    w('1. Níveis por ano (o pareamento do F19 refeito; valor bruto de 2026 ao lado dos outros anos)')
    for ano in ('2026', '2022', '2018'):
        r = N[ano]
        w(f"  {ano}: D = {fz(r['D_nivel'])} (ep por país {fz(r['ep_por_pais'])}; ep por cidade {fz(r['ep_por_cidade'])}; F19 publicado {fz(r['D_publicado_F19'])},"
          f" diferença {fz(r['diferenca_para_o_F19'], 4)}); virada do exterior {fz(r['virada_exterior'])}, dos pares {fz(r['virada_pares'])}, do Brasil {fz(r['virada_brasil_candidatas'])};"
          f" {fi(r['contagens']['exterior_com_piso_30'])} seções, {r['cidades_com_secao']} cidades, {r['paises_com_secao']} países, {fi(r['votos_finalistas_exterior_com_piso'])} votos nos finalistas.")
    w('')
    w('2. Parte (a): diferença em diferenças por cidade')
    w(f"  Principal: {fz(pa['DiD'])} (ep {fz(pa['ep_por_pais'])}; CR1 por país {fz(pa['ep_cr1_por_pais'])}); {pa['cidades_pareadas_pela_mesma_cidade']} cidades pela mesma cidade;"
      f" pelo país: {', '.join(pa['cidades_pareadas_pelo_pais']) or 'nenhuma'}; fora, sem referência: {', '.join(pa['cidades_fora_sem_referencia']) or 'nenhuma'} ({fi(pa['peso_fora'])} votos).")
    la = A['ao_lado']
    def lr(r):
        return f"{fz(r['est'])} (ep {fz(r['ep'])})"
    w(f"  Ao lado: só cidades nos dois anos {lr(la['so_cidades_nos_dois_anos'])}; por país {lr(la['por_pais'])}; diferença simples dos agregados {lr(la['diferenca_simples_dos_agregados'])};"
      f" média sem peso {lr(la['media_sem_peso_das_cidades'])}; mediana das cidades {fz(la['mediana_das_cidades'])}; 10 pares {lr(la['10_pares'])}; 50 pares {lr(la['50_pares'])};"
      f" sem a variação do comparecimento {lr(la['sem_variacao_do_comparecimento'])}.")
    t1 = la['tirando_um_pais']
    w(f"  Tirando um país de cada vez: de {fz(t1['minimo'])} (sem {t1['sem_o_pais_min']}) a {fz(t1['maximo'])} (sem {t1['sem_o_pais_max']}).")
    w('  DiD por grupo de dose: ' + '; '.join(f"{n}: {lr(r)}, {r['n']} cidades" for n, r in la['DiD_por_grupo_de_dose'].items()))
    pl = la['placebo_2018_para_2022']; tp = la['tripla_(2026-2022)-(2022-2018)']
    w(f"  Placebo 2018 para 2022 (mesma conta; Adendo 18: não é régua limpa): {lr(pl)}, leitura pelo mesmo critério {pl['leitura_pelo_mesmo_criterio']};"
      f" diferença tripla {lr(tp)}; diferença simples 2022 menos 2018 {lr(la['diferenca_simples_2022_menos_2018'])}.")
    w(f"  Espelho: critério com o sinal trocado dispara? {'sim' if A['espelho']['criterio_com_sinal_trocado_dispara'] else 'não'};"
      f" mesma conta com o desfecho branco e nulo: {lr(A['espelho']['desfecho_branco_nulo'])}.")
    w('')
    w('3. Parte (b): dose por fuso')
    for ano in ('2026', '2022', '2018'):
        r = Bp['regressao_por_ano'][ano]
        w(f"  {ano}: inclinação {fz(r['inclinacao'])} (ep bootstrap de países {fz(r['ep'])}; CR1 por país {fz(r['ep_cr1_pais'])}; p de permutação entre países {fz(r['p_permutacao_entre_paises'], 3)});"
          f" constante {fz(r['constante'])}; {r['cidades']} cidades, {r['paises']} países. Por grupo: " +
          '; '.join(f"{n}: D {fz(g['D'])} (ep {fz(g['ep_por_pais'])}), {g['cidades']} cidades, {fi(g['votos'])} votos, Lula no 1º turno {fz(g['f1_medio'], 1)}" for n, g in r['por_grupo_de_dose'].items()))
    lb = Bp['ao_lado']
    def li(r):
        return f"{fz(r['inclinacao'])} (ep {fz(r['ep'])})"
    w(f"  Dose sobre a DiD (2026 menos 2022): {li(lb['dose_sobre_a_DiD_2026_menos_2022'])}; placebo sobre a DiD de 2022 menos 2018: {li(lb['dose_sobre_a_DiD_2022_menos_2018_placebo'])}.")
    for ano in ('2026', '2022', '2018'):
        cf = lb[f'com_controle_de_f1_{ano}']; fg = lb[f'f_e_g_juntos_{ano}']
        w(f"  {ano}, ao lado: com controle de f1 {fz(cf['inclinacao_f'])} (ep CR1 {fz(cf['ep_cr1_pais'])}); forma proporcional {li(lb[f'forma_proporcional_{ano}'])};"
          f" sem peso {li(lb[f'sem_peso_{ano}'])}; sem o Japão {li(lb[f'sem_o_Japao_{ano}'])}; 10 pares {li(lb[f'10_pares_{ano}'])}; 50 pares {li(lb[f'50_pares_{ano}'])};"
          f" espelho g (depois das 17h de Brasília) {li(lb[f'espelho_g_depois_das_17h_{ano}'])}; f e g juntos: f {fz(fg['inclinacao_f'])} (ep {fz(fg['ep_cr1_f'])}), g {fz(fg['inclinacao_g'])} (ep {fz(fg['ep_cr1_g'])});"
          f" desfecho branco e nulo {li(lb[f'espelho_branco_nulo_{ano}'])}.")
    t1 = lb['tirando_um_pais_2026']
    w(f"  2026, tirando um país de cada vez: inclinação de {fz(t1['minimo'])} (sem {t1['sem_o_pais_min']}) a {fz(t1['maximo'])} (sem {t1['sem_o_pais_max']}).")
    w(f"  Leitura com o ep CR1 no lugar do bootstrap: {pb['leitura_com_ep_cr1']}.")
    w('')
    w('4. Calibração por efeito plantado nos dados de 2026 (partes a e b)')
    for parte, nome in (('a', 'DiD'), ('b', 'inclinação')):
        for cen, r in cal[parte].items():
            if not isinstance(r, dict):
                continue
            w(f"  ({parte}) {cen}: {nome} com plantio {fz(r['estatistica_com_plantio'])}; deslocamento {fz(r['deslocamento'])} (esperado {fz(-r['delta'])}; recuperação {fz(100 * r['recuperacao'], 0)}%;"
              f" {fz(r['deslocamento_em_ep'], 1)} ep); poder de medida: {'sim' if r['poder_de_medida'] else 'não'}; critério de sinal dispara com o plantio: {'sim' if r['criterio_de_sinal_dispara_com_plantio'] else 'não'}.")
        w(f"  ({parte}) menor efeito que o critério enxergaria numa base sem desvio: {fz(cal[parte]['menor_efeito_que_o_criterio_enxerga_em_base_sem_desvio'])} ponto.")
    w('')
    w('5. Parte (c): seções do Brasil com zero habilitação biométrica de fato')
    e = Cc['estrutura']; bo = Cc['boletins']
    w(f"  Estrutura: {fi(e['secoes_do_brasil_no_bweb_2t_com_comparecimento'])} seções do Brasil; sem nenhum eleitor com biometria no perfil: {e['secoes_sem_nenhum_eleitor_com_biometria_no_perfil']};"
      f" com NH maior ou igual aos eleitores com biometria: {e['secoes_com_NH_maior_ou_igual_aos_eleitores_com_biometria']}; com Bmin até 5 pelo perfil: {e['secoes_com_Bmin_ate_5_pelo_perfil']}.")
    w(f"  Boletins lidos: {fi(bo['secoes_com_boletim'])} seções ({fi(bo['coerentes_com_o_bweb'])} coerentes com o bweb, {bo['excluidos_por_discordancia']} excluídos). Por pasta: " +
      '; '.join(f"{p}: {v['secoes_novas']}" for p, v in Cc['boletins_lidos_por_pasta'].items()))
    w(f"  Cobertura da lista de download: {json.dumps(e['cobertura_da_lista_de_download'], ensure_ascii=False)}; B = 0 por estrato: {json.dumps(e['B_igual_a_zero_por_estrato_da_lista'], ensure_ascii=False)}.")
    w(f"  Presos e internação ({e['secoes_de_preso_provisorio_no_bweb_2t']} seções): {e['presos_com_boletim']} com boletim, {e['presos_com_B_zero']} com B = 0; soma S, B, M = {e['presos_soma_S_B_M']}."
      f" Voto em trânsito ({e['secoes_de_voto_em_transito_no_bweb_2t']}): {e['transito_com_boletim']} com boletim, {e['transito_com_B_zero']} com B = 0; soma S, B, M = {e['transito_soma_S_B_M']}.")
    w(f"  Exterior: {bo['boletins_do_exterior_baixados']} boletins baixados (uma seção de cada uma das 12 cidades com mais seções); com o campo de habilitações [S, B, M]: {bo['boletins_do_exterior_com_o_campo_de_habilitacoes']}."
      " O boletim do exterior não traz o campo: a urna de lá roda sem o módulo de biometria. No Brasil todos os boletins lidos trazem o campo.")
    w(f"  Z (B = 0): {e['Z_total']} seção(ões): " + '; '.join(f"{k} S {v['S']} M {v['M']} ({v['tipo_do_local']})" for k, v in e['Z_detalhe'].items()))
    for nome, rot in (('Z', 'Z, zero habilitação de fato'), ('Z_nao_presos', 'Z fora de presos'), ('P_presos', 'P, presos e internação pelo tipo do local (com biometria)'), ('Q_espelho', 'Q, espelho: pouca biometria, B > 0')):
        r = Cc[nome]
        if r['secoes_no_universo'] == 0:
            w(f"  {rot}: nenhuma seção no universo."); continue
        b_ = r['bruto']
        def le(x):
            return 'n/d' if not x else f"{fz(x['d'])} (ep {fz(x['ep'])})"
        pq = r.get('pareado_como_o_exterior')
        if r.get('aviso'):
            w(f"  {rot}: {r['secoes_no_universo']} seção(ões), {fi(r['votos_finalistas_2t'])} votos; virada {fz(b_['virada_grupo'])}; Lula no 1º turno {fz(b_['f1_grupo'], 1)};"
              f" diferença bruta para as vizinhas do local {fz(r['local']['d']) if r.get('local') else 'n/d'} e da zona {fz(r['zona']['d']) if r.get('zona') else 'n/d'}; {r['aviso']}.")
            continue
        w(f"  {rot}: {r['secoes_no_universo']} seções, {fi(r['votos_finalistas_2t'])} votos; virada {fz(b_['virada_grupo'])} contra {fz(b_['virada_brasil'])} no resto do Brasil; Lula no 1º turno {fz(b_['f1_grupo'], 1)};"
          f" d no local {le(r['local'])}, {r['informam_local']} informam; d na zona {le(r['zona'])}, {r['informam_zona']} informam; com covariáveis: local {le(r.get('local_com_covariaveis'))}, zona {le(r.get('zona_com_covariaveis'))};"
          f" pareado como o exterior: {'n/d' if not pq else fz(pq['D']) + ' (ep ' + fz(pq['ep_por_municipio']) + ')'}"
          + (f"; permutação na zona p {fz(r['permutacao_na_zona']['p_bilateral'], 3)}" if r.get('permutacao_na_zona') else '') + '.')
    w(f"  Leitura de P e de Q pelo mesmo critério numérico (não é o veredito): P {Cc['P_presos'].get('leitura_pelo_mesmo_criterio')} pelo estimador de {Cc['P_presos'].get('estimador_da_leitura')};"
      f" Q {Cc['Q_espelho'].get('leitura_pelo_mesmo_criterio')} pelo estimador de {Cc['Q_espelho'].get('estimador_da_leitura')}."
      " P não vale como condição da H1: os boletins mostram habilitação por biometria em todas as seções de presos; a diferença bruta para a zona some quase toda com as covariáveis.")
    x8 = Cc.get('X8_exploratorio_dose_sem_biometria')
    if x8:
        dq, dp = x8['dose_dentro_do_local_nos_locais_de_Q'], x8['dose_dentro_do_local_no_pais']
        w(f"  X8, EXPLORATÓRIO (depois de ver Q): habilitação sem biometria, nb = (S + M)/comparecimento. Q tem nb médio de {fz(x8['nb_medio_Q_exato'])} (exato, do boletim); as vizinhas de local, {fz(x8['nb_medio_vizinhas_de_local_de_Q_aprox'])} (aproximado pelo perfil);"
          f" presos {fz(x8['nb_medio_presos_exato'])}; Brasil {fz(x8['nb_medio_brasil_aprox'])}. Se a troca poupasse o voto habilitado sem biometria, Q ficaria {fz(x8.get('d_previsto_para_Q_se_a_troca_poupasse_o_voto_sem_biometria'))} abaixo das vizinhas; observado {fz(x8.get('d_observado_Q_local'))} (ep {fz(x8.get('ep_observado_Q_local'))})."
          f" Dose dentro do local, virada contra nb: nos locais de Q {fz(dq['inclinacao_por_unidade'])} (ep {fz(dq['ep'])}; {fi(dq['n'])} seções, {fi(dq['locais'])} locais), com covariáveis {fz(x8['dose_nos_locais_de_Q_com_covariaveis']['inclinacao_por_unidade'])} (ep {fz(x8['dose_nos_locais_de_Q_com_covariaveis']['ep'])}),"
          f" placebo de nível nesses locais {fz(x8['placebo_nivel_f1_nos_locais_de_Q']['inclinacao_por_unidade'])} (ep {fz(x8['placebo_nivel_f1_nos_locais_de_Q']['ep'])});"
          f" só seções com boletim, nb exato dos dois lados: {fz(x8['dose_dentro_do_local_so_com_boletim_nb_exato'].get('inclinacao_por_unidade'))} (ep {fz(x8['dose_dentro_do_local_so_com_boletim_nb_exato'].get('ep'))}; {fi(x8['dose_dentro_do_local_so_com_boletim_nb_exato'].get('n', 0))} seções); no país {fz(dp['inclinacao_por_unidade'])} (ep {fz(dp['ep'])}; {fi(dp['n'])} seções),"
          f" com covariáveis {fz(x8['dose_dentro_do_local_no_pais_com_covariaveis']['inclinacao_por_unidade'])} (ep {fz(x8['dose_dentro_do_local_no_pais_com_covariaveis']['ep'])});"
          f" placebo de nível (Lula no 1º turno contra nb, dentro do local) {fz(x8['placebo_nivel_f1_dentro_do_local_no_pais']['inclinacao_por_unidade'])} (ep {fz(x8['placebo_nivel_f1_dentro_do_local_no_pais']['ep'])}). A hipótese de dose preveria -1,785 por unidade.")
    for g, cg in Cc['calibracao'].items():
        for cen, ce in cg.items():
            for en, r in ce.items():
                if r['secoes_que_informam'] < 100:
                    if cen == 'uniforme_1,785' and en == 'zona':
                        w(f"  Calibração {g}: {r['secoes_que_informam']} seção(ões) informam, menos que as 100 do critério; o plantio de 1,785 não pode ser medido contra um erro-padrão. SEM PODER.")
                    continue
                w(f"  Calibração {g}, {cen}, {en}: d com plantio {fz(r['estatistica_com_plantio'])} (ep {fz(r['ep_com_plantio'])}); deslocamento {fz(r['deslocamento'])}; recuperação {fz(100 * r['recuperacao'], 0)}%;"
                  f" {fz(r['deslocamento_em_ep'], 1)} ep; poder de medida: {'sim' if r['poder_de_medida'] else 'não'}; critério dispara: {'sim' if r['criterio_de_sinal_dispara_com_plantio'] else 'não'} ({r['secoes_que_informam']} seções informam).")
    w('')
    w('6. Tradução em votos (se o desvio valesse para as seções do Brasil; a margem muda o dobro dos votos trocados)')
    for nome, r in tr.items():
        if nome == 'exterior_inteiro':
            continue
        w(f"  {nome}: {fz(r['pontos'])} ponto = {fi(r['votos_trocados_se_valesse_para_o_brasil'])} votos trocados, {fi(r['efeito_na_margem'])} de margem ({fz(100 * r['fracao_da_margem_oficial'], 0)}% da margem oficial; {fz(100 * r['fracao_da_regua_1,785'], 0)}% da régua).")
    if o.get('traducao_parte_c'):
        w('  Parte (c): ' + o['traducao_parte_c'] + '.')
    x = tr['exterior_inteiro']
    w(f"  Exterior inteiro no 2º turno: {fi(x['secoes_2t'])} seções, {fi(x['aptos_2t'])} aptos, {fi(x['comparecimento_2t'])} de comparecimento; Lula {fi(x['lula_2t'])}, Flávio {fi(x['flavio_2t'])};"
      f" {fi(x['votos_finalistas_2t'])} votos nos finalistas ({fz(100 * x['votos_finalistas_como_fracao_do_total'], 2)}% do total; {fz(100 * x['votos_finalistas_como_fracao_da_margem'], 1)}% da margem)."
      f" Margem nacional sem o exterior: {fi(x['margem_nacional_sem_o_exterior'])}; se todo voto do exterior fosse de Flávio: {fi(x['margem_nacional_se_todo_voto_do_exterior_fosse_de_flavio'])}.")
    w('')
    w('7. Fusos')
    w(f"  Fonte: {o['fusos']['fonte']}. Brasília: {o['fusos']['brasilia']}.")
    w('  Cidades de 2026 (votos nos finalistas; UTC; f; D 2026; D 2022; D 2018; DiD): ' + '; '.join(
        f"{c['cidade']} {fi(c['votos_finalistas'])} {fz(c['utc_2026'], 1)} {fz(c['f'], 2)} {fz(c['D_2026'])} {fz(c['D_2022'])} {fz(c['D_2018'])} {fz(c['DiD'])}" for c in o['cidades_2026']))
    if o.get('exploratorio'):
        w('')
        w('8. EXPLORATÓRIO (feito depois de ver os resultados; não muda veredito)')
        for linha in o['exploratorio'].get('texto', []):
            w('  ' + linha)
    if o.get('leitura'):
        w('')
        w('LEITURA')
        for linha in o['leitura']:
            w('  ' + linha)
    txt = '\n'.join(L) + '\n'
    for ch in (chr(0x2014), chr(0x2013)):
        txt = txt.replace(ch, '-')
    with open(caminho, 'w') as f:
        f.write(txt)


if __name__ == '__main__':
    modo = sys.argv[1] if len(sys.argv) > 1 else 'rodar'
    if modo == 'estrutura':
        estrutura()
    elif modo == 'texto':
        escrever_txt(json.load(open(SAIDA_JSON)), SAIDA_TXT)
    else:
        main()
