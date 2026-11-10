"""R27 A1 (Adendo 27, Onda A): BRANCO E NULO.

Fragilidade "Canal do branco e nulo (forma A)" de registro/adendo27/equipe_vermelha_relatorio.json (retestes a, b, c e a
calibração d, com o critério proposto ali), a parte (b) do D4-6 de registro/adendo27/desenho_D4_proposta.json e a correção
do T34 (fragilidade "T34 e T23(b)").

Hipótese: brancos e nulos da tela de presidente registrados como voto nominal em Lula, talvez só onde há um cargo na
cédula do 2º turno (21 UFs sem 2º turno de governador), poupando as 6 UFs em que a mesma urna dá referência
(AC, AM, DF, ES, RN, TO).

Aviso do registro: os retestes da equipe vermelha foram escritos por quem já conhecia os resultados antigos (o critério
é novo, a escolha do que retestar é posterior ao dado). O D4-6 é desenho cego.

CRITÉRIOS DO REGISTRO (aplicados pela letra, sem mudar limiar)
  Item (a): se 2014 der coeficiente de +0,00 ou mais, a subida de 2026 é regime de queda de branco e nulo; se 2014 ficar
    abaixo de -0,04, 2026 destoa em mais de 0,06 e vira indício a cruzar com (c). Entre -0,04 e 0,00 o registro não diz
    nada: INCONCLUSIVO.
  Itens (b) e (c), SINAL: no lado de um cargo só, branco e nulo pelo menos 1,0 ponto abaixo (a mais de 4 ep) E fatia de
    Lula pelo menos 0,5 ponto acima (a mais de 3 ep), com o mesmo salto de Lula abaixo de 0,25 nas divisas equivalentes
    de 2014, 2018 e 2022. SEM SINAL: salto de Lula abaixo de 0,25 em valor absoluto com ep até 0,12, OU diferença em
    diferenças do branco e nulo de 2026 a até 0,3 ponto da média dos anos de referência. Fora disso: INCONCLUSIVO.
  D4-6(b), SINAL: DiD mediano das 6 UFs igual ou menor que -0,35 e pelo menos 0,15 abaixo do menor DiD das UFs placebo.
    SEM SINAL: DiD das 6 UFs entre o percentil 10 e o percentil 90 das UFs placebo. INCONCLUSIVO: entre os limiares, ou
    menos de 10 pares de UF e ano no placebo.
  T34: sinal com J de 0,015 ou mais a mais de 2,5 ep e J(2026) - J(2022) de 0,015 ou mais a mais de 2,5 ep; se a mediana
    do |J| das divisas placebo de 2026 passar de 0,01, vira inconclusivo; sem sinal com J de 0,008 ou menos e ep até
    0,005; agora com Bonferroni pelo número de divisas.

DECISÕES QUE O REGISTRO NÃO FIXA (escritas em 10/11/2026, antes de qualquer conta com votos deste script; o que eu já
conhecia: os números antigos citados no registro, entre eles bn_secao_2026.json +0,0251, o T34 publicado e a geometria do
cadastro de locais, que não tem voto)

 Geral
  G1. Grupos de 2026: G6 = AC, AM, DF, ES, RN, TO (2º turno de governador); G21 = as outras 21 UFs. O exterior (ZZ) fica
      fora dos contrastes e sai em separado no item (a).
  G2. UFs com 2º turno de governador por ano: 2018, 2022 e 2026 pelo bloco '2g' das bases de dados/. A base de 2014 não
      tem governador: a lista sai dos zips do bweb do 2º turno de 2014 em /home/user/trabalho-eleicao/adendo23/F21_2014
      (UFs em que aparece o cargo GOVERNADOR), fonte TSE, a mesma do F21.
  G3. Plantio: sorteio binomial com semente 20261110. Em cada seção do lado de um cargo só, x ~ Binomial(B2+N2, 0,35)
      votos saem do branco e nulo do 2º turno e entram em L2 (35% do branco e nulo observado, cerca de 1,35 milhão de
      votos). Ao lado, a versão 0,35/0,65 = 53,8% do observado (35% do branco e nulo de antes da conversão, se o
      observado já fosse o de depois).
  G4. "O teste enxerga": PODER PLENO se, com o plantio, as condições numéricas de SINAL de 2026 disparam. PODER DE
      MEDIDA se o plantio desloca cada estatística em pelo menos 80% do esperado e o deslocamento passa de 4 ep (branco
      e nulo) e de 3 ep (Lula). Sem poder de medida, o veredito é SEM PODER. Com poder de medida e sem poder pleno, vale
      o veredito pela letra e a ressalva é escrita.
  G5. Espelho: (i) a mesma conta para o adversário, com os desfechos em parcela do comparecimento e dos aptos (ganho de
      L e ganho de R separados; conversão de branco em Lula mexe só no ganho de L, eleitor de branco que fica em casa
      mexe na abstenção); (ii) onde não deveria dar nada: divisas entre UFs do mesmo grupo em 2026 e permutação das 6
      UFs entre as 27.
  G6. Tradução em votos: salto ou diferença em pontos vezes o comparecimento do 2º turno das 21 UFs; para a fatia de
      Lula, x = J * N / (1 - m - J), com N os votos nominais das 21 UFs e m a fatia de Lula nelas. Cada voto de branco
      ou nulo convertido soma 1 voto à margem (a margem é 4.430.191).

 Item (a), regressão do analisar_bn_secao.py
  A1. Funções montar() e rodar() importadas do script original, sem mudança, nos quatro anos, com todas as seções da
      base (inclusive exterior), como o original.
  A2. 2026 separado: G6, G21 e ZZ, cada um com a mesma função. Diferença G21 menos G6 com ep = raiz da soma das
      variâncias. Sem limiar no registro; leitura declarada aqui: a separação pesa a favor da tese se a diferença for
      positiva a mais de 3 ep E maior que a maior diferença análoga (um cargo menos dois cargos) de 2014, 2018 e 2022.
  A3. A mesma separação por UFs com e sem 2º turno de governador em 2014, 2018 e 2022.
  A4. Espelho: a mesma regressão com y = 100*(L2/comp2 - L1/comp1) e com y = 100*(R2/comp2 - R1/comp1).
  A5. Calibração em 2026: conversão nacional de f*(B2+N2) para L2 (a simulação do próprio script) nos totais de 1,0,
      1,82, 2,2 e 4,43 milhões; e o plantio G3 só nas 21 UFs, olhando a diferença G21 menos G6.
  A6. Votos pela calibração do Adendo 1: interpolação linear pelos pontos (0; 0), (+0,061; 1,82 milhão) e
      (+0,142; 4,43 milhões), extrapolando com a última inclinação, aplicada ao deslocamento do coeficiente de 2026
      contra cada ano de referência. Ao lado, a inclinação medida dentro de 2026 (A5), que não depende de outro ano.

 Item (b), diferença em diferenças por UF
  B1. Por UF e ano: bn_t = 100*(B+N)/comparecimento do turno t, com todas as seções da base naquele turno, sem exterior.
      Variação = bn_2 - bn_1.
  B2. DiD principal (agregada): variação do conjunto das UFs sem 2º turno de governador menos a do conjunto das UFs com
      (somas de votos de cada grupo). Negativo = o branco e nulo caiu mais onde só havia presidente. Ep por bootstrap de
      UFs dentro de cada grupo (2.000 reamostras). Ao lado: média simples das UFs com ep de Welch, e a versão em log.
  B3. Critério: |DiD 2026 - média(DiD 2014, 2018, 2022)| até 0,3 ponto, na versão agregada. A média simples sai ao lado.
  B4. Régua interna de 2026 (não usa outro ano): permutação exata, todas as 296.010 escolhas de 6 UFs entre 27, fração
      com DiD de média simples tão extrema quanto a observada.
  B5. Contabilidade em % dos aptos por grupo e ano: variação de L, de R, do branco e nulo, da abstenção e os eliminados
      do 1º turno (somam zero quando os aptos não mudam).

 D4-6(b)
  D1. (b1) Seções com os quatro blocos (1, 2, 1g, 2g). D_t = soma do B+N de presidente / soma do B+N de governador, por
      UF e turno. DiD = ln D_2 - ln D_1. Placebo: todas as UFs com 2º turno de governador em 2018 e 2022. Percentis 10 e
      90 por interpolação linear. "DiD das 6 UFs entre os percentis" lido como: todas as 6 dentro; a mediana ao lado.
  D2. Poder (b1), como no desenho: mover 26% e 52% do B+N de presidente do 2º turno para L2 nas 6 UFs e conferir a queda
      de 0,30 e 0,73; poder pleno se o critério de SINAL dispara com 52% (a conversão que viraria).
  D3. (b2) Especificação do D4-1: seções apuradas nos dois turnos, |aptos2 - aptos1| até 2, comparecimento do 1º turno
      de 30 ou mais, sem exterior, locais com 2 ou mais seções; respostas L2, R2, BN2 e A2 em número de eleitores;
      regressoras L1, R1, eliminados, B1, N1 e A1 = aptos - comparecimento; efeito fixo de local, peso 1/aptos, erro
      agrupado por município. Em 2026, cada eliminado com 0,5% ou mais dos válidos nacionais entra separado (Cury,
      Renan Santos e Caiado) e os demais somados; nos quatro anos, a variante (d) com os eliminados somados. O desenho
      não dá critério para (b2): é descritivo. Leitura declarada: coeficientes de B1 e de N1 na equação de L2 contra os
      mesmos na de R2 (espelho) e contra os outros anos; em 2026 também separados em G6 e G21.

 Item (c), divisas, e correção do T34
  C1. Coordenadas: arquivo de locais de 2026, linhas do 2º turno, como o T34. Filtro: (i) caixa da UF com folga de 0,1
      grau (extremos de cada UF fixados na tabela CAIXA deste script; conferi sem votos que todos os extremos do
      cadastro das UFs sem erro cabem nela); (ii) distância ao centroide do município (mediana de latitude e de
      longitude dos locais do município) de até 150 km, ou até 400 km em AC, AM, AP, MT, PA, RO e RR (municípios
      gigantes); (iii) multiplicidade máxima de 20 por local: de cada local ficam só os 20 pares mais próximos (o par
      fica se estiver entre os 20 mais próximos dos seus dois locais). Sensibilidades: limite de 100 e 300 km; tirar o
      local com mais de 20 pares em vez de cortar; sem filtro nenhum.
  C2. Unidade, modelo, pares e J como no T34 (scripts/analisar_divisa.py): local com 100 ou mais votos nominais no 2º
      turno; resíduo da fatia de Lula num modelo linear ponderado pelos nominais do 2º turno, ajustado nos locais a até
      100 km do outro lado, contra as fatias do comparecimento do 1º turno (L, R, demais) e o log dos aptos; pares a até
      20 km nos dois sentidos; J = média de (lado b menos lado a) ponderada pelos nominais do par; 2.000 reamostras.
  C3. Lado a = cada uma das 6 UFs; lado b = o conjunto das 21 (o método acha as vizinhas pela distância). São seis
      divisas compostas, cada uma com o seu modelo. Estatística do teste: J conjunto, a média ponderada de todos os
      pares das seis. Orientação: lado de um cargo só menos lado de dois cargos, em pontos percentuais.
  C4. Desfechos: resíduo da fatia de Lula (critério); variação do branco e nulo em pontos do comparecimento, bruta
      (critério); variação do comparecimento em pontos dos aptos, bruta. Ao lado: as versões residualizadas pelo mesmo
      modelo, a variação bruta da fatia de Lula, e a contabilidade em % dos aptos (L, R, branco e nulo, abstenção).
  C4b. Em 2026, o J conjunto de Lula sai também com o modelo M2 (Zema, Cury, Caiado e Renan Santos separados, ver T2),
      porque o eleitor de Caiado pesa de um lado só da divisa de GO. O critério usa o modelo do T34 (M0); o M2 fica ao lado.
  C5. Erro-padrão: bootstrap de municípios do lado a (como o T34), todos os pares das seis divisas juntos. O DF é um
      município só: nele o agrupamento é a zona eleitoral. Ao lado: bootstrap de municípios do lado b, e o erro com a
      divisa como unidade (bootstrap dos pares de UF). O critério usa o primeiro.
  C6. Divisas equivalentes dos outros anos, duas leituras, as duas relatadas: (E) equivalentes na condição: em cada ano,
      lado a = cada UF com 2º turno de governador naquele ano, lado b = as UFs sem; (G) as mesmas seis divisas de 2026
      com os votos de cada ano (placebo geográfico). A condição do critério ("salto de Lula abaixo de 0,25 nas divisas
      equivalentes") é lida em (E), pela letra (J menor que 0,25) e também em valor absoluto. As seções de 2014, 2018
      e 2022 são ligadas às coordenadas de 2026 pela chave UF|município|zona|seção, como na referência de 2022 do T34;
      onde a numeração mudou, o local pode estar errado dentro do mesmo município (ruído, não viés de UF).
  C7. Onde não deveria dar nada: J de cada divisa entre duas UFs do mesmo grupo em 2026 (as duas sem governador, ou
      AC com AM), pelo método do T34 divisa a divisa, com 50 pares ou mais.
  C8. Calibração: plantio G3 no lado das 21 e a conta inteira de novo (modelo reajustado).
  T1. T34 corrigido: a lista registrada (PR com SP+MS; PR-SP e PR-MS descritivas; as 11 placebo), sem filtro (para
      conferir que reproduzo o publicado) e com o filtro C1, em 2026 e 2022, e o critério registrado. Depois, todas as
      divisas de UF do país com 50 pares ou mais, com Bonferroni: 2,5 ep vira o quantil normal de 1 - 0,0062/n.
      Sem direção prevista nessas divisas, o critério é lido em |J|.
  T2. SP-MG: J com o filtro em três modelos: M0 (o do T34, eliminados somados), M1 (Zema e Cury separados dos demais),
      M2 (Zema, Cury, Caiado e Renan Santos separados). A explicação pela composição dos eliminados vale se, de M0 para
      M1, o |J| cair pelo menos à metade e ficar a menos de 2 ep de zero. O mesmo nas outras divisas com MG, ao lado.

O QUE FOR ACRESCENTADO DEPOIS DE VER RESULTADO FICA NA SEÇÃO "EXPLORATÓRIO" DO JSON E DO TXT, MARCADO.

ACRESCENTADO DEPOIS DE VER OS RESULTADOS (EXPLORATÓRIO; nada aqui muda veredito pela letra)
  X1. SP-MG sem filtro nos modelos M0, M1 e M2, e sem o único local de MG que vira par de 1.800 locais de SP: para
      separar a explicação "composição dos eliminados" da explicação "coordenada errada" no salto de -0,034.
  X2. Permutação (200 mil sorteios) da DiD do item (b) em 2014, 2018 e 2022, para pôr ao lado da de 2026.
  X3. D4-6(b1): teste de postos (Mann-Whitney) das 6 UFs contra as 26 placebo e a conversão que a diferença de
      medianas equivaleria.
  X4. Números digitados nos nulos de presidente do 2º turno nos RDV da amostra (835 seções, 10 UFs; das 6 UFs só o AC,
      12 seções): quanto do nulo de presidente é número de finalista de governador (erro de tela).
  X5. Votos pela calibração do plantio nas divisas (em vez da fórmula G6) e o salto de Lula que a conversão do salto
      inteiro do branco e nulo produziria.
  X6. (b2) em votos: (coeficiente em L2 menos coeficiente em R2) vezes o estoque de brancos e de nulos do 1º turno.
  X7. Salto de 2026 menos o salto de 2022 nas mesmas seis divisas.
  DESVIO: a regra G4 não previu o caso que apareceu no item (c): o critério dispara com o plantio (poder pleno pela
  definição), mas o deslocamento de Lula fica em 76% do esperado e 2,7 ep (sem poder de medida pela definição). Os
  dois fatos são relatados e o veredito de poder do item (c) fica como LIMITADO.
  DESVIO: na conferência do T34 sem filtro, 2 das 9 divisas diferem do publicado na quarta casa (SC-RS e MG-RJ em 2026):
  locais com coordenadas idênticas empatam na busca do vizinho mais próximo e a ordem de leitura decide o par.

RETOMADA (10/11/2026, depois do reinício do container por volta de 01:06 UTC)
  A execução anterior deste mesmo teste rodou as partes registradas (a, b, d, c, t; resultados parciais e logs em
  /home/user/trabalho-eleicao/adendo27/R27_A1, gravados entre 00:59 e 01:02 UTC) e foi interrompida antes de escrever
  as funções exploratorio() e escrever(). O docstring registrado antes de rodar está guardado sem mudança em
  docstring_antes_de_rodar.py, na mesma pasta. A retomada não mudou nenhuma função das partes registradas: conferiu o
  código, escreveu as duas funções que faltavam e rodou tudo de novo de uma vez (as sementes são fixas, os números das
  partes registradas saem iguais aos dos logs da primeira execução).
  Acrescentado na retomada, já conhecendo os resultados das partes registradas (EXPLORATÓRIO):
  X8. Para onde foi o branco e nulo que falta no lado de um cargo só: salto residual (mesmo modelo, mesmos pares) do
      ganho de Lula e do ganho do adversário em pontos do comparecimento. Os dois somam, por identidade contábil, o
      salto residual do branco e nulo com o sinal trocado. Conversão para Lula prevê tudo em Lula e zero no adversário.
      Em 2026 com M0 e M2, com o plantio de 35% ao lado, e nas divisas equivalentes (E) dos outros anos.
  X9. Ordem de grandeza do que uma conversão que virasse o resultado só nas 21 UFs (4,43 milhões) deixaria na divisa,
      por extrapolação linear do plantio de 35% (não dá para plantar: é mais que todo o branco e nulo observado ali).
  X10. Régua das divisas onde nada deveria saltar: a dispersão do salto nas divisas entre UFs do mesmo grupo em 2026,
      aplicada à média ponderada das divisas mistas; e quanto cada divisa mista contribui para o salto de Lula.
  X11. Dose entre divisas: regressão pela origem do salto de Lula sobre o salto do branco e nulo entre as divisas de UF
      de cada ano (todas, mesmo grupo, mistas). Conversão de branco e nulo em voto do PT prevê inclinação negativa.
  X3 (acréscimo): a taxa de conversão que o resultado das 6 UFs deixaria passar se a subida natural fosse a do
      percentil 90 ou a máxima do placebo, e o que essas taxas valeriam em votos se valessem nas 27 UFs.
  X1 (acréscimo): os locais com mais de 200 pares são retirados até não sobrar nenhum (há locais com a mesma
      coordenada que herdam os pares do que saiu); X4 (acréscimo): 13 e 22 separados nos nulos da tela de governador.
  DESVIO (aplicação da regra G4 ao item (b), que a primeira execução não tinha calculado): o plantio de 35% desloca a
  DiD em 99,9% do esperado, mas isso são 3,9 ep do bootstrap (o limite da G4 é 4), e a DiD plantada cai a 0,28 ponto
  da média dos anos de referência, isto é, dentro da faixa que o registro chama de "sem sinal". Pela letra da G4 e
  pela regra do pedido ("se não enxergar, o veredito é SEM PODER"), o item (b) sai como SEM PODER; o veredito pela
  letra do critério (INCONCLUSIVO) fica ao lado.
  DESVIO (item (c)): a terceira condição do SINAL (salto de Lula abaixo de 0,25 nas divisas equivalentes dos outros
  anos) falha por causa de 2018 (+1,14) e de 2014 (+0,26), qualquer que seja o dado de 2026. O critério, como escrito,
  não tinha como dar SINAL. Isso é relatado junto com o veredito pela letra.

Uso: python3 -I scripts/analisar_R27_A1.py [--partes a,b,d,c,t] [--trab pasta]
Saídas: resultados/R27_A1_branco_nulo.json e resultados/R27_A1_branco_nulo.txt
"""
import os as _os, sys as _sys
_AQUI = _os.path.dirname(_os.path.abspath(__file__))
_sys.path.insert(0, _AQUI)
import collections, csv, glob, gzip, io, itertools, json, math, sys, time, warnings, zipfile
import numpy as np
from scipy.spatial import cKDTree
from scipy.stats import norm
from lib import carregar, chave_local, fe_ols, demean
import analisar_bn_secao as BN
warnings.filterwarnings('ignore')

RAIZ = _os.path.dirname(_AQUI)
DADOS = _os.path.join(RAIZ, 'dados')
RESULT = _os.path.join(RAIZ, 'resultados')
ZIP_LOCAIS = '/home/user/trabalho-eleicao/adendo21/F14_dl_locais/eleitorado_local_votacao_2026.zip'
BWEB2014 = '/home/user/trabalho-eleicao/adendo23/F21_2014'
TRAB = '/home/user/trabalho-eleicao/adendo27/R27_A1'
SEMENTE = 20261110
MARGEM = 4430191
ANOS = [2014, 2018, 2022, 2026]
UFS27 = 'AC AL AM AP BA CE DF ES GO MA MG MS MT PA PB PE PI PR RJ RN RO RR RS SC SE SP TO'.split()
G6 = ['AC', 'AM', 'DF', 'ES', 'RN', 'TO']
NOMES = {2014: ('Dilma', 'Aécio'), 2018: ('Haddad', 'Bolsonaro'), 2022: ('Lula', 'Bolsonaro'), 2026: ('Lula', 'Flávio')}
COLS = ['L1', 'R1', 'O1', 'B1', 'N1', 'C1', 'A1', 'L2', 'R2', 'O2', 'B2', 'N2', 'C2', 'A2',
        'gB1', 'gN1', 'gC1', 'gB2', 'gN2', 'gC2', 'ap1', 'ap2']
IX = {c: i for i, c in enumerate(COLS)}
CAIXA = {'AC': (-11.15, -7.11, -73.99, -66.62), 'AL': (-10.50, -8.81, -38.24, -35.15), 'AM': (-9.82, 2.25, -73.80, -56.10),
         'AP': (-1.24, 4.44, -54.88, -49.87), 'BA': (-18.35, -8.53, -46.62, -37.34), 'CE': (-7.86, -2.78, -41.42, -37.25),
         'DF': (-16.05, -15.50, -48.29, -47.31), 'ES': (-21.30, -17.89, -41.88, -39.66), 'GO': (-19.50, -12.39, -53.25, -45.91),
         'MA': (-10.26, -1.04, -48.76, -41.79), 'MG': (-22.92, -14.23, -51.05, -39.86), 'MS': (-24.07, -17.17, -58.17, -50.92),
         'MT': (-18.04, -7.35, -61.63, -50.22), 'PA': (-9.84, 2.59, -58.90, -46.06), 'PB': (-8.30, -6.02, -38.77, -34.79),
         'PE': (-9.48, -3.80, -41.36, -32.39), 'PI': (-10.93, -2.74, -45.99, -40.37), 'PR': (-26.72, -22.52, -54.62, -48.02),
         'RJ': (-23.37, -20.76, -44.89, -40.96), 'RN': (-6.98, -4.83, -38.58, -34.97), 'RO': (-13.69, -7.97, -66.81, -59.77),
         'RR': (-1.58, 5.27, -64.83, -58.89), 'RS': (-33.75, -27.08, -57.64, -49.69), 'SC': (-29.35, -25.96, -53.84, -48.36),
         'SE': (-11.57, -9.51, -38.25, -36.39), 'SP': (-25.31, -19.78, -53.11, -44.16), 'TO': (-13.47, -5.17, -50.74, -45.70)}
FOLGA = 0.1
GIGANTES = {'AC', 'AM', 'AP', 'MT', 'PA', 'RO', 'RR'}
R_TERRA = 6371.0
T34_PRINCIPAL = 'PR-SP+MS'
T34_DESCRITIVAS = ['PR-SP', 'PR-MS']
T34_PLACEBO = ['PR-SC', 'SC-RS', 'SP-MS', 'SP-MG', 'SP-RJ', 'MS-MT', 'MS-GO', 'MS-MG', 'MG-GO', 'GO-MT', 'MG-RJ']
LOG = []


def diga(*a):
    s = ' '.join(str(x) for x in a)
    LOG.append(s); print(s, flush=True)


# ---------------------------------------------------------------- leitura
def extrair(d):
    """Dicionário da base -> (chaves, chave do local, UF, matriz de inteiros; -1 = bloco ausente)."""
    n = len(d)
    ks = np.empty(n, dtype=object); locs = np.empty(n, dtype=object)
    M = np.full((n, len(COLS)), -1, np.int64)
    tipos = collections.Counter()
    for i, (k, v) in enumerate(d.items()):
        ks[i] = k
        a, b = v.get('1'), v.get('2')
        locs[i] = chave_local(k, a) if a else (chave_local(k, b) if b else '')
        if a:
            M[i, 0:7] = (a['L'], a['R'], a['O'], a['B'], a['N'], a['comp'], a.get('apt', -1))
            M[i, IX['ap1']] = 1 if str(a.get('tipo', '')).lower() == 'apurada' else 0
            tipos[('1', a.get('tipo'))] += 1
        if b:
            M[i, 7:14] = (b['L'], b['R'], b['O'], b['B'], b['N'], b['comp'], b.get('apt', -1))
            M[i, IX['ap2']] = 1 if str(b.get('tipo', '')).lower() == 'apurada' else 0
            tipos[('2', b.get('tipo'))] += 1
        g = v.get('1g')
        if g: M[i, 14:17] = (g['B'], g['N'], g['comp'])
        g = v.get('2g')
        if g: M[i, 17:20] = (g['B'], g['N'], g['comp'])
    return ks.astype(str), locs.astype(str), M, {f'{t}|{n_}': c for (t, n_), c in tipos.items()}


def carregar_ano(ano, conferir=True):
    """Lê a base do ano (com cache em TRAB). Na primeira leitura confere que os meus vetores reproduzem montar()."""
    cache = _os.path.join(TRAB, f'sec{ano}.npz')
    if _os.path.exists(cache):
        z = np.load(cache, allow_pickle=False)
        return z['k'], z['loc'], z['M'], json.loads(str(z['tipos']))
    d = carregar(_os.path.join(DADOS, f'secoes{ano}.json.gz'))
    k, loc, M, tipos = extrair(d)
    if conferir:
        loc0, A0 = BN.montar(d)
        loc1, A1 = vetores_bn(loc, M)
        assert len(loc0) == len(loc1) and (loc0 == loc1).all() and (A0 == A1).all(), 'vetores diferentes de montar()'
    del d
    np.savez_compressed(cache, k=k, loc=loc, M=M, tipos=json.dumps(tipos))
    return k, loc, M, tipos


def vetores_bn(loc, M):
    """Os mesmos vetores de analisar_bn_secao.montar(): seções com os dois turnos."""
    m = (M[:, 0] >= 0) & (M[:, 7] >= 0)
    A = M[m][:, [0, 1, 2, 3, 4, 5, 7, 8, 9, 10, 11, 12]].astype(float).T
    return loc[m], A


def ufs_de(k):
    return np.array([x.split('|', 1)[0] for x in k])


def gov_2014():
    """UFs em que o bweb do 2º turno de 2014 traz o cargo GOVERNADOR."""
    com = []
    for uf in UFS27:
        zs = glob.glob(_os.path.join(BWEB2014, f'bweb_2t_{uf}', '*.zip'))
        if not zs:
            raise SystemExit(f'falta o bweb do 2º turno de 2014 de {uf}')
        z = zipfile.ZipFile(zs[0]); nome = [i.filename for i in z.infolist() if i.filename.lower().endswith('.txt')][0]
        achou = False; resto = b''
        with z.open(nome) as f:
            while True:
                b = f.read(1 << 22)
                if not b: break
                if b';"GOVERNADOR";' in resto + b:
                    achou = True; break
                resto = b[-40:]
        if achou: com.append(uf)
    return com


def grupos_gov(S):
    """ano -> lista das UFs com 2º turno de governador."""
    G = {}
    for ano in ANOS:
        k, loc, M, _ = S[ano]
        if ano == 2014:
            G[ano] = gov_2014()
        else:
            uf = ufs_de(k)
            G[ano] = sorted(set(uf[M[:, IX['gB2']] >= 0]) - {'ZZ'})
    return G


# ---------------------------------------------------------------- utilidades
def adendo1_votos(desloc):
    """Calibração do Adendo 1: (0;0), (+0,061; 1,82 mi), (+0,142; 4,43 mi), linear por trechos; devolve milhões."""
    if desloc <= 0.061:
        return desloc * 1.82 / 0.061
    return 1.82 + (desloc - 0.061) * (4.43 - 1.82) / (0.142 - 0.061)


def fe_ols_multi(Y, X, fe, cl, w, nomes_x, nomes_y):
    """MQO com efeito fixo (fe), peso w e erro agrupado por cl (CR1); várias respostas com as mesmas regressoras."""
    Y = np.asarray(Y, float); X = np.asarray(X, float); w = np.asarray(w, float)
    _, g = np.unique(fe, return_inverse=True)
    ok = np.bincount(g)[g] >= 2
    Y, X, w, g, cl = Y[ok], X[ok], w[ok], g[ok], np.asarray(cl)[ok]
    _, g = np.unique(g, return_inverse=True)
    Z = demean(np.column_stack([Y, X]), g, w)
    Yd, Xd = Z[:, :Y.shape[1]], Z[:, Y.shape[1]:]
    XtX = (Xd * w[:, None]).T @ Xd
    inv = np.linalg.inv(XtX)
    B = inv @ ((Xd * w[:, None]).T @ Yd)
    E = Yd - Xd @ B
    _, c = np.unique(cl, return_inverse=True); G = c.max() + 1
    N, kx = Xd.shape
    fator = G / (G - 1) * (N - 1) / (N - kx)
    out = {'n': int(N), 'locais': int(g.max() + 1), 'municipios': int(G), 'eq': {}}
    for r, ny in enumerate(nomes_y):
        Sg = np.column_stack([np.bincount(c, weights=w * Xd[:, j] * E[:, r], minlength=G) for j in range(kx)])
        V = fator * inv @ (Sg.T @ Sg) @ inv
        out['eq'][ny] = {'coef': dict(zip(nomes_x, B[:, r].tolist())), 'ep': dict(zip(nomes_x, np.sqrt(np.diag(V)).tolist()))}
    return out


def plantio_secoes(M, masc, frac, rng):
    """Cópia de M com x ~ Binomial(B2+N2, frac) movido do branco e nulo do 2º turno para L2 nas seções de masc."""
    M2 = M.copy()
    m = masc & (M[:, IX['L2']] >= 0)
    bn = M[m, IX['B2']] + M[m, IX['N2']]
    x = rng.binomial(bn, frac)
    xb = np.minimum(M[m, IX['B2']], np.round(x * np.where(bn > 0, M[m, IX['B2']] / np.maximum(bn, 1), 0)).astype(np.int64))
    xn = x - xb
    xn = np.minimum(xn, M[m, IX['N2']]); xb = x - xn
    M2[m, IX['L2']] += x; M2[m, IX['B2']] -= xb; M2[m, IX['N2']] -= xn
    assert (M2[m, IX['B2']] >= 0).all() and (M2[m, IX['N2']] >= 0).all()
    return M2, int(x.sum())


# ---------------------------------------------------------------- item (a)
def rodar_espelho(loc, A, lado):
    """A mesma regressão do analisar_bn_secao.rodar, com y = ganho do candidato em pontos do comparecimento."""
    L1, R1, O1, B1, N1, C1, L2, R2, O2, B2, N2, C2 = A
    ok = (C1 > 0) & (C2 > 0) & (L1 + R1 > 0) & (L2 + R2 > 0)
    y = 100 * (L2 / C2 - L1 / C1) if lado == 'L' else 100 * (R2 / C2 - R1 / C1)
    X = np.column_stack([100 * (B1 + N1) / C1, 100 * O1 / C1, 100 * L1 / C1])
    return fe_ols(y[ok], X[ok], loc[ok], (L2 + R2)[ok], ['branco_nulo_1t', 'outros_1t', 'fatia13_1t'])


def cb(r):
    return [r['coef']['branco_nulo_1t'], r['ep']['branco_nulo_1t'], r['n'], r['grupos']]


def parte_a(S, GOV):
    out = {'descricao': 'coeficiente do branco e nulo do 1º turno na virada do 13 entre turnos, efeito fixo de local '
                        '(analisar_bn_secao.py sem mudança); listas = [coeficiente, ep, n seções, n locais]', 'anos': {}}
    for ano in ANOS:
        k, loc, M, _ = S[ano]
        locA, A = vetores_bn(loc, M)
        uf = ufs_de(locA)
        base = BN.rodar(locA, A)
        com = np.isin(uf, GOV[ano]); zz = uf == 'ZZ'; sem = ~com & ~zz
        r = {'base': base, 'bn_1t_pct': base['bn_medio_1t'],
             'bn_2t_pct': float(100 * (A[9] + A[10]).sum() / A[11].sum()),
             'ufs_com_gov_2t': GOV[ano]}
        r['com_gov_2t'] = BN.rodar(locA[com], A[:, com]); r['sem_gov_2t'] = BN.rodar(locA[sem], A[:, sem])
        if zz.sum() > 50:
            try: r['exterior'] = BN.rodar(locA[zz], A[:, zz])
            except Exception as e: r['exterior'] = {'erro': str(e)}
        c1, c0 = r['sem_gov_2t'], r['com_gov_2t']
        dif = c1['coef']['branco_nulo_1t'] - c0['coef']['branco_nulo_1t']
        epd = math.hypot(c1['ep']['branco_nulo_1t'], c0['ep']['branco_nulo_1t'])
        r['dif_um_cargo_menos_dois'] = [dif, epd, dif / epd]
        r['espelho'] = {lado: {g: cb(rodar_espelho(locA[m], A[:, m], lado)) for g, m in
                               (('todas', np.ones(len(uf), bool)), ('com_gov_2t', com), ('sem_gov_2t', sem))} for lado in 'LR'}
        out['anos'][str(ano)] = r
        diga(f'(a) {ano}: base {cb(base)} | sem gov 2t {cb(c1)} | com gov 2t {cb(c0)} | dif {dif:+.4f} ({epd:.4f})')
    # calibração dentro de 2026
    k, loc, M, _ = S[2026]
    locA, A = vetores_bn(loc, M); uf = ufs_de(locA)
    b0 = out['anos']['2026']['base']['coef']['branco_nulo_1t']
    ok = (A[5] > 0) & (A[11] > 0) & (A[0] + A[1] > 0) & (A[6] + A[7] > 0)
    bn2 = float((A[9] + A[10])[ok].sum())
    cal = {}
    for alvo in (1.0e6, 1.82e6, 2.2e6, 4.43e6):
        rr = BN.rodar(locA, A, alvo / bn2)
        cal[f'{alvo / 1e6:.2f}'] = {'convertidos': rr['convertidos'], 'coef': rr['coef']['branco_nulo_1t'], 'ep': rr['ep']['branco_nulo_1t'],
                                    'desloc': rr['coef']['branco_nulo_1t'] - b0}
    incl = cal['1.82']['desloc'] / 1.82
    out['calibracao_2026_nacional'] = {'bn_2t_nas_secoes': bn2, 'por_milhoes': cal, 'desloc_por_milhao_ate_1_82': incl,
                                       'nota': 'conversão proporcional ao B+N do 2º turno de cada seção, somada por cima do dado de 2026'}
    # plantio só nas 21
    rng = np.random.default_rng(SEMENTE)
    g21 = ~np.isin(ufs_de(k), G6 + ['ZZ'])
    pl = {}
    for nome, frac in (('35', 0.35), ('53.8', 0.35 / 0.65)):
        M2, tot = plantio_secoes(M, g21, frac, rng)
        l2, A2 = vetores_bn(loc, M2); u2 = ufs_de(l2)
        m21 = ~np.isin(u2, G6 + ['ZZ']); m6 = np.isin(u2, G6)
        r21 = BN.rodar(l2[m21], A2[:, m21]); r6 = BN.rodar(l2[m6], A2[:, m6]); rn = BN.rodar(l2, A2)
        dif = r21['coef']['branco_nulo_1t'] - r6['coef']['branco_nulo_1t']; epd = math.hypot(r21['ep']['branco_nulo_1t'], r6['ep']['branco_nulo_1t'])
        d0 = out['anos']['2026']['dif_um_cargo_menos_dois']
        pl[nome] = {'votos_plantados': tot, 'g21': cb(r21), 'g6': cb(r6), 'nacional': cb(rn), 'dif': [dif, epd, dif / epd],
                    'desloc_da_dif': dif - d0[0], 'desloc_em_ep': (dif - d0[0]) / epd}
    out['plantio_21_ufs'] = pl
    # tradução em votos
    c26 = out['anos']['2026']['base']['coef']['branco_nulo_1t']
    trad = {}
    for ano in (2014, 2018, 2022):
        cr = out['anos'][str(ano)]['base']['coef']['branco_nulo_1t']
        d = c26 - cr
        trad[str(ano)] = {'coef_ref': cr, 'desloc_2026': d, 'adendo1_milhoes': adendo1_votos(d) if d > 0 else 0.0,
                          'regua_interna_2026_milhoes': d / incl}
    trad['zero'] = {'coef_ref': 0.0, 'desloc_2026': c26, 'adendo1_milhoes': adendo1_votos(c26), 'regua_interna_2026_milhoes': c26 / incl}
    out['traducao_votos'] = trad
    c14 = out['anos']['2014']['base']['coef']['branco_nulo_1t']
    out['criterio'] = {'coef_2014': c14, 'coef_2026': c26, 'dif_2026_menos_2014': c26 - c14,
                       'veredito': 'REGIME DE QUEDA (sem indício)' if c14 >= 0 else ('2026 DESTOA (indício a cruzar com c)' if c14 < -0.04 else 'INCONCLUSIVO')}
    difs = {a: out['anos'][str(a)]['dif_um_cargo_menos_dois'] for a in ANOS}
    maior_ref = max(difs[a][0] for a in (2014, 2018, 2022))
    out['separacao'] = {'dif_por_ano': {str(a): v for a, v in difs.items()}, 'maior_dif_de_referencia': maior_ref,
                        'pesa_a_favor': bool(difs[2026][0] > 0 and difs[2026][2] > 3 and difs[2026][0] > maior_ref),
                        'plantio_35_enxergado': bool(pl['35']['desloc_em_ep'] > 3)}
    diga('(a) criterio:', out['criterio'], '| separacao:', out['separacao'])
    return out


# ---------------------------------------------------------------- item (b)
def somas_uf(k, M):
    uf = ufs_de(k); r = {}
    t1 = M[:, 0] >= 0; t2 = M[:, 7] >= 0; t12 = t1 & t2
    for u in UFS27:
        m = uf == u
        f = lambda c, t: float(M[m & t, IX[c]].sum())
        r[u] = {'bn1': f('B1', t1) + f('N1', t1), 'c1': f('C1', t1), 'bn2': f('B2', t2) + f('N2', t2), 'c2': f('C2', t2),
                'L1': f('L1', t1), 'R1': f('R1', t1), 'O1': f('O1', t1), 'L2': f('L2', t2), 'R2': f('R2', t2),
                'a1': f('A1', t1), 'a2': f('A2', t2), 'nom2': f('L2', t2) + f('R2', t2)}
    return r


def did_de(U, com):
    """U: somas por UF; com: UFs com 2º turno de governador. Devolve as medidas da diferença em diferenças."""
    sem = [u for u in UFS27 if u not in com]
    def var(us):
        s = lambda c: sum(U[u][c] for u in us)
        return 100 * (s('bn2') / s('c2') - s('bn1') / s('c1'))
    def varlog(us):
        s = lambda c: sum(U[u][c] for u in us)
        return math.log((s('bn2') / s('c2')) / (s('bn1') / s('c1')))
    du = {u: 100 * (U[u]['bn2'] / U[u]['c2'] - U[u]['bn1'] / U[u]['c1']) for u in UFS27}
    a = np.array([du[u] for u in sem]); b = np.array([du[u] for u in com])
    return {'var_sem': var(sem), 'var_com': var(com), 'did_agregada': var(sem) - var(com),
            'did_log': varlog(sem) - varlog(com),
            'did_media_simples': float(a.mean() - b.mean()),
            'ep_welch': float(math.sqrt(a.var(ddof=1) / len(a) + b.var(ddof=1) / len(b))) if len(a) > 1 and len(b) > 1 else None,
            'var_por_uf': du, 'n_sem': len(sem), 'n_com': len(com)}


def boot_did(U, com, reps, rng):
    sem = [u for u in UFS27 if u not in com]
    V = {u: np.array([U[u]['bn1'], U[u]['c1'], U[u]['bn2'], U[u]['c2']]) for u in UFS27}
    As = np.array([V[u] for u in sem]); Ac = np.array([V[u] for u in com]); o = []
    for _ in range(reps):
        s = As[rng.integers(0, len(As), len(As))].sum(0); c = Ac[rng.integers(0, len(Ac), len(Ac))].sum(0)
        o.append(100 * ((s[2] / s[3] - s[0] / s[1]) - (c[2] / c[3] - c[0] / c[1])))
    return float(np.std(o, ddof=1))


def contab(k, M, com):
    """Contabilidade em % dos aptos, seções com os dois turnos, por grupo."""
    uf = ufs_de(k); t = (M[:, 0] >= 0) & (M[:, 7] >= 0) & (M[:, IX['A1']] > 0) & (M[:, IX['A2']] > 0)
    r = {}
    for nome, m in (('com_gov_2t', np.isin(uf, com)), ('sem_gov_2t', ~np.isin(uf, list(com) + ['ZZ']))):
        s = lambda c: float(M[m & t, IX[c]].sum())
        a1, a2 = s('A1'), s('A2')
        r[nome] = {'dL': 100 * (s('L2') / a2 - s('L1') / a1), 'dR': 100 * (s('R2') / a2 - s('R1') / a1),
                   'dBN': 100 * ((s('B2') + s('N2')) / a2 - (s('B1') + s('N1')) / a1),
                   'dAbst': 100 * ((a2 - s('C2')) / a2 - (a1 - s('C1')) / a1), 'O1': 100 * s('O1') / a1,
                   'bn1_pct_comp': 100 * (s('B1') + s('N1')) / s('C1'), 'bn2_pct_comp': 100 * (s('B2') + s('N2')) / s('C2'),
                   'aptos_2t': a2, 'comp_2t': s('C2'), 'nominais_2t': s('L2') + s('R2'), 'fatia_L_2t': s('L2') / (s('L2') + s('R2'))}
    r['dif_sem_menos_com'] = {c: r['sem_gov_2t'][c] - r['com_gov_2t'][c] for c in ('dL', 'dR', 'dBN', 'dAbst', 'O1')}
    return r


def parte_b(S, GOV):
    rng = np.random.default_rng(SEMENTE + 1)
    out = {'descricao': 'variação do branco e nulo de presidente entre turnos (pontos do comparecimento): UFs sem 2º turno de '
                        'governador menos UFs com. Negativo = caiu mais onde só havia presidente.', 'anos': {}}
    for ano in ANOS:
        k, loc, M, _ = S[ano]
        U = somas_uf(k, M)
        r = did_de(U, GOV[ano]); r['ep_boot_agregada'] = boot_did(U, GOV[ano], 2000, rng)
        r['contabilidade_pct_aptos'] = contab(k, M, GOV[ano]); r['ufs_com_gov_2t'] = GOV[ano]
        out['anos'][str(ano)] = r
        diga(f"(b) {ano}: var sem {r['var_sem']:+.3f} com {r['var_com']:+.3f} DiD agregada {r['did_agregada']:+.3f} (ep {r['ep_boot_agregada']:.3f}) "
             f"media simples {r['did_media_simples']:+.3f} (ep {r['ep_welch']:.3f}) log {r['did_log']:+.3f}")
    ref = [out['anos'][str(a)]['did_agregada'] for a in (2014, 2018, 2022)]
    refs = [out['anos'][str(a)]['did_media_simples'] for a in (2014, 2018, 2022)]
    d26 = out['anos']['2026']['did_agregada']; d26s = out['anos']['2026']['did_media_simples']
    out['criterio'] = {'did_2026_agregada': d26, 'media_referencia_agregada': float(np.mean(ref)), 'distancia_agregada': d26 - float(np.mean(ref)),
                       'did_2026_media_simples': d26s, 'media_referencia_media_simples': float(np.mean(refs)), 'distancia_media_simples': d26s - float(np.mean(refs)),
                       'dentro_de_0_3': bool(abs(d26 - np.mean(ref)) <= 0.3), 'dentro_de_0_3_media_simples': bool(abs(d26s - np.mean(refs)) <= 0.3)}
    # permutação exata dentro de 2026
    k, loc, M, _ = S[2026]; U = somas_uf(k, M)
    du = np.array([out['anos']['2026']['var_por_uf'][u] for u in UFS27])
    V = np.array([[U[u]['bn1'], U[u]['c1'], U[u]['bn2'], U[u]['c2']] for u in UFS27])
    comb = np.array(list(itertools.combinations(range(27), 6)))
    sg = du[comb].sum(1); ms = (du.sum() - sg) / 21 - sg / 6
    Vc = V[comb].sum(1); Vs = V.sum(0)[None, :] - Vc
    ag = 100 * ((Vs[:, 2] / Vs[:, 3] - Vs[:, 0] / Vs[:, 1]) - (Vc[:, 2] / Vc[:, 3] - Vc[:, 0] / Vc[:, 1]))
    out['permutacao_2026'] = {'n_escolhas': int(len(comb)),
                              'p_media_simples_tao_negativa': float((ms <= d26s + 1e-12).mean()), 'p_media_simples_bilateral': float((np.abs(ms) >= abs(d26s) - 1e-12).mean()),
                              'p_agregada_tao_negativa': float((ag <= d26 + 1e-12).mean()), 'p_agregada_bilateral': float((np.abs(ag) >= abs(d26) - 1e-12).mean()),
                              'dp_media_simples': float(ms.std()), 'dp_agregada': float(ag.std())}
    # plantio
    rng = np.random.default_rng(SEMENTE)
    g21 = ~np.isin(ufs_de(k), G6 + ['ZZ']); pl = {}
    for nome, frac in (('35', 0.35), ('53.8', 0.35 / 0.65)):
        M2, tot = plantio_secoes(M, g21, frac, rng)
        r = did_de(somas_uf(k, M2), G6)
        pl[nome] = {'votos_plantados': tot, 'did_agregada': r['did_agregada'], 'desloc': r['did_agregada'] - d26,
                    'esperado': -frac * out['anos']['2026']['contabilidade_pct_aptos']['sem_gov_2t']['bn2_pct_comp'],
                    'distancia_da_media_de_referencia': r['did_agregada'] - float(np.mean(ref)),
                    'sai_da_zona_sem_sinal': bool(abs(r['did_agregada'] - np.mean(ref)) > 0.3)}
    out['plantio_21_ufs'] = pl
    c = out['anos']['2026']['contabilidade_pct_aptos']['sem_gov_2t']
    out['traducao_votos'] = {'comp_2t_21_ufs': c['comp_2t'], 'did_2026_em_votos': d26 / 100 * c['comp_2t'],
                             'distancia_da_referencia_em_votos': (d26 - float(np.mean(ref))) / 100 * c['comp_2t'],
                             'pct_da_margem': abs(d26 / 100 * c['comp_2t']) / MARGEM}
    diga('(b) criterio:', out['criterio']); diga('(b) permutacao:', out['permutacao_2026']); diga('(b) votos:', out['traducao_votos'])
    return out


# ---------------------------------------------------------------- D4-6(b)
def d_pres_gov(k, M, ufs):
    uf = ufs_de(k); t = (M[:, 0] >= 0) & (M[:, 7] >= 0) & (M[:, IX['gB1']] >= 0) & (M[:, IX['gB2']] >= 0); r = {}
    for u in ufs:
        m = t & (uf == u)
        s = lambda c: float(M[m, IX[c]].sum())
        p1, p2, g1, g2 = s('B1') + s('N1'), s('B2') + s('N2'), s('gB1') + s('gN1'), s('gB2') + s('gN2')
        r[u] = {'secoes': int(m.sum()), 'bn_pres_1t': p1, 'bn_gov_1t': g1, 'bn_pres_2t': p2, 'bn_gov_2t': g2,
                'pct_pres_1t': 100 * p1 / s('C1'), 'pct_pres_2t': 100 * p2 / s('C2'), 'pct_gov_1t': 100 * g1 / s('gC1'), 'pct_gov_2t': 100 * g2 / s('gC2'),
                'lnD1': math.log(p1 / g1), 'lnD2': math.log(p2 / g2), 'DiD': math.log(p2 / g2) - math.log(p1 / g1)}
    return r


def parte_d(S, GOV, cand26):
    out = {}
    por = {str(a): d_pres_gov(S[a][0], S[a][2], GOV[a]) for a in (2018, 2022, 2026)}
    plac = np.array([v['DiD'] for a in ('2018', '2022') for v in por[a].values()])
    seis = np.array([por['2026'][u]['DiD'] for u in G6])
    p10, p90 = np.percentile(plac, [10, 90])
    b1 = {'por_uf': por, 'placebo_n': int(len(plac)), 'placebo_min': float(plac.min()), 'placebo_p10': float(p10), 'placebo_mediana': float(np.median(plac)),
          'placebo_p90': float(p90), 'placebo_max': float(plac.max()), 'seis_DiD': {u: float(por['2026'][u]['DiD']) for u in G6}, 'seis_mediana': float(np.median(seis)),
          'seis_dentro_p10_p90': int(((seis >= p10) & (seis <= p90)).sum())}
    sinal = bool(np.median(seis) <= -0.35 and np.median(seis) <= plac.min() - 0.15)
    sem = bool(((seis >= p10) & (seis <= p90)).all())
    b1['veredito'] = 'INCONCLUSIVO' if len(plac) < 10 else ('SINAL' if sinal else ('SEM SINAL' if sem else 'INCONCLUSIVO'))
    b1['mediana_dentro_p10_p90'] = bool(p10 <= np.median(seis) <= p90)
    # poder: 26% e 52% nas 6 UFs
    k, loc, M, _ = S[2026]; rng = np.random.default_rng(SEMENTE); pod = {}
    m6 = np.isin(ufs_de(k), G6)
    for frac in (0.26, 0.52):
        M2, tot = plantio_secoes(M, m6, frac, rng)
        r = d_pres_gov(k, M2, G6); s2 = np.array([r[u]['DiD'] for u in G6])
        pod[str(frac)] = {'votos_plantados': tot, 'mediana': float(np.median(s2)), 'queda_da_mediana': float(np.median(s2) - np.median(seis)),
                          'esperado': math.log(1 - frac), 'sinal_dispara': bool(np.median(s2) <= -0.35 and np.median(s2) <= plac.min() - 0.15),
                          'sai_de_sem_sinal': bool(not ((s2 >= p10) & (s2 <= p90)).all())}
    b1['poder'] = pod
    b1['poder_pleno'] = pod['0.52']['sinal_dispara']
    b1['poder_de_medida'] = bool(abs(pod['0.52']['queda_da_mediana'] / pod['0.52']['esperado'] - 1) < 0.2)
    out['b1'] = b1
    diga('(D4-6 b1) placebo n', len(plac), 'min %.3f p10 %.3f med %.3f p90 %.3f max %.3f' % (plac.min(), p10, np.median(plac), p90, plac.max()),
         '| 6 UFs', {u: round(float(por['2026'][u]['DiD']), 3) for u in G6}, 'mediana %.3f' % np.median(seis), b1['veredito'], '| poder', pod)
    # (b2)
    b2 = {}
    for ano in ANOS:
        k, loc, M, _ = S[ano]; uf = ufs_de(k)
        m = ((M[:, 0] >= 0) & (M[:, 7] >= 0) & (M[:, IX['ap1']] == 1) & (M[:, IX['ap2']] == 1) & (np.abs(M[:, IX['A2']] - M[:, IX['A1']]) <= 2)
             & (M[:, IX['C1']] >= 30) & (uf != 'ZZ') & (M[:, IX['A1']] > 0))
        Mm = M[m].astype(float); c = lambda x: Mm[:, IX[x]]
        Y = np.column_stack([c('L2'), c('R2'), c('B2') + c('N2'), c('A2') - c('C2')])
        mun = np.array(['|'.join(x.split('|')[:2]) for x in k[m]]); w = 1 / c('A1')
        Xd = np.column_stack([c('L1'), c('R1'), c('O1'), c('B1'), c('N1'), c('A1') - c('C1')])
        nx = ['L1', 'R1', 'O1', 'B1', 'N1', 'A1']; ny = ['L2', 'R2', 'BN2', 'A2']
        r = {'variante_d': fe_ols_multi(Y, Xd, loc[m], mun, w, nx, ny)}
        for nome, g in (('com_gov_2t', np.isin(uf[m], GOV[ano])), ('sem_gov_2t', ~np.isin(uf[m], GOV[ano]))):
            r['variante_d_' + nome] = fe_ols_multi(Y[g], Xd[g], loc[m][g], mun[g], w[g], nx, ny)
        if ano == 2026:
            sc = cand26['secoes']; tot = cand26['totais']; val = sum(v for n_, v in tot.items())
            sep = [n_ for n_, v in tot.items() if n_ not in ('13', '22') and v / val >= 0.005]
            E = np.array([[sc.get(kk, {}).get(n_, 0) for n_ in sep] for kk in k[m]], float)
            X1 = np.column_stack([c('L1'), c('R1'), E, c('O1') - E.sum(1), c('B1'), c('N1'), c('A1') - c('C1')])
            nx1 = ['L1', 'R1'] + ['cand_' + n_ for n_ in sep] + ['demais', 'B1', 'N1', 'A1']
            r['principal'] = fe_ols_multi(Y, X1, loc[m], mun, w, nx1, ny); r['eliminados_separados'] = {n_: cand26['nomes'][n_] for n_ in sep}
            for nome, g in (('g6', np.isin(uf[m], G6)), ('g21', ~np.isin(uf[m], G6))):
                r['principal_' + nome] = fe_ols_multi(Y[g], X1[g], loc[m][g], mun[g], w[g], nx1, ny)
        b2[str(ano)] = r
        e = r['variante_d']['eq']
        diga(f"(D4-6 b2) {ano} n {r['variante_d']['n']}: L2~B1 {e['L2']['coef']['B1']:+.4f} ({e['L2']['ep']['B1']:.4f}) L2~N1 {e['L2']['coef']['N1']:+.4f} ({e['L2']['ep']['N1']:.4f}) | "
             f"R2~B1 {e['R2']['coef']['B1']:+.4f} ({e['R2']['ep']['B1']:.4f}) R2~N1 {e['R2']['coef']['N1']:+.4f} ({e['R2']['ep']['N1']:.4f})")
    out['b2'] = b2
    return out


# ---------------------------------------------------------------- locais e divisas
def xyz(lat, lon):
    la, lo = np.radians(lat), np.radians(lon)
    return np.column_stack([np.cos(la) * np.cos(lo), np.cos(la) * np.sin(lo), np.sin(la)])


def corda(km):
    return 2 * np.sin(km / (2 * R_TERRA))


def km_de(c):
    return 2 * R_TERRA * np.arcsin(np.minimum(c, 2) / 2)


def ler_locais():
    """Cadastro de locais de 2026 (2º turno), como no analisar_divisa.py: chave da seção -> local; local -> coordenada."""
    cache = _os.path.join(TRAB, 'locais2026.npz')
    if _os.path.exists(cache):
        z = np.load(cache, allow_pickle=False)
        return {c: z[c] for c in z.files}
    Z = zipfile.ZipFile(ZIP_LOCAIS); sec = {}; loc = {}
    for uf in UFS27:
        with Z.open(f'eleitorado_local_votacao_2026_{uf}.csv') as fb:
            f = io.TextIOWrapper(fb, encoding='latin1', newline='')
            r = csv.reader(f, delimiter=';'); h = next(r); ix = {c: i for i, c in enumerate(h)}
            for row in r:
                if row[ix['NR_TURNO']] != '2':
                    continue
                try:
                    lat = float(row[ix['NR_LATITUDE']].replace(',', '.')); lon = float(row[ix['NR_LONGITUDE']].replace(',', '.'))
                except ValueError:
                    continue
                if lat == -1 or lon == -1:
                    continue
                mun, z_, s, lv = (int(row[ix[c]]) for c in ('CD_MUNICIPIO', 'NR_ZONA', 'NR_SECAO', 'NR_LOCAL_VOTACAO'))
                lid = f'{uf}|{mun}|{z_}|{lv}'
                sec[f'{uf}|{mun}|{z_}|{s}'] = lid; loc[lid] = (lat, lon)
    lids = np.array(list(loc)); pos = {l: i for i, l in enumerate(lids)}
    g = {'lid': lids, 'lat': np.array([loc[l][0] for l in lids]), 'lon': np.array([loc[l][1] for l in lids]),
         'sec_k': np.array(list(sec)), 'sec_l': np.array([pos[v] for v in sec.values()], np.int64)}
    np.savez_compressed(cache, **g)
    return g


class Geo:
    def __init__(self):
        g = ler_locais()
        self.lid = g['lid']; self.lat = g['lat']; self.lon = g['lon']; self.n = len(self.lid)
        self.sec = dict(zip(g['sec_k'].tolist(), g['sec_l'].tolist()))
        p = [x.split('|') for x in self.lid.tolist()]
        self.uf = np.array([x[0] for x in p]); self.mun = np.array([x[0] + '|' + x[1] for x in p])
        # agrupamento do bootstrap: município; no DF, a zona eleitoral
        self.grupo = np.array([x[0] + '|' + x[1] if x[0] != 'DF' else 'DF|z' + x[2] for x in p])
        self.P = xyz(self.lat, self.lon)
        cx = np.array([CAIXA[u] for u in self.uf])
        self.na_caixa = ((self.lat >= cx[:, 0] - FOLGA) & (self.lat <= cx[:, 1] + FOLGA) & (self.lon >= cx[:, 2] - FOLGA) & (self.lon <= cx[:, 3] + FOLGA))
        # centroide do município: mediana dos locais dentro da caixa
        _, gi = np.unique(self.mun, return_inverse=True)
        cl = np.full(gi.max() + 1, np.nan); co = np.full(gi.max() + 1, np.nan)
        ordem = np.argsort(gi, kind='stable'); cnt = np.bincount(gi); ini = np.concatenate([[0], np.cumsum(cnt)])
        for i in range(len(cnt)):
            ii = ordem[ini[i]:ini[i + 1]]; ii = ii[self.na_caixa[ii]]
            if len(ii): cl[i] = np.median(self.lat[ii]); co[i] = np.median(self.lon[ii])
        p_ = np.pi / 180
        a = np.sin((self.lat - cl[gi]) * p_ / 2) ** 2 + np.cos(self.lat * p_) * np.cos(cl[gi] * p_) * np.sin((self.lon - co[gi]) * p_ / 2) ** 2
        self.dist_centro = 2 * R_TERRA * np.arcsin(np.sqrt(a))

    def filtro(self, lim=150, lim_gig=400):
        gig = np.isin(self.uf, list(GIGANTES))
        return self.na_caixa & (self.dist_centro <= np.where(gig, lim_gig, lim))

    def resumo(self):
        f = self.filtro()
        return {'locais_com_coordenada': int(self.n), 'fora_da_caixa': int((~self.na_caixa).sum()),
                'longe_do_centroide': int((self.na_caixa & ~f).sum()), 'ficam': int(f.sum()),
                'fora_da_caixa_por_uf': dict(collections.Counter(self.uf[~self.na_caixa].tolist())),
                'longe_por_uf': dict(collections.Counter(self.uf[self.na_caixa & ~f].tolist()))}


LC = ['L1', 'R1', 'O1', 'BN1', 'C1', 'A1', 'L2', 'R2', 'BN2', 'C2', 'A2', 'Z1', 'CU1', 'CA1', 'RE1']
LX = {c: i for i, c in enumerate(LC)}
DESF = ['dbn', 'dcomp', 'dlula_bruta', 'dL_comp', 'dR_comp', 'dbn_apt', 'dabst_apt', 'dL_apt', 'dR_apt', 'O1_apt', 'bn1', 'bn2']
TODOS = ['lula_res'] + DESF + ['dbn_res', 'dcomp_res']


def agregar(k, M, geo, cand=None):
    """Soma as seções com os dois turnos por local do cadastro de 2026 (chave UF|município|zona|seção)."""
    m = (M[:, 0] >= 0) & (M[:, 7] >= 0)
    li = np.array([geo.sec.get(x, -1) for x in k.tolist()])
    m &= li >= 0
    T = np.zeros((geo.n, len(LC)))
    src = {'L1': M[:, IX['L1']], 'R1': M[:, IX['R1']], 'O1': M[:, IX['O1']], 'BN1': M[:, IX['B1']] + M[:, IX['N1']], 'C1': M[:, IX['C1']],
           'A1': M[:, IX['A1']], 'L2': M[:, IX['L2']], 'R2': M[:, IX['R2']], 'BN2': M[:, IX['B2']] + M[:, IX['N2']], 'C2': M[:, IX['C2']], 'A2': M[:, IX['A2']]}
    for c, v in src.items():
        T[:, LX[c]] = np.bincount(li[m], weights=v[m].astype(float), minlength=geo.n)
    if cand is not None:
        sc = cand['secoes']
        for c, num in (('Z1', '30'), ('CU1', '70'), ('CA1', '55'), ('RE1', '14')):
            v = np.array([sc.get(x, {}).get(num, 0) for x in k.tolist()], float)
            T[:, LX[c]] = np.bincount(li[m], weights=v[m], minlength=geo.n)
    return T, {'secoes_com_dois_turnos': int(((M[:, 0] >= 0) & (M[:, 7] >= 0)).sum()), 'ligadas_ao_cadastro_2026': int(m.sum())}


def desfechos(T):
    c = lambda x: T[:, LX[x]]
    with np.errstate(divide='ignore', invalid='ignore'):
        nom2 = c('L2') + c('R2')
        V = np.column_stack([
            100 * (c('BN2') / c('C2') - c('BN1') / c('C1')),
            100 * (c('C2') / c('A2') - c('C1') / c('A1')),
            100 * (c('L2') / nom2 - c('L1') / (c('L1') + c('R1'))),
            100 * (c('L2') / c('C2') - c('L1') / c('C1')),
            100 * (c('R2') / c('C2') - c('R1') / c('C1')),
            100 * (c('BN2') / c('A2') - c('BN1') / c('A1')),
            100 * ((c('A2') - c('C2')) / c('A2') - (c('A1') - c('C1')) / c('A1')),
            100 * (c('L2') / c('A2') - c('L1') / c('A1')),
            100 * (c('R2') / c('A2') - c('R1') / c('A1')),
            100 * c('O1') / c('A1'),
            100 * c('BN1') / c('C1'),
            100 * c('BN2') / c('C2')])
    return V


def validos(T, t34=False):
    c = lambda x: T[:, LX[x]]
    v = (c('L2') + c('R2') >= 100) & (c('C1') > 0)
    if not t34:
        v &= (c('A1') > 0) & (c('A2') > 0) & (c('C2') > 0) & (c('L1') + c('R1') > 0)
    return v


def desenho(T, ii, modelo):
    c = lambda x: T[ii, LX[x]]
    c1 = c('C1')
    base = [np.ones(len(ii)), c('L1') / c1, c('R1') / c1]
    if modelo == 'M0':
        el = [c('O1') / c1]
    elif modelo == 'M1':
        el = [c('Z1') / c1, c('CU1') / c1, (c('O1') - c('Z1') - c('CU1')) / c1]
    else:
        el = [c('Z1') / c1, c('CU1') / c1, c('CA1') / c1, c('RE1') / c1, (c('O1') - c('Z1') - c('CU1') - c('CA1') - c('RE1')) / c1]
    return np.column_stack(base + el + [np.log(np.maximum(c('A2'), 1))])


def divisa(T, V, geo, ma, mb, cap=20, hub='corta', modelo='M0', completo=True):
    """Método do T34 para os lados ma e mb (máscaras de locais já válidos e filtrados). Devolve os pares e as diferenças
    (lado b menos lado a) de cada desfecho de TODOS, em pontos percentuais."""
    ia, ib = np.where(ma)[0], np.where(mb)[0]
    if len(ia) == 0 or len(ib) == 0:
        return {'pares': 0, 'faixa': 0}
    Ta, Tb = cKDTree(geo.P[ia]), cKDTree(geo.P[ib])
    da, ja = Tb.query(geo.P[ia]); db, jb = Ta.query(geo.P[ib])
    faixa = np.concatenate([ia[da <= corda(100)], ib[db <= corda(100)]])
    if len(faixa) < 20:
        return {'pares': 0, 'faixa': int(len(faixa))}
    P = {}
    for q in np.where(da <= corda(20))[0]: P[(int(ia[q]), int(ib[ja[q]]))] = float(da[q])
    for q in np.where(db <= corda(20))[0]: P[(int(ia[jb[q]]), int(ib[q]))] = float(db[q])
    if not P:
        return {'pares': 0, 'faixa': int(len(faixa))}
    pk = sorted(P); pa = np.array([x[0] for x in pk]); pb = np.array([x[1] for x in pk]); pd = np.array([P[x] for x in pk])
    mult_antes = (int(np.bincount(pa).max()), int(np.bincount(pb).max()))
    if cap:
        if hub == 'corta':
            def posto(g):
                o = np.lexsort((pd, g)); r = np.empty(len(g), int); gs = g[o]
                ini = np.concatenate([[True], gs[1:] != gs[:-1]]); idx = np.arange(len(g)); r[o] = idx - np.maximum.accumulate(np.where(ini, idx, 0))
                return r
            fica = (posto(pa) < cap) & (posto(pb) < cap)
        else:
            fica = (np.bincount(pa)[pa] <= cap) & (np.bincount(pb)[pb] <= cap)
        pa, pb, pd = pa[fica], pb[fica], pd[fica]
    if len(pa) == 0:
        return {'pares': 0, 'faixa': int(len(faixa))}
    nom2 = T[:, LX['L2']] + T[:, LX['R2']]
    X = desenho(T, faixa, modelo); sw = np.sqrt(nom2[faixa]); wf = nom2[faixa]
    def residuo(y):
        beta = np.linalg.lstsq(X * sw[:, None], y * sw, rcond=None)[0]
        e = y - X @ beta
        r2 = 1 - np.average(e ** 2, weights=wf) / np.average((y - np.average(y, weights=wf)) ** 2, weights=wf)
        full = np.full(geo.n, np.nan); full[faixa] = e
        return full, float(r2)
    res, r2 = residuo(T[faixa, LX['L2']] / nom2[faixa])
    cols = [100 * (res[pb] - res[pa])]
    if completo:
        cols += [V[pb, j] - V[pa, j] for j in range(len(DESF))]
        for j in (0, 1):
            rj, _ = residuo(V[faixa, j]); cols.append(rj[pb] - rj[pa])
    return {'pares': int(len(pa)), 'faixa': int(len(faixa)), 'pa': pa, 'pb': pb, 'dist_km': km_de(pd), 'dif': np.column_stack(cols),
            'w': nom2[pa] + nom2[pb], 'r2_modelo': r2, 'mult_antes': mult_antes}


def estat(dif, w, grupos, reps, rng):
    """J = média ponderada das diferenças; ep por bootstrap dos grupos."""
    J = (w[:, None] * dif).sum(0) / w.sum()
    _, g = np.unique(grupos, return_inverse=True); G = g.max() + 1
    sw = np.bincount(g, weights=w, minlength=G)
    sd = np.column_stack([np.bincount(g, weights=w * dif[:, j], minlength=G) for j in range(dif.shape[1])])
    if G < 2:
        return J, np.full(dif.shape[1], np.nan), int(G)
    C = rng.multinomial(G, np.ones(G) / G, size=reps).astype(float)
    B = (C @ sd) / (C @ sw)[:, None]
    return J, B.std(0, ddof=1), int(G)


def junta(ds):
    ds = [d for d in ds if d.get('pares', 0) > 0]
    if not ds:
        return None
    return {'pa': np.concatenate([d['pa'] for d in ds]), 'pb': np.concatenate([d['pb'] for d in ds]),
            'dif': np.vstack([d['dif'] for d in ds]), 'w': np.concatenate([d['w'] for d in ds]), 'pares': sum(d['pares'] for d in ds)}


def resumo_divisa(d, geo, reps, rng, nomes=TODOS, por_divisa=True):
    """J e ep (três agrupamentos) de um conjunto de pares; e o detalhe por par de UFs."""
    if d is None or d.get('pares', 0) == 0:
        return {'pares': 0}
    J, ea, Ga = estat(d['dif'], d['w'], geo.grupo[d['pa']], reps, rng)
    _, eb, Gb = estat(d['dif'], d['w'], geo.grupo[d['pb']], reps, rng)
    par_uf = np.char.add(np.char.add(geo.uf[d['pa']], '-'), geo.uf[d['pb']])
    _, ed, Gd = estat(d['dif'], d['w'], par_uf, reps, rng)
    r = {'pares': int(d['pares']), 'locais_a': int(len(set(d['pa'].tolist()))), 'locais_b': int(len(set(d['pb'].tolist()))),
         'grupos_lado_a': Ga, 'grupos_lado_b': Gb, 'divisas': Gd, 'nominais_dos_pares': float(d['w'].sum()),
         'J': dict(zip(nomes, J.tolist())), 'ep': dict(zip(nomes, ea.tolist())), 'ep_lado_b': dict(zip(nomes, eb.tolist())),
         'ep_por_divisa': dict(zip(nomes, ed.tolist()))}
    if por_divisa:
        r['por_divisa'] = {}
        for pu in sorted(set(par_uf.tolist())):
            m = par_uf == pu
            Jp, ep, Gp = estat(d['dif'][m], d['w'][m], geo.grupo[d['pa'][m]], reps, rng)
            r['por_divisa'][pu] = {'pares': int(m.sum()), 'grupos_lado_a': Gp, 'J': dict(zip(nomes, Jp.tolist())), 'ep': dict(zip(nomes, ep.tolist()))}
    return r


def composto(T, V, geo, val, lado_a, lado_b, **kw):
    """Uma divisa composta por UF do lado a contra o conjunto do lado b; devolve a junção dos pares."""
    mb = val & np.isin(geo.uf, lado_b)
    ds = []
    for u in lado_a:
        d = divisa(T, V, geo, val & (geo.uf == u), mb, **kw)
        ds.append(d)
    return junta(ds), {u: {'pares': d.get('pares', 0), 'faixa': d.get('faixa', 0), 'r2_modelo': d.get('r2_modelo'), 'mult_antes': d.get('mult_antes')} for u, d in zip(lado_a, ds)}


def votos_de_J(J_pontos, N, m):
    """Votos somados a L que produzem um salto de J pontos na fatia de Lula, com N nominais e fatia m."""
    j = J_pontos / 100
    return j * N / (1 - m - j)


def parte_c(S, GOV, geo, cand26, reps=2000):
    rng = np.random.default_rng(SEMENTE + 2)
    out = {'filtro': geo.resumo(), 'orientacao': 'lado de um cargo só menos lado de dois cargos, em pontos percentuais', 'anos': {}}
    f = geo.filtro()
    LOC = {}
    for ano in ANOS:
        k, loc, M, _ = S[ano]
        T, lig = agregar(k, M, geo, cand26 if ano == 2026 else None)
        LOC[ano] = (T, desfechos(T), validos(T)); out['anos'][str(ano)] = {'ligacao': lig}
    sem_de = lambda ano: [u for u in UFS27 if u not in GOV[ano]]
    # 2026, principal
    T, V, val = LOC[2026]
    d, det = composto(T, V, geo, val & f, G6, sem_de(2026))
    r26 = resumo_divisa(d, geo, reps, rng); r26['composicao'] = det
    out['anos']['2026']['equivalente'] = r26
    diga(f"(c) 2026: pares {r26['pares']} | Lula res {r26['J']['lula_res']:+.3f} ({r26['ep']['lula_res']:.3f}) | dBN {r26['J']['dbn']:+.3f} ({r26['ep']['dbn']:.3f}) | "
         f"dcomp {r26['J']['dcomp']:+.3f} ({r26['ep']['dcomp']:.3f})")
    for pu, v in r26['por_divisa'].items():
        diga(f"      {pu}: pares {v['pares']} Lula {v['J']['lula_res']:+.3f} ({v['ep']['lula_res']:.3f}) dBN {v['J']['dbn']:+.3f} ({v['ep']['dbn']:.3f}) dcomp {v['J']['dcomp']:+.3f} ({v['ep']['dcomp']:.3f})")
    # sensibilidades do filtro em 2026
    sens = {}
    for nome, (ff, kw) in {'limite_100_300': (geo.filtro(100, 300), {}), 'tira_local_com_mais_de_20': (f, {'hub': 'tira'}),
                           'sem_filtro': (np.ones(geo.n, bool), {'cap': None}), 'sem_corte_de_multiplicidade': (f, {'cap': None})}.items():
        ds, _ = composto(T, V, geo, val & ff, G6, sem_de(2026), **kw)
        rs = resumo_divisa(ds, geo, reps, rng, por_divisa=False)
        sens[nome] = {'pares': rs['pares'], 'lula_res': [rs['J']['lula_res'], rs['ep']['lula_res']], 'dbn': [rs['J']['dbn'], rs['ep']['dbn']], 'dcomp': [rs['J']['dcomp'], rs['ep']['dcomp']]}
    dm2, _ = composto(T, V, geo, val & f, G6, sem_de(2026), modelo='M2')
    rm2 = resumo_divisa(dm2, geo, reps, rng)
    sens['modelo_M2_eliminados_separados'] = {'pares': rm2['pares'], 'lula_res': [rm2['J']['lula_res'], rm2['ep']['lula_res']],
                                              'por_divisa': {pu: [v['pares'], v['J']['lula_res'], v['ep']['lula_res']] for pu, v in rm2['por_divisa'].items()}}
    out['anos']['2026']['sensibilidade'] = sens
    diga('(c) 2026 sensibilidade:', json.dumps(sens, ensure_ascii=False))
    # outros anos: (E) equivalentes na condição; (G) as mesmas divisas de 2026
    for ano in (2014, 2018, 2022):
        T_, V_, val_ = LOC[ano]
        dE, detE = composto(T_, V_, geo, val_ & f, GOV[ano], sem_de(ano))
        rE = resumo_divisa(dE, geo, reps, rng); rE['composicao'] = detE
        dG, detG = composto(T_, V_, geo, val_ & f, G6, sem_de(2026))
        rG = resumo_divisa(dG, geo, reps, rng); rG['composicao'] = detG
        out['anos'][str(ano)]['equivalente'] = rE; out['anos'][str(ano)]['mesmas_divisas_de_2026'] = rG
        for nome, r in (('E', rE), ('G', rG)):
            diga(f"(c) {ano} ({nome}): pares {r['pares']} | PT res {r['J']['lula_res']:+.3f} ({r['ep']['lula_res']:.3f}) | dBN {r['J']['dbn']:+.3f} ({r['ep']['dbn']:.3f}) | dcomp {r['J']['dcomp']:+.3f} ({r['ep']['dcomp']:.3f})")
    # onde não deveria dar nada: todas as divisas de UF, em cada ano (também serve ao T34)
    todas = {}
    for ano in ANOS:
        T_, V_, val_ = LOC[ano]; todas[str(ano)] = {}
        for a, b in itertools.combinations(UFS27, 2):
            ca, cb_ = CAIXA[a], CAIXA[b]
            if ca[0] - 0.5 > cb_[1] or cb_[0] - 0.5 > ca[1] or ca[2] - 0.5 > cb_[3] or cb_[2] - 0.5 > ca[3]:
                continue
            dd = divisa(T_, V_, geo, val_ & f & (geo.uf == a), val_ & f & (geo.uf == b))
            if dd.get('pares', 0) < 50:
                if dd.get('pares', 0) > 0: todas[str(ano)][f'{a}-{b}'] = {'pares': dd['pares'], 'fora': 'menos de 50 pares'}
                continue
            J, e, G = estat(dd['dif'], dd['w'], geo.grupo[dd['pa']], reps, rng)
            _, e2, G2 = estat(dd['dif'], dd['w'], geo.grupo[dd['pb']], reps, rng)
            todas[str(ano)][f'{a}-{b}'] = {'pares': dd['pares'], 'faixa': dd['faixa'], 'grupos_lado_a': G, 'grupos_lado_b': G2, 'r2_modelo': dd['r2_modelo'],
                                           'J': {n_: float(J[TODOS.index(n_)]) for n_ in ('lula_res', 'dbn', 'dcomp', 'dR_comp', 'dL_comp')},
                                           'ep': {n_: float(max(e[TODOS.index(n_)], e2[TODOS.index(n_)]) if G2 > 1 and G > 1 else (e[TODOS.index(n_)] if G > 1 else e2[TODOS.index(n_)]))
                                                  for n_ in ('lula_res', 'dbn', 'dcomp', 'dR_comp', 'dL_comp')}}
    out['todas_as_divisas'] = todas
    def mesmo_grupo(ano):
        com = set(GOV[ano]); r = {}
        for dv, v in todas[str(ano)].items():
            a, b = dv.split('-')
            if 'J' in v and ((a in com) == (b in com)): r[dv] = v
        return r
    nulo = {}
    for ano in ANOS:
        mg = mesmo_grupo(ano)
        if not mg: continue
        jl = np.array([v['J']['lula_res'] for v in mg.values()]); jb = np.array([v['J']['dbn'] for v in mg.values()])
        wv = np.array([v['pares'] for v in mg.values()], float)
        nulo[str(ano)] = {'n_divisas': len(mg), 'lula_res_abs_mediana': float(np.median(np.abs(jl))), 'lula_res_abs_p90': float(np.percentile(np.abs(jl), 90)), 'lula_res_abs_max': float(np.abs(jl).max()),
                          'lula_res_dp': float(np.sqrt((jl ** 2).mean())), 'dbn_abs_mediana': float(np.median(np.abs(jb))), 'dbn_abs_p90': float(np.percentile(np.abs(jb), 90)),
                          'dbn_abs_max': float(np.abs(jb).max()), 'dbn_dp': float(np.sqrt((jb ** 2).mean()))}
    out['divisas_do_mesmo_grupo'] = nulo
    diga('(c) divisas do mesmo grupo (nada deveria saltar):', json.dumps(nulo))
    # calibração: plantio de 35% nas 21
    k, loc, M, _ = S[2026]; g21 = ~np.isin(ufs_de(k), G6 + ['ZZ']); pl = {}
    c21 = contab(k, M, G6)['sem_gov_2t']
    for nome, frac in (('35', 0.35), ('53.8', 0.35 / 0.65)):
        M2, tot = plantio_secoes(M, g21, frac, np.random.default_rng(SEMENTE))
        T2, _ = agregar(k, M2, geo, cand26); V2 = desfechos(T2)
        d2, _ = composto(T2, V2, geo, validos(T2) & f, G6, sem_de(2026))
        r2 = resumo_divisa(d2, geo, reps, rng, por_divisa=False)
        # esperado nos pares: média ponderada de -frac*bn2 do lado b e do ganho de fatia correspondente
        pb = d['pb']; w = d['w']; bn2 = T[pb, LX['BN2']]; nom = T[pb, LX['L2']] + T[pb, LX['R2']]; l2 = T[pb, LX['L2']]
        esp_bn = float((w * (-100 * frac * bn2 / T[pb, LX['C2']])).sum() / w.sum())
        esp_l = float((w * 100 * ((l2 + frac * bn2) / (nom + frac * bn2) - l2 / nom)).sum() / w.sum())
        pl[nome] = {'votos_plantados': tot, 'pares': r2['pares'],
                    'lula_res': [r2['J']['lula_res'], r2['ep']['lula_res']], 'dbn': [r2['J']['dbn'], r2['ep']['dbn']], 'dcomp': [r2['J']['dcomp'], r2['ep']['dcomp']],
                    'desloc_lula': r2['J']['lula_res'] - r26['J']['lula_res'], 'desloc_dbn': r2['J']['dbn'] - r26['J']['dbn'],
                    'esperado_lula_bruto': esp_l, 'esperado_dbn': esp_bn,
                    'sinal_dispara': bool(r2['J']['dbn'] <= -1.0 and abs(r2['J']['dbn']) > 4 * r2['ep']['dbn'] and r2['J']['lula_res'] >= 0.5 and r2['J']['lula_res'] > 3 * r2['ep']['lula_res'])}
        pl[nome]['poder_de_medida'] = bool(pl[nome]['desloc_dbn'] / esp_bn >= 0.8 and abs(pl[nome]['desloc_dbn']) > 4 * r26['ep']['dbn']
                                           and pl[nome]['desloc_lula'] / esp_l >= 0.8 and pl[nome]['desloc_lula'] > 3 * r26['ep']['lula_res'])
    out['plantio_21_ufs'] = pl
    diga('(c) plantio:', json.dumps(pl))
    # critério
    jl, el = r26['J']['lula_res'], r26['ep']['lula_res']; jb, eb = r26['J']['dbn'], r26['ep']['dbn']
    eqs = {str(a): [out['anos'][str(a)]['equivalente']['J']['lula_res'], out['anos'][str(a)]['equivalente']['ep']['lula_res']] for a in (2014, 2018, 2022)}
    crit = {'salto_bn_2026': [jb, eb, jb / eb], 'salto_lula_2026': [jl, el, jl / el], 'salto_lula_equivalentes': eqs,
            'cond_bn': bool(jb <= -1.0 and abs(jb) > 4 * eb), 'cond_lula': bool(jl >= 0.5 and jl > 3 * el),
            'cond_outros_anos_pela_letra': bool(all(v[0] < 0.25 for v in eqs.values())), 'cond_outros_anos_em_modulo': bool(all(abs(v[0]) < 0.25 for v in eqs.values())),
            'sem_sinal_pelo_salto_de_lula': bool(abs(jl) < 0.25 and el <= 0.12)}
    crit['sinal'] = bool(crit['cond_bn'] and crit['cond_lula'] and crit['cond_outros_anos_pela_letra'])
    out['criterio'] = crit
    N21, m21 = c21['nominais_2t'], c21['fatia_L_2t']
    out['traducao_votos'] = {'nominais_2t_21_ufs': N21, 'fatia_L_21_ufs': m21, 'comp_2t_21_ufs': c21['comp_2t'],
                             'salto_lula_em_votos': votos_de_J(jl, N21, m21), 'limite_sup_95_em_votos': votos_de_J(jl + 1.96 * el, N21, m21),
                             'limite_inf_95_em_votos': votos_de_J(jl - 1.96 * el, N21, m21),
                             'salto_bn_em_votos': jb / 100 * c21['comp_2t'], 'salto_bn_ic95_em_votos': [(jb - 1.96 * eb) / 100 * c21['comp_2t'], (jb + 1.96 * eb) / 100 * c21['comp_2t']]}
    diga('(c) criterio:', json.dumps(crit)); diga('(c) votos:', json.dumps(out['traducao_votos']))
    return out, LOC


# ---------------------------------------------------------------- T34 corrigido
def parte_t(S, geo, LOC, cand26, c_out, reps=2000):
    rng = np.random.default_rng(SEMENTE + 3)
    out = {}
    f = geo.filtro(); tudo = np.ones(geo.n, bool)
    lista = [T34_PRINCIPAL] + T34_DESCRITIVAS + T34_PLACEBO
    def uma(ano, dv, filtrar, modelo='M0'):
        T, V, _ = LOC[ano]; v34 = validos(T, t34=True)
        a, b = dv.split('-')
        ma = v34 & np.isin(geo.uf, a.split('+')) & (f if filtrar else tudo); mb = v34 & np.isin(geo.uf, b.split('+')) & (f if filtrar else tudo)
        d = divisa(T, V, geo, ma, mb, cap=20 if filtrar else None, modelo=modelo, completo=False)
        if d.get('pares', 0) < 50:
            return {'pares': d.get('pares', 0), 'faixa': d.get('faixa', 0), 'fora': 'menos de 50 pares'}
        J, e, G = estat(d['dif'], d['w'], geo.mun[d['pa']] if not filtrar else geo.grupo[d['pa']], reps, rng)
        return {'pares': d['pares'], 'faixa': d['faixa'], 'municipios_lado_a': G, 'J': float(J[0]) / 100, 'ep': float(e[0]) / 100, 'r2_modelo': d['r2_modelo'], 'mult_antes_do_corte': d['mult_antes']}
    for rot, filtrar in (('sem_filtro', False), ('com_filtro', True)):
        out[rot] = {str(ano): {dv: uma(ano, dv, filtrar) for dv in lista} for ano in (2026, 2022)}
        r = out[rot]
        p26 = r['2026'][T34_PRINCIPAL]; p22 = r['2022'][T34_PRINCIPAL]
        pl = [abs(r['2026'][dv]['J']) for dv in T34_PLACEBO if 'J' in r['2026'][dv]]
        med = float(np.median(pl))
        dJ = p26['J'] - p22['J']; edJ = math.hypot(p26['ep'], p22['ep'])
        sinal = p26['J'] >= 0.015 and p26['J'] > 2.5 * p26['ep'] and dJ >= 0.015 and dJ > 2.5 * edJ
        sem = p26['J'] <= 0.008 and p26['ep'] <= 0.005
        r['criterio'] = {'J_2026': [p26['J'], p26['ep']], 'J_2022': [p22['J'], p22['ep']], 'dif': [dJ, edJ], 'mediana_abs_J_placebo_2026': med, 'n_placebo': len(pl),
                         'veredito': ('INCONCLUSIVO' if sinal and med > 0.01 else 'SINAL') if sinal else ('SEM SINAL' if sem else 'INCONCLUSIVO')}
        diga(f'(T34) {rot}:', json.dumps(r['criterio']))
        for dv in lista:
            diga(f"      {dv}: 2026 {r['2026'][dv]} | 2022 {r['2022'][dv]}")
    # todas as divisas, 2026 e 2022, com Bonferroni
    t26, t22 = c_out['todas_as_divisas']['2026'], c_out['todas_as_divisas']['2022']
    com = [dv for dv in t26 if 'J' in t26[dv]]
    n = len(com); z = float(norm.ppf(1 - 0.0062 / n))
    tb = {}
    for dv in com:
        j26, e26 = t26[dv]['J']['lula_res'] / 100, t26[dv]['ep']['lula_res'] / 100
        r = {'pares': t26[dv]['pares'], 'J_2026': j26, 'ep_2026': e26, 'z_2026': j26 / e26}
        if dv in t22 and 'J' in t22[dv]:
            j22, e22 = t22[dv]['J']['lula_res'] / 100, t22[dv]['ep']['lula_res'] / 100
            r.update({'J_2022': j22, 'ep_2022': e22, 'dif': j26 - j22, 'ep_dif': math.hypot(e26, e22)})
            r['passa'] = bool(abs(j26) >= 0.015 and abs(j26) > z * e26 and abs(r['dif']) >= 0.015 and abs(r['dif']) > z * r['ep_dif'] and (j26 > 0) == (r['dif'] > 0))
            r['passa_sem_bonferroni'] = bool(abs(j26) >= 0.015 and abs(j26) > 2.5 * e26 and abs(r['dif']) >= 0.015 and abs(r['dif']) > 2.5 * r['ep_dif'] and (j26 > 0) == (r['dif'] > 0))
        tb[dv] = r
    out['todas_as_divisas'] = {'n_divisas_com_50_pares': n, 'z_bonferroni': z, 'tabela': tb, 'passam': [dv for dv in tb if tb[dv].get('passa')],
                               'passam_sem_bonferroni': [dv for dv in tb if tb[dv].get('passa_sem_bonferroni')],
                               'mediana_abs_J_2026': float(np.median([abs(v['J_2026']) for v in tb.values()])),
                               'nota': 'ep = o maior entre o bootstrap de municípios do lado a e o do lado b; modelo por divisa; |J| porque não há direção prevista'}
    diga('(T34) todas as divisas:', n, 'z', round(z, 3), 'passam', out['todas_as_divisas']['passam'], 'sem Bonferroni', out['todas_as_divisas']['passam_sem_bonferroni'],
         'mediana |J|', out['todas_as_divisas']['mediana_abs_J_2026'])
    # SP-MG e as outras divisas de MG: composição dos eliminados
    comp = {}
    T, V, _ = LOC[2026]; v34 = validos(T, t34=True)
    for dv in ('SP-MG', 'MG-RJ', 'MG-GO', 'ES-MG', 'BA-MG', 'DF-GO', 'GO-MT', 'PR-SP+MS', 'PR-SC'):
        r = {m_: uma(2026, dv, True, m_) for m_ in ('M0', 'M1', 'M2')}
        a, b = dv.split('-'); ma = v34 & np.isin(geo.uf, a.split('+')) & f; mb = v34 & np.isin(geo.uf, b.split('+')) & f
        d = divisa(T, V, geo, ma, mb, completo=False)
        if d.get('pares', 0) >= 50:
            w = d['w']; fat = lambda c, ii: float((w * 100 * T[ii, LX[c]] / T[ii, LX['C1']]).sum() / w.sum())
            r['fatias_1t_nos_pares_pct_comp'] = {lado: {c: fat(c, ii) for c in ('L1', 'R1', 'O1', 'Z1', 'CU1', 'CA1', 'RE1', 'BN1')} for lado, ii in (('a', d['pa']), ('b', d['pb']))}
            if 'J' in r['M0'] and 'J' in r['M1']:
                r['explicada_pela_composicao'] = bool(abs(r['M1']['J']) <= abs(r['M0']['J']) / 2 and abs(r['M1']['J']) < 2 * r['M1']['ep'])
        comp[dv] = r
        diga(f'(T34) {dv} por modelo:', {m_: (round(r[m_]['J'], 5), round(r[m_]['ep'], 5), r[m_]['pares']) if 'J' in r[m_] else r[m_] for m_ in ('M0', 'M1', 'M2')}, r.get('explicada_pela_composicao'))
    out['composicao_dos_eliminados'] = comp
    return out


# ---------------------------------------------------------------- exploratório (depois de ver os resultados)
PASTA_RDV = '/home/user/trabalho-eleicao/amostra2t/arq'


def amostra_b2(k, loc, M):
    """A amostra e as matrizes da especificação (b2) do D4-6, como em parte_d (variante d, eliminados somados)."""
    uf = ufs_de(k)
    m = ((M[:, 0] >= 0) & (M[:, 7] >= 0) & (M[:, IX['ap1']] == 1) & (M[:, IX['ap2']] == 1) & (np.abs(M[:, IX['A2']] - M[:, IX['A1']]) <= 2)
         & (M[:, IX['C1']] >= 30) & (uf != 'ZZ') & (M[:, IX['A1']] > 0))
    Mm = M[m].astype(float); c = lambda x: Mm[:, IX[x]]
    mun = np.array(['|'.join(x.split('|')[:2]) for x in k[m]]); w = 1 / c('A1')
    Xd = np.column_stack([c('L1'), c('R1'), c('O1'), c('B1'), c('N1'), c('A1') - c('C1')])
    return m, uf[m], loc[m], mun, w, Xd, c


def boot_razao(num, den, w, grupos, reps, rng):
    """Razão de duas médias ponderadas (num/den) com intervalo de 95% por bootstrap dos grupos."""
    _, g = np.unique(grupos, return_inverse=True); G = g.max() + 1
    sn = np.bincount(g, weights=w * num, minlength=G); sd = np.bincount(g, weights=w * den, minlength=G)
    C = rng.multinomial(G, np.ones(G) / G, size=reps).astype(float)
    b = (C @ sn) / (C @ sd)
    return [float(sn.sum() / sd.sum()), float(np.percentile(b, 2.5)), float(np.percentile(b, 97.5))]


def exploratorio(S, GOV, geo, LOC, res, cand26, reps=2000):
    """Tudo aqui foi acrescentado depois de ver os resultados das partes registradas. Não muda veredito."""
    from scipy.stats import mannwhitneyu
    rng = np.random.default_rng(SEMENTE + 4)
    x = {'aviso': 'EXPLORATÓRIO: contas escolhidas depois de ver os resultados das partes registradas; não mudam veredito pela letra'}
    f = geo.filtro()
    T, V, val = LOC[2026]; v34 = validos(T, t34=True)
    sem_de = lambda ano: [u for u in UFS27 if u not in GOV[ano]]

    # X1: SP-MG e MG-RJ sem filtro, por modelo, e sem os locais que viram par de centenas de locais
    def jt(ma, mb, modelo):
        d = divisa(T, V, geo, ma, mb, cap=None, modelo=modelo, completo=False)
        if d.get('pares', 0) < 50:
            return {'pares': d.get('pares', 0)}, d
        J, e, G = estat(d['dif'], d['w'], geo.mun[d['pa']], reps, rng)
        return {'pares': d['pares'], 'J': float(J[0]) / 100, 'ep': float(e[0]) / 100, 'municipios_lado_a': G, 'mult_maxima': d['mult_antes']}, d
    x1 = {}
    for dv in ('SP-MG', 'MG-RJ'):
        a, b = dv.split('-'); ma = v34 & (geo.uf == a); mb = v34 & (geo.uf == b); r = {}
        d0 = None
        for m_ in ('M0', 'M1', 'M2'):
            r['sem_filtro_' + m_], d = jt(ma, mb, m_)
            if m_ == 'M0': d0 = d
        ca = np.bincount(d0['pa'], minlength=geo.n); cb_ = np.bincount(d0['pb'], minlength=geo.n)
        hubs = np.where((ca > 200) | (cb_ > 200))[0]
        r['locais_com_mais_de_200_pares'] = [{'local': str(geo.lid[h]), 'lat': float(geo.lat[h]), 'lon': float(geo.lon[h]), 'pares': int(max(ca[h], cb_[h])),
                                             'km_do_centroide_do_municipio': float(geo.dist_centro[h]), 'dentro_da_caixa_da_uf': bool(geo.na_caixa[h]),
                                             'passa_no_filtro': bool(f[h]), 'nominais_2t': float(T[h, LX['L2']] + T[h, LX['R2']])} for h in hubs]
        eh = np.isin(d0['pa'], hubs) | np.isin(d0['pb'], hubs); w = d0['w']; dj = d0['dif'][:, 0] / 100
        r['pares_desses_locais'] = {'pares': int(eh.sum()), 'peso_no_J': float(w[eh].sum() / w.sum()),
                                    'J_so_deles': float((w[eh] * dj[eh]).sum() / w[eh].sum()) if eh.any() else None,
                                    'J_dos_demais_sem_reajustar_o_modelo': float((w[~eh] * dj[~eh]).sum() / w[~eh].sum()) if (~eh).any() else None}
        fora = np.ones(geo.n, bool); fora[hubs] = False; tirados = list(hubs)
        for _ in range(30):  # locais com a mesma coordenada herdam os pares do que saiu: tira até não sobrar nenhum com mais de 200
            d1 = divisa(T, V, geo, ma & fora, mb & fora, cap=None, completo=False)
            c1 = np.bincount(d1['pa'], minlength=geo.n) + np.bincount(d1['pb'], minlength=geo.n)
            h1 = np.where(c1 > 200)[0]
            if len(h1) == 0: break
            fora[h1] = False; tirados += list(h1)
        r['locais_tirados_ao_todo'] = [{'local': str(geo.lid[h]), 'lat': float(geo.lat[h]), 'lon': float(geo.lon[h]), 'km_do_centroide_do_municipio': float(geo.dist_centro[h]),
                                       'dentro_da_caixa_da_uf': bool(geo.na_caixa[h]), 'passa_no_filtro': bool(f[h])} for h in tirados]
        for m_ in ('M0', 'M1'):
            r['sem_filtro_sem_esses_locais_' + m_], _ = jt(ma & fora, mb & fora, m_)
        x1[dv] = r
        diga(f'(X1) {dv}:', json.dumps(limpar(r), ensure_ascii=False))
    x['X1_sp_mg_e_mg_rj_sem_filtro'] = x1

    # X2: permutação da DiD do item (b) em cada ano (200 mil sorteios)
    x2 = {}
    for ano in ANOS:
        k, loc, M, _ = S[ano]; U = somas_uf(k, M); rb = res['b']['anos'][str(ano)]
        du = np.array([rb['var_por_uf'][u] for u in UFS27]); nc = len(GOV[ano])
        V4 = np.array([[U[u]['bn1'], U[u]['c1'], U[u]['bn2'], U[u]['c2']] for u in UFS27])
        idx = np.argsort(rng.random((200000, 27)), axis=1)[:, :nc]
        sg = du[idx].sum(1); ms = (du.sum() - sg) / (27 - nc) - sg / nc
        Vc = V4[idx].sum(1); Vs = V4.sum(0)[None, :] - Vc
        ag = 100 * ((Vs[:, 2] / Vs[:, 3] - Vs[:, 0] / Vs[:, 1]) - (Vc[:, 2] / Vc[:, 3] - Vc[:, 0] / Vc[:, 1]))
        x2[str(ano)] = {'ufs_com_gov_2t': nc, 'did_media_simples': rb['did_media_simples'], 'dp_permutacao_media_simples': float(ms.std()),
                        'p_tao_negativa_media_simples': float((ms <= rb['did_media_simples'] + 1e-12).mean()),
                        'did_agregada': rb['did_agregada'], 'dp_permutacao_agregada': float(ag.std()),
                        'p_tao_negativa_agregada': float((ag <= rb['did_agregada'] + 1e-12).mean())}
        diga(f'(X2) {ano}:', json.dumps(x2[str(ano)]))
    x['X2_permutacao_da_did_por_ano'] = x2

    # X3: D4-6(b1), teste de postos e conversão equivalente
    b1 = res['d']['b1']
    plac = np.array([v['DiD'] for a in ('2018', '2022') for v in b1['por_uf'][a].values()]); seis = np.array([b1['seis_DiD'][u] for u in G6])
    bn6 = sum(b1['por_uf']['2026'][u]['bn_pres_2t'] for u in G6)
    dmed = float(np.median(seis) - np.median(plac))
    x['X3_d46_b1_postos'] = {'mediana_6': float(np.median(seis)), 'mediana_placebo': float(np.median(plac)), 'dif_medianas': dmed,
                             'p_mann_whitney_menor': float(mannwhitneyu(seis, plac, alternative='less').pvalue),
                             'p_mann_whitney_bilateral': float(mannwhitneyu(seis, plac, alternative='two-sided').pvalue),
                             'conversao_equivalente_fracao_do_bn_antes': float(1 - math.exp(dmed)) if dmed < 0 else 0.0,
                             'bn_presidente_2t_nas_6_ufs': bn6,
                             'conversao_equivalente_votos': float(bn6 * (math.exp(-dmed) - 1)) if dmed < 0 else 0.0,
                             'seis_abaixo_da_mediana_placebo': int((seis < np.median(plac)).sum()),
                             'conversao_compativel_com_o_p90_do_placebo': float(max(0.0, 1 - math.exp(np.median(seis) - np.percentile(plac, 90)))),
                             'conversao_compativel_com_o_maximo_do_placebo': float(max(0.0, 1 - math.exp(np.median(seis) - plac.max()))),
                             'bn_presidente_2t_no_pais': res['a']['calibracao_2026_nacional']['bn_2t_nas_secoes'],
                             'nota': 'se a diferença de medianas inteira fosse conversão: votos = B+N observado vezes (exp(-dif) - 1)'}
    x3_ = x['X3_d46_b1_postos']
    x3_['votos_no_pais_se_a_taxa_valesse_nas_27'] = {n_: float(x3_['bn_presidente_2t_no_pais'] * f_ / (1 - f_)) for n_, f_ in
                                                     (('mediana', x3_['conversao_equivalente_fracao_do_bn_antes']), ('p90', x3_['conversao_compativel_com_o_p90_do_placebo']),
                                                      ('maximo', x3_['conversao_compativel_com_o_maximo_do_placebo']))}
    diga('(X3)', json.dumps(x3_))

    # X4: o que foi digitado nos nulos de presidente do 2º turno (RDV da amostra)
    try:
        from decodificar import ler_rdv
        ELIM = set(cand26['nomes']) - {'13', '22'}
        por_uf = {}
        for uf in sorted(_os.listdir(PASTA_RDV)):
            a = collections.Counter(); nsec = 0; gv = collections.Counter(); nulp = collections.Counter(); nulg = collections.Counter()
            for m_ in sorted(_os.listdir(_os.path.join(PASTA_RDV, uf))):
                for z_ in sorted(_os.listdir(_os.path.join(PASTA_RDV, uf, m_))):
                    for s_ in sorted(_os.listdir(_os.path.join(PASTA_RDV, uf, m_, z_))):
                        p_ = _os.path.join(PASTA_RDV, uf, m_, z_, s_)
                        rd = sorted(q for q in _os.listdir(p_) if q.endswith('-rdv.dat'))
                        if not rd: continue
                        try: c = ler_rdv(_os.path.join(p_, rd[-1]))
                        except Exception: a['rdv_ilegivel'] += 1; continue
                        nsec += 1
                        for (ide, cod, tipo, dig), q in c.items():
                            if cod == 1:
                                a['pres_total'] += q
                                a[{2: 'pres_nominal', 3: 'pres_branco', 4: 'pres_nulo_digitado', 6: 'pres_nulo_sem_digito'}.get(tipo, 'pres_outro')] += q
                                if tipo == 4: nulp[dig] += q
                                if tipo == 2 and dig in ('13', '22'): a['pres_' + dig] += q
                            elif cod == 3:
                                a['gov_total'] += q
                                a[{2: 'gov_nominal', 3: 'gov_branco', 4: 'gov_nulo_digitado', 6: 'gov_nulo_sem_digito'}.get(tipo, 'gov_outro')] += q
                                if tipo == 2: gv[dig] += q
                                if tipo == 4: nulg[dig] += q
            if nsec == 0: continue
            fin = [n_ for n_, _ in gv.most_common(2)]
            r = {'secoes_com_rdv': nsec, **{k_: int(v) for k_, v in a.items()}, 'finalistas_gov': fin,
                 'nulo_pres_com_numero_de_eliminado': int(sum(q for d_, q in nulp.items() if d_ in ELIM)),
                 'nulo_pres_mais_digitados': nulp.most_common(8)}
            if fin:
                r['nulo_pres_com_numero_de_finalista_gov'] = int(sum(q for d_, q in nulp.items() if d_ in fin and d_ not in ('13', '22')))
                r['nulo_gov_com_13_ou_22'] = int(sum(q for d_, q in nulg.items() if d_ in ('13', '22') and d_ not in fin))
                r['nulo_gov_com_13'] = int(nulg.get('13', 0)) if '13' not in fin else None
                r['nulo_gov_com_22'] = int(nulg.get('22', 0)) if '22' not in fin else None
                if r['nulo_gov_com_13'] is not None and r['nulo_gov_com_22'] is not None and r['nulo_gov_com_13_ou_22'] > 0:
                    r['fatia_13_entre_os_que_digitaram_presidente_na_tela_de_gov'] = r['nulo_gov_com_13'] / r['nulo_gov_com_13_ou_22']
                    r['fatia_13_nos_nominais_de_presidente_das_mesmas_secoes'] = a['pres_13'] / max(a['pres_13'] + a['pres_22'], 1)
                r['nulo_gov_mais_digitados'] = nulg.most_common(8)
                r['pct_do_comparecimento_nulo_pres_com_numero_de_gov'] = 100 * r['nulo_pres_com_numero_de_finalista_gov'] / max(a['pres_total'], 1)
                r['pct_do_bn_pres_que_e_numero_de_gov'] = 100 * r['nulo_pres_com_numero_de_finalista_gov'] / max(a['pres_branco'] + a['pres_nulo_digitado'] + a['pres_nulo_sem_digito'], 1)
            r['bn_pres_pct'] = 100 * (a['pres_branco'] + a['pres_nulo_digitado'] + a['pres_nulo_sem_digito']) / max(a['pres_total'], 1)
            r['_nulp'] = dict(nulp)
            por_uf[uf.upper()] = r
        x4 = {'por_uf': por_uf, 'secoes': int(sum(v['secoes_com_rdv'] for v in por_uf.values()))}
        # régua: os mesmos números dos finalistas do AC digitados como nulo de presidente nas UFs sem 2º turno de governador
        for u6 in [u for u in por_uf if por_uf[u].get('finalistas_gov')]:
            fin = [n_ for n_ in por_uf[u6]['finalistas_gov'] if n_ not in ('13', '22')]
            fora = [u for u in por_uf if not por_uf[u].get('finalistas_gov')]
            tot = sum(por_uf[u]['pres_total'] for u in fora); q = sum(por_uf[u]['_nulp'].get(n_, 0) for u in fora for n_ in fin)
            x4[f'regua_{u6}'] = {'numeros': fin, 'pct_do_comparecimento_nas_ufs_sem_gov_2t': 100 * q / max(tot, 1), 'votos': int(q), 'comparecimento': int(tot),
                                 'pct_do_comparecimento_na_propria_uf': por_uf[u6].get('pct_do_comparecimento_nulo_pres_com_numero_de_gov')}
        for v in por_uf.values(): v.pop('_nulp', None)
        x['X4_nulos_digitados_rdv'] = x4
        diga('(X4)', json.dumps({u: {k_: v for k_, v in r.items() if k_ in ('secoes_com_rdv', 'pres_total', 'bn_pres_pct', 'finalistas_gov', 'nulo_pres_com_numero_de_finalista_gov',
                                                                           'pct_do_comparecimento_nulo_pres_com_numero_de_gov', 'pct_do_bn_pres_que_e_numero_de_gov', 'nulo_gov_com_13_ou_22')}
                                 for u, r in por_uf.items()}, ensure_ascii=False), json.dumps({k_: v for k_, v in x4.items() if k_.startswith('regua')}))
    except Exception as e:
        x['X4_nulos_digitados_rdv'] = {'erro': repr(e)}; diga('(X4) erro', repr(e))

    # X5 e X9: votos pela calibração do plantio nas divisas
    c = res['c']; p35 = c['plantio_21_ufs']['35']; jl, el = c['criterio']['salto_lula_2026'][:2]; jb, eb = c['criterio']['salto_bn_2026'][:2]
    el_div = c['anos']['2026']['equivalente']['ep_por_divisa']['lula_res']; eb_div = c['anos']['2026']['equivalente']['ep_por_divisa']['dbn']
    vpl = p35['votos_plantados'] / p35['desloc_lula']; vpb = p35['votos_plantados'] / p35['desloc_dbn']
    lula_tudo = p35['desloc_lula'] * jb / p35['desloc_dbn']
    x['X5_votos_pela_calibracao_do_plantio'] = {
        'votos_por_ponto_de_salto_de_lula': vpl, 'votos_por_ponto_de_salto_de_bn': vpb,
        'salto_lula_em_votos': jl * vpl, 'salto_lula_ic95_em_votos': [(jl - 1.96 * el) * vpl, (jl + 1.96 * el) * vpl],
        'salto_lula_ic95_em_votos_ep_por_divisa': [(jl - 1.96 * el_div) * vpl, (jl + 1.96 * el_div) * vpl],
        'salto_bn_em_votos': jb * vpb, 'salto_bn_ic95_em_votos': [(jb + 1.96 * eb) * vpb, (jb - 1.96 * eb) * vpb],
        'salto_de_lula_se_o_salto_inteiro_do_bn_fosse_conversao': lula_tudo,
        'observado_sobre_isso': jl / lula_tudo, 'z_observado_contra_isso': (jl - lula_tudo) / el, 'z_observado_contra_isso_ep_por_divisa': (jl - lula_tudo) / el_div,
        'z_observado_contra_zero': jl / el, 'z_observado_contra_zero_ep_por_divisa': jl / el_div,
        'pct_da_margem_salto_lula': 100 * jl * vpl / MARGEM, 'pct_da_margem_salto_bn': 100 * jb * vpb / MARGEM,
        'nota': 'votos = salto observado vezes (votos plantados / deslocamento medido com o plantio de 35% nas 21 UFs); vale se a conversão for proporcional ao B+N de cada seção'}
    fator = MARGEM / p35['votos_plantados']
    x['X9_conversao_que_viraria_so_nas_21'] = {
        'votos': MARGEM, 'bn_observado_2t_nas_21': c['traducao_votos']['comp_2t_21_ufs'] * res['b']['anos']['2026']['contabilidade_pct_aptos']['sem_gov_2t']['bn2_pct_comp'] / 100,
        'salto_bn_esperado': p35['desloc_dbn'] * fator, 'salto_lula_esperado': p35['desloc_lula'] * fator,
        'salto_bn_observado': jb, 'salto_lula_observado': jl, 'observado_sobre_esperado_bn': jb / (p35['desloc_dbn'] * fator), 'observado_sobre_esperado_lula': jl / (p35['desloc_lula'] * fator),
        'z_lula_observado_contra_esperado': (jl - p35['desloc_lula'] * fator) / el, 'z_lula_observado_contra_esperado_ep_por_divisa': (jl - p35['desloc_lula'] * fator) / el_div,
        'nota': 'extrapolação linear do plantio de 35%; supõe que as 6 UFs ficaram limpas e que o salto de base seria zero'}
    diga('(X5)', json.dumps(x['X5_votos_pela_calibracao_do_plantio'])); diga('(X9)', json.dumps(x['X9_conversao_que_viraria_so_nas_21']))

    # X6: (b2) em votos, com a diferença L2 - R2 como resposta (erro-padrão próprio)
    x6 = {}
    for ano in ANOS:
        k, loc, M, _ = S[ano]
        m, ufm, locm, mun, w, Xd, cc = amostra_b2(k, loc, M)
        Y = np.column_stack([cc('L2') - cc('R2'), cc('L2'), cc('R2')]); nx = ['L1', 'R1', 'O1', 'B1', 'N1', 'A1']
        def conta(g):
            r = fe_ols_multi(Y[g], Xd[g], locm[g], mun[g], w[g], nx, ['L2_menos_R2', 'L2', 'R2'])
            e = r['eq']['L2_menos_R2']; sb, sn = float(cc('B1')[g].sum()), float(cc('N1')[g].sum())
            return {'n': r['n'], 'coef_B1': [e['coef']['B1'], e['ep']['B1']], 'coef_N1': [e['coef']['N1'], e['ep']['N1']], 'brancos_1t': sb, 'nulos_1t': sn,
                    'votos_de_margem_associados': e['coef']['B1'] * sb + e['coef']['N1'] * sn,
                    'ep_votos': math.hypot(e['ep']['B1'] * sb, e['ep']['N1'] * sn),
                    'coef_L2': [r['eq']['L2']['coef']['B1'], r['eq']['L2']['coef']['N1']], 'coef_R2': [r['eq']['R2']['coef']['B1'], r['eq']['R2']['coef']['N1']],
                    'coef_outros_L2_menos_R2': [e['coef']['O1'], e['ep']['O1']], 'coef_abstencao_1t_L2_menos_R2': [e['coef']['A1'], e['ep']['A1']]}
        r = {'todas': conta(np.ones(len(ufm), bool)), 'com_gov_2t': conta(np.isin(ufm, GOV[ano])), 'sem_gov_2t': conta(~np.isin(ufm, GOV[ano]))}
        x6[str(ano)] = r
        diga(f"(X6) {ano}: L2-R2 ~ B1 {r['todas']['coef_B1'][0]:+.4f} ({r['todas']['coef_B1'][1]:.4f}) N1 {r['todas']['coef_N1'][0]:+.4f} ({r['todas']['coef_N1'][1]:.4f}) "
             f"votos {r['todas']['votos_de_margem_associados']:,.0f} | sem gov {r['sem_gov_2t']['coef_B1'][0]:+.4f} {r['sem_gov_2t']['coef_N1'][0]:+.4f} | com gov {r['com_gov_2t']['coef_B1'][0]:+.4f} {r['com_gov_2t']['coef_N1'][0]:+.4f}")
    x['X6_b2_em_votos'] = x6

    # X7: salto de 2026 menos o salto de cada outro ano nas mesmas seis divisas
    e26 = c['anos']['2026']['equivalente']; x7 = {}
    for ano in ('2014', '2018', '2022'):
        g = c['anos'][ano]['mesmas_divisas_de_2026']
        x7[ano] = {n_: [e26['J'][n_] - g['J'][n_], math.hypot(e26['ep'][n_], g['ep'][n_]), math.hypot(e26['ep_por_divisa'][n_], g['ep_por_divisa'][n_])] for n_ in ('lula_res', 'dbn', 'dcomp')}
    x['X7_2026_menos_outros_anos_nas_mesmas_divisas'] = x7
    diga('(X7)', json.dumps(x7))

    # X8: para onde foi o branco e nulo que falta no lado de um cargo só (ganho residual de cada candidato)
    iL, iR, iB = TODOS.index('dbn_res'), TODOS.index('dcomp_res'), TODOS.index('dbn')
    def partilha(T_, V_, val_, lado_a, lado_b, modelo='M0'):
        Vx = V_.copy(); Vx[:, 0] = V_[:, DESF.index('dL_comp')]; Vx[:, 1] = V_[:, DESF.index('dR_comp')]
        d, _ = composto(T_, Vx, geo, val_ & f, lado_a, lado_b, modelo=modelo)
        if d is None: return {'pares': 0}
        dif = np.column_stack([d['dif'][:, iL], d['dif'][:, iR], d['dif'][:, iL] - d['dif'][:, iR], d['dif'][:, iL] + d['dif'][:, iR]])
        J, e, G = estat(dif, d['w'], geo.grupo[d['pa']], reps, rng)
        par_uf = np.char.add(np.char.add(geo.uf[d['pa']], '-'), geo.uf[d['pb']])
        _, ed, _ = estat(dif, d['w'], par_uf, reps, rng)
        fr = boot_razao(dif[:, 0], dif[:, 3], d['w'], geo.grupo[d['pa']], reps, rng)
        nomes = ['ganho_residual_PT', 'ganho_residual_adversario', 'PT_menos_adversario', 'soma_igual_a_menos_bn_residual']
        return {'pares': int(d['pares']), **{n_: [float(J[i]), float(e[i]), float(ed[i])] for i, n_ in enumerate(nomes)}, 'fracao_para_o_PT_ic95': fr}
    x8 = {'2026_M0': partilha(T, V, val, G6, sem_de(2026)), '2026_M2': partilha(T, V, val, G6, sem_de(2026), 'M2')}
    k, loc, M, _ = S[2026]; g21 = ~np.isin(ufs_de(k), G6 + ['ZZ'])
    M2, tot = plantio_secoes(M, g21, 0.35, np.random.default_rng(SEMENTE))
    T2, _ = agregar(k, M2, geo, cand26); V2 = desfechos(T2)
    x8['2026_M0_com_plantio_35'] = partilha(T2, V2, validos(T2), G6, sem_de(2026)); x8['2026_M0_com_plantio_35']['votos_plantados'] = tot
    for ano in (2014, 2018, 2022):
        T_, V_, val_ = LOC[ano]
        x8[f'{ano}_E'] = partilha(T_, V_, val_, GOV[ano], sem_de(ano))
        x8[f'{ano}_G'] = partilha(T_, V_, val_, G6, sem_de(2026))
    x8['nota'] = ('listas = [salto, ep por municípios do lado a, ep com a divisa como unidade], em pontos do comparecimento; lado de um cargo só menos lado de dois cargos. '
                  'Conversão de branco e nulo em voto do PT prevê ganho residual do adversário igual a zero.')
    x['X8_partilha_do_bn_que_falta'] = x8
    for n_, v in x8.items():
        if isinstance(v, dict) and v.get('pares'):
            diga(f"(X8) {n_}: pares {v['pares']} PT {v['ganho_residual_PT'][0]:+.3f} ({v['ganho_residual_PT'][1]:.3f}) adversário {v['ganho_residual_adversario'][0]:+.3f} ({v['ganho_residual_adversario'][1]:.3f}) "
                 f"fração PT {v['fracao_para_o_PT_ic95'][0]:.2f} [{v['fracao_para_o_PT_ic95'][1]:.2f}; {v['fracao_para_o_PT_ic95'][2]:.2f}]")
    # X10: régua das divisas onde nada deveria saltar (mesmo grupo), aplicada à média das divisas mistas de 2026
    d26, _ = composto(T, V, geo, val & f, G6, sem_de(2026))
    par_uf = np.char.add(np.char.add(geo.uf[d26['pa']], '-'), geo.uf[d26['pb']])
    wd = np.array([d26['w'][par_uf == pu].sum() for pu in sorted(set(par_uf.tolist()))])
    conc = float(np.sqrt((wd ** 2).sum()) / wd.sum())
    x10 = {'divisas_mistas': int(len(wd)), 'raiz_da_soma_dos_pesos_ao_quadrado': conc, 'divisas_efetivas': float(1 / conc ** 2)}
    for ano in ANOS:
        ng = res['c']['divisas_do_mesmo_grupo'].get(str(ano))
        if not ng: continue
        x10[str(ano)] = {'n_divisas_do_mesmo_grupo': ng['n_divisas'], 'dp_por_divisa_lula': ng['lula_res_dp'], 'dp_por_divisa_bn': ng['dbn_dp']}
    ng = res['c']['divisas_do_mesmo_grupo']['2026']
    x10['dp_da_media_lula'] = ng['lula_res_dp'] * conc; x10['dp_da_media_bn'] = ng['dbn_dp'] * conc
    x10['salto_lula_em_dp'] = jl / x10['dp_da_media_lula']; x10['salto_bn_em_dp'] = jb / x10['dp_da_media_bn']
    mistas = {dv: v for dv, v in res['c']['todas_as_divisas']['2026'].items() if 'J' in v and ((dv.split('-')[0] in G6) != (dv.split('-')[1] in G6))}
    x10['divisas_mistas_com_50_pares'] = {dv: {'pares': v['pares'], 'bn_lado_de_um_cargo_menos_dois': (v['J']['dbn'] if dv.split('-')[0] in G6 else -v['J']['dbn']),
                                              'lula_lado_de_um_cargo_menos_dois': (v['J']['lula_res'] if dv.split('-')[0] in G6 else -v['J']['lula_res'])} for dv, v in mistas.items()}
    x10['mistas_com_bn_menor_no_lado_de_um_cargo'] = int(sum(1 for v in x10['divisas_mistas_com_50_pares'].values() if v['bn_lado_de_um_cargo_menos_dois'] < 0))
    x10['mistas_com_lula_maior_no_lado_de_um_cargo'] = int(sum(1 for v in x10['divisas_mistas_com_50_pares'].values() if v['lula_lado_de_um_cargo_menos_dois'] > 0))
    x10['nota'] = ('dp por divisa = raiz da média dos quadrados do salto nas divisas entre UFs do mesmo grupo em 2026 (inclui ruído de amostra e efeito de estado); '
                   'dp da média = dp por divisa vezes a concentração dos pesos das divisas mistas')
    nomes_pu = sorted(set(par_uf.tolist())); il = TODOS.index('lula_res')
    x10['contribuicao_por_divisa_lula'] = {pu: {'peso': float(d26['w'][par_uf == pu].sum() / d26['w'].sum()),
                                                'J': float((d26['w'][par_uf == pu] * d26['dif'][par_uf == pu, il]).sum() / d26['w'][par_uf == pu].sum()),
                                                'contribuicao': float((d26['w'][par_uf == pu] * d26['dif'][par_uf == pu, il]).sum() / d26['w'].sum())} for pu in nomes_pu}
    x['X10_regua_das_divisas_do_mesmo_grupo'] = x10
    # X11: dose entre divisas: onde o branco e nulo salta mais para baixo, a fatia do PT salta mais para cima?
    x11 = {}
    for ano in ANOS:
        td_ = {dv: v for dv, v in res['c']['todas_as_divisas'][str(ano)].items() if 'J' in v}
        com = set(GOV[ano]); r11 = {}
        for nome, sel in (('todas', lambda a_, b_: True), ('mesmo_grupo', lambda a_, b_: (a_ in com) == (b_ in com)), ('mistas', lambda a_, b_: (a_ in com) != (b_ in com))):
            dvs = [dv for dv in td_ if sel(*dv.split('-'))]
            if len(dvs) < 4: continue
            xb = np.array([td_[dv]['J']['dbn'] for dv in dvs]); yl = np.array([td_[dv]['J']['lula_res'] for dv in dvs]); wp = np.array([td_[dv]['pares'] for dv in dvs], float)
            # pela origem: o sinal de cada divisa é arbitrário (ordem alfabética das UFs)
            inc = float((wp * xb * yl).sum() / (wp * xb * xb).sum()); e_ = yl - inc * xb
            ep = float(np.sqrt(((wp * xb * e_) ** 2).sum()) / (wp * xb * xb).sum() * math.sqrt(len(dvs) / (len(dvs) - 1)))
            r11[nome] = {'n': len(dvs), 'inclinacao': inc, 'ep': ep, 'correlacao_pela_origem': float((wp * xb * yl).sum() / math.sqrt((wp * xb * xb).sum() * (wp * yl * yl).sum()))}
        x11[str(ano)] = r11
    x11['nota'] = ('regressão pela origem, ponderada pelos pares, do salto do resíduo da fatia do PT sobre o salto do branco e nulo entre divisas de UF (50 pares ou mais); '
                   'ep robusto com a divisa como unidade. Conversão de branco e nulo em voto do PT prevê inclinação negativa.')
    x['X11_dose_entre_divisas'] = x11
    diga('(X11)', json.dumps(x11, ensure_ascii=False))
    diga('(X10)', json.dumps(x10, ensure_ascii=False))
    k, loc, M, _ = S[2026]; U = somas_uf(k, M)
    x['nominais_2t_por_uf_2026'] = {u: U[u]['nom2'] for u in UFS27}
    return x


def br(v, c=3, sinal=True):
    """Número com vírgula decimal."""
    if v is None or (isinstance(v, float) and (math.isnan(v) or math.isinf(v))):
        return 'n/d'
    return (f'{v:+.{c}f}' if sinal else f'{v:.{c}f}').replace('.', ',')


def mil(v):
    return f'{int(round(v)):,}'.replace(',', '.')


def mi(v, c=2):
    m = v / 1e6
    return f'{m:.{c}f}'.replace('.', ',') + (' milhão' if abs(m) < 2 else ' milhões')


def vereditos(res):
    """Aplica os critérios do registro e as regras do docstring aos números já calculados."""
    a, b, c, d, t = res['a'], res['b'], res['c'], res['d'], res['t']
    v = {}
    c26 = a['anos']['2026']['base']['coef']['branco_nulo_1t']; e26 = a['anos']['2026']['base']['ep']['branco_nulo_1t']
    sec7 = 'SINAL' if (c26 > 0.04 and (c26 - 0.04) / e26 > 3) else ('SEM SINAL' if -0.07 <= c26 <= 0.04 else 'INCONCLUSIVO')
    cal = a['calibracao_2026_nacional']['por_milhoes']['1.82']
    va = a['criterio']['veredito']
    v['a'] = {'criterio_do_adendo_27_item_a': va,
              'veredito_pela_letra': 'SINAL' if va.startswith('2026 DESTOA') else ('SEM SINAL' if va.startswith('REGIME') else 'INCONCLUSIVO'),
              'leitura': 'pela letra do item (a), 2026 destoa de 2014 e vira indício a cruzar com (c); o item (c) saiu INCONCLUSIVO',
              'criterio_da_secao_7_e_adendo_1': sec7,
              'separacao_6_e_21_pesa_a_favor': a['separacao']['pesa_a_favor'],
              'poder_de_medida': bool(cal['desloc'] / cal['ep'] > 4), 'desloc_de_1_82_milhao_em_ep': cal['desloc'] / cal['ep'],
              'plantio_35_nas_21_desloca_a_diferenca_em_ep': a['plantio_21_ufs']['35']['desloc_em_ep']}
    p35 = b['plantio_21_ufs']['35']; epb = b['anos']['2026']['ep_boot_agregada']
    pm = bool(p35['desloc'] / p35['esperado'] >= 0.8 and abs(p35['desloc']) > 4 * epb)
    letra_b = 'SEM SINAL' if b['criterio']['dentro_de_0_3'] else 'INCONCLUSIVO'
    v['b'] = {'veredito_pela_letra': letra_b, 'poder_de_medida_G4': pm, 'desloc_do_plantio_35_em_ep': abs(p35['desloc']) / epb,
              'desloc_sobre_esperado': p35['desloc'] / p35['esperado'], 'plantio_35_cai_na_faixa_sem_sinal': bool(not p35['sai_da_zona_sem_sinal']),
              'veredito': 'SEM PODER' if (not pm or not p35['sai_da_zona_sem_sinal']) else letra_b}
    cr = c['criterio']; pc = c['plantio_21_ufs']['35']; pc2 = c['plantio_21_ufs']['53.8']
    r26 = c['anos']['2026']['equivalente']
    letra_c = 'SINAL' if cr['sinal'] else ('SEM SINAL' if (cr['sem_sinal_pelo_salto_de_lula'] or b['criterio']['dentro_de_0_3']) else 'INCONCLUSIVO')
    v['c'] = {'veredito_pela_letra': letra_c, 'poder': 'LIMITADO',
              'condicoes': {'bn_1_ponto_abaixo_a_4_ep': cr['cond_bn'], 'lula_0_5_acima_a_3_ep': cr['cond_lula'], 'outros_anos_abaixo_de_0_25': cr['cond_outros_anos_pela_letra'],
                            'sem_sinal_pelo_salto_de_lula': cr['sem_sinal_pelo_salto_de_lula'], 'sem_sinal_pela_did': b['criterio']['dentro_de_0_3']},
              'sinal_inalcancavel_pela_terceira_condicao': bool(not cr['cond_outros_anos_pela_letra']),
              'plantio_35': {'condicoes_de_2026_disparam_por_cima_do_observado': pc['sinal_dispara'], 'poder_de_medida_G4': pc['poder_de_medida'],
                             'bn_desloc_sobre_esperado': pc['desloc_dbn'] / pc['esperado_dbn'], 'bn_desloc_em_ep': abs(pc['desloc_dbn']) / r26['ep']['dbn'],
                             'lula_desloc_sobre_esperado': pc['desloc_lula'] / pc['esperado_lula_bruto'], 'lula_desloc_em_ep': pc['desloc_lula'] / r26['ep']['lula_res'],
                             'dispararia_partindo_de_salto_zero': bool(pc['desloc_lula'] >= 0.5 and pc['desloc_lula'] > 3 * r26['ep']['lula_res'])},
              'plantio_53_8': {'lula_desloc_sobre_esperado': pc2['desloc_lula'] / pc2['esperado_lula_bruto'], 'lula_desloc_em_ep': pc2['desloc_lula'] / r26['ep']['lula_res'],
                               'dispararia_partindo_de_salto_zero': bool(pc2['desloc_lula'] >= 0.5 and pc2['desloc_lula'] > 3 * r26['ep']['lula_res'])}}
    b1 = d['b1']
    v['d46_b1'] = {'veredito_pela_letra': b1['veredito'], 'poder_pleno': b1['poder_pleno'], 'poder_de_medida': b1['poder_de_medida']}
    v['d46_b2'] = {'veredito_pela_letra': 'SEM CRITÉRIO NO DESENHO (descritivo)'}
    v['t34'] = {'veredito_sem_filtro': t['sem_filtro']['criterio']['veredito'], 'veredito_com_filtro': t['com_filtro']['criterio']['veredito'],
                'divisas_que_passam_com_bonferroni': t['todas_as_divisas']['passam'], 'divisas_que_passam_sem_bonferroni': t['todas_as_divisas']['passam_sem_bonferroni']}
    return v


def escrever(res, GOV, dt):
    import textwrap
    a, b, c, d, t, x = res['a'], res['b'], res['c'], res['d'], res['t'], res['exploratorio']
    v = vereditos(res)
    A = a['anos']; B = b['anos']; C = c['anos']; r26 = C['2026']['equivalente']; cr = c['criterio']
    x5, x8, x9, x10 = x['X5_votos_pela_calibracao_do_plantio'], x['X8_partilha_do_bn_que_falta'], x['X9_conversao_que_viraria_so_nas_21'], x['X10_regua_das_divisas_do_mesmo_grupo']
    c26 = A['2026']['base']['coef']['branco_nulo_1t']; e26 = A['2026']['base']['ep']['branco_nulo_1t']
    tv = a['traducao_votos']; calp = a['calibracao_2026_nacional']
    tvb = b['traducao_votos']; tvc = c['traducao_votos']
    jl, el = cr['salto_lula_2026'][:2]; jb, eb = cr['salto_bn_2026'][:2]
    nneg = sum(1 for r_ in r26['por_divisa'].values() if r_['J']['dbn'] < 0); ndiv = len(r26['por_divisa'])
    x11 = x['X11_dose_entre_divisas']
    resumo = {
        'a_coef_2026': [c26, e26, A['2026']['base']['n'], A['2026']['base']['grupos']],
        'a_coef_por_ano': {an: [A[an]['base']['coef']['branco_nulo_1t'], A[an]['base']['ep']['branco_nulo_1t'], A[an]['base']['n']] for an in A},
        'a_2026_g21': A['2026']['sem_gov_2t']['coef']['branco_nulo_1t'], 'a_2026_g6': A['2026']['com_gov_2t']['coef']['branco_nulo_1t'],
        'a_2026_g21_menos_g6': A['2026']['dif_um_cargo_menos_dois'],
        'a_votos_adendo1_milhoes': {k_: tv[k_]['adendo1_milhoes'] for k_ in tv}, 'a_votos_regua_interna_milhoes': {k_: tv[k_]['regua_interna_2026_milhoes'] for k_ in tv},
        'b_did_por_ano': {an: [B[an]['did_agregada'], B[an]['ep_boot_agregada']] for an in B}, 'b_did_2026_em_votos': tvb['did_2026_em_votos'],
        'c_salto_bn_2026': cr['salto_bn_2026'], 'c_salto_lula_2026': cr['salto_lula_2026'], 'c_salto_lula_outros_anos': cr['salto_lula_equivalentes'],
        'c_salto_bn_em_votos': [tvc['salto_bn_em_votos'], x5['salto_bn_em_votos']], 'c_salto_lula_em_votos': [tvc['salto_lula_em_votos'], x5['salto_lula_em_votos']],
        'd46_b1_mediana_6': d['b1']['seis_mediana'], 'd46_b1_placebo_p10_p90': [d['b1']['placebo_p10'], d['b1']['placebo_p90']],
        't34_J_2026_sem_e_com_filtro': [t['sem_filtro']['criterio']['J_2026'], t['com_filtro']['criterio']['J_2026']],
        't34_sp_mg_sem_e_com_filtro': [t['sem_filtro']['2026']['SP-MG'].get('J'), t['com_filtro']['2026']['SP-MG'].get('J')], 'margem': MARGEM}
    desvios = [
        'G4 e item (c): com o plantio de 35% as condições numéricas de 2026 disparam por cima do dado observado, mas o deslocamento de Lula fica em 76% do esperado e 2,7 ep; o poder do item (c) fica como LIMITADO (decisão da primeira execução, depois de ver o resultado).',
        'G4 e item (b): a primeira execução não tinha aplicado a regra de poder ao item (b). Aplicada na retomada: 3,9 ep (limite 4) e a DiD plantada cai dentro da faixa "sem sinal" do registro. Veredito SEM PODER; pela letra do critério seria INCONCLUSIVO.',
        'Item (c): a terceira condição do SINAL falha por 2018 e 2014 qualquer que seja o dado de 2026; o critério, como escrito, não tinha como dar SINAL.',
        'Conferência do T34 sem filtro: 2 das 9 divisas diferem do publicado na quarta casa (SC-RS e MG-RJ em 2026), por empate entre locais de coordenadas idênticas na busca do vizinho mais próximo.',
        'Retomada depois do reinício do container: as funções das partes registradas não mudaram e os números delas saíram idênticos aos dos parciais da primeira execução (conferido campo a campo); exploratorio() e escrever() foram escritas na retomada.',
        'O registro pede a variação do comparecimento como terceiro desfecho do item (c); ela foi medida (salto de %s, ep %s) e não entra no critério.' % (br(r26['J']['dcomp']), br(r26['ep']['dcomp'], sinal=False)),
        'Exploratório (X1 a X11): tudo escolhido depois de ver os resultados das partes registradas; não muda veredito.']
    testes = {'com_criterio_registrado': 5, 'lista': ['(a) regressão', '(b) diferença em diferenças', '(c) divisas', 'D4-6(b1)', 'T34 corrigido'],
              'comparacoes_dentro_do_T34_com_bonferroni': t['todas_as_divisas']['n_divisas_com_50_pares'],
              'sinais_que_o_acaso_daria': 'menos de 0,05 nos quatro critérios com limiar em erros-padrão (2,5 a 4 ep); o critério do item (a) compara dois coeficientes sem limiar de erro e não tem taxa de acaso calculável',
              'sinais_pela_letra': [k_ for k_, vv in v.items() if vv.get('veredito_pela_letra') == 'SINAL'],
              'conferente_independente': 'ainda não refeito por outro agente'}
    saida = {'teste': 'R27 A1 (Adendo 27, Onda A): branco e nulo',
             'registro': {'arquivo': 'PRE-REGISTRO-2026-10-26.md, Adendo 27', 'commit': '2748895 (10/11/2026 00:16:42 UTC)',
                          'criterios': ['registro/adendo27/equipe_vermelha_relatorio.json, fragilidade "Canal do branco e nulo (forma A)", retestes a, b, c, d',
                                        'registro/adendo27/desenho_D4_proposta.json, D4-6, parte (b)', 'T34: Adendo 15, com a correção de coordenadas pedida no Adendo 27'],
                          'decisoes_antes_de_rodar': 'docstring de scripts/analisar_R27_A1.py (cópia do momento em /home/user/trabalho-eleicao/adendo27/R27_A1/docstring_antes_de_rodar.py)'},
             'avisos': ['Os retestes da equipe vermelha foram escritos por quem já conhecia os resultados antigos; o D4-6 é desenho cego.',
                        '2014, 2018 e 2022 não são régua limpa: todo número de outro ano vem com o valor bruto de 2026 ao lado.',
                        'Um SINAL só conta como indício depois de conferente independente, calibração e espelho. Este teste ainda não foi refeito por conferente.',
                        'Todos os dados são totais por seção (bweb): um voto em branco convertido dentro da urna e um eleitor que de fato votou em Lula dão o mesmo boletim. O que se testa aqui é o contraste entre lugares.'],
             'ufs_com_2t_de_governador': {str(k_): v_ for k_, v_ in GOV.items()},
             'fonte_das_ufs': '2018, 2022 e 2026: bloco 2g das bases em dados/. 2014: zips do bweb do 2º turno de 2014 do TSE (UFs em que aparece o cargo GOVERNADOR), em /home/user/trabalho-eleicao/adendo23/F21_2014',
             'vereditos': v, 'resumo_numeros': resumo, 'contagem_de_testes': testes, 'desvios': desvios,
             'a_regressao': a, 'b_diferenca_em_diferencas': b, 'd46_b': d, 'c_divisas': c, 't34_corrigido': t, 'exploratorio': x,
             'tempo_s': round(dt), 'semente': SEMENTE}
    json.dump(limpar(saida), open(_os.path.join(RESULT, 'R27_A1_branco_nulo.json'), 'w'), ensure_ascii=False, indent=1)

    # ------------------------------------------------------------ texto
    L = []
    def par(s, ind=0, prim=None):
        pre = ' ' * ind if prim is None else prim
        L.extend(textwrap.wrap(s, width=118, initial_indent=pre, subsequent_indent=' ' * max(ind, len(pre))) or [''])
    def tit(s):
        L.append(''); L.append(s)
    ce = lambda r_: f"{br(r_['coef']['branco_nulo_1t'], 4)} ({br(r_['ep']['branco_nulo_1t'], 4, False)})"
    je = lambda r_, n_, cc=3: f"{br(r_['J'][n_], cc)} ({br(r_['ep'][n_], cc, False)})"
    L.append('R27 A1 (ADENDO 27, ONDA A): BRANCO E NULO (RESULTADOS)')
    L.append('')
    par('Registro: PRE-REGISTRO-2026-10-26.md, Adendo 27, commit 2748895 (10/11/2026 00:16:42 UTC), antes de rodar. Critérios: fragilidade "Canal do branco e nulo '
        '(forma A)" de registro/adendo27/equipe_vermelha_relatorio.json (retestes a, b, c e a calibração d) e parte (b) do D4-6 de desenho_D4_proposta.json. Decisões que o '
        'registro não fixa: docstring de scripts/analisar_R27_A1.py, escrito antes de qualquer conta com votos. Números completos em resultados/R27_A1_branco_nulo.json.')
    par('Hipótese: brancos e nulos da tela de presidente registrados como voto em Lula, talvez só onde há um cargo na cédula do 2º turno (21 UFs), poupando as 6 UFs em que '
        'a mesma urna dá referência (AC, AM, DF, ES, RN, TO).')
    par('Avisos. (1) Os retestes da equipe vermelha foram escritos por quem já conhecia os resultados antigos: o critério é novo, a escolha do que retestar é posterior ao dado. '
        'O D4-6 é desenho cego. (2) 2014, 2018 e 2022 não são régua limpa (o Léo suspeita deles também): todo número de outro ano vem com o valor bruto de 2026 ao lado. '
        '(3) Um SINAL só conta como indício depois de conferente independente, calibração e espelho; este teste ainda NÃO foi refeito por conferente. (4) Os dados são totais por '
        'seção: branco convertido dentro da urna e eleitor que votou em Lula dão o mesmo boletim; o que se mede é o contraste entre lugares. (5) O container reiniciou no meio da '
        'primeira execução; a retomada rodou tudo de novo e as partes registradas saíram idênticas aos parciais gravados antes.')
    tit('VEREDITOS PELA LETRA')
    par(f"SINAL pela letra do item (a) do Adendo 27 (2014 deu {br(A['2014']['base']['coef']['branco_nulo_1t'], 4)}, abaixo de -0,04: \"2026 destoa e vira indício a cruzar com (c)\"), "
        f"e o cruzamento com (c) saiu INCONCLUSIVO. Pelo critério original da seção 7 e do Adendo 1 o mesmo número é {v['a']['criterio_da_secao_7_e_adendo_1']} "
        f"({br(c26, 4)}, abaixo de +0,04). A separação de 2026 em 6 e 21 UFs não pesa a favor da variante \"só onde há um cargo\".", 5, '(a)  ')
    par(f"SEM PODER. Pela letra do critério seria {v['b']['veredito_pela_letra']} (a DiD de 2026 fica a {br(b['criterio']['distancia_agregada'], 2)} ponto da média dos outros anos, "
        f"fora da faixa de 0,3), mas a calibração mostra que a comparação com os outros anos não enxerga a conversão de 35%: com ela plantada a DiD cai a "
        f"{br(abs(b['plantio_21_ufs']['35']['distancia_da_media_de_referencia']), 2, False)} ponto da média de referência, dentro da faixa que o registro chama de sem sinal.", 5, '(b)  ')
    par(f"{v['c']['veredito_pela_letra']}, com poder LIMITADO. O branco e nulo salta {br(jb, 2)} ponto na divisa ({br(abs(jb / eb), 1, False)} ep; condição cumprida). A fatia de Lula "
        f"salta {br(jl, 3)} (ep {br(el, 3, False)}; {br(jl / el, 2, False)} ep), abaixo dos 0,5 ponto e dos 3 ep exigidos, e acima do 0,25 que daria SEM SINAL. A terceira condição "
        f"falha: nas divisas equivalentes o salto foi {br(cr['salto_lula_equivalentes']['2014'][0], 2)} em 2014, {br(cr['salto_lula_equivalentes']['2018'][0], 2)} em 2018 e "
        f"{br(cr['salto_lula_equivalentes']['2022'][0], 2)} em 2022. Com 2018 em +1,14, o critério, como escrito, não tinha como dar SINAL.", 5, '(c)  ')
    par(f"D4-6(b1): {v['d46_b1']['veredito_pela_letra']}, com poder pleno. Nas 6 UFs a razão entre o branco e nulo de presidente e o de governador subiu entre os turnos "
        f"(mediana {br(d['b1']['seis_mediana'], 3)}), dentro da faixa das 26 UFs placebo de 2018 e 2022 (percentil 10 {br(d['b1']['placebo_p10'], 3)}, percentil 90 "
        f"{br(d['b1']['placebo_p90'], 3)}). D4-6(b2): descritivo, sem critério no desenho.", 5, '     ')
    par(f"T34 corrigido: {v['t34']['veredito_com_filtro']} (não muda). O salto SP-MG de -0,034 some com o filtro de coordenadas.", 5, '     ')
    par(f"Contagem: {testes['com_criterio_registrado']} testes com critério registrado; {len(testes['sinais_pela_letra'])} sinal pela letra ({', '.join(testes['sinais_pela_letra'])}), em critério que compara "
        f"dois coeficientes sem limiar de erro. O acaso daria menos de 0,05 sinal nos outros quatro. Nenhum SINAL que passe por calibração, espelho e conferente.", 5, '     ')

    tit('(a) REGRESSÃO DO BRANCO E NULO POR SEÇÃO (scripts/analisar_bn_secao.py, sem mudança)')
    par('Coeficiente do branco e nulo do 1º turno na virada da fatia do 13 entre os turnos, dentro do mesmo local de votação. Erro-padrão entre parênteses.')
    L.append('  ano    todas as seções        n seções   locais   B+N 1ºt   B+N 2ºt   UFs sem gov 2ºt       UFs com gov 2ºt       sem menos com')
    for an in ('2014', '2018', '2022', '2026'):
        r_ = A[an]; dd = r_['dif_um_cargo_menos_dois']
        L.append(f"  {an}   {ce(r_['base']):<22} {mil(r_['base']['n']):>8}  {mil(r_['base']['grupos']):>7}   {br(r_['bn_1t_pct'], 2, False):>6}%   {br(r_['bn_2t_pct'], 2, False):>6}%   "
                 f"{ce(r_['sem_gov_2t']):<21} {ce(r_['com_gov_2t']):<21} {br(dd[0], 4)} ({br(dd[1], 4, False)})")
    par(f"Valor de resultados/bn_secao_2026.json que nunca tinha sido relatado: {br(c26, 4)} (ep {br(e26, 4, False)}), {mil(A['2026']['base']['n'])} seções em "
        f"{mil(A['2026']['base']['grupos'])} locais. Este script reproduz o número até a última casa.")
    par(f"Em 2026 separado: 21 UFs {ce(A['2026']['sem_gov_2t'])}, n {mil(A['2026']['sem_gov_2t']['n'])}; 6 UFs {ce(A['2026']['com_gov_2t'])}, n {mil(A['2026']['com_gov_2t']['n'])}; "
        f"diferença {br(A['2026']['dif_um_cargo_menos_dois'][0], 4)} (ep {br(A['2026']['dif_um_cargo_menos_dois'][1], 4, False)}). O coeficiente é MAIOR nas 6 UFs que a tese diz poupadas."
        + (f" Exterior: {ce(A['2026']['exterior'])}." if 'coef' in A['2026'].get('exterior', {}) else ''))
    par(f"Em votos, pela calibração do Adendo 1 (+0,061 para 1,82 milhão; +0,142 para 4,43 milhões): contra zero, {br(tv['zero']['adendo1_milhoes'], 2, False)} milhão; contra 2018 "
        f"(deslocamento {br(tv['2018']['desloc_2026'], 3)}), {br(tv['2018']['adendo1_milhoes'], 2, False)} milhões; contra 2022 ({br(tv['2022']['desloc_2026'], 3)}), "
        f"{br(tv['2022']['adendo1_milhoes'], 2, False)} milhões; contra 2014 ({br(tv['2014']['desloc_2026'], 3)}), {br(tv['2014']['adendo1_milhoes'], 1, False)} milhões, o que é impossível: "
        f"todo o branco e nulo do 2º turno soma {br(calp['bn_2t_nas_secoes'] / 1e6, 2, False)} milhões. A distância entre anos não mede conversão.")
    par(f"Calibração dentro de 2026 (conversão somada por cima do dado): 1,00 milhão desloca {br(calp['por_milhoes']['1.00']['desloc'], 4)}; 1,82 milhão, {br(calp['por_milhoes']['1.82']['desloc'], 4)} "
        f"({br(v['a']['desloc_de_1_82_milhao_em_ep'], 0, False)} ep); 4,43 milhões, {br(calp['por_milhoes']['4.43']['desloc'], 4)}. Bate com o Adendo 1. Plantio de 35% só nas 21 UFs "
        f"({mil(a['plantio_21_ufs']['35']['votos_plantados'])} votos): a diferença 21 menos 6 anda {br(a['plantio_21_ufs']['35']['desloc_da_dif'], 4)} "
        f"({br(a['plantio_21_ufs']['35']['desloc_em_ep'], 1, False)} ep). O teste enxerga o plantio. O que ele não tem é ponto zero: a diferença análoga foi "
        f"{br(A['2014']['dif_um_cargo_menos_dois'][0], 3)} em 2014, {br(A['2018']['dif_um_cargo_menos_dois'][0], 3)} em 2018 e {br(A['2022']['dif_um_cargo_menos_dois'][0], 3)} em 2022.")
    es = lambda an, lado: f"{br(A[an]['espelho'][lado]['todas'][0], 3)}"
    par(f"Espelho (a mesma regressão com o ganho de cada candidato em pontos do comparecimento): em 2026, cada ponto de branco e nulo do 1º turno vale {es('2026', 'L')} para Lula e "
        f"{es('2026', 'R')} para Flávio. Em 2022, {es('2022', 'L')} e {es('2022', 'R')}; em 2018, {es('2018', 'L')} e {es('2018', 'R')}; em 2014, {es('2014', 'L')} e {es('2014', 'R')}. "
        f"O adversário recebe em 2026 o mesmo que nos outros anos; o que sobe é a parte do PT.")

    tit('(b) DIFERENÇA EM DIFERENÇAS POR UF')
    par('Variação do branco e nulo de presidente entre os turnos, em pontos do comparecimento: UFs sem 2º turno de governador menos UFs com. Negativo = caiu mais onde só havia presidente.')
    L.append('  ano    UFs com gov   sem gov    com gov    DiD agregada (ep)    média simples (ep)   p da permutação   em % dos aptos, sem menos com: PT, adversário, B+N, abstenção')
    for an in ('2014', '2018', '2022', '2026'):
        r_ = B[an]; k_ = r_['contabilidade_pct_aptos']['dif_sem_menos_com']; pp = x['X2_permutacao_da_did_por_ano'][an]['p_tao_negativa_media_simples']
        if an == '2026': pp = b['permutacao_2026']['p_media_simples_tao_negativa']
        L.append(f"  {an}   {len(r_['ufs_com_gov_2t']):>6}       {br(r_['var_sem'], 2):>7}    {br(r_['var_com'], 2):>7}    {br(r_['did_agregada'], 3)} ({br(r_['ep_boot_agregada'], 3, False)})      "
                 f"{br(r_['did_media_simples'], 3)} ({br(r_['ep_welch'], 3, False)})      {(('%.6f' % pp).replace('.', ',') if pp > 0 else '<0,000005'):>9}       {br(k_['dL'], 2)}  {br(k_['dR'], 2)}  {br(k_['dBN'], 2)}  {br(k_['dAbst'], 2)}")
    par('p da permutação: fração dos sorteios de UFs com diferença de média simples tão negativa quanto a observada (2026: todas as 296.010 escolhas; outros anos: 200 mil sorteios, exploratório X2).')
    par('UFs com 2º turno de governador. ' + ' '.join(f"{an}: {', '.join(GOV[int(an)] if int(an) in GOV else GOV[an])}." for an in ('2014', '2018', '2022', '2026')))
    par('Fonte: 2018, 2022 e 2026 pelo bloco de governador do 2º turno das bases em dados/; a base de 2014 não tem governador, e a lista saiu dos zips do bweb do 2º turno de 2014 do TSE '
        '(UFs em que aparece o cargo GOVERNADOR), os mesmos do F21.')
    par(f"Valor bruto de 2026: {br(B['2026']['did_agregada'], 3)} ponto (ep {br(B['2026']['ep_boot_agregada'], 3, False)}): {br(B['2026']['var_sem'], 2)} nas 21 UFs e {br(B['2026']['var_com'], 2)} nas 6. "
        f"Aplicado ao comparecimento das 21 UFs ({mil(tvb['comp_2t_21_ufs'])}) são {mil(abs(tvb['did_2026_em_votos']))} votos, {br(100 * tvb['pct_da_margem'], 0, False)}% da margem, se a diferença inteira fosse conversão. "
        f"Régua interna (todas as {mil(b['permutacao_2026']['n_escolhas'])} escolhas de 6 UFs entre 27): só {('%.4f' % (100 * b['permutacao_2026']['p_agregada_tao_negativa'])).replace('.', ',')}% "
        f"dão diferença tão negativa. As 6 UFs são mesmo diferentes das 21.")
    par(f"Outros anos: {br(B['2014']['did_agregada'], 2)} (2014), {br(B['2018']['did_agregada'], 2)} (2018), {br(B['2022']['did_agregada'], 2)} (2022), média {br(b['criterio']['media_referencia_agregada'], 2)}. "
        f"A diferença existe nos quatro anos e é significativa em todos pela permutação. 2026 fica {br(b['criterio']['distancia_agregada'], 2)} ponto ACIMA da média (queda menor que a média, maior que a de 2022).")
    p35 = b['plantio_21_ufs']['35']; p53 = b['plantio_21_ufs']['53.8']
    par(f"Calibração: plantio de 35% do branco e nulo das 21 UFs em Lula ({mil(p35['votos_plantados'])} votos) desloca a DiD em {br(p35['desloc'], 3)} (esperado {br(p35['esperado'], 3)}; "
        f"{br(v['b']['desloc_do_plantio_35_em_ep'], 1, False)} ep, abaixo dos 4 da regra G4) e leva a DiD a {br(p35['did_agregada'], 2)}, a {br(abs(p35['distancia_da_media_de_referencia']), 2, False)} "
        f"ponto da média de referência: o critério chamaria isso de sem sinal. Com 53,8% ({mil(p53['votos_plantados'])} votos) a DiD vai a {br(p53['did_agregada'], 2)} e sai da faixa. "
        f"Os anos de referência variam de {br(B['2022']['did_agregada'], 2)} a {br(B['2018']['did_agregada'], 2)}; o efeito plantado cabe dentro dessa variação.")
    kb = B['2026']['contabilidade_pct_aptos']
    par(f"Espelho (em % dos aptos, 2026): nas 21 UFs Lula ganhou {br(kb['sem_gov_2t']['dL'], 2)} e Flávio {br(kb['sem_gov_2t']['dR'], 2)}; nas 6, {br(kb['com_gov_2t']['dL'], 2)} e {br(kb['com_gov_2t']['dR'], 2)}. "
        f"Diferença: Lula {br(kb['dif_sem_menos_com']['dL'], 2)}, Flávio {br(kb['dif_sem_menos_com']['dR'], 2)}, branco e nulo {br(kb['dif_sem_menos_com']['dBN'], 2)}, abstenção {br(kb['dif_sem_menos_com']['dAbst'], 2)}. "
        f"O adversário também ganhou mais onde só havia presidente, quase tanto quanto Lula. Conversão de branco em Lula não dá voto a Flávio.")

    tit('D4-6(b): PRESIDENTE CONTRA GOVERNADOR NA MESMA URNA (6 UFs)')
    b1 = d['b1']
    par('(b1) DiD = ln(B+N de presidente / B+N de governador) no 2º turno menos o mesmo no 1º. ' + ' '.join(f"{u} {br(b1['seis_DiD'][u], 3)}." for u in G6)
        + f" Mediana {br(b1['seis_mediana'], 3)}. Placebo (todas as UFs com 2º turno de governador em 2018 e 2022, n = {b1['placebo_n']}): mínimo {br(b1['placebo_min'], 3)}, percentil 10 "
        f"{br(b1['placebo_p10'], 3)}, mediana {br(b1['placebo_mediana'], 3)}, percentil 90 {br(b1['placebo_p90'], 3)}, máximo {br(b1['placebo_max'], 3)}. As 6 de 2026 ficam todas entre os percentis 10 e 90 "
        f"({b1['seis_dentro_p10_p90']} de 6): {b1['veredito']}. O sinal exigia mediana de -0,35 ou menos. O veredito usa 2018 e 2022 como placebo. Valor bruto de 2026, sem outro ano: a razão SUBIU "
        f"nas 6 UFs (de {br(min(b1['seis_DiD'].values()), 2)} a {br(max(b1['seis_DiD'].values()), 2)}); a conversão que vira o resultado a derrubaria em 0,73, e para escondê-la a subida natural teria de ser de "
        f"{br(b1['seis_mediana'] + 0.73, 2)} ou mais, acima do máximo já visto ({br(b1['placebo_max'], 2)}).")
    pd_ = b1['poder']
    par(f"Poder: mover 26% do branco e nulo de presidente para Lula nas 6 UFs ({mil(pd_['0.26']['votos_plantados'])} votos) derruba a mediana em {br(pd_['0.26']['queda_da_mediana'], 3)} "
        f"(esperado {br(pd_['0.26']['esperado'], 3)}) e tira o resultado da faixa sem sinal; mover 52% ({mil(pd_['0.52']['votos_plantados'])} votos) derruba em {br(pd_['0.52']['queda_da_mediana'], 3)} "
        f"(esperado {br(pd_['0.52']['esperado'], 3)}) e dispara o SINAL. Poder pleno. Este teste só fala das 6 UFs.")
    x3 = x['X3_d46_b1_postos']
    par(f"Exploratório (X3): a mediana das 6 fica {br(abs(x3['dif_medianas']), 3, False)} abaixo da mediana placebo (5 das 6 abaixo; postos, p unilateral {br(x3['p_mann_whitney_menor'], 3, False)}). "
        f"Se essa diferença inteira fosse conversão, seriam {br(100 * x3['conversao_equivalente_fracao_do_bn_antes'], 0, False)}% do branco e nulo, cerca de {mil(x3['conversao_equivalente_votos'])} votos nas 6 UFs. "
        f"O que a faixa placebo deixa passar é mais: se a subida natural fosse a do percentil 90, o observado esconderia {br(100 * x3['conversao_compativel_com_o_p90_do_placebo'], 0, False)}%; se fosse a máxima já vista, "
        f"{br(100 * x3['conversao_compativel_com_o_maximo_do_placebo'], 0, False)}%. Com a mesma taxa nas 27 UFs isso seria {mi(x3['votos_no_pais_se_a_taxa_valesse_nas_27']['mediana'])}, "
        f"{mi(x3['votos_no_pais_se_a_taxa_valesse_nas_27']['p90'])} e {mi(x3['votos_no_pais_se_a_taxa_valesse_nas_27']['maximo'])}. Os 52% que virariam o resultado ficam fora de qualquer leitura.")
    L.append('  (b2) coeficientes de brancos (B1) e nulos (N1) do 1º turno nas equações de L2 e de R2 (efeito fixo de local, peso 1/aptos, erro por município; eliminados somados)')
    L.append('  ano      n          L2~B1             L2~N1             R2~B1             R2~N1             (L2-R2)~B1        (L2-R2)~N1        votos de margem associados')
    for an in ('2014', '2018', '2022', '2026'):
        e_ = d['b2'][an]['variante_d']['eq']; x6 = x['X6_b2_em_votos'][an]['todas']
        f2 = lambda eq, vx: f"{br(e_[eq]['coef'][vx], 4)} ({br(e_[eq]['ep'][vx], 4, False)})"
        L.append(f"  {an}   {mil(d['b2'][an]['variante_d']['n']):>8}   {f2('L2', 'B1')}  {f2('L2', 'N1')}  {f2('R2', 'B1')}  {f2('R2', 'N1')}  "
                 f"{br(x6['coef_B1'][0], 4)} ({br(x6['coef_B1'][1], 4, False)})  {br(x6['coef_N1'][0], 4)} ({br(x6['coef_N1'][1], 4, False)})  {mil(x6['votos_de_margem_associados'])}")
    x6 = x['X6_b2_em_votos']['2026']
    par(f"Em 2026 a assimetria a favor do PT é a maior dos quatro anos: {br(x6['todas']['coef_B1'][0], 3)} por branco e {br(x6['todas']['coef_N1'][0], 3)} por nulo do 1º turno, o que, vezes o estoque "
        f"({mil(x6['todas']['brancos_1t'])} brancos e {mil(x6['todas']['nulos_1t'])} nulos), dá {mil(x6['todas']['votos_de_margem_associados'])} votos de margem associados (exploratório, X6). "
        f"A assimetria é a mesma nas 6 UFs ({br(x6['com_gov_2t']['coef_B1'][0], 3)} e {br(x6['com_gov_2t']['coef_N1'][0], 3)}) e nas 21 ({br(x6['sem_gov_2t']['coef_B1'][0], 3)} e {br(x6['sem_gov_2t']['coef_N1'][0], 3)}): "
        f"não distingue o lado que a tese diz poupado. É associação entre seções do mesmo local; não separa conversão de eleitor que mudou de voto.")

    tit('(c) DIVISAS ENTRE AS 6 UFs E AS VIZINHAS (pares de locais a até 20 km)')
    fl = c['filtro']
    par(f"Filtro de coordenadas: {mil(fl['locais_com_coordenada'])} locais com coordenada; {fl['fora_da_caixa']} fora da caixa da UF ({', '.join(f'{u} {n_}' for u, n_ in sorted(fl['fora_da_caixa_por_uf'].items()))}); "
        f"{fl['longe_do_centroide']} a mais de 150 km do centroide do município (400 km nos estados de municípios gigantes); ficam {mil(fl['ficam'])}. Multiplicidade máxima de 20 pares por local.")
    par(f"2026: {mil(r26['pares'])} pares, {r26['locais_a']} locais do lado das 6 UFs e {r26['locais_b']} do lado das 21, {r26['grupos_lado_a']} municípios do lado a, {r26['divisas']} divisas, "
        f"{mil(r26['nominais_dos_pares'])} votos nominais. Orientação: lado de um cargo só menos lado de dois cargos, em pontos percentuais. Erro-padrão por bootstrap de municípios do lado a; "
        f"entre colchetes, com a divisa como unidade.")
    def linha(nome, r_):
        return (f"  {nome:<26} pares {mil(r_['pares']):>5}   B+N {br(r_['J']['dbn'], 3)} ({br(r_['ep']['dbn'], 3, False)}) [{br(r_['ep_por_divisa']['dbn'], 3, False)}]   "
                f"PT resíduo {br(r_['J']['lula_res'], 3)} ({br(r_['ep']['lula_res'], 3, False)}) [{br(r_['ep_por_divisa']['lula_res'], 3, False)}]   "
                f"comparecimento {br(r_['J']['dcomp'], 3)} ({br(r_['ep']['dcomp'], 3, False)})")
    L.append(linha('2026 (critério)', r26))
    for an in ('2014', '2018', '2022'):
        L.append(linha(f'{an} equivalentes (E)', C[an]['equivalente'])); L.append(linha(f'{an} mesmas seis (G)', C[an]['mesmas_divisas_de_2026']))
    par('(E) = em cada ano, UFs com 2º turno de governador naquele ano contra as sem; (G) = as mesmas seis divisas de 2026 com os votos de cada ano. Seções de outros anos ligadas ao cadastro de '
        f"2026 pela chave da seção: {mil(C['2014']['ligacao']['ligadas_ao_cadastro_2026'])} de {mil(C['2014']['ligacao']['secoes_com_dois_turnos'])} em 2014, "
        f"{mil(C['2018']['ligacao']['ligadas_ao_cadastro_2026'])} de {mil(C['2018']['ligacao']['secoes_com_dois_turnos'])} em 2018, {mil(C['2022']['ligacao']['ligadas_ao_cadastro_2026'])} de "
        f"{mil(C['2022']['ligacao']['secoes_com_dois_turnos'])} em 2022.")
    L.append('  2026 por divisa (lado das 6 primeiro):')
    for pu, r_ in r26['por_divisa'].items():
        if r_['pares'] >= 15:
            L.append(f"    {pu}: pares {r_['pares']:>4}   B+N {br(r_['J']['dbn'], 2)} ({br(r_['ep']['dbn'], 2, False)})   Lula {br(r_['J']['lula_res'], 2)} ({br(r_['ep']['lula_res'], 2, False)})   comparecimento {br(r_['J']['dcomp'], 2)}")
    sn = C['2026']['sensibilidade']
    rot = {'limite_100_300': 'limite de 100 e 300 km', 'tira_local_com_mais_de_20': 'tirando o local com mais de 20 pares', 'sem_filtro': 'sem filtro nenhum', 'sem_corte_de_multiplicidade': 'sem corte de multiplicidade'}
    par('Sensibilidade do filtro (Lula; B+N): ' + '; '.join(f"{rot.get(nome, nome)} {br(s_['lula_res'][0], 3)} ({br(s_['lula_res'][1], 3, False)}); {br(s_['dbn'][0], 3)}" for nome, s_ in sn.items() if 'dbn' in s_)
        + f". Com os eliminados separados (M2: Zema, Cury, Caiado, Renan Santos): Lula {br(sn['modelo_M2_eliminados_separados']['lula_res'][0], 3)} ({br(sn['modelo_M2_eliminados_separados']['lula_res'][1], 3, False)}).")
    par(f"Contabilidade do salto de 2026 em % dos aptos: Lula {je(r26, 'dL_apt', 2)}, Flávio {je(r26, 'dR_apt', 2)}, branco e nulo {je(r26, 'dbn_apt', 2)}, abstenção {je(r26, 'dabst_apt', 2)}; "
        f"o lado de um cargo só tinha {br(r26['J']['O1_apt'], 2)} ponto a mais de voto em eliminados no 1º turno (Caiado em GO).")
    pc = c['plantio_21_ufs']['35']; pc2 = c['plantio_21_ufs']['53.8']
    par(f"Calibração: plantio de 35% do branco e nulo das 21 UFs em Lula ({mil(pc['votos_plantados'])} votos). O salto do branco e nulo vai a {br(pc['dbn'][0], 3)} (deslocamento {br(pc['desloc_dbn'], 3)}, "
        f"esperado {br(pc['esperado_dbn'], 3)}; {br(v['c']['plantio_35']['bn_desloc_em_ep'], 1, False)} ep) e o de Lula a {br(pc['lula_res'][0], 3)} (deslocamento {br(pc['desloc_lula'], 3)}, esperado bruto "
        f"{br(pc['esperado_lula_bruto'], 3)}: {br(100 * v['c']['plantio_35']['lula_desloc_sobre_esperado'], 0, False)}% e {br(v['c']['plantio_35']['lula_desloc_em_ep'], 1, False)} ep). O teste mede o branco e nulo por inteiro e a fatia "
        f"de Lula com atenuação. Por cima do dado observado as condições de 2026 disparam; partindo de salto zero, 35% não chegaria a 0,5 ponto nem a 3 ep, e 53,8% ({mil(pc2['votos_plantados'])} votos) "
        f"daria {br(pc2['desloc_lula'], 3)} ({br(v['c']['plantio_53_8']['lula_desloc_em_ep'], 1, False)} ep), ainda abaixo de 0,5. Pela letra da regra G4 do docstring isso é falta de poder de medida "
        f"na metade de Lula para 35%; a primeira execução registrou o caso como poder LIMITADO.")
    ng = c['divisas_do_mesmo_grupo']['2026']
    par(f"Onde nada deveria saltar: {ng['n_divisas']} divisas entre UFs do mesmo grupo em 2026 (50 pares ou mais). |salto de Lula|: mediana {br(ng['lula_res_abs_mediana'], 2, False)}, percentil 90 "
        f"{br(ng['lula_res_abs_p90'], 2, False)}, máximo {br(ng['lula_res_abs_max'], 2, False)}. |salto do B+N|: mediana {br(ng['dbn_abs_mediana'], 2, False)}, percentil 90 {br(ng['dbn_abs_p90'], 2, False)}, "
        f"máximo {br(ng['dbn_abs_max'], 2, False)}. Exploratório (X10): com a dispersão dessas divisas como régua, o salto médio de Lula nas divisas mistas ({br(jl, 3)}) fica a "
        f"{br(abs(x10['salto_lula_em_dp']), 1, False)} desvio; o do branco e nulo ({br(jb, 2)}), a {br(abs(x10['salto_bn_em_dp']), 1, False)} desvios. Das 7 divisas mistas com 50 pares ou mais, "
        f"{x10['mistas_com_bn_menor_no_lado_de_um_cargo']} têm branco e nulo menor e {x10['mistas_com_lula_maior_no_lado_de_um_cargo']} têm Lula maior no lado de um cargo só.")
    par(f"Em votos. Branco e nulo: {br(jb, 2)} ponto vezes o comparecimento das 21 UFs = {mil(abs(tvc['salto_bn_em_votos']))} (intervalo de 95%: {mil(abs(tvc['salto_bn_ic95_em_votos'][1]))} a "
        f"{mil(abs(tvc['salto_bn_ic95_em_votos'][0]))}); pela calibração do plantio, {mil(x5['salto_bn_em_votos'])} ({mil(x5['salto_bn_ic95_em_votos'][0])} a {mil(x5['salto_bn_ic95_em_votos'][1])}). "
        f"Fatia de Lula: {br(jl, 3)} = {mil(tvc['salto_lula_em_votos'])} votos pela fórmula ({mil(tvc['limite_inf_95_em_votos'])} a {mil(tvc['limite_sup_95_em_votos'])}); pela calibração do plantio, "
        f"{mil(x5['salto_lula_em_votos'])} ({mil(x5['salto_lula_ic95_em_votos'][0])} a {mil(x5['salto_lula_ic95_em_votos'][1])}), {br(x5['pct_da_margem_salto_lula'], 0, False)}% da margem. "
        f"A margem é {mil(MARGEM)}.")
    par(f"Exploratório (X5, X9). Se o salto inteiro do branco e nulo fosse conversão em Lula, o salto de Lula seria {br(x5['salto_de_lula_se_o_salto_inteiro_do_bn_fosse_conversao'], 3)}; o observado é "
        f"{br(100 * x5['observado_sobre_isso'], 0, False)}% disso (a {br(abs(x5['z_observado_contra_isso']), 1, False)} ep; a {br(x5['z_observado_contra_zero'], 1, False)} ep de zero). Uma conversão que virasse o resultado só nas 21 UFs "
        f"(4,43 milhões; o branco e nulo observado ali é {mil(x9['bn_observado_2t_nas_21'])}) deixaria na divisa, por extrapolação linear, branco e nulo {br(x9['salto_bn_esperado'], 2)} e Lula "
        f"{br(x9['salto_lula_esperado'], 2)}: o observado é {br(100 * x9['observado_sobre_esperado_bn'], 0, False)}% e {br(100 * x9['observado_sobre_esperado_lula'], 0, False)}% disso "
        f"(Lula a {br(abs(x9['z_lula_observado_contra_esperado']), 1, False)} ep; {br(abs(x9['z_lula_observado_contra_esperado_ep_por_divisa']), 1, False)} ep com a divisa como unidade).")
    f8 = lambda k_: (f"PT {br(x8[k_]['ganho_residual_PT'][0], 2)} ({br(x8[k_]['ganho_residual_PT'][1], 2, False)}), adversário {br(x8[k_]['ganho_residual_adversario'][0], 2)} "
                     f"({br(x8[k_]['ganho_residual_adversario'][1], 2, False)}), fração do PT {br(100 * x8[k_]['fracao_para_o_PT_ic95'][0], 0, False)}% "
                     f"[{br(100 * x8[k_]['fracao_para_o_PT_ic95'][1], 0, False)}; {br(100 * x8[k_]['fracao_para_o_PT_ic95'][2], 0, False)}]")
    par(f"Exploratório (X8), para onde foi o branco e nulo que falta no lado de um cargo só (ganho residual de cada candidato em pontos do comparecimento, mesmos pares, mesmo modelo; os dois somam o "
        f"salto residual do branco e nulo com o sinal trocado). 2026: {f8('2026_M0')}. Com o plantio de 35%: {f8('2026_M0_com_plantio_35')}. Divisas equivalentes: 2014, {f8('2014_E')}; 2018, {f8('2018_E')}; "
        f"2022, {f8('2022_E')}. Conversão pura prevê zero para o adversário; em 2026 ele recebe {br(x8['2026_M0']['ganho_residual_adversario'][0], 2)} "
        f"({br(x8['2026_M0']['ganho_residual_adversario'][0] / x8['2026_M0']['ganho_residual_adversario'][1], 1, False)} ep).")
    x7 = x['X7_2026_menos_outros_anos_nas_mesmas_divisas']
    par('Exploratório (X7), 2026 menos cada outro ano nas mesmas seis divisas (Lula; B+N): ' + '; '.join(
        f"{an}: {br(x7[an]['lula_res'][0], 2)} ({br(x7[an]['lula_res'][1], 2, False)}); {br(x7[an]['dbn'][0], 2)} ({br(x7[an]['dbn'][1], 2, False)})" for an in ('2014', '2018', '2022')) + '.')
    x4 = x['X4_nulos_digitados_rdv']
    if 'por_uf' in x4 and 'AC' in x4['por_uf']:
        ac = x4['por_uf']['AC']; rg = x4.get('regua_AC', {})
        s4 = (f"Exploratório (X4), o que foi digitado nos nulos (RDV da amostra, {x4['secoes']} seções em {len(x4['por_uf'])} UFs; das 6 UFs só o AC, {ac['secoes_com_rdv']} seções e "
              f"{mil(ac['pres_total'])} votos). No AC, {ac['nulo_pres_com_numero_de_finalista_gov']} nulos de presidente foram digitados com o número de um dos dois finalistas de governador "
              f"({' e '.join(ac['finalistas_gov'])}): {br(ac['pct_do_comparecimento_nulo_pres_com_numero_de_gov'], 2, False)}% do comparecimento e {br(ac['pct_do_bn_pres_que_e_numero_de_gov'], 0, False)}% do branco e nulo "
              f"de presidente dali. Nas UFs sem 2º turno de governador os mesmos números aparecem em {br(rg.get('pct_do_comparecimento_nas_ufs_sem_gov_2t'), 2, False)}% do comparecimento "
              f"({mil(rg.get('votos', 0))} de {mil(rg.get('comparecimento', 0))}). Na tela de governador do AC, {ac['nulo_gov_com_13_ou_22']} nulos foram digitados 13 ou 22")
        if ac.get('nulo_gov_com_13') is not None and ac.get('fatia_13_entre_os_que_digitaram_presidente_na_tela_de_gov') is not None:
            s4 += (f" ({ac['nulo_gov_com_13']} com 13 e {ac['nulo_gov_com_22']} com 22: {br(100 * ac['fatia_13_entre_os_que_digitaram_presidente_na_tela_de_gov'], 0, False)}% de 13, contra "
                   f"{br(100 * ac['fatia_13_nos_nominais_de_presidente_das_mesmas_secoes'], 0, False)}% de Lula nos votos nominais das mesmas seções)")
        s4 += ('. Troca de tela (o número de um cargo digitado no outro) explicaria por que o nulo de presidente sobe onde há dois cargos, sem conversão. São 12 seções de uma UF: é pista, não medida. '
               'O teste D4-3 (onda D) mede isso no AC e no TO inteiros.')
        par(s4)

    tit('T34 CORRIGIDO (salto na divisa PR contra SP e MS; filtro de coordenadas)')
    for rot, nome in (('sem_filtro', 'Sem filtro (reproduz o publicado)'), ('com_filtro', 'Com filtro')):
        k_ = t[rot]['criterio']
        par(f"{nome}: J de 2026 {br(k_['J_2026'][0], 4)} (ep {br(k_['J_2026'][1], 4, False)}); J de 2022 {br(k_['J_2022'][0], 4)} (ep {br(k_['J_2022'][1], 4, False)}); diferença {br(k_['dif'][0], 4)} "
            f"(ep {br(k_['dif'][1], 4, False)}); mediana do |J| das {k_['n_placebo']} divisas placebo {br(k_['mediana_abs_J_placebo_2026'], 4, False)}. {k_['veredito']}.")
    L.append('  divisa        sem filtro 2026: pares, J (ep)           com filtro 2026: pares, J (ep)           com filtro 2022: pares, J (ep)')
    for dv in [T34_PRINCIPAL] + T34_DESCRITIVAS + T34_PLACEBO:
        cel = lambda r_: (f"{mil(r_['pares']):>5}  {br(r_['J'], 4)} ({br(r_['ep'], 4, False)})" if 'J' in r_ else f"{mil(r_.get('pares', 0)):>5}  menos de 50 pares").ljust(38)
        L.append(f"  {dv:<10}  {cel(t['sem_filtro']['2026'][dv])}  {cel(t['com_filtro']['2026'][dv])}  {cel(t['com_filtro']['2022'][dv])}")
    td = t['todas_as_divisas']
    par(f"Todas as divisas de UF do país com 50 pares ou mais, com o filtro: {td['n_divisas_com_50_pares']}; limiar de Bonferroni {br(td['z_bonferroni'], 2, False)} ep; passam o critério: "
        f"{len(td['passam'])}; sem Bonferroni: {len(td['passam_sem_bonferroni'])}; mediana do |J| {br(td['mediana_abs_J_2026'], 4, False)}.")
    x1 = x['X1_sp_mg_e_mg_rj_sem_filtro']['SP-MG']; cm = t['composicao_dos_eliminados']['SP-MG']
    hubs = x1['locais_com_mais_de_200_pares']
    par(f"SP-MG. Sem filtro: {br(t['sem_filtro']['2026']['SP-MG']['J'], 4)} (ep {br(t['sem_filtro']['2026']['SP-MG']['ep'], 4, False)}), {mil(t['sem_filtro']['2026']['SP-MG']['pares'])} pares. "
        f"Com filtro: {br(t['com_filtro']['2026']['SP-MG']['J'], 4)} (ep {br(t['com_filtro']['2026']['SP-MG']['ep'], 4, False)}), {mil(t['com_filtro']['2026']['SP-MG']['pares'])} pares. "
        f"O cadastro põe {len(hubs)} locais de MG dentro da Grande São Paulo (latitude perto de -23,6, longitude perto de -46,6), a {br(min(h['km_do_centroide_do_municipio'] for h in hubs), 0, False)} a "
        f"{br(max(h['km_do_centroide_do_municipio'] for h in hubs), 0, False)} km dos seus municípios; cada um vira par de {', '.join(mil(h['pares']) for h in sorted(hubs, key=lambda h: h['pares']))} "
        f"locais paulistas. Esses pares são {mil(x1['pares_desses_locais']['pares'])} dos {mil(x1['sem_filtro_M0']['pares'])} e {br(100 * x1['pares_desses_locais']['peso_no_J'], 0, False)}% do peso; "
        f"só neles J = {br(x1['pares_desses_locais']['J_so_deles'], 4)}. Tirando só esses locais (exploratório, X1): {br(x1['sem_filtro_sem_esses_locais_M0']['J'], 4)} "
        f"(ep {br(x1['sem_filtro_sem_esses_locais_M0']['ep'], 4, False)}).")
    par(f"Explicação pela composição dos eliminados (Zema e Cury separados, M1; mais Caiado e Renan Santos, M2). Sem filtro: M0 {br(x1['sem_filtro_M0']['J'], 4)}, M1 {br(x1['sem_filtro_M1']['J'], 4)}, "
        f"M2 {br(x1['sem_filtro_M2']['J'], 4)}: separar os eliminados tira {br(100 * (1 - abs(x1['sem_filtro_M1']['J']) / abs(x1['sem_filtro_M0']['J'])), 0, False)}% do salto, não a metade exigida. "
        f"Com filtro: M0 {br(cm['M0']['J'], 4)} (ep {br(cm['M0']['ep'], 4, False)}), M1 {br(cm['M1']['J'], 4)}, M2 {br(cm['M2']['J'], 4)}: não sobra salto para explicar. Nos pares filtrados, Zema teve "
        f"{br(cm['fatias_1t_nos_pares_pct_comp']['a']['Z1'], 2, False)}% do lado de SP e {br(cm['fatias_1t_nos_pares_pct_comp']['b']['Z1'], 2, False)}% do lado de MG; Cury, "
        f"{br(cm['fatias_1t_nos_pares_pct_comp']['a']['CU1'], 2, False)}% e {br(cm['fatias_1t_nos_pares_pct_comp']['b']['CU1'], 2, False)}%. O salto de -0,034 era erro de coordenada, não composição dos eliminados.")
    x1r = x['X1_sp_mg_e_mg_rj_sem_filtro']['MG-RJ']
    par(f"MG-RJ: sem filtro {br(t['sem_filtro']['2026']['MG-RJ']['J'], 4)} (ep {br(t['sem_filtro']['2026']['MG-RJ']['ep'], 4, False)}); com filtro {br(t['com_filtro']['2026']['MG-RJ']['J'], 4)} "
        f"(ep {br(t['com_filtro']['2026']['MG-RJ']['ep'], 4, False)}). {len(x1r['locais_tirados_ao_todo'])} locais de MG com a mesma coordenada do centro do Rio de Janeiro respondiam por "
        f"{br(100 * x1r['pares_desses_locais']['peso_no_J'], 0, False)}% do peso.")
    nm = x.get('nominais_2t_por_uf_2026', {})
    if nm:
        nsul = nm['PR'] + nm['SC'] + nm['RS']; j_ = t['com_filtro']['criterio']['J_2026']
        par(f"Em votos: um J de {br(j_[0], 4)} na fatia de Lula, aplicado aos {mil(nsul)} votos nominais de PR, SC e RS, seria {mil(abs(2 * j_[0] * nsul))} votos de margem; o limite de 95% "
            f"({br(j_[0] + 1.96 * j_[1], 4)}) seria {mil(2 * (j_[0] + 1.96 * j_[1]) * nsul)}. Nada perto da margem.")

    tit('O QUE PESA A FAVOR DA TESE')
    par(f"1. O coeficiente de 2026 ({br(c26, 4)}) é o único positivo dos quatro anos e fica longe de 2014 ({br(A['2014']['base']['coef']['branco_nulo_1t'], 3)}), o outro ano em que o branco e nulo caiu entre os "
        f"turnos. A queda do branco e nulo, sozinha, não explica o sinal positivo. Pela letra do registro, isso é indício a cruzar com as divisas.", 3, '')
    par(f"2. Na divisa, o branco e nulo é {br(abs(jb), 2, False)} ponto mais baixo no lado de um cargo só ({br(abs(jb / eb), 1, False)} ep; {nneg} das {ndiv} divisas com o mesmo sinal), e a maior parte do que falta aparece como voto de "
        f"Lula ({br(100 * x8['2026_M0']['fracao_para_o_PT_ic95'][0], 0, False)}%, exploratório). Lido inteiro a favor da tese, o salto de Lula vale de {mil(tvc['salto_lula_em_votos'])} a {mil(x5['salto_lula_em_votos'])} votos.", 3, '')
    par(f"3. Dentro do mesmo local, seção com mais branco e nulo no 1º turno deu mais ganho a Lula que a Flávio em 2026 ({br(x6['todas']['coef_B1'][0], 2)} e {br(x6['todas']['coef_N1'][0], 2)} por voto), "
        f"a maior assimetria dos quatro anos.", 3, '')
    tit('O QUE PESA CONTRA')
    par(f"1. O contraste que a tese pede (6 UFs poupadas contra 21) não aparece na regressão: o coeficiente é maior nas 6 ({br(A['2026']['com_gov_2t']['coef']['branco_nulo_1t'], 3)}) que nas 21 "
        f"({br(A['2026']['sem_gov_2t']['coef']['branco_nulo_1t'], 3)}), e a assimetria do item 3 acima é igual nos dois grupos.", 3, '')
    par(f"2. A queda maior do branco e nulo onde só há presidente existe em 2014, 2018, 2022 e 2026, significativa em todos. Não é marca de 2026.", 3, '')
    par(f"3. O salto de Lula na divisa ({br(jl, 3)}, {br(jl / el, 1, False)} ep; {br(x5['z_observado_contra_zero_ep_por_divisa'], 1, False)} ep com a divisa como unidade) não passa do limiar e é do tamanho do que as divisas "
        f"fazem quando nada deveria saltar (mediana {br(ng['lula_res_abs_mediana'], 2, False)}). O mesmo padrão aparece mais forte em 2018 ({br(cr['salto_lula_equivalentes']['2018'][0], 2)}), ano que o PT perdeu.", 3, '')
    par(f"4. O adversário também ganha no lado de um cargo só: {br(x8['2026_M0']['ganho_residual_adversario'][0], 2)} ponto residual na divisa e {br(kb['dif_sem_menos_com']['dR'], 2)} "
        f"ponto dos aptos entre os grupos de UFs. Conversão de branco em Lula não produz isso.", 3, '')
    par(f"5. Nas 6 UFs, onde a mesma urna dá a referência do governador, o branco e nulo de presidente se comporta como nas 26 UFs placebo. Isso exclui ali a conversão de 52% que viraria o resultado; "
        f"não exclui taxas de até {br(100 * x3['conversao_compativel_com_o_p90_do_placebo'], 0, False)}%.", 3, '')
    par(f"6. Entre as {x11['2026']['mesmo_grupo']['n']} divisas de UFs do mesmo grupo, onde o branco e nulo cai mais a fatia de Lula não sobe mais: inclinação {br(x11['2026']['mesmo_grupo']['inclinacao'], 2)} "
        f"(ep {br(x11['2026']['mesmo_grupo']['ep'], 2, False)}); conversão daria cerca de {br(x5['salto_de_lula_se_o_salto_inteiro_do_bn_fosse_conversao'] / jb, 2)} (exploratório, X11). Nas {x11['2026']['mistas']['n']} "
        f"divisas mistas a inclinação é {br(x11['2026']['mistas']['inclinacao'], 2)} (ep {br(x11['2026']['mistas']['ep'], 2, False)}).", 3, '')
    par(f"7. Há mecanismo inocente com evidência direta, ainda pequena: nas 12 seções do AC com RDV, {br(ac['pct_do_comparecimento_nulo_pres_com_numero_de_gov'], 1, False)}% dos eleitores anularam o voto de presidente "
        f"digitando o número de candidato a governador." if ('por_uf' in x4 and 'AC' in x4['por_uf']) else '7. (RDV do AC não lido.)', 3, '')
    tit('O QUE ISSO SIGNIFICA')
    zbn = abs(x9['salto_bn_esperado'] - jb) / x10['dp_da_media_bn']; zlu = abs(x9['salto_lula_esperado'] - jl) / x10['dp_da_media_lula']
    vp = x3['votos_no_pais_se_a_taxa_valesse_nas_27']
    par(f"O canal do branco e nulo tem teto nas duas formas. Só nas 21 UFs: todo o desnível de branco e nulo entre os dois lados da divisa vale de {mi(abs(tvc['salto_bn_em_votos']))} a "
        f"{mi(x5['salto_bn_em_votos'])} de votos (limite de 95%: {mi(x5['salto_bn_ic95_em_votos'][1])}), cerca de metade da margem de {mil(MARGEM)}. A conversão que virasse o resultado por esse caminho "
        f"pediria {br(1 / x9['observado_sobre_esperado_bn'], 1, False)} vezes esse desnível (fica a {br(zbn, 1, False)} desvios do observado pela régua das divisas do mesmo grupo) e "
        f"{br(1 / x9['observado_sobre_esperado_lula'], 1, False)} vezes o salto de Lula ({br(zlu, 1, False)} desvios pela mesma régua; {br(abs(x9['z_lula_observado_contra_esperado']), 1, False)} ep pelo bootstrap de municípios).")
    par(f"Em todo o país: nas 6 UFs, único lugar com régua na mesma urna, a conversão de 52% que viraria o resultado exigiria uma subida natural da razão maior que qualquer uma já vista. O que os números "
        f"dali deixam passar vai de {br(100 * x3['conversao_equivalente_fracao_do_bn_antes'], 0, False)}% (contra a mediana do placebo; {mi(vp['mediana'])} no país) a "
        f"{br(100 * x3['conversao_compativel_com_o_p90_do_placebo'], 0, False)}% (percentil 90; {mi(vp['p90'])}) ou {br(100 * x3['conversao_compativel_com_o_maximo_do_placebo'], 0, False)}% (máximo; {mi(vp['maximo'])}).")
    par(f"O que fica em aberto, portanto, é uma conversão parcial de até cerca de 2 milhões de votos, o tamanho que a equipe vermelha apontou: os dados por seção não a distinguem de eleitor que, sem a tela "
        f"de governador, deixou de anular e votou. Sozinha não vira o resultado; somada a outro canal, importaria. Nenhum resultado daqui passa pelos três filtros do Adendo 27 (conferente, calibração, espelho).")
    tit('PISTAS')
    par('1. D4-3 e D4-4 (onda D): os RDV mostram o que foi digitado em cada nulo. Se o nulo de presidente das 6 UFs for, em boa parte, número de governador, o desnível de branco e nulo está explicado sem '
        'conversão; se não for, o item (c) volta a pesar. É o teste que decide este canal.', 3, '')
    ct = x10['contribuicao_por_divisa_lula']; tb_ = t['todas_as_divisas']['tabela']
    es_ = sum(v_['contribuicao'] for dv_, v_ in ct.items() if dv_.startswith('ES-'))
    par(f"2. Divisas do ES: respondem por {br(es_, 3)} do salto de Lula de {br(jl, 3)} (ES-MG {br(ct['ES-MG']['contribuicao'], 3)}, ES-RJ {br(ct['ES-RJ']['contribuicao'], 3)}; DF-GO {br(ct['DF-GO']['contribuicao'], 3)}). "
        f"ES-RJ já saltava em 2022 ({br(100 * tb_['ES-RJ']['J_2022'], 2)}, contra {br(100 * tb_['ES-RJ']['J_2026'], 2)} em 2026); ES-MG não ({br(100 * tb_['ES-MG']['J_2022'], 2)} contra "
        f"{br(100 * tb_['ES-MG']['J_2026'], 2)}). Vale olhar município a município.", 3, '')
    vu = B['2026']['var_por_uf']; ordem = sorted(vu, key=lambda u_: vu[u_])
    par(f"3. As maiores quedas de branco e nulo entre os turnos foram em {ordem[0]} ({br(vu[ordem[0]], 2)}), {ordem[1]} ({br(vu[ordem[1]], 2)}) e {ordem[2]} ({br(vu[ordem[2]], 2)}), todas do grupo das 21, e há "
        f"divisas entre UFs do mesmo grupo com salto de branco e nulo de até {br(ng['dbn_abs_max'], 2, False)} ponto. O contraste 6 contra 21 não explica isso. Entre as {x11['2026']['todas']['n']} divisas de 2026, o salto de Lula "
        f"anda {br(x11['2026']['todas']['inclinacao'], 2)} por ponto de salto do branco e nulo (ep {br(x11['2026']['todas']['ep'], 2, False)}; exploratório, X11); em 2018 era "
        f"{br(x11['2018']['todas']['inclinacao'], 2)} (ep {br(x11['2018']['todas']['ep'], 2, False)}), em 2022 {br(x11['2022']['todas']['inclinacao'], 2)} e em 2014 {br(x11['2014']['todas']['inclinacao'], 2)}.", 3, '')
    par(f"4. O cadastro de locais reprova {fl['fora_da_caixa'] + fl['longe_do_centroide']} coordenadas no filtro, {fl['fora_da_caixa_por_uf'].get('MG', 0) + fl['longe_por_uf'].get('MG', 0)} delas em MG; "
        f"todo teste geográfico precisa do filtro (T23b incluído).", 3, '')
    tit('DESVIOS E DECISÕES FORA DO REGISTRO')
    for i, s_ in enumerate(desvios, 1):
        par(f'{i}. {s_}', 3, '')
    tit('ARQUIVOS')
    for s_ in ('scripts/analisar_R27_A1.py', 'resultados/R27_A1_branco_nulo.json', 'resultados/R27_A1_branco_nulo.txt',
               '/home/user/trabalho-eleicao/adendo27/R27_A1/ (parciais por parte, logs, docstring registrado antes de rodar, parciais da primeira execução)'):
        L.append('  ' + s_)
    txt = '\n'.join(L) + '\n'
    assert chr(8212) not in txt and chr(8211) not in txt, 'travessão no texto'
    open(_os.path.join(RESULT, 'R27_A1_branco_nulo.txt'), 'w', encoding='utf-8').write(txt)
    diga('gravados: resultados/R27_A1_branco_nulo.json e .txt')


# ---------------------------------------------------------------- principal
def limpar(o):
    if isinstance(o, dict): return {str(k): limpar(v) for k, v in o.items()}
    if isinstance(o, (list, tuple)): return [limpar(v) for v in o]
    if isinstance(o, np.ndarray): return limpar(o.tolist())
    if isinstance(o, (np.floating,)): return float(o)
    if isinstance(o, (np.integer,)): return int(o)
    if isinstance(o, (np.bool_,)): return bool(o)
    if isinstance(o, float) and (math.isnan(o) or math.isinf(o)): return None
    return o


def main():
    global TRAB
    arg = lambda f, pad: sys.argv[sys.argv.index(f) + 1] if f in sys.argv else pad
    partes = arg('--partes', 'a,b,d,c,t').split(',')
    TRAB = arg('--trab', TRAB); _os.makedirs(TRAB, exist_ok=True)
    t0 = time.time()
    S = {ano: carregar_ano(ano) for ano in ANOS}
    GOV = grupos_gov(S)
    diga('UFs com 2º turno de governador:', json.dumps({str(a): GOV[a] for a in ANOS}))
    diga('tipos de seção:', json.dumps({str(a): S[a][3] for a in ANOS}, ensure_ascii=False))
    cand26 = carregar(_os.path.join(DADOS, 'candidatos2026_1t.json.gz')) if set(partes) & {'d', 'c', 't'} else None
    res = {}
    def guarda(nome, r):
        res[nome] = limpar(r)
        json.dump(res[nome], open(_os.path.join(TRAB, f'parte_{nome}.json'), 'w'), ensure_ascii=False)
    if 'a' in partes: guarda('a', parte_a(S, GOV)); diga('tempo', round(time.time() - t0))
    if 'b' in partes: guarda('b', parte_b(S, GOV)); diga('tempo', round(time.time() - t0))
    if 'd' in partes: guarda('d', parte_d(S, GOV, cand26)); diga('tempo', round(time.time() - t0))
    if 'c' in partes or 't' in partes:
        geo = Geo(); diga('filtro de coordenadas:', json.dumps(geo.resumo()))
        c, LOC = parte_c(S, GOV, geo, cand26); guarda('c', c); diga('tempo', round(time.time() - t0))
        if 't' in partes: guarda('t', parte_t(S, geo, LOC, cand26, res['c'])); diga('tempo', round(time.time() - t0))
    open(_os.path.join(TRAB, 'log_' + '_'.join(partes) + '.txt'), 'w').write('\n'.join(LOG) + '\n')
    if set(partes) >= {'a', 'b', 'd', 'c', 't'}:
        res['exploratorio'] = limpar(exploratorio(S, GOV, geo, LOC, res, cand26))
        open(_os.path.join(TRAB, 'log_x.txt'), 'w').write('\n'.join(LOG) + '\n')
        json.dump(res['exploratorio'], open(_os.path.join(TRAB, 'parte_x.json'), 'w'), ensure_ascii=False)
        escrever(res, GOV, time.time() - t0)


if __name__ == '__main__':
    main()
