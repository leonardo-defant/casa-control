"""R27_B4: REGRA DETERMINÍSTICA (Adendo 27, última onda, item B4).

Testes: D1.2 (pente, paredão e degrau nas contagens inteiras) e D1.3 (limiar de contagem: a urna que só age depois do
voto de número K) de registro/adendo27/desenho_D1_proposta.json, com as DEFINIÇÕES COMUNS do campo "frente"; D4-2
(pente) de registro/adendo27/desenho_D4_proposta.json; e a fragilidade "V2 (k votos por urna) e contagem do T30" de
registro/adendo27/equipe_vermelha_relatorio.json. Registro: Adendo 27 (commit 2748895, 10/11/2026 00:16:42 UTC), com a
ordem do Adendo 30 (commit a7218fb). Os critérios valem como escritos nesses arquivos.

Este docstring foi escrito ANTES de qualquer conta com votos. Até aqui só foi lida estrutura: nomes de campos, dois
registros de exemplo de cada base, totais oficiais já publicados, os campos da urna extraídos pelo desenhista
(desenho_D1/estrutura_2t.json.gz, sem votos) e o cabeçalho do perfil do eleitorado. Os desenhos D1 e D4 são cegos; o
reteste da equipe vermelha foi escrito por quem conhecia os resultados antigos (critério novo, escolha posterior ao
dado). O que o registro não fixa está abaixo como DECISÕES e sai no resultado como desvio. O que for feito depois de
ver resultado fica em funções "exploratorio_" e sai marcado como exploratório.

Uso (python3 -I scripts/analisar_R27_B4.py <modo>):
  perfil   extrai o perfil do eleitorado por seção (F15, sem votos)
  gov2t    extrai governador do 2º turno por candidato nas 6 UFs (bweb do 2º turno, cargo 3)
  base     monta as bases numéricas (2026, 2022, 2018, 2014)
  pente    D1.2(a), D4-2 e os resíduos módulo k da equipe vermelha, com nulos, placebos e plantios
  paredao  D1.2(b)
  degrau   D1.2(c)
  limiar   D1.3 e o gatilho por contagem da equipe vermelha
  relatorio  junta os parciais em resultados/R27_B4_regra_deterministica.json e .txt
Trabalho e parciais: /home/user/trabalho-eleicao/adendo27/R27_B4/

O QUE O REGISTRO FIXA (aplicado à letra)
D1, definições comuns. Universo U: seções do 2º turno de 2026 pareadas com o 1º turno pela chave, com L2 + R2 de 30 ou
  mais, fora o exterior e as 27 seções com junta apuradora. y = 100 x L2 / (L2 + R2). Modelo base: y = efeito fixo de
  local + X + b x D + erro, peso V = L2 + R2, erro agrupado por município. X: fração de cada candidato do 1º turno
  sobre o comparecimento do 1º turno (13, 22, cada um dos demais com 0,5% ou mais no país, resto agrupado), brancos,
  nulos, abstenção do 1º turno, variação da abstenção, perfil do eleitorado (faixas etárias, sexo, escolaridade,
  fração com biometria), logaritmo dos aptos e posição da seção no local. Phi = 2 x b x soma(D x V) / 100 / 4.430.191.
  y_BN = 100 x (B2 + N2) / comparecimento do 2º turno (cada voto convertido vale um voto de margem).
D1.2(a) pente. X em {R2, L2, B2, N2}; h(v) = número de seções com X = v, v de 0 a 500; curva lisa por regressão local
  quadrática com janela de 21 valores, sem o próprio ponto; e(v) = (h menos liso) / raiz(liso), v de 10 em diante (3 em
  B e N). Estatística 1: Z(p, o) = soma de e(v) nos v congruentes a o módulo p, dividida pela raiz do número de
  dentes, p de 2 a 120. Estatística 2: periodograma de e(v), frequências de 0,004 a 0,5, passo 0,0005. Nulo do máximo
  por 1.000 histogramas Poisson em torno da curva lisa. País, UF e modelo de urna.
  SINAL: máximo de Z de 8 ou mais, ou pico do periodograma acima de todos os sorteios nulos e equivalente a z de 8 ou
  mais, em R2 (ou B2 ou N2), com amplitude de 2% ou mais nos dentes, ausente no mesmo período em 2022, 2018, no 1º
  turno de 2026 e em L2. SEM SINAL: máximo de Z abaixo de 5 e periodograma dentro do quantil de 99% do nulo nas quatro
  variáveis, no país e por modelo. INCONCLUSIVO: Z entre 5 e 8, ou pico que aparece também em placebo.
  Poder: plantar R' = R menos piso(R/k), L' = L mais piso(R/k) em fração q das seções (q = 1 e k = 110; q = 1 e
  k = 56; q = 1 e k = 28; q = 0,25 e k = 7), a versão R' = piso(R x (1 menos f)), e a versão sorteada (binomial) com
  Phi = 1; exigir Z de 8 ou mais nas determinísticas. Placebos: R e L do 2º turno de 2022, 2018 e 2014; 13 e 22 no 1º
  turno de 2026; governador do 2º turno nas 6 UFs; L2.
D1.2(b) paredão. Histograma de y em faixas de 0,1 p.p., seções com L2 + R2 de 150 ou mais, contra referência simulada
  (binomial com densidade lisa e tamanhos reais); z por faixa; seções com y abaixo de 5 e acima de 95 contra o previsto
  pelo modelo base. SINAL: faixa com z de 6 ou mais fora dos picos naturais, ou cauda vazia onde o modelo previa 200
  seções ou mais. SEM SINAL: nenhuma faixa com z de 6 ou mais e caudas dentro do previsto.
D1.2(c) degrau. h(D), D = L2 menos R2 de menos 80 a mais 80; polinômio de grau 4 em log h fora de menos 10 a mais 10;
  S = log da razão entre a massa em D de 1 a 10 e a massa em D de menos 10 a menos 1, menos o previsto; z de h(0).
  SINAL: S de 0,05 ou mais em módulo com z de 5 ou mais, ausente nos placebos. SEM SINAL: S abaixo de 0,02 em módulo.
D1.3 limiar. Modelo base com D_K = max(0, 1 menos K / comparecimento do 2º turno), K em {25, 50, 75, 100, 150, 200}.
  Estimador principal: b_K de 2026 menos b_K da mesma regressão na virada de 2022 (dose e controles de 2022), erro por
  bootstrap de municípios. Estimador de joelho: 1/comparecimento como controle a mais. Média do resíduo em 25 faixas
  de comparecimento, 2026 e 2022. Mesmas contas com y_BN.
  SINAL: para algum K, Phi_K (diferença) de 0,25 ou mais a favor de Lula, z de 3,9 ou mais, joelho no mesmo sentido
  com z de 2 ou mais, mesma direção em 4 das 5 regiões. SEM SINAL: intervalo de 99% de Phi_K (diferença) entre menos
  0,15 e mais 0,15 para K de 75 a 200 e entre menos 0,25 e mais 0,25 para K = 50; K = 25 descritivo. INCONCLUSIVO: o
  resto. Poder: mover de R para L um binomial com taxa f x D_K, f para Phi = 0,10; 0,25; 0,5 e 1, 200 repetições por
  K; exigir 95% de detecção em Phi = 0,25. Placebos: virada de 2022 e de 2018; governador do 2º turno nas 6 UFs; 1º
  turno de 2026 contra 2022 com a dose do 1º turno.
D4-2 pente. H[v], v de 0 a 520; d[v] = H[v] menos a média de H[v-1] e H[v+1], padronizado por raiz(1,5 x S[v]), S a
  média móvel de 9 casas, só casas com S de 300 ou mais; periodograma somado em 3 harmônicos; Z = máximo sobre períodos
  de 8 a 150 (passo 0,02). Nulo: 1.000 histogramas multinomiais da curva lisa (média móvel de 13). R2 e L2 nacionais
  (primário), B2 e N2, R2 e L2 por UF e por três faixas de tamanho, com limiar do máximo do nulo sobre os recortes.
  SINAL: Z de R2 ou L2 nacional acima de 1,5 vez o máximo do nulo e de 1,5 vez o maior placebo, pico entre 8 e 150 e
  harmônicos coerentes; em recorte, o mesmo com o limiar do conjunto. SEM SINAL: Z de R2 e de L2 abaixo do percentil 99
  do nulo e abaixo do maior placebo, no país e em todos os recortes. INCONCLUSIVO: entre os dois, ou pico só em recorte
  pequeno. Poder: as trocas do desenho plantadas em R1 de 2026 e em R2 de 2022. Placebos: comparecimento dos dois
  turnos e aptos de 2026; L1 e R1 de 2026; L e R dos dois turnos de 2014, 2018 e 2022.
Equipe vermelha. Histograma de Flávio, Lula, brancos e nulos no 2º turno, resíduos módulo k para k de 2 a 200 contra
  ajuste suave, comparado com o 1º turno e com 200 sorteios binomiais; plantar "um a cada 28 votos de Flávio".
  SINAL: algum k com excesso de 3% ou mais numa classe de resíduo e p abaixo de 1e-6 depois de Bonferroni (796
  testes), ausente no 1º turno. SEM SINAL: estatística máxima abaixo do percentil 99 das simulações em todos os k e o
  caso plantado detectado com z acima de 20. Gatilho por contagem com N de 50 a 300 de 25 em 25, com controle de log
  do tamanho (o reteste não traz critério próprio para esta parte; vale o do T30, Adendo 9).

DECISÕES QUE O REGISTRO NÃO FIXA (tomadas aqui, antes de calcular qualquer coisa com votos)
Gerais
G1. U como nas definições comuns. Junta = NR_JUNTA_APURADORA igual a 1 na estrutura do 2º turno. U serve a D1.2 (a, b,
    c), a D1.3 e aos resíduos módulo k. O D4-2 não define universo e o código do desenhista usa todas as seções com 2º
    turno, exterior incluído: o D4-2 usa todas. Sensibilidade do pente D1.2(a) com todas as seções do Brasil.
G2. Outros anos: seções com os dois turnos na chave, L2 + R2 de 30 ou mais, fora o exterior e as de tipo anulada. As
    bases de 2014 a 2022 não trazem a junta apuradora.
G3. Governador do 2º turno: G1 = candidato mais votado da UF, G2 = o outro; histogramas das 6 UFs juntas, nas seções
    de U.
G4. Modelo de urna: número de série da urna do 2º turno, faixas de 2026 de scripts/modelos.py.
G5. Semente 20261110 (geradores separados por etapa). Regiões: Norte (AC AM AP PA RO RR TO), Nordeste (AL BA CE MA PB PE
    PI RN SE), Sudeste (ES MG RJ SP), Sul (PR RS SC), Centro-Oeste (DF GO MS MT).
G6. SEM PODER: qualquer parte em que o efeito plantado do tamanho que o registro manda enxergar não for enxergado
    pela mesma conta. O veredito sai por parte; não há veredito único somado.
Pente D1.2(a)
P1. h(v) é contado de 0 a 510 para a janela existir até v = 500; seção com X acima de 510 fica fora (contada).
P2. Curva lisa em v: mínimos quadrados de um polinômio de grau 2 em (u menos v) nos inteiros u de max(0, v menos 10)
    a v mais 10, sem u = v, pesos iguais; o liso é o valor ajustado em v.
P3. e(v) entra para v do mínimo da letra (10; 3 em B e N) até 500, e só nas casas com liso de 30 seções ou mais (abaixo
    disso a raiz não padroniza e o liso pode ficar negativo). As casas usadas são relatadas.
P4. Z(p, o) só com 2 ou mais dentes dentro das casas usadas. A estatística é o maior |Z|: excesso (dente) e falta
    (buraco) contam igual, e o sinal de Z é relatado. Amplitude nos dentes = soma de (h menos liso) / soma do liso nos
    dentes de (p, o).
P5. Periodograma P(f) = |soma de e(v) x exp(menos 2 pi i f v)|^2 / n, n = casas usadas. "Equivalente a z" = z normal
    com a mesma probabilidade de cauda dos dois lados: 2 x (1 menos Fi(z)) = exp(menos P); z de 8 corresponde a P de
    34,3. Amplitude do pico = 2 x |soma de ((h menos liso)/liso) x exp(menos 2 pi i f v)| / n.
P6. Nulo: 1.000 histogramas com h*(v) Poisson de média igual ao liso (para v abaixo do mínimo da letra, média igual ao
    h observado; liso negativo vira zero), cada um refeito pela mesma conta e com as mesmas casas. Saem o máximo de |Z|
    e o máximo de P de cada sorteio, o quantil de 99% e o maior valor.
P7. "Ausente no mesmo período": o placebo está "presente" se, no mesmo (p, o), tiver |Z| de 5 ou mais com o mesmo
    sinal; para pico de periodograma, se o P do placebo em f mais ou menos 0,001 passar do quantil de 99% do nulo do
    próprio placebo. Placebos de R2: R do 2º turno de 2022, 2018 e 2014, o 22 no 1º turno de 2026 e L2. Para B2 e N2
    (a letra não lista): a mesma variável no 2º turno de 2022, 2018 e 2014 e no 1º turno de 2026.
P8. Rodadas: país; 4 modelos de urna; 27 UFs; as 4 variáveis em cada uma. O critério SEM SINAL usa país e modelos (20
    rodadas), como na letra. O critério SINAL vale em qualquer rodada (um recorte com a regra apareceria ali). L2 com
    as condições numéricas de sinal e R2 sem elas é relatado como sinal espelho (a favor de Flávio), com o mesmo
    destaque. UF sem nenhuma casa usada fica "não avaliável".
P9. Veredito por variável e combinado, nesta ordem: SEM PODER (G6: algum plantio determinístico da letra com |Z| abaixo
    de 8 em R2 no país); SINAL; SEM SINAL; INCONCLUSIVO.
P10. Plantios em cópia de 2026 (U): os quatro pares (q, k) da letra; fração arredondada R' = piso(R x (1 menos f)),
    L' = L + R menos R', com f = Phi x 0,0357 para Phi = 0,25; 0,5; 1; binomial com Phi = 1 (ponto cego); os mesmos de
    L para R (espelho); e conversão determinística em brancos e em nulos, X' = X menos piso(X/k), k = 3, 5 e 10. Para
    cada um: votos movidos, Phi efetivo, |Z| máximo, (p, o), amplitude, P máximo.
P11. Viés previsto antes do dado: em B e N as contagens são pequenas (média de poucos votos por seção) e a regressão
    quadrática de 21 valores não acompanha a subida e a queda do histograma perto de v = 3; isso gera resíduo grande
    sem período, que entra em Z e em P e aparece igual nos placebos. A letra é aplicada mesmo assim. Complemento
    declarado agora para B e N (e rodado também em R e L): quarta diferença do logaritmo, q(v) = [6 ln h(v) menos
    4 ln h(v-1) menos 4 ln h(v+1) + ln h(v-2) + ln h(v+2)] / 6, que zera para curva suave e vale ln(1 + a) num dente
    de amplitude a; erro por Poisson. "Dente" = |q| de 0,02 ou mais com |z| de 8 ou mais em algum v de 3 em diante com
    h de 400 ou mais, sem o mesmo no 1º turno de 2026. Este complemento não muda o veredito da letra; é a leitura
    oferecida se a letra der INCONCLUSIVO em B e N só por viés de alisamento presente também nos placebos.
Paredão D1.2(b)
B1. Seções de U com V de 150 ou mais. Faixa = parte inteira de 10 x y (y = 100 fica na faixa 1000).
B2. Referência: 400 simulações; em cada uma p_i = y_i/100 + normal de desvio 0,01 (limitado a 0 e 1) e L* binomial de
    (V_i, p_i). A densidade lisa é a de y alisada por núcleo normal de 1 p.p., condicionada ao tamanho real da própria
    seção (mantém a relação entre tamanho e fração). z = (observado menos média simulada) / raiz(max(variância
    simulada, média simulada, 1)). Faixa com média simulada abaixo de 20 é relatada mas não decide.
B3. Picos naturais: faixas que contêm 100 x a/b com b de 1 a 12 (inclui 0 e 100).
B4. Caudas: seções com V de 150 ou mais e y abaixo de 5 ou acima de 95, contra a previsão do modelo base (sem dose):
    200 simulações com y* = 100 x binomial(V, p)/V, p = ajustado/100 + normal de variância tau2, tau2 pelo excesso da
    variância do resíduo sobre a binomial (com correção de graus de liberdade). Como o efeito fixo de local absorve o
    nível do prédio e torna a previsão quase circular, vai ao lado a mesma conta com efeito fixo de UF no lugar do
    local. "Dentro do previsto" = razão observado/previsto entre 0,5 e 2 (decide só onde o previsto é de 200 ou mais).
B5. Veredito: SEM PODER se o teto plantado não der faixa com z de 6 ou mais; SINAL se houver faixa com z de 6 ou mais
    (excesso) fora dos picos naturais, ou cauda vazia com 200 ou mais previstos; SEM SINAL se nenhuma faixa fora dos
    picos naturais tiver |z| de 6 ou mais e as caudas estiverem dentro do previsto; INCONCLUSIVO no resto (inclui
    faixa com z de menos 6 ou abaixo).
B6. Plantios: teto de 85% para Flávio (em toda seção com y abaixo de 15, votos passam de R para L até y chegar a 15)
    em todas as seções e em 20% delas; espelho (teto de 85% para Lula). Tradução: votos que um teto em 95, 90, 85, 80
    e 70% moveria nos dados observados.
B7. Placebos: a mesma conta no 2º turno de 2022, 2018 e 2014 e no 1º turno de 2026 (L1 e R1).
Degrau D1.2(c)
C1. h(D) em U. Ajuste por mínimos quadrados ponderados (peso h) de ln h num polinômio de grau 4 em D/80, com |D| de 11
    a 80. S = ln(M+ / M-) menos ln(P+ / P-), M = massa observada e P = massa prevista em D de 1 a 10 e de menos 10 a
    menos 1. Erro de S por 1.000 reamostragens Poisson de h com novo ajuste; z = S / desvio. z de h(0) = (h(0) menos
    previsto) / raiz(previsto).
C2. Placebos: 2º turno de 2022, 2018 e 2014; 1º turno de 2026 (L1 menos R1); governador do 2º turno (G1 menos G2).
    "Ausente nos placebos" = nenhum placebo com |S| de 0,05 ou mais e |z| de 5 ou mais.
C3. Plantio: em fração q das seções com D de menos 10 a menos 1, passam de R para L os votos que bastam para Lula
    ficar na frente (D vira 1 ou 2); q = 0,025; 0,05; 0,10. Espelho: o mesmo de L para R nas seções com D de 1 a 10.
    SEM PODER se o plantio de q = 0,025 (S esperado de 0,05) não mover S em 5 erros ou mais.
C4. Veredito: SEM PODER; SINAL (|S| de 0,05 ou mais, |z| de 5 ou mais, ausente nos placebos); SEM SINAL (|S| abaixo de
    0,02); INCONCLUSIVO no resto.
Limiar D1.3
L1. X de 2026: frações sobre o comparecimento do 1º turno do 13, do 22 e de cada candidato com 0,5% ou mais do
    comparecimento nacional do 1º turno (resto = referência), brancos e nulos; abstenção do 1º turno; abstenção do 2º
    menos a do 1º; perfil (fração de mulheres; 8 faixas de idade, referência 35 a 44; 8 graus de escolaridade,
    referência médio completo; fração com biometria; em seção com agregadas, soma da principal com as agregadas);
    ln dos aptos do 2º turno; posição = (ordem pelo número da seção no local menos 1) / (seções do local menos 1).
    Seção sem perfil sai (contada). Local com uma só seção não informa. Coluna sem variação dentro dos locais sai.
L2. Regressão de 2022: mesmas definições com os dados de 2022 (frações de L, R, brancos e nulos do 1º turno de 2022,
    outros = referência; abstenção e variação de 2022; ln dos aptos e posição de 2022; dose pelo comparecimento do 2º
    turno de 2022; efeito fixo do local de 2022; peso V de 2022). O perfil só existe para 2026: entra o perfil de 2026
    da mesma chave, e a seção de 2022 sem chave em 2026 sai (contada). Motivo: o desenho usa o perfil etário para
    separar a explicação inocente, então as duas regressões precisam do mesmo controle. Sensibilidade: as duas sem
    perfil. Para 2018, igual.
L3. Estimador principal = b_K(2026) menos b_K(2022). Erro: 500 reamostragens de municípios com reposição, o mesmo
    sorteio aplicado aos dois anos (município = UF mais código). z = diferença / desvio das reamostragens; intervalo
    de 99% = diferença mais ou menos 2,5758 desvios. Phi_K (diferença) = 2 x diferença x soma em U de (D_K x V) / 100
    / 4.430.191, com a exposição de 2026. Erro analítico agrupado por município (CR1) ao lado.
L4. Joelho: b_K com 1/comparecimento do 2º turno como controle, em 2026, erro CR1 por município; "mesmo sentido com z
    de 2 ou mais" refere-se a esse b de 2026. A diferença do joelho contra 2022 vai ao lado.
L5. Regiões: a diferença b_K(2026) menos b_K(2022) estimada dentro de cada região; "mesma direção" = mesmo sinal da
    nacional.
L6. y_BN: mesmas contas e mesmo peso V. Phi_BN = menos diferença / 100 x soma(D_K x comparecimento do 2º turno) /
    4.430.191 (positivo = brancos e nulos caem com a dose, sentido da conversão). Limites iguais aos de y.
L7. Calibração: T binomial(R2, f x D_K) passa de R para L, f = Phi x 2.215.096 / soma(D_K x R2), Phi em {0,10; 0,25;
    0,5; 1}, 200 repetições por K e Phi. Como V não muda, só y muda. Detecção = (b da cópia menos b observado) / erro
    do estimador principal de 3,9 ou mais. Recuperação = média do deslocamento / b que corresponde a Phi. Espelho: o
    mesmo de L para R com Phi = 0,25. Para o joelho: (deslocamento do b de joelho) / erro do joelho de 2 ou mais.
    y_BN: T binomial(B2 + N2, f x D_K) sai de brancos e nulos, para Phi_BN = 0,10 e 0,25 (peso mantido em V).
    Explicação inocente plantada (seção pequena diferente, sem joelho): mesma transferência com dose suave
    D_s = ln(comparecimento/20)/ln(20), limitada a 0 e 1, no total de Phi = 0,25 e 0,5; mede-se quanto o estimador
    principal e o de joelho se movem em cada K. O esperado, se o desenho funciona: o principal acusa e o joelho não.
L8. SEM PODER para um K se a detecção em Phi = 0,25 ficar abaixo de 95%. Veredito de D1.3: SINAL se algum K de 50 a 200
    cumprir tudo (sentido contrário relatado igual); SEM SINAL se os cinco intervalos couberem nos limites e todos
    tiverem poder; SEM PODER se os limites couberem mas faltar poder; INCONCLUSIVO no resto.
L9. Placebos: (i) b_K da virada de 2018 e as diferenças 2026 menos 2018 e 2022 menos 2018 (esta última sem 2026,
    mostra quanto o estimador oscila sozinho); (ii) governador do 2º turno, uma regressão por UF: desfecho 100 x
    G1/(G1+G2), X de presidente do 1º turno mais as frações de G1 e de G2 no 1º turno de governador, mesma dose, erro
    por local; resumo por inverso da variância; (iii) 1º turno de 2026 contra 2022: desfecho 100 x L1/(L1+R1), dose
    pelo comparecimento do 1º turno, controles: fração de Lula no 2º turno de 2022, frações de L, R, brancos e nulos
    do 1º turno de 2022, abstenção do 1º turno de 2022, abstenção do 1º de 2026 menos a do 1º de 2022, perfil, ln dos
    aptos, posição; peso L1 + R1; seções de U com chave em 2022.
L10. Tabela no lugar da figura: resíduo médio do modelo base sem dose em 25 faixas de comparecimento do 2º turno
    (quantis ponderados por seção), 2026 e 2022.
D4-2
Q1. Estatística refeita com código próprio a partir da descrição: casas de 0 a 519, reflexão nas bordas da média
    móvel, primeira e última casa fora. Universo: todas as seções com 2º turno (G1). "Três faixas de tamanho": tercis
    do comparecimento do 2º turno. UF: as 27 e o exterior (ZZ) à parte.
Q2. Nulo de cada histograma: 1.000 multinomiais da média móvel de 13 casas. Nulo do conjunto de recortes: em cada
    sorteio, o maior Z entre os recortes (27 UFs, exterior e 3 faixas; R2 e L2); limiar de sinal = 1,5 x o maior desses
    máximos; percentil 99 desses máximos para o critério SEM SINAL. Recorte sem casa com S de 300 ou mais não é
    avaliável.
Q3. Placebos (17): comparecimento do 2º turno, do 1º turno e aptos de 2026; L1 e R1 de 2026; L e R dos dois turnos de
    2014, 2018 e 2022. "Maior placebo" = o maior Z desses 17.
Q4. "Harmônicos coerentes" = pelo menos 2 dos 3 termos do pico acima de 6,9 cada (cauda de 0,001).
Q5. Plantios do desenho em R1 de 2026, em R2 de 2022 e, pelo pedido de calibração em 2026, em R2 de 2026: piso de
    3,57% em todas, em 50%, 20% e 10% das seções; piso de 1,8% em todas, 50% e 20%; piso de 1% em todas e em 50%;
    arredondamento de 3,57%; inflar o beneficiado em 3,45% dos próprios votos (em L); binomial de 3,57%; piso de 1,8%
    do comparecimento. SEM PODER se o piso de 3,57% em todas, plantado em R2 de 2026, não passar de 1,5 x o máximo do
    nulo.
Q6. Veredito: SEM PODER; SINAL; SEM SINAL; INCONCLUSIVO, pela letra.
Equipe vermelha, resíduos módulo k
E1. Universo U; variáveis R2, L2, B2, N2 e, para a comparação, R1, L1, B1, N1 nas mesmas seções. Histograma, curva lisa
    e casas usadas como em P1 a P3. Para k de 2 a 200 e classe r: O = soma de h, E = soma do liso nas casas da classe;
    z = (O menos E) / raiz(E); excesso = O/E menos 1.
E2. "200 sorteios binomiais": por seção, X* binomial(n_i, p_i), n_i = comparecimento do turno, p_i = [m_i + raiz(s) x
    (X_i menos m_i)] / n_i, m_i = n_i x taxa do município, s = 1 menos soma de X(1 menos X/n) / soma de (X menos m)^2
    (encolhimento que mantém a variância do histograma; sem ele o sorteio alargaria B e N). Cada sorteio passa pela
    mesma conta. Correção: zc(k, r) = (z observado menos média dos sorteios) / desvio dos sorteios; excesso corrigido
    = excesso menos a média dos sorteios. Isso desconta o viés de alisamento de P11.
E3. Estatística por k: T(k) = maior zc entre as classes (excesso). p de k = k x cauda normal superior de T(k); depois
    de Bonferroni = 796 x p. SINAL: algum k com excesso corrigido de 3% ou mais na classe de T(k) e p corrigido abaixo
    de 1e-6, sem o mesmo (mesmo k, mesma classe, mesmas duas condições) na variável do 1º turno.
E4. "Estatística máxima abaixo do percentil 99 das simulações em todos os k": lida como o maior T(k) sobre k, por
    variável, contra o percentil 99 do maior T(k) de cada sorteio (cada sorteio corrigido pelos outros 199). A leitura
    alternativa (cada k contra o percentil 99 do próprio k) vai ao lado com o número de k que passam; com 199 testes a
    1% por variável ela dá cerca de 2 passagens por acaso e quase nunca daria SEM SINAL.
E5. Plantio: R' = R menos piso(R/28), L' = L mais piso(R/28) em todas as seções; "detectado com z acima de 20" = zc da
    classe 0 de k = 27 (o período do dente) em R2 acima de 20, com média e desvio dos sorteios sem plantio.
E6. Veredito: SEM PODER se o plantio não passar de 20; SINAL; SEM SINAL; INCONCLUSIVO no resto.
Equipe vermelha, gatilho por contagem
T1. Conta do T30 (Adendo 9) no bweb inteiro: (fatia de Lula do 2º turno menos a do 1º, em pontos) contra
    x_N = max(0, votantes menos N)/votantes do 2º turno, N de 50 a 300 de 25 em 25, controlando a variação do
    comparecimento (100 x (comp2 menos comp1)/aptos) e ln(votantes do 2º turno), efeito fixo de local, peso L2 + R2,
    erro agrupado por local (lib.fe_ols, como no T30). Universo U. Placebo: 2022.
T2. Critério do T30 com Bonferroni para 11 cortes: SINAL se coeficiente de 4 pontos ou mais com z de 3,32 ou mais
    (1% bilateral dividido por 11) e |coeficiente de 2022| abaixo de 1,5; SEM SINAL se |coeficiente| de até 1,5 em
    todos os cortes; INCONCLUSIVO no resto. Calibração: os plantios de L7 (Phi = 0,25 e 1, K = 100 e 200), 20
    repetições, para dizer quanto do coeficiente corresponde a que fração da margem; SEM PODER se o plantio de
    Phi = 1 mover o coeficiente menos de 3,32 erros.
Obrigatórios do pedido
O1. Valor bruto de 2026 ao lado de toda comparação com outro ano; onde o veredito depende de outro ano (D1.3 pela
    diferença contra 2022; placebos do pente, do degrau e do paredão), isso é dito no veredito.
O2. Espelho: L2 no pente; plantios de L para R; sentido contrário de Phi em D1.3; S negativo no degrau; teto para
    Lula no paredão.
O3. Tradução em votos: Phi x 2.215.096 votos trocados = Phi x 4.430.191 de margem; para o pente, a fração da margem
    que a menor regra plantada e enxergada representa.
O4. Contagem de estatísticas com limiar e de quantos sinais o acaso daria.
"""
import sys, os, gzip, json, zipfile, glob, time, hashlib, math
import numpy as np

RAIZ = '/home/user/casa-control/eleicao-2026'
DADOS = RAIZ + '/dados'
TRAB = '/home/user/trabalho-eleicao/adendo27/R27_B4'
D1DIR = '/home/user/trabalho-eleicao/adendo27/desenho_D1'
PERFIL_DIR = '/home/user/trabalho-eleicao/adendo21/F15_dl_perfil_secao'
ZIPS2T = '/home/user/trabalho-eleicao/trab2t/zips2t'
SAIDA_JSON = RAIZ + '/resultados/R27_B4_regra_deterministica.json'
SAIDA_TXT = RAIZ + '/resultados/R27_B4_regra_deterministica.txt'
sys.path.insert(0, RAIZ + '/scripts')

SEMENTE = 20261110
MARGEM = 4430191
NECESSARIO = 2215096
L2_OFICIAL, R2_OFICIAL = 64256232, 59826041
Z99 = 2.5758293035489
UFS_GOV = ['AC', 'AM', 'DF', 'ES', 'RN', 'TO']
REGIOES = {'Norte': ['AC', 'AM', 'AP', 'PA', 'RO', 'RR', 'TO'],
           'Nordeste': ['AL', 'BA', 'CE', 'MA', 'PB', 'PE', 'PI', 'RN', 'SE'],
           'Sudeste': ['ES', 'MG', 'RJ', 'SP'], 'Sul': ['PR', 'RS', 'SC'], 'Centro-Oeste': ['DF', 'GO', 'MS', 'MT']}
UF_REGIAO = {u: r for r, us in REGIOES.items() for u in us}
COLS_PERFIL = ['total', 'biometria', 'mulheres', 'i1617', 'i1824', 'i2534', 'i3544', 'i4559', 'i6069', 'i7079', 'i80m',
               'e1', 'e2', 'e3', 'e4', 'e5', 'e6', 'e7', 'e8']
FAIXAS_IDADE = {'i1617': [1600, 1700], 'i1824': [1800, 1900, 2000, 2124], 'i2534': [2529, 3034], 'i3544': [3539, 4044],
                'i4559': [4549, 5054, 5559], 'i6069': [6064, 6569], 'i7079': [7074, 7579],
                'i80m': [8084, 8589, 9094, 9599, 9999]}


def grava(nome, obj):
    os.makedirs(TRAB, exist_ok=True)
    tmp = f'{TRAB}/{nome}.tmp'
    with open(tmp, 'w') as f:
        json.dump(obj, f, ensure_ascii=False, indent=1, default=_jsonavel)
    os.replace(tmp, f'{TRAB}/{nome}')


def _jsonavel(o):
    if isinstance(o, (np.integer,)):
        return int(o)
    if isinstance(o, (np.floating,)):
        return float(o)
    if isinstance(o, np.bool_):
        return bool(o)
    if isinstance(o, np.ndarray):
        return o.tolist()
    raise TypeError(str(type(o)))


def le(nome):
    with open(f'{TRAB}/{nome}') as f:
        return json.load(f)


def log(*a):
    print(time.strftime('%H:%M:%S'), *a, flush=True)


# ---------------------------------------------------------------------------------------------------------------
# Extrações sem voto de presidente: perfil do eleitorado e governador do 2º turno
# ---------------------------------------------------------------------------------------------------------------
def _perfil_uf(caminho):
    import pandas as pd
    uf = os.path.basename(caminho)[:-4].split('_')[-1]
    acum = None
    with zipfile.ZipFile(caminho) as zf:
        nome = [i.filename for i in zf.infolist() if i.filename.lower().endswith('.csv')][0]
        with zf.open(nome) as f:
            for ch in pd.read_csv(f, sep=';', encoding='latin-1', chunksize=1000000,
                                  usecols=['CD_MUNICIPIO', 'NR_ZONA', 'NR_SECAO', 'CD_GENERO', 'CD_FAIXA_ETARIA',
                                           'CD_GRAU_ESCOLARIDADE', 'QT_ELEITORES', 'QT_ELEITORES_BIOMETRIA']):
                q = ch['QT_ELEITORES'].to_numpy()
                fx = ch['CD_FAIXA_ETARIA'].to_numpy(); es = ch['CD_GRAU_ESCOLARIDADE'].to_numpy()
                t = {'total': q, 'biometria': ch['QT_ELEITORES_BIOMETRIA'].to_numpy(),
                     'mulheres': q * (ch['CD_GENERO'].to_numpy() == 4)}
                for nm, cods in FAIXAS_IDADE.items():
                    t[nm] = q * np.isin(fx, cods)
                for e in range(1, 9):
                    t[f'e{e}'] = q * (es == e)
                df = pd.DataFrame(t)
                df['m'] = ch['CD_MUNICIPIO'].to_numpy(); df['z'] = ch['NR_ZONA'].to_numpy(); df['s'] = ch['NR_SECAO'].to_numpy()
                g = df.groupby(['m', 'z', 's'])[COLS_PERFIL].sum()
                acum = g if acum is None else acum.add(g, fill_value=0)
    return {f'{uf}|{int(m)}|{int(zn)}|{int(s)}': [int(x) for x in v] for (m, zn, s), v in zip(acum.index, acum.values)}


def modo_perfil():
    from multiprocessing import Pool
    os.makedirs(TRAB, exist_ok=True)
    zips = [z for z in sorted(glob.glob(PERFIL_DIR + '/perfil_eleitor_secao_2026_*.zip')) if not z.endswith('_ZZ.zip')]
    zips.sort(key=os.path.getsize, reverse=True)
    out = {}
    with Pool(3) as p:
        for r in p.imap_unordered(_perfil_uf, zips):
            out.update(r)
            log('perfil', len(out))
    with gzip.open(TRAB + '/perfil_secao_B4.json.gz', 'wt') as f:
        json.dump({'colunas': COLS_PERFIL, 'secoes': out}, f, separators=(',', ':'))
    log('perfil: secoes', len(out), 'eleitores', sum(v[0] for v in out.values()), 'biometria', sum(v[1] for v in out.values()))


def modo_gov2t():
    """Governador do 2º turno por candidato, 6 UFs. Linhas filtradas por bytes antes do csv."""
    import csv, io
    os.makedirs(TRAB, exist_ok=True)
    out = {}
    for uf in UFS_GOV:
        zp = glob.glob(f'{ZIPS2T}/bweb_2t_{uf}_*.zip')[0]
        with zipfile.ZipFile(zp) as z:
            nome = [n for n in z.namelist() if n.lower().endswith('.csv')][0]
            with z.open(nome) as fh:
                cab = fh.readline().decode('latin1')
                ix = {c.strip().strip('"'): i for i, c in enumerate(cab.split(';'))}
                linhas = [l for l in fh if b';3;"Governador";' in l]
        for r in csv.reader(io.StringIO(b''.join(linhas).decode('latin1')), delimiter=';'):
            if r[ix['CD_CARGO_PERGUNTA']] != '3' or r[ix['DS_TIPO_VOTAVEL']] != 'Nominal':
                continue
            k = f"{uf}|{int(r[ix['CD_MUNICIPIO']])}|{int(r[ix['NR_ZONA']])}|{int(r[ix['NR_SECAO']])}"
            out.setdefault(k, {})[r[ix['NR_VOTAVEL']]] = out.get(k, {}).get(r[ix['NR_VOTAVEL']], 0) + int(r[ix['QT_VOTOS']])
        log('gov2t', uf, sum(1 for k in out if k.startswith(uf + '|')))
    with gzip.open(TRAB + '/gov2t_6ufs_B4.json.gz', 'wt') as f:
        json.dump(out, f, separators=(',', ':'))
    tot = {}
    for k, v in out.items():
        for c, q in v.items():
            tot[(k[:2], c)] = tot.get((k[:2], c), 0) + q
    log('gov2t totais', sorted(tot.items()))


# ---------------------------------------------------------------------------------------------------------------
# Bases numéricas
# ---------------------------------------------------------------------------------------------------------------
def _carrega_json(caminho):
    with gzip.open(caminho, 'rt') as f:
        return json.load(f)


def _base_ano(ano):
    d = _carrega_json(f'{DADOS}/secoes{ano}.json.gz')
    ks = [k for k, v in d.items() if '2' in v and '1' in v and str(v['2'].get('tipo', '')).lower() == 'apurada']
    n = len(ks)
    o = {'chave': np.array(ks), 'uf': np.array([k.split('|')[0] for k in ks]),
         'mun': np.array(['|'.join(k.split('|')[:2]) for k in ks]),
         'secao': np.array([int(k.split('|')[3]) for k in ks]),
         'loc': np.array(['|'.join(k.split('|')[:3]) + '|' + str(d[k]['2']['loc']) for k in ks])}
    for t in ('1', '2'):
        for c in ('apt', 'comp', 'L', 'R', 'O', 'B', 'N'):
            o[c + t] = np.array([d[k][t][c] for k in ks], dtype=np.int64)
    o['so2'] = np.array([n, sum(1 for v in d.values() if '2' in v)])
    return o


def modo_base():
    from modelos import modelo as modelo_urna
    os.makedirs(TRAB, exist_ok=True)
    for ano in (2022, 2018, 2014):
        o = _base_ano(ano)
        np.savez_compressed(f'{TRAB}/base_{ano}.npz', **o)
        log(ano, 'secoes pareadas', len(o['chave']), 'com 2T', int(o['so2'][1]), 'L2', int(o['L2'].sum()), 'R2', int(o['R2'].sum()))
    d = _carrega_json(f'{DADOS}/secoes2026.json.gz')
    est = _carrega_json(f'{D1DIR}/estrutura_2t.json.gz')
    cand = _carrega_json(f'{DADOS}/candidatos2026_1t.json.gz')
    ks = [k for k, v in d.items() if '2' in v]
    n = len(ks)
    o = {'chave': np.array(ks), 'uf': np.array([k.split('|')[0] for k in ks]),
         'mun': np.array(['|'.join(k.split('|')[:2]) for k in ks]),
         'secao': np.array([int(k.split('|')[3]) for k in ks]),
         'loc': np.array(['|'.join(k.split('|')[:3]) + '|' + str(d[k]['2']['loc']) for k in ks]),
         'pareada': np.array(['1' in d[k] for k in ks]),
         'junta': np.array([est[k][16] == '1' for k in ks]),
         'urna2': np.array([int(d[k]['2']['urna']) for k in ks], dtype=np.int64)}
    o['modelo'] = np.array([modelo_urna(int(u), 2026) or 'outro' for u in o['urna2']])
    for c in ('apt', 'comp', 'L', 'R', 'O', 'B', 'N'):
        o[c + '2'] = np.array([d[k]['2'][c] for k in ks], dtype=np.int64)
        o[c + '1'] = np.array([d[k]['1'][c] if '1' in d[k] else 0 for k in ks], dtype=np.int64)
    comp1_nac = sum(v['1']['comp'] for v in d.values() if '1' in v)
    maiores = sorted(c for c, t in cand['totais'].items() if c not in ('13', '22') and t / comp1_nac >= 0.005)
    for c in maiores:
        o['c' + c] = np.array([cand['secoes'].get(k, {}).get(c, 0) for k in ks], dtype=np.int64)
    o['maiores'] = np.array(maiores)
    # perfil, somando as agregadas
    pf = _carrega_json(f'{TRAB}/perfil_secao_B4.json.gz')['secoes']
    P = np.zeros((n, len(COLS_PERFIL)), dtype=np.int64); tem = np.zeros(n, bool); nag = 0
    for i, k in enumerate(ks):
        uf, mun, zona, sec = k.split('|')
        secs = [sec]
        ag = est[k][15]
        if ag and not ag.startswith('#'):
            secs += [s.strip() for s in ag.replace(';', '/').replace(',', '/').split('/') if s.strip()]
            nag += 1
        for s in secs:
            v = pf.get(f'{uf}|{mun}|{zona}|{int(s)}')
            if v is not None:
                P[i] += v; tem[i] = True
    o['perfil'] = P; o['tem_perfil'] = tem
    # governador: 1º turno (B, N e os dois finalistas) e 2º turno por candidato
    g2 = _carrega_json(f'{TRAB}/gov2t_6ufs_B4.json.gz')
    g1 = _carrega_json(f'{DADOS}/candidatos_gov_2026_1t_6ufs.json.gz')['secoes']
    tot = {}
    for k, v in g2.items():
        for c, q in v.items():
            tot.setdefault(k.split('|')[0], {}).setdefault(c, 0)
            tot[k.split('|')[0]][c] += q
    fin = {uf: [c for c, _ in sorted(t.items(), key=lambda x: -x[1])[:2]] for uf, t in tot.items()}
    G = np.zeros((n, 6), dtype=np.int64)  # G1_2t, G2_2t, G1_1t, G2_1t, B_1t, N_1t
    for i, k in enumerate(ks):
        uf = k.split('|')[0]
        if uf in fin and k in g2:
            a, b = fin[uf]
            G[i, 0] = g2[k].get(a, 0); G[i, 1] = g2[k].get(b, 0)
            G[i, 2] = g1.get(k, {}).get(a, 0); G[i, 3] = g1.get(k, {}).get(b, 0)
            if '1g' in d[k]:
                G[i, 4] = d[k]['1g']['B']; G[i, 5] = d[k]['1g']['N']
    o['gov'] = G
    np.savez_compressed(f'{TRAB}/base_2026.npz', **o)
    U = o['pareada'] & (o['L2'] + o['R2'] >= 30) & (o['uf'] != 'ZZ') & ~o['junta']
    meta = {'secoes_2t': n, 'pareadas': int(o['pareada'].sum()), 'exterior': int((o['uf'] == 'ZZ').sum()),
            'junta': int(o['junta'].sum()), 'U': int(U.sum()), 'U_com_perfil': int((U & tem).sum()),
            'L2': int(o['L2'].sum()), 'R2': int(o['R2'].sum()), 'B2': int(o['B2'].sum()), 'N2': int(o['N2'].sum()),
            'L2_ok': bool(o['L2'].sum() == L2_OFICIAL), 'R2_ok': bool(o['R2'].sum() == R2_OFICIAL),
            'comp2': int(o['comp2'].sum()), 'comp1': int(o['comp1'].sum()), 'comp1_nacional': int(comp1_nac),
            'maiores_05': maiores, 'secoes_com_agregadas': nag, 'finalistas_gov': fin,
            'comp_ate_K': {str(K): int((o['comp2'] <= K).sum()) for K in (25, 50, 75, 100, 150, 200)},
            'modelos': {m: int((o['modelo'] == m).sum()) for m in sorted(set(o['modelo']))},
            'perfil_total': int(P[:, 0].sum()), 'perfil_secoes_no_arquivo': len(pf)}
    grava('base_meta.json', meta)
    log(json.dumps(meta, ensure_ascii=False))


def carrega(ano=2026):
    z = np.load(f'{TRAB}/base_{ano}.npz')
    return {k: z[k] for k in z.files}


def universo_U(b):
    return b['pareada'] & (b['L2'] + b['R2'] >= 30) & (b['uf'] != 'ZZ') & ~b['junta']


def universo_ano(b):
    return (b['L2'] + b['R2'] >= 30) & (b['uf'] != 'ZZ')


# ---------------------------------------------------------------------------------------------------------------
# Pente D1.2(a)
# ---------------------------------------------------------------------------------------------------------------
VMAXP = 510
VFIM = 500
FREQ = np.arange(0.004, 0.5 + 1e-9, 0.0005)
PERIODOS = list(range(2, 121))
COMBOS = [(p, o) for p in PERIODOS for o in range(p)]


def matriz_lisa():
    """liso = S @ h: regressão local quadrática, janela de 21 valores, sem o próprio ponto (P2)."""
    n = VMAXP + 1
    S = np.zeros((n, n))
    for v in range(n):
        us = np.array([u for u in range(max(0, v - 10), min(VMAXP, v + 10) + 1) if u != v])
        A = np.column_stack([np.ones(len(us)), us - v, (us - v) ** 2.0])
        S[v, us] = np.linalg.pinv(A)[0]
    return S


_SLISA = None


def slisa():
    global _SLISA
    if _SLISA is None:
        _SLISA = matriz_lisa()
    return _SLISA


def histograma(x, vmax=VMAXP):
    x = np.asarray(x)
    return np.bincount(x[(x >= 0) & (x <= vmax)], minlength=vmax + 1).astype(float), int((x > vmax).sum())


class Pente:
    """Estatísticas 1 e 2 do D1.2(a) para um histograma; as casas usadas ficam fixas pelo observado (P3, P6)."""

    def __init__(self, h, vmin):
        self.h = h; self.vmin = vmin
        self.s = slisa() @ h
        casas = np.zeros(VMAXP + 1, bool); casas[vmin:VFIM + 1] = True
        casas &= self.s >= 30
        self.casas = casas; self.vs = np.nonzero(casas)[0]; self.n = len(self.vs)
        if self.n < 2:
            return
        M = np.zeros((len(COMBOS), self.n), dtype=np.float32); self.valido = np.zeros(len(COMBOS), bool)
        self.ndentes = np.zeros(len(COMBOS), int)
        for i, (p, o) in enumerate(COMBOS):
            m = (self.vs % p) == o
            k = int(m.sum()); self.ndentes[i] = k
            if k >= 2:
                M[i, m] = 1.0 / math.sqrt(k); self.valido[i] = True
        self.M = M
        ang = -2 * np.pi * np.outer(FREQ, self.vs)
        self.Ec = np.cos(ang).astype(np.float32); self.Es = np.sin(ang).astype(np.float32)

    def residuo(self, H):
        """H: (n_hist, 511). Devolve e nas casas usadas."""
        s = H @ slisa().T
        return ((H - s) / np.sqrt(np.maximum(s, 1.0)))[:, self.casas]

    def estat(self, H):
        e = self.residuo(np.atleast_2d(H)).astype(np.float32)
        Z = e @ self.M.T
        Z[:, ~self.valido] = 0.0
        P = ((e @ self.Ec.T) ** 2 + (e @ self.Es.T) ** 2) / self.n
        return Z, P

    def media_nulo(self):
        m = np.maximum(self.s, 0.0).copy()
        m[:self.vmin] = self.h[:self.vmin]
        return m

    def observado(self, top=5):
        from scipy.stats import norm
        Z, P = self.estat(self.h)
        Z = Z[0].astype(float); P = P[0].astype(float)
        o = {'casas_usadas': int(self.n), 'v_primeira': int(self.vs[0]), 'v_ultima': int(self.vs[-1]),
             'secoes_nas_casas': float(self.h[self.casas].sum())}
        ordem = np.argsort(-np.abs(Z))[:top]
        lista = []
        for i in ordem:
            p, of = COMBOS[i]
            m = (self.vs % p) == of
            amp = float((self.h[self.vs[m]] - self.s[self.vs[m]]).sum() / self.s[self.vs[m]].sum()) if m.any() else 0.0
            lista.append({'p': p, 'o': of, 'Z': float(Z[i]), 'dentes': int(m.sum()), 'amplitude': amp})
        o['maiores_Z'] = lista; o['maxabsZ'] = abs(lista[0]['Z']); o['Z_do_max'] = lista[0]['Z']
        o['maxZ_excesso'] = float(Z.max()); o['minZ_falta'] = float(Z.min())
        j = int(P.argmax())
        rel = (self.h[self.vs] - self.s[self.vs]) / self.s[self.vs]
        ampf = 2 * abs(np.sum(rel * np.exp(-2j * np.pi * FREQ[j] * self.vs))) / self.n
        o['periodograma'] = {'P_max': float(P[j]), 'f': float(FREQ[j]), 'periodo': float(1 / FREQ[j]),
                             'z_equivalente': float(norm.isf(min(1.0, math.exp(-P[j])) / 2)) if P[j] < 700 else 99.0,
                             'amplitude': float(ampf)}
        return o, Z, P

    def nulo(self, rng, nsim=1000, lote=250):
        mz, mp = [], []
        med = self.media_nulo()
        for a in range(0, nsim, lote):
            H = rng.poisson(med, size=(min(lote, nsim - a), VMAXP + 1)).astype(float)
            Z, P = self.estat(H)
            mz.append(np.abs(Z).max(axis=1)); mp.append(P.max(axis=1))
        mz = np.concatenate(mz); mp = np.concatenate(mp)
        return {'n': nsim, 'maxabsZ_q50': float(np.median(mz)), 'maxabsZ_q99': float(np.quantile(mz, 0.99)),
                'maxabsZ_max': float(mz.max()), 'P_q50': float(np.median(mp)), 'P_q99': float(np.quantile(mp, 0.99)),
                'P_max': float(mp.max())}


def roda_pente(x, vmin, rng, nulo=True, guarda=None, nome=None):
    h, fora = histograma(x)
    pt = Pente(h, vmin)
    if pt.n < 2 or not pt.valido.any():
        return {'avaliavel': False, 'secoes': int(len(x)), 'casas_usadas': int(pt.n)}
    o, Z, P = pt.observado()
    o['avaliavel'] = True; o['secoes'] = int(len(x)); o['acima_de_510'] = fora
    if nulo:
        o['nulo'] = pt.nulo(rng)
        o['P_acima_de_todos_os_nulos'] = bool(o['periodograma']['P_max'] > o['nulo']['P_max'])
        o['P_dentro_do_q99'] = bool(o['periodograma']['P_max'] <= o['nulo']['P_q99'])
        o['Z_acima_do_q99_do_nulo'] = bool(o['maxabsZ'] > o['nulo']['maxabsZ_q99'])
    if guarda is not None:
        guarda[nome] = (Z, P, pt.valido.copy())
    return o


def quarta_diferenca(x, vmin=3, hmin=400, vmax=120):
    """Complemento P11: q(v) = [6 ln h(v) - 4 ln h(v-1) - 4 ln h(v+1) + ln h(v-2) + ln h(v+2)]/6, erro por Poisson."""
    h, _ = histograma(x)
    out = []
    for v in range(max(vmin, 2), vmax + 1):
        hh = h[v - 2:v + 3]
        if hh.min() <= 0 or h[v] < hmin:
            continue
        q = (6 * math.log(hh[2]) - 4 * math.log(hh[1]) - 4 * math.log(hh[3]) + math.log(hh[0]) + math.log(hh[4])) / 6
        ep = math.sqrt(36 / hh[2] + 16 / hh[1] + 16 / hh[3] + 1 / hh[0] + 1 / hh[4]) / 6
        out.append((v, q, q / ep, hh[2]))
    return out


def resumo_q4(lst):
    if not lst:
        return {'casas': 0}
    a = np.array(lst)
    i = int(np.abs(a[:, 2]).argmax()); j = int(np.abs(a[:, 1]).argmax())
    dentes = [{'v': int(v), 'q': float(q), 'z': float(z), 'h': float(hv)} for v, q, z, hv in lst if abs(q) >= 0.02 and abs(z) >= 8]
    return {'casas': len(lst), 'maior_z': {'v': int(a[i, 0]), 'q': float(a[i, 1]), 'z': float(a[i, 2])},
            'maior_q': {'v': int(a[j, 0]), 'q': float(a[j, 1]), 'z': float(a[j, 2])}, 'dentes': dentes,
            'tabela_v3_a_v20': [{'v': int(v), 'q': round(float(q), 5), 'z': round(float(z), 2), 'h': int(hv)} for v, q, z, hv in lst if v <= 20]}


# ---------------------------------------------------------------------------------------------------------------
# Pente D4-2 (código próprio a partir da descrição do desenho)
# ---------------------------------------------------------------------------------------------------------------
class D42:
    VM = 520
    PER = np.arange(8.0, 150.0, 0.02)

    def __init__(self):
        v = np.arange(self.VM)
        self.C = []; self.S = []
        for m in (1, 2, 3):
            ang = 2 * np.pi * np.outer(m / self.PER, v)
            self.C.append(np.cos(ang).astype(np.float32)); self.S.append(np.sin(ang).astype(np.float32))

    @staticmethod
    def histo(x):
        return np.bincount(np.clip(np.asarray(x), 0, D42.VM), minlength=D42.VM + 1)[:D42.VM].astype(float)

    @staticmethod
    def liso(H, k):
        H = np.atleast_2d(H)
        pad = np.pad(H, ((0, 0), (k, k)), mode='reflect')
        cs = np.cumsum(np.concatenate([np.zeros((H.shape[0], 1)), pad], axis=1), axis=1)
        return (cs[:, 2 * k + 1:] - cs[:, :-(2 * k + 1)]) / (2 * k + 1)

    def estat(self, H, detalhe=False):
        H = np.atleast_2d(H).astype(float)
        s = self.liso(H, 4)
        d = np.zeros_like(H)
        d[:, 1:-1] = H[:, 1:-1] - (H[:, :-2] + H[:, 2:]) / 2
        ok = s >= 300; ok[:, 0] = False; ok[:, -1] = False
        z = np.where(ok, d / np.sqrt(1.5 * np.maximum(s, 1)), 0.0).astype(np.float32)
        n = ok.sum(axis=1).astype(float)
        termos = [((c @ z.T) ** 2 + (sn @ z.T) ** 2) for c, sn in zip(self.C, self.S)]   # (períodos, hist)
        Z2 = sum(termos) / np.maximum(n, 1)
        j = Z2.argmax(axis=0)
        Zm = Z2[j, np.arange(H.shape[0])]
        Zm = np.where(n > 0, Zm, np.nan)
        if detalhe:
            return {'Z': float(Zm[0]), 'periodo': float(self.PER[j[0]]), 'casas': int(n[0]),
                    'termos_do_pico': [float(t[j[0], 0] / max(n[0], 1)) for t in termos],
                    'fracao_implicita': float(1 / (self.PER[j[0]] + 1))} if n[0] > 0 else {'Z': None, 'casas': 0}
        return Zm

    def nulo(self, h, rng, nsim=1000, lote=250):
        s0 = self.liso(h, 6)[0]
        pr = np.maximum(s0, 0); pr = pr / pr.sum()
        N = int(round(h.sum()))
        out = []
        for a in range(0, nsim, lote):
            H = rng.multinomial(N, pr, size=min(lote, nsim - a)).astype(float)
            out.append(self.estat(H))
        return np.concatenate(out)


# ---------------------------------------------------------------------------------------------------------------
# Equipe vermelha: resíduos módulo k (E1 a E6)
# ---------------------------------------------------------------------------------------------------------------
KS_EV = list(range(2, 201))
N_TESTES_EV = 4 * len(KS_EV)   # 796


def matriz_classes(vs):
    linhas = []; dono = []
    for k in KS_EV:
        r = vs % k
        for c in range(k):
            linhas.append(r == c); dono.append((k, c))
    return np.array(linhas, dtype=np.float32), np.array(dono)


def ev_z(pt, Mc, H):
    H = np.atleast_2d(H).astype(float)
    s = H @ slisa().T
    O = H[:, pt.casas] @ Mc.T; E = s[:, pt.casas] @ Mc.T
    E = np.maximum(E, 1e-9)
    return (O - E) / np.sqrt(E), O / E - 1


def sorteios_binomiais(X, n, mun, rng, nsim=200):
    """E2: binomial por seção com encolhimento que mantém a variância do histograma."""
    X = X.astype(float); n = n.astype(float)
    _, g = np.unique(mun, return_inverse=True)
    taxa = np.bincount(g, X) / np.maximum(np.bincount(g, n), 1)
    m = n * taxa[g]
    ruido = float((X * (1 - X / np.maximum(n, 1))).sum()); disp = float(((X - m) ** 2).sum())
    s = max(0.0, 1 - ruido / disp)
    p = np.clip((m + math.sqrt(s) * (X - m)) / np.maximum(n, 1), 0, 1)
    ni = n.astype(np.int64)
    H = np.empty((nsim, VMAXP + 1))
    for j in range(nsim):
        H[j] = histograma(rng.binomial(ni, p))[0]
    return H, s


def ev_variavel(X, n, mun, vmin, rng, plantado=None):
    from scipy.stats import norm
    h, _ = histograma(X)
    pt = Pente(h, vmin)
    Mc, dono = matriz_classes(pt.vs)
    zo, eo = ev_z(pt, Mc, h); zo = zo[0]; eo = eo[0]
    Hs, s = sorteios_binomiais(X, n, mun, rng)
    zs, es = ev_z(pt, Mc, Hs)
    med = zs.mean(axis=0); dp = zs.std(axis=0, ddof=1); emed = es.mean(axis=0)
    zc = (zo - med) / dp; ec = eo - emed
    ini = np.concatenate([[0], np.cumsum(KS_EV)])
    nS = zs.shape[0]
    S1 = zs.sum(axis=0); S2 = (zs ** 2).sum(axis=0)
    m_loo = (S1[None, :] - zs) / (nS - 1)
    v_loo = (S2[None, :] - zs ** 2 - (nS - 1) * m_loo ** 2) / (nS - 2)
    zs_c = (zs - m_loo) / np.sqrt(np.maximum(v_loo, 1e-12))
    T = np.empty(len(KS_EV)); cls = np.empty(len(KS_EV), int); Ts = np.empty((nS, len(KS_EV)))
    for i, k in enumerate(KS_EV):
        a, b_ = ini[i], ini[i + 1]
        j = int(zc[a:b_].argmax()); T[i] = zc[a + j]; cls[i] = j
        Ts[:, i] = zs_c[:, a:b_].max(axis=1)
    pk = np.minimum(1.0, np.array(KS_EV) * norm.sf(T))
    pb = np.minimum(1.0, N_TESTES_EV * pk)
    exc_T = np.array([ec[ini[i] + cls[i]] for i in range(len(KS_EV))])
    maxT_s = Ts.max(axis=1)
    q99_k = np.quantile(Ts, 0.99, axis=0)
    i = int(T.argmax())
    out = {'secoes': int(len(X)), 'casas_usadas': int(pt.n), 'encolhimento_s': s,
           'maxT': float(T[i]), 'k_do_max': int(KS_EV[i]), 'classe_do_max': int(cls[i]),
           'excesso_corrigido_no_max': float(exc_T[i]), 'p_bonferroni_no_max': float(pb[i]),
           'menor_p_bonferroni': float(pb.min()), 'maior_excesso_corrigido_em_T': float(exc_T.max()),
           'sorteios_maxT_q50': float(np.median(maxT_s)), 'sorteios_maxT_q99': float(np.quantile(maxT_s, 0.99)),
           'sorteios_maxT_max': float(maxT_s.max()),
           'abaixo_do_q99_do_maximo': bool(T[i] < np.quantile(maxT_s, 0.99)),
           'k_acima_do_q99_do_proprio_k': int((T > q99_k).sum()), 'esperado_por_acaso': 0.01 * len(KS_EV),
           'k_com_condicoes_de_sinal': [{'k': int(KS_EV[t]), 'classe': int(cls[t]), 'T': float(T[t]),
                                         'excesso_corrigido': float(exc_T[t]), 'p_bonferroni': float(pb[t])}
                                        for t in range(len(KS_EV)) if exc_T[t] >= 0.03 and pb[t] < 1e-6],
           'k2_a_k12': [{'k': int(KS_EV[t]), 'classe': int(cls[t]), 'T': round(float(T[t]), 2),
                         'excesso_corrigido': round(float(exc_T[t]), 5)} for t in range(11)]}
    aux = {'zc': zc, 'ec': ec, 'ini': ini, 'med': med, 'dp': dp, 'emed': emed, 'pt': pt, 'Mc': Mc}
    if plantado is not None:
        hp, _ = histograma(plantado)
        zp, ep = ev_z(pt, Mc, hp); zp = (zp[0] - med) / dp; ep = ep[0] - emed
        a = ini[KS_EV.index(27)]
        Tp = np.array([zp[ini[t]:ini[t + 1]].max() for t in range(len(KS_EV))])
        out['plantado_um_a_cada_28'] = {'zc_k27_classe0': float(zp[a]), 'excesso_corrigido_k27_classe0': float(ep[a]),
                                        'maxT': float(Tp.max()), 'k_do_max': int(KS_EV[int(Tp.argmax())]),
                                        'detectado_z_acima_de_20': bool(zp[a] > 20)}
    return out, aux


def modo_pente():
    t0 = time.time()
    b = carrega(2026); U = universo_U(b)
    res = {'universo_U': int(U.sum())}
    guarda = {}
    VARS = {'R2': 10, 'L2': 10, 'B2': 3, 'N2': 3}
    # ---------------- D1.2(a): observado e nulo, país, modelos e UFs
    rng = np.random.default_rng([SEMENTE, 1])
    recortes = {'pais': U}
    for m in ('UE2013', 'UE2015', 'UE2020', 'UE2022'):
        recortes['modelo_' + m] = U & (b['modelo'] == m)
    for uf in sorted(set(b['uf'][U])):
        recortes['uf_' + uf] = U & (b['uf'] == uf)
    d12 = {}
    for rn, mask in recortes.items():
        for X, vmin in VARS.items():
            d12[f'{rn}|{X}'] = roda_pente(b[X][mask], vmin, rng, guarda=guarda, nome=f'{rn}|{X}')
        log('D1.2a', rn, {X: round(d12[f'{rn}|{X}'].get('maxabsZ', float('nan')), 2) for X in VARS})
    brasil = b['uf'] != 'ZZ'
    sens = {X: roda_pente(b[X][brasil], vmin, rng) for X, vmin in VARS.items()}
    # ---------------- placebos
    plac = {}
    for X, vmin in (('R1', 10), ('L1', 10), ('B1', 3), ('N1', 3)):
        plac[f'2026_1t|{X}'] = roda_pente(b[X][U], vmin, rng, guarda=guarda, nome=f'2026_1t|{X}')
    bases = {}
    for ano in (2022, 2018, 2014):
        ba = carrega(ano); Ua = universo_ano(ba); bases[ano] = ba
        for X, vmin in VARS.items():
            plac[f'{ano}_2t|{X}'] = roda_pente(ba[X][Ua], vmin, rng, guarda=guarda, nome=f'{ano}_2t|{X}')
    mg = U & np.isin(b['uf'], UFS_GOV) & (b['gov'][:, 0] + b['gov'][:, 1] > 0)
    plac['2026_gov2t|G1'] = roda_pente(b['gov'][mg, 0], 10, rng, guarda=guarda, nome='2026_gov2t|G1')
    plac['2026_gov2t|G2'] = roda_pente(b['gov'][mg, 1], 10, rng, guarda=guarda, nome='2026_gov2t|G2')
    log('placebos', {k: round(v.get('maxabsZ', float('nan')), 2) for k, v in plac.items()})
    # Placebos no mesmo recorte para as rodadas de UF. ACRESCENTADO DEPOIS DE VER A PRIMEIRA RODADA (desvio): o placebo
    # nacional não tem as mesmas casas usadas de uma UF, então "ausente no mesmo período" precisa do placebo da própria UF.
    plac_uf = {}
    for uf in sorted(set(b['uf'][U])):
        mu = U & (b['uf'] == uf)
        for X, vmin in (('R1', 10), ('L1', 10), ('B1', 3), ('N1', 3)):
            plac_uf[f'uf_{uf}|2026_1t|{X}'] = roda_pente(b[X][mu], vmin, rng, guarda=guarda, nome=f'uf_{uf}|2026_1t|{X}')
        for ano in (2022, 2018, 2014):
            ba = bases[ano]; ma = universo_ano(ba) & (ba['uf'] == uf)
            for X, vmin in VARS.items():
                plac_uf[f'uf_{uf}|{ano}_2t|{X}'] = roda_pente(ba[X][ma], vmin, rng, guarda=guarda, nome=f'uf_{uf}|{ano}_2t|{X}')
    log('placebos por UF prontos', round(time.time() - t0))

    def lista_placebos(rn, X):
        pre = rn + '|' if rn.startswith('uf_') else ''
        if X == 'R2':
            return [pre + '2022_2t|R2', pre + '2018_2t|R2', pre + '2014_2t|R2', pre + '2026_1t|R1', f'{rn}|L2']
        if X == 'L2':
            return [pre + '2022_2t|L2', pre + '2018_2t|L2', pre + '2014_2t|L2', pre + '2026_1t|L1', f'{rn}|R2']
        return [pre + f'2022_2t|{X}', pre + f'2018_2t|{X}', pre + f'2014_2t|{X}', pre + f'2026_1t|{X[0]}1']

    for nome, o in d12.items():
        if not o.get('avaliavel'):
            continue
        rn, X = nome.split('|')
        top = o['maiores_Z'][0]; i = COMBOS.index((top['p'], top['o']))
        jf = int(round((o['periodograma']['f'] - FREQ[0]) / 0.0005))
        presZ, presP, mesmo_tipo = [], [], []
        for pn in lista_placebos(rn, X):
            if pn not in guarda:
                continue
            Zp, Pp, val = guarda[pn]
            if val[i] and abs(Zp[i]) >= 5 and np.sign(Zp[i]) == np.sign(top['Z']):
                presZ.append({'placebo': pn, 'Z': float(Zp[i])})
            op = plac.get(pn) or plac_uf.get(pn) or d12.get(pn)
            if op['maxabsZ'] >= 8 and abs(op['maiores_Z'][0]['amplitude']) >= 0.02:
                mesmo_tipo.append({'placebo': pn, 'maxabsZ': op['maxabsZ'], 'p': op['maiores_Z'][0]['p'], 'o': op['maiores_Z'][0]['o']})
            pq = op['nulo']['P_q99']
            pv = float(Pp[max(0, jf - 2):jf + 3].max())
            if pv > pq:
                presP.append({'placebo': pn, 'P': pv, 'q99': pq})
        condZ = o['maxabsZ'] >= 8 and abs(top['amplitude']) >= 0.02
        condP = (o['P_acima_de_todos_os_nulos'] and o['periodograma']['z_equivalente'] >= 8
                 and o['periodograma']['amplitude'] >= 0.02)
        o['placebo_presente_no_mesmo_p_o'] = presZ; o['placebo_presente_na_mesma_frequencia'] = presP
        o['placebos_com_Z8_e_amplitude_em_qualquer_p_o'] = mesmo_tipo
        o['cond_Z8_com_amplitude'] = bool(condZ); o['cond_periodograma'] = bool(condP)
        o['sinal_numerico'] = bool((condZ and not presZ) or (condP and not presP))
        o['sem_sinal_numerico'] = bool(o['maxabsZ'] < 5 and o['P_dentro_do_q99'])
    res['D12a'] = {'rodadas': d12, 'placebos': plac, 'placebos_por_UF': plac_uf, 'sensibilidade_todas_as_secoes_do_Brasil': sens}
    grava('parcial_pente_D12a.json', res['D12a'])
    log('D1.2a observado e placebos prontos', round(time.time() - t0))
    # ---------------- D1.2(a): plantios (P10)
    R = b['R2'][U]; L = b['L2'][U]; B = b['B2'][U]; N = b['N2'][U]
    plant = {}

    def reg(nome, x, vmin, movidos, escala):
        o = roda_pente(x, vmin, rng, nulo=False)
        o['votos_movidos'] = int(movidos); o['Phi_efetivo'] = float(movidos / escala)
        o['enxerga_Z8'] = bool(o.get('maxabsZ', 0) >= 8)
        o['quarta_diferenca'] = resumo_q4(quarta_diferenca(x, vmin=max(vmin, 3)))
        plant[nome] = o

    for q, k in ((1, 110), (1, 56), (1, 28), (0.25, 7)):
        sel = (rng.random(len(R)) < q) if q < 1 else np.ones(len(R), bool)
        m = np.where(sel, R // k, 0); reg(f'R_para_L_q{q}_k{k}|R2', R - m, 10, m.sum(), NECESSARIO)
        m = np.where(sel, L // k, 0); reg(f'espelho_L_para_R_q{q}_k{k}|L2', L - m, 10, m.sum(), NECESSARIO)
    for phi in (0.25, 0.5, 1.0):
        Rn = np.floor(R * (1 - phi * 0.0357)).astype(np.int64)
        reg(f'fracao_arredondada_Phi{phi}|R2', Rn, 10, (R - Rn).sum(), NECESSARIO)
    m = rng.binomial(R, NECESSARIO / R.sum()); reg('binomial_Phi1|R2', R - m, 10, m.sum(), NECESSARIO)
    for k in (3, 5, 10):
        m = B // k; reg(f'conversao_brancos_k{k}|B2', B - m, 3, m.sum(), MARGEM)
        m = N // k; reg(f'conversao_nulos_k{k}|N2', N - m, 3, m.sum(), MARGEM)
    res['D12a']['plantios'] = plant
    log('plantios', {k: (round(v['maxabsZ'], 1), round(v['Phi_efetivo'], 3)) for k, v in plant.items()})
    # complemento P11
    q4 = {}
    for X in ('B2', 'N2', 'R2', 'L2'):
        q4[f'2026_2t|{X}'] = resumo_q4(quarta_diferenca(b[X][U]))
        q4[f'2026_1t|{X[0]}1'] = resumo_q4(quarta_diferenca(b[X[0] + '1'][U]))
        for ano in (2022, 2018, 2014):
            q4[f'{ano}_2t|{X}'] = resumo_q4(quarta_diferenca(bases[ano][X][universo_ano(bases[ano])]))
    for X in ('B2', 'N2', 'R2', 'L2'):
        d2 = {d['v'] for d in q4[f'2026_2t|{X}'].get('dentes', [])}
        d1 = {d['v'] for d in q4[f'2026_1t|{X[0]}1'].get('dentes', [])}
        q4[f'2026_2t|{X}']['dentes_sem_o_mesmo_no_1t'] = sorted(d2 - d1)
    res['D12a']['quarta_diferenca'] = q4
    # o mesmo complemento em cada recorte (país, modelos, UFs)
    q4r = {}
    for rn, mask in recortes.items():
        for X in VARS:
            r_ = resumo_q4(quarta_diferenca(b[X][mask])); r_.pop('tabela_v3_a_v20', None)
            q4r[f'{rn}|{X}'] = r_
    res['D12a']['quarta_diferenca_por_recorte'] = q4r
    grava('parcial_pente_D12a.json', res['D12a'])
    log('D1.2a completo', round(time.time() - t0))
    # ---------------- D4-2
    rng2 = np.random.default_rng([SEMENTE, 2])
    d42 = D42()

    def roda42(x, nulo=True):
        h = d42.histo(x); o = d42.estat(h, detalhe=True); o['secoes'] = int(len(x)); nl = None
        if nulo and o['casas'] > 0:
            nl = d42.nulo(h, rng2)
            o['nulo'] = {'q50': float(np.nanmedian(nl)), 'q99': float(np.nanquantile(nl, 0.99)), 'max': float(np.nanmax(nl))}
        return o, nl

    nac = {}
    for X in ('R2', 'L2', 'B2', 'N2'):
        nac[X], _ = roda42(b[X])
    log('D4-2 nacional', {X: (round(o['Z'], 1), o['periodo'], round(o['nulo']['max'], 1)) for X, o in nac.items()})
    cortes = np.quantile(b['comp2'], [1 / 3, 2 / 3]); faixa = np.digitize(b['comp2'], cortes)
    rec42 = {'uf_' + uf: b['uf'] == uf for uf in sorted(set(b['uf']))}
    for t in range(3):
        rec42[f'tamanho_{t + 1}'] = faixa == t
    rec = {}; fam = []
    for rn, mask in rec42.items():
        for X in ('R2', 'L2'):
            o, nl = roda42(b[X][mask]); rec[f'{rn}|{X}'] = o
            if nl is not None:
                fam.append(nl)
    fam_max = np.nanmax(np.vstack(fam), axis=0)
    plc = {}
    par = b['pareada']
    for nome, x in (('2026 comparecimento 2T', b['comp2']), ('2026 comparecimento 1T', b['comp1'][par]), ('2026 aptos 2T', b['apt2']),
                    ('2026 L1', b['L1'][par]), ('2026 R1', b['R1'][par])):
        plc[nome], _ = roda42(x)
    for ano in (2014, 2018, 2022):
        for X in ('L1', 'R1', 'L2', 'R2'):
            plc[f'{ano} {X}'], _ = roda42(bases[ano][X])
    maior_plc = max(v['Z'] for v in plc.values())
    # B e N nos outros turnos e anos, só para comparar com B2 e N2 (descritivo; ACRESCENTADO DEPOIS de ver B2 e N2)
    bn_comp = {}
    for nome, x in (('2026 B1', b['B1'][par]), ('2026 N1', b['N1'][par])):
        bn_comp[nome], _ = roda42(x)
    for ano in (2014, 2018, 2022):
        for X in ('B2', 'N2'):
            bn_comp[f'{ano} {X}'], _ = roda42(bases[ano][X])

    def plant42(Rx, Tx, Lx):
        n = len(Rx); out = {}
        for p, fr in ((0.0357, (1.0, 0.5, 0.2, 0.1)), (0.018, (1.0, 0.5, 0.2)), (0.01, (1.0, 0.5))):
            for phi in fr:
                x = Rx.copy(); m = rng2.random(n) < phi
                tira = np.floor(p * x[m]).astype(np.int64); x[m] = x[m] - tira
                o = d42.estat(d42.histo(x), detalhe=True); o['votos_movidos'] = int(tira.sum())
                out[f'piso_{p}_em_{phi}_das_secoes'] = o
        tira = rng2.binomial(Rx, 0.0357); o = d42.estat(d42.histo(Rx - tira), detalhe=True); o['votos_movidos'] = int(tira.sum())
        out['binomial_0.0357 (ponto cego)'] = o
        tira = np.rint(0.0357 * Rx).astype(np.int64); o = d42.estat(d42.histo(Rx - tira), detalhe=True); o['votos_movidos'] = int(tira.sum())
        out['arredonda_0.0357'] = o
        poe = np.floor(0.0345 * Lx).astype(np.int64); o = d42.estat(d42.histo(Lx + poe), detalhe=True); o['votos_movidos'] = int(poe.sum())
        out['inflar_beneficiado_0.0345 (em L)'] = o
        tira = np.minimum(np.floor(0.018 * Tx).astype(np.int64), Rx); o = d42.estat(d42.histo(Rx - tira), detalhe=True); o['votos_movidos'] = int(tira.sum())
        out['piso_0.018_do_comparecimento (ponto cego)'] = o
        return out

    b22 = bases[2022]
    pl42 = {'R2_2026': plant42(b['R2'], b['comp2'], b['L2']), 'R1_2026': plant42(b['R1'][par], b['comp1'][par], b['L1'][par]),
            'R2_2022': plant42(b22['R2'], b22['comp2'], b22['L2'])}
    lim_nac = {X: 1.5 * nac[X]['nulo']['max'] for X in nac}
    for base_, d_ in pl42.items():
        for k_, o in d_.items():
            o['enxerga'] = bool(o['Z'] is not None and o['Z'] > 1.5 * nac['R2']['nulo']['max'])
            o['fracao_da_margem'] = o['votos_movidos'] / NECESSARIO
    res['D42'] = {'nacional': nac, 'recortes': rec, 'placebos': plc, 'maior_placebo': maior_plc,
                  'brancos_e_nulos_de_comparacao': bn_comp,
                  'nulo_do_conjunto_de_recortes': {'q99': float(np.quantile(fam_max, 0.99)), 'max': float(fam_max.max()),
                                                   'limiar_de_sinal': float(1.5 * fam_max.max()), 'recortes_avaliaveis': len(fam)},
                  'limiar_de_sinal_nacional': lim_nac, 'plantios': pl42,
                  'tercis_de_comparecimento': [float(c) for c in cortes]}
    grava('parcial_pente_D42.json', res['D42'])
    log('D4-2 completo', round(time.time() - t0), 'maior placebo', round(maior_plc, 1))
    # ---------------- equipe vermelha: resíduos módulo k
    rng3 = np.random.default_rng([SEMENTE, 3])
    ev = {}; auxs = {}
    munU = b['mun'][U]
    for X, vmin in VARS.items():
        pl = (R - R // 28) if X == 'R2' else ((L - L // 28) if X == 'L2' else None)
        ev[X], auxs[X] = ev_variavel(b[X][U], b['comp2'][U], munU, vmin, rng3, plantado=pl)
        X1 = X[0] + '1'
        ev[X1], auxs[X1] = ev_variavel(b[X1][U], b['comp1'][U], munU, vmin, rng3)
        log('EV', X, round(ev[X]['maxT'], 2), 'q99', round(ev[X]['sorteios_maxT_q99'], 2), '| 1T', round(ev[X1]['maxT'], 2))
    from scipy.stats import norm
    for X in VARS:
        X1 = X[0] + '1'; a1 = auxs[X1]
        for item in ev[X]['k_com_condicoes_de_sinal']:
            pos = a1['ini'][KS_EV.index(item['k'])] + item['classe']
            z1 = float(a1['zc'][pos]); e1 = float(a1['ec'][pos])
            p1 = min(1.0, N_TESTES_EV * item['k'] * float(norm.sf(z1)))
            item['no_1t'] = {'zc': z1, 'excesso_corrigido': e1, 'p_bonferroni': p1, 'presente': bool(e1 >= 0.03 and p1 < 1e-6)}
        ev[X]['sinal_numerico'] = bool(any(not it['no_1t']['presente'] for it in ev[X]['k_com_condicoes_de_sinal']))
    res['EV_modulo'] = ev
    grava('parcial_pente_EV.json', ev)
    log('pente: fim', round(time.time() - t0))


# ---------------------------------------------------------------------------------------------------------------
# Regressão com efeito fixo, erro agrupado e somas por grupo (para o bootstrap de municípios)
# ---------------------------------------------------------------------------------------------------------------
class Reg:
    """MQO ponderado com efeito fixo (transformação within) e erro CR1 agrupado por 'grupo' (que contém o efeito fixo).
    Guarda X'WX e X'Wy por grupo: reamostrar grupos equivale a refazer a regressão, porque o efeito fixo fica dentro."""

    def __init__(self, cols, ys, w, fe, grupo):
        _, g = np.unique(fe, return_inverse=True)
        ok = np.bincount(g)[g] >= 2
        g = np.unique(fe[ok], return_inverse=True)[1]
        w = np.asarray(w, float)[ok]
        nomes = list(cols); self.ynomes = list(ys)
        M = np.column_stack([np.asarray(cols[c], float)[ok] for c in nomes] + [np.asarray(ys[c], float)[ok] for c in ys])
        sw = np.bincount(g, w)
        for j in range(M.shape[1]):
            M[:, j] -= (np.bincount(g, w * M[:, j]) / sw)[g]
        k = len(nomes)
        var = (w[:, None] * M[:, :k] ** 2).sum(0)
        self.sem_variacao = [nomes[j] for j in range(k) if var[j] < 1e-12 * max(var.max(), 1e-300)]
        gu, gg = np.unique(np.asarray(grupo)[ok], return_inverse=True)
        ordem = np.argsort(gg, kind='stable')
        self.linhas = np.nonzero(ok)[0][ordem]
        self.nomes = nomes; self.Xd = M[ordem, :k]; self.Yd = M[ordem, k:]; self.w = w[ordem]; self.gg = gg[ordem]
        self.grupos = gu; self.G = len(gu); self.n = len(self.gg); self.locais = int(g.max() + 1)
        self.ini = np.searchsorted(self.gg, np.arange(self.G))
        fim = list(self.ini[1:]) + [self.n]
        Xw = self.Xd * self.w[:, None]
        self.A = np.empty((self.G, k, k)); self.C = np.empty((self.G, k, len(self.ynomes)))
        for i in range(self.G):
            a, b_ = self.ini[i], fim[i]
            self.A[i] = Xw[a:b_].T @ self.Xd[a:b_]; self.C[i] = Xw[a:b_].T @ self.Yd[a:b_]
        self.At = self.A.sum(0); self.Ct = self.C.sum(0)
        self.ng = np.diff(np.concatenate([self.ini, [self.n]]))

    def ix(self, nomes):
        return [self.nomes.index(c) for c in nomes if c not in self.sem_variacao]

    def somas(self, m):
        return np.tensordot(m, self.A, 1), np.tensordot(m, self.C, 1)

    def resolve(self, A, C, nomes, y):
        ix = self.ix(nomes)
        As = A[np.ix_(ix, ix)]; d = 1 / np.sqrt(np.diag(As))          # escala das colunas, para o condicionamento
        try:
            return d * np.linalg.solve(As * np.outer(d, d), d * C[ix, self.ynomes.index(y)])
        except np.linalg.LinAlgError:       # reamostra sem nenhuma seção que separe as colunas (joelho com K = 25)
            return np.full(len(ix), np.nan)

    def ajusta(self, nomes, y, sel=None):
        """sel: vetor booleano de grupos (None = todos). Devolve coeficientes, erros CR1 e contagens."""
        ix = self.ix(nomes); iy = self.ynomes.index(y); usados = [self.nomes[j] for j in ix]
        if sel is None:
            A = self.At[np.ix_(ix, ix)]; c = self.Ct[ix, iy]; linhas = slice(None); G = self.G; N = self.n
        else:
            A = self.A[sel][:, ix][:, :, ix].sum(0); c = self.C[sel][:, ix, iy].sum(0)
            linhas = sel[self.gg]; G = int(sel.sum()); N = int(linhas.sum())
        d = 1 / np.sqrt(np.diag(A))                                    # escala das colunas, para o condicionamento
        Ai = np.linalg.inv(A * np.outer(d, d)) * np.outer(d, d)
        b = Ai @ c
        e = self.Yd[:, iy] - self.Xd[:, ix] @ b
        S = np.add.reduceat(self.Xd[:, ix] * (self.w * e)[:, None], self.ini, axis=0)
        if sel is not None:
            S = S[sel]
        cf = G / (G - 1) * (N - 1) / (N - len(ix))
        V = cf * Ai @ (S.T @ S) @ Ai
        return {'coef': dict(zip(usados, b.tolist())), 'ep': dict(zip(usados, np.sqrt(np.diag(V)).tolist())),
                'n': int(N), 'grupos': int(G), 'residuo': e if sel is None else None}

    def projetor(self, nomes, alvo):
        """Vetor a (na ordem de self.linhas) tal que o coeficiente de 'alvo' = a . y (y sem transformar)."""
        ix = self.ix(nomes); j = [self.nomes[i] for i in ix].index(alvo)
        A = self.At[np.ix_(ix, ix)]; d = 1 / np.sqrt(np.diag(A))
        Ai = np.linalg.inv(A * np.outer(d, d)) * np.outer(d, d)
        return (self.Xd[:, ix] @ Ai[j]) * self.w


def posicao_no_local(loc, secao):
    _, g = np.unique(loc, return_inverse=True)
    ordem = np.lexsort((secao, g)); cnt = np.bincount(g)
    ini = np.concatenate([[0], np.cumsum(cnt)[:-1]])
    rank = np.empty(len(g)); rank[ordem] = np.arange(len(g)) - ini[g[ordem]]
    return np.where(cnt[g] > 1, rank / np.maximum(cnt[g] - 1, 1), 0.0)


KS_LIMIAR = [25, 50, 75, 100, 150, 200]
COLS_PERFIL_X = ['mulher', 'i1617', 'i1824', 'i2534', 'i4559', 'i6069', 'i7079', 'i80m', 'e1', 'e2', 'e3', 'e4', 'e5', 'e7', 'e8', 'biom']


def colunas_perfil(P):
    tot = np.maximum(P[:, 0], 1).astype(float)
    c = {'mulher': P[:, 2] / tot, 'biom': P[:, 1] / tot}
    for nm in ('i1617', 'i1824', 'i2534', 'i4559', 'i6069', 'i7079', 'i80m', 'e1', 'e2', 'e3', 'e4', 'e5', 'e7', 'e8'):
        c[nm] = P[:, COLS_PERFIL.index(nm)] / tot
    return c


def colunas_2026(b):
    """X do modelo base de 2026 (L1), doses e desfechos, em todas as seções com 2º turno; e a máscara da amostra."""
    c1 = np.maximum(b['comp1'], 1).astype(float); c2 = np.maximum(b['comp2'], 1).astype(float)
    cols = {'f13': b['L1'] / c1, 'f22': b['R1'] / c1}
    for c in b['maiores']:
        cols['f' + str(c)] = b['c' + str(c)] / c1
    cols['fB'] = b['B1'] / c1; cols['fN'] = b['N1'] / c1
    cols['abst1'] = 1 - b['comp1'] / np.maximum(b['apt1'], 1)
    cols['dabst'] = (1 - b['comp2'] / np.maximum(b['apt2'], 1)) - cols['abst1']
    pf = colunas_perfil(b['perfil'])
    for nm in COLS_PERFIL_X:
        cols[nm] = pf[nm]
    cols['lnapt'] = np.log(np.maximum(b['apt2'], 1)); cols['pos'] = posicao_no_local(b['loc'], b['secao'])
    base = list(cols)
    for K in KS_LIMIAR:
        cols[f'D{K}'] = np.maximum(0.0, 1 - K / c2)
    cols['inv'] = 1 / c2
    V = (b['L2'] + b['R2']).astype(float)
    ys = {'y': 100 * b['L2'] / np.maximum(V, 1), 'ybn': 100 * (b['B2'] + b['N2']) / c2}
    amostra = universo_U(b) & b['tem_perfil'] & (b['perfil'][:, 0] > 0)
    return cols, base, ys, V, amostra


def colunas_ano(ba, b26, com_perfil=True):
    """X da regressão de outro ano (L2): frações de L, R, B e N do 1º turno (outros = referência) e o perfil de 2026 pela chave."""
    c1 = np.maximum(ba['comp1'], 1).astype(float); c2 = np.maximum(ba['comp2'], 1).astype(float)
    cols = {'f13': ba['L1'] / c1, 'f22': ba['R1'] / c1, 'fB': ba['B1'] / c1, 'fN': ba['N1'] / c1}
    cols['abst1'] = 1 - ba['comp1'] / np.maximum(ba['apt1'], 1)
    cols['dabst'] = (1 - ba['comp2'] / np.maximum(ba['apt2'], 1)) - cols['abst1']
    amostra = universo_ano(ba)
    if com_perfil:
        pos = {k: i for i, k in enumerate(b26['chave'])}
        idx = np.array([pos.get(k, -1) for k in ba['chave']])
        tem = (idx >= 0) & b26['tem_perfil'][np.maximum(idx, 0)] & (b26['perfil'][np.maximum(idx, 0), 0] > 0)
        pf = colunas_perfil(b26['perfil'][np.maximum(idx, 0)])
        for nm in COLS_PERFIL_X:
            cols[nm] = pf[nm]
        amostra = amostra & tem
    cols['lnapt'] = np.log(np.maximum(ba['apt2'], 1)); cols['pos'] = posicao_no_local(ba['loc'], ba['secao'])
    base = list(cols)
    for K in KS_LIMIAR:
        cols[f'D{K}'] = np.maximum(0.0, 1 - K / c2)
    cols['inv'] = 1 / c2
    V = (ba['L2'] + ba['R2']).astype(float)
    ys = {'y': 100 * ba['L2'] / np.maximum(V, 1), 'ybn': 100 * (ba['B2'] + ba['N2']) / c2}
    return cols, base, ys, V, amostra


def monta_reg(cols, ys, V, amostra, fe, grupo):
    return Reg({k: v[amostra] for k, v in cols.items()}, {k: v[amostra] for k, v in ys.items()}, V[amostra], fe[amostra], grupo[amostra])


# ---------------------------------------------------------------------------------------------------------------
# Paredão D1.2(b)
# ---------------------------------------------------------------------------------------------------------------
def faixas_naturais():
    nat = np.zeros(1001, bool)
    for den in range(1, 13):
        for a in range(den + 1):
            nat[(1000 * a) // den] = True
    return nat


def paredao_conta(L, R, rng, nsim=400):
    V = (L + R).astype(np.int64); m = V >= 150
    L = L[m].astype(np.int64); V = V[m]
    obs = np.bincount((1000 * L) // V, minlength=1001).astype(float)
    p0 = L / V
    acc = np.zeros(1001); acc2 = np.zeros(1001)
    for _ in range(nsim):
        p = np.clip(p0 + rng.normal(0, 0.01, len(L)), 0, 1)
        h = np.bincount((1000 * rng.binomial(V, p)) // V, minlength=1001).astype(float)
        acc += h; acc2 += h * h
    med = acc / nsim; var = (acc2 / nsim - med ** 2) * nsim / (nsim - 1)
    z = (obs - med) / np.sqrt(np.maximum(np.maximum(var, med), 1.0))
    nat = faixas_naturais(); dec = (med >= 20) & ~nat
    zz = np.where(dec, z, 0.0)
    i_max = int(zz.argmax()); i_min = int(zz.argmin())
    fora = [{'faixa_pp': i / 10, 'observado': int(obs[i]), 'esperado': float(med[i]), 'z': float(z[i])} for i in np.nonzero(dec & (np.abs(z) >= 6))[0]]
    zn = np.where(nat & (med >= 20), z, 0.0)
    return {'secoes_V150': int(m.sum()), 'faixas_que_decidem': int(dec.sum()),
            'maior_z': {'faixa_pp': i_max / 10, 'z': float(z[i_max]), 'observado': int(obs[i_max]), 'esperado': float(med[i_max])},
            'menor_z': {'faixa_pp': i_min / 10, 'z': float(z[i_min]), 'observado': int(obs[i_min]), 'esperado': float(med[i_min])},
            'faixas_com_absz_6_ou_mais_fora_dos_picos': fora,
            'dp_dos_z_que_decidem': float(z[dec].std()), 'media_dos_z_que_decidem': float(z[dec].mean()),
            'picos_naturais': {'faixas': int((nat & (med >= 20)).sum()), 'maior_absz': float(np.abs(zn).max()),
                               'faixa_pp': int(np.abs(zn).argmax()) / 10, 'z_em_50': float(z[500]),
                               'observado_em_50': int(obs[500]), 'esperado_em_50': float(med[500])},
            'cauda_y_abaixo_de_5': int(((1000 * L) < 50 * V).sum()), 'cauda_y_acima_de_95': int(((1000 * L) > 950 * V).sum()),
            'esperado_ref_abaixo_de_5': float(med[:50].sum()), 'esperado_ref_acima_de_95': float(med[951:].sum())}


def caudas_modelo(reg, base, yv, Vv, rng, nsim=200):
    """B4: caudas previstas pelo modelo base sem dose. yv e Vv já na ordem de reg.linhas."""
    r = reg.ajusta(base, 'y')
    e = r['residuo']; aj = yv - e
    gl = reg.n - reg.locais - len(reg.ix(base))
    p = np.clip(aj / 100, 0, 1)
    tau2 = max(0.0, float((e ** 2).sum() / 1e4 / gl - (p * (1 - p) / Vv).sum() / reg.n))
    m = Vv >= 150
    Vi = Vv[m].astype(np.int64); pm = aj[m] / 100
    ab, ac = [], []
    for _ in range(nsim):
        pp = np.clip(pm + rng.normal(0, math.sqrt(tau2), len(pm)), 0, 1)
        Ls = rng.binomial(Vi, pp)
        ab.append(int((1000 * Ls < 50 * Vi).sum())); ac.append(int((1000 * Ls > 950 * Vi).sum()))
    obs_ab = int((yv[m] < 5).sum()); obs_ac = int((yv[m] > 95).sum())
    o = {'secoes': int(m.sum()), 'tau': math.sqrt(tau2), 'observado_abaixo_de_5': obs_ab, 'previsto_abaixo_de_5': float(np.mean(ab)),
         'dp_previsto_abaixo': float(np.std(ab)), 'observado_acima_de_95': obs_ac, 'previsto_acima_de_95': float(np.mean(ac)),
         'dp_previsto_acima': float(np.std(ac))}
    o['razao_abaixo'] = obs_ab / max(o['previsto_abaixo_de_5'], 1e-9); o['razao_acima'] = obs_ac / max(o['previsto_acima_de_95'], 1e-9)
    return o


def modo_paredao():
    t0 = time.time()
    rng = np.random.default_rng([SEMENTE, 4])
    b = carrega(2026); U = universo_U(b)
    L = b['L2'][U]; R = b['R2'][U]; V = L + R
    res = {'2026_2t': paredao_conta(L, R, rng)}
    log('paredao 2026', res['2026_2t']['maior_z'], res['2026_2t']['menor_z'], len(res['2026_2t']['faixas_com_absz_6_ou_mais_fora_dos_picos']))
    grava('parcial_paredao.json', res)
    # placebos
    res['placebos'] = {'2026_1t': paredao_conta(b['L1'][U], b['R1'][U], rng)}
    for ano in (2022, 2018, 2014):
        ba = carrega(ano); Ua = universo_ano(ba)
        res['placebos'][f'{ano}_2t'] = paredao_conta(ba['L2'][Ua], ba['R2'][Ua], rng)
        log('paredao placebo', ano, res['placebos'][f'{ano}_2t']['maior_z'], res['placebos'][f'{ano}_2t']['menor_z'])
    grava('parcial_paredao.json', res)
    # plantios (B6)
    pl = {}
    baixo = 20 * L < 3 * V            # y abaixo de 15
    alvo = -((-3 * V) // 20)          # teto(0,15 V)
    for nome, sel in (('teto_85_para_Flavio_em_todas', baixo), ('teto_85_para_Flavio_em_20pct', baixo & (rng.random(len(L)) < 0.2))):
        L2 = np.where(sel, alvo, L); mov = int((L2 - L).sum())
        o = paredao_conta(L2, V - L2, rng, nsim=200); o['votos_movidos'] = mov; o['secoes_alteradas'] = int(sel.sum())
        o['fracao_da_margem'] = mov / NECESSARIO
        o['z_faixas_15_0_a_15_6'] = None
        pl[nome] = o
    alto = 20 * L > 17 * V            # y acima de 85
    L2 = np.where(alto, (17 * V) // 20, L); mov = int((L - L2).sum())
    o = paredao_conta(L2, V - L2, rng, nsim=200); o['votos_movidos'] = mov; o['secoes_alteradas'] = int(alto.sum()); o['fracao_da_margem'] = mov / NECESSARIO
    pl['espelho_teto_85_para_Lula_em_todas'] = o
    for k_, o in pl.items():
        o['enxerga'] = bool(any(f['z'] >= 6 for f in o['faixas_com_absz_6_ou_mais_fora_dos_picos']))
    res['plantios'] = pl
    # tradução: votos que um teto moveria nos dados observados
    trad = {}
    for c in (95, 90, 85, 80, 70):
        exc_R = np.maximum(R - (c * V) // 100, 0); exc_L = np.maximum(L - (c * V) // 100, 0)
        trad[str(c)] = {'teto_para_Flavio_votos': int(exc_R.sum()), 'secoes': int((exc_R > 0).sum()), 'fracao_da_margem': float(exc_R.sum() / NECESSARIO),
                        'teto_para_Lula_votos': int(exc_L.sum()), 'secoes_Lula': int((exc_L > 0).sum())}
    res['votos_que_um_teto_moveria'] = trad
    grava('parcial_paredao.json', res)
    log('paredao plantios', {k: (v['enxerga'], v['votos_movidos'], v['maior_z']['z']) for k, v in pl.items()})
    # caudas contra o modelo base (B4)
    cols, base, ys, Vt, amostra = colunas_2026(b)
    reg = monta_reg({k: cols[k] for k in base}, {'y': ys['y']}, Vt, amostra, b['loc'], b['mun'])
    idx = np.nonzero(amostra)[0][reg.linhas]
    res['caudas_modelo_base_local'] = caudas_modelo(reg, base, ys['y'][idx], Vt[idx], rng)
    reg_uf = monta_reg({k: cols[k] for k in base}, {'y': ys['y']}, Vt, amostra, b['uf'], b['mun'])
    idx = np.nonzero(amostra)[0][reg_uf.linhas]
    res['caudas_modelo_efeito_fixo_de_UF'] = caudas_modelo(reg_uf, base, ys['y'][idx], Vt[idx], rng)
    grava('parcial_paredao.json', res)
    log('paredao: fim', round(time.time() - t0), res['caudas_modelo_base_local'], res['caudas_modelo_efeito_fixo_de_UF'])


# ---------------------------------------------------------------------------------------------------------------
# Degrau D1.2(c)
# ---------------------------------------------------------------------------------------------------------------
def degrau_conta(L, R, rng, nboot=1000):
    D = (L - R).astype(np.int64)
    D = D[np.abs(D) <= 80]
    h = np.bincount(D + 80, minlength=161).astype(float)
    x = np.arange(-80, 81) / 80.0
    fit = np.abs(np.arange(-80, 81)) >= 11

    def ajuste(hh):
        m = fit & (hh > 0)
        co = np.polyfit(x[m], np.log(hh[m]), 4, w=np.sqrt(hh[m]))
        pr = np.exp(np.polyval(co, x))
        Mp = hh[81:91].sum(); Mm = hh[70:80].sum()
        return math.log(Mp / Mm) - math.log(pr[81:91].sum() / pr[70:80].sum()), pr

    S, pr = ajuste(h)
    Sb = np.array([ajuste(rng.poisson(h).astype(float))[0] for _ in range(nboot)])
    ep = float(Sb.std(ddof=1))
    return {'secoes_com_D_de_-80_a_80': int(h.sum()), 'massa_D_1_a_10': int(h[81:91].sum()), 'massa_D_-10_a_-1': int(h[70:80].sum()),
            'log_razao_bruta': math.log(h[81:91].sum() / h[70:80].sum()), 'log_razao_prevista': math.log(pr[81:91].sum() / pr[70:80].sum()),
            'S': float(S), 'ep': ep, 'z': float(S / ep), 'h0': int(h[80]), 'h0_previsto': float(pr[80]),
            'z_h0': float((h[80] - pr[80]) / math.sqrt(pr[80])),
            'razao_obs_previsto_D_-10_a_10': [round(float(h[i] / pr[i]), 4) for i in range(70, 91)]}


def modo_degrau():
    rng = np.random.default_rng([SEMENTE, 5])
    b = carrega(2026); U = universo_U(b)
    L = b['L2'][U]; R = b['R2'][U]
    res = {'2026_2t': degrau_conta(L, R, rng)}
    plc = {'2026_1t': degrau_conta(b['L1'][U], b['R1'][U], rng)}
    for ano in (2022, 2018, 2014):
        ba = carrega(ano); Ua = universo_ano(ba)
        plc[f'{ano}_2t'] = degrau_conta(ba['L2'][Ua], ba['R2'][Ua], rng)
    mg = U & np.isin(b['uf'], UFS_GOV) & (b['gov'][:, 0] + b['gov'][:, 1] > 0)
    plc['2026_gov2t_G1_menos_G2'] = degrau_conta(b['gov'][mg, 0], b['gov'][mg, 1], rng)
    res['placebos'] = plc
    res['placebo_com_sinal'] = [k for k, v in plc.items() if abs(v['S']) >= 0.05 and abs(v['z']) >= 5]
    pl = {}
    D = L - R
    for q in (0.025, 0.05, 0.10):
        for lado in ('R_para_L', 'espelho_L_para_R'):
            if lado == 'R_para_L':
                sel = (D >= -10) & (D <= -1) & (rng.random(len(D)) < q); mv = np.where(sel, -((D - 1) // 2), 0)
                o = degrau_conta(L + mv, R - mv, rng, nboot=200)
            else:
                sel = (D >= 1) & (D <= 10) & (rng.random(len(D)) < q); mv = np.where(sel, (D + 2) // 2, 0)
                o = degrau_conta(L - mv, R + mv, rng, nboot=200)
            o['secoes_alteradas'] = int(sel.sum()); o['votos_movidos'] = int(mv.sum()); o['margem_em_votos'] = int(2 * mv.sum())
            o['deslocamento_de_S'] = o['S'] - res['2026_2t']['S']; o['deslocamento_em_erros'] = o['deslocamento_de_S'] / res['2026_2t']['ep']
            pl[f'{lado}_q{q}'] = o
    res['plantios'] = pl
    # tradução: quanto de margem um degrau do tamanho do limiar (S = 0,05) e do tamanho medido representaria
    res['traducao'] = {'votos_por_unidade_de_S': pl['R_para_L_q0.025']['votos_movidos'] / max(pl['R_para_L_q0.025']['deslocamento_de_S'], 1e-9)}
    grava('parcial_degrau.json', res)
    log('degrau', {k: (round(v['S'], 4), round(v['z'], 2), round(v['z_h0'], 2)) for k, v in [('2026_2t', res['2026_2t'])] + list(plc.items())})
    log('degrau plantios', {k: (round(v['deslocamento_de_S'], 4), round(v['deslocamento_em_erros'], 1), v['votos_movidos']) for k, v in pl.items()})


# ---------------------------------------------------------------------------------------------------------------
# Limiar de contagem D1.3 e gatilho por contagem da equipe vermelha
# ---------------------------------------------------------------------------------------------------------------
NS_EV = list(range(50, 301, 25))
Z_EV_CONTAGEM = 3.3172      # 1% bilateral dividido por 11 cortes


def modo_limiar():
    t0 = time.time()
    rng = np.random.default_rng([SEMENTE, 6])
    b = carrega(2026); U = universo_U(b)
    cols, base, ys, V, am = colunas_2026(b)
    R26 = monta_reg(cols, ys, V, am, b['loc'], b['mun'])
    anos = {}
    for ano in (2022, 2018):
        ba = carrega(ano)
        c_, bs_, y_, V_, am_ = colunas_ano(ba, b)
        anos[ano] = {'b': ba, 'cols': c_, 'base': bs_, 'ys': y_, 'V': V_, 'am': am_, 'R': monta_reg(c_, y_, V_, am_, ba['loc'], ba['mun'])}
        log('regressao', ano, anos[ano]['R'].n, anos[ano]['R'].G)
    R22 = anos[2022]['R']; R18 = anos[2018]['R']; base22 = anos[2022]['base']; base18 = anos[2018]['base']
    expo = {K: float((cols[f'D{K}'][U] * V[U]).sum()) for K in KS_LIMIAR}
    expo_bn = {K: float((cols[f'D{K}'][U] * b['comp2'][U]).sum()) for K in KS_LIMIAR}
    res = {'amostra_2026': {'U': int(U.sum()), 'com_perfil': int(am.sum()), 'na_regressao': R26.n, 'locais': R26.locais,
                            'municipios': R26.G, 'colunas_sem_variacao': R26.sem_variacao, 'X': base},
           'amostra_2022': {'universo': int(universo_ano(anos[2022]['b']).sum()), 'com_chave_e_perfil_de_2026': int(anos[2022]['am'].sum()),
                            'na_regressao': R22.n, 'locais': R22.locais, 'municipios': R22.G, 'X': base22},
           'amostra_2018': {'universo': int(universo_ano(anos[2018]['b']).sum()), 'com_chave_e_perfil_de_2026': int(anos[2018]['am'].sum()),
                            'na_regressao': R18.n, 'locais': R18.locais, 'municipios': R18.G},
           'secoes_de_U_com_comparecimento_ate_K': {str(K): int((b['comp2'][U] <= K).sum()) for K in KS_LIMIAR},
           'dose_media_ponderada': {str(K): expo[K] / float(V[U].sum()) for K in KS_LIMIAR},
           'b_que_corresponde_a_Phi_1': {str(K): MARGEM * 100 / (2 * expo[K]) for K in KS_LIMIAR}}

    def tabela(R, bs, y):
        out = {}
        for K in KS_LIMIAR:
            r = R.ajusta(bs + [f'D{K}'], y); rj = R.ajusta(bs + [f'D{K}', 'inv'], y)
            out[K] = {'b': r['coef'][f'D{K}'], 'ep': r['ep'][f'D{K}'], 'b_joelho': rj['coef'][f'D{K}'], 'ep_joelho': rj['ep'][f'D{K}']}
        return out

    pt = {(ano, y): tabela(R, bs, y) for ano, R, bs in ((2026, R26, base), (2022, R22, base22), (2018, R18, base18)) for y in ('y', 'ybn')}
    log('pontos', {K: (round(pt[2026, 'y'][K]['b'], 3), round(pt[2022, 'y'][K]['b'], 3), round(pt[2018, 'y'][K]['b'], 3)) for K in KS_LIMIAR})
    # bootstrap de municípios, o mesmo sorteio nos três anos (L3)
    uniao = np.unique(np.concatenate([R26.grupos, R22.grupos, R18.grupos]))
    pos = {g: i for i, g in enumerate(uniao)}
    ii = {2026: np.array([pos[g] for g in R26.grupos]), 2022: np.array([pos[g] for g in R22.grupos]), 2018: np.array([pos[g] for g in R18.grupos])}
    NB = 500
    boot = {(ano, y, K, s): np.empty(NB) for ano in (2026, 2022, 2018) for y in ('y', 'ybn') for K in KS_LIMIAR for s in 'pj'}
    for r in range(NB):
        m = rng.multinomial(len(uniao), np.full(len(uniao), 1 / len(uniao))).astype(float)
        for ano, R, bs in ((2026, R26, base), (2022, R22, base22), (2018, R18, base18)):
            A, C = R.somas(m[ii[ano]])
            for K in KS_LIMIAR:
                for y in ('y', 'ybn'):
                    boot[ano, y, K, 'p'][r] = R.resolve(A, C, bs + [f'D{K}'], y)[-1]
                    boot[ano, y, K, 'j'][r] = R.resolve(A, C, bs + [f'D{K}', 'inv'], y)[-2]
    log('bootstrap pronto', round(time.time() - t0))
    grupos_uf = {ano: np.array([g.split('|')[0] for g in R.grupos]) for ano, R in ((2026, R26), (2022, R22))}
    lim = {'25': None, '50': 0.25, '75': 0.15, '100': 0.15, '150': 0.15, '200': 0.15}
    saida = {}
    for y in ('y', 'ybn'):
        saida[y] = {}
        for K in KS_LIMIAR:
            p26, p22, p18 = pt[2026, y][K], pt[2022, y][K], pt[2018, y][K]
            dif = p26['b'] - p22['b']
            epb = float((boot[2026, y, K, 'p'] - boot[2022, y, K, 'p']).std(ddof=1))
            esc = (2 * expo[K] / 100 / MARGEM) if y == 'y' else (-expo_bn[K] / 100 / MARGEM)
            phi = dif * esc; ep_phi = epb * abs(esc)
            o = {'b_2026': p26['b'], 'ep_2026_cr1': p26['ep'], 'ep_2026_bootstrap': float(boot[2026, y, K, 'p'].std(ddof=1)),
                 'b_2022': p22['b'], 'ep_2022_cr1': p22['ep'], 'diferenca': dif, 'ep_bootstrap': epb, 'z': dif / epb,
                 'ep_analitico_soma': math.hypot(p26['ep'], p22['ep']),
                 'Phi_diferenca': phi, 'Phi_ic99': [phi - Z99 * ep_phi, phi + Z99 * ep_phi],
                 'Phi_so_2026': p26['b'] * esc, 'Phi_so_2026_ic99': [p26['b'] * esc - Z99 * p26['ep'] * abs(esc), p26['b'] * esc + Z99 * p26['ep'] * abs(esc)],
                 'votos_de_margem_diferenca': phi * MARGEM, 'votos_de_margem_ic99': [(phi - Z99 * ep_phi) * MARGEM, (phi + Z99 * ep_phi) * MARGEM],
                 'joelho_2026': {'b': p26['b_joelho'], 'ep': p26['ep_joelho'], 'z': p26['b_joelho'] / p26['ep_joelho'], 'Phi': p26['b_joelho'] * esc},
                 'joelho_2022': {'b': p22['b_joelho'], 'ep': p22['ep_joelho'], 'z': p22['b_joelho'] / p22['ep_joelho']},
                 'joelho_diferenca': {'dif': p26['b_joelho'] - p22['b_joelho'],
                                      'ep_bootstrap': float(np.nanstd(boot[2026, y, K, 'j'] - boot[2022, y, K, 'j'], ddof=1)),
                                      'reamostras_sem_solucao': int(np.isnan(boot[2026, y, K, 'j'] - boot[2022, y, K, 'j']).sum())},
                 'placebo_2018': {'b_2018': p18['b'], 'ep_cr1': p18['ep'],
                                  'dif_2026_menos_2018': p26['b'] - p18['b'],
                                  'ep_2026_menos_2018': float((boot[2026, y, K, 'p'] - boot[2018, y, K, 'p']).std(ddof=1)),
                                  'dif_2022_menos_2018': p22['b'] - p18['b'],
                                  'ep_2022_menos_2018': float((boot[2022, y, K, 'p'] - boot[2018, y, K, 'p']).std(ddof=1))}}
            o['joelho_diferenca']['z'] = o['joelho_diferenca']['dif'] / o['joelho_diferenca']['ep_bootstrap']
            pl = o['placebo_2018']
            pl['Phi_2026_menos_2018'] = pl['dif_2026_menos_2018'] * esc; pl['z_2026_menos_2018'] = pl['dif_2026_menos_2018'] / pl['ep_2026_menos_2018']
            pl['Phi_2022_menos_2018'] = pl['dif_2022_menos_2018'] * esc; pl['z_2022_menos_2018'] = pl['dif_2022_menos_2018'] / pl['ep_2022_menos_2018']
            reg_ = {}
            for nome, ufs in REGIOES.items():
                a = R26.ajusta(base + [f'D{K}'], y, sel=np.isin(grupos_uf[2026], ufs))
                c = R22.ajusta(base22 + [f'D{K}'], y, sel=np.isin(grupos_uf[2022], ufs))
                d_ = a['coef'][f'D{K}'] - c['coef'][f'D{K}']
                reg_[nome] = {'b_2026': a['coef'][f'D{K}'], 'b_2022': c['coef'][f'D{K}'], 'diferenca': d_,
                              'ep': math.hypot(a['ep'][f'D{K}'], c['ep'][f'D{K}']), 'Phi_sentido': d_ * esc}
            o['regioes'] = reg_
            o['regioes_no_sentido_da_nacional'] = int(sum(1 for v in reg_.values() if np.sign(v['Phi_sentido']) == np.sign(phi)))
            L_ = lim[str(K)]
            o['cond_sinal_pro_Lula' if y == 'y' else 'cond_sinal_conversao'] = bool(
                phi >= 0.25 and o['z'] * np.sign(esc) >= 3.9 and o['joelho_2026']['Phi'] > 0 and abs(o['joelho_2026']['z']) >= 2
                and o['regioes_no_sentido_da_nacional'] >= 4)
            o['cond_sinal_sentido_contrario'] = bool(
                phi <= -0.25 and o['z'] * np.sign(esc) <= -3.9 and o['joelho_2026']['Phi'] < 0 and abs(o['joelho_2026']['z']) >= 2
                and o['regioes_no_sentido_da_nacional'] >= 4)
            o['limite_sem_sinal'] = L_
            o['dentro_do_limite_sem_sinal'] = None if L_ is None else bool(o['Phi_ic99'][0] >= -L_ and o['Phi_ic99'][1] <= L_)
            saida[y][str(K)] = o
    res['principal'] = saida
    grava('parcial_limiar.json', res)
    log('principal', {K: (round(saida['y'][str(K)]['Phi_diferenca'], 3), round(saida['y'][str(K)]['z'], 2)) for K in KS_LIMIAR})
    # sensibilidade: as duas regressões sem o perfil (L2)
    sem_pf = [c for c in base if c not in COLS_PERFIL_X]
    ba = anos[2022]['b']; c_, bs_, y_, V_, am_ = colunas_ano(ba, b, com_perfil=False)
    R22s = monta_reg(c_, y_, V_, am_, ba['loc'], ba['mun'])
    sens = {}
    for K in KS_LIMIAR:
        a = R26.ajusta(sem_pf + [f'D{K}'], 'y'); c = R22s.ajusta(bs_ + [f'D{K}'], 'y')
        d_ = a['coef'][f'D{K}'] - c['coef'][f'D{K}']; ep = math.hypot(a['ep'][f'D{K}'], c['ep'][f'D{K}'])
        sens[str(K)] = {'b_2026': a['coef'][f'D{K}'], 'b_2022': c['coef'][f'D{K}'], 'diferenca': d_, 'ep': ep,
                        'Phi': d_ * 2 * expo[K] / 100 / MARGEM, 'ep_Phi': ep * 2 * expo[K] / 100 / MARGEM, 'n_2022': c['n']}
    res['sensibilidade_sem_perfil'] = sens
    # tabela do resíduo em 25 faixas de comparecimento (L10)
    e26 = R26.ajusta(base, 'y')['residuo']; c26 = b['comp2'][np.nonzero(am)[0][R26.linhas]]
    e22 = R22.ajusta(base22, 'y')['residuo']; c22 = ba['comp2'][np.nonzero(anos[2022]['am'])[0][R22.linhas]]
    bordas = np.quantile(c26, np.linspace(0, 1, 26)); bordas[0] = 0; bordas[-1] = 1e9
    tab = []
    for i in range(25):
        m26 = (c26 > bordas[i]) & (c26 <= bordas[i + 1]); m22 = (c22 > bordas[i]) & (c22 <= bordas[i + 1])
        tab.append({'comp_de': float(bordas[i]), 'comp_ate': float(bordas[i + 1]), 'n_2026': int(m26.sum()),
                    'residuo_2026': float(np.average(e26[m26], weights=R26.w[m26])) if m26.any() else None,
                    'n_2022': int(m22.sum()), 'residuo_2022': float(np.average(e22[m22], weights=R22.w[m22])) if m22.any() else None})
    res['residuo_por_faixa_de_comparecimento'] = tab
    grava('parcial_limiar.json', res)
    # ---------------- calibração (L7)
    lin = np.nonzero(am)[0][R26.linhas]
    Rv = b['R2'][lin]; Lv = b['L2'][lin]; Vv = V[lin]; BNv = (b['B2'] + b['N2'])[lin]; Cv = b['comp2'][lin].astype(float)
    aP = {K: R26.projetor(base + [f'D{K}'], f'D{K}') for K in KS_LIMIAR}
    aJ = {K: R26.projetor(base + [f'D{K}', 'inv'], f'D{K}') for K in KS_LIMIAR}
    res['conferencia_do_projetor'] = {str(K): [float(aP[K] @ ys['y'][lin]), pt[2026, 'y'][K]['b']] for K in KS_LIMIAR}
    NREP = 200
    cal = {}
    for K in KS_LIMIAR:
        Dk = cols[f'D{K}'][lin]; epm = saida['y'][str(K)]['ep_bootstrap']; epj = saida['y'][str(K)]['joelho_2026']['ep']
        cal[str(K)] = {}
        for phi in (0.10, 0.25, 0.5, 1.0):
            f = phi * NECESSARIO / float((cols[f'D{K}'][U] * b['R2'][U]).sum())
            db = np.empty(NREP); dj = np.empty(NREP)
            for r in range(NREP):
                dy = 100 * rng.binomial(Rv, np.minimum(1.0, f * Dk)) / Vv
                db[r] = aP[K] @ dy; dj[r] = aJ[K] @ dy
            alvo = phi * MARGEM * 100 / (2 * expo[K])
            cal[str(K)][f'Phi_{phi}'] = {'taxa_f': f, 'deslocamento_medio_b': float(db.mean()), 'b_esperado': alvo, 'recuperacao': float(db.mean() / alvo),
                                         'deslocamento_em_erros': float(db.mean() / epm), 'deteccao_z_3_9': float((db / epm >= 3.9).mean()),
                                         'joelho_deslocamento_medio': float(dj.mean()), 'joelho_em_erros': float(dj.mean() / epj),
                                         'joelho_deteccao_z_2': float((dj / epj >= 2).mean())}
        f = 0.25 * NECESSARIO / float((cols[f'D{K}'][U] * b['L2'][U]).sum())
        db = np.array([aP[K] @ (-100 * rng.binomial(Lv, np.minimum(1.0, f * Dk)) / Vv) for _ in range(NREP)])
        cal[str(K)]['espelho_Phi_0.25'] = {'deslocamento_em_erros': float(db.mean() / epm), 'deteccao_z_3_9': float((-db / epm >= 3.9).mean())}
        epbn = saida['ybn'][str(K)]['ep_bootstrap']
        for phi in (0.10, 0.25):
            f = phi * MARGEM / float((cols[f'D{K}'][U] * (b['B2'] + b['N2'])[U]).sum())
            db = np.array([aP[K] @ (-100 * rng.binomial(BNv, np.minimum(1.0, f * Dk)) / Cv) for _ in range(NREP)])
            cal[str(K)][f'ybn_Phi_{phi}'] = {'taxa_f': f, 'deslocamento_medio_b': float(db.mean()), 'deslocamento_em_erros': float(-db.mean() / epbn),
                                             'deteccao_z_3_9': float((-db / epbn >= 3.9).mean()),
                                             'Phi_recuperado': float(-db.mean() / 100 * expo_bn[K] / MARGEM)}
        log('calibracao K', K, {k: (round(v.get('recuperacao', 0), 3), v['deteccao_z_3_9']) for k, v in cal[str(K)].items()})
    res['calibracao'] = cal
    # explicação inocente plantada: dose suave, sem joelho
    Ds_all = np.clip(np.log(np.maximum(b['comp2'], 1) / 20) / math.log(20), 0, 1); Ds = Ds_all[lin]
    ino = {}
    for phi in (0.25, 0.5):
        f = phi * NECESSARIO / float((Ds_all[U] * b['R2'][U]).sum())
        acc = {K: [[], []] for K in KS_LIMIAR}
        for r in range(NREP):
            dy = 100 * rng.binomial(Rv, np.minimum(1.0, f * Ds)) / Vv
            for K in KS_LIMIAR:
                acc[K][0].append(aP[K] @ dy); acc[K][1].append(aJ[K] @ dy)
        ino[f'Phi_{phi}'] = {str(K): {'principal_deslocamento_em_erros': float(np.mean(acc[K][0]) / saida['y'][str(K)]['ep_bootstrap']),
                                      'principal_Phi_aparente': float(np.mean(acc[K][0]) * 2 * expo[K] / 100 / MARGEM),
                                      'joelho_deslocamento_em_erros': float(np.mean(acc[K][1]) / saida['y'][str(K)]['joelho_2026']['ep']),
                                      'joelho_passaria_de_2': bool(np.mean(acc[K][1]) / saida['y'][str(K)]['joelho_2026']['ep'] >= 2)}
                             for K in KS_LIMIAR}
    res['explicacao_inocente_plantada'] = ino
    grava('parcial_limiar.json', res)
    log('calibracao pronta', round(time.time() - t0))
    # ---------------- placebos (L9): governador e 1º turno contra 2022
    gov = {}
    c1 = np.maximum(b['comp1'], 1).astype(float)
    colsg = dict(cols); colsg['fG1'] = b['gov'][:, 2] / c1; colsg['fG2'] = b['gov'][:, 3] / c1
    Vg = (b['gov'][:, 0] + b['gov'][:, 1]).astype(float)
    ysg = {'yg': 100 * b['gov'][:, 0] / np.maximum(Vg, 1), 'y': ys['y']}
    for uf in UFS_GOV:
        mg = am & (b['uf'] == uf) & (Vg >= 30)
        Rg = monta_reg(colsg, ysg, Vg, mg, b['loc'], b['loc'])
        gov[uf] = {'n': Rg.n}
        for K in KS_LIMIAR:
            r = Rg.ajusta(base + ['fG1', 'fG2', f'D{K}'], 'yg'); rp = Rg.ajusta(base + [f'D{K}'], 'y')
            gov[uf][str(K)] = {'b_governador': r['coef'][f'D{K}'], 'ep': r['ep'][f'D{K}'], 'b_presidente_mesmas_secoes': rp['coef'][f'D{K}'], 'ep_presidente': rp['ep'][f'D{K}']}
    gov['resumo'] = {}
    for K in KS_LIMIAR:
        bs_ = np.array([gov[uf][str(K)]['b_governador'] for uf in UFS_GOV]); es_ = np.array([gov[uf][str(K)]['ep'] for uf in UFS_GOV])
        w_ = 1 / es_ ** 2
        bp_ = np.array([gov[uf][str(K)]['b_presidente_mesmas_secoes'] for uf in UFS_GOV]); ep_ = np.array([gov[uf][str(K)]['ep_presidente'] for uf in UFS_GOV])
        wp_ = 1 / ep_ ** 2
        gov['resumo'][str(K)] = {'media_modulo_b_governador': float(np.abs(bs_).mean()), 'qui2_dos_6_z': float(((bs_ / es_) ** 2).sum()),
                                 'b_presidente_ivw': float((wp_ * bp_).sum() / wp_.sum()), 'ep_presidente_ivw': float(1 / math.sqrt(wp_.sum())),
                                 'qui2_presidente': float(((bp_ / ep_) ** 2).sum())}
    res['placebo_governador'] = gov
    b22 = anos[2022]['b']
    pos22 = {k: i for i, k in enumerate(b22['chave'])}
    j22 = np.array([pos22.get(k, -1) for k in b['chave']]); tem22 = j22 >= 0; j = np.maximum(j22, 0)
    tem22 &= universo_ano(b22)[j]
    c1_22 = np.maximum(b22['comp1'][j], 1).astype(float)
    V1 = (b['L1'] + b['R1']).astype(float)
    colsp = {'y22': 100 * b22['L2'][j] / np.maximum(b22['L2'][j] + b22['R2'][j], 1), 'fL22': b22['L1'][j] / c1_22, 'fR22': b22['R1'][j] / c1_22,
             'fB22': b22['B1'][j] / c1_22, 'fN22': b22['N1'][j] / c1_22, 'abst22': 1 - b22['comp1'][j] / np.maximum(b22['apt1'][j], 1)}
    colsp['dab'] = (1 - b['comp1'] / np.maximum(b['apt1'], 1)) - colsp['abst22']
    for nm in COLS_PERFIL_X:
        colsp[nm] = cols[nm]
    colsp['lnapt1'] = np.log(np.maximum(b['apt1'], 1)); colsp['pos'] = cols['pos']
    basep = list(colsp)
    for K in KS_LIMIAR:
        colsp[f'D{K}'] = np.maximum(0.0, 1 - K / c1)
    mp = am & tem22 & (V1 >= 30)
    Rp = monta_reg(colsp, {'y1': 100 * b['L1'] / np.maximum(V1, 1)}, V1, mp, b['loc'], b['mun'])
    p1 = {'n': Rp.n}
    for K in KS_LIMIAR:
        r = Rp.ajusta(basep + [f'D{K}'], 'y1'); e1 = float((colsp[f'D{K}'][mp] * V1[mp]).sum())
        p1[str(K)] = {'b': r['coef'][f'D{K}'], 'ep': r['ep'][f'D{K}'], 'z': r['coef'][f'D{K}'] / r['ep'][f'D{K}'],
                      'Phi_equivalente': r['coef'][f'D{K}'] * 2 * e1 / 100 / MARGEM}
    res['placebo_1t_2026_contra_2022'] = p1
    grava('parcial_limiar.json', res)
    log('placebos prontos', round(time.time() - t0))
    # ---------------- equipe vermelha: gatilho por contagem (T1, T2)
    def contagem(bb, mask, com_ln=True):
        V_ = (bb['L2'] + bb['R2']).astype(float); V1_ = (bb['L1'] + bb['R1']).astype(float)
        mk = mask & (V1_ > 0)
        c2 = np.maximum(bb['comp2'], 1).astype(float)
        cc = {f'x{N}': np.maximum(0.0, c2 - N) / c2 for N in NS_EV}
        cc['dcomp'] = 100 * (bb['comp2'] - bb['comp1']) / np.maximum(bb['apt2'], 1); cc['lncomp'] = np.log(c2)
        yy = {'dy': 100 * bb['L2'] / np.maximum(V_, 1) - 100 * bb['L1'] / np.maximum(V1_, 1)}
        Rc = monta_reg(cc, yy, V_, mk, bb['loc'], bb['loc'])
        ctr = ['dcomp', 'lncomp'] if com_ln else ['dcomp']
        out = {}
        for N in NS_EV:
            r = Rc.ajusta([f'x{N}'] + ctr, 'dy')
            out[str(N)] = {'coef': r['coef'][f'x{N}'], 'ep': r['ep'][f'x{N}'], 'z': r['coef'][f'x{N}'] / r['ep'][f'x{N}']}
        return out, Rc, mk, ctr

    ev26, Rc, mk, ctr = contagem(b, U)
    ev22, _, _, _ = contagem(b22, universo_ano(b22))
    ev26_sem, _, _, _ = contagem(b, U, com_ln=False); ev22_sem, _, _, _ = contagem(b22, universo_ano(b22), com_ln=False)
    linc = np.nonzero(mk)[0][Rc.linhas]
    aN = {N: Rc.projetor([f'x{N}'] + ctr, f'x{N}') for N in NS_EV}
    calc = {}
    for K in (100, 200):
        for phi in (0.25, 1.0):
            f = phi * NECESSARIO / float((cols[f'D{K}'][U] * b['R2'][U]).sum())
            acc = {N: [] for N in NS_EV}
            for r in range(20):
                dy = 100 * rng.binomial(b['R2'][linc], np.minimum(1.0, f * cols[f'D{K}'][linc])) / V[linc]
                for N in NS_EV:
                    acc[N].append(aN[N] @ dy)
            calc[f'K{K}_Phi{phi}'] = {str(N): {'deslocamento': float(np.mean(acc[N])), 'em_erros': float(np.mean(acc[N]) / ev26[str(N)]['ep'])} for N in NS_EV}
    for N in NS_EV:
        o = ev26[str(N)]; o['coef_2022'] = ev22[str(N)]['coef']; o['ep_2022'] = ev22[str(N)]['ep']
        o['sem_ln_coef'] = ev26_sem[str(N)]['coef']; o['sem_ln_ep'] = ev26_sem[str(N)]['ep']; o['sem_ln_coef_2022'] = ev22_sem[str(N)]['coef']
        o['cond_sinal'] = bool(o['coef'] >= 4 and o['z'] >= Z_EV_CONTAGEM and abs(o['coef_2022']) < 1.5)
        o['cond_sinal_contrario'] = bool(o['coef'] <= -4 and o['z'] <= -Z_EV_CONTAGEM and abs(o['coef_2022']) < 1.5)
        o['dentro_de_1_5'] = bool(abs(o['coef']) <= 1.5)
    res['EV_contagem'] = {'cortes': ev26, 'n': Rc.n, 'locais': Rc.G, 'calibracao': calc}
    grava('parcial_limiar.json', res)
    log('EV contagem', {N: (round(ev26[str(N)]['coef'], 2), round(ev26[str(N)]['z'], 1), round(ev26[str(N)]['coef_2022'], 2)) for N in NS_EV})
    log('limiar: fim', round(time.time() - t0))


# ---------------------------------------------------------------------------------------------------------------
# EXPLORATÓRIO (feito depois de ver o resultado do pente em brancos e nulos)
# ---------------------------------------------------------------------------------------------------------------
def modo_exploratorio():
    """exploratorio_artefato_bn: a estatística da letra do D1.2(a) dispara em histograma SEM pente de contagens pequenas?
    Histogramas sorteados pelo gerador E2 (binomial por seção, sem regra nenhuma) passam pela conta da letra. Se ela
    der |Z| de 8 ou mais com amplitude de 2% nesses sorteios, o disparo em B2 e N2 é do alisamento, não de pente."""
    rng = np.random.default_rng([SEMENTE, 7])
    b = carrega(2026); U = universo_U(b)
    out = {}
    d12 = le('parcial_pente_D12a.json')['rodadas']
    rodadas = [('pais', U)] + [('uf_' + uf, U & (b['uf'] == uf)) for uf in sorted(set(b['uf'][U]))]
    for rn, mask in rodadas:
        for X, vmin in (('B2', 3), ('N2', 3)) + ((('R2', 10), ('L2', 10)) if rn == 'pais' else ()):
            obs = d12.get(f'{rn}|{X}', {})
            if not obs.get('avaliavel'):
                continue
            Hs, s = sorteios_binomiais(b[X][mask], b['comp2'][mask], b['mun'][mask], rng, nsim=100)
            zs = []; dispara = 0
            for h in Hs:
                pt = Pente(h, vmin)
                if pt.n < 2 or not pt.valido.any():
                    continue
                o, _, _ = pt.observado(top=1)
                zs.append(o['maxabsZ'])
                dispara += int(o['maxabsZ'] >= 8 and abs(o['maiores_Z'][0]['amplitude']) >= 0.02)
            zs = np.array(zs)
            out[f'{rn}|{X}'] = {'observado_maxabsZ': obs['maxabsZ'], 'sorteios': len(zs), 'sorteios_maxabsZ_mediana': float(np.median(zs)),
                                'sorteios_maxabsZ_min': float(zs.min()), 'sorteios_maxabsZ_max': float(zs.max()),
                                'fracao_dos_sorteios_com_Z8_e_amplitude': dispara / max(len(zs), 1),
                                'sinal_numerico_pela_letra_no_observado': bool(obs.get('sinal_numerico'))}
        log('exploratorio', rn, {k.split('|')[1]: (round(v['observado_maxabsZ'], 1), round(v['sorteios_maxabsZ_mediana'], 1), v['fracao_dos_sorteios_com_Z8_e_amplitude'])
                                 for k, v in out.items() if k.startswith(rn + '|')})
    grava('parcial_exploratorio.json', out)


# ---------------------------------------------------------------------------------------------------------------
# Relatório
# ---------------------------------------------------------------------------------------------------------------
def br(x, d=2):
    return 'n.d.' if x is None or (isinstance(x, float) and math.isnan(x)) else f'{x:.{d}f}'.replace('.', ',')


def mil(x):
    return f'{int(round(x)):,}'.replace(',', '.')


def vereditos():
    d12 = le('parcial_pente_D12a.json'); d42 = le('parcial_pente_D42.json'); ev = le('parcial_pente_EV.json')
    par = le('parcial_paredao.json'); deg = le('parcial_degrau.json'); lim = le('parcial_limiar.json')
    v = {}
    # D1.2(a)
    R = d12['rodadas']
    r20 = [k for k in R if k.startswith('pais|') or k.startswith('modelo_')]
    letra = ['R_para_L_q1_k110|R2', 'R_para_L_q1_k56|R2', 'R_para_L_q1_k28|R2', 'R_para_L_q0.25_k7|R2',
             'fracao_arredondada_Phi0.25|R2', 'fracao_arredondada_Phi0.5|R2', 'fracao_arredondada_Phi1.0|R2']
    poder = all(d12['plantios'][k]['enxerga_Z8'] for k in letra)
    a = {}
    for X in ('R2', 'L2', 'B2', 'N2'):
        sinal = sorted(k for k in R if k.endswith('|' + X) and R[k].get('sinal_numerico'))
        sem = all(R[k]['sem_sinal_numerico'] for k in r20 if k.endswith('|' + X))
        a[X] = {'veredito': 'SEM PODER' if not poder else ('SINAL' if sinal else ('SEM SINAL' if sem else 'INCONCLUSIVO')),
                'rodadas_com_condicoes_de_sinal_e_placebo_ausente': sinal, 'sem_sinal_no_pais_e_nos_modelos': bool(sem)}
    a['plantios_da_letra_enxergados'] = bool(poder)
    a['combinado_pela_letra'] = ('SEM PODER' if not poder else 'SINAL' if any(a[X]['veredito'] == 'SINAL' for X in ('R2', 'B2', 'N2'))
                                 else 'SEM SINAL' if all(a[X]['veredito'] == 'SEM SINAL' for X in ('R2', 'L2', 'B2', 'N2')) else 'INCONCLUSIVO')
    v['D1.2a'] = a
    # D4-2
    nac = d42['nacional']; conj = d42['nulo_do_conjunto_de_recortes']; mp = d42['maior_placebo']
    coer = lambda o: sum(t >= 6.9 for t in o['termos_do_pico']) >= 2
    recs = {k: o for k, o in d42['recortes'].items() if o.get('Z') is not None}
    s_nac = [X for X in ('R2', 'L2') if nac[X]['Z'] > 1.5 * nac[X]['nulo']['max'] and nac[X]['Z'] > 1.5 * mp and coer(nac[X])]
    s_rec = [k for k, o in recs.items() if o['Z'] > conj['limiar_de_sinal'] and o['Z'] > 1.5 * mp and coer(o)]
    sem = (all(nac[X]['Z'] < nac[X]['nulo']['q99'] and nac[X]['Z'] < mp for X in ('R2', 'L2'))
           and all(o['Z'] < conj['q99'] and o['Z'] < mp for o in recs.values()))
    pod = d42['plantios']['R2_2026']['piso_0.0357_em_1.0_das_secoes']['enxerga']
    v['D4-2'] = {'veredito': 'SEM PODER' if not pod else 'SINAL' if (s_nac or s_rec) else 'SEM SINAL' if sem else 'INCONCLUSIVO',
                 'sinal_nacional': s_nac, 'sinal_em_recorte': s_rec, 'recortes_avaliaveis': len(recs),
                 'recortes_nao_avaliaveis': len(d42['recortes']) - len(recs)}
    # equipe vermelha, módulo k
    pod = ev['R2']['plantado_um_a_cada_28']['detectado_z_acima_de_20']
    e = {}
    for X in ('R2', 'L2', 'B2', 'N2'):
        e[X] = 'SEM PODER' if not pod else 'SINAL' if ev[X]['sinal_numerico'] else 'SEM SINAL' if ev[X]['abaixo_do_q99_do_maximo'] else 'INCONCLUSIVO'
    e['combinado_pela_letra'] = ('SEM PODER' if not pod else 'SINAL' if any(e[X] == 'SINAL' for X in ('R2', 'L2', 'B2', 'N2'))
                                 else 'SEM SINAL' if all(e[X] == 'SEM SINAL' for X in ('R2', 'L2', 'B2', 'N2')) else 'INCONCLUSIVO')
    v['EV_modulo'] = e
    # paredão
    p = par['2026_2t']; fora = p['faixas_com_absz_6_ou_mais_fora_dos_picos']; cm = par['caudas_modelo_base_local']
    caudas = [(cm['observado_abaixo_de_5'], cm['previsto_abaixo_de_5']), (cm['observado_acima_de_95'], cm['previsto_acima_de_95'])]
    vazia = any(pr >= 200 and ob == 0 for ob, pr in caudas)
    caudas_ok = all(pr < 200 or 0.5 <= ob / pr <= 2 for ob, pr in caudas)
    pod = par['plantios']['teto_85_para_Flavio_em_todas']['enxerga']
    v['D1.2b'] = {'veredito': 'SEM PODER' if not pod else 'SINAL' if (any(f['z'] >= 6 for f in fora) or vazia) else 'SEM SINAL' if (not fora and caudas_ok) else 'INCONCLUSIVO',
                  'caudas_dentro_do_previsto': bool(caudas_ok), 'cauda_vazia': bool(vazia)}
    # degrau
    g = deg['2026_2t']; pod = deg['plantios']['R_para_L_q0.025']['deslocamento_em_erros'] >= 5
    v['D1.2c'] = {'veredito': 'SEM PODER' if not pod else 'SINAL' if (abs(g['S']) >= 0.05 and abs(g['z']) >= 5 and not deg['placebo_com_sinal'])
                  else 'SEM SINAL' if abs(g['S']) < 0.02 else 'INCONCLUSIVO'}
    # limiar
    l = {}
    for y, chave, cal in (('y', 'cond_sinal_pro_Lula', 'Phi_0.25'), ('ybn', 'cond_sinal_conversao', 'ybn_Phi_0.25')):
        l[y] = {}
        for K in ('50', '75', '100', '150', '200'):
            o = lim['principal'][y][K]; det = lim['calibracao'][K][cal]['deteccao_z_3_9']
            l[y][K] = ('SINAL' if o[chave] else 'SINAL NO SENTIDO CONTRÁRIO' if o['cond_sinal_sentido_contrario'] else 'SEM PODER' if det < 0.95
                       else 'SEM SINAL' if o['dentro_do_limite_sem_sinal'] else 'INCONCLUSIVO')
    v['D1.3'] = l
    c = lim['EV_contagem']['cortes']; cal = lim['EV_contagem']['calibracao']
    pod = cal['K100_Phi1.0']['100']['em_erros'] >= Z_EV_CONTAGEM and cal['K200_Phi1.0']['200']['em_erros'] >= Z_EV_CONTAGEM
    v['EV_contagem'] = {'veredito': 'SEM PODER' if not pod else 'SINAL' if any(o['cond_sinal'] or o['cond_sinal_contrario'] for o in c.values())
                        else 'SEM SINAL' if all(o['dentro_de_1_5'] for o in c.values()) else 'INCONCLUSIVO'}
    return v


def modo_relatorio():
    import textwrap
    meta = le('base_meta.json'); d12 = le('parcial_pente_D12a.json'); d42 = le('parcial_pente_D42.json'); ev = le('parcial_pente_EV.json')
    par = le('parcial_paredao.json'); deg = le('parcial_degrau.json'); lim = le('parcial_limiar.json'); ex = le('parcial_exploratorio.json')
    v = vereditos()
    R = d12['rodadas']; PL = d12['plantios']
    T = []

    def P(txt='', rec=0):
        if not txt:
            T.append(''); return
        T.extend(textwrap.wrap(txt, 118, initial_indent=' ' * rec, subsequent_indent=' ' * (rec + 2)))

    def lz(k):
        o = R[k]; t = o['maiores_Z'][0]; n = o['nulo']
        return (f"|Z| máximo {br(o['maxabsZ'])} (p = {t['p']}, o = {t['o']}, Z = {br(t['Z'])}, amplitude {br(100 * t['amplitude'], 1)}%); nulo: mediana "
                f"{br(n['maxabsZ_q50'])}, percentil 99 {br(n['maxabsZ_q99'])}, maior {br(n['maxabsZ_max'])}. Periodograma: pico {br(o['periodograma']['P_max'], 1)} "
                f"(período {br(o['periodograma']['periodo'])}; z equivalente {br(o['periodograma']['z_equivalente'])}); nulo: percentil 99 {br(n['P_q99'], 1)}, maior {br(n['P_max'], 1)}.")

    P('R27_B4, REGRA DETERMINÍSTICA: PENTE, PAREDÃO, DEGRAU E LIMIAR DE CONTAGEM (RESULTADOS)')
    P()
    P('Registro: Adendo 27 (commit 2748895, 10/11/2026 00:16:42 UTC), ordem do Adendo 30 (commit a7218fb). Testes D1.2 e D1.3 de '
      'desenho_D1_proposta.json, D4-2 de desenho_D4_proposta.json (desenhos cegos) e a fragilidade "V2 e contagem do T30" da equipe vermelha '
      '(critério novo, mas escolhido por quem conhecia os resultados antigos). As decisões que o registro não fixa foram escritas no docstring '
      'de scripts/analisar_R27_B4.py antes de qualquer conta com votos (cópia e SHA-256 em /home/user/trabalho-eleicao/adendo27/R27_B4/). '
      'Ainda sem conferente independente.')
    P()
    P(f"Base: {mil(meta['secoes_2t'])} seções do 2º turno (Lula {mil(meta['L2'])}, Flávio {mil(meta['R2'])}, iguais ao oficial; brancos {mil(meta['B2'])}, "
      f"nulos {mil(meta['N2'])}). Universo U (definição comum do D1): {mil(meta['U'])} seções (fora {mil(meta['exterior'])} do exterior, {meta['junta']} com junta "
      f"e as com menos de 30 votos nos dois finalistas).")
    P()
    P('O QUE SE PROCURA. Uma troca feita por REGRA FIXA dentro do programa (um a cada tantos votos, fração arredondada, teto de fração, virada '
      'quando o adversário lidera na urna, ou só depois do voto de número K) deixa marca aritmética nas contagens inteiras que nenhum '
      'comportamento de eleitor produz. PONTO CEGO, dito antes e medido aqui: troca SORTEADA voto a voto não deixa dente; estes testes não a enxergam.')
    P()
    P('VEREDITOS PELA LETRA')
    a = v['D1.2a']
    P(f"1. Pente D1.2(a), votos de Flávio (R2): {a['R2']['veredito']}, com poder. Lula (L2, espelho): {a['L2']['veredito']}.", 2)
    nsb = len(a['B2']['rodadas_com_condicoes_de_sinal_e_placebo_ausente']); nsn = len(a['N2']['rodadas_com_condicoes_de_sinal_e_placebo_ausente'])
    P(f"   Brancos (B2) e nulos (N2): pela letra, {a['B2']['veredito']} e {a['N2']['veredito']} ({nsb} e {nsn} rodadas de UF com as condições numéricas e placebo ausente "
      f"no mesmo período). É ARTEFATO DEMONSTRADO do alisamento em contagens pequenas, previsto no docstring (P11) antes do dado, e não conta como "
      f"indício pelas três condições do Adendo 27 (o espelho e os placebos mostram o mesmo). Combinado pela letra: {a['combinado_pela_letra']}.", 2)
    P(f"2. Pente D4-2 (R2 e L2, país e recortes): {v['D4-2']['veredito']}, com poder.", 2)
    e = v['EV_modulo']
    P(f"3. Resíduos módulo k de 2 a 200 (equipe vermelha): R2 {e['R2']}, L2 {e['L2']}, B2 {e['B2']}, N2 {e['N2']}; combinado pela letra: {e['combinado_pela_letra']}.", 2)
    P(f"4. Paredão D1.2(b): {v['D1.2b']['veredito']}, com poder.", 2)
    P(f"5. Degrau D1.2(c): {v['D1.2c']['veredito']}, com poder; o desvio medido tem o sinal CONTRÁRIO ao da tese.", 2)
    l = v['D1.3']
    P('6. Limiar de contagem D1.3: ' + '; '.join(f"K = {K}: {l['y'][K]}" for K in ('50', '75', '100', '150', '200')) + '. K = 25 é descritivo. '
      'Com y_BN (brancos e nulos): ' + '; '.join(f"K = {K}: {l['ybn'][K]}" for K in ('50', '75', '100', '150', '200')) + '.', 2)
    P(f"7. Gatilho por contagem da equipe vermelha (conta do T30, N de 50 a 300): {v['EV_contagem']['veredito']}.", 2)
    P()
    # ---------------- 1
    P('1. PENTE D1.2(a): DENTES PERIÓDICOS NO HISTOGRAMA DAS CONTAGENS')
    P('Votos de Flávio (R2), país: ' + lz('pais|R2'), 2)
    P('Votos de Lula (L2), país: ' + lz('pais|L2'), 2)
    P('Por modelo de urna (|Z| máximo de R2 e de L2; percentil 99 do nulo perto de 5,2 em todos): ' + '; '.join(
        f"{m}: {br(R[f'modelo_{m}|R2']['maxabsZ'])} e {br(R[f'modelo_{m}|L2']['maxabsZ'])}" for m in ('UE2013', 'UE2015', 'UE2020', 'UE2022'))
      + '. Nenhum passa de 5 e todos os periodogramas ficam dentro do percentil 99 do nulo.', 2)
    ufs = sorted((o['maxabsZ'], k) for k, o in R.items() if k.startswith('uf_') and k[-2:] in ('R2', 'L2') and o.get('avaliavel'))
    nav = [k for k, o in R.items() if not o.get('avaliavel')]
    P(f"Por UF (R2 e L2): {len(ufs)} rodadas avaliáveis; a maior é {ufs[-1][1].replace('uf_', '').replace('|', ' ')} com |Z| = {br(ufs[-1][0])} "
      f"(percentil 99 do nulo dela: {br(R[ufs[-1][1]]['nulo']['maxabsZ_q99'])}); as outras ficam abaixo de 5. Com cerca de 50 rodadas, uma acima de 5 é o que o acaso dá. "
      f"Não avaliáveis por falta de seções: {', '.join(k.replace('uf_', '').replace('|', ' ') for k in nav)}.", 2)
    s = d12['sensibilidade_todas_as_secoes_do_Brasil']
    P(f"Sensibilidade com todas as seções do Brasil (sem o corte de 30 votos e com as de junta): R2 {br(s['R2']['maxabsZ'])}, L2 {br(s['L2']['maxabsZ'])}.", 2)
    pc = d12['placebos']
    P('Placebos, mesma conta (|Z| máximo): ' + '; '.join(f"{k.replace('_2t', ' 2º turno').replace('_1t', ' 1º turno').replace('|', ' ')}: {br(pc[k]['maxabsZ'])}"
                                                          for k in ('2026_1t|R1', '2026_1t|L1', '2022_2t|R2', '2022_2t|L2', '2018_2t|R2', '2018_2t|L2', '2014_2t|R2', '2014_2t|L2',
                                                                    '2026_gov2t|G1', '2026_gov2t|G2')) + '.', 2)
    P('Calibração (regra plantada nos dados de 2026; votos movidos, fração da troca necessária, |Z| e período achado):', 2)
    for k, nome in (('R_para_L_q1_k110|R2', 'um a cada 110 votos de Flávio, todas as seções'), ('R_para_L_q1_k56|R2', 'um a cada 56, todas'),
                    ('R_para_L_q1_k28|R2', 'um a cada 28, todas'), ('R_para_L_q0.25_k7|R2', 'um a cada 7, em 25% das seções'),
                    ('fracao_arredondada_Phi0.25|R2', 'fração de 0,89% arredondada'), ('fracao_arredondada_Phi0.5|R2', 'fração de 1,79% arredondada'),
                    ('fracao_arredondada_Phi1.0|R2', 'fração de 3,57% arredondada'), ('binomial_Phi1|R2', 'SORTEADA (binomial), tamanho que vira o resultado'),
                    ('espelho_L_para_R_q1_k110|L2', 'espelho: um a cada 110 votos de Lula'), ('espelho_L_para_R_q1_k28|L2', 'espelho: um a cada 28 votos de Lula')):
        o = PL[k]
        P(f"{nome}: {mil(o['votos_movidos'])} votos ({br(100 * o['Phi_efetivo'], 1)}% do necessário), |Z| = {br(o['maxabsZ'], 1)}, p = {o['maiores_Z'][0]['p']}"
          + (' (NÃO ENXERGA: ponto cego)' if not o['enxerga_Z8'] else ''), 4)
    P('A menor regra plantada (um a cada 110) move 13,8% da troca necessária e dá |Z| de 57; o limiar de sinal é 8 e o observado é 3,65. '
      'Obs.: o desenho chamava esse par de "Phi = 0,25"; com a parte inteira, o que ele move de fato é 0,138.', 2)
    P('BRANCOS E NULOS. A regressão quadrática de 21 valores da letra não acompanha histogramas tão estreitos (média de 2,9 brancos e 5,5 nulos por '
      'seção; o "liso" erra em até 50%). Resultado da letra, país: B2 ' + f"|Z| = {br(R['pais|B2']['maxabsZ'], 1)} (nulo: mediana {br(R['pais|B2']['nulo']['maxabsZ_q50'], 1)}); "
      f"N2 |Z| = {br(R['pais|N2']['maxabsZ'], 1)} (nulo: mediana {br(R['pais|N2']['nulo']['maxabsZ_q50'], 1)}). Os placebos dão o mesmo: brancos do 1º turno de 2026 "
      f"{br(pc['2026_1t|B1']['maxabsZ'], 1)}, de 2022 {br(pc['2022_2t|B2']['maxabsZ'], 1)}, de 2018 {br(pc['2018_2t|B2']['maxabsZ'], 1)}, de 2014 {br(pc['2014_2t|B2']['maxabsZ'], 1)}; "
      f"nulos {br(pc['2026_1t|N1']['maxabsZ'], 1)}, {br(pc['2022_2t|N2']['maxabsZ'], 1)}, {br(pc['2018_2t|N2']['maxabsZ'], 1)} e {br(pc['2014_2t|N2']['maxabsZ'], 1)}. "
      'No país e por modelo o pico aparece nos placebos no mesmo (p, o): INCONCLUSIVO pela letra.', 2)
    nuf = [k for k, o in R.items() if k.startswith('uf_') and k[-2:] in ('B2', 'N2') and o.get('avaliavel')]
    ncond = [k for k in nuf if R[k]['cond_Z8_com_amplitude'] or R[k]['cond_periodograma']]
    sn = v['D1.2a']['B2']['rodadas_com_condicoes_de_sinal_e_placebo_ausente'] + v['D1.2a']['N2']['rodadas_com_condicoes_de_sinal_e_placebo_ausente']
    P(f"Por UF, as condições numéricas de sinal aparecem em {len(ncond)} de {len(nuf)} rodadas de B2 e N2 (em todas), e em {len(sn)} delas o placebo da própria UF não tem "
      f"|Z| de 5 no mesmo (p, o): {', '.join(k.replace('uf_', '').replace('|', ' ') for k in sn)}. Pela letra isso é SINAL em recorte. "
      'Por que é artefato e não indício:', 2)
    P(f"(i) EXPLORATÓRIO, feito depois de ver: histogramas sorteados sem regra nenhuma (binomial por seção, gerador E2 do docstring) passam pela conta da letra e dão "
      f"|Z| mediano de {br(ex['pais|B2']['sorteios_maxabsZ_mediana'], 1)} em brancos (observado {br(ex['pais|B2']['observado_maxabsZ'], 1)}) e de "
      f"{br(ex['pais|N2']['sorteios_maxabsZ_mediana'], 1)} em nulos (observado {br(ex['pais|N2']['observado_maxabsZ'], 1)}); "
      f"{br(100 * ex['pais|B2']['fracao_dos_sorteios_com_Z8_e_amplitude'], 0)}% e {br(100 * ex['pais|N2']['fracao_dos_sorteios_com_Z8_e_amplitude'], 0)}% dos sorteios "
      f"cumprem \"Z de 8 com amplitude de 2%\". Nos votos de Flávio e de Lula os mesmos sorteios dão {br(ex['pais|R2']['sorteios_maxabsZ_mediana'], 1)} e "
      f"{br(ex['pais|L2']['sorteios_maxabsZ_mediana'], 1)} e nenhum dispara.", 4)
    exs = [ex[k] for k in sn if k in ex]
    P(f"(ii) Nas {len(exs)} rodadas de UF marcadas, os sorteios sem regra disparam em " + ', '.join(f"{br(100 * x['fracao_dos_sorteios_com_Z8_e_amplitude'], 0)}%" for x in exs)
      + ' dos casos (na ordem da lista).', 4)
    q4 = d12['quarta_diferenca']; q4r = d12['quarta_diferenca_por_recorte']
    nd = sum(len(x.get('dentes', [])) for x in q4r.values())
    P(f"(iii) Complemento declarado antes (quarta diferença do logaritmo, que não depende de curva lisa): nenhum dente em B2 nem em N2 no país "
      f"(maior |z|: {br(abs(q4['2026_2t|B2']['maior_z']['z']))} e {br(abs(q4['2026_2t|N2']['maior_z']['z']))}; limiar 8 com 2% de amplitude), e {nd} dentes nas "
      f"{len(q4r)} rodadas por recorte. As conversões determinísticas plantadas aparecem nesse complemento: um a cada 3 brancos, "
      f"{len(PL['conversao_brancos_k3|B2']['quarta_diferenca']['dentes'])} dentes ({mil(PL['conversao_brancos_k3|B2']['votos_movidos'])} votos); um a cada 3 nulos, "
      f"{len(PL['conversao_nulos_k3|N2']['quarta_diferenca']['dentes'])} ({mil(PL['conversao_nulos_k3|N2']['votos_movidos'])}); um a cada 5 nulos, "
      f"{len(PL['conversao_nulos_k5|N2']['quarta_diferenca']['dentes'])} ({mil(PL['conversao_nulos_k5|N2']['votos_movidos'])}); um a cada 10 nulos, "
      f"{len(PL['conversao_nulos_k10|N2']['quarta_diferenca']['dentes'])} ({mil(PL['conversao_nulos_k10|N2']['votos_movidos'])} votos, 1,3% da margem).", 4)
    P()
    # ---------------- 2
    nac = d42['nacional']; conj = d42['nulo_do_conjunto_de_recortes']
    P('2. PENTE D4-2 (segunda diferença e periodograma em 3 harmônicos, períodos de 8 a 150)')
    P(f"R2 nacional (todas as seções, exterior incluído): Z = {br(nac['R2']['Z'], 1)} (nulo: mediana {br(nac['R2']['nulo']['q50'], 1)}, percentil 99 "
      f"{br(nac['R2']['nulo']['q99'], 1)}, maior {br(nac['R2']['nulo']['max'], 1)}; limiar de sinal {br(1.5 * nac['R2']['nulo']['max'], 1)}). L2 nacional: Z = "
      f"{br(nac['L2']['Z'], 1)} (percentil 99 {br(nac['L2']['nulo']['q99'], 1)}; limiar {br(1.5 * nac['L2']['nulo']['max'], 1)}). Maior dos 17 placebos: "
      f"{br(d42['maior_placebo'], 1)} (L do 2º turno de 2014). Os dois ficam abaixo da mediana ou perto dela.", 2)
    recs = sorted(((o['Z'], k) for k, o in d42['recortes'].items() if o.get('Z') is not None), reverse=True)
    P(f"Recortes: {len(recs)} avaliáveis (3 faixas de tamanho e as UFs grandes); o maior é {recs[0][1].replace('uf_', '').replace('|', ' ')} com {br(recs[0][0], 1)}, contra "
      f"percentil 99 do conjunto de {br(conj['q99'], 1)} e limiar de sinal de {br(conj['limiar_de_sinal'], 1)}. {v['D4-2']['recortes_nao_avaliaveis']} recortes (UFs "
      f"menores e exterior) não têm casas com 300 seções e não são avaliáveis por este teste; neles vale o D1.2(a) por UF.", 2)
    p26 = d42['plantios']['R2_2026']
    P('Calibração em R2 de 2026 (Z; enxerga se passar de ' + br(1.5 * nac['R2']['nulo']['max'], 1) + '): ' + '; '.join(
        f"{k.replace('_das_secoes', '').replace('_em_', ' em ').replace('piso_', 'piso de ').replace('0.0357', '3,57%').replace('0.018', '1,8%').replace('0.01', '1%').replace('1.0', 'todas').replace('0.5', '50%').replace('0.2', '20%').replace('0.1', '10%')}: "
        f"{br(o['Z'], 0)}{'' if o['enxerga'] else ' (não vê)'}" for k, o in p26.items()) + '. Os mesmos plantios em R1 de 2026 e em R2 de 2022 dão números '
      'parecidos (no JSON). Isso reproduz no dado real o que o desenhista mediu em dado sintético.', 2)
    P('Exclui, pela calibração: troca por parte inteira de 1% ou mais dos votos de Flávio em todas as seções (16% da troca necessária), de 1,8% em metade '
      '(19%) e de 3,57% em 20% delas (17%). Não exclui troca sorteada nem troca calculada sobre o comparecimento (cego por construção).', 2)
    bn = d42['brancos_e_nulos_de_comparacao']
    P(f"B2 e N2 (descritivo; o critério do D4-2 é sobre R2 e L2): Z = {br(nac['B2']['Z'], 0)} e {br(nac['N2']['Z'], 0)}, o mesmo artefato de contagem pequena; "
      f"os brancos e nulos do 1º turno dão {br(bn['2026 B1']['Z'], 0)} e {br(bn['2026 N1']['Z'], 0)}, os de 2022 {br(bn['2022 B2']['Z'], 0)} e {br(bn['2022 N2']['Z'], 0)} "
      f"(acrescentado depois de ver).", 2)
    P()
    # ---------------- 3
    P('3. RESÍDUOS MÓDULO k (EQUIPE VERMELHA), k DE 2 A 200, CONTRA 200 SORTEIOS BINOMIAIS')
    for X, nome in (('R2', 'Flávio'), ('L2', 'Lula'), ('B2', 'brancos'), ('N2', 'nulos')):
        o = ev[X]; o1 = ev[X[0] + '1']
        P(f"{nome}: maior estatística {br(o['maxT'])} (k = {o['k_do_max']}, classe {o['classe_do_max']}, excesso {br(100 * o['excesso_corrigido_no_max'], 1)}%, p depois de "
          f"Bonferroni {br(o['p_bonferroni_no_max'], 4)}); sorteios: mediana {br(o['sorteios_maxT_q50'])}, percentil 99 {br(o['sorteios_maxT_q99'])}. "
          f"k com as duas condições de sinal: {len(o['k_com_condicoes_de_sinal'])}. 1º turno: {br(o1['maxT'])} (percentil 99 {br(o1['sorteios_maxT_q99'])}; "
          f"k com as duas condições: {len(o1['k_com_condicoes_de_sinal'])}).", 2)
    pp = ev['R2']['plantado_um_a_cada_28']
    P(f"Plantado \"um a cada 28 votos de Flávio\": z = {br(pp['zc_k27_classe0'], 1)} na classe 0 de k = 27, excesso de {br(100 * pp['excesso_corrigido_k27_classe0'], 0)}% "
      f"(exigido: acima de 20). Espelho em Lula: {br(ev['L2']['plantado_um_a_cada_28']['zc_k27_classe0'], 1)}.", 2)
    P('Leitura: em Flávio, Lula e brancos a estatística fica abaixo do percentil 99 dos sorteios. Em nulos passa (5,23 contra 3,54), sem chegar às '
      'condições de sinal (excesso de 2,8% contra 3%; p de 0,0006 contra 0,000001). Não é dente: a classe é a que contém v = 5, e o mesmo acontece no 1º '
      'turno em nulos e, mais forte, em brancos (193 valores de k com as duas condições no 1º turno, zero no 2º). É a referência que não reproduz a forma '
      'exata de contagens tão pequenas (ela iguala média e variância, não a curva). Pela letra, INCONCLUSIVO em nulos.', 2)
    P()
    # ---------------- 4
    p = par['2026_2t']
    P('4. PAREDÃO D1.2(b): TETO OU PISO NA FRAÇÃO DE LULA')
    P(f"{mil(p['secoes_V150'])} seções com 150 votos ou mais nos dois finalistas, {p['faixas_que_decidem']} faixas de 0,1 ponto que decidem. Maior z: {br(p['maior_z']['z'])} "
      f"(faixa {br(p['maior_z']['faixa_pp'], 1)}%; {p['maior_z']['observado']} contra {br(p['maior_z']['esperado'], 0)}); menor: {br(p['menor_z']['z'])} "
      f"(faixa {br(p['menor_z']['faixa_pp'], 1)}%). Nenhuma faixa com |z| de 6 ou mais fora dos picos naturais. Nos picos naturais, o maior |z| é "
      f"{br(p['picos_naturais']['maior_absz'])}, na faixa de 100% (seções com todos os votos em Lula), e o empate (50,0%) tem {p['picos_naturais']['observado_em_50']} "
      f"seções contra {br(p['picos_naturais']['esperado_em_50'], 0)} esperadas.", 2)
    P('Placebos (maior e menor z): ' + '; '.join(f"{k.replace('_2t', ' 2º turno').replace('_1t', ' 1º turno')}: {br(o['maior_z']['z'])} e {br(o['menor_z']['z'])}"
                                                  for k, o in par['placebos'].items()) + '. Nenhum com |z| de 6 fora dos picos.', 2)
    P(f"Caudas, valor bruto (seções com 150 votos ou mais): Lula abaixo de 5% em {p['cauda_y_abaixo_de_5']} seções e acima de 95% em {mil(p['cauda_y_acima_de_95'])}. "
      + 'Outros anos: ' + '; '.join(f"{k.replace('_2t', ' 2º turno').replace('_1t', ' 1º turno')}: {o['cauda_y_abaixo_de_5']} e {mil(o['cauda_y_acima_de_95'])}"
                                    for k, o in par['placebos'].items())
      + '. A cauda de Lula acima de 95% é MENOR em 2026 que em 2022, 2018 e 2014.', 2)
    cm = par['caudas_modelo_base_local']; cu = par['caudas_modelo_efeito_fixo_de_UF']
    P(f"Contra o modelo base (efeito fixo de local): abaixo de 5%, {cm['observado_abaixo_de_5']} observadas e {br(cm['previsto_abaixo_de_5'], 1)} previstas; acima de 95%, "
      f"{cm['observado_acima_de_95']} e {br(cm['previsto_acima_de_95'], 0)} (razão {br(cm['razao_acima'])}). Com efeito fixo de UF: {cu['observado_abaixo_de_5']} e "
      f"{br(cu['previsto_abaixo_de_5'], 1)}; {mil(cu['observado_acima_de_95'])} e {mil(cu['previsto_acima_de_95'])} (razão {br(cu['razao_acima'])}). Nenhuma cauda vazia; a "
      'previsão é larga demais porque o resíduo do modelo é menor que o ruído binomial (o eleitor do 2º turno é o mesmo do 1º) e a simulação usa o binomial.', 2)
    pl = par['plantios']; tr = par['votos_que_um_teto_moveria']
    P(f"Calibração: teto de 85% para Flávio plantado em todas as seções ({mil(pl['teto_85_para_Flavio_em_todas']['votos_movidos'])} votos em "
      f"{mil(pl['teto_85_para_Flavio_em_todas']['secoes_alteradas'])} seções): z = {br(pl['teto_85_para_Flavio_em_todas']['maior_z']['z'], 1)}; em 20% das seções "
      f"({mil(pl['teto_85_para_Flavio_em_20pct']['votos_movidos'])} votos): z = {br(pl['teto_85_para_Flavio_em_20pct']['maior_z']['z'], 1)}. Espelho (teto de 85% para Lula, "
      f"{mil(pl['espelho_teto_85_para_Lula_em_todas']['votos_movidos'])} votos): z = {br(pl['espelho_teto_85_para_Lula_em_todas']['maior_z']['z'], 1)}.", 2)
    P('Tradução: votos que um teto para Flávio moveria nos dados de 2026: ' + '; '.join(
        f"teto de {c}%: {mil(tr[c]['teto_para_Flavio_votos'])} ({br(100 * tr[c]['fracao_da_margem'], 1)}% do necessário)" for c in ('95', '90', '85', '80', '70'))
      + '. Para pesar na margem o teto teria de ficar em 70% ou menos, e ali há ' + mil(tr['70']['secoes']) + ' seções acima dele: seria um paredão impossível de não ver.', 2)
    P()
    # ---------------- 5
    g = deg['2026_2t']
    P('5. DEGRAU D1.2(c): VIRADA CONDICIONADA AO PLACAR DA URNA')
    P(f"Seções com Lula de 1 a 10 votos à frente: {mil(g['massa_D_1_a_10'])}; com Flávio de 1 a 10 à frente: {mil(g['massa_D_-10_a_-1'])}. Log da razão: {br(g['log_razao_bruta'], 4)} "
      f"(previsto pelo polinômio: {br(g['log_razao_prevista'], 4)}). S = {br(g['S'], 4)} (ep {br(g['ep'], 4)}, z = {br(g['z'])}). Empates: {g['h0']} contra "
      f"{br(g['h0_previsto'], 0)} previstos (z = {br(g['z_h0'])}).", 2)
    P('Limiares: sinal com |S| de 0,05 e z de 5; sem sinal com |S| abaixo de 0,02. O valor fica entre os dois: INCONCLUSIVO. O sinal é NEGATIVO: faltam seções com '
      'Lula pouco à frente, o contrário do que uma virada a favor de Lula produziria. Placebos (S e z): ' + '; '.join(
          f"{k.replace('_2t', ' 2º turno').replace('_1t', ' 1º turno').replace('_G1_menos_G2', '').replace('_gov2t', ' governador')}: {br(o['S'], 4)} ({br(o['z'])})"
          for k, o in deg['placebos'].items()) + '. O 1º turno de 2026 tem quase o mesmo desvio, o que aponta para o ajuste do polinômio e não para o 2º turno.', 2)
    dp = deg['plantios']
    P(f"Calibração: virar {mil(dp['R_para_L_q0.025']['secoes_alteradas'])} seções (2,5% das que têm Flávio pouco à frente, {mil(dp['R_para_L_q0.025']['votos_movidos'])} votos) "
      f"move S em {br(dp['R_para_L_q0.025']['deslocamento_de_S'], 4)} ({br(dp['R_para_L_q0.025']['deslocamento_em_erros'], 1)} erros); o espelho move "
      f"{br(dp['espelho_L_para_R_q0.025']['deslocamento_de_S'], 4)}. Tradução: o S medido, lido inteiro como virada, valeria cerca de "
      f"{mil(abs(g['S']) * deg['traducao']['votos_por_unidade_de_S'])} votos trocados, e a favor de Flávio. Degrau em zero não explica margem nacional.", 2)
    P()
    # ---------------- 6
    P('6. LIMIAR DE CONTAGEM D1.3: A URNA QUE SÓ AGE DEPOIS DO VOTO DE NÚMERO K')
    am = lim['amostra_2026']
    P(f"Modelo base da letra (efeito fixo de local, {len(am['X'])} controles, peso V, erro por município): {mil(am['na_regressao'])} seções em {mil(am['locais'])} locais e "
      f"{mil(am['municipios'])} municípios. 2022: {mil(lim['amostra_2022']['na_regressao'])} seções. Erro do estimador principal por 500 reamostragens de municípios.", 2)
    P('K | seções até K | b 2026 (ep) | b 2022 (ep) | diferença (ep) z | Phi da diferença [IC 99%] | Phi só com 2026 [IC 99%] | joelho 2026 z | regiões', 2)
    for K in ('25', '50', '75', '100', '150', '200'):
        o = lim['principal']['y'][K]
        P(f"{K} | {mil(lim['secoes_de_U_com_comparecimento_ate_K'][K])} | {br(o['b_2026'], 3)} ({br(o['ep_2026_cr1'], 3)}) | {br(o['b_2022'], 3)} ({br(o['ep_2022_cr1'], 3)}) | "
          f"{br(o['diferenca'], 3)} ({br(o['ep_bootstrap'], 3)}) {br(o['z'])} | {br(o['Phi_diferenca'], 3)} [{br(o['Phi_ic99'][0], 3)}; {br(o['Phi_ic99'][1], 3)}] | "
          f"{br(o['Phi_so_2026'], 3)} [{br(o['Phi_so_2026_ic99'][0], 3)}; {br(o['Phi_so_2026_ic99'][1], 3)}] | {br(o['joelho_2026']['z'])} | {o['regioes_no_sentido_da_nacional']} de 5", 2)
    P('Nenhum K chega perto do sinal (z de 3,9; o maior é 1,74). Mas o intervalo só cabe no limite de sem sinal em K = 200. O erro é 5 a 8 vezes o que o desenho '
      'previa (0,06 a 0,10 ponto), porque o modelo base da letra já tem o logaritmo dos aptos e as duas abstenções, que juntos quase determinam o '
      'comparecimento: sobra pouca variação da dose.', 2)
    cal = lim['calibracao']
    P('Calibração (taxa plantada f x D_K; fração das 200 cópias detectadas com z de 3,9), Phi = 0,25 | 0,5 | 1: ' + '; '.join(
        f"K = {K}: {br(100 * cal[K]['Phi_0.25']['deteccao_z_3_9'], 0)}% | {br(100 * cal[K]['Phi_0.5']['deteccao_z_3_9'], 0)}% | {br(100 * cal[K]['Phi_1.0']['deteccao_z_3_9'], 0)}%"
        for K in ('50', '75', '100', '150', '200')) + f". Recuperação do coeficiente plantado: de {br(min(cal[K]['Phi_1.0']['recuperacao'] for K in cal))} a "
      f"{br(max(cal[K]['Phi_1.0']['recuperacao'] for K in cal))}. O registro exige 95% em Phi = 0,25: só K = 200 cumpre. Espelho (plantio a favor de Flávio, Phi = 0,25): "
      + '; '.join(f"K = {K}: {br(100 * cal[K]['espelho_Phi_0.25']['deteccao_z_3_9'], 0)}%" for K in ('50', '75', '100', '150', '200')) + '.', 2)
    ino = lim['explicacao_inocente_plantada']['Phi_0.5']
    P('Explicação inocente plantada (seção pequena diferente, dose suave sem joelho, tamanho de Phi = 0,5): o estimador principal se move ' + '; '.join(
        f"K = {K}: {br(ino[K]['principal_deslocamento_em_erros'], 1)} erros (Phi aparente {br(ino[K]['principal_Phi_aparente'])}), joelho {br(ino[K]['joelho_deslocamento_em_erros'], 1)}"
        for K in ('50', '100', '150', '200')) + '. Ou seja: uma inclinação suave do tamanho de meia margem também apareceria no estimador principal, e é o joelho que a separa.', 2)
    P('Placebo de 2018, que mostra quanto o estimador muda sozinho de uma eleição para outra (Phi de 2022 menos 2018 | de 2026 menos 2018): ' + '; '.join(
        f"K = {K}: {br(lim['principal']['y'][K]['placebo_2018']['Phi_2022_menos_2018'])} | {br(lim['principal']['y'][K]['placebo_2018']['Phi_2026_menos_2018'])}"
        for K in ('50', '75', '100', '150', '200')) + '. O coeficiente vem subindo de eleição em eleição (K = 50: ' +
      f"{br(lim['principal']['y']['50']['placebo_2018']['b_2018'])} em 2018, {br(lim['principal']['y']['50']['b_2022'])} em 2022, {br(lim['principal']['y']['50']['b_2026'])} em 2026).", 2)
    gv = lim['placebo_governador']['resumo']; p1 = lim['placebo_1t_2026_contra_2022']
    P('Outros placebos: governador do 2º turno nas 6 UFs, qui-quadrado dos 6 z (6 graus de liberdade): ' + '; '.join(f"K = {K}: {br(gv[K]['qui2_dos_6_z'], 1)}" for K in ('50', '100', '150', '200'))
      + '. 1º turno de 2026 contra 2022 com a dose do 1º turno (b, z, Phi equivalente): ' + '; '.join(
          f"K = {K}: {br(p1[K]['b'], 3)}, {br(p1[K]['z'])}, {br(p1[K]['Phi_equivalente'], 3)}" for K in ('50', '100', '150', '200')) + '.', 2)
    sp = lim['sensibilidade_sem_perfil']
    P('Sensibilidade, as duas regressões sem o perfil do eleitorado (Phi da diferença, ep): ' + '; '.join(f"K = {K}: {br(sp[K]['Phi'], 3)} ({br(sp[K]['ep_Phi'], 3)})" for K in ('50', '75', '100', '150', '200')) + '.', 2)
    P('y_BN (brancos e nulos; Phi positivo = caem com a dose, sentido da conversão), Phi da diferença [IC 99%]: ' + '; '.join(
        f"K = {K}: {br(lim['principal']['ybn'][K]['Phi_diferenca'], 3)} [{br(lim['principal']['ybn'][K]['Phi_ic99'][0], 3)}; {br(lim['principal']['ybn'][K]['Phi_ic99'][1], 3)}]"
        for K in ('50', '75', '100', '150', '200')) + '. Detecção do plantio de Phi = 0,25: ' + '; '.join(
          f"K = {K}: {br(100 * cal[K]['ybn_Phi_0.25']['deteccao_z_3_9'], 0)}%" for K in ('50', '75', '100', '150', '200')) + '.', 2)
    tab = lim['residuo_por_faixa_de_comparecimento']
    P('Resíduo médio do modelo base por faixa de comparecimento (pontos de fração de Lula; 2026 | 2022), no lugar da figura: ' + '; '.join(
        f"{int(t['comp_de']) + 1} a {int(min(t['comp_ate'], 9999))}: {br(t['residuo_2026'], 3)} | {br(t['residuo_2022'], 3)}" for t in tab[:6]) + ' ... (as 25 faixas estão no JSON).', 2)
    P()
    # ---------------- 7
    c = lim['EV_contagem']['cortes']
    P('7. GATILHO POR CONTAGEM DA EQUIPE VERMELHA (conta do T30 no bweb inteiro, com ln do tamanho)')
    P('Coeficiente em pontos por unidade da fração de votantes além de N (ep) | o mesmo em 2022: ' + '; '.join(
        f"N = {N}: {br(c[N]['coef'])} ({br(c[N]['ep'])}) | {br(c[N]['coef_2022'])}" for N in c) + '.', 2)
    cc = lim['EV_contagem']['calibracao']
    P(f"Limiares do T30: sinal com 4 pontos e z de 3,32 (11 cortes), ausente em 2022; sem sinal com até 1,5 ponto em módulo. Calibração: o plantio de Phi = 1 com K = 100 "
      f"move o coeficiente de N = 100 em {br(cc['K100_Phi1.0']['100']['deslocamento'])} ponto ({br(cc['K100_Phi1.0']['100']['em_erros'], 1)} erros) e o de K = 200 move o de "
      f"N = 200 em {br(cc['K200_Phi1.0']['200']['deslocamento'])} ({br(cc['K200_Phi1.0']['200']['em_erros'], 1)} erros). O limiar de 4 pontos do T30 corresponde a mais do que a "
      f"margem inteira nos cortes baixos; o que decide é o erro. Sem o ln do tamanho (conta original do T30), N = 100: {br(c['100']['sem_ln_coef'])} em 2026 e "
      f"{br(c['100']['sem_ln_coef_2022'])} em 2022.", 2)
    P()
    return T, v


if __name__ == '__main__':
    modo = sys.argv[1] if len(sys.argv) > 1 else ''
    f = globals().get('modo_' + modo)
    if not f:
        sys.exit('modos: perfil gov2t base pente paredao degrau limiar relatorio')
    f()
