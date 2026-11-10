#!/usr/bin/env python3
"""R27_N3: FORMA REGULADA PELA FORÇA DE LULA (Adendo 28, teste N3; confirmação de um exploratório).

Registro: PRE-REGISTRO-2026-10-26.md, seção "Adendo 28", item N3 (commit 938be19, 10/11/2026 04:36:33 UTC), com os
avisos do Adendo 27 (commit 2748895, 10/11/2026 00:16:42 UTC). Aplicado pela letra, sem mudar limiar.

Este docstring foi escrito ANTES de calcular qualquer resultado com votos. Cópia com data e SHA-256 em
/home/user/trabalho-eleicao/adendo27/R27_N3/docstring_antes_de_rodar.txt. Não havia execução anterior deste teste
em disco (nem script, nem pasta de trabalho) quando este arquivo foi criado.

Uso (sempre com python3 -I):
  python3 -I scripts/analisar_R27_N3.py          roda tudo e grava resultados/R27_N3_forma_concentrada.json e .txt
  python3 -I scripts/analisar_R27_N3.py texto    só reescreve o .txt a partir do .json

O QUE EU JÁ SABIA ANTES DE ESCREVER (por isso NÃO é teste cego; é confirmação por outro agente)
  Li o resumo da Onda A e a conferência da A3. O conferente da A3 calculou, depois de ver os resultados, que onde
  Flávio tem menos de 35% a parcela dos votos dele que aparece em Lula é +0,0161 (ep 0,0030; n 95.386), abaixo do
  espelho (+0,0208, ep 0,0022), que a forma concentrada plantada (2.136.651 votos) sobe essa parcela em 4,03 pontos,
  e que a diferença entre os dois sentidos por UF vai de -0,043 (RR) a +0,034 (AM). Li o código dele só para saber
  as definições que o registro cita; não importo nem uso código ou cache dele. Não abri os resultados de N1 e N2.

O QUE O REGISTRO FIXA (texto do N3)
  "O conferente da A3 já calculou, depois de ver os resultados, que onde Flávio tem menos de 35% a parcela dos votos
  dele que aparece em Lula é +0,0161, abaixo do espelho (+0,0208). Por isso este teste é confirmação por outro
  agente, não teste cego.
  Matriz de transferência por seção sem a variação do comparecimento como controle, por faixa de força de Flávio no
  local (menos de 35%, 35 a 50, 50 a 65, 65 ou mais), com o espelho de Lula.
  Sinal: na faixa de menos de 35%, parcela de Flávio que aparece em Lula acima do espelho em 0,02 ou mais, a mais de
  4 erros-padrão. Sem sinal: diferença mais 2 erros-padrão abaixo de 0,01, com a forma concentrada plantada
  (2.136.651 votos) detectada."

DECISÕES QUE O REGISTRO NÃO FIXA (tomadas aqui, antes de qualquer conta com votos; relatadas como desvios)

D1. Base: dados/secoes2026.json.gz e dados/candidatos2026_1t.json.gz. Seções com os dois turnos. Local de votação =
    UF, município, zona e número do local do 2º turno.
D2. Universo principal: seções com aptos iguais (e maiores que zero) nos dois turnos, com o exterior. É o universo
    do exploratório que se confirma, e com aptos iguais cada linha da matriz soma 1. Ao lado: sem o exterior; todas
    as seções com os dois turnos; o universo do desenho D4-1 (diferença de aptos de até 2, comparecimento do 1º
    turno de 30 ou mais, sem o exterior, peso 1/aptos, erro por município).
D3. Matriz de transferência. Respostas, em número de eleitores do 2º turno: L2 (Lula), R2 (Flávio), BN2 (brancos
    mais nulos) e A2 (aptos menos comparecimento). Regressoras, em número de eleitores do 1º turno: L1, R1, Cury
    (70), Renan (14), Caiado (55), Zema (30), demais candidatos (inclui o 28, anulado), BN1 (brancos mais nulos) e
    A1 (aptos menos comparecimento). Nenhuma variação de comparecimento entra como controle. Efeito fixo de local
    de votação, sem peso, erro agrupado por local (CR1), tudo como na conta do exploratório. Rodada em separado
    dentro de cada recorte: local com uma seção só dentro do recorte não informa e sai. Estimador escrito aqui e
    conferido uma vez contra lib.fe_ols.
    V = coeficiente de R1 na equação de L2 (parcela dos votos de Flávio no 1º turno que aparece em Lula no 2º).
    M = coeficiente de L1 na equação de R2 (o sentido contrário).
    Ao lado: outros agregados num termo só; branco e nulo separados; efeito fixo de município.
D4. "Força de Flávio no local". A frase admite duas leituras, e as duas são calculadas com veredito completo.
    Leitura A (a letra, como no T35, que usa as mesmas quatro faixas): fatia de Flávio entre os votos válidos do
    1º turno do LOCAL DE VOTAÇÃO (soma de todas as seções do local com os dois turnos; válidos = L1 + R1 + outros
    menos o 28). O local inteiro cai numa faixa só.
    Leitura B (a conta do exploratório que se confirma): a mesma fatia na própria SEÇÃO.
    O veredito "pela letra" é o da Leitura A. A Leitura B sai ao lado com o mesmo critério. Se as duas derem
    vereditos diferentes, isso é dito no veredito e nenhuma das duas é escondida.
    Faixas: [0; 0,35), [0,35; 0,50), [0,50; 0,65), [0,65; 1]. Local ou seção sem voto válido não entra.
D5. Espelho de Lula: M medido na faixa em que LULA tem menos de 35% (mesma leitura, A ou B). Estatística:
    D = V(faixa em que Flávio tem menos de 35%) menos M(faixa em que Lula tem menos de 35%).
    Erro-padrão de D: pela contribuição de cada local às duas estimativas (um local que esteja nos dois recortes
    entra com a covariância). Ao lado: raiz da soma dos quadrados dos dois erros e erro agrupado por município.
D6. Critério, pela letra. SINAL: D >= 0,02 e D/ep > 4 (distância a zero, como as leituras anteriores da mesma
    expressão; ao lado, a distância ao limiar, (D - 0,02)/ep). SEM SINAL: D + 2 ep < 0,01 e forma concentrada
    detectada. "Detectada" = o critério de SINAL dispara nos dados de 2026 com a forma plantada por cima, na
    versão pelo valor esperado e em pelo menos 95% de 200 sorteios. SEM PODER: o critério de sinal não dispara nos
    dados brutos e a forma plantada não é detectada. Qualquer outro caso: INCONCLUSIVO.
    Ao lado, leitura mais frouxa de "detectada": D sobe 0,02 ou mais com o plantio. Se as duas leituras de
    "detectada" derem vereditos diferentes, isso é dito.
D7. Forma concentrada plantada (a do registro). Regra C1, que é a do exploratório de onde saiu o número
    2.136.651: em toda seção do país com os dois turnos (com o exterior), d votos saem de Flávio no 2º turno e
    entram em Lula no 2º turno, d = binomial(R2, p), p = min(1, k x fatia de Lula entre os válidos do 1º turno
    DA SEÇÃO), com k resolvido para que o total esperado seja exatamente 2.136.651. 1º turno, branco, nulo e
    comparecimento ficam intactos. 200 sorteios (semente 28032026, cenário, índice) e a versão pelo valor
    esperado (d = R2 x p, sem sorteio). Doses pelo valor esperado: 10%, 25%, 50%, 75%, 100% e 125% do total.
    Outras regras de concentração, ao lado, com o mesmo total esperado (30 sorteios e valor esperado), para
    saber se a detecção depende da regra:
      C1L: taxa proporcional à fatia de Lula no LOCAL de votação.
      C2:  só nas seções em que Lula teve 50% ou mais dos válidos no 1º turno, taxa uniforme nelas.
      C3:  taxa proporcional ao quadrado da fatia de Lula na seção.
      C4:  forma k x L: votos trocados proporcionais aos votos de Lula no 2º turno da seção (limitados a R2).
      C5:  só nas nove UFs do Nordeste, taxa uniforme nelas.
      U:   uniforme (mesma taxa em toda seção), como referência.
D8. Explicações que passam pelo comparecimento, plantadas para medir especificidade (200 sorteios e valor
    esperado; mesma regra C1 e mesmo total de 2.136.651, salvo a I2):
      I1: abstenção pura concentrada. a = binomial(R2, p da regra C1) sai de Flávio no 2º turno e vira faltoso
          (comparecimento do 2º turno cai); nenhum voto para Lula.
      I2: abstenção pura uniforme de 3,6% dos votos de Flávio (o tamanho da retirada do N2).
      I3: entrada de eleitores reais concentrada. e = binomial(A2, min(1, k x fatia de Lula na seção)) sai dos
          faltosos do 2º turno e vira voto em Lula; nada sai de Flávio.
      I4: I1 e I3 juntas (a virada inteira pelo comparecimento, 4.273.302 de margem, sem nenhuma troca).
    O teste "distingue" se o critério de SINAL dispara com a troca (D7) e não dispara com I1 a I4.
    Aviso fixado antes: boletim não separa eleitor que faltou de eleitor registrado como faltoso, nem eleitor
    real que entrou de voto lançado em nome de faltoso. "Explicação inocente" aqui quer dizer só "passa pelo
    comparecimento e não por troca de voto dentro da urna". Este teste, por construção, não acusa nem absolve o
    canal do comparecimento.
    Fato aritmético conhecido antes de rodar: abstenção pura não mexe em L2, logo não mexe em V; se mexer em D,
    é pelo espelho M. Por isso sai ao lado a estatística só com V (V com plantio menos V bruto) e D com M fixo.
    Teste de estresse, ao lado, fora do veredito: troca C1 mais entrada I3 juntas (a troca fica mascarada?).
D9. Espelho do teste. (i) O critério invertido nos dados brutos: -D >= 0,02 a mais de 4 ep (Lula perdendo para
    Flávio onde Lula é fraco, acima do que Flávio perde onde Flávio é fraco). (ii) Plantio espelho: 2.136.651
    votos de Lula para Flávio, taxa proporcional à fatia de Flávio na seção; o critério invertido tem de
    disparar e o direto não. (iii) As outras três faixas (D por faixa), descritivo.
D10. Outros anos (2014, 2018, 2022): só ao lado, com outros agregados (as bases não separam os eliminados), e com
    o valor de 2026 na mesma especificação na mesma linha. Não é régua e nenhum veredito depende deles.
D11. Por UF (descritivo, sem veredito): a matriz inteira dentro de cada uma das 27 UFs (exterior à parte), no
    universo principal; V, M e D = V - M com erro conjunto por local; quem não voltou (coeficientes de R1 e de
    L1 em A2) e faltosos do 1º turno que aparecem em Lula e em Flávio. Homogeneidade de D entre as UFs
    (qui-quadrado contra a média ponderada pelo inverso da variância) e contagem de UFs além de +0,010 e de
    -0,010. Ao lado: D por UF com a forma C1 plantada (valor esperado) e, onde houver 30 locais ou mais em cada
    lado, V e M dentro da faixa de menos de 35% (Leitura A).
D12. Tradução em votos de margem.
    (i) Direta: D x votos de Flávio no 1º turno nas seções da faixa (país inteiro, mesma leitura) = votos
        líquidos acima do espelho; vezes 2 = margem; teto com D + 2 ep. Margem oficial: 4.430.191.
    (ii) Pela calibração: a forma C1 de 2.136.651 votos (4.273.302 de margem) sobe D em dD. Tamanho máximo
        compatível = max(0, D + 2 ep) / dD x 2.136.651, com a premissa de que sem desvio D seria zero (o espelho
        é o nível natural). Sem essa premissa (premissa extrema: nível natural de V igual a zero, tudo em V é
        troca): (V + 2 ep) / dV x 2.136.651. As duas leituras saem lado a lado, cada uma com a sua premissa.
D13. Contagem de testes: um critério de decisão, em duas leituras da faixa. O relatório diz se disparou e o que o
    acaso daria.
D14. O que for feito depois de ver resultados fica em funções com nome "exploratorio_" e sai marcado assim.
"""
import sys, os, gzip, json, time, hashlib, datetime
import numpy as np

RAIZ = '/home/user/casa-control/eleicao-2026'
TRAB = '/home/user/trabalho-eleicao/adendo27/R27_N3'
SAIDA_JSON = RAIZ + '/resultados/R27_N3_forma_concentrada.json'
SAIDA_TXT = RAIZ + '/resultados/R27_N3_forma_concentrada.txt'

TOTAL = 2136651
SEMENTE = 28032026
F2_OFICIAL, L2_OFICIAL, MARGEM = 59826041, 64256232, 4430191
FAIXAS = [(0.0, 0.35), (0.35, 0.50), (0.50, 0.65), (0.65, 1.0001)]
NOME_FAIXA = ['menos de 35%', '35 a 50%', '50 a 65%', '65% ou mais']
NORDESTE = ('AL', 'BA', 'CE', 'MA', 'PB', 'PE', 'PI', 'RN', 'SE')
REGIAO = {'N': ('AC', 'AM', 'AP', 'PA', 'RO', 'RR', 'TO'), 'NE': NORDESTE, 'SE': ('ES', 'MG', 'RJ', 'SP'),
          'S': ('PR', 'RS', 'SC'), 'CO': ('DF', 'GO', 'MS', 'MT')}
NSORT, NSORT_LADO = 200, 30
T0 = time.time()


def log(*a):
    print('[%6.1fs]' % (time.time() - T0), *a, flush=True)


def agora():
    return datetime.datetime.now(datetime.timezone.utc).strftime('%Y-%m-%d %H:%M:%S UTC')


def limpa(o):
    if isinstance(o, dict):
        return {str(k): limpa(v) for k, v in o.items()}
    if isinstance(o, (list, tuple)):
        return [limpa(v) for v in o]
    if isinstance(o, (np.integer,)):
        return int(o)
    if isinstance(o, (np.floating,)):
        return None if not np.isfinite(o) else float(o)
    if isinstance(o, float):
        return None if not np.isfinite(o) else o
    if isinstance(o, (np.bool_,)):
        return bool(o)
    if isinstance(o, np.ndarray):
        return limpa(o.tolist())
    return o


def gravar(nome, o):
    os.makedirs(TRAB, exist_ok=True)
    tmp = os.path.join(TRAB, nome + '.tmp')
    with open(tmp, 'w') as f:
        json.dump(limpa(o), f, ensure_ascii=False, indent=1)
    os.replace(tmp, os.path.join(TRAB, nome))


# ------------------------------------------------------------------ base
def montar_base(ano):
    """Seções com os dois turnos, em vetores. Cache em TRAB (menos de 30 MB por ano)."""
    cache = os.path.join(TRAB, 'base_%d.npz' % ano)
    if os.path.exists(cache):
        z = np.load(cache, allow_pickle=False)
        return {k: z[k] for k in z.files}
    with gzip.open('%s/dados/secoes%d.json.gz' % (RAIZ, ano), 'rt') as f:
        d = json.load(f)
    cand = {}
    if ano == 2026:
        with gzip.open(RAIZ + '/dados/candidatos2026_1t.json.gz', 'rt') as f:
            cand = json.load(f)['secoes']
    chaves, locs, muns, num = [], [], [], []
    for k, v in d.items():
        if '1' not in v or '2' not in v:
            continue
        a, b = v['1'], v['2']
        uf, mu, zo, se = k.split('|')
        cv = cand.get(k, {})
        chaves.append(k)
        locs.append('%s|%s|%s|%s' % (uf, mu, zo, b['loc']))
        muns.append('%s|%s' % (uf, mu))
        num.append([a['L'], a['R'], a['O'], a['B'], a['N'], a['comp'], a['apt'], a.get('c28', 0),
                    cv.get('70', 0), cv.get('14', 0), cv.get('55', 0), cv.get('30', 0),
                    b['L'], b['R'], b['O'], b['B'], b['N'], b['comp'], b['apt']])
    del d, cand
    A = np.array(num, np.int64)
    nomes = ['L1', 'R1', 'O1', 'B1', 'N1', 'comp1', 'apt1', 'c28', 'g70', 'g14', 'g55', 'g30',
             'L2', 'R2', 'O2', 'B2', 'N2', 'comp2', 'apt2']
    B = {n: A[:, i].copy() for i, n in enumerate(nomes)}
    _, B['loc'] = np.unique(np.array(locs), return_inverse=True)
    _, B['mun'] = np.unique(np.array(muns), return_inverse=True)
    B['uf'] = np.array([k[:2] for k in chaves])
    os.makedirs(TRAB, exist_ok=True)
    np.savez_compressed(cache, **B)
    return B


def regressoras(B, modo='grupos'):
    """Colunas do 1º turno. Devolve X, nomes, índice de L1 e de R1."""
    BN1 = B['B1'] + B['N1']
    A1 = B['apt1'] - B['comp1']
    if modo == 'grupos':
        dem = B['O1'] - B['g70'] - B['g14'] - B['g55'] - B['g30']
        cols = [B['L1'], B['R1'], B['g70'], B['g14'], B['g55'], B['g30'], dem, BN1, A1]
        nomes = ['L1', 'R1', 'Cury', 'Renan', 'Caiado', 'Zema', 'demais', 'BN1', 'A1']
    elif modo == 'agregado':
        cols = [B['L1'], B['R1'], B['O1'], BN1, A1]
        nomes = ['L1', 'R1', 'outros', 'BN1', 'A1']
    elif modo == 'bn_separados':
        dem = B['O1'] - B['g70'] - B['g14'] - B['g55'] - B['g30']
        cols = [B['L1'], B['R1'], B['g70'], B['g14'], B['g55'], B['g30'], dem, B['B1'], B['N1'], A1]
        nomes = ['L1', 'R1', 'Cury', 'Renan', 'Caiado', 'Zema', 'demais', 'B1', 'N1', 'A1']
    else:
        raise ValueError(modo)
    return np.column_stack(cols).astype(float), nomes


def respostas(B):
    return {'L2': B['L2'].astype(float), 'R2': B['R2'].astype(float),
            'BN2': (B['B2'] + B['N2']).astype(float), 'A2': (B['apt2'] - B['comp2']).astype(float)}


def fatias(B):
    """Fatia de Flávio e de Lula entre os válidos do 1º turno: na seção e no local (soma das seções do local)."""
    val = (B['L1'] + B['R1'] + B['O1'] - B['c28']).astype(float)
    with np.errstate(divide='ignore', invalid='ignore'):
        fFs = np.where(val > 0, B['R1'] / val, np.nan)
        fLs = np.where(val > 0, B['L1'] / val, np.nan)
        nl = int(B['loc'].max()) + 1
        vl = np.bincount(B['loc'], weights=val, minlength=nl)
        rl = np.bincount(B['loc'], weights=B['R1'].astype(float), minlength=nl)
        ll = np.bincount(B['loc'], weights=B['L1'].astype(float), minlength=nl)
        fFl = np.where(vl > 0, rl / vl, np.nan)[B['loc']]
        fLl = np.where(vl > 0, ll / vl, np.nan)[B['loc']]
    return {'val': val, 'fFs': fFs, 'fLs': fLs, 'fFl': fFl, 'fLl': fLl}


def em_faixa(f, i):
    lo, hi = FAIXAS[i]
    return np.isfinite(f) & (f >= lo) & (f < hi)


# ------------------------------------------------------------------ estimador (efeito fixo, CR1, influência por grupo)
class Recorte:
    """Regressão com efeito fixo de grupo dentro de um recorte. Guarda X já centrado para reusar com muitos y."""

    def __init__(self, X, grupo, mask, w=None):
        idx = np.flatnonzero(mask)
        gr = grupo[idx]
        u, g = np.unique(gr, return_inverse=True)
        cnt = np.bincount(g, minlength=len(u))
        ok = cnt[g] >= 2
        self.secoes = int(len(idx))
        idx = idx[ok]
        u, g = np.unique(gr[ok], return_inverse=True)
        self.idx, self.g, self.gid, self.G = idx, g, u, int(len(u))
        self.N, self.k = int(len(idx)), int(X.shape[1])
        self.w = np.ones(self.N) if w is None else np.asarray(w, float)[idx]
        self.sw = np.bincount(g, weights=self.w, minlength=self.G)
        self.vazio = self.N <= self.k + 1 or self.G < 2
        if self.vazio:
            return
        self.Xd = self._centra(X[idx])
        XtX = (self.Xd * self.w[:, None]).T @ self.Xd
        self.inv = np.linalg.pinv(XtX)
        self.c = self.G / (self.G - 1) * (self.N - 1) / (self.N - self.k)
        self.Z = self.Xd @ self.inv           # N x k: linha i, coluna j = contribuição da seção i ao coeficiente j

    def _centra(self, M):
        M = np.asarray(M, float)
        if M.ndim == 1:
            m = np.bincount(self.g, weights=self.w * M, minlength=self.G) / self.sw
            return M - m[self.g]
        out = np.empty_like(M)
        for j in range(M.shape[1]):
            m = np.bincount(self.g, weights=self.w * M[:, j], minlength=self.G) / self.sw
            out[:, j] = M[:, j] - m[self.g]
        return out

    def ajusta(self, y_inteiro, js=None):
        """y_inteiro: vetor do tamanho da base. Devolve b, ep (CR1 por grupo) e psi (influência por grupo, sem o
        fator c) para as colunas js (todas, se js for None)."""
        yd = self._centra(y_inteiro[self.idx])
        b = self.inv @ (self.Xd.T @ (self.w * yd))
        e = yd - self.Xd @ b
        js = range(self.k) if js is None else js
        psi, ep = {}, {}
        we = self.w * e
        for j in js:
            p = np.bincount(self.g, weights=self.Z[:, j] * we, minlength=self.G)
            psi[j] = p
            ep[j] = float(np.sqrt(self.c * (p @ p)))
        return b, ep, psi


def ep_conjunto(partes, nclu, mapa=None, n_k=None):
    """Erro-padrão de uma soma com sinais de coeficientes de recortes (possivelmente) diferentes.
    partes: lista de (recorte, psi do coeficiente, sinal). Agrupa pela identidade global do grupo (local).
    mapa: se dado, vetor local -> município, para agrupar por município (fator CR1 com o número de municípios)."""
    tot = np.zeros(nclu)
    for rec, psi, s in partes:
        if mapa is None:
            np.add.at(tot, rec.gid, s * np.sqrt(rec.c) * psi)
        else:
            mg = mapa[rec.gid]
            Gm = len(np.unique(mg))
            cm = Gm / (Gm - 1) * (rec.N - 1) / (rec.N - rec.k)
            np.add.at(tot, mg, s * np.sqrt(cm) * psi)
    return float(np.sqrt(tot @ tot))


def matriz(rec, Y, nomes, nloc):
    """Matriz inteira dentro de um recorte: as quatro equações. V, M, quem não voltou, faltosos que entraram."""
    if rec.vazio:
        return {'secoes': rec.secoes, 'n': rec.N, 'locais': rec.G, 'vazio': True}
    iL, iR, iA = nomes.index('L1'), nomes.index('R1'), nomes.index('A1')
    r = {}
    for nome in ('L2', 'R2', 'BN2', 'A2'):
        r[nome] = rec.ajusta(Y[nome])
    out = {'secoes': rec.secoes, 'n': rec.N, 'locais': rec.G, 'vazio': False}

    def par(eq, j):
        return [float(r[eq][0][j]), float(r[eq][1][j])]
    out['V'] = par('L2', iR)
    out['M'] = par('R2', iL)
    out['retF'], out['retL'] = par('R2', iR), par('L2', iL)
    out['aF'], out['aL'] = par('A2', iR), par('A2', iL)
    out['bnF'], out['bnL'] = par('BN2', iR), par('BN2', iL)
    out['A1_para_L'], out['A1_para_F'], out['A1_fica'] = par('L2', iA), par('R2', iA), par('A2', iA)
    out['soma_linha_R1'] = float(sum(r[q][0][iR] for q in r))
    out['soma_linha_L1'] = float(sum(r[q][0][iL] for q in r))
    d = out['V'][0] - out['M'][0]
    ep = ep_conjunto([(rec, r['L2'][2][iR], 1.0), (rec, r['R2'][2][iL], -1.0)], nloc)
    out['D_dentro'] = [float(d), ep]
    da = out['aF'][0] - out['aL'][0]
    epa = ep_conjunto([(rec, r['A2'][2][iR], 1.0), (rec, r['A2'][2][iL], -1.0)], nloc)
    out['nao_voltou_F_menos_L'] = [float(da), epa]
    df = out['A1_para_L'][0] - out['A1_para_F'][0]
    epf = ep_conjunto([(rec, r['L2'][2][iA], 1.0), (rec, r['R2'][2][iA], -1.0)], nloc)
    out['A1_L_menos_F'] = [float(df), epf]
    out['coef_L2'] = {n: [float(r['L2'][0][j]), float(r['L2'][1][j])] for j, n in enumerate(nomes)}
    out['coef_R2'] = {n: [float(r['R2'][0][j]), float(r['R2'][1][j])] for j, n in enumerate(nomes)}
    return out


def estat(recV, recM, L2, R2, iL, iR, nloc, munloc=None):
    """Estatística do registro: D = V(recorte de Flávio fraco) - M(recorte de Lula fraco), com erro conjunto."""
    bV, eV, pV = recV.ajusta(L2, js=[iR])
    bM, eM, pM = recM.ajusta(R2, js=[iL])
    V, M = float(bV[iR]), float(bM[iL])
    D = V - M
    ep = ep_conjunto([(recV, pV[iR], 1.0), (recM, pM[iL], -1.0)], nloc)
    o = {'V': V, 'epV': eV[iR], 'M': M, 'epM': eM[iL], 'D': D, 'ep': ep,
         'ep_independente': float(np.hypot(eV[iR], eM[iL])),
         'D_sobre_ep': D / ep, 'D_menos_limiar_sobre_ep': (D - 0.02) / ep, 'D_mais_2ep': D + 2 * ep,
         'sinal': bool(D >= 0.02 and D / ep > 4), 'sem_sinal_numerico': bool(D + 2 * ep < 0.01),
         'sinal_espelho': bool(-D >= 0.02 and -D / ep > 4)}
    if munloc is not None:
        epm = ep_conjunto([(recV, pV[iR], 1.0), (recM, pM[iL], -1.0)], int(munloc.max()) + 1, mapa=munloc)
        o['ep_por_municipio'] = epm
        o['sinal_ep_municipio'] = bool(D >= 0.02 and D / epm > 4)
        o['sem_sinal_numerico_ep_municipio'] = bool(D + 2 * epm < 0.01)
    return o


# ------------------------------------------------------------------ plantio
def resolver_k(base, w, total):
    """k tal que a soma de base x min(1, k w) seja o total."""
    base = np.asarray(base, float)
    w = np.nan_to_num(np.asarray(w, float))
    teto = float(base[w > 0].sum())
    if teto < total:
        raise ValueError('a regra não comporta o total: teto %.0f' % teto)
    f = lambda k: float((base * np.minimum(1.0, k * w)).sum())
    lo, hi = 0.0, total / float((base * w).sum())
    while f(hi) < total:
        hi *= 2
    for _ in range(100):
        mid = 0.5 * (lo + hi)
        if f(mid) < total:
            lo = mid
        else:
            hi = mid
    k = 0.5 * (lo + hi)
    return k, np.minimum(1.0, k * w)


def pesos_regra(B, fat, regra):
    fLs, fLl, fFs = np.nan_to_num(fat['fLs']), np.nan_to_num(fat['fLl']), np.nan_to_num(fat['fFs'])
    if regra == 'C1':
        return fLs
    if regra == 'C1L':
        return fLl
    if regra == 'C2':
        return (fLs >= 0.5).astype(float)
    if regra == 'C3':
        return fLs ** 2
    if regra == 'C4':
        return B['L2'] / np.maximum(B['R2'], 1).astype(float)
    if regra == 'C5':
        return np.isin(B['uf'], NORDESTE).astype(float)
    if regra == 'U':
        return np.ones(len(fLs))
    if regra == 'E':
        return fFs
    raise ValueError(regra)


class Plantio:
    """Guarda as taxas por seção de cada cenário e devolve L2, R2 e A2 modificados (sorteio ou valor esperado)."""

    def __init__(self, B, fat, Y):
        self.B, self.fat, self.Y = B, fat, Y
        self.R2i, self.L2i = B['R2'].astype(np.int64), B['L2'].astype(np.int64)
        self.A2i = np.maximum(B['apt2'] - B['comp2'], 0).astype(np.int64)
        self.p, self.k = {}, {}
        for regra in ('C1', 'C1L', 'C2', 'C3', 'C4', 'C5', 'U'):
            self.k[regra], self.p[regra] = resolver_k(self.R2i, pesos_regra(B, fat, regra), TOTAL)
        self.k['E'], self.p['E'] = resolver_k(self.L2i, pesos_regra(B, fat, 'E'), TOTAL)
        self.k['ENT'], self.p['ENT'] = resolver_k(self.A2i, pesos_regra(B, fat, 'C1'), TOTAL)
        self.p['I2'] = np.full(len(self.R2i), 0.036)

    def _tira(self, base, p, rng, dose=1.0):
        if rng is None:
            return base * p * dose
        return rng.binomial(base, np.minimum(1.0, p * dose)).astype(float)

    def gera(self, cen, rng=None, dose=1.0):
        """Devolve (L2, R2, A2, info). cen: 'P_<regra>', 'I1', 'I2', 'I3', 'I4', 'E2', 'S1'."""
        L2, R2, A2 = self.Y['L2'].copy(), self.Y['R2'].copy(), self.Y['A2'].copy()
        info = {}
        if cen.startswith('P_'):
            d = self._tira(self.R2i, self.p[cen[2:]], rng, dose)
            L2 += d; R2 -= d
            info['troca'] = d
        elif cen == 'I1':
            a = self._tira(self.R2i, self.p['C1'], rng, dose)
            R2 -= a; A2 += a
            info['abst'] = a
        elif cen == 'I2':
            a = self._tira(self.R2i, self.p['I2'], rng, dose)
            R2 -= a; A2 += a
            info['abst'] = a
        elif cen == 'I3':
            e = self._tira(self.A2i, self.p['ENT'], rng, dose)
            L2 += e; A2 -= e
            info['entrada'] = e
        elif cen == 'I4':
            a = self._tira(self.R2i, self.p['C1'], rng, dose)
            e = self._tira(self.A2i, self.p['ENT'], rng, dose)
            R2 -= a; A2 += a; L2 += e; A2 -= e
            info['abst'], info['entrada'] = a, e
        elif cen == 'E2':
            d = self._tira(self.L2i, self.p['E'], rng, dose)
            L2 -= d; R2 += d
            info['troca_espelho'] = d
        elif cen == 'S1':
            d = self._tira(self.R2i, self.p['C1'], rng, dose)
            e = self._tira(self.A2i, self.p['ENT'], rng, dose)
            L2 += d; R2 -= d; L2 += e; A2 -= e
            info['troca'], info['entrada'] = d, e
        else:
            raise ValueError(cen)
        return L2, R2, A2, info


CENARIOS = {
    'P_C1': ('troca concentrada, regra C1 (a do registro): taxa proporcional à fatia de Lula na seção', NSORT),
    'P_C1L': ('troca concentrada, regra C1L: taxa proporcional à fatia de Lula no local', NSORT_LADO),
    'P_C2': ('troca concentrada, regra C2: só onde Lula teve 50% ou mais na seção, taxa uniforme', NSORT_LADO),
    'P_C3': ('troca concentrada, regra C3: taxa proporcional ao quadrado da fatia de Lula', NSORT_LADO),
    'P_C4': ('troca na forma k x L: votos trocados proporcionais aos votos de Lula no 2º turno', NSORT_LADO),
    'P_C5': ('troca só nas nove UFs do Nordeste, taxa uniforme', NSORT_LADO),
    'P_U': ('troca uniforme do mesmo total (referência)', NSORT_LADO),
    'I1': ('abstenção pura concentrada (regra C1), sem voto para Lula', NSORT),
    'I2': ('abstenção pura uniforme de 3,6% dos votos de Flávio', NSORT),
    'I3': ('entrada de eleitores reais concentrada (faltosos do 2º turno viram voto em Lula)', NSORT),
    'I4': ('I1 e I3 juntas: virada pelo comparecimento, sem troca', NSORT),
    'E2': ('plantio espelho: de Lula para Flávio, taxa proporcional à fatia de Flávio na seção', NSORT),
    'S1': ('estresse: troca C1 mais entrada I3 juntas', NSORT),
}


def resumo_sorteios(lista):
    """lista de dicionários estat. Média, desvio e frequência do critério."""
    o = {'sorteios': len(lista)}
    for q in ('V', 'M', 'D', 'ep', 'D_sobre_ep', 'D_mais_2ep'):
        v = np.array([x[q] for x in lista], float)
        o[q + '_media'] = float(v.mean())
        o[q + '_dp'] = float(v.std(ddof=1)) if len(v) > 1 else 0.0
    o['D_min'], o['D_max'] = float(min(x['D'] for x in lista)), float(max(x['D'] for x in lista))
    o['sinal_freq'] = float(np.mean([x['sinal'] for x in lista]))
    o['sinal_espelho_freq'] = float(np.mean([x['sinal_espelho'] for x in lista]))
    o['sem_sinal_numerico_freq'] = float(np.mean([x['sem_sinal_numerico'] for x in lista]))
    return o


def veredito_letra(obs, detectada):
    if obs['sinal']:
        return 'SINAL'
    if not detectada:
        return 'SEM PODER'
    if obs['sem_sinal_numerico']:
        return 'SEM SINAL'
    return 'INCONCLUSIVO'


# ------------------------------------------------------------------ partes
def conferir_base(B):
    o = {'secoes_dois_turnos': int(len(B['L1'])), 'L2': int(B['L2'].sum()), 'R2': int(B['R2'].sum()),
         'margem': int(B['L2'].sum() - B['R2'].sum()), 'L1': int(B['L1'].sum()), 'R1': int(B['R1'].sum()),
         'O1': int(B['O1'].sum()), 'comp1': int(B['comp1'].sum()), 'comp2': int(B['comp2'].sum()),
         'apt1': int(B['apt1'].sum()), 'apt2': int(B['apt2'].sum()),
         'aumento_comparecimento': int(B['comp2'].sum() - B['comp1'].sum()),
         'identidade_1t_erro_max': int(np.abs(B['L1'] + B['R1'] + B['O1'] + B['B1'] + B['N1'] - B['comp1']).max()),
         'identidade_2t_erro_max': int(np.abs(B['L2'] + B['R2'] + B['O2'] + B['B2'] + B['N2'] - B['comp2']).max()),
         'O2_total': int(B['O2'].sum()), 'locais': int(B['loc'].max()) + 1, 'municipios': int(B['mun'].max()) + 1,
         'bate_oficial': bool(B['L2'].sum() == L2_OFICIAL and B['R2'].sum() == F2_OFICIAL)}
    return o


def conferir_estimador(B, X, nomes, Y, U):
    """Uma vez: meu estimador contra lib.fe_ols (equação de L2 no universo principal)."""
    sys.path.insert(0, RAIZ + '/scripts')
    from lib import fe_ols
    rec = Recorte(X, B['loc'], U)
    b, ep, _ = rec.ajusta(Y['L2'])
    r = fe_ols(Y['L2'][U], X[U], B['loc'][U], nomes=nomes)
    return {'n_meu': rec.N, 'n_lib': r['n'], 'grupos_meu': rec.G, 'grupos_lib': r['grupos'],
            'dif_max_coef': float(max(abs(b[j] - r['coef'][n]) for j, n in enumerate(nomes))),
            'dif_max_ep': float(max(abs(ep[j] - r['ep'][n]) for j, n in enumerate(nomes)))}


def montar_leituras(B, X, U, fat, grupo=None, w=None):
    """Recortes das quatro faixas nas duas leituras. Devolve dict leitura -> {'V': [rec x4], 'M': [rec x4]}."""
    grupo = B['loc'] if grupo is None else grupo
    out = {}
    for nome, fF, fL in (('A_local', fat['fFl'], fat['fLl']), ('B_secao', fat['fFs'], fat['fLs'])):
        out[nome] = {'V': [Recorte(X, grupo, U & em_faixa(fF, i), w) for i in range(4)],
                     'M': [Recorte(X, grupo, U & em_faixa(fL, i), w) for i in range(4)],
                     'mV': [U & em_faixa(fF, i) for i in range(4)], 'mM': [U & em_faixa(fL, i) for i in range(4)],
                     'pais_V': [em_faixa(fF, i) for i in range(4)], 'pais_M': [em_faixa(fL, i) for i in range(4)]}
    return out


def perfil_faixas(B, lt, Y, nomes, nloc, munloc=None, completo=True):
    """D por faixa (as quatro), com a matriz inteira de cada recorte se completo."""
    iL, iR = nomes.index('L1'), nomes.index('R1')
    out = []
    for i in range(4):
        recV, recM = lt['V'][i], lt['M'][i]
        if recV.vazio or recM.vazio:
            out.append({'faixa': NOME_FAIXA[i], 'vazio': True})
            continue
        e = estat(recV, recM, Y['L2'], Y['R2'], iL, iR, nloc, munloc)
        e['faixa'] = NOME_FAIXA[i]
        e['lado_V'] = {'secoes': recV.secoes, 'n': recV.N, 'locais': recV.G,
                       'votos_F_1t_universo': int(B['R1'][lt['mV'][i]].sum()),
                       'votos_F_2t_universo': int(B['R2'][lt['mV'][i]].sum()),
                       'votos_F_1t_pais': int(B['R1'][lt['pais_V'][i]].sum()),
                       'votos_F_2t_pais': int(B['R2'][lt['pais_V'][i]].sum()),
                       'secoes_pais': int(lt['pais_V'][i].sum())}
        e['lado_M'] = {'secoes': recM.secoes, 'n': recM.N, 'locais': recM.G,
                       'votos_L_1t_universo': int(B['L1'][lt['mM'][i]].sum()),
                       'votos_L_2t_universo': int(B['L2'][lt['mM'][i]].sum()),
                       'votos_L_1t_pais': int(B['L1'][lt['pais_M'][i]].sum()),
                       'votos_L_2t_pais': int(B['L2'][lt['pais_M'][i]].sum()),
                       'secoes_pais': int(lt['pais_M'][i].sum())}
        e['locais_nos_dois_recortes'] = int(len(np.intersect1d(recV.gid, recM.gid)))
        if completo:
            e['matriz_lado_V'] = matriz(recV, Y, nomes, nloc)
            e['matriz_lado_M'] = matriz(recM, Y, nomes, nloc)
        out.append(e)
    return out


def rodar_cenario(cen, nsort, PL, leituras, nomes, nloc, obs, B, idc):
    """Valor esperado (perfil das quatro faixas, enxuto) e sorteios (só a faixa que decide) nas duas leituras."""
    iL, iR = nomes.index('L1'), nomes.index('R1')
    out = {'descricao': CENARIOS[cen][0], 'leituras': {}}
    L2, R2, A2, info = PL.gera(cen)
    out['total_esperado'] = {k: float(v.sum()) for k, v in info.items()}
    Ymod = {'L2': L2, 'R2': R2, 'A2': A2, 'BN2': PL.Y['BN2']}
    for nome, lt in leituras.items():
        pf = perfil_faixas(B, lt, Ymod, nomes, nloc, completo=False)
        for i, e in enumerate(pf):
            if e.get('vazio'):
                continue
            o = obs[nome][i]
            e['dV'], e['dM'], e['dD'] = e['V'] - o['V'], e['M'] - o['M'], e['D'] - o['D']
            e['D_com_M_fixo'] = e['V'] - o['M']
            for q in ('lado_V', 'lado_M'):
                e.pop(q, None)
            mV = lt['mV'][i]
            for k, v in info.items():
                base = B['L2'] if k == 'troca_espelho' else (np.maximum(B['apt2'] - B['comp2'], 0) if k == 'entrada' else B['R2'])
                e['taxa_%s_na_faixa_V' % k] = float(v[mV].sum() / max(base[mV].sum(), 1))
                e['votos_%s_na_faixa_V' % k] = float(v[mV].sum())
        m0 = matriz(lt['V'][0], Ymod, nomes, nloc)
        pf[0]['matriz_lado_V_resumo'] = {q: m0[q] for q in ('V', 'aF', 'retF', 'A1_para_L', 'A1_para_F')}
        out['leituras'][nome] = {'valor_esperado': pf}
    sor = {nome: [] for nome in leituras}
    tot = []
    for j in range(nsort):
        rng = np.random.default_rng([SEMENTE, idc, j])
        L2, R2, A2, info = PL.gera(cen, rng)
        tot.append({k: float(v.sum()) for k, v in info.items()})
        for nome, lt in leituras.items():
            sor[nome].append(estat(lt['V'][0], lt['M'][0], L2, R2, iL, iR, nloc))
    out['total_sorteado_media'] = {k: float(np.mean([t[k] for t in tot])) for k in tot[0]} if tot else {}
    for nome in leituras:
        rs = resumo_sorteios(sor[nome])
        o = obs[nome][0]
        rs['dV_media'], rs['dM_media'], rs['dD_media'] = rs['V_media'] - o['V'], rs['M_media'] - o['M'], rs['D_media'] - o['D']
        rs['D_subiu_0.02_freq'] = float(np.mean([x['D'] - o['D'] >= 0.02 for x in sor[nome]]))
        rs['V_subiu_0.02_freq'] = float(np.mean([x['V'] - o['V'] >= 0.02 for x in sor[nome]]))
        rs['sinal_com_M_fixo_freq'] = float(np.mean([(x['V'] - o['M'] >= 0.02) and ((x['V'] - o['M']) / x['ep'] > 4)
                                                      for x in sor[nome]]))
        out['leituras'][nome]['sorteios'] = rs
    return out


def doses(PL, leituras, nomes, nloc, obs):
    iL, iR = nomes.index('L1'), nomes.index('R1')
    out = {nome: [] for nome in leituras}
    for dose in (0.10, 0.25, 0.50, 0.75, 1.00, 1.25):
        L2, R2, A2, info = PL.gera('P_C1', None, dose)
        for nome, lt in leituras.items():
            e = estat(lt['V'][0], lt['M'][0], L2, R2, iL, iR, nloc)
            o = obs[nome][0]
            out[nome].append({'dose': dose, 'votos': float(info['troca'].sum()), 'V': e['V'], 'M': e['M'], 'D': e['D'],
                              'ep': e['ep'], 'dV': e['V'] - o['V'], 'dM': e['M'] - o['M'], 'dD': e['D'] - o['D'],
                              'sinal': e['sinal'], 'D_sobre_ep': e['D_sobre_ep']})
    for nome in out:
        lst = out[nome]
        x = np.array([q['votos'] for q in lst]); y = np.array([q['dD'] for q in lst]); yv = np.array([q['dV'] for q in lst])
        incl = float((x @ y) / (x @ x)); inclv = float((x @ yv) / (x @ x))
        det = [q['votos'] for q in lst if q['sinal']]
        out[nome] = {'pontos': lst, 'dD_por_voto': incl, 'dV_por_voto': inclv,
                     'dD_por_2136651': incl * TOTAL, 'dV_por_2136651': inclv * TOTAL,
                     'menor_dose_que_dispara': (min(det) if det else None)}
    return out


def variantes(B, Y, fat, PL, nloc):
    """Ao lado: outros universos e especificações. Bruto e forma C1 pelo valor esperado, nas duas leituras."""
    out = {}
    U0 = (B['apt1'] == B['apt2']) & (B['apt1'] > 0)
    ext = B['uf'] == 'ZZ'
    munloc = np.zeros(nloc, np.int64)
    munloc[B['loc']] = B['mun']
    Lp, Rp, Ap, _ = PL.gera('P_C1')
    Yp = {'L2': Lp, 'R2': Rp, 'A2': Ap, 'BN2': Y['BN2']}
    esp = [
        ('sem_exterior', 'universo principal sem o exterior', 'grupos', U0 & ~ext, None, 'loc'),
        ('todas_as_secoes', 'todas as seções com os dois turnos (aptos podem diferir)', 'grupos', B['apt1'] > 0, None, 'loc'),
        ('desenho_D4_1', 'universo do D4-1: aptos a até 2, comparecimento 1T de 30 ou mais, sem exterior, peso 1/aptos',
         'grupos', (np.abs(B['apt1'] - B['apt2']) <= 2) & (B['comp1'] >= 30) & ~ext & (B['apt1'] > 0),
         1.0 / np.maximum(B['apt1'], 1), 'loc'),
        ('outros_agregados', 'outros candidatos num termo só', 'agregado', U0, None, 'loc'),
        ('bn_separados', 'branco e nulo do 1º turno em termos separados', 'bn_separados', U0, None, 'loc'),
        ('efeito_fixo_municipio', 'efeito fixo e erro por município em vez de local', 'grupos', U0, None, 'mun'),
        ('peso_aptos', 'universo principal com peso igual aos aptos', 'grupos', U0, B['apt1'].astype(float), 'loc'),
    ]
    for chave, desc, modo, U, w, grp in esp:
        X, nomes = regressoras(B, modo)
        iL, iR = nomes.index('L1'), nomes.index('R1')
        grupo = B['loc'] if grp == 'loc' else B['mun']
        ncl = nloc if grp == 'loc' else int(B['mun'].max()) + 1
        lts = montar_leituras(B, X, U, fat, grupo, w)
        o = {'descricao': desc, 'secoes_universo': int(U.sum())}
        for nome, lt in lts.items():
            ml = munloc if grp == 'loc' else None
            e = estat(lt['V'][0], lt['M'][0], Y['L2'], Y['R2'], iL, iR, ncl, ml)
            ep_ = estat(lt['V'][0], lt['M'][0], Yp['L2'], Yp['R2'], iL, iR, ncl, ml)
            e['nV'], e['nM'] = lt['V'][0].N, lt['M'][0].N
            e['com_C1'] = {q: ep_[q] for q in ('V', 'M', 'D', 'ep', 'D_sobre_ep', 'sinal')}
            e['com_C1']['dD'] = ep_['D'] - e['D']
            if 'ep_por_municipio' in ep_:
                e['com_C1']['sinal_ep_municipio'] = ep_['sinal_ep_municipio']
            e['veredito'] = veredito_letra(e, ep_['sinal'])
            if 'ep_por_municipio' in e:
                em = dict(e); em['sinal'] = e['sinal_ep_municipio']; em['sem_sinal_numerico'] = e['sem_sinal_numerico_ep_municipio']
                e['veredito_ep_municipio'] = veredito_letra(em, ep_['sinal_ep_municipio'])
            o[nome] = e
        out[chave] = o
        log('variante', chave)
    return out


def outros_anos(nloc26):
    """Ao lado, não é régua: a mesma estatística com outros agregados em 2014, 2018, 2022 e 2026."""
    out = {}
    for ano in (2014, 2018, 2022, 2026):
        B = montar_base(ano)
        X, nomes = regressoras(B, 'agregado')
        iL, iR = nomes.index('L1'), nomes.index('R1')
        Y = respostas(B)
        U = (B['apt1'] == B['apt2']) & (B['apt1'] > 0)
        fat = fatias(B)
        nloc = int(B['loc'].max()) + 1
        lts = montar_leituras(B, X, U, fat)
        o = {'secoes_dois_turnos': int(len(B['L1'])), 'secoes_universo': int(U.sum())}
        for nome, lt in lts.items():
            pf = []
            for i in range(4):
                if lt['V'][i].vazio or lt['M'][i].vazio:
                    pf.append({'faixa': NOME_FAIXA[i], 'vazio': True}); continue
                e = estat(lt['V'][i], lt['M'][i], Y['L2'], Y['R2'], iL, iR, nloc)
                e['faixa'] = NOME_FAIXA[i]; e['nV'], e['nM'] = lt['V'][i].N, lt['M'][i].N
                pf.append(e)
            o[nome] = pf
        rec = Recorte(X, B['loc'], U)
        o['universo'] = {q: v for q, v in matriz(rec, Y, nomes, nloc).items()
                         if q in ('V', 'M', 'D_dentro', 'aF', 'aL', 'nao_voltou_F_menos_L', 'A1_para_L', 'A1_para_F', 'n', 'locais')}
        out[str(ano)] = o
        log('ano', ano)
        del B
    return out


def por_uf(B, X, nomes, Y, U, fat, PL, nloc, leitA):
    """Descritivo: a matriz inteira dentro de cada UF, com a diferença entre os dois sentidos."""
    iL, iR = nomes.index('L1'), nomes.index('R1')
    Lp, Rp, Ap, info = PL.gera('P_C1')
    Yp = {'L2': Lp, 'R2': Rp, 'A2': Ap, 'BN2': Y['BN2']}
    Lu, Ru, Au, infou = PL.gera('P_U')
    Yu = {'L2': Lu, 'R2': Ru, 'A2': Au, 'BN2': Y['BN2']}
    ufs = sorted(set(B['uf'].tolist()))
    out = {}
    for uf in ufs:
        m = U & (B['uf'] == uf)
        rec = Recorte(X, B['loc'], m)
        mt = matriz(rec, Y, nomes, nloc)
        if mt.get('vazio'):
            out[uf] = mt; continue
        mt.pop('coef_L2', None); mt.pop('coef_R2', None)
        mp = matriz(rec, Yp, nomes, nloc)
        mu = matriz(rec, Yu, nomes, nloc)
        mt['com_C1'] = {'V': mp['V'], 'M': mp['M'], 'D_dentro': mp['D_dentro'],
                        'taxa_plantada': float(info['troca'][m].sum() / max(B['R2'][m].sum(), 1)),
                        'votos_plantados': float(info['troca'][m].sum())}
        mt['com_U'] = {'V': mu['V'], 'M': mu['M'], 'D_dentro': mu['D_dentro']}
        mt['votos_F_1t'], mt['votos_L_1t'] = int(B['R1'][m].sum()), int(B['L1'][m].sum())
        mt['votos_F_2t'], mt['votos_L_2t'] = int(B['R2'][m].sum()), int(B['L2'][m].sum())
        mt['faltosos_1t'] = int((B['apt1'] - B['comp1'])[m].sum())
        mt['fatia_L_1t'] = float(B['L1'][m].sum() / max(fat['val'][m].sum(), 1))
        # dentro da faixa de menos de 35% (Leitura A), onde houver 30 locais ou mais de cada lado
        rV = Recorte(X, B['loc'], m & em_faixa(fat['fFl'], 0))
        rM = Recorte(X, B['loc'], m & em_faixa(fat['fLl'], 0))
        fx = {'locais_V': rV.G, 'locais_M': rM.G, 'nV': rV.N, 'nM': rM.N}
        if not rV.vazio and rV.G >= 30:
            b, ep, _ = rV.ajusta(Y['L2'], js=[iR]); fx['V'] = [float(b[iR]), ep[iR]]
        if not rM.vazio and rM.G >= 30:
            b, ep, _ = rM.ajusta(Y['R2'], js=[iL]); fx['M'] = [float(b[iL]), ep[iL]]
        if 'V' in fx and 'M' in fx:
            e = estat(rV, rM, Y['L2'], Y['R2'], iL, iR, nloc)
            fx['D'] = [e['D'], e['ep']]
        mt['faixa_menos_35_leitura_A'] = fx
        out[uf] = mt
    # homogeneidade entre as 27 UFs (sem o exterior)
    lst = [(uf, o['D_dentro'][0], o['D_dentro'][1]) for uf, o in out.items() if uf != 'ZZ' and not o.get('vazio')]
    d = np.array([x[1] for x in lst]); e = np.array([x[2] for x in lst])
    w = 1 / e ** 2
    mbar = float((w * d).sum() / w.sum())
    qui = float((w * (d - mbar) ** 2).sum())
    dp_ = np.array([out[x[0]]['com_C1']['D_dentro'][0] for x in lst])
    du_ = np.array([out[x[0]]['com_U']['D_dentro'][0] for x in lst])
    wv = np.array([out[x[0]]['votos_F_1t'] for x in lst], float)
    res = {'n_ufs': len(lst), 'media_ponderada_inv_var': mbar, 'ep_media': float(np.sqrt(1 / w.sum())),
           'media_ponderada_votos_F': float((wv * d).sum() / wv.sum()), 'media_simples': float(d.mean()),
           'dp_entre_ufs': float(d.std(ddof=1)), 'qui2_homogeneidade': qui, 'gl': len(lst) - 1,
           'min': [lst[int(d.argmin())][0], float(d.min())], 'max': [lst[int(d.argmax())][0], float(d.max())],
           'ufs_acima_de_+0.010': sorted([x[0] for x in lst if x[1] > 0.010]),
           'ufs_abaixo_de_-0.010': sorted([x[0] for x in lst if x[1] < -0.010]),
           'ufs_acima_de_+0.010_a_2ep': sorted([x[0] for x in lst if x[1] - 2 * x[2] > 0.010]),
           'ufs_abaixo_de_-0.010_a_2ep': sorted([x[0] for x in lst if x[1] + 2 * x[2] < -0.010]),
           'ufs_positivas_a_2ep': sorted([x[0] for x in lst if x[1] - 2 * x[2] > 0]),
           'ufs_negativas_a_2ep': sorted([x[0] for x in lst if x[1] + 2 * x[2] < 0]),
           'com_C1_subida_media': float((dp_ - d).mean()), 'com_C1_subida_min': float((dp_ - d).min()),
           'com_C1_subida_max': float((dp_ - d).max()), 'com_C1_dp_entre_ufs': float(dp_.std(ddof=1)),
           'com_U_subida_media': float((du_ - d).mean()), 'com_U_subida_min': float((du_ - d).min()),
           'com_U_subida_max': float((du_ - d).max())}
    # correlação de D com a força de Lula na UF (uma troca regulada pela força de Lula daria D crescente)
    fl = np.array([out[x[0]]['fatia_L_1t'] for x in lst])
    res['correlacao_D_com_fatia_de_Lula'] = float(np.corrcoef(d, fl)[0, 1])
    res['correlacao_D_com_C1_com_fatia_de_Lula'] = float(np.corrcoef(dp_, fl)[0, 1])
    sl = np.polyfit(fl, d, 1, w=1 / e)
    res['inclinacao_D_por_fatia_de_Lula'] = float(sl[0])
    slp = np.polyfit(fl, dp_ - d, 1)
    res['inclinacao_da_subida_com_C1_por_fatia_de_Lula'] = float(slp[0])
    return {'ufs': out, 'resumo': res}


def traducao(obsA, obsB, dos):
    out = {}
    for nome, obs in (('A_local', obsA), ('B_secao', obsB)):
        o = obs[0]
        vF = o['lado_V']['votos_F_1t_pais']
        t = {'votos_F_1t_na_faixa_pais': vF, 'votos_F_2t_na_faixa_pais': o['lado_V']['votos_F_2t_pais']}
        t['direta_votos'] = o['D'] * vF
        t['direta_margem'] = 2 * o['D'] * vF
        t['direta_pct_da_margem'] = 100 * 2 * o['D'] * vF / MARGEM
        t['direta_teto_votos'] = max(0.0, o['D_mais_2ep']) * vF
        t['direta_teto_margem'] = 2 * max(0.0, o['D_mais_2ep']) * vF
        t['direta_teto_pct_da_margem'] = 100 * 2 * max(0.0, o['D_mais_2ep']) * vF / MARGEM
        t['so_V_votos'] = o['V'] * vF
        t['so_V_teto_votos'] = (o['V'] + 2 * o['epV']) * vF
        t['so_V_teto_pct_da_margem'] = 100 * 2 * (o['V'] + 2 * o['epV']) * vF / MARGEM
        dD, dV = dos[nome]['dD_por_2136651'], dos[nome]['dV_por_2136651']
        t['calibracao_dD_por_2136651'] = dD
        t['calibracao_dV_por_2136651'] = dV
        t['forma_C1_maximo_votos_premissa_espelho'] = max(0.0, o['D_mais_2ep']) / dD * TOTAL if dD > 0 else None
        t['forma_C1_ponto_votos_premissa_espelho'] = o['D'] / dD * TOTAL if dD > 0 else None
        t['forma_C1_maximo_votos_premissa_extrema'] = max(0.0, o['V'] + 2 * o['epV']) / dV * TOTAL if dV > 0 else None
        for q in ('forma_C1_maximo_votos_premissa_espelho', 'forma_C1_ponto_votos_premissa_espelho',
                  'forma_C1_maximo_votos_premissa_extrema'):
            if t[q] is not None:
                t[q + '_pct_da_margem'] = 100 * 2 * t[q] / MARGEM
        out[nome] = t
    out['referencia'] = {'margem_oficial': MARGEM, 'forma_plantada_votos': TOTAL, 'forma_plantada_margem': 2 * TOTAL,
                         'forma_plantada_pct_da_margem': 100 * 2 * TOTAL / MARGEM, 'vira_com_votos_trocados': 2215096}
    return out


def rodar():
    os.makedirs(TRAB, exist_ok=True)
    R = {'teste': 'R27_N3', 'registro': 'Adendo 28, N3 (commit 938be19, 10/11/2026 04:36:33 UTC)',
         'iniciado_em': agora(), 'total_plantado': TOTAL, 'semente': SEMENTE,
         'docstring_sha256': hashlib.sha256(__doc__.encode()).hexdigest()}
    B = montar_base(2026)
    R['base'] = conferir_base(B)
    log('base', R['base'])
    X, nomes = regressoras(B, 'grupos')
    iL, iR = nomes.index('L1'), nomes.index('R1')
    Y = respostas(B)
    U = (B['apt1'] == B['apt2']) & (B['apt1'] > 0)
    fat = fatias(B)
    nloc = int(B['loc'].max()) + 1
    munloc = np.zeros(nloc, np.int64)
    munloc[B['loc']] = B['mun']
    R['universo'] = {'secoes': int(U.sum()), 'fora_por_aptos': int((~U).sum()), 'exterior_no_universo': int((U & (B['uf'] == 'ZZ')).sum()),
                     'votos_F_2t': int(B['R2'][U].sum()), 'votos_L_2t': int(B['L2'][U].sum()),
                     'margem_no_universo': int(B['L2'][U].sum() - B['R2'][U].sum()),
                     'votos_F_1t': int(B['R1'][U].sum()), 'votos_L_1t': int(B['L1'][U].sum())}
    R['conferencia_estimador'] = conferir_estimador(B, X, nomes, Y, U)
    log('estimador', R['conferencia_estimador'])
    gravar('parcial_base.json', R)

    # --- matriz no universo inteiro (referência) e por faixa nas duas leituras, dados brutos
    recU = Recorte(X, B['loc'], U)
    R['matriz_universo'] = matriz(recU, Y, nomes, nloc)
    leituras = montar_leituras(B, X, U, fat)
    obs = {nome: perfil_faixas(B, lt, Y, nomes, nloc, munloc) for nome, lt in leituras.items()}
    R['observado'] = obs
    for nome in obs:
        o = obs[nome][0]
        log('bruto', nome, 'V %.4f (%.4f) M %.4f (%.4f) D %.4f (%.4f) D+2ep %.4f' % (o['V'], o['epV'], o['M'], o['epM'], o['D'], o['ep'], o['D_mais_2ep']))
    gravar('parcial_observado.json', R)

    # --- plantios
    PL = Plantio(B, fat, Y)
    R['plantio_regras'] = {r: {'k': float(PL.k[r]), 'taxa_media_ponderada': float((PL.p[r] * (PL.L2i if r == 'E' else (PL.A2i if r == 'ENT' else PL.R2i))).sum()
                                                                                / max((PL.L2i if r == 'E' else (PL.A2i if r == 'ENT' else PL.R2i)).sum(), 1)),
                               'taxa_max': float(PL.p[r].max()), 'secoes_com_taxa_1': int((PL.p[r] >= 1).sum())}
                           for r in PL.k}
    R['doses_C1'] = doses(PL, leituras, nomes, nloc, obs)
    R['cenarios'] = {}
    for idc, (cen, (desc, ns)) in enumerate(CENARIOS.items()):
        R['cenarios'][cen] = rodar_cenario(cen, ns, PL, leituras, nomes, nloc, obs, B, idc)
        s = R['cenarios'][cen]['leituras']['A_local']['sorteios']
        log('cenário', cen, 'A: D %.4f (dp %.4f) sinal %.2f espelho %.2f' % (s['D_media'], s['D_dp'], s['sinal_freq'], s['sinal_espelho_freq']))
        gravar('parcial_cenarios.json', R)

    # --- vereditos pela letra
    R['veredito'] = {}
    for nome in leituras:
        o = obs[nome][0]
        c1 = R['cenarios']['P_C1']['leituras'][nome]
        det = bool(c1['valor_esperado'][0]['sinal'] and c1['sorteios']['sinal_freq'] >= 0.95)
        det_frouxa = bool(c1['valor_esperado'][0]['dD'] >= 0.02 and c1['sorteios']['D_subiu_0.02_freq'] >= 0.95)
        om = dict(o); om['sinal'] = o['sinal_ep_municipio']; om['sem_sinal_numerico'] = o['sem_sinal_numerico_ep_municipio']
        esp = R['cenarios']
        distingue = {c: esp[c]['leituras'][nome]['sorteios']['sinal_freq'] for c in ('I1', 'I2', 'I3', 'I4')}
        R['veredito'][nome] = {
            'D': o['D'], 'ep': o['ep'], 'D_sobre_ep': o['D_sobre_ep'], 'D_mais_2ep': o['D_mais_2ep'],
            'sinal': o['sinal'], 'sem_sinal_numerico': o['sem_sinal_numerico'], 'sinal_espelho': o['sinal_espelho'],
            'forma_detectada': det, 'forma_detectada_leitura_frouxa': det_frouxa,
            'veredito_pela_letra': veredito_letra(o, det),
            'veredito_com_detectada_frouxa': veredito_letra(o, det_frouxa),
            'veredito_com_erro_por_municipio': veredito_letra(om, det),
            'criterio_dispara_com_explicacao_do_comparecimento_freq': distingue,
            'distingue_troca_de_comparecimento': bool(det and all(v <= 0.05 for v in distingue.values())),
            'espelho_plantado_dispara_invertido_freq': esp['E2']['leituras'][nome]['sorteios']['sinal_espelho_freq'],
            'espelho_plantado_dispara_direto_freq': esp['E2']['leituras'][nome]['sorteios']['sinal_freq'],
            'estresse_troca_mais_entrada_dispara_freq': esp['S1']['leituras'][nome]['sorteios']['sinal_freq']}
        log('veredito', nome, R['veredito'][nome]['veredito_pela_letra'])
    gravar('parcial_veredito.json', R)

    # --- ao lado
    R['variantes'] = variantes(B, Y, fat, PL, nloc)
    gravar('parcial_variantes.json', R)
    R['por_uf'] = por_uf(B, X, nomes, Y, U, fat, PL, nloc, leituras['A_local'])
    log('por UF', R['por_uf']['resumo'])
    gravar('parcial_uf.json', R)
    R['traducao_em_votos'] = traducao(obs['A_local'], obs['B_secao'], R['doses_C1'])
    R['exploratorio'] = exploratorio_tudo(B, X, nomes, Y, U, fat, PL, nloc, leituras, obs, R)
    gravar('parcial_exploratorio.json', R['exploratorio'])
    del B, X, Y
    R['outros_anos_nao_e_regua'] = outros_anos(nloc)
    R['exploratorio']['E2_outros_anos_nao_e_regua'] = exploratorio_depois(R)
    R['terminado_em'] = agora()
    gravar('resultado_completo.json', R)
    with open(SAIDA_JSON, 'w') as f:
        json.dump(limpa(R), f, ensure_ascii=False, indent=1)
    escrever_texto(limpa(R))
    log('fim')


# ------------------------------------------------------------------ EXPLORATÓRIO (feito depois de ver os resultados)
def exploratorio_contraste(lt, L2, R2, iL, iR, ncl):
    """D da faixa de menos de 35% menos D da faixa de 65% ou mais, com erro conjunto (os recortes se sobrepõem)."""
    pecas = [(lt['V'][0], L2, iR, 1.0), (lt['M'][0], R2, iL, -1.0), (lt['V'][3], L2, iR, -1.0), (lt['M'][3], R2, iL, 1.0)]
    if any(p[0].vazio for p in pecas):
        return None
    val, partes = 0.0, []
    for rec, y, j, s in pecas:
        b, ep, psi = rec.ajusta(y, js=[j])
        val += s * float(b[j])
        partes.append((rec, psi[j], s))
    return [val, ep_conjunto(partes, ncl)]


def exploratorio_ef_municipio(B, X, nomes, Y, U, fat, PL):
    """A variante com efeito fixo de município disparou. Aqui: as quatro faixas, o que cada plantio faz nela e a
    matriz do universo, para saber o que essa variante mede."""
    iL, iR = nomes.index('L1'), nomes.index('R1')
    nmun = int(B['mun'].max()) + 1
    ltm = montar_leituras(B, X, U, fat, B['mun'])
    out = {}
    for nome, lt in ltm.items():
        pf = []
        for i in range(4):
            e = estat(lt['V'][i], lt['M'][i], Y['L2'], Y['R2'], iL, iR, nmun)
            e['faixa'] = NOME_FAIXA[i]
            e['nV'], e['nM'], e['municipios_V'], e['municipios_M'] = lt['V'][i].N, lt['M'][i].N, lt['V'][i].G, lt['M'][i].G
            pf.append(e)
        cen = {}
        for c in ('P_C1', 'P_U', 'P_C4', 'I1', 'I3', 'I4', 'E2'):
            L2, R2, A2, info = PL.gera(c)
            x = estat(lt['V'][0], lt['M'][0], L2, R2, iL, iR, nmun)
            cen[c] = {q: x[q] for q in ('V', 'M', 'D', 'ep', 'sinal', 'sinal_espelho')}
            cen[c]['dV'], cen[c]['dM'], cen[c]['dD'] = x['V'] - pf[0]['V'], x['M'] - pf[0]['M'], x['D'] - pf[0]['D']
        out[nome] = {'faixas': pf, 'cenarios': cen,
                     'contraste_menos35_menos_65mais': exploratorio_contraste(lt, Y['L2'], Y['R2'], iL, iR, nmun)}
    rec = Recorte(X, B['mun'], U)
    mt = matriz(rec, Y, nomes, nmun)
    out['universo'] = {q: mt[q] for q in ('V', 'M', 'D_dentro', 'aF', 'aL', 'retF', 'retL', 'A1_para_L', 'A1_para_F', 'n', 'locais')}
    return out


def exploratorio_outros_anos():
    """Não é régua. A mesma estatística em 2014, 2018, 2022 e 2026 (outros agregados), com efeito fixo de local e
    de município, e o contraste entre as faixas extremas. Serve para saber se o instrumento tem zero estável."""
    out = {}
    for ano in (2014, 2018, 2022, 2026):
        B = montar_base(ano)
        X, nomes = regressoras(B, 'agregado')
        iL, iR = nomes.index('L1'), nomes.index('R1')
        Y = respostas(B)
        U = (B['apt1'] == B['apt2']) & (B['apt1'] > 0)
        fat = fatias(B)
        o = {}
        for grp in ('loc', 'mun'):
            ncl = int(B[grp].max()) + 1
            lts = montar_leituras(B, X, U, fat, B[grp])
            og = {}
            for nome, lt in lts.items():
                pf = []
                for i in range(4):
                    if lt['V'][i].vazio or lt['M'][i].vazio:
                        pf.append({'faixa': NOME_FAIXA[i], 'vazio': True}); continue
                    e = estat(lt['V'][i], lt['M'][i], Y['L2'], Y['R2'], iL, iR, ncl)
                    pf.append({'faixa': NOME_FAIXA[i], 'V': e['V'], 'epV': e['epV'], 'M': e['M'], 'epM': e['epM'],
                               'D': e['D'], 'ep': e['ep'], 'sinal': e['sinal'], 'sinal_espelho': e['sinal_espelho'],
                               'nV': lt['V'][i].N, 'nM': lt['M'][i].N})
                og[nome] = {'faixas': pf, 'contraste_menos35_menos_65mais': exploratorio_contraste(lt, Y['L2'], Y['R2'], iL, iR, ncl)}
            o[grp] = og
        # por região, efeito fixo de local, faixa de menos de 35% (para situar o que aparece no Sudeste em 2026)
        nl = int(B['loc'].max()) + 1
        reg = {}
        for g, ufs in REGIAO.items():
            mr = U & np.isin(B['uf'], ufs)
            rg = {}
            for nome, fF, fL in (('A_local', fat['fFl'], fat['fLl']), ('B_secao', fat['fFs'], fat['fLs'])):
                rV = Recorte(X, B['loc'], mr & em_faixa(fF, 0))
                rM = Recorte(X, B['loc'], mr & em_faixa(fL, 0))
                if rV.vazio or rM.vazio or rV.G < 30 or rM.G < 30:
                    rg[nome] = {'nV': rV.N, 'nM': rM.N, 'poucos_locais': True}
                    continue
                e = estat(rV, rM, Y['L2'], Y['R2'], iL, iR, nl)
                rg[nome] = {'V': e['V'], 'epV': e['epV'], 'M': e['M'], 'epM': e['epM'], 'D': e['D'], 'ep': e['ep'],
                            'nV': rV.N, 'nM': rM.N}
            reg[g] = rg
        o['regioes_loc'] = reg
        out[str(ano)] = o
        del B
    # 2026 menos cada ano, na faixa de menos de 35% (erros independentes entre anos)
    dif = {}
    for grp in ('loc', 'mun'):
        for nome in ('A_local', 'B_secao'):
            a = out['2026'][grp][nome]['faixas'][0]
            for ano in ('2014', '2018', '2022'):
                b = out[ano][grp][nome]['faixas'][0]
                dif['%s|%s|2026_menos_%s' % (grp, nome, ano)] = [a['D'] - b['D'], float(np.hypot(a['ep'], b['ep']))]
    out['diferencas_faixa_menos_35'] = dif
    return out


def exploratorio_regioes(B, X, nomes, Y, U, fat, PL, nloc):
    """Por região e nas cinco UFs do indício do comparecimento (PI, MA, TO, PB, CE) juntas."""
    iL, iR = nomes.index('L1'), nomes.index('R1')
    Lp, Rp, Ap, info = PL.gera('P_C1')
    grupos = dict(REGIAO)
    grupos['cinco_UFs_PI_MA_TO_PB_CE'] = ('PI', 'MA', 'TO', 'PB', 'CE')
    grupos['resto_sem_as_cinco'] = tuple(u for u in sorted(set(B['uf'].tolist())) if u not in ('PI', 'MA', 'TO', 'PB', 'CE', 'ZZ'))
    out = {}
    for g, ufs in grupos.items():
        m = U & np.isin(B['uf'], ufs)
        rec = Recorte(X, B['loc'], m)
        mt = matriz(rec, Y, nomes, nloc)
        o = {q: mt[q] for q in ('V', 'M', 'D_dentro', 'aF', 'aL', 'nao_voltou_F_menos_L', 'A1_para_L', 'A1_para_F', 'n', 'locais')}
        o['votos_F_1t'] = int(B['R1'][m].sum())
        for nome, fF, fL in (('A_local', fat['fFl'], fat['fLl']), ('B_secao', fat['fFs'], fat['fLs'])):
            rV = Recorte(X, B['loc'], m & em_faixa(fF, 0))
            rM = Recorte(X, B['loc'], m & em_faixa(fL, 0))
            fx = {'nV': rV.N, 'nM': rM.N, 'locais_V': rV.G, 'locais_M': rM.G,
                  'votos_F_1t_faixa': int(B['R1'][m & em_faixa(fF, 0)].sum())}
            if not rV.vazio and rV.G >= 30:
                b, ep, _ = rV.ajusta(Y['L2'], js=[iR]); fx['V'] = [float(b[iR]), ep[iR]]
                b2, _, _ = rV.ajusta(Lp, js=[iR]); fx['dV_com_C1'] = float(b2[iR] - b[iR])
            if not rM.vazio and rM.G >= 30:
                b, ep, _ = rM.ajusta(Y['R2'], js=[iL]); fx['M'] = [float(b[iL]), ep[iL]]
            if 'V' in fx and 'M' in fx:
                e = estat(rV, rM, Y['L2'], Y['R2'], iL, iR, nloc)
                ep_ = estat(rV, rM, Lp, Rp, iL, iR, nloc)
                fx['D'] = [e['D'], e['ep']]
                fx['D_com_C1'] = ep_['D']
            o['faixa_menos_35_' + nome] = fx
        out[g] = o
    return out


def exploratorio_tudo(B, X, nomes, Y, U, fat, PL, nloc, leituras, obs, R):
    E = {'aviso': 'Tudo neste bloco foi feito DEPOIS de ver os resultados da parte registrada. Não entra em veredito.'}
    iL, iR = nomes.index('L1'), nomes.index('R1')
    # E1. A variante com efeito fixo de município, que disparou
    E['E1_efeito_fixo_municipio'] = exploratorio_ef_municipio(B, X, nomes, Y, U, fat, PL)
    log('exploratório E1')
    # E3. Tamanho máximo compatível com cada regra de concentração (premissa: o espelho é o nível natural)
    # E4. Menor tamanho que o critério enxerga (D bruto + inclinação x T = 0,02), pela regra C1
    e3 = {}
    for nome in leituras:
        o = obs[nome][0]
        linha = {}
        for c in ('P_C1', 'P_C1L', 'P_C2', 'P_C3', 'P_C4', 'P_C5', 'P_U'):
            ve = R['cenarios'][c]['leituras'][nome]['valor_esperado'][0]
            dD, dV = ve['dD'], ve['dV']
            linha[c] = {'dD': dD, 'dV': dV, 'dM': ve['dM'],
                        'maximo_votos_premissa_espelho': max(0.0, o['D_mais_2ep']) / dD * TOTAL if dD > 0 else None,
                        'maximo_votos_so_V_nivel_natural_igual_ao_espelho': (max(0.0, o['V'] + 2 * o['epV'] - o['M']) / dV * TOTAL) if dV > 0.005 else None,
                        'menor_tamanho_que_dispara': (0.02 - o['D']) / dD * TOTAL if dD > 0 else None}
            for q in ('maximo_votos_premissa_espelho', 'menor_tamanho_que_dispara'):
                if linha[c][q] is not None:
                    linha[c][q + '_pct_da_margem'] = 100 * 2 * linha[c][q] / MARGEM
        e3[nome] = linha
    E['E3_E4_tamanhos_por_regra'] = e3
    # E5. Regiões e as cinco UFs do indício do comparecimento
    E['E5_regioes'] = exploratorio_regioes(B, X, nomes, Y, U, fat, PL, nloc)
    log('exploratório E5')
    # E6. Contraste entre as faixas extremas (tira um deslocamento constante do instrumento)
    e6 = {}
    Lp, Rp, Ap, _ = PL.gera('P_C1')
    L1_, R1_, A1_, _ = PL.gera('I1')
    L3_, R3_, A3_, _ = PL.gera('I3')
    for nome, lt in leituras.items():
        e6[nome] = {'observado': exploratorio_contraste(lt, Y['L2'], Y['R2'], iL, iR, nloc),
                    'com_C1': exploratorio_contraste(lt, Lp, Rp, iL, iR, nloc),
                    'com_I1': exploratorio_contraste(lt, L1_, R1_, iL, iR, nloc),
                    'com_I3': exploratorio_contraste(lt, L3_, R3_, iL, iR, nloc)}
    E['E6_contraste_faixas'] = e6
    # E7. Soma por UF: D da UF vezes os votos de Flávio no 1º turno da UF (universo), só positivas e todas
    ufs = R['por_uf']['ufs']
    lst = [(u, o['D_dentro'][0], o['D_dentro'][1], o['votos_F_1t']) for u, o in ufs.items() if u != 'ZZ' and not o.get('vazio')]
    pos = [x for x in lst if x[1] > 0]
    neg = [x for x in lst if x[1] < 0]
    E['E7_soma_por_uf'] = {
        'todas_votos': float(sum(x[1] * x[3] for x in lst)), 'todas_ep': float(np.sqrt(sum((x[2] * x[3]) ** 2 for x in lst))),
        'positivas_votos': float(sum(x[1] * x[3] for x in pos)), 'positivas_ufs': sorted(x[0] for x in pos),
        'negativas_votos': float(sum(x[1] * x[3] for x in neg)), 'negativas_ufs': sorted(x[0] for x in neg),
        'por_uf_votos': {x[0]: x[1] * x[3] for x in lst},
        'aviso': 'somar só as positivas é escolher depois de ver; o número serve de teto grosseiro, não de estimativa'}
    for q in ('todas_votos', 'positivas_votos', 'negativas_votos'):
        E['E7_soma_por_uf'][q + '_pct_da_margem'] = 100 * 2 * E['E7_soma_por_uf'][q] / MARGEM
    # E8. Teto da premissa extrema se existir nos dados uma entrada concentrada como a I3 (que rebaixa V)
    e8 = {}
    for nome in leituras:
        o = obs[nome][0]
        dvi3 = R['cenarios']['I3']['leituras'][nome]['valor_esperado'][0]['dV']
        dv = R['doses_C1'][nome]['dV_por_2136651']
        t = (max(0.0, o['V'] + 2 * o['epV']) - dvi3) / dv * TOTAL
        e8[nome] = {'dV_da_entrada_I3': dvi3, 'teto_votos': t, 'teto_pct_da_margem': 100 * 2 * t / MARGEM}
    E['E8_teto_extremo_com_entrada'] = e8
    # E9. As explicações pelo comparecimento com taxa uniforme DENTRO do local (regra por local ou por UF):
    #     a abstenção ainda dispara o critério? (valor esperado)
    R2f, A2f = PL.R2i.astype(float), PL.A2i.astype(float)
    _, p_entL = resolver_k(PL.A2i, pesos_regra(B, fat, 'C1L'), TOTAL)
    _, p_ent5 = resolver_k(PL.A2i, pesos_regra(B, fat, 'C5'), TOTAL)
    mods = {'abstencao_pela_regra_C1L_fatia_no_local': (Y['L2'], Y['R2'] - R2f * PL.p['C1L']),
            'abstencao_pela_regra_C5_so_Nordeste': (Y['L2'], Y['R2'] - R2f * PL.p['C5']),
            'entrada_pela_regra_C1L_fatia_no_local': (Y['L2'] + A2f * p_entL, Y['R2']),
            'entrada_pela_regra_C5_so_Nordeste': (Y['L2'] + A2f * p_ent5, Y['R2']),
            'abstencao_e_entrada_pela_regra_C1L': (Y['L2'] + A2f * p_entL, Y['R2'] - R2f * PL.p['C1L'])}
    e9 = {}
    for k, (l2, r2) in mods.items():
        e9[k] = {}
        for nome, lt in leituras.items():
            x = estat(lt['V'][0], lt['M'][0], l2, r2, iL, iR, nloc)
            o = obs[nome][0]
            e9[k][nome] = {'V': x['V'], 'M': x['M'], 'D': x['D'], 'ep': x['ep'], 'sinal': x['sinal'],
                           'dV': x['V'] - o['V'], 'dM': x['M'] - o['M'], 'dD': x['D'] - o['D']}
    E['E9_comparecimento_com_taxa_por_local'] = e9
    # E10. "Voto em nome de faltoso" na forma mais simples: entrada para Lula pro rata do estoque de faltosos do
    #      2º turno da seção, taxa uniforme. (a) no país, total de 2.136.651; (b) só nas cinco UFs do indício do
    #      comparecimento, taxa de 10% dos faltosos. Mede quanto V sobe (parte dos faltosos do 2º turno é eleitor
    #      de Flávio que não voltou, e a regressão o enxerga como "voto de Flávio que aparece em Lula").
    e10 = {}
    _, p_entU = resolver_k(PL.A2i, np.ones(len(A2f)), TOTAL)
    l2u = Y['L2'] + A2f * p_entU
    e10['pais_uniforme_2136651'] = {'taxa_dos_faltosos': float(p_entU.max())}
    for nome, lt in leituras.items():
        x = estat(lt['V'][0], lt['M'][0], l2u, Y['R2'], iL, iR, nloc)
        o = obs[nome][0]
        e10['pais_uniforme_2136651'][nome] = {'V': x['V'], 'D': x['D'], 'ep': x['ep'], 'sinal': x['sinal'],
                                              'dV': x['V'] - o['V'], 'dD': x['D'] - o['D']}
    cinco = np.isin(B['uf'], ('PI', 'MA', 'TO', 'PB', 'CE'))
    taxa = 0.10
    ent5 = np.where(cinco, A2f * taxa, 0.0)
    l25 = Y['L2'] + ent5
    o5 = {'taxa_dos_faltosos': taxa, 'votos_plantados_pais': float(ent5.sum()), 'votos_plantados_universo': float(ent5[U].sum()),
          'faltosos_2t_nas_cinco': float(A2f[cinco].sum())}
    for rot, m in (('cinco_UFs_inteiras', U & cinco), ('cinco_UFs_faixa_menos_35_A', U & cinco & em_faixa(fat['fFl'], 0)),
                   ('cinco_UFs_faixa_menos_35_B', U & cinco & em_faixa(fat['fFs'], 0))):
        rec = Recorte(X, B['loc'], m)
        b0, ep0, _ = rec.ajusta(Y['L2'], js=[iR])
        b1, ep1, _ = rec.ajusta(l25, js=[iR])
        ba, epa, _ = rec.ajusta(Y['A2'], js=[iR])
        dv = float(b1[iR] - b0[iR])
        teto_taxa = max(0.0, float(b0[iR]) + 2 * ep0[iR]) / dv * taxa if dv > 0 else None
        o5[rot] = {'n': rec.N, 'locais': rec.G, 'V': [float(b0[iR]), ep0[iR]], 'V_com_plantio': float(b1[iR]), 'dV': dv,
                   'nao_voltou_F': [float(ba[iR]), epa[iR]],
                   'taxa_maxima_premissa_V_natural_zero': teto_taxa,
                   'votos_maximos_premissa_V_natural_zero': (teto_taxa / taxa * float(ent5.sum())) if teto_taxa is not None else None}
    e10['cinco_UFs_taxa_10pct'] = o5
    E['E10_voto_em_nome_de_faltoso_pro_rata'] = e10
    return E


def exploratorio_depois(R):
    """Parte do exploratório que precisa das bases dos outros anos (roda depois de liberar a base de 2026)."""
    oa = exploratorio_outros_anos()
    log('exploratório outros anos')
    # tradução das diferenças entre anos pela inclinação do plantio C1 na especificação principal
    tr = {}
    for nome in ('A_local', 'B_secao'):
        dD = R['doses_C1'][nome]['dD_por_2136651']
        vF = R['observado'][nome][0]['lado_V']['votos_F_1t_pais']
        for ano in ('2014', '2018', '2022'):
            d, ep = oa['diferencas_faixa_menos_35']['loc|%s|2026_menos_%s' % (nome, ano)]
            tr['%s|2026_menos_%s' % (nome, ano)] = {
                'diferenca': d, 'ep': ep, 'direta_votos': d * vF, 'direta_pct_da_margem': 100 * 2 * d * vF / MARGEM,
                'pela_forma_C1_votos': d / dD * TOTAL, 'pela_forma_C1_pct_da_margem': 100 * 2 * d / dD * TOTAL / MARGEM}
    oa['traducao_das_diferencas'] = tr
    return oa


# ------------------------------------------------------------------ texto
def _n(x):
    return '{:,}'.format(int(round(x))).replace(',', '.')


def _c(x, d=4):
    if abs(x) < 0.5 * 10 ** (-d):
        x = 0.0
    return ('%+.*f' % (d, x)).replace('.', ',')


def _u(x, d=4):
    return ('%.*f' % (d, x)).replace('.', ',')


def _p(x, d=1):
    return ('%.*f' % (d, x)).replace('.', ',') + '%'


def _ce(par, d=4):
    return '%s (ep %s)' % (_c(par[0], d), _u(par[1], d))


NOME_LEITURA = {'A_local': 'Leitura A (faixa pela fatia no LOCAL de votação; é a letra)',
                'B_secao': 'Leitura B (faixa pela fatia na SEÇÃO; é a conta do exploratório)'}


def escrever_texto(R):
    L = []
    w = L.append
    ver = R['veredito']
    obs = R['observado']
    cen = R['cenarios']
    E = R.get('exploratorio', {})
    tr = R['traducao_em_votos']
    vA, vB = ver['A_local'], ver['B_secao']
    oA, oB = obs['A_local'][0], obs['B_secao'][0]
    w('R27_N3: FORMA REGULADA PELA FORÇA DE LULA (Adendo 28, teste N3)')
    w('')
    w('Registro: PRE-REGISTRO-2026-10-26.md, Adendo 28, item N3 (commit 938be19, 10/11/2026 04:36:33 UTC), antes de rodar.')
    w('Natureza: CONFIRMAÇÃO, por outro agente e com código próprio, de um exploratório que o conferente da A3 já tinha')
    w('visto (+0,0161 contra +0,0208). Não é teste cego. As decisões que o registro não fixa estão no docstring de')
    w('scripts/analisar_R27_N3.py, gravado em 10/11/2026 06:34:58 UTC, antes da primeira conta com votos')
    w('(SHA-256 %s).' % R['docstring_sha256'])
    w('Rodado em %s. Semente %d. Total plantado: %s votos.' % (R['terminado_em'], R['semente'], _n(R['total_plantado'])))
    w('')
    w('VEREDITO PELA LETRA')
    w('  %s: %s.' % (NOME_LEITURA['A_local'], vA['veredito_pela_letra']))
    w('    D = %s (ep %s); D + 2 ep = %s (limite do sem sinal: 0,01; limiar do sinal: 0,02 a mais de 4 ep).' % (
        _c(vA['D']), _u(vA['ep']), _c(vA['D_mais_2ep'])))
    w('  %s: %s.' % (NOME_LEITURA['B_secao'], vB['veredito_pela_letra']))
    w('    D = %s (ep %s); D + 2 ep = %s.' % (_c(vB['D']), _u(vB['ep']), _c(vB['D_mais_2ep'])))
    w('  Forma concentrada plantada (2.136.651 votos): detectada em %s dos 200 sorteios na Leitura A e em %s na B.' % (
        _p(100 * cen['P_C1']['leituras']['A_local']['sorteios']['sinal_freq'], 0),
        _p(100 * cen['P_C1']['leituras']['B_secao']['sorteios']['sinal_freq'], 0)))
    w('  Especificidade: o critério NÃO separa troca de abstenção concentrada (dispara em %s dos sorteios com abstenção' % (
        _p(100 * cen['I1']['leituras']['A_local']['sorteios']['sinal_freq'], 0)))
    w('  pura concentrada plantada, pelo lado do espelho). Isso tiraria valor de um SINAL; não muda um SEM SINAL.')
    vs = [o[nome]['veredito'] for o in R['variantes'].values() for nome in ('A_local', 'B_secao')]
    w('  Ao lado, %d variantes: %d SEM SINAL, %d INCONCLUSIVO e %d SINAL (as duas com efeito fixo de município no lugar de' % (
        len(vs), vs.count('SEM SINAL'), vs.count('INCONCLUSIVO'), vs.count('SINAL')))
    w('  local); a do desenho D4-1 na Leitura A passa a INCONCLUSIVO com o erro por município que aquele desenho pede.')
    w('  Descritivo por UF: sem veredito.')
    w('  Em uma frase: onde Flávio é fraco, a parcela dos votos dele que aparece em Lula é igual à do sentido contrário,')
    w('  e a troca concentrada do tamanho que vira o resultado teria aparecido; o teste não decide o canal do')
    w('  comparecimento, e o "igual ao espelho" não tem zero estável quando se olha 2014, 2018 e 2022.')
    w('')
    w('1. BASE E CONFERÊNCIAS')
    b = R['base']
    w('  %s seções com os dois turnos, %s locais de votação, soma igual ao oficial (Lula %s, Flávio %s, margem %s).' % (
        _n(b['secoes_dois_turnos']), _n(b['locais']), _n(b['L2']), _n(b['R2']), _n(b['margem'])))
    w('  Comparecimento %s no 1º turno e %s no 2º (aumento de %s). Identidades de soma dos dois turnos: erro zero.' % (
        _n(b['comp1']), _n(b['comp2']), _n(b['aumento_comparecimento'])))
    u = R['universo']
    w('  Universo principal (aptos iguais nos dois turnos, com o exterior): %s seções (%s saem; %s do exterior ficam).' % (
        _n(u['secoes']), _n(u['fora_por_aptos']), _n(u['exterior_no_universo'])))
    w('  Nele: Lula %s e Flávio %s no 2º turno, margem %s.' % (_n(u['votos_L_2t']), _n(u['votos_F_2t']), _n(u['margem_no_universo'])))
    ce = R['conferencia_estimador']
    w('  Estimador próprio conferido contra lib.fe_ols: %s seções informativas em %s locais nos dois; maior diferença de' % (
        _n(ce['n_meu']), _n(ce['grupos_meu'])))
    w('  coeficiente %.1e e de erro-padrão %.1e.' % (ce['dif_max_coef'], ce['dif_max_ep']))
    mu = R['matriz_universo']
    w('  Matriz no universo inteiro (referência, %s seções informativas): de Flávio para Lula %s; de Lula para Flávio %s;' % (
        _n(mu['n']), _ce(mu['V']), _ce(mu['M'])))
    w('  diferença %s. Não voltou: Flávio %s, Lula %s. Faltosos do 1º turno que aparecem em Lula %s e em Flávio %s.' % (
        _ce(mu['D_dentro']), _ce(mu['aF']), _ce(mu['aL']), _ce(mu['A1_para_L']), _ce(mu['A1_para_F'])))
    w('  Cada linha da matriz soma 1 (conferido: %s e %s).' % (_u(mu['soma_linha_R1'], 6), _u(mu['soma_linha_L1'], 6)))
    w('')
    w('2. RESULTADO REGISTRADO: MATRIZ DE TRANSFERÊNCIA POR FAIXA, COM O ESPELHO')
    w('  V = parcela dos votos de Flávio no 1º turno que aparece em Lula no 2º, na faixa pela força de FLÁVIO.')
    w('  M = parcela dos votos de Lula no 1º turno que aparece em Flávio no 2º, na faixa pela força de LULA (espelho).')
    w('  D = V - M. Efeito fixo de local, sem peso, erro por local; n = seções informativas (lado de V / lado de M).')
    for nome in ('A_local', 'B_secao'):
        w('  %s' % NOME_LEITURA[nome])
        w('    faixa          V (ep)             M (ep)             D (ep)             D/ep   D+2ep     n de V / n de M')
        for e in obs[nome]:
            w('    %-13s  %s (%s)   %s (%s)   %s (%s)   %6s  %s   %s / %s' % (
                e['faixa'], _c(e['V']), _u(e['epV']), _c(e['M']), _u(e['epM']), _c(e['D']), _u(e['ep']),
                _c(e['D_sobre_ep'], 1), _c(e['D_mais_2ep']), _n(e['lado_V']['n']), _n(e['lado_M']['n'])))
        e = obs[nome][0]
        w('    Na faixa que decide: %s seções no recorte de V (%s informativas em %s locais) e %s no de M (%s em %s locais).' % (
            _n(e['lado_V']['secoes']), _n(e['lado_V']['n']), _n(e['lado_V']['locais']),
            _n(e['lado_M']['secoes']), _n(e['lado_M']['n']), _n(e['lado_M']['locais'])))
        w('    Erro de D por município: %s; pela raiz da soma dos quadrados: %s. Distância ao limiar: (D - 0,02)/ep = %s.' % (
            _u(e['ep_por_municipio']), _u(e['ep_independente']), _c(e['D_menos_limiar_sobre_ep'], 1)))
        mv = e['matriz_lado_V']
        mm = e['matriz_lado_M']
        w('    Onde Flávio é fraco: eleitor de Flávio que não voltou %s; faltosos do 1º turno que aparecem em Lula %s e' % (
            _ce(mv['aF']), _ce(mv['A1_para_L'])))
        w('    em Flávio %s. Onde Lula é fraco: eleitor de Lula que não voltou %s; faltosos em Lula %s, em Flávio %s.' % (
            _ce(mv['A1_para_F']), _ce(mm['aL']), _ce(mm['A1_para_L']), _ce(mm['A1_para_F'])))
    w('  Reprodução do exploratório (Leitura B): V = %s com n = %s e espelho %s. O conferente da A3 tinha +0,0161' % (
        _ce([oB['V'], oB['epV']]), _n(oB['lado_V']['n']), _ce([oB['M'], oB['epM']])))
    w('  (ep 0,0030; n 95.386) e +0,0208 (ep 0,0022). Igual.')
    w('  Pela letra: SINAL exige D >= 0,02 a mais de 4 ep; não dispara em nenhuma das duas leituras. SEM SINAL exige')
    w('  D + 2 ep < 0,01 com a forma plantada detectada; vale nas duas (%s e %s). Com erro por município o veredito' % (
        _c(vA['D_mais_2ep']), _c(vB['D_mais_2ep'])))
    w('  fica %s na A e %s na B.' % (vA['veredito_com_erro_por_municipio'], vB['veredito_com_erro_por_municipio']))
    w('')
    w('3. CALIBRAÇÃO: A FORMA CONCENTRADA PLANTADA NOS DADOS DE 2026')
    pr = R['plantio_regras']
    w('  Regra C1 (a do registro): em toda seção do país, votos saem de Flávio e entram em Lula no 2º turno com taxa')
    w('  igual a %s vezes a fatia de Lula na seção no 1º turno (taxa média %s dos votos de Flávio, máxima %s),' % (
        _u(pr['C1']['k']), _p(100 * pr['C1']['taxa_media_ponderada'], 2), _p(100 * pr['C1']['taxa_max'], 2)))
    w('  total esperado de 2.136.651 votos (4.273.302 de margem, %s da margem oficial).' % _p(tr['referencia']['forma_plantada_pct_da_margem']))
    w('  cenário  regra                                         leitura   V        M        D (dp)             dV       dM       dD      dispara')
    ordem = ['P_C1', 'P_C1L', 'P_C2', 'P_C3', 'P_C4', 'P_C5', 'P_U']
    rot = {'P_C1': 'C1: taxa proporcional à fatia de Lula na seção', 'P_C1L': 'C1L: proporcional à fatia de Lula no local',
           'P_C2': 'C2: só onde Lula teve 50% ou mais, uniforme', 'P_C3': 'C3: proporcional ao quadrado da fatia',
           'P_C4': 'C4: forma k x L (proporcional aos votos de Lula)', 'P_C5': 'C5: só no Nordeste, uniforme',
           'P_U': 'U: uniforme no país (referência)', 'I1': 'I1: abstenção pura concentrada (regra C1)',
           'I2': 'I2: abstenção pura uniforme de 3,6%', 'I3': 'I3: entrada concentrada de eleitores reais',
           'I4': 'I4: I1 e I3 juntas (virada pelo comparecimento)', 'E2': 'E2: espelho, de Lula para Flávio',
           'S1': 'S1: troca C1 mais entrada I3 (estresse)'}

    def linha_cen(c):
        for nome in ('A_local', 'B_secao'):
            s = cen[c]['leituras'][nome]['sorteios']
            w('  %-7s  %-45s %s   %s  %s  %s (%s)   %s  %s  %s   %s de %d' % (
                c, rot[c], nome[0], _c(s['V_media']), _c(s['M_media']), _c(s['D_media']), _u(s['D_dp']),
                _c(s['dV_media']), _c(s['dM_media']), _c(s['dD_media']), _n(s['sinal_freq'] * s['sorteios']), s['sorteios']))
    for c in ordem:
        linha_cen(c)
    c1a = cen['P_C1']['leituras']['A_local']
    c1b = cen['P_C1']['leituras']['B_secao']
    w('  Pelo valor esperado (sem sorteio), a C1 dá D = %s na Leitura A e %s na B, e o critério dispara nas duas.' % (
        _c(c1a['valor_esperado'][0]['D']), _c(c1b['valor_esperado'][0]['D'])))
    w('  A taxa plantada na faixa de menos de 35%% é %s; V sobe %s e o espelho M cai %s (o plantio tira voto de' % (
        _p(100 * c1a['valor_esperado'][0]['taxa_troca_na_faixa_V'], 2), _u(c1a['valor_esperado'][0]['dV']),
        _u(-c1a['valor_esperado'][0]['dM'])))
    w('  Flávio também onde Lula é fraco, em proporção à fatia de Lula, e isso rebaixa M). Com M fixo no valor bruto,')
    w('  o critério ainda dispara em %s dos sorteios (A) e %s (B): a detecção não depende do espelho.' % (
        _p(100 * c1a['sorteios']['sinal_com_M_fixo_freq'], 0), _p(100 * c1b['sorteios']['sinal_com_M_fixo_freq'], 0)))
    w('  A forma k x L (C4) quase não mexe em V (%s): o critério só a enxerga pelo espelho (M cai %s).' % (
        _c(cen['P_C4']['leituras']['A_local']['valor_esperado'][0]['dV']), _u(-cen['P_C4']['leituras']['A_local']['valor_esperado'][0]['dM'])))
    w('  Nas regras em que a taxa é a mesma dentro do local (C1L, C2 quase, C5, U) o espelho não se mexe e a detecção')
    w('  vem toda de V.')
    w('  Perfil da C1 nas quatro faixas (subida de D, Leitura A): %s.' % '; '.join(
        '%s %s' % (e['faixa'], _c(e['dD'])) for e in c1a['valor_esperado']))
    w('  Doses da C1 pelo valor esperado (Leitura A):')
    for p in R['doses_C1']['A_local']['pontos']:
        w('    %3d%% do total (%s votos): V sobe %s, M %s, D vai a %s (%s ep). Critério %s.' % (
            round(100 * p['dose']), _n(p['votos']), _c(p['dV']), _c(p['dM']), _c(p['D']), _c(p['D_sobre_ep'], 1),
            'dispara' if p['sinal'] else 'não dispara'))
    w('  Inclinação: D sobe %s por 2.136.651 votos na Leitura A e %s na B.' % (
        _c(R['doses_C1']['A_local']['dD_por_2136651']), _c(R['doses_C1']['B_secao']['dD_por_2136651'])))
    w('')
    w('4. ESPECIFICIDADE: O QUE PASSA PELO COMPARECIMENTO, PLANTADO')
    w('  Aviso fixado antes: boletim não separa quem faltou de quem foi registrado como faltoso, nem eleitor real que')
    w('  entrou de voto lançado em nome de faltoso. "Inocente" aqui quer dizer só "não é troca de voto dentro da urna".')
    w('  cenário  o que se planta                                leitura   V        M        D (dp)             dV       dM       dD      dispara')
    for c in ('I1', 'I2', 'I3', 'I4', 'S1'):
        linha_cen(c)
    i1 = cen['I1']['leituras']['A_local']['valor_esperado'][0]
    i3 = cen['I3']['leituras']['A_local']['valor_esperado'][0]
    w('  Leitura: (i) abstenção pura CONCENTRADA pela regra C1 dispara o critério sem nenhuma troca. Ela não mexe em V')
    w('  (%s, por aritmética: Lula não ganha voto), mas rebaixa o espelho M em %s, e D sobe %s. Logo um SINAL neste' % (
        _c(i1['dV']), _u(-i1['dM']), _u(i1['dD'])))
    w('  teste não distinguiria troca de abstenção concentrada. (ii) Abstenção uniforme não mexe em nada. (iii) Entrada')
    w('  concentrada de eleitores reais para Lula REBAIXA V em %s (taxa de %s dos faltosos na faixa): pode esconder parte de' % (
        _u(-i3['dV']), _p(100 * i3['taxa_entrada_na_faixa_V'], 1)))
    w('  uma troca. (iv) Com troca e entrada do mesmo tamanho juntas (S1) o critério ainda dispara em %s dos sorteios' % (
        _p(100 * cen['S1']['leituras']['A_local']['sorteios']['sinal_freq'], 0)))
    w('  (com M fixo, em %s). (v) A estatística só com V é específica contra abstenção e cega para a forma k x L.' % (
        _p(100 * cen['S1']['leituras']['A_local']['sorteios']['sinal_com_M_fixo_freq'], 0)))
    w('  (vi) Depois de ver (exploratório E9): com taxa igual dentro do local, a abstenção não mexe em nada e a entrada')
    w('  SOBE V em vez de rebaixar. O efeito da entrada depende da forma.')
    w('  Consequência para a leitura do resultado: como o resultado bruto é SEM SINAL, a falta de especificidade não o')
    w('  afeta; o que o afeta é a possibilidade (iii), tratada na seção 9.')
    w('')
    w('5. ESPELHO')
    w('  (i) Critério invertido nos dados brutos (-D >= 0,02 a mais de 4 ep): %s na Leitura A e %s na B.' % (
        'dispara' if vA['sinal_espelho'] else 'não dispara', 'dispara' if vB['sinal_espelho'] else 'não dispara'))
    e2 = cen['E2']['leituras']
    w('  (ii) Plantio espelho (2.136.651 votos de Lula para Flávio, concentrados onde Flávio é forte): D vai a %s (A) e' % (
        _c(e2['A_local']['sorteios']['D_media'])))
    w('  %s (B); o critério invertido dispara em %s e %s dos 200 sorteios e o direto em %s e %s.' % (
        _c(e2['B_secao']['sorteios']['D_media']), _p(100 * e2['A_local']['sorteios']['sinal_espelho_freq'], 0),
        _p(100 * e2['B_secao']['sorteios']['sinal_espelho_freq'], 0), _p(100 * e2['A_local']['sorteios']['sinal_freq'], 0),
        _p(100 * e2['B_secao']['sorteios']['sinal_freq'], 0)))
    w('  (iii) Nas outras faixas (tabela da seção 2) D não passa de 0,02 em nenhuma. Na de 35 a 50%% fica em %s (A) e' % (
        _ce([obs['A_local'][1]['D'], obs['A_local'][1]['ep']])))
    w('  %s (B); na de 65%% ou mais fica negativo, %s (A): nos redutos, quem aparece mais no adversário é o' % (
        _ce([obs['B_secao'][1]['D'], obs['B_secao'][1]['ep']]), _ce([obs['A_local'][3]['D'], obs['A_local'][3]['ep']])))
    w('  eleitor de Lula, não o de Flávio.')
    w('')
    w('6. AO LADO: OUTROS UNIVERSOS E ESPECIFICAÇÕES (faixa de menos de 35%)')
    w('  variante                 leitura  D (ep)              D+2ep     veredito        com a C1 plantada')
    for k, o in R['variantes'].items():
        for nome in ('A_local', 'B_secao'):
            e = o[nome]
            extra = ''
            if e.get('veredito_ep_municipio') and e['veredito_ep_municipio'] != e['veredito']:
                extra = '  (com erro por município: %s)' % e['veredito_ep_municipio']
            w('  %-24s %s        %s (%s)   %s   %-14s  D = %s, %s%s' % (
                k, nome[0], _c(e['D']), _u(e['ep']), _c(e['D_mais_2ep']), e['veredito'], _c(e['com_C1']['D']),
                'dispara' if e['com_C1']['sinal'] else 'não dispara', extra))
    for k, o in R['variantes'].items():
        w('    %s: %s (%s seções).' % (k, o['descricao'], _n(o['secoes_universo'])))
    vm = R['variantes']['efeito_fixo_municipio']
    w('  Duas variantes saem do SEM SINAL por margem mínima (todas as seções, Leitura A; D4-1 com erro por município).')
    w('  Uma variante DISPARA: com efeito fixo de município no lugar de local, D = %s (A) e %s (B).' % (
        _ce([vm['A_local']['D'], vm['A_local']['ep']]), _ce([vm['B_secao']['D'], vm['B_secao']['ep']])))
    w('  Nela V e M são negativos (V = %s, M = %s na A), o que uma parcela de eleitores não pode ser: é a marca de' % (
        _c(vm['A_local']['V']), _c(vm['A_local']['M'])))
    w('  viés de composição entre bairros do mesmo município. Ver o exploratório E1.')
    w('')
    w('7. OUTROS ANOS, AO LADO (NÃO É RÉGUA; o Léo suspeita também de 2014, 2018 e 2022)')
    w('  A mesma estatística com os eliminados agregados (as bases antigas não os separam), efeito fixo de local.')
    w('  ano    leitura   V         M         D (ep)             n de V / n de M     na mesma linha, 2026 bruto')
    oa = R['outros_anos_nao_e_regua']
    for ano in ('2014', '2018', '2022', '2026'):
        for nome in ('A_local', 'B_secao'):
            e = oa[ano][nome][0]
            r = oa['2026'][nome][0]
            w('  %s   %s         %s   %s   %s (%s)   %s / %s   2026: %s (%s)' % (
                ano, nome[0], _c(e['V']), _c(e['M']), _c(e['D']), _u(e['ep']), _n(e['nV']), _n(e['nM']), _c(r['D']), _u(r['ep'])))
    w('  Pelo mesmo critério, 2014 daria SINAL direto (a favor de Dilma), 2018 e 2022 dariam SINAL invertido (contra o')
    w('  PT), e 2026 é o único dos quatro anos em que D fica perto de zero. O "zero" deste instrumento não é estável:')
    w('  andou de -0,05 a +0,05 em três eleições. Nenhum veredito acima depende desses anos.')
    w('')
    w('8. POR UF (DESCRITIVO, SEM VEREDITO): A MATRIZ DENTRO DE CADA UF, UNIVERSO PRINCIPAL')
    w('  V = de Flávio para Lula; M = de Lula para Flávio; D = V - M (erro conjunto por local). "Não voltou" = coeficiente')
    w('  do candidato na equação dos faltosos do 2º turno. A1>L e A1>F = faltosos do 1º turno que aparecem em cada um.')
    w('  UF  n        V (ep)             M (ep)             D (ep)             não voltou F    L        A1>L     A1>F     D com C1  D com U')
    ufs = R['por_uf']['ufs']
    for uf, o in sorted(ufs.items(), key=lambda kv: (kv[0] == 'ZZ', -(kv[1]['D_dentro'][0] if not kv[1].get('vazio') else 0))):
        if o.get('vazio'):
            continue
        w('  %s  %7s  %s (%s)   %s (%s)   %s (%s)   %s         %s  %s  %s  %s   %s%s' % (
            uf, _n(o['n']), _c(o['V'][0]), _u(o['V'][1]), _c(o['M'][0]), _u(o['M'][1]), _c(o['D_dentro'][0]), _u(o['D_dentro'][1]),
            _c(o['aF'][0]), _c(o['aL'][0]), _c(o['A1_para_L'][0]), _c(o['A1_para_F'][0]), _c(o['com_C1']['D_dentro'][0]),
            _c(o['com_U']['D_dentro'][0]), '  (exterior, fora das 27)' if uf == 'ZZ' else ''))
    ru = R['por_uf']['resumo']
    w('  Resumo das 27 UFs: D vai de %s (%s) a %s (%s); média simples %s; ponderada pelo inverso da variância %s (ep %s);' % (
        _c(ru['min'][1]), ru['min'][0], _c(ru['max'][1]), ru['max'][0], _c(ru['media_simples']), _c(ru['media_ponderada_inv_var']), _u(ru['ep_media'])))
    w('  desvio-padrão entre UFs %s; qui-quadrado de homogeneidade %s com %d graus de liberdade (heterogêneo).' % (
        _u(ru['dp_entre_ufs']), _u(ru['qui2_homogeneidade'], 1), ru['gl']))
    w('  Acima de +0,010: %d UFs (%s). Abaixo de -0,010: %d (%s).' % (
        len(ru['ufs_acima_de_+0.010']), ', '.join(ru['ufs_acima_de_+0.010']), len(ru['ufs_abaixo_de_-0.010']), ', '.join(ru['ufs_abaixo_de_-0.010'])))
    w('  Positivas a mais de 2 ep: %s. Negativas a mais de 2 ep: %s.' % (', '.join(ru['ufs_positivas_a_2ep']), ', '.join(ru['ufs_negativas_a_2ep'])))
    w('  A forma C1 plantada subiria D em TODAS as 27 UFs, de %s a %s (média %s); a uniforme, de %s a %s.' % (
        _c(ru['com_C1_subida_min']), _c(ru['com_C1_subida_max']), _c(ru['com_C1_subida_media']), _c(ru['com_U_subida_min']), _c(ru['com_U_subida_max'])))
    w('  Correlação entre D da UF e a fatia de Lula na UF no 1º turno: %s (27 UFs); inclinação %s por unidade de fatia.' % (
        _c(ru['correlacao_D_com_fatia_de_Lula'], 2), _c(ru['inclinacao_D_por_fatia_de_Lula'], 3)))
    cinco = [(u_, ufs[u_]) for u_ in ('PI', 'MA', 'TO', 'PB', 'CE')]
    w('  Nas cinco UFs do indício do comparecimento: ' + '; '.join('%s %s' % (u_, _ce(o['D_dentro'])) for u_, o in cinco) + '.')
    w('  Nelas a diferença de quem não voltou (Flávio menos Lula) é: ' + '; '.join('%s %s' % (u_, _c(o['nao_voltou_F_menos_L'][0])) for u_, o in cinco) + '.')
    w('  Dentro da faixa de menos de 35% (Leitura A), onde há 30 locais ou mais de cada lado na UF:')
    lst = [(u_, o['faixa_menos_35_leitura_A']) for u_, o in ufs.items() if not o.get('vazio') and 'D' in o['faixa_menos_35_leitura_A']]
    for u_, fx in sorted(lst, key=lambda x: -x[1]['D'][0]):
        w('    %s: V %s; M %s; D %s (%s ep); n %s / %s' % (u_, _ce(fx['V']), _ce(fx['M']), _ce(fx['D']), _c(fx['D'][0] / fx['D'][1], 1), _n(fx['nV']), _n(fx['nM'])))
    w('    Só V (a UF não tem 30 locais em que Lula é fraco): ' + '; '.join(
        '%s %s' % (u_, _ce(o['faixa_menos_35_leitura_A']['V'])) for u_, o in sorted(ufs.items())
        if not o.get('vazio') and 'V' in o['faixa_menos_35_leitura_A'] and 'D' not in o['faixa_menos_35_leitura_A']) + '.')
    w('')
    w('9. TRADUÇÃO EM VOTOS DE MARGEM (margem oficial 4.430.191; vira com 2.215.096 votos trocados)')
    for nome in ('A_local', 'B_secao'):
        t = tr[nome]
        w('  %s' % NOME_LEITURA[nome])
        w('    Votos de Flávio no 1º turno nas seções da faixa, país inteiro: %s.' % _n(t['votos_F_1t_na_faixa_pais']))
        w('    Direta: D x esses votos = %s votos (%s da margem, contando em dobro). Teto com D + 2 ep: %s votos,' % (
            _n(t['direta_votos']), _p(t['direta_pct_da_margem'], 2), _n(t['direta_teto_votos'])))
        w('    %s de margem, %s da margem.' % (_n(t['direta_teto_margem']), _p(t['direta_teto_pct_da_margem'], 2)))
        w('    Pela calibração, premissa "o espelho é o nível natural": a forma concentrada C1 cabe até %s votos' % _n(t['forma_C1_maximo_votos_premissa_espelho']))
        w('    (%s da margem); o plantado tinha 2.136.651.' % _p(t['forma_C1_maximo_votos_premissa_espelho_pct_da_margem']))
        w('    Premissa extrema (tudo o que há em V é troca, nível natural zero): até %s votos (%s da margem).' % (
            _n(t['forma_C1_maximo_votos_premissa_extrema']), _p(t['forma_C1_maximo_votos_premissa_extrema_pct_da_margem'])))
    w('  Aviso: a premissa extrema supõe que nada rebaixa V. A entrada concentrada de eleitores reais (I3) rebaixa V em')
    e8 = E.get('E8_teto_extremo_com_entrada')
    if e8:
        w('  %s por 2.136.651 entradas. Se uma entrada desse tamanho e dessa forma existir nos dados, o teto da premissa' % _u(-e8['A_local']['dV_da_entrada_I3']))
        w('  extrema sobe para %s votos na Leitura A (%s da margem) e %s na B (%s): conta feita depois de ver.' % (
            _n(e8['A_local']['teto_votos']), _p(e8['A_local']['teto_pct_da_margem']), _n(e8['B_secao']['teto_votos']), _p(e8['B_secao']['teto_pct_da_margem'])))
        w('  Sem a premissa do espelho, o teste sozinho não exclui a forma concentrada do tamanho que vira. O contrário')
        w('  também vale: entrada com taxa igual dentro do local sobe V (E9), e nesse caso o teto verdadeiro seria menor.')
    w('')
    if E:
        w('10. EXPLORATÓRIO (feito DEPOIS de ver os resultados acima; não entra em veredito; ninguém refez)')
        e1 = E['E1_efeito_fixo_municipio']
        w('  E1. A variante com efeito fixo de município, que disparou. Faixas (Leitura A):')
        for e in e1['A_local']['faixas']:
            w('      %-13s V %s (%s)  M %s (%s)  D %s (%s)  %s ep' % (e['faixa'], _c(e['V']), _u(e['epV']), _c(e['M']), _u(e['epM']), _c(e['D']), _u(e['ep']), _c(e['D_sobre_ep'], 1)))
        c_ = e1['A_local']['cenarios']
        w('      O que cada plantio faz nela (subida de D): C1 %s; uniforme %s; k x L %s; abstenção concentrada %s;' % (
            _c(c_['P_C1']['dD']), _c(c_['P_U']['dD']), _c(c_['P_C4']['dD']), _c(c_['I1']['dD'])))
        w('      entrada concentrada %s. No universo inteiro com efeito fixo de município: V %s, M %s.' % (
            _c(c_['I3']['dD']), _ce(e1['universo']['V']), _ce(e1['universo']['M'])))
        w('      Leitura: V e M negativos mostram que, entre locais do mesmo município, a regressão carrega diferença de')
        w('      composição entre bairros; o disparo vem de M ser mais negativo que V, não de V positivo. A abstenção')
        w('      concentrada sozinha produz essa subida. Ainda assim é uma especificação em que o critério dispara, e isso')
        w('      fica dito.')
        o2 = E.get('E2_outros_anos_nao_e_regua')
        if o2:
            w('  E2. Não é régua. D na faixa de menos de 35% nos quatro anos (outros agregados; * dispara, # dispara invertido):')
            w('      ano    efeito fixo de local: A            B                 efeito fixo de município: A      B')
            for ano in ('2014', '2018', '2022', '2026'):
                def cel(grp, nome):
                    e = o2[ano][grp][nome]['faixas'][0]
                    return '%s (%s)%s' % (_c(e['D']), _u(e['ep']), '*' if e['sinal'] else ('#' if e['sinal_espelho'] else ' '))
                w('      %s   %s   %s            %s   %s' % (ano, cel('loc', 'A_local'), cel('loc', 'B_secao'), cel('mun', 'A_local'), cel('mun', 'B_secao')))
            t2 = o2['traducao_das_diferencas']
            for ano in ('2014', '2018', '2022'):
                x = t2['A_local|2026_menos_%s' % ano]
                w('      2026 menos %s (Leitura A, local): %s (ep %s). Se fosse a forma C1: %s votos (%s da margem); direta: %s votos.' % (
                    ano, _c(x['diferenca']), _u(x['ep']), _n(x['pela_forma_C1_votos']), _p(x['pela_forma_C1_pct_da_margem']), _n(x['direta_votos'])))
            w('      Leitura nos dois sentidos: medido contra 2018 ou 2022, 2026 está cerca de 0,05 ACIMA, o que na forma C1')
            w('      valeria perto de 1,3 milhão de votos (perto de 58% da margem; sozinho não vira). Medido contra 2014, está')
            w('      0,05 ABAIXO. Como os três anos também são suspeitos para o Léo, nenhum serve de zero.')
            w('      Por região, efeito fixo de local, faixa de menos de 35% (Leitura A), D (ep):')
            for g in ('N', 'NE', 'SE', 'S', 'CO'):
                cels = []
                for ano in ('2014', '2018', '2022', '2026'):
                    x = o2[ano]['regioes_loc'][g]['A_local']
                    cels.append('%s %s' % (ano, 'poucos locais' if x.get('poucos_locais') else '%s (%s)' % (_c(x['D']), _u(x['ep']))))
                w('        %-2s  %s' % (g, ';  '.join(cels)))
        e3 = E['E3_E4_tamanhos_por_regra']
        w('  E3 e E4. Por regra de concentração (Leitura A / Leitura B): menor tamanho que o critério enxerga e maior tamanho')
        w('      compatível com o observado (premissa: o espelho é o nível natural), em votos trocados:')
        for c in ordem:
            a, b_ = e3['A_local'][c], e3['B_secao'][c]
            w('      %-48s enxerga a partir de %s / %s;  cabe até %s / %s' % (
                rot[c], _n(a['menor_tamanho_que_dispara']), _n(b_['menor_tamanho_que_dispara']),
                _n(a['maximo_votos_premissa_espelho']), _n(b_['maximo_votos_premissa_espelho'])))
        e5 = E['E5_regioes']
        w('  E5. Por região e nas cinco UFs do indício do comparecimento, faixa de menos de 35%:')
        w('      grupo                        leitura  V (ep)             M (ep)             D (ep)             D/ep   n de V / n de M    D com C1')
        for g, o in e5.items():
            for nome in ('A_local', 'B_secao'):
                fx = o['faixa_menos_35_' + nome]
                if 'D' in fx:
                    w('      %-28s %s        %s (%s)   %s (%s)   %s (%s)   %s   %s / %s   %s' % (
                        g, nome[0], _c(fx['V'][0]), _u(fx['V'][1]), _c(fx['M'][0]), _u(fx['M'][1]), _c(fx['D'][0]), _u(fx['D'][1]),
                        _c(fx['D'][0] / fx['D'][1], 1), _n(fx['nV']), _n(fx['nM']), _c(fx['D_com_C1'])))
                elif 'V' in fx:
                    w('      %-28s %s        %s (%s)   sem 30 locais do lado de M   n de V %s' % (g, nome[0], _c(fx['V'][0]), _u(fx['V'][1]), _n(fx['nV'])))
        s5 = e5['cinco_UFs_PI_MA_TO_PB_CE']
        se_ = e5['SE']
        w('      Nas cinco UFs juntas (PI, MA, TO, PB, CE), onde Flávio é fraco, V = %s com %s seções informativas' % (
            _ce(s5['faixa_menos_35_A_local']['V']), _n(s5['faixa_menos_35_A_local']['nV'])))
        w('      (%s votos de Flávio no 1º turno), abaixo do resto do país (%s); a C1 plantada o subiria em %s.' % (
            _n(s5['faixa_menos_35_A_local']['votos_F_1t_faixa']), _ce(e5['resto_sem_as_cinco']['faixa_menos_35_A_local']['V']),
            _u(s5['faixa_menos_35_A_local']['dV_com_C1'])))
        w('      A diferença de quem não voltou nelas é %s. O eleitor de Flávio dali aparece na abstenção, não em Lula.' % _ce(s5['nao_voltou_F_menos_L']))
        w('      Ressalva: entrada concentrada de eleitores reais rebaixa V (seção 4), e nessas UFs a entrada para Lula é alta.')
        w('      No Sudeste a Leitura A dá D = %s (%s ep), acima de 0,02 e de 4 ep; a Leitura B dá %s (%s ep).' % (
            _ce(se_['faixa_menos_35_A_local']['D']), _c(se_['faixa_menos_35_A_local']['D'][0] / se_['faixa_menos_35_A_local']['D'][1], 1),
            _ce(se_['faixa_menos_35_B_secao']['D']), _c(se_['faixa_menos_35_B_secao']['D'][0] / se_['faixa_menos_35_B_secao']['D'][1], 1)))
        vse = se_['faixa_menos_35_A_local']['D'][0] * se_['faixa_menos_35_A_local']['votos_F_1t_faixa']
        w('      É recorte escolhido depois de ver (uma de cinco regiões, uma de duas leituras) e vale %s votos (%s de' % (_n(vse), _n(2 * vse)))
        w('      margem, %s da margem), porque no Sudeste há poucos votos de Flávio em locais onde ele é fraco (%s).' % (
            _p(100 * 2 * vse / MARGEM, 2), _n(se_['faixa_menos_35_A_local']['votos_F_1t_faixa'])))
        if o2:
            w('      No Sudeste o mesmo D foi positivo também em 2014 e 2018 e negativo em 2022 (tabela do E2; não é régua).')
        e6 = E['E6_contraste_faixas']
        w('  E6. Contraste entre as faixas extremas, D(menos de 35%) menos D(65% ou mais), que tira um deslocamento')
        w('      constante do instrumento: observado %s (A) e %s (B); com a C1 plantada %s (A); com abstenção' % (
            _ce(e6['A_local']['observado']), _ce(e6['B_secao']['observado']), _c(e6['A_local']['com_C1'][0])))
        w('      concentrada %s; com entrada concentrada %s.' % (_c(e6['A_local']['com_I1'][0]), _c(e6['A_local']['com_I3'][0])))
        if o2:
            w('      Nos outros anos (não é régua; efeito fixo de local, Leitura A): ' + '; '.join(
                '%s %s' % (ano, _c(o2[ano]['loc']['A_local']['contraste_menos35_menos_65mais'][0])) for ano in ('2014', '2018', '2022', '2026')) + '.')
        e9 = E.get('E9_comparecimento_com_taxa_por_local')
        if e9:
            w('  E9. As explicações pelo comparecimento com taxa igual dentro do local (valor esperado, Leitura A), para')
            w('      saber quando a abstenção dispara o critério: subida de V, de M e de D, e se dispara.')
            rot9 = {'abstencao_pela_regra_C1L_fatia_no_local': 'abstenção, taxa pela fatia de Lula no local',
                    'abstencao_pela_regra_C5_so_Nordeste': 'abstenção, só no Nordeste, uniforme',
                    'entrada_pela_regra_C1L_fatia_no_local': 'entrada, taxa pela fatia de Lula no local',
                    'entrada_pela_regra_C5_so_Nordeste': 'entrada, só no Nordeste, uniforme',
                    'abstencao_e_entrada_pela_regra_C1L': 'abstenção e entrada juntas, taxa por local'}
            for k, o in e9.items():
                x = o['A_local']
                w('      %-46s dV %s  dM %s  dD %s  %s' % (rot9[k], _c(x['dV']), _c(x['dM']), _c(x['dD']), 'dispara' if x['sinal'] else 'não dispara'))
            w('      Com taxa igual dentro do local, a abstenção não mexe em V nem em M: o critério não a acusa e também não')
            w('      a enxerga. A entrada com taxa igual dentro do local SOBE V (ao contrário da I3), porque parte dos faltosos')
            w('      do 2º turno é eleitor de Flávio que não voltou; concentrada só no Nordeste, ela sozinha dispararia o critério.')
            w('      Resumo: o teste confunde abstenção com troca só quando a taxa varia de seção para seção no mesmo local, e')
            w('      a entrada tanto pode esconder uma troca (taxa que acompanha a fatia de Lula da seção) quanto imitá-la')
            w('      (taxa igual no local). O aviso do docstring ("não acusa nem absolve o comparecimento") vale só em parte.')
        e10 = E.get('E10_voto_em_nome_de_faltoso_pro_rata')
        if e10:
            pu = e10['pais_uniforme_2136651']
            c5 = e10['cinco_UFs_taxa_10pct']
            w('  E10. "Voto em nome de faltoso" na forma mais simples: entrada para Lula pro rata do estoque de faltosos do')
            w('      2º turno da seção, taxa uniforme (valor esperado).')
            w('      No país, 2.136.651 votos (%s dos faltosos): V sobe %s e D vai a %s na Leitura A; critério %s.' % (
                _p(100 * pu['taxa_dos_faltosos'], 2), _c(pu['A_local']['dV']), _c(pu['A_local']['D']),
                'dispara' if pu['A_local']['sinal'] else 'não dispara'))
            w('      Só nas cinco UFs (PI, MA, TO, PB, CE), 10%% dos faltosos (%s votos):' % _n(c5['votos_plantados_pais']))
            for rot_, nome_ in (('cinco_UFs_inteiras', 'as cinco UFs inteiras'), ('cinco_UFs_faixa_menos_35_A', 'faixa de menos de 35%, Leitura A'),
                                ('cinco_UFs_faixa_menos_35_B', 'faixa de menos de 35%, Leitura B')):
                x = c5[rot_]
                w('        %-34s V observado %s; com o plantio %s (sobe %s); n %s. Teto com V + 2 ep e nível natural' % (
                    nome_ + ':', _ce(x['V']), _c(x['V_com_plantio']), _u(x['dV']), _n(x['n'])))
                w('        %-34s zero: taxa de %s dos faltosos, %s votos.' % ('', _p(100 * x['taxa_maxima_premissa_V_natural_zero'], 1), _n(x['votos_maximos_premissa_V_natural_zero'])))
            w('      Leitura: voto lançado em proporção ao estoque de faltosos do 2º turno faria o voto de Flávio do 1º turno')
            w('      "aparecer em Lula" na regressão, porque parte desse estoque é eleitor de Flávio que não voltou. Nas cinco')
            w('      UFs isso não aparece (V fica abaixo do resto do país). O limite vale só para essa forma pro rata: voto lançado')
            w('      em nome de quem já tinha faltado no 1º turno cai no coeficiente dos faltosos do 1º turno, igual à entrada')
            w('      de eleitor real, e este teste não separa as duas coisas.')
        e7 = E['E7_soma_por_uf']
        w('  E7. Soma por UF de D x votos de Flávio no 1º turno (universo): %s votos (ep %s), %s da margem contando em' % (
            _n(e7['todas_votos']), _n(e7['todas_ep']), _p(e7['todas_votos_pct_da_margem'])))
        w('      dobro. Só as UFs positivas: %s votos (%s); só as negativas: %s. Somar só as positivas é escolher depois' % (
            _n(e7['positivas_votos']), _p(e7['positivas_votos_pct_da_margem']), _n(e7['negativas_votos'])))
        w('      de ver; serve de teto grosseiro, não de estimativa.')
        w('')
    w('11. LEITURA, NOS DOIS SENTIDOS')
    w('  Contra a tese (troca de voto dentro da urna regulada pela força de Lula):')
    w('  a) Pela letra, SEM SINAL nas duas leituras, com poder: a forma do registro foi detectada em 200 de 200 sorteios,')
    w('     e também nas outras seis regras de concentração testadas (30 de 30 em cada).')
    w('  b) D é %s (ep %s) na Leitura A e %s (ep %s) na B: a parcela de Flávio que aparece em Lula onde Flávio é' % (
        _c(vA['D']), _u(vA['ep']), _c(vB['D']), _u(vB['ep'])))
    w('     fraco é igual ou menor que a do sentido contrário. A forma plantada daria %s.' % _c(c1a['sorteios']['D_media']))
    w('  c) Nas cinco UFs em que o eleitor de Flávio mais deixou de voltar (PI, MA, TO, PB, CE), a parcela dele que')
    w('     aparece em Lula onde ele é fraco é 0,7% (ep 0,4), abaixo do resto do país (2,8%, ep 0,3). O que aparece')
    w('     ali é comparecimento, não troca (exploratório E5).')
    w('  d) O plantio espelho se comporta de modo simétrico; o critério invertido não dispara nos dados brutos.')
    w('  A favor da tese, ou limitando o que o resultado exclui:')
    w('  e) O teste não decide o canal do comparecimento. É cego para eleitor de Flávio registrado como ausente quando')
    w('     a taxa é igual dentro do local, e para voto lançado em nome de quem já tinha faltado no 1º turno. Só a')
    w('     forma pro rata do estoque de faltosos do 2º turno mexeria em V (E9 e E10). O indício da Onda A continua aberto.')
    w('  f) O "sem sinal" depende da premissa de que, sem desvio, D seria zero. Em 2014, 2018 e 2022 o mesmo D foi')
    w('     +0,047, -0,051 e -0,049. Contra 2018 e 2022, o valor de 2026 fica cerca de 0,05 acima (seção 10, E2).')
    w('  g) Com efeito fixo de município a mesma estatística dispara (seção 6 e E1), com as ressalvas ditas.')
    w('  h) Entre UFs, D é heterogêneo e cresce com a força de Lula (correlação %s); é positivo a mais de 2 ep em %s.' % (
        _c(ru['correlacao_D_com_fatia_de_Lula'], 2), ', '.join(ru['ufs_positivas_a_2ep'])))
    w('  i) No Sudeste, na Leitura A, o critério dispararia sozinho (exploratório E5), valendo poucos votos.')
    w('  j) Entrada de eleitores para Lula com taxa que acompanha a fatia de Lula da seção rebaixa V; se existir nos')
    w('     dados, sem a premissa do espelho o teto do teste chega ao que vira o resultado (seção 9). Com taxa igual')
    w('     dentro do local o efeito é o contrário (E9).')
    w('')
    w('12. DESVIOS E DECISÕES (o que o registro não fixa; tudo escrito no docstring antes de calcular)')
    w('  1. "Força de Flávio no local" tem duas leituras (local de votação, como no T35; seção, como no exploratório).')
    w('     Calculei as duas com veredito completo; deram o mesmo veredito.')
    w('  2. Universo: aptos iguais nos dois turnos, com o exterior (o do exploratório). Variantes ao lado.')
    w('  3. Erro de D pela contribuição de cada local às duas estimativas; "a mais de 4 ep" lido a partir de zero.')
    w('  4. "Detectada" = o critério de sinal dispara com a forma plantada (valor esperado e 95% de 200 sorteios).')
    w('  5. Regra de concentração C1 (taxa proporcional à fatia de Lula na seção, total esperado exato de 2.136.651),')
    w('     mais seis regras ao lado. No exploratório do conferente o total de 2.136.651 foi o resultado de um sorteio')
    w('     com taxa média de 3,57%; aqui é o valor esperado, e cada sorteio fica a poucas centenas de votos dele.')
    w('  6. Explicações pelo comparecimento plantadas: abstenção concentrada, abstenção uniforme de 3,6%, entrada')
    w('     concentrada, as duas juntas, e troca mais entrada como estresse.')
    w('  7. Regra do SEM PODER e a leitura mais frouxa de "detectada" (não mudou nada).')
    w('  8. A correlação de D por UF com a fatia de Lula estava no código antes da primeira rodada, mas não no docstring.')
    w('  Depois de ver os resultados (exploratório, seção 10): E1 a E10. A parte registrada saiu idêntica na primeira')
    w('  rodada (06:38 UTC, antes do exploratório existir) e na final.')
    w('')
    w('13. CONTAGEM DE TESTES')
    nvar = sum(1 for k, o in R['variantes'].items() for nome in ('A_local', 'B_secao'))
    ndis = sum(1 for k, o in R['variantes'].items() for nome in ('A_local', 'B_secao') if o[nome]['sinal'])
    w('  Um critério de decisão registrado, em duas leituras: zero disparos. Ao lado, %d variantes (7 especificações x 2' % nvar)
    w('  leituras): %d disparam (as duas com efeito fixo de município). A 4 erros-padrão o acaso de amostra daria perto' % ndis)
    w('  de zero disparos em 16; o disparo da variante de município não é acaso de amostra, é diferença de especificação.')
    w('  No exploratório há dezenas de recortes (27 UFs, 5 regiões, 4 anos, 2 leituras); os destaques dele não contam.')
    txt = '\n'.join(L) + '\n'
    assert chr(0x2013) not in txt and chr(0x2014) not in txt
    with open(SAIDA_TXT, 'w') as f:
        f.write(txt)


if __name__ == '__main__':
    if len(sys.argv) > 1 and sys.argv[1] == 'texto':
        with open(SAIDA_JSON) as f:
            escrever_texto(json.load(f))
    else:
        rodar()
