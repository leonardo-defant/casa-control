#!/usr/bin/env python3
"""R27_A3: TROCA PROPORCIONAL COM RÉGUA INTERNA (Adendo 27, Onda A, item A3).

Quatro retestes da equipe vermelha (registro/adendo27/equipe_vermelha_relatorio.json, commit 2748895,
10/11/2026 00:16:42 UTC), aplicados pela letra, sem mudar limiar:
  Parte 1: fragilidade "T14 (troca proporcional por seção)": T8 por decil de capacidade de troca de eleitores.
  Parte 2: fragilidade "T16 (piso da troca uniforme por UF)": estratos de reduto e três formas de troca.
  Parte 3: fragilidade "T7 (ganho além do bolo)": limite aritmético estrito, por UF e por faixa.
  Parte 4: fragilidade "L1 e L3", parte do L3: núcleo do PL por decil de capacidade.
Aviso do próprio registro: estes retestes foram escritos por quem já conhecia os resultados antigos. O critério é
novo, mas a escolha do que retestar é posterior ao dado.

Este docstring foi escrito ANTES de calcular qualquer resultado com votos. Cópia com data e SHA-256 em
/home/user/trabalho-eleicao/adendo27/R27_A3/docstring_antes_de_rodar.txt. Não havia execução anterior deste
teste em disco (nem script, nem pasta de trabalho) quando este arquivo foi criado.

Uso (sempre com python3 -I):
  python3 -I scripts/analisar_R27_A3.py extrair   lê deputado federal do 1º turno no bweb (filtro por bytes)
  python3 -I scripts/analisar_R27_A3.py           roda as quatro partes e grava resultados/R27_A3_troca_regua_interna.json e .txt
  python3 -I scripts/analisar_R27_A3.py texto     só reescreve o .txt a partir do .json

O QUE O REGISTRO FIXA (texto dos campos reteste_proposto e criterio_proposto)
Parte 1 (T14). "Rodar a regressão do T8 por decil de capacidade de troca de eleitores, c = (aptos - comparecimento
  do 1º turno)/aptos, só em seções com aptos iguais nos dois turnos. [...] Calibrar plantando 2% e 3,6% de troca e
  exigindo recuperação a 0,3 ponto em cada decil. Somar também o limite aritmético: votos de Lula que excedem
  eliminados mais todo o branco e nulo do 1º turno mais todos os faltosos do 1º turno da seção."
  "SINAL (a troca de eleitores não explica): coeficiente de Flávio no decil de menor capacidade de pelo menos 0,03 a
  mais de 4 ep e de pelo menos 80% do coeficiente do decil de maior capacidade. SEM SINAL: coeficiente do decil de
  menor capacidade abaixo de 0,015 ou abaixo de 40% do decil superior. Limite aritmético: indício se a soma passar
  de 2,8 milhões."
Parte 2 (T16). "Refazer com estratos de reduto em vez de UF: seções no 1% e nos 5% de maior fatia de Flávio no 1º
  turno e no quintil de maior fatia do PL para deputado federal (L3), com calibração plantada de troca proporcional
  a F, proporcional a L e proporcional ao total. Relatar o piso de cada forma em separado."
  "EXCLUSÃO de troca s x F de 2% ou mais: coeficiente no estrato de reduto mais 2 ep abaixo de 0,02 menos o menor
  coeficiente natural plantado (usar o do estrato espelho de Lula em 2026, não outro ano). SINAL: coeficiente de
  reduto de 0,03 ou mais a mais de 4 ep. Para a forma k x L: coeficiente próprio de Lula por estrato; indício se
  ficar a menos de 0,01 de zero em todos os estratos enquanto o de Flávio passa de 0,04."
Parte 3 (T7). "T7 estrito com limite aritmético: bolo máximo = eliminados + todo o branco e nulo do 1º turno +
  todos os faltosos do 1º turno. Por UF e por faixa, com calibração plantada de 1%, 2% e 3,6% dentro de 2026 (não
  em 2022) para saber quanto cada ponto de troca acrescenta ao (a)."
  "SINAL: excesso estrito somado acima de 0,6 milhão de votos [...] ou (a) da faixa abaixo de 35% acima do (a)
  plantado com 3% sobre a faixa de 65% ou mais. SEM SINAL: excesso estrito abaixo de 0,1 milhão e gradiente por
  faixa igual ao espelho de Flávio."
Parte 4 (L3). "L3 dentro de faixas de capacidade de troca de eleitores (ver T14) e só no quintil de maior fatia do
  PL." "INDÍCIO: P5 de -0,025 ou menos a mais de 4 ep no decil de menor capacidade. SEM SINAL: P5 acima de -0,010
  nesse decil."

DECISÕES QUE O REGISTRO NÃO FIXA (tomadas aqui, antes de qualquer conta com votos; relatadas como desvios)

Gerais
G1. Base: dados/secoes2026.json.gz e dados/candidatos2026_1t.json.gz. Seções com os dois turnos. Local de votação
    = UF, município, zona e número do local do 2º turno (lib.chave_local).
G2. Regressão do T8 como registrada para 2026 (analisar_fluxo_regressao.py): y = votos do candidato no 2º turno
    menos no 1º; X = votos de Cury (70), Renan (14), Caiado (55), Zema (30) e demais outros no 1º turno, queda do
    branco+nulo (1º menos 2º, sem truncar), variação do comparecimento (2º menos 1º), votos do adversário no 1º
    turno e votos do próprio no 1º turno; efeito fixo de local, sem peso, erro agrupado por local (CR1). Rodada
    em separado dentro de cada decil ou estrato: local com uma seção só dentro do recorte não informa e sai.
    Estimador escrito aqui (mesma conta de lib.fe_ols), conferido contra lib.fe_ols e contra os números já
    publicados (T14 nacional 0,0393; L3 P1 e P5; T7 original 8,99%).
G3. "Coeficiente de Flávio" = coeficiente dos votos de Flávio no 1º turno na regressão do ganho de Lula (o
    coeficiente do T14). Como no 2º turno não há outros candidatos, ganho de Lula + ganho de Flávio = outros do
    1º turno + queda do branco+nulo + variação do comparecimento, exatamente; logo esse coeficiente é igual, com o
    sinal trocado, ao coeficiente próprio de Flávio na regressão do ganho de Flávio (o "P" do L3). A identidade é
    conferida numericamente. Espelho: coeficiente dos votos de Lula no 1º turno na regressão do ganho de Flávio,
    igual a menos o coeficiente próprio de Lula.
G4. "A mais de N ep": distância a zero em erros-padrão (principal, como o L3 leu a mesma expressão). Ao lado, a
    distância ao próprio limiar. Se as duas leituras derem vereditos diferentes, isso é dito.
G5. Plantio (calibração), sempre por cima dos dados de 2026, em todas as seções com os dois turnos: d votos saem
    de Flávio no 2º turno e entram em Lula no 2º turno; 1º turno, branco, nulo e comparecimento ficam intactos.
    Forma F (s x F): d = binomial(R2, s). Forma L (k x L): d = binomial(R2, min(1, k L2/R2)), com k resolvido para
    que o total esperado seja igual ao da forma F do mesmo tamanho. Forma total: o mesmo com L2 + R2 no lugar de
    L2. Tamanhos: 1%, 2%, 3% e 3,6% dos votos de Flávio no 2º turno (3,6% é o número do registro; o que vira o
    resultado é 3,57%). Semente 20261110 mais o índice do cenário. Ao lado, a versão pelo valor esperado (sem
    sorteio), usada para medir inclinações. Espelho do plantio: de Lula para Flávio, binomial(L2, s).
    Forma concentrada (só ao lado): mesmo total de 3,6%, proporcional a R2 vezes a fatia de Lula no 1º turno.
G6. Regra do SEM PODER (vale para as quatro partes): se o critério de sinal não dispara nos dados brutos e também
    não dispara com a irregularidade registrada plantada por cima (forma F, 3,6%), o veredito da parte é SEM
    PODER, mesmo que a letra desse SEM SINAL ou INCONCLUSIVO. Também é SEM PODER se a recuperação exigida pelo
    registro falhar no recorte que decide o critério. Se o critério dispara nos dados brutos, vale a letra, e a
    calibração e o espelho dizem se o disparo conta como indício (avisos ii e iii do Adendo 27).
G7. Fatia de um candidato no 1º turno da seção = votos dele sobre os válidos do 1º turno (L + R + outros, menos o
    28, anulado), como no T7 original.
G8. Deputado federal do 1º turno: linhas com CD_CARGO_PERGUNTA 6 dos zips do bweb do 1º turno, filtradas por
    bytes. PL = partido 22, nominal mais legenda; PT = partido 13; válidos = nominal mais legenda. Quintil de
    maior fatia = fatia acima do percentil 80 entre as seções com os dois turnos, fora do exterior, com válidos
    de deputado maiores que zero (o universo do L3). Conferências: cortes e P1 e P5 do L3 publicados.
G9. Outros anos (2014, 2018, 2022) não entram em nenhum veredito. Só na Parte 1, ao lado, sai o perfil por decil
    desses anos (outros agregados), com o valor bruto de 2026 na mesma linha, marcado como "não é régua".
G10. Tradução em votos: troca s x F com s em fração dos votos verdadeiros de Flávio; votos trocados = s/(1 - s) x
    59.826.041 (oficial de Flávio no 2º turno); efeito na margem = 2 vezes isso, contra a margem oficial de
    4.430.191 (vira com 2.215.096 votos trocados, s = 3,57%). Um coeficiente b inteiro atribuído a desvio
    equivale a s = b (premissa extrema: nível natural zero); com o espelho de Lula como nível natural, s =
    (b - b_espelho)/(1 - b_espelho). As duas leituras saem lado a lado, cada uma com a sua premissa.
G11. O que for feito depois de ver resultados fica em funções com nome "exploratorio_" e sai marcado assim.

Parte 1 (T14 por decil de capacidade)
P1.1 Universo: seções com os dois turnos e aptos iguais (e maiores que zero) nos dois turnos, com o exterior, como
     o T14 original. Ao lado: sem o exterior.
P1.2 c = (aptos - comparecimento do 1º turno)/aptos. Decis: cortes nos percentis 10 a 90 de c entre as seções do
     universo, sem peso (numpy.quantile linear). D1: c <= p10 (menor capacidade); D10: c > p90.
P1.3 Critério. SINAL se b(D1) >= 0,03, b(D1)/ep > 4 e b(D1) >= 0,8 x b(D10). SEM SINAL se b(D1) < 0,015 ou b(D1) <
     0,4 x b(D10). Senão INCONCLUSIVO. As comparações com o D10 são de ponto, como está escrito; ao lado sai o
     erro-padrão de b(D1) - 0,8 b(D10) e de b(D1) - 0,4 b(D10) com a covariância entre decis (mesmo local em
     decis diferentes), pela função de influência por local.
P1.4 Calibração registrada: recuperação no decil = (b com plantio menos b bruto) em pontos; aprovada se ficar a
     0,3 ponto do tamanho plantado (2% e 3,6%, forma F). Pela letra vale para cada decil; SEM PODER se falhar no
     D1 (o decil que decide). Falha em outro decil é relatada e não muda o veredito.
     Além disso (regra G6): o critério da P1.3 aplicado aos dados com 2% e com 3,6% plantados.
P1.5 Espelho: o mesmo critério com o coeficiente espelho (votos de Lula no 1º turno na regressão do ganho de
     Flávio), nos mesmos decis; e a recuperação do plantio espelho.
P1.6 Limite aritmético: é o excesso estrito da Parte 3 (uma conta só). Indício se a soma passar de 2,8 milhões.
P1.7 Ao lado, sem entrar no veredito: outros agregados em vez dos grupos; sem o exterior; quintis de c; regressão
     empilhada com efeito fixo de local comum a todos os decis (inclinações e interceptos por decil); interação
     contínua (todos os regressores vezes c, mais c), que dá o coeficiente de Flávio extrapolado para capacidade
     zero; reta ponderada dos dez coeficientes contra o c médio do decil; perfil de 2014, 2018 e 2022 (G9).

Parte 2 (T16 por estrato de reduto)
P2.1 Universo: seções com os dois turnos, fora do exterior, válidos do 1º turno maiores que zero (o T16 original
     também deixava o exterior fora). Estratos de reduto de Flávio: R1 = fatia de Flávio acima do percentil 99; R5
     = acima do percentil 95; RPL = quintil de maior fatia do PL (G8). Estratos espelho de Lula: fatia de Lula
     acima dos percentis 99 e 95; quintil de maior fatia do PT.
P2.2 SINAL no estrato: b >= 0,03 e b/ep > 4 (G4). SINAL da parte: nos três estratos.
P2.3 EXCLUSÃO de troca s x F de 2% ou mais. A frase do registro ("abaixo de 0,02 menos o menor coeficiente natural
     plantado") admite mais de uma leitura. Leitura principal, fixada aqui: o coeficiente do reduto, mais 2 ep,
     menos o nível natural, fica abaixo de 0,02; isto é, b + 2 ep < 0,02 + n, com n = o menor dos três
     coeficientes espelho de Lula em 2026 (o nível natural mais baixo, o mais exigente entre as leituras
     coerentes). Ao lado: (i) a aritmética literal, b + 2 ep < 0,02 - n; (ii) n = o maior dos três espelhos;
     (iii) cada estrato contra o próprio espelho; (iv) o espelho com 2% de fato plantados de Lula para Flávio.
     EXCLUSÃO da parte: em pelo menos um estrato (uma troca uniforme tem de aparecer em todos) e SINAL em nenhum.
     Qualquer outro caso: INCONCLUSIVO. No resumo, EXCLUSÃO conta como SEM SINAL para troca s x F de 2% ou mais.
P2.4 Poder (além da regra G6): o estrato só entra na exclusão se 2 ep < 0,02 e se a recuperação do plantio de 2%
     e de 3,6% (forma F) ficar a 0,3 ponto. Se nenhum estrato passar, SEM PODER.
P2.5 Forma k x L. Coeficiente próprio de Lula (votos de Lula no 1º turno na regressão do ganho de Lula) por
     estrato. "Todos os estratos" = os três estratos de reduto do reteste (principal); ao lado, os três
     espelhos e o país. INDÍCIO se, nos três, |próprio de Lula| < 0,01 e o coeficiente de Flávio > 0,04. O
     registro não fixa critério de sem sinal para esta forma: sem indício e com poder, INCONCLUSIVO; sem indício
     e sem que a cláusula dispare com a forma L de 3,6% plantada, SEM PODER.
P2.6 "Piso de cada forma": para cada forma (F, L, total), a inclinação = variação do coeficiente de Flávio no
     estrato por unidade de troca (total trocado sobre os votos de Flávio no país), medida no plantio pelo valor
     esperado com 3,6%. Tamanho máximo compatível = o menor, entre os estratos com inclinação de 0,1 ou mais, de
     (b + 2 ep - n)/inclinação, com n = 0 (premissa: sem desvio, o reduto não perde eleitor líquido) e com n = o
     menor espelho. Se nenhuma inclinação chega a 0,1, o coeficiente de reduto é cego para a forma. Sai também a
     inclinação do coeficiente próprio de Lula em cada forma.

Parte 3 (T7 estrito)
P3.1 Universo: todas as seções com os dois turnos (como o T7). Ao lado: só aptos iguais; sem o exterior.
P3.2 Bolo máximo = outros do 1º turno + brancos + nulos do 1º turno + (aptos do 1º turno - comparecimento do 1º
     turno). Excesso estrito = ganho de Lula menos o bolo máximo, quando positivo. Soma no país, por UF e por
     faixa da fatia de Flávio no 1º turno (0 a 35, 35 a 50, 50 a 65, 65 a 100, como o T7).
P3.3 "(a)" na segunda cláusula do sinal e no gradiente: o registro escreve "excesso estrito" na primeira cláusula
     e só "(a)" na segunda. Leitura principal, fixada aqui: (a) é a estatística do T7, % das seções com excesso
     positivo sobre o bolo do Adendo 3 (outros + queda do branco+nulo se positiva + aumento do comparecimento se
     positivo), recalibrada dentro de 2026. Ao lado: as mesmas cláusulas com o (a) do bolo máximo.
P3.4 Cláusula A: soma do excesso estrito > 600.000. Cláusula B: (a) da faixa em que Flávio tem menos de 35% maior
     que o (a) da faixa de 65% ou mais com 3% plantados (forma F) nessa faixa. SINAL se A ou B.
P3.5 SEM SINAL: soma do excesso estrito < 100.000 e gradiente por faixa igual ao espelho. Gradiente = (a) da
     faixa abaixo de 35% do adversário menos (a) da faixa de 65% ou mais. Espelho: a mesma conta para o ganho de
     Flávio, faixas pela fatia de Lula. "Igual" = diferença de até 2 pontos entre os dois gradientes (a
     tolerância que o próprio T7 usava no Adendo 3). Senão INCONCLUSIVO.
P3.6 Calibração: (a), (b) e soma estrita, no país e por faixa, com 1%, 2%, 3% e 3,6% plantados (forma F); quanto
     cada ponto acrescenta ao (a). Regra G6 por cláusula: a cláusula "enxerga" se dispara com 3,6% plantados (para
     a B, o lado direito recebe mais 3% por cima do plantio). Se o sinal bruto vier só de cláusula que não
     enxerga o plantio uniforme, isso é dito no veredito; a forma concentrada sai ao lado.
P3.7 Espelho da cláusula B: (a) de Flávio onde Lula tem menos de 35% contra (a) de Flávio onde Lula tem 65% ou
     mais com 3% plantados de Lula para Flávio.
P3.8 Leitura com premissa (ao lado): troca uniforme equivalente em cada faixa = ((a) de Lula menos (a) espelho de
     Flávio)/inclinação do plantio na faixa.

Parte 4 (L3 por capacidade)
P4.1 Universo: seções do quintil de maior fatia do PL (G8) com aptos iguais nos dois turnos. Decis de capacidade
     com os mesmos cortes nacionais da Parte 1 ("ver T14"). Ao lado: decis recalculados dentro do quintil.
P4.2 P5 = coeficiente próprio de Flávio (G3) na célula quintil do PL x decil. INDÍCIO se P5(D1) <= -0,025 e
     P5(D1)/ep < -4 (G4). SEM SINAL se P5(D1) > -0,010. Senão INCONCLUSIVO.
P4.3 Calibração: plantio de 2% e 3,6% (forma F); recuperação a 0,3 ponto na célula D1; critério com o plantio.
P4.4 Espelho: coeficiente próprio de Lula no quintil de maior fatia do PT x D1, mesmo critério.

Contagem de testes: esta peça aplica 7 cláusulas de decisão (P1.3, limite de 2,8 milhões, P2.2 e P2.3, P2.5,
cláusulas A e B do T7, P4.2). O relatório diz quantas dispararam e o que o acaso daria.
"""
import sys, os, gzip, json, zipfile, glob, time, hashlib, csv
from multiprocessing import Pool
import numpy as np

RAIZ = '/home/user/casa-control/eleicao-2026'
TRAB = '/home/user/trabalho-eleicao/adendo27/R27_A3'
ZIPS1T = '/home/user/trabalho-eleicao/bweb1t/zips'
SAIDA_JSON = RAIZ + '/resultados/R27_A3_troca_regua_interna.json'
SAIDA_TXT = RAIZ + '/resultados/R27_A3_troca_regua_interna.txt'
sys.path.insert(0, RAIZ + '/scripts')
from lib import carregar, chave_local, fe_ols  # noqa: E402

SEMENTE = 20261110
F2_OFICIAL, L2_OFICIAL, MARGEM = 59826041, 64256232, 4430191
GRUPOS = [('Cury', '70'), ('Renan', '14'), ('Caiado', '55'), ('Zema', '30')]
COLS = ['L1', 'R1', 'O1', 'B1', 'N1', 'comp1', 'apt1', 'c28', 'L2', 'R2', 'O2', 'B2', 'N2', 'comp2', 'apt2',
        'g70', 'g14', 'g55', 'g30']
FAIXAS = [(0.0, 0.35), (0.35, 0.50), (0.50, 0.65), (0.65, 1.01)]
NOME_FAIXA = ['0-35', '35-50', '50-65', '65-100']
T0 = time.time()


def log(*a):
    print(f'[{time.time() - T0:6.0f}s]', *a, file=sys.stderr, flush=True)


def gravar(nome, obj):
    os.makedirs(TRAB, exist_ok=True)
    tmp = f'{TRAB}/{nome}.tmp'
    with open(tmp, 'w') as f:
        json.dump(obj, f, ensure_ascii=False, indent=1, default=_jd)
    os.replace(tmp, f'{TRAB}/{nome}')


def _jd(o):
    if isinstance(o, (np.integer,)):
        return int(o)
    if isinstance(o, (np.floating,)):
        return float(o)
    if isinstance(o, (np.bool_,)):
        return bool(o)
    if isinstance(o, np.ndarray):
        return o.tolist()
    raise TypeError(str(type(o)))


# ============================================================ deputado federal do 1º turno (bweb)
DF_COLS = ['comp', 'nom', 'leg', 'bra', 'nul', 'pl', 'pt', 'comp_varia', 'linhas', 'tipo_estranho']


def _ler_zip_df(zpath):
    """Linhas de deputado federal (cargo 6) de um zip do bweb do 1º turno, filtradas por bytes."""
    pat = b';6;"Deputado Federal";'
    z = zipfile.ZipFile(zpath)
    nome = [n for n in z.namelist() if n.lower().endswith('.csv')][0]
    sec = {}
    tot = passou = fallback = 0
    with z.open(nome) as fh:
        cab = [c.strip().strip('"').replace('SG_ UF', 'SG_UF') for c in fh.readline().decode('latin1').strip().split(';')]
        ix = {c: i for i, c in enumerate(cab)}
        nc = len(cab)
        iu, im, iz, isec = ix['SG_UF'], ix['CD_MUNICIPIO'], ix['NR_ZONA'], ix['NR_SECAO']
        icg, ip, ico, it, iq = ix['CD_CARGO_PERGUNTA'], ix['NR_PARTIDO'], ix['QT_COMPARECIMENTO'], ix['CD_TIPO_VOTAVEL'], ix['QT_VOTOS']
        for linha in fh:
            tot += 1
            if pat not in linha:
                continue
            f = linha.rstrip(b'\r\n').split(b';')
            if len(f) != nc:
                f = [x.encode('latin1') for x in next(csv.reader([linha.decode('latin1')], delimiter=';'))]
                fallback += 1
            if f[icg].strip(b'"') != b'6':
                continue
            passou += 1
            k = (f[iu], f[im], f[iz], f[isec])
            s = sec.get(k)
            comp = int(f[ico].strip(b'"'))
            if s is None:
                s = sec[k] = [comp, 0, 0, 0, 0, 0, 0, 0, 0, 0]
            elif s[0] != comp:
                s[7] = 1
            s[8] += 1
            tv = f[it].strip(b'"')
            q = int(f[iq].strip(b'"'))
            if tv == b'1' or tv == b'4':
                s[1 if tv == b'1' else 2] += q
                p = f[ip].strip(b'"')
                if p == b'22':
                    s[5] += q
                elif p == b'13':
                    s[6] += q
            elif tv == b'2':
                s[3] += q
            elif tv == b'3':
                s[4] += q
            else:
                s[9] += 1
    chaves = [f"{k[0].strip(b'\"').decode()}|{int(k[1].strip(b'\"'))}|{int(k[2].strip(b'\"'))}|{int(k[3].strip(b'\"'))}" for k in sec]
    M = np.array(list(sec.values()), np.int64).reshape(-1, len(DF_COLS))
    return os.path.basename(zpath), chaves, M, {'linhas': tot, 'deputado_federal': passou, 'fallback_csv': fallback}


def extrair_df():
    saida = TRAB + '/depfed_1t.npz'
    if os.path.exists(saida):
        log('deputado federal: cache', saida)
        return
    os.makedirs(TRAB, exist_ok=True)
    zips = sorted(glob.glob(ZIPS1T + '/*.zip'), key=lambda p: -os.path.getsize(p))
    chaves, mats, meta = [], [], {}
    with Pool(4) as pool:
        for nome, ks, M, m in pool.imap_unordered(_ler_zip_df, zips):
            log(f'{nome}: {m["linhas"]} linhas, {m["deputado_federal"]} de deputado federal, {len(ks)} seções')
            meta[nome] = m
            chaves += ks
            mats.append(M)
    M = np.vstack([m for m in mats if len(m)])
    assert len(chaves) == len(M) == len(set(chaves)), 'seção repetida entre zips'
    np.savez_compressed(saida, keys=np.array(chaves), M=M)
    gravar('depfed_meta.json', {'zips': len(zips), 'secoes': len(chaves), 'linhas_total': sum(m['linhas'] for m in meta.values()),
                                'linhas_deputado_federal': sum(m['deputado_federal'] for m in meta.values()),
                                'fallback_csv': sum(m['fallback_csv'] for m in meta.values()),
                                'totais': dict(zip(DF_COLS, M.sum(0).tolist())), 'por_zip': meta})
    log('deputado federal gravado', len(chaves), 'seções')


# ============================================================ base de 2026
def montar_base():
    cache = TRAB + '/base2026.npz'
    if os.path.exists(cache):
        z = np.load(cache)
        return {k: z[k] for k in z.files}
    log('lendo secoes2026 e candidatos')
    d = carregar(RAIZ + '/dados/secoes2026.json.gz')
    cand = carregar(RAIZ + '/dados/candidatos2026_1t.json.gz')['secoes']
    rows, locs, keys = [], [], []
    for k, v in d.items():
        if '1' not in v or '2' not in v:
            continue
        a, b = v['1'], v['2']
        cv = cand.get(k, {})
        rows.append([a['L'], a['R'], a['O'], a['B'], a['N'], a['comp'], a['apt'], a.get('c28', 0),
                     b['L'], b['R'], b['O'], b['B'], b['N'], b['comp'], b['apt']] + [cv.get(n, 0) for _, n in GRUPOS])
        locs.append(chave_local(k, b))
        keys.append(k)
    A = np.array(rows, np.int64)
    _, loc = np.unique(np.array(locs), return_inverse=True)
    keys = np.array(keys)
    uf = np.array([k[:2] for k in keys])
    # deputado federal alinhado
    z = np.load(TRAB + '/depfed_1t.npz')
    pos = {k: i for i, k in enumerate(z['keys'].tolist())}
    D = np.full((len(keys), len(DF_COLS)), -1, np.int64)
    idx = np.array([pos.get(k, -1) for k in keys.tolist()])
    D[idx >= 0] = z['M'][idx[idx >= 0]]
    B = {'A': A, 'loc': loc.astype(np.int64), 'keys': keys, 'uf': uf, 'D': D,
         'df_fora_da_base': np.array([len(pos) - int((idx >= 0).sum())])}
    np.savez_compressed(cache, **B)
    del d, cand
    return B


class Base:
    def __init__(self, B):
        A = B['A']
        for i, c in enumerate(COLS):
            setattr(self, c, A[:, i])
        self.loc, self.keys, self.uf, self.D = B['loc'], B['keys'], B['uf'], B['D']
        self.n = len(A)
        self.zz = self.uf == 'ZZ'
        self.queda = (self.B1 + self.N1) - (self.B2 + self.N2)
        self.dcomp = self.comp2 - self.comp1
        self.val1 = self.L1 + self.R1 + self.O1 - self.c28
        v = np.maximum(self.val1, 1).astype(float)
        self.fR1 = np.where(self.val1 > 0, self.R1 / v, np.nan)
        self.fL1 = np.where(self.val1 > 0, self.L1 / v, np.nan)
        G = np.column_stack([self.g70, self.g14, self.g55, self.g30])
        # regressão do ganho de Lula: colunas ... , R1 (adversário), L1 (próprio)
        self.X = np.column_stack([G, self.O1 - G.sum(1), self.queda, self.dcomp, self.R1, self.L1]).astype(float)
        self.Xsg = np.column_stack([self.O1, self.queda, self.dcomp, self.R1, self.L1]).astype(float)
        self.yL = (self.L2 - self.L1).astype(float)
        self.yR = (self.R2 - self.R1).astype(float)
        self.iR, self.iL = 7, 8          # índices em X
        self.iRs, self.iLs = 3, 4        # índices em Xsg
        self.apt_igual = (self.apt1 == self.apt2) & (self.apt1 > 0)
        self.cap = np.where(self.apt1 > 0, (self.apt1 - self.comp1) / np.maximum(self.apt1, 1), np.nan)
        df_ok = (self.D[:, 0] >= 0)
        self.df_val = np.where(df_ok, self.D[:, 1] + self.D[:, 2], 0)
        dv = np.maximum(self.df_val, 1).astype(float)
        self.fPL = np.where(self.df_val > 0, self.D[:, 5] / dv, np.nan)
        self.fPT = np.where(self.df_val > 0, self.D[:, 6] / dv, np.nan)
        self.uni_df = (~self.zz) & (self.df_val > 0)      # universo do L3


# ============================================================ estimador
class Reg:
    """MQO com efeito fixo de grupo e erro agrupado pelo mesmo grupo (CR1), como lib.fe_ols. Guarda a parte que
    não depende de y, para reaproveitar em cada cenário de plantio."""

    def __init__(self, X, g):
        X = np.asarray(X, float)
        ug, gi = np.unique(g, return_inverse=True)
        cnt = np.bincount(gi)
        self.ok = cnt[gi] >= 2
        if self.ok.sum() == 0:
            raise ValueError('nenhum grupo com 2 ou mais seções')
        X = X[self.ok]
        self.ug, self.gi = np.unique(np.asarray(g)[self.ok], return_inverse=True)
        self.G = len(self.ug)
        self.n, self.k = X.shape
        self.cg = np.bincount(self.gi, minlength=self.G).astype(float)
        self.Xd = X - self._med(X)
        self.inv = np.linalg.inv(self.Xd.T @ self.Xd)
        self.c = self.G / (self.G - 1) * (self.n - 1) / (self.n - self.k) if self.G > 1 else float('nan')

    def _med(self, M):
        if M.ndim == 1:
            return (np.bincount(self.gi, weights=M, minlength=self.G) / self.cg)[self.gi]
        return np.column_stack([np.bincount(self.gi, weights=M[:, j], minlength=self.G) for j in range(M.shape[1])])[self.gi] / self.cg[self.gi][:, None]

    def fit(self, y, influencia=False):
        y = np.asarray(y, float)[self.ok]
        yd = y - self._med(y)
        b = self.inv @ (self.Xd.T @ yd)
        e = yd - self.Xd @ b
        S = np.column_stack([np.bincount(self.gi, weights=self.Xd[:, j] * e, minlength=self.G) for j in range(self.k)])
        IF = (S @ self.inv) * np.sqrt(self.c)
        V = IF.T @ IF
        out = {'b': b, 'ep': np.sqrt(np.diag(V)), 'n': int(self.n), 'locais': int(self.G)}
        if influencia:
            out['IF'] = IF
            out['ug'] = self.ug
        return out


def cov_cruzada(fa, ja, fb, jb):
    """Covariância entre o coeficiente ja do ajuste fa e o jb do ajuste fb (mesmos locais em recortes diferentes)."""
    comum, ia, ib = np.intersect1d(fa['ug'], fb['ug'], assume_unique=True, return_indices=True)
    return float((fa['IF'][ia, ja] * fb['IF'][ib, jb]).sum())


# ============================================================ plantio
def _resolver_k(R2, w, alvo):
    lo, hi = 0.0, 1.0
    while np.minimum(R2, hi * w).sum() < alvo:
        hi *= 2
        if hi > 1e6:
            raise ValueError('alvo inalcançável')
    for _ in range(80):
        mid = (lo + hi) / 2
        if np.minimum(R2, mid * w).sum() < alvo:
            lo = mid
        else:
            hi = mid
    return (lo + hi) / 2


def cenarios(Bz):
    """Vetores d (votos tirados de Flávio no 2º turno e somados a Lula; negativo no plantio espelho)."""
    R2, L2 = Bz.R2.astype(float), Bz.L2.astype(float)
    Ri, Li = Bz.R2, Bz.L2
    totR = R2.sum()
    cen, info = {}, {}
    idx = 0

    def rng():
        nonlocal idx
        idx += 1
        return np.random.default_rng(SEMENTE + idx)

    for s in (0.01, 0.02, 0.03, 0.036):
        nm = f'F_{int(round(s * 1000)):03d}'
        cen[nm] = rng().binomial(Ri, s).astype(float)
        cen['E' + nm] = s * R2
    for forma, w in (('L', L2), ('T', L2 + R2), ('C', np.nan_to_num(Bz.fL1) * R2)):
        for s in ((0.02, 0.036) if forma != 'C' else (0.036,)):
            k = _resolver_k(R2, w, s * totR)
            esp = np.minimum(R2, k * w)
            p = np.where(R2 > 0, esp / np.maximum(R2, 1), 0.0)
            nm = f'{forma}_{int(round(s * 1000)):03d}'
            cen[nm] = rng().binomial(Ri, np.clip(p, 0, 1)).astype(float)
            cen['E' + nm] = esp
            info[nm] = {'k': k, 'secoes_no_teto': int((k * w >= R2).sum() - (R2 == 0).sum())}
    for s in (0.02, 0.03, 0.036):
        cen[f'M_{int(round(s * 1000)):03d}'] = -rng().binomial(Li, s).astype(float)
    # mais 3% por cima do plantio de 3,6% (para a cláusula B do T7 avaliada nos dados plantados)
    cen['F_036_mais3'] = cen['F_036'] + rng().binomial((Ri - cen['F_036']).astype(np.int64), 0.03)
    for nm, d in cen.items():
        info.setdefault(nm, {})
        info[nm].update({'votos': float(d.sum()), 'pct_de_F2': float(100 * d.sum() / totR)})
    return cen, info


# ============================================================ utilidades de critério
def coefs(Bz, m, cen, lista, sem_grupos=False, influencia=False):
    """Regressão do ganho de Lula no recorte m. Devolve b (coef. de Flávio), pL (próprio de Lula) e, para cada
    cenário da lista, os mesmos coeficientes com o plantio."""
    X = Bz.Xsg if sem_grupos else Bz.X
    iR, iL = (Bz.iRs, Bz.iLs) if sem_grupos else (Bz.iR, Bz.iL)
    try:
        rg = Reg(X[m], Bz.loc[m])
    except Exception as e:  # noqa
        return {'secoes': int(m.sum()), 'erro': str(e)}
    f = rg.fit(Bz.yL[m], influencia)
    out = {'secoes': int(m.sum()), 'n': f['n'], 'locais': f['locais'],
           'b': float(f['b'][iR]), 'ep': float(f['ep'][iR]), 'pL': float(f['b'][iL]), 'ep_pL': float(f['ep'][iL])}
    if influencia:
        out['_fit'] = f
        out['_iR'], out['_iL'] = iR, iL
    pl = {}
    for nm in lista:
        g = rg.fit(Bz.yL[m] + cen[nm][m])
        pl[nm] = {'b': float(g['b'][iR]), 'ep': float(g['ep'][iR]), 'pL': float(g['b'][iL]), 'ep_pL': float(g['ep'][iL])}
    out['plantio'] = pl
    return out


def limpa(o):
    """Tira campos internos (começados por _) antes de gravar."""
    if isinstance(o, dict):
        return {k: limpa(v) for k, v in o.items() if not str(k).startswith('_')}
    if isinstance(o, list):
        return [limpa(v) for v in o]
    return o


def crit_p1(b1, ep1, b10):
    sinal = (b1 >= 0.03) and (b1 / ep1 > 4) and (b1 >= 0.8 * b10)
    sinal_lim = (b1 >= 0.03) and ((b1 - 0.03) / ep1 > 4) and (b1 >= 0.8 * b10)
    sem = (b1 < 0.015) or (b1 < 0.4 * b10)
    v = 'SINAL' if sinal else 'SEM SINAL' if sem else 'INCONCLUSIVO'
    v2 = 'SINAL' if sinal_lim else 'SEM SINAL' if sem else 'INCONCLUSIVO'
    return {'veredito_letra': v, 'veredito_z_do_limiar': v2, 'b_D1': b1, 'ep_D1': ep1, 'b_D10': b10,
            'z_de_zero': b1 / ep1, 'z_do_limiar_0.03': (b1 - 0.03) / ep1, 'razao_D1_D10': (b1 / b10 if b10 else None),
            'cond_b>=0.03': bool(b1 >= 0.03), 'cond_>=80%': bool(b1 >= 0.8 * b10), 'cond_<0.015': bool(b1 < 0.015),
            'cond_<40%': bool(b1 < 0.4 * b10)}


def votos_de_s(s):
    """Troca s (fração dos votos verdadeiros de Flávio) em votos trocados e efeito na margem."""
    if s is None or not np.isfinite(s) or s >= 1:
        return None
    v = s / (1 - s) * F2_OFICIAL
    return {'s_pct': 100 * s, 'votos_trocados': v, 'efeito_na_margem': 2 * v, 'fracao_da_margem': 2 * v / MARGEM,
            'vira_o_resultado': bool(2 * v > MARGEM)}


# ============================================================ Parte 1
def decis(c, cortes):
    return np.searchsorted(cortes, c, side='left')


def parte1(Bz, cen):
    log('Parte 1')
    U = Bz.apt_igual
    cortes = np.quantile(Bz.cap[U], np.arange(0.1, 0.95, 0.1))
    dec = decis(Bz.cap, cortes)
    lista = ['F_020', 'F_036', 'EF_020', 'EF_036', 'M_020', 'M_036', 'L_036', 'T_036', 'C_036']
    res = {'universo': {'secoes_dois_turnos': int(Bz.n), 'aptos_iguais': int(U.sum()), 'exterior_no_universo': int((U & Bz.zz).sum()),
                        'aptos_diferentes': int((~Bz.apt_igual).sum())},
           'cortes_c': cortes.tolist()}

    def bloco(Um, sem_grupos=False, nd=10, cts=None, lst=lista, influencia=True):
        d_ = dec if cts is None else decis(Bz.cap, cts)
        out = []
        for j in range(nd):
            m = Um & (d_ == j)
            r = coefs(Bz, m, cen, lst, sem_grupos, influencia)
            r.update({'decil': j + 1, 'c_min': float(np.nanmin(Bz.cap[m])), 'c_max': float(np.nanmax(Bz.cap[m])),
                      'c_medio': float(np.nanmean(Bz.cap[m])),
                      'R1': int(Bz.R1[m].sum()), 'L1': int(Bz.L1[m].sum()), 'R2': int(Bz.R2[m].sum()), 'L2': int(Bz.L2[m].sum()),
                      'faltosos_1T': int((Bz.apt1[m] - Bz.comp1[m]).sum()), 'fatia_F_1T': float(Bz.R1[m].sum() / max(1, Bz.val1[m].sum()))})
            out.append(r)
        return out

    D = bloco(U)
    res['decis'] = D
    b1, ep1, b10 = D[0]['b'], D[0]['ep'], D[9]['b']
    cr = crit_p1(b1, ep1, b10)
    # erro-padrão das comparações com o D10, com a covariância entre decis
    f1, f10, iR, iL = D[0]['_fit'], D[9]['_fit'], D[0]['_iR'], D[0]['_iL']
    v1, v10, c110 = D[0]['ep'] ** 2, D[9]['ep'] ** 2, cov_cruzada(f1, iR, f10, iR)
    for a in (0.8, 0.4):
        cr[f'b_D1_menos_{a}_b_D10'] = [b1 - a * b10, float(np.sqrt(max(0.0, v1 + a * a * v10 - 2 * a * c110)))]
    cr['correlacao_D1_D10'] = c110 / np.sqrt(v1 * v10)
    res['criterio'] = cr
    # calibração registrada: recuperação a 0,3 ponto em cada decil
    cal = {}
    for nm, s in (('F_020', 0.02), ('F_036', 0.036), ('EF_020', 0.02), ('EF_036', 0.036)):
        rec = [100 * (x['plantio'][nm]['b'] - x['b']) for x in D]
        cal[nm] = {'plantado_pontos': 100 * s, 'recuperado_pontos_por_decil': rec,
                   'aprovado_por_decil': [bool(abs(r - 100 * s) <= 0.3) for r in rec],
                   'aprovado_D1': bool(abs(rec[0] - 100 * s) <= 0.3), 'aprovado_todos': bool(all(abs(r - 100 * s) <= 0.3 for r in rec)),
                   'criterio_com_plantio': crit_p1(D[0]['plantio'][nm]['b'], D[0]['plantio'][nm]['ep'], D[9]['plantio'][nm]['b'])}
    for nm in ('L_036', 'T_036', 'C_036'):
        cal[nm] = {'deslocamento_b_pontos_por_decil': [100 * (x['plantio'][nm]['b'] - x['b']) for x in D],
                   'deslocamento_pL_pontos_por_decil': [100 * (x['plantio'][nm]['pL'] - x['pL']) for x in D],
                   'criterio_com_plantio': crit_p1(D[0]['plantio'][nm]['b'], D[0]['plantio'][nm]['ep'], D[9]['plantio'][nm]['b'])}
    res['calibracao'] = cal
    # espelho: coeficiente dos votos de Lula no 1T na regressão do ganho de Flávio = -pL
    e1, eep1, e10 = -D[0]['pL'], D[0]['ep_pL'], -D[9]['pL']
    esp = {'coef_espelho_por_decil': [[-x['pL'], x['ep_pL']] for x in D], 'criterio': crit_p1(e1, eep1, e10)}
    for nm, s in (('M_020', 0.02), ('M_036', 0.036)):
        rec = [100 * (-(x['plantio'][nm]['pL']) - (-x['pL'])) for x in D]
        esp[nm] = {'plantado_pontos': 100 * s, 'recuperado_pontos_por_decil': rec, 'aprovado_D1': bool(abs(rec[0] - 100 * s) <= 0.3),
                   'criterio_com_plantio': crit_p1(-D[0]['plantio'][nm]['pL'], D[0]['plantio'][nm]['ep_pL'], -D[9]['plantio'][nm]['pL'])}
    res['espelho'] = esp
    # veredito (G6 e P1.4)
    plantado_sinal = cal['F_036']['criterio_com_plantio']['veredito_letra'] == 'SINAL'
    rec_ok = cal['F_020']['aprovado_D1'] and cal['F_036']['aprovado_D1']
    letra = cr['veredito_letra']
    if not rec_ok:
        final, motivo = 'SEM PODER', 'a recuperação do plantio falha no decil de menor capacidade'
    elif letra != 'SINAL' and not plantado_sinal:
        final, motivo = 'SEM PODER', 'o critério não dispara nos dados brutos nem com 3,6% plantados por cima (regra G6)'
    else:
        final, motivo = letra, 'letra do critério; a calibração enxerga o plantio'
    res['veredito'] = {'letra': letra, 'final': final, 'motivo': motivo, 'recuperacao_D1_ok': bool(rec_ok),
                       'recuperacao_todos_os_decis_ok': bool(cal['F_020']['aprovado_todos'] and cal['F_036']['aprovado_todos']),
                       'criterio_dispara_com_2pct': cal['F_020']['criterio_com_plantio']['veredito_letra'],
                       'criterio_dispara_com_3.6pct': cal['F_036']['criterio_com_plantio']['veredito_letra'],
                       'espelho_letra': esp['criterio']['veredito_letra']}
    # ---------------- ao lado
    lado = {}
    lado['sem_grupos'] = [{k: x[k] for k in ('decil', 'n', 'b', 'ep', 'pL', 'ep_pL')} for x in bloco(U, True, lst=[], influencia=False)]
    Dz = bloco(U & ~Bz.zz, lst=['F_036'], influencia=False)
    lado['sem_exterior'] = {'decis': [{k: x[k] for k in ('decil', 'secoes', 'n', 'b', 'ep', 'pL', 'ep_pL')} for x in Dz],
                            'criterio': crit_p1(Dz[0]['b'], Dz[0]['ep'], Dz[9]['b']),
                            'criterio_com_3.6pct': crit_p1(Dz[0]['plantio']['F_036']['b'], Dz[0]['plantio']['F_036']['ep'], Dz[9]['plantio']['F_036']['b'])}
    cq = np.quantile(Bz.cap[U], [0.2, 0.4, 0.6, 0.8])
    lado['quintis_de_c'] = {'cortes': cq.tolist(),
                            'q': [{k: x[k] for k in ('decil', 'secoes', 'n', 'b', 'ep', 'pL', 'ep_pL', 'c_medio')} for x in bloco(U, nd=5, cts=cq, lst=[], influencia=False)]}
    # reta ponderada dos dez coeficientes contra o c médio
    cm = np.array([x['c_medio'] for x in D]); bb = np.array([x['b'] for x in D]); ee = np.array([x['ep'] for x in D])
    lado['reta_b_contra_c'] = _reta(cm, bb, ee)
    lado['reta_espelho_contra_c'] = _reta(cm, np.array([-x['pL'] for x in D]), np.array([x['ep_pL'] for x in D]))
    # todas as seções do universo numa regressão só (nível do universo)
    r = coefs(Bz, U, cen, ['F_036'])
    lado['universo_inteiro'] = {k: r[k] for k in ('secoes', 'n', 'locais', 'b', 'ep', 'pL', 'ep_pL')}
    # empilhada com efeito fixo de local comum
    lado['empilhada_fe_comum'] = _empilhada(Bz, U, dec)
    lado['interacao_continua'] = _interacao(Bz, U)
    res['ao_lado'] = lado
    res['decis'] = limpa(D)
    return res, cortes, dec


def _reta(x, y, ep):
    w = 1 / ep ** 2
    X = np.column_stack([np.ones(len(x)), x])
    XtW = X.T * w
    V = np.linalg.inv(XtW @ X)
    b = V @ (XtW @ y)
    res = y - X @ b
    chi2 = float((w * res ** 2).sum())
    fator = max(1.0, chi2 / (len(x) - 2))        # erro inflado se os pontos fogem da reta
    return {'intercepto_c0': float(b[0]), 'ep_intercepto': float(np.sqrt(V[0, 0])), 'ep_intercepto_inflado': float(np.sqrt(V[0, 0] * fator)),
            'inclinacao': float(b[1]), 'ep_inclinacao': float(np.sqrt(V[1, 1])), 'chi2': chi2, 'gl': len(x) - 2}


def _empilhada(Bz, U, dec):
    X = Bz.X[U]; y = Bz.yL[U]; g = Bz.loc[U]; d = dec[U]
    n, k = X.shape
    XX = np.zeros((n, 10 * k + 9))
    for j in range(10):
        m = d == j
        XX[m, j * k:(j + 1) * k] = X[m]
        if j > 0:
            XX[m, 10 * k + j - 1] = 1.0
    f = Reg(XX, g).fit(y)
    out = {'n': f['n'], 'locais': f['locais'],
           'b_por_decil': [[float(f['b'][j * k + Bz.iR]), float(f['ep'][j * k + Bz.iR])] for j in range(10)],
           'pL_por_decil': [[float(f['b'][j * k + Bz.iL]), float(f['ep'][j * k + Bz.iL])] for j in range(10)]}
    out['criterio'] = crit_p1(out['b_por_decil'][0][0], out['b_por_decil'][0][1], out['b_por_decil'][9][0])
    return out


def _interacao(Bz, U):
    X = Bz.X[U]; y = Bz.yL[U]; g = Bz.loc[U]; c = Bz.cap[U]
    XX = np.column_stack([X, X * c[:, None], c])
    f = Reg(XX, g).fit(y)
    k = X.shape[1]
    return {'n': f['n'], 'locais': f['locais'],
            'b_em_c0': [float(f['b'][Bz.iR]), float(f['ep'][Bz.iR])], 'b_por_unidade_de_c': [float(f['b'][k + Bz.iR]), float(f['ep'][k + Bz.iR])],
            'pL_em_c0': [float(f['b'][Bz.iL]), float(f['ep'][Bz.iL])], 'pL_por_unidade_de_c': [float(f['b'][k + Bz.iL]), float(f['ep'][k + Bz.iL])]}


def parte1_outros_anos(cortes26):
    """Ao lado (G9): perfil por decil em 2014, 2018 e 2022, outros agregados. Não é régua e não entra em veredito."""
    out = {}
    for ano, pt, adv in (('2022', 'Lula', 'Bolsonaro'), ('2018', 'Haddad', 'Bolsonaro'), ('2014', 'Dilma', 'Aécio')):
        log('outros anos', ano)
        d = carregar(f'{RAIZ}/dados/secoes{ano}.json.gz')
        rows, locs = [], []
        for k, v in d.items():
            if '1' not in v or '2' not in v:
                continue
            a, b = v['1'], v['2']
            try:
                rows.append([a['L'], a['R'], a['O'], a['B'], a['N'], a['comp'], a['apt'], b['L'], b['R'], b['B'], b['N'], b['comp'], b['apt'], b.get('O', 0)])
            except (KeyError, TypeError):
                continue
            locs.append(chave_local(k, b))
        del d
        A = np.array(rows, float)
        _, loc = np.unique(np.array(locs), return_inverse=True)
        L1, R1, O1, B1, N1, c1, ap1, L2, R2, B2, N2, c2, ap2, O2 = A.T
        U = (ap1 == ap2) & (ap1 > 0)
        cap = np.where(ap1 > 0, (ap1 - c1) / np.maximum(ap1, 1), np.nan)
        cortes = np.quantile(cap[U], np.arange(0.1, 0.95, 0.1))
        dec = decis(cap, cortes)
        X = np.column_stack([O1, (B1 + N1) - (B2 + N2), c2 - c1, R1, L1])
        yL, yR = L2 - L1, R2 - R1
        linhas = []
        for j in range(10):
            m = U & (dec == j)
            rg = Reg(X[m], loc[m])
            fL, fR = rg.fit(yL[m]), rg.fit(yR[m])
            linhas.append({'decil': j + 1, 'n': fL['n'], 'c_medio': float(cap[m].mean()),
                           'perda_do_adversario_para_o_PT': [float(fL['b'][3]), float(fL['ep'][3])],     # coef. de R1 no ganho do PT
                           'perda_do_PT_para_o_adversario': [float(fR['b'][4]), float(fR['ep'][4])]})    # coef. de L1 no ganho do adversário
        out[ano] = {'PT': pt, 'adversario': adv, 'secoes_universo': int(U.sum()), 'secoes_dois_turnos': int(len(A)),
                    'O2_soma': float(O2.sum()), 'cortes_c': cortes.tolist(), 'decis': linhas,
                    'ganho_PT': float(yL.sum()), 'ganho_adversario': float(yR.sum())}
    return out


# ============================================================ Parte 2
def parte2(Bz, cen):
    log('Parte 2')
    U = (~Bz.zz) & (Bz.val1 > 0)
    cF = np.quantile(Bz.fR1[U], [0.95, 0.99]); cL = np.quantile(Bz.fL1[U], [0.95, 0.99])
    cPL = np.quantile(Bz.fPL[Bz.uni_df], [0.2, 0.4, 0.6, 0.8]); cPT = np.quantile(Bz.fPT[Bz.uni_df], [0.2, 0.4, 0.6, 0.8])
    estr = {'R1': U & (Bz.fR1 > cF[1]), 'R5': U & (Bz.fR1 > cF[0]), 'RPL': Bz.uni_df & (Bz.fPL > cPL[3]),
            'E1': U & (Bz.fL1 > cL[1]), 'E5': U & (Bz.fL1 > cL[0]), 'EPT': Bz.uni_df & (Bz.fPT > cPT[3]), 'PAIS': U}
    lista = ['F_020', 'F_036', 'L_020', 'L_036', 'T_020', 'T_036', 'EF_020', 'EF_036', 'EL_036', 'ET_036', 'M_020', 'M_036', 'C_036']
    res = {'universo_secoes': int(U.sum()), 'universo_deputado_federal': int(Bz.uni_df.sum()),
           'cortes': {'fatia_Flavio_p95_p99': cF.tolist(), 'fatia_Lula_p95_p99': cL.tolist(), 'PL_quintis': cPL.tolist(), 'PT_quintis': cPT.tolist()}}
    E = {}
    for nm, m in estr.items():
        r = coefs(Bz, m, cen, lista)
        r.update({'fatia_F_1T': float(Bz.R1[m].sum() / Bz.val1[m].sum()), 'fatia_L_1T': float(Bz.L1[m].sum() / Bz.val1[m].sum()),
                  'R1': int(Bz.R1[m].sum()), 'L1': int(Bz.L1[m].sum()), 'R2': int(Bz.R2[m].sum()), 'L2': int(Bz.L2[m].sum()),
                  'fatia_F_min': float(np.nanmin(Bz.fR1[m])), 'fatia_L_min': float(np.nanmin(Bz.fL1[m]))})
        E[nm] = r
        log(f'  estrato {nm}: {r.get("secoes")} seções, n {r.get("n")}, b {r.get("b")}, ep {r.get("ep")}')
    res['estratos'] = E
    red, espn = ['R1', 'R5', 'RPL'], ['E1', 'E5', 'EPT']
    par = dict(zip(red, espn))
    # coeficiente espelho (nível natural): votos de Lula 1T no ganho de Flávio = -pL
    nat = {e: -E[e]['pL'] for e in espn}
    nat_ep = {e: E[e]['ep_pL'] for e in espn}
    n_min, n_max = min(nat.values()), max(nat.values())
    nat_plant = {e: -E[e]['plantio']['M_020']['pL'] for e in espn}
    res['espelho'] = {'coef': nat, 'ep': nat_ep, 'menor': n_min, 'maior': n_max, 'com_2pct_plantados_de_L_para_F': nat_plant,
                      'menor_com_2pct_plantados': min(nat_plant.values())}

    def avalia(get):
        """get(estrato) -> (b, ep). Aplica P2.2 e P2.3."""
        linhas = {}
        for k in red:
            b, ep = get(k)
            linhas[k] = {'b': b, 'ep': ep, 'z_de_zero': b / ep, 'z_do_limiar_0.03': (b - 0.03) / ep,
                         'sinal': bool(b >= 0.03 and b / ep > 4), 'sinal_z_do_limiar': bool(b >= 0.03 and (b - 0.03) / ep > 4),
                         'b_mais_2ep': b + 2 * ep,
                         'limite_principal': 0.02 + n_min, 'exclui_principal': bool(b + 2 * ep < 0.02 + n_min),
                         'limite_literal': 0.02 - n_min, 'exclui_literal': bool(b + 2 * ep < 0.02 - n_min),
                         'limite_maior_espelho': 0.02 + n_max, 'exclui_maior_espelho': bool(b + 2 * ep < 0.02 + n_max),
                         'limite_proprio_espelho': 0.02 + nat[par[k]], 'exclui_proprio_espelho': bool(b + 2 * ep < 0.02 + nat[par[k]]),
                         'limite_espelho_plantado': min(nat_plant.values()), 'exclui_espelho_plantado': bool(b + 2 * ep < min(nat_plant.values()))}
        ns = sum(v['sinal'] for v in linhas.values())

        def geral(campo):
            ne = sum(v[campo] for v in linhas.values())
            return 'SINAL' if ns == 3 else 'EXCLUSÃO' if (ne >= 1 and ns == 0) else 'INCONCLUSIVO'
        return {'por_estrato': linhas, 'sinais': ns, 'letra_principal': geral('exclui_principal'), 'letra_literal': geral('exclui_literal'),
                'letra_maior_espelho': geral('exclui_maior_espelho'), 'letra_proprio_espelho': geral('exclui_proprio_espelho'),
                'letra_espelho_plantado': geral('exclui_espelho_plantado')}

    bruto = avalia(lambda k: (E[k]['b'], E[k]['ep']))
    res['forma_F'] = {'bruto': bruto}
    for nm in ('F_020', 'F_036'):
        res['forma_F']['com_' + nm] = avalia(lambda k, nm=nm: (E[k]['plantio'][nm]['b'], E[k]['plantio'][nm]['ep']))
    # poder por estrato (P2.4)
    pod = {}
    for k in red:
        rec2 = 100 * (E[k]['plantio']['F_020']['b'] - E[k]['b']); rec36 = 100 * (E[k]['plantio']['F_036']['b'] - E[k]['b'])
        pod[k] = {'2ep': 2 * E[k]['ep'], 'precisao_ok': bool(2 * E[k]['ep'] < 0.02), 'recuperado_2pct': rec2, 'recuperado_3.6pct': rec36,
                  'recuperacao_ok': bool(abs(rec2 - 2) <= 0.3 and abs(rec36 - 3.6) <= 0.3)}
        pod[k]['com_poder'] = bool(pod[k]['precisao_ok'] and pod[k]['recuperacao_ok'])
    res['forma_F']['poder'] = pod
    letra = bruto['letra_principal']
    com_poder = [k for k in red if pod[k]['com_poder']]
    plantado_sinal = res['forma_F']['com_F_036']['letra_principal'] == 'SINAL'
    if not com_poder:
        final, motivo = 'SEM PODER', 'nenhum estrato de reduto tem precisão e recuperação para o critério'
    elif letra != 'SINAL' and not plantado_sinal:
        final, motivo = 'SEM PODER', 'o critério de sinal não dispara nos dados brutos nem com 3,6% plantados (regra G6)'
    elif letra == 'EXCLUSÃO' and not any(bruto['por_estrato'][k]['exclui_principal'] for k in com_poder):
        final, motivo = 'INCONCLUSIVO', 'a exclusão vem só de estrato sem poder'
    else:
        final, motivo = letra, 'letra do critério, leitura principal da frase de exclusão'
    res['forma_F']['veredito'] = {'letra': letra, 'final': final, 'motivo': motivo, 'estratos_com_poder': com_poder,
                                  'letra_literal': bruto['letra_literal'], 'letra_maior_espelho': bruto['letra_maior_espelho'],
                                  'letra_proprio_espelho': bruto['letra_proprio_espelho'], 'letra_espelho_plantado': bruto['letra_espelho_plantado'],
                                  'com_2pct_plantados': res['forma_F']['com_F_020']['letra_principal'],
                                  'com_3.6pct_plantados': res['forma_F']['com_F_036']['letra_principal']}
    # espelho do teste: os estratos de Lula avaliados com o nível natural = menor coeficiente dos redutos de Flávio
    nF = min(E[k]['b'] for k in red)
    res['espelho_do_teste'] = {e: {'b_espelho': nat[e], 'ep': nat_ep[e], 'sinal': bool(nat[e] >= 0.03 and nat[e] / nat_ep[e] > 4),
                                   'exclui_com_natural_dos_redutos_de_Flavio': bool(nat[e] + 2 * nat_ep[e] < 0.02 + nF)} for e in espn}
    res['espelho_do_teste']['natural_usado'] = nF
    # forma k x L (P2.5)
    def clausula_L(get, quais):
        lin = {k: {'pL': get(k)[0], 'b': get(k)[1], 'abs_pL<0.01': bool(abs(get(k)[0]) < 0.01), 'b>0.04': bool(get(k)[1] > 0.04)} for k in quais}
        return {'por_estrato': lin, 'indicio': bool(all(v['abs_pL<0.01'] and v['b>0.04'] for v in lin.values()))}
    fl = {'bruto_redutos': clausula_L(lambda k: (E[k]['pL'], E[k]['b']), red),
          'bruto_espelhos_ao_lado': clausula_L(lambda k: (E[k]['pL'], E[k]['b']), espn),
          'bruto_pais_ao_lado': clausula_L(lambda k: (E[k]['pL'], E[k]['b']), ['PAIS']),
          'bruto_seis_estratos_ao_lado': clausula_L(lambda k: (E[k]['pL'], E[k]['b']), red + espn)}
    for nm in ('L_020', 'L_036'):
        fl['com_' + nm + '_redutos'] = clausula_L(lambda k, nm=nm: (E[k]['plantio'][nm]['pL'], E[k]['plantio'][nm]['b']), red)
        fl['com_' + nm + '_seis'] = clausula_L(lambda k, nm=nm: (E[k]['plantio'][nm]['pL'], E[k]['plantio'][nm]['b']), red + espn)
    fl['ep_pL'] = {k: E[k]['ep_pL'] for k in red + espn + ['PAIS']}
    ind = fl['bruto_redutos']['indicio']; enx = fl['com_L_036_redutos']['indicio']
    fl['veredito'] = {'letra': 'INDÍCIO' if ind else 'sem indício (o registro não fixa critério de sem sinal)',
                      'final': 'SINAL' if ind else ('INCONCLUSIVO' if enx else 'SEM PODER'),
                      'clausula_dispara_com_forma_L_3.6pct_plantada': bool(enx)}
    res['forma_L'] = fl
    # inclinações e teto por forma (P2.6)
    S = 0.036
    incl = {}
    for forma, nm in (('F', 'EF_036'), ('L', 'EL_036'), ('total', 'ET_036')):
        incl[forma] = {k: {'b': (E[k]['plantio'][nm]['b'] - E[k]['b']) / S, 'pL': (E[k]['plantio'][nm]['pL'] - E[k]['pL']) / S} for k in red + espn + ['PAIS']}
    res['inclinacoes_por_unidade_de_troca'] = incl
    teto = {}
    for forma in ('F', 'L', 'total'):
        t = {}
        for rot, n0 in (('natural_zero', 0.0), ('natural_menor_espelho', n_min)):
            cand_ = {k: (E[k]['b'] + 2 * E[k]['ep'] - n0) / incl[forma][k]['b'] for k in red if incl[forma][k]['b'] >= 0.1}
            ponto = {k: (E[k]['b'] - n0) / incl[forma][k]['b'] for k in red if incl[forma][k]['b'] >= 0.1}
            if cand_:
                kmin = min(cand_, key=cand_.get)
                smax = max(0.0, cand_[kmin])
                t[rot] = {'estrato_que_limita': kmin, 'S_max': smax, 'S_ponto': max(0.0, ponto[kmin]), 'por_estrato': cand_,
                          'votos': votos_de_s(smax), 'votos_no_ponto': votos_de_s(max(0.0, ponto[kmin]))}
            else:
                t[rot] = {'cego': True}
        teto[forma] = t
    res['teto_por_forma'] = teto
    # tradução: assimetria reduto de Flávio menos espelho de Lula, estrato a estrato (premissa: campos iguais onde dominam)
    res['assimetria_reduto_menos_espelho'] = {k: {'b': E[k]['b'], 'espelho': nat[par[k]], 'dif': E[k]['b'] - nat[par[k]],
                                                  'ep': float(np.hypot(E[k]['ep'], nat_ep[par[k]])),
                                                  'votos': votos_de_s(max(0.0, (E[k]['b'] - nat[par[k]]) / (1 - nat[par[k]])))} for k in red}
    return res, estr, cPL, cPT


# ============================================================ Parte 3
def _ep_media_agrupada(z, cl):
    n = len(z)
    if n == 0:
        return float('nan')
    p = z.mean()
    _, g = np.unique(cl, return_inverse=True)
    u = np.bincount(g, weights=z - p)
    G = len(u)
    return float(np.sqrt(G / max(1, G - 1) * (u ** 2).sum()) / n)


def parte3(Bz, cen):
    log('Parte 3')
    n = Bz.n
    bolo_orig = Bz.O1 + np.maximum(0, Bz.queda) + np.maximum(0, Bz.dcomp)
    bolo_max = Bz.O1 + Bz.B1 + Bz.N1 + (Bz.apt1 - Bz.comp1)
    gL = (Bz.L2 - Bz.L1).astype(float); gR = (Bz.R2 - Bz.R1).astype(float)
    faixaF = np.full(n, -1); faixaL = np.full(n, -1)
    for i, (lo, hi) in enumerate(FAIXAS):
        faixaF[(Bz.fR1 >= lo) & (Bz.fR1 < hi)] = i
        faixaL[(Bz.fL1 >= lo) & (Bz.fL1 < hi)] = i

    def est(g, m, com_ep=False):
        gm = g[m]; eo = gm - bolo_orig[m]; em = gm - bolo_max[m]
        nn = int(m.sum())
        if nn == 0:
            return {'secoes': 0}
        r = {'secoes': nn, 'ganho': float(gm.sum()),
             'a_orig': float(100 * (eo > 0).mean()), 'b_orig': float(100 * eo[eo > 0].sum() / gm.sum()) if gm.sum() else None,
             'excesso_orig': float(eo[eo > 0].sum()),
             'a_estrito': float(100 * (em > 0).mean()), 'secoes_estrito': int((em > 0).sum()), 'excesso_estrito': float(em[em > 0].sum())}
        if com_ep:
            r['ep_a_orig'] = 100 * _ep_media_agrupada((eo > 0).astype(float), Bz.loc[m])
            r['ep_a_estrito'] = 100 * _ep_media_agrupada((em > 0).astype(float), Bz.loc[m])
        return r

    todos = np.ones(n, bool)

    def quadro(g, faixa, d=None, com_ep=False, mask=None):
        gg = g if d is None else g + d
        mk = todos if mask is None else mask
        q = {'pais': est(gg, mk, com_ep)}
        for i, nm in enumerate(NOME_FAIXA):
            q[nm] = est(gg, mk & (faixa == i), com_ep)
        return q

    res = {'secoes': int(n), 'bolo_orig_total': int(bolo_orig.sum()), 'bolo_max_total': int(bolo_max.sum()),
           'ganho_Lula': float(gL.sum()), 'ganho_Flavio': float(gR.sum())}
    res['Lula_bruto'] = quadro(gL, faixaF, com_ep=True)
    res['Flavio_bruto_espelho'] = quadro(gR, faixaL, com_ep=True)
    res['Lula_aptos_iguais'] = quadro(gL, faixaF, mask=Bz.apt_igual)
    res['Lula_sem_exterior'] = quadro(gL, faixaF, mask=~Bz.zz)
    # calibração
    cal = {}
    for nm in ('F_010', 'F_020', 'F_030', 'F_036', 'EF_036', 'C_036', 'L_036', 'T_036', 'F_036_mais3'):
        cal[nm] = quadro(gL, faixaF, cen[nm])
    res['calibracao_Lula'] = cal
    cal_e = {}
    for nm in ('M_020', 'M_030', 'M_036'):
        cal_e[nm] = quadro(gR, faixaL, -cen[nm])      # d negativo: votos entram em Flávio
    res['calibracao_espelho_Flavio'] = cal_e
    incl = {}
    for chave in ['pais'] + NOME_FAIXA:
        incl[chave] = {f'a_orig_por_ponto_ate_{t}': (cal[nm][chave]['a_orig'] - res['Lula_bruto'][chave]['a_orig']) / s
                       for nm, s, t in (('F_010', 1.0, '1'), ('F_020', 2.0, '2'), ('F_036', 3.6, '3.6'))}
        incl[chave]['a_estrito_por_ponto_ate_3.6'] = (cal['F_036'][chave]['a_estrito'] - res['Lula_bruto'][chave]['a_estrito']) / 3.6
        incl[chave]['excesso_estrito_por_ponto_ate_3.6'] = (cal['F_036'][chave]['excesso_estrito'] - res['Lula_bruto'][chave]['excesso_estrito']) / 3.6
    res['inclinacao_por_ponto_de_troca'] = incl
    # cláusulas (P3.3 a P3.5)
    def clausulas(q_esq, q_dir3, q_esp, tipo):
        a = 'a_' + tipo
        soma = q_esq['pais']['excesso_estrito']
        A_ = soma > 600000
        B_ = q_esq['0-35'][a] > q_dir3['65-100'][a]
        gradL = q_esq['0-35'][a] - q_esq['65-100'][a]
        gradF = q_esp['0-35'][a] - q_esp['65-100'][a]
        igual = abs(gradL - gradF) <= 2.0
        sem = (soma < 100000) and igual
        return {'soma_excesso_estrito': soma, 'clausula_A_>600mil': bool(A_), 'a_faixa_0-35': q_esq['0-35'][a],
                'a_faixa_65-100_com_3pct': q_dir3['65-100'][a], 'clausula_B': bool(B_), 'gradiente_Lula': gradL, 'gradiente_espelho_Flavio': gradF,
                'gradientes_iguais_ate_2_pontos': bool(igual), 'soma_<100mil': bool(soma < 100000),
                'letra': 'SINAL' if (A_ or B_) else 'SEM SINAL' if sem else 'INCONCLUSIVO', 'indicio_T14_>2.8_milhoes': bool(soma > 2800000)}
    cl = {}
    for tipo in ('orig', 'estrito'):
        cl[tipo] = {'bruto': clausulas(res['Lula_bruto'], cal['F_030'], res['Flavio_bruto_espelho'], tipo),
                    'com_3.6pct_plantados': clausulas(cal['F_036'], cal['F_036_mais3'], res['Flavio_bruto_espelho'], tipo),
                    'com_forma_concentrada_3.6pct': clausulas(cal['C_036'], cal['F_030'], res['Flavio_bruto_espelho'], tipo)}
        # espelho da cláusula B: (a) de Flávio onde Lula < 35% contra (a) de Flávio onde Lula >= 65% com 3% plantados de L para F
        a = 'a_' + tipo
        cl[tipo]['espelho_clausula_B'] = {'a_Flavio_onde_Lula_0-35': res['Flavio_bruto_espelho']['0-35'][a],
                                          'a_Flavio_onde_Lula_65-100_com_3pct': cal_e['M_030']['65-100'][a],
                                          'dispara': bool(res['Flavio_bruto_espelho']['0-35'][a] > cal_e['M_030']['65-100'][a])}
    res['clausulas'] = cl
    pr = cl['orig']
    letra = pr['bruto']['letra']
    enxA = pr['com_3.6pct_plantados']['clausula_A_>600mil']; enxB = pr['com_3.6pct_plantados']['clausula_B']
    if letra != 'SINAL' and not (enxA or enxB):
        final, motivo = 'SEM PODER', 'nenhuma das duas cláusulas de sinal dispara com 3,6% plantados por cima (regra G6)'
    elif letra == 'SINAL':
        veio = [c for c, v in (('A', pr['bruto']['clausula_A_>600mil']), ('B', pr['bruto']['clausula_B'])) if v]
        enx = {'A': enxA, 'B': enxB}
        if not any(enx[c] for c in veio):
            final, motivo = 'SINAL', 'sinal pela letra, vindo só de cláusula (' + ' e '.join(veio) + ') que não dispara com troca uniforme plantada; ver espelho e forma concentrada'
        else:
            final, motivo = 'SINAL', 'sinal pela letra; a cláusula também dispara com o plantio'
    else:
        final, motivo = letra, 'letra do critério; ao menos uma cláusula enxerga o plantio'
    res['veredito'] = {'letra': letra, 'final': final, 'motivo': motivo, 'clausula_A_enxerga_3.6pct': bool(enxA), 'clausula_B_enxerga_3.6pct': bool(enxB),
                       'letra_com_a_estrito_ao_lado': cl['estrito']['bruto']['letra'], 'espelho_clausula_B_dispara': cl['orig']['espelho_clausula_B']['dispara'],
                       'indicio_T14_2.8_milhoes': pr['bruto']['indicio_T14_>2.8_milhoes']}
    # leitura com premissa (P3.8)
    res['troca_equivalente_por_faixa_premissa_espelho'] = {
        nm: {'a_Lula': res['Lula_bruto'][nm]['a_orig'], 'a_espelho_Flavio': res['Flavio_bruto_espelho'][nm]['a_orig'],
             'inclinacao': incl[nm]['a_orig_por_ponto_ate_3.6'],
             'troca_pct': ((res['Lula_bruto'][nm]['a_orig'] - res['Flavio_bruto_espelho'][nm]['a_orig']) / incl[nm]['a_orig_por_ponto_ate_3.6']
                           if incl[nm]['a_orig_por_ponto_ate_3.6'] > 0 else None)} for nm in ['pais'] + NOME_FAIXA}
    # por UF
    por_uf = {}
    for u in sorted(set(Bz.uf.tolist())):
        m = Bz.uf == u
        r0 = est(gL, m); r36 = est(gL + cen['F_036'], m); rF = est(gR, m)
        por_uf[u] = {'secoes': r0['secoes'], 'a_orig': r0['a_orig'], 'excesso_orig': r0['excesso_orig'], 'a_estrito': r0['a_estrito'],
                     'secoes_estrito': r0['secoes_estrito'], 'excesso_estrito': r0['excesso_estrito'],
                     'a_orig_com_3.6pct': r36['a_orig'], 'excesso_estrito_com_3.6pct': r36['excesso_estrito'],
                     'espelho_Flavio_a_orig': rF['a_orig'], 'espelho_Flavio_excesso_estrito': rF['excesso_estrito'],
                     'fatia_F_1T': float(Bz.R1[m].sum() / max(1, Bz.val1[m].sum()))}
    res['por_UF'] = por_uf
    # as seções com excesso estrito (casos individuais)
    em = gL - bolo_max
    idx = np.where(em > 0)[0]
    ordem = idx[np.argsort(-em[idx])]
    res['secoes_com_excesso_estrito'] = {
        'total': int(len(idx)), 'com_aptos_iguais': int((Bz.apt_igual[idx]).sum()),
        'excesso_nas_de_aptos_iguais': float(em[idx][Bz.apt_igual[idx]].sum()),
        'maiores': [{'secao': str(Bz.keys[i]), 'excesso': float(em[i]), 'L1': int(Bz.L1[i]), 'R1': int(Bz.R1[i]), 'L2': int(Bz.L2[i]), 'R2': int(Bz.R2[i]),
                     'apt1': int(Bz.apt1[i]), 'apt2': int(Bz.apt2[i]), 'comp1': int(Bz.comp1[i]), 'comp2': int(Bz.comp2[i])} for i in ordem[:40]]}
    emF = gR - bolo_max
    res['secoes_com_excesso_estrito']['espelho_Flavio_total'] = int((emF > 0).sum())
    res['secoes_com_excesso_estrito']['espelho_Flavio_com_aptos_iguais'] = int(((emF > 0) & Bz.apt_igual).sum())
    res['secoes_com_excesso_estrito']['espelho_Flavio_excesso_nas_de_aptos_iguais'] = float(emF[(emF > 0) & Bz.apt_igual].sum())
    return res


# ============================================================ Parte 4
def crit_p4(p, ep):
    ind = (p <= -0.025) and (p / ep < -4)
    ind_lim = (p <= -0.025) and ((p + 0.025) / ep < -4)
    sem = p > -0.010
    return {'P': p, 'ep': ep, 'z_de_zero': p / ep, 'z_do_limiar_-0.025': (p + 0.025) / ep,
            'letra': 'INDÍCIO' if ind else 'SEM SINAL' if sem else 'INCONCLUSIVO',
            'letra_z_do_limiar': 'INDÍCIO' if ind_lim else 'SEM SINAL' if sem else 'INCONCLUSIVO'}


def parte4(Bz, cen, cortes, dec, cPL, cPT):
    log('Parte 4')
    QPL = Bz.uni_df & (Bz.fPL > cPL[3]); QPT = Bz.uni_df & (Bz.fPT > cPT[3])
    U = Bz.apt_igual
    lista = ['F_020', 'F_036', 'M_020', 'M_036', 'C_036']
    res = {'quintil_PL_secoes': int(QPL.sum()), 'quintil_PL_aptos_iguais': int((QPL & U).sum()),
           'quintil_PT_secoes': int(QPT.sum()), 'quintil_PT_aptos_iguais': int((QPT & U).sum()), 'corte_PL_p80': float(cPL[3]), 'corte_PT_p80': float(cPT[3])}

    def celulas(Q, d_, nd=10):
        out = []
        for j in range(nd):
            m = Q & U & (d_ == j)
            r = coefs(Bz, m, cen, lista) if m.sum() >= 50 else {'secoes': int(m.sum()), 'erro': 'menos de 50 seções'}
            r['decil'] = j + 1
            if m.sum():
                r.update({'c_medio': float(Bz.cap[m].mean()), 'fatia_F_1T': float(Bz.R1[m].sum() / max(1, Bz.val1[m].sum())),
                          'fatia_L_1T': float(Bz.L1[m].sum() / max(1, Bz.val1[m].sum())), 'R1': int(Bz.R1[m].sum()), 'L1': int(Bz.L1[m].sum())})
            out.append(r)
        return out

    PL = celulas(QPL, dec); PT = celulas(QPT, dec)
    res['PL_por_decil'] = PL; res['PT_por_decil'] = PT
    c1 = PL[0]
    if 'b' not in c1:
        res['veredito'] = {'letra': 'não calculável', 'final': 'SEM PODER', 'motivo': 'célula D1 sem seções informativas'}
        return res
    cr = crit_p4(-c1['b'], c1['ep'])
    res['criterio'] = cr
    cal = {}
    for nm, s in (('F_020', 2.0), ('F_036', 3.6)):
        rec = 100 * (c1['plantio'][nm]['b'] - c1['b'])
        cal[nm] = {'plantado_pontos': s, 'recuperado_pontos': rec, 'aprovado': bool(abs(rec - s) <= 0.3),
                   'criterio_com_plantio': crit_p4(-c1['plantio'][nm]['b'], c1['plantio'][nm]['ep'])}
    cal['C_036'] = {'deslocamento_pontos': 100 * (c1['plantio']['C_036']['b'] - c1['b']), 'criterio_com_plantio': crit_p4(-c1['plantio']['C_036']['b'], c1['plantio']['C_036']['ep'])}
    res['calibracao'] = cal
    e1 = PT[0]
    if 'pL' in e1:
        res['espelho'] = {'criterio': crit_p4(e1['pL'], e1['ep_pL']),
                          'M_036': {'recuperado_pontos': 100 * (e1['pL'] - e1['plantio']['M_036']['pL']),
                                    'criterio_com_plantio': crit_p4(e1['plantio']['M_036']['pL'], e1['plantio']['M_036']['ep_pL'])}}
    rec_ok = cal['F_020']['aprovado'] and cal['F_036']['aprovado']
    letra = cr['letra']
    plantado = cal['F_036']['criterio_com_plantio']['letra'] == 'INDÍCIO'
    if not rec_ok:
        final, motivo = 'SEM PODER', 'a recuperação do plantio falha na célula que decide'
    elif letra != 'INDÍCIO' and not plantado:
        final, motivo = 'SEM PODER', 'o critério não dispara nos dados brutos nem com 3,6% plantados (regra G6)'
    else:
        final, motivo = ('SINAL' if letra == 'INDÍCIO' else letra), 'letra do critério; a calibração enxerga o plantio'
    res['veredito'] = {'letra': letra, 'final': final, 'motivo': motivo, 'com_2pct': cal['F_020']['criterio_com_plantio']['letra'],
                       'com_3.6pct': cal['F_036']['criterio_com_plantio']['letra'],
                       'espelho_letra': res.get('espelho', {}).get('criterio', {}).get('letra')}
    # ao lado: decis recalculados dentro do quintil; quintil inteiro (com e sem o filtro de aptos); quintis de capacidade
    lado = {}
    cq = np.quantile(Bz.cap[QPL & U], np.arange(0.1, 0.95, 0.1))
    dl = decis(Bz.cap, cq)
    lado['decis_dentro_do_quintil_PL'] = {'cortes': cq.tolist(), 'celulas': [{k: x.get(k) for k in ('decil', 'secoes', 'n', 'b', 'ep', 'c_medio')} for x in celulas(QPL, dl)]}
    cq2 = np.quantile(Bz.cap[QPT & U], np.arange(0.1, 0.95, 0.1))
    lado['decis_dentro_do_quintil_PT'] = {'cortes': cq2.tolist(), 'celulas': [{k: x.get(k) for k in ('decil', 'secoes', 'n', 'pL', 'ep_pL', 'c_medio')} for x in celulas(QPT, decis(Bz.cap, cq2))]}
    for nm, m in (('quintil_PL_inteiro', QPL), ('quintil_PL_aptos_iguais', QPL & U), ('quintil_PT_inteiro', QPT), ('quintil_PT_aptos_iguais', QPT & U)):
        r = coefs(Bz, m, cen, [])
        lado[nm] = {k: r[k] for k in ('secoes', 'n', 'locais', 'b', 'ep', 'pL', 'ep_pL')}
    # P1 (quintil de menor fatia do PL), para conferir com o L3 publicado
    r = coefs(Bz, Bz.uni_df & (Bz.fPL <= cPL[0]), cen, [])
    lado['quintil_PL_mais_fraco_inteiro'] = {k: r[k] for k in ('secoes', 'n', 'locais', 'b', 'ep')}
    c5 = np.quantile(Bz.cap[U], [0.2, 0.4, 0.6, 0.8])
    lado['PL_por_quintil_de_capacidade'] = [{k: x.get(k) for k in ('decil', 'secoes', 'n', 'b', 'ep', 'c_medio')} for x in celulas(QPL, decis(Bz.cap, c5), 5)]
    xs = [x for x in PL if 'b' in x]
    if len(xs) >= 3:
        lado['reta_P5_contra_c'] = _reta(np.array([x['c_medio'] for x in xs]), np.array([-x['b'] for x in xs]), np.array([x['ep'] for x in xs]))
    res['ao_lado'] = lado
    return res


# ============================================================ EXPLORATÓRIO (feito depois de ver os resultados acima)
def exploratorio_transferencia(Bz, cen, dec, estr):
    """EXPLORATÓRIO. O coeficiente do T8 condiciona na variação do comparecimento e na queda do branco+nulo, então
    mistura o eleitor de Flávio que foi para Lula com o que não voltou. Aqui a matriz de transferência sem esses
    controles (como o desenho D4-1 do A2, mas sem peso e com erro por local): L2, R2, branco+nulo do 2º turno e
    faltosos do 2º turno contra L1, R1, eliminados, B1, N1 e faltosos do 1º turno, por decil de capacidade."""
    U = Bz.apt_igual
    G = np.column_stack([Bz.g70, Bz.g14, Bz.g55, Bz.g30])
    A1 = Bz.apt1 - Bz.comp1; A2 = Bz.apt2 - Bz.comp2
    X = np.column_stack([G, Bz.O1 - G.sum(1), Bz.B1, Bz.N1, A1, Bz.R1, Bz.L1]).astype(float)
    iR, iL = 8, 9
    L2, R2, BN2, A2 = Bz.L2.astype(float), Bz.R2.astype(float), (Bz.B2 + Bz.N2).astype(float), A2.astype(float)

    def um(m):
        rg = Reg(X[m], Bz.loc[m])
        fL, fR, fB, fA = rg.fit(L2[m]), rg.fit(R2[m]), rg.fit(BN2[m]), rg.fit(A2[m])
        fP = rg.fit(L2[m] + cen['F_036'][m]); fP2 = rg.fit(L2[m] + cen['F_020'][m]); fM = rg.fit(R2[m] - cen['M_036'][m])
        return {'secoes': int(m.sum()), 'n': fL['n'], 'locais': fL['locais'],
                'V_R1_em_L2': [float(fL['b'][iR]), float(fL['ep'][iR])], 'M_L1_em_R2': [float(fR['b'][iL]), float(fR['ep'][iL])],
                'R1_em_R2': [float(fR['b'][iR]), float(fR['ep'][iR])], 'L1_em_L2': [float(fL['b'][iL]), float(fL['ep'][iL])],
                'R1_em_faltosos_2T': [float(fA['b'][iR]), float(fA['ep'][iR])], 'L1_em_faltosos_2T': [float(fA['b'][iL]), float(fA['ep'][iL])],
                'R1_em_BN_2T': [float(fB['b'][iR]), float(fB['ep'][iR])], 'L1_em_BN_2T': [float(fB['b'][iL]), float(fB['ep'][iL])],
                'faltosos1T_em_L2': [float(fL['b'][7]), float(fL['ep'][7])], 'faltosos1T_em_R2': [float(fR['b'][7]), float(fR['ep'][7])],
                'V_com_2pct': float(fP2['b'][iR]), 'V_com_3.6pct': float(fP['b'][iR]), 'ep_V_com_3.6pct': float(fP['ep'][iR]),
                'M_com_3.6pct_espelho': float(fM['b'][iL])}
    out = {'universo_aptos_iguais': um(U), 'decis': []}
    for j in range(10):
        r = um(U & (dec == j)); r['decil'] = j + 1
        out['decis'].append(r)
    D = out['decis']
    out['criterio_P1_com_V'] = crit_p1(D[0]['V_R1_em_L2'][0], D[0]['V_R1_em_L2'][1], D[9]['V_R1_em_L2'][0])
    out['criterio_P1_com_V_espelho_M'] = crit_p1(D[0]['M_L1_em_R2'][0], D[0]['M_L1_em_R2'][1], D[9]['M_L1_em_R2'][0])
    out['criterio_P1_com_V_e_3.6pct_plantados'] = crit_p1(D[0]['V_com_3.6pct'], D[0]['ep_V_com_3.6pct'], D[9]['V_com_3.6pct'])
    out['recuperacao_V_D1_pontos'] = {'2pct': 100 * (D[0]['V_com_2pct'] - D[0]['V_R1_em_L2'][0]), '3.6pct': 100 * (D[0]['V_com_3.6pct'] - D[0]['V_R1_em_L2'][0])}
    out['estratos_parte2_aptos_iguais'] = {k: um(m & U) for k, m in estr.items() if k != 'PAIS'}
    # conferência da decomposição: b do T8 ~ V + coef(dcomp) x (R1 -> faltosos) + coef(queda) x (R1 -> branco e nulo)
    f = Reg(Bz.X[U], Bz.loc[U]).fit(Bz.yL[U])
    u = out['universo_aptos_iguais']
    out['decomposicao_do_b_do_T8'] = {'b_T8': float(f['b'][Bz.iR]), 'coef_dcomp': float(f['b'][6]), 'coef_queda_bn': float(f['b'][5]),
                                      'V': u['V_R1_em_L2'][0], 'parcela_faltosos': float(f['b'][6]) * u['R1_em_faltosos_2T'][0],
                                      'parcela_branco_nulo': float(f['b'][5]) * u['R1_em_BN_2T'][0]}
    out['decomposicao_do_b_do_T8']['soma'] = (out['decomposicao_do_b_do_T8']['V'] + out['decomposicao_do_b_do_T8']['parcela_faltosos']
                                              + out['decomposicao_do_b_do_T8']['parcela_branco_nulo'])
    return out


def exploratorio_d1_por_faixa(Bz, cen, dec):
    """EXPLORATÓRIO. O decil de menor capacidade aberto pela fatia de Flávio no 1º turno da seção (as faixas do T7),
    para ver se o coeficiente do D1 é parecido em todo lugar ou vem de onde Lula é forte. Mesmo para o universo."""
    U = Bz.apt_igual
    out = {'D1': {}, 'universo': {}, 'D10_so_exterior': None, 'D10_sem_exterior': None}
    for i, (lo, hi) in enumerate(FAIXAS):
        fx = (Bz.fR1 >= lo) & (Bz.fR1 < hi)
        for rot, m in (('D1', U & (dec == 0) & fx), ('universo', U & fx)):
            r = coefs(Bz, m, cen, ['F_036'])
            out[rot][NOME_FAIXA[i]] = {k: r.get(k) for k in ('secoes', 'n', 'locais', 'b', 'ep', 'pL', 'ep_pL')}
            out[rot][NOME_FAIXA[i]].update({'R1': int(Bz.R1[m].sum()), 'L1': int(Bz.L1[m].sum())})
    for rot, m in (('D10_so_exterior', U & (dec == 9) & Bz.zz), ('D10_sem_exterior', U & (dec == 9) & ~Bz.zz)):
        r = coefs(Bz, m, cen, [])
        out[rot] = {k: r.get(k) for k in ('secoes', 'n', 'locais', 'b', 'ep', 'pL', 'ep_pL', 'erro')}
    return out


def exploratorio_ruido_do_sorteio(Bz, cortes, dec, cPL, nrep=200):
    """EXPLORATÓRIO. Quanto o sorteio binomial do plantio mexe (a) na cláusula B do T7 e (b) na recuperação exigida
    nas células que decidem as Partes 1 e 4. Mais a versão pelo valor esperado (prevista no G5)."""
    out = {}
    # (a) cláusula B do T7
    bolo = Bz.O1 + np.maximum(0, Bz.queda) + np.maximum(0, Bz.dcomp)
    e0 = (Bz.L2 - Bz.L1 - bolo).astype(float)
    m65 = (Bz.fR1 >= 0.65) & (Bz.fR1 < 1.01); m35 = (Bz.fR1 >= 0.0) & (Bz.fR1 < 0.35)
    a35 = 100 * (e0[m35] > 0).mean()
    R65 = Bz.R2[m65]
    vals = []
    for i in range(nrep):
        d = np.random.default_rng(SEMENTE + 1000 + i).binomial(R65, 0.03)
        vals.append(100 * ((e0[m65] + d) > 0).mean())
    vals = np.array(vals)
    grade = {}
    for s in (0.025, 0.028, 0.029, 0.030, 0.031, 0.032, 0.035):
        grade[f'{100 * s:.1f}'] = {'valor_esperado': float(100 * ((e0[m65] + s * R65) > 0).mean()),
                                   'binomial_media_20': float(np.mean([100 * ((e0[m65] + np.random.default_rng(SEMENTE + 5000 + int(1e4 * s) + i).binomial(R65, s)) > 0).mean() for i in range(20)]))}
    out['clausula_B_T7'] = {'a_faixa_0-35': float(a35), 'a_65-100_com_3pct_binomial': {'media': float(vals.mean()), 'dp': float(vals.std(ddof=1)), 'min': float(vals.min()), 'max': float(vals.max()),
                                                                                       'fracao_dos_sorteios_em_que_B_dispara': float((a35 > vals).mean()), 'sorteios': nrep},
                            'a_65-100_com_3pct_valor_esperado': float(100 * ((e0[m65] + 0.03 * R65) > 0).mean()),
                            'B_dispara_com_valor_esperado': bool(a35 > 100 * ((e0[m65] + 0.03 * R65) > 0).mean()),
                            'a_65-100_por_tamanho_de_troca': grade}
    # (b) recuperação nas células
    U = Bz.apt_igual
    QPL = Bz.uni_df & (Bz.fPL > cPL[3])
    for rot, m in (('parte1_D1', U & (dec == 0)), ('parte4_PL_D1', QPL & U & (dec == 0))):
        rg = Reg(Bz.X[m], Bz.loc[m]); b0 = rg.fit(Bz.yL[m])['b'][Bz.iR]
        o = {}
        for s in (0.02, 0.036):
            rec = np.array([100 * (rg.fit(Bz.yL[m] + np.random.default_rng(SEMENTE + 2000 + i).binomial(Bz.R2[m], s))['b'][Bz.iR] - b0) for i in range(nrep)])
            o[f'{100 * s:.1f}'] = {'media': float(rec.mean()), 'dp': float(rec.std(ddof=1)), 'fracao_a_0.3_ponto': float((abs(rec - 100 * s) <= 0.3).mean()),
                                   'valor_esperado': float(100 * (rg.fit(Bz.yL[m] + s * Bz.R2[m])['b'][Bz.iR] - b0))}
        out['recuperacao_' + rot] = o
    return out


def exploratorio_transferencia_outros_anos():
    """EXPLORATÓRIO, não é régua. A mesma matriz de transferência (outros agregados) em 2014, 2018 e 2022, no
    universo de aptos iguais e no decil de menor capacidade, para saber se "quem não voltou" também foi
    assimétrico nesses anos. O valor bruto de 2026 sai ao lado no texto."""
    out = {}
    for ano in ('2022', '2018', '2014'):
        d = carregar(f'{RAIZ}/dados/secoes{ano}.json.gz')
        rows, locs = [], []
        for k, v in d.items():
            if '1' not in v or '2' not in v:
                continue
            a, b = v['1'], v['2']
            try:
                rows.append([a['L'], a['R'], a['O'], a['B'], a['N'], a['comp'], a['apt'], b['L'], b['R'], b['B'], b['N'], b['comp'], b['apt']])
            except (KeyError, TypeError):
                continue
            locs.append(chave_local(k, b))
        del d
        A = np.array(rows, float)
        _, loc = np.unique(np.array(locs), return_inverse=True)
        L1, R1, O1, B1, N1, c1, ap1, L2, R2, B2, N2, c2, ap2 = A.T
        U = (ap1 == ap2) & (ap1 > 0)
        cap = np.where(ap1 > 0, (ap1 - c1) / np.maximum(ap1, 1), np.nan)
        dec = decis(cap, np.quantile(cap[U], np.arange(0.1, 0.95, 0.1)))
        X = np.column_stack([O1, B1, N1, ap1 - c1, R1, L1])
        o = {}
        for rot, m in (('universo_aptos_iguais', U), ('D1', U & (dec == 0)), ('D10', U & (dec == 9))):
            rg = Reg(X[m], loc[m])
            fL, fR, fA = rg.fit(L2[m]), rg.fit(R2[m]), rg.fit((ap2 - c2)[m])
            o[rot] = {'n': fL['n'], 'adversario_em_PT': [float(fL['b'][4]), float(fL['ep'][4])], 'PT_em_adversario': [float(fR['b'][5]), float(fR['ep'][5])],
                      'adversario_em_faltosos_2T': [float(fA['b'][4]), float(fA['ep'][4])], 'PT_em_faltosos_2T': [float(fA['b'][5]), float(fA['ep'][5])]}
        out[ano] = o
    return out


def exploratorio_criterio_outros_anos(p1):
    """EXPLORATÓRIO. A letra da P1.3 aplicada, só de conta, ao perfil por decil dos outros anos (não é régua)."""
    out = {}
    for ano, o in p1['ao_lado']['outros_anos_nao_e_regua'].items():
        D = o['decis']
        out[ano] = {'adversario_para_PT': crit_p1(D[0]['perda_do_adversario_para_o_PT'][0], D[0]['perda_do_adversario_para_o_PT'][1], D[9]['perda_do_adversario_para_o_PT'][0]),
                    'PT_para_adversario': crit_p1(D[0]['perda_do_PT_para_o_adversario'][0], D[0]['perda_do_PT_para_o_adversario'][1], D[9]['perda_do_PT_para_o_adversario'][0])}
    sg = p1['ao_lado']['sem_grupos']
    out['2026_outros_agregados'] = {'Flavio_para_Lula': crit_p1(sg[0]['b'], sg[0]['ep'], sg[9]['b']),
                                    'Lula_para_Flavio': crit_p1(-sg[0]['pL'], sg[0]['ep_pL'], -sg[9]['pL'])}
    return out


def traducao_em_votos(res):
    """G10: leituras em votos de margem, cada uma com a sua premissa."""
    p1, p2, p3, p4 = res['parte1_T14_por_capacidade'], res['parte2_T16_redutos'], res['parte3_T7_estrito'], res['parte4_L3_por_capacidade']
    D = p1['decis']
    b1, e1 = D[0]['b'], -D[0]['pL']
    ep_dif = float(np.hypot(D[0]['ep'], D[0]['ep_pL']))
    s_esp = (b1 - e1) / (1 - e1)
    t = {'vira_com': {'votos_trocados': MARGEM / 2, 's_pct': 100 * (MARGEM / 2) / (F2_OFICIAL + MARGEM / 2)},
         'parte1_D1_nivel_natural_zero': votos_de_s(b1),
         'parte1_D1_nivel_natural_espelho': votos_de_s(s_esp),
         'parte1_D1_espelho_ic95': [votos_de_s(max(0.0, (b1 - e1 - 1.96 * ep_dif) / (1 - e1))), votos_de_s((b1 - e1 + 1.96 * ep_dif) / (1 - e1))],
         'parte2_teto_forma_F': p2['teto_por_forma']['F'], 'parte2_teto_forma_total': p2['teto_por_forma']['total'],
         'parte2_assimetria_redutos': p2['assimetria_reduto_menos_espelho'],
         'parte3_excesso_estrito': {'votos': p3['Lula_bruto']['pais']['excesso_estrito'], 'efeito_na_margem': 2 * p3['Lula_bruto']['pais']['excesso_estrito'],
                                    'fracao_da_margem': 2 * p3['Lula_bruto']['pais']['excesso_estrito'] / MARGEM},
         'parte3_excesso_bolo_original': {'votos': p3['Lula_bruto']['pais']['excesso_orig'], 'efeito_na_margem': 2 * p3['Lula_bruto']['pais']['excesso_orig'],
                                          'fracao_da_margem': 2 * p3['Lula_bruto']['pais']['excesso_orig'] / MARGEM}}
    if 'criterio' in p4:
        P = p4['criterio']['P']; pe = p4.get('espelho', {}).get('criterio', {}).get('P')
        t['parte4_PL_D1_nivel_natural_zero'] = votos_de_s(max(0.0, -P))
        if pe is not None:
            t['parte4_PL_D1_nivel_natural_espelho'] = votos_de_s(max(0.0, (-P - (-pe)) / (1 - (-pe))))
    if 'exploratorio' in res and 'transferencia' in res['exploratorio']:
        x = res['exploratorio']['transferencia']
        V1, M1 = x['decis'][0]['V_R1_em_L2'][0], x['decis'][0]['M_L1_em_R2'][0]
        Vu, Mu = x['universo_aptos_iguais']['V_R1_em_L2'][0], x['universo_aptos_iguais']['M_L1_em_R2'][0]
        t['exploratorio_transferencia_D1_zero'] = votos_de_s(max(0.0, V1))
        t['exploratorio_transferencia_D1_espelho'] = votos_de_s(max(0.0, (V1 - M1) / (1 - M1)))
        t['exploratorio_transferencia_universo_zero'] = votos_de_s(max(0.0, Vu))
        t['exploratorio_transferencia_universo_espelho'] = votos_de_s(max(0.0, (Vu - Mu) / (1 - Mu)))
    return t



# ============================================================ texto (só lê o resultado; não faz conta nova com votos)
def n_(x, d=4, sinal=True):
    if x is None:
        return 'n/d'
    t = f'{x:+.{d}f}' if sinal else f'{x:.{d}f}'
    return t.replace('.', ',')


def i_(x):
    return f'{int(round(x)):,}'.replace(',', '.')


def be(v, d=4):
    return f'{n_(v[0], d)} (ep {n_(v[1], d, False)})'


DESVIOS = [
    'Os quatro retestes vêm da equipe vermelha, que já conhecia os resultados antigos; o critério é novo, a escolha do que retestar é posterior ao dado (aviso do Adendo 27).',
    'Decisões que o registro não fixa: G1 a G11, P1.1 a P1.7, P2.1 a P2.6, P3.1 a P3.8 e P4.1 a P4.4 do docstring, escritas antes de qualquer conta com votos (cópia datada e SHA-256 em /home/user/trabalho-eleicao/adendo27/R27_A3/docstring_antes_de_rodar.txt).',
    'Parte 2: a frase de exclusão do registro ("abaixo de 0,02 menos o menor coeficiente natural plantado") foi lida como b + 2 ep < 0,02 + menor espelho; a aritmética literal (0,02 menos o espelho) sai ao lado e daria INCONCLUSIVO.',
    'Parte 3: "(a)" da segunda cláusula foi lido como a estatística do T7 com o bolo do Adendo 3; com o bolo máximo (estrito) a letra daria SEM SINAL, mas esse lado não enxerga nenhum plantio.',
    'Plantio principal por sorteio binomial (fixado antes). Na cláusula B do T7 isso decide o resultado: com o plantio pelo valor esperado a cláusula não dispara.',
    'Parte 1: universo com o exterior, como o T14 original (fixado antes). Sem as 990 seções do exterior que caem no decil de maior capacidade, a razão D1/D10 cai para 0,798 e a letra daria INCONCLUSIVO.',
    'Parte 1: a recuperação de 0,3 ponto falha em um decil (D3, com 3,6% por sorteio: 3,25); no D1, que decide, passa. Pela regra P1.4 isso não muda o veredito.',
    'Regra do SEM PODER (G6) e regras de combinação entre estratos (P2.2, P2.3) são desta peça, não do registro.',
    'Bloco exploratório (feito depois de ver os resultados): matriz de transferência por decil e por estrato; D1 por faixa; ruído do sorteio; a letra da P1.3 aplicada a 2014, 2018 e 2022; matriz de transferência nesses anos. Nada disso entra em veredito.',
    'Outros anos aparecem só ao lado e só na Parte 1; nenhum veredito depende deles.',
]


def montar_vereditos(res):
    p1, p2, p3, p4 = res['parte1_T14_por_capacidade'], res['parte2_T16_redutos'], res['parte3_T7_estrito'], res['parte4_L3_por_capacidade']
    x = res['exploratorio']
    D = p1['decis']
    v = {
        'parte1_T14_por_capacidade': {'letra': p1['veredito']['letra'], 'final': p1['veredito']['final'],
                                      'ressalvas': ['sem o exterior: ' + p1['ao_lado']['sem_exterior']['criterio']['veredito_letra'],
                                                    'exploratório, matriz de transferência: ' + x['transferencia']['criterio_P1_com_V']['veredito_letra'],
                                                    'espelho (Lula perdendo para Flávio): ' + p1['veredito']['espelho_letra']]},
        'parte2_T16_forma_F': {'letra': p2['forma_F']['veredito']['letra'], 'final': 'SEM SINAL (EXCLUSÃO de troca s x F de 2% ou mais)' if p2['forma_F']['veredito']['final'] == 'EXCLUSÃO' else p2['forma_F']['veredito']['final'],
                               'leitura_literal_ao_lado': p2['forma_F']['veredito']['letra_literal']},
        'parte2_T16_forma_L': {'letra': p2['forma_L']['veredito']['letra'], 'final': p2['forma_L']['veredito']['final']},
        'parte2_T16_forma_total': {'letra': 'o registro não fixa critério próprio; sai o teto', 'final': 'teto de ' + n_(100 * p2['teto_por_forma']['total']['natural_zero']['S_max'], 2, False) + '% dos votos de Flávio (nível natural zero)'},
        'parte3_T7_estrito': {'letra': p3['veredito']['letra'], 'final': p3['veredito']['final'], 'motivo': p3['veredito']['motivo'],
                              'limite_aritmetico': 'SEM PODER: soma de ' + i_(p3['Lula_bruto']['pais']['excesso_estrito']) + ' votos; com 3,6% plantados, ' + i_(p3['calibracao_Lula']['F_036']['pais']['excesso_estrito']),
                              'clausula_B_com_plantio_pelo_valor_esperado': 'dispara' if x['ruido_do_sorteio']['clausula_B_T7']['B_dispara_com_valor_esperado'] else 'não dispara'},
        'parte4_L3_por_capacidade': {'letra': p4['veredito']['letra'], 'final': p4['veredito']['final'], 'motivo': p4['veredito']['motivo']},
        'clausulas_aplicadas': 7,
        'clausulas_que_dispararam': ['P1.3 (Parte 1)', 'cláusula B do T7 (Parte 3)'],
    }
    v['resumo_em_uma_frase'] = (
        'Pela letra há dois sinais (Parte 1 e cláusula B do T7), mas nenhum dos dois marca troca de voto: pela decomposição exploratória, o da Parte 1 vem do eleitor de Flávio que não voltou '
        '(no decil de menor capacidade, a parcela dos votos de Flávio que aparece em Lula é ' + n_(100 * x['transferencia']['decis'][0]['V_R1_em_L2'][0], 2, False) +
        '%, igual ao espelho de ' + n_(100 * x['transferencia']['decis'][0]['M_L1_em_R2'][0], 2, False) + '%), o do T7 passa por 0,45 ponto e some com o plantio pelo valor esperado; '
        'nos redutos de Flávio, troca uniforme de 2% ou mais dos votos dele fica excluída; o limite aritmético estrito e a forma k x L ficam SEM PODER.')
    return v


def escrever_txt(res):
    p1, p2, p3, p4 = res['parte1_T14_por_capacidade'], res['parte2_T16_redutos'], res['parte3_T7_estrito'], res['parte4_L3_por_capacidade']
    x, tv, cf, V = res['exploratorio'], res['traducao_em_votos'], res['conferencias'], res['vereditos']
    L = []
    P = L.append
    P('R27_A3: TROCA PROPORCIONAL COM RÉGUA INTERNA (Adendo 27, Onda A, item A3)')
    P('Quatro retestes da equipe vermelha: T14 por capacidade de troca de eleitores, T16 por reduto, T7 estrito e L3 por capacidade.')
    P('Critérios: registro/adendo27/equipe_vermelha_relatorio.json (commit 2748895, 10/11/2026 00:16:42 UTC), aplicados pela letra.')
    P('Decisões que o registro não fixa: docstring de scripts/analisar_R27_A3.py, escrito antes das contas (SHA-256 ' + res['sha256_docstring'][:16] + '...).')
    P('Aviso do registro: estes retestes foram escritos por quem já conhecia os resultados antigos; o critério é novo, a escolha do que retestar não.')
    P('Só dados de 2026 decidem. Outros anos aparecem ao lado, com o valor de 2026 na mesma linha, e não são régua.')
    P('')
    P('VEREDITOS PELA LETRA')
    c = p1['criterio']
    P(f'  Parte 1 (T14 por capacidade): {V["parte1_T14_por_capacidade"]["letra"]}. Coeficiente de Flávio no decil de menor capacidade {be([c["b_D1"], c["ep_D1"]])}, '
      f'{n_(c["z_de_zero"], 1, False)} ep de zero; no decil de maior capacidade {n_(c["b_D10"])}; razão {n_(c["razao_D1_D10"], 3, False)}.')
    P(f'    Ressalvas que mudam a leitura: sem o exterior a letra dá {p1["ao_lado"]["sem_exterior"]["criterio"]["veredito_letra"]} (razão {n_(p1["ao_lado"]["sem_exterior"]["criterio"]["razao_D1_D10"], 3, False)}); '
      f'o espelho dá {p1["veredito"]["espelho_letra"]}; a decomposição exploratória (item 1.5) mostra que o coeficiente do D1 é eleitor de Flávio que não voltou, não voto que foi para Lula.')
    f = p2['forma_F']
    P(f'  Parte 2 (T16 por reduto), forma s x F: {f["veredito"]["letra"]} de troca uniforme de 2% ou mais, isto é, SEM SINAL para essa forma. '
      f'Coeficiente no 1% de maior fatia de Flávio {be([p2["estratos"]["R1"]["b"], p2["estratos"]["R1"]["ep"]])}; nos 5%, {be([p2["estratos"]["R5"]["b"], p2["estratos"]["R5"]["ep"]])}; '
      f'no quintil do PL, {be([p2["estratos"]["RPL"]["b"], p2["estratos"]["RPL"]["ep"]])}. Limite {n_(f["bruto"]["por_estrato"]["R1"]["limite_principal"])}. '
      f'Pela aritmética literal da frase do registro: {f["veredito"]["letra_literal"]}.')
    P(f'    Forma k x L: {p2["forma_L"]["veredito"]["final"]} (a cláusula não dispara nem com a forma plantada). '
      f'Forma proporcional ao total: teto de {n_(100 * p2["teto_por_forma"]["total"]["natural_zero"]["S_max"], 2, False)}% dos votos de Flávio com nível natural zero '
      f'({n_(100 * p2["teto_por_forma"]["total"]["natural_menor_espelho"]["S_max"], 2, False)}% com o espelho).')
    cb = p3['clausulas']['orig']['bruto']
    P(f'  Parte 3 (T7 estrito): {V["parte3_T7_estrito"]["letra"]} pela letra, só pela cláusula B e por {n_(cb["a_faixa_0-35"] - cb["a_faixa_65-100_com_3pct"], 2, False)} ponto '
      f'((a) de {n_(cb["a_faixa_0-35"], 2, False)}% onde Flávio tem menos de 35% contra {n_(cb["a_faixa_65-100_com_3pct"], 2, False)}% com 3% plantados onde ele tem 65% ou mais). '
      f'Com o plantio pelo valor esperado a cláusula {V["parte3_T7_estrito"]["clausula_B_com_plantio_pelo_valor_esperado"]} '
      f'({n_(x["ruido_do_sorteio"]["clausula_B_T7"]["a_65-100_com_3pct_valor_esperado"], 2, False)}%).')
    P(f'    Limite aritmético estrito: {i_(p3["Lula_bruto"]["pais"]["excesso_estrito"])} votos em {p3["Lula_bruto"]["pais"]["secoes_estrito"]} seções no país inteiro '
      f'(limites de 0,1 milhão, 0,6 milhão e 2,8 milhões). SEM PODER: com 3,6% plantados a soma vai a {i_(p3["calibracao_Lula"]["F_036"]["pais"]["excesso_estrito"])} votos.')
    c4 = p4['criterio']
    P(f'  Parte 4 (L3 por capacidade): {p4["veredito"]["letra"]} pela letra; {p4["veredito"]["final"]} pela regra de recuperação fixada antes. '
      f'P5 no decil de menor capacidade {be([c4["P"], c4["ep"]])}, {n_(abs(c4["z_de_zero"]), 1, False)} ep de zero; espelho (núcleo do PT) {be([p4["espelho"]["criterio"]["P"], p4["espelho"]["criterio"]["ep"]])}.')
    P('  Resumo: ' + V['resumo_em_uma_frase'])
    P('  Contagem: 7 cláusulas de decisão aplicadas; 2 dispararam (P1.3 e cláusula B do T7). A P1.3 passa a 16 ep de zero, não é acaso de amostra; o que se discute nela')
    P('  é o que o coeficiente mede. A cláusula B passa por cerca de 1,5 a 2 erros-padrão; entre 7 cláusulas, o acaso daria por volta de 0,2 a 0,3 disparo dessa margem.')
    P('  Um SINAL só conta como indício depois de o conferente independente reproduzir (Adendo 27). Isso ainda não foi feito para esta peça.')
    P('')
    P('0. CONFERÊNCIAS (o código reproduz o que já estava publicado antes de relatar o novo)')
    P(f'  Estimador próprio contra lib.fe_ols: maior diferença de coeficiente {cf["estimador_maior_dif_coef_contra_lib"]:.1e}; de erro-padrão {cf["estimador_maior_dif_ep_contra_lib"]:.1e}.')
    P(f'  T14 nacional {be(cf["T14_nacional_com_exterior"][:2])} (publicado +0,0393, ep 0,0007); {i_(cf["n_e_locais"][0])} seções informativas em {i_(cf["n_e_locais"][1])} locais (publicado 477.035 e 72.538).')
    P(f'  Identidade do G3 (coeficiente de Flávio no ganho de Lula mais o próprio de Flávio no ganho de Flávio): {cf["identidade_coef_R1_L_mais_F"]:.1e}. Outros no 2º turno: {cf["O2_soma"]}.')
    P(f'  Totais do 2º turno na base: Lula {i_(cf["totais_2T"]["L2"])}, Flávio {i_(cf["totais_2T"]["R2"])}, margem {i_(cf["totais_2T"]["margem"])} (iguais ao oficial).')
    dfm = cf['deputado_federal']
    P(f'  Deputado federal do 1º turno, lido do bweb por filtro de bytes: 26.151.133 linhas em 497.897 seções (os mesmos números do L3); soma diferente do comparecimento em {dfm["soma_diferente_do_comparecimento"]} seções; '
      f'{dfm["secoes_sem_linha_de_deputado_fora_do_exterior"]} seções do país sem deputado; cortes do PL e do PT iguais aos do L3 publicado.')
    al4 = p4['ao_lado']
    P(f'  L3 refeito: quintil de maior fatia do PL {n_(-al4["quintil_PL_inteiro"]["b"])} (ep {n_(al4["quintil_PL_inteiro"]["ep"], 4, False)}), publicado -0,0293 (0,0012); '
      f'quintil de menor fatia {n_(-al4["quintil_PL_mais_fraco_inteiro"]["b"])} (ep {n_(al4["quintil_PL_mais_fraco_inteiro"]["ep"], 4, False)}), publicado -0,0812 (0,0021).')
    P(f'  T7 original refeito: (a) {n_(p3["Lula_bruto"]["pais"]["a_orig"], 2, False)}% e (b) {n_(p3["Lula_bruto"]["pais"]["b_orig"], 2, False)}% (publicado 8,99 e 1,42); por faixa '
      + ', '.join(n_(p3['Lula_bruto'][k]['a_orig'], 2, False) for k in NOME_FAIXA) + ' (publicado 17,90, 8,15, 5,23 e 3,72).')
    P('')
    # ---------------------------------------------------------------- Parte 1
    P('1. PARTE 1: T14 POR DECIL DE CAPACIDADE DE TROCA DE ELEITORES')
    u = p1['universo']
    P(f'  Universo: {i_(u["aptos_iguais"])} seções com aptos iguais nos dois turnos, de {i_(u["secoes_dois_turnos"])} com os dois turnos ({i_(u["aptos_diferentes"])} têm aptos diferentes e saem); {i_(u["exterior_no_universo"])} são do exterior.')
    P('  c = (aptos - comparecimento do 1º turno)/aptos. Regressão do T8 dentro de cada decil, efeito fixo de local, erro agrupado por local.')
    P('  b = coeficiente dos votos de Flávio no 1º turno no ganho de Lula (o coeficiente do T14). Espelho = coeficiente dos votos de Lula no 1º turno no ganho de Flávio.')
    P('  decil | c (mínimo a máximo, média) | seções | informativas | fatia de Flávio no 1T | b (ep) | espelho (ep) | recuperado com 2% | com 3,6%')
    for d in p1['decis']:
        P(f'   D{d["decil"]:<2d} | {n_(d["c_min"], 3, False)} a {n_(d["c_max"], 3, False)}, {n_(d["c_medio"], 3, False)} | {i_(d["secoes"]):>7s} | {i_(d["n"]):>7s} | {n_(100 * d["fatia_F_1T"], 1, False)}% | '
          f'{be([d["b"], d["ep"]])} | {be([-d["pL"], d["ep_pL"]])} | {n_(p1["calibracao"]["F_020"]["recuperado_pontos_por_decil"][d["decil"] - 1], 2, False)} | {n_(p1["calibracao"]["F_036"]["recuperado_pontos_por_decil"][d["decil"] - 1], 2, False)}')
    P('  1.1 Critério (P1.3)')
    P(f'    b(D1) = {be([c["b_D1"], c["ep_D1"]])}: é de pelo menos 0,03 ({"sim" if c["cond_b>=0.03"] else "não"}), a {n_(c["z_de_zero"], 1, False)} ep de zero ({n_(c["z_do_limiar_0.03"], 1, False)} ep do limiar de 0,03), '
      f'e é {n_(100 * c["razao_D1_D10"], 0, False)}% do b(D10) = {n_(c["b_D10"])}. SINAL pela letra, nas duas leituras de "a mais de 4 ep".')
    P(f'    b(D1) menos 0,8 x b(D10) = {be(c["b_D1_menos_0.8_b_D10"])}; menos 0,4 x b(D10) = {be(c["b_D1_menos_0.4_b_D10"])}.')
    P('    O coeficiente quase não muda com a capacidade: fica entre ' + n_(min(d['b'] for d in p1['decis'])) + ' e ' + n_(max(d['b'] for d in p1['decis'])) + ' nos dez decis.')
    P('    Atenção ao que "menor capacidade" quer dizer nos dados: no D1 a abstenção do 1º turno vai até ' + n_(100 * p1['decis'][0]['c_max'], 1, False) + '% (média ' + n_(100 * p1['decis'][0]['c_medio'], 1, False) +
      '%), com ' + i_(p1['decis'][0]['faltosos_1T']) + ' faltosos para ' + i_(p1['decis'][0]['R1']) + ' votos de Flávio. Não existe decil em que "quase não cabem eleitores novos".')
    P('  1.2 Calibração registrada (plantio de 2% e 3,6% dos votos de Flávio no 2º turno, por cima de 2026)')
    k2, k36 = p1['calibracao']['F_020'], p1['calibracao']['F_036']
    P(f'    Recuperação no D1: {n_(k2["recuperado_pontos_por_decil"][0], 2, False)} pontos para 2 plantados e {n_(k36["recuperado_pontos_por_decil"][0], 2, False)} para 3,6: dentro de 0,3 ponto. '
      f'Em todos os decis: com 2% sim; com 3,6% {"sim" if k36["aprovado_todos"] else "não (um decil fica a mais de 0,3; pelo valor esperado, sem sorteio, todos ficam entre " + n_(min(p1["calibracao"]["EF_036"]["recuperado_pontos_por_decil"]), 2, False) + " e " + n_(max(p1["calibracao"]["EF_036"]["recuperado_pontos_por_decil"]), 2, False) + ")"}.')
    rs = x['ruido_do_sorteio']['recuperacao_parte1_D1']
    P(f'    Ruído do sorteio no D1 (exploratório, 200 sorteios): 2% recupera {n_(rs["2.0"]["media"], 2, False)} (dp {n_(rs["2.0"]["dp"], 2, False)}); 3,6% recupera {n_(rs["3.6"]["media"], 2, False)} (dp {n_(rs["3.6"]["dp"], 2, False)}).')
    P(f'    O critério aplicado aos dados com plantio: {k2["criterio_com_plantio"]["veredito_letra"]} com 2% e {k36["criterio_com_plantio"]["veredito_letra"]} com 3,6%. O instrumento enxerga a troca plantada.')
    P('    Outras formas, 3,6% (deslocamento de b no D1, em pontos): forma k x L ' + n_(p1['calibracao']['L_036']['deslocamento_b_pontos_por_decil'][0], 2) + '; proporcional ao total ' + n_(p1['calibracao']['T_036']['deslocamento_b_pontos_por_decil'][0], 2) +
      '; concentrada onde Lula é forte ' + n_(p1['calibracao']['C_036']['deslocamento_b_pontos_por_decil'][0], 2) + '. O coeficiente de Flávio é cego para a forma k x L.')
    P('  1.3 Espelho')
    e = p1['espelho']['criterio']
    P(f'    O mesmo critério para Lula perdendo para Flávio: espelho(D1) = {be([e["b_D1"], e["ep_D1"]])}, espelho(D10) = {n_(e["b_D10"])}: {e["veredito_letra"]} (abaixo de 0,015). '
      f'O plantio espelho de 3,6% é recuperado no D1 ({n_(p1["espelho"]["M_036"]["recuperado_pontos_por_decil"][0], 2, False)}) e faria o espelho dar {p1["espelho"]["M_036"]["criterio_com_plantio"]["veredito_letra"]}.')
    P(f'    Diferença no D1 entre o coeficiente de Flávio e o de Lula: {n_(c["b_D1"] - e["b_D1"])} (ep {n_(float(np.hypot(c["ep_D1"], e["ep_D1"])), 4, False)}).')
    P('  1.4 Ao lado (fixado antes; não entra no veredito)')
    se = p1['ao_lado']['sem_exterior']
    P(f'    Sem o exterior: b(D1) {n_(se["criterio"]["b_D1"])}, b(D10) {n_(se["criterio"]["b_D10"])}, razão {n_(se["criterio"]["razao_D1_D10"], 3, False)}: {se["criterio"]["veredito_letra"]}, faltando {n_(80 - 100 * se["criterio"]["razao_D1_D10"], 1, False)} ponto percentual para os 80%. '
      f'As {x["D1_por_faixa"]["D10_so_exterior"]["secoes"]} seções do exterior que caem no D10 têm coeficiente {be([x["D1_por_faixa"]["D10_so_exterior"]["b"], x["D1_por_faixa"]["D10_so_exterior"]["ep"]])} e puxam o D10 para baixo.')
    em = p1['ao_lado']['empilhada_fe_comum']
    P(f'    Empilhada com efeito fixo de local comum: b(D1) {be(em["b_por_decil"][0])}, b(D10) {be(em["b_por_decil"][9])}: {em["criterio"]["veredito_letra"]}. Espelho: D1 {be([-em["pL_por_decil"][0][0], em["pL_por_decil"][0][1]])}, D10 {be([-em["pL_por_decil"][9][0], em["pL_por_decil"][9][1]])}.')
    it = p1['ao_lado']['interacao_continua']
    P(f'    Interação contínua: coeficiente de Flávio extrapolado para capacidade zero {be(it["b_em_c0"])}; inclinação por unidade de c {be(it["b_por_unidade_de_c"])}. Reta dos dez decis: intercepto {be([p1["ao_lado"]["reta_b_contra_c"]["intercepto_c0"], p1["ao_lado"]["reta_b_contra_c"]["ep_intercepto_inflado"]])}.')
    P('    Outros agregados em vez dos grupos: b(D1) ' + n_(p1['ao_lado']['sem_grupos'][0]['b']) + ', b(D10) ' + n_(p1['ao_lado']['sem_grupos'][9]['b']) + ': mesmo veredito.')
    P('    Outros anos, mesma conta com outros agregados (NÃO É RÉGUA; o Léo suspeita também desses anos). Coeficiente no D1 e no D10:')
    P(f'      2026: Flávio perdendo para Lula {n_(p1["ao_lado"]["sem_grupos"][0]["b"])} e {n_(p1["ao_lado"]["sem_grupos"][9]["b"])}; Lula perdendo para Flávio {n_(-p1["ao_lado"]["sem_grupos"][0]["pL"])} e {n_(-p1["ao_lado"]["sem_grupos"][9]["pL"])}.')
    for ano, o in p1['ao_lado']['outros_anos_nao_e_regua'].items():
        d1, d10 = o['decis'][0], o['decis'][9]
        ca = x['criterio_P1_em_outros_anos'][ano]
        P(f'      {ano}: {o["adversario"]} perdendo para {o["PT"]} {n_(d1["perda_do_adversario_para_o_PT"][0])} e {n_(d10["perda_do_adversario_para_o_PT"][0])} (a letra daria {ca["adversario_para_PT"]["veredito_letra"]}); '
          f'{o["PT"]} perdendo para {o["adversario"]} {n_(d1["perda_do_PT_para_o_adversario"][0])} e {n_(d10["perda_do_PT_para_o_adversario"][0])} (a letra daria {ca["PT_para_adversario"]["veredito_letra"]}).')
    P('      Leitura: pela mesma letra, 2022 daria SINAL com os papéis trocados (eleitor de Lula "perdido" para Bolsonaro, +0,0313 no D1, 90% do D10; na leitura a 4 ep do limiar, INCONCLUSIVO).')
    P('      Ou houve troca contra Lula em 2022, o que ninguém sustenta, ou o coeficiente do T8 passa de 0,03 no decil de menor capacidade por razão que não é troca de voto.')
    P('  1.5 EXPLORATÓRIO (depois de ver o resultado): o que o coeficiente do T8 mede')
    P('    A regressão do T8 tem a variação do comparecimento como controle (coeficiente ' + n_(x['transferencia']['decomposicao_do_b_do_T8']['coef_dcomp'], 3, False) + '). Um eleitor de Flávio que falta no 2º turno derruba o comparecimento em 1, a regressão')
    P('    espera que Lula perca 0,57 voto com isso, Lula não perde nada, e a sobra aparece como "voto de Flávio que foi para Lula". O coeficiente do T14 mistura as duas coisas.')
    P('    Matriz de transferência sem esses controles (L2, R2, branco+nulo e faltosos do 2º turno contra tudo do 1º turno; a especificação do desenho cego D4-1, aqui sem peso), por decil:')
    P('    decil | Flávio 1T que aparece em Lula (ep) | Lula 1T que aparece em Flávio (ep) | Flávio 1T que não voltou (ep) | Lula 1T que não voltou (ep)')
    for d in x['transferencia']['decis']:
        P(f'     D{d["decil"]:<2d} | {be(d["V_R1_em_L2"])} | {be(d["M_L1_em_R2"])} | {be(d["R1_em_faltosos_2T"])} | {be(d["L1_em_faltosos_2T"])}')
    uu = x['transferencia']['universo_aptos_iguais']
    P(f'     todos | {be(uu["V_R1_em_L2"])} | {be(uu["M_L1_em_R2"])} | {be(uu["R1_em_faltosos_2T"])} | {be(uu["L1_em_faltosos_2T"])}')
    dd = x['transferencia']['decomposicao_do_b_do_T8']
    P(f'    Conferência da decomposição no universo: b do T8 {n_(dd["b_T8"])} contra transferência {n_(dd["V"])} + faltosos {n_(dd["parcela_faltosos"])} + branco e nulo {n_(dd["parcela_branco_nulo"])} = {n_(dd["soma"])}.')
    t1 = x['transferencia']['decis'][0]
    P(f'    No D1, a parcela dos votos de Flávio que aparece em Lula é {be(t1["V_R1_em_L2"])}, igual ao espelho {be(t1["M_L1_em_R2"])}. O que é diferente é quem não voltou: {be(t1["R1_em_faltosos_2T"])} dos eleitores de Flávio contra {be(t1["L1_em_faltosos_2T"])} dos de Lula.')
    P(f'    A letra da P1.3 aplicada à transferência: {x["transferencia"]["criterio_P1_com_V"]["veredito_letra"]} (D1 abaixo de 0,015 e {n_(100 * x["transferencia"]["criterio_P1_com_V"]["razao_D1_D10"], 0, False)}% do D10); espelho {x["transferencia"]["criterio_P1_com_V_espelho_M"]["veredito_letra"]}. '
      f'A transferência cresce com a capacidade nos dois sentidos, de {n_(100 * t1["V_R1_em_L2"][0], 1, False)}% a {n_(100 * x["transferencia"]["decis"][9]["V_R1_em_L2"][0], 1, False)}% e de {n_(100 * t1["M_L1_em_R2"][0], 1, False)}% a {n_(100 * x["transferencia"]["decis"][9]["M_L1_em_R2"][0], 1, False)}%: é o desenho que a troca de eleitores prevê.')
    P(f'    O plantio de 3,6% também aparece na transferência do D1 (sobe {n_(x["transferencia"]["recuperacao_V_D1_pontos"]["3.6pct"], 2, False)} pontos; com plantio a letra daria {x["transferencia"]["criterio_P1_com_V_e_3.6pct_plantados"]["veredito_letra"]}, porque a razão com o D10 não chega a 80%).')
    P('    Uma troca de voto dentro da urna não mexe no comparecimento: aparece na transferência, não em "quem não voltou". O sinal da Parte 1 é do canal do comparecimento.')
    P('    Quem não voltou, nos outros anos (NÃO É RÉGUA; universo de aptos iguais; adversário e PT):')
    P(f'      2026: Flávio {n_(100 * uu["R1_em_faltosos_2T"][0], 2)}%, Lula {n_(100 * uu["L1_em_faltosos_2T"][0], 2)}%; no D1, Flávio {n_(100 * t1["R1_em_faltosos_2T"][0], 2)}%, Lula {n_(100 * t1["L1_em_faltosos_2T"][0], 2)}%.')
    for ano, o in x['transferencia_outros_anos_nao_e_regua'].items():
        P(f'      {ano}: adversário {n_(100 * o["universo_aptos_iguais"]["adversario_em_faltosos_2T"][0], 2)}%, PT {n_(100 * o["universo_aptos_iguais"]["PT_em_faltosos_2T"][0], 2)}%; no D1, adversário {n_(100 * o["D1"]["adversario_em_faltosos_2T"][0], 2)}%, PT {n_(100 * o["D1"]["PT_em_faltosos_2T"][0], 2)}%.')
    P('      Em 2014, 2018 e 2022 quem menos voltou foi o eleitor do PT, por 0,8 a 2,1 pontos; em 2026 é o de Flávio, por 3,5 pontos (4,2 no D1). Essa inversão é real e fica sem explicação aqui.')
    P('    O D1 aberto pela fatia de Flávio na seção (coeficiente de Flávio do T8):')
    for k in NOME_FAIXA:
        a = x['D1_por_faixa']['D1'][k]; bU = x['D1_por_faixa']['universo'][k]
        P(f'      Flávio com {k.replace("-", " a ")}%: D1 {be([a["b"], a["ep"]])} ({i_(a["n"])} seções informativas); universo {be([bU["b"], bU["ep"]])}; próprio de Lula no universo {be([bU["pL"], bU["ep_pL"]])}.')
    P('      O coeficiente do D1 não é uniforme: é alto onde Lula domina e baixo onde Flávio domina, igual ao resto do país. É o desenho do T35 (item A4), não o de uma fração fixa.')
    P('')
    # ---------------------------------------------------------------- Parte 2
    P('2. PARTE 2: T16 POR ESTRATO DE REDUTO, TRÊS FORMAS DE TROCA')
    P(f'  Universo: {i_(p2["universo_secoes"])} seções com os dois turnos, fora do exterior. Cortes: fatia de Flávio acima de {n_(100 * p2["cortes"]["fatia_Flavio_p95_p99"][1], 1, False)}% (1%) e de {n_(100 * p2["cortes"]["fatia_Flavio_p95_p99"][0], 1, False)}% (5%); '
      f'PL para deputado federal acima de {n_(100 * p2["cortes"]["PL_quintis"][3], 1, False)}% (quintil). Espelhos: Lula acima de {n_(100 * p2["cortes"]["fatia_Lula_p95_p99"][1], 1, False)}% e de {n_(100 * p2["cortes"]["fatia_Lula_p95_p99"][0], 1, False)}%; PT acima de {n_(100 * p2["cortes"]["PT_quintis"][3], 1, False)}%.')
    P('  estrato | seções | informativas | Flávio e Lula no 1T | coeficiente de Flávio b (ep) | próprio de Lula (ep) | b com 2% | b com 3,6% (forma F)')
    rot = {'R1': 'reduto de Flávio 1%', 'R5': 'reduto de Flávio 5%', 'RPL': 'quintil do PL', 'E1': 'espelho, Lula 1%', 'E5': 'espelho, Lula 5%', 'EPT': 'espelho, quintil do PT', 'PAIS': 'país sem exterior'}
    for k in ('R1', 'R5', 'RPL', 'E1', 'E5', 'EPT', 'PAIS'):
        s_ = p2['estratos'][k]
        P(f'   {rot[k]:<24s} | {i_(s_["secoes"]):>7s} | {i_(s_["n"]):>7s} | {n_(100 * s_["fatia_F_1T"], 1, False)}% e {n_(100 * s_["fatia_L_1T"], 1, False)}% | {be([s_["b"], s_["ep"]])} | {be([s_["pL"], s_["ep_pL"]])} | {n_(s_["plantio"]["F_020"]["b"])} | {n_(s_["plantio"]["F_036"]["b"])}')
    es = p2['espelho']
    P(f'  Nível natural pelo espelho (Lula perdendo para Flávio nos redutos de Lula): {be([es["coef"]["E1"], es["ep"]["E1"]])}, {be([es["coef"]["E5"], es["ep"]["E5"]])} e {be([es["coef"]["EPT"], es["ep"]["EPT"]])}. Menor: {n_(es["menor"])}.')
    P('  2.1 Forma s x F (troca uniforme proporcional aos votos de Flávio)')
    for k in ('R1', 'R5', 'RPL'):
        a = f['bruto']['por_estrato'][k]
        P(f'    {rot[k]}: b + 2 ep = {n_(a["b_mais_2ep"])}; limite principal {n_(a["limite_principal"])}: {"exclui" if a["exclui_principal"] else "não exclui"}; limite literal {n_(a["limite_literal"])}: {"exclui" if a["exclui_literal"] else "não exclui"}; '
          f'contra o próprio espelho {n_(a["limite_proprio_espelho"])}: {"exclui" if a["exclui_proprio_espelho"] else "não exclui"}. Sinal (0,03 a mais de 4 ep): {"sim" if a["sinal"] else "não"}.')
    P(f'    Veredito: {f["veredito"]["letra"]} (pelo menos um estrato exclui e nenhum dá sinal). Leituras ao lado: literal {f["veredito"]["letra_literal"]}; maior espelho {f["veredito"]["letra_maior_espelho"]}; cada estrato com o próprio espelho {f["veredito"]["letra_proprio_espelho"]}; espelho com 2% plantados {f["veredito"]["letra_espelho_plantado"]}.')
    P(f'    Poder: os três estratos têm 2 ep abaixo de 0,02 e recuperam o plantio (1%: {n_(f["poder"]["R1"]["recuperado_2pct"], 2, False)} e {n_(f["poder"]["R1"]["recuperado_3.6pct"], 2, False)}; 5%: {n_(f["poder"]["R5"]["recuperado_2pct"], 2, False)} e {n_(f["poder"]["R5"]["recuperado_3.6pct"], 2, False)}; PL: {n_(f["poder"]["RPL"]["recuperado_2pct"], 2, False)} e {n_(f["poder"]["RPL"]["recuperado_3.6pct"], 2, False)}). '
      f'Com 2% plantados o critério deixa de excluir ({f["veredito"]["com_2pct_plantados"]}); com 3,6% dá {f["veredito"]["com_3.6pct_plantados"]}. O teste enxerga a forma F.')
    et = p2['espelho_do_teste']
    P(f'    Espelho do teste: os redutos de Lula, julgados com o menor coeficiente dos redutos de Flávio como nível natural ({n_(et["natural_usado"])}), também ficam excluídos e sem sinal. Os dois lados perdem o mesmo nos próprios redutos.')
    ar = p2['assimetria_reduto_menos_espelho']
    P(f'    Diferença reduto de Flávio menos espelho de Lula: 1% {be([ar["R1"]["dif"], ar["R1"]["ep"]])}; 5% {be([ar["R5"]["dif"], ar["R5"]["ep"]])}; partido {be([ar["RPL"]["dif"], ar["RPL"]["ep"]])}. '
      f'No quintil do partido a diferença existe, mas os dois estratos não são simétricos: o do PL tem Lula com {n_(100 * p2["estratos"]["RPL"]["fatia_L_1T"], 0, False)}% e o do PT tem Flávio com {n_(100 * p2["estratos"]["EPT"]["fatia_F_1T"], 0, False)}%.')
    P('  2.2 Forma k x L (troca proporcional aos votos de Lula)')
    il = p2['inclinacoes_por_unidade_de_troca']['L']
    P(f'    O coeficiente de Flávio nos redutos não se mexe com essa forma (inclinação {n_(il["R1"]["b"], 3, False)}, {n_(il["R5"]["b"], 3, False)} e {n_(il["RPL"]["b"], 3, False)} por unidade de troca). Quem se mexe é o próprio de Lula (inclinação {n_(il["PAIS"]["pL"], 2, False)} no país).')
    fl = p2['forma_L']
    P('    Cláusula do registro (|próprio de Lula| < 0,01 e coeficiente de Flávio > 0,04, em todos os estratos): nos três redutos, ' + ('dispara' if fl['bruto_redutos']['indicio'] else 'não dispara') +
      '; nos três espelhos (ao lado), ' + ('dispara' if fl['bruto_espelhos_ao_lado']['indicio'] else 'não dispara') + '; no país (ao lado), ' + ('dispara' if fl['bruto_pais_ao_lado']['indicio'] else 'não dispara') + '.')
    P(f'    Com a forma L de 3,6% plantada a cláusula {"dispara" if fl["veredito"]["clausula_dispara_com_forma_L_3.6pct_plantada"] else "não dispara"} nos redutos (exige coeficiente de Flávio acima de 0,04 onde essa forma não o move): SEM PODER.')
    P(f'    Nos espelhos, com 2% plantados ela dispararia e com 3,6% não (o próprio de Lula passa de zero e sai da faixa): a cláusula mede nível, e o nível natural do próprio de Lula não se conhece.')
    P(f'    Valores brutos: próprio de Lula {n_(p2["estratos"]["E1"]["pL"])}, {n_(p2["estratos"]["E5"]["pL"])} e {n_(p2["estratos"]["EPT"]["pL"])} nos redutos dele e {n_(p2["estratos"]["PAIS"]["pL"])} no país. Uma troca k x L do tamanho que vira (k de 3,3%) pediria que, sem ela, Lula perdesse cerca de 4,5% dos próprios eleitores no país. Este teste não tem como dizer se perderia.')
    P('  2.3 Forma proporcional ao total e teto de cada forma (P2.6)')
    it_ = p2['inclinacoes_por_unidade_de_troca']
    P(f'    Inclinação do coeficiente de Flávio por unidade de troca, no reduto de 1%: forma F {n_(it_["F"]["R1"]["b"], 2, False)}; forma L {n_(it_["L"]["R1"]["b"], 2, False)}; total {n_(it_["total"]["R1"]["b"], 2, False)}.')
    for forma, nm in (('F', 's x F'), ('total', 'proporcional ao total')):
        t0, t1_ = p2['teto_por_forma'][forma]['natural_zero'], p2['teto_por_forma'][forma]['natural_menor_espelho']
        P(f'    Teto da forma {nm}: com nível natural zero, {n_(100 * t0["S_max"], 2, False)}% dos votos de Flávio ({i_(t0["votos"]["votos_trocados"])} votos, {n_(100 * t0["votos"]["fracao_da_margem"], 0, False)}% da margem; ponto {n_(100 * t0["S_ponto"], 2, False)}%); '
          f'com o espelho, {n_(100 * t1_["S_max"], 2, False)}% ({i_(t1_["votos"]["votos_trocados"])} votos, {n_(100 * t1_["votos"]["fracao_da_margem"], 0, False)}% da margem). Limita: reduto de 1%.')
    P('    Forma k x L: o coeficiente de reduto é cego; não há teto.')
    P(f'    Forma concentrada onde Lula é forte, do tamanho que vira (ao lado): moveria o coeficiente do reduto de 1% em {n_(100 * (p2["estratos"]["R1"]["plantio"]["C_036"]["b"] - p2["estratos"]["R1"]["b"]), 2)} ponto e o de 5% em {n_(100 * (p2["estratos"]["R5"]["plantio"]["C_036"]["b"] - p2["estratos"]["R5"]["b"]), 2)}. A exclusão desta parte não vale para ela.')
    P('  2.4 EXPLORATÓRIO: matriz de transferência nos mesmos estratos (aptos iguais)')
    for k in ('R1', 'R5', 'RPL', 'E1', 'E5', 'EPT'):
        a = x['transferencia']['estratos_parte2_aptos_iguais'][k]
        P(f'    {rot[k]:<24s}: Flávio 1T em Lula {be(a["V_R1_em_L2"])}; Lula 1T em Flávio {be(a["M_L1_em_R2"])}; Flávio 1T que não voltou {be(a["R1_em_faltosos_2T"])}; Lula 1T que não voltou {be(a["L1_em_faltosos_2T"])}.')
    P('    Nos redutos de Lula, pela matriz de transferência, o coeficiente alto de Flávio no T8 (+0,27 e +0,16) corresponde a eleitor que não voltou (30% e 19%, com ep de 6 e 1 ponto); a parcela que aparece em Lula é zero.')
    P('    É regressão ecológica em seções muito homogêneas: o número diz que, dentro do mesmo local, a seção com mais votos de Flávio no 1º turno teve mais faltosos no 2º; não identifica eleitores.')
    P('')
    # ---------------------------------------------------------------- Parte 3
    P('3. PARTE 3: T7 ESTRITO (LIMITE ARITMÉTICO)')
    P(f'  Bolo máximo = outros + brancos + nulos + faltosos do 1º turno: {i_(p3["bolo_max_total"])} no país (bolo do Adendo 3: {i_(p3["bolo_orig_total"])}). Ganho de Lula {i_(p3["ganho_Lula"])}; de Flávio {i_(p3["ganho_Flavio"])}.')
    P('  O excesso estrito é positivo quando os votos de Lula no 2º turno passam de todos os eleitores da seção que não votaram em Flávio no 1º turno.')
    P('  faixa da fatia de Flávio | seções | (a) bolo do Adendo 3 (ep) | (b) | excesso | (a) estrito | seções com excesso estrito | excesso estrito em votos')
    for k in ['pais'] + NOME_FAIXA:
        a = p3['Lula_bruto'][k]
        P(f'   {("país" if k == "pais" else k.replace("-", " a ") + "%"):<10s} | {i_(a["secoes"]):>7s} | {n_(a["a_orig"], 2, False)}% ({n_(a["ep_a_orig"], 2, False)}) | {n_(a["b_orig"], 2, False)}% | {i_(a["excesso_orig"]):>7s} | {n_(a["a_estrito"], 4, False)}% | {a["secoes_estrito"]} | {i_(a["excesso_estrito"])}')
    ef = p3['Flavio_bruto_espelho']
    P(f'  Espelho (ganho de Flávio; faixas pela fatia de Lula): (a) {n_(ef["pais"]["a_orig"], 2, False)}% no país; ' + ', '.join(n_(ef[k]['a_orig'], 2, False) for k in NOME_FAIXA) + f' por faixa; excesso estrito {i_(ef["pais"]["excesso_estrito"])} votos em {ef["pais"]["secoes_estrito"]} seção.')
    P(f'  Só aptos iguais: excesso estrito {i_(p3["Lula_aptos_iguais"]["pais"]["excesso_estrito"])} votos em {p3["Lula_aptos_iguais"]["pais"]["secoes_estrito"]} seções (as 10 seções têm aptos iguais). Sem o exterior: o mesmo.')
    P('  3.1 Calibração dentro de 2026 (forma F por sorteio; quanto cada ponto de troca acrescenta)')
    P('    troca | (a) país | (a) por faixa de Flávio (0 a 35, 35 a 50, 50 a 65, 65 a 100) | (b) país | excesso estrito no país')
    P(f'     0,0% | {n_(p3["Lula_bruto"]["pais"]["a_orig"], 2, False)} | ' + ', '.join(n_(p3['Lula_bruto'][k]['a_orig'], 2, False) for k in NOME_FAIXA) + f' | {n_(p3["Lula_bruto"]["pais"]["b_orig"], 2, False)} | {i_(p3["Lula_bruto"]["pais"]["excesso_estrito"])} votos')
    for nm, t in (('F_010', '1,0%'), ('F_020', '2,0%'), ('F_030', '3,0%'), ('F_036', '3,6%')):
        a = p3['calibracao_Lula'][nm]
        P(f'     {t} | {n_(a["pais"]["a_orig"], 2, False)} | ' + ', '.join(n_(a[k]['a_orig'], 2, False) for k in NOME_FAIXA) + f' | {n_(a["pais"]["b_orig"], 2, False)} | {i_(a["pais"]["excesso_estrito"])} votos')
    inc = p3['inclinacao_por_ponto_de_troca']
    P(f'    Cada ponto de troca acrescenta ao (a) do país {n_(inc["pais"]["a_orig_por_ponto_ate_1"], 2, False)} pontos no primeiro ponto e {n_(inc["pais"]["a_orig_por_ponto_ate_3.6"], 2, False)} em média até 3,6; na faixa de 65% ou mais, {n_(inc["65-100"]["a_orig_por_ponto_ate_3.6"], 2, False)}; na faixa abaixo de 35%, {n_(inc["0-35"]["a_orig_por_ponto_ate_3.6"], 2, False)}.')
    P(f'    Ao excesso estrito, cada ponto acrescenta {n_(inc["pais"]["excesso_estrito_por_ponto_ate_3.6"], 0, False)} votos no país inteiro. O limite aritmético não enxerga uma troca de 2,15 milhões de votos.')
    P('    Outras formas, 3,6% (ao lado), (a) por faixa: k x L ' + ', '.join(n_(p3['calibracao_Lula']['L_036'][k]['a_orig'], 1, False) for k in NOME_FAIXA) + '; total ' + ', '.join(n_(p3['calibracao_Lula']['T_036'][k]['a_orig'], 1, False) for k in NOME_FAIXA) +
      '; concentrada ' + ', '.join(n_(p3['calibracao_Lula']['C_036'][k]['a_orig'], 1, False) for k in NOME_FAIXA) + '.')
    P('  3.2 Cláusulas')
    P(f'    A: excesso estrito somado acima de 600.000 votos? Não: {i_(cb["soma_excesso_estrito"])} votos. Limite de indício do T14 (2,8 milhões): não. Abaixo de 100.000: sim.')
    rb = x['ruido_do_sorteio']['clausula_B_T7']
    P(f'    B: (a) da faixa abaixo de 35% ({n_(cb["a_faixa_0-35"], 2, False)}%) acima do (a) da faixa de 65% ou mais com 3% plantados ({n_(cb["a_faixa_65-100_com_3pct"], 2, False)}%)? Sim, por {n_(cb["a_faixa_0-35"] - cb["a_faixa_65-100_com_3pct"], 2, False)} ponto.')
    P(f'       Exploratório: em 200 sorteios do plantio, o lado direito fica em {n_(rb["a_65-100_com_3pct_binomial"]["media"], 2, False)}% (dp {n_(rb["a_65-100_com_3pct_binomial"]["dp"], 2, False)}; de {n_(rb["a_65-100_com_3pct_binomial"]["min"], 2, False)} a {n_(rb["a_65-100_com_3pct_binomial"]["max"], 2, False)}) e a cláusula dispara em todos. '
      f'Com o plantio pelo valor esperado (como o Adendo 4 fez em 2022) o lado direito é {n_(rb["a_65-100_com_3pct_valor_esperado"], 2, False)}% e a cláusula não dispara.')
    P(f'       O (a) de 17,90% equivale ao que uma troca de 3,0% a 3,1% produz na faixa forte de Flávio (3,1% por sorteio: {n_(rb["a_65-100_por_tamanho_de_troca"]["3.1"]["binomial_media_20"], 2, False)}%; 2,9% pelo valor esperado: {n_(rb["a_65-100_por_tamanho_de_troca"]["2.9"]["valor_esperado"], 2, False)}%). O limiar do registro era 3%.')
    P(f'    SEM SINAL exigiria gradiente por faixa igual ao espelho: Lula {n_(cb["gradiente_Lula"], 2)} pontos, espelho de Flávio {n_(cb["gradiente_espelho_Flavio"], 2)}. Não é igual.')
    c36 = p3['clausulas']['orig']['com_3.6pct_plantados']; cc = p3['clausulas']['orig']['com_forma_concentrada_3.6pct']
    P(f'    O que a cláusula B enxerga: com 3,6% uniformes plantados ela deixa de disparar ({n_(c36["a_faixa_0-35"], 2, False)}% contra {n_(c36["a_faixa_65-100_com_3pct"], 2, False)}%); com a forma concentrada onde Lula é forte ela dispara ({n_(cc["a_faixa_0-35"], 2, False)}% contra {n_(cc["a_faixa_65-100_com_3pct"], 2, False)}%). '
      'Ela não é detector de troca uniforme: mede se o excesso se concentra onde Flávio é fraco.')
    eb = p3['clausulas']['orig']['espelho_clausula_B']
    P(f'    Espelho da cláusula B: (a) de Flávio onde Lula tem menos de 35% {n_(eb["a_Flavio_onde_Lula_0-35"], 2, False)}% contra {n_(eb["a_Flavio_onde_Lula_65-100_com_3pct"], 2, False)}% com 3% plantados onde Lula tem 65% ou mais: não dispara. '
      'Mas os dois lados não são comparáveis em nível: Lula ganhou 10,4 milhões de votos entre os turnos e Flávio 3,7 milhões, disputando o mesmo bolo.')
    P(f'    Com o (a) do bolo máximo (ao lado): letra {p3["veredito"]["letra_com_a_estrito_ao_lado"]}, sem valor, porque esse (a) é de {n_(p3["Lula_bruto"]["pais"]["a_estrito"], 4, False)}% e não se mexe com plantio nenhum.')
    P('    Conta que ajuda a ler o (a): pela identidade do 2º turno, excesso positivo sobre o bolo do Adendo 3 quer dizer que Flávio perdeu votos na seção além da queda do comparecimento e da alta do branco e nulo.')
    P('    Não é troca provada: é saída líquida de votos de Flávio, que também vem de eleitor dele que faltou e foi substituído por eleitor novo de Lula.')
    te = p3['troca_equivalente_por_faixa_premissa_espelho']
    P('    Leitura com premissa (P3.8; o espelho de Flávio como nível natural, premissa fraca pelo motivo acima): troca uniforme equivalente de ' + n_(te['pais']['troca_pct'], 1, False) + '% no país; por faixa ' + ', '.join(n_(te[k]['troca_pct'], 1, False) + '%' for k in NOME_FAIXA) + '.')
    P('  3.3 Seções com excesso estrito (casos individuais; todas com aptos iguais)')
    for s_ in p3['secoes_com_excesso_estrito']['maiores']:
        P(f'    {s_["secao"]}: excesso {int(s_["excesso"])}; Lula {s_["L1"]} para {s_["L2"]}, Flávio {s_["R1"]} para {s_["R2"]}; aptos {s_["apt1"]}; comparecimento {s_["comp1"]} e {s_["comp2"]}.')
    P('    São seções pequenas ou de comparecimento quase total em que alguns eleitores de Flávio do 1º turno votaram em Lula no 2º (ou foram trocados por outros). Vinte votos no país.')
    P('    A parte determinística do A2, que usa os aptos do 2º turno, lista as mesmas 10 seções e mais algumas em que o número de aptos mudou entre os turnos (por exemplo BA|34134|170|262, de 119 para 68 aptos); nessas o limite deixa de ser estrito.')
    P('  3.4 Por UF: (a) do bolo do Adendo 3, bruto e com 3,6% plantados; excesso estrito em votos; espelho de Flávio')
    for u_, a in sorted(p3['por_UF'].items(), key=lambda kv: -kv[1]['a_orig']):
        P(f'    {u_}: {n_(a["a_orig"], 1, False)}% e {n_(a["a_orig_com_3.6pct"], 1, False)}%; estrito {int(a["excesso_estrito"])} ({a["secoes_estrito"]} seç.); espelho {n_(a["espelho_Flavio_a_orig"], 2, False)}%; Flávio no 1T {n_(100 * a["fatia_F_1T"], 0, False)}%')
    P('')
    # ---------------------------------------------------------------- Parte 4
    P('4. PARTE 4: L3 (NÚCLEO DO PL) POR DECIL DE CAPACIDADE')
    P(f'  Quintil de maior fatia do PL: {i_(p4["quintil_PL_secoes"])} seções ({i_(p4["quintil_PL_aptos_iguais"])} com aptos iguais). Decis com os cortes nacionais da Parte 1.')
    P('  decil | seções | informativas | P5, próprio de Flávio (ep) | com 3,6% | núcleo do PT, próprio de Lula (ep)')
    for a, b_ in zip(p4['PL_por_decil'], p4['PT_por_decil']):
        P(f'   D{a["decil"]:<2d} | {i_(a["secoes"]):>6s} | {i_(a["n"]):>6s} | {be([-a["b"], a["ep"]])} | {n_(-a["plantio"]["F_036"]["b"])} | {be([b_["pL"], b_["ep_pL"]])}')
    P(f'  Critério: P5(D1) = {be([c4["P"], c4["ep"]])}, {n_(abs(c4["z_de_zero"]), 1, False)} ep de zero. Não chega a -0,025 nem fica acima de -0,010: INCONCLUSIVO pela letra.')
    k4 = p4['calibracao']; r4 = x['ruido_do_sorteio']['recuperacao_parte4_PL_D1']
    P(f'  Calibração: o sorteio fixado recupera {n_(k4["F_020"]["recuperado_pontos"], 2, False)} para 2 plantados e {n_(k4["F_036"]["recuperado_pontos"], 2, False)} para 3,6: fora de 0,3 ponto. Pela regra fixada antes (P4.3 e G6), SEM PODER.')
    P(f'    Exploratório: em 200 sorteios a recuperação tem dp de {n_(r4["2.0"]["dp"], 2, False)} e {n_(r4["3.6"]["dp"], 2, False)} ponto e fica a 0,3 em {n_(100 * r4["2.0"]["fracao_a_0.3_ponto"], 0, False)}% e {n_(100 * r4["3.6"]["fracao_a_0.3_ponto"], 0, False)}% deles; pelo valor esperado recupera {n_(r4["2.0"]["valor_esperado"], 2, False)} e {n_(r4["3.6"]["valor_esperado"], 2, False)}. A célula ({i_(p4["PL_por_decil"][0]["n"])} seções informativas) é pequena demais para a tolerância do registro.')
    P(f'    O critério com plantio: {k4["F_020"]["criterio_com_plantio"]["letra"]} com 2% e {k4["F_036"]["criterio_com_plantio"]["letra"]} com 3,6% (a 4 ep de zero; a 4 ep do limiar, {k4["F_036"]["criterio_com_plantio"]["letra_z_do_limiar"]}).')
    e4 = p4['espelho']['criterio']
    P(f'  Espelho: núcleo do PT no D1 {be([e4["P"], e4["ep"]])}: {e4["letra"]}. Diferença entre os dois núcleos no D1: {n_(c4["P"] - e4["P"])} (ep {n_(float(np.hypot(c4["ep"], e4["ep"])), 4, False)}). Onde quase não cabe eleitor novo, os dois núcleos perdem o mesmo.')
    P(f'  Ao lado: quintil de capacidade mais baixo (D1 e D2 juntos) {be([-al4["PL_por_quintil_de_capacidade"][0]["b"], al4["PL_por_quintil_de_capacidade"][0]["ep"]])}; decis recalculados dentro do quintil do PL, D1 {be([-al4["decis_dentro_do_quintil_PL"]["celulas"][0]["b"], al4["decis_dentro_do_quintil_PL"]["celulas"][0]["ep"]])}; '
      f'reta dos dez decis: P5 em capacidade zero {be([al4["reta_P5_contra_c"]["intercepto_c0"], al4["reta_P5_contra_c"]["ep_intercepto_inflado"]])}, inclinação {be([al4["reta_P5_contra_c"]["inclinacao"], al4["reta_P5_contra_c"]["ep_inclinacao"]], 3)} por unidade de c.')
    P('    Com o quintil de capacidade em vez do decil, P5 passaria de -0,025 a mais de 4 ep. O registro pede decil; fica dito.')
    P('')
    # ---------------------------------------------------------------- votos
    P('5. TRADUÇÃO EM VOTOS DE MARGEM (cada linha com a sua premissa)')
    P(f'  Referência: vira com {i_(tv["vira_com"]["votos_trocados"])} votos trocados, {n_(tv["vira_com"]["s_pct"], 2, False)}% dos votos verdadeiros de Flávio; margem oficial {i_(MARGEM)}.')

    def lv(t):
        return f'{n_(t["s_pct"], 2, False)}% = {i_(t["votos_trocados"])} votos trocados, {i_(t["efeito_na_margem"])} de margem ({n_(100 * t["fracao_da_margem"], 0, False)}% da margem; {"vira" if t["vira_o_resultado"] else "não vira"})'
    P('  Parte 1, coeficiente do T8 no D1 inteiro atribuído a desvio e igual no país inteiro (premissa extrema): ' + lv(tv['parte1_D1_nivel_natural_zero']) + '.')
    P('  Parte 1, o mesmo descontando o espelho de Lula: ' + lv(tv['parte1_D1_nivel_natural_espelho']) + f'; intervalo de 95% de {n_(tv["parte1_D1_espelho_ic95"][0]["s_pct"], 2, False)}% a {n_(tv["parte1_D1_espelho_ic95"][1]["s_pct"], 2, False)}%, que contém os 3,57%.')
    P('    Essa conta só vale se o coeficiente do T8 for troca de voto. Pela decomposição exploratória ele é quase todo eleitor que não voltou; a parcela que aparece em Lula dá:')
    P('    transferência no D1, nível natural zero: ' + lv(tv['exploratorio_transferencia_D1_zero']) + '; descontando o espelho: ' + lv(tv['exploratorio_transferencia_D1_espelho']) + '.')
    P('    transferência no universo, nível natural zero: ' + lv(tv['exploratorio_transferencia_universo_zero']) + '; descontando o espelho: ' + lv(tv['exploratorio_transferencia_universo_espelho']) + '.')
    P('  Parte 2, teto da troca uniforme s x F pelos redutos (nível natural zero, 2 ep): ' + lv(tv['parte2_teto_forma_F']['natural_zero']['votos']) + '; com o espelho: ' + lv(tv['parte2_teto_forma_F']['natural_menor_espelho']['votos']) + '.')
    P('  Parte 2, teto da forma proporcional ao total (nível natural zero, 2 ep): ' + lv(tv['parte2_teto_forma_total']['natural_zero']['votos']) + '; com o espelho: ' + lv(tv['parte2_teto_forma_total']['natural_menor_espelho']['votos']) + '.')
    P(f'  Parte 3, excesso estrito: {i_(tv["parte3_excesso_estrito"]["votos"])} votos, {i_(tv["parte3_excesso_estrito"]["efeito_na_margem"])} de margem. Excesso sobre o bolo do Adendo 3: {i_(tv["parte3_excesso_bolo_original"]["votos"])} votos, {i_(tv["parte3_excesso_bolo_original"]["efeito_na_margem"])} de margem ({n_(100 * tv["parte3_excesso_bolo_original"]["fracao_da_margem"], 1, False)}% da margem), se fosse tudo desvio.')
    P('  Parte 4, P5 do D1 inteiro atribuído a desvio uniforme: ' + lv(tv['parte4_PL_D1_nivel_natural_zero']) + '; descontando o núcleo do PT: ' + lv(tv['parte4_PL_D1_nivel_natural_espelho']) + '.')
    P('  Canal do comparecimento (exploratório, fora do que esta peça testa): se o eleitor de Flávio do 1º turno tivesse voltado na mesma taxa do de Lula, seriam cerca de '
      + i_((uu['R1_em_faltosos_2T'][0] - uu['L1_em_faltosos_2T'][0]) * 56104503) + ' votos a mais para Flávio (' + n_(100 * (uu['R1_em_faltosos_2T'][0] - uu['L1_em_faltosos_2T'][0]) * 56104503 / MARGEM, 0, False) + '% da margem, contando uma vez). Não vira, e não é troca de voto.')
    P('')
    P('6. O QUE PESA A FAVOR DA TESE')
    P(f'  - Parte 1 dá SINAL pela letra: o coeficiente de Flávio no T8 é {n_(c["b_D1"])} no decil de menor capacidade e não cresce com a capacidade. A troca de eleitores, do jeito que o reteste a mede, não explica o nível.')
    P(f'  - O espelho não acompanha: Lula {n_(e["b_D1"])} no mesmo decil. A diferença, {n_(c["b_D1"] - e["b_D1"])}, se fosse toda troca de voto e valesse para o país, daria {n_(tv["parte1_D1_nivel_natural_espelho"]["s_pct"], 2, False)}% (2,8% a 4,2%), em cima dos 3,57% que viram.')
    P('  - Cláusula B do T7 dispara pela letra: onde Flávio é fraco, 17,9% das seções têm saída de votos dele além do bolo, o mesmo que uma troca de 3% produziria onde ele é forte.')
    P('  - Quem não voltou (exploratório): o eleitor de Flávio do 1º turno faltou mais no 2º do que o de Lula, 2,65% contra -0,83% no país e 4,9% contra 0,8% no decil de menor capacidade. Em 2014, 2018 e 2022 foi o contrário (o do PT voltou menos). Não é troca de voto, mas é uma assimetria de 2026 sem explicação nesta peça.')
    P('  - A forma k x L e qualquer forma regulada pela força local de Lula não são limitadas por nada aqui. O teto da forma proporcional ao total, com nível natural zero, chega a 3,35% (94% da margem).')
    P('7. O QUE PESA CONTRA A TESE')
    P(f'  - O sinal da Parte 1 não é de troca de voto. Separando (exploratório), a parcela dos votos de Flávio que aparece em Lula no decil de menor capacidade é {n_(100 * t1["V_R1_em_L2"][0], 2, False)}% (ep {n_(100 * t1["V_R1_em_L2"][1], 2, False)}), igual ao espelho de {n_(100 * t1["M_L1_em_R2"][0], 2, False)}%, e cresce com a capacidade nos dois sentidos. Uma troca uniforme de 3,57% poria esse número perto de 4,3%.')
    P('  - A mesma letra dá SINAL em 2022 com os papéis trocados (ao lado, não é régua), e a razão D1/D10 de 2026 cai abaixo de 80% sem 990 seções do exterior. O critério dispara também onde ninguém alega troca.')
    P(f'  - Nos redutos de Flávio (1% e 5% de maior fatia), o coeficiente dele é {n_(p2["estratos"]["R1"]["b"])} e {n_(p2["estratos"]["R5"]["b"])}, igual ao de Lula nos redutos de Lula ({n_(es["coef"]["E1"])} e {n_(es["coef"]["E5"])}). Troca uniforme de 2% ou mais dos votos de Flávio está excluída; o teto é 1,63% (45% da margem) sem premissa de espelho.')
    P('  - O limite aritmético estrito acha 20 votos em 10 seções. Não prova ausência (é cego), mas também não há uma única seção grande em que Lula tenha passado do teto físico.')
    P('  - No núcleo do PL com pouca capacidade, Flávio perde 1,8% (ep 0,6) e o núcleo do PT perde 1,5% (ep 0,4): o mesmo.')
    P('  - A cláusula B do T7 passa por 0,45 ponto, some com o plantio pelo valor esperado e não é produzida por troca uniforme.')
    P('')
    P('8. O QUE ISSO SIGNIFICA')
    P('  Esta peça procura a marca de uma troca de votos proporcional (o programa tira uma fração dos votos de Flávio e põe em Lula). Onde o teste tem poder, a forma uniforme de 2% ou mais não está nos dados.')
    P('  O que os dados mostram de assimétrico entre os dois candidatos é outra coisa (leitura exploratória, a conferir): o eleitor de Flávio do 1º turno voltou menos no 2º, sobretudo onde Lula domina. Troca dentro da urna não muda o comparecimento.')
    P('  Ficam sem limite: troca proporcional aos votos de Lula, troca regulada pela força local de Lula, e qualquer coisa que passe pelo comparecimento.')
    P('')
    P('9. PISTAS PARA OS PRÓXIMOS TESTES')
    P('  - Canal do comparecimento (Onda B, B2 e B3): por que o eleitor de Flávio não voltou, 30% e 19% nos redutos de Lula de 1% e 5%, contra 3% do eleitor de Lula nos redutos de Flávio. Cruzar com horário de fechamento, fila, biometria e perfil de idade da seção.')
    P('  - Testes de troca entre turnos devem usar a matriz de transferência (sem a variação do comparecimento como controle), não o coeficiente do T8. Vale para T14, T16, T35 e L3.')
    P('  - A forma k x L só se testa com testemunha fora da disputa presidencial (D4-3 e D4-4 da Onda D) ou com o voto de Lula contra o voto do PT em outros cargos na mesma urna (H2).')
    P('  - As 10 seções com excesso estrito estão listadas no item 3.3, para conferência de boletim.')
    P('')
    P('10. DESVIOS, DECISÕES E O QUE É EXPLORATÓRIO')
    for d in DESVIOS:
        P('  - ' + d)
    txt = '\n'.join(L) + '\n'
    assert '\u2014' not in txt and '\u2013' not in txt
    with open(SAIDA_TXT, 'w') as fh:
        fh.write(txt)
    return txt


def finalizar(res):
    res['vereditos'] = montar_vereditos(res)
    res['desvios'] = DESVIOS
    with open(SAIDA_JSON, 'w') as f:
        json.dump(res, f, ensure_ascii=False, indent=1, default=_jd)
    gravar('resultado_completo.json', res)
    escrever_txt(res)



# ============================================================ conferências
def conferencias(Bz, cen):
    log('conferências')
    conf = {}
    todos = np.ones(Bz.n, bool)
    # estimador contra lib.fe_ols e identidade (G3)
    f = Reg(Bz.X, Bz.loc)
    a = f.fit(Bz.yL); b = f.fit(Bz.yR)
    nomes = [g for g, _ in GRUPOS] + ['demais', 'queda', 'dcomp', 'R1', 'L1']
    r = fe_ols(Bz.yL, Bz.X, Bz.loc, None, nomes)
    conf['estimador_maior_dif_coef_contra_lib'] = float(max(abs(a['b'][i] - r['coef'][n]) for i, n in enumerate(nomes)))
    conf['estimador_maior_dif_ep_contra_lib'] = float(max(abs(a['ep'][i] - r['ep'][n]) for i, n in enumerate(nomes)))
    conf['T14_nacional_com_exterior'] = [float(a['b'][Bz.iR]), float(a['ep'][Bz.iR]), 'publicado 0,0393 (0,0007)']
    conf['proprio_Lula_nacional'] = [float(a['b'][Bz.iL]), float(a['ep'][Bz.iL]), 'publicado -0,013 (0,001)']
    conf['identidade_coef_R1_L_mais_F'] = float(a['b'][Bz.iR] + b['b'][Bz.iR])
    conf['identidade_coef_L1_L_mais_F'] = float(a['b'][Bz.iL] + b['b'][Bz.iL])
    conf['O2_soma'] = int(Bz.O2.sum())
    conf['n_e_locais'] = [a['n'], a['locais'], 'publicado 477.035 em 72.538']
    conf['totais_2T'] = {'L2': int(Bz.L2.sum()), 'R2': int(Bz.R2.sum()), 'margem': int(Bz.L2.sum() - Bz.R2.sum()),
                         'oficial': [L2_OFICIAL, F2_OFICIAL, MARGEM]}
    conf['deputado_federal'] = {'secoes_sem_linha_de_deputado_fora_do_exterior': int(((Bz.D[:, 0] < 0) & ~Bz.zz).sum()),
                                'secoes_do_exterior_sem_deputado': int(((Bz.D[:, 0] < 0) & Bz.zz).sum()),
                                'soma_diferente_do_comparecimento': int(((Bz.D[:, 0] >= 0) & (Bz.D[:, 1:5].sum(1) != Bz.D[:, 0])).sum()),
                                'comp_deputado_diferente_do_presidente': int(((Bz.D[:, 0] >= 0) & (Bz.D[:, 0] != Bz.comp1)).sum()),
                                'comp_varia_entre_linhas': int((Bz.D[:, 7] > 0).sum()), 'tipo_de_voto_estranho': int((Bz.D[:, 9] > 0).sum()),
                                'universo_L3': [int(Bz.uni_df.sum()), 'publicado 497.897'],
                                'fora_da_base': int(np.load(TRAB + '/base2026.npz')['df_fora_da_base'][0])}
    return conf


# ============================================================ principal
def sha_docstring():
    return hashlib.sha256(__doc__.encode()).hexdigest()


def rodar():
    os.makedirs(TRAB, exist_ok=True)
    extrair_df()
    Bz = Base(montar_base())
    log('base', Bz.n, 'seções')
    cen, info = cenarios(Bz)
    res = {'teste': 'R27_A3: troca proporcional com régua interna (T14, T16, T7 e L3 da equipe vermelha)',
           'registro': 'PRE-REGISTRO-2026-10-26.md, Adendo 27 (commit 2748895, 10/11/2026 00:16:42 UTC); registro/adendo27/equipe_vermelha_relatorio.json',
           'sha256_docstring': sha_docstring(), 'semente': SEMENTE, 'plantios': info}
    res['conferencias'] = conferencias(Bz, cen)
    gravar('parcial_conferencias.json', res)
    p1, cortes, dec = parte1(Bz, cen)
    res['parte1_T14_por_capacidade'] = p1
    gravar('parcial_parte1.json', res)
    p2, estr, cPL, cPT = parte2(Bz, cen)
    res['parte2_T16_redutos'] = p2
    gravar('parcial_parte2.json', res)
    res['parte3_T7_estrito'] = parte3(Bz, cen)
    gravar('parcial_parte3.json', res)
    res['parte4_L3_por_capacidade'] = parte4(Bz, cen, cortes, dec, cPL, cPT)
    gravar('parcial_parte4.json', res)
    res['parte1_T14_por_capacidade']['ao_lado']['outros_anos_nao_e_regua'] = parte1_outros_anos(cortes)
    gravar('parcial_outros_anos.json', res)
    log('exploratório')
    res['exploratorio'] = {'aviso': 'tudo neste bloco foi feito depois de ver os resultados das quatro partes',
                           'transferencia': exploratorio_transferencia(Bz, cen, dec, estr),
                           'D1_por_faixa': exploratorio_d1_por_faixa(Bz, cen, dec),
                           'ruido_do_sorteio': exploratorio_ruido_do_sorteio(Bz, cortes, dec, cPL),
                           'criterio_P1_em_outros_anos': exploratorio_criterio_outros_anos(res['parte1_T14_por_capacidade']),
                           'transferencia_outros_anos_nao_e_regua': exploratorio_transferencia_outros_anos()}
    res['traducao_em_votos'] = traducao_em_votos(res)
    res['tempo_s'] = time.time() - T0
    gravar('resultado_completo.json', res)
    res = json.loads(json.dumps(res, default=_jd))
    finalizar(res)
    log('fim das contas')
    return res


if __name__ == '__main__':
    modo = sys.argv[1] if len(sys.argv) > 1 else ''
    if modo == 'extrair':
        extrair_df()
    elif modo == 'docstring':
        print(__doc__)
    elif modo == 'texto':
        finalizar(json.load(open(SAIDA_JSON)))
    else:
        rodar()
