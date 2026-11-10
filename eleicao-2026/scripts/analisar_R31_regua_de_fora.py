#!/usr/bin/env python3
"""R31 (Adendo 31): a régua de fora para o gráfico por estado.

Registro: PRE-REGISTRO-2026-10-26.md, seção "Adendo 31", commit 167e0ff (10/11/2026 11:56:37 UTC).
Este docstring foi escrito ANTES de baixar qualquer tabela de fora e ANTES de calcular qualquer medida
(cópia datada e SHA-256 em /home/user/trabalho-eleicao/adendo31/parciais/docstring_antes_de_calcular.txt).
O que o registro fixa vale pela letra. O que ele não fixa está decidido abaixo (D1 a D12) e sai no
relatório como desvio. O que for feito depois de ver o resultado sai marcado como EXPLORATÓRIO.

O QUE O REGISTRO FIXA (resumo; vale o texto do registro)
  Eleições: França 2022, Chile 2021, Colômbia 2022, Argentina 2023 (geral e segundo turno), Turquia 2023,
  Equador 2025 e qualquer outra de dois turnos com cédula de papel em que os dois finalistas somem 85% ou
  mais dos válidos do 1º turno. Só unidades com 50 mil votos válidos ou mais no 2º turno. Voto no exterior
  relatado à parte. Medidas: (1) receita do carrossel (x = fatia do finalista B entre os votos dos dois
  finalistas no 1º turno; y = votos de A sobre votos de B no 2º turno; R² linear, quadrático e exponencial);
  (2) S = desvio-padrão, entre as unidades, da variação da fatia a dois de B, sem peso e com peso por
  votos; (3) resíduo da reta da fatia a dois do 2º turno contra a do 1º; (4) o = fatia dos válidos do 1º
  turno fora dos dois finalistas; (5) em quantas unidades o movimento teve o mesmo sinal.
  Leitura: conjunto comparável = eleições de fora com o de 15% ou menos. "2026 FORA DO PADRÃO" se o S de
  2026 for menor que a metade do menor S do conjunto comparável E ficar abaixo do limite inferior de 95% da
  reta de S contra o ajustada em todas as eleições de fora. "2026 DENTRO DO PADRÃO" se o S de 2026 for de
  pelo menos 0,75 vez o menor S do conjunto comparável, OU ficar dentro do intervalo de 95% da reta. Entre
  os dois, ou com menos de duas eleições no conjunto comparável: INCONCLUSIVO. A mesma leitura para 2022.

DECISÕES QUE O REGISTRO NÃO FIXA (tomadas aqui, antes de qualquer conta)

D1. Unidades de primeiro nível.
    Brasil: 27 UFs; exterior = UF "ZZ" das bases por seção.
    França 2022: os departamentos do arquivo do Ministério do Interior por departamento (96 da metrópole,
      com as duas Córsegas separadas, mais os departamentos e coletividades de ultramar, cada um como
      unidade do território); exterior = "Français établis hors de France".
    Chile 2021: 16 regiões; exterior = "Extranjero".
    Colômbia 2022: 32 departamentos mais Bogotá D.C.; exterior = "Consulados".
    Argentina 2023: 24 distritos (23 províncias e a Cidade de Buenos Aires). O voto de residentes no
      exterior é apurado dentro do distrito do eleitor; não existe unidade "exterior" separável, então as
      versões com e sem exterior coincidem.
    Turquia 2023: 81 províncias; exterior = urnas das representações no exterior mais as dos postos de
      fronteira (gümrük), somadas numa unidade.
    Equador 2025: 24 províncias; exterior = as circunscrições especiais do exterior somadas numa unidade.
    Eleições adicionais: a unidade de primeiro nível da tabela oficial (região, departamento, condado ou
      distrito administrativo).

D2. Voto válido = voto dado a candidato (nominal), como no Brasil. Branco e nulo ficam fora em todos os
    países, inclusive onde a lei local chama o branco de válido (voto en blanco da Colômbia, voto en
    blanco da Argentina). Filtro do registro: entra a unidade com 50.000 ou mais votos válidos no 2º turno
    (soma dos dois finalistas). O filtro vale também para a unidade "exterior" e, na versão agregada, para
    o grupo já somado (as unidades pequenas entram na soma do grupo).

D3. Quem é B. No Brasil, B = adversário do PT (coluna R da base: Flávio em 2026, Bolsonaro em 2022 e 2018,
    Aécio em 2014) e A = candidato do PT, como no Adendo 29. Nas eleições de fora, B = o finalista mais
    votado no país no 1º turno (o papel de Flávio em 2026) e A = o outro. As medidas 2, 3 e 5 não mudam
    se A e B trocarem de lugar; a 4 também não. Só os três R² do carrossel mudam, e por isso eles saem
    também com os papéis trocados, ao lado.

D4. Medida 1 (carrossel). x = 100 * B1 / (A1 + B1); y = A2 / B2. Linear e quadrático por mínimos quadrados
    (polinômio de grau 1 e 2). Exponencial y = a * exp(b * x) por mínimos quadrados não lineares em y,
    partindo do ajuste pelo log (a mesma conta que reproduziu a legenda do carrossel no Adendo 29: 0,9350;
    0,9949; 0,9987). R² = 1 - SQR / SQT em y. Sem peso. Ao lado, o exponencial ajustado pelo log.

D5. Medida 2. d = 100 * [B2 / (A2 + B2) - B1 / (A1 + B1)] por unidade, em pontos. S sem peso = desvio-padrão
    amostral (divisor n - 1), a conta que deu 0,69 para 2026 no Adendo 29. S com peso = raiz da média
    ponderada de (d - média ponderada)², com peso = válidos do 2º turno da unidade (A2 + B2).

D6. Medida 3. Reta de mínimos quadrados, sem peso, de p2 = 100 * B2 / (A2 + B2) contra p1 = 100 * B1 /
    (A1 + B1); resíduo = raiz de SQR / (n - 2), como no Adendo 29. Saem também a inclinação e o R² da reta.

D7. Medida 4. o = 100 * (válidos do 1º turno fora dos dois finalistas) / (válidos do 1º turno), no total
    do país somando TODAS as unidades de primeiro nível (inclusive as que não passam o filtro de 50 mil),
    sem o exterior na versão principal e com o exterior na outra. No Brasil, o = O / (L + R + O) da base
    (em 2026 o O inclui os votos do candidato 28, anulado, como está na base).

D8. Medida 5. Sinal do movimento nacional = sinal de d calculado na soma das unidades incluídas. Conto as
    unidades com d do mesmo sinal ("k de n") e digo o sentido (B subiu ou caiu).

D9. Versões. PRINCIPAL = sem o exterior (unidades do território com 50 mil válidos ou mais), que é a
    conta dos números do Brasil citados no registro (0,69; 0,53; 3,38; 4,01 com 27 UFs). COM EXTERIOR = as
    mesmas unidades mais o exterior como um ponto a mais, se ele passar o filtro (foi assim que o
    carrossel desenhou o 28º ponto). A leitura fixada usa a versão principal; a versão com exterior vai
    ao lado.

D10. Agregação (o registro pede "também" as medidas com unidades agregadas em 20 a 30 grupos de regiões
    oficiais, onde as unidades forem pequenas). Regra: agrego a eleição que tiver mais de 30 unidades
    depois do filtro e tiver divisão regional oficial. Pelo que se sabe do número de unidades, isso pega
    França e Turquia.
    França: as 22 regiões administrativas da metrópole que valeram até 31/12/2015 (código INSEE antigo),
      com cada departamento ou coletividade de ultramar como grupo próprio se passar o filtro (dá de 22 a
      27 grupos). Ao lado, como sensibilidade, as 13 regiões atuais da metrópole (fora da faixa de 20 a 30).
    Turquia: as 26 sub-regiões estatísticas de nível 2 do TÜİK (İBBS-2, equivalente a NUTS-2).
    As outras (até 30 unidades depois do filtro) ficam como estão, e o valor delas repete na versão
    agregada. Como o registro diz "também", a LEITURA PRINCIPAL usa as unidades de primeiro nível e a
    leitura com França e Turquia agregadas vai ao lado, com o mesmo destaque. Se as duas divergirem,
    isso é dito no veredito.

D11. Reta de S contra o. Um ponto por eleição de fora incluída; S sem peso da versão principal (primeiro
    nível, sem exterior); o da versão principal, em pontos percentuais; mínimos quadrados sem peso, S e o
    em escala natural. O registro diz "limite inferior de 95% da reta" e "intervalo de 95% da reta" sem
    dizer se é a faixa de confiança da reta (incerteza da média) ou o intervalo de predição para uma
    eleição nova. Fixo como PRINCIPAL o intervalo de predição bilateral de 95% para uma eleição nova no o
    do ano brasileiro (t de Student com n - 2 graus de liberdade), porque a pergunta é se UMA eleição cai
    no padrão das outras; a faixa de confiança da reta (mais estreita, mais favorável a "fora") vai ao
    lado, e se a leitura mudar de uma para a outra isso é dito no veredito. "Abaixo do limite inferior" =
    S do Brasil menor que o limite inferior; "dentro do intervalo" = entre os dois limites, inclusive.
    Aviso fixado antes: se o limite inferior do intervalo for zero ou negativo, a cláusula do intervalo
    não consegue excluir valor nenhum de S; nesse caso relato a leitura pela letra e digo, ao lado, que
    essa cláusula ficou sem dentes e o que dizem sozinhas a regra da metade e a de 0,75.
    Com menos de 3 eleições de fora não há reta: a leitura fica só com as razões, e "fora do padrão" não
    pode fechar.
    Descritivo, sem leitura: onde caem 2018 e 2014 em relação à reta.

D12. Eleições adicionais (as de 85% ou mais). Lista de candidatas fixada agora, antes de ver qualquer
    número por unidade: Chile 1999/2000, Gana 2000, Gana 2008, El Salvador 2014, Libéria 2023, Serra Leoa
    2018, Moldávia 2016, Macedônia do Norte 2019, Maldivas 2023, Cabo Verde 2001. Se a busca achar outra
    que cumpra a regra, entra na lista e eu digo que foi achada depois. Entra na análise a que cumprir
    tudo: (i) cédula de papel; (ii) dois finalistas com 85% ou mais dos válidos do 1º turno; (iii) 2º turno
    disputado de fato (boicote do 2º turno exclui: Zimbábue 2008, Libéria 2011); (iv) os dois turnos por
    unidade de primeiro nível obtidos de fonte oficial, ou de segunda mão com a soma das unidades a 0,5%
    ou menos do total nacional oficial de cada finalista nos dois turnos; (v) 8 ou mais unidades com 50
    mil válidos no 2º turno. Eleição contestada pelo perdedor entra com o aviso ao lado (o registro fez
    assim com o Equador). A mesma tolerância de 0,5% vale para as seis eleições nomeadas quando a tabela
    for de segunda mão; acima disso a eleição sai da leitura e fica relatada à parte.
    Leitura principal = com todas as eleições de fora incluídas. Ao lado = só com as seis nomeadas na
    tarefa (França, Chile, Colômbia, Argentina, Turquia, Equador).

SAÍDAS
  resultados/R31_regua_de_fora.json e .txt; resultados/R31_tabelas/ (um CSV por eleição, com fonte e
  data de acesso nas linhas de cabeçalho que começam com "#").

USO
  python3 -I scripts/analisar_R31_regua_de_fora.py
  Lê só os CSV de resultados/R31_tabelas/ e as bases dados/secoesAAAA.json.gz. Não acessa a rede.
"""

# ---------------------------------------------------------------------------------------------------------
# NOTAS ESCRITAS DEPOIS DO DOCSTRING (durante o levantamento dos dados e ANTES de calcular qualquer medida)
# ---------------------------------------------------------------------------------------------------------
# N1. Equador 2025: o CNE respondeu com captcha e não foi achada tabela de votos por província do 2º turno.
#     Só há votos por província no 1º turno (Wikipedia em alemão, confere com o CNE) e porcentagens parciais
#     do 2º turno na imprensa. Pela D12 (tolerância de 0,5% na soma, que aqui não dá para conferir), o
#     Equador fica FORA da leitura principal e é relatado à parte, com uma leitura de sensibilidade que o
#     inclui. Os "votos" do 2º turno no CSV são pseudovotos (ver o cabeçalho do CSV).
# N2. Colômbia 2022: a tabela por departamento é o preconteo (difere do escrutínio em 0,10% a 0,23%).
# N3. Turquia 2023: províncias pela contagem das agências (haberler.com), que difere do YSK em 0,02% ou
#     menos; exterior e totais do YSK.
# N4. Adicionais que cumpriram a D12: Chile 1999/2000 (fonte oficial) e El Salvador 2014 (segunda mão que
#     fecha exatamente com o TSE). Não obtidas por unidade: Gana 2000 e 2008, Libéria 2023, Serra Leoa 2018
#     (só o 2º turno), Moldávia 2016, Macedônia do Norte 2019. Maldivas 2023 e Cabo Verde 2001 não têm 8
#     unidades com 50 mil válidos.
# N5. As tabelas foram montadas pelos scripts de /home/user/trabalho-eleicao/adendo31/scripts/ (montar_*.py),
#     que só leem e gravam dados; nenhuma medida foi calculada antes de este script rodar.
# N6. Os CSV do Brasil (brasil_AAAA.csv) são a soma por UF de dados/secoesAAAA.json.gz. Para refazê-los a partir
#     das bases: python3 -I scripts/analisar_R31_regua_de_fora.py --refazer-brasil (regrava os quatro CSV e segue).

import csv, json, math, os, sys
import numpy as np
from scipy import stats
from scipy.optimize import least_squares

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
TAB = os.path.join(BASE, 'resultados', 'R31_tabelas')
SAIDA_JSON = os.path.join(BASE, 'resultados', 'R31_regua_de_fora.json')
SAIDA_TXT = os.path.join(BASE, 'resultados', 'R31_regua_de_fora.txt')
FILTRO = 50000
NUM = ['v1_A', 'v1_B', 'v1_validos', 'v2_A', 'v2_B']

# id, arquivo, rótulo, classe, nomeada na tarefa, entra na leitura principal, tipo de voto, coluna de agregação, aviso
ELEICOES = [
    ('fr2022', 'franca_2022.csv', 'França 2022', 'fora', True, True, 'papel', 'grupo', ''),
    ('cl2021', 'chile_2021.csv', 'Chile 2021', 'fora', True, True, 'papel', None, ''),
    ('co2022', 'colombia_2022.csv', 'Colômbia 2022', 'fora', True, True, 'papel', None, 'tabela por departamento é o preconteo'),
    ('ar2023', 'argentina_2023.csv', 'Argentina 2023', 'fora', True, True, 'papel', None, ''),
    ('tr2023', 'turquia_2023.csv', 'Turquia 2023', 'fora', True, True, 'papel', 'grupo', 'campanha desigual; contagem não contestada pela oposição'),
    ('ec2025', 'equador_2025.csv', 'Equador 2025', 'fora', True, False, 'papel', None, 'contestada pela perdedora; 2º turno só em porcentagem parcial, não conferível por soma: FORA da leitura principal'),
    ('cl1999', 'chile_1999.csv', 'Chile 1999/2000', 'fora', False, True, 'papel', None, 'adicional (85% ou mais)'),
    ('sv2014', 'elsalvador_2014.csv', 'El Salvador 2014', 'fora', False, True, 'papel', None, 'adicional (85% ou mais); contestada pelo perdedor'),
    ('br2014', 'brasil_2014.csv', 'Brasil 2014', 'brasil', False, False, 'urna eletrônica', None, ''),
    ('br2018', 'brasil_2018.csv', 'Brasil 2018', 'brasil', False, False, 'urna eletrônica', None, ''),
    ('br2022', 'brasil_2022.csv', 'Brasil 2022', 'brasil', False, False, 'urna eletrônica', None, 'também sob suspeita do Léo'),
    ('br2026', 'brasil_2026.csv', 'Brasil 2026', 'brasil', False, False, 'urna eletrônica', None, 'eleição sob suspeita'),
]


def ler_csv(arq):
    meta, linhas = {}, []
    with open(os.path.join(TAB, arq), encoding='utf-8', newline='') as f:
        corpo = []
        for ln in f:
            if ln.startswith('#'):
                k, _, v = ln[1:].partition(':'); meta[k.strip()] = v.strip()
            else:
                corpo.append(ln)
    for r in csv.DictReader(corpo, delimiter=';'):
        for c in NUM: r[c] = int(r[c])
        linhas.append(r)
    return meta, linhas


def agregar(linhas, col):
    """Soma as unidades do território por grupo; o exterior fica como está."""
    g, ext = {}, []
    for r in linhas:
        if r['tipo'] != 'territorio': ext.append(r); continue
        a = g.setdefault(r[col], {'unidade': r[col], 'tipo': 'territorio', **{c: 0 for c in NUM}})
        for c in NUM: a[c] += r[c]
    return list(g.values()) + ext


def r2(y, yh):
    return float(1.0 - ((y - yh) ** 2).sum() / ((y - y.mean()) ** 2).sum())


def tres_r2(x, y):
    """R² linear, quadrático, exponencial (mínimos quadrados não lineares em y) e exponencial pelo log (R² em y)."""
    lin = r2(y, np.polyval(np.polyfit(x, y, 1), x))
    quad = r2(y, np.polyval(np.polyfit(x, y, 2), x))
    b0 = np.polyfit(x, np.log(y), 1); xm = x.mean()
    elog = r2(y, np.exp(np.polyval(b0, x)))
    f = lambda p: p[0] * np.exp(p[1] * (x - xm)) - y
    s = least_squares(f, [math.exp(b0[1] + b0[0] * xm), b0[0]], method='lm', xtol=1e-14, ftol=1e-14, gtol=1e-14)
    enls = r2(y, s.x[0] * np.exp(s.x[1] * (x - xm)))
    return {'linear': lin, 'quadratico': quad, 'exponencial': enls, 'exponencial_pelo_log': elog}


def medidas(linhas, com_exterior, filtro=FILTRO):
    univ = [r for r in linhas if r['tipo'] == 'territorio' or (com_exterior and r['tipo'] == 'exterior')]
    v1 = sum(r['v1_validos'] for r in univ); ab1 = sum(r['v1_A'] + r['v1_B'] for r in univ)
    o = 100.0 * (v1 - ab1) / v1
    un = [r for r in univ if r['v2_A'] + r['v2_B'] >= filtro]
    fora = [r['unidade'] for r in univ if r['v2_A'] + r['v2_B'] < filtro]
    A1 = np.array([r['v1_A'] for r in un], float); B1 = np.array([r['v1_B'] for r in un], float)
    A2 = np.array([r['v2_A'] for r in un], float); B2 = np.array([r['v2_B'] for r in un], float)
    nomes = [r['unidade'] for r in un]; n = len(un)
    p1 = 100 * B1 / (A1 + B1); p2 = 100 * B2 / (A2 + B2); d = p2 - p1; w = A2 + B2
    nat1 = 100 * B1.sum() / (A1.sum() + B1.sum()); nat2 = 100 * B2.sum() / (A2.sum() + B2.sum()); dnat = nat2 - nat1
    m = {'n_unidades': n, 'unidades_fora_do_filtro': fora, 'o': o, 'fatia_dois_finalistas_1T': 100 - o,
         'fatia_a_dois_B_1T_nas_unidades': nat1, 'fatia_a_dois_B_2T_nas_unidades': nat2, 'movimento_nas_unidades': dnat}
    if n < 3:
        m['erro'] = 'menos de 3 unidades'; return m
    m['carrossel'] = tres_r2(p1, A2 / B2)
    m['carrossel_papeis_trocados'] = tres_r2(100 - p1, B2 / A2)
    m['S_sem_peso'] = float(d.std(ddof=1))
    dm = float((w * d).sum() / w.sum()); m['S_com_peso'] = float(math.sqrt((w * (d - dm) ** 2).sum() / w.sum()))
    m['d_media_sem_peso'] = float(d.mean()); m['d_media_com_peso'] = dm
    b = np.polyfit(p1, p2, 1); e = p2 - np.polyval(b, p1)
    m['reta_p2_contra_p1'] = {'inclinacao': float(b[0]), 'intercepto': float(b[1]), 'residuo': float(math.sqrt((e ** 2).sum() / (n - 2))), 'r2': r2(p2, np.polyval(b, p1))}
    sinal = 1 if dnat > 0 else -1
    k = int(((d * sinal) > 0).sum())
    m['mesmo_sinal'] = {'k': k, 'n': n, 'sentido': 'B subiu' if sinal > 0 else 'B caiu'}
    ordem = np.argsort(d)
    m['d_min'] = [nomes[ordem[0]], float(d[ordem[0]])]; m['d_max'] = [nomes[ordem[-1]], float(d[ordem[-1]])]
    m['faixa_p1'] = [float(p1.min()), float(p1.max())]; m['dp_p1'] = float(p1.std(ddof=1))
    m['por_unidade'] = [{'unidade': nomes[i], 'p1': round(float(p1[i]), 3), 'p2': round(float(p2[i]), 3), 'd': round(float(d[i]), 3), 'validos_2T': int(w[i])} for i in range(n)]
    return m


def reta_S_o(pontos, o0s):
    """pontos: lista de (o, S). Devolve a reta e, para cada o0, ajuste, faixa de confiança e intervalo de predição de 95%."""
    n = len(pontos)
    if n < 3: return None
    o = np.array([p[0] for p in pontos], float); S = np.array([p[1] for p in pontos], float)
    b = np.polyfit(o, S, 1); e = S - np.polyval(b, o); gl = n - 2
    se = math.sqrt((e ** 2).sum() / gl); sxx = ((o - o.mean()) ** 2).sum(); t = float(stats.t.ppf(0.975, gl))
    out = {'n': n, 'inclinacao': float(b[0]), 'intercepto': float(b[1]), 'erro_padrao_residual': se, 't_975': t, 'graus_de_liberdade': gl,
           'r2': r2(S, np.polyval(b, o)), 'em': {}}
    for nome, o0 in o0s.items():
        aj = float(np.polyval(b, o0)); hc = se * math.sqrt(1 / n + (o0 - o.mean()) ** 2 / sxx); hp = se * math.sqrt(1 + 1 / n + (o0 - o.mean()) ** 2 / sxx)
        out['em'][nome] = {'o': o0, 'ajuste': aj, 'confianca_95': [aj - t * hc, aj + t * hc], 'predicao_95': [aj - t * hp, aj + t * hp]}
    return out


def ler_letra(S_br, comp, intervalo):
    """Aplica a leitura fixada. comp: lista de (rotulo, S) do conjunto comparável. intervalo: [inf, sup] ou None."""
    r = {'S_brasil': S_br, 'n_comparavel': len(comp), 'comparavel': comp, 'intervalo_95': intervalo}
    if len(comp) < 2:
        r['leitura'] = 'INCONCLUSIVO'; r['motivo'] = 'menos de duas eleições no conjunto comparável'; return r
    menor = min(comp, key=lambda c: c[1]); r['menor_S_comparavel'] = list(menor); r['razao'] = S_br / menor[1]
    metade = S_br < 0.5 * menor[1]; r['regra_da_metade_S_menor_que_metade_do_menor'] = bool(metade)
    r['regra_075_S_pelo_menos_075_do_menor'] = bool(S_br >= 0.75 * menor[1])
    if intervalo is None:
        abaixo = dentro = False; r['aviso_intervalo'] = 'sem reta (menos de 3 eleições de fora)'
    else:
        abaixo = S_br < intervalo[0]; dentro = intervalo[0] <= S_br <= intervalo[1]
        if intervalo[0] <= 0: r['aviso_intervalo'] = 'limite inferior zero ou negativo: a cláusula do intervalo não consegue excluir valor nenhum de S (sem dentes)'
    r['abaixo_do_limite_inferior'] = bool(abaixo); r['dentro_do_intervalo'] = bool(dentro)
    if metade and abaixo: r['leitura'] = 'FORA DO PADRÃO'
    elif r['regra_075_S_pelo_menos_075_do_menor'] or dentro: r['leitura'] = 'DENTRO DO PADRÃO'
    else: r['leitura'] = 'INCONCLUSIVO'
    r['leitura_so_pelas_razoes'] = 'abaixo da metade' if metade else ('0,75 ou mais' if r['regra_075_S_pelo_menos_075_do_menor'] else 'entre a metade e 0,75')
    return r


def refazer_brasil():
    """Soma as bases por seção por UF e regrava resultados/R31_tabelas/brasil_AAAA.csv (mesmo conteúdo do montador original)."""
    import gzip, hashlib
    D = os.path.join(BASE, 'dados')
    nomes = {'2026': ('Lula (PT)', 'Flavio Bolsonaro (22)'), '2022': ('Lula (PT)', 'Jair Bolsonaro (22)'), '2018': ('Haddad (PT)', 'Jair Bolsonaro (17)'), '2014': ('Dilma (PT)', 'Aecio Neves (45)')}
    esperado = dict(l.split()[::-1] for l in open(os.path.join(D, 'SHA256SUMS.txt')).read().splitlines() if l.strip())
    cols = ['unidade', 'tipo', 'grupo', 'grupo2'] + NUM
    for ano in ('2026', '2022', '2018', '2014'):
        arq = 'secoes%s.json.gz' % ano
        h = hashlib.sha256(open(os.path.join(D, arq), 'rb').read()).hexdigest(); ok = esperado.get(arq, esperado.get('./' + arq)) == h
        with gzip.open(os.path.join(D, arq), 'rt') as f: S = json.load(f)
        U = {}
        for k, sec in S.items():
            u = U.setdefault(k.split('|')[0], {'1': [0, 0, 0], '2': [0, 0, 0]})
            for t in ('1', '2'):
                if t in sec and sec[t]:
                    u[t][0] += sec[t].get('L', 0) or 0; u[t][1] += sec[t].get('R', 0) or 0; u[t][2] += sec[t].get('O', 0) or 0
        del S
        linhas = [{'unidade': uf, 'tipo': 'exterior' if uf == 'ZZ' else 'territorio', 'grupo': '', 'grupo2': '', 'v1_A': U[uf]['1'][0], 'v1_B': U[uf]['1'][1],
                   'v1_validos': sum(U[uf]['1']), 'v2_A': U[uf]['2'][0], 'v2_B': U[uf]['2'][1]} for uf in sorted(U)]
        t = {c: sum(r[c] for r in linhas) for c in NUM}
        meta = [('eleicao', 'Brasil %s, presidencial, dois turnos' % ano), ('tipo_de_voto', 'urna eletronica'), ('A', nomes[ano][0]), ('B', nomes[ano][1] + ' (adversario do PT, como no Adendo 29)'),
                ('unidades', '27 UFs e exterior (ZZ)'), ('validos', 'votos nominais: L + R + O da base por secao'),
                ('fonte', 'dados/%s do repositorio (bweb do TSE; ver dados/LEIAME.md), somado por UF; sha256 %s (%s com dados/SHA256SUMS.txt)' % (arq, h, 'confere' if ok else 'NAO CONFERE')),
                ('acesso', '10/11/2026'), ('fonte_oficial_direta', 'sim (dados abertos do TSE, ja no repositorio)'),
                ('conferencia_total_nacional', 'somas com exterior: 1o turno A %d, B %d, validos %d; 2o turno A %d, B %d' % (t['v1_A'], t['v1_B'], t['v1_validos'], t['v2_A'], t['v2_B']))]
        with open(os.path.join(TAB, 'brasil_%s.csv' % ano), 'w', encoding='utf-8', newline='') as f:
            for k, v in meta: f.write('# %s: %s\n' % (k, v))
            w = csv.DictWriter(f, fieldnames=cols, delimiter=';'); w.writeheader()
            for r in linhas: w.writerow(r)
        print('refeito brasil_%s.csv' % ano, 'sha confere' if ok else 'SHA NAO CONFERE', flush=True)


def calcular():
    R = {'registro': 'Adendo 31, commit 167e0ff (10/11/2026 11:56:37 UTC)', 'filtro_validos_2T': FILTRO, 'eleicoes': {}}
    for eid, arq, rot, classe, nomeada, na_leitura, tipo, col, aviso in ELEICOES:
        meta, linhas = ler_csv(arq)
        E = {'rotulo': rot, 'classe': classe, 'nomeada_na_tarefa': nomeada, 'na_leitura_principal': na_leitura, 'tipo_de_voto': tipo, 'aviso': aviso,
             'arquivo': 'resultados/R31_tabelas/' + arq, 'A': meta.get('A'), 'B': meta.get('B'), 'fonte': meta.get('fonte'), 'acesso': meta.get('acesso'),
             'fonte_oficial_direta': meta.get('fonte_oficial_direta'), 'conferencia_total_nacional': meta.get('conferencia_total_nacional'),
             'tem_exterior': any(r['tipo'] == 'exterior' for r in linhas)}
        E['principal'] = medidas(linhas, False)
        E['com_exterior'] = medidas(linhas, True)
        if col:
            ag = agregar(linhas, col)
            E['agregado'] = medidas(ag, False); E['agregado_com_exterior'] = medidas(ag, True); E['agregado']['criterio'] = meta.get(col)
            if eid == 'fr2022':
                E['agregado_13_regioes'] = medidas(agregar(linhas, 'grupo2'), False)
        R['eleicoes'][eid] = E
    return R


def leituras(R):
    El = R['eleicoes']
    def S_de(eid, versao):
        E = El[eid]
        if versao == 'agregado': m = E.get('agregado', E['principal'])
        elif versao == 'agregado_com_exterior': m = E.get('agregado_com_exterior', E['com_exterior'])
        else: m = E[versao]
        return m['o'], m['S_sem_peso']
    cenarios = {
        'principal': ('todas as de fora conferidas, primeiro nível, sem exterior', [e for e, v in El.items() if v['classe'] == 'fora' and v['na_leitura_principal']], 'principal'),
        'agregado': ('as mesmas, com França e Turquia agregadas em regiões', [e for e, v in El.items() if v['classe'] == 'fora' and v['na_leitura_principal']], 'agregado'),
        'com_exterior': ('as mesmas, primeiro nível, com o exterior como unidade', [e for e, v in El.items() if v['classe'] == 'fora' and v['na_leitura_principal']], 'com_exterior'),
        'so_nomeadas_conferidas': ('só as nomeadas na tarefa que passaram na conferência (sem Equador)', [e for e, v in El.items() if v['classe'] == 'fora' and v['na_leitura_principal'] and v['nomeada_na_tarefa']], 'principal'),
        'com_equador': ('todas as de fora, incluindo o Equador não conferível', [e for e, v in El.items() if v['classe'] == 'fora'], 'principal'),
        'com_equador_agregado': ('todas as de fora com o Equador, França e Turquia agregadas', [e for e, v in El.items() if v['classe'] == 'fora'], 'agregado'),
        'seis_nomeadas': ('só as seis nomeadas na tarefa, incluindo o Equador não conferível', [e for e, v in El.items() if v['classe'] == 'fora' and v['nomeada_na_tarefa']], 'principal'),
    }
    L = {}
    for nome, (descr, ids, versao) in cenarios.items():
        pts = {e: S_de(e, versao) for e in ids}
        vbr = 'com_exterior' if versao in ('com_exterior',) else 'principal'
        br = {a: (El['br' + a][vbr]['o'], El['br' + a][vbr]['S_sem_peso']) for a in ('2026', '2022', '2018', '2014')}
        reta = reta_S_o(list(pts.values()), {a: br[a][0] for a in br})
        comp = [(El[e]['rotulo'], pts[e][1]) for e in ids if pts[e][0] <= 15.0]
        c = {'descricao': descr, 'eleicoes': {El[e]['rotulo']: {'o': pts[e][0], 'S': pts[e][1]} for e in ids}, 'reta_S_contra_o': reta, 'brasil': {}}
        for a in ('2026', '2022'):
            iv_p = reta['em'][a]['predicao_95'] if reta else None; iv_c = reta['em'][a]['confianca_95'] if reta else None
            c['brasil'][a] = {'o': br[a][0], 'S': br[a][1], 'pela_predicao_95': ler_letra(br[a][1], comp, iv_p), 'pela_faixa_de_confianca_95': ler_letra(br[a][1], comp, iv_c)}
        for a in ('2018', '2014'):
            c['brasil'][a] = {'o': br[a][0], 'S': br[a][1], 'descritivo': (reta['em'][a] if reta else None)}
        L[nome] = c
    return L



def exploratorio(R):
    """Tudo aqui foi decidido DEPOIS de ver o resultado. Não entra na leitura pela letra."""
    El = R['eleicoes']; X = {}
    # E1: S dividido por o (dispersão por ponto de voto a redistribuir)
    X['E1_S_sobre_o'] = {E['rotulo']: E['principal']['S_sem_peso'] / E['principal']['o'] for E in El.values()}
    # E2: França só com a metrópole (os territórios de ultramar são casos extremos)
    _, fr = ler_csv('franca_2022.csv'); met = [r for r in fr if r['tipo'] == 'territorio' and not r['grupo'].startswith('ultramar')]
    m1 = medidas(met, False); m2 = medidas(agregar(met, 'grupo'), False)
    X['E2_franca_so_metropole'] = {'departamentos': {'n': m1['n_unidades'], 'S': m1['S_sem_peso'], 'residuo': m1['reta_p2_contra_p1']['residuo'], 'mesmo_sinal': m1['mesmo_sinal']},
                                   '22_regioes': {'n': m2['n_unidades'], 'S': m2['S_sem_peso'], 'residuo': m2['reta_p2_contra_p1']['residuo'], 'mesmo_sinal': m2['mesmo_sinal']}}
    # E3: a leitura só pelas razões tirando uma eleição do conjunto comparável de cada vez (com e sem o Equador)
    comp = [(E['rotulo'], E['principal']['S_sem_peso']) for E in El.values() if E['classe'] == 'fora' and E['principal']['o'] <= 15]
    X['E3_tirando_uma'] = {}
    conf = [x for x in comp if x[0] != 'Equador 2025']          # as conferidas; o S do Equador nunca é o menor, então incluí-lo não muda nada
    for fora_nome in [None] + [c[0] for c in conf]:
        c = [x for x in conf if x[0] != fora_nome]
        menor = min(c, key=lambda x: x[1]); chave = ('sem ' + fora_nome) if fora_nome else 'as três conferidas'
        X['E3_tirando_uma'][chave] = {'n': len(c), 'menor': list(menor), 'razao_2026': El['br2026']['principal']['S_sem_peso'] / menor[1], 'razao_2022': El['br2022']['principal']['S_sem_peso'] / menor[1]}
    # E4: as medidas sem o filtro de 50 mil válidos
    X['E4_sem_filtro'] = {}
    for eid, arq, rot, classe, *_ in ELEICOES:
        _, linhas = ler_csv(arq); m = medidas(linhas, False, 0)
        X['E4_sem_filtro'][rot] = {'n': m['n_unidades'], 'S': m['S_sem_peso'], 'residuo': m['reta_p2_contra_p1']['residuo']}
    # E5: posição do Brasil entre as eleições polarizadas (o de 15% ou menos), em S, em resíduo e em S sobre o
    pol = [(E['rotulo'], E['principal']['S_sem_peso'], E['principal']['reta_p2_contra_p1']['residuo'], E['principal']['S_sem_peso'] / E['principal']['o'], E['principal']['dp_p1'])
           for E in El.values() if E['principal']['o'] <= 15]
    X['E5_polarizadas'] = [{'eleicao': a, 'S': b, 'residuo': c, 'S_sobre_o': d, 'dp_p1': e} for a, b, c, d, e in sorted(pol, key=lambda x: x[1])]
    # E6: a reta de S contra o passando pela origem e em log (só descritivo)
    pts = [(E['principal']['o'], E['principal']['S_sem_peso']) for E in El.values() if E['classe'] == 'fora' and E['na_leitura_principal']]
    o = np.array([p[0] for p in pts]); S = np.array([p[1] for p in pts]); k = float((o * S).sum() / (o * o).sum())
    lr = np.log(S / o); t = float(stats.t.ppf(0.975, len(pts) - 1)); h = t * lr.std(ddof=1) * math.sqrt(1 + 1 / len(pts))
    X['E6_proporcional'] = {'inclinacao_pela_origem': k, 'S_sobre_o_media_geometrica': float(math.exp(lr.mean())),
                            'intervalo_predicao_95_de_S_sobre_o': [float(math.exp(lr.mean() - h)), float(math.exp(lr.mean() + h))],
                            'brasil_2026_S_sobre_o': El['br2026']['principal']['S_sem_peso'] / El['br2026']['principal']['o'],
                            'brasil_2022_S_sobre_o': El['br2022']['principal']['S_sem_peso'] / El['br2022']['principal']['o']}
    return X


NAO_OBTIDAS = [
    'Gana 2008 (o de 2,9%) e Gana 2000 (7,3%): a Wikipedia e o arquivo Psephos só têm o total nacional da eleição presidencial; o portal de dados abertos de Gana (data.gov.gh), que lista os arquivos da Comissão Eleitoral por região, recusou a conexão; o GhanaWeb só tem o resultado por distrito eleitoral em 460 páginas, que não baixei para não pesar.',
    'Libéria 2023 (12,7%): sem tabela por condado na Wikipedia nem no Psephos; o sítio da comissão eleitoral (necliberia.org) respondeu com a tela de verificação da Cloudflare (bloqueio): parei.',
    'Serra Leoa 2018 (14,1%): a Wikipedia só tem o 2º turno por distrito; o 1º turno por distrito não foi achado.',
    'Moldávia 2016 (13,3%) e Macedônia do Norte 2019 (11,1%): só o total nacional nas fontes consultadas; as unidades de primeiro nível (raions e municípios) são quase todas menores que 50 mil válidos.',
    'Maldivas 2023 (14,9%) e Cabo Verde 2001 (7,7%): eleitorado pequeno demais; não há 8 unidades com 50 mil válidos (critério v da D12).',
    'Excluídas pela regra, sem busca de dados: Zimbábue 2008 e Libéria 2011 (2º turno boicotado); República Dominicana 1996 (84,9%) e Irã 2024 (84,8%), abaixo dos 85%.',
]

DESVIOS = [
    'D1 a D12 do docstring: decisões que o registro não fixa, tomadas antes de baixar as tabelas de fora e antes de qualquer conta (unidades, voto válido, quem é B, receita exata dos R², fórmulas de S, resíduo e o, contagem do sinal, versão principal sem exterior, agregação de França e Turquia, intervalo de predição como principal e faixa de confiança ao lado, lista e critérios das eleições adicionais).',
    'Equador 2025 ficou FORA da leitura principal: o CNE respondeu com captcha e não foi achada tabela de votos do 2º turno por província. A tabela usada (votos do 1º turno e porcentagens parciais do 2º) não pode ser conferida por soma contra o total nacional, como o registro exige. Vai relatado à parte e numa leitura de sensibilidade.',
    'Colômbia 2022: a tabela por departamento é o preconteo da Registraduría, não o escrutínio (diferença de 0,10% a 0,23% por finalista). Turquia 2023: províncias pela contagem das agências (diferença de 0,02% ou menos contra o YSK). Chile 2021: tabela de segunda mão; o exterior do 1º turno saiu por diferença.',
    'Só França 2022 e Chile 1999/2000 vieram direto de fonte oficial. As outras são tabelas de segunda mão conferidas contra o total nacional oficial.',
    'Correções de erro de digitação das tabelas de segunda mão, todas decididas pela soma contra o total oficial ou pela porcentagem publicada, antes de qualquer medida: Chile 2021 (Biobío no 1º turno, Aisén no 2º), Colômbia 2022 (Vaupés no 2º), El Salvador 2014 (Chalatenango no 2º, Cuscatlán no 1º). Estão no cabeçalho de cada CSV.',
    'A lista de adicionais do docstring tinha 10 candidatas; só Chile 1999/2000 e El Salvador 2014 foram obtidas e conferidas. A ausência das outras não pode virar a leitura de "dentro" para "fora": a regra usa o MENOR S do conjunto comparável, e acrescentar eleições só pode baixar esse menor.',
    'A seção EXPLORATÓRIO (E1 a E6) foi feita depois de ver o resultado e não entra na leitura.',
]


def nf(x, d=2):
    return ('%.*f' % (d, x)).replace('.', ',')


def relatorio(R):
    El = R['eleicoes']; L = R['leituras']; X = R['exploratorio']; T = []
    A = T.append
    P = L['principal']; b26 = P['brasil']['2026']; b22 = P['brasil']['2022']; l26 = b26['pela_predicao_95']; l22 = b22['pela_predicao_95']
    A('R31 (ADENDO 31): A RÉGUA DE FORA PARA O GRÁFICO POR ESTADO')
    A('')
    A('Registro: PRE-REGISTRO-2026-10-26.md, Adendo 31, commit 167e0ff (10/11/2026 11:56:37 UTC), antes de rodar.')
    A('Decisões que o registro não fixa: docstring de scripts/analisar_R31_regua_de_fora.py, escrito antes de baixar as tabelas')
    A('de fora e antes de qualquer conta (cópia datada de 10/11/2026 12:02:03 UTC, SHA-256 b3027741...b170fd).')
    A('')
    A('RESUMO EM UMA LINHA')
    A('Pela letra do registro, 2026 fica DENTRO DO PADRÃO das eleições com cédula de papel, e 2022 também. Existe pelo menos')
    A('uma eleição em papel, que ninguém contesta, em que as regiões andaram ainda mais juntas do que os estados brasileiros')
    A('em 2026: Chile 1999/2000 (S de %s contra %s do Brasil em 2026 e %s em 2022). Isso derruba o argumento da "matemática' % (nf(El['cl1999']['principal']['S_sem_peso']), nf(b26['S']), nf(b22['S'])))
    A('impossível". Não prova que não houve troca uniforme: a régua não enxerga esse tipo de troca. E o resultado depende')
    A('dessa única eleição: nas outras três de 1º turno polarizado (Turquia, Equador, El Salvador) o S é de 1,7 a 2,3 vezes o de 2026.')
    A('')
    A('TABELA COMPARATIVA (versão principal: unidades de primeiro nível com 50 mil válidos ou mais no 2º turno, sem exterior)')
    cab = '%-17s %-9s %4s %6s %6s %6s %6s %7s %7s %7s  %-18s' % ('eleição', 'voto', 'unid', 'o %', 'S', 'S peso', 'resíd.', 'R² lin', 'R² quad', 'R² exp', 'mesmo sinal')
    A(cab); A('-' * len(cab))
    def linha(E, m, rot=None):
        return '%-17s %-9s %4d %6s %6s %6s %6s %7s %7s %7s  %-18s' % ((rot or E['rotulo'])[:17], 'papel' if E['tipo_de_voto'] == 'papel' else 'urna el.', m['n_unidades'], nf(m['o']), nf(m['S_sem_peso']), nf(m['S_com_peso']),
            nf(m['reta_p2_contra_p1']['residuo']), nf(m['carrossel']['linear'], 4), nf(m['carrossel']['quadratico'], 4), nf(m['carrossel']['exponencial'], 4),
            '%d de %d (%s)' % (m['mesmo_sinal']['k'], m['mesmo_sinal']['n'], m['mesmo_sinal']['sentido']))
    ordem = ['cl1999', 'tr2023', 'ec2025', 'sv2014', 'co2022', 'ar2023', 'cl2021', 'fr2022', 'br2026', 'br2022', 'br2018', 'br2014']
    for e in ordem:
        A(linha(El[e], El[e]['principal']) + ('  [fora da leitura principal]' if e == 'ec2025' else ''))
    A('Colunas: o = fatia dos válidos do 1º turno fora dos dois finalistas; S = desvio-padrão, entre as unidades, da variação da')
    A('fatia a dois do finalista B (2º turno menos 1º), em pontos, sem peso e com peso por votos; resíd. = resíduo da reta da fatia')
    A('a dois do 2º turno contra a do 1º; R² = receita do carrossel (x = fatia a dois de B no 1º turno, y = votos de A sobre votos')
    A('de B no 2º); mesmo sinal = unidades que andaram no sentido do movimento nacional. B = mais votado no 1º turno (no Brasil,')
    A('o adversário do PT). Equador 2025: 2º turno só em porcentagem parcial da imprensa, não conferível por soma.')
    A('')
    A('AS OUTRAS VERSÕES')
    A('  Com o exterior como uma unidade a mais (quando passa o filtro de 50 mil):')
    for e in ordem:
        E = El[e]; m = E['com_exterior']; p = E['principal']
        if m['n_unidades'] != p['n_unidades'] or abs(m['o'] - p['o']) > 0.005:
            A('    ' + linha(E, m))
    A('    Nas demais o exterior não existe como unidade separada (Argentina, Chile 1999) ou não passa o filtro (Chile 2021, El Salvador).')
    A('  Com as unidades pequenas agregadas em regiões oficiais (só França e Turquia têm mais de 30 unidades):')
    A('    ' + linha(El['fr2022'], El['fr2022']['agregado'], 'França 22 reg.+ultr'))
    A('    ' + linha(El['fr2022'], El['fr2022']['agregado_13_regioes'], 'França 13 reg.+ultr'))
    A('    ' + linha(El['tr2023'], El['tr2023']['agregado'], 'Turquia 26 sub-reg'))
    A('    Na França a agregação AUMENTA o S sem peso (de %s para %s) porque os territórios de ultramar, onde Macron despencou' % (nf(El['fr2022']['principal']['S_sem_peso']), nf(El['fr2022']['agregado']['S_sem_peso'])))
    A('    (Martinica %s pontos), passam a ser 5 de 27 pontos em vez de 5 de 100. Só com a metrópole (exploratório): %s com %d' % (nf(El['fr2022']['principal']['d_min'][1]), nf(X['E2_franca_so_metropole']['departamentos']['S']), X['E2_franca_so_metropole']['departamentos']['n']))
    A('    departamentos e %s com 22 regiões.' % nf(X['E2_franca_so_metropole']['22_regioes']['S']))
    A('  Receita do carrossel com os papéis de A e B trocados (só os R² mudam): exponencial de ' + '; '.join('%s %s' % (El[e]['rotulo'], nf(El[e]['principal']['carrossel_papeis_trocados']['exponencial'], 4)) for e in ordem) + '.')
    A('')
    A('A LEITURA FIXADA, PASSO A PASSO')
    A('  Eleições de fora que entraram (conferidas contra o total nacional oficial): ' + ', '.join(P['eleicoes'].keys()) + '.')
    A('  Conjunto comparável (o de 15% ou menos): ' + '; '.join('%s (o %s; S %s)' % (k, nf(v['o']), nf(v['S'])) for k, v in P['eleicoes'].items() if v['o'] <= 15) + '.')
    A('  Menor S do conjunto comparável: %s, %s. Metade: %s. 0,75 vez: %s.' % (l26['menor_S_comparavel'][0], nf(l26['menor_S_comparavel'][1], 3), nf(0.5 * l26['menor_S_comparavel'][1], 3), nf(0.75 * l26['menor_S_comparavel'][1], 3)))
    r = P['reta_S_contra_o']
    A('  Reta de S contra o nas %d eleições de fora: S = %s + %s x o; erro-padrão residual %s; R² %s.' % (r['n'], nf(r['intercepto'], 3), nf(r['inclinacao'], 4), nf(r['erro_padrao_residual']), nf(r['r2'])))
    for a, b in (('2026', b26), ('2022', b22)):
        lp = b['pela_predicao_95']; lc = b['pela_faixa_de_confianca_95']; e = r['em'][a]
        A('  %s: S = %s, o = %s. Razão para o menor S comparável: %s. Regra da metade (S menor que a metade): %s. Regra de 0,75: %s.' % (a, nf(b['S'], 3), nf(b['o']), nf(lp['razao']), 'SIM' if lp['regra_da_metade_S_menor_que_metade_do_menor'] else 'NÃO', 'CUMPRE' if lp['regra_075_S_pelo_menos_075_do_menor'] else 'NÃO CUMPRE'))
        A('        Reta no o de %s: ajuste %s; intervalo de predição de 95%% de %s a %s; faixa de confiança de 95%% de %s a %s.' % (a, nf(e['ajuste']), nf(e['predicao_95'][0]), nf(e['predicao_95'][1]), nf(e['confianca_95'][0]), nf(e['confianca_95'][1])))
        A('        Leitura pela letra: %s (pelo intervalo de predição) e %s (pela faixa de confiança).' % (lp['leitura'], lc['leitura']))
    A('  Aviso fixado antes (D11): o limite inferior do intervalo saiu NEGATIVO nas duas formas. A cláusula do intervalo ficou sem')
    A('  dentes: com 7 eleições e essa dispersão ela não consegue excluir valor nenhum de S. Quem decide a leitura é a regra de 0,75,')
    A('  e ela fecha por causa do Chile 1999/2000.')
    A('')
    A('  A mesma leitura nos outros recortes (2026; 2022):')
    for nome in ('agregado', 'com_exterior', 'so_nomeadas_conferidas', 'com_equador', 'com_equador_agregado', 'seis_nomeadas'):
        c = L[nome]; x26 = c['brasil']['2026']['pela_predicao_95']; x22 = c['brasil']['2022']['pela_predicao_95']
        det = ''
        if 'razao' in x26:
            det = ' Menor S comparável: %s %s; razões %s e %s; só pelas razões: %s; %s.' % (x26['menor_S_comparavel'][0], nf(x26['menor_S_comparavel'][1]), nf(x26['razao']), nf(x22['razao']), x26['leitura_so_pelas_razoes'], x22['leitura_so_pelas_razoes'])
        else:
            det = ' ' + x26.get('motivo', '') + '.'
        A('    %s: %s; %s.%s' % (c['descricao'], x26['leitura'], x22['leitura'], det))
    A('  Nos recortes sem o Chile 1999/2000 o "dentro do padrão" só fecha pela cláusula do intervalo, que está sem dentes; só pelas')
    A('  razões, 2026 fica entre a metade e 0,75 do menor S (Turquia) e 2022 fica abaixo da metade.')
    A('')
    A('  Descritivo, sem leitura: 2018 (S %s, o %s) e 2014 (S %s, o %s) ficam perto da reta (ajuste %s e %s), acima dela.' % (nf(P['brasil']['2018']['S']), nf(P['brasil']['2018']['o']), nf(P['brasil']['2014']['S']), nf(P['brasil']['2014']['o']), nf(P['brasil']['2018']['descritivo']['ajuste']), nf(P['brasil']['2014']['descritivo']['ajuste'])))
    A('')
    A('EXPLORATÓRIO (feito depois de ver o resultado; não entra na leitura)')
    A('  E1. S dividido por o (dispersão por ponto de voto a redistribuir): ' + '; '.join('%s %s' % (k, nf(v, 3)) for k, v in sorted(X['E1_S_sobre_o'].items(), key=lambda kv: kv[1])) + '.')
    e2 = X['E2_franca_so_metropole']
    A('  E2. França só com a metrópole (sem os territórios de ultramar): S %s e resíduo %s com %d departamentos (mesmo sinal em %d de %d);' % (nf(e2['departamentos']['S']), nf(e2['departamentos']['residuo']), e2['departamentos']['n'], e2['departamentos']['mesmo_sinal']['k'], e2['departamentos']['mesmo_sinal']['n']))
    A('      S %s e resíduo %s com as 22 regiões antigas (mesmo sinal em %d de %d). Com metade do 1º turno fora dos dois finalistas, as' % (nf(e2['22_regioes']['S']), nf(e2['22_regioes']['residuo']), e2['22_regioes']['mesmo_sinal']['k'], e2['22_regioes']['mesmo_sinal']['n']))
    A('      22 regiões da França andaram tão juntas quanto as 27 UFs do Brasil em 2026 (%s). Recorte escolhido depois de ver os dados.' % nf(El['br2026']['principal']['S_sem_peso']))
    A('  E3. Tirando uma eleição do conjunto comparável de cada vez (menor S que sobra; razão de 2026; razão de 2022). Incluir o')
    A('      Equador não muda nenhuma linha, porque o S dele nunca é o menor:')
    for k, v in X['E3_tirando_uma'].items():
        A('      %s: %s %s; %s; %s' % (k, v['menor'][0], nf(v['menor'][1]), nf(v['razao_2026']), nf(v['razao_2022'])))
    A('  E4. Sem o filtro de 50 mil (unidades; S): ' + '; '.join('%s %d; %s' % (k, v['n'], nf(v['S'])) for k, v in X['E4_sem_filtro'].items()) + '.')
    A('  E5. Eleições de 1º turno polarizado (o de 15% ou menos), da mais uniforme para a menos (S; resíduo; S sobre o; desvio-padrão')
    A('      da fatia a dois do 1º turno entre as unidades):')
    for v in X['E5_polarizadas']:
        A('      %-17s %s; %s; %s; %s' % (v['eleicao'], nf(v['S']), nf(v['residuo']), nf(v['S_sobre_o'], 3), nf(v['dp_p1'], 1)))
    e6 = X['E6_proporcional']
    A('  E6. S proporcional a o nas 7 eleições de fora da leitura: média geométrica de S sobre o = %s; intervalo de predição de 95%%' % nf(e6['S_sobre_o_media_geometrica'], 3))
    A('      de %s a %s. Brasil 2026: %s. Brasil 2022: %s. Os dois dentro.' % (nf(e6['intervalo_predicao_95_de_S_sobre_o'][0], 3), nf(e6['intervalo_predicao_95_de_S_sobre_o'][1], 3), nf(e6['brasil_2026_S_sobre_o'], 3), nf(e6['brasil_2022_S_sobre_o'], 3)))
    A('')
    A('O QUE PESA A FAVOR DA TESE, SEM AMACIAR')
    A('  - O "dentro do padrão" apoia-se numa eleição só. Sem o Chile 1999/2000, o menor S de eleição polarizada em papel é o da')
    sc = X['E3_tirando_uma']['sem Chile 1999/2000']
    ta = El['tr2023']['agregado']['S_sem_peso']
    A('    Turquia. Contra as 80 províncias (S de %s), 2026 fica em %s e 2022 em %s, abaixo da metade. Contra as 26 sub-regiões' % (nf(El['tr2023']['principal']['S_sem_peso']), nf(sc['razao_2026']), nf(sc['razao_2022'])))
    A('    (S de %s), 2026 fica em %s e 2022 em %s.' % (nf(ta), nf(El['br2026']['principal']['S_sem_peso'] / ta), nf(El['br2022']['principal']['S_sem_peso'] / ta)))
    A('  - Das quatro eleições de papel com 1º turno polarizado medidas aqui (três conferidas e o Equador), só o Chile 1999/2000 é')
    A('    tão uniforme quanto o Brasil. Turquia, Equador e El Salvador têm S de 1,15 a 1,60. Em S sobre o (exploratório), 2022 (0,064)')
    A('    e 2026 (0,088) ficam abaixo das quatro (0,107 a 0,201), embora acima de Chile 2021 (0,046) e, no caso de 2026, da França (0,075).')
    A('  - O R² exponencial de 2026 na receita do carrossel (0,9989 com 27 UFs) é o mais alto das 12 linhas da tabela, e o de 2022')
    A('    (0,9975) é o segundo.')
    A('  - O Chile 1999/2000 tem só 12 unidades e um 1º turno ainda mais fechado nos dois finalistas (95,5% contra 92%).')
    A('  - O Brasil é muito mais desigual entre as unidades do que o Chile de 1999: a fatia a dois do 1º turno varia de 25% a 76%')
    A('    entre as UFs (desvio de 15 pontos), contra 42% a 60% entre as regiões chilenas (desvio de 5,6). A eleição de fora mais')
    A('    parecida com o Brasil nesse ponto e na polarização é a Turquia, e lá a dispersão é maior.')
    A('  - A cláusula do intervalo de 95% não testou nada: o limite inferior é negativo. Com 7 eleições não há reta que preste.')
    A('  - A régua não alcança a hipótese H2 (troca igual em todos os estados): uma troca uniforme não muda o S. O teste não a afasta.')
    A('')
    A('O QUE PESA CONTRA A TESE')
    A('  - Existe eleição em papel, sem contestação, com apuração manual, em que o movimento entre os turnos foi MAIS uniforme do')
    A('    que no Brasil de 2026: Chile 1999/2000, S de 0,49 e resíduo de 0,37 entre 12 regiões (2026: 0,69 e 0,51; 2022: 0,53 e 0,53),')
    A('    com R² exponencial de 0,9961 na receita do carrossel (2026: 0,9989 com 27 UFs). Logo, esse grau de uniformidade não é')
    A('    "impossível" nem exclusivo de urna eletrônica.')
    A('  - O sinal igual em todas as unidades é comum quando o movimento nacional é grande perto do S: Argentina 24 de 24, Chile 2021')
    A('    15 de 15, El Salvador 14 de 14, Equador 23 de 23, Chile 1999/2000 11 de 12. "27 de 27" não distingue o Brasil.')
    A('  - O S cresce com o voto a redistribuir: as eleições com 30% a 49% fora dos dois finalistas têm S de 2,1 a 7,1; as com 4,5% a')
    A('    12% têm S de 0,5 a 1,6. O Brasil de 2022 e 2026 (8% fora dos finalistas) cai na faixa das polarizadas; o de 2014 e 2018')
    A('    (25%) cai na faixa das outras. O mesmo sistema de urna deu S de 3,4 e 4,0 quando havia 25% de votos a redistribuir.')
    A('  - O R² alto também aparece em papel quando o 1º turno é polarizado: 0,9961 no Chile 1999/2000, 0,9912 na Turquia por')
    A('    sub-região, 0,9886 no Equador. O R² sobe com a largura do eixo x, que no Brasil é o triplo da do Chile; na medida que não')
    A('    depende disso (o resíduo da reta), o Chile 1999/2000 é mais justo que o Brasil (0,37 contra 0,51).')
    A('  - Exploratório (E2): tirando os territórios de ultramar, as 22 regiões da França de 2022 têm S de %s, igual ao das UFs em' % nf(X['E2_franca_so_metropole']['22_regioes']['S']))
    A('    2026, mesmo com 49% do 1º turno fora dos dois finalistas. Unidades grandes andam mais juntas que unidades pequenas.')
    A('  - Pela regra registrada, as eleições que faltaram (Gana, Libéria, Serra Leoa) não poderiam virar a leitura para "fora":')
    A('    a regra usa o menor S, e mais eleições só podem baixar o menor.')
    A('')
    A('O QUE ISSO SIGNIFICA E O QUE NÃO SIGNIFICA')
    A('  Significa: o argumento do carrossel ("estados andarem tão juntos é matematicamente impossível de ser orgânico") cai. Numa')
    A('  eleição de papel com 1º turno quase todo nos dois finalistas, as regiões andaram tão juntas quanto os estados brasileiros.')
    A('  R² de 0,99 para cima é o que aparece, em papel, quando quase todo o 1º turno já está nos dois finalistas.')
    A('  Não significa: (1) que não houve fraude. O registro já avisava: estados andarem juntos é o que um movimento nacional')
    A('  produz e também o que uma troca uniforme produziria; a régua só diz se esse grau de uniformidade aparece em papel, e')
    A('  aparece. (2) Que o Brasil é típico: ele está na ponta uniforme da distribuição, e a comparação tem 3 eleições polarizadas')
    A('  conferidas (4 com o Equador). (3) Que 2022 serve de eleição limpa: recebeu a mesma leitura e também fica na ponta.')
    A('')
    A('FONTES E CONFERÊNCIA CONTRA O TOTAL NACIONAL OFICIAL (acesso em 10/11/2026)')
    for e in ordem[:8]:
        E = El[e]
        A('  %s [%s]. Fonte oficial direta: %s.' % (E['rotulo'], E['arquivo'], E['fonte_oficial_direta']))
        A('    Fonte: %s' % E['fonte'])
        A('    Conferência: %s' % E['conferencia_total_nacional'])
    A('  Conferências a mais: (1) Chile 1999/2000, a eleição de que a leitura depende, foi comparado também com as tabelas por')
    A('  região da Wikipedia em espanhol (es.wikipedia.org/wiki/Elección_presidencial_de_Chile_de_1999): os votos de Lagos e Lavín e os')
    A('  válidos batem em 12 das 13 regiões nos dois turnos; na Araucanía a Wikipedia traz 10 votos a menos para Lagos no 2º turno')
    A('  (erro de digitação de lá: no dado oficial a soma fecha com os válidos). (2) S, o, resíduo e sinal das 12 eleições foram refeitos com')
    A('  código separado (/home/user/trabalho-eleicao/adendo31/scripts/conferir_independente.py) e batem na segunda casa.')
    A('  Brasil 2014, 2018, 2022 e 2026: bases por seção de dados/ (bweb do TSE), somadas por UF; hashes conferidos com dados/SHA256SUMS.txt.')
    A('  S de 2026 = %s, 2022 = %s, 2018 = %s, 2014 = %s (o registro cita 0,69; 0,53; 3,38; 4,01). Com o exterior, a receita do carrossel' % tuple(nf(El['br' + a]['principal']['S_sem_peso'], 3) for a in ('2026', '2022', '2018', '2014')))
    A('  de 2026 dá %s; %s; %s (legenda do carrossel: 0,935; 0,995; 0,999).' % tuple(nf(El['br2026']['com_exterior']['carrossel'][k], 4) for k in ('linear', 'quadratico', 'exponencial')))
    A('')
    A('ELEIÇÕES PROCURADAS E NÃO OBTIDAS')
    for t in R['nao_obtidas']: A('  - ' + t)
    A('  Fontes oficiais que não abriram: Servel 2021 (só painéis Power BI; historico.servel.cl com erro 502), Registraduría da')
    A('  Colômbia (erro 403), YSK e Resmî Gazete da Turquia (sem resposta), CNE do Equador (captcha), DINE da Argentina (só o zip')
    A('  provisório da geral, sem o 2º turno). A Wikipedia limitou as requisições (erro 429) várias vezes; esperei e baixei devagar.')
    A('')
    A('DESVIOS E DECISÕES FORA DO REGISTRO')
    for i, t in enumerate(R['desvios'], 1): A('  %d. %s' % (i, t))
    A('')
    A('ARQUIVOS')
    A('  scripts/analisar_R31_regua_de_fora.py; resultados/R31_regua_de_fora.json e .txt; resultados/R31_tabelas/ (12 CSV, um por')
    A('  eleição, com fonte, data de acesso e conferência no cabeçalho, e _comparativa.csv). Montadores das tabelas e páginas')
    A('  baixadas: /home/user/trabalho-eleicao/adendo31/scripts/ e /home/user/trabalho-eleicao/adendo31/baixados/ (fora do repositório).')
    return '\n'.join(T) + '\n'


if __name__ == '__main__':
    if '--refazer-brasil' in sys.argv: refazer_brasil()
    R = calcular()
    R['leituras'] = leituras(R)
    with open(SAIDA_JSON, 'w', encoding='utf-8') as f:
        json.dump(R, f, ensure_ascii=False, indent=1)          # parcial: medidas e leituras, antes do exploratório
    R['exploratorio'] = exploratorio(R)
    R['nao_obtidas'] = NAO_OBTIDAS; R['desvios'] = DESVIOS
    P = R['leituras']['principal']['brasil']
    R['veredito'] = {'2026': P['2026']['pela_predicao_95']['leitura'], '2022': P['2022']['pela_predicao_95']['leitura'],
                     '2026_pela_faixa_de_confianca': P['2026']['pela_faixa_de_confianca_95']['leitura'], '2022_pela_faixa_de_confianca': P['2022']['pela_faixa_de_confianca_95']['leitura'],
                     'clausula_que_fechou': 'regra de 0,75 (S de 2026 e de 2022 maiores que 0,75 vez o menor S do conjunto comparável, que é o do Chile 1999/2000)',
                     'aviso': 'a cláusula do intervalo de 95% ficou sem dentes (limite inferior negativo); sem o Chile 1999/2000 a leitura só pelas razões seria inconclusiva para 2026 e abaixo da metade para 2022'}
    with open(SAIDA_JSON, 'w', encoding='utf-8') as f:
        json.dump(R, f, ensure_ascii=False, indent=1)
    txt = relatorio(R)
    with open(SAIDA_TXT, 'w', encoding='utf-8') as f:
        f.write(txt)
    with open(os.path.join(TAB, '_comparativa.csv'), 'w', encoding='utf-8', newline='') as f:
        w = csv.writer(f, delimiter=';')
        w.writerow(['eleicao', 'versao', 'tipo_de_voto', 'na_leitura_principal', 'unidades', 'o', 'S_sem_peso', 'S_com_peso', 'residuo', 'inclinacao', 'R2_linear', 'R2_quadratico', 'R2_exponencial', 'mesmo_sinal_k', 'mesmo_sinal_n', 'sentido'])
        for eid, E in R['eleicoes'].items():
            for v in ('principal', 'com_exterior', 'agregado', 'agregado_com_exterior', 'agregado_13_regioes'):
                if v not in E: continue
                m = E[v]
                w.writerow([E['rotulo'], v, E['tipo_de_voto'], E['na_leitura_principal'] if E['classe'] == 'fora' else 'Brasil', m['n_unidades'], '%.3f' % m['o'], '%.4f' % m['S_sem_peso'], '%.4f' % m['S_com_peso'],
                            '%.4f' % m['reta_p2_contra_p1']['residuo'], '%.4f' % m['reta_p2_contra_p1']['inclinacao'], '%.4f' % m['carrossel']['linear'], '%.4f' % m['carrossel']['quadratico'], '%.4f' % m['carrossel']['exponencial'],
                            m['mesmo_sinal']['k'], m['mesmo_sinal']['n'], m['mesmo_sinal']['sentido']])
    print('gravados', SAIDA_JSON, 'e', SAIDA_TXT)
    print('veredito:', R['veredito']['2026'], '(2026);', R['veredito']['2022'], '(2022)')
