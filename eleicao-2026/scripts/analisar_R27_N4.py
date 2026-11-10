"""R27_N4: SAÍDA CONTRA ENTRADA (teste N4 do Adendo 30 do pré-registro, por inteiro).

Adendo 30 (commit a7218fb, 10/11/2026 10:08:24 UTC), escrito depois da Onda B e antes de rodar. O critério vale como
está no adendo. Este docstring foi escrito ANTES de qualquer conta com votos deste teste; o que ele decide e o registro
não fixa está em DECISÕES e sai no resultado como desvio. Até aqui só foi lida estrutura sem voto: as chaves e campos
das bases de dados/ (2026: 499.205 seções com os dois turnos; 2022: 472.028; 2018: 454.448; 2014: 428.852), os tipos
de seção (apurada, anulada) e o cabeçalho do cadastro de locais de votação.

ESTE TESTE É CONFIRMAÇÃO DE UM EXPLORATÓRIO JÁ VISTO, NÃO TESTE CEGO. O que eu já conhecia antes de escrever isto:
- os textos das Ondas A e B e o resultado do N2 com a conferência (resultados/R27_N2_quem_nao_voltou.txt e o bloco N2 de
  resultados/testes_adendo27_ondaB_com_conferencia.json);
- o exploratório do conferente do N2, que é a origem deste teste: assimetria do modelo 0 por faixa de abstenção do 1º
  turno em 2026: menos de 10% (7.351 seções, 581.767 votos de Flávio, abstenção média 8,4%) A = -0,0223 (ep 0,0060);
  10 a 15% -0,0118 (ep 0,0034); 15 a 20% -0,0116 (ep 0,0029); 20 a 25% -0,0163; 25 a 30% -0,0276; 30% ou mais -0,0497
  (ep 0,0088); e, na faixa de menos de 10%, +0,009 (2014), +0,001 (2018) e +0,005 (2022);
- como o conferente plantou a entrada (li a definição no código dele, c_passo6.py: faltosos do 1º turno x inclinação da
  seção a Lula, L/(L+F), com o total de 3,6% dos votos de Flávio do 2º turno) e que, no país, ela move a assimetria
  -0,0340 contra -0,0364 da retirada.
Logo o número principal (a assimetria na faixa de menos de 10%) já é conhecido e, refeito com código próprio, só pode
confirmar a conta. O que é NOVO e decide: a calibração nas duas direções DENTRO da faixa (ninguém calculou), os
espelhos, as regiões e a lista de seções. Conta de guardanapo feita antes de rodar, só com agregados já publicados
(abstenção média 8,4% na faixa contra 20,9% no país): a razão entrada/retirada na faixa deve ficar perto de 0,3 a
0,4, isto é, perto do limiar de um terço. Por isso as definições dos plantios ficam fixadas aqui e não mudam depois.

Uso:
  python3 -I scripts/analisar_R27_N4.py base     monta os vetores por ano (2026, 2022, 2018, 2014)
  python3 -I scripts/analisar_R27_N4.py rodar    calcula tudo e grava resultados/R27_N4_saida_contra_entrada.json
  python3 -I scripts/analisar_R27_N4.py lista    grava resultados/R27_N4_secoes_para_cadernos.csv
  python3 -I scripts/analisar_R27_N4.py texto    escreve resultados/R27_N4_saida_contra_entrada.txt a partir do JSON
Trabalho e parciais: /home/user/trabalho-eleicao/adendo27/R27_N4/

Pergunta. O N2 mostrou que, dentro do município, o eleitor de Flávio do 1º turno "voltou menos" que o de Lula
(assimetria -0,0178), mas o conferente mostrou que ENTRADA de faltosos do lado de Lula produz o mesmo número que SAÍDA
de eleitores de Flávio. Onde quase não houve faltoso no 1º turno (abstenção abaixo de 10%) há pouco espaço para
entrada; se a assimetria continuar lá, é saída. Limite dito no registro: saída é eleitor de Flávio que ficou em casa OU
eleitor registrado como ausente; boletim não separa. O teste não prova retirada; o produto útil é a lista de seções.

O QUE O REGISTRO FIXA (aplicado à letra)
- Conta: modelo 0 do N2 (y = variação do comparecimento sobre aptos contra as fatias sobre aptos de Flávio, Lula,
  eliminados e branco mais nulo do 1º turno, efeito fixo de município, peso aptos, erro por município), separado por
  faixa de abstenção do 1º turno na seção: menos de 10%, 10 a 15, 15 a 20, 20 a 25, 25 ou mais.
  Assimetria A = coeficiente de Flávio menos o de Lula.
- Calibração nas duas direções, plantadas com o mesmo total: retirada de eleitores de Flávio e entrada de faltosos do
  lado de Lula. O teste só vale se, na faixa de menos de 10%, a entrada plantada mover a assimetria menos de um terço
  do que a retirada plantada move.
- Leitura: "há saída" se A na faixa de menos de 10% for de -0,015 ou menos, a mais de 3 erros-padrão, com a calibração
  cumprida. "Não há saída medida" se A mais 2 erros-padrão ficar acima de -0,005. Entre os dois, inconclusivo.
- Produto: lista das seções com abstenção do 1º turno abaixo de 10%, voto relevante de Flávio e maior queda.
- Ao lado: os mesmos números em 2014, 2018 e 2022, e por região.
- Dos avisos do Adendo 27 e das regras desta onda: calibração por efeito plantado nos dados de 2026 (da
  irregularidade e da explicação inocente), teste espelho, valor bruto de 2026 ao lado de qualquer comparação com
  outro ano, tradução em votos de margem.

DECISÕES QUE O REGISTRO NÃO FIXA (tomadas aqui, antes de calcular qualquer coisa com votos)
D1. Universo U (o do N2): chaves de dados/secoes2026.json.gz com UF diferente de ZZ, com os blocos "1" e "2", aptos
    do 1º turno iguais aos do 2º e maiores que zero. Nos outros anos a mesma regra, e fica fora a seção com turno
    anulado (tipo diferente de "apurada" em qualquer turno); as excluídas são contadas.
D2. Variáveis, todas sobre aptos da seção: F = Flávio (campo R) no 1º turno; L = Lula (campo L); E = eliminados
    (campo O, inclui o 28 anulado); BN = brancos mais nulos do 1º turno. Categoria omitida: abstenção do 1º turno.
    y = (comparecimento do 2º turno menos o do 1º) sobre aptos.
D3. Abstenção do 1º turno na seção: a = (aptos menos comparecimento do 1º turno) sobre aptos. Faixas fechadas embaixo
    e abertas em cima: [0; 0,10), [0,10; 0,15), [0,15; 0,20), [0,20; 0,25), [0,25; 1].
D4. "Separado por faixa" = uma regressão por faixa, só com as seções da faixa: coeficientes próprios e efeito fixo de
    município dentro da faixa (compara seções da mesma faixa no mesmo município). Mínimos quadrados com peso aptos,
    erro agrupado por município (CR1, a mesma fórmula de scripts/lib.py: município com uma só seção na faixa não
    informa e sai; correção G/(G-1) x (N-1)/(N-k)). Código próprio, conferido contra lib.fe_ols.
    A = bF menos bL, erro pela covariância agrupada. A negativa: o eleitor de Flávio voltou menos que o de Lula.
    "A mais de 3 erros-padrão" = |A| / ep maior que 3.
D5. Calibração (o que decide se o teste vale). Os dois plantios mexem só no comparecimento do 2º turno; as faixas e os
    regressores (1º turno) não mudam. Como o ajuste é linear em y, o deslocamento dA de cada plantio é a assimetria
    da regressão da própria perturbação, sem ruído do dado.
    RETIRADA (a irregularidade; é o plantio D7 do N2): em toda seção de U, x ~ Binomial(votos de Flávio no 2º turno;
      0,036), semente 20261110; esses eleitores passam à abstenção do 2º turno (y cai x/aptos).
    ENTRADA (a explicação sem saída; é o plantio do conferente do N2, que motivou o Adendo 30): em toda seção de U,
      cada faltoso do 1º turno entra no 2º com probabilidade k x pL, onde pL = L/(L+F) é a inclinação da seção a Lula
      no 1º turno (0,5 se L+F = 0): x ~ Binomial(faltosos do 1º turno; k x pL), limitado ao espaço físico da seção
      (aptos menos comparecimento do 2º turno observado); y sobe x/aptos. k é escolhido para que o total esperado no
      país seja o MESMO total da retirada sorteada ("mesmo total" = mesmo total NACIONAL, em U: é a leitura que dá
      sentido ao critério, porque a entrada só pode mover menos na faixa se ali houver menos faltosos para entrar).
    Medida (letra): na faixa de menos de 10%, R = |dA da entrada| / |dA da retirada|. Calibração CUMPRIDA se R for
      menor que 1/3 E a retirada plantada for vista (|dA da retirada| maior que 3 erros-padrão de A na faixa).
    Decide o sorteio da semente 20261110. Ao lado: 200 sorteios (sementes 20261110 + j), a versão sem sorteio (valores
      esperados) e as variantes da entrada, que NÃO decidem: (b) inclinação por válidos, L/(F+L+E); (c) sem o limite
      físico; (d) escala que a Onda A relatou (faltosos entram 10,9% do lado de Lula e 5,5% do lado de Flávio,
      conforme a inclinação; não é o mesmo total); (e) entrada uniforme com o mesmo total (não deve mover A);
      (f) leitura dura: o mesmo total DENTRO da faixa de menos de 10% (a entrada da faixa reescalada para igualar a
      retirada da faixa); (g) retirada de 3,6% dos votos de Flávio do 1º turno. Se a principal cumprir e alguma das
      variantes (b), (c) ou a versão sem sorteio não cumprir, isso é dito no veredito como "margem estreita".
    Também relatado: a menor retirada uniforme que o teste enxerga na faixa (a que leva A a -0,015 e a que dá 3 ep).
D6. Leitura e veredito, pela letra:
    Calibração cumprida, A <= -0,015 e |A|/ep > 3: "há saída" = SINAL, no sentido estreito de que há saída medida
      onde entrada quase não cabe; pelo limite dito no registro isso não distingue eleitor que ficou em casa de eleitor
      registrado como ausente e não prova retirada.
    A + 2 ep > -0,005 (com a retirada plantada vista): "não há saída medida" = SEM SINAL.
    Calibração NÃO cumprida (R de 1/3 ou mais, ou retirada não vista) e A fora do "não há saída": o teste não vale
      para afirmar saída = SEM PODER (não separa saída de entrada na faixa), qualquer que seja A.
    Demais casos: INCONCLUSIVO.
D7. Leitura de dose, AO LADO (fixada aqui, não decide; serve para o caso de a calibração ficar perto do limiar):
    escala nacional da entrada = quanto do plantio de entrada reproduz sozinho a assimetria do modelo 0 no país inteiro
    (s = A0 de U sobre dA da entrada em U). Entrada nessa escala produziria, na faixa de menos de 10%,
    A_prevista = s x dA da entrada na faixa. Excesso = A observada na faixa menos A_prevista: a parte da assimetria
    da faixa que a entrada, na escala que explicaria o país, não alcança. Erro do excesso por reamostragem de
    municípios (999 réplicas, semente 20261110, a mesma réplica para o país e para a faixa). O mesmo para cada faixa.
D8. Espelhos:
    E1 (plantio espelho): retirada de 3,6% dos votos de Lula do 2º turno e entrada de faltosos do lado de Flávio
        (k x pF, mesmo total). Têm de mover A no sentido contrário, com a mesma razão R.
    E2 (a mesma conta nos outros anos): modelo 0 por faixa em 2014, 2018 e 2022 (adversário do PT menos PT), faixas
        pela abstenção do 1º turno do próprio ano, sempre com o valor bruto de 2026 ao lado. O Léo suspeita também
        desses anos: entram como comparação, não como régua de inocência.
    E3 (onde não deveria dar nada): na faixa de menos de 10%, y embaralhado entre as seções do mesmo município (500
        permutações, semente 20261110). A tem de ficar em torno de zero; o desvio das permutações confere o
        erro-padrão agrupado (faixa pequena, muitos municípios com poucas seções) e dá a fração de permutações com |A|
        maior ou igual ao observado. Ao lado: intervalo de 95% de A por reamostragem de municípios (999 réplicas).
D9. Regiões: N (AC, AM, AP, PA, RO, RR, TO), NE (AL, BA, CE, MA, PB, PE, PI, RN, SE), CO (DF, GO, MS, MT),
    SE (ES, MG, RJ, SP), S (PR, RS, SC). Modelo 0 por região e faixa em 2026; na faixa de menos de 10%, também por
    região nos outros anos. Célula com menos de 30 municípios informativos (2 ou mais seções na faixa) é relatada com
    a marca "poucas unidades". Descritivo por UF na faixa de menos de 10% só para UF com 300 ou mais seções e 30 ou
    mais municípios informativos.
D10. Votos de margem: V da faixa = menos A x (votos de Flávio no 1º turno na faixa) = eleitores de Flávio que não
    voltaram acima da taxa do eleitor de Lula; cada um vale 1 voto de margem (não vira voto de Lula). Soma das cinco
    faixas. Ao lado, e marcada como extrapolação: a taxa da faixa de menos de 10% aplicada a todos os votos de Flávio
    de U. Margem oficial: 4.430.191.
D11. Sensibilidades (fixadas aqui; não decidem): sem peso; efeito fixo de local de votação com erro por município;
    corte da primeira faixa em 8% e em 12%; modelo único com efeito fixo de município comum às faixas e interações
    faixa x fatias; só seções com 50 ou mais votos de Flávio no 1º turno; municípios com menos de 20.000 aptos
    contra os demais dentro da faixa; A da faixa tirando uma UF de cada vez e uma região de cada vez.
    Descritivo ao lado: decomposição exata de A em cada faixa na parte carregada pelas seções em que o
    comparecimento caiu (y negativo) e na parte das seções em que subiu (A = A de min(y,0) + A de max(y,0)).
D12. Produto (CSV para pedido de cadernos): seções de U (aptos iguais nos dois turnos, para a queda não ser efeito de
    transferência de eleitores entre seções) com abstenção do 1º turno abaixo de 10% e 50 ou mais votos de Flávio no
    1º turno, ordenadas pela maior queda ABSOLUTA de votos de Flávio (2º turno menos 1º, do mais negativo para o
    menos); empate: maior queda relativa, depois a chave. As 300 primeiras. Colunas: ordem, UF, código e nome do
    município, zona, seção, número, nome, endereço, bairro, tipo e coordenadas do local (cadastro de locais do TSE),
    aptos, comparecimento, Flávio, Lula, eliminados (1º turno), brancos e nulos dos dois turnos, abstenção do 1º
    turno e as variações. Contadas à parte, sem entrar na lista: as seções que cumpririam os critérios mas têm aptos
    diferentes entre os turnos. Descritivo da lista (não é teste): soma das quedas, quantas seções têm forma de saída
    (queda do comparecimento de pelo menos metade da queda de Flávio) e quantas têm forma de troca (ganho de Lula de
    pelo menos metade da queda de Flávio), por UF e por tipo de local; e o ESPELHO da lista: as 300 maiores quedas de
    Lula pelos mesmos critérios (50 ou mais votos de Lula), para dar a medida do que a escolha de extremos produz.
    A lista é escolha de extremos: serve para auditoria, não é evidência por si.
D13. Tudo o que for feito depois de ver resultado fica na chave "exploratorio" do JSON e marcado no texto.
"""
# Acrescentado DEPOIS de rodar: só o comando "texto" (redação do .txt a partir do JSON) e o que estiver na função
# explorar(), marcada como exploratória. As funções base(), rodar() e lista() são as do arquivo guardado antes de
# rodar em /home/user/trabalho-eleicao/adendo27/R27_N4/analisar_R27_N4_antes_de_rodar.py.
import collections
import csv
import gzip
import hashlib
import importlib.util
import io
import json
import os
import sys
import time
import zipfile

import numpy as np

AQUI = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.dirname(AQUI)
DADOS = os.path.join(REPO, 'dados')
TRAB = '/home/user/trabalho-eleicao/adendo27/R27_N4'
LOCAIS = '/home/user/trabalho-eleicao/adendo21/F14_dl_locais/eleitorado_local_votacao_2026.zip'
SAIDA_JSON = os.path.join(REPO, 'resultados', 'R27_N4_saida_contra_entrada.json')
SAIDA_TXT = os.path.join(REPO, 'resultados', 'R27_N4_saida_contra_entrada.txt')
SAIDA_CSV = os.path.join(REPO, 'resultados', 'R27_N4_secoes_para_cadernos.csv')
SEMENTE = 20261110
MARGEM = 4430191
TAXA = 0.036
ANOS = (2026, 2022, 2018, 2014)
FAIXAS = [(0.0, 0.10, 'menos de 10%'), (0.10, 0.15, '10 a 15%'), (0.15, 0.20, '15 a 20%'),
          (0.20, 0.25, '20 a 25%'), (0.25, 1.0000001, '25% ou mais')]
REGIOES = collections.OrderedDict([
    ('N', ['AC', 'AM', 'AP', 'PA', 'RO', 'RR', 'TO']),
    ('NE', ['AL', 'BA', 'CE', 'MA', 'PB', 'PE', 'PI', 'RN', 'SE']),
    ('CO', ['DF', 'GO', 'MS', 'MT']),
    ('SE', ['ES', 'MG', 'RJ', 'SP']),
    ('S', ['PR', 'RS', 'SC'])])
UF_REG = {u: r for r, us in REGIOES.items() for u in us}
PEQUENO = 20000
LIM_SINAL = -0.015
LIM_SEM = -0.005
COLS = ['apt1', 'apt2', 'c1', 'c2', 'R1', 'L1', 'O1', 'B1', 'N1', 'R2', 'L2', 'O2', 'B2', 'N2', 'ok']
CONTRASTE = np.array([1.0, -1.0, 0.0, 0.0])


def diga(*a):
    print(time.strftime('%H:%M:%S'), *a, flush=True)


def grava(nome, obj):
    os.makedirs(TRAB, exist_ok=True)
    tmp = os.path.join(TRAB, nome + '.tmp')
    with open(tmp, 'w') as f:
        json.dump(obj, f, ensure_ascii=False, indent=1)
    os.replace(tmp, os.path.join(TRAB, nome))


# ---------------------------------------------------------------- base
def base():
    os.makedirs(TRAB, exist_ok=True)
    info = {}
    for ano in ANOS:
        with gzip.open(os.path.join(DADOS, f'secoes{ano}.json.gz'), 'rt') as f:
            S = json.load(f)
        ks = sorted(k for k, v in S.items() if not k.startswith('ZZ|') and '1' in v and '2' in v)
        n = len(ks)
        M = np.zeros((n, len(COLS)), dtype=np.int64)
        loc = []
        for i, k in enumerate(ks):
            v1, v2 = S[k]['1'], S[k]['2']
            ok = str(v1.get('tipo', '')).lower() == 'apurada' and str(v2.get('tipo', '')).lower() == 'apurada'
            M[i] = (v1['apt'], v2['apt'], v1['comp'], v2['comp'], v1['R'], v1['L'], v1['O'], v1['B'], v1['N'],
                    v2['R'], v2['L'], v2.get('O', 0), v2['B'], v2['N'], int(ok))
            loc.append(str(v1.get('loc', '')))
        am = collections.Counter()
        for k, v in S.items():
            if '1' in v and not k.startswith('ZZ|'):
                am[k.rsplit('|', 2)[0]] += v['1']['apt']
        aptmun = np.array([am[k.rsplit('|', 2)[0]] for k in ks], dtype=np.int64)
        np.savez_compressed(os.path.join(TRAB, f'base_{ano}.npz'), chaves='\n'.join(ks), M=M, loc='\n'.join(loc),
                            aptmun=aptmun)
        info[ano] = {'secoes_na_base': len(S), 'com_dois_turnos_27_ufs': n,
                     'com_turno_nao_apurado': int((M[:, COLS.index('ok')] == 0).sum())}
        diga(ano, info[ano])
        del S
    grava('base_info.json', info)


def carrega(ano):
    z = np.load(os.path.join(TRAB, f'base_{ano}.npz'))
    ks = np.array(str(z['chaves']).split('\n'))
    M = z['M']
    d = {c: M[:, i] for i, c in enumerate(COLS)}
    d['chave'] = ks
    partes = [k.split('|') for k in ks]
    d['uf'] = np.array([p[0] for p in partes])
    d['mun'] = np.array([p[0] + '|' + p[1] for p in partes])
    d['zona'] = np.array([p[2] for p in partes])
    d['secao'] = np.array([p[3] for p in partes])
    locs = str(z['loc']).split('\n')
    d['loc'] = np.array(locs)
    d['local'] = np.array([p[0] + '|' + p[1] + '|' + p[2] + '|' + l for p, l in zip(partes, locs)])
    d['aptmun'] = z['aptmun']
    d['reg'] = np.array([UF_REG[u] for u in d['uf']])
    d['U'] = (d['apt1'] == d['apt2']) & (d['apt1'] > 0) & (d['ok'] == 1)
    return d


def recorta(d, sel):
    return {k: (v[sel] if isinstance(v, np.ndarray) and v.shape[:1] == sel.shape else v) for k, v in d.items()}


def variaveis(d):
    """y, X (F, L, E, BN sobre aptos), peso, abstenção do 1º turno."""
    apt = np.maximum(d['apt1'], 1).astype(float)   # aptos zero só fora de U; evita divisão por zero
    X = np.column_stack([d['R1'] / apt, d['L1'] / apt, d['O1'] / apt, (d['B1'] + d['N1']) / apt])
    y = (d['c2'] - d['c1']) / apt
    a = (d['apt1'] - d['c1']) / apt
    return y, X, apt, a


# ---------------------------------------------------------------- regressão (código próprio)
def codigos(v):
    return np.unique(v, return_inverse=True)[1]


class Ajuste:
    """Mínimos quadrados com peso, efeito fixo (transformação dentro do grupo) e erro agrupado CR1.
    Grupos de efeito fixo com uma só observação saem, como em scripts/lib.py."""

    def __init__(self, X, fe, w, cl):
        X = np.asarray(X, float)
        fe = codigos(fe)
        cnt = np.bincount(fe)
        self.ok = cnt[fe] >= 2
        X, w = X[self.ok], np.asarray(w, float)[self.ok]
        self.fe = codigos(fe[self.ok])
        self.cl = codigos(np.asarray(cl)[self.ok])
        self.w = w
        self.sw = np.bincount(self.fe, weights=w)
        self.Xd = self._dm(X)
        self.N, self.k = self.Xd.shape
        self.G = int(self.cl.max()) + 1
        self.Gfe = int(self.fe.max()) + 1
        self.XtX = (self.Xd * w[:, None]).T @ self.Xd
        self.inv = np.linalg.inv(self.XtX)
        self.c = self.G / (self.G - 1) * (self.N - 1) / (self.N - self.k) if self.G > 1 else float('nan')

    def _dm(self, M):
        out = np.empty_like(M, dtype=float)
        for j in range(M.shape[1]):
            m = np.bincount(self.fe, weights=self.w * M[:, j]) / self.sw
            out[:, j] = M[:, j] - m[self.fe]
        return out

    def coef(self, y):
        """b e covariância agrupada para um desfecho y (vetor do tamanho original)."""
        y = np.asarray(y, float)[self.ok]
        yd = self._dm(y[:, None])[:, 0]
        b = self.inv @ ((self.Xd * self.w[:, None]).T @ yd)
        e = yd - self.Xd @ b
        S = np.zeros((self.G, self.k))
        for j in range(self.k):
            S[:, j] = np.bincount(self.cl, weights=self.w * self.Xd[:, j] * e, minlength=self.G)
        V = self.c * self.inv @ (S.T @ S) @ self.inv
        return b, V

    def funcional(self, contraste=CONTRASTE):
        """Vetor a tal que contraste.b = a . y (y no tamanho original; zero fora do ajuste)."""
        a = np.zeros(len(self.ok))
        a[self.ok] = (self.Xd * self.w[:, None]) @ (self.inv @ contraste)
        return a

    def A(self, y, contraste=CONTRASTE):
        b, V = self.coef(y)
        return float(contraste @ b), float(np.sqrt(contraste @ V @ contraste)), b, V

    def suficientes(self, y, cl_global, ng):
        """Somas por município (índice global) para a reamostragem: XtX_g e Xty_g."""
        yd = self._dm(np.asarray(y, float)[self.ok][:, None])[:, 0]
        g = np.asarray(cl_global)[self.ok]
        k = self.k
        XX = np.zeros((ng, k, k))
        Xy = np.zeros((ng, k))
        for i in range(k):
            Xy[:, i] = np.bincount(g, weights=self.w * self.Xd[:, i] * yd, minlength=ng)
            for j in range(i, k):
                XX[:, i, j] = XX[:, j, i] = np.bincount(g, weights=self.w * self.Xd[:, i] * self.Xd[:, j], minlength=ng)
        return XX, Xy


def modelo0(d, sel, y=None, fe='mun', peso=True, extra=None):
    """Modelo 0 nas seções sel. Devolve dict com A, ep, coeficientes, n."""
    yy, X, apt, a = variaveis(d)
    if y is not None:
        yy = y
    if sel.sum() < 10:
        return None
    w = apt[sel] if peso else np.ones(int(sel.sum()))
    try:
        aj = Ajuste(X[sel], d[fe][sel], w, d['mun'][sel])
    except (ValueError, np.linalg.LinAlgError):
        return None
    if aj.N <= aj.k + 1 or aj.G < 2:
        return None
    A, ep, b, V = aj.A(yy[sel])
    se = np.sqrt(np.diag(V))
    usado = np.zeros(len(sel), bool)
    usado[np.where(sel)[0][aj.ok]] = True
    o = {'A': A, 'ep': ep, 'z': A / ep if ep > 0 else None,
         'coef': {'F': b[0], 'L': b[1], 'E': b[2], 'BN': b[3]},
         'ep_coef': {'F': se[0], 'L': se[1], 'E': se[2], 'BN': se[3]},
         'n_secoes_faixa': int(sel.sum()), 'n_no_ajuste': int(aj.N), 'municipios_informativos': int(aj.G if fe == 'mun' else len(set(d['mun'][usado]))),
         'grupos_efeito_fixo': int(aj.Gfe),
         'votos_F_1t': int(d['R1'][sel].sum()), 'votos_L_1t': int(d['L1'][sel].sum()),
         'votos_F_2t': int(d['R2'][sel].sum()), 'votos_L_2t': int(d['L2'][sel].sum()),
         'aptos': int(d['apt1'][sel].sum()), 'comp_1t': int(d['c1'][sel].sum()), 'comp_2t': int(d['c2'][sel].sum()),
         'abst_media_ponderada': float((d['apt1'][sel] - d['c1'][sel]).sum() / d['apt1'][sel].sum()),
         'y_medio_ponderado': float((d['c2'][sel] - d['c1'][sel]).sum() / d['apt1'][sel].sum())}
    o['V_votos'] = -A * o['votos_F_1t']
    o['V_ep'] = ep * o['votos_F_1t']
    o['V_pct_margem'] = 100 * o['V_votos'] / MARGEM
    if extra:
        o.update(extra)
    return o


def faixa_sel(d, a, i, base=None):
    lo, hi, _ = FAIXAS[i]
    s = (a >= lo) & (a < hi)
    return s & (d['U'] if base is None else base)


def leitura(A, ep, cumprida, vista):
    forte = A <= LIM_SINAL and abs(A) / ep > 3
    sem = A + 2 * ep > LIM_SEM
    if sem and vista:
        return 'SEM SINAL', 'não há saída medida'
    if forte and cumprida:
        return 'SINAL', 'há saída'
    if not cumprida:
        return 'SEM PODER', 'a calibração não foi cumprida: o teste não separa saída de entrada na faixa'
    return 'INCONCLUSIVO', 'entre os dois limiares'


# ---------------------------------------------------------------- plantios
def plantios(d, rng, det=False):
    """Perturbações de y (em fração de aptos) em todas as seções de U. Devolve dict nome -> (vetor dy, total)."""
    U = d['U']
    apt = np.maximum(d['apt1'], 1).astype(float)
    F2 = np.where(U, d['R2'], 0)
    L2 = np.where(U, d['L2'], 0)
    falt = np.where(U, d['apt1'] - d['c1'], 0).astype(np.int64)
    espaco = np.where(U, np.maximum(d['apt2'] - d['c2'], 0), 0).astype(float)
    fl = (d['R1'] + d['L1']).astype(float)
    pL = np.where(fl > 0, d['L1'] / np.where(fl > 0, fl, 1), 0.5)
    pF = 1 - pL
    val = (d['R1'] + d['L1'] + d['O1']).astype(float)
    pLv = np.where(val > 0, d['L1'] / np.where(val > 0, val, 1), 0.5)
    out = {}

    def sorteia(n, p):
        p = np.clip(p, 0, 1)
        return n * p if det else rng.binomial(n, p).astype(float)

    def k_para(total, peso, limite=None):
        """k tal que a soma de min(k x peso, limite) dê o total (bisseção)."""
        if limite is None:
            return total / peso.sum()
        lo, hi = 0.0, 1.0
        while np.minimum(hi * peso, limite).sum() < total and hi < 1e6:
            hi *= 2
        for _ in range(80):
            mid = (lo + hi) / 2
            if np.minimum(mid * peso, limite).sum() < total:
                lo = mid
            else:
                hi = mid
        return (lo + hi) / 2

    # retirada de eleitores de Flávio (2º turno) e espelho de Lula
    x = sorteia(F2, TAXA)
    T = float(x.sum())
    out['retirada_F'] = (-x / apt, T)
    xl = sorteia(L2, TAXA)
    TL = float(xl.sum())
    out['retirada_L'] = (-xl / apt, TL)
    # entrada do lado de Lula, mesmo total nacional, com limite físico
    k = k_para(T, falt * pL, espaco)
    e = np.minimum(sorteia(falt, k * pL), espaco)
    out['entrada_L'] = (e / apt, float(e.sum()))
    out['_k_entrada_L'] = k
    out['_cortadas_entrada_L'] = int(((k * falt * pL) > espaco).sum())
    # espelho: entrada do lado de Flávio com o mesmo total
    kF = k_para(T, falt * pF, espaco)
    e = np.minimum(sorteia(falt, kF * pF), espaco)
    out['entrada_F'] = (e / apt, float(e.sum()))
    # variantes
    kb = k_para(T, falt * pLv, espaco)
    e = np.minimum(sorteia(falt, kb * pLv), espaco)
    out['entrada_L_validos'] = (e / apt, float(e.sum()))
    kc = k_para(T, falt * pL)
    e = sorteia(falt, kc * pL)
    out['entrada_L_sem_limite'] = (e / apt, float(e.sum()))
    e = np.minimum(sorteia(falt, 0.109 * pL + 0.055 * pF), espaco)
    out['entrada_escala_ondaA'] = (e / apt, float(e.sum()))
    ku = k_para(T, falt.astype(float), espaco)
    e = np.minimum(sorteia(falt, np.full(len(falt), ku)), espaco)
    out['entrada_uniforme'] = (e / apt, float(e.sum()))
    F1 = np.where(U, d['R1'], 0)
    x1 = sorteia(F1, TAXA)
    out['retirada_F_votos_1t'] = (-x1 / apt, float(x1.sum()))
    return out


def reamostra(suf, mult):
    """A com multiplicidades por município. suf = (XX, Xy)."""
    XX = np.tensordot(mult, suf[0], axes=(0, 0))
    Xy = mult @ suf[1]
    b = np.linalg.solve(XX, Xy)
    return float(CONTRASTE @ b)


# ---------------------------------------------------------------- conta principal
def rodar():
    t0 = time.time()
    R = {'teste': 'R27_N4', 'gerado_em_utc': time.strftime('%Y-%m-%dT%H:%M:%SZ', time.gmtime()),
         'registro': 'PRE-REGISTRO-2026-10-26.md, Adendo 30 (commit a7218fb, 10/11/2026 10:08:24 UTC), N4',
         'aviso': 'Confirmação de um exploratório já visto (conferente do N2), não teste cego.',
         'margem_oficial': MARGEM}
    d = carrega(2026)
    U = d['U']
    y, X, apt, a = variaveis(d)
    mun_g = codigos(d['mun'])           # índice global de município (todas as seções com dois turnos)
    ng = int(mun_g.max()) + 1
    R['universo'] = {'secoes_com_dois_turnos': int(len(U)), 'secoes_U': int(U.sum()),
                     'municipios_U': int(len(set(d['mun'][U]))), 'aptos_U': int(d['apt1'][U].sum()),
                     'comp_1t': int(d['c1'][U].sum()), 'comp_2t': int(d['c2'][U].sum()),
                     'F_1t': int(d['R1'][U].sum()), 'F_2t': int(d['R2'][U].sum()),
                     'L_1t': int(d['L1'][U].sum()), 'L_2t': int(d['L2'][U].sum()),
                     'abst_1t': float((d['apt1'][U] - d['c1'][U]).sum() / d['apt1'][U].sum())}
    diga('universo', R['universo'])

    # --- modelo 0 no país e conferência do código contra scripts/lib.py
    m_pais = modelo0(d, U)
    R['modelo0_pais'] = m_pais
    spec = importlib.util.spec_from_file_location('lib_repo', os.path.join(AQUI, 'lib.py'))
    lib = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(lib)
    conf = {}
    for nome, sel in [('pais', U), ('faixa_menos_de_10', faixa_sel(d, a, 0))]:
        r = lib.fe_ols(y[sel], X[sel], d['mun'][sel], apt[sel], ['F', 'L', 'E', 'BN'])
        m = modelo0(d, sel)
        conf[nome] = {'dif_max_coef': max(abs(r['coef'][c] - m['coef'][c]) for c in 'F L E BN'.split()),
                      'dif_max_ep': max(abs(r['ep'][c] - m['ep_coef'][c]) for c in 'F L E BN'.split()),
                      'n_lib': r['n'], 'n_meu': m['n_no_ajuste']}
    R['conferencia_lib'] = conf
    diga('modelo 0 país', m_pais['A'], m_pais['ep'], 'conferência lib', conf)

    # --- por faixa (o que o registro fixa)
    fx = []
    sels = []
    ajustes = []
    for i, (lo, hi, nome) in enumerate(FAIXAS):
        sel = faixa_sel(d, a, i)
        sels.append(sel)
        m = modelo0(d, sel, extra={'faixa': nome})
        # decomposição exata: seções em que o comparecimento caiu e em que subiu
        mn = modelo0(d, sel, y=np.minimum(y, 0))
        mp = modelo0(d, sel, y=np.maximum(y, 0))
        m['A_parte_quedas'] = mn['A']
        m['ep_parte_quedas'] = mn['ep']
        m['A_parte_altas'] = mp['A']
        m['ep_parte_altas'] = mp['ep']
        m['secoes_comp_caiu'] = int((sel & (y < 0)).sum())
        m['secoes_comp_subiu'] = int((sel & (y > 0)).sum())
        fx.append(m)
        ajustes.append(Ajuste(X[sel], d['mun'][sel], apt[sel], d['mun'][sel]))
        diga('faixa', nome, 'n', m['n_secoes_faixa'], 'A', round(m['A'], 5), 'ep', round(m['ep'], 5))
    R['faixas_2026'] = fx
    R['soma_V_faixas'] = float(sum(m['V_votos'] for m in fx))
    R['extrapolacao_taxa_faixa1_a_todo_U'] = {'votos': -fx[0]['A'] * R['universo']['F_1t'],
                                             'ep': fx[0]['ep'] * R['universo']['F_1t'],
                                             'pct_margem': -100 * fx[0]['A'] * R['universo']['F_1t'] / MARGEM}
    grava('parcial_faixas.json', R)

    # --- calibração nas duas direções
    aj_pais = Ajuste(X[U], d['mun'][U], apt[U], d['mun'][U])
    func = []        # funcional de A por faixa, no tamanho total
    for sel, aj in zip(sels, ajustes):
        f = np.zeros(len(U))
        f[sel] = aj.funcional()
        func.append(f)
    f_pais = np.zeros(len(U))
    f_pais[U] = aj_pais.funcional()
    assert abs(func[0] @ y - fx[0]['A']) < 1e-9 and abs(f_pais @ y - m_pais['A']) < 1e-9

    def mede(pl):
        o = {}
        for nome, v in pl.items():
            if nome.startswith('_'):
                o[nome] = v
                continue
            dy, tot = v
            o[nome] = {'total_U': tot, 'dA_pais': float(f_pais @ dy),
                       'dA_faixas': [float(f @ dy) for f in func],
                       'total_faixas': [float(np.abs(dy * apt)[s].sum()) for s in sels]}
        return o

    cal = {}
    pl = plantios(d, np.random.default_rng(SEMENTE))
    cal['sorteio_principal'] = mede(pl)
    # conferência da linearidade: A com o y plantado menos A observada
    yr = y + pl['retirada_F'][0]
    ye = y + pl['entrada_L'][0]
    cal['conferencia_linearidade'] = {
        'retirada_faixa1': modelo0(d, sels[0], y=yr)['A'] - fx[0]['A'],
        'entrada_faixa1': modelo0(d, sels[0], y=ye)['A'] - fx[0]['A'],
        'A_faixa1_com_retirada': modelo0(d, sels[0], y=yr)['A'], 'ep_com_retirada': modelo0(d, sels[0], y=yr)['ep'],
        'A_faixa1_com_entrada': modelo0(d, sels[0], y=ye)['A'], 'ep_com_entrada': modelo0(d, sels[0], y=ye)['ep']}
    cal['sem_sorteio'] = mede(plantios(d, None, det=True))
    # (f) leitura dura: mesmo total dentro da faixa de menos de 10%
    pld = plantios(d, None, det=True)
    tr = float(np.abs(pld['retirada_F'][0] * apt)[sels[0]].sum())
    te = float(np.abs(pld['entrada_L'][0] * apt)[sels[0]].sum())
    cal['leitura_dura_mesmo_total_na_faixa'] = {
        'total_retirada_faixa1': tr, 'total_entrada_faixa1_escala_nacional': te, 'fator': tr / te,
        'dA_entrada_reescalada': float(func[0] @ pld['entrada_L'][0]) * tr / te,
        'dA_retirada': float(func[0] @ pld['retirada_F'][0])}
    cal['leitura_dura_mesmo_total_na_faixa']['R'] = abs(cal['leitura_dura_mesmo_total_na_faixa']['dA_entrada_reescalada']
                                                        / cal['leitura_dura_mesmo_total_na_faixa']['dA_retirada'])

    def razoes(m, ent='entrada_L', ret='retirada_F'):
        return [abs(m[ent]['dA_faixas'][i] / m[ret]['dA_faixas'][i]) if m[ret]['dA_faixas'][i] != 0 else None
                for i in range(len(FAIXAS))] + [abs(m[ent]['dA_pais'] / m[ret]['dA_pais'])]

    sp = cal['sorteio_principal']
    cal['R_por_faixa_e_pais'] = {'principal': razoes(sp), 'sem_sorteio': razoes(cal['sem_sorteio']),
                                'inclinacao_por_validos': razoes(sp, 'entrada_L_validos'),
                                'sem_limite_fisico': razoes(sp, 'entrada_L_sem_limite'),
                                'escala_ondaA_nao_e_mesmo_total': razoes(sp, 'entrada_escala_ondaA'),
                                'uniforme': razoes(sp, 'entrada_uniforme'),
                                'retirada_sobre_votos_1t': razoes(sp, 'entrada_L', 'retirada_F_votos_1t'),
                                'espelho_entrada_F_sobre_retirada_L': razoes(sp, 'entrada_F', 'retirada_L')}
    # 200 sorteios
    Rs, dR, dE = [], [], []
    for j in range(200):
        p = plantios(d, np.random.default_rng(SEMENTE + j))
        r_ = float(func[0] @ p['retirada_F'][0])
        e_ = float(func[0] @ p['entrada_L'][0])
        dR.append(r_)
        dE.append(e_)
        Rs.append(abs(e_ / r_))
    cal['200_sorteios_faixa1'] = {'R_min': min(Rs), 'R_mediana': float(np.median(Rs)), 'R_max': max(Rs),
                                  'R_p2_5': float(np.percentile(Rs, 2.5)), 'R_p97_5': float(np.percentile(Rs, 97.5)),
                                  'fracao_abaixo_de_um_terco': float(np.mean(np.array(Rs) < 1 / 3)),
                                  'dA_retirada_media': float(np.mean(dR)), 'dA_retirada_dp': float(np.std(dR)),
                                  'dA_entrada_media': float(np.mean(dE)), 'dA_entrada_dp': float(np.std(dE))}
    Rprin = cal['R_por_faixa_e_pais']['principal'][0]
    dAret = sp['retirada_F']['dA_faixas'][0]
    vista = abs(dAret) > 3 * fx[0]['ep']
    cal['criterio'] = {'R_faixa1': Rprin, 'limiar': 1 / 3, 'dA_retirada_faixa1': dAret,
                       'dA_entrada_faixa1': sp['entrada_L']['dA_faixas'][0],
                       'retirada_em_ep_da_faixa': abs(dAret) / fx[0]['ep'], 'retirada_vista': bool(vista),
                       'cumprida': bool(Rprin < 1 / 3 and vista),
                       'variantes_que_nao_cumprem': [n for n in ('sem_sorteio', 'inclinacao_por_validos', 'sem_limite_fisico')
                                                     if not cal['R_por_faixa_e_pais'][n][0] < 1 / 3],
                       'menor_retirada_que_leva_A_a_-0,015_pct_dos_votos_F': 100 * TAXA * abs(LIM_SINAL) / abs(dAret),
                       'menor_retirada_a_3_ep_pct_dos_votos_F': 100 * TAXA * 3 * fx[0]['ep'] / abs(dAret)}
    R['calibracao'] = cal
    diga('calibração', cal['criterio'], cal['200_sorteios_faixa1'])
    grava('parcial_calibracao.json', R)

    # --- leitura pela letra
    ver, frase = leitura(fx[0]['A'], fx[0]['ep'], cal['criterio']['cumprida'], vista)
    R['veredito'] = {'pela_letra': ver, 'leitura': frase, 'A_faixa1': fx[0]['A'], 'ep': fx[0]['ep'],
                     'A_em_ep': abs(fx[0]['A']) / fx[0]['ep'], 'A_mais_2ep': fx[0]['A'] + 2 * fx[0]['ep'],
                     'cond_A_menor_ou_igual_-0,015': bool(fx[0]['A'] <= LIM_SINAL),
                     'cond_mais_de_3_ep': bool(abs(fx[0]['A']) / fx[0]['ep'] > 3),
                     'cond_calibracao': cal['criterio']['cumprida'],
                     'cond_sem_saida_A_mais_2ep_acima_de_-0,005': bool(fx[0]['A'] + 2 * fx[0]['ep'] > LIM_SEM)}
    diga('VEREDITO', R['veredito'])

    # --- reamostragem de municípios (E3 e leitura de dose D7)
    rng = np.random.default_rng(SEMENTE)
    det = plantios(d, None, det=True)
    suf_y = [aj.suficientes(y[s], mun_g[s], ng) for aj, s in zip(ajustes, sels)]
    suf_e = [aj.suficientes(det['entrada_L'][0][s], mun_g[s], ng) for aj, s in zip(ajustes, sels)]
    sufp_y = aj_pais.suficientes(y[U], mun_g[U], ng)
    sufp_e = aj_pais.suficientes(det['entrada_L'][0][U], mun_g[U], ng)
    # dose no ponto
    s_esc = m_pais['A'] / float(f_pais @ det['entrada_L'][0])
    dose = {'escala_s': s_esc, 'k_equivalente': s_esc * det['_k_entrada_L'],
            'entrantes_equivalentes_no_pais': s_esc * det['entrada_L'][1], 'por_faixa': []}
    boot_A = [[] for _ in FAIXAS]
    boot_exc = [[] for _ in FAIXAS]
    boot_pais = []
    usados = np.unique(mun_g[U])
    for b in range(999):
        mult = np.bincount(rng.choice(usados, size=len(usados), replace=True), minlength=ng).astype(float)
        try:
            Ap = reamostra(sufp_y, mult)
            Ep = reamostra(sufp_e, mult)
        except np.linalg.LinAlgError:
            continue
        boot_pais.append(Ap)
        for i in range(len(FAIXAS)):
            try:
                Ai = reamostra(suf_y[i], mult)
                Ei = reamostra(suf_e[i], mult)
            except np.linalg.LinAlgError:
                continue
            boot_A[i].append(Ai)
            boot_exc[i].append(Ai - (Ap / Ep) * Ei)
    for i, (_, _, nome) in enumerate(FAIXAS):
        prev = s_esc * float(func[i] @ det['entrada_L'][0])
        exc = fx[i]['A'] - prev
        ba = np.array(boot_A[i])
        be = np.array(boot_exc[i])
        dose['por_faixa'].append({'faixa': nome, 'A_observada': fx[i]['A'], 'A_prevista_so_entrada': prev,
                                  'excesso': exc, 'ep_excesso_reamostragem': float(be.std(ddof=1)),
                                  'ic95_excesso': [float(np.percentile(be, 2.5)), float(np.percentile(be, 97.5))],
                                  'ep_A_reamostragem': float(ba.std(ddof=1)),
                                  'ic95_A_reamostragem': [float(np.percentile(ba, 2.5)), float(np.percentile(ba, 97.5))],
                                  'replicas': int(len(ba))})
    dose['ep_A_pais_reamostragem'] = float(np.std(boot_pais, ddof=1))
    R['dose_ao_lado'] = dose
    diga('dose', dose['por_faixa'][0])

    # --- E3: permutação de y dentro do município, faixa de menos de 10%
    s0 = sels[0]
    aj0 = ajustes[0]
    g0 = aj0.fe
    y0 = y[s0][aj0.ok]
    pos = np.argsort(g0, kind='stable')
    a0 = func[0][s0][aj0.ok]
    prm = []
    rngp = np.random.default_rng(SEMENTE)
    for _ in range(500):
        o = np.lexsort((rngp.random(len(g0)), g0))
        yp = np.empty_like(y0)
        yp[pos] = y0[o]
        prm.append(float(a0 @ yp))
    prm = np.array(prm)
    R['espelho_permutacao_faixa1'] = {'permutacoes': 500, 'media': float(prm.mean()), 'dp': float(prm.std(ddof=1)),
                                      'ep_agrupado_do_ajuste': fx[0]['ep'],
                                      'fracao_com_modulo_maior_ou_igual': float(np.mean(np.abs(prm) >= abs(fx[0]['A']))),
                                      'A_observada_em_dp_da_permutacao': abs(fx[0]['A']) / float(prm.std(ddof=1))}
    diga('permutação', R['espelho_permutacao_faixa1'])
    grava('parcial_espelhos.json', R)

    # --- regiões e UFs em 2026
    reg = {}
    for r in REGIOES:
        br = U & (d['reg'] == r)
        linha = {'todas_as_faixas': modelo0(d, br)}
        linha['faixas'] = []
        for i, (_, _, nome) in enumerate(FAIXAS):
            m = modelo0(d, faixa_sel(d, a, i, br), extra={'faixa': nome})
            if m is not None:
                m['poucas_unidades'] = bool(m['municipios_informativos'] < 30)
            linha['faixas'].append(m)
        reg[r] = linha
        diga('região', r, [(None if m is None else (round(m['A'], 4), round(m['ep'], 4), m['n_secoes_faixa'])) for m in linha['faixas']])
    R['regioes_2026'] = reg
    ufs = {}
    for uf in sorted(set(d['uf'])):
        s = sels[0] & (d['uf'] == uf)
        o = {'secoes_faixa1': int(s.sum()), 'votos_F_1t': int(d['R1'][s].sum())}
        m = modelo0(d, s) if s.sum() >= 300 else None
        if m is not None and m['municipios_informativos'] >= 30:
            o.update({'A': m['A'], 'ep': m['ep'], 'municipios_informativos': m['municipios_informativos'], 'V_votos': m['V_votos']})
        ufs[uf] = o
    R['ufs_faixa1_2026'] = ufs
    grava('parcial_regioes.json', R)

    # --- sensibilidades (não decidem)
    sen = {}
    sen['sem_peso'] = [modelo0(d, s, peso=False) for s in sels]
    sen['efeito_fixo_local'] = [modelo0(d, s, fe='local') for s in sels]
    for corte in (0.08, 0.12):
        sen[f'corte_{int(corte * 100)}'] = modelo0(d, U & (a < corte))
    s50 = sels[0] & (d['R1'] >= 50)
    sen['faixa1_50_ou_mais_votos_F'] = modelo0(d, s50)
    sen['faixa1_municipios_pequenos'] = modelo0(d, sels[0] & (d['aptmun'] < PEQUENO))
    sen['faixa1_municipios_demais'] = modelo0(d, sels[0] & (d['aptmun'] >= PEQUENO))
    sen['por_faixa_municipios_pequenos'] = [modelo0(d, s & (d['aptmun'] < PEQUENO)) for s in sels]
    sen['por_faixa_municipios_demais'] = [modelo0(d, s & (d['aptmun'] >= PEQUENO)) for s in sels]
    sen['faixa1_sem_uma_uf'] = {}
    for uf in sorted(set(d['uf'][sels[0]])):
        m = modelo0(d, sels[0] & (d['uf'] != uf))
        sen['faixa1_sem_uma_uf'][uf] = {'A': m['A'], 'ep': m['ep'], 'n': m['n_secoes_faixa']}
    sen['faixa1_sem_uma_regiao'] = {}
    for r in REGIOES:
        m = modelo0(d, sels[0] & (d['reg'] != r))
        sen['faixa1_sem_uma_regiao'][r] = {'A': m['A'], 'ep': m['ep'], 'n': m['n_secoes_faixa']}
    # modelo único: efeito fixo de município comum, interações faixa x fatias
    fa = np.full(len(U), -1)
    for i in range(len(FAIXAS)):
        fa[sels[i]] = i
    cols = []
    for i in range(len(FAIXAS)):
        ind = (fa == i).astype(float)
        for j in range(4):
            cols.append(X[:, j] * ind)
    for i in range(1, len(FAIXAS)):
        cols.append((fa == i).astype(float))
    XX = np.column_stack(cols)
    ajp = Ajuste(XX[U], d['mun'][U], apt[U], d['mun'][U])
    b, V = ajp.coef(y[U])
    un = []
    for i in range(len(FAIXAS)):
        c = np.zeros(XX.shape[1])
        c[4 * i] = 1
        c[4 * i + 1] = -1
        un.append({'faixa': FAIXAS[i][2], 'A': float(c @ b), 'ep': float(np.sqrt(c @ V @ c))})
    sen['modelo_unico_efeito_fixo_comum'] = un
    R['sensibilidades'] = sen
    diga('sensibilidades', 'sem peso', sen['sem_peso'][0]['A'], 'local', sen['efeito_fixo_local'][0]['A'],
         'único', un[0])
    grava('parcial_sens.json', R)

    # --- outros anos (E2), com 2026 ao lado
    anos = {}
    for ano in ANOS:
        da = d if ano == 2026 else carrega(ano)
        ya, Xa, apta, aa = variaveis(da)
        Ua = da['U']
        o = {'universo': {'secoes_com_dois_turnos': int(len(Ua)), 'secoes_U': int(Ua.sum()),
                          'fora_por_aptos_diferentes': int(((da['apt1'] != da['apt2']) & (da['ok'] == 1)).sum()),
                          'fora_por_turno_anulado': int((da['ok'] == 0).sum()),
                          'abst_1t': float((da['apt1'][Ua] - da['c1'][Ua]).sum() / da['apt1'][Ua].sum()),
                          'y_medio': float((da['c2'][Ua] - da['c1'][Ua]).sum() / da['apt1'][Ua].sum())},
             'modelo0_pais': modelo0(da, Ua), 'faixas': [], 'faixa1_por_regiao': {}}
        for i, (_, _, nome) in enumerate(FAIXAS):
            o['faixas'].append(modelo0(da, faixa_sel(da, aa, i), extra={'faixa': nome}))
        for r in REGIOES:
            m = modelo0(da, faixa_sel(da, aa, 0, Ua & (da['reg'] == r)))
            if m is not None:
                m['poucas_unidades'] = bool(m['municipios_informativos'] < 30)
            o['faixa1_por_regiao'][r] = m
        anos[str(ano)] = o
        diga(ano, 'A0', round(o['modelo0_pais']['A'], 4), 'faixas',
             [(round(m['A'], 4), round(m['ep'], 4), m['n_secoes_faixa']) if m else None for m in o['faixas']])
    R['anos'] = anos
    R['tempo_s'] = time.time() - t0
    grava('resultado_registrado_antes_do_exploratorio.json', R)
    with open(SAIDA_JSON, 'w') as f:
        json.dump(R, f, ensure_ascii=False, indent=1)
    diga('gravado', SAIDA_JSON, round(R['tempo_s']), 's')


# ---------------------------------------------------------------- lista para cadernos
def _cadastro(chaves):
    """Nome do município e dados do local de votação das chaves pedidas (cadastro de locais do TSE, lido como dado)."""
    quer = set(chaves)
    ufs = sorted({k.split('|')[0] for k in quer})
    out = {}
    z = zipfile.ZipFile(LOCAIS)
    for uf in ufs:
        nome = f'eleitorado_local_votacao_2026_{uf}.csv'
        with z.open(nome) as fh:
            rd = csv.reader(io.TextIOWrapper(fh, encoding='latin1', newline=''), delimiter=';')
            cab = next(rd)
            ix = {c: i for i, c in enumerate(cab)}
            for p in rd:
                if len(p) != len(cab):
                    continue
                k = f"{p[ix['SG_UF']]}|{int(p[ix['CD_MUNICIPIO']])}|{int(p[ix['NR_ZONA']])}|{int(p[ix['NR_SECAO']])}"
                if k not in quer:
                    continue
                t = p[ix['NR_TURNO']]
                if k in out and t != '1':
                    continue
                out[k] = {'municipio': p[ix['NM_MUNICIPIO']], 'num_local': p[ix['NR_LOCAL_VOTACAO']],
                          'nome_local': p[ix['NM_LOCAL_VOTACAO']], 'tipo_local': p[ix['DS_TIPO_LOCAL']],
                          'endereco': p[ix['DS_ENDERECO']], 'bairro': p[ix['NM_BAIRRO']],
                          'lat': p[ix['NR_LATITUDE']], 'lon': p[ix['NR_LONGITUDE']],
                          'tipo_secao': p[ix['DS_TIPO_SECAO_AGREGADA']]}
    return out


def lista():
    d = carrega(2026)
    y, X, apt, a = variaveis(d)
    U = d['U']
    crit = (a < 0.10) & (d['R1'] >= 50)
    cand = np.where(U & crit)[0]
    fora = (~U) & crit & (d['apt1'] > 0)
    dF = (d['R2'] - d['R1'])[cand]
    rel = dF / d['R1'][cand]
    ordem = sorted(range(len(cand)), key=lambda i: (dF[i], rel[i], d['chave'][cand[i]]))
    top = [cand[i] for i in ordem[:300]]
    cad = _cadastro([d['chave'][i] for i in top])
    linhas = []
    for n, i in enumerate(top, 1):
        k = d['chave'][i]
        uf, mun, zona, sec = k.split('|')
        c = cad.get(k, {})
        linhas.append(collections.OrderedDict([
            ('ordem', n), ('uf', uf), ('cod_municipio', mun), ('municipio', c.get('municipio', '')), ('zona', zona),
            ('secao', sec), ('num_local', c.get('num_local', d['loc'][i])), ('nome_local', c.get('nome_local', '')),
            ('endereco', c.get('endereco', '')), ('bairro', c.get('bairro', '')), ('tipo_local', c.get('tipo_local', '')),
            ('latitude', c.get('lat', '')), ('longitude', c.get('lon', '')),
            ('aptos_1t', int(d['apt1'][i])), ('aptos_2t', int(d['apt2'][i])),
            ('comparecimento_1t', int(d['c1'][i])), ('comparecimento_2t', int(d['c2'][i])),
            ('abstencao_1t_pct', round(100 * float(a[i]), 2)),
            ('flavio_1t', int(d['R1'][i])), ('flavio_2t', int(d['R2'][i])),
            ('variacao_flavio', int(d['R2'][i] - d['R1'][i])),
            ('variacao_flavio_pct', round(100 * float(d['R2'][i] - d['R1'][i]) / float(d['R1'][i]), 1)),
            ('lula_1t', int(d['L1'][i])), ('lula_2t', int(d['L2'][i])), ('variacao_lula', int(d['L2'][i] - d['L1'][i])),
            ('eliminados_1t', int(d['O1'][i])),
            ('brancos_1t', int(d['B1'][i])), ('brancos_2t', int(d['B2'][i])),
            ('nulos_1t', int(d['N1'][i])), ('nulos_2t', int(d['N2'][i])),
            ('variacao_comparecimento', int(d['c2'][i] - d['c1'][i]))]))
    tmp = SAIDA_CSV + '.tmp'
    with open(tmp, 'w', newline='', encoding='utf-8') as f:
        w = csv.DictWriter(f, fieldnames=list(linhas[0].keys()), delimiter=';')
        w.writeheader()
        w.writerows(linhas)
    os.replace(tmp, SAIDA_CSV)

    def resumo(idx, quem='R', outro='L'):
        q1, q2 = d[quem + '1'][idx], d[quem + '2'][idx]
        o1, o2 = d[outro + '1'][idx], d[outro + '2'][idx]
        queda = (q1 - q2).astype(float)
        dc = (d['c2'][idx] - d['c1'][idx]).astype(float)
        do = (o2 - o1).astype(float)
        dbn = ((d['B2'] + d['N2']) - (d['B1'] + d['N1']))[idx].astype(float)
        return {'secoes': int(len(idx)), 'soma_queda': float(queda.sum()), 'queda_min': float(queda.min()),
                'queda_mediana': float(np.median(queda)), 'queda_max': float(queda.max()),
                'votos_1t': int(q1.sum()), 'votos_2t': int(q2.sum()),
                'soma_variacao_comparecimento': float(dc.sum()), 'soma_variacao_do_outro': float(do.sum()),
                'soma_variacao_brancos_nulos': float(dbn.sum()),
                'aptos': int(d['apt1'][idx].sum()), 'comp_1t': int(d['c1'][idx].sum()), 'comp_2t': int(d['c2'][idx].sum()),
                'forma_de_saida': int((-dc >= 0.5 * queda).sum()), 'forma_de_troca': int((do >= 0.5 * queda).sum()),
                'as_duas': int(((-dc >= 0.5 * queda) & (do >= 0.5 * queda)).sum()),
                'nenhuma': int((~(-dc >= 0.5 * queda) & ~(do >= 0.5 * queda)).sum())}

    top = np.array(top)
    # espelho: maiores quedas de Lula pelos mesmos critérios
    critL = (a < 0.10) & (d['L1'] >= 50)
    candL = np.where(U & critL)[0]
    dL = (d['L2'] - d['L1'])[candL]
    relL = dL / d['L1'][candL]
    ordL = sorted(range(len(candL)), key=lambda i: (dL[i], relL[i], d['chave'][candL[i]]))
    topL = np.array([candL[i] for i in ordL[:300]])
    res = {'criterios': 'U (aptos iguais nos dois turnos), abstenção do 1º turno abaixo de 10%, 50 ou mais votos de Flávio no 1º turno',
           'candidatas': int(len(cand)), 'candidatas_com_queda_de_flavio': int((dF < 0).sum()),
           'candidatas_com_alta_de_flavio': int((dF > 0).sum()), 'candidatas_sem_variacao': int((dF == 0).sum()),
           'soma_variacao_flavio_candidatas': int(dF.sum()), 'votos_flavio_1t_candidatas': int(d['R1'][cand].sum()),
           'fora_da_lista_por_aptos_diferentes': int(fora.sum()),
           'lista_300': resumo(top), 'por_uf': dict(collections.Counter(d['uf'][top]).most_common()),
           'por_regiao': dict(collections.Counter(d['reg'][top]).most_common()),
           'por_tipo_local': dict(collections.Counter(l['tipo_local'] for l in linhas).most_common()),
           'sem_cadastro_de_local': int(sum(1 for l in linhas if not l['nome_local'])),
           'municipios_na_lista': int(len(set(d['mun'][top]))),
           'candidatas_por_uf': dict(collections.Counter(d['uf'][cand]).most_common()),
           'espelho_lula': {'candidatas': int(len(candL)), 'candidatas_com_queda': int((dL < 0).sum()),
                            'soma_variacao_lula_candidatas': int(dL.sum()),
                            'lista_300': resumo(topL, 'L', 'R'),
                            'por_uf': dict(collections.Counter(d['uf'][topL]).most_common())},
           'sha256_csv': hashlib.sha256(open(SAIDA_CSV, 'rb').read()).hexdigest()}
    grava('lista_resumo.json', res)
    if os.path.exists(SAIDA_JSON):
        R = json.load(open(SAIDA_JSON))
        R['lista_para_cadernos'] = res
        with open(SAIDA_JSON, 'w') as f:
            json.dump(R, f, ensure_ascii=False, indent=1)
    diga('lista gravada', SAIDA_CSV, {k: v for k, v in res.items() if k not in ('candidatas_por_uf',)})


# ---------------------------------------------------------------- EXPLORATÓRIO (escrito DEPOIS de ver o resultado de rodar)
def explorar():
    """Tudo aqui foi decidido depois de ver os números registrados; não muda veredito. Motivo: a sensibilidade fixada
    "só seções com 50 ou mais votos de Flávio" deu A = 0,000 na faixa de menos de 10%, e a faixa é 61% Nordeste."""
    R = json.load(open(SAIDA_JSON))
    E = {'aviso': 'Exploratório, feito depois de ver os resultados registrados. Não decide veredito.'}
    d = carrega(2026)
    y, X, apt, a = variaveis(d)
    U = d['U']
    s0 = faixa_sel(d, a, 0)
    mun_g = codigos(d['mun'])
    ng = int(mun_g.max()) + 1

    def r(m):
        if m is None:
            return None
        return {k: m[k] for k in ('A', 'ep', 'n_secoes_faixa', 'n_no_ajuste', 'municipios_informativos', 'votos_F_1t',
                                  'votos_L_1t', 'aptos', 'abst_media_ponderada', 'y_medio_ponderado', 'V_votos')}

    # (a) por quantidade de votos de Flávio na seção, faixa de menos de 10%
    E['faixa1_por_votos_de_flavio'] = {}
    for nome, sel in [('menos de 20', d['R1'] < 20), ('20 a 49', (d['R1'] >= 20) & (d['R1'] < 50)), ('menos de 50', d['R1'] < 50),
                      ('50 ou mais', d['R1'] >= 50), ('20 ou mais', d['R1'] >= 20), ('30 ou mais', d['R1'] >= 30),
                      ('100 ou mais', d['R1'] >= 100)]:
        E['faixa1_por_votos_de_flavio'][nome] = r(modelo0(d, s0 & sel))
    # espelho da sensibilidade: 50 ou mais votos de Lula; e os dois
    E['faixa1_50_ou_mais_votos_de_lula'] = r(modelo0(d, s0 & (d['L1'] >= 50)))
    E['faixa1_50_ou_mais_dos_dois'] = r(modelo0(d, s0 & (d['L1'] >= 50) & (d['R1'] >= 50)))
    # (b) a mesma restrição nas outras faixas e no país
    E['50_ou_mais_votos_F_por_faixa'] = [r(modelo0(d, faixa_sel(d, a, i) & (d['R1'] >= 50))) for i in range(len(FAIXAS))]
    E['menos_de_50_votos_F_por_faixa'] = [r(modelo0(d, faixa_sel(d, a, i) & (d['R1'] < 50))) for i in range(len(FAIXAS))]
    E['50_ou_mais_votos_F_pais'] = r(modelo0(d, U & (d['R1'] >= 50)))
    # (c) por força de Lula na seção (Lula sobre válidos do 1º turno), faixa de menos de 10%
    val = (d['R1'] + d['L1'] + d['O1']).astype(float)
    fl = np.where(val > 0, d['L1'] / np.where(val > 0, val, 1), 0)
    E['faixa1_por_forca_de_lula'] = {}
    for lo, hi, nome in [(0, .35, 'menos de 35%'), (.35, .5, '35 a 50%'), (.5, .65, '50 a 65%'), (.65, .8, '65 a 80%'), (.8, 1.01, '80% ou mais')]:
        E['faixa1_por_forca_de_lula'][nome] = r(modelo0(d, s0 & (fl >= lo) & (fl < hi)))
    # (d) tamanho da seção: descritivo e controle
    def desc(sel):
        return {'secoes': int(sel.sum()), 'aptos_medio': float(d['apt1'][sel].mean()), 'aptos_mediana': float(np.median(d['apt1'][sel])),
                'votos_F': int(d['R1'][sel].sum()), 'votos_L': int(d['L1'][sel].sum()),
                'y_medio': float((d['c2'][sel] - d['c1'][sel]).sum() / d['apt1'][sel].sum()),
                'comp_caiu': int((sel & (y < 0)).sum()), 'comp_subiu': int((sel & (y > 0)).sum()),
                'fatia_F_sobre_aptos': float(d['R1'][sel].sum() / d['apt1'][sel].sum()),
                'var_F': int((d['R2'] - d['R1'])[sel].sum()), 'var_L': int((d['L2'] - d['L1'])[sel].sum()),
                'var_comp': int((d['c2'] - d['c1'])[sel].sum()), 'elim_1t': int(d['O1'][sel].sum()),
                'var_BN': int(((d['B2'] + d['N2']) - (d['B1'] + d['N1']))[sel].sum())}
    E['faixa1_descritivo'] = {'menos de 50 votos de Flávio': desc(s0 & (d['R1'] < 50)), '50 ou mais': desc(s0 & (d['R1'] >= 50)),
                              'todas': desc(s0), 'Nordeste': desc(s0 & (d['reg'] == 'NE')), 'fora do Nordeste': desc(s0 & (d['reg'] != 'NE'))}
    for nome, extra in [('com_log_aptos', np.log(apt)), ('com_aptos', apt / 1000.0)]:
        Xe = np.column_stack([X, extra])
        aj = Ajuste(Xe[s0], d['mun'][s0], apt[s0], d['mun'][s0])
        c = np.array([1.0, -1.0, 0, 0, 0])
        b, V = aj.coef(y[s0])
        E['faixa1_' + nome] = {'A': float(c @ b), 'ep': float(np.sqrt(c @ V @ c)), 'coef_extra': float(b[4]), 'ep_extra': float(np.sqrt(V[4, 4]))}
    for corte in (100, 200):
        E[f'faixa1_secoes_com_{corte}_ou_mais_aptos'] = r(modelo0(d, s0 & (d['apt1'] >= corte)))
    # (e) Nordeste e resto, com e sem a restrição de 50 votos
    E['faixa1_NE_50_ou_mais'] = r(modelo0(d, s0 & (d['reg'] == 'NE') & (d['R1'] >= 50)))
    E['faixa1_NE_menos_de_50'] = r(modelo0(d, s0 & (d['reg'] == 'NE') & (d['R1'] < 50)))
    E['faixa1_fora_NE'] = r(modelo0(d, s0 & (d['reg'] != 'NE')))
    E['faixa1_fora_NE_50_ou_mais'] = r(modelo0(d, s0 & (d['reg'] != 'NE') & (d['R1'] >= 50)))
    E['faixa1_sem_CE'] = r(modelo0(d, s0 & (d['uf'] != 'CE')))
    E['faixa1_so_CE'] = r(modelo0(d, s0 & (d['uf'] == 'CE')))
    # (f) diferença entre a faixa inteira e o recorte de 50 ou mais, por reamostragem de municípios
    s50 = s0 & (d['R1'] >= 50)
    sne = s0 & (d['reg'] == 'NE')
    sfo = s0 & (d['reg'] != 'NE')
    ajs = {n: Ajuste(X[s], d['mun'][s], apt[s], d['mun'][s]) for n, s in [('todas', s0), ('50', s50)]}
    suf = {n: ajs[n].suficientes(y[s], mun_g[s], ng) for n, s in [('todas', s0), ('50', s50)]}
    rng = np.random.default_rng(SEMENTE + 7)
    usados = np.unique(mun_g[U])
    dif = []
    for _ in range(999):
        mult = np.bincount(rng.choice(usados, size=len(usados), replace=True), minlength=ng).astype(float)
        try:
            dif.append(reamostra(suf['todas'], mult) - reamostra(suf['50'], mult))
        except np.linalg.LinAlgError:
            pass
    dif = np.array(dif)
    E['faixa1_diferenca_todas_menos_50_ou_mais'] = {'dif': R['faixas_2026'][0]['A'] - R['sensibilidades']['faixa1_50_ou_mais_votos_F']['A'],
                                                    'ep_reamostragem': float(dif.std(ddof=1)),
                                                    'ic95': [float(np.percentile(dif, 2.5)), float(np.percentile(dif, 97.5))]}
    # (g) calibração dentro do recorte de 50 ou mais (sem sorteio) e a retirada que o recorte exclui
    det = plantios(d, None, det=True)
    f50 = np.zeros(len(U))
    f50[s50] = ajs['50'].funcional()
    m50 = R['sensibilidades']['faixa1_50_ou_mais_votos_F']
    dr = float(f50 @ det['retirada_F'][0])
    de = float(f50 @ det['entrada_L'][0])
    E['faixa1_50_ou_mais_calibracao_sem_sorteio'] = {
        'dA_retirada': dr, 'dA_entrada': de, 'R': abs(de / dr), 'retirada_em_ep': abs(dr) / m50['ep'],
        'retirada_maxima_compativel_2ep_pct_dos_votos_F': 100 * TAXA * max(0.0, -(m50['A'] - 2 * m50['ep'])) / abs(dr),
        'idem_faixa_inteira': 100 * TAXA * max(0.0, -(R['faixas_2026'][0]['A'] - 2 * R['faixas_2026'][0]['ep']))
        / abs(R['calibracao']['sem_sorteio']['retirada_F']['dA_faixas'][0])}
    # (h) outros anos: a mesma restrição (50 ou mais votos do adversário do PT) e o Nordeste por faixa
    E['anos'] = {}
    for ano in ANOS:
        da = d if ano == 2026 else carrega(ano)
        ya, Xa, apta, aa = variaveis(da)
        b0 = faixa_sel(da, aa, 0)
        o = {'faixa1_50_ou_mais': r(modelo0(da, b0 & (da['R1'] >= 50))), 'faixa1_menos_de_50': r(modelo0(da, b0 & (da['R1'] < 50))),
             'NE_por_faixa': [r(modelo0(da, faixa_sel(da, aa, i, da['U'] & (da['reg'] == 'NE')))) for i in range(len(FAIXAS))],
             'faixa1_fora_NE': r(modelo0(da, b0 & (da['reg'] != 'NE'))),
             'faixa1_parte_quedas': modelo0(da, b0, y=np.minimum(ya, 0))['A'], 'faixa1_parte_altas': modelo0(da, b0, y=np.maximum(ya, 0))['A'],
             'faixa1_ep_parte_quedas': modelo0(da, b0, y=np.minimum(ya, 0))['ep'], 'faixa1_ep_parte_altas': modelo0(da, b0, y=np.maximum(ya, 0))['ep'],
             'faixa1_efeito_fixo_local': r(modelo0(da, b0, fe='local')),
             'faixa1_secoes_NE': int((b0 & (da['reg'] == 'NE')).sum()), 'faixa1_secoes': int(b0.sum())}
        E['anos'][str(ano)] = o
    # (i) 2026 menos cada ano na faixa de menos de 10% (amostras de anos diferentes tratadas como independentes)
    E['faixa1_2026_menos_ano'] = {}
    f26 = R['anos']['2026']['faixas'][0]
    for ano in ('2022', '2018', '2014'):
        fa = R['anos'][ano]['faixas'][0]
        ne26, nea = R['anos']['2026']['faixa1_por_regiao']['NE'], R['anos'][ano]['faixa1_por_regiao']['NE']
        E['faixa1_2026_menos_ano'][ano] = {'dif': f26['A'] - fa['A'], 'ep': float(np.hypot(f26['ep'], fa['ep'])),
                                           'dif_NE': ne26['A'] - nea['A'], 'ep_NE': float(np.hypot(ne26['ep'], nea['ep']))}
    R['exploratorio'] = E
    grava('parcial_exploratorio.json', E)
    with open(SAIDA_JSON, 'w') as f:
        json.dump(R, f, ensure_ascii=False, indent=1)
    diga('exploratório gravado')


def explorar2():
    """Segundo bloco exploratório (depois de ver o primeiro): poucos votos contra muitos votos, em todas as faixas e
    anos; o espelho (seções com poucos votos de Lula); perfil por faixa contra a previsão da entrada."""
    R = json.load(open(SAIDA_JSON))
    E = R['exploratorio']
    out = {}
    for ano in ANOS:
        d = carrega(ano)
        y, X, apt, a = variaveis(d)
        U = d['U']
        o = {}
        for nome, sel in [('F_menos_de_50', d['R1'] < 50), ('F_50_ou_mais', d['R1'] >= 50),
                          ('L_menos_de_50', d['L1'] < 50), ('L_50_ou_mais', d['L1'] >= 50)]:
            linhas = []
            for i in range(len(FAIXAS)):
                m = modelo0(d, faixa_sel(d, a, i) & sel)
                linhas.append(None if m is None else {'A': m['A'], 'ep': m['ep'], 'n': m['n_secoes_faixa'],
                                                      'votos_F_1t': m['votos_F_1t'], 'votos_L_1t': m['votos_L_1t'],
                                                      'V_votos': m['V_votos'], 'municipios': m['municipios_informativos']})
            m = modelo0(d, U & sel)
            o[nome] = {'faixas': linhas, 'todas': {'A': m['A'], 'ep': m['ep'], 'n': m['n_secoes_faixa'], 'votos_F_1t': m['votos_F_1t'],
                                                   'votos_L_1t': m['votos_L_1t'], 'V_votos': m['V_votos']}}
        if ano == 2026:
            # perfil por faixa no recorte de 50 ou mais votos de Flávio contra a previsão da entrada (sem sorteio)
            det = plantios(d, None, det=True)
            s50 = U & (d['R1'] >= 50)
            ajp = Ajuste(X[s50], d['mun'][s50], apt[s50], d['mun'][s50])
            fp = np.zeros(len(U))
            fp[s50] = ajp.funcional()
            Ap = float(fp @ y)
            esc = Ap / float(fp @ det['entrada_L'][0])
            escr = Ap / float(fp @ det['retirada_F'][0])
            perfil = []
            for i in range(len(FAIXAS)):
                s = faixa_sel(d, a, i) & (d['R1'] >= 50)
                aj = Ajuste(X[s], d['mun'][s], apt[s], d['mun'][s])
                f = np.zeros(len(U))
                f[s] = aj.funcional()
                Ai, epi, _, _ = aj.A(y[s])
                perfil.append({'faixa': FAIXAS[i][2], 'A': Ai, 'ep': epi, 'previsto_so_entrada': esc * float(f @ det['entrada_L'][0]),
                               'previsto_so_saida_uniforme': escr * float(f @ det['retirada_F'][0])})
            qe = sum(((p['A'] - p['previsto_so_entrada']) / p['ep']) ** 2 for p in perfil)
            qs = sum(((p['A'] - p['previsto_so_saida_uniforme']) / p['ep']) ** 2 for p in perfil)
            o['perfil_50_ou_mais_contra_previsoes'] = {'A_pais_recorte': Ap, 'escala_entrada': esc, 'escala_saida': escr, 'faixas': perfil,
                                                       'soma_quadrados_padronizados_entrada': qe, 'soma_quadrados_padronizados_saida': qs,
                                                       'nota': 'as faixas partilham municípios; as somas servem só para comparar as duas formas'}
        out[str(ano)] = o
    E['poucos_e_muitos_votos'] = out
    R['exploratorio'] = E
    grava('parcial_exploratorio2.json', out)
    with open(SAIDA_JSON, 'w') as f:
        json.dump(R, f, ensure_ascii=False, indent=1)
    diga('exploratório 2 gravado')


if __name__ == '__main__':
    cmd = sys.argv[1] if len(sys.argv) > 1 else ''
    if cmd == 'base':
        base()
    elif cmd == 'rodar':
        rodar()
    elif cmd == 'lista':
        lista()
    elif cmd == 'explorar':
        explorar()
    elif cmd == 'explorar2':
        explorar2()
    else:
        print(__doc__)
