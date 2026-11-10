#!/usr/bin/env python3
"""R29_J: O CARROSSEL "A MATEMÁTICA IMPOSSÍVEL DA ELEIÇÃO" (Adendo 29, J1 a J4, pela letra).

Critérios: PRE-REGISTRO-2026-10-26.md, seção "Adendo 29" (commit 3929135, 10/11/2026 09:49:50 UTC),
aplicados como estão escritos, sem mudar limiar. Este docstring foi escrito ANTES de calcular qualquer
R², resíduo ou simulação. Uma cópia com data e SHA-256 fica em
/home/user/trabalho-eleicao/adendo29/J/docstring_antes_de_rodar.txt.

Uso (sempre com python3 -I):
  python3 -I scripts/analisar_R29_J.py [--cache DIR]
Grava resultados/R29_matematica_impossivel.json e .txt. Com --cache, guarda em DIR (fora do repositório)
os agregados por UF e município e os vetores por seção, para não reler as bases em nova rodada.

O QUE O REGISTRO FIXA
- J1: por UF, x em três definições (Flávio sozinho; Flávio mais os eliminados de direita; a que melhor
  reproduzir os pontos legíveis: PI perto de x 25 e y 3,1; BA perto de 30 e 2,5; SC perto de 75 e 0,4);
  y = votos de Lula sobre votos de Flávio no 2º turno; ajustes linear, quadrático e exponencial, com R².
- J2: a mesma conta em 2022, 2018 e 2014, com o adversário do PT no lugar da direita.
- J3: votos reais do 1º turno de 2026 por UF; no 2º turno cada bloco (Lula, Flávio, cada eliminado,
  branco e nulo, faltosos) se divide com taxas nacionais mais um ruído sorteado por UF, com desvio de 2, 5
  e 10 pontos nas taxas; 1.000 sorteios por nível; distribuição do R² dos três ajustes.
- J4: o mesmo gráfico por município e por seção em 2026; por UF, o desvio em pontos de fatia entre o
  2º turno e o previsto pelo 1º.
- Leitura: "PROPRIEDADE DO GRÁFICO" se o R² do melhor ajuste for 0,98 ou mais na mediana da simulação com
  ruído de 5 pontos e em pelo menos dois dos outros anos. "ANOMALIA DE 2026" se o desvio-padrão dos
  resíduos de 2026 (em pontos de fatia do 2º turno) for menor que a metade do menor dos outros anos e
  ficar abaixo do percentil 1 da simulação com ruído de 2 pontos. A simulação é a régua principal e os
  outros anos vão ao lado.

O QUE EU JÁ SABIA AO ESCREVER ISTO (para o leitor pesar)
- Os nomes, números e totais nacionais dos candidatos (candidatos2026_1t, campo "nomes" e "totais").
- resultados/T38_pontos_por_uf.txt, já publicado: ganho em pontos de Lula e de Flávio entre os turnos
  e a fatia dos quatro maiores eliminados por UF. Com isso dá para antever, por alto, onde cada UF cai no
  eixo x em cada definição. Os R², os resíduos, os outros anos e a simulação eu não conhecia.
- resultados/R27_A2_assimetria_vazamento.txt, de onde saem as taxas nacionais da simulação.

CANDIDATOS DO 1º TURNO DE 2026 (número, nome na urna, votos, e como classifico, ANTES de calcular)
  22 FLAVIO BOLSONARO (PL)            56.104.503  direita (finalista)
  13 LULA (PT)                        53.879.538  esquerda (finalista)
  70 ESCRITOR AUGUSTO CURY (Avante)    3.448.569  centro ou indefinido
  14 RENAN SANTOS (Missão)             2.675.887  direita
  55 RONALDO CAIADO (PSD)              2.605.148  direita
  30 ZEMA (Novo)                         326.488  direita
  80 SAMARA (UP)                         122.911  esquerda
  16 HERTZ DIAS (PSTU)                    43.103  esquerda
  27 CLARIANA BARAO (DC)                  40.043  indefinido
  21 EDMILSON COSTA (PCB)                 22.693  esquerda
  35 VETERINÁRIO WILSON GRASSI (PMB)      16.881  indefinido
  29 RUI COSTA PIMENTA (PCO)              15.024  esquerda
  28 LEONARDO AVALANCHE                    5.246  candidatura anulada, fora dos válidos
Por quê. Direita: Caiado, Zema e Renan Santos fizeram campanha no campo da direita e de oposição ao
governo Lula, por partidos desse campo (PSD de Caiado, Novo, Missão do MBL); Zema e Caiado apoiaram Flávio
no 2º turno e Renan Santos liberou os eleitores (README, tabela de apoios). Cury (Avante) fez campanha sem
se pôr em nenhum dos dois campos, anunciou neutralidade em 05/10 e depois apoio condicionado: fica como
centro ou indefinido, fora do bloco. Clariana (DC) e Grassi (PMB) são de partidos pequenos sem campo
nítido e somam 0,05% dos válidos: indefinidos, fora do bloco. Esquerda: PT, UP, PSTU, PCB e PCO.
A classificação foi feita pelo campo político, não pelo encaixe no gráfico. As sensibilidades abaixo
mostram o que muda com outra classificação.

DECISÕES QUE O REGISTRO NÃO FIXA (tomadas aqui, antes de qualquer conta; relatadas como desvios)
D1. Pontos: as 27 UFs (26 estados e o DF). O exterior (ZZ) fica fora e é mostrado à parte como 28º ponto.
D2. Total de cada UF e de cada município = soma de todas as seções da base que têm aquele turno, cada
    turno por si (é o total oficial), sem exigir que a seção exista nos dois turnos. Valores ausentes
    contam zero.
D3. Válidos do 1º turno de 2026 = votos nominais dos 12 candidatos válidos (o 28 fica fora). Nos outros
    anos, válidos = L + R + O da base. Fatias em porcentagem (0 a 100).
D4. Definições de x em 2026, sempre sobre os válidos do 1º turno:
    (a) "Flávio sozinho" = 22.
    (b) "bloco de direita" = 22 + 55 + 30 + 14.
    (c) "a que melhor reproduz" = escolhida por regra, sem olhar R²: entre as 25 candidatas da família
        abaixo, a de menor soma dos quadrados das diferenças entre o x calculado e o x legível em PI (25),
        BA (30) e SC (75). Empate: a primeira na ordem da lista. Família: numeradores N1 = 22;
        N2 = 22+55+30+14; N3 = N2+70; N4 = N3+27+35 (tudo menos a esquerda); N5 = todos menos o 13
        (100 menos Lula); N6 = 22+55; N7 = 22+55+30; N8 = 22+14; cada um sobre três denominadores
        (válidos, comparecimento, aptos do 1º turno); mais N0 = fatia de Flávio nos válidos do 2º turno
        (diagnóstico: se N0 ganhar, o gráfico pôs o 2º turno contra ele mesmo).
    O y legível (PI 3,1; BA 2,5; SC 0,4) é conferido contra o y calculado, que não depende da definição.
    Os outros pontos legíveis (MG perto de x 69 e y 0,5; RS e SP perto de x 60 a 63 e y 0,7 a 0,85) não
    entram na regra, porque os rótulos podem estar imprecisos; relato a que distância ficam e quais UFs
    estão mais perto dessas posições.
    Sensibilidades relatadas ao lado: N3, N4 e N5 sobre os válidos.
D5. y = L2 / R2 (votos de Lula sobre votos de Flávio no 2º turno), por UF.
D6. Ajustes, sem peso, um ponto por UF: linear y = a + b x; quadrático y = a + b x + c x²; exponencial
    y = a * exp(b x) de dois modos: (i) mínimos quadrados de ln y contra x, com o R² na escala do log e
    também na escala de y; (ii) mínimos quadrados não lineares na escala de y (projeção de a e busca de b
    em grade refinada, partindo de uma grade larga). R² = 1 menos soma dos quadrados dos resíduos sobre a
    soma dos quadrados em torno da média de y. O "R² do exponencial" que comparo com o gráfico é o (ii);
    o (i) vai ao lado. "Melhor ajuste" = o maior entre linear, quadrático e exponencial (ii).
    A tarefa escreve a fórmula como "y = a x exp(b x)"; leio o primeiro x como sinal de multiplicação.
    A leitura literal y = a * x * exp(b x) é rodada ao lado, por mínimos quadrados não lineares.
D7. Resíduo em pontos de fatia: p2 = 100 * R2 / (L2 + R2) (fatia de Flávio nos válidos do 2º turno);
    reta de mínimos quadrados de p2 contra x, sem peso, nas 27 UFs; desvio-padrão dos resíduos =
    raiz(soma dos quadrados / (n menos 2)). Ao lado: raiz(soma / n) e o maior resíduo em módulo.
D8. Outros anos (J2): x = R1 / (L1 + R1 + O1) ("adversário sozinho") e x = (R1 + O1) / (L1 + R1 + O1)
    ("adversário mais outros", igual a 100 menos a fatia do PT); y = L2 / R2. Em 2026 as mesmas duas
    contas saem ao lado, para comparar igual com igual.
D9. Qual definição entra em cada cláusula da leitura (o registro não diz):
    - "R² do melhor ajuste >= 0,98 na mediana da simulação com ruído de 5 pontos": versão A da simulação
      (taxas publicadas), ruído independente, x = definição (c); para cada sorteio tomo o maior dos três
      R² e depois a mediana dos 1.000 sorteios.
    - "e em pelo menos dois dos outros anos": 2022, 2018 e 2014 com x = adversário sozinho (a letra do
      registro: "com o adversário do PT no lugar da direita").
    - "desvio-padrão dos resíduos de 2026 menor que a metade do menor dos outros anos": x = adversário
      sozinho nos quatro anos (em 2026, Flávio sozinho), a única definição que existe igual nos quatro.
    - "abaixo do percentil 1 da simulação com ruído de 2 pontos": versão A, ruído independente, mesma
      definição de x (Flávio sozinho). Percentil com interpolação linear (numpy).
    Ao lado, as quatro cláusulas com as outras definições (bloco de direita, definição (c), adversário
    mais outros), com as outras versões da simulação e com o ruído comum, e digo se a leitura mudaria.
    Se nenhuma das duas leituras valer pela letra: "NENHUMA DAS DUAS PELA LETRA (INCONCLUSIVO)". Se as
    duas valerem: relato as duas e o conflito.
D10. Simulação (J3). Estoques por UF do 1º turno de 2026: L1, R1, E70, E14, E55, Edem (demais nominais,
    inclusive o 28, como na matriz do A2), B1, N1 e A1 = aptos menos comparecimento. Em cada UF o voto
    do 2º turno de Lula é a soma dos estoques vezes a taxa de cada bloco para Lula; o de Flávio, idem.
    Versões das taxas nacionais (para Lula, para Flávio):
    A (principal, publicada em R27_A2, matriz de 2026): L1 (0,9845; 0,0097), R1 (0,0174; 0,9454),
       E70 (0,4738; 0,3144), E14 (0,3294; 0,3022), E55 (0,4337; 0,4906), Edem (0,4670; 0,3630),
       B1 (0,4558; 0,1757), N1 (0,5044; 0,2109), A1 (0,1129; 0,0572). Aviso: estas taxas foram
       estimadas com o próprio 2º turno de 2026, que é o resultado sob suspeita; por isso rodam também
       as versões B, C e D, que não usam nenhum dado do 2º turno.
    B (simples e simétrica, declarada): L1 (0,95; 0,02), R1 (0,02; 0,95), cada eliminado (0,40; 0,40),
       B1 e N1 (0,30; 0,30), A1 (0,05; 0,05).
    C (arbitrária com finalistas fiéis, sorteada a cada sorteio): cada finalista guarda uma parcela
       uniforme entre 0,80 e 1,00 e cede ao rival uma parcela uniforme entre 0 e o que sobra; os outros
       sete blocos se dividem (Lula, Flávio, resto) ao acaso, uniforme no simplex.
    D (inteiramente arbitrária): os nove blocos, inclusive os finalistas, uniforme no simplex. Na
       versão D relato também a distribuição separada dos sorteios em que os dois finalistas guardam
       pelo menos metade dos seus eleitores.
    Ruído: o registro diz "um ruído sorteado por UF ... nas taxas". Principal (independente): um ruído
    normal de média 0 e desvio 0,02, 0,05 ou 0,10 para cada UF, cada bloco e cada destino. Ao lado
    (comum, o mais duro contra a tese de "propriedade do gráfico"): um só sorteio por UF, somado às taxas
    de todos os blocos para Lula e subtraído das taxas para Flávio. Em qualquer caso a taxa é cortada em
    0 e 1 e, se as duas somarem mais de 1, são reduzidas na mesma proporção. 1.000 sorteios por nível,
    semente 20261129 mais os índices da versão, do tipo de ruído e do nível.
    Para cada sorteio: R² dos três ajustes de y contra x (definições (a), (b), (c) e "tudo menos Lula"),
    o maior deles, e o desvio-padrão dos resíduos de p2 sobre a reta (D7).
    Ao lado, fora da leitura: níveis de ruído 0 (sem ruído), 0,5 e 1 ponto na versão A, para dizer a que
    nível de ruído os dados reais de 2026 equivalem; e a "curva pura": y = (100 menos x) / x calculado
    só com o x real de cada UF, sem nenhum dado do 2º turno, com os três ajustes.
D11. Calibração do gráfico com fraude plantada (não está no registro; declarada aqui). Hipótese do Léo:
    o resultado oficial contém T = 2.215.096 votos trocados de Flávio para Lula (metade da margem oficial
    de 4.430.191, arredondada para cima). Desfaço a troca de dois modos e refaço o gráfico: (i) uniforme,
    a mesma fração dos válidos do 2º turno em toda UF; (ii) concentrada nas 9 UFs do Nordeste, proporcional
    aos válidos de cada uma. Comparo os R² e o desvio-padrão dos resíduos do resultado oficial com os dos
    dois resultados "sem a troca". Se forem praticamente iguais, o gráfico não distingue uma eleição com
    essa troca de uma sem ela, e portanto não serve nem para provar nem para afastar a fraude.
D12. J4. Município = (UF, código do município), Brasil sem exterior. Seção = seções do Brasil com os dois
    turnos. Entram as unidades com válidos do 1º turno > 0 e R2 > 0 (y exige R2 > 0; o número de
    excluídas é relatado). Para cada nível e definição de x: R² dos três ajustes de y, sem peso (um ponto
    por unidade, como no gráfico) e, ao lado, com peso L2 + R2; correlação de postos (Spearman) entre x
    e y; R² e desvio-padrão dos resíduos da reta de p2 contra x; percentis 1, 5, 25, 50, 75, 95 e 99 dos
    resíduos. O ajuste no log usa só as unidades com y > 0. Por UF: x, p2, previsto pela reta, resíduo,
    na definição (c) e em Flávio sozinho; resíduo positivo = Flávio acima do previsto.
D13. Arredondamento só na impressão; os limiares são comparados com os valores sem arredondar.

O QUE FOR FEITO DEPOIS DE VER O RESULTADO fica em funções com nome "exploratorio_" e sai marcado assim.
"""
import sys, os, json, time, math
import numpy as np

RAIZ = '/home/user/casa-control/eleicao-2026'
DADOS = RAIZ + '/dados'
SAIDA_JSON = RAIZ + '/resultados/R29_matematica_impossivel.json'
SAIDA_TXT = RAIZ + '/resultados/R29_matematica_impossivel.txt'
sys.path.insert(0, RAIZ + '/scripts')
from lib import carregar  # noqa: E402

SEMENTE = 20261129
NSORT = 1000
ANOS = [2026, 2022, 2018, 2014]
NOME_PT = {2026: 'Lula', 2022: 'Lula', 2018: 'Haddad', 2014: 'Dilma'}
NOME_ADV = {2026: 'Flávio', 2022: 'Bolsonaro', 2018: 'Bolsonaro', 2014: 'Aécio'}
CAND = ['22', '13', '70', '14', '55', '30', '80', '16', '27', '21', '35', '29', '28']
VALIDOS = [c for c in CAND if c != '28']
PARTIDO = {'22': 'PL', '13': 'PT', '70': 'Avante', '14': 'Missão', '55': 'PSD', '30': 'Novo', '80': 'UP',
           '16': 'PSTU', '27': 'DC', '21': 'PCB', '35': 'PMB', '29': 'PCO', '28': 'anulado'}
CLASSE = {'22': 'direita (finalista)', '13': 'esquerda (finalista)', '70': 'centro ou indefinido',
          '14': 'direita', '55': 'direita', '30': 'direita', '80': 'esquerda', '16': 'esquerda',
          '27': 'indefinido', '21': 'esquerda', '35': 'indefinido', '29': 'esquerda',
          '28': 'candidatura anulada, fora dos válidos'}
NUMERADORES = [
    ('N1 Flávio sozinho (22)', ['22']),
    ('N2 bloco de direita (22+55+30+14)', ['22', '55', '30', '14']),
    ('N3 bloco mais Cury (22+55+30+14+70)', ['22', '55', '30', '14', '70']),
    ('N4 tudo menos a esquerda (22+55+30+14+70+27+35)', ['22', '55', '30', '14', '70', '27', '35']),
    ('N5 tudo menos Lula', [c for c in VALIDOS if c != '13']),
    ('N6 Flávio e Caiado (22+55)', ['22', '55']),
    ('N7 Flávio, Caiado e Zema (22+55+30)', ['22', '55', '30']),
    ('N8 Flávio e Renan (22+14)', ['22', '14']),
]
DENOMINADORES = [('válidos', 'val'), ('comparecimento', 'comp1'), ('aptos', 'apt1')]
LEGIVEL = {'PI': (25.0, 3.1), 'BA': (30.0, 2.5), 'SC': (75.0, 0.4)}
LEGIVEL_DUVIDOSO = {'MG': (69.0, 0.5), 'RS': (61.5, 0.775), 'SP': (61.5, 0.775)}
GRAFICO_R2 = {'linear': 0.935, 'quadratico': 0.995, 'exponencial': 0.999}
NORDESTE = ['AL', 'BA', 'CE', 'MA', 'PB', 'PE', 'PI', 'RN', 'SE']
T_PLANTIO = 2215096
BLOCOS = ['L1', 'R1', 'E70', 'E14', 'E55', 'Edem', 'B1', 'N1', 'A1']
TAXAS_A = [(0.9845, 0.0097), (0.0174, 0.9454), (0.4738, 0.3144), (0.3294, 0.3022), (0.4337, 0.4906),
           (0.4670, 0.3630), (0.4558, 0.1757), (0.5044, 0.2109), (0.1129, 0.0572)]
TAXAS_B = [(0.95, 0.02), (0.02, 0.95), (0.40, 0.40), (0.40, 0.40), (0.40, 0.40), (0.40, 0.40),
           (0.30, 0.30), (0.30, 0.30), (0.05, 0.05)]
NIVEIS = [0.02, 0.05, 0.10]
NIVEIS_EXTRA = [0.0, 0.005, 0.01]
QUANTIS = [1, 5, 25, 50, 75, 95, 99]
CAMPOS = ['L', 'R', 'O', 'B', 'N', 'comp', 'apt']


# ------------------------------------------------------------------ leitura e agregação
def _num(v):
    return v if isinstance(v, (int, float)) and not isinstance(v, bool) else 0


def ler_ano(ano, cand=None):
    """Agrega uma base por UF e por município; em 2026 devolve também os vetores por seção."""
    d = carregar(f'{DADOS}/secoes{ano}.json.gz')
    uf, mun = {}, {}
    sec = []
    nsec = {'1': 0, '2': 0, 'ambos': 0}
    for k, s in d.items():
        u, m, _, _ = k.split('|')
        km = u + '|' + m
        au = uf.setdefault(u, {})
        am = mun.setdefault(km, {})
        t1, t2 = s.get('1'), s.get('2')
        for t, tag in ((t1, '1'), (t2, '2')):
            if not isinstance(t, dict):
                continue
            nsec[tag] += 1
            for c in CAMPOS:
                v = _num(t.get(c))
                au[c + tag] = au.get(c + tag, 0) + v
                am[c + tag] = am.get(c + tag, 0) + v
        cs = None
        if cand is not None and isinstance(t1, dict):
            cs = cand.get(k, {})
            for n, v in cs.items():
                au['c' + n] = au.get('c' + n, 0) + v
                am['c' + n] = am.get('c' + n, 0) + v
        if isinstance(t1, dict) and isinstance(t2, dict):
            nsec['ambos'] += 1
            if cand is not None and u != 'ZZ':
                sec.append((u, _num(t1.get('L')), _num(t1.get('R')), _num(t1.get('O')), _num(t1.get('comp')),
                            _num(t1.get('apt')), _num(t2.get('L')), _num(t2.get('R')))
                           + tuple(cs.get(n, 0) for n in CAND))
    del d
    return {'uf': uf, 'mun': mun, 'nsec': nsec}, sec


def carregar_tudo(cache=None):
    arq_ag = os.path.join(cache, 'agregados.json') if cache else None
    arq_sec = os.path.join(cache, 'secoes2026.npz') if cache else None
    if cache and os.path.exists(arq_ag) and os.path.exists(arq_sec):
        with open(arq_ag) as f:
            ag = {int(k): v for k, v in json.load(f).items()}
        z = np.load(arq_sec, allow_pickle=False)
        return ag, {k: z[k] for k in z.files}, 'cache'
    cj = carregar(f'{DADOS}/candidatos2026_1t.json.gz')
    cand, nomes, totais = cj['secoes'], cj['nomes'], cj['totais']
    ag = {}
    a, sec = ler_ano(2026, cand)
    a['nomes'] = nomes
    a['totais'] = totais
    ag[2026] = a
    del cand, cj
    cols = ['L1', 'R1', 'O1', 'comp1', 'apt1', 'L2', 'R2'] + ['c' + n for n in CAND]
    S = {'uf': np.array([r[0] for r in sec])}
    M = np.array([r[1:] for r in sec], dtype=np.int64)
    for i, c in enumerate(cols):
        S[c] = M[:, i]
    del sec, M
    for ano in (2022, 2018, 2014):
        ag[ano], _ = ler_ano(ano)
    if cache:
        os.makedirs(cache, exist_ok=True)
        with open(arq_ag, 'w') as f:
            json.dump(ag, f)
        np.savez_compressed(arq_sec, **S)
    return ag, S, 'bases'


# ------------------------------------------------------------------ ajustes
def _mq(X, Y, w=None):
    """Mínimos quadrados de cada linha de Y (m, n) contra X (n, k). Devolve coeficientes (m, k) e previsto."""
    if w is None:
        beta = np.linalg.lstsq(X, Y.T, rcond=None)[0]
    else:
        sw = np.sqrt(w)
        beta = np.linalg.lstsq(X * sw[:, None], (Y * sw).T, rcond=None)[0]
    return beta.T, (X @ beta).T


def _r2(Y, P, w=None):
    w = np.ones(Y.shape[1]) if w is None else w
    med = (Y * w).sum(1, keepdims=True) / w.sum()
    sst = (w * (Y - med) ** 2).sum(1)
    ssr = (w * (Y - P) ** 2).sum(1)
    with np.errstate(divide='ignore', invalid='ignore'):
        return 1 - ssr / sst


def exp_nls(z, Y, w=None, mult=None, lim=40.0, ng=321, rodadas=4):
    """Mínimos quadrados não lineares de y = a * g(z) * exp(b z), g = 1 (padrão) ou mult.
    Para b fixo, a ótimo = soma(w y e) / soma(w e²); busca b em grade larga e refina 4 vezes.
    Devolve a (m,), b (m,) em unidades de z, e o previsto (m, n)."""
    m, n = Y.shape
    w_ = np.ones(n) if w is None else w
    g = np.ones(n) if mult is None else mult
    zc = z - z.mean()
    Yw = Y * w_
    bloco = max(1, int(2e7 // (m * n)))

    def Q(B):
        G = B.shape[1]
        q = np.empty((m, G)); a = np.empty((m, G))
        for i in range(0, G, bloco):
            E = g[None, None, :] * np.exp(B[:, i:i + bloco, None] * zc[None, None, :])
            num = (E * Yw[:, None, :]).sum(2)
            den = (E * E * w_[None, None, :]).sum(2)
            q[:, i:i + bloco] = num * num / den
            a[:, i:i + bloco] = num / den
        return q, a

    while True:
        grade = np.linspace(-lim, lim, ng)
        q, a = Q(np.broadcast_to(grade, (m, ng)))
        j = np.argmax(q, 1)
        if ((j == 0) | (j == ng - 1)).any() and lim < 300:
            lim = min(300.0, lim * 2)
            continue
        break
    b = grade[j]
    passo = 2 * lim / (ng - 1)
    for _ in range(rodadas):
        B = b[:, None] + np.linspace(-passo, passo, 41)[None, :]
        q, a = Q(B)
        j = np.argmax(q, 1)
        b = B[np.arange(m), j]
        passo = passo / 20
    a_c = a[np.arange(m), j]
    P = a_c[:, None] * g[None, :] * np.exp(b[:, None] * zc[None, :])
    a0 = a_c * np.exp(-b * z.mean())
    return a0, b, P


def r2_lote(x, Y, w=None, detalhe=False):
    """R² dos ajustes de cada linha de Y (m, n) contra x (em pontos percentuais)."""
    z = x / 100.0
    n = len(z)
    X1 = np.column_stack([np.ones(n), z])
    X2 = np.column_stack([np.ones(n), z, z * z])
    b1, P1 = _mq(X1, Y, w)
    b2, P2 = _mq(X2, Y, w)
    out = {'linear': _r2(Y, P1, w), 'quadratico': _r2(Y, P2, w)}
    pos = (Y > 0).all(0) if Y.shape[0] == 1 else np.ones(n, bool)
    if (Y[:, pos] > 0).all():
        lY = np.log(Y[:, pos])
        wl = None if w is None else w[pos]
        bl, Pl = _mq(X1[pos], lY, wl)
        out['exp_log_escala_log'] = _r2(lY, Pl, wl)
        Pe = np.exp(bl[:, [0]] + bl[:, [1]] * z[None, :])
        out['exp_log_escala_y'] = _r2(Y, Pe, w)
    else:
        bl = np.full((Y.shape[0], 2), np.nan)
        out['exp_log_escala_log'] = np.full(Y.shape[0], np.nan)
        out['exp_log_escala_y'] = np.full(Y.shape[0], np.nan)
    a, b, Pn = exp_nls(z, Y, w)
    out['exponencial'] = _r2(Y, Pn, w)
    out['melhor'] = np.maximum(np.maximum(out['linear'], out['quadratico']), out['exponencial'])
    if detalhe:
        a3, b3, P3 = exp_nls(z, Y, w, mult=z * 100.0)
        out['exp_literal_a_x_exp_bx'] = _r2(Y, P3, w)
        out['coef'] = {
            'linear': {'a': float(b1[0, 0]), 'b_por_ponto': float(b1[0, 1] / 100)},
            'quadratico': {'a': float(b2[0, 0]), 'b_por_ponto': float(b2[0, 1] / 100),
                           'c_por_ponto2': float(b2[0, 2] / 1e4)},
            'exp_log': {'a': float(np.exp(bl[0, 0])), 'b_por_ponto': float(bl[0, 1] / 100)},
            'exponencial': {'a': float(a[0]), 'b_por_ponto': float(b[0] / 100)},
        }
        out['n_fora_do_log'] = int((~pos).sum())
    return out


def ajustes_um(x, y, w=None):
    r = r2_lote(np.asarray(x, float), np.asarray(y, float)[None, :], w, detalhe=True)
    return {k: (float(v[0]) if isinstance(v, np.ndarray) else v) for k, v in r.items()}


def residuos_reta(x, P2, w=None):
    """Reta de p2 contra x. P2 (m, n). Devolve dp (n menos 2), dp (n), maior módulo, R², resíduos, coef."""
    n = len(x)
    X = np.column_stack([np.ones(n), np.asarray(x, float)])
    b, P = _mq(X, P2, w)
    E = P2 - P
    w_ = np.ones(n) if w is None else w
    ssr = (w_ * E * E).sum(1)
    if w is None:
        dp = np.sqrt(ssr / (n - 2)); dp0 = np.sqrt(ssr / n)
    else:
        dp = np.sqrt(ssr / w_.sum() * n / (n - 2)); dp0 = np.sqrt(ssr / w_.sum())
    return {'dp': dp, 'dp_n': dp0, 'max': np.abs(E).max(1), 'r2': _r2(P2, P, w), 'res': E, 'coef': b, 'prev': P}


def quantis(v):
    v = np.asarray(v, float)
    d = {f'p{q}': float(np.percentile(v, q)) for q in QUANTIS}
    d['media'] = float(v.mean())
    d['min'] = float(v.min()); d['max'] = float(v.max())
    return d


# ------------------------------------------------------------------ tabelas por UF
def tabela(dic, chaves, campos):
    return {c: np.array([dic[k].get(c, 0) for k in chaves], dtype=float) for c in campos}


def campos_ano(ano):
    c = [f + t for f in CAMPOS for t in ('1', '2')]
    if ano == 2026:
        c += ['c' + n for n in CAND]
    return c


def monta(ag, ano, nivel='uf', com_zz=False):
    dic = ag[ano][nivel]
    chaves = sorted(k for k in dic if com_zz or not k.startswith('ZZ'))
    T = tabela(dic, chaves, campos_ano(ano))
    if ano == 2026:
        T['val'] = sum(T['c' + n] for n in VALIDOS)
    else:
        T['val'] = T['L1'] + T['R1'] + T['O1']
    return chaves, T


def x2026(T, nums, den='val'):
    with np.errstate(divide='ignore', invalid='ignore'):
        return 100.0 * sum(T['c' + n] for n in nums) / T[den]


# ------------------------------------------------------------------ J1
def j1(ag):
    ufs, T = monta(ag, 2026)
    assert len(ufs) == 27, len(ufs)
    y = T['L2'] / T['R2']
    p2 = 100 * T['R2'] / (T['L2'] + T['R2'])
    iu = {u: i for i, u in enumerate(ufs)}
    familia = []
    for rot, nums in NUMERADORES:
        for dn, dc in DENOMINADORES:
            x = x2026(T, nums, dc)
            sq = sum((x[iu[u]] - LEGIVEL[u][0]) ** 2 for u in LEGIVEL)
            familia.append({'definicao': f'{rot} sobre {dn}', 'nums': nums, 'den': dc,
                            'x_PI': float(x[iu['PI']]), 'x_BA': float(x[iu['BA']]), 'x_SC': float(x[iu['SC']]),
                            'soma_quadrados': float(sq)})
    sq0 = sum((p2[iu[u]] - LEGIVEL[u][0]) ** 2 for u in LEGIVEL)
    familia.append({'definicao': 'N0 fatia de Flávio nos válidos do 2º turno (diagnóstico)', 'nums': None, 'den': None,
                    'x_PI': float(p2[iu['PI']]), 'x_BA': float(p2[iu['BA']]), 'x_SC': float(p2[iu['SC']]),
                    'soma_quadrados': float(sq0)})
    melhor = min(range(len(familia)), key=lambda i: (familia[i]['soma_quadrados'], i))
    fm = familia[melhor]
    defs = {
        'a_flavio_sozinho': x2026(T, ['22']),
        'b_bloco_direita': x2026(T, ['22', '55', '30', '14']),
        'c_melhor_reproduz': p2.copy() if fm['nums'] is None else x2026(T, fm['nums'], fm['den']),
        's_bloco_mais_cury': x2026(T, NUMERADORES[2][1]),
        's_tudo_menos_esquerda': x2026(T, NUMERADORES[3][1]),
        's_tudo_menos_lula': x2026(T, NUMERADORES[4][1]),
    }
    res = {'ufs': ufs, 'y': y.tolist(), 'p2': p2.tolist(), 'familia': familia,
           'definicao_c': fm['definicao'], 'definicoes': {}}
    for nome, x in defs.items():
        a = ajustes_um(x, y)
        rr = residuos_reta(x, p2[None, :])
        res['definicoes'][nome] = {
            'x': x.tolist(), 'ajustes': a,
            'reta_p2': {'dp': float(rr['dp'][0]), 'dp_n': float(rr['dp_n'][0]), 'max': float(rr['max'][0]),
                        'r2': float(rr['r2'][0]), 'intercepto': float(rr['coef'][0, 0]),
                        'inclinacao': float(rr['coef'][0, 1]), 'residuos': rr['res'][0].tolist(),
                        'previsto': rr['prev'][0].tolist()},
            'legiveis': {u: {'x_calc': float(x[iu[u]]), 'x_grafico': LEGIVEL[u][0],
                             'y_calc': float(y[iu[u]]), 'y_grafico': LEGIVEL[u][1]} for u in LEGIVEL},
        }
    # pontos de rótulo duvidoso: onde está a UF e quais UFs estão perto da posição lida
    xc = defs['c_melhor_reproduz']
    duv = {}
    for u, (xl, yl) in LEGIVEL_DUVIDOSO.items():
        dist = np.sqrt(((xc - xl) / 50.0) ** 2 + ((y - yl) / 2.7) ** 2)  # distância em fração da largura dos eixos
        ordem = np.argsort(dist)[:3]
        duv[u] = {'x_grafico': xl, 'y_grafico': yl, 'x_calc': float(xc[iu[u]]), 'y_calc': float(y[iu[u]]),
                  'ufs_mais_perto_da_posicao': [{'uf': ufs[i], 'x': float(xc[i]), 'y': float(y[i])} for i in ordem]}
    res['rotulos_duvidosos'] = duv
    # exterior como 28º ponto
    ufz, Tz = monta(ag, 2026, com_zz=True)
    if 'ZZ' in ufz:
        yz = Tz['L2'] / Tz['R2']
        res['com_exterior'] = {}
        for nome, nums in (('a_flavio_sozinho', ['22']), ('b_bloco_direita', ['22', '55', '30', '14'])):
            xz = x2026(Tz, nums)
            a = ajustes_um(xz, yz)
            i = ufz.index('ZZ')
            res['com_exterior'][nome] = {'x_ZZ': float(xz[i]), 'y_ZZ': float(yz[i]),
                                         'linear': a['linear'], 'quadratico': a['quadratico'],
                                         'exponencial': a['exponencial']}
    # conferências de soma
    nac = {c: float(T[c].sum()) for c in ('L1', 'R1', 'O1', 'L2', 'R2')}
    res['conferencia'] = {
        'soma_27_ufs': nac,
        'c22_igual_R1': bool((T['c22'] == T['R1']).all()), 'c13_igual_L1': bool((T['c13'] == T['L1']).all()),
        'outros_mais_28_igual_O1': bool((sum(T['c' + n] for n in CAND if n not in ('13', '22')) == T['O1']).all()),
    }
    return res, ufs, T, defs, y, p2


# ------------------------------------------------------------------ J2
def j2(ag):
    out = {}
    for ano in ANOS:
        ufs, T = monta(ag, ano)
        assert len(ufs) == 27, (ano, len(ufs))
        val = T['L1'] + T['R1'] + T['O1']
        if ano == 2026:
            val = T['val']
            xo = 100 * (T['val'] - T['c13']) / val
        else:
            xo = 100 * (T['R1'] + T['O1']) / val
        xr = 100 * T['R1'] / val
        y = T['L2'] / T['R2']
        p2 = 100 * T['R2'] / (T['L2'] + T['R2'])
        d = {'ufs': ufs, 'y': y.tolist(), 'p2': p2.tolist(),
             'nacional': {'L1': float(T['L1'].sum()), 'R1': float(T['R1'].sum()), 'O1': float(T['O1'].sum()),
                          'L2': float(T['L2'].sum()), 'R2': float(T['R2'].sum())}}
        for nome, x in (('adversario_sozinho', xr), ('adversario_mais_outros', xo)):
            a = ajustes_um(x, y)
            rr = residuos_reta(x, p2[None, :])
            d[nome] = {'x': x.tolist(), 'ajustes': a,
                       'reta_p2': {'dp': float(rr['dp'][0]), 'dp_n': float(rr['dp_n'][0]), 'max': float(rr['max'][0]),
                                   'r2': float(rr['r2'][0]), 'intercepto': float(rr['coef'][0, 0]),
                                   'inclinacao': float(rr['coef'][0, 1]), 'residuos': rr['res'][0].tolist()}}
        out[str(ano)] = d
    return out


# ------------------------------------------------------------------ J3
def taxas_sorteadas(versao, rng, m):
    nb = len(BLOCOS)
    if versao == 'A':
        return np.broadcast_to(np.array(TAXAS_A), (m, nb, 2)).copy()
    if versao == 'B':
        return np.broadcast_to(np.array(TAXAS_B), (m, nb, 2)).copy()
    nat = rng.dirichlet([1.0, 1.0, 1.0], size=(m, nb))[:, :, :2].copy()
    if versao == 'C':
        ret = rng.uniform(0.80, 1.00, size=(m, 2))
        ced = rng.uniform(0.0, 1.0, size=(m, 2)) * (1 - ret)
        nat[:, 0, 0] = ret[:, 0]; nat[:, 0, 1] = ced[:, 0]
        nat[:, 1, 1] = ret[:, 1]; nat[:, 1, 0] = ced[:, 1]
    return nat


def simular(S, nat, sigma, tipo, rng):
    """S (n, nb) estoques; nat (m, nb, 2) taxas nacionais. Devolve L2, R2 (m, n)."""
    m, nb, _ = nat.shape
    n = S.shape[0]
    tx = np.broadcast_to(nat[:, None, :, :], (m, n, nb, 2)).copy()
    if sigma > 0:
        if tipo == 'independente':
            tx += rng.normal(0.0, sigma, size=(m, n, nb, 2))
        else:
            d = rng.normal(0.0, sigma, size=(m, n, 1))
            tx[..., 0] += d
            tx[..., 1] -= d
    np.clip(tx, 0.0, 1.0, out=tx)
    s = tx.sum(-1, keepdims=True)
    tx = np.where(s > 1, tx / np.where(s > 0, s, 1), tx)
    L2 = (S[None, :, :] * tx[..., 0]).sum(2)
    R2 = (S[None, :, :] * tx[..., 1]).sum(2)
    return L2, R2


def j3(T, defs, y_real, p2_real):
    S = np.column_stack([T['L1'], T['R1'], T['c70'], T['c14'], T['c55'],
                         T['O1'] - T['c70'] - T['c14'] - T['c55'], T['B1'], T['N1'], T['apt1'] - T['comp1']])
    xs = {'a_flavio_sozinho': defs['a_flavio_sozinho'], 'b_bloco_direita': defs['b_bloco_direita'],
          'c_melhor_reproduz': defs['c_melhor_reproduz'], 's_tudo_menos_lula': defs['s_tudo_menos_lula']}
    real = {}
    for nome, x in xs.items():
        a = r2_lote(x, y_real[None, :])
        real[nome] = {'melhor': float(a['melhor'][0]), 'dp': float(residuos_reta(x, p2_real[None, :])['dp'][0])}
    out = {'estoques_nacionais': dict(zip(BLOCOS, S.sum(0).tolist())), 'real_2026': real, 'cenarios': {}}
    planos = [(v, t, s) for v in 'ABCD' for t in ('independente', 'comum') for s in NIVEIS]
    planos += [('A', 'independente', s) for s in NIVEIS_EXTRA]
    for v, t, s in planos:
        iv, it = 'ABCD'.index(v), ('independente', 'comum').index(t)
        rng = np.random.default_rng([SEMENTE, iv, it, int(round(s * 10000))])
        m = 1 if s == 0 else NSORT
        nat = taxas_sorteadas(v, rng, m)
        L2, R2 = simular(S, nat, s, t, rng)
        with np.errstate(divide='ignore', invalid='ignore'):
            Y = L2 / R2
        # Acrescentado depois de ver o resultado: sorteio em que alguma UF fica com zero voto de um dos dois
        # (razão infinita ou nula) sai da conta e é contado. Só acontece na versão D com ruído comum.
        ok = np.isfinite(Y).all(1) & (Y > 0).all(1)
        L2, R2, Y, nat = L2[ok], R2[ok], Y[ok], nat[ok]
        P2 = 100 * R2 / (L2 + R2)
        cen = {'versao': v, 'ruido': t, 'desvio_pontos': s * 100, 'sorteios': m,
               'sorteios_validos': int(ok.sum()), 'definicoes': {}}
        fieis = (nat[:, 0, 0] >= 0.5) & (nat[:, 1, 1] >= 0.5)
        for nome, x in xs.items():
            a = r2_lote(x, Y)
            rr = residuos_reta(x, P2)
            d = {k: quantis(a[k]) for k in ('linear', 'quadratico', 'exponencial', 'exp_log_escala_log', 'melhor')}
            d['dp_residuos'] = quantis(rr['dp'])
            d['fracao_melhor_ge_098'] = float((a['melhor'] >= 0.98).mean())
            d['fracao_melhor_ge_0995'] = float((a['melhor'] >= 0.995).mean())
            d['fracao_melhor_ge_0999'] = float((a['melhor'] >= 0.999).mean())
            d['fracao_melhor_ge_real'] = float((a['melhor'] >= real[nome]['melhor']).mean())
            d['fracao_dp_menor_que_real'] = float((rr['dp'] < real[nome]['dp']).mean())
            if v == 'D':
                d['finalistas_guardam_metade'] = {
                    'sorteios': int(fieis.sum()),
                    'melhor': quantis(a['melhor'][fieis]) if fieis.sum() else None,
                    'melhor_nos_demais': quantis(a['melhor'][~fieis]) if (~fieis).sum() else None}
            cen['definicoes'][nome] = d
        out['cenarios'][f'{v}|{t}|{s * 100:g}'] = cen
    # curva pura: nenhum dado do 2º turno
    pura = {}
    for nome, x in list(xs.items()) + [('p2_real_contra_ele_mesmo', p2_real)]:
        a = ajustes_um(x, (100 - x) / x)
        pura[nome] = {k: a[k] for k in ('linear', 'quadratico', 'exponencial', 'exp_log_escala_log')}
    out['curva_pura'] = pura
    return out


# ------------------------------------------------------------------ D11 fraude plantada
def calibracao(ufs, T, x, nac_L2, nac_R2):
    L2, R2 = T['L2'].copy(), T['R2'].copy()
    val2 = L2 + R2
    out = {'T': T_PLANTIO}
    f = T_PLANTIO / (nac_L2 + nac_R2)
    ne = np.array([u in NORDESTE for u in ufs])
    mov_u = f * val2
    mov_c = np.where(ne, T_PLANTIO * val2 / val2[ne].sum(), 0.0)
    for nome, mov in (('oficial', np.zeros(len(ufs))), ('sem_troca_uniforme', mov_u), ('sem_troca_concentrada_nordeste', mov_c)):
        l, r = L2 - mov, R2 + mov
        a = ajustes_um(x, l / r)
        rr = residuos_reta(x, (100 * r / (l + r))[None, :])
        out[nome] = {'votos_movidos_nas_27_ufs': float(mov.sum()), 'linear': a['linear'], 'quadratico': a['quadratico'],
                     'exponencial': a['exponencial'], 'exp_log_escala_log': a['exp_log_escala_log'],
                     'melhor': a['melhor'], 'dp_residuos': float(rr['dp'][0]),
                     'fatia_flavio_27_ufs': float(100 * r.sum() / (l.sum() + r.sum()))}
    out['fracao_uniforme_dos_validos'] = f
    out['fracao_concentrada_dos_validos_do_nordeste'] = float(T_PLANTIO / val2[ne].sum())
    return out


# ------------------------------------------------------------------ J4
def spearman(x, y):
    from scipy.stats import rankdata
    rx, ry = rankdata(x), rankdata(y)
    return float(np.corrcoef(rx, ry)[0, 1])


def nivel_fino(xdefs, val1, L2, R2):
    """xdefs: nome -> x (pode ter nan). Devolve as medidas do gráfico num nível fino (município ou seção)."""
    out = {'unidades': int(len(L2))}
    base = (val1 > 0) & ((L2 + R2) > 0)
    ok = base & (R2 > 0)
    out['com_validos_e_votos_no_2t'] = int(base.sum())
    out['excluidas_por_R2_zero'] = int((base & (R2 == 0)).sum())
    out['usadas'] = int(ok.sum())
    y = L2[ok] / R2[ok]
    p2 = 100 * R2[ok] / (L2[ok] + R2[ok])
    w = (L2 + R2)[ok].astype(float)
    out['y'] = quantis(y)
    out['definicoes'] = {}
    for nome, x in xdefs.items():
        xx = x[ok]
        d = {}
        a = ajustes_um(xx, y)
        d['sem_peso'] = {k: a[k] for k in ('linear', 'quadratico', 'exponencial', 'exp_log_escala_log',
                                            'exp_log_escala_y', 'melhor', 'n_fora_do_log')}
        aw = ajustes_um(xx, y, w)
        d['com_peso'] = {k: aw[k] for k in ('linear', 'quadratico', 'exponencial', 'exp_log_escala_log', 'melhor')}
        d['spearman_x_y'] = spearman(xx, y)
        rr = residuos_reta(xx, p2[None, :])
        d['reta_p2'] = {'r2': float(rr['r2'][0]), 'dp': float(rr['dp'][0]), 'max': float(rr['max'][0]),
                        'inclinacao': float(rr['coef'][0, 1]), 'intercepto': float(rr['coef'][0, 0]),
                        'residuos': quantis(rr['res'][0])}
        rw = residuos_reta(xx, p2[None, :], w)
        d['reta_p2_com_peso'] = {'r2': float(rw['r2'][0]), 'dp': float(rw['dp'][0])}
        d['x'] = quantis(xx)
        out['definicoes'][nome] = d
    return out


def j4(ag, S, ufs, T, defs, p2, def_c):
    out = {}
    # município
    muns, Tm = monta(ag, 2026, 'mun')
    nums_c, den_c = def_c

    def xdefs(Tb):
        d = {'a_flavio_sozinho': x2026(Tb, ['22']), 'b_bloco_direita': x2026(Tb, ['22', '55', '30', '14'])}
        if nums_c is None:
            with np.errstate(divide='ignore', invalid='ignore'):
                d['c_melhor_reproduz'] = 100 * Tb['R2'] / (Tb['L2'] + Tb['R2'])
        else:
            d['c_melhor_reproduz'] = x2026(Tb, nums_c, den_c)
        return d
    out['municipio'] = nivel_fino(xdefs(Tm), Tm['val'], Tm['L2'], Tm['R2'])
    out['municipio']['municipios_na_base'] = len(muns)
    # seção
    Ts = {k: S[k].astype(float) for k in S if k != 'uf'}
    Ts['val'] = sum(Ts['c' + n] for n in VALIDOS)
    out['secao'] = nivel_fino(xdefs(Ts), Ts['val'], Ts['L2'], Ts['R2'])
    # por UF
    tab = {}
    for nome in ('c_melhor_reproduz', 'a_flavio_sozinho', 'b_bloco_direita', 's_tudo_menos_lula'):
        x = defs[nome]
        rr = residuos_reta(x, p2[None, :])
        linhas = [{'uf': ufs[i], 'x': float(x[i]), 'p2': float(p2[i]), 'previsto': float(rr['prev'][0, i]),
                   'residuo': float(rr['res'][0, i]), 'p2_menos_x': float(p2[i] - x[i])} for i in range(len(ufs))]
        linhas.sort(key=lambda r: r['residuo'])
        tab[nome] = {'intercepto': float(rr['coef'][0, 0]), 'inclinacao': float(rr['coef'][0, 1]),
                     'dp': float(rr['dp'][0]), 'linhas': linhas}
    out['por_uf'] = tab
    return out


# ------------------------------------------------------------------ leitura fixada
def leitura(J1, J2, J3):
    def cen(v, t, s):
        return J3['cenarios'][f'{v}|{t}|{s:g}']['definicoes']
    L = {}
    med5 = cen('A', 'independente', 5)['c_melhor_reproduz']['melhor']['p50']
    anos = {a: J2[a]['adversario_sozinho']['ajustes']['melhor'] for a in ('2022', '2018', '2014')}
    n_anos = sum(v >= 0.98 for v in anos.values())
    L['propriedade'] = {'mediana_melhor_R2_ruido5': med5, 'clausula_simulacao': bool(med5 >= 0.98),
                        'melhor_R2_outros_anos': anos, 'anos_com_098': int(n_anos),
                        'clausula_anos': bool(n_anos >= 2), 'vale': bool(med5 >= 0.98 and n_anos >= 2)}
    dp26 = J2['2026']['adversario_sozinho']['reta_p2']['dp']
    dps = {a: J2[a]['adversario_sozinho']['reta_p2']['dp'] for a in ('2022', '2018', '2014')}
    menor = min(dps.values())
    p1 = cen('A', 'independente', 2)['a_flavio_sozinho']['dp_residuos']['p1']
    L['anomalia'] = {'dp_2026': dp26, 'dp_outros_anos': dps, 'metade_do_menor': menor / 2,
                     'clausula_anos': bool(dp26 < menor / 2), 'percentil1_simulacao_ruido2': p1,
                     'clausula_simulacao': bool(dp26 < p1), 'vale': bool(dp26 < menor / 2 and dp26 < p1)}
    p, a = L['propriedade']['vale'], L['anomalia']['vale']
    L['veredito'] = ('PROPRIEDADE DO GRÁFICO' if p and not a else 'ANOMALIA DE 2026' if a and not p else
                     'AS DUAS CLÁUSULAS VALEM (CONFLITO)' if p and a else 'NENHUMA DAS DUAS PELA LETRA (INCONCLUSIVO)')
    # ao lado: as mesmas cláusulas com outras escolhas
    lado = {}
    for v in 'ABCD':
        for t in ('independente', 'comum'):
            for nome in ('a_flavio_sozinho', 'b_bloco_direita', 'c_melhor_reproduz', 's_tudo_menos_lula'):
                lado[f'{v}|{t}|{nome}'] = {
                    'mediana_melhor_R2_ruido2': cen(v, t, 2)[nome]['melhor']['p50'],
                    'mediana_melhor_R2_ruido5': cen(v, t, 5)[nome]['melhor']['p50'],
                    'mediana_melhor_R2_ruido10': cen(v, t, 10)[nome]['melhor']['p50'],
                    'p1_dp_ruido2': cen(v, t, 2)[nome]['dp_residuos']['p1'],
                    'dp_real_2026': J3['real_2026'][nome]['dp'],
                    'real_abaixo_do_p1': bool(J3['real_2026'][nome]['dp'] < cen(v, t, 2)[nome]['dp_residuos']['p1'])}
    L['ao_lado_simulacao'] = lado
    anos_o = {a: J2[a]['adversario_mais_outros']['ajustes']['melhor'] for a in ('2022', '2018', '2014')}
    dps_o = {a: J2[a]['adversario_mais_outros']['reta_p2']['dp'] for a in ('2022', '2018', '2014')}
    dp26_o = J2['2026']['adversario_mais_outros']['reta_p2']['dp']
    L['ao_lado_anos_adversario_mais_outros'] = {
        'melhor_R2': anos_o, 'anos_com_098': int(sum(v >= 0.98 for v in anos_o.values())),
        'dp_2026': dp26_o, 'dp_outros_anos': dps_o, 'metade_do_menor': min(dps_o.values()) / 2,
        'clausula_anos_anomalia': bool(dp26_o < min(dps_o.values()) / 2)}
    return L


# ------------------------------------------------------------------ texto
def n(v, d=4):
    if v is None or (isinstance(v, float) and (math.isnan(v) or math.isinf(v))):
        return 'n/d'
    return f'{v:.{d}f}'.replace('.', ',')


def mil(v):
    return f'{int(round(v)):,}'.replace(',', '.')


def sn(b):
    return 'SIM' if b else 'NÃO'


def texto(R):
    J1, J2, J3, J4, L, C = R['J1'], R['J2'], R['J3'], R['J4'], R['leitura'], R['calibracao']
    o = []
    A = o.append
    A('R29: CARROSSEL "A MATEMÁTICA IMPOSSÍVEL DA ELEIÇÃO" (R² de 99,8% por estado)')
    A('Critérios fixados antes de rodar: PRE-REGISTRO-2026-10-26.md, Adendo 29 (commit 3929135).')
    A('Decisões que o registro não fixa: D1 a D13 do docstring de scripts/analisar_R29_J.py, escritas antes das contas.')
    A('')
    A('LEITURA PELA LETRA: ' + L['veredito'])
    P, An = L['propriedade'], L['anomalia']
    A(f"  Propriedade do gráfico: mediana do melhor R² na simulação com ruído de 5 pontos = {n(P['mediana_melhor_R2_ruido5'])} "
      f"(pede 0,98 ou mais: {sn(P['clausula_simulacao'])}); outros anos com 0,98 ou mais: {P['anos_com_098']} de 3 "
      f"(2022 {n(P['melhor_R2_outros_anos']['2022'])}, 2018 {n(P['melhor_R2_outros_anos']['2018'])}, "
      f"2014 {n(P['melhor_R2_outros_anos']['2014'])}; pede 2: {sn(P['clausula_anos'])}). Vale: {sn(P['vale'])}.")
    A(f"  Anomalia de 2026: desvio-padrão dos resíduos de 2026 = {n(An['dp_2026'], 3)} ponto; outros anos: "
      f"2022 {n(An['dp_outros_anos']['2022'], 3)}, 2018 {n(An['dp_outros_anos']['2018'], 3)}, 2014 {n(An['dp_outros_anos']['2014'], 3)}; "
      f"metade do menor = {n(An['metade_do_menor'], 3)} (2026 abaixo disso: {sn(An['clausula_anos'])}); percentil 1 da simulação "
      f"com ruído de 2 pontos = {n(An['percentil1_simulacao_ruido2'], 3)} (2026 abaixo disso: {sn(An['clausula_simulacao'])}). "
      f"Vale: {sn(An['vale'])}.")
    A('')
    A('J1. REPRODUÇÃO DO GRÁFICO (27 UFs, 2026)')
    A('  Candidatos do 1º turno e classificação fixada antes: ')
    for c in CAND:
        A(f"    {c} {R['candidatos'][c]['nome']} ({PARTIDO[c]}) {mil(R['candidatos'][c]['votos'])}: {CLASSE[c]}")
    A(f"  Definição que melhor reproduz os pontos legíveis (regra D4): {J1['definicao_c']}.")
    fam = sorted(J1['familia'], key=lambda r: r['soma_quadrados'])[:6]
    A('  As seis melhores da família (x calculado em PI, BA e SC; soma dos quadrados contra 25, 30 e 75):')
    for f in fam:
        A(f"    {f['definicao']}: PI {n(f['x_PI'], 2)}, BA {n(f['x_BA'], 2)}, SC {n(f['x_SC'], 2)}; soma {n(f['soma_quadrados'], 2)}")
    dc = J1['definicoes']['c_melhor_reproduz']
    A('  y calculado contra o y lido no gráfico: ' + '; '.join(
        f"{u} {n(dc['legiveis'][u]['y_calc'], 3)} (gráfico {n(dc['legiveis'][u]['y_grafico'], 1)})" for u in LEGIVEL) + '.')
    A('  Rótulos duvidosos (posição lida no gráfico, onde a UF está de fato, e as UFs mais perto da posição lida):')
    for u, d in J1['rotulos_duvidosos'].items():
        A(f"    {u}: lido x {n(d['x_grafico'], 1)} e y {n(d['y_grafico'], 2)}; real x {n(d['x_calc'], 2)} e y {n(d['y_calc'], 3)}; "
          'perto da posição lida: ' + ', '.join(f"{p['uf']} ({n(p['x'], 1)}; {n(p['y'], 2)})" for p in d['ufs_mais_perto_da_posicao']))
    A('  R² dos ajustes (gráfico do autor: linear 0,935; quadrático 0,995; exponencial 0,999):')
    rot = {'a_flavio_sozinho': '(a) Flávio sozinho', 'b_bloco_direita': '(b) bloco de direita (22+55+30+14)',
           'c_melhor_reproduz': '(c) a que melhor reproduz', 's_bloco_mais_cury': 'sens. bloco mais Cury',
           's_tudo_menos_esquerda': 'sens. tudo menos a esquerda', 's_tudo_menos_lula': 'sens. tudo menos Lula'}
    for nome, d in J1['definicoes'].items():
        a = d['ajustes']
        A(f"    {rot[nome]}: linear {n(a['linear'])}; quadrático {n(a['quadratico'])}; exponencial (não linear) {n(a['exponencial'])}; "
          f"exponencial pelo log {n(a['exp_log_escala_log'])} na escala do log e {n(a['exp_log_escala_y'])} na de y; "
          f"leitura literal a*x*exp(bx) {n(a['exp_literal_a_x_exp_bx'])}; resíduo da reta de fatia {n(d['reta_p2']['dp'], 3)} ponto")
    if 'com_exterior' in J1:
        e = J1['com_exterior']['b_bloco_direita']
        A(f"  Com o exterior como 28º ponto (bloco de direita): linear {n(e['linear'])}; quadrático {n(e['quadratico'])}; exponencial {n(e['exponencial'])}.")
    A('')
    A('J2. A MESMA CONTA NOS OUTROS ANOS (27 UFs; y = PT sobre adversário no 2º turno)')
    for ano in ('2026', '2022', '2018', '2014'):
        for nome, r in (('adversario_sozinho', 'adversário sozinho'), ('adversario_mais_outros', 'adversário mais outros')):
            a = J2[ano][nome]['ajustes']
            A(f"    {ano} {NOME_ADV[int(ano)]}, x = {r}: linear {n(a['linear'])}; quadrático {n(a['quadratico'])}; "
              f"exponencial {n(a['exponencial'])} (pelo log {n(a['exp_log_escala_log'])}); resíduo da reta de fatia "
              f"{n(J2[ano][nome]['reta_p2']['dp'], 3)} ponto (maior {n(J2[ano][nome]['reta_p2']['max'], 2)})")
    A('')
    A('J3. SIMULAÇÃO SEM FRAUDE (1º turno real de 2026 por UF; 1.000 sorteios por nível)')
    cp = J3['curva_pura']
    A('  Curva pura, sem nenhum dado do 2º turno: y = (100 menos x) / x calculado só com o x real de cada UF.')
    for nome in ('a_flavio_sozinho', 'b_bloco_direita', 'c_melhor_reproduz', 'p2_real_contra_ele_mesmo'):
        A(f"    x = {nome}: linear {n(cp[nome]['linear'])}; quadrático {n(cp[nome]['quadratico'])}; exponencial {n(cp[nome]['exponencial'])}")
    A('  Mediana [percentil 5; percentil 95] do R² de cada ajuste e do desvio-padrão dos resíduos (x = definição (c)):')
    for chave, cen in J3['cenarios'].items():
        d = cen['definicoes']['c_melhor_reproduz']
        A(f"    versão {cen['versao']}, ruído {cen['ruido']} de {n(cen['desvio_pontos'], 1)} ponto(s): "
          f"linear {n(d['linear']['p50'])} [{n(d['linear']['p5'])}; {n(d['linear']['p95'])}]; "
          f"quadrático {n(d['quadratico']['p50'])} [{n(d['quadratico']['p5'])}; {n(d['quadratico']['p95'])}]; "
          f"exponencial {n(d['exponencial']['p50'])} [{n(d['exponencial']['p5'])}; {n(d['exponencial']['p95'])}]; "
          f"melhor {n(d['melhor']['p50'])}; resíduo {n(d['dp_residuos']['p50'], 3)} "
          f"[{n(d['dp_residuos']['p1'], 3)} no percentil 1]; sorteios com melhor R² >= 0,98: {n(100 * d['fracao_melhor_ge_098'], 1)}%; "
          f">= 0,999: {n(100 * d['fracao_melhor_ge_0999'], 1)}%")
    A('  Versão D (tudo arbitrário), separando os sorteios em que os dois finalistas guardam pelo menos metade dos seus eleitores:')
    for s in (2, 5, 10):
        d = J3['cenarios'][f'D|independente|{s:g}']['definicoes']['c_melhor_reproduz']['finalistas_guardam_metade']
        if d['melhor'] and d['melhor_nos_demais']:
            A(f"    ruído {s}: {d['sorteios']} sorteios com finalistas fiéis, mediana do melhor R² {n(d['melhor']['p50'])}; "
              f"nos demais, {n(d['melhor_nos_demais']['p50'])}")
    A('')
    A('CALIBRAÇÃO COM FRAUDE PLANTADA (D11): o gráfico enxerga uma troca de 2.215.096 votos?')
    for nome, r in (('oficial', 'resultado oficial'), ('sem_troca_uniforme', 'desfeita a troca, uniforme'),
                    ('sem_troca_concentrada_nordeste', 'desfeita a troca, só no Nordeste')):
        c = C[nome]
        A(f"    {r}: fatia de Flávio nas 27 UFs {n(c['fatia_flavio_27_ufs'], 2)}%; linear {n(c['linear'])}; quadrático {n(c['quadratico'])}; "
          f"exponencial {n(c['exponencial'])}; resíduo {n(c['dp_residuos'], 3)} ponto")
    A('')
    A('J4. ONDE ESTÁ A VARIAÇÃO (2026)')
    for niv, r in (('municipio', 'Município'), ('secao', 'Seção')):
        d = J4[niv]
        A(f"  {r}: {mil(d['usadas'])} unidades usadas ({mil(d['excluidas_por_R2_zero'])} fora por Flávio com zero voto no 2º turno).")
        for nome in ('a_flavio_sozinho', 'b_bloco_direita', 'c_melhor_reproduz'):
            x = d['definicoes'][nome]
            A(f"    {rot[nome]}: R² de y sem peso: linear {n(x['sem_peso']['linear'])}; quadrático {n(x['sem_peso']['quadratico'])}; "
              f"exponencial {n(x['sem_peso']['exponencial'])} (pelo log {n(x['sem_peso']['exp_log_escala_log'])}); com peso: "
              f"{n(x['com_peso']['linear'])}; {n(x['com_peso']['quadratico'])}; {n(x['com_peso']['exponencial'])}; Spearman {n(x['spearman_x_y'])}; "
              f"reta de fatia: R² {n(x['reta_p2']['r2'])}, resíduo {n(x['reta_p2']['dp'], 2)} pontos, percentis 5 e 95 "
              f"{n(x['reta_p2']['residuos']['p5'], 2)} e {n(x['reta_p2']['residuos']['p95'], 2)}")
    for nome in ('c_melhor_reproduz', 'a_flavio_sozinho'):
        t = J4['por_uf'][nome]
        A(f"  Por UF, {rot[nome]}: fatia de Flávio no 2º turno = {n(t['intercepto'], 3)} + {n(t['inclinacao'], 4)} * x; "
          f"desvio-padrão dos resíduos {n(t['dp'], 3)} ponto. Resíduo positivo = Flávio acima do previsto.")
        A('    ' + '; '.join(f"{r['uf']} {'+' if r['residuo'] >= 0 else ''}{n(r['residuo'], 2)}" for r in t['linhas']))
    A('')
    return o


# ------------------------------------------------------------------ principal
def main():
    t0 = time.time()
    cache = None
    if '--cache' in sys.argv:
        cache = sys.argv[sys.argv.index('--cache') + 1]
    ag, S, origem = carregar_tudo(cache)
    R = {'teste': 'R29_J (Adendo 29, J1 a J4)', 'registro': 'PRE-REGISTRO-2026-10-26.md, Adendo 29, commit 3929135',
         'origem_dos_dados': origem, 'semente': SEMENTE,
         'secoes_por_ano': {str(a): ag[a]['nsec'] for a in ANOS}}
    R['candidatos'] = {c: {'nome': ag[2026]['nomes'].get(c), 'partido': PARTIDO[c], 'classe': CLASSE[c],
                           'votos': ag[2026]['totais'].get(c)} for c in CAND}
    J1, ufs, T, defs, y, p2 = j1(ag)
    R['J1'] = J1
    R['J2'] = j2(ag)
    R['J3'] = j3(T, defs, y, p2)
    ufz, Tz = monta(ag, 2026, com_zz=True)
    R['calibracao'] = calibracao(ufs, T, defs['c_melhor_reproduz'], float(Tz['L2'].sum()), float(Tz['R2'].sum()))
    R['calibracao']['nacional_com_exterior'] = {'L2': float(Tz['L2'].sum()), 'R2': float(Tz['R2'].sum())}
    fm = [f for f in J1['familia'] if f['definicao'] == J1['definicao_c']][0]
    R['J4'] = j4(ag, S, ufs, T, defs, p2, (fm['nums'], fm['den']))
    R['leitura'] = leitura(R['J1'], R['J2'], R['J3'])
    for nome, f in list(globals().items()):
        if nome.startswith('exploratorio_') and callable(f):
            R.setdefault('exploratorio', {})[nome] = f(ag, S, R, ufs, T, defs, y, p2)
    linhas = texto(R)
    if 'texto_final' in globals():
        linhas = globals()['texto_final'](R, linhas)
    R['segundos'] = round(time.time() - t0, 1)
    with open(SAIDA_JSON, 'w') as f:
        json.dump(R, f, ensure_ascii=False, indent=1)
    with open(SAIDA_TXT, 'w') as f:
        f.write('\n'.join(linhas) + '\n')
    print('\n'.join(linhas))
    print('segundos', R['segundos'])


if __name__ == '__main__':
    main()
