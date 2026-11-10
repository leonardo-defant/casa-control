"""R27_C3: COERÊNCIA INTERNA DA URNA E REAÇÃO DO ELEITOR NA TELA (teste D1.6 de registro/adendo27/desenho_D1_proposta.json).

Adendo 27 do pré-registro (commit 2748895, 10/11/2026 00:16:42 UTC), Onda C, item C3, mantido pelos Adendos 28 (commit
938be19) e 30 (commit a7218fb, 10/11/2026 10:08:24 UTC: "C3 (coerência interna e reação na tela)"). Os critérios valem
como escritos nos campos estatistica, criterio_sinal, criterio_sem_sinal, poder, placebo e explicacao_inocente do D1.6.
Este docstring foi escrito ANTES de qualquer conta deste teste com votos por candidato. O que ele decide e o registro
não fixa está em DECISÕES e sai no resultado como desvio. O que for feito depois de ver resultado fica em funções com
nome "exploratorio_" e sai marcado. O D1.6 é desenho cego (o autor só viu estrutura).

Uso (sempre com python3 -I):
  scripts/analisar_R27_C3.py extrair   lê os logs (sem voto por candidato) e grava R27_C3/logs_C3.pkl.gz
  scripts/analisar_R27_C3.py urna      lê boletins e RDV (com votos) e grava R27_C3/urna_C3.pkl.gz
  scripts/analisar_R27_C3.py rodar     roda as três partes e grava resultados/R27_C3_coerencia_e_reacao_na_tela.json e .txt
Trabalho e parciais: /home/user/trabalho-eleicao/adendo27/R27_C3/

O QUE CADA PARTE PROVA E O QUE NÃO PROVA (dito antes)
(a) e (b) usam só arquivos que saem do mesmo programa da urna. Enxergam alteração DESCUIDADA (um produto mexido e os
outros não), programa trocado em parte das urnas que o verificador genuíno acusa, ou mistura de versões. Um programa
adulterado na origem, assinado com as chaves oficiais e coerente, escreve boletim, RDV e log iguais entre si e registra
SUCESSO: passa por (a) e por (b) inteiras. Só (c) mede algo fora do controle do programa, o comportamento do eleitor
diante da tela, e só se a tela MOSTRASSE a troca. Troca invisível na tela passa por (c) também. E (c) ainda depende
de o log registrar com fidelidade a tecla CORRIGE: um programa que escondesse do log as correções passaria.

O QUE EU JÁ SABIA ANTES DE ESCREVER (contaminação declarada)
- Li ADENDO27_ondaA_resultados.txt e ADENDO27_ondaB_resultados.txt (a virada passa pelo comparecimento; sem marca de
  troca onde há poder) e o R27_DA (D3-3) inteiro: na amostra aleatória, RDV igual ao boletim em 3.000 de 3.000 nos
  dois turnos; votos computados no log iguais ao comparecimento em 3.000 de 3.000; uma seção (BA|37311|50|156) com 185
  confirmações de presidente e 184 votos, com queda de energia no log; o mesmo padrão em MG|46698|139|34 (amostra
  antiga), RJ|60011|234|189 (lista P) e 3 seções no dia do 1º turno. Do R27_C2: nulos por suspensão aparecem no RDV do
  1º turno como tipo 6, em número igual ao do log (230 = 230). Logo a parte (a) é quase toda reconferência com leitor
  próprio; o que ela tem de novo são as identidades de suspensão por seção e cargo e os 835 RDV da amostra antiga.
- Do desenho D1 (observações de estrutura): versão única, UEFI por modelo, fase Oficial em todas, duas seções com etapa
  de assinatura sem SUCESSO (PB|21873|33|98 e BA|33553|169|132), taxas 0,85% e 0,73% de correção, 334 e 3 suspensões.
- Estrutura que eu mesmo levantei antes de escrever, SEM voto por candidato (R27_C3/extrair_logs_C3.py, o mesmo leitor
  que está neste arquivo): (i) a lista de pacotes verificados na inicialização tem 34 etapas e a ordem dos quatro
  pacotes /uenux/bin/avpart9x.vst muda de urna para urna (dezenas de sequências por modelo); posta em ordem alfabética
  e trocados o código da seção e a UF por marcadores, sobra uma lista por modelo (só muda /lib/modules/ue20xx), mais
  três variantes só em pacotes de DADOS: todas as urnas de PE têm uma etapa a mais (o06261<uf>-ce.vsc), todas as do
  exterior têm uma a menos (o06259<uf>-ce.vsc) e uma urna (BA|34193|53|239, série 02305282) tem uma a menos
  (<seção>-lo.vsc da mídia externa) depois de três erros "GAP erro 16 | Sincronização da MI para MV" e de um
  "procedimento de contingência de MV" registrado no próprio log; (ii) três etapas sem SUCESSO: BA|33553|169|132
  (04/10 08:24:40, série 02305138, /uenux/bin/avusrbin.vst, urna sem nenhum voto, trocada por contingência),
  PB|21873|33|98 (22/09, infomidia.vsc, preparação; a mesma urna passou depois e recebeu os votos dos dois turnos) e
  DF|97012|13|105 (23/09, infomidia.vsc, preparação, nova carga 5 minutos depois; idem); (iii) confirmações de
  presidente mais suspensões diferentes dos votos computados em 1 seção por amostra no 2º turno (as já conhecidas) e em
  CE|13676|22|4 no 1º; em todas há religamento da urna entre a confirmação e a habilitação seguinte; (iv) taxas
  agregadas de correção na tela de presidente perto de 0,7% (1º turno) e 0,9% (2º); ordem das telas no 2º turno:
  Governador > Presidente nas UFs com 2º turno de governador, Presidente sozinho nas demais.
- Para testar o decodificador abri o boletim e o RDV de UMA seção (AC|1392|9|117).
- Não eram conhecidos: nenhum coeficiente da parte (c), nenhum resíduo da parte (b), nenhuma soma com sinal da (a)
  na amostra antiga, nenhuma calibração.

=========================== O QUE O REGISTRO FIXA (D1.6) ===========================
(a) Por seção e por cargo do 2º turno: BU = RDV candidato a candidato, brancos e nulos; linhas do RDV = comparecimento
    = votos computados no log; confirmações de presidente + nulos por suspensão de presidente = comparecimento; RDV
    tipo 6 = suspensões do log; nulos do BU maiores ou iguais às suspensões do log. Contar violações e somar a
    diferença com sinal (BU menos RDV, por candidato).
    SINAL: qualquer seção com BU diferente do RDV em presidente, ou suspensão no log sem nulo correspondente, que não
    se explique por contingência documentada no próprio log. SEM SINAL: zero violações (regra de três: menos de 0,08%
    das urnas). INCONCLUSIVO: violações explicadas só em parte por contingência; RDV que não pôde ser baixado.
    Poder: contagem exata; conferir o leitor plantando (alterar um voto em cópia de um RDV e ver a identidade quebrar).
    Placebo: as mesmas identidades no 1º turno e no cargo de governador do 2º turno.
(b) Impressão digital por urna: versão do aplicativo, modelo, UEFI, fase e a lista ordenada de pacotes verificados na
    última inicialização antes da votação de 25/10; contar impressões distintas por modelo; listar etapas sem SUCESSO
    e o que veio depois.
    SINAL: qualquer urna que computou voto oficial com etapa de assinatura sem SUCESSO na inicialização do dia, ou
    impressão digital minoritária em 20 urnas ou mais com resíduo médio de y deslocado (z de 3,3 ou mais em módulo).
    SEM SINAL: uma impressão digital por modelo e nenhuma etapa sem SUCESSO em urna que recebeu voto.
(c) c2 = fração de eleitores com "Eleitor corrigiu" na tela de presidente no 2º turno; c1 = o mesmo no 1º turno;
    "Tecla indevida" como controle. Regressão c2 = efeito fixo de UF + l x c1 + t2 x r2 + perfil etário + erro, com
    r2 = R2/(L2 + R2) e erro agrupado por município; regressão espelho de c1 sobre r1 = R1/(L1 + R1), dando t1.
    Estimando: t2 menos t1.
    SINAL: t2 menos t1 de 0,0045 ou mais com z de 3,3 ou mais (troca visível de um quarto da margem, 0,89% dos votos
    de Flávio, com metade dos atingidos corrigindo). SEM SINAL: limite superior de 99% de t2 menos t1 abaixo de 0,0045.
    Poder: somar às correções do 2º turno um binomial com taxa 0,0357 x Phi x 0,5 x r2 por eleitor.
    Placebo: o gradiente do 1º turno (t1); as telas dos outros cargos do 1º turno; "Tecla indevida".
    Explicação inocente: no 2º turno a tela de presidente é a primeira (mais erro de início) e eleitores mais velhos
    corrigem mais.

=========================== DECISÕES QUE O REGISTRO NÃO FIXA (escritas antes de rodar) ===========================
DADOS E AMOSTRAS (desvio mandado pela tarefa desta onda)
G1. ANT = amostra antiga (amostra2t/arq: 3.897 logs e boletins, 835 RDV; não aleatória). AAS = amostra aleatória simples
    nova (aas/t2 e aas/t1: 3.000 seções com boletim e RDV dos dois turnos, log e assinatura do 2º). UNI = união das
    duas, cada seção uma vez (a cópia da AAS vale nas seções repetidas). Em vez de baixar os 3.062 RDV que faltam na
    ANT, uso os 3.000 da AAS: as identidades com RDV valem para 835 + 3.000 seções (menos as repetidas), as de log e
    boletim para a UNI inteira. Ao lado, sem entrar no veredito: lista P e C1 (aas/c1p_t2), extensão (aas/ext_t2 e
    ext_t1, só boletim e RDV, o que estiver completo em disco na hora de rodar) e os 80 boletins de amostra2t/arq1t.
G2. Só a AAS é amostra aleatória do país: todo limite "no país" sai da AAS; a UNI vai ao lado como contagem.
LEITOR DO LOG (sem voto; o log não registra tecla de número nem voto)
E1. Pacote = -log.jez; blocos = logd.dat do pacote e de cada .jez aninhado (urna original em caso de contingência). Um
    trecho só conta para a seção do pacote se a identidade corrente do bloco (linhas "Município:", "Zona Eleitoral:",
    "Seção Eleitoral:" do aplicativo GAP) for a da seção; trecho sem identidade só entra se for do logd.dat principal.
E2. Dias 04/10/2026 (1º turno) e 25/10/2026 (2º turno), aplicativo VOTA. Eleitor = de "Eleitor foi habilitado" até
    "O voto do eleitor foi computado". Tela de um cargo = do evento anterior (habilitação ou confirmação do cargo
    anterior) até "Voto confirmado para [cargo]"; "Tecla indevida pressionada" e "Eleitor corrigiu na tela de
    confirmação de candidato" contam para a tela em curso. Se o eleitor for suspenso, o que estava pendente conta para
    o primeiro cargo anulado. Senador tem duas telas (Senador#1 e Senador#2).
E3. Inicialização = cada corrida de "Verificação de assinatura - Etapa [n]" do GAP (recomeça quando n volta a 1), dentro
    de cada ligação da urna ("Início das operações do logd"). Os votos computados contam para a última corrida antes
    deles na mesma ligação.
E4. Confirmação órfã = "Voto confirmado para [Presidente]" sem "O voto do eleitor foi computado" antes da habilitação
    seguinte ou do fim do bloco.
PARTE (a)
A1. Cargos do 2º turno: presidente (código 1) em todas; governador (código 3) onde houve, como placebo do desenho.
    Identidades por seção e cargo:
      I1  BU = RDV: cada número de candidato (RDV tipo 2), brancos (tipo 3) e nulos (tipo 4 mais tipo 6);
      I2a linhas do RDV do cargo = comparecimento do cargo no BU;
      I2b votos computados no log (E1) = comparecimento do cargo no BU;
      I3  confirmações do cargo no log + nulos por suspensão do cargo no log = votos computados no log;
      I4  RDV tipo 6 do cargo = suspensões do cargo no log;
      I5  nulos do BU >= suspensões do cargo no log.
    Soma com sinal: BU menos RDV para 13, 22, brancos e nulos, somada nas seções; "a favor de Lula" = (13 - 22).
A2. "Explicada por contingência documentada no próprio log" (regra automática, fixada agora):
      I3: a diferença é igual ao número de confirmações órfãs do cargo (E4) e em cada uma há, entre a confirmação e a
          habilitação seguinte, religamento da urna ("Início das operações do logd"), desligamento ou tela de reinício
          da votação. Sobra para o outro lado (menos confirmações que votos) não tem explicação prevista.
      I2b: a seção tem mais de um número de série com voto no dia, ou log aninhado ilegível, ou linha de contingência.
      I1, I2a, I4 e I5 não têm explicação prevista: qualquer violação é caso a apresentar.
A3. Veredito da (a), nesta ordem: SINAL se houver violação de I1 em presidente, ou de I4 (mais suspensão no log que
    tipo 6 no RDV) ou I5, sem explicação. SEM SINAL se não houver violação alguma depois de retiradas as explicadas
    por inteiro pela regra A2 (elas saem listadas como casos) e o plantio for apontado. INCONCLUSIVO no resto.
    Leitura mais estrita, dita ao lado: "zero violações" sem descontar as explicadas; por ela, as seções já conhecidas
    com confirmação órfã levam a INCONCLUSIVO. Escrevo esta regra sabendo que esses casos existem (ver contaminação).
A4. Calibração (dados de 2026, em memória): P1 mover 1 voto do 22 para o 13 no RDV de 30 seções sorteadas (I1 tem de
    apontar 30 e nenhuma fora); P2 "conversão de nulo por suspensão" coerente em boletim e RDV (nulo do BU -1, 13 +1,
    tipo 6 -1, tipo 2 do 13 +1) em todas as seções com suspensão de presidente no log do dia, nos dois turnos (I4 tem
    de apontar todas); P3 um voto computado a menos no log em 30 seções (I2b e I3). Explicação inocente plantada: ler
    só o logd.dat principal nas seções de contingência (quantas violações falsas de I2b apareceriam sem somar o log
    aninhado). Espelho: as mesmas identidades no 1º turno das mesmas seções (AAS: boletim e RDV do 1º turno e o dia
    04/10 do log quando a urna é a mesma) e P1 no sentido contrário (13 para 22), que tem de aparecer com o sinal
    trocado na soma.
A5. Em votos: com zero violação em n seções da AAS, limite superior de 95% p = 1 - 0,05^(1/n) das 499.205 seções; pior
    caso = todos os votos válidos dessas seções trocados (2 x votos, em votos de margem); Phi = pior caso/4.430.191.
    Com violações sem explicação: a soma com sinal expandida (média por seção da AAS x 499.205, erro de amostra
    aleatória simples). Teto do canal "nulo por suspensão convertido": suspensões de presidente no log do 2º turno
    expandidas para o país.
PARTE (b)
B1. Unidade: corrida de inicialização (E3) depois da qual a urna computou voto da própria seção em 25/10 (e em 04/10,
    ao lado, como espelho). Impressão digital completa FC = (textos de "Versão da aplicação" da ligação, modelo, UEFI
    da série da urna [linha do SCUE na carga; as UE2013 e UE2015 não têm essa linha], fase, lista de pacotes
    verificados com o resultado). "Lista ordenada" = posta em ordem alfabética (a ordem em que os pacotes avpart9x
    aparecem no log muda de urna para urna; essa ordem vai ao lado, ver B5). Normalização: o código de 13 dígitos da
    seção vira <MZS> e a UF nos nomes o0NNNNuf- vira <uf>.
    Impressão digital de PROGRAMA FP = FC só com os pacotes fora de /dsk/ mais /dsk/fi/estatico/chave/avusrchave.vst
    (binários, bibliotecas, módulos, inicialização, vozes e chaves). Pacotes de DADOS = os demais de /dsk/ (arquivos
    da carga e das eleições da UF).
B2. Leitura de "uma impressão digital por modelo" (fixada agora, depois de ver a estrutura e antes de qualquer voto):
    conto FC por modelo no país e por modelo dentro de cada UF (os arquivos de dados das eleições são definidos por
    UF). Variante que é a mesma em todas as urnas de uma UF e não aparece em outra é "variante de dados da UF";
    variante com procedimento de contingência de mídia registrado no log da mesma ligação é "explicada por contingência
    documentada". O veredito usa FP por modelo no país e FC por modelo dentro da UF, descontadas as explicadas (que
    saem listadas). Leitura mais estrita, ao lado: FC por modelo no país inteiro.
B3. Etapa sem SUCESSO: toda linha "Verificação de assinatura" (GAP ou SCUE) que não termina em [SUCESSO], em qualquer
    data, com as 14 linhas seguintes, os votos oficiais computados depois na mesma ligação e depois no mesmo bloco pela
    mesma série. "Na inicialização do dia" (SINAL) = na corrida depois da qual há voto oficial na mesma ligação, em
    25/10 ou em 04/10. "Em urna que recebeu voto" (SEM SINAL) = idem. Leitura mais estrita, ao lado: qualquer etapa
    sem SUCESSO, em qualquer data, em urna (série) que depois computou voto oficial, mesmo com nova carga ou nova
    verificação bem sucedida no meio. Escrevo sabendo que há 2 urnas assim (PB e DF) e 1 que falhou sem voto (BA).
B4. Resíduo de y (só se houver variante minoritária em 20 urnas ou mais que varie DENTRO de UF): modelo base do D1,
    y = 100 x L2/(L2 + R2), peso V = L2 + R2, X = frações sobre o comparecimento do 1º turno de 13, 22, 70, 14, 55,
    demais nominais e brancos; abstenção do 1º turno; variação da abstenção; fração com biometria, de mulheres, 7
    faixas de idade e 7 graus de escolaridade (perfil F15, extração da A6); ln dos aptos; posição da seção no local.
    Indicador da variante com efeito fixo de município (principal; a amostra aleatória quase não tem dois ou mais
    seções por local), de local e de UF ao lado; erro por município; z = b/ep.
    Variante que coincide com uma UF inteira: o contraste é a própria UF e o efeito fixo o absorve; não é
    identificável. Ao lado, sem veredito: resíduo médio da UF no modelo com X e sem efeito fixo (só AAS), comparado
    com a distribuição do mesmo número nas outras UFs (posição e distância em desvios-padrão entre UFs).
B5. Ao lado, sem veredito: classes de ordem dos quatro pacotes avpart9x (até 24 por modelo). Para cada classe com 20
    urnas ou mais na UNI, b do indicador no modelo de B4 (efeito fixo de município). Conto |z| >= 3,3 e digo quantos
    o acaso daria. Também ao lado: resumo da lista de arquivos verificados pelo SCUE na carga (aplicação e dados),
    versão gravada no cabeçalho do boletim.
B6. Veredito da (b): SINAL pela letra (B3 ou B4). SEM SINAL se FP for uma por modelo, FC uma por modelo dentro da UF
    (descontadas as explicadas), nenhuma etapa sem SUCESSO em corrida seguida de voto, e a calibração apontar o
    plantado. INCONCLUSIVO no resto. Digo o veredito também pelas leituras mais estritas de B2 e B3.
B7. Calibração: Q1 trocar por [ERRO] o resultado de uma etapa na corrida do dia em 30 urnas (o contador tem de apontar
    30); Q2 trocar um pacote de programa por outro nome em 25 urnas sorteadas dentro de UFs (FP minoritária de 25
    urnas) e mover de R2 para L2 um binomial com taxa f nessas urnas, f = 3,57% (a troca uniforme que vira o
    resultado), 10% e 30%; 200 sorteios; fração com |z| >= 3,3 no teste de B4. Inocente: as mesmas 25 urnas sem mover
    voto (taxa de falso alarme). Espelho: mover de L2 para R2. Se o teste de resíduo não enxergar f = 30%, a cláusula
    de resíduo é SEM PODER (a contagem exata de impressões não depende dela).
B8. Em votos: com uma só FP por modelo em n urnas da AAS, limite de 95% para a fração de urnas com programa de
    impressão diferente = 1 - 0,05^(1/n); x 499.205; pior caso em votos como em A5.
PARTE (c)
C1. Universo: pares (seção com votos próprios nos dois dias no mesmo pacote, isto é, mesma urna ou urna substituta com o
    log do 1º turno junto), fora o exterior, com L2 + R2 de 30 ou mais, L1 + R1 maior que zero e perfil do eleitorado.
    Votos por seção: dados/secoes2026.json.gz (bweb). O exterior sai descrito à parte se tiver 20 pares ou mais.
C2. k_t = eleitores do dia t com pelo menos um "Eleitor corrigiu" na tela de presidente (E2); n_t = eleitores com voto
    computado no dia; c_t = k_t/n_t. i_t = o mesmo com "Tecla indevida pressionada". Perfil etário = frações do
    eleitorado da seção em 7 faixas (16 a 17, 18 a 24, 35 a 44, 45 a 59, 60 a 69, 70 a 79, 80 ou mais; 25 a 34 é a
    referência), do perfil F15.
C3. Regressão da letra, sem peso (o desenho não põe peso e a conta de poder dele é sem peso): c2 = efeito fixo de UF +
    l x c1 + t2 x r2 + perfil etário; espelho: c1 = efeito fixo de UF + t1 x r1 + perfil etário. T = t2 - t1. Erro de T:
    as duas regressões empilhadas, com a função de influência de cada município (CR1, a mesma correção de lib.fe_ols).
    z = T/ep. Limite superior de 99% = T + 2,576 x ep.
C4. Amostra do veredito: UNI. ANT e AAS ao lado; se ANT e AAS diferirem em mais de 2 erros, digo.
C5. Ao lado, fixadas agora e sem substituir a letra: S1 peso n_t; S2 sem o controle c1; S3 primeira diferença
    (c2 - c1) sobre r2; S4 efeito fixo de município; S5 com escolaridade, biometria e fração de mulheres a mais; S6 só
    as 21 UFs em que a tela de presidente é a única do 2º turno, e só as 6 em que vem depois da de governador; S7
    correções por eleitor (total de "Eleitor corrigiu" na tela de presidente sobre n_t) no lugar da fração de eleitores;
    S8 tempo de cabine na tela de presidente: média por seção de min(segundos da tela, 120) e fração de eleitores com
    mais de 30 segundos, com a mesma regressão (aviso dito antes: no 2º turno a tela de presidente é a primeira na
    maioria das UFs e o intervalo inclui o caminho da mesa à cabine; medida fraca, sem veredito próprio).
C6. Placebos e espelho: (i) t1, relatado; (ii) T da "Tecla indevida" (i_t no lugar de c_t); (iii) gradiente em r1 da
    correção nas telas dos outros cargos do 1º turno (Deputado Federal, Estadual ou Distrital, Senador#1, Senador#2,
    Governador); (iv) tela de governador do 2º turno nas UFs que a têm: T com a correção na tela de governador nos dois
    turnos. Espelho: o gradiente na fração de Lula é -T por construção; SINAL ESPELHADO se T for -0,0045 ou menos com z
    de -3,3 ou menos (eleitor de Lula corrigindo mais no 2º turno), relatado com o mesmo destaque. Um SINAL em (c) só
    conta como indício se o T padronizado da "Tecla indevida" (T dividido pelo desvio-padrão do desfecho entre seções)
    for no máximo um terço do T padronizado da correção.
C7. Calibração (200 cópias por caso, semente 20261110): k2' = k2 + Binomial(n2 - k2, 0,0357 x Phi x q x r2), com
    Phi = 0,25; 0,5 e 1 e q = 0,5 (letra); ao lado q = 0,25 e q = 0,10 com Phi = 1. Em cada cópia: T, ep, z. "Enxerga"
    = (T da cópia - T observado)/ep >= 3,3. Recuperação = (T médio das cópias - T observado)/(0,0357 x Phi x q).
    Também conto em quantas cópias o critério inteiro de SINAL dispara. Espelho plantado: a mesma taxa com (1 - r2).
    Inocentes plantadas com o mesmo total de correções de Phi = 0,25 e q = 0,5: J1 nível (taxa igual em todas as
    seções, "mais erro de início"); J2 idade (taxa proporcional à fração do eleitorado com 60 anos ou mais). Conto as
    cópias em que SINAL dispara e o deslocamento médio de T. Tempo (S8): cada correção plantada soma à tela de
    presidente Delta segundos, Delta = diferença média observada entre eleitores com e sem correção no 2º turno.
C8. Veredito da (c), nesta ordem: SEM PODER se o plantio de Phi = 0,25 com q = 0,5 for enxergado em menos de 95% das
    cópias ou a recuperação sair de 0,8 a 1,2; SINAL pela letra (T >= 0,0045 e z >= 3,3); SEM SINAL se T + 2,576 ep
    < 0,0045; INCONCLUSIVO no resto.
C9. Em votos: T de 0,0045 corresponde a Phi = 0,25 com q = 0,5. Phi máximo compatível = (T + 2,576 ep)/(0,0357 x q),
    para q = 0,5 (letra), 0,25 e 0,10; em votos de margem, Phi x 4.430.191. O valor de q (quantos reagiriam) é hipótese
    do desenho, não medida: digo o q mínimo para o qual uma troca visível que zera a margem (Phi = 1) ficaria excluída.
C10. Valor bruto de 2026 ao lado: c1 e c2 na AAS (média por seção e razão de totais, com erro), por terço de r2, e a
    cauda (seções com c2 de 5% ou mais e n2 de 50 ou mais, contra o mesmo no 1º turno). Nenhum outro ano entra neste
    teste: não há log de outro ano em disco e nenhum veredito depende de comparação com 2014, 2018 ou 2022.
CONTAGEM DE TESTES: 1 conjunto de identidades exatas (a), 1 contagem de impressões e etapas (b), 1 estimando com
veredito (c), mais placebos e leituras ao lado. Com z de 3,3 de um lado só a chance por teste é 0,05%.
"""
import os as _os, sys as _sys
_sys.path.insert(0, _os.path.dirname(_os.path.abspath(__file__)))
import collections, gzip, hashlib, io, json, math, os, pickle, re, sys, time, zipfile
import numpy as np

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
TRAB = '/home/user/trabalho-eleicao/adendo27/R27_C3'
FONTES = {'ant': '/home/user/trabalho-eleicao/amostra2t/arq',
          'aas': '/home/user/trabalho-eleicao/adendo27/aas/t2',
          'c1p': '/home/user/trabalho-eleicao/adendo27/aas/c1p_t2'}
URNA_DIRS = {'ant2': '/home/user/trabalho-eleicao/amostra2t/arq', 'ant1': '/home/user/trabalho-eleicao/amostra2t/arq1t',
             'aas2': '/home/user/trabalho-eleicao/adendo27/aas/t2', 'aas1': '/home/user/trabalho-eleicao/adendo27/aas/t1',
             'c1p2': '/home/user/trabalho-eleicao/adendo27/aas/c1p_t2',
             'ext2': '/home/user/trabalho-eleicao/adendo27/aas/ext_t2', 'ext1': '/home/user/trabalho-eleicao/adendo27/aas/ext_t1'}
PERFIL = '/home/user/trabalho-eleicao/adendo27/R27_A6/perfil_secao_2026_A6.json.gz'
DIAS = {'04/10/2026': '1', '25/10/2026': '2'}
MARGEM = 4430191; L2_NAC = 64256232; R2_NAC = 59826041; V_NAC = L2_NAC + R2_NAC; N_SECOES_2T = 499205
SEMENTE = 20261110
TAXA_VIRA = 0.0357          # fração dos votos de Flávio que, trocada, zera a margem (letra do desenho)
LIMIAR_T = 0.0045
UFS_GOV2 = ('AC', 'AM', 'DF', 'ES', 'RN', 'TO')
SAIDA_JSON = os.path.join(REPO, 'resultados', 'R27_C3_coerencia_e_reacao_na_tela.json')
SAIDA_TXT = os.path.join(REPO, 'resultados', 'R27_C3_coerencia_e_reacao_na_tela.txt')


def diz(*a):
    print(time.strftime('%H:%M:%S'), *a, flush=True)


def _js(o):
    if isinstance(o, (np.floating,)): return float(o)
    if isinstance(o, (np.integer,)): return int(o)
    if isinstance(o, (np.bool_,)): return bool(o)
    if isinstance(o, np.ndarray): return o.tolist()
    if isinstance(o, (set, frozenset)): return sorted(o)
    if isinstance(o, tuple): return list(o)
    raise TypeError(type(o))


def grava(nome, obj):
    with open(os.path.join(TRAB, nome), 'w') as f:
        json.dump(obj, f, ensure_ascii=False, indent=1, default=_js)


# ====================================================================================================================
# LEITOR DO LOG (sem voto por candidato)
# ====================================================================================================================
RX_ETAPA = re.compile(r'^Verificação de assinatura - Etapa \[(\d+)\] - \[([^\]]*)\] - \[([^\]]*)\]')
RX_MZS = re.compile(r'(?<![0-9])(\d{13})-')
RX_UF = re.compile(r'(?<![0-9a-z])o(\d{5})([a-z]{2})-')
RX_NUM = re.compile(r'\d+')
RX_NUMETAPA = re.compile(r'etapa \[\d+\]')
EVENTOS_INFO = ('Urna desligada', 'Mudança do estado da chave', 'Desligando a urna', 'Apresentada tela do reinício', 'Mesário confirmou o reinício',
                'Votação suspensa', 'Eleitor foi suspenso pelo mesário', 'Eleitor votou parcialmente', 'Modo de carga da UE', 'Contingência',
                'Recuperador', 'Solicitado título eleitoral para suspensão', 'Eleitor suspenso', 'Suspensão', 'Eleitor impedido',
                'Reinício', 'Urna desligada a pedido do aplicativo', 'Eleitor sem atividade', 'Eleitor não está votando',
                'Votação reiniciada', 'Dados recuperados', 'Início do procedimento de contingência', 'Término do processo de contingência')


def blocos(p):
    z = zipfile.ZipFile(p)
    for n in z.namelist():
        if n.startswith('logd'):
            yield n, z.read(n).decode('latin1').splitlines(), True
        elif n.endswith('.jez'):
            try:
                zz = zipfile.ZipFile(io.BytesIO(z.read(n)))
            except zipfile.BadZipFile:
                yield n, None, False
                continue
            for m in zz.namelist():
                if m.startswith('logd'):
                    yield n + '/' + m, zz.read(m).decode('latin1').splitlines(), False


def norm_caminho(c):
    c = RX_MZS.sub('<MZS>-', c)
    c = RX_UF.sub(lambda m: 'o' + m.group(1) + '<uf>-', c)
    return c


def _novo_dia():
    return {'n': 0, 'hab': 0, 'conf': collections.Counter(), 'susp': collections.Counter(), 'tipo': collections.Counter(),
            'dp': [], 'ip': [], 'cp': [], 'fl': [], 'dt': [], 'th': [], 'boot': [], 'ser': [],
            'telas': {}, 'ordem': collections.Counter(), 'orf': [], 'ev': collections.Counter(), 'series': set(),
            'pronta': [], 'enc': [], 'outra_secao': 0, 'comp_sem_hab': 0, 'n_principal': 0}


def _tela(R, rot, dur, ind, cor):
    T = R['telas'].get(rot)
    if T is None:
        T = R['telas'][rot] = [0, 0, 0, 0, 0, 0]  # eleitores, com >=1 correção, com >=1 tecla indevida, correções, teclas, segundos
    T[0] += 1; T[1] += 1 if cor else 0; T[2] += 1 if ind else 0; T[3] += cor; T[4] += ind; T[5] += dur


def _novo_boot(ib, ts, ser):
    return {'b': ib, 'ts': ts, 'ser': ser, 'ver': set(), 'mod': set(), 'uefi': set(), 'fase': set(), 'modo': set(), 'turno': set(),
            'id': None, 'runs': [], 'nruim': 0, 'v1': 0, 'v2': 0, 'v1o': 0, 'v2o': 0, 'apps': set(), 'pronta': 0, 'sim': 0,
            'scue_n': 0, 'scue_app': hashlib.sha1(), 'scue_dado': hashlib.sha1(), 'scue_app_n': 0, 'scue_dado_n': 0, 'conting_mv': 0}


def ler_pacote(arg):
    fonte, p = arg
    partes = p.split('/')
    uf, mun, zona, sec = partes[-5].upper(), int(partes[-4]), int(partes[-3]), int(partes[-2])
    chave = f'{uf}|{mun}|{zona}|{sec}'
    out = {'fonte': fonte, 'blocos': 0, 'boots': [], 'ruins': [], 'listas': {}, 'jez_ruim': 0, '1': None, '2': None,
           'n_scue': 0, 'scue_ruim': 0, 'uefi_serie': {}}
    dias = {'1': None, '2': None}
    try:
        bl = list(blocos(p))
    except Exception as e:
        return chave, {'fonte': fonte, 'erro': repr(e)}
    for nome, linhas, principal in bl:
        if linhas is None:
            out['jez_ruim'] += 1
            continue
        ib = out['blocos']; out['blocos'] += 1
        idm = idz = ids = None
        boot = None
        cur = None          # eleitor em curso
        pend_tipo = None; pend_man = False
        desde = set()       # eventos desde a última confirmação ou habilitação do eleitor em curso
        vt_bloco = {}       # votos oficiais computados neste bloco, por série, até a linha corrente
        ruins_ini = len(out['ruins'])
        nl = len(linhas)
        for il in range(nl):
            q = linhas[il].split('\t')
            if len(q) < 5:
                continue
            ts, niv, ser, ap, msg = q[0], q[1], q[2], q[3], q[4]
            if ap == 'LOGD' and msg.startswith('Início das operações do logd'):
                boot = _novo_boot(ib, ts, ser)
                out['boots'].append(boot)
                if cur is not None:
                    cur['cruzou'] = True
                desde.add('boot')
                continue
            if boot is None:
                boot = _novo_boot(ib, ts, ser); boot['sem_inicio'] = True
                out['boots'].append(boot)
            boot['apps'].add(ap)
            if msg.startswith('Verificação de assinatura'):
                m = RX_ETAPA.match(msg)
                if m and ap == 'GAP':
                    ne = int(m.group(1))
                    if ne == 1 or not boot['runs']:
                        boot['runs'].append({'ts': ts, 'et': [], 'nok': 0, 'v1': 0, 'v2': 0})
                    rn = boot['runs'][-1]
                    rn['et'].append((ne, norm_caminho(m.group(2)), m.group(3)))
                    if m.group(3) == 'SUCESSO': rn['nok'] += 1
                else:
                    out['n_scue'] += 1; boot['scue_n'] += 1
                    mm = norm_caminho(RX_NUMETAPA.sub('etapa [#]', msg)).encode()
                    if 'de aplicação' in msg:
                        boot['scue_app'].update(mm + b'\n'); boot['scue_app_n'] += 1
                    else:
                        boot['scue_dado'].update(mm + b'\n'); boot['scue_dado_n'] += 1
                if not msg.rstrip().endswith('[SUCESSO]'):
                    boot['nruim'] += 1
                    if ap != 'GAP': out['scue_ruim'] += 1
                    seg = []
                    for j in range(il + 1, min(nl, il + 400)):
                        qq = linhas[j].split('\t')
                        if len(qq) < 5: continue
                        if qq[4].startswith('Verificação de assinatura') and qq[4].rstrip().endswith('[SUCESSO]'): continue
                        seg.append(qq[0] + ' ' + qq[1] + ' ' + qq[3] + ' ' + qq[4][:150])
                        if len(seg) >= 14: break
                    out['ruins'].append({'b': ib, 'nboot': len(out['boots']) - 1, 'ts': ts, 'ser': ser, 'ap': ap, 'msg': msg[:300], 'depois': seg,
                                         'antes_boot': boot['v1'] + boot['v2'], 'antes_bloco': vt_bloco.get(ser, 0), 'antes_sim': boot['sim']})
                continue
            if ap == 'GAP' or ap == 'SCUE' or ap == 'ATUE':
                if ap != 'GAP' and msg.startswith(('Município: ', 'Zona Eleitoral: ', 'Seção Eleitoral: ')):
                    pass
                elif msg.startswith('Município: '):
                    try: idm = int(msg[11:])
                    except ValueError: idm = None
                    idz = ids = None
                elif msg.startswith('Zona Eleitoral: '):
                    try: idz = int(msg[16:])
                    except ValueError: idz = None
                elif msg.startswith('Seção Eleitoral: '):
                    try: ids = int(msg[17:])
                    except ValueError: ids = None
                    boot['id'] = (idm, idz, ids)
                elif msg.startswith('Identificação do Modelo de Urna'): boot['mod'].add(msg.split(': ')[-1])
                elif msg.startswith('Versão da aplicação'): boot['ver'].add(msg.split(': ', 1)[-1])
                elif msg.startswith('Versão do UEFI'):
                    boot['uefi'].add(msg.split(': ')[-1]); out['uefi_serie'].setdefault(ser, set()).add(msg.split(': ')[-1])
                elif msg.startswith('Versão d'):
                    boot['uefi'].add(msg[:60]); out['uefi_serie'].setdefault(ser, set()).add(msg[:60])
                elif msg.startswith('Fase da UE'): boot['fase'].add(msg.split(': ')[-1])
                elif msg.startswith('Modo de carga da UE'): boot['modo'].add(msg.split(' - ')[-1])
                elif msg.startswith('Turno da UE'): boot['turno'].add(msg.split(': ')[-1])
                elif msg.startswith(('Início do procedimento de contingência', 'Contingência de MV')): boot['conting_mv'] += 1
                if ap != 'GAP':
                    continue
            if ap == 'VOTA' and msg.startswith('Versão da aplicação'):
                boot['ver'].add(msg.split(': ', 1)[-1])
            d = DIAS.get(ts[:10])
            if d is None:
                if ap == 'VOTA' and msg == 'O voto do eleitor foi computado': boot['sim'] += 1
                continue
            if ap not in ('VOTA', 'GAP', 'INITJE', 'LOGD'):
                continue
            conhecida = idm is not None and idz is not None and ids is not None
            propria = (conhecida and (idm, idz, ids) == (mun, zona, sec)) or (not conhecida and principal)
            try:
                t = int(ts[11:13]) * 3600 + int(ts[14:16]) * 60 + int(ts[17:19])
            except ValueError:
                continue
            if dias[d] is None: dias[d] = _novo_dia()
            R = dias[d]
            if niv != 'INFO' or msg.startswith(EVENTOS_INFO):
                if propria:
                    R['ev'][niv + '|' + ap + '|' + RX_NUM.sub('#', msg)[:90]] += 1
                if msg.startswith(('Urna desligada', 'Mudança do estado da chave', 'Desligando a urna')): desde.add('desligada')
                elif msg.startswith(('Apresentada tela do reinício', 'Mesário confirmou o reinício')): desde.add('reinicio')
                elif msg.startswith(('Eleitor foi suspenso', 'Eleitor votou parcialmente', 'Solicitado título eleitoral para suspensão')): desde.add('suspenso')
                elif niv == 'ERRO': desde.add('erro')
            if ap != 'VOTA':
                continue
            if msg == 'Eleitor foi habilitado':
                if propria: R['hab'] += 1
                if cur is not None and propria:
                    R['orf'].append({'t': cur['ant'], 'cargos': list(cur['rot']), 'desde': sorted(desde), 'tipo': 'nova habilitação sem voto computado',
                                     'cruzou': cur.get('cruzou', False)})
                cur = {'th': t, 'ant': t, 'ind': 0, 'cor': 0, 'rot': [], 'dp': -1, 'ip': 0, 'cp': 0, 'sp': 0,
                       'tipo': pend_tipo, 'man': pend_man, 'nsen': 0, 'telas': []}
                pend_tipo = None; pend_man = False; desde = set()
            elif msg.startswith('Tipo de habilitação do eleitor'):
                pend_tipo = msg[msg.find('[') + 1:msg.find(']')]
            elif msg.startswith('Solicitação de dado pessoal do eleitor para habilitação manual') or (msg.startswith('Mesário') and msg.endswith('habilitou o eleitor')):
                pend_man = True
            elif msg == 'Tecla indevida pressionada':
                if cur is not None: cur['ind'] += 1
            elif msg.startswith('Eleitor corrigiu'):
                if cur is not None: cur['cor'] += 1
            elif msg.startswith('Voto confirmado para'):
                cargo = msg[msg.find('[') + 1:msg.find(']')]
                if propria: R['conf'][cargo] += 1
                if cur is None:
                    cur = {'th': -1, 'ant': t, 'ind': 0, 'cor': 0, 'rot': [], 'dp': -1, 'ip': 0, 'cp': 0, 'sp': 0, 'tipo': None, 'man': False,
                           'nsen': 0, 'telas': [], 'cruzou': True, 'sem_hab': True}
                rot = cargo
                if cargo == 'Senador':
                    cur['nsen'] += 1; rot = 'Senador#' + str(cur['nsen'])
                if rot in cur['rot']:
                    cur['repetiu'] = True
                dur = t - cur['ant']
                if cargo == 'Presidente':
                    cur['dp'] = dur; cur['ip'] = cur['ind']; cur['cp'] = cur['cor']
                cur['telas'].append((rot, dur, cur['ind'], cur['cor']))
                cur['rot'].append(rot); cur['ant'] = t; cur['ind'] = 0; cur['cor'] = 0; desde = set()
            elif msg.startswith('Atribuido voto nulo por suspensão'):
                cargo = msg[msg.find('[') + 1:msg.find(']')]
                if propria: R['susp'][cargo] += 1
                if cur is not None:
                    if cargo == 'Presidente':
                        cur['sp'] = 1
                        if not cur.get('susp_vista'):
                            cur['ip'] = cur['ind']; cur['cp'] = cur['cor']
                    cur['susp_vista'] = True
            elif msg == 'O voto do eleitor foi computado':
                if d == '1': boot['v1'] += 1
                else: boot['v2'] += 1
                vt_bloco[ser] = vt_bloco.get(ser, 0) + 1
                if boot['runs']:
                    boot['runs'][-1]['v' + d] += 1
                else:
                    boot['v_sem_run'] = boot.get('v_sem_run', 0) + 1
                if not propria:
                    R['outra_secao'] += 1
                    if d == '1': boot['v1o'] += 1
                    else: boot['v2o'] += 1
                else:
                    R['n'] += 1; R['series'].add(ser)
                    if principal: R['n_principal'] += 1
                    if cur is None:
                        R['comp_sem_hab'] += 1
                        R['dp'].append(-1); R['ip'].append(0); R['cp'].append(0); R['fl'].append(2); R['dt'].append(-1); R['th'].append(-1)
                    else:
                        tipo = cur['tipo']
                        f = cur['sp']
                        if cur.get('cruzou') or cur.get('repetiu') or cur.get('sem_hab'): f |= 2
                        if tipo != 'biométrica':
                            f |= 4 if cur['man'] else 8
                        if tipo is not None and tipo != 'biométrica': R['tipo']['outro:' + tipo] += 1
                        R['tipo']['B' if tipo == 'biométrica' else ('M' if cur['man'] else 'S')] += 1
                        R['dp'].append(cur['dp']); R['ip'].append(cur['ip']); R['cp'].append(cur['cp']); R['fl'].append(f)
                        R['dt'].append(t - cur['th'] if cur['th'] >= 0 else -1); R['th'].append(cur['th'])
                        if not (f & 2):
                            for rot, dur, ind, cor in cur['telas']:
                                _tela(R, rot, dur, ind, cor)
                        R['ordem'][' > '.join(cur['rot']) + (' (suspenso)' if cur.get('susp_vista') else '')] += 1
                        if cur.get('repetiu'):
                            R['orf'].append({'t': t, 'cargos': list(cur['rot']), 'desde': ['boot'] if cur.get('cruzou') else [],
                                             'tipo': 'cargo confirmado duas vezes na mesma sessão', 'cruzou': cur.get('cruzou', False)})
                    R['boot'].append(len(out['boots']) - 1)
                cur = None; desde = set()
            elif msg == 'Urna pronta para receber votos':
                boot['pronta'] += 1
                if propria: R['pronta'].append(t)
            elif msg.startswith('Inicio do Encerramento') or msg.startswith('Início do Encerramento'):
                if propria: R['enc'].append(t)
        for ru in out['ruins'][ruins_ini:]:
            bt = out['boots'][ru['nboot']]
            ru['votos_depois_no_boot'] = bt['v1'] + bt['v2'] - ru.pop('antes_boot')
            ru['votos_depois_no_bloco_mesma_serie'] = vt_bloco.get(ru['ser'], 0) - ru.pop('antes_bloco')
            ru['simulados_depois_no_boot'] = bt['sim'] - ru.pop('antes_sim')
        if cur is not None and cur['rot']:
            for d in ('2', '1'):
                if dias[d] is not None:
                    dias[d]['orf'].append({'t': cur['ant'], 'cargos': list(cur['rot']), 'desde': sorted(desde), 'tipo': 'fim do bloco sem voto computado',
                                           'cruzou': cur.get('cruzou', False)})
                    break
    for bt in out['boots']:
        for rn in bt['runs']:
            et = rn.pop('et')
            seq = '\n'.join(f'{c}|{r}' for (n, c, r) in et)
            h = hashlib.sha1(seq.encode()).hexdigest()[:16]
            rn['eh'] = h; rn['ne'] = len(et)
            rn['ordem_ok'] = [n for (n, c, r) in et] == list(range(1, len(et) + 1))
            if et and h not in out['listas']:
                out['listas'][h] = [f'{c}|{r}' for (n, c, r) in et]
        bt['scue_app'] = bt['scue_app'].hexdigest()[:16] if bt['scue_app_n'] else None
        bt['scue_dado'] = bt['scue_dado'].hexdigest()[:16] if bt['scue_dado_n'] else None
        for k in ('ver', 'mod', 'uefi', 'fase', 'modo', 'turno', 'apps'):
            bt[k] = sorted(bt[k])
    out['uefi_serie'] = {k: sorted(v) for k, v in out['uefi_serie'].items()}
    for d in ('1', '2'):
        R = dias[d]
        if R is not None:
            R['series'] = sorted(R['series'])
            for k in ('conf', 'susp', 'tipo', 'ordem', 'ev'):
                R[k] = dict(R[k])
        out[d] = R
    return chave, out


def listar_logs(fonte, base):
    arqs = []
    for r, dd, f in os.walk(base):
        for n in f:
            if n.endswith('-log.jez'):
                arqs.append((fonte, os.path.join(r, n)))
    arqs.sort()
    return arqs


def cmd_extrair():
    from multiprocessing import Pool
    os.makedirs(TRAB, exist_ok=True)
    t0 = time.time(); res = {}; listas = {}
    for fonte, base in FONTES.items():
        arqs = listar_logs(fonte, base); R = {}
        with Pool(3) as pool:
            for i, (k, o) in enumerate(pool.imap_unordered(ler_pacote, arqs, chunksize=6)):
                for h, lst in o.pop('listas', {}).items():
                    listas.setdefault(h, lst)
                if k in R: k = k + '#dup' + str(i)
                R[k] = o
        res[fonte] = R
        diz(fonte, 'pacotes', len(arqs), 'secoes', len(R))
    with gzip.open(os.path.join(TRAB, 'logs_C3.pkl.gz'), 'wb', compresslevel=5) as f:
        pickle.dump({'res': res, 'listas': listas, 'quando': time.strftime('%Y-%m-%d %H:%M:%S UTC', time.gmtime()),
                     'segundos': time.time() - t0}, f, protocol=4)
    diz('fim', round(time.time() - t0), 's')


# ====================================================================================================================
# LEITOR DE BOLETIM E RDV (com votos)
# ====================================================================================================================
def _ler_urna(arg):
    import decodificar as D
    rot, pasta = arg
    partes = pasta.split('/')
    chave = f'{partes[-4].upper()}|{int(partes[-3])}|{int(partes[-2])}|{int(partes[-1])}'
    out = {'bu': None, 'rdv': None, 'erro': []}
    try:
        nomes = os.listdir(pasta)
    except OSError as e:
        return rot, chave, {'erro': [repr(e)]}
    for n in nomes:
        p = os.path.join(pasta, n)
        if n.endswith('-bu.dat') or n.endswith('-busa.dat'):
            try:
                b = D.ler_bu(p)
                cargos = {}
                for ide, rec in b['eleicoes'].items():
                    for cargo, c in rec['cargos'].items():
                        v = c['votos']
                        cargos[cargo] = {'ide': ide, 'apt': rec['apt'], 'comp': c['comp'],
                                         'cand': {int(nn): q for (t, nn), q in v.items() if t == 1 and nn is not None},
                                         'B': sum(q for (t, nn), q in v.items() if t == 2), 'N': sum(q for (t, nn), q in v.items() if t == 3),
                                         'outros_tipos': {int(t): q for (t, nn), q in v.items() if t not in (1, 2, 3)}}
                out['bu'] = {'cargos': cargos, 'versao': b.get('versao'), 'urna': b.get('urna'), 'arquivo': n,
                             'mun': b.get('mun'), 'zona': b.get('zona'), 'secao': b.get('secao')}
            except Exception as e:
                out['erro'].append('bu ' + n + ' ' + repr(e)[:120])
        elif n.endswith('-rdv.dat'):
            try:
                c = D.ler_rdv(p)
                cargos = {}
                for (ide, cod, tipo, dig), q in c.items():
                    r = cargos.setdefault(cod, {'ide': ide, 'cand': {}, 'B': 0, 'N4': 0, 'N6': 0, 'outros_tipos': {}, 'linhas': 0, 'nulo_dig': {}})
                    r['linhas'] += q
                    if tipo == 2:
                        try: r['cand'][int(dig)] = r['cand'].get(int(dig), 0) + q
                        except ValueError: r['outros_tipos']['2:' + dig] = q
                    elif tipo == 3: r['B'] += q
                    elif tipo == 4: r['N4'] += q
                    elif tipo == 6: r['N6'] += q
                    else: r['outros_tipos'][str(tipo)] = r['outros_tipos'].get(str(tipo), 0) + q
                out['rdv'] = {'cargos': cargos, 'arquivo': n}
            except Exception as e:
                out['erro'].append('rdv ' + n + ' ' + repr(e)[:120])
    return rot, chave, out


def cmd_urna():
    from multiprocessing import Pool
    t0 = time.time(); res = {}
    for rot, base in URNA_DIRS.items():
        pastas = []
        for r, dd, f in os.walk(base):
            if any(n.endswith('.dat') for n in f):
                pastas.append((rot, r))
        pastas.sort(); R = {}
        with Pool(3) as pool:
            for rr, k, o in pool.imap_unordered(_ler_urna, pastas, chunksize=20):
                R[k] = o
        res[rot] = R
        diz(rot, 'pastas', len(pastas), 'com bu', sum(1 for o in R.values() if o.get('bu')), 'com rdv', sum(1 for o in R.values() if o.get('rdv')),
            'erros', sum(1 for o in R.values() if o.get('erro')))
    with gzip.open(os.path.join(TRAB, 'urna_C3.pkl.gz'), 'wb', compresslevel=5) as f:
        pickle.dump({'res': res, 'quando': time.strftime('%Y-%m-%d %H:%M:%S UTC', time.gmtime())}, f, protocol=4)
    diz('fim', round(time.time() - t0), 's')


# ====================================================================================================================
# REGRESSÃO COM EFEITO FIXO E FUNÇÃO DE INFLUÊNCIA POR GRUPO
# ====================================================================================================================
def reg_fe(y, X, fe, cl, w=None, tira_unicos=False):
    """MQO com efeito fixo (within), peso e erro agrupado CR1. Devolve b, ep, IF por grupo de erro (G x k), n, G, e, ok."""
    y = np.asarray(y, float); X = np.asarray(X, float)
    if X.ndim == 1: X = X[:, None]
    n0 = len(y)
    w = np.ones(n0) if w is None else np.asarray(w, float)
    _, g = np.unique(fe, return_inverse=True)
    ok = np.ones(n0, bool)
    if tira_unicos:
        cnt = np.bincount(g); ok = cnt[g] >= 2
    y, X, w, g = y[ok], X[ok], w[ok], g[ok]
    _, g = np.unique(g, return_inverse=True)
    _, c = np.unique(np.asarray(cl)[ok], return_inverse=True)
    ng = g.max() + 1
    sw = np.bincount(g, weights=w, minlength=ng)
    Z = np.column_stack([y, X])
    Zd = np.empty_like(Z)
    for j in range(Z.shape[1]):
        m = np.bincount(g, weights=w * Z[:, j], minlength=ng) / np.where(sw > 0, sw, 1)
        Zd[:, j] = Z[:, j] - m[g]
    yd, Xd = Zd[:, 0], Zd[:, 1:]
    XtX = (Xd * w[:, None]).T @ Xd
    inv = np.linalg.pinv(XtX)
    b = inv @ ((Xd * w[:, None]).T @ yd)
    e = yd - Xd @ b
    G = c.max() + 1
    k = X.shape[1]
    S = np.zeros((G, k))
    for j in range(k):
        S[:, j] = np.bincount(c, weights=w * Xd[:, j] * e, minlength=G)
    IF = S @ inv.T
    N = len(yd)
    fator = G / (G - 1) * (N - 1) / (N - k) if G > 1 else float('nan')
    V = fator * IF.T @ IF
    return {'b': b, 'ep': np.sqrt(np.diag(V)), 'IF': IF, 'n': N, 'G': G, 'fator': fator, 'ok': ok, 'cl_idx': c, 'e': e, 'Xd': Xd, 'inv': inv, 'w': w}


def dif_coef(r2, j2, r1, j1):
    """t2 - t1 de duas regressões nas mesmas seções e nos mesmos grupos de erro (empilhadas, CR1)."""
    d = r2['IF'][:, j2] - r1['IF'][:, j1]
    fator = max(r2['fator'], r1['fator'])
    ep = math.sqrt(fator * float(d @ d))
    T = float(r2['b'][j2] - r1['b'][j1])
    return T, ep


# ====================================================================================================================
# BASE
# ====================================================================================================================
def carrega_tudo():
    import lib
    diz('lendo logs e urnas')
    with gzip.open(os.path.join(TRAB, 'logs_C3.pkl.gz'), 'rb') as f: LG = pickle.load(f)
    with gzip.open(os.path.join(TRAB, 'urna_C3.pkl.gz'), 'rb') as f: UR = pickle.load(f)
    diz('lendo base por seção, perfil e candidatos')
    S = lib.carregar(os.path.join(REPO, 'dados', 'secoes2026.json.gz'))
    P = lib.carregar(PERFIL)
    C = lib.carregar(os.path.join(REPO, 'dados', 'candidatos2026_1t.json.gz'))['secoes']
    return LG, UR, S, P, C


def binom_sup(n, alfa=0.05):
    return 1 - alfa ** (1.0 / n) if n > 0 else float('nan')


def clopper(k, n, alfa=0.05):
    from scipy.stats import beta
    lo = 0.0 if k == 0 else float(beta.ppf(alfa / 2, k, n - k + 1))
    hi = 1.0 if k == n else float(beta.ppf(1 - alfa / 2, k + 1, n - k))
    return lo, hi


# ====================================================================================================================
# PARTE (a): COERÊNCIA BU, RDV, LOG
# ====================================================================================================================
CARGO_ROT = {1: 'Presidente', 3: 'Governador'}


def identidades_secao(chave, bu, rdv, logdia, cargo):
    """Devolve dict de identidades para um cargo (1 presidente, 3 governador). Valores None = não aplicável (falta arquivo)."""
    out = {'I1': None, 'I2a': None, 'I2b': None, 'I3': None, 'I4': None, 'I5': None, 'dif': None, 'det': {}}
    rot = CARGO_ROT[cargo]
    b = bu['cargos'].get(cargo) if bu else None
    r = rdv['cargos'].get(cargo) if rdv else None
    if b is None and r is None:
        return None
    if b is not None and r is not None:
        nums = set(b['cand']) | set(r['cand'])
        dif = {n: b['cand'].get(n, 0) - r['cand'].get(n, 0) for n in nums}
        dB = b['B'] - r['B']; dN = b['N'] - (r['N4'] + r['N6'])
        out['dif'] = {'13': dif.get(13, 0), '22': dif.get(22, 0), 'outros': sum(v for n, v in dif.items() if n not in (13, 22)),
                      'abs_outros': sum(abs(v) for n, v in dif.items() if n not in (13, 22)), 'B': dB, 'N': dN}
        out['I1'] = (all(v == 0 for v in dif.values()) and dB == 0 and dN == 0 and not r['outros_tipos'] and not b['outros_tipos'])
        out['I2a'] = (r['linhas'] == b['comp'])
        out['det']['rdv_linhas'] = r['linhas']; out['det']['bu_comp'] = b['comp']
    if logdia is not None:
        n = logdia['n']; conf = logdia['conf'].get(rot, 0) if rot != 'Senador' else None
        susp = logdia['susp'].get(rot, 0)
        out['det'].update({'log_n': n, 'log_conf': conf, 'log_susp': susp})
        if b is not None:
            out['I2b'] = (n == b['comp']); out['I5'] = (b['N'] >= susp)
            out['det']['bu_N'] = b['N']
        out['I3'] = (conf + susp == n)
        if r is not None:
            out['I4'] = (r['N6'] == susp); out['det']['rdv_N6'] = r['N6']
    return out


def explica(ident, nome, logdia, pacote, cargo):
    rot = CARGO_ROT[cargo]
    if nome == 'I3':
        d = ident['det']; dif = d['log_conf'] + d['log_susp'] - d['log_n']
        orf = [o for o in logdia['orf'] if rot in o['cargos'] or any(x.startswith(rot) for x in o['cargos'])]
        bons = [o for o in orf if set(o['desde']) & {'boot', 'desligada', 'reinicio'}]
        if dif > 0 and len(orf) == dif and len(bons) == dif:
            return True, f'{dif} confirmação órfã com religamento, desligamento ou reinício no log'
        return False, f'diferença {dif}, órfãs {len(orf)}, com evento {len(bons)}'
    if nome == 'I2b':
        if len(logdia['series']) > 1: return True, 'mais de um número de série com voto no dia'
        if pacote.get('jez_ruim'): return True, 'log aninhado ilegível'
        if any('ontingência' in e for e in logdia['ev']): return True, 'linha de contingência no log do dia'
        return False, ''
    return False, ''


def parte_a(LG, UR):
    diz('parte (a)')
    out = {'conjuntos': {}, 'casos': [], 'calibracao': {}}
    # conjuntos: (rótulo, fonte de urna, fonte de log, dia do log)
    conj = [('ANT 2º turno', 'ant2', 'ant', '2'), ('AAS 2º turno', 'aas2', 'aas', '2'), ('AAS 1º turno (placebo e espelho)', 'aas1', 'aas', '1'),
            ('ANT 1º turno (só log, placebo)', None, 'ant', '1'),
            ('Lista P e C1, 2º turno (ao lado)', 'c1p2', 'c1p', '2'), ('Extensão 2º turno (ao lado, só BU e RDV)', 'ext2', None, None),
            ('Extensão 1º turno (ao lado, só BU e RDV)', 'ext1', None, None), ('ANT 1º turno, 80 boletins (ao lado, só BU e log)', 'ant1', 'ant', '1')]
    tabela = {}
    registros = {}
    for rot, fu, fl, dia in conj:
        U = UR['res'].get(fu, {}) if fu else {}
        Lg = LG['res'].get(fl, {}) if fl else {}
        chaves = sorted(set(U) | (set(Lg) if fu is None else set()))
        if fu is None:
            chaves = sorted(k for k in Lg if Lg[k].get(dia) and Lg[k][dia]['n'] > 0)
        T = {}
        regs = {}
        for cargo in (1, 3):
            cont = {nm: {'aplicavel': 0, 'violam': 0, 'explicadas': 0, 'sem_explicacao': 0} for nm in ('I1', 'I2a', 'I2b', 'I3', 'I4', 'I5')}
            soma = collections.Counter(); nsec = 0; com_rdv = 0; com_log = 0
            for k in chaves:
                u = U.get(k) or {}
                pac = Lg.get(k)
                ld = pac.get(dia) if (pac and dia and 'erro' not in pac) else None
                if ld is not None and ld['n'] == 0: ld = None
                # o log do 1º turno só vale para a seção se a urna do pacote do 2º turno tiver o dia 04/10 da própria seção
                idn = identidades_secao(k, u.get('bu'), u.get('rdv'), ld, cargo)
                if idn is None:
                    if ld is None: continue
                    if cargo == 3 and ld['conf'].get('Governador', 0) + ld['susp'].get('Governador', 0) == 0: continue
                    idn = identidades_secao(k, {'cargos': {}}, None, ld, cargo) or {'I1': None, 'I2a': None, 'I2b': None, 'I4': None, 'I5': None,
                                                                                    'I3': None, 'dif': None, 'det': {}}
                    rotc = CARGO_ROT[cargo]
                    idn = {'I1': None, 'I2a': None, 'I2b': None, 'I4': None, 'I5': None, 'dif': None,
                           'I3': (ld['conf'].get(rotc, 0) + ld['susp'].get(rotc, 0) == ld['n']),
                           'det': {'log_n': ld['n'], 'log_conf': ld['conf'].get(rotc, 0), 'log_susp': ld['susp'].get(rotc, 0)}}
                elif cargo == 3 and not ((u.get('bu') and 3 in u['bu']['cargos']) or (u.get('rdv') and 3 in u['rdv']['cargos'])):
                    continue
                nsec += 1
                if idn['dif'] is not None:
                    com_rdv += 1
                    for kk, v in idn['dif'].items(): soma[kk] += v
                if ld is not None: com_log += 1
                for nm in cont:
                    v = idn[nm]
                    if v is None: continue
                    cont[nm]['aplicavel'] += 1
                    if not v:
                        cont[nm]['violam'] += 1
                        ok, txt = explica(idn, nm, ld, pac, cargo) if ld is not None else (False, '')
                        cont[nm]['explicadas' if ok else 'sem_explicacao'] += 1
                        out['casos'].append({'conjunto': rot, 'secao': k, 'cargo': CARGO_ROT[cargo], 'identidade': nm, 'explicada': ok, 'explicacao': txt,
                                             'detalhe': idn['det'], 'dif': idn['dif'],
                                             'orfas': [o for o in (ld['orf'] if ld else []) if o['cargos']],
                                             'eventos_do_dia': {e: v for e, v in (ld['ev'] if ld else {}).items() if e.startswith(('ERRO', 'INFO|VOTA|Apresentada', 'INFO|VOTA|Mesário confirmou', 'INFO|INITJE', 'INFO|GAP|Cont'))}})
                regs[(k, cargo)] = idn
            T[CARGO_ROT[cargo]] = {'secoes': nsec, 'com_bu_e_rdv': com_rdv, 'com_log_do_dia': com_log, 'identidades': cont,
                                   'soma_BU_menos_RDV': dict(soma), 'a_favor_de_Lula_13_menos_22': soma.get('13', 0) - soma.get('22', 0)}
        tabela[rot] = T; registros[rot] = regs
    out['conjuntos'] = tabela
    # suspensões de presidente e teto do canal
    sus = {}
    for fl in ('ant', 'aas', 'c1p'):
        for dia in ('1', '2'):
            tot = 0; n = 0; secs = 0; lista = []
            for k, o in LG['res'][fl].items():
                if 'erro' in o or not o.get(dia) or o[dia]['n'] == 0: continue
                s = o[dia]['susp'].get('Presidente', 0); tot += s; n += o[dia]['n']; secs += 1; lista.append(s)
            a = np.array(lista, float)
            sus[f'{fl}_{dia}'] = {'secoes': secs, 'votos_no_log': n, 'suspensoes_de_presidente': tot,
                                  'media_por_secao': float(a.mean()) if secs else None,
                                  'ep_media': float(a.std(ddof=1) / math.sqrt(secs)) if secs > 1 else None}
    aas2 = sus['aas_2']
    out['suspensoes'] = sus
    out['teto_canal_suspensao_pais_2t'] = {'estimativa': aas2['media_por_secao'] * N_SECOES_2T,
                                           'ep': aas2['ep_media'] * N_SECOES_2T * math.sqrt(1 - aas2['secoes'] / N_SECOES_2T),
                                           'lim_sup_95_poisson_se_zero_ou_poucos': None,
                                           'em_votos_de_margem': aas2['media_por_secao'] * N_SECOES_2T,
                                           'fracao_da_margem': aas2['media_por_secao'] * N_SECOES_2T / MARGEM}
    # limite por regra de três, só AAS 2º turno, presidente
    Tp = tabela['AAS 2º turno']['Presidente']
    n_rdv = Tp['identidades']['I1']['aplicavel']
    viol_sem = sum(Tp['identidades'][nm]['sem_explicacao'] for nm in Tp['identidades'])
    p95 = binom_sup(n_rdv)
    med_v = V_NAC / N_SECOES_2T
    out['limite_AAS'] = {'n': n_rdv, 'violacoes_sem_explicacao': viol_sem, 'p_sup_95': p95, 'secoes_no_pais': p95 * N_SECOES_2T,
                         'votos_validos_nessas_secoes': p95 * N_SECOES_2T * med_v,
                         'pior_caso_votos_de_margem': 2 * p95 * N_SECOES_2T * med_v, 'Phi_pior_caso': 2 * p95 * N_SECOES_2T * med_v / MARGEM}
    # união das seções com RDV (ANT + AAS, sem repetir)
    ch_rdv = set(k for k, o in UR['res']['ant2'].items() if o.get('rdv') and o.get('bu')) | set(k for k, o in UR['res']['aas2'].items() if o.get('rdv') and o.get('bu'))
    ch_log = set(k for f in ('ant', 'aas') for k, o in LG['res'][f].items() if 'erro' not in o and o.get('2') and o['2']['n'] > 0)
    out['uniao'] = {'secoes_com_BU_e_RDV_2t': len(ch_rdv), 'secoes_com_log_2t': len(ch_log),
                    'repetidas_nas_duas_amostras': len(set(UR['res']['ant2']) & set(UR['res']['aas2'])),
                    'p_sup_95_se_fosse_aleatoria': binom_sup(len(ch_rdv))}
    # ----------------- calibração -----------------
    rng = np.random.default_rng(SEMENTE)
    U = UR['res']['aas2']; Lg = LG['res']['aas']
    chs = sorted(k for k, o in U.items() if o.get('bu') and o.get('rdv') and 1 in o['rdv']['cargos'] and o['rdv']['cargos'][1]['cand'].get(22, 0) > 0
                 and o['rdv']['cargos'][1]['cand'].get(13, 0) > 0)
    import copy
    def conta(mod_chaves, mexe, nomes):
        ap = collections.Counter(); fora = collections.Counter(); soma = 0
        alvo = set(mod_chaves)
        for k in sorted(U):
            u = U[k]
            if not (u.get('bu') and u.get('rdv')): continue
            pac = Lg.get(k); ld = pac.get('2') if pac and 'erro' not in pac else None
            bu, rdv, ldm = u['bu'], u['rdv'], ld
            if k in alvo:
                bu, rdv, ldm = mexe(copy.deepcopy(u['bu']), copy.deepcopy(u['rdv']), copy.deepcopy(ld))
            idn = identidades_secao(k, bu, rdv, ldm, 1)
            if idn is None: continue
            if idn['dif']: soma += idn['dif']['13'] - idn['dif']['22']
            for nm in nomes:
                if idn[nm] is False:
                    (ap if k in alvo else fora)[nm] += 1
        return {'plantadas': len(alvo), 'apontadas': dict(ap), 'apontadas_fora': dict(fora), 'soma_13_menos_22_BU_menos_RDV': soma}
    alvo = [chs[i] for i in rng.choice(len(chs), 30, replace=False)]
    def p1(bu, rdv, ld):
        c = rdv['cargos'][1]['cand']; c[22] -= 1; c[13] = c.get(13, 0) + 1; return bu, rdv, ld
    def p1e(bu, rdv, ld):
        c = rdv['cargos'][1]['cand']; c[13] -= 1; c[22] = c.get(22, 0) + 1; return bu, rdv, ld
    out['calibracao']['P1_um_voto_22_para_13_no_RDV_30_secoes'] = conta(alvo, p1, ('I1', 'I2a'))
    out['calibracao']['P1_espelho_um_voto_13_para_22_no_RDV_30_secoes'] = conta(alvo, p1e, ('I1', 'I2a'))
    # P2: conversão coerente de nulo por suspensão, nos dois turnos da AAS (o log fica como está)
    for dia, fu in (('2', 'aas2'), ('1', 'aas1')):
        Ud = UR['res'][fu]; n_alvo = 0; ap4 = 0; ap5 = 0; ap1 = 0
        for k, u in Ud.items():
            pac = Lg.get(k); ld = pac.get(dia) if pac and 'erro' not in pac else None
            if not (u.get('bu') and u.get('rdv') and ld and ld['n'] > 0): continue
            s = ld['susp'].get('Presidente', 0)
            if s == 0 or 1 not in u['rdv']['cargos'] or u['rdv']['cargos'][1]['N6'] == 0: continue
            n_alvo += 1
            bu = copy.deepcopy(u['bu']); rdv = copy.deepcopy(u['rdv'])
            bu['cargos'][1]['N'] -= 1; bu['cargos'][1]['cand'][13] = bu['cargos'][1]['cand'].get(13, 0) + 1
            rdv['cargos'][1]['N6'] -= 1; rdv['cargos'][1]['cand'][13] = rdv['cargos'][1]['cand'].get(13, 0) + 1
            idn = identidades_secao(k, bu, rdv, ld, 1)
            ap4 += idn['I4'] is False; ap5 += idn['I5'] is False; ap1 += idn['I1'] is False
        out['calibracao'][f'P2_conversao_coerente_de_nulo_por_suspensao_turno_{dia}'] = {
            'secoes_com_suspensao_de_presidente': n_alvo, 'I4_aponta': ap4, 'I5_aponta': ap5, 'I1_aponta': ap1,
            'nota': 'I1 não vê porque boletim e RDV mudam juntos; I5 só vê se não sobrar outro nulo; I4 (tipo 6 contra o log) vê todas'}
    # P3: um voto computado a menos no log
    comlog = [k for k in chs if Lg.get(k) and 'erro' not in Lg[k] and Lg[k].get('2') and Lg[k]['2']['n'] > 0]
    alvo3 = [comlog[i] for i in rng.choice(len(comlog), 30, replace=False)]
    def p3(bu, rdv, ld):
        ld['n'] -= 1; return bu, rdv, ld
    out['calibracao']['P3_um_voto_computado_a_menos_no_log_30_secoes'] = conta(alvo3, p3, ('I2b', 'I3'))
    # explicação inocente: ler só o log principal
    falsas = {}
    for fl, fu in (('ant', 'ant2'), ('aas', 'aas2')):
        f = 0; tot = 0
        for k, o in LG['res'][fl].items():
            if 'erro' in o or not o.get('2') or o['2']['n'] == 0: continue
            u = UR['res'][fu].get(k)
            if not (u and u.get('bu') and 1 in u['bu']['cargos']): continue
            tot += 1
            if o['2']['n_principal'] != u['bu']['cargos'][1]['comp']: f += 1
        falsas[fl] = {'secoes': tot, 'violacoes_falsas_de_I2b_lendo_so_o_log_principal': f}
    out['calibracao']['inocente_so_log_principal'] = falsas
    grava('parcial_a.json', out)
    return out


# ====================================================================================================================
# PARTE (b): IMPRESSÃO DIGITAL DO PROGRAMA
# ====================================================================================================================
def eh_programa(item):
    c = item.split('|')[0]
    return (not c.startswith('/dsk/')) or c.endswith('/chave/avusrchave.vst')


def impressoes(LG):
    """Uma linha por (fonte, seção, dia, corrida com voto próprio)."""
    Ls = LG['listas']; linhas = []
    for fl in ('ant', 'aas', 'c1p'):
        for k, o in LG['res'][fl].items():
            if 'erro' in o: continue
            uf = k.split('|')[0]
            for ib, bt in enumerate(o['boots']):
                for rn in bt['runs']:
                    for d in ('1', '2'):
                        proprios = rn['v' + d]
                        if not proprios: continue
                        lst = Ls[rn['eh']]
                        canon = tuple(sorted(lst))
                        prog = tuple(x for x in canon if eh_programa(x)); dados = tuple(x for x in canon if not eh_programa(x))
                        avp = tuple(x.split('|')[0].rsplit('/', 1)[-1] for x in lst if '/uenux/bin/avpart' in x)
                        uefi = tuple(o['uefi_serie'].get(bt['ser'], ['(sem linha de UEFI)']))
                        mod = tuple(bt['mod'])
                        FP = (tuple(bt['ver']), mod, uefi, tuple(bt['fase']), prog)
                        FC = FP + (dados,)
                        linhas.append({'fonte': fl, 'chave': k, 'uf': uf, 'dia': d, 'serie': bt['ser'], 'modelo': '+'.join(mod) or '(sem modelo)', 'ne': rn['ne'], 'nok': rn['nok'],
                                       'FP': FP, 'FC': FC, 'dados': dados, 'prog': prog, 'ordem_avpart': avp, 'eh': rn['eh'], 'votos': proprios,
                                       'ts': rn['ts'], 'modo': tuple(bt['modo']), 'conting_mv': bt.get('conting_mv', 0), 'ruim_no_boot': bt['nruim'],
                                       'id': bt['id'], 'seq_ok': rn['ordem_ok']})
    return linhas


def _h(obj):
    return hashlib.sha1(repr(obj).encode()).hexdigest()[:10]


def base_modelo(S, P, C, chaves):
    """Modelo base do D1 para as seções pedidas (as que estão em U e têm perfil). Devolve dict de arrays e a lista de chaves."""
    locs = collections.defaultdict(list)
    for k, s in S.items():
        if '2' in s:
            uf, mun, zona, sec = k.split('|')
            locs[(uf, mun, zona, s['2']['loc'])].append(int(sec))
    pos = {}
    for kk, v in locs.items():
        v.sort(); n = len(v)
        for i, sec in enumerate(v):
            pos[f'{kk[0]}|{kk[1]}|{kk[2]}|{sec}'] = 0.5 if n == 1 else i / (n - 1)
    cols = P['colunas']; ic = {c: i for i, c in enumerate(cols)}
    ks = []; rows = []; y = []; V = []
    for k in chaves:
        s = S.get(k)
        if not s or '1' not in s or '2' not in s or k.startswith('ZZ'): continue
        a, b = s['1'], s['2']
        if b['L'] + b['R'] < 30 or a['L'] + a['R'] <= 0 or a['comp'] <= 0 or a['apt'] <= 0 or b['apt'] <= 0: continue
        pf = P['secoes'].get(k)
        if not pf or pf[0] <= 0: continue
        cand = C.get(k, {})
        c1 = a['comp']
        o_resto = a['O'] - sum(cand.get(n, 0) for n in ('70', '14', '55'))
        tot = pf[0]
        x = [a['L'] / c1, a['R'] / c1, cand.get('70', 0) / c1, cand.get('14', 0) / c1, cand.get('55', 0) / c1, o_resto / c1, a['B'] / c1,
             1 - a['comp'] / a['apt'], (1 - b['comp'] / b['apt']) - (1 - a['comp'] / a['apt']),
             pf[ic['biometria']] / tot, pf[ic['mulheres']] / tot]
        x += [pf[ic[c]] / tot for c in ('i1617', 'i1824', 'i3544', 'i4559', 'i6069', 'i7079', 'i80m')]
        x += [pf[ic[c]] / tot for c in ('e2', 'e3', 'e4', 'e5', 'e6', 'e7', 'e8')]
        x += [math.log(b['apt']), pos.get(k, 0.5)]
        ks.append(k); rows.append(x); y.append(100.0 * b['L'] / (b['L'] + b['R'])); V.append(b['L'] + b['R'])
    return {'k': ks, 'X': np.array(rows, float), 'y': np.array(y, float), 'V': np.array(V, float),
            'uf': np.array([k.split('|')[0] for k in ks]), 'mun': np.array(['|'.join(k.split('|')[:2]) for k in ks]),
            'loc': np.array(['|'.join(k.split('|')[:3]) + '|' + str(S[k]['2']['loc']) for k in ks]),
            'L2': np.array([S[k]['2']['L'] for k in ks], float), 'R2': np.array([S[k]['2']['R'] for k in ks], float)}


def teste_indicador(B, D, fe='mun'):
    """b do indicador D no modelo base, efeito fixo fe, erro por município."""
    D = np.asarray(D, float)
    r = reg_fe(B['y'], np.column_stack([D, B['X']]), B[fe], B['mun'], w=B['V'], tira_unicos=True)
    Dd = r['Xd'][:, 0]
    if float((r['w'] * Dd * Dd).sum()) < 1e-9:
        return {'estimavel': False, 'n': int(r['n'])}
    b = float(r['b'][0]); ep = float(r['ep'][0])
    return {'estimavel': True, 'b': b, 'ep': ep, 'z': b / ep if ep > 0 else float('nan'), 'n': int(r['n']), 'municipios': int(r['G']),
            'urnas_com_contraste': int((np.abs(Dd) > 1e-12).sum())}


def parte_b(LG, UR, S, P, C):
    diz('parte (b)')
    out = {}
    linhas = impressoes(LG)
    # união: cada seção uma vez por dia (AAS vale nas repetidas); lista P fica ao lado
    aas_k = set(LG['res']['aas'])
    def conjunto(nome):
        if nome == 'UNI': return [l for l in linhas if l['fonte'] == 'aas' or (l['fonte'] == 'ant' and l['chave'] not in aas_k)]
        if nome == 'ANT': return [l for l in linhas if l['fonte'] == 'ant']
        if nome == 'AAS': return [l for l in linhas if l['fonte'] == 'aas']
        return [l for l in linhas if l['fonte'] == 'c1p']
    rot_fp = {}; rot_fc = {}
    def nome_fp(fp, d): return d.setdefault(fp, 'F' + _h(fp))
    tab = {}
    for nome in ('UNI', 'ANT', 'AAS', 'P'):
        for dia in ('2', '1'):
            L = [l for l in conjunto(nome) if l['dia'] == dia]
            por_mod = collections.defaultdict(lambda: {'urnas': 0, 'FP': collections.Counter(), 'FC': collections.Counter(), 'ordem': collections.Counter(),
                                                       'ne': collections.Counter(), 'nao_sucesso': 0, 'FC_por_uf': collections.defaultdict(collections.Counter)})
            for l in L:
                m = por_mod[l['modelo']]
                m['urnas'] += 1; m['FP'][nome_fp(l['FP'], rot_fp)] += 1; m['FC'][nome_fp(l['FC'], rot_fc)] += 1
                m['ordem'][l['ordem_avpart']] += 1; m['ne'][l['ne']] += 1
                m['nao_sucesso'] += (l['nok'] != l['ne'])
                m['FC_por_uf'][l['uf']][nome_fp(l['FC'], rot_fc)] += 1
            T = {}
            for mod, m in sorted(por_mod.items()):
                ufs_mais_de_uma = {uf: dict(c) for uf, c in m['FC_por_uf'].items() if len(c) > 1}
                T[mod] = {'corridas_com_voto': m['urnas'], 'FP_distintas': len(m['FP']), 'FP': dict(m['FP']), 'FC_distintas_no_pais': len(m['FC']), 'FC': dict(m['FC']),
                          'ordens_distintas_dos_avpart': len(m['ordem']), 'etapas_por_corrida': {str(a): b for a, b in m['ne'].items()},
                          'corridas_com_etapa_sem_SUCESSO': m['nao_sucesso'], 'UFs_com_mais_de_uma_FC': ufs_mais_de_uma}
            tab[f'{nome}_dia{dia}'] = T
    out['contagem'] = tab
    # descrição de cada FC distinta (UNI + P, dia 2 e 1)
    desc = {}
    ref = {}
    for l in linhas:
        nm = nome_fp(l['FC'], rot_fc)
        d = desc.setdefault(nm, {'modelo': l['modelo'], 'versao': list(l['FP'][0]), 'uefi': list(l['FP'][2]), 'fase': list(l['FP'][3]),
                                 'n_pacotes_programa': len(l['prog']), 'n_pacotes_dados': len(l['dados']), 'dados': list(l['dados']),
                                 'FP': nome_fp(l['FP'], rot_fp), 'corridas': 0, 'ufs': collections.Counter(), 'conting_mv': 0, 'exemplos': []})
        d['corridas'] += 1; d['ufs'][l['uf']] += 1; d['conting_mv'] += 1 if l['conting_mv'] else 0
        if len(d['exemplos']) < 3: d['exemplos'].append(f"{l['fonte']} {l['chave']} dia {l['dia']} série {l['serie']} {l['ts']}")
    # maioria de dados por modelo, para dizer o que sobra e o que falta
    for mod in set(d['modelo'] for d in desc.values()):
        cands = [(d['corridas'], nm) for nm, d in desc.items() if d['modelo'] == mod]
        ref[mod] = max(cands)[1]
    for nm, d in desc.items():
        base = collections.Counter(desc[ref[d['modelo']]]['dados']); eu = collections.Counter(d['dados'])
        d['a_mais_que_a_maioria'] = sorted((eu - base).elements()); d['a_menos_que_a_maioria'] = sorted((base - eu).elements())
        d['ufs'] = dict(d['ufs']); d['e_a_maioria_do_modelo'] = (nm == ref[d['modelo']])
    for d in desc.values():
        del d['dados']
    out['FC_descricao'] = desc
    out['FP_descricao'] = {}
    for l in linhas:
        nm = nome_fp(l['FP'], rot_fp)
        if nm not in out['FP_descricao']:
            out['FP_descricao'][nm] = {'modelo': l['modelo'], 'versao': list(l['FP'][0]), 'uefi': list(l['FP'][2]), 'fase': list(l['FP'][3]), 'pacotes_de_programa': list(l['prog'])}
    # classificação das variantes de FC (B2), na UNI, dia 2
    L2 = [l for l in conjunto('UNI') if l['dia'] == '2']
    por_uf_mod = collections.defaultdict(collections.Counter)
    for l in L2: por_uf_mod[(l['modelo'], l['uf'])][nome_fp(l['FC'], rot_fc)] += 1
    fc_ufs = collections.defaultdict(set)
    for l in L2: fc_ufs[nome_fp(l['FC'], rot_fc)].add(l['uf'])
    variantes = []
    for (mod, uf), c in sorted(por_uf_mod.items()):
        if len(c) > 1:
            maior = c.most_common(1)[0][0]
            for nm, q in c.items():
                if nm == maior: continue
                exs = [l for l in L2 if l['modelo'] == mod and l['uf'] == uf and nome_fp(l['FC'], rot_fc) == nm]
                variantes.append({'modelo': mod, 'uf': uf, 'FC': nm, 'urnas': q, 'maioria_da_uf': maior,
                                  'explicada_por_contingencia_de_midia_no_log': all(e['conting_mv'] > 0 for e in exs),
                                  'a_menos': desc[nm]['a_menos_que_a_maioria'], 'a_mais': desc[nm]['a_mais_que_a_maioria'],
                                  'secoes': [f"{e['chave']} série {e['serie']} {e['ts']} votos {e['votos']}" for e in exs]})
    out['variantes_dentro_de_UF_UNI_2t'] = variantes
    n_mod = collections.Counter(l['modelo'] for l in L2)
    fp_por_mod = collections.defaultdict(set)
    for l in L2: fp_por_mod[l['modelo']].add(nome_fp(l['FP'], rot_fp))
    out['FP_por_modelo_UNI_2t'] = {m: {'urnas': n_mod[m], 'FP_distintas': len(v)} for m, v in fp_por_mod.items()}
    fc_pais = collections.defaultdict(collections.Counter)
    for l in L2: fc_pais[l['modelo']][nome_fp(l['FC'], rot_fc)] += 1
    out['FC_por_modelo_no_pais_UNI_2t'] = {m: dict(c) for m, c in fc_pais.items()}
    variantes_uf = []
    for mod, c in fc_pais.items():
        maior = c.most_common(1)[0][0]
        for nm, q in c.items():
            if nm == maior: continue
            ufs = fc_ufs[nm]
            inteira = all(len(por_uf_mod[(mod, uf)]) == 1 for uf in ufs)
            variantes_uf.append({'modelo': mod, 'FC': nm, 'urnas': q, 'ufs': sorted(ufs), 'coincide_com_UF_inteira': inteira,
                                 'a_mais': desc[nm]['a_mais_que_a_maioria'], 'a_menos': desc[nm]['a_menos_que_a_maioria']})
    out['variantes_no_pais_UNI_2t'] = variantes_uf
    # etapas sem SUCESSO
    ruins = []
    for fl in ('ant', 'aas', 'c1p'):
        for k, o in LG['res'][fl].items():
            if 'erro' in o: continue
            for ru in o['ruins']:
                bt = o['boots'][ru['nboot']]
                depois_serie = sum(b['v1'] + b['v2'] for i, b in enumerate(o['boots']) if b['ser'] == ru['ser'] and (b['b'], i) > (bt['b'], ru['nboot']))
                ruins.append({'fonte': fl, 'secao': k, 'quando': ru['ts'], 'serie': ru['ser'], 'aplicativo': ru['ap'], 'linha': ru['msg'],
                              'no_dia_de_votacao': ru['ts'][:10] in DIAS,
                              'votos_oficiais_depois_na_mesma_ligacao': ru['votos_depois_no_boot'],
                              'votos_oficiais_depois_no_mesmo_bloco_mesma_serie': ru['votos_depois_no_bloco_mesma_serie'],
                              'votos_oficiais_da_mesma_serie_em_ligacoes_posteriores_do_pacote': depois_serie,
                              'o_que_veio_depois': ru['depois'],
                              'series_que_computaram_os_votos_da_secao': {d: (o[d]['series'] if o.get(d) else []) for d in ('1', '2')}})
    out['etapas_sem_SUCESSO'] = ruins
    out['corridas_do_dia_com_etapa_sem_SUCESSO_e_voto'] = [f"{l['fonte']} {l['chave']} dia {l['dia']}" for l in linhas if l['nok'] != l['ne']]
    out['votos_em_ligacao_sem_corrida_de_verificacao'] = sum(b.get('v_sem_run', 0) for fl in ('ant', 'aas', 'c1p') for o in LG['res'][fl].values() if 'erro' not in o for b in o['boots'])
    # SCUE e versão do boletim (ao lado)
    scue = collections.defaultdict(collections.Counter)
    for fl in ('ant', 'aas'):
        for k, o in LG['res'][fl].items():
            if 'erro' in o: continue
            for bt in o['boots']:
                if bt['scue_n']:
                    scue['+'.join(bt['mod'])][(bt['scue_app'], bt['scue_app_n'])] += 1
    out['SCUE_resumo_da_lista_de_aplicacao_por_modelo'] = {m: {f'{h} ({n} linhas)': q for (h, n), q in c.items()} for m, c in scue.items()}
    vb = collections.Counter()
    for fu in ('ant2', 'aas2', 'aas1', 'c1p2', 'ext2'):
        for k, u in UR['res'].get(fu, {}).items():
            if u.get('bu'): vb[(fu, u['bu']['versao'])] += 1
    out['versao_no_cabecalho_do_boletim'] = {f'{a}: {b}': q for (a, b), q in vb.items()}
    grava('parcial_b_contagem.json', out)
    # ----------------- resíduo de y -----------------
    diz('parte (b): modelo base')
    uni2 = {l['chave']: l for l in L2}
    B = base_modelo(S, P, C, sorted(uni2))
    out['modelo_base'] = {'secoes': len(B['k']), 'municipios': int(len(set(B['mun']))), 'ufs': int(len(set(B['uf'])))}
    testes = []
    for v in variantes:
        pass
    # variantes dentro de UF com 20 urnas ou mais
    cont_var = collections.Counter((v['modelo'], v['FC']) for v in variantes for _ in range(v['urnas']))
    for (mod, nm), q in cont_var.items():
        if q >= 20:
            D = np.array([1.0 if nome_fp(uni2[k]['FC'], rot_fc) == nm else 0.0 for k in B['k']])
            t = {fe: teste_indicador(B, D, fe) for fe in ('mun', 'loc', 'uf')}
            testes.append({'variante': nm, 'modelo': mod, 'urnas': q, 'testes': t})
    out['residuo_variantes_dentro_de_UF_com_20_ou_mais'] = testes
    # variantes de UF inteira: resíduo médio da UF sem efeito fixo, só AAS
    aasB = np.array([uni2[k]['fonte'] == 'aas' for k in B['k']])
    Xc = np.column_stack([np.ones(aasB.sum()), B['X'][aasB]])
    w = B['V'][aasB]
    bb = np.linalg.lstsq(Xc * np.sqrt(w)[:, None], B['y'][aasB] * np.sqrt(w), rcond=None)[0]
    res = B['y'][aasB] - Xc @ bb
    ufa = B['uf'][aasB]
    med_uf = {}
    for uf in sorted(set(ufa)):
        m = ufa == uf
        med_uf[uf] = {'n': int(m.sum()), 'residuo_medio_ponderado': float((w[m] * res[m]).sum() / w[m].sum())}
    out['residuo_medio_por_UF_AAS_sem_efeito_fixo'] = med_uf
    lado = []; ja = set()
    urnas_uf = collections.Counter()
    for v in variantes_uf:
        if v['coincide_com_UF_inteira']:
            for uf in v['ufs']: urnas_uf[uf] += v['urnas']
    for v in variantes_uf:
        if v['coincide_com_UF_inteira']:
            for uf in v['ufs']:
                if uf in med_uf and uf not in ja and urnas_uf[uf] >= 20:
                    ja.add(uf)
                    outros = np.array([x['residuo_medio_ponderado'] for u, x in med_uf.items() if u != uf])
                    val = med_uf[uf]['residuo_medio_ponderado']
                    lado.append({'variante': 'lista de dados própria da UF (todos os modelos)', 'urnas_na_UNI': urnas_uf[uf], 'uf': uf, 'residuo_medio_da_UF': val, 'media_das_outras_UFs': float(outros.mean()),
                                 'dp_entre_as_outras_UFs': float(outros.std(ddof=1)), 'distancia_em_dp': float((val - outros.mean()) / outros.std(ddof=1)),
                                 'posicao_entre_as_UFs': int(1 + (outros > val).sum()), 'ufs': int(len(med_uf)),
                                 'nota': 'não identificável: a variante é a própria UF; valor só descritivo'})
    out['variantes_de_UF_inteira_ao_lado'] = lado
    # B5: ordem dos avpart
    cl = collections.Counter((uni2[k]['modelo'], uni2[k]['ordem_avpart']) for k in B['k'])
    b5 = []
    for (mod, ordm), q in sorted(cl.items(), key=lambda x: -x[1]):
        if q >= 20:
            D = np.array([1.0 if (uni2[k]['modelo'], uni2[k]['ordem_avpart']) == (mod, ordm) else 0.0 for k in B['k']])
            # dentro do modelo: restringe às urnas do modelo
            m = np.array([uni2[k]['modelo'] == mod for k in B['k']])
            Bm = {kk: (vv[m] if isinstance(vv, np.ndarray) else [x for x, f in zip(vv, m) if f]) for kk, vv in B.items()}
            t = teste_indicador(Bm, D[m], 'mun')
            b5.append({'modelo': mod, 'ordem': ' '.join(ordm), 'urnas': q, **t})
    zs = [abs(x['z']) for x in b5 if x.get('estimavel')]
    out['B5_ordem_dos_avpart'] = {'classes_testadas': len(zs), 'com_z_3_3_ou_mais': int(sum(z >= 3.3 for z in zs)), 'com_z_2_ou_mais': int(sum(z >= 2 for z in zs)),
                                  'esperado_por_acaso_z_2': 0.0455 * len(zs), 'esperado_por_acaso_z_3_3': 0.00097 * len(zs),
                                  'maior_z': max(zs) if zs else None, 'classes': b5}
    grava('parcial_b_residuo.json', {k: out[k] for k in ('modelo_base', 'residuo_variantes_dentro_de_UF_com_20_ou_mais', 'variantes_de_UF_inteira_ao_lado', 'B5_ordem_dos_avpart')})
    # ----------------- calibração -----------------
    diz('parte (b): calibração')
    rng = np.random.default_rng(SEMENTE + 1)
    cal = {}
    # Q1: etapa trocada por ERRO em 30 urnas (na cópia das listas)
    L2all = [l for l in linhas if l['dia'] == '2' and l['fonte'] in ('ant', 'aas')]
    idx = rng.choice(len(L2all), 30, replace=False)
    apont = 0
    for i in idx:
        lst = list(LG['listas'][L2all[i]['eh']]); j = int(rng.integers(len(lst)))
        lst[j] = lst[j].rsplit('|', 1)[0] + '|ERRO'
        nok = sum(1 for x in lst if x.endswith('|SUCESSO'))
        apont += (nok != len(lst))
    cal['Q1_etapa_trocada_por_ERRO_em_30_urnas'] = {'plantadas': 30, 'apontadas': int(apont)}
    # Q2: FP minoritária de 25 urnas dentro de UFs, com troca de votos
    nB = len(B['k'])
    cnt_mun = collections.Counter(B['mun'])
    elegiveis = np.array([cnt_mun[m] >= 2 for m in B['mun']])
    ie = np.where(elegiveis)[0]
    res_q2 = {}
    for rot, f, sentido in (('inocente_sem_mover_voto', 0.0, 1), ('f_3,57%', 0.0357, 1), ('f_10%', 0.10, 1), ('f_30%', 0.30, 1), ('espelho_f_10%_de_Lula_para_Flavio', 0.10, -1)):
        zs = []; bs = []; nest = 0
        for rep in range(200):
            sel = rng.choice(ie, 25, replace=False)
            D = np.zeros(nB); D[sel] = 1
            L2c = B['L2'].copy(); R2c = B['R2'].copy()
            if f > 0:
                if sentido > 0:
                    m = rng.binomial(R2c[sel].astype(int), f); L2c[sel] += m; R2c[sel] -= m
                else:
                    m = rng.binomial(L2c[sel].astype(int), f); L2c[sel] -= m; R2c[sel] += m
            Bc = dict(B); Bc['y'] = 100.0 * L2c / (L2c + R2c)
            t = teste_indicador(Bc, D, 'mun')
            if t['estimavel']:
                nest += 1; zs.append(t['z']); bs.append(t['b'])
        zs = np.array(zs)
        res_q2[rot] = {'copias': 200, 'estimaveis': nest, 'b_medio': float(np.mean(bs)), 'z_medio': float(zs.mean()),
                       'fracao_com_z_3_3_ou_mais_em_modulo': float((np.abs(zs) >= 3.3).mean()),
                       'fracao_com_z_3_3_no_sentido_plantado': float(((zs * sentido) >= 3.3).mean())}
    cal['Q2_FP_minoritaria_de_25_urnas'] = res_q2
    out['calibracao'] = cal
    # limite em votos
    vistos = {}
    for l in conjunto('AAS'):
        if l['dia'] == '2': vistos[(l['chave'], l['serie'])] = l['modelo']
    nA = collections.Counter(vistos.values())
    ntot = len(set(k for k, _ in vistos))
    p95 = binom_sup(ntot); med_v = V_NAC / N_SECOES_2T
    out['limite_AAS'] = {'urnas_AAS_2t': ntot, 'urnas_por_modelo_contando_substitutas': dict(nA), 'p_sup_95': p95, 'urnas_no_pais': p95 * N_SECOES_2T,
                         'pior_caso_votos_de_margem': 2 * p95 * N_SECOES_2T * med_v, 'Phi_pior_caso': 2 * p95 * N_SECOES_2T * med_v / MARGEM}
    try:
        out['exploratorio_teste_conjunto_da_ordem_dos_avpart'] = exploratorio_ordem(B, uni2, linhas)
    except Exception as e:
        out['exploratorio_teste_conjunto_da_ordem_dos_avpart'] = {'erro': repr(e)}
    grava('parcial_b.json', out)
    return out


# ====================================================================================================================
# PARTE (c): REAÇÃO NA TELA
# ====================================================================================================================
def base_c(LG, S, P):
    cols = P['colunas']; ic = {c: i for i, c in enumerate(cols)}
    aas_k = set(LG['res']['aas'])
    linhas = []; fora = collections.Counter(); ext = []
    for fl in ('aas', 'ant'):
        for k, o in LG['res'][fl].items():
            if fl == 'ant' and k in aas_k:
                fora['repetida na AAS'] += 1; continue
            if 'erro' in o:
                fora['erro de leitura'] += 1; continue
            d1, d2 = o.get('1'), o.get('2')
            if not (d1 and d2 and d1['n'] > 0 and d2['n'] > 0):
                fora[f'{fl}: sem par (urna trocada sem o log do 1º turno)'] += 1; continue
            s = S.get(k)
            if not s or '1' not in s or '2' not in s:
                fora['sem a seção na base dos dois turnos'] += 1; continue
            a, b = s['1'], s['2']
            if k.startswith('ZZ'):
                fora[f'{fl}: exterior'] += 1; ext.append((fl, k)); continue
            if b['L'] + b['R'] < 30 or a['L'] + a['R'] <= 0:
                fora[f'{fl}: L2 + R2 abaixo de 30 ou L1 + R1 zero'] += 1; continue
            pf = P['secoes'].get(k)
            if not pf or pf[0] <= 0:
                fora[f'{fl}: sem perfil'] += 1; continue
            tot = pf[0]
            def dia(D):
                cp = np.array(D['cp']); ip = np.array(D['ip']); dp = np.array(D['dp']); fl_ = np.array(D['fl'])
                bom = (fl_ & 2) == 0
                tem = bom & (dp >= 0)
                return {'n': int(D['n']), 'k': int((cp[bom] > 0).sum()), 'i': int((ip[bom] > 0).sum()), 'kt': int(cp[bom].sum()),
                        'seg': float(np.minimum(dp[tem], 120).mean()) if tem.any() else float('nan'),
                        'm30': float((dp[tem] > 30).mean()) if tem.any() else float('nan'),
                        'seg_cor': float(np.minimum(dp[tem & (cp > 0)], 120).sum()), 'n_cor': int((tem & (cp > 0)).sum()),
                        'seg_sem': float(np.minimum(dp[tem & (cp == 0)], 120).sum()), 'n_sem': int((tem & (cp == 0)).sum()),
                        'telas': D['telas']}
            linhas.append({'k': k, 'fonte': fl, 'uf': k.split('|')[0], 'mun': '|'.join(k.split('|')[:2]),
                           'r1': a['R'] / (a['L'] + a['R']), 'r2': b['R'] / (b['L'] + b['R']), 'd1': dia(d1), 'd2': dia(d2),
                           'idade': [pf[ic[c]] / tot for c in ('i1617', 'i1824', 'i3544', 'i4559', 'i6069', 'i7079', 'i80m')],
                           'mais': [pf[ic['biometria']] / tot, pf[ic['mulheres']] / tot] + [pf[ic[c]] / tot for c in ('e2', 'e3', 'e4', 'e5', 'e6', 'e7', 'e8')],
                           'i60': (pf[ic['i6069']] + pf[ic['i7079']] + pf[ic['i80m']]) / tot,
                           'V2': b['L'] + b['R'], 'comp2': b['comp']})
    return linhas, dict(fora), ext


def arr(L, f):
    return np.array([f(l) for l in L], float)


def estima_T(L, y2, y1, c1ctl=True, peso=False, fe='uf', extra=False, so_dif=False, mais=None):
    """T = t2 - t1 pela letra. y2, y1: desfechos por seção (arrays). Devolve dict. mais: controles a mais (só no exploratório)."""
    r2 = arr(L, lambda l: l['r2']); r1 = arr(L, lambda l: l['r1'])
    idade = np.array([l['idade'] for l in L], float)
    ctl = idade if not extra else np.column_stack([idade, np.array([l['mais'] for l in L], float)])
    if mais is not None: ctl = np.column_stack([ctl, mais])
    fes = np.array([l[fe] for l in L]); cl = np.array([l['mun'] for l in L])
    w2 = arr(L, lambda l: l['d2']['n']) if peso else None
    w1 = arr(L, lambda l: l['d1']['n']) if peso else None
    tira = (fe != 'uf')
    if so_dif:
        R = reg_fe(y2 - y1, np.column_stack([r2, ctl]), fes, cl, w=w2, tira_unicos=tira)
        return {'T': float(R['b'][0]), 'ep': float(R['ep'][0]), 'z': float(R['b'][0] / R['ep'][0]), 'n': int(R['n']), 'municipios': int(R['G'])}
    X2 = np.column_stack([r2, y1, ctl]) if c1ctl else np.column_stack([r2, ctl])
    R2 = reg_fe(y2, X2, fes, cl, w=w2, tira_unicos=tira)
    R1 = reg_fe(y1, np.column_stack([r1, ctl]), fes, cl, w=w1, tira_unicos=tira)
    T, ep = dif_coef(R2, 0, R1, 0)
    return {'T': T, 'ep': ep, 'z': T / ep, 'lim_sup_99': T + 2.576 * ep, 'lim_inf_99': T - 2.576 * ep,
            't2': float(R2['b'][0]), 'ep_t2': float(R2['ep'][0]), 't1': float(R1['b'][0]), 'ep_t1': float(R1['ep'][0]),
            'l_coef_de_c1': float(R2['b'][1]) if c1ctl else None, 'n': int(R2['n']), 'municipios': int(R2['G'])}


class RapidoT:
    """Pré-computa a projeção para reestimar T muitas vezes mudando só y2 (calibração)."""
    def __init__(self, L, y1):
        r2 = arr(L, lambda l: l['r2']); r1 = arr(L, lambda l: l['r1'])
        idade = np.array([l['idade'] for l in L], float)
        self.fes = np.array([l['uf'] for l in L]); self.cl = np.array([l['mun'] for l in L])
        self.X2 = np.column_stack([r2, y1, idade]); self.R1 = reg_fe(y1, np.column_stack([r1, idade]), self.fes, self.cl)
        R = reg_fe(np.zeros(len(L)), self.X2, self.fes, self.cl)
        self.Xd = R['Xd']; self.inv = R['inv']; self.c = R['cl_idx']; self.G = R['G']; self.fator = max(R['fator'], self.R1['fator'])
        _, g = np.unique(self.fes, return_inverse=True); self.g = g; self.ng = g.max() + 1; self.cnt = np.bincount(g)
        self.A = self.inv @ self.Xd.T          # k x n
        self.if1 = self.R1['IF'][:, 0]; self.t1 = float(self.R1['b'][0])

    def T(self, y2):
        yd = y2 - (np.bincount(self.g, weights=y2, minlength=self.ng) / self.cnt)[self.g]
        b = self.A @ yd
        e = yd - self.Xd @ b
        s = np.zeros((self.G, self.Xd.shape[1]))
        for j in range(self.Xd.shape[1]):
            s[:, j] = np.bincount(self.c, weights=self.Xd[:, j] * e, minlength=self.G)
        if2 = (s @ self.inv.T)[:, 0]
        d = if2 - self.if1
        ep = math.sqrt(self.fator * float(d @ d))
        return float(b[0]) - self.t1, ep


def parte_c(LG, S, P):
    diz('parte (c)')
    out = {}
    Ltodas, fora, ext = base_c(LG, S, P)
    out['fora_do_universo'] = fora; out['exterior_pares'] = len(ext)
    amostras = {'UNI': Ltodas, 'ANT': [l for l in Ltodas if l['fonte'] == 'ant'], 'AAS': [l for l in Ltodas if l['fonte'] == 'aas']}
    # a ANT sozinha inclui as repetidas? Não: as 28 repetidas valem como AAS (decisão G1); digo o n.
    out['n'] = {k: len(v) for k, v in amostras.items()}
    f_c = lambda l, d: l[d]['k'] / l[d]['n']
    f_i = lambda l, d: l[d]['i'] / l[d]['n']
    f_kt = lambda l, d: l[d]['kt'] / l[d]['n']
    # ---------- valor bruto de 2026 ----------
    bruto = {}
    for nome, L in amostras.items():
        c1 = arr(L, lambda l: f_c(l, 'd1')); c2 = arr(L, lambda l: f_c(l, 'd2'))
        i1 = arr(L, lambda l: f_i(l, 'd1')); i2 = arr(L, lambda l: f_i(l, 'd2'))
        n1 = arr(L, lambda l: l['d1']['n']); n2 = arr(L, lambda l: l['d2']['n'])
        k1 = arr(L, lambda l: l['d1']['k']); k2 = arr(L, lambda l: l['d2']['k'])
        r2 = arr(L, lambda l: l['r2'])
        q = np.quantile(r2, [1 / 3, 2 / 3]); ter = np.digitize(r2, q)
        n = len(L)
        bruto[nome] = {'secoes': n, 'eleitores_1t': int(n1.sum()), 'eleitores_2t': int(n2.sum()),
                       'c1_media_das_secoes': float(c1.mean()), 'ep_c1': float(c1.std(ddof=1) / math.sqrt(n)),
                       'c2_media_das_secoes': float(c2.mean()), 'ep_c2': float(c2.std(ddof=1) / math.sqrt(n)),
                       'c2_menos_c1': float((c2 - c1).mean()), 'ep_dif': float((c2 - c1).std(ddof=1) / math.sqrt(n)),
                       'c1_razao_de_totais': float(k1.sum() / n1.sum()), 'c2_razao_de_totais': float(k2.sum() / n2.sum()),
                       'dp_c2_entre_secoes': float(c2.std(ddof=1)), 'dp_c1_entre_secoes': float(c1.std(ddof=1)),
                       'dp_r2_dentro_da_UF': float(reg_fe(r2, np.ones((n, 1)), np.array([l['uf'] for l in L]), np.array([l['mun'] for l in L]))['e'].std(ddof=1)),
                       'tecla_indevida_1t': float(i1.mean()), 'tecla_indevida_2t': float(i2.mean()),
                       'por_terco_de_r2': [{'terco': int(t + 1), 'r2_medio': float(r2[ter == t].mean()), 'secoes': int((ter == t).sum()),
                                            'c1': float(c1[ter == t].mean()), 'c2': float(c2[ter == t].mean()),
                                            'c2_menos_c1': float((c2 - c1)[ter == t].mean()), 'ep': float((c2 - c1)[ter == t].std(ddof=1) / math.sqrt((ter == t).sum()))} for t in range(3)],
                       'cauda_c2_5pct_ou_mais_com_n_50': int(((c2 >= 0.05) & (n2 >= 50)).sum()), 'cauda_c1_5pct_ou_mais_com_n_50': int(((c1 >= 0.05) & (n1 >= 50)).sum()),
                       'r2_medio_na_cauda_c2': float(r2[(c2 >= 0.05) & (n2 >= 50)].mean()) if ((c2 >= 0.05) & (n2 >= 50)).any() else None,
                       'r2_medio_geral': float(r2.mean())}
        seg2c = sum(l['d2']['seg_cor'] for l in L); n2c = sum(l['d2']['n_cor'] for l in L); seg2s = sum(l['d2']['seg_sem'] for l in L); n2s = sum(l['d2']['n_sem'] for l in L)
        seg1c = sum(l['d1']['seg_cor'] for l in L); n1c = sum(l['d1']['n_cor'] for l in L); seg1s = sum(l['d1']['seg_sem'] for l in L); n1s = sum(l['d1']['n_sem'] for l in L)
        bruto[nome]['tempo_tela_presidente_s'] = {'2t_com_correcao': seg2c / max(n2c, 1), '2t_sem_correcao': seg2s / max(n2s, 1),
                                                  '1t_com_correcao': seg1c / max(n1c, 1), '1t_sem_correcao': seg1s / max(n1s, 1),
                                                  'Delta_2t': seg2c / max(n2c, 1) - seg2s / max(n2s, 1)}
    out['bruto_2026'] = bruto
    grava('parcial_c_bruto.json', out)
    # ---------- estimativas ----------
    est = {}
    for nome, L in amostras.items():
        c1 = arr(L, lambda l: f_c(l, 'd1')); c2 = arr(L, lambda l: f_c(l, 'd2'))
        i1 = arr(L, lambda l: f_i(l, 'd1')); i2 = arr(L, lambda l: f_i(l, 'd2'))
        E = {'letra': estima_T(L, c2, c1)}
        E['S1_peso_n'] = estima_T(L, c2, c1, peso=True)
        E['S2_sem_controle_c1'] = estima_T(L, c2, c1, c1ctl=False)
        E['S3_primeira_diferenca'] = estima_T(L, c2, c1, so_dif=True)
        if nome != 'AAS':
            E['S4_efeito_fixo_de_municipio'] = estima_T(L, c2, c1, fe='mun')
        else:
            try: E['S4_efeito_fixo_de_municipio'] = estima_T(L, c2, c1, fe='mun')
            except Exception as e: E['S4_efeito_fixo_de_municipio'] = {'erro': repr(e)}
        E['S5_mais_controles'] = estima_T(L, c2, c1, extra=True)
        L21 = [l for l in L if l['uf'] not in UFS_GOV2]; L6 = [l for l in L if l['uf'] in UFS_GOV2]
        E['S6_21_UFs_so_presidente'] = estima_T(L21, arr(L21, lambda l: f_c(l, 'd2')), arr(L21, lambda l: f_c(l, 'd1')))
        if len(L6) > 50:
            E['S6_6_UFs_com_governador_antes'] = estima_T(L6, arr(L6, lambda l: f_c(l, 'd2')), arr(L6, lambda l: f_c(l, 'd1')))
        E['S7_correcoes_por_eleitor'] = estima_T(L, arr(L, lambda l: f_kt(l, 'd2')), arr(L, lambda l: f_kt(l, 'd1')))
        Lt = [l for l in L if not (math.isnan(l['d1']['seg']) or math.isnan(l['d2']['seg']))]
        E['S8_tempo_medio_s'] = estima_T(Lt, arr(Lt, lambda l: l['d2']['seg']), arr(Lt, lambda l: l['d1']['seg']))
        E['S8_fracao_mais_de_30_s'] = estima_T(Lt, arr(Lt, lambda l: l['d2']['m30']), arr(Lt, lambda l: l['d1']['m30']))
        # placebos
        Pl = {'tecla_indevida': estima_T(L, i2, i1)}
        Pl['tecla_indevida']['dp_do_desfecho'] = float(i2.std(ddof=1))
        Pl['tecla_indevida']['T_padronizado'] = Pl['tecla_indevida']['T'] / float(i2.std(ddof=1))
        E['letra']['dp_do_desfecho'] = float(c2.std(ddof=1)); E['letra']['T_padronizado'] = E['letra']['T'] / float(c2.std(ddof=1))
        # outras telas do 1º turno: gradiente em r1
        outras = {}
        for rot in ('Deputado Federal', 'Deputado Estadual', 'Deputado Distrital', 'Senador#1', 'Senador#2', 'Governador', 'Presidente'):
            Lr = [l for l in L if rot in l['d1']['telas'] and l['d1']['telas'][rot][0] > 0]
            if len(Lr) < 100: continue
            yr = arr(Lr, lambda l: l['d1']['telas'][rot][1] / l['d1']['telas'][rot][0])
            r1 = arr(Lr, lambda l: l['r1']); idade = np.array([l['idade'] for l in Lr], float)
            R = reg_fe(yr, np.column_stack([r1, idade]), np.array([l['uf'] for l in Lr]), np.array([l['mun'] for l in Lr]))
            outras[rot] = {'gradiente_em_r1': float(R['b'][0]), 'ep': float(R['ep'][0]), 'z': float(R['b'][0] / R['ep'][0]), 'n': int(R['n']), 'taxa_media': float(yr.mean())}
        Pl['telas_do_1t_gradiente_em_r1'] = outras
        Lg = [l for l in L if 'Governador' in l['d2']['telas'] and l['d2']['telas']['Governador'][0] > 0 and 'Governador' in l['d1']['telas'] and l['d1']['telas']['Governador'][0] > 0]
        if len(Lg) > 100:
            g2 = arr(Lg, lambda l: l['d2']['telas']['Governador'][1] / l['d2']['telas']['Governador'][0])
            g1 = arr(Lg, lambda l: l['d1']['telas']['Governador'][1] / l['d1']['telas']['Governador'][0])
            Pl['tela_de_governador_2t'] = estima_T(Lg, g2, g1)
        E['placebos'] = Pl
        est[nome] = E
    d = est['ANT']['letra']['T'] - est['AAS']['letra']['T']; ed = math.hypot(est['ANT']['letra']['ep'], est['AAS']['letra']['ep'])
    est['ANT_menos_AAS'] = {'diferenca': d, 'ep': ed, 'z': d / ed}
    out['estimativas'] = est
    grava('parcial_c_estimativas.json', out)
    # ---------- calibração ----------
    diz('parte (c): calibração')
    cal = {}
    for nome, L in amostras.items():
        rng = np.random.default_rng(SEMENTE + {'UNI': 10, 'ANT': 11, 'AAS': 12}[nome])
        c1 = arr(L, lambda l: f_c(l, 'd1')); c2 = arr(L, lambda l: f_c(l, 'd2'))
        n2 = arr(L, lambda l: l['d2']['n']).astype(int); k2 = arr(L, lambda l: l['d2']['k']).astype(int)
        r2 = arr(L, lambda l: l['r2']); i60 = arr(L, lambda l: l['i60'])
        RT = RapidoT(L, c1)
        T0, ep0 = RT.T(c2)
        assert abs(T0 - est[nome]['letra']['T']) < 1e-9 and abs(ep0 - est[nome]['letra']['ep']) < 1e-9, (T0, ep0, est[nome]['letra'])
        C = {'T_observado': T0, 'ep_observado': ep0}
        total_ref = float((n2 * TAXA_VIRA * 0.25 * 0.5 * r2).sum())
        casos = [('Phi_0,25_q_0,5', TAXA_VIRA * 0.25 * 0.5 * r2, TAXA_VIRA * 0.25 * 0.5, 1), ('Phi_0,5_q_0,5', TAXA_VIRA * 0.5 * 0.5 * r2, TAXA_VIRA * 0.5 * 0.5, 1),
                 ('Phi_1_q_0,5', TAXA_VIRA * 1 * 0.5 * r2, TAXA_VIRA * 0.5, 1), ('Phi_1_q_0,25', TAXA_VIRA * 0.25 * r2, TAXA_VIRA * 0.25, 1),
                 ('Phi_1_q_0,10', TAXA_VIRA * 0.10 * r2, TAXA_VIRA * 0.10, 1),
                 ('espelho_Phi_0,25_q_0,5_eleitor_de_Lula', TAXA_VIRA * 0.25 * 0.5 * (1 - r2), -TAXA_VIRA * 0.25 * 0.5, -1),
                 ('inocente_J1_nivel', np.full(len(L), total_ref / n2.sum()), None, 1),
                 ('inocente_J2_idade', i60 * total_ref / float((n2 * i60).sum()), None, 1)]
        for rot, taxa, plantado, sentido in casos:
            Ts = []; eps = []
            for rep in range(200):
                m = rng.binomial(n2 - k2, np.clip(taxa, 0, 1))
                T, ep = RT.T((k2 + m) / n2)
                Ts.append(T); eps.append(ep)
            Ts = np.array(Ts); eps = np.array(eps)
            r = {'copias': 200, 'T_medio': float(Ts.mean()), 'deslocamento_medio_de_T': float(Ts.mean() - T0), 'ep_medio': float(eps.mean()),
                 'fracao_SINAL_pela_letra': float(((Ts >= LIMIAR_T) & (Ts / eps >= 3.3)).mean()),
                 'fracao_SINAL_espelhado': float(((Ts <= -LIMIAR_T) & (Ts / eps <= -3.3)).mean()),
                 'correcoes_plantadas_em_media': float((n2 - k2) @ np.clip(taxa, 0, 1))}
            if plantado is not None:
                r['plantado'] = plantado
                r['fracao_enxerga_incremento_z_3_3'] = float((sentido * (Ts - T0) / eps >= 3.3).mean())
                r['recuperacao'] = float((Ts.mean() - T0) / plantado)
            C[rot] = r
        cal[nome] = C
    # tempo (S8), só UNI: Delta observado
    L = [l for l in amostras['UNI'] if not (math.isnan(l['d1']['seg']) or math.isnan(l['d2']['seg']))]
    delta = out['bruto_2026']['UNI']['tempo_tela_presidente_s']['Delta_2t']
    rng = np.random.default_rng(SEMENTE + 20)
    s1 = arr(L, lambda l: l['d1']['seg']); s2 = arr(L, lambda l: l['d2']['seg'])
    n2 = arr(L, lambda l: l['d2']['n']).astype(int); k2 = arr(L, lambda l: l['d2']['k']).astype(int); r2 = arr(L, lambda l: l['r2'])
    RTt = RapidoT(L, s1); T0, ep0 = RTt.T(s2)
    ct = {'Delta_s': delta, 'T_observado_s': T0, 'ep': ep0}
    for rot, phi in (('Phi_0,25_q_0,5', 0.25), ('Phi_1_q_0,5', 1.0)):
        Ts = []; eps = []
        for rep in range(200):
            m = rng.binomial(n2 - k2, TAXA_VIRA * phi * 0.5 * r2)
            T, ep = RTt.T(s2 + delta * m / n2); Ts.append(T); eps.append(ep)
        Ts = np.array(Ts); eps = np.array(eps)
        ct[rot] = {'plantado_s': TAXA_VIRA * phi * 0.5 * delta, 'deslocamento_medio': float(Ts.mean() - T0), 'fracao_enxerga_incremento_z_3_3': float(((Ts - T0) / eps >= 3.3).mean())}
    cal['tempo_UNI'] = ct
    out['calibracao'] = cal
    grava('parcial_c.json', out)
    return out


# ====================================================================================================================
# VEREDITOS E SAÍDA
# ====================================================================================================================
def vereditos(A, B, Cc):
    v = {}
    # (a): presidente, 2º turno, ANT e AAS
    viol = {'sem': 0, 'expl': 0, 'sinal': 0}
    for rot in ('ANT 2º turno', 'AAS 2º turno'):
        ids = A['conjuntos'][rot]['Presidente']['identidades']
        for nm, c in ids.items():
            viol['sem'] += c['sem_explicacao']; viol['expl'] += c['explicadas']
            if nm in ('I1', 'I4', 'I5'): viol['sinal'] += c['sem_explicacao']
    p1 = A['calibracao']['P1_um_voto_22_para_13_no_RDV_30_secoes']
    p2 = A['calibracao']['P2_conversao_coerente_de_nulo_por_suspensao_turno_1']
    plantio_ok = (p1['apontadas'].get('I1', 0) == 30 and not p1['apontadas_fora'].get('I1', 0)
                  and p2['I4_aponta'] == p2['secoes_com_suspensao_de_presidente'] and p2['secoes_com_suspensao_de_presidente'] > 0)
    if viol['sinal'] > 0: va = 'SINAL'
    elif viol['sem'] == 0 and plantio_ok: va = 'SEM SINAL'
    elif not plantio_ok and viol['sem'] == 0: va = 'SEM PODER'
    else: va = 'INCONCLUSIVO'
    v['a'] = {'veredito': va, 'violacoes_sem_explicacao': viol['sem'], 'violacoes_explicadas_por_evento_no_log': viol['expl'],
              'violacoes_que_dariam_SINAL': viol['sinal'], 'plantio_apontado': plantio_ok,
              'leitura_mais_estrita_zero_violacao_sem_descontar': 'SEM SINAL' if (viol['sem'] + viol['expl'] == 0 and plantio_ok) else ('SINAL' if viol['sinal'] else 'INCONCLUSIVO')}
    # (b)
    fp_ok = all(x['FP_distintas'] == 1 for x in B['FP_por_modelo_UNI_2t'].values())
    var_in = B['variantes_dentro_de_UF_UNI_2t']
    var_nao_expl = [x for x in var_in if not x['explicada_por_contingencia_de_midia_no_log']]
    corr_ruim = B['corridas_do_dia_com_etapa_sem_SUCESSO_e_voto']
    res_sinal = [t for t in B['residuo_variantes_dentro_de_UF_com_20_ou_mais'] if t['testes']['mun'].get('estimavel') and abs(t['testes']['mun']['z']) >= 3.3]
    q1 = B['calibracao']['Q1_etapa_trocada_por_ERRO_em_30_urnas']
    if corr_ruim or res_sinal: vb = 'SINAL'
    elif fp_ok and not var_nao_expl and q1['apontadas'] == 30: vb = 'SEM SINAL'
    else: vb = 'INCONCLUSIVO'
    estrita_fc = all(len(c) == 1 for c in B['FC_por_modelo_no_pais_UNI_2t'].values())
    estrita_etapa = [r for r in B['etapas_sem_SUCESSO'] if r['fonte'] in ('ant', 'aas') and (r['votos_oficiais_depois_na_mesma_ligacao'] or r['votos_oficiais_depois_no_mesmo_bloco_mesma_serie'] or r['votos_oficiais_da_mesma_serie_em_ligacoes_posteriores_do_pacote'])]
    q2 = B['calibracao']['Q2_FP_minoritaria_de_25_urnas']
    v['b'] = {'veredito': vb, 'FP_uma_por_modelo': fp_ok, 'variantes_de_FC_dentro_de_UF': len(var_in), 'das_quais_sem_explicacao': len(var_nao_expl),
              'corridas_do_dia_com_etapa_sem_SUCESSO_e_voto': len(corr_ruim), 'variantes_com_residuo_deslocado': len(res_sinal),
              'leitura_mais_estrita': {'FC_uma_por_modelo_no_pais': estrita_fc, 'urnas_com_etapa_sem_SUCESSO_em_qualquer_data_que_depois_receberam_voto': len(estrita_etapa),
                                       'veredito': 'SEM SINAL' if (vb == 'SEM SINAL' and estrita_fc and not estrita_etapa) else ('SINAL' if vb == 'SINAL' else 'INCONCLUSIVO')},
              'clausula_de_residuo': 'SEM PODER' if q2['f_30%']['fracao_com_z_3_3_no_sentido_plantado'] < 0.95 else 'com poder para f = 30% em 25 urnas',
              'poder_residuo_f_3,57%': q2['f_3,57%']['fracao_com_z_3_3_no_sentido_plantado'], 'poder_residuo_f_10%': q2['f_10%']['fracao_com_z_3_3_no_sentido_plantado'],
              'poder_residuo_f_30%': q2['f_30%']['fracao_com_z_3_3_no_sentido_plantado']}
    # (c)
    vc = {}
    for nome in ('UNI', 'ANT', 'AAS'):
        e = Cc['estimativas'][nome]['letra']; c = Cc['calibracao'][nome]['Phi_0,25_q_0,5']
        poder = c['fracao_enxerga_incremento_z_3_3'] >= 0.95 and 0.8 <= c['recuperacao'] <= 1.2
        if not poder: r = 'SEM PODER'
        elif e['T'] >= LIMIAR_T and e['z'] >= 3.3: r = 'SINAL'
        elif e['lim_sup_99'] < LIMIAR_T: r = 'SEM SINAL'
        else: r = 'INCONCLUSIVO'
        esp = (e['T'] <= -LIMIAR_T and e['z'] <= -3.3)
        ul = e['lim_sup_99']
        E = Cc['estimativas'][nome]
        pl = E['placebos']['tecla_indevida']
        placebo_limpo = abs(pl['T_padronizado']) <= abs(e['T_padronizado']) / 3
        cons = {k: E[k]['lim_sup_99'] for k in ('letra', 'S1_peso_n', 'S2_sem_controle_c1', 'S4_efeito_fixo_de_municipio', 'S5_mais_controles') if k in E and 'lim_sup_99' in E[k]}
        pior = max(cons, key=cons.get); ulc = max(cons[pior], 0.0)
        vc[nome] = {'veredito': r, 'T': e['T'], 'ep': e['ep'], 'z': e['z'], 'lim_sup_99': ul, 'SINAL_espelhado': esp,
                    'placebo_tecla_indevida_limpo_pela_regra_C6': placebo_limpo,
                    'T_padronizado_correcao': e['T_padronizado'], 'T_padronizado_tecla_indevida': pl['T_padronizado'],
                    'linha_de_base_que_esconderia_Phi_0,25': ul - LIMIAR_T,
                    'limite_mais_folgado_entre_as_especificacoes_fixadas': {'especificacao': pior, 'lim_sup_99': cons[pior],
                        'Phi_max': {q: ulc / (TAXA_VIRA * qq) for q, qq in (('q_0,5', 0.5), ('q_0,25', 0.25), ('q_0,10', 0.10))},
                        'votos_de_margem_max': {q: ulc / (TAXA_VIRA * qq) * MARGEM for q, qq in (('q_0,5', 0.5), ('q_0,25', 0.25), ('q_0,10', 0.10))},
                        'q_minimo_para_excluir_Phi_1': ulc / TAXA_VIRA,
                        'nota': 'apresentação decidida depois de ver o resultado; as especificações são as fixadas antes (letra, S1, S2, S4, S5)'},
                    'poder_Phi_0,25': c['fracao_enxerga_incremento_z_3_3'], 'recuperacao': c['recuperacao'],
                    'Phi_ponto_q_0,5': e['T'] / (TAXA_VIRA * 0.5), 'votos_de_margem_ponto_q_0,5': e['T'] / (TAXA_VIRA * 0.5) * MARGEM,
                    'Phi_max_99': {q: max(ul, 0) / (TAXA_VIRA * qq) for q, qq in (('q_0,5', 0.5), ('q_0,25', 0.25), ('q_0,10', 0.10))},
                    'votos_de_margem_max_99': {q: max(ul, 0) / (TAXA_VIRA * qq) * MARGEM for q, qq in (('q_0,5', 0.5), ('q_0,25', 0.25), ('q_0,10', 0.10))},
                    'q_minimo_para_excluir_Phi_1': max(ul, 0) / TAXA_VIRA}
    v['c'] = {'veredito': vc['UNI']['veredito'], 'por_amostra': vc,
              'espelho': 'SINAL ESPELHADO pela letra' if vc['UNI']['SINAL_espelhado'] else ('contraste no sentido contrário ao da tese, abaixo do limiar espelhado na UNI' if vc['UNI']['z'] <= -3.3 else 'sem contraste espelhado')}
    return v


def fmt(x, casas=4):
    if x is None: return 'n/d'
    if isinstance(x, float) and math.isnan(x): return 'n/d'
    s = f'{x:,.{casas}f}'
    return s.replace(',', 'X').replace('.', ',').replace('X', '.')


def fi(x):
    return f'{int(round(x)):,}'.replace(',', '.')


def escreve_txt(R):
    A, B, Cc, V = R['parte_a'], R['parte_b'], R['parte_c'], R['vereditos']
    o = []
    w = o.append
    w('R27_C3: COERÊNCIA INTERNA DA URNA E REAÇÃO DO ELEITOR NA TELA (teste D1.6 do desenho cego D1)')
    w('')
    w('Registro: Adendo 27 (commit 2748895, 10/11/2026 00:16:42 UTC), Onda C, item C3; mantido pelos Adendos 28 e 30 (commit a7218fb).')
    w('Critérios: campos do D1.6 em registro/adendo27/desenho_D1_proposta.json, aplicados pela letra. Decisões que o desenho não fixa:')
    w('docstring de scripts/analisar_R27_C3.py, gravado antes de qualquer conta com votos (cópia e SHA-256 em')
    w(f'{TRAB}/docstring_antes_de_rodar.*). Rodado em {R["quando"]}.')
    w('Amostras: ANT = amostra antiga (3.897 seções, não aleatória); AAS = amostra aleatória simples nova (3.000 seções); UNI = união.')
    w('Desvio mandado pela tarefa: em vez de baixar os 3.062 RDV que faltam na ANT, entram os 3.000 RDV da AAS.')
    w('')
    w('O QUE CADA PARTE PROVA E O QUE NÃO PROVA')
    w('  (a) e (b) usam só arquivos escritos pelo próprio programa da urna. Excluem alteração descuidada (um produto mexido e os outros não),')
    w('  programa trocado em parte das urnas que o verificador acusa, e mistura de versões. Um programa adulterado na origem, assinado com as')
    w('  chaves oficiais e coerente passa por (a) e (b) inteiras. Só (c) mede algo fora do controle do programa (o que o eleitor faz diante da')
    w('  tela), e só se a tela MOSTRASSE a troca; troca invisível passa por (c) também. E (c) supõe que o log registre a tecla CORRIGE.')
    w('')
    w('VEREDITO PELA LETRA')
    va, vb, vc = V['a'], V['b'], V['c']
    w(f'  (a) boletim contra RDV e log: {va["veredito"]}. Violações sem explicação: {va["violacoes_sem_explicacao"]}; explicadas por evento do próprio log: {va["violacoes_explicadas_por_evento_no_log"]}.')
    w(f'      Leitura mais estrita (zero violação sem descontar as explicadas): {va["leitura_mais_estrita_zero_violacao_sem_descontar"]}.')
    w(f'  (b) impressão digital do programa: {vb["veredito"]}. Leitura mais estrita (uma lista por modelo no país inteiro e nenhuma etapa sem SUCESSO')
    w(f'      em nenhuma data em urna que depois recebeu voto): {vb["leitura_mais_estrita"]["veredito"]}. Cláusula de resíduo: {vb["clausula_de_residuo"]}.')
    u = vc['por_amostra']['UNI']
    w(f'  (c) reação na tela: {vc["veredito"]} (UNI). T = t2 - t1 = {fmt(u["T"], 5)} (ep {fmt(u["ep"], 5)}, z {fmt(u["z"], 2)}); limite superior de 99% = {fmt(u["lim_sup_99"], 5)}; limiar 0,0045.')
    w(f'      ANT: {vc["por_amostra"]["ANT"]["veredito"]} (T {fmt(vc["por_amostra"]["ANT"]["T"], 5)}, ep {fmt(vc["por_amostra"]["ANT"]["ep"], 5)}). AAS: {vc["por_amostra"]["AAS"]["veredito"]} (T {fmt(vc["por_amostra"]["AAS"]["T"], 5)}, ep {fmt(vc["por_amostra"]["AAS"]["ep"], 5)}).')
    w(f'      ESPELHO, com o mesmo destaque: T é NEGATIVO. No 2º turno a correção na tela de presidente cresceu mais onde LULA é forte, não onde Flávio é forte.')
    w(f'      Critério espelhado (T de -0,0045 ou menos com z de -3,3 ou menos): UNI {"cumprido" if u["SINAL_espelhado"] else "não cumprido"} (T {fmt(u["T"], 5)}); AAS sozinha {"cumprido" if vc["por_amostra"]["AAS"]["SINAL_espelhado"] else "não cumprido"} (T {fmt(vc["por_amostra"]["AAS"]["T"], 5)}, z {fmt(vc["por_amostra"]["AAS"]["z"], 2)}); ANT {"cumprido" if vc["por_amostra"]["ANT"]["SINAL_espelhado"] else "não cumprido"}.')
    w(f'      Pela regra C6, fixada antes, esse contraste não conta como indício: o placebo da tecla indevida moveu {fmt(u["T_padronizado_tecla_indevida"], 2)} desvios-padrão contra {fmt(u["T_padronizado_correcao"], 2)} da correção (placebo {"limpo" if u["placebo_tecla_indevida_limpo_pela_regra_C6"] else "sujo"}).')
    w('')
    # ---------------- (a)
    w('PARTE (a). BOLETIM, RDV E LOG DA MESMA URNA')
    w('  Identidades: I1 BU = RDV (cada candidato, brancos, nulos); I2a linhas do RDV = comparecimento; I2b votos computados no log = comparecimento;')
    w('  I3 confirmações + nulos por suspensão no log = votos computados; I4 RDV tipo 6 = suspensões do log; I5 nulos do BU >= suspensões do log.')
    for rot, T in A['conjuntos'].items():
        for cargo in ('Presidente', 'Governador'):
            t = T[cargo]
            if t['secoes'] == 0: continue
            w(f'  {rot}, {cargo}: {fi(t["secoes"])} seções; com BU e RDV {fi(t["com_bu_e_rdv"])}; com log do dia {fi(t["com_log_do_dia"])}.')
            partes = []
            for nm in ('I1', 'I2a', 'I2b', 'I3', 'I4', 'I5'):
                c = t['identidades'][nm]
                if c['aplicavel'] == 0: continue
                partes.append(f'{nm} {c["violam"]} de {fi(c["aplicavel"])}' + (f' ({c["explicadas"]} explicadas, {c["sem_explicacao"]} sem explicação)' if c['violam'] else ''))
            w('     violam: ' + '; '.join(partes) + '.')
            if t['com_bu_e_rdv']:
                s = t['soma_BU_menos_RDV']
                w(f'     soma com sinal BU menos RDV: 13 {s.get("13", 0):+d}; 22 {s.get("22", 0):+d}; outros {s.get("outros", 0):+d}; brancos {s.get("B", 0):+d}; nulos {s.get("N", 0):+d}; a favor de Lula {t["a_favor_de_Lula_13_menos_22"]:+d}.')
    w('  Casos de presidente (todas as violações, com a explicação quando há):')
    if not [c for c in A['casos'] if c['cargo'] == 'Presidente']: w('     nenhum.')
    for c in A['casos']:
        if c['cargo'] != 'Presidente': continue
        d = c['detalhe']
        w(f'     {c["secao"]} ({c["conjunto"]}, {c["cargo"]}, {c["identidade"]}): ' + ('EXPLICADA: ' + c['explicacao'] if c['explicada'] else 'SEM EXPLICAÇÃO PELA REGRA: ' + c['explicacao'])
          + f'. Log: {d.get("log_conf")} confirmações, {d.get("log_susp")} suspensões, {d.get("log_n")} votos computados' + (f'; boletim {d.get("bu_comp")}' if d.get('bu_comp') is not None else '') + '.')
    ng = collections.Counter((c['conjunto'], c['identidade']) for c in A['casos'] if c['cargo'] == 'Governador')
    w('  Governador (placebo do desenho): I2b e I3, do jeito que escrevi antes de rodar, acusam ' + '; '.join(f'{k[0]} {k[1]} {v}' for k, v in sorted(ng.items())) + '.')
    w('  São seções com eleitores que só têm a tela de presidente (voto em trânsito fora da UF): o comparecimento de governador é menor que o de presidente.')
    w('  Erro meu de especificação do placebo, visto depois de rodar; a conferência corrigida está no EXPLORATÓRIO. I1, I2a, I4 e I5 de governador: zero violação.')
    s = A['suspensoes']
    w(f'  Nulos por suspensão de presidente no log: 2º turno ANT {s["ant_2"]["suspensoes_de_presidente"]} em {fi(s["ant_2"]["votos_no_log"])} votos; AAS {s["aas_2"]["suspensoes_de_presidente"]} em {fi(s["aas_2"]["votos_no_log"])};')
    w(f'  1º turno ANT {s["ant_1"]["suspensoes_de_presidente"]} em {fi(s["ant_1"]["votos_no_log"])}; AAS {s["aas_1"]["suspensoes_de_presidente"]} em {fi(s["aas_1"]["votos_no_log"])}.')
    t = A['teto_canal_suspensao_pais_2t']
    w(f'  Teto do canal "nulo por suspensão convertido" no 2º turno, pela AAS: {fi(t["estimativa"])} votos no país (ep {fi(t["ep"])}), {fmt(100 * t["fracao_da_margem"], 3)}% da margem.')
    l = A['limite_AAS']
    w(f'  Em votos (AAS, n = {fi(l["n"])}, {l["violacoes_sem_explicacao"]} violação sem explicação): no máximo {fmt(100 * l["p_sup_95"], 4)}% das seções ({fi(l["secoes_no_pais"])} no país) com incoerência interna,')
    w(f'  a 95%; pior caso, com todos os votos dessas seções trocados: {fi(l["pior_caso_votos_de_margem"])} votos de margem, Phi = {fmt(l["Phi_pior_caso"], 3)} ({fmt(100 * l["Phi_pior_caso"], 1)}% da margem).')
    un = A['uniao']
    w(f'  União das duas amostras: {fi(un["secoes_com_BU_e_RDV_2t"])} seções com BU e RDV, {fi(un["secoes_com_log_2t"])} com log ({un["repetidas_nas_duas_amostras"]} repetidas contadas uma vez).')
    cal = A['calibracao']
    p = cal['P1_um_voto_22_para_13_no_RDV_30_secoes']; pe = cal['P1_espelho_um_voto_13_para_22_no_RDV_30_secoes']
    w(f'  Calibração. P1, 1 voto do 22 para o 13 no RDV de 30 seções: I1 apontou {p["apontadas"].get("I1", 0)} de 30 e {p["apontadas_fora"].get("I1", 0)} fora; soma com sinal {p["soma_13_menos_22_BU_menos_RDV"]:+d} (plantado -60 em BU menos RDV).')
    w(f'  Espelho (13 para 22): I1 apontou {pe["apontadas"].get("I1", 0)} de 30; soma {pe["soma_13_menos_22_BU_menos_RDV"]:+d}.')
    for dia in ('2', '1'):
        p2 = cal[f'P2_conversao_coerente_de_nulo_por_suspensao_turno_{dia}']
        w(f'  P2, nulo por suspensão convertido de forma coerente em boletim e RDV, {dia}º turno: {p2["secoes_com_suspensao_de_presidente"]} seções com suspensão; I4 apontou {p2["I4_aponta"]}, I5 {p2["I5_aponta"]}, I1 {p2["I1_aponta"]}.')
    p3 = cal['P3_um_voto_computado_a_menos_no_log_30_secoes']
    w(f'  P3, um voto computado a menos no log em 30 seções: I2b apontou {p3["apontadas"].get("I2b", 0)}, I3 {p3["apontadas"].get("I3", 0)}; fora {sum(p3["apontadas_fora"].values())}.')
    ino = cal['inocente_so_log_principal']
    w(f'  Explicação inocente (contingência): lendo só o log principal, I2b acusaria {ino["ant"]["violacoes_falsas_de_I2b_lendo_so_o_log_principal"]} seções na ANT e {ino["aas"]["violacoes_falsas_de_I2b_lendo_so_o_log_principal"]} na AAS; somando o log aninhado, as que ficam estão na tabela.')
    w('')
    # ---------------- (b)
    w('PARTE (b). IMPRESSÃO DIGITAL DO PROGRAMA NA INICIALIZAÇÃO DO DIA')
    w('  Impressão de programa (FP) = versão, modelo, UEFI, fase e pacotes de programa verificados; completa (FC) = FP mais os pacotes de dados.')
    for nome in ('UNI', 'ANT', 'AAS', 'P'):
        for dia in ('2', '1'):
            T = B['contagem'][f'{nome}_dia{dia}']
            partes = [f'{mod}: {fi(t["corridas_com_voto"])} inicializações com voto, FP {t["FP_distintas"]}, FC {t["FC_distintas_no_pais"]}, ordens dos avpart {t["ordens_distintas_dos_avpart"]}, com etapa sem SUCESSO {t["corridas_com_etapa_sem_SUCESSO"]}' for mod, t in T.items()]
            w(f'  {nome}, dia do {dia}º turno: ' + '; '.join(partes) + '.')
    w('  Variantes da lista completa no país (UNI, 2º turno):')
    for x in B['variantes_no_pais_UNI_2t']:
        w(f'     {x["modelo"]} {x["FC"]}: {x["urnas"]} urnas, UFs {", ".join(x["ufs"])}; coincide com UF inteira: {"sim" if x["coincide_com_UF_inteira"] else "não"}; a mais {x["a_mais"]}; a menos {x["a_menos"]}.')
    w('  Variantes dentro de UF (UNI, 2º turno):')
    if not B['variantes_dentro_de_UF_UNI_2t']: w('     nenhuma.')
    for x in B['variantes_dentro_de_UF_UNI_2t']:
        w(f'     {x["modelo"]} {x["uf"]}: {x["urnas"]} urna(s); a menos {x["a_menos"]}; a mais {x["a_mais"]}; contingência de mídia no log: {"sim" if x["explicada_por_contingencia_de_midia_no_log"] else "não"}; {"; ".join(x["secoes"])}.')
    w('  Etapas de assinatura sem SUCESSO (todas as datas, GAP e SCUE):')
    for r in B['etapas_sem_SUCESSO']:
        w(f'     {r["secao"]} ({r["fonte"]}), {r["quando"]}, série {r["serie"]}: {r["linha"][:150]}')
        w(f'        votos oficiais depois: na mesma ligação {r["votos_oficiais_depois_na_mesma_ligacao"]}; no mesmo bloco pela mesma série {r["votos_oficiais_depois_no_mesmo_bloco_mesma_serie"]}; em ligações posteriores da mesma série {r["votos_oficiais_da_mesma_serie_em_ligacoes_posteriores_do_pacote"]}.')
        for x in r['o_que_veio_depois'][:4]: w('        depois: ' + x[:170])
    w(f'  Corridas do dia com etapa sem SUCESSO seguidas de voto: {len(B["corridas_do_dia_com_etapa_sem_SUCESSO_e_voto"])}. Votos em ligação sem corrida de verificação: {B["votos_em_ligacao_sem_corrida_de_verificacao"]}.')
    if B['residuo_variantes_dentro_de_UF_com_20_ou_mais']:
        for t in B['residuo_variantes_dentro_de_UF_com_20_ou_mais']:
            w(f'  Resíduo da variante {t["variante"]} ({t["urnas"]} urnas): ' + '; '.join(f'{fe}: b {fmt(x.get("b"), 3)} z {fmt(x.get("z"), 2)}' if x.get('estimavel') else f'{fe}: não estimável' for fe, x in t['testes'].items()))
    else:
        w('  Nenhuma variante minoritária com 20 urnas ou mais que varie dentro de UF: o teste de resíduo da letra não tem em que ser aplicado.')
    for x in B['variantes_de_UF_inteira_ao_lado']:
        w(f'  Ao lado, sem veredito ({x["uf"]}, lista de dados própria da UF, {x["urnas_na_UNI"]} urnas na UNI; não identificável): resíduo médio {fmt(x["residuo_medio_da_UF"], 2)} ponto; outras UFs média {fmt(x["media_das_outras_UFs"], 2)}, dp {fmt(x["dp_entre_as_outras_UFs"], 2)}; distância {fmt(x["distancia_em_dp"], 2)} dp; posição {x["posicao_entre_as_UFs"]} de {x["ufs"]}.')
    b5 = B['B5_ordem_dos_avpart']
    w(f'  Ao lado (ordem dos quatro pacotes avpart9x): {b5["classes_testadas"]} classes com 20 urnas ou mais; |z| >= 3,3 em {b5["com_z_3_3_ou_mais"]} (acaso: {fmt(b5["esperado_por_acaso_z_3_3"], 2)}); |z| >= 2 em {b5["com_z_2_ou_mais"]} (acaso: {fmt(b5["esperado_por_acaso_z_2"], 1)}); maior |z| {fmt(b5["maior_z"], 2)}.')
    w('  Lista de arquivos verificados pelo SCUE na carga (resumo da parte de aplicação), por modelo: ' + '; '.join(f'{m}: {len(c)} resumo(s)' for m, c in B['SCUE_resumo_da_lista_de_aplicacao_por_modelo'].items()) + '.')
    w('  Versão no cabeçalho do boletim: ' + '; '.join(f'{k} = {v}' for k, v in B['versao_no_cabecalho_do_boletim'].items()) + '.')
    q = B['calibracao']
    w(f'  Calibração. Q1, etapa trocada por [ERRO] em 30 urnas: apontadas {q["Q1_etapa_trocada_por_ERRO_em_30_urnas"]["apontadas"]} de 30.')
    for rot, x in q['Q2_FP_minoritaria_de_25_urnas'].items():
        w(f'  Q2 {rot}: b médio {fmt(x["b_medio"], 3)}; |z| >= 3,3 em {fmt(100 * x["fracao_com_z_3_3_ou_mais_em_modulo"], 1)}% das 200 cópias; no sentido plantado {fmt(100 * x["fracao_com_z_3_3_no_sentido_plantado"], 1)}%.')
    l = B['limite_AAS']
    w(f'  Em votos (AAS, {fi(l["urnas_AAS_2t"])} seções, uma só impressão de programa por modelo): no máximo {fmt(100 * l["p_sup_95"], 4)}% das urnas ({fi(l["urnas_no_pais"])} no país) com programa de')
    w(f'  impressão diferente, a 95%; pior caso {fi(l["pior_caso_votos_de_margem"])} votos de margem ({fmt(100 * l["Phi_pior_caso"], 1)}% da margem). Isso NÃO limita programa adulterado com a mesma impressão.')
    w('')
    # ---------------- (c)
    w('PARTE (c). REAÇÃO DO ELEITOR NA TELA DE PRESIDENTE')
    w(f'  Universo: pares com a mesma urna (ou o log do 1º turno no pacote), fora o exterior, L2 + R2 de 30 ou mais, com perfil. UNI {fi(Cc["n"]["UNI"])}; ANT {fi(Cc["n"]["ANT"])} (sem as repetidas, que valem como AAS); AAS {fi(Cc["n"]["AAS"])}.')
    w('  Fora do universo: ' + '; '.join(f'{k} {v}' for k, v in Cc['fora_do_universo'].items()) + '.')
    for nome in ('AAS', 'UNI', 'ANT'):
        b = Cc['bruto_2026'][nome]
        w(f'  Valor bruto de 2026, {nome}: c1 = {fmt(100 * b["c1_media_das_secoes"], 3)}% (ep {fmt(100 * b["ep_c1"], 3)}); c2 = {fmt(100 * b["c2_media_das_secoes"], 3)}% (ep {fmt(100 * b["ep_c2"], 3)}); c2 - c1 = {fmt(100 * b["c2_menos_c1"], 3)} ponto (ep {fmt(100 * b["ep_dif"], 3)});')
        w(f'     razão de totais {fmt(100 * b["c1_razao_de_totais"], 3)}% e {fmt(100 * b["c2_razao_de_totais"], 3)}%; tecla indevida {fmt(100 * b["tecla_indevida_1t"], 1)}% e {fmt(100 * b["tecla_indevida_2t"], 1)}%; dp de c2 entre seções {fmt(b["dp_c2_entre_secoes"], 4)}; dp de r2 dentro da UF {fmt(b["dp_r2_dentro_da_UF"], 3)}.')
        w('     por terço da fração de Flávio (r2): ' + '; '.join(f'r2 {fmt(t["r2_medio"], 2)}: c1 {fmt(100 * t["c1"], 3)}%, c2 {fmt(100 * t["c2"], 3)}%, c2 - c1 {fmt(100 * t["c2_menos_c1"], 3)} (ep {fmt(100 * t["ep"], 3)})' for t in b['por_terco_de_r2']) + '.')
        w(f'     cauda: seções com c2 de 5% ou mais {b["cauda_c2_5pct_ou_mais_com_n_50"]} (r2 médio {fmt(b["r2_medio_na_cauda_c2"], 3)}; geral {fmt(b["r2_medio_geral"], 3)}); com c1 de 5% ou mais {b["cauda_c1_5pct_ou_mais_com_n_50"]}.')
        tt = b['tempo_tela_presidente_s']
        w(f'     tempo na tela de presidente: 2º turno {fmt(tt["2t_sem_correcao"], 1)} s sem correção e {fmt(tt["2t_com_correcao"], 1)} s com; 1º turno {fmt(tt["1t_sem_correcao"], 1)} s e {fmt(tt["1t_com_correcao"], 1)} s.')
    w('  Estimativas (T = t2 - t1; erro por município):')
    for nome in ('UNI', 'ANT', 'AAS'):
        E = Cc['estimativas'][nome]; e = E['letra']
        w(f'  {nome}, letra: t2 = {fmt(e["t2"], 5)} (ep {fmt(e["ep_t2"], 5)}); t1 = {fmt(e["t1"], 5)} (ep {fmt(e["ep_t1"], 5)}); T = {fmt(e["T"], 5)} (ep {fmt(e["ep"], 5)}, z {fmt(e["z"], 2)}); IC99 {fmt(e["lim_inf_99"], 5)} a {fmt(e["lim_sup_99"], 5)}; coeficiente de c1 {fmt(e["l_coef_de_c1"], 3)}; n {fi(e["n"])}, municípios {fi(e["municipios"])}.')
        for rot in ('S1_peso_n', 'S2_sem_controle_c1', 'S3_primeira_diferenca', 'S4_efeito_fixo_de_municipio', 'S5_mais_controles', 'S6_21_UFs_so_presidente', 'S6_6_UFs_com_governador_antes', 'S7_correcoes_por_eleitor', 'S8_tempo_medio_s', 'S8_fracao_mais_de_30_s'):
            x = E.get(rot)
            if not x or 'erro' in x: continue
            w(f'     {rot}: T {fmt(x["T"], 5)} (ep {fmt(x["ep"], 5)}, z {fmt(x["z"], 2)}; n {fi(x["n"])})')
        pl = E['placebos']
        x = pl['tecla_indevida']
        w(f'     placebo tecla indevida: T {fmt(x["T"], 5)} (ep {fmt(x["ep"], 5)}, z {fmt(x["z"], 2)}); padronizado {fmt(x["T_padronizado"], 3)} contra {fmt(e["T_padronizado"], 3)} da correção.')
        w('     placebo, gradiente em r1 nas telas do 1º turno: ' + '; '.join(f'{rot} {fmt(y["gradiente_em_r1"], 5)} (z {fmt(y["z"], 1)}; taxa {fmt(100 * y["taxa_media"], 2)}%)' for rot, y in pl['telas_do_1t_gradiente_em_r1'].items()) + '.')
        if 'tela_de_governador_2t' in pl:
            x = pl['tela_de_governador_2t']
            w(f'     placebo tela de governador do 2º turno: T {fmt(x["T"], 5)} (ep {fmt(x["ep"], 5)}, z {fmt(x["z"], 2)}; n {fi(x["n"])}).')
    d = Cc['estimativas']['ANT_menos_AAS']
    w(f'  ANT menos AAS: {fmt(d["diferenca"], 5)} (ep {fmt(d["ep"], 5)}, z {fmt(d["z"], 2)}).')
    w('  Calibração por efeito plantado (200 cópias por caso; "enxerga" = incremento sobre o observado com z de 3,3 ou mais):')
    for nome in ('UNI', 'ANT', 'AAS'):
        C = Cc['calibracao'][nome]
        for rot in ('Phi_0,25_q_0,5', 'Phi_0,5_q_0,5', 'Phi_1_q_0,5', 'Phi_1_q_0,25', 'Phi_1_q_0,10', 'espelho_Phi_0,25_q_0,5_eleitor_de_Lula'):
            x = C[rot]
            w(f'     {nome} {rot}: plantado {fmt(x["plantado"], 5)}; deslocamento médio {fmt(x["deslocamento_medio_de_T"], 5)}; recuperação {fmt(x["recuperacao"], 2)}; enxerga em {fmt(100 * x["fracao_enxerga_incremento_z_3_3"], 1)}%; SINAL pela letra em {fmt(100 * x["fracao_SINAL_pela_letra"], 1)}%; SINAL espelhado em {fmt(100 * x["fracao_SINAL_espelhado"], 1)}%.')
        for rot in ('inocente_J1_nivel', 'inocente_J2_idade'):
            x = C[rot]
            w(f'     {nome} {rot}: deslocamento médio de T {fmt(x["deslocamento_medio_de_T"], 5)}; SINAL pela letra em {fmt(100 * x["fracao_SINAL_pela_letra"], 1)}% das cópias.')
    ct = Cc['calibracao']['tempo_UNI']
    w(f'  Tempo (S8, UNI): cada correção custa {fmt(ct["Delta_s"], 1)} s a mais; T do tempo {fmt(ct["T_observado_s"], 3)} s (ep {fmt(ct["ep"], 3)}); plantio Phi 0,25: deslocamento {fmt(ct["Phi_0,25_q_0,5"]["deslocamento_medio"], 3)} s, enxerga em {fmt(100 * ct["Phi_0,25_q_0,5"]["fracao_enxerga_incremento_z_3_3"], 1)}%; Phi 1: {fmt(ct["Phi_1_q_0,5"]["deslocamento_medio"], 3)} s, enxerga em {fmt(100 * ct["Phi_1_q_0,5"]["fracao_enxerga_incremento_z_3_3"], 1)}%.')
    w('  Em votos de margem:')
    for nome in ('UNI', 'ANT', 'AAS'):
        x = vc['por_amostra'][nome]; lf = x['limite_mais_folgado_entre_as_especificacoes_fixadas']
        w(f'     {nome}: T = {fmt(x["T"], 5)}; limite superior de 99% {fmt(x["lim_sup_99"], 5)}. ' + ('O intervalo inteiro fica abaixo de zero: nenhuma troca visível contra Flávio cabe nele, a menos que a linha de base inocente fosse de ' + fmt(x['linha_de_base_que_esconderia_Phi_0,25'], 4) + ' ou menos.' if x['lim_sup_99'] < 0 else f'Máximo a 99% com metade reagindo: {fi(x["votos_de_margem_max_99"]["q_0,5"])} votos de margem ({fmt(100 * x["Phi_max_99"]["q_0,5"], 1)}% da margem); um quarto reagindo {fi(x["votos_de_margem_max_99"]["q_0,25"])}; um décimo {fi(x["votos_de_margem_max_99"]["q_0,10"])}.'))
        w(f'        Limite mais folgado entre as especificações fixadas antes ({lf["especificacao"]}, 99% = {fmt(lf["lim_sup_99"], 5)}): metade reagindo {fi(lf["votos_de_margem_max"]["q_0,5"])} votos de margem ({fmt(100 * lf["Phi_max"]["q_0,5"], 1)}% da margem); um quarto {fi(lf["votos_de_margem_max"]["q_0,25"])} ({fmt(100 * lf["Phi_max"]["q_0,25"], 1)}%); um décimo {fi(lf["votos_de_margem_max"]["q_0,10"])} ({fmt(100 * lf["Phi_max"]["q_0,10"], 1)}%).')
        w(f'        Troca visível que zera a margem (Phi = 1) fica excluída se {fmt(100 * lf["q_minimo_para_excluir_Phi_1"], 1)}% ou mais dos atingidos apertassem CORRIGE.')
        w(f'        Leitura espelhada do ponto (troca visível CONTRA Lula, metade reagindo): Phi {fmt(-x["Phi_ponto_q_0,5"], 3)} = {fi(-x["votos_de_margem_ponto_q_0,5"])} votos de margem no sentido de Flávio; não conta como indício (placebo sujo, ver acima).')
    w('')
    if R.get('exploratorio'):
        X = R['exploratorio']
        w('EXPLORATÓRIO (feito depois de ver os resultados da primeira rodada; não entra em veredito)')
        w('  E1. Governador com a conferência corrigida (confirmações + suspensões de governador contra o comparecimento de governador):')
        for rot, g in X['governador'].items():
            w(f'     {rot}: {fi(g["secoes_com_governador_no_log"])} seções; {g["com_I3_de_governador_diferente"]} com diferença; {g["explicadas_por_sessoes_so_de_presidente_no_log"]} fecham com as sessões só de presidente do próprio log ({fi(g["eleitores_so_de_presidente"])} eleitores); boletim fecha em {g["boletim_fecha_com_confirmacoes_mais_suspensoes"]} de {g["com_boletim"]}; sem fechar: {len(g["sem_fechar"])}.')
            for z in g['sem_fechar'][:6]:
                w(f'        {z["secao"]}: votos {z["n"]}, confirmações de governador {z["conf_gov"]}, suspensões {z["susp_gov"]}, órfãs {z["orfas_gov"]}, sessões sem tela de governador {z["sessoes_sem_tela_de_governador"]}, boletim {z["bu_comp_gov"]}.')
        od = X.get('ordem_dos_avpart') or {}
        if od and 'erro' not in od:
            mo = od['mesma_ordem_nos_dois_turnos_mesma_urna']; fp_ = od['fracao_de_pares_com_a_mesma_ordem']
            w(f'  E2. Ordem dos pacotes avpart9x: é da urna (igual nos dois turnos em {fi(mo["iguais"])} de {fi(mo["de"])}) e não agrupa por lugar (pares com a mesma ordem: {fmt(100 * fp_["dentro_do_local"], 1)}% dentro do local, {fmt(100 * fp_["dentro_do_municipio"], 1)}% no município, {fmt(100 * fp_["dentro_da_UF"], 1)}% na UF; ao acaso {fmt(100 / 24, 1)}%).')
            w('      Teste conjunto das classes contra o resíduo de y, por modelo (permutação dos rótulos dentro do município, 2.000 vezes): ' + '; '.join(f'{m}: {x["classes"]} classes, p {fmt(x["p_permutacao_dentro_do_municipio"], 3)} (Wald com erro por município, que rejeita demais nesse desenho: p {fmt(x["p_wald"], 3)})' for m, x in od['por_modelo'].items()) + '.')
        xc = X['reacao_na_tela']
        w('  E3. Os três estimadores de T (com o controle do 1º turno, como na letra; sem ele; primeira diferença). O estimando da letra controla c1 só na')
        w('      regressão do 2º turno; quando o desfecho se repete muito de um turno para o outro, isso sozinho desloca T.')
        for nome in ('UNI', 'AAS', 'ANT'):
            for rot, e in xc['X1_tres_estimadores'][nome].items():
                a, b, c = e['letra_com_controle_do_1t'], e['sem_controle_do_1t'], e['primeira_diferenca']
                casas = 3 if rot == 'tempo_medio_s' else 5
                w(f'     {nome} {rot}: letra T {fmt(a["T"], casas)} (z {fmt(a["z"], 1)}; t2 {fmt(a["t2"], casas)}, t1 {fmt(a["t1"], casas)}, coeficiente do 1º turno {fmt(a["l_coef_de_c1"], 2)}); sem controle T {fmt(b["T"], casas)} (z {fmt(b["z"], 1)}; t2 {fmt(b["t2"], casas)}); primeira diferença {fmt(c["T"], casas)} (z {fmt(c["z"], 1)}).')
        w('  E4. Correção na tela de presidente por décimo da fração de Flávio (r2), valor bruto:')
        for nome in ('AAS', 'UNI'):
            w(f'     {nome}: ' + '; '.join(f'r2 {fmt(d["r2_medio"], 2)}: {fmt(100 * d["c1"], 2)}% e {fmt(100 * d["c2"], 2)}% ({fmt(100 * d["c2_menos_c1"], 2)}, ep {fmt(100 * d["ep"], 2)})' for d in xc['X2_decis_de_r2'][nome]) + '.')
        w('  E5. T com um controle a mais de cada vez:')
        for nome in ('UNI', 'AAS'):
            w(f'     {nome}: ' + '; '.join(f'{rot}: {fmt(e["T"], 5)} (ep {fmt(e["ep"], 5)}, z {fmt(e["z"], 1)}, 99% até {fmt(e["lim_sup_99"], 5)})' for rot, e in xc['X3_um_controle_a_mais'][nome].items() if 'T' in e) + '.')
            e = xc['X3_um_controle_a_mais'][nome]['coef_da_variacao_do_comparecimento_sobre_c2_menos_c1']
            w(f'        coeficiente da variação do comparecimento sobre c2 - c1: {fmt(e["b"], 5)} (ep {fmt(e["ep"], 5)}, z {fmt(e["z"], 1)}).')
        w('  E6. T por região (UNI): ' + '; '.join(f'{r}: {fmt(e["T"], 5)} (ep {fmt(e["ep"], 5)}, z {fmt(e["z"], 1)}; n {fi(e["n"])}; c1 {fmt(100 * e["c1"], 2)}%, c2 {fmt(100 * e["c2"], 2)}%)' for r, e in xc['X4_por_regiao_UNI'].items()) + '.')
        x5 = xc['X5_correcao_por_tipo_de_habilitacao_UNI']
        w('  E7. Taxa de correção por tipo de habilitação do eleitor (UNI, agregado): ' + '; '.join(f'{dia}º turno: ' + ', '.join(f'{t} {fmt(100 * v["taxa"], 2)}% de {fi(v["eleitores"])}' for t, v in x5[dia].items()) for dia in ('1', '2')) + '.')
        x6 = xc['X6_c2_menos_c1_por_terco_de_r2_e_de_baixa_escolaridade_AAS']
        w(f'  E8. c2 - c1 por terço de r2 e por terço de baixa escolaridade (AAS; correlação entre r2 e baixa escolaridade {fmt(x6["correlacao_r2_baixa_escolaridade"], 2)}):')
        for a in range(3):
            w('     terço ' + str(a + 1) + ' de r2: ' + '; '.join(f'escolaridade baixa terço {t["terco_baixa_escolaridade"]}: {fmt(100 * t["c2_menos_c1"], 2) if t["c2_menos_c1"] is not None else "n/d"} (ep {fmt(100 * t["ep"], 2) if t["ep"] is not None else "n/d"}; n {t["secoes"]})' for t in x6['tabela'] if t['terco_r2'] == a + 1) + '.')
        x7 = xc.get('X7_votantes_a_mais_na_cabine')
        if x7:
            w('  E9. Os votantes a mais se comportam na cabine como os outros? Inclinação da taxa do 2º turno contra a variação do comparecimento da seção, com a taxa do')
            w('      1º turno, r2 e idade de controle; ao lado, a inclinação que apareceria se as sessões a mais fossem "limpas" (sem tecla indevida e sem correção),')
            w('      plantadas nos dados de 2026:')
            for nome in ('UNI', 'AAS'):
                w(f'     {nome} ({fi(x7[nome]["secoes"])} seções; {fi(x7[nome]["secoes_com_aumento"])} com aumento): ' + '; '.join(f'{rot}: observada {fmt(x7[nome][rot]["inclinacao_observada"], 4)} (ep {fmt(x7[nome][rot]["ep"], 4)}); com sessões limpas plantadas {fmt(x7[nome][rot]["inclinacao_com_sessoes_a_mais_limpas_plantadas"], 4)}; distância {fmt(x7[nome][rot]["distancia_em_ep_entre_observado_e_plantado"], 1)} ep' for rot in ('tecla_indevida', 'correcao')) + '.')
                w('        tecla indevida por faixa da variação do comparecimento (1º e 2º turno): ' + '; '.join((f'queda de {fmt(-100 * t["ate"], 0)}% ou mais' if t['de'] <= -1 else (f'alta de {fmt(100 * t["de"], 0)}% ou mais' if t['ate'] >= 10 else f'{fmt(100 * t["de"], 0)}% a {fmt(100 * t["ate"], 0)}%')) + f': {fmt(100 * t["taxa_1t"], 1)}% e {fmt(100 * t["taxa_2t"], 1)}% (n {t["secoes"]})' for t in x7[nome]['tecla_indevida']['por_faixa_da_variacao_do_comparecimento']) + '.')
                d = x7[nome]['tecla_indevida']['primeira_diferenca_sem_controle_do_1t']
                w(f'        em primeira diferença, sem o controle do 1º turno, a inclinação da tecla indevida é {fmt(d["inclinacao"], 4)} (z {fmt(d["z"], 1)}): vem do 1º turno (taxa mais alta onde o comparecimento depois subiu), não do 2º, que é plano.')
            w('      Só fala contra a versão ingênua (sessões fabricadas sem imitar o erro do eleitor); um programa que imitasse o comportamento passaria.')
        w('')
    w('DESVIOS, DECISÕES NÃO FIXADAS PELO REGISTRO (escritas no docstring antes de rodar) E ERROS VISTOS DEPOIS')
    for linha in R['desvios']: w('  - ' + linha)
    w('')
    w('CONTAGEM DE TESTES: 3 partes com veredito (a, b, c). Com z de 3,3 de um lado, a chance de um sinal por acaso em (c) é 0,05%; (a) e (b) são contagens exatas.')
    w('Nenhuma comparação com outro ano foi usada: não há log de outro ano em disco e nenhum veredito depende de 2014, 2018 ou 2022.')
    txt = '\n'.join(o) + '\n'
    assert chr(8212) not in txt and chr(8211) not in txt
    return txt



# ====================================================================================================================
# EXPLORATÓRIO (escrito DEPOIS de ver os resultados da primeira rodada; não entra em veredito)
# ====================================================================================================================
def exploratorio_governador(LG, UR):
    """O placebo de governador acusou I2b e I3 em seções onde parte dos eleitores só tem a tela de presidente (voto em
    trânsito fora da UF). Regra acrescentada depois de ver o resultado: a diferença é explicada pelo próprio log quando
    é igual ao número de sessões sem tela de governador, e o boletim fecha com confirmações + suspensões de governador."""
    out = {}
    for rot, fu, fl, dia in (('ANT 2º turno', 'ant2', 'ant', '2'), ('AAS 2º turno', 'aas2', 'aas', '2'), ('AAS 1º turno', 'aas1', 'aas', '1'),
                             ('ANT 1º turno (só log)', None, 'ant', '1')):
        tot = viol = fecha_log = com_bu = fecha_bu = eleitores = 0; sobra = []
        for k, o in LG['res'][fl].items():
            if 'erro' in o or not o.get(dia) or o[dia]['n'] == 0: continue
            D = o[dia]; cg = D['conf'].get('Governador', 0); sg = D['susp'].get('Governador', 0)
            if cg + sg == 0: continue
            tot += 1
            orf = len([x for x in D['orf'] if 'Governador' in x['cargos']])
            if cg + sg == D['n']: continue
            viol += 1
            sem_gov = sum(v for kk, v in D['ordem'].items() if 'Governador' not in kk and '(suspenso)' not in kk)
            ok_log = (D['n'] - (cg + sg - orf) == sem_gov)
            fecha_log += ok_log; eleitores += sem_gov
            u = UR['res'].get(fu, {}).get(k) if fu else None
            ok_bu = None
            if u and u.get('bu') and 3 in u['bu']['cargos']:
                com_bu += 1; ok_bu = (u['bu']['cargos'][3]['comp'] == cg + sg - orf); fecha_bu += ok_bu
            if not ok_log or ok_bu is False:
                sobra.append({'secao': k, 'n': D['n'], 'conf_gov': cg, 'susp_gov': sg, 'orfas_gov': orf, 'sessoes_sem_tela_de_governador': sem_gov,
                              'bu_comp_gov': u['bu']['cargos'][3]['comp'] if (u and u.get('bu') and 3 in u['bu']['cargos']) else None})
        out[rot] = {'secoes_com_governador_no_log': tot, 'com_I3_de_governador_diferente': viol, 'explicadas_por_sessoes_so_de_presidente_no_log': fecha_log,
                    'com_boletim': com_bu, 'boletim_fecha_com_confirmacoes_mais_suspensoes': fecha_bu, 'eleitores_so_de_presidente': eleitores, 'sem_fechar': sobra}
    return out


def exploratorio_ordem(B, uni2, linhas):
    """Classes de ordem dos pacotes avpart9x: a ordem é da urna? agrupa por lugar? está ligada ao voto (permutação dentro do município)?"""
    from scipy.stats import chi2
    out = {'por_modelo': {}}
    d1 = {(l['chave'], l['serie']): l['ordem_avpart'] for l in linhas if l['dia'] == '1'}
    ig = tot = 0
    for l in uni2.values():
        kk = (l['chave'], l['serie'])
        if kk in d1:
            tot += 1; ig += (d1[kk] == l['ordem_avpart'])
    out['mesma_ordem_nos_dois_turnos_mesma_urna'] = {'iguais': ig, 'de': tot}
    def pares(grupo):
        g = collections.defaultdict(list)
        for k, gg in zip(B['k'], grupo): g[(gg, uni2[k]['modelo'])].append(uni2[k]['ordem_avpart'])
        same = t = 0
        for v in g.values():
            n = len(v)
            if n < 2: continue
            c = collections.Counter(v); same += sum(q * (q - 1) // 2 for q in c.values()); t += n * (n - 1) // 2
        return same / t if t else None
    out['fracao_de_pares_com_a_mesma_ordem'] = {'dentro_do_local': pares(B['loc']), 'dentro_do_municipio': pares(B['mun']), 'dentro_da_UF': pares(B['uf']), 'ao_acaso_1_em_24': 1 / 24}
    rng = np.random.default_rng(SEMENTE + 5)
    for mod in sorted(set(uni2[k]['modelo'] for k in B['k'])):
        m = np.array([uni2[k]['modelo'] == mod for k in B['k']])
        ks = [k for k, f in zip(B['k'], m) if f]
        cl = collections.Counter(uni2[k]['ordem_avpart'] for k in ks)
        classes = [c for c, q in cl.most_common() if q >= 5]
        if len(classes) < 3: continue
        Dm = np.column_stack([[1.0 if uni2[k]['ordem_avpart'] == c else 0.0 for k in ks] for c in classes[1:]])
        r = reg_fe(B['y'][m], np.column_stack([Dm, B['X'][m]]), B['mun'][m], B['mun'][m], w=B['V'][m], tira_unicos=True)
        q = Dm.shape[1]
        V = r['fator'] * (r['IF'].T @ r['IF'])[:q, :q]
        b = r['b'][:q]
        Wd = float(b @ np.linalg.pinv(V) @ b)
        # permutação: resíduo do modelo sem as classes; rótulos embaralhados dentro do município
        r0 = reg_fe(B['y'][m], B['X'][m], B['mun'][m], B['mun'][m], w=B['V'][m], tira_unicos=True)
        e = r0['e']; w = r0['w']; ok = r0['ok']
        lab = np.array([classes.index(uni2[k]['ordem_avpart']) if uni2[k]['ordem_avpart'] in classes else -1 for k in ks])[ok]
        mun = B['mun'][m][ok]
        _, gm = np.unique(mun, return_inverse=True)
        ordem_g = np.argsort(gm, kind='stable'); lim = np.flatnonzero(np.diff(gm[ordem_g])) + 1
        grupos = np.split(ordem_g, lim)
        nc = len(classes)
        def ssb(lb):
            v = lb >= 0
            sw = np.bincount(lb[v], weights=w[v], minlength=nc); se = np.bincount(lb[v], weights=(w * e)[v], minlength=nc)
            return float((se[sw > 0] ** 2 / sw[sw > 0]).sum())
        obs = ssb(lab); maior = 0; NP = 2000
        for _ in range(NP):
            lb = lab.copy()
            for gidx in grupos:
                if len(gidx) > 1: lb[gidx] = lab[rng.permutation(gidx)]
            maior += ssb(lb) >= obs
        out['por_modelo'][mod] = {'urnas': int(r['n']), 'classes': len(classes), 'graus': q, 'wald_com_erro_por_municipio': Wd, 'p_wald': float(chi2.sf(Wd, q)), 'municipios': int(r['G']),
                                  'p_permutacao_dentro_do_municipio': (maior + 1) / (NP + 1), 'permutacoes': NP, 'maior_b_em_modulo': float(np.abs(b).max()),
                                  'nota': 'o Wald com muitas restrições e poucos municípios por classe rejeita demais; vale a permutação'}
    return out


def exploratorio_c(LG, S, P):
    L, fora, ext = base_c(LG, S, P)
    out = {}
    f = lambda l, d, c: l[d][c] / l[d]['n']
    amostras = {'UNI': L, 'AAS': [l for l in L if l['fonte'] == 'aas'], 'ANT': [l for l in L if l['fonte'] == 'ant']}
    # X1: os três estimadores para cada desfecho (com controle do 1º turno, sem controle, primeira diferença)
    x1 = {}
    for nome, Ls in amostras.items():
        Lt = [l for l in Ls if not (math.isnan(l['d1']['seg']) or math.isnan(l['d2']['seg']))]
        des = {'correcao': (Ls, arr(Ls, lambda l: f(l, 'd2', 'k')), arr(Ls, lambda l: f(l, 'd1', 'k'))),
               'tecla_indevida': (Ls, arr(Ls, lambda l: f(l, 'd2', 'i')), arr(Ls, lambda l: f(l, 'd1', 'i'))),
               'tempo_medio_s': (Lt, arr(Lt, lambda l: l['d2']['seg']), arr(Lt, lambda l: l['d1']['seg'])),
               'fracao_mais_de_30_s': (Lt, arr(Lt, lambda l: l['d2']['m30']), arr(Lt, lambda l: l['d1']['m30']))}
        x1[nome] = {}
        for rot, (LL, y2, y1) in des.items():
            a = estima_T(LL, y2, y1); b = estima_T(LL, y2, y1, c1ctl=False); c = estima_T(LL, y2, y1, so_dif=True)
            x1[nome][rot] = {'letra_com_controle_do_1t': {k: a[k] for k in ('T', 'ep', 'z', 't2', 't1', 'l_coef_de_c1')},
                             'sem_controle_do_1t': {k: b[k] for k in ('T', 'ep', 'z', 't2', 't1')}, 'primeira_diferenca': {k: c[k] for k in ('T', 'ep', 'z')}}
    out['X1_tres_estimadores'] = x1
    # X2: decis de r2 (bruto)
    x2 = {}
    for nome, Ls in amostras.items():
        r2 = arr(Ls, lambda l: l['r2']); c1 = arr(Ls, lambda l: f(l, 'd1', 'k')); c2 = arr(Ls, lambda l: f(l, 'd2', 'k'))
        q = np.quantile(r2, np.arange(1, 10) / 10); dz = np.digitize(r2, q)
        x2[nome] = [{'decil': int(d + 1), 'r2_medio': float(r2[dz == d].mean()), 'secoes': int((dz == d).sum()), 'c1': float(c1[dz == d].mean()), 'c2': float(c2[dz == d].mean()),
                     'c2_menos_c1': float((c2 - c1)[dz == d].mean()), 'ep': float((c2 - c1)[dz == d].std(ddof=1) / math.sqrt((dz == d).sum()))} for d in range(10)]
    out['X2_decis_de_r2'] = x2
    # X3: um controle a mais de cada vez (UNI e AAS)
    x3 = {}
    for nome in ('UNI', 'AAS'):
        Ls = amostras[nome]
        c1 = arr(Ls, lambda l: f(l, 'd1', 'k')); c2 = arr(Ls, lambda l: f(l, 'd2', 'k'))
        mais = np.array([l['mais'] for l in Ls], float)
        dcomp = np.array([(S[l['k']]['2']['comp'] - S[l['k']]['1']['comp']) / S[l['k']]['1']['comp'] for l in Ls])
        abst1 = np.array([1 - S[l['k']]['1']['comp'] / S[l['k']]['1']['apt'] for l in Ls])
        casos = {'so_idade_(letra)': None, 'mais_escolaridade': mais[:, 2:], 'mais_biometria': mais[:, 0:1], 'mais_mulheres': mais[:, 1:2],
                 'mais_variacao_do_comparecimento': dcomp[:, None], 'mais_abstencao_do_1t': abst1[:, None],
                 'tudo_junto': np.column_stack([mais, dcomp, abst1])}
        x3[nome] = {}
        for rot, M in casos.items():
            e = estima_T(Ls, c2, c1, mais=M)
            x3[nome][rot] = {k: e[k] for k in ('T', 'ep', 'z', 't2', 't1', 'lim_sup_99')}
        # coeficiente da variação do comparecimento sobre c2 - c1
        r2 = arr(Ls, lambda l: l['r2']); idade = np.array([l['idade'] for l in Ls], float)
        R = reg_fe(c2 - c1, np.column_stack([dcomp, r2, idade]), np.array([l['uf'] for l in Ls]), np.array([l['mun'] for l in Ls]))
        x3[nome]['coef_da_variacao_do_comparecimento_sobre_c2_menos_c1'] = {'b': float(R['b'][0]), 'ep': float(R['ep'][0]), 'z': float(R['b'][0] / R['ep'][0])}
    out['X3_um_controle_a_mais'] = x3
    # X4: por região (UNI)
    REG = {**{u: 'N' for u in ('AC', 'AM', 'AP', 'PA', 'RO', 'RR', 'TO')}, **{u: 'NE' for u in ('AL', 'BA', 'CE', 'MA', 'PB', 'PE', 'PI', 'RN', 'SE')},
           **{u: 'SE' for u in ('ES', 'MG', 'RJ', 'SP')}, **{u: 'S' for u in ('PR', 'RS', 'SC')}, **{u: 'CO' for u in ('DF', 'GO', 'MS', 'MT')}}
    x4 = {}
    for reg in ('N', 'NE', 'SE', 'S', 'CO'):
        Lr = [l for l in L if REG[l['uf']] == reg]
        e = estima_T(Lr, arr(Lr, lambda l: f(l, 'd2', 'k')), arr(Lr, lambda l: f(l, 'd1', 'k')))
        c1 = arr(Lr, lambda l: f(l, 'd1', 'k')); c2 = arr(Lr, lambda l: f(l, 'd2', 'k'))
        x4[reg] = {'T': e['T'], 'ep': e['ep'], 'z': e['z'], 'n': e['n'], 'c1': float(c1.mean()), 'c2': float(c2.mean())}
    out['X4_por_regiao_UNI'] = x4
    # X5: correção por tipo de habilitação do eleitor (agregado, UNI)
    ks = set(l['k'] for l in L); fonte = {l['k']: l['fonte'] for l in L}
    x5 = {}
    for dia in ('1', '2'):
        cont = {t: [0, 0] for t in ('biometria', 'liberado_pelo_mesario', 'sem_biometria_no_cadastro')}
        for k in ks:
            D = LG['res'][fonte[k]][k][dia]
            fl = np.array(D['fl']); cp = np.array(D['cp'])
            bom = (fl & 2) == 0
            for t, m in (('biometria', (fl & 12) == 0), ('liberado_pelo_mesario', (fl & 4) > 0), ('sem_biometria_no_cadastro', (fl & 8) > 0)):
                cont[t][0] += int((bom & m).sum()); cont[t][1] += int((bom & m & (cp > 0)).sum())
        x5[dia] = {t: {'eleitores': v[0], 'com_correcao': v[1], 'taxa': v[1] / v[0] if v[0] else None} for t, v in cont.items()}
    out['X5_correcao_por_tipo_de_habilitacao_UNI'] = x5
    # X6: nível educacional baixo contra r2, e c2 - c1 por terço de escolaridade baixa dentro de terço de r2 (AAS)
    Ls = amostras['AAS']
    r2 = arr(Ls, lambda l: l['r2']); baixa = arr(Ls, lambda l: 1 - sum(l['mais'][5:9]))   # 1 - (e5..e8) = até fundamental completo, aproximado
    d = arr(Ls, lambda l: f(l, 'd2', 'k') - f(l, 'd1', 'k'))
    tr = np.digitize(r2, np.quantile(r2, [1 / 3, 2 / 3])); tb = np.digitize(baixa, np.quantile(baixa, [1 / 3, 2 / 3]))
    out['X6_c2_menos_c1_por_terco_de_r2_e_de_baixa_escolaridade_AAS'] = {
        'correlacao_r2_baixa_escolaridade': float(np.corrcoef(r2, baixa)[0, 1]),
        'tabela': [{'terco_r2': int(a + 1), 'terco_baixa_escolaridade': int(b + 1), 'secoes': int(((tr == a) & (tb == b)).sum()),
                    'c2_menos_c1': float(d[(tr == a) & (tb == b)].mean()) if ((tr == a) & (tb == b)).any() else None,
                    'ep': float(d[(tr == a) & (tb == b)].std(ddof=1) / math.sqrt(((tr == a) & (tb == b)).sum())) if ((tr == a) & (tb == b)).sum() > 1 else None}
                   for a in range(3) for b in range(3)]}
    # X7: os votantes a mais se comportam na cabine como os outros? (fala à hipótese de presença fabricada, e só à versão ingênua dela)
    x7 = {}
    for nome in ('UNI', 'AAS'):
        Ls = amostras[nome]
        n1 = arr(Ls, lambda l: l['d1']['n']); n2 = arr(Ls, lambda l: l['d2']['n'])
        g = (n2 - n1) / n1
        r2 = arr(Ls, lambda l: l['r2']); idade = np.array([l['idade'] for l in Ls], float)
        fes = np.array([l['uf'] for l in Ls]); cl = np.array([l['mun'] for l in Ls])
        i1 = arr(Ls, lambda l: f(l, 'd1', 'i')); i2 = arr(Ls, lambda l: f(l, 'd2', 'i'))
        c1 = arr(Ls, lambda l: f(l, 'd1', 'k')); c2 = arr(Ls, lambda l: f(l, 'd2', 'k'))
        x7[nome] = {'secoes': len(Ls), 'variacao_media_do_comparecimento': float(g.mean()), 'dp': float(g.std(ddof=1)), 'secoes_com_aumento': int((g > 0).sum())}
        faixas = [(-1, -0.02), (-0.02, 0), (0, 0.02), (0.02, 0.05), (0.05, 0.10), (0.10, 10)]
        for rot, y2, y1 in (('tecla_indevida', i2, i1), ('correcao', c2, c1)):
            # plantio: sessões a mais "limpas" (sem tecla indevida e sem correção) nas seções com aumento
            y2p = np.where(g > 0, y2 * n1 / n2, y2)
            R = reg_fe(y2, np.column_stack([g, y1, r2, idade]), fes, cl)
            Rp = reg_fe(y2p, np.column_stack([g, y1, r2, idade]), fes, cl)
            Rd = reg_fe(y2 - y1, np.column_stack([g, r2, idade]), fes, cl)
            x7[nome][rot] = {'inclinacao_observada': float(R['b'][0]), 'ep': float(R['ep'][0]), 'z': float(R['b'][0] / R['ep'][0]),
                             'inclinacao_com_sessoes_a_mais_limpas_plantadas': float(Rp['b'][0]), 'ep_plantado': float(Rp['ep'][0]),
                             'distancia_em_ep_entre_observado_e_plantado': float((R['b'][0] - Rp['b'][0]) / R['ep'][0]), 'taxa_media_2t': float(y2.mean()),
                             'primeira_diferenca_sem_controle_do_1t': {'inclinacao': float(Rd['b'][0]), 'ep': float(Rd['ep'][0]), 'z': float(Rd['b'][0] / Rd['ep'][0])},
                             'por_faixa_da_variacao_do_comparecimento': [{'de': a, 'ate': bb, 'secoes': int(((g > a) & (g <= bb)).sum()),
                                                                          'taxa_1t': float(y1[(g > a) & (g <= bb)].mean()), 'taxa_2t': float(y2[(g > a) & (g <= bb)].mean())}
                                                                         for a, bb in faixas if ((g > a) & (g <= bb)).sum() > 10]}
    out['X7_votantes_a_mais_na_cabine'] = x7
    return out


DESVIOS = [
    'RDV: em vez de baixar os 3.062 que faltam na amostra antiga, entram os 3.000 da amostra aleatória nova (mandado pela tarefa). As identidades com RDV valem para 835 + 3.000 seções; as de log e boletim para as duas amostras inteiras.',
    'Parte (a): "explicada por contingência documentada no próprio log" virou regra automática (confirmação órfã com religamento, desligamento ou reinício no log). O veredito SEM SINAL desconta as violações explicadas por inteiro; a leitura mais estrita (zero violação de qualquer identidade) sai ao lado. Regra escrita sabendo dos casos já achados pelo R27_DA.',
    'Parte (b): "lista ordenada" lida como lista em ordem alfabética; a ordem em que os quatro pacotes avpart9x aparecem no log muda de urna para urna e sai ao lado. Normalização do código da seção e da UF. "Uma impressão por modelo" lida como uma impressão de PROGRAMA por modelo no país e uma lista completa por modelo dentro da UF, descontada a contingência de mídia registrada no log; a leitura mais estrita sai ao lado. Regra escrita depois de ver a estrutura dos logs (sem voto).',
    'Parte (b): "etapa sem SUCESSO em urna que recebeu voto" lida como etapa sem SUCESSO na corrida de verificação seguida de voto oficial na mesma ligação; a leitura mais estrita (qualquer data, mesma série) sai ao lado.',
    'Parte (b): resíduo de y com efeito fixo de município (a amostra aleatória quase não tem duas seções no mesmo local); local e UF ao lado. Variante que coincide com UF inteira: não identificável, só descrita.',
    'Parte (c): regressão sem peso (o desenho não fixa peso); amostra do veredito = união das duas; erro de t2 - t1 pelas duas regressões empilhadas com erro por município; "enxerga o plantado" = incremento com z de 3,3 ou mais em 95% das cópias e recuperação entre 0,8 e 1,2.',
    'Parte (c): o exterior fica fora (efeito fixo de UF); o universo exige o log dos dois turnos no mesmo pacote.',
    'Parte (c): tempo de cabine entra só ao lado (S8), sem veredito, porque no 2º turno a tela de presidente é a primeira e o intervalo inclui o caminho até a cabine.',
    'ERRO MEU, visto depois de rodar: as identidades I2b e I3 de governador (placebo) comparavam com o total de votos computados, e parte dos eleitores só tem a tela de presidente (voto em trânsito fora da UF). A tabela registrada fica como saiu; a conferência corrigida está no exploratório E1 e fecha em todas as seções. As identidades de presidente, que dão o veredito, não mudam.',
    'LIMITE DO ESTIMANDO DA LETRA, visto depois de rodar: ele controla c1 só na regressão do 2º turno. Para a correção isso quase não pesa (coeficiente de c1 de 0,15), mas para o tempo de tela (0,77) e para a tecla indevida (0,50) desloca T por construção. Os números da letra ficam como saíram; o exploratório E3 traz os três estimadores lado a lado.',
    'Apresentação decidida depois de ver o resultado: como T saiu negativo, o limite em votos é dado também pela especificação menos favorável entre as fixadas antes (letra, S1, S2, S4, S5).',
    'O exterior tem só 10 pares na amostra aleatória: não foi descrito à parte (o registro pedia 20 ou mais).',
]


def cmd_rodar():
    LG, UR, S, P, C = carrega_tudo()
    A = parte_a(LG, UR)
    B = parte_b(LG, UR, S, P, C)
    Cc = parte_c(LG, S, P)
    V = vereditos(A, B, Cc)
    R = {'teste': 'R27_C3 (D1.6): coerência interna da urna e reação do eleitor na tela', 'quando': time.strftime('%Y-%m-%d %H:%M:%S UTC', time.gmtime()),
         'registro': 'Adendo 27 (commit 2748895), Onda C, item C3; Adendos 28 e 30', 'vereditos': V, 'parte_a': A, 'parte_b': B, 'parte_c': Cc, 'desvios': DESVIOS,
         'extracao_dos_logs': LG.get('quando'), 'leitura_das_urnas': UR.get('quando')}
    diz('exploratório')
    X = {'aviso': 'feito depois de ver os resultados da primeira rodada (rodada1.log); não entra em veredito',
         'governador': exploratorio_governador(LG, UR), 'ordem_dos_avpart': B.get('exploratorio_teste_conjunto_da_ordem_dos_avpart'),
         'reacao_na_tela': exploratorio_c(LG, S, P)}
    grava('parcial_exploratorio.json', X)
    R['exploratorio'] = X
    grava('resultado_completo.json', R)
    with open(SAIDA_JSON, 'w') as f:
        json.dump(R, f, ensure_ascii=False, indent=1, default=_js)
    txt = escreve_txt(R)
    with open(SAIDA_TXT, 'w') as f:
        f.write(txt)
    diz('vereditos', json.dumps({k: v['veredito'] for k, v in V.items()}, ensure_ascii=False))
    diz('gravado', SAIDA_JSON, SAIDA_TXT)


if __name__ == '__main__':
    cmd = sys.argv[1] if len(sys.argv) > 1 else ''
    if cmd == 'extrair': cmd_extrair()
    elif cmd == 'urna': cmd_urna()
    elif cmd == 'rodar': cmd_rodar()
    else:
        print(__doc__)
