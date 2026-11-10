"""R27_C1: QUEM LIBEROU E A QUE HORAS (testes D2-2 MESALOG e D2-5 RELOGIO de registro/adendo27/desenho_D2_proposta.json).

Adendo 27 do pré-registro (commit 2748895, 10/11/2026 00:16:42 UTC), Onda C, item C1, na ordem do Adendo 28 (commit
938be19, 10/11/2026 04:36:33 UTC). Os critérios valem como escritos nos campos estatistica, criterio_sinal,
criterio_sem_sinal, poder e placebo de cada teste. Este docstring foi escrito ANTES de qualquer conta deste teste com
votos, com classes de habilitação ou com horários. O que ele decide e o registro não fixa está em DECISÕES e sai no
resultado como desvio. O que for feito depois de ver o resultado fica em funções com nome "exploratorio_" e sai marcado.

Uso (todos com python3 -I):
  scripts/analisar_R27_C1.py extrair   leitor próprio dos 3.897 logs (sem voto por candidato), grava eventos por seção
  scripts/analisar_R27_C1.py perfil    eleitores sem biometria por seção da amostra (perfil do eleitorado, em fluxo)
  scripts/analisar_R27_C1.py rodar     monta as tabelas, roda tudo, grava resultados/R27_C1_quem_liberou_e_quando.json e .txt
Trabalho e parciais: /home/user/trabalho-eleicao/adendo27/R27_C1/

O QUE EU JÁ SABIA ANTES DE ESCREVER (contaminação declarada)
- Do próprio desenho D2 (campo observacoes_sobre_os_dados): totais brutos da amostra por tipo e turno vistos pelo
  desenhista (ANO 48.399 no 1T e 50.875 no 2T; pedidos de liberação manual 73.141 e 76.011; mesário identificado
  42.857 e 49.750; não associado 14.452 e 12.871; alertas de eleitor que já votou 1.103 e 825; votos computados
  969.282 e 1.001.462). Logo B1 e B8 do D2-2 não são cegos: a sobra de nível é pequena, perto de 0,13 ponto.
- Da Onda A e do Adendo 28: comparecimento +2.960.239; liberações manuais do bweb +290.239 no país; a virada passa
  pelo comparecimento; A6 sem relação entre fração de liberação e virada.
- De novidades_relatorio.json: o TSE fala em cerca de 34 mil votos na prorrogação. Não vi contagem própria.
- Não eram conhecidos: razão de cauda (B2), fim de fila (B3), sequências (B4), dedo (B5), reservatório (B6), elo com o
  voto (B7), nada do D2-5 em 2026 fora a calibração de tempos do 1T feita pelo desenhista, nada do censo de
  encerramentos.
- Antes de escrever abri só estrutura: a gramática do log em 5 pacotes (mensagens, blocos aninhados), as listas da
  amostra, os campos das bases. Descobri nessa leitura que o pacote de log pode trazer, em bloco aninhado, o log de
  OUTRA seção (urna de contingência que serviu a outra seção no 1T). Por isso o leitor filtra pela identificação
  da seção gravada pelo próprio log (ver E2).

ESCALA COMUM (registro): margem 4.430.191; comparecimento do 2T 128.236.074; 10% da margem = 443.019 = 0,345% do
comparecimento; 25% = 1.107.548 = 0,864%. Voto inserido vale 1 na margem.

=========================== O QUE O REGISTRO FIXA: D2-2 MESALOG ===========================
Amostra principal L: prefixo de L_ordem.txt (locais inteiros), sem o local cortado no fim. Secundária: M10 (10
municípios inteiros). As demais em separado. Só seções cujo log traz votos nos dois dias. Estimadores de razão com
IC de 95% por reamostragem de locais (L) ou municípios (M10), 2.000 réplicas; totais nacionais = razão x 128.236.074.
B1: s_ANO = soma ANO2/soma C2 - soma ANO1/soma C1; s_MAN idem.
B2: rho_t = soma MAN_t/soma BIO3_t (BIO3 = BIO com 3 ou 4 tentativas); ln(rho_2/rho_1); X = soma MAN2 - rho_1 x soma BIO3_2.
B3: n_fim = habilitações ANO ou MAN depois da última BIO do dia; somar n_fim nas seções com n_fim >= 3; 2T menos 1T.
B4: votos em sequências de 4 ou mais habilitações sem biometria seguidas, menos o esperado por permutação das classes
    dentro da seção e do turno (200 permutações); 2T menos 1T por voto.
B5: fração das MAN por dedo novo ou não associado; fração das MAN sem nenhuma digital capturada do eleitor; 2T - 1T.
B6: seções com ANO do turno maior que os eleitores sem biometria da seção mais 2.
B7: regressão do D2-1 (efeito fixo de local, peso C1, erro por local) com x = [(ANO2 + MAN2) - (ANO1 + MAN1)]/C1, e
    outra com x separado em suspeito (B3, B4 e dedo novo) e comum.
B8: alertas "O eleitor identificado já votou" por mil votos, 2T contra 1T.
V = (X/soma C2 + max(s_ANO, 0)) x 128.236.074.
SINAL: V >= 1.107.548 com limite inferior >= 443.019 E pelo menos um confirmador (B3 + B4 >= 443.019 votos nacionais
  a favor do 2T, ou gama de B7 >= 0,30 com IC que exclui zero). A diferença em diferenças de manhã e tarde do placebo
  não pode explicar o achado.
SEM SINAL: limite superior de V < 443.019 E limite superior de B3 + B4 < 443.019.
INCONCLUSIVO: IC largo demais, divergência entre L e M10 maior que os ICs, ou B6 > 0 sem explicação cadastral.
Achado local: seções com n_fim >= 5 no 2T, com ANO acima do reservatório, ou com mais de 30% das liberações por dedo novo.
Poder: (a) MAN sintéticas uniformes somando 0,864% dos votos (L2 e C2 junto): ln perto de 0,109 e X perto de 0,864%;
  (b) 30 ANO sintéticas depois do último voto em 5% das seções: B3 e B4 acusam todas, gama de B7 perto de 1; (c) 0,345%.
Placebo: 1T da mesma urna; razão de cauda manhã contra tarde no 1T e diferença em diferenças; permutação em B4;
  desfecho branco e nulo em B7.

=========================== O QUE O REGISTRO FIXA: D2-5 RELOGIO ===========================
Por voto: g = habilitação menos voto computado anterior; d = voto computado menos habilitação; c = ciclo entre votos
computados. IMP: g < 12 s, ou d < 2 s, ou c < 15 s; voto antes de "Urna pronta" ou depois do último "Inicio do
Encerramento"; voto computado sem habilitação; total de votos computados no log diferente do comparecimento do boletim;
relógio que anda para trás. RAJ: 8 ou mais votos seguidos com g abaixo do percentil 5 de g da própria seção no 1T
(22 s com menos de 100 votos no 1T). T17: votos computados depois de 17:00:00 de Brasília. T17o: os de T17 precedidos
de 15 minutos ou mais sem voto. CURTO (só descritiva): BIO ou MAN com d < 4 s. No 1T, IMP usa só g e as regras de
relógio. Totais nacionais por razão em L x 128.236.074, IC por reamostragem de locais; M10 confere.
Composição: razão de chances de habilitação sem biometria em T17 contra o resto do dia, 2T contra 1T.
Elo: regressão do D2-1 com x = fração dos votos da seção em (IMP ou RAJ ou T17o), efeito fixo de local.
Censo: seções com DT_ENCERRAMENTO depois de 17:30 de Brasília em cada turno (contagem e comparecimento) e regressão
com efeito fixo de local de y sobre o indicador e sobre os minutos de atraso.
V = votos nacionais em (IMP ou RAJ ou T17o) no 2T menos a taxa do 1T aplicada ao 2T. Teto: total nacional de T17.
SINAL: V >= 1.107.548 com limite inferior >= 443.019, taxa do 2T pelo menos 3 vezes a do 1T, e elo positivo (IC
  excluindo zero) na amostra ou no censo. Qualquer voto IMP vai para lista.
SEM SINAL: limite superior de T17 < 443.019 E limite superior de IMP + RAJ < 443.019. Se T17 passar, ainda sem sinal
  se o limite superior de T17o + IMP + RAJ < 443.019 e o elo tiver limite superior < 0,10 de margem por voto tardio.
INCONCLUSIVO: demais casos, e sempre que a taxa de RAJ no 1T passar de 0,1% dos votos.
Poder: bloco de 40 ciclos sintéticos de 20 s depois do último voto em 5% das seções (40 votos em L2 e C2): todos em
  RAJ e, depois das 17h, em T17o; total nacional perto de 0,78%. Repetir com 15 por seção (0,29%).
Placebo: o dia do 1T nas mesmas urnas; censo do 1T em corte; desfecho branco e nulo.

=========================== DECISÕES QUE O REGISTRO NÃO FIXA (escritas antes de rodar) ===========================
LEITOR (próprio; o do desenhista e o do D1 foram lidos só para entender o formato)
E1. Pacote = arquivo -log.jez de cada pasta de amostra2t/arq. Blocos = logd.dat do pacote e de cada .jez aninhado.
E2. Identidade: cada bloco grava, a cada partida, "Município:", "Zona Eleitoral:" e "Seção Eleitoral:" (aplicativo GAP).
    Um trecho de log só conta para a seção do pacote se a identidade corrente do bloco for a da seção. Trechos de
    outra seção são contados à parte e ficam fora. Trecho sem identidade conhecida só entra se for do logd.dat principal.
E3. Dias: 04/10/2026 (1T) e 25/10/2026 (2T), aplicativo VOTA.
E4. Ciclo de habilitação: a janela de mensagens recomeça em "Aguardando digitação do identificador do eleitor" e em
    "Identificador do eleitor digitado pelo mesário" e fecha em "Eleitor foi habilitado". Classe pela janela:
      BIO  "Tipo de habilitação do eleitor [biométrica]";
      MAN  "Solicitação de dado pessoal do eleitor para habilitação manual" ou "Solicita digital do mesário", sem a
           linha biométrica; subtipos: MES ("Mesário N habilitou o eleitor"), NAOASSOC ("Digital coletada bate com
           uma digital gravada após o registro inicial de mesário"), NOVO ("Não encontrou digital coletada em nenhum
           dos arquivos"), OUTRO;
      ANO  "Ano de nascimento digitado é igual ao do cadastro", sem pedido de digital do mesário e sem linha biométrica;
      BIO_SL  nenhuma das linhas acima, mas com "Capturada a digital" na janela (linha de tipo ausente): conta como
           BIO e é contada à parte;
      OUTRO  o resto (contado; não entra em BIO nem em "sem biometria").
    Tentativas = maior k de "Solicita digital. Tentativa [k] de [4]" na janela. BIO3 = BIO com tentativas >= 3.
    Digitais capturadas do eleitor = linhas "Capturada a digital. Tentativa" na janela.
E5. Voto = "O voto do eleitor foi computado". Recebe a classe da habilitação aberta. Habilitação sem voto e voto sem
    habilitação são contados à parte. ANO_t, MAN_t, BIO3_t contam VOTOS computados com essa classe. C_t = votos
    computados no log do dia (confiro contra o comparecimento do bweb e contra QT_ELEI_BIOM_SEM_HABILITACAO).
E6. Ordem dos votos no dia: ordem do arquivo dentro do bloco; blocos ordenados pela hora do primeiro evento do dia.
    Intervalos g e c não atravessam blocos (o primeiro voto de cada bloco fica sem g e sem c).
E7. Relógio para trás: par de linhas consecutivas do mesmo dia no mesmo bloco em que a hora diminui (qualquer
    aplicativo). O voto IMP por essa regra é o primeiro voto computado depois do recuo (o ciclo que contém o recuo).
    Recuo fora de ciclo de voto vai para a lista sem contar voto.

AMOSTRA
A1. Local = lib.chave_local com o local do 1T (o do sorteio). L = seções baixadas que estão em L_ordem.txt; o local do
    fim do prefixo sai se alguma seção dele em L_ordem.txt não foi baixada. M10 = seções de M10.txt; conglomerado =
    município. Resto = as demais, só valores pontuais.
A2. Universo "par" = seções com votos próprios (E2) no log nos dois dias. Vale para o D2-2 e para as taxas do D2-5.
    Seções só com o 2T no log: categorias do D2-5 à parte (limiar de 22 s).
A3. Reamostragem: 2.000 réplicas, semente 20261110, percentis 2,5 e 97,5. Em M10 são 10 conglomerados: IC grosseiro,
    dito no resultado.

D2-2
B-1. Manhã = habilitação antes de 12:00:00 local; tarde = o resto (placebo 2).
B-2. B3 e B4 usam a sequência de votos computados do dia (E6); "sem biometria" = ANO ou MAN (qualquer subtipo).
     Seção sem nenhuma BIO no dia: n_fim = todos os votos sem biometria (contada à parte).
     B3 nacional = (S_fim2/soma C2 - S_fim1/soma C1) x 128.236.074, S_fim = soma de n_fim nas seções com n_fim >= 3.
     B4 nacional = (Exc2/soma C2 - Exc1/soma C1) x 128.236.074, Exc = soma por seção de (observado - média de 200
     permutações com semente fixa). "B3 + B4" = soma das duas, como escrito (a união sem dupla contagem vai ao lado).
B-3. B6: reservatório = soma, na seção principal e nas agregadas a ela (arquivo de locais), de QT_ELEITORES menos
     QT_ELEITORES_BIOMETRIA do perfil do eleitorado de 2026. "Explicação cadastral", fixada aqui: (E-a) aptos do bweb
     no turno diferem do total do perfil (com agregadas) em mais de 2, isto é, o perfil não descreve o caderno da
     urna; (E-b) a mesma seção já passa do reservatório + 2 no 1T com ANO1 >= ANO2 - 2 (descompasso estável entre a
     marca de biometria do perfil e a da urna, presente no turno de controle). Sem (E-a) nem (E-b): sem explicação.
     Informo as três contagens por turno. A cláusula de inconclusivo usa as do 2T sem explicação.
B-4. B7: y = [(L2 - R2) - (L1 - R1)]/C1 com votos e comparecimento de dados/secoes2026.json.gz; controles do D2-1:
     (C2 - C1)/C1, O1/C1, (B1 + N1)/C1, L1/C1, H1/C1 (H1 = MAN1 do log) e urna trocada (cai se constante). Efeito fixo
     de local, peso C1, erro por local. Principal em L; M10 e todas as pares ao lado. IC de 95% normal.
     Suspeito = votos sem biometria do 2T menos os do 1T que estão em fim de fila com n_fim >= 3, ou em sequência de
     4 ou mais, ou são MAN de dedo novo (NOVO); comum = os demais. Ao lado: NAOASSOC também como suspeito; sem o
     controle de comparecimento; com ANO1/C1 a mais.
     Espelho: a mesma regressão com y = (L2 - L1)/C1 e com y = (R2 - R1)/C1 (o ganho de cada candidato em separado),
     e a conta inteira com os turnos invertidos (1T tratado como suspeito). Placebo: y = [(B2 + N2) - (B1 + N1)]/C1.
B-5. Divergência L contra M10: ICs de 95% de V que não se cruzam.
B-6. "Placebo explica o achado" (só importa se houver SINAL): |ln(rho_1T,tarde/rho_1T,manhã)| >= |ln(rho_2/rho_1)|.
B-7. Lista local: todas as seções da amostra (L, M10 e resto) que cumprem cada condição no 2T, com a mesma contagem
     no 1T ao lado; para dedo novo informo também quantas têm 5 ou mais liberações (com 1 ou 2 liberações a fração
     passa de 30% por acaso).
B-8. Plantios (só nas tabelas, só no 2T, semente 20261110):
     (a) uniforme: k_i ~ Binomial(C2_i, 0,00864) votos MAN (subtipo MES, 4 tentativas) em posição aleatória do dia,
         somados a L2 e C2; (a') o mesmo com 0,00345.
     (b) concentrado: 30 votos ANO depois do último voto em 5% das seções sorteadas, somados a L2 e C2;
         (b') e (b'') o mesmo bloco de 30 em tantas seções quantas somem 0,345% e 0,864% dos votos.
     Explicações inocentes plantadas: (i1) eleitores reais sem biometria: k_i ~ Binomial(C2_i, 0,00864) votos ANO em
         posição aleatória, repartidos entre L2, R2, B2 e N2 como a seção votou no 2T; (i2) leitor pior: 11,5% a mais de
         MAN (tirados das BIO3) e 11,5% a mais de BIO3 (tiradas das BIO de 1 ou 2 tentativas), sem mexer em voto;
         (i3) abstenção pura: retirada de 3,57% dos votos de Flávio (sorteio binomial por seção), apagando do log
         votos ao acaso; C2 e R2 caem.
     SEM PODER se (a) não devolver ln entre 0,08 e 0,14 e X entre 0,7% e 1,0%, ou se (b) não for acusado por B3 e B4
     em pelo menos 90% dos votos plantados.

D2-5
R-1. Fuso: deslocamento do município = 8 menos a hora modal de abertura (campo ab da base, 2T, arredondada) das seções
     do município; sem moda clara, a regra por UF do registro. Hora de Brasília = hora local + deslocamento.
R-2. IMP no 2T: g < 12, d < 2, c < 15; voto antes da primeira "Urna pronta" do dia ou depois do último "Inicio do
     Encerramento" do dia (da própria seção); voto sem habilitação; relógio para trás (E7); e |votos no log -
     comparecimento do bweb| contado como votos IMP da seção. IMP no 1T (letra): g < 12 e as regras de relógio (antes
     de pronta, depois do encerramento, relógio para trás). Ao lado: as mesmas regras completas nos dois turnos, e
     IMP sem a regra do total (que pega troca de urna com log incompleto).
R-3. RAJ: sequência de 8 ou mais votos seguidos no mesmo bloco, todos com g definido e menor que o limiar da seção
     (percentil 5 de g do 1T por numpy.percentile linear; 22 s se o log do 1T tem menos de 100 votos com g).
     Todos os votos da sequência contam. No 1T, o mesmo limiar.
R-4. T17: voto computado com hora de Brasília > 17:00:00. T17o: voto de T17 que vem depois de um intervalo de 900 s ou
     mais sem voto computado, intervalo esse terminado (pelo voto seguinte) depois das 17:00:00 de Brasília; daí em
     diante todos os votos do dia contam (é a leitura que faz valer a frase do campo poder: "todos devem cair em RAJ
     e, quando depois das 17h, em T17o"). Ao lado: leitura estrita (só o voto imediatamente precedido de 900 s) e
     leitura larga (intervalo terminado depois das 16:45).
R-5. Taxas = votos na categoria / votos computados (universo par, L). V = (taxa2 - taxa1) x 128.236.074, com
     taxa1 pela definição de IMP do 1T (letra). Razão das taxas = taxa2/taxa1.
R-6. Composição: OR_t = [sem biometria/BIO em T17] / [sem biometria/BIO no resto do dia]; estatística ln(OR_2/OR_1).
R-7. Elo na amostra: y e controles do D2-1 (B-4), x = (votos em IMP ou RAJ ou T17o no 2T)/C2, efeito fixo de local,
     peso C1, erro por município (regra do D2-1) e por local ao lado. Espelho e placebo como em B-4. Ao lado, em
     corte no 1T: L1/(L1 + R1 + O1) contra a mesma fração calculada no 1T.
R-8. Censo (país): universo do D2-1 (dois turnos, Apurada, comparecimento >= 50 nos dois, variação de aptos <= 2, sem
     exterior). Encerramento = DT_ENCERRAMENTO do bweb (extração de estrutura da B2, R27_B2/est2026_*.json.gz, que
     confiro contra a base e contra os meus logs). Tardia = encerramento depois de 17:30:00 de Brasília. Regressões:
     y do D2-1 sobre tardia2, e sobre minutos de atraso (minutos depois de 17:00 de Brasília, zero se antes), com os
     controles do D2-1 (H1 do bweb), efeito fixo de local, peso C1, erro por município. Placebo do 1T em corte:
     L1/(L1 + R1 + O1) sobre tardia1. Desfecho placebo: branco e nulo. Espelho: ganho de L e de R em separado.
R-9. Plantios (5% das seções pares de L, semente 20261110): (p40) 40 ciclos de 20 s (g = 13, d = 7) começando 20
     minutos depois do último voto do dia, 40 votos em L2 e C2; (p15) o mesmo com 15; (p40c) o bloco colado ao último
     voto (sem os 20 minutos). Explicação inocente plantada: (fila) 40 eleitores reais em fila contínua logo depois
     do último voto, com g e d sorteados dos votos da própria seção no 2T e voto repartido como a seção votou.
     O encerramento é empurrado para depois do bloco. SEM PODER se (p40) não recuperar entre 0,6% e 0,95% dos votos.
R-10. Lista IMP: seção, turno, hora, regra e trecho do log (12 linhas antes e 4 depois), até 300 casos por regra.

DESCRITIVO PEDIDO
Q-1. Seções pares com C2 > C1 (votos do log): soma das variações de BIO, ANO e MAN (por subtipo) e por hora de
     Brasília do voto. O mesmo para C2 < C1. Em L (principal), M10 e todas. Também o grupo PI, MA, TO, PB, CE contra
     o resto (fixado aqui; amostra pequena nesse grupo, só descritivo).
     Aviso fixado antes: o 1T tem 5 cargos e fila mais lenta, então o perfil por hora difere entre os turnos por
     construção; a comparação por hora é descritiva.

VEREDITO: pela letra, para cada teste em separado. Onde a decisão depender de uma destas escolhas, digo qual.
NENHUM outro ano entra neste teste: o controle é o 1T de 2026 na mesma urna.

CONFERÊNCIA ESTRUTURAL FEITA DEPOIS DA EXTRAÇÃO E ANTES DE RODAR (sem classe de habilitação, sem horário, sem voto)
Vi apenas: 3.897 pacotes lidos sem erro; votos computados do log da própria seção iguais ao comparecimento do bweb
em 3.897 de 3.897 seções no 2T e em 3.874 de 3.874 no 1T; 23 seções sem log próprio do 1T (o desenhista contou 42
sem os dois dias no mesmo arquivo; com os blocos aninhados e a identidade da seção são 23); 2 trechos de outra seção
dentro de pacotes (381 habilitações do 1T, fora da conta); nenhum voto sem habilitação; 352 e 82 habilitações sem
voto; 24 e 47 habilitações da classe BIO_SL; nenhuma da classe OUTRO nem MAN sem subtipo; um único recuo de relógio
(2T, entre linhas de SCUE e LOGD). L = 3.062 seções em 476 locais inteiros (nenhum cortado), M10 = 734, resto = 101.
Logo as regras "voto sem habilitação" e "total do log diferente do boletim" do IMP valem zero por construção nesta
amostra, e isso é dito no resultado. Nenhuma decisão acima foi mudada depois dessa conferência.
"""
import os
import sys
import io
import re
import gzip
import json
import pickle
import zipfile
import collections

REPO = '/home/user/casa-control/eleicao-2026'
TRAB = '/home/user/trabalho-eleicao/adendo27/R27_C1'
AMOSTRA = '/home/user/trabalho-eleicao/amostra2t'
ARQ = AMOSTRA + '/arq'
DIAS = {'04/10/2026': 0, '25/10/2026': 1}
# classes
BIO, ANO, MAN_MES, MAN_NAO, MAN_NOVO, MAN_OUT, BIO_SL, OUTRO = range(8)
NOMES_CLASSE = ['BIO', 'ANO', 'MAN_MES', 'MAN_NAOASSOC', 'MAN_NOVO', 'MAN_OUTRO', 'BIO_SL', 'OUTRO']
RX_TENT = re.compile(r'Tentativa \[(\d+)\]')
RX_MES = re.compile(r'^Mesário (\d+) habilitou o eleitor')
# colunas do registro por habilitação
C_TID, C_THAB, C_TCOMP, C_CLS, C_MAXK, C_NSOL, C_NCAPT, C_NTOUT, C_MES, C_LIHAB, C_LICOMP, C_TPRES, C_RETRO = range(13)


# =====================================================================================================================
# LEITOR
# =====================================================================================================================
def _blocos(caminho):
    z = zipfile.ZipFile(caminho)
    out = []
    for n in z.namelist():
        if n.startswith('logd'):
            out.append((n, z.read(n).decode('latin1').splitlines()))
        elif n.endswith('.jez'):
            try:
                zz = zipfile.ZipFile(io.BytesIO(z.read(n)))
                for m in zz.namelist():
                    if m.startswith('logd'):
                        out.append((n + '/' + m, zz.read(m).decode('latin1').splitlines()))
            except zipfile.BadZipFile:
                out.append((n + '/ILEGIVEL', []))
    return out


def _novo_seg(bi, di, ident):
    return {'b': bi, 'dia': di, 'ident': ident, 'series': set(), 'nlin': 0, 'hab': [], 'comp_sem_hab': [], 'pronta': [],
            'ini_enc': [], 'enc_conf': [], 'ja_votou': [], 'justif': 0, 'reinicios': 0, 'conting': False,
            'ajuste_hora': 0, 'retro': [], 'mesarios': [], 'cancel': 0, 't_min': None, 't_max': None}


def _novo_ciclo():
    return [-1, 0, 0, 0, 0, 0, None]  # t_id, flags, maxk, nsol, ncapt, ntout, mesario


def _classe(c):
    f = c[1]
    if f & 1:
        return BIO
    if f & 6:
        if c[6] is not None:
            return MAN_MES
        if f & 8:
            return MAN_NAO
        if f & 16:
            return MAN_NOVO
        return MAN_OUT
    if f & 32:
        return ANO
    if c[4] > 0:
        return BIO_SL
    return OUTRO


def ler_pacote(caminho):
    """Lê um pacote de log e devolve os trechos (bloco, dia, identidade) com as habilitações e os eventos do dia."""
    partes = caminho.split('/')
    chave = f"{partes[-5].upper()}|{int(partes[-4])}|{int(partes[-3])}|{int(partes[-2])}"
    alvo = (int(partes[-4]), int(partes[-3]), int(partes[-2]))
    try:
        blocos = _blocos(caminho)
    except Exception as e:  # pacote ilegível
        return chave, {'erro': str(e), 'arquivo': caminho}
    segs = []
    for bi, (nome, linhas) in enumerate(blocos):
        ident = [None, None, None]
        seg_por = {}
        seg = None
        cur = _novo_ciclo()
        aberto = None
        prev_t = [None, None]
        prev_app = [None, None]
        retro_pend = False
        for li, l in enumerate(linhas):
            dia = l[:10]
            di = DIAS.get(dia)
            if di is None:
                if '\tGAP\t' in l:
                    p = l.split('\t')
                    if len(p) >= 5:
                        m = p[4]
                        if m.startswith('Município: '):
                            ident[0] = _int(m[11:])
                        elif m.startswith('Zona Eleitoral: '):
                            ident[1] = _int(m[16:])
                        elif m.startswith('Seção Eleitoral: '):
                            ident[2] = _int(m[17:])
                continue
            p = l.split('\t')
            if len(p) < 5:
                continue
            try:
                t = int(l[11:13]) * 3600 + int(l[14:16]) * 60 + int(l[17:19])
            except ValueError:
                continue
            app = p[3]
            m = p[4]
            if app == 'GAP':
                if m.startswith('Município: '):
                    ident[0] = _int(m[11:])
                elif m.startswith('Zona Eleitoral: '):
                    ident[1] = _int(m[16:])
                elif m.startswith('Seção Eleitoral: '):
                    ident[2] = _int(m[17:])
            idt = tuple(ident)
            if seg is None or seg['dia'] != di or seg['ident'] != idt:
                seg = seg_por.get((di, idt))
                if seg is None:
                    seg = seg_por[(di, idt)] = _novo_seg(bi, di, idt)
                    segs.append(seg)
                cur = _novo_ciclo()
                aberto = None
                retro_pend = False
            seg['nlin'] += 1
            seg['series'].add(p[2])
            if seg['t_min'] is None:
                seg['t_min'] = t
            seg['t_max'] = t
            if prev_t[di] is not None and t < prev_t[di]:
                seg['retro'].append((li, prev_t[di], t, prev_app[di], app))
                retro_pend = True
            prev_t[di] = t
            prev_app[di] = app
            if app != 'VOTA':
                if app == 'SCUE' and m.startswith('Data e hora'):
                    seg['ajuste_hora'] += 1
                elif app == 'GAP' and (m.startswith('Modo de carga da UE - Urna de contingência') or m.startswith('Contingência executada')):
                    seg['conting'] = True
                continue
            c0 = m[:9]
            if c0 == 'Solicita ':
                if m.startswith('Solicita digital. Tentativa'):
                    cur[3] += 1
                    mm = RX_TENT.search(m)
                    if mm:
                        k = int(mm.group(1))
                        if k > cur[2]:
                            cur[2] = k
                elif m == 'Solicita digital do mesário':
                    cur[1] |= 4
            elif c0 == 'Capturada':
                if m.startswith('Capturada a digital. Tentativa'):
                    cur[4] += 1
            elif m == 'Eleitor foi habilitado':
                rec = [cur[0], t, -1, _classe(cur), cur[2], cur[3], cur[4], cur[5], -1, li, -1, -1, 0]
                if cur[6] is not None:
                    if cur[6] not in seg['mesarios']:
                        seg['mesarios'].append(cur[6])
                    rec[C_MES] = seg['mesarios'].index(cur[6])
                seg['hab'].append(rec)
                aberto = rec
                cur = _novo_ciclo()
            elif m == 'O voto do eleitor foi computado':
                if aberto is None:
                    seg['comp_sem_hab'].append((t, li, 1 if retro_pend else 0))
                else:
                    aberto[C_TCOMP] = t
                    aberto[C_LICOMP] = li
                    if retro_pend:
                        aberto[C_RETRO] = 1
                aberto = None
                retro_pend = False
            elif m == 'Aguardando digitação do identificador do eleitor':
                cur = _novo_ciclo()
            elif m == 'Identificador do eleitor digitado pelo mesário':
                cur = _novo_ciclo()
                cur[0] = t
            elif m.startswith('Tipo de habilitação do eleitor [biom'):
                cur[1] |= 1
            elif m == 'Voto confirmado para [Presidente]':
                if aberto is not None:
                    aberto[C_TPRES] = t
            elif m.startswith('Timeout de reconhecimento do dedo'):
                cur[5] += 1
            elif m.startswith('Solicitação de dado pessoal do eleitor para habilitação manual'):
                cur[1] |= 2
            elif m == 'Ano de nascimento digitado é igual ao do cadastro':
                cur[1] |= 32
            elif m.startswith('Digital coletada bate com uma digital gravada após'):
                cur[1] |= 8
            elif m.startswith('Não encontrou digital coletada em nenhum dos arquivos'):
                cur[1] |= 16
            elif m == 'O eleitor identificado já votou':
                seg['ja_votou'].append(t)
            elif m == 'Justificativa recebida':
                seg['justif'] += 1
            elif m == 'Urna pronta para receber votos':
                seg['pronta'].append(t)
            elif m.startswith('Inicio do Encerramento') or m.startswith('Início do Encerramento'):
                seg['ini_enc'].append(t)
            elif m == 'Procedimento de encerramento confirmado':
                seg['enc_conf'].append(t)
            elif m.startswith('Iniciando aplicação'):
                seg['reinicios'] += 1
            elif m.startswith('Habilitação cancelada'):
                seg['cancel'] += 1
            elif c0 == 'Mesário 0' or c0[:8] == 'Mesário ':
                mm = RX_MES.match(m)
                if mm:
                    cur[6] = mm.group(1)
        for s in seg_por.values():
            s['series'] = sorted(s['series'])
            s['bloco'] = nome
    return chave, {'arquivo': caminho, 'alvo': alvo, 'blocos': [n for n, _ in blocos], 'segs': segs}


def _int(s):
    try:
        return int(s.strip())
    except ValueError:
        return None


def modo_extrair():
    from multiprocessing import Pool
    os.makedirs(TRAB, exist_ok=True)
    arqs = []
    for r, d, fs in os.walk(ARQ):
        for n in fs:
            if n.endswith('-log.jez'):
                arqs.append(os.path.join(r, n))
    arqs.sort()
    if len(sys.argv) > 2:
        arqs = arqs[:int(sys.argv[2])]
    res = {}
    dup = 0
    with Pool(3) as p:
        for i, (k, o) in enumerate(p.imap_unordered(ler_pacote, arqs, chunksize=6)):
            if k in res:
                dup += 1
                k = k + '#' + str(i)
            res[k] = o
            if (i + 1) % 500 == 0:
                print(i + 1, flush=True)
    with gzip.open(TRAB + '/eventos.pkl.gz', 'wb', compresslevel=4) as f:
        pickle.dump(res, f, protocol=4)
    nseg = sum(len(o.get('segs', [])) for o in res.values())
    print('pacotes', len(arqs), 'secoes', len(res), 'duplicadas', dup, 'trechos', nseg,
          'erros', sum(1 for o in res.values() if 'erro' in o), flush=True)


# =====================================================================================================================
# PERFIL DO ELEITORADO (reservatório de eleitores sem biometria) E AGREGADAS, SÓ DAS SEÇÕES DA AMOSTRA
# =====================================================================================================================
LOCAIS_ZIP = '/home/user/trabalho-eleicao/adendo21/F14_dl_locais/eleitorado_local_votacao_2026.zip'
PERFIL_DIR = '/home/user/trabalho-eleicao/adendo21/F15_dl_perfil_secao'


def _chaves_amostra():
    ks = []
    for r, d, fs in os.walk(ARQ):
        if any(n.endswith('-log.jez') for n in fs):
            p = r.split('/')[-4:]
            ks.append((p[0].upper(), int(p[1]), int(p[2]), int(p[3])))
    return sorted(ks)


def _ler_locais(chaves):
    """Arquivo de locais: tipo (principal ou agregada), seção principal, local e eleitores, por turno, nos municípios da amostra."""
    import csv
    muns = {(u, m) for u, m, z, s in chaves}
    ufs = {u for u, m in muns}
    out = {1: {}, 2: {}}
    with zipfile.ZipFile(LOCAIS_ZIP) as zf:
        for info in zf.infolist():
            nome = info.filename
            if not nome.lower().endswith('.csv') or 'BRASIL' in nome:
                continue
            uf = nome[:-4].split('_')[-1]
            if uf not in ufs:
                continue
            pref = {(';"%05d";' % m).encode() for u, m in muns if u == uf}
            with zf.open(nome) as f:
                cab = next(csv.reader([f.readline().decode('latin1')], delimiter=';'))
                ix = {c: i for i, c in enumerate(cab)}
                for raw in f:
                    cab80 = raw[:90]
                    if not any(p in cab80 for p in pref):
                        continue
                    r = next(csv.reader([raw.decode('latin1')], delimiter=';'))
                    k = (uf, int(r[ix['CD_MUNICIPIO']]), int(r[ix['NR_ZONA']]), int(r[ix['NR_SECAO']]))
                    out[int(r[ix['NR_TURNO']])][k] = [int(r[ix['CD_TIPO_SECAO_AGREGADA']]), int(r[ix['NR_SECAO_PRINCIPAL']]),
                                                      int(r[ix['NR_LOCAL_VOTACAO']]), int(r[ix['QT_ELEITOR_SECAO']]),
                                                      int(r[ix['QT_ELEITOR_ELEICAO_FEDERAL']])]
    return out


def _perfil_uf(arg):
    z, precisa = arg
    uf = os.path.basename(z).split('_')[-1][:2]
    muns = {('%05d' % m).encode() for (u, m, zn, s) in precisa}
    alvo = {(m, zn, s) for (u, m, zn, s) in precisa}
    out = {}
    with zipfile.ZipFile(z) as zf:
        nome = [i.filename for i in zf.infolist() if i.filename.lower().endswith('.csv')][0]
        with zf.open(nome) as f:
            cab = f.readline().decode('latin1').strip().replace('"', '').split(';')
            ix = {c: i for i, c in enumerate(cab)}
            im, izn, isc, iq, ib = ix['CD_MUNICIPIO'], ix['NR_ZONA'], ix['NR_SECAO'], ix['QT_ELEITORES'], ix['QT_ELEITORES_BIOMETRIA']
            ifx = ix['CD_FAIXA_ETARIA']
            for raw in f:
                if raw[35:40] not in muns:
                    continue
                r = raw.decode('latin1').rstrip('\r\n').split(';')
                try:
                    k = (int(r[im].strip('"')), int(r[izn]), int(r[isc]))
                except ValueError:
                    continue
                if k not in alvo:
                    continue
                # campos de quantidade são os quatro últimos (texto de local pode ter ponto e vírgula)
                q, b = int(r[-4]), int(r[-3])
                o = out.setdefault(k, [0, 0, 0, 0])
                o[0] += q
                o[1] += b
                try:
                    fx = int(r[ifx])
                except ValueError:
                    fx = 0
                if fx >= 7074:  # 70 anos ou mais (voto facultativo)
                    o[2] += q
                    o[3] += q - b
    return uf, {f'{uf}|{m}|{zn}|{s}': v for (m, zn, s), v in out.items()}


def modo_perfil():
    from multiprocessing import Pool
    import glob
    chaves = _chaves_amostra()
    loc = _ler_locais(chaves)
    print('locais lidos: 1T', len(loc[1]), '2T', len(loc[2]), flush=True)
    setc = set(chaves)
    agreg = {1: collections.defaultdict(list), 2: collections.defaultdict(list)}
    for t in (1, 2):
        for (u, m, z, s), v in loc[t].items():
            if v[0] != 1 and v[1] > 0 and (u, m, z, v[1]) in setc:
                agreg[t][(u, m, z, v[1])].append(s)
    precisa = set(chaves)
    for t in (1, 2):
        for (u, m, z, sp), ss in agreg[t].items():
            for s in ss:
                precisa.add((u, m, z, s))
    por_uf = collections.defaultdict(set)
    for k in precisa:
        por_uf[k[0]].add(k)
    zips = [(z, por_uf[os.path.basename(z).split('_')[-1][:2]]) for z in sorted(glob.glob(PERFIL_DIR + '/perfil_eleitor_secao_2026_*.zip'))
            if os.path.basename(z).split('_')[-1][:2] in por_uf]
    zips.sort(key=lambda a: os.path.getsize(a[0]), reverse=True)
    perfil = {}
    with Pool(3) as p:
        for uf, r in p.imap_unordered(_perfil_uf, zips):
            perfil.update(r)
            print(uf, len(r), len(perfil), flush=True)
    saida = {'colunas_perfil': ['eleitores', 'com_biometria', 'eleitores_70mais', 'sem_biometria_70mais'], 'perfil': perfil,
             'agregadas': {str(t): {'|'.join(map(str, k)): sorted(v) for k, v in agreg[t].items()} for t in (1, 2)},
             'locais': {str(t): {'|'.join(map(str, k)): v for k, v in loc[t].items() if k in precisa} for t in (1, 2)}}
    with gzip.open(TRAB + '/perfil_amostra.json.gz', 'wt') as f:
        json.dump(saida, f, separators=(',', ':'))
    print('perfil: secoes', len(perfil), 'de', len(precisa), 'precisas; eleitores', sum(v[0] for v in perfil.values()),
          'com biometria', sum(v[1] for v in perfil.values()), flush=True)


# =====================================================================================================================
# ANÁLISE
# =====================================================================================================================
N2 = 128236074
MARGEM = 4430191
L25 = 1107548
L10 = 443019
SEMENTE = 20261110
NREP = 2000
UF_FUSO = {'AC': 6, 'AM': 7, 'MS': 7, 'MT': 7, 'RO': 7, 'RR': 7}
GRUPO_NE = {'PI', 'MA', 'TO', 'PB', 'CE'}

# estatísticas por seção e turno do D2-2
N22 = ['C', 'BIO', 'BIO_SL', 'ANO', 'MAN', 'MAN_MES', 'MAN_NAO', 'MAN_NOVO', 'MAN_OUT', 'OUTRO', 'BIO3', 'MAN_semcapt',
       'MAN_m', 'BIO3_m', 'MAN_t', 'BIO3_t', 'n_fim', 'S_fim', 'sem_bio', 'seq4', 'seq4_exp', 'uni34', 'susp', 'susp_l',
       'ja', 'hab_sem_voto', 'ANO_m', 'BIO12']
I22 = {n: i for i, n in enumerate(N22)}
# estatísticas por seção e turno do D2-5
N25 = ['C', 'imp_g', 'imp_d', 'imp_c', 'imp_pre', 'imp_pos', 'imp_retro', 'IMP_full', 'IMP_letra', 'RAJ', 'T17', 'T17o',
       'T17o_estrita', 'T17o_larga', 'U_full', 'U_letra', 'IR_full', 'IR_letra', 'CURTO', 'nb_T17', 'bio_T17', 'nb_rest',
       'bio_rest', 'T18', 'T19', 'RAJ22', 'U_full_larga']
I25 = {n: i for i, n in enumerate(N25)}


def em_seq(a, k):
    """Máscara das posições que pertencem a sequências de k ou mais True seguidos (último eixo)."""
    import numpy as np
    n = a.shape[-1]
    out = np.zeros_like(a)
    if n < k:
        return out
    w = a[..., :n - k + 1].copy()
    for j in range(1, k):
        w &= a[..., j:n - k + 1 + j]
    for j in range(k):
        out[..., j:n - k + 1 + j] |= w
    return out


def registros_secao(o):
    """Votos computados da própria seção em cada dia, na ordem do log (E2, E5, E6)."""
    import numpy as np
    alvo = tuple(o['alvo'])
    out = {}
    for di in (0, 1):
        own = [s for s in o['segs'] if s['dia'] == di and tuple(s['ident']) == alvo]
        outras = [s for s in o['segs'] if s['dia'] == di and tuple(s['ident']) != alvo and s['hab']]
        com = sorted([s for s in own if s['hab']], key=lambda s: s['hab'][0][C_THAB])
        rows, segid = [], []
        for j, s in enumerate(com):
            for r in s['hab']:
                if r[C_TCOMP] >= 0:
                    rows.append(r)
                    segid.append(j)
        if not rows:
            out[di] = None
            continue
        A = np.array(rows, dtype=np.int64)
        pr = [min(s['pronta']) for s in own if s['pronta']]
        ie = [max(s['ini_enc']) for s in own if s['ini_enc']]
        ec = [max(s['enc_conf']) for s in own if s['enc_conf']]
        out[di] = {'thab': A[:, C_THAB].astype(float), 'tcomp': A[:, C_TCOMP].astype(float), 'cls': A[:, C_CLS].copy(),
                   'maxk': A[:, C_MAXK].copy(), 'ncapt': A[:, C_NCAPT].copy(), 'retro': A[:, C_RETRO].astype(bool),
                   'seg': np.array(segid), 'li': A[:, C_LICOMP].copy(),
                   'pronta': float(min(pr)) if pr else None, 'ini_enc': float(max(ie)) if ie else None,
                   'enc_conf': float(max(ec)) if ec else None,
                   'ja': sum(len(s['ja_votou']) for s in own), 'hab_sem_voto': sum(1 for s in own for r in s['hab'] if r[C_TCOMP] < 0),
                   'voto_sem_hab': sum(len(s['comp_sem_hab']) for s in own), 'justif': sum(s['justif'] for s in own),
                   'reinicios': sum(s['reinicios'] for s in own), 'nseg': len(com),
                   'blocos': [s['bloco'] for s in com], 'retro_ev': [tuple(e) + (s['bloco'],) for s in own for e in s['retro']],
                   'conting_no_pacote': any(s['conting'] for s in o['segs'] if s['dia'] == di),
                   'votos_outra_secao': sum(len(s['hab']) for s in outras)}
    return out


def st22(rec, semente):
    """Estatísticas do D2-2 de uma seção em um turno."""
    import numpy as np
    v = np.zeros(len(N22))
    cls = rec['cls']
    n = len(cls)
    bio = (cls == BIO) | (cls == BIO_SL)
    ano = cls == ANO
    man = (cls >= MAN_MES) & (cls <= MAN_OUT)
    nb = ano | man
    bio3 = bio & (rec['maxk'] >= 3)
    manha = rec['thab'] < 43200
    v[I22['C']] = n
    v[I22['BIO']] = bio.sum()
    v[I22['BIO_SL']] = (cls == BIO_SL).sum()
    v[I22['ANO']] = ano.sum()
    v[I22['MAN']] = man.sum()
    v[I22['MAN_MES']] = (cls == MAN_MES).sum()
    v[I22['MAN_NAO']] = (cls == MAN_NAO).sum()
    v[I22['MAN_NOVO']] = (cls == MAN_NOVO).sum()
    v[I22['MAN_OUT']] = (cls == MAN_OUT).sum()
    v[I22['OUTRO']] = (cls == OUTRO).sum()
    v[I22['BIO3']] = bio3.sum()
    v[I22['BIO12']] = (bio & (rec['maxk'] < 3)).sum()
    v[I22['MAN_semcapt']] = (man & (rec['ncapt'] == 0)).sum()
    v[I22['MAN_m']] = (man & manha).sum()
    v[I22['BIO3_m']] = (bio3 & manha).sum()
    v[I22['MAN_t']] = (man & ~manha).sum()
    v[I22['BIO3_t']] = (bio3 & ~manha).sum()
    v[I22['ANO_m']] = (ano & manha).sum()
    fim = np.zeros(n, bool)
    if bio.any():
        ult = np.nonzero(bio)[0][-1]
        fim[ult + 1:] = nb[ult + 1:]
    else:
        fim = nb.copy()
        v[I22['sem_bio']] = 1
    nfim = int(fim.sum())
    v[I22['n_fim']] = nfim
    if nfim >= 3:
        v[I22['S_fim']] = nfim
    else:
        fim[:] = False
    m = int(nb.sum())
    if m >= 4:
        sq = em_seq(nb, 4)
        rng = np.random.default_rng(semente)
        P = rng.permuted(np.broadcast_to(nb, (200, n)), axis=1)
        v[I22['seq4_exp']] = em_seq(P, 4).sum() / 200.0
    else:
        sq = np.zeros(n, bool)
    v[I22['seq4']] = sq.sum()
    u = fim | sq
    v[I22['uni34']] = u.sum()
    v[I22['susp']] = (u | (cls == MAN_NOVO)).sum()
    v[I22['susp_l']] = (u | (cls == MAN_NOVO) | (cls == MAN_NAO)).sum()
    v[I22['ja']] = rec['ja']
    v[I22['hab_sem_voto']] = rec['hab_sem_voto']
    return v


def intervalos(rec):
    """g (mesa), d (cabine), c (ciclo) por voto; g e c não atravessam blocos (E6)."""
    import numpy as np
    th, tc, seg = rec['thab'], rec['tcomp'], rec['seg']
    n = len(th)
    g = np.full(n, np.nan)
    c = np.full(n, np.nan)
    if n > 1:
        mesmo = seg[1:] == seg[:-1]
        g[1:] = np.where(mesmo, th[1:] - tc[:-1], np.nan)
        c[1:] = np.where(mesmo, tc[1:] - tc[:-1], np.nan)
    return g, tc - th, c


def limiar_raj(rec1):
    import numpy as np
    if rec1 is None:
        return 22.0
    g = intervalos(rec1)[0]
    g = g[~np.isnan(g)]
    if len(g) < 100:
        return 22.0
    return float(np.percentile(g, 5))


def cat25(rec, thr, off):
    """Máscaras por voto das categorias do D2-5."""
    import numpy as np
    g, d, c = intervalos(rec)
    tc = rec['tcomp']
    n = len(tc)
    with np.errstate(invalid='ignore'):
        m = {'imp_g': g < 12, 'imp_d': d < 2, 'imp_c': c < 15}
        rap = g < thr
        rap22 = g < 22.0
    m['imp_pre'] = (tc < rec['pronta']) if rec['pronta'] is not None else np.zeros(n, bool)
    m['imp_pos'] = (tc > rec['ini_enc']) if rec['ini_enc'] is not None else np.zeros(n, bool)
    m['imp_retro'] = rec['retro'].copy()
    m['IMP_full'] = m['imp_g'] | m['imp_d'] | m['imp_c'] | m['imp_pre'] | m['imp_pos'] | m['imp_retro']
    m['IMP_letra'] = m['imp_g'] | m['imp_pre'] | m['imp_pos'] | m['imp_retro']
    m['RAJ'] = em_seq(rap, 8)
    m['RAJ22'] = em_seq(rap22, 8)
    tb = tc + off
    m['T17'] = tb > 61200
    m['T18'] = tb > 64800
    m['T19'] = tb > 68400
    gap = np.empty(n)
    gap[0] = (tc[0] - rec['pronta']) if rec['pronta'] is not None else 0.0
    gap[1:] = tc[1:] - tc[:-1]
    m['T17o'] = m['T17'] & (np.cumsum((gap >= 900) & (tb > 61200)) > 0)
    m['T17o_estrita'] = m['T17'] & (gap >= 900)
    m['T17o_larga'] = m['T17'] & (np.cumsum((gap >= 900) & (tb > 60300)) > 0)
    m['U_full'] = m['IMP_full'] | m['RAJ'] | m['T17o']
    m['U_letra'] = m['IMP_letra'] | m['RAJ'] | m['T17o']
    m['U_full_larga'] = m['IMP_full'] | m['RAJ'] | m['T17o_larga']
    m['IR_full'] = m['IMP_full'] | m['RAJ']
    m['IR_letra'] = m['IMP_letra'] | m['RAJ']
    cls = rec['cls']
    bio = (cls == BIO) | (cls == BIO_SL)
    man = (cls >= MAN_MES) & (cls <= MAN_OUT)
    nb = (cls == ANO) | man
    m['CURTO'] = (bio | man) & (d < 4)
    m['nb_T17'] = nb & m['T17']
    m['bio_T17'] = bio & m['T17']
    m['nb_rest'] = nb & ~m['T17']
    m['bio_rest'] = bio & ~m['T17']
    m['_g'], m['_d'], m['_c'], m['_tb'] = g, d, c, tb
    return m


def st25(rec, thr, off):
    import numpy as np
    m = cat25(rec, thr, off)
    v = np.zeros(len(N25))
    v[0] = len(rec['tcomp'])
    for nme in N25[1:]:
        v[I25[nme]] = m[nme].sum()
    return v


def fe_reg(y, X, fe, w, cl, nomes):
    """MQO com efeito fixo (within), pesos e erro agrupado CR1 por um agrupamento que pode diferir do efeito fixo."""
    import numpy as np
    from lib import demean
    y = np.asarray(y, float)
    X = np.asarray(X, float)
    if X.ndim == 1:
        X = X[:, None]
    w = np.asarray(w, float)
    _, g = np.unique(fe, return_inverse=True)
    ok = np.bincount(g)[g] >= 2
    ok &= np.isfinite(y) & np.isfinite(X).all(axis=1) & (w > 0)
    y, X, w, g = y[ok], X[ok], w[ok], g[ok]
    cl = np.asarray(cl)[ok]
    _, g = np.unique(g, return_inverse=True)
    ok2 = np.bincount(g)[g] >= 2
    y, X, w, g, cl = y[ok2], X[ok2], w[ok2], g[ok2], cl[ok2]
    _, g = np.unique(g, return_inverse=True)
    _, c = np.unique(cl, return_inverse=True)
    Z = demean(np.column_stack([y, X]), g, w)
    yd, Xd = Z[:, 0], Z[:, 1:]
    usa = [j for j in range(Xd.shape[1]) if np.sum(w * Xd[:, j] ** 2) > 1e-12]
    fora = [nomes[j] for j in range(Xd.shape[1]) if j not in usa]
    Xd = Xd[:, usa]
    nm = [nomes[j] for j in usa]
    k = Xd.shape[1]
    sw = np.sqrt(w)
    Xw, yw = Xd * sw[:, None], yd * sw
    XtX = Xw.T @ Xw
    b = np.linalg.solve(XtX, Xw.T @ yw)
    e = yd - Xd @ b
    G = int(c.max()) + 1
    S = np.zeros((G, k))
    for j in range(k):
        S[:, j] = np.bincount(c, weights=w * Xd[:, j] * e, minlength=G)
    inv = np.linalg.inv(XtX)
    N = len(y)
    fator = G / (G - 1) * (N - 1) / (N - k) if G > 1 else float('nan')
    V = fator * inv @ (S.T @ S) @ inv
    se = np.sqrt(np.diag(V))
    return {'n': int(N), 'grupos_ef': int(g.max()) + 1, 'conglomerados': G, 'coef': dict(zip(nm, [float(x) for x in b])),
            'ep': dict(zip(nm, [float(x) for x in se])), 'fora_por_constante': fora}


def _ic(coef, ep):
    return [coef - 1.959964 * ep, coef + 1.959964 * ep]


def reamostra(S_list, cl, nrep=NREP, semente=SEMENTE):
    """Somas por conglomerado e matriz de réplicas (nrep x n_estatisticas) para cada matriz de S_list."""
    import numpy as np
    _, c = np.unique(cl, return_inverse=True)
    G = int(c.max()) + 1
    rng = np.random.default_rng(semente)
    W = rng.multinomial(G, np.full(G, 1.0 / G), size=nrep).astype(float)
    out = []
    for S in S_list:
        CS = np.zeros((G, S.shape[1]))
        for j in range(S.shape[1]):
            CS[:, j] = np.bincount(c, weights=S[:, j], minlength=G)
        out.append((S.sum(axis=0), W @ CS))
    return out, G


def deriv22(T1, T2):
    """Quantidades do D2-2 a partir dos totais (vetor ou matriz de réplicas) de cada turno."""
    import numpy as np
    a1 = {n: T1[..., i] for n, i in I22.items()}
    a2 = {n: T2[..., i] for n, i in I22.items()}
    o = {}
    with np.errstate(divide='ignore', invalid='ignore'):
        for nome in ('ANO', 'MAN', 'BIO', 'BIO3', 'OUTRO', 'MAN_MES', 'MAN_NAO', 'MAN_NOVO'):
            o['frac_%s_1T' % nome] = a1[nome] / a1['C']
            o['frac_%s_2T' % nome] = a2[nome] / a2['C']
        o['s_ANO'] = a2['ANO'] / a2['C'] - a1['ANO'] / a1['C']
        o['s_MAN'] = a2['MAN'] / a2['C'] - a1['MAN'] / a1['C']
        o['s_BIO3'] = a2['BIO3'] / a2['C'] - a1['BIO3'] / a1['C']
        r1 = a1['MAN'] / a1['BIO3']
        r2 = a2['MAN'] / a2['BIO3']
        o['rho_1T'] = r1
        o['rho_2T'] = r2
        o['ln_rho'] = np.log(r2 / r1)
        X = a2['MAN'] - r1 * a2['BIO3']
        o['X_frac'] = X / a2['C']
        o['V_MAN'] = X / a2['C'] * N2
        o['V_ANO'] = np.maximum(o['s_ANO'], 0) * N2
        o['V'] = o['V_MAN'] + o['V_ANO']
        o['V_nivel_puro'] = (np.maximum(o['s_MAN'], 0) + np.maximum(o['s_ANO'], 0)) * N2
        Xi = a1['MAN'] - r2 * a1['BIO3']
        o['V_invertido'] = (Xi / a1['C'] + np.maximum(-o['s_ANO'], 0)) * N2
        o['B3'] = (a2['S_fim'] / a2['C'] - a1['S_fim'] / a1['C']) * N2
        o['B3_taxa_1T'] = a1['S_fim'] / a1['C']
        o['B3_taxa_2T'] = a2['S_fim'] / a2['C']
        e1 = (a1['seq4'] - a1['seq4_exp']) / a1['C']
        e2 = (a2['seq4'] - a2['seq4_exp']) / a2['C']
        o['B4_exc_1T'] = e1
        o['B4_exc_2T'] = e2
        o['B4'] = (e2 - e1) * N2
        o['B3B4'] = o['B3'] + o['B4']
        o['B34_uniao'] = ((a2['uni34'] - a2['seq4_exp']) / a2['C'] - (a1['uni34'] - a1['seq4_exp']) / a1['C']) * N2
        o['B5_dedo_1T'] = (a1['MAN_NAO'] + a1['MAN_NOVO']) / a1['MAN']
        o['B5_dedo_2T'] = (a2['MAN_NAO'] + a2['MAN_NOVO']) / a2['MAN']
        o['B5_dedo_dif'] = o['B5_dedo_2T'] - o['B5_dedo_1T']
        o['B5_novo_1T'] = a1['MAN_NOVO'] / a1['MAN']
        o['B5_novo_2T'] = a2['MAN_NOVO'] / a2['MAN']
        o['B5_novo_dif'] = o['B5_novo_2T'] - o['B5_novo_1T']
        o['B5_semcapt_1T'] = a1['MAN_semcapt'] / a1['MAN']
        o['B5_semcapt_2T'] = a2['MAN_semcapt'] / a2['MAN']
        o['B5_semcapt_dif'] = o['B5_semcapt_2T'] - o['B5_semcapt_1T']
        o['B5_semcapt_por_voto_dif_nac'] = (a2['MAN_semcapt'] / a2['C'] - a1['MAN_semcapt'] / a1['C']) * N2
        o['B5_novo_por_voto_dif_nac'] = (a2['MAN_NOVO'] / a2['C'] - a1['MAN_NOVO'] / a1['C']) * N2
        o['B5_dedo_por_voto_dif_nac'] = ((a2['MAN_NOVO'] + a2['MAN_NAO']) / a2['C'] - (a1['MAN_NOVO'] + a1['MAN_NAO']) / a1['C']) * N2
        o['B8_1T'] = 1000 * a1['ja'] / a1['C']
        o['B8_2T'] = 1000 * a2['ja'] / a2['C']
        o['B8_dif'] = o['B8_2T'] - o['B8_1T']
        lm1 = np.log((a1['MAN_t'] / a1['BIO3_t']) / (a1['MAN_m'] / a1['BIO3_m']))
        lm2 = np.log((a2['MAN_t'] / a2['BIO3_t']) / (a2['MAN_m'] / a2['BIO3_m']))
        o['plac_ln_tarde_manha_1T'] = lm1
        o['plac_ln_tarde_manha_2T'] = lm2
        o['plac_did'] = lm2 - lm1
        o['ln_rho_manha'] = np.log((a2['MAN_m'] / a2['BIO3_m']) / (a1['MAN_m'] / a1['BIO3_m']))
        o['ln_rho_tarde'] = np.log((a2['MAN_t'] / a2['BIO3_t']) / (a1['MAN_t'] / a1['BIO3_t']))
        o['hab_sem_voto_1T_por_mil'] = 1000 * a1['hab_sem_voto'] / a1['C']
        o['hab_sem_voto_2T_por_mil'] = 1000 * a2['hab_sem_voto'] / a2['C']
    return o


def deriv25(T1, T2):
    import numpy as np
    a1 = {n: T1[..., i] for n, i in I25.items()}
    a2 = {n: T2[..., i] for n, i in I25.items()}
    o = {}
    with np.errstate(divide='ignore', invalid='ignore'):
        for nome in N25[1:19] + ['T18', 'T19', 'RAJ22', 'U_full_larga']:
            o['taxa_%s_1T' % nome] = a1[nome] / a1['C']
            o['taxa_%s_2T' % nome] = a2[nome] / a2['C']
            o['nac_%s_2T' % nome] = a2[nome] / a2['C'] * N2
            o['nac_%s_1T_aplicada' % nome] = a1[nome] / a1['C'] * N2
        o['V'] = (a2['U_full'] / a2['C'] - a1['U_letra'] / a1['C']) * N2
        o['V_mesmas_regras'] = (a2['U_full'] / a2['C'] - a1['U_full'] / a1['C']) * N2
        o['razao_taxas'] = (a2['U_full'] / a2['C']) / (a1['U_letra'] / a1['C'])
        o['razao_taxas_mesmas_regras'] = (a2['U_full'] / a2['C']) / (a1['U_full'] / a1['C'])
        o['T17_dif_nac'] = (a2['T17'] / a2['C'] - a1['T17'] / a1['C']) * N2
        or1 = (a1['nb_T17'] / a1['bio_T17']) / (a1['nb_rest'] / a1['bio_rest'])
        or2 = (a2['nb_T17'] / a2['bio_T17']) / (a2['nb_rest'] / a2['bio_rest'])
        o['OR_1T'] = or1
        o['OR_2T'] = or2
        o['ln_OR2_OR1'] = np.log(or2 / or1)
        o['frac_sembio_T17_1T'] = a1['nb_T17'] / (a1['nb_T17'] + a1['bio_T17'])
        o['frac_sembio_T17_2T'] = a2['nb_T17'] / (a2['nb_T17'] + a2['bio_T17'])
        o['frac_sembio_resto_1T'] = a1['nb_rest'] / (a1['nb_rest'] + a1['bio_rest'])
        o['frac_sembio_resto_2T'] = a2['nb_rest'] / (a2['nb_rest'] + a2['bio_rest'])
    return o


def avaliar(deriv, S1, S2, cl, semente=SEMENTE):
    """Ponto e IC de 95% (percentil, reamostragem de conglomerados) de cada quantidade derivada."""
    import numpy as np
    (rs, G) = reamostra([S1, S2], cl, semente=semente)
    (t1, R1), (t2, R2) = rs
    p = deriv(t1, t2)
    r = deriv(R1, R2)
    out = {}
    for k in p:
        x = r[k]
        x = x[np.isfinite(x)]
        if len(x) >= 0.9 * NREP:
            lo, hi = np.percentile(x, [2.5, 97.5])
            ep = float(np.std(x, ddof=1))
        else:
            lo = hi = ep = float('nan')
        out[k] = {'valor': float(p[k]), 'ic95': [float(lo), float(hi)], 'ep': ep, 'replicas_validas': int(len(x))}
    return out, G


def _sha(txt):
    import hashlib
    return hashlib.sha256(txt.encode('utf-8')).hexdigest()


def _grava_parcial(nome, obj):
    with open(TRAB + '/' + nome, 'w') as f:
        json.dump(obj, f, ensure_ascii=False, indent=1, default=_json_default)


def _json_default(o):
    import numpy as np
    if isinstance(o, (np.integer,)):
        return int(o)
    if isinstance(o, (np.floating,)):
        return float(o)
    if isinstance(o, np.ndarray):
        return o.tolist()
    if isinstance(o, (set, tuple)):
        return list(o)
    raise TypeError(str(type(o)))


class Dados:
    """Carrega tudo o que a análise usa e monta as tabelas por seção."""

    def __init__(self):
        import numpy as np
        sys.path.insert(0, REPO + '/scripts')
        from lib import carregar, chave_local
        self.np = np
        with gzip.open(TRAB + '/eventos.pkl.gz', 'rb') as f:
            ev = pickle.load(f)
        self.base = carregar(REPO + '/dados/secoes2026.json.gz')
        base = self.base
        self.chaves = sorted(ev.keys())
        self.rec = {k: registros_secao(ev[k]) for k in self.chaves}
        self.outra_secao = {'trechos': 0, 'habilitacoes': 0, 'pacotes': []}
        for k in self.chaves:
            for sg in ev[k]['segs']:
                if tuple(sg['ident']) != tuple(ev[k]['alvo']) and sg['hab']:
                    self.outra_secao['trechos'] += 1
                    self.outra_secao['habilitacoes'] += len(sg['hab'])
                    self.outra_secao['pacotes'].append([k, 'secao %s' % str(sg['ident'][2]), '1T' if sg['dia'] == 0 else '2T', len(sg['hab'])])
        self.arquivo = {k: ev[k]['arquivo'] for k in self.chaves}
        del ev
        # fuso por município (R-1)
        cont = collections.defaultdict(collections.Counter)
        for k, v in base.items():
            if '2' in v and v['2'].get('ab'):
                ab = v['2']['ab']
                try:
                    h = int(ab[:2]) + (1 if int(ab[3:5]) >= 30 else 0)
                except ValueError:
                    continue
                cont[k.split('|')[0] + '|' + k.split('|')[1]][h] += 1
        self.fuso_mun = {}
        for mk, c in cont.items():
            (h1, n1), = c.most_common(1)
            self.fuso_mun[mk] = h1
        self.off = {}
        for k in self.chaves:
            uf, mun = k.split('|')[:2]
            h = self.fuso_mun.get(uf + '|' + mun, UF_FUSO.get(uf, 8))
            self.off[k] = (8 - h) * 3600.0
        # amostras (A1)
        Lord = [l.strip() for l in open(AMOSTRA + '/L_ordem.txt') if l.strip()]
        M10 = [l.strip() for l in open(AMOSTRA + '/M10.txt') if l.strip()]
        setk = set(self.chaves)
        self.local = {k: chave_local(k, base[k]['1']) for k in self.chaves}
        por_local = collections.OrderedDict()
        for k in Lord:
            por_local.setdefault(chave_local(k, base[k]['1']) if k in base and '1' in base[k] else '?', []).append(k)
        self.L = [k for l, ks in por_local.items() if all(x in setk for x in ks) for k in ks]
        self.L_locais_cortados = [l for l, ks in por_local.items() if any(x in setk for x in ks) and not all(x in setk for x in ks)]
        self.M10 = [k for k in M10 if k in setk]
        fora = setk - set(self.L) - set(self.M10)
        self.resto = sorted(fora)
        self.par = [k for k in self.chaves if self.rec[k][0] is not None and self.rec[k][1] is not None]
        self.so2 = [k for k in self.chaves if self.rec[k][0] is None and self.rec[k][1] is not None]
        self.ix = {k: i for i, k in enumerate(self.par)}
        self.amostra_de = {}
        for k in self.L:
            self.amostra_de[k] = 'L'
        for k in self.M10:
            self.amostra_de[k] = 'M10'
        for k in self.resto:
            self.amostra_de[k] = 'resto'
        # limiar de rajada por seção (R-3)
        self.thr = {k: limiar_raj(self.rec[k][0]) for k in self.chaves}

    def votos(self, k):
        b = self.base[k]
        return b['1'], b['2']

    def tabela22(self, recs2=None, chaves=None):
        """Matrizes S1, S2 (seções pares x estatísticas do D2-2). recs2 substitui o registro do 2T de algumas seções."""
        np = self.np
        chaves = chaves or self.par
        S1 = np.zeros((len(chaves), len(N22)))
        S2 = np.zeros((len(chaves), len(N22)))
        for i, k in enumerate(chaves):
            j = self.ix[k]
            S1[i] = st22(self.rec[k][0], [SEMENTE, j, 1])
            r2 = recs2[k] if (recs2 is not None and k in recs2) else self.rec[k][1]
            S2[i] = st22(r2, [SEMENTE, j, 2])
        return S1, S2

    def tabela25(self, recs2=None, chaves=None):
        np = self.np
        chaves = chaves or self.par
        S1 = np.zeros((len(chaves), len(N25)))
        S2 = np.zeros((len(chaves), len(N25)))
        for i, k in enumerate(chaves):
            S1[i] = st25(self.rec[k][0], self.thr[k], self.off[k])
            r2 = recs2[k] if (recs2 is not None and k in recs2) else self.rec[k][1]
            S2[i] = st25(r2, self.thr[k], self.off[k])
        return S1, S2

    def conglomerado(self, chaves, tipo):
        if tipo == 'local':
            return [self.local[k] for k in chaves]
        return ['|'.join(k.split('|')[:2]) for k in chaves]

    def vetores_voto(self, chaves, delta=None):
        """Votos e comparecimento da base por seção; delta = {chave: {'L2':..,'R2':..,'B2':..,'N2':..,'C2':..}} somado ao 2T."""
        np = self.np
        nomes = ['L1', 'R1', 'O1', 'B1', 'N1', 'C1', 'L2', 'R2', 'O2', 'B2', 'N2', 'C2', 'U']
        M = np.zeros((len(chaves), len(nomes)))
        for i, k in enumerate(chaves):
            a, b = self.votos(k)
            M[i] = [a['L'], a['R'], a['O'], a['B'], a['N'], a['comp'], b['L'], b['R'], b['O'], b['B'], b['N'], b['comp'],
                    1.0 if a['urna'] != b['urna'] else 0.0]
            if delta and k in delta:
                dl = delta[k]
                for nm in ('L2', 'R2', 'B2', 'N2', 'C2'):
                    M[i, nomes.index(nm)] += dl.get(nm, 0)
        return {n: M[:, j] for j, n in enumerate(nomes)}


def regs_elo(D, chaves, x_dict, H1, cl_tipo='local', delta=None, extras=None):
    """Regressões do D2-1 com o x dado (dict nome -> vetor por seção). Devolve principal, espelho e placebo."""
    np = D.np
    v = D.vetores_voto(chaves, delta)
    C1 = v['C1']
    y = ((v['L2'] - v['R2']) - (v['L1'] - v['R1'])) / C1
    yL = (v['L2'] - v['L1']) / C1
    yR = (v['R2'] - v['R1']) / C1
    yBN = ((v['B2'] + v['N2']) - (v['B1'] + v['N1'])) / C1
    ctrl = {'dC': (v['C2'] - v['C1']) / C1, 'O1': v['O1'] / C1, 'BN1': (v['B1'] + v['N1']) / C1, 'L1': v['L1'] / C1,
            'H1': H1 / C1, 'urna_trocada': v['U']}
    if extras:
        ctrl.update(extras)
    fe = D.conglomerado(chaves, 'local')
    cl = D.conglomerado(chaves, cl_tipo)
    nomes = list(x_dict.keys()) + list(ctrl.keys())
    X = np.column_stack([x_dict[n] for n in x_dict] + [ctrl[n] for n in ctrl])
    out = {}
    for rot, yy in (('margem', y), ('ganho_L', yL), ('ganho_R', yR), ('placebo_BN', yBN)):
        r = fe_reg(yy, X, fe, C1, cl, nomes)
        out[rot] = {'n': r['n'], 'locais': r['grupos_ef'], 'conglomerados': r['conglomerados'],
                    'coef': {n: r['coef'].get(n) for n in x_dict}, 'ep': {n: r['ep'].get(n) for n in x_dict},
                    'ic95': {n: (_ic(r['coef'][n], r['ep'][n]) if n in r['coef'] else None) for n in x_dict},
                    'controles': {n: [r['coef'].get(n), r['ep'].get(n)] for n in ctrl}, 'fora_por_constante': r['fora_por_constante']}
    return out


# ------------------------------------------------- plantios do D2-2 -------------------------------------------------
def _copia(rec):
    return {k: (v.copy() if hasattr(v, 'copy') and not isinstance(v, (list, dict)) else v) for k, v in rec.items()}


def _insere(rec, pos, thab, tcomp, cls, maxk, ncapt):
    """Insere votos sintéticos depois das posições pos (vetor) do registro."""
    import numpy as np
    ordem = np.argsort(pos, kind='stable')
    pos = np.asarray(pos)[ordem]
    novo = _copia(rec)
    ins = pos + 1
    novo['thab'] = np.insert(rec['thab'], ins, np.asarray(thab, float)[ordem])
    novo['tcomp'] = np.insert(rec['tcomp'], ins, np.asarray(tcomp, float)[ordem])
    novo['cls'] = np.insert(rec['cls'], ins, np.asarray(cls)[ordem])
    novo['maxk'] = np.insert(rec['maxk'], ins, np.asarray(maxk)[ordem])
    novo['ncapt'] = np.insert(rec['ncapt'], ins, np.asarray(ncapt)[ordem])
    novo['retro'] = np.insert(rec['retro'], ins, False)
    novo['seg'] = np.insert(rec['seg'], ins, rec['seg'][pos])
    novo['li'] = np.insert(rec['li'], ins, -1)
    return novo


def plantio_uniforme(D, chaves, p, classe, rng, como_secao=False):
    """k_i ~ Binomial(C2_i, p) votos sintéticos da classe em posição aleatória do dia."""
    np = D.np
    recs, delta, tot = {}, {}, 0
    for k in chaves:
        r = D.rec[k][1]
        n = len(r['cls'])
        kk = int(rng.binomial(n, p))
        if kk == 0:
            continue
        pos = rng.integers(0, n, size=kk)
        th = r['tcomp'][pos] + 30
        recs[k] = _insere(r, pos, th, th + 20, np.full(kk, classe), np.full(kk, 4 if classe != ANO else 0),
                          np.full(kk, 4 if classe != ANO else 0))
        if como_secao:
            b = D.base[k]['2']
            pr = np.array([b['L'], b['R'], b['B'], b['N']], float)
            q = rng.multinomial(kk, pr / pr.sum()) if pr.sum() > 0 else [kk, 0, 0, 0]
            delta[k] = {'L2': int(q[0]), 'R2': int(q[1]), 'B2': int(q[2]), 'N2': int(q[3]), 'C2': kk}
        else:
            delta[k] = {'L2': kk, 'C2': kk}
        tot += kk
    return recs, delta, tot


def plantio_concentrado(D, chaves, frac, nbloco, rng):
    """nbloco votos ANO depois do último voto do dia em uma fração das seções."""
    np = D.np
    nsec = max(1, int(round(frac * len(chaves))))
    esc = [chaves[i] for i in sorted(rng.choice(len(chaves), size=nsec, replace=False))]
    recs, delta = {}, {}
    for k in esc:
        r = D.rec[k][1]
        n = len(r['cls'])
        pos = np.full(nbloco, n - 1)
        th = r['tcomp'][-1] + 30 + 50 * np.arange(nbloco)
        recs[k] = _insere(r, pos, th, th + 20, np.full(nbloco, ANO), np.zeros(nbloco, int), np.zeros(nbloco, int))
        delta[k] = {'L2': nbloco, 'C2': nbloco}
    return recs, delta, nsec * nbloco, esc


def plantio_leitor_pior(D, chaves, S2, rng, alta=0.115):
    np = D.np
    tot = S2.sum(axis=0)
    p1 = alta * tot[I22['MAN']] / tot[I22['BIO3']]
    p2 = (alta + p1) * tot[I22['BIO3']] / tot[I22['BIO12']]
    recs = {}
    for k in chaves:
        r = D.rec[k][1]
        cls = r['cls']
        bio = (cls == BIO) | (cls == BIO_SL)
        b3 = bio & (r['maxk'] >= 3)
        b12 = bio & (r['maxk'] < 3)
        v1 = b3 & (rng.random(len(cls)) < p1)
        v2 = b12 & (rng.random(len(cls)) < p2)
        if not v1.any() and not v2.any():
            continue
        novo = _copia(r)
        novo['cls'][v1] = MAN_MES
        novo['maxk'][v1] = 4
        novo['maxk'][v2] = 3
        recs[k] = novo
    return recs, {'p_BIO3_vira_MAN': float(p1), 'p_BIO12_vira_BIO3': float(p2)}


def plantio_abstencao(D, chaves, frac, rng):
    np = D.np
    recs, delta, tot = {}, {}, 0
    for k in chaves:
        r = D.rec[k][1]
        n = len(r['cls'])
        kk = int(rng.binomial(int(D.base[k]['2']['R']), frac))
        kk = min(kk, n - 1)
        if kk <= 0:
            continue
        tira = rng.choice(n, size=kk, replace=False)
        fica = np.ones(n, bool)
        fica[tira] = False
        novo = _copia(r)
        for nm in ('thab', 'tcomp', 'cls', 'maxk', 'ncapt', 'retro', 'seg', 'li'):
            novo[nm] = r[nm][fica]
        recs[k] = novo
        delta[k] = {'R2': -kk, 'C2': -kk}
        tot += kk
    return recs, delta, tot


# ------------------------------------------------- plantios do D2-5 -------------------------------------------------
def plantio_bloco_tempo(D, esc, nbloco, espera, rng, fila=False):
    """Bloco depois do último voto do dia. Sintético: ciclos de 20 s (g = 13, d = 7). Fila: g e d da própria seção."""
    np = D.np
    recs, delta = {}, {}
    for k in esc:
        r = D.rec[k][1]
        n = len(r['cls'])
        ult = r['tcomp'][-1]
        if fila:
            g, d, c = intervalos(r)
            ok = ~np.isnan(g)
            ii = rng.choice(np.nonzero(ok)[0], size=nbloco, replace=True)
            gg, dd = g[ii], d[ii]
            cl = r['cls'][ii]
            mk, nc = r['maxk'][ii], r['ncapt'][ii]
            th = np.empty(nbloco)
            tc = np.empty(nbloco)
            t = ult
            for j in range(nbloco):
                th[j] = t + gg[j]
                tc[j] = th[j] + dd[j]
                t = tc[j]
            b = D.base[k]['2']
            pr = np.array([b['L'], b['R'], b['B'], b['N']], float)
            q = rng.multinomial(nbloco, pr / pr.sum())
            delta[k] = {'L2': int(q[0]), 'R2': int(q[1]), 'B2': int(q[2]), 'N2': int(q[3]), 'C2': nbloco}
        else:
            tc = ult + espera + 20.0 * np.arange(nbloco)
            th = tc - 7.0
            cl = np.full(nbloco, ANO)
            mk = np.zeros(nbloco, int)
            nc = np.zeros(nbloco, int)
            delta[k] = {'L2': nbloco, 'C2': nbloco}
        novo = _insere(r, np.full(nbloco, n - 1), th, tc, cl, mk, nc)
        if novo['ini_enc'] is not None:
            novo['ini_enc'] = max(novo['ini_enc'], float(tc[-1]) + 60.0)
        recs[k] = novo
    return recs, delta


def _resumo(av, nomes):
    return {n: av[n] for n in nomes if n in av}


def _fmt(x, casas=0):
    """Número em formato brasileiro."""
    if x is None or (isinstance(x, float) and x != x):
        return 'n/d'
    s = f'{x:,.{casas}f}'
    return s.replace(',', 'X').replace('.', ',').replace('X', '.')


def modo_rodar():
    import numpy as np
    import time
    t0 = time.time()
    os.makedirs(TRAB, exist_ok=True)
    doc = __doc__
    p_doc = TRAB + '/docstring_antes_de_rodar.txt'
    if not os.path.exists(p_doc):
        open(p_doc, 'w').write(doc)
        open(TRAB + '/docstring_antes_de_rodar.sha256', 'w').write(_sha(doc) + '  docstring_antes_de_rodar.txt\n')
    D = Dados()
    R = {'teste': 'R27_C1', 'registro': {'adendo27_commit': '2748895', 'adendo28_commit': '938be19',
                                         'desenho': 'registro/adendo27/desenho_D2_proposta.json (D2-2 e D2-5)'},
         'docstring_sha256_antes_de_rodar': open(TRAB + '/docstring_antes_de_rodar.sha256').read().split()[0],
         'docstring_atual_sha256': _sha(doc),
         'escala': {'margem': MARGEM, 'comparecimento_2T': N2, 'limiar_25': L25, 'limiar_10': L10}}
    print('dados carregados', round(time.time() - t0), 's', flush=True)

    # ------------------------------------------------------------------ amostra e conferências estruturais
    par = D.par
    setpar = set(par)
    am = {'L': [k for k in D.L if k in setpar], 'M10': [k for k in D.M10 if k in setpar], 'resto': [k for k in D.resto if k in setpar],
          'todas': par}
    conf = {'pacotes': len(D.chaves), 'L_secoes': len(D.L), 'L_locais': len(set(D.local[k] for k in D.L)),
            'L_locais_cortados_no_fim': D.L_locais_cortados, 'M10_secoes': len(D.M10), 'resto_secoes': len(D.resto),
            'pares': len(par), 'so_2T_no_log': len(D.so2), 'pares_por_amostra': {a: len(v) for a, v in am.items()},
            'so_2T_por_amostra': dict(collections.Counter(D.amostra_de[k] for k in D.so2))}
    bate = collections.Counter()
    for k in D.chaves:
        for di, t in ((0, '1'), (1, '2')):
            r = D.rec[k][di]
            if r is None:
                continue
            nv = len(r['tcomp']) + r['voto_sem_hab']
            bate['log_igual_bweb_%sT' % t if nv == D.base[k][t]['comp'] else 'log_difere_bweb_%sT' % t] += 1
            bate['voto_sem_hab_%sT' % t] += r['voto_sem_hab']
            bate['hab_sem_voto_%sT' % t] += r['hab_sem_voto']
            bate['recuos_de_relogio_%sT' % t] += len(r['retro_ev'])
            bate['votos_de_outra_secao_no_pacote_%sT' % t] += r['votos_outra_secao']
            bate['secoes_com_2_blocos_%sT' % t] += int(r['nseg'] >= 2)
            bate['sem_urna_pronta_%sT' % t] += int(r['pronta'] is None)
            bate['sem_inicio_encerramento_%sT' % t] += int(r['ini_enc'] is None)
    conf['log_contra_bweb'] = dict(bate)
    conf['trechos_de_outra_secao_dentro_de_pacotes'] = D.outra_secao
    try:
        conf['leitor_contra_extrator_de_referencia_do_desenhista'] = conferir_leitor()
    except Exception as ex:
        conf['leitor_contra_extrator_de_referencia_do_desenhista'] = {'erro': repr(ex)}
    conf['urna_diferente_entre_turnos_na_base'] = {a: int(sum(1 for k in v if D.base[k]['1']['urna'] != D.base[k]['2']['urna'])) for a, v in am.items()}
    conf['fuso'] = dict(collections.Counter(int(D.off[k] // 3600) for k in D.chaves))
    R['amostra_e_conferencias'] = conf
    print('amostra', conf['pares_por_amostra'], flush=True)

    # ------------------------------------------------------------------ D2-2: tabelas e estimativas
    S1, S2 = D.tabela22()
    idx = {a: np.array([D.ix[k] for k in v], int) for a, v in am.items()}
    cl = {'L': D.conglomerado(am['L'], 'local'), 'M10': D.conglomerado(am['M10'], 'mun'),
          'resto': D.conglomerado(am['resto'], 'local'), 'todas': D.conglomerado(am['todas'], 'local')}
    d22 = {}
    for a in ('L', 'M10', 'resto', 'todas'):
        av, G = avaliar(deriv22, S1[idx[a]], S2[idx[a]], cl[a])
        d22[a] = {'secoes': len(idx[a]), 'conglomerados': G,
                  'totais_1T': {n: float(S1[idx[a]][:, i].sum()) for n, i in I22.items()},
                  'totais_2T': {n: float(S2[idx[a]][:, i].sum()) for n, i in I22.items()}, 'estimativas': av}
        if a == 'resto':
            d22[a]['aviso'] = 'amostra avulsa; IC por seção isolada, só indicativo'
    # conferência: MAN do log contra QT_ELEI_BIOM_SEM_HABILITACAO do bweb (extração de estrutura da B2)
    try:
        D.est = carrega_estrutura_b2()
        H = {t: {k: D.est[t][k][1] for k in par if k in D.est[t]} for t in ('1', '2')}
        cfh = {}
        for t, S in (('1', S1), ('2', S2)):
            ig = sum(1 for k in par if k in H[t] and H[t][k] == S[D.ix[k], I22['MAN']])
            cfh['MAN_log_igual_H_bweb_%sT' % t] = [ig, sum(1 for k in par if k in H[t])]
        d22['conferencia_MAN_contra_bweb'] = cfh
    except Exception as ex:  # a conferência depende de arquivo de outro teste; se faltar, segue
        d22['conferencia_MAN_contra_bweb'] = {'erro': str(ex)}
        H = None
    R['D2_2'] = d22
    _grava_parcial('parcial_d22_estimativas.json', d22)
    print('D2-2 estimativas', round(time.time() - t0), 's', flush=True)

    # ------------------------------------------------------------------ D2-2: B6 (reservatório)
    pf = json.load(gzip.open(TRAB + '/perfil_amostra.json.gz', 'rt'))
    perfil, agreg = pf['perfil'], pf['agregadas']
    b6 = {'1': [], '2': []}
    b6res = {}
    tot_res = {'eleitores_perfil': 0, 'sem_biometria_perfil': 0, 'ANO_1T': 0, 'ANO_2T': 0, 'aptos_2T': 0}
    sem_perfil = 0
    res_sec = {}
    for k in par:
        i = D.ix[k]
        linha = {}
        for t in ('1', '2'):
            secs = [k] + ['|'.join(k.split('|')[:3]) + '|' + str(s) for s in agreg[t].get(k, [])]
            if any(s not in perfil for s in secs):
                linha[t] = None
                continue
            el = sum(perfil[s][0] for s in secs)
            sb = sum(perfil[s][0] - perfil[s][1] for s in secs)
            linha[t] = (el, sb)
        if linha['1'] is None or linha['2'] is None:
            sem_perfil += 1
            continue
        res_sec[k] = linha
        a1 = S1[i, I22['ANO']]
        a2 = S2[i, I22['ANO']]
        if D.amostra_de[k] == 'L':
            tot_res['eleitores_perfil'] += linha['2'][0]
            tot_res['sem_biometria_perfil'] += linha['2'][1]
            tot_res['ANO_1T'] += a1
            tot_res['ANO_2T'] += a2
            tot_res['aptos_2T'] += D.base[k]['2']['apt']
        for t, a in (('1', a1), ('2', a2)):
            el, sb = linha[t]
            if a > sb + 2:
                apt = D.base[k][t]['apt']
                ea = abs(apt - el) > 2
                eb = (t == '2' and a1 > linha['1'][1] + 2 and a1 >= a2 - 2)
                b6[t].append({'secao': k, 'amostra': D.amostra_de[k], 'ANO': int(a), 'sem_biometria_perfil': int(sb),
                              'excesso': int(a - sb), 'aptos_bweb': int(apt), 'eleitores_perfil': int(el),
                              'ANO_outro_turno': int(a2 if t == '1' else a1), 'explica_a_aptos_diferem': bool(ea),
                              'explica_b_ja_no_1T': bool(eb), 'agregadas': len(agreg[t].get(k, []))})
    for t in ('1', '2'):
        ls = b6[t]
        b6res[t + 'T'] = {'secoes_acima_do_reservatorio_mais_2': len(ls),
                          'por_amostra': dict(collections.Counter(x['amostra'] for x in ls)),
                          'com_explicacao_a': sum(1 for x in ls if x['explica_a_aptos_diferem']),
                          'com_explicacao_b': sum(1 for x in ls if x['explica_b_ja_no_1T']),
                          'sem_explicacao': sum(1 for x in ls if not x['explica_a_aptos_diferem'] and not x['explica_b_ja_no_1T']),
                          'excesso_total_votos': int(sum(x['excesso'] for x in ls)),
                          'lista': sorted(ls, key=lambda x: -x['excesso'])[:60]}
    b6res['secoes_pares_sem_perfil'] = sem_perfil
    b6res['L_totais'] = {k: float(v) for k, v in tot_res.items()}
    b6res['L_uso_do_reservatorio'] = {'ANO_1T_sobre_sem_biometria': tot_res['ANO_1T'] / max(tot_res['sem_biometria_perfil'], 1),
                                      'ANO_2T_sobre_sem_biometria': tot_res['ANO_2T'] / max(tot_res['sem_biometria_perfil'], 1)}
    # distribuição de ANO menos reservatório (para ver se a marca de biometria do perfil e a da urna coincidem)
    dif = {'1': [], '2': []}
    for k, linha in res_sec.items():
        i = D.ix[k]
        dif['1'].append(S1[i, I22['ANO']] - linha['1'][1])
        dif['2'].append(S2[i, I22['ANO']] - linha['2'][1])
    for t in ('1', '2'):
        x = np.array(dif[t])
        b6res[t + 'T']['ANO_menos_reservatorio'] = {'secoes': int(len(x)), 'acima_de_0': int((x > 0).sum()), 'acima_de_2': int((x > 2).sum()),
                                                     'acima_de_5': int((x > 5).sum()), 'acima_de_10': int((x > 10).sum()),
                                                     'maximo': float(x.max())}
    R['D2_2']['B6'] = b6res
    _grava_parcial('parcial_d22_b6.json', b6res)

    # ------------------------------------------------------------------ D2-2: B7 (elo com o voto)
    def x_b7(chs, S1x, S2x):
        ii = np.array([D.ix[k] for k in chs], int)
        v = D.vetores_voto(chs)
        C1 = v['C1']
        nb1 = S1x[ii, I22['ANO']] + S1x[ii, I22['MAN']]
        nb2 = S2x[ii, I22['ANO']] + S2x[ii, I22['MAN']]
        return ii, C1, nb1, nb2

    def roda_b7(chs, S1x, S2x, delta=None, completo=True):
        ii, C1, nb1, nb2 = x_b7(chs, S1x, S2x)
        H1v = S1x[ii, I22['MAN']]
        o = {'x_total': regs_elo(D, chs, {'x': (nb2 - nb1) / C1}, H1v, 'local', delta)}
        s1, s2 = S1x[ii, I22['susp']], S2x[ii, I22['susp']]
        o['x_suspeito_e_comum'] = regs_elo(D, chs, {'suspeito': (s2 - s1) / C1, 'comum': ((nb2 - s2) - (nb1 - s1)) / C1}, H1v, 'local', delta)
        if completo:
            sl1, sl2 = S1x[ii, I22['susp_l']], S2x[ii, I22['susp_l']]
            o['ao_lado_suspeito_com_nao_associado'] = regs_elo(D, chs, {'suspeito': (sl2 - sl1) / C1, 'comum': ((nb2 - sl2) - (nb1 - sl1)) / C1}, H1v, 'local', delta)
            o['ao_lado_com_ANO1'] = regs_elo(D, chs, {'x': (nb2 - nb1) / C1}, H1v, 'local', delta, extras={'ANO1': S1x[ii, I22['ANO']] / C1})
            o['ao_lado_ANO_e_MAN_separados'] = regs_elo(D, chs, {'dANO': (S2x[ii, I22['ANO']] - S1x[ii, I22['ANO']]) / C1,
                                                                 'dMAN': (S2x[ii, I22['MAN']] - S1x[ii, I22['MAN']]) / C1}, H1v, 'local', delta)
            o['ao_lado_erro_por_municipio'] = regs_elo(D, chs, {'x': (nb2 - nb1) / C1}, H1v, 'mun', delta)
            # sem o controle de comparecimento
            v = D.vetores_voto(chs, delta)
            y = ((v['L2'] - v['R2']) - (v['L1'] - v['R1'])) / C1
            X = np.column_stack([(nb2 - nb1) / C1, v['O1'] / C1, (v['B1'] + v['N1']) / C1, v['L1'] / C1, H1v / C1, v['U']])
            r = fe_reg(y, X, D.conglomerado(chs, 'local'), C1, D.conglomerado(chs, 'local'), ['x', 'O1', 'BN1', 'L1', 'H1', 'urna_trocada'])
            o['ao_lado_sem_controle_de_comparecimento'] = {'coef': r['coef']['x'], 'ep': r['ep']['x'], 'ic95': _ic(r['coef']['x'], r['ep']['x']), 'n': r['n']}
        return o

    b7 = {a: roda_b7(am[a], S1, S2) for a in ('L', 'M10', 'todas')}
    R['D2_2']['B7'] = b7
    _grava_parcial('parcial_d22_b7.json', b7)
    print('D2-2 B6 e B7', round(time.time() - t0), 's', flush=True)

    # ------------------------------------------------------------------ D2-2: lista local
    lista = []
    cont_l = collections.Counter()
    for k in D.chaves:
        r2 = D.rec[k][1]
        if r2 is None:
            continue
        v2 = S2[D.ix[k]] if k in D.ix else st22(r2, [SEMENTE, 999999, 2])
        v1 = S1[D.ix[k]] if k in D.ix else None
        man2 = v2[I22['MAN']]
        f2 = v2[I22['MAN_NOVO']] / man2 if man2 > 0 else 0.0
        c_fim = v2[I22['n_fim']] >= 5
        c_dedo = f2 > 0.30
        c_res = any(x['secao'] == k for x in b6['2'])
        if v1 is not None:
            man1 = v1[I22['MAN']]
            f1 = v1[I22['MAN_NOVO']] / man1 if man1 > 0 else 0.0
            cont_l['1T_n_fim_5'] += int(v1[I22['n_fim']] >= 5)
            cont_l['1T_dedo_novo_30'] += int(f1 > 0.30)
            cont_l['1T_dedo_novo_30_com_5_liberacoes'] += int(f1 > 0.30 and man1 >= 5)
            cont_l['2T_pares_n_fim_5'] += int(c_fim)
            cont_l['2T_pares_dedo_novo_30'] += int(c_dedo)
            cont_l['2T_pares_dedo_novo_30_com_5_liberacoes'] += int(c_dedo and man2 >= 5)
            cont_l['dedo_novo_30_nos_dois_turnos'] += int(c_dedo and f1 > 0.30)
            cont_l['dedo_novo_30_so_no_2T'] += int(c_dedo and not f1 > 0.30)
            cont_l['dedo_novo_30_so_no_1T'] += int(f1 > 0.30 and not c_dedo)
        cont_l['2T_n_fim_5'] += int(c_fim)
        cont_l['2T_dedo_novo_30'] += int(c_dedo)
        cont_l['2T_dedo_novo_30_com_5_liberacoes'] += int(c_dedo and man2 >= 5)
        cont_l['2T_acima_do_reservatorio'] += int(c_res)
        if c_fim or c_dedo or c_res:
            lista.append([k, D.amostra_de[k], int(v2[I22['C']]), int(v2[I22['ANO']]), int(man2), int(v2[I22['MAN_NOVO']]),
                          round(f2, 3), int(v2[I22['n_fim']]), int(c_fim), int(c_dedo), int(c_res),
                          int(v1[I22['n_fim']]) if v1 is not None else '', int(v1[I22['MAN']]) if v1 is not None else '',
                          int(v1[I22['MAN_NOVO']]) if v1 is not None else ''])
    cont_l['secoes_na_lista'] = len(lista)
    with open(REPO + '/resultados/R27_C1_lista_local.csv', 'w') as f:
        f.write('secao;amostra;votos_2T;ANO_2T;MAN_2T;MAN_dedo_novo_2T;fracao_dedo_novo_2T;n_fim_2T;cond_n_fim_5;cond_dedo_novo_30;'
                'cond_acima_reservatorio;n_fim_1T;MAN_1T;MAN_dedo_novo_1T\n')
        for l in sorted(lista, key=lambda x: (-x[8], -x[10], -x[7], x[0])):
            f.write(';'.join(str(x) for x in l) + '\n')
    R['D2_2']['lista_local'] = {'contagens': dict(cont_l), 'arquivo': 'resultados/R27_C1_lista_local.csv',
                                'maiores_n_fim_2T': sorted([l for l in lista if l[8]], key=lambda x: -x[7])[:25]}

    # ------------------------------------------------------------------ D2-2: plantios (calibração)
    cal = {}
    Lk = am['L']
    iL = idx['L']
    base_av = d22['L']['estimativas']

    def avalia_plantio(recs, delta, completo_b7=False):
        S2p = S2.copy()
        for k, r in recs.items():
            S2p[D.ix[k]] = st22(r, [SEMENTE, D.ix[k], 2])
        av, _ = avaliar(deriv22, S1[iL], S2p[iL], cl['L'])
        nomes = ['s_ANO', 's_MAN', 'ln_rho', 'X_frac', 'V', 'V_MAN', 'V_ANO', 'B3', 'B4', 'B3B4', 'B34_uniao', 'B5_dedo_dif', 'B5_semcapt_dif', 'plac_did']
        o = {'estimativas': _resumo(av, nomes), 'S2p': S2p}
        b = roda_b7(Lk, S1, S2p, delta, completo=False)
        o['B7'] = {'gama': b['x_total']['margem']['coef']['x'], 'ep': b['x_total']['margem']['ep']['x'],
                   'ic95': b['x_total']['margem']['ic95']['x'],
                   'gama_suspeito': b['x_suspeito_e_comum']['margem']['coef'].get('suspeito'),
                   'ep_suspeito': b['x_suspeito_e_comum']['margem']['ep'].get('suspeito'),
                   'gama_comum': b['x_suspeito_e_comum']['margem']['coef'].get('comum'),
                   'ep_comum': b['x_suspeito_e_comum']['margem']['ep'].get('comum'),
                   'ganho_L': b['x_total']['ganho_L']['coef']['x'], 'ganho_R': b['x_total']['ganho_R']['coef']['x']}
        return o

    def veredito22(av, gama, gama_ic, plac_ok=True, b6_sem=0, diverge=False):
        V = av['V']
        b34 = av['B3B4']
        conf_ok = (b34['valor'] >= L10) or (gama is not None and gama >= 0.30 and gama_ic[0] > 0)
        if V['valor'] >= L25 and V['ic95'][0] >= L10 and conf_ok and plac_ok:
            return 'SINAL'
        if b6_sem > 0 or diverge:
            return 'INCONCLUSIVO'
        if V['ic95'][1] < L10 and b34['ic95'][1] < L10:
            return 'SEM SINAL'
        return 'INCONCLUSIVO'

    C2L = S2[iL, I22['C']].sum()
    for rot, p in (('a_uniforme_MAN_0864', 0.00864), ('a_uniforme_MAN_0345', 0.00345)):
        rng = np.random.default_rng([SEMENTE, 22, int(p * 1e5)])
        recs, delta, tot = plantio_uniforme(D, Lk, p, MAN_MES, rng)
        o = avalia_plantio(recs, delta)
        S2p = o.pop('S2p')
        o['votos_plantados'] = tot
        o['fracao_plantada'] = tot / (C2L + tot)
        o['equivalente_nacional'] = tot / (C2L + tot) * N2
        o['efeito_em_ln_rho'] = o['estimativas']['ln_rho']['valor'] - base_av['ln_rho']['valor']
        o['efeito_em_X_frac'] = o['estimativas']['X_frac']['valor'] - base_av['X_frac']['valor']
        o['efeito_em_V'] = o['estimativas']['V']['valor'] - base_av['V']['valor']
        o['veredito_que_o_teste_daria'] = veredito22(o['estimativas'], o['B7']['gama'], o['B7']['ic95'])
        cal[rot] = o
    for rot, frac_sec, alvo in (('b_concentrado_30_ANO_em_5pct', 0.05, None), ('b_concentrado_30_ANO_somando_0345', None, 0.00345),
                                ('b_concentrado_30_ANO_somando_0864', None, 0.00864)):
        if frac_sec is None:
            frac_sec = alvo * C2L / (30.0 * len(Lk))
        rng = np.random.default_rng([SEMENTE, 23, int(frac_sec * 1e6)])
        recs, delta, tot, esc = plantio_concentrado(D, Lk, frac_sec, 30, rng)
        o = avalia_plantio(recs, delta)
        S2p = o.pop('S2p')
        ie = np.array([D.ix[k] for k in esc], int)
        o['secoes_plantadas'] = len(esc)
        o['votos_plantados'] = tot
        o['fracao_plantada'] = tot / (C2L + tot)
        o['equivalente_nacional'] = tot / (C2L + tot) * N2
        o['B3_votos_acusados'] = float((S2p[ie, I22['S_fim']] - S2[ie, I22['S_fim']]).sum())
        o['B4_votos_acusados'] = float((S2p[ie, I22['seq4']] - S2[ie, I22['seq4']]).sum())
        o['B3_fracao_acusada'] = o['B3_votos_acusados'] / tot
        o['B4_fracao_acusada'] = o['B4_votos_acusados'] / tot
        o['secoes_plantadas_com_n_fim_5'] = int((S2p[ie, I22['n_fim']] >= 5).sum())
        o['efeito_em_B3B4'] = o['estimativas']['B3B4']['valor'] - base_av['B3B4']['valor']
        o['efeito_em_V'] = o['estimativas']['V']['valor'] - base_av['V']['valor']
        o['veredito_que_o_teste_daria'] = veredito22(o['estimativas'], o['B7']['gama'], o['B7']['ic95'])
        cal[rot] = o
    # explicações inocentes
    rng = np.random.default_rng([SEMENTE, 24])
    recs, delta, tot = plantio_uniforme(D, Lk, 0.00864, ANO, rng, como_secao=True)
    o = avalia_plantio(recs, delta)
    o.pop('S2p')
    o['votos_plantados'] = tot
    o['equivalente_nacional'] = tot / (C2L + tot) * N2
    o['efeito_em_V'] = o['estimativas']['V']['valor'] - base_av['V']['valor']
    o['veredito_que_o_teste_daria'] = veredito22(o['estimativas'], o['B7']['gama'], o['B7']['ic95'])
    cal['i1_inocente_eleitores_reais_sem_biometria_0864'] = o
    rng = np.random.default_rng([SEMENTE, 25])
    recs, info = plantio_leitor_pior(D, Lk, S2[iL], rng)
    o = avalia_plantio(recs, None)
    o.pop('S2p')
    o.update(info)
    o['efeito_em_V'] = o['estimativas']['V']['valor'] - base_av['V']['valor']
    o['efeito_em_s_MAN'] = o['estimativas']['s_MAN']['valor'] - base_av['s_MAN']['valor']
    o['efeito_em_ln_rho'] = o['estimativas']['ln_rho']['valor'] - base_av['ln_rho']['valor']
    o['veredito_que_o_teste_daria'] = veredito22(o['estimativas'], o['B7']['gama'], o['B7']['ic95'])
    cal['i2_inocente_leitor_pior_115'] = o
    rng = np.random.default_rng([SEMENTE, 26])
    recs, delta, tot = plantio_abstencao(D, Lk, 0.0357, rng)
    o = avalia_plantio(recs, delta)
    o.pop('S2p')
    o['votos_retirados'] = tot
    o['efeito_em_V'] = o['estimativas']['V']['valor'] - base_av['V']['valor']
    o['veredito_que_o_teste_daria'] = veredito22(o['estimativas'], o['B7']['gama'], o['B7']['ic95'])
    cal['i3_inocente_abstencao_pura_357_de_Flavio'] = o
    a0 = cal['a_uniforme_MAN_0864']
    b0 = cal['b_concentrado_30_ANO_em_5pct']
    cal['tem_poder'] = bool(0.08 <= a0['efeito_em_ln_rho'] <= 0.14 and 0.007 <= a0['efeito_em_X_frac'] <= 0.010
                            and b0['B3_fracao_acusada'] >= 0.9 and b0['B4_fracao_acusada'] >= 0.9)
    R['D2_2']['calibracao'] = cal
    _grava_parcial('parcial_d22_calibracao.json', cal)
    print('D2-2 calibração', round(time.time() - t0), 's', flush=True)

    # ------------------------------------------------------------------ D2-2: veredito
    eL = d22['L']['estimativas']
    eM = d22['M10']['estimativas']
    g7 = b7['L']['x_total']['margem']
    diverge = eL['V']['ic95'][1] < eM['V']['ic95'][0] or eM['V']['ic95'][1] < eL['V']['ic95'][0]
    plac_explica = abs(eL['plac_ln_tarde_manha_1T']['valor']) >= abs(eL['ln_rho']['valor'])
    b6_sem = b6res['2T']['sem_explicacao']
    ver22 = veredito22(eL, g7['coef']['x'], g7['ic95']['x'], plac_ok=not plac_explica, b6_sem=b6_sem, diverge=diverge)
    ver22_sem_b6 = veredito22(eL, g7['coef']['x'], g7['ic95']['x'], plac_ok=not plac_explica, b6_sem=0, diverge=diverge)
    if not cal['tem_poder']:
        ver22_final = 'SEM PODER'
    else:
        ver22_final = ver22
    R['D2_2']['veredito'] = {
        'pela_letra': ver22_final, 'pela_letra_sem_a_clausula_B6': ver22_sem_b6, 'calibracao_tem_poder': cal['tem_poder'],
        'V': eL['V'], 'V_parte_MAN_razao_de_cauda': eL['V_MAN'], 'V_parte_ANO': eL['V_ANO'], 'ln_rho': eL['ln_rho'], 's_ANO': eL['s_ANO'],
        's_MAN': eL['s_MAN'], 'B3B4': eL['B3B4'], 'gama_B7': {'coef': g7['coef']['x'], 'ep': g7['ep']['x'], 'ic95': g7['ic95']['x']},
        'clausulas': {'V_ge_1107548': eL['V']['valor'] >= L25, 'V_limite_inferior_ge_443019': eL['V']['ic95'][0] >= L10,
                      'V_limite_superior_lt_443019': eL['V']['ic95'][1] < L10, 'B3B4_ge_443019': eL['B3B4']['valor'] >= L10,
                      'B3B4_limite_superior_lt_443019': eL['B3B4']['ic95'][1] < L10,
                      'gama_ge_030_com_IC_sem_zero': bool(g7['coef']['x'] >= 0.30 and g7['ic95']['x'][0] > 0),
                      'divergencia_L_M10': bool(diverge), 'B6_2T_sem_explicacao_cadastral': int(b6_sem),
                      'placebo_manha_tarde_explicaria': bool(plac_explica)},
        'V_em_fracao_da_margem': eL['V']['valor'] / MARGEM, 'V_limite_superior_em_fracao_da_margem': eL['V']['ic95'][1] / MARGEM}
    _grava_parcial('parcial_d22_veredito.json', R['D2_2']['veredito'])
    print('D2-2 veredito', ver22_final, round(time.time() - t0), 's', flush=True)

    # ------------------------------------------------------------------ D2-5: tabelas e estimativas
    T1, T2 = D.tabela25()
    d25 = {}
    for a in ('L', 'M10', 'resto', 'todas'):
        av, G = avaliar(deriv25, T1[idx[a]], T2[idx[a]], cl[a])
        d25[a] = {'secoes': len(idx[a]), 'conglomerados': G,
                  'totais_1T': {n: float(T1[idx[a]][:, i].sum()) for n, i in I25.items()},
                  'totais_2T': {n: float(T2[idx[a]][:, i].sum()) for n, i in I25.items()}, 'estimativas': av}
    # seções só com o 2T no log (limiar de 22 s)
    so2 = {}
    if D.so2:
        Tso = np.array([st25(D.rec[k][1], 22.0, D.off[k]) for k in D.so2])
        so2 = {'secoes': len(D.so2), 'totais_2T': {n: float(Tso[:, i].sum()) for n, i in I25.items()}}
    d25['so_2T_no_log'] = so2
    thr = np.array([D.thr[k] for k in par])
    d25['limiar_rajada'] = {'secoes_com_limiar_proprio': int(sum(1 for k in par if D.thr[k] != 22.0 or len(D.rec[k][0]['tcomp']) > 100)),
                            'percentis_do_limiar_p5_p50_p95': [float(x) for x in np.percentile(thr, [5, 50, 95])], 'minimo': float(thr.min()), 'maximo': float(thr.max())}
    # distribuição de g, d, c por turno (L), para o leitor ver os pisos
    dist = {}
    for di, t in ((0, '1T'), (1, '2T')):
        gs, ds, cs = [], [], []
        for k in am['L']:
            g, d, c = intervalos(D.rec[k][di])
            gs.append(g[~np.isnan(g)])
            ds.append(d)
            cs.append(c[~np.isnan(c)])
        gs, ds, cs = np.concatenate(gs), np.concatenate(ds), np.concatenate(cs)
        dist[t] = {'votos_com_g': int(len(gs)),
                   'g_percentis_0.01_0.1_1_5_50': [float(x) for x in np.percentile(gs, [0.01, 0.1, 1, 5, 50])], 'g_minimo': float(gs.min()),
                   'd_percentis_0.01_0.1_1_5_50': [float(x) for x in np.percentile(ds, [0.01, 0.1, 1, 5, 50])], 'd_minimo': float(ds.min()),
                   'c_percentis_0.01_0.1_1_5_50': [float(x) for x in np.percentile(cs, [0.01, 0.1, 1, 5, 50])], 'c_minimo': float(cs.min())}
    d25['distribuicao_de_tempos_L'] = dist
    R['D2_5'] = d25
    _grava_parcial('parcial_d25_estimativas.json', d25)
    print('D2-5 estimativas', round(time.time() - t0), 's', flush=True)

    # ------------------------------------------------------------------ D2-5: elo na amostra
    def roda_elo25(chs, T1x, T2x, delta=None):
        ii = np.array([D.ix[k] for k in chs], int)
        v = D.vetores_voto(chs, delta)
        H1v = S1[ii, I22['MAN']]
        x = T2x[ii, I25['U_full']] / T2x[ii, I25['C']]
        o = {'erro_por_municipio': regs_elo(D, chs, {'x': x}, H1v, 'mun', delta),
             'erro_por_local': regs_elo(D, chs, {'x': x}, H1v, 'local', delta)}
        o['x_media'] = float(np.average(x, weights=v['C1']))
        o['secoes_com_x_positivo'] = int((x > 0).sum())
        for nome in ('T17', 'T17o', 'RAJ', 'IMP_full'):
            xx = T2x[ii, I25[nome]] / T2x[ii, I25['C']]
            if (xx > 0).sum() >= 5:
                r = regs_elo(D, chs, {'x': xx}, H1v, 'mun', delta)
                o['ao_lado_x_' + nome] = {q: {'coef': r[q]['coef']['x'], 'ep': r[q]['ep']['x'], 'ic95': r[q]['ic95']['x']} for q in r}
                o['ao_lado_x_' + nome]['secoes_com_x_positivo'] = int((xx > 0).sum())
        # corte no 1T: fatia do 13 contra a fração de votos nas categorias no 1T
        x1 = T1x[ii, I25['U_letra']] / T1x[ii, I25['C']]
        val1 = v['L1'] + v['R1'] + v['O1']
        if (x1 > 0).sum() >= 5:
            r = fe_reg(v['L1'] / val1, x1[:, None], D.conglomerado(chs, 'local'), v['C1'], D.conglomerado(chs, 'mun'), ['x1'])
            o['corte_1T'] = {'coef': r['coef'].get('x1'), 'ep': r['ep'].get('x1'), 'n': r['n'], 'secoes_com_x_positivo': int((x1 > 0).sum())}
        return o

    elo25 = {a: roda_elo25(am[a], T1, T2) for a in ('L', 'M10', 'todas')}
    R['D2_5']['elo_amostra'] = elo25
    _grava_parcial('parcial_d25_elo.json', elo25)
    print('D2-5 elo', round(time.time() - t0), 's', flush=True)

    # ------------------------------------------------------------------ D2-5: lista IMP com trecho do log
    casos = []
    for k in D.chaves:
        for di, t in ((0, '1T'), (1, '2T')):
            r = D.rec[k][di]
            if r is None:
                continue
            m = cat25(r, D.thr[k], D.off[k])
            for regra in ('imp_g', 'imp_d', 'imp_c', 'imp_pre', 'imp_pos', 'imp_retro'):
                for i in np.nonzero(m[regra])[0]:
                    casos.append({'secao': k, 'amostra': D.amostra_de[k], 'turno': t, 'regra': regra, 'hora_local': _hms(r['tcomp'][i]),
                                  'g': None if np.isnan(m['_g'][i]) else float(m['_g'][i]), 'd': float(m['_d'][i]),
                                  'c': None if np.isnan(m['_c'][i]) else float(m['_c'][i]), 'classe': NOMES_CLASSE[int(r['cls'][i])],
                                  'bloco': r['blocos'][int(r['seg'][i])], 'linha': int(r['li'][i]),
                                  'pronta': _hms(r['pronta']), 'inicio_encerramento': _hms(r['ini_enc'])})
            for (li, ta, tb, pa, pb, blo) in r['retro_ev']:
                casos.append({'secao': k, 'amostra': D.amostra_de[k], 'turno': t, 'regra': 'recuo_de_relogio_no_dia', 'hora_local': _hms(tb),
                              'de': _hms(ta), 'apps': pa + '>' + pb, 'linha': int(li), 'bloco': blo})
    cont_imp = collections.Counter((c['turno'], c['regra']) for c in casos)
    por_regra = collections.defaultdict(list)
    for c in casos:
        por_regra[(c['turno'], c['regra'])].append(c)
    with open(REPO + '/resultados/R27_C1_lista_IMP.csv', 'w') as f:
        f.write('secao;amostra;turno;regra;hora_local;g;d;c;classe;urna_pronta;inicio_encerramento\n')
        for c in sorted(casos, key=lambda c: (c['turno'], c['regra'], c['secao'], c['hora_local'])):
            f.write(';'.join(str(c.get(x, '')) for x in ('secao', 'amostra', 'turno', 'regra', 'hora_local', 'g', 'd', 'c', 'classe', 'pronta', 'inicio_encerramento')) + '\n')
    with open(REPO + '/resultados/R27_C1_trechos_IMP.txt', 'w') as f:
        f.write('R27_C1: trechos do log dos votos marcados como IMP (12 linhas antes e 4 depois; até 300 casos por regra e turno).\n')
        f.write('A última coluna do log (código de verificação da linha) foi cortada. O log não traz o candidato votado.\n\n')
        for (t, regra), cs in sorted(por_regra.items()):
            f.write(f'=== {t} {regra}: {len(cs)} casos ===\n')
            for c in sorted(cs, key=lambda c: (c['secao'], c['hora_local']))[:300]:
                f.write(f"--- {c['secao']} {t} {regra} {c['hora_local']} g={c.get('g')} d={c.get('d')} c={c.get('c')} classe={c.get('classe')}\n")
                try:
                    for l in _trecho(D.arquivo[c['secao']], c.get('bloco'), c['linha'], 12, 4):
                        f.write('    ' + l + '\n')
                except Exception as ex:
                    f.write('    (trecho não lido: %s)\n' % ex)
            f.write('\n')
    R['D2_5']['lista_IMP'] = {'contagem_por_turno_e_regra': {f'{t} {r}': n for (t, r), n in sorted(cont_imp.items())},
                              'secoes_com_algum_IMP_2T': len({c['secao'] for c in casos if c['turno'] == '2T' and c['regra'] != 'recuo_de_relogio_no_dia'}),
                              'arquivos': ['resultados/R27_C1_lista_IMP.csv', 'resultados/R27_C1_trechos_IMP.txt'],
                              'exemplos': sorted([c for c in casos if c['turno'] == '2T'], key=lambda c: (c['regra'], c.get('g') or 0))[:40]}
    print('D2-5 lista IMP', len(casos), round(time.time() - t0), 's', flush=True)

    # ------------------------------------------------------------------ D2-5: plantios
    cal5 = {}
    rng = np.random.default_rng([SEMENTE, 51])
    nsec = max(1, int(round(0.05 * len(Lk))))
    esc = [Lk[i] for i in sorted(rng.choice(len(Lk), size=nsec, replace=False))]
    base5 = d25['L']['estimativas']
    C2L5 = T2[iL, I25['C']].sum()

    def veredito25(av, elo_coef, elo_ic, censo_pos=False):
        V = av['V']
        if av['taxa_RAJ_1T']['valor'] > 0.001:
            return 'INCONCLUSIVO'
        elo_pos = (elo_ic is not None and elo_ic[0] > 0) or censo_pos
        if V['valor'] >= L25 and V['ic95'][0] >= L10 and av['razao_taxas']['valor'] >= 3 and elo_pos:
            return 'SINAL'
        if av['nac_T17_2T']['ic95'][1] < L10 and av['nac_IR_full_2T']['ic95'][1] < L10:
            return 'SEM SINAL'
        if av['nac_U_full_2T']['ic95'][1] < L10 and elo_ic is not None and elo_ic[1] < 0.10:
            return 'SEM SINAL'
        return 'INCONCLUSIVO'

    def avalia5(recs, delta, nb):
        T2p = T2.copy()
        for k, r in recs.items():
            T2p[D.ix[k]] = st25(r, D.thr[k], D.off[k])
        av, _ = avaliar(deriv25, T1[iL], T2p[iL], cl['L'])
        ie = np.array([D.ix[k] for k in recs], int)
        tot = nb * len(recs)
        o = {'secoes_plantadas': len(recs), 'votos_plantados': tot, 'fracao_plantada': tot / (C2L5 + tot),
             'equivalente_nacional': tot / (C2L5 + tot) * N2}
        for nome in ('RAJ', 'T17', 'T17o', 'T17o_estrita', 'IMP_full', 'U_full'):
            o['acusados_' + nome] = float((T2p[ie, I25[nome]] - T2[ie, I25[nome]]).sum())
            o['fracao_acusada_' + nome] = o['acusados_' + nome] / tot
        o['estimativas'] = _resumo(av, ['V', 'razao_taxas', 'nac_U_full_2T', 'nac_T17_2T', 'nac_T17o_2T', 'nac_RAJ_2T', 'nac_IR_full_2T', 'taxa_RAJ_1T', 'ln_OR2_OR1'])
        o['efeito_em_V'] = av['V']['valor'] - base5['V']['valor']
        o['fracao_recuperada_em_V'] = o['efeito_em_V'] / N2
        e = roda_elo25(Lk, T1, T2p, delta)['erro_por_municipio']
        o['elo'] = {'coef': e['margem']['coef']['x'], 'ep': e['margem']['ep']['x'], 'ic95': e['margem']['ic95']['x'],
                    'ganho_L': e['ganho_L']['coef']['x'], 'ganho_R': e['ganho_R']['coef']['x']}
        o['veredito_que_o_teste_daria'] = veredito25(av, o['elo']['coef'], o['elo']['ic95'])
        return o

    for rot, nb, espera, fila in (('p40_bloco_40_ciclos_20s_apos_20min', 40, 1200.0, False), ('p15_bloco_15_ciclos_20s_apos_20min', 15, 1200.0, False),
                                  ('p40c_bloco_40_colado_ao_ultimo_voto', 40, 20.0, False), ('fila_inocente_40_eleitores_reais_em_fila', 40, 0.0, True)):
        rngp = np.random.default_rng([SEMENTE, 52, nb, int(espera), int(fila)])
        recs, delta = plantio_bloco_tempo(D, esc, nb, espera, rngp, fila=fila)
        cal5[rot] = avalia5(recs, delta, nb)
    cal5['tem_poder'] = bool(0.006 <= cal5['p40_bloco_40_ciclos_20s_apos_20min']['fracao_recuperada_em_V'] <= 0.0095)
    R['D2_5']['calibracao'] = cal5
    _grava_parcial('parcial_d25_calibracao.json', cal5)
    print('D2-5 calibração', round(time.time() - t0), 's', flush=True)

    # ------------------------------------------------------------------ D2-5: censo dos encerramentos
    censo = censo_encerramentos(D)
    R['D2_5']['censo'] = censo
    _grava_parcial('parcial_d25_censo.json', censo)
    print('D2-5 censo', round(time.time() - t0), 's', flush=True)

    # ------------------------------------------------------------------ D2-5: veredito
    e5 = d25['L']['estimativas']
    eloL = elo25['L']['erro_por_municipio']['margem']
    censo_pos = bool(censo.get('regressao_tardia2', {}).get('margem', {}).get('ic95', [0, 0])[0] > 0)
    ver25 = veredito25(e5, eloL['coef']['x'], eloL['ic95']['x'], censo_pos)
    ver25_final = ver25 if cal5['tem_poder'] else 'SEM PODER'
    R['D2_5']['veredito'] = {
        'pela_letra': ver25_final, 'calibracao_tem_poder': cal5['tem_poder'], 'V': e5['V'], 'teto_T17_nacional': e5['nac_T17_2T'],
        'IMP_ou_RAJ_nacional_2T': e5['nac_IR_full_2T'], 'IMP_ou_RAJ_ou_T17o_nacional_2T': e5['nac_U_full_2T'], 'razao_taxas': e5['razao_taxas'],
        'taxa_RAJ_1T': e5['taxa_RAJ_1T'], 'elo_amostra': {'coef': eloL['coef']['x'], 'ep': eloL['ep']['x'], 'ic95': eloL['ic95']['x']},
        'clausulas': {'V_ge_1107548': e5['V']['valor'] >= L25, 'V_limite_inferior_ge_443019': e5['V']['ic95'][0] >= L10,
                      'razao_ge_3': e5['razao_taxas']['valor'] >= 3, 'elo_positivo_amostra': bool(eloL['ic95']['x'][0] > 0),
                      'elo_positivo_censo': censo_pos, 'T17_limite_superior_lt_443019': e5['nac_T17_2T']['ic95'][1] < L10,
                      'IMP_RAJ_limite_superior_lt_443019': e5['nac_IR_full_2T']['ic95'][1] < L10,
                      'RAJ_1T_acima_de_0_1_pct': e5['taxa_RAJ_1T']['valor'] > 0.001},
        'teto_T17_em_fracao_da_margem': e5['nac_T17_2T']['valor'] / MARGEM,
        'teto_T17_limite_superior_em_fracao_da_margem': e5['nac_T17_2T']['ic95'][1] / MARGEM}
    print('D2-5 veredito', ver25_final, flush=True)

    # ------------------------------------------------------------------ descritivo pedido
    R['descritivo'] = descritivo(D, am, S1, S2, T1, T2)
    _grava_parcial('parcial_descritivo.json', R['descritivo'])

    R['exploratorio'] = exploratorio_tudo(D, am, S1, S2, T1, T2, b6, roda_elo25)
    _grava_parcial('parcial_exploratorio.json', R['exploratorio'])
    print('exploratório', round(time.time() - t0), 's', flush=True)

    R['contagem_de_testes'] = {
        'clausulas_com_limiar_neste_teste': 2,
        'estatisticas_olhadas': 'D2-2: B1 a B8 e V (9), em L e M10; D2-5: IMP, RAJ, T17, T17o, composição, elo na amostra e censo (7)',
        'sinais_que_o_acaso_daria': 'com 2 vereditos a 5% cada, 0,1 sinal por acaso; o registro pede nível de 1% na estatística primária de cada teste'}
    R['tempo_s'] = round(time.time() - t0)
    with open(REPO + '/resultados/R27_C1_quem_liberou_e_quando.json', 'w') as f:
        json.dump(R, f, ensure_ascii=False, indent=1, default=_json_default)
    print('json gravado', R['tempo_s'], 's', flush=True)
    try:
        escrever_txt(json.load(open(REPO + '/resultados/R27_C1_quem_liberou_e_quando.json')))
    except Exception as ex:
        print('txt nao escrito:', repr(ex), flush=True)


def exploratorio_tudo(D, am, S1, S2, T1, T2, b6, roda_elo25):
    """EXPLORATÓRIO: tudo aqui foi escrito DEPOIS de ver os resultados da primeira rodada. Não muda veredito."""
    np = D.np
    out = {'aviso': 'Escrito depois de ver os resultados. Serve para entender os achados; não entra em veredito.'}
    par = am['todas']
    # X1. As rajadas, uma a uma, e o elo do D2-5 sem elas
    raj = []
    for k in par:
        for di, t in ((0, '1T'), (1, '2T')):
            r = D.rec[k][di]
            m = cat25(r, D.thr[k], D.off[k])
            if not m['RAJ'].any():
                continue
            ii = np.nonzero(m['RAJ'])[0]
            a, b = D.votos(k)
            viz = [q for q in par if D.local[q] == D.local[k] and q != k]
            def yy(q):
                x, z = D.votos(q)
                return ((z['L'] - z['R']) - (x['L'] - x['R'])) / x['comp']
            raj.append({'secao': k, 'amostra': D.amostra_de[k], 'turno': t, 'votos_em_rajada': int(len(ii)),
                        'inicio_local': _hms(r['tcomp'][ii[0]]), 'fim_local': _hms(r['tcomp'][ii[-1]]),
                        'hora_de_brasilia_inicio': _hms(m['_tb'][ii[0]]), 'limiar_da_secao_s': D.thr[k],
                        'g_dos_votos': [float(x) for x in m['_g'][ii]], 'd_dos_votos': [float(x) for x in m['_d'][ii]],
                        'classes': dict(collections.Counter(NOMES_CLASSE[int(c)] for c in r['cls'][ii])),
                        'votos_no_dia': int(len(r['tcomp'])), 'L1': a['L'], 'R1': a['R'], 'C1': a['comp'], 'L2': b['L'], 'R2': b['R'], 'C2': b['comp'],
                        'y_margem_da_secao': yy(k), 'y_media_das_vizinhas_do_local': (float(np.mean([yy(q) for q in viz])) if viz else None),
                        'vizinhas': len(viz)})
    out['X1_rajadas'] = raj
    sem_raj = [k for k in am['L'] if not any(x['secao'] == k and x['turno'] == '2T' for x in raj)]
    e = roda_elo25(sem_raj, T1, T2)['erro_por_municipio']
    out['X1_elo_D2_5_em_L_sem_as_secoes_com_rajada'] = {y: {'coef': e[y]['coef']['x'], 'ep': e[y]['ep']['x'], 'ic95': e[y]['ic95']['x']} for y in e}
    out['X1_elo_D2_5_em_L_sem_as_secoes_com_rajada']['secoes_retiradas'] = len(am['L']) - len(sem_raj)
    # o mesmo elo com x = 1 se a seção tem algum voto nas categorias (tira a alavanca do tamanho de x)
    ii = np.array([D.ix[k] for k in am['L']], int)
    ind = (T2[ii, I25['U_full']] > 0).astype(float)
    r = regs_elo(D, am['L'], {'x': ind}, S1[ii, I22['MAN']], 'mun')
    out['X1_elo_D2_5_em_L_com_indicador'] = {y: {'coef': r[y]['coef']['x'], 'ep': r[y]['ep']['x']} for y in r}
    out['X1_elo_D2_5_em_L_com_indicador']['secoes_com_indicador'] = int(ind.sum())
    # X2. Espelho do B6: a mesma regra de "sem explicação" com os turnos trocados
    por1 = {x['secao']: x for x in b6['1']}
    por2 = {x['secao']: x for x in b6['2']}
    esp = [x for k, x in por1.items() if not x['explica_a_aptos_diferem']
           and not (k in por2 and por2[k]['ANO'] >= x['ANO'] - 2)]
    sem2 = [x for x in b6['2'] if not x['explica_a_aptos_diferem'] and not x['explica_b_ja_no_1T']]
    out['X2_espelho_B6'] = {'sem_explicacao_2T': len(sem2), 'excesso_de_votos_2T': int(sum(x['ANO'] - x['ANO_outro_turno'] for x in sem2)),
                            'sem_explicacao_1T_pela_regra_espelhada': len(esp),
                            'excesso_de_votos_1T': int(sum(x['ANO'] - x['ANO_outro_turno'] for x in esp)),
                            'secoes_2T': [[x['secao'], x['ANO'], x['sem_biometria_perfil'], x['ANO_outro_turno']] for x in sem2],
                            'secoes_1T': [[x['secao'], x['ANO'], x['sem_biometria_perfil'], x['ANO_outro_turno']] for x in esp]}
    # X3. Como vota a seção com mais eleitores sem biometria, em nível, em cada turno (dentro do mesmo local)
    x3 = {}
    for a in ('L', 'M10', 'todas'):
        chs = am[a]
        ii = np.array([D.ix[k] for k in chs], int)
        v = D.vetores_voto(chs)
        fe = D.conglomerado(chs, 'local')
        o = {}
        for t, S, Lv, Rv, Cv in (('1T', S1, v['L1'], v['R1'], v['C1']), ('2T', S2, v['L2'], v['R2'], v['C2'])):
            X = np.column_stack([S[ii, I22['ANO']] / S[ii, I22['C']], S[ii, I22['MAN']] / S[ii, I22['C']]])
            r = fe_reg((Lv - Rv) / Cv, X, fe, Cv, fe, ['ANO', 'MAN'])
            o[t] = {'coef': r['coef'], 'ep': r['ep'], 'n': r['n']}
        # mudança: margem contra a variação de ANO, sem e com controle da fatia de eleitores de 70 anos ou mais
        x3[a] = o
    out['X3_nivel_margem_do_13_sobre_fracao_ANO_e_MAN'] = x3
    # X4. CURTO: concentração e elo
    ii = np.array([D.ix[k] for k in am['L']], int)
    cur = T2[ii, I25['CURTO']]
    x = cur / T2[ii, I25['C']]
    r = regs_elo(D, am['L'], {'x': x}, S1[ii, I22['MAN']], 'mun')
    out['X4_CURTO_em_L'] = {'votos': float(cur.sum()), 'secoes_com_algum': int((cur > 0).sum()), 'secoes_com_5_ou_mais': int((cur >= 5).sum()),
                            'secoes_com_10_ou_mais': int((cur >= 10).sum()), 'maximo_na_secao': float(cur.max()),
                            'elo': {y: {'coef': r[y]['coef']['x'], 'ep': r[y]['ep']['x']} for y in r}}
    dd = np.concatenate([intervalos(D.rec[k][1])[1] for k in am['L']])
    out['X4_CURTO_em_L']['d_2T_contagem_por_segundo'] = {str(q): int((dd == q).sum()) for q in range(0, 8)}
    # X6. D2-2 no grupo PI, MA, TO, PB, CE e no resto
    x6 = {}
    for rot, chs in (('grupo_PI_MA_TO_PB_CE_em_L', [k for k in am['L'] if k.split('|')[0] in GRUPO_NE]),
                     ('demais_UFs_em_L', [k for k in am['L'] if k.split('|')[0] not in GRUPO_NE]),
                     ('grupo_PI_MA_TO_PB_CE_todas', [k for k in par if k.split('|')[0] in GRUPO_NE])):
        ii = np.array([D.ix[k] for k in chs], int)
        av, G = avaliar(deriv22, S1[ii], S2[ii], D.conglomerado(chs, 'local'))
        x6[rot] = {'secoes': len(chs), 'locais': G,
                   'estimativas': _resumo(av, ['frac_ANO_1T', 'frac_ANO_2T', 'frac_MAN_1T', 'frac_MAN_2T', 'frac_BIO3_1T', 'frac_BIO3_2T', 's_ANO',
                                               's_MAN', 's_BIO3', 'ln_rho', 'X_frac', 'V', 'V_nivel_puro', 'B3B4'])}
        av5, _ = avaliar(deriv25, T1[ii], T2[ii], D.conglomerado(chs, 'local'))
        x6[rot]['D2_5'] = _resumo(av5, ['nac_T17_2T', 'nac_U_full_2T', 'nac_RAJ_2T', 'taxa_T17_2T', 'taxa_T17_1T'])
        x6[rot]['por_UF'] = dict(collections.Counter(k.split('|')[0] for k in chs))
    out['X6_D2_2_por_grupo_de_UF'] = x6
    comp_grupo = sum(v['2']['comp'] for k, v in D.base.items() if k.split('|')[0] in GRUPO_NE and '2' in v)
    e6 = x6['grupo_PI_MA_TO_PB_CE_em_L']['estimativas']
    out['X6_traducao_no_grupo'] = {
        'comparecimento_2T_do_grupo_na_base': int(comp_grupo),
        'sobra_de_nivel_ANO_mais_MAN_em_votos_do_grupo': e6['V_nivel_puro']['valor'] / N2 * comp_grupo,
        'sobra_de_nivel_ic95_em_votos_do_grupo': [x / N2 * comp_grupo for x in e6['V_nivel_puro']['ic95']],
        'V_em_votos_do_grupo': e6['V']['valor'] / N2 * comp_grupo,
        'V_ic95_em_votos_do_grupo': [x / N2 * comp_grupo for x in e6['V']['ic95']]}
    # X9. B7 por grupo de UF (todas as amostras, para ter seções), com ANO e MAN separados
    x9 = {}
    for rot, chs in (('grupo_PI_MA_TO_PB_CE', [k for k in par if k.split('|')[0] in GRUPO_NE]),
                     ('demais_UFs', [k for k in par if k.split('|')[0] not in GRUPO_NE])):
        ii = np.array([D.ix[k] for k in chs], int)
        v = D.vetores_voto(chs)
        C1 = v['C1']
        nb1 = S1[ii, I22['ANO']] + S1[ii, I22['MAN']]
        nb2 = S2[ii, I22['ANO']] + S2[ii, I22['MAN']]
        a = regs_elo(D, chs, {'x': (nb2 - nb1) / C1}, S1[ii, I22['MAN']], 'local')
        b = regs_elo(D, chs, {'dANO': (S2[ii, I22['ANO']] - S1[ii, I22['ANO']]) / C1, 'dMAN': (S2[ii, I22['MAN']] - S1[ii, I22['MAN']]) / C1},
                     S1[ii, I22['MAN']], 'local')
        x9[rot] = {'n': a['margem']['n'], 'locais': a['margem']['locais'],
                   'x_total': {y: [a[y]['coef']['x'], a[y]['ep']['x']] for y in a},
                   'dANO': {y: [b[y]['coef']['dANO'], b[y]['ep']['dANO']] for y in b},
                   'dMAN': {y: [b[y]['coef']['dMAN'], b[y]['ep']['dMAN']] for y in b}}
    out['X9_B7_por_grupo_de_UF'] = x9
    # X10. MAN sem nenhuma digital do eleitor capturada: onde cresceu e se anda com o voto (L)
    chs = am['L']
    ii = np.array([D.ix[k] for k in chs], int)
    v = D.vetores_voto(chs)
    C1 = v['C1']
    sc1, sc2 = S1[ii, I22['MAN_semcapt']], S2[ii, I22['MAN_semcapt']]
    nb1 = S1[ii, I22['ANO']] + S1[ii, I22['MAN']]
    nb2 = S2[ii, I22['ANO']] + S2[ii, I22['MAN']]
    r = regs_elo(D, chs, {'sem_captura': (sc2 - sc1) / C1, 'demais_sem_biometria': ((nb2 - sc2) - (nb1 - sc1)) / C1}, S1[ii, I22['MAN']], 'local')
    dsc = sc2 - sc1
    ordem = np.argsort(-dsc)
    out['X10_MAN_sem_captura_em_L'] = {
        'total_1T': float(sc1.sum()), 'total_2T': float(sc2.sum()),
        'secoes_com_5_ou_mais_1T': int((sc1 >= 5).sum()), 'secoes_com_5_ou_mais_2T': int((sc2 >= 5).sum()),
        'secoes_com_algum_1T': int((sc1 > 0).sum()), 'secoes_com_algum_2T': int((sc2 > 0).sum()),
        'aumento_nas_20_secoes_que_mais_subiram': float(dsc[ordem[:20]].sum()), 'queda_nas_20_que_mais_cairam': float(dsc[ordem[-20:]].sum()),
        'maiores_altas': [[chs[j], int(sc1[j]), int(sc2[j])] for j in ordem[:10]],
        'elo': {y: {q: [r[y]['coef'][q], r[y]['ep'][q]] for q in r[y]['coef']} for y in r}}
    da = S2[ii, I22['ANO']] - S1[ii, I22['ANO']]
    oa = np.argsort(-da)
    out['X10_variacao_de_ANO_por_secao_em_L'] = {
        'secoes_que_subiram': int((da > 0).sum()), 'secoes_que_cairam': int((da < 0).sum()), 'soma_das_altas': float(da[da > 0].sum()),
        'soma_das_quedas': float(da[da < 0].sum()), 'secoes_com_alta_de_5_ou_mais': int((da >= 5).sum()), 'secoes_com_queda_de_5_ou_mais': int((da <= -5).sum()),
        'secoes_com_alta_de_10_ou_mais': int((da >= 10).sum()), 'secoes_com_queda_de_10_ou_mais': int((da <= -10).sum()),
        'maiores_altas': [[chs[j], int(S1[ii[j], I22['ANO']]), int(S2[ii[j], I22['ANO']])] for j in oa[:10]]}
    # X11. A cauda do ANO: seções de L com alta de 5 ou mais contra queda de 5 ou mais; margem contra as vizinhas do local
    y = ((v['L2'] - v['R2']) - (v['L1'] - v['R1'])) / C1
    fe_l = np.array(D.conglomerado(chs, 'local'))
    _, gl = np.unique(fe_l, return_inverse=True)
    sw = np.bincount(gl, weights=C1)
    swy = np.bincount(gl, weights=C1 * y)
    nloc = np.bincount(gl)
    with np.errstate(divide='ignore', invalid='ignore'):
        outros = (swy[gl] - C1 * y) / (sw[gl] - C1)
    exc = (y - outros) * C1
    x11 = {}
    for rot, msk in (('alta_de_5_ou_mais', da >= 5), ('queda_de_5_ou_mais', da <= -5), ('entre_menos_4_e_mais_4', (da > -5) & (da < 5))):
        m2 = msk & (nloc[gl] >= 2)
        x11[rot] = {'secoes': int(m2.sum()), 'variacao_de_ANO': float(da[m2].sum()), 'variacao_do_comparecimento': float((v['C2'] - v['C1'])[m2].sum()),
                    'margem_acima_das_vizinhas_em_votos': float(np.nansum(exc[m2])),
                    'margem_acima_das_vizinhas_por_secao': float(np.nanmean(exc[m2])) if m2.sum() else None,
                    'ep_por_secao': float(np.nanstd(exc[m2], ddof=1) / np.sqrt(m2.sum())) if m2.sum() > 1 else None,
                    'ANO_1T': float(S1[ii, I22['ANO']][m2].sum()), 'votos_1T': float(C1[m2].sum())}
    out['X11_cauda_do_ANO_em_L'] = x11
    # o eleitor sem biometria voltou mais onde o 1º turno teve fila? (explicação inocente: fila longa afasta o idoso)
    fila1 = T1[ii, I25['T17']] / T1[ii, I25['C']]
    r = fe_reg(da / C1, np.column_stack([fila1, (v['C2'] - v['C1']) / C1, S1[ii, I22['ANO']] / C1]), fe_l, C1, fe_l, ['fila_1T', 'dC', 'ANO1'])
    out['X11_variacao_de_ANO_contra_fila_do_1T'] = {'coef': r['coef'], 'ep': r['ep'], 'n': r['n']}
    r = fe_reg(da / C1, np.column_stack([fila1, S1[ii, I22['ANO']] / C1]), np.array(D.conglomerado(chs, 'mun')), C1, np.array(D.conglomerado(chs, 'mun')), ['fila_1T', 'ANO1'])
    out['X11_variacao_de_ANO_contra_fila_do_1T_entre_locais_do_municipio'] = {'coef': r['coef'], 'ep': r['ep'], 'n': r['n']}
    # tradução do coeficiente de ANO em votos de margem (L)
    iL = np.array([D.ix[k] for k in am['L']], int)
    dano_nac = (S2[iL, I22['ANO']].sum() - S1[iL, I22['ANO']].sum()) / S2[iL, I22['C']].sum() * N2
    out['X3_variacao_bruta_de_ANO_equivalente_nacional'] = float(dano_nac)
    dman_nac = (S2[iL, I22['MAN']].sum() - S1[iL, I22['MAN']].sum()) / S2[iL, I22['C']].sum() * N2
    out['X3_variacao_bruta_de_MAN_equivalente_nacional'] = float(dman_nac)
    # X7. Hora: diferença em diferenças entre as seções que subiram e as que caíram (fatia dos votos por hora de Brasília)
    def fatias(chs, di):
        h = np.zeros(24)
        for k in chs:
            r = D.rec[k][di]
            hh = np.clip(((r['tcomp'] + D.off[k]) // 3600).astype(int), 0, 23)
            h += np.bincount(hh, minlength=24)
        return h / h.sum()
    ii = np.array([D.ix[k] for k in am['L']], int)
    dC = S2[ii, I22['C']] - S1[ii, I22['C']]
    sub = [k for k, q in zip(am['L'], dC) if q > 0]
    cai = [k for k, q in zip(am['L'], dC) if q < 0]
    f = {('sub', 0): fatias(sub, 0), ('sub', 1): fatias(sub, 1), ('cai', 0): fatias(cai, 0), ('cai', 1): fatias(cai, 1)}
    out['X7_hora_dif_em_dif_L'] = {f'{h:02d}h': {'subiu_1T': float(f[('sub', 0)][h]), 'subiu_2T': float(f[('sub', 1)][h]),
                                                 'caiu_1T': float(f[('cai', 0)][h]), 'caiu_2T': float(f[('cai', 1)][h]),
                                                 'dif_em_dif': float((f[('sub', 1)][h] - f[('sub', 0)][h]) - (f[('cai', 1)][h] - f[('cai', 0)][h]))}
                                   for h in range(7, 20)}
    # a variação do comparecimento da seção depende da fração de votos tardios do 1T? (quem tinha fila no 1T)
    # X8. O recuo de relógio: contexto das linhas
    x8 = []
    for k in D.chaves:
        for di in (0, 1):
            r = D.rec[k][di]
            if r is None:
                continue
            for (li, ta, tb, pa, pb, blo) in r['retro_ev']:
                try:
                    for nome, linhas in _blocos(D.arquivo[k]):
                        if nome == blo:
                            datas = [l[:19] for l in linhas[max(0, li - 400):li] if l[:10] in DIAS]
                            ant = [('\t'.join(l.split('\t')[:5])) for l in linhas[max(0, li - 400):li] if l[:10] in DIAS][-6:]
                            ctx = []
                            for j in range(max(0, li - 400), li):
                                if linhas[j][:10] in DIAS:
                                    ctx = ['\t'.join(q.split('\t')[:5]) for q in linhas[max(0, j - 4):j + 6]]
                            x8.append({'secao': k, 'turno': di + 1, 'linha_do_recuo': li, 'ultimas_linhas_com_data_do_dia_antes_do_recuo': ant,
                                       'contexto_da_ultima': ctx})
                except Exception as ex:
                    x8.append({'secao': k, 'erro': str(ex)})
    out['X8_recuo_de_relogio'] = x8
    return out


def escrever_txt(R):
    """Relatório em texto, a partir do JSON. Só formata: nenhuma conta nova."""
    L = []
    w = L.append

    def n0(x):
        return _fmt(x, 0)

    def n(x, c=2):
        return _fmt(x, c)

    def pc(x, c=3):
        return _fmt(100 * x, c) + '%'

    def ic(d, f=n0):
        return f"{f(d['valor'])} (ep {f(d['ep'])}; IC 95% de {f(d['ic95'][0])} a {f(d['ic95'][1])})"

    def icp(d, c=3):
        return f"{_fmt(100 * d['valor'], c)} ponto (ep {_fmt(100 * d['ep'], c)}; IC de {_fmt(100 * d['ic95'][0], c)} a {_fmt(100 * d['ic95'][1], c)})"

    def icn(d, c=4):
        return f"{_fmt(d['valor'], c)} (ep {_fmt(d['ep'], c)}; IC de {_fmt(d['ic95'][0], c)} a {_fmt(d['ic95'][1], c)})"

    def ce(c, e, k=4):
        return f"{'+' if c >= 0 else ''}{_fmt(c, k)} (ep {_fmt(e, k)})"

    A = R['amostra_e_conferencias']
    d2 = R['D2_2']
    d5 = R['D2_5']
    e = d2['L']['estimativas']
    em = d2['M10']['estimativas']
    t1, t2 = d2['L']['totais_1T'], d2['L']['totais_2T']
    v2 = d2['veredito']
    v5 = d5['veredito']
    f = d5['L']['estimativas']
    fm = d5['M10']['estimativas']
    u1, u2 = d5['L']['totais_1T'], d5['L']['totais_2T']
    cal, cal5 = d2['calibracao'], d5['calibracao']
    b6 = d2['B6']
    b7 = d2['B7']
    X = R['exploratorio']
    ds = R['descritivo']
    cs = d5['censo']

    w('R27_C1: QUEM LIBEROU E A QUE HORAS')
    w('Testes D2-2 (MESALOG) e D2-5 (RELOGIO) do desenho cego D2, com os logs das 3.897 seções da amostra antiga.')
    w('Registro: Adendo 27 (commit 2748895, 10/11/2026 00:16:42 UTC) e Adendo 28 (commit 938be19, 04:36:33 UTC).')
    w(f"Docstring com as decisões gravado antes de rodar: SHA-256 {R['docstring_sha256_antes_de_rodar']}")
    w(f"  (igual ao docstring atual do script: {'sim' if R['docstring_sha256_antes_de_rodar'] == R['docstring_atual_sha256'] else 'NÃO'}).")
    w('O log da urna não traz o candidato votado. Os votos por seção vêm de dados/secoes2026.json.gz.')
    w('Nenhum outro ano entra neste teste. O controle é o 1º turno de 2026 na mesma seção.')
    w('Escala: margem 4.430.191; 25% = 1.107.548; 10% = 443.019; comparecimento do 2º turno 128.236.074. Voto inserido vale 1 na margem.')
    w('')
    w('VEREDITOS PELA LETRA')
    w(f"  D2-2 MESALOG: {v2['pela_letra']}.")
    w(f"    Nas cláusulas de tamanho o resultado é {v2['pela_letra_sem_a_clausula_B6']}: V = {n0(v2['V']['valor'])} votos, limite superior {n0(v2['V']['ic95'][1])},")
    w(f"    abaixo de 443.019; B3 + B4 = {n0(v2['B3B4']['valor'])}, limite superior {n0(v2['B3B4']['ic95'][1])}. O que leva a INCONCLUSIVO é só a cláusula B6:")
    w(f"    {v2['clausulas']['B6_2T_sem_explicacao_cadastral']} seções no 2º turno com habilitações por ano de nascimento acima do reservatório do perfil, sem explicação cadastral")
    w(f"    pelas regras fixadas antes ({X['X2_espelho_B6']['excesso_de_votos_2T']} votos acima do 1º turno, somadas as {X['X2_espelho_B6']['sem_explicacao_2T']}). A calibração mostra poder: {'sim' if v2['calibracao_tem_poder'] else 'não'}.")
    w(f"  D2-5 RELOGIO: {v5['pela_letra']}.")
    w(f"    Teto da prorrogação (todos os votos depois das 17h de Brasília): {n0(v5['teto_T17_nacional']['valor'])} votos no país, limite superior {n0(v5['teto_T17_nacional']['ic95'][1])}")
    w(f"    ({pc(v5['teto_T17_limite_superior_em_fracao_da_margem'], 1)} da margem). Votos impossíveis ou em rajada: {n0(v5['IMP_ou_RAJ_nacional_2T']['valor'])}, limite superior {n0(v5['IMP_ou_RAJ_nacional_2T']['ic95'][1])}.")
    w(f"    A calibração mostra poder: {'sim' if v5['calibracao_tem_poder'] else 'não'}.")
    w('')
    w('RESUMO')
    w(f"1. Pela porta sem biometria (ano de nascimento ou liberação do mesário) não entrou, a mais que no 1º turno, nada perto de um décimo")
    w(f"   da margem: {n0(v2['V']['valor'])} votos (de {n0(v2['V']['ic95'][0])} a {n0(v2['V']['ic95'][1])}), {pc(v2['V_em_fracao_da_margem'], 1)} da margem, teto de {pc(v2['V_limite_superior_em_fracao_da_margem'], 1)}.")
    w(f"2. A liberação pelo mesário subiu junto com as biometrias difíceis (3ª ou 4ª tentativa): a razão entre as duas ficou igual")
    w(f"   (ln = {_fmt(e['ln_rho']['valor'], 4)}, ep {_fmt(e['ln_rho']['ep'], 4)}). É a marca de dedo ruim, não de voto lançado na mesa.")
    w(f"3. Não há fim de fila sem biometria nem sequências a mais no 2º turno (há menos que no 1º), nem voto em ritmo impossível.")
    w(f"4. Depois das 17h de Brasília houve cerca de {n0(f['nac_T17_2T']['valor'])} votos no país. A prorrogação não chega a 1% da margem, votem como votarem.")
    w(f"5. O que pesa a favor da tese, pequeno: a seção onde as habilitações sem biometria mais cresceram ganhou margem para o 13 contra as")
    w(f"   vizinhas do prédio (gama = {ce(v2['gama_B7']['coef'], v2['gama_B7']['ep'])}, abaixo do 0,30 do registro), e esse elo vem quase todo do ano de nascimento")
    x3 = b7['L']['ao_lado_ANO_e_MAN_separados']['margem']
    w(f"   ({ce(x3['coef']['dANO'], x3['ep']['dANO'])} por voto; liberação do mesário {ce(x3['coef']['dMAN'], x3['ep']['dMAN'])}). Em votos, o canal inteiro do ano de")
    w(f"   nascimento não passa de {n0(e['V_ANO']['ic95'][1])} acima do proporcional, ou de {n0(X['X3_variacao_bruta_de_ANO_equivalente_nacional'])} se todo o aumento bruto fosse irregular.")
    w('')
    w('O QUE FOI LIDO')
    w(f"  Pacotes de log: {n0(A['pacotes'])}, todos lidos. Leitor próprio, com filtro pela identidade da seção gravada no próprio log")
    w(f"  (um pacote pode trazer, em bloco aninhado, o log de outra seção: {A['trechos_de_outra_secao_dentro_de_pacotes']['trechos']} trechos com {n0(A['trechos_de_outra_secao_dentro_de_pacotes']['habilitacoes'])} habilitações ficaram fora por isso).")
    lb = A['log_contra_bweb']
    w(f"  Votos computados no log iguais ao comparecimento do bweb: {n0(lb['log_igual_bweb_2T'])} de {n0(A['pacotes'])} seções no 2º turno e {n0(lb['log_igual_bweb_1T'])} de {n0(A['pares'])} no 1º.")
    cf = d2['conferencia_MAN_contra_bweb']
    if 'erro' not in cf:
        w(f"  Liberações pelo mesário no log iguais ao campo QT_ELEI_BIOM_SEM_HABILITACAO do bweb: {n0(cf['MAN_log_igual_H_bweb_1T'][0])} de {n0(cf['MAN_log_igual_H_bweb_1T'][1])} no 1º turno e {n0(cf['MAN_log_igual_H_bweb_2T'][0])} de {n0(cf['MAN_log_igual_H_bweb_2T'][1])} no 2º.")
    lr = A.get('leitor_contra_extrator_de_referencia_do_desenhista', {})
    if 'pacotes_conferidos' in lr:
        w(f"  Leitor conferido contra o extrator de referência do desenhista em {n0(lr['pacotes_conferidos'])} pacotes sorteados ({n0(lr['votos_comparados'])} votos): contagens por classe e")
        w(f"  de BIO na 3ª ou 4ª tentativa idênticas em {n0(lr.get('secao_dia_com_contagens_identicas', 0))} de {n0(lr.get('secao_dia_com_contagens_identicas', 0) + lr.get('secao_dia_com_diferenca', 0))} seções e dias.")
    w(f"  Seções com log próprio dos dois dias (pares): {n0(A['pares'])}; só com o 2º turno: {n0(A['so_2T_no_log'])}.")
    w(f"  Amostra principal L: {n0(A['pares_por_amostra']['L'])} seções pares em {n0(d2['L']['conglomerados'])} locais inteiros sorteados (de {n0(A['L_secoes'])} seções em {n0(A['L_locais'])} locais).")
    w(f"  Secundária M10: {n0(A['pares_por_amostra']['M10'])} seções em 10 municípios inteiros. Resto: {n0(A['pares_por_amostra']['resto'])} seções avulsas.")
    w(f"  Votos em L: {n0(t1['C'])} no 1º turno e {n0(t2['C'])} no 2º. IC de 95% por reamostragem de locais, 2.000 réplicas.")
    w('')
    w('=' * 100)
    w('D2-2 MESALOG: HABILITAÇÕES SEM BIOMETRIA, 1º CONTRA 2º TURNO NA MESMA SEÇÃO (amostra L)')
    w('=' * 100)
    w('Tipos: BIO = dedo do eleitor reconhecido; ANO = eleitor sem biometria no cadastro, liberado pelo ano de nascimento;')
    w('MAN = eleitor com biometria, quatro leituras frustradas e dedo do mesário (mesário identificado, dedo já visto sem mesário, dedo novo).')
    w('')
    w(f"                          1º turno              2º turno")
    for rot, k in (('votos computados', 'C'), ('BIO', 'BIO'), ('  BIO na 3ª ou 4ª tentativa', 'BIO3'), ('ANO', 'ANO'), ('MAN', 'MAN'), ('  mesário identificado', 'MAN_MES'),
                   ('  dedo já visto, sem mesário', 'MAN_NAO'), ('  dedo novo', 'MAN_NOVO'), ('  MAN sem digital do eleitor capturada', 'MAN_semcapt')):
        w(f"  {rot:<38}{n0(t1[k]):>10} ({pc(t1[k] / t1['C'], 2):>7})   {n0(t2[k]):>10} ({pc(t2[k] / t2['C'], 2):>7})")
    w('')
    w(f"B1, nível:  ANO subiu {icp(e['s_ANO'])}.")
    w(f"            MAN subiu {icp(e['s_MAN'])}.")
    w(f"            As BIO difíceis (3ª ou 4ª tentativa) subiram {icp(e['s_BIO3'])}.")
    w(f"B2, razão de cauda MAN/BIO3: {_fmt(e['rho_1T']['valor'], 4)} no 1º turno e {_fmt(e['rho_2T']['valor'], 4)} no 2º; ln(rho2/rho1) = {icn(e['ln_rho'])}.")
    w(f"            O limite superior ({_fmt(e['ln_rho']['ic95'][1], 4)}) fica abaixo de 0,045, que é o que 10% da margem produziria.")
    w(f"            Liberações a mais que a razão do 1º turno explicaria: X = {pc(e['X_frac']['valor'], 4)} dos votos = {ic(e['V_MAN'])} votos no país.")
    w(f"V (primária) = (X + sobra de ANO) x 128.236.074 = {ic(e['V'])}.")
    w(f"            Parte do ANO: {ic(e['V_ANO'])}. Em M10: V = {ic(em['V'])} (10 municípios, IC grosseiro).")
    w(f"            Ao lado, só nível, sem a razão de cauda (ANO mais MAN acima do proporcional): {ic(e['V_nivel_puro'])}.")
    w(f"B3, fim de fila (habilitações sem biometria depois da última BIO do dia, seções com 3 ou mais): {n0(t1['S_fim'])} votos no 1º turno e {n0(t2['S_fim'])} no 2º;")
    w(f"            no país, 2º menos 1º: {ic(e['B3'])}.")
    w(f"B4, sequências de 4 ou mais sem biometria: {n0(t1['seq4'])} votos no 1º turno (esperado por permutação {n(t1['seq4_exp'], 1)}) e {n0(t2['seq4'])} no 2º (esperado {n(t2['seq4_exp'], 1)});")
    w(f"            excesso 2º menos 1º no país: {ic(e['B4'])}. B3 + B4 = {ic(e['B3B4'])}.")
    w(f"B5, dedo:   MAN por dedo novo ou não associado: {pc(e['B5_dedo_1T']['valor'], 2)} no 1º turno e {pc(e['B5_dedo_2T']['valor'], 2)} no 2º (diferença {icp(e['B5_dedo_dif'], 2)}).")
    w(f"            MAN sem nenhuma digital do eleitor capturada: {pc(e['B5_semcapt_1T']['valor'], 2)} e {pc(e['B5_semcapt_2T']['valor'], 2)} (diferença {icp(e['B5_semcapt_dif'], 2)});")
    w(f"            por voto, isso equivale a {ic(e['B5_semcapt_por_voto_dif_nac'])} votos no país.")
    w(f"B6, reservatório: seções com ANO acima dos eleitores sem biometria do perfil mais 2: {b6['1T']['secoes_acima_do_reservatorio_mais_2']} no 1º turno e {b6['2T']['secoes_acima_do_reservatorio_mais_2']} no 2º")
    w(f"            (de {n0(b6['2T']['ANO_menos_reservatorio']['secoes'])} seções pares). No 2º turno: {b6['2T']['com_explicacao_a']} com aptos do boletim diferentes do perfil; {b6['2T']['com_explicacao_b']} que já passavam no 1º turno")
    w(f"            com o mesmo tamanho (algumas com as duas); {b6['2T']['sem_explicacao']} sem explicação. Excesso total: {n0(b6['1T']['excesso_total_votos'])} votos no 1º turno e {n0(b6['2T']['excesso_total_votos'])} no 2º.")
    w(f"            Em L, o ANO usa {pc(b6['L_uso_do_reservatorio']['ANO_1T_sobre_sem_biometria'], 1)} do reservatório no 1º turno e {pc(b6['L_uso_do_reservatorio']['ANO_2T_sobre_sem_biometria'], 1)} no 2º ({n0(b6['L_totais']['sem_biometria_perfil'])} eleitores sem biometria no perfil).")
    g = b7['L']['x_total']
    w(f"B7, elo com o voto (efeito fixo de local, peso C1, erro por local; {n0(g['margem']['n'])} seções em {n0(g['margem']['locais'])} locais):")
    w(f"            gama = {ce(g['margem']['coef']['x'], g['margem']['ep']['x'])}, IC de {_fmt(g['margem']['ic95']['x'][0], 4)} a {_fmt(g['margem']['ic95']['x'][1], 4)}. O registro pede 0,30 ou mais.")
    gs = b7['L']['x_suspeito_e_comum']['margem']
    w(f"            Separado: suspeito (fim de fila, sequência, dedo novo) {ce(gs['coef']['suspeito'], gs['ep']['suspeito'])}; comum {ce(gs['coef']['comum'], gs['ep']['comum'])}.")
    w(f"            Em M10: {ce(b7['M10']['x_total']['margem']['coef']['x'], b7['M10']['x_total']['margem']['ep']['x'])}. Todas as pares: {ce(b7['todas']['x_total']['margem']['coef']['x'], b7['todas']['x_total']['margem']['ep']['x'])}.")
    w(f"B8, alertas de eleitor que já votou, por mil votos: {n(e['B8_1T']['valor'], 3)} no 1º turno e {n(e['B8_2T']['valor'], 3)} no 2º.")
    w('')
    w('Placebos e espelho do D2-2')
    w(f"  Razão de cauda de tarde contra de manhã, dentro do 1º turno: ln = {icn(e['plac_ln_tarde_manha_1T'])}; no 2º: {_fmt(e['plac_ln_tarde_manha_2T']['valor'], 4)};")
    w(f"  diferença em diferenças {icn(e['plac_did'])}. A razão não é estável dentro do dia (varia 12% entre manhã e tarde),")
    w(f"  mas entre os turnos, na mesma metade do dia, fica em {_fmt(e['ln_rho_manha']['valor'], 4)} (manhã) e {_fmt(e['ln_rho_tarde']['valor'], 4)} (tarde). Só importaria se houvesse sinal.")
    w(f"  Turnos invertidos (1º turno tratado como suspeito): V = {ic(e['V_invertido'])}.")
    w(f"  B7 com o ganho de cada candidato: Lula {ce(g['ganho_L']['coef']['x'], g['ganho_L']['ep']['x'])}; Flávio {ce(g['ganho_R']['coef']['x'], g['ganho_R']['ep']['x'])}.")
    w(f"  B7 com desfecho placebo (branco e nulo): {ce(g['placebo_BN']['coef']['x'], g['placebo_BN']['ep']['x'])}.")
    w(f"  B6 espelhado (a mesma regra com os turnos trocados; exploratório): {X['X2_espelho_B6']['sem_explicacao_1T_pela_regra_espelhada']} seções e {X['X2_espelho_B6']['excesso_de_votos_1T']} votos no 1º turno,")
    w(f"  contra {X['X2_espelho_B6']['sem_explicacao_2T']} seções e {X['X2_espelho_B6']['excesso_de_votos_2T']} votos no 2º.")
    w('')
    w('Calibração do D2-2 (efeito plantado nos registros de 2026, só no 2º turno, amostra L)')
    a = cal['a_uniforme_MAN_0864']
    w(f"  (a) Liberações MAN sintéticas espalhadas, {n0(a['votos_plantados'])} votos ({pc(a['fracao_plantada'])}; {n0(a['equivalente_nacional'])} no país): ln sobe {_fmt(a['efeito_em_ln_rho'], 4)} (esperado 0,109),")
    w(f"      X sobe {pc(a['efeito_em_X_frac'])}, V sobe {n0(a['efeito_em_V'])} e passa a {n0(a['estimativas']['V']['valor'])} (de {n0(a['estimativas']['V']['ic95'][0])} a {n0(a['estimativas']['V']['ic95'][1])}). O teste enxerga.")
    w(f"      Mas gama fica em {_fmt(a['B7']['gama'], 3)} e B3 + B4 não mexe: pela letra daria {a['veredito_que_o_teste_daria']}, não SINAL. Nunca daria sem sinal.")
    a = cal['a_uniforme_MAN_0345']
    w(f"  (a') O mesmo com {pc(a['fracao_plantada'])} ({n0(a['equivalente_nacional'])} no país): V sobe {n0(a['efeito_em_V'])}, vai a {n0(a['estimativas']['V']['valor'])} (limite superior {n0(a['estimativas']['V']['ic95'][1])}): {a['veredito_que_o_teste_daria']}.")
    a = cal['b_concentrado_30_ANO_em_5pct']
    w(f"  (b) 30 habilitações ANO depois do último voto em 5% das seções ({n0(a['secoes_plantadas'])} seções, {n0(a['votos_plantados'])} votos, {n0(a['equivalente_nacional'])} no país):")
    w('      (passa de 100% porque o bloco puxa para a conta habilitações sem biometria que já estavam no fim do dia)')
    w(f"      B3 acusa {pc(a['B3_fracao_acusada'], 1)} e B4 acusa {pc(a['B4_fracao_acusada'], 1)} dos votos; todas as {a['secoes_plantadas_com_n_fim_5']} seções entram na lista local; B3 + B4 vai a {n0(a['estimativas']['B3B4']['valor'])};")
    w(f"      gama = {_fmt(a['B7']['gama'], 3)} (ep {_fmt(a['B7']['ep'], 3)}), suspeito {_fmt(a['B7']['gama_suspeito'], 3)}. O registro esperava gama perto de 1; com o controle de comparecimento do D2-1")
    w(f"      o voto plantado se reparte entre x e o comparecimento, e gama fica perto de 0,4. Veredito: {a['veredito_que_o_teste_daria']} (o plantio soma menos de 25% da margem).")
    a = cal['b_concentrado_30_ANO_somando_0864']
    w(f"  (b'') O mesmo bloco somando 0,864% ({n0(a['secoes_plantadas'])} seções, {n0(a['equivalente_nacional'])} no país): V = {n0(a['estimativas']['V']['valor'])}, B3 + B4 = {n0(a['estimativas']['B3B4']['valor'])}, gama = {_fmt(a['B7']['gama'], 3)}: {a['veredito_que_o_teste_daria']}.")
    a = cal['b_concentrado_30_ANO_somando_0345']
    w(f"  (b') Somando 0,345% ({n0(a['secoes_plantadas'])} seções): V = {n0(a['estimativas']['V']['valor'])}, B3 + B4 = {n0(a['estimativas']['B3B4']['valor'])}, gama = {_fmt(a['B7']['gama'], 3)}: {a['veredito_que_o_teste_daria']}.")
    w('  Explicações inocentes plantadas, para ver se o teste as separa da irregularidade:')
    a = cal['i1_inocente_eleitores_reais_sem_biometria_0864']
    w(f"  (i1) Eleitores reais sem biometria entrando espalhados ({n0(a['votos_plantados'])} votos ANO, votando como a seção): V sobe {n0(a['efeito_em_V'])}, igual ao plantio (a).")
    w(f"       gama = {_fmt(a['B7']['gama'], 3)}; B3 + B4 parado. Veredito {a['veredito_que_o_teste_daria']}. Ou seja: pelo V, o teste NÃO separa eleitor real sem biometria de voto lançado")
    w('       espalhado pelo dia. O que separa é só o elo com o voto, e ele é fraco nas duas situações. O V é um teto para os dois juntos.')
    a = cal['i2_inocente_leitor_pior_115']
    w(f"  (i2) Leitor pior (11,5% a mais de MAN e de BIO difíceis): ln mexe {_fmt(a['efeito_em_ln_rho'], 4)}, V mexe {n0(a['efeito_em_V'])}, s_MAN sobe {pc(a['efeito_em_s_MAN'])}. Veredito {a['veredito_que_o_teste_daria']}.")
    w('       A razão de cauda separa dedo ruim de voto lançado.')
    a = cal['i3_inocente_abstencao_pura_357_de_Flavio']
    w(f"  (i3) Abstenção pura de 3,57% dos eleitores de Flávio ({n0(a['votos_retirados'])} votos tirados): V mexe {n0(a['efeito_em_V'])}. Veredito {a['veredito_que_o_teste_daria']}.")
    w('       O teste é cego para eleitor que ficou em casa ou foi registrado como ausente, como devia: ele só olha quem foi habilitado.')
    w('')
    ll = d2['lista_local']['contagens']
    w('Achado local do D2-2 (arquivo resultados/R27_C1_lista_local.csv; para pedido de ata, caderno e digitais)')
    w(f"  Seções com 5 ou mais habilitações sem biometria depois da última BIO: {ll['2T_n_fim_5']} no 2º turno ({ll['1T_n_fim_5']} no 1º).")
    w(f"  Seções com mais de 30% das liberações por dedo novo: {ll['2T_dedo_novo_30']} no 2º turno ({ll['2T_pares_dedo_novo_30']} entre as pares) e {ll['1T_dedo_novo_30']} no 1º; {ll['dedo_novo_30_nos_dois_turnos']} nos dois, {ll['dedo_novo_30_so_no_2T']} só no 2º, {ll['dedo_novo_30_so_no_1T']} só no 1º.")
    w(f"  Seções com ANO acima do reservatório: {ll['2T_acima_do_reservatorio']}. Total na lista: {ll['secoes_na_lista']}.")
    w('')
    w('=' * 100)
    w('D2-5 RELOGIO: VOTOS FORA DE HORA E EM RITMO QUE MESA E CABINE NÃO FAZEM (amostra L)')
    w('=' * 100)
    w('g = da habilitação ao voto computado anterior (mesa); d = da habilitação ao voto computado (cabine); c = ciclo entre votos.')
    dt = d5['distribuicao_de_tempos_L']
    w(f"  Mínimos observados: g {n0(dt['1T']['g_minimo'])} s e {n0(dt['2T']['g_minimo'])} s; d {n0(dt['1T']['d_minimo'])} s e {n0(dt['2T']['d_minimo'])} s; c {n0(dt['1T']['c_minimo'])} s e {n0(dt['2T']['c_minimo'])} s (1º e 2º turno). Pisos do registro: 12, 2 e 15 s.")
    w('')
    w('                                        1º turno      2º turno      2º turno no país (IC 95%)')
    for rot, k in (('IMP por g < 12 s', 'imp_g'), ('IMP por d < 2 s', 'imp_d'), ('IMP por c < 15 s', 'imp_c'), ('IMP antes de urna pronta', 'imp_pre'),
                   ('IMP depois do início do encerramento', 'imp_pos'), ('IMP por relógio para trás', 'imp_retro'), ('RAJ (8 ou mais com g abaixo do p5 do 1T)', 'RAJ'),
                   ('T17 (depois das 17h de Brasília)', 'T17'), ('  depois das 18h', 'T18'), ('  depois das 19h', 'T19'),
                   ('T17o (depois de 15 min sem voto)', 'T17o'), ('IMP ou RAJ', 'IR_full'), ('IMP ou RAJ ou T17o', 'U_full'), ('CURTO (BIO ou MAN com d < 4 s; descritivo)', 'CURTO')):
        q = f['nac_%s_2T' % k]
        w(f"  {rot:<42}{n0(u1[k]):>8}    {n0(u2[k]):>8}      {n0(q['valor'])} ({n0(q['ic95'][0])} a {n0(q['ic95'][1])})")
    w(f"  Voto sem habilitação: {lb['voto_sem_hab_1T']} e {lb['voto_sem_hab_2T']}. Total do log diferente do boletim: {lb.get('log_difere_bweb_1T', 0)} e {lb.get('log_difere_bweb_2T', 0)} seções.")
    w(f"  T17 no 1º turno, sem liminar: {n0(u1['T17'])} votos ({pc(u1['T17'] / u1['C'], 2)}), o que no país seriam {n0(f['nac_T17_1T_aplicada']['valor'])}. No 2º: {pc(u2['T17'] / u2['C'], 3)}.")
    w(f"  V (primária) = votos em (IMP ou RAJ ou T17o) no 2º turno menos a taxa do 1º: {ic(f['V'])}. Razão das taxas: {n(f['razao_taxas']['valor'], 2)} (o registro pede 3 ou mais).")
    w(f"  Taxa de RAJ no 1º turno (placebo): {pc(f['taxa_RAJ_1T']['valor'], 4)}, abaixo de 0,1%: a definição não pega fila normal.")
    w(f"  Em M10: T17 no país {ic(fm['nac_T17_2T'])}; IMP ou RAJ {n0(fm['nac_IR_full_2T']['valor'])} (até {n0(fm['nac_IR_full_2T']['ic95'][1])}).")
    so = d5.get('so_2T_no_log') or {}
    if so:
        w(f"  Nas {so['secoes']} seções só com o 2º turno no log ({n0(so['totais_2T']['C'])} votos): {n0(so['totais_2T']['T17'])} votos depois das 17h, nenhum IMP, nenhuma rajada.")
    w(f"  Composição: fatia sem biometria entre os votos depois das 17h: {pc(f['frac_sembio_T17_2T']['valor'], 1)} no 2º turno ({n0(u2['nb_T17'])} de {n0(u2['T17'])} votos) contra {pc(f['frac_sembio_resto_2T']['valor'], 1)} no resto do dia;")
    w(f"  no 1º turno {pc(f['frac_sembio_T17_1T']['valor'], 1)} contra {pc(f['frac_sembio_resto_1T']['valor'], 1)}. ln da razão de chances 2º contra 1º: {icn(f['ln_OR2_OR1'], 3)}. Poucos votos, não decide.")
    el = d5['elo_amostra']['L']
    em5 = el['erro_por_municipio']
    w(f"  Elo com o voto na amostra (x = fração dos votos da seção em IMP ou RAJ ou T17o; {el['secoes_com_x_positivo']} seções com x acima de zero):")
    w(f"    margem {ce(em5['margem']['coef']['x'], em5['margem']['ep']['x'], 3)}, IC de {_fmt(em5['margem']['ic95']['x'][0], 3)} a {_fmt(em5['margem']['ic95']['x'][1], 3)}; ganho de Lula {ce(em5['ganho_L']['coef']['x'], em5['ganho_L']['ep']['x'], 3)}; ganho de Flávio {ce(em5['ganho_R']['coef']['x'], em5['ganho_R']['ep']['x'], 3)};")
    w(f"    placebo branco e nulo {ce(em5['placebo_BN']['coef']['x'], em5['placebo_BN']['ep']['x'], 3)}. Pela letra é elo positivo com IC que exclui zero.")
    xs = X['X1_elo_D2_5_em_L_sem_as_secoes_com_rajada']
    xi = X['X1_elo_D2_5_em_L_com_indicador']
    w(f"    Exploratório: o coeficiente depende de {xs['secoes_retiradas']} seções com rajada (x grande). Sem elas: {ce(xs['margem']['coef'], xs['margem']['ep'], 3)}.")
    w(f"    Com x = 1 se a seção tem algum voto nas categorias: {ce(xi['margem']['coef'], xi['margem']['ep'])}. Em votos, o elo cheio vale {n0(em5['margem']['coef']['x'] * f['nac_U_full_2T']['valor'])} de margem.")
    w('')
    w('As rajadas, uma a uma (exploratório): todas de manhã ou perto do meio do dia e todas com biometria do eleitor reconhecida')
    for r in X['X1_rajadas']:
        w(f"    {r['secao']} ({r['amostra']}, {r['turno']}): {r['votos_em_rajada']} votos de {r['inicio_local']} a {r['fim_local']}, classes {r['classes']}, g de {n0(min(r['g_dos_votos']))} a {n0(max(r['g_dos_votos']))} s (limiar da seção {n(r['limiar_da_secao_s'], 1)} s)")
    w('')
    w('Lista IMP (resultados/R27_C1_lista_IMP.csv e R27_C1_trechos_IMP.txt)')
    for k, q in d5['lista_IMP']['contagem_por_turno_e_regra'].items():
        w(f"    {k}: {q}")
    w('    O único caso é artefato: na seção SP|66079|63|214 a urna estava com o relógio um mês adiantado na carga (marcava 25/10/2026')
    w('    13:07 no dia 25/09/2026) e o operador acertou a data. As 64 linhas da carga ficaram com a data do 2º turno e o leitor vê a')
    w('    hora "voltar" quando o dia verdadeiro começa. O voto marcado é o primeiro do dia (08:05:30, biometria reconhecida, d = 8 s).')
    w('')
    w('Censo dos encerramentos (país inteiro, bweb; universo do D2-1)')
    w(f"  Universo: {n0(cs['universo'])} seções. Encerraram depois de 17:30 de Brasília: {n0(cs['tardias_2T']['secoes'])} no 2º turno ({pc(cs['tardias_2T']['fracao_das_secoes'], 2)}; comparecimento {n0(cs['tardias_2T']['comparecimento'])};")
    w(f"  {n0(cs['tardias_2T']['depois_de_19h'])} depois das 19h) e {n0(cs['tardias_1T']['secoes'])} no 1º ({pc(cs['tardias_1T']['fracao_das_secoes'], 2)}; comparecimento {n0(cs['tardias_1T']['comparecimento'])}).")
    w(f"  No 2º turno por UF: {', '.join(f'{u} {n0(q)}' for u, q in cs['tardias_2T']['por_UF_10_maiores'][:6])}.")
    rt = cs['regressao_tardia2']
    w(f"  Regressão do D2-1 com o indicador de tardia no 2º turno ({n0(rt['margem']['n'])} seções, erro por município): margem {ce(rt['margem']['coef'], rt['margem']['ep'], 5)};")
    w(f"  ganho de Lula {ce(rt['ganho_L']['coef'], rt['ganho_L']['ep'], 5)}; ganho de Flávio {ce(rt['ganho_R']['coef'], rt['ganho_R']['ep'], 5)}; placebo branco e nulo {ce(rt['placebo_BN']['coef'], rt['placebo_BN']['ep'], 5)}.")
    tv = cs['traducao_em_votos']
    w(f"  Em votos: {n0(tv['margem_associada'])} de margem (de {n0(tv['margem_associada_ic95'][0])} a {n0(tv['margem_associada_ic95'][1])}) nas seções tardias.")
    rm = cs['regressao_minutos_de_atraso2']['margem']
    w(f"  Por minuto de atraso: {_fmt(rm['coef'] * 1e6, 2)} por milhão (ep {_fmt(rm['ep'] * 1e6, 2)}).")
    pl = cs['plantio_40_votos_para_o_13_em_cada_tardia']
    w(f"  Calibração: 40 votos a mais para o 13 em cada seção tardia ({n0(pl['votos_plantados'])} votos) levariam o coeficiente a {ce(pl['coef_com_controle_de_comparecimento'], pl['ep'], 4)}. O censo veria.")
    xl = cs['exploratorio_locais']
    w(f"  Aviso (exploratório): o efeito fixo de local só compara dentro de prédios mistos: {n0(xl['locais_mistos_2T'])} prédios com {n0(xl['secoes_tardias_em_locais_mistos'])} seções tardias;")
    xm = cs['exploratorio_efeito_fixo_de_municipio']
    w(f"  outras {n0(xl['secoes_tardias_em_locais_inteiros_tardios'])} estão em prédios inteiros tardios. Com efeito fixo de município: margem {ce(xm['margem']['coef'], xm['margem']['ep'], 5)}.")
    p1 = cs['placebo_corte_1T_fatia_do_13_sobre_tardia1']
    w(f"  Placebo do 1º turno em corte: a seção que fechou tarde tinha {ce(100 * p1['coef'], 100 * p1['ep'], 3)} ponto a mais de 13 que as vizinhas, sem liminar nenhuma.")
    w(f"  Ou seja, fechar tarde anda junto com voto no 13 por composição (fila onde o eleitor é mais lento). No 2º turno, em corte: {ce(100 * cs['ao_lado_corte_2T_fatia_do_13_sobre_tardia2']['coef'], 100 * cs['ao_lado_corte_2T_fatia_do_13_sobre_tardia2']['ep'], 3)} ponto.")
    w('')
    w('Calibração do D2-5 (5% das seções de L, só no 2º turno)')
    for rot, nome in (('p40_bloco_40_ciclos_20s_apos_20min', '(p40) 40 ciclos de 20 s, 20 minutos depois do último voto'),
                      ('p15_bloco_15_ciclos_20s_apos_20min', '(p15) 15 ciclos de 20 s, 20 minutos depois do último voto'),
                      ('p40c_bloco_40_colado_ao_ultimo_voto', '(p40c) 40 ciclos de 20 s colados ao último voto'),
                      ('fila_inocente_40_eleitores_reais_em_fila', '(fila) INOCENTE: 40 eleitores reais em fila, no ritmo da própria seção')):
        a = cal5[rot]
        w(f"  {nome}: {n0(a['votos_plantados'])} votos ({n0(a['equivalente_nacional'])} no país).")
        w(f"      RAJ pega {pc(a['fracao_acusada_RAJ'], 1)}; T17 {pc(a['fracao_acusada_T17'], 1)}; T17o {pc(a['fracao_acusada_T17o'], 1)}. V recupera {n0(a['efeito_em_V'])} ({pc(a['fracao_recuperada_em_V'])} dos votos). Elo {ce(a['elo']['coef'], a['elo']['ep'], 3)}. Veredito: {a['veredito_que_o_teste_daria']}.")
    w('  Leitura: o teste recupera o bloco sintético inteiro e só um décimo da fila real; separa as duas. O teto T17 não separa, por construção.')
    w('  O plantio de 40 votos soma 0,76% dos votos, abaixo dos 25% da margem, por isso dá inconclusivo e não sinal; o de 15 fica abaixo de 10% e dá sem sinal.')
    w('')
    w('=' * 100)
    w('DESCRITIVO PEDIDO: POR ONDE ENTRARAM E QUANDO (amostra L, seções pares)')
    w('=' * 100)
    dl = ds['L']
    for gname, rot in (('subiu', 'Seções em que o comparecimento SUBIU'), ('caiu', 'Seções em que o comparecimento CAIU')):
        q = dl[gname]
        vt = q['variacao_por_tipo']
        w(f"{rot}: {n0(q['secoes'])} seções, de {n0(q['votos_1T'])} para {n0(q['votos_2T'])} votos ({'+' if q['variacao_votos'] > 0 else ''}{n0(q['variacao_votos'])}).")
        w(f"    BIO {n0(vt['BIO'])} ({pc(q['fracao_da_variacao_por_tipo']['BIO'], 1)} da variação); ANO {n0(vt['ANO'])} ({pc(q['fracao_da_variacao_por_tipo']['ANO'], 1)}); MAN {n0(vt['MAN'])} ({pc(q['fracao_da_variacao_por_tipo']['MAN'], 1)}).")
        w(f"    Dentro do MAN: mesário identificado {n0(vt['MAN_MES'])}; dedo já visto {n0(vt['MAN_NAO'])}; dedo novo {n0(vt['MAN_NOVO'])}. BIO difíceis {n0(vt['BIO3'])}.")
        w(f"    Composição no 1º turno: BIO {pc(q['composicao_1T']['BIO'], 1)}, ANO {pc(q['composicao_1T']['ANO'], 1)}, MAN {pc(q['composicao_1T']['MAN'], 1)}.")
        w(f"    Antes do meio-dia (Brasília): {pc(q['fracao_dos_votos_antes_de_12h_1T'], 1)} dos votos no 1º turno e {pc(q['fracao_dos_votos_antes_de_12h_2T'], 1)} no 2º. Depois das 17h: variação de {n0(q['variacao_depois_de_17h'])} votos.")
    lq = dl['liquido']
    w(f"Líquido das {n0(lq['secoes'])} seções: +{n0(lq['variacao_votos'])} votos ({pc(lq['variacao_relativa_do_comparecimento'], 2)}). BIO {n0(lq['variacao_por_tipo']['BIO'])}, ANO {n0(lq['variacao_por_tipo']['ANO'])}, MAN {n0(lq['variacao_por_tipo']['MAN'])}.")
    w(f"    A biometria reconhecida responde por {pc(lq['fracao_BIO_no_aumento_liquido'], 1)} do aumento líquido (IC de {pc(lq['fracao_BIO_ic95'][0], 1)} a {pc(lq['fracao_BIO_ic95'][1], 1)}). Fica abaixo dos 90% da leitura fixada no N1.")
    w(f"    ANO e MAN somam {pc(1 - lq['fracao_BIO_no_aumento_liquido'], 1)} do aumento, contra {pc((t1['ANO'] + t1['MAN']) / t1['C'], 1)} dos votos do 1º turno. No país, o aumento bruto equivale a {n0(X['X3_variacao_bruta_de_ANO_equivalente_nacional'])} votos ANO")
    w(f"    e {n0(X['X3_variacao_bruta_de_MAN_equivalente_nacional'])} votos MAN (o bweb conta +290.239 liberações no país: a amostra reproduz).")
    w('Horas: o 2º turno inteiro andou para a manhã (um cargo só, sem fila), nas seções que subiram e nas que caíram por igual.')
    w('    Hora de Brasília   subiu 1T   subiu 2T   caiu 1T   caiu 2T   diferença em diferenças')
    for h, q in X['X7_hora_dif_em_dif_L'].items():
        if q['subiu_1T'] + q['subiu_2T'] > 0:
            w(f"    {h}                {pc(q['subiu_1T'], 1):>7}   {pc(q['subiu_2T'], 1):>7}   {pc(q['caiu_1T'], 1):>7}   {pc(q['caiu_2T'], 1):>7}   {_fmt(100 * q['dif_em_dif'], 2):>7} ponto")
    w('    Contra as seções que caíram, as que subiram têm um pouco menos de voto às 8h e 9h e um pouco mais das 11h às 13h. Nada no fim do dia.')
    gne = ds['grupo_PI_MA_TO_PB_CE_em_L']
    if gne:
        q = gne['liquido']
        w(f"Grupo PI, MA, TO, PB, CE (em L, {n0(q['secoes'])} seções; amostra pequena): líquido +{n0(q['variacao_votos'])} votos; BIO {n0(q['variacao_por_tipo']['BIO'])}, ANO {n0(q['variacao_por_tipo']['ANO'])}, MAN {n0(q['variacao_por_tipo']['MAN'])}.")
        s_ = gne['subiu']
        c_ = gne['caiu']
        w(f"    Onde subiu ({n0(s_['secoes'])} seções, +{n0(s_['variacao_votos'])}): BIO {pc(s_['fracao_da_variacao_por_tipo']['BIO'], 1)}, ANO {pc(s_['fracao_da_variacao_por_tipo']['ANO'], 1)}, MAN {pc(s_['fracao_da_variacao_por_tipo']['MAN'], 1)}; BIO difíceis +{n0(s_['variacao_por_tipo']['BIO3'])}.")
        w(f"    Onde caiu ({n0(c_['secoes'])} seções, {n0(c_['variacao_votos'])}): saiu BIO ({pc(c_['fracao_da_variacao_por_tipo']['BIO'], 1)} da queda); ANO {n0(c_['variacao_por_tipo']['ANO'])}; MAN {n0(c_['variacao_por_tipo']['MAN'])}.")
        x6 = X['X6_D2_2_por_grupo_de_UF']['grupo_PI_MA_TO_PB_CE_em_L']['estimativas']
        tr = X['X6_traducao_no_grupo']
        w(f"    Exploratório, D2-2 só nesse grupo: MAN sobe {icp(x6['s_MAN'])} e as BIO difíceis sobem {icp(x6['s_BIO3'])};")
        w(f"    razão de cauda ln = {icn(x6['ln_rho'])}; ANO {icp(x6['s_ANO'])}. A liberação do mesário cresceu mais ali que no resto do país,")
        w(f"    acompanhada das BIO difíceis. O limite superior do ln passa de 0,045: nesse grupo a amostra não exclui uma sobra do tamanho de 10% da taxa.")
        w(f"    Em votos do grupo (comparecimento {n0(tr['comparecimento_2T_do_grupo_na_base'])}): sobra de nível de ANO mais MAN {n0(tr['sobra_de_nivel_ANO_mais_MAN_em_votos_do_grupo'])} (de {n0(tr['sobra_de_nivel_ic95_em_votos_do_grupo'][0])} a {n0(tr['sobra_de_nivel_ic95_em_votos_do_grupo'][1])}).")
    w('')
    w('=' * 100)
    w('O QUE PESA A FAVOR E CONTRA A TESE')
    w('=' * 100)
    w('A favor (tudo pequeno em votos)')
    w(f"  1. Elo do D2-2 positivo com IC que exclui zero: gama = {ce(v2['gama_B7']['coef'], v2['gama_B7']['ep'])}. Vem do ganho de Lula ({ce(g['ganho_L']['coef']['x'], g['ganho_L']['ep']['x'])}) e da perda de Flávio ({ce(g['ganho_R']['coef']['x'], g['ganho_R']['ep']['x'])}).")
    xa = b7['L']['ao_lado_ANO_e_MAN_separados']
    xam = b7['M10']['ao_lado_ANO_e_MAN_separados']
    w(f"  2. Separando (conta escrita no código antes de rodar, mas fora do docstring, então exploratória): por voto ANO a mais, margem {ce(xa['margem']['coef']['dANO'], xa['margem']['ep']['dANO'])} em L")
    w(f"     e {ce(xam['margem']['coef']['dANO'], xam['margem']['ep']['dANO'])} em M10; Lula {ce(xa['ganho_L']['coef']['dANO'], xa['ganho_L']['ep']['dANO'])}, Flávio {ce(xa['ganho_R']['coef']['dANO'], xa['ganho_R']['ep']['dANO'])}; placebo {ce(xa['placebo_BN']['coef']['dANO'], xa['placebo_BN']['ep']['dANO'])}.")
    x3n = X['X3_nivel_margem_do_13_sobre_fracao_ANO_e_MAN']['L']
    w(f"     Em nível, a seção com mais ANO não é mais lulista que as vizinhas ({ce(x3n['1T']['coef']['ANO'], x3n['1T']['ep']['ANO'], 3)} no 1º turno, {ce(x3n['2T']['coef']['ANO'], x3n['2T']['ep']['ANO'], 3)} no 2º): a composição não explica sozinha.")
    w(f"     Passa do 0,30 do registro, mas não era a estatística registrada. Tamanho: {_fmt(xa['margem']['coef']['dANO'], 3)} x {n0(X['X3_variacao_bruta_de_ANO_equivalente_nacional'])} = {n0(xa['margem']['coef']['dANO'] * X['X3_variacao_bruta_de_ANO_equivalente_nacional'])} votos de margem.")
    x11 = X['X11_cauda_do_ANO_em_L']
    x9 = X['X9_B7_por_grupo_de_UF']
    w(f"     Cauda (exploratório): {x11['alta_de_5_ou_mais']['secoes']} seções de L com alta de 5 ou mais votos ANO (soma +{n0(x11['alta_de_5_ou_mais']['variacao_de_ANO'])}) contra {x11['queda_de_5_ou_mais']['secoes']} com queda de 5 ou mais;")
    w(f"     nas {x11['alta_de_5_ou_mais']['secoes']}, a margem ficou {n0(x11['alta_de_5_ou_mais']['margem_acima_das_vizinhas_em_votos'])} votos acima das vizinhas ({n(x11['alta_de_5_ou_mais']['margem_acima_das_vizinhas_por_secao'])} por seção, ep {n(x11['alta_de_5_ou_mais']['ep_por_secao'])}): {n0(x11['alta_de_5_ou_mais']['margem_acima_das_vizinhas_em_votos'] / t2['C'] * N2)} no país.")
    w(f"     Por grupo de UF (exploratório): no grupo PI, MA, TO, PB, CE gama = {ce(x9['grupo_PI_MA_TO_PB_CE']['x_total']['margem'][0], x9['grupo_PI_MA_TO_PB_CE']['x_total']['margem'][1])} e ANO {ce(x9['grupo_PI_MA_TO_PB_CE']['dANO']['margem'][0], x9['grupo_PI_MA_TO_PB_CE']['dANO']['margem'][1])};")
    w(f"     nas demais UFs gama = {ce(x9['demais_UFs']['x_total']['margem'][0], x9['demais_UFs']['x_total']['margem'][1])} e ANO {ce(x9['demais_UFs']['dANO']['margem'][0], x9['demais_UFs']['dANO']['margem'][1])}. O elo não está concentrado onde o eleitor de Flávio não voltou.")
    w(f"  3. A fatia de ANO subiu de verdade ({icp(e['s_ANO'])}): o eleitor sem biometria cresceu o dobro do resto. Vale {n0(e['V_ANO']['valor'])} votos (até {n0(e['V_ANO']['ic95'][1])}).")
    w(f"  4. MAN sem nenhuma digital do eleitor capturada subiu {icp(e['B5_semcapt_dif'], 2)} das liberações ({n0(e['B5_semcapt_por_voto_dif_nac']['valor'])} votos no país).")
    x10 = X['X10_MAN_sem_captura_em_L']
    w(f"     Seções com 5 ou mais: {x10['secoes_com_5_ou_mais_1T']} no 1º turno e {x10['secoes_com_5_ou_mais_2T']} no 2º. Sem elo com o voto (exploratório): {ce(x10['elo']['margem']['sem_captura'][0], x10['elo']['margem']['sem_captura'][1])}.")
    w(f"  5. B6: {X['X2_espelho_B6']['sem_explicacao_2T']} seções e {X['X2_espelho_B6']['excesso_de_votos_2T']} votos no 2º turno contra {X['X2_espelho_B6']['sem_explicacao_1T_pela_regra_espelhada']} e {X['X2_espelho_B6']['excesso_de_votos_1T']} no espelho.")
    w(f"  6. Elo do D2-5 positivo pela letra ({ce(em5['margem']['coef']['x'], em5['margem']['ep']['x'], 3)}), mas sustentado por {xs['secoes_retiradas']} seções; vale {n0(em5['margem']['coef']['x'] * f['nac_U_full_2T']['valor'])} votos.")
    w(f"  7. A biometria reconhecida responde por {pc(lq['fracao_BIO_no_aumento_liquido'], 1)} do aumento líquido, não por 90%.")
    w('Contra')
    w(f"  1. O teto de tudo o que entrou a mais sem biometria é {n0(v2['V']['ic95'][1])} votos ({pc(v2['V_limite_superior_em_fracao_da_margem'], 1)} da margem). A margem é 4.430.191.")
    w(f"  2. A liberação pelo mesário não subiu além das biometrias difíceis (ln = {_fmt(e['ln_rho']['valor'], 4)}; limite superior {_fmt(e['ln_rho']['ic95'][1], 4)}).")
    w(f"  3. Fim de fila e sequências sem biometria: menos no 2º turno que no 1º (B3 + B4 = {n0(e['B3B4']['valor'])}).")
    w(f"  4. Liberação por dedo novo ou não associado caiu de {pc(e['B5_dedo_1T']['valor'], 1)} para {pc(e['B5_dedo_2T']['valor'], 1)}. Alertas de eleitor que já votou caíram.")
    w(f"  5. Nenhum voto em ritmo impossível em {n0(t1['C'] + t2['C'])} votos de L; as 4 rajadas do 2º turno são de eleitores com biometria reconhecida, de manhã.")
    w(f"  6. Depois das 17h: {n0(f['nac_T17_2T']['valor'])} votos no país (até {n0(f['nac_T17_2T']['ic95'][1])}); depois das 18h, {n0(u2['T18'])} votos em L. No 1º turno foram {n0(f['nac_T17_1T_aplicada']['valor'])}.")
    w(f"  7. No censo, a seção que ficou aberta até tarde não ganhou margem contra as vizinhas ({n0(tv['margem_associada'])} votos; até {n0(tv['margem_associada_ic95'][1])}).")
    xf = X['X11_variacao_de_ANO_contra_fila_do_1T_entre_locais_do_municipio']
    xg = X['X11_variacao_de_ANO_contra_fila_do_1T']
    w(f"  8. Explicação inocente com apoio parcial (exploratório): o eleitor sem biometria voltou mais nos locais que tiveram mais fila no 1º turno")
    w(f"     (entre locais do mesmo município {ce(xf['coef']['fila_1T'], xf['ep']['fila_1T'])}; dentro do mesmo local {ce(xg['coef']['fila_1T'], xg['ep']['fila_1T'])}).")
    w(f"  9. CURTO (voto computado menos de 4 s depois da habilitação): {n0(u2['CURTO'])} votos em L no 2º turno, cauda natural de um turno com um cargo só")
    xc = X['X4_CURTO_em_L']
    w(f"     (d de 2 s em {xc['d_2T_contagem_por_segundo']['2']} votos, 3 s em {n0(xc['d_2T_contagem_por_segundo']['3'])}, 4 s em {n0(xc['d_2T_contagem_por_segundo']['4'])}, 5 s em {n0(xc['d_2T_contagem_por_segundo']['5'])}); espalhados em {n0(xc['secoes_com_algum'])} seções; sem elo com o voto ({ce(xc['elo']['margem']['coef'], xc['elo']['margem']['ep'], 3)}).")
    w('')
    w('O QUE ESTE TESTE NÃO ENXERGA')
    w('  Voto lançado e registrado no log como biometria reconhecida (programa adulterado na origem): log, boletim e RDV saem do mesmo programa.')
    w('  Eleitor de Flávio registrado como ausente ou que ficou em casa: o teste só vê quem foi habilitado (plantio i3).')
    w('  Inserção por ANO escondida atrás de uma queda natural do comparecimento dos sem biometria: o V supõe a fatia natural estável.')
    w('  Eventos raros fora da amostra: são 0,78% das seções do país; os testes de tamanho valem para o país, os achados locais não.')
    w('  O que decide: cadernos de votação (assinaturas contra o comparecimento) e o confronto pericial das digitais das liberações.')
    w('')
    w('DESVIOS E DECISÕES (todas escritas no docstring antes de rodar, salvo onde dito)')
    w('  1. Pares: 3.874 seções, não as 3.855 do desenho. O leitor usa a identidade da seção gravada no log e os blocos aninhados.')
    w('  2. Contagens por VOTO computado (classe da habilitação que levou ao voto), não por habilitação. Bate com o bweb em todas as seções.')
    w('  3. T17o lido por bloco: todos os votos depois de 15 minutos de mesa parada terminados depois das 17h (é o que faz valer o campo poder).')
    w(f"     Leitura estrita (só o primeiro voto depois da parada): {n0(f['nac_T17o_estrita_2T']['valor'])} votos no país; leitura larga (parada terminada depois das 16:45): {n0(f['nac_T17o_larga_2T']['valor'])}.")
    w('  4. B6: regra de "explicação cadastral" fixada por mim (aptos diferentes do perfil, ou a mesma sobra já no 1º turno). Com ela sobram 7 seções.')
    w('     Sem a regra (b), as 46 seções do 2º turno contariam; com qualquer leitura, a cláusula dá inconclusivo. A régua do perfil (cadastro de 14/07/2026)')
    w('     não é a marca de biometria que a urna usa: há seções com zero eleitor sem biometria no perfil e 18 a 20 votos ANO nos dois turnos.')
    w('  5. B7: controles do D2-1 ao pé da letra (com a variação do comparecimento). Por isso o plantio concentrado dá gama perto de 0,4 e não de 1.')
    w(f"     Sem o controle de comparecimento: gama = {ce(b7['L']['ao_lado_sem_controle_de_comparecimento']['coef'], b7['L']['ao_lado_sem_controle_de_comparecimento']['ep'])}.")
    w('  6. IMP no 1º turno pela letra (só g e regras de relógio); com as regras completas nos dois turnos o V é o mesmo (não há IMP por d ou c).')
    w('  7. Censo: usei a extração de estrutura do bweb feita pela B2 (R27_B2/est2026_*.json.gz), conferida contra a base (comparecimento e hora de')
    w(f"     encerramento iguais em {n0(cs['conferencia_da_estrutura_da_B2']['encerramento_igual_a_base_2T'])} de {n0(cs['universo'])} seções) e contra os meus logs (liberações iguais em todas as pares).")
    w('  8. Plantio (c) do D2-2: fiz 0,345% nos dois desenhos e acrescentei o concentrado somando 0,864%, que o registro não pedia.')
    w('  9. Exploratório (depois de ver o resultado): rajadas uma a uma, elo do D2-5 sem elas, espelho do B6, nível por ANO, CURTO, D2-2 e B7 por grupo de UF,')
    w('     diferença em diferenças por hora, contexto do recuo de relógio, censo com efeito fixo de município. A separação de ANO e MAN no B7 estava no')
    w('     código antes da primeira rodada, mas não no docstring: trato como exploratória.')
    w('')
    w('CONTAGEM')
    w('  Dois vereditos com limiar (D2-2 e D2-5). Estatísticas olhadas: 9 no D2-2 e 7 no D2-5, em L e em M10. Com 16 estatísticas a 5%,')
    w('  o acaso daria perto de 1 intervalo excluindo zero; apareceram 2 a favor (gama do B7 e elo do D2-5) e vários contra (B4, B5, B8, V do D2-5).')
    w('  Nenhum SINAL pela letra. O conferente independente ainda precisa refazer.')
    w('')
    w('ARQUIVOS')
    w('  scripts/analisar_R27_C1.py; resultados/R27_C1_quem_liberou_e_quando.json e .txt; resultados/R27_C1_lista_local.csv;')
    w('  resultados/R27_C1_lista_IMP.csv; resultados/R27_C1_trechos_IMP.txt; trabalho em /home/user/trabalho-eleicao/adendo27/R27_C1/.')
    txt = '\n'.join(L) + '\n'
    assert chr(8211) not in txt and chr(8212) not in txt
    with open(REPO + '/resultados/R27_C1_quem_liberou_e_quando.txt', 'w') as fo:
        fo.write(txt)


def conferir_leitor(n=400, semente=7):
    """Conferência do leitor próprio contra o extrator de referência do desenhista D2, em n pacotes sorteados (sem votos)."""
    import random
    import importlib.util
    caminho = '/home/user/trabalho-eleicao/adendo27/desenho_D2/scripts/extrair_eventos_log.py'
    spec = importlib.util.spec_from_file_location('ref_d2', caminho)
    ref = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(ref)
    arqs = []
    for r, d, fs in os.walk(ARQ):
        for f in fs:
            if f.endswith('-log.jez'):
                arqs.append(os.path.join(r, f))
    arqs.sort()
    random.Random(semente).shuffle(arqs)
    mapa = {BIO: 'BIO', BIO_SL: 'BIO', ANO: 'ANO', MAN_MES: 'MAN_MES', MAN_NAO: 'MAN_NAOASSOC', MAN_NOVO: 'MAN_DEDO_NOVO', MAN_OUT: 'MAN_OUTRO', OUTRO: 'OUTRO'}
    c = collections.Counter()
    for p in arqs[:n]:
        k, o = ler_pacote(p)
        if any(tuple(sg['ident']) != tuple(o['alvo']) and sg['hab'] for sg in o['segs']):
            c['pacotes_com_trecho_de_outra_secao_fora_da_conferencia'] += 1
            continue
        R = ref.ler(p)
        c['pacotes_conferidos'] += 1
        for di, dia in ((0, '04/10/2026'), (1, '25/10/2026')):
            a, b = collections.Counter(), collections.Counter()
            for sg in o['segs']:
                if sg['dia'] == di and tuple(sg['ident']) == tuple(o['alvo']):
                    for r in sg['hab']:
                        if r[C_TCOMP] >= 0:
                            a[mapa[r[C_CLS]]] += 1
                            if r[C_CLS] == BIO and r[C_MAXK] >= 3:
                                a['BIO3'] += 1
            for v in R.get(dia, {}).get('votos', []):
                if v['t_comp'] is not None:
                    b['BIO' if v['classe'] == 'OUTRO' else v['classe']] += 1
                    if v['classe'] == 'BIO' and v['tent'] >= 3:
                        b['BIO3'] += 1
            c['secao_dia_com_contagens_identicas' if a == b else 'secao_dia_com_diferenca'] += 1
            c['votos_comparados'] += sum(v for q, v in a.items() if q != 'BIO3')
    return dict(c)


def _hms(t):
    if t is None:
        return ''
    t = int(t)
    return '%02d:%02d:%02d' % (t // 3600, (t % 3600) // 60, t % 60)


def _trecho(arquivo, bloco, linha, antes, depois):
    for nome, linhas in _blocos(arquivo):
        if bloco is None or nome == bloco:
            out = []
            for l in linhas[max(0, linha - antes):linha + depois + 1]:
                p = l.split('\t')
                out.append('\t'.join(p[:5]))
            return out
    return []


def carrega_estrutura_b2():
    """Estrutura por seção extraída do bweb pela B2 (sem votos): comparecimento, liberações, abertura e encerramento."""
    def _i(x):
        try:
            return int(x)
        except (TypeError, ValueError):
            return None
    out = {}
    for t in ('1', '2'):
        with gzip.open(f'/home/user/trabalho-eleicao/adendo27/R27_B2/est2026_{t}t.json.gz', 'rt') as f:
            e = json.load(f)
        ix = {c: i for i, c in enumerate(e['campos'])}
        a, b, c, d = ix['QT_COMPARECIMENTO'], ix['QT_ELEI_BIOM_SEM_HABILITACAO'], ix['DT_ENCERRAMENTO'], ix['DT_ABERTURA']
        out[t] = {k: (_i(r[a]), _i(r[b]), r[c], r[d]) for k, r in e['secoes'].items()}
        del e
    return out


def censo_encerramentos(D):
    """Censo do país: seções que encerraram depois de 17:30 de Brasília, por turno, e o elo com o voto (R-8)."""
    np = D.np
    base = D.base
    est = D.est
    dia = {'1': '2026-10-04', '2': '2026-10-25'}

    def seg(ts, t):
        # segundos desde 00:00 do dia da eleição (hora local)
        if not ts or len(ts) < 19:
            return None
        d, h = ts[:10], ts[11:19]
        s = int(h[:2]) * 3600 + int(h[3:5]) * 60 + int(h[6:8])
        if d == dia[t]:
            return s
        try:
            import datetime
            dd = (datetime.date.fromisoformat(d) - datetime.date.fromisoformat(dia[t])).days
        except ValueError:
            return None
        return s + 86400 * dd

    chaves, fora = [], collections.Counter()
    confere = collections.Counter()
    for k, v in base.items():
        if k.startswith('ZZ|'):
            fora['exterior'] += 1
            continue
        if '1' not in v or '2' not in v:
            fora['sem_os_dois_turnos'] += 1
            continue
        a, b = v['1'], v['2']
        if a['tipo'] != 'Apurada' or b['tipo'] != 'Apurada':
            fora['tipo_nao_apurada'] += 1
            continue
        if a['comp'] < 50 or b['comp'] < 50:
            fora['comparecimento_menor_que_50'] += 1
            continue
        if abs(a['apt'] - b['apt']) > 2:
            fora['aptos_variam_mais_de_2'] += 1
            continue
        if k not in est['1'] or k not in est['2']:
            fora['sem_estrutura_bweb'] += 1
            continue
        chaves.append(k)
    n = len(chaves)
    cols = {c: np.zeros(n) for c in ('L1', 'R1', 'O1', 'B1', 'N1', 'C1', 'L2', 'R2', 'B2', 'N2', 'C2', 'H1', 'U', 'enc1', 'enc2')}
    fe, mun = [], []
    semenc = collections.Counter()
    for i, k in enumerate(chaves):
        a, b = base[k]['1'], base[k]['2']
        uf, m = k.split('|')[:2]
        off = (8 - D.fuso_mun.get(uf + '|' + m, UF_FUSO.get(uf, 8))) * 3600.0
        for t, x in (('1', a), ('2', b)):
            r = est[t][k]
            e = seg(r[2], t)
            if e is None:
                semenc[t] += 1
                e = float('nan')
            cols['enc' + t][i] = e + off
            if r[0] == x['comp']:
                confere['comparecimento_igual_a_base_%sT' % t] += 1
            if (r[2] or '')[11:19] == x.get('enc'):
                confere['encerramento_igual_a_base_%sT' % t] += 1
        cols['H1'][i] = est['1'][k][1] if est['1'][k][1] is not None else float('nan')
        cols['L1'][i], cols['R1'][i], cols['O1'][i], cols['B1'][i], cols['N1'][i], cols['C1'][i] = a['L'], a['R'], a['O'], a['B'], a['N'], a['comp']
        cols['L2'][i], cols['R2'][i], cols['B2'][i], cols['N2'][i], cols['C2'][i] = b['L'], b['R'], b['B'], b['N'], b['comp']
        cols['U'][i] = 1.0 if a['urna'] != b['urna'] else 0.0
        fe.append(f"{uf}|{m}|{k.split('|')[2]}|{a['loc']}")
        mun.append(uf + '|' + m)
    fe = np.array(fe)
    mun = np.array(mun)
    C1 = cols['C1']
    out = {'universo': n, 'fora': dict(fora), 'sem_hora_de_encerramento': dict(semenc), 'conferencia_da_estrutura_da_B2': dict(confere)}
    for t in ('1', '2'):
        e = cols['enc' + t]
        tard = e > 63000
        out['tardias_%sT' % t] = {'secoes': int(np.nansum(tard)), 'comparecimento': float(cols['C' + t][tard].sum()),
                                  'fracao_das_secoes': float(np.nanmean(tard)),
                                  'depois_de_18h': int((e > 64800).sum()), 'depois_de_19h': int((e > 68400).sum()),
                                  'depois_de_19h30': int((e > 70200).sum()),
                                  'comparecimento_depois_de_18h': float(cols['C' + t][e > 64800].sum()),
                                  'mediana_do_encerramento': _hms(float(np.nanmedian(e)))}
        ufs = collections.Counter(k.split('|')[0] for k, q in zip(chaves, tard) if q)
        out['tardias_%sT' % t]['por_UF_10_maiores'] = ufs.most_common(10)
    y = ((cols['L2'] - cols['R2']) - (cols['L1'] - cols['R1'])) / C1
    yL = (cols['L2'] - cols['L1']) / C1
    yR = (cols['R2'] - cols['R1']) / C1
    yBN = ((cols['B2'] + cols['N2']) - (cols['B1'] + cols['N1'])) / C1
    ctrl = [(cols['C2'] - C1) / C1, cols['O1'] / C1, (cols['B1'] + cols['N1']) / C1, cols['L1'] / C1, cols['H1'] / C1, cols['U']]
    nctrl = ['dC', 'O1', 'BN1', 'L1', 'H1', 'urna_trocada']
    ok = np.isfinite(cols['enc1']) & np.isfinite(cols['enc2'])
    tard2 = (cols['enc2'] > 63000).astype(float)
    tard1 = (cols['enc1'] > 63000).astype(float)
    atr2 = np.maximum(0, (cols['enc2'] - 61200) / 60.0)

    def roda(xs, nomes, ys):
        X = np.column_stack(xs + ctrl)
        o = {}
        for rot, yy in ys:
            r = fe_reg(yy[ok], X[ok], fe[ok], C1[ok], mun[ok], nomes + nctrl)
            o[rot] = {'coef': {q: r['coef'].get(q) for q in nomes}, 'ep': {q: r['ep'].get(q) for q in nomes}, 'n': r['n'],
                      'conglomerados': r['conglomerados']}
            if len(nomes) == 1:
                o[rot]['ic95'] = _ic(r['coef'][nomes[0]], r['ep'][nomes[0]])
                o[rot]['coef'] = r['coef'][nomes[0]]
                o[rot]['ep'] = r['ep'][nomes[0]]
        return o

    ys = [('margem', y), ('ganho_L', yL), ('ganho_R', yR), ('placebo_BN', yBN)]
    out['regressao_tardia2'] = roda([tard2], ['tardia2'], ys)
    out['regressao_minutos_de_atraso2'] = roda([atr2], ['minutos_atraso2'], ys)
    out['ao_lado_regressao_tardia1_como_placebo'] = roda([tard1], ['tardia1'], [('margem', y)])
    out['ao_lado_regressao_tardia2_e_tardia1_juntas'] = roda([tard2, tard1], ['tardia2', 'tardia1'], [('margem', y)])
    # sem o controle de comparecimento (voto a mais na prorrogação mexe em x e em dC ao mesmo tempo)
    X = np.column_stack([tard2] + ctrl[1:])
    r = fe_reg(y[ok], X[ok], fe[ok], C1[ok], mun[ok], ['tardia2'] + nctrl[1:])
    out['ao_lado_tardia2_sem_controle_de_comparecimento'] = {'coef': r['coef']['tardia2'], 'ep': r['ep']['tardia2'], 'ic95': _ic(r['coef']['tardia2'], r['ep']['tardia2'])}
    # comparecimento: a seção tardia teve mais comparecimento a mais?
    r = fe_reg(((cols['C2'] - C1) / C1)[ok], tard2[ok][:, None], fe[ok], C1[ok], mun[ok], ['tardia2'])
    out['ao_lado_variacao_do_comparecimento_sobre_tardia2'] = {'coef': r['coef']['tardia2'], 'ep': r['ep']['tardia2']}
    # placebo do 1T em corte e o mesmo corte no 2T
    v1 = cols['L1'] + cols['R1'] + cols['O1']
    r = fe_reg((cols['L1'] / v1)[ok], tard1[ok][:, None], fe[ok], C1[ok], mun[ok], ['tardia1'])
    out['placebo_corte_1T_fatia_do_13_sobre_tardia1'] = {'coef': r['coef'].get('tardia1'), 'ep': r['ep'].get('tardia1'), 'n': r['n']}
    v2 = cols['L2'] + cols['R2']
    r = fe_reg((cols['L2'] / v2)[ok], tard2[ok][:, None], fe[ok], C1[ok], mun[ok], ['tardia2'])
    out['ao_lado_corte_2T_fatia_do_13_sobre_tardia2'] = {'coef': r['coef'].get('tardia2'), 'ep': r['ep'].get('tardia2'), 'n': r['n']}
    # exploratório (depois de ver o resultado): quantos locais têm seção tardia e não tardia, e a conta entre locais do mesmo município
    _, gl = np.unique(fe[ok], return_inverse=True)
    nl = np.bincount(gl)
    st = np.bincount(gl, weights=tard2[ok])
    misto = (st > 0) & (st < nl)
    out['exploratorio_locais'] = {'locais_com_alguma_tardia_2T': int((st > 0).sum()), 'locais_mistos_2T': int(misto.sum()),
                                  'secoes_tardias_em_locais_mistos': int(st[misto].sum()),
                                  'secoes_tardias_em_locais_inteiros_tardios': int(st[(st > 0) & ~misto].sum())}
    X = np.column_stack([tard2] + ctrl)
    out['exploratorio_efeito_fixo_de_municipio'] = {}
    for rot, yy in ys:
        r = fe_reg(yy[ok], X[ok], mun[ok], C1[ok], mun[ok], ['tardia2'] + nctrl)
        out['exploratorio_efeito_fixo_de_municipio'][rot] = {'coef': r['coef']['tardia2'], 'ep': r['ep']['tardia2'],
                                                             'ic95': _ic(r['coef']['tardia2'], r['ep']['tardia2']), 'n': r['n']}
    Lp = cols['L2'] + 40 * tard2
    Cp = cols['C2'] + 40 * tard2
    ypm = ((Lp - cols['R2']) - (cols['L1'] - cols['R1'])) / C1
    Xpm = np.column_stack([tard2, (Cp - C1) / C1] + ctrl[1:])
    r = fe_reg(ypm[ok], Xpm[ok], mun[ok], C1[ok], mun[ok], ['tardia2'] + nctrl)
    out['exploratorio_efeito_fixo_de_municipio']['plantio_40_votos_coef'] = r['coef']['tardia2']
    c1t = float(C1[ok & (tard2 > 0)].sum())
    g = out['regressao_tardia2']['margem']
    out['traducao_em_votos'] = {'C1_das_tardias_2T': c1t, 'margem_associada': g['coef'] * c1t,
                                'margem_associada_ic95': [g['ic95'][0] * c1t, g['ic95'][1] * c1t],
                                'em_fracao_da_margem': g['coef'] * c1t / MARGEM}
    # plantio no censo: 40 votos a mais para o 13 em cada seção tardia (o que a hipótese (a) diria)
    L2p = cols['L2'] + 40 * tard2
    C2p = cols['C2'] + 40 * tard2
    yp = ((L2p - cols['R2']) - (cols['L1'] - cols['R1'])) / C1
    Xp = np.column_stack([tard2, (C2p - C1) / C1] + ctrl[1:])
    r = fe_reg(yp[ok], Xp[ok], fe[ok], C1[ok], mun[ok], ['tardia2'] + nctrl)
    Xq = np.column_stack([tard2] + ctrl[1:])
    r2 = fe_reg(yp[ok], Xq[ok], fe[ok], C1[ok], mun[ok], ['tardia2'] + nctrl[1:])
    out['plantio_40_votos_para_o_13_em_cada_tardia'] = {
        'votos_plantados': float(40 * tard2[ok].sum()), 'coef_com_controle_de_comparecimento': r['coef']['tardia2'], 'ep': r['ep']['tardia2'],
        'coef_sem_controle_de_comparecimento': r2['coef']['tardia2'], 'ep_sem': r2['ep']['tardia2'],
        'efeito_no_coef_sem_controle': r2['coef']['tardia2'] - out['ao_lado_tardia2_sem_controle_de_comparecimento']['coef'],
        'efeito_no_coef_com_controle': r['coef']['tardia2'] - g['coef']}
    return out


def descritivo(D, am, S1, S2, T1, T2):
    """Q-1: por qual tipo de habilitação e em que horas entraram os eleitores a mais; que tipo saiu onde caiu."""
    np = D.np
    out = {}

    def horas(rec, off):
        h = np.clip(((rec['tcomp'] + off) // 3600).astype(int), 0, 23)
        cls = rec['cls']
        grp = np.where((cls == BIO) | (cls == BIO_SL), 0, np.where(cls == ANO, 1, np.where((cls >= MAN_MES) & (cls <= MAN_OUT), 2, 3)))
        M = np.zeros((4, 24))
        np.add.at(M, (grp, h), 1)
        return M

    def bloco(chs):
        o = {}
        if not chs:
            return o
        ii = np.array([D.ix[k] for k in chs], int)
        dC = S2[ii, I22['C']] - S1[ii, I22['C']]
        grupos = {'subiu': dC > 0, 'caiu': dC < 0, 'igual': dC == 0}
        H1 = np.array([horas(D.rec[k][0], D.off[k]) for k in chs])
        H2 = np.array([horas(D.rec[k][1], D.off[k]) for k in chs])
        C2tot = S2[ii, I22['C']].sum()
        for g, msk in grupos.items():
            q = {'secoes': int(msk.sum())}
            if msk.sum() == 0:
                o[g] = q
                continue
            s1, s2 = S1[ii][msk].sum(axis=0), S2[ii][msk].sum(axis=0)
            q['votos_1T'] = float(s1[I22['C']])
            q['votos_2T'] = float(s2[I22['C']])
            q['variacao_votos'] = float(s2[I22['C']] - s1[I22['C']])
            var = {}
            for nome in ('BIO', 'ANO', 'MAN', 'MAN_MES', 'MAN_NAO', 'MAN_NOVO', 'OUTRO', 'BIO3'):
                var[nome] = float(s2[I22[nome]] - s1[I22[nome]])
            q['variacao_por_tipo'] = var
            tot = q['variacao_votos']
            q['fracao_da_variacao_por_tipo'] = {nome: (var[nome] / tot if tot else None) for nome in ('BIO', 'ANO', 'MAN', 'OUTRO')}
            q['composicao_1T'] = {nome: float(s1[I22[nome]] / s1[I22['C']]) for nome in ('BIO', 'ANO', 'MAN')}
            q['composicao_2T'] = {nome: float(s2[I22[nome]] / s2[I22['C']]) for nome in ('BIO', 'ANO', 'MAN')}
            q['equivalente_nacional_da_variacao'] = {nome: var[nome] / C2tot * N2 for nome in ('BIO', 'ANO', 'MAN')}
            q['equivalente_nacional_da_variacao']['total'] = tot / C2tot * N2
            dH = (H2[msk] - H1[msk]).sum(axis=0)
            h1, h2 = H1[msk].sum(axis=0), H2[msk].sum(axis=0)
            q['por_hora_de_brasilia'] = {f'{h:02d}h': {'votos_1T': float(h1[:, h].sum()), 'votos_2T': float(h2[:, h].sum()),
                                                      'variacao': float(dH[:, h].sum()), 'variacao_BIO': float(dH[0, h]),
                                                      'variacao_ANO': float(dH[1, h]), 'variacao_MAN': float(dH[2, h])}
                                         for h in range(6, 21) if h1[:, h].sum() + h2[:, h].sum() > 0}
            man = dH[:, :12].sum()
            q['variacao_manha_antes_de_12h'] = float(man)
            q['variacao_tarde_12h_em_diante'] = float(dH[:, 12:].sum())
            q['variacao_depois_de_17h'] = float((T2[ii, I25['T17']][msk] - T1[ii, I25['T17']][msk]).sum())
            q['fracao_dos_votos_antes_de_12h_1T'] = float(h1[:, :12].sum() / h1.sum())
            q['fracao_dos_votos_antes_de_12h_2T'] = float(h2[:, :12].sum() / h2.sum())
            o[g] = q
        tot1, tot2 = S1[ii].sum(axis=0), S2[ii].sum(axis=0)
        o['liquido'] = {'secoes': len(chs), 'variacao_votos': float(tot2[I22['C']] - tot1[I22['C']]),
                        'variacao_por_tipo': {nome: float(tot2[I22[nome]] - tot1[I22[nome]]) for nome in ('BIO', 'ANO', 'MAN', 'MAN_MES', 'MAN_NAO', 'MAN_NOVO', 'OUTRO')}}
        lv = o['liquido']['variacao_votos']
        o['liquido']['fracao_BIO_no_aumento_liquido'] = (o['liquido']['variacao_por_tipo']['BIO'] / lv) if lv else None
        o['liquido']['variacao_relativa_do_comparecimento'] = lv / float(tot1[I22['C']])
        return o

    for a in ('L', 'M10', 'todas'):
        out[a] = bloco(am[a])
    ne = [k for k in am['todas'] if k.split('|')[0] in GRUPO_NE]
    rs = [k for k in am['todas'] if k.split('|')[0] not in GRUPO_NE]
    out['grupo_PI_MA_TO_PB_CE_todas_as_amostras'] = bloco(ne)
    out['demais_UFs_todas_as_amostras'] = bloco(rs)
    out['grupo_PI_MA_TO_PB_CE_em_L'] = bloco([k for k in am['L'] if k.split('|')[0] in GRUPO_NE])
    # IC do aumento por tipo em L (reamostragem de locais): fração do aumento líquido que entrou por BIO
    ii = np.array([D.ix[k] for k in am['L']], int)
    (r1, R1), (r2, R2) = reamostra([S1[ii], S2[ii]], D.conglomerado(am['L'], 'local'))[0]
    dl = R2[:, I22['C']] - R1[:, I22['C']]
    fb = (R2[:, I22['BIO']] - R1[:, I22['BIO']]) / dl
    out['L']['liquido']['fracao_BIO_ic95'] = [float(x) for x in np.percentile(fb, [2.5, 97.5])]
    for nome in ('BIO', 'ANO', 'MAN'):
        x = (R2[:, I22[nome]] / R2[:, I22['C']] * (R2[:, I22['C']] / R1[:, I22['C']]) - R1[:, I22[nome]] / R1[:, I22['C']])
        out['L']['liquido']['variacao_%s_por_voto_do_1T' % nome] = {
            'valor': float((r2[I22[nome]] - r1[I22[nome]]) / r1[I22['C']]), 'ic95': [float(q) for q in np.percentile(x, [2.5, 97.5])]}
    return out


if __name__ == '__main__':
    modo = sys.argv[1] if len(sys.argv) > 1 else ''
    if modo == 'extrair':
        modo_extrair()
    elif modo == 'perfil':
        modo_perfil()
    elif modo == 'rodar':
        modo_rodar()
    elif modo == 'txt':
        escrever_txt(json.load(open(REPO + '/resultados/R27_C1_quem_liberou_e_quando.json')))
    if modo in ('rodar', 'txt'):
        import hashlib
        fin = {}
        for nome in ('scripts/analisar_R27_C1.py', 'resultados/R27_C1_quem_liberou_e_quando.json', 'resultados/R27_C1_quem_liberou_e_quando.txt',
                     'resultados/R27_C1_lista_local.csv', 'resultados/R27_C1_lista_IMP.csv', 'resultados/R27_C1_trechos_IMP.txt'):
            if os.path.exists(REPO + '/' + nome):
                fin[nome] = hashlib.sha256(open(REPO + '/' + nome, 'rb').read()).hexdigest()
        json.dump(fin, open(TRAB + '/sha256_finais.json', 'w'), indent=1)
    else:
        print(__doc__)
