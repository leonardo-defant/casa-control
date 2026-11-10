#!/usr/bin/env python3
"""R27_B6: VIZINHO DE SALA E CAUDAS (Adendo 27, Onda B, item B6; última onda do Adendo 30).

Três partes:
  A. Teste D4-5 de registro/adendo27/desenho_D4_proposta.json, por inteiro (dispersão da passagem entre turnos
     dentro do mesmo local de votação: a troca aplicada só a parte das urnas).
  B. Fragilidade "F5 (caudas)" de registro/adendo27/equipe_vermelha_relatorio.json (z dividido pelo desvio robusto
     por faixa de tamanho, previsão deixando a seção de fora, calibrado plantando +5 pontos em 1.000 seções de
     10 zonas).
  C. Descritivo, sem veredito: a suspeita de "linearidade" do Léo (a virada parecida demais em toda parte).

Critérios: commit 2748895 (10/11/2026 00:16:42 UTC), aplicados pela letra, sem mudar limiar. Este docstring foi
escrito ANTES de calcular qualquer resultado com votos; cópia com data e SHA-256 em
/home/user/trabalho-eleicao/adendo27/R27_B6/docstring_antes_de_rodar.txt. O desenho D4-5 é cego. O reteste do F5
foi escrito pela equipe vermelha, que já conhecia o resultado antigo (13 contra 57 pela letra, 160 contra 313 no
exploratório): o critério é novo, a escolha do que retestar é posterior ao dado. A parte C não tem critério
registrado: o que se lê como marca está escrito abaixo, antes de rodar.

Uso (sempre com python3 -I):
  python3 -I scripts/analisar_R27_B6.py perfil   extrai o perfil do eleitorado por seção (sem votos)
  python3 -I scripts/analisar_R27_B6.py gov2t    extrai governador do 2º turno por candidato (6 UFs)
  python3 -I scripts/analisar_R27_B6.py A | B | C   roda uma parte e grava o parcial em TRAB
  python3 -I scripts/analisar_R27_B6.py final    junta os parciais em resultados/R27_B6_vizinho_de_sala_e_caudas.json e .txt

=====================================================================================================
PARTE A. D4-5, O QUE O REGISTRO FIXA (aplicado como está escrito)
- Universo: o do D4-1 (seções apuradas nos dois turnos, diferença de aptos entre turnos de no máximo 2,
  comparecimento do 1º turno de pelo menos 30, fora do exterior, locais com 2 ou mais seções válidas),
  restrito a locais com 4 ou mais seções.
- Resíduo e da equação de L2 do D4-1: efeito fixo de local, peso 1/aptos, regressoras do 1º turno em número
  de eleitores (L1, R1, eliminados somados, B1, N1, A1 = aptos menos comparecimento).
- Variância de referência de cada seção: v = soma de X_j b_j (1 - b_j), com b truncado entre 0 e 1.
- phi = média de e ao quadrado sobre v, com correção de graus de liberdade por local (k/(k-1)).
- Primária: phi de 2026 dividido pelo maior phi dos anos placebo (2014, 2018, 2022).
- Secundárias: fração de seções com e/raiz(v phi_ref) acima de 3 e abaixo de -3, phi_ref = mediana dos anos
  placebo; mistura de duas normais no resíduo padronizado (fração pi e separação delta) e votos implicados =
  pi vezes delta vezes o total de válidos das seções; phi por UF.
- SINAL: phi de 2026 >= 1,5 vez o maior phi placebo; E (cauda de um lado >= 3 vezes a do outro, OU mistura com
  separação >= 2 pontos percentuais dos válidos e fração entre 5% e 95%); E votos implicados pela mistura >= 550 mil.
- SEM SINAL: phi de 2026 <= 1,15 vez o maior phi placebo E razão entre caudas entre 0,67 e 1,5.
- INCONCLUSIVO: razão entre 1,15 e 1,5, ou phi dos anos placebo variando mais de 1,5 vez entre si.
- Poder (no dado real): plantar as mesmas trocas do sintético (dose inteira de 3,57% dos votos de R em 10%, 30%,
  50%, 70%, 90% e 100% das urnas; meia dose em 30% e 50%) em 2022 e conferir a razão.
- Placebo: a mesma conta em 2014, 2018 e 2022; placebo contemporâneo: a mesma conta para governador nas 6 UFs
  com 2º turno, mesmas urnas.

PARTE A. DECISÕES QUE O REGISTRO NÃO FIXA (tomadas aqui, antes de qualquer conta com votos; saem como desvios)
A1. Universo do D4-1 pelas mesmas decisões do script da A2 (R27_A2, D1 a D4): "apurada" = campo tipo igual a
    APURADA sem diferenciar maiúsculas, nos dois turnos; local = UF, município, zona e número do local
    (lib.chave_local, com o local do 1º turno); A1 = aptos do 1º menos comparecimento do 1º; A2 = aptos do 2º
    menos comparecimento do 2º; peso = 1/aptos do 1º turno. "Local com 4 ou mais seções" = 4 ou mais seções
    válidas, contadas depois de todos os outros filtros. O campo "dados" do desenho cita DS_SECOES_AGREGADAS
    "para excluir seções agregadas", mas o campo "estatistica" (que é o que vale) não exclui, e as bases de
    2014, 2018 e 2022 não têm essa marca. Principal: SEM excluir, nos quatro anos. Ao lado: 2026 sem as agregadas.
A2. A regressão é refeita dentro do universo restrito (locais com 4 ou mais), com as quatro respostas do D4-1
    (L2, R2, BN2, A2) e as regressoras L1, R1, O1 (todos os eliminados somados; em 2026 o 28 anulado está em
    O), B1, N1, A1. Mesma especificação nos quatro anos. Ao lado, só em 2026: eliminados separados (um termo
    para cada um com 0,5% ou mais dos válidos nacionais: Cury 70, Renan 14, Caiado 55; os demais somados).
A3. e = resíduo da regressão com efeito fixo (transformação within com o peso), em número de votos. v usa os
    coeficientes da própria equação e as contagens do 1º turno da seção. Seção com v <= 0 fica fora (contada).
A4. phi = média, nas seções, de (e ao quadrado / v) vezes k/(k-1), k = seções válidas do local. Ao lado, sem
    entrar no critério: razão das somas (soma de e2 k/(k-1) sobre soma de v) e versão robusta (mediana de
    e2 k/(k-1)/v dividida por 0,4549, a mediana de um qui-quadrado com 1 grau).
A5. Erro: bootstrap de municípios (500 réplicas, semente 20261110 + ano), com os coeficientes fixos. Para a razão
    de 2026 sobre o maior placebo, as quatro réplicas são independentes; intervalo percentil de 2,5% a 97,5%.
A6. phi_ref = mediana dos três phi placebo (o do meio). u = e / raiz(v phi_ref), sem a correção k/(k-1) (letra).
    Cauda direita = fração com u > 3 (Lula acima do previsto); esquerda = fração com u < -3 (Lula abaixo).
    "Razão entre caudas" = direita / esquerda. Cláusula de sinal: razão >= 3 ou <= 1/3 (a letra diz "de um
    lado"); o lado é relatado, e só o lado direito é o sentido da tese. Cláusula de sem sinal: 0,67 a 1,5.
A7. Mistura: máxima verossimilhança (EM) de duas normais com VARIÂNCIA COMUM em u (o modelo da hipótese: dois
    grupos de urnas com o mesmo ruído, separados por delta); para ser rápido, u é agrupado em classes de
    0,02 entre -12 e 12, com os valores além disso mantidos um a um; 7 pontos de partida, fica o de maior
    verossimilhança. Componente "alto" = o de média maior; pi = peso do alto (as urnas que teriam recebido a
    troca a favor de Lula); delta_u = diferença das médias. Conversão para pontos dos válidos: delta_pp =
    delta_u vezes soma de raiz(v phi_ref) sobre soma dos válidos (L2 + R2) das seções do universo; votos
    implicados = pi vezes delta_pp vezes o total de válidos do universo = pi vezes delta_u vezes soma de
    raiz(v phi_ref). O critério usa esse número (o do universo do teste); ao lado, o espelho ((1 - pi) no lugar
    de pi: a troca a favor de Flávio) e a extrapolação para os válidos do país. Ao lado: mistura com variâncias
    livres (piso de 0,05 no desvio).
A8. Ordem do veredito pela letra: SINAL se as três cláusulas do sinal valerem; senão INCONCLUSIVO se os phi placebo
    variarem mais de 1,5 vez entre si (máximo sobre mínimo); senão SEM SINAL se as duas cláusulas valerem; senão
    INCONCLUSIVO. Razão muito abaixo de 1 (2026 menos disperso que os outros anos) não tem nome no registro:
    pela letra é SEM SINAL quanto à troca em parte das urnas, e a pergunta "regular demais" vai para a parte C.
A9. SEM PODER (regra obrigatória da tarefa). Cenário de referência: dose inteira (3,57% dos votos de Flávio do
    universo) concentrada em 30% das urnas, plantada POR CIMA de 2026. O teste "enxerga" um cenário se, com ele
    plantado, o phi de 2026 sobe 15% ou mais (fator >= 1,15, o mesmo passo que o critério usa). Veredito SEM PODER
    se o fator do cenário de referência ficar abaixo de 1,15, OU se o veredito bruto for SEM SINAL e o veredito
    pela letra com o cenário de referência plantado continuar SEM SINAL (a régua dos outros anos absolveria a
    própria fraude plantada). Em qualquer outro caso vale o veredito pela letra, com a lista do que o teste
    enxerga e do que não enxerga.
A10. Plantio (calibração da irregularidade): em cada cenário, sorteio de uma fração f das seções do universo;
    nelas, votos movidos = binomial(R2, p f_tot), com f_tot = soma de R2 / soma de R2 nas sorteadas (mesmo total
    que a dose p em todas); tirados de R2 e somados a L2; regressão, v e phi refeitos com o dado plantado.
    Cenários por cima de 2026: doses 1, 1/2 e 1/4 de 3,57% em 10%, 30%, 50%, 70% e 90% das urnas, e dose inteira
    em todas. Por cima de 2022 (letra do desenho): os 8 cenários do sintético. Semente 20261110 + índice.
    O cenário de referência é repetido com 5 sementes para medir a variação do sorteio.
A11. Plantio da explicação inocente (por cima de 2026, dois mecanismos, os dois com o mesmo número de votos que a
    dose inteira põe em Lula, 3,57% da soma de R2 do universo):
    (I1) mobilização desigual entre seções: em 30% das seções sorteadas, uma fração dos faltosos do 2º turno
         (A2) vira votante, 2/3 para Lula e 1/3 para Flávio (a proporção medida na Onda A); nada sai de Flávio.
    (I2) conversão dos eliminados dependente do perfil da seção: em toda seção com perfil, desloca-se entre
         Flávio e Lula um número de votos proporcional a O1 vezes (parcela de 60 anos ou mais da seção menos a
         média do local ponderada pelos aptos), com sinal, arredondado por sorteio, com fator tal que a soma dos
         valores absolutos dê a dose. É troca de destino de eleitor de eliminado, zero em média dentro do local.
    O que se mede em cada um: se phi sobe como na troca; se as caudas e a mistura se distinguem; quanto a
    variante com covariáveis de perfil absorve; e a "parcela espelhada" (A12).
A12. Espelho e controles, escritos antes de ver qualquer número:
    (a) a razão entre caudas já é o espelho (direita: Lula acima; esquerda: Flávio acima);
    (b) phi das outras três equações (R2, BN2, A2) nos quatro anos, cada uma com a sua variância de referência;
        uma troca entre os finalistas não mexe em branco, nulo nem abstenção: se a razão 2026 sobre placebo subir
        igual em A2 ou BN2, a dispersão a mais não é de troca;
    (c) "parcela espelhada": c_LR = média de e_L e_R k/(k-1) / v_L (e o mesmo com e_BN e e_A). Como as quatro
        respostas somam os aptos, phi_L é aproximadamente -(c_LR + c_LBN + c_LA). Parcela espelhada em Flávio =
        -c_LR/phi_L; em abstenção = -c_LA/phi_L; em branco e nulo = -c_LBN/phi_L. A troca plantada só aumenta a
        primeira. Estatística complementar "phi de troca" = -c_LR, com a mesma razão 2026 sobre o maior placebo.
        Não é do registro e não muda o veredito; serve para dizer de que tipo é a dispersão;
    (d) plantio espelho: o cenário de referência no sentido contrário (de L2 para R2, mesmo número de votos):
        phi deve subir o mesmo e a razão entre caudas deve inverter.
A13. Variantes ao lado (não entram no veredito): (v1) 2026 sem seções agregadas; (v2) 2026 com eliminados
    separados; (v3) 2026 com as covariáveis de perfil do D4-1 (parcelas de 16 a 24 anos, 60 anos ou mais, superior
    completo e mulheres, cada uma vezes os aptos do 1º turno; seções sem perfil fora), com o mesmo universo sem
    as covariáveis para comparar; (v4) coeficientes próprios de cada UF (regressão dentro da UF) nos quatro anos;
    (v5) universo do D4-1 inteiro (locais com 2 ou mais) nos quatro anos.
A14. Placebo contemporâneo (governador, AC, AM, DF, ES, RN e TO): dentro de cada UF, L = finalista que venceu o
    2º turno de governador na UF, R = o outro (lidos do bweb do 2º turno); regressoras = votos dos dois no 1º
    turno, demais nominais somados, branco e nulo do cargo, A1 da seção; resposta = L do 2º turno; mesmo
    universo (filtros do D4-1, locais com 4 ou mais seções válidas dentro da UF). phi do governador por UF e nas
    6 juntas (média nas seções). Ao lado, phi presidencial nas mesmas seções, com regressão dentro da UF.
    Leitura escrita antes: é a régua que não depende de outro ano. phi presidencial de 1,5 vez ou mais o do
    governador nas mesmas urnas iria no sentido da tese (troca só no cargo de presidente); 1,15 vez ou menos,
    não. Não muda o veredito pela letra.
A15. Tradução em votos de margem: (i) votos implicados pela mistura (A7), vezes 2 = margem; (ii) teto lido
    inteiro a favor da tese: para cada fração f de urnas, a maior dose cuja dispersão caberia na folga
    phi de 2026 menos uma base, com a subida de phi medida no plantio (ajuste delta_phi = a d + c d2 pelas três
    doses plantadas, a e c não negativos). Bases: 1 (só o acaso binomial das transições; nada do que há de
    dispersão natural é descontado), o menor, o mediano e o maior phi placebo. Votos movidos = p/(1-p) vezes
    59.826.041; margem = 2 vezes isso, sobre 4.430.191. O teto com base 1 é a leitura mais favorável à tese e
    não é estimativa; o registro já avisa que troca igual em todas as urnas não é assunto deste teste.
A16. O valor bruto de 2026 aparece sempre ao lado de qualquer comparação com outro ano. O veredito pela letra
    depende só da comparação com 2014, 2018 e 2022 (anos de que o Léo também suspeita); isso é dito no veredito,
    com as réguas internas ao lado (binomial, governador nas mesmas urnas, parcela espelhada, covariáveis).

=====================================================================================================
PARTE B. F5 (CAUDAS), O QUE O REGISTRO FIXA
- Adendo 20: previsão pela regressão do T8 com efeito fixo de local (ganho de Lula e de Flávio contra os votos do
  1º turno da seção); z = (fatia observada - p) / raiz(p(1-p)/n), n = votos dos finalistas no 2º turno.
- Equipe vermelha (Adendo 27): principal = z dividido pelo desvio robusto por faixa de tamanho, com previsão
  deixando a seção de fora; calibrar plantando +5 pontos em 1.000 seções de 10 zonas.
- SINAL: seções com z recalibrado > +4 em número de pelo menos 1,3 vez as com < -4, com 200 ou mais acima de +4, e
  30% ou mais das de cima em até 10 zonas, exigindo que o caso plantado seja detectado.
- SEM SINAL: razão de 0,8 a 1,25, ou abaixo de 0,8 (dito "desvio para Flávio").

PARTE B. DECISÕES QUE O REGISTRO NÃO FIXA
B1. Base e regressão: as do F5 original (scripts/analisar_F5.py): as 499.205 seções com os dois turnos, exterior
    incluído; y = L2 - L1; X = Cury 70, Renan 14, Caiado 55, Zema 30, demais outros, queda do branco e nulo,
    variação do comparecimento, votos do adversário no 1º turno e os próprios; efeito fixo de local (local do 2º
    turno), sem peso. Coeficientes conferidos contra resultados/T7_T14_bweb.json.
B2. Deixar a seção de fora: resíduo vezes m/(m-1), m = seções do local (D1 e D7 do F5 original). Seção sozinha no
    local, n = 0 ou previsão fora de (0, n): sem z (contadas).
B3. Faixas de tamanho (n = votos dos finalistas no 2º turno): 1 a 49, 50 a 149, 150 a 299, 300 ou mais (as da
    tabela do F5 já publicado). Desvio robusto = 1,4826 vezes a mediana dos desvios absolutos em torno da mediana
    da faixa. z recalibrado = z / desvio robusto da faixa (sem centrar; as medianas são relatadas).
B4. Zona = UF + número da zona. Concentração = fração das seções acima de +4 nas 10 zonas com mais delas.
B5. Margem movida por uma cauda = soma de 2 (L2 - L2 previsto deixando a seção de fora).
B6. Caso plantado: sorteio de 10 zonas do Brasil com 200 ou mais seções com z; em cada uma, 100 seções com z
    sorteadas; em cada seção, arredondado(0,05 n) votos passam de R2 para L2 (limitado a R2): +5 pontos da fatia
    de Lula. Tudo é refeito (regressão, previsão, desvios robustos). 20 sorteios (semente 20261110 + i).
    "Detectado" = o critério de sinal inteiro (razão >= 1,3, 200 ou mais acima de +4, 30% em 10 zonas) é atingido
    em 16 ou mais dos 20 sorteios. Ao lado: quantas seções plantadas passam de +4; quantas das 10 zonas plantadas
    aparecem entre as 10 primeiras; e a tabela de resolução (+10 e +15 pontos em 1.000 seções de 10 zonas;
    +5 pontos em 5.000 seções de 50 zonas; 5 sorteios cada), e o plantio espelho (-5 pontos, 5 sorteios).
B7. Veredito: SEM PODER se o caso plantado não for detectado (regra obrigatória), com a classificação pela letra
    ao lado. Se for detectado: SINAL com as três cláusulas; SEM SINAL com razão de 0,8 a 1,25; SEM SINAL (desvio
    para Flávio) com razão abaixo de 0,8; senão INCONCLUSIVO.
B8. Sensibilidades ao lado (não mudam o veredito): só seções com previsão entre 0,1 e 0,9; faixas de tamanho
    cruzadas com 5 faixas de previsão; z em pontos (resíduo em pontos sobre o desvio robusto em pontos da faixa,
    sem a fórmula binomial); faixas por decis de n; sem exterior; n >= 50; sem deixar a seção de fora.
B9. Lista das 30 de maior z recalibrado e das 10 de menor, para auditoria. O reteste não pede arquivos de urna;
    diz-se quais já tiveram os arquivos conferidos no F5 original.

=====================================================================================================
PARTE C. LINEARIDADE (DESCRITIVO, SEM VEREDITO), ESCRITO ANTES DE CALCULAR
- Virada de uma unidade = fatia de Lula entre os dois finalistas no 2º turno menos a mesma fatia no 1º (PT e
  adversário nos outros anos), com votos somados na unidade. Seções do Brasil com os dois turnos, apuradas, com
  votos dos finalistas nos dois turnos. Anos: 2014, 2018, 2022, 2026.
- Quatro níveis: UF em torno do país; município em torno da UF; local em torno do município; seção em torno do
  local. Em cada nível, variância ponderada pelos votos dos finalistas no 2º turno, e o desvio em pontos.
  Para a UF, também o desvio simples entre as 27 (o número do Adendo 29).
- Acaso binomial, duas réguas simuladas e medidas do mesmo jeito (3 sorteios cada):
  (i) "sorteio novo" (teto do acaso): cada seção com a fatia do 1º turno mais a virada da unidade de cima, e L2
      sorteado como binomial de n; (ii) "regra única" (piso): cada bloco do 1º turno (L1, R1, eliminados, branco,
      nulo, faltosos) se divide com as taxas nacionais estimadas no próprio ano (regressão do D4-1 com
      eliminados somados, truncadas entre 0 e 1), por sorteio multinomial. A régua (ii) é o que uma única regra
      nacional de transferência mais o acaso produziria: é a forma numérica da "linearidade".
- Leitura escrita antes: razão observado sobre (ii) perto de 1 em 2026, com os outros anos bem acima, seria a marca
  de virada uniforme demais. Razão abaixo de 1 em qualquer nível seria regularidade maior que o acaso permite.
  Dentro do local, a medida fina é o phi da parte A: phi abaixo de 1 seria dispersão pequena demais.
- "Locais regulares demais": por local do universo da parte A, T = soma de e2/v; fração de locais com T abaixo
  dos quantis de 1% e 5% do qui-quadrado com k-1 graus, contra a mesma fração em dado simulado só com o acaso
  binomial das transições (2 sorteios, regressão refeita). Marca: fração observada acima da simulada. Ao lado, a
  fração acima do quantil de 99%.
- Sem critério registrado: nada desta parte vira veredito de sinal; o que aparecer vira pista.

O QUE FOR FEITO DEPOIS DE VER O RESULTADO fica em funções com nome "exploratorio_" e sai marcado assim.
"""
import sys, os, gzip, json, zipfile, csv, glob, time, hashlib
import numpy as np

RAIZ = '/home/user/casa-control/eleicao-2026'
TRAB = '/home/user/trabalho-eleicao/adendo27/R27_B6'
PERFIL_DIR = '/home/user/trabalho-eleicao/adendo21/F15_dl_perfil_secao'
ZIPS2T = '/home/user/trabalho-eleicao/trab2t/zips2t'
sys.path.insert(0, RAIZ + '/scripts')
from lib import carregar, chave_local, demean  # noqa: E402

SEMENTE = 20261110
NBOOT = 500
ANOS = [2014, 2018, 2022, 2026]
PLACEBO = [2014, 2018, 2022]
MARGEM = 4430191
L2_OFICIAL, R2_OFICIAL = 64256232, 59826041
NECESSARIO = 2215096
P_DOSE = 0.0357
UFS_GOV = ['AC', 'AM', 'DF', 'ES', 'RN', 'TO']
GRUPOS = [('Cury', '70'), ('Renan', '14'), ('Caiado', '55'), ('Zema', '30')]
NX = ['L1', 'R1', 'O1', 'B1', 'N1', 'A1']
NY = ['L2', 'R2', 'BN2', 'A2']
SAIDA_JSON = RAIZ + '/resultados/R27_B6_vizinho_de_sala_e_caudas.json'
SAIDA_TXT = RAIZ + '/resultados/R27_B6_vizinho_de_sala_e_caudas.txt'


def log(*a):
    print('#', time.strftime('%H:%M:%S'), *a, file=sys.stderr, flush=True)


def gravar(nome, obj):
    os.makedirs(TRAB, exist_ok=True)
    tmp = f'{TRAB}/{nome}.tmp'
    with open(tmp, 'w') as f:
        json.dump(obj, f, ensure_ascii=False, indent=1, default=_js)
    os.replace(tmp, f'{TRAB}/{nome}')


def _js(o):
    if isinstance(o, (np.integer,)):
        return int(o)
    if isinstance(o, (np.floating,)):
        return float(o)
    if isinstance(o, np.ndarray):
        return o.tolist()
    if isinstance(o, (np.bool_,)):
        return bool(o)
    raise TypeError(str(type(o)))


# ================================================================ extrações (sem resultado de votos de presidente)
def _perfil_uf(z):
    import pandas as pd
    uf = os.path.basename(z).split('_')[-1][:2]
    jov = [1600, 1700, 1800, 1900, 2000, 2124]
    partes = []
    with zipfile.ZipFile(z) as zf:
        nome = [i.filename for i in zf.infolist() if i.filename.endswith('.csv')][0]
        with zf.open(nome) as f:
            it = pd.read_csv(f, sep=';', encoding='latin-1', chunksize=1500000,
                             usecols=['CD_MUNICIPIO', 'NR_ZONA', 'NR_SECAO', 'CD_GENERO', 'CD_FAIXA_ETARIA',
                                      'CD_GRAU_ESCOLARIDADE', 'QT_ELEITORES'])
            for ch in it:
                q = ch['QT_ELEITORES']
                ch = ch.assign(mul=q * (ch['CD_GENERO'] == 4), jov=q * ch['CD_FAIXA_ETARIA'].isin(jov),
                               ido=q * (ch['CD_FAIXA_ETARIA'] >= 6064), sup8=q * (ch['CD_GRAU_ESCOLARIDADE'] == 8))
                partes.append(ch.groupby(['CD_MUNICIPIO', 'NR_ZONA', 'NR_SECAO'])[
                    ['QT_ELEITORES', 'mul', 'jov', 'ido', 'sup8']].sum())
    g = pd.concat(partes).groupby(level=[0, 1, 2]).sum()
    return {f'{uf}|{m}|{zn}|{s}': [int(x) for x in v] for (m, zn, s), v in zip(g.index, g.values)}


def extrair_perfil():
    from multiprocessing import Pool
    os.makedirs(TRAB, exist_ok=True)
    zips = [z for z in sorted(glob.glob(PERFIL_DIR + '/perfil_eleitor_secao_2026_*.zip')) if not z.endswith('_ZZ.zip')]
    zips.sort(key=os.path.getsize, reverse=True)
    out = {}
    with Pool(3) as p:
        for r in p.imap_unordered(_perfil_uf, zips):
            out.update(r)
            log('perfil', len(out))
    with gzip.open(TRAB + '/perfil_secao_2026.json.gz', 'wt') as f:
        json.dump({'colunas': ['total', 'mulheres', 'de16a24', 'de60mais', 'superior_completo'], 'secoes': out}, f)
    log('perfil: secoes', len(out), 'eleitores', sum(v[0] for v in out.values()))


def extrair_gov2t():
    os.makedirs(TRAB, exist_ok=True)
    out = {}
    for uf in UFS_GOV:
        z = glob.glob(f'{ZIPS2T}/bweb_2t_{uf}_*.zip')[0]
        nlin = 0
        with zipfile.ZipFile(z) as zf:
            nome = [i.filename for i in zf.infolist() if i.filename.endswith('.csv')][0]
            with zf.open(nome) as f:
                cab = [c.strip('"') for c in f.readline().decode('latin-1').rstrip('\r\n').split(';')]
                ix = {c: i for i, c in enumerate(cab)}
                for raw in f:
                    if b'"Governador"' not in raw:
                        continue
                    row = next(csv.reader([raw.decode('latin-1')], delimiter=';', quotechar='"'))
                    if row[ix['CD_CARGO_PERGUNTA']] != '3':
                        continue
                    nlin += 1
                    k = f"{row[ix['SG_UF']]}|{int(row[ix['CD_MUNICIPIO']])}|{int(row[ix['NR_ZONA']])}|{int(row[ix['NR_SECAO']])}"
                    s = out.setdefault(k, {'nom': {}, 'B': 0, 'N': 0, 'outros': 0})
                    tp = row[ix['DS_TIPO_VOTAVEL']].strip().lower()
                    q = int(row[ix['QT_VOTOS']])
                    if tp == 'nominal':
                        s['nom'][row[ix['NR_VOTAVEL']]] = s['nom'].get(row[ix['NR_VOTAVEL']], 0) + q
                    elif tp == 'branco':
                        s['B'] += q
                    elif tp == 'nulo':
                        s['N'] += q
                    else:
                        s['outros'] += q
        log(uf, 'linhas do cargo 3:', nlin)
    with gzip.open(TRAB + '/gov2t_6ufs.json.gz', 'wt') as f:
        json.dump(out, f)
    log('gov2t: secoes', len(out))


# ================================================================ bases
CAMPOS = ['apt1', 'comp1', 'L1', 'R1', 'O1', 'B1', 'N1', 'apt2', 'comp2', 'L2', 'R2', 'B2', 'N2']


def montar(ano):
    """Vetores por seção com os dois turnos (todas as seções que têm 1 e 2). Guarda em npz."""
    arq = f'{TRAB}/base_{ano}.npz'
    if os.path.exists(arq):
        z = np.load(arq)
        return {k: z[k] for k in z.files}
    os.makedirs(TRAB, exist_ok=True)
    d = carregar(f'{RAIZ}/dados/secoes{ano}.json.gz')
    ch = [k for k, v in d.items() if '1' in v and '2' in v]
    n = len(ch)
    b = {c: np.zeros(n, dtype=np.int64) for c in CAMPOS}
    uf = np.empty(n, dtype='U2'); mun = np.empty(n, dtype='U12'); zona = np.empty(n, dtype='U8')
    loc1 = np.empty(n, dtype='U28'); loc2 = np.empty(n, dtype='U28')
    apur = np.zeros(n, dtype=bool); agr = np.zeros(n, dtype=bool)
    g1 = np.full((n, 3), -1, dtype=np.int64)
    for i, k in enumerate(ch):
        v = d[k]; a, c = v['1'], v['2']
        p = k.split('|')
        uf[i] = p[0]; mun[i] = p[0] + '|' + p[1]; zona[i] = p[0] + '|' + p[2]
        loc1[i] = chave_local(k, a); loc2[i] = chave_local(k, c)
        apur[i] = str(a.get('tipo', '')).upper() == 'APURADA' and str(c.get('tipo', '')).upper() == 'APURADA'
        agr[i] = ('agr' in a) or ('agr' in c)
        b['apt1'][i] = a['apt']; b['comp1'][i] = a['comp']; b['L1'][i] = a['L']; b['R1'][i] = a['R']
        b['O1'][i] = a['O']; b['B1'][i] = a['B']; b['N1'][i] = a['N']
        b['apt2'][i] = c['apt']; b['comp2'][i] = c['comp']; b['L2'][i] = c['L']; b['R2'][i] = c['R']
        b['B2'][i] = c['B']; b['N2'][i] = c['N']
        if '1g' in v:
            g1[i] = (v['1g']['B'], v['1g']['N'], v['1g']['V'])
    b.update(chave=np.array(ch), uf=uf, mun=mun, zona=zona, loc1=loc1, loc2=loc2, apur=apur, agr=agr, g1=g1)
    if ano == 2026:
        cand = carregar(f'{RAIZ}/dados/candidatos2026_1t.json.gz')['secoes']
        G = np.zeros((n, len(GRUPOS)), dtype=np.int64)
        for i, k in enumerate(ch):
            cv = cand.get(k, {})
            G[i] = [cv.get(num, 0) for _, num in GRUPOS]
        b['G'] = G
    np.savez_compressed(arq, **b)
    return b


def derivar(b):
    b = dict(b)
    b['A1'] = b['apt1'] - b['comp1']; b['A2'] = b['apt2'] - b['comp2']; b['BN2'] = b['B2'] + b['N2']
    return b


def universo(b, kmin, extra=None, grupo='loc1'):
    u = b['apur'] & (np.abs(b['apt1'] - b['apt2']) <= 2) & (b['comp1'] >= 30) & (b['uf'] != 'ZZ')
    if extra is not None:
        u = u & extra
    _, g = np.unique(b[grupo], return_inverse=True)
    cnt = np.bincount(g, weights=u.astype(float))
    return u & (cnt[g] >= kmin)


# ================================================================ estimador
class Modelo:
    """MQO com efeito fixo (within), peso w; guarda o que não depende da resposta para refazer com Y plantado."""

    def __init__(self, X, grupo, w, nb=None):
        self.X = np.asarray(X, float)
        self.nb = self.X.shape[1] if nb is None else nb     # colunas que são blocos de eleitores do 1º turno
        _, self.g = np.unique(grupo, return_inverse=True)
        self.w = np.asarray(w, float)
        self.k_loc = np.bincount(self.g)[self.g]
        self.kfac = self.k_loc / np.maximum(self.k_loc - 1, 1)
        self.Xd = demean(self.X, self.g, self.w)
        self.WX = self.Xd * self.w[:, None]
        self.Ainv = np.linalg.inv(self.Xd.T @ self.WX)

    def fit(self, Y):
        Y = np.asarray(Y, float)
        if Y.ndim == 1:
            Y = Y[:, None]
        Yd = demean(Y, self.g, self.w)
        beta = self.Ainv @ (self.WX.T @ Yd)
        return beta, Yd - self.Xd @ beta

    def v(self, bcol):
        bt = np.clip(bcol[: self.nb], 0.0, 1.0)
        return self.X[:, : self.nb] @ (bt * (1 - bt))


def em2(u, comum=True):
    """Mistura de duas normais por EM, em dado agrupado (classes de 0,02 entre -12 e 12; fora disso, um a um)."""
    u = np.asarray(u, float)
    dentro = np.abs(u) < 12
    h, edges = np.histogram(u[dentro], bins=1200, range=(-12, 12))
    x = np.concatenate([(edges[:-1] + edges[1:]) / 2, u[~dentro]])
    wt = np.concatenate([h.astype(float), np.ones((~dentro).sum())])
    ok = wt > 0; x = x[ok]; wt = wt[ok]; n = wt.sum()
    piso = 0.05

    def passo(par, it):
        pi, m1, m2, s1, s2 = par
        ll = -np.inf
        for _ in range(it):
            la = np.log(max(1 - pi, 1e-300)) - np.log(s1) - 0.5 * ((x - m1) / s1) ** 2
            lb = np.log(max(pi, 1e-300)) - np.log(s2) - 0.5 * ((x - m2) / s2) ** 2
            mx = np.maximum(la, lb)
            tot = mx + np.log(np.exp(la - mx) + np.exp(lb - mx))
            ll_novo = float((wt * tot).sum() - n * 0.9189385332046727)
            r = np.exp(lb - tot)
            sr = (wt * r).sum(); sq = n - sr
            pi = sr / n
            if sr < 1e-9 or sq < 1e-9:
                ll = ll_novo
                break
            m2 = (wt * r * x).sum() / sr; m1 = (wt * (1 - r) * x).sum() / sq
            q2 = (wt * r * (x - m2) ** 2).sum(); q1 = (wt * (1 - r) * (x - m1) ** 2).sum()
            if comum:
                s1 = s2 = max(np.sqrt((q1 + q2) / n), piso)
            else:
                s1 = max(np.sqrt(q1 / sq), piso); s2 = max(np.sqrt(q2 / sr), piso)
            if abs(ll_novo - ll) < 1e-9 * n:
                ll = ll_novo
                break
            ll = ll_novo
        return ll, (pi, m1, m2, s1, s2)

    sd = float(np.sqrt((wt * (x - (wt * x).sum() / n) ** 2).sum() / n))
    part = [(0.5, -0.5, 0.5), (0.1, -0.2, 1.8), (0.9, -1.8, 0.2), (0.3, -0.6, 1.4), (0.7, -1.4, 0.6), (0.02, 0.0, 4.0),
            (0.98, -4.0, 0.0)]
    cand = []
    for pi, m1, m2 in part:
        cand.append(passo((pi, m1 * sd, m2 * sd, sd if comum else 0.7 * sd, sd if comum else 1.5 * sd), 40))
    cand.sort(key=lambda c: -c[0])
    fim = [passo(c[1], 3000) for c in cand[:3]]
    fim.sort(key=lambda c: -c[0])
    ll, (pi, m1, m2, s1, s2) = fim[0]
    mu = (wt * x).sum() / n
    ll1 = float(-n * np.log(sd) - 0.5 * n - n * 0.9189385332046727)
    if m2 < m1:
        pi, m1, m2, s1, s2 = 1 - pi, m2, m1, s2, s1
    return {'pi_alto': float(pi), 'media_baixo': float(m1), 'media_alto': float(m2), 'dp_baixo': float(s1),
            'dp_alto': float(s2), 'delta_u': float(m2 - m1), 'loglik': ll, 'loglik_uma_normal': ll1,
            'ganho_loglik': float(ll - ll1), 'n': float(n), 'media_u': float(mu), 'dp_u': sd}


class Dado:
    """Um ano no universo da parte A: regressoras, respostas, grupos."""

    def __init__(self, b, mask, extra_X=None, grupo='loc1', extra_e_bloco=True):
        self.mask = mask
        s = {k: v[mask] for k, v in b.items()}
        self.s = s
        self.n = int(mask.sum())
        X = np.column_stack([s[c] for c in NX]).astype(float)
        self.nx = list(NX)
        if extra_X is not None:
            X = np.column_stack([X, extra_X[mask]]); self.nx += [f'cov{i}' for i in range(extra_X.shape[1])]
        self.Y = np.column_stack([s[c] for c in NY]).astype(float)
        self.mod = Modelo(X, s[grupo], 1.0 / s['apt1'], nb=(X.shape[1] if extra_e_bloco else len(NX)))
        _, self.cm = np.unique(s['mun'], return_inverse=True)
        self.G = int(self.cm.max() + 1)
        self.validos2 = (s['L2'] + s['R2']).astype(float)
        self.uf = s['uf']


def medir(D, Y=None, phi_ref=None, mistura=True, livre=False, por_uf=False, boot=False, semente=SEMENTE, guarda=False):
    """Todas as medidas da parte A para as respostas Y (n x 4, na ordem NY) do dado D."""
    Y = D.Y if Y is None else Y
    mod = D.mod
    beta, E = mod.fit(Y)
    r = {'n': D.n, 'locais': int(mod.g.max() + 1), 'municipios': D.G,
         'coef': {y: {x: float(beta[i, j]) for i, x in enumerate(D.nx)} for j, y in enumerate(NY)}}
    V = np.column_stack([mod.v(beta[:, j]) for j in range(4)])
    okv = V[:, 0] > 0
    r['secoes_v_nao_positivo'] = int((~okv).sum())
    kf = mod.kfac
    eL = E[:, 0]; vL = np.where(okv, V[:, 0], np.nan)
    contrib = eL ** 2 / vL * kf
    r['phi'] = float(np.nanmean(contrib))
    r['phi_razao_das_somas'] = float(np.nansum(eL ** 2 * kf * okv) / np.nansum(V[:, 0] * okv))
    r['phi_robusto'] = float(np.nanmedian(contrib) / 0.4549364)
    r['dp_residuo_votos'] = float(np.sqrt(np.mean(eL ** 2 * kf)))
    r['v_medio'] = float(np.nanmean(vL))
    for j, y in enumerate(NY[1:], start=1):
        vj = V[:, j]; okj = vj > 0
        r['phi_' + y] = float(np.mean(E[okj, j] ** 2 / vj[okj] * kf[okj]))
    for j, y in ((1, 'R2'), (2, 'BN2'), (3, 'A2')):
        r['c_L_' + y] = float(np.nanmean(eL * E[:, j] / vL * kf))
    r['parcela_espelhada_em_R'] = -r['c_L_R2'] / r['phi']
    r['parcela_em_BN'] = -r['c_L_BN2'] / r['phi']
    r['parcela_em_abstencao'] = -r['c_L_A2'] / r['phi']
    r['phi_de_troca'] = -r['c_L_R2']
    if boot:
        rng = np.random.default_rng(semente)
        c0 = np.where(okv, contrib, 0.0)
        Sm = np.bincount(D.cm, weights=c0, minlength=D.G); Nm = np.bincount(D.cm, weights=okv.astype(float), minlength=D.G)
        c1 = np.where(okv, -(eL * E[:, 1] / vL * kf), 0.0)
        Tm = np.bincount(D.cm, weights=c1, minlength=D.G)
        bt = np.empty(NBOOT); bt2 = np.empty(NBOOT)
        for i in range(NBOOT):
            cnt = np.bincount(rng.integers(0, D.G, D.G), minlength=D.G)
            bt[i] = (cnt * Sm).sum() / (cnt * Nm).sum(); bt2[i] = (cnt * Tm).sum() / (cnt * Nm).sum()
        r['ep_phi'] = float(bt.std(ddof=1)); r['ic95_phi'] = [float(np.percentile(bt, 2.5)), float(np.percentile(bt, 97.5))]
        r['ep_phi_de_troca'] = float(bt2.std(ddof=1))
        r['_boot'] = bt; r['_boot_troca'] = bt2
    if por_uf:
        pu = {}
        for uf in np.unique(D.uf):
            m = (D.uf == uf) & okv
            pu[str(uf)] = {'n': int(m.sum()), 'phi': float(np.mean(contrib[m])),
                           'phi_de_troca': float(np.mean(-(eL[m] * E[m, 1] / vL[m] * kf[m])))}
        r['por_uf'] = pu
    if phi_ref is not None:
        esc = np.sqrt(vL * phi_ref)
        u = eL / esc
        uo = u[okv]
        fd = float((uo > 3).mean()); fe = float((uo < -3).mean())
        r['cauda_direita'] = fd; r['cauda_esquerda'] = fe
        r['n_direita'] = int((uo > 3).sum()); r['n_esquerda'] = int((uo < -3).sum())
        r['razao_caudas'] = (fd / fe) if fe > 0 else (float('inf') if fd > 0 else None)
        r['dp_u'] = float(uo.std()); r['assimetria_u'] = float(((uo - uo.mean()) ** 3).mean() / uo.std() ** 3)
        r['curtose_u'] = float(((uo - uo.mean()) ** 4).mean() / uo.std() ** 4)
        soma_esc = float(np.nansum(esc[okv])); val = float(D.validos2[okv].sum())
        r['soma_raiz_v_phi_ref'] = soma_esc; r['validos_universo'] = val
        if mistura:
            mx = em2(uo, comum=True)
            mx['delta_pp'] = 100 * mx['delta_u'] * soma_esc / val
            mx['votos_implicados'] = mx['pi_alto'] * mx['delta_u'] * soma_esc
            mx['votos_implicados_espelho'] = (1 - mx['pi_alto']) * mx['delta_u'] * soma_esc
            r['mistura'] = mx
            if livre:
                ml = em2(uo, comum=False)
                ml['delta_pp'] = 100 * ml['delta_u'] * soma_esc / val
                ml['votos_implicados'] = ml['pi_alto'] * ml['delta_u'] * soma_esc
                r['mistura_variancias_livres'] = ml
        if guarda:
            r['_u'] = u; r['_okv'] = okv
    if guarda:
        r['_E'] = E; r['_V'] = V; r['_beta'] = beta
    return r


def limpa(r):
    return {k: v for k, v in r.items() if not k.startswith('_')}


def veredito_A(phi26, phis_placebo, razao_caudas, mix):
    mx = max(phis_placebo); mn = min(phis_placebo)
    raz = phi26 / mx
    c1 = raz >= 1.5
    c2a = razao_caudas is not None and (razao_caudas >= 3 or razao_caudas <= 1 / 3)
    c2b = mix is not None and mix['delta_pp'] >= 2 and 0.05 <= mix['pi_alto'] <= 0.95
    c3 = mix is not None and mix['votos_implicados'] >= 550000
    s1 = raz <= 1.15
    s2 = razao_caudas is not None and 0.67 <= razao_caudas <= 1.5
    varia = mx / mn > 1.5
    if c1 and (c2a or c2b) and c3:
        v = 'SINAL'
    elif varia:
        v = 'INCONCLUSIVO'
    elif s1 and s2:
        v = 'SEM SINAL'
    else:
        v = 'INCONCLUSIVO'
    return v, {'razao_phi_sobre_maior_placebo': raz, 'sinal_phi_1,5': bool(c1), 'sinal_cauda_3x': bool(c2a),
               'sinal_mistura_2pp_5a95': bool(c2b), 'sinal_votos_550mil': bool(c3), 'semsinal_phi_1,15': bool(s1),
               'semsinal_caudas_0,67_a_1,5': bool(s2), 'placebos_variam_mais_de_1,5': bool(varia),
               'max_sobre_min_placebo': mx / mn}


def plantar(fonte, p, frac, rng):
    n = len(fonte)
    if frac >= 1:
        return rng.binomial(fonte, p)
    sel = np.zeros(n, bool); sel[rng.permutation(n)[: int(round(frac * n))]] = True
    pc = p * fonte.sum() / fonte[sel].sum()
    return np.where(sel, rng.binomial(fonte, min(pc, 1.0)), 0)


def y_troca(D, f, de='R'):
    Y = D.Y.copy()
    if de == 'R':
        Y[:, 0] += f; Y[:, 1] -= f
    else:
        Y[:, 0] -= f; Y[:, 1] += f
    return Y


def carregar_perfil(b):
    """Parcelas do perfil por seção alinhadas à base: (tem, cov[n,4] = parcela x aptos do 1º turno, parcela de 60+)."""
    with gzip.open(TRAB + '/perfil_secao_2026.json.gz', 'rt') as f:
        p = json.load(f)['secoes']
    n = len(b['chave'])
    tem = np.zeros(n, bool); cov = np.zeros((n, 4)); ido = np.zeros(n)
    for i, k in enumerate(b['chave']):
        v = p.get(k)
        if v is None or v[0] <= 0:
            continue
        tem[i] = True
        tot = v[0]
        cov[i] = [v[2] / tot, v[3] / tot, v[4] / tot, v[1] / tot]
        ido[i] = v[3] / tot
    cov = cov * b['apt1'][:, None]
    return tem, cov, ido


# ================================================================ PARTE A
def parte_A():
    t0 = time.time()
    R = {'parte': 'A (D4-5, vizinho de sala)'}
    bases = {a: derivar(montar(a)) for a in ANOS}
    D = {}
    bruto = {}
    for a in ANOS:
        b = bases[a]
        D[a] = Dado(b, universo(b, 4))
        bruto[a] = medir(D[a])
        log('bruto', a, 'n', D[a].n, 'phi', round(bruto[a]['phi'], 4))
    phis = {a: bruto[a]['phi'] for a in ANOS}
    phi_ref = float(np.median([phis[a] for a in PLACEBO]))
    R['phi_ref_mediana_placebo'] = phi_ref
    # segunda passada com phi_ref: caudas, mistura, por UF
    res = {}
    for a in ANOS:
        r = medir(D[a], phi_ref=phi_ref, mistura=True, livre=True, por_uf=True, boot=True, semente=SEMENTE + a, guarda=True)
        res[a] = r
        log('medidas', a, 'caudas', r['cauda_direita'], r['cauda_esquerda'], 'mistura', r['mistura']['pi_alto'], r['mistura']['delta_pp'])
    # bootstrap das caudas (por município)
    for a in ANOS:
        r = res[a]; u = r['_u']; okv = r['_okv']
        rng = np.random.default_rng(SEMENTE + a + 7)
        d = np.bincount(D[a].cm, weights=((u > 3) & okv).astype(float), minlength=D[a].G)
        e = np.bincount(D[a].cm, weights=((u < -3) & okv).astype(float), minlength=D[a].G)
        bt = np.empty(NBOOT)
        for i in range(NBOOT):
            cnt = np.bincount(rng.integers(0, D[a].G, D[a].G), minlength=D[a].G)
            bt[i] = (cnt * d).sum() / max((cnt * e).sum(), 1e-9)
        r['ic95_razao_caudas'] = [float(np.percentile(bt, 2.5)), float(np.percentile(bt, 97.5))]
    bt_raz = res[2026]['_boot'] / np.maximum.reduce([res[a]['_boot'] for a in PLACEBO])
    ver, cl = veredito_A(phis[2026], [phis[a] for a in PLACEBO], res[2026]['razao_caudas'], res[2026]['mistura'])
    R['por_ano'] = {str(a): limpa(res[a]) for a in ANOS}
    R['primaria'] = {'phi_2026': phis[2026], 'ep_phi_2026': res[2026]['ep_phi'],
                     'phi_placebo': {str(a): phis[a] for a in PLACEBO},
                     'ep_phi_placebo': {str(a): res[a]['ep_phi'] for a in PLACEBO},
                     'maior_placebo': max(phis[a] for a in PLACEBO), 'razao': cl['razao_phi_sobre_maior_placebo'],
                     'ic95_razao': [float(np.percentile(bt_raz, 2.5)), float(np.percentile(bt_raz, 97.5))],
                     'ep_razao': float(bt_raz.std(ddof=1))}
    R['veredito_pela_letra_bruto'] = ver; R['clausulas_bruto'] = cl
    # as outras equações e o phi de troca: razão 2026 sobre o maior placebo
    R['espelho_outras_equacoes'] = {}
    for nome in ('phi', 'phi_R2', 'phi_BN2', 'phi_A2', 'phi_de_troca', 'phi_razao_das_somas', 'phi_robusto'):
        vals = {str(a): res[a][nome] for a in ANOS}
        R['espelho_outras_equacoes'][nome] = {'valores': vals, 'razao_2026_sobre_maior_placebo': res[2026][nome] / max(res[a][nome] for a in PLACEBO),
                                              'max_sobre_min_placebo': max(res[a][nome] for a in PLACEBO) / min(res[a][nome] for a in PLACEBO)}
    bt_tr = res[2026]['_boot_troca'] / np.maximum.reduce([res[a]['_boot_troca'] for a in PLACEBO])
    R['espelho_outras_equacoes']['phi_de_troca']['ic95_razao'] = [float(np.percentile(bt_tr, 2.5)), float(np.percentile(bt_tr, 97.5))]
    # phi por UF: razão 2026 sobre o maior placebo da UF
    pu = {}
    for uf in sorted(res[2026]['por_uf']):
        pl = [res[a]['por_uf'][uf]['phi'] for a in PLACEBO if uf in res[a]['por_uf']]
        pu[uf] = {'phi_2026': res[2026]['por_uf'][uf]['phi'], 'n_2026': res[2026]['por_uf'][uf]['n'],
                  'placebo': {str(a): res[a]['por_uf'][uf]['phi'] for a in PLACEBO if uf in res[a]['por_uf']},
                  'razao_sobre_maior_placebo': res[2026]['por_uf'][uf]['phi'] / max(pl) if pl else None,
                  'phi_de_troca_2026': res[2026]['por_uf'][uf]['phi_de_troca'],
                  'phi_de_troca_placebo': {str(a): res[a]['por_uf'][uf]['phi_de_troca'] for a in PLACEBO if uf in res[a]['por_uf']}}
    R['phi_por_uf'] = pu
    gravar('parcial_A.json', R)

    # ---------- variantes
    b26 = bases[2026]
    var = {}
    Dv = Dado(b26, universo(b26, 4, extra=~b26['agr']))
    var['v1_2026_sem_agregadas'] = limpa(medir(Dv, phi_ref=phi_ref))
    G = b26['G']
    Xsep = np.column_stack([G[:, 0], G[:, 1], G[:, 2]]).astype(float)   # Cury, Renan, Caiado; O1 passa a ser "demais"
    b26s = dict(b26); b26s['O1'] = b26['O1'] - G[:, :3].sum(1)
    Ds = Dado(b26s, universo(b26, 4), extra_X=Xsep)
    var['v2_2026_eliminados_separados'] = limpa(medir(Ds, phi_ref=phi_ref))
    tem, cov, ido = carregar_perfil(b26)
    u_perf = universo(b26, 4, extra=tem)
    Dc0 = Dado(b26, u_perf); Dc1 = Dado(b26, u_perf, extra_X=cov, extra_e_bloco=False)
    var['v3_2026_mesmo_universo_sem_covariaveis'] = limpa(medir(Dc0, phi_ref=phi_ref))
    var['v3_2026_com_covariaveis_de_perfil'] = limpa(medir(Dc1, phi_ref=phi_ref))
    var['v3_secoes_sem_perfil_fora'] = int(universo(b26, 4).sum() - u_perf.sum())
    # v4: coeficientes por UF
    v4 = {}
    for a in ANOS:
        b = bases[a]; u = universo(b, 4)
        tot = 0.0; tot_tr = 0.0; nn = 0; por = {}
        for uf in np.unique(b['uf'][u]):
            m = universo(b, 4, extra=(b['uf'] == uf))
            if m.sum() < 50:
                continue
            Du = Dado(b, m); ru = medir(Du)
            por[str(uf)] = {'n': Du.n, 'phi': ru['phi'], 'phi_de_troca': ru['phi_de_troca']}
            tot += ru['phi'] * Du.n; tot_tr += ru['phi_de_troca'] * Du.n; nn += Du.n
        v4[str(a)] = {'phi': tot / nn, 'phi_de_troca': tot_tr / nn, 'n': nn, 'por_uf': por}
    v4['razao_2026_sobre_maior_placebo'] = v4['2026']['phi'] / max(v4[str(a)]['phi'] for a in PLACEBO)
    v4['razao_phi_de_troca'] = v4['2026']['phi_de_troca'] / max(v4[str(a)]['phi_de_troca'] for a in PLACEBO)
    var['v4_coeficientes_por_uf'] = v4
    v5 = {}
    for a in ANOS:
        b = bases[a]
        v5[str(a)] = limpa(medir(Dado(b, universo(b, 2))))
    v5['razao_2026_sobre_maior_placebo'] = v5['2026']['phi'] / max(v5[str(a)]['phi'] for a in PLACEBO)
    var['v5_locais_com_2_ou_mais'] = v5
    R['variantes'] = var
    gravar('parcial_A.json', R)
    log('variantes ok', round(time.time() - t0))

    # ---------- placebo contemporâneo: governador
    R['placebo_governador'] = placebo_gov(b26)
    gravar('parcial_A.json', R)
    log('governador ok', round(time.time() - t0))

    # ---------- calibração: plantio da troca
    def avalia_plantado(a, Y, com_mistura=True):
        r = medir(D[a], Y=Y, phi_ref=phi_ref, mistura=com_mistura)
        r = limpa(r)
        r['fator_sobre_bruto'] = r['phi'] / phis[a]
        r['fator_phi_de_troca'] = r['phi_de_troca'] / res[a]['phi_de_troca']
        outros = [phis[x] for x in PLACEBO] if a == 2026 else [phis[x] for x in ANOS if x not in (a, 2026)]
        vv, cc = veredito_A(r['phi'], outros, r['razao_caudas'], r.get('mistura'))
        r['veredito_pela_letra_com_plantio'] = vv; r['clausulas'] = cc
        r.pop('coef', None)
        return r

    cen26 = [(d, f) for f in (0.10, 0.30, 0.50, 0.70, 0.90) for d in (1.0, 0.5, 0.25)] + [(1.0, 1.0)]
    cen22 = [(1.0, 0.10), (1.0, 0.30), (1.0, 0.50), (1.0, 0.70), (1.0, 0.90), (1.0, 1.0), (0.5, 0.30), (0.5, 0.50)]
    cal = {'2026': {}, '2022': {}}
    for a, cens in ((2026, cen26), (2022, cen22)):
        R2 = D[a].s['R2']
        for i, (d, f) in enumerate(cens):
            rng = np.random.default_rng(SEMENTE + 100 * (a - 2000) + i)
            mov = plantar(R2, d * P_DOSE, f, rng)
            r = avalia_plantado(a, y_troca(D[a], mov))
            r['dose'] = d; r['fracao_urnas'] = f; r['votos_movidos'] = int(mov.sum())
            cal[str(a)][f'dose{d:g}_f{int(round(100 * f))}'] = r
            log('plantio', a, d, f, 'fator', round(r['fator_sobre_bruto'], 3), r['veredito_pela_letra_com_plantio'])
        R['calibracao_troca'] = cal
        gravar('parcial_A.json', R)
    # repetição do cenário de referência
    rep = []
    R2 = D[2026].s['R2']
    for j in range(5):
        rng = np.random.default_rng(SEMENTE + 5000 + j)
        mov = plantar(R2, P_DOSE, 0.30, rng)
        r = avalia_plantado(2026, y_troca(D[2026], mov))
        rep.append({'fator_sobre_bruto': r['fator_sobre_bruto'], 'phi': r['phi'], 'razao_caudas': r['razao_caudas'],
                    'pi_alto': r['mistura']['pi_alto'], 'delta_pp': r['mistura']['delta_pp'],
                    'votos_implicados': r['mistura']['votos_implicados'], 'votos_movidos': int(mov.sum()),
                    'parcela_espelhada_em_R': r['parcela_espelhada_em_R'], 'fator_phi_de_troca': r['fator_phi_de_troca'],
                    'veredito': r['veredito_pela_letra_com_plantio']})
    R['calibracao_referencia_5_sorteios'] = rep
    ref = cal['2026']['dose1_f30']
    fator_ref = ref['fator_sobre_bruto']
    sem_poder = (fator_ref < 1.15) or (ver == 'SEM SINAL' and ref['veredito_pela_letra_com_plantio'] == 'SEM SINAL')
    R['poder'] = {'fator_cenario_referencia': fator_ref, 'veredito_com_referencia_plantada': ref['veredito_pela_letra_com_plantio'],
                  'sem_poder': bool(sem_poder),
                  'cenarios_com_fator_1,15_ou_mais': [k for k, v in cal['2026'].items() if v['fator_sobre_bruto'] >= 1.15],
                  'cenarios_com_fator_abaixo_de_1,15': [k for k, v in cal['2026'].items() if v['fator_sobre_bruto'] < 1.15],
                  'cenarios_que_saem_de_SEM_SINAL_pela_letra': [k for k, v in cal['2026'].items() if v['veredito_pela_letra_com_plantio'] != 'SEM SINAL'],
                  'cenarios_que_dao_SINAL_pela_letra': [k for k, v in cal['2026'].items() if v['veredito_pela_letra_com_plantio'] == 'SINAL']}
    R['veredito'] = 'SEM PODER' if sem_poder else ver
    gravar('parcial_A.json', R)

    # ---------- espelho plantado e explicações inocentes
    S = D[2026].s
    dose_votos = P_DOSE * S['R2'].sum()
    rng = np.random.default_rng(SEMENTE + 9001)
    movL = plantar(S['L2'], dose_votos / S['L2'].sum(), 0.30, rng)
    r = avalia_plantado(2026, y_troca(D[2026], movL, de='L')); r['votos_movidos'] = int(movL.sum())
    R['espelho_plantado_L_para_R'] = r
    # I1: mobilização desigual
    rng = np.random.default_rng(SEMENTE + 9002)
    n = D[2026].n
    sel = np.zeros(n, bool); sel[rng.permutation(n)[: int(round(0.30 * n))]] = True
    q = dose_votos / ((2 / 3) * S['A2'][sel].sum())
    novos = np.where(sel, rng.binomial(np.maximum(S['A2'], 0), min(q, 1.0)), 0)
    paraL = rng.binomial(novos, 2 / 3)
    Y = D[2026].Y.copy(); Y[:, 0] += paraL; Y[:, 1] += novos - paraL; Y[:, 3] -= novos
    r = avalia_plantado(2026, Y); r['votos_para_L'] = int(paraL.sum()); r['novos_votantes'] = int(novos.sum()); r['fracao_dos_faltosos_nas_sorteadas'] = float(q)
    R['inocente_I1_mobilizacao_desigual'] = r
    # I2: conversão dos eliminados dependente do perfil (precisa do perfil; seções sem perfil ficam sem deslocamento)
    m26 = D[2026].mask
    tem_u = tem[m26]; ido_u = ido[m26]
    g = D[2026].mod.g; apt = S['apt1'].astype(float)
    sw = np.bincount(g, weights=apt * tem_u); sm = np.bincount(g, weights=apt * tem_u * ido_u)
    med = (sm / np.where(sw > 0, sw, 1))[g]
    z = np.where(tem_u, ido_u - med, 0.0)
    bruto_d = S['O1'] * z
    gama = dose_votos / np.abs(bruto_d).sum()
    alvo = gama * bruto_d
    rng = np.random.default_rng(SEMENTE + 9003)
    mag = np.floor(np.abs(alvo)) + (rng.random(n) < (np.abs(alvo) - np.floor(np.abs(alvo))))
    pos = np.minimum(np.where(alvo > 0, mag, 0), S['R2']); neg = np.minimum(np.where(alvo < 0, mag, 0), S['L2'])
    desl = pos - neg
    Y = D[2026].Y.copy(); Y[:, 0] += desl; Y[:, 1] -= desl
    r = avalia_plantado(2026, Y); r['soma_dos_valores_absolutos'] = float(np.abs(desl).sum()); r['saldo'] = float(desl.sum()); r['gama'] = float(gama)
    R['inocente_I2_conversao_por_perfil'] = r
    # o que a variante com covariáveis absorve em cada plantio (universo com perfil)
    idx_full = np.where(m26)[0]; idx_perf = np.where(u_perf)[0]
    mapa = np.searchsorted(idx_full, idx_perf)      # o universo com perfil é subconjunto do principal
    assert (idx_full[mapa] == idx_perf).all()
    absor = {}
    base0 = medir(Dc0)['phi']; base1 = medir(Dc1)['phi']
    rng = np.random.default_rng(SEMENTE + 130)
    movref = plantar(S['R2'], P_DOSE, 0.30, rng)
    for nome, Yp in (('troca_referencia', y_troca(D[2026], movref)), ('I1', None), ('I2', None)):
        if nome == 'I1':
            Yp = D[2026].Y.copy(); Yp[:, 0] += paraL; Yp[:, 1] += novos - paraL; Yp[:, 3] -= novos
        if nome == 'I2':
            Yp = D[2026].Y.copy(); Yp[:, 0] += desl; Yp[:, 1] -= desl
        Ys = Yp[mapa]
        p0 = medir(Dc0, Y=Ys)['phi']; p1 = medir(Dc1, Y=Ys)['phi']
        absor[nome] = {'phi_sem_cov': p0, 'phi_com_cov': p1, 'subida_sem_cov': p0 - base0, 'subida_com_cov': p1 - base1,
                       'fracao_absorvida_pelas_covariaveis': 1 - (p1 - base1) / (p0 - base0) if p0 != base0 else None}
    absor['bruto'] = {'phi_sem_cov': base0, 'phi_com_cov': base1}
    R['absorcao_pelas_covariaveis'] = absor
    gravar('parcial_A.json', R)

    # ---------- tradução em votos
    trad = {'votos_implicados_mistura_universo': res[2026]['mistura']['votos_implicados'],
            'margem_implicada_mistura': 2 * res[2026]['mistura']['votos_implicados'],
            'validos_universo': res[2026]['validos_universo'], 'validos_pais_2t': L2_OFICIAL + R2_OFICIAL,
            'votos_implicados_mistura_extrapolado_pais': res[2026]['mistura']['votos_implicados'] * (L2_OFICIAL + R2_OFICIAL) / res[2026]['validos_universo']}
    bases_phi = {'binomial_1': 1.0, 'menor_placebo': min(phis[a] for a in PLACEBO), 'mediana_placebo': phi_ref,
                 'maior_placebo': max(phis[a] for a in PLACEBO)}
    teto = {}
    for f in (0.10, 0.30, 0.50, 0.70, 0.90):
        ds = np.array([0.25, 0.5, 1.0])
        dl = np.array([cal['2026'][f'dose{d:g}_f{int(round(100 * f))}']['phi'] - phis[2026] for d in ds])
        M = np.column_stack([ds, ds ** 2])
        co, *_ = np.linalg.lstsq(M, dl, rcond=None)
        a_, c_ = float(co[0]), float(co[1])
        if a_ < 0:
            a_ = 0.0; c_ = float((dl * ds ** 2).sum() / (ds ** 4).sum())
        if c_ < 0:
            c_ = 0.0; a_ = float((dl * ds).sum() / (ds ** 2).sum())
        linha = {'ajuste_a': a_, 'ajuste_c': c_, 'subidas_medidas': {f'{d:g}': float(x) for d, x in zip(ds, dl)}}
        for nb, base in bases_phi.items():
            folga = phis[2026] - base
            if a_ <= 0 and c_ <= 0:
                dmax = float('nan')          # o plantio não move phi nessa fração de urnas: o teste é cego, não há teto
            elif folga <= 0:
                dmax = 0.0
            elif c_ > 0:
                dmax = (-a_ + np.sqrt(a_ ** 2 + 4 * c_ * folga)) / (2 * c_)
            else:
                dmax = folga / a_ if a_ > 0 else float('nan')
            p = dmax * P_DOSE
            mov = p / (1 - p) * R2_OFICIAL if p < 1 else float('nan')
            linha[nb] = {'folga_phi': folga, 'dose_maxima_em_doses_inteiras': float(dmax), 'votos_movidos': float(mov),
                         'margem': float(2 * mov), 'pct_da_margem': float(100 * 2 * mov / MARGEM)}
        teto[f'{int(round(100 * f))}%'] = linha
    trad['teto_por_fracao_de_urnas'] = teto
    R['traducao_em_votos'] = trad
    R['segundos'] = round(time.time() - t0)
    gravar('parcial_A.json', R)
    log('parte A pronta', R['veredito'], round(time.time() - t0))


def placebo_gov(b26):
    cand = carregar(f'{RAIZ}/dados/candidatos_gov_2026_1t_6ufs.json.gz')['secoes']
    with gzip.open(TRAB + '/gov2t_6ufs.json.gz', 'rt') as f:
        g2 = json.load(f)
    out = {'por_uf': {}}
    tot_g = tot_p = tot_gt = tot_pt = 0.0; nn = 0
    for uf in UFS_GOV:
        idx = np.where(b26['uf'] == uf)[0]
        soma = {}
        for i in idx:
            s = g2.get(b26['chave'][i])
            if s:
                for num, q in s['nom'].items():
                    soma[num] = soma.get(num, 0) + q
        fin = sorted(soma, key=lambda x: -soma[x])[:2]
        Lg, Rg = fin[0], fin[1]
        n = len(b26['chave'])
        tem = np.zeros(n, bool)
        arr = {c: np.zeros(n) for c in ('L1', 'R1', 'O1', 'B1', 'N1', 'L2', 'R2', 'BN2')}
        for i in idx:
            k = b26['chave'][i]
            s2 = g2.get(k); c1 = cand.get(k)
            if s2 is None or c1 is None or b26['g1'][i, 2] < 0:
                continue
            tem[i] = True
            l1 = c1.get(Lg, 0); r1 = c1.get(Rg, 0)
            arr['L1'][i] = l1; arr['R1'][i] = r1; arr['O1'][i] = b26['g1'][i, 2] - l1 - r1
            arr['B1'][i] = b26['g1'][i, 0]; arr['N1'][i] = b26['g1'][i, 1]
            arr['L2'][i] = s2['nom'].get(Lg, 0); arr['R2'][i] = s2['nom'].get(Rg, 0); arr['BN2'][i] = s2['B'] + s2['N']
        m = universo(b26, 4, extra=tem)
        bg = dict(b26)
        for c in arr:
            bg[c] = arr[c]
        Dg = Dado(bg, m); rg = medir(Dg)
        Dp = Dado(b26, m); rp = medir(Dp)
        out['por_uf'][uf] = {'finalistas': {'L_vencedor': Lg, 'R': Rg, 'votos_2t': {Lg: soma[Lg], Rg: soma[Rg]}},
                             'n': Dg.n, 'locais': rg['locais'], 'phi_governador': rg['phi'], 'phi_presidente': rp['phi'],
                             'razao_pres_sobre_gov': rp['phi'] / rg['phi'],
                             'phi_de_troca_governador': rg['phi_de_troca'], 'phi_de_troca_presidente': rp['phi_de_troca'],
                             'parcela_espelhada_gov': rg['parcela_espelhada_em_R'], 'parcela_espelhada_pres': rp['parcela_espelhada_em_R'],
                             'O1_negativo': int((arr['O1'][m] < 0).sum())}
        tot_g += rg['phi'] * Dg.n; tot_p += rp['phi'] * Dg.n; nn += Dg.n
        tot_gt += rg['phi_de_troca'] * Dg.n; tot_pt += rp['phi_de_troca'] * Dg.n
    out['seis_ufs'] = {'n': nn, 'phi_governador': tot_g / nn, 'phi_presidente': tot_p / nn,
                       'razao_pres_sobre_gov': tot_p / tot_g, 'phi_de_troca_governador': tot_gt / nn,
                       'phi_de_troca_presidente': tot_pt / nn, 'razao_phi_de_troca': tot_pt / tot_gt}
    return out


# ================================================================ PARTE B (F5)
FAIXAS_N = [(1, 50), (50, 150), (150, 300), (300, 10 ** 9)]


def f5_prepara():
    b = derivar(montar(2026))
    n = len(b['chave'])
    G = b['G'].astype(float)
    Xc = [G[:, 0], G[:, 1], G[:, 2], G[:, 3], b['O1'] - G.sum(1), (b['B1'] + b['N1']) - (b['B2'] + b['N2']), b['comp2'] - b['comp1']]
    XL = np.column_stack(Xc + [b['R1'], b['L1']]).astype(float)
    modL = Modelo(XL, b['loc2'], np.ones(n))
    P = {'b': b, 'modL': modL, 'm': modL.k_loc, 'nfin': (b['L2'] + b['R2']).astype(float),
         'zz': b['uf'] == 'ZZ', 'nomes': [g for g, _ in GRUPOS] + ['demais_outros', 'queda_branco_nulo', 'var_comparecimento', 'adversario_1T', 'proprio_1T']}
    _, P['zid'] = np.unique(b['zona'], return_inverse=True)
    P['zonas'] = np.unique(b['zona'])
    return P


def desvio_rob(x):
    med = np.median(x)
    return float(1.4826 * np.median(np.abs(x - med))), float(med)


def f5_z(P, L2, modo='loo'):
    """z binomial com previsão deixando a seção de fora (ou dentro), e resíduo em pontos."""
    b = P['b']; n = P['nfin']; m = P['m']
    beta, E = P['modL'].fit(L2 - b['L1'])
    res = E[:, 0]
    fator = np.where(m >= 2, m / np.maximum(m - 1, 1), np.nan) if modo == 'loo' else np.where(m >= 2, 1.0, np.nan)
    rl = res * fator
    L2h = L2 - rl
    ok = (m >= 2) & (n > 0) & (L2h > 0) & (L2h < n)
    nn = np.where(n > 0, n, 1)
    p = np.where(ok, L2h / nn, np.nan)
    z = np.where(ok, (L2 / nn - p) / np.sqrt(p * (1 - p) / nn), np.nan)
    pts = np.where((m >= 2) & (n > 0), 100 * rl / nn, np.nan)
    return {'beta': beta[:, 0], 'z': z, 'ok': ok, 'p': p, 'rl': rl, 'pts': pts, 'ok_pts': (m >= 2) & (n > 0)}


def recalibra(x, ok, faixa_id, nf):
    out = np.full(len(x), np.nan); info = []
    for j in range(nf):
        mk = ok & (faixa_id == j)
        if mk.sum() < 30:
            info.append({'secoes': int(mk.sum()), 'desvio_robusto': None, 'mediana': None})
            continue
        s, med = desvio_rob(x[mk])
        out[mk] = x[mk] / s if s > 0 else np.nan
        info.append({'secoes': int(mk.sum()), 'desvio_robusto': s, 'mediana': med})
    return out, info


def f5_conta(P, zr, mask, rl, lim=4.0):
    up = mask & (zr > lim); dn = mask & (zr < -lim)
    a, c = int(up.sum()), int(dn.sum())
    r = {'secoes_com_z': int((mask & ~np.isnan(zr)).sum()), 'acima': a, 'abaixo': c, 'razao': (a / c if c else (float('inf') if a else None))}
    if a:
        cz = np.bincount(P['zid'][up], minlength=len(P['zonas']))
        top = np.argsort(-cz, kind='stable')[:10]
        r['zonas_distintas_acima'] = int((cz > 0).sum())
        r['top10_zonas'] = [[str(P['zonas'][i]), int(cz[i])] for i in top if cz[i] > 0]
        r['pct_nas_10_zonas'] = float(100 * cz[top].sum() / a)
        r['_top10_ids'] = top[cz[top] > 0]
    else:
        r['pct_nas_10_zonas'] = None; r['_top10_ids'] = np.array([], int)
    if c:
        cz = np.bincount(P['zid'][dn], minlength=len(P['zonas']))
        top = np.argsort(-cz, kind='stable')[:10]
        r['zonas_distintas_abaixo'] = int((cz > 0).sum())
        r['top10_zonas_abaixo'] = [[str(P['zonas'][i]), int(cz[i])] for i in top if cz[i] > 0]
        r['pct_nas_10_zonas_abaixo'] = float(100 * cz[top].sum() / c)
    r['margem_cauda_de_cima'] = float(2 * rl[up].sum()); r['margem_cauda_de_baixo'] = float(2 * rl[dn].sum())
    r['margem_liquida'] = r['margem_cauda_de_cima'] + r['margem_cauda_de_baixo']
    r['pct_da_margem_nacional'] = 100 * r['margem_liquida'] / MARGEM
    if a and c:
        r['ep_log_razao'] = float(np.sqrt(1 / a + 1 / c))
    return r


def faixa_n_id(n):
    f = np.full(len(n), -1)
    for j, (lo, hi) in enumerate(FAIXAS_N):
        f[(n >= lo) & (n < hi)] = j
    return f


def f5_principal(P, L2):
    Z = f5_z(P, L2)
    fid = faixa_n_id(P['nfin'])
    zr, info = recalibra(Z['z'], Z['ok'], fid, len(FAIXAS_N))
    c = f5_conta(P, zr, Z['ok'], Z['rl'])
    return Z, zr, info, c


def classifica_f5(c):
    R = c['razao']; a = c['acima']; pct = c.get('pct_nas_10_zonas') or 0
    if R is not None and R >= 1.3 and a >= 200 and pct >= 30:
        return 'SINAL'
    if R is not None and 0.8 <= R <= 1.25:
        return 'SEM SINAL'
    if R is not None and R < 0.8:
        return 'SEM SINAL (desvio para Flávio)'
    return 'INCONCLUSIVO'


def f5_planta(P, Zbruto, rng, pts, por_zona, nzonas, sinal=1):
    b = P['b']; ok = Zbruto['ok'] & ~P['zz']
    cz = np.bincount(P['zid'][ok], minlength=len(P['zonas']))
    eleg = np.where(cz >= 2 * por_zona)[0]
    zs = rng.choice(eleg, nzonas, replace=False)
    sel = np.zeros(len(ok), bool)
    for zq in zs:
        cand = np.where(ok & (P['zid'] == zq))[0]
        sel[rng.choice(cand, por_zona, replace=False)] = True
    n = P['nfin']
    mv = np.where(sel, np.rint(pts / 100 * n), 0)
    if sinal > 0:
        mv = np.minimum(mv, b['R2']); L2 = b['L2'] + mv
    else:
        mv = np.minimum(mv, b['L2']); L2 = b['L2'] - mv
    return L2.astype(float), sel, zs, float(mv.sum())


def parte_B():
    t0 = time.time()
    R = {'parte': 'B (F5, caudas com z recalibrado)'}
    P = f5_prepara()
    b = P['b']; n = P['nfin']
    L2 = b['L2'].astype(float)
    Z, zr, info, c = f5_principal(P, L2)
    try:
        ref = json.load(open(RAIZ + '/resultados/T7_T14_bweb.json'))['2026']['T14_com_grupos']['coef']
        R['conferencia_coeficientes_T8_dif_max'] = float(max(abs(Z['beta'][i] - ref[nm]) for i, nm in enumerate(P['nomes'])))
    except Exception as ex:  # noqa: BLE001
        R['conferencia_coeficientes_T8_dif_max'] = 'sem arquivo de referencia: ' + str(ex)
    R['coeficientes'] = {nm: float(Z['beta'][i]) for i, nm in enumerate(P['nomes'])}
    R['secoes_base'] = int(len(n)); R['sozinhas_no_local'] = int((P['m'] < 2).sum()); R['n_zero'] = int(((P['m'] >= 2) & (n <= 0)).sum())
    R['previsao_fora_de_0_n'] = int(((P['m'] >= 2) & (n > 0) & ~Z['ok']).sum())
    R['faixas_de_tamanho'] = [{'faixa': f'{lo} a {hi - 1}' if hi < 10 ** 9 else f'{lo} ou mais', **i} for (lo, hi), i in zip(FAIXAS_N, info)]
    R['principal'] = {k: v for k, v in c.items() if not k.startswith('_')}
    R['classificacao_pela_letra'] = classifica_f5(c)
    zok = zr[Z['ok']]
    R['distribuicao_z_recalibrado'] = {'dp': float(np.nanstd(zok)), 'quantis': {str(q): float(np.nanquantile(zok, q / 100)) for q in (0.1, 1, 5, 25, 50, 75, 95, 99, 99.9)},
                                       'acima_3': int((zok > 3).sum()), 'abaixo_3': int((zok < -3).sum()),
                                       'acima_5': int((zok > 5).sum()), 'abaixo_5': int((zok < -5).sum()),
                                       'acima_6': int((zok > 6).sum()), 'abaixo_6': int((zok < -6).sum())}
    # sensibilidades
    sens = {}
    ok = Z['ok']; p = Z['p']; fid = faixa_n_id(n)
    sens['previsao_entre_0,1_e_0,9'] = f5_conta(P, zr, ok & (p >= 0.1) & (p <= 0.9), Z['rl'])
    pid = np.clip(np.floor(np.nan_to_num(p, nan=0.0) * 5).astype(int), 0, 4)
    z2, _ = recalibra(Z['z'], ok, fid * 5 + pid, 20)
    sens['faixas_de_tamanho_x_previsao'] = f5_conta(P, z2, ok, Z['rl'])
    z3, info3 = recalibra(Z['pts'], Z['ok_pts'], fid, len(FAIXAS_N))
    sens['z_em_pontos'] = f5_conta(P, z3, Z['ok_pts'], Z['rl'])
    sens['z_em_pontos']['desvio_robusto_em_pontos_por_faixa'] = [i['desvio_robusto'] for i in info3]
    qs = np.quantile(n[ok], np.linspace(0, 1, 11)); did = np.clip(np.searchsorted(qs, n, side='right') - 1, 0, 9)
    z4, _ = recalibra(Z['z'], ok, did, 10)
    sens['faixas_por_decis_de_n'] = f5_conta(P, z4, ok, Z['rl'])
    sens['sem_exterior'] = f5_conta(P, zr, ok & ~P['zz'], Z['rl'])
    sens['n_50_ou_mais'] = f5_conta(P, zr, ok & (n >= 50), Z['rl'])
    Zd = f5_z(P, L2, modo='dentro'); zd, _ = recalibra(Zd['z'], Zd['ok'], fid, len(FAIXAS_N))
    sens['sem_deixar_de_fora'] = f5_conta(P, zd, Zd['ok'], Zd['rl'])
    sens['z_bruto_deixando_de_fora_sem_recalibrar'] = f5_conta(P, Z['z'], ok, Z['rl'])
    por_faixa = {}
    for j, (lo, hi) in enumerate(FAIXAS_N):
        por_faixa[f'{lo}-{hi if hi < 10 ** 9 else "mais"}'] = {k: v for k, v in f5_conta(P, zr, ok & (fid == j), Z['rl']).items() if k in ('secoes_com_z', 'acima', 'abaixo', 'razao')}
    sens['por_faixa_de_tamanho'] = por_faixa
    por_p = {}
    for j in range(5):
        por_p[f'{j / 5:.1f}-{(j + 1) / 5:.1f}'] = {k: v for k, v in f5_conta(P, zr, ok & (pid == j), Z['rl']).items() if k in ('secoes_com_z', 'acima', 'abaixo', 'razao')}
    sens['por_faixa_de_previsao'] = por_p
    R['sensibilidades'] = {k: ({kk: vv for kk, vv in v.items() if not kk.startswith('_')} if 'acima' in v else v) for k, v in sens.items()}
    por_uf = {}
    for uf in np.unique(b['uf']):
        mk = ok & (b['uf'] == uf)
        por_uf[str(uf)] = {'secoes': int(mk.sum()), 'acima': int((zr[mk] > 4).sum()), 'abaixo': int((zr[mk] < -4).sum())}
    R['por_uf'] = por_uf
    gravar('parcial_B.json', R)
    log('F5 bruto', c['acima'], c['abaixo'], c['razao'], R['classificacao_pela_letra'])

    # listas para auditoria
    def linha(i):
        return {'secao': str(b['chave'][i]), 'z_recalibrado': float(zr[i]), 'z_binomial': float(Z['z'][i]), 'residuo_pontos': float(Z['pts'][i]),
                'n': int(n[i]), 'L1': int(b['L1'][i]), 'R1': int(b['R1'][i]), 'L2': int(b['L2'][i]), 'R2': int(b['R2'][i]),
                'comp1': int(b['comp1'][i]), 'comp2': int(b['comp2'][i]), 'BN1': int(b['B1'][i] + b['N1'][i]), 'BN2': int(b['BN2'][i]),
                'previsto_p': float(Z['p'][i]), 'secoes_no_local': int(P['m'][i]), 'agregada': bool(b['agr'][i])}
    idx = np.where(ok)[0]
    cima = idx[np.argsort(-zr[idx], kind='stable')[:30]]; baixo = idx[np.argsort(zr[idx], kind='stable')[:10]]
    R['top30'] = [linha(i) for i in cima]; R['bot10'] = [linha(i) for i in baixo]
    try:
        ant = json.load(open(RAIZ + '/resultados/F5_caudas.json'))
        ja = {r['secao'] for r in ant.get('top30', []) + ant.get('bot10', [])}
        R['ja_conferidas_no_F5_original'] = {'top30': [r['secao'] for r in R['top30'] if r['secao'] in ja], 'bot10': [r['secao'] for r in R['bot10'] if r['secao'] in ja]}
    except Exception as ex:  # noqa: BLE001
        R['ja_conferidas_no_F5_original'] = 'sem arquivo: ' + str(ex)

    # calibração: caso plantado
    def roda(pts, por_zona, nzonas, nsort, base_sem, sinal=1):
        outs = []
        for i in range(nsort):
            rng = np.random.default_rng(base_sem + i)
            L2p, sel, zs, mv = f5_planta(P, Z, rng, pts, por_zona, nzonas, sinal)
            Zp, zrp, _, cp = f5_principal(P, L2p)
            cl = classifica_f5(cp)
            if sinal > 0:
                passam = int((sel & Zp['ok'] & (zrp > 4)).sum())
            else:
                passam = int((sel & Zp['ok'] & (zrp < -4)).sum())
            ntop = int(np.isin(zs, cp['_top10_ids']).sum()) if sinal > 0 else None
            outs.append({'acima': cp['acima'], 'abaixo': cp['abaixo'], 'razao': cp['razao'], 'pct_nas_10_zonas': cp['pct_nas_10_zonas'],
                         'classificacao': cl, 'plantadas_alem_de_4': passam, 'plantadas': int(sel.sum()),
                         'zonas_plantadas_entre_as_10': ntop, 'votos_movidos': mv, 'margem_plantada': 2 * mv})
        return outs
    ref = roda(5, 100, 10, 20, SEMENTE)
    nsin = sum(o['classificacao'] == 'SINAL' for o in ref)
    R['calibracao'] = {'referencia_+5pts_1000_secoes_10_zonas': {'sorteios': ref, 'sinal_em': nsin, 'de': len(ref),
                       'media_plantadas_alem_de_4': float(np.mean([o['plantadas_alem_de_4'] for o in ref])),
                       'media_zonas_plantadas_entre_as_10': float(np.mean([o['zonas_plantadas_entre_as_10'] for o in ref])),
                       'media_razao': float(np.mean([o['razao'] for o in ref])), 'media_margem_plantada': float(np.mean([o['margem_plantada'] for o in ref]))}}
    detectado = nsin >= 16
    R['caso_plantado_detectado'] = bool(detectado)
    gravar('parcial_B.json', R)
    log('F5 calibracao referencia: sinal em', nsin, 'de', len(ref))
    for nome, args in (('+10pts_1000_secoes_10_zonas', (10, 100, 10, 5, SEMENTE + 100)), ('+15pts_1000_secoes_10_zonas', (15, 100, 10, 5, SEMENTE + 200)),
                       ('+5pts_5000_secoes_50_zonas', (5, 100, 50, 5, SEMENTE + 300)), ('+10pts_5000_secoes_50_zonas', (10, 100, 50, 5, SEMENTE + 400))):
        o = roda(*args)
        R['calibracao'][nome] = {'sorteios': o, 'sinal_em': sum(x['classificacao'] == 'SINAL' for x in o), 'de': len(o),
                                 'media_plantadas_alem_de_4': float(np.mean([x['plantadas_alem_de_4'] for x in o])),
                                 'media_razao': float(np.mean([x['razao'] for x in o])), 'media_margem_plantada': float(np.mean([x['margem_plantada'] for x in o]))}
        log('F5 calibracao', nome, R['calibracao'][nome]['sinal_em'])
    o = roda(5, 100, 10, 5, SEMENTE + 500, sinal=-1)
    R['calibracao']['espelho_-5pts_1000_secoes_10_zonas'] = {'sorteios': o, 'media_plantadas_alem_de_-4': float(np.mean([x['plantadas_alem_de_4'] for x in o])),
                                                            'media_razao': float(np.mean([x['razao'] for x in o]))}
    R['veredito'] = R['classificacao_pela_letra'] if detectado else 'SEM PODER'
    R['segundos'] = round(time.time() - t0)
    gravar('parcial_B.json', R)
    log('parte B pronta', R['veredito'])


# ================================================================ PARTE C (linearidade)
def niveis_var(L1, n1, L2, n2, ids):
    """Variância ponderada (peso n2) da virada de cada unidade em torno da unidade de cima, nos quatro níveis.
    ids = dict(uf, mun, loc) de inteiros por seção. Devolve dict de variâncias (em fração ao quadrado)."""
    def pooled(g, G):
        a = np.bincount(g, weights=L2, minlength=G); bb = np.bincount(g, weights=n2, minlength=G)
        c = np.bincount(g, weights=L1, minlength=G); d = np.bincount(g, weights=n1, minlength=G)
        okk = (bb > 0) & (d > 0)
        return np.where(okk, a / np.where(bb > 0, bb, 1) - c / np.where(d > 0, d, 1), np.nan), bb
    nac = L2.sum() / n2.sum() - L1.sum() / n1.sum()
    s_uf, w_uf = pooled(ids['uf'], 27); s_mun, w_mun = pooled(ids['mun'], len(ids['uf_de_mun'])); s_loc, w_loc = pooled(ids['loc'], len(ids['mun_de_loc']))
    s_sec = L2 / n2 - L1 / n1
    out = {'virada_nacional': float(nac)}
    out['uf'] = float(np.nansum(w_uf * (s_uf - nac) ** 2) / w_uf.sum())
    out['uf_dp_simples'] = float(np.nanstd(s_uf))
    pm = ids['uf_de_mun']
    out['mun'] = float(np.nansum(w_mun * (s_mun - s_uf[pm]) ** 2) / w_mun.sum())
    pl = ids['mun_de_loc']
    out['loc'] = float(np.nansum(w_loc * (s_loc - s_mun[pl]) ** 2) / w_loc.sum())
    out['sec'] = float(np.sum(n2 * (s_sec - s_loc[ids['loc']]) ** 2) / n2.sum())
    out['_s'] = {'uf': s_uf, 'mun': s_mun, 'loc': s_loc}
    return out


def parte_C():
    from scipy.stats import chi2
    t0 = time.time()
    R = {'parte': 'C (linearidade, descritivo)', 'por_ano': {}}
    for a in ANOS:
        b = derivar(montar(a))
        n1 = (b['L1'] + b['R1']).astype(float); n2 = (b['L2'] + b['R2']).astype(float)
        m = b['apur'] & (b['uf'] != 'ZZ') & (n1 > 0) & (n2 > 0)
        s = {k: v[m] for k, v in b.items()}
        L1 = s['L1'].astype(float); L2 = s['L2'].astype(float); n1 = n1[m]; n2 = n2[m]
        ufs, iu = np.unique(s['uf'], return_inverse=True)
        _, im = np.unique(s['mun'], return_inverse=True)
        _, il = np.unique(s['loc1'], return_inverse=True)
        uf_de_mun = np.zeros(im.max() + 1, int); uf_de_mun[im] = iu
        mun_de_loc = np.zeros(il.max() + 1, int); mun_de_loc[il] = im
        ids = {'uf': iu, 'mun': im, 'loc': il, 'uf_de_mun': uf_de_mun, 'mun_de_loc': mun_de_loc}
        obs = niveis_var(L1, n1, L2, n2, ids)
        f1 = L1 / n1
        ra = {'secoes': int(m.sum()), 'municipios': int(im.max() + 1), 'locais': int(il.max() + 1),
              'virada_nacional_pontos': 100 * obs['virada_nacional'],
              'outros_sobre_validos_1t': float(s['O1'].sum() / (s['L1'].sum() + s['R1'].sum() + s['O1'].sum())),
              'dp_observado_pontos': {k: 100 * np.sqrt(obs[k]) for k in ('uf', 'mun', 'loc', 'sec')},
              'dp_simples_entre_ufs_pontos': 100 * obs['uf_dp_simples']}
        # (i) sorteio novo, um por nível
        rng = np.random.default_rng(SEMENTE + a)
        sim_i = {k: [] for k in ('uf', 'mun', 'loc', 'sec')}
        pais = {'uf': np.full(len(L1), obs['virada_nacional']), 'mun': obs['_s']['uf'][iu], 'loc': obs['_s']['mun'][im], 'sec': obs['_s']['loc'][il]}
        for rep in range(3):
            for k in ('uf', 'mun', 'loc', 'sec'):
                pp = np.clip(f1 + np.nan_to_num(pais[k], nan=obs['virada_nacional']), 0, 1)
                Ls = rng.binomial(n2.astype(np.int64), pp).astype(float)
                sim_i[k].append(niveis_var(L1, n1, Ls, n2, ids)[k])
        ra['dp_sorteio_novo_pontos'] = {k: 100 * np.sqrt(np.mean(v)) for k, v in sim_i.items()}
        ra['razao_var_observada_sobre_sorteio_novo'] = {k: obs[k] / np.mean(v) for k, v in sim_i.items()}
        # (ii) regra única nacional: taxas do D4-1 (eliminados somados) no universo com 2 ou mais seções por local
        Dn = Dado(b, universo(b, 2))
        beta, _ = Dn.mod.fit(Dn.Y)
        bL = np.clip(beta[:, 0], 0, 1); bR = np.clip(beta[:, 1], 0, 1)
        tot = bL + bR; esc = np.where(tot > 1, 1 / tot, 1.0); bL = bL * esc; bR = bR * esc
        ra['taxas_regra_unica'] = {x: {'para_L': float(bL[i]), 'para_R': float(bR[i])} for i, x in enumerate(NX)}
        X = np.column_stack([s[c] for c in NX]).astype(np.int64)
        X = np.maximum(X, 0)
        sim_ii = {k: [] for k in ('uf', 'mun', 'loc', 'sec')}; nac_ii = []
        for rep in range(3):
            Ls = np.zeros(len(L1)); Rs = np.zeros(len(L1))
            for j in range(6):
                mn = rng.multinomial(X[:, j], [bL[j], bR[j], max(0.0, 1 - bL[j] - bR[j])])
                Ls += mn[:, 0]; Rs += mn[:, 1]
            ns = Ls + Rs
            okk = ns > 0
            idk = {'uf': iu[okk], 'mun': im[okk], 'loc': il[okk], 'uf_de_mun': uf_de_mun, 'mun_de_loc': mun_de_loc}
            o2 = niveis_var(L1[okk], n1[okk], Ls[okk], ns[okk], idk)
            nac_ii.append(o2['virada_nacional'])
            for k in sim_ii:
                sim_ii[k].append(o2[k])
        ra['dp_regra_unica_pontos'] = {k: 100 * np.sqrt(np.mean(v)) for k, v in sim_ii.items()}
        ra['razao_var_observada_sobre_regra_unica'] = {k: obs[k] / np.mean(v) for k, v in sim_ii.items()}
        ra['virada_nacional_regra_unica_pontos'] = 100 * float(np.mean(nac_ii))
        # locais regulares demais (universo da parte A)
        Da = Dado(b, universo(b, 4))
        beta, E = Da.mod.fit(Da.Y)
        v = Da.mod.v(beta[:, 0]); g = Da.mod.g; k = np.bincount(g)
        okl = np.bincount(g, weights=(v <= 0).astype(float)) == 0
        T = np.bincount(g, weights=E[:, 0] ** 2 / np.where(v > 0, v, 1))
        q01 = chi2.ppf(0.01, k - 1); q05 = chi2.ppf(0.05, k - 1); q99 = chi2.ppf(0.99, k - 1)
        reg = {'locais': int(okl.sum()), 'obs_abaixo_1%': float((T[okl] < q01[okl]).mean()), 'obs_abaixo_5%': float((T[okl] < q05[okl]).mean()),
               'obs_acima_99%': float((T[okl] > q99[okl]).mean())}
        Xa = np.maximum(Da.mod.X.astype(np.int64), 0); bt = np.clip(beta[:, 0], 0, 1)
        s01, s05, s99, sphi = [], [], [], []
        for rep in range(2):
            Ls = np.zeros(Da.n)
            for j in range(Xa.shape[1]):
                Ls += rng.binomial(Xa[:, j], bt[j])
            b2, E2 = Da.mod.fit(Ls)
            v2 = Da.mod.v(b2[:, 0])
            T2 = np.bincount(g, weights=E2[:, 0] ** 2 / np.where(v2 > 0, v2, 1))
            s01.append(float((T2[okl] < q01[okl]).mean())); s05.append(float((T2[okl] < q05[okl]).mean())); s99.append(float((T2[okl] > q99[okl]).mean()))
            sphi.append(float(np.mean(E2[:, 0] ** 2 / np.where(v2 > 0, v2, 1) * Da.mod.kfac)))
        reg.update({'sim_abaixo_1%': float(np.mean(s01)), 'sim_abaixo_5%': float(np.mean(s05)), 'sim_acima_99%': float(np.mean(s99)),
                    'phi_no_dado_simulado': float(np.mean(sphi))})
        if a == 2026:
            pu = {}
            ufl = np.empty(len(k), dtype='U2'); ufl[g] = Da.uf
            for uf in np.unique(ufl):
                mk = okl & (ufl == uf)
                pu[str(uf)] = {'locais': int(mk.sum()), 'obs_abaixo_5%': float((T[mk] < q05[mk]).mean())}
            reg['por_uf_2026'] = pu
        ra['locais_regulares_demais'] = reg
        R['por_ano'][str(a)] = ra
        gravar('parcial_C.json', R)
        log('linearidade', a, ra['dp_observado_pontos'], ra['razao_var_observada_sobre_regra_unica'])
    R['segundos'] = round(time.time() - t0)
    gravar('parcial_C.json', R)


# ================================================================ EXPLORATÓRIO (escrito DEPOIS de ver os resultados das partes A, B e C)
def exploratorio_tudo():
    """Feito depois de ver o resultado; só pistas e réguas internas a mais, sem veredito.
    E0 conferência interna dos coeficientes com lib.fe_ols; E1 piso multinomial do "phi de troca" e teto interno;
    E2 anatomia das caudas da parte A; E3 seções com Lula acima e Flávio abaixo ao mesmo tempo (lista para auditoria);
    E4 varredura por zona eleitoral (onde o reteste do F5 não tem poder), calibrada com o mesmo caso plantado."""
    from lib import fe_ols
    t0 = time.time()
    A = json.load(open(TRAB + '/parcial_A.json'))
    phi_ref = A['phi_ref_mediana_placebo']
    phiR_ref = float(np.median([A['por_ano'][str(a)]['phi_R2'] for a in PLACEBO]))
    out = {'aviso': 'tudo aqui foi escrito e calculado depois de ver os resultados das partes A, B e C', 'phi_R2_ref': phiR_ref}
    bases = {a: derivar(montar(a)) for a in ANOS}
    piso = {}; anat = {}; par = {}; zon = {}
    guard = {}
    for a in ANOS:
        b = bases[a]; D = Dado(b, universo(b, 4))
        beta, E = D.mod.fit(D.Y)
        V = [D.mod.v(beta[:, j]) for j in range(4)]
        kf = D.mod.kfac
        if a == 2026:
            r = fe_ols(D.Y[:, 0], D.mod.X, D.s['loc1'], 1.0 / D.s['apt1'], NX)
            out['E0_conferencia_interna'] = {'dif_max_coeficientes_contra_lib_fe_ols': float(max(abs(r['coef'][x] - beta[i, 0]) for i, x in enumerate(NX))),
                                             'n': r['n'], 'phi_recalculado': float(np.mean(E[:, 0] ** 2 / V[0] * kf))}
        bL = np.clip(beta[:6, 0], 0, 1); bR = np.clip(beta[:6, 1], 0, 1)
        p_i = (D.mod.X[:, :6] @ (bL * bR)) / V[0]
        tro = -(E[:, 0] * E[:, 1] / V[0] * kf)
        piso[str(a)] = {'phi_de_troca': float(tro.mean()), 'piso_multinomial': float(p_i.mean()), 'excesso': float(tro.mean() - p_i.mean()),
                        'phi': float(np.mean(E[:, 0] ** 2 / V[0] * kf)), 'excesso_de_phi_sobre_1': float(np.mean(E[:, 0] ** 2 / V[0] * kf) - 1)}
        u = E[:, 0] / np.sqrt(V[0] * phi_ref); uR = E[:, 1] / np.sqrt(V[1] * phiR_ref)
        an = {}
        for nome, mk in (('direita', u > 3), ('esquerda', u < -3)):
            an[nome] = {'secoes': int(mk.sum()), 'media_e_L': float(E[mk, 0].mean()), 'media_e_R': float(E[mk, 1].mean()),
                        'media_e_BN': float(E[mk, 2].mean()), 'media_e_abstencao': float(E[mk, 3].mean()),
                        'soma_e_L': float(E[mk, 0].sum()), 'soma_e_R': float(E[mk, 1].sum())}
        an['saldo_votos_L_nas_duas_caudas'] = an['direita']['soma_e_L'] + an['esquerda']['soma_e_L']
        for lim in (2.5, 4.0):
            an[f'razao_caudas_limiar_{lim:g}'] = float((u > lim).sum() / max((u < -lim).sum(), 1)); an[f'n_limiar_{lim:g}'] = [int((u > lim).sum()), int((u < -lim).sum())]
        anat[str(a)] = an
        fav = (u > 3) & (uR < -3); con = (u < -3) & (uR > 3)
        par[str(a)] = {'lula_acima_e_adversario_abaixo': int(fav.sum()), 'lula_abaixo_e_adversario_acima': int(con.sum()),
                       'razao': float(fav.sum() / max(con.sum(), 1)), 'por_100_mil_secoes': [float(1e5 * fav.mean()), float(1e5 * con.mean())],
                       'limiar_2,5': [int(((u > 2.5) & (uR < -2.5)).sum()), int(((u < -2.5) & (uR > 2.5)).sum())]}
        if a == 2026:
            s = D.s
            por_uf = {}
            for uf in np.unique(D.uf):
                m = D.uf == uf
                por_uf[str(uf)] = [int((u[m] > 3).sum()), int((u[m] < -3).sum()), int(fav[m].sum()), int(con[m].sum())]
            out['E2_caudas_2026_por_uf_[direita, esquerda, par a favor de Lula, par a favor de Flávio]'] = por_uf
            idx = np.where(fav)[0]; idx = idx[np.argsort(-(u[idx] - uR[idx]))][:40]
            out['E3_lista_2026_lula_acima_e_flavio_abaixo'] = [
                {'secao': str(s['chave'][i]), 'u_L': float(u[i]), 'u_R': float(uR[i]), 'e_L': float(E[i, 0]), 'e_R': float(E[i, 1]), 'e_BN': float(E[i, 2]), 'e_abst': float(E[i, 3]),
                 'L1': int(s['L1'][i]), 'R1': int(s['R1'][i]), 'L2': int(s['L2'][i]), 'R2': int(s['R2'][i]), 'comp1': int(s['comp1'][i]), 'comp2': int(s['comp2'][i]),
                 'BN1': int(s['B1'][i] + s['N1'][i]), 'BN2': int(s['BN2'][i]), 'secoes_no_local': int(D.mod.k_loc[i]), 'agregada': bool(s['agr'][i])} for i in idx]
            idx = np.where(con)[0]; idx = idx[np.argsort(u[idx] - uR[idx])][:15]
            out['E3_lista_2026_espelho_flavio_acima_e_lula_abaixo'] = [
                {'secao': str(s['chave'][i]), 'u_L': float(u[i]), 'u_R': float(uR[i]), 'e_L': float(E[i, 0]), 'e_R': float(E[i, 1]),
                 'L1': int(s['L1'][i]), 'R1': int(s['R1'][i]), 'L2': int(s['L2'][i]), 'R2': int(s['R2'][i]), 'comp1': int(s['comp1'][i]), 'comp2': int(s['comp2'][i])} for i in idx]
        if a in (2022, 2026):
            zs, zi = np.unique(D.s['zona'], return_inverse=True)
            nz = np.bincount(zi)
            zphi = np.bincount(zi, weights=E[:, 0] ** 2 / V[0] * kf) / nz; ztro = np.bincount(zi, weights=tro) / nz
            zon[a] = {str(z): (int(nz[j]), float(zphi[j]), float(ztro[j])) for j, z in enumerate(zs)}
            guard[a] = (D, zi, zs, nz)
    out['E1_piso_multinomial_do_phi_de_troca'] = piso
    out['E2_anatomia_das_caudas'] = anat
    out['E3_pares_lula_acima_adversario_abaixo'] = par
    # E1: teto interno pela parte espelhada (base = piso multinomial de 2026; e base = excesso de 2022)
    cal = A['calibracao_troca']['2026']; tro26 = piso['2026']['phi_de_troca']
    teto = {}
    for f in (10, 30, 50, 70, 90):
        ds = np.array([0.25, 0.5, 1.0])
        dl = np.array([cal[f'dose{d:g}_f{f}']['phi_de_troca'] - tro26 for d in ds])
        M = np.column_stack([ds, ds ** 2]); co, *_ = np.linalg.lstsq(M, dl, rcond=None)
        a_, c_ = float(co[0]), float(co[1])
        if a_ < 0:
            a_ = 0.0; c_ = float((dl * ds ** 2).sum() / (ds ** 4).sum())
        if c_ < 0:
            c_ = 0.0; a_ = float((dl * ds).sum() / (ds ** 2).sum())
        linha = {'subidas_medidas_do_phi_de_troca': {f'{d:g}': float(x) for d, x in zip(ds, dl)}}
        for nb, folga in (('base_piso_multinomial', piso['2026']['excesso']), ('base_excesso_de_2022', piso['2026']['excesso'] - piso['2022']['excesso']),
                          ('base_menor_excesso_placebo', piso['2026']['excesso'] - min(piso[str(x)]['excesso'] for x in PLACEBO))):
            if folga <= 0:
                dmax = 0.0
            elif c_ > 0:
                dmax = (-a_ + np.sqrt(a_ ** 2 + 4 * c_ * folga)) / (2 * c_)
            else:
                dmax = folga / a_ if a_ > 0 else float('nan')
            pp = dmax * P_DOSE
            mov = pp / (1 - pp) * R2_OFICIAL
            linha[nb] = {'folga': float(folga), 'dose_maxima': float(dmax), 'pct_da_margem': float(100 * 2 * mov / MARGEM)}
        teto[f'{f}%'] = linha
    out['E1_teto_interno_pela_parte_espelhada'] = teto
    gravar('parcial_exploratorio.json', out)
    # E4: varredura por zona (2026), com 2022 ao lado e o caso plantado do F5 (+5 pontos em 100 seções de cada uma de 10 zonas)
    D, zi, zs, nz = guard[2026]
    z26 = zon[2026]; z22 = zon[2022]
    gr = [(z, v) for z, v in z26.items() if v[0] >= 100]
    arr_phi = np.array([v[1] for _, v in gr]); arr_tro = np.array([v[2] for _, v in gr])
    e4 = {'zonas_com_100_ou_mais_secoes': len(gr),
          'phi_por_zona_quantis': {str(q): float(np.quantile(arr_phi, q / 100)) for q in (1, 5, 25, 50, 75, 95, 99, 100)},
          'phi_de_troca_por_zona_quantis': {str(q): float(np.quantile(arr_tro, q / 100)) for q in (1, 5, 25, 50, 75, 95, 99, 100)}}
    top = sorted(gr, key=lambda x: -x[1][2])[:20]
    e4['top20_zonas_por_phi_de_troca'] = [{'zona': z, 'secoes': v[0], 'phi': v[1], 'phi_de_troca': v[2],
                                           'em_2022': ({'secoes': z22[z][0], 'phi': z22[z][1], 'phi_de_troca': z22[z][2]} if z in z22 else None)} for z, v in top]
    com = [(z, v[2], z22[z][2]) for z, v in gr if z in z22 and z22[z][0] >= 100]
    d26 = np.array([c[1] for c in com]); d22 = np.array([c[2] for c in com])
    e4['zonas_nos_dois_anos'] = len(com)
    e4['correlacao_phi_de_troca_2026_x_2022_por_zona'] = float(np.corrcoef(d26, d22)[0, 1])
    e4['zonas_com_phi_de_troca_2026_acima_do_dobro_de_2022_e_acima_de_1,5'] = [{'zona': c[0], '2026': c[1], '2022': c[2]} for c in com if c[1] > 2 * c[2] and c[1] > 1.5]
    S = D.s; nfin = (S['L2'] + S['R2']).astype(float)
    eleg = np.where(nz >= 200)[0]
    cals = []
    for i in range(5):
        rng = np.random.default_rng(SEMENTE + 700 + i)
        zsel = rng.choice(eleg, 10, replace=False)
        sel = np.zeros(D.n, bool)
        for zq in zsel:
            cand = np.where(zi == zq)[0]; sel[rng.choice(cand, 100, replace=False)] = True
        linha = {}
        for pts in (3, 5):
            mv = np.minimum(np.where(sel, np.rint(pts / 100 * nfin), 0), S['R2'])
            Y = y_troca(D, mv)
            beta, E = D.mod.fit(Y)
            v0 = D.mod.v(beta[:, 0])
            tro = -(E[:, 0] * E[:, 1] / v0 * D.mod.kfac)
            ztro = np.bincount(zi, weights=tro) / nz
            grande = nz >= 100
            ordem = np.argsort(-np.where(grande, ztro, -9))
            rank = {int(z): int(np.where(ordem == z)[0][0]) + 1 for z in zsel}
            linha[f'+{pts}pts'] = {'phi_de_troca_das_zonas_plantadas': [float(ztro[z]) for z in zsel], 'posicoes_no_ranking': sorted(rank.values()),
                                   'entre_as_10_primeiras': int(sum(r <= 10 for r in rank.values())), 'entre_as_20_primeiras': int(sum(r <= 20 for r in rank.values())),
                                   'margem_plantada': float(2 * mv.sum())}
        cals.append(linha)
    e4['calibracao_caso_plantado_100_secoes_em_cada_uma_de_10_zonas'] = cals
    out['E4_varredura_por_zona'] = e4
    # E5: limite do teste da parte A: a mesma dose inteira aplicada a 30% dos LOCAIS inteiros, ou a 30% das ZONAS inteiras
    e5 = {}
    R2 = S['R2']; phi0 = piso['2026']['phi']
    for nome, gid, sem in (('30%_dos_locais_inteiros', D.mod.g, 801), ('30%_das_zonas_inteiras', zi, 802)):
        rng = np.random.default_rng(SEMENTE + sem)
        selg = rng.random(int(gid.max() + 1)) < 0.30
        sel = selg[gid]
        pc = P_DOSE * R2.sum() / R2[sel].sum()
        mov = np.where(sel, rng.binomial(R2, pc), 0)
        beta, E = D.mod.fit(y_troca(D, mov))
        v0 = D.mod.v(beta[:, 0])
        ph = float(np.mean(E[:, 0] ** 2 / v0 * D.mod.kfac))
        e5[nome] = {'votos_movidos': int(mov.sum()), 'phi': ph, 'fator_sobre_bruto': ph / phi0, 'fracao_das_secoes': float(sel.mean())}
    out['E5_troca_por_local_ou_zona_inteira'] = e5
    out['segundos'] = round(time.time() - t0)
    gravar('parcial_exploratorio.json', out)
    log('exploratorio pronto', round(time.time() - t0))


# ================================================================ saída
def fn(x, nd=2, sinal=False):
    if x is None:
        return 'n/d'
    if isinstance(x, float) and (np.isnan(x) or np.isinf(x)):
        return 'inf' if np.isinf(x) else 'n/d'
    s = f'{x:+,.{nd}f}' if sinal else f'{x:,.{nd}f}'
    return s.replace(',', 'X').replace('.', ',').replace('X', '.')


def fi(x):
    return f'{int(round(x)):,}'.replace(',', '.')


def final():
    A = json.load(open(TRAB + '/parcial_A.json')); B = json.load(open(TRAB + '/parcial_B.json')); C = json.load(open(TRAB + '/parcial_C.json'))
    extra = {}
    if os.path.exists(TRAB + '/parcial_exploratorio.json'):
        extra = json.load(open(TRAB + '/parcial_exploratorio.json'))
    out = {'teste': 'R27_B6: vizinho de sala (D4-5) e caudas (F5 recalibrado), com o descritivo da linearidade',
           'registro': 'PRE-REGISTRO-2026-10-26.md, Adendo 27 (commit 2748895) e Adendo 30 (commit a7218fb); registro/adendo27/desenho_D4_proposta.json (D4-5) e equipe_vermelha_relatorio.json (F5)',
           'script': 'scripts/analisar_R27_B6.py', 'docstring_antes_de_rodar': TRAB + '/docstring_antes_de_rodar.txt',
           'veredito': {'A_D4-5': A.get('veredito'), 'A_D4-5_pela_letra_bruto': A.get('veredito_pela_letra_bruto'),
                        'B_F5': B.get('veredito'), 'B_F5_classificacao_pela_letra': B.get('classificacao_pela_letra'),
                        'C_linearidade': 'descritivo, sem veredito'},
           'parte_A': A, 'parte_B': B, 'parte_C': C}
    if extra:
        out['exploratorio_depois_de_ver_o_resultado'] = extra
    out = _finito(out)
    with open(SAIDA_JSON, 'w') as f:
        json.dump(out, f, ensure_ascii=False, indent=1, allow_nan=False)
    txt = texto(out)
    with open(SAIDA_TXT, 'w') as f:
        f.write(txt)
    print(txt)


def _finito(o):
    if isinstance(o, dict):
        return {k: _finito(v) for k, v in o.items()}
    if isinstance(o, list):
        return [_finito(v) for v in o]
    if isinstance(o, float) and (np.isnan(o) or np.isinf(o)):
        return 'sem limite' if np.isnan(o) else 'infinito'
    return o


def texto(o):
    A, B, C = o['parte_A'], o['parte_B'], o['parte_C']
    X = o.get('exploratorio_depois_de_ver_o_resultado', {})
    AN = ('2014', '2018', '2022', '2026')
    L = []
    w = L.append
    pr = A['primaria']; pa = A['por_ano']; cl = A['clausulas_bruto']; po = A['poder']; cal = A['calibracao_troca']['2026']
    p = B['principal']; ca = B['calibracao']; rf = ca['referencia_+5pts_1000_secoes_10_zonas']
    w('R27_B6 (Adendo 27, última onda): VIZINHO DE SALA (D4-5) E CAUDAS (F5 RECALIBRADO), COM O DESCRITIVO DA LINEARIDADE')
    w('Registro: Adendo 27 (commit 2748895, 10/11/2026 00:16:42 UTC) e Adendo 30 (commit a7218fb). Script: scripts/analisar_R27_B6.py.')
    w('Docstring com as decisões gravado antes de qualquer conta com votos: ' + o['docstring_antes_de_rodar'] + '.')
    w('O script com esse docstring entrou no repositório no commit 03fac40 (10/11/2026 13:23:32 UTC); a primeira conta com votos começou às 13:24:50 UTC.')
    w('Depois disso mudaram só a função do exploratório, as funções de saída e três linhas do teto em votos (onde o plantio não move phi, o teto sai')
    w('"sem limite" em vez de zero). As contas das partes A, B e C são as do commit; a parte A foi rodada duas vezes e deu os mesmos números.')
    w('O desenho D4-5 é cego. O reteste do F5 foi escrito por quem já conhecia o resultado antigo. A parte C é descritiva, sem critério registrado.')
    w('')
    w('VEREDITOS PELA LETRA')
    w(f"- A, D4-5 (troca aplicada só a parte das urnas de um mesmo local): {A['veredito']}, com poder. phi de 2026 = {fn(pr['phi_2026'], 3)}; maior placebo = {fn(pr['maior_placebo'], 3)};")
    w(f"  razão {fn(pr['razao'], 3)} (limite do sem sinal 1,15; do sinal 1,5); caudas {fn(pa['2026']['razao_caudas'], 2)} (faixa do sem sinal 0,67 a 1,5). O cenário de referência plantado")
    w(f"  (dose inteira em 30% das urnas) multiplica phi por {fn(po['fator_cenario_referencia'], 2)} e dá {po['veredito_com_referencia_plantada']} pela letra. O veredito depende só da comparação com 2014, 2018 e 2022.")
    w(f"- B, F5 (caudas com z recalibrado): {B['veredito']}. Pela letra seria {B['classificacao_pela_letra']} ({fi(p['acima'])} acima de +4 contra {fi(p['abaixo'])} abaixo de -4, razão {fn(p['razao'], 2)}),")
    w(f"  mas o caso plantado (+5 pontos em 1.000 seções de 10 zonas) foi detectado em {rf['sinal_em']} de {rf['de']} sorteios: o critério não enxerga o que deveria enxergar.")
    w('- C, linearidade: descritivo, sem veredito. Não apareceu regularidade maior que o acaso em nenhum ano; 2026 fica ao lado de 2022.')
    w('Cláusulas com veredito nesta rodada: 2 (A e B). Sinais pela letra: 0. Com 2 cláusulas o acaso daria menos de 1 sinal.')
    w('')
    # ---------------- A
    w('PARTE A. D4-5, DISPERSÃO DA PASSAGEM ENTRE TURNOS DENTRO DO MESMO LOCAL')
    w('Universo: filtros do D4-1, locais com 4 ou mais seções válidas. Resíduo da equação de L2 (efeito fixo de local, peso 1/aptos, eliminados')
    w('somados). phi = média de e2/v com k/(k-1); phi = 1 seria só o acaso binomial das transições. "Espelhada em R" = parte da dispersão de')
    w('Lula que aparece com sinal trocado em Flávio (a marca de troca); "em abstenção" = a que aparece no comparecimento.')
    w('  ano    seções   locais  dp do resíduo   phi (ep)         phi R2   phi BN2  phi A2   phi de troca  espelhada em R  em abstenção  em BN')
    for a in AN:
        r = pa[a]
        w(f"  {a}  {fi(r['n']):>8} {fi(r['locais']):>7}   {fn(r['dp_residuo_votos'], 2)} votos   {fn(r['phi'], 3)} ({fn(r['ep_phi'], 3)})   {fn(r['phi_R2'], 3)}    {fn(r['phi_BN2'], 3)}    {fn(r['phi_A2'], 3)}    {fn(r['phi_de_troca'], 3)}         {fn(100 * r['parcela_espelhada_em_R'], 1)}%         {fn(100 * r['parcela_em_abstencao'], 1)}%       {fn(100 * r['parcela_em_BN'], 1)}%")
    w(f"Primária: phi de 2026 = {fn(pr['phi_2026'], 3)} (ep {fn(pr['ep_phi_2026'], 3)}; n = {fi(pa['2026']['n'])} seções em {fi(pa['2026']['locais'])} locais e {fi(pa['2026']['municipios'])} municípios).")
    w(f"  Dividido pelo maior placebo (2014, {fn(pr['maior_placebo'], 3)}): {fn(pr['razao'], 3)} (ep {fn(pr['ep_razao'], 3)}; IC 95% {fn(pr['ic95_razao'][0], 3)} a {fn(pr['ic95_razao'][1], 3)}).")
    w('  Contra cada ano: ' + '; '.join(f"{a}: {fn(pr['phi_2026'] / pr['phi_placebo'][a], 3)}" for a in ('2014', '2018', '2022')) + f". Os placebos variam {fn(cl['max_sobre_min_placebo'], 2)} vez entre si (limite 1,5).")
    w(f"  Valor bruto de 2026, sem outro ano: phi {fn(pr['phi_2026'], 3)}, isto é, {fn(100 * (pr['phi_2026'] - 1), 0)}% acima do acaso binomial; resíduo de {fn(pa['2026']['dp_residuo_votos'], 2)} votos por seção.")
    w(f"Caudas (u = e/raiz(v phi_ref), phi_ref = {fn(A['phi_ref_mediana_placebo'], 3)}; direita = Lula acima do previsto) e mistura de duas normais com variância comum:")
    w('  ano    direita > 3      esquerda < -3     razão (IC 95%)        mistura: fração alta   separação (pontos dos válidos)   votos implicados')
    for a in AN:
        r = pa[a]; mx = r['mistura']
        fora = '' if 0.05 <= mx['pi_alto'] <= 0.95 else ' (fração fora de 5% a 95%: só isola a ponta)'
        w(f"  {a}   {fn(100 * r['cauda_direita'], 3)}% ({r['n_direita']})   {fn(100 * r['cauda_esquerda'], 3)}% ({r['n_esquerda']})   {fn(r['razao_caudas'], 2)} ({fn(r['ic95_razao_caudas'][0], 2)} a {fn(r['ic95_razao_caudas'][1], 2)})    {fn(100 * mx['pi_alto'], 2)}%                 {fn(mx['delta_pp'], 2)}                            {fi(mx['votos_implicados'])}{fora}")
    ml = pa['2026']['mistura_variancias_livres']
    w(f"  Mistura com variâncias livres em 2026: fração {fn(100 * ml['pi_alto'], 1)}%, separação {fn(ml['delta_pp'], 2)} ponto (duas larguras, sem dois grupos separados).")
    w(f"Cláusulas em 2026: phi >= 1,5 x placebo: {'sim' if cl['sinal_phi_1,5'] else 'não'}; cauda de um lado 3 x a do outro: {'sim' if cl['sinal_cauda_3x'] else 'não'}; mistura com 2 pontos e fração de 5% a 95%: {'sim' if cl['sinal_mistura_2pp_5a95'] else 'não'}; votos implicados >= 550 mil: {'sim' if cl['sinal_votos_550mil'] else 'não'};")
    w(f"  phi <= 1,15 x placebo: {'sim' if cl['semsinal_phi_1,15'] else 'não'}; caudas entre 0,67 e 1,5: {'sim' if cl['semsinal_caudas_0,67_a_1,5'] else 'não'}. Pela letra: {A['veredito_pela_letra_bruto']}.")
    e = A['espelho_outras_equacoes']
    w('Espelho e controles, razão de 2026 sobre o maior placebo: equação de Flávio (R2) ' + fn(e['phi_R2']['razao_2026_sobre_maior_placebo'], 2) + '; branco e nulo ' + fn(e['phi_BN2']['razao_2026_sobre_maior_placebo'], 2)
      + '; abstenção ' + fn(e['phi_A2']['razao_2026_sobre_maior_placebo'], 2) + '; phi de troca ' + fn(e['phi_de_troca']['razao_2026_sobre_maior_placebo'], 2)
      + f" (IC 95% {fn(e['phi_de_troca']['ic95_razao'][0], 2)} a {fn(e['phi_de_troca']['ic95_razao'][1], 2)}); phi pela razão das somas " + fn(e['phi_razao_das_somas']['razao_2026_sobre_maior_placebo'], 2) + '; phi robusto ' + fn(e['phi_robusto']['razao_2026_sobre_maior_placebo'], 2) + '.')
    v = A['variantes']
    w('Variantes de 2026 (phi): sem seções agregadas ' + fn(v['v1_2026_sem_agregadas']['phi'], 3) + '; eliminados separados ' + fn(v['v2_2026_eliminados_separados']['phi'], 3)
      + '; com covariáveis de perfil ' + fn(v['v3_2026_com_covariaveis_de_perfil']['phi'], 3) + ' contra ' + fn(v['v3_2026_mesmo_universo_sem_covariaveis']['phi'], 3) + f" no mesmo universo ({v['v3_secoes_sem_perfil_fora']} seções sem perfil fora).")
    w('  O perfil (idade, escolaridade, gênero) NÃO reduz a dispersão de 2026: a explicação inocente do desenho não é o que sustenta o phi acima de 1.')
    w('  Coeficientes próprios de cada UF, phi: ' + '; '.join(f"{a} {fn(v['v4_coeficientes_por_uf'][a]['phi'], 3)}" for a in AN) + f"; razão {fn(v['v4_coeficientes_por_uf']['razao_2026_sobre_maior_placebo'], 3)}.")
    w('  Locais com 2 ou mais seções, phi: ' + '; '.join(f"{a} {fn(v['v5_locais_com_2_ou_mais'][a]['phi'], 3)}" for a in AN) + f"; razão {fn(v['v5_locais_com_2_ou_mais']['razao_2026_sobre_maior_placebo'], 3)}.")
    g = A['placebo_governador']
    w('Placebo contemporâneo, que não depende de outro ano (governador nas mesmas urnas, mesmo dia, regressão dentro da UF):')
    for uf, r in g['por_uf'].items():
        w(f"  {uf}: {fi(r['n'])} seções; phi governador {fn(r['phi_governador'], 3)}; phi presidente {fn(r['phi_presidente'], 3)}; razão {fn(r['razao_pres_sobre_gov'], 2)}; phi de troca governador {fn(r['phi_de_troca_governador'], 3)}, presidente {fn(r['phi_de_troca_presidente'], 3)}")
    s6 = g['seis_ufs']
    w(f"  6 UFs juntas: {fi(s6['n'])} seções; phi governador {fn(s6['phi_governador'], 3)}; phi presidente {fn(s6['phi_presidente'], 3)}; razão {fn(s6['razao_pres_sobre_gov'], 2)}; no phi de troca, razão {fn(s6['razao_phi_de_troca'], 2)}.")
    w('  Leitura escrita antes: 1,5 ou mais iria no sentido da tese; 1,15 ou menos, não. Só o TO fica entre os dois (e lá o phi de troca do presidente é menor que o do governador).')
    w('phi por UF em 2026 (entre parênteses, a razão sobre o maior placebo da mesma UF): ' + '; '.join(f"{uf} {fn(r['phi_2026'], 2)} ({fn(r['razao_sobre_maior_placebo'], 2)})" for uf, r in A['phi_por_uf'].items()) + '.')
    mxuf = max(A['phi_por_uf'].items(), key=lambda kv: kv[1]['razao_sobre_maior_placebo'])
    w(f"  Nenhuma UF passa de 1,15; a maior razão é {mxuf[0]} com {fn(mxuf[1]['razao_sobre_maior_placebo'], 2)}.")
    w('')
    w('Calibração: troca plantada por cima de 2026 (dose inteira = 3,57% dos votos de Flávio do universo, em votos movidos)')
    w('  dose   urnas   votos movidos   phi      fator   razão sobre placebo   caudas   fração alta   separação   votos implicados   espelhada em R   pela letra')
    for k, r in cal.items():
        mx = r['mistura']
        w(f"  {fn(r['dose'], 2):>5}  {fn(100 * r['fracao_urnas'], 0):>4}%   {fi(r['votos_movidos']):>10}   {fn(r['phi'], 3):>6}   {fn(r['fator_sobre_bruto'], 3)}      {fn(r['clausulas']['razao_phi_sobre_maior_placebo'], 3)}            {fn(r['razao_caudas'], 2):>5}     {fn(100 * mx['pi_alto'], 1):>5}%       {fn(mx['delta_pp'], 2):>5}      {fi(mx['votos_implicados']) if 0.05 <= mx['pi_alto'] <= 0.95 else 'fora de 5 a 95%':>15}      {fn(100 * r['parcela_espelhada_em_R'], 1)}%       {r['veredito_pela_letra_com_plantio']}")
    w('  Por cima de 2022 (letra do desenho), fator: ' + '; '.join(f"{fn(r['dose'], 1)} dose em {fn(100 * r['fracao_urnas'], 0)}%: {fn(r['fator_sobre_bruto'], 2)}" for k, r in A['calibracao_troca']['2022'].items()) + '.')
    rep = A['calibracao_referencia_5_sorteios']
    w('  Cenário de referência repetido com 5 sementes: fator ' + ', '.join(fn(x['fator_sobre_bruto'], 3) for x in rep) + '; votos implicados pela mistura ' + ', '.join(fi(x['votos_implicados']) for x in rep) + f" (plantados {fi(rep[0]['votos_movidos'])}: a mistura recupera cerca de {fn(100 * np.mean([x['votos_implicados'] / x['votos_movidos'] for x in rep]), 0)}%).")
    w('  O que o SEM SINAL exclui (cenários que, plantados por cima de 2026, tiram o resultado do sem sinal): dose inteira em até 50% das urnas, meia dose em até 50%,')
    w('  um quarto de dose em até 30%. O que NÃO exclui (continuaria SEM SINAL com a fraude plantada): dose inteira em 70% das urnas ou mais, meia dose em 70% ou mais,')
    w('  um quarto de dose em 50% ou mais, e qualquer troca igual em todas as urnas. O desenho prometia excluir a dose inteira em até 70%: no dado real o alcance é até 50%.')
    w('  (Meia dose em 50% e um quarto de dose em 30% saem do sem sinal só pela cláusula das caudas, que em 2026 já parte de 1,38; o fator de phi neles é menor que 1,15.)')
    w('  Sinal pela letra só com: ' + '; '.join(f"{fn(cal[k]['dose'], 2)} dose em {fn(100 * cal[k]['fracao_urnas'], 0)}% das urnas" for k in po['cenarios_que_dao_SINAL_pela_letra']) + '.')
    for nome, tit in (('espelho_plantado_L_para_R', 'Espelho plantado (mesmos votos, de Lula para Flávio, 30% das urnas)'), ('inocente_I1_mobilizacao_desigual', 'Explicação inocente I1 (mobilização desigual: faltosos que entram em 30% das seções, 2/3 para Lula)'),
                      ('inocente_I2_conversao_por_perfil', 'Explicação inocente I2 (destino dos eleitores de eliminados conforme a idade da seção)')):
        r = A[nome]; mx = r['mistura']
        w(f"{tit}: phi {fn(r['phi'], 3)} (fator {fn(r['fator_sobre_bruto'], 3)}); caudas {fn(r['razao_caudas'], 2)}; mistura {fn(100 * mx['pi_alto'], 1)}% e {fn(mx['delta_pp'], 2)} pontos; espelhada em R {fn(100 * r['parcela_espelhada_em_R'], 1)}%; phi de troca vezes {fn(r['fator_phi_de_troca'], 2)}; pela letra {r['veredito_pela_letra_com_plantio']}.")
    ab = A['absorcao_pelas_covariaveis']
    w('  Quanto as covariáveis de perfil absorvem da subida de phi: troca ' + fn(100 * ab['troca_referencia']['fracao_absorvida_pelas_covariaveis'], 1) + '%; I1 ' + fn(100 * ab['I1']['fracao_absorvida_pelas_covariaveis'], 1) + '%; I2 ' + fn(100 * ab['I2']['fracao_absorvida_pelas_covariaveis'], 1) + '%.')
    w('  Leitura da calibração: o critério registrado NÃO separa troca em parte das urnas de mobilização desigual entre seções (I1 também daria SINAL). O que separa é a')
    w('  parte espelhada em Flávio: sobe para cerca de 76% com a troca e cai abaixo de zero com a mobilização. Em 2026 ela é ' + fn(100 * pa['2026']['parcela_espelhada_em_R'], 1) + '%, contra ' + fn(100 * pa['2022']['parcela_espelhada_em_R'], 1) + '% em 2022.')
    t = A['traducao_em_votos']
    w('Tradução em votos de margem:')
    w(f"  Mistura de 2026: {fi(t['votos_implicados_mistura_universo'])} votos no universo ({fi(t['votos_implicados_mistura_extrapolado_pais'])} extrapolando ao país); margem {fi(2 * t['votos_implicados_mistura_extrapolado_pais'])} = {fn(100 * 2 * t['votos_implicados_mistura_extrapolado_pais'] / MARGEM, 1)}% de 4.430.191. O limiar era 550 mil.")
    w('  Teto lido inteiro a favor da tese: maior troca em parte das urnas cuja dispersão caberia na folga de phi, em % da margem (não é estimativa):')
    w('  urnas atingidas   folga sobre o acaso binomial (phi - 1)   folga sobre 2022 (menor placebo)   sobre a mediana ou o maior placebo')
    for f, r in t['teto_por_fracao_de_urnas'].items():
        def cel(x):
            return fn(x['pct_da_margem'], 1) + '%' if isinstance(x['pct_da_margem'], (int, float)) else 'sem limite (o teste não enxerga)'
        w(f"  {f:>6}             {cel(r['binomial_1']):>30}           {cel(r['menor_placebo']):>30}       {cel(r['mediana_placebo'])}")
    w('')
    # ---------------- B
    w('PARTE B. F5, CAUDAS COM z RECALIBRADO (previsão deixando a seção de fora; desvio robusto por faixa de tamanho)')
    w(f"Base: {fi(B['secoes_base'])} seções (exterior incluído); sozinhas no local {fi(B['sozinhas_no_local'])}; previsão fora de (0, n) {fi(B['previsao_fora_de_0_n'])}; com z {fi(p['secoes_com_z'])}.")
    w(f"Regressão do T8 reproduzida: diferença máxima dos coeficientes contra resultados/T7_T14_bweb.json = {B['conferencia_coeficientes_T8_dif_max']:.1e}.")
    w('Desvio robusto de z por faixa de n: ' + '; '.join(f"{x['faixa']}: {fn(x['desvio_robusto'], 3)} (mediana {fn(x['mediana'], 3)}; {fi(x['secoes'])} seções)" for x in B['faixas_de_tamanho']) + '.')
    w(f"Acima de +4: {fi(p['acima'])}. Abaixo de -4: {fi(p['abaixo'])}. Razão: {fn(p['razao'], 3)} (ep do logaritmo {fn(p.get('ep_log_razao'), 3)}). Nas 10 zonas com mais: {fn(p['pct_nas_10_zonas'], 1)}% das de cima ({p.get('zonas_distintas_acima')} zonas distintas; limiar 30%); no espelho {fn(p.get('pct_nas_10_zonas_abaixo'), 1)}%.")
    w('  As 10 zonas com mais seções acima de +4: ' + '; '.join(f"{z} {n}" for z, n in p['top10_zonas']) + ' (ZZ|1 é o exterior inteiro).')
    w(f"Margem movida pelas caudas: de cima {fi(p['margem_cauda_de_cima'])} votos; de baixo {fi(p['margem_cauda_de_baixo'])}; líquida {fi(p['margem_liquida'])} votos = {fn(p['pct_da_margem_nacional'], 3)}% da margem nacional (a favor de Flávio).")
    w(f"Classificação pela letra: {B['classificacao_pela_letra']}.")
    w('Sensibilidades escritas antes (acima / abaixo / razão):')
    nomes_s = {'previsao_entre_0,1_e_0,9': 'só previsão entre 0,1 e 0,9', 'faixas_de_tamanho_x_previsao': 'faixas de tamanho cruzadas com faixas de previsão', 'z_em_pontos': 'z em pontos (sem a fórmula binomial)',
               'faixas_por_decis_de_n': 'faixas por decis de n', 'sem_exterior': 'sem exterior', 'n_50_ou_mais': 'n de 50 ou mais', 'sem_deixar_de_fora': 'sem deixar a seção de fora',
               'z_bruto_deixando_de_fora_sem_recalibrar': 'z binomial sem recalibrar'}
    for k, r in B['sensibilidades'].items():
        if 'acima' in r:
            w(f"  {nomes_s.get(k, k)}: {fi(r['acima'])} / {fi(r['abaixo'])} / {fn(r['razao'], 2)}")
    w('  por faixa de previsão da fatia de Lula (acima/abaixo): ' + '; '.join(f"{k.replace('.', ',')}: {r['acima']}/{r['abaixo']}" for k, r in B['sensibilidades']['por_faixa_de_previsao'].items()) + '.')
    w('  por faixa de n (acima/abaixo): ' + '; '.join(f"{k}: {r['acima']}/{r['abaixo']}" for k, r in B['sensibilidades']['por_faixa_de_tamanho'].items()) + '.')
    w('  O "desvio para Flávio" é efeito de borda: onde a previsão passa de 0,8 a fatia de Lula só pode errar para baixo (69 contra 544); onde fica abaixo de 0,2, só para cima (73 contra 4).')
    w('  Longe das bordas as caudas são iguais (186 contra 203).')
    w('Por UF (acima/abaixo): ' + '; '.join(f"{uf} {r['acima']}/{r['abaixo']}" for uf, r in B['por_uf'].items()) + '.')
    w(f"Calibração, caso plantado (+5 pontos em 1.000 seções de 10 zonas, 20 sorteios): critério de sinal atingido em {rf['sinal_em']} de {rf['de']}; em média {fn(rf['media_plantadas_alem_de_4'], 1)} das 1.000 plantadas")
    w(f"  passam de +4; razão média {fn(rf['media_razao'], 2)}; {fn(rf['media_zonas_plantadas_entre_as_10'], 1)} das 10 zonas plantadas aparecem entre as 10 primeiras; margem plantada {fi(rf['media_margem_plantada'])} votos ({fn(100 * rf['media_margem_plantada'] / MARGEM, 2)}% da margem).")
    nomes_c = {'+10pts_1000_secoes_10_zonas': '+10 pontos em 1.000 seções de 10 zonas', '+15pts_1000_secoes_10_zonas': '+15 pontos em 1.000 seções de 10 zonas',
               '+5pts_5000_secoes_50_zonas': '+5 pontos em 5.000 seções de 50 zonas', '+10pts_5000_secoes_50_zonas': '+10 pontos em 5.000 seções de 50 zonas'}
    for k, r in ca.items():
        if k.startswith('+'):
            w(f"  {nomes_c.get(k, k)}: sinal em {r['sinal_em']} de {r['de']}; plantadas além de +4: {fn(r['media_plantadas_alem_de_4'], 1)}; razão média {fn(r['media_razao'], 2)}; margem plantada {fi(r['media_margem_plantada'])} votos.")
    es = ca['espelho_-5pts_1000_secoes_10_zonas']
    w(f"  espelho (-5 pontos em 1.000 seções de 10 zonas): {fn(es['media_plantadas_alem_de_-4'], 1)} plantadas além de -4; razão média {fn(es['media_razao'], 2)}.")
    w(f"  Nenhum dos casos plantados dá SINAL: com {fi(p['abaixo'])} seções na cauda de baixo (efeito de borda), a razão de 1,3 exigiria {fi(np.ceil(1.3 * p['abaixo']))} seções na cauda de cima (há {fi(p['acima'])}),")
    w('  e quando a razão passa (+10 pontos em 5.000 seções) a cláusula das 10 zonas falha. O critério do F5, mesmo recalibrado, não tem como acusar nem absolver.')
    w(f"Caso plantado detectado: {'sim' if B['caso_plantado_detectado'] else 'não'}. VEREDITO: {B['veredito']}.")
    jc = B.get('ja_conferidas_no_F5_original')
    if isinstance(jc, dict):
        w(f"Das 30 de cima, {len(jc['top30'])} já tiveram boletim, RDV, log e assinatura conferidos no F5 original (sem sinal no arquivo); das 10 de baixo, {len(jc['bot10'])}.")
    w('As 30 de maior z recalibrado e as 10 de menor (para auditoria; em local com 2 seções a previsão vem de uma única vizinha):')
    for r in B['top30'] + B['bot10']:
        w(f"  {r['secao']:<22} z {fn(r['z_recalibrado'], 1):>7} | {fn(r['residuo_pontos'], 1):>6} pontos | n {r['n']:>4} | {r['L1']}/{r['R1']} -> {r['L2']}/{r['R2']} | comp {r['comp1']}->{r['comp2']} | BN {r['BN1']}->{r['BN2']} | local com {r['secoes_no_local']}" + (' | agregada' if r['agregada'] else ''))
    w('')
    # ---------------- C
    w('PARTE C. LINEARIDADE (descritivo): dispersão da virada por nível, em pontos da fatia de Lula (ou do PT) entre os dois finalistas')
    w('"Sorteio novo" = teto do acaso (cada seção sorteada de novo com a virada da unidade de cima). "Regra única" = uma só regra nacional de transferência')
    w('aplicada à composição de cada seção, mais o acaso. Razões são de variâncias.')
    w('  ano   virada   fora dos finalistas no 1T   nível       observado   sorteio novo   regra única   obs/sorteio novo   obs/regra única')
    nomes = {'uf': 'UF', 'mun': 'município', 'loc': 'local', 'sec': 'seção'}
    for a in AN:
        r = C['por_ano'][a]
        for k in ('uf', 'mun', 'loc', 'sec'):
            w(f"  {a}  {fn(r['virada_nacional_pontos'], 2, True)}    {fn(100 * r['outros_sobre_validos_1t'], 1):>5}%                    {nomes[k]:<10}  {fn(r['dp_observado_pontos'][k], 2)}        {fn(r['dp_sorteio_novo_pontos'][k], 2)}           {fn(r['dp_regra_unica_pontos'][k], 2)}          {fn(r['razao_var_observada_sobre_sorteio_novo'][k], 2):>6}             {fn(r['razao_var_observada_sobre_regra_unica'][k], 2)}")
        w(f"        desvio simples entre as 27 UFs: {fn(r['dp_simples_entre_ufs_pontos'], 2)} ponto ({fi(r['secoes'])} seções, {fi(r['municipios'])} municípios, {fi(r['locais'])} locais)")
    w('Leitura (as frases de antes estão no docstring):')
    w('  1. Entre UFs e entre municípios a virada de 2026 varia pouco em valor bruto (0,84 e 0,81 ponto), como em 2022 (0,55 e 0,70) e muito menos que em 2018 e 2014')
    w('     (2,8 a 4,1). Em 2018 e 2014 um quarto dos votos do 1º turno estava fora dos finalistas; em 2022 e 2026, 8%.')
    w('  2. Contra o acaso puro (sorteio novo), a variação entre UFs de 2026 é 12,8 vezes a do acaso, mais que em 2022 (5,1). As UFs não andaram juntas até o limite do acaso.')
    w('  3. Contra a regra única, a razão entre UFs e entre municípios fica ABAIXO de 1 nos quatro anos (2026: 0,17 e 0,34; 2022: 0,13 e 0,33; 2018: 0,37 e 0,89;')
    w('     2014: 0,46 e 0,73). A leitura escrita antes ("abaixo de 1 seria regularidade maior que o acaso") estava mal desenhada para esses níveis: a regra única não é')
    w('     piso, porque soma ao acaso o efeito da composição, e a virada real varia menos entre lugares do que a composição faria prever, em todos os anos. A marca')
    w('     registrada antes (perto de 1 em 2026 com os outros anos bem acima) não apareceu. 2026 e 2022 são parecidos; se isso for marca, é marca dos dois.')
    w('  4. Dentro do local, onde a régua é limpa, a dispersão de 2026 está ACIMA do acaso (razão 1,42 contra a regra única; phi 1,64 na parte A), como nos outros anos.')
    w('Locais regulares demais (T do local abaixo do quantil do qui-quadrado; observado contra simulado só com o acaso binomial das transições):')
    for a in AN:
        r = C['por_ano'][a]['locais_regulares_demais']
        w(f"  {a}: {fi(r['locais'])} locais; abaixo do quantil de 1%: {fn(100 * r['obs_abaixo_1%'], 2)}% (acaso {fn(100 * r['sim_abaixo_1%'], 2)}%); de 5%: {fn(100 * r['obs_abaixo_5%'], 2)}% (acaso {fn(100 * r['sim_abaixo_5%'], 2)}%); acima do de 99%: {fn(100 * r['obs_acima_99%'], 2)}% (acaso {fn(100 * r['sim_acima_99%'], 2)}%).")
    pu = C['por_ano']['2026']['locais_regulares_demais']['por_uf_2026']
    mxu = max(pu.items(), key=lambda kv: kv[1]['obs_abaixo_5%'])
    w(f"  Em 2026 há MENOS locais regulares demais do que o acaso daria, em todas as UFs (a maior fração abaixo do quantil de 5% é {mxu[0]}, {fn(100 * mxu[1]['obs_abaixo_5%'], 1)}%, contra 5% do acaso).")
    w('')
    if X:
        w('EXPLORATÓRIO (escrito e calculado DEPOIS de ver os resultados acima; pistas e réguas a mais, sem veredito)')
        e0 = X['E0_conferencia_interna']
        w(f"E0. Conferência interna: coeficientes iguais aos de lib.fe_ols (diferença máxima {e0['dif_max_coeficientes_contra_lib_fe_ols']:.1e}); phi recalculado {fn(e0['phi_recalculado'], 4)}.")
        w('E1. Régua interna para a parte espelhada. Mesmo sem fraude e sem nenhuma heterogeneidade, o sorteio multinomial dá um "phi de troca" maior que zero.')
        w('    ano    phi de troca   piso do acaso   excesso')
        for a in AN:
            r = X['E1_piso_multinomial_do_phi_de_troca'][a]
            w(f"    {a}   {fn(r['phi_de_troca'], 3)}          {fn(r['piso_multinomial'], 3)}           {fn(r['excesso'], 3)}")
        w('    O excesso de 2026 é igual ao de 2022 (0,169 contra 0,168) e muito menor que os de 2018 e 2014. Teto lendo TODO o excesso de 2026 como troca (sem')
        w('    nenhuma heterogeneidade natural), em % da margem: ' + '; '.join(f"{f} das urnas: {fn(r['base_piso_multinomial']['pct_da_margem'], 1)}%" for f, r in X['E1_teto_interno_pela_parte_espelhada'].items()) + '.')
        w('    Descontando o excesso de 2022: ' + '; '.join(f"{f}: {fn(r['base_excesso_de_2022']['pct_da_margem'], 1)}%" for f, r in X['E1_teto_interno_pela_parte_espelhada'].items()) + '.')
        w('E2. Anatomia das caudas da parte A (seções com Lula 3 desvios acima ou abaixo do previsto). Média do resíduo, em votos:')
        w('    ano    cauda      seções   Lula     Flávio   branco e nulo   abstenção')
        for a in AN:
            for lado in ('direita', 'esquerda'):
                r = X['E2_anatomia_das_caudas'][a][lado]
                w(f"    {a}   {lado:<9}  {r['secoes']:>5}   {fn(r['media_e_L'], 1, True):>6}   {fn(r['media_e_R'], 1, True):>6}   {fn(r['media_e_BN'], 1, True):>6}          {fn(r['media_e_abstencao'], 1, True):>6}")
        an = X['E2_anatomia_das_caudas']
        w('    Em 2026 a cauda direita (366 contra 265, razão 1,38, a maior dos quatro anos) tem como contrapartida a abstenção (-12,0 votos) mais que Flávio (-5,7):')
        w('    são seções onde veio mais gente do que o previsto, não seções onde o voto de Flávio encolheu. Saldo de votos de Lula nas duas caudas: ' + '; '.join(f"{a} {fi(an[a]['saldo_votos_L_nas_duas_caudas'])}" for a in AN) + '.')
        w('    Razão das caudas com outros limiares, 2026: 2,5 desvios ' + fn(an['2026']['razao_caudas_limiar_2.5'], 2) + f" ({an['2026']['n_limiar_2.5'][0]} contra {an['2026']['n_limiar_2.5'][1]}); 4 desvios " + fn(an['2026']['razao_caudas_limiar_4'], 2) + f" ({an['2026']['n_limiar_4'][0]} contra {an['2026']['n_limiar_4'][1]}).")
        puf = X['E2_caudas_2026_por_uf_[direita, esquerda, par a favor de Lula, par a favor de Flávio]']
        w('    Por UF em 2026 (direita/esquerda): ' + '; '.join(f"{u} {x[0]}/{x[1]}" for u, x in puf.items()) + '.')
        w('E3. Seções com a marca de troca nos dois lados ao mesmo tempo (Lula 3 desvios acima E Flávio 3 abaixo, na mesma seção), e o espelho:')
        w('    ' + '; '.join(f"{a}: {r['lula_acima_e_adversario_abaixo']} a favor do PT e {r['lula_abaixo_e_adversario_acima']} contra" for a, r in X['E3_pares_lula_acima_adversario_abaixo'].items()) + '.')
        w('    Em 2026 são 9 em 420.440 seções (em 2014 eram 108). Lista para auditoria (resíduo de Lula e de Flávio em votos):')
        for r in X['E3_lista_2026_lula_acima_e_flavio_abaixo']:
            w(f"      {r['secao']:<20} Lula {fn(r['e_L'], 1, True)}, Flávio {fn(r['e_R'], 1, True)} | {r['L1']}/{r['R1']} -> {r['L2']}/{r['R2']} | comp {r['comp1']}->{r['comp2']} | BN {r['BN1']}->{r['BN2']} | local com {r['secoes_no_local']}")
        w('    Espelho (Flávio acima e Lula abaixo): ' + '; '.join(f"{r['secao']} ({r['L1']}/{r['R1']} -> {r['L2']}/{r['R2']})" for r in X['E3_lista_2026_espelho_flavio_acima_e_lula_abaixo']) + '.')
        e4 = X['E4_varredura_por_zona']
        w(f"E4. Varredura por zona eleitoral (o que o F5 pela letra não enxerga). phi de troca por zona, {e4['zonas_com_100_ou_mais_secoes']} zonas com 100 ou mais seções: mediana {fn(e4['phi_de_troca_por_zona_quantis']['50'], 2)}; percentil 99 {fn(e4['phi_de_troca_por_zona_quantis']['99'], 2)}; máximo {fn(e4['phi_de_troca_por_zona_quantis']['100'], 2)}.")
        cz = e4['calibracao_caso_plantado_100_secoes_em_cada_uma_de_10_zonas']
        mn5 = min(min(c['+5pts']['phi_de_troca_das_zonas_plantadas']) for c in cz); mx5 = max(max(c['+5pts']['phi_de_troca_das_zonas_plantadas']) for c in cz)
        w(f"    Com o caso plantado do F5 (+5 pontos em 100 seções de cada uma de 10 zonas, 5 sorteios), as zonas plantadas ficam com phi de troca de {fn(mn5, 2)} a {fn(mx5, 2)} e ocupam")
        w('    as 10 primeiras posições em 5 de 5 sorteios. Com +3 pontos, ' + ', '.join(str(c['+3pts']['entre_as_10_primeiras']) for c in cz) + ' das 10 entram nas 10 primeiras.')
        w(f"    No dado real nenhuma zona chega perto: a maior é {e4['top20_zonas_por_phi_de_troca'][0]['zona']} com {fn(e4['top20_zonas_por_phi_de_troca'][0]['phi_de_troca'], 2)}. Não existe zona com a marca de +5 pontos em 100 das suas seções.")
        w('    As 20 zonas de maior phi de troca em 2026 (entre parênteses, a mesma zona em 2022), para quem quiser auditar: ' + '; '.join(f"{r['zona']} {fn(r['phi_de_troca'], 2)} ({fn(r['em_2022']['phi_de_troca'], 2) if r['em_2022'] else 'n/d'})" for r in e4['top20_zonas_por_phi_de_troca']) + '.')
        w(f"    Correlação do phi de troca por zona entre 2026 e 2022: {fn(e4['correlacao_phi_de_troca_2026_x_2022_por_zona'], 2)} ({e4['zonas_nos_dois_anos']} zonas). Zonas com 2026 acima do dobro de 2022 e acima de 1,5: {len(e4['zonas_com_phi_de_troca_2026_acima_do_dobro_de_2022_e_acima_de_1,5'])}.")
        e5 = X['E5_troca_por_local_ou_zona_inteira']
        w(f"E5. Limite do teste da parte A: a mesma dose inteira aplicada a 30% dos LOCAIS inteiros dá fator {fn(e5['30%_dos_locais_inteiros']['fator_sobre_bruto'], 2)}; a 30% das ZONAS inteiras, {fn(e5['30%_das_zonas_inteiras']['fator_sobre_bruto'], 2)}.")
        w('    O vizinho de sala só enxerga troca que atinja umas urnas e poupe outras DENTRO do mesmo prédio. Troca por prédio, zona ou UF inteira é assunto de B1, A3 e N3.')
        w('')
    w('O QUE PESA A FAVOR DA TESE (sem suavizar)')
    w('- A cauda direita de 2026 (Lula acima do previsto) é 1,38 vez a esquerda, a maior assimetria dos quatro anos (1,10 a 1,16 nos outros); o intervalo de 95% (1,18 a 1,63) exclui 1')
    w('  e contém o limite de 1,5 do registro. Está em SP (50 contra 21), MG (25 contra 8) e MA (25 contra 7). Em votos é pequeno: saldo de 2.268 votos.')
    d22 = pr['phi_2026'] - pr['phi_placebo']['2022']; e22 = float(np.hypot(pr['ep_phi_2026'], pr['ep_phi_placebo']['2022']))
    w(f"- phi de 2026 é {fn(100 * (pr['phi_2026'] / pr['phi_placebo']['2022'] - 1), 1)}% maior que o de 2022 ({fn(pr['phi_2026'], 3)} contra {fn(pr['phi_placebo']['2022'], 3)}; diferença {fn(d22, 3)}, ep {fn(e22, 3)}, {fn(d22 / e22, 1)} erros-padrão). A razão registrada")
    w('  fica em 0,83 porque o denominador é 2014, o ano mais disperso; contra 2022 seria 1,04, ainda abaixo de 1,15.')
    w('- A dispersão de 2026 é 64% maior que o acaso binomial e o perfil do eleitorado não explica nada dela. Lida inteira a favor da tese, cabe ali uma troca em 30% das urnas')
    w('  valendo até 54% da margem, ou em 50% das urnas valendo até 87%; pela parte espelhada (exploratório), 24% e 37%. Não são estimativas, são tetos.')
    w('- O teste não exclui troca em 70% das urnas ou mais (com a dose inteira plantada em 70% o veredito continuaria SEM SINAL) e é cego para troca igual em todas')
    w('  e para troca por prédio, zona ou UF inteira (fator 0,94 nos dois plantios).')
    w('- O reteste do F5 não tem poder: pela letra não se pode dizer que não houve +5 pontos em 1.000 seções.')
    w('- No TO o phi do presidente é 1,35 vez o do governador nas mesmas urnas (abaixo de 1,5; o phi de troca não acompanha).')
    w('O QUE PESA CONTRA A TESE (sem suavizar)')
    w('- Em nenhuma medida 2026 é mais disperso que o maior ano placebo: phi 0,83; equação de Flávio 0,76; phi de troca 0,51. Nenhuma UF passa de 1,15.')
    w('- A troca plantada é vista: a dose inteira em 30% das urnas multiplica phi por 2,3 (5 sorteios, 2,27 a 2,30) e dá SINAL pela letra; em 10%, por 6,2.')
    w('- A régua que não depende de outro ano vai no mesmo sentido: nas mesmas urnas, o phi do presidente é 0,95 do phi do governador, e o phi de troca, 0,63.')
    w('- A parte da dispersão que espelha em Flávio é 37,8% em 2026 e 35,9% em 2022; o excesso sobre o acaso é igual nos dois anos (0,169 e 0,168). A troca plantada a leva a 76%.')
    w('- As seções da cauda direita têm como contrapartida a abstenção, não o voto de Flávio: é o canal do comparecimento das Ondas A e B, não troca.')
    w('- Seções com a marca de troca nos dois lados: 9 em 420 mil (4 no espelho). Nenhuma zona com aglomerado.')
    w('- Se a marca de troca em parte das urnas existe em algum dos quatro anos, o ano que mais se parece com ela é 2014 (60,8% da dispersão espelhada no adversário,')
    w('  excesso de 0,694 sobre o acaso, 108 seções com a marca nos dois lados), não 2026. Ressalva: em 2014 e 2018 um quarto dos eleitores votou em eliminados, e a divisão')
    w('  deles entre os finalistas varia de seção para seção, o que produz dispersão espelhada sem fraude (é o mecanismo I2 da calibração).')
    w('- Linearidade: dentro do local a dispersão está acima do acaso; há menos locais "regulares demais" do que o acaso daria; entre UFs a variação é 12,8 vezes a do acaso.')
    w('')
    w('PISTAS (para auditoria; nenhuma é indício pelas regras do Adendo 27)')
    w('- As 9 seções de 2026 com Lula acima e Flávio abaixo ao mesmo tempo (lista em E3; duas na mesma zona de Manaus, AM|2550|63|822 e 788) e as 4 do espelho:')
    w('  boletim, RDV, log e assinatura, e caderno de votação. Nenhuma está nas amostras de arquivos em disco; não baixei nada (há um download em curso no mesmo site).')
    w('- As 366 seções da cauda direita da parte A (a assimetria vem de SP, MG e MA): o excesso de Lula ali vem com comparecimento acima do previsto. É o mesmo canal do N4;')
    w('  o que decide é caderno de votação, não boletim.')
    w('- As 30 seções de maior z do F5 recalibrado: 13 já tiveram os arquivos conferidos sem sinal; faltam 17 (todas em local com 2 ou 3 seções).')
    w('- As 20 zonas de maior phi de troca (E4), começando por SC|98, PE|57, SP|229, MT|40, AL|22 e AL|13 (PE|57, SP|229, MT|40 e AL|13 mais que dobraram em relação a')
    w('  2022, o que em parte é efeito de escolher as maiores). Em valor absoluto todas ficam abaixo de 1,25, longe do 1,6 a 3,6 do caso plantado.')
    w('- TO: presidente mais disperso que governador nas mesmas urnas (1,35). Cruzar com o D4-3 (testemunhas na tela de governador, AC e TO).')
    w('- 2014 é o ano em que a dispersão espelhada é maior. Para quem suspeita de 2014, é o lugar onde este teste teria mais a dizer, com a ressalva dos eliminados.')
    w('')
    w('DESVIOS DECLARADOS (decisões que o registro não fixa, tomadas no docstring antes de calcular)')
    w('- Parte A: A1 (seções agregadas não excluídas, porque o campo estatistica não exclui e os outros anos não têm a marca; variante ao lado), A2 (regressão refeita no')
    w('  universo restrito), A4 (phi como média de e2/v; razão das somas e versão robusta ao lado), A5 (bootstrap de municípios com coeficientes fixos), A6 (razão entre')
    w('  caudas = direita sobre esquerda), A7 (mistura com variância comum, dado agrupado em classes de 0,02; conversão para pontos e votos), A8 (ordem do veredito),')
    w('  A9 (regra do SEM PODER), A10 e A11 (plantios), A12 (parte espelhada e phi de troca, complementares), A13 (variantes), A14 (governador), A15 (tetos).')
    w('- Parte B: B1 a B9; em especial B3 (quatro faixas de n), B6 (o que é "caso plantado" e "detectado": o critério inteiro em 16 de 20 sorteios) e B7.')
    w('- Parte C inteira: sem critério registrado. Uma das leituras escritas antes (razão contra a regra única abaixo de 1 = regular demais) mostrou-se mal desenhada')
    w('  para os níveis de UF, município e local, e isso é dito no texto em vez de ser corrigido em silêncio.')
    w('- O desvio simples entre UFs sai 0,675 aqui e 0,69 no Adendo 29: lá entram todas as seções de cada turno; aqui, só as que têm os dois turnos, apuradas, no Brasil.')
    w('- Exploratório (E0 a E5): tudo escrito depois de ver o resultado.')
    return '\n'.join(L) + '\n'


if __name__ == '__main__':
    cmd = sys.argv[1] if len(sys.argv) > 1 else ''
    if cmd == 'perfil':
        extrair_perfil()
    elif cmd == 'gov2t':
        extrair_gov2t()
    elif cmd == 'A':
        parte_A()
    elif cmd == 'B':
        parte_B()
    elif cmd == 'C':
        parte_C()
    elif cmd == 'E':
        exploratorio_tudo()
    elif cmd == 'final':
        final()
    else:
        print(__doc__)
