"""R27_L5 (Adendo 27, Onda D-c, e Adendo 30, última onda): ERRO DAS PESQUISAS ESTADUAIS POR UF.

Fragilidade "L5(a), F13 e F17 (urna contra pesquisas)" de registro/adendo27/equipe_vermelha_relatorio.json.
Registro: PRE-REGISTRO-2026-10-26.md, Adendo 27 (commit 2748895, 10/11/2026 00:16:42 UTC), Adendo 28 (commit 938be19)
e Adendo 30 (commit a7218fb, 10/11/2026 10:08:24 UTC).

LETRA DO REGISTRO (copiada)
  reteste_proposto: "Erro das pesquisas estaduais de presidente no 2º turno, UF por UF (últimos 7 dias, institutos com
    histórico no 1º turno), contra o coeficiente do T16 da UF e contra a fatia de Lula no 1º turno. Um desvio regulado
    pela força local de Lula prevê erro maior onde o coeficiente é maior (PI, MA, AP) e quase zero em SC e PR; uma
    virada nacional de última hora prevê erro igual em toda parte. Somar o erro por recorte de região das pesquisas
    nacionais (Nordeste contra Sul)."
  criterio_proposto: "ERRO ESTRUTURADO (indício a cruzar): inclinação de 20 pontos ou mais por unidade de coeficiente
    (1,6 ponto entre PI e SC) a mais de 3 ep com pelo menos 15 UFs. ERRO UNIFORME: |inclinação| abaixo de 8 com ep
    até 4. Não dá veredito de fraude sozinho: diz qual forma procurar."
  Aviso do Adendo 27: este reteste foi escrito por quem já conhecia os resultados antigos. O critério é novo; a
    escolha do que retestar é posterior ao dado.

O QUE EU JÁ TINHA VISTO AO ESCREVER ESTE DOCSTRING (antes de qualquer busca nova e de qualquer conta)
  - L5(a) nacional (resultados/L5_pesquisas.txt): 11 de 11 institutos, erro médio de Lula no 2º turno +2,70 pontos.
  - Os 27 coeficientes do T16 (resultados/T16_bweb.txt) e a tabela T38 de pontos ganhos por UF.
  - resultados/estaduais_gov_pres_pesquisas_verificadas.txt: AtlasIntel de presidente em AC, AM, DF, ES, RN e TO
    (campo 18 a 23/10) e Paraná Pesquisas no TO, com o resultado ao lado. São 7 erros estaduais que eu já conhecia
    (Lula, urna menos pesquisa: AC -0,5; AM +0,5; DF +2,6; ES +2,1; RN +2,7; TO +1,0 pela AtlasIntel; TO +5,6 pela
    Paraná Pesquisas). Nenhuma outra pesquisa estadual, nenhum recorte por região e nenhuma pesquisa estadual do
    1º turno eram conhecidos. Por isso a regra de inclusão abaixo não foi desenhada em cima dos números que ela decide,
    salvo esses 7, e isso é dito no resultado.

DECISÕES QUE O REGISTRO NÃO FIXA, ESCRITAS ANTES DE LEVANTAR AS PESQUISAS E DE CALCULAR QUALQUER ERRO
(todas relatadas como desvio)

PARTE A: PESQUISAS ESTADUAIS, UF POR UF

Inclusão das pesquisas
P1. Pesquisa estadual: pesquisa de intenção de voto para presidente no 2º turno de 2026 (Lula contra Flávio) com
    amostra desenhada para UMA UF e ficha própria (instituto, datas, amostra). Recorte por estado de amostra nacional
    não entra. Pesquisa de uma só cidade ou região do estado não entra.
P2. Janela "últimos 7 dias antes de 25/10/2026": último dia de campo entre 18/10 e 24/10/2026, inclusive. O primeiro
    dia de campo pode ser anterior. Sensibilidade S1: só as de campo inteiro dentro da janela.
P3. "Instituto com pesquisa também no 1º turno": o instituto divulgou pelo menos uma pesquisa de intenção de voto
    para presidente do 1º turno de 2026 (cenário estimulado, nacional ou em qualquer UF) com campo terminado entre
    04/09 e 03/10/2026. Os 11 institutos do L5(a) já cumprem (resultados/L5_pesquisas.json). Para os demais, a
    pesquisa do 1º turno tem de ser achada com link. Instituto sem essa comprovação fica FORA da análise principal
    e entra só na sensibilidade S3 (todas as pesquisas da janela). Sensibilidade S2: histórico na MESMA UF.
P4. Número usado: fatia de Lula nos votos válidos da pesquisa, Lula / (Lula + Flávio). Se a fonte publica os
    válidos, vale o publicado (é a previsão do instituto, inclusive quando usa modelo de eleitor provável). Se só
    publica os totais do estimulado, válidos = Lula / (Lula + Flávio) dos totais. Sensibilidade S4: sempre pelos
    totais, quando existirem.
P5. Uma pesquisa por instituto e por UF: a de último dia de campo mais recente; empate, a de maior amostra. Mesmo
    instituto com contratantes diferentes conta como um instituto.
P6. Fonte: cada número tem link público (imprensa, instituto ou TSE). Nível "conferida": a página foi aberta
    (WebFetch) e o número está nela, ou já consta como confirmada em resultados/estaduais_gov_pres_pesquisas_
    verificadas.txt. Nível "trecho": o número só apareceu no resumo da busca, sem a página aberta. Nível "tabela":
    veio de tabela de segunda mão (Wikipédia ou agregador) sem a matéria original aberta. A análise principal usa só
    "conferida". Sensibilidade S5: conferida mais tabela mais trecho. Sem login, sem contornar bloqueio.
P7. Amostra não publicada: 1.000 para o erro amostral, marcado. Registro no TSE: anotado quando a fonte traz.
P8. A coleta é feita por UF, com as mesmas buscas para as 27 (nome do estado, "presidente", "2º turno", "Lula",
    "Flávio", e os institutos que fazem pesquisa estadual: AtlasIntel, Quaest, Paraná Pesquisas, Real Time Big Data,
    Datafolha, Ipec, Futura, Veritá, Gerp e os que aparecerem), sem olhar o resultado da UF durante a coleta. O que
    não for achado é listado. A coleta para quando as buscas das 27 UFs tiverem sido feitas ou o limite da ferramenta
    acabar; o que ficou sem busca é dito.

Erro por UF
P9. Urna: fatia de Lula nos válidos do 2º turno da UF, Lula / (Lula + Flávio), da base dados/secoes2026.json.gz
    (bweb oficial, sem o exterior). Não uso número de imprensa para a urna.
P10. Média por UF: média simples da fatia de Lula (válidos) das pesquisas incluídas na UF, uma por instituto.
    erro_UF = urna menos média, em pontos percentuais. Positivo = Lula teve mais do que as pesquisas davam.
    Ao lado: mediana e média ponderada pela amostra.

Regressão e veredito pela letra
P11. x principal = coeficiente do T16 de 2026 por UF, versão principal (com os eliminados separados;
    resultados/T16_bweb.json, 2026 > com_grupos_principal > por_UF > coef). Ao lado, a versão "sem grupos".
    A letra traz "(1,6 ponto entre PI e SC)"; com os coeficientes principais (PI 0,0957; SC 0,0057) 20 por unidade
    dá 1,80 ponto. Vale a inclinação de 20, que é o que a letra fixa.
P12. Estimador principal: mínimos quadrados simples, um ponto por UF, sem peso, erro-padrão clássico. Motivo, dito
    antes: o erro das pesquisas é dominado por erro não amostral (os 11 institutos erraram para o mesmo lado no
    nacional), então ponderar pela amostra daria precisão falsa. Ao lado, sem mudar o veredito pela letra:
    erro-padrão HC3; meta-regressão de efeitos aleatórios (peso 1 / (variância amostral da média + tau²), tau² pelo
    método dos momentos); peso pelos válidos da UF; e regressão no nível da pesquisa com efeito fixo de instituto e
    erro agrupado por UF (tira o viés de casa quando institutos diferentes cobrem UFs diferentes). Se alguma dessas
    der veredito diferente do principal, o resultado é relatado como frágil.
P13. Veredito pela letra (Parte A, coeficiente): ESTRUTURADO se inclinação >= 20 E inclinação / ep > 3 E pelo menos
    15 UFs. UNIFORME se |inclinação| < 8 E ep <= 4. Fora disso, INCONCLUSIVO. Com menos de 15 UFs o ESTRUTURADO é
    impossível pela letra; com menos de 8 UFs não há regressão e o veredito é SEM PODER por falta de dados.
    Tradução para o vocabulário da onda: ESTRUTURADO = SINAL (indício a cruzar, de forma regulada pela força local);
    UNIFORME = SEM SINAL de estrutura (o erro existe e é igual em toda parte); o resto INCONCLUSIVO ou SEM PODER.
P14. Segundo regressor (a letra pede "e contra a fatia de Lula no 1º turno", sem limiar): x2 = Lula / válidos do
    1º turno na UF (válidos sem o candidato 28, anulado; dados/candidatos2026_1t.json.gz). Relato inclinação, ep e
    a diferença prevista entre PI e SC. Tradução do limiar, dita como desvio: ESTRUTURADO se a diferença prevista
    entre PI e SC for de 20 x (coef PI menos coef SC) = 1,80 ponto ou mais a mais de 3 ep, com 15 UFs; UNIFORME se
    for menor que 8 x 0,090 = 0,72 em módulo com ep até 4 x 0,090 = 0,36. O veredito da Parte A é o do coeficiente;
    este vai ao lado.

Calibração por efeito plantado (obrigatória) e regra do SEM PODER
P15. Irregularidade plantada, forma pura: "todo o erro nacional regulado pela força local". kappa = 2,70 (erro médio
    de Lula no 2º turno das 11 pesquisas nacionais, L5(a), conhecido antes) dividido pela média ponderada dos
    coeficientes do T16 (0,04572) = 59,05 pontos por unidade (PI 5,65 pontos; SC 0,34). Ao lado, o plantado no
    limiar (20) e o uniforme (0).
P16. Plantio nos dados de 2026: tiro dos erros observados por UF a reta ajustada (ficam a média e os resíduos reais),
    somo a reta plantada (inclinação 0, 20 ou kappa) e permuto os resíduos entre as UFs (10.000 permutações, semente
    20261110). Para cada plantio: fração das permutações em que a letra dá ESTRUTURADO e em que dá UNIFORME.
    REGRA: se o plantado puro (kappa) não der ESTRUTURADO em pelo menos 80% das permutações, o teste não enxerga o
    plantado e o veredito da Parte A é SEM PODER, salvo se a letra der ESTRUTURADO nos dados reais (um positivo com
    pouco poder continua sendo relatado como sinal, com esse aviso). O UNIFORME pela letra exige ep <= 4, que por si
    garante poder (20 / 4 = 5 ep).
    Ao lado (poder do desenho a priori, sem usar os resíduos): simulação com as pesquisas reais incluídas
    (instituto, UF, amostra), erro de cada pesquisa = erro plantado da UF + viés de casa do instituto (dp 1,0) +
    erro não amostral da pesquisa (dp 1,5) + erro amostral binomial com efeito de desenho 1,5; cenários "só
    amostral" (0; 0; 1,0) e "pessimista" (1,5; 2,5; 2,0). 10.000 sorteios, semente 20261110.
P17. Explicação inocente plantada: subamostragem do interior. Para cada UF, com os votos reais do 2º turno por
    município, calculo a fatia de Lula que uma pesquisa mediria se os municípios com menos de 50 mil aptos pesassem
    (1 - u) do que pesam, com u = 10%, 20% e 30%: (i) só nas 9 UFs do Nordeste, (ii) em todas as UFs. O erro
    plantado é urna menos essa fatia. Relato a inclinação que isso produz contra o coeficiente nas UFs incluídas,
    o u que produziria a inclinação de 20 e a observada, e se o teste chamaria esse plantio de ESTRUTURADO (mesma
    permutação de resíduos). Ao lado, a mesma conta com capital contra o resto. Se a explicação inocente plantada
    der ESTRUTURADO, fica dito que o teste não separa desvio regulado pela força local de subamostragem do interior.

Teste espelho
P18. E1, espelho no 1º turno ("onde não deveria dar nada", porque a suspeita é sobre a virada do 2º turno e no
    1º turno as pesquisas nacionais acertaram Lula, erro médio -0,05): mesmas regras P1 a P7 deslocadas para o
    1º turno (último dia de campo de 27/09 a 03/10/2026; cenário estimulado; fatia de Lula nos válidos = Lula sobre a
    soma dos candidatos; mesmos institutos que entram na UF no 2º turno quando houver, senão qualquer instituto que
    cumpra P3 pelo 2º turno), erro = urna do 1º turno (Lula sobre válidos sem o 28) menos média das pesquisas, e a
    mesma regressão contra o mesmo coeficiente do T16. Leitura fixada: se a inclinação do 1º turno for de 20 ou mais
    a mais de 3 ep, ou se a diferença (inclinação do 2º turno menos a do 1º, nas UFs comuns) ficar abaixo de 2 ep
    da diferença, a estrutura é das pesquisas e não da contagem do 2º turno. Só vale com 10 UFs ou mais; com menos,
    "espelho sem dados". A coleta do 1º turno é feita depois da do 2º e pode ficar incompleta; isso é dito.
P19. E2, espelho por candidato: nos válidos, erro de Flávio = menos erro de Lula, então a conta espelhada é a mesma
    regressão contra o coeficiente espelho (o de "votos de Lula no 1º turno" na regressão do ganho de Flávio, mesma
    especificação do T16, calculado aqui por UF com scripts/lib.py). Espelho ESTRUTURADO se o erro de Flávio subir 20
    pontos ou mais por unidade do coeficiente espelho a mais de 3 ep. Aviso dito antes: os dois coeficientes são
    correlacionados entre as UFs, então este espelho não é independente do teste; a correlação é relatada.

Tradução em votos de margem
P20. Parte uniforme: erro médio (ponderado pelos válidos das UFs incluídas) vezes os válidos do país = votos de Lula
    acima das pesquisas; margem = 2 vezes isso. Parte estruturada: soma, nas 27 UFs, de inclinação x (coef da UF
    menos o menor coef) x válidos da UF / 100 = votos de Lula que a reta atribui à força local acima do nível da UF
    de menor coeficiente; margem = 2 vezes. O mesmo para a inclinação do limiar (20) e para os limites de 95%.
    Tudo ao lado da margem oficial de 4.430.191.

PARTE B: RECORTE POR REGIÃO DAS PESQUISAS NACIONAIS (o registro pede "somar", sem critério numérico)
B1. Pesquisas: a última rodada nacional de 2º turno de cada instituto do L5 (os 11 mais Ipespe) com último dia de
    campo de 18 a 24/10/2026, que tenha publicado Lula e Flávio por região. Fatia de Lula nos válidos da região =
    Lula / (Lula + Flávio) do recorte (ou os válidos, se publicados). Regiões como o instituto as define (por
    exemplo Norte e Centro-Oeste juntos); urna = soma das UFs da região na base por seção. Nível de fonte como em P6;
    na Parte B entram "conferida" e "tabela ou trecho", marcados, porque são poucos institutos.
B2. Estatística: por instituto, D = erro no Nordeste menos erro no Sul (erro = urna menos pesquisa, Lula, válidos).
    Média dos D entre institutos; ep pela dispersão entre institutos (dp / raiz de k); ao lado, o ep amostral com a
    subamostra publicada ou estimada (amostra x fatia da região no eleitorado, efeito de desenho 1).
B3. Critério, traduzido da letra e dito como desvio: delta_c = média dos coeficientes do T16 do Nordeste menos a do
    Sul, ponderadas pelos válidos do 2º turno. inclinação_B = D médio / delta_c, ep_B = ep / delta_c. ESTRUTURADO se
    inclinação_B >= 20 a mais de 3 ep, com 3 institutos ou mais (no lugar das 15 UFs). UNIFORME se |inclinação_B| < 8
    com ep_B <= 4. Fora disso INCONCLUSIVO. SEM PODER se, com o ep observado, o plantado puro (D = kappa x delta_c)
    tiver menos de 80% de chance de dar ESTRUTURADO (aproximação normal), salvo ESTRUTURADO nos dados reais; ou se
    houver menos de 3 institutos.
B4. Ao lado: o erro em todas as regiões de cada instituto; a inclinação entre regiões com efeito fixo de instituto;
    o contraste espelho Sudeste menos Centro-Oeste/Norte (regiões de coeficiente médio parecido, onde a forma
    regulada pela força local prevê pouco); o mesmo D no 1º turno para os institutos que publicaram o recorte
    (espelho no tempo), se achado; e a explicação inocente plantada de P17 agregada por região.

O QUE CADA RESULTADO SIGNIFICARIA (fixado antes)
  - UNIFORME: o erro das pesquisas é igual onde Lula é forte e onde é fraco. Combina com virada nacional de última
    hora (ou erro comum das pesquisas) e também com um desvio uniforme na contagem; não combina com desvio regulado
    pela força local. Não separa as duas primeiras.
  - ESTRUTURADO: o erro cresce com o coeficiente. Combina com desvio regulado pela força local de Lula e também com
    subamostragem do interior do Nordeste (P17) e com mobilização maior onde Lula é forte. É indício a cruzar, não
    veredito. O espelho do 1º turno (P18) é o que pode separar "defeito das pesquisas" de "algo do 2º turno".
  - Pesquisa não passa pela urna, mas também não é contagem: um erro de pesquisa, com qualquer forma, não prova
    alteração de voto. O teste diz qual forma procurar.

CONTAGEM DE TESTES
  Vereditos com limiar neste arquivo: Parte A (coeficiente), Parte A ao lado (fatia de Lula) e Parte B. Com limiar
  de 3 ep unilateral, a chance de um ESTRUTURADO por acaso em cada um é de cerca de 0,1%; os três não são
  independentes.

ACRÉSCIMO AO DOCSTRING (10/11/2026, 14h41 UTC), ESCRITO DEPOIS DAS BUSCAS DO 2º TURNO NAS 27 UFs E ANTES DE
LEVANTAR AS PESQUISAS ESTADUAIS DO 1º TURNO, OS RECORTES POR REGIÃO E DE CALCULAR QUALQUER ERRO
  O que as buscas mostraram: pesquisa estadual de presidente com campo terminado de 18 a 24/10 só apareceu nas 6 UFs
  com 2º turno de governador (AtlasIntel em AC, AM, DF, ES, RN e TO; Paraná Pesquisas no TO; Quaest no DF). Nas
  outras 21 UFs as buscas só devolveram pesquisas estaduais anteriores ao 1º turno. Pela letra e por P13, com 6 UFs
  não há regressão: a Parte A registrada tende a SEM PODER por falta de pesquisas. A parte abaixo é EXPLORATÓRIA
  (decidida depois de ver quantas pesquisas existem, antes de ver os números dela) e não muda o veredito pela letra.
  Números que eu já tinha visto de passagem nos resumos das buscas, sem conta: cenários de 2º turno anteriores ao
  1º turno em PE (Real Time, Lula 60 ou 61 a 35, e a urna 69,2%), PR (Real Time 67 a 33 nos válidos), CE, SC, MG, DF,
  SE, AL, PI, PA, PB, AP, GO e RS (números soltos de datas variadas), e resultados oficiais aproximados de algumas
  UFs citados pelo buscador.
X1. Dados: as pesquisas estaduais do espelho E1 (P18): pesquisa estadual de presidente com último dia de campo de
    27/09 a 03/10/2026, uma por instituto e por UF (a mais recente), fonte "conferida" na principal. De cada uma
    saem dois números: L1 = fatia de Lula nos válidos do cenário estimulado do 1º turno (válidos publicados, ou
    Lula / (100 menos branco, nulo e indecisos)); L2 = Lula / (Lula + Flávio) do cenário de 2º turno perguntado
    na mesma pesquisa. Sensibilidade: janela larga, último dia de campo de 20/09 a 03/10.
X2. Três erros por UF (média simples entre institutos): e1 = urna do 1º turno menos L1 (é o espelho E1);
    e2 = urna do 2º turno menos L2 (o cenário de 2º turno foi perguntado cerca de 4 semanas antes: mistura erro de
    pesquisa com mudança real de opinião); DD = e2 menos e1 (o que a urna andou a favor de Lula entre os turnos além
    do que a própria pesquisa previa de um cenário para o outro; a mesma amostra serve de controle de si mesma, o que
    tira subamostragem do interior e viés de casa que valham igual nas duas perguntas).
X3. Regressões de e1, e2 e DD contra o coeficiente do T16 e contra a fatia de Lula no 1º turno, com P12 (MQO por UF,
    ep clássico; ao lado HC3, efeito fixo de instituto no nível da pesquisa, e só Real Time ou só Quaest se algum
    deles cobrir 10 UFs ou mais). Os limiares da letra (20 a mais de 3 ep com 15 UFs; menor que 8 com ep até 4) são
    aplicados e relatados como "leitura exploratória", com a calibração P16 e a explicação inocente P17 calculadas
    também para a fatia do 1º turno.
X4. Aviso dito antes: o coeficiente do T16 é calculado com a própria urna (ganho de Lula entre os turnos contra os
    votos de Flávio no 1º turno), então UF em que Lula ganhou mais entre os turnos tende a ter coeficiente e DD
    maiores juntos. Uma inclinação positiva de DD diz que as pesquisas feitas antes do 1º turno não previam o
    desenho por UF do ganho de Lula; não diz por quê. Uma inclinação perto de zero diz que os próprios eleitores
    já declaravam, antes, o desenho que a urna mostrou.

Uso: python3 -I scripts/analisar_R27_L5.py   (lê resultados/R27_L5_coleta_pesquisas.json, a coleta com fontes;
     grava resultados/R27_L5_pesquisas_estaduais.json e .txt)
"""
import os as _os, sys as _sys
_AQUI = _os.path.dirname(_os.path.abspath(__file__))
_sys.path.insert(0, _AQUI)
import gzip, hashlib, itertools, json, math, time
import numpy as np
from lib import carregar, chave_local, fe_ols

RAIZ = _os.path.dirname(_AQUI)
DADOS = _os.path.join(RAIZ, 'dados')
RES = _os.path.join(RAIZ, 'resultados')
COLETA = _os.path.join(RES, 'R27_L5_coleta_pesquisas.json')
SAIDA_JSON = _os.path.join(RES, 'R27_L5_pesquisas_estaduais.json')
SAIDA_TXT = _os.path.join(RES, 'R27_L5_pesquisas_estaduais.txt')
SEMENTE = 20261110
NPERM = 10000
MARGEM = 4430191
ERRO_NACIONAL_L5A = 2.70          # erro médio de Lula no 2º turno, 11 pesquisas nacionais (L5a), conhecido antes
LIM_ESTR, LIM_UNIF, EP_UNIF, MIN_UFS, MIN_REG = 20.0, 8.0, 4.0, 15, 8
JANELA_2T = ('2026-10-18', '2026-10-24')
JANELA_1T = ('2026-09-27', '2026-10-03')
JANELA_1T_LARGA = ('2026-09-20', '2026-10-03')
GRUPOS = ['70', '14', '55', '30']    # Cury, Renan, Caiado, Zema, como no T16
REGIOES = {'NE': ['AL', 'BA', 'CE', 'MA', 'PB', 'PE', 'PI', 'RN', 'SE'], 'S': ['PR', 'RS', 'SC'],
           'SE': ['ES', 'MG', 'RJ', 'SP'], 'N': ['AC', 'AM', 'AP', 'PA', 'RO', 'RR', 'TO'], 'CO': ['DF', 'GO', 'MS', 'MT']}
REGIOES['N+CO'] = REGIOES['N'] + REGIOES['CO']
UFS = sorted(u for r in ('NE', 'S', 'SE', 'N', 'CO') for u in REGIOES[r])
LINHAS = []


def P(*a):
    s = ' '.join(str(x) for x in a)
    LINHAS.append(s)
    print(s)


def f(x, d=2):
    """Número com vírgula decimal."""
    if x is None or (isinstance(x, float) and (math.isnan(x) or math.isinf(x))):
        return 'n/d'
    return f'{x:.{d}f}'.replace('.', ',')


def mil(x):
    return f'{int(round(x)):,}'.replace(',', '.')


# ---------------------------------------------------------------- dados da urna
def ler_urna():
    d = carregar(_os.path.join(DADOS, 'secoes2026.json.gz'))
    with gzip.open(_os.path.join(DADOS, 'candidatos2026_1t.json.gz'), 'rt') as fh:
        cand = json.load(fh)['secoes']
    uf = {u: dict(L1=0, R1=0, O1=0, v28=0, L2=0, R2=0, comp2=0) for u in UFS}
    mun = {}                      # (uf, mun) -> [aptos2, L2, R2, L1, valid1]
    reg = {u: [] for u in UFS}    # linhas para a regressão do coeficiente
    for k, v in d.items():
        u, m = k.split('|')[:2]
        if u not in uf:
            continue
        a, b = v.get('1'), v.get('2')
        cv = cand.get(k, {})
        mm = mun.setdefault((u, m), [0, 0, 0, 0, 0])
        if a:
            x28 = cv.get('28', 0)
            uf[u]['L1'] += a['L']; uf[u]['R1'] += a['R']; uf[u]['O1'] += a['O']; uf[u]['v28'] += x28
            mm[3] += a['L']; mm[4] += a['L'] + a['R'] + a['O'] - x28
        if b:
            uf[u]['L2'] += b['L']; uf[u]['R2'] += b['R']; uf[u]['comp2'] += b['comp']
            mm[0] += b['apt']; mm[1] += b['L']; mm[2] += b['R']
        if a and b:
            g = [cv.get(n, 0) for n in GRUPOS]
            reg[u].append((chave_local(k, b), b['L'] - a['L'], b['R'] - a['R'], g[0], g[1], g[2], g[3], a['O'] - sum(g),
                           (a['B'] + a['N']) - (b['B'] + b['N']), b['comp'] - a['comp'], a['L'], a['R']))
    return uf, mun, reg


def coeficientes(reg):
    """Coeficiente do T16 (Lula: ganho de Lula contra votos de Flávio no 1T) e o espelho (Flávio contra Lula), por UF."""
    nomes = ['Cury', 'Renan', 'Caiado', 'Zema', 'demais', 'queda_bn', 'var_comp', 'adversario_1T', 'proprio_1T']
    out = {}
    for u in UFS:
        loc = np.array([r[0] for r in reg[u]])
        A = np.array([r[1:] for r in reg[u]], float)
        comuns = A[:, 2:9]
        XL = np.column_stack([comuns, A[:, 10], A[:, 9]])    # Lula: adversário = Flávio 1T, próprio = Lula 1T
        XR = np.column_stack([comuns, A[:, 9], A[:, 10]])    # Flávio: adversário = Lula 1T, próprio = Flávio 1T
        rl = fe_ols(A[:, 0], XL, loc, None, nomes)
        rr = fe_ols(A[:, 1], XR, loc, None, nomes)
        out[u] = dict(coef_L=rl['coef']['adversario_1T'], ep_L=rl['ep']['adversario_1T'],
                      coef_espelho=rr['coef']['adversario_1T'], ep_espelho=rr['ep']['adversario_1T'], secoes=len(loc))
    return out


# ---------------------------------------------------------------- estatística
def ols(x, y, w=None):
    x = np.asarray(x, float); y = np.asarray(y, float); n = len(x)
    w = np.ones(n) if w is None else np.asarray(w, float)
    X = np.column_stack([np.ones(n), x]); W = np.diag(w)
    XtWX = X.T @ W @ X
    if n < 3 or abs(np.linalg.det(XtWX)) < 1e-18:
        return dict(n=n, a=float('nan'), b=float('nan'), ep=float('nan'), ep_hc3=float('nan'), t=float('nan'), r2=float('nan'))
    inv = np.linalg.inv(XtWX)
    beta = inv @ X.T @ W @ y
    e = y - X @ beta
    s2 = float((w * e * e).sum() / (n - 2))
    V = inv * s2
    H = np.einsum('ij,jk,ik->i', X * np.sqrt(w)[:, None], inv, X * np.sqrt(w)[:, None])
    u = (w * e) / np.clip(1 - H, 1e-9, None)
    Vh = inv @ (X.T @ np.diag(u * u) @ X) @ inv
    ym = float((w * y).sum() / w.sum())
    sst = float((w * (y - ym) ** 2).sum())
    return dict(n=n, a=float(beta[0]), b=float(beta[1]), ep=float(math.sqrt(V[1, 1])), ep_hc3=float(math.sqrt(Vh[1, 1])),
                t=float(beta[1] / math.sqrt(V[1, 1])) if V[1, 1] > 0 else float('nan'),
                r2=float(1 - (w * e * e).sum() / sst) if sst > 0 else float('nan'), residuos=[float(v) for v in e])


def letra(b, ep, n, lim_s=LIM_ESTR, lim_u=LIM_UNIF, ep_u=EP_UNIF, min_n=MIN_UFS, exigir_n=True):
    if b is None or math.isnan(b) or math.isnan(ep):
        return 'SEM REGRESSÃO'
    if b >= lim_s and ep > 0 and b / ep > 3 and (n >= min_n or not exigir_n):
        return 'ESTRUTURADO'
    if abs(b) < lim_u and ep <= ep_u:
        return 'UNIFORME'
    return 'INCONCLUSIVO'


def phi(z):
    return 0.5 * (1 + math.erf(z / math.sqrt(2)))


def fatia_valida(p):
    """Fatia de Lula nos válidos de um registro da coleta (P4): publicado, senão dos totais."""
    if p.get('lula_validos') is not None:
        return float(p['lula_validos'])
    return 100.0 * p['lula_total'] / (p['lula_total'] + p['flavio_total'])


def fatia_dos_totais(p):
    if p.get('lula_total') is not None and p.get('flavio_total') is not None:
        return 100.0 * p['lula_total'] / (p['lula_total'] + p['flavio_total'])
    return fatia_valida(p)


def uma_por_instituto(pesqs):
    """P5: por UF e instituto, a de último dia de campo mais recente; empate, a de maior amostra."""
    melhor = {}
    for p in pesqs:
        k = (p['uf'], p['instituto'])
        c = (p['campo_fim'], p.get('amostra') or 0)
        if k not in melhor or c > melhor[k][0]:
            melhor[k] = (c, p)
    return [v[1] for v in melhor.values()]


def erros_por_uf(pesqs, urna2, fn=fatia_valida):
    por = {}
    for p in pesqs:
        por.setdefault(p['uf'], []).append(p)
    out = {}
    for u, lst in sorted(por.items()):
        vals = [fn(p) for p in lst]
        ns = [p.get('amostra') or 1000 for p in lst]
        media = float(np.mean(vals))
        var_am = sum((v / 100) * (1 - v / 100) / n for v, n in zip(vals, ns)) / len(vals) ** 2 * 1e4
        out[u] = dict(urna=urna2[u], media=media, mediana=float(np.median(vals)),
                      media_pond_amostra=float(np.average(vals, weights=ns)), n_pesquisas=len(lst),
                      institutos=[p['instituto'] for p in lst], erro=urna2[u] - media,
                      erro_mediana=urna2[u] - float(np.median(vals)), ep_amostral=math.sqrt(var_am),
                      pesquisas=[dict(id=p.get('id'), instituto=p['instituto'], fatia=fn(p), erro=urna2[u] - fn(p),
                                      amostra=p.get('amostra')) for p in lst])
    return out


def permutacao_plantio(x, y, inclinacoes, rng, exigir_n=True):
    """P16: tira a reta ajustada, soma a plantada e permuta os resíduos."""
    x = np.asarray(x, float); y = np.asarray(y, float); n = len(x)
    r = ols(x, y)
    res = np.array(r['residuos']); media = float(y.mean()); xc = x - x.mean()
    if n <= 7:
        perms = [np.array(p) for p in itertools.permutations(range(n))]
    else:
        perms = [rng.permutation(n) for _ in range(NPERM)]
    out = {}
    for nome, b0 in inclinacoes.items():
        ce = cu = 0; bs = []; eps = []
        for pm in perms:
            yy = media + b0 * xc + res[pm]
            rr = ols(x, yy)
            v = letra(rr['b'], rr['ep'], n, exigir_n=exigir_n)
            ce += v == 'ESTRUTURADO'; cu += v == 'UNIFORME'; bs.append(rr['b']); eps.append(rr['ep'])
        out[nome] = dict(plantado=b0, permutacoes=len(perms), frac_estruturado=ce / len(perms), frac_uniforme=cu / len(perms),
                         inclinacao_media=float(np.mean(bs)), ep_medio=float(np.mean(eps)))
    return out


def simular_desenho(desenho, coef, urna, planos, cenarios, rng, nsim=10000):
    """Poder a priori: desenho = lista de (uf, instituto, amostra)."""
    ufs = sorted({d[0] for d in desenho}); x = np.array([coef[u] for u in ufs]); n = len(ufs)
    insts = sorted({d[1] for d in desenho}); ii = {k: i for i, k in enumerate(insts)}
    iu = {u: i for i, u in enumerate(ufs)}
    pu = np.array([urna[d[0]] / 100 for d in desenho]); nn = np.array([d[2] or 1000 for d in desenho], float)
    idx_u = np.array([iu[d[0]] for d in desenho]); idx_i = np.array([ii[d[1]] for d in desenho])
    cont = np.bincount(idx_u, minlength=n).astype(float)
    xc = x - x.mean(); sxx = float((xc ** 2).sum())
    out = {}
    for cn, (sh, sg, deff) in cenarios.items():
        H = rng.standard_normal((nsim, len(insts))) * sh
        G = rng.standard_normal((nsim, len(desenho))) * sg
        S = rng.standard_normal((nsim, len(desenho))) * np.sqrt(deff * pu * (1 - pu) / nn) * 100
        ruido = -(H[:, idx_i] + G + S)                       # erro = urna - pesquisa
        ru = np.zeros((nsim, n))
        for j in range(len(desenho)):
            ru[:, idx_u[j]] += ruido[:, j]
        ru /= cont
        out[cn] = {}
        for pn, b0 in planos.items():
            Y = ERRO_NACIONAL_L5A + b0 * xc + ru
            b = (Y * xc).sum(1) / sxx
            a = Y.mean(1)
            E = Y - a[:, None] - b[:, None] * xc
            ep = np.sqrt((E ** 2).sum(1) / (n - 2) / sxx)
            estr = (b >= LIM_ESTR) & (b / ep > 3) & (n >= MIN_UFS)
            unif = (np.abs(b) < LIM_UNIF) & (ep <= EP_UNIF)
            out[cn][pn] = dict(plantado=b0, frac_estruturado=float(estr.mean()), frac_uniforme=float(unif.mean()),
                               ep_medio=float(ep.mean()), dp_da_inclinacao=float(b.std()))
    return out


def subamostragem(mun, ufs_alvo, u, turno=2, criterio='pequenos', capitais=None):
    """P17: erro (urna menos pesquisa) por UF se os municípios pequenos (ou o interior) pesassem (1-u) nas UFs alvo."""
    out = {}
    for uf in UFS:
        g = h = gp = hp = 0.0
        for (uu, m), v in mun.items():
            if uu != uf:
                continue
            num, den = (v[1], v[1] + v[2]) if turno == 2 else (v[3], v[4])
            peq = (v[0] < 50000) if criterio == 'pequenos' else (capitais is not None and int(m) != capitais[uf])
            if peq:
                gp += num; hp += den
            else:
                g += num; h += den
        real = (g + gp) / (h + hp)
        k = (1 - u) if uf in ufs_alvo else 1.0
        pesq = (g + k * gp) / (h + k * hp)
        out[uf] = dict(erro=100 * (real - pesq), peso_pequenos=hp / (h + hp),
                       lula_pequenos=100 * gp / hp if hp else None, lula_grandes=100 * g / h if h else None)
    return out


def dentro(p, jan):
    return jan[0] <= p['campo_fim'] <= jan[1]


# ---------------------------------------------------------------- principal
def main():
    t0 = time.time()
    rng = np.random.default_rng(SEMENTE)
    doc_sha = hashlib.sha256(__doc__.encode('utf-8')).hexdigest()
    coleta = json.load(open(COLETA, encoding='utf-8'))
    t16 = json.load(open(_os.path.join(RES, 'T16_bweb.json'), encoding='utf-8'))
    coef = {u: t16['2026']['com_grupos_principal']['por_UF'][u]['coef'] for u in UFS}
    coef_sg = {u: t16['2026']['sem_grupos_comparavel']['por_UF'][u]['coef'] for u in UFS}
    capitais = t16['capitais_codigo_TSE']
    cbar = t16['2026']['com_grupos_principal']['media_ponderada_UFs']
    kappa = ERRO_NACIONAL_L5A / cbar
    uf, mun, reg = ler_urna()
    cf = coeficientes(reg)
    dif_max = max(abs(cf[u]['coef_L'] - coef[u]) for u in UFS)
    urna2 = {u: 100 * uf[u]['L2'] / (uf[u]['L2'] + uf[u]['R2']) for u in UFS}
    val2 = {u: uf[u]['L2'] + uf[u]['R2'] for u in UFS}
    val1 = {u: uf[u]['L1'] + uf[u]['R1'] + uf[u]['O1'] - uf[u]['v28'] for u in UFS}
    urna1 = {u: 100 * uf[u]['L1'] / val1[u] for u in UFS}
    VAL2 = sum(val2.values()); L2T = sum(uf[u]['L2'] for u in UFS); R2T = sum(uf[u]['R2'] for u in UFS)
    cesp = {u: cf[u]['coef_espelho'] for u in UFS}
    R = dict(teste='R27_L5: erro das pesquisas estaduais por UF e recorte por região', sha256_docstring=doc_sha, semente=SEMENTE,
             registro='PRE-REGISTRO-2026-10-26.md, Adendo 27 (commit 2748895), Adendo 28 (938be19) e Adendo 30 (a7218fb); '
                      'fragilidade "L5(a), F13 e F17" de registro/adendo27/equipe_vermelha_relatorio.json',
             conferencias={}, coleta=coleta)

    P('R27_L5 (Adendo 27, Onda D-c; Adendo 30, última onda): ERRO DAS PESQUISAS ESTADUAIS POR UF E RECORTE POR REGIÃO')
    P('Script: scripts/analisar_R27_L5.py. Coleta com fontes: resultados/R27_L5_coleta_pesquisas.json. Números: resultados/R27_L5_pesquisas_estaduais.json.')
    P(f'SHA-256 do docstring (regras): {doc_sha}')
    P('Aviso do Adendo 27: reteste escrito pela equipe vermelha, que já conhecia os resultados antigos; o critério é novo, a escolha do que')
    P('retestar é posterior ao dado. Regras de inclusão e de média fixadas no docstring antes da coleta (14h35 UTC de 10/11) e o acréscimo')
    P('exploratório antes de levantar as pesquisas do 1º turno (14h41 UTC). Nenhum outro ano serve de régua neste teste.')
    P('')
    P('CRITÉRIO PELA LETRA (equipe_vermelha_relatorio.json)')
    P('  ERRO ESTRUTURADO (indício a cruzar): inclinação de 20 pontos ou mais por unidade de coeficiente a mais de 3 ep, com 15 UFs ou mais.')
    P('  ERRO UNIFORME: |inclinação| abaixo de 8 com ep até 4. "Não dá veredito de fraude sozinho: diz qual forma procurar."')
    P('')
    P('0. CONFERÊNCIAS DA BASE')
    P(f'  Urna do 2º turno sem o exterior: Lula {mil(L2T)}, Flávio {mil(R2T)}, válidos {mil(VAL2)}; Lula {f(100 * L2T / VAL2, 3)}% dos válidos.')
    P(f'  Coeficiente do T16 refeito aqui por UF (mesma regressão): maior diferença contra resultados/T16_bweb.json = {dif_max:.2e}.')
    cc = float(np.corrcoef([coef[u] for u in UFS], [cesp[u] for u in UFS])[0, 1])
    c1 = float(np.corrcoef([coef[u] for u in UFS], [urna1[u] for u in UFS])[0, 1])
    P(f'  Coeficiente espelho (votos de Lula no 1º turno no ganho de Flávio), calculado aqui: correlação com o do T16 entre as 27 UFs = {f(cc, 3)}.')
    P(f'  Correlação do coeficiente do T16 com a fatia de Lula no 1º turno: {f(c1, 3)}. kappa (forma pura) = 2,70 / {f(cbar, 5)} = {f(kappa, 2)} pontos por unidade.')
    R['conferencias'] = dict(lula_2T=L2T, flavio_2T=R2T, validos_2T=VAL2, dif_max_coef_T16=dif_max, corr_coef_espelho=cc,
                             corr_coef_fatia_lula_1T=c1, kappa=kappa, media_ponderada_coef=cbar)
    R['por_UF_base'] = {u: dict(coef_T16=coef[u], coef_sem_grupos=coef_sg[u], coef_espelho=cesp[u], ep_espelho=cf[u]['ep_espelho'],
                                lula_2T_validos=urna2[u], lula_1T_validos=urna1[u], validos_2T=val2[u], validos_1T=val1[u]) for u in UFS}

    # ============================================================ PARTE A
    P('')
    P('1. PARTE A: PESQUISAS ESTADUAIS DE PRESIDENTE NO 2º TURNO, JANELA DE 18 A 24/10/2026')
    todas = coleta['parte_A_segundo_turno']
    conj = {
        'principal': [p for p in todas if dentro(p, JANELA_2T) and p['nivel'] == 'conferida' and p.get('historico_1T')],
        'S1_campo_inteiro_na_janela': [p for p in todas if dentro(p, JANELA_2T) and p['campo_inicio'] >= JANELA_2T[0]
                                       and p['nivel'] == 'conferida' and p.get('historico_1T')],
        'S3_todas_da_janela': [p for p in todas if dentro(p, JANELA_2T) and p['nivel'] == 'conferida'],
        'S5_com_trecho_e_tabela': [p for p in todas if dentro(p, JANELA_2T) and p.get('historico_1T')],
    }
    P('  O que existe: as buscas das 27 UFs só acharam pesquisa estadual de presidente na janela nas 6 UFs com 2º turno de governador.')
    fat6 = sum(val2[u] for u in {p['uf'] for p in todas}) / VAL2
    P(f'  Nas outras 21 UFs ({f(100 * (1 - fat6), 1)}% dos válidos do país) não achei nenhuma. Lista do que entrou e do que ficou de fora no JSON da coleta.')
    P('  pesquisa                      | campo        | amostra | Lula válidos | urna   | erro (urna menos pesquisa) | fonte')
    for p in sorted(todas, key=lambda q: (q['uf'], q['instituto'])):
        fv = fatia_valida(p)
        nota = '' if p.get('historico_1T') else ' [sem histórico de 1º turno comprovado: fora da principal]'
        P(f"  {p['uf']} {p['instituto']:<26} | {p['campo_inicio'][8:]}/10 a {p['campo_fim'][8:]}/10 | {str(p.get('amostra') or 'n/p'):>7} |"
          f" {f(fv):>12} | {f(urna2[p['uf']]):>6} | {f(urna2[p['uf']] - fv):>8} | {p['nivel']}{nota}")
    RA = {}
    for nome, lst in conj.items():
        sel = uma_por_instituto(lst)
        e = erros_por_uf(sel, urna2)
        ufs_a = sorted(e)
        x = [coef[u] for u in ufs_a]; y = [e[u]['erro'] for u in ufs_a]
        w = [val2[u] for u in ufs_a]
        r = ols(x, y) if len(ufs_a) >= 3 else dict(n=len(ufs_a), b=float('nan'), ep=float('nan'), ep_hc3=float('nan'), t=float('nan'), r2=float('nan'), a=float('nan'))
        r2 = ols([urna1[u] for u in ufs_a], y) if len(ufs_a) >= 3 else None
        RA[nome] = dict(n_UFs=len(ufs_a), n_pesquisas=len(sel), UFs=ufs_a, por_UF=e,
                        erro_medio_simples=float(np.mean(y)), dp_entre_UFs=float(np.std(y, ddof=1)) if len(y) > 1 else None,
                        ep_do_erro_medio=float(np.std(y, ddof=1) / math.sqrt(len(y))) if len(y) > 1 else None,
                        erro_medio_ponderado_validos=float(np.average(y, weights=w)),
                        fatia_dos_validos_do_pais=sum(w) / VAL2,
                        regressao_descritiva_coef={k: v for k, v in r.items() if k != 'residuos'},
                        regressao_descritiva_fatia_lula_1T={k: v for k, v in r2.items() if k != 'residuos'} if r2 else None,
                        veredito_pela_letra=('SEM PODER (menos de 8 UFs: sem regressão, P13)' if len(ufs_a) < MIN_REG
                                             else letra(r['b'], r['ep'], len(ufs_a))))
    A = RA['principal']
    P('')
    P(f"  Análise principal (conferidas, uma por instituto e UF, instituto com pesquisa de presidente no 1º turno): {A['n_pesquisas']} pesquisas em {A['n_UFs']} UFs")
    P(f"  ({f(100 * A['fatia_dos_validos_do_pais'], 1)}% dos válidos do país).")
    P('  UF | coef T16 | Lula 1T | urna 2T | média das pesquisas (n) | erro   | ep amostral | institutos')
    for u in A['UFs']:
        q = A['por_UF'][u]
        P(f"  {u} | {coef[u]:+.4f}  | {f(urna1[u]):>7} | {f(q['urna']):>7} | {f(q['media']):>6} ({q['n_pesquisas']})              | {f(q['erro']):>6} |"
          f" {f(q['ep_amostral']):>5}       | {', '.join(q['institutos'])}")
    P(f"  Erro médio de Lula nas {A['n_UFs']} UFs: {f(A['erro_medio_simples'])} pontos (dp entre UFs {f(A['dp_entre_UFs'])}; ep {f(A['ep_do_erro_medio'])});"
      f" ponderado pelos válidos: {f(A['erro_medio_ponderado_validos'])}.")
    P(f"  Para comparar: as 11 pesquisas nacionais finais erraram Lula em +2,70 (L5a).")
    rd = A['regressao_descritiva_coef']
    P(f"  VEREDITO PELA LETRA (Parte A, coeficiente): {A['veredito_pela_letra']}.")
    P(f"    A letra exige 15 UFs para ESTRUTURADO; há {A['n_UFs']}. Com menos de 8 UFs não há regressão (P13).")
    P(f"    Só descritivo, sem veredito: reta pelos {A['n_UFs']} pontos = {f(rd['b'], 1)} pontos por unidade de coeficiente (ep {f(rd['ep'], 1)}; HC3 {f(rd['ep_hc3'], 1)});")
    r2d = A['regressao_descritiva_fatia_lula_1T']
    P(f"    contra a fatia de Lula no 1º turno: {f(r2d['b'], 3)} ponto de erro por ponto de fatia (ep {f(r2d['ep'], 3)}). Nenhum dos dois decide nada com 6 pontos.")
    P('  Sensibilidades (mesma conta):')
    for nome in ('S1_campo_inteiro_na_janela', 'S3_todas_da_janela', 'S5_com_trecho_e_tabela'):
        q = RA[nome]; rr = q['regressao_descritiva_coef']
        P(f"    {nome}: {q['n_pesquisas']} pesquisas, {q['n_UFs']} UFs, erro médio {f(q['erro_medio_simples'])}, reta {f(rr['b'], 1)} (ep {f(rr['ep'], 1)}); veredito {q['veredito_pela_letra']}.")
    sel4 = uma_por_instituto(conj['principal']); e4 = erros_por_uf(sel4, urna2, fatia_dos_totais)
    RA['S4_validos_pelos_totais'] = dict(erro_medio_simples=float(np.mean([e4[u]['erro'] for u in e4])), por_UF={u: e4[u]['erro'] for u in e4})
    P(f"    S4_validos_pelos_totais: erro médio {f(RA['S4_validos_pelos_totais']['erro_medio_simples'])}.")
    fora = coleta['parte_A_fora_da_janela_pos_1T']
    P('  Fora da janela, depois do 1º turno (só listadas): ' + '; '.join(
        f"{p['uf']} {p['instituto']} {p['campo']}: Lula {f(p['lula_validos'] if p.get('lula_validos') else 100 * p['lula_total'] / (p['lula_total'] + p['flavio_total']), 1)}"
        f" (urna {f(urna2[p['uf']], 1)}) [{p['nivel']}]" for p in fora) + '.')

    # calibração da Parte A
    P('')
    P('  1.1 Calibração por efeito plantado (P15 e P16)')
    xa = [coef[u] for u in A['UFs']]; ya = [A['por_UF'][u]['erro'] for u in A['UFs']]
    planos = {'uniforme_0': 0.0, 'limiar_20': LIM_ESTR, 'puro_kappa': kappa}
    cal_letra = permutacao_plantio(xa, ya, planos, rng, exigir_n=True)
    cal_sem_n = permutacao_plantio(xa, ya, planos, rng, exigir_n=False)
    P(f"    Plantio nos resíduos reais das {A['n_UFs']} UFs (todas as {cal_letra['puro_kappa']['permutacoes']} permutações):")
    for k in planos:
        P(f"      plantado {f(planos[k], 1):>6}: ESTRUTURADO pela letra em {f(100 * cal_letra[k]['frac_estruturado'], 1)}% (ignorando a exigência de 15 UFs: "
          f"{f(100 * cal_sem_n[k]['frac_estruturado'], 1)}%); UNIFORME em {f(100 * cal_letra[k]['frac_uniforme'], 1)}%; ep médio da reta {f(cal_letra[k]['ep_medio'], 1)}.")
    cen = {'so_amostral': (0.0, 0.0, 1.0), 'central': (1.0, 1.5, 1.5), 'pessimista': (1.5, 2.5, 2.0)}
    des_real = [(p['uf'], p['instituto'], p.get('amostra') or 1000) for p in uma_por_instituto(conj['principal'])]
    des_27 = [(u, 'instituto único', 1500) for u in UFS]
    des_27x3 = [(u, k, 1500) for u in UFS for k in ('A', 'B', 'C')]
    sim = {'desenho_real': simular_desenho(des_real, coef, urna2, planos, cen, rng),
           'hipotetico_27_UFs_1_pesquisa_de_1500': simular_desenho(des_27, coef, urna2, planos, cen, rng),
           'hipotetico_27_UFs_3_pesquisas_de_1500': simular_desenho(des_27x3, coef, urna2, planos, cen, rng)}
    P('    Poder do desenho a priori (simulação, 10.000 sorteios; viés de casa, erro não amostral e efeito de desenho do docstring):')
    for dn, dv in sim.items():
        for cn in cen:
            q = dv[cn]
            P(f"      {dn:<40} {cn:<11}: ep médio {f(q['puro_kappa']['ep_medio'], 1):>5}; plantado kappa vira ESTRUTURADO em {f(100 * q['puro_kappa']['frac_estruturado'], 1):>5}%;"
              f" plantado 20 em {f(100 * q['limiar_20']['frac_estruturado'], 1):>5}%; uniforme vira UNIFORME em {f(100 * q['uniforme_0']['frac_uniforme'], 1):>5}%;"
              f" falso ESTRUTURADO {f(100 * q['uniforme_0']['frac_estruturado'], 2)}%")
    P('    Leitura: com as 6 UFs que existem, o plantado puro nunca vira ESTRUTURADO pela letra. Mesmo com uma pesquisa de 1.500 em cada')
    P('    uma das 27 UFs o limiar de ep até 4 (UNIFORME) não seria alcançado no cenário central. O desenho da letra pede mais dado do que há.')
    R['parte_A'] = dict(conjuntos=RA, calibracao_permutacao_pela_letra=cal_letra, calibracao_permutacao_sem_exigir_15=cal_sem_n,
                        simulacao_desenho=sim, cenarios={k: dict(dp_vies_de_casa=v[0], dp_nao_amostral=v[1], efeito_de_desenho=v[2]) for k, v in cen.items()})

    # explicação inocente plantada
    P('')
    P('  1.2 Explicação inocente plantada (P17): subamostragem dos municípios com menos de 50 mil aptos')
    inoc = {}
    for alvo_nome, alvo in (('so_Nordeste', REGIOES['NE']), ('todas_as_UFs', UFS)):
        for crit in ('pequenos', 'interior'):
            for turno in (2, 1):
                for u_ in (0.10, 0.20, 0.30):
                    s = subamostragem(mun, alvo, u_, turno, crit, capitais)
                    r27 = ols([coef[u] for u in UFS], [s[u]['erro'] for u in UFS])
                    r6 = ols(xa, [s[u]['erro'] for u in A['UFs']])
                    inoc[f'{alvo_nome}|{crit}|T{turno}|u={u_:.2f}'] = dict(
                        inclinacao_27_UFs=r27['b'], inclinacao_UFs_incluidas=r6['b'],
                        erro_medio_27=float(np.mean([s[u]['erro'] for u in UFS])),
                        erro_nacional_pontos=sum(s[u]['erro'] * (val2[u] if turno == 2 else val1[u]) for u in UFS) / (VAL2 if turno == 2 else sum(val1.values())),
                        erro_NE=float(np.mean([s[u]['erro'] for u in REGIOES['NE']])), erro_S=float(np.mean([s[u]['erro'] for u in REGIOES['S']])),
                        por_UF={u: s[u]['erro'] for u in UFS})
    base = subamostragem(mun, UFS, 0.0, 2, 'pequenos', capitais)
    P('    Quanto os municípios pequenos pesam e quanto Lula tem neles (2º turno): ' + '; '.join(
        f"{u} {f(100 * base[u]['peso_pequenos'], 0)}% dos válidos, Lula {f(base[u]['lula_pequenos'], 1)} contra {f(base[u]['lula_grandes'], 1)}" for u in ('PI', 'MA', 'BA', 'CE', 'PE', 'SP', 'SC', 'PR', 'RS')) + '.')
    P('    cenário                               | u    | inclinação nas 27 UFs | erro médio NE | erro médio Sul | erro nacional (pontos)')
    for alvo_nome in ('so_Nordeste', 'todas_as_UFs'):
        for u_ in (0.10, 0.20, 0.30):
            q = inoc[f'{alvo_nome}|pequenos|T2|u={u_:.2f}']
            P(f"    {alvo_nome + ', municípios < 50 mil aptos':<37} | {f(u_, 2)} | {f(q['inclinacao_27_UFs'], 1):>8}              | {f(q['erro_NE']):>6}        | {f(q['erro_S']):>6}         | {f(q['erro_nacional_pontos'])}")
    q20 = {}
    for alvo_nome, alvo in (('so_Nordeste', REGIOES['NE']), ('todas_as_UFs', UFS)):
        lo, hi = 0.0, 0.95
        fn = lambda uu: ols([coef[u] for u in UFS], [subamostragem(mun, alvo, uu, 2, 'pequenos', capitais)[u]['erro'] for u in UFS])['b']
        if fn(hi) < LIM_ESTR:
            q20[alvo_nome] = None
        else:
            for _ in range(30):
                mid = (lo + hi) / 2
                if fn(mid) < LIM_ESTR: lo = mid
                else: hi = mid
            q20[alvo_nome] = hi
    P(f"    Subamostragem que produziria sozinha a inclinação de 20 nas 27 UFs: só no Nordeste u = {f(100 * q20['so_Nordeste'], 1) if q20['so_Nordeste'] else 'acima de 95'}%;"
      f" em todas as UFs u = {f(100 * q20['todas_as_UFs'], 1) if q20['todas_as_UFs'] else 'acima de 95'}%.")
    qi = inoc['todas_as_UFs|interior|T2|u=0.20']
    P(f"    Ao lado, capital contra o resto do estado (o resto pesando 80% do que pesa, em todas as UFs): inclinação {f(qi['inclinacao_27_UFs'], 1)}; erro médio no Nordeste {f(qi['erro_NE'])}, no Sul {f(qi['erro_S'])}.")
    P('    Leitura: pesquisa que ouça de menos o município pequeno do Nordeste produz um erro que cresce com o coeficiente, do mesmo lado que')
    P('    um desvio regulado pela força local. O teste por UF não separa as duas coisas; o espelho do 1º turno é o que pode separar.')
    R['explicacao_inocente_plantada'] = dict(cenarios=inoc, u_para_inclinacao_20=q20, pesos={u: base[u] for u in UFS})

    # ============================================================ PARTE B
    P('')
    P('2. PARTE B: RECORTE POR REGIÃO DAS PESQUISAS NACIONAIS FINAIS (NORDESTE CONTRA SUL)')
    def reg_urna(r, turno=2):
        if turno == 2:
            return 100 * sum(uf[u]['L2'] for u in REGIOES[r]) / sum(val2[u] for u in REGIOES[r])
        return 100 * sum(uf[u]['L1'] for u in REGIOES[r]) / sum(val1[u] for u in REGIOES[r])
    def reg_coef(r):
        return float(np.average([coef[u] for u in REGIOES[r]], weights=[val2[u] for u in REGIOES[r]]))
    def reg_peso(r):
        return sum(val2[u] for u in REGIOES[r]) / VAL2
    regs = ('NE', 'SE', 'S', 'N', 'CO', 'N+CO')
    URN = {r: reg_urna(r) for r in regs}; URN1 = {r: reg_urna(r, 1) for r in regs}
    CRE = {r: reg_coef(r) for r in regs}; CES = {r: float(np.average([cesp[u] for u in REGIOES[r]], weights=[val2[u] for u in REGIOES[r]])) for r in regs}
    delta_c = CRE['NE'] - CRE['S']
    P('  Urna por região (Lula, válidos do 2º turno) e coeficiente médio do T16 (ponderado pelos válidos):')
    P('    ' + '; '.join(f"{r}: urna {f(URN[r])}, coef {CRE[r]:+.4f}, {f(100 * reg_peso(r), 1)}% dos válidos" for r in regs))
    P(f"  delta_c = coef do Nordeste menos o do Sul = {delta_c:.4f}. Limiares traduzidos (B3): ESTRUTURADO se D >= {f(LIM_ESTR * delta_c)} ponto a mais de 3 ep,")
    P(f"  com 3 institutos ou mais; UNIFORME se |D| < {f(LIM_UNIF * delta_c)} com ep até {f(EP_UNIF * delta_c)}. Plantado puro: D = kappa x delta_c = {f(kappa * delta_c)} pontos.")
    def val_reg(q, base):
        if q is None or q.get('lula') is None or q.get('flavio') is None:
            return None
        return 100.0 * q['lula'] / (q['lula'] + q['flavio'])
    linhasB = []
    for p in coleta['parte_B_recorte_regional_2T']:
        item = dict(id=p['id'], instituto=p['instituto'], campo=f"{p['campo_inicio']} a {p['campo_fim']}", amostra=p['amostra'], base=p['base'], regioes={})
        for r, q in p['regioes'].items():
            if p['base'] == 'totais_um_lado':
                o = p['outros_nacional']
                lv = (100 * q['lula'] / (100 - o)) if q.get('lula') is not None else (100 * (100 - o - q['flavio']) / (100 - o))
                faixa = []
                for oo in (1.0, 2.6):
                    faixa.append((100 * q['lula'] / (100 - oo)) if q.get('lula') is not None else (100 * (100 - oo - q['flavio']) / (100 - oo)))
                item['regioes'][r] = dict(lula_validos=lv, faixa=sorted(faixa), estimado=True)
            else:
                item['regioes'][r] = dict(lula_validos=val_reg(q, p['base']), estimado=False)
            lv = item['regioes'][r]['lula_validos']
            item['regioes'][r]['erro'] = URN[r] - lv
            nreg = p['amostra'] * reg_peso(r) * 0.93
            item['regioes'][r]['ep_amostral'] = 100 * math.sqrt((lv / 100) * (1 - lv / 100) / nreg)
        if 'NE' in item['regioes'] and 'S' in item['regioes']:
            item['D'] = item['regioes']['NE']['erro'] - item['regioes']['S']['erro']
            item['ep_amostral_D'] = math.sqrt(item['regioes']['NE']['ep_amostral'] ** 2 + item['regioes']['S']['ep_amostral'] ** 2)
        linhasB.append(item)
    P('  instituto (campo, amostra)                 | região: Lula válidos na pesquisa -> erro (urna menos pesquisa)                              | D = erro NE - erro Sul (ep amostral)')
    for it in linhasB:
        P(f"  {it['instituto']:<10} ({it['campo'][8:10]}/10 a {it['campo'][-2:]}/10, {it['amostra']}){'' if it['base'] != 'totais_um_lado' else ' [estimada]'}".ljust(45) + '| ' +
          '; '.join(f"{r} {f(q['lula_validos'], 1)} -> {f(q['erro'], 1)}" for r, q in it['regioes'].items()).ljust(91) +
          f" | {f(it.get('D'))} ({f(it.get('ep_amostral_D'))})")
    def resumo_B(itens, nome):
        Ds = [it['D'] for it in itens]; k = len(Ds)
        m = float(np.mean(Ds)); dp = float(np.std(Ds, ddof=1)) if k > 1 else float('nan')
        ep_entre = dp / math.sqrt(k) if k > 1 else float('nan')
        ep_am = math.sqrt(sum(it['ep_amostral_D'] ** 2 for it in itens)) / k
        ep_maior = max(ep_entre, ep_am) if k > 1 else ep_am
        out = dict(conjunto=nome, institutos=[it['instituto'] for it in itens], k=k, D_medio=m, dp_entre_institutos=dp,
                   ep_entre_institutos=ep_entre, ep_amostral=ep_am, inclinacao_B=m / delta_c, ep_B_entre=ep_entre / delta_c,
                   ep_B_amostral=ep_am / delta_c, erro_medio_NE=float(np.mean([it['regioes']['NE']['erro'] for it in itens])),
                   erro_medio_S=float(np.mean([it['regioes']['S']['erro'] for it in itens])))
        def ver(ep):
            if k < 3:
                return 'SEM PODER (menos de 3 institutos)'
            v = letra(m / delta_c, ep / delta_c, k, min_n=3)
            T = max(LIM_ESTR * delta_c, 3 * ep)
            poder = 1 - phi((T - kappa * delta_c) / ep)
            poder20 = 1 - phi((T - LIM_ESTR * delta_c) / ep)
            if v != 'ESTRUTURADO' and poder < 0.80:
                v = f'SEM PODER (pela letra seria {v}; o plantado puro só viraria ESTRUTURADO em {f(100 * poder, 1)}% das vezes)'
            return v, poder, poder20
        for rot, ep in (('entre_institutos', ep_entre), ('amostral', ep_am), ('maior_dos_dois', ep_maior)):
            vv = ver(ep)
            if isinstance(vv, str):
                out[f'veredito_ep_{rot}'] = vv
            else:
                out[f'veredito_ep_{rot}'] = vv[0]; out[f'poder_plantado_puro_ep_{rot}'] = vv[1]; out[f'poder_plantado_20_ep_{rot}'] = vv[2]
                out[f'letra_sem_regra_de_poder_ep_{rot}'] = letra(m / delta_c, ep / delta_c, k, min_n=3)
        return out
    princ = [it for it in linhasB if 'D' in it and not any(q['estimado'] for q in it['regioes'].values())]
    comatlas = [it for it in linhasB if 'D' in it]
    RB = dict(urna_por_regiao=URN, coef_por_regiao=CRE, coef_espelho_por_regiao=CES, delta_c=delta_c, D_plantado_puro=kappa * delta_c,
              limiar_estruturado_D=LIM_ESTR * delta_c, limiar_uniforme_D=LIM_UNIF * delta_c, ep_max_uniforme_D=EP_UNIF * delta_c,
              institutos=linhasB, principal=resumo_B(princ, 'principal: Lula e Flávio publicados no Nordeste e no Sul'),
              com_AtlasIntel_estimada=resumo_B(comatlas, 'sensibilidade: com a AtlasIntel estimada'))
    for chave in ('principal', 'com_AtlasIntel_estimada'):
        q = RB[chave]
        P(f"  {q['conjunto']} ({', '.join(q['institutos'])}):")
        P(f"    erro médio no Nordeste {f(q['erro_medio_NE'])}, no Sul {f(q['erro_medio_S'])}; D médio = {f(q['D_medio'])} pontos; ep entre institutos {f(q['ep_entre_institutos'])}"
          f" (dp {f(q['dp_entre_institutos'])}, k = {q['k']}); ep amostral {f(q['ep_amostral'])}.")
        P(f"    Em unidades da letra: inclinação_B = {f(q['inclinacao_B'], 1)} pontos por unidade de coeficiente; ep {f(q['ep_B_entre'], 1)} (entre institutos) ou {f(q['ep_B_amostral'], 1)} (amostral).")
        P(f"    Veredito com o ep entre institutos (o do docstring): {q['veredito_ep_entre_institutos']}.")
        P(f"    Com o ep amostral: {q['veredito_ep_amostral']}. Com o maior dos dois: {q['veredito_ep_maior_dos_dois']}.")
    faixa_atlas = [it for it in linhasB if it['base'] == 'totais_um_lado']
    if faixa_atlas:
        it = faixa_atlas[0]
        dmin = (URN['NE'] - it['regioes']['NE']['faixa'][1]) - (URN['S'] - it['regioes']['S']['faixa'][0])
        dmax = (URN['NE'] - it['regioes']['NE']['faixa'][0]) - (URN['S'] - it['regioes']['S']['faixa'][1])
        RB['AtlasIntel_faixa_D'] = [dmin, dmax]
        P(f"    AtlasIntel: D entre {f(dmin)} e {f(dmax)} conforme o branco, nulo e indeciso regional seja de 2,6% a 1,0% (só o líder de cada região foi publicado).")
    # todas as regiões, efeito fixo de instituto
    pts = [(it['instituto'], r, CRE[r], q['erro']) for it in linhasB if it['base'] != 'totais_um_lado' for r, q in it['regioes'].items()]
    insts = sorted({p[0] for p in pts})
    Xd = np.array([[1.0 if p[0] == k else 0.0 for k in insts] + [p[2]] for p in pts]); yd = np.array([p[3] for p in pts])
    bt, *_ = np.linalg.lstsq(Xd, yd, rcond=None)
    ed = yd - Xd @ bt; gl = len(pts) - Xd.shape[1]
    Vd = np.linalg.inv(Xd.T @ Xd) * float((ed ** 2).sum() / gl)
    RB['todas_as_regioes_efeito_fixo_de_instituto'] = dict(pontos=len(pts), inclinacao=float(bt[-1]), ep=float(math.sqrt(Vd[-1, -1])), graus_de_liberdade=gl)
    P(f"  Ao lado, todas as regiões publicadas com efeito fixo de instituto ({len(pts)} pontos, {gl} graus de liberdade): inclinação {f(bt[-1], 1)} (ep {f(math.sqrt(Vd[-1, -1]), 1)}).")
    # espelho Sudeste contra Norte e Centro-Oeste
    esp = []
    for it in linhasB:
        if it['base'] != 'totais_um_lado' and 'SE' in it['regioes'] and 'N+CO' in it['regioes']:
            esp.append(dict(instituto=it['instituto'], D_espelho=it['regioes']['SE']['erro'] - it['regioes']['N+CO']['erro'],
                            ep_amostral=math.sqrt(it['regioes']['SE']['ep_amostral'] ** 2 + it['regioes']['N+CO']['ep_amostral'] ** 2)))
    RB['espelho_Sudeste_menos_Norte_Centro_Oeste'] = dict(delta_c=CRE['SE'] - CRE['N+CO'], institutos=esp)
    P(f"  Espelho Sudeste menos Norte/Centro-Oeste (coef {CRE['SE']:+.4f} contra {CRE['N+CO']:+.4f}; a forma regulada prevê {f(kappa * (CRE['SE'] - CRE['N+CO']))} ponto): " +
      ('; '.join(f"{e['instituto']} {f(e['D_espelho'])} (ep amostral {f(e['ep_amostral'])})" for e in esp) if esp else 'sem instituto com as duas regiões') + '.')
    # espelho por candidato
    dce = CES['NE'] - CES['S']
    xm = [cesp[u] for u in A['UFs']]; ym = [-A['por_UF'][u]['erro'] for u in A['UFs']]
    rm = ols(xm, ym)
    sem_ac = [u for u in A['UFs'] if u != 'AC']
    rm_sem_ac = ols([cesp[u] for u in sem_ac], [-A['por_UF'][u]['erro'] for u in sem_ac])
    RB['espelho_por_candidato'] = dict(coef_espelho_por_regiao=CES, delta_coef_espelho_NE_menos_S=dce,
                                       aplicavel_ao_contraste_regional=abs(dce) >= 0.02,
                                       parte_A_descritivo=dict(n=rm['n'], inclinacao=rm['b'], ep=rm['ep']),
                                       parte_A_descritivo_sem_AC=dict(n=rm_sem_ac['n'], inclinacao=rm_sem_ac['b'], ep=rm_sem_ac['ep']))
    P(f"  Espelho por candidato (P19): o coeficiente espelho quase não muda entre as regiões (NE {CES['NE']:+.4f}, SE {CES['SE']:+.4f}, Sul {CES['S']:+.4f},"
      f" N+CO {CES['N+CO']:+.4f}; NE menos Sul = {dce:+.4f}) e não acompanha o do T16 (correlação {f(cc, 2)}, e não alta como o docstring supôs).")
    P(f"    Sem diferença de coeficiente espelho entre Nordeste e Sul, o espelho por candidato não se aplica ao contraste regional. Nas {A['n_UFs']} UFs da Parte A,")
    P(f"    só descritivo: erro de Flávio contra o coeficiente espelho = {f(rm['b'], 1)} por unidade (ep {f(rm['ep'], 1)}); sem o AC (coeficiente espelho {f(cesp['AC'], 3)},"
      f" o maior do país): {f(rm_sem_ac['b'], 1)} (ep {f(rm_sem_ac['ep'], 1)}).")
    P(f"    Pelo limiar do P19 (20 ou mais a mais de 3 ep) o espelho passaria se a exigência de 15 UFs fosse ignorada, enquanto o teste principal, nas mesmas UFs, dá {f(rd['b'], 1)}.")
    P('    Com 6 pontos, e com coeficientes tirados da própria urna do 2º turno (onde Flávio foi melhor que o esperado o coeficiente espelho é maior e o erro dele é menor')
    P('    por construção), isso não vale como sinal para nenhum lado; mostra que o desenho por UF, com o que existe, não mede o que promete.')
    # decomposição do erro por região
    dec = {}
    for r in ('NE', 'SE', 'S', 'N+CO'):
        vals = [it['regioes'][r]['erro'] for it in linhasB if it['base'] != 'totais_um_lado' and r in it['regioes']]
        if vals:
            dec[r] = dict(n_institutos=len(vals), erro_medio=float(np.mean(vals)), erros=vals, peso=reg_peso(r),
                          contribuicao_ao_erro_nacional=float(np.mean(vals)) * reg_peso(r), previsto_forma_pura=kappa * CRE[r],
                          previsto_uniforme=ERRO_NACIONAL_L5A)
    RB['erro_medio_por_regiao'] = dec
    P('  Erro médio por região (institutos com Lula e Flávio publicados) ao lado do que cada forma prevê:')
    P('    região | institutos | erro médio | forma pura (kappa x coef) | forma uniforme | peso nos válidos | contribuição ao erro nacional')
    for r, q in dec.items():
        P(f"    {r:<6} | {q['n_institutos']}          | {f(q['erro_medio']):>6}     | {f(q['previsto_forma_pura']):>6}                    | {f(q['previsto_uniforme']):>6}         |"
          f" {f(100 * q['peso'], 1):>5}%           | {f(q['contribuicao_ao_erro_nacional'])}")
    # espelho no tempo (1º turno)
    P('  Espelho no tempo (1º turno, onde a suspeita não está):')
    et = []
    for p in coleta['parte_B_espelho_1T']:
        item = dict(instituto=p['instituto'], campo=p['campo'], amostra=p['amostra'])
        r1 = p.get('regioes_1T_validos')
        if r1 and 'NE' in r1 and 'S' in r1:
            # válidos publicados do 1º turno (base válidos): Lula direto
            item['erro_1T_NE'] = URN1['NE'] - r1['NE']['lula']; item['erro_1T_S'] = URN1['S'] - r1['S']['lula']
            item['D_1T'] = item['erro_1T_NE'] - item['erro_1T_S']
            n_ne = p['amostra'] * reg_peso('NE') * 0.93; n_s = p['amostra'] * reg_peso('S') * 0.93
            item['ep_amostral_D_1T'] = 100 * math.sqrt(0.61 * 0.39 / n_ne + 0.32 * 0.68 / n_s)
        r2h = p.get('regioes_2T_hipotetico_totais')
        if r2h and r2h.get('NE', {}).get('flavio') is not None and r2h.get('S', {}).get('flavio') is not None:
            ne = 100 * r2h['NE']['lula'] / (r2h['NE']['lula'] + r2h['NE']['flavio']); s_ = 100 * r2h['S']['lula'] / (r2h['S']['lula'] + r2h['S']['flavio'])
            item['lula_2T_hipotetico_NE'] = ne; item['lula_2T_hipotetico_S'] = s_
            item['D_2T_hipotetico'] = (URN['NE'] - ne) - (URN['S'] - s_)
        et.append(item)
    RB['espelho_1T'] = dict(urna_1T_por_regiao=URN1, institutos=et)
    for it in et:
        if 'D_1T' in it:
            P(f"    {it['instituto']} {it['campo']} ({it['amostra']}): 1º turno, Lula nos válidos: Nordeste pesquisa 61 contra urna {f(URN1['NE'])} (erro {f(it['erro_1T_NE'])});"
              f" Sul pesquisa 32 contra urna {f(URN1['S'])} (erro {f(it['erro_1T_S'])}); D do 1º turno = {f(it['D_1T'])} (ep amostral {f(it['ep_amostral_D_1T'])}).")
        if 'D_2T_hipotetico' in it:
            P(f"    {it['instituto']} {it['campo']}: cenário de 2º turno perguntado antes do 1º: Nordeste {f(it['lula_2T_hipotetico_NE'], 1)}, Sul {f(it['lula_2T_hipotetico_S'], 1)};"
              f" D contra a urna do 2º turno = {f(it['D_2T_hipotetico'])}.")
    dfinal = next((it for it in linhasB if it['instituto'] == 'Datafolha'), None)
    d1 = next((it for it in et if it['instituto'] == 'Datafolha' and 'D_1T' in it), None)
    if dfinal and d1:
        dd = dfinal['D'] - d1['D_1T']; epdd = math.sqrt(dfinal['ep_amostral_D'] ** 2 + d1['ep_amostral_D_1T'] ** 2)
        RB['espelho_1T']['Datafolha_D_2T_menos_D_1T'] = dict(valor=dd, ep_amostral=epdd)
        RB['espelho_1T']['Datafolha_erros'] = dict(NE_1T=d1['erro_1T_NE'], NE_2T=dfinal['regioes']['NE']['erro'], S_1T=d1['erro_1T_S'], S_2T=dfinal['regioes']['S']['erro'])
        P(f"    Datafolha, D do 2º turno ({f(dfinal['D'])}) menos D do 1º turno ({f(d1['D_1T'])}) = {f(dd)} (ep amostral {f(epdd)}). Na Datafolha o erro de Lula no Nordeste")
        P(f"    foi do mesmo tamanho nos dois turnos ({f(d1['erro_1T_NE'])} no 1º, {f(dfinal['regioes']['NE']['erro'])} no 2º); o que mudou do 1º para o 2º turno foi o Sul"
          f" ({f(d1['erro_1T_S'])} para {f(dfinal['regioes']['S']['erro'])}). Um instituto só, descritivo.")
    P('  Rodadas anteriores do cenário Lula contra Flávio (fora da janela, descritivo; D contra a urna do 2º turno): ' + '; '.join(
        f"{p['instituto']} {p['campo']}: D = " + f((URN['NE'] - val_reg(p['regioes']['NE'], p['base'])) - (URN['S'] - val_reg(p['regioes']['S'], p['base'])))
        for p in coleta['parte_B_rodadas_anteriores']) + '.')
    RB['rodadas_anteriores'] = [dict(instituto=p['instituto'], campo=p['campo'],
                                     D=(URN['NE'] - val_reg(p['regioes']['NE'], p['base'])) - (URN['S'] - val_reg(p['regioes']['S'], p['base'])),
                                     erros={r: URN[r] - val_reg(q, p['base']) for r, q in p['regioes'].items()}) for p in coleta['parte_B_rodadas_anteriores']]
    # explicação inocente agregada por região
    def inoc_regiao(u_, alvo, turno=2):
        out = {}
        for r in ('NE', 'S'):
            g = h = gp = hp = 0.0
            for (uu, m), v in mun.items():
                if uu not in REGIOES[r]:
                    continue
                num, den = (v[1], v[1] + v[2]) if turno == 2 else (v[3], v[4])
                k = (1 - u_) if uu in alvo else 1.0
                if v[0] < 50000:
                    gp += num; hp += den
                    g += 0
                    out.setdefault(r, [0, 0, 0, 0])
                    out[r][0] += num; out[r][1] += den; out[r][2] += k * num; out[r][3] += k * den
                else:
                    out.setdefault(r, [0, 0, 0, 0])
                    out[r][0] += num; out[r][1] += den; out[r][2] += num; out[r][3] += den
        return {r: 100 * (v[0] / v[1] - v[2] / v[3]) for r, v in out.items()}
    ib = {}
    for alvo_nome, alvo in (('so_Nordeste', REGIOES['NE']), ('todas_as_UFs', UFS)):
        for u_ in (0.10, 0.20, 0.30):
            e_ = inoc_regiao(u_, alvo)
            ib[f'{alvo_nome}|u={u_:.2f}'] = dict(erro_NE=e_['NE'], erro_S=e_['S'], D=e_['NE'] - e_['S'])
    Dobs = RB['principal']['D_medio']
    def u_para_D(alvo, Dalvo):
        lo, hi = 0.0, 0.95
        g = lambda uu: (lambda e_: e_['NE'] - e_['S'])(inoc_regiao(uu, alvo))
        if g(hi) < Dalvo:
            return None
        for _ in range(30):
            mid = (lo + hi) / 2
            if g(mid) < Dalvo: lo = mid
            else: hi = mid
        return hi
    ib['u_que_produz_o_D_observado'] = {'so_Nordeste': u_para_D(REGIOES['NE'], Dobs) if Dobs > 0 else None,
                                        'todas_as_UFs': u_para_D(UFS, Dobs) if Dobs > 0 else None}
    RB['explicacao_inocente_por_regiao'] = ib
    P('  Explicação inocente plantada, agregada por região (municípios com menos de 50 mil aptos pesando 1 - u):')
    P('    ' + '; '.join(f"{k.replace('|', ', ')}: D = {f(v['D'])}" for k, v in ib.items() if k.startswith(('so_', 'todas'))) + '.')
    uq = ib['u_que_produz_o_D_observado']
    P(f"    Para produzir sozinha o D observado ({f(Dobs)}): só no Nordeste u = {f(100 * uq['so_Nordeste'], 0) + '%' if uq['so_Nordeste'] else 'impossível (acima de 95%)'};"
      f" em todas as UFs u = {f(100 * uq['todas_as_UFs'], 0) + '%' if uq['todas_as_UFs'] else 'impossível (acima de 95%)'}.")
    R['parte_B'] = RB

    # ============================================================ PARTE X (exploratória)
    P('')
    P('3. PARTE EXPLORATÓRIA (acréscimo ao docstring): PESQUISAS ESTADUAIS DA ÚLTIMA SEMANA ANTES DO 1º TURNO')
    P('  Decidida depois de ver que a janela registrada só tem 6 UFs; regras escritas antes de levantar estas pesquisas. Coleta incompleta.')
    RX = {}
    def l1(p):
        t = p.get('t1')
        return None if not t else 100.0 * t['lula'] / (t['lula'] + t['flavio'] + t['outros'])
    def l2(p):
        t = p.get('t2')
        if not t:
            return None
        if t.get('lula_validos') is not None:
            return float(t['lula_validos'])
        return 100.0 * t['lula'] / (t['lula'] + t['flavio'])
    for jn, jan in (('janela_27_09_a_03_10', JANELA_1T), ('janela_larga_20_09_a_03_10', JANELA_1T_LARGA)):
        sel = uma_por_instituto([p for p in coleta['parte_X_pre_1T_estaduais'] if dentro(p, jan) and p['nivel'] == 'conferida'])
        por = {}
        for p in sel:
            a1, a2 = l1(p), l2(p)
            d = dict(id=p['id'], instituto=p['instituto'], campo=f"{p['campo_inicio'][8:]}/{p['campo_inicio'][5:7]} a {p['campo_fim'][8:]}/{p['campo_fim'][5:7]}",
                     amostra=p['amostra'], L1=a1, L2=a2, e1=(urna1[p['uf']] - a1) if a1 is not None else None,
                     e2=(urna2[p['uf']] - a2) if a2 is not None else None)
            d['DD'] = (d['e2'] - d['e1']) if d['e1'] is not None and d['e2'] is not None else None
            por.setdefault(p['uf'], []).append(d)
        tab = {}
        for u, lst in sorted(por.items()):
            tab[u] = {k: (float(np.mean([d[k] for d in lst if d[k] is not None])) if any(d[k] is not None for d in lst) else None) for k in ('e1', 'e2', 'DD')}
            tab[u]['pesquisas'] = lst
        regx = {}
        for k in ('e1', 'e2', 'DD'):
            us = [u for u in tab if tab[u][k] is not None]
            if len(us) >= 3:
                r = ols([coef[u] for u in us], [tab[u][k] for u in us])
                rf = ols([urna1[u] for u in us], [tab[u][k] for u in us])
                regx[k] = dict(UFs=us, n=len(us), media=float(np.mean([tab[u][k] for u in us])), inclinacao=r['b'], ep=r['ep'], ep_hc3=r['ep_hc3'],
                               leitura_exploratoria=('sem dados para o limiar (menos de 8 UFs)' if len(us) < MIN_REG else letra(r['b'], r['ep'], len(us))),
                               contra_fatia_lula_1T=dict(inclinacao=rf['b'], ep=rf['ep']))
                if len(us) >= 4:
                    cp = permutacao_plantio([coef[u] for u in us], [tab[u][k] for u in us], planos, rng, exigir_n=False)
                    regx[k]['plantio_sem_exigir_15_UFs'] = {a: dict(frac_estruturado=b['frac_estruturado'], frac_uniforme=b['frac_uniforme'], ep_medio=b['ep_medio']) for a, b in cp.items()}
        so_rt = {}
        for k in ('e1', 'e2', 'DD'):
            us = [u for u in por if any(d['instituto'] == 'Real Time Big Data' and d[k] is not None for d in por[u])]
            if len(us) >= 3:
                yv = [float(np.mean([d[k] for d in por[u] if d['instituto'] == 'Real Time Big Data' and d[k] is not None])) for u in us]
                r = ols([coef[u] for u in us], yv)
                so_rt[k] = dict(UFs=us, n=len(us), media=float(np.mean(yv)), inclinacao=r['b'], ep=r['ep'])
        RX[jn] = dict(por_UF=tab, regressoes=regx, so_Real_Time_Big_Data=so_rt)
        P(f"  {jn.replace('_', ' ')}: {len(sel)} pesquisas em {len(tab)} UFs")
        P('    UF | coef T16 | pesquisa (campo, amostra)                  | 1T: pesq. -> urna (e1)      | 2T: pesq. -> urna (e2)      | DD = e2 - e1')
        for u in sorted(tab):
            for d in tab[u]['pesquisas']:
                P(f"    {u} | {coef[u]:+.4f}  | {(d['instituto'] + ' (' + d['campo'] + ', ' + str(d['amostra']) + ')'):<42} | "
                  f"{(f(d['L1'], 1) + ' -> ' + f(urna1[u], 1) + ' (' + f(d['e1'], 1) + ')') if d['L1'] is not None else 'não publicado':<27} | "
                  f"{(f(d['L2'], 1) + ' -> ' + f(urna2[u], 1) + ' (' + f(d['e2'], 1) + ')') if d['L2'] is not None else 'não publicado':<27} | {f(d['DD'], 1)}")
        for k, rot in (('e1', 'e1 (espelho E1: 1º turno)'), ('e2', 'e2 (cenário de 2º turno perguntado antes do 1º)'), ('DD', 'DD (e2 menos e1)')):
            if k in regx:
                q = regx[k]
                P(f"    {rot}: {q['n']} UFs, média {f(q['media'])}; reta contra o coeficiente {f(q['inclinacao'], 1)} (ep {f(q['ep'], 1)}; HC3 {f(q['ep_hc3'], 1)});"
                  f" contra a fatia de Lula no 1º turno {f(q['contra_fatia_lula_1T']['inclinacao'], 3)} (ep {f(q['contra_fatia_lula_1T']['ep'], 3)}). Leitura: {q['leitura_exploratoria']}.")
                if 'plantio_sem_exigir_15_UFs' in q:
                    pp = q['plantio_sem_exigir_15_UFs']
                    P(f"      plantio nos resíduos, sem exigir 15 UFs: kappa vira ESTRUTURADO em {f(100 * pp['puro_kappa']['frac_estruturado'], 1)}%, 20 em {f(100 * pp['limiar_20']['frac_estruturado'], 1)}%,"
                      f" uniforme vira UNIFORME em {f(100 * pp['uniforme_0']['frac_uniforme'], 1)}%.")
        if so_rt:
            P('    Só Real Time Big Data (mesmo método em todas): ' + '; '.join(f"{k}: {v['n']} UFs, média {f(v['media'])}, reta {f(v['inclinacao'], 1)} (ep {f(v['ep'], 1)})" for k, v in so_rt.items()) + '.')
    P('  Espelho E1 pela regra fixada em P18: ESPELHO SEM DADOS (o docstring pede 10 UFs; há 6 na janela de uma semana e 8 na larga).')
    P('  Leitura exploratória: com 6 a 9 UFs nenhuma reta decide. O que os números dizem sem reta está na seção 6.')
    R['parte_X_exploratoria'] = RX

    # ============================================================ votos
    P('')
    P('4. TRADUÇÃO EM VOTOS DE MARGEM (P20)')
    cmin = min(coef.values())
    S_estr = sum((coef[u] - cmin) * val2[u] for u in UFS) / 100       # votos por ponto de inclinação
    votos = dict(votos_por_ponto_de_erro_uniforme=VAL2 / 100,
                 parte_A_erro_medio_ponderado=A['erro_medio_ponderado_validos'],
                 parte_A_votos_de_Lula_se_valesse_no_pais=A['erro_medio_ponderado_validos'] * VAL2 / 100,
                 parte_A_votos_nas_UFs_incluidas=sum(A['por_UF'][u]['erro'] * val2[u] for u in A['UFs']) / 100,
                 estruturado_votos_por_unidade_de_inclinacao=S_estr,
                 limiar_20_votos=LIM_ESTR * S_estr, limiar_20_margem=2 * LIM_ESTR * S_estr,
                 puro_kappa_votos=kappa * S_estr, puro_kappa_margem=2 * kappa * S_estr,
                 margem_oficial=MARGEM)
    P(f"  Um ponto de erro igual em todo o país vale {mil(VAL2 / 100)} votos de Lula, ou {mil(2 * VAL2 / 100)} de margem (margem oficial: {mil(MARGEM)}).")
    P(f"  Parte A: erro médio ponderado de {f(A['erro_medio_ponderado_validos'])} ponto nas 6 UFs = {mil(votos['parte_A_votos_nas_UFs_incluidas'])} votos de Lula acima das pesquisas nessas UFs"
      f" ({mil(2 * votos['parte_A_votos_nas_UFs_incluidas'])} de margem, {f(100 * 2 * votos['parte_A_votos_nas_UFs_incluidas'] / MARGEM, 1)}% da margem oficial). Estendido ao país seriam"
      f" {mil(votos['parte_A_votos_de_Lula_se_valesse_no_pais'])} votos ({mil(2 * votos['parte_A_votos_de_Lula_se_valesse_no_pais'])} de margem), mas 6 UFs com {f(100 * A['fatia_dos_validos_do_pais'], 1)}% dos válidos não representam o país.")
    P(f"  Forma estruturada: cada ponto de inclinação vale {mil(S_estr)} votos acima do nível da UF de menor coeficiente (SC). No limiar de 20: {mil(LIM_ESTR * S_estr)} votos,"
      f" {mil(2 * LIM_ESTR * S_estr)} de margem ({f(100 * 2 * LIM_ESTR * S_estr / MARGEM, 1)}% da oficial). Na forma pura (kappa): {mil(kappa * S_estr)} votos, {mil(2 * kappa * S_estr)} de margem.")
    q = RB['principal']
    bB = q['inclinacao_B']
    vNE = q['erro_medio_NE'] * sum(val2[u] for u in REGIOES['NE']) / 100; vS = q['erro_medio_S'] * sum(val2[u] for u in REGIOES['S']) / 100
    votos.update(parte_B_inclinacao=bB, parte_B_votos_estruturados=bB * S_estr, parte_B_margem_estruturada=2 * bB * S_estr,
                 parte_B_votos_NE=vNE, parte_B_votos_S=vS,
                 parte_B_ic95_margem_estruturada_ep_amostral=[2 * (bB - 1.96 * q['ep_B_amostral']) * S_estr, 2 * (bB + 1.96 * q['ep_B_amostral']) * S_estr])
    P(f"  Parte B: erro médio de {f(q['erro_medio_NE'])} no Nordeste = {mil(vNE)} votos de Lula acima das pesquisas ({mil(2 * vNE)} de margem); de {f(q['erro_medio_S'])} no Sul = {mil(vS)} votos"
      f" ({mil(2 * vS)} de margem).")
    P(f"    O contraste D = {f(q['D_medio'])} equivale à inclinação {f(bB, 1)}; aplicada às 27 UFs, a parte regulada pela força local seria de {mil(bB * S_estr)} votos, {mil(2 * bB * S_estr)} de margem"
      f" ({f(100 * 2 * bB * S_estr / MARGEM, 1)}% da oficial; faixa de 95% pelo ep amostral: {mil(votos['parte_B_ic95_margem_estruturada_ep_amostral'][0])} a {mil(votos['parte_B_ic95_margem_estruturada_ep_amostral'][1])}).")
    R['votos'] = votos

    # ============================================================ vereditos
    vA = A['veredito_pela_letra']
    vB = RB['principal']['veredito_ep_entre_institutos']
    R['vereditos'] = dict(
        parte_A_coeficiente=vA, parte_A_fatia_lula_1T='SEM PODER (mesmas 6 UFs; sem regressão)',
        parte_B_letra_ep_entre_institutos=vB, parte_B_ep_amostral=RB['principal']['veredito_ep_amostral'],
        parte_B_maior_ep=RB['principal']['veredito_ep_maior_dos_dois'],
        parte_B_com_AtlasIntel=RB['com_AtlasIntel_estimada']['veredito_ep_entre_institutos'],
        testes_com_limiar=3)
    P('')
    P('5. VEREDITOS PELA LETRA')
    P(f"  Parte A, coeficiente do T16: {vA}")
    P(f"  Parte A, fatia de Lula no 1º turno (ao lado): {R['vereditos']['parte_A_fatia_lula_1T']}")
    P(f"  Parte B, Nordeste contra Sul (critério traduzido, ep entre institutos): {vB}")
    P(f"    com o ep amostral: {RB['principal']['veredito_ep_amostral']}; com o maior dos dois: {RB['principal']['veredito_ep_maior_dos_dois']}; com a AtlasIntel estimada: {RB['com_AtlasIntel_estimada']['veredito_ep_entre_institutos']}")
    P('  Três vereditos com limiar; a 3 ep unilateral, a chance de um ESTRUTURADO por acaso em cada um é de cerca de 0,1%, e eles não são independentes.')
    P('  Nenhum SINAL e nenhum SEM SINAL: o teste não chega a dizer se o erro das pesquisas é igual em toda parte ou cresce com a força de Lula.')

    # ============================================================ leitura
    pos = sum(1 for u in A['UFs'] if A['por_UF'][u]['erro'] > 0)
    dec = RB['erro_medio_por_regiao']; pq = RB['principal']
    xw = RX['janela_larga_20_09_a_03_10']['regressoes']; xp = RX['janela_27_09_a_03_10']['regressoes']
    d1 = next((it for it in RB['espelho_1T']['institutos'] if it['instituto'] == 'Datafolha' and 'D_1T' in it), None)
    ant = {(a['instituto'], a['campo'][:8]): a['D'] for a in RB['rodadas_anteriores']}
    esp_n = RB['espelho_Sudeste_menos_Norte_Centro_Oeste']['institutos']
    uq = RB['explicacao_inocente_por_regiao']['u_que_produz_o_D_observado']
    leitura = dict(
        a_favor=[
            f"No recorte por região das pesquisas nacionais finais o erro de Lula foi maior no Nordeste ({f(pq['erro_medio_NE'])}) que no Sul ({f(pq['erro_medio_S'])}): "
            f"D = {f(pq['D_medio'])} pontos, acima do limiar traduzido ({f(LIM_ESTR * delta_c)}) e perto do que a forma pura prevê ({f(kappa * delta_c)}).",
            f"A ordem das regiões acompanha o coeficiente: Nordeste {f(dec['NE']['erro_medio'])}, Sudeste {f(dec['SE']['erro_medio'])}, Sul {f(dec['S']['erro_medio'])}; a forma pura previa "
            f"{f(dec['NE']['previsto_forma_pura'])}, {f(dec['SE']['previsto_forma_pura'])} e {f(dec['S']['previsto_forma_pura'])}. O Norte/Centro-Oeste foge: {f(dec['N+CO']['erro_medio'])} na Nexus,"
            f" único instituto com esse recorte, contra {f(dec['N+CO']['previsto_forma_pura'])} previstos.",
            f"Três dos quatro institutos com recorte (Nexus, CNT/MDA e a AtlasIntel estimada) têm D de {f(min(it['D'] for it in linhasB if it['instituto'] != 'Datafolha'))} a "
            f"{f(max(it['D'] for it in linhasB if it['instituto'] != 'Datafolha'))}.",
            f"A subamostragem dos municípios pequenos não explica sozinha um D desse tamanho: precisaria tirar {f(100 * uq['todas_as_UFs'], 0) if uq['todas_as_UFs'] else 'mais de 95'}% do peso deles em todas as UFs"
            f" ({f(100 * uq['so_Nordeste'], 0) if uq['so_Nordeste'] else 'mais de 95'}% se só no Nordeste).",
            f"Nas 6 UFs com pesquisa estadual a urna deu mais a Lula que as pesquisas em {pos} de {A['n_UFs']} (média {f(A['erro_medio_simples'])}, ep {f(A['ep_do_erro_medio'])})."],
        contra=[
            f"O D de {f(pq['D_medio'])} está a {f(pq['D_medio'] / pq['ep_entre_institutos'], 1)} ep de zero pela dispersão entre institutos e a {f(pq['D_medio'] / pq['ep_amostral'], 1)} ep pelo erro amostral"
            f" (k = {pq['k']}); a letra pede 3. Não distingue zero da forma pura.",
            f"A Datafolha, a maior amostra presencial (4.050), errou igual nas três regiões publicadas: Nordeste {f(linhasB[0]['regioes']['NE']['erro'])}, Sudeste {f(linhasB[0]['regioes']['SE']['erro'])},"
            f" Sul {f(linhasB[0]['regioes']['S']['erro'])} (D = {f(linhasB[0]['D'])}).",
            (f"O contraste já existia antes do 2º turno: a Datafolha de 29/09 a 01/10 errou Lula no 1º turno em {f(d1['erro_1T_NE'])} no Nordeste e {f(d1['erro_1T_S'])} no Sul"
             f" (D = {f(d1['D_1T'])}), com o erro nacional de Lula perto de zero.") if d1 else '',
            (f"O contraste que não deveria dar nada (Sudeste menos Norte/Centro-Oeste, previsão da forma regulada {f(kappa * (CRE['SE'] - CRE['N+CO']))}) deu {f(esp_n[0]['D_espelho'])} na Nexus:"
             f" recorte regional de uma pesquisa de 2.000 erra 3 a 4 pontos por acaso.") if esp_n else '',
            f"Nas 6 UFs com pesquisa estadual o erro não cresce com o coeficiente (reta {f(rd['b'], 1)}, ep {f(rd['ep'], 1)}): AM {f(A['por_UF']['AM']['erro'])} e AC {f(A['por_UF']['AC']['erro'])},"
            f" de coeficiente alto, contra DF {f(A['por_UF']['DF']['erro'])} e ES {f(A['por_UF']['ES']['erro'])}, de coeficiente baixo.",
            f"Exploratório: nas pesquisas estaduais de antes do 1º turno, o quanto a urna andou a favor de Lula além do previsto (DD) não acompanha o coeficiente"
            f" (janela larga, {xw['DD']['n']} UFs: reta {f(xw['DD']['inclinacao'], 1)}, ep {f(xw['DD']['ep'], 1)}; janela de uma semana, {xp['DD']['n']} UFs: {f(xp['DD']['inclinacao'], 1)}, ep {f(xp['DD']['ep'], 1)});"
            f" os maiores DD estão no PR, em PE e no RS.",
            f"Exploratório: o espelho do 1º turno por UF aponta para o mesmo lado que o 2º (erro de Lula no 1º turno contra o coeficiente, janela larga, {xw['e1']['n']} UFs:"
            f" reta {f(xw['e1']['inclinacao'], 1)}, ep {f(xw['e1']['ep'], 1)}; cenário de 2º turno, {xw['e2']['n']} UFs: {f(xw['e2']['inclinacao'], 1)}, ep {f(xw['e2']['ep'], 1)}):"
            f" se há estrutura, ela não é própria do 2º turno. Pela regra fixada, com menos de 10 UFs este espelho fica como sem dados."],
        neutro=[
            f"O contraste não surgiu na última semana: na Nexus o cenário Lula contra Flávio já dava D = {f(ant.get(('Nexus/BTG', '18 a 20/'), float('nan')))} em 18 a 20/09 e"
            f" {f(ant.get(('Nexus/BTG', '10 a 12/'), float('nan')))} em 10 a 12/10, contra {f(next(it['D'] for it in linhasB if it['instituto'] == 'Nexus/BTG'))} na véspera; na Datafolha,"
            f" {f(ant.get(('Datafolha', '13 e 14/'), float('nan')))} em 13 e 14/10. Isso afasta uma virada de última hora concentrada no Nordeste, mas não separa viés fixo das pesquisas no Nordeste de desvio na urna.",
            f"A reta do espelho por candidato nas 6 UFs (erro de Flávio contra o coeficiente espelho: {f(rm['b'], 1)}, ep {f(rm['ep'], 1)}; sem o AC: {f(rm_sem_ac['b'], 1)}, ep {f(rm_sem_ac['ep'], 1)})"
            f" passaria do limiar de 3 ep se a exigência de 15 UFs fosse ignorada, enquanto a reta principal nas mesmas UFs é {f(rd['b'], 1)} (ep {f(rd['ep'], 1)})."
            f" São 6 pontos e coeficientes tirados da própria urna: não conta para lado nenhum."],
        ressalva_sobre_o_espelho_do_1T="Para a hipótese do Léo de que o 1º turno também foi alterado, o contraste já existir no 1º turno não é contrapeso: uma alteração presente nos "
                                       "dois turnos no Nordeste daria o mesmo. O espelho do 1º turno só pesa contra a hipótese de algo novo no 2º turno.")
    leitura['contra'] = [s for s in leitura['contra'] if s]
    R['leitura'] = leitura
    P('')
    P('6. LEITURA, NOS DOIS SENTIDOS')
    P('  A favor da tese (erro regulado pela força local de Lula):')
    for s in leitura['a_favor']:
        P('   - ' + s)
    P('  Contra:')
    for s in leitura['contra']:
        P('   - ' + s)
    P('  Nem a favor nem contra:')
    for s in leitura['neutro']:
        P('   - ' + s)
    P('  Ressalva: ' + leitura['ressalva_sobre_o_espelho_do_1T'])
    P('  O que cada resultado significaria (fixado antes): erro igual em toda parte combina com virada nacional de última hora e também com desvio')
    P('  uniforme na contagem; erro maior onde Lula é forte combina com desvio regulado pela força local e também com subamostragem do interior do')
    P('  Nordeste ou mobilização maior onde Lula é forte. O teste não chegou a nenhum dos dois. Pesquisa não é contagem: erro de pesquisa, com')
    P('  qualquer forma, não prova alteração de voto.')

    desvios = [
        'O registro não fixa regra de inclusão nem de média: P1 a P10 foram escritas no docstring antes da coleta (hash e hora em trabalho-eleicao/adendo27/R27_L5).',
        'P3: "instituto com histórico no 1º turno" lido como pesquisa de presidente, nacional ou estadual, com campo terminado de 04/09 a 03/10/2026. A Paraná Pesquisas (TO) ficou fora da principal por isso.',
        'P12 e P13: estimador (mínimos quadrados por UF, ep clássico) e piso de 8 UFs para haver regressão; tradução ESTRUTURADO = SINAL, UNIFORME = SEM SINAL.',
        'P14: limiar para a fatia de Lula no 1º turno traduzido pela diferença prevista entre PI e SC; não chegou a ser usado (6 UFs).',
        'P15 a P17: forma pura (kappa = 2,70 / 0,04572), regra dos 80% para SEM PODER e explicação inocente plantada (municípios com menos de 50 mil aptos) não estão no registro.',
        'Parte B: o registro só diz "somar o recorte por região"; o critério (B3) é tradução da letra, com piso de 3 institutos e regra de poder de 80%.',
        'Parte B: a AtlasIntel só publicou o líder de cada região; o outro lado foi estimado e ela entra só na sensibilidade. Na CNT/MDA o Lula do Sul é o complemento do Flávio (base válidos).',
        'Parte B, espelho do 1º turno: a Datafolha usada é a de 29/09 a 01/10 (2.506), não a última (2 e 3/10), cujo recorte regional não achei.',
        'P19: o docstring supôs que o coeficiente espelho era correlacionado com o do T16; a correlação é 0,06 e o coeficiente espelho não difere entre Nordeste e Sul, então o espelho por candidato não se aplica ao contraste regional.',
        'Parte exploratória (seção 3): decidida depois de ver que só 6 UFs têm pesquisa na janela; regras escritas antes de levantar essas pesquisas; coleta interrompida de propósito com 11 pesquisas.',
        'Amostra não publicada: 1.000 no erro amostral (AtlasIntel de AM, DF, ES, RN e TO; Quaest DF).',
        'As versões ao lado de P12 (meta-regressão, peso pelos válidos, efeito fixo de instituto) e o segundo regressor de P14 não foram calculados como teste: com 6 UFs não há regressão.',
        'Feito depois de ver o primeiro resultado (exploratório): a tabela de erro médio por região ao lado da forma pura; a busca da rodada Nexus de 18 a 20/09; a redação do espelho da Datafolha; a reta do espelho por candidato sem o AC. Os desenhos hipotéticos de 27 UFs na simulação de poder não estão no docstring.',
        'O critério da letra traz "(1,6 ponto entre PI e SC)"; com os coeficientes principais do T16 são 1,80. Vale a inclinação de 20.']
    limites = [
        'A coleta depende de um buscador restrito: não achar pesquisa estadual em 21 UFs não prova que não exista. O PesqEle do TSE não foi consultado.',
        'Os números vêm de matérias de imprensa lidas por ferramenta automática, não dos relatórios registrados; cada um tem link no JSON da coleta.',
        'Recorte regional de pesquisa nacional tem subamostra pequena (Sul: 280 a 600 entrevistas); o ep amostral de cada D vai de 2,3 a 3,6 pontos.',
        'Com 3 institutos, o ep pela dispersão entre institutos é ele mesmo incerto; por isso o ep amostral vai ao lado e o veredito é o mesmo com os dois.',
        'O limiar de ep até 4 do ERRO UNIFORME não é alcançável com pesquisa estadual real: na simulação, nem 3 pesquisas de 1.500 em cada uma das 27 UFs chegam lá (ep 8,8 no cenário central).',
        'O coeficiente do T16 é calculado com a própria urna e acompanha a fatia de Lula no 1º turno (correlação 0,82): o teste não separa "regulado pelo coeficiente" de "maior onde Lula é forte".']
    pistas = [
        'Microdados ou relatórios completos das pesquisas nacionais finais registradas (AtlasIntel 4.990, Datafolha 4.050, Quaest 3.702, CNT/MDA 2.032, Nexus 2.000, PoderData), com a UF de cada entrevista: partido político pode requerer à Justiça Eleitoral acesso ao sistema interno de controle e aos dados das pesquisas registradas (Resolução TSE 23.600/2019, art. 13; conferir a redação que valeu em 2026). Com eles o teste por UF passa a ter as 27 UFs.',
        'Recorte por região das últimas rodadas de Quaest, PoderData, Ipespe e Real Time Big Data: com 7 ou 8 institutos o ep do D cai para perto de 1 ponto e a forma pura (3,8) passa a ser visível.',
        'O mesmo recorte por região nas pesquisas finais do 1º turno, de todos os institutos: é o espelho que separa defeito fixo das pesquisas no Nordeste de algo próprio do 2º turno.',
        'O erro das pesquisas se concentra no Nordeste e no Sudeste, e o Nordeste é também onde o comparecimento mais subiu (Adendo 28): cruzar com a conferência de cadernos de votação em PI, MA, CE, PB e TO, que continua sendo a checagem que decide.']
    R['desvios'] = desvios; R['limites'] = limites; R['pistas'] = pistas
    P('')
    P('7. DESVIOS E DECISÕES NÃO REGISTRADAS')
    for s in desvios:
        P('  - ' + s)
    P('')
    P('8. LIMITES')
    for s in limites:
        P('  - ' + s)
    P('')
    P('9. PISTAS')
    for s in pistas:
        P('  - ' + s)
    R['tempo_s'] = time.time() - t0
    return R


if __name__ == '__main__':
    R = main()
    with open(SAIDA_JSON + '.parcial', 'w', encoding='utf-8') as fh:
        json.dump(R, fh, ensure_ascii=False, indent=1)
    _os.replace(SAIDA_JSON + '.parcial', SAIDA_JSON)
    with open(SAIDA_TXT + '.parcial', 'w', encoding='utf-8') as fh:
        fh.write('\n'.join(LINHAS) + '\n')
    _os.replace(SAIDA_TXT + '.parcial', SAIDA_TXT)
