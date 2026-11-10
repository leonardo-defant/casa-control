"""R27_C2: GATILHO POR HORÁRIO (teste D1.4 de registro/adendo27/desenho_D1_proposta.json, com a fragilidade
"T30 (gatilho por horário e por contagem)" de registro/adendo27/equipe_vermelha_relatorio.json).

Adendo 27 do pré-registro (commit 2748895, 10/11/2026 00:16:42 UTC), Onda C, item C2, na ordem do Adendo 28 (commit
938be19) e do Adendo 30 (commit a7218fb, 10/11/2026 10:08:24 UTC: "C2 (gatilho por horário, agora com os logs das duas
amostras)"). Os critérios valem como escritos nos campos estatistica, criterio_sinal, criterio_sem_sinal, poder e
placebo do D1.4 e nos campos reteste_proposto e criterio_proposto da fragilidade T30. Este docstring foi escrito ANTES
de qualquer conta deste teste com votos por candidato. O que ele decide e o registro não fixa está em DECISÕES e sai no
resultado como desvio. O que for feito depois de ver resultado fica em funções com nome "exploratorio_" e sai marcado.
Aviso do registro: o D1.4 é desenho cego; o reteste do T30 foi escrito por quem conhecia o resultado antigo (o critério
é novo, a escolha do que retestar é posterior ao dado).

Uso (sempre com python3 -I):
  scripts/analisar_R27_C2.py extrair   lê os logs das três listas (sem voto por candidato) e grava a hora de cada voto
  scripts/analisar_R27_C2.py rodar     roda tudo e grava resultados/R27_C2_gatilho_por_horario.json e .txt
Trabalho e parciais: /home/user/trabalho-eleicao/adendo27/R27_C2/

O QUE EU JÁ SABIA ANTES DE ESCREVER (contaminação declarada)
- Do T30 antigo (Adendos 9 e 12, texto da equipe vermelha): às 16h inclinação +11,3 (z 4,2) no desenho registrado e
  +4,1 (ep 2,1) em R2; às 14h +5,0 (z 3,6); placebo de nível falhando por composição. Logo a escolha de olhar o
  horário não é cega; o que é novo é o critério, a amostra aleatória e a calibração.
- Do desenho D1 (observações de estrutura): perfil horário dos votos da amostra antiga (17% às 8h ... 5% às 16h, 0,03%
  depois das 17h), 334 e 3 nulos por suspensão de presidente, 187 seções com governador no 2º turno.
- Da Onda B (C1): cerca de 36 mil votos depois das 17h de Brasília no país e zero depois das 19h, pela amostra antiga;
  novidades: o TSE fala em cerca de 34 mil votos na prorrogação. A Parte 2 confere isso com amostra própria das
  prorrogadas, que ninguém leu ainda.
- Estrutura que eu mesmo levantei antes de escrever, sem voto por candidato (R27_C2/estrutura_tmp.py): votos no log
  iguais ao comparecimento do bweb em todos os pacotes; pares de dias no mesmo pacote: 3.874 de 3.897 (antiga), 2.986
  de 3.000 (aleatória), 398 de 400 (P); 28 seções estão nas duas amostras; fora do relógio de Brasília: 180 seções
  da antiga (AC 28, AM 28, MS 36, MT 52, RO 36) e 198 da aleatória (AC 20, AM 44, MS 41, MT 46, RO 37, RR 10);
  locais com 2 ou mais seções: 623 (3.757 seções) na antiga, 70 (141 seções) na aleatória, 693 (3.898) na união;
  municípios com 2 ou mais: 410, 455 (2.025 seções) e 750 (5.968). Ou seja: com efeito fixo de local a amostra
  aleatória quase não informa, e isso é dito antes de rodar.
- Para a Parte 0 abri os TIPOS de voto (sem candidato) de 309 RDV do 1º turno da amostra aleatória: os nulos por
  suspensão aparecem no RDV como tipo 6, em número igual ao do log (230 = 230), e nos 6 exemplos impressos estão no FIM
  da lista do cargo. Logo já espero que o marcador do desenho não informe a ordem (ver P0).
- Não eram conhecidos: nenhum coeficiente novo, nenhuma calibração, a contagem das prorrogadas.

=========================== O QUE O REGISTRO FIXA ===========================
D1.4 (desenho cego). Definições comuns: universo U = seções do 2º turno pareadas com o 1º, L2 + R2 de 30 ou mais,
fora o exterior e as seções com junta. y = 100 x L2/(L2 + R2). X = 1º turno na mesma seção: fração sobre o
comparecimento do 1º turno de 13, 22, cada um dos demais com 0,5% ou mais no país, resto agrupado, brancos, nulos;
abstenção do 1º turno; variação da abstenção; perfil do eleitorado (faixas etárias, sexo, escolaridade, fração com
biometria); ln dos aptos; posição da seção no local. Modelo base: y = efeito fixo de local + X + b x D + erro, peso
V = L2 + R2, erro agrupado por município. Phi = 2 x b x soma(D x V)/100/4.430.191.
  Estatística: hora de Brasília por seção. Para h em {10, 12, 14, 15, 16}: D_h = fração dos votos de presidente do 2º
  turno confirmados da hora h em diante; controle adicional: a mesma fração no 1º turno da mesma urna. Um h por vez, e
  um modelo conjunto com as frações por hora cheia (9 faixas). Phi_h usa a fração nacional da janela.
  Parte 2: votos computados depois das 17h de Brasília nas seções de encerramento tardio, expandidos para o total T.
  Parte 0: nas seções com RDV, a posição do voto no RDV guarda relação com a ordem de votação? Marcador: nulos por
  suspensão (hora conhecida no log), correlação de postos.
  SINAL: para algum h, Phi_h de 0,5 ou mais a favor de Lula, z de 3,9 ou mais, degrau no modelo conjunto na mesma hora
  (salto entre faixas vizinhas de pelo menos metade de b) e coeficiente do placebo de 1º turno de no máximo um terço.
  Prorrogação: se 2 x T passar de 443 mil votos (10% da margem), a janela é relevante e manda baixar todos os logs;
  abaixo disso a prorrogação não alcança 10% da margem mesmo que todos os votos dela fossem irregulares.
  SEM SINAL: só nas janelas em que o intervalo de 99% de Phi_h couber entre -0,5 e +0,5. Nas janelas largas (h = 10 e
  12) a amostra antiga não permite declarar ausência: INCONCLUSIVAS por desenho, salvo ampliação da amostra. Também
  inconclusivo: coeficiente significativo sem degrau, ou igual ao do 1º turno.
  Poder: em cada seção, mover de R para L um binomial com taxa f x D_h, f para Phi = 0,25; 0,5 e 1; 200 repetições.
  Placebo: a mesma regressão no 1º turno (desfecho: fração de Lula no 1º turno contra 2022; dose: perfil horário do 1º
  turno). Governador do 2º turno nas seções da amostra que têm governador. Janelas falsas em minuto quebrado no
  modelo conjunto.
T30 (equipe vermelha). Cortes de hora em hora (9h a 17h), nos dois relógios (Brasília e relógio da urna), regressor
f2 x fatia de Flávio no 1º turno, controles f1, variação do comparecimento e fatia de Lula no 1º turno, efeito fixo de
local, erro CV3. Placebo certo: a mesma regressão de virada com f1 do 1º turno no lugar de f2. Calibrar plantando
troca de 5%, 10% e 15% dos votos de Flávio depois do corte para obter o efeito mínimo detectável.
  SINAL: inclinação de 4 pontos ou mais com z CV3 acima de 3,2 (Bonferroni para 18 cortes) em R2, com dose crescente
  em pelo menos 3 horas vizinhas e placebo de virada abaixo de 2 ep.
  SEM SINAL: |inclinação| abaixo de 1,5 e efeito mínimo detectável (2,8 ep) abaixo da inclinação que uma troca de 5%
  produz na calibração. Fora disso, SEM PODER, dito assim.

=========================== DECISÕES QUE O REGISTRO NÃO FIXA (escritas antes de rodar) ===========================
LEITOR E RELÓGIO
E1. Leitor próprio. Pacote = -log.jez; blocos = logd.dat do pacote e de cada .jez aninhado. Um trecho só conta para a
    seção do pacote se a identidade corrente do bloco (linhas "Município:", "Zona Eleitoral:", "Seção Eleitoral:" do
    aplicativo GAP) for a da seção; trecho sem identidade conhecida só entra se for do logd.dat principal.
E2. Dias 04/10/2026 (1º turno) e 25/10/2026 (2º turno), aplicativo VOTA. Voto = "O voto do eleitor foi computado".
    Hora do voto de presidente = hora de "Voto confirmado para [Presidente]" desse eleitor; se não houver (nulo por
    suspensão), a hora do voto computado. Nas contas da Parte 2 vale a hora do voto computado, como escrito.
E3. Fuso por MUNICÍPIO (a equipe vermelha pede que não seja por UF): deslocamento = 8 menos a hora modal de abertura
    (campo ab do bweb do 2º turno, arredondada) entre todas as seções do município. Hora de Brasília = hora do log
    mais o deslocamento. Relógio da urna = hora do log.
E4. Par = seção com votos próprios nos dois dias no mesmo pacote. Universo de cada amostra = pares em U (fora o
    exterior, L2 + R2 de 30 ou mais, L1 + R1 maior que zero). Votos por seção: dados/secoes2026.json.gz.
AMOSTRAS E EFEITO FIXO
A1. ANT = amostra antiga (amostra2t/arq, não aleatória). AAS = amostra aleatória simples nova (aas/t2). UNI = união
    das duas, cada seção uma vez, sem peso de desenho (o contraste é dentro do grupo).
A2. Especificação da letra: efeito fixo de LOCAL (lib.chave_local com o local do 2º turno), nas três amostras. A AAS
    com efeito fixo de local usa só 70 locais: sai relatada e, se a calibração confirmar, como SEM PODER.
    Ao lado, fixadas agora e sem substituir a letra: efeito fixo de MUNICÍPIO (ANT, AAS e UNI) e de UF (AAS e UNI).
    Essas controlam menos a composição (prédios diferentes do mesmo município) e por isso só valem como leitura de
    apoio; a AAS com efeito fixo de UF é a única conta em que a amostra é aleatória simples do país.
A3. Veredito de cada parte: o da especificação da letra na UNI (a maior amostra com efeito fixo de local), com ANT e
    AAS ao lado. "Salvo ampliação da amostra": na UNI a regra do intervalo de 99% vale para as cinco janelas; na ANT
    sozinha h = 10 e 12 ficam INCONCLUSIVAS por desenho.
PARTE 0 (antes de qualquer conta com candidato)
P0. Marcador = entradas de tipo 6 do cargo presidente no RDV (nulo sem dígitos), quando o número delas é igual ao de
    nulos por suspensão de presidente no log do mesmo dia. Dados: RDV do 1º e do 2º turno da AAS e RDV do 2º turno da
    ANT (onde houver). u_rdv = (posição + 0,5)/N e u_log = (ordem do eleitor no dia + 0,5)/N. Estatística: correlação
    de postos (Spearman) entre u_rdv e u_log, todos os marcadores juntos, com erro 1/raiz(n - 1). "Guarda relação" se
    |r| for 3 erros ou mais: nesse caso o desenho teria de ser reescrito voto a voto antes de olhar candidato, e este
    script para. Ao lado: fração dos marcadores nas últimas posições da lista (se o programa grava o tipo 6 à parte,
    no fim, o marcador não mede a ordem dos demais votos e a Parte 0 fica SEM PODER, dito assim); e, para saber se a
    lista está ordenada por tipo, a posição média normalizada dos brancos (tipo 3) e dos nulos digitados (tipo 4).
PARTE A (D1.4, modelo base)
D1. Candidatos com 0,5% ou mais no país no 1º turno: 70, 14 e 55 (além de 13 e 22); "resto" = demais nominais. X =
    frações sobre o comparecimento do 1º turno de 13, 22, 70, 14, 55, resto e brancos (nulos = referência), abstenção
    do 1º turno, abstenção do 2º menos a do 1º, fração com biometria, fração de mulheres, 7 faixas de idade (25 a 34
    = referência), 7 graus de escolaridade (o primeiro = referência), ln dos aptos do 2º turno e posição (posto do
    número da seção entre as seções do local no bweb, de 0 a 1; 0,5 se o local tem uma seção). Perfil: extração do
    F15 feita na A6 (R27_A6/perfil_secao_2026_A6.json.gz, sem votos). Seção sem perfil sai do modelo base.
D2. D_h = fração dos votos de presidente do 2º turno com hora de Brasília >= h:00:00; controle D1_h = o mesmo no 1º
    turno. Erro CR1 agrupado por município (com a correção de lib.fe_ols). z = b/ep. Intervalo de 99% = 2,576 ep.
D3. Fração nacional da janela: F_h = soma(D_h x V)/soma(V) nos pares da AAS em U (amostra aleatória simples; a ANT
    não tem peso de desenho guardado). Phi_h = 2 x b x F_h x 124.082.273/100/4.430.191 nas três amostras.
D4. Modelo conjunto: frações por hora cheia de Brasília, 9 faixas (antes das 9h = referência; 9h, 10h, ..., 15h; 16h
    em diante), com as mesmas 8 frações do 1º turno como controle e o X. Degrau em h: c_h - c_(h-1) >= b_h/2, com
    c_8 = 0. Janelas falsas: uma por vez, a fração dos votos entre h:37 e (h+1):00 somada ao modelo conjunto (h de
    9 a 15); o coeficiente é o salto dentro da hora; conto |z| >= 2 e saltos >= metade do b da janela vizinha.
D5. Placebo de 1º turno: desfecho 100 x L1/(L1 + R1) de 2026; controles: 100 x L/(L + R) do 2º turno de 2022 na
    mesma chave, frações de L, R, brancos e nulos sobre o comparecimento do 1º turno de 2022, abstenção do 1º turno
    de 2022, abstenção do 1º turno de 2026 menos a de 2022, perfil, ln dos aptos do 1º turno, posição; peso L1 + R1;
    dose D1_h. Só seções com a chave em 2022 e L + R de 30 ou mais nos dois turnos de 2022. "No máximo um terço":
    |b do placebo| <= |b|/3. "Igual ao do 1º turno": |b - b do placebo| menor que 2 erros da diferença.
    Como o Léo suspeita de 2022, o valor bruto de 2026 vai ao lado: a mesma regressão do placebo SEM nenhum controle
    de 2022 (só perfil, ln dos aptos, posição), e a tabela bruta por quintil de D_12 e D_15.
D6. Secundários (ao lado): y_BN = 100 x (B2 + N2)/comparecimento do 2º turno com o mesmo X; y_alt = y menos
    100 x L/(L + R) do 2º turno de 2022, com controles de 2022 (frações do 1º turno de 2022, abstenção do 1º turno de
    2022, variação da abstenção de 2022, abstenção do 2º turno de 2026 menos a de 2022, perfil, ln dos aptos,
    posição), sem o controle D1_h (serve ao caso de a irregularidade existir também no 1º turno).
D7. Placebo de governador (ao lado, não decide): AC, AM, DF, ES, RN e TO; desfecho 100 x votos do finalista "do lado
    de Lula"/votos dos dois finalistas a governador no 2º turno (lado = o de correlação ponderada positiva com y nas
    seções da UF; extração do bweb feita na B1); controles próprios de cada UF: frações do 1º turno dos dois
    finalistas sobre o comparecimento; mais variação da abstenção, 100 x L1/(L1 + R1) de presidente e D1_h; dose D_h.
D8. Regiões (ao lado): b por região na janela, para a cláusula geral "mesmo sentido em 4 das 5".
D9. Calibração: 200 cópias por janela e tamanho, semente 20261110. Em cada seção m ~ Binomial(R2, f x D_h), movidos
    de R2 para L2; f = Phi x 2.215.095,5/(F^R_h x 59.826.041), com F^R_h = soma(D_h x R2)/soma(R2) na AAS (f limitado
    a 1). Em cada cópia: b, z, Phi, degrau. "Enxerga" = z >= 3,9 e Phi >= metade do plantado. Recuperação = (Phi médio
    das cópias - Phi observado)/Phi plantado.
    Explicações inocentes plantadas com o mesmo total de votos de Phi = 0,5 (200 cópias cada):
      I1 rampa suave no 2º turno: taxa proporcional à média, na seção, de (hora de Brasília - 8h)/9h, entre 0 e 1;
      I2 composição: taxa proporcional ao perfil horário do 1º TURNO da seção (D1_h no lugar de D_h).
    Conto em quantas cópias o critério inteiro de SINAL dispara. Espelho: o mesmo plantio de L2 para R2 (Phi = -0,5
    e -1), que o teste tem de ver com o sinal trocado; e contraste do mesmo tamanho a favor de Flávio nos dados
    reais (Phi <= -0,5 com z <= -3,9) relatado com o mesmo destaque.
D10. Veredito por janela, nesta ordem: SEM PODER se o plantio de Phi = 1 for enxergado em menos de 95% das cópias (a
    regra obrigatória desta onda; passa por cima do INCONCLUSIVO do desenho); SINAL pela letra; SEM SINAL se o
    intervalo de 99% de Phi couber em -0,5 a +0,5 e a recuperação do plantio de 0,5 ficar entre 0,8 e 1,2;
    INCONCLUSIVO no resto. Veredito da parte: SINAL se alguma janela der SINAL; SEM SINAL se as cinco derem SEM SINAL;
    senão o rótulo mais fraco entre as janelas, com a lista de quais janelas têm qual rótulo.
PARTE B (T30 da equipe vermelha, 18 cortes)
T1. y = fat2 - fat1, fat_t = 100 x L_t/(L_t + R_t). f_t(h) = fração dos votos de presidente do turno t com hora >=
    h:00:00, h de 9 a 17, no relógio de Brasília e no relógio da urna (18 cortes; nas seções sem deslocamento os dois
    relógios são o mesmo número). Fatia de Flávio no 1º turno = rho1 = R1/(L1 + R1), de 0 a 1 (a mesma escala da
    "fatia de Lula no 1º turno" do T30, que é 100 x L1/(L1 + R1)). Regressor = f2(h) x rho1. Controles: f1(h),
    dcomp = 100 x (comp2 - comp1)/aptos do 2º turno, fat1. Sem f2 sozinho entre os controles (a letra não o lista);
    ao lado, a versão com f2 e f1 x rho1 a mais, e a versão do Adendo 12 (regressor f2, R2). Peso L2 + R2.
T2. Erro CV3 = jackknife tirando um grupo de cada vez, raiz((G - 1)/G x soma dos desvios ao quadrado), grupo = o do
    efeito fixo (local na letra), como no Adendo 12. Ao lado: CR1 e CV3 por município. Com efeito fixo de UF o
    agrupamento é o município (CV3 exato nos dados reais, CR1 nas cópias da calibração).
T3. Placebo de virada (letra: "com f1 no lugar de f2"): regressor f1(h) x rho1, controles f1(h), dcomp, fat1.
    "Abaixo de 2 ep": |b do placebo| < 2 x ep CV3 do placebo. Ao lado, a troca completa de papéis (regressor
    f1 x rho1, controle f2).
T4. "Dose crescente em pelo menos 3 horas vizinhas": existe uma sequência de 3 cortes de horas seguidas do mesmo
    relógio, contendo o corte que passa em valor e z, em que a inclinação é positiva nos três e não diminui quando o
    corte avança. Ao lado, leitura mais frouxa: inclinação positiva com z CV3 de 2 ou mais em 3 cortes seguidos.
T5. Calibração: 200 cópias por corte e taxa q (5%, 10%, 15%), semente 20261110: m ~ Binomial(R2, q x f2(h)), de R2
    para L2. "Inclinação que a troca de 5% produz" = média das cópias menos o observado. EMD = 2,8 x ep CV3 do
    observado, em pontos de inclinação, em q (pela inclinação por unidade de q da calibração) e em fração da margem
    (2 x q x soma nacional de R2 x f2(h), pela AAS, sobre 4.430.191). Poder = fração das cópias com inclinação >= 4 e
    z CV3 > 3,2; e fração com o critério inteiro (com T3 e T4).
    Inocentes (200 cópias, total de votos igual ao da troca de 10% depois das 14h de Brasília): I1 rampa suave no 2º
    turno; I2 composição pelo perfil do 1º turno (taxa q x f1(14h)). Conto os cortes que dão SINAL em cada cópia.
    Espelho: regressor f2(h) x fatia de Lula no 1º turno (1 - rho1), SINAL espelhado se inclinação <= -4 com z CV3
    < -3,2; plantio espelhado de 10% dos votos de Lula depois do corte, de L2 para R2, nos cortes de 12h, 14h e 16h.
T6. Veredito por corte pela letra (SINAL, SEM SINAL, senão SEM PODER). Da parte: SINAL se algum corte der SINAL;
    SEM SINAL se os 18 derem SEM SINAL; senão SEM PODER nos cortes que não fecham, com a lista. Quando a inclinação
    for significativa (z CV3 de 2 ou mais) entre 1,5 e 4, o rótulo da letra continua SEM PODER, mas digo que o corte
    é intermediário e não falta de precisão.
T7. Separação dos relógios (ao lado): nas seções com deslocamento diferente de zero, a mesma regressão por corte nos
    dois relógios, com efeito fixo de município; e o número de seções que a sustenta.
PARTE 2 (prorrogação)
R1. Desvio declarado: em vez de 600 das 7.089 seções que encerraram às 18h locais ou depois, sorteio proporcional por
    UF, uso a lista P já registrada e baixada (400 sorteadas por ordem de SHA-256 entre as 6.773 seções, fora o
    exterior, que encerraram às 18:30 de Brasília ou depois). Refaço o universo P com o campo enc da base e E3.
R2. T17 da seção = votos computados no 2º turno com hora de Brasília >= 17:00:00. T_P = 6.773 x média na amostra P,
    erro de amostra aleatória simples com correção de população finita. As seções fora de P (inclusive as que
    encerraram entre 18:00 e 18:30) entram por T_resto = N_resto x média de T17 nas seções da AAS fora do universo P
    e fora do exterior, N_resto = seções do bweb do 2º turno fora do exterior menos 6.773. T = T_P + T_resto.
    Letra: compara 2 x T com 443.019. Ao lado: limite superior de 95% e de 99% de 2 x T; votos por faixa (17h, 18h,
    19h em diante); a mesma conta no dia do 1º turno (espelho: onde não houve a mesma prorrogação); calibração: 33
    votos sintéticos por seção de P em média (Poisson), total nacional esperado de 221.510, que a conta tem de
    devolver e acusar.
R3. Ao lado: cortes de 16h e 17h da Parte B na amostra P (efeito fixo de município), com o poder dito.
TRADUÇÃO EM VOTOS: Phi x 4.430.191 (Parte A); 2 x q x votos nacionais de Flávio depois do corte (Parte B); 2 x T
(Parte 2). Contagem de testes: 5 janelas + 18 cortes + 1 limite, em 3 amostras; digo quantos sinais o acaso daria.
"""
import os as _os, sys as _sys
_sys.path.insert(0, _os.path.dirname(_os.path.abspath(__file__)))
import collections, glob, gzip, hashlib, io, json, math, os, sys, time, zipfile
import numpy as np

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
TRAB = '/home/user/trabalho-eleicao/adendo27/R27_C2'
FONTES = {'ant': '/home/user/trabalho-eleicao/amostra2t/arq',
          'aas': '/home/user/trabalho-eleicao/adendo27/aas/t2',
          'c1p': '/home/user/trabalho-eleicao/adendo27/aas/c1p_t2'}
RDV_DIRS = {('aas', '1'): '/home/user/trabalho-eleicao/adendo27/aas/t1', ('aas', '2'): '/home/user/trabalho-eleicao/adendo27/aas/t2',
            ('ant', '2'): '/home/user/trabalho-eleicao/amostra2t/arq'}
PERFIL = '/home/user/trabalho-eleicao/adendo27/R27_A6/perfil_secao_2026_A6.json.gz'
GOV2 = '/home/user/trabalho-eleicao/adendo27/R27_B1/gov2t_6ufs_B1.json.gz'
DIAS = {'04/10/2026': '1', '25/10/2026': '2'}
MARGEM = 4430191; V_NAC = 64256232 + 59826041; R2_NAC = 59826041; L2_NAC = 64256232; N_SECOES_2T = 499205
N_P = 6773
SEMENTE = 20261110
CORTES = list(range(9, 18)); JANELAS = [10, 12, 14, 15, 16]
REGIAO = {**{u: 'N' for u in ('AC', 'AM', 'AP', 'PA', 'RO', 'RR', 'TO')},
          **{u: 'NE' for u in ('AL', 'BA', 'CE', 'MA', 'PB', 'PE', 'PI', 'RN', 'SE')},
          **{u: 'SE' for u in ('ES', 'MG', 'RJ', 'SP')}, **{u: 'S' for u in ('PR', 'RS', 'SC')},
          **{u: 'CO' for u in ('DF', 'GO', 'MS', 'MT')}}


def diz(*a):
    print(time.strftime('%H:%M:%S'), *a, flush=True)


def grava(nome, obj):
    with open(os.path.join(TRAB, nome), 'w') as f:
        json.dump(obj, f, ensure_ascii=False, indent=1, default=_js)


def _js(o):
    if isinstance(o, (np.floating,)): return float(o)
    if isinstance(o, (np.integer,)): return int(o)
    if isinstance(o, (np.bool_,)): return bool(o)
    if isinstance(o, np.ndarray): return o.tolist()
    raise TypeError(type(o))


# ============================== LEITOR DO LOG (sem voto por candidato) ==============================
def blocos(p):
    z = zipfile.ZipFile(p)
    for n in z.namelist():
        if n.startswith('logd'):
            yield n, z.read(n).decode('latin1').splitlines(), True
        elif n.endswith('.jez'):
            try:
                zz = zipfile.ZipFile(io.BytesIO(z.read(n)))
            except zipfile.BadZipFile:
                continue
            for m in zz.namelist():
                if m.startswith('logd'):
                    yield n + '/' + m, zz.read(m).decode('latin1').splitlines(), False


def _novo():
    return {'t': [], 'tc': [], 'susp': [], 'th': [], 'pronta': [], 'enc': [], 'bloco': []}


def ler_pacote(arg):
    fonte, p = arg
    partes = p.split('/')
    uf, mun, zona, sec = partes[-5].upper(), int(partes[-4]), int(partes[-3]), int(partes[-2])
    chave = f'{uf}|{mun}|{zona}|{sec}'
    out = {'fonte': fonte, 'blocos': 0, 'votos_de_outra_secao': {'1': 0, '2': 0}}
    dias = {'1': None, '2': None}
    modelos, series = set(), set()
    try:
        bl = list(blocos(p))
    except Exception as e:
        return chave, {'fonte': fonte, 'erro': repr(e)}
    for nome, linhas, principal in bl:
        out['blocos'] += 1
        idm = idz = ids = None
        pres = None; susp = False; hab = None
        for l in linhas:
            q = l.split('\t')
            if len(q) < 5:
                continue
            ts, ap, msg = q[0], q[3], q[4]
            if ap == 'GAP':
                if msg.startswith('Município: '):
                    try: idm = int(msg[11:])
                    except ValueError: idm = None
                    idz = ids = None
                elif msg.startswith('Zona Eleitoral: '):
                    try: idz = int(msg[16:])
                    except ValueError: idz = None
                elif msg.startswith('Seção Eleitoral: '):
                    try: ids = int(msg[17:])
                    except ValueError: ids = None
                elif msg.startswith('Identificação do Modelo de Urna'):
                    modelos.add(msg.split(': ')[-1])
                continue
            if ap != 'VOTA':
                continue
            d = DIAS.get(ts[:10])
            if d is None:
                continue
            t = int(ts[11:13]) * 3600 + int(ts[14:16]) * 60 + int(ts[17:19])
            conhecida = idm is not None and idz is not None and ids is not None
            propria = (conhecida and (idm, idz, ids) == (mun, zona, sec)) or (not conhecida and principal)
            if msg == 'O voto do eleitor foi computado':
                if not propria:
                    out['votos_de_outra_secao'][d] += 1
                else:
                    if dias[d] is None: dias[d] = _novo()
                    R = dias[d]
                    R['t'].append(pres if pres is not None else t)
                    R['tc'].append(t)
                    R['th'].append(hab if hab is not None else -1)
                    R['susp'].append(1 if susp else 0)
                    R['bloco'].append(out['blocos'] - 1)
                    series.add(q[2])
                pres = None; susp = False; hab = None
            elif msg == 'Voto confirmado para [Presidente]':
                pres = t
            elif msg.startswith('Atribuido voto nulo por suspensão') and '[Presidente]' in msg:
                susp = True
            elif msg == 'Eleitor foi habilitado':
                pres = None; susp = False; hab = t
            elif propria and msg == 'Urna pronta para receber votos':
                if dias[d] is None: dias[d] = _novo()
                dias[d]['pronta'].append(t)
            elif propria and (msg.startswith('Inicio do Encerramento') or msg.startswith('Início do Encerramento')):
                if dias[d] is None: dias[d] = _novo()
                dias[d]['enc'].append(t)
    out['modelo'] = sorted(modelos); out['series'] = sorted(series)
    out['1'] = dias['1']; out['2'] = dias['2']
    return chave, out


def modo_extrair():
    from multiprocessing import Pool
    res = {}
    for fonte, base in FONTES.items():
        arqs = sorted(os.path.join(r, n) for r, _, f in os.walk(base) for n in f if n.endswith('-log.jez'))
        with Pool(4) as pool:
            for k, o in pool.imap_unordered(ler_pacote, [(fonte, a) for a in arqs], chunksize=16):
                res[fonte + ':' + k] = o
        diz(fonte, 'pacotes', len(arqs))
    with gzip.open(TRAB + '/votos_hora.json.gz', 'wt') as f:
        json.dump(res, f, separators=(',', ':'))
    diz('gravado', len(res))


# ============================== REGRESSÃO ==============================
class Modelo:
    """MQO ponderado com efeito fixo absorvido, CR1 por agrupamento e jackknife (CV3) por agrupamento quando os grupos
    do efeito fixo estão contidos nos agrupamentos (tirar um agrupamento não muda as médias dos demais grupos)."""

    def __init__(self, X, fe, cl, w, jack=True):
        X = np.asarray(X, float)
        if X.ndim == 1: X = X[:, None]
        _, g = np.unique(np.asarray(fe), return_inverse=True)
        ok = np.bincount(g)[g] >= 2
        self.ok = ok
        X = X[ok]; w = np.asarray(w, float)[ok]
        _, g = np.unique(g[ok], return_inverse=True)
        _, c = np.unique(np.asarray(cl)[ok], return_inverse=True)
        self.g, self.c, self.w = g, c, w
        self.n, self.k = X.shape; self.G = int(g.max()) + 1; self.C = int(c.max()) + 1
        self.sw = np.bincount(g, weights=w, minlength=self.G)
        self.Xd = self._dm(X)
        self.WX = self.Xd * w[:, None]
        self.XtX = self.WX.T @ self.Xd
        self.inv = np.linalg.pinv(self.XtX)
        cmin = np.full(self.G, self.C); cmax = np.full(self.G, -1)
        np.minimum.at(cmin, g, c); np.maximum.at(cmax, g, c)
        self.nested = bool(np.all(cmin == cmax))
        self.Minv = None
        if jack and self.nested and self.C > 2:
            k = self.k
            A = np.zeros((self.C, k, k))
            for a in range(k):
                for b in range(a, k):
                    v = np.bincount(c, weights=self.WX[:, a] * self.Xd[:, b], minlength=self.C)
                    A[:, a, b] = v; A[:, b, a] = v
            self.Minv = np.linalg.pinv(self.XtX[None] - A)

    def _dm(self, M):
        M = np.asarray(M, float)
        if M.ndim == 1: M = M[:, None]
        out = np.empty_like(M)
        for j in range(M.shape[1]):
            mu = np.bincount(self.g, weights=self.w * M[:, j], minlength=self.G) / self.sw
            out[:, j] = M[:, j] - mu[self.g]
        return out

    def fit(self, y, cv3=True):
        yd = self._dm(np.asarray(y, float)[self.ok])[:, 0]
        Xty = self.WX.T @ yd
        b = self.inv @ Xty
        e = yd - self.Xd @ b
        S = np.column_stack([np.bincount(self.c, weights=self.WX[:, a] * e, minlength=self.C) for a in range(self.k)])
        corr = self.C / (self.C - 1) * (self.n - 1) / (self.n - self.k) if self.C > 1 else float('nan')
        Vb = corr * self.inv @ (S.T @ S) @ self.inv
        out = {'b': b, 'ep': np.sqrt(np.maximum(np.diag(Vb), 0)), 'V': Vb, 'n': self.n, 'G': self.G, 'C': self.C}
        if cv3 and self.Minv is not None:
            bg = np.column_stack([np.bincount(self.c, weights=self.WX[:, a] * yd, minlength=self.C) for a in range(self.k)])
            bj = np.einsum('gab,gb->ga', self.Minv, Xty[None] - bg)
            out['ep_cv3'] = np.sqrt((self.C - 1) / self.C * ((bj - bj.mean(0)) ** 2).sum(0))
        return out


def jack_exato(X, fe, cl, w, y, j=0):
    """CV3 exato do coeficiente j refazendo a regressão sem cada agrupamento (para efeito fixo que não cabe no agrupamento)."""
    X = np.asarray(X, float)
    if X.ndim == 1: X = X[:, None]
    cl = np.asarray(cl); fe = np.asarray(fe); bs = []
    for u in np.unique(cl):
        m = cl != u
        try:
            bs.append(Modelo(X[m], fe[m], cl[m], w[m], jack=False).fit(y[m], cv3=False)['b'][j])
        except (ValueError, np.linalg.LinAlgError):
            continue
    bs = np.array(bs); G = len(bs)
    return float(np.sqrt((G - 1) / G * ((bs - bs.mean()) ** 2).sum()))


# ============================== BASE ==============================
def carregar(c):
    with gzip.open(c, 'rt') as f:
        return json.load(f)


def fusos(B):
    abm = collections.defaultdict(list)
    for k, v in B.items():
        s = v.get('2')
        if s and s.get('ab') and not k.startswith('ZZ'):
            h, m, sg = (int(x) for x in s['ab'].split(':'))
            abm['|'.join(k.split('|')[:2])].append(round((h * 3600 + m * 60 + sg) / 3600))
    return {mun: 8 - collections.Counter(hs).most_common(1)[0][0] for mun, hs in abm.items()}


def seg(hms):
    h, m, s = (int(x) for x in hms.split(':'))
    return h * 3600 + m * 60 + s


def montar():
    """Tabela por seção das duas amostras (pares em U) com votos, controles e frações por hora. Lista P à parte."""
    B = carregar(REPO + '/dados/secoes2026.json.gz')
    C1 = carregar(REPO + '/dados/candidatos2026_1t.json.gz')['secoes']
    PF = carregar(PERFIL)['secoes']
    S22 = carregar(REPO + '/dados/secoes2022.json.gz')
    V = carregar(TRAB + '/votos_hora.json.gz')
    fuso = fusos(B)
    # posição no local e universo P, com a base inteira
    por_local = collections.defaultdict(list); univP = set(); n_br = 0
    for k, v in B.items():
        s = v.get('2')
        if not s or k.startswith('ZZ'):
            continue
        n_br += 1
        por_local[lib_local(k, s)].append(int(k.split('|')[3]))
        m = '|'.join(k.split('|')[:2])
        if s.get('enc') and m in fuso and seg(s['enc']) + 3600 * fuso[m] >= 18 * 3600 + 30 * 60:
            univP.add(k)
    for l in por_local.values(): l.sort()
    linhas = {}
    conta = collections.Counter()
    for kk, o in V.items():
        fonte, k = kk.split(':', 1)
        if fonte == 'c1p' or 'erro' in o:
            continue
        conta[fonte + '_pacotes'] += 1
        if not (o['1'] and o['2'] and o['1']['t'] and o['2']['t']):
            conta[fonte + '_sem_par'] += 1; continue
        if k.startswith('ZZ'):
            conta[fonte + '_exterior'] += 1; continue
        b = B.get(k)
        if not b or '1' not in b or '2' not in b:
            conta[fonte + '_sem_base'] += 1; continue
        a1, a2 = b['1'], b['2']
        if a2['L'] + a2['R'] < 30 or a1['L'] + a1['R'] <= 0:
            conta[fonte + '_fora_de_U'] += 1; continue
        if len(o['1']['t']) != a1['comp'] or len(o['2']['t']) != a2['comp']:
            conta[fonte + '_log_difere_do_comparecimento'] += 1
        conta[fonte + '_em_U'] += 1
        if k in linhas:
            linhas[k]['fontes'].add(fonte); continue
        m = '|'.join(k.split('|')[:2]); ds = fuso[m]
        t1 = np.array(o['1']['t']); t2 = np.array(o['2']['t']); tc2 = np.array(o['2']['tc'])
        r = {'k': k, 'fontes': {fonte}, 'uf': k.split('|')[0], 'mun': m, 'loc': lib_local(k, a2), 'desloc': ds,
             'a1': a1, 'a2': a2, 't1': t1, 't2': t2, 'tc2': tc2, 'tc1': np.array(o['1']['tc'])}
        linhas[k] = r
    ks = sorted(linhas)
    n = len(ks)
    T = {'k': ks, 'n': n}
    col = lambda f: np.array([f(linhas[k]) for k in ks])
    T['ant'] = col(lambda r: 'ant' in r['fontes']); T['aas'] = col(lambda r: 'aas' in r['fontes'])
    T['uf'] = col(lambda r: r['uf']); T['mun'] = col(lambda r: r['mun']); T['loc'] = col(lambda r: r['loc'])
    T['reg'] = np.array([REGIAO[u] for u in T['uf']]); T['desloc'] = col(lambda r: r['desloc'])
    for t in ('1', '2'):
        for c in ('L', 'R', 'O', 'B', 'N', 'comp', 'apt'):
            T[c + t] = col(lambda r, t=t, c=c: r['a' + t][c]).astype(float)
    cand = {}
    for num in ('70', '14', '55'):
        cand[num] = np.array([C1.get(k, {}).get(num, 0) for k in ks], float)
    T['c70'], T['c14'], T['c55'] = cand['70'], cand['14'], cand['55']
    T['cresto'] = T['O1'] - T['c70'] - T['c14'] - T['c55']
    # perfil
    pf = np.array([PF.get(k, [np.nan] * 19) for k in ks], float)
    T['tem_perfil'] = ~np.isnan(pf[:, 0]) & (np.nan_to_num(pf[:, 0]) > 0)
    tot = np.where(T['tem_perfil'], pf[:, 0], 1.0)
    T['perfil'] = np.column_stack([pf[:, 1] / tot, pf[:, 2] / tot] + [pf[:, i] / tot for i in (3, 4, 6, 7, 8, 9, 10)] +
                                  [pf[:, i] / tot for i in range(12, 19)])
    T['perfil'][~T['tem_perfil']] = 0.0
    # posição
    pos = []
    for k in ks:
        l = por_local[linhas[k]['loc']]; s = int(k.split('|')[3])
        pos.append(0.5 if len(l) < 2 else l.index(s) / (len(l) - 1))
    T['pos'] = np.array(pos)
    # 2022
    def de22(k):
        s = S22.get(k)
        if not s or '1' not in s or '2' not in s:
            return [np.nan] * 12
        a, b = s['1'], s['2']
        if a['L'] + a['R'] < 30 or b['L'] + b['R'] < 30 or a['comp'] <= 0 or a['apt'] <= 0 or b['apt'] <= 0:
            return [np.nan] * 12
        return [a['L'], a['R'], a['B'], a['N'], a['comp'], a['apt'], b['L'], b['R'], b['B'], b['N'], b['comp'], b['apt']]
    T['s22'] = np.array([de22(k) for k in ks], float)
    T['tem22'] = ~np.isnan(T['s22'][:, 0])
    # horas
    fB = {('1', h): np.zeros(n) for h in CORTES}; fB.update({('2', h): np.zeros(n) for h in CORTES})
    fU = {('1', h): np.zeros(n) for h in CORTES}; fU.update({('2', h): np.zeros(n) for h in CORTES})
    faixas = {'1': np.zeros((n, 9)), '2': np.zeros((n, 9))}
    quebr = {h: np.zeros(n) for h in range(9, 16)}
    rampa = np.zeros(n); t17 = {'1': np.zeros(n), '2': np.zeros(n)}
    for i, k in enumerate(ks):
        r = linhas[k]; ds = r['desloc'] * 3600
        for t, arr in (('1', r['t1']), ('2', r['t2'])):
            tb = arr + ds
            for h in CORTES:
                fB[(t, h)][i] = np.mean(tb >= h * 3600); fU[(t, h)][i] = np.mean(arr >= h * 3600)
            hb = np.clip(tb // 3600, 8, 16).astype(int) - 8
            faixas[t][i] = np.bincount(hb, minlength=9) / len(tb)
        tb2 = r['t2'] + ds
        for h in quebr:
            quebr[h][i] = np.mean((tb2 >= h * 3600 + 37 * 60) & (tb2 < (h + 1) * 3600))
        rampa[i] = np.mean(np.clip((tb2 - 8 * 3600) / (9 * 3600), 0, 1))
        t17['2'][i] = np.sum(r['tc2'] + ds >= 17 * 3600); t17['1'][i] = np.sum(r['tc1'] + ds >= 17 * 3600)
    T['fB'], T['fU'], T['faixas'], T['quebr'], T['rampa'], T['t17'] = fB, fU, faixas, quebr, rampa, t17
    T['em_univP'] = np.array([k in univP for k in ks])
    # lista P
    P = []
    for kk, o in V.items():
        fonte, k = kk.split(':', 1)
        if fonte != 'c1p' or 'erro' in o or not o['2'] or not o['2']['t']:
            continue
        m = '|'.join(k.split('|')[:2]); ds = fuso[m] * 3600
        tc2 = np.array(o['2']['tc']) + ds
        tc1 = (np.array(o['1']['tc']) + ds) if (o['1'] and o['1']['tc']) else np.array([])
        P.append({'k': k, 'em_univP': k in univP, 'n2': len(tc2), 'n1': len(tc1),
                  't17_2': int(np.sum(tc2 >= 17 * 3600)), 't18_2': int(np.sum(tc2 >= 18 * 3600)), 't19_2': int(np.sum(tc2 >= 19 * 3600)),
                  't17_1': int(np.sum(tc1 >= 17 * 3600)) if len(tc1) else None, 'ultimo_2': int(tc2.max()),
                  'comp2': B[k]['2']['comp'], 'enc_bweb': B[k]['2'].get('enc')})
    # AAS inteira para T_resto (todas as seções com log do 2º turno, não só os pares)
    aas_t17 = []
    for kk, o in V.items():
        fonte, k = kk.split(':', 1)
        if fonte != 'aas' or 'erro' in o or not o['2'] or not o['2']['t']:
            continue
        if k.startswith('ZZ'):
            aas_t17.append({'k': k, 'ext': True}); continue
        m = '|'.join(k.split('|')[:2]); ds = fuso[m] * 3600
        tc2 = np.array(o['2']['tc']) + ds
        tc1 = (np.array(o['1']['tc']) + ds) if (o['1'] and o['1']['tc']) else None
        aas_t17.append({'k': k, 'ext': False, 'em_univP': k in univP, 't17_2': int(np.sum(tc2 >= 17 * 3600)),
                        't18_2': int(np.sum(tc2 >= 18 * 3600)), 't19_2': int(np.sum(tc2 >= 19 * 3600)),
                        't17_1': None if tc1 is None else int(np.sum(tc1 >= 17 * 3600)), 'n2': len(tc2)})
    meta = {'contagens': dict(conta), 'n_uniao': n, 'universo_P_refeito': len(univP), 'secoes_brasil_2t': n_br,
            'deslocamentos': {s: dict(collections.Counter(int(x) for x in T['desloc'][T[s]])) for s in ('ant', 'aas')}}
    return T, P, aas_t17, meta, {'B': B, 'fuso': fuso}


def lib_local(k, s):
    uf, mun, zona, _ = k.split('|')
    return f"{uf}|{mun}|{zona}|{s['loc']}"


# ============================== PARTE 0 ==============================
def parte0(linhas_V):
    from ber import parse
    from decodificar import _int, _filhos

    def tipos_pres(f):
        top = parse(open(f, 'rb').read())[0][2]
        els = [n for n in top[2][2] if (n[0], n[1]) == (2, 1)][0][2]
        for el in els:
            for cargo in _filhos(_filhos(el)[1]):
                h = _filhos(cargo)
                if _int(h[0][2]) == 1:
                    return [_int(_filhos(v)[0][2]) for v in _filhos(h[2])]
        return None

    out = {}; ur, ul = [], []
    pos_b, pos_n = [], []
    for (fonte, dia), base in RDV_DIRS.items():
        c = collections.Counter(); urf, ulf = [], []
        for kk, o in linhas_V.items():
            f0, k = kk.split(':', 1)
            if f0 != fonte or 'erro' in o or not o[dia] or not o[dia]['t']:
                continue
            ns = sum(o[dia]['susp'])
            uf, m, z, s = k.split('|')
            fs = glob.glob(f'{base}/{uf.lower()}/{int(m):05d}/{int(z):04d}/{int(s):04d}/*-rdv.dat')
            if not fs:
                c['secoes_sem_rdv'] += 1; continue
            c['secoes_com_rdv'] += 1
            if ns == 0 and c['lidas_sem_suspensao'] >= 300:
                continue
            try:
                tp = tipos_pres(fs[0])
            except Exception:
                c['rdv_ilegivel'] += 1; continue
            if tp is None:
                c['rdv_sem_presidente'] += 1; continue
            N = len(tp); n6 = sum(1 for x in tp if x == 6)
            if ns == 0:
                c['lidas_sem_suspensao'] += 1; c['tipo6_em_secao_sem_suspensao'] += n6
            if N != len(o[dia]['t']):
                c['rdv_com_total_diferente_do_log'] += 1; continue
            for i, x in enumerate(tp):
                if x == 3: pos_b.append((i + 0.5) / N)
                elif x == 4: pos_n.append((i + 0.5) / N)
            if ns == 0:
                continue
            c['secoes_com_suspensao'] += 1; c['suspensoes_no_log'] += ns; c['tipo6_no_rdv'] += n6
            if n6 != ns:
                c['secoes_com_contagem_diferente'] += 1; continue
            p6 = [i for i, x in enumerate(tp) if x == 6]; pl = [i for i, x in enumerate(o[dia]['susp']) if x]
            c['marcadores'] += ns
            c['marcadores_no_fim_da_lista'] += sum(1 for j, i in enumerate(p6) if i >= N - ns)
            for a, b in zip(p6, pl):  # i-ésimo tipo 6 do RDV com a i-ésima suspensão do dia
                urf.append((a + 0.5) / N); ulf.append((b + 0.5) / N)
        d = dict(c); d['spearman'] = spearman(urf, ulf)
        out[f'{fonte}_{dia}t'] = d; ur += urf; ul += ulf
    n = len(ur)
    r = spearman(ur, ul)
    ep = 1 / math.sqrt(n - 1) if n > 1 else float('nan')
    fim = sum(v.get('marcadores_no_fim_da_lista', 0) for v in out.values() if isinstance(v, dict))
    out['todos'] = {'marcadores': n, 'spearman': r, 'ep': ep, 'limite_3_ep': 3 * ep, 'guarda_relacao': bool(n > 1 and abs(r) >= 3 * ep),
                    'fracao_no_fim_da_lista': fim / n if n else None,
                    'u_rdv_medio': float(np.mean(ur)) if n else None, 'u_log_medio': float(np.mean(ul)) if n else None,
                    'brancos_posicao_media': float(np.mean(pos_b)) if pos_b else None, 'brancos_n': len(pos_b),
                    'nulos_digitados_posicao_media': float(np.mean(pos_n)) if pos_n else None, 'nulos_digitados_n': len(pos_n),
                    'ep_posicao_media_uniforme_brancos': 1 / math.sqrt(12 * len(pos_b)) if pos_b else None,
                    'ep_posicao_media_uniforme_nulos': 1 / math.sqrt(12 * len(pos_n)) if pos_n else None}
    t = out['todos']
    t['marcador_informa'] = bool(t['fracao_no_fim_da_lista'] is not None and t['fracao_no_fim_da_lista'] < 0.9)
    t['leitura'] = ('GUARDA RELAÇÃO: o desenho teria de ser reescrito voto a voto' if t['guarda_relacao'] else
                    ('sem relação medida entre posição no RDV e ordem de votação' if t['marcador_informa'] else
                     'SEM PODER: o programa grava o nulo por suspensão (tipo 6) no fim da lista do cargo, fora da ordem dos demais; '
                     'o marcador não mede a ordem dos outros votos'))
    return out


def spearman(a, b):
    if len(a) < 3:
        return float('nan')
    ra = np.argsort(np.argsort(a)).astype(float); rb = np.argsort(np.argsort(b)).astype(float)
    if ra.std() == 0 or rb.std() == 0:
        return float('nan')
    return float(np.corrcoef(ra, rb)[0, 1])


# ============================== PARTE A (D1.4) ==============================
def x_base(T):
    c1 = T['comp1']
    return np.column_stack([T['L1'] / c1, T['R1'] / c1, T['c70'] / c1, T['c14'] / c1, T['c55'] / c1, T['cresto'] / c1, T['B1'] / c1,
                            1 - c1 / T['apt1'], (1 - T['comp2'] / T['apt2']) - (1 - c1 / T['apt1']), T['perfil'],
                            np.log(T['apt2']), T['pos']])


def nacional_F(T):
    """Frações nacionais das janelas pela AAS (pares em U)."""
    a = T['aas']; V = T['L2'] + T['R2']
    out = {}
    for h in CORTES:
        D = T['fB'][('2', h)]
        out[h] = {'F_V': float((D[a] * V[a]).sum() / V[a].sum()), 'F_R': float((D[a] * T['R2'][a]).sum() / T['R2'][a].sum()),
                  'F_L': float((D[a] * T['L2'][a]).sum() / T['L2'][a].sum()), 'F_comp': float((D[a] * T['comp2'][a]).sum() / T['comp2'][a].sum()),
                  'F_V_relogio_da_urna': float((T['fU'][('2', h)][a] * V[a]).sum() / V[a].sum()),
                  'F_R_relogio_da_urna': float((T['fU'][('2', h)][a] * T['R2'][a]).sum() / T['R2'][a].sum()),
                  'F_V_na_antiga_sem_peso': float((D[T['ant']] * V[T['ant']]).sum() / V[T['ant']].sum())}
    return out


def phi(b, F):
    return 2 * b * F * V_NAC / 100 / MARGEM


def specs(T):
    """(nome, máscara, efeito fixo, agrupamento do CR1 da Parte A, grupo do CV3 da Parte B, da letra?)"""
    uni = np.ones(T['n'], bool)
    return [('ANT_local', T['ant'], 'loc', 'mun', 'loc', True), ('AAS_local', T['aas'], 'loc', 'mun', 'loc', True),
            ('UNI_local', uni, 'loc', 'mun', 'loc', True),
            ('ANT_municipio', T['ant'], 'mun', 'mun', 'mun', False), ('AAS_municipio', T['aas'], 'mun', 'mun', 'mun', False),
            ('UNI_municipio', uni, 'mun', 'mun', 'mun', False),
            ('AAS_uf', T['aas'], 'uf', 'mun', 'mun', False), ('UNI_uf', uni, 'uf', 'mun', 'mun', False)]


def parte_a(T, F, rng):
    res = {}
    V = T['L2'] + T['R2']; y = 100 * T['L2'] / V
    XB = x_base(T)
    ybn = 100 * (T['B2'] + T['N2']) / T['comp2']
    s = T['s22']
    with np.errstate(invalid='ignore', divide='ignore'):
        fat2_22 = 100 * s[:, 6] / (s[:, 6] + s[:, 7]); c22 = s[:, 4]
        X22 = np.column_stack([s[:, 0] / c22, s[:, 1] / c22, s[:, 2] / c22, s[:, 3] / c22, 1 - c22 / s[:, 5]])
        ab22_2 = 1 - s[:, 10] / s[:, 11]
    V1 = T['L1'] + T['R1']; y1 = 100 * T['L1'] / np.where(V1 > 0, V1, 1)
    ab26_1 = 1 - T['comp1'] / T['apt1']; ab26_2 = 1 - T['comp2'] / T['apt2']
    Xpl = np.column_stack([fat2_22, X22, ab26_1 - X22[:, 4], T['perfil'], np.log(T['apt1']), T['pos']])
    Xpl_bruto = np.column_stack([T['perfil'], np.log(T['apt1']), T['pos']])
    Xalt = np.column_stack([X22, ab22_2 - X22[:, 4], ab26_2 - ab22_2, T['perfil'], np.log(T['apt2']), T['pos']])
    for nome, masc, fe, cl, _, letra in specs(T):
        m = masc & T['tem_perfil']
        r = {'letra': letra, 'efeito_fixo': fe, 'secoes_na_amostra': int(masc.sum()), 'sem_perfil': int((masc & ~T['tem_perfil']).sum()), 'janelas': {}}
        if m.sum() < 60:
            res[nome] = r; continue
        idx = np.where(m)[0]
        fe_v, cl_v, w = T[fe][idx], T[cl][idx], V[idx]
        # modelo conjunto
        Fx2 = T['faixas']['2'][idx][:, 1:]; Fx1 = T['faixas']['1'][idx][:, 1:]
        try:
            MJ = Modelo(np.column_stack([Fx2, Fx1, XB[idx]]), fe_v, cl_v, w, jack=False)
        except ValueError:
            res[nome] = r; continue
        fj = MJ.fit(y[idx], cv3=False)
        r['n'] = MJ.n; r['grupos_do_efeito_fixo'] = MJ.G; r['municipios'] = MJ.C
        r['modelo_conjunto'] = {'faixas': ['9h', '10h', '11h', '12h', '13h', '14h', '15h', '16h em diante'], 'referencia': 'antes das 9h',
                                'c': fj['b'][:8].tolist(), 'ep': fj['ep'][:8].tolist()}
        cj = np.concatenate([[0.0], fj['b'][:8]])  # c_8 = 0, c_9 ... c_16
        # janelas falsas
        falsas = {}
        for h in range(9, 16):
            Mf = Modelo(np.column_stack([T['quebr'][h][idx], Fx2, Fx1, XB[idx]]), fe_v, cl_v, w, jack=False)
            ff = Mf.fit(y[idx], cv3=False)
            falsas[f'{h}h37'] = {'salto': float(ff['b'][0]), 'ep': float(ff['ep'][0]), 'z': float(ff['b'][0] / ff['ep'][0])}
        r['janelas_falsas'] = falsas
        mods = {}
        for h in JANELAS:
            D = T['fB'][('2', h)][idx]; D1 = T['fB'][('1', h)][idx]
            M = Modelo(np.column_stack([D, D1, XB[idx]]), fe_v, cl_v, w, jack=False)
            mods[h] = M
            f = M.fit(y[idx], cv3=False)
            b, ep = float(f['b'][0]), float(f['ep'][0])
            ph = phi(b, F[h]['F_V']); eph = phi(ep, F[h]['F_V'])
            degrau = float(cj[h - 8] - cj[h - 9])
            j = {'b': b, 'ep': ep, 'z': b / ep, 'Phi': ph, 'Phi_ep': eph, 'Phi_ic99': [ph - 2.576 * eph, ph + 2.576 * eph],
                 'F_nacional': F[h]['F_V'], 'b_que_zera_a_margem': 1.785 / F[h]['F_V'], 'votos_de_margem': ph * MARGEM,
                 'coef_do_controle_D1': float(f['b'][1]), 'ep_do_controle_D1': float(f['ep'][1]),
                 'dp_da_dose_dentro_do_grupo': float(np.sqrt(np.average(M.Xd[:, 0] ** 2, weights=M.w))),
                 'degrau_no_conjunto': degrau, 'degrau_cumpre': bool(b > 0 and degrau >= b / 2)}
            # placebo de 1º turno
            mp = m & T['tem22'] & (V1 >= 30)
            ip = np.where(mp)[0]
            try:
                Mp = Modelo(np.column_stack([T['fB'][('1', h)][ip], Xpl[ip]]), T[fe][ip], T[cl][ip], V1[ip], jack=False)
                fp = Mp.fit(y1[ip], cv3=False)
                Mb = Modelo(np.column_stack([T['fB'][('1', h)][ip], Xpl_bruto[ip]]), T[fe][ip], T[cl][ip], V1[ip], jack=False)
                fb = Mb.fit(y1[ip], cv3=False)
                bp, epp = float(fp['b'][0]), float(fp['ep'][0])
                j['placebo_1t'] = {'b': bp, 'ep': epp, 'z': bp / epp, 'n': Mp.n, 'no_maximo_um_terco': bool(abs(bp) <= abs(b) / 3),
                                   'igual_ao_principal': bool(abs(b - bp) < 2 * math.hypot(ep, epp)),
                                   'bruto_2026_sem_controle_de_2022': {'b': float(fb['b'][0]), 'ep': float(fb['ep'][0])}}
            except ValueError:
                j['placebo_1t'] = None
            # secundários
            fbn = M.fit(ybn[idx], cv3=False)
            j['y_BN'] = {'b': float(fbn['b'][0]), 'ep': float(fbn['ep'][0]), 'z': float(fbn['b'][0] / fbn['ep'][0]),
                         'votos_convertidos_se_fosse_efeito': float(fbn['b'][0] / 100 * F[h]['F_comp'] * 128236074)}
            ia = np.where(m & T['tem22'])[0]
            try:
                Ma = Modelo(np.column_stack([T['fB'][('2', h)][ia], Xalt[ia]]), T[fe][ia], T[cl][ia], V[ia], jack=False)
                fa = Ma.fit((y - fat2_22)[ia], cv3=False)
                j['y_alt'] = {'b': float(fa['b'][0]), 'ep': float(fa['ep'][0]), 'z': float(fa['b'][0] / fa['ep'][0]), 'n': Ma.n,
                              'Phi': phi(float(fa['b'][0]), F[h]['F_V'])}
            except ValueError:
                j['y_alt'] = None
            # regiões
            reg = {}
            for rg in ('N', 'NE', 'SE', 'S', 'CO'):
                ir = idx[T['reg'][idx] == rg]
                try:
                    Mr = Modelo(np.column_stack([T['fB'][('2', h)][ir], T['fB'][('1', h)][ir], XB[ir]]), T[fe][ir], T[cl][ir], V[ir], jack=False)
                    if Mr.n - Mr.G - Mr.k < 20: raise ValueError
                    fr = Mr.fit(y[ir], cv3=False)
                    reg[rg] = {'b': float(fr['b'][0]), 'ep': float(fr['ep'][0]), 'n': Mr.n}
                except ValueError:
                    reg[rg] = None
            j['regioes'] = reg
            r['janelas'][f'{h}h'] = j
        # calibração
        if True:  # calibração em todas as especificações
            cal = {}
            R2 = T['R2'][idx]; L2 = T['L2'][idx]; Vi = V[idx]
            for h in JANELAS:
                M = mods[h]; D = T['fB'][('2', h)][idx]; D1 = T['fB'][('1', h)][idx]
                bobs = r['janelas'][f'{h}h']['b']; phobs = r['janelas'][f'{h}h']['Phi']
                ch = {}
                for nomep, PhiP, taxa, origem in (
                        [(f'Phi_{p}', p, np.minimum(1.0, p * 2215095.5 / (F[h]['F_R'] * R2_NAC) * D), 'R') for p in (0.25, 0.5, 1.0)] +
                        [(f'espelho_Phi_-{p}', -p, np.minimum(1.0, p * 2215095.5 / (F[h]['F_L'] * L2_NAC) * D), 'L') for p in (0.5, 1.0)] +
                        [('inocente_I1_rampa', 0.5, None, 'R'), ('inocente_I2_composicao', 0.5, None, 'R')]):
                    if taxa is None:
                        base_t = T['rampa'][idx] if 'I1' in nomep else D1
                        alvo = (np.minimum(1.0, 0.5 * 2215095.5 / (F[h]['F_R'] * R2_NAC) * D) * R2).sum()
                        taxa = np.minimum(1.0, base_t * alvo / max((base_t * R2).sum(), 1e-9))
                    bs, zs, phs, dg, full = [], [], [], [], 0
                    for _ in range(200):
                        if origem == 'R':
                            mv = rng.binomial(R2.astype(int), taxa); yy = y[idx] + 100 * mv / Vi
                        else:
                            mv = rng.binomial(L2.astype(int), taxa); yy = y[idx] - 100 * mv / Vi
                        f = M.fit(yy, cv3=False); b = f['b'][0]; ep = f['ep'][0]
                        cjj = np.concatenate([[0.0], MJ.fit(yy, cv3=False)['b'][:8]])
                        d_ok = b > 0 and (cjj[h - 8] - cjj[h - 9]) >= b / 2
                        ph = phi(b, F[h]['F_V'])
                        pl = r['janelas'][f'{h}h']['placebo_1t']
                        pl_ok = pl is not None and abs(pl['b']) <= abs(b) / 3
                        bs.append(b); zs.append(b / ep); phs.append(ph); dg.append(d_ok)
                        full += bool(ph >= 0.5 and b / ep >= 3.9 and d_ok and pl_ok)
                    bs, zs, phs = np.array(bs), np.array(zs), np.array(phs)
                    sinal = 1 if PhiP > 0 else -1
                    ch[nomep] = {'Phi_plantado': PhiP, 'votos_movidos_esperados_na_amostra': float((taxa * (R2 if origem == 'R' else L2)).sum()),
                                 'taxa_media_f': float(np.average(taxa, weights=(R2 if origem == 'R' else L2))),
                                 'Phi_medio': float(phs.mean()), 'recuperacao': float((phs.mean() - phobs) / PhiP),
                                 'z_medio': float(zs.mean()),
                                 'enxerga': float(np.mean((sinal * zs >= 3.9) & (sinal * phs >= abs(PhiP) / 2))),
                                 'z_3,9_ou_mais': float(np.mean(sinal * zs >= 3.9)),
                                 'degrau_cumprido': float(np.mean(dg)), 'criterio_inteiro_de_sinal': full / 200}
                cal[f'{h}h'] = ch
            r['calibracao'] = cal
        res[nome] = r
        grava('parcial_parteA.json', res)
        diz('parte A', nome, 'n', r.get('n'))
    return res


def veredito_a(r, nome):
    """Veredito por janela e da parte, pela regra D10."""
    out = {}
    for h in JANELAS:
        j = r['janelas'].get(f'{h}h')
        if j is None:
            out[f'{h}h'] = 'SEM PODER'; continue
        cal = r.get('calibracao', {}).get(f'{h}h')
        ve = cal['Phi_1.0']['enxerga'] if cal else None
        rec = cal['Phi_0.5']['recuperacao'] if cal else None
        pl = j.get('placebo_1t')
        if ve is not None and ve < 0.95:
            v = 'SEM PODER'
        elif j['Phi'] >= 0.5 and j['z'] >= 3.9 and j['degrau_cumpre'] and pl is not None and pl['no_maximo_um_terco']:
            v = 'SINAL'
        elif j['Phi_ic99'][0] >= -0.5 and j['Phi_ic99'][1] <= 0.5 and rec is not None and 0.8 <= rec <= 1.2 and not (nome.startswith('ANT') and h in (10, 12)):
            v = 'SEM SINAL'
        else:
            v = 'INCONCLUSIVO'
        out[f'{h}h'] = v
    vs = list(out.values())
    if 'SINAL' in vs: p = 'SINAL'
    elif all(v == 'SEM SINAL' for v in vs): p = 'SEM SINAL'
    elif 'SEM PODER' in vs: p = 'SEM PODER'
    else: p = 'INCONCLUSIVO'
    out['parte'] = p
    out['espelho_a_favor_de_flavio'] = [f'{h}h' for h in JANELAS if r['janelas'].get(f'{h}h') and r['janelas'][f'{h}h']['Phi'] <= -0.5 and r['janelas'][f'{h}h']['z'] <= -3.9]
    return out


# ============================== PARTE B (T30) ==============================
def parte_b(T, F, rng, so=None):
    res = {}
    V = T['L2'] + T['R2']; V1 = T['L1'] + T['R1']
    fat1 = 100 * T['L1'] / V1; fat2 = 100 * T['L2'] / V
    y = fat2 - fat1; rho = T['R1'] / V1; lam = 1 - rho
    dcomp = 100 * (T['comp2'] - T['comp1']) / T['apt2']
    for nome, masc, fe, _, cl, letra in specs(T):
        if so and nome not in so:
            continue
        idx = np.where(masc)[0]
        fe_v, cl_v, w = T[fe][idx], T[cl][idx], V[idx]
        aninhado = fe != 'uf'
        r = {'letra': letra, 'efeito_fixo': fe, 'grupo_do_cv3': cl, 'cortes': {}}
        mods = {}; mods_pl = {}; mods_esp = {}
        try:
            for rel, fx in (('brasilia', T['fB']), ('urna', T['fU'])):
                for h in CORTES:
                    f2 = fx[('2', h)][idx]; f1 = fx[('1', h)][idx]
                    X = np.column_stack([f2 * rho[idx], f1, dcomp[idx], fat1[idx]])
                    Xp = np.column_stack([f1 * rho[idx], f1, dcomp[idx], fat1[idx]])
                    Xe = np.column_stack([f2 * lam[idx], f1, dcomp[idx], fat1[idx]])
                    mods[(rel, h)] = (Modelo(X, fe_v, cl_v, w), X); mods_pl[(rel, h)] = (Modelo(Xp, fe_v, cl_v, w), Xp)
                    mods_esp[(rel, h)] = (Modelo(Xe, fe_v, cl_v, w), Xe)
        except ValueError:
            res[nome] = r; continue

        def ajusta(par, yy, exato=False):
            M, X = par
            f = M.fit(yy)
            b = float(f['b'][0]); cr1 = float(f['ep'][0])
            if 'ep_cv3' in f: cv3 = float(f['ep_cv3'][0])
            elif exato: cv3 = jack_exato(X, fe_v, cl_v, w, yy)
            else: cv3 = cr1
            return b, cr1, cv3

        M0 = mods[('brasilia', 12)][0]
        r['n'] = M0.n; r['grupos_do_efeito_fixo'] = M0.G; r['grupos_do_cv3'] = M0.C
        obs = {}
        for key in mods:
            rel, h = key
            b, cr1, cv3 = ajusta(mods[key], y[idx], exato=True)
            bp, cr1p, cv3p = ajusta(mods_pl[key], y[idx], exato=True)
            be, cr1e, cv3e = ajusta(mods_esp[key], y[idx], exato=True)
            f2 = (T['fB'] if rel == 'brasilia' else T['fU'])[('2', h)][idx]; f1 = (T['fB'] if rel == 'brasilia' else T['fU'])[('1', h)][idx]
            o = {'inclinacao': b, 'ep_cv3': cv3, 'z_cv3': b / cv3 if cv3 > 0 else float('nan'), 'ep_cr1': cr1,
                 'f2_medio': float(np.average(f2, weights=w)), 'f1_medio': float(np.average(f1, weights=w)),
                 'dp_do_regressor_dentro_do_grupo': float(np.sqrt(np.average(mods[key][0].Xd[:, 0] ** 2, weights=mods[key][0].w))),
                 'placebo_virada': {'inclinacao': bp, 'ep_cv3': cv3p, 'z_cv3': bp / cv3p if cv3p > 0 else float('nan'), 'abaixo_de_2_ep': bool(abs(bp) < 2 * cv3p)},
                 'espelho': {'inclinacao': be, 'ep_cv3': cv3e, 'z_cv3': be / cv3e if cv3e > 0 else float('nan'),
                             'sinal_espelhado_valor_e_z': bool(be <= -4 and be / cv3e < -3.2)},
                 'emd_2,8_ep': 2.8 * cv3}
            # ao lado: CV3 e CR1 por município (quando o grupo da letra é o local), troca completa de papéis, versão com f2 sozinho, Adendo 12
            try:
                if fe == 'loc':
                    Mm = Modelo(mods[key][1], fe_v, T['mun'][idx], w); fm = Mm.fit(y[idx])
                    o['ao_lado_agrupado_por_municipio'] = {'ep_cr1': float(fm['ep'][0]), 'ep_cv3': float(fm['ep_cv3'][0]) if 'ep_cv3' in fm else None}
                Xt = np.column_stack([f1 * rho[idx], f2, dcomp[idx], fat1[idx]]); ft = Modelo(Xt, fe_v, cl_v, w).fit(y[idx])
                o['ao_lado_placebo_troca_completa'] = {'inclinacao': float(ft['b'][0]), 'ep': float(ft.get('ep_cv3', ft['ep'])[0])}
                Xf = np.column_stack([f2 * rho[idx], f2, f1 * rho[idx], f1, dcomp[idx], fat1[idx]]); ff = Modelo(Xf, fe_v, cl_v, w).fit(y[idx])
                o['ao_lado_com_f2_sozinho'] = {'inclinacao': float(ff['b'][0]), 'ep': float(ff.get('ep_cv3', ff['ep'])[0]),
                                               'coef_f2': float(ff['b'][1]), 'ep_f2': float(ff.get('ep_cv3', ff['ep'])[1])}
                Xa = np.column_stack([f2, f1, dcomp[idx], fat1[idx]]); fa = Modelo(Xa, fe_v, cl_v, w).fit(y[idx])
                o['ao_lado_adendo12_R2_regressor_f2'] = {'inclinacao': float(fa['b'][0]), 'ep': float(fa.get('ep_cv3', fa['ep'])[0])}
            except ValueError:
                pass
            obs[key] = o
        # calibração
        fazer_cal = True
        R2 = T['R2'][idx].astype(int); L2 = T['L2'][idx].astype(int); Vi = V[idx]
        if fazer_cal:
            for key in mods:
                rel, h = key
                fx = T['fB'] if rel == 'brasilia' else T['fU']
                f2 = fx[('2', h)][idx]
                cal = {}
                viz = [(rel, hh) for hh in CORTES]
                for q in (0.05, 0.10, 0.15):
                    bsv, passa, inteiro = [], 0, 0
                    for _ in range(200):
                        mv = rng.binomial(R2, np.minimum(1.0, q * f2)); yy = y[idx] + 100 * mv / Vi
                        fits = {kk: ajusta(mods[kk], yy) for kk in viz}
                        b, _, cv3 = fits[key]; bsv.append(b)
                        ok = b >= 4 and b / cv3 > 3.2
                        passa += ok
                        if ok:
                            bp, _, cv3p = ajusta(mods_pl[key], yy)
                            inteiro += bool(abs(bp) < 2 * cv3p and dose_crescente({hh: fits[(rel, hh)][0] for hh in CORTES}, h))
                    bsv = np.array(bsv)
                    cal[f'q_{int(q * 100)}%'] = {'inclinacao_media': float(bsv.mean()), 'inclinacao_que_a_troca_produz': float(bsv.mean() - obs[key]['inclinacao']),
                                                 'dp_entre_copias': float(bsv.std()), 'poder_valor_e_z': passa / 200, 'poder_criterio_inteiro': inteiro / 200}
                por_q = np.mean([cal[f'q_{int(q * 100)}%']['inclinacao_que_a_troca_produz'] / q for q in (0.05, 0.10, 0.15)])
                FR = F[h]['F_R'] if rel == 'brasilia' else F[h]['F_R_relogio_da_urna']
                o = obs[key]
                o['calibracao'] = cal
                o['inclinacao_por_unidade_de_q'] = float(por_q)
                o['emd_em_q'] = float(o['emd_2,8_ep'] / por_q) if por_q > 0 else None
                o['emd_em_fracao_da_margem'] = float(2 * o['emd_em_q'] * FR * R2_NAC / MARGEM) if por_q > 0 else None
                o['q_implicado'] = float(o['inclinacao'] / por_q) if por_q > 0 else None
                o['votos_de_margem_implicados'] = float(2 * o['q_implicado'] * FR * R2_NAC) if por_q > 0 else None
                o['fracao_nacional_dos_votos_de_flavio_depois_do_corte'] = FR
            # espelho plantado e inocentes
            esp = {}
            for key in [('brasilia', 12), ('brasilia', 14), ('brasilia', 16)]:
                f2 = T['fB'][('2', key[1])][idx]; passa = 0; bsv = []
                for _ in range(200):
                    mv = rng.binomial(L2, np.minimum(1.0, 0.10 * f2)); yy = y[idx] - 100 * mv / Vi
                    b, _, cv3 = ajusta(mods_esp[key], yy); bsv.append(b); passa += bool(b <= -4 and b / cv3 < -3.2)
                esp[f'{key[1]}h'] = {'inclinacao_media_do_espelho': float(np.mean(bsv)), 'observado': obs[key]['espelho']['inclinacao'], 'visto': passa / 200}
            r['espelho_plantado_10%'] = esp
            ino = {}
            alvo = (np.minimum(1.0, 0.10 * T['fB'][('2', 14)][idx]) * R2).sum()
            for nomei, base_t in (('I1_rampa_suave_no_2t', T['rampa'][idx]), ('I2_composicao_perfil_do_1t', T['fB'][('1', 14)][idx])):
                taxa = np.minimum(1.0, base_t * alvo / (base_t * R2).sum())
                n_vz = collections.Counter(); n_int = collections.Counter(); algum_vz = 0; algum_int = 0; bm = collections.defaultdict(list); plm = collections.defaultdict(list)
                for _ in range(200):
                    mv = rng.binomial(R2, taxa); yy = y[idx] + 100 * mv / Vi
                    fits = {kk: ajusta(mods[kk], yy) for kk in mods}
                    a_vz = a_int = False
                    for kk, (b, _, cv3) in fits.items():
                        bm[kk].append(b)
                        if b >= 4 and b / cv3 > 3.2:
                            n_vz[kk] += 1; a_vz = True
                            bp, _, cv3p = ajusta(mods_pl[kk], yy)
                            plm[kk].append(abs(bp) / cv3p)
                            if abs(bp) < 2 * cv3p and dose_crescente({hh: fits[(kk[0], hh)][0] for hh in CORTES}, kk[1]):
                                n_int[kk] += 1; a_int = True
                    algum_vz += a_vz; algum_int += a_int
                ino[nomei] = {'votos_movidos_esperados_na_amostra': float((taxa * R2).sum()),
                              'copias_com_algum_corte_em_valor_e_z': algum_vz / 200, 'copias_com_algum_SINAL_inteiro': algum_int / 200,
                              'por_corte': {f'{kk[0]}_{kk[1]}h': {'inclinacao_media': float(np.mean(bm[kk])), 'valor_e_z': n_vz[kk] / 200, 'sinal_inteiro': n_int[kk] / 200,
                                                                    'placebo_em_ep_quando_passa': float(np.mean(plm[kk])) if plm[kk] else None} for kk in mods}}
            r['inocentes_plantados'] = ino
            r['observado_cortes_que_passam_valor_e_z'] = [f'{kk[0]}_{kk[1]}h' for kk, o in obs.items() if o['inclinacao'] >= 4 and o['z_cv3'] > 3.2]
        # vereditos por corte
        for key in mods:
            rel, h = key; o = obs[key]
            passa = o['inclinacao'] >= 4 and o['z_cv3'] > 3.2
            dc = dose_crescente({hh: obs[(rel, hh)]['inclinacao'] for hh in CORTES}, h)
            dc2 = dose_frouxa({hh: obs[(rel, hh)]['z_cv3'] for hh in CORTES}, h)
            o['passa_valor_e_z'] = bool(passa); o['dose_crescente_3_horas'] = bool(dc); o['dose_leitura_frouxa'] = bool(dc2)
            if passa and dc and o['placebo_virada']['abaixo_de_2_ep']:
                v = 'SINAL'
            elif abs(o['inclinacao']) < 1.5 and 'calibracao' in o and o['emd_2,8_ep'] < o['calibracao']['q_5%']['inclinacao_que_a_troca_produz']:
                v = 'SEM SINAL'
            else:
                v = 'SEM PODER'
            o['veredito'] = v
            o['intermediario'] = bool(v == 'SEM PODER' and 1.5 <= abs(o['inclinacao']) and abs(o['z_cv3']) >= 2)
            r['cortes'][f'{rel}_{h}h'] = o
        vs = [o['veredito'] for o in r['cortes'].values()]
        r['veredito_da_parte'] = 'SINAL' if 'SINAL' in vs else ('SEM SINAL' if all(v == 'SEM SINAL' for v in vs) else 'SEM PODER')
        r['contagem_de_vereditos'] = dict(collections.Counter(vs))
        r['espelho_cortes_com_sinal_a_favor_de_flavio'] = [k for k, o in r['cortes'].items() if o['espelho']['sinal_espelhado_valor_e_z']]
        res[nome] = r
        grava('parcial_parteB.json', res)
        diz('parte B', nome, 'n', r.get('n'), r['contagem_de_vereditos'])
    return res


def dose_crescente(bs, h):
    """Sequência de 3 cortes seguidos contendo h, inclinação positiva nos três e não decrescente."""
    for ini in (h - 2, h - 1, h):
        tr = [ini, ini + 1, ini + 2]
        if all(t in bs for t in tr) and bs[tr[0]] > 0 and bs[tr[0]] <= bs[tr[1]] <= bs[tr[2]]:
            return True
    return False


def dose_frouxa(zs, h):
    for ini in (h - 2, h - 1, h):
        tr = [ini, ini + 1, ini + 2]
        if all(t in zs for t in tr) and all(zs[t] >= 2 for t in tr):
            return True
    return False


def relogios(T):
    """T7: seções fora do relógio de Brasília, os dois relógios por corte, efeito fixo de município."""
    V = T['L2'] + T['R2']; V1 = T['L1'] + T['R1']
    fat1 = 100 * T['L1'] / V1; y = 100 * T['L2'] / V - fat1; rho = T['R1'] / V1
    dcomp = 100 * (T['comp2'] - T['comp1']) / T['apt2']
    idx = np.where(T['desloc'] != 0)[0]
    out = {'secoes': int(len(idx)), 'por_uf': dict(collections.Counter(T['uf'][idx].tolist())), 'cortes': {}}
    for rel, fx in (('brasilia', T['fB']), ('urna', T['fU'])):
        for h in CORTES:
            f2 = fx[('2', h)][idx]; f1 = fx[('1', h)][idx]
            try:
                M = Modelo(np.column_stack([f2 * rho[idx], f1, dcomp[idx], fat1[idx]]), T['mun'][idx], T['mun'][idx], V[idx])
                f = M.fit(y[idx])
                out['cortes'][f'{rel}_{h}h'] = {'inclinacao': float(f['b'][0]), 'ep_cv3': float(f['ep_cv3'][0]), 'z_cv3': float(f['b'][0] / f['ep_cv3'][0]), 'n': M.n, 'municipios': M.G}
            except (ValueError, KeyError):
                out['cortes'][f'{rel}_{h}h'] = None
    return out


# ============================== PARTE 2 ==============================
def parte2(P, aas, meta, rng):
    Pu = [p for p in P if p['em_univP']]
    n = len(Pu)
    out = {'amostra_P_lida': len(P), 'amostra_P_no_universo_refeito': n, 'universo_P': N_P, 'universo_P_refeito_com_a_base': meta['universo_P_refeito']}

    def tot(vals, N):
        v = np.array(vals, float); nn = len(v)
        return float(N * v.mean()), float(N * v.std(ddof=1) / math.sqrt(nn) * math.sqrt(max(0.0, 1 - nn / N)))

    resto = [a for a in aas if not a['ext'] and not a['em_univP']]
    N_resto = meta['secoes_brasil_2t'] - meta['universo_P_refeito']
    out['aas_fora_de_P'] = len(resto); out['N_resto'] = N_resto
    out['aas_dentro_do_universo_P'] = sum(1 for a in aas if not a['ext'] and a['em_univP'])
    for nome, cp, ca in (('17h', 't17_2', 't17_2'), ('18h', 't18_2', 't18_2'), ('19h', 't19_2', 't19_2')):
        tp, ep_p = tot([p[cp] for p in Pu], N_P); tr, ep_r = tot([a[ca] for a in resto], N_resto)
        T = tp + tr; ep = math.hypot(ep_p, ep_r)
        out[f'votos_a_partir_das_{nome}'] = {'T_P': tp, 'ep_P': ep_p, 'T_resto': tr, 'ep_resto': ep_r, 'T': T, 'ep': ep,
                                             'dobro_de_T': 2 * T, 'dobro_lim_sup_95': 2 * (T + 1.645 * ep), 'dobro_lim_sup_99': 2 * (T + 2.326 * ep),
                                             'fracao_da_margem': 2 * T / MARGEM, 'secoes_P_com_algum': int(sum(1 for p in Pu if p[cp] > 0)),
                                             'secoes_resto_com_algum': int(sum(1 for a in resto if a[ca] > 0)),
                                             'maximo_por_secao_em_P': int(max(p[cp] for p in Pu))}
    t = out['votos_a_partir_das_17h']
    out['criterio'] = {'limiar': 443019, 'dobro_de_T': t['dobro_de_T'], 'relevante': bool(t['dobro_de_T'] > 443019),
                       'lim_sup_99_abaixo_do_limiar': bool(t['dobro_lim_sup_99'] < 443019)}
    out['veredito'] = ('JANELA RELEVANTE: baixar o log das prorrogadas todas' if t['dobro_de_T'] > 443019 else
                       'SEM SINAL: a prorrogação não alcança 10% da margem mesmo que todos os votos dela fossem irregulares')
    # espelho: 1º turno
    p1 = [p['t17_1'] for p in Pu if p['t17_1'] is not None]; r1 = [a['t17_1'] for a in resto if a['t17_1'] is not None]
    tp, ep_p = tot(p1, N_P); tr, ep_r = tot(r1, N_resto)
    out['espelho_1t_votos_a_partir_das_17h'] = {'T_P': tp, 'ep_P': ep_p, 'T_resto': tr, 'ep_resto': ep_r, 'T': tp + tr, 'ep': math.hypot(ep_p, ep_r), 'n_P': len(p1), 'n_resto': len(r1)}
    # calibração: 33 votos sintéticos por seção de P
    lam = 221510 / N_P; rec = []
    for _ in range(200):
        v = np.array([p['t17_2'] for p in Pu]) + rng.poisson(lam, n)
        rec.append(N_P * v.mean() + t['T_resto'])
    rec = np.array(rec)
    out['calibracao_plantio_221510'] = {'media_por_secao': lam, 'T_medio_devolvido': float(rec.mean()), 'T_observado': t['T'],
                                        'acrescimo_devolvido': float(rec.mean() - t['T']), 'copias_que_acusam': float(np.mean(2 * rec > 443019))}
    out['comparecimento_medio_P'] = float(np.mean([p['comp2'] for p in Pu]))
    out['fracao_dos_votos_de_P_a_partir_das_17h'] = float(sum(p['t17_2'] for p in Pu) / sum(p['n2'] for p in Pu))
    out['ultimo_voto_mais_tardio_em_P_hora_de_brasilia'] = max(p['ultimo_2'] for p in Pu)
    return out


def bruto(T):
    """Tabela bruta de 2026 por quintil de D_12 e D_15 na AAS (sem modelo)."""
    a = np.where(T['aas'])[0]; V = T['L2'] + T['R2']; V1 = T['L1'] + T['R1']; out = {}
    for h in (12, 15):
        D = T['fB'][('2', h)][a]; q = np.quantile(D, [0.2, 0.4, 0.6, 0.8]); g = np.searchsorted(q, D)
        tb = []
        for i in range(5):
            m = a[g == i]
            tb.append({'quintil': i + 1, 'n': int(len(m)), 'D_medio': float(T['fB'][('2', h)][m].mean()), 'D_1t_medio': float(T['fB'][('1', h)][m].mean()),
                       'lula_1t_dois_candidatos': float(100 * T['L1'][m].sum() / V1[m].sum()), 'lula_2t': float(100 * T['L2'][m].sum() / V[m].sum()),
                       'virada': float(100 * T['L2'][m].sum() / V[m].sum() - 100 * T['L1'][m].sum() / V1[m].sum())})
        out[f'D_{h}h'] = tb
    return out


def placebo_gov(T, B):
    """D7: governador do 2º turno nas 6 UFs como desfecho (ao lado, não decide)."""
    G2 = carregar(GOV2); G1 = carregar(REPO + '/dados/candidatos_gov_2026_1t_6ufs.json.gz')['secoes']
    ufs = ('AC', 'AM', 'DF', 'ES', 'RN', 'TO'); lado = {}
    for uf in ufs:
        tot = collections.Counter()
        ks = [k for k in G2 if k.startswith(uf + '|')]
        for k in ks:
            for num, q in G2[k].items():
                if num not in ('B', 'N'): tot[num] += q
        (a, _), (b, _) = tot.most_common(2)
        sa, yy, ww = [], [], []
        for k in ks:
            s2 = B.get(k, {}).get('2'); ga, gb = G2[k].get(a, 0), G2[k].get(b, 0)
            if not s2 or s2['L'] + s2['R'] < 30 or ga + gb < 30: continue
            sa.append(ga / (ga + gb)); yy.append(s2['L'] / (s2['L'] + s2['R'])); ww.append(s2['L'] + s2['R'])
        sa, yy, ww = np.array(sa), np.array(yy), np.array(ww, float)
        ma, my = np.average(sa, weights=ww), np.average(yy, weights=ww)
        cor = np.average((sa - ma) * (yy - my), weights=ww) / math.sqrt(np.average((sa - ma) ** 2, weights=ww) * np.average((yy - my) ** 2, weights=ww))
        lado[uf] = {'lado_de_lula': a if cor > 0 else b, 'outro': b if cor > 0 else a, 'correlacao_do_primeiro_com_y': float(cor), 'secoes_da_uf': len(sa)}
    n = T['n']; yg = np.full(n, np.nan); wg = np.zeros(n); XU = np.zeros((n, 12))
    for i, k in enumerate(T['k']):
        uf = T['uf'][i]
        if uf not in lado or k not in G2: continue
        a, b = lado[uf]['lado_de_lula'], lado[uf]['outro']
        ga, gb = G2[k].get(a, 0), G2[k].get(b, 0)
        if ga + gb < 30: continue
        yg[i] = 100 * ga / (ga + gb); wg[i] = ga + gb
        j = ufs.index(uf); g1 = G1.get(k, {})
        XU[i, 2 * j] = g1.get(a, 0) / T['comp1'][i]; XU[i, 2 * j + 1] = g1.get(b, 0) / T['comp1'][i]
    V1 = T['L1'] + T['R1']; fat1 = 100 * T['L1'] / V1
    dab = (1 - T['comp2'] / T['apt2']) - (1 - T['comp1'] / T['apt1'])
    out = {'lado': lado, 'specs': {}}
    tem = ~np.isnan(yg)
    for nome, masc, fe in (('ANT_local', T['ant'], 'loc'), ('UNI_local', np.ones(n, bool), 'loc'), ('UNI_municipio', np.ones(n, bool), 'mun')):
        idx = np.where(masc & tem)[0]; r = {'secoes': int(len(idx)), 'janelas': {}}
        for h in JANELAS:
            try:
                X = np.column_stack([T['fB'][('2', h)][idx], T['fB'][('1', h)][idx], XU[idx], dab[idx], fat1[idx]])
                X = X[:, [0, 1] + [c for c in range(2, X.shape[1]) if X[:, c].std() > 0]]
                M = Modelo(X, T[fe][idx], T['mun'][idx], wg[idx], jack=False)
                if M.n - M.G - M.k < 20: raise ValueError
                ff = M.fit(yg[idx], cv3=False)
                r['janelas'][f'{h}h'] = {'b': float(ff['b'][0]), 'ep': float(ff['ep'][0]), 'z': float(ff['b'][0] / ff['ep'][0]), 'n': M.n, 'grupos': M.G}
            except ValueError:
                r['janelas'][f'{h}h'] = None
        out['specs'][nome] = r
    return out


def cortes_em_P(B, fuso):
    """R3: cortes de 16h e 17h (Brasília) da Parte B na amostra P, efeito fixo de município."""
    V = carregar(TRAB + '/votos_hora.json.gz'); rows = []
    for kk, o in V.items():
        fonte, k = kk.split(':', 1)
        if fonte != 'c1p' or 'erro' in o or not (o['1'] and o['2'] and o['1']['t'] and o['2']['t']) or k.startswith('ZZ'): continue
        b = B.get(k)
        if not b or '1' not in b or '2' not in b: continue
        a1, a2 = b['1'], b['2']
        if a2['L'] + a2['R'] < 30 or a1['L'] + a1['R'] <= 0: continue
        m = '|'.join(k.split('|')[:2]); ds = fuso[m] * 3600
        t1 = np.array(o['1']['t']) + ds; t2 = np.array(o['2']['t']) + ds
        rows.append((m, a1, a2, {h: (float(np.mean(t1 >= h * 3600)), float(np.mean(t2 >= h * 3600))) for h in (15, 16, 17)}))
    mun = np.array([r[0] for r in rows])
    L1 = np.array([r[1]['L'] for r in rows], float); R1 = np.array([r[1]['R'] for r in rows], float)
    L2 = np.array([r[2]['L'] for r in rows], float); R2 = np.array([r[2]['R'] for r in rows], float)
    fat1 = 100 * L1 / (L1 + R1); y = 100 * L2 / (L2 + R2) - fat1; rho = R1 / (L1 + R1)
    dcomp = np.array([100 * (r[2]['comp'] - r[1]['comp']) / r[2]['apt'] for r in rows])
    out = {'secoes': len(rows), 'cortes': {}}
    rng = np.random.default_rng(SEMENTE + 1)
    for h in (15, 16, 17):
        f1 = np.array([r[3][h][0] for r in rows]); f2 = np.array([r[3][h][1] for r in rows])
        try:
            M = Modelo(np.column_stack([f2 * rho, f1, dcomp, fat1]), mun, mun, L2 + R2)
            ff = M.fit(y); b, cv3 = float(ff['b'][0]), float(ff['ep_cv3'][0])
            cal = {}
            for q in (0.05, 0.15):
                bs = []
                for _ in range(200):
                    mv = rng.binomial(R2.astype(int), np.minimum(1.0, q * f2)); bs.append(M.fit(y + 100 * mv / (L2 + R2))['b'][0])
                cal[f'q_{int(q * 100)}%'] = float(np.mean(bs) - b)
            out['cortes'][f'{h}h'] = {'inclinacao': b, 'ep_cv3': cv3, 'z_cv3': b / cv3 if cv3 > 0 else None, 'ep_cr1': float(ff['ep'][0]), 'n': M.n, 'municipios': M.G,
                                      'f2_medio': float(np.average(f2, weights=L2 + R2)), 'emd_2,8_ep': 2.8 * cv3, 'inclinacao_que_a_troca_produz': cal}
        except (ValueError, KeyError) as e:
            out['cortes'][f'{h}h'] = {'erro': repr(e)}
    return out



# ============================== EXPLORATÓRIO (escrito DEPOIS de ver a primeira rodada) ==============================
def _pb(T):
    V = T['L2'] + T['R2']; V1 = T['L1'] + T['R1']
    fat1 = 100 * T['L1'] / V1
    return V, fat1, 100 * T['L2'] / V - fat1, T['R1'] / V1, 100 * (T['comp2'] - T['comp1']) / T['apt2']


def exploratorio_dentro_e_entre(T):
    """Inclinação da Parte B DENTRO do local contra ENTRE locais do mesmo município (decomposição de Mundlak, efeito fixo
    de município, erro por município). Um gatilho na urna prevê a mesma inclinação nos dois níveis; composição do bairro
    prevê inclinação maior entre prédios do que dentro do prédio."""
    V, fat1, y, rho, dcomp = _pb(T); out = {}
    for nome, masc in (('ANT', T['ant']), ('UNI', np.ones(T['n'], bool))):
        idx0 = np.where(masc)[0]
        _, g = np.unique(T['loc'][idx0], return_inverse=True)
        idx = idx0[np.bincount(g)[g] >= 2]
        _, g = np.unique(T['loc'][idx], return_inverse=True); w = V[idx]; sw = np.bincount(g, weights=w)
        r = {'secoes': int(len(idx)), 'locais': int(g.max() + 1), 'cortes': {}}
        for h in CORTES:
            f2 = T['fB'][('2', h)][idx]; f1 = T['fB'][('1', h)][idx]
            cols = []
            for c in (f2 * rho[idx], f1, dcomp[idx], fat1[idx]):
                mu = (np.bincount(g, weights=w * c) / sw)[g]; cols += [c - mu, mu]
            try:
                M = Modelo(np.column_stack(cols), T['mun'][idx], T['mun'][idx], w, jack=False); ff = M.fit(y[idx], cv3=False)
            except ValueError:
                continue
            bd, be = float(ff['b'][0]), float(ff['b'][1]); Vb = ff['V']
            epd = float(math.sqrt(Vb[0, 0] + Vb[1, 1] - 2 * Vb[0, 1]))
            r['cortes'][f'{h}h'] = {'dentro_do_local': bd, 'ep_dentro': float(ff['ep'][0]), 'entre_locais': be, 'ep_entre': float(ff['ep'][1]),
                                    'entre_menos_dentro': be - bd, 'ep_da_diferenca': epd, 'z_da_diferenca': (be - bd) / epd if epd > 0 else None,
                                    'n': M.n, 'municipios': M.G}
        out[nome] = r
    return out


def exploratorio_controles(T):
    """Parte B com os controles que a letra do T30 não tem: frações do 1º turno dos eliminados (70, 14, 55, resto), brancos,
    nulos e abstenção (bloco E); e mais o perfil do eleitorado (bloco E+P)."""
    V, fat1, y, rho, dcomp = _pb(T); c1 = T['comp1']; out = {}
    rng = np.random.default_rng(SEMENTE + 2)
    E = np.column_stack([T['c70'] / c1, T['c14'] / c1, T['c55'] / c1, T['cresto'] / c1, T['B1'] / c1, T['N1'] / c1, 1 - c1 / T['apt1']])
    for nome, masc, fe, _, cl, _ in specs(T):
        idx = np.where(masc & T['tem_perfil'])[0]; r = {}
        for h in CORTES:
            f2 = T['fB'][('2', h)][idx]; f1 = T['fB'][('1', h)][idx]
            base = [f2 * rho[idx], f1, dcomp[idx], fat1[idx]]; o = {}
            for rot, extra in (('letra', []), ('com_E', [E[idx]]), ('com_E_e_perfil', [E[idx], T['perfil'][idx], np.log(T['apt2'][idx])[:, None]])):
                try:
                    X = np.column_stack(base + extra)
                    M = Modelo(X, T[fe][idx], T[cl][idx], V[idx]); ff = M.fit(y[idx])
                    ep = float(ff['ep_cv3'][0]) if 'ep_cv3' in ff else float(ff['ep'][0])
                    o[rot] = {'inclinacao': float(ff['b'][0]), 'ep': ep, 'z': float(ff['b'][0]) / ep if ep > 0 else None, 'erro': 'CV3' if 'ep_cv3' in ff else 'CR1 por município'}
                    if rot == 'com_E_e_perfil' and h in (10, 12, 14, 16):  # o modelo com mais controles ainda enxerga um gatilho plantado?
                        R2i = T['R2'][idx].astype(int); bs = []
                        for _ in range(50):
                            mv = rng.binomial(R2i, np.minimum(1.0, 0.05 * f2))
                            bs.append(M.fit(y[idx] + 100 * mv / V[idx], cv3=False)['b'][0])
                        o[rot]['troca_de_5%_plantada_produz'] = float(np.mean(bs) - ff['b'][0])
                except ValueError:
                    o[rot] = None
            r[f'{h}h'] = o
        out[nome] = r
    return out


def exploratorio_simetria(T):
    """y ~ a x f2 x rho1 + c x f2 x (1 - rho1) + f1 + dcomp + fat1. a = efeito do voto tardio onde só há voto de Flávio;
    c = onde só há voto de Lula. Troca de Flávio para Lula prevê a > 0 e c = 0; reversão simétrica prevê c < 0."""
    V, fat1, y, rho, dcomp = _pb(T); out = {}
    for nome, masc, fe, _, cl, _ in specs(T):
        idx = np.where(masc)[0]; r = {}
        for h in CORTES:
            f2 = T['fB'][('2', h)][idx]; f1 = T['fB'][('1', h)][idx]
            try:
                M = Modelo(np.column_stack([f2 * rho[idx], f2 * (1 - rho[idx]), f1, dcomp[idx], fat1[idx]]), T[fe][idx], T[cl][idx], V[idx]); ff = M.fit(y[idx])
                ep = ff['ep_cv3'] if 'ep_cv3' in ff else ff['ep']
                r[f'{h}h'] = {'a_onde_flavio': float(ff['b'][0]), 'ep_a': float(ep[0]), 'c_onde_lula': float(ff['b'][1]), 'ep_c': float(ep[1]),
                              'z_a': float(ff['b'][0] / ep[0]), 'z_c': float(ff['b'][1] / ep[1])}
            except ValueError:
                r[f'{h}h'] = None
        out[nome] = r
    return out


def exploratorio_ordem_rdv(n_max=400):
    """A lista do cargo presidente no RDV está ordenada? Só a ordem: tipos e número digitado, sem ligar a hora."""
    from ber import parse
    from decodificar import _int, _filhos
    arqs = sorted(glob.glob(RDV_DIRS[('aas', '2')] + '/*/*/*/*/*-rdv.dat'))[::7][:n_max]
    tipos_ordenados = 0; pares = 0; pares_nd = 0; lidos = 0; blocos_n = []; cands = []
    for fpath in arqs:
        try:
            top = parse(open(fpath, 'rb').read())[0][2]
            els = [n for n in top[2][2] if (n[0], n[1]) == (2, 1)][0][2]
            seq = None
            for el in els:
                for cargo in _filhos(_filhos(el)[1]):
                    hh = _filhos(cargo)
                    if _int(hh[0][2]) == 1:
                        seq = [(_int(_filhos(v)[0][2]), _filhos(v)[1][2].decode() if len(_filhos(v)) > 1 else '') for v in _filhos(hh[2])]
        except Exception:
            continue
        if not seq:
            continue
        lidos += 1
        tp = [t for t, _ in seq]
        tipos_ordenados += int(all(tp[i] <= tp[i + 1] for i in range(len(tp) - 1)))
        nom = [d for t, d in seq if t == 2]
        pares += len(nom) - 1; pares_nd += sum(1 for i in range(len(nom) - 1) if nom[i] <= nom[i + 1])
        blocos_n.append(1 + sum(1 for i in range(len(nom) - 1) if nom[i] != nom[i + 1])); cands.append(len(set(nom)))
    return {'rdv_lidos': lidos, 'listas_com_tipos_em_ordem_crescente': tipos_ordenados,
            'pares_vizinhos_nominais': pares, 'pares_com_numero_nao_decrescente': pares_nd,
            'blocos_de_numero_igual_por_lista_media': float(np.mean(blocos_n)) if blocos_n else None,
            'candidatos_distintos_por_lista_media': float(np.mean(cands)) if cands else None,
            'leitura': 'se os blocos por lista forem iguais ao número de candidatos distintos, a lista está agrupada por candidato e não guarda ordem de votação'}



# ============================== RELATÓRIO ==============================
def f(x, d=2):
    if x is None or (isinstance(x, float) and (math.isnan(x) or math.isinf(x))): return 'n/d'
    return f'{x:,.{d}f}'.replace(',', 'X').replace('.', ',').replace('X', '.')


def texto(R):
    L = []; a = L.append
    a('R27_C2: GATILHO POR HORÁRIO (D1.4 do desenho cego D1, com o reteste "T30" da equipe vermelha)')
    a('Registro: Adendo 27 (commit 2748895), Adendo 28 (938be19) e Adendo 30 (a7218fb), antes de rodar. Decisões que o registro não fixa:')
    a('docstring de scripts/analisar_R27_C2.py, gravado antes de qualquer conta com votos (R27_C2/docstring_antes_de_rodar.txt).')
    a('')
    a('VEREDITOS PELA LETRA')
    for k, v in R['vereditos'].items():
        a(f'  {k}: {v}')
    a('')
    m = R['meta']
    a('AMOSTRAS')
    a(f"  Antiga (não aleatória): {m['contagens'].get('ant_em_U')} seções com os dois dias no log e em U. Aleatória nova: {m['contagens'].get('aas_em_U')}. União: {m['n_uniao']} seções.")
    a(f"  Fuso por município (8 menos a hora modal de abertura). Seções fora do relógio de Brasília: antiga {sum(v for k, v in m['deslocamentos']['ant'].items() if str(k) != '0')}, aleatória {sum(v for k, v in m['deslocamentos']['aas'].items() if str(k) != '0')}.")
    Fn = R['fracao_nacional']
    a('  Fração nacional dos votos válidos do 2º turno da hora h em diante (Brasília), pela amostra aleatória: ' +
      '; '.join(f"{h}h {f(100 * Fn[str(h)]['F_V'], 1)}%" for h in CORTES))
    a('')
    p0 = R['parte0']['todos']
    a('PARTE 0, O RDV GUARDA A ORDEM DE VOTAÇÃO?')
    a(f"  Marcadores (nulo por suspensão de presidente, tipo 6 no RDV): {p0['marcadores']}. Correlação de postos entre posição no RDV e ordem de votação: {f(p0['spearman'], 3)} (erro {f(p0['ep'], 3)}; limite de 3 erros {f(p0['limite_3_ep'], 3)}).")
    a(f"  Fração dos marcadores nas últimas posições da lista do cargo: {f(100 * p0['fracao_no_fim_da_lista'], 1)}%. Posição média normalizada dos brancos {f(p0['brancos_posicao_media'], 3)} (n {p0['brancos_n']}) e dos nulos digitados {f(p0['nulos_digitados_posicao_media'], 3)} (n {p0['nulos_digitados_n']}); lista uniforme daria 0,500.")
    a(f"  Leitura: {p0['leitura']}.")
    a('')
    a('PARTE A, D1.4 (modelo base: y = 100 x L2/(L2+R2), efeito fixo, X do 1º turno e perfil, dose D_h e controle D_h do 1º turno)')
    for nome, r in R['parteA'].items():
        if 'n' not in r:
            a(f"  {nome}: não estimável ({r['secoes_na_amostra']} seções)"); continue
        ve = R['vereditos_A'].get(nome, {})
        a(f"  {nome}{' (LETRA)' if r['letra'] else ' (ao lado)'}: n {r['n']}, grupos {r['grupos_do_efeito_fixo']}, municípios {r['municipios']}. Parte: {ve.get('parte')}")
        for h in JANELAS:
            j = r['janelas'][f'{h}h']; c = r.get('calibracao', {}).get(f'{h}h')
            pl = j.get('placebo_1t')
            s = (f"    {h}h: b {f(j['b'])} (ep {f(j['ep'])}, z {f(j['z'])}); Phi {f(j['Phi'], 3)} (IC99 {f(j['Phi_ic99'][0], 3)} a {f(j['Phi_ic99'][1], 3)}); "
                 f"votos de margem {f(j['votos_de_margem'], 0)}; degrau {f(j['degrau_no_conjunto'])}; placebo 1T {f(pl['b']) if pl else 'n/d'} (ep {f(pl['ep']) if pl else 'n/d'})")
            if c:
                s += (f"; plantio Phi 0,25/0,5/1 enxergado em {f(100 * c['Phi_0.25']['enxerga'], 0)}%/{f(100 * c['Phi_0.5']['enxerga'], 0)}%/{f(100 * c['Phi_1.0']['enxerga'], 0)}%, "
                      f"recuperação em 0,5: {f(c['Phi_0.5']['recuperacao'])}; espelho -1 visto em {f(100 * c['espelho_Phi_-1.0']['enxerga'], 0)}%; "
                      f"inocentes com critério inteiro: rampa {f(100 * c['inocente_I1_rampa']['criterio_inteiro_de_sinal'], 0)}%, composição {f(100 * c['inocente_I2_composicao']['criterio_inteiro_de_sinal'], 0)}%")
            s += f" => {ve.get(f'{h}h')}"
            a(s)
        fz = r['janelas_falsas']
        a('    janelas falsas (salto em h:37, z): ' + '; '.join(f"{k} {f(v['z'], 1)}" for k, v in fz.items()))
        if ve.get('espelho_a_favor_de_flavio'):
            a(f"    ESPELHO: contraste do mesmo tamanho a favor de Flávio em {ve['espelho_a_favor_de_flavio']}")
    a('')
    a('PARTE B, T30 DA EQUIPE VERMELHA (y = virada da fatia de Lula; regressor f2 x fatia de Flávio no 1º turno; controles f1, variação do comparecimento, fatia de Lula no 1º turno; erro CV3)')
    for nome, r in R['parteB'].items():
        if 'n' not in r:
            a(f'  {nome}: não estimável'); continue
        a(f"  {nome}{' (LETRA)' if r['letra'] else ' (ao lado)'}: n {r['n']}, grupos do efeito fixo {r['grupos_do_efeito_fixo']}, grupos do CV3 {r['grupos_do_cv3']}. Parte: {r['veredito_da_parte']} {r['contagem_de_vereditos']}")
        for rel in ('brasilia', 'urna'):
            for h in CORTES:
                o = r['cortes'][f'{rel}_{h}h']; c = o.get('calibracao')
                s = (f"    {rel} {h}h: inclinação {f(o['inclinacao'])} (ep CV3 {f(o['ep_cv3'])}, z {f(o['z_cv3'])}); placebo {f(o['placebo_virada']['inclinacao'])} (ep {f(o['placebo_virada']['ep_cv3'])}); "
                     f"espelho {f(o['espelho']['inclinacao'])} (z {f(o['espelho']['z_cv3'])})")
                if c:
                    s += (f"; troca de 5% produz {f(c['q_5%']['inclinacao_que_a_troca_produz'])}; EMD {f(o['emd_2,8_ep'])} = q {f(100 * o['emd_em_q'], 1) if o['emd_em_q'] else 'n/d'}% = {f(100 * o['emd_em_fracao_da_margem'], 1) if o['emd_em_fracao_da_margem'] else 'n/d'}% da margem; "
                          f"poder (valor e z) 5/10/15%: {f(100 * c['q_5%']['poder_valor_e_z'], 0)}/{f(100 * c['q_10%']['poder_valor_e_z'], 0)}/{f(100 * c['q_15%']['poder_valor_e_z'], 0)}%; "
                          f"margem implicada {f(o['votos_de_margem_implicados'], 0)}")
                s += f" => {o['veredito']}{' (intermediário)' if o['intermediario'] else ''}"
                a(s)
        if 'inocentes_plantados' in r:
            for k, v in r['inocentes_plantados'].items():
                a(f"    inocente {k}: cópias com algum corte em valor e z {f(100 * v['copias_com_algum_corte_em_valor_e_z'], 0)}%; com SINAL inteiro {f(100 * v['copias_com_algum_SINAL_inteiro'], 0)}%")
            a('    espelho plantado (10% dos votos de Lula depois do corte): ' + '; '.join(f"{k} visto em {f(100 * v['visto'], 0)}%" for k, v in r['espelho_plantado_10%'].items()))
        if r['espelho_cortes_com_sinal_a_favor_de_flavio']:
            a(f"    ESPELHO nos dados reais: {r['espelho_cortes_com_sinal_a_favor_de_flavio']}")
    rl = R['relogios']
    a(f"  Separação dos relógios (ao lado): {rl['secoes']} seções fora do relógio de Brasília {rl['por_uf']}")
    for rel in ('brasilia', 'urna'):
        a('    ' + rel + ': ' + '; '.join(f"{h}h {f(rl['cortes'][f'{rel}_{h}h']['inclinacao'], 1)} (z {f(rl['cortes'][f'{rel}_{h}h']['z_cv3'], 1)})" for h in CORTES if rl['cortes'].get(f'{rel}_{h}h')))
    a('')
    p2 = R['parte2']; t = p2['votos_a_partir_das_17h']
    a('PARTE 2, PRORROGAÇÃO')
    a(f"  Amostra P: {p2['amostra_P_no_universo_refeito']} seções lidas de {p2['universo_P']} que encerraram às 18:30 de Brasília ou depois (universo refeito com a base: {p2['universo_P_refeito_com_a_base']}).")
    a(f"  Votos computados a partir das 17h de Brasília: nas prorrogadas T_P = {f(t['T_P'], 0)} (ep {f(t['ep_P'], 0)}); no resto do país T_resto = {f(t['T_resto'], 0)} (ep {f(t['ep_resto'], 0)}, {p2['aas_fora_de_P']} seções da aleatória); T = {f(t['T'], 0)} (ep {f(t['ep'], 0)}).")
    a(f"  2 x T = {f(t['dobro_de_T'], 0)} = {f(100 * t['fracao_da_margem'], 2)}% da margem (limite superior de 99%: {f(t['dobro_lim_sup_99'], 0)}); limiar 443.019.")
    a(f"  A partir das 18h: T = {f(p2['votos_a_partir_das_18h']['T'], 0)} (ep {f(p2['votos_a_partir_das_18h']['ep'], 0)}); a partir das 19h: {f(p2['votos_a_partir_das_19h']['T'], 0)} (ep {f(p2['votos_a_partir_das_19h']['ep'], 0)}).")
    e = p2['espelho_1t_votos_a_partir_das_17h']
    a(f"  Espelho (dia do 1º turno, mesmas seções): T = {f(e['T'], 0)} (ep {f(e['ep'], 0)}).")
    c = p2['calibracao_plantio_221510']
    a(f"  Calibração: 221.510 votos plantados depois das 17h nas prorrogadas; a conta devolve +{f(c['acrescimo_devolvido'], 0)} e acusa em {f(100 * c['copias_que_acusam'], 0)}% das cópias.")
    a(f"  Veredito: {p2['veredito']}.")
    a('')
    a('BRUTO DE 2026 (amostra aleatória, sem modelo): quintis da fração de votos do 2º turno das 12h em diante')
    for q in R['bruto']['D_12h']:
        a(f"  quintil {q['quintil']}: n {q['n']}, D {f(100 * q['D_medio'], 1)}%, Lula no 1º turno (dois candidatos) {f(q['lula_1t_dois_candidatos'])}, no 2º {f(q['lula_2t'])}, virada {f(q['virada'])}")
    a('')
    for s in R.get('notas', []):
        a(s)
    return '\n'.join(L) + '\n'


def notas(R):
    """Linhas finais do texto, montadas a partir dos números (nada digitado à mão)."""
    N = []; a = N.append
    pb = R['parteB']; pa = R['parteA']; ex = R['exploratorio']
    a('PODER DE CADA AMOSTRA (Parte B: efeito mínimo detectável, 2,8 ep CV3, em % dos votos de Flávio depois do corte e em % da margem; relógio de Brasília)')
    for nome in ('ANT_local', 'AAS_local', 'UNI_local', 'ANT_municipio', 'AAS_municipio', 'UNI_municipio', 'AAS_uf', 'UNI_uf'):
        r = pb.get(nome)
        if not r or 'n' not in r: continue
        ps = []
        for h in (10, 12, 14, 15, 16):
            o = r['cortes'][f'brasilia_{h}h']
            if o.get('emd_em_q') is not None:
                ps.append(f"{h}h q {f(100 * o['emd_em_q'], 1)}% = {f(100 * o['emd_em_fracao_da_margem'], 0)}% da margem")
        a(f"  {nome} (n {r['n']}, {r['grupos_do_efeito_fixo']} grupos): " + '; '.join(ps))
    a('PODER DE CADA AMOSTRA (Parte A: erro de Phi por janela; Phi = 1 é a margem inteira)')
    for nome, r in pa.items():
        if 'n' not in r: continue
        a(f"  {nome} (n {r['n']}): " + '; '.join(f"{h}h ep {f(r['janelas'][f'{h}h']['Phi_ep'], 3)}" for h in JANELAS))
    a('')
    a('AO LADO, SEM CONTROLE DE PRÉDIO (efeito fixo de município ou de UF; não é a especificação da letra)')
    for nome in ('ANT_municipio', 'AAS_municipio', 'UNI_municipio', 'AAS_uf', 'UNI_uf'):
        r = pb.get(nome)
        if not r or 'n' not in r: continue
        sn = [k for k, o in r['cortes'].items() if o['veredito'] == 'SINAL']; vz = [k for k, o in r['cortes'].items() if o['passa_valor_e_z']]
        a(f"  {nome}: cortes que passam valor e z: {len(vz)} de 18; com o critério inteiro (dose e placebo): {len(sn)} {sn}")
    a('  Leitura registrada antes (A2): essas contas controlam menos a composição e só valem como apoio. O que elas mostram, sem suavizar: na amostra')
    a('  aleatória, seção com mais voto à tarde virou mais para Lula, com inclinação que cresce com a hora e z de até 6 ou 7. Lida inteira como gatilho,')
    o12 = pb['AAS_uf']['cortes']['brasilia_12h']
    a(f"  essa associação valeria a margem quase toda (AAS com efeito fixo de UF, 12h: inclinação {f(o12['inclinacao'])}, margem implicada {f(o12.get('votos_de_margem_implicados'), 0)}).")
    a('')
    a('EXPLORATÓRIO (escolhido depois de ver a primeira rodada; não muda veredito)')
    a('  1. Dentro do prédio contra entre prédios do mesmo município (um gatilho na urna prevê a mesma inclinação nos dois níveis):')
    for nome, r in ex['dentro_e_entre_locais'].items():
        a(f"     {nome} ({r['secoes']} seções, {r['locais']} locais): " + '; '.join(
            f"{h} dentro {f(o['dentro_do_local'], 1)} (ep {f(o['ep_dentro'], 1)}), entre {f(o['entre_locais'], 1)} (ep {f(o['ep_entre'], 1)}), z da diferença {f(o['z_da_diferenca'], 1)}"
            for h, o in r['cortes'].items() if h in ('12h', '13h', '14h', '15h', '16h')))
    a('  2. Parte B com os controles que a letra não tem (eliminados, brancos, nulos e abstenção do 1º turno = E; mais o perfil de idade, sexo, escolaridade e biometria = E+P):')
    for nome in ('UNI_local', 'AAS_municipio', 'UNI_municipio', 'AAS_uf', 'UNI_uf'):
        r = ex['parte_B_com_mais_controles'].get(nome, {})
        a(f"     {nome}: " + '; '.join(f"{h} letra {f(o['letra']['inclinacao'], 1)}, E {f(o['com_E']['inclinacao'], 1)}, E+P {f(o['com_E_e_perfil']['inclinacao'], 1)} (ep {f(o['com_E_e_perfil']['ep'], 1)})"
                                       for h, o in r.items() if h in ('10h', '12h', '14h', '15h', '16h') and o.get('letra') and o.get('com_E') and o.get('com_E_e_perfil')))
    rec = [o['com_E_e_perfil'].get('troca_de_5%_plantada_produz') for r in ex['parte_B_com_mais_controles'].values() for o in r.values() if o.get('com_E_e_perfil')]
    rec = [x for x in rec if x is not None]
    if rec:
        a(f"     O modelo E+P continua enxergando um gatilho: troca de 5% plantada produz de {f(min(rec), 1)} a {f(max(rec), 1)} pontos de inclinação nas {len(rec)} combinações testadas (50 cópias cada).")
    a('  3. Simetria (a = efeito do voto tardio onde só há voto de Flávio; c = onde só há voto de Lula; troca de Flávio para Lula prevê c = 0):')
    for nome in ('ANT_local', 'UNI_local', 'AAS_uf'):
        r = ex['simetria'].get(nome, {})
        a(f"     {nome}: " + '; '.join(f"{h} a {f(o['a_onde_flavio'], 1)} (z {f(o['z_a'], 1)}), c {f(o['c_onde_lula'], 1)} (z {f(o['z_c'], 1)})" for h, o in r.items() if o and h in ('10h', '12h', '14h', '16h')))
    orr = ex['ordem_do_rdv']
    a(f"  4. Ordem do RDV: em {orr['rdv_lidos']} RDV do 2º turno, {orr['listas_com_tipos_em_ordem_crescente']} têm os tipos em ordem crescente e {orr['pares_com_numero_nao_decrescente']} de {orr['pares_vizinhos_nominais']} pares vizinhos de votos nominais têm número não decrescente")
    a(f"     ({f(orr['blocos_de_numero_igual_por_lista_media'], 2)} blocos por lista para {f(orr['candidatos_distintos_por_lista_media'], 2)} candidatos): a lista publicada está agrupada por tipo e por candidato, não guarda ordem de votação.")
    a('')
    pg = R['placebo_governador']
    if 'specs' in pg:
        a('PLACEBO DE GOVERNADOR (ao lado; 6 UFs; desfecho = finalista do lado de Lula para governador)')
        for nome, r in pg['specs'].items():
            a(f"  {nome} ({r['secoes']} seções): " + '; '.join(f"{h} b {f(o['b'], 1)} (ep {f(o['ep'], 1)}, z {f(o['z'], 1)}, n {o['n']})" for h, o in r['janelas'].items() if o))
    pc = R['cortes_na_amostra_P']
    a(f"CORTES NA AMOSTRA P (ao lado, efeito fixo de município, {pc['secoes']} seções): " + '; '.join(
        f"{h} inclinação {f(o['inclinacao'], 1)} (ep CV3 {f(o['ep_cv3'], 1)}), EMD {f(o['emd_2,8_ep'], 1)} contra {f(o['inclinacao_que_a_troca_produz']['q_5%'], 1)} da troca de 5%" for h, o in pc['cortes'].items() if 'inclinacao' in o) + ': sem poder.')
    a('')
    a('DESVIOS E DECISÕES FORA DO REGISTRO (todas escritas no docstring antes de rodar, salvo a última)')
    a('  1. Parte 2 com a lista P (400 de 6.773 seções que encerraram às 18:30 de Brasília ou depois, sorteio simples) em vez de 600 de 7.089, proporcional por UF; o resto do país entra pela amostra aleatória.')
    a('  2. Amostra aleatória: o registro pede efeito fixo de local, e ela só tem 70 locais com 2 seções. Leituras com efeito fixo de município e de UF ficaram ao lado, sem decidir.')
    a('  3. Fração nacional de cada janela pela amostra aleatória nova (o desenho previa pesos da amostra antiga, que não existem guardados).')
    a('  4. Regras fixadas por mim: "dose crescente em 3 horas vizinhas", placebo de virada pela letra (f1 no lugar de f2, mantendo o controle f1), fatia de Flávio = R1/(L1+R1), "enxerga" e SEM PODER da Parte A (plantio de Phi = 1 visto em menos de 95%).')
    a('  5. Placebo de governador com controles reduzidos (frações do 1º turno dos dois finalistas, por UF), não o X inteiro: poucas seções.')
    a('  6. Depois de ver a primeira rodada: calibração estendida a todas as especificações ao lado; contas exploratórias 1 a 4. Os números observados não mudaram entre as rodadas; os das cópias mudam na segunda casa porque a sequência de sorteios mudou.')
    a('  7. Não feito: baixar mais 4.000 logs com sobreamostra em AC, AM, MT, MS, RO e RR (a amostra aleatória nova fez esse papel, sem sobreamostra); desfecho contra 2022 com conferência do pareamento de seções (usei a chave igual).')
    a('')
    ul = pa['UNI_local']['janelas']; ub = pb['UNI_local']['cortes']; p2 = R['parte2']['votos_a_partir_das_17h']
    de = ex['dentro_e_entre_locais']['UNI']['cortes']
    a('LEITURA')
    a('  O que pesa A FAVOR da tese, sem suavizar:')
    a(f"  a) O reteste da equipe vermelha (Parte B) não absolve nenhum dos 18 cortes. Dentro do mesmo prédio a inclinação é positiva em todos os cortes de 9h a 16h (de {f(min(ub[f'brasilia_{h}h']['inclinacao'] for h in range(9, 16)), 1)} a {f(max(ub[f'brasilia_{h}h']['inclinacao'] for h in range(9, 16)), 1)} até as 15h; {f(ub['brasilia_16h']['inclinacao'], 1)} às 16h, z {f(ub['brasilia_16h']['z_cv3'], 1)}),")
    a(f"     sem chegar ao z de 3,2. Lida inteira como gatilho, valeria de {f(min(ub[f'brasilia_{h}h']['votos_de_margem_implicados'] for h in range(9, 17)), 0)} a {f(max(ub[f'brasilia_{h}h']['votos_de_margem_implicados'] for h in range(9, 17)), 0)} votos de margem, conforme o corte. O teste não exclui uma troca de 5% dos votos de Flávio dados depois das 12h ({f(100 * ub['brasilia_12h']['emd_em_fracao_da_margem'], 0)}% da margem).")
    a('  b) Sem o controle de prédio, na amostra aleatória, a associação é forte, cresce com a hora e passa o critério inteiro em 10 ou 11 dos 18 cortes.')
    a(f"  c) Depois das 16h todas as contas dão positivo: na Parte A, b = {f(ul['16h']['b'])} (ep {f(ul['16h']['ep'])}), com degrau na mesma hora e placebo de 1º turno limpo; faltam o tamanho (Phi {f(ul['16h']['Phi'], 3)}, limiar 0,5) e o z ({f(ul['16h']['z'], 1)}, limiar 3,9).")
    a('  d) Janelas largas (gatilho desde a manhã ou desde o meio-dia): sem poder. Um gatilho assim se confunde com troca uniforme, que este teste não enxerga.')
    a('  O que pesa CONTRA:')
    a(f"  a) No desenho cego (Parte A), dentro do prédio, Phi é {f(ul['14h']['Phi'], 3)} às 14h, {f(ul['15h']['Phi'], 3)} às 15h e {f(ul['16h']['Phi'], 3)} às 16h; um gatilho de fim de tarde que explique metade da margem está excluído a 99% (tetos {f(ul['14h']['Phi_ic99'][1], 2)}, {f(ul['15h']['Phi_ic99'][1], 2)} e {f(ul['16h']['Phi_ic99'][1], 2)} da margem), com o plantio enxergado.")
    a(f"  b) A associação está ENTRE prédios, não dentro: às 14h a inclinação entre prédios do mesmo município é {f(de['14h']['entre_locais'], 1)} contra {f(de['14h']['dentro_do_local'], 1)} dentro do prédio (z da diferença {f(de['14h']['z_da_diferenca'], 1)}). Um gatilho na urna daria a mesma nos dois níveis.")
    a('  c) Com o perfil do eleitorado da seção como controle a associação da amostra aleatória some à tarde, e o mesmo modelo continua enxergando o gatilho plantado.')
    a('  d) Dentro do prédio o padrão é simétrico: onde Lula é forte, mais voto tardio acompanha ganho de Flávio (c negativo). Troca de Flávio para Lula daria c = 0.')
    a('  e) O voto de governador do lado de Lula sobe junto com o voto tardio nas 6 UFs (16h, z de 4 dentro do prédio): é quem vota tarde, não o cargo.')
    a(f"  f) Prorrogação: {f(p2['T'], 0)} votos depois das 17h de Brasília no país (ep {f(p2['ep'], 0)}); mesmo todos irregulares valeriam {f(100 * p2['fracao_da_margem'], 1)}% da margem.")
    a('')
    a('CONTAGEM DE TESTES: 5 janelas (Parte A) e 18 cortes (Parte B) em 3 amostras da letra, mais 1 limite (Parte 2): 70 cláusulas. Com z de 3,9 e de 3,2 o acaso daria menos de 0,1 sinal.')
    return N



def modo_rodar():
    rng = np.random.default_rng(SEMENTE)
    doc = open(os.path.join(TRAB, 'docstring_antes_de_rodar.txt')).read() if os.path.exists(os.path.join(TRAB, 'docstring_antes_de_rodar.txt')) else None
    diz('montando a base')
    T, P, aas, meta, extra = montar()
    grava('parcial_meta.json', meta)
    diz('base', meta)
    V = carregar(TRAB + '/votos_hora.json.gz')
    p0 = parte0(V); del V
    grava('parcial_parte0.json', p0)
    diz('parte 0', p0['todos'])
    if p0['todos']['guarda_relacao']:
        diz('PARTE 0: a posição no RDV guarda relação com a ordem. O desenho tem de ser reescrito. Parando.')
        return
    F = nacional_F(T)
    grava('parcial_F.json', F)
    p2 = parte2(P, aas, meta, rng)
    grava('parcial_parte2.json', p2)
    diz('parte 2', p2['criterio'])
    br = bruto(T)
    pc = cortes_em_P(extra['B'], extra['fuso'])
    grava('parcial_cortes_em_P.json', pc)
    try:
        pg = placebo_gov(T, extra['B'])
    except Exception as e:
        pg = {'erro': repr(e)}
    grava('parcial_placebo_gov.json', pg)
    del extra
    pb = parte_b(T, F, rng)
    rl = relogios(T)
    pa = parte_a(T, F, rng)
    va = {nome: veredito_a(r, nome) for nome, r in pa.items() if 'n' in r}
    ex = {'aviso': 'EXPLORATÓRIO: contas escolhidas depois de ver a primeira rodada; não mudam veredito',
          'dentro_e_entre_locais': exploratorio_dentro_e_entre(T), 'parte_B_com_mais_controles': exploratorio_controles(T),
          'simetria': exploratorio_simetria(T), 'ordem_do_rdv': exploratorio_ordem_rdv()}
    grava('parcial_exploratorio.json', ex)
    R = {'teste': 'R27_C2 gatilho por horário', 'docstring_sha256': hashlib.sha256(doc.encode()).hexdigest() if doc else None,
         'meta': meta, 'fracao_nacional': {str(h): v for h, v in F.items()}, 'parte0': p0, 'parteA': pa, 'vereditos_A': va,
         'parteB': pb, 'relogios': rl, 'parte2': p2, 'cortes_na_amostra_P': pc, 'placebo_governador': pg, 'bruto': br, 'exploratorio': ex}
    R['vereditos'] = {
        'Parte 0 (RDV e ordem de votação)': p0['todos']['leitura'],
        'Parte A (D1.4, letra, UNI com efeito fixo de local)': f"{va.get('UNI_local', {}).get('parte')} " + str({k: v for k, v in va.get('UNI_local', {}).items() if k.endswith('h')}),
        'Parte A na ANT (letra)': f"{va.get('ANT_local', {}).get('parte')} " + str({k: v for k, v in va.get('ANT_local', {}).items() if k.endswith('h')}),
        'Parte A na AAS (letra)': f"{va.get('AAS_local', {}).get('parte')} " + str({k: v for k, v in va.get('AAS_local', {}).items() if k.endswith('h')}),
        'Parte B (T30, letra, UNI com efeito fixo de local)': f"{pb['UNI_local'].get('veredito_da_parte')} {pb['UNI_local'].get('contagem_de_vereditos')}",
        'Parte B na ANT (letra)': f"{pb['ANT_local'].get('veredito_da_parte')} {pb['ANT_local'].get('contagem_de_vereditos')}",
        'Parte B na AAS (letra)': f"{pb['AAS_local'].get('veredito_da_parte')} {pb['AAS_local'].get('contagem_de_vereditos')}",
        'Parte 2 (prorrogação)': p2['veredito']}
    R['notas'] = notas(json.loads(json.dumps(R, default=_js)))
    grava('resultado_completo.json', R)
    with open(REPO + '/resultados/R27_C2_gatilho_por_horario.json', 'w') as fo:
        json.dump(R, fo, ensure_ascii=False, indent=1, default=_js)
    with open(REPO + '/resultados/R27_C2_gatilho_por_horario.txt', 'w') as fo:
        fo.write(texto(json.loads(json.dumps(R, default=_js))))
    diz('fim')


def modo_exploratorio():
    """Refaz só o bloco exploratório e o texto, a partir do resultado completo já gravado."""
    T, P, aas, meta, extra = montar(); del extra
    R = json.load(open(os.path.join(TRAB, 'resultado_completo.json')))
    R['exploratorio'] = {'aviso': 'EXPLORATÓRIO: contas escolhidas depois de ver a primeira rodada; não mudam veredito',
                         'dentro_e_entre_locais': exploratorio_dentro_e_entre(T), 'parte_B_com_mais_controles': exploratorio_controles(T),
                         'simetria': exploratorio_simetria(T), 'ordem_do_rdv': exploratorio_ordem_rdv()}
    R = json.loads(json.dumps(R, default=_js))
    R['notas'] = notas(R)
    grava('resultado_completo.json', R)
    with open(REPO + '/resultados/R27_C2_gatilho_por_horario.json', 'w') as fo:
        json.dump(R, fo, ensure_ascii=False, indent=1, default=_js)
    with open(REPO + '/resultados/R27_C2_gatilho_por_horario.txt', 'w') as fo:
        fo.write(texto(R))
    diz('fim do exploratório')


if __name__ == '__main__':
    modo = sys.argv[1] if len(sys.argv) > 1 else ''
    if modo == 'extrair': modo_extrair()
    elif modo == 'rodar': modo_rodar()
    elif modo == 'exploratorio': modo_exploratorio()
    else: print(__doc__)
