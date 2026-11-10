"""R27_B5: JANELAS DA TOTALIZAÇÃO.

Adendo 27 do pré-registro (commit 2748895, 10/11/2026 00:16:42 UTC), Onda B, item B5, mantido pelo Adendo 28 (commit
938be19, 10/11/2026 04:36:33 UTC). Quatro peças, com o critério de cada uma valendo como escrito no registro:
  PARTE 1  D3-5 de registro/adendo27/desenho_D3_proposta.json por inteiro (a retenção das 17:08 às 19:03).
  PARTE 2  D3-6 do mesmo arquivo por inteiro (pausa das 19:48, ordem de chegada e boletins fora de hora).
  PARTE 3  D3-2, só a parte que não pede milhares de requisições: bweb contra o histórico oficial da totalização
           publicado em 03/11 (dl_hist2t e dl_hist1t) e os .sha512 dos zips do bweb. O JSON oficial por município e
           o aux.json da amostra antiga NÃO rodam nesta onda, e por isso o veredito da parte 3 vale só para o que
           rodou.
  PARTE 4  Alegações novas R1, R7 e R8 de registro/adendo27/novidades_relatorio.json, cada uma ao pé da letra, com o
           número que a alegação prevê.
Os grupos de tratamento são os congelados pelo desenhista em desenho_D3/grupos_2t.json.gz (SHA-256 do arquivo
e1c741a3f3672b9a8a951a23133213b941ba3ca928f8632beb6798aa884d8ec8, conferido aqui antes de qualquer conta).
Aviso do registro: o D3 é desenho cego. As alegações R1, R7 e R8 não têm critério no registro: os critérios delas
estão escritos abaixo, antes de calcular, e saem no resultado como desvio.

Este docstring foi escrito ANTES de qualquer conta com votos. Até aqui só foi lida estrutura sem voto: os grupos
congelados, os metadados do bweb (meta1t e meta2t do desenhista), a hora e a contagem de seções de cada passo do
histórico da totalização (sem as colunas de voto) e a distribuição dos horários de encerramento. O que o registro
não fixa está em DECISÕES e sai no resultado como desvio. O que for feito depois de ver resultado sai marcado como
exploratório.

Uso:
  python3 -I scripts/analisar_R27_B5.py base       monta a base por seção em R27_B5/
  python3 -I scripts/analisar_R27_B5.py sha        baixa os 56 .sha512 de hoje (1 por segundo) e confere os zips
  python3 -I scripts/analisar_R27_B5.py hist       PARTE 3 (bweb contra o histórico, dois turnos)
  python3 -I scripts/analisar_R27_B5.py d35        PARTE 1
  python3 -I scripts/analisar_R27_B5.py d36        PARTE 2
  python3 -I scripts/analisar_R27_B5.py r1 | r7 | r8   PARTE 4
  python3 -I scripts/analisar_R27_B5.py relatorio  junta os parciais em resultados/R27_B5_janelas_da_totalizacao.*
Trabalho e parciais: /home/user/trabalho-eleicao/adendo27/R27_B5/

O QUE O REGISTRO FIXA (aplicado à letra)
D3-5. y = fatia de Lula nos válidos do 2º turno, em pontos. Regressão de D3-4 (b): controles do 1º turno por
candidato, brancos e nulos, variação do comparecimento, log dos aptos, idade; peso = válidos do 2º turno; erro
agrupado por município. Tratamento E = 1 para seção recebida antes da retenção (cedo). Fora: exterior, seções de
junta e prorrogadas. A, mesmo prédio: só os locais mistos, efeito fixo de local e do minuto de emissão. B, gêmeas de
canal: cedo contra rajada das 19:03, efeito fixo de zona e do minuto de emissão. C: cedo contra todas as tardias da
mesma zona que emitiram antes das 17:08. A hipótese prevê beta_E negativo. Margem implicada = 2 x (-beta_E) x válidos
recebidos depois da retenção. SINAL: beta_E de -0,45 ou mais negativo com p < 0,001 em A, e de -0,45 ou mais negativo
com p < 0,01 em B, com os placebos abaixo de 0,15 em módulo; alcance pleno se o intervalo de 95% incluir -1,79.
SEM SINAL: limite inferior do intervalo de 95% acima de -0,90 em A e em B (sem sinal forte: acima de -0,45 nos dois).
INCONCLUSIVO: sinais opostos em A e B; significância só numa das duas; placebo de 0,15 ou mais; erro padrão acima de
0,45 (declarado antes de olhar o coeficiente). Poder: mover x% dos válidos do 22 para o 13 em toda seção recebida de
19:03 em diante, x = 0,45; 0,90; 1,79. Placebos: (1) fatia de Lula no 1º turno de 2026 controlada pela fatia do 2º
turno de 2022; (2) rajada das 19:03 contra recebidas de 19:05 a 19:30 da mesma zona; (3) 1º turno: primeiras seções
recebidas de cada zona contra as seguintes.
D3-6. r = fatia de Lula nos válidos do 2º turno menos o previsto por uma regressão no país inteiro com os controles
de D3-4 (b) e efeito fixo de zona, sem variável de tempo. (1) Descontinuidade: variável de corrida = segundos do
recebimento até o corte (19:48:00 de um lado, 19:50:00 do outro), regressão linear local de cada lado, núcleo
triangular, banda de 8 minutos (4 e 16 de robustez), peso = válidos, erro por zona; tau = salto. (2) Inclinação: r
contra a posição do recebimento dentro da zona (0 a 1), efeito fixo de zona, sem prorrogadas; theta. (3) Deslocados:
regressão de D3-4 (b) com tratamento desloc >= 30 minutos (também >= 60, e cauda), efeito fixo de local. Margem:
(1) 2 x tau x válidos recebidos a partir de 19:50; (2) theta x válidos totais; (3) 2 x beta x válidos dos
deslocados. SINAL: (1) tau de +0,45 ou mais com p < 0,001 na banda de 8, mesmo sinal com p < 0,01 nas bandas de 4 e
16, maior em módulo que todos os cortes falsos, salto do desfecho placebo abaixo de 0,15; (2) theta de +0,9 ou mais
com p < 0,001 e theta placebo abaixo de 0,3; (3) beta de +1,0 ou mais com p < 0,001 e placebo abaixo de 0,3 (sinal
local). SEM SINAL: intervalo de 95% de tau entre -0,45 e +0,45; de theta entre -0,9 e +0,9; de beta entre -1,0 e
+1,0. INCONCLUSIVO: desfecho placebo com salto de 0,15 ou mais no mesmo corte; tau significativo mas menor que algum
corte falso; resultado que muda de sinal entre bandas. Degraus de vazão (19:12, 19:14, 19:18, 19:24, 19:30, 20:00):
exploratórios, só contam com p < 0,001/6. Poder: +0,45; +0,9; +2,1 pontos em toda seção recebida a partir de 19:50;
rampa de 0 a 0,9; 1,8; 3,6 pela ordem de chegada; +5 pontos nos deslocados. Placebos: desfecho anterior (1º turno
controlado por 2022) nos três estimadores; cortes falsos de 5 em 5 minutos entre 19:55 e 21:05, pulando 10 minutos
em volta dos cortes registrados; as pausas do 1º turno com o desfecho do 1º turno controlado por 2022.
D3-2 (parte rodada). Censo: d(u, c) = soma das seções do bweb em u menos o valor oficial, para 13, 22, branco, nulo,
comparecimento e aptos. SINAL: qualquer unidade com d diferente de zero para o 13 ou o 22, ou total nacional
diferente; com alcance se |d líquido| nacional passar de 443.019. SEM SINAL: diferença zero em todas as unidades,
zips iguais aos resumos publicados. Poder: plantar numa cópia (1) 1 voto a mais para o 13 em 1 seção; (2) retirar 1
seção inteira; (3) trocar 10 votos entre dois municípios da mesma UF. Placebo: a mesma conciliação no 1º turno.

DECISÕES QUE O REGISTRO NÃO FIXA (tomadas aqui, antes de calcular qualquer coisa com votos)
Gerais
G1. Zona = UF, município e zona (é a definição que reproduz as 274 zonas com cedo e rajada, 1.027 e 4.009 seções,
    citadas no desenho; com ela as janelas da pausa dão 1.216 zonas com os dois lados, e não as 1.255 do texto do
    desenho: fica dito). Município = UF mais código. Local = UF, município, zona e local do 2º turno.
G2. Universo das regressões: seções do 2º turno no Brasil (sem o exterior), sem junta apuradora, pareadas com o 1º
    turno pela chave, com 30 válidos ou mais nos dois turnos (válidos do 1º turno = comparecimento menos brancos e
    nulos; do 2º = L + R) e com perfil do eleitorado. Seção sem perfil sai (contagem dita).
G3. Controles de D3-4 (b), como o teste B1 (decisão T2) já aplicou: frações do 13, do 22 e de cada outro candidato
    com 1% ou mais do comparecimento nacional do 1º turno (calculado no script), de brancos e de nulos, todas sobre
    o comparecimento do 1º turno; (comparecimento do 2º menos o do 1º) / aptos do 2º; ln dos aptos do 2º turno;
    fração de eleitores de 60 anos ou mais no perfil (extração R27_A6/perfil_secao_2026_A6.json.gz, sem voto; seção
    com agregadas soma a principal com as agregadas). Ao lado, a regressão principal sem a idade.
G4. Regressão: mínimos quadrados ponderados com transformação dentro dos efeitos fixos (um efeito: médias; dois:
    projeções alternadas até 1e-10), erro agrupado CR1 por município, p bilateral pela normal, intervalo de 95% =
    1,96 erro. Grupo de efeito fixo com uma só observação sai (de forma iterada quando são dois efeitos).
G5. Plantios: troca = T ~ Binomial(L2 + R2, x/100), limitado a R2, sai de R e entra em L. Explicações inocentes:
    entrada de eleitores reais = N ~ Binomial(L2 + R2, 2x/100) eleitores novos, todos de Lula (L2 e comparecimento
    sobem); abstenção pura = N ~ Binomial(R2, min(1, 2x (L2 + R2) / (100 R2))) eleitores de Flávio a menos (R2 e
    comparecimento caem). As duas têm o mesmo efeito na margem que a troca de x%. Com elas o controle da variação do
    comparecimento é refeito. "O teste distingue" se o incremento do coeficiente sob a explicação inocente for menor
    que a metade do incremento sob a troca de mesmo efeito na margem. Semente 20261110.
G6. Ordem do veredito de cada parte: SINAL se todas as condições do critério estiverem presentes; senão SEM PODER se
    a calibração não enxergar o tamanho que o registro indica; senão INCONCLUSIVO se alguma cláusula de inconclusivo
    do registro valer, lida ao pé da letra; senão SEM SINAL se couber no critério; senão INCONCLUSIVO. As cláusulas
    "sinais opostos em A e B" e "muda de sinal entre bandas" são lidas pela letra (sinal da estimativa pontual, sem
    exigir significância); quando o veredito for inconclusivo só por elas, o resultado diz ao lado se os limites
    numéricos de SEM SINAL estão cumpridos. Espelho: as mesmas condições com o sinal trocado (a favor de Flávio).

Parte 1 (D3-5)
R1. Tardia = ret "rajada" ou "depois". Local misto = local com pelo menos uma seção cedo e uma tardia entre as
    seções do Brasil sem junta e sem prorrogação (pela estrutura: 468 locais, 722 e 3.154 seções). Minuto de emissão
    = parte inteira de emi (minutos de Brasília) dos grupos congelados.
    A: seções do universo G2, não prorrogadas, em locais mistos; efeito fixo de local e de minuto de emissão.
    B: seções cedo ou rajada do universo, não prorrogadas; efeito fixo de zona e de minuto de emissão.
    C: cedo contra tardias com emissão antes de 17:08:00 de Brasília; efeito fixo de zona (letra); ao lado, com o
    minuto de emissão. C não entra no critério (o registro só cita A e B).
R2. Margem implicada = 2 x (-beta_E) / 100 x válidos de todas as seções recebidas depois da retenção (exterior
    incluído, valor exato do bweb).
R3. Placebo (1): desfecho 100 x L1 / (L1 + R1) do 1º turno de 2026; único controle = 100 x L / (L + R) do 2º turno
    de 2022 na mesma chave (letra, como no B1); mesma amostra, tratamento e efeitos fixos de A e de B; peso L1 + R1;
    só seções com par em 2022 e 30 votos dos dois ou mais em cada ano. Placebo (2): rajada (tratamento) contra
    seções recebidas de 19:05:00 a 19:30:59 da mesma zona; y, controles e efeitos de B. Placebo (3): no 1º turno,
    tratamento = seção recebida nos três primeiros minutos do recebimento (17:08:00 a 17:10:59, o análogo dos três
    minutos de 17:05 a 17:07 do 2º turno) contra as seguintes da mesma zona com emissão antes de 17:11:00 de
    Brasília; desfecho 100 x L1 / (L1 + R1), controle = fatia de 2022, efeito fixo de zona e de minuto de emissão
    do 1º turno, peso L1 + R1; fora exterior, junta e seções que encerraram às 18:30 ou depois no 1º turno.
    "Placebos abaixo de 0,15 em módulo" = os quatro coeficientes: (1) em A, (1) em B, (2) e (3).
R4. Calibração: 200 cópias para cada x (0,45; 0,90; 1,79), troca em toda seção tardia. Devolução = média de
    (beta da cópia menos beta observado), a comparar com -x. Detecção = fração das cópias em que o incremento
    dividido pelo erro da cópia passa do z do critério (3,2905 em A, 2,5758 em B) no sentido plantado. Efeito
    mínimo detectável com 80% de poder = (z do critério + 0,8416) x erro. SEM PODER se o erro de A ou de B passar de
    0,45 (o registro chama de inconclusivo declarado antes de olhar o coeficiente; fica dito assim) ou se a troca de
    1,79 não for detectada em 95% das cópias em A e em B. Espelho: a mesma troca de L para R com x = 0,45 e 1,79.
    Explicações inocentes (G5) com x = 1,79 nas tardias, 100 cópias cada.
    Significância na cláusula "só numa das duas" = p abaixo do limiar do critério de cada comparação (0,001 em A;
    0,01 em B).

Parte 2 (D3-6)
S1. Resíduo r: uma regressão ponderada (peso L2 + R2) no universo G2 inteiro (com as prorrogadas no ajuste), y
    contra os controles G3 com efeito fixo de zona; r = y menos o ajustado. Os três estimadores excluem as
    prorrogadas (o texto do desenho as exclui em (2) e na explicação inocente). O exterior fica fora (sem perfil).
S2. (1) À esquerda x = recebimento menos 19:48:00 (segundos, negativo), à direita x = recebimento menos 19:50:00;
    núcleo K = 1 - |x| / h; mínimos quadrados de r em constante, D, x e D x, peso (L2 + R2) K, erro por zona (letra;
    por município ao lado). Margem = 2 x tau / 100 x válidos de todas as seções recebidas de 19:50:00 em diante.
    Cortes falsos: a grade do registro (de 5 em 5 minutos de 19:55 a 21:05) tem 15 pontos, não 20; pulando os que
    ficam a menos de 10 minutos de um corte registrado (19:48, 19:50 e o degrau das 20:00) sobram 12 (20:10 a
    21:05): é o conjunto principal. Ao lado, um conjunto de 20 cortes de 3 em 3 minutos de 20:08 a 21:05. Corte
    falso em c: x = recebimento menos c dos dois lados, banda de 8.
    Desfecho placebo: r_p = resíduo de 100 x L1 / (L1 + R1) contra a fatia de 2022 com efeito fixo de zona (peso
    L1 + R1), nas seções com par em 2022; mesma descontinuidade no corte de 19:48.
    1º turno: r_p com a hora de recebimento do 1º turno, nas três pausas vistas nos metadados (limites pelos
    minutos sem nenhum recebimento: 18:02:00 e 18:08:00; 18:50:00 e 18:53:00; 19:32:00 e 19:59:00; o desenho dizia
    19:32 a 19:54), banda de 8; fora exterior, junta e seções que encerraram às 18:30 ou depois no 1º turno.
    Degraus de vazão: mesma conta com banda de 8 e de 2 minutos, só exploratório.
S3. (2) Posição = (ordem do recebimento dentro da zona menos 1) / (seções da zona menos 1), entre todas as seções
    do bweb do 2º turno da zona, empates pela média. Regressão de r na posição com efeito fixo de zona, peso
    L2 + R2, erro por município (por zona ao lado). Margem = theta / 100 x válidos totais. Placebo: r_p no lugar de
    r. Rampas plantadas: (a) pela ordem nacional de chegada, u = (ordem entre as 499.205 seções menos 1) / 499.204,
    T ~ Binomial(L2 + R2, x u / 100); (b) pela posição dentro da zona, T ~ Binomial(L2 + R2, x pos / 100); x = 0,9;
    1,8; 3,6; 100 cópias cada, com o resíduo refeito. SEM PODER para a rampa nacional se a de 3,6 (a margem
    inteira) não devolver theta de +0,9 ou mais com p < 0,001 em 95% das cópias; o fator de devolução (theta
    devolvido / x) é relatado para as duas formas.
S4. (3) Regressão G3 com efeito fixo de local, tratamento desloc >= 30 (principal), desloc >= 60 e cauda; amostra =
    universo sem prorrogadas. Margem = 2 x beta / 100 x válidos de todas as seções do grupo no bweb. Placebo: 100 x
    L1 / (L1 + R1) contra a fatia de 2022, efeito fixo de local, mesmo tratamento. Ao lado, com o controle do
    encerramento (minutos de Brasília depois das 17:00). Plantio: troca de 5% nos deslocados, 200 cópias.
S5. Calibração de (1): 100 cópias para cada tamanho (0,45; 0,9; 2,1), troca em toda seção recebida de 19:50:00 em
    diante, resíduo refeito; detecção = incremento / erro acima de 3,2905 na banda de 8 e de 2,5758 nas de 4 e 16.
    SEM PODER se o plantio de 0,45 não for detectado em 95% das cópias na banda de 8. Espelho: troca de L para R de
    0,45. Explicações inocentes: (i) composição: troca de 2,1% em todas as seções das zonas cuja mediana de
    recebimento é 19:50:00 ou depois, qualquer que seja a hora da seção (o salto não pode responder); (ii) entrada
    de eleitores reais e (iii) abstenção pura (G5) com x = 2,1 nas seções recebidas de 19:50:00 em diante.

Parte 3 (D3-2, bweb contra o histórico e .sha512)
H1. Fontes. 2º turno: votos, comparecimento, aptos e DT_BU_RECEBIDO lidos de novo, aqui, direto dos 28 zips do bweb
    (cargo 1); a base dados/secoes2026.json.gz é conferida contra essa leitura. 1º turno: votos por candidato de
    dados/candidatos2026_1t.json.gz e brancos, nulos, comparecimento e aptos de dados/secoes2026.json.gz (extraídos
    do bweb e conferidos campo a campo no Adendo 25), com a hora de recebimento do meta1t do desenhista.
    Pela estrutura, a coluna QT_APTOS_TOT do histórico traz o comparecimento das seções do passo, e não os aptos
    (o LEIAME do TSE diz aptos): é tratada como comparecimento, e isso sai como ponto a explicar.
H2. Conferências, todas exatas:
    (a) fim: em cada município e zona, o último acumulado do histórico (13, 22, brancos, nulos, comparecimento e
        seções) menos a soma dos boletins do bweb; o mesmo por município, por UF e no país; soma dos passos igual ao
        último acumulado; QT_APTOS_ZONA contra os aptos do bweb.
    (b) ordem: em cada zona e passo, seções totalizadas até o passo não podem passar das seções com DT_BU_RECEBIDO
        até a hora do passo (boletim somado antes de recebido); nenhum boletim recebido fica sem passo.
    (c) passo a passo: dentro da zona os boletins entram nos passos pela ordem de DT_BU_RECEBIDO (empate pelo número
        da seção). O passo fecha se (13, 22, brancos, nulos, comparecimento) do passo for igual à soma do bloco.
        Onde a ordem estrita não fecha: procura-se o menor trecho de passos consecutivos cujo conjunto fecha (troca
        de ordem dentro do trecho) e, dentro do trecho, uma atribuição exata por busca. Conta-se: passos que fecham
        na ordem, passos que fecham com outra ordem, passos sem atribuição possível.
    (d) série nacional por minuto: acumulado do histórico por minuto de totalização contra o acumulado do bweb por
        minuto de DT_BU_RECEBIDO: o primeiro nunca pode passar o segundo (13, 22, brancos, nulos, seções); "bate" =
        (c) fecha em todos os passos, isto é, a série do histórico é a dos boletins na hora do passo de cada um.
        Ao lado: a defasagem entre recebimento e totalização e a maior fila.
    SINAL (letra do D3-2 levada ao histórico): alguma unidade com d diferente de zero para o 13 ou o 22, total
    nacional diferente, boletim somado antes de recebido, passo sem atribuição possível, ou zip diferente do resumo;
    com alcance se |d líquido| nacional passar de 443.019. SEM SINAL na parte rodada: tudo zero. Diferença só em
    aptos ou em contagem de seções: INCONCLUSIVO (letra).
H3. Plantios, 20 sorteios cada, numa cópia do bweb do 2º turno: (1) 1 voto a mais para o 13 em 1 seção (tem de
    apontar exatamente 1 zona, 1 município, 1 UF e o país); (2) retirar 1 seção; (3) trocar 10 votos do 13 entre
    dois municípios da mesma UF (a UF fecha, os municípios não); (4) fora do registro: trocar a hora de recebimento
    de duas seções de passos diferentes da mesma zona (a conferência (b) ou a (c) tem de acusar). Inocente: (5)
    trocar a hora de duas seções do mesmo passo (nada pode acusar).
H4. .sha512: SHA-512 de cada um dos 56 zips locais contra o .sha512 baixado junto com o zip (26 e 28/10) e contra o
    .sha512 que o repositório serve hoje (56 pedidos pequenos a cdn.tse.jus.br, 1 por segundo, parando em 429).
H5. Universo, sem requisição: seções da configuração do site (desenho_D3/cs_2t) que não estão no bweb, e os
    números QT_SECOES_BRASIL e QT_APTOS_BRASIL do histórico contra o bweb. Só descritivo.

Parte 4 (alegações)
Q1. R1, "um voto transferido a cada dez segundos depois das 17h01". d = segundos entre 17:01:00 de Brasília e o
    encerramento da seção (zero se encerrou antes); a alegação prevê T = d / 10 votos passados de Flávio para Lula.
    Universo G2 COM as prorrogadas (são a dose maior). Contas:
    (a) aritmética: soma de T no país (o total que a alegação prevê) contra a margem e contra os votos de Flávio;
        seções em que T passa dos votos que Lula teve (impossível se a alegação valesse) e soma do excesso.
    (b) dose: y contra dose = 100 x T / (L2 + R2), controles G3, efeito fixo de local, peso L2 + R2, erro por
        município. kappa = 1 se a alegação vale, 0 se o horário não transfere nada. Principal: seções que
        encerraram antes de 17:10:00 (97% das seções; T de até 54 votos). Ao lado: todas, com a dose limitada a 50
        pontos. Margem implicada = 2 x kappa x soma de T das seções da conta principal.
    (c) dez grupos por horário de encerramento, com cortes fixados pela distribuição sem voto: antes de 17:01;
        17:01; 17:02; 17:03 a 17:04; 17:05 a 17:09; 17:10 a 17:19; 17:20 a 17:39; 17:40 a 18:29; 18:30 a 18:59;
        19:00 em diante. Por grupo: seções, T médio previsto, fatia bruta dos dois turnos, e a diferença ajustada
        contra o primeiro grupo (indicadoras de grupo, controles G3, efeito fixo de local) ao lado da diferença que a
        alegação prevê. Ao lado: decis do encerramento.
    Critério (meu, não do registro): a alegação AO PÉ DA LETRA fica refutada se o limite superior de 95% de kappa
    ficar abaixo de 0,5 e confirmada se o inferior ficar acima de 0,5. Efeito do horário com alcance: SINAL se kappa
    for positivo com p < 0,001, o limite inferior de 95% da margem implicada for de 443.019 ou mais (10% da margem,
    a régua do D3) e o placebo (desfecho do 1º turno controlado por 2022, mesma dose) ficar abaixo de um terço do
    kappa; SEM SINAL se o limite superior de 95% da margem implicada ficar abaixo de 443.019; senão INCONCLUSIVO.
    Calibração: plantar a própria alegação (T = d / 10, limitado a R2) e versões de 1 voto a cada 100 s e a cada
    1.000 s; o teste tem de devolver kappa perto de 1; 0,1; 0,01. Espelho: a mesma transferência de Lula para
    Flávio. Inocente: fila real (d / 100 eleitores novos repartidos como a seção: nada pode aparecer) e entrada de
    eleitores reais de Lula (d / 100 eleitores novos, todos de Lula, com o comparecimento subindo).
Q2. R7, "cadê os 165.699 votos": a tela mostra Lula 193.574 e Flávio 142.169 no país. Com o histórico, ordenando os
    passos por hora e identificador: (a) existe instante com esse acumulado exato? quantas seções? (b) a soma das
    páginas dos estados seria 193.574 - 165.699 = 27.875: existe instante anterior com Lula = 27.875, ou conjunto
    de UFs (27 mais exterior) cujos votos de Lula no instante da tela somam exatamente 165.699 (busca exaustiva)?
    (c) no fim, total nacional de Lula menos a soma das UFs no bweb e no histórico. A alegação prevê 165.699 votos
    de Lula sem seção de origem; SEM SINAL se (c) for zero e nenhum passo do histórico tiver voto fora de zona.
Q3. R8, "Flávio tinha tendência de vitória com 30% apurado". (a) Fato: fatia de Flávio no acumulado com 23%, 30% e
    38% das seções e às 20:00 e 20:15, e os instantes de troca de liderança, pelo histórico. (b) Composição: nas
    primeiras 30% das seções pela ordem de recebimento, a fatia de Flávio no 2º turno menos a final do país (g2) e
    a fatia dos dois no 1º turno, nas mesmas seções, menos a do país (g1). Se a parcial era representativa, g1 = 0;
    se a ordem de chegada explica, g1 perto de g2. Uma alteração ligada depois dos 30% e que sozinha virasse a
    eleição prevê g2 - g1 = +1,79 ponto. (c) Curva prevista sem ajuste: fatia acumulada de Flávio a cada 1% das
    seções usando, no lugar do voto de cada seção, a fatia final da zona dela (curva das zonas) e a fatia dos dois
    no 1º turno menos a variação nacional (curva do 1º turno), contra a curva real: diferença máxima e nos 30%, e a
    hora prevista da troca de liderança. (d) Dentro da zona: regressão G3 com efeito fixo de zona e tratamento =
    seção entre as primeiras 30%; a alteração ligada aos 30% prevê -2,55 pontos; SINAL com -0,45 ou mais negativo e
    p < 0,001; SEM SINAL com o intervalo de 95% entre -0,45 e +0,45 (a régua do D3-6 (1)). Plantio: troca de 2,55%
    e de 0,45% nas seções depois dos 30%. A inclinação dentro da zona é o theta do D3-6 (2).

TRADUÇÃO EM VOTOS: margem de 4.430.191; cada resultado traz a margem implicada pela fórmula do registro e o teto
pelo limite do intervalo de 95%.
"""
# ACRESCENTADO DEPOIS DO DOCSTRING (o docstring acima é o gravado antes de qualquer conta com votos, sem mudança):
#   R27_ENSAIO=1 python3 -I scripts/analisar_R27_B5.py <modo>   ensaio do programa com um 2º turno sorteado pela fatia
#       do 1º turno (sem efeito de hora); grava com prefixo ensaio_. Foi como o código foi depurado antes do dado real.
#   python3 -I scripts/analisar_R27_B5.py expl   EXPLORATÓRIO, decidido depois de ver as partes 1 e 2 (comparecimento
#       como desfecho; placebo (3) com efeito fixo de local). Não entra em veredito.
#   Conciliação do histórico: onde a busca por trocas não acha atribuição, decide por programação inteira (HiGHS).
#   R7: bloco exploratório sobre o exterior e sobre o número de conjuntos de UFs esperado por acaso.
import os as _os, sys as _sys
_sys.path.insert(0, _os.path.dirname(_os.path.abspath(__file__)))
import collections, csv, datetime, glob, gzip, hashlib, io, itertools, json, math, sys, time, zipfile
import numpy as np

REPO = _os.path.dirname(_os.path.dirname(_os.path.abspath(__file__)))
DADOS = REPO + '/dados'
TRAB = '/home/user/trabalho-eleicao/adendo27/R27_B5'
D3DIR = '/home/user/trabalho-eleicao/adendo27/desenho_D3'
PERFIL_A6 = '/home/user/trabalho-eleicao/adendo27/R27_A6/perfil_secao_2026_A6.json.gz'
ZIPS = {'1': '/home/user/trabalho-eleicao/bweb1t/zips', '2': '/home/user/trabalho-eleicao/trab2t/zips2t'}
HIST = {'1': '/home/user/trabalho-eleicao/adendo27/novidades/dl_hist1t/Historico_Totalizacao_Presidente_BR_1T_2026.zip',
        '2': '/home/user/trabalho-eleicao/adendo27/novidades/dl_hist2t/Historico_Totalizacao_Presidente_BR_2T_2026.zip'}
SHA_HIST = {'1': '9b8edf4997f2cb556b45a1d307075f08f5b0d4c122acce29cc4f86e1e322d105',
            '2': '0594dbb8fdb7974f0ad520d5bd4552ae40479601984b0073d7ce5a6a1d43b4cd'}
SHA_GRUPOS = 'e1c741a3f3672b9a8a951a23133213b941ba3ca928f8632beb6798aa884d8ec8'
SAIDA_JSON = REPO + '/resultados/R27_B5_janelas_da_totalizacao.json'
SAIDA_TXT = REPO + '/resultados/R27_B5_janelas_da_totalizacao.txt'
MARGEM = 4430191
DEZ_PCT = 443019
SEMENTE = 20261110
Z001, Z01, Z80 = 3.2905, 2.5758, 0.8416


def diz(*a):
    print(time.strftime('%H:%M:%S'), *a, flush=True)


def _carrega(c):
    with gzip.open(c, 'rt') as f:
        return json.load(f)


def grava(nome, obj):
    if _os.environ.get('R27_ENSAIO'):
        nome = 'ensaio_' + nome
    tmp = TRAB + '/' + nome + '.tmp'
    with open(tmp, 'w') as f:
        json.dump(obj, f, ensure_ascii=False, indent=1, default=_jsonavel)
    _os.replace(tmp, TRAB + '/' + nome)


def _jsonavel(o):
    if isinstance(o, (np.integer,)):
        return int(o)
    if isinstance(o, (np.floating,)):
        return float(o)
    if isinstance(o, np.ndarray):
        return o.tolist()
    if isinstance(o, (np.bool_,)):
        return bool(o)
    raise TypeError(str(type(o)))


def _le(nome):
    try:
        with open(TRAB + '/' + nome) as f:
            return json.load(f)
    except FileNotFoundError:
        return None


def pnorm(z):
    return float(math.erfc(abs(z) / math.sqrt(2)))


def hhmmss(seg):
    seg = int(round(seg)); d = seg // 86400; s = seg % 86400
    return ('1d ' if d else '') + f'{s // 3600:02d}:{(s % 3600) // 60:02d}:{s % 60:02d}'


def _seg(s, dia0):
    """'2026-10-25 19:57:33' -> segundos desde 0h do dia do turno."""
    return (int(s[8:10]) - dia0) * 86400 + int(s[11:13]) * 3600 + int(s[14:16]) * 60 + int(s[17:19])


# ============================================================================================ BASE
def modo_base():
    t0 = time.time()
    assert hashlib.sha256(open(D3DIR + '/grupos_2t.json.gz', 'rb').read()).hexdigest() == SHA_GRUPOS, 'grupos congelados com hash diferente'
    GR = _carrega(D3DIR + '/grupos_2t.json.gz')
    M2 = _carrega(D3DIR + '/meta2t.json.gz'); M1 = _carrega(D3DIR + '/meta1t.json.gz')
    S = _carrega(DADOS + '/secoes2026.json.gz')
    CAND = _carrega(DADOS + '/candidatos2026_1t.json.gz')
    chaves = sorted(GR)
    assert set(chaves) == {k for k, v in S.items() if '2' in v}, 'universo do 2o turno difere entre grupos e base'
    n = len(chaves); meta = {'secoes_2t': n}
    part = [k.split('|') for k in chaves]

    def ids(lst):
        u, inv = np.unique(np.array(lst), return_inverse=True)
        return u, inv.astype(np.int32)
    ufs, uf_id = ids([p[0] for p in part])
    _, mun_id = ids([p[0] + '|' + p[1] for p in part])
    _, zona_id = ids([p[0] + '|' + p[1] + '|' + p[2] for p in part])
    _, loc_id = ids([p[0] + '|' + p[1] + '|' + p[2] + '|' + str(S[k]['2']['loc']) for p, k in zip(part, chaves)])
    A = {'uf_id': uf_id, 'mun_id': mun_id, 'zona_id': zona_id, 'loc_id': loc_id,
         'secao': np.array([int(p[3]) for p in part], np.int32)}
    for c in ('L', 'R', 'B', 'N', 'comp', 'apt'):
        A[c + '2'] = np.array([S[k]['2'][c] for k in chaves], np.int32)
    tem1 = np.array(['1' in S[k] for k in chaves])
    A['tem1'] = tem1
    for c in ('L', 'R', 'O', 'B', 'N', 'comp', 'apt'):
        A[c + '1'] = np.array([S[k]['1'][c] if '1' in S[k] else 0 for k in chaves], np.int32)
    # candidatos com 1% ou mais do comparecimento nacional do 1o turno (todas as secoes do 1o turno, exterior incluido)
    tot = collections.Counter(); comp1 = 0
    for k, v in S.items():
        if '1' in v:
            comp1 += v['1']['comp']
            for c, q in CAND['secoes'].get(k, {}).items():
                tot[c] += q
    outros = sorted(c for c, q in tot.items() if c not in ('13', '22') and q / comp1 >= 0.01)
    meta['comparecimento_nacional_1t'] = comp1
    meta['candidatos_1t_fracao_do_comparecimento'] = {c: round(q / comp1, 6) for c, q in tot.most_common()}
    meta['outros_com_1pct'] = outros
    meta['todos_candidatos_1t'] = sorted(tot, key=int)
    for c in sorted(tot, key=int):
        A['c' + c] = np.array([CAND['secoes'].get(k, {}).get(c, 0) for k in chaves], np.int32)
    # grupos congelados
    f = lambda v: np.nan if v is None else v
    A['rec_min'] = np.array([GR[k]['rec'] for k in chaves])
    A['emi'] = np.array([f(GR[k]['emi']) for k in chaves])
    A['enc'] = np.array([f(GR[k]['enc']) for k in chaves])
    A['ret'] = np.array([{'cedo': 0, 'rajada': 1, 'depois': 2}[GR[k]['ret']] for k in chaves], np.int8)
    A['pausa'] = np.array([{None: 0, 'antes': 1, 'depois': 2}[GR[k]['pausa']] for k in chaves], np.int8)
    A['desloc'] = np.array([f(GR[k]['desloc']) for k in chaves])
    for c in ('cauda', 'prorrog', 'junta', 'exterior', 'off'):
        A[c] = np.array([GR[k][c] for k in chaves], np.int8)
    A['rec_s'] = np.array([_seg(M2[k]['rec'], 25) for k in chaves], np.int64)
    # 1o turno: horas (Brasilia) do meta1t; fuso do municipio = off dos grupos
    rec1 = np.full(n, -1, np.int64); emi1 = np.full(n, np.nan); enc1 = np.full(n, np.nan); junta1 = np.zeros(n, np.int8)
    for i, k in enumerate(chaves):
        v = M1.get(k)
        if v is None:
            continue
        rec1[i] = _seg(v['rec'], 4)
        o = int(A['off'][i]) * 3600
        if v['emi'] not in ('#NULO#', '', '#NULO'):
            emi1[i] = (_seg(v['emi'], 4) + o) / 60
        if v['enc'] not in ('#NULO#', '', '#NULO'):
            enc1[i] = (_seg(v['enc'], 4) + o) / 60
        junta1[i] = int((v['junta'], v['turma']) != ('-1', '-1'))
    A['rec1_s'] = rec1; A['emi1'] = emi1; A['enc1'] = enc1; A['junta1'] = junta1
    # perfil (60 anos ou mais), somando agregadas
    PFj = _carrega(PERFIL_A6); cols = PFj['colunas']; PF = PFj['secoes']
    i_tot = cols.index('total'); i60 = [cols.index(c) for c in ('i6069', 'i7079', 'i80m')]
    f60 = np.full(n, np.nan); sem = 0
    for i, k in enumerate(chaves):
        base = PF.get(k)
        if base is None:
            sem += 1; continue
        v = np.array(base, float)
        ag = M2[k]['agr']
        if ag not in ('#NULO#', ''):
            for s in ag.split('/'):
                s = s.strip()
                if s.isdigit():
                    o = PF.get(f'{part[i][0]}|{part[i][1]}|{part[i][2]}|{int(s)}')
                    if o is not None:
                        v = v + np.array(o, float)
        if v[i_tot] > 0:
            f60[i] = v[i60].sum() / v[i_tot]
    A['f60'] = f60; meta['sem_perfil'] = sem
    del PFj, PF
    # 2022 pela chave (2o turno)
    S22 = _carrega(DADOS + '/secoes2022.json.gz')
    L22 = np.zeros(n, np.int32); R22 = np.zeros(n, np.int32); tem22 = np.zeros(n, bool)
    for i, k in enumerate(chaves):
        v = S22.get(k)
        if v is None or '2' not in v:
            continue
        L22[i] = v['2'].get('L') or 0; R22[i] = v['2'].get('R') or 0; tem22[i] = True
    A['L22'] = L22; A['R22'] = R22; A['tem22'] = tem22
    meta['pareadas_2022'] = int(tem22.sum())
    del S22
    # posicao do recebimento dentro da zona e ordem nacional
    ordem = np.lexsort((np.arange(n), A['rec_s']))
    u = np.empty(n); u[ordem] = np.arange(n) / (n - 1)
    A['u_nac'] = u
    A['ordem_nac'] = np.empty(n, np.int64); A['ordem_nac'][ordem] = np.arange(n)
    pos = np.zeros(n); nz = np.bincount(zona_id)
    o2 = np.lexsort((A['rec_s'], zona_id))
    zs = zona_id[o2]; rs = A['rec_s'][o2]
    ini = np.r_[0, np.flatnonzero(np.diff(zs)) + 1, n]
    for a, b in zip(ini[:-1], ini[1:]):
        r = rs[a:b]
        if b - a == 1:
            pos[o2[a:b]] = np.nan; continue
        # ordem media nos empates
        _, inv, cnt = np.unique(r, return_inverse=True, return_counts=True)
        fim = np.cumsum(cnt); med = fim - (cnt - 1) / 2 - 1
        pos[o2[a:b]] = med[inv] / (b - a - 1)
    A['pos_zona'] = pos
    np.savez_compressed(TRAB + '/base_B5.npz', **A)
    with gzip.open(TRAB + '/base_B5_chaves.json.gz', 'wt') as fh:
        json.dump({'chaves': chaves, 'ufs': ufs.tolist(), 'meta': meta}, fh, separators=(',', ':'), ensure_ascii=False)
    diz('base gravada', n, 'sem perfil', sem, 'outros 1%', outros, round(time.time() - t0))


ENSAIO = bool(_os.environ.get('R27_ENSAIO'))


def carrega_base():
    A = dict(np.load(TRAB + '/base_B5.npz'))
    J = _carrega(TRAB + '/base_B5_chaves.json.gz')
    if ENSAIO:
        # ensaio do código antes do dado real: o 2o turno é trocado por um sorteio binomial com a fatia dos dois no
        # 1o turno (sem nenhum efeito de hora). Serve só para achar erro de programa; grava com prefixo ensaio_.
        rg = np.random.default_rng(1)
        V = (A['L2'] + A['R2']).astype(np.int64)
        p = (A['L1'] + 0.5) / (A['L1'] + A['R1'] + 1.0)
        A['L2'] = rg.binomial(V, p).astype(np.int32); A['R2'] = (V - A['L2']).astype(np.int32)
    return A, J['chaves'], J['ufs'], J['meta']

# ============================================================================================ PARTE 3: .sha512
def modo_sha():
    """Confere o SHA-512 dos 56 zips locais contra o .sha512 baixado com o zip e contra o que o repositorio serve hoje."""
    import subprocess
    pasta = TRAB + '/dl_sha512_hoje'
    _os.makedirs(pasta, exist_ok=True)
    out = {'pedidos': 0, 'http': {}, 'parou_em_429': False, 'zips': {}, 'baixado_em_utc': time.strftime('%Y-%m-%dT%H:%M:%SZ', time.gmtime())}
    zips = sorted(glob.glob(ZIPS['1'] + '/bweb_1t_*.zip') + glob.glob(ZIPS['2'] + '/bweb_2t_*.zip'))
    for zp in zips:
        nome = _os.path.basename(zp); dest = pasta + '/' + nome + '.sha512'
        if not _os.path.exists(dest) and not out['parou_em_429']:
            url = 'https://cdn.tse.jus.br/estatistica/sead/eleicoes/eleicoes2026/buweb/' + nome + '.sha512'
            r = subprocess.run(['curl', '-sS', '-o', dest + '.parte', '-w', '%{http_code}', '--max-time', '60', url], capture_output=True, text=True)
            cod = r.stdout.strip(); out['pedidos'] += 1; out['http'][cod] = out['http'].get(cod, 0) + 1
            if cod == '200':
                _os.replace(dest + '.parte', dest)
            else:
                if _os.path.exists(dest + '.parte'):
                    _os.remove(dest + '.parte')
                if cod == '429':
                    out['parou_em_429'] = True
            time.sleep(1.0)
    for zp in zips:
        nome = _os.path.basename(zp)
        h = hashlib.sha512()
        with open(zp, 'rb') as f:
            for b in iter(lambda: f.read(1 << 22), b''):
                h.update(b)
        loc = open(zp + '.sha512').read().split()[0].lower() if _os.path.exists(zp + '.sha512') else None
        hj = pasta + '/' + nome + '.sha512'
        hoje = open(hj).read().split()[0].lower() if _os.path.exists(hj) else None
        out['zips'][nome] = {'bytes': _os.path.getsize(zp), 'sha512': h.hexdigest(), 'igual_ao_resumo_baixado_com_o_zip': loc == h.hexdigest() if loc else None,
                             'igual_ao_resumo_de_hoje': hoje == h.hexdigest() if hoje else None}
        diz(nome, out['zips'][nome]['igual_ao_resumo_baixado_com_o_zip'], out['zips'][nome]['igual_ao_resumo_de_hoje'])
    z = out['zips'].values()
    out['resumo'] = {'zips': len(out['zips']), 'turno1': sum(1 for k in out['zips'] if '_1t_' in k), 'turno2': sum(1 for k in out['zips'] if '_2t_' in k),
                     'iguais_ao_resumo_baixado_com_o_zip': sum(1 for v in z if v['igual_ao_resumo_baixado_com_o_zip']),
                     'iguais_ao_resumo_de_hoje': sum(1 for v in z if v['igual_ao_resumo_de_hoje']),
                     'sem_resumo_de_hoje': sum(1 for v in z if v['igual_ao_resumo_de_hoje'] is None),
                     'diferentes': sorted(k for k, v in out['zips'].items() if v['igual_ao_resumo_baixado_com_o_zip'] is False or v['igual_ao_resumo_de_hoje'] is False)}
    for t in ('1', '2'):
        out['resumo'][f'sha256_do_zip_do_historico_{t}t_igual_ao_anotado_em_09_11'] = hashlib.sha256(open(HIST[t], 'rb').read()).hexdigest() == SHA_HIST[t]
    grava('parcial_sha.json', out)
    diz('sha pronto', out['resumo'])


# ============================================================================================ PARTE 3: histórico
def le_bweb_2t():
    """Lê direto dos 28 zips do bweb do 2o turno as linhas do cargo 1: votos, comparecimento, aptos e hora de recebimento."""
    secs = {}; tipos = collections.Counter()
    for zp in sorted(glob.glob(ZIPS['2'] + '/bweb_2t_*.zip')):
        z = zipfile.ZipFile(zp)
        nome = [x for x in z.namelist() if x.lower().endswith('.csv')][0]
        with z.open(nome) as fh:
            rd = csv.reader(io.TextIOWrapper(fh, encoding='latin1', newline=''), delimiter=';')
            cab = next(rd); ix = {c.strip().replace('SG_ UF', 'SG_UF'): i for i, c in enumerate(cab)}
            iC, iU, iM, iZ, iS = ix['CD_CARGO_PERGUNTA'], ix['SG_UF'], ix['CD_MUNICIPIO'], ix['NR_ZONA'], ix['NR_SECAO']
            iT, iV, iQ, iR, iA, iP = ix['DS_TIPO_VOTAVEL'], ix['NR_VOTAVEL'], ix['QT_VOTOS'], ix['DT_BU_RECEBIDO'], ix['QT_APTOS'], ix['QT_COMPARECIMENTO']
            for r in rd:
                if r[iC] != '1':
                    continue
                k = f'{r[iU]}|{int(r[iM])}|{int(r[iZ])}|{int(r[iS])}'
                d = secs.get(k)
                if d is None:
                    d = secs[k] = {'rec': r[iR], 'apt': int(r[iA]), 'comp': int(r[iP]), '13': 0, '22': 0, 'B': 0, 'N': 0}
                else:
                    assert d['rec'] == r[iR] and d['apt'] == int(r[iA]) and d['comp'] == int(r[iP]), k
                tp = r[iT].strip().lower(); nv = r[iV]; tipos[(tp, nv)] += 1
                c = 'B' if tp == 'branco' else 'N' if tp == 'nulo' else nv if tp == 'nominal' else None
                assert c in ('13', '22', 'B', 'N'), (k, tp, nv)
                d[c] += int(r[iQ])
    return secs, {f'{a}|{b}': q for (a, b), q in tipos.items()}


def le_historico(turno):
    """Passos do historico por (UF, municipio, zona). Devolve lista de passos e rotulos dos votaveis."""
    dia0 = 25 if turno == '2' else 4
    z = zipfile.ZipFile(HIST[turno])
    passos = {}; rot = None; meta = {'linhas': 0, 'QT_SECOES_BRASIL': set(), 'QT_APTOS_BRASIL': set(), 'geracao': set()}
    aptz = {}; secz = {}
    for nome in sorted(z.namelist()):
        if not nome.endswith('.csv'):
            continue
        with z.open(nome) as f:
            r = csv.reader(io.TextIOWrapper(f, encoding='latin-1', newline=''), delimiter=';')
            cab = next(r); ix = {c: i for i, c in enumerate(cab)}
            for l in r:
                meta['linhas'] += 1
                assert int(l[ix['NR_TURNO']]) == int(turno) and l[ix['CD_CARGO']] == '1'
                k = (l[ix['SG_UF']], int(l[ix['CD_MUNICIPIO']]), int(l[ix['NR_ZONA']]))
                i = int(l[ix['ID_TOTALIZACAO']])
                dt = l[ix['DT_TOTALIZACAO']]   # dd/mm/aaaa hh:mm:ss
                t = (int(dt[0:2]) - dia0) * 86400 + int(dt[11:13]) * 3600 + int(dt[14:16]) * 60 + int(dt[17:19])
                assert dt[3:5] == '10'
                nm = l[ix['NM_CANDIDATO']]
                c = 'B' if nm == 'VOTOS BRANCOS' else 'N' if nm == 'VOTOS NULOS' else l[ix['NR_VOTAVEL']]
                p = passos.setdefault((k, i), {'t': t, 'n': int(l[ix['QT_SECOES_TOT']]), 'nac': int(l[ix['QT_SECOES_TOT_ACUMULADO']]),
                                               'comp': int(l[ix['QT_APTOS_TOT']]), 'compac': int(l[ix['QT_APTOS_TOT_ACUMULADO']]), 'v': {}, 'ac': {}, 'val': {}})
                assert p['t'] == t and p['n'] == int(l[ix['QT_SECOES_TOT']]) and c not in p['v'], (k, i)
                p['v'][c] = int(l[ix['QT_VOTOS_TOT']]); p['ac'][c] = int(l[ix['QT_VOTOS_TOTAL_ACUMULADO']])
                p['val'][c] = int(l[ix['QT_VOTOS_VALIDOS_ACUMULADO']])
                meta['QT_SECOES_BRASIL'].add(int(l[ix['QT_SECOES_BRASIL']])); meta['QT_APTOS_BRASIL'].add(int(l[ix['QT_APTOS_BRASIL']]))
                meta['geracao'].add(l[ix['DT_GERACAO']])
                aptz[k] = int(l[ix['QT_APTOS_ZONA']]); secz[k] = int(l[ix['QT_SECOES_ZONA']])
    for c in ('QT_SECOES_BRASIL', 'QT_APTOS_BRASIL', 'geracao'):
        meta[c] = sorted(meta[c])
    return passos, aptz, secz, meta


def monta_conciliacao(passos, secoes, cands):
    """Arruma historico e bweb em vetores ordenados para a conferencia.
    secoes: {chave: {'rec': segundos, 'v': [votos na ordem de cands + comparecimento], 'apt': int}}"""
    K = len(cands) + 1
    zonas = sorted({k for (k, i) in passos} | {tuple([c.split('|')[0], int(c.split('|')[1]), int(c.split('|')[2])]) for c in secoes})
    zix = {z: j for j, z in enumerate(zonas)}
    # passos
    pk = sorted(passos, key=lambda x: (zix[x[0]], passos[x]['t'], x[1]))
    Pz = np.array([zix[k] for k, i in pk], np.int64); Pt = np.array([passos[x]['t'] for x in pk], np.int64)
    Pn = np.array([passos[x]['n'] for x in pk], np.int64); Pid = np.array([x[1] for x in pk], np.int64)
    Pv = np.array([[passos[x]['v'].get(c, 0) for c in cands] + [passos[x]['comp']] for x in pk], np.int64)
    Pac = np.array([[passos[x]['ac'].get(c, 0) for c in cands] + [passos[x]['compac']] for x in pk], np.int64)
    Pnac = np.array([passos[x]['nac'] for x in pk], np.int64)
    return dict(zonas=zonas, zix=zix, K=K, cands=cands, Pz=Pz, Pt=Pt, Pn=Pn, Pid=Pid, Pv=Pv, Pac=Pac, Pnac=Pnac)


def _trocas(vA, vR, delta, kmax=3, teto=4000000):
    """Gera (índices a tirar de A, índices a pôr de R) com soma(vR[Y]) - soma(vA[X]) == delta, |X| = |Y| = k."""
    tA = [tuple(v) for v in vA.tolist()]; tR = [tuple(v) for v in vR.tolist()]
    d = tuple(delta.tolist()); K = len(d)
    dA = {}
    for i, v in enumerate(tA):
        dA.setdefault(v, []).append(i)
    for j, v in enumerate(tR):
        for i in dA.get(tuple(v[q] - d[q] for q in range(K)), ()):
            yield [i], [j]
    if kmax >= 2 and len(tA) * (len(tA) - 1) // 2 + len(tR) * (len(tR) - 1) // 2 <= teto:
        pa = {}
        for i1 in range(len(tA)):
            a1 = tA[i1]
            for i2 in range(i1 + 1, len(tA)):
                a2 = tA[i2]
                pa.setdefault(tuple(a1[q] + a2[q] for q in range(K)), []).append((i1, i2))
        for j1 in range(len(tR)):
            b1 = tR[j1]
            for j2 in range(j1 + 1, len(tR)):
                b2 = tR[j2]
                for (i1, i2) in pa.get(tuple(b1[q] + b2[q] - d[q] for q in range(K)), ()):
                    yield [i1, i2], [j1, j2]
    if kmax >= 3 and len(tA) <= 60 and len(tR) <= 60:
        pa = {}
        for c in itertools.combinations(range(len(tA)), 3):
            pa.setdefault(tuple(tA[c[0]][q] + tA[c[1]][q] + tA[c[2]][q] for q in range(K)), []).append(c)
        for c in itertools.combinations(range(len(tR)), 3):
            for x in pa.get(tuple(tR[c[0]][q] + tR[c[1]][q] + tR[c[2]][q] - d[q] for q in range(K)), ()):
                yield list(x), list(c)


def _busca(vecs, recs, alvo_v, alvo_n, alvo_t, max_alt=50):
    """Atribuição exata de seções (já na ordem de recebimento) a passos de um trecho, por trocas a partir da ordem
    estrita. Devolve lista de índices por passo, None se não achou."""
    m = len(vecs)

    def rec(j, livres):
        if j == len(alvo_n):
            return []
        nj = alvo_n[j]
        A = livres[:nj]; R = [i for i in livres[nj:] if recs[i] <= alvo_t[j]]
        if len(A) < nj or any(recs[i] > alvo_t[j] for i in A):
            # a ordem estrita já põe no passo seção recebida depois dele: só vale se a troca tirar essas
            pass
        delta = alvo_v[j] - vecs[A].sum(0)
        if not delta.any() and all(recs[i] <= alvo_t[j] for i in A):
            r = rec(j + 1, livres[nj:])
            if r is not None:
                return [A] + r
        alt = 0
        for X, Y in _trocas(vecs[A], vecs[R], delta):
            fica = [a for q, a in enumerate(A) if q not in X] + [R[y] for y in Y]
            if any(recs[i] > alvo_t[j] for i in fica):
                continue
            usados = set(fica)
            r = rec(j + 1, [i for i in livres if i not in usados])
            if r is not None:
                return [fica] + r
            alt += 1
            if alt >= max_alt:
                break
        return None
    return rec(0, list(range(m)))


def _busca_milp(vecs, recs, alvo_v, alvo_n, alvo_t, tempo=120):
    """Atribuição exata por programação inteira (HiGHS, scipy.optimize.milp): x[i, j] = 1 se a seção i entra no
    passo j. Devolve a lista por passo, None se o problema é inviável (não existe atribuição), 'tempo' se parou."""
    from scipy.optimize import milp, LinearConstraint, Bounds
    from scipy.sparse import lil_matrix
    m = len(vecs); J = len(alvo_n); K = vecs.shape[1]
    nv = m * J
    A = lil_matrix((m + J + J * K, nv)); lo = np.zeros(m + J + J * K); hi = np.zeros(m + J + J * K)
    for i in range(m):
        for j in range(J):
            A[i, i * J + j] = 1
        lo[i] = hi[i] = 1
    for j in range(J):
        for i in range(m):
            A[m + j, i * J + j] = 1
            for q in range(K):
                if vecs[i, q]:
                    A[m + J + j * K + q, i * J + j] = vecs[i, q]
        lo[m + j] = hi[m + j] = alvo_n[j]
        for q in range(K):
            lo[m + J + j * K + q] = hi[m + J + j * K + q] = alvo_v[j][q]
    ub = np.ones(nv)
    for i in range(m):
        for j in range(J):
            if recs[i] > alvo_t[j]:
                ub[i * J + j] = 0
    r = milp(c=np.zeros(nv), constraints=LinearConstraint(A.tocsr(), lo, hi), integrality=np.ones(nv), bounds=Bounds(np.zeros(nv), ub),
             options={'time_limit': tempo, 'presolve': True})
    if r.status == 2:
        return None
    if r.x is None:
        return 'tempo'
    x = np.round(r.x).reshape(m, J)
    sol = [np.flatnonzero(x[:, j] == 1).tolist() for j in range(J)]
    for j in range(J):       # confere a solução com inteiros
        if len(sol[j]) != alvo_n[j] or (vecs[sol[j]].sum(0) != alvo_v[j]).any() or any(recs[i] > alvo_t[j] for i in sol[j]):
            return 'tempo'
    return sol


def prepara_secoes(C, secoes):
    zix = C['zix']; ks = list(secoes)
    Sz = np.array([zix[(c.split('|')[0], int(c.split('|')[1]), int(c.split('|')[2]))] for c in ks], np.int64)
    Ssec = np.array([int(c.split('|')[3]) for c in ks], np.int64)
    Sr = np.array([secoes[c]['rec'] for c in ks], np.int64)
    Sv = np.array([secoes[c]['v'] for c in ks], np.int64)
    Sa = np.array([secoes[c]['apt'] for c in ks], np.int64)
    return dict(ks=np.array(ks), Sz=Sz, Ssec=Ssec, Sr=Sr, Sv=Sv, Sa=Sa)


def concilia(C, P, detalhe=True, milp=True, passo_a_passo=True):
    """Conferências (a), (b), (c) e (d) do H2. P = vetores de prepara_secoes (podem vir alterados por um plantio)."""
    K = C['K']; nz = len(C['zonas'])
    o = np.lexsort((P['Ssec'], P['Sr'], P['Sz']))
    Sz, Ssec, Sr, Sv, ks = P['Sz'][o], P['Ssec'][o], P['Sr'][o], P['Sv'][o], P['ks'][o]
    out = {}
    somaB = np.zeros((nz, K), np.int64); np.add.at(somaB, Sz, Sv)
    nB = np.bincount(Sz, minlength=nz)
    somaP = np.zeros((nz, K), np.int64); np.add.at(somaP, C['Pz'], C['Pv'])
    nP = np.zeros(nz, np.int64); np.add.at(nP, C['Pz'], C['Pn'])
    ult = np.r_[np.flatnonzero(np.diff(C['Pz'])), len(C['Pz']) - 1]
    acF = np.zeros((nz, K), np.int64); acF[C['Pz'][ult]] = C['Pac'][ult]
    nacF = np.zeros(nz, np.int64); nacF[C['Pz'][ult]] = C['Pnac'][ult]
    d = somaB - acF                       # bweb menos histórico (último acumulado)
    out['zonas'] = int(nz)
    out['zonas_com_soma_dos_passos_diferente_do_ultimo_acumulado'] = int(((somaP != acF).any(1) | (nP != nacF)).sum())
    rot = C['cands'] + ['comparecimento']
    out['zonas_com_d_diferente_de_zero'] = {r: int((d[:, j] != 0).sum()) for j, r in enumerate(rot)}
    out['zonas_com_numero_de_secoes_diferente'] = int((nB != nacF).sum())
    apont = np.flatnonzero((d != 0).any(1) | (nB != nacF))
    out['zonas_apontadas_n'] = int(len(apont))
    out['zonas_apontadas'] = [dict(zona='|'.join(map(str, C['zonas'][j])), d={r: int(d[j, q]) for q, r in enumerate(rot) if d[j, q]}, secoes_bweb_menos_hist=int(nB[j] - nacF[j]))
                              for j in apont[:50]]
    ufz = np.array([z[0] for z in C['zonas']]); munz = np.array([z[0] + '|' + str(z[1]) for z in C['zonas']])
    for nome, lab in (('municipios', munz), ('ufs', ufz)):
        u, inv = np.unique(lab, return_inverse=True)
        dm = np.zeros((len(u), K), np.int64); np.add.at(dm, inv, d)
        out[nome] = int(len(u))
        out[nome + '_com_d_diferente_de_zero'] = {r: int((dm[:, j] != 0).sum()) for j, r in enumerate(rot)}
        out[nome + '_apontados'] = [str(x) for x in u[(dm != 0).any(1)][:50]]
    dn = d.sum(0)
    out['d_nacional_bweb_menos_historico'] = {r: int(dn[j]) for j, r in enumerate(rot)}
    out['soma_abs_d_por_zona'] = {r: int(np.abs(d[:, j]).sum()) for j, r in enumerate(rot)}
    if '13' in rot and '22' in rot:
        out['d_liquido_nacional_13_menos_22'] = int(dn[rot.index('13')] - dn[rot.index('22')])
    out['total_bweb'] = {r: int(somaB[:, j].sum()) for j, r in enumerate(rot)}
    out['total_historico'] = {r: int(acF[:, j].sum()) for j, r in enumerate(rot)}
    out['secoes_bweb'] = int(len(ks)); out['secoes_historico'] = int(nacF.sum())
    if not passo_a_passo:
        return out, None
    # (b) e (c): blocos pela ordem de recebimento, só nas zonas com contagem igual
    iniS = np.zeros(nz + 1, np.int64); np.cumsum(nB, out=iniS[1:])
    zona_ok = nB == nP
    acum = np.cumsum(C['Pn'])
    iniP = np.r_[0, np.flatnonzero(np.diff(C['Pz'])) + 1]
    base_z = np.zeros(nz, np.int64); base_z[C['Pz'][iniP]] = np.r_[0, acum[iniP[1:] - 1]]
    Pfim = acum - base_z[C['Pz']] + iniS[C['Pz']]
    Pini = Pfim - C['Pn']
    okp = zona_ok[C['Pz']]
    N = len(ks)
    CS = np.zeros((N + 1, K), np.int64); np.cumsum(Sv, axis=0, out=CS[1:])
    fimc = np.clip(Pfim, 0, N); inic = np.clip(Pini, 0, N)
    bloco = CS[fimc] - CS[inic]
    ultrec = Sr[np.clip(Pfim - 1, 0, N - 1)]
    antes = (ultrec > C['Pt']) & okp & (C['Pn'] > 0)
    fecha = (bloco == C['Pv']).all(1) & okp & ~antes
    out['passos'] = int(len(C['Pn'])); out['passos_sem_secao'] = int((C['Pn'] == 0).sum())
    out['zonas_com_contagem_de_secoes_diferente_dos_passos'] = int((~zona_ok).sum())
    out['passos_com_boletim_recebido_depois_do_passo_na_ordem_de_recebimento'] = int(antes.sum())
    out['passos_que_fecham_na_ordem_de_recebimento'] = int(fecha.sum())
    out['passos_que_nao_fecham_na_ordem_estrita'] = int((~fecha & okp).sum())
    trechos = []; n_outra = 0; n_sem = 0; n_milp = 0; n_tempo = 0; ex_sem = []
    atrib_t = np.full(N, -1, np.int64)
    if okp.any():
        rep = np.repeat(np.arange(len(C['Pn'])), np.where(okp, C['Pn'], 0))
        idx_sec = np.concatenate([np.arange(a, b) for a, b in zip(Pini[okp], Pfim[okp])])
        passo_fifo = np.full(N, -1, np.int64); passo_fifo[idx_sec] = rep
        bom = (passo_fifo >= 0)
        bom[bom] = fecha[passo_fifo[bom]]
        atrib_t[bom] = C['Pt'][passo_fifo[bom]]
    nao = np.flatnonzero(~fecha & okp)
    acP = np.cumsum(C['Pv'], axis=0)
    j = 0
    while j < len(nao):
        a = nao[j]; b = a; z = C['Pz'][a]
        while True:
            sp = acP[b] - (acP[a - 1] if a > 0 else 0)
            sb = CS[Pfim[b]] - CS[Pini[a]]
            if (sp == sb).all():
                break
            b += 1
            if b >= len(C['Pn']) or C['Pz'][b] != z:
                b = None; break
        if b is None:
            fimz = a
            while fimz + 1 < len(C['Pn']) and C['Pz'][fimz + 1] == z:
                fimz += 1
            n_sem += fimz - a + 1
            ex_sem.append(dict(zona='|'.join(map(str, C['zonas'][z])), passo=int(C['Pid'][a]), motivo='o trecho não fecha até o fim da zona'))
            while j < len(nao) and C['Pz'][nao[j]] == z:
                j += 1
            continue
        pool = np.arange(Pini[a], Pfim[b]); npas = b - a + 1
        r = _busca(Sv[pool], Sr[pool].tolist(), C['Pv'][a:b + 1], C['Pn'][a:b + 1].tolist(), C['Pt'][a:b + 1].tolist())
        if r is None and milp:             # as trocas pequenas não acharam: decide por programação inteira
            r = _busca_milp(Sv[pool], Sr[pool].tolist(), C['Pv'][a:b + 1], C['Pn'][a:b + 1].tolist(), C['Pt'][a:b + 1].tolist())
            n_milp += npas
        if r == 'tempo':
            n_tempo += npas
        elif r is None:
            n_sem += npas
            ex_sem.append(dict(zona='|'.join(map(str, C['zonas'][z])), passos=[int(x) for x in C['Pid'][a:b + 1]], secoes=[str(ks[i]) for i in pool][:12], motivo='programação inteira inviável: não existe atribuição que respeite votos e hora de recebimento'))
        else:
            n_outra += npas
            for q, comb in enumerate(r):
                atrib_t[pool[comb]] = C['Pt'][a + q]
        trechos.append(npas)
        while j < len(nao) and nao[j] <= b:
            j += 1
    out['trechos_com_ordem_trocada'] = int(len(trechos))
    out['trechos_por_tamanho_em_passos'] = {str(k): v for k, v in sorted(collections.Counter(trechos).items())}
    out['passos_que_fecham_com_outra_ordem'] = int(n_outra)
    out['passos_sem_atribuicao_possivel'] = int(n_sem)
    out['passos_decididos_por_programacao_inteira'] = int(n_milp)
    out['passos_com_busca_interrompida_por_tempo'] = int(n_tempo)
    out['exemplos_sem_atribuicao'] = ex_sem[:20]
    out['secoes_com_passo_atribuido'] = int((atrib_t >= 0).sum())
    if detalhe:
        lag = (atrib_t - Sr)[atrib_t >= 0]
        if len(lag):
            q = np.quantile(lag, [0, .01, .1, .5, .9, .99, 1])
            out['defasagem_totalizacao_menos_recebimento_s'] = dict(min=float(q[0]), p1=float(q[1]), p10=float(q[2]), mediana=float(q[3]), p90=float(q[4]), p99=float(q[5]), max=float(q[6]), negativas=int((lag < 0).sum()))
        mP = C['Pt'] // 60; mS = Sr // 60
        m0 = int(min(mP.min(), mS.min())); m1 = int(max(mP.max(), mS.max()))
        H = np.zeros((m1 - m0 + 1, K + 1), np.int64); B = np.zeros((m1 - m0 + 1, K + 1), np.int64)
        np.add.at(H, mP - m0, np.column_stack([C['Pv'], C['Pn']])); np.add.at(B, mS - m0, np.column_stack([Sv, np.ones(N, np.int64)]))
        Hc = H.cumsum(0); Bc = B.cumsum(0)
        viol = (Hc > Bc).any(1)
        fila = Bc[:, K] - Hc[:, K]
        out['serie_por_minuto'] = dict(minutos=int(len(Hc)), minutos_em_que_o_historico_passa_o_recebido=int(viol.sum()),
                                       maior_fila_em_secoes=int(fila.max()), minuto_da_maior_fila=hhmmss((m0 + int(fila.argmax())) * 60),
                                       minutos_com_fila_acima_de_1000=int((fila > 1000).sum()), acumulado_final_igual=bool((Hc[-1] == Bc[-1]).all()))
    return out, dict(ks=ks, atrib_t=atrib_t, Sr=Sr)


def modo_hist():
    t0 = time.time()
    A, chaves, ufs, meta = carrega_base()
    res = {'sha256_zip_historico_confere': {t: hashlib.sha256(open(HIST[t], 'rb').read()).hexdigest() == SHA_HIST[t] for t in ('1', '2')}}
    # ------------------------------------------------ 2o turno, lido direto dos zips
    bw, tipos = le_bweb_2t()
    diz('bweb 2t lido', len(bw), round(time.time() - t0))
    ix = {k: i for i, k in enumerate(chaves)}
    dif_base = 0
    for k, v in bw.items():
        i = ix.get(k)
        if i is None or (v['13'], v['22'], v['B'], v['N'], v['comp'], v['apt']) != (int(A['L2'][i]), int(A['R2'][i]), int(A['B2'][i]), int(A['N2'][i]), int(A['comp2'][i]), int(A['apt2'][i])) or _seg(v['rec'], 25) != int(A['rec_s'][i]):
            dif_base += 1
    res['leitura_direta_2t'] = dict(secoes=len(bw), tipos_de_votavel=tipos, secoes_diferentes_da_base_dados=dif_base, secoes_so_na_base=len(set(chaves) - set(bw)),
                                    aptos=sum(v['apt'] for v in bw.values()), comparecimento=sum(v['comp'] for v in bw.values()))
    cands2 = ['13', '22', 'B', 'N']
    sec2 = {k: {'rec': _seg(v['rec'], 25), 'v': [v['13'], v['22'], v['B'], v['N'], v['comp']], 'apt': v['apt']} for k, v in bw.items()}
    passos2, aptz2, secz2, mh2 = le_historico('2')
    C2 = monta_conciliacao(passos2, sec2, cands2)
    P2 = prepara_secoes(C2, sec2)
    r2, det2 = concilia(C2, P2)
    # aptos por zona
    az = collections.Counter()
    for k, v in sec2.items():
        p = k.split('|'); az[(p[0], int(p[1]), int(p[2]))] += v['apt']
    r2['zonas_com_QT_APTOS_ZONA_diferente_do_bweb'] = sum(1 for z in az if az[z] != aptz2.get(z))
    r2['soma_QT_APTOS_ZONA'] = sum(aptz2.values()); r2['aptos_bweb'] = sum(az.values()); r2['soma_QT_SECOES_ZONA'] = sum(secz2.values())
    r2['historico'] = mh2
    res['turno2'] = r2
    grava('parcial_hist.json', res)
    diz('2t conciliado', {k: r2[k] for k in ('zonas_com_d_diferente_de_zero', 'passos', 'passos_que_fecham_na_ordem_de_recebimento', 'passos_que_fecham_com_outra_ordem', 'passos_sem_atribuicao_possivel')}, round(time.time() - t0))
    # hora do passo de cada secao (para R8 e descritivos)
    tt = np.full(len(chaves), -1, np.int64)
    for k, t in zip(det2['ks'], det2['atrib_t']):
        tt[ix[k]] = t
    np.save(TRAB + '/hora_do_passo_2t.npy', tt)
    # ------------------------------------------------ plantios no 2o turno
    rng = np.random.default_rng(SEMENTE)
    kk = sorted(sec2)
    por_mun = collections.defaultdict(list)
    for k in kk:
        por_mun['|'.join(k.split('|')[:2])].append(k)
    por_uf = collections.defaultdict(list)
    for m in por_mun:
        por_uf[m.split('|')[0]].append(m)
    # blocos por passo (para o plantio de ordem)
    passo_de = {}
    porz = collections.defaultdict(list)
    for k, t in zip(det2['ks'], det2['atrib_t']):
        p = k.split('|'); porz[(p[0], int(p[1]), int(p[2]))].append((int(t), k))
    base_ok = dict(zonas=sum(r2['zonas_com_d_diferente_de_zero'].values()), sem=r2['passos_sem_atribuicao_possivel'], antes=r2['passos_com_boletim_recebido_depois_do_passo_na_ordem_de_recebimento'])
    pl = {n: [] for n in ('1_um_voto_a_mais', '2_secao_retirada', '3_dez_votos_entre_municipios', '4_hora_trocada_entre_passos', '5_hora_trocada_no_mesmo_passo')}

    def resumo(r):
        return dict(zonas_13=r['zonas_com_d_diferente_de_zero']['13'], municipios_13=r['municipios_com_d_diferente_de_zero']['13'], ufs_13=r['ufs_com_d_diferente_de_zero']['13'],
                    d_nacional_13=r['d_nacional_bweb_menos_historico']['13'], zonas_qualquer=r['zonas_apontadas_n'],
                    zonas_n_secoes=r['zonas_com_numero_de_secoes_diferente'],
                    passos_nao_fecham=r['passos_que_nao_fecham_na_ordem_estrita'], passos_sem_atribuicao=r['passos_sem_atribuicao_possivel'],
                    passos_antes_de_recebido=r['passos_com_boletim_recebido_depois_do_passo_na_ordem_de_recebimento'],
                    passos_outra_ordem=r['passos_que_fecham_com_outra_ordem'])
    NPL = 20
    pix = {k: i for i, k in enumerate(P2['ks'].tolist())}

    def copia(**alt):
        Q = dict(P2)
        for c in ('Sv', 'Sr'):
            Q[c] = P2[c].copy()
        return Q
    for rep in range(NPL):
        # (1) um voto a mais para o 13 em uma seção
        k = kk[rng.integers(len(kk))]; Q = copia(); Q['Sv'][pix[k], 0] += 1
        pl['1_um_voto_a_mais'].append(resumo(concilia(C2, Q, False, milp=False)[0]))
        # (2) uma seção inteira retirada
        k = kk[rng.integers(len(kk))]; m = np.ones(len(kk), bool); m[pix[k]] = False
        Q = {c: v[m] for c, v in P2.items()}
        pl['2_secao_retirada'].append(resumo(concilia(C2, Q, False, milp=False)[0]))
        # (3) dez votos do 13 entre dois municípios da mesma UF
        while True:
            uf = list(por_uf)[rng.integers(len(por_uf))]
            if len(por_uf[uf]) < 2:
                continue
            ma, mb = [por_uf[uf][i] for i in rng.choice(len(por_uf[uf]), 2, replace=False)]
            ka = por_mun[ma][rng.integers(len(por_mun[ma]))]; kb = por_mun[mb][rng.integers(len(por_mun[mb]))]
            if sec2[ka]['v'][0] >= 10:
                break
        Q = copia(); Q['Sv'][pix[ka], 0] -= 10; Q['Sv'][pix[kb], 0] += 10
        pl['3_dez_votos_entre_municipios'].append(resumo(concilia(C2, Q, False, milp=False)[0]))
        # (4) a primeira seção de uma zona troca de hora com uma seção recebida DEPOIS da hora do primeiro passo
        while True:
            z = list(porz)[rng.integers(len(porz))]
            l = sorted(porz[z])
            if len({t for t, _ in l}) < 2:
                continue
            t1 = l[0][0]
            tarde = [k_ for t, k_ in l if sec2[k_]['rec'] > t1 and sec2[k_]['v'] != sec2[l[0][1]]['v']]
            if not tarde:
                continue
            ka = l[0][1]; kb = tarde[rng.integers(len(tarde))]
            break
        Q = copia(); Q['Sr'][pix[ka]], Q['Sr'][pix[kb]] = P2['Sr'][pix[kb]], P2['Sr'][pix[ka]]
        pl['4_hora_trocada_entre_passos'].append(resumo(concilia(C2, Q, False, milp=False)[0]))
        # (5) duas seções do mesmo passo trocam a hora
        while True:
            z = list(porz)[rng.integers(len(porz))]
            g = collections.defaultdict(list)
            for t, k_ in porz[z]:
                g[t].append(k_)
            gg = [v for v in g.values() if len(v) >= 2]
            if gg:
                v = gg[rng.integers(len(gg))]; ka, kb = [v[i] for i in rng.choice(len(v), 2, replace=False)]
                break
        Q = copia(); Q['Sr'][pix[ka]], Q['Sr'][pix[kb]] = P2['Sr'][pix[kb]], P2['Sr'][pix[ka]]
        pl['5_hora_trocada_no_mesmo_passo'].append(resumo(concilia(C2, Q, False, milp=False)[0]))
        diz('plantio', rep + 1, round(time.time() - t0))
    b0 = resumo(concilia(C2, P2, False, milp=False)[0])     # mesma busca dos plantios (só trocas pequenas, sem programação inteira)
    det = {}
    det['1_um_voto_a_mais'] = dict(repeticoes=NPL, aponta_exatamente_1_zona_1_municipio_1_uf_e_pais=sum(1 for x in pl['1_um_voto_a_mais'] if (x['zonas_13'], x['municipios_13'], x['ufs_13'], x['d_nacional_13']) == (1, 1, 1, 1)),
                                   acusa_tambem_no_passo_a_passo=sum(1 for x in pl['1_um_voto_a_mais'] if x['passos_nao_fecham'] > b0['passos_nao_fecham']))
    det['2_secao_retirada'] = dict(repeticoes=NPL, aponta_exatamente_1_zona=sum(1 for x in pl['2_secao_retirada'] if x['zonas_n_secoes'] == 1 and x['zonas_qualquer'] == 1))
    det['3_dez_votos_entre_municipios'] = dict(repeticoes=NPL, aponta_2_municipios_uf_fecha_pais_fecha=sum(1 for x in pl['3_dez_votos_entre_municipios'] if (x['municipios_13'], x['ufs_13'], x['d_nacional_13']) == (2, 0, 0)))
    det['4_hora_trocada_entre_passos'] = dict(repeticoes=NPL, acusa=sum(1 for x in pl['4_hora_trocada_entre_passos'] if x['passos_sem_atribuicao'] > b0['passos_sem_atribuicao'] or x['passos_antes_de_recebido'] > b0['passos_antes_de_recebido']),
                                              zonas_no_fim=sum(x['zonas_qualquer'] for x in pl['4_hora_trocada_entre_passos']))
    det['5_hora_trocada_no_mesmo_passo'] = dict(repeticoes=NPL, acusa=sum(1 for x in pl['5_hora_trocada_no_mesmo_passo'] if (x['zonas_qualquer'], x['passos_sem_atribuicao'], x['passos_antes_de_recebido']) != (b0['zonas_qualquer'], b0['passos_sem_atribuicao'], b0['passos_antes_de_recebido'])))
    res['plantios_2t'] = dict(deteccao=det, sem_plantio=b0, cada=pl)
    grava('parcial_hist.json', res)
    diz('plantios', det)
    del bw, sec2, passos2, C2, P2
    # ------------------------------------------------ 1o turno (placebo): base dados + meta1t
    S = _carrega(DADOS + '/secoes2026.json.gz'); CAND = _carrega(DADOS + '/candidatos2026_1t.json.gz'); M1 = _carrega(D3DIR + '/meta1t.json.gz')
    passos1, aptz1, secz1, mh1 = le_historico('1')
    cands1 = sorted({c for p in passos1.values() for c in p['v'] if c not in ('B', 'N')}, key=int) + ['B', 'N']
    sec1 = {}
    for k, v in S.items():
        if '1' not in v:
            continue
        c = CAND['secoes'].get(k, {})
        nom = [c.get(x, 0) for x in cands1[:-2]]
        # na base, O = comparecimento menos 13, 22, brancos e nulos; o que sobra de O depois dos nominais é o 28
        resto = v['1']['O'] - sum(q for x, q in zip(cands1[:-2], nom) if x not in ('13', '22'))
        sec1[k] = {'rec': _seg(M1[k]['rec'], 4), 'v': nom + [v['1']['B'], v['1']['N'], v['1']['comp']], 'apt': v['1']['apt'], 'resto': resto}
    # passada 1, pela letra: cada votável do histórico contra o mesmo votável do bweb (só o fim)
    C1 = monta_conciliacao(passos1, sec1, cands1)
    lit, _ = concilia(C1, prepara_secoes(C1, sec1), passo_a_passo=False)
    j28 = cands1.index('28') if '28' in cands1 else None
    lit['soma_do_resto_de_O_na_base'] = int(sum(v['resto'] for v in sec1.values()))
    lit['historico_total_do_28'] = int(sum(p['v'].get('28', 0) for p in passos1.values()))
    # passada 2: nulos mais o 28 (candidato anulado) dos dois lados, e os votos do 28 que a base guarda em O
    cands1m = [c for c in cands1 if c != '28']
    for p in passos1.values():
        for campo in ('v', 'ac'):
            p[campo]['N'] = p[campo]['N'] + p[campo].get('28', 0)
    sec1m = {}
    for k, v in sec1.items():
        vv = list(v['v']); n28 = vv.pop(j28) if j28 is not None else 0
        vv[len(cands1m) - 1] += n28 + v['resto']
        sec1m[k] = {'rec': v['rec'], 'v': vv, 'apt': v['apt']}
    C1 = monta_conciliacao(passos1, sec1m, cands1m)
    r1, det1 = concilia(C1, prepara_secoes(C1, sec1m))
    r1['passada_pela_letra_votavel_a_votavel'] = {k: lit[k] for k in ('zonas_com_d_diferente_de_zero', 'd_nacional_bweb_menos_historico', 'total_bweb', 'total_historico', 'soma_do_resto_de_O_na_base', 'historico_total_do_28')}
    r1['nota'] = 'passada principal com nulos mais o 28 (candidato anulado) somados dos dois lados'
    sec1 = sec1m
    az = collections.Counter()
    for k, v in sec1.items():
        p = k.split('|'); az[(p[0], int(p[1]), int(p[2]))] += v['apt']
    r1['zonas_com_QT_APTOS_ZONA_diferente_do_bweb'] = sum(1 for z in az if az[z] != aptz1.get(z))
    r1['soma_QT_APTOS_ZONA'] = sum(aptz1.values()); r1['aptos_bweb'] = sum(az.values()); r1['soma_QT_SECOES_ZONA'] = sum(secz1.values())
    r1['historico'] = mh1; r1['candidatos'] = cands1
    res['turno1'] = r1
    grava('parcial_hist.json', res)
    diz('1t conciliado', {k: r1[k] for k in ('zonas_com_d_diferente_de_zero', 'passos', 'passos_que_fecham_na_ordem_de_recebimento', 'passos_que_fecham_com_outra_ordem', 'passos_sem_atribuicao_possivel')}, round(time.time() - t0))
    # ------------------------------------------------ universo (H5): configuracao do site contra o bweb
    uni = {}
    for t, pasta, base in (('2', 'cs_2t', set(chaves)), ('1', 'cs_1t', set(sec1))):
        cs = {}
        for f in sorted(glob.glob(f'{D3DIR}/{pasta}/*.json')):
            c = json.load(open(f))
            for a in c['abr']:
                for mu in a['mu']:
                    for zn in mu['zon']:
                        for s in zn['sec']:
                            if 'nsp' in s and s.get('nsp') not in (None, '', s['ns']):
                                continue
                            cs[f"{a['cd'].upper()}|{int(mu['cd'])}|{int(zn['cd'])}|{int(s['ns'])}"] = (s.get('da'), s.get('ha'))
        so_cs = sorted(set(cs) - base)
        uni[t] = dict(secoes_na_configuracao=len(cs), no_bweb=len(base), so_na_configuracao=len(so_cs), so_no_bweb=sorted(base - set(cs))[:20],
                      so_na_configuracao_com_hora=[k for k in so_cs if cs[k][1]], so_na_configuracao_sem_hora=len([k for k in so_cs if not cs[k][1]]))
    res['universo'] = uni
    grava('parcial_hist.json', res)
    diz('hist pronto', round(time.time() - t0))


# ============================================================================================ REGRESSÃO
def _ids(*cols):
    """Um inteiro por combinação das colunas."""
    if len(cols) == 1:
        return np.unique(cols[0], return_inverse=True)[1]
    return np.unique(np.column_stack(cols), axis=0, return_inverse=True)[1].ravel()


def absorve(M, fes, w, tol=1e-10, maxit=5000):
    """Tira de cada coluna de M as médias ponderadas dos grupos de cada efeito fixo (projeções alternadas se 2)."""
    M = np.array(M, float)
    if M.ndim == 1:
        M = M[:, None]
    sws = [np.bincount(g, weights=w) for g in fes]
    for j in range(M.shape[1]):
        x = M[:, j]
        for it in range(maxit):
            x0 = x
            for g, sw in zip(fes, sws):
                x = x - (np.bincount(g, weights=w * x, minlength=len(sw)) / sw)[g]
            if len(fes) == 1 or np.abs(x - x0).max() <= tol * max(1.0, np.abs(x).max()):
                break
        M[:, j] = x
    return M


class Modelo:
    """MQO ponderado com efeitos fixos absorvidos e erro CR1 agrupado. Guarda o que não depende de y, para que
    plantios que só mexem em y saiam depressa."""

    def __init__(self, X, fes, w, cl, nomes):
        X = np.asarray(X, float)
        if X.ndim == 1:
            X = X[:, None]
        n = len(X); fica = np.ones(n, bool)
        while True:                       # tira grupos de uma observação só, de forma iterada
            mudou = False
            for g in fes:
                cnt = np.bincount(g[fica], minlength=g.max() + 1)
                so = fica & (cnt[g] < 2)
                if so.any():
                    fica &= ~so; mudou = True
            if not mudou:
                break
        self.fica = fica; self.nomes = list(nomes)
        self.fes = [np.unique(g[fica], return_inverse=True)[1] for g in fes]
        self.w = np.asarray(w, float)[fica]
        self.cl = np.unique(np.asarray(cl)[fica], return_inverse=True)[1]
        self.G = int(self.cl.max() + 1) if len(self.cl) else 0
        self.n = int(fica.sum()); self.k = X.shape[1]
        self.Xd = absorve(X[fica], self.fes, self.w)
        XtX = (self.Xd * self.w[:, None]).T @ self.Xd
        try:
            self.inv = np.linalg.inv(XtX)
        except np.linalg.LinAlgError:
            self.inv = np.linalg.pinv(XtX)
        self.P = self.inv @ (self.Xd * self.w[:, None]).T     # b = P yd
        self.grupos = [int(g.max() + 1) for g in self.fes]

    def ajusta(self, y, so_residuo=False):
        yd = absorve(np.asarray(y, float)[self.fica], self.fes, self.w)[:, 0]
        b = self.P @ yd
        e = yd - self.Xd @ b
        if so_residuo:
            return e
        S = np.zeros((self.G, self.k))
        for j in range(self.k):
            S[:, j] = np.bincount(self.cl, weights=self.w * self.Xd[:, j] * e, minlength=self.G)
        c = self.G / (self.G - 1) * (self.n - 1) / (self.n - self.k) if self.G > 1 else float('nan')
        V = c * self.inv @ (S.T @ S) @ self.inv
        return b, np.sqrt(np.diag(V))

    def coef(self, y, nome=None):
        b, se = self.ajusta(y)
        j = 0 if nome is None else self.nomes.index(nome)
        return linha(b[j], se[j], self.n, self.G)


def linha(b, se, n, G, **mais):
    z = b / se if se > 0 else float('nan')
    d = dict(beta=float(b), ep=float(se), z=float(z), p=pnorm(z), ic95=[float(b - 1.96 * se), float(b + 1.96 * se)], n=int(n), municipios=int(G))
    d.update(mais)
    return d


def universo(A, prorrog=True, perfil=True):
    """Universo G2: Brasil, sem junta, pareada, 30 válidos nos dois turnos, com perfil."""
    V1 = A['comp1'] - A['B1'] - A['N1']; V2 = A['L2'] + A['R2']
    U = (A['exterior'] == 0) & (A['junta'] == 0) & A['tem1'] & (V1 >= 30) & (V2 >= 30) & (A['comp1'] > 0)
    if perfil:
        U &= ~np.isnan(A['f60'])
    if not prorrog:
        U &= A['prorrog'] == 0
    return U


NOMES_CTRL = ['f13', 'f22', 'f14', 'f55', 'f70', 'fB', 'fN', 'dcomp', 'lnapt', 'f60']


def controles(A, comp2=None, idade=True, outros=('14', '55', '70')):
    c1 = np.maximum(A['comp1'], 1).astype(float)
    comp2 = A['comp2'] if comp2 is None else comp2
    cols = [A['L1'] / c1, A['R1'] / c1] + [A['c' + c] / c1 for c in outros] + [A['B1'] / c1, A['N1'] / c1,
            (comp2 - A['comp1']) / np.maximum(A['apt2'], 1), np.log(np.maximum(A['apt2'], 1))]
    if idade:
        cols.append(np.nan_to_num(A['f60']))
    return np.column_stack(cols)


def fatia(L, R):
    return 100.0 * L / np.maximum(L + R, 1)


def troca(rng, L, R, taxa, onde):
    """Troca binomial de R para L: T ~ Binomial(L + R, taxa), limitado a R, nas seções marcadas. taxa pode ser vetor."""
    V = L + R
    p = np.broadcast_to(np.asarray(taxa, float), V.shape)
    T = np.zeros(len(V), np.int64)
    T[onde] = np.minimum(rng.binomial(V[onde], np.clip(p[onde], 0, 1)), R[onde])
    return L + T, R - T


def entrada(rng, L, R, comp, taxa, onde):
    """Entrada de eleitores reais: N ~ Binomial(L + R, taxa) eleitores novos, todos de Lula."""
    V = L + R; N = np.zeros(len(V), np.int64)
    N[onde] = rng.binomial(V[onde], taxa)
    return L + N, R, comp + N


def abstencao(rng, L, R, comp, taxa, onde):
    """Abstenção pura: N ~ Binomial(R, min(1, taxa (L + R) / R)) eleitores de Flávio a menos."""
    V = L + R; N = np.zeros(len(V), np.int64)
    p = np.clip(taxa * V / np.maximum(R, 1), 0, 1)
    N[onde] = rng.binomial(R[onde], p[onde])
    return L, R - N, comp - N


# ============================================================================================ PARTE 1 (D3-5)
def modo_d35():
    t0 = time.time()
    A, chaves, ufs, meta = carrega_base()
    rng = np.random.default_rng(SEMENTE + 35)
    n = len(chaves)
    L2, R2 = A['L2'].astype(np.int64), A['R2'].astype(np.int64); V2 = L2 + R2
    y = fatia(L2, R2)
    U = universo(A, prorrog=False)
    cedo = A['ret'] == 0; raj = A['ret'] == 1; tardia = A['ret'] > 0
    emin = np.floor(np.nan_to_num(A['emi'], nan=-1)).astype(np.int64)
    res = {'universo': dict(secoes_no_universo_sem_prorrogadas=int(U.sum()), cedo_no_universo=int((U & cedo).sum()), sem_emissao=int((U & np.isnan(A['emi'])).sum()),
                            cedo_brasil=int((cedo & (A['exterior'] == 0)).sum()))}
    U &= ~np.isnan(A['emi'])
    # locais mistos pela estrutura (Brasil, sem junta, sem prorrogação)
    estr = (A['exterior'] == 0) & (A['junta'] == 0) & (A['prorrog'] == 0)
    nl = A['loc_id'].max() + 1
    tem_c = np.bincount(A['loc_id'][estr & cedo], minlength=nl) > 0; tem_t = np.bincount(A['loc_id'][estr & tardia], minlength=nl) > 0
    misto = (tem_c & tem_t)[A['loc_id']]
    res['universo']['locais_mistos_estrutura'] = int((tem_c & tem_t).sum())
    res['universo']['secoes_em_locais_mistos_estrutura'] = dict(cedo=int((estr & misto & cedo).sum()), tardias=int((estr & misto & tardia).sum()))
    val_depois = int(V2[tardia].sum()); res['validos_recebidos_depois_da_retencao'] = val_depois
    res['validos_recebidos_antes'] = int(V2[cedo].sum())
    X = controles(A); Xs = controles(A, idade=False)
    E = cedo.astype(float)
    amostras = {
        'A': dict(m=U & misto, fes=('loc_id', 'emin'), rot='mesmo prédio: locais mistos, efeito fixo de local e de minuto de emissão'),
        'B': dict(m=U & (cedo | raj), fes=('zona_id', 'emin'), rot='gêmeas de canal: cedo contra rajada das 19:03, efeito fixo de zona e de minuto de emissão'),
        'C': dict(m=U & (cedo | (tardia & (A['emi'] < 17 * 60 + 8))), fes=('zona_id',), rot='cedo contra tardias da mesma zona com emissão antes de 17:08, efeito fixo de zona'),
        'C_com_minuto': dict(m=U & (cedo | (tardia & (A['emi'] < 17 * 60 + 8))), fes=('zona_id', 'emin'), rot='C com efeito fixo de minuto de emissão (ao lado)'),
    }
    FE = {'loc_id': A['loc_id'], 'zona_id': A['zona_id'], 'emin': emin}
    mods = {}

    def monta(m, fes, Xc, w, trat):
        idx = np.flatnonzero(m)
        return idx, Modelo(np.column_stack([trat[idx], Xc[idx]]), [_ids(FE[f][idx]) for f in fes], w[idx], A['mun_id'][idx], ['E'] + ['c%d' % i for i in range(Xc.shape[1])])

    def margem(b):
        return 2 * (-b) / 100 * val_depois
    obs = {}
    for nome, a in amostras.items():
        idx, M = monta(a['m'], a['fes'], X, V2.astype(float), E)
        mods[nome] = (idx, M)
        r = M.coef(y[idx], 'E')
        f = idx[M.fica]
        r.update(descricao=a['rot'], cedo=int(cedo[f].sum()), tardias=int((~cedo[f]).sum()), grupos_de_efeito_fixo=M.grupos,
                 ufs=int(len(np.unique(A['uf_id'][f]))),
                 margem_implicada=margem(r['beta']), margem_ic95=[margem(r['ic95'][1]), margem(r['ic95'][0])],
                 fracao_da_margem=margem(r['beta']) / MARGEM,
                 emd_80=(Z001 if nome == 'A' else Z01) * r['ep'] + Z80 * r['ep'])
        # bruto, sem modelo: médias ponderadas
        wc = V2[f][cedo[f]]; wt = V2[f][~cedo[f]]
        y1 = fatia(A['L1'], A['R1'])
        r['bruto'] = dict(fatia_2t_cedo=float(np.average(y[f][cedo[f]], weights=wc)), fatia_2t_tardias=float(np.average(y[f][~cedo[f]], weights=wt)),
                          fatia_1t_dos_dois_cedo=float(np.average(y1[f][cedo[f]], weights=wc)), fatia_1t_dos_dois_tardias=float(np.average(y1[f][~cedo[f]], weights=wt)))
        r['bruto']['virada_cedo'] = r['bruto']['fatia_2t_cedo'] - r['bruto']['fatia_1t_dos_dois_cedo']
        r['bruto']['virada_tardias'] = r['bruto']['fatia_2t_tardias'] - r['bruto']['fatia_1t_dos_dois_tardias']
        r['bruto']['diferenca_de_virada_cedo_menos_tardias'] = r['bruto']['virada_cedo'] - r['bruto']['virada_tardias']
        # sem a idade
        _, Ms = monta(a['m'], a['fes'], Xs, V2.astype(float), E)
        r['sem_idade'] = Ms.coef(y[idx], 'E')
        obs[nome] = r
        diz('D3-5', nome, round(r['beta'], 4), round(r['ep'], 4), 'n', r['n'], 'cedo', r['cedo'])
    res['observado'] = obs
    grava('parcial_d35.json', res)
    # ---------------- placebos
    y1 = fatia(A['L1'], A['R1']); V1d = (A['L1'] + A['R1']).astype(float)
    f22 = fatia(A['L22'], A['R22'])
    okp = A['tem22'] & ((A['L22'] + A['R22']) >= 30) & (V1d >= 30)
    pb = {}
    for nome in ('A', 'B', 'C'):
        a = amostras[nome]
        idx = np.flatnonzero(a['m'] & okp)
        M = Modelo(np.column_stack([E[idx], f22[idx]]), [_ids(FE[f][idx]) for f in a['fes']], V1d[idx], A['mun_id'][idx], ['E', 'f22'])
        pb['1_desfecho_anterior_' + nome] = dict(M.coef(y1[idx], 'E'), cedo=int(cedo[idx][M.fica].sum()))
    # (2) corte falso dentro do depois
    m2 = U & (raj | ((A['rec_s'] >= 19 * 3600 + 5 * 60) & (A['rec_s'] < 19 * 3600 + 31 * 60)))
    idx = np.flatnonzero(m2)
    M = Modelo(np.column_stack([raj[idx].astype(float), X[idx]]), [_ids(A['zona_id'][idx]), _ids(emin[idx])], V2[idx].astype(float), A['mun_id'][idx], ['E'] + NOMES_CTRL)
    pb['2_rajada_contra_19h05_a_19h30'] = dict(M.coef(y[idx], 'E'), rajada=int(raj[idx][M.fica].sum()), outras=int((~raj[idx][M.fica]).sum()))
    # (3) 1o turno: três primeiros minutos do recebimento contra as seguintes da zona
    e1 = (A['rec1_s'] >= 17 * 3600 + 8 * 60) & (A['rec1_s'] < 17 * 3600 + 11 * 60)
    m3 = (A['exterior'] == 0) & (A['junta1'] == 0) & A['tem1'] & okp & (A['enc1'] < 18 * 60 + 30) & (A['emi1'] < 17 * 60 + 11)
    idx = np.flatnonzero(m3)
    em1 = np.floor(A['emi1'][idx]).astype(np.int64)
    M = Modelo(np.column_stack([e1[idx].astype(float), f22[idx]]), [_ids(A['zona_id'][idx]), _ids(em1)], V1d[idx], A['mun_id'][idx], ['E', 'f22'])
    pb['3_primeiro_turno_primeiras_recebidas'] = dict(M.coef(y1[idx], 'E'), primeiras=int(e1[idx][M.fica].sum()), seguintes=int((~e1[idx][M.fica]).sum()),
                                                     primeiras_no_brasil=int((e1 & (A['exterior'] == 0)).sum()))
    res['placebos'] = pb
    res['placebos_do_criterio'] = {k: pb[k]['beta'] for k in ('1_desfecho_anterior_A', '1_desfecho_anterior_B', '2_rajada_contra_19h05_a_19h30', '3_primeiro_turno_primeiras_recebidas')}
    grava('parcial_d35.json', res)
    diz('placebos', {k: (round(v['beta'], 4), round(v['ep'], 4)) for k, v in pb.items()})
    # ---------------- calibração: troca nas tardias
    cal = {}
    alvo = U & tardia
    NREP = 200
    for sentido, xs in (('a_favor_de_lula', (0.45, 0.90, 1.79)), ('espelho_a_favor_de_flavio', (0.45, 1.79))):
        for x in xs:
            inc = {k: [] for k in ('A', 'B', 'C')}; zz = {k: [] for k in inc}; crit = {k: 0 for k in inc}
            for rep in range(NREP):
                if sentido == 'a_favor_de_lula':
                    Lp, Rp = troca(rng, L2, R2, x / 100, alvo)
                else:
                    Rp, Lp = troca(rng, R2, L2, x / 100, alvo)
                yp = fatia(Lp, Rp)
                for k in inc:
                    idx, M = mods[k]
                    b, se = M.ajusta(yp[idx])
                    d = b[0] - obs[k]['beta']; inc[k].append(d); zz[k].append(d / se[0])
                    zc = Z001 if k == 'A' else Z01
                    if sentido == 'a_favor_de_lula':
                        crit[k] += int(b[0] <= -0.45 and b[0] / se[0] <= -zc)
                    else:
                        crit[k] += int(b[0] >= 0.45 and b[0] / se[0] >= zc)
            sg = -1 if sentido == 'a_favor_de_lula' else 1
            cal[f'{sentido}_x{x}'] = {k: dict(esperado=sg * x, incremento_medio=float(np.mean(inc[k])), dp=float(np.std(inc[k])),
                                              vies_relativo=float(np.mean(inc[k]) / (sg * x) - 1),
                                              deteccao=float(np.mean(sg * np.array(zz[k]) >= (Z001 if k == 'A' else Z01))),
                                              cumpre_condicoes_numericas_do_criterio=crit[k] / NREP) for k in inc}
            diz('calibração', sentido, x, {k: (round(v['incremento_medio'], 3), v['deteccao']) for k, v in cal[f'{sentido}_x{x}'].items()})
    res['calibracao'] = dict(repeticoes=NREP, plantios=cal)
    grava('parcial_d35.json', res)
    # ---------------- explicações inocentes (x = 1,79 nas tardias; mesmo efeito na margem que a troca)
    ino = {}
    for nome_i, fn in (('entrada_de_eleitores_reais', entrada), ('abstencao_pura', abstencao)):
        inc = {k: [] for k in ('A', 'B', 'C')}
        for rep in range(100 if nome_i else 0):
            Lp, Rp, cp = fn(rng, L2, R2, A['comp2'].astype(np.int64), 2 * 1.79 / 100, alvo)
            yp = fatia(Lp, Rp); Xp = controles(A, comp2=cp); wp = (Lp + Rp).astype(float)
            for k in inc:
                a = amostras[k]
                idx = mods[k][0]
                M = Modelo(np.column_stack([E[idx], Xp[idx]]), [_ids(FE[f][idx]) for f in a['fes']], wp[idx], A['mun_id'][idx], ['E'] + NOMES_CTRL)
                b, se = M.ajusta(yp[idx])
                inc[k].append(b[0] - obs[k]['beta'])
            if rep == 9:
                diz(nome_i, 'parcial 10', {k: round(float(np.mean(v)), 3) for k, v in inc.items()}, round(time.time() - t0))
        ino[nome_i] = {k: dict(incremento_medio=float(np.mean(v)), dp=float(np.std(v)),
                               razao_para_a_troca_de_mesma_margem=float(np.mean(v) / cal['a_favor_de_lula_x1.79'][k]['incremento_medio'])) for k, v in inc.items()}
        diz(nome_i, ino[nome_i])
    res['explicacoes_inocentes'] = dict(repeticoes=100, x=1.79, plantios=ino,
                                        distingue={k: {c: abs(v[c]['razao_para_a_troca_de_mesma_margem']) < 0.5 for c in v} for k, v in ino.items()})
    # ---------------- veredito
    a, b = obs['A'], obs['B']
    pls = res['placebos_do_criterio']; plac_ok = all(abs(v) < 0.15 for v in pls.values())
    cond_sinal = a['beta'] <= -0.45 and a['p'] < 0.001 and b['beta'] <= -0.45 and b['p'] < 0.01 and plac_ok
    espelho = a['beta'] >= 0.45 and a['p'] < 0.001 and b['beta'] >= 0.45 and b['p'] < 0.01 and plac_ok
    ep_alto = a['ep'] > 0.45 or b['ep'] > 0.45
    c179 = cal['a_favor_de_lula_x1.79']
    sem_poder = ep_alto or c179['A']['deteccao'] < 0.95 or c179['B']['deteccao'] < 0.95
    sigA = a['p'] < 0.001; sigB = b['p'] < 0.01
    clausulas = []
    if (a['beta'] > 0) != (b['beta'] > 0):
        clausulas.append('sinais opostos em A e B')
    if sigA != sigB:
        clausulas.append('significância só numa das duas')
    if not plac_ok:
        clausulas.append('placebo de 0,15 ou mais: ' + ', '.join(f'{k} = {v:+.3f}' for k, v in pls.items() if abs(v) >= 0.15))
    if ep_alto:
        clausulas.append('erro padrão acima de 0,45')
    sem_sinal = a['ic95'][0] > -0.90 and b['ic95'][0] > -0.90
    sem_sinal_forte = a['ic95'][0] > -0.45 and b['ic95'][0] > -0.45
    if cond_sinal:
        v = 'SINAL'
    elif sem_poder:
        v = 'SEM PODER'
    elif clausulas:
        v = 'INCONCLUSIVO'
    elif sem_sinal:
        v = 'SEM SINAL'
    else:
        v = 'INCONCLUSIVO'
    res['veredito'] = dict(veredito=v, condicoes_de_sinal=bool(cond_sinal), espelho_a_favor_de_flavio=bool(espelho), sem_poder=bool(sem_poder),
                           clausulas_de_inconclusivo=clausulas, limites_de_sem_sinal_cumpridos=bool(sem_sinal), sem_sinal_forte=bool(sem_sinal_forte),
                           alcance_pleno_ic_inclui_menos_1_79=bool(a['ic95'][0] <= -1.79 <= a['ic95'][1]),
                           diferenca_para_o_placebo=dict(A=a['beta'] - pb['1_desfecho_anterior_A']['beta'], B=b['beta'] - pb['1_desfecho_anterior_B']['beta']))
    grava('parcial_d35.json', res)
    diz('d35 pronto', res['veredito'], round(time.time() - t0))


# ============================================================================================ PARTE 2 (D3-6)
def rd(r, rec, w, cl, ce, cd, h):
    """Descontinuidade linear local com núcleo triangular. ce = corte à esquerda (s), cd = à direita, h = banda (s).
    Devolve tau, erro agrupado, n de cada lado."""
    x = np.where(rec < ce, rec - ce, rec - cd).astype(float)
    m = ((rec < ce) & (x > -h)) | ((rec >= cd) & (x < h))
    x = x[m]; D = (rec[m] >= cd).astype(float); ww = w[m] * (1 - np.abs(x) / h); rr = r[m]
    Z = np.column_stack([np.ones(len(x)), D, x / 60.0, D * x / 60.0])
    XtX = (Z * ww[:, None]).T @ Z
    try:
        inv = np.linalg.inv(XtX)
    except np.linalg.LinAlgError:
        return dict(tau=float('nan'), ep=float('nan'), z=float('nan'), p=float('nan'), ic95=[float('nan')] * 2, n_antes=int((D == 0).sum()), n_depois=int((D == 1).sum()))
    b = inv @ (Z * ww[:, None]).T @ rr
    e = rr - Z @ b
    g = np.unique(cl[m], return_inverse=True)[1]; G = g.max() + 1
    S = np.zeros((G, 4))
    for j in range(4):
        S[:, j] = np.bincount(g, weights=ww * Z[:, j] * e, minlength=G)
    c = G / (G - 1) * (len(x) - 1) / (len(x) - 4)
    V = c * inv @ (S.T @ S) @ inv
    se = float(np.sqrt(V[1, 1])); tau = float(b[1])
    return dict(tau=tau, ep=se, z=tau / se, p=pnorm(tau / se), ic95=[tau - 1.96 * se, tau + 1.96 * se], n_antes=int((D == 0).sum()), n_depois=int((D == 1).sum()), grupos=int(G))


H = lambda h, m, s=0: h * 3600 + m * 60 + s


def modo_d36():
    t0 = time.time()
    A, chaves, ufs, meta = carrega_base()
    rng = np.random.default_rng(SEMENTE + 36)
    L2, R2 = A['L2'].astype(np.int64), A['R2'].astype(np.int64); V2 = L2 + R2
    comp2 = A['comp2'].astype(np.int64)
    y = fatia(L2, R2)
    U = universo(A, prorrog=True)
    iu = np.flatnonzero(U)
    X = controles(A)
    Mn = Modelo(X[iu], [_ids(A['zona_id'][iu])], V2[iu].astype(float), A['mun_id'][iu], NOMES_CTRL)
    fu = iu[Mn.fica]                      # seções com resíduo
    res = {'universo': dict(secoes=int(U.sum()), com_residuo=int(len(fu)), zonas=Mn.grupos[0], prorrogadas_no_ajuste=int(A['prorrog'][fu].sum()))}

    def residuo(yv, M=Mn, f=fu):
        r = np.full(len(yv), np.nan); r[f] = M.ajusta(yv[iu] if M is Mn else yv, so_residuo=True)
        return r
    r = residuo(y)
    res['universo']['dp_do_residuo'] = float(np.sqrt(np.average(r[fu] ** 2, weights=V2[fu])))
    np_ = A['prorrog'] == 0
    rec = A['rec_s']; w = V2.astype(float); zid = A['zona_id']; mid = A['mun_id']
    S1 = np.zeros(len(y), bool); S1[fu] = True; S1 &= np_       # amostra dos estimadores
    val_1950 = int(V2[rec >= H(19, 50)].sum()); val_tot = int(V2.sum())
    res['validos_recebidos_de_19h50_em_diante'] = val_1950; res['validos_totais'] = val_tot
    # desfecho placebo: 1o turno controlado por 2022
    y1 = fatia(A['L1'], A['R1']); V1d = (A['L1'] + A['R1']).astype(float); f22 = fatia(A['L22'], A['R22'])
    Up = (A['exterior'] == 0) & (A['junta'] == 0) & A['tem1'] & A['tem22'] & ((A['L22'] + A['R22']) >= 30) & (V1d >= 30)
    ip = np.flatnonzero(Up)
    Mp = Modelo(f22[ip][:, None], [_ids(zid[ip])], V1d[ip], mid[ip], ['f22'])
    rp = np.full(len(y), np.nan); rp[ip[Mp.fica]] = Mp.ajusta(y1[ip], so_residuo=True)
    Sp = ~np.isnan(rp) & np_
    Sp1 = ~np.isnan(rp) & (A['junta1'] == 0) & (A['enc1'] < 18 * 60 + 30) & (A['rec1_s'] >= 0)
    res['universo']['placebo_com_residuo'] = int((~np.isnan(rp)).sum())

    # ---------------- (1) descontinuidade
    def RD(rv, S, relogio, ce, cd, h, cl=None, peso=None):
        cl = zid if cl is None else cl
        peso = w if peso is None else peso
        return rd(rv[S], relogio[S], peso[S], cl[S], ce, cd, h * 60)
    e1 = {}
    for h in (8, 4, 16):
        o = RD(r, S1, rec, H(19, 48), H(19, 50), h)
        o['margem_implicada'] = 2 * o['tau'] / 100 * val_1950; o['margem_ic95'] = [2 * v / 100 * val_1950 for v in o['ic95']]
        o['fracao_da_margem'] = o['margem_implicada'] / MARGEM
        o['erro_por_municipio'] = RD(r, S1, rec, H(19, 48), H(19, 50), h, cl=mid)['ep']
        e1[f'banda_{h}'] = o
    e1['zonas_com_os_dois_lados_banda_8'] = int(len(set(zid[S1 & (rec < H(19, 48)) & (rec >= H(19, 40))]) & set(zid[S1 & (rec >= H(19, 50)) & (rec < H(19, 58))])))
    e1['placebo_desfecho_anterior'] = {f'banda_{h}': RD(rp, Sp, rec, H(19, 48), H(19, 50), h, peso=V1d) for h in (8, 4, 16)}
    falsos = {}
    for nome, lista in (('grade_do_registro_12', [H(20, 10) + 300 * i for i in range(12)]), ('vinte_de_3_em_3', [H(20, 8) + 180 * i for i in range(20)])):
        falsos[nome] = [dict(corte=hhmmss(c), **RD(r, S1, rec, c, c, 8)) for c in lista]
    e1['cortes_falsos'] = falsos
    e1['maior_salto_falso_em_modulo'] = {k: float(max(abs(x['tau']) for x in v)) for k, v in falsos.items()}
    e1['cortes_falsos_com_p_abaixo_de_0_001'] = {k: int(sum(x['p'] < 0.001 for x in v)) for k, v in falsos.items()}
    e1['primeiro_turno_pausas'] = {nome: dict(RD(rp, Sp1, A['rec1_s'], ce, cd, 8, peso=V1d), corte=f'{hhmmss(ce)} a {hhmmss(cd)}')
                                   for nome, ce, cd in (('18h02', H(18, 2), H(18, 8)), ('18h50', H(18, 50), H(18, 53)), ('19h32', H(19, 32), H(19, 59)))}
    e1['degraus_de_vazao_exploratorio'] = {hhmmss(c)[:5]: {f'banda_{h}': RD(r, S1, rec, c, c, h) for h in (8, 2)}
                                          for c in (H(19, 12), H(19, 14), H(19, 18), H(19, 24), H(19, 30), H(20, 0))}
    # bruto em volta da pausa (sem modelo)
    ja = S1 & (A['pausa'] == 1); jd = S1 & (A['pausa'] == 2)
    e1['bruto_janelas_de_8_min'] = dict(secoes_antes=int(ja.sum()), secoes_depois=int(jd.sum()),
                                         fatia_2t_antes=float(np.average(y[ja], weights=w[ja])), fatia_2t_depois=float(np.average(y[jd], weights=w[jd])),
                                         fatia_1t_dos_dois_antes=float(np.average(y1[ja], weights=w[ja])), fatia_1t_dos_dois_depois=float(np.average(y1[jd], weights=w[jd])),
                                         residuo_medio_antes=float(np.average(r[ja], weights=w[ja])), residuo_medio_depois=float(np.average(r[jd], weights=w[jd])))
    res['e1_descontinuidade'] = e1
    grava('parcial_d36.json', res)
    diz('(1)', {k: (round(v['tau'], 4), round(v['ep'], 4)) for k, v in e1.items() if k.startswith('banda')}, 'placebo', round(e1['placebo_desfecho_anterior']['banda_8']['tau'], 4), 'falsos', e1['maior_salto_falso_em_modulo'])

    # ---------------- (2) inclinação dentro da zona
    pos = A['pos_zona']
    S2 = S1 & ~np.isnan(pos)
    i2 = np.flatnonzero(S2)
    M2 = Modelo(pos[i2][:, None], [_ids(zid[i2])], w[i2], mid[i2], ['pos'])
    M2z = Modelo(pos[i2][:, None], [_ids(zid[i2])], w[i2], zid[i2], ['pos'])
    e2 = M2.coef(r[i2], 'pos'); e2['erro_por_zona'] = M2z.coef(r[i2], 'pos')['ep']
    e2['margem_implicada'] = e2['beta'] / 100 * val_tot; e2['margem_ic95'] = [v / 100 * val_tot for v in e2['ic95']]
    e2['fracao_da_margem'] = e2['margem_implicada'] / MARGEM
    S2p = Sp & ~np.isnan(pos); i2p = np.flatnonzero(S2p)
    M2p = Modelo(pos[i2p][:, None], [_ids(zid[i2p])], V1d[i2p], mid[i2p], ['pos'])
    e2['placebo_desfecho_anterior'] = M2p.coef(rp[i2p], 'pos')
    # bruto: terços da posição
    t3 = np.digitize(pos[i2], [1 / 3, 2 / 3])
    e2['bruto_por_terco_da_posicao'] = [dict(terco=int(q) + 1, secoes=int((t3 == q).sum()), fatia_2t=float(np.average(y[i2][t3 == q], weights=w[i2][t3 == q])),
                                             fatia_1t_dos_dois=float(np.average(y1[i2][t3 == q], weights=w[i2][t3 == q])),
                                             residuo_medio=float(np.average(r[i2][t3 == q], weights=w[i2][t3 == q]))) for q in range(3)]
    res['e2_inclinacao'] = e2
    diz('(2)', round(e2['beta'], 4), round(e2['ep'], 4), 'placebo', round(e2['placebo_desfecho_anterior']['beta'], 4))

    # ---------------- (3) deslocados
    e3 = {}
    i3 = np.flatnonzero(S1)
    enc_c = np.nan_to_num(A['enc'], nan=1020.0) - 1020.0
    trat = {'desloc_30': np.nan_to_num(A['desloc'], nan=-1) >= 30, 'desloc_60': np.nan_to_num(A['desloc'], nan=-1) >= 60, 'cauda': A['cauda'] == 1}
    M3 = {}
    for nome, tr in trat.items():
        M = Modelo(np.column_stack([tr[i3].astype(float), X[i3]]), [_ids(A['loc_id'][i3])], w[i3], mid[i3], ['T'] + NOMES_CTRL)
        M3[nome] = M
        o = M.coef(y[i3], 'T')
        f = i3[M.fica]
        val_g = int(V2[tr].sum())
        o.update(tratadas_na_conta=int(tr[f].sum()), tratadas_no_bweb=int(tr.sum()), validos_das_tratadas_no_bweb=val_g,
                 margem_implicada=2 * o['beta'] / 100 * val_g, margem_ic95=[2 * v / 100 * val_g for v in o['ic95']])
        Mc = Modelo(np.column_stack([tr[i3].astype(float), X[i3], enc_c[i3]]), [_ids(A['loc_id'][i3])], w[i3], mid[i3], ['T'] + NOMES_CTRL + ['enc'])
        o['com_controle_do_encerramento'] = Mc.coef(y[i3], 'T')
        ipp = np.flatnonzero(Sp)
        Mpp = Modelo(np.column_stack([tr[ipp].astype(float), f22[ipp]]), [_ids(A['loc_id'][ipp])], V1d[ipp], mid[ipp], ['T', 'f22'])
        o['placebo_desfecho_anterior'] = Mpp.coef(y1[ipp], 'T')
        # bruto
        tt = tr[f]
        o['bruto'] = dict(virada_tratadas=float(np.average((y - y1)[f][tt], weights=w[f][tt])), virada_demais=float(np.average((y - y1)[f][~tt], weights=w[f][~tt])))
        e3[nome] = o
        diz('(3)', nome, round(o['beta'], 4), round(o['ep'], 4), 'placebo', round(o['placebo_desfecho_anterior']['beta'], 4))
    res['e3_deslocados'] = e3
    grava('parcial_d36.json', res)

    # ---------------- calibração de (1)
    alvo = rec >= H(19, 50)
    cal1 = {}
    NREP = 100
    for sentido, xs in (('a_favor_de_lula', (0.45, 0.9, 2.1)), ('espelho_a_favor_de_flavio', (0.45,))):
        sg = 1 if sentido == 'a_favor_de_lula' else -1
        for x in xs:
            inc = {h: [] for h in (8, 4, 16)}; zz = {h: [] for h in inc}; crit = 0
            for rep in range(NREP):
                if sg > 0:
                    Lp, Rp = troca(rng, L2, R2, x / 100, alvo)
                else:
                    Rp, Lp = troca(rng, R2, L2, x / 100, alvo)
                rv = residuo(fatia(Lp, Rp))
                tt = {}
                for h in inc:
                    o = RD(rv, S1, rec, H(19, 48), H(19, 50), h)
                    d = o['tau'] - e1[f'banda_{h}']['tau']; inc[h].append(d); zz[h].append(d / o['ep']); tt[h] = o
                crit += int(sg * tt[8]['tau'] >= 0.45 and tt[8]['p'] < 0.001 and all(sg * tt[h]['tau'] > 0 and tt[h]['p'] < 0.01 for h in (4, 16)))
            cal1[f'{sentido}_x{x}'] = {f'banda_{h}': dict(esperado=sg * x, incremento_medio=float(np.mean(inc[h])), dp=float(np.std(inc[h])),
                                                         devolucao=float(np.mean(inc[h]) / (sg * x)),
                                                         deteccao=float(np.mean(sg * np.array(zz[h]) >= (Z001 if h == 8 else Z01)))) for h in inc}
            cal1[f'{sentido}_x{x}']['cumpre_condicoes_numericas_de_tau'] = crit / NREP
            diz('cal (1)', sentido, x, {h: (round(float(np.mean(inc[h])), 3), float(np.mean(sg * np.array(zz[h]) >= (Z001 if h == 8 else Z01)))) for h in inc})
    res['e1_calibracao'] = dict(repeticoes=NREP, plantios=cal1, emd_80_banda_8=(Z001 + Z80) * e1['banda_8']['ep'])
    grava('parcial_d36.json', res)
    # explicações inocentes de (1)
    ino = {}
    medz = np.zeros(zid.max() + 1)
    for z_ in np.unique(zid):
        pass
    o_ = np.lexsort((rec, zid)); zs = zid[o_]; ini = np.r_[0, np.flatnonzero(np.diff(zs)) + 1, len(zs)]
    for a_, b_ in zip(ini[:-1], ini[1:]):
        medz[zs[a_]] = np.median(rec[o_[a_:b_]])
    zona_tarde = medz[zid] >= H(19, 50)
    inc = []
    for rep in range(30):
        Lp, Rp = troca(rng, L2, R2, 2.1 / 100, zona_tarde)
        inc.append(RD(residuo(fatia(Lp, Rp)), S1, rec, H(19, 48), H(19, 50), 8)['tau'] - e1['banda_8']['tau'])
    ino['composicao_zona_inteira_depois_da_pausa'] = dict(secoes_alteradas=int(zona_tarde.sum()), incremento_medio=float(np.mean(inc)), dp=float(np.std(inc)))
    for nome_i, fn in (('entrada_de_eleitores_reais', entrada), ('abstencao_pura', abstencao)):
        inc = []
        for rep in range(30):
            Lp, Rp, cp = fn(rng, L2, R2, comp2, 2 * 2.1 / 100, alvo)
            Xp = controles(A, comp2=cp); wp = (Lp + Rp).astype(float)
            Mq = Modelo(Xp[iu], [_ids(zid[iu])], wp[iu], mid[iu], NOMES_CTRL)
            rv = np.full(len(y), np.nan); rv[iu[Mq.fica]] = Mq.ajusta(fatia(Lp, Rp)[iu], so_residuo=True)
            inc.append(rd(rv[S1], rec[S1], wp[S1], zid[S1], H(19, 48), H(19, 50), 480)['tau'] - e1['banda_8']['tau'])
        ino[nome_i] = dict(incremento_medio=float(np.mean(inc)), dp=float(np.std(inc)))
        diz('inocente (1)', nome_i, ino[nome_i])
    ref = cal1['a_favor_de_lula_x2.1']['banda_8']['incremento_medio']
    for k in ino:
        ino[k]['razao_para_a_troca_de_mesma_margem'] = ino[k]['incremento_medio'] / ref
        ino[k]['distingue'] = abs(ino[k]['razao_para_a_troca_de_mesma_margem']) < 0.5
    res['e1_explicacoes_inocentes'] = dict(repeticoes=30, x=2.1, plantios=ino)
    grava('parcial_d36.json', res)

    # ---------------- calibração de (2): rampas
    cal2 = {}
    u = A['u_nac']; pz = np.nan_to_num(pos, nan=0.0)
    for forma, dose in (('ordem_nacional', u), ('posicao_na_zona', pz)):
        for x in (0.9, 1.8, 3.6):
            inc = []; crit = 0
            for rep in range(NREP):
                Lp, Rp = troca(rng, L2, R2, x * dose / 100, np.ones(len(y), bool))
                rv = residuo(fatia(Lp, Rp))
                b, se = M2.ajusta(rv[i2])
                inc.append(b[0] - e2['beta']); crit += int(b[0] >= 0.9 and b[0] / se[0] >= Z001)
            cal2[f'{forma}_x{x}'] = dict(plantado=x, incremento_medio=float(np.mean(inc)), dp=float(np.std(inc)), devolucao=float(np.mean(inc) / x),
                                         deteccao_do_incremento=float(np.mean(np.array(inc) / e2['ep'] >= Z001)), cumpre_theta_0_9_e_p=crit / NREP)
            diz('cal (2)', forma, x, cal2[f'{forma}_x{x}'])
    res['e2_calibracao'] = dict(repeticoes=NREP, plantios=cal2, emd_80=(Z001 + Z80) * e2['ep'])
    grava('parcial_d36.json', res)
    # ---------------- calibração de (3): +5 pontos nos deslocados
    cal3 = {}
    for nome, tr in trat.items():
        inc = []; det = 0
        for rep in range(200 if nome == 'desloc_30' else 50):
            Lp, Rp = troca(rng, L2, R2, 0.05, tr)
            b, se = M3[nome].ajusta(fatia(Lp, Rp)[i3])
            inc.append(b[0] - e3[nome]['beta']); det += int((b[0] - e3[nome]['beta']) / se[0] >= Z001)
        cal3[nome] = dict(plantado=5.0, incremento_medio=float(np.mean(inc)), dp=float(np.std(inc)), deteccao=det / len(inc), emd_80=(Z001 + Z80) * e3[nome]['ep'])
    res['e3_calibracao'] = cal3
    # inocente em (3): entrada de eleitores reais nos deslocados (mesma margem que troca de 5%)
    inc = []
    tr = trat['desloc_30']
    for rep in range(30):
        Lp, Rp, cp = entrada(rng, L2, R2, comp2, 0.10, tr)
        Xp = controles(A, comp2=cp); wp = (Lp + Rp).astype(float)
        M = Modelo(np.column_stack([tr[i3].astype(float), Xp[i3]]), [_ids(A['loc_id'][i3])], wp[i3], mid[i3], ['T'] + NOMES_CTRL)
        inc.append(M.ajusta(fatia(Lp, Rp)[i3])[0][0] - e3['desloc_30']['beta'])
    res['e3_explicacao_inocente_entrada'] = dict(repeticoes=30, incremento_medio=float(np.mean(inc)), razao_para_a_troca=float(np.mean(inc) / cal3['desloc_30']['incremento_medio']),
                                                 distingue=bool(abs(np.mean(inc) / cal3['desloc_30']['incremento_medio']) < 0.5))
    grava('parcial_d36.json', res)

    # ---------------- vereditos
    V = {}
    b8, b4, b16 = e1['banda_8'], e1['banda_4'], e1['banda_16']
    mf = e1['maior_salto_falso_em_modulo']['grade_do_registro_12']
    plc = e1['placebo_desfecho_anterior']['banda_8']['tau']

    def v1(sg):
        return (sg * b8['tau'] >= 0.45 and b8['p'] < 0.001 and all(sg * b['tau'] > 0 and b['p'] < 0.01 for b in (b4, b16)) and abs(b8['tau']) > mf and abs(plc) < 0.15)
    sem_poder1 = cal1['a_favor_de_lula_x0.45']['banda_8']['deteccao'] < 0.95
    cl = []
    if abs(plc) >= 0.15:
        cl.append(f'desfecho placebo com salto de {plc:+.3f} no mesmo corte')
    if b8['p'] < 0.001 and abs(b8['tau']) <= mf:
        cl.append('tau significativo mas menor que algum corte falso')
    if len({b['tau'] > 0 for b in (b8, b4, b16)}) > 1:
        cl.append('muda de sinal entre bandas')
    ss1 = -0.45 < b8['ic95'][0] and b8['ic95'][1] < 0.45
    V['1_descontinuidade'] = dict(veredito='SINAL' if v1(1) else 'SEM PODER' if sem_poder1 else 'INCONCLUSIVO' if cl else 'SEM SINAL' if ss1 else 'INCONCLUSIVO',
                                  espelho_a_favor_de_flavio=bool(v1(-1)), clausulas_de_inconclusivo=cl, limites_de_sem_sinal_cumpridos=bool(ss1),
                                  maior_que_todos_os_cortes_falsos=dict(grade_12=bool(abs(b8['tau']) > mf), vinte=bool(abs(b8['tau']) > e1['maior_salto_falso_em_modulo']['vinte_de_3_em_3'])))
    pl2 = e2['placebo_desfecho_anterior']['beta']
    s2 = e2['beta'] >= 0.9 and e2['p'] < 0.001 and abs(pl2) < 0.3
    sp2 = cal2['ordem_nacional_x3.6']['cumpre_theta_0_9_e_p'] < 0.95
    ss2 = -0.9 < e2['ic95'][0] and e2['ic95'][1] < 0.9
    V['2_inclinacao'] = dict(veredito='SINAL' if s2 else 'SEM PODER' if sp2 else 'SEM SINAL' if ss2 else 'INCONCLUSIVO',
                             espelho_a_favor_de_flavio=bool(e2['beta'] <= -0.9 and e2['p'] < 0.001 and abs(pl2) < 0.3), limites_de_sem_sinal_cumpridos=bool(ss2),
                             sem_poder_para_a_rampa_nacional=bool(sp2), enxerga_rampa_dentro_da_zona=bool(cal2['posicao_na_zona_x0.9']['cumpre_theta_0_9_e_p'] >= 0.5 or cal2['posicao_na_zona_x1.8']['cumpre_theta_0_9_e_p'] >= 0.95),
                             placebo_abaixo_de_0_3=bool(abs(pl2) < 0.3))
    for nome in trat:
        o = e3[nome]; pl3 = o['placebo_desfecho_anterior']['beta']
        s3 = o['beta'] >= 1.0 and o['p'] < 0.001 and abs(pl3) < 0.3
        sp3 = cal3[nome]['deteccao'] < 0.95
        ss3 = -1.0 < o['ic95'][0] and o['ic95'][1] < 1.0
        V['3_' + nome] = dict(veredito='SINAL' if s3 else 'SEM PODER' if sp3 else 'SEM SINAL' if ss3 else 'INCONCLUSIVO',
                              espelho_a_favor_de_flavio=bool(o['beta'] <= -1.0 and o['p'] < 0.001 and abs(pl3) < 0.3), limites_de_sem_sinal_cumpridos=bool(ss3),
                              placebo_abaixo_de_0_3=bool(abs(pl3) < 0.3))
    res['vereditos'] = V
    grava('parcial_d36.json', res)
    diz('d36 pronto', {k: v['veredito'] for k, v in V.items()}, round(time.time() - t0))


# ============================================================================================ PARTE 4: R1
FAIXAS_R1 = [(0, 1021, 'antes de 17:01'), (1021, 1022, '17:01'), (1022, 1023, '17:02'), (1023, 1025, '17:03 a 17:04'), (1025, 1030, '17:05 a 17:09'),
             (1030, 1040, '17:10 a 17:19'), (1040, 1060, '17:20 a 17:39'), (1060, 1110, '17:40 a 18:29'), (1110, 1140, '18:30 a 18:59'), (1140, 10 ** 6, '19:00 em diante')]


def modo_r1():
    t0 = time.time()
    A, chaves, ufs, meta = carrega_base()
    rng = np.random.default_rng(SEMENTE + 1)
    L2, R2 = A['L2'].astype(np.int64), A['R2'].astype(np.int64); V2 = L2 + R2; comp2 = A['comp2'].astype(np.int64)
    y = fatia(L2, R2); w = V2.astype(float); mid = A['mun_id']
    enc = A['enc']; tem_enc = ~np.isnan(enc)
    d = np.where(tem_enc, np.maximum(0.0, np.nan_to_num(enc) - 1021.0) * 60.0, 0.0)      # segundos depois de 17:01:00
    T = d / 10.0
    res = {}
    # (a) aritmética
    res['a_aritmetica'] = dict(secoes_com_encerramento=int(tem_enc.sum()), secoes_que_encerraram_depois_de_17h01=int((d > 0).sum()),
                               segundos_depois_de_17h01_media=float(d[tem_enc].mean()), mediana=float(np.median(d[tem_enc])),
                               total_que_a_alegacao_preve_transferido=float(T.sum()), margem_que_isso_deslocaria=float(2 * T.sum()),
                               razao_para_a_margem_oficial=float(2 * T.sum() / MARGEM), votos_de_flavio_oficiais=int(R2.sum()), votos_de_lula_oficiais=int(L2.sum()),
                               flavio_teria_sem_a_transferencia=float(R2.sum() + T.sum()),
                               secoes_em_que_T_passa_dos_votos_de_lula=int((T > L2)[tem_enc].sum()), soma_do_excesso_sobre_os_votos_de_lula=float(np.maximum(0, T - L2)[tem_enc].sum()),
                               secoes_em_que_T_passa_do_comparecimento=int((T > comp2)[tem_enc].sum()),
                               entre_as_que_encerraram_de_19h_em_diante=dict(secoes=int((enc >= 1140).sum()), T_medio=float(T[enc >= 1140].mean()) if (enc >= 1140).any() else None,
                                                                              comparecimento_medio=float(comp2[enc >= 1140].mean()) if (enc >= 1140).any() else None,
                                                                              secoes_com_T_acima_dos_votos_de_lula=int(((T > L2) & (enc >= 1140)).sum())))
    U = universo(A, prorrog=True) & tem_enc
    X = controles(A)
    dose = 100.0 * T / np.maximum(V2, 1)
    y1 = fatia(A['L1'], A['R1']); V1d = (A['L1'] + A['R1']).astype(float); f22 = fatia(A['L22'], A['R22'])
    okp = A['tem22'] & ((A['L22'] + A['R22']) >= 30) & (V1d >= 30)

    def conta(S, dz, rot):
        idx = np.flatnonzero(S)
        M = Modelo(np.column_stack([dz[idx], X[idx]]), [_ids(A['loc_id'][idx])], w[idx], mid[idx], ['dose'] + NOMES_CTRL)
        o = M.coef(y[idx], 'dose'); o['descricao'] = rot
        o['dose_media_pontos'] = float(np.average(dz[idx][M.fica], weights=w[idx][M.fica])); o['dose_dp'] = float(np.sqrt(np.cov(dz[idx][M.fica], aweights=w[idx][M.fica])))
        ip = np.flatnonzero(S & okp)
        Mp = Modelo(np.column_stack([dz[ip], f22[ip]]), [_ids(A['loc_id'][ip])], V1d[ip], mid[ip], ['dose', 'f22'])
        o['placebo_desfecho_anterior'] = Mp.coef(y1[ip], 'dose')
        return idx, M, o
    Sp = U & (enc < 1030)
    idx, Mprin, o = conta(Sp, dose, 'principal: seções que encerraram antes de 17:10:00, dose sem limite')
    classe = tem_enc & (enc < 1030)
    somaT = float(T[classe].sum())
    o['soma_de_T_da_classe'] = somaT; o['secoes_da_classe'] = int(classe.sum())
    o['margem_implicada'] = 2 * o['beta'] * somaT; o['margem_ic95'] = [2 * v * somaT for v in o['ic95']]
    o['taxa_implicada_votos_por_10_s'] = o['beta']; o['teto_95_votos_por_10_s'] = o['ic95'][1]
    res['b_dose'] = {'principal': o}
    _, _, o2 = conta(U, np.minimum(dose, 50.0), 'ao lado: todas as seções, dose limitada a 50 pontos')
    res['b_dose']['todas_com_dose_limitada_a_50'] = o2
    grava('parcial_r1.json', res)
    diz('R1 kappa', round(o['beta'], 5), round(o['ep'], 5), 'placebo', round(o['placebo_desfecho_anterior']['beta'], 5), '| todas', round(o2['beta'], 5), round(o2['ep'], 5))
    # (c) dez grupos
    def grupos(S, cod, rotulos):
        idx = np.flatnonzero(S)
        G = len(rotulos)
        Dm = np.column_stack([(cod[idx] == g).astype(float) for g in range(1, G)])
        M = Modelo(np.column_stack([Dm, X[idx]]), [_ids(A['loc_id'][idx])], w[idx], mid[idx], [f'g{g}' for g in range(1, G)] + NOMES_CTRL)
        b, se = M.ajusta(y[idx])
        f = idx[M.fica]; tab = []
        ref_dose = float(np.average(dose[idx][cod[idx] == 0], weights=w[idx][cod[idx] == 0]))
        for g in range(G):
            m = cod[idx] == g; mf = cod[f] == g
            lin = dict(grupo=rotulos[g], secoes=int(m.sum()), encerramento_medio=hhmmss(float(np.mean(enc[idx][m])) * 60), T_medio_previsto_votos=float(np.mean(T[idx][m])),
                       comparecimento_medio=float(np.mean(comp2[idx][m])),
                       fatia_2t=float(np.average(y[idx][m], weights=w[idx][m])), fatia_1t_dos_dois=float(np.average(y1[idx][m], weights=w[idx][m])))
            lin['virada_bruta'] = lin['fatia_2t'] - lin['fatia_1t_dos_dois']
            lin['dose_media_prevista_pontos'] = float(np.average(dose[idx][m], weights=w[idx][m]))
            lin['diferenca_prevista_pela_alegacao'] = lin['dose_media_prevista_pontos'] - ref_dose
            if g:
                lin.update(diferenca_ajustada=float(b[g - 1]), ep=float(se[g - 1]), z=float(b[g - 1] / se[g - 1]), p=pnorm(b[g - 1] / se[g - 1]))
                lin['pelo_menos_metade_do_previsto_com_p_0_001'] = bool(b[g - 1] >= 0.5 * lin['diferenca_prevista_pela_alegacao'] and b[g - 1] > 0 and lin['p'] < 0.001)
            tab.append(lin)
        return tab
    cod = np.zeros(len(y), np.int64)
    for g, (a_, b_, _) in enumerate(FAIXAS_R1):
        cod[(np.nan_to_num(enc) >= a_) & (np.nan_to_num(enc) < b_)] = g
    res['c_dez_grupos_fixos'] = grupos(U, cod, [f[2] for f in FAIXAS_R1])
    q = np.quantile(enc[U], np.arange(1, 10) / 10)
    res['c_decis'] = grupos(U, np.digitize(np.nan_to_num(enc), q), [f'decil {i + 1}' for i in range(10)])
    res['c_resumo'] = dict(grupos_que_confirmam_a_alegacao=int(sum(1 for l in res['c_dez_grupos_fixos'][1:] if l['pelo_menos_metade_do_previsto_com_p_0_001'])),
                           maior_diferenca_ajustada=float(max(l['diferenca_ajustada'] for l in res['c_dez_grupos_fixos'][1:])),
                           menor_diferenca_ajustada=float(min(l['diferenca_ajustada'] for l in res['c_dez_grupos_fixos'][1:])))
    grava('parcial_r1.json', res)
    # calibração: plantar a alegação e versões mais fracas
    cal = {}
    kap = res['b_dose']['principal']['beta']
    for nome, taxa_s, sentido in (('1_voto_a_cada_10_s', 10, 1), ('1_voto_a_cada_100_s', 100, 1), ('1_voto_a_cada_1000_s', 1000, 1), ('espelho_1_voto_a_cada_10_s_de_lula_para_flavio', 10, -1),
                                  ('espelho_1_voto_a_cada_100_s', 100, -1)):
        Tp = np.floor(d / taxa_s + rng.random(len(d))).astype(np.int64)      # arredondamento sorteado: em média d / taxa
        if sentido > 0:
            Tp = np.minimum(Tp, R2); Lp, Rp = L2 + Tp, R2 - Tp
        else:
            Tp = np.minimum(Tp, L2); Lp, Rp = L2 - Tp, R2 + Tp
        b, se = Mprin.ajusta(fatia(Lp, Rp)[idx])
        cal[nome] = dict(esperado=sentido * 10.0 / taxa_s, incremento_de_kappa=float(b[0] - kap), ep=float(se[0]), z_do_incremento=float((b[0] - kap) / se[0]),
                         votos_plantados_na_classe=int(Tp[classe].sum()))
    res['calibracao'] = cal
    res['emd_80_votos_por_10_s'] = (Z001 + Z80) * res['b_dose']['principal']['ep']
    # inocentes
    ino = {}
    Nf = np.floor(d / 100 + rng.random(len(d))).astype(np.int64)
    Lf = np.rint(Nf * L2 / np.maximum(V2, 1)).astype(np.int64)
    for nome, Lp, Rp, cp in (('fila_real_repartida_como_a_secao', L2 + Lf, R2 + (Nf - Lf), comp2 + Nf), ('entrada_de_eleitores_reais_de_lula', L2 + 2 * Nf, R2, comp2 + 2 * Nf)):
        Xp = controles(A, comp2=cp); wp = (Lp + Rp).astype(float)
        dz = 100.0 * T / np.maximum(V2, 1)
        M = Modelo(np.column_stack([dz[idx], Xp[idx]]), [_ids(A['loc_id'][idx])], wp[idx], mid[idx], ['dose'] + NOMES_CTRL)
        b, se = M.ajusta(fatia(Lp, Rp)[idx])
        ino[nome] = dict(incremento_de_kappa=float(b[0] - kap), razao_para_a_transferencia_de_mesma_margem=float((b[0] - kap) / cal['1_voto_a_cada_100_s']['incremento_de_kappa']))
    res['explicacoes_inocentes'] = ino
    # veredito
    o = res['b_dose']['principal']; pl = o['placebo_desfecho_anterior']['beta']
    letra = 'REFUTADA' if o['ic95'][1] < 0.5 else 'CONFIRMADA' if o['ic95'][0] > 0.5 else 'INDEFINIDA'
    sinal = o['beta'] > 0 and o['p'] < 0.001 and o['margem_ic95'][0] >= DEZ_PCT and abs(pl) < abs(o['beta']) / 3
    sem_poder = abs(cal['1_voto_a_cada_10_s']['incremento_de_kappa'] - 1) > 0.25 or cal['1_voto_a_cada_10_s']['z_do_incremento'] < Z001
    semsinal = o['margem_ic95'][1] < DEZ_PCT
    espelho = o['beta'] < 0 and o['p'] < 0.001 and o['margem_ic95'][1] <= -DEZ_PCT and abs(pl) < abs(o['beta']) / 3
    res['veredito'] = dict(alegacao_ao_pe_da_letra=letra, efeito_do_horario_com_alcance='SINAL' if sinal else 'SEM PODER' if sem_poder else 'SEM SINAL' if semsinal else 'INCONCLUSIVO',
                           espelho_a_favor_de_flavio=bool(espelho), placebo=pl, placebo_abaixo_de_um_terco=bool(abs(pl) < abs(o['beta']) / 3))
    grava('parcial_r1.json', res)
    diz('r1 pronto', res['veredito'], round(time.time() - t0))


# ============================================================================================ PARTE 4: R7 e R8
def _serie_nacional():
    """Acumulado nacional do histórico do 2o turno, passo a passo, na ordem de hora e identificador."""
    passos, _, _, _ = le_historico('2')
    ks = sorted(passos, key=lambda x: (passos[x]['t'], x[1]))
    t = np.array([passos[k]['t'] for k in ks]); n = np.array([passos[k]['n'] for k in ks])
    L = np.array([passos[k]['v']['13'] for k in ks]); R = np.array([passos[k]['v']['22'] for k in ks])
    uf = np.array([k[0][0] for k in ks])
    return ks, t, n, L, R, uf


def modo_r7():
    ks, t, n, L, R, uf = _serie_nacional()
    cL, cR, cn = np.cumsum(L), np.cumsum(R), np.cumsum(n)
    res = {'tela': dict(lula=193574, flavio=142169, sem_origem_alegado=165699, soma_das_paginas_implicita=193574 - 165699)}
    # (a) instante com o acumulado exato da tela
    ex = np.flatnonzero((cL == 193574) & (cR == 142169))
    res['a_instante_exato'] = [dict(hora=hhmmss(t[i]), passo=int(i + 1), secoes=int(cn[i]), pct_das_secoes=float(100 * cn[i] / 499248)) for i in ex]
    i_prox = int(np.argmin(np.abs(cL - 193574) + np.abs(cR - 142169)))
    res['a_mais_proximo'] = dict(hora=hhmmss(t[i_prox]), lula=int(cL[i_prox]), flavio=int(cR[i_prox]), secoes=int(cn[i_prox]), distancia=int(abs(cL[i_prox] - 193574) + abs(cR[i_prox] - 142169)))
    # a ordem dentro do mesmo segundo não é conhecida: tenta também subconjuntos dos passos do mesmo segundo
    res['a_no_fim_de_cada_minuto_ate_17h07'] = [dict(ate=hhmmss(m * 60 + 59), lula=int(L[t <= m * 60 + 59].sum()), flavio=int(R[t <= m * 60 + 59].sum()), secoes=int(n[t <= m * 60 + 59].sum())) for m in (17 * 60 + 5, 17 * 60 + 6, 17 * 60 + 7)]
    if len(ex) == 0:
        # busca por instante: acumulado até o segundo s, mais um subconjunto dos passos do segundo s + 1
        achou = []
        for s in np.unique(t[t < 18 * 3600]):
            bL = int(L[t < s].sum()); bR = int(R[t < s].sum())
            ii = np.flatnonzero(t == s)
            if bL <= 193574 <= bL + L[ii].sum() and bR <= 142169 <= bR + R[ii].sum() and len(ii) <= 22:
                for q in range(1, len(ii) + 1):
                    for comb in itertools.combinations(ii, q):
                        if bL + L[list(comb)].sum() == 193574 and bR + R[list(comb)].sum() == 142169:
                            achou.append(dict(segundo=hhmmss(s), passos_do_segundo=len(ii), usados=q, secoes=int(n[t < s].sum() + n[list(comb)].sum())))
                            break
                    if achou and achou[-1]['segundo'] == hhmmss(s):
                        break
        res['a_instante_com_ordem_livre_dentro_do_segundo'] = achou
    # (b) de onde sairia 165.699: instante anterior com Lula = 27.875, ou conjunto de UFs que soma 165.699 no instante da tela
    res['b_instante_com_lula_27875'] = [dict(hora=hhmmss(t[i]), flavio=int(cR[i]), secoes=int(cn[i])) for i in np.flatnonzero(cL == 27875)]
    refs = {}
    if len(ex):
        refs['instante_da_tela'] = ex[0]
    refs['fim_de_17h07'] = int(np.flatnonzero(t <= 17 * 3600 + 7 * 60 + 59)[-1])
    for nome, i in refs.items():
        ufs_ = sorted(set(uf))
        vL = {u: int(L[:i + 1][uf[:i + 1] == u].sum()) for u in ufs_}
        vR = {u: int(R[:i + 1][uf[:i + 1] == u].sum()) for u in ufs_}
        com = [u for u in ufs_ if vL[u] > 0 or vR[u] > 0]
        # busca exaustiva (encontro no meio) de subconjuntos de UFs com soma de Lula = 165.699
        a = com[:len(com) // 2]; b = com[len(com) // 2:]
        somas = {}
        for q in range(len(a) + 1):
            for c in itertools.combinations(a, q):
                somas.setdefault(sum(vL[u] for u in c), []).append(c)
        sol = []
        for q in range(len(b) + 1):
            for c in itertools.combinations(b, q):
                s = 165699 - sum(vL[u] for u in c)
                for c2 in somas.get(s, []):
                    sol.append(sorted(c2 + c))
        res['b_' + nome] = dict(hora=hhmmss(t[i]), lula_total=int(cL[i]), flavio_total=int(cR[i]), secoes=int(cn[i]), lula_por_uf={u: vL[u] for u in com}, flavio_por_uf={u: vR[u] for u in com},
                                ufs_com_voto=len(com), conjuntos_de_ufs_com_lula_165699=sol[:10], n_conjuntos=len(sol),
                                exterior_lula=vL.get('ZZ', 0), exterior_flavio=vR.get('ZZ', 0), exterior_secoes=int(n[:i + 1][uf[:i + 1] == 'ZZ'].sum()))
    # EXPLORATÓRIO (acrescentado depois de ver o resultado de (a) e (b)): a busca por conjuntos de UFs não distingue
    # nada, porque com k UFs há 2^k conjuntos para somas de até 193 mil; e a soma das páginas sem o exterior.
    br = uf != 'ZZ'
    cLb = np.cumsum(np.where(br, L, 0)); cLz = np.cumsum(np.where(~br, L, 0)); cnb = np.cumsum(np.where(br, n, 0)); cnz = np.cumsum(np.where(~br, n, 0))
    expl = {}
    if len(ex):
        i = int(ex[0]); k_ufs = res['b_instante_da_tela']['ufs_com_voto']
        expl['conjuntos_esperados_por_acaso_para_um_numero_qualquer'] = float(2 ** k_ufs / 193574)
        expl['no_instante_da_tela'] = dict(lula_nas_27_ufs=int(cLb[i]), secoes_nas_27_ufs=int(cnb[i]), lula_no_exterior=int(cLz[i]), secoes_do_exterior=int(cnz[i]),
                                           fracao_do_exterior_nos_votos_de_lula_da_tela=float(cLz[i] / cL[i]), numero_alegado_menos_exterior=int(165699 - cLz[i]))
    expl['instantes_com_lula_27875_nas_27_ufs'] = int((cLb == 27875).sum())
    j = int(np.argmin(np.abs(cLb - 27875)))
    expl['mais_proximo_de_27875_nas_27_ufs'] = dict(hora=hhmmss(t[j]), lula=int(cLb[j]), secoes=int(cnb[j]))
    expl['exterior_igual_a_165699_em_algum_instante'] = int((cLz == 165699).sum())
    res['exploratorio'] = expl
    # (c) fim: total nacional menos a soma das UFs
    A, chaves, ufs, meta = carrega_base()
    tot_bweb = int(A['L2'].sum()); por_uf = np.bincount(A['uf_id'], weights=A['L2'].astype(float)).astype(np.int64)
    of = None
    try:
        of = json.load(open('/home/user/trabalho-eleicao/oficial_br/br2.json'))
    except Exception:
        pass
    lula_of = None
    if of is not None:
        def acha(o):
            if isinstance(o, dict):
                if str(o.get('n')) == '13' and 'vap' in o:
                    return int(str(o['vap']).replace('.', ''))
                for v in o.values():
                    r = acha(v)
                    if r is not None:
                        return r
            elif isinstance(o, list):
                for v in o:
                    r = acha(v)
                    if r is not None:
                        return r
            return None
        lula_of = acha(of)
    res['c_fim'] = dict(lula_historico=int(cL[-1]), lula_bweb=tot_bweb, soma_das_ufs_bweb=int(por_uf.sum()), lula_json_oficial_nacional=lula_of,
                        nacional_menos_soma_das_ufs_no_historico=int(cL[-1] - sum(int(L[uf == u].sum()) for u in set(uf))),
                        nacional_oficial_menos_bweb=None if lula_of is None else int(lula_of - tot_bweb),
                        exterior_lula_final=int(A['L2'][A['exterior'] == 1].sum()), exterior_flavio_final=int(A['R2'][A['exterior'] == 1].sum()))
    c = res['c_fim']
    res['veredito'] = 'SEM SINAL' if c['nacional_menos_soma_das_ufs_no_historico'] == 0 and c['lula_historico'] == c['lula_bweb'] and (lula_of is None or lula_of == tot_bweb) else 'SINAL'
    grava('parcial_r7.json', res)
    diz('r7 pronto', {k: res[k] for k in ('a_instante_exato', 'a_mais_proximo', 'b_instante_com_lula_27875', 'c_fim', 'veredito')})
    for k in res:
        if k.startswith('b_') and isinstance(res[k], dict):
            diz(k, {q: res[k][q] for q in ('hora', 'lula_total', 'flavio_total', 'secoes', 'n_conjuntos', 'conjuntos_de_ufs_com_lula_165699', 'exterior_lula', 'exterior_flavio', 'exterior_secoes')})


def modo_r8():
    t0 = time.time()
    A, chaves, ufs, meta = carrega_base()
    rng = np.random.default_rng(SEMENTE + 8)
    ks, t, n, L, R, uf = _serie_nacional()
    cL, cR, cn = np.cumsum(L), np.cumsum(R), np.cumsum(n)
    NS = int(cn[-1])
    fl = 100.0 * cR / np.maximum(cL + cR, 1)
    res = {}
    fato = {}
    for pct in (23, 30, 38):
        i = int(np.searchsorted(cn, pct / 100 * NS))
        fato[f'com_{pct}_pct_das_secoes'] = dict(hora=hhmmss(t[i]), secoes=int(cn[i]), flavio_pct=float(fl[i]), lula=int(cL[i]), flavio=int(cR[i]))
    for nome, s in (('as_20h00', 20 * 3600), ('as_20h15', 20 * 3600 + 900)):
        i = int(np.flatnonzero(t <= s)[-1])
        fato[nome] = dict(secoes=int(cn[i]), pct_das_secoes=float(100 * cn[i] / NS), flavio_pct=float(fl[i]))
    lid = np.sign(cL - cR)
    tro = np.flatnonzero((lid[1:] != lid[:-1]) & (lid[1:] != 0)) + 1
    fato['trocas_de_lideranca'] = [dict(hora=hhmmss(t[i]), passa_a_liderar='Lula' if lid[i] > 0 else 'Flávio', pct_das_secoes=float(100 * cn[i] / NS)) for i in tro]
    fato['trocas_de_lideranca_n'] = int(len(tro))
    fato['final_flavio_pct'] = float(fl[-1])
    fato['maior_vantagem_de_flavio'] = dict(hora=hhmmss(t[int(np.argmax(fl[cn > 0.05 * NS]) + np.flatnonzero(cn > 0.05 * NS)[0])]), flavio_pct=float(fl[cn > 0.05 * NS].max()))
    res['a_fato'] = fato
    # (b) composição das primeiras 30% pela ordem de recebimento
    N = len(chaves)
    L2, R2 = A['L2'].astype(np.int64), A['R2'].astype(np.int64); V2 = L2 + R2
    L1, R1 = A['L1'].astype(np.int64), A['R1'].astype(np.int64)
    p30 = A['ordem_nac'] < 0.30 * N
    pF = 100.0 * R2.sum() / V2.sum(); pF1 = 100.0 * R1.sum() / (L1 + R1).sum()
    f2_30 = 100.0 * R2[p30].sum() / V2[p30].sum(); f1_30 = 100.0 * R1[p30].sum() / (L1 + R1)[p30].sum()
    f2_r = 100.0 * R2[~p30].sum() / V2[~p30].sum(); f1_r = 100.0 * R1[~p30].sum() / (L1 + R1)[~p30].sum()
    res['b_composicao'] = dict(secoes_nas_primeiras_30=int(p30.sum()), ultima_hora_de_recebimento_das_30=hhmmss(int(A['rec_s'][p30].max())),
                               flavio_2t_nas_30=f2_30, flavio_2t_pais=pF, g2=f2_30 - pF, flavio_1t_dos_dois_nas_30=f1_30, flavio_1t_dos_dois_pais=pF1, g1=f1_30 - pF1,
                               g2_menos_g1=(f2_30 - pF) - (f1_30 - pF1), previsto_por_alteracao_ligada_aos_30=1.79, previsto_se_a_parcial_fosse_representativa_g1=0.0,
                               virada_a_favor_de_lula_nas_30=f1_30 - f2_30, virada_nas_demais=f1_r - f2_r, virada_no_pais=pF1 - pF,
                               primeiras_30_por_regiao={k: float(v) for k, v in zip(*np.unique(np.array(ufs)[A['uf_id'][p30]], return_counts=True))})
    # (c) curvas previstas sem ajuste
    o = np.argsort(A['ordem_nac'])
    zid = A['zona_id']; nz = zid.max() + 1
    fz = np.bincount(zid, weights=R2.astype(float), minlength=nz) / np.maximum(np.bincount(zid, weights=V2.astype(float), minlength=nz), 1)
    f1s = np.where((L1 + R1) > 0, R1 / np.maximum(L1 + R1, 1), fz[zid])
    sw = (pF1 - pF) / 100.0
    cV = np.cumsum(V2[o]); cRr = np.cumsum(R2[o]); cZ = np.cumsum((V2 * fz[zid])[o]); c1 = np.cumsum((V2 * (f1s - sw))[o])
    pts = [int(round(q / 100 * N)) - 1 for q in range(1, 101)]
    real = 100 * cRr[pts] / cV[pts]; pz = 100 * cZ[pts] / cV[pts]; p1 = 100 * c1[pts] / cV[pts]
    rec_o = A['rec_s'][o]

    def ultima_troca(curva_cum):
        s = np.sign(curva_cum - 0.5 * cV)
        i = np.flatnonzero((s[1:] != s[:-1]) & (s[1:] != 0)) + 1
        i = i[cV[i] > 0.05 * cV[-1]]
        return [dict(hora=hhmmss(int(rec_o[j])), pct_das_secoes=float(100 * (j + 1) / N), passa_a_liderar='Flávio' if s[j] > 0 else 'Lula') for j in i[-3:]]
    res['c_curvas'] = dict(real_aos_30=float(real[29]), curva_das_zonas_aos_30=float(pz[29]), curva_do_1t_aos_30=float(p1[29]),
                           real_aos_23=float(real[22]), curva_das_zonas_aos_23=float(pz[22]), curva_do_1t_aos_23=float(p1[22]),
                           real_aos_38=float(real[37]), curva_das_zonas_aos_38=float(pz[37]), curva_do_1t_aos_38=float(p1[37]),
                           diferenca_maxima_real_menos_zonas=float(np.abs(real - pz)[4:].max()), diferenca_maxima_real_menos_1t=float(np.abs(real - p1)[4:].max()),
                           em_que_pct_a_maior_diferenca_do_1t=int(np.abs(real - p1)[4:].argmax() + 5),
                           trocas_reais_pela_ordem_de_recebimento=ultima_troca(cRr.astype(float)), trocas_previstas_pela_curva_das_zonas=ultima_troca(cZ), trocas_previstas_pela_curva_do_1t=ultima_troca(c1),
                           curva_real=[round(float(x), 3) for x in real], curva_zonas=[round(float(x), 3) for x in pz], curva_1t=[round(float(x), 3) for x in p1])
    grava('parcial_r8.json', res)
    # (d) dentro da zona
    y = fatia(L2, R2); X = controles(A); w = V2.astype(float)
    out = {}
    for nome, U in (('universo_G2', universo(A, prorrog=True)), ('sem_prorrogadas', universo(A, prorrog=False))):
        idx = np.flatnonzero(U)
        M = Modelo(np.column_stack([p30[idx].astype(float), X[idx]]), [_ids(zid[idx])], w[idx], A['mun_id'][idx], ['P30'] + NOMES_CTRL)
        oo = M.coef(y[idx], 'P30')
        f = idx[M.fica]
        zz = zid[f]; tem_a = np.bincount(zz[p30[f]], minlength=nz) > 0; tem_b = np.bincount(zz[~p30[f]], minlength=nz) > 0
        oo['zonas_com_os_dois_lados'] = int((tem_a & tem_b).sum()); oo['secoes_nessas_zonas'] = int((tem_a & tem_b)[zz].sum())
        val_dep = int(V2[~p30].sum())
        oo['margem_implicada'] = 2 * (-oo['beta']) / 100 * val_dep; oo['margem_ic95'] = [2 * (-v) / 100 * val_dep for v in oo['ic95'][::-1]]
        if nome == 'universo_G2':
            y1 = fatia(A['L1'], A['R1']); V1d = (L1 + R1).astype(float); f22 = fatia(A['L22'], A['R22'])
            okp = U & A['tem22'] & ((A['L22'] + A['R22']) >= 30) & (V1d >= 30)
            ip = np.flatnonzero(okp)
            Mp = Modelo(np.column_stack([p30[ip].astype(float), f22[ip]]), [_ids(zid[ip])], V1d[ip], A['mun_id'][ip], ['P30', 'f22'])
            oo['placebo_desfecho_anterior'] = Mp.coef(y1[ip], 'P30')
            cal = {}
            for x in (2.55, 0.45):
                inc = []; det = 0
                for rep in range(100):
                    Lp, Rp = troca(rng, L2, R2, x / 100, ~p30)
                    b, se = M.ajusta(fatia(Lp, Rp)[idx])
                    inc.append(b[0] - oo['beta']); det += int((b[0] - oo['beta']) / se[0] <= -Z001)
                cal[f'x{x}'] = dict(esperado=-x, incremento_medio=float(np.mean(inc)), deteccao=det / 100)
            oo['calibracao'] = cal; oo['emd_80'] = (Z001 + Z80) * oo['ep']
        out[nome] = oo
    res['d_dentro_da_zona'] = out
    oo = out['universo_G2']
    sinal = oo['beta'] <= -0.45 and oo['p'] < 0.001
    sem_poder = oo['calibracao']['x0.45']['deteccao'] < 0.95
    semsinal = -0.45 < oo['ic95'][0] and oo['ic95'][1] < 0.45
    res['veredito'] = dict(fato_confere=bool(fato['com_30_pct_das_secoes']['flavio_pct'] > 50), dentro_da_zona='SINAL' if sinal else 'SEM PODER' if sem_poder else 'SEM SINAL' if semsinal else 'INCONCLUSIVO',
                           espelho_a_favor_de_flavio=bool(oo['beta'] >= 0.45 and oo['p'] < 0.001))
    grava('parcial_r8.json', res)
    diz('r8 pronto', res['veredito'], {k: v for k, v in res['b_composicao'].items() if k != 'primeiras_30_por_regiao'}, round(time.time() - t0))


# ============================================================================================ EXPLORATÓRIO
def modo_expl():
    """EXPLORATÓRIO, decidido DEPOIS de ver os resultados das partes 1 e 2 (não entra em veredito). O modelo do
    registro controla a variação do comparecimento, e o indício da Onda A passa pelo comparecimento. Aqui os mesmos
    contrastes de hora (cedo contra tardias, salto na pausa, posição na zona) têm como desfecho a própria variação
    do comparecimento e os ganhos de cada candidato sobre os aptos, sem esse controle."""
    A, chaves, ufs, meta = carrega_base()
    L2, R2 = A['L2'].astype(np.int64), A['R2'].astype(np.int64); V2 = L2 + R2
    apt = np.maximum(A['apt2'], 1).astype(float)
    y = fatia(L2, R2)
    des = {'fatia_de_lula_sem_controle_do_comparecimento': (y, V2.astype(float)),
           'variacao_do_comparecimento_pp_dos_aptos': (100.0 * (A['comp2'] - A['comp1']) / apt, apt),
           'ganho_de_lula_pp_dos_aptos': (100.0 * (L2 - A['L1']) / apt, apt),
           'ganho_de_flavio_pp_dos_aptos': (100.0 * (R2 - A['R1']) / apt, apt),
           'variacao_de_brancos_e_nulos_pp_dos_aptos': (100.0 * ((A['B2'] + A['N2']) - (A['B1'] + A['N1'])) / apt, apt)}
    Xf = controles(A)
    sem = [i for i, nm in enumerate(NOMES_CTRL) if nm != 'dcomp']
    X = Xf[:, sem]; nomes = [NOMES_CTRL[i] for i in sem]
    cedo = A['ret'] == 0; raj = A['ret'] == 1; tardia = A['ret'] > 0
    emin = np.floor(np.nan_to_num(A['emi'], nan=-1)).astype(np.int64)
    U = universo(A, prorrog=False) & ~np.isnan(A['emi'])
    estr = (A['exterior'] == 0) & (A['junta'] == 0) & (A['prorrog'] == 0)
    nl = A['loc_id'].max() + 1
    misto = ((np.bincount(A['loc_id'][estr & cedo], minlength=nl) > 0) & (np.bincount(A['loc_id'][estr & tardia], minlength=nl) > 0))[A['loc_id']]
    FE = {'loc_id': A['loc_id'], 'zona_id': A['zona_id'], 'emin': emin}
    res = {'aviso': 'exploratório, feito depois de ver os resultados; sem critério registrado', 'd35': {}, 'd36': {}}
    for nome, m, fes in (('A', U & misto, ('loc_id', 'emin')), ('B', U & (cedo | raj), ('zona_id', 'emin')), ('C', U & (cedo | (tardia & (A['emi'] < 17 * 60 + 8))), ('zona_id',))):
        idx = np.flatnonzero(m); res['d35'][nome] = {}
        for dn, (yy, ww) in des.items():
            M = Modelo(np.column_stack([cedo[idx].astype(float), X[idx]]), [_ids(FE[f][idx]) for f in fes], ww[idx], A['mun_id'][idx], ['E'] + nomes)
            o = M.coef(yy[idx], 'E')
            f = idx[M.fica]
            o['bruto_cedo'] = float(np.average(yy[f][cedo[f]], weights=ww[f][cedo[f]])); o['bruto_tardias'] = float(np.average(yy[f][~cedo[f]], weights=ww[f][~cedo[f]]))
            res['d35'][nome][dn] = o
    # D3-6: resíduo sem o controle do comparecimento, salto na pausa e inclinação
    U6 = universo(A, prorrog=True); iu = np.flatnonzero(U6)
    rec = A['rec_s']; zid = A['zona_id']; mid = A['mun_id']; np_ = A['prorrog'] == 0; pos = A['pos_zona']
    for dn, (yy, ww) in des.items():
        Mn = Modelo(X[iu], [_ids(zid[iu])], ww[iu], mid[iu], nomes)
        r = np.full(len(yy), np.nan); r[iu[Mn.fica]] = Mn.ajusta(yy[iu], so_residuo=True)
        S1 = ~np.isnan(r) & np_
        o1 = rd(r[S1], rec[S1], ww[S1], zid[S1], H(19, 48), H(19, 50), 480)
        i2 = np.flatnonzero(S1 & ~np.isnan(pos))
        M2 = Modelo(pos[i2][:, None], [_ids(zid[i2])], ww[i2], mid[i2], ['pos'])
        res['d36'][dn] = dict(salto_na_pausa_banda_8=o1, inclinacao_na_zona=M2.coef(r[i2], 'pos'))
    # tamanho de referência: quanto a variação do comparecimento das tardias teria de diferir das cedo se a margem
    # inteira tivesse entrado como voto a mais (4.430.191 eleitores) só nas seções recebidas depois da retenção
    apt_t = float(A['apt2'][tardia].sum())
    res['referencia'] = dict(aptos_das_tardias=apt_t, margem_sobre_aptos_das_tardias_pp=100.0 * MARGEM / apt_t)
    # placebo (3) do D3-5 com efeito fixo de local (o registrado usa zona): a diferença é de prédio ou de hora?
    y1 = fatia(A['L1'], A['R1']); V1d = (A['L1'] + A['R1']).astype(float); f22 = fatia(A['L22'], A['R22'])
    okp = A['tem22'] & ((A['L22'] + A['R22']) >= 30) & (V1d >= 30)
    e1 = (A['rec1_s'] >= 17 * 3600 + 8 * 60) & (A['rec1_s'] < 17 * 3600 + 11 * 60)
    m3 = (A['exterior'] == 0) & (A['junta1'] == 0) & A['tem1'] & okp & (A['enc1'] < 18 * 60 + 30) & (A['emi1'] < 17 * 60 + 11)
    ix = np.flatnonzero(m3); em1 = np.floor(A['emi1'][ix]).astype(np.int64)
    res['placebo3_variantes'] = {}
    for nome, fes in (('zona_e_minuto_registrado', [_ids(A['zona_id'][ix]), _ids(em1)]), ('local_e_minuto', [_ids(A['loc_id'][ix]), _ids(em1)])):
        M = Modelo(np.column_stack([e1[ix].astype(float), f22[ix]]), fes, V1d[ix], A['mun_id'][ix], ['E', 'f22'])
        res['placebo3_variantes'][nome] = dict(M.coef(y1[ix], 'E'), tratadas=int(e1[ix][M.fica].sum()))
    grava('parcial_expl.json', res)
    for k, v in res['d35'].items():
        diz('expl d35', k, {a: (round(b['beta'], 4), round(b['ep'], 4)) for a, b in v.items()})
    diz('expl d36', {a: ((round(b['salto_na_pausa_banda_8']['tau'], 4), round(b['salto_na_pausa_banda_8']['ep'], 4)), (round(b['inclinacao_na_zona']['beta'], 4), round(b['inclinacao_na_zona']['ep'], 4))) for a, b in res['d36'].items()})


# ============================================================================================ RELATÓRIO
def nb(x, d=2, sinal=False):
    """Número no formato brasileiro."""
    if x is None or (isinstance(x, float) and (math.isnan(x) or math.isinf(x))):
        return 'n/d'
    s = f'{x:+,.{d}f}' if sinal else f'{x:,.{d}f}'
    return s.replace(',', 'X').replace('.', ',').replace('X', '.')


def ni(x, sinal=False):
    return nb(float(x), 0, sinal)


def pv(p):
    return 'p < 0,0001' if p < 0.0001 else 'p = ' + nb(p, 4)


def modo_relatorio():
    sha = _le('parcial_sha.json'); hist = _le('parcial_hist.json'); d35 = _le('parcial_d35.json'); d36 = _le('parcial_d36.json')
    r1 = _le('parcial_r1.json'); r7 = _le('parcial_r7.json'); r8 = _le('parcial_r8.json'); ex = _le('parcial_expl.json')
    meta = _carrega(TRAB + '/base_B5_chaves.json.gz')['meta']
    doc = open(TRAB + '/docstring_antes_de_rodar.sha256').read().split()
    T = []; A = T.append
    V = {}; J = {}
    # ---------------- vereditos
    if d35:
        v = d35['veredito']; a = d35['observado']['A']; b = d35['observado']['B']
        rotp = {'1_desfecho_anterior_A': 'placebo (1) em A', '1_desfecho_anterior_B': 'placebo (1) em B', '2_rajada_contra_19h05_a_19h30': 'placebo (2)', '3_primeiro_turno_primeiras_recebidas': 'placebo (3), o do 1º turno,'}
        v['clausulas_de_inconclusivo'] = [c_ if not c_.startswith('placebo de 0,15') else 'placebo de 0,15 ou mais: ' + ', '.join(f"{rotp[k_]} = {nb(x_, 3, True)}" for k_, x_ in d35['placebos_do_criterio'].items() if abs(x_) >= 0.15) for c_ in v['clausulas_de_inconclusivo']]
        so3 = [k_ for k_, x_ in d35['placebos_do_criterio'].items() if abs(x_) >= 0.15] == ['3_primeiro_turno_primeiras_recebidas'] and len(v['clausulas_de_inconclusivo']) == 1
        V['D3-5 retenção das 17:08 às 19:03'] = v['veredito']
        J['D3-5 retenção das 17:08 às 19:03'] = (f"beta_E de A = {nb(a['beta'], 3, True)} (ep {nb(a['ep'], 3)}), de B = {nb(b['beta'], 3, True)} (ep {nb(b['ep'], 3)}); a hipótese previa -0,45 ou mais negativo. "
                                                 + ('Cláusulas de inconclusivo: ' + '; '.join(v['clausulas_de_inconclusivo']) + '. ' if v['clausulas_de_inconclusivo'] else '')
                                                 + ('Os limites numéricos de SEM SINAL estão cumpridos (limite inferior de 95% acima de -0,45 nos dois).' if v['sem_sinal_forte'] else 'Limites de SEM SINAL cumpridos.' if v['limites_de_sem_sinal_cumpridos'] else '')
                                                 + (' Os placebos (1) e (2), que são os comparáveis ao coeficiente real, ficam abaixo de 0,15: sem o placebo (3) o veredito seria SEM SINAL.' if so3 else ''))
    if d36:
        vv = d36['vereditos']; e1 = d36['e1_descontinuidade']; e2 = d36['e2_inclinacao']; e3 = d36['e3_deslocados']
        V['D3-6 (1) salto na pausa das 19:48'] = vv['1_descontinuidade']['veredito']
        J['D3-6 (1) salto na pausa das 19:48'] = (f"tau = {nb(e1['banda_8']['tau'], 3, True)} (ep {nb(e1['banda_8']['ep'], 3)}) na banda de 8 minutos; intervalo de 95% de {nb(e1['banda_8']['ic95'][0], 3, True)} a {nb(e1['banda_8']['ic95'][1], 3, True)}, dentro de -0,45 a +0,45."
                                                  + (' Cláusulas: ' + '; '.join(vv['1_descontinuidade']['clausulas_de_inconclusivo']) if vv['1_descontinuidade']['clausulas_de_inconclusivo'] else ''))
        V['D3-6 (2) inclinação dentro da zona'] = vv['2_inclinacao']['veredito']
        J['D3-6 (2) inclinação dentro da zona'] = f"theta = {nb(e2['beta'], 3, True)} (ep {nb(e2['ep'], 3)}, {pv(e2['p'])}); o limiar de sinal é +0,9; intervalo de 95% de {nb(e2['ic95'][0], 3, True)} a {nb(e2['ic95'][1], 3, True)}."
        for k, rot in (('desloc_30', 'D3-6 (3) deslocados de 30 minutos ou mais'), ('desloc_60', 'D3-6 (3) deslocados de 60 minutos ou mais'), ('cauda', 'D3-6 (3) cauda das 21:10 em diante')):
            V[rot] = vv['3_' + k]['veredito']
            J[rot] = f"beta = {nb(e3[k]['beta'], 3, True)} (ep {nb(e3[k]['ep'], 3)}); limiar de sinal local +1,0; placebo {nb(e3[k]['placebo_desfecho_anterior']['beta'], 3, True)}."
    if hist and sha:
        t2 = hist['turno2']; t1 = hist.get('turno1')
        zero2 = (sum(t2['zonas_com_d_diferente_de_zero'].values()) == 0 and t2['zonas_com_numero_de_secoes_diferente'] == 0 and t2['passos_sem_atribuicao_possivel'] == 0
                 and t2['passos_com_busca_interrompida_por_tempo'] == 0 and t2['passos_com_boletim_recebido_depois_do_passo_na_ordem_de_recebimento'] == 0 and not sha['resumo']['diferentes'])
        s13 = t2['zonas_com_d_diferente_de_zero']['13'] + t2['zonas_com_d_diferente_de_zero']['22'] + t2['passos_sem_atribuicao_possivel'] + len(sha['resumo']['diferentes'])
        V['D3-2 (parte rodada) bweb contra o histórico e .sha512'] = 'SEM SINAL' if zero2 else 'SINAL' if s13 else 'INCONCLUSIVO'
        J['D3-2 (parte rodada) bweb contra o histórico e .sha512'] = (f"diferença zero nas {ni(t2['zonas'])} zonas, {ni(t2['municipios'])} municípios, 28 UFs e no país para 13, 22, brancos, nulos e comparecimento; "
                                                                      f"{ni(t2['passos'])} passos conferidos, nenhum sem atribuição possível, nenhum boletim somado antes de recebido; 56 de 56 zips iguais ao resumo publicado. "
                                                                      "Vale só para o que rodou: o JSON oficial por município e o aux.json da amostra antiga ficaram para a onda D.")
    if r1:
        v = r1['veredito']; o = r1['b_dose']['principal']
        V['R1 um voto a cada dez segundos depois das 17h01 (ao pé da letra)'] = 'SEM SINAL' if v['alegacao_ao_pe_da_letra'] == 'REFUTADA' else 'SINAL' if v['alegacao_ao_pe_da_letra'] == 'CONFIRMADA' else 'INCONCLUSIVO'
        J['R1 um voto a cada dez segundos depois das 17h01 (ao pé da letra)'] = f"a alegação prevê kappa = 1; medido {nb(o['beta'], 4, True)} (ep {nb(o['ep'], 4)}), teto de 95% em {nb(o['ic95'][1], 4)} voto a cada dez segundos. Critério meu, escrito antes."
        V['R1 efeito do horário de encerramento com alcance'] = v['efeito_do_horario_com_alcance']
        J['R1 efeito do horário de encerramento com alcance'] = f"margem implicada {ni(o['margem_implicada'], True)} votos, teto de 95% {ni(o['margem_ic95'][1])}, abaixo de 443.019 (10% da margem)."
    if r7:
        V['R7 os 165.699 votos sem origem'] = r7['veredito']
        J['R7 os 165.699 votos sem origem'] = 'total nacional menos a soma das UFs = 0 no histórico, no bweb e no JSON oficial; a tela do vídeo é o estado exato das 17:06:27. Critério meu, escrito antes.'
    if r8:
        o = r8['d_dentro_da_zona']['universo_G2']
        V['R8 tendência de vitória de Flávio com 30% apurado'] = r8['veredito']['dentro_da_zona']
        J['R8 tendência de vitória de Flávio com 30% apurado'] = (f"o fato confere (Flávio com {nb(r8['a_fato']['com_30_pct_das_secoes']['flavio_pct'], 2)}% aos 30% das seções), mas a composição explica {nb(r8['b_composicao']['g1'], 2)} dos {nb(r8['b_composicao']['g2'], 2)} pontos; "
                                                                  f"dentro da zona a diferença é {nb(o['beta'], 3, True)} (ep {nb(o['ep'], 3)}), contra -2,55 previstos por uma alteração ligada aos 30%. Critério meu, escrito antes.")
    resumo = ('A retenção das 17:08 às 19:03, a pausa das 19:48, a ordem de chegada e os boletins fora de hora não marcam a virada: onde o teste enxerga meio ponto, os contrastes de hora ficam entre -0,05 e +0,11 ponto; '
              'o bweb é igual ao histórico oficial passo a passo; e as três alegações com número (R1, R7, R8) não se sustentam com o número que preveem.')
    # ---------------- texto
    A('R27_B5: JANELAS DA TOTALIZAÇÃO (D3-5, D3-6, parte do D3-2, alegações R1, R7 e R8)')
    A('')
    A('Registro: Adendo 27 (commit 2748895, 10/11/2026 00:16:42 UTC), item B5, mantido pelo Adendo 28 (commit 938be19). D3-5, D3-6 e D3-2 são do desenho cego D3')
    A('(registro/adendo27/desenho_D3_proposta.json). Os grupos de tratamento são os congelados em desenho_D3/grupos_2t.json.gz, com SHA-256 conferido antes de')
    A('qualquer conta. As alegações R1, R7 e R8 (novidades_relatorio.json) não têm critério no registro: o critério de cada uma foi escrito no docstring antes de')
    A(f'calcular. Docstring gravado às {doc[0]}, antes de qualquer conta com votos (SHA-256 {doc[1][:16]}...). O programa foi ensaiado com um 2º turno')
    A('sorteado (sem efeito de hora) antes de rodar no dado real; os testes estatísticos (D3-5, D3-6, R1, R8) rodaram uma vez no dado real, sem mudança de estimador.')
    A('')
    A('VEREDITOS PELA LETRA')
    for k in V:
        A(f'  {V[k]:13s} {k}')
        A(f'                {J[k]}')
    A('')
    A('RESUMO EM UMA FRASE')
    A('  ' + resumo)
    A('')
    A('AVISOS DE ALCANCE (valem para tudo abaixo)')
    A('  1. Estes testes comparam boletins conforme a HORA em que o TSE os recebeu ou somou. Enxergam alteração feita na totalização, na fila de espera ou ligada')
    A('     a um horário. Não enxergam alteração feita dentro da urna antes da emissão do boletim e igual em todas as horas: essa hipótese fica com os testes de')
    A('     urna, de log e, no fim, com o papel (boletim impresso e caderno de votação).')
    A('  2. Se a alteração tivesse alcançado também os boletins já recebidos antes das 17:08, o D3-5 não teria contraste (aviso do próprio desenho).')
    A('  3. O modelo do registro controla a variação do comparecimento. A calibração mostra que, mesmo assim, ele NÃO separa troca de voto de entrada de')
    A('     eleitores ou de abstenção de um lado só: os três mecanismos plantados mexem o coeficiente quase igual. Um sinal aqui não diria qual dos três; a')
    A('     ausência de sinal vale para os três.')
    A('')
    # ---------------- PARTE 1
    if d35:
        u = d35['universo']; ob = d35['observado']; pb = d35['placebos']; cal = d35['calibracao']['plantios']; v = d35['veredito']
        A('PARTE 1. D3-5: A RETENÇÃO DAS 17:08 ÀS 19:03 (boletins recebidos antes contra recebidos depois)')
        A(f"  Estrutura: {ni(u['cedo_brasil'])} seções do Brasil foram recebidas de 17:05 a 17:07, antes da retenção ({ni(u['cedo_no_universo'])} entram nas contas); nenhuma de 17:08 a 19:02;")
        A(f"  5.651 no minuto 19:03. Votos válidos recebidos antes: {ni(d35['validos_recebidos_antes'])}; depois: {ni(d35['validos_recebidos_depois_da_retencao'])}.")
        A('  y = fatia de Lula nos válidos do 2º turno (pontos). beta_E = quanto a seção recebida ANTES difere da comparável recebida DEPOIS. A hipótese prevê negativo.')
        A('')
        A('  comparação                                      beta_E     ep      z    p        IC 95%            n     cedo  tardias  municípios   margem implicada (IC 95%)')
        for k, rot in (('A', 'A mesmo prédio (local e minuto de emissão)'), ('B', 'B cedo contra rajada das 19:03 (zona, minuto)'), ('C', 'C cedo contra tardias da zona (ao lado)'), ('C_com_minuto', 'C com minuto de emissão (ao lado)')):
            o = ob[k]
            A(f"  {rot:46s} {nb(o['beta'], 3, True):>7s} {nb(o['ep'], 3):>6s} {nb(o['z'], 2, True):>6s} {nb(o['p'], 3):>6s}  {nb(o['ic95'][0], 3, True):>7s} a {nb(o['ic95'][1], 3, True):>7s} {ni(o['n']):>8s} {ni(o['cedo']):>6s} {ni(o['tardias']):>8s} {ni(o['municipios']):>7s}     {ni(o['margem_implicada'], True)} ({ni(o['margem_ic95'][0], True)} a {ni(o['margem_ic95'][1], True)})")
        A('  Margem implicada = 2 x (-beta_E) x válidos recebidos depois. Positiva = a favor de Lula nas tardias; negativa = o contrário.')
        a = ob['A']; b = ob['B']
        A(f"  Em votos: o pior caso a favor da tese (limite inferior de 95%) é {ni(a['margem_ic95'][1], True)} votos de margem em A e {ni(b['margem_ic95'][1], True)} em B, isto é,")
        A(f"  {nb(100 * a['margem_ic95'][1] / MARGEM, 1)}% e {nb(100 * b['margem_ic95'][1] / MARGEM, 1)}% da margem de 4.430.191. A estimativa pontual tem o sinal contrário ao da hipótese nas quatro contas.")
        A(f"  Sem o controle de idade: A {nb(a['sem_idade']['beta'], 3, True)} (ep {nb(a['sem_idade']['ep'], 3)}); B {nb(b['sem_idade']['beta'], 3, True)} (ep {nb(b['sem_idade']['ep'], 3)}).")
        A('  Valor bruto de 2026, sem modelo e sem outro ano (média ponderada pelos válidos):')
        for k in ('A', 'B'):
            br = ob[k]['bruto']
            A(f"    {k}: cedo {nb(br['fatia_1t_dos_dois_cedo'], 2)}% no 1º turno (fatia dos dois) e {nb(br['fatia_2t_cedo'], 2)}% no 2º, virada {nb(br['virada_cedo'], 2, True)}; tardias {nb(br['fatia_1t_dos_dois_tardias'], 2)}% e {nb(br['fatia_2t_tardias'], 2)}%, virada {nb(br['virada_tardias'], 2, True)}; diferença {nb(br['diferenca_de_virada_cedo_menos_tardias'], 2, True)}.")
        A('  Placebos (o registro pede todos abaixo de 0,15 em módulo):')
        rp = {'1_desfecho_anterior_A': '(1) desfecho anterior em A (1º turno de 2026 controlado por 2022)', '1_desfecho_anterior_B': '(1) desfecho anterior em B',
              '1_desfecho_anterior_C': '(1) desfecho anterior em C (ao lado, fora do critério)', '2_rajada_contra_19h05_a_19h30': '(2) corte falso: rajada das 19:03 contra 19:05 a 19:30',
              '3_primeiro_turno_primeiras_recebidas': '(3) 1º turno: recebidas de 17:08 a 17:10 contra as seguintes da zona'}
        for k, rot in rp.items():
            o = pb[k]
            A(f"    {rot:66s} {nb(o['beta'], 3, True):>7s} (ep {nb(o['ep'], 3)}, n {ni(o['n'])}){'  PASSA DE 0,15' if abs(o['beta']) >= 0.15 and 'C' not in k[-1:] else ''}")
        A('    Os placebos (1) e (3) comparam com 2022: o veredito desta parte depende, na cláusula do placebo, de outro ano. O placebo (2) é interno a 2026.')
        A(f"    O placebo (3) tem erro de {nb(pb['3_primeiro_turno_primeiras_recebidas']['ep'], 2)}, maior que o próprio limiar de 0,15: ele não consegue ficar abaixo do limiar com segurança, e só {ni(pb['3_primeiro_turno_primeiras_recebidas']['primeiras'])} seções tratadas entram.")
        if ex and 'placebo3_variantes' in ex:
            pv3 = ex['placebo3_variantes']['local_e_minuto']
            A(f"    Exploratório (depois de ver): o mesmo placebo (3) dentro do mesmo prédio (efeito fixo de local e de minuto) dá {nb(pv3['beta'], 3, True)} (ep {nb(pv3['ep'], 3)}, {ni(pv3['tratadas'])} tratadas): a maior parte dos +0,69 é diferença")
            A('    entre prédios da mesma zona, não entre horas; ainda assim a estimativa pontual não fica abaixo de 0,15.')
        A('  Calibração (troca binomial do 22 para o 13 em toda seção recebida de 19:03 em diante, 200 cópias): incremento médio de beta_E e detecção')
        for x in ('0.45', '0.9', '1.79'):
            c = cal[f'a_favor_de_lula_x{x}']
            A(f"    x = {x.replace('.', ',')}%: A {nb(c['A']['incremento_medio'], 3, True)} (detecta {nb(100 * c['A']['deteccao'], 0)}%), B {nb(c['B']['incremento_medio'], 3, True)} ({nb(100 * c['B']['deteccao'], 0)}%), C {nb(c['C']['incremento_medio'], 3, True)} ({nb(100 * c['C']['deteccao'], 0)}%); cumpre o critério inteiro em A: {nb(100 * c['A']['cumpre_condicoes_numericas_do_criterio'], 0)}%, em B: {nb(100 * c['B']['cumpre_condicoes_numericas_do_criterio'], 0)}%.")
        A(f"    Efeito mínimo detectável com 80% de poder: A {nb(a['emd_80'], 2)} ponto (p < 0,001), B {nb(b['emd_80'], 2)} (p < 0,01). O teste enxerga o que diz enxergar.")
        c = cal['espelho_a_favor_de_flavio_x0.45']; c2 = cal['espelho_a_favor_de_flavio_x1.79']
        A(f"  Espelho (mesma conta a favor de Flávio): plantio de 0,45 devolve A {nb(c['A']['incremento_medio'], 3, True)}, B {nb(c['B']['incremento_medio'], 3, True)}; de 1,79, A {nb(c2['A']['incremento_medio'], 3, True)}, B {nb(c2['B']['incremento_medio'], 3, True)}.")
        A(f"    No dado real o critério espelhado (beta_E de +0,45 ou mais) {'É' if v['espelho_a_favor_de_flavio'] else 'NÃO é'} cumprido.")
        ino = d35['explicacoes_inocentes']['plantios']
        A('  Explicação inocente plantada (mesmo efeito na margem que a troca de 1,79%, nas tardias, 100 cópias): fração do incremento da troca que aparece')
        A(f"    entrada de eleitores reais de Lula: A {nb(100 * ino['entrada_de_eleitores_reais']['A']['razao_para_a_troca_de_mesma_margem'], 0)}%, B {nb(100 * ino['entrada_de_eleitores_reais']['B']['razao_para_a_troca_de_mesma_margem'], 0)}%, C {nb(100 * ino['entrada_de_eleitores_reais']['C']['razao_para_a_troca_de_mesma_margem'], 0)}%")
        A(f"    abstenção pura de eleitores de Flávio: A {nb(100 * ino['abstencao_pura']['A']['razao_para_a_troca_de_mesma_margem'], 0)}%, B {nb(100 * ino['abstencao_pura']['B']['razao_para_a_troca_de_mesma_margem'], 0)}%, C {nb(100 * ino['abstencao_pura']['C']['razao_para_a_troca_de_mesma_margem'], 0)}%")
        A('    O teste NÃO distingue troca de voto de diferença de comparecimento (todas acima de 50%). Como não há sinal, isso só importa para a leitura: a')
        A('    ausência de contraste entre cedo e tardias vale também para entrada de votos e para retirada de eleitores durante a retenção.')
        A(f"  VEREDITO PELA LETRA: {v['veredito']}. " + ('Motivo: ' + '; '.join(v['clausulas_de_inconclusivo']) + '.' if v['clausulas_de_inconclusivo'] else ''))
        A(f"    Condições de SINAL: {'presentes' if v['condicoes_de_sinal'] else 'ausentes'}. Limite inferior de 95% acima de -0,90 em A e B: {'sim' if v['limites_de_sem_sinal_cumpridos'] else 'não'}; acima de -0,45 (sem sinal forte): {'sim' if v['sem_sinal_forte'] else 'não'}.")
        A(f"    Como o registro manda quando o placebo passa de 0,15, fica a diferença entre o beta real e o do placebo (1), sem concluir: A {nb(v['diferenca_para_o_placebo']['A'], 3, True)}, B {nb(v['diferenca_para_o_placebo']['B'], 3, True)}.")
        A('')
    # ---------------- PARTE 2
    if d36:
        e1 = d36['e1_descontinuidade']; e2 = d36['e2_inclinacao']; e3 = d36['e3_deslocados']; vv = d36['vereditos']
        A('PARTE 2. D3-6: PAUSA DAS 19:48, ORDEM DE CHEGADA E BOLETINS FORA DE HORA')
        A(f"  Resíduo r = fatia de Lula no 2º turno menos o previsto pelo 1º turno, com efeito fixo de zona ({ni(d36['universo']['com_residuo'])} seções, {ni(d36['universo']['zonas'])} zonas; desvio padrão {nb(d36['universo']['dp_do_residuo'], 2)} ponto).")
        A('  (1) Salto na pausa (último boletim antes às 19:47:43, primeiro depois às 19:50:57). tau positivo = quem entrou depois virou mais para Lula.')
        A('      banda     tau      ep      z     p       IC 95%           antes    depois   margem implicada (IC 95%)')
        for h in (8, 4, 16):
            o = e1[f'banda_{h}']
            A(f"      {h:2d} min  {nb(o['tau'], 3, True):>7s} {nb(o['ep'], 3):>6s} {nb(o['z'], 2, True):>6s} {nb(o['p'], 3):>6s} {nb(o['ic95'][0], 3, True):>7s} a {nb(o['ic95'][1], 3, True):>7s} {ni(o['n_antes']):>8s} {ni(o['n_depois']):>8s}   {ni(o['margem_implicada'], True)} ({ni(o['margem_ic95'][0], True)} a {ni(o['margem_ic95'][1], True)})")
        A(f"      Margem = 2 x tau x válidos recebidos de 19:50 em diante ({ni(d36['validos_recebidos_de_19h50_em_diante'])}). Zonas com os dois lados na banda de 8: {ni(e1['zonas_com_os_dois_lados_banda_8'])} (o desenho dizia 1.255).")
        f12 = e1['cortes_falsos']['grade_do_registro_12']; f20 = e1['cortes_falsos']['vinte_de_3_em_3']
        A(f"      Cortes falsos (banda de 8): maior salto em módulo {nb(e1['maior_salto_falso_em_modulo']['grade_do_registro_12'], 3)} nos 12 da grade do registro e {nb(e1['maior_salto_falso_em_modulo']['vinte_de_3_em_3'], 3)} nos 20 de 3 em 3 minutos;")
        A(f"      com p < 0,001: {e1['cortes_falsos_com_p_abaixo_de_0_001']['grade_do_registro_12']} e {e1['cortes_falsos_com_p_abaixo_de_0_001']['vinte_de_3_em_3']}. O salto real ({nb(abs(e1['banda_8']['tau']), 3)}) {'é maior' if vv['1_descontinuidade']['maior_que_todos_os_cortes_falsos']['grade_12'] else 'NÃO é maior'} que todos os falsos da grade.")
        A('      Grade: ' + ', '.join(f"{x['corte'][:5]} {nb(x['tau'], 3, True)}" for x in f12))
        pl = e1['placebo_desfecho_anterior']
        A(f"      Desfecho placebo (1º turno controlado por 2022) no mesmo corte: {nb(pl['banda_8']['tau'], 3, True)} (ep {nb(pl['banda_8']['ep'], 3)}); bandas de 4 e 16: {nb(pl['banda_4']['tau'], 3, True)} e {nb(pl['banda_16']['tau'], 3, True)}. Limite do registro: 0,15.")
        p1 = e1['primeiro_turno_pausas']
        A('      Pausas do 1º turno (mesma conta, desfecho do 1º turno controlado por 2022): ' + '; '.join(f"{v_['corte']}: {nb(v_['tau'], 3, True)} (ep {nb(v_['ep'], 3)})" for v_ in p1.values()) + '.')
        dg = e1['degraus_de_vazao_exploratorio']
        A('      Degraus de vazão (exploratório do registro, só contam com p < 0,00017), banda de 8: ' + '; '.join(f"{k} {nb(v_['banda_8']['tau'], 3, True)} (p {nb(v_['banda_8']['p'], 3)})" for k, v_ in dg.items()) + '.')
        A('      Banda de 2: ' + '; '.join(f"{k} {nb(v_['banda_2']['tau'], 3, True)} (p {nb(v_['banda_2']['p'], 3)})" for k, v_ in dg.items()) + '.')
        br = e1['bruto_janelas_de_8_min']
        A(f"      Bruto de 2026, sem modelo: 8 minutos antes da pausa, {ni(br['secoes_antes'])} seções com {nb(br['fatia_1t_dos_dois_antes'], 2)}% no 1º turno e {nb(br['fatia_2t_antes'], 2)}% no 2º (virada {nb(br['fatia_2t_antes'] - br['fatia_1t_dos_dois_antes'], 2, True)});")
        A(f"      8 minutos depois, {ni(br['secoes_depois'])} seções com {nb(br['fatia_1t_dos_dois_depois'], 2)}% e {nb(br['fatia_2t_depois'], 2)}% (virada {nb(br['fatia_2t_depois'] - br['fatia_1t_dos_dois_depois'], 2, True)}). A composição muda no corte; a virada, não.")
        c1 = d36['e1_calibracao']['plantios']
        A('      Calibração (troca em toda seção recebida de 19:50 em diante, resíduo refeito, 100 cópias): '
          + '; '.join(f"+{x.replace('.', ',')} devolve {nb(c1[f'a_favor_de_lula_x{x}']['banda_8']['incremento_medio'], 3, True)} (detecta {nb(100 * c1[f'a_favor_de_lula_x{x}']['banda_8']['deteccao'], 0)}%)" for x in ('0.45', '0.9', '2.1')) + '.')
        A(f"      Devolve {nb(100 * c1['a_favor_de_lula_x0.45']['banda_8']['devolucao'], 0)}% do plantado porque o efeito fixo de zona absorve as zonas que entraram inteiras depois da pausa. Efeito mínimo detectável: {nb(d36['e1_calibracao']['emd_80_banda_8'], 2)} ponto.")
        A(f"      Espelho: plantio de 0,45 a favor de Flávio devolve {nb(c1['espelho_a_favor_de_flavio_x0.45']['banda_8']['incremento_medio'], 3, True)}; no dado real o critério espelhado {'É' if vv['1_descontinuidade']['espelho_a_favor_de_flavio'] else 'NÃO é'} cumprido.")
        i1 = d36['e1_explicacoes_inocentes']['plantios']
        A(f"      Inocentes: composição (2,1 pontos em zonas inteiras que entraram depois, {ni(i1['composicao_zona_inteira_depois_da_pausa']['secoes_alteradas'])} seções) mexe tau em {nb(i1['composicao_zona_inteira_depois_da_pausa']['incremento_medio'], 3, True)}: o teste não confunde bloco de zona com salto.")
        A(f"      Entrada de eleitores reais e abstenção pura depois da pausa devolvem {nb(100 * i1['entrada_de_eleitores_reais']['razao_para_a_troca_de_mesma_margem'], 0)}% e {nb(100 * i1['abstencao_pura']['razao_para_a_troca_de_mesma_margem'], 0)}% do que a troca devolve: o teste não separa troca de comparecimento.")
        A(f"      VEREDITO PELA LETRA: {vv['1_descontinuidade']['veredito']}." + (' Cláusulas: ' + '; '.join(vv['1_descontinuidade']['clausulas_de_inconclusivo']) + '.' if vv['1_descontinuidade']['clausulas_de_inconclusivo'] else ''))
        A('')
        A('  (2) Inclinação: r contra a posição do recebimento dentro da zona (0 = primeiro boletim da zona, 1 = último), sem prorrogadas.')
        A(f"      theta = {nb(e2['beta'], 3, True)} ponto (ep {nb(e2['ep'], 3)} por município, {nb(e2['erro_por_zona'], 3)} por zona; z {nb(e2['z'], 2, True)}; {pv(e2['p'])}); IC 95% {nb(e2['ic95'][0], 3, True)} a {nb(e2['ic95'][1], 3, True)}; n {ni(e2['n'])}.")
        A(f"      Margem pela fórmula do registro (theta x válidos totais): {ni(e2['margem_implicada'], True)} votos (IC 95% {ni(e2['margem_ic95'][0], True)} a {ni(e2['margem_ic95'][1], True)}), {nb(100 * e2['fracao_da_margem'], 1)}% da margem.")
        p2 = e2['placebo_desfecho_anterior']
        A(f"      Placebo (desfecho anterior): {nb(p2['beta'], 3, True)} (ep {nb(p2['ep'], 3)}); limite do registro 0,3.")
        A('      Bruto de 2026 por terço da posição na zona: ' + '; '.join(f"{t_['terco']}º terço: 1º turno {nb(t_['fatia_1t_dos_dois'], 2)}%, 2º turno {nb(t_['fatia_2t'], 2)}%, virada {nb(t_['fatia_2t'] - t_['fatia_1t_dos_dois'], 2, True)}" for t_ in e2['bruto_por_terco_da_posicao']) + '.')
        c2 = d36['e2_calibracao']['plantios']
        A('      Calibração (100 cópias, resíduo refeito). Rampa pela ordem NACIONAL de chegada: '
          + '; '.join(f"0 a {x.replace('.', ',')} devolve {nb(c2[f'ordem_nacional_x{x}']['incremento_medio'], 3, True)}" for x in ('0.9', '1.8', '3.6')) + f" (fator {nb(c2['ordem_nacional_x3.6']['devolucao'], 3)}).")
        A('      Rampa pela posição DENTRO da zona: ' + '; '.join(f"0 a {x.replace('.', ',')} devolve {nb(c2[f'posicao_na_zona_x{x}']['incremento_medio'], 3, True)}" for x in ('0.9', '1.8', '3.6')) + f". Efeito mínimo detectável: {nb(d36['e2_calibracao']['emd_80'], 3)} ponto.")
        fat = c2['ordem_nacional_x3.6']['devolucao']
        A(f"      Leitura calibrada: a rampa nacional que vira a eleição (0 a 3,6) apareceria aqui como theta de {nb(c2['ordem_nacional_x3.6']['incremento_medio'], 2)}, e cumpre o critério em {nb(100 * c2['ordem_nacional_x3.6']['cumpre_theta_0_9_e_p'], 0)}% das cópias.")
        A(f"      O theta medido equivale a uma rampa nacional de 0 a {nb(e2['beta'] / fat, 2)} ponto (teto de 95%: {nb(e2['ic95'][1] / fat, 2)}), isto é, {ni(e2['beta'] / fat / 100 * d36['validos_totais'])} votos de margem (teto {ni(e2['ic95'][1] / fat / 100 * d36['validos_totais'])},")
        A(f"      {nb(100 * e2['ic95'][1] / fat / 100 * d36['validos_totais'] / MARGEM, 1)}% da margem). Contado a partir do placebo ({nb(p2['beta'], 3, True)}) em vez de zero, a diferença é {nb(e2['beta'] - p2['beta'], 3, True)} e a rampa nacional equivalente vai a {nb((e2['beta'] - p2['beta']) / fat, 2)} ponto,")
        A(f"      {ni((e2['beta'] - p2['beta']) / fat / 100 * d36['validos_totais'])} votos ({nb(100 * (e2['beta'] - p2['beta']) / fat / 100 * d36['validos_totais'] / MARGEM, 1)}% da margem). Essa conta contra o placebo é exploratória.")
        A(f"      VEREDITO PELA LETRA: {vv['2_inclinacao']['veredito']}. O coeficiente é positivo e distinguível de zero ({pv(e2['p'])}), no sentido da hipótese, mas tem {nb(100 * e2['beta'] / 0.9, 0)}% do limiar de +0,9.")
        A('')
        A('  (3) Deslocados: seção recebida muito depois da mediana do próprio prédio, contra as vizinhas (efeito fixo de local).')
        A('      grupo                beta      ep      p       IC 95%          tratadas  placebo   com encerramento   margem implicada (IC 95%)')
        for k, rot in (('desloc_30', '30 minutos ou mais'), ('desloc_60', '60 minutos ou mais'), ('cauda', 'cauda (21:10 ou mais)')):
            o = e3[k]
            A(f"      {rot:20s} {nb(o['beta'], 3, True):>7s} {nb(o['ep'], 3):>6s} {nb(o['p'], 3):>6s} {nb(o['ic95'][0], 3, True):>7s} a {nb(o['ic95'][1], 3, True):>7s} {ni(o['tratadas_na_conta']):>8s} {nb(o['placebo_desfecho_anterior']['beta'], 3, True):>8s} {nb(o['com_controle_do_encerramento']['beta'], 3, True):>12s}          {ni(o['margem_implicada'], True)} ({ni(o['margem_ic95'][0], True)} a {ni(o['margem_ic95'][1], True)})")
        c3 = d36['e3_calibracao']
        A(f"      Calibração: +5 pontos plantados devolvem {nb(c3['desloc_30']['incremento_medio'], 2, True)} (detecta {nb(100 * c3['desloc_30']['deteccao'], 0)}%); efeito mínimo detectável {nb(c3['desloc_30']['emd_80'], 2)} (30 min), {nb(c3['desloc_60']['emd_80'], 2)} (60 min), {nb(c3['cauda']['emd_80'], 2)} (cauda).")
        A(f"      Inocente: entrada de eleitores reais nos deslocados devolve {nb(100 * d36['e3_explicacao_inocente_entrada']['razao_para_a_troca'], 0)}% do que a troca devolve (não separa).")
        A(f"      Bruto de 2026 (30 min): virada das deslocadas {nb(e3['desloc_30']['bruto']['virada_tratadas'], 2, True)}, das demais {nb(e3['desloc_30']['bruto']['virada_demais'], 2, True)}.")
        A('      VEREDITO PELA LETRA: ' + '; '.join(f"{rot}: {vv['3_' + k]['veredito']}" for k, rot in (('desloc_30', '30 min'), ('desloc_60', '60 min'), ('cauda', 'cauda'))) + '. O grupo é pequeno: mesmo no teto não move a margem.')
        A('')
    # ---------------- PARTE 3
    if hist and sha:
        t2 = hist['turno2']; t1 = hist.get('turno1'); pl = hist.get('plantios_2t', {}).get('deteccao', {})
        A('PARTE 3. D3-2 (PARTE RODADA): BWEB CONTRA O HISTÓRICO OFICIAL DA TOTALIZAÇÃO (publicado em 03/11) E .SHA512 DOS ZIPS')
        A(f"  2º turno, lido de novo direto dos 28 zips do bweb ({ni(hist['leitura_direta_2t']['secoes'])} seções; {hist['leitura_direta_2t']['secoes_diferentes_da_base_dados']} diferentes da base dados/).")
        A(f"  Histórico: {ni(t2['historico']['linhas'])} linhas, {ni(t2['passos'])} passos de totalização em {ni(t2['zonas'])} pares de município e zona.")
        A(f"  (a) Fim: último acumulado de cada município e zona contra a soma dos boletins. Unidades com diferença para 13, 22, brancos, nulos e comparecimento:")
        A(f"      zonas {sum(t2['zonas_com_d_diferente_de_zero'].values())} de {ni(t2['zonas'])}; municípios e cidades do exterior {sum(t2['municipios_com_d_diferente_de_zero'].values())} de {ni(t2['municipios'])}; UFs {sum(t2['ufs_com_d_diferente_de_zero'].values())} de 28; país 0.")
        A(f"      Totais iguais: Lula {ni(t2['total_bweb']['13'])}, Flávio {ni(t2['total_bweb']['22'])}, brancos {ni(t2['total_bweb']['B'])}, nulos {ni(t2['total_bweb']['N'])}, comparecimento {ni(t2['total_bweb']['comparecimento'])}, seções {ni(t2['secoes_bweb'])}.")
        A(f"      d líquido nacional (13 menos 22): {t2['d_liquido_nacional_13_menos_22']} voto. Aptos por zona: {t2['zonas_com_QT_APTOS_ZONA_diferente_do_bweb']} zonas diferentes ({ni(t2['aptos_bweb'])} dos dois lados).")
        A(f"  (b) Ordem: passos em que um boletim teria sido somado antes de recebido: {t2['passos_com_boletim_recebido_depois_do_passo_na_ordem_de_recebimento']}. Boletins sem passo: {t2['secoes_bweb'] - t2['secoes_com_passo_atribuido']}.")
        A(f"  (c) Passo a passo: {ni(t2['passos_que_fecham_na_ordem_de_recebimento'])} passos fecham voto a voto na ordem estrita de DT_BU_RECEBIDO; {ni(t2['passos_que_fecham_com_outra_ordem'])} fecham com a ordem trocada dentro de")
        A(f"      {ni(t2['trechos_com_ordem_trocada'])} trechos de 2 ou 3 passos vizinhos ({t2['passos_decididos_por_programacao_inteira']} deles resolvidos por programação inteira); sem atribuição possível: {t2['passos_sem_atribuicao_possivel']}; busca interrompida: {t2['passos_com_busca_interrompida_por_tempo']}.")
        dfs = t2['defasagem_totalizacao_menos_recebimento_s']; sm = t2['serie_por_minuto']
        A(f"  (d) Série por minuto: em {sm['minutos_em_que_o_historico_passa_o_recebido']} de {sm['minutos']} minutos o acumulado do histórico passa o acumulado recebido. Defasagem entre receber e somar: mediana {nb(dfs['mediana'], 0)} s,")
        A(f"      99% até {nb(dfs['p99'], 0)} s, máximo {nb(dfs['max'], 0)} s, nenhuma negativa. Maior fila: {ni(sm['maior_fila_em_secoes'])} boletins às {sm['minuto_da_maior_fila'][:5]} (a rajada), zerada no minuto seguinte.")
        A('      Em português: a série do histórico é a dos boletins do bweb, cada um somado segundos depois de recebido, sem voto a mais nem a menos em passo nenhum.')
        if pl:
            A('  Plantios numa cópia do bweb do 2º turno (20 sorteios cada):')
            A(f"      1 voto a mais para o 13 em 1 seção: aponta exatamente 1 zona, 1 município, 1 UF e o país em {pl['1_um_voto_a_mais']['aponta_exatamente_1_zona_1_municipio_1_uf_e_pais']} de 20 (e também no passo a passo em {pl['1_um_voto_a_mais']['acusa_tambem_no_passo_a_passo']});")
            A(f"      1 seção retirada: aponta 1 zona em {pl['2_secao_retirada']['aponta_exatamente_1_zona']} de 20; 10 votos trocados entre dois municípios da mesma UF: aponta os 2 municípios, com UF e país fechando, em {pl['3_dez_votos_entre_municipios']['aponta_2_municipios_uf_fecha_pais_fecha']} de 20;")
            A(f"      hora de recebimento trocada entre passos (boletim somado antes de recebido): acusa em {pl['4_hora_trocada_entre_passos']['acusa']} de 20. Inocente (hora trocada dentro do mesmo passo): acusa em {pl['5_hora_trocada_no_mesmo_passo']['acusa']} de 20.")
        if t1:
            lit = t1['passada_pela_letra_votavel_a_votavel']
            A(f"  Placebo, 1º turno (base dados/ e hora do bweb): {ni(t1['passos'])} passos em {ni(t1['zonas'])} zonas, 13 candidatos mais brancos e nulos.")
            A(f"      Votável a votável, tudo zero menos dois: o 28 (candidatura anulada) tem {ni(lit['d_nacional_bweb_menos_historico']['28'])} votos como nominais no bweb e zero no histórico, e os nulos do histórico têm exatamente")
            A(f"      esses {ni(-lit['d_nacional_bweb_menos_historico']['N'])} a mais ({ni(lit['zonas_com_d_diferente_de_zero']['28'])} zonas). É classificação do candidato anulado, não voto de 13 nem de 22. Somando nulos e 28 dos dois lados:")
            A(f"      diferença zero em todas as zonas; {ni(t1['passos_que_fecham_na_ordem_de_recebimento'])} passos fecham na ordem, {t1['passos_que_fecham_com_outra_ordem']} com ordem trocada, {t1['passos_sem_atribuicao_possivel']} sem atribuição; defasagem mediana {nb(t1['defasagem_totalizacao_menos_recebimento_s']['mediana'], 0)} s, máximo {nb(t1['defasagem_totalizacao_menos_recebimento_s']['max'], 0)} s.")
        s = sha['resumo']
        A(f"  .sha512: {s['zips']} zips do bweb ({s['turno1']} do 1º turno, {s['turno2']} do 2º). Iguais ao resumo baixado junto com o zip (26 e 28/10): {s['iguais_ao_resumo_baixado_com_o_zip']}. Iguais ao resumo que o repositório")
        A(f"      serve hoje ({sha['baixado_em_utc']}, {sha['pedidos']} pedidos a 1 por segundo, nenhum 429): {s['iguais_ao_resumo_de_hoje']}. Diferentes: {len(s['diferentes'])}. Os dois zips do histórico têm o SHA-256 anotado em 09/11.")
        un = hist.get('universo')
        if un:
            A(f"  Universo: a configuração do site lista {ni(un['2']['secoes_na_configuracao'])} seções no 2º turno = {ni(un['2']['no_bweb'])} do bweb + {len(un['2']['so_na_configuracao_com_hora'])} com hora e fora do bweb ({', '.join(un['2']['so_na_configuracao_com_hora'])}) + {un['2']['so_na_configuracao_sem_hora']} sem hora.")
            A(f"      Nenhuma seção do bweb falta na configuração. O histórico traz QT_SECOES_BRASIL = {ni(t2['historico']['QT_SECOES_BRASIL'][0])} e QT_APTOS_BRASIL = {ni(t2['historico']['QT_APTOS_BRASIL'][0])}, {ni(t2['historico']['QT_APTOS_BRASIL'][0] - t2['aptos_bweb'])} aptos a mais que o bweb: são as 43 seções fora dele.")
        A('  Pontos a explicar, sem voto envolvido: a coluna QT_APTOS_TOT do histórico traz o comparecimento do passo, e não os aptos como diz o LEIAME do TSE; e o')
        A('      histórico soma o 28 em nulos enquanto o bweb o mantém como nominal.')
        A(f"  VEREDITO PELA LETRA (só a parte rodada): {V['D3-2 (parte rodada) bweb contra o histórico e .sha512']}. Aviso do desenho: isso prova que bweb e histórico são a mesma conta; não diz nada sobre mudança")
        A('      feita antes de o boletim existir e levada de forma coerente às duas camadas. Faltam o JSON oficial por município e o aux.json da amostra antiga (onda D).')
        A('')
    # ---------------- PARTE 4
    A('PARTE 4. ALEGAÇÕES NOVAS, AO PÉ DA LETRA (critérios meus, escritos antes de calcular; não são do registro)')
    if r1:
        a = r1['a_aritmetica']; o = r1['b_dose']['principal']; o2 = r1['b_dose']['todas_com_dose_limitada_a_50']; cal = r1['calibracao']; v = r1['veredito']
        A('  R1. "Código ativado às 17h01 transfere um voto a cada dez segundos; quanto mais tempo a urna fica aberta, maior a diferença."')
        A(f"    (a) Aritmética da própria alegação: {ni(a['secoes_que_encerraram_depois_de_17h01'])} seções encerraram depois de 17:01:00 de Brasília (mediana de {nb(a['mediana'], 0)} s depois). Um voto a cada 10 s daria")
        A(f"        {ni(a['total_que_a_alegacao_preve_transferido'])} votos transferidos, isto é, {ni(a['margem_que_isso_deslocaria'])} de margem: {nb(a['razao_para_a_margem_oficial'], 2)} vezes a margem oficial. Flávio teria tido {ni(a['flavio_teria_sem_a_transferencia'])} votos, {nb(100 * a['flavio_teria_sem_a_transferencia'] / (a['votos_de_flavio_oficiais'] + a['votos_de_lula_oficiais']), 1)}% dos válidos.")
        A(f"        Em {ni(a['secoes_em_que_T_passa_dos_votos_de_lula'])} seções o número previsto passa de TODOS os votos que Lula teve na seção (impossível), inclusive nas {ni(a['entre_as_que_encerraram_de_19h_em_diante']['secoes'])} que encerraram de 19h em diante")
        A(f"        (previsto {nb(a['entre_as_que_encerraram_de_19h_em_diante']['T_medio'], 0)} votos transferidos por urna, comparecimento médio {nb(a['entre_as_que_encerraram_de_19h_em_diante']['comparecimento_medio'], 0)}).")
        A(f"    (b) Dose: kappa = fração da taxa alegada que aparece nos votos (1 = a alegação vale; 0 = o horário não transfere nada). Seções que encerraram antes de 17:10 (n {ni(o['n'])}),")
        A(f"        efeito fixo de local: kappa = {nb(o['beta'], 4, True)} (ep {nb(o['ep'], 4)}; {pv(o['p'])}); IC 95% {nb(o['ic95'][0], 4, True)} a {nb(o['ic95'][1], 4, True)}. O teto equivale a 1 voto a cada {nb(10 / o['ic95'][1] / 60, 0)} minutos, não a cada 10 segundos.")
        A(f"        Margem implicada: {ni(o['margem_implicada'], True)} votos (IC 95% {ni(o['margem_ic95'][0], True)} a {ni(o['margem_ic95'][1], True)}), {nb(100 * o['margem_implicada'] / MARGEM, 2)}% da margem. Todas as seções com dose limitada: {nb(o2['beta'], 4, True)} (ep {nb(o2['ep'], 4)}).")
        pp = o['placebo_desfecho_anterior']
        A(f"        Placebo (1º turno controlado por 2022, mesma dose): {nb(pp['beta'], 4, True)} (ep {nb(pp['ep'], 4)}): do tamanho do efeito e de sinal contrário. Contra o placebo a diferença seria {nb(o['beta'] - pp['beta'], 4, True)},")
        A(f"        {ni(2 * (o['beta'] - pp['beta']) * o['soma_de_T_da_classe'])} votos de margem ({nb(100 * 2 * (o['beta'] - pp['beta']) * o['soma_de_T_da_classe'] / MARGEM, 1)}% da margem). O kappa positivo é pequeno demais para ser a alegação e não se separa do ruído do desenho.")
        A('    (c) Dez grupos por horário de encerramento (diferença ajustada contra o grupo que encerrou antes de 17:01, mesmo prédio):')
        A('        grupo               seções   encerra   T previsto  virada bruta   previsto pela alegação   medido (ep)')
        for l in r1['c_dez_grupos_fixos']:
            med = f"{nb(l['diferenca_ajustada'], 3, True)} ({nb(l['ep'], 3)})" if 'diferenca_ajustada' in l else 'referência'
            A(f"        {l['grupo']:18s} {ni(l['secoes']):>8s}  {l['encerramento_medio']}  {nb(l['T_medio_previsto_votos'], 1):>8s}    {nb(l['virada_bruta'], 2, True):>7s}        {nb(l['diferenca_prevista_pela_alegacao'], 1, True):>8s} pontos       {med}")
        A(f"        Grupos em que aparece pelo menos metade do previsto: {r1['c_resumo']['grupos_que_confirmam_a_alegacao']} de 9. A virada bruta de 2026 é a mesma (2,8 a 3,3 pontos) em quem fechou às 17:00 e em quem ficou aberto até as 19h.")
        A(f"    Calibração: a alegação plantada devolve kappa {nb(cal['1_voto_a_cada_10_s']['incremento_de_kappa'], 3, True)}; 1 voto a cada 100 s devolve {nb(cal['1_voto_a_cada_100_s']['incremento_de_kappa'], 4, True)}; a cada 1.000 s, {nb(cal['1_voto_a_cada_1000_s']['incremento_de_kappa'], 4, True)} (z {nb(cal['1_voto_a_cada_1000_s']['z_do_incremento'], 1)}).")
        A(f"        Efeito mínimo detectável: {nb(r1['emd_80_votos_por_10_s'], 4)} voto a cada 10 s. Espelho (de Lula para Flávio): {nb(cal['espelho_1_voto_a_cada_10_s_de_lula_para_flavio']['incremento_de_kappa'], 3, True)}. Inocentes: fila real repartida como a seção mexe {nb(100 * r1['explicacoes_inocentes']['fila_real_repartida_como_a_secao']['razao_para_a_transferencia_de_mesma_margem'], 0)}%;")
        A(f"        entrada de eleitores reais de Lula aparece com {nb(100 * r1['explicacoes_inocentes']['entrada_de_eleitores_reais_de_lula']['razao_para_a_transferencia_de_mesma_margem'], 0)}% do tamanho da transferência (o teste não separa as duas).")
        A(f"    VEREDITO: a alegação ao pé da letra está {v['alegacao_ao_pe_da_letra']}; efeito do horário com alcance: {v['efeito_do_horario_com_alcance']}. Não li os logs (votos depois das 17h01 por urna): fica para a onda C.")
        A('')
    if r7:
        ai = r7['a_instante_exato']; c = r7['c_fim']; e = r7.get('exploratorio', {})
        A('  R7. "Cadê os 165.699 votos do Nine?" (total nacional de Lula menos a soma das páginas dos estados e do exterior; tela com Lula 193.574 e Flávio 142.169)')
        if ai:
            A(f"    (a) A tela existe no histórico: o acumulado nacional é exatamente Lula 193.574 e Flávio 142.169 às {ai[0]['hora']}, com {ni(ai[0]['secoes'])} seções ({nb(ai[0]['pct_das_secoes'], 2)}% das 499.248).")
            A('        É o ponto em que a divulgação parou (a imprensa registrou 0,25%). A totalização interna seguiu até 17:07:37: ' + '; '.join(f"até {x['ate'][:5]}: Lula {ni(x['lula'])}, Flávio {ni(x['flavio'])}, {ni(x['secoes'])} seções" for x in r7['a_no_fim_de_cada_minuto_ate_17h07']) + '.')
            A(f"        As {ni(r7['b_fim_de_17h07']['secoes'] - ai[0]['secoes'])} seções somadas depois desse instante e antes da pausa não estão na tela do vídeo (gravado por volta das 17h57, segundo a checagem): se a divulgação ficou")
            A('        parada ali durante toda a pausa, elas só apareceram ao público depois das 19h. Isso é inferência da tela e do registro da imprensa, não dado do TSE.')
        else:
            A(f"    (a) Não há instante com o acumulado exato; o mais próximo: {json.dumps(r7['a_mais_proximo'], ensure_ascii=False)}.")
        A(f"    (b) De onde sairia 165.699: não há instante anterior com Lula = 27.875 no país ({len(r7['b_instante_com_lula_27875'])}) nem só nas 27 UFs ({e.get('instantes_com_lula_27875_nas_27_ufs')}). A busca por conjuntos de UFs que somem 165.699 no")
        if 'b_instante_da_tela' in r7:
            A(f"        instante da tela acha {r7['b_instante_da_tela']['n_conjuntos']} conjuntos, mas com {r7['b_instante_da_tela']['ufs_com_voto']} UFs há 2^{r7['b_instante_da_tela']['ufs_com_voto']} conjuntos e o acaso dá {nb(e.get('conjuntos_esperados_por_acaso_para_um_numero_qualquer'), 1)} por número: essa busca NÃO distingue nada (teste meu sem poder).")
            x = e.get('no_instante_da_tela', {})
            A(f"        Exploratório: naquele instante {ni(x.get('lula_no_exterior', 0))} dos 193.574 votos de Lula ({nb(100 * x.get('fracao_do_exterior_nos_votos_de_lula_da_tela', 0), 0)}%) eram do exterior ({ni(x.get('secoes_do_exterior', 0))} seções), e as 27 UFs somavam {ni(x.get('lula_nas_27_ufs', 0))}.")
            A('        O exterior sozinho não é o número (faltam 24.313), então a conta do vídeo não se reproduz ao voto; ela depende de em que estado estava cada página.')
        A(f"    (c) O que a alegação prevê, votos de Lula sem seção de origem, não existe: total nacional menos soma das UFs = {c['nacional_menos_soma_das_ufs_no_historico']} no histórico; Lula no histórico {ni(c['lula_historico'])},")
        A(f"        no bweb {ni(c['lula_bweb'])}, no JSON oficial nacional {ni(c['lula_json_oficial_nacional']) if c['lula_json_oficial_nacional'] else 'n/d'}. Cada passo do histórico pertence a um município e zona, e todos fecham com boletins (parte 3).")
        A(f"    VEREDITO: {r7['veredito']}. O número previsto é 165.699; o medido é 0. A diferença entre painéis no meio da pausa é atraso de publicação, não voto.")
        A('')
    if r8:
        f = r8['a_fato']; b = r8['b_composicao']; c = r8['c_curvas']; d = r8['d_dentro_da_zona']; o = d['universo_G2']
        A('  R8. "Flávio tinha tendência de vitória com 30% apurado."')
        A(f"    (a) O fato confere: com 23% das seções Flávio tinha {nb(f['com_23_pct_das_secoes']['flavio_pct'], 2)}% do acumulado ({f['com_23_pct_das_secoes']['hora']}); com 30%, {nb(f['com_30_pct_das_secoes']['flavio_pct'], 2)}% ({f['com_30_pct_das_secoes']['hora']}); com 38%, {nb(f['com_38_pct_das_secoes']['flavio_pct'], 2)}%.")
        tr = f['trocas_de_lideranca']
        noite = [x for x in tr if x['hora'] >= '19:00:00']
        t_a = noite[0]['hora'] if noite else 'n/d'
        t_b = [x for x in noite if x['hora'] < '20:00:00'][-1]['hora'] if [x for x in noite if x['hora'] < '20:00:00'] else 'n/d'
        t_c = [x for x in noite if x['hora'] >= '20:00:00'][0]['hora'] if [x for x in noite if x['hora'] >= '20:00:00'] else 'n/d'
        A(f"        Lula liderou até {t_a}, Flávio de {t_b} a {t_c}, Lula de {tr[-1]['hora']} em diante ({f['trocas_de_lideranca_n']} cruzamentos passo a passo, {len(noite)} deles nesses dois momentos da noite).")
        A(f"        Maior fatia de Flávio depois dos 5% das seções: {nb(f['maior_vantagem_de_flavio']['flavio_pct'], 2)}% às {f['maior_vantagem_de_flavio']['hora']}. Final: {nb(f['final_flavio_pct'], 2)}%.")
        A(f"    (b) Composição: as primeiras 30% das seções (recebidas até {b['ultima_hora_de_recebimento_das_30']}) deram a Flávio {nb(b['flavio_2t_nas_30'], 2)}% no 2º turno, {nb(b['g2'], 2, True)} ponto acima do final do país ({nb(b['flavio_2t_pais'], 2)}%).")
        A(f"        As MESMAS seções já tinham dado a Flávio, no 1º turno, {nb(b['flavio_1t_dos_dois_nas_30'], 2)}% dos votos dos dois, {nb(b['g1'], 2, True)} ponto acima do país ({nb(b['flavio_1t_dos_dois_pais'], 2)}%).")
        A(f"        Se a parcial fosse representativa, esse segundo número seria zero. Sobra g2 - g1 = {nb(b['g2_menos_g1'], 2, True)} ponto; uma alteração ligada depois dos 30% que virasse a eleição prevê +1,79.")
        A(f"        Bruto de 2026: virada a favor de Lula de {nb(b['virada_a_favor_de_lula_nas_30'], 2)} pontos nas primeiras 30% e de {nb(b['virada_nas_demais'], 2)} nas demais (país {nb(b['virada_no_pais'], 2)}).")
        A(f"    (c) Curva prevista sem ajuste: usando só o 1º turno de cada seção e a variação nacional, a fatia prevista de Flávio aos 30% é {nb(c['curva_do_1t_aos_30'], 2)}% (real {nb(c['real_aos_30'], 2)}%);")
        A(f"        a maior distância entre a curva real e a prevista, em toda a apuração, é {nb(c['diferenca_maxima_real_menos_1t'], 2)} ponto. A troca de liderança prevista cai às {c['trocas_previstas_pela_curva_do_1t'][-1]['hora']}; a real (pela ordem de recebimento), às {c['trocas_reais_pela_ordem_de_recebimento'][-1]['hora']}.")
        A(f"        Com a fatia final de cada zona no lugar do voto da seção: {nb(c['curva_das_zonas_aos_30'], 2)}% aos 30%, distância máxima {nb(c['diferenca_maxima_real_menos_zonas'], 2)}.")
        A(f"    (d) Dentro da zona (seção entre as primeiras 30% contra as demais da mesma zona, controles do registro): {nb(o['beta'], 3, True)} ponto (ep {nb(o['ep'], 3)}; {pv(o['p'])}); IC 95% {nb(o['ic95'][0], 3, True)} a {nb(o['ic95'][1], 3, True)};")
        A(f"        {ni(o['zonas_com_os_dois_lados'])} zonas com os dois lados. Uma alteração ligada aos 30% prevê -2,55. Margem implicada: {ni(o['margem_implicada'], True)} votos (IC 95% {ni(o['margem_ic95'][0], True)} a {ni(o['margem_ic95'][1], True)}), {nb(100 * o['margem_implicada'] / MARGEM, 1)}% da margem.")
        A(f"        Placebo (desfecho anterior): {nb(o['placebo_desfecho_anterior']['beta'], 3, True)} (ep {nb(o['placebo_desfecho_anterior']['ep'], 3)}), do mesmo tamanho e sinal. Plantios de 2,55 e 0,45 devolvem {nb(o['calibracao']['x2.55']['incremento_medio'], 2, True)} e {nb(o['calibracao']['x0.45']['incremento_medio'], 2, True)} (detecção {nb(100 * o['calibracao']['x0.45']['deteccao'], 0)}%).")
        A(f"    VEREDITO: o fato é verdadeiro e a inferência não: {r8['veredito']['dentro_da_zona']}. A liderança de Flávio com 30% é o que a ordem de chegada das seções prevê, com erro de {nb(c['diferenca_maxima_real_menos_1t'], 2)} ponto.")
        A('')
    # ---------------- exploratório
    if ex:
        A('EXPLORATÓRIO (feito DEPOIS de ver os resultados acima; sem critério registrado; não entra em veredito)')
        A('  Como o indício da Onda A passa pelo comparecimento e o modelo do registro controla o comparecimento, os mesmos contrastes de hora foram refeitos com o')
        A('  comparecimento como desfecho (pontos percentuais dos aptos), sem esse controle. Lê-se: quem foi recebido ANTES da retenção, e portanto não pode ter sido')
        A('  mexido durante ela, teve variação de comparecimento diferente da seção gêmea recebida depois?')
        rot = {'fatia_de_lula_sem_controle_do_comparecimento': 'fatia de Lula, sem o controle do comparecimento (pontos)', 'variacao_do_comparecimento_pp_dos_aptos': 'variação do comparecimento (pp dos aptos)',
               'ganho_de_lula_pp_dos_aptos': 'ganho de Lula entre os turnos (pp dos aptos)', 'ganho_de_flavio_pp_dos_aptos': 'ganho de Flávio entre os turnos (pp dos aptos)',
               'variacao_de_brancos_e_nulos_pp_dos_aptos': 'variação de brancos e nulos (pp dos aptos)'}
        A('  desfecho                                                   cedo menos tardias: A (mesmo prédio)   B (cedo contra rajada)   C (zona)       salto na pausa     inclinação na zona')
        for k, r_ in rot.items():
            a = ex['d35']['A'][k]; b = ex['d35']['B'][k]; c = ex['d35']['C'][k]; s_ = ex['d36'][k]['salto_na_pausa_banda_8']; i_ = ex['d36'][k]['inclinacao_na_zona']
            A(f"  {r_:58s} {nb(a['beta'], 3, True):>8s} ({nb(a['ep'], 3)})        {nb(b['beta'], 3, True):>8s} ({nb(b['ep'], 3)})      {nb(c['beta'], 3, True):>8s} ({nb(c['ep'], 3)})   {nb(s_['tau'], 3, True):>8s} ({nb(s_['ep'], 3)})   {nb(i_['beta'], 3, True):>8s} ({nb(i_['ep'], 3)})")
        A(f"  Régua: se a margem inteira tivesse entrado como comparecimento a mais só nas seções recebidas depois da retenção, a variação do comparecimento delas seria {nb(ex['referencia']['margem_sobre_aptos_das_tardias_pp'], 2)} pp dos aptos")
        A('  maior que a das cedo (coeficiente negativo desse tamanho na linha do comparecimento).')
        xa = ex['d35']['A']; xb = ex['d35']['B']; xc = ex['d35']['C']; kc = 'variacao_do_comparecimento_pp_dos_aptos'; kb = 'variacao_de_brancos_e_nulos_pp_dos_aptos'
        apt_t = ex['referencia']['aptos_das_tardias']
        A(f"  Leituras: (i) nos desenhos de gêmeas a variação do comparecimento é a mesma: {nb(xa[kc]['beta'], 3, True)} (ep {nb(xa[kc]['ep'], 3)}) no mesmo prédio e {nb(xb[kc]['beta'], 3, True)} (ep {nb(xb[kc]['ep'], 3)}) contra a rajada.")
        A(f"  (ii) Em C (zona inteira, o desenho mais fraco) as cedo tiveram {nb(xc[kc]['beta'], 2, True)} pp de variação do comparecimento (ep {nb(xc[kc]['ep'], 2)}), repartido quase igual entre os dois: Lula {nb(xc['ganho_de_lula_pp_dos_aptos']['beta'], 2, True)},")
        A(f"  Flávio {nb(xc['ganho_de_flavio_pp_dos_aptos']['beta'], 2, True)}. Não gera margem; é o que se espera de seção sem fila, que transmite primeiro.")
        A(f"  (iii) Brancos e nulos caíram um pouco MENOS nas cedo que nas gêmeas tardias: {nb(xa[kb]['beta'], 3, True)} (ep {nb(xa[kb]['ep'], 3)}) em A e {nb(xb[kb]['beta'], 3, True)} (ep {nb(xb[kb]['ep'], 3)}) em B. Se fosse tudo branco e nulo convertido em voto de Lula")
        A(f"  durante a retenção, valeria {ni(xa[kb]['beta'] / 100 * apt_t)} votos de margem pela conta de A ({nb(100 * xa[kb]['beta'] / 100 * apt_t / MARGEM, 1)}% da margem) e {ni(xb[kb]['beta'] / 100 * apt_t)} pela de B. São 25 contas exploratórias: a 5% o acaso dá uma ou duas")
        A('  desse tamanho, e o ganho de Lula nas mesmas contas não acompanha (linha do ganho de Lula). Fica como pista para o teste de branco e nulo, não como indício.')
        s_ = ex['d36'][kc]['inclinacao_na_zona']
        A(f"  (iv) Dentro da zona, boletim que chega mais tarde tem um pouco mais de aumento de comparecimento ({nb(s_['beta'], 3, True)} pp, ep {nb(s_['ep'], 3)}), que aparece como ganho de Lula ({nb(ex['d36']['ganho_de_lula_pp_dos_aptos']['inclinacao_na_zona']['beta'], 3, True)})")
        A(f"  e perda de Flávio ({nb(ex['d36']['ganho_de_flavio_pp_dos_aptos']['inclinacao_na_zona']['beta'], 3, True)}): é o mesmo theta do D3-6 (2) visto pelo comparecimento. Tamanho: centésimos de ponto.")
        A('')
    # ---------------- a favor e contra
    favor = []; contra = []
    if d36:
        e2 = d36['e2_inclinacao']; fat = d36['e2_calibracao']['plantios']['ordem_nacional_x3.6']['devolucao']
        favor.append(f"D3-6 (2): dentro da zona, boletim que chegou mais tarde virou um pouco mais para Lula: theta = {nb(e2['beta'], 3, True)} (ep {nb(e2['ep'], 3)}, {pv(e2['p'])}), no sentido da hipótese, enquanto o placebo com desfecho anterior tem o sinal contrário ({nb(e2['placebo_desfecho_anterior']['beta'], 3, True)}). É {nb(100 * e2['beta'] / 0.9, 0)}% do limiar; lido como rampa nacional, vale de {ni(e2['beta'] / 100 * d36['validos_totais'])} a {ni((e2['beta'] - e2['placebo_desfecho_anterior']['beta']) / fat / 100 * d36['validos_totais'])} votos de margem conforme a régua (1% a 10% da margem). O teste não separa isso de eleitor de fim de fila.")
    if r8:
        o = r8['d_dentro_da_zona']['universo_G2']
        favor.append(f"R8 (d): as seções das primeiras 30% viraram {nb(-o['beta'], 3)} ponto a menos para Lula que as demais da mesma zona ({pv(o['p'])}), mesmo sentido; mas o placebo dá o mesmo ({nb(o['placebo_desfecho_anterior']['beta'], 3, True)}), então não é novidade do 2º turno. No bruto, g2 - g1 = {nb(r8['b_composicao']['g2_menos_g1'], 2, True)} ponto.")
    if r1:
        o = r1['b_dose']['principal']
        favor.append(f"R1: o kappa é positivo ({nb(o['beta'], 4, True)}, {pv(o['p'])}): seção que fechou segundos mais tarde tem fatia de Lula um nada maior no mesmo prédio. Vale {ni(o['margem_implicada'])} votos de margem ({nb(100 * o['margem_implicada'] / MARGEM, 1)}%), {nb(1 / o['beta'], 0)} vezes menos que a alegação, e o placebo tem tamanho maior com sinal contrário.")
    if d35:
        pb3 = d35['placebos']['3_primeiro_turno_primeiras_recebidas']
        favor.append(f"D3-5: o veredito pela letra não é SEM SINAL e sim {d35['veredito']['veredito']}, porque o placebo (3) do 1º turno deu {nb(pb3['beta'], 2, True)} (ep {nb(pb3['ep'], 2)}): as primeiras seções recebidas no 1º turno já diferiam das seguintes da zona. Isso tira do teste a absolvição formal, embora o coeficiente real tenha o sinal contrário ao da hipótese e os placebos comparáveis a ele, (1) e (2), fiquem abaixo de 0,15.")
    if ex:
        xa = ex['d35']['A']['variacao_de_brancos_e_nulos_pp_dos_aptos']; xb = ex['d35']['B']['variacao_de_brancos_e_nulos_pp_dos_aptos']
        favor.append(f"Exploratório: brancos e nulos caíram um pouco menos nas seções recebidas antes da retenção que nas gêmeas recebidas depois ({nb(xa['beta'], 3, True)} pp dos aptos, ep {nb(xa['ep'], 3)}, no mesmo prédio; {nb(xb['beta'], 3, True)}, ep {nb(xb['ep'], 3)}, contra a rajada). No teto, {ni(xa['beta'] / 100 * ex['referencia']['aptos_das_tardias'])} votos de margem ({nb(100 * xa['beta'] / 100 * ex['referencia']['aptos_das_tardias'] / MARGEM, 1)}%). Uma de 25 contas exploratórias; o ganho de Lula nas mesmas seções não acompanha.")
    favor.append('Limite de alcance que continua de pé: nada aqui testa alteração feita dentro da urna antes de o boletim existir, igual em todas as horas; e o histórico e o bweb saem do mesmo banco do TSE, então a igualdade entre os dois não é conferência independente. Continuam sem publicação o perfil do comparecimento do 2º turno e os logs do receptor de arquivos.')
    favor.append('Pontos sem explicação pública: a retenção de 116 minutos com 1.868 boletins já somados (645 deles fora da tela divulgada, pelo que o vídeo das 17h57 mostra), a coluna QT_APTOS_TOT do histórico com comparecimento no lugar de aptos, e as 2 seções do exterior com hora no site e fora do bweb.')
    if d35:
        a = d35['observado']['A']; b = d35['observado']['B']
        contra.append(f"D3-5: os boletins recebidos ANTES da retenção, que não podem ter sido mexidos durante ela, viraram para Lula tanto quanto os gêmeos que esperaram duas horas: {nb(a['beta'], 3, True)} (ep {nb(a['ep'], 3)}) no mesmo prédio e {nb(b['beta'], 3, True)} (ep {nb(b['ep'], 3)}) contra a rajada. Uma alteração na retenção que virasse a eleição daria -1,79 (z perto de {nb(1.79 / a['ep'], 0)}); o intervalo de 95% exclui até -0,45. O plantio de 1,79 é detectado em 100% das cópias.")
    if d36:
        e1 = d36['e1_descontinuidade']
        contra.append(f"D3-6 (1): não há salto na pausa das 19:48: {nb(e1['banda_8']['tau'], 3, True)} (ep {nb(e1['banda_8']['ep'], 3)}), menor que o maior de 12 cortes falsos ({nb(e1['maior_salto_falso_em_modulo']['grade_do_registro_12'], 3)}) e igual ao do desfecho placebo ({nb(e1['placebo_desfecho_anterior']['banda_8']['tau'], 3, True)}). Teto de 95%: {ni(e1['banda_8']['margem_ic95'][1])} votos de margem ({nb(100 * e1['banda_8']['margem_ic95'][1] / MARGEM, 1)}%). O plantio de 0,45 é detectado em 100% das cópias.")
        contra.append(f"D3-6 (3): boletins que chegaram 30 minutos ou mais depois dos vizinhos de prédio não viraram mais para Lula ({nb(d36['e3_deslocados']['desloc_30']['beta'], 3, True)}, ep {nb(d36['e3_deslocados']['desloc_30']['ep'], 3)}); nem os de 60 minutos nem a cauda.")
    if hist:
        contra.append(f"D3-2: o histórico oficial e o bweb são a mesma conta, zona a zona e passo a passo: {ni(hist['turno2']['passos'])} passos, nenhum com voto que não venha de boletim recebido antes dele; nenhum boletim somado antes de recebido; nenhum recebido e não somado. Um único voto plantado é apontado em 20 de 20 sorteios. Os 56 zips do bweb continuam iguais aos resumos publicados.")
    if r1:
        contra.append(f"R1: a alegação das 17h01 erra por três ordens de grandeza: prevê {ni(r1['a_aritmetica']['total_que_a_alegacao_preve_transferido'])} votos transferidos e mais votos transferidos que votos de Lula em {ni(r1['a_aritmetica']['secoes_em_que_T_passa_dos_votos_de_lula'])} seções; o teto medido é de 1 voto a cada {nb(10 / r1['b_dose']['principal']['ic95'][1] / 60, 0)} minutos. Nos dez grupos, nenhum mostra nem metade do previsto.")
    if r7:
        contra.append('R7: os "165.699 votos sem origem" não existem no resultado: a tela é o estado das 17:06:27, e nacional menos soma das UFs é zero.')
    if r8:
        contra.append(f"R8: a liderança de Flávio com 30% apurado é prevista pelo 1º turno das mesmas seções ({nb(r8['c_curvas']['curva_do_1t_aos_30'], 2)}% previsto, {nb(r8['c_curvas']['real_aos_30'], 2)}% real); a curva inteira da apuração sai do 1º turno mais uma variação nacional uniforme com erro máximo de {nb(r8['c_curvas']['diferenca_maxima_real_menos_1t'], 2)} ponto.")
    if ex:
        a = ex['d35']['A']['variacao_do_comparecimento_pp_dos_aptos']; b = ex['d35']['B']['variacao_do_comparecimento_pp_dos_aptos']
        contra.append(f"Exploratório, canal do comparecimento: a variação do comparecimento das seções recebidas antes da retenção não difere da das gêmeas recebidas depois ({nb(a['beta'], 3, True)} pp dos aptos, ep {nb(a['ep'], 3)}, no mesmo prédio; {nb(b['beta'], 3, True)}, ep {nb(b['ep'], 3)}, contra a rajada), contra {nb(-ex['referencia']['margem_sobre_aptos_das_tardias_pp'], 2)} se a margem tivesse entrado como voto a mais durante a retenção.")
    A('O QUE PESA A FAVOR DA TESE')
    for i, x in enumerate(favor, 1):
        A(f'  {i}. {x}')
    A('')
    A('O QUE PESA CONTRA A TESE')
    for i, x in enumerate(contra, 1):
        A(f'  {i}. {x}')
    A('')
    significa = ('A totalização não é o lugar da virada. Se a diferença de 4,43 milhões tivesse sido fabricada na fila de espera das 17:08 às 19:03, numa pausa, aos poucos ao longo da noite ou em boletins segurados, '
                 'os boletins que entraram antes teriam de se comportar diferente dos que entraram depois, e não se comportam: os contrastes ficam em centésimos de ponto, com poder medido para meio ponto. '
                 'O que o TSE publicou como histórico é, passo a passo, a soma dos boletins do bweb. Para a pergunta desta onda (mobilização desigual ou irregularidade no registro de quem votou), este teste fecha uma porta: '
                 'a diferença de comparecimento entre eleitores de Flávio e de Lula já está nos boletins na hora em que cada urna os emitiu, igual para os recebidos antes e depois da retenção. '
                 'Se houve irregularidade, ela está antes da transmissão: na seção (mesa, caderno, habilitação) ou no programa da urna. Não separa as duas leituras; diz onde não procurar.')
    A('O QUE ISSO SIGNIFICA')
    A('  ' + significa)
    A('')
    pistas = ['Caderno de votação e boletim impresso continuam sendo a única conferência independente: priorizar PI, MA, TO, PB e CE (Adendo 28).',
              'Completar o D3-2 na onda D: JSON oficial por município (5.750 pedidos) e aux.json da amostra antiga, para fechar a terceira camada.',
              'Pedir ao TSE o registro da ordem de retenção e de retomada (horários e quem mandou), os logs do receptor de arquivos e a explicação para as 645 seções somadas de 17:06:27 a 17:07:37 que não aparecem na tela gravada às 17h57.',
              'O theta positivo dentro da zona (0,05 ponto) merece uma conta com os logs: se for eleitor de fim de fila, some ao controlar a hora do último voto da urna (onda C).',
              'R1 nos logs (votos computados depois das 17h01 por urna contra o ganho de Lula) não foi feito aqui.',
              'Pedir ao TSE a correção do LEIAME do histórico (QT_APTOS_TOT traz comparecimento) e a identificação das 2 seções do exterior com hora no site e fora do bweb.']
    A('PISTAS')
    for i, x in enumerate(pistas, 1):
        A(f'  {i}. {x}')
    A('')
    desvios = ['R1, R7 e R8 não têm critério no registro; os critérios são meus, escritos no docstring antes de calcular.',
               'D3-2 rodou só em parte (bweb contra histórico, .sha512 e universo pela configuração em disco). O histórico não existia quando o desenho foi escrito; o critério do D3-2 foi levado a ele pela letra. Não rodaram o JSON oficial por município nem o aux.json.',
               'No 1º turno a conferência usou a base dados/ (extraída do bweb e conferida no Adendo 25) e não uma leitura nova dos zips; no 2º turno os zips foram lidos de novo.',
               'Cortes falsos do D3-6: o registro fala em vinte, mas a grade que ele mesmo descreve (de 5 em 5 minutos de 19:55 a 21:05) tem 15 pontos, e 12 depois de pular os que ficam a menos de 10 minutos de um corte registrado. Usei os 12 como principal e um conjunto de 20 (de 3 em 3 minutos) ao lado.',
               'Pausas do 1º turno: usei os limites vistos nos metadados (18:02 a 18:08, 18:50 a 18:53, 19:32 a 19:59); o desenho dizia 19:32 a 19:54.',
               'Zona = UF, município e zona: reproduz as 274 zonas do D3-5; no D3-6 dá 1.216 zonas com os dois lados da pausa (1.214 na conta), não as 1.255 do texto do desenho.',
               'Placebo (3) do D3-5: o registro diz "primeiras seções recebidas de cada zona contra as seguintes"; fixei antes de calcular os três primeiros minutos do recebimento do 1º turno (17:08 a 17:10) contra as seguintes da zona com emissão antes de 17:11. É essa escolha que leva o D3-5 a INCONCLUSIVO pela letra.',
               'Cláusulas "sinais opostos" e "muda de sinal entre bandas" lidas pela letra (sinal da estimativa, sem exigir significância), como escrito no docstring.',
               'Ordem de execução: o desenho pede plantios e placebos antes do dado real. O programa foi ensaiado inteiro com um 2º turno sorteado sem efeito de hora (os placebos, que não usam o 2º turno, saíram já nesse ensaio); depois o dado real rodou uma vez, sem mudança de estimador.',
               'Busca do R7 por conjuntos de UFs: escrita antes, mostrou-se sem poder (o acaso dá 5 conjuntos por número). Fica relatada como tal.',
               'No R1 o plantio de 1 voto a cada 100 s e a cada 1.000 s usa arredondamento sorteado (a parte inteira daria zero voto em quase toda seção); detalhe decidido no ensaio, antes do dado real.',
               'A conciliação passo a passo usa busca por trocas e, onde ela não acha, programação inteira (11 passos do 2º turno); nos plantios só a busca por trocas, com a mesma régua para a linha de base. A conciliação rodou três vezes por causa da busca (a primeira versão deixava 16 passos sem decidir, a segunda 11; a programação inteira decidiu todos); o fim de zona deu zero nas três. A primeira passada do 1º turno mostrou a diferença do 28, e a soma de nulos com o 28 foi acrescentada depois de vê-la. O R7 rodou duas vezes (a segunda só acrescentou o bloco exploratório).',
               'Exploratório: os contrastes com o comparecimento como desfecho e a leitura do theta contra o placebo foram feitos depois de ver os resultados.',
               'Contagem: esta peça tem 11 vereditos. Com limiar de p < 0,001 (e condições de tamanho), o acaso daria cerca de 0,01 sinal. Nenhum SINAL saiu.']
    A('DESVIOS E DECISÕES FORA DO REGISTRO')
    for i, x in enumerate(desvios, 1):
        A(f'  {i}. {x}')
    A('')
    A('Arquivos: scripts/analisar_R27_B5.py; resultados/R27_B5_janelas_da_totalizacao.json; parciais e docstring datado em /home/user/trabalho-eleicao/adendo27/R27_B5/.')
    txt = '\n'.join(T) + '\n'
    assert chr(8212) not in txt and chr(8211) not in txt, 'travessão no texto'
    with open(SAIDA_TXT, 'w') as fh:
        fh.write(txt)
    saida = dict(teste='R27_B5', nome='Janelas da totalização', registro=dict(adendo27='2748895', adendo28='938be19', docstring_gravado_em=doc[0], docstring_sha256=doc[1],
                                                                              grupos_congelados_sha256=SHA_GRUPOS),
                 vereditos=V, justificativas=J, resumo=resumo, margem=MARGEM, base=meta,
                 parte1_D3_5=d35, parte2_D3_6=d36, parte3_D3_2=dict(historico=hist, sha512=sha), parte4=dict(R1=r1, R7=r7, R8=r8), exploratorio=ex,
                 a_favor_da_tese=favor, contra_a_tese=contra, o_que_isso_significa=significa, pistas=pistas, desvios=desvios)
    with open(SAIDA_JSON, 'w') as fh:
        json.dump(saida, fh, ensure_ascii=False, indent=1, default=_jsonavel)
    print(txt)


# ==== PRINCIPAL
if __name__ == '__main__':
    _os.makedirs(TRAB, exist_ok=True)
    modo = sys.argv[1] if len(sys.argv) > 1 else ''
    fn = globals().get('modo_' + modo)
    if fn is None:
        print(__doc__.split('Uso:')[1].split('Trabalho e parciais')[0])
        sys.exit(1)
    fn(*sys.argv[2:])
