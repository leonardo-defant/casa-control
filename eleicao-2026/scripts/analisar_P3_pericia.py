"""P3 do pré-registro, Adendo 26 (commit 5174ff5, 07/11/2026 13:57:56 UTC): padrões usados em perícia eleitoral nos
quatro anos (2014, 2018, 2022, 2026) e nos dois turnos, sem o exterior, com veredito por ano. Checagem da postagem
"2014 parecida com 2026" (@FelipeCecilio_, X; republicada no Instagram felipececilio.reserva).
Escrito antes de calcular qualquer número de P3 (07/11/2026, cerca de 14h15 UTC).

O QUE O REGISTRO FIXA (letra do Adendo 26, P3)
- Último dígito: votos do candidato do PT e do adversário por seção, só seções com 50 votos ou mais daquele candidato;
  qui-quadrado contra a uniforme.
- Canto de enchimento de urna (Klimek e outros, 2012): fração de seções com comparecimento de 95% ou mais dos aptos e
  fatia do PT de 90% ou mais entre os finalistas.
- Comparecimento e virada: dentro do município, correlação entre a variação da taxa de comparecimento e a virada do PT
  do 1º para o 2º turno, por seção.
- Sinal, por ano: último dígito com p abaixo de 0,001 e alguma frequência a mais de 0,5 ponto de 10%; ou canto acima de
  3 vezes a média dos outros três anos no mesmo turno; ou correlação de 0,10 ou mais a mais de 4 erros-padrão. Sem
  sinal: nenhum dos três. A semelhança de 2014 com 2026 nesses padrões só pesa se 2026 tiver sinal.

SABIDO ANTES DE ESCREVER ESTE SCRIPT (não é resultado de P3)
- F2 (Adendo 20) já rodou o último dígito de 2026 (Lula e Flávio, dois turnos, contagens de 50 ou mais, seções do Brasil
  com os dois turnos, quase o mesmo universo daqui): p teórico (9 gl) de 0,155 (Lula, 2º turno) a 3,2e-21 (Lula, 1º
  turno); a frequência mais longe de 10% foi a do dígito 9 de Lula no 1º turno, 9,69% (0,31 ponto). Ou seja, já se sabe
  que em 2026 o p fica abaixo de 0,001 em três das quatro séries e que nenhuma frequência passou de 0,5 ponto naquele
  universo. Para 2014, 2018 e 2022 o último dígito nunca foi rodado.
- T28 (Adendo 9) rodou, em 2022 e 2026, um canto parecido (comparecimento de 95% ou mais e fatia de 80% ou mais, só
  seções com 100 aptos ou mais, contra um esperado por beta-binomial): sem sinal. O canto de 90% e a comparação crua
  entre os quatro anos nunca foram feitos. 2014 e 2018 nunca entraram num canto.
- F15 (Adendo 21) deu, entre zonas da mesma UF, coeficiente de 0,07 (ep 0,068 agrupado por UF) da virada de Lula sobre a
  variação do comparecimento da zona em 2026. Por seção, dentro do município, e nos outros anos, nunca foi rodado.
- F21 (Adendo 23) e o enunciado da tarefa: curva por faixa de 2026 parecida com a de 2014; erro das pesquisas no PT.
- Não vi nenhum número de P1 nem de P2.

O QUE O REGISTRO NÃO FIXA, DECIDIDO AQUI ANTES DE CALCULAR (relatado como desvio)
D1. Universo de cada turno: seções da base do ano que têm aquele turno, com UF diferente de ZZ (exterior fora), tipo
    "apurada" (sem distinguir maiúsculas) e aptos > 0. Seções anuladas saem e são contadas (nas bases elas têm L = R =
    0, então sairiam de qualquer forma). Cada turno usa todas as suas seções; os anos não são ligados entre si e os dois
    turnos não precisam ter as mesmas seções (só a parte 3 liga os turnos).
D2. Candidatos: L = candidato do PT (Dilma 13, Haddad 13, Lula 13, Lula 13), R = adversário no 2º turno (Aécio 45,
    Bolsonaro 17, Bolsonaro 22, Flávio 22). No 1º turno, L e R são os votos desses mesmos dois no 1º turno (campos L e
    R do turno '1' da base). Os outros nominais (O) e o 28 cassado de 2026 não entram em nada de P3.
D3. Último dígito, por ano, turno e candidato (16 séries): só as contagens do candidato de 50 ou mais (cada série com o
    seu corte). Frequência de cada dígito de 0 a 9; qui-quadrado de Pearson contra 10% em cada dígito, 9 graus de
    liberdade; p por scipy.stats.chi2.sf e log10 de p por chi2.logsf (p pode ficar abaixo do menor número
    representável). Maior desvio = max |100 f_d - 10|, em pontos, com o dígito. Erro-padrão binomial de cada frequência,
    raiz(f(1-f)/n), só descritivo. Condição da série: p < 0,001 E maior desvio > 0,5 ponto (estrito), as duas na MESMA
    série (mesmo candidato e mesmo turno). O registro põe o adversário dentro do teste do último dígito ("votos do
    candidato do PT e do adversário"), então as quatro séries do ano (L e R, 1º e 2º turnos) contam para o veredito do
    ano; isso não é exploratório. Sem simulação: o registro de P3 fixa a uniforme (não a régua simulada do F2).
D4. Canto: comparecimento/aptos >= 0,95 calculado em inteiros (100 comp >= 95 apt); fatia L/(L+R) >= 0,90 em inteiros
    (10 L >= 9 (L+R)). Denominador: seções do universo do turno com L+R > 0 (onde a fatia existe); robustez com todas
    as seções do universo do turno no denominador (relatada, fora do veredito). Razão = fração do ano / média simples das
    frações dos outros três anos no mesmo turno. Condição: razão > 3 (estrito), em qualquer dos dois turnos. Se a média
    dos outros três for zero, a razão é infinita quando a fração do ano é positiva (cumpre) e indefinida quando também
    é zero (não cumpre). Erro-padrão da fração agrupado por município (média de indicadores, CR1, G/(G-1)); da razão
    pelo método delta, com os anos independentes. Os dois erros-padrão são descritivos: o veredito usa o número pontual.
D5. Comparecimento e virada: seções com a mesma chave UF|município|zona|seção nos dois turnos, as duas apuradas, aptos
    > 0 e L+R > 0 nos dois turnos. x = comp2/apt2 - comp1/apt1 e y = L2/(L2+R2) - L1/(L1+R1), em frações (não em
    pontos). Município = UF|código do município da base. Correlação dentro do município: x e y menos a média do
    município (lib.demean) com peso L2+R2 (versão ponderada) e com peso 1 (versão sem peso);
    r = soma w xd yd / raiz(soma w xd^2 x soma w yd^2). Erro-padrão primário, fixado aqui: regressão padronizada com
    erro agrupado por município, lib.fe_ols(y/sy, x/sx, município, w), com sx = raiz(soma w xd^2 / soma w) e sy idem;
    o coeficiente é igual a r (conferido e relatado). Robustez declarada antes, fora do veredito: bootstrap de
    municípios, 2.000 reamostragens com reposição (o município inteiro entra ou sai; a média do município não muda, então
    r de cada reamostragem sai das somas por município), numpy SeedSequence(20261107).spawn(8), PCG64, um fluxo por ano e
    peso na ordem 2014 ponderada, 2014 sem peso, 2018 ponderada, ..., 2026 sem peso; ep = desvio-padrão das 2.000
    (ddof 1). Condição: r >= 0,10 E r / ep > 4 (estrito), com o ep primário; cumpre se a versão ponderada OU a sem peso
    cumprir (as duas são relatadas, e o que cada uma diria sozinha). Para leitura (fora do veredito):
    lib.fe_ols(y, x, local, w = L2+R2), local = lib.chave_local com o local do 2º turno, erro agrupado por local.
D6. Veredito por ano: SINAL se qualquer condição acontecer (D3 em qualquer das quatro séries; D4 em qualquer dos dois
    turnos; D5 em qualquer dos dois pesos). SEM SINAL se nenhuma. O veredito por ano cobre os dois turnos, porque o
    título de P3 diz "nos dois turnos" e o canto é comparado "no mesmo turno"; relata-se qual série, turno ou peso bateu.
D7. Leitura do registro: a semelhança de 2014 com 2026 nesses padrões só pesa se 2026 tiver SINAL. Se 2026 der SEM
    SINAL, a semelhança não pesa, qualquer que seja o resultado de 2014. Se 2026 der SINAL, diz-se se 2014 também deu e
    por qual condição.
D8. Ao lado, exploratório (pedido na tarefa, fora do registro e fora do veredito, mas fixado aqui antes de rodar):
    (a) canto do adversário: R/(L+R) >= 0,90 em inteiros, mesmo comparecimento e denominador de D4, mesma regra de razão
    > 3; (b) correlação do lado do adversário: y_R = R2/(L2+R2) - R1/(L1+R1) = -y, então r_R = -r com o mesmo ep;
    mesma regra (r_R >= 0,10 e r_R / ep > 4, ponderada ou sem peso); (c) contagem de seções com comparecimento >= 95%
    sozinha, fração e razão sobre a média dos outros três anos no mesmo turno (descritivo). O último dígito já cobre os
    dois lados pela letra (D3) e aparece separado por candidato na tabela.
D9. Os limiares são comparados com os números sem arredondar; o texto arredonda só na impressão.
D10. Erros-padrão: as frações e contagens são sobre todas as seções (população inteira); os erros-padrão relatados tratam
    as seções como sorteio de um processo (binomial no dígito, agrupado por município no canto e na correlação, por local
    na regressão de leitura).

ALTERAÇÕES DEPOIS DE RODAR (07/11/2026, depois da rodada 1 das 14h16 UTC; D1 a D10 ficaram como estavam; cópia do
docstring original, com sha1 e hora, em /home/user/trabalho-eleicao/adendo26/P3/docstring_antes_de_rodar.txt)
- A leitura passou a guardar também O, c28, o local e a chave de cada seção em cada turno, só para o bloco exploratório;
  nenhuma conta registrada mudou (conferido: os números das partes 1 a 3 da rodada 2 são iguais aos da rodada 1).
- Bloco EXPLORATÓRIO, decidido DEPOIS de ver que o último dígito bateu em Aécio (2014, 1º turno, dígito 0) e Haddad
  (2018, 1º turno, dígito 0) e que o canto bateu no PT em 2014 (1º turno) e, no lado do adversário, em 2018. Fora do
  veredito e da leitura:
  E1. Régua simulada do último dígito, no modelo do F2 (D4 do F2): em cada ano e turno, 200 sorteios; válidos V = L+R+O
      menos c28; fatias do local (lib.chave_local, todas as seções do local no mesmo turno, a própria incluída);
      L* ~ Bin(V, pL); R* ~ Bin(V - L*, pR/(1 - pL)) (no 2º turno R* = V - L*); mesmo corte de 50 em cada sorteio.
      Semente numpy SeedSequence(2026110726).spawn(8), PCG64, um fluxo por ano e turno na ordem 2014 1º, 2014 2º, ...,
      2026 2º. Relata, por série, quantos sorteios cumprem a regra do registro (p < 0,001 e desvio > 0,5 ponto) e onde o
      observado cai na distribuição simulada do qui-quadrado, do maior desvio e da frequência do dígito 0.
  E2. Último dígito só com contagens de 100 ou mais (descritivo).
  E3. Onde estão as seções dos cantos que passaram da razão 3 (PT em 2014, 1º turno; adversário em 2018, 1º e 2º
      turnos) e, para comparação, o canto do PT no 2º turno de 2026: por UF, municípios com mais seções, quantas estão
      no mesmo canto no outro turno, e comparecimento e fatia médios delas no outro turno. Acrescentado na rodada 3,
      depois de ver na rodada 2 que 175 das 433 seções do canto do PT de 2014 (1º turno) estão em PE|25313 (Recife, nome
      de resultados/T23_bweb.txt): as fatias médias do PT, do adversário e dos outros nos válidos do próprio turno.
  E4. (rodada 3, mesmo motivo) Para o município com mais seções de cada canto: seções com comparecimento >= 95% e
      comparecimento agregado do município em cada ano e turno (municípios seguidos pelo código UF|município do TSE).
- Rodada 4: só texto. Seções "O que isso significa" (leitura escrita depois de rodar, com os números puxados dos
  resultados), "Desvios" e "Fontes" (inclui a página do CJF de 07/03/2013 sobre a revisão biométrica de Recife, lida em
  07/11/2026). Nenhuma conta nova.

Uso:
  python3 -I analisar_P3_pericia.py <secoes2014.json.gz> <secoes2018.json.gz> <secoes2022.json.gz>
          <secoes2026.json.gz> <saida.json> <saida.txt>
"""
import os as _os, sys as _sys
_sys.path.insert(0, _os.path.dirname(_os.path.abspath(__file__)))
import json, sys, math
import numpy as np
from scipy.stats import chi2 as _chi2
from lib import carregar, chave_local, demean, fe_ols

ANOS = [2014, 2018, 2022, 2026]
TURNOS = ['1', '2']
CAND = {2014: ('Dilma', 'Aécio'), 2018: ('Haddad', 'Bolsonaro'), 2022: ('Lula', 'Bolsonaro'), 2026: ('Lula', 'Flávio')}
MIN_DIG = 50
LIM_P, LIM_DESVIO = 0.001, 0.5
LIM_CANTO = 3.0
LIM_R, LIM_Z = 0.10, 4.0
SEMENTE, NBOOT = 20261107, 2000


# ------------------------------------------------------------------------------------------------ leitura
def apurada(s):
    return str(s.get('tipo', '')).strip().lower() == 'apurada'


def ler_ano(caminho):
    d = carregar(caminho)
    T = {t: {'L': [], 'R': [], 'comp': [], 'apt': [], 'mun': [], 'O': [], 'c28': [], 'loc': [], 'k': []} for t in TURNOS}
    P = {c: [] for c in ('L1', 'R1', 'c1', 'a1', 'L2', 'R2', 'c2', 'a2', 'mun', 'loc')}
    cont = {'chaves': len(d), 'exterior': 0}
    for t in TURNOS:
        cont[f'sem_turno_{t}'] = 0
        cont[f'nao_apurada_{t}'] = 0
        cont[f'aptos_zero_{t}'] = 0
    cont['par_sem_os_dois_turnos'] = 0
    cont['par_fora_apurada_aptos_LR'] = 0
    for k, v in d.items():
        uf, mun, _, _ = k.split('|')
        if uf == 'ZZ':
            cont['exterior'] += 1
            continue
        m = f'{uf}|{mun}'
        for t in TURNOS:
            if t not in v:
                cont[f'sem_turno_{t}'] += 1
                continue
            s = v[t]
            if not apurada(s):
                cont[f'nao_apurada_{t}'] += 1
                continue
            if s['apt'] <= 0:
                cont[f'aptos_zero_{t}'] += 1
                continue
            T[t]['L'].append(s['L']); T[t]['R'].append(s['R'])
            T[t]['comp'].append(s['comp']); T[t]['apt'].append(s['apt']); T[t]['mun'].append(m)
            T[t]['O'].append(s['O']); T[t]['c28'].append(s.get('c28', 0))
            T[t]['loc'].append(chave_local(k, s)); T[t]['k'].append(k)
        if '1' not in v or '2' not in v:
            cont['par_sem_os_dois_turnos'] += 1
            continue
        a, b = v['1'], v['2']
        if not (apurada(a) and apurada(b) and a['apt'] > 0 and b['apt'] > 0
                and a['L'] + a['R'] > 0 and b['L'] + b['R'] > 0):
            cont['par_fora_apurada_aptos_LR'] += 1
            continue
        P['L1'].append(a['L']); P['R1'].append(a['R']); P['c1'].append(a['comp']); P['a1'].append(a['apt'])
        P['L2'].append(b['L']); P['R2'].append(b['R']); P['c2'].append(b['comp']); P['a2'].append(b['apt'])
        P['mun'].append(m); P['loc'].append(chave_local(k, b))
    del d
    for t in TURNOS:
        for c in ('L', 'R', 'comp', 'apt', 'O', 'c28'):
            T[t][c] = np.asarray(T[t][c], dtype=np.int64)
        for c in ('mun', 'loc', 'k'):
            T[t][c] = np.asarray(T[t][c])
        cont[f'universo_{t}'] = int(len(T[t]['L']))
    for c in ('L1', 'R1', 'c1', 'a1', 'L2', 'R2', 'c2', 'a2'):
        P[c] = np.asarray(P[c], dtype=np.int64)
    P['mun'] = np.asarray(P['mun']); P['loc'] = np.asarray(P['loc'])
    cont['pares'] = int(len(P['L1']))
    return T, P, cont


# ------------------------------------------------------------------------------------------------ 1. último dígito
def digito(v):
    v = np.asarray(v, dtype=np.int64)
    v = v[v >= MIN_DIG]
    n = int(len(v))
    cnt = np.bincount(v % 10, minlength=10).astype(float)
    f = cnt / n
    E = n / 10.0
    x2 = float(((cnt - E) ** 2 / E).sum())
    p = float(_chi2.sf(x2, 9))
    log10p = float(_chi2.logsf(x2, 9) / math.log(10))
    desv = 100 * f - 10
    j = int(np.argmax(np.abs(desv)))
    ep = 100 * np.sqrt(f * (1 - f) / n)
    cond_p = p < LIM_P
    cond_d = abs(desv[j]) > LIM_DESVIO
    return {'n': n, 'contagens': cnt.astype(int).tolist(), 'freq_pct': (100 * f).tolist(), 'ep_freq_pts': ep.tolist(),
            'qui2': x2, 'gl': 9, 'p': p, 'log10_p': log10p,
            'maior_desvio_pts': float(abs(desv[j])), 'maior_desvio_com_sinal_pts': float(desv[j]), 'digito_maior_desvio': j,
            'cond_p_menor_0001': bool(cond_p), 'cond_desvio_maior_05': bool(cond_d), 'cumpre': bool(cond_p and cond_d)}


# ------------------------------------------------------------------------------------------------ 2. canto
def frac_agrupada(ind, g):
    """Fração de indicadores e erro-padrão agrupado (CR1) por grupo."""
    ind = np.asarray(ind, float)
    N = len(ind)
    p = float(ind.mean())
    G = int(g.max() + 1)
    e = np.bincount(g, weights=ind - p, minlength=G)
    var = G / (G - 1) * float((e ** 2).sum()) / N ** 2
    return p, math.sqrt(var), G


def canto_turno(Tt):
    L, R, comp, apt = Tt['L'], Tt['R'], Tt['comp'], Tt['apt']
    _, g_all = np.unique(Tt['mun'], return_inverse=True)
    lr = (L + R) > 0
    alto = 100 * comp >= 95 * apt
    pt = lr & alto & (10 * L >= 9 * (L + R))
    adv = lr & alto & (10 * R >= 9 * (L + R))
    _, g = np.unique(Tt['mun'][lr], return_inverse=True)
    out = {'secoes_universo': int(len(L)), 'secoes_LR_pos': int(lr.sum()), 'secoes_LR_zero': int((~lr).sum())}
    for nome, ind in (('canto_PT', pt), ('canto_adversario', adv), ('comp95', alto)):
        f, ep, G = frac_agrupada(ind[lr], g)
        f_all, ep_all, _ = frac_agrupada(ind, g_all)
        out[nome] = {'n': int(ind[lr].sum()), 'fracao': f, 'ep': ep, 'municipios': G,
                     'n_denominador_todas': int(ind.sum()), 'fracao_denominador_todas': f_all, 'ep_denominador_todas': ep_all}
    return out


def razoes_canto(C, chave, campo='fracao', ep_campo='ep'):
    """Para cada ano e turno: fração do ano / média simples das frações dos outros três anos no mesmo turno."""
    R = {}
    for t in TURNOS:
        R[t] = {}
        for a in ANOS:
            fa, va = C[a][t][chave][campo], C[a][t][chave][ep_campo] ** 2
            outros = [b for b in ANOS if b != a]
            fo = [C[b][t][chave][campo] for b in outros]
            vo = [C[b][t][chave][ep_campo] ** 2 for b in outros]
            m = sum(fo) / 3.0
            vm = sum(vo) / 9.0
            if m > 0:
                r = fa / m
                vr = (va + r ** 2 * vm) / m ** 2  # delta: d(fa/m) = dfa/m - fa dm/m^2
                ep = math.sqrt(vr)
                cumpre = r > LIM_CANTO
            else:
                r = float('inf') if fa > 0 else float('nan')
                ep = float('nan')
                cumpre = fa > 0
            R[t][a] = {'fracao': fa, 'media_outros_tres': m, 'razao': r, 'ep_razao': ep, 'cumpre_razao_maior_3': bool(cumpre)}
    return R


# ------------------------------------------------------------------------------------------------ 3. comparecimento e virada
def corr_dentro(x, y, g, w, rng):
    Z = demean(np.column_stack([x, y]), g, w)
    xd, yd = Z[:, 0], Z[:, 1]
    sxy = float((w * xd * yd).sum()); sxx = float((w * xd * xd).sum()); syy = float((w * yd * yd).sum())
    r = sxy / math.sqrt(sxx * syy)
    W = float(w.sum())
    sx, sy = math.sqrt(sxx / W), math.sqrt(syy / W)
    reg = fe_ols(y / sy, x / sx, g, w=w, nomes=['x'])
    b, ep = reg['coef']['x'], reg['ep']['x']
    G = int(g.max() + 1)
    Sxy = np.bincount(g, weights=w * xd * yd, minlength=G)
    Sxx = np.bincount(g, weights=w * xd * xd, minlength=G)
    Syy = np.bincount(g, weights=w * yd * yd, minlength=G)
    rb = np.empty(NBOOT)
    for i in range(NBOOT):
        c = np.bincount(rng.integers(0, G, G), minlength=G).astype(float)
        rb[i] = (c @ Sxy) / math.sqrt((c @ Sxx) * (c @ Syy))
    ep_b = float(rb.std(ddof=1))
    z = r / ep
    cum_pt = (r >= LIM_R) and (z > LIM_Z)
    cum_adv = (-r >= LIM_R) and (-z > LIM_Z)
    return {'r': r, 'coef_regressao_padronizada': b, 'dif_r_menos_coef': r - b, 'ep_agrupado_municipio': ep, 'z': z,
            'n_regressao': reg['n'], 'municipios_regressao': reg['grupos'],
            'ep_bootstrap': ep_b, 'z_bootstrap': r / ep_b, 'boot_p2_5': float(np.percentile(rb, 2.5)),
            'boot_p97_5': float(np.percentile(rb, 97.5)),
            'cumpre_PT': bool(cum_pt), 'cumpre_PT_com_ep_bootstrap': bool((r >= LIM_R) and (r / ep_b > LIM_Z)),
            'r_adversario': -r, 'z_adversario': -z, 'cumpre_adversario_exploratorio': bool(cum_adv)}


def comparecimento_virada(P, ss):
    L1, R1, c1, a1 = (P[c].astype(float) for c in ('L1', 'R1', 'c1', 'a1'))
    L2, R2, c2, a2 = (P[c].astype(float) for c in ('L2', 'R2', 'c2', 'a2'))
    x = c2 / a2 - c1 / a1
    y = L2 / (L2 + R2) - L1 / (L1 + R1)
    _, g = np.unique(P['mun'], return_inverse=True)
    w2 = L2 + R2
    out = {'secoes': int(len(x)), 'municipios': int(g.max() + 1),
           'media_x': float(x.mean()), 'media_y': float(y.mean()),
           'media_x_pond': float((w2 * x).sum() / w2.sum()), 'media_y_pond': float((w2 * y).sum() / w2.sum())}
    out['ponderada'] = corr_dentro(x, y, g, w2, np.random.Generator(np.random.PCG64(ss[0])))
    out['sem_peso'] = corr_dentro(x, y, g, np.ones_like(x), np.random.Generator(np.random.PCG64(ss[1])))
    reg = fe_ols(y, x, P['loc'], w=w2, nomes=['x'])
    out['leitura_dentro_do_local'] = {'coef': reg['coef']['x'], 'ep_agrupado_local': reg['ep']['x'],
                                      't': reg['coef']['x'] / reg['ep']['x'], 'n': reg['n'], 'locais': reg['grupos']}
    out['cumpre_PT'] = bool(out['ponderada']['cumpre_PT'] or out['sem_peso']['cumpre_PT'])
    out['cumpre_adversario_exploratorio'] = bool(out['ponderada']['cumpre_adversario_exploratorio']
                                                 or out['sem_peso']['cumpre_adversario_exploratorio'])
    return out


# ------------------------------------------------------------------------------------------------ EXPLORATÓRIO (depois de rodar)
SEMENTE_EXP, NSIM = 2026110726, 200


def _stats_dig(v, minv=MIN_DIG):
    v = v[v >= minv]
    n = len(v)
    cnt = np.bincount(v % 10, minlength=10).astype(float)
    E = n / 10.0
    x2 = float(((cnt - E) ** 2 / E).sum())
    f = 100 * cnt / n
    return x2, float(np.abs(f - 10).max()), float(f[0]), n


def e1_sim_digito(Tt, turno, rng):
    """E1: régua simulada do último dígito (modelo do F2): fatias do local, mesmos válidos."""
    L, R, O, c28 = Tt['L'], Tt['R'], Tt['O'], Tt['c28']
    assert (O >= c28).all()
    V = L + R + O - c28
    _, gl = np.unique(Tt['loc'], return_inverse=True)
    sV = np.bincount(gl, weights=V.astype(float)); sL = np.bincount(gl, weights=L.astype(float))
    sR = np.bincount(gl, weights=R.astype(float))
    den = np.where(sV > 0, sV, 1.0)
    pL = np.clip((sL / den)[gl], 0, 1); pR = np.clip((sR / den)[gl], 0, 1)
    q = np.clip(np.where(pL < 1, pR / np.where(pL < 1, 1 - pL, 1), 0), 0, 1)
    sims = {'L': [], 'R': []}
    for _ in range(NSIM):
        Ls = rng.binomial(V, pL)
        Rs = V - Ls if turno == '2' else rng.binomial(V - Ls, q)
        sims['L'].append(_stats_dig(Ls)); sims['R'].append(_stats_dig(Rs))
    out = {}
    for c, obs_v in (('L', L), ('R', R)):
        x2o, mdo, f0o, n = _stats_dig(obs_v)
        S = np.array([s[:3] for s in sims[c]])
        ps = _chi2.sf(S[:, 0], 9)
        cum = (ps < LIM_P) & (S[:, 1] > LIM_DESVIO)
        out[c] = {'n_obs': n, 'qui2_obs': x2o, 'qui2_sim_media': float(S[:, 0].mean()),
                  'qui2_sim_p99_9': float(np.percentile(S[:, 0], 99.9)), 'sims_qui2_maior_igual': int((S[:, 0] >= x2o).sum()),
                  'maior_desvio_obs': mdo, 'maior_desvio_sim_media': float(S[:, 1].mean()),
                  'maior_desvio_sim_max': float(S[:, 1].max()), 'sims_desvio_maior_igual': int((S[:, 1] >= mdo).sum()),
                  'freq0_obs': f0o, 'freq0_sim_media': float(S[:, 2].mean()), 'freq0_sim_dp': float(S[:, 2].std(ddof=1)),
                  'z_freq0': float((f0o - S[:, 2].mean()) / S[:, 2].std(ddof=1)),
                  'sims_que_cumprem_a_regra': int(cum.sum()), 'sims': NSIM}
    return out


def e2_digito100(Tt):
    out = {}
    for c in ('L', 'R'):
        v = Tt[c][Tt[c] >= 100]
        n = int(len(v))
        cnt = np.bincount(v % 10, minlength=10).astype(float)
        E = n / 10.0
        x2 = float(((cnt - E) ** 2 / E).sum())
        desv = 100 * cnt / n - 10
        j = int(np.argmax(np.abs(desv)))
        out[c] = {'n': n, 'qui2': x2, 'p': float(_chi2.sf(x2, 9)), 'log10_p': float(_chi2.logsf(x2, 9) / math.log(10)),
                  'maior_desvio_com_sinal_pts': float(desv[j]), 'digito': j,
                  'cumpriria_a_regra': bool(_chi2.sf(x2, 9) < LIM_P and abs(desv[j]) > LIM_DESVIO)}
    return out


def e3_localiza(T):
    """E3: onde estão as seções de cada canto, e como elas ficaram no outro turno."""
    from collections import Counter
    idx = {t: {k: i for i, k in enumerate(T[t]['k'])} for t in TURNOS}
    out = {}
    for t in TURNOS:
        o = '2' if t == '1' else '1'
        Tt, To = T[t], T[o]
        lr = (Tt['L'] + Tt['R']) > 0
        alto = 100 * Tt['comp'] >= 95 * Tt['apt']
        for lado, X in (('PT', Tt['L']), ('adversario', Tt['R'])):
            ind = lr & alto & (10 * X >= 9 * (Tt['L'] + Tt['R']))
            sel = np.nonzero(ind)[0]
            n = int(len(sel))
            muns = Counter(Tt['mun'][sel].tolist())
            ufs = Counter(m.split('|')[0] for m in Tt['mun'][sel].tolist())
            top = muns.most_common(10)
            j = np.array([idx[o][k] for k in Tt['k'][sel].tolist() if k in idx[o]], dtype=np.int64)
            r = {'secoes': n, 'municipios': len(muns), 'locais': int(len(set(Tt['loc'][sel].tolist()))),
                 'por_UF': dict(ufs.most_common()), 'municipios_com_mais': [[m, c] for m, c in top],
                 'parte_top1': (top[0][1] / n) if n else None,
                 'parte_top5': (sum(c for _, c in top[:5]) / n) if n else None,
                 'parte_top10': (sum(c for _, c in top[:10]) / n) if n else None}
            if n:
                Ls, Rs = Tt['L'][sel].astype(float), Tt['R'][sel].astype(float)
                Xs = Ls if lado == 'PT' else Rs
                r['comparecimento_medio'] = float((Tt['comp'][sel] / Tt['apt'][sel]).mean())
                r['fatia_media'] = float((Xs / (Ls + Rs)).mean())
                r['votos_LR'] = int((Ls + Rs).sum())
                Vs = (Tt['L'][sel] + Tt['R'][sel] + Tt['O'][sel] - Tt['c28'][sel]).astype(float)
                Os = (Tt['O'][sel] - Tt['c28'][sel]).astype(float)
                r['fatia_PT_nos_validos_media'] = float((Ls / Vs).mean())
                r['fatia_adversario_nos_validos_media'] = float((Rs / Vs).mean())
                r['fatia_outros_nos_validos_media'] = float((Os / Vs).mean())
            if len(j):
                Lo, Ro, co, ao = To['L'][j], To['R'][j], To['comp'][j], To['apt'][j]
                Xo = Lo if lado == 'PT' else Ro
                lro = (Lo + Ro) > 0
                r['no_outro_turno'] = {
                    'achadas': int(len(j)),
                    'no_mesmo_canto': int((lro & (100 * co >= 95 * ao) & (10 * Xo >= 9 * (Lo + Ro))).sum()),
                    'comp95': int((100 * co >= 95 * ao).sum()),
                    'comparecimento_medio': float((co / ao).mean()),
                    'fatia_media': float((Xo[lro] / (Lo + Ro)[lro]).mean())}
            out[f'{t}_{lado}'] = r
    return out


def e4_municipios(T):
    """E4: por município e turno, seções e seções com comparecimento >= 95% (para seguir um município entre anos)."""
    out = {}
    for t in TURNOS:
        Tt = T[t]
        m, g = np.unique(Tt['mun'], return_inverse=True)
        n = np.bincount(g)
        n95 = np.bincount(g, weights=(100 * Tt['comp'] >= 95 * Tt['apt']).astype(float)).astype(int)
        sc = np.bincount(g, weights=Tt['comp'].astype(float)); sa = np.bincount(g, weights=Tt['apt'].astype(float))
        out[t] = {mm: [int(a), int(b), float(c / d)] for mm, a, b, c, d in zip(m.tolist(), n, n95, sc, sa)}
    return out


NOMES = {'PE|25313': 'Recife'}  # nome tirado de resultados/T23_bweb.txt; os outros códigos ficam sem nome


def texto_exploratorio(a_, E1, E2, E3, RZ, E4=None):
    a_('7. EXPLORATÓRIO, decidido DEPOIS de ver as partes 1 a 3 (fora do veredito e da leitura; ver o docstring)')
    a_('   E1. Último dígito contra contagens limpas simuladas (modelo do F2: binomial com a fatia do local, mesmos válidos;')
    a_(f'   {NSIM} sorteios por ano e turno). "Sorteios que cumprem" = quantos dos {NSIM} sorteios limpos cumprem a regra do registro.')
    a_('   ano  turno candidato     qui2 obs  sim média  sims>=obs | dígito 0 obs  sim média (dp)     z    | maior desvio obs  sim máx | sorteios que cumprem')
    for a in ANOS:
        for t in TURNOS:
            for c in ('L', 'R'):
                x = E1[a][t][c]
                nome = CAND[a][0] if c == 'L' else CAND[a][1]
                a_(f'   {a} {t}º    {nome:<10} {fn(x["qui2_obs"], 1):>9} {fn(x["qui2_sim_media"], 1):>9} {x["sims_qui2_maior_igual"]:>6}'
                   f'    | {fn(x["freq0_obs"], 3):>8}  {fn(x["freq0_sim_media"], 3)} ({fn(x["freq0_sim_dp"], 3)}) {fn(x["z_freq0"], 1):>6}'
                   f'  | {fn(x["maior_desvio_obs"], 3):>10}  {fn(x["maior_desvio_sim_max"], 3):>9} | {x["sims_que_cumprem_a_regra"]:>4} de {x["sims"]}')
    a_('   E2. Último dígito só com contagens de 100 ou mais (descritivo):')
    lin = []
    for a in ANOS:
        for t in TURNOS:
            for c in ('L', 'R'):
                x = E2[a][t][c]
                nome = CAND[a][0] if c == 'L' else CAND[a][1]
                lin.append(f'{a} {t}º {nome} {fn(x["maior_desvio_com_sinal_pts"], 3)} ({x["digito"]}), p {fp(x["p"], x["log10_p"])}'
                           + (' CUMPRIRIA' if x['cumpriria_a_regra'] else ''))
    for i in range(0, len(lin), 4):
        a_('     ' + '; '.join(lin[i:i + 4]))
    a_('   E3. Onde estão as seções dos cantos que passaram de 3 vezes, e o canto do PT no 2º turno de 2026 (comparação)')
    alvos = []
    for t in TURNOS:
        for a in ANOS:
            for lado, nome in (('PT', 'canto_PT'), ('adversario', 'canto_adversario')):
                if RZ[nome][t][a]['cumpre_razao_maior_3']:
                    alvos.append((a, t, lado))
    if (2026, '2', 'PT') not in alvos:
        alvos.append((2026, '2', 'PT'))
    for a, t, lado in alvos:
        r = E3[a][f'{t}_{lado}']
        oo = r.get('no_outro_turno', {})
        outro = '2º' if t == '1' else '1º'
        ufs = ', '.join(f'{u} {c}' for u, c in list(r['por_UF'].items())[:6])
        tops = ', '.join(f'{m} {c}' for m, c in r['municipios_com_mais'][:5])
        a_(f'   {a} {t}º turno, canto do {"PT" if lado == "PT" else "adversário"}: {fi(r["secoes"])} seções em {fi(r["municipios"])} municípios'
           f' e {fi(r["locais"])} locais; por UF: {ufs}; municípios com mais (UF|código): {tops};'
           f' os 5 primeiros somam {fn(100 * r["parte_top5"], 1)}% e os 10 primeiros {fn(100 * r["parte_top10"], 1)}%.'
           f' Comparecimento médio {fn(100 * r["comparecimento_medio"], 1)}%, fatia média {fn(100 * r["fatia_media"], 1)}%.'
           f' No {outro} turno: {oo.get("no_mesmo_canto", 0)} no mesmo canto, {oo.get("comp95", 0)} com comparecimento >= 95%,'
           f' comparecimento médio {fn(100 * oo.get("comparecimento_medio", float("nan")), 1)}%, fatia média {fn(100 * oo.get("fatia_media", float("nan")), 1)}%.'
           f' Nos válidos do próprio turno (média por seção): PT {fn(100 * r["fatia_PT_nos_validos_media"], 1)}%,'
           f' adversário {fn(100 * r["fatia_adversario_nos_validos_media"], 1)}%, outros {fn(100 * r["fatia_outros_nos_validos_media"], 1)}%.')
        if E4 is not None and r['municipios_com_mais']:
            mm = r['municipios_com_mais'][0][0]
            seq = []
            for b in ANOS:
                for tt in TURNOS:
                    x = E4[b][tt].get(mm)
                    if x:
                        seq.append(f'{b} {tt}º {fi(x[1])} de {fi(x[0])} (comparecimento {fn(100 * x[2], 1)}%)')
            a_(f'     {mm}{" (" + NOMES[mm] + ")" if mm in NOMES else ""}, seções com comparecimento >= 95% por ano e turno: ' + '; '.join(seq) + '.')


def texto_significado(a_, D, C, RZ, V, VER, E1, E2, E3, E4):
    """Leitura escrita DEPOIS de rodar (números puxados dos resultados)."""
    a_('O QUE ISSO SIGNIFICA (leitura escrita depois de rodar; o veredito acima é só a letra)')
    v26 = VER[2026]['veredito']
    a_(f'- 2026: {v26} nos três padrões e nos dois turnos. Último dígito: maior desvio de 10% de '
       f'{fn(max(D[2026][t][c]["maior_desvio_pts"] for t in TURNOS for c in "LR"), 3)} ponto (limiar 0,5); canto do PT '
       f'{fn(RZ["canto_PT"]["1"][2026]["razao"], 2)} vez a média dos outros três anos no 1º turno e '
       f'{fn(RZ["canto_PT"]["2"][2026]["razao"], 2)} no 2º (limiar 3); correlação comparecimento x virada '
       f'{fn(V[2026]["ponderada"]["r"], 3)} (ep {fn(V[2026]["ponderada"]["ep_agrupado_municipio"], 3)}) ponderada e '
       f'{fn(V[2026]["sem_peso"]["r"], 3)} sem peso (limiar 0,10). Pela regra do registro, a semelhança de 2014 com 2026 '
       f'nesses padrões não pesa.')
    d14 = max(D[2014]['2'][c]['maior_desvio_pts'] for c in 'LR')
    a_(f'- 2014 ({VER[2014]["veredito"]}) e 2018 ({VER[2018]["veredito"]}) só batem no 1º turno. No 2º turno de 2014, o turno '
       f'citado na postagem, nenhuma condição bate: maior desvio do dígito {fn(d14, 3)} ponto, canto do PT '
       f'{fn(RZ["canto_PT"]["2"][2014]["razao"], 2)} vez, correlação {fn(V[2014]["ponderada"]["r"], 3)} '
       f'(z {fn(V[2014]["ponderada"]["z"], 1)}). Ou seja, 2014 e 2026 não se parecem nesses padrões: 2014 bate no 1º turno, '
       f'2026 em nada.')
    xa, xh = E1[2014]['1']['R'], E1[2018]['1']['L']
    n100 = sum(E2[a][t][c]['cumpriria_a_regra'] for a in ANOS for t in TURNOS for c in 'LR')
    n100_26 = sum(E2[2026][t][c]['cumpriria_a_regra'] for t in TURNOS for c in 'LR')
    ser = [np.asarray(D[a][t][c]['freq_pct']) for a in ANOS for t in TURNOS for c in 'LR']
    n_desce = sum(1 for f in ser if f[0] > f[9] and np.polyfit(np.arange(10), f, 1)[0] < 0)
    a_(f'- Exploratório: os dois "sinais" de último dígito são o formato esperado de contagens limpas. Em {n_desce} das 16 séries '
       f'a frequência desce do dígito 0 para o 9 (0 acima de 9 e inclinação negativa), como acontece quando há mais seções '
       f'com 150 votos do que com 159; nos dois "sinais" o excesso está no 0. Contagens '
       f'limpas sorteadas com a fatia do local dão o dígito 0 de Aécio em {fn(xa["freq0_sim_media"], 2)}% (observado '
       f'{fn(xa["freq0_obs"], 2)}%) e o de Haddad em {fn(xh["freq0_sim_media"], 2)}% (observado {fn(xh["freq0_obs"], 2)}%); a '
       f'regra do registro bate em {xa["sims_que_cumprem_a_regra"]} e {xh["sims_que_cumprem_a_regra"]} de {NSIM} sorteios limpos. '
       f'Com o corte em 100 votos, {n100} das 16 séries cumpririam a regra, inclusive {n100_26} das 4 de 2026. A regra '
       f'(uniforme e 0,5 ponto) acusa candidatos com muitas contagens pequenas; não separa contagem limpa de mexida.')
    r14 = E3[2014]['1_PT']
    rec = E4[2014]['1'].get('PE|25313')
    rec_dep = [E4[b][t]['PE|25313'][2] for b in (2018, 2022, 2026) for t in TURNOS if 'PE|25313' in E4[b][t]]
    a_(f'- Exploratório: o canto do PT de 2014 (1º turno) tem {r14["municipios_com_mais"][0][1]} das {r14["secoes"]} seções em '
       f'Recife. Nelas o PT teve {fn(100 * r14["fatia_PT_nos_validos_media"], 1)}% dos válidos, Aécio '
       f'{fn(100 * r14["fatia_adversario_nos_validos_media"], 1)}% e os outros {fn(100 * r14["fatia_outros_nos_validos_media"], 1)}% '
       f'(a base não separa os outros por candidato; em Pernambuco a terceira candidata era Marina Silva, do PSB, que '
       f'substituiu Eduardo Campos): os 90% "entre os finalistas" vêm de tirar o '
       f'terceiro candidato da conta, não de 90% dos votos. O comparecimento de Recife foi {fn(100 * rec[2], 1)}% no 1º turno de '
       f'2014, contra {fn(100 * min(rec_dep), 1)}% a {fn(100 * max(rec_dep), 1)}% em 2018, 2022 e 2026; Recife estava na revisão '
       f'biométrica de 2013 e 2014 (CJF, 07/03/2013), que cancela títulos não revistos e encolhe os aptos. Isso é compatível '
       f'com o pico, mas o número de cancelados não foi conferido aqui. No 2º turno só {r14["no_outro_turno"]["no_mesmo_canto"]} '
       f'dessas seções ficaram no canto.')
    rb = E3[2018]['1_adversario']
    mm = rb['municipios_com_mais'][0][0]
    xb = E4[2018]['1'][mm]
    outros_b = [E4[b][t][mm][2] for b in (2014, 2022, 2026) for t in TURNOS if mm in E4[b][t]]
    adv_lados = [f'{a} ({", ".join(VER[a]["exploratorio_canto_adversario"])})' for a in ANOS if VER[a]['exploratorio_canto_adversario']]
    adv_cor = [a for a in ANOS if VER[a]['exploratorio_correlacao_adversario']]
    a_(f'- Exploratório, lado do adversário: o canto passa de 3 vezes em {"; ".join(adv_lados) or "nenhum ano"} (Bolsonaro, '
       f'{rb["secoes"]} seções no 1º turno, sobretudo SC e RS; o município com mais, {mm}, teve {xb[1]} de {xb[0]} seções com '
       f'95% ou mais e comparecimento de {fn(100 * xb[2], 1)}% em 2018, contra {fn(100 * min(outros_b), 1)}% a '
       f'{fn(100 * max(outros_b), 1)}% nos outros anos). Correlação do adversário de 0,10 ou mais: '
       f'{", ".join(map(str, adv_cor)) or "em nenhum ano"}. Os cantos que passam do limiar aparecem nos dois lados (PT em 2014, '
       f'direita em 2018) e seguem picos de comparecimento de municípios inteiros; nenhum dos três padrões passa do limiar '
       f'sempre a favor do mesmo lado.')
    xbo = E1[2018]['1']['R']
    a_(f'- Cético: (a) os cantos são frações de 0,01% a 0,1% das seções, e um município muda a razão (2014, 1º turno: '
       f'{fn(RZ["canto_PT"]["1"][2014]["razao"], 2)} com ep {fn(RZ["canto_PT"]["1"][2014]["ep_razao"], 2)}). (b) O último dígito '
       f'de Bolsonaro no 1º turno de 2018 tem qui-quadrado ({fn(xbo["qui2_obs"], 1)}) acima dos {NSIM} sorteios limpos (média '
       f'{fn(xbo["qui2_sim_media"], 1)}), mas o desvio máximo é {fn(xbo["maior_desvio_obs"], 2)} ponto, com o mesmo formato '
       f'decrescente, e não cumpre a regra; entre 16 séries, uma fora dos {NSIM} sorteios não é raro. (c) A correlação '
       f'comparecimento x virada muda de sinal entre os anos (2014 {fn(V[2014]["ponderada"]["r"], 3)}, 2018 '
       f'{fn(V[2018]["ponderada"]["r"], 3)}, 2022 {fn(V[2022]["ponderada"]["r"], 3)}, 2026 {fn(V[2026]["ponderada"]["r"], 3)}) '
       f'e fica longe de 0,10 em todos. (d) "Sem sinal" quer dizer que estes três padrões não acusam nada; não prova que a '
       f'eleição é limpa.')
    a_('')


def texto_desvios(a_):
    a_('DESVIOS (decisões que o registro não fixa, escritas no docstring antes de calcular, 07/11/2026 14:16:03 UTC)')
    for s in (
            'D1. Universo de cada turno: seções do Brasil apuradas e com aptos > 0; cada turno com todas as suas seções.',
            'D2. L = candidato do PT e R = adversário do 2º turno, nos dois turnos; outros nominais e o 28 de 2026 fora.',
            'D3. Último dígito: 16 séries (ano, turno, candidato); p < 0,001 e desvio > 0,5 ponto na mesma série; as quatro séries'
            ' do ano contam, porque o registro inclui o adversário no teste.',
            'D4. Canto em inteiros; denominador = seções com L+R > 0; razão sobre a média simples dos outros três anos; > 3 em'
            ' qualquer turno; ep agrupado por município e delta, descritivos.',
            'D5. Correlação ponderada (L2+R2) e sem peso; ep primário da regressão padronizada agrupada por município'
            ' (bootstrap de municípios ao lado); cumpre se uma das duas versões cumprir.',
            'D6. Veredito do ano cobre os dois turnos; SINAL se qualquer condição bater.',
            'D7 a D10. Leitura do registro aplicada só ao veredito de 2026; lado do adversário exploratório; limiares sem'
            ' arredondar; ep tratam as seções como sorteio de um processo.',
            'Depois de rodar: só o bloco 7 (E1 a E4) e estas leituras; nada nas partes 1 a 3 mudou (conferido entre as rodadas).'):
        a_('  ' + s)
    a_('')
    a_('FONTES')
    a_('  Bases por seção (bweb do TSE): 2014 adendo23/F21_base/secoes2014.json.gz (conferida contra o oficial no F21);'
       ' 2018 e 2022 dados_ref/; 2026 trab2t/secoes2026.json.gz.')
    a_('  Revisão biométrica de Recife: CJF, "Eleitores do DF serão os primeiros a realizar recadastramento biométrico",'
       ' 07/03/2013, https://www.cjf.jus.br/cjf/outras-noticias/2013/marco/eleitores-do-df-serao-os-primeiros-a-realizar-'
       'recadastramento-biometrico (lida em 07/11/2026; lista "PE Recife e outros 52 municípios, 2.438.008 eleitores", até'
       ' maio de 2014). Nome de PE|25313 (Recife): resultados/T23_bweb.txt.')
    a_('')


# ------------------------------------------------------------------------------------------------ formatação
def fn(x, k=2):
    if x is None or (isinstance(x, float) and math.isnan(x)):
        return 'indef.'
    if isinstance(x, float) and math.isinf(x):
        return 'infinita'
    s = f'{x:,.{k}f}'
    return s.replace(',', '#').replace('.', ',').replace('#', '.')


def fi(n):
    return f'{int(n):,}'.replace(',', '.')


def fp(p, log10p):
    if p >= 1e-4:
        return fn(p, 4)
    if p > 0:
        m, e = f'{p:.1e}'.split('e')
        return f'{m.replace(".", ",")}e{int(e)}'
    return f'10^{fn(log10p, 1)}'


def sn(b):
    return 'sim' if b else 'não'


# ------------------------------------------------------------------------------------------------ principal
def main():
    if len(sys.argv) != 7:
        print(__doc__.split('Uso:')[1]); sys.exit(1)
    caminhos = dict(zip(ANOS, sys.argv[1:5]))
    saida_json, saida_txt = sys.argv[5], sys.argv[6]
    ss = np.random.SeedSequence(SEMENTE).spawn(8)

    ss_exp = np.random.SeedSequence(SEMENTE_EXP).spawn(8)
    U, D, C, V = {}, {}, {}, {}
    E1, E2, E3, E4 = {}, {}, {}, {}
    for i, a in enumerate(ANOS):
        T, P, cont = ler_ano(caminhos[a])
        U[a] = cont
        D[a] = {t: {'L': digito(T[t]['L']), 'R': digito(T[t]['R'])} for t in TURNOS}
        C[a] = {t: canto_turno(T[t]) for t in TURNOS}
        V[a] = comparecimento_virada(P, ss[2 * i: 2 * i + 2])
        # exploratório (depois de rodar)
        E1[a] = {t: e1_sim_digito(T[t], t, np.random.Generator(np.random.PCG64(ss_exp[2 * i + j])))
                 for j, t in enumerate(TURNOS)}
        E2[a] = {t: e2_digito100(T[t]) for t in TURNOS}
        E3[a] = e3_localiza(T)
        E4[a] = e4_municipios(T)
        del T, P
        print(f'{a} lido: {cont}', file=sys.stderr)

    RZ = {nome: razoes_canto(C, nome) for nome in ('canto_PT', 'canto_adversario', 'comp95')}
    RZ_todas = {nome: razoes_canto(C, nome, 'fracao_denominador_todas', 'ep_denominador_todas')
                for nome in ('canto_PT', 'canto_adversario')}

    # veredito por ano
    VER = {}
    for a in ANOS:
        dig = [f'{CAND[a][0] if c == "L" else CAND[a][1]} ({c}), {t}º turno' for t in TURNOS for c in ('L', 'R')
               if D[a][t][c]['cumpre']]
        can = [f'{t}º turno' for t in TURNOS if RZ['canto_PT'][t][a]['cumpre_razao_maior_3']]
        cor = [nm for nm in ('ponderada', 'sem_peso') if V[a][nm]['cumpre_PT']]
        sinal = bool(dig or can or cor)
        VER[a] = {'veredito': 'SINAL' if sinal else 'SEM SINAL', 'digito': dig, 'canto_PT': can, 'correlacao_PT': cor,
                  'exploratorio_canto_adversario': [f'{t}º turno' for t in TURNOS
                                                    if RZ['canto_adversario'][t][a]['cumpre_razao_maior_3']],
                  'exploratorio_correlacao_adversario': [nm for nm in ('ponderada', 'sem_peso')
                                                         if V[a][nm]['cumpre_adversario_exploratorio']],
                  'robustez_canto_PT_denominador_todas': [f'{t}º turno' for t in TURNOS
                                                          if RZ_todas['canto_PT'][t][a]['cumpre_razao_maior_3']],
                  'robustez_correlacao_PT_ep_bootstrap': [nm for nm in ('ponderada', 'sem_peso')
                                                          if V[a][nm]['cumpre_PT_com_ep_bootstrap']]}
    if VER[2026]['veredito'] == 'SINAL':
        leitura = ('2026 tem SINAL pela letra; a semelhança de 2014 com 2026 nestes padrões pesa. 2014: '
                   + VER[2014]['veredito'] + '.')
    else:
        leitura = ('2026 SEM SINAL pela letra; pelo registro, a semelhança de 2014 com 2026 nestes padrões não pesa, '
                   'qualquer que seja o resultado de 2014 (2014: ' + VER[2014]['veredito'] + ').')

    res = {'registro': 'PRE-REGISTRO-2026-10-26.md, Adendo 26, P3 (commit 5174ff5, 07/11/2026 13:57:56 UTC)',
           'script': 'scripts/analisar_P3_pericia.py', 'fontes': {str(a): caminhos[a] for a in ANOS},
           'candidatos': {str(a): {'L': CAND[a][0], 'R': CAND[a][1]} for a in ANOS},
           'limiares': {'min_votos_digito': MIN_DIG, 'p': LIM_P, 'desvio_pts': LIM_DESVIO, 'razao_canto': LIM_CANTO,
                        'r': LIM_R, 'z': LIM_Z},
           'semente_bootstrap': SEMENTE, 'reamostragens': NBOOT,
           'universo': {str(a): U[a] for a in ANOS},
           'ultimo_digito': {str(a): D[a] for a in ANOS},
           'canto': {str(a): C[a] for a in ANOS},
           'canto_razoes': {nome: {t: {str(a): RZ[nome][t][a] for a in ANOS} for t in TURNOS} for nome in RZ},
           'canto_razoes_robustez_denominador_todas': {nome: {t: {str(a): RZ_todas[nome][t][a] for a in ANOS}
                                                              for t in TURNOS} for nome in RZ_todas},
           'comparecimento_virada': {str(a): V[a] for a in ANOS},
           'veredito_por_ano': {str(a): VER[a] for a in ANOS},
           'leitura_do_registro': leitura,
           'exploratorio_depois_de_rodar': {
               'aviso': 'Decidido depois de ver as partes 1 a 3; fora do veredito e da leitura (ver o docstring, E1 a E3).',
               'semente': SEMENTE_EXP, 'sorteios': NSIM,
               'E1_digito_simulado': {str(a): E1[a] for a in ANOS},
               'E2_digito_100_ou_mais': {str(a): E2[a] for a in ANOS},
               'E3_localizacao_cantos': {str(a): E3[a] for a in ANOS},
               'E4_municipio_com_mais_secoes_de_cada_canto': {
                   mm: {str(b): {tt: E4[b][tt].get(mm) for tt in TURNOS} for b in ANOS}
                   for mm in sorted({E3[a][f'{t}_{l}']['municipios_com_mais'][0][0] for a in ANOS for t in TURNOS
                                     for l in ('PT', 'adversario') if E3[a][f'{t}_{l}']['municipios_com_mais']})},
               'E4_formato': '[seções, seções com comparecimento >= 95%, comparecimento agregado do município]'}}

    def limpa(o):
        if isinstance(o, dict):
            return {k: limpa(v) for k, v in o.items()}
        if isinstance(o, list):
            return [limpa(v) for v in o]
        if isinstance(o, float) and (math.isinf(o) or math.isnan(o)):
            return str(o)
        return o

    with open(saida_json, 'w') as f:
        json.dump(limpa(res), f, ensure_ascii=False, indent=1)

    # ---------------------------------------------------------------------------------------- texto
    o = []
    a_ = o.append
    a_('P3 (Adendo 26): padrões de perícia eleitoral em 2014, 2018, 2022 e 2026, dois turnos, sem o exterior.')
    a_('Registro: PRE-REGISTRO-2026-10-26.md, Adendo 26, P3, commit 5174ff5 (07/11/2026 13:57:56 UTC), antes de rodar.')
    a_('Script: scripts/analisar_P3_pericia.py (python3 -I). Números completos: resultados/P3_pericia_4_anos.json.')
    a_('Postagem checada: @FelipeCecilio_ (X), republicada em felipececilio.reserva (Instagram): "métricas do 2º turno de 2014')
    a_('muito semelhantes às observadas agora" e "padrões estatísticos que levantam questionamentos".')
    a_('')
    a_('VEREDITO POR ANO, PELA LETRA')
    for a in ANOS:
        v = VER[a]
        motivo = []
        if v['digito']:
            motivo.append('último dígito: ' + '; '.join(v['digito']))
        if v['canto_PT']:
            motivo.append('canto do PT: ' + ', '.join(v['canto_PT']))
        if v['correlacao_PT']:
            motivo.append('correlação: ' + ', '.join(v['correlacao_PT']))
        a_(f'  {a} ({CAND[a][0]} x {CAND[a][1]}): {v["veredito"]}' + (f' ({" | ".join(motivo)})' if motivo else ''))
    a_(f'  Leitura do registro: {leitura}')
    a_('')
    texto_significado(a_, D, C, RZ, V, VER, E1, E2, E3, E4)
    a_('1. Último dígito (contagens de 50 ou mais do candidato; qui-quadrado contra a uniforme, 9 gl)')
    a_('   Condição de sinal da série: p < 0,001 E alguma frequência a mais de 0,5 ponto de 10%.')
    a_('   ano  turno candidato     contagens   qui2     p            maior desvio (dígito)  p<0,001  desvio>0,5  cumpre')
    for a in ANOS:
        for t in TURNOS:
            for c in ('L', 'R'):
                x = D[a][t][c]
                nome = CAND[a][0] if c == 'L' else CAND[a][1]
                a_(f'   {a} {t}º    {nome:<10} {fi(x["n"]):>11} {fn(x["qui2"]):>8} {fp(x["p"], x["log10_p"]):>12}'
                   f'  {fn(x["maior_desvio_com_sinal_pts"], 3):>7} ({x["digito_maior_desvio"]})'
                   f'          {sn(x["cond_p_menor_0001"]):>3}      {sn(x["cond_desvio_maior_05"]):>3}       {sn(x["cumpre"])}')
    a_('   Frequências (%, dígitos 0 a 9; ep binomial de cada uma entre 0,04 e 0,05 ponto): ver o .json, campo freq_pct.')
    a_('')
    a_('2. Canto de enchimento (comparecimento >= 95% dos aptos e fatia >= 90% entre os finalistas; seções com L+R > 0)')
    a_('   Fração em %; ep agrupado por município; razão = fração do ano / média simples dos outros três anos no mesmo turno.')
    for t in TURNOS:
        a_(f'   {t}º turno')
        a_('   ano   seções    canto do PT: n  fração % (ep)        razão (ep)      >3  | canto do adversário: n  fração % (ep)        razão  | comp >= 95%: n  fração %  razão')
        for a in ANOS:
            cc = C[a][t]
            p_ = cc['canto_PT']; r_ = RZ['canto_PT'][t][a]
            q_ = cc['canto_adversario']; s_ = RZ['canto_adversario'][t][a]
            u_ = cc['comp95']; w_ = RZ['comp95'][t][a]
            a_(f'   {a} {fi(cc["secoes_LR_pos"]):>9} {fi(p_["n"]):>15}  {fn(100 * p_["fracao"], 4)} ({fn(100 * p_["ep"], 4)})'
               f'  {fn(r_["razao"], 3):>7} ({fn(r_["ep_razao"], 3)})  {sn(r_["cumpre_razao_maior_3"]):>3}'
               f'  | {fi(q_["n"]):>22}  {fn(100 * q_["fracao"], 4)} ({fn(100 * q_["ep"], 4)})  {fn(s_["razao"], 3):>6}'
               f'  | {fi(u_["n"]):>14}  {fn(100 * u_["fracao"], 3):>7}  {fn(w_["razao"], 3)}')
    a_('')
    a_('3. Comparecimento e virada, por seção, dentro do município')
    a_('   x = comp2/apt2 - comp1/apt1; y = L2/(L2+R2) - L1/(L1+R1) (frações). Condição: r >= 0,10 e r > 4 ep (ep primário:')
    a_('   regressão padronizada com erro agrupado por município). Ao lado: ep por bootstrap de municípios (2.000) e o')
    a_('   coeficiente de y em x dentro do local (lib.fe_ols, peso L2+R2, erro agrupado por local).')
    a_('   ano   seções   municípios | ponderada: r (ep; ep boot)        z    | sem peso: r (ep; ep boot)         z    | cumpre | dentro do local: coef (ep)  t')
    for a in ANOS:
        vv = V[a]; pw = vv['ponderada']; uw = vv['sem_peso']; ll = vv['leitura_dentro_do_local']
        a_(f'   {a} {fi(vv["secoes"]):>9} {fi(vv["municipios"]):>8} | {fn(pw["r"], 4):>7} ({fn(pw["ep_agrupado_municipio"], 4)}; {fn(pw["ep_bootstrap"], 4)})'
           f' {fn(pw["z"], 1):>6} | {fn(uw["r"], 4):>7} ({fn(uw["ep_agrupado_municipio"], 4)}; {fn(uw["ep_bootstrap"], 4)})'
           f' {fn(uw["z"], 1):>6} | {sn(vv["cumpre_PT"]):>6} | {fn(ll["coef"], 4):>7} ({fn(ll["ep_agrupado_local"], 4)}) {fn(ll["t"], 1):>6}')
    a_('   Conferência: o coeficiente da regressão padronizada é igual a r (maior diferença absoluta '
       + fn(max(abs(V[a][nm]['dif_r_menos_coef']) for a in ANOS for nm in ('ponderada', 'sem_peso')) * 1e12, 3) + 'e-12).')
    a_('')
    a_('4. Exploratório (pedido na tarefa, fora do registro e do veredito; regra fixada antes de rodar): o lado do adversário')
    for a in ANOS:
        v = VER[a]
        ca = '; '.join(f'{t}º turno razão {fn(RZ["canto_adversario"][t][a]["razao"], 3)}' for t in TURNOS)
        a_(f'   {a}: canto do adversário {ca}: cumpre {", ".join(v["exploratorio_canto_adversario"]) or "em nenhum turno"};'
           f' correlação do adversário (r_R = -r) ponderada {fn(V[a]["ponderada"]["r_adversario"], 4)},'
           f' sem peso {fn(V[a]["sem_peso"]["r_adversario"], 4)}: cumpre {", ".join(v["exploratorio_correlacao_adversario"]) or "em nenhum peso"}.')
    a_('')
    a_('5. Robustez declarada antes (não muda o veredito)')
    for a in ANOS:
        v = VER[a]
        a_(f'   {a}: canto do PT com todas as seções no denominador: razão '
           + '; '.join(f'{t}º {fn(RZ_todas["canto_PT"][t][a]["razao"], 3)}' for t in TURNOS)
           + f' (cumpre: {", ".join(v["robustez_canto_PT_denominador_todas"]) or "nenhum"}); correlação com o ep do bootstrap'
           f' cumpre: {", ".join(v["robustez_correlacao_PT_ep_bootstrap"]) or "nenhum"}.')
    a_('')
    a_('6. Universo')
    for a in ANOS:
        u = U[a]
        a_(f'   {a}: chaves {fi(u["chaves"])}; exterior fora {fi(u["exterior"])}; 1º turno {fi(u["universo_1"])} seções'
           f' (anuladas fora {u["nao_apurada_1"]}); 2º turno {fi(u["universo_2"])} (anuladas fora {u["nao_apurada_2"]});'
           f' pares para a parte 3 {fi(u["pares"])} (fora por anulada ou L+R = 0 em algum turno: {u["par_fora_apurada_aptos_LR"]}).')
    a_('')
    texto_exploratorio(a_, E1, E2, E3, RZ, E4)
    a_('')
    texto_desvios(a_)
    with open(saida_txt, 'w') as f:
        f.write('\n'.join(o))


if __name__ == '__main__':
    main()
