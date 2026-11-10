"""R27_B2: LIBERAÇÕES E MUDANÇAS NA SEÇÃO (testes D2-1 LIBERA e D2-6 TROCA de registro/adendo27/desenho_D2_proposta.json
e a parte (a) do D4-6 de registro/adendo27/desenho_D4_proposta.json).

Adendo 27 do pré-registro (commit 2748895, 10/11/2026 00:16:42 UTC), Onda B, item B2, na ordem do Adendo 28 (commit
938be19, 10/11/2026 04:36:33 UTC). Os critérios valem como escritos nos campos estatistica, criterio_sinal,
criterio_sem_sinal, poder e placebo de cada teste. Este docstring foi escrito ANTES de qualquer conta deste teste com
votos ou com os totais de liberação. O que ele decide e o registro não fixa está em DECISÕES e sai no resultado como
desvio. O que for feito depois de ver o resultado fica em funções com nome "exploratorio_" e sai marcado.

O QUE EU JÁ SABIA ANTES DE ESCREVER (contaminação declarada)
- Do Adendo 28 e da Onda A: comparecimento +2.960.239 entre os turnos; liberações manuais (QT_ELEI_BIOM_SEM_HABILITACAO
  do bweb) +290.239 no país; 55.722 seções com aptos diferentes entre os turnos; total de aptos difere em 30; urna
  diferente em 4.435 seções; A6 sem relação entre fração de liberação e virada (b = +0,16, ep 0,14); T21 (Adendo 16)
  inconclusivo porque faltava 2022. Ou seja: o tamanho bruto da sobra nacional de liberações já era conhecido em
  ordem de grandeza (dezenas a uma centena de milhar). Não eram conhecidos: a cauda (S2), o elo com o voto (S3), a
  razão de 2022, as contas por UF, o elo das bandeiras do D2-6, os coeficientes do D4-6(a).
- Só estrutura foi lida antes: cabeçalhos do bweb de 2022 e de 2026, formato de DS_SECOES_AGREGADAS, tipos do
  arquivo de locais (499.248 principais e 17.931 agregadas por turno), campos do log.

Uso (todos com python3 -I):
  scripts/analisar_R27_B2.py extrair    passada própria no bweb de 2026 (estrutura por seção, sem votos)
  scripts/analisar_R27_B2.py baixar2022 bweb de 2022 do CDN do TSE, lido em fluxo (estrutura por seção, sem votos)
  scripts/analisar_R27_B2.py locais     arquivo de locais de 2026 (cadastro de cada turno)
  scripts/analisar_R27_B2.py logs       eventos dos logs da amostra de 3.897 seções (contingência, reinício, tipo e hora)
  scripts/analisar_R27_B2.py rodar      monta as bases, roda tudo, grava resultados/R27_B2_liberacoes_e_mudancas.json e .txt
Trabalho e parciais: /home/user/trabalho-eleicao/adendo27/R27_B2/

ESCALA COMUM (registro): margem 4.430.191; 25% = 1.107.548; 10% = 443.019; comparecimento do 2º turno 128.236.074.
Voto inserido vale 1 na margem.

=========================== D2-1 LIBERA: O QUE O REGISTRO FIXA ===========================
Universo: seções com os dois turnos e a mesma chave, tipo Apurada, comparecimento de 50 ou mais nos dois turnos,
variação de aptos de no máximo 2, fora do exterior. H = QT_ELEI_BIOM_SEM_HABILITACAO, C = comparecimento.
S1 (nível): q = (soma H2/soma C2)/(soma H1/soma C1); E = soma H2 - q_ref x (soma H1/soma C1) x soma C2, com q_ref = q
  de 2022 (QT_ELEITORES_BIOMETRIA_NH). IC de 95% por reamostragem de municípios, 2.000 réplicas. Por UF e por urna
  igual ou diferente nos dois turnos.
S2 (cauda): e_i = H1_i x (C2_i/C1_i) x q_UF, q_UF = mediana na UF de (H2/C2)/(H1/C1) entre seções com H1 de 5 ou
  mais; d_i = 2 x (raiz(H2_i + 3/8) - raiz(e_i + 3/8)), padronizado pelo desvio robusto (1,4826 x MAD) em cinco
  faixas de e_i (menos de 5; 5 a 10; 10 a 20; 20 a 40; mais de 40). X+ = soma de (H2 - e) com z de 4 ou mais;
  X- = soma de (e - H2) com z de -4 ou menos; A = X+ - X-.
S3 (elo): efeito fixo de local, peso C1, erro por município: y = [(L2 - R2) - (L1 - R1)]/C1 sobre x = (H2 - H1)/C1,
  controlando (C2 - C1)/C1, O1/C1, (B1 + N1)/C1, L1/C1, H1/C1 e indicador de urna trocada. gama = coeficiente de x.
Q = max(E, A).
SINAL: Q de 1.107.548 ou mais com limite inferior do IC de 443.019 ou mais, E gama de 0,30 ou mais com limite
  inferior acima de 0,10, E placebo de 2022 com sobra proporcional menor que um terço da de 2026 e gama de 2022
  abaixo de 0,10.
SEM SINAL: limite superior do IC de E abaixo de 443.019 E A abaixo de 443.019 E limite superior de gama abaixo de
  0,10. INCONCLUSIVO: o resto; também se 2022 mostrar sobra parecida; também sem 2022.
Poder: plantar K votos em H2, C2 e L2: (a) uniforme (K = 1.107.548, sorteio binomial em todas as seções): E entre
  0,95K e 1,05K; (b) concentrado (o mesmo K em 5% das seções sorteadas): A de 0,9K ou mais e gama de 0,6 ou mais;
  (c) K = 443.019 nos dois desenhos.
Placebo: (1) 2022 com as mesmas S1, S2, S3; (2) cauda esquerda e turnos invertidos; (3) desfecho branco e nulo.
Achado local: lista das seções com z de 6 ou mais.

=========================== D2-6 TROCA: O QUE O REGISTRO FIXA ===========================
T1 (aptos): seções com apt2 diferente de apt1; soma de max(apt2 - apt1, 0); seções com comparecimento acima dos
  aptos; diferença entre QT_APTOS do boletim e a soma de QT_ELEITOR_ELEICAO_FEDERAL do arquivo de locais (agregadas
  somadas na principal) em cada turno; seções com comparecimento de 95% ou mais dos aptos por turno; referência de
  seções com aptos diferentes em 2014, 2018 e 2022.
T2 (urna): bandeiras no 2º turno: U (urna diferente da do 1º), CT (carga em 05/10/2026 ou depois), CD (carga em
  25/10/2026) e, na amostra de logs, CG (contingência ou reinício no log do dia). T3 (agregação): AG (seção com
  agregadas) e AM (conjunto de agregadas mudou entre os turnos, pelo bweb e pelo arquivo de locais).
  Para cada bandeira: teto = soma do comparecimento do 2º turno das seções marcadas; elo = regressão com efeito
  fixo de local, peso C1, erro por município, de y = [(L2 - R2) - (L1 - R1)]/C1 sobre a bandeira, controlando
  (C2 - C1)/C1, O1/C1, (B1 + N1)/C1 e L1/C1; V_b = gama_b x teto. Nível de teste por bandeira: 0,2%.
SINAL: alguma bandeira com V_b de 1.107.548 ou mais e limite inferior de 443.019 ou mais, com o gama da mesma
  bandeira em 2022 (disponível para U) menor que um terço; ou soma de max(apt2 - apt1, 0) de 443.019 ou mais sem
  explicação pelo arquivo de locais. Comparecimento acima dos aptos em qualquer seção é achado local imediato.
SEM SINAL: para cada bandeira, teto abaixo de 443.019 ou limite superior de V_b abaixo de 443.019; e soma de
  max(apt2 - apt1, 0) abaixo de 443.019. INCONCLUSIVO: V_b entre os limiares, ou 2022 com gama parecido.
Poder: nas seções U somar votos a L2 e C2 até 443.019 e depois 1.107.548; V_b dentro de 10% do plantado. Em T1,
  plantar 1 apto a mais em 1% das seções e conferir a contagem.
Placebo: U em 2022, 2018 e 2014; troca de urna do 1º turno (carga depois da cerimônia e antes de 04/10, ou
  contingência no log de 04/10) contra o voto do 1º turno em corte dentro do prédio; desfecho branco e nulo.

=========================== D4-6 (a): O QUE O REGISTRO FIXA ===========================
(a1) F = soma de (NB2 - NB1) - (soma NB1/soma comp1) x soma de (comp2 - comp1), NB = QT_ELEI_BIOM_SEM_HABILITACAO.
(a2) Por seção, efeito fixo de local, peso 1/aptos, erro por município: (L2 - L1) - (R2 - R1) sobre a variação de
  NB, a variação do comparecimento com biometria (variação de comp menos variação de NB), os votos de cada
  eliminado, B1 e N1. Estatística: mu (variação de NB) menos mu' (comparecimento com biometria).
(a3) SB = QT_ELEITORES - QT_ELEITORES_BIOMETRIA (perfil F15): coeficiente de SB na regressão da variação de
  comparecimento, controlando a abstenção do 1º turno, efeito fixo de local; votos implicados = coeficiente x soma SB.
(a4) Logs: habilitações não biométricas depois das 17h locais e sua parcela entre os votos tardios, por turno.
SINAL: F de 1,1 milhão ou mais (25%) com mu - mu' de 0,5 ou mais; ou votos implicados em (a3) de 1,1 milhão ou
  mais. SEM SINAL: F de até 0,44 milhão (10%), mu - mu' de até 0,2 e votos implicados em (a3) de até 0,44 milhão.
  INCONCLUSIVO: entre os limiares; ou parcela de eleitores sem biometria alta demais para o limite de (a3) informar.
Poder: somar votos a L2, comp e NB do 2º turno em 5% das seções sorteadas (1,1 milhão e 4,43 milhões): F devolve o
  total e mu - mu' sobe para perto de 1. Placebo: a mesma conta em 2022.

=========================== DECISÕES QUE O REGISTRO NÃO FIXA (tomadas antes de calcular) ===========================
BASE
B1. Estrutura por seção (local, tipo, aptos, comparecimento, H, urna, cargas, data de carga, agregadas) vem de uma
    passada própria nos zips do bweb dos dois turnos (modo extrair), conferida campo a campo contra a extração dos
    desenhistas (desenho_D1/estrutura_1t e 2t) e contra dados/secoes2026.json.gz (aptos, comparecimento, urna,
    local). Votos: dados/secoes2026.json.gz e dados/candidatos2026_1t.json.gz.
B2. Chave do local = UF, município, zona e local do 2º turno (lib.chave_local com o bloco do 2º turno). Local com uma
    única seção no universo não informa a regressão (como em lib.fe_ols). Município = UF mais código.
B3. Erro por município: lib.fe_ols agrupa o erro pelo mesmo grupo do efeito fixo; uso função própria (reg_fe) com a
    mesma fórmula CR1 e o município como agrupamento, conferida contra lib.fe_ols com agrupamento por local.
B4. 2022: H de 2022 = QT_ELEITORES_BIOMETRIA_NH, primeira linha de Presidente por seção, lido em fluxo do CDN do
    TSE (modo baixar2022; nada além de estrutura é guardado); votos de dados/secoes2022.json.gz (L = 13, R = 22). O
    universo de 2022 usa a mesma regra do de 2026 (tipo APURADA). Se faltar alguma UF de 2022, q_ref sai das UFs
    disponíveis e isso é dito; sem nenhuma, q_ref = 1 e o D2-1 fica INCONCLUSIVO pela letra.
B5. Semente 20261110 em todos os sorteios.

D2-1
L1. Intervalos. A letra pede IC de 95% (percentis 2,5 e 97,5 das 2.000 réplicas). O desenhista também escreveu
    "usar nível de 1% na estatística primária": o IC de 99% sai ao lado e o veredito diz se mudaria com ele. Para E
    com q_ref de 2022, a réplica reamostra os mesmos municípios nos dois anos (q_ref reestimado em cada réplica),
    porque q_ref é estimativa; o IC com q_ref fixo sai ao lado. Para A, a classificação das seções (q_UF, escalas,
    z) fica fixa e reamostram-se as contribuições dos municípios. IC de Q = percentis de max(E*, A*). Para gama:
    gama mais ou menos 1,96 erro-padrão (95%) e 2,5758 (99%).
L2. S2: z_i = (d_i - mediana de d na faixa)/(1,4826 x MAD na faixa), MAD em torno da mediana, faixas nacionais
    [0;5), [5;10), [10;20), [20;40), [40; infinito). A versão sem centrar (z = d/escala) sai ao lado e não decide.
    Seção com H1 = 0 tem e = 0 e entra na primeira faixa.
L3. Por UF, q_ref é o q de 2022 da própria UF (ao lado, o q_ref nacional). Por urna igual ou diferente, q_ref é o
    do mesmo estrato em 2022. O IC por UF usa as mesmas réplicas nacionais restritas aos municípios da UF (o DF tem
    um município só e fica sem IC).
L4. "Sobra proporcional" de um ano = E com q_ref = 1 dividido pela soma de C2 do ano, isto é, (q - 1) x soma H1/soma
    C1. Placebo de 2022 limpo = sobra proporcional de 2022 menor que um terço da de 2026 (com a de 2026 positiva).
L5. "Sobra parecida em 2022" (cláusula de INCONCLUSIVO): sobra proporcional de 2022 de um terço ou mais da de 2026
    E limite superior do IC de 95% do E bruto de 2026 (q_ref = 1, sem outro ano) de 443.019 ou mais. Se o E bruto
    de 2026 não alcança 10% da margem nem sem descontar nada, não há deriva a explicar e a cláusula não se aplica.
    Ordem do veredito: SEM PODER (L8); SINAL; INCONCLUSIVO pela cláusula; SEM SINAL; INCONCLUSIVO no resto. O
    resultado diz se o SEM SINAL vale também com q_ref = 1 (só 2026) ou se depende de 2022.
L6. Valor bruto de 2026 ao lado de tudo: q, E com q_ref = 1 (igual, por álgebra, ao F do D4-6 no mesmo universo),
    X+, X-, gama. A comparação com 2022 entra em E (q_ref) e nas condições de placebo, e isso é dito.
L7. Plantios (20 repetições cada, nas tabelas de análise). k_i = votos plantados na seção i.
    Uniforme: k ~ multinomial(K, C2_i/soma C2) em todas as seções do universo. Concentrado: 5% das seções do
    universo por sorteio simples e k ~ multinomial(K, C2_i/soma C2 das sorteadas). K = 1.107.548 e 443.019.
    Irregularidade (letra): H2, C2 e L2 somam k.
    Explicações inocentes plantadas, para medir se o teste distingue:
      I1 "eleitor real que entrou": C2 e L2 somam k (todos em Lula, o caso mais parecido com inserção no voto) e
         H2 soma binomial(k, H1_i/C1_i), isto é, passa na biometria na taxa da própria seção.
      I2 "leitor pior no 2º turno": H2 soma k (limitado a C2 - H2), sem mexer em comparecimento nem em voto.
      I3 "abstenção pura": k eleitores de Flávio saem (R2 e C2 perdem k, k limitado a R2; H2 perde
         binomial(k, H2_i/C2_i)). É a forma do indício da Onda A; o teste não deve acusá-la como liberação.
    Medidas: variação de E, de A e de gama sobre o observado, média e extremos das repetições.
L8. Regra de SEM PODER (o registro pede a calibração e não diz como decide). S1 enxerga se o plantio uniforme de
    443.019 e de 1.107.548 sobe E em 0,90K ou mais (o registro espera 0,95K a 1,05K; pela fórmula o esperado é
    K x (1 - q_ref x soma H1/soma C1), porque voto inserido também aumenta C2, e isso é dito) e se a meia largura do
    IC de 95% de E for menor que 443.019. S2 enxerga se o plantio concentrado de 1.107.548 sobe A em 0,90K ou mais.
    S3 enxerga se o mesmo plantio leva gama a 0,6 ou mais. Veredito SEM PODER para o D2-1 se S1 não enxergar, ou se
    nem S2 nem S3 enxergarem. Se só um de S2 e S3 falhar, o veredito segue a letra e o texto diz o que ficou cego.
L9. Espelhos: (i) X- ao lado de X+; (ii) turnos invertidos: as mesmas S1, S2 e S3 trocando os índices 1 e 2 (E' com
    q_ref' = 1/q_ref; y' = [(L1 - R1) - (L2 - R2)]/C2 sobre (H1 - H2)/C2 com os controles do 2º turno; coluna sem
    variação é retirada); (iii) por candidato: a regressão S3 com y_L = (L2 - L1)/C1 e com y_R = (R2 - R1)/C1 em
    separado (gama = gama_L - gama_R; liberação a mais que favorece Flávio daria gama negativo, e o critério é lido
    igual no sentido contrário); (iv) desfecho placebo y_BN = [(B2 + N2) - (B1 + N1)]/C1.
L10. Complementos fixados antes, que não decidem: (i) S1 e S3 nas cinco UFs do indício da Onda A (PI, MA, TO, PB,
    CE) e no resto; (ii) S3 com perfil da seção (frações de 60 a 69, de 70 ou mais e de eleitores sem biometria no
    cadastro, do F15), para a explicação inocente da idade; (iii) "cauda e voto": regressão de y, com os controles
    de S3 menos x, sobre os indicadores z de 4 ou mais e z de -4 ou menos; (iv) inclinação de (H2 - H1) em
    (C2 - C1) dentro do local, em votos, ao lado da fatia H1/C1; (v) S3 por região.
L11. Achado local: seções com z de 6 ou mais (lista com chave, H1, C1, H2, C2, e, z, variação da margem); o JSON
    traz as 300 de maior z e a contagem total; a lista inteira fica em secoes_z6.csv na pasta de trabalho.

D4-6 (a)
F1. (a1) "nacional": todas as seções pareadas pela chave nos dois turnos, 27 UFs mais exterior (a seção que só
    existe no 1º turno fica fora e é contada). Ao lado: só 27 UFs; e o universo do D2-1 (onde F = E com q_ref = 1).
    IC de 95% por reamostragem de municípios (2.000). Limiar exato: 1.107.548 e 443.019.
F2. (a2) e (a3) usam o universo do D4-1 (mesmo desenho): seções apuradas nos dois turnos, variação de aptos de no
    máximo 2, comparecimento do 1º turno de 30 ou mais, fora do exterior, locais com 2 ou mais seções válidas.
    Peso = 1/aptos do 1º turno. Contas em votos (níveis). "Votos de cada eliminado" = um termo para cada candidato
    eliminado com 0,5% ou mais dos votos nominais nacionais do 1º turno e os demais somados (O1 menos os termos
    individuais, inclui o candidato anulado), como no D4-1. mu - mu' e seu erro saem da reparametrização
    y = (mu - mu') x dNB + mu' x dC + ..., com dC = C2 - C1.
F3. (a3) SB por seção do perfil F15 (cadastro de julho; extração sem votos do A6, conferida pelo total), somando as
    agregadas do 2º turno na principal. Regressão de (C2 - C1) sobre SB e A1 = aptos do 1º turno menos C1, efeito
    fixo de local, peso 1/aptos, erro por município. Votos implicados = coeficiente x soma nacional de SB (27 UFs,
    seções com perfil). "(a3) não informa" se 1,96 x erro x soma SB for de 443.019 ou mais.
F4. Veredito pela letra com as estimativas pontuais; o IC de 95% sai ao lado e o texto diz se ele cruza o limiar.
    Regra de poder: (a2) enxerga se o plantio concentrado de 1.107.548 levar mu - mu' a 0,5 ou mais; (a1) enxerga se
    devolver 0,90K ou mais. Sem isso, SEM PODER. Ordem: SEM PODER; SINAL; SEM SINAL; INCONCLUSIVO.
F5. Plantios (20 repetições): a letra (5% das seções sorteadas no universo do D4-1, k ~ multinomial(K, C2), somado
    a L2, C2 e NB2; K = 1.107.548 e 4.430.191). Inocentes: I1 (eleitor real: C2 e L2 somam k, NB2 soma
    binomial(k, NB1/C1)) e I3 (abstenção pura de eleitores de Flávio, como em L7). Espelho: o plantio da letra em R2
    (a favor de Flávio), que deve dar mu - mu' de sinal contrário; e a regressão com (L2 - L1) e (R2 - R1) em separado.
    Emenda feita às 04h58 UTC de 10/11, depois do primeiro congelamento do docstring e ANTES de qualquer conta
    (as bases ainda não tinham sido montadas): plantio do (a3), que o registro não descreve: C2 soma
    binomial(SB_i, phi), phi = 1.107.548/soma de SB do universo, sem voto; o coeficiente de SB deve subir phi.
    (a3) enxerga se o coeficiente subir 0,8 phi ou mais; senão o (a3) fica SEM PODER e não decide.
F6. Placebo de 2022: (a1) e (a2) com H de 2022 e secoes2022 (eliminados somados em O1, porque a base de 2022 não
    traz cada um); ao lado, 2026 na mesma versão com eliminados somados.
F7. (a4) Amostra de 3.897 logs (não aleatória; sem extrapolar): por seção e turno, habilitações com voto computado
    depois das 17h00m00 locais, quantas sem biometria (liberação pelo mesário ou eleitor sem biometria) e a parcela;
    totais por turno, diferença entre turnos com erro por reamostragem de locais (2.000). Só descritivo.

D2-6
T1. Contagens de T1 em todas as seções pareadas (27 UFs mais exterior, e só 27 UFs). Espelho: soma de
    max(apt1 - apt2, 0). "Explicada pelo arquivo de locais" = seção em que QT_APTOS do boletim é igual à soma de
    QT_ELEITOR_ELEICAO_FEDERAL (principal mais agregadas do turno) nos dois turnos: a variação está no cadastro de
    cada turno publicado pelo TSE. Soma "sem explicação" = soma de max(apt2 - apt1, 0) nas demais. Limite dito
    antes: isso mostra que o boletim segue o cadastro do turno, não por que o cadastro mudou.
T2. Universo do elo (o registro não diz): seções pareadas das 27 UFs, tipo Apurada, comparecimento de 50 ou mais
    nos dois turnos; SEM o filtro de aptos (mudança de aptos é objeto do teste). Sensibilidade com o filtro. O teto
    soma o comparecimento do 2º turno de TODAS as seções marcadas das 27 UFs (com exterior ao lado).
T3. Bandeiras: U = NR_URNA_EFETIVADA diferente entre os turnos; CT = data de DT_CARGA_URNA_EFETIVADA do 2º turno em
    05/10/2026 ou depois; CD = essa data igual a 25/10/2026; AG = DS_SECOES_AGREGADAS do 2º turno preenchido; AM =
    conjunto de agregadas diferente entre os turnos pelo bweb OU pelo arquivo de locais (as duas fontes contadas em
    separado). Uma regressão por bandeira. IC de V_b ao nível de 0,2%: (gama_b mais ou menos 3,0902 erro) x teto;
    o IC de 95% sai ao lado. Bandeira sem variação dentro de nenhum local fica sem estimativa e isso é dito.
T4. CG (amostra de logs, sem extrapolar): no log do dia 25/10/2026, linha de "Modo de carga da UE - Urna de
    contingência" ou "Contingência executada", OU aplicativo VOTA iniciado 2 ou mais vezes no dia, OU evento SCUE de
    data e hora no dia, OU mais de uma urna no log do dia. Teto e elo só dentro da amostra.
T5. Placebos: U em 2022, 2018 e 2014 com a mesma regressão (H não entra). Troca do 1º turno em 2026: bandeira C1T =
    data de carga da urna do 1º turno posterior ao último dia em que a zona carregou 5% ou mais das suas urnas do 1º
    turno ("cerimônia" da zona) e até 04/10/2026; corte dentro do prédio: (L1 - R1)/C1 sobre C1T, efeito fixo de
    local, peso C1, erro por município, sem controles; na amostra, contingência ou reinício no log de 04/10.
    Desfecho placebo: y_BN = [(B2 + N2) - (B1 + N1)]/C1 em cada bandeira. Espelho: y_L = (L2 - L1)/C1 e
    y_R = (R2 - R1)/C1 em separado em cada bandeira; o critério é lido igual no sentido de Flávio (V_b negativo).
T6. "gama de 2022 menor que um terço" = |gama_U de 2022| menor que |gama_U de 2026|/3. "2022 com gama parecido" =
    o contrário, quando V_U de 2026 estiver entre os limiares ou acima.
T7. Plantios (20 repetições): para cada bandeira com teto de 443.019 ou mais, k ~ multinomial(K, C2) entre as seções
    marcadas das 27 UFs, somado a L2 e C2, K = 443.019 e 1.107.548 (se K passar do teto, usa-se o teto e isso é
    dito). Recuperação rho_b = (V_b plantado - V_b observado)/K. Inocente: os mesmos k como eleitores reais que
    dividem o voto como a seção no 2º turno (L2 soma binomial(k, L2/(L2 + R2)), R2 o resto, C2 soma k).
    T1: plantar 1 apto a mais em 1% das seções e conferir contagem e soma.
T8. Regra de poder e cautela: a bandeira enxerga K se rho_b for de 0,5 ou mais e o efeito plantado de 443.019 passar
    da meia largura do IC de 0,2% de V_b. Sem isso, a bandeira com teto de 443.019 ou mais fica SEM PODER. Se rho_b
    ficar entre 0,5 e 0,9, o SEM SINAL exige também limite superior de V_b dividido por rho_b abaixo de 443.019
    (desvio da letra no sentido da cautela); senão, INCONCLUSIVO.
T9. Complementos fixados antes, que não decidem: bandeiras AP+ (apt2 maior que apt1) e AP- (apt2 menor que apt1) e a
    dose (apt2 - apt1)/C1 no mesmo elo; modelo da urna do 2º turno (scripts/modelos.py) como controle na bandeira U;
    U por UF; seções com comparecimento acima dos aptos listadas.
T10. Veredito do D2-6: SINAL se alguma bandeira ou T1 cumprir o critério; SEM PODER se alguma bandeira com teto de
    443.019 ou mais não enxergar e nenhuma der sinal; SEM SINAL se todas as cinco bandeiras e T1 cumprirem o
    critério; INCONCLUSIVO no resto. CG entra só como relato da amostra.

GERAIS
G1. Tradução em votos de margem: E, A, F e votos implicados valem 1 por 1; V_b já está em votos de margem.
G2. O resultado conta quantas estatísticas com limiar rodaram e quantos sinais o acaso daria.
"""
# NOTA POSTERIOR AO DOCSTRING (o docstring acima não foi tocado depois da emenda das 04h58 UTC):
# 1. Antes da rodada final houve um ensaio com poucas réplicas (B2_TESTE=1) para achar erro de código. Dois erros
#    corrigidos, sem mexer em critério: percentil de vetor vazio (UF de 2022 ainda não baixada) e erro agrupado com um
#    município só (DF na conta da bandeira U por UF).
# 2. Depois de ver o ensaio foram acrescentados, só como relato: o rótulo "pela letra do registro sem a regra de
#    poder" (as regras L8 e F4 são decisões minhas e saíram mais duras do que o registro), rho com o teto de antes do
#    plantio, e as funções exploratorio_ (efeito fixo de zona, município e UF; correlações por UF; leitura calibrada;
#    lista das seções com carga no dia). Nada disso entra em veredito.
import sys, os, gzip, json, zipfile, io, csv, re, glob, time, struct, zlib, collections, hashlib
import numpy as np

RAIZ = '/home/user/casa-control/eleicao-2026'
DADOS = RAIZ + '/dados'
TRAB = '/home/user/trabalho-eleicao/adendo27/R27_B2'
D1DIR = '/home/user/trabalho-eleicao/adendo27/desenho_D1'
PERFIL_A6 = '/home/user/trabalho-eleicao/adendo27/R27_A6/perfil_secao_2026_A6.json.gz'
LOCAIS_ZIP = '/home/user/trabalho-eleicao/adendo21/F14_dl_locais/eleitorado_local_votacao_2026.zip'
ZIPS = {'1': '/home/user/trabalho-eleicao/bweb1t/zips/*.zip', '2': '/home/user/trabalho-eleicao/trab2t/zips2t/*.zip'}
LOGS = '/home/user/trabalho-eleicao/amostra2t/arq'
SAIDA_JSON = RAIZ + '/resultados/R27_B2_liberacoes_e_mudancas.json'
SAIDA_TXT = RAIZ + '/resultados/R27_B2_liberacoes_e_mudancas.txt'
sys.path.insert(0, RAIZ + '/scripts')
from lib import carregar, fe_ols  # noqa: E402
from modelos import modelo as modelo_urna  # noqa: E402

SEMENTE = 20261110
NBOOT = 2000
NREP = 20
MARGEM = 4430191
LIM25 = 1107548
LIM10 = 443019
COMP2T = 128236074
Z95, Z99, Z998 = 1.959963985, 2.5758293035, 3.0902323062
UFS = 'AC AL AM AP BA CE DF ES GO MA MG MS MT PA PB PE PI PR RJ RN RO RR RS SC SE SP TO'.split()
UF5 = ['PI', 'MA', 'TO', 'PB', 'CE']
REGIOES = {'Norte': ['AC', 'AM', 'AP', 'PA', 'RO', 'RR', 'TO'],
           'Nordeste': ['AL', 'BA', 'CE', 'MA', 'PB', 'PE', 'PI', 'RN', 'SE'],
           'Sudeste': ['ES', 'MG', 'RJ', 'SP'], 'Sul': ['PR', 'RS', 'SC'], 'Centro-Oeste': ['DF', 'GO', 'MS', 'MT']}
CAMPOS_BWEB = ['NR_LOCAL_VOTACAO', 'DS_TIPO_URNA', 'QT_APTOS', 'QT_COMPARECIMENTO', 'QT_ELEI_BIOM_SEM_HABILITACAO',
               'NR_URNA_EFETIVADA', 'CD_CARGA_1_URNA_EFETIVADA', 'CD_CARGA_2_URNA_EFETIVADA',
               'CD_FLASHCARD_URNA_EFETIVADA', 'DT_CARGA_URNA_EFETIVADA', 'DS_SECOES_AGREGADAS', 'DT_ABERTURA',
               'DT_ENCERRAMENTO', 'CD_TIPO_URNA', 'NR_JUNTA_APURADORA']


def grava(nome, obj):
    """Parcial em disco (o container pode reiniciar)."""
    with open(f'{TRAB}/{nome}.tmp', 'w') as f:
        json.dump(obj, f, ensure_ascii=False, indent=1, default=_jsonavel)
    os.replace(f'{TRAB}/{nome}.tmp', f'{TRAB}/{nome}')


def sem_nan(o):
    """JSON estrito: NaN e infinito viram null."""
    if isinstance(o, dict): return {k: sem_nan(v) for k, v in o.items()}
    if isinstance(o, (list, tuple)): return [sem_nan(v) for v in o]
    if isinstance(o, (float, np.floating)): return float(o) if np.isfinite(o) else None
    if isinstance(o, np.integer): return int(o)
    if isinstance(o, np.bool_): return bool(o)
    if isinstance(o, np.ndarray): return sem_nan(o.tolist())
    return o


def _jsonavel(o):
    if isinstance(o, (np.integer,)): return int(o)
    if isinstance(o, (np.floating,)): return float(o)
    if isinstance(o, np.ndarray): return o.tolist()
    if isinstance(o, (set, frozenset)): return sorted(o)
    raise TypeError(str(type(o)))


# ----------------------------------------------------------------------------------------------------------------
# EXTRAÇÕES SEM VOTOS
# ----------------------------------------------------------------------------------------------------------------
MARCA_PRES = b';1;"Presidente";'


def _bweb_um_zip(zp):
    z = zipfile.ZipFile(zp); nome = [n for n in z.namelist() if n.lower().endswith('.csv')][0]
    out = {}; resto = b''; ix = None; nl = 0
    with z.open(nome) as fh:
        while True:
            b = fh.read(1 << 22)
            if not b: break
            dados = resto + b
            c = dados.rfind(b'\n')
            if c < 0: resto = dados; continue
            bloco, resto = dados[:c], dados[c + 1:]
            if ix is None:
                c0 = bloco.find(b'\n')
                cab = bloco[:c0].decode('latin1').strip().replace('"', '').replace('SG_ UF', 'SG_UF').split(';')
                ix = {x: j for j, x in enumerate(cab)}; bloco = bloco[c0 + 1:]
                iU, iM, iZ, iS, iC = ix['SG_UF'], ix['CD_MUNICIPIO'], ix['NR_ZONA'], ix['NR_SECAO'], ix['CD_CARGO_PERGUNTA']
                cols = [ix[x] for x in CAMPOS_BWEB]
            pos = 0
            while True:
                j = bloco.find(MARCA_PRES, pos)
                if j < 0: break
                a = bloco.rfind(b'\n', 0, j) + 1
                e = bloco.find(b'\n', j)
                if e < 0: e = len(bloco)
                pos = e + 1; nl += 1
                f = bloco[a:e].decode('latin1').rstrip('\r').split(';')
                if f[iC] != '1': continue
                k = f'{f[iU].strip(chr(34))}|{int(f[iM])}|{int(f[iZ])}|{int(f[iS])}'
                if k not in out: out[k] = [f[c].strip('"') for c in cols]
    return zp.split('/')[-1], out, nl


def extrair():
    """Passada própria no bweb de 2026: uma linha de estrutura por seção (primeira do cargo 1). Sem votos."""
    from multiprocessing import Pool
    for turno in ('2', '1'):
        zips = sorted(glob.glob(ZIPS[turno]), key=lambda p: -zipfile.ZipFile(p).infolist()[0].file_size)
        tudo = {}
        with Pool(3) as p:
            for nome, o, nl in p.imap_unordered(_bweb_um_zip, zips):
                tudo.update(o); print(nome, len(o), nl, flush=True)
        with gzip.open(f'{TRAB}/est2026_{turno}t.json.gz', 'wt') as f:
            json.dump({'campos': CAMPOS_BWEB, 'secoes': tudo}, f, separators=(',', ':'))
        print('turno', turno, 'secoes', len(tudo), flush=True)


BASE22 = 'https://cdn.tse.jus.br/estatistica/sead/eleicoes/eleicoes2022/buweb/'
SUF22 = {1: '051020221321', 2: '311020221535'}
COLS22 = ('NR_LOCAL_VOTACAO', 'DS_TIPO_URNA', 'QT_APTOS', 'QT_COMPARECIMENTO', 'QT_ELEITORES_BIOMETRIA_NH',
          'NR_URNA_EFETIVADA', 'DT_CARGA_URNA_EFETIVADA', 'DS_AGREGADAS', 'DT_ABERTURA', 'DT_ENCERRAMENTO', 'CD_TIPO_URNA')


def baixar2022(pasta=None):
    """bweb de 2022 em fluxo (sem gravar o zip): 3 pedidos por arquivo, 1,2 s entre pedidos, para em 429/403/407."""
    import ssl, urllib.request, urllib.error
    pasta = pasta or f'{TRAB}/dl_bweb2022'; os.makedirs(pasta, exist_ok=True)
    ctx = ssl.create_default_context(cafile='/root/.ccr/ca-bundle.crt')
    ua = {'User-Agent': 'pesquisa-dados-abertos'}; ult = [0.0]

    def abrir(url, extra=None, metodo='GET'):
        d = 1.2 - (time.time() - ult[0])
        if d > 0: time.sleep(d)
        ult[0] = time.time()
        req = urllib.request.Request(url, method=metodo, headers=dict(ua, **(extra or {})))
        try:
            return urllib.request.urlopen(req, timeout=120, context=ctx)
        except urllib.error.HTTPError as e:
            if e.code in (429, 403, 407):
                print('PARADA: resposta', e.code, 'em', url, flush=True); sys.exit(3)
            raise

    def processa(uf, turno, saida):
        url = f'{BASE22}bweb_{turno}t_{uf}_{SUF22[turno]}.zip'
        with abrir(url, metodo='HEAD') as r: n = int(r.headers['Content-Length'])
        with abrir(url, {'Range': f'bytes={max(0, n - 65536)}-{n - 1}'}) as r: cauda = r.read()
        i = cauda.rfind(b'PK\x05\x06'); tot, cdsz, cdoff = struct.unpack('<HII', cauda[i + 10:i + 20])
        cd = cauda[len(cauda) - (n - cdoff):][:cdsz]; p = 0; alvo = None
        while p < len(cd) and cd[p:p + 4] == b'PK\x01\x02':
            metodo, = struct.unpack('<H', cd[p + 10:p + 12]); csz, usz = struct.unpack('<II', cd[p + 20:p + 28])
            fl, el, cl = struct.unpack('<HHH', cd[p + 28:p + 34]); off, = struct.unpack('<I', cd[p + 42:p + 46])
            nome = cd[p + 46:p + 46 + fl].decode('latin1'); p += 46 + fl + el + cl
            if nome.lower().endswith('.csv'): alvo = (off, csz, usz, metodo)
        off, csz, usz, metodo = alvo
        assert metodo == 8 and csz < 0xFFFFFFFF
        out = {}; ix = None; resto = b''; nlin = 0; dec = zlib.decompressobj(-15)
        with abrir(url, {'Range': f'bytes={off}-{min(off + 630 + csz, n - 1)}'}) as r:
            cab = r.read(30); fl, el = struct.unpack('<HH', cab[26:30]); r.read(fl + el)
            falta = csz
            while falta > 0:
                b = r.read(min(1 << 20, falta))
                if not b: raise IOError('fluxo cortado')
                falta -= len(b)
                dados = resto + dec.decompress(b)
                c = dados.rfind(b'\n')
                if c < 0: resto = dados; continue
                bloco, resto = dados[:c], dados[c + 1:]
                if ix is None:
                    c0 = bloco.find(b'\n'); cabec = bloco[:c0].decode('latin1').strip().replace('"', '').split(';')
                    ix = {x: j for j, x in enumerate(cabec)}; bloco = bloco[c0 + 1:]
                    iM, iZ, iS = ix['CD_MUNICIPIO'], ix['NR_ZONA'], ix['NR_SECAO']
                    cols = [ix[x] for x in COLS22]
                    assert ix['CD_CARGO_PERGUNTA'] == 16 and ix['DS_CARGO_PERGUNTA'] == 17
                pos = 0
                while True:
                    j = bloco.find(b';"1";"Presidente";', pos)
                    if j < 0: break
                    a = bloco.rfind(b'\n', 0, j) + 1
                    e = bloco.find(b'\n', j)
                    if e < 0: e = len(bloco)
                    f = [x.strip('"') for x in bloco[a:e].decode('latin1').rstrip('\r').split(';')]
                    pos = e + 1; nlin += 1
                    if f[16] != '1': continue
                    k = f'{uf}|{int(f[iM])}|{int(f[iZ])}|{int(f[iS])}'
                    if k not in out: out[k] = [f[c] for c in cols]
        with gzip.open(saida + '.tmp', 'wt') as fo:
            json.dump(out, fo, separators=(',', ':'))
        os.replace(saida + '.tmp', saida)
        return n, usz, len(out), nlin

    for uf, t in [(u, 2) for u in UFS] + [(u, 1) for u in UFS]:
        saida = f'{pasta}/est2022_{t}t_{uf}.json.gz'
        if os.path.exists(saida): continue
        t0 = time.time()
        for tent in range(3):
            try:
                n, usz, ns, nl = processa(uf, t, saida); break
            except SystemExit: raise
            except Exception as e:
                print('erro', uf, t, type(e).__name__, e, 'tentativa', tent + 1, flush=True); time.sleep(20)
        else:
            print('FALHOU', uf, t, flush=True); continue
        print(f'ok {uf} {t}t zip {n} csv {usz} secoes {ns} linhas_pres {nl} {time.time() - t0:.0f}s', flush=True)
    print('FIM', flush=True)


def locais():
    """Arquivo de locais de 2026 (cadastro de cada turno; sem votos)."""
    z = zipfile.ZipFile(LOCAIS_ZIP); out = {'1': {}, '2': {}}
    for nome in sorted(z.namelist()):
        if not nome.lower().endswith('.csv') or 'BRASIL' in nome: continue
        with z.open(nome) as fh:
            rd = csv.reader(io.TextIOWrapper(fh, encoding='latin1', newline=''), delimiter=';')
            cab = next(rd); ix = {c: i for i, c in enumerate(cab)}
            for r in rd:
                k = f"{r[ix['SG_UF']]}|{int(r[ix['CD_MUNICIPIO']])}|{int(r[ix['NR_ZONA']])}|{int(r[ix['NR_SECAO']])}"
                out[r[ix['NR_TURNO']]][k] = [int(r[ix['CD_TIPO_SECAO_AGREGADA']]), int(r[ix['NR_SECAO_PRINCIPAL']]),
                                             int(r[ix['NR_LOCAL_VOTACAO']]), int(r[ix['QT_ELEITOR_ELEICAO_FEDERAL']]),
                                             int(r[ix['QT_ELEITOR_SECAO']])]
    with gzip.open(f'{TRAB}/locais2026.json.gz', 'wt') as f:
        json.dump({'campos': ['tipo_agr', 'principal', 'local', 'fed', 'secao'], 'turnos': out}, f, separators=(',', ':'))
    print('locais', len(out['1']), len(out['2']))


DIAS_LOG = {'04/10/2026': '1', '25/10/2026': '2'}


def _log_um(p):
    """Eventos de um log (sem voto por candidato): por dia, habilitações (segundo, classe B/M/S, voto computado),
    contingência, inícios do VOTA, eventos SCUE de data e hora, urnas vistas."""
    partes = p.split('/')
    chave = f"{partes[-5].upper()}|{int(partes[-4])}|{int(partes[-3])}|{int(partes[-2])}"
    res = {}
    try:
        z = zipfile.ZipFile(p); blocos = []
        for n in z.namelist():
            if n.startswith('logd'):
                blocos.append(z.read(n).decode('latin1').splitlines())
            elif n.endswith('.jez'):
                try:
                    zz = zipfile.ZipFile(io.BytesIO(z.read(n)))
                    for m in zz.namelist():
                        if m.startswith('logd'): blocos.append(zz.read(m).decode('latin1').splitlines())
                except zipfile.BadZipFile:
                    pass
    except Exception as e:
        return chave, {'erro': str(e)}
    for linhas in blocos:
        cur = {'bio': False, 'man': False}; aberto = None
        for l in linhas:
            q = l.split('\t')
            if len(q) < 5: continue
            d = DIAS_LOG.get(q[0][:10])
            if d is None: continue
            r = res.setdefault(d, {'hab': [], 'cont': 0, 'ini_vota': 0, 'scue_hora': 0, 'urnas': set(), 'comp_sem_hab': 0})
            try: t = int(q[0][11:13]) * 3600 + int(q[0][14:16]) * 60 + int(q[0][17:19])
            except ValueError: continue
            app, m = q[3], q[4]
            r['urnas'].add(q[2])
            if app == 'SCUE' and m.startswith('Data e hora'): r['scue_hora'] += 1
            if m.startswith('Modo de carga da UE - Urna de contingência') or m.startswith('Contingência executada'): r['cont'] += 1
            if app != 'VOTA': continue
            if m.startswith('Iniciando aplicação'): r['ini_vota'] += 1
            elif m == 'Aguardando digitação do identificador do eleitor': cur = {'bio': False, 'man': False}
            elif m.startswith('Tipo de habilitação do eleitor [biom'): cur['bio'] = True
            elif m.startswith('Solicitação de dado pessoal do eleitor para habilitação manual') or m == 'Solicita digital do mesário' \
                    or (m.startswith('Mesário') and m.endswith('habilitou o eleitor')): cur['man'] = True
            elif m == 'Eleitor foi habilitado':
                aberto = [t, 'B' if cur['bio'] else ('M' if cur['man'] else 'S'), 0]
                r['hab'].append(aberto); cur = {'bio': False, 'man': False}
            elif m == 'O voto do eleitor foi computado':
                if aberto is None: r['comp_sem_hab'] += 1
                else: aberto[2] = 1
                aberto = None
    for d in res: res[d]['urnas'] = sorted(res[d]['urnas'])
    return chave, res


def logs():
    from multiprocessing import Pool
    arqs = sorted(glob.glob(LOGS + '/*/*/*/*/*-log.jez'))
    out = {}
    with Pool(3) as p:
        for i, (k, o) in enumerate(p.imap_unordered(_log_um, arqs, chunksize=16)):
            out[k] = o
            if i % 500 == 0: print(i, flush=True)
    with gzip.open(f'{TRAB}/logs_B2.json.gz', 'wt') as f:
        json.dump(out, f, separators=(',', ':'))
    print('logs', len(arqs), 'secoes', len(out))



# ----------------------------------------------------------------------------------------------------------------
# BASES (aqui entram os votos)
# ----------------------------------------------------------------------------------------------------------------
def _agr(s):
    return tuple(sorted(int(x) for x in re.findall(r'\d+', s))) if s and s != '#NULO#' else ()


def _data(s):
    return int(s[:4] + s[5:7] + s[8:10]) if len(s) >= 10 and s[4] == '-' else 0


def _cod(a):
    u, inv = np.unique(a, return_inverse=True)
    return inv.astype(np.int64), u


def montar_2026():
    """Base de 2026 por seção pareada (27 UFs e exterior): estrutura da passada própria no bweb, votos das bases."""
    e1 = json.load(gzip.open(f'{TRAB}/est2026_1t.json.gz', 'rt'))['secoes']
    e2 = json.load(gzip.open(f'{TRAB}/est2026_2t.json.gz', 'rt'))['secoes']
    sec = carregar(DADOS + '/secoes2026.json.gz')
    conf = collections.Counter()
    for t, e in (('1', e1), ('2', e2)):
        d = json.load(gzip.open(f'{D1DIR}/estrutura_{t}t.json.gz', 'rt'))
        conf[f'secoes_{t}t_passada_propria'] = len(e); conf[f'secoes_{t}t_desenhista'] = len(d)
        dif = falta = 0
        for k, v in e.items():
            w = d.get(k)
            if w is None: falta += 1; continue
            if tuple(v[:11]) != (w[0], w[2], w[13], w[14], w[12], w[3], w[4], w[5], w[6], w[7], w[15]): dif += 1
        conf[f'divergencias_{t}t_contra_desenhista_11_campos'] = dif; conf[f'faltam_no_desenhista_{t}t'] = falta
        del d
        dif = falta = 0
        for k, v in e.items():
            s = sec.get(k, {}).get(t)
            if s is None: falta += 1; continue
            if (int(v[2]), int(v[3]), int(v[5]), int(v[0])) != (int(s['apt']), int(s['comp']), int(s['urna']), int(s['loc'])): dif += 1
        conf[f'divergencias_{t}t_contra_secoes2026_aptos_comp_urna_local'] = dif; conf[f'faltam_em_secoes2026_{t}t'] = falta
    chaves = sorted(k for k in e2 if k in e1 and '1' in sec.get(k, {}) and '2' in sec[k])
    conf['secoes_pareadas'] = len(chaves)
    conf['so_no_1t'] = sum(1 for k in e1 if k not in e2); conf['so_no_2t'] = sum(1 for k in e2 if k not in e1)
    so1 = [k for k in e1 if k not in e2]
    conf_so1 = {k: {'aptos': int(e1[k][2]), 'comp': int(e1[k][3]), 'H': int(e1[k][4])} for k in so1}
    cand = carregar(DADOS + '/candidatos2026_1t.json.gz')
    tot = {k: int(v) for k, v in cand['totais'].items()}; nominal = sum(tot.values())
    elim = sorted(n for n in tot if n not in ('13', '22') and tot[n] / nominal >= 0.005)
    perf = json.load(gzip.open(PERFIL_A6, 'rt'))['secoes']
    n = len(chaves)
    B = {'chave': np.array(chaves)}
    for nm in ('apt1', 'apt2', 'C1', 'C2', 'H1', 'H2', 'urna1', 'urna2', 'dc1', 'dc2', 'L1', 'R1', 'O1', 'B1', 'N1', 'L2',
               'R2', 'O2', 'B2', 'N2', 'ptot', 'pbio', 'p6069', 'p70m', 'nagr2', 'apur'):
        B[nm] = np.zeros(n, dtype=np.int64)
    B['elim'] = np.zeros((n, len(elim)), dtype=np.int64)
    uf = []; mun = []; zona = []; loc = []; agr1 = []; agr2 = []; locmudou = 0
    cs = cand['secoes']
    for i, k in enumerate(chaves):
        a, b = e1[k], e2[k]; s1, s2 = sec[k]['1'], sec[k]['2']
        u, m, z, _ = k.split('|')
        uf.append(u); mun.append(u + '|' + m); zona.append(u + '|' + z); loc.append(f'{u}|{m}|{z}|{b[0]}')
        if a[0] != b[0]: locmudou += 1
        B['apt1'][i] = int(a[2]); B['apt2'][i] = int(b[2]); B['C1'][i] = int(a[3]); B['C2'][i] = int(b[3])
        B['H1'][i] = int(a[4]); B['H2'][i] = int(b[4]); B['urna1'][i] = int(a[5]); B['urna2'][i] = int(b[5])
        B['dc1'][i] = _data(a[9]); B['dc2'][i] = _data(b[9])
        B['apur'][i] = 1 if (a[1] == 'Apurada' and b[1] == 'Apurada') else 0
        g1, g2 = _agr(a[10]), _agr(b[10]); agr1.append(g1); agr2.append(g2); B['nagr2'][i] = len(g2)
        for nm in ('L', 'R', 'O', 'B', 'N'):
            B[nm + '1'][i] = s1[nm]; B[nm + '2'][i] = s2[nm]
        c = cs.get(k, {})
        for j, nmr in enumerate(elim): B['elim'][i, j] = c.get(nmr, 0)
        pp = perf.get(k)
        if pp is not None:
            v = np.array(pp, dtype=np.int64)
            for ag in g2:
                q = perf.get(f'{u}|{m}|{z}|{ag}')
                if q is not None: v = v + np.array(q, dtype=np.int64)
            B['ptot'][i] = v[0]; B['pbio'][i] = v[1]; B['p6069'][i] = v[8]; B['p70m'][i] = v[9] + v[10]
        else:
            B['ptot'][i] = -1
    B['uf'] = np.array(uf); B['mun'] = np.array(mun); B['zona'] = np.array(zona); B['loc'] = np.array(loc)
    conf['local_mudou_entre_turnos'] = locmudou
    conf['secoes_sem_perfil'] = int((B['ptot'] < 0).sum())
    meta = {'conferencia': dict(conf), 'so_no_1t': conf_so1, 'eliminados_com_termo_proprio': elim,
            'totais_1t': tot, 'nominais_1t': nominal,
            'perfil_soma_total_27ufs_e_exterior': int(B['ptot'][B['ptot'] > 0].sum()),
            'perfil_soma_brutos_todas_as_secoes': int(sum(v[0] for v in perf.values())),
            'perfil_sem_biometria_bruto': int(sum(v[0] - v[1] for v in perf.values()))}
    return B, agr1, agr2, meta


def montar_ano(ano):
    """Bases de 2014, 2018 e 2022 (placebos). Em 2022 junta H = QT_ELEITORES_BIOMETRIA_NH do bweb lido em fluxo."""
    sec = carregar(f'{DADOS}/secoes{ano}.json.gz')
    h = {1: {}, 2: {}}; meta = {}
    if ano == 2022:
        faltam = []
        for t in (1, 2):
            for u in UFS:
                p = f'{TRAB}/dl_bweb2022/est2022_{t}t_{u}.json.gz'
                if os.path.exists(p): h[t].update(json.load(gzip.open(p, 'rt')))
                else: faltam.append(f'{u}_{t}t')
        meta['ufs_faltando_no_bweb2022'] = faltam
    chaves = sorted(k for k, v in sec.items() if '1' in v and '2' in v)
    n = len(chaves); B = {'chave': np.array(chaves)}
    for nm in ('apt1', 'apt2', 'C1', 'C2', 'H1', 'H2', 'urna1', 'urna2', 'L1', 'R1', 'O1', 'B1', 'N1', 'L2', 'R2', 'O2',
               'B2', 'N2', 'apur'):
        B[nm] = np.zeros(n, dtype=np.int64)
    uf = []; mun = []; loc = []; dif = collections.Counter()
    for i, k in enumerate(chaves):
        s1, s2 = sec[k]['1'], sec[k]['2']; u, m, z, _ = k.split('|')
        uf.append(u); mun.append(u + '|' + m); loc.append(f"{u}|{m}|{z}|{s2['loc']}")
        B['apt1'][i] = s1['apt']; B['apt2'][i] = s2['apt']; B['C1'][i] = s1['comp']; B['C2'][i] = s2['comp']
        try: B['urna1'][i] = int(s1['urna']); B['urna2'][i] = int(s2['urna'])
        except (ValueError, TypeError): B['urna1'][i] = -1; B['urna2'][i] = -2
        B['apur'][i] = 1 if (str(s1['tipo']).upper() == 'APURADA' and str(s2['tipo']).upper() == 'APURADA') else 0
        for nm in ('L', 'R', 'O', 'B', 'N'):
            B[nm + '1'][i] = s1[nm]; B[nm + '2'][i] = s2[nm]
        if ano == 2022:
            a, b = h[1].get(k), h[2].get(k)
            if a is None or b is None or not a[4].lstrip('-').isdigit() or not b[4].lstrip('-').isdigit():
                B['H1'][i] = -1; B['H2'][i] = -1; dif['sem_H'] += 1
            else:
                B['H1'][i] = int(a[4]); B['H2'][i] = int(b[4])
                if int(a[4]) < 0 or int(b[4]) < 0: B['H1'][i] = -1; B['H2'][i] = -1; dif['H_negativo'] += 1
                if (int(a[2]), int(a[3])) != (int(s1['apt']), int(s1['comp'])): dif['aptos_ou_comp_1t_difere_da_base'] += 1
                if (int(b[2]), int(b[3])) != (int(s2['apt']), int(s2['comp'])): dif['aptos_ou_comp_2t_difere_da_base'] += 1
    B['uf'] = np.array(uf); B['mun'] = np.array(mun); B['loc'] = np.array(loc)
    meta['pareadas'] = n; meta['conferencia'] = dict(dif)
    if ano == 2022: meta['secoes_no_bweb2022'] = {'1t': len(h[1]), '2t': len(h[2])}
    return B, meta


# ----------------------------------------------------------------------------------------------------------------
# REGRESSÃO COM EFEITO FIXO, PESO E ERRO AGRUPADO POR OUTRO GRUPO (decisão B3)
# ----------------------------------------------------------------------------------------------------------------
class Ctx:
    def __init__(self, g_fe, g_cl, w):
        _, g = np.unique(g_fe, return_inverse=True)
        self.ok = np.bincount(g)[g] >= 2
        _, self.g = np.unique(g[self.ok], return_inverse=True)
        _, self.cl = np.unique(np.asarray(g_cl)[self.ok], return_inverse=True)
        self.w = np.asarray(w, float)[self.ok]; self.ng = int(self.g.max()) + 1; self.ncl = int(self.cl.max()) + 1
        self.sw = np.bincount(self.g, weights=self.w, minlength=self.ng); self.rw = np.sqrt(self.w)
        self.n = int(self.ok.sum())

    def dm(self, v):
        v = np.asarray(v, float)[self.ok]
        return v - (np.bincount(self.g, weights=self.w * v, minlength=self.ng) / self.sw)[self.g]

    def reg(self, y, cols, nomes, pre=None):
        """pre: dict nome -> coluna já centrada (para reaproveitar controles fixos nos plantios)."""
        yd = self.dm(y)
        Xd = np.column_stack([pre[nm] if (pre is not None and nm in pre) else self.dm(c) for c, nm in zip(cols, nomes)])
        var = (Xd * Xd * self.w[:, None]).sum(0)
        fica = var > 1e-9
        nomes_f = [nm for nm, f in zip(nomes, fica) if f]; Xd = Xd[:, fica]; k = Xd.shape[1]
        Xw = Xd * self.rw[:, None]; inv = np.linalg.inv(Xw.T @ Xw); b = inv @ (Xw.T @ (yd * self.rw))
        e = yd - Xd @ b
        S = np.column_stack([np.bincount(self.cl, weights=self.w * Xd[:, j] * e, minlength=self.ncl) for j in range(k)])
        N = len(yd); G = self.ncl
        V = ((G / (G - 1) * (N - 1) / (N - k)) if G > 1 else float('nan')) * inv @ (S.T @ S) @ inv  # com 1 agrupamento não há erro
        se = np.sqrt(np.diag(V))
        return {'n': N, 'locais': self.ng, 'agrupamentos_do_erro': G, 'coef': dict(zip(nomes_f, b.tolist())),
                'ep': dict(zip(nomes_f, se.tolist())), 'retiradas_sem_variacao': [nm for nm, f in zip(nomes, fica) if not f],
                '_V': V, '_nomes': nomes_f}


def limpa(r):
    return {k: v for k, v in r.items() if not k.startswith('_')}


def ce(r, nome):
    return (r['coef'].get(nome), r['ep'].get(nome))


def ic(c, e, z=Z95):
    return [c - z * e, c + z * e]


# ----------------------------------------------------------------------------------------------------------------
# D2-1
# ----------------------------------------------------------------------------------------------------------------
def s1(H1, C1, H2, C2, qref=1.0):
    sH1, sC1, sH2, sC2 = float(H1.sum()), float(C1.sum()), float(H2.sum()), float(C2.sum())
    h1 = sH1 / sC1; h2 = sH2 / sC2; q = h2 / h1
    return {'secoes': int(len(H1)), 'soma_H1': sH1, 'soma_C1': sC1, 'soma_H2': sH2, 'soma_C2': sC2, 'h1': h1, 'h2': h2,
            'q': q, 'q_ref': qref, 'E': sH2 - qref * h1 * sC2, 'E_bruto_qref1': sH2 - h1 * sC2,
            'sobra_proporcional_qref1': (q - 1) * h1}


def s2(H1, C1, H2, C2, ufc, nuf, centrar=True):
    n = len(H1); m5 = H1 >= 5
    r = np.full(n, np.nan); r[m5] = (H2[m5] / C2[m5]) / (H1[m5] / C1[m5])
    quf = np.ones(nuf)
    for u in range(nuf):
        mm = m5 & (ufc == u)
        if mm.any(): quf[u] = np.median(r[mm])
    e = H1 * (C2 / C1) * quf[ufc]
    d = 2 * (np.sqrt(H2 + 0.375) - np.sqrt(e + 0.375))
    fx = np.digitize(e, [5, 10, 20, 40]); z = np.zeros(n); esc = []
    for f in range(5):
        mm = fx == f
        if not mm.any(): esc.append(None); continue
        med = float(np.median(d[mm])); s = 1.4826 * float(np.median(np.abs(d[mm] - med)))
        z[mm] = (d[mm] - (med if centrar else 0.0)) / s
        esc.append({'secoes': int(mm.sum()), 'mediana_d': med, 'escala': s})
    di = z >= 4; es = z <= -4
    cp = np.where(di, H2 - e, 0.0); cm = np.where(es, e - H2, 0.0)
    return {'X_mais': float(cp.sum()), 'X_menos': float(cm.sum()), 'A': float(cp.sum() - cm.sum()),
            'secoes_cauda_direita': int(di.sum()), 'secoes_cauda_esquerda': int(es.sum()),
            'secoes_z6_ou_mais': int((z >= 6).sum()), 'secoes_z_menos6_ou_menos': int((z <= -6).sum()),
            'faixas': esc, '_z': z, '_e': e, '_cp': cp, '_cm': cm, '_quf': quf}


def cols_s3(U, y_extra=None):
    """Colunas da regressão S3 no universo U (dict de vetores)."""
    C1 = U['C1'].astype(float)
    y = ((U['L2'] - U['R2']) - (U['L1'] - U['R1'])) / C1
    x = (U['H2'] - U['H1']) / C1; dC = (U['C2'] - U['C1']) / C1
    cols = [x, dC, U['O1'] / C1, (U['B1'] + U['N1']) / C1, U['L1'] / C1, U['H1'] / C1, (U['urna1'] != U['urna2']).astype(float)]
    return y, cols, ['x_dH', 'dC', 'O1', 'BN1', 'L1', 'H1', 'urna_trocada']


def sub(B, m):
    return {k: (v[m] if isinstance(v, np.ndarray) and len(v) == len(m) else v) for k, v in B.items()}


def universo_d21(B):
    return (B['apur'] == 1) & (B['C1'] >= 50) & (B['C2'] >= 50) & (np.abs(B['apt2'] - B['apt1']) <= 2) & (B['uf'] != 'ZZ') & (B['H1'] >= 0)


def inverte(U):
    V = dict(U)
    for a in ('apt', 'C', 'H', 'urna', 'L', 'R', 'O', 'B', 'N'):
        V[a + '1'], V[a + '2'] = U[a + '2'], U[a + '1']
    return V


def d21_completo(U, rotulo, qref, com_boot=True, rng=None, W=None, muns=None):
    """S1, S2 e S3 num universo (dict de vetores). Devolve resultados e peças para o bootstrap."""
    ufc, ufs = _cod(U['uf'])
    r1 = s1(U['H1'], U['C1'], U['H2'], U['C2'], qref)
    r2 = s2(U['H1'].astype(float), U['C1'].astype(float), U['H2'].astype(float), U['C2'].astype(float), ufc, len(ufs))
    r2n = s2(U['H1'].astype(float), U['C1'].astype(float), U['H2'].astype(float), U['C2'].astype(float), ufc, len(ufs), centrar=False)
    ctx = Ctx(U['loc'], U['mun'], U['C1'])
    y, cols, nomes = cols_s3(U)
    r3 = ctx.reg(y, cols, nomes)
    return r1, r2, r2n, r3, ctx


def somas_mun(muns_idx, G, *vs):
    return np.column_stack([np.bincount(muns_idx, weights=np.asarray(v, float), minlength=G) for v in vs])


def pct(a, ps=(2.5, 97.5)):
    a = np.asarray(a, float); a = a[np.isfinite(a)]
    return [float(x) for x in np.percentile(a, ps)] if len(a) else None



def sort_uniforme(rng, K, C2):
    return rng.multinomial(int(K), C2 / C2.sum())


def sort_concentrado(rng, K, C2, frac=0.05, onde=None):
    n = len(C2); k = np.zeros(n, dtype=np.int64)
    cand = np.arange(n) if onde is None else np.flatnonzero(onde)
    idx = rng.choice(cand, size=max(1, int(round(frac * len(cand)))), replace=False)
    k[idx] = rng.multinomial(int(K), C2[idx] / C2[idx].sum())
    return k


def resumo(v):
    v = np.asarray(v, float)
    return {'media': float(v.mean()), 'min': float(v.min()), 'max': float(v.max())}


def roda_d21(B, B22, meta22, rng):
    R = {}
    m = universo_d21(B); U = sub(B, m); n = int(m.sum())
    R['universo'] = {
        'secoes': n, 'secoes_pareadas': int(len(m)), 'secoes_fora': int((~m).sum()),
        'comparecimento_2t_dentro': int(B['C2'][m].sum()), 'comparecimento_2t_fora': int(B['C2'][~m].sum()),
        'comparecimento_1t_fora': int(B['C1'][~m].sum()),
        'margem_2t_dentro': int((B['L2'][m] - B['R2'][m]).sum()), 'margem_2t_fora': int((B['L2'][~m] - B['R2'][~m]).sum()),
        'fora_por_motivo_nao_exclusivo': {
            'exterior': int((B['uf'] == 'ZZ').sum()), 'tipo_nao_apurada': int((B['apur'] == 0).sum()),
            'comparecimento_abaixo_de_50_em_algum_turno': int(((B['C1'] < 50) | (B['C2'] < 50)).sum()),
            'aptos_variam_mais_de_2': int((np.abs(B['apt2'] - B['apt1']) > 2).sum())},
        'liberacoes_2t_fora': int(B['H2'][~m].sum()), 'liberacoes_1t_fora': int(B['H1'][~m].sum())}
    m22 = universo_d21(B22); U22 = sub(B22, m22)
    tem22 = int(m22.sum()) > 1000
    R['universo_2022'] = {'secoes': int(m22.sum()), 'secoes_pareadas': int(len(m22)), 'tem_2022': tem22, **meta22}
    q22 = s1(U22['H1'], U22['C1'], U22['H2'], U22['C2'])['q'] if tem22 else 1.0
    r1, r2, r2n, r3, ctx = d21_completo(U, '2026', q22)
    # conferência da função de regressão contra lib.fe_ols (erro por local nos dois)
    y, cols, nomes = cols_s3(U)
    a = fe_ols(y, np.column_stack(cols), U['loc'], w=U['C1'], nomes=nomes)
    b = Ctx(U['loc'], U['loc'], U['C1']).reg(y, cols, nomes)
    R['conferencia_reg_fe_contra_lib'] = {'maior_dif_coef': max(abs(a['coef'][k] - b['coef'][k]) for k in nomes),
                                          'maior_dif_ep': max(abs(a['ep'][k] - b['ep'][k]) for k in nomes),
                                          'gama_ep_por_local': b['ep']['x_dH']}
    # ---------- bootstrap de municípios (os mesmos municípios nos dois anos) ----------
    muns = np.unique(np.concatenate([U['mun'], U22['mun']])) if tem22 else np.unique(U['mun'])
    G = len(muns); i26 = np.searchsorted(muns, U['mun']); i22 = np.searchsorted(muns, U22['mun']) if tem22 else None
    M26 = somas_mun(i26, G, U['H1'], U['C1'], U['H2'], U['C2'], r2['_cp'], r2['_cm'])
    W = rng.multinomial(G, np.full(G, 1.0 / G), size=NBOOT).astype(np.float64)
    S26 = W @ M26
    h1b = S26[:, 0] / S26[:, 1]; q26b = (S26[:, 2] / S26[:, 3]) / h1b
    Eb_bruto = S26[:, 2] - h1b * S26[:, 3]; Ab = S26[:, 4] - S26[:, 5]
    if tem22:
        r1_22 = s1(U22['H1'], U22['C1'], U22['H2'], U22['C2'])
        ufc22, ufs22 = _cod(U22['uf'])
        r2_22 = s2(U22['H1'].astype(float), U22['C1'].astype(float), U22['H2'].astype(float), U22['C2'].astype(float), ufc22, len(ufs22))
        ctx22 = Ctx(U22['loc'], U22['mun'], U22['C1']); y22, c22, n22 = cols_s3(U22); r3_22 = ctx22.reg(y22, c22, n22)
        M22 = somas_mun(i22, G, U22['H1'], U22['C1'], U22['H2'], U22['C2'], r2_22['_cp'], r2_22['_cm'])
        S22 = W @ M22
        h1b22 = S22[:, 0] / S22[:, 1]; q22b = (S22[:, 2] / S22[:, 3]) / h1b22
        Eb22_bruto = S22[:, 2] - h1b22 * S22[:, 3]; Ab22 = S22[:, 4] - S22[:, 5]
    else:
        q22b = np.ones(NBOOT)
    Eb_conj = S26[:, 2] - q22b * h1b * S26[:, 3]; Eb_fixo = S26[:, 2] - q22 * h1b * S26[:, 3]
    Qb = np.maximum(Eb_conj, Ab)
    g, eg = ce(r3, 'x_dH')
    Q = max(r1['E'], r2['A'])
    R['S1'] = {**r1, 'ic95_E_qref_reestimado': pct(Eb_conj), 'ic99_E_qref_reestimado': pct(Eb_conj, (0.5, 99.5)),
               'ic95_E_qref_fixo': pct(Eb_fixo), 'ic95_E_bruto_qref1': pct(Eb_bruto), 'ic99_E_bruto_qref1': pct(Eb_bruto, (0.5, 99.5)),
               'ep_boot_E': float(Eb_conj.std()), 'ep_boot_E_bruto': float(Eb_bruto.std()),
               'ic95_q': pct(q26b), 'E_sobre_margem': r1['E'] / MARGEM, 'E_bruto_sobre_margem': r1['E_bruto_qref1'] / MARGEM,
               'variacao_H': r1['soma_H2'] - r1['soma_H1'], 'variacao_C': r1['soma_C2'] - r1['soma_C1'],
               'fatia_da_alta_do_comparecimento_que_veio_por_liberacao': (r1['soma_H2'] - r1['soma_H1']) / (r1['soma_C2'] - r1['soma_C1'])}
    R['S2'] = {**limpa(r2), 'ic95_A': pct(Ab), 'ic99_A': pct(Ab, (0.5, 99.5)), 'ep_boot_A': float(Ab.std()),
               'sem_centrar_ao_lado': limpa(r2n)}
    R['Q'] = {'Q': Q, 'ic95': pct(Qb), 'ic99': pct(Qb, (0.5, 99.5)), 'Q_sobre_margem': Q / MARGEM}
    R['S3'] = {**limpa(r3), 'gama': g, 'ep': eg, 'ic95': ic(g, eg), 'ic99': ic(g, eg, Z99)}
    # ---------- por UF e por urna ----------
    porUF = {}
    ufm = np.array([x.split('|')[0] for x in muns])
    for u in UFS:
        a = U['uf'] == u
        if tem22:
            b = U22['uf'] == u
            qr = s1(U22['H1'][b], U22['C1'][b], U22['H2'][b], U22['C2'][b])['q'] if b.sum() > 0 and U22['H1'][b].sum() > 0 else float('nan')
        else: qr = 1.0
        x = s1(U['H1'][a], U['C1'][a], U['H2'][a], U['C2'][a], qr)
        mk = ufm == u; Wk = W[:, mk]
        if mk.sum() > 1:
            s = Wk @ M26[mk]; ok = (s[:, 1] > 0) & (s[:, 3] > 0) & (s[:, 0] > 0)
            hb = s[ok, 0] / s[ok, 1]; ebb = s[ok, 2] - hb * s[ok, 3]
            if tem22:
                t = Wk @ M22[mk]; ok2 = ok & (t[:, 0] > 0) & (t[:, 1] > 0) & (t[:, 3] > 0)
                qb = (t[ok2, 2] / t[ok2, 3]) / (t[ok2, 0] / t[ok2, 1]); s2_ = s[ok2]
                ebc = s2_[:, 2] - qb * (s2_[:, 0] / s2_[:, 1]) * s2_[:, 3]
            else: ebc = ebb
            x['ic95_E_bruto_qref1'] = pct(ebb); x['ic95_E_qref_uf'] = pct(ebc)
        else:
            x['ic95_E_bruto_qref1'] = None; x['ic95_E_qref_uf'] = None
        x['E_qref_nacional'] = x['soma_H2'] - q22 * x['h1'] * x['soma_C2']
        x['variacao_H'] = x['soma_H2'] - x['soma_H1']; x['variacao_C'] = x['soma_C2'] - x['soma_C1']
        x['margem_2t'] = int((U['L2'][a] - U['R2'][a]).sum())
        porUF[u] = x
    R['S1_por_UF'] = porUF
    R['S1_soma_das_UFs'] = {'E_qref_da_UF': float(np.nansum([v['E'] for v in porUF.values()])),
                            'E_bruto_qref1_por_UF': float(sum(v['E_bruto_qref1'] for v in porUF.values())),
                            'soma_dos_E_positivos_bruto': float(sum(max(v['E_bruto_qref1'], 0) for v in porUF.values())),
                            'soma_dos_E_positivos_qref_uf': float(np.nansum([max(v['E'], 0) for v in porUF.values()]))}
    est = {}
    for nome, f in (('mesma_urna', lambda X: X['urna1'] == X['urna2']), ('urna_diferente', lambda X: X['urna1'] != X['urna2'])):
        a = f(U)
        if tem22:
            b = f(U22); qr = s1(U22['H1'][b], U22['C1'][b], U22['H2'][b], U22['C2'][b])['q']
        else: qr = 1.0
        x = s1(U['H1'][a], U['C1'][a], U['H2'][a], U['C2'][a], qr)
        s = W @ somas_mun(i26[a], G, U['H1'][a], U['C1'][a], U['H2'][a], U['C2'][a]); ok = s[:, 1] > 0
        x['ic95_E_bruto_qref1'] = pct(s[ok, 2] - s[ok, 0] / s[ok, 1] * s[ok, 3])
        if tem22:
            t = W @ somas_mun(i22[b], G, U22['H1'][b], U22['C1'][b], U22['H2'][b], U22['C2'][b]); ok2 = ok & (t[:, 1] > 0) & (t[:, 0] > 0) & (t[:, 3] > 0)
            qb = (t[ok2, 2] / t[ok2, 3]) / (t[ok2, 0] / t[ok2, 1])
            x['ic95_E_qref_estrato'] = pct(s[ok2, 2] - qb * s[ok2, 0] / s[ok2, 1] * s[ok2, 3])
        est[nome] = x
    R['S1_por_urna'] = est
    # ---------- placebo de 2022 ----------
    if tem22:
        g22, eg22 = ce(r3_22, 'x_dH')
        R['placebo_2022'] = {
            'S1': {**r1_22, 'ic95_E_bruto_qref1': pct(Eb22_bruto), 'ic95_q': pct(q22b),
                   'variacao_H': r1_22['soma_H2'] - r1_22['soma_H1'], 'variacao_C': r1_22['soma_C2'] - r1_22['soma_C1']},
            'S2': {**limpa(r2_22), 'ic95_A': pct(Ab22)},
            'S3': {**limpa(r3_22), 'gama': g22, 'ep': eg22, 'ic95': ic(g22, eg22)},
            'sobra_proporcional_2022': r1_22['sobra_proporcional_qref1'], 'sobra_proporcional_2026': r1['sobra_proporcional_qref1'],
            'razao_2022_sobre_2026': r1_22['sobra_proporcional_qref1'] / r1['sobra_proporcional_qref1'] if r1['sobra_proporcional_qref1'] != 0 else None,
            'ic95_razao': pct(((q22b - 1) * h1b22) / ((q26b - 1) * h1b))}
        yL = (U22['L2'] - U22['L1']) / U22['C1']; yR = (U22['R2'] - U22['R1']) / U22['C1']
        yBN = ((U22['B2'] + U22['N2']) - (U22['B1'] + U22['N1'])) / U22['C1']
        for nm, yy in (('gama_L', yL), ('gama_R', yR), ('gama_BN', yBN)):
            rr = ctx22.reg(yy, c22, n22); R['placebo_2022']['S3'][nm] = list(ce(rr, 'x_dH'))
        Ui = inverte(U22); ui1 = s1(Ui['H1'], Ui['C1'], Ui['H2'], Ui['C2'])
        ui2 = s2(Ui['H1'].astype(float), Ui['C1'].astype(float), Ui['H2'].astype(float), Ui['C2'].astype(float), ufc22, len(ufs22))
        R['placebo_2022']['turnos_invertidos'] = {'S1': ui1, 'S2': limpa(ui2)}
    # ---------- espelhos de 2026 ----------
    esp = {}
    Ui = inverte(U); ufc, ufs = _cod(U['uf'])
    ui1 = s1(Ui['H1'], Ui['C1'], Ui['H2'], Ui['C2'], 1.0 / q22)
    ui2 = s2(Ui['H1'].astype(float), Ui['C1'].astype(float), Ui['H2'].astype(float), Ui['C2'].astype(float), ufc, len(ufs))
    ctxi = Ctx(Ui['loc'], Ui['mun'], Ui['C1']); yi, ci, ni = cols_s3(Ui); ri = ctxi.reg(yi, ci, ni)
    Mi = somas_mun(i26, G, Ui['H1'], Ui['C1'], Ui['H2'], Ui['C2'], ui2['_cp'], ui2['_cm']); Si = W @ Mi
    esp['turnos_invertidos'] = {'S1': {**ui1, 'ic95_E_bruto_qref1': pct(Si[:, 2] - Si[:, 0] / Si[:, 1] * Si[:, 3])},
                                'S2': {**limpa(ui2), 'ic95_A': pct(Si[:, 4] - Si[:, 5])},
                                'S3': {**limpa(ri), 'gama': ri['coef']['x_dH'], 'ep': ri['ep']['x_dH']}}
    C1f = U['C1'].astype(float)
    for nm, yy in (('gama_L', (U['L2'] - U['L1']) / C1f), ('gama_R', (U['R2'] - U['R1']) / C1f),
                   ('gama_BN_desfecho_placebo', ((U['B2'] + U['N2']) - (U['B1'] + U['N1'])) / C1f)):
        rr = ctx.reg(yy, cols, nomes); esp[nm] = {'coef': rr['coef']['x_dH'], 'ep': rr['ep']['x_dH'], 'todos': limpa(rr)}
    R['espelhos'] = esp
    # ---------- complementos fixados antes (não decidem) ----------
    comp = {}
    for nome, lista in (('UF5_PI_MA_TO_PB_CE', UF5), ('resto', [u for u in UFS if u not in UF5])):
        a = np.isin(U['uf'], lista); Ua = sub(U, a)
        if tem22:
            b = np.isin(U22['uf'], lista); qr = s1(U22['H1'][b], U22['C1'][b], U22['H2'][b], U22['C2'][b])['q']
        else: qr = 1.0
        x = s1(Ua['H1'], Ua['C1'], Ua['H2'], Ua['C2'], qr)
        mk = np.isin(ufm, lista); s = W[:, mk] @ M26[mk]
        x['ic95_E_bruto_qref1'] = pct(s[:, 2] - s[:, 0] / s[:, 1] * s[:, 3])
        ca = Ctx(Ua['loc'], Ua['mun'], Ua['C1']); ya, cola, na = cols_s3(Ua); ra = ca.reg(ya, cola, na)
        x['S3'] = {'gama': ra['coef']['x_dH'], 'ep': ra['ep']['x_dH'], 'n': ra['n']}
        x['margem_2t'] = int((Ua['L2'] - Ua['R2']).sum())
        comp[nome] = x
    comp['S3_por_regiao'] = {}
    for reg, lista in REGIOES.items():
        a = np.isin(U['uf'], lista); Ua = sub(U, a)
        ca = Ctx(Ua['loc'], Ua['mun'], Ua['C1']); ya, cola, na = cols_s3(Ua); ra = ca.reg(ya, cola, na)
        comp['S3_por_regiao'][reg] = {'gama': ra['coef']['x_dH'], 'ep': ra['ep']['x_dH'], 'n': ra['n']}
    tp = U['ptot'] > 0
    if tp.sum() > 1000:
        Up = sub(U, tp); cp_ = Ctx(Up['loc'], Up['mun'], Up['C1']); yp, colp, np_ = cols_s3(Up)
        pt = Up['ptot'].astype(float)
        colp2 = colp + [Up['p6069'] / pt, Up['p70m'] / pt, (Up['ptot'] - Up['pbio']) / pt]
        rp = cp_.reg(yp, colp2, np_ + ['f_60a69', 'f_70mais', 'f_sem_biometria'])
        rp0 = cp_.reg(yp, colp, np_)
        comp['S3_com_perfil'] = {'gama': rp['coef']['x_dH'], 'ep': rp['ep']['x_dH'], 'gama_sem_perfil_mesmas_secoes': rp0['coef']['x_dH'],
                                 'n': rp['n'], 'coef': rp['coef'], 'ep_todos': rp['ep']}
    z = r2['_z']
    rc = ctx.reg(y, [(z >= 4).astype(float), (z <= -4).astype(float)] + cols[1:], ['cauda_direita', 'cauda_esquerda'] + nomes[1:])
    comp['cauda_e_voto'] = {'coef_cauda_direita': rc['coef']['cauda_direita'], 'ep_cauda_direita': rc['ep']['cauda_direita'],
                            'coef_cauda_esquerda': rc['coef']['cauda_esquerda'], 'ep_cauda_esquerda': rc['ep']['cauda_esquerda'],
                            'C1_cauda_direita': int(U['C1'][z >= 4].sum()), 'C1_cauda_esquerda': int(U['C1'][z <= -4].sum()),
                            'votos_de_margem_cauda_direita': rc['coef']['cauda_direita'] * float(U['C1'][z >= 4].sum()),
                            'votos_de_margem_cauda_esquerda': rc['coef']['cauda_esquerda'] * float(U['C1'][z <= -4].sum())}
    c1 = Ctx(U['loc'], U['mun'], np.ones(n)); ri2 = c1.reg(U['H2'] - U['H1'], [U['C2'] - U['C1']], ['dC'])
    comp['inclinacao_dH_em_dC_dentro_do_local'] = {'coef': ri2['coef']['dC'], 'ep': ri2['ep']['dC'], 'fatia_H1_sobre_C1': r1['h1']}
    R['complementos'] = comp
    # ---------- achado local ----------
    e_ = r2['_e']; o = np.argsort(-z); nz6 = int((z >= 6).sum())
    lst = [{'chave': str(U['chave'][i]), 'H1': int(U['H1'][i]), 'C1': int(U['C1'][i]), 'H2': int(U['H2'][i]), 'C2': int(U['C2'][i]),
            'esperado': round(float(e_[i]), 2), 'z': round(float(z[i]), 2),
            'variacao_da_margem': int((U['L2'][i] - U['R2'][i]) - (U['L1'][i] - U['R1'][i])), 'urna_trocada': bool(U['urna1'][i] != U['urna2'][i])}
           for i in o[:nz6]]
    with open(f'{TRAB}/secoes_z6.csv', 'w') as f:
        f.write('chave;H1;C1;H2;C2;esperado;z;variacao_da_margem;urna_trocada\n')
        for d in lst: f.write(';'.join(str(d[k]) for k in ('chave', 'H1', 'C1', 'H2', 'C2', 'esperado', 'z', 'variacao_da_margem', 'urna_trocada')) + '\n')
    z6 = z >= 6
    R['achado_local'] = {'secoes_z6_ou_mais': nz6, 'liberacoes_a_mais_nelas': float((U['H2'] - e_)[z6].sum()),
                         'H2_nelas': int(U['H2'][z6].sum()), 'C2_nelas': int(U['C2'][z6].sum()),
                         'por_UF': dict(collections.Counter(U['uf'][z6].tolist())),
                         'com_urna_trocada': int((U['urna1'][z6] != U['urna2'][z6]).sum()),
                         'variacao_da_margem_nelas': int(((U['L2'] - U['R2']) - (U['L1'] - U['R1']))[z6].sum()),
                         'variacao_da_margem_por_C1_nelas': float(((U['L2'] - U['R2']) - (U['L1'] - U['R1']))[z6].sum() / U['C1'][z6].sum()),
                         'variacao_da_margem_por_C1_no_universo': float(((U['L2'] - U['R2']) - (U['L1'] - U['R1'])).sum() / U['C1'].sum()),
                         'lista_300_maiores': lst[:300], 'lista_inteira': f'{TRAB}/secoes_z6.csv'}
    grava('parcial_d21_observado.json', R)
    # ---------- plantios ----------
    pre = {nm: ctx.dm(c) for nm, c in zip(nomes, cols) if nm in ('O1', 'BN1', 'L1', 'H1', 'urna_trocada')}
    H1f, C1f2 = U['H1'].astype(float), U['C1'].astype(float)

    def mede(H2, C2, L2, R2):
        e1_ = s1(U['H1'], U['C1'], H2, C2, q22)
        a_ = s2(H1f, C1f2, H2.astype(float), C2.astype(float), ufc, len(ufs))
        yy = ((L2 - R2) - (U['L1'] - U['R1'])) / C1f2
        rr = ctx.reg(yy, [(H2 - U['H1']) / C1f2, (C2 - U['C1']) / C1f2] + cols[2:], nomes, pre=pre)
        return e1_['E'], e1_['E_bruto_qref1'], a_['A'], a_['X_mais'], a_['X_menos'], rr['coef']['x_dH'], rr['ep']['x_dH']

    base = mede(U['H2'], U['C2'], U['L2'], U['R2'])
    P = {'observado': dict(zip(['E', 'E_bruto', 'A', 'X_mais', 'X_menos', 'gama', 'ep_gama'], base))}
    C2u, H2u, L2u, R2u = U['C2'], U['H2'], U['L2'], U['R2']
    p1 = np.where(U['C1'] > 0, U['H1'] / np.maximum(U['C1'], 1), 0.0)
    p2 = np.where(C2u > 0, H2u / np.maximum(C2u, 1), 0.0)
    conf_ = []
    for K in (LIM25, LIM10):
        for des in ('uniforme', 'concentrado'):
            conf_.append((f'irregularidade_{des}_{K}', K, des, 'irr'))
    for des in ('uniforme', 'concentrado'):
        conf_.append((f'inocente_I1_eleitor_real_{des}_{LIM25}', LIM25, des, 'I1'))
        conf_.append((f'inocente_I2_leitor_pior_{des}_{LIM25}', LIM25, des, 'I2'))
    conf_.append((f'inocente_I3_abstencao_pura_uniforme_{LIM25}', LIM25, 'uniforme', 'I3'))
    conf_.append((f'inocente_I3_abstencao_pura_concentrado_{LIM25}', LIM25, 'concentrado', 'I3'))
    for nome, K, des, tipo in conf_:
        out = []
        for rep in range(NREP):
            if tipo == 'I3':
                k = sort_uniforme(rng, K, R2u.astype(float)) if des == 'uniforme' else sort_concentrado(rng, K, R2u.astype(float))
                k = np.minimum(k, R2u)
                dh = rng.binomial(k, np.clip(p2, 0, 1)); dh = np.minimum(dh, H2u)
                out.append(mede(H2u - dh, C2u - k, L2u, R2u - k) + (int(k.sum()),))
                continue
            k = sort_uniforme(rng, K, C2u.astype(float)) if des == 'uniforme' else sort_concentrado(rng, K, C2u.astype(float))
            if tipo == 'irr': out.append(mede(H2u + k, C2u + k, L2u + k, R2u) + (int(k.sum()),))
            elif tipo == 'I1': out.append(mede(H2u + rng.binomial(k, np.clip(p1, 0, 1)), C2u + k, L2u + k, R2u) + (int(k.sum()),))
            elif tipo == 'I2':
                kk = np.minimum(k, C2u - H2u); out.append(mede(H2u + kk, C2u, L2u, R2u) + (int(kk.sum()),))
        o = np.array(out, float); Kef = float(o[:, 7].mean())
        P[nome] = {'K': K, 'K_efetivo': Kef, 'repeticoes': NREP,
                   'delta_E': resumo(o[:, 0] - base[0]), 'delta_E_sobre_K': float((o[:, 0] - base[0]).mean() / Kef),
                   'delta_E_bruto_sobre_K': float((o[:, 1] - base[1]).mean() / Kef),
                   'delta_A': resumo(o[:, 2] - base[2]), 'delta_A_sobre_K': float((o[:, 2] - base[2]).mean() / Kef),
                   'gama': resumo(o[:, 5]), 'delta_gama': float((o[:, 5] - base[5]).mean()), 'ep_gama': float(o[:, 6].mean()),
                   'E_plantado': resumo(o[:, 0]), 'A_plantado': resumo(o[:, 2])}
        grava('parcial_d21_plantios.json', P)
        print('  plantio', nome, round(P[nome]['delta_E_sobre_K'], 3), round(P[nome]['delta_A_sobre_K'], 3), round(P[nome]['gama']['media'], 3), flush=True)
    R['plantios'] = P
    # ---------- regra de poder (L8) e veredito ----------
    esperado_S1 = 1 - q22 * r1['h1']
    pu10, pu25 = P[f'irregularidade_uniforme_{LIM10}'], P[f'irregularidade_uniforme_{LIM25}']
    pc25, pc10 = P[f'irregularidade_concentrado_{LIM25}'], P[f'irregularidade_concentrado_{LIM10}']
    icE = R['S1']['ic95_E_qref_reestimado']
    v_s1 = pu10['delta_E_sobre_K'] >= 0.90 and pu25['delta_E_sobre_K'] >= 0.90 and (icE[1] - icE[0]) / 2 < LIM10
    v_s2 = pc25['delta_A_sobre_K'] >= 0.90
    v_s3 = pc25['gama']['media'] >= 0.6
    R['poder'] = {'S1_enxerga': bool(v_s1), 'S2_enxerga': bool(v_s2), 'S3_enxerga': bool(v_s3),
                  'S1_devolve_uniforme_25': pu25['delta_E_sobre_K'], 'S1_devolve_uniforme_10': pu10['delta_E_sobre_K'],
                  'S1_esperado_pela_formula': esperado_S1, 'S1_na_faixa_do_registro_095_105': bool(0.95 <= pu25['delta_E_sobre_K'] <= 1.05),
                  'S1_meia_largura_ic95': (icE[1] - icE[0]) / 2,
                  'S2_devolve_concentrado_25': pc25['delta_A_sobre_K'], 'S2_devolve_concentrado_10': pc10['delta_A_sobre_K'],
                  'S3_gama_concentrado_25': pc25['gama']['media'], 'S3_gama_concentrado_10': pc10['gama']['media']}
    icQ = R['Q']['ic95']; icg = R['S3']['ic95']
    sp26 = r1['sobra_proporcional_qref1']; sp22 = r1_22['sobra_proporcional_qref1'] if tem22 else None
    plc_limpo = bool(tem22 and sp26 > 0 and sp22 < sp26 / 3 and g22 < 0.10)
    c_sinal = bool(Q >= LIM25 and icQ[0] >= LIM10 and g >= 0.30 and icg[0] > 0.10 and plc_limpo)
    c_sem = bool(icE[1] < LIM10 and r2['A'] < LIM10 and icg[1] < 0.10)
    icEb = R['S1']['ic95_E_bruto_qref1']
    c_sem_so_2026 = bool(icEb[1] < LIM10 and r2['A'] < LIM10 and icg[1] < 0.10)
    parecida = bool(tem22 and sp26 > 0 and sp22 >= sp26 / 3 and icEb[1] >= LIM10)
    if not v_s1 or (not v_s2 and not v_s3): ver = 'SEM PODER'
    elif c_sinal: ver = 'SINAL'
    elif not tem22: ver = 'INCONCLUSIVO'
    elif parecida: ver = 'INCONCLUSIVO'
    elif c_sem: ver = 'SEM SINAL'
    else: ver = 'INCONCLUSIVO'
    letra = 'SINAL' if c_sinal else ('INCONCLUSIVO' if (not tem22 or parecida) else ('SEM SINAL' if c_sem else 'INCONCLUSIVO'))
    ic99E = R['S1']['ic99_E_qref_reestimado']; ic99g = R['S3']['ic99']
    R['veredito'] = {'veredito': ver, 'pela_letra_do_registro_sem_a_regra_de_poder_L8': letra, 'condicoes_sinal': {'Q>=1107548': bool(Q >= LIM25), 'limite_inferior_Q>=443019': bool(icQ[0] >= LIM10),
                                                          'gama>=0,30': bool(g >= 0.30), 'limite_inferior_gama>0,10': bool(icg[0] > 0.10),
                                                          'placebo_2022_limpo': plc_limpo},
                     'condicoes_sem_sinal': {'limite_superior_E<443019': bool(icE[1] < LIM10), 'A<443019': bool(r2['A'] < LIM10),
                                             'limite_superior_gama<0,10': bool(icg[1] < 0.10)},
                     'sem_sinal_vale_so_com_2026_qref1': c_sem_so_2026, 'clausula_sobra_parecida_em_2022': parecida,
                     'com_ic99_as_condicoes_de_sem_sinal_seguem': bool(ic99E[1] < LIM10 and r2['A'] < LIM10 and ic99g[1] < 0.10),
                     'tem_2022': tem22}
    grava('parcial_d21.json', R)
    return R, U, r2



# ----------------------------------------------------------------------------------------------------------------
# D4-6 (a)
# ----------------------------------------------------------------------------------------------------------------
def f_a1(X):
    return float((X['H2'] - X['H1']).sum() - X['H1'].sum() / X['C1'].sum() * (X['C2'] - X['C1']).sum())


def boot_f(X, rng):
    ic_, u = _cod(X['mun']); G = len(u)
    M = somas_mun(ic_, G, X['H1'], X['C1'], X['H2'], X['C2'])
    S = rng.multinomial(G, np.full(G, 1.0 / G), size=NBOOT).astype(float) @ M
    Fb = (S[:, 2] - S[:, 0]) - S[:, 0] / S[:, 1] * (S[:, 3] - S[:, 1])
    return pct(Fb), float(Fb.std())


def cols_a2(X, somados=False):
    y = ((X['L2'] - X['L1']) - (X['R2'] - X['R1'])).astype(float)
    cols = [(X['H2'] - X['H1']).astype(float), (X['C2'] - X['C1']).astype(float)]; nomes = ['dNB_mu_menos_mulinha', 'dC_mulinha']
    if somados or 'elim' not in X:
        cols.append(X['O1'].astype(float)); nomes.append('eliminados_somados')
    else:
        for j, nm in enumerate(X['_elim_nomes']):
            cols.append(X['elim'][:, j].astype(float)); nomes.append('elim_' + nm)
        cols.append((X['O1'] - X['elim'].sum(1)).astype(float)); nomes.append('elim_resto')
    cols += [X['B1'].astype(float), X['N1'].astype(float)]; nomes += ['B1', 'N1']
    return y, cols, nomes


def le_a2(r):
    a, b = '_nomes', '_V'; i, j = r[a].index('dNB_mu_menos_mulinha'), r[a].index('dC_mulinha')
    d, m_ = r['coef']['dNB_mu_menos_mulinha'], r['coef']['dC_mulinha']
    V = r[b]
    return {'mu_menos_mulinha': d, 'ep': r['ep']['dNB_mu_menos_mulinha'], 'ic95': ic(d, r['ep']['dNB_mu_menos_mulinha']),
            'mulinha_com_biometria': m_, 'ep_mulinha': r['ep']['dC_mulinha'],
            'mu_sem_biometria': d + m_, 'ep_mu': float(np.sqrt(V[i, i] + V[j, j] + 2 * V[i, j])), 'n': r['n'], 'locais': r['locais']}


def universo_d41(B):
    return (B['apur'] == 1) & (np.abs(B['apt2'] - B['apt1']) <= 2) & (B['C1'] >= 30) & (B['uf'] != 'ZZ') & (B['apt1'] > 0) & (B['H1'] >= 0)


def roda_d46(B, B22, meta, rng):
    R = {}
    # ---- a1 ----
    br = B['uf'] != 'ZZ'
    a1 = {}
    for nome, m in (('todas_as_pareadas_27UFs_e_exterior', np.ones(len(br), bool)), ('so_27_UFs', br), ('universo_do_D2-1', universo_d21(B))):
        X = sub(B, m); icf, epf = boot_f(X, rng)
        a1[nome] = {'secoes': int(m.sum()), 'F': f_a1(X), 'ic95': icf, 'ep_boot': epf, 'variacao_NB': int((X['H2'] - X['H1']).sum()),
                    'variacao_comp': int((X['C2'] - X['C1']).sum()), 'fatia_NB_1t': float(X['H1'].sum() / X['C1'].sum()),
                    'fatia_NB_2t': float(X['H2'].sum() / X['C2'].sum()), 'soma_NB1': int(X['H1'].sum()), 'soma_NB2': int(X['H2'].sum()),
                    'F_sobre_margem': f_a1(X) / MARGEM}
    R['a1'] = a1
    Fp = a1['todas_as_pareadas_27UFs_e_exterior']['F']
    # ---- a2 ----
    m = universo_d41(B); X = sub(B, m); X['_elim_nomes'] = meta['eliminados_com_termo_proprio']
    ctx = Ctx(X['loc'], X['mun'], 1.0 / X['apt1'])
    y, cols, nomes = cols_a2(X)
    r = ctx.reg(y, cols, nomes)
    R['a2'] = {'universo_secoes': int(m.sum()), **le_a2(r), 'coef': r['coef'], 'ep_todos': r['ep']}
    for nm, yy in (('ganho_de_Lula_L2_menos_L1', (X['L2'] - X['L1']).astype(float)), ('ganho_de_Flavio_R2_menos_R1', (X['R2'] - X['R1']).astype(float)),
                   ('desfecho_placebo_BN2_menos_BN1', ((X['B2'] + X['N2']) - (X['B1'] + X['N1'])).astype(float))):
        R['a2'][nm] = le_a2(ctx.reg(yy, cols, nomes))
    ys, cs, ns = cols_a2(X, somados=True); R['a2']['versao_eliminados_somados'] = le_a2(ctx.reg(ys, cs, ns))
    Xi = inverte(X); Xi['_elim_nomes'] = X['_elim_nomes']
    yi = ((Xi['L2'] - Xi['L1']) - (Xi['R2'] - Xi['R1'])).astype(float)
    ci = [(Xi['H2'] - Xi['H1']).astype(float), (Xi['C2'] - Xi['C1']).astype(float), Xi['B1'].astype(float), Xi['N1'].astype(float)]
    ri = Ctx(Xi['loc'], Xi['mun'], 1.0 / Xi['apt1']).reg(yi, ci, ['dNB_mu_menos_mulinha', 'dC_mulinha', 'B1', 'N1'])
    R['a2']['espelho_turnos_invertidos'] = le_a2(ri)
    # ---- a3 ----
    tp = X['ptot'] > 0; Xp = sub(X, tp); Xp['_elim_nomes'] = X['_elim_nomes']
    SB = (Xp['ptot'] - Xp['pbio']).astype(float); A1 = (Xp['apt1'] - Xp['C1']).astype(float)
    ctx3 = Ctx(Xp['loc'], Xp['mun'], 1.0 / Xp['apt1'])
    r3 = ctx3.reg((Xp['C2'] - Xp['C1']).astype(float), [SB, A1], ['SB', 'abstencao_1t'])
    sSB_nac = float(meta['perfil_sem_biometria_bruto']); c3, e3 = ce(r3, 'SB')
    R['a3'] = {'secoes': r3['n'], 'coef_SB': c3, 'ep': e3, 'coef_abstencao_1t': r3['coef']['abstencao_1t'],
               'soma_SB_nacional_27UFs': sSB_nac, 'soma_SB_no_universo': float(SB.sum()),
               'parcela_sem_biometria_no_cadastro': sSB_nac / float(meta['perfil_soma_brutos_todas_as_secoes']),
               'votos_implicados': c3 * sSB_nac, 'ic95_votos_implicados': [x * sSB_nac for x in ic(c3, e3)],
               'meia_largura_ic95_em_votos': Z95 * e3 * sSB_nac, 'a3_informa': bool(Z95 * e3 * sSB_nac < LIM10),
               'perfil_total_menos_aptos_1t_no_universo': int((Xp['ptot'] - Xp['apt1']).sum())}
    r3L = ctx3.reg(((Xp['L2'] - Xp['L1']) - (Xp['R2'] - Xp['R1'])).astype(float), [SB, A1], ['SB', 'abstencao_1t'])
    R['a3']['ao_lado_margem_sobre_SB'] = {'coef': r3L['coef']['SB'], 'ep': r3L['ep']['SB']}
    phi = LIM25 / float(SB.sum()); out = []
    for rep in range(NREP):
        k = rng.binomial(SB.astype(np.int64), min(phi, 1.0))
        rr = ctx3.reg((Xp['C2'] + k - Xp['C1']).astype(float), [SB, A1], ['SB', 'abstencao_1t']); out.append(rr['coef']['SB'])
    R['a3']['plantio'] = {'phi': phi, 'coef_plantado': resumo(out), 'subida_sobre_phi': float((np.mean(out) - c3) / phi),
                          'a3_enxerga': bool((np.mean(out) - c3) / phi >= 0.8)}
    grava('parcial_d46_observado.json', R)
    # ---- plantios de a1 e a2 ----
    pre = {nm: ctx.dm(c) for nm, c in zip(nomes, cols) if nm not in ('dNB_mu_menos_mulinha', 'dC_mulinha')}
    F0 = f_a1(X); base = le_a2(r)

    def mede(H2, C2, L2, R2):
        yy = ((L2 - X['L1']) - (R2 - X['R1'])).astype(float)
        rr = ctx.reg(yy, [(H2 - X['H1']).astype(float), (C2 - X['C1']).astype(float)] + cols[2:], nomes, pre=pre)
        Ff = float((H2 - X['H1']).sum() - X['H1'].sum() / X['C1'].sum() * (C2 - X['C1']).sum())
        return Ff, rr['coef']['dNB_mu_menos_mulinha'], rr['ep']['dNB_mu_menos_mulinha'], rr['coef']['dC_mulinha']

    P = {'observado_no_universo_do_a2': {'F': F0, 'mu_menos_mulinha': base['mu_menos_mulinha'], 'mulinha': base['mulinha_com_biometria']}}
    C2x, H2x, L2x, R2x = X['C2'], X['H2'], X['L2'], X['R2']
    p1 = np.clip(X['H1'] / np.maximum(X['C1'], 1), 0, 1); p2 = np.clip(H2x / np.maximum(C2x, 1), 0, 1)
    for nome, K, tipo in ((f'letra_concentrado_{LIM25}', LIM25, 'irr'), (f'letra_concentrado_{MARGEM}', MARGEM, 'irr'),
                          (f'letra_concentrado_{LIM10}', LIM10, 'irr'),
                          (f'inocente_I1_eleitor_real_concentrado_{LIM25}', LIM25, 'I1'), (f'inocente_I1_eleitor_real_uniforme_{LIM25}', LIM25, 'I1u'),
                          (f'inocente_I3_abstencao_pura_concentrado_{LIM25}', LIM25, 'I3'), (f'inocente_I3_abstencao_pura_uniforme_{LIM25}', LIM25, 'I3u'),
                          (f'espelho_a_favor_de_Flavio_concentrado_{LIM25}', LIM25, 'esp')):
        out = []
        for rep in range(NREP):
            if tipo in ('I3', 'I3u'):
                k = sort_concentrado(rng, K, R2x.astype(float)) if tipo == 'I3' else sort_uniforme(rng, K, R2x.astype(float))
                k = np.minimum(k, R2x); dh = np.minimum(rng.binomial(k, p2), H2x)
                out.append(mede(H2x - dh, C2x - k, L2x, R2x - k) + (int(k.sum()),)); continue
            k = sort_uniforme(rng, K, C2x.astype(float)) if tipo == 'I1u' else sort_concentrado(rng, K, C2x.astype(float))
            if tipo == 'irr': out.append(mede(H2x + k, C2x + k, L2x + k, R2x) + (int(k.sum()),))
            elif tipo in ('I1', 'I1u'): out.append(mede(H2x + rng.binomial(k, p1), C2x + k, L2x + k, R2x) + (int(k.sum()),))
            elif tipo == 'esp': out.append(mede(H2x + k, C2x + k, L2x, R2x + k) + (int(k.sum()),))
        o = np.array(out, float); Kef = float(o[:, 4].mean())
        P[nome] = {'K': K, 'K_efetivo': Kef, 'delta_F_sobre_K': float((o[:, 0] - F0).mean() / Kef), 'F_plantado': resumo(o[:, 0]),
                   'mu_menos_mulinha': resumo(o[:, 1]), 'ep': float(o[:, 2].mean()), 'mulinha': resumo(o[:, 3])}
        grava('parcial_d46_plantios.json', P)
        print('  plantio a2', nome, round(P[nome]['delta_F_sobre_K'], 3), round(P[nome]['mu_menos_mulinha']['media'], 3), round(P[nome]['mulinha']['media'], 3), flush=True)
    R['plantios'] = P
    # ---- placebo de 2022 ----
    m22 = universo_d41(B22)
    if m22.sum() > 1000:
        X22 = sub(B22, m22); tem = B22['H1'] >= 0; Xt = sub(B22, tem); icf, epf = boot_f(Xt, rng)
        c22 = Ctx(X22['loc'], X22['mun'], 1.0 / X22['apt1']); y22, co22, no22 = cols_a2(X22, somados=True)
        R['placebo_2022'] = {'a1': {'secoes_com_H': int(tem.sum()), 'F': f_a1(Xt), 'ic95': icf, 'variacao_NB': int((Xt['H2'] - Xt['H1']).sum()),
                                    'variacao_comp': int((Xt['C2'] - Xt['C1']).sum()), 'fatia_NB_1t': float(Xt['H1'].sum() / Xt['C1'].sum()),
                                    'fatia_NB_2t': float(Xt['H2'].sum() / Xt['C2'].sum()),
                                    'F_como_fracao_do_comparecimento_2t': f_a1(Xt) / float(Xt['C2'].sum())},
                             'a2_eliminados_somados': le_a2(c22.reg(y22, co22, no22))}
        R['a1']['F_2026_como_fracao_do_comparecimento_2t_27UFs'] = a1['so_27_UFs']['F'] / float(B['C2'][br].sum())
    # ---- a4: logs da amostra ----
    R['a4'] = roda_a4(B, rng)
    # ---- poder e veredito ----
    pl = P[f'letra_concentrado_{LIM25}']
    v_a1 = pl['delta_F_sobre_K'] >= 0.90; v_a2 = pl['mu_menos_mulinha']['media'] >= 0.5
    d = R['a2']['mu_menos_mulinha']; vi = R['a3']['votos_implicados']
    a3_vale = R['a3']['a3_informa'] and R['a3']['plantio']['a3_enxerga']
    sinal = bool((Fp >= LIM25 and d >= 0.5) or (a3_vale and vi >= LIM25))
    sem = bool(Fp <= LIM10 and d <= 0.2 and vi <= LIM10)
    if not (v_a1 and v_a2): ver = 'SEM PODER'
    elif sinal: ver = 'SINAL'
    elif sem and a3_vale: ver = 'SEM SINAL'
    else: ver = 'INCONCLUSIVO'
    R['poder'] = {'a1_enxerga': bool(v_a1), 'a2_enxerga': bool(v_a2), 'a3_enxerga': bool(R['a3']['plantio']['a3_enxerga']),
                  'a1_devolve': pl['delta_F_sobre_K'], 'a2_mu_menos_mulinha_plantado_25': pl['mu_menos_mulinha']['media'],
                  'a2_mu_menos_mulinha_plantado_10': P[f'letra_concentrado_{LIM10}']['mu_menos_mulinha']['media'],
                  'a2_mu_menos_mulinha_plantado_margem_inteira': P[f'letra_concentrado_{MARGEM}']['mu_menos_mulinha']['media']}
    letra = 'SINAL' if sinal else ('SEM SINAL' if (sem and R['a3']['a3_informa']) else 'INCONCLUSIVO')
    R['veredito'] = {'veredito': ver, 'pela_letra_do_registro_sem_a_regra_de_poder_F4': letra, 'F_nacional': Fp, 'mu_menos_mulinha': d, 'votos_implicados_a3': vi,
                     'condicoes_sinal': {'F>=1107548': bool(Fp >= LIM25), 'mu-mulinha>=0,5': bool(d >= 0.5), 'a3>=1107548': bool(vi >= LIM25)},
                     'condicoes_sem_sinal': {'F<=443019': bool(Fp <= LIM10), 'mu-mulinha<=0,2': bool(d <= 0.2), 'a3<=443019': bool(vi <= LIM10)},
                     'a3_informa_e_enxerga': bool(a3_vale),
                     'ic95_cruza_limiar': {'F': bool(a1['todas_as_pareadas_27UFs_e_exterior']['ic95'][1] > LIM10),
                                           'mu-mulinha': bool(R['a2']['ic95'][1] > 0.2),
                                           'a3': bool(R['a3']['ic95_votos_implicados'][1] > LIM10)}}
    grava('parcial_d46.json', R)
    return R


def le_logs(B):
    d = json.load(gzip.open(f'{TRAB}/logs_B2.json.gz', 'rt'))
    pos = {k: i for i, k in enumerate(B['chave'].tolist())}
    return d, pos


def roda_a4(B, rng):
    d, pos = le_logs(B)
    lin = []
    for k, v in d.items():
        if k not in pos or '1' not in v or '2' not in v: continue
        row = [pos[k]]
        for t in ('1', '2'):
            hab = [h for h in v[t]['hab'] if h[2] == 1]
            tard = [h for h in hab if h[0] >= 17 * 3600]
            row += [len(hab), sum(1 for h in hab if h[1] != 'B'), len(tard), sum(1 for h in tard if h[1] != 'B'),
                    sum(1 for h in tard if h[1] == 'M'), sum(1 for h in tard if h[1] == 'S')]
        lin.append(row)
    a = np.array(lin, dtype=np.int64)
    if len(a) == 0: return {'secoes': 0}
    idx = a[:, 0]; s = a[:, 1:].sum(0)
    lc, u = _cod(B['loc'][idx]); G = len(u)
    M = somas_mun(lc, G, *[a[:, j] for j in range(1, 13)])
    S = rng.multinomial(G, np.full(G, 1.0 / G), size=NBOOT).astype(float) @ M
    par = lambda S_: (S_[..., 9] / np.maximum(S_[..., 8], 1)) - (S_[..., 3] / np.maximum(S_[..., 2], 1))
    dn = lambda S_: S_[..., 9] - S_[..., 3]
    exc = lambda S_: S_[..., 9] - S_[..., 3] / np.maximum(S_[..., 2], 1) * S_[..., 8]
    r = {'secoes_com_os_dois_dias_no_log': int(len(a)), 'locais': int(G), 'amostra_nao_aleatoria_sem_extrapolar': True}
    for j, t in ((0, '1t'), (6, '2t')):
        r[t] = {'votos_computados': int(s[j]), 'sem_biometria': int(s[j + 1]), 'depois_das_17h': int(s[j + 2]),
                'sem_biometria_depois_das_17h': int(s[j + 3]), 'liberados_pelo_mesario_depois_das_17h': int(s[j + 4]),
                'eleitor_sem_biometria_no_cadastro_depois_das_17h': int(s[j + 5]),
                'parcela_sem_biometria_entre_os_tardios': float(s[j + 3] / max(s[j + 2], 1)),
                'parcela_sem_biometria_no_dia': float(s[j + 1] / max(s[j], 1))}
    r['diferenca_da_parcela_tardia_2t_menos_1t'] = float(par(s[None, :])[0]); r['ic95_diferenca_da_parcela'] = pct(par(S))
    r['diferenca_do_numero_2t_menos_1t'] = int(dn(s[None, :])[0]); r['ic95_diferenca_do_numero'] = pct(dn(S))
    r['excesso_tardio_sobre_a_parcela_do_1t'] = float(exc(s[None, :])[0]); r['ic95_excesso_tardio'] = pct(exc(S))
    r['margem_2t_das_secoes_da_amostra'] = int((B['L2'][idx] - B['R2'][idx]).sum())
    return r



# ----------------------------------------------------------------------------------------------------------------
# D2-6
# ----------------------------------------------------------------------------------------------------------------
def universo_d26(B):
    return (B['apur'] == 1) & (B['C1'] >= 50) & (B['C2'] >= 50) & (B['uf'] != 'ZZ')


def cols_elo(X):
    C1 = X['C1'].astype(float)
    y = ((X['L2'] - X['R2']) - (X['L1'] - X['R1'])) / C1
    cols = [(X['C2'] - X['C1']) / C1, X['O1'] / C1, (X['B1'] + X['N1']) / C1, X['L1'] / C1]
    return y, cols, ['dC', 'O1', 'BN1', 'L1']


def elo(ctx, y, flag, cols, nomes, teto, pre=None):
    r = ctx.reg(y, [flag.astype(float)] + cols, ['bandeira'] + nomes, pre=pre)
    if 'bandeira' not in r['coef']:
        return {'sem_variacao_dentro_dos_locais': True, 'teto': teto}
    g, e = ce(r, 'bandeira')
    return {'gama': g, 'ep': e, 'z': g / e, 'n': r['n'], 'teto': teto, 'V': g * teto, 'ic998_V': [x * teto for x in ic(g, e, Z998)],
            'ic95_V': [x * teto for x in ic(g, e)], 'coef_dC': r['coef'].get('dC')}


def roda_d26(B, agr1, agr2, rng, anos):
    R = {}
    n = len(B['uf']); br = B['uf'] != 'ZZ'
    lc = json.load(gzip.open(f'{TRAB}/locais2026.json.gz', 'rt'))['turnos']
    fed = {}; sec_ = {}; cj = {}
    for t in ('1', '2'):
        f = collections.defaultdict(int); q = collections.defaultdict(int); c = collections.defaultdict(list)
        for k, v in lc[t].items():
            if v[0] == 2:
                u, m, z, s = k.split('|'); kp = f'{u}|{m}|{z}|{v[1]}'; f[kp] += v[3]; q[kp] += v[4]; c[kp].append(int(s))
            else:
                f[k] += v[3]; q[k] += v[4]
        fed[t], sec_[t], cj[t] = f, q, c
    ch = B['chave'].tolist()
    fed1 = np.array([fed['1'].get(k, -1) for k in ch]); fed2 = np.array([fed['2'].get(k, -1) for k in ch])
    qs1 = np.array([sec_['1'].get(k, -1) for k in ch]); qs2 = np.array([sec_['2'].get(k, -1) for k in ch])
    am_loc = np.array([tuple(sorted(cj['1'].get(k, []))) != tuple(sorted(cj['2'].get(k, []))) for k in ch])
    am_bweb = np.array([a != b for a, b in zip(agr1, agr2)])
    ag_loc2 = np.array([len(cj['2'].get(k, [])) > 0 for k in ch])
    da = B['apt2'] - B['apt1']
    # ---------- T1 ----------
    T1 = {}
    for nome, m in (('27UFs_e_exterior', np.ones(n, bool)), ('so_27_UFs', br)):
        d = da[m]
        expl = (fed1[m] == B['apt1'][m]) & (fed2[m] == B['apt2'][m])
        T1[nome] = {
            'secoes_pareadas': int(m.sum()), 'secoes_com_aptos_diferentes': int((d != 0).sum()),
            'secoes_com_alta': int((d > 0).sum()), 'secoes_com_queda': int((d < 0).sum()),
            'soma_das_altas_max(apt2-apt1,0)': int(np.maximum(d, 0).sum()), 'espelho_soma_das_quedas_max(apt1-apt2,0)': int(np.maximum(-d, 0).sum()),
            'liquido': int(d.sum()), 'aptos_1t': int(B['apt1'][m].sum()), 'aptos_2t': int(B['apt2'][m].sum()),
            'distribuicao_da_diferenca': {'-11_ou_menos': int((d <= -11).sum()), '-10_a_-3': int(((d >= -10) & (d <= -3)).sum()),
                                          '-2_a_-1': int(((d >= -2) & (d <= -1)).sum()), '0': int((d == 0).sum()),
                                          '1_a_2': int(((d >= 1) & (d <= 2)).sum()), '3_a_10': int(((d >= 3) & (d <= 10)).sum()),
                                          '11_ou_mais': int((d >= 11).sum())},
            'maior_alta': int(d.max()), 'maior_queda': int(d.min()),
            'comparecimento_acima_dos_aptos_1t': int((B['C1'][m] > B['apt1'][m]).sum()),
            'comparecimento_acima_dos_aptos_2t': int((B['C2'][m] > B['apt2'][m]).sum()),
            'comparecimento_95_ou_mais_dos_aptos_1t': int((B['C1'][m] >= 0.95 * B['apt1'][m]).sum()),
            'comparecimento_95_ou_mais_dos_aptos_2t': int((B['C2'][m] >= 0.95 * B['apt2'][m]).sum()),
            'boletim_igual_ao_cadastro_de_locais_1t': int((fed1[m] == B['apt1'][m]).sum()),
            'boletim_igual_ao_cadastro_de_locais_2t': int((fed2[m] == B['apt2'][m]).sum()),
            'sem_linha_no_cadastro_1t': int((fed1[m] < 0).sum()), 'sem_linha_no_cadastro_2t': int((fed2[m] < 0).sum()),
            'soma_|boletim-cadastro|_1t': int(np.abs(B['apt1'][m] - fed1[m])[fed1[m] >= 0].sum()),
            'soma_|boletim-cadastro|_2t': int(np.abs(B['apt2'][m] - fed2[m])[fed2[m] >= 0].sum()),
            'secoes_com_alta_explicada_pelo_cadastro': int(((d > 0) & expl).sum()),
            'soma_das_altas_explicadas_pelo_cadastro': int(np.maximum(d, 0)[expl].sum()),
            'soma_das_altas_SEM_explicacao': int(np.maximum(d, 0)[~expl].sum()),
            'soma_das_quedas_SEM_explicacao': int(np.maximum(-d, 0)[~expl].sum()),
            'QT_ELEITOR_SECAO_igual_nos_dois_turnos': int((qs1[m] == qs2[m]).sum()),
            'soma_QT_ELEITOR_SECAO_1t': int(qs1[m][qs1[m] >= 0].sum()), 'soma_QT_ELEITOR_SECAO_2t': int(qs2[m][qs2[m] >= 0].sum()),
            'soma_federal_1t': int(fed1[m][fed1[m] >= 0].sum()), 'soma_federal_2t': int(fed2[m][fed2[m] >= 0].sum())}
    ac = np.flatnonzero((B['C1'] > B['apt1']) | (B['C2'] > B['apt2']))
    T1['lista_comparecimento_acima_dos_aptos'] = [{'chave': str(B['chave'][i]), 'aptos_1t': int(B['apt1'][i]), 'comp_1t': int(B['C1'][i]),
                                                   'aptos_2t': int(B['apt2'][i]), 'comp_2t': int(B['C2'][i])} for i in ac[:200]]
    # plantio de T1: 1 apto a mais em 1% das seções
    idx = rng.choice(n, size=int(round(0.01 * n)), replace=False); d2 = da.copy(); d2[idx] += 1
    T1['plantio_1_apto_em_1pct'] = {'secoes_plantadas': int(len(idx)), 'soma_das_altas_antes': int(np.maximum(da, 0).sum()),
                                    'soma_das_altas_depois': int(np.maximum(d2, 0).sum()),
                                    'secoes_diferentes_antes': int((da != 0).sum()), 'secoes_diferentes_depois': int((d2 != 0).sum()),
                                    'ja_estavam_em_queda_entre_as_plantadas': int((da[idx] < 0).sum())}
    T1['historico_secoes_com_aptos_diferentes'] = {}
    for ano, (Ba, _) in anos.items():
        mm = Ba['uf'] != 'ZZ'; dd = Ba['apt2'] - Ba['apt1']
        T1['historico_secoes_com_aptos_diferentes'][str(ano)] = {
            'todas': int((dd != 0).sum()), 'so_27_UFs': int((dd[mm] != 0).sum()), 'pareadas': int(len(dd)),
            'soma_das_altas': int(np.maximum(dd, 0).sum()), 'soma_das_quedas': int(np.maximum(-dd, 0).sum()),
            'urna_diferente': int((Ba['urna1'] != Ba['urna2']).sum())}
    R['T1'] = T1
    # ---------- bandeiras ----------
    Fl = {'U': B['urna1'] != B['urna2'], 'CT': B['dc2'] >= 20261005, 'CD': B['dc2'] == 20261025, 'AG': B['nagr2'] > 0,
          'AM': am_bweb | am_loc}
    extra = {'AP_mais': da > 0, 'AP_menos': da < 0}
    zc, zu = _cod(B['zona']); par = zc * 10 ** 8 + B['dc1']
    u_, cnt = np.unique(par, return_counts=True); uz = u_ // 10 ** 8; ud = u_ % 10 ** 8
    nzs = np.bincount(zc); cer = cnt >= 0.05 * nzs[uz]
    ult = np.zeros(len(zu), dtype=np.int64); np.maximum.at(ult, uz[cer], ud[cer])
    c1t = (B['dc1'] > ult[zc]) & (B['dc1'] <= 20261004)
    R['bandeiras_contagem'] = {k: {'secoes_27UFs': int((v & br).sum()), 'secoes_exterior': int((v & ~br).sum()),
                                   'teto_27UFs': int(B['C2'][v & br].sum()), 'teto_com_exterior': int(B['C2'][v].sum())}
                               for k, v in {**Fl, **extra}.items()}
    R['bandeiras_contagem']['AM_pelo_bweb'] = int((am_bweb & br).sum()); R['bandeiras_contagem']['AM_pelo_arquivo_de_locais'] = int((am_loc & br).sum())
    R['bandeiras_contagem']['AG_pelo_arquivo_de_locais_2t'] = int((ag_loc2 & br).sum())
    R['bandeiras_contagem']['C1T_carga_tardia_do_1t'] = int((c1t & br).sum())
    R['bandeiras_contagem']['datas_de_carga_2t_de_05_10_em_diante'] = dict(collections.Counter(B['dc2'][(B['dc2'] >= 20261005) & br].tolist()).most_common(30))
    R['bandeiras_contagem']['U_e_CT'] = int((Fl['U'] & Fl['CT'] & br).sum()); R['bandeiras_contagem']['U_sem_CT'] = int((Fl['U'] & ~Fl['CT'] & br).sum())
    R['bandeiras_contagem']['CT_sem_U'] = int((~Fl['U'] & Fl['CT'] & br).sum())
    m = universo_d26(B); X = sub(B, m); ctx = Ctx(X['loc'], X['mun'], X['C1'])
    y, cols, nomes = cols_elo(X); C1f = X['C1'].astype(float)
    yL = (X['L2'] - X['L1']) / C1f; yR = (X['R2'] - X['R1']) / C1f; yBN = ((X['B2'] + X['N2']) - (X['B1'] + X['N1'])) / C1f
    R['universo_do_elo'] = {'secoes': int(m.sum()), 'usadas_na_regressao': ctx.n, 'locais': ctx.ng}
    m2 = m & (np.abs(da) <= 2); X2 = sub(B, m2); ctx2 = Ctx(X2['loc'], X2['mun'], X2['C1']); y2, cols2, _ = cols_elo(X2)
    E = {}
    for nm, fl in {**Fl, **extra}.items():
        teto = int(B['C2'][fl & br].sum()); f = fl[m]
        e = elo(ctx, y, f, cols, nomes, teto)
        e['secoes_marcadas_no_universo'] = int(f.sum()); e['secoes_marcadas_usadas'] = int(f[ctx.ok].sum())
        e['C1_marcadas_no_universo'] = int(X['C1'][f].sum())
        if 'gama' in e:
            for rot, yy in (('espelho_ganho_de_Lula', yL), ('espelho_ganho_de_Flavio', yR), ('desfecho_placebo_BN', yBN)):
                rr = ctx.reg(yy, [f.astype(float)] + cols, ['bandeira'] + nomes); e[rot] = {'gama': rr['coef']['bandeira'], 'ep': rr['ep']['bandeira']}
            e2 = elo(ctx2, y2, fl[m2], cols2, nomes, teto)
            e['sensibilidade_com_filtro_de_aptos'] = {k: e2.get(k) for k in ('gama', 'ep', 'V', 'n')}
            medY = float(np.average(y[f], weights=C1f[f])) if f.any() else None
            e['bruto_y_medio_marcadas'] = medY; e['bruto_y_medio_universo'] = float(np.average(y, weights=C1f))
        E[nm] = e
    rr = ctx.reg(y, [(da[m] / C1f)] + cols, ['dose_aptos'] + nomes)
    E['dose_(apt2-apt1)/C1'] = {'gama': rr['coef']['dose_aptos'], 'ep': rr['ep']['dose_aptos'],
                               'votos_de_margem_por_apto_a_mais_x_soma_das_altas': rr['coef']['dose_aptos'] * float(np.maximum(da[br], 0).sum())}
    # U com modelo da urna do 2º turno como controle
    mod = np.array([modelo_urna(int(s), 2026) or 'fora' for s in X['urna2']]); cm_ = []; nm_ = []
    for mo in sorted(set(mod.tolist())):
        if mo != 'UE2020': cm_.append((mod == mo).astype(float)); nm_.append('modelo_' + mo)
    rr = ctx.reg(y, [Fl['U'][m].astype(float)] + cols + cm_, ['bandeira'] + nomes + nm_)
    E['U']['com_modelo_da_urna'] = {'gama': rr['coef']['bandeira'], 'ep': rr['ep']['bandeira'], 'modelos': dict(collections.Counter(mod.tolist()))}
    porUF = {}
    for u in UFS:
        a = X['uf'] == u
        if (Fl['U'][m] & a).sum() < 30: continue
        Xa = sub(X, a); ca = Ctx(Xa['loc'], Xa['mun'], Xa['C1']); ya, cola, na = cols_elo(Xa)
        tet = int(B['C2'][Fl['U'] & (B['uf'] == u)].sum())
        porUF[u] = {k: v for k, v in elo(ca, ya, Fl['U'][m][a], cola, na, tet).items() if k in ('gama', 'ep', 'z', 'teto', 'V', 'sem_variacao_dentro_dos_locais')}
    E['U']['por_UF'] = porUF
    # placebo: troca do 1º turno em corte dentro do prédio
    y1 = (X['L1'] - X['R1']) / C1f
    rr = ctx.reg(y1, [c1t[m].astype(float)], ['C1T'])
    E['placebo_C1T_corte_do_1t'] = {'gama': rr['coef'].get('C1T'), 'ep': rr['ep'].get('C1T'), 'secoes_marcadas': int(c1t[m].sum()),
                                    'teto_C1': int(B['C1'][c1t & br].sum())}
    rr = ctx.reg(y1, [Fl['U'][m].astype(float)], ['U'])
    E['placebo_U_contra_o_nivel_do_1t'] = {'gama': rr['coef'].get('U'), 'ep': rr['ep'].get('U')}
    R['elo'] = E
    grava('parcial_d26_observado.json', R)
    # ---------- placebo da bandeira U em outros anos ----------
    PA = {}
    for ano, (Ba, _) in anos.items():
        ma = universo_d26(Ba); Xa = sub(Ba, ma); ca = Ctx(Xa['loc'], Xa['mun'], Xa['C1']); ya, cola, na = cols_elo(Xa)
        fa = Xa['urna1'] != Xa['urna2']; tet = int(Ba['C2'][(Ba['urna1'] != Ba['urna2']) & (Ba['uf'] != 'ZZ')].sum())
        e = elo(ca, ya, fa, cola, na, tet); e['secoes_marcadas_no_universo'] = int(fa.sum()); e['secoes_universo'] = int(ma.sum())
        e['fracao_de_secoes_com_urna_trocada'] = float(fa.mean())
        PA[str(ano)] = e
    R['placebo_U_outros_anos'] = PA
    # ---------- plantios ----------
    P = {}
    pre = {nm: ctx.dm(c) for nm, c in zip(nomes, cols) if nm != 'dC'}
    L2, R2_, C2 = B['L2'], B['R2'], B['C2']
    for nm, fl in Fl.items():
        teto = int(C2[fl & br].sum())
        if teto < LIM10 or 'gama' not in E[nm]:
            P[nm] = {'nao_plantado': 'teto abaixo de 443.019 ou bandeira sem variação dentro dos locais', 'teto': teto}; continue
        P[nm] = {}
        for K in (LIM10, LIM25):
            Kp = min(K, teto); out = []; outi = []
            for rep in range(NREP):
                k = np.zeros(n, dtype=np.int64); ii = np.flatnonzero(fl & br)
                k[ii] = rng.multinomial(Kp, C2[ii] / C2[ii].sum()); km = k[m]
                yy = (((X['L2'] + km) - X['R2']) - (X['L1'] - X['R1'])) / C1f
                e = elo(ctx, yy, fl[m], [((X['C2'] + km) - X['C1']) / C1f] + cols[1:], nomes, teto + Kp, pre=pre)
                out.append((e['V'], e['gama'], e['ep'], e['ic998_V'][0], e['ic998_V'][1]))
                pL = np.clip(X['L2'] / np.maximum(X['L2'] + X['R2'], 1), 0, 1); kl = rng.binomial(km, pL)
                yy = (((X['L2'] + kl) - (X['R2'] + km - kl)) - (X['L1'] - X['R1'])) / C1f
                e = elo(ctx, yy, fl[m], [((X['C2'] + km) - X['C1']) / C1f] + cols[1:], nomes, teto + Kp, pre=pre)
                outi.append((e['V'], e['gama']))
            o = np.array(out); oi = np.array(outi); V0 = E[nm]['V']
            P[nm][str(K)] = {'K_plantado': Kp, 'limitado_pelo_teto': bool(Kp < K), 'V_plantado': resumo(o[:, 0]), 'gama_plantado': resumo(o[:, 1]),
                             'rho': float((o[:, 0].mean() - V0) / Kp), 'ep_gama': float(o[:, 2].mean()),
                             'rho_com_o_teto_de_antes_do_plantio': float((o[:, 1].mean() * teto - V0) / Kp),
                             'meia_largura_ic998_V': float(((o[:, 4] - o[:, 3]) / 2).mean()),
                             'efeito_plantado_sobre_meia_largura': float((o[:, 0].mean() - V0) / ((o[:, 4] - o[:, 3]) / 2).mean()),
                             'inocente_eleitor_real_que_divide_o_voto': {'V': resumo(oi[:, 0]), 'rho': float((oi[:, 0].mean() - V0) / Kp)}}
        grava('parcial_d26_plantios.json', P)
        print('  plantio bandeira', nm, {k: round(v['rho'], 3) for k, v in P[nm].items() if isinstance(v, dict)}, flush=True)
    R['plantios'] = P
    # ---------- CG na amostra de logs ----------
    try:
        d, pos = le_logs(B)
        cg2 = np.zeros(n, bool); cg1 = np.zeros(n, bool); am2 = np.zeros(n, bool); am1 = np.zeros(n, bool); det = collections.Counter()
        for k, v in d.items():
            if k not in pos: continue
            i = pos[k]
            for t, cg, am in (('1', cg1, am1), ('2', cg2, am2)):
                r = v.get(t)
                if r is None: continue
                am[i] = True
                a = r['cont'] > 0; b = r['ini_vota'] >= 2; c = r['scue_hora'] > 0; e_ = len(r['urnas']) >= 2
                if a: det[f'contingencia_{t}t'] += 1
                if b: det[f'vota_iniciado_2_ou_mais_{t}t'] += 1
                if c: det[f'scue_data_e_hora_{t}t'] += 1
                if e_: det[f'mais_de_uma_urna_{t}t'] += 1
                cg[i] = a or b or c or e_
        ms = m & am2; Xs = sub(B, ms); cs = Ctx(Xs['loc'], Xs['mun'], Xs['C1']); ys, cols_s, ns = cols_elo(Xs); C1s = Xs['C1'].astype(float)
        tet = int(B['C2'][cg2 & am2].sum()); e = elo(cs, ys, cg2[ms], cols_s, ns, tet)
        e['secoes_da_amostra_no_universo'] = int(ms.sum()); e['secoes_marcadas'] = int(cg2[ms].sum()); e['detalhe'] = dict(det)
        e['comparecimento_2t_da_amostra'] = int(B['C2'][am2].sum()); e['margem_2t_da_amostra'] = int((B['L2'][am2] - B['R2'][am2]).sum())
        for rot, yy in (('espelho_ganho_de_Lula', (Xs['L2'] - Xs['L1']) / C1s), ('espelho_ganho_de_Flavio', (Xs['R2'] - Xs['R1']) / C1s),
                        ('desfecho_placebo_BN', ((Xs['B2'] + Xs['N2']) - (Xs['B1'] + Xs['N1'])) / C1s)):
            rr = cs.reg(yy, [cg2[ms].astype(float)] + cols_s, ['bandeira'] + ns)
            if 'bandeira' in rr['coef']: e[rot] = {'gama': rr['coef']['bandeira'], 'ep': rr['ep']['bandeira']}
        so_cont = np.zeros(n, bool)
        for k, v in d.items():
            if k in pos and v.get('2') and (v['2']['cont'] > 0 or len(v['2']['urnas']) >= 2): so_cont[pos[k]] = True
        e['so_contingencia_ou_duas_urnas'] = {k: v for k, v in elo(cs, ys, so_cont[ms], cols_s, ns, int(B['C2'][so_cont].sum())).items()
                                              if k in ('gama', 'ep', 'z', 'teto', 'V', 'sem_variacao_dentro_dos_locais')}
        e['so_contingencia_ou_duas_urnas']['secoes'] = int(so_cont[ms].sum())
        ms1 = m & am1; Xs1 = sub(B, ms1); cs1 = Ctx(Xs1['loc'], Xs1['mun'], Xs1['C1'])
        rr = cs1.reg((Xs1['L1'] - Xs1['R1']) / Xs1['C1'].astype(float), [cg1[ms1].astype(float)], ['CG1'])
        e['placebo_CG_do_1t_contra_o_voto_do_1t'] = {'gama': rr['coef'].get('CG1'), 'ep': rr['ep'].get('CG1'), 'secoes_marcadas': int(cg1[ms1].sum())}
        # plantio na amostra: inserir em CG o equivalente a 10% e 25% da margem da amostra
        Pcg = {}
        ii = np.flatnonzero(cg2[ms]); marg_am = abs(e['margem_2t_da_amostra'])
        pre_s = {nm: cs.dm(c) for nm, c in zip(ns, cols_s) if nm != 'dC'}
        for fr in (0.10, 0.25):
            Kp = int(round(fr * marg_am)); out = []
            if len(ii) == 0 or 'gama' not in e: break
            for rep in range(NREP):
                k = np.zeros(int(ms.sum()), dtype=np.int64); k[ii] = rng.multinomial(Kp, Xs['C2'][ii] / Xs['C2'][ii].sum())
                yy = (((Xs['L2'] + k) - Xs['R2']) - (Xs['L1'] - Xs['R1'])) / C1s
                ee = elo(cs, yy, cg2[ms], [((Xs['C2'] + k) - Xs['C1']) / C1s] + cols_s[1:], ns, tet + Kp, pre=pre_s); out.append((ee['V'], ee['ic998_V'][1] - ee['V']))
            o = np.array(out)
            Pcg[f'{int(fr * 100)}pct_da_margem_da_amostra'] = {'K': Kp, 'rho': float((o[:, 0].mean() - e['V']) / Kp),
                                                             'efeito_sobre_meia_largura': float((o[:, 0].mean() - e['V']) / o[:, 1].mean())}
        e['plantio_na_amostra'] = Pcg
        R['CG_amostra_de_logs'] = e
    except FileNotFoundError:
        R['CG_amostra_de_logs'] = {'nao_rodado': 'logs_B2.json.gz ausente (rodar o modo logs)'}
    # ---------- veredito ----------
    V = {}; algum_sinal = False; algum_sem_poder = False; todos_sem = True
    gU22 = PA.get('2022', {}).get('gama')
    for nm in Fl:
        e = E[nm]; teto = e['teto']; pl = P.get(nm, {})
        if teto < LIM10:
            V[nm] = {'rotulo': 'SEM SINAL', 'motivo': 'teto abaixo de 443.019', 'teto': teto}; continue
        if 'gama' not in e:
            V[nm] = {'rotulo': 'SEM PODER', 'motivo': 'bandeira sem variação dentro dos locais; teto acima do limiar', 'teto': teto}
            algum_sem_poder = True; todos_sem = False; continue
        p10 = pl.get(str(LIM10), {}); rho = p10.get('rho', 0.0); enx = rho >= 0.5 and p10.get('efeito_plantado_sobre_meia_largura', 0) >= 1.0
        lo, hi = e['ic998_V']
        sinal_num = e['V'] >= LIM25 and lo >= LIM10; sinal_esp = e['V'] <= -LIM25 and hi <= -LIM10
        plc = True
        if nm == 'U' and gU22 is not None: plc = abs(gU22) < abs(e['gama']) / 3
        hi_corr = hi / rho if 0 < rho < 0.9 else hi
        if not enx: rot = 'SEM PODER'; algum_sem_poder = True; todos_sem = False
        elif (sinal_num or sinal_esp) and plc: rot = 'SINAL' if sinal_num else 'SINAL NO SENTIDO DE FLÁVIO'; algum_sinal = True; todos_sem = False
        elif hi < LIM10 and hi_corr < LIM10 and lo > -LIM10: rot = 'SEM SINAL'
        else: rot = 'INCONCLUSIVO'; todos_sem = False
        V[nm] = {'rotulo': rot, 'teto': teto, 'V': e['V'], 'ic998_V': e['ic998_V'], 'rho_plantio_10pct': rho, 'enxerga': bool(enx),
                 'limite_superior_corrigido_por_rho': hi_corr, 'placebo_2022_menor_que_um_terco': bool(plc) if nm == 'U' else None}
    alt = T1['so_27_UFs']['soma_das_altas_max(apt2-apt1,0)']; alt_se = T1['so_27_UFs']['soma_das_altas_SEM_explicacao']
    t1_sinal = alt >= LIM10 and alt_se >= LIM10; t1_sem = alt < LIM10
    V['T1'] = {'rotulo': 'SINAL' if t1_sinal else ('SEM SINAL' if t1_sem else 'INCONCLUSIVO'), 'soma_das_altas': alt, 'soma_das_altas_sem_explicacao': alt_se,
               'achado_local_comparecimento_acima_dos_aptos': T1['so_27_UFs']['comparecimento_acima_dos_aptos_1t'] + T1['so_27_UFs']['comparecimento_acima_dos_aptos_2t']}
    if algum_sinal or t1_sinal: ver = 'SINAL'
    elif algum_sem_poder: ver = 'SEM PODER'
    elif todos_sem and t1_sem: ver = 'SEM SINAL'
    else: ver = 'INCONCLUSIVO'
    R['veredito'] = {'veredito': ver, 'por_bandeira': V}
    grava('parcial_d26.json', R)
    return R




# ----------------------------------------------------------------------------------------------------------------
# EXPLORATÓRIO (escrito depois de ver os resultados do ensaio; não decide nada)
# ----------------------------------------------------------------------------------------------------------------
def exploratorio_efeito_fixo_mais_largo(B):
    """A equipe vermelha pede que todo teste com efeito fixo de local seja repetido com efeito fixo de município ou
    de zona, porque um desvio igual em todas as urnas do prédio some na média do local. Não estava no docstring."""
    out = {}
    m = universo_d21(B); U = sub(B, m); y, cols, nomes = cols_s3(U); C1f = U['C1'].astype(float)
    yL = (U['L2'] - U['L1']) / C1f; yR = (U['R2'] - U['R1']) / C1f
    for rot, g in (('local', U['loc']), ('zona', U['zona']), ('municipio', U['mun']), ('UF', U['uf'])):
        c = Ctx(g, U['mun'], U['C1']); r = c.reg(y, cols, nomes); rl = c.reg(yL, cols, nomes); rr = c.reg(yR, cols, nomes)
        out[f'S3_efeito_fixo_de_{rot}'] = {'gama': r['coef']['x_dH'], 'ep': r['ep']['x_dH'], 'n': r['n'], 'gama_L': rl['coef']['x_dH'],
                                           'ep_L': rl['ep']['x_dH'], 'gama_R': rr['coef']['x_dH'], 'ep_R': rr['ep']['x_dH']}
    a = np.isin(U['uf'], UF5); Ua = sub(U, a); ya, ca_, na = cols_s3(Ua); C1a = Ua['C1'].astype(float)
    for rot, g in (('local', Ua['loc']), ('municipio', Ua['mun'])):
        c = Ctx(g, Ua['mun'], Ua['C1']); r = c.reg(ya, ca_, na)
        rl = c.reg((Ua['L2'] - Ua['L1']) / C1a, ca_, na); rr = c.reg((Ua['R2'] - Ua['R1']) / C1a, ca_, na)
        out[f'S3_nas_5_UFs_efeito_fixo_de_{rot}'] = {'gama': r['coef']['x_dH'], 'ep': r['ep']['x_dH'], 'n': r['n'], 'gama_L': rl['coef']['x_dH'],
                                                     'ep_L': rl['ep']['x_dH'], 'gama_R': rr['coef']['x_dH'], 'ep_R': rr['ep']['x_dH']}
    # plantio concentrado de 10% com efeito fixo de município, para saber o que esse desenho enxerga
    rng = np.random.default_rng(SEMENTE + 7); c = Ctx(U['mun'], U['mun'], U['C1']); gs = []
    for rep in range(5):
        k = sort_concentrado(rng, LIM10, U['C2'].astype(float))
        yy = (((U['L2'] + k) - U['R2']) - (U['L1'] - U['R1'])) / C1f
        r = c.reg(yy, [(U['H2'] + k - U['H1']) / C1f, (U['C2'] + k - U['C1']) / C1f] + cols[2:], nomes); gs.append(r['coef']['x_dH'])
    out['S3_efeito_fixo_de_municipio_plantio_concentrado_10pct'] = resumo(gs)
    # prédios inteiros: 5% dos LOCAIS sorteados recebem os votos (o que o efeito fixo de local não vê)
    lc, lu = _cod(U['loc']); res = {}
    for rot, g in (('local', U['loc']), ('municipio', U['mun'])):
        c = Ctx(g, U['mun'], U['C1']); gs = []
        for rep in range(5):
            esc = rng.choice(len(lu), size=int(round(0.05 * len(lu))), replace=False); onde = np.isin(lc, esc)
            k = np.zeros(len(lc), dtype=np.int64); ii = np.flatnonzero(onde); k[ii] = rng.multinomial(LIM10, U['C2'][ii] / U['C2'][ii].sum())
            yy = (((U['L2'] + k) - U['R2']) - (U['L1'] - U['R1'])) / C1f
            r = c.reg(yy, [(U['H2'] + k - U['H1']) / C1f, (U['C2'] + k - U['C1']) / C1f] + cols[2:], nomes); gs.append(r['coef']['x_dH'])
        res[f'efeito_fixo_de_{rot}'] = resumo(gs)
    out['plantio_de_10pct_em_5pct_dos_PREDIOS_inteiros_gama'] = res
    # D4-6 a2 e bandeiras do D2-6 com efeito fixo de município
    m4 = universo_d41(B); X = sub(B, m4); X['_elim_nomes'] = [str(j) for j in range(X['elim'].shape[1])]
    y4, c4, n4 = cols_a2(X)
    for rot, g in (('municipio', X['mun']), ('zona', X['zona'])):
        out[f'a2_efeito_fixo_de_{rot}'] = {k: v for k, v in le_a2(Ctx(g, X['mun'], 1.0 / X['apt1']).reg(y4, c4, n4)).items()
                                           if k in ('mu_menos_mulinha', 'ep', 'mulinha_com_biometria', 'ep_mulinha', 'n')}
    m6 = universo_d26(B); X6 = sub(B, m6); y6, c6, n6 = cols_elo(X6); br = B['uf'] != 'ZZ'
    Fl = {'U': B['urna1'] != B['urna2'], 'CT': B['dc2'] >= 20261005, 'AG': B['nagr2'] > 0}
    for rot, g in (('municipio', X6['mun']), ('zona', X6['zona'])):
        c = Ctx(g, X6['mun'], X6['C1'])
        for nm, fl in Fl.items():
            e = elo(c, y6, fl[m6], c6, n6, int(B['C2'][fl & br].sum()))
            out[f'bandeira_{nm}_efeito_fixo_de_{rot}'] = {k: e.get(k) for k in ('gama', 'ep', 'z', 'V', 'ic998_V')}
    return out


def exploratorio_por_uf(R, B):
    """Onde está a sobra de liberações: acompanha a virada? Correlações entre UFs (27 pontos), só descritivo."""
    d = R['D2-1']['S1_por_UF']; m = universo_d21(B); linhas = []
    for u in UFS:
        a = m & (B['uf'] == u)
        l1, r1, l2, r2, c1 = [float(B[k][a].sum()) for k in ('L1', 'R1', 'L2', 'R2', 'C1')]
        v = d[u]
        linhas.append({'uf': u, 'q_2026': v['q'], 'q_2022': v['q_ref'], 'razao_q2026_sobre_q2022': v['q'] / v['q_ref'],
                       'fatia_de_Lula_2t': l2 / (l2 + r2), 'ganho_de_margem_por_C1': ((l2 - r2) - (l1 - r1)) / c1,
                       'variacao_do_comparecimento_por_C1': v['variacao_C'] / v['soma_C1'],
                       'perda_de_Flavio_por_R1': (r1 - r2) / r1, 'E_bruto': v['E_bruto_qref1'], 'E_qref_UF': v['E']})
    def corr(a, b, postos=False):
        x = np.array([l[a] for l in linhas], float); y = np.array([l[b] for l in linhas], float)
        if postos: x = np.argsort(np.argsort(x)).astype(float); y = np.argsort(np.argsort(y)).astype(float)
        return float(np.corrcoef(x, y)[0, 1])
    cs = {}
    for a in ('q_2026', 'razao_q2026_sobre_q2022', 'q_2022'):
        for b in ('fatia_de_Lula_2t', 'ganho_de_margem_por_C1', 'variacao_do_comparecimento_por_C1', 'perda_de_Flavio_por_R1'):
            cs[f'{a} x {b}'] = {'pearson': corr(a, b), 'spearman': corr(a, b, True)}
    return {'n_ufs': len(linhas), 'correlacoes': cs, 'linhas': linhas,
            'nota': 'com 27 pontos, |r| acima de 0,38 passa de 5% bilateral; são 12 correlações, uma passaria por acaso a cada 20'}


def exploratorio_listas(B):
    """Listas para conferência de ata: seções com carga da urna no próprio dia 25/10 e as de maior comparecimento."""
    br = B['uf'] != 'ZZ'; cd = np.flatnonzero((B['dc2'] == 20261025) & br)
    f = lambda i: {'chave': str(B['chave'][i]), 'urna_1t': int(B['urna1'][i]), 'urna_2t': int(B['urna2'][i]), 'aptos_2t': int(B['apt2'][i]),
                   'comp_1t': int(B['C1'][i]), 'comp_2t': int(B['C2'][i]), 'H1': int(B['H1'][i]), 'H2': int(B['H2'][i]),
                   'margem_1t_L_menos_R': int(B['L1'][i] - B['R1'][i]), 'margem_2t_L_menos_R': int(B['L2'][i] - B['R2'][i])}
    t2 = np.where(B['apt2'] > 0, B['C2'] / np.maximum(B['apt2'], 1), 0); o = np.argsort(-t2)
    o = [i for i in o[:400] if br[i] and B['apt2'][i] >= 50][:20]
    # zonas com maior sobra bruta de liberações (taxa do 1º turno da própria zona), para pedido de atas e cadernos
    m = universo_d21(B); zc, zu = _cod(B['zona'][m]); G = len(zu)
    S = somas_mun(zc, G, B['H1'][m], B['C1'][m], B['H2'][m], B['C2'][m], (B['L2'] - B['R2'])[m] - (B['L1'] - B['R1'])[m])
    Ez = S[:, 2] - S[:, 0] / np.maximum(S[:, 1], 1) * S[:, 3]
    def zl(g): return {'zona': str(zu[g]), 'sobra_bruta': float(Ez[g]), 'H1': int(S[g, 0]), 'C1': int(S[g, 1]), 'H2': int(S[g, 2]), 'C2': int(S[g, 3]),
                       'q': float((S[g, 2] / S[g, 3]) / (S[g, 0] / S[g, 1])) if S[g, 0] > 0 else None, 'variacao_da_margem': int(S[g, 4])}
    ordem = np.argsort(-Ez); uf5 = np.array([z.split('|')[0] in UF5 for z in zu])
    return {'carga_no_dia_25_10': [f(i) for i in cd], 'vinte_maiores_comparecimentos_2t_com_50_aptos_ou_mais': [dict(f(i), taxa=float(t2[i])) for i in o],
            'vinte_zonas_de_maior_sobra_bruta_de_liberacoes_no_pais': [zl(g) for g in ordem[:20]],
            'quinze_zonas_de_maior_sobra_bruta_nas_5_UFs': [zl(g) for g in ordem if uf5[g]][:15],
            'zonas_no_universo': int(G), 'zonas_com_sobra_positiva': int((Ez > 0).sum()), 'soma_das_sobras_positivas_por_zona': float(Ez[Ez > 0].sum())}


def exploratorio_leitura_calibrada(R):
    """Compara o observado com o que cada plantio produz (leitura posterior, não é o critério do registro)."""
    d = R['D2-1']; p = d['plantios']; g, eg = d['S3']['gama'], d['S3']['ep']
    a2 = R['D4-6a']['a2']; pa = R['D4-6a']['plantios']
    def dist(obs, ep, alvo): return (alvo - obs) / ep
    return {
        'S3_gama_observado': g, 'S3_ep': eg,
        'S3_gama_com_10pct_concentrado': p[f'irregularidade_concentrado_{LIM10}']['gama']['media'],
        'S3_distancia_em_ep_ate_o_plantio_de_10pct_concentrado': dist(g, eg, p[f'irregularidade_concentrado_{LIM10}']['gama']['media']),
        'S3_gama_com_25pct_concentrado': p[f'irregularidade_concentrado_{LIM25}']['gama']['media'],
        'S3_gama_com_25pct_uniforme': p[f'irregularidade_uniforme_{LIM25}']['gama']['media'],
        'S3_distancia_em_ep_ate_o_plantio_de_25pct_uniforme': dist(g, eg, p[f'irregularidade_uniforme_{LIM25}']['gama']['media']),
        'a2_observado': a2['mu_menos_mulinha'], 'a2_ep': a2['ep'],
        'a2_com_10pct_concentrado': pa[f'letra_concentrado_{LIM10}']['mu_menos_mulinha']['media'],
        'a2_distancia_em_ep_ate_o_plantio_de_10pct': dist(a2['mu_menos_mulinha'], a2['ep'], pa[f'letra_concentrado_{LIM10}']['mu_menos_mulinha']['media']),
        }




# ----------------------------------------------------------------------------------------------------------------
# EXPLORATÓRIO: SEGUNDO ANO DE REFERÊNCIA PARA q (eleição municipal de 2024, cidades com 2º turno)
# Decidido depois de ver que o veredito do D2-1 depende inteiro do q de 2022. Não está no registro e não decide nada.
# ----------------------------------------------------------------------------------------------------------------
BASE24 = 'https://cdn.tse.jus.br/estatistica/sead/eleicoes/eleicoes2024/buweb/'
SUF24 = {1: '091020241636', 2: '281020241046'}


def exploratorio_baixar2024(minutos=25):
    """bweb de 2024 em fluxo: 2º turno de todas as UFs que tiverem arquivo; depois o 1º turno dessas UFs, do menor para
    o maior, guardando só as seções dos municípios com 2º turno. Uma linha de estrutura por seção (primeira de
    Prefeito). Para em 429/403/407 e quando passar do tempo dado. 1,2 s entre pedidos."""
    import ssl, urllib.request, urllib.error
    pasta = f'{TRAB}/dl_bweb2024'; os.makedirs(pasta, exist_ok=True)
    ctx = ssl.create_default_context(cafile='/root/.ccr/ca-bundle.crt'); ua = {'User-Agent': 'pesquisa-dados-abertos'}; ult = [0.0]
    t0 = time.time()

    def abrir(url, extra=None, metodo='GET'):
        d = 1.2 - (time.time() - ult[0])
        if d > 0: time.sleep(d)
        ult[0] = time.time()
        req = urllib.request.Request(url, method=metodo, headers=dict(ua, **(extra or {})))
        try:
            return urllib.request.urlopen(req, timeout=180, context=ctx)
        except urllib.error.HTTPError as e:
            if e.code in (429, 403, 407):
                print('PARADA: resposta', e.code, 'em', url, flush=True); sys.exit(3)
            if e.code == 404: return None
            raise

    def processa(uf, turno, saida, so_mun=None):
        url = f'{BASE24}bweb_{turno}t_{uf}_{SUF24[turno]}.zip'
        r = abrir(url, metodo='HEAD')
        if r is None: return None
        n = int(r.headers['Content-Length']); r.close()
        with abrir(url, {'Range': f'bytes={max(0, n - 65536)}-{n - 1}'}) as r: cauda = r.read()
        i = cauda.rfind(b'PK\x05\x06'); tot, cdsz, cdoff = struct.unpack('<HII', cauda[i + 10:i + 20])
        cd = cauda[len(cauda) - (n - cdoff):][:cdsz]; p = 0; alvo = None
        while p < len(cd) and cd[p:p + 4] == b'PK\x01\x02':
            metodo, = struct.unpack('<H', cd[p + 10:p + 12]); csz, usz = struct.unpack('<II', cd[p + 20:p + 28])
            fl, el, cl = struct.unpack('<HHH', cd[p + 28:p + 34]); off, = struct.unpack('<I', cd[p + 42:p + 46])
            nome = cd[p + 46:p + 46 + fl].decode('latin1'); p += 46 + fl + el + cl
            if nome.lower().endswith('.csv'): alvo = (off, csz, metodo)
        off, csz, metodo = alvo
        assert metodo == 8 and csz < 0xFFFFFFFF and off < 0xFFFFFFFF
        out = {}; ix = None; resto = b''; dec = zlib.decompressobj(-15)
        with abrir(url, {'Range': f'bytes={off}-{min(off + 700 + csz, n - 1)}'}) as r:
            cab = r.read(30); fl, el = struct.unpack('<HH', cab[26:30]); r.read(fl + el)
            falta = csz
            while falta > 0:
                b = r.read(min(1 << 20, falta))
                if not b: raise IOError('fluxo cortado')
                falta -= len(b)
                dados = resto + dec.decompress(b)
                c = dados.rfind(b'\n')
                if c < 0: resto = dados; continue
                bloco, resto = dados[:c], dados[c + 1:]
                if ix is None:
                    c0 = bloco.find(b'\n'); cabec = bloco[:c0].decode('latin1').strip().replace('"', '').split(';')
                    ix = {x: j for j, x in enumerate(cabec)}; bloco = bloco[c0 + 1:]
                    iM, iZ, iS, iC = ix['CD_MUNICIPIO'], ix['NR_ZONA'], ix['NR_SECAO'], ix['CD_CARGO_PERGUNTA']
                    cH = ix.get('QT_ELEI_BIOM_SEM_HABILITACAO', ix.get('QT_ELEITORES_BIOMETRIA_NH'))
                    cols = [ix['NR_LOCAL_VOTACAO'], ix['DS_TIPO_URNA'], ix['QT_APTOS'], ix['QT_COMPARECIMENTO'], cH, ix['NR_URNA_EFETIVADA']]
                pos = 0
                while True:
                    j = bloco.find(b'"Prefeito"', pos)
                    if j < 0: break
                    a = bloco.rfind(b'\n', 0, j) + 1
                    e = bloco.find(b'\n', j)
                    if e < 0: e = len(bloco)
                    f = [x.strip('"') for x in bloco[a:e].decode('latin1').rstrip('\r').split(';')]
                    pos = e + 1
                    if f[iC] != '11': continue
                    mu = int(f[iM])
                    if so_mun is not None and mu not in so_mun: continue
                    k = f'{uf}|{mu}|{int(f[iZ])}|{int(f[iS])}'
                    if k not in out: out[k] = [f[c] for c in cols]
        with gzip.open(saida + '.tmp', 'wt') as fo: json.dump(out, fo, separators=(',', ':'))
        os.replace(saida + '.tmp', saida)
        return n, len(out)

    tam = {}
    for uf in UFS:
        if uf == 'DF': continue
        s2 = f'{pasta}/est2024_2t_{uf}.json.gz'
        if not os.path.exists(s2) and not os.path.exists(s2 + '.nao_tem'):
            try: r = processa(uf, 2, s2)
            except SystemExit: raise
            except Exception as e: print('erro 2t', uf, type(e).__name__, e, flush=True); continue
            if r is None: open(s2 + '.nao_tem', 'w').write('404\n'); print('sem 2t', uf, flush=True); continue
            print(f'ok {uf} 2t zip {r[0]} secoes {r[1]} {time.time() - t0:.0f}s', flush=True)
    com2t = [uf for uf in UFS if os.path.exists(f'{pasta}/est2024_2t_{uf}.json.gz')
             and len(json.load(gzip.open(f'{pasta}/est2024_2t_{uf}.json.gz', 'rt'))) > 0]  # UF sem 2º turno em 2024 não é lida
    for uf in com2t:
        r = abrir(f'{BASE24}bweb_1t_{uf}_{SUF24[1]}.zip', metodo='HEAD'); tam[uf] = int(r.headers['Content-Length']) if r else 0
        if r: r.close()
    print('tamanhos 1t', tam, flush=True)
    for uf in sorted(com2t, key=lambda u: tam[u]):
        s1_ = f'{pasta}/est2024_1t_{uf}.json.gz'
        if os.path.exists(s1_): continue
        if time.time() - t0 > minutos * 60:
            print('tempo esgotado antes de', uf, flush=True); continue
        muns = {int(k.split('|')[1]) for k in json.load(gzip.open(f'{pasta}/est2024_2t_{uf}.json.gz', 'rt'))}
        try: r = processa(uf, 1, s1_, so_mun=muns)
        except SystemExit: raise
        except Exception as e: print('erro 1t', uf, type(e).__name__, e, flush=True); continue
        print(f'ok {uf} 1t zip {r[0]} secoes {r[1]} municipios {len(muns)} {time.time() - t0:.0f}s', flush=True)
    print('FIM', flush=True)


def exploratorio_placebo_2024(B=None, B22=None):
    """q de 2024 (1º contra 2º turno, cidades com 2º turno, primeira linha de Prefeito por seção), mesma regra de
    universo do D2-1 onde o dado permite (tipo Apurada, comparecimento de 50 ou mais, aptos variando até 2).
    Com as bases de 2026 e 2022, calcula q desses anos nas MESMAS cidades."""
    pasta = f'{TRAB}/dl_bweb2024'; linhas = []; porUF = {}
    for uf in UFS:
        a, b = f'{pasta}/est2024_1t_{uf}.json.gz', f'{pasta}/est2024_2t_{uf}.json.gz'
        if not (os.path.exists(a) and os.path.exists(b)): continue
        d1 = json.load(gzip.open(a, 'rt')); d2 = json.load(gzip.open(b, 'rt')); n0 = len(linhas)
        for k, v2 in d2.items():
            v1 = d1.get(k)
            if v1 is None: continue
            try: x = [int(v1[2]), int(v1[3]), int(v1[4]), int(v2[2]), int(v2[3]), int(v2[4])]
            except ValueError: continue
            if v1[1].upper() != 'APURADA' or v2[1].upper() != 'APURADA' or x[1] < 50 or x[4] < 50 or abs(x[3] - x[0]) > 2 or x[2] < 0 or x[5] < 0: continue
            linhas.append([uf + '|' + k.split('|')[1]] + x + [int(v1[5] != v2[5])])
        porUF[uf] = {'secoes_2t': len(d2), 'secoes_1t_lidas': len(d1), 'no_universo': len(linhas) - n0}
    if not linhas: return {'nao_rodado': 'sem arquivos de 2024'}
    mun = np.array([l[0] for l in linhas]); M = np.array([l[1:] for l in linhas], dtype=np.int64)
    H1, C1, H2, C2 = M[:, 2], M[:, 1], M[:, 5], M[:, 4]
    r = s1(H1, C1, H2, C2)
    mc, mu = _cod(mun); G = len(mu); S = somas_mun(mc, G, H1, C1, H2, C2)
    rng = np.random.default_rng(SEMENTE + 24); W = rng.multinomial(G, np.full(G, 1.0 / G), size=NBOOT).astype(float) @ S
    qb = (W[:, 2] / W[:, 3]) / (W[:, 0] / W[:, 1])
    ufc, ufs = _cod(np.array([m.split('|')[0] for m in mun]))
    out = {'secoes': int(len(M)), 'municipios': int(G), 'ufs_com_dado': sorted(porUF), 'por_UF_leitura': porUF,
           'h1': r['h1'], 'h2': r['h2'], 'q_2024': r['q'], 'ic95_q_2024': pct(qb), 'variacao_H': r['soma_H2'] - r['soma_H1'],
           'variacao_C': r['soma_C2'] - r['soma_C1'], 'soma_C1': r['soma_C1'], 'soma_C2': r['soma_C2'], 'urna_diferente': int(M[:, 6].sum()),
           'q_por_UF': {str(ufs[u]): s1(H1[ufc == u], C1[ufc == u], H2[ufc == u], C2[ufc == u])['q'] for u in range(len(ufs))},
           'q_por_municipio_mediana': float(np.median([(S[g, 2] / S[g, 3]) / (S[g, 0] / S[g, 1]) for g in range(G) if S[g, 0] > 0])),
           'nota': 'eleição municipal, só cidades com 2º turno (grandes, urbanas)'}
    cidades = set(mu.tolist())
    for rot, Bx in (('2026', B), ('2022', B22)):
        if Bx is None: continue
        mm = universo_d21(Bx) & np.isin(Bx['mun'], list(cidades))
        if mm.sum() == 0: continue
        x = s1(Bx['H1'][mm], Bx['C1'][mm], Bx['H2'][mm], Bx['C2'][mm])
        c_, u_ = _cod(Bx['mun'][mm]); Sx = somas_mun(c_, len(u_), Bx['H1'][mm], Bx['C1'][mm], Bx['H2'][mm], Bx['C2'][mm])
        Wx = np.random.default_rng(SEMENTE + 25).multinomial(len(u_), np.full(len(u_), 1.0 / len(u_)), size=NBOOT).astype(float) @ Sx
        out[f'nas_mesmas_cidades_{rot}'] = {'secoes': int(mm.sum()), 'municipios': int(len(u_)), 'h1': x['h1'], 'h2': x['h2'], 'q': x['q'],
                                            'ic95_q': pct((Wx[:, 2] / Wx[:, 3]) / (Wx[:, 0] / Wx[:, 1])),
                                            'variacao_H': x['soma_H2'] - x['soma_H1'], 'variacao_C': x['soma_C2'] - x['soma_C1'],
                                            'soma_C1': x['soma_C1'], 'soma_C2': x['soma_C2'],
                                            'E_bruto_qref1': x['E_bruto_qref1'], 'E_com_qref_de_2024': x['soma_H2'] - r['q'] * x['h1'] * x['soma_C2']}
    if B is not None:
        m = universo_d21(B); z = s1(B['H1'][m], B['C1'][m], B['H2'][m], B['C2'][m], r['q'])
        out['E_de_2026_no_pais_com_qref_de_2024'] = z['E']
        out['ic95_E_de_2026_no_pais_com_qref_de_2024_so_incerteza_de_q2024'] = [z['soma_H2'] - q_ * z['h1'] * z['soma_C2'] for q_ in pct(qb)[::-1]]
    return out


# ----------------------------------------------------------------------------------------------------------------
# RELATÓRIO EM TEXTO
# ----------------------------------------------------------------------------------------------------------------
def mi(x):
    if x is None: return 'n/d'
    s = f'{abs(int(round(x))):,}'.replace(',', '.')
    return ('-' if round(x) < 0 else '') + s


def de(x, n=4):
    if x is None or (isinstance(x, float) and x != x): return 'n/d'
    return f'{x:.{n}f}'.replace('.', ',')


def pc(x, n=2):
    return de(100 * x, n) + '%'


def fx(v, f=mi):
    return 'n/d' if v is None else f'{f(v[0])} a {f(v[1])}'


def escreve_txt(R):
    L = []; w = L.append
    D, F, T, X = R['D2-1'], R['D4-6a'], R['D2-6'], R['exploratorio']
    S1, S2, S3, P22, PL, PO, VE = D['S1'], D['S2'], D['S3'], D['placebo_2022'], D['plantios'], D['poder'], D['veredito']
    w('R27_B2: LIBERAÇÕES E MUDANÇAS NA SEÇÃO (D2-1 LIBERA, D2-6 TROCA e D4-6 parte a)')
    w('')
    w('Registro: Adendo 27 (commit 2748895, 10/11/2026 00:16:42 UTC), Onda B, item B2, na ordem do Adendo 28 (commit 938be19,')
    w('04:36:33 UTC). Critérios de registro/adendo27/desenho_D2_proposta.json (D2-1 e D2-6) e desenho_D4_proposta.json (D4-6 a).')
    w('Desenhos cegos. Docstring com as decisões que o registro não fixa congelado às 04:52 UTC, com uma emenda às 04:58 UTC')
    w('(plantio do a3), tudo antes de qualquer conta. Script: scripts/analisar_R27_B2.py. Números completos no JSON ao lado.')
    w('')
    w('PERGUNTA. A Onda A mostrou que a virada passa pelo comparecimento. Se os votos a mais tivessem sido lançados pela mesa em')
    w('nome de quem não foi votar, o eleitor com biometria teria de ser liberado pelo mesário, e cada liberação fica contada no')
    w('boletim (QT_ELEI_BIOM_SEM_HABILITACAO). Se tivessem vindo de aptos acrescentados, urna trocada, urna recarregada ou seção')
    w('agregada, isso também fica nos campos do boletim. Este teste olha esses campos em todas as seções do país.')
    w('')
    w('VEREDITOS')
    w(f"  D2-1 LIBERA: {VE['veredito']} pela regra de poder que fixei antes de rodar (L8); pela letra do critério do registro, sem")
    w(f"     essa regra, {VE['pela_letra_do_registro_sem_a_regra_de_poder_L8']}. O inconclusivo vem só da comparação com 2022 (a régua de 2024, exploratória, aponta")
    w('     para o mesmo lado); só com 2026 as três condições de SEM SINAL se cumprem.')
    w(f"  D4-6 (a):    {F['veredito']['veredito']} pela regra de poder que fixei antes (F4); pela letra do critério do registro, {F['veredito']['pela_letra_do_registro_sem_a_regra_de_poder_F4']}.")
    w(f"  D2-6 TROCA:  {T['veredito']['veredito']} (as cinco bandeiras e os aptos), com plantio recuperado.")
    w('  Em uma frase: a alta do comparecimento não entrou por liberação do mesário, nem por aptos, urna trocada, recarga ou')
    w('  agregação; sobra uma diferença de nível contra 2022 e 2024 (a liberação não caiu no 2º turno como caía: 570 a 740 mil,')
    w('  13% a 17% da margem) que não tem ligação com o voto e não chega a um quarto da margem.')
    w('')
    c = R['base']['conferencia']
    w('0. DADOS E CONFERÊNCIAS')
    w(f"  bweb de 2026 lido de novo dos zips (uma linha por seção): {mi(c['secoes_1t_passada_propria'])} seções no 1º turno e {mi(c['secoes_2t_passada_propria'])} no 2º;")
    w(f"  {c['divergencias_1t_contra_desenhista_11_campos'] + c['divergencias_2t_contra_desenhista_11_campos']} divergências em 11 campos contra a extração dos desenhistas e {c['divergencias_1t_contra_secoes2026_aptos_comp_urna_local'] + c['divergencias_2t_contra_secoes2026_aptos_comp_urna_local']} contra dados/secoes2026 (aptos, comparecimento, urna, local).")
    w(f"  Pareadas pela chave: {mi(c['secoes_pareadas'])}. Só no 1º turno: 1 seção do exterior (30 aptos, 2 votos).")
    u22 = D['universo_2022']
    w(f"  bweb de 2022 (placebo): baixado em fluxo do CDN do TSE, 54 arquivos, sem erro e sem bloqueio; {mi(u22['secoes_no_bweb2022']['1t'])} seções por turno;")
    w(f"  aptos e comparecimento iguais aos de dados/secoes2022 em todas; sem o campo só as {mi(u22['conferencia'].get('sem_H', 0))} seções do exterior (não baixado).")
    w(f"  Regressão própria (erro por município) conferida contra lib.fe_ols: maior diferença de coeficiente {D['conferencia_reg_fe_contra_lib']['maior_dif_coef']:.1e}.")
    w('')
    U = D['universo']
    w('1. D2-1 LIBERA: liberações manuais em todas as seções')
    w(f"  Universo (letra): {mi(U['secoes'])} seções, {mi(U['comparecimento_2t_dentro'])} votantes no 2º turno. Fora: {mi(U['secoes_fora'])} seções e {mi(U['comparecimento_2t_fora'])} votantes")
    fm = U['fora_por_motivo_nao_exclusivo']
    w(f"  (exterior {mi(fm['exterior'])}; comparecimento abaixo de 50 em algum turno {mi(fm['comparecimento_abaixo_de_50_em_algum_turno'])}; aptos variando mais de 2: {mi(fm['aptos_variam_mais_de_2'])}); a margem de fora é {mi(U['margem_2t_fora'])}.")
    w('')
    w('  S1, NÍVEL (enxerga inserção espalhada ou concentrada, porque é soma nacional)')
    w(f"    2026 bruto: liberações {mi(S1['soma_H1'])} no 1º turno ({pc(S1['h1'], 3)} do comparecimento) e {mi(S1['soma_H2'])} no 2º ({pc(S1['h2'], 3)}).")
    w(f"    Razão q = {de(S1['q'])} (IC 95% {fx(S1['ic95_q'], de)}): a taxa subiu 1,1%. Alta de {mi(S1['variacao_H'])} liberações para {mi(S1['variacao_C'])} votantes")
    w(f"    a mais: {pc(S1['fatia_da_alta_do_comparecimento_que_veio_por_liberacao'], 1)} da alta do comparecimento veio por liberação, contra {pc(S1['h1'], 1)} de taxa de base.")
    w(f"    Sobra bruta de 2026 (q_ref = 1, sem outro ano): E = {mi(S1['E_bruto_qref1'])} liberações (IC 95% {fx(S1['ic95_E_bruto_qref1'])}; 99% {fx(S1['ic99_E_bruto_qref1'])}),")
    w(f"    {pc(S1['E_bruto_sobre_margem'], 1)} da margem.")
    p1 = P22['S1']
    w(f"    2022 (placebo): a taxa CAIU do 1º para o 2º turno, de {pc(p1['h1'], 2)} para {pc(p1['h2'], 2)}: q_ref = {de(p1['q'])} (IC {fx(p1['ic95_q'], de)});")
    w(f"    {mi(-p1['variacao_H'])} liberações a menos com {mi(p1['variacao_C'])} votantes a mais.")
    w(f"    Sobra pela letra (contra o padrão de 2022): E = {mi(S1['E'])} (IC 95% {fx(S1['ic95_E_qref_reestimado'])}; 99% {fx(S1['ic99_E_qref_reestimado'])}),")
    w(f"    {pc(S1['E_sobre_margem'], 1)} da margem. Com q_ref fixo o IC é {fx(S1['ic95_E_qref_fixo'])}. Este número depende inteiro de 2022.")
    pu = D['S1_por_urna']
    w(f"    Mesma urna nos dois turnos ({mi(pu['mesma_urna']['secoes'])} seções): q {de(pu['mesma_urna']['q'])}, E bruto {mi(pu['mesma_urna']['E_bruto_qref1'])}, E contra 2022 {mi(pu['mesma_urna']['E'])}.")
    w(f"    Urna diferente ({mi(pu['urna_diferente']['secoes'])} seções): q {de(pu['urna_diferente']['q'])}, E bruto {mi(pu['urna_diferente']['E_bruto_qref1'])}, E contra 2022 {mi(pu['urna_diferente']['E'])}.")
    w('')
    w('    Por UF (E bruto usa só 2026; E contra 2022 usa o q de 2022 da própria UF; IC 95% por reamostragem de municípios):')
    w('    UF  seções  taxa 1T  q 2026  q 2022    E bruto  E contra 2022   IC 95% do E contra 2022   alta de H  alta de C')
    for u, v in D['S1_por_UF'].items():
        w(f"    {u} {mi(v['secoes']):>7} {pc(v['h1'], 2):>8} {de(v['q'], 3):>7} {de(v['q_ref'], 3):>7} {mi(v['E_bruto_qref1']):>10} {mi(v['E']):>14}   {fx(v['ic95_E_qref_uf']):>22} {mi(v['variacao_H']):>11} {mi(v['variacao_C']):>10}")
    su = D['S1_soma_das_UFs']
    w(f"    Soma das UFs: E bruto {mi(su['E_bruto_qref1_por_UF'])} (só as positivas: {mi(su['soma_dos_E_positivos_bruto'])}); E contra 2022 {mi(su['E_qref_da_UF'])}.")
    cu = D['complementos']
    a5, ar = cu['UF5_PI_MA_TO_PB_CE'], cu['resto']
    w(f"    Nas cinco UFs do indício da Onda A (PI, MA, TO, PB, CE): q = {de(a5['q'])} contra {de(ar['q'])} no resto; E bruto = {mi(a5['E_bruto_qref1'])}")
    w(f"    (IC {fx(a5['ic95_E_bruto_qref1'])}); E contra 2022 = {mi(a5['E'])}. A margem de Lula nessas cinco UFs é {mi(a5['margem_2t'])}.")
    w('')
    w('  S2, CAUDA (enxerga inserção concentrada em poucas seções)')
    w(f"    Cauda direita (z de 4 ou mais): {mi(S2['secoes_cauda_direita'])} seções, X+ = {mi(S2['X_mais'])} liberações acima do esperado.")
    w(f"    Cauda esquerda (z de -4 ou menos): {mi(S2['secoes_cauda_esquerda'])} seções, X- = {mi(S2['X_menos'])}. A = X+ menos X- = {mi(S2['A'])} (IC 95% {fx(S2['ic95_A'])}).")
    w(f"    Há mais queda grande que subida grande. Sem centrar (ao lado): A = {mi(S2['sem_centrar_ao_lado']['A'])}. Em 2022: X+ {mi(P22['S2']['X_mais'])}, X- {mi(P22['S2']['X_menos'])}, A {mi(P22['S2']['A'])}.")
    w('')
    w('  S3, ELO COM O VOTO (dentro do mesmo local de votação)')
    w(f"    gama = {de(S3['gama'])} (ep {de(S3['ep'])}; IC 95% {fx(S3['ic95'], de)}; n = {mi(S3['n'])} seções em {mi(S3['locais'])} locais, erro por {mi(S3['agrupamentos_do_erro'])} municípios).")
    w('    Onde a liberação subiu mais, Lula não ganhou mais margem. O registro esperava 0,3 a 1,1 com inserção.')
    w(f"    2022: gama = {de(P22['S3']['gama'])} (ep {de(P22['S3']['ep'])}), positivo e pequeno.")
    es = D['espelhos']
    w(f"    Espelho por candidato em 2026: ganho de Lula por liberação a mais {de(es['gama_L']['coef'])} (ep {de(es['gama_L']['ep'])}); de Flávio {de(es['gama_R']['coef'])} (ep {de(es['gama_R']['ep'])}).")
    w(f"    Desfecho placebo (branco e nulo): {de(es['gama_BN_desfecho_placebo']['coef'])} (ep {de(es['gama_BN_desfecho_placebo']['ep'])}).")
    ti = es['turnos_invertidos']
    w(f"    Turnos invertidos (1º turno tratado como suspeito): E bruto {mi(ti['S1']['E_bruto_qref1'])}; cauda A = {mi(ti['S2']['A'])} (X+ {mi(ti['S2']['X_mais'])}, X- {mi(ti['S2']['X_menos'])}); gama = {de(ti['S3']['gama'])} (ep {de(ti['S3']['ep'])}).")
    w('')
    w('  CALIBRAÇÃO POR EFEITO PLANTADO (20 repetições cada; K = votos somados a H2, C2 e L2)')
    w('    plantio                                              E devolve   A devolve   gama (ep)')
    nomes_pl = [(f'irregularidade_uniforme_{LIM25}', 'inserção uniforme, 25% da margem'), (f'irregularidade_uniforme_{LIM10}', 'inserção uniforme, 10% da margem'),
                (f'irregularidade_concentrado_{LIM25}', 'inserção em 5% das seções, 25% da margem'), (f'irregularidade_concentrado_{LIM10}', 'inserção em 5% das seções, 10% da margem'),
                (f'inocente_I1_eleitor_real_uniforme_{LIM25}', 'INOCENTE eleitor real para Lula, uniforme, 25%'), (f'inocente_I1_eleitor_real_concentrado_{LIM25}', 'INOCENTE eleitor real para Lula, 5% das seções'),
                (f'inocente_I2_leitor_pior_uniforme_{LIM25}', 'INOCENTE leitor pior (só H sobe), uniforme'), (f'inocente_I2_leitor_pior_concentrado_{LIM25}', 'INOCENTE leitor pior, 5% das seções'),
                (f'inocente_I3_abstencao_pura_uniforme_{LIM25}', 'INOCENTE abstenção pura de Flávio, uniforme'), (f'inocente_I3_abstencao_pura_concentrado_{LIM25}', 'INOCENTE abstenção pura de Flávio, 5% das seções')]
    for k, rot in nomes_pl:
        v = PL[k]
        w(f"    {rot:<50} {pc(v['delta_E_sobre_K'], 1):>9}   {pc(v['delta_A_sobre_K'], 1):>9}   {de(v['gama']['media'], 3)} ({de(v['ep_gama'], 3)})")
    w(f"    observado em 2026                                                                {de(S3['gama'], 3)} ({de(S3['ep'], 3)})")
    w(f"    Leitura: S1 devolve {pc(PO['S1_devolve_uniforme_25'], 1)} do plantado em qualquer desenho (o registro esperava 95% a 105%; pela fórmula o esperado é")
    w(f"    {pc(PO['S1_esperado_pela_formula'], 1)}, porque o voto inserido também aumenta o comparecimento). S2 devolve {pc(PO['S2_devolve_concentrado_25'], 1)} do plantio concentrado de 25% e só")
    w(f"    {pc(PO['S2_devolve_concentrado_10'], 1)} do de 10% (18 votos por seção não passam de z = 4). S3 dá gama de {de(PO['S3_gama_concentrado_25'], 2)} e {de(PO['S3_gama_concentrado_10'], 2)}, não os 0,6 do registro, porque")
    w('    a própria regressão do registro controla a variação do comparecimento, que sobe junto com a liberação inserida.')
    w('    O teste distingue as explicações: eleitor real que entra (I1) e abstenção pura (I3) não mexem em E nem em A; leitor')
    w('    pior (I2) mexe em E e em A igual à inserção, e só gama separa os dois (gama fica em zero).')
    w('')
    w('  PODER E VEREDITO')
    w(f"    Regra L8, fixada antes: S1 enxerga (sim); S2 enxerga se devolver 90% (devolve {pc(PO['S2_devolve_concentrado_25'], 1)}: não); S3 enxerga se gama plantado for 0,6")
    w(f"    ou mais (é {de(PO['S3_gama_concentrado_25'], 2)}: não). Com S2 e S3 abaixo da régua do registro, a regra dá SEM PODER para o conjunto.")
    cs, cn = VE['condicoes_sinal'], VE['condicoes_sem_sinal']
    w(f"    Pela letra do critério do registro: SINAL exige Q de 1.107.548 ou mais (Q = {mi(D['Q']['Q'])}: não) e gama de 0,30 ou mais (não).")
    w(f"    SEM SINAL exige limite superior do IC de E abaixo de 443.019 (é {mi(S1['ic95_E_qref_reestimado'][1])}: não), A abaixo de 443.019 (sim) e limite superior")
    w(f"    de gama abaixo de 0,10 (é {de(S3['ic95'][1])}: sim). Resultado pela letra: {VE['pela_letra_do_registro_sem_a_regra_de_poder_L8']}.")
    w(f"    Só com 2026 (q_ref = 1): limite superior de E = {mi(S1['ic95_E_bruto_qref1'][1])}, abaixo de 443.019; as três condições de SEM SINAL se cumprem.")
    w('    O que decide entre INCONCLUSIVO e SEM SINAL é, portanto, aceitar ou não a queda de 2022 como o padrão natural. O')
    w('    exploratório com 2024 (seção 4, item e) mostra que a queda entre turnos se repete; isso reforça o INCONCLUSIVO.')
    w('')
    w('  COMPLEMENTOS FIXADOS ANTES (não decidem)')
    w(f"    Elo nas cinco UFs: gama = {de(a5['S3']['gama'])} (ep {de(a5['S3']['ep'])}); no resto: {de(ar['S3']['gama'])} (ep {de(ar['S3']['ep'])}).")
    w('    Por região: ' + '; '.join(f"{r} {de(v['gama'], 3)} ({de(v['ep'], 3)})" for r, v in cu['S3_por_regiao'].items()) + '.')
    sp = cu['S3_com_perfil']
    w(f"    Com perfil da seção (idade e fração sem biometria no cadastro): gama = {de(sp['gama'])} (ep {de(sp['ep'])}); positivo, e 20 vezes menor que o")
    w('    que 10% da margem inserida produziria.')
    cv = cu['cauda_e_voto']
    w(f"    Cauda e voto: as seções da cauda direita ganharam {de(cv['coef_cauda_direita'])} de margem por votante contra as vizinhas (ep {de(cv['ep_cauda_direita'])}): {mi(cv['votos_de_margem_cauda_direita'])} votos.")
    ic_ = cu['inclinacao_dH_em_dC_dentro_do_local']
    w(f"    Dentro do local, cada votante a mais traz {de(ic_['coef'], 3)} liberação (ep {de(ic_['ep'], 3)}), contra {de(ic_['fatia_H1_sobre_C1'], 3)} de taxa média: o eleitor marginal é")
    w('    liberado pelo mesário um terço mais vezes que a média, e 91% dele entra sem liberação.')
    al = D['achado_local']
    w('')
    w('  ACHADO LOCAL (para pedido de ata, caderno e arquivos da urna)')
    w(f"    {al['secoes_z6_ou_mais']} seções com z de 6 ou mais, {mi(al['liberacoes_a_mais_nelas'])} liberações acima do esperado; {al['com_urna_trocada']} delas com urna trocada entre os turnos.")
    w(f"    Variação da margem nelas: {de(al['variacao_da_margem_por_C1_nelas'], 3)} por votante, contra {de(al['variacao_da_margem_por_C1_no_universo'], 3)} no país. As dez maiores:")
    for s in al['lista_300_maiores'][:10]:
        w(f"      {s['chave']:<20} H {s['H1']:>3} de {s['C1']:>3} no 1º turno; {s['H2']:>3} de {s['C2']:>3} no 2º; z {de(s['z'], 1)}; margem {s['variacao_da_margem']:+d}; urna trocada: {'sim' if s['urna_trocada'] else 'não'}")
    w('    Lista inteira no JSON (campo achado_local).')
    w('')
    # ---------------- D4-6 ----------------
    a1 = F['a1']; a2 = F['a2']; a3 = F['a3']; a4 = F['a4']; pf = F['plantios']; p22 = F.get('placebo_2022', {})
    t = a1['todas_as_pareadas_27UFs_e_exterior']
    w('2. D4-6 (a): VOTOS SEM ORIGEM PELO COMPARECIMENTO SEM BIOMETRIA')
    w(f"  (a1) Excesso nacional F = {mi(t['F'])} (IC 95% {fx(t['ic95'])}), {pc(t['F_sobre_margem'], 1)} da margem: variação de NB {mi(t['variacao_NB'])}, do comparecimento {mi(t['variacao_comp'])},")
    w(f"       fatia de NB no 1º turno {pc(t['fatia_NB_1t'], 2)}. Só 27 UFs: {mi(a1['so_27_UFs']['F'])}. No universo do D2-1: {mi(a1['universo_do_D2-1']['F'])} (é o E bruto da S1).")
    if p22:
        w(f"       2022: F = {mi(p22['a1']['F'])} (IC {fx(p22['a1']['ic95'])}): negativo, a liberação caiu.")
    w(f"  (a2) mu menos mu' = {de(a2['mu_menos_mulinha'])} (ep {de(a2['ep'])}; IC 95% {fx(a2['ic95'], de)}; {mi(a2['n'])} seções). Margem por votante a mais com biometria:")
    w(f"       mu' = {de(a2['mulinha_com_biometria'], 3)} (ep {de(a2['ep_mulinha'], 3)}); por liberado sem biometria: mu = {de(a2['mu_sem_biometria'], 3)} (ep {de(a2['ep_mu'], 3)}). É o mesmo valor.")
    gl, gr = a2['ganho_de_Lula_L2_menos_L1'], a2['ganho_de_Flavio_R2_menos_R1']
    w(f"       Em separado: cada votante a mais com biometria dá {de(gl['mulinha_com_biometria'], 3)} voto a Lula e {de(gr['mulinha_com_biometria'], 3)} a Flávio; liberado pelo mesário, {de(gl['mu_sem_biometria'], 3)} e {de(gr['mu_sem_biometria'], 3)}.")
    if p22:
        q2 = p22['a2_eliminados_somados']; vs = a2['versao_eliminados_somados']
        w(f"       2022 (eliminados somados): mu menos mu' = {de(q2['mu_menos_mulinha'])} (ep {de(q2['ep'])}); 2026 na mesma versão: {de(vs['mu_menos_mulinha'])} (ep {de(vs['ep'])}).")
    w(f"       Espelho com os turnos invertidos: {de(a2['espelho_turnos_invertidos']['mu_menos_mulinha'])} (ep {de(a2['espelho_turnos_invertidos']['ep'])}). Desfecho placebo (branco e nulo): {de(a2['desfecho_placebo_BN2_menos_BN1']['mu_menos_mulinha'])} (ep {de(a2['desfecho_placebo_BN2_menos_BN1']['ep'])}).")
    w(f"  (a3) Eleitores sem biometria no cadastro: {mi(a3['soma_SB_nacional_27UFs'])} ({pc(a3['parcela_sem_biometria_no_cadastro'], 1)} do eleitorado). Coeficiente na alta do comparecimento:")
    w(f"       {de(a3['coef_SB'])} (ep {de(a3['ep'])}): onde há mais eleitor sem biometria o comparecimento subiu MENOS. Votos implicados: {mi(a3['votos_implicados'])}")
    w(f"       (IC 95% {fx(a3['ic95_votos_implicados'])}). Plantio: o coeficiente sobe {pc(a3['plantio']['subida_sobre_phi'], 1)} do plantado. O reservatório sem biometria não aparece.")
    if a4.get('secoes'):
        pass
    if 'secoes_com_os_dois_dias_no_log' in a4:
        w(f"  (a4) Logs da amostra antiga ({mi(a4['secoes_com_os_dois_dias_no_log'])} seções, não aleatória, sem extrapolar): votos depois das 17h locais: {mi(a4['1t']['depois_das_17h'])} no 1º turno e")
        w(f"       {mi(a4['2t']['depois_das_17h'])} no 2º; sem biometria entre eles: {mi(a4['1t']['sem_biometria_depois_das_17h'])} ({pc(a4['1t']['parcela_sem_biometria_entre_os_tardios'], 1)}) e {mi(a4['2t']['sem_biometria_depois_das_17h'])} ({pc(a4['2t']['parcela_sem_biometria_entre_os_tardios'], 1)}). Excesso tardio sobre a parcela do")
        w(f"       1º turno: {de(a4['excesso_tardio_sobre_a_parcela_do_1t'], 1)} votos (IC {fx(a4['ic95_excesso_tardio'], lambda z: de(z, 1))}). No dia inteiro: {pc(a4['1t']['parcela_sem_biometria_no_dia'], 2)} sem biometria no 1º turno e {pc(a4['2t']['parcela_sem_biometria_no_dia'], 2)} no 2º.")
        w('       Nesta amostra quase não houve voto depois das 17h no 2º turno; por aí não entrou volume.')
    w('  Calibração (20 repetições; plantio em 5% das seções sorteadas, somado a L2, comparecimento e NB):')
    for k, rot in ((f'letra_concentrado_{LIM10}', 'inserção de 10% da margem'), (f'letra_concentrado_{LIM25}', 'inserção de 25% da margem'), (f'letra_concentrado_{MARGEM}', 'inserção da margem inteira'),
                   (f'espelho_a_favor_de_Flavio_concentrado_{LIM25}', 'ESPELHO: 25% inseridos para Flávio'),
                   (f'inocente_I1_eleitor_real_concentrado_{LIM25}', 'INOCENTE eleitor real para Lula, 5% das seções'), (f'inocente_I1_eleitor_real_uniforme_{LIM25}', 'INOCENTE eleitor real para Lula, uniforme'),
                   (f'inocente_I3_abstencao_pura_concentrado_{LIM25}', 'INOCENTE abstenção pura de Flávio, 5% das seções'), (f'inocente_I3_abstencao_pura_uniforme_{LIM25}', 'INOCENTE abstenção pura de Flávio, uniforme')):
        v = pf[k]
        w(f"    {rot:<50} F devolve {pc(v['delta_F_sobre_K'], 1):>6}; mu menos mu' = {de(v['mu_menos_mulinha']['media'], 3)} (ep {de(v['ep'], 3)}); mu' = {de(v['mulinha']['media'], 3)}")
    w(f"    observado                                          F = {mi(t['F'])}; mu menos mu' = {de(a2['mu_menos_mulinha'], 3)} (ep {de(a2['ep'], 3)}); mu' = {de(a2['mulinha_com_biometria'], 3)}")
    w("    Leitura: o registro esperava mu menos mu' perto de 1 com inserção; nem a margem inteira plantada chega a 0,5, porque a")
    w('    liberação natural troca de lugar com a biometria na mesma seção e isso dilui o coeficiente. Logo o teste não tem como')
    w("    ACUSAR pelo limiar de 0,5 (regra F4: SEM PODER). Para ABSOLVER ele tem poder: 10% da margem plantados dão 0,226, acima")
    w('    do limiar de 0,2, e o observado é 0,002. Eleitor real que entra e abstenção pura não mexem na estatística.')
    vf = F['veredito']
    w(f"  Veredito: {vf['veredito']} pela regra F4; pela letra do registro, {vf['pela_letra_do_registro_sem_a_regra_de_poder_F4']} (F de até 443.019: sim; mu menos mu' de até 0,2: sim;")
    w('  votos implicados em (a3) de até 443.019: sim; nenhum IC de 95% cruza o limiar).')
    w('')
    # ---------------- D2-6 ----------------
    t1 = T['T1']; tt = t1['27UFs_e_exterior']; tb = t1['so_27_UFs']; bc = T['bandeiras_contagem']; E = T['elo']
    w('3. D2-6 TROCA: O QUE MUDOU NA SEÇÃO ENTRE OS TURNOS')
    w('  T1, APTOS')
    w(f"    Seções com aptos diferentes: {mi(tt['secoes_com_aptos_diferentes'])} ({mi(tt['secoes_com_alta'])} com alta, {mi(tt['secoes_com_queda'])} com queda). Soma das altas: {mi(tt['soma_das_altas_max(apt2-apt1,0)'])} eleitores;")
    w(f"    espelho, soma das quedas: {mi(tt['espelho_soma_das_quedas_max(apt1-apt2,0)'])}; líquido {mi(tt['liquido'])}. Só 27 UFs: altas {mi(tb['soma_das_altas_max(apt2-apt1,0)'])}, quedas {mi(tb['espelho_soma_das_quedas_max(apt1-apt2,0)'])}.")
    dd = tt['distribuicao_da_diferenca']
    w(f"    Tamanho: {mi(dd['1_a_2'])} seções com 1 ou 2 a mais, {mi(dd['3_a_10'])} com 3 a 10, {dd['11_ou_mais']} com 11 ou mais (maior alta {tt['maior_alta']}); {mi(dd['-2_a_-1'])} com 1 ou 2 a menos,")
    w(f"    {mi(dd['-10_a_-3'])} com 3 a 10, {dd['-11_ou_menos']} com 11 ou mais a menos (maior queda {tt['maior_queda']}).")
    w(f"    Boletim contra o arquivo de locais do TSE (gerado em 25/10/2026; cadastro de cada turno, agregadas somadas na principal): igual em {mi(tt['boletim_igual_ao_cadastro_de_locais_1t'])} de")
    w(f"    {mi(tt['secoes_pareadas'])} seções no 1º turno e em {mi(tt['boletim_igual_ao_cadastro_de_locais_2t'])} no 2º. Soma das altas sem explicação pelo cadastro: {mi(tt['soma_das_altas_SEM_explicacao'])}.")
    w('    O eleitorado inscrito da seção (QT_ELEITOR_SECAO) é igual nos dois turnos em todas; o que muda é o número de aptos da')
    w('    eleição federal em cada turno, na casa de 1 ou 2 por seção, com soma zero. Limite: isso mostra que o boletim segue o')
    w('    cadastro publicado, não por que o cadastro de cada turno difere.')
    w(f"    Comparecimento acima dos aptos: {tt['comparecimento_acima_dos_aptos_1t']} seções no 1º turno e {tt['comparecimento_acima_dos_aptos_2t']} no 2º. Com 95% ou mais dos aptos: {tt['comparecimento_95_ou_mais_dos_aptos_1t']} e {tt['comparecimento_95_ou_mais_dos_aptos_2t']}.")
    h = t1['historico_secoes_com_aptos_diferentes']
    w('    Outros anos (seções com aptos diferentes; soma das altas): ' + '; '.join(f"{a}: {mi(h[a]['todas'])}; {mi(h[a]['soma_das_altas'])}" for a in ('2014', '2018', '2022')) + f"; 2026: {mi(tt['secoes_com_aptos_diferentes'])}; {mi(tt['soma_das_altas_max(apt2-apt1,0)'])}.")
    pt = t1['plantio_1_apto_em_1pct']
    w(f"    Plantio: 1 apto a mais em {mi(pt['secoes_plantadas'])} seções leva a soma das altas de {mi(pt['soma_das_altas_antes'])} para {mi(pt['soma_das_altas_depois'])} ({pt['ja_estavam_em_queda_entre_as_plantadas']} das plantadas estavam em queda): a contagem enxerga.")
    w('')
    w('  T2 e T3, BANDEIRAS (elo dentro do local; IC ao nível de 0,2%; V em votos de margem)')
    w('    bandeira                                   seções        teto     gama (ep)             V     IC 99,8% de V        rho do plantio de 10%')
    rot = {'U': 'U urna diferente da do 1º turno', 'CT': 'CT carga de 05/10 em diante', 'CD': 'CD carga no dia 25/10', 'AG': 'AG seção com agregadas', 'AM': 'AM conjunto de agregadas mudou'}
    for nm in ('U', 'CT', 'CD', 'AG', 'AM'):
        e = E[nm]; b = bc[nm]; pl = T['plantios'].get(nm, {}).get(str(LIM10), {})
        if 'gama' in e:
            w(f"    {rot[nm]:<40} {mi(b['secoes_27UFs']):>8} {mi(e['teto']):>11}   {de(e['gama'], 5)} ({de(e['ep'], 5)}) {mi(e['V']):>9}   {fx(e['ic998_V']):>20}   {de(pl['rho'], 2) if pl else 'teto abaixo de 443.019'}")
        else:
            w(f"    {rot[nm]:<40} {mi(b['secoes_27UFs']):>8} {mi(e['teto']):>11}   sem seção marcada")
    w(f"    U e CT juntas em {mi(bc['U_e_CT'])} seções; U sem CT em {mi(bc['U_sem_CT'])}; CT sem U em {mi(bc['CT_sem_U'])}. AM: zero pelo bweb e zero pelo arquivo de locais.")
    w(f"    Espelho por candidato na bandeira U: Lula {de(E['U']['espelho_ganho_de_Lula']['gama'], 5)} (ep {de(E['U']['espelho_ganho_de_Lula']['ep'], 5)}); Flávio {de(E['U']['espelho_ganho_de_Flavio']['gama'], 5)} (ep {de(E['U']['espelho_ganho_de_Flavio']['ep'], 5)}).")
    w(f"    AG: gama positivo a 3,8 ep dentro do local, {mi(E['AG']['V'])} votos; com efeito fixo de município o sinal inverte ({mi(X['efeito_fixo_mais_largo']['bandeira_AG_efeito_fixo_de_municipio']['V'])} votos, exploratório).")
    w('    Desfecho placebo (branco e nulo): ' + '; '.join(f"{nm} {de(E[nm]['desfecho_placebo_BN']['gama'], 5)} ({de(E[nm]['desfecho_placebo_BN']['ep'], 5)})" for nm in ('U', 'CT', 'AG')) + '.')
    pa = T['placebo_U_outros_anos']
    w('    Placebo da bandeira U em outros anos: ' + '; '.join(f"{a}: gama {de(pa[a]['gama'], 5)} (ep {de(pa[a]['ep'], 5)}), V {mi(pa[a]['V'])}, {pc(pa[a]['fracao_de_secoes_com_urna_trocada'], 2)} das seções" for a in ('2014', '2018', '2022')) + '.')
    w(f"    Em 2026 a urna foi trocada em {pc(bc['U']['secoes_27UFs'] / tb['secoes_pareadas'], 2)} das seções, um terço da taxa dos outros anos.")
    pc1 = E['placebo_C1T_corte_do_1t']
    w(f"    Placebo do 1º turno (carga tardia antes de 04/10, {mi(pc1['secoes_marcadas'])} seções): diferença de nível no 1º turno contra as vizinhas {de(pc1['gama'], 4)} (ep {de(pc1['ep'], 4)}).")
    w(f"    Com o modelo da urna como controle, U: {de(E['U']['com_modelo_da_urna']['gama'], 5)} (ep {de(E['U']['com_modelo_da_urna']['ep'], 5)}). Por UF, o maior desvio de U é o da PB: {de(E['U']['por_UF']['PB']['gama'], 4)} (z {de(E['U']['por_UF']['PB']['z'], 1)}),")
    w(f"    a favor de Flávio, {mi(E['U']['por_UF']['PB']['V'])} votos; com 24 UFs testadas, um z desse tamanho por acaso é esperado uma vez a cada 30 baterias.")
    w(f"    Complementos: seções com aptos em alta: gama {de(E['AP_mais']['gama'], 5)} (ep {de(E['AP_mais']['ep'], 5)}), V {mi(E['AP_mais']['V'])}; em queda: {de(E['AP_menos']['gama'], 5)} (ep {de(E['AP_menos']['ep'], 5)}), V {mi(E['AP_menos']['V'])};")
    w(f"    dose (apto a mais por votante): {de(E['dose_(apt2-apt1)/C1']['gama'], 3)} (ep {de(E['dose_(apt2-apt1)/C1']['ep'], 3)}).")
    pl = T['plantios']
    w('    Plantio (votos somados a L2 e C2 nas seções marcadas): U devolve ' + f"{pc(pl['U'][str(LIM10)]['rho'], 0)} de 443.019 e {pc(pl['U'][str(LIM25)]['rho'], 0)} de 1.107.548; CT {pc(pl['CT'][str(LIM10)]['rho'], 0)}; AG {pc(pl['AG'][str(LIM10)]['rho'], 0)} e {pc(pl['AG'][str(LIM25)]['rho'], 0)}.")
    w(f"    Passa de 100% porque o teto é medido depois do plantio; com o teto de antes: U {pc(pl['U'][str(LIM10)]['rho_com_o_teto_de_antes_do_plantio'], 0)}, CT {pc(pl['CT'][str(LIM10)]['rho_com_o_teto_de_antes_do_plantio'], 0)}, AG {pc(pl['AG'][str(LIM10)]['rho_com_o_teto_de_antes_do_plantio'], 0)}. O efeito plantado é")
    w(f"    {de(pl['U'][str(LIM10)]['efeito_plantado_sobre_meia_largura'], 0)} (U), {de(pl['CT'][str(LIM10)]['efeito_plantado_sobre_meia_largura'], 0)} (CT) e {de(pl['AG'][str(LIM10)]['efeito_plantado_sobre_meia_largura'], 0)} (AG) vezes a meia largura do IC. Inocente plantado (eleitor real que divide o voto como a")
    w(f"    seção): V de U vai a {mi(pl['U'][str(LIM10)]['inocente_eleitor_real_que_divide_o_voto']['V']['media'])}, sem acusar inserção.")
    cg = T['CG_amostra_de_logs']
    if 'gama' in cg:
        w(f"  CG na amostra de logs ({mi(cg['secoes_da_amostra_no_universo'])} seções, não aleatória): {cg['secoes_marcadas']} seções com reinício do aplicativo de votação, contingência, ajuste de")
        w(f"    relógio ou duas urnas no dia 25/10 (contingência ou duas urnas: {cg['so_contingencia_ou_duas_urnas']['secoes']}). Teto {mi(cg['teto'])}; gama {de(cg['gama'], 4)} (ep {de(cg['ep'], 4)}); V = {mi(cg['V'])} votos")
        w(f"    (IC 99,8% {fx(cg['ic998_V'])}). Plantio de 10% da margem da amostra: devolve {pc(cg['plantio_na_amostra']['10pct_da_margem_da_amostra']['rho'], 0)}, {de(cg['plantio_na_amostra']['10pct_da_margem_da_amostra']['efeito_sobre_meia_largura'], 1)} vezes a meia largura.")
        w(f"    Placebo do 1º turno (mesmos eventos em 04/10, {cg['placebo_CG_do_1t_contra_o_voto_do_1t']['secoes_marcadas']} seções): {de(cg['placebo_CG_do_1t_contra_o_voto_do_1t']['gama'], 4)} (ep {de(cg['placebo_CG_do_1t_contra_o_voto_do_1t']['ep'], 4)}).")
    w(f"  Veredito: {T['veredito']['veredito']}. Tetos de CD ({mi(E['CD']['teto'])}) e AM (0) abaixo de 443.019; U, CT e AG com limite superior de V abaixo de 18 mil votos;")
    w('  soma das altas de aptos de 37 mil, toda no cadastro; nenhuma seção com comparecimento acima dos aptos.')
    w('')
    # ---------------- exploratório ----------------
    ef = X['efeito_fixo_mais_largo']; cu_ = X['por_UF']['correlacoes']; lc_ = X['leitura_calibrada']; p24 = X.get('placebo_2024', {})
    w('4. EXPLORATÓRIO (feito depois de ver os resultados; não decide veredito)')
    w('  a) Efeito fixo mais largo, como pede a equipe vermelha (o efeito fixo de local é cego para inserção no prédio inteiro):')
    w(f"     gama com efeito fixo de zona {de(ef['S3_efeito_fixo_de_zona']['gama'], 3)} (ep {de(ef['S3_efeito_fixo_de_zona']['ep'], 3)}); de município {de(ef['S3_efeito_fixo_de_municipio']['gama'], 3)} (ep {de(ef['S3_efeito_fixo_de_municipio']['ep'], 3)}); de UF {de(ef['S3_efeito_fixo_de_UF']['gama'], 3)} (ep {de(ef['S3_efeito_fixo_de_UF']['ep'], 3)}).")
    w('     O sinal é NEGATIVO: entre prédios e entre cidades, onde a liberação subiu mais Lula ganhou menos (por candidato, com')
    w(f"     efeito fixo de município: Lula {de(ef['S3_efeito_fixo_de_municipio']['gama_L'], 3)}, Flávio {de(ef['S3_efeito_fixo_de_municipio']['gama_R'], 3)}). Plantio de 10% da margem em 5% dos PRÉDIOS inteiros: gama de")
    w(f"     {de(ef['plantio_de_10pct_em_5pct_dos_PREDIOS_inteiros_gama']['efeito_fixo_de_local']['media'], 3)} com efeito fixo de local (cego, como previsto) e {de(ef['plantio_de_10pct_em_5pct_dos_PREDIOS_inteiros_gama']['efeito_fixo_de_municipio']['media'], 3)} com efeito fixo de município (enxerga).")
    w(f"     a2 com efeito fixo de município: mu menos mu' = {de(ef['a2_efeito_fixo_de_municipio']['mu_menos_mulinha'])} (ep {de(ef['a2_efeito_fixo_de_municipio']['ep'])}). Bandeiras com efeito fixo de município: U {mi(ef['bandeira_U_efeito_fixo_de_municipio']['V'])} votos,")
    w(f"     CT {mi(ef['bandeira_CT_efeito_fixo_de_municipio']['V'])}, AG {mi(ef['bandeira_AG_efeito_fixo_de_municipio']['V'])} (z {de(ef['bandeira_AG_efeito_fixo_de_municipio']['z'], 1)}, a favor de Flávio).")
    n5l, n5m = ef['S3_nas_5_UFs_efeito_fixo_de_local'], ef['S3_nas_5_UFs_efeito_fixo_de_municipio']
    w(f"     Nas cinco UFs, dentro do local: Lula {de(n5l['gama_L'], 4)} (ep {de(n5l['ep_L'], 4)}), Flávio {de(n5l['gama_R'], 4)} (ep {de(n5l['ep_R'], 4)}); com efeito fixo de município: gama {de(n5m['gama'], 3)} (ep {de(n5m['ep'], 3)}).")
    w('  b) Entre as 27 UFs: o q bruto de 2026 acompanha o ganho de margem de Lula entre os turnos (correlação ' + f"{de(cu_['q_2026 x ganho_de_margem_por_C1']['pearson'], 2)}; por postos {de(cu_['q_2026 x ganho_de_margem_por_C1']['spearman'], 2)}),")
    w(f"     mas o q de 2022 das mesmas UFs acompanha o ganho de 2026 quase igual ({de(cu_['q_2022 x ganho_de_margem_por_C1']['pearson'], 2)}; {de(cu_['q_2022 x ganho_de_margem_por_C1']['spearman'], 2)}): é um padrão regional que já existia. A razão")
    w(f"     q de 2026 sobre q de 2022, que é o que forma a sobra de 737 mil, não acompanha a virada ({de(cu_['razao_q2026_sobre_q2022 x ganho_de_margem_por_C1']['pearson'], 2)}; {de(cu_['razao_q2026_sobre_q2022 x ganho_de_margem_por_C1']['spearman'], 2)}) nem a perda de Flávio")
    w(f"     ({de(cu_['razao_q2026_sobre_q2022 x perda_de_Flavio_por_R1']['pearson'], 2)}). As maiores razões estão em RS, SC, SP, TO e AC, onde Flávio venceu.")
    w(f"  c) Leitura calibrada: o gama observado está a {de(lc_['S3_distancia_em_ep_ate_o_plantio_de_10pct_concentrado'], 0)} erros-padrão do que 10% da margem inserida em 5% das seções produziria, e a")
    w(f"     {de(lc_['S3_distancia_em_ep_ate_o_plantio_de_25pct_uniforme'], 0)} do que 25% inseridos por igual produziria; mu menos mu' está a {de(lc_['a2_distancia_em_ep_ate_o_plantio_de_10pct'], 0)} erros-padrão do plantio de 10%.")
    li = X['listas']
    w(f"  d) Seções com carga da urna no próprio dia 25/10: {len(li['carga_no_dia_25_10'])}: " + '; '.join(f"{s['chave']} (margem {s['margem_1t_L_menos_R']:+d} no 1º turno e {s['margem_2t_L_menos_R']:+d} no 2º)" for s in li['carga_no_dia_25_10']) + '.')
    if 'quinze_zonas_de_maior_sobra_bruta_nas_5_UFs' in li:
        w('     Zonas de maior sobra bruta de liberações (UF|zona: liberações a mais; q), para pedido de atas e cadernos. No país: '
          + '; '.join(f"{z['zona']}: {mi(z['sobra_bruta'])}; {de(z['q'], 2)}" for z in li['vinte_zonas_de_maior_sobra_bruta_de_liberacoes_no_pais'][:8]) + '.')
        w('     Nas cinco UFs: ' + '; '.join(f"{z['zona']}: {mi(z['sobra_bruta'])}; {de(z['q'], 2)}" for z in li['quinze_zonas_de_maior_sobra_bruta_nas_5_UFs'][:8]) + '. Listas completas no JSON.')
    if 'q_2024' in p24:
        a26, a22 = p24.get('nas_mesmas_cidades_2026', {}), p24.get('nas_mesmas_cidades_2022', {})
        w(f"  e) Segundo ano de referência para q (download novo, exploratório): eleição municipal de 2024, {p24['municipios']} cidades com 2º turno,")
        w(f"     {mi(p24['secoes'])} seções de {len(p24['ufs_com_dado'])} UFs. Taxa de liberação: {pc(p24['h1'], 2)} no 1º turno e {pc(p24['h2'], 2)} no 2º: q de 2024 = {de(p24['q_2024'])} (IC 95% {fx(p24['ic95_q_2024'], de)}).")
        if a26 and a22:
            w(f"     Nas mesmas cidades: q de 2022 = {de(a22['q'])} (IC {fx(a22['ic95_q'], de)}); q de 2026 = {de(a26['q'])} (IC {fx(a26['ic95_q'], de)}).")
            w(f"     Sobra de 2026 nessas cidades com q_ref de 2024: {mi(a26['E_com_qref_de_2024'])}; bruta: {mi(a26['E_bruto_qref1'])}.")
        if 'E_de_2026_no_pais_com_qref_de_2024' in p24:
            w(f"     No país, com q_ref de 2024 no lugar do de 2022: E = {mi(p24['E_de_2026_no_pais_com_qref_de_2024'])} ({pc(p24['E_de_2026_no_pais_com_qref_de_2024'] / MARGEM, 1)} da margem; só com a incerteza de q de 2024:")
            w(f"     {fx(p24['ic95_E_de_2026_no_pais_com_qref_de_2024_so_incerteza_de_q2024'])}). A queda da taxa entre os turnos é a regra nos dois anos que têm o campo, e 2026 é a exceção.")
            m_h = D['complementos']['inclinacao_dH_em_dC_dentro_do_local']['coef'] / S1['h1'] - 1
            cmp24 = p24['variacao_C'] / p24['soma_C2'] * m_h; cmp26 = S1['variacao_C'] / S1['soma_C2'] * m_h
            w(f"     Parte é composição: o eleitor marginal é liberado {pc(m_h, 0)} mais vezes que a média; em 2024 o comparecimento caiu {pc(-p24['variacao_C'] / p24['soma_C1'], 1)} entre os")
            w(f"     turnos (efeito de {de(100 * cmp24, 1)} ponto em q) e em 2026 subiu {pc(S1['variacao_C'] / S1['soma_C1'], 1)} (efeito de +{de(100 * cmp26, 1)} ponto). Isso explica menos de um terço da distância.")
            w('     A hipótese de que a queda de 2022 fosse efeito da volta da biometria depois da pandemia não se sustenta: 2024 caiu também.')
            w('     Limite: 2024 é eleição municipal e só de cidades grandes; serve para saber se a queda é regra ou exceção, não de régua fina.')
            gu10, gu25 = PL[f'irregularidade_uniforme_{LIM10}']['gama']['media'], PL[f'irregularidade_uniforme_{LIM25}']['gama']['media']
            gE = gu10 + (gu25 - gu10) * (S1['E'] - LIM10) / (LIM25 - LIM10); gE24 = gu10 + (gu25 - gu10) * (p24['E_de_2026_no_pais_com_qref_de_2024'] - LIM10) / (LIM25 - LIM10)
            w(f"  f) Se a sobra de nível fosse voto inserido para Lula espalhado por igual, o gama seria de cerca de {de(gE24, 3)} a {de(gE, 3)} (interpolação entre os")
            w(f"     dois plantios uniformes). O observado é {de(S3['gama'], 4)} (ep {de(S3['ep'], 4)}) na conta do registro, {de(sp['gama'], 3)} com perfil e {de(ti['S3']['gama'], 3)} com os controles do 2º")
            w('     turno: de 5 a 12 erros-padrão abaixo (plantios medidos na conta do registro). A sobra tem a forma do plantio inocente')
            w('     I2 (a liberação sobe e o voto não muda), não a da inserção.')
    w('')
    w('5. TRADUÇÃO EM VOTOS DE MARGEM (voto inserido vale 1)')
    w(f"  Liberação manual acima da taxa do próprio 1º turno de 2026: {mi(S1['E_bruto_qref1'])} votos no máximo ({pc(S1['E_bruto_sobre_margem'], 1)} da margem; limite de 99%: {mi(S1['ic99_E_bruto_qref1'][1])}).")
    w(f"  Liberação manual acima do padrão de 2022: {mi(S1['E'])} ({pc(S1['E_sobre_margem'], 1)} da margem; limite de 99%: {mi(S1['ic99_E_qref_reestimado'][1])}, {pc(S1['ic99_E_qref_reestimado'][1] / MARGEM, 1)}). Mesmo lida inteira")
    w('  a favor da tese, não chega a um quarto da margem; e não tem nenhuma ligação medida com o voto.')
    if 'E_de_2026_no_pais_com_qref_de_2024' in p24:
        w(f"  Com a régua de 2024 (exploratório, 51 cidades): {mi(p24['E_de_2026_no_pais_com_qref_de_2024'])} ({pc(p24['E_de_2026_no_pais_com_qref_de_2024'] / MARGEM, 1)} da margem).")
    w(f"  Cauda de seções com liberação anormal: {mi(S2['X_mais'])} votos à direita contra {mi(S2['X_menos'])} à esquerda. Aptos acrescentados: {mi(tt['soma_das_altas_max(apt2-apt1,0)'])} no teto,")
    w(f"  compensados por {mi(tt['espelho_soma_das_quedas_max(apt1-apt2,0)'])} retirados. Urna trocada: {mi(E['U']['V'])} votos (limite {mi(E['U']['ic998_V'][1])}). Carga depois do 1º turno: {mi(E['CT']['V'])} (limite {mi(E['CT']['ic998_V'][1])}).")
    w(f"  Agregadas: {mi(E['AG']['V'])} (limite {mi(E['AG']['ic998_V'][1])}). Eleitores sem biometria como reservatório: {mi(a3['votos_implicados'])} (negativo).")
    w('')
    w('6. O QUE PESA A FAVOR DA TESE, SEM SUAVIZAR')
    w(f"  1. Contra 2022, 2026 tem {mi(S1['E'])} liberações a mais do que o padrão (IC {fx(S1['ic95_E_qref_reestimado'])}). Em 2022 a taxa caiu 7,6% do 1º")
    w('     para o 2º turno; em 2026 subiu 1,1%. Pela letra isso impede o SEM SINAL. E não é só 2022: nas 51 cidades com 2º turno')
    if 'q_2024' in p24 and p24.get('nas_mesmas_cidades_2026'):
        w(f"     em 2024 a taxa caiu {pc(1 - p24['q_2024'], 1)} (q {de(p24['q_2024'], 3)}); nas mesmas cidades caiu {pc(1 - p24['nas_mesmas_cidades_2022']['q'], 1)} em 2022 e só {pc(1 - p24['nas_mesmas_cidades_2026']['q'], 1)} em 2026. Com a régua de")
        w(f"     2024 a sobra do país é de {mi(p24['E_de_2026_no_pais_com_qref_de_2024'])} ({pc(p24['E_de_2026_no_pais_com_qref_de_2024'] / MARGEM, 0)} da margem). Em 2026 a liberação não caiu como caía, e eu não sei dizer por quê.")
    w(f"  2. A taxa de liberação subiu mais justamente onde a Onda A achou o indício: q de {de(a5['q'], 3)} nas cinco UFs contra {de(ar['q'], 3)} no resto; essas UFs têm")
    w(f"     13,5% das seções e {pc(a5['E_bruto_qref1'] / S1['E_bruto_qref1'], 0)} da sobra bruta do país. No MA e no PI a liberação subiu com o comparecimento caindo.")
    w(f"  3. O eleitor marginal foi liberado pelo mesário mais vezes que a média ({de(ic_['coef'], 3)} contra {de(ic_['fatia_H1_sobre_C1'], 3)}).")
    w(f"  4. O gama muda com os controles: com o perfil da seção fica em {de(sp['gama'], 3)} (4 ep) e com os controles do 2º turno (conta invertida) em")
    w(f"     {de(ti['S3']['gama'], 3)} (5 ep), os dois positivos. São 17 a 20 vezes menores que a marca de 10% da margem inserida (0,24).")
    w(f"  5. Há {al['secoes_z6_ou_mais']} seções com salto de liberação sem explicação nos dados (uma com 281 liberações em 314 votantes na mesma urna).")
    w('  6. Limite que vale para tudo aqui: se o programa registrasse como biométrica uma habilitação que não houve, nenhum')
    w('     destes campos mudaria. Este teste fecha a porta da mesa, não a do programa.')
    w('')
    w('7. O QUE PESA CONTRA, COM O MESMO RIGOR')
    w(f"  1. Em 2026, sem comparar com ano nenhum, a sobra é de {mi(S1['E_bruto_qref1'])} liberações, {pc(S1['E_bruto_sobre_margem'], 1)} da margem. Nas cinco UFs do indício são {mi(a5['E_bruto_qref1'])},")
    w(f"     contra {mi(a5['margem_2t'])} de margem de Lula ali.")
    w(f"  2. Onde a liberação subiu mais, Lula não ganhou mais: gama {de(S3['gama'])} (ep {de(S3['ep'])}) dentro do prédio e {de(ef['S3_efeito_fixo_de_municipio']['gama'], 3)} entre prédios da mesma")
    w("     cidade (sinal contrário; exploratório). O voto de quem foi liberado pelo mesário vale a mesma margem que o de quem passou na")
    w(f"     biometria (mu menos mu' = {de(a2['mu_menos_mulinha'], 3)}, ep {de(a2['ep'], 3)}); 10% da margem inserida daria 0,23.")
    w(f"  3. Não há cauda: {S2['secoes_cauda_direita']} seções com subida anormal contra {S2['secoes_cauda_esquerda']} com queda anormal.")
    w('  4. A sobra contra 2022 e 2024 não se comporta como voto inserido: não está onde a virada está (é maior, em proporção,')
    w('     em RS, SC, SP, TO e AC, onde Flávio venceu), não tem cauda e não tem elo com o voto. Mesmo espalhada por igual, uma')
    w('     inserção desse volume levaria gama a cerca de 0,03; o observado fica entre 0,000 e 0,014. E lida inteira a favor da')
    w('     tese ela vale de 13% a 17% da margem (limite de 99%: 22%), não a margem.')
    w(f"  5. Onde há mais eleitor sem biometria no cadastro o comparecimento subiu menos ({de(a3['coef_SB'], 3)} por eleitor).")
    w(f"  6. Aptos: {mi(tt['soma_das_altas_max(apt2-apt1,0)'])} a mais e {mi(tt['espelho_soma_das_quedas_max(apt1-apt2,0)'])} a menos, tudo igual ao cadastro; nenhuma seção com mais votos que aptos. Urna trocada, recarga e")
    w('     agregação: efeito dentro de 18 mil votos no limite mais largo, e a troca de urna foi um terço da de outros anos.')
    w('')
    w('8. O QUE ISSO SIGNIFICA PARA O INDÍCIO DO COMPARECIMENTO')
    w('  O canal do comparecimento da Onda A vale cerca de 3,35 milhões de votos de margem. Se a mesa tivesse votado no lugar de')
    w('  eleitores com biometria, esse volume teria de aparecer como liberação manual. O que aparece, medido só com 2026, são')
    w(f"  {mi(S1['E_bruto_qref1'])} liberações acima da taxa do 1º turno (limite de 99%: {mi(S1['ic99_E_bruto_qref1'][1])}); na leitura mais favorável à tese (o padrão de 2022")
    w(f"  como natural), {mi(S1['E'])} (limite de 99%: {mi(S1['ic99_E_qref_reestimado'][1])}), menos de um terço do canal, e sem ligação com o voto em nenhum desenho.")
    w('  Aptos (teto de 37 mil, compensado por quedas iguais), urna trocada, recarga e agregação (limites de 2 mil, 2 mil e 18')
    w('  mil) não somam 60 mil votos. Logo o indício da Onda A NÃO passou pela liberação da mesa nem por mudança na seção.')
    w('  Ficam de pé duas leituras: comparecimento real e desigual (o eleitor foi, pôs o dedo e')
    w('  a urna reconheceu), ou registro falso feito pelo próprio programa, que dado público não testa. O N1 mede quanto entrou')
    w('  por biometria reconhecida; o que separa as duas é caderno de votação e comprovante no e-Título.')
    w('')
    w('9. DESVIOS E DECISÕES QUE O REGISTRO NÃO FIXAVA')
    w('  1. Regras de poder L8, F4 e T8 são minhas. L8 e F4 usaram como régua os valores que o registro esperava do plantio (90%')
    w("     em A, gama de 0,6, mu menos mu' de 0,5). O plantio de 25% da margem dá 83%, 0,43 e 0,40; o mu menos mu' não chega a")
    w('     0,5 nem com a margem inteira (0,47). Por isso os rótulos SEM PODER; o rótulo pela letra do registro sai ao lado. Não')
    w('     mudei a regra depois de ver o resultado. Nos dois testes o plantio de 10% da margem NÃO seria absolvido pela letra.')
    w('  2. S1 devolve 93,8% e não 95% a 105%: é a fórmula do registro (o voto inserido aumenta também o comparecimento).')
    w('  3. IC de E com q_ref reestimado em cada réplica (mesmos municípios nos dois anos); z de S2 centrado na mediana da faixa.')
    w('  4. D4-6: universo do D4-1 para (a2) e (a3); eliminados com termo próprio: 14, 55 e 70; peso 1/aptos do 1º turno.')
    w('  5. D2-6: universo do elo sem filtro de aptos; IC de 99,8% para V; "cerimônia" da zona definida pelos dias com 5% ou')
    w('     mais das cargas; CG só na amostra antiga de logs. A bandeira AM não tem nenhuma seção.')
    w('  6. Emenda de 04:58 UTC, antes de qualquer conta: plantio do (a3).')
    w('  7. Perfil do eleitorado (a3 e complemento): reaproveitei a extração sem votos do A6, conferida pelo total.')
    w('  8. Exploratório marcado na seção 4. O placebo de 2022 usa download novo (cdn.tse.jus.br), lido em fluxo.')
    w('')
    w('10. CONTAGEM')
    w('  Estatísticas com limiar do registro: 3 no D2-1 (Q, A, gama), 3 no D4-6 a (F, mu menos mu\', a3), 6 no D2-6 (cinco bandeiras e')
    w('  aptos): 12, nenhuma em SINAL. Ao lado rodaram cerca de 90 estatísticas com erro-padrão (espelhos, placebos, UFs, regiões,')
    w('  complementos, exploratório); por acaso se esperam 4 ou 5 acima de 1,96 ep e nenhuma perto dos limiares em votos. As que')
    w('  Entre as que passam de 3 ep estão: gama de 2022 (+0,022), gama com perfil (+0,012) e com os controles do 2º turno (+0,014),')
    w('  AG dentro do local (+0,0026) e entre prédios (-0,0028), U na PB (-0,0075), o coeficiente dos eleitores sem biometria')
    w('  (-0,028) e o gama com efeito fixo largo (-0,047). Nenhuma das positivas chega a um décimo da marca de inserção.')
    txt = '\n'.join(L) + '\n'
    assert chr(8212) not in txt and chr(8211) not in txt  # sem travessão longo nem meio
    with open(SAIDA_TXT, 'w') as f: f.write(txt)
    return txt


# ----------------------------------------------------------------------------------------------------------------
# EXECUÇÃO
# ----------------------------------------------------------------------------------------------------------------
def bases(refaz=False):
    import pickle
    cache = f'{TRAB}/base2026.pkl.gz'
    if os.path.exists(cache) and not refaz:
        with gzip.open(cache, 'rb') as f: return pickle.load(f)
    x = montar_2026()
    with gzip.open(cache, 'wb', compresslevel=1) as f: pickle.dump(x, f, protocol=4)
    return x


def rodar():
    global NBOOT, NREP, SAIDA_JSON
    t0 = time.time()
    if os.environ.get('B2_TESTE'):  # ensaio rápido do código (poucas réplicas), grava fora do repositório
        NBOOT, NREP, SAIDA_JSON = 200, 2, f'{TRAB}/ensaio.json'
    B, agr1, agr2, meta = bases()
    print('base 2026', len(B['uf']), f'{time.time() - t0:.0f}s', flush=True)
    grava('parcial_meta.json', meta)
    B22, meta22 = montar_ano(2022)
    print('base 2022', len(B22['uf']), meta22.get('conferencia'), f'{time.time() - t0:.0f}s', flush=True)
    R = {'teste': 'R27_B2: liberações e mudanças na seção (D2-1 LIBERA, D2-6 TROCA e D4-6 parte a)',
         'registro': 'Adendo 27 (commit 2748895, 10/11/2026 00:16:42 UTC) e Adendo 28 (commit 938be19, 10/11/2026 04:36:33 UTC); '
                     'critérios de registro/adendo27/desenho_D2_proposta.json (D2-1, D2-6) e desenho_D4_proposta.json (D4-6 a)',
         'docstring_sha256_antes_de_rodar': open(f'{TRAB}/docstring_antes_de_rodar.sha256').read().split(),
         'escala': {'margem': MARGEM, '25pct': LIM25, '10pct': LIM10, 'comparecimento_2t': COMP2T},
         'semente': SEMENTE, 'replicas_bootstrap': NBOOT, 'repeticoes_por_plantio': NREP, 'base': meta}
    R['D2-1'], _, _ = roda_d21(B, B22, meta22, np.random.default_rng(SEMENTE))
    print('D2-1', R['D2-1']['veredito']['veredito'], f'{time.time() - t0:.0f}s', flush=True)
    R['D4-6a'] = roda_d46(B, B22, meta, np.random.default_rng(SEMENTE + 1))
    print('D4-6a', R['D4-6a']['veredito']['veredito'], f'{time.time() - t0:.0f}s', flush=True)
    anos = {2022: (B22, meta22)}
    for ano in (2018, 2014): anos[ano] = montar_ano(ano)
    R['D2-6'] = roda_d26(B, agr1, agr2, np.random.default_rng(SEMENTE + 2), anos)
    print('D2-6', R['D2-6']['veredito']['veredito'], f'{time.time() - t0:.0f}s', flush=True)
    R['exploratorio'] = {'aviso': 'feito depois de ver os resultados; não decide nenhum veredito',
                         'efeito_fixo_mais_largo': exploratorio_efeito_fixo_mais_largo(B),
                         'por_UF': exploratorio_por_uf(R, B), 'leitura_calibrada': exploratorio_leitura_calibrada(R),
                         'listas': exploratorio_listas(B)}
    R['exploratorio']['placebo_2024'] = exploratorio_placebo_2024(B, B22)
    grava('parcial_exploratorio.json', R['exploratorio'])
    R['segundos'] = round(time.time() - t0)
    R = sem_nan(R)
    with open(SAIDA_JSON + '.tmp', 'w') as f:
        json.dump(R, f, ensure_ascii=False, indent=1, default=_jsonavel, allow_nan=False)
    os.replace(SAIDA_JSON + '.tmp', SAIDA_JSON)
    print('gravado', SAIDA_JSON, flush=True)
    if not os.environ.get('B2_TESTE'): escreve_txt(R)


if __name__ == '__main__':
    modo = sys.argv[1] if len(sys.argv) > 1 else ''
    if modo == 'extrair': extrair()
    elif modo == 'baixar2022': baixar2022()
    elif modo == 'locais': locais()
    elif modo == 'logs': logs()
    elif modo == 'rodar': rodar()
    elif modo == 'txt': print(escreve_txt(json.load(open(SAIDA_JSON))))
    elif modo == 'baixar2024': exploratorio_baixar2024(int(sys.argv[2]) if len(sys.argv) > 2 else 25)
    elif modo == 'junta2024':
        R = json.load(open(SAIDA_JSON)); B, _, _, _ = bases(); B22, _ = montar_ano(2022)
        R['exploratorio']['placebo_2024'] = exploratorio_placebo_2024(B, B22)
        R = sem_nan(R)
        with open(SAIDA_JSON + '.tmp', 'w') as f: json.dump(R, f, ensure_ascii=False, indent=1, default=_jsonavel, allow_nan=False)
        os.replace(SAIDA_JSON + '.tmp', SAIDA_JSON); escreve_txt(R)
        print(json.dumps({k: v for k, v in R['exploratorio']['placebo_2024'].items() if k != 'por_UF_leitura'}, ensure_ascii=False, indent=1))
    elif modo == 'junta_listas':
        R = json.load(open(SAIDA_JSON)); B, _, _, _ = bases()
        R['exploratorio']['listas'] = exploratorio_listas(B); R = sem_nan(R)
        with open(SAIDA_JSON + '.tmp', 'w') as f: json.dump(R, f, ensure_ascii=False, indent=1, default=_jsonavel, allow_nan=False)
        os.replace(SAIDA_JSON + '.tmp', SAIDA_JSON); escreve_txt(R)
    elif modo == 'placebo2024': print(json.dumps(exploratorio_placebo_2024(), ensure_ascii=False, indent=1, default=_jsonavel))
    else: print(__doc__)
