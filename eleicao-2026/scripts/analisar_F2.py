"""F2 do Adendo 20: último dígito, porcentagens redondas e boletins repetidos, com o bweb completo dos dois turnos de 2026.

Registro (PRE-REGISTRO-2026-10-26.md, Adendo 20, commit d976d4d de 30/10/2026 12:11:50 UTC, antes de rodar):
  Todas as seções do Brasil; exterior fora.
  (a) Último dígito dos votos de Lula e de Flávio por seção, só contagens de 50 ou mais. Estatística: qui-quadrado contra
      uniforme. Referência: 200 simulações em que cada contagem é sorteada de uma binomial com a fatia do local de votação
      da seção, mesmo total de válidos. Sinal: o qui-quadrado observado de Lula ou de Flávio no 2º turno passa do
      percentil 99,9 das simulações e o do mesmo candidato no 1º turno fica abaixo do percentil 99. Sem sinal: abaixo do
      percentil 95 nos dois candidatos no 2º turno. Entre os dois: inconclusivo.
  (b) Porcentagens redondas: fração de seções em que 100 x Lula / válidos, ou 100 x comparecimento / aptos, cai a 0,1
      ponto ou menos de um múltiplo de 5. Mesma referência simulada. Sinal: excesso do observado sobre a média simulada
      acima de 4 desvios-padrão da simulação no 2º turno, para Lula ou para o comparecimento, e pelo menos o dobro do
      excesso padronizado do 1º turno. Sem sinal: dentro de 2 desvios-padrão. Entre os dois: inconclusivo.
  (c) Boletins repetidos: pares de seções da mesma zona com Lula, Flávio, branco e nulo idênticos no 2º turno,
      comparecimento de 100 ou mais. Esperado pela mesma simulação. Sinal: observado de pelo menos 3 vezes o esperado e
      20 pares ou mais. Sem sinal: até 1,5 vez o esperado.

Decisões onde o registro não fixa (tomadas e escritas aqui antes de calcular qualquer resultado; todas declaradas como
desvio no resultado):
  D1. Universo: seções com boletim nos dois turnos e UF diferente de ZZ (exterior). Cada turno usa os seus próprios
      números nas mesmas seções (controle "1º turno nas mesmas seções" do Adendo 20).
  D2. Válidos: no 2º turno, 13 + 22; no 1º turno, os nominais menos o 28 cassado (Adendo 6, como em T7, T23, T28 e T29).
      No 1º turno os votos do 28 entram no nulo.
  D3. Fatia do local: soma dos votos do candidato sobre a soma dos válidos de todas as seções do local de votação
      (UF, município, zona, NR_LOCAL_VOTACAO), no mesmo turno, com a própria seção incluída (leitura direta de "fatia do
      local de votação da seção").
  D4. Simulação de referência (uma por turno, 200 sorteios cada, usada em (a), (b) e (c)):
      2º turno: Lula* ~ Bin(V, fatia de Lula no local); Flávio* = V - Lula* (cada um com marginal binomial pela fatia do
      local e o mesmo total de válidos V da seção).
      1º turno: Lula* ~ Bin(V, pL); Flávio* | Lula* ~ Bin(V - Lula*, pR / (1 - pL)); outros* = V - Lula* - Flávio*
      (multinomial; cada contagem tem marginal Bin(V, fatia do local)).
      Comparecimento (só para (b)): C* ~ Bin(aptos, comparecimento do local / aptos do local). "Mesmo total" lido como
      os mesmos aptos da seção.
      Branco e nulo (só para (c), o registro não fala deles): B* ~ Bin(B + N, fatia do branco em branco + nulo no local),
      N* = (B + N) - B*. Válidos e branco mais nulo ficam como observados, logo o comparecimento também.
  D5. Semente: numpy SeedSequence(20261030).spawn(3): o primeiro fluxo para o 1º turno, o segundo para o 2º turno, o
      terceiro para a sensibilidade de (c). Gerador PCG64. Ordem dos sorteios fixa no código.
  D6. (a) "Só contagens de 50 ou mais" vale para cada conjunto de dados: no observado, contagens observadas >= 50; em cada
      simulação, contagens simuladas >= 50. Qui-quadrado de Pearson com 10 caselas, esperado n/10.
      Percentis das 200 simulações pelo método linear do numpy (padrão). Com 200 sorteios, o percentil 99,9 fica entre os
      dois maiores valores simulados. Vão ao lado, como descritivo: o número de simulações com qui-quadrado igual ou
      maior que o observado e o valor-p teórico do qui-quadrado com 9 graus de liberdade.
  D7. (b) "A 0,1 ponto ou menos de um múltiplo de 5": existe m inteiro com |100 x / y - 5 m| <= 0,1, calculado em inteiros
      (min(r, 50y - r) <= y, com r = 1000 x mod 50 y). Inclui 0 e 100. Todas as seções do universo (nenhuma tem válidos
      ou aptos zero). Lula e comparecimento são duas medidas separadas; a união vai como descritivo.
      Excesso padronizado z = (observado - média simulada) / desvio-padrão simulado (ddof = 1), em cada turno.
      Sinal: z do 2º turno > 4 e z do 2º turno >= 2 x z do 1º turno, na mesma medida, para Lula ou para o comparecimento.
      Sem sinal: |z do 2º turno| <= 2 nas duas medidas ("dentro de 2 desvios-padrão" lido como nos dois sentidos).
      O resto é inconclusivo.
  D8. (c) Zona = (UF, NR_ZONA); a zona pode ter mais de um município. Par = duas seções distintas da mesma zona, as duas
      com comparecimento >= 100 no 2º turno, com 13, 22, branco e nulo iguais. Contagem de pares = soma de m(m-1)/2 nos
      grupos de seções idênticas. Esperado = média dos pares nas 200 simulações do 2º turno. Conferência: o esperado
      exato do mesmo modelo (soma, nos pares com mesmos V e B + N, de P(Lula igual) x P(branco igual)).
      Sinal: observado >= 3 x esperado e observado >= 20. Sem sinal: observado <= 1,5 x esperado. O resto, inconclusivo.
  D9. Veredito do F2 como um todo (o registro dá um por item): SINAL se algum item der sinal; SEM SINAL se os três derem
      sem sinal; INCONCLUSIVO no resto. Os três itens são relatados separados.
  D10. Concentração por zona e município (pedida na tarefa, fora do critério, sem veredito): qui-quadrado do último dígito
      por zona e por município, só unidades com 100 contagens ou mais no observado (esperado de 10 por dígito); nas
      simulações, as mesmas unidades. Por unidade: valor-p teórico (qui-quadrado, 9 graus) e valor-p empírico
      (1 + simulações com qui-quadrado >= observado) / 201. Concentração medida pela soma dos qui-quadrados das unidades,
      pelo número de unidades acima do valor crítico de 0,1% e pelo maior qui-quadrado, cada um contra as 200 simulações.
      O 1º turno é o controle.
  D11. Descritivos fora do critério, sem veredito: dois últimos dígitos (contagens de 100 ou mais), último dígito do
      comparecimento (50 ou mais), qui-quadrado por UF e por faixa da fatia de Lula no local no 2º turno (a mesma faixa
      nos dois turnos), pares repetidos no mesmo
      local e no país inteiro, pares repetidos no 1º turno (13, 22, outros válidos, branco e nulo com o 28), e uma
      sensibilidade de (c) em que as quatro contagens são sorteadas juntas (multinomial pelo comparecimento da seção com
      as fatias do local), que não segura válidos nem branco mais nulo.

Acréscimos post hoc (escritos depois de ver o resultado do veredito; descritivos, sem veredito, sem mudar nada acima):
  D12. Lista das seções das zonas com valor-p teórico abaixo de 0,001 no último dígito do 2º turno (Lula ou Flávio),
      com local, urna e votos, para conferência nos arquivos de urna; margem da zona e margem nacional como escala.
  D13. Decomposição dos pares idênticos no país inteiro: pares com mesmos válidos, mesmo branco mais nulo e mesmo 13
      (ou mesmo branco), observado contra as mesmas simulações do 2º e do 1º turno.
  D14. Seções do 2º turno com comparecimento de 100% dos aptos.
  D15. Ordem de grandeza do poder de (a): quantas seções com último dígito inventado seriam precisas para passar do
      percentil 99,9, a partir da distância entre o observado e esse percentil.
  Nome do local: quando o número do local do bweb não está no cadastro atual, usa o nome do local original do cadastro.

Uso: python3 -I analisar_F2.py <secoes2026.json.gz> <saida.json> <saida.txt> [<pasta locais_votacao>]
"""
import os as _os, sys as _sys
_sys.path.insert(0, _os.path.dirname(_os.path.abspath(__file__)))
import csv, glob, io, json, math, os, sys, time
from multiprocessing import Pool
import numpy as np
from scipy import stats
from lib import carregar

SEMENTE = 20261030
NSIM = 200
MIN_DIG = 50
MIN_DIG2 = 100
MIN_COMP_PAR = 100
MIN_UNID = 100
RADIX = 512          # maior contagem possível por seção é 481 (comparecimento máximo)
Q2_CRIT = float(stats.chi2.isf(0.001, 9))
NTOP = 15

CRITERIO = {
    'a': ("Último dígito dos votos de Lula e de Flávio por seção, só contagens de 50 ou mais. Estatística: qui-quadrado "
          "contra uniforme. Referência: 200 simulações em que cada contagem é sorteada de uma binomial com a fatia do local "
          "de votação da seção, mesmo total de válidos. Sinal: o qui-quadrado observado de Lula ou de Flávio no 2º turno "
          "passa do percentil 99,9 das simulações e o do mesmo candidato no 1º turno fica abaixo do percentil 99. Sem "
          "sinal: abaixo do percentil 95 nos dois candidatos no 2º turno. Entre os dois: inconclusivo."),
    'b': ("Porcentagens redondas: fração de seções em que 100 x Lula / válidos, ou 100 x comparecimento / aptos, cai a 0,1 "
          "ponto ou menos de um múltiplo de 5. Mesma referência simulada. Sinal: excesso do observado sobre a média "
          "simulada acima de 4 desvios-padrão da simulação no 2º turno, para Lula ou para o comparecimento, e pelo menos o "
          "dobro do excesso padronizado do 1º turno. Sem sinal: dentro de 2 desvios-padrão. Entre os dois: inconclusivo."),
    'c': ("Boletins repetidos: pares de seções da mesma zona com Lula, Flávio, branco e nulo idênticos no 2º turno, "
          "comparecimento de 100 ou mais. Esperado pela mesma simulação. Sinal: observado de pelo menos 3 vezes o esperado "
          "e 20 pares ou mais. Sem sinal: até 1,5 vez o esperado."),
}

DECISOES = [
    "D1. Universo: seções com boletim nos dois turnos e UF diferente de ZZ (exterior); cada turno com os seus números nas mesmas seções.",
    "D2. Válidos: 2º turno 13 + 22; 1º turno nominais menos o 28 cassado (Adendo 6); no 1º turno o 28 entra no nulo.",
    "D3. Fatia do local: votos do candidato sobre válidos somados em todas as seções do local (UF, município, zona, NR_LOCAL_VOTACAO), no mesmo turno, com a própria seção incluída.",
    "D4. Simulação: 2º turno Lula* ~ Bin(V, fatia do local), Flávio* = V - Lula*; 1º turno multinomial (Lula, Flávio, outros) pelas fatias do local com o mesmo V; comparecimento* ~ Bin(aptos, comparecimento do local); branco* ~ Bin(B + N, fatia do branco no local), nulo* = (B + N) - branco*. Válidos e branco mais nulo ficam como observados em (c).",
    "D5. Semente numpy SeedSequence(20261030).spawn(3), PCG64: fluxo 1 para o 1º turno, 2 para o 2º, 3 para a sensibilidade de (c).",
    "D6. (a) O corte de 50 vale para cada conjunto (observado e cada simulação, cada um pelas suas contagens). Percentis pelo método linear do numpy; com 200 sorteios o percentil 99,9 fica entre os dois maiores. Valor-p teórico e número de simulações acima do observado vão como descritivo.",
    "D7. (b) Múltiplo de 5 calculado em inteiros, 0 e 100 incluídos, todas as seções; Lula e comparecimento como medidas separadas; z = (obs - média sim) / dp sim (ddof 1). Sinal: z2 > 4 e z2 >= 2 z1 na mesma medida. Sem sinal: |z2| <= 2 nas duas medidas.",
    "D8. (c) Zona = (UF, NR_ZONA). Pares = soma de m(m-1)/2 em grupos de seções idênticas (13, 22, branco, nulo) com comparecimento >= 100. Esperado = média das 200 simulações; conferido pelo esperado exato do mesmo modelo.",
    "D9. Veredito do F2: SINAL se algum item der sinal; SEM SINAL se os três derem sem sinal; INCONCLUSIVO no resto.",
    "D10. Concentração (fora do critério): qui-quadrado por zona e por município com 100 contagens ou mais; valor-p teórico e empírico; soma, contagem acima do valor crítico de 0,1% e máximo contra as simulações; 1º turno como controle.",
    "D12 a D15 (post hoc, depois do veredito, sem veredito): lista das seções das zonas com p teórico < 0,001 no 2º turno; decomposição dos pares no país; seções com 100% de comparecimento no 2º turno; ordem de grandeza do poder de (a).",
    "D11. Descritivos fora do critério: dois últimos dígitos (>= 100), último dígito do comparecimento (>= 50), por UF, por faixa da fatia de Lula no local no 2º turno (a mesma nos dois turnos), pares no mesmo local e no país, pares no 1º turno, e sensibilidade de (c) com as quatro contagens sorteadas juntas pelo comparecimento.",
]


# ---------------------------------------------------------------- formatação

def fi(x):
    return f"{int(x):,}".replace(',', '.')


def ff(x, d=2):
    if x is None or (isinstance(x, float) and not math.isfinite(x)):
        return 'n/d'
    s = f"{x:,.{d}f}"
    return s.replace(',', 'X').replace('.', ',').replace('X', '.')


def fp(p):
    if p is None:
        return 'n/d'
    if p < 1e-4:
        return f"{p:.1e}".replace('.', ',')
    return ff(p, 4)


# ---------------------------------------------------------------- dados

def montar(d):
    ks = sorted(k for k, v in d.items() if not k.startswith('ZZ|') and '1' in v and '2' in v)
    n = len(ks)
    A = {t: {f: np.zeros(n, np.int64) for f in ('L', 'R', 'Ov', 'B', 'N', 'apt', 'comp', 'urna')} for t in '12'}
    zona_k, mun_k, uf_k, loc_k = [], [], [], []
    o2_nao_zero = 0
    agr = np.zeros(n, bool)
    for i, k in enumerate(ks):
        u, m, z, s = k.split('|')
        uf_k.append(u); mun_k.append(f"{u}|{m}"); zona_k.append(f"{u}|{z}")
        loc_k.append(f"{u}|{m}|{z}|{d[k]['2']['loc']}")
        for t in '12':
            a = d[k][t]
            c28 = a.get('c28', 0)
            A[t]['L'][i] = a['L']; A[t]['R'][i] = a['R']
            A[t]['Ov'][i] = a['O'] - c28
            A[t]['B'][i] = a['B']; A[t]['N'][i] = a['N'] + c28
            A[t]['apt'][i] = a['apt']; A[t]['comp'][i] = a['comp']; A[t]['urna'][i] = a['urna']
            if t == '2' and a['O'] != 0:
                o2_nao_zero += 1
        if 'agr' in d[k]['2']:
            agr[i] = True
    ids = {}
    for nome, lst in (('zona', zona_k), ('mun', mun_k), ('uf', uf_k), ('loc', loc_k)):
        u, g = np.unique(np.array(lst), return_inverse=True)
        ids[nome] = g.astype(np.int64); ids[nome + '_nomes'] = u.tolist()
    for t in '12':
        a = A[t]
        a['V'] = a['L'] + a['R'] + a['Ov']
        a['BN'] = a['B'] + a['N']
        assert np.all(a['V'] + a['BN'] == a['comp']), 'soma das contagens diferente do comparecimento'
    return ks, A, ids, o2_nao_zero, agr


def fatias(a, loc, nl, turno):
    sb = lambda x: np.bincount(loc, weights=x, minlength=nl).astype(float)
    V, apt, BN, comp = sb(a['V']), sb(a['apt']), sb(a['BN']), sb(a['comp'])
    div = lambda x, y: np.where(y > 0, x / np.where(y > 0, y, 1), 0.0)
    P = {'pL': div(sb(a['L']), V)[loc], 'pR': div(sb(a['R']), V)[loc], 'tc': div(comp, apt)[loc],
         'qB': div(sb(a['B']), BN)[loc]}
    if turno == '2':
        for f in ('L', 'R', 'B', 'N'):
            P['a' + f] = div(sb(a[f]), comp)[loc]
    return P


def simular(rng, a, P, turno):
    V = a['V']
    L = rng.binomial(V, P['pL'])
    if turno == '2':
        R = V - L
    else:
        cond = np.where(P['pL'] < 1, P['pR'] / np.maximum(1 - P['pL'], 1e-300), 0.0)
        R = rng.binomial(V - L, np.clip(cond, 0, 1))
    C = rng.binomial(a['apt'], P['tc'])
    B = rng.binomial(a['BN'], P['qB'])
    N = a['BN'] - B
    Ov = V - L - R
    return {'L': L, 'R': R, 'C': C, 'B': B, 'N': N, 'Ov': Ov}


def simular_multinomial(rng, a, P):
    """Sensibilidade de (c): as quatro contagens sorteadas juntas pelo comparecimento da seção, fatias do local."""
    comp = a['comp']
    rest, prest = comp.copy(), np.ones_like(P['aL'])
    out = {}
    for f in ('L', 'R', 'B'):
        pc = np.clip(np.where(prest > 1e-12, P['a' + f] / np.maximum(prest, 1e-300), 0.0), 0, 1)
        x = rng.binomial(rest, pc)
        out[f] = x; rest = rest - x; prest = prest - P['a' + f]
    out['N'] = rest
    return out


# ---------------------------------------------------------------- estatísticas

def qui2(cnt):
    cnt = np.asarray(cnt, float)
    n = cnt.sum()
    if n == 0:
        return float('nan')
    e = n / len(cnt)
    return float(((cnt - e) ** 2).sum() / e)


def qui2_grupos(x, mask, g, ng):
    dg = x[mask] % 10
    M = np.bincount(g[mask] * 10 + dg, minlength=ng * 10).reshape(ng, 10)
    n = M.sum(1)
    e = n / 10.0
    q = ((M - e[:, None]) ** 2).sum(1) / np.where(e > 0, e, 1)
    return q, n, M


def redondo(x, y):
    r = (1000 * x) % (50 * y)
    dist = np.minimum(r, 50 * y - r)
    ok = dist <= y
    m = (40 * x + y) // (2 * y)    # múltiplo de 5 mais próximo, em unidades de 5 pontos (0 a 20)
    return ok, m


def chave_pares(g, campos, mask):
    key = g[mask].astype(np.int64)
    for c in campos:
        key = key * RADIX + c[mask]
    return key


def contar_pares(key):
    _, cnt = np.unique(key, return_counts=True)
    return int((cnt * (cnt - 1) // 2).sum())


def estat(x, a, ids, ng, faixa, turno):
    """x: contagens (observadas ou simuladas) com L, R, C, B, N, Ov."""
    out = {}
    for nome in ('L', 'R', 'C'):
        v = x[nome]
        m = v >= MIN_DIG
        cnt = np.bincount(v[m] % 10, minlength=10)
        out['dig_' + nome] = cnt
        out['q2_' + nome] = qui2(cnt)
        m2 = v >= MIN_DIG2
        out['q2d_' + nome] = qui2(np.bincount(v[m2] % 100, minlength=100))
        if nome in ('L', 'R'):
            for lv in ('zona', 'mun', 'uf'):
                q, n, M = qui2_grupos(v, m, ids[lv], ng[lv])
                out[f'g_{nome}_{lv}'] = (q, n, M)
            q, n, M = qui2_grupos(v, m, faixa, 10)
            out[f'g_{nome}_faixa'] = (q, n, M)
    okL, mL = redondo(x['L'], a['V'])
    okC, mC = redondo(x['C'], a['apt'])
    out['red_L'] = int(okL.sum()); out['red_C'] = int(okC.sum()); out['red_LouC'] = int((okL | okC).sum())
    out['red_L_mult'] = np.bincount(mL[okL], minlength=21)[:21]
    out['red_C_mult'] = np.bincount(mC[okC], minlength=21)[:21]
    ext_L = okL & ((mL == 0) | (mL == 20)); ext_C = okC & ((mC == 0) | (mC == 20))
    out['red_L_sem_0_100'] = int((okL & ~ext_L).sum()); out['red_C_sem_0_100'] = int((okC & ~ext_C).sum())
    mp = a['comp'] >= MIN_COMP_PAR
    campos = (x['L'], x['R'], x['B'], x['N']) if turno == '2' else (x['L'], x['R'], x['Ov'], x['B'], x['N'])
    out['pares_zona'] = contar_pares(chave_pares(ids['zona'], campos, mp))
    out['pares_local'] = contar_pares(chave_pares(ids['loc'], campos, mp))
    z0 = np.zeros_like(ids['zona'])
    out['pares_pais'] = contar_pares(chave_pares(z0, campos, mp))
    out['pares_pais_VBN_L'] = contar_pares(chave_pares(z0, (a['V'], a['BN'], x['L']), mp))
    out['pares_pais_VBN_B'] = contar_pares(chave_pares(z0, (a['V'], a['BN'], x['B']), mp))
    return out


def resumo_sim(vals):
    v = np.asarray(vals, float)
    p95, p99, p999 = np.percentile(v, [95, 99, 99.9])
    return {'media': float(v.mean()), 'dp': float(v.std(ddof=1)), 'p95': float(p95), 'p99': float(p99),
            'p999': float(p999), 'min': float(v.min()), 'max': float(v.max())}


def esperado_exato_pares(a, P, ids):
    """Esperado exato de pares em (c) sob a simulação D4: só pares com mesmos V e B + N podem coincidir."""
    mp = np.where(a['comp'] >= MIN_COMP_PAR)[0]
    key = (ids['zona'][mp] * 1024 + a['V'][mp]) * 1024 + a['BN'][mp]
    order = np.argsort(key, kind='stable')
    ks = key[order]; idx = mp[order]
    cortes = np.flatnonzero(np.diff(ks)) + 1
    tot = 0.0; npares = 0
    for grp in np.split(idx, cortes):
        if len(grp) < 2:
            continue
        V = int(a['V'][grp[0]]); BN = int(a['BN'][grp[0]])
        kL = np.arange(V + 1)
        PL = stats.binom.pmf(kL[None, :], V, P['pL'][grp][:, None])
        GL = PL @ PL.T
        if BN > 0:
            kB = np.arange(BN + 1)
            PB = stats.binom.pmf(kB[None, :], BN, P['qB'][grp][:, None])
            GB = PB @ PB.T
        else:
            GB = np.ones_like(GL)
        iu = np.triu_indices(len(grp), 1)
        tot += float((GL[iu] * GB[iu]).sum()); npares += len(iu[0])
    return tot, npares


# ---------------------------------------------------------------- nomes (opcional)

def _ler_nomes(caminho):
    mun, loc, orig = {}, {}, {}
    with open(caminho, encoding='latin1', newline='') as fh:
        rd = csv.reader(fh, delimiter=';')
        cab = next(rd)
        ix = {c: i for i, c in enumerate(cab)}
        for r in rd:
            u = r[ix['SG_UF']]; m = int(r[ix['CD_MUNICIPIO']]); z = int(r[ix['NR_ZONA']])
            mun[f"{u}|{m}"] = r[ix['NM_MUNICIPIO']]
            loc[f"{u}|{m}|{z}|{int(r[ix['NR_LOCAL_VOTACAO']])}"] = r[ix['NM_LOCAL_VOTACAO']]
            if r[ix['NR_LOCAL_VOTACAO_ORIGINAL']] not in ('', '-1', '#NULO#'):
                orig.setdefault(f"{u}|{m}|{z}|{int(r[ix['NR_LOCAL_VOTACAO_ORIGINAL']])}", r[ix['NM_LOCAL_VOTACAO_ORIGINAL']] + ' (local original no cadastro)')
    for k, v in orig.items():
        loc.setdefault(k, v)
    return mun, loc


def ler_nomes(pasta):
    arqs = sorted(glob.glob(os.path.join(pasta, 'eleitorado_local_votacao_2026_*.csv')))
    mun, loc = {}, {}
    with Pool(4) as pool:
        for m, l in pool.imap_unordered(_ler_nomes, arqs):
            mun.update(m); loc.update(l)
    return mun, loc


# ---------------------------------------------------------------- principal

def main():
    t0 = time.time()
    entrada, saida_json, saida_txt = sys.argv[1], sys.argv[2], sys.argv[3]
    pasta_locais = sys.argv[4] if len(sys.argv) > 4 else None
    d = carregar(entrada)
    n_total = {t: sum(1 for v in d.values() if t in v) for t in '12'}
    n_zz = {t: sum(1 for k, v in d.items() if k.startswith('ZZ|') and t in v) for t in '12'}
    ks, A, ids, o2_nao_zero, agr = montar(d)
    del d
    n = len(ks)
    ng = {lv: len(ids[lv + '_nomes']) for lv in ('zona', 'mun', 'uf', 'loc')}
    print(f'{n} seções; {ng}; {time.time()-t0:.0f}s', flush=True)

    P = {t: fatias(A[t], ids['loc'], ng['loc'], t) for t in '12'}
    # faixa da fatia de Lula no local (2º turno), a mesma nos dois turnos e fixa nas simulações
    f2 = np.minimum((P['2']['pL'] * 10).astype(np.int64), 9)
    faixa = {'1': f2, '2': f2}

    ss = np.random.SeedSequence(SEMENTE)
    s1, s2, s3 = ss.spawn(3)
    rngs = {'1': np.random.Generator(np.random.PCG64(s1)), '2': np.random.Generator(np.random.PCG64(s2))}
    rng3 = np.random.Generator(np.random.PCG64(s3))

    OBS, SIM = {}, {}
    for t in '12':
        a = A[t]
        x = {'L': a['L'], 'R': a['R'], 'C': a['comp'], 'B': a['B'], 'N': a['N'], 'Ov': a['Ov']}
        OBS[t] = estat(x, a, ids, ng, faixa[t], t)
        sims = []
        for s in range(NSIM):
            xs = simular(rngs[t], a, P[t], t)
            e = estat(xs, a, ids, ng, faixa[t], t)
            # guarda só o necessário dos grupos
            for k in list(e):
                if k.startswith('g_'):
                    e[k] = (e[k][0].astype(np.float32), e[k][1].astype(np.int32))
            sims.append(e)
            if s % 50 == 49:
                print(f'turno {t}: {s+1} simulações, {time.time()-t0:.0f}s', flush=True)
        SIM[t] = sims

    # sensibilidade de (c)
    sens = []
    a2 = A['2']; mp2 = a2['comp'] >= MIN_COMP_PAR
    for s in range(NSIM):
        xs = simular_multinomial(rng3, a2, P['2'])
        sens.append(contar_pares(chave_pares(ids['zona'], (xs['L'], xs['R'], xs['B'], xs['N']), mp2)))
    print(f'sensibilidade pronta, {time.time()-t0:.0f}s', flush=True)

    E_exato, n_pares_cand = esperado_exato_pares(a2, P['2'], ids)
    print(f'esperado exato {E_exato:.2f} em {n_pares_cand} pares candidatos, {time.time()-t0:.0f}s', flush=True)

    R = {'teste': 'F2 (Adendo 20): último dígito, porcentagens redondas e boletins repetidos',
         'registro': 'PRE-REGISTRO-2026-10-26.md, Adendo 20, commit d976d4d (30/10/2026 12:11:50 UTC)',
         'criterio': CRITERIO, 'decisoes_declaradas_como_desvio': DECISOES,
         'semente': SEMENTE, 'nsim': NSIM,
         'universo': {'boletins_1T': n_total['1'], 'boletins_2T': n_total['2'], 'exterior_1T': n_zz['1'],
                      'exterior_2T': n_zz['2'], 'secoes_nos_dois_turnos_sem_exterior': n,
                      'zonas': ng['zona'], 'municipios': ng['mun'], 'locais': ng['loc'],
                      'secoes_2T_com_outros_nominais_diferente_de_zero': o2_nao_zero}}

    # ---------------- (a)
    ra = {}
    for t in '12':
        for c in ('L', 'R'):
            sv = [e['q2_' + c] for e in SIM[t]]
            obs = OBS[t]['q2_' + c]
            rs = resumo_sim(sv)
            dig = OBS[t]['dig_' + c]
            dsim = np.array([e['dig_' + c] for e in SIM[t]], float)
            nobs = int(dig.sum())
            ra[f'{c}_{t}T'] = {
                'n_contagens': nobs, 'qui2': obs, 'sim': rs,
                'sims_maior_ou_igual': int(sum(1 for v in sv if v >= obs)),
                'p_teorico_qui2_9gl': float(stats.chi2.sf(obs, 9)),
                'conferencia_scipy_chisquare': float(stats.chisquare(dig).statistic),
                'digitos_obs': dig.tolist(),
                'digitos_frac_obs': (dig / nobs).tolist(),
                'digitos_sim_media_frac': (dsim / dsim.sum(1, keepdims=True)).mean(0).tolist(),
                'digitos_z': ((dig / nobs - (dsim / dsim.sum(1, keepdims=True)).mean(0))
                              / (dsim / dsim.sum(1, keepdims=True)).std(0, ddof=1)).tolist(),
            }
    cond = {}
    for c in ('L', 'R'):
        a2_, a1_ = ra[f'{c}_2T'], ra[f'{c}_1T']
        cond[c] = {'2T_acima_p999': a2_['qui2'] > a2_['sim']['p999'], '1T_abaixo_p99': a1_['qui2'] < a1_['sim']['p99'],
                   '2T_abaixo_p95': a2_['qui2'] < a2_['sim']['p95']}
    if any(cond[c]['2T_acima_p999'] and cond[c]['1T_abaixo_p99'] for c in cond):
        va = 'SINAL'
    elif all(cond[c]['2T_abaixo_p95'] for c in cond):
        va = 'SEM SINAL'
    else:
        va = 'INCONCLUSIVO'
    ra['condicoes'] = cond; ra['veredito'] = va

    # concentração por zona, município, UF, faixa
    conc = {}
    nomes_mun, nomes_loc = ({}, {})
    if pasta_locais:
        nomes_mun, nomes_loc = ler_nomes(pasta_locais)
        print(f'nomes lidos: {len(nomes_mun)} municípios, {len(nomes_loc)} locais, {time.time()-t0:.0f}s', flush=True)
    for lv in ('zona', 'mun', 'uf', 'faixa'):
        conc[lv] = {}
        for t in '12':
            for c in ('L', 'R'):
                qo, no, Mo = OBS[t][f'g_{c}_{lv}']
                minu = MIN_UNID if lv in ('zona', 'mun') else 1
                sel = np.flatnonzero(no >= minu)
                qs = np.array([e[f'g_{c}_{lv}'][0][sel] for e in SIM[t]], float)   # NSIM x unidades
                qsel = qo[sel]
                pemp = (1 + (qs >= qsel[None, :]).sum(0)) / (NSIM + 1)
                pteo = stats.chi2.sf(qsel, 9)
                S_obs = float(qsel.sum()); S_sim = qs.sum(1)
                K_obs = int((qsel > Q2_CRIT).sum()); K_sim = (qs > Q2_CRIT).sum(1)
                X_obs = float(qsel.max()) if len(sel) else float('nan'); X_sim = qs.max(1)
                ent = {'unidades': int(len(sel)),
                       'soma_qui2_obs': S_obs, 'soma_qui2_sim': resumo_sim(S_sim),
                       'soma_sims_maior_ou_igual': int((S_sim >= S_obs).sum()),
                       'n_acima_critico_0_1pct_obs': K_obs, 'n_acima_critico_sim': resumo_sim(K_sim),
                       'n_acima_sims_maior_ou_igual': int((K_sim >= K_obs).sum()),
                       'max_qui2_obs': X_obs, 'max_qui2_sim': resumo_sim(X_sim),
                       'max_sims_maior_ou_igual': int((X_sim >= X_obs).sum())}
                if lv in ('uf', 'faixa') or t == '2':
                    ordem = np.argsort(-qsel) if lv in ('zona', 'mun') else np.arange(len(sel))
                    lst = []
                    for j in (ordem[:NTOP * 2] if lv in ('zona', 'mun') else ordem):
                        u = int(sel[j])
                        nome_u = (ids[lv + '_nomes'][u] if lv != 'faixa' else f'{u*10}-{u*10+10}%')
                        ent_u = {'unidade': nome_u, 'n': int(no[u]), 'qui2': float(qo[u]), 'p_teorico': float(pteo[j]),
                                 'p_empirico': float(pemp[j]), 'digitos': Mo[u].tolist()}
                        if lv == 'mun':
                            ent_u['nome'] = nomes_mun.get(nome_u, '')
                        lst.append(ent_u)
                    ent['unidades_lista'] = lst
                    ent['n_p_teorico_abaixo_0_001'] = int((pteo < 0.001).sum())
                    ent['n_p_empirico_minimo'] = int((pemp <= 1 / (NSIM + 1) + 1e-12).sum())
                conc[lv][f'{c}_{t}T'] = ent
    # completar as listas do 2º turno com o 1º turno da mesma unidade e o outro candidato
    for lv in ('zona', 'mun'):
        for c in ('L', 'R'):
            outro = 'R' if c == 'L' else 'L'
            for ent_u in conc[lv][f'{c}_2T']['unidades_lista']:
                u = ids[lv + '_nomes'].index(ent_u['unidade'])
                q1, n1, _ = OBS['1'][f'g_{c}_{lv}']
                qo2, no2, _ = OBS['2'][f'g_{outro}_{lv}']
                ent_u['qui2_mesmo_candidato_1T'] = float(q1[u]); ent_u['n_1T'] = int(n1[u])
                ent_u['p_teorico_1T'] = float(stats.chi2.sf(q1[u], 9)) if n1[u] > 0 else None
                ent_u['qui2_outro_candidato_2T'] = float(qo2[u]); ent_u['n_outro_2T'] = int(no2[u])
                ent_u['fatia_Lula_2T'] = None
    # fatia de Lula por zona e município, 2º turno
    for lv in ('zona', 'mun'):
        g = ids[lv]
        Ls = np.bincount(g, weights=A['2']['L'], minlength=ng[lv]); Vs = np.bincount(g, weights=A['2']['V'], minlength=ng[lv])
        for c in ('L', 'R'):
            for ent_u in conc[lv][f'{c}_2T']['unidades_lista']:
                u = ids[lv + '_nomes'].index(ent_u['unidade'])
                ent_u['fatia_Lula_2T'] = float(Ls[u] / Vs[u])
    ra['concentracao'] = conc

    # ---------------- (b)
    rb = {}
    for t in '12':
        for med in ('L', 'C'):
            obs = OBS[t]['red_' + med]
            sv = np.array([e['red_' + med] for e in SIM[t]], float)
            mu, sd = sv.mean(), sv.std(ddof=1)
            mult_o = OBS[t][f'red_{med}_mult']
            mult_s = np.array([e[f'red_{med}_mult'] for e in SIM[t]], float)
            so = OBS[t][f'red_{med}_sem_0_100']
            ss_ = np.array([e[f'red_{med}_sem_0_100'] for e in SIM[t]], float)
            rb[f'{med}_{t}T'] = {'secoes': n, 'obs': int(obs), 'frac_obs': obs / n, 'sim_media': float(mu),
                                 'sim_dp': float(sd), 'frac_sim_media': float(mu / n), 'z': float((obs - mu) / sd),
                                 'por_multiplo': [{'pct': 5 * m, 'obs': int(mult_o[m]), 'sim_media': float(mult_s[:, m].mean()),
                                                   'sim_dp': float(mult_s[:, m].std(ddof=1)),
                                                   'z': float((mult_o[m] - mult_s[:, m].mean()) / mult_s[:, m].std(ddof=1))
                                                   if mult_s[:, m].std(ddof=1) > 0 else None} for m in range(21)],
                                 'sem_0_e_100': {'obs': int(so), 'sim_media': float(ss_.mean()), 'sim_dp': float(ss_.std(ddof=1)),
                                                 'z': float((so - ss_.mean()) / ss_.std(ddof=1))}}
        obs = OBS[t]['red_LouC']; sv = np.array([e['red_LouC'] for e in SIM[t]], float)
        rb[f'LouC_{t}T'] = {'obs': int(obs), 'sim_media': float(sv.mean()), 'sim_dp': float(sv.std(ddof=1)),
                            'z': float((obs - sv.mean()) / sv.std(ddof=1))}
    condb = {}
    for med in ('L', 'C'):
        z2, z1 = rb[f'{med}_2T']['z'], rb[f'{med}_1T']['z']
        condb[med] = {'z2': z2, 'z1': z1, 'z2_acima_4': z2 > 4, 'z2_pelo_menos_2z1': z2 >= 2 * z1, 'abs_z2_ate_2': abs(z2) <= 2}
    if any(condb[m]['z2_acima_4'] and condb[m]['z2_pelo_menos_2z1'] for m in condb):
        vb = 'SINAL'
    elif all(condb[m]['abs_z2_ate_2'] for m in condb):
        vb = 'SEM SINAL'
    else:
        vb = 'INCONCLUSIVO'
    rb['condicoes'] = condb; rb['veredito'] = vb

    # ---------------- (c)
    rc = {}
    obs_c = OBS['2']['pares_zona']
    sv = np.array([e['pares_zona'] for e in SIM['2']], float)
    E = float(sv.mean())
    rc['zona_2T'] = {'obs': obs_c, 'esperado_sim': E, 'sim_dp': float(sv.std(ddof=1)), 'sim': resumo_sim(sv),
                     'esperado_exato_mesmo_modelo': E_exato, 'pares_candidatos_mesmo_V_e_BN': n_pares_cand,
                     'razao_obs_esperado': obs_c / E if E > 0 else None,
                     'sims_maior_ou_igual': int((sv >= obs_c).sum()),
                     'p_poisson_obs_ou_mais': float(stats.poisson.sf(obs_c - 1, E))}
    if obs_c >= 3 * E and obs_c >= 20:
        vc = 'SINAL'
    elif obs_c <= 1.5 * E:
        vc = 'SEM SINAL'
    else:
        vc = 'INCONCLUSIVO'
    rc['veredito'] = vc
    for t in '12':
        for esc in ('zona', 'local', 'pais'):
            if t == '2' and esc == 'zona':
                continue
            o = OBS[t]['pares_' + esc]; s_ = np.array([e['pares_' + esc] for e in SIM[t]], float)
            rc[f'{esc}_{t}T'] = {'obs': int(o), 'esperado_sim': float(s_.mean()), 'sim_dp': float(s_.std(ddof=1)),
                                 'razao': o / s_.mean() if s_.mean() > 0 else None,
                                 'sims_maior_ou_igual': int((s_ >= o).sum())}
    sens = np.array(sens, float)
    rc['sensibilidade_multinomial_pelo_comparecimento'] = {'esperado_sim': float(sens.mean()), 'sim_dp': float(sens.std(ddof=1)),
                                                           'razao_obs_esperado': obs_c / sens.mean() if sens.mean() > 0 else None}
    # lista dos pares observados
    mp = np.flatnonzero(a2['comp'] >= MIN_COMP_PAR)
    key = chave_pares(ids['zona'], (a2['L'], a2['R'], a2['B'], a2['N']), a2['comp'] >= MIN_COMP_PAR)
    _, inv, cnt = np.unique(key, return_inverse=True, return_counts=True)
    grupos = {}
    for j in np.flatnonzero(cnt[inv] >= 2):
        grupos.setdefault(int(inv[j]), []).append(int(mp[j]))
    a1 = A['1']
    lista = []
    for gi, membros in grupos.items():
        sec = []
        for i in membros:
            k = ks[i]; u, m, z, s = k.split('|'); lk = ids['loc_nomes'][ids['loc'][i]]
            sec.append({'secao': k, 'local': lk, 'nome_local': nomes_loc.get(lk, ''), 'municipio': nomes_mun.get(f'{u}|{m}', ''),
                        'urna_2T': int(a2['urna'][i]), 'apt': int(a2['apt'][i]), 'comp_2T': int(a2['comp'][i]),
                        'L2': int(a2['L'][i]), 'R2': int(a2['R'][i]), 'B2': int(a2['B'][i]), 'N2': int(a2['N'][i]),
                        'L1': int(a1['L'][i]), 'R1': int(a1['R'][i]), 'O1': int(a1['Ov'][i]), 'B1': int(a1['B'][i]),
                        'N1': int(a1['N'][i]), 'comp_1T': int(a1['comp'][i]), 'agregada': bool(agr[i]),
                        'fatia_Lula_local_2T': float(P['2']['pL'][i])})
        # probabilidade exata do par sob o modelo (só para o primeiro par do grupo)
        i, j = membros[0], membros[1]
        V = int(a2['V'][i]); BN = int(a2['BN'][i]); kL = np.arange(V + 1)
        pl = float((stats.binom.pmf(kL, V, P['2']['pL'][i]) * stats.binom.pmf(kL, V, P['2']['pL'][j])).sum())
        kB = np.arange(BN + 1)
        pb = float((stats.binom.pmf(kB, BN, P['2']['qB'][i]) * stats.binom.pmf(kB, BN, P['2']['qB'][j])).sum()) if BN > 0 else 1.0
        mesmo_local = len(set(x_['local'] for x_ in sec)) == 1
        mesmo_1T = len(set((x_['L1'], x_['R1'], x_['O1'], x_['B1'], x_['N1']) for x_ in sec)) == 1
        lista.append({'secoes': sec, 'tamanho': len(membros), 'mesmo_local': mesmo_local, 'tambem_igual_no_1T': mesmo_1T,
                      'mesma_urna': len(set(x_['urna_2T'] for x_ in sec)) < len(sec),
                      'prob_par_no_modelo': pl * pb})
    lista.sort(key=lambda g: g['prob_par_no_modelo'])
    rc['pares_observados'] = lista
    rc['resumo_pares_observados'] = {'grupos': len(lista), 'no_mesmo_local': sum(g['mesmo_local'] for g in lista),
                                     'iguais_tambem_no_1T': sum(g['tambem_igual_no_1T'] for g in lista),
                                     'com_mesma_urna': sum(g['mesma_urna'] for g in lista),
                                     'com_secao_agregada': sum(any(s_['agregada'] for s_ in g['secoes']) for g in lista)}

    # ---------------- descritivos
    rd = {}
    for t in '12':
        for c in ('L', 'R', 'C'):
            for k_, rot in (('q2d_', 'dois_digitos'), ('q2_', 'ultimo_digito')):
                if c != 'C' and k_ == 'q2_':
                    continue
                obs = OBS[t][k_ + c]; sv = [e[k_ + c] for e in SIM[t]]
                gl = 99 if k_ == 'q2d_' else 9
                rd[f'{rot}_{c}_{t}T'] = {'qui2': obs, 'sim': resumo_sim(sv), 'sims_maior_ou_igual': int(sum(1 for v in sv if v >= obs)),
                                         'p_teorico': float(stats.chi2.sf(obs, gl)),
                                         'n': int(OBS[t]['dig_' + c].sum()) if k_ == 'q2_' else None}
    # ---------------- post hoc (D12 a D15), descritivos sem veredito
    ph = {}
    zg = ids['zona']
    Lz = np.bincount(zg, weights=a2['L'], minlength=ng['zona']); Rz = np.bincount(zg, weights=a2['R'], minlength=ng['zona'])
    ph['margem_nacional_2T_sem_exterior'] = {'L': int(a2['L'].sum()), 'R': int(a2['R'].sum()), 'margem_L_menos_R': int(a2['L'].sum() - a2['R'].sum())}
    d12 = []
    for cnd in ('L', 'R'):
        for ent_u in conc['zona'][f'{cnd}_2T']['unidades_lista']:
            if ent_u['p_teorico'] >= 0.001:
                continue
            u = ids['zona_nomes'].index(ent_u['unidade'])
            dmax = int(np.argmax(ent_u['digitos']))
            sel = np.flatnonzero((zg == u) & (a2[cnd] >= MIN_DIG))
            secs = []
            for i in sel:
                if a2[cnd][i] % 10 != dmax:
                    continue
                k = ks[i]; uu, mm, _, _ = k.split('|'); lk = ids['loc_nomes'][ids['loc'][i]]
                secs.append({'secao': k, 'municipio': nomes_mun.get(f'{uu}|{mm}', ''), 'local': lk, 'nome_local': nomes_loc.get(lk, ''),
                             'urna_2T': int(a2['urna'][i]), 'apt': int(a2['apt'][i]), 'comp_2T': int(a2['comp'][i]),
                             'L2': int(a2['L'][i]), 'R2': int(a2['R'][i]), 'B2': int(a2['B'][i]), 'N2': int(a2['N'][i]),
                             'L1': int(a1['L'][i]), 'R1': int(a1['R'][i])})
            n_locais = len(set(s_['local'] for s_ in secs))
            n_locais_zona = len(set(int(ids['loc'][i]) for i in sel))
            d12.append({'zona': ent_u['unidade'], 'candidato': NOME[cnd], 'n': ent_u['n'], 'qui2': ent_u['qui2'], 'p_teorico': ent_u['p_teorico'],
                        'p_empirico': ent_u['p_empirico'], 'digito_mais_comum': dmax, 'secoes_com_esse_digito': len(secs),
                        'esperado_uniforme': ent_u['n'] / 10, 'locais_dessas_secoes': n_locais, 'locais_da_zona': n_locais_zona,
                        'municipios_da_zona': sorted(set(nomes_mun.get('|'.join(ks[i].split('|')[:2]), ks[i].split('|')[1]) for i in sel)),
                        'votos_L_zona_2T': int(Lz[u]), 'votos_R_zona_2T': int(Rz[u]), 'margem_zona_L_menos_R': int(Lz[u] - Rz[u]),
                        'secoes': secs})
    ph['D12_zonas_p_teorico_abaixo_0_001'] = d12
    d13 = {}
    for t in '21':
        for k_ in ('pares_pais_VBN_L', 'pares_pais_VBN_B', 'pares_pais'):
            o_ = OBS[t][k_]; s_ = np.array([e[k_] for e in SIM[t]], float)
            d13[f'{k_}_{t}T'] = {'obs': int(o_), 'sim_media': float(s_.mean()), 'sim_dp': float(s_.std(ddof=1)),
                                 'razao': float(o_ / s_.mean()), 'z': float((o_ - s_.mean()) / s_.std(ddof=1))}
    ph['D13_decomposicao_pares_pais'] = d13
    d14 = []
    for i in np.flatnonzero(a2['comp'] == a2['apt']):
        k = ks[i]; uu, mm, _, _ = k.split('|'); lk = ids['loc_nomes'][ids['loc'][i]]
        d14.append({'secao': k, 'municipio': nomes_mun.get(f'{uu}|{mm}', ''), 'nome_local': nomes_loc.get(lk, ''),
                    'apt': int(a2['apt'][i]), 'comp_2T': int(a2['comp'][i]), 'L2': int(a2['L'][i]), 'R2': int(a2['R'][i]),
                    'B2': int(a2['B'][i]), 'N2': int(a2['N'][i]), 'apt_1T': int(a1['apt'][i]), 'comp_1T': int(a1['comp'][i]),
                    'L1': int(a1['L'][i]), 'R1': int(a1['R'][i]), 'O1': int(a1['Ov'][i])})
    ph['D14_comparecimento_100pct_2T'] = d14
    d15 = {}
    for cnd in ('L', 'R'):
        x = ra[f'{cnd}_2T']; gap = max(x['sim']['p999'] - x['qui2'], 0.0); nn = x['n_contagens']
        d15[cnd] = {'distancia_ate_p999': gap, 'n': nn,
                    'secoes_todas_num_digito': math.sqrt(gap * nn / 9.0),
                    'secoes_metade_0_metade_5': math.sqrt(gap * nn / 4.0)}
    ph['D15_poder_aproximado'] = d15
    R['post_hoc'] = ph

    R['a'] = ra; R['b'] = rb; R['c'] = rc; R['descritivos'] = rd
    vs = [va, vb, vc]
    R['veredito_F2'] = 'SINAL' if 'SINAL' in vs else ('SEM SINAL' if all(v == 'SEM SINAL' for v in vs) else 'INCONCLUSIVO')
    R['tempo_s'] = time.time() - t0

    def conv(o):
        if isinstance(o, dict): return {k: conv(v) for k, v in o.items()}
        if isinstance(o, (list, tuple)): return [conv(v) for v in o]
        if isinstance(o, (np.integer,)): return int(o)
        if isinstance(o, (np.floating,)): return float(o)
        if isinstance(o, np.bool_): return bool(o)
        if isinstance(o, np.ndarray): return conv(o.tolist())
        return o
    R = conv(R)
    with open(saida_json, 'w') as f:
        json.dump(R, f, ensure_ascii=False, indent=1)
    with open(saida_txt, 'w') as f:
        f.write(texto(R))
    print(f'pronto em {time.time()-t0:.0f}s', flush=True)


# ---------------------------------------------------------------- texto

NOME = {'L': 'Lula', 'R': 'Flávio', 'C': 'comparecimento'}


def texto(R):
    o = []
    w = o.append
    a, b, c, u = R['a'], R['b'], R['c'], R['universo']
    w('F2. Último dígito, porcentagens redondas e boletins repetidos, bweb completo dos dois turnos de 2026 (Adendo 20)')
    w('Script: scripts/analisar_F2.py. Números completos: resultados/F2_digitos.json.')
    w(f"Simulações: {R['nsim']} por turno, semente {R['semente']} (numpy SeedSequence.spawn(3), PCG64).")
    w('')
    w('Critério registrado (PRE-REGISTRO-2026-10-26.md, Adendo 20, commit d976d4d, 30/10/2026 12:11:50 UTC, antes de rodar):')
    w('- Todas as seções do Brasil; exterior fora.')
    for k in 'abc':
        w(f'- ({k}) ' + R['criterio'][k])
    w('')
    w(f"VEREDITO PELA LETRA: (a) {a['veredito']}; (b) {b['veredito']}; (c) {c['veredito']}. F2 como um todo (D9): {R['veredito_F2']}.")
    w('')
    w('Resumo')
    for cnd in ('L', 'R'):
        x2, x1 = a[f'{cnd}_2T'], a[f'{cnd}_1T']
        w(f"- (a) {NOME[cnd]}: qui-quadrado do último dígito no 2º turno {ff(x2['qui2'])} ({fi(x2['n_contagens'])} contagens >= 50); "
          f"simulações: média {ff(x2['sim']['media'])}, p95 {ff(x2['sim']['p95'])}, p99 {ff(x2['sim']['p99'])}, p99,9 {ff(x2['sim']['p999'])}; "
          f"{x2['sims_maior_ou_igual']} de 200 simulações com valor igual ou maior. 1º turno: {ff(x1['qui2'])} "
          f"(p99 das simulações {ff(x1['sim']['p99'])}; {x1['sims_maior_ou_igual']} de 200 iguais ou maiores).")
    for med in ('L', 'C'):
        x2, x1 = b[f'{med}_2T'], b[f'{med}_1T']
        w(f"- (b) {NOME[med]}: {fi(x2['obs'])} seções a 0,1 ponto ou menos de um múltiplo de 5 no 2º turno ({ff(100*x2['frac_obs'])}%), "
          f"simulação {ff(x2['sim_media'],1)} (dp {ff(x2['sim_dp'],1)}), excesso padronizado z = {ff(x2['z'])}; "
          f"1º turno: {fi(x1['obs'])} contra {ff(x1['sim_media'],1)} (dp {ff(x1['sim_dp'],1)}), z = {ff(x1['z'])}.")
    z = c['zona_2T']
    w(f"- (c) Pares de boletins idênticos (13, 22, branco, nulo) na mesma zona, comparecimento >= 100, 2º turno: {fi(z['obs'])} observados "
      f"contra {ff(z['esperado_sim'])} esperados pela simulação (dp {ff(z['sim_dp'])}; esperado exato do mesmo modelo {ff(z['esperado_exato_mesmo_modelo'])}); "
      f"razão {ff(z['razao_obs_esperado'])}. Limiar de sinal: 3 vezes e 20 pares; de sem sinal: 1,5 vez.")
    w('')
    w('1. Decisões onde o registro não fixa (escritas no docstring antes de calcular; declaradas como desvio)')
    for x in R['decisoes_declaradas_como_desvio']:
        w('  ' + x)
    w('')
    w('2. Universo')
    w(f"  Boletins no arquivo: 1º turno {fi(u['boletins_1T'])}, 2º turno {fi(u['boletins_2T'])}; exterior (ZZ) fora: {fi(u['exterior_1T'])} e {fi(u['exterior_2T'])}.")
    w(f"  Seções do Brasil com boletim nos dois turnos: {fi(u['secoes_nos_dois_turnos_sem_exterior'])}, em {fi(u['zonas'])} zonas, "
      f"{fi(u['municipios'])} municípios e {fi(u['locais'])} locais. Seções do 2º turno com nominais além de 13 e 22: {u['secoes_2T_com_outros_nominais_diferente_de_zero']}.")
    w('')
    w('3. (a) Último dígito')
    w('  Candidato e turno | contagens >= 50 | qui-quadrado | média sim | p95 | p99 | p99,9 | sims >= obs | p teórico (9 gl)')
    for t in '21':
        for cnd in ('L', 'R'):
            x = a[f'{cnd}_{t}T']
            w(f"  {NOME[cnd]} {t}º turno | {fi(x['n_contagens'])} | {ff(x['qui2'])} | {ff(x['sim']['media'])} | {ff(x['sim']['p95'])} | "
              f"{ff(x['sim']['p99'])} | {ff(x['sim']['p999'])} | {x['sims_maior_ou_igual']} | {fp(x['p_teorico_qui2_9gl'])}")
    w('  Nota: o valor-p teórico supõe último dígito uniforme. Contagens de uma eleição limpa não têm dígito uniforme: a')
    w('  densidade das contagens cai dentro de cada dezena (há mais seções com 150 do que com 159 votos), e com 450 a 480 mil')
    w('  contagens essa inclinação basta para um qui-quadrado alto. Por isso a régua do registro é a simulação, não o 9 gl.')
    w('  Condições do registro:')
    for cnd in ('L', 'R'):
        cc = a['condicoes'][cnd]
        w(f"    {NOME[cnd]}: 2º turno acima do p99,9: {'sim' if cc['2T_acima_p999'] else 'não'}; 1º turno abaixo do p99: "
          f"{'sim' if cc['1T_abaixo_p99'] else 'não'}; 2º turno abaixo do p95: {'sim' if cc['2T_abaixo_p95'] else 'não'}.")
    w('  Frequência de cada dígito (% observado; z contra a simulação):')
    for t in '21':
        for cnd in ('L', 'R'):
            x = a[f'{cnd}_{t}T']
            cel = ', '.join(f"{dg}: {ff(100*x['digitos_frac_obs'][dg],2)} ({ff(x['digitos_z'][dg],1)})" for dg in range(10))
            w(f"    {NOME[cnd]} {t}º: {cel}")
    w('')
    w('  Concentração por unidade (fora do critério, D10). Soma dos qui-quadrados das unidades, número de unidades acima do valor')
    w(f'  crítico de 0,1% ({ff(Q2_CRIT)}) e maior qui-quadrado, cada um com o número de simulações (de 200) com valor igual ou maior:')
    for lv, rot in (('zona', 'Zonas'), ('mun', 'Municípios')):
        for t in '21':
            for cnd in ('L', 'R'):
                e = a['concentracao'][lv][f'{cnd}_{t}T']
                w(f"    {rot}, {NOME[cnd]}, {t}º turno ({fi(e['unidades'])} unidades com 100 contagens ou mais): soma {ff(e['soma_qui2_obs'],0)} "
                  f"(sim {ff(e['soma_qui2_sim']['media'],0)}, dp {ff(e['soma_qui2_sim']['dp'],0)}; {e['soma_sims_maior_ou_igual']} sims >=); "
                  f"acima do crítico {e['n_acima_critico_0_1pct_obs']} (sim {ff(e['n_acima_critico_sim']['media'],1)}, máx {ff(e['n_acima_critico_sim']['max'],0)}; "
                  f"{e['n_acima_sims_maior_ou_igual']} sims >=); máximo {ff(e['max_qui2_obs'],1)} (sim média do máximo "
                  f"{ff(e['max_qui2_sim']['media'],1)}, p95 {ff(e['max_qui2_sim']['p95'],1)}; {e['max_sims_maior_ou_igual']} sims >=)")
    for lv, rot in (('zona', 'zonas'), ('mun', 'municípios')):
        for cnd in ('L', 'R'):
            e = a['concentracao'][lv][f'{cnd}_2T']
            w(f'  As {NTOP} {rot} com maior qui-quadrado do último dígito de {NOME[cnd]} no 2º turno (n = contagens >= 50; '
              'p teórico; p empírico pelas 200 simulações; mesmo candidato no 1º turno; outro candidato no 2º):')
            for x in e['unidades_lista'][:NTOP]:
                nm = f" {x['nome']}" if x.get('nome') else ''
                dg = x['digitos']; dmax = int(np.argmax(dg))
                w(f"    {x['unidade']}{nm}: n {x['n']}, qui2 {ff(x['qui2'],1)}, p {fp(x['p_teorico'])}, p emp {ff(x['p_empirico'],3)}; "
                  f"dígito mais comum {dmax} ({dg[dmax]} de {x['n']}); 1º turno qui2 {ff(x['qui2_mesmo_candidato_1T'],1)} "
                  f"(n {x['n_1T']}, p {fp(x['p_teorico_1T'])}); {NOME['R' if cnd=='L' else 'L']} no 2º qui2 {ff(x['qui2_outro_candidato_2T'],1)}; "
                  f"Lula {ff(100*x['fatia_Lula_2T'],1)}% no 2º")
    w('')
    w('  Por UF (qui-quadrado do último dígito; p empírico pelas 200 simulações):')
    ufs = [x['unidade'] for x in a['concentracao']['uf']['L_2T']['unidades_lista']]
    idx = {t + c_: {x['unidade']: x for x in a['concentracao']['uf'][f'{c_}_{t}T']['unidades_lista']} for t in '12' for c_ in 'LR'}
    for uf in ufs:
        cel = []
        for t in '21':
            for c_ in 'LR':
                x = idx[t + c_].get(uf)
                cel.append(f"{NOME[c_]} {t}º {ff(x['qui2'],1)} (p emp {ff(x['p_empirico'],3)})" if x else f'{NOME[c_]} {t}º n/d')
        w(f"    {uf} (n {fi(idx['2L'][uf]['n'])}): " + '; '.join(cel))
    w('  Por faixa da fatia de Lula no local (2º turno; p empírico):')
    for t in '21':
        for c_ in 'LR':
            lst = a['concentracao']['faixa'][f'{c_}_{t}T']['unidades_lista']
            w(f"    {NOME[c_]} {t}º: " + '; '.join(f"{x['unidade']} n {fi(x['n'])} qui2 {ff(x['qui2'],1)} (p emp {ff(x['p_empirico'],3)})" for x in lst))
    w('')
    w('4. (b) Porcentagens redondas (a 0,1 ponto ou menos de um múltiplo de 5)')
    for med in ('L', 'C'):
        for t in '21':
            x = b[f'{med}_{t}T']
            w(f"  {NOME[med]} {t}º turno: {fi(x['obs'])} de {fi(x['secoes'])} ({ff(100*x['frac_obs'],3)}%); simulação {ff(x['sim_media'],1)} "
              f"({ff(100*x['frac_sim_media'],3)}%), dp {ff(x['sim_dp'],1)}; z = {ff(x['z'])}. Sem os exatos 0% e 100%: {fi(x['sem_0_e_100']['obs'])} "
              f"contra {ff(x['sem_0_e_100']['sim_media'],1)} (z {ff(x['sem_0_e_100']['z'])}).")
    for t in '21':
        x = b[f'LouC_{t}T']
        w(f"  Lula ou comparecimento (união, descritivo) {t}º turno: {fi(x['obs'])} contra {ff(x['sim_media'],1)} (z {ff(x['z'])}).")
    w('  Condições do registro:')
    for med in ('L', 'C'):
        cc = b['condicoes'][med]
        w(f"    {NOME[med]}: z2 = {ff(cc['z2'])}, z1 = {ff(cc['z1'])}; z2 > 4: {'sim' if cc['z2_acima_4'] else 'não'}; z2 >= 2 z1: "
          f"{'sim' if cc['z2_pelo_menos_2z1'] else 'não'}; |z2| <= 2: {'sim' if cc['abs_z2_ate_2'] else 'não'}.")
    w('  Por múltiplo (observado, média simulada, z), onde |z| >= 2 em algum turno:')
    for med in ('L', 'C'):
        for m in range(21):
            x2, x1 = b[f'{med}_2T']['por_multiplo'][m], b[f'{med}_1T']['por_multiplo'][m]
            zs = [abs(x2['z'] or 0), abs(x1['z'] or 0)]
            if max(zs) >= 2:
                w(f"    {NOME[med]} {5*m}%: 2º turno {fi(x2['obs'])} contra {ff(x2['sim_media'],1)} (z {ff(x2['z'],1) if x2['z'] is not None else 'n/d'}); "
                  f"1º turno {fi(x1['obs'])} contra {ff(x1['sim_media'],1)} (z {ff(x1['z'],1) if x1['z'] is not None else 'n/d'})")
    w('')
    w('5. (c) Boletins repetidos')
    w(f"  Mesma zona, 2º turno: {fi(z['obs'])} pares observados; esperado pela simulação {ff(z['esperado_sim'])} (dp {ff(z['sim_dp'])}, "
      f"mín {ff(z['sim']['min'],0)}, máx {ff(z['sim']['max'],0)}); esperado exato do mesmo modelo {ff(z['esperado_exato_mesmo_modelo'])} "
      f"em {fi(z['pares_candidatos_mesmo_V_e_BN'])} pares com mesmos válidos e mesmo branco mais nulo; {z['sims_maior_ou_igual']} de 200 "
      f"simulações com tantos pares ou mais; P(Poisson >= obs) = {fp(z['p_poisson_obs_ou_mais'])}.")
    s_ = c['sensibilidade_multinomial_pelo_comparecimento']
    w(f"  Sensibilidade (D11, as quatro contagens sorteadas juntas pelo comparecimento): esperado {ff(s_['esperado_sim'])} (dp {ff(s_['sim_dp'])}); "
      f"razão {ff(s_['razao_obs_esperado'])}.")
    for k_, rot in (('local_2T', 'Mesmo local, 2º turno'), ('pais_2T', 'País inteiro, 2º turno'), ('zona_1T', 'Mesma zona, 1º turno (13, 22, outros, branco, nulo)'),
                    ('local_1T', 'Mesmo local, 1º turno'), ('pais_1T', 'País inteiro, 1º turno')):
        x = c[k_]
        w(f"  {rot}: {fi(x['obs'])} contra {ff(x['esperado_sim'])} (dp {ff(x['sim_dp'])}); razão {ff(x['razao'])}; {x['sims_maior_ou_igual']} sims >=.")
    rs = c['resumo_pares_observados']
    w(f"  Grupos observados na mesma zona no 2º turno: {rs['grupos']}; no mesmo local {rs['no_mesmo_local']}; iguais também no 1º turno "
      f"{rs['iguais_tambem_no_1T']}; com o mesmo número de urna {rs['com_mesma_urna']}; com seção agregada {rs['com_secao_agregada']}.")
    w('  Os 25 pares menos prováveis no modelo (seção: local, urna, aptos, comparecimento, 2º turno 13/22/B/N, 1º turno 13/22/outros/B/N):')
    for g in c['pares_observados'][:25]:
        w(f"    prob {fp(g['prob_par_no_modelo'])}; mesmo local {'sim' if g['mesmo_local'] else 'não'}; igual no 1º {'sim' if g['tambem_igual_no_1T'] else 'não'}")
        for s in g['secoes']:
            nm = (s['municipio'] + ', ' if s['municipio'] else '') + (s['nome_local'] or '')
            w(f"      {s['secao']} ({nm}; local {s['local'].split('|')[-1]}; urna {s['urna_2T']}): aptos {s['apt']}, comp {s['comp_2T']}, "
              f"2º {s['L2']}/{s['R2']}/{s['B2']}/{s['N2']}, 1º {s['L1']}/{s['R1']}/{s['O1']}/{s['B1']}/{s['N1']}{', agregada' if s['agregada'] else ''}")
    w('')
    w('6. Descritivos fora do critério (D11)')
    dsc = R['descritivos']
    for t in '21':
        for c_ in ('L', 'R', 'C'):
            x = dsc[f'dois_digitos_{c_}_{t}T']
            w(f"  Dois últimos dígitos, {NOME[c_]} {t}º (contagens >= 100): qui2 {ff(x['qui2'],1)} (sim média {ff(x['sim']['media'],1)}, p99 {ff(x['sim']['p99'],1)}; "
              f"{x['sims_maior_ou_igual']} sims >=; p teórico 99 gl {fp(x['p_teorico'])})")
        x = dsc[f'ultimo_digito_C_{t}T']
        w(f"  Último dígito do comparecimento {t}º (>= 50, n {fi(x['n'])}): qui2 {ff(x['qui2'],1)} (sim média {ff(x['sim']['media'],1)}, p99 {ff(x['sim']['p99'],1)}; "
          f"{x['sims_maior_ou_igual']} sims >=; p teórico {fp(x['p_teorico'])})")
    w('')
    ph = R['post_hoc']
    w('7. Post hoc (D12 a D15, escritos depois de ver o veredito; descritivos, sem veredito)')
    mn = ph['margem_nacional_2T_sem_exterior']
    w(f"  Escala: no Brasil sem o exterior, 2º turno, Lula {fi(mn['L'])}, Flávio {fi(mn['R'])}, margem {fi(mn['margem_L_menos_R'])}.")
    w('  D12. Zonas com p teórico abaixo de 0,001 no último dígito do 2º turno (seções cujo voto termina no dígito mais comum):')
    for z_ in ph['D12_zonas_p_teorico_abaixo_0_001']:
        w(f"    {z_['zona']} ({', '.join(z_['municipios_da_zona'])}), {z_['candidato']}: qui2 {ff(z_['qui2'],1)}, p {fp(z_['p_teorico'])}, p emp {ff(z_['p_empirico'],3)}; "
          f"dígito {z_['digito_mais_comum']} em {z_['secoes_com_esse_digito']} de {z_['n']} (uniforme daria {ff(z_['esperado_uniforme'],1)}), "
          f"em {z_['locais_dessas_secoes']} dos {z_['locais_da_zona']} locais da zona; margem da zona {fi(z_['margem_zona_L_menos_R'])} "
          f"(Lula {fi(z_['votos_L_zona_2T'])}, Flávio {fi(z_['votos_R_zona_2T'])}).")
        vals = sorted(s_['L2' if z_['candidato'] == 'Lula' else 'R2'] for s_ in z_['secoes'])
        w(f"      valores: {', '.join(str(v) for v in vals)}")
    w('  D13. Pares idênticos no país inteiro, por parte (mesmos válidos e branco mais nulo em todos):')
    d13 = ph['D13_decomposicao_pares_pais']
    for t in '21':
        for k_, rot in (('pares_pais_VBN_L', 'mesmo 13'), ('pares_pais_VBN_B', 'mesmo branco'), ('pares_pais', 'boletim inteiro')):
            x = d13[f'{k_}_{t}T']
            w(f"    {t}º turno, {rot}: {fi(x['obs'])} contra {ff(x['sim_media'],1)} (dp {ff(x['sim_dp'],1)}); razão {ff(x['razao'],4)}; z {ff(x['z'],1)}")
    w('  D14. Seções do 2º turno com comparecimento de 100% dos aptos:')
    for s_ in ph['D14_comparecimento_100pct_2T']:
        w(f"    {s_['secao']} ({s_['municipio']}, {s_['nome_local']}): aptos {s_['apt']}; 2º {s_['L2']}/{s_['R2']}/{s_['B2']}/{s_['N2']}; "
          f"1º aptos {s_['apt_1T']}, comparecimento {s_['comp_1T']}, 13/22/outros {s_['L1']}/{s_['R1']}/{s_['O1']}")
    w('  D15. Poder aproximado de (a) no país (ordem de grandeza, supondo base uniforme): seções com último dígito inventado')
    w('  precisas para o qui-quadrado do 2º turno passar do p99,9 das simulações:')
    for cnd in ('L', 'R'):
        x = ph['D15_poder_aproximado'][cnd]
        w(f"    {NOME[cnd]}: distância até o p99,9 {ff(x['distancia_ate_p999'],1)}; todas num só dígito: cerca de {fi(round(x['secoes_todas_num_digito']))} seções; "
          f"metade em 0 e metade em 5: cerca de {fi(round(x['secoes_metade_0_metade_5']))} seções. Dígito inventado ao acaso (uniforme): nenhuma quantidade é detectada.")
    w('')
    return '\n'.join(o) + '\n'


if __name__ == '__main__':
    main()
