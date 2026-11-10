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
            secs += [s.strip() for s in ag.replace(';', ',').split(',') if s.strip()]
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
        if self.n < 10:
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
            amp = float((self.h[self.vs[m]] - self.s[self.vs[m]]).sum() / self.s[self.vs[m]].sum())
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
    if pt.n < 10:
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


if __name__ == '__main__':
    modo = sys.argv[1] if len(sys.argv) > 1 else ''
    f = globals().get('modo_' + modo)
    if not f:
        sys.exit('modos: perfil gov2t base pente paredao degrau limiar relatorio')
    f()
