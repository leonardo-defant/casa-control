"""R27_B1: CARGA, LOTE, FLASHCARD E ZONA.

Adendo 27 do pré-registro (commit 2748895, 10/11/2026 00:16:42 UTC), Onda B, item B1, mantido pelo Adendo 28 (commit
938be19). Três peças, com o critério de cada uma valendo como escrito no registro:
  PARTE 1  D1.1 de registro/adendo27/desenho_D1_proposta.json por inteiro (contrastes por modelo, lote, carga e
           flashcard dentro do mesmo prédio), com as DEFINIÇÕES COMUNS do campo "frente".
  PARTE 2  fragilidade "F9 (computador da mídia), L2 (carga e urna trocada) e T20 (pendências de carga)" de
           registro/adendo27/equipe_vermelha_relatorio.json (desenho entre zonas, sem efeito fixo de local).
  PARTE 3  D3-4 de registro/adendo27/desenho_D3_proposta.json (identidade da urna e boletins repetidos).
Aviso do registro: o D1.1 e o D3-4 são desenhos cegos; o reteste da equipe vermelha foi escrito por quem conhecia os
resultados antigos (o critério é novo, a escolha do que retestar é posterior ao dado).

Este docstring foi escrito ANTES de qualquer conta com votos. Até aqui só foi lida estrutura sem voto: campos da urna
no bweb (estrutura_1t e estrutura_2t do desenhista D1, meta1t, meta2t e grupos_2t do desenhista D3), as linhas do log
que nomeiam computador, usuário e data das mídias (extração própria, R27_B1/logs_midia.json.gz) e o perfil do
eleitorado. O que o registro não fixa está em DECISÕES e sai no resultado como desvio. O que for feito depois de ver
resultado sai marcado como exploratório.

Uso:
  python3 -I scripts/analisar_R27_B1.py logs       extrai do log computador, usuário e data das mídias (sem votos)
  python3 -I scripts/analisar_R27_B1.py gov        extrai governador do 2º turno nas 6 UFs (bweb do 2º turno)
  python3 -I scripts/analisar_R27_B1.py base       monta as bases em R27_B1/
  python3 -I scripts/analisar_R27_B1.py d11        PARTE 1
  python3 -I scripts/analisar_R27_B1.py ev         PARTE 2
  python3 -I scripts/analisar_R27_B1.py d34        PARTE 3
  python3 -I scripts/analisar_R27_B1.py relatorio  junta os parciais em resultados/R27_B1_carga_lote_zona.json e .txt
Trabalho e parciais: /home/user/trabalho-eleicao/adendo27/R27_B1/

O QUE O REGISTRO FIXA (aplicado à letra)
Definições comuns do D1: universo U = seções do 2º turno de 2026 pareadas com o 1º turno pela chave, com L2 + R2 de
30 ou mais, fora o exterior e as 27 seções com junta apuradora. y = 100 x L2 / (L2 + R2). X = 1º turno na mesma seção
(fração de cada candidato sobre o comparecimento do 1º turno: 13, 22, cada um dos demais com 0,5% ou mais no país,
resto agrupado; brancos; nulos; abstenção do 1º turno; variação da abstenção entre os turnos; perfil do eleitorado;
logaritmo dos aptos; posição da seção no local). Modelo base: y = efeito fixo de local + X + b x D + erro, peso
V = L2 + R2, erro agrupado por município. Phi = 2 x b x soma(D x V) / 100 / 4.430.191. Regra geral: SINAL se Phi de
0,25 ou mais a favor de Lula, |z| de 3,3 ou mais, placebo limpo e mesmo sentido em 4 das 5 regiões; SEM SINAL se o
intervalo de 99% de Phi couber em -0,10 a +0,10 e a calibração mostrar poder de 95% para Phi = 0,25; INCONCLUSIVO no
resto. Secundários: y_BN = 100 x (B2 + N2) / comparecimento do 2º turno; y_alt = y menos a fração de 2022 na mesma
seção, com controles de 2022.
D1.1: (a) UE2022 contra UE2020 nos locais que têm os dois; (b) UE2015 contra UE2013 nos locais mistos; (c) família
nova contra antiga com efeito fixo de zona e município e, como conferência, de local; (d) carga depois de 04/10/2026
contra carga de setembro no mesmo local; (e) urna diferente da do 1º turno contra mesma urna; (f) média do resíduo
por data de carga dentro do local, com Bonferroni; (h) o mesmo por faixa de 5.000 números de série dentro de cada
modelo; (g) componente de variância entre flashcards dentro do local (tau, em p.p.) e assimetria das médias por
flashcard; (g) repetido na amostra de logs por computador e usuário da mídia de carga e da mídia de resultado.
Critérios: (a), (b), (c) regra geral com |z| de 3,9 ou mais; (c) só pode dar sinal ou inconclusivo. (d), (e): SINAL
se |b| de 0,45 p.p. ou mais com |z| de 3,3 ou mais e placebo de período anterior de no máximo um terço; SEM SINAL se
o intervalo de 99% de b couber em -0,18 a +0,18. (g): SINAL se o excesso de tau sobre o placebo, raiz(tau2 de 2026
menos tau2 do placebo), for de 0,22 p.p. ou mais, com limite inferior de 99,9% acima de zero (bootstrap por
município) e assimetria a favor de Lula; SEM SINAL se o limite superior de 99% do excesso ficar abaixo de 0,15.
(f), (h): SINAL se alguma data ou faixa tiver |z| de 5 ou mais depois de Bonferroni, repetida em 3 UFs ou mais; SEM
SINAL se nenhuma tiver |z| de 5 ou mais. Poder: plantar Phi = 0,10; 0,25; 0,50; 1 (binomial de R para L nas seções
expostas; em (d) e (e), troca uniforme de 1,785% x Phi em todas as seções menos as do grupo), 200 repetições,
detecção em 95% para Phi = 0,25 e viés abaixo de 10%; 200 embaralhamentos do atributo dentro do município com menos
de 1% de falso sinal; em (g), efeito em fração q dos flashcards (0,1; 0,5; 0,8). Placebos: período anterior (os
atributos de 2026 na virada de 2022 e de 2018), cargo (governador do 2º turno nas 6 UFs), turno (1º turno de 2026
com referência em 2022) e ano (modelos de 2022 em 2022).
Equipe vermelha: resíduo de um modelo por UF com a composição completa do 1º turno, sem efeito fixo de local;
variância entre grupos de carga no bweb inteiro (data de carga, código de carga, flashcard) contra permutação dos
grupos entre zonas da mesma UF; na amostra de logs, o mesmo por computador e por data de geração da mídia. SINAL:
componente de variância do grupo de pelo menos 2 vezes o de agrupamentos aleatórios de zonas do mesmo tamanho
(p abaixo de 0,001) e ao menos um grupo com 500 seções ou mais e resíduo de +1,0 ponto ou mais a mais de 4 ep
(agrupado por zona). SEM SINAL: p acima de 0,05 e nenhum grupo acima de +0,5.
D3-4: (a) censo de número de urna e código de carga repetidos por turno; C_exato = pares de seções com vetor completo
idêntico (comparecimento, 13, 22, brancos, nulos, biometria sem habilitação, segundo do encerramento e segundo da
emissão) contra 1.000 permutações dos horários dentro da UF; C_votos = pares com (comparecimento, 13, 22, brancos,
nulos) idênticos entre seções com 50 votos ou mais, contra a média de 200 reamostragens multinomiais; rho = C_votos
sobre a média, também para 2022 e para o 1º turno de 2026. SINAL: urna ou carga repetida fora das seções de junta; ou
C_exato de 3 ou mais e acima do percentil 99,9; ou rho de 2026 pelo menos 25% acima do maior placebo com excesso de
3.000 pares ou mais. SEM SINAL: nenhuma repetição, C_exato dentro do percentil 95 e rho dentro de 25% dos placebos.
(b) y = fatia de Lula nos válidos do 2º turno; S = urna diferente entre os turnos (segunda rodada: carga depois de
04/10); controles: fatias do 13, do 22, dos outros com 1% ou mais e de brancos e nulos sobre o comparecimento do
1º turno, variação do comparecimento, log dos aptos, fatia de 60 anos ou mais; efeito fixo de local; peso = válidos
do 2º turno; erro por município. SINAL: beta_S de +1,0 ou mais com p < 0,001 e placebo abaixo de 0,3 em módulo.
SEM SINAL: intervalo de 95% inteiro entre -1,0 e +1,0. Placebo: fatia de Lula no 1º turno de 2026 controlada pela
fatia do 2º turno de 2022. Poder: copiar o vetor completo de 5 seções (C_exato sobe 5); copiar os votos de 3.000
seções grandes para outras 3.000 de mesmo comparecimento (rho passa o limiar); mover 1,8% dos válidos do 22 para o 13
nas seções tratadas (beta_S perto de +1,8 com p < 0,001).

DECISÕES QUE O REGISTRO NÃO FIXA (tomadas aqui, antes de calcular qualquer coisa com votos)
Gerais
G1. Junta apuradora = NR_JUNTA_APURADORA diferente de -1 no 2º turno (27 seções, todas no exterior). "0,5% ou mais no
    país" = votos do candidato no 1º turno sobre o comparecimento nacional do 1º turno (com exterior). O "resto
    agrupado" (demais candidatos e o candidato anulado) é a categoria de referência. Abstenção do 1º turno = 1 menos
    comparecimento/aptos; variação = abstenção do 2º menos a do 1º. Logaritmo dos aptos = ln(aptos do 2º turno).
    Posição = (ordem da seção pelo número entre as seções do 2º turno do mesmo local, menos 1) / (seções menos 1),
    zero em local de seção única.
G2. Perfil do eleitorado: reaproveito a extração por seção feita no teste A6 a partir do F15
    (R27_A6/perfil_secao_2026_A6.json.gz: contagens de eleitores por sexo, 8 faixas de idade, 8 graus de escolaridade
    e com biometria; não tem voto). Seção com agregadas (DS_SECOES_AGREGADAS do 2º turno) soma a principal com as
    agregadas. Entram: fração de mulheres, 7 frações de idade (referência 35 a 44), 7 de escolaridade (referência
    ensino médio completo) e fração com biometria. Seção sem perfil sai das contas que usam perfil (contagem dita).
G3. Regressão: mínimos quadrados ponderados com transformação dentro do efeito fixo e erro agrupado CR1 por município
    (UF mais código), em função própria (classe Modelo), conferida contra lib.fe_ols com o agrupamento no próprio
    efeito fixo. Grupo de efeito fixo com uma só observação não informa. z = b / erro. Intervalo de 99% = b mais ou
    menos 2,5758 erros; de 95%, 1,96; de 99,9% unilateral no bootstrap, percentil 0,1.
G4. Regiões: Norte (AC AM AP PA RO RR TO), Nordeste (AL BA CE MA PB PE PI RN SE), Sudeste (ES MG RJ SP), Sul (PR RS
    SC), Centro-Oeste (DF GO MS MT). "Mesmo sentido" = sinal do b da região (regressão refeita só com a região) igual
    ao do b nacional. Região sem variação do atributo não conta nem a favor nem contra (dito no resultado).
G5. Ordem do veredito de cada parte: SINAL se todas as condições do critério estiverem presentes (em qualquer dos dois
    sentidos, dito qual); senão SEM PODER se a calibração não enxergar o tamanho que o registro indica; senão SEM
    SINAL se couber no critério; senão INCONCLUSIVO. Semente 20261110.

Parte 1 (D1.1)
A1. Modelo da urna pelo número de série do 2º turno (scripts/modelos.py, faixas de 2026). Amostra de (a): seções de
    U com UE2020 ou UE2022 em locais que têm os dois; D = 1 na UE2022. Amostra de (b): seções com UE2013 ou UE2015
    em locais que têm os dois; D = 1 na UE2015. (c): todo U, D = 1 na família nova, efeito fixo de zona e município
    (UF, município, zona); conferência com efeito fixo de local. (d): todo U, D = 1 se a data de carga do 2º turno é
    posterior a 04/10/2026. (e): todo U, D = 1 se a urna do 2º turno difere da do 1º. (d) e (e) vêm dos grupos
    congelados pelo desenhista D3 (carga_pos, urna_dif), um por vez; ao lado, os dois juntos na mesma regressão.
    Conferência de (a) e (b): todo U com indicadoras de modelo e efeito fixo de local.
A2. Phi dos contrastes de fatia. O contraste entre duas classes de urna não diz em qual delas estaria a alteração.
    Phi_1 = 2 x b x V1 / 100 / 4.430.191, com V1 = votos válidos (L2 + R2) de todas as seções de U na classe D = 1
    (alteração a favor de Lula nas urnas D = 1 quando b é positivo); Phi_0 = 2 x (menos b) x V0 / 100 / 4.430.191,
    com V0 o mesmo na classe D = 0 (alteração a favor de Lula nas urnas D = 0 quando b é negativo). O Phi "a favor
    de Lula" da regra é Phi_1 se b for positivo e Phi_0 se for negativo; a leitura espelho (mesma diferença como
    alteração a favor de Flávio na outra classe) tem o mesmo tamanho e é dita junto. SEM SINAL pede o intervalo de
    99% dentro de 0,10 na escala da classe maior (a mais exigente). Para (d) e (e) vale a letra: Phi = menos b / 1,785.
A3. Placebo limpo = Phi (ou b) do placebo de período anterior de 2022 de no máximo um terço do Phi (ou b) do teste,
    em módulo. A leitura absoluta (um terço de Phi = 1) sai ao lado. O placebo de 2018 e os de cargo, turno e ano saem
    ao lado e não decidem sozinhos; se o de 2022 mostrar efeito do mesmo tamanho o veredito não pode ser SINAL.
    Os placebos só decidem quando as condições numéricas de SINAL estão presentes.
A4. Placebo de período anterior: desfecho 100 x L2/(L2+R2) de 2022 (ou 2018) na mesma chave de seção, com L2 + R2 de
    30 ou mais naquele ano; X = frações de L, R, brancos e nulos sobre o comparecimento do 1º turno daquele ano
    (outros = referência), abstenção do 1º turno e variação da abstenção daquele ano, perfil de 2026, ln dos aptos do
    2º turno daquele ano e posição; D, amostra e efeito fixo de 2026; peso = L2 + R2 daquele ano.
    Placebo de turno: desfecho 100 x L1/(L1+R1) do 1º turno de 2026 (L1 + R1 de 30 ou mais); controles: fração de
    2022 do 2º turno, frações do 1º turno de 2022, abstenção do 1º turno de 2022, abstenção do 1º de 2026 menos a do
    1º de 2022, perfil, ln dos aptos do 1º turno, posição; peso L1 + R1; D do 2º turno de 2026 (a urna é a mesma em
    99% das seções; em (d) e (e) o desfecho é anterior à carga tardia e à troca).
    Placebo de cargo: governador do 2º turno em AC, AM, DF, ES, RN e TO; desfecho 100 x votos do candidato "do lado
    de Lula" / votos dos dois, sendo "do lado de Lula" aquele cuja fração por seção tem correlação ponderada positiva
    com y na UF; X por UF (colunas próprias de cada UF): frações de cada candidato a governador do 1º turno com 0,5%
    ou mais do comparecimento da UF, brancos e nulos de governador, abstenção, variação da abstenção, perfil, ln dos
    aptos, posição; peso = votos dos dois; erro por município, e por zona no DF (um município só).
    Placebo de ano: desfecho, X, local e modelo de urna de 2022 (número de série do 2º turno de 2022, faixas de 2022
    de scripts/modelos.py): UE2020 contra as anteriores com efeito fixo de zona e município e de local; UE2015 contra
    UE2013 nos locais mistos de 2022.
A5. y_alt = y menos 100 x L2/(L2+R2) de 2022 na mesma seção; controles de 2022 (frações de L, R, brancos e nulos do
    1º turno de 2022, abstenção do 1º turno de 2022, variação da abstenção de 2022, abstenção do 2º turno de 2026
    menos a do 2º de 2022), perfil, ln dos aptos, posição; peso V. y_BN com o mesmo X e o mesmo peso V do modelo
    base. Escala de y_BN: Phi_BN = menos b_BN / 100 x soma(D x comparecimento do 2º turno) / 4.430.191 (positivo =
    menos branco e nulo nas urnas D = 1, o sentido de uma conversão a favor de alguém; não diz de quem).
A6. (f) e (h): uma regressão por data (dia da carga do 2º turno) e uma por faixa (modelo, série // 5.000), cada uma
    com D = 1 naquele grupo contra todos os outros, modelo base em todo U; em (h) as indicadoras de modelo entram
    como controle, para que a comparação seja dentro do modelo. São testados os grupos com 30 seções ou mais e 10
    municípios ou mais em locais onde D varia. "Depois de Bonferroni" = |z| de 5 ou mais e p bilateral vezes o número
    de grupos testados abaixo de 0,05. "Repetida em 3 UFs ou mais" = coeficiente parcial do grupo, calculado só com
    as seções de cada UF sobre os resíduos nacionais, com o mesmo sinal do nacional e |z| de 2 ou mais em 3 UFs ou
    mais. Poder por fórmula: menor deslocamento que daria z = 5 em cada grupo (5 erros) e o Phi correspondente, mais
    um plantio de conferência na data e na faixa de tamanho mediano.
A7. (g) Estimador de tau2 (par a par dentro do prédio): com r = resíduo do modelo base sem D, para cada local com
    pares de seções do mesmo flashcard e pares de flashcards diferentes, d = média de (r_i menos r_j)^2 / 2 nos pares
    de flashcards diferentes menos a mesma média nos pares de mesmo flashcard, cada média descontada da variância
    binomial média dos pares (v = 10^4 p (1 - p) / V da seção). O efeito de local some na diferença. tau2 = média de
    d entre locais, com peso gl_m x gl_e / (gl_m + gl_e), onde gl_m = soma de (seções do flashcard no local menos 1)
    e gl_e = flashcards do local menos 1. tau = raiz, com sinal de tau2. Sem o desconto binomial ao lado.
    Excesso = raiz com sinal de (tau2 de 2026 menos tau2 do placebo de 2022), nas mesmas seções (as de U com par em
    2022); 2018 ao lado. Bootstrap por município (9.999 reamostras, as mesmas para os dois anos).
    Assimetria = terceiro momento padronizado de t_f = média por flashcard do resíduo centrado no local vezes raiz
    do número de seções, nos flashcards com 5 seções ou mais em locais de 2 ou mais flashcards; "a favor de Lula" =
    assimetria positiva. Ao lado: flashcards com t_f padronizado acima de +3 e abaixo de -3.
    Calibração: troca binomial de R para L somando um quarto da margem (1.107.548 votos de margem, isto é, 553.774
    votos trocados) em fração q dos flashcards sorteados (0,1; 0,5; 0,8), 200 repetições por q; nulo com os rótulos
    de flashcard embaralhados dentro do local (200 vezes).
    Na amostra de logs: o mesmo estimador com o grupo = computador ou usuário da mídia de carga e da mídia de
    resultado do 2º turno (e da mídia de votação, ao lado), só com as seções da amostra; bootstrap por município.
    Mídia de carga da seção = último bloco "Mídia de carga gerada pelo computador / data / usuário" do pacote na urna
    do boletim do 2º turno (qualquer urna, se não houver). Mídia de resultado do 2º turno = último bloco de MR com
    "Aplicativo presente na MR [VOTA]" lido até 25/10/2026, com a mesma regra de urna.
A8. Poder de (a) a (e): em cada cópia, T ~ Binomial(R2, f) passa de R para L nas seções expostas de todo U (classe
    D = 1 em (a), (b), (c); todas menos o grupo em (d), (e)), f = Phi x 2.215.096 / soma de R2 nas expostas.
    pi(Phi) = fração das 200 cópias em que o incremento (b da cópia menos b observado) dividido pelo erro da cópia
    passa do z do critério (3,9 ou 3,3) no sentido plantado. Viés = média do incremento sobre o esperado (Phi na
    escala de A2; -1,785 x Phi em (d), (e)) menos 1. SEM PODER se pi(0,25) < 95% (é dito o menor Phi plantado com
    pi de 95%). Espelho: o mesmo plantio de L para R com Phi = 0,25. Falso sinal: 200 embaralhamentos de D dentro do
    município (na amostra do contraste), contando quantos cumprem as condições numéricas de SINAL (Phi e z).
    Explicação inocente plantada (30 cópias cada, com X e pesos refeitos): (i) abstenção pura uniforme: 3,6% dos
    votos de Flávio de toda seção de U viram abstenção (binomial), sem relação com o atributo; o teste não pode
    acusar. (ii) abstenção pura localizada: nas seções expostas, Binomial(R2, 2f) de Flávio vira abstenção, com o f
    de Phi = 0,25 (mesmo efeito na margem que a troca); mede se o teste vê e se y distingue troca de comparecimento.
A9. Acréscimo fora do registro, decidido antes de calcular e lido como EXPLORATÓRIO (não entra no veredito): como o
    modelo base controla a variação da abstenção, ele é cego para irregularidade que passe pelo comparecimento
    (o indício da Onda A). Para cada contraste de (a) a (e) e para (g) saem também: y sem o controle da variação da
    abstenção, e y_T = 100 x (comparecimento do 2º menos o do 1º) / aptos do 2º turno, com X sem a variação da
    abstenção e peso aptos.

Parte 2 (equipe vermelha)
E1. Resíduo r: uma regressão ponderada (peso V) por UF, y contra constante e o mesmo X do modelo base, sem efeito
    fixo de local, em U com perfil.
E2. Estatística de um agrupamento: T = soma_g W_g (m_g menos m_e)^2 / soma W, com m_g a média ponderada de r no
    grupo, W_g a soma dos pesos e m_e a média do estrato. Referência: 1.999 permutações dos rótulos entre células
    dentro do estrato (cada célula fica inteira e recebe o rótulo de outra célula do mesmo estrato). Razão = T sobre
    a média das permutações; p = (1 + permutações com T maior ou igual) / 2.000.
    Agrupamentos no bweb: (i) data de carga: grupo = UF x dia da carga, célula = zona x dia, estrato = UF (são
    "agrupamentos aleatórios de zonas do mesmo tamanho" em número de células); principal. (ii) data modal da zona:
    grupo = UF x dia modal da carga da zona, célula = zona, estrato = UF; ao lado. (iii) flashcard: grupo =
    flashcard, célula = local x flashcard, estrato = zona (o flashcard fica dentro da zona, então não existe
    permutação "entre zonas" para ele; a referência passa a ser agrupamentos aleatórios de locais da mesma zona).
    Nenhum flashcard tem 500 seções (máximo 125): pela letra o flashcard não pode dar SINAL nesta parte. (iv) código
    de carga (CD_CARGA_1): é único por urna (499.180 valores para 499.205 seções), não forma grupo; não testável.
    Na amostra de logs: grupo = computador da mídia de resultado do 2º turno, computador da mídia de carga, e UF x
    dia de geração de cada uma; célula = zona x grupo; estrato = UF.
E3. Grupo que cumpre a segunda condição: 500 seções ou mais na conta, média de r de +1,0 ou mais e média / erro
    acima de 4, com erro agrupado por zona (por local, se o grupo tiver uma zona só; marcado). SEM SINAL: p acima de
    0,05 e nenhum grupo de 500 seções ou mais com média acima de +0,5. Espelho: os mesmos contadores para -1,0 e
    -0,5 (a favor de Flávio). Onde não deveria dar nada: a mesma estatística com o resíduo de 2022 (modelo por UF
    com os controles de 2022) e os grupos de 2026.
E4. Calibração (100 cópias cada, 1.999 permutações): troca de R para L somando um quarto da margem concentrada em
    grupos UF x data sorteados até somarem 10% e 50% dos votos; e um grupo sorteado de 500 seções ou mais com +2,0
    pontos. Mede a fração de cópias com razão de 2 ou mais, p < 0,001 e grupo que cumpre E3. SEM PODER se a
    concentração em 10% dos votos não for vista em 95% das cópias.

Parte 3 (D3-4)
T1. Universo de (a): as 499.205 seções do 2º turno (exterior incluído). Horários = carimbo completo até o segundo de
    DT_ENCERRAMENTO e DT_EMISSAO_BU. As 27 seções de junta (sem encerramento) ficam fora de C_exato. Permutação: o
    par (encerramento, emissão) é embaralhado inteiro entre seções da mesma UF. "50 votos ou mais" = comparecimento
    de 50 ou mais. Reamostragem: comparecimento fixo e multinomial com as proporções da própria seção (2º turno: L,
    R, brancos, nulos; 1º turno: L, R, outros, brancos, nulos; vetor comparado: comparecimento, L, R, brancos,
    nulos). Placebos de rho: 2º turno de 2022 e 1º turno de 2026 (os do registro); 1º turno de 2022 e os dois turnos
    de 2018 e 2014 ao lado. Excesso = C_votos de 2026 menos o maior rho dos placebos do registro vezes a média
    reamostrada de 2026; ao lado, C_votos menos a média.
T2. (b): uma linha por seção do 2º turno (exterior incluído) com 30 válidos ou mais nos dois turnos (válidos do 1º
    turno = comparecimento menos brancos e nulos). y em pontos = 100 x L2 / (L2 + R2). Controles: frações do 13, do
    22, do 70, do 14 e do 55 (os outros com 1% ou mais), de brancos e de nulos sobre o comparecimento do 1º turno,
    (comparecimento do 2º menos o do 1º) / aptos do 2º, ln dos aptos e fração de 60 anos ou mais. Principal: com a
    idade, nas seções com perfil; ao lado: sem a idade, com o exterior. p pela normal. Margem implicada = 2 x beta /
    100 x válidos das seções tratadas. "Significativo" na cláusula de inconclusivo = p < 0,001. Veredito de (b):
    SINAL pela letra; INCONCLUSIVO se p < 0,001 com |beta| abaixo de 1 ou se o placebo passar de 0,3 em módulo; SEM
    SINAL se o intervalo de 95% couber em -1 a +1 e não for nenhum dos casos anteriores. Placebo: 100 x L1/(L1+R1)
    do 1º turno de 2026 contra a fração de 2022 do 2º turno, efeito fixo de local, peso L1 + R1.
T3. Poder de (a): 20 repetições copiando o vetor completo de 5 seções sorteadas para outras 5; 20 repetições copiando
    os votos de 3.000 seções com comparecimento de 200 ou mais para outras 3.000 de mesmo comparecimento. De (b):
    200 cópias movendo Binomial(V, 0,018), limitado a R2, de R para L nas seções tratadas.

TRADUÇÃO EM VOTOS: em toda parte, Phi x 4.430.191 = votos de margem que o contraste explicaria se fosse inteiro
efeito de irregularidade; o limite do intervalo de 99% dá o teto.
"""
import os as _os, sys as _sys
_sys.path.insert(0, _os.path.dirname(_os.path.abspath(__file__)))
import collections, csv, glob, gzip, io, json, math, re, sys, time, zipfile
import numpy as np

REPO = _os.path.dirname(_os.path.dirname(_os.path.abspath(__file__)))
DADOS = REPO + '/dados'
TRAB = '/home/user/trabalho-eleicao/adendo27/R27_B1'
D1DIR = '/home/user/trabalho-eleicao/adendo27/desenho_D1'
D3DIR = '/home/user/trabalho-eleicao/adendo27/desenho_D3'
PERFIL_A6 = '/home/user/trabalho-eleicao/adendo27/R27_A6/perfil_secao_2026_A6.json.gz'
ZIPS2T = '/home/user/trabalho-eleicao/trab2t/zips2t'
AMOSTRA = '/home/user/trabalho-eleicao/amostra2t/arq'
SAIDA_JSON = REPO + '/resultados/R27_B1_carga_lote_zona.json'
SAIDA_TXT = REPO + '/resultados/R27_B1_carga_lote_zona.txt'
MARGEM = 4430191
TROCA_VIRA = 2215096          # votos trocados que zeram a margem (Phi = 1)
SEMENTE = 20261110
UFS = ['AC', 'AL', 'AM', 'AP', 'BA', 'CE', 'DF', 'ES', 'GO', 'MA', 'MG', 'MS', 'MT', 'PA', 'PB', 'PE', 'PI', 'PR', 'RJ',
       'RN', 'RO', 'RR', 'RS', 'SC', 'SE', 'SP', 'TO']
REGIOES = {'Norte': ['AC', 'AM', 'AP', 'PA', 'RO', 'RR', 'TO'], 'Nordeste': ['AL', 'BA', 'CE', 'MA', 'PB', 'PE', 'PI', 'RN', 'SE'],
           'Sudeste': ['ES', 'MG', 'RJ', 'SP'], 'Sul': ['PR', 'RS', 'SC'], 'Centro-Oeste': ['DF', 'GO', 'MS', 'MT']}
UFS_GOV = ['AC', 'AM', 'DF', 'ES', 'RN', 'TO']
MODS = ['UE2013', 'UE2015', 'UE2020', 'UE2022']
Z99, Z95 = 2.5758, 1.96


def agora():
    return time.strftime('%H:%M:%S', time.gmtime())


def diz(*a):
    print(agora(), *a, flush=True)


def grava(nome, obj):
    """Grava um parcial em TRAB (escrita atômica)."""
    tmp = f'{TRAB}/{nome}.tmp'
    with open(tmp, 'w') as f:
        json.dump(obj, f, ensure_ascii=False, indent=1, default=_json_padrao)
    _os.replace(tmp, f'{TRAB}/{nome}')


def _json_padrao(o):
    if isinstance(o, (np.integer,)):
        return int(o)
    if isinstance(o, (np.floating,)):
        return float(o)
    if isinstance(o, np.ndarray):
        return o.tolist()
    if isinstance(o, (np.bool_,)):
        return bool(o)
    return str(o)


def pnorm2(z):
    """p bilateral pela normal."""
    return math.erfc(abs(z) / math.sqrt(2))


# ============================================================================================ extrações
PAT_LOG = re.compile(r'gerada pelo (computador|usuário)|Data e hora da geração|Número de série da MR|presentes? na MR|transitada para|Código de carga')


def _blocos_log(p):
    z = zipfile.ZipFile(p)
    for n in z.namelist():
        if n.startswith('logd'):
            yield z.read(n).decode('latin1').splitlines()
        elif n.endswith('.jez'):
            try:
                zz = zipfile.ZipFile(io.BytesIO(z.read(n)))
                for m in zz.namelist():
                    if m.startswith('logd'):
                        yield zz.read(m).decode('latin1').splitlines()
            except Exception:
                pass


def _um_log(p):
    partes = p.split('/')
    chave = f"{partes[-5].upper()}|{int(partes[-4])}|{int(partes[-3])}|{int(partes[-2])}"
    ev = []
    try:
        for bi, linhas in enumerate(_blocos_log(p)):
            for l in linhas:
                q = l.split('\t')
                if len(q) >= 5 and PAT_LOG.search(q[4]):
                    ev.append([bi, q[0], q[2], q[3], q[4][:200]])
    except Exception as e:
        return chave, {'erro': str(e)}
    return chave, {'ev': ev}


def modo_logs():
    """Estrutura do log (sem votos): linhas que nomeiam computador, usuário e data das mídias."""
    from multiprocessing import Pool
    arqs = sorted(_os.path.join(r, f) for r, _, fs in _os.walk(AMOSTRA) for f in fs if f.endswith('-log.jez'))
    out = {}
    with Pool(3) as pool:
        for k, v in pool.imap_unordered(_um_log, arqs, chunksize=20):
            if k in out and 'ev' in out[k] and 'ev' in v:
                out[k]['ev'] += v['ev']
            else:
                out[k] = v
    with gzip.open(TRAB + '/logs_midia.json.gz', 'wt') as f:
        json.dump(out, f, separators=(',', ':'), ensure_ascii=False)
    diz('logs: secoes', len(out), 'com erro', sum('erro' in v for v in out.values()))


def midias_da_secao(ev, urna2):
    """Regra A7: mídia de carga, de votação e de resultado do 2º turno da seção, a partir das linhas do log."""
    alvo = f'{int(urna2):08d}' if urna2 else None

    def dia(ts):
        return (int(ts[6:10]), int(ts[3:5]), int(ts[0:2]))
    carga, vot, mr = [], [], []
    cur = None; cur_mr = None
    for bi, ts, ser, ap, msg in ev:
        if msg.startswith('Mídia de carga gerada pelo computador'):
            cur = {'tipo': 'c', 'comp': msg.split(': ', 1)[1].split(' - ')[0].strip(), 'ser': ser, 'ts': ts}
        elif msg.startswith('Mídia de votação gerada pelo computador'):
            cur = {'tipo': 'v', 'comp': msg.split(': ', 1)[1].split(' - ')[0].strip(), 'ser': ser, 'ts': ts}
        elif msg.startswith('Data e hora da geração da mídia de') and cur is not None:
            cur['data'] = msg.split(': ', 1)[1].strip()
        elif msg.startswith('Mídia de carga gerada pelo usuário') and cur is not None and cur['tipo'] == 'c':
            cur['user'] = msg.split(': ', 1)[1].strip(); carga.append(cur); cur = None
        elif msg.startswith('Mídia de votação gerada pelo usuário') and cur is not None and cur['tipo'] == 'v':
            cur['user'] = msg.split(': ', 1)[1].strip(); vot.append(cur); cur = None
        elif msg.startswith('Número de série da MR'):
            cur_mr = {'ser': ser, 'ts': ts, 'app': None}
        elif 'na MR [' in msg and cur_mr is not None:
            cur_mr['app'] = msg[msg.index('[') + 1:msg.rindex(']')]
        elif msg.startswith('MR gerada pelo computador') and cur_mr is not None:
            cur_mr['comp'] = msg.split(': ', 1)[1].strip()
        elif msg.startswith('Data e hora da geração da MR') and cur_mr is not None:
            cur_mr['data'] = msg.split(': ', 1)[1].strip()
        elif msg.startswith('MR gerada pelo usuário') and cur_mr is not None:
            cur_mr['user'] = msg.split(': ', 1)[1].strip(); mr.append(cur_mr); cur_mr = None

    def ultimo(lst, filtro=lambda x: True):
        a = [x for x in lst if filtro(x) and x['ser'] == alvo]
        if a:
            return a[-1], 'urna do boletim'
        b = [x for x in lst if filtro(x)]
        return (b[-1], 'qualquer urna do pacote') if b else (None, 'ausente')
    c, rc = ultimo(carga)
    v, rv = ultimo(vot, lambda x: dia(x['ts']) <= (2026, 10, 25))
    m, rm = ultimo(mr, lambda x: x.get('app') == 'VOTA' and 'comp' in x and dia(x['ts']) <= (2026, 10, 25))
    out = {}
    for nome, o, r in (('c', c, rc), ('v', v, rv), ('m', m, rm)):
        out[nome + '_regra'] = r
        out[nome + '_comp'] = o.get('comp') if o else None
        out[nome + '_user'] = o.get('user') if o else None
        d = o.get('data') if o else None
        out[nome + '_dia'] = (d[6:10] + '-' + d[3:5] + '-' + d[0:2]) if d else None
    return out


def modo_gov():
    """Governador do 2º turno (cargo 3) por seção nas 6 UFs, direto do bweb do 2º turno."""
    out = {}
    for uf in UFS_GOV:
        zp = glob.glob(f'{ZIPS2T}/bweb_2t_{uf}_*.zip')[0]
        z = zipfile.ZipFile(zp)
        nome = [n for n in z.namelist() if n.lower().endswith('.csv')][0]
        with z.open(nome) as fh:
            rd = csv.reader(io.TextIOWrapper(fh, encoding='latin1', newline=''), delimiter=';')
            cab = next(rd); ix = {c.strip().replace('SG_ UF', 'SG_UF'): i for i, c in enumerate(cab)}
            for r in rd:
                if r[ix['CD_CARGO_PERGUNTA']] != '3':
                    continue
                k = f"{r[ix['SG_UF']]}|{int(r[ix['CD_MUNICIPIO']])}|{int(r[ix['NR_ZONA']])}|{int(r[ix['NR_SECAO']])}"
                d = out.setdefault(k, {})
                t = r[ix['DS_TIPO_VOTAVEL']]
                nm = r[ix['NR_VOTAVEL']] if t == 'Nominal' else ('B' if t == 'Branco' else 'N')
                d[nm] = d.get(nm, 0) + int(r[ix['QT_VOTOS']])
        diz('gov', uf, len(out))
    with gzip.open(TRAB + '/gov2t_6ufs_B1.json.gz', 'wt') as f:
        json.dump(out, f, separators=(',', ':'))


# ============================================================================================ base
def _carrega(caminho):
    with gzip.open(caminho, 'rt') as f:
        return json.load(f)


def modo_base():
    from modelos import modelo
    diz('lendo dados')
    S = _carrega(DADOS + '/secoes2026.json.gz')
    CAND = _carrega(DADOS + '/candidatos2026_1t.json.gz')
    E2 = _carrega(D1DIR + '/estrutura_2t.json.gz')
    E1 = _carrega(D1DIR + '/estrutura_1t.json.gz')
    GR = _carrega(D3DIR + '/grupos_2t.json.gz')
    PF = _carrega(PERFIL_A6)
    cols_pf = PF['colunas']; PF = PF['secoes']
    meta = {}
    # candidatos com 0,5% ou mais do comparecimento nacional do 1º turno
    comp1_nac = sum(v['1']['comp'] for v in S.values() if '1' in v)
    tot = CAND['totais']
    meta['comparecimento_1t_nacional'] = comp1_nac
    meta['fracao_nacional_1t'] = {n: tot[n] / comp1_nac for n in tot}
    outros05 = sorted([n for n in tot if n not in ('13', '22') and tot[n] / comp1_nac >= 0.005], key=lambda n: -tot[n])
    outros1 = sorted([n for n in tot if n not in ('13', '22') and tot[n] / comp1_nac >= 0.01], key=lambda n: -tot[n])
    meta['outros_0_5'] = outros05; meta['outros_1'] = outros1
    diz('outros com 0,5%:', outros05, 'com 1%:', outros1)

    # ---------------- universo U
    chaves = []
    cont = collections.Counter()
    for k in sorted(E2):
        v = S.get(k)
        if v is None or '2' not in v:
            cont['sem_2t_na_base'] += 1; continue
        if k.startswith('ZZ'):
            cont['exterior'] += 1; continue
        if E2[k][16] != '-1':
            cont['junta'] += 1; continue
        if '1' not in v:
            cont['sem_par_1t'] += 1; continue
        if v['2']['L'] + v['2']['R'] < 30:
            cont['LR2_abaixo_de_30'] += 1; continue
        chaves.append(k)
    n = len(chaves); cont['U'] = n
    meta['contagem_universo'] = dict(cont)
    diz('U', n, dict(cont))
    ix = {k: i for i, k in enumerate(chaves)}

    def ids(lst):
        u, inv = np.unique(np.array(lst), return_inverse=True)
        return u, inv.astype(np.int32)
    part = [k.split('|') for k in chaves]
    uf_i = np.array([UFS.index(p[0]) for p in part], np.int16)
    _, mun_id = ids([p[0] + '|' + p[1] for p in part])
    _, zm_id = ids([p[0] + '|' + p[1] + '|' + p[2] for p in part])
    _, zona_id = ids([p[0] + '|' + p[2] for p in part])
    loc_lab = [p[0] + '|' + p[1] + '|' + p[2] + '|' + str(S[k]['2']['loc']) for p, k in zip(part, chaves)]
    _, loc_id = ids(loc_lab)
    A = {}
    for t in ('1', '2'):
        for c in ('L', 'R', 'O', 'B', 'N', 'comp', 'apt'):
            A[c + t] = np.array([S[k][t][c] for k in chaves], np.int32)
    for nc in outros05:
        A['c' + nc] = np.array([CAND['secoes'].get(k, {}).get(nc, 0) for k in chaves], np.int32)
    A['urna1'] = np.array([int(E1[k][3]) for k in chaves], np.int64)
    A['urna2'] = np.array([int(E2[k][3]) for k in chaves], np.int64)
    A['mod2'] = np.array([MODS.index(m) if (m := modelo(int(E2[k][3]), 2026)) in MODS else -1 for k in chaves], np.int8)
    A['mod1'] = np.array([MODS.index(m) if (m := modelo(int(E1[k][3]), 2026)) in MODS else -1 for k in chaves], np.int8)
    fc_u, A['fc'] = ids([E2[k][6] for k in chaves])
    dia_u, A['dia'] = ids([E2[k][7][:10] for k in chaves])
    A['carga_pos'] = np.array([GR[k]['carga_pos'] for k in chaves], np.int8)
    A['urna_dif'] = np.array([GR[k]['urna_dif'] for k in chaves], np.int8)
    A['biomsh2'] = np.array([int(E2[k][12]) for k in chaves], np.int32)
    A['secao'] = np.array([int(p[3]) for p in part], np.int32)
    # posição no local (entre todas as seções do 2º turno do local)
    porloc = collections.defaultdict(list)
    for k, v in S.items():
        if '2' in v:
            p = k.split('|'); porloc[p[0] + '|' + p[1] + '|' + p[2] + '|' + str(v['2']['loc'])].append(int(p[3]))
    for l in porloc.values():
        l.sort()
    pos = np.zeros(n)
    for i, (k, ll) in enumerate(zip(chaves, loc_lab)):
        l = porloc[ll]
        if len(l) > 1:
            pos[i] = l.index(int(part[i][3])) / (len(l) - 1)
    A['pos'] = pos
    # perfil (soma com agregadas)
    perf = np.full((n, len(cols_pf)), np.nan)
    sem = 0
    for i, k in enumerate(chaves):
        p = part[i]; base = PF.get(k)
        if base is None:
            sem += 1; continue
        v = np.array(base, float)
        ag = E2[k][15]
        if ag not in ('#NULO#', ''):
            for s in ag.split('/'):
                s = s.strip()
                if s.isdigit():
                    o = PF.get(f'{p[0]}|{p[1]}|{p[2]}|{int(s)}')
                    if o is not None:
                        v = v + np.array(o, float)
        perf[i] = v
    meta['sem_perfil'] = sem
    A['perfil'] = perf.astype(np.float32)
    meta['colunas_perfil'] = cols_pf

    # 2022 e 2018 pela chave
    for ano in (2022, 2018):
        Sx = _carrega(f'{DADOS}/secoes{ano}.json.gz')
        tem = np.zeros(n, bool)
        arr = {c + t: np.zeros(n, np.int32) for t in ('1', '2') for c in ('L', 'R', 'O', 'B', 'N', 'comp', 'apt')}
        loc = []; urna = np.zeros(n, np.int64)
        for i, k in enumerate(chaves):
            v = Sx.get(k)
            if v is None or '1' not in v or '2' not in v:
                loc.append(''); continue
            tem[i] = True
            for t in ('1', '2'):
                for c in ('L', 'R', 'O', 'B', 'N', 'comp', 'apt'):
                    arr[c + t][i] = v[t].get(c) or 0
            p = part[i]; loc.append(p[0] + '|' + p[1] + '|' + p[2] + '|' + str(v['2'].get('loc')))
            try:
                urna[i] = int(v['2'].get('urna') or 0)
            except (TypeError, ValueError):
                urna[i] = 0
        s = str(ano)[2:]
        A['tem' + s] = tem
        for c, a in arr.items():
            A[c + '_' + s] = a
        _, A['loc_' + s] = ids(loc)
        A['urna_' + s] = urna
        meta[f'pareadas_{ano}'] = int(tem.sum())
        if ano == 2022:
            A['mod_22'] = np.array([(['UE2009', 'UE2010', 'UE2011', 'UE2013', 'UE2015', 'UE2020'].index(m)
                                     if (m := modelo(int(u), 2022)) else -1) if u else -1 for u in urna], np.int8)
        del Sx
    # governador
    G2 = _carrega(TRAB + '/gov2t_6ufs_B1.json.gz')
    G1 = _carrega(DADOS + '/candidatos_gov_2026_1t_6ufs.json.gz')
    gov = {}
    for uf in UFS_GOV:
        ks = [k for k in chaves if k.startswith(uf + '|')]
        tot2 = collections.Counter()
        for k in ks:
            for c, q in G2.get(k, {}).items():
                if c not in ('B', 'N'):
                    tot2[c] += q
        fin = [c for c, _ in tot2.most_common(2)]
        tot1 = collections.Counter(); comp1 = 0
        for k in ks:
            for c, q in G1['secoes'].get(k, {}).items():
                tot1[c] += q
            comp1 += S[k].get('1g', {}).get('comp', 0)
        c1 = [c for c, q in tot1.most_common() if comp1 and q / comp1 >= 0.005]
        gov[uf] = {'finalistas': fin, 'cand_1t': c1, 'total_2t': dict(tot2)}
    meta['gov'] = gov
    ga = np.zeros(n, np.int32); gb = np.zeros(n, np.int32); gtem = np.zeros(n, bool)
    g1 = np.zeros((n, 12), np.float32); g1b = np.zeros(n, np.float32); g1n = np.zeros(n, np.float32)
    for i, k in enumerate(chaves):
        uf = part[i][0]
        if uf not in gov:
            continue
        d2 = G2.get(k); d1 = G1['secoes'].get(k); s1g = S[k].get('1g')
        if d2 is None or d1 is None or s1g is None or not s1g.get('comp'):
            continue
        gtem[i] = True
        ga[i] = d2.get(gov[uf]['finalistas'][0], 0); gb[i] = d2.get(gov[uf]['finalistas'][1], 0)
        for j, c in enumerate(gov[uf]['cand_1t'][:12]):
            g1[i, j] = d1.get(c, 0) / s1g['comp']
        g1b[i] = s1g.get('B', 0) / s1g['comp']; g1n[i] = s1g.get('N', 0) / s1g['comp']
    A['gov_a'] = ga; A['gov_b'] = gb; A['gov_tem'] = gtem; A['gov_f1'] = g1; A['gov_b1'] = g1b; A['gov_n1'] = g1n
    # amostra de logs
    LG = _carrega(TRAB + '/logs_midia.json.gz')
    rot = {c: [''] * n for c in ('c_comp', 'c_user', 'c_dia', 'm_comp', 'm_user', 'm_dia', 'v_comp', 'v_user', 'v_dia')}
    nolog = np.zeros(n, bool); regras = collections.Counter()
    for k, v in LG.items():
        i = ix.get(k)
        if i is None or 'ev' not in v:
            continue
        m = midias_da_secao(v['ev'], int(E2[k][3]))
        nolog[i] = True
        for c in rot:
            rot[c][i] = m[c] or ''
        regras[('carga', m['c_regra'])] += 1; regras[('mr', m['m_regra'])] += 1; regras[('votacao', m['v_regra'])] += 1
    A['nolog'] = nolog
    meta['logs_regras'] = {f'{a}: {b}': q for (a, b), q in regras.items()}
    meta['logs_em_U'] = int(nolog.sum()); meta['logs_total'] = len(LG)
    rotulos = {}
    for c, l in rot.items():
        u, inv = ids(l); A['log_' + c] = inv; rotulos['log_' + c] = u.tolist()
    np.savez_compressed(TRAB + '/base_B1.npz', uf_i=uf_i, mun_id=mun_id, zm_id=zm_id, zona_id=zona_id, loc_id=loc_id, **A)
    rotulos.update({'fc': fc_u.tolist(), 'dia': dia_u.tolist()})
    with gzip.open(TRAB + '/base_B1_rotulos.json.gz', 'wt') as f:
        json.dump({'chaves': chaves, 'rotulos': rotulos, 'meta': meta}, f, separators=(',', ':'), ensure_ascii=False)
    diz('base gravada', n)

    # ---------------- base do D3-4 (todas as seções, exterior incluído)
    M2 = _carrega(D3DIR + '/meta2t.json.gz'); M1 = _carrega(D3DIR + '/meta1t.json.gz')

    def seg(s):
        if s in ('#NULO#', '', None):
            return -1
        return ((int(s[8:10]) * 24 + int(s[11:13])) * 60 + int(s[14:16])) * 60 + int(s[17:19])
    B = {}
    for t, M in (('2', M2), ('1', M1)):
        ks = sorted(k for k in M if k in S and t in S[k])
        B['uf' + t] = np.array([(UFS + ['ZZ']).index(k.split('|')[0]) for k in ks], np.int16)
        for c in ('L', 'R', 'O', 'B', 'N', 'comp', 'apt'):
            B[c + t] = np.array([S[k][t][c] for k in ks], np.int32)
        B['biom' + t] = np.array([int(M[k]['biom_sh']) for k in ks], np.int32)
        B['enc' + t] = np.array([seg(M[k]['enc']) for k in ks], np.int64)
        B['emi' + t] = np.array([seg(M[k]['emi']) for k in ks], np.int64)
        B['junta' + t] = np.array([M[k]['junta'] != '-1' for k in ks], bool)
        meta[f'd34_n_{t}t'] = len(ks)
        cu = collections.Counter(M[k]['urna'] for k in ks); cc = collections.Counter(M[k]['carga'] for k in ks)
        ru = {u: q for u, q in cu.items() if q > 1}; rc = {u: q for u, q in cc.items() if q > 1}
        meta[f'd34_urnas_repetidas_{t}t'] = ru; meta[f'd34_cargas_repetidas_{t}t'] = rc
        meta[f'd34_urnas_repetidas_fora_de_junta_{t}t'] = sorted(k for k in ks if cu[M[k]['urna']] > 1 and M[k]['junta'] == '-1')
        meta[f'd34_cargas_repetidas_fora_de_junta_{t}t'] = sorted(k for k in ks if cc[M[k]['carga']] > 1 and M[k]['junta'] == '-1')
        meta[f'd34_secoes_de_junta_{t}t'] = int(sum(M[k]['junta'] != '-1' for k in ks))
        meta[f'd34_secoes_em_urna_repetida_{t}t'] = int(sum(cu[M[k]['urna']] > 1 for k in ks))
        if t == '2':
            ks2 = ks
    # linhas de (b): seções do 2º turno com par no 1º
    kb = [k for k in ks2 if '1' in S[k]]
    Bb = {}
    for t in ('1', '2'):
        for c in ('L', 'R', 'O', 'B', 'N', 'comp', 'apt'):
            Bb['b_' + c + t] = np.array([S[k][t][c] for k in kb], np.int32)
    for nc in outros1:
        Bb['b_c' + nc] = np.array([CAND['secoes'].get(k, {}).get(nc, 0) for k in kb], np.int32)
    Bb['b_urna_dif'] = np.array([GR[k]['urna_dif'] for k in kb], np.int8)
    Bb['b_carga_pos'] = np.array([GR[k]['carga_pos'] for k in kb], np.int8)
    pb = [k.split('|') for k in kb]
    _, Bb['b_loc'] = ids([p[0] + '|' + p[1] + '|' + p[2] + '|' + str(S[k]['2']['loc']) for p, k in zip(pb, kb)])
    _, Bb['b_mun'] = ids([p[0] + '|' + p[1] for p in pb])
    i60 = [cols_pf.index(c) for c in ('i6069', 'i7079', 'i80m')]; itot = cols_pf.index('total')
    f60 = np.full(len(kb), np.nan)
    for i, k in enumerate(kb):
        base = PF.get(k)
        if base is None:
            continue
        v = np.array(base, float); p = pb[i]
        ag = M2[k]['agr']
        if ag not in ('#NULO#', ''):
            for s in ag.split('/'):
                s = s.strip()
                if s.isdigit():
                    o = PF.get(f'{p[0]}|{p[1]}|{p[2]}|{int(s)}')
                    if o is not None:
                        v = v + np.array(o, float)
        if v[itot] > 0:
            f60[i] = v[i60].sum() / v[itot]
    Bb['b_f60'] = f60
    S22 = _carrega(DADOS + '/secoes2022.json.gz')
    y22 = np.full(len(kb), np.nan)
    for i, k in enumerate(kb):
        v = S22.get(k)
        if v and '2' in v and (v['2']['L'] + v['2']['R']) >= 30:
            y22[i] = 100.0 * v['2']['L'] / (v['2']['L'] + v['2']['R'])
    Bb['b_y22'] = y22
    # vetores de votos dos outros anos, para rho
    for ano in (2022, 2018, 2014):
        Sx = S22 if ano == 2022 else _carrega(f'{DADOS}/secoes{ano}.json.gz')
        for t in ('1', '2'):
            ks = [k for k in Sx if t in Sx[k]]
            B[f'v{ano}_{t}'] = np.array([[Sx[k][t].get(c) or 0 for c in ('comp', 'L', 'R', 'O', 'B', 'N')] for k in ks], np.int32)
        del Sx
    np.savez_compressed(TRAB + '/base_d34.npz', **B, **Bb)
    with open(TRAB + '/base_meta.json', 'w') as f:
        json.dump(meta, f, ensure_ascii=False, indent=1, default=_json_padrao)
    diz('base d34 gravada')


# ============================================================================================ regressão
class Modelo:
    """MQO ponderado com efeito fixo (transformação within) e erro CR1 por agrupamento (decisão G3).

    Guarda o que não depende de y nem de D: X centrado no efeito fixo e a inversa de X'WX. Os coeficientes de D saem
    pelo teorema de Frisch, Waugh e Lovell (resíduo de y e de D em X dentro do efeito fixo), com o mesmo erro CR1 da
    regressão completa."""

    def __init__(self, X, w, fe, cl, idx):
        idx = np.asarray(idx)
        _, g = np.unique(fe[idx], return_inverse=True)
        ok = np.bincount(g)[g] >= 2
        self.idx = idx[ok]
        _, self.g = np.unique(fe[self.idx], return_inverse=True)
        self.w = w[self.idx].astype(float)
        self.sw = np.bincount(self.g, self.w)
        self.ng = len(self.sw)
        _, self.cl = np.unique(cl[self.idx], return_inverse=True)
        self.ncl = int(self.cl.max()) + 1
        self.n = len(self.idx)
        Xd = self._dm(np.asarray(X[self.idx], float))
        var = (self.w[:, None] * Xd ** 2).sum(0)
        self.keep = var > 1e-10 * self.w.sum()
        self.Xd = Xd[:, self.keep]
        XtX = (self.Xd * self.w[:, None]).T @ self.Xd
        self.XtXi = np.linalg.pinv(XtX, hermitian=True)
        self.k = int(np.linalg.matrix_rank(XtX, hermitian=True))

    def _dm(self, M):
        out = np.empty_like(M, dtype=float)
        for j in range(M.shape[1]):
            out[:, j] = M[:, j] - (np.bincount(self.g, self.w * M[:, j], minlength=self.ng) / self.sw)[self.g]
        return out

    def res(self, v):
        """Resíduo de v (já recortado em self.idx) contra X dentro do efeito fixo."""
        v = np.asarray(v, float)
        um = v.ndim == 1
        V = v[:, None] if um else v
        Vd = self._dm(V)
        R = Vd - self.Xd @ (self.XtXi @ (self.Xd.T @ (self.w[:, None] * Vd)))
        return R[:, 0] if um else R

    def fit_res(self, yr, Dr):
        Dm = Dr[:, None] if Dr.ndim == 1 else Dr
        A = (Dm * self.w[:, None]).T @ Dm
        Ai = np.linalg.inv(A)
        b = Ai @ (Dm.T @ (self.w * yr))
        e = yr - Dm @ b
        m = Dm.shape[1]
        S = np.column_stack([np.bincount(self.cl, self.w * Dm[:, j] * e, minlength=self.ncl) for j in range(m)])
        G, N, K = self.ncl, self.n, self.k + m
        c = G / (G - 1) * (N - 1) / (N - K)
        V = c * Ai @ (S.T @ S) @ Ai
        return b, np.sqrt(np.diag(V))

    def fit(self, y, D):
        """y e D na indexação da base inteira."""
        Dr = self.res(np.asarray(D, float)[self.idx])
        b, ep = self.fit_res(self.res(np.asarray(y, float)[self.idx]), Dr)
        return b, ep


def carrega_base():
    B = dict(np.load(TRAB + '/base_B1.npz'))
    with gzip.open(TRAB + '/base_B1_rotulos.json.gz', 'rt') as f:
        R = json.load(f)
    return B, R


def perfil_X(B, cols):
    P = B['perfil'].astype(float)
    tot = P[:, cols.index('total')]
    ok = np.isfinite(tot) & (tot > 0)
    f = P / np.where(ok, tot, 1)[:, None]
    usar = ['mulheres', 'i1617', 'i1824', 'i2534', 'i4559', 'i6069', 'i7079', 'i80m', 'e1', 'e2', 'e3', 'e4', 'e5', 'e7', 'e8',
            'biometria']
    M = np.column_stack([f[:, cols.index(c)] for c in usar])
    M[~ok] = 0
    return M, ok, usar


def spec(B, cols, nome, sub=None):
    """Desfecho, X, peso, linhas disponíveis e agrupamento do erro de cada especificação (A4, A5, A9).
    sub: dicionário com vetores substitutos (plantios que mudam X e peso)."""
    g = (lambda c: (sub[c] if sub and c in sub else B[c]).astype(float))
    PX, pok, _ = perfil_X(B, cols)
    L1, R1, B1, N1, C1, A1 = g('L1'), g('R1'), g('B1'), g('N1'), g('comp1'), g('apt1')
    L2, R2, B2, N2, C2, A2 = g('L2'), g('R2'), g('B2'), g('N2'), g('comp2'), g('apt2')
    V = L2 + R2
    ab1 = 1 - C1 / A1; ab2 = 1 - C2 / A2
    lnapt = np.log(A2); pos = B['pos']
    comp = [L1 / C1, R1 / C1] + [g('c' + c) / C1 for c in ('70', '14', '55')] + [B1 / C1, N1 / C1]
    cl = B['mun_id']
    if nome in ('y', 'yBN'):
        X = np.column_stack(comp + [ab1, ab2 - ab1, PX, lnapt, pos])
        y = 100 * L2 / V if nome == 'y' else 100 * (B2 + N2) / C2
        return dict(y=y, X=X, w=V, ok=pok, cl=cl)
    if nome == 'ysd':
        return dict(y=100 * L2 / V, X=np.column_stack(comp + [ab1, PX, lnapt, pos]), w=V, ok=pok, cl=cl)
    if nome == 'yT':
        return dict(y=100 * (C2 - C1) / A2, X=np.column_stack(comp + [ab1, PX, lnapt, pos]), w=A2, ok=pok, cl=cl)
    if nome in ('pl22', 'pl18', 'yalt', 'plturno', 'plBN22', 'plT22'):
        s = '_18' if nome == 'pl18' else '_22'
        h = lambda c: B[c + s].astype(float)
        tem = B['tem' + s[1:]] & (h('L2') + h('R2') >= 30) & (h('comp1') > 0) & (h('apt1') > 0) & (h('apt2') > 0) & (h('comp2') > 0)
        d = lambda a, b: a / np.where(b > 0, b, 1)
        c1, a1, c2, a2 = h('comp1'), h('apt1'), h('comp2'), h('apt2')
        compx = [d(h('L1'), c1), d(h('R1'), c1), d(h('B1'), c1), d(h('N1'), c1)]
        abx1 = 1 - d(c1, a1); abx2 = 1 - d(c2, a2)
        Vx = h('L2') + h('R2'); yx = 100 * d(h('L2'), Vx)
        if nome in ('pl22', 'pl18'):
            return dict(y=yx, X=np.column_stack(compx + [abx1, abx2 - abx1, PX, np.log(np.where(a2 > 0, a2, 1)), pos]),
                        w=Vx, ok=pok & tem, cl=cl)
        if nome == 'plT22':
            return dict(y=100 * (c2 - c1) / np.where(a2 > 0, a2, 1),
                        X=np.column_stack(compx + [abx1, PX, np.log(np.where(a2 > 0, a2, 1)), pos]), w=a2, ok=pok & tem, cl=cl)
        if nome == 'plBN22':
            return dict(y=100 * d(h('B2') + h('N2'), c2),
                        X=np.column_stack(compx + [abx1, abx2 - abx1, PX, np.log(np.where(a2 > 0, a2, 1)), pos]),
                        w=Vx, ok=pok & tem, cl=cl)
        if nome == 'yalt':
            return dict(y=100 * L2 / V - yx, X=np.column_stack(compx + [abx1, abx2 - abx1, ab2 - abx2, PX, lnapt, pos]),
                        w=V, ok=pok & tem, cl=cl)
        V1 = L1 + R1
        return dict(y=100 * L1 / np.where(V1 > 0, V1, 1),
                    X=np.column_stack([yx / 100] + compx + [abx1, ab1 - abx1, PX, np.log(A1), pos]),
                    w=V1, ok=pok & tem & (V1 >= 30), cl=cl)
    if nome == 'gov':
        ga, gb = B['gov_a'].astype(float), B['gov_b'].astype(float)
        Vg = ga + gb
        ok = pok & B['gov_tem'] & (Vg >= 30)
        yg = 100 * ga / np.where(Vg > 0, Vg, 1)
        y0 = 100 * L2 / V
        lado = {}
        blocos = []
        base = np.column_stack([B['gov_f1'].astype(float), B['gov_b1'], B['gov_n1'], ab1, ab2 - ab1, PX, lnapt, pos])
        for uf in UFS_GOV:
            m = ok & (B['uf_i'] == UFS.index(uf))
            if m.sum() == 0:
                continue
            ww = Vg[m]
            a = yg[m] - np.average(yg[m], weights=ww); b = y0[m] - np.average(y0[m], weights=ww)
            r = float((ww * a * b).sum() / math.sqrt((ww * a * a).sum() * (ww * b * b).sum()))
            lado[uf] = r
            if r < 0:
                yg[m] = 100 - yg[m]
            blocos.append(base * m[:, None])
        cl2 = cl.astype(np.int64).copy()
        df = B['uf_i'] == UFS.index('DF')
        cl2[df] = 10 ** 6 + B['zona_id'][df]
        return dict(y=yg, X=np.column_stack(blocos), w=Vg, ok=ok, cl=cl2, lado=lado)
    raise ValueError(nome)


def spec22_proprio(B, cols):
    """Placebo de ano: tudo de 2022 (desfecho, X, peso), para os contrastes com os modelos de urna de 2022."""
    return spec(B, cols, 'pl22')


def mistos(fe, m1, m0, base):
    """Linhas das classes m1 ou m0 em grupos (locais) que têm as duas classes, dentro de base."""
    ng = int(fe.max()) + 1
    t1 = np.bincount(fe[base & m1], minlength=ng) > 0
    t0 = np.bincount(fe[base & m0], minlength=ng) > 0
    return base & (m1 | m0) & (t1 & t0)[fe]


def n_var(mod, D):
    """Seções e grupos de efeito fixo em que D varia dentro do grupo (os que identificam b)."""
    d = np.asarray(D, float)[mod.idx]
    s = np.bincount(mod.g, d, minlength=mod.ng); c = np.bincount(mod.g, minlength=mod.ng)
    v = (s > 0) & (s < c)
    return int(v[mod.g].sum()), int(v.sum()), int((d[v[mod.g]] > 0).sum())


def regiao_de(uf_i):
    r = np.zeros(len(uf_i), np.int8)
    for j, (nm, ufs) in enumerate(REGIOES.items()):
        for u in ufs:
            r[uf_i == UFS.index(u)] = j
    return r


# ============================================================================================ PARTE 1 (D1.1)
def tau2_pares(r, v, loc, grp):
    """A7: por local, d = meia média dos quadrados das diferenças entre pares de grupos diferentes menos a dos pares
    do mesmo grupo, com e sem o desconto da variância binomial. Devolve (local, d, d_sem_desconto, peso)."""
    lu, l = np.unique(loc, return_inverse=True)
    nl = len(lu)
    K = int(grp.max()) + 2
    cu, c = np.unique(l.astype(np.int64) * K + grp, return_inverse=True)
    lc = (cu // K).astype(np.int64)
    n_c = np.bincount(c).astype(float); S_c = np.bincount(c, r); Q_c = np.bincount(c, r * r); v_c = np.bincount(c, v)
    n_l = np.bincount(l).astype(float); S_l = np.bincount(l, r); Q_l = np.bincount(l, r * r); v_l = np.bincount(l, v)
    C_l = np.bincount(lc, minlength=nl).astype(float)
    SS_s = np.bincount(lc, n_c * Q_c - S_c ** 2, minlength=nl)
    P_s = np.bincount(lc, n_c * (n_c - 1) / 2, minlength=nl)
    VB_s = np.bincount(lc, (n_c - 1) * v_c, minlength=nl)
    SS_a = n_l * Q_l - S_l ** 2; P_a = n_l * (n_l - 1) / 2; VB_a = (n_l - 1) * v_l
    SS_d = SS_a - SS_s; P_d = P_a - P_s; VB_d = VB_a - VB_s
    ok = (P_s > 0) & (P_d > 0)
    with np.errstate(divide='ignore', invalid='ignore'):
        d_raw = SS_d / (2 * P_d) - SS_s / (2 * P_s)
        d = d_raw - (VB_d / (2 * P_d) - VB_s / (2 * P_s))
        gm = n_l - C_l; ge = C_l - 1
        w = gm * ge / (gm + ge)
    return lu[ok], d[ok], d_raw[ok], w[ok], dict(locais=int(ok.sum()), pares_dif=float(P_d[ok].sum()), pares_iguais=float(P_s[ok].sum()),
                                                  secoes=int(n_l[ok].sum()))


def raiz_sinal(x):
    return np.sign(x) * np.sqrt(np.abs(x))


def assimetria_grupos(rt, loc, grp, minimo=5):
    """Assimetria das médias por grupo (t_f = média x raiz de n) nas seções de locais com 2 ou mais grupos."""
    nl = int(loc.max()) + 1
    K = int(grp.max()) + 2
    cu = np.unique(loc.astype(np.int64) * K + grp)
    ngl = np.bincount((cu // K).astype(np.int64), minlength=nl)
    m = ngl[loc] >= 2
    gu, gi = np.unique(grp[m], return_inverse=True)
    n = np.bincount(gi).astype(float); s = np.bincount(gi, rt[m])
    k = n >= minimo
    if k.sum() < 10:
        return dict(n_grupos=int(k.sum()), assimetria=None)
    t = s[k] / np.sqrt(n[k])
    z = (t - t.mean()) / t.std()
    return dict(n_grupos=int(k.sum()), assimetria=float((z ** 3).mean()), acima_de_3=int((z > 3).sum()), abaixo_de_menos_3=int((z < -3).sum()),
                acima_de_4=int((z > 4).sum()), abaixo_de_menos_4=int((z < -4).sum()), dp_t=float(t.std()))


def boot_contagens(rng, M, reps):
    return rng.multinomial(M, np.full(M, 1.0 / M), size=reps).astype(np.float32)


def por_municipio(locs, vals, w, mun_do_local, M):
    m = mun_do_local[locs]
    return np.bincount(m, w * vals, minlength=M), np.bincount(m, w, minlength=M)


def modo_d11():
    t0 = time.time()
    B, R = carrega_base()
    meta = R['meta']; cols = meta['colunas_perfil']
    n = len(B['uf_i'])
    rng = np.random.default_rng(SEMENTE)
    L2, R2 = B['L2'].astype(float), B['R2'].astype(float)
    V = L2 + R2
    comp2 = B['comp2'].astype(float); apt2 = B['apt2'].astype(float)
    mod2 = B['mod2']; loc = B['loc_id']; zm = B['zm_id']; mun = B['mun_id']; uf_i = B['uf_i']
    reg = regiao_de(uf_i)
    tudo = np.ones(n, bool)
    res = {'meta': {'U': n, 'sem_perfil': meta['sem_perfil'], 'modelos_em_U': {MODS[j]: int((mod2 == j).sum()) for j in range(4)},
                    'modelo_desconhecido': int((mod2 < 0).sum()), 'V_total_U': float(V.sum()),
                    'carga_pos_em_U': int(B['carga_pos'].sum()), 'urna_dif_em_U': int(B['urna_dif'].sum())}}
    nova = mod2 >= 2
    CONTR = {
        'a': dict(nome='UE2022 contra UE2020, locais mistos', D=(mod2 == 3), amostra=mistos(loc, mod2 == 3, mod2 == 2, tudo), fe=loc,
                  c1=(mod2 == 3), c0=(mod2 == 2), zc=3.9, tipo='fatia'),
        'b': dict(nome='UE2015 contra UE2013, locais mistos', D=(mod2 == 1), amostra=mistos(loc, mod2 == 1, mod2 == 0, tudo), fe=loc,
                  c1=(mod2 == 1), c0=(mod2 == 0), zc=3.9, tipo='fatia'),
        'c': dict(nome='família nova contra antiga, efeito fixo de zona e município', D=nova, amostra=(mod2 >= 0), fe=zm,
                  c1=nova, c0=(mod2 >= 0) & ~nova, zc=3.9, tipo='fatia'),
        'c_local': dict(nome='família nova contra antiga, efeito fixo de local (conferência)', D=nova, amostra=(mod2 >= 0), fe=loc,
                        c1=nova, c0=(mod2 >= 0) & ~nova, zc=3.9, tipo='fatia'),
        'd': dict(nome='carga depois de 04/10 contra carga de setembro no mesmo local', D=(B['carga_pos'] == 1), amostra=tudo, fe=loc,
                  c1=(B['carga_pos'] == 1), c0=(B['carga_pos'] == 0), zc=3.3, tipo='controle'),
        'e': dict(nome='urna diferente da do 1º turno contra mesma urna', D=(B['urna_dif'] == 1), amostra=tudo, fe=loc,
                  c1=(B['urna_dif'] == 1), c0=(B['urna_dif'] == 0), zc=3.3, tipo='controle'),
    }
    for c in CONTR.values():
        c['V1'] = float(V[c['c1']].sum()); c['V0'] = float(V[c['c0']].sum())
        c['C1'] = float(comp2[c['c1']].sum()); c['A1'] = float(apt2[c['c1']].sum())

    def phis(nome, b, ep):
        c = CONTR[nome]
        if c['tipo'] == 'fatia':
            p1 = 2 * b * c['V1'] / 100 / MARGEM; p0 = 2 * (-b) * c['V0'] / 100 / MARGEM
            esc = 2 * max(c['V1'], c['V0']) / 100 / MARGEM
            return dict(Phi_1=p1, Phi_0=p0, Phi_a_favor_de_Lula=(p1 if b >= 0 else p0),
                        classe_que_teria_a_alteracao_a_favor_de_Lula=('D=1' if b >= 0 else 'D=0'),
                        ic99_Phi_escala_maior=[(b - Z99 * ep) * esc, (b + Z99 * ep) * esc],
                        votos_de_margem=(p1 if b >= 0 else p0) * MARGEM,
                        teto99_votos_de_margem=max(abs(b - Z99 * ep), abs(b + Z99 * ep)) * esc * MARGEM)
        p = -b / 1.785
        return dict(Phi=p, ic99_b=[b - Z99 * ep, b + Z99 * ep], votos_de_margem=p * MARGEM,
                    teto99_votos_de_margem=max(abs(b - Z99 * ep), abs(b + Z99 * ep)) / 1.785 * MARGEM)

    def linha(b, ep, mod, D):
        ns, ngr, n1 = n_var(mod, D)
        return dict(b=float(b), ep=float(ep), z=float(b / ep), n=mod.n, grupos_ef=mod.ng, municipios=mod.ncl,
                    secoes_em_grupos_onde_D_varia=ns, grupos_onde_D_varia=ngr, secoes_D1_nesses_grupos=n1,
                    ic99=[float(b - Z99 * ep), float(b + Z99 * ep)])

    # ------------------------------------------------------------------ observados e placebos de (a) a (e)
    obs = {k: {} for k in CONTR}
    MODELOS = {}          # (contraste) -> Modelo da especificação y (para os plantios)
    combos = {}
    for k, c in CONTR.items():
        combos.setdefault((id(c['fe']), c['amostra'].tobytes()), []).append(k)
    for nome_spec in ('y', 'yBN', 'yalt', 'pl22', 'pl18', 'plturno', 'gov', 'ysd', 'yT', 'plBN22'):
        sp = spec(B, cols, nome_spec)
        feitos = {}
        for k, c in CONTR.items():
            chave = (id(c['fe']), c['amostra'].tobytes())
            if nome_spec == 'yBN' and chave in feitos.get('_mods', {}):
                pass
            idx = np.flatnonzero(c['amostra'] & sp['ok'])
            try:
                cache = feitos.setdefault('_mods', {})
                if chave not in cache:
                    cache[chave] = Modelo(sp['X'], sp['w'], c['fe'], sp['cl'], idx)
                mod = cache[chave]
                b, ep = mod.fit(sp['y'], c['D'])
                o = linha(b[0], ep[0], mod, c['D'])
            except Exception as e:
                o = dict(erro=str(e))
            if 'b' in o:
                if nome_spec in ('y', 'ysd', 'yalt', 'pl22', 'pl18', 'plturno', 'gov'):
                    o.update(phis(k, o['b'], o['ep']))
                elif nome_spec in ('yBN', 'plBN22'):
                    o['Phi_BN'] = -o['b'] / 100 * c['C1'] / MARGEM
                    o['votos_de_margem'] = o['Phi_BN'] * MARGEM
                elif nome_spec == 'yT':
                    o['eleitores_a_mais_nas_D1'] = o['b'] / 100 * c['A1']
            if nome_spec == 'gov':
                o['lado_de_Lula_correlacao_por_UF'] = sp.get('lado')
            obs[k][nome_spec] = o
            if nome_spec == 'y' and 'b' in o:
                MODELOS[k] = mod
                # regiões
                rg = {}
                for j, nm in enumerate(REGIOES):
                    try:
                        mr = Modelo(sp['X'], sp['w'], c['fe'], sp['cl'], np.flatnonzero(c['amostra'] & sp['ok'] & (reg == j)))
                        br, er = mr.fit(sp['y'], c['D'])
                        rg[nm] = linha(br[0], er[0], mr, c['D'])
                    except Exception as e:
                        rg[nm] = dict(erro=str(e)[:80])
                o['regioes'] = rg
                o['regioes_mesmo_sentido'] = int(sum(1 for v in rg.values() if 'b' in v and v['b'] * o['b'] > 0))
                o['regioes_com_estimativa'] = int(sum(1 for v in rg.values() if 'b' in v))
            diz('obs', nome_spec, k, {a: (round(v, 4) if isinstance(v, float) else v) for a, v in o.items() if a in ('b', 'ep', 'z', 'n', 'erro')})
        if nome_spec == 'y':
            SP_Y = sp
            # conferência da função contra lib.fe_ols (agrupando o erro no próprio efeito fixo)
            from lib import fe_ols
            c = CONTR['e']
            ii = np.flatnonzero(c['amostra'] & sp['ok'])
            ii = ii[uf_i[ii] == UFS.index('SE')]
            m1 = Modelo(sp['X'], sp['w'], loc, loc, ii)
            b1, e1 = m1.fit(sp['y'], c['D'])
            f = fe_ols(sp['y'][ii], np.column_stack([sp['X'][ii], c['D'][ii].astype(float)]), loc[ii], sp['w'][ii])
            res['conferencia_fe_ols'] = dict(uf='SE', b_proprio=float(b1[0]), ep_proprio=float(e1[0]), b_lib=f['coef'][f'x{sp["X"].shape[1]}'],
                                             ep_lib=f['ep'][f'x{sp["X"].shape[1]}'])
            diz('conferencia', res['conferencia_fe_ols'])
            # (d) e (e) juntos; (a) e (b) em todo U com indicadoras
            mF = feitos['_mods'][(id(loc), tudo.tobytes())]
            bj, ej = mF.fit(sp['y'], np.column_stack([B['carga_pos'], B['urna_dif']]).astype(float))
            res['d_e_juntos'] = dict(b_carga_pos=float(bj[0]), ep_carga_pos=float(ej[0]), b_urna_dif=float(bj[1]), ep_urna_dif=float(ej[1]))
            bm, em = mF.fit(sp['y'], np.column_stack([mod2 == 0, mod2 == 1, mod2 == 3]).astype(float))
            res['modelos_todo_U_ref_UE2020'] = {m_: dict(b=float(b_), ep=float(e_), z=float(b_ / e_)) for m_, b_, e_ in zip(('UE2013', 'UE2015', 'UE2022'), bm, em)}
            M_F = mF
        del feitos
    res['observado'] = obs
    for k, c in CONTR.items():
        res.setdefault('contrastes', {})[k] = dict(nome=c['nome'], V1=c['V1'], V0=c['V0'], secoes_D1_em_U=int(c['c1'].sum()),
                                                   secoes_D0_em_U=int(c['c0'].sum()), z_criterio=c['zc'], tipo=c['tipo'],
                                                   b_de_Phi_1=(100 * MARGEM / 2 / c['V1'] if c['tipo'] == 'fatia' else -1.785))
    # placebo de ano (modelos de 2022 em 2022)
    sp22 = spec(B, cols, 'pl22')
    m22 = B['mod_22']; loc22 = B['loc_22']
    ano = {}
    novo22 = m22 == 5
    for nm, D, am, fe in (('UE2020 contra anteriores, zona e município', novo22, m22 >= 0, zm),
                          ('UE2020 contra anteriores, local de 2022', novo22, m22 >= 0, loc22),
                          ('UE2015 contra UE2013, locais mistos de 2022', m22 == 4, mistos(loc22, m22 == 4, m22 == 3, sp22['ok']), loc22)):
        try:
            mm = Modelo(sp22['X'], sp22['w'], fe, sp22['cl'], np.flatnonzero(am & sp22['ok']))
            b, ep = mm.fit(sp22['y'], D)
            ano[nm] = linha(b[0], ep[0], mm, D)
        except Exception as e:
            ano[nm] = dict(erro=str(e)[:100])
    ano['modelos_de_2022_em_U'] = {m_: int((m22 == j).sum()) for j, m_ in enumerate(['UE2009', 'UE2010', 'UE2011', 'UE2013', 'UE2015', 'UE2020'])}
    res['placebo_de_ano_2022'] = ano
    del sp22
    grava('parcial_d11_observado.json', res)
    diz('observados gravados', round(time.time() - t0))

    # ------------------------------------------------------------------ calibração de (a) a (e)
    cal = {}
    y0 = SP_Y['y']
    for k, c in CONTR.items():
        mod = MODELOS[k]
        Dr = mod.res(c['D'].astype(float)[mod.idx])
        yr0 = mod.res(y0[mod.idx])
        b0, e0 = mod.fit_res(yr0, Dr)
        exp_U = c['c1'] if c['tipo'] == 'fatia' else c['c0']
        exp_s = exp_U[mod.idx]
        Ls, Rs, Vs = L2[mod.idx], R2[mod.idx], V[mod.idx]
        esperado1 = (100 * MARGEM / 2 / c['V1']) if c['tipo'] == 'fatia' else -1.785   # b esperado para Phi = 1
        ck = {'b_observado': float(b0[0]), 'ep_observado': float(e0[0]), 'b_esperado_para_Phi_1': esperado1, 'plantios': {}}
        for sentido, phis_ in (('R_para_L', (0.10, 0.25, 0.50, 1.0)), ('L_para_R_espelho', (0.25,))):
            fonte_U = R2 if sentido == 'R_para_L' else L2
            fonte_s = Rs if sentido == 'R_para_L' else Ls
            sg = 1 if sentido == 'R_para_L' else -1
            for Phi in phis_:
                f = Phi * TROCA_VIRA / fonte_U[exp_U].sum()
                db = np.empty(200); ee = np.empty(200); bb = np.empty(200)
                for r in range(200):
                    t = rng.binomial(fonte_s[exp_s].astype(np.int64), min(f, 1.0))
                    yn = y0[mod.idx].copy()
                    yn[exp_s] = 100 * (Ls[exp_s] + sg * t) / Vs[exp_s]
                    b, ep = mod.fit_res(mod.res(yn), Dr)
                    bb[r] = b[0]; ee[r] = ep[0]; db[r] = b[0] - b0[0]
                esp = sg * esperado1 * Phi
                zinc = db / ee * np.sign(esp)
                if c['tipo'] == 'fatia':
                    phi_c = 2 * np.abs(bb) * np.where(bb >= 0, c['V1'], c['V0']) / 100 / MARGEM
                    sinal_num = float(np.mean((phi_c >= 0.25) & (np.abs(bb / ee) >= c['zc'])))
                    esc = 2 * max(c['V1'], c['V0']) / 100 / MARGEM
                    semsinal = float(np.mean((np.abs(bb) + Z99 * ee) * esc <= 0.10))
                else:
                    sinal_num = float(np.mean((np.abs(bb) >= 0.45) & (np.abs(bb / ee) >= c['zc'])))
                    semsinal = float(np.mean((np.abs(bb) + Z99 * ee) <= 0.18))
                ck['plantios'][f'{sentido}_Phi_{Phi}'] = dict(
                    taxa_f=float(f), incremento_medio_b=float(db.mean()), dp_incremento=float(db.std()), esperado_b=float(esp),
                    recuperacao=float(db.mean() / esp), vies=float(db.mean() / esp - 1), ep_medio=float(ee.mean()),
                    poder_pi=float(np.mean(zinc >= c['zc'])), fracao_condicoes_numericas_de_SINAL=sinal_num,
                    fracao_que_passaria_por_SEM_SINAL=semsinal)
        # falso sinal: D embaralhado dentro do município
        zs = np.empty(200); fs = 0
        d_s = c['D'].astype(float)[mod.idx]
        ordem = np.argsort(mod.cl, kind='stable')
        for r in range(200):
            perm = np.lexsort((rng.random(mod.n), mod.cl))
            dn = np.empty(mod.n); dn[ordem] = d_s[perm]
            try:
                b, ep = mod.fit_res(yr0, mod.res(dn))
            except np.linalg.LinAlgError:
                zs[r] = np.nan; continue
            zs[r] = b[0] / ep[0]
            if c['tipo'] == 'fatia':
                ph = 2 * abs(b[0]) * (c['V1'] if b[0] >= 0 else c['V0']) / 100 / MARGEM
                fs += int(ph >= 0.25 and abs(zs[r]) >= c['zc'])
            else:
                fs += int(abs(b[0]) >= 0.45 and abs(zs[r]) >= c['zc'])
        ck['embaralhado_no_municipio'] = dict(falso_sinal=fs / 200, dp_de_z=float(np.nanstd(zs)), media_de_z=float(np.nanmean(zs)),
                                              fracao_z_acima_do_criterio=float(np.nanmean(np.abs(zs) >= c['zc'])))
        pis = {p: ck['plantios'][f'R_para_L_Phi_{p}']['poder_pi'] for p in (0.10, 0.25, 0.50, 1.0)}
        ck['menor_Phi_com_poder_de_95'] = next((p for p in (0.10, 0.25, 0.50, 1.0) if pis[p] >= 0.95), None)
        ck['tem_poder_para_Phi_0_25'] = bool(pis[0.25] >= 0.95)
        cal[k] = ck
        diz('cal', k, {p: round(v, 3) for p, v in pis.items()}, 'vies(0,25)', round(ck['plantios']['R_para_L_Phi_0.25']['vies'], 3),
            'falso', ck['embaralhado_no_municipio'])
        grava('parcial_d11_calibracao.json', cal)
    res['calibracao'] = cal

    # ------------------------------------------------------------------ explicação inocente plantada (A8)
    ino = {}
    C2i = B['comp2'].astype(np.int64); R2i = B['R2'].astype(np.int64)

    def refaz(sub, quais):
        sp = spec(B, cols, 'y', sub=sub)
        out = {}
        cache = {}
        for k in quais:
            c = CONTR[k]
            chave = (id(c['fe']), c['amostra'].tobytes())
            if chave not in cache:
                cache[chave] = Modelo(sp['X'], sp['w'], c['fe'], sp['cl'], np.flatnonzero(c['amostra'] & sp['ok'] & (sp['w'] >= 30)))
            b, ep = cache[chave].fit(sp['y'], c['D'])
            out[k] = (b[0], ep[0])
        return out
    # (i) uniforme
    acc = {k: [] for k in CONTR}
    for r in range(30):
        t = rng.binomial(R2i, 0.036)
        o = refaz({'R2': R2i - t, 'comp2': C2i - t}, list(CONTR))
        for k, v in o.items():
            acc[k].append(v)
    ino['abstencao_pura_uniforme_3_6_por_cento'] = {}
    for k, l in acc.items():
        a = np.array(l); b0 = obs[k]['y']['b']
        ino['abstencao_pura_uniforme_3_6_por_cento'][k] = dict(
            b_medio=float(a[:, 0].mean()), incremento_medio=float(a[:, 0].mean() - b0), ep_medio=float(a[:, 1].mean()),
            z_medio_do_incremento=float(((a[:, 0] - b0) / a[:, 1]).mean()),
            fracao_incremento_acima_do_z_criterio=float(np.mean(np.abs((a[:, 0] - b0) / a[:, 1]) >= CONTR[k]['zc'])))
    grava('parcial_d11_inocente.json', ino)
    diz('inocente uniforme', {k: round(v['z_medio_do_incremento'], 2) for k, v in ino['abstencao_pura_uniforme_3_6_por_cento'].items()})
    # (ii) localizada
    ino['abstencao_pura_localizada_mesmo_efeito_na_margem_que_Phi_0_25'] = {}
    for k in ('a', 'b', 'c', 'd', 'e'):
        c = CONTR[k]
        exp_U = c['c1'] if c['tipo'] == 'fatia' else c['c0']
        f = 0.25 * TROCA_VIRA / R2[exp_U].sum()
        a = []
        for r in range(30):
            t = np.zeros(n, np.int64)
            t[exp_U] = rng.binomial(R2i[exp_U], min(2 * f, 1.0))
            a.append(refaz({'R2': R2i - t, 'comp2': C2i - t}, [k])[k])
        a = np.array(a); b0 = obs[k]['y']['b']
        esp = (100 * MARGEM / 2 / c['V1'] if c['tipo'] == 'fatia' else -1.785) * 0.25
        ino['abstencao_pura_localizada_mesmo_efeito_na_margem_que_Phi_0_25'][k] = dict(
            taxa_de_abstencao_plantada=float(2 * f), incremento_medio_b=float(a[:, 0].mean() - b0), b_que_a_troca_de_Phi_0_25_daria=float(esp),
            razao_sobre_a_troca=float((a[:, 0].mean() - b0) / esp), ep_medio=float(a[:, 1].mean()),
            fracao_vista=float(np.mean(((a[:, 0] - b0) / a[:, 1]) * np.sign(esp) >= c['zc'])))
        grava('parcial_d11_inocente.json', ino)
        diz('inocente localizada', k, ino['abstencao_pura_localizada_mesmo_efeito_na_margem_que_Phi_0_25'][k])
    res['explicacao_inocente_plantada'] = ino
    grava('parcial_d11.json', res)
    diz('d11 parte A pronta', round(time.time() - t0))
    return res, B, R, SP_Y, M_F, CONTR


def varredura(mod, yr, rot_idx, rotulos, Vv, uf_s, zmin=5.0):
    """A6: uma regressão por grupo (D = 1 no grupo contra todos os outros), pelos resíduos de mod. Devolve a lista."""
    out = []
    lab = rot_idx[mod.idx]
    for j in np.unique(lab):
        d = (lab == j).astype(float)
        s = np.bincount(mod.g, d, minlength=mod.ng); c = np.bincount(mod.g, minlength=mod.ng)
        var = ((s > 0) & (s < c))[mod.g] & (d > 0)
        nsec = int(var.sum()); nmun = int(len(np.unique(mod.cl[var])))
        o = dict(grupo=rotulos[j], secoes_na_conta=int(d.sum()), secoes_em_locais_onde_varia=nsec, municipios=nmun,
                 V_grupo=float(Vv[mod.idx][d > 0].sum()))
        if nsec >= 30 and nmun >= 10:
            Dr = mod.res(d)
            b, ep = mod.fit_res(yr, Dr)
            o.update(b=float(b[0]), ep=float(ep[0]), z=float(b[0] / ep[0]), testado=True,
                     Phi_do_grupo=float(2 * b[0] * o['V_grupo'] / 100 / MARGEM),
                     deslocamento_que_daria_z5=float(zmin * ep[0]), Phi_que_daria_z5=float(2 * zmin * ep[0] * o['V_grupo'] / 100 / MARGEM))
            # repetição por UF (coeficiente parcial sobre os resíduos nacionais)
            if abs(o['z']) >= 3:
                rep = {}
                for u in np.unique(uf_s[d > 0]):
                    m = uf_s == u
                    den = (mod.w[m] * Dr[m] ** 2).sum()
                    if den <= 0:
                        continue
                    bu = (mod.w[m] * Dr[m] * yr[m]).sum() / den
                    e = yr[m] - bu * Dr[m]
                    _, cl = np.unique(mod.cl[m], return_inverse=True)
                    G = cl.max() + 1
                    if G < 3:
                        continue
                    sc = np.bincount(cl, mod.w[m] * Dr[m] * e)
                    epu = math.sqrt(G / (G - 1) * (sc ** 2).sum()) / den
                    rep[UFS[u]] = dict(b=float(bu), z=float(bu / epu), secoes_do_grupo=int(d[m].sum()))
                o['por_UF'] = rep
                o['UFs_mesmo_sinal_e_z2'] = int(sum(1 for v in rep.values() if v['b'] * o['b'] > 0 and abs(v['z']) >= 2))
        else:
            o['testado'] = False
        out.append(o)
    nt = sum(1 for o in out if o['testado'])
    for o in out:
        if o['testado']:
            o['p_bonferroni'] = min(1.0, pnorm2(o['z']) * nt)
            o['passa'] = bool(abs(o['z']) >= zmin and o['p_bonferroni'] < 0.05)
    return out, nt


def resumo_varredura(lst, nt):
    t = [o for o in lst if o['testado']]
    zs = np.array([o['z'] for o in t])
    pas = [o for o in t if o['passa']]
    return dict(grupos=len(lst), testados=nt, max_abs_z=float(np.abs(zs).max()), z_esperado_do_maximo_sob_acaso=float(math.sqrt(2 * math.log(max(nt, 2)))),
                dp_dos_z=float(zs.std()), n_abs_z_3=int((np.abs(zs) >= 3).sum()), n_abs_z_5=int((np.abs(zs) >= 5).sum()),
                passam=[dict(grupo=o['grupo'], b=o['b'], z=o['z'], UFs=o.get('UFs_mesmo_sinal_e_z2'), secoes=o['secoes_na_conta'],
                             Phi_do_grupo=o['Phi_do_grupo']) for o in pas],
                passam_e_repetem_em_3_UFs=[o['grupo'] for o in pas if (o.get('UFs_mesmo_sinal_e_z2') or 0) >= 3],
                positivos=int((zs > 0).sum()), negativos=int((zs < 0).sum()),
                maiores=[dict(grupo=o['grupo'], b=o['b'], ep=o['ep'], z=o['z'], secoes=o['secoes_na_conta'], Phi_do_grupo=o['Phi_do_grupo'],
                              UFs=o.get('UFs_mesmo_sinal_e_z2')) for o in sorted(t, key=lambda o: -abs(o['z']))[:6]],
                Phi_que_daria_z5_mediana=float(np.median([o['Phi_que_daria_z5'] for o in t])),
                Phi_que_daria_z5_maximo=float(np.max([o['Phi_que_daria_z5'] for o in t])),
                deslocamento_z5_mediana_pp=float(np.median([o['deslocamento_que_daria_z5'] for o in t])))


def modo_d11b():
    """(f), (h), (g) e a amostra de logs."""
    t0 = time.time()
    B, R = carrega_base()
    meta = R['meta']; cols = meta['colunas_perfil']; rot = R['rotulos']
    n = len(B['uf_i'])
    rng = np.random.default_rng(SEMENTE + 1)
    L2, R2 = B['L2'].astype(float), B['R2'].astype(float); V = L2 + R2
    loc = B['loc_id']; mun = B['mun_id']; uf_i = B['uf_i']; mod2 = B['mod2']; fc = B['fc']
    R2i = B['R2'].astype(np.int64)
    res = {}
    sp = spec(B, cols, 'y'); spBN = spec(B, cols, 'yBN'); spA = spec(B, cols, 'yalt')
    M_F = Modelo(sp['X'], sp['w'], loc, sp['cl'], np.flatnonzero(sp['ok']))
    M_A = Modelo(spA['X'], spA['w'], loc, spA['cl'], np.flatnonzero(spA['ok']))
    yr = M_F.res(sp['y'][M_F.idx]); yrBN = M_F.res(spBN['y'][M_F.idx]); yrA = M_A.res(spA['y'][M_A.idx])
    # ---------------- (f) datas de carga
    f = {}
    for nm, mod, r_ in (('y', M_F, yr), ('yBN', M_F, yrBN), ('yalt', M_A, yrA)):
        lst, nt = varredura(mod, r_, B['dia'], rot['dia'], V, uf_i[mod.idx])
        f[nm] = dict(resumo=resumo_varredura(lst, nt), grupos=lst)
        diz('(f)', nm, {k: v for k, v in f[nm]['resumo'].items() if k in ('testados', 'max_abs_z', 'n_abs_z_5', 'passam_e_repetem_em_3_UFs')})
    res['f_datas_de_carga'] = f
    grava('parcial_d11b.json', res)
    # ---------------- (h) faixas de 5.000 números de série dentro do modelo
    faixa_lab = [f'{MODS[m]}:{int(u) // 5000 * 5000}' if m >= 0 else 'desconhecido' for m, u in zip(mod2, B['urna2'])]
    fu, fi = np.unique(np.array(faixa_lab), return_inverse=True)
    dm = np.column_stack([mod2 == 0, mod2 == 1, mod2 == 3]).astype(float)
    M_H = Modelo(np.column_stack([sp['X'], dm]), sp['w'], loc, sp['cl'], np.flatnonzero(sp['ok']))
    M_HA = Modelo(np.column_stack([spA['X'], dm]), spA['w'], loc, spA['cl'], np.flatnonzero(spA['ok']))
    h = {}
    for nm, mod, yv in (('y', M_H, sp['y']), ('yBN', M_H, spBN['y']), ('yalt', M_HA, spA['y'])):
        lst, nt = varredura(mod, mod.res(yv[mod.idx]), fi, fu.tolist(), V, uf_i[mod.idx])
        h[nm] = dict(resumo=resumo_varredura(lst, nt), grupos=lst)
        diz('(h)', nm, {k: v for k, v in h[nm]['resumo'].items() if k in ('testados', 'max_abs_z', 'n_abs_z_5', 'passam_e_repetem_em_3_UFs')})
    res['h_faixas_de_serie'] = h
    # plantio de conferência em (f) e (h): grupo de tamanho mediano, Phi = 0,25 (taxa limitada a 1)
    conf = {}
    for nm, mod, labs, rotl, yv in (('f', M_F, B['dia'], rot['dia'], sp['y']), ('h', M_H, fi, fu.tolist(), sp['y'])):
        tst = [o for o in (res['f_datas_de_carga'] if nm == 'f' else h)['y']['grupos'] if o['testado']]
        alvo = sorted(tst, key=lambda o: o['secoes_na_conta'])[len(tst) // 2]
        j = rotl.index(alvo['grupo'])
        exp_U = labs == j
        fplant = min(1.0, 0.25 * TROCA_VIRA / R2[exp_U].sum())
        d = (labs[mod.idx] == j).astype(float); Dr = mod.res(d)
        es = exp_U[mod.idx]
        zz = []
        for r in range(50):
            t = rng.binomial(R2i[mod.idx][es], fplant)
            yn = yv[mod.idx].copy(); yn[es] = 100 * (L2[mod.idx][es] + t) / V[mod.idx][es]
            b, ep = mod.fit_res(mod.res(yn), Dr)
            zz.append(b[0] / ep[0])
        conf[nm] = dict(grupo=alvo['grupo'], secoes=alvo['secoes_na_conta'], taxa_plantada=float(fplant),
                        Phi_plantado=float(fplant * R2[exp_U].sum() / TROCA_VIRA), z_observado=alvo['z'], z_medio_com_plantio=float(np.mean(zz)),
                        fracao_z5=float(np.mean(np.abs(zz) >= 5)))
    res['f_h_plantio_de_conferencia'] = conf
    grava('parcial_d11b.json', res)
    diz('(f) e (h) prontos', round(time.time() - t0), conf)
    del M_H, M_HA

    # ---------------- (g) flashcard
    nloc = int(loc.max()) + 1; M = int(mun.max()) + 1
    mun_do_local = np.zeros(nloc, np.int64); mun_do_local[loc] = mun
    p2 = L2 / V; vbin = 1e4 * p2 * (1 - p2) / V
    comp2 = B['comp2'].astype(float); q2 = (B['B2'] + B['N2']) / comp2; vbinBN = 1e4 * q2 * (1 - q2) / comp2
    full = lambda mod, r_: (lambda a: (a.__setitem__(mod.idx, r_), a)[1])(np.full(n, np.nan))
    r26 = full(M_F, yr); rBN = full(M_F, yrBN); rA = full(M_A, yrA)
    plac = {}
    for nm in ('pl22', 'pl18', 'plBN22'):
        s_ = spec(B, cols, nm)
        m_ = Modelo(s_['X'], s_['w'], loc, s_['cl'], np.flatnonzero(s_['ok']))
        rr = full(m_, m_.res(s_['y'][m_.idx]))
        if nm == 'plBN22':
            c2 = B['comp2_22'].astype(float); qq = (B['B2_22'] + B['N2_22']) / np.where(c2 > 0, c2, 1)
            vv = 1e4 * qq * (1 - qq) / np.where(c2 > 0, c2, 1)
        else:
            sfx = nm[2:]
            Lx, Rx = B['L2_' + sfx].astype(float), B['R2_' + sfx].astype(float); Vx = np.where(Lx + Rx > 0, Lx + Rx, 1)
            vv = 1e4 * (Lx / Vx) * (1 - Lx / Vx) / Vx
        plac[nm] = (rr, vv)
        del m_, s_
    Cb = boot_contagens(rng, M, 9999)

    def tau_e_excesso(ra, va, rb, vb, grp, cb, base=None):
        """tau2 de a e de b nas seções em que os dois resíduos existem; excesso com bootstrap por município."""
        m = np.isfinite(ra) & np.isfinite(rb)
        if base is not None:
            m &= base
        la, da, dra, wa, inf = tau2_pares(ra[m], va[m], loc[m], grp[m])
        lb, db, drb, wb, _ = tau2_pares(rb[m], vb[m], loc[m], grp[m])
        Na, Dn = por_municipio(la, da, wa, mun_do_local, M); Nb, _ = por_municipio(lb, db, wb, mun_do_local, M)
        Nra, _ = por_municipio(la, dra, wa, mun_do_local, M); Nrb, _ = por_municipio(lb, drb, wb, mun_do_local, M)
        t2a, t2b = Na.sum() / Dn.sum(), Nb.sum() / Dn.sum()
        den = cb @ Dn.astype(np.float32)
        ba, bb = (cb @ Na.astype(np.float32)) / den, (cb @ Nb.astype(np.float32)) / den
        ex = raiz_sinal(ba - bb)
        return dict(info=inf, tau2=float(t2a), tau=float(raiz_sinal(t2a)), tau2_placebo=float(t2b), tau_placebo=float(raiz_sinal(t2b)),
                    tau_sem_desconto_binomial=float(raiz_sinal(Nra.sum() / Dn.sum())),
                    tau_placebo_sem_desconto_binomial=float(raiz_sinal(Nrb.sum() / Dn.sum())),
                    ep_tau2=float(np.nanstd(ba)), ep_tau2_placebo=float(np.nanstd(bb)),
                    excesso=float(raiz_sinal(t2a - t2b)), excesso2=float(t2a - t2b), ep_excesso2=float(np.nanstd(ba - bb)),
                    excesso_li_99_9=float(np.nanpercentile(ex, 0.1)), excesso_ls_99=float(np.nanpercentile(ex, 99)),
                    excesso_ic95=[float(np.nanpercentile(ex, 2.5)), float(np.nanpercentile(ex, 97.5))])

    def tau_so(ra, va, grp, cb, base=None):
        m = np.isfinite(ra)
        if base is not None:
            m &= base
        la, da, dra, wa, inf = tau2_pares(ra[m], va[m], loc[m], grp[m])
        Na, Dn = por_municipio(la, da, wa, mun_do_local, M)
        Nr, _ = por_municipio(la, dra, wa, mun_do_local, M)
        bo = (cb @ Na.astype(np.float32)) / (cb @ Dn.astype(np.float32))
        t2 = Na.sum() / Dn.sum()
        return dict(info=inf, tau2=float(t2), tau=float(raiz_sinal(t2)), ep_tau2=float(np.nanstd(bo)),
                    tau_sem_desconto_binomial=float(raiz_sinal(Nr.sum() / Dn.sum())),
                    tau_ic95=[float(raiz_sinal(np.nanpercentile(bo, 2.5))), float(raiz_sinal(np.nanpercentile(bo, 97.5)))],
                    z_tau2=float(t2 / np.nanstd(bo)))

    g = {}
    g['y_contra_2022'] = tau_e_excesso(r26, vbin, plac['pl22'][0], plac['pl22'][1], fc, Cb)
    g['y_contra_2018'] = tau_e_excesso(r26, vbin, plac['pl18'][0], plac['pl18'][1], fc, Cb)
    g['y_todo_U'] = tau_so(r26, vbin, fc, Cb)
    g['yBN_contra_2022'] = tau_e_excesso(rBN, vbinBN, plac['plBN22'][0], plac['plBN22'][1], fc, Cb)
    v22 = plac['pl22'][1]
    g['yalt'] = tau_so(rA, vbin + v22, fc, Cb)
    mF = np.isfinite(r26)
    g['assimetria_y'] = assimetria_grupos(r26[mF], loc[mF], fc[mF])
    m22 = np.isfinite(plac['pl22'][0])
    g['assimetria_placebo_2022'] = assimetria_grupos(plac['pl22'][0][m22], loc[m22], fc[m22])
    g['assimetria_yBN'] = assimetria_grupos(rBN[mF], loc[mF], fc[mF])
    # exploratório A9
    for nm in ('ysd', 'yT'):
        s_ = spec(B, cols, nm)
        m_ = Modelo(s_['X'], s_['w'], loc, s_['cl'], np.flatnonzero(s_['ok']))
        rr = full(m_, m_.res(s_['y'][m_.idx]))
        g['exploratorio_' + nm] = tau_so(rr, vbin if nm == 'ysd' else np.zeros(n), fc, Cb)
        g['exploratorio_' + nm]['assimetria'] = assimetria_grupos(rr[np.isfinite(rr)], loc[np.isfinite(rr)], fc[np.isfinite(rr)])
        del m_, s_
    res['g_flashcard'] = g
    grava('parcial_d11b.json', res)
    diz('(g) observado', {k: (round(v['tau'], 4), round(v.get('excesso', float('nan')), 4)) for k, v in g.items() if 'tau' in v}, round(time.time() - t0))

    # calibração de (g)
    Cc = Cb[:2999]
    calg = {}
    nfc = int(fc.max()) + 1
    idxF = M_F.idx; y0 = sp['y']
    for q in (0.1, 0.5, 0.8):
        acc = []
        for r in range(200):
            sel = rng.random(nfc) < q
            exp_U = sel[fc]
            fpl = (TROCA_VIRA / 4) / R2[exp_U].sum()
            t = np.zeros(n); t[exp_U] = rng.binomial(R2i[exp_U], fpl)
            yn = 100 * (L2 + t) / V
            rn = np.full(n, np.nan); rn[idxF] = M_F.res(yn[idxF])
            pn = (L2 + t) / V
            o = tau_e_excesso(rn, 1e4 * pn * (1 - pn) / V, plac['pl22'][0], plac['pl22'][1], fc, Cc)
            a = assimetria_grupos(rn[mF], loc[mF], fc[mF])
            acc.append((o['tau'], o['excesso'], o['excesso_li_99_9'], o['excesso_ls_99'], a['assimetria'], a['acima_de_3'], a['abaixo_de_menos_3']))
        a = np.array(acc, float)
        teor = 0.446 * math.sqrt((1 - q) / q)
        calg[f'q_{q}'] = dict(tau_teorico_do_plantio=teor, tau_medio=float(a[:, 0].mean()), excesso_medio=float(a[:, 1].mean()),
                              excesso_esperado=float(raiz_sinal(g['y_contra_2022']['excesso2'] + teor ** 2)),
                              fracao_li_99_9_acima_de_zero=float(np.mean(a[:, 2] > 0)), fracao_excesso_0_22=float(np.mean(a[:, 1] >= 0.22)),
                              fracao_ls_99_abaixo_de_0_15=float(np.mean(a[:, 3] < 0.15)), assimetria_media=float(a[:, 4].mean()),
                              fracao_assimetria_positiva=float(np.mean(a[:, 4] > 0)),
                              fracao_SINAL_completo=float(np.mean((a[:, 1] >= 0.22) & (a[:, 2] > 0) & (a[:, 4] > 0))),
                              fracao_SINAL_sem_a_assimetria=float(np.mean((a[:, 1] >= 0.22) & (a[:, 2] > 0))),
                              acima_de_3_medio=float(a[:, 5].mean()), abaixo_de_menos_3_medio=float(a[:, 6].mean()))
        diz('cal (g)', q, calg[f'q_{q}'])
        res['g_calibracao'] = calg
        grava('parcial_d11b.json', res)
    # nulo: rótulos de flashcard embaralhados dentro do local
    ls, fs, rs, vs = loc[mF], fc[mF], r26[mF], vbin[mF]
    ordem = np.argsort(ls, kind='stable')
    nul = []
    for r in range(200):
        perm = np.lexsort((rng.random(len(ls)), ls))
        fn = np.empty_like(fs); fn[ordem] = fs[perm]
        la, da, dra, wa, _ = tau2_pares(rs, vs, ls, fn)
        nul.append((wa * da).sum() / wa.sum())
    nul = np.array(nul)
    calg['nulo_rotulos_embaralhados_no_local'] = dict(tau2_medio=float(nul.mean()), dp_tau2=float(nul.std()), tau2_observado=g['y_todo_U']['tau2'],
                                                     z_do_observado=float((g['y_todo_U']['tau2'] - nul.mean()) / nul.std()),
                                                     p=float((1 + (nul >= g['y_todo_U']['tau2']).sum()) / 201))
    res['g_calibracao'] = calg
    grava('parcial_d11b.json', res)
    diz('nulo (g)', calg['nulo_rotulos_embaralhados_no_local'])

    # ---------------- (g) na amostra de logs: computador e usuário das mídias
    lg = {}
    nolog = B['nolog']
    for chave, titulo in (('log_c_comp', 'computador da mídia de carga'), ('log_c_user', 'usuário da mídia de carga'),
                          ('log_m_comp', 'computador da mídia de resultado do 2º turno'), ('log_m_user', 'usuário da mídia de resultado do 2º turno'),
                          ('log_v_comp', 'computador da mídia de votação (ao lado)'), ('log_v_user', 'usuário da mídia de votação (ao lado)')):
        grp = B[chave]; vazio = rot[chave].index('') if '' in rot[chave] else -1
        base = nolog & (grp != vazio)
        try:
            o = tau_e_excesso(r26, vbin, plac['pl22'][0], plac['pl22'][1], grp, Cb, base=base)
            o['so_2026'] = tau_so(r26, vbin, grp, Cb, base=base)
        except Exception as e:
            o = dict(erro=str(e)[:100])
        mm = base & mF
        o['secoes_da_amostra_na_conta'] = int(mm.sum()); o['grupos'] = int(len(np.unique(grp[mm])))
        o['titulo'] = titulo
        # poder: metade dos grupos com a taxa de um quarto da margem concentrada em metade (q = 0,5)
        if 'tau' in o:
            fpl = (TROCA_VIRA / 4) / (0.5 * R2.sum())
            ng = int(grp.max()) + 1
            vis = []
            for r in range(100):
                sel = rng.random(ng) < 0.5
                e_ = base & sel[grp]
                t = np.zeros(n); t[e_] = rng.binomial(R2i[e_], fpl)
                yn = 100 * (L2 + t) / V
                rn = np.full(n, np.nan); rn[idxF] = M_F.res(yn[idxF])
                oo = tau_e_excesso(rn, vbin, plac['pl22'][0], plac['pl22'][1], grp, Cc, base=base)
                vis.append((oo['excesso_li_99_9'] > 0, oo['excesso'], oo['tau']))
            vv = np.array(vis, float)
            o['plantio_q_0_5'] = dict(taxa=float(fpl), tau_teorico=0.446, fracao_li_99_9_acima_de_zero=float(vv[:, 0].mean()),
                                      excesso_medio=float(vv[:, 1].mean()), tau_medio=float(vv[:, 2].mean()))
        lg[chave] = o
        diz('(g) logs', chave, {k: v for k, v in o.items() if k in ('tau', 'excesso', 'excesso_li_99_9', 'excesso_ls_99', 'info', 'plantio_q_0_5', 'erro')})
    res['g_logs'] = lg
    res['logs_meta'] = {k: meta[k] for k in ('logs_regras', 'logs_em_U', 'logs_total')}
    grava('parcial_d11b.json', res)
    diz('d11b pronto', round(time.time() - t0))


def modo_d11d():
    """EXPLORATÓRIO, escrito depois de ver o resultado de (g): o excesso de tau sobre 2022 saiu acima de 0,22 sem
    passar no limite de 99,9% nem na assimetria, e o placebo de 2018 deu tau maior que o de 2026. Quatro contas para
    saber o que o tau de 2026 marca:
    (1) pares vizinhos: só pares de seções vizinhas na ordem do número dentro do local; diferença entre vizinhas de
        flashcards diferentes e vizinhas do mesmo flashcard (tira a explicação "seções de numeração distante têm
        eleitorado diferente");
    (2) tau do desfecho do 1º turno de 2026 com referência em 2022 (placebo de turno) com os flashcards do 2º turno;
    (3) tau da variação do comparecimento (y_T) em 2026 e no placebo de 2022, com excesso;
    (4) tau2 de 2026 e de 2022 por UF e por região (onde estaria)."""
    t0 = time.time()
    B, R = carrega_base()
    meta = R['meta']; cols = meta['colunas_perfil']
    n = len(B['uf_i'])
    rng = np.random.default_rng(SEMENTE + 5)
    loc = B['loc_id']; mun = B['mun_id']; uf_i = B['uf_i']; fc = B['fc']; sec = B['secao']
    L2, R2 = B['L2'].astype(float), B['R2'].astype(float); V = L2 + R2
    nloc = int(loc.max()) + 1; M = int(mun.max()) + 1
    mun_do_local = np.zeros(nloc, np.int64); mun_do_local[loc] = mun
    uf_do_mun = np.zeros(M, np.int64); uf_do_mun[mun] = uf_i
    Cb = boot_contagens(rng, M, 4999)

    def resid(nome):
        s_ = spec(B, cols, nome)
        m_ = Modelo(s_['X'], s_['w'], loc, s_['cl'], np.flatnonzero(s_['ok']))
        a = np.full(n, np.nan); a[m_.idx] = m_.res(s_['y'][m_.idx])
        return a
    p2 = L2 / V; v26 = 1e4 * p2 * (1 - p2) / V

    def vbin(sfx):
        Lx, Rx = B['L2_' + sfx].astype(float), B['R2_' + sfx].astype(float); Vx = np.where(Lx + Rx > 0, Lx + Rx, 1)
        return 1e4 * (Lx / Vx) * (1 - Lx / Vx) / Vx
    L1, R1 = B['L1'].astype(float), B['R1'].astype(float); V1 = np.where(L1 + R1 > 0, L1 + R1, 1)
    v1t = 1e4 * (L1 / V1) * (1 - L1 / V1) / V1
    RES = {'y_2026': (resid('y'), v26), 'placebo_2022': (resid('pl22'), vbin('22')), 'placebo_2018': (resid('pl18'), vbin('18')),
           'turno_1t_2026_ref_2022': (resid('plturno'), v1t), 'yT_2026': (resid('yT'), np.zeros(n)), 'yT_2022': (resid('plT22'), np.zeros(n))}
    out = {}

    def tau_boot(ra, va, base):
        la, da, dra, wa, inf = tau2_pares(ra[base], va[base], loc[base], fc[base])
        Na, Dn = por_municipio(la, da, wa, mun_do_local, M)
        return Na, Dn, inf
    # (2) e (3): tau em conjuntos comuns
    comum = np.isfinite(RES['y_2026'][0]) & np.isfinite(RES['placebo_2022'][0]) & np.isfinite(RES['turno_1t_2026_ref_2022'][0]) & np.isfinite(RES['yT_2022'][0])
    t = {}
    NN = {}
    for nm, (ra, va) in RES.items():
        if nm == 'placebo_2018':
            continue
        Na, Dn, inf = tau_boot(ra, va, comum)
        bo = (Cb @ Na.astype(np.float32)) / (Cb @ Dn.astype(np.float32))
        t2 = Na.sum() / Dn.sum()
        NN[nm] = (Na, Dn)
        t[nm] = dict(tau2=float(t2), tau=float(raiz_sinal(t2)), ep_tau2=float(bo.std()), z=float(t2 / bo.std()), info=inf)
    den = Cb @ NN['y_2026'][1].astype(np.float32)
    for a, b in (('yT_2026', 'yT_2022'), ('y_2026', 'turno_1t_2026_ref_2022'), ('y_2026', 'placebo_2022')):
        dfb = (Cb @ (NN[a][0] - NN[b][0]).astype(np.float32)) / den
        e2 = t[a]['tau2'] - t[b]['tau2']
        t[f'excesso_{a}_sobre_{b}'] = dict(excesso2=float(e2), excesso=float(raiz_sinal(e2)), ep_excesso2=float(dfb.std()), z=float(e2 / dfb.std()),
                                          li_99_9=float(raiz_sinal(np.percentile(dfb, 0.1))), ls_99=float(raiz_sinal(np.percentile(dfb, 99))))
    out['tau_no_conjunto_comum'] = t
    grava('parcial_d11d.json', out)
    diz('d11d tau', {k: (round(v.get('tau', v.get('excesso')), 4), round(v['z'], 2)) for k, v in t.items()})

    # (1) pares vizinhos
    def vizinhos(ra, va, base):
        ii = np.flatnonzero(base)
        o = ii[np.lexsort((sec[ii], loc[ii]))]
        a, b = o[:-1], o[1:]
        k = loc[a] == loc[b]
        a, b = a[k], b[k]
        q = (ra[a] - ra[b]) ** 2 / 2 - (va[a] + va[b]) / 2
        qraw = (ra[a] - ra[b]) ** 2 / 2
        mesmo = fc[a] == fc[b]
        l = loc[a]
        nd = np.bincount(l[~mesmo], minlength=nloc).astype(float); ns = np.bincount(l[mesmo], minlength=nloc).astype(float)
        sd_ = np.bincount(l[~mesmo], q[~mesmo], minlength=nloc); ss_ = np.bincount(l[mesmo], q[mesmo], minlength=nloc)
        sdr = np.bincount(l[~mesmo], qraw[~mesmo], minlength=nloc); ssr = np.bincount(l[mesmo], qraw[mesmo], minlength=nloc)
        ok = (nd > 0) & (ns > 0)
        w = nd[ok] * ns[ok] / (nd[ok] + ns[ok])
        d = sd_[ok] / nd[ok] - ss_[ok] / ns[ok]
        dr = sdr[ok] / nd[ok] - ssr[ok] / ns[ok]
        lo = np.flatnonzero(ok)
        N_, D_ = por_municipio(lo, d, w, mun_do_local, M)
        Nr, _ = por_municipio(lo, dr, w, mun_do_local, M)
        return N_, D_, Nr, dict(locais=int(ok.sum()), pares_vizinhos_de_flashcards_diferentes=int(nd[ok].sum()),
                               pares_vizinhos_do_mesmo_flashcard=int(ns[ok].sum()), fracao_de_pares_vizinhos_com_o_mesmo_flashcard=float(mesmo.mean()),
                               pares_vizinhos_total=int(len(mesmo)))
    viz = {}
    VV = {}
    comum2 = np.isfinite(RES['y_2026'][0]) & np.isfinite(RES['placebo_2022'][0])
    for nm in ('y_2026', 'placebo_2022', 'yT_2026', 'yT_2022', 'turno_1t_2026_ref_2022'):
        ra, va = RES[nm]
        N_, D_, Nr, inf = vizinhos(ra, va, comum)
        bo = (Cb @ N_.astype(np.float32)) / (Cb @ D_.astype(np.float32))
        t2 = N_.sum() / D_.sum()
        VV[nm] = (N_, D_)
        viz[nm] = dict(tau2=float(t2), tau=float(raiz_sinal(t2)), ep_tau2=float(bo.std()), z=float(t2 / bo.std()),
                       tau_sem_desconto_binomial=float(raiz_sinal(Nr.sum() / D_.sum())), info=inf)
    den = Cb @ VV['y_2026'][1].astype(np.float32)
    for a, b in (('y_2026', 'placebo_2022'), ('yT_2026', 'yT_2022')):
        dfb = (Cb @ (VV[a][0] - VV[b][0]).astype(np.float32)) / den
        e2 = viz[a]['tau2'] - viz[b]['tau2']
        viz[f'excesso_{a}_sobre_{b}'] = dict(excesso2=float(e2), excesso=float(raiz_sinal(e2)), ep_excesso2=float(dfb.std()), z=float(e2 / dfb.std()))
    ra, va = RES['placebo_2018']
    c18 = np.isfinite(RES['y_2026'][0]) & np.isfinite(ra)
    for nm, (rx, vx) in (('y_2026_no_conjunto_de_2018', RES['y_2026']), ('placebo_2018', RES['placebo_2018'])):
        N_, D_, Nr, inf = vizinhos(rx, vx, c18)
        bo = (Cb @ N_.astype(np.float32)) / (Cb @ D_.astype(np.float32))
        viz[nm] = dict(tau2=float(N_.sum() / D_.sum()), tau=float(raiz_sinal(N_.sum() / D_.sum())), ep_tau2=float(bo.std()),
                       z=float(N_.sum() / D_.sum() / bo.std()), info=inf)
    out['pares_vizinhos'] = viz
    grava('parcial_d11d.json', out)
    diz('d11d vizinhos', {k: (round(v.get('tau', v.get('excesso')), 4), round(v['z'], 2)) for k, v in viz.items()})

    # (4) por UF e por região: tau2 de 2026 e de 2022 e o excesso
    Na, Dn = NN['y_2026']; Nb, _ = NN['placebo_2022']
    reg_do_mun = regiao_de(uf_do_mun)
    por = {}
    for rot_, grupo_do_mun, nomes in (('UF', uf_do_mun, UFS), ('regiao', reg_do_mun, list(REGIOES))):
        d_ = {}
        for j, nm in enumerate(nomes):
            k = np.flatnonzero((grupo_do_mun == j) & (Dn > 0))
            if len(k) < 5:
                continue
            cb = rng.multinomial(len(k), np.full(len(k), 1.0 / len(k)), size=1999).astype(np.float32)
            dd = cb @ Dn[k].astype(np.float32)
            ba, bb = (cb @ Na[k].astype(np.float32)) / dd, (cb @ Nb[k].astype(np.float32)) / dd
            ta, tb = Na[k].sum() / Dn[k].sum(), Nb[k].sum() / Dn[k].sum()
            d_[nm] = dict(municipios=int(len(k)), peso=float(Dn[k].sum()), tau2_2026=float(ta), ep_2026=float(ba.std()), tau2_2022=float(tb),
                          ep_2022=float(bb.std()), excesso2=float(ta - tb), ep_excesso2=float((ba - bb).std()), z_excesso=float((ta - tb) / (ba - bb).std()),
                          tau_2026=float(raiz_sinal(ta)), tau_2022=float(raiz_sinal(tb)))
        por[rot_] = d_
    out['tau_por_UF_e_regiao'] = por
    grava('parcial_d11d.json', out)
    diz('d11d pronto', round(time.time() - t0), {k: (round(v['tau_2026'], 3), round(v['tau_2022'], 3), round(v['z_excesso'], 2)) for k, v in por['regiao'].items()})


def modo_d11e():
    """EXPLORATÓRIO, depois de ver o A9: os contrastes de (a) a (e) na variação do comparecimento de 2022 (mesmas seções,
    atributos de 2026), para saber se a diferença de comparecimento vista em (b), (c) e (d) já existia antes das urnas
    de 2026; e (b), (c) e (d) de y_T por UF onde há variação."""
    B, R = carrega_base()
    cols = R['meta']['colunas_perfil']
    n = len(B['uf_i'])
    mod2 = B['mod2']; loc = B['loc_id']; zm = B['zm_id']; mun = B['mun_id']
    tudo = np.ones(n, bool); nova = mod2 >= 2
    CONTR = {'a': ((mod2 == 3), mistos(loc, mod2 == 3, mod2 == 2, tudo), loc), 'b': ((mod2 == 1), mistos(loc, mod2 == 1, mod2 == 0, tudo), loc),
             'c': (nova, mod2 >= 0, zm), 'd': (B['carga_pos'] == 1, tudo, loc), 'e': (B['urna_dif'] == 1, tudo, loc)}
    out = {}
    for nome_spec in ('yT', 'plT22'):
        sp = spec(B, cols, nome_spec)
        for k, (D, am, fe) in CONTR.items():
            o = {}
            for nm, cl in (('municipio', mun), ('local', loc)):
                mod = Modelo(sp['X'], sp['w'], fe, cl, np.flatnonzero(am & sp['ok']))
                b, ep = mod.fit(sp['y'], D)
                o.update({'b': float(b[0]), 'ep_por_' + nm: float(ep[0]), 'z_por_' + nm: float(b[0] / ep[0]), 'n': mod.n})
            if nome_spec == 'yT' and k in ('b', 'c', 'd'):
                pu = {}
                for u in range(27):
                    try:
                        mod = Modelo(sp['X'], sp['w'], fe, loc, np.flatnonzero(am & sp['ok'] & (B['uf_i'] == u)))
                        ns, ngr, n1 = n_var(mod, D)
                        if ngr < 10:
                            continue
                        b, ep = mod.fit(sp['y'], D)
                        pu[UFS[u]] = dict(b=float(b[0]), ep_por_local=float(ep[0]), z=float(b[0] / ep[0]), grupos_onde_varia=ngr, secoes_D1=n1)
                    except Exception:
                        pass
                o['por_UF'] = pu
            out.setdefault(k, {})[nome_spec] = o
        diz('d11e', nome_spec, {k: (round(v[nome_spec]['b'], 4), round(v[nome_spec]['z_por_municipio'], 2), round(v[nome_spec]['z_por_local'], 2)) for k, v in out.items()})
    grava('parcial_d11e.json', out)
    for k in ('b', 'c', 'd'):
        diz('d11e por UF', k, {u: (round(x['b'], 3), round(x['z'], 1), x['grupos_onde_varia']) for u, x in out[k]['yT']['por_UF'].items()})


def modo_d11f():
    """EXPLORATÓRIO, depois de ver que o excesso de (g) depende do desconto binomial: o mesmo tau com o resíduo
    padronizado pelo tamanho da seção (r x raiz(V / V médio)), sem desconto, em 2026, 2022 e 2018; e o tau com desconto
    só nos locais em que todas as seções têm V entre 0,8 e 1,25 vezes a mediana do local (tamanhos parecidos)."""
    B, R = carrega_base()
    cols = R['meta']['colunas_perfil']
    n = len(B['uf_i'])
    rng = np.random.default_rng(SEMENTE + 7)
    loc = B['loc_id']; mun = B['mun_id']; fc = B['fc']
    nloc = int(loc.max()) + 1; M = int(mun.max()) + 1
    mun_do_local = np.zeros(nloc, np.int64); mun_do_local[loc] = mun
    Cb = boot_contagens(rng, M, 4999)
    out = {}
    RES = {}
    for nm, sfx in (('y', None), ('pl22', '22'), ('pl18', '18')):
        s_ = spec(B, cols, nm)
        m_ = Modelo(s_['X'], s_['w'], loc, s_['cl'], np.flatnonzero(s_['ok']))
        a = np.full(n, np.nan); a[m_.idx] = m_.res(s_['y'][m_.idx])
        Vx = s_['w'].astype(float)
        p_ = (B['L2'] if sfx is None else B['L2_' + sfx]).astype(float) / np.where(Vx > 0, Vx, 1)
        RES[nm] = (a, Vx, 1e4 * p_ * (1 - p_) / np.where(Vx > 0, Vx, 1))
    for par, (na, nb) in (('2026_contra_2022', ('y', 'pl22')), ('2026_contra_2018', ('y', 'pl18'))):
        ra, Va, va = RES[na]; rb, Vb, vb = RES[nb]
        m = np.isfinite(ra) & np.isfinite(rb)
        o = {}
        # (i) padronizado
        sa = ra * np.sqrt(Va / Va[m].mean()); sb = rb * np.sqrt(Vb / Vb[m].mean())
        z0 = np.zeros(n)
        la, da, _, wa, inf = tau2_pares(sa[m], z0[m], loc[m], fc[m]); lb, db, _, wb, _ = tau2_pares(sb[m], z0[m], loc[m], fc[m])
        Na, Dn = por_municipio(la, da, wa, mun_do_local, M); Nb, _ = por_municipio(lb, db, wb, mun_do_local, M)
        den = Cb @ Dn.astype(np.float32)
        ba, bb = (Cb @ Na.astype(np.float32)) / den, (Cb @ Nb.astype(np.float32)) / den
        ta, tb = Na.sum() / Dn.sum(), Nb.sum() / Dn.sum()
        o['residuo_padronizado_pelo_tamanho'] = dict(tau2_a=float(ta), ep_a=float(ba.std()), tau2_b=float(tb), ep_b=float(bb.std()), tau_a=float(raiz_sinal(ta)),
                                                     tau_b=float(raiz_sinal(tb)), excesso2=float(ta - tb), ep_excesso2=float((ba - bb).std()),
                                                     z_excesso=float((ta - tb) / (ba - bb).std()), excesso=float(raiz_sinal(ta - tb)), locais=inf['locais'])
        # (ii) locais de tamanhos parecidos nos dois anos
        def parecidos(Vv):
            lu, l = np.unique(loc[m], return_inverse=True)
            vv = Vv[m]
            mx = np.zeros(len(lu)); np.maximum.at(mx, l, vv)
            mn = np.full(len(lu), np.inf); np.minimum.at(mn, l, vv)
            ok = (mx / np.maximum(mn, 1)) <= 1.5625
            k = np.zeros(n, bool); k[np.flatnonzero(m)] = ok[l]
            return k
        k = parecidos(Va) & parecidos(Vb)
        la, da, _, wa, inf = tau2_pares(ra[k], va[k], loc[k], fc[k]); lb, db, _, wb, _ = tau2_pares(rb[k], vb[k], loc[k], fc[k])
        Na, Dn = por_municipio(la, da, wa, mun_do_local, M); Nb, _ = por_municipio(lb, db, wb, mun_do_local, M)
        den = Cb @ Dn.astype(np.float32)
        ba, bb = (Cb @ Na.astype(np.float32)) / den, (Cb @ Nb.astype(np.float32)) / den
        ta, tb = Na.sum() / Dn.sum(), Nb.sum() / Dn.sum()
        o['locais_de_secoes_de_tamanho_parecido'] = dict(tau2_a=float(ta), ep_a=float(np.nanstd(ba)), tau2_b=float(tb), ep_b=float(np.nanstd(bb)), tau_a=float(raiz_sinal(ta)),
                                                         tau_b=float(raiz_sinal(tb)), excesso2=float(ta - tb), ep_excesso2=float(np.nanstd(ba - bb)),
                                                         z_excesso=float((ta - tb) / np.nanstd(ba - bb)), excesso=float(raiz_sinal(ta - tb)), locais=inf['locais'], secoes=inf['secoes'])
        out[par] = o
        diz('d11f', par, json.dumps(o))
    grava('parcial_d11f.json', out)


def modo_d11g():
    """Lista de conferência (pista, não teste): flashcards com média do resíduo centrado no local mais afastada de zero
    (t_f = média x raiz de n, padronizado), com UF, zona e seções, para pedido de atas de carga."""
    B, R = carrega_base()
    cols = R['meta']['colunas_perfil']; rot = R['rotulos']; chaves = R['chaves']
    n = len(B['uf_i'])
    loc = B['loc_id']; fc = B['fc']
    sp = spec(B, cols, 'y')
    mod = Modelo(sp['X'], sp['w'], loc, sp['cl'], np.flatnonzero(sp['ok']))
    r = mod.res(sp['y'][mod.idx]); ii = mod.idx
    l, f = loc[ii], fc[ii]
    nl = int(loc.max()) + 1; K = int(fc.max()) + 2
    cu = np.unique(l.astype(np.int64) * K + f)
    ngl = np.bincount((cu // K).astype(np.int64), minlength=nl)
    m = ngl[l] >= 2
    nf = np.bincount(f[m], minlength=K).astype(float); sf = np.bincount(f[m], r[m], minlength=K)
    Vf = np.bincount(f[m], sp['w'][ii][m], minlength=K)
    k = nf >= 5
    t = np.where(k, sf / np.sqrt(np.maximum(nf, 1)), 0.0)
    z = (t - t[k].mean()) / t[k].std()
    out = {'flashcards_na_conta': int(k.sum())}
    for nome, ordem in (('a_favor_de_Lula', np.argsort(-np.where(k, z, -np.inf))[:10]), ('a_favor_de_Flavio', np.argsort(np.where(k, z, np.inf))[:10])):
        lst = []
        for j in ordem:
            secs = ii[m][f[m] == j]
            zs = sorted(set('|'.join(chaves[i].split('|')[:3]) for i in secs))
            lst.append(dict(flashcard=rot['fc'][j], secoes_em_locais_com_2_flashcards=int(nf[j]), media_do_residuo=float(sf[j] / nf[j]), t_padronizado=float(z[j]),
                            votos_validos=float(Vf[j]), votos_de_margem_se_fosse_irregularidade=float(2 * sf[j] / nf[j] / 100 * Vf[j]),
                            uf_municipio_zona=zs[:4], exemplo_de_secoes=[chaves[i] for i in secs[:3]]))
        out[nome] = lst
    grava('parcial_d11g.json', out)
    for nome in ('a_favor_de_Lula', 'a_favor_de_Flavio'):
        diz(nome, [(x['flashcard'], x['secoes_em_locais_com_2_flashcards'], round(x['media_do_residuo'], 2), round(x['t_padronizado'], 1), x['uf_municipio_zona'][:2]) for x in out[nome]])


def modo_d11c():
    """Sensibilidade do erro de (a) a (e): agrupado por local e por zona e município, em cada especificação.
    Acrescentado depois de ver que o placebo de governador de (c) só é identificado em Manaus (um município), onde o
    erro por município degenera. Não muda nenhum coeficiente."""
    B, R = carrega_base()
    cols = R['meta']['colunas_perfil']
    n = len(B['uf_i'])
    mod2 = B['mod2']; loc = B['loc_id']; zm = B['zm_id']
    tudo = np.ones(n, bool); nova = mod2 >= 2
    CONTR = {'a': ((mod2 == 3), mistos(loc, mod2 == 3, mod2 == 2, tudo), loc), 'b': ((mod2 == 1), mistos(loc, mod2 == 1, mod2 == 0, tudo), loc),
             'c': (nova, mod2 >= 0, zm), 'c_local': (nova, mod2 >= 0, loc), 'd': (B['carga_pos'] == 1, tudo, loc), 'e': (B['urna_dif'] == 1, tudo, loc)}
    out = {}
    for nome_spec in ('y', 'yBN', 'yalt', 'pl22', 'pl18', 'plturno', 'gov', 'ysd', 'yT'):
        sp = spec(B, cols, nome_spec)
        for k, (D, am, fe) in CONTR.items():
            o = {}
            for nm, cl in (('local', loc), ('zona_municipio', zm)):
                try:
                    mod = Modelo(sp['X'], sp['w'], fe, cl, np.flatnonzero(am & sp['ok']))
                    b, ep = mod.fit(sp['y'], D)
                    o['b'] = float(b[0]); o['ep_por_' + nm] = float(ep[0]); o['z_por_' + nm] = float(b[0] / ep[0]); o['grupos_' + nm] = mod.ncl
                    d = np.asarray(D, float)[mod.idx]
                    s = np.bincount(mod.g, d, minlength=mod.ng); c = np.bincount(mod.g, minlength=mod.ng)
                    v = ((s > 0) & (s < c))[mod.g]
                    o['municipios_onde_D_varia'] = int(len(np.unique(B['mun_id'][mod.idx][v])))
                    o['ufs_onde_D_varia'] = sorted(UFS[u] for u in np.unique(B['uf_i'][mod.idx][v]))
                except Exception as e:
                    o['erro_' + nm] = str(e)[:80]
            if nome_spec == 'y':
                reg = regiao_de(B['uf_i'])
                rg = {}
                for j, nm_r in enumerate(REGIOES):
                    try:
                        mod = Modelo(sp['X'], sp['w'], fe, loc, np.flatnonzero(am & sp['ok'] & (reg == j)))
                        b, ep = mod.fit(sp['y'], D)
                        d = np.asarray(D, float)[mod.idx]
                        s_ = np.bincount(mod.g, d, minlength=mod.ng); c_ = np.bincount(mod.g, minlength=mod.ng)
                        v = ((s_ > 0) & (s_ < c_))[mod.g]
                        rg[nm_r] = dict(b=float(b[0]), ep_por_local=float(ep[0]), z_por_local=float(b[0] / ep[0]),
                                        municipios_onde_D_varia=int(len(np.unique(B['mun_id'][mod.idx][v]))),
                                        secoes_D1_onde_varia=int((d[v] > 0).sum()))
                    except Exception as e:
                        rg[nm_r] = dict(erro=str(e)[:60])
                o['regioes_erro_por_local'] = rg
            out.setdefault(k, {})[nome_spec] = o
        diz('d11c', nome_spec, {k: (round(v[nome_spec].get('ep_por_local', float('nan')), 4), v[nome_spec].get('municipios_onde_D_varia')) for k, v in out.items()})
        grava('parcial_d11c.json', out)


# ============================================================================================ PARTE 2 (equipe vermelha)
def _proj_por_uf(X, w, ok, uf_i):
    """Para cada UF: linhas e base ortonormal (QR) de [1, X] ponderado, para tirar resíduo de qualquer y."""
    P = {}
    for u in range(27):
        ii = np.flatnonzero(ok & (uf_i == u))
        sw = np.sqrt(w[ii])
        Xu = np.column_stack([np.ones(len(ii)), X[ii]]) * sw[:, None]
        Q, Rr = np.linalg.qr(Xu)
        dg = np.abs(np.diag(Rr)); Q = Q[:, dg > 1e-9 * dg.max()]
        P[u] = (ii, sw, Q)
    return P


def _residuo_uf(P, y, n):
    r = np.full(n, np.nan)
    for u, (ii, sw, Q) in P.items():
        yw = y[ii] * sw
        r[ii] = (yw - Q @ (Q.T @ yw)) / sw
    return r


class Agrup:
    """E2: grupo, célula e estrato; estatística T e permutação dos rótulos entre células do estrato."""

    def __init__(self, estrato, celula, rotulo, base):
        ii = np.flatnonzero(base)
        self.ii = ii
        e = estrato[ii].astype(np.int64); c = celula[ii].astype(np.int64); l = rotulo[ii].astype(np.int64)
        K1 = int(c.max()) + 1; K2 = int(l.max()) + 1
        cu, self.cel = np.unique((e * K1 + c) * K2 + l, return_inverse=True)      # célula = estrato x célula x rótulo
        self.nc = len(cu)
        self.c_e = (cu // K2 // K1).astype(np.int64)
        gu, self.c_g = np.unique(self.c_e * K2 + (cu % K2), return_inverse=True)  # grupo = estrato x rótulo
        self.ng = len(gu)
        self.g_e = (gu // K2).astype(np.int64); self.g_l = (gu % K2).astype(np.int64)
        self.ordem = np.argsort(self.c_e, kind='stable')
        self.c_n = np.bincount(self.cel, minlength=self.nc).astype(float)

    def somas(self, r, w):
        rr, ww = r[self.ii], w[self.ii]
        return (np.bincount(self.cel, ww, minlength=self.nc), np.bincount(self.cel, ww * rr, minlength=self.nc),
                np.bincount(self.cel, ww * ww, minlength=self.nc), np.bincount(self.cel, ww * ww * rr, minlength=self.nc),
                np.bincount(self.cel, ww * ww * rr * rr, minlength=self.nc))

    def T(self, W, S, c_g=None):
        c_g = self.c_g if c_g is None else c_g
        ne = int(self.c_e.max()) + 1
        me = np.bincount(self.c_e, S, minlength=ne) / np.maximum(np.bincount(self.c_e, W, minlength=ne), 1e-300)
        Wg = np.bincount(c_g, W, minlength=self.ng); Sg = np.bincount(c_g, S, minlength=self.ng)
        k = Wg > 0
        return float((Wg[k] * (Sg[k] / Wg[k] - me[self.g_e[k]]) ** 2).sum() / W.sum())

    def perm(self, rng, W, S, reps):
        out = np.empty(reps)
        for r in range(reps):
            p = np.lexsort((rng.random(self.nc), self.c_e))
            cg = np.empty_like(self.c_g); cg[self.ordem] = self.c_g[p]
            out[r] = self.T(W, S, cg)
        return out

    def grupos(self, W, S, W2, S2, Q2):
        """Média, erro agrupado pela célula (zona) e número de seções de cada grupo."""
        Wg = np.bincount(self.c_g, W, minlength=self.ng); Sg = np.bincount(self.c_g, S, minlength=self.ng)
        ng_ = np.bincount(self.c_g, self.c_n, minlength=self.ng); G = np.bincount(self.c_g, minlength=self.ng).astype(float)
        m = Sg / np.maximum(Wg, 1e-300)
        sc = (S - m[self.c_g] * W) ** 2
        v_cl = np.bincount(self.c_g, sc, minlength=self.ng)
        with np.errstate(divide='ignore', invalid='ignore'):
            ep_cl = np.sqrt(G / (G - 1) * v_cl) / Wg
            v_s = np.bincount(self.c_g, Q2 - 2 * m[self.c_g] * S2 + m[self.c_g] ** 2 * W2, minlength=self.ng)
            ep_s = np.sqrt(ng_ / np.maximum(ng_ - 1, 1) * v_s) / Wg
        ep = np.where(G >= 2, ep_cl, ep_s)
        return m, ep, ng_, G, Wg


def _avalia(ag, r, w, rng, reps, nomes_g, lim_n=500, lista=True):
    W, S, W2, S2, Q2 = ag.somas(r, w)
    T = ag.T(W, S)
    tp = ag.perm(rng, W, S, reps)
    m, ep, ng_, G, Wg = ag.grupos(W, S, W2, S2, Q2)
    with np.errstate(divide='ignore', invalid='ignore'):
        z = m / ep
    gr = ng_ >= lim_n
    o = dict(T=T, T_medio_permutado=float(tp.mean()), razao=float(T / tp.mean()), p=float((1 + (tp >= T).sum()) / (1 + reps)),
             T_permutado_p95=float(np.percentile(tp, 95)), T_permutado_max=float(tp.max()),
             grupos=int(ag.ng), celulas=int(ag.nc), secoes=int(len(ag.ii)), grupos_500=int(gr.sum()),
             cumprem_mais_1_e_z4=int((gr & (m >= 1.0) & (z > 4)).sum()), acima_de_mais_0_5=int((gr & (m > 0.5)).sum()),
             espelho_cumprem_menos_1_e_z4=int((gr & (m <= -1.0) & (z < -4)).sum()), espelho_abaixo_de_menos_0_5=int((gr & (m < -0.5)).sum()),
             acima_de_mais_1=int((gr & (m >= 1.0)).sum()), abaixo_de_menos_1=int((gr & (m <= -1.0)).sum()))
    if lista:
        ordm = np.argsort(-np.where(gr, m, -np.inf))[:8]
        ordn = np.argsort(np.where(gr, m, np.inf))[:8]
        f = lambda j: dict(grupo=nomes_g(j), secoes=int(ng_[j]), zonas_ou_celulas=int(G[j]), media=float(m[j]), ep=float(ep[j]), z=float(z[j]),
                           votos_validos=float(Wg[j]), votos_de_margem_se_fosse_irregularidade=float(2 * m[j] / 100 * Wg[j]))
        o['maiores_a_favor_de_Lula'] = [f(j) for j in ordm if gr[j]]
        o['maiores_a_favor_de_Flavio'] = [f(j) for j in ordn if gr[j]]
        k = gr & (m >= 1.0) & (z > 4)
        o['votos_de_margem_nos_grupos_que_cumprem'] = float((2 * m[k] / 100 * Wg[k]).sum())
        k2 = gr & (m <= -1.0) & (z < -4)
        o['espelho_votos_de_margem_nos_grupos_que_cumprem'] = float((2 * m[k2] / 100 * Wg[k2]).sum())
    return o, (m, ep, ng_, Wg)


def modo_ev():
    t0 = time.time()
    B, R = carrega_base()
    meta = R['meta']; cols = meta['colunas_perfil']; rot = R['rotulos']
    n = len(B['uf_i'])
    rng = np.random.default_rng(SEMENTE + 2)
    uf_i = B['uf_i'].astype(np.int64); zona = B['zona_id'].astype(np.int64); loc = B['loc_id'].astype(np.int64)
    L2, R2 = B['L2'].astype(float), B['R2'].astype(float); V = L2 + R2
    R2i = B['R2'].astype(np.int64)
    sp = spec(B, cols, 'y')
    P = _proj_por_uf(sp['X'], sp['w'], sp['ok'], uf_i)
    r = _residuo_uf(P, sp['y'], n)
    ok = np.isfinite(r)
    s22 = spec(B, cols, 'pl22')
    P22 = _proj_por_uf(s22['X'], s22['w'], s22['ok'], uf_i)
    r22 = _residuo_uf(P22, s22['y'], n); ok22 = np.isfinite(r22); w22 = s22['w']
    del P22
    res = {'residuo': dict(secoes=int(ok.sum()), dp_ponderado=float(math.sqrt(np.average(r[ok] ** 2, weights=V[ok]))),
                           dp_ponderado_2022=float(math.sqrt(np.average(r22[ok22] ** 2, weights=w22[ok22]))))}
    dia = B['dia'].astype(np.int64); fc = B['fc'].astype(np.int64)
    nz = int(zona.max()) + 1; nd = int(dia.max()) + 1
    # dia modal da zona
    cz = np.zeros((nz, nd), np.int32); np.add.at(cz, (zona, dia), 1)
    modal = cz.argmax(1)[zona]
    AGR = {
        'data_de_carga_UF_x_dia (principal)': (uf_i, zona, dia, lambda ag: (lambda j: f"{UFS[ag.g_e[j]]} {rot['dia'][ag.g_l[j]]}")),
        'dia_modal_da_zona (ao lado)': (uf_i, zona, modal, lambda ag: (lambda j: f"{UFS[ag.g_e[j]]} dia modal {rot['dia'][ag.g_l[j]]}")),
        'flashcard (celula = local, estrato = zona)': (zona, loc, fc, lambda ag: (lambda j: f"flashcard {rot['fc'][ag.g_l[j]]}")),
    }
    obs = {}
    AG = {}
    for nm, (e, c, l, fn) in AGR.items():
        reps = 1999
        ag = Agrup(e, c, l, ok); AG[nm] = ag
        o, _ = _avalia(ag, r, V, rng, reps, fn(ag))
        ag2 = Agrup(e, c, l, ok22)
        o2, _ = _avalia(ag2, r22, w22, rng, reps, fn(ag2))
        o['placebo_residuo_de_2022_com_os_grupos_de_2026'] = {k: v for k, v in o2.items() if not k.startswith('maiores')}
        o['placebo_residuo_de_2022_com_os_grupos_de_2026']['maiores_a_favor_de_Lula'] = o2.get('maiores_a_favor_de_Lula', [])[:4]
        obs[nm] = o
        diz('ev', nm, {k: v for k, v in o.items() if k in ('T', 'razao', 'p', 'grupos_500', 'cumprem_mais_1_e_z4', 'acima_de_mais_0_5',
                                                         'espelho_cumprem_menos_1_e_z4', 'espelho_abaixo_de_menos_0_5')},
            'placebo', {k: v for k, v in o2.items() if k in ('razao', 'p', 'cumprem_mais_1_e_z4', 'espelho_cumprem_menos_1_e_z4')})
        res['bweb'] = obs
        grava('parcial_ev.json', res)
    res['codigo_de_carga'] = dict(testavel=False, motivo='CD_CARGA_1_URNA_EFETIVADA é único por urna (uma seção por valor, fora o valor de '
                                  'preenchimento das juntas): não forma grupo', valores_distintos_2t=499180, secoes_2t=499205)
    # amostra de logs
    nolog = B['nolog']
    lg = {}
    for chave, titulo, por_uf in (('log_m_comp', 'computador da mídia de resultado do 2º turno', False),
                                  ('log_c_comp', 'computador da mídia de carga', False),
                                  ('log_m_dia', 'UF x dia de geração da mídia de resultado do 2º turno', True),
                                  ('log_c_dia', 'UF x dia de geração da mídia de carga', True),
                                  ('log_m_user', 'usuário da mídia de resultado do 2º turno (ao lado)', False),
                                  ('log_c_user', 'usuário da mídia de carga (ao lado)', False)):
        lab = B[chave].astype(np.int64); vazio = rot[chave].index('') if '' in rot[chave] else -1
        base = nolog & ok & (lab != vazio)
        ag = Agrup(uf_i, zona, lab, base)
        o, _ = _avalia(ag, r, V, rng, 1999, (lambda ag_, ch: (lambda j: f"{UFS[ag_.g_e[j]]} {rot[ch][ag_.g_l[j]]}"))(ag, chave), lim_n=10)
        o['nota'] = 'na amostra o piso de 500 seções não existe; a lista usa grupos com 10 seções ou mais e os contadores são desse piso'
        o['maior_grupo_secoes'] = int(np.bincount(ag.c_g, ag.c_n).max())
        b22 = nolog & ok22 & (lab != vazio)
        ag2 = Agrup(uf_i, zona, lab, b22)
        o2, _ = _avalia(ag2, r22, w22, rng, 1999, None, lim_n=10, lista=False)
        o['placebo_residuo_de_2022'] = o2
        o['titulo'] = titulo
        lg[chave] = o
        diz('ev logs', chave, {k: v for k, v in o.items() if k in ('T', 'razao', 'p', 'grupos', 'celulas', 'secoes', 'grupos_500', 'cumprem_mais_1_e_z4')})
    res['logs'] = lg
    # datas de geração na amostra (descritivo, sem voto)
    res['logs_dias_de_geracao'] = {
        'midia_de_resultado_2t': dict(collections.Counter(rot['log_m_dia'][j] for j in B['log_m_dia'][nolog]).most_common()),
        'midia_de_carga': dict(collections.Counter(rot['log_c_dia'][j] for j in B['log_c_dia'][nolog]).most_common())}
    grava('parcial_ev.json', res)

    # ---------------- calibração (E4)
    nm0 = 'data_de_carga_UF_x_dia (principal)'
    ag = AG[nm0]
    W, S, W2, S2, Q2 = ag.somas(r, V)
    _, _, ng_, _, Wg = ag.grupos(W, S, W2, S2, Q2)
    # grupo de cada seção
    g_sec = np.full(n, -1, np.int64); g_sec[ag.ii] = ag.c_g[ag.cel]
    cal = {}
    for nome, q in (('concentrado_em_10_por_cento_dos_votos', 0.10), ('concentrado_em_50_por_cento_dos_votos', 0.50), ('um_grupo_de_500_ou_mais_com_2_pontos', None)):
        acc = []
        for rep in range(100):
            if q is not None:
                ordg = rng.permutation(ag.ng); cum = np.cumsum(Wg[ordg]); k = int(np.searchsorted(cum, q * Wg.sum())) + 1
                sel = np.zeros(ag.ng, bool); sel[ordg[:k]] = True
                e_ = (g_sec >= 0) & sel[np.maximum(g_sec, 0)]
                fpl = (TROCA_VIRA / 4) / R2[e_].sum()
            else:
                cand = np.flatnonzero(ng_ >= 500); gsel = rng.choice(cand)
                sel = np.zeros(ag.ng, bool); sel[gsel] = True
                e_ = (g_sec == gsel)
                fpl = min(1.0, 0.02 * V[e_].sum() / R2[e_].sum())
            t = np.zeros(n); t[e_] = rng.binomial(R2i[e_], fpl)
            rn = _residuo_uf(P, 100 * (L2 + t) / V, n)
            o, (m, ep, ngx, _) = _avalia(ag, rn, V, rng, 1999, None, lista=False)
            with np.errstate(divide='ignore', invalid='ignore'):
                zz = m / ep
            pl = sel & (ngx >= 500)
            acc.append((o['razao'], o['p'], o['cumprem_mais_1_e_z4'], float(np.mean(m[pl])) if pl.any() else np.nan,
                        float(np.mean((m[pl] >= 1.0) & (zz[pl] > 4))) if pl.any() else np.nan, 100 * fpl * R2[e_].sum() / V[e_].sum()))
        a = np.array(acc, float)
        cal[nome] = dict(razao_media=float(a[:, 0].mean()), fracao_razao_2=float(np.mean(a[:, 0] >= 2)), fracao_p_0_001=float(np.mean(a[:, 1] < 0.001)),
                         fracao_com_grupo_que_cumpre=float(np.mean(a[:, 2] > 0)),
                         fracao_SINAL_completo=float(np.mean((a[:, 0] >= 2) & (a[:, 1] < 0.001) & (a[:, 2] > 0))),
                         media_do_residuo_nos_grupos_plantados=float(np.nanmean(a[:, 3])),
                         fracao_dos_grupos_plantados_que_cumprem=float(np.nanmean(a[:, 4])), deslocamento_plantado_pp=float(a[:, 5].mean()),
                         grupos_que_cumprem_medio=float(a[:, 2].mean()))
        diz('ev cal', nome, cal[nome])
        res['calibracao'] = cal
        grava('parcial_ev.json', res)
    diz('ev pronto', round(time.time() - t0))


def modo_evb():
    """Complementos da PARTE 2, escritos DEPOIS de ver a primeira saída (marcados como exploratórios no relatório):
    (1) a referência do agrupamento principal (rótulos permutados entre células zona x dia) saiu acima do observado em
        todas as 1.999 permutações, em 2026 e no placebo de 2022: ela mistura células grandes e pequenas e por isso não
        é "do mesmo tamanho". Aqui a calibração é refeita avaliando, nas mesmas cópias plantadas, o agrupamento
        principal e o do dia modal da zona (declarado antes como "ao lado"), cuja referência permuta zonas inteiras.
    (2) poder na amostra de logs (um quarto da margem concentrado em 10% e em 50% dos computadores da mídia de resultado).
    (3) conferência dirigida da coincidência citada pela equipe vermelha: mídia de resultado gerada de 16/10 em diante
        contra gerada antes, na amostra de logs, com erro por zona; AM e MA à parte."""
    t0 = time.time()
    B, R = carrega_base()
    meta = R['meta']; cols = meta['colunas_perfil']; rot = R['rotulos']
    n = len(B['uf_i'])
    rng = np.random.default_rng(SEMENTE + 4)
    uf_i = B['uf_i'].astype(np.int64); zona = B['zona_id'].astype(np.int64)
    L2, R2 = B['L2'].astype(float), B['R2'].astype(float); V = L2 + R2
    R2i = B['R2'].astype(np.int64)
    sp = spec(B, cols, 'y')
    P = _proj_por_uf(sp['X'], sp['w'], sp['ok'], uf_i)
    r = _residuo_uf(P, sp['y'], n); ok = np.isfinite(r)
    dia = B['dia'].astype(np.int64)
    nz = int(zona.max()) + 1; nd = int(dia.max()) + 1
    cz = np.zeros((nz, nd), np.int32); np.add.at(cz, (zona, dia), 1)
    modal = cz.argmax(1)[zona]
    ag1 = Agrup(uf_i, zona, dia, ok); ag2 = Agrup(uf_i, zona, modal, ok)
    res = {}
    out = {}
    for alvo_nome, agp in (('plantio_em_grupos_UF_x_dia', ag1), ('plantio_em_grupos_de_zonas_pelo_dia_modal', ag2)):
        W, S, W2, S2, Q2 = agp.somas(r, V)
        _, _, ng_, _, Wg = agp.grupos(W, S, W2, S2, Q2)
        g_sec = np.full(n, -1, np.int64); g_sec[agp.ii] = agp.c_g[agp.cel]
        for nome, q in (('10_por_cento_dos_votos', 0.10), ('50_por_cento_dos_votos', 0.50)):
            acc = []
            for rep in range(100):
                ordg = rng.permutation(agp.ng); cum = np.cumsum(Wg[ordg]); k = int(np.searchsorted(cum, q * Wg.sum())) + 1
                sel = np.zeros(agp.ng, bool); sel[ordg[:k]] = True
                e_ = (g_sec >= 0) & sel[np.maximum(g_sec, 0)]
                fpl = (TROCA_VIRA / 4) / R2[e_].sum()
                t = np.zeros(n); t[e_] = rng.binomial(R2i[e_], fpl)
                rn = _residuo_uf(P, 100 * (L2 + t) / V, n)
                o1, _ = _avalia(ag1, rn, V, rng, 999, None, lista=False)
                o2, _ = _avalia(ag2, rn, V, rng, 999, None, lista=False)
                acc.append((o1['razao'], o1['p'], o1['cumprem_mais_1_e_z4'], o1['acima_de_mais_0_5'],
                            o2['razao'], o2['p'], o2['cumprem_mais_1_e_z4'], o2['acima_de_mais_0_5']))
            a = np.array(acc, float)
            f = lambda j: dict(razao_media=float(a[:, j].mean()), fracao_razao_2=float(np.mean(a[:, j] >= 2)),
                               fracao_p_minimo=float(np.mean(a[:, j + 1] <= 0.001)), fracao_p_abaixo_de_0_05=float(np.mean(a[:, j + 1] < 0.05)),
                               fracao_com_grupo_que_cumpre=float(np.mean(a[:, j + 2] > 0)), fracao_com_grupo_acima_de_0_5=float(np.mean(a[:, j + 3] > 0)),
                               fracao_SINAL_completo=float(np.mean((a[:, j] >= 2) & (a[:, j + 1] <= 0.001) & (a[:, j + 2] > 0))),
                               fracao_que_escaparia_como_SEM_SINAL=float(np.mean((a[:, j + 1] > 0.05) & (a[:, j + 3] == 0))))
            out[f'{alvo_nome}: {nome}'] = dict(principal_UF_x_dia=f(0), dia_modal_da_zona=f(4), nota='999 permutações por cópia: o menor p possível é 0,001')
            diz('evb', alvo_nome, nome, out[f'{alvo_nome}: {nome}'])
            res['calibracao_dos_dois_agrupamentos'] = out
            grava('parcial_evb.json', res)
    # (2) poder na amostra de logs
    nolog = B['nolog']
    lab = B['log_m_comp'].astype(np.int64); vazio = rot['log_m_comp'].index('') if '' in rot['log_m_comp'] else -1
    base = nolog & ok & (lab != vazio)
    agl = Agrup(uf_i, zona, lab, base)
    nl = int(lab.max()) + 1
    pl = {}
    for nome, q in (('10_por_cento_dos_computadores', 0.10), ('50_por_cento_dos_computadores', 0.50)):
        fpl = min(1.0, (TROCA_VIRA / 4) / (q * R2.sum()))
        acc = []
        for rep in range(100):
            sel = rng.random(nl) < q
            e_ = base & sel[lab]
            t = np.zeros(n); t[e_] = rng.binomial(R2i[e_], fpl)
            rn = r.copy(); rn[e_] = r[e_] + 100 * t[e_] / V[e_]      # o modelo por UF quase não muda com 0,8% das seções
            o1, _ = _avalia(agl, rn, V, rng, 999, None, lim_n=10, lista=False)
            acc.append((o1['razao'], o1['p']))
        a = np.array(acc)
        pl[nome] = dict(taxa=float(fpl), razao_media=float(a[:, 0].mean()), fracao_razao_2=float(np.mean(a[:, 0] >= 2)),
                        fracao_p_minimo=float(np.mean(a[:, 1] <= 0.001)), fracao_p_abaixo_de_0_05=float(np.mean(a[:, 1] < 0.05)))
        diz('evb logs', nome, pl[nome])
    res['poder_na_amostra_de_logs_computador_da_midia_de_resultado'] = pl
    # (3) mídia de resultado gerada de 16/10 em diante
    dias = np.array(rot['log_m_dia'])[B['log_m_dia']]
    tem = nolog & ok & (dias != '')
    tarde = tem & (dias >= '2026-10-16')
    cedo = tem & (dias < '2026-10-16')

    def dif(mask_uf=None):
        a = tarde if mask_uf is None else tarde & mask_uf
        b = cedo if mask_uf is None else cedo & mask_uf
        if a.sum() < 5 or b.sum() < 5:
            return dict(secoes_tarde=int(a.sum()), secoes_cedo=int(b.sum()))
        ma = np.average(r[a], weights=V[a]); mb = np.average(r[b], weights=V[b])
        def var(m_, mu):
            _, z = np.unique(zona[m_], return_inverse=True)
            sc = np.bincount(z, V[m_] * (r[m_] - mu)); G = len(sc)
            return (G / max(G - 1, 1)) * (sc ** 2).sum() / V[m_].sum() ** 2, G
        va, Ga = var(a, ma); vb, Gb = var(b, mb)
        ep = math.sqrt(va + vb)
        return dict(secoes_tarde=int(a.sum()), zonas_tarde=int(Ga), secoes_cedo=int(b.sum()), zonas_cedo=int(Gb), media_tarde=float(ma), media_cedo=float(mb),
                    diferenca=float(ma - mb), ep=float(ep), z=float((ma - mb) / ep))
    res['midia_de_resultado_gerada_de_16_10_em_diante'] = {'amostra_inteira': dif(), 'AM': dif(uf_i == UFS.index('AM')), 'MA': dif(uf_i == UFS.index('MA')),
                                                           'AM_e_MA': dif((uf_i == UFS.index('AM')) | (uf_i == UFS.index('MA'))),
                                                           'por_UF_secoes_tarde': {UFS[u]: int((tarde & (uf_i == u)).sum()) for u in range(27) if (tarde & (uf_i == u)).sum()}}
    # grupos de 500 seções ou mais na amostra de logs (a letra do critério), por agrupamento
    g500 = {}
    for chave in ('log_m_comp', 'log_c_comp', 'log_m_dia', 'log_c_dia'):
        lab_ = B[chave].astype(np.int64); vz = rot[chave].index('') if '' in rot[chave] else -1
        ag_ = Agrup(uf_i, zona, lab_, nolog & ok & (lab_ != vz))
        W, S, W2, S2, Q2 = ag_.somas(r, V)
        m_, ep_, ng_, G_, Wg_ = ag_.grupos(W, S, W2, S2, Q2)
        g500[chave] = [dict(grupo=f"{UFS[ag_.g_e[j]]} {rot[chave][ag_.g_l[j]]}", secoes=int(ng_[j]), zonas=int(G_[j]), media=float(m_[j]),
                            ep=float(ep_[j]), z=float(m_[j] / ep_[j])) for j in np.flatnonzero(ng_ >= 500)]
    res['logs_grupos_de_500_secoes_ou_mais'] = g500
    # no bweb: AM e MA, resíduo médio por dia de carga (descritivo)
    res['bweb_AM_MA_residuo_medio_da_UF'] = {}
    for u in ('AM', 'MA', 'PI', 'TO', 'PB', 'CE'):
        m_ = ok & (uf_i == UFS.index(u))
        dd = {}
        for j in np.unique(dia[m_]):
            k = m_ & (dia == j)
            if k.sum() >= 200:
                dd[rot['dia'][j]] = dict(secoes=int(k.sum()), media=float(np.average(r[k], weights=V[k])))
        res['bweb_AM_MA_residuo_medio_da_UF'][u] = dd
    grava('parcial_evb.json', res)
    diz('evb pronto', round(time.time() - t0), json.dumps(res['midia_de_resultado_gerada_de_16_10_em_diante'], ensure_ascii=False))


def modo_evc():
    """Poder de cada agrupamento da amostra de logs na PARTE 2 (exploratório, complementa o modo evb): um quarto da margem
    concentrado em 10% e em 50% dos grupos sorteados, 100 cópias, 999 permutações."""
    B, R = carrega_base()
    cols = R['meta']['colunas_perfil']; rot = R['rotulos']
    n = len(B['uf_i'])
    rng = np.random.default_rng(SEMENTE + 6)
    uf_i = B['uf_i'].astype(np.int64); zona = B['zona_id'].astype(np.int64)
    L2, R2 = B['L2'].astype(float), B['R2'].astype(float); V = L2 + R2
    R2i = B['R2'].astype(np.int64)
    sp = spec(B, cols, 'y')
    r = _residuo_uf(_proj_por_uf(sp['X'], sp['w'], sp['ok'], uf_i), sp['y'], n); ok = np.isfinite(r)
    nolog = B['nolog']
    out = {}
    for chave in ('log_m_comp', 'log_c_comp', 'log_m_dia', 'log_c_dia'):
        lab = B[chave].astype(np.int64); vazio = rot[chave].index('') if '' in rot[chave] else -1
        base = nolog & ok & (lab != vazio)
        ag = Agrup(uf_i, zona, lab, base)
        g_sec = np.full(n, -1, np.int64); g_sec[ag.ii] = ag.c_g[ag.cel]
        o = {}
        for nome, q in (('10_por_cento_dos_grupos', 0.10), ('50_por_cento_dos_grupos', 0.50)):
            fpl = min(1.0, (TROCA_VIRA / 4) / (q * R2.sum()))
            acc = []
            for rep in range(100):
                sel = rng.random(ag.ng) < q
                e_ = (g_sec >= 0) & sel[np.maximum(g_sec, 0)]
                t = np.zeros(n); t[e_] = rng.binomial(R2i[e_], fpl)
                rn = r.copy(); rn[e_] = r[e_] + 100 * t[e_] / V[e_]
                o1, _ = _avalia(ag, rn, V, rng, 999, None, lim_n=10, lista=False)
                acc.append((o1['razao'], o1['p']))
            a = np.array(acc)
            o[nome] = dict(taxa=float(fpl), razao_media=float(a[:, 0].mean()), fracao_razao_2=float(np.mean(a[:, 0] >= 2)),
                           fracao_p_minimo=float(np.mean(a[:, 1] <= 0.001)), fracao_p_abaixo_de_0_05=float(np.mean(a[:, 1] < 0.05)))
        out[chave] = o
        diz('evc', chave, o)
    grava('parcial_evc.json', out)


# ============================================================================================ PARTE 3 (D3-4)
def _pares(chave):
    _, c = np.unique(chave, return_counts=True)
    c = c[c > 1].astype(np.int64)
    return int((c * (c - 1) // 2).sum())


def _chave_votos(comp, L, R_, Bq, N):
    return (((comp.astype(np.int64) * 4096 + L) * 4096 + R_) * 4096 + Bq) * 4096 + N


def _rho(rng, V6, reps=200, minimo=50):
    """V6 = colunas comp, L, R, O, B, N. C_votos entre seções com comparecimento de 50 ou mais e a média reamostrada."""
    V6 = V6[(V6[:, 0] >= minimo) & (V6[:, 1:].sum(1) == V6[:, 0])]
    comp = V6[:, 0].astype(np.int64)
    C = _pares(_chave_votos(comp, V6[:, 1], V6[:, 2], V6[:, 4], V6[:, 5]))
    Pm = V6[:, 1:].astype(float) / comp[:, None]
    sim = np.empty(reps)
    for r in range(reps):
        X = rng.multinomial(comp, Pm)
        sim[r] = _pares(_chave_votos(comp, X[:, 0], X[:, 1], X[:, 3], X[:, 4]))
    return dict(secoes=int(len(comp)), C_votos=C, media_reamostrada=float(sim.mean()), dp_reamostrada=float(sim.std()),
                rho=float(C / sim.mean()), z=float((C - sim.mean()) / sim.std()), excesso_sobre_a_media=float(C - sim.mean())), V6


def modo_d34():
    t0 = time.time()
    D = dict(np.load(TRAB + '/base_d34.npz'))
    with open(TRAB + '/base_meta.json') as f:
        meta = json.load(f)
    rng = np.random.default_rng(SEMENTE + 3)
    res = {}
    # ---------------- (a) censo
    res['a_censo'] = {t: dict(secoes=meta[f'd34_n_{t}t'], urnas_repetidas=meta[f'd34_urnas_repetidas_{t}t'],
                              cargas_repetidas=meta[f'd34_cargas_repetidas_{t}t'], secoes_de_junta=meta[f'd34_secoes_de_junta_{t}t'],
                              secoes_em_urna_repetida=meta[f'd34_secoes_em_urna_repetida_{t}t'],
                              urna_repetida_fora_de_junta=meta[f'd34_urnas_repetidas_fora_de_junta_{t}t'],
                              carga_repetida_fora_de_junta=meta[f'd34_cargas_repetidas_fora_de_junta_{t}t']) for t in ('1', '2')}
    # ---------------- (a) C_exato
    def c_exato(t, reps, rng):
        m = ~D['junta' + t] & (D['enc' + t] >= 0) & (D['emi' + t] >= 0)
        Vt = np.column_stack([D[c + t][m] for c in ('comp', 'L', 'R', 'B', 'N')] + [D['biom' + t][m]])
        _, gid, cnt = np.unique(Vt, axis=0, return_inverse=True, return_counts=True)
        gid = gid.ravel()
        cand = cnt[gid] > 1
        tk = D['enc' + t][m].astype(np.int64) * (1 << 22) + D['emi' + t][m].astype(np.int64)
        uf = D['uf' + t][m]
        f = lambda tkv: _pares(gid[cand].astype(np.int64) * (1 << 44) + tkv[cand])
        C = f(tk)
        ordem = np.argsort(uf, kind='stable')
        sim = np.empty(reps)
        for r in range(reps):
            p = np.lexsort((rng.random(len(uf)), uf))
            tn = np.empty_like(tk); tn[ordem] = tk[p]
            sim[r] = f(tn)
        return dict(secoes=int(m.sum()), secoes_com_vetor_de_votos_e_biometria_repetido=int(cand.sum()), C_exato=C,
                    permutacoes=reps, media_permutada=float(sim.mean()), p95=float(np.percentile(sim, 95)), p99_9=float(np.percentile(sim, 99.9)),
                    max_permutado=float(sim.max())), (m, Vt, gid, cand, tk)
    ce2, guard = c_exato('2', 1000, rng)
    ce1, _ = c_exato('1', 200, rng)
    res['a_C_exato'] = {'2t': ce2, '1t_ao_lado': ce1}
    diz('C_exato', ce2, ce1)
    # poder: copiar o vetor completo de 5 seções para outras 5
    m, Vt, gid, cand, tk = guard
    pw = []
    full_key = np.column_stack([Vt, tk])
    C0 = ce2['C_exato']
    for r in range(20):
        ii = rng.choice(len(tk), 10, replace=False)
        fk = full_key.copy(); fk[ii[5:]] = fk[ii[:5]]
        _, cnt = np.unique(fk, axis=0, return_counts=True)
        c = cnt[cnt > 1].astype(np.int64)
        pw.append(int((c * (c - 1) // 2).sum()) - C0)
    res['a_C_exato']['poder_copia_de_5'] = dict(aumentos=pw, todos_iguais_a_5=bool(all(x == 5 for x in pw)))
    grava('parcial_d34.json', res)
    # ---------------- (a) C_votos e rho
    rho = {}
    conj = {'2026_2t': np.column_stack([D[c + '2'] for c in ('comp', 'L', 'R', 'O', 'B', 'N')]),
            '2026_1t': np.column_stack([D[c + '1'] for c in ('comp', 'L', 'R', 'O', 'B', 'N')]),
            '2022_2t': D['v2022_2'], '2022_1t': D['v2022_1'], '2018_2t': D['v2018_2'], '2018_1t': D['v2018_1'],
            '2014_2t': D['v2014_2'], '2014_1t': D['v2014_1']}
    guarda = {}
    for nm, V6 in conj.items():
        rho[nm], guarda[nm] = _rho(rng, V6)
        diz('rho', nm, rho[nm])
    plac = max(rho['2022_2t']['rho'], rho['2026_1t']['rho'])
    r26 = rho['2026_2t']
    res['a_C_votos'] = dict(por_conjunto=rho, maior_rho_dos_placebos_do_registro=plac, razao_2026_sobre_o_maior_placebo=r26['rho'] / plac,
                            excesso_sobre_o_maior_placebo=r26['C_votos'] - plac * r26['media_reamostrada'],
                            maior_rho_de_todos_os_outros=max(v['rho'] for k, v in rho.items() if k != '2026_2t'))
    # poder: copiar os votos de 3.000 seções grandes para outras 3.000 de mesmo comparecimento
    V6 = guarda['2026_2t']
    comp = V6[:, 0]
    porcomp = collections.defaultdict(list)
    for i, c in enumerate(comp):
        porcomp[int(c)].append(i)
    grandes = np.flatnonzero(comp >= 200)
    pw = []
    for r in range(20):
        Vn = V6.copy(); usados = set(); feitos = 0
        for i in rng.permutation(grandes):
            if feitos == 3000:
                break
            if i in usados:
                continue
            l = porcomp[int(comp[i])]
            j = l[rng.integers(len(l))]
            if j == i or j in usados:
                continue
            Vn[j] = V6[i]; usados.add(i); usados.add(j); feitos += 1
        C = _pares(_chave_votos(Vn[:, 0], Vn[:, 1], Vn[:, 2], Vn[:, 4], Vn[:, 5]))
        rr = C / r26['media_reamostrada']
        pw.append((feitos, C, rr, rr / plac, C - plac * r26['media_reamostrada']))
    a = np.array(pw, float)
    res['a_C_votos']['poder_copia_de_3000'] = dict(copias=float(a[:, 0].mean()), C_votos_medio=float(a[:, 1].mean()), rho_medio=float(a[:, 2].mean()),
                                                   razao_media_sobre_o_maior_placebo=float(a[:, 3].mean()), excesso_medio=float(a[:, 4].mean()),
                                                   fracao_que_passa_o_limiar=float(np.mean((a[:, 3] >= 1.25) & (a[:, 4] >= 3000))),
                                                   fracao_razao_1_25=float(np.mean(a[:, 3] >= 1.25)), fracao_excesso_3000=float(np.mean(a[:, 4] >= 3000)),
                                                   nota='a média reamostrada usada é a observada (as cópias quase não a mudam)')
    grava('parcial_d34.json', res)
    diz('(a) pronto', round(time.time() - t0))
    # ---------------- (b)
    g = lambda c: D['b_' + c].astype(float)
    L1, R1, O1, B1, N1, C1, A1 = (g(c + '1') for c in ('L', 'R', 'O', 'B', 'N', 'comp', 'apt'))
    L2, R2, C2, A2 = g('L2'), g('R2'), g('comp2'), g('apt2')
    V2 = L2 + R2; val1 = C1 - B1 - N1; V1 = L1 + R1
    base = (V2 >= 30) & (val1 >= 30) & (A2 > 0) & (C1 > 0)
    y = 100 * L2 / np.where(V2 > 0, V2, 1)
    c1 = np.where(C1 > 0, C1, 1)
    Xs = np.column_stack([L1 / c1, R1 / c1, g('c70') / c1, g('c14') / c1, g('c55') / c1, B1 / c1, N1 / c1, (C2 - C1) / np.where(A2 > 0, A2, 1),
                          np.log(np.where(A2 > 0, A2, 1))])
    f60 = D['b_f60']; tem60 = np.isfinite(f60)
    Xp = np.column_stack([Xs, np.where(tem60, f60, 0)])
    loc = D['b_loc']; mun = D['b_mun']
    y22 = D['b_y22']; tem22 = np.isfinite(y22)
    y1 = 100 * L1 / np.where(V1 > 0, V1, 1)
    R2i = D['b_R2'].astype(np.int64); V2i = (D['b_L2'] + D['b_R2']).astype(np.int64)
    b = {}
    for nome, S in (('urna_diferente', D['b_urna_dif'] == 1), ('carga_depois_de_04_10', D['b_carga_pos'] == 1)):
        o = {}
        for esp, X, mk in (('principal_com_idade', Xp, base & tem60), ('sem_idade_com_exterior', Xs, base)):
            mod = Modelo(X, V2, loc, mun, np.flatnonzero(mk))
            bb, ep = mod.fit(y, S)
            ns, ngr, n1 = n_var(mod, S)
            vt = float(V2[mod.idx][S[mod.idx]].sum())
            o[esp] = dict(beta=float(bb[0]), ep=float(ep[0]), z=float(bb[0] / ep[0]), p=pnorm2(bb[0] / ep[0]), n=mod.n, locais=mod.ng, municipios=mod.ncl,
                          tratadas_na_conta=int(S[mod.idx].sum()), tratadas_em_locais_com_comparacao=n1, ic95=[float(bb[0] - Z95 * ep[0]), float(bb[0] + Z95 * ep[0])],
                          validos_das_tratadas=vt, margem_implicada=float(2 * bb[0] / 100 * vt),
                          margem_implicada_teto_95=float(2 * max(abs(bb[0] - Z95 * ep[0]), abs(bb[0] + Z95 * ep[0])) / 100 * vt))
            if esp == 'principal_com_idade':
                # poder: mover Binomial(V, 0,018) limitado a R2, de R para L, nas tratadas; e o espelho
                Dr = mod.res(S.astype(float)[mod.idx]); yr0 = mod.res(y[mod.idx])
                es = S[mod.idx]
                for sg, nm in ((1, 'poder_mais_1_8'), (-1, 'espelho_menos_1_8')):
                    acc = []
                    for r in range(200):
                        t = rng.binomial(V2i[mod.idx][es], 0.018)
                        lim = R2i[mod.idx][es] if sg > 0 else D['b_L2'].astype(np.int64)[mod.idx][es]
                        t = np.minimum(t, lim)
                        yn = y[mod.idx].copy(); yn[es] = 100 * (L2[mod.idx][es] + sg * t) / V2[mod.idx][es]
                        b2, e2 = mod.fit_res(mod.res(yn), Dr)
                        acc.append((b2[0], e2[0]))
                    a = np.array(acc)
                    o[nm] = dict(beta_medio=float(a[:, 0].mean()), incremento_medio=float(a[:, 0].mean() - bb[0]), ep_medio=float(a[:, 1].mean()),
                                 fracao_p_0_001=float(np.mean(np.abs(a[:, 0] / a[:, 1]) >= 3.2905)),
                                 fracao_criterio_numerico=float(np.mean((sg * a[:, 0] >= 1.0) & (np.abs(a[:, 0] / a[:, 1]) >= 3.2905))))
                # embaralhado dentro do município
                zs = []
                d_s = S.astype(float)[mod.idx]; ordem = np.argsort(mod.cl, kind='stable')
                for r in range(200):
                    p = np.lexsort((rng.random(mod.n), mod.cl)); dn = np.empty(mod.n); dn[ordem] = d_s[p]
                    b2, e2 = mod.fit_res(yr0, mod.res(dn)); zs.append(b2[0] / e2[0])
                o['embaralhado_no_municipio'] = dict(dp_de_z=float(np.std(zs)), fracao_p_0_001=float(np.mean(np.abs(zs) >= 3.2905)))
        # placebo: 1º turno de 2026 contra a fração de 2022 do 2º turno
        mk = base & tem22 & (V1 >= 30)
        mod = Modelo(np.where(tem22, y22, 0)[:, None], V1, loc, mun, np.flatnonzero(mk))
        bb, ep = mod.fit(y1, S)
        o['placebo_1t_2026_controlado_por_2022'] = dict(beta=float(bb[0]), ep=float(ep[0]), z=float(bb[0] / ep[0]), n=mod.n,
                                                       tratadas_na_conta=int(S[mod.idx].sum()))
        mod = Modelo(np.column_stack([np.where(tem22, y22, 0), np.where(tem60, f60, 0)]), V1, loc, mun, np.flatnonzero(mk & tem60))
        bb, ep = mod.fit(y1, S)
        o['placebo_com_idade_ao_lado'] = dict(beta=float(bb[0]), ep=float(ep[0]), z=float(bb[0] / ep[0]), n=mod.n)
        b[nome] = o
        diz('(b)', nome, {k: ({a: round(v, 4) for a, v in vv.items() if a in ('beta', 'ep', 'z', 'beta_medio', 'fracao_p_0_001')} if isinstance(vv, dict) else vv) for k, vv in o.items()})
    res['b_urna_trocada'] = b
    res['b_meta'] = dict(linhas=int(base.sum()), com_perfil=int((base & tem60).sum()), urna_diferente=int((base & (D['b_urna_dif'] == 1)).sum()),
                         carga_depois=int((base & (D['b_carga_pos'] == 1)).sum()))
    grava('parcial_d34.json', res)
    diz('d34 pronto', round(time.time() - t0))


def modo_d34b():
    """Identifica os pares de C_exato (seções com o vetor completo idêntico) para conferência nos arquivos."""
    S = _carrega(DADOS + '/secoes2026.json.gz')
    out = {}
    for t, arq in (('2', 'meta2t.json.gz'), ('1', 'meta1t.json.gz')):
        M = _carrega(f'{D3DIR}/{arq}')
        vist = collections.defaultdict(list)
        for k in sorted(k for k in M if k in S and t in S[k]):
            v = M[k]; s = S[k][t]
            if v['junta'] != '-1' or v['enc'] in ('#NULO#', ''):
                continue
            vist[(s['comp'], s['L'], s['R'], s['B'], s['N'], int(v['biom_sh']), v['enc'], v['emi'])].append(k)
        pares = [dict(secoes=ks, comparecimento=c[0], L=c[1], R=c[2], brancos=c[3], nulos=c[4], biometria_sem_habilitacao=c[5],
                      encerramento=c[6], emissao=c[7], aptos=[S[k][t]['apt'] for k in ks], urnas=[M[k]['urna'] for k in ks],
                      locais=[M[k]['loc'] for k in ks], recebido=[M[k]['rec'] for k in ks])
                 for c, ks in vist.items() if len(ks) > 1]
        out[t + 't'] = pares
    grava('parcial_d34b.json', out)
    diz('pares identicos', json.dumps(out, ensure_ascii=False))


# ============================================================================================ relatório
def _n(x, d=2):
    if x is None or (isinstance(x, float) and not math.isfinite(x)):
        return 'n/d'
    return f'{x:,.{d}f}'.replace(',', 'X').replace('.', ',').replace('X', '.')


def _i(x):
    return _n(x, 0)


def _pc(x, d=1):
    return _n(100 * x, d) + '%'


def _le(nome):
    c = f'{TRAB}/{nome}'
    if not _os.path.exists(c):
        return None
    with open(c) as f:
        return json.load(f)


def modo_relatorio():
    import hashlib
    d11 = _le('parcial_d11.json') or _le('parcial_d11_observado.json')
    if 'calibracao' not in d11:
        d11['calibracao'] = _le('parcial_d11_calibracao.json') or {}
    if 'explicacao_inocente_plantada' not in d11:
        d11['explicacao_inocente_plantada'] = _le('parcial_d11_inocente.json') or {}
    d11b = _le('parcial_d11b.json') or {}
    d11c = _le('parcial_d11c.json') or {}
    d11d = _le('parcial_d11d.json') or {}
    d11e = _le('parcial_d11e.json') or {}
    d11f = _le('parcial_d11f.json') or {}
    d11g = _le('parcial_d11g.json') or {}
    ev = _le('parcial_ev.json') or {}
    evb = _le('parcial_evb.json') or {}
    evc = _le('parcial_evc.json') or {}
    d34 = _le('parcial_d34.json') or {}
    d34b = _le('parcial_d34b.json') or {}
    meta = _le('base_meta.json')
    obs = d11['observado']; cal = d11['calibracao']; contr = d11['contrastes']; ino = d11['explicacao_inocente_plantada']
    V = {}          # vereditos
    just = {}       # justificativa de cada veredito

    # ---------------- vereditos da PARTE 1
    def v_fatia(k):
        o = obs[k]['y']; c = cal.get(k, {}); pl = obs[k]['pl22']
        phi = o['Phi_a_favor_de_Lula']; z = abs(o['z']); zc = contr[k]['z_criterio']
        limpo = abs(pl.get('b', 0)) <= abs(o['b']) / 3
        sinal = phi >= 0.25 and z >= zc and limpo and o['regioes_mesmo_sentido'] >= 4
        ic = o['ic99_Phi_escala_maior']
        if sinal:
            return 'SINAL', 'todas as condições presentes'
        if not c.get('tem_poder_para_Phi_0_25', False):
            return 'SEM PODER', 'a calibração não enxerga Phi = 0,25 em 95% das cópias'
        if k in ('c', 'c_local'):
            return 'INCONCLUSIVO', ('pela letra, (c) só pode dar sinal ou inconclusivo; o intervalo de 99% de Phi vai de '
                                    f'{_n(ic[0], 3)} a {_n(ic[1], 3)}')
        if ic[0] >= -0.10 and ic[1] <= 0.10:
            return 'SEM SINAL', f'intervalo de 99% de Phi de {_n(ic[0], 3)} a {_n(ic[1], 3)}, dentro de -0,10 a +0,10, com poder'
        return 'INCONCLUSIVO', 'entre os limiares'

    def v_controle(k):
        o = obs[k]['y']; c = cal.get(k, {}); pl = obs[k]['pl22']
        limpo = abs(pl.get('b', 0)) <= abs(o['b']) / 3
        if abs(o['b']) >= 0.45 and abs(o['z']) >= 3.3 and limpo:
            return 'SINAL', 'todas as condições presentes'
        if not c.get('tem_poder_para_Phi_0_25', False):
            return 'SEM PODER', 'a calibração não enxerga Phi = 0,25 em 95% das cópias'
        ic = o['ic99_b']
        if ic[0] >= -0.18 and ic[1] <= 0.18:
            return 'SEM SINAL', f'intervalo de 99% de b de {_n(ic[0], 3)} a {_n(ic[1], 3)} p.p., dentro de -0,18 a +0,18, com poder'
        return 'INCONCLUSIVO', 'entre os limiares'
    for k in ('a', 'b', 'c'):
        V[f'D1.1({k})'], just[f'D1.1({k})'] = v_fatia(k)
    for k in ('d', 'e'):
        V[f'D1.1({k})'], just[f'D1.1({k})'] = v_controle(k)

    def v_varr(bloco):
        r = bloco['y']['resumo']
        if r['passam_e_repetem_em_3_UFs']:
            return 'SINAL', 'grupo com |z| de 5 ou mais repetido em 3 UFs'
        if r['n_abs_z_5'] == 0:
            return 'SEM SINAL', f"nenhum dos {r['testados']} grupos testados com |z| de 5 ou mais (maior |z| {_n(r['max_abs_z'])})"
        return 'INCONCLUSIVO', 'grupo com |z| de 5 ou mais que não se repete em 3 UFs'
    if 'f_datas_de_carga' in d11b:
        V['D1.1(f)'], just['D1.1(f)'] = v_varr(d11b['f_datas_de_carga'])
        V['D1.1(h)'], just['D1.1(h)'] = v_varr(d11b['h_faixas_de_serie'])
    g = d11b.get('g_flashcard', {}); gcal = d11b.get('g_calibracao', {})
    if g:
        gy = g['y_contra_2022']; ass = g['assimetria_y']['assimetria']
        ve = gcal.get('q_0.5', {}).get('fracao_li_99_9_acima_de_zero', 0)
        if gy['excesso'] >= 0.22 and gy['excesso_li_99_9'] > 0 and ass > 0:
            V['D1.1(g)'] = 'SINAL'; just['D1.1(g)'] = 'todas as condições presentes'
        elif ve < 0.95:
            V['D1.1(g)'] = 'SEM PODER'; just['D1.1(g)'] = 'o plantio em metade dos flashcards não é visto em 95% das cópias'
        elif gy['excesso_ls_99'] < 0.15:
            V['D1.1(g)'] = 'SEM SINAL'; just['D1.1(g)'] = 'limite superior de 99% do excesso abaixo de 0,15'
        else:
            V['D1.1(g)'] = 'INCONCLUSIVO'
            just['D1.1(g)'] = (f"excesso de {_n(gy['excesso'], 3)} p.p. ({'acima' if gy['excesso'] >= 0.22 else 'abaixo'} de 0,22), limite inferior de 99,9% "
                               f"{_n(gy['excesso_li_99_9'], 3)} ({'acima' if gy['excesso_li_99_9'] > 0 else 'não acima'} de zero), assimetria {_n(ass, 3)} "
                               f"({'a favor' if ass > 0 else 'não a favor'} de Lula), limite superior de 99% {_n(gy['excesso_ls_99'], 3)} (não abaixo de 0,15)")
    lg = d11b.get('g_logs', {})
    for ch, rot_ in (('log_c_comp', 'computador da carga'), ('log_c_user', 'usuário da carga'), ('log_m_comp', 'computador da mídia de resultado'),
                     ('log_m_user', 'usuário da mídia de resultado')):
        o = lg.get(ch)
        if not o:
            continue
        nome = f'D1.1(g) logs: {rot_}'
        if 'tau' not in o:
            V[nome] = 'SEM PODER'; just[nome] = 'sem locais com dois grupos na amostra: ' + o.get('erro', '')
            continue
        ve = o.get('plantio_q_0_5', {}).get('fracao_li_99_9_acima_de_zero', 0)
        if o['excesso'] >= 0.22 and o['excesso_li_99_9'] > 0:
            V[nome] = 'SINAL'; just[nome] = 'excesso e limite inferior presentes (assimetria não calculável com tão poucos grupos por local)'
        elif ve < 0.95:
            V[nome] = 'SEM PODER'
            just[nome] = (f"só {o['info']['locais']} locais da amostra têm dois grupos; o plantio em metade dos grupos é visto em {_pc(ve, 0)} das cópias")
        elif o['excesso_ls_99'] < 0.15:
            V[nome] = 'SEM SINAL'; just[nome] = 'limite superior de 99% do excesso abaixo de 0,15'
        else:
            V[nome] = 'INCONCLUSIVO'; just[nome] = 'entre os limiares'

    # ---------------- vereditos da PARTE 2
    bw = ev.get('bweb', {}); ecal = ev.get('calibracao', {})
    for nm, o in bw.items():
        nome = 'EV ' + nm
        cumpre = o['cumprem_mais_1_e_z4'] > 0
        if o['razao'] >= 2 and o['p'] < 0.001 and cumpre:
            V[nome] = 'SINAL'; just[nome] = 'razão, p e grupo presentes'
        elif nm.startswith('data_de_carga') and ecal.get('concentrado_em_10_por_cento_dos_votos', {}).get('fracao_SINAL_completo', 0) < 0.95:
            V[nome] = 'SEM PODER'; just[nome] = 'a concentração em 10% dos votos não é vista em 95% das cópias'
        elif o['p'] > 0.05 and o['acima_de_mais_0_5'] == 0:
            V[nome] = 'SEM SINAL'
            just[nome] = f"p = {_n(o['p'], 4)} (acima de 0,05), razão {_n(o['razao'])} e nenhum grupo de 500 seções ou mais acima de +0,5"
            if o['p'] > 0.999:
                just[nome] += ('. Ressalva: a referência deste agrupamento ficou acima do observado em todas as permutações, também no placebo de 2022; o p não informa. '
                               'Sustentam o veredito a calibração (o plantio é visto) e a ausência de grupo acima de 0,5 em módulo')
        else:
            V[nome] = 'INCONCLUSIVO'
            just[nome] = (f"razão {_n(o['razao'])} (abaixo de 2) com p = {_n(o['p'], 4)}; nenhum grupo de 500 seções; o placebo de 2022 com os mesmos grupos dá "
                          f"razão {_n(o['placebo_residuo_de_2022_com_os_grupos_de_2026']['razao'])}")
    V['EV código de carga'] = 'NÃO TESTÁVEL'; just['EV código de carga'] = 'o código de carga é único por urna e não forma grupo'
    g500 = evb.get('logs_grupos_de_500_secoes_ou_mais', {})
    for ch, o in ev.get('logs', {}).items():
        if ch.endswith('_user'):
            continue
        nome = 'EV logs: ' + o['titulo']
        gg = g500.get(ch, [])
        pw_ = (evc.get(ch) or {})
        p10 = pw_.get('10_por_cento_dos_grupos', {}).get('fracao_p_abaixo_de_0_05'); p50 = pw_.get('50_por_cento_dos_grupos', {}).get('fracao_p_abaixo_de_0_05')
        if o['razao'] >= 2 and o['p'] < 0.001 and any(x['media'] >= 1.0 and x['z'] > 4 for x in gg):
            V[nome] = 'SINAL'; just[nome] = 'razão, p e grupo presentes'
        elif p10 is not None and p10 < 0.95:
            V[nome] = 'SEM PODER'
            just[nome] = (f"razão {_n(o['razao'])}, p = {_n(o['p'], 3)}; mas um quarto da margem concentrado em 10% dos grupos só tira o p de cima de 0,05 em {_pc(p10, 0)} das cópias "
                          f"(em 50% dos grupos, {_pc(p50, 0)}), e a razão chega a 2 em {_pc(pw_['10_por_cento_dos_grupos']['fracao_razao_2'], 0)}")
        elif o['p'] > 0.05 and not any(x['media'] > 0.5 for x in gg):
            V[nome] = 'SEM SINAL'
            just[nome] = (f"p = {_n(o['p'], 3)}, razão {_n(o['razao'])}; " + (f"{len(gg)} grupo(s) de 500 seções ou mais, nenhum acima de +0,5" if gg else
                                                                               'a amostra não tem grupo de 500 seções'))
        else:
            V[nome] = 'INCONCLUSIVO'; just[nome] = f"p = {_n(o['p'], 3)}, razão {_n(o['razao'])}"
    # ---------------- vereditos da PARTE 3
    if d34:
        ce = d34['a_censo']; cx = d34['a_C_exato']['2t']; cv = d34['a_C_votos']
        fora = ce['2']['urna_repetida_fora_de_junta'] or ce['2']['carga_repetida_fora_de_junta'] or ce['1']['urna_repetida_fora_de_junta'] or ce['1']['carga_repetida_fora_de_junta']
        s1 = bool(fora); s2 = cx['C_exato'] >= 3 and cx['C_exato'] > cx['p99_9']
        s3 = cv['razao_2026_sobre_o_maior_placebo'] >= 1.25 and cv['excesso_sobre_o_maior_placebo'] >= 3000
        V['D3-4(a) censo de urna e carga repetidas'] = 'SINAL' if s1 else 'SEM SINAL'
        just['D3-4(a) censo de urna e carga repetidas'] = ('repetição fora das seções de junta' if s1 else
                                                           'nenhuma urna e nenhuma carga repetida fora das seções de junta, nos dois turnos (contagem exata)')
        nome = 'D3-4(a) C_exato (vetor completo idêntico)'
        if s2:
            V[nome] = 'SINAL'; just[nome] = 'C_exato de 3 ou mais e acima do percentil 99,9'
        elif not d34['a_C_exato']['poder_copia_de_5']['todos_iguais_a_5']:
            V[nome] = 'SEM PODER'; just[nome] = 'a cópia plantada de 5 seções não aumenta C_exato em 5'
        elif cx['C_exato'] <= cx['p95']:
            V[nome] = 'SEM SINAL'
            just[nome] = (f"C_exato = {cx['C_exato']}, dentro do percentil 95 das permutações ({_n(cx['p95'], 0)}); a cópia plantada de 5 seções sobe a contagem em 5")
        else:
            V[nome] = 'INCONCLUSIVO'; just[nome] = 'C_exato entre os percentis 95 e 99,9'
        nome = 'D3-4(a) rho (votos idênticos contra reamostragem)'
        r26 = cv['por_conjunto']['2026_2t']
        precisa = 1.25 * cv['maior_rho_dos_placebos_do_registro'] * r26['media_reamostrada'] - r26['C_votos']
        cv['pares_a_mais_para_passar_o_limiar'] = precisa
        if s3:
            V[nome] = 'SINAL'; just[nome] = 'rho 25% acima do maior placebo com excesso de 3.000 pares'
        elif cv['poder_copia_de_3000']['fracao_que_passa_o_limiar'] < 0.95:
            V[nome] = 'SEM PODER'
            just[nome] = (f"a cópia plantada de 3.000 seções não passa o limiar (rho vai de {_n(r26['rho'], 3)} a {_n(cv['poder_copia_de_3000']['rho_medio'], 3)}; o limiar pede "
                          f"{_n(1.25 * cv['maior_rho_dos_placebos_do_registro'], 3)}, cerca de {_i(precisa)} pares a mais). O observado fica abaixo dos dois placebos do registro")
        elif cv['razao_2026_sobre_o_maior_placebo'] <= 1.25:
            V[nome] = 'SEM SINAL'; just[nome] = 'rho dentro de 25% dos placebos'
        else:
            V[nome] = 'INCONCLUSIVO'; just[nome] = 'rho acima dos placebos com excesso menor que 3.000'
        for nm, rot_ in (('urna_diferente', 'urna diferente'), ('carga_depois_de_04_10', 'carga depois de 04/10')):
            o = d34['b_urna_trocada'][nm]; pr = o['principal_com_idade']; pl = o['placebo_1t_2026_controlado_por_2022']
            nome = f'D3-4(b) {rot_}'
            if pr['beta'] >= 1.0 and pr['p'] < 0.001 and abs(pl['beta']) < 0.3:
                V[nome] = 'SINAL'; just[nome] = 'beta, p e placebo presentes'
            else:
                pw = o.get('poder_mais_1_8') or {}
                if pw.get('fracao_p_0_001', 0) < 0.95:
                    V[nome] = 'SEM PODER'; just[nome] = 'o plantio de 1,8 ponto não é visto em 95% das cópias'
                elif (pr['p'] < 0.001 and abs(pr['beta']) < 1) or abs(pl['beta']) > 0.3:
                    V[nome] = 'INCONCLUSIVO'
                    just[nome] = (f"beta = {_n(pr['beta'], 3)} com p = {_n(pr['p'], 4)}; placebo {_n(pl['beta'], 3)}")
                elif pr['ic95'][0] >= -1 and pr['ic95'][1] <= 1:
                    V[nome] = 'SEM SINAL'
                    just[nome] = (f"intervalo de 95% de beta de {_n(pr['ic95'][0], 3)} a {_n(pr['ic95'][1], 3)}, dentro de -1 a +1; placebo "
                                  f"{_n(pl['beta'], 3)} (ep {_n(pl['ep'], 3)})")
                else:
                    V[nome] = 'INCONCLUSIVO'; just[nome] = 'intervalo mais largo que o limite'
    res = dict(teste='R27_B1: carga, lote, flashcard e zona', gerado_em=time.strftime('%Y-%m-%d %H:%M:%S UTC', time.gmtime()),
               registro=dict(adendo_27='commit 2748895, 10/11/2026 00:16:42 UTC', adendo_28='commit 938be19, 10/11/2026 04:36:33 UTC',
                             pecas=['D1.1 de desenho_D1_proposta.json', 'fragilidade F9, L2 e T20 de equipe_vermelha_relatorio.json', 'D3-4 de desenho_D3_proposta.json']),
               docstring_antes_de_rodar=open(TRAB + '/docstring_antes_de_rodar.sha256').read().strip(),
               vereditos=V, justificativas=just, base=meta,
               parte1_D1_1=dict(primeira_metade=d11, segunda_metade=d11b, sensibilidade_do_erro=d11c, exploratorio_flashcard=d11d, exploratorio_flashcard_ruido=d11f, exploratorio_comparecimento=d11e, lista_de_flashcards_extremos=d11g),
               parte2_equipe_vermelha=dict(principal=ev, complementos_exploratorios=evb, poder_na_amostra_de_logs=evc),
               parte3_D3_4=dict(principal=d34, pares_identicos=d34b))
    cont = collections.Counter(V.values())
    res['contagem_de_clausulas'] = dict(cont)
    L = []
    A = L.append
    A('R27_B1: CARGA, LOTE, FLASHCARD E ZONA (Adendo 27, Onda B, item B1)')
    A('')
    A('Registro: Adendo 27 (commit 2748895, 10/11/2026 00:16:42 UTC) e Adendo 28 (commit 938be19). Três peças: D1.1 do desenho cego D1')
    A('(modelo, lote, carga e flashcard dentro do mesmo prédio), o reteste da equipe vermelha para F9, L2 e T20 (desenho entre zonas, sem')
    A('efeito fixo de local) e D3-4 do desenho cego D3 (identidade da urna e boletins repetidos). O reteste da equipe vermelha foi escrito')
    A('por quem conhecia os resultados antigos; os dois desenhos são cegos.')
    A('Decisões que o registro não fixa: no docstring de scripts/analisar_R27_B1.py, gravado antes de qualquer conta com votos')
    A(f"({res['docstring_antes_de_rodar']}).")
    A('Este teste ainda não foi refeito por conferente independente: pelo Adendo 27, nenhum veredito daqui conta como indício antes disso.')
    A('')
    tetos = [obs[k]['y']['teto99_votos_de_margem'] / MARGEM for k in ('a', 'b', 'd', 'e')]
    A('RESUMO')
    A(f"1. Nenhuma das {len(V)} cláusulas deu SINAL. Onde a peça tem poder (vê um décimo da margem em 100% das cópias plantadas), modelo de urna dentro da")
    A('   família, lote de fabricação, data de carga, carga tardia, urna trocada entre os turnos, grupo de carga da zona e boletim repetido não')
    A(f"   mostram nada: os tetos de 99% dos contrastes ficam entre {_pc(min(tetos))} e {_pc(max(tetos))} da margem.")
    if g:
        A(f"2. Inconclusivos: o flashcard (variância entre flashcards dentro do prédio acima da de 2022 por {_n(g['y_contra_2022']['excesso'], 3)} p.p., sem passar no limite de 99,9%")
        A(f"   e sem direção; teto de {_pc(0.25 * g['y_contra_2022']['excesso_ls_99'] / 0.446)} da margem pela letra, e sem excesso nas contas exploratórias) e a família de urna nova contra antiga (só comparável")
        A('   em SP). Sem poder: computador da mídia (dentro do prédio e entre zonas na amostra de logs) e a cláusula rho de boletins repetidos.')
    A('3. Para o indício do comparecimento da Onda A: a calibração mostra que a peça veria abstenção localizada num tipo de urna ou numa carga tanto')
    A('   quanto veria troca de voto. Não viu. A leitura com fraude perde a forma "lote de urnas ou leva de cargas" e fica restrita a algo igual em')
    A('   todas as urnas ou feito na mesa, que esta peça não enxerga.')
    A('')
    A('VEREDITOS PELA LETRA')
    for k, v in V.items():
        A(f'  {k}: {v}. {just.get(k, "")}')
    A(f"  Contagem: {', '.join(f'{v} {k}' for k, v in cont.items())}, em {len(V)} cláusulas. Nenhuma tem limiar em que o acaso daria sinal com frequência")
    A('  (z de 3,3 a 5; p de 0,001): o esperado por acaso é menos de 0,1 sinal no conjunto.')
    A('')
    # ---------------- Parte 1
    m = d11['meta']
    A('PARTE 1. D1.1: MODELO, LOTE, CARGA E FLASHCARD DENTRO DO MESMO PRÉDIO')
    A(f"Universo U: {_i(m['U'])} seções (2º turno pareado com o 1º, L2 + R2 de 30 ou mais, sem exterior e sem junta); {_i(m['sem_perfil'])} sem perfil do")
    A(f"eleitorado ficam fora das regressões. Modelos em U: UE2013 {_i(m['modelos_em_U']['UE2013'])}, UE2015 {_i(m['modelos_em_U']['UE2015'])}, UE2020 "
      f"{_i(m['modelos_em_U']['UE2020'])}, UE2022 {_i(m['modelos_em_U']['UE2022'])}.")
    A(f"Carga depois de 04/10: {_i(m['carga_pos_em_U'])} seções; urna diferente da do 1º turno: {_i(m['urna_dif_em_U'])}.")
    cf = d11.get('conferencia_fe_ols')
    if cf:
        A(f"Conferência da regressão própria contra lib.fe_ols (SE, erro pelo local): b {_n(cf['b_proprio'], 6)} e {_n(cf['b_lib'], 6)}; erro {_n(cf['ep_proprio'], 6)} e {_n(cf['ep_lib'], 6)}.")
    A('')
    A('Contrastes (y = 100 x L2/(L2+R2); b em pontos percentuais; erro agrupado por município)')
    nomes = {'a': '(a) UE2022 contra UE2020, locais mistos', 'b': '(b) UE2015 contra UE2013, locais mistos', 'c': '(c) família nova contra antiga, zona e município',
             'c_local': '(c) conferência com efeito fixo de local', 'd': '(d) carga depois de 04/10', 'e': '(e) urna diferente da do 1º turno'}
    for k in ('a', 'b', 'c', 'c_local', 'd', 'e'):
        o = obs[k]['y']; c = contr[k]; sl = d11c.get(k, {}).get('y', {})
        A(f"  {nomes[k]}")
        A(f"    b = {_n(o['b'], 4)} (ep {_n(o['ep'], 4)}; z {_n(o['z'])}); n = {_i(o['n'])} seções, {_i(o['grupos_onde_D_varia'])} grupos onde o atributo varia "
          f"({_i(o['secoes_em_grupos_onde_D_varia'])} seções, {_i(o['secoes_D1_nesses_grupos'])} com D = 1), {_i(o['municipios'])} municípios."
          + (f" Erro por local: {_n(sl.get('ep_por_local'), 4)}; municípios onde varia: {_i(sl.get('municipios_onde_D_varia'))}"
             + (f" (UFs: {', '.join(sl.get('ufs_onde_D_varia', []))})" if len(sl.get('ufs_onde_D_varia', [])) <= 6 else f" ({len(sl.get('ufs_onde_D_varia', []))} UFs)") + '.' if sl else ''))
        if c['tipo'] == 'fatia':
            A(f"    Tamanho de referência: b = {_n(c['b_de_Phi_1'])} p.p. zeraria a margem (Phi = 1). Phi a favor de Lula = {_n(o['Phi_a_favor_de_Lula'], 4)} "
              f"({o['classe_que_teria_a_alteracao_a_favor_de_Lula']}); intervalo de 99% de Phi na escala da classe maior: {_n(o['ic99_Phi_escala_maior'][0], 4)} a "
              f"{_n(o['ic99_Phi_escala_maior'][1], 4)}.")
        else:
            A(f"    Phi = menos b / 1,785 = {_n(o['Phi'], 4)}; intervalo de 99% de b: {_n(o['ic99_b'][0], 4)} a {_n(o['ic99_b'][1], 4)} p.p. (limites do registro: 0,45 para sinal, 0,18 para sem sinal).")
        A(f"    Em votos de margem: {_i(o['votos_de_margem'])}; teto do intervalo de 99%: {_i(o['teto99_votos_de_margem'])} ({_pc(o['teto99_votos_de_margem'] / MARGEM)} da margem).")
        rg = d11c.get(k, {}).get('y', {}).get('regioes_erro_por_local') or {}
        if rg:
            A('    Regiões (b; z com erro por local; municípios onde o atributo varia): ' + '; '.join(
                f"{r_} {_n(x['b'], 3)} (z {_n(x['z_por_local'], 1)}; {x['municipios_onde_D_varia']})" if 'b' in x else f'{r_} sem variação' for r_, x in rg.items())
              + f". Mesmo sentido do nacional em {o['regioes_mesmo_sentido']} de {o['regioes_com_estimativa']}.")
        ou = []
        for sp_, rt in (('pl22', 'virada de 2022'), ('pl18', 'virada de 2018'), ('plturno', '1º turno de 2026 com referência em 2022'), ('gov', 'governador do 2º turno, 6 UFs')):
            x = obs[k].get(sp_, {})
            if 'b' in x:
                e2 = d11c.get(k, {}).get(sp_, {})
                extra = ''
                if sp_ == 'gov' and e2:
                    extra = f"; erro por local {_n(e2.get('ep_por_local'), 3)}; municípios onde varia: {e2.get('municipios_onde_D_varia')}"
                ou.append(f"{rt} {_n(x['b'], 4)} (ep {_n(x['ep'], 4)}; n {_i(x['n'])}{extra})")
            else:
                ou.append(f'{rt} sem estimativa')
        A('    Placebos (mesmo D de 2026, onde não deveria dar nada): ' + '; '.join(ou) + '.')
        x = obs[k]['yBN']; x2 = obs[k]['yalt']
        A(f"    y_BN: b = {_n(x['b'], 4)} (ep {_n(x['ep'], 4)}), Phi_BN = {_n(x['Phi_BN'], 4)} ({_i(x['votos_de_margem'])} votos de margem). "
          f"y_alt (contra 2022): b = {_n(x2['b'], 4)} (ep {_n(x2['ep'], 4)}; n {_i(x2['n'])}).")
        c_ = cal.get(k)
        if c_:
            pp = c_['plantios']
            A('    Calibração (200 cópias por tamanho): poder ' + ', '.join(f"Phi {str(ph).replace('.', ',')}: {_pc(pp[f'R_para_L_Phi_{ph}']['poder_pi'], 0)}" for ph in (0.1, 0.25, 0.5, 1.0))
              + f"; recuperação em Phi = 0,25: {_n(pp['R_para_L_Phi_0.25']['recuperacao'], 3)} (viés {_pc(pp['R_para_L_Phi_0.25']['vies'])}); espelho (plantio a favor de Flávio) visto em "
              f"{_pc(pp['L_para_R_espelho_Phi_0.25']['poder_pi'], 0)}; atributo embaralhado no município: {_pc(c_['embaralhado_no_municipio']['falso_sinal'])} de falso sinal, desvio-padrão de z "
              f"{_n(c_['embaralhado_no_municipio']['dp_de_z'])}.")
        i1 = ino.get('abstencao_pura_uniforme_3_6_por_cento', {}).get(k); i2 = ino.get('abstencao_pura_localizada_mesmo_efeito_na_margem_que_Phi_0_25', {}).get(k)
        if i1:
            t_ = f"    Explicação inocente plantada: abstenção pura uniforme (3,6% dos votos de Flávio em toda seção) desloca b em {_n(i1['incremento_medio'], 4)} (z médio {_n(i1['z_medio_do_incremento'])})"
            if i2:
                t_ += (f"; abstenção pura só nas urnas expostas, com o mesmo efeito na margem que Phi = 0,25, desloca b em {_n(i2['incremento_medio_b'], 4)}, "
                       f"{_pc(i2['razao_sobre_a_troca'], 0)} do que a troca daria, e é vista em {_pc(i2['fracao_vista'], 0)} das cópias")
            A(t_ + '.')
    dj = d11.get('d_e_juntos'); mt = d11.get('modelos_todo_U_ref_UE2020')
    if dj:
        A(f"  (d) e (e) na mesma regressão: carga tardia {_n(dj['b_carga_pos'], 4)} (ep {_n(dj['ep_carga_pos'], 4)}); urna diferente {_n(dj['b_urna_dif'], 4)} (ep {_n(dj['ep_urna_dif'], 4)}).")
    if mt:
        A('  Todo U com indicadoras de modelo (referência UE2020): ' + '; '.join(f"{k_} {_n(v_['b'], 4)} (ep {_n(v_['ep'], 4)})" for k_, v_ in mt.items()) + '.')
    an = d11.get('placebo_de_ano_2022', {})
    if an:
        A('  Placebo de ano (modelos de 2022 na virada de 2022): ' + '; '.join(f"{k_}: {_n(v_['b'], 4)} (ep {_n(v_['ep'], 4)})" for k_, v_ in an.items() if isinstance(v_, dict) and 'b' in v_) + '.')
    A('')
    if 'f_datas_de_carga' in d11b:
        for ch, tit in (('f_datas_de_carga', '(f) Datas de carga (dia), uma por vez contra as outras no mesmo local'), ('h_faixas_de_serie', '(h) Faixas de 5.000 números de série dentro do modelo')):
            A('  ' + tit)
            for sp_ in ('y', 'yBN', 'yalt'):
                r = d11b[ch][sp_]['resumo']
                A(f"    {sp_}: {r['testados']} grupos testados de {r['grupos']}; maior |z| = {_n(r['max_abs_z'])} (o acaso daria perto de {_n(r['z_esperado_do_maximo_sob_acaso'])}); "
                  f"com |z| de 3 ou mais: {r['n_abs_z_3']}; de 5 ou mais: {r['n_abs_z_5']}; desvio-padrão dos z: {_n(r['dp_dos_z'])}; positivos {r['positivos']}, negativos {r['negativos']}.")
            r = d11b[ch]['y']['resumo']
            A('    Maiores em y: ' + '; '.join(f"{x['grupo']} b {_n(x['b'], 3)} z {_n(x['z'])} ({_i(x['secoes'])} seções, Phi {_n(x['Phi_do_grupo'], 4)})" for x in r['maiores'][:4]) + '.')
            A(f"    Poder por fórmula: o deslocamento que daria z = 5 tem mediana de {_n(r['deslocamento_z5_mediana_pp'], 3)} p.p.; em Phi do grupo, mediana {_n(r['Phi_que_daria_z5_mediana'], 4)} e máximo "
              f"{_n(r['Phi_que_daria_z5_maximo'], 4)}: nenhuma data ou faixa isolada poderia esconder 1% da margem sem passar de z = 5.")
        cfp = d11b.get('f_h_plantio_de_conferencia', {})
        if cfp:
            A('    Plantio de conferência: ' + '; '.join(f"{k_}: grupo {v_['grupo']} ({_i(v_['secoes'])} seções), Phi plantado {_n(v_['Phi_plantado'], 3)}, z médio {_n(v_['z_medio_com_plantio'], 1)}, visto em {_pc(v_['fracao_z5'], 0)}" for k_, v_ in cfp.items()) + '.')
        A('')
    if g:
        gy = g['y_contra_2022']; g18 = g['y_contra_2018']; gu = g['y_todo_U']
        A('  (g) Flashcard de carga: componente de variância entre flashcards dentro do local (tau, p.p.)')
        A(f"    2026 nas seções com par em 2022 ({_i(gy['info']['locais'])} locais com os dois tipos de par, {_i(gy['info']['secoes'])} seções): tau = {_n(gy['tau'], 3)} "
          f"(tau2 {_n(gy['tau2'], 4)}, ep {_n(gy['ep_tau2'], 4)}). Placebo de 2022 com os flashcards de 2026: tau = {_n(gy['tau_placebo'], 3)} (tau2 {_n(gy['tau2_placebo'], 4)}, ep {_n(gy['ep_tau2_placebo'], 4)}).")
        A(f"    Excesso sobre 2022 = {_n(gy['excesso'], 3)} p.p. (limiar de sinal 0,22); limite inferior de 99,9% = {_n(gy['excesso_li_99_9'], 3)}; limite superior de 99% = {_n(gy['excesso_ls_99'], 3)} "
          f"(limiar de sem sinal 0,15); intervalo de 95%: {_n(gy['excesso_ic95'][0], 3)} a {_n(gy['excesso_ic95'][1], 3)}.")
        A(f"    Placebo de 2018 (ao lado): tau de 2018 = {_n(g18['tau_placebo'], 3)} contra {_n(g18['tau'], 3)} de 2026 nas mesmas seções; excesso de 2026 sobre 2018 = {_n(g18['excesso'], 3)} (negativo: 2018 tem mais).")
        A(f"    2026 em todo U: tau = {_n(gu['tau'], 3)} (tau2 {_n(gu['tau2'], 4)}, ep {_n(gu['ep_tau2'], 4)}). Sem o desconto binomial: 2026 {_n(gy['tau_sem_desconto_binomial'], 3)}, 2022 "
          f"{_n(gy['tau_placebo_sem_desconto_binomial'], 3)}: sem o desconto os dois anos ficam iguais, e o excesso depende inteiro dele.")
        a1 = g['assimetria_y']; a2 = g['assimetria_placebo_2022']
        A(f"    Assimetria das médias por flashcard ({_i(a1['n_grupos'])} flashcards): {_n(a1['assimetria'], 3)} em 2026 ({a1['acima_de_3']} acima de +3 e {a1['abaixo_de_menos_3']} abaixo de -3); "
          f"no placebo de 2022, {_n(a2['assimetria'], 3)} ({a2['acima_de_3']} e {a2['abaixo_de_menos_3']}). Sem cauda para um lado.")
        gb = g['yBN_contra_2022']; ga = g['yalt']
        A(f"    y_BN: tau = {_n(gb['tau'], 3)} em 2026 e {_n(gb['tau_placebo'], 3)} em 2022 (excesso {_n(gb['excesso'], 3)}). y_alt: tau = {_n(ga['tau'], 3)} (sem placebo próprio).")
        if gcal:
            A('    Calibração (um quarto da margem em fração q dos flashcards, 200 cópias): ' + '; '.join(
                f"q = {k_[2:].replace('.', ',')}: excesso médio {_n(v_['excesso_medio'], 3)}, limite de 99,9% acima de zero em {_pc(v_['fracao_li_99_9_acima_de_zero'], 0)}, "
                f"assimetria positiva em {_pc(v_['fracao_assimetria_positiva'], 0)}, regra completa em {_pc(v_['fracao_SINAL_completo'], 0)}" for k_, v_ in gcal.items() if k_.startswith('q_')) + '.')
            A('    Com q = 0,8 a cauda fica do lado contrário (a minoria é que fica sem o efeito): a exigência de assimetria a favor de Lula impede a regra de enxergar efeito presente na maioria dos flashcards.')
            nu = gcal.get('nulo_rotulos_embaralhados_no_local')
            if nu:
                A(f"    Nulo (rótulos embaralhados dentro do local, 200 vezes): tau2 médio {_n(nu['tau2_medio'], 4)} (dp {_n(nu['dp_tau2'], 4)}); o observado em todo U ({_n(nu['tau2_observado'], 4)}) fica a "
                  f"{_n(nu['z_do_observado'])} desvios, p = {_n(nu['p'], 3)}.")
        A(f"    Em votos: se o tau de 2026 inteiro fosse efeito de carga concentrado em metade dos flashcards, valeria {_pc(0.25 * gy['tau'] / 0.446)} da margem "
          f"({_i(0.25 * gy['tau'] / 0.446 * MARGEM)} votos); pelo limite superior de 99% do excesso, {_pc(0.25 * gy['excesso_ls_99'] / 0.446)} ({_i(0.25 * gy['excesso_ls_99'] / 0.446 * MARGEM)}).")
        if d11d:
            t = d11d.get('tau_no_conjunto_comum', {}); vz = d11d.get('pares_vizinhos', {})
            A('    EXPLORATÓRIO (feito depois de ver o resultado acima; não entra no veredito):')
            if vz:
                A(f"      Pares de seções vizinhas na numeração do mesmo local ({_i(vz['y_2026']['info']['pares_vizinhos_total'])} pares; {_pc(vz['y_2026']['info']['fracao_de_pares_vizinhos_com_o_mesmo_flashcard'])} com o mesmo flashcard): "
                  f"tau de 2026 = {_n(vz['y_2026']['tau'], 3)} (z {_n(vz['y_2026']['z'])}); de 2022 = {_n(vz['placebo_2022']['tau'], 3)} (z {_n(vz['placebo_2022']['z'])}); "
                  f"excesso = {_n(vz['excesso_y_2026_sobre_placebo_2022']['excesso'], 3)} (z {_n(vz['excesso_y_2026_sobre_placebo_2022']['z'])}). "
                  f"2018: {_n(vz['placebo_2018']['tau'], 3)} (z {_n(vz['placebo_2018']['z'])}) contra {_n(vz['y_2026_no_conjunto_de_2018']['tau'], 3)} de 2026 nas mesmas seções.")
            if t:
                A(f"      O mesmo tau com o desfecho do 1º turno de 2026 (referência 2022) e os flashcards do 2º turno: {_n(t['turno_1t_2026_ref_2022']['tau'], 3)} (z {_n(t['turno_1t_2026_ref_2022']['z'])}), "
                  f"contra {_n(t['y_2026']['tau'], 3)} do 2º turno nas mesmas seções.")
                A(f"      Variação do comparecimento entre os turnos (y_T): tau de 2026 = {_n(t['yT_2026']['tau'], 3)} (z {_n(t['yT_2026']['z'])}); de 2022 = {_n(t['yT_2022']['tau'], 3)} (z {_n(t['yT_2022']['z'])}); "
                  f"excesso = {_n(t['excesso_yT_2026_sobre_yT_2022']['excesso'], 3)} (z {_n(t['excesso_yT_2026_sobre_yT_2022']['z'])}).")
            if d11f:
                x = d11f['2026_contra_2022']; a_ = x['residuo_padronizado_pelo_tamanho']; b_ = x['locais_de_secoes_de_tamanho_parecido']
                x8 = d11f['2026_contra_2018']['residuo_padronizado_pelo_tamanho']
                A(f"      Sem depender do desconto binomial: com o resíduo padronizado pelo tamanho da seção, tau de 2026 = {_n(a_['tau_a'], 3)} (tau2 {_n(a_['tau2_a'], 4)}, ep {_n(a_['ep_a'], 4)}) e de 2022 = {_n(a_['tau_b'], 3)} "
                  f"(tau2 {_n(a_['tau2_b'], 4)}, ep {_n(a_['ep_b'], 4)}); excesso = {_n(a_['excesso'], 3)} (z {_n(a_['z_excesso'])}). Só nos {_i(b_['locais'])} locais de seções de tamanho parecido, com desconto: "
                  f"{_n(b_['tau_a'], 3)} e {_n(b_['tau_b'], 3)}; excesso = {_n(b_['excesso'], 3)} (z {_n(b_['z_excesso'])}). Contra 2018, padronizado: {_n(x8['tau_a'], 3)} e {_n(x8['tau_b'], 3)} (z {_n(x8['z_excesso'])}).")
            if d11g:
                A('      Flashcards mais afastados (lista de conferência, não teste; média do resíduo, seções, zona): a favor de Lula '
                  + '; '.join(f"{x['flashcard']} {_n(x['media_do_residuo'], 2)} ({x['secoes_em_locais_com_2_flashcards']}; {x['uf_municipio_zona'][0]})" for x in d11g['a_favor_de_Lula'][:5])
                  + '; a favor de Flávio ' + '; '.join(f"{x['flashcard']} {_n(x['media_do_residuo'], 2)} ({x['secoes_em_locais_com_2_flashcards']}; {x['uf_municipio_zona'][0]})" for x in d11g['a_favor_de_Flavio'][:5]) + '.')
            pr = d11d.get('tau_por_UF_e_regiao', {})
            if pr:
                A('      Por região (tau de 2026; tau de 2022; z do excesso): ' + '; '.join(f"{k_} {_n(v_['tau_2026'], 2)}; {_n(v_['tau_2022'], 2)}; {_n(v_['z_excesso'], 1)}" for k_, v_ in pr['regiao'].items()) + '.')
                ufz = sorted(pr['UF'].items(), key=lambda x: -x[1]['z_excesso'])
                A('      UFs com maior z do excesso: ' + '; '.join(f"{k_} tau {_n(v_['tau_2026'], 2)} contra {_n(v_['tau_2022'], 2)} (z {_n(v_['z_excesso'], 1)})" for k_, v_ in ufz[:6])
                  + '. PI, MA, TO, PB e CE (as UFs do indício da Onda A): ' + '; '.join(f"{u} {_n(pr['UF'][u]['tau_2026'], 2)} contra {_n(pr['UF'][u]['tau_2022'], 2)} (z {_n(pr['UF'][u]['z_excesso'], 1)})" for u in ('PI', 'MA', 'TO', 'PB', 'CE') if u in pr['UF']) + '.')
        A('')
    if lg:
        lm = d11b.get('logs_meta', {})
        A(f"  (g) na amostra de logs ({_i(lm.get('logs_em_U', 0))} seções da amostra antiga, não aleatória): computador e usuário das mídias")
        for ch, o in lg.items():
            if 'tau' in o:
                A(f"    {o['titulo']}: {o['grupos']} grupos; locais da amostra com dois grupos: {o['info']['locais']} ({_i(o['info']['secoes'])} seções); tau = {_n(o['tau'], 3)}, placebo de 2022 {_n(o['tau_placebo'], 3)}, "
                  f"excesso {_n(o['excesso'], 3)} (99,9% inferior {_n(o['excesso_li_99_9'], 3)}; 99% superior {_n(o['excesso_ls_99'], 3)}); plantio em metade dos grupos visto em "
                  f"{_pc(o.get('plantio_q_0_5', {}).get('fracao_li_99_9_acima_de_zero', 0), 0)} das cópias.")
            else:
                A(f"    {o['titulo']}: {o.get('grupos')} grupos; sem estimativa ({o.get('erro', '')}).")
        A('    Como a equipe vermelha previu, quase todo local usa um computador só: dentro do prédio este agrupamento não tem como ser testado. O desenho entre zonas está na Parte 2.')
        A('')
    # exploratório A9
    A('  EXPLORATÓRIO declarado antes (A9), fora do veredito: os mesmos contrastes sem o controle da variação da abstenção e na variação do comparecimento')
    for k in ('a', 'b', 'c', 'd', 'e'):
        x = obs[k]['ysd']; t_ = obs[k]['yT']; sl = d11c.get(k, {}).get('yT', {})
        A(f"    {nomes[k]}: y sem o controle {_n(x['b'], 4)} (ep {_n(x['ep'], 4)}); y_T = {_n(t_['b'], 4)} p.p. dos aptos (ep {_n(t_['ep'], 4)}; z {_n(t_['z'])}"
          + (f"; z com erro por local {_n(sl.get('z_por_local'))}" if sl else '') + f"), ou {_i(t_['eleitores_a_mais_nas_D1'])} eleitores nas urnas D = 1"
          + (f". A mesma conta na variação do comparecimento de 2022 (exploratório posterior): {_n(d11e[k]['plT22']['b'], 4)} (z {_n(d11e[k]['plT22']['z_por_municipio'])})." if d11e.get(k) else '.'))
    if d11e:
        for k in ('b', 'c', 'd'):
            pu = d11e[k]['yT'].get('por_UF', {})
            if pu:
                A(f"    y_T de {nomes[k]} por UF (b; z com erro por local; UFs com 10 ou mais grupos onde varia): " + '; '.join(f"{u} {_n(x['b'], 2)} ({_n(x['z'], 1)})" for u, x in sorted(pu.items(), key=lambda kv: kv[1]['z'])) + '.')
    A('')
    # ---------------- Parte 2
    if bw:
        rs = ev['residuo']
        A('PARTE 2. EQUIPE VERMELHA (F9, L2, T20): DESENHO ENTRE ZONAS, SEM EFEITO FIXO DE LOCAL')
        A(f"Resíduo de um modelo por UF com a composição completa do 1º turno ({_i(rs['secoes'])} seções; desvio-padrão ponderado {_n(rs['dp_ponderado'])} p.p.; em 2022, {_n(rs['dp_ponderado_2022'])}).")
        for nm, o in bw.items():
            pl = o['placebo_residuo_de_2022_com_os_grupos_de_2026']
            A(f"  {nm}: {_i(o['grupos'])} grupos, {_i(o['celulas'])} células; T = {_n(o['T'], 4)} p.p.2 (raiz {_n(math.sqrt(o['T']), 3)} p.p.); média das permutações {_n(o['T_medio_permutado'], 4)}; "
              f"razão {_n(o['razao'], 3)}; p = {_n(o['p'], 4)}. Placebo (resíduo de 2022, grupos de 2026): razão {_n(pl['razao'], 3)}, p = {_n(pl['p'], 4)}.")
            if o['grupos_500']:
                A(f"    Grupos de 500 seções ou mais: {o['grupos_500']}; com +1,0 ou mais a mais de 4 ep: {o['cumprem_mais_1_e_z4']} (espelho, -1,0: {o['espelho_cumprem_menos_1_e_z4']}); acima de +0,5: "
                  f"{o['acima_de_mais_0_5']} (abaixo de -0,5: {o['espelho_abaixo_de_menos_0_5']}).")
                A('    Maiores a favor de Lula: ' + '; '.join(f"{x['grupo']} {_n(x['media'], 3)} (z {_n(x['z'], 1)}; {_i(x['secoes'])} seções em {x['zonas_ou_celulas']} zonas)" for x in o['maiores_a_favor_de_Lula'][:4]) + '.')
                A('    Maiores a favor de Flávio: ' + '; '.join(f"{x['grupo']} {_n(x['media'], 3)} (z {_n(x['z'], 1)}; {_i(x['secoes'])} seções em {x['zonas_ou_celulas']} zonas)" for x in o['maiores_a_favor_de_Flavio'][:4]) + '.')
        A('    Código de carga (CD_CARGA_1): único por urna, não forma grupo; não testável por variância entre grupos.')
        if ecal:
            A('  Calibração do agrupamento principal (100 cópias, 1.999 permutações): ' + '; '.join(
                f"{k_.replace('_', ' ')}: deslocamento {_n(v_['deslocamento_plantado_pp'])} p.p., razão média {_n(v_['razao_media'], 1)}, p < 0,001 em {_pc(v_['fracao_p_0_001'], 0)}, grupo que cumpre em "
                f"{_pc(v_['fracao_com_grupo_que_cumpre'], 0)}, regra completa em {_pc(v_['fracao_SINAL_completo'], 0)}" for k_, v_ in ecal.items()) + '.')
        cb = evb.get('calibracao_dos_dois_agrupamentos', {})
        if cb:
            A('  EXPLORATÓRIO (depois de ver a primeira saída): a referência do agrupamento principal ficou acima do observado em todas as permutações, em 2026 e em 2022. Ela embaralha rótulos')
            A('  entre células de tamanhos muito diferentes e por isso não reproduz "agrupamentos do mesmo tamanho": o p de 1,0000 não é evidência de nada. A variante declarada antes como "ao lado"')
            A('  (dia modal da zona, que permuta zonas inteiras) não tem esse defeito. Calibração das duas nas mesmas cópias (um quarto da margem):')
            for k_, v_ in cb.items():
                a_, b_ = v_['principal_UF_x_dia'], v_['dia_modal_da_zona']
                A(f"    {k_.replace('_', ' ')}: principal com razão de 2 ou mais em {_pc(a_['fracao_razao_2'], 0)}, p mínimo em {_pc(a_['fracao_p_minimo'], 0)}, escaparia como sem sinal em {_pc(a_['fracao_que_escaparia_como_SEM_SINAL'], 0)}; "
                  f"dia modal com razão de 2 ou mais em {_pc(b_['fracao_razao_2'], 0)}, p mínimo em {_pc(b_['fracao_p_minimo'], 0)}, escaparia em {_pc(b_['fracao_que_escaparia_como_SEM_SINAL'], 0)}.")
        if ev.get('logs'):
            A(f"  Amostra de logs ({_i(next(iter(ev['logs'].values()))['secoes'])} seções; grupo x zona como célula, UF como estrato)")
            for ch, o in ev['logs'].items():
                pl = o['placebo_residuo_de_2022']
                A(f"    {o['titulo']}: {o['grupos']} grupos; razão {_n(o['razao'], 3)}; p = {_n(o['p'], 3)} (placebo de 2022: razão {_n(pl['razao'], 3)}, p = {_n(pl['p'], 3)}). Grupos de 10 seções ou mais com +1,0 e z acima de 4: "
                  f"{o['cumprem_mais_1_e_z4']}; espelho: {o['espelho_cumprem_menos_1_e_z4']}; no placebo: {pl['cumprem_mais_1_e_z4']} e {pl['espelho_cumprem_menos_1_e_z4']}.")
            o = ev['logs']['log_m_comp']
            A('    Maiores grupos de computador da mídia de resultado (erro por seção quando o grupo tem uma zona só, o que exagera o z): a favor de Lula '
              + '; '.join(f"{x['grupo']} {_n(x['media'], 2)} ({x['secoes']} seções, {_i(x['votos_de_margem_se_fosse_irregularidade'])} votos de margem)" for x in o['maiores_a_favor_de_Lula'][:3])
              + '; a favor de Flávio ' + '; '.join(f"{x['grupo']} {_n(x['media'], 2)} ({x['secoes']} seções)" for x in o['maiores_a_favor_de_Flavio'][:3]) + '.')
            for ch, gg in g500.items():
                if gg:
                    A(f"    Grupos de 500 seções ou mais em {ev['logs'][ch]['titulo']}: " + '; '.join(f"{x['grupo']} {_n(x['media'], 3)} (ep {_n(x['ep'], 3)}; {x['secoes']} seções em {x['zonas']} zonas)" for x in gg) + '.')
            if evc:
                A('    Poder na amostra (um quarto da margem concentrado em 10% e em 50% dos grupos; fração das cópias com p abaixo de 0,05, e com razão de 2 ou mais no caso de 10%): '
                  + '; '.join(f"{ev['logs'][k_]['titulo']}: {_pc(v_['10_por_cento_dos_grupos']['fracao_p_abaixo_de_0_05'], 0)} e {_pc(v_['50_por_cento_dos_grupos']['fracao_p_abaixo_de_0_05'], 0)} (razão: {_pc(v_['10_por_cento_dos_grupos']['fracao_razao_2'], 0)})" for k_, v_ in evc.items()) + '.')
            mr = evb.get('midia_de_resultado_gerada_de_16_10_em_diante', {})
            if mr:
                x = mr['amostra_inteira']
                A(f"    Coincidência citada pela equipe vermelha (mídia gerada de 16 a 24/10 em AM e MA), exploratório: na amostra, {x['secoes_tarde']} seções em {x.get('zonas_tarde')} zonas têm mídia de resultado gerada de 16/10 em diante; "
                  f"resíduo médio {_n(x.get('media_tarde'), 3)} contra {_n(x.get('media_cedo'), 3)} das demais; diferença {_n(x.get('diferenca'), 3)} (ep {_n(x.get('ep'), 3)}; z {_n(x.get('z'))}). "
                  + '; '.join(f"{u}: {mr[u].get('secoes_tarde')} seções tardias, diferença {_n(mr[u].get('diferenca'), 3)} (ep {_n(mr[u].get('ep'), 3)})" for u in ('AM', 'MA', 'AM_e_MA')) + '.')
        A('')
    # ---------------- Parte 3
    if d34:
        ce = d34['a_censo']; cx = d34['a_C_exato']; cv = d34['a_C_votos']
        A('PARTE 3. D3-4: IDENTIDADE DA URNA E BOLETINS REPETIDOS')
        for t in ('2', '1'):
            c = ce[t]
            A(f"  (a) Censo do {t}º turno ({_i(c['secoes'])} seções): números de urna repetidos {json.dumps(c['urnas_repetidas'])}; códigos de carga repetidos {len(c['cargas_repetidas'])}; seções de junta {c['secoes_de_junta']}; "
              f"seções em urna repetida {c['secoes_em_urna_repetida']}; fora de junta: {len(c['urna_repetida_fora_de_junta'])} de urna e {len(c['carga_repetida_fora_de_junta'])} de carga.")
        x = cx['2t']
        A(f"  (a) C_exato (vetor completo idêntico) no 2º turno: {x['C_exato']} par em {_i(x['secoes'])} seções ({_i(x['secoes_com_vetor_de_votos_e_biometria_repetido'])} seções têm votos e biometria iguais aos de outra); "
          f"1.000 permutações dos horários dentro da UF: média {_n(x['media_permutada'], 3)}, percentil 95 = {_n(x['p95'], 0)}, percentil 99,9 = {_n(x['p99_9'], 0)}, máximo {_n(x['max_permutado'], 0)}. No 1º turno: {cx['1t_ao_lado']['C_exato']}.")
        for pz in d34b.get('2t', []):
            A(f"      O par: {pz['secoes'][0]} e {pz['secoes'][1]} (comparecimento {pz['comparecimento']}, Lula {pz['L']}, Flávio {pz['R']}, brancos {pz['brancos']}, nulos {pz['nulos']}, biometria sem habilitação {pz['biometria_sem_habilitacao']}, "
              f"encerramento {pz['encerramento'][11:]}, emissão {pz['emissao'][11:]}); urnas {pz['urnas'][0]} e {pz['urnas'][1]}, aptos {pz['aptos'][0]} e {pz['aptos'][1]}: são urnas diferentes em estados diferentes.")
        A(f"      Poder: copiar o vetor de 5 seções para outras 5 aumentou C_exato em {sorted(set(cx['poder_copia_de_5']['aumentos']))} nas 20 repetições.")
        A('  (a) C_votos (comparecimento, 13, 22, brancos e nulos idênticos, seções com 50 votos ou mais) e rho = C_votos / média de 200 reamostragens multinomiais')
        for k_, v_ in cv['por_conjunto'].items():
            A(f"      {k_.replace('_', ' ')}: C_votos {_i(v_['C_votos'])}; média reamostrada {_i(v_['media_reamostrada'])}; rho = {_n(v_['rho'], 3)} ({_i(v_['secoes'])} seções).")
        A(f"      2026 no 2º turno sobre o maior placebo do registro (2º turno de 2022 e 1º de 2026): razão {_n(cv['razao_2026_sobre_o_maior_placebo'], 3)} (sinal pede 1,25 ou mais); excesso sobre o maior placebo: "
          f"{_i(cv['excesso_sobre_o_maior_placebo'])} pares (sinal pede 3.000 ou mais).")
        pw = cv['poder_copia_de_3000']
        A(f"      Poder: copiar os votos de 3.000 seções grandes para outras 3.000 leva rho a {_n(pw['rho_medio'], 3)} (razão {_n(pw['razao_media_sobre_o_maior_placebo'], 3)}; excesso {_i(pw['excesso_medio'])}); passa o limiar em "
          f"{_pc(pw['fracao_que_passa_o_limiar'], 0)} das repetições (razão de 1,25 em {_pc(pw['fracao_razao_1_25'], 0)}; excesso de 3.000 em {_pc(pw['fracao_excesso_3000'], 0)}).")
        A(f"      Para passar o limiar seriam precisos cerca de {_i(cv.get('pares_a_mais_para_passar_o_limiar'))} pares a mais: a cláusula só enxerga cópia de dezenas de milhares de boletins. "
          f"C_votos menos a média reamostrada de 2026: {_i(cv['por_conjunto']['2026_2t']['excesso_sobre_a_media'])} pares (leitura alternativa do excesso; todos os anos têm excesso desse tipo).")
        bm = d34['b_meta']
        A(f"  (b) Urna trocada e carga tardia contra as vizinhas do mesmo local ({_i(bm['linhas'])} seções com 30 válidos nos dois turnos; {_i(bm['com_perfil'])} com perfil; {_i(bm['urna_diferente'])} com urna diferente; {_i(bm['carga_depois'])} com carga tardia)")
        for nm, rot_ in (('urna_diferente', 'urna diferente entre os turnos'), ('carga_depois_de_04_10', 'carga depois de 04/10')):
            o = d34['b_urna_trocada'][nm]; pr = o['principal_com_idade']; s2 = o['sem_idade_com_exterior']; pl = o['placebo_1t_2026_controlado_por_2022']
            A(f"      {rot_}: beta = {_n(pr['beta'], 4)} (ep {_n(pr['ep'], 4)}; p = {_n(pr['p'], 3)}; n {_i(pr['n'])}; {_i(pr['tratadas_em_locais_com_comparacao'])} tratadas com vizinha de comparação); intervalo de 95%: "
              f"{_n(pr['ic95'][0], 3)} a {_n(pr['ic95'][1], 3)}. Sem a idade e com o exterior: {_n(s2['beta'], 4)} (ep {_n(s2['ep'], 4)}).")
            A(f"        Margem implicada: {_i(pr['margem_implicada'])} votos; teto de 95%: {_i(pr['margem_implicada_teto_95'])} ({_pc(pr['margem_implicada_teto_95'] / MARGEM, 2)} da margem). Placebo (1º turno de 2026 contra 2022): "
              f"{_n(pl['beta'], 4)} (ep {_n(pl['ep'], 4)}).")
            pw = pr.get('poder_mais_1_8'); es = pr.get('espelho_menos_1_8'); em = pr.get('embaralhado_no_municipio')
            if pw is None:
                pw = o.get('poder_mais_1_8'); es = o.get('espelho_menos_1_8'); em = o.get('embaralhado_no_municipio')
            if pw:
                A(f"        Poder: com 1,8 ponto plantado, beta médio {_n(pw['beta_medio'], 3)}, p < 0,001 em {_pc(pw['fracao_p_0_001'], 0)} das 200 cópias; espelho (a favor de Flávio): {_n(es['beta_medio'], 3)}, visto em {_pc(es['fracao_p_0_001'], 0)}; "
                  f"tratamento embaralhado no município: desvio-padrão de z {_n(em['dp_de_z'])}, p < 0,001 em {_pc(em['fracao_p_0_001'])}.")
        A('')
    res['texto_auxiliar'] = None
    with open(TRAB + '/relatorio_corpo.txt', 'w') as f:
        f.write('\n'.join(L) + '\n')
    leitura = TRAB + '/leitura.txt'
    corpo = '\n'.join(L) + '\n'
    if _os.path.exists(leitura):
        corpo += open(leitura).read()
    assert chr(0x2014) not in corpo and chr(0x2013) not in corpo
    with open(SAIDA_TXT, 'w') as f:
        f.write(corpo)
    if _os.path.exists(TRAB + '/leitura.json'):
        res['leitura'] = json.load(open(TRAB + '/leitura.json'))
    del res['texto_auxiliar']
    with open(SAIDA_JSON, 'w') as f:
        json.dump(res, f, ensure_ascii=False, indent=1, default=_json_padrao)
    hs = {a: hashlib.sha256(open(a, 'rb').read()).hexdigest() for a in (SAIDA_JSON, SAIDA_TXT, __file__)}
    with open(TRAB + '/sha256_finais.json', 'w') as f:
        json.dump(hs, f, indent=1)
    diz('relatório gravado', json.dumps(V, ensure_ascii=False))


def principal():
    # Modos do registro: logs, gov, base, d11 (ou d11a e d11b), ev, d34, relatorio.
    # Modos acrescentados depois de ver resultado (exploratórios ou de sensibilidade): d11c, d11d, d11e, d11f, d11g, evb, evc, d34b.
    modo = sys.argv[1] if len(sys.argv) > 1 else ''
    _os.makedirs(TRAB, exist_ok=True)
    if modo == 'logs':
        modo_logs()
    elif modo == 'gov':
        modo_gov()
    elif modo == 'base':
        modo_base()
    elif modo == 'd11':
        modo_d11(); modo_d11b()
    elif modo == 'd11a':
        modo_d11()
    elif modo == 'd11b':
        modo_d11b()
    elif modo == 'd11c':
        modo_d11c()
    elif modo == 'd11g':
        modo_d11g()
    elif modo == 'd11f':
        modo_d11f()
    elif modo == 'd11e':
        modo_d11e()
    elif modo == 'd11d':
        modo_d11d()
    elif modo == 'ev':
        modo_ev()
    elif modo == 'evb':
        modo_evb()
    elif modo == 'evc':
        modo_evc()
    elif modo == 'd34':
        modo_d34()
    elif modo == 'd34b':
        modo_d34b()
    elif modo == 'relatorio':
        modo_relatorio()
    else:
        print(__doc__)


if __name__ == '__main__':
    principal()
