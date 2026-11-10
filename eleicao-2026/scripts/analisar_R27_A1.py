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
        res['exploratorio'] = limpar(exploratorio(S, GOV, geo, LOC, res))
        json.dump(res['exploratorio'], open(_os.path.join(TRAB, 'parte_x.json'), 'w'), ensure_ascii=False)
        escrever(res, GOV, time.time() - t0)


if __name__ == '__main__':
    main()
