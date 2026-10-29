"""T23 do pré-registro (Adendo 9): componente de zona e degrau na fronteira de zona, com o bweb completo do 2º turno.

Registro (PRE-REGISTRO-2026-10-26.md, Adendo 9, T23):
  "Resíduo r da variação da fatia de Lula por seção, de um modelo dentro da UF com a composição completa do 1º turno e a
  variação do comparecimento. (a) Decompor a variância de r em município, zona dentro do município, local dentro da zona e
  seção, descontando a variância binomial. (b) Nos municípios com 2 zonas ou mais, pares de locais a até 1 km em zonas
  diferentes contra pares à mesma distância na mesma zona (coordenadas do cadastro de locais do TSE).
  Sinal: componente de zona de pelo menos 2 vezes o maior de 2018 e 2022, degrau médio na fronteira de 1 ponto ou mais e mais
  de 200 mil votos somados nas zonas extremas.
  Sem sinal: componente até 1,3 vez o das referências e degrau abaixo de 0,3 ponto."

Leitura escolhida (cada ponto ambíguo sai no resultado como escolha declarada):
- y = variação da fatia de Lula entre os dois finalistas, 2º menos 1º turno, em pontos: 100*(L2/(L2+R2) - L1/(L1+R1)).
  2018: Haddad (13) contra Bolsonaro; 2022: Lula contra Bolsonaro; 2026: Lula contra Flávio.
- Modelo dentro da UF: MQO sem peso, uma regressão por UF (constante e coeficientes próprios de cada UF), y contra as fatias do
  comparecimento do 1º turno de cada candidato (branco+nulo, com o 28 anulado contado como nulo, é a categoria omitida) e a
  variação do comparecimento, 100*(C2-C1)/aptos do 2º turno. 2026: Lula, Flávio, Cury, Renan, Caiado, Zema e demais
  (composição completa, principal). 2018 e 2022: as bases só têm L, R e "outros" por seção, então a composição é L, R e outros;
  2026 com a mesma composição agregada sai ao lado, para a comparação com as referências na mesma especificação.
- Amostra: seções das 27 UFs (exterior fora: não há UF nem coordenada), com os dois turnos, votos nos dois finalistas nos dois
  turnos, comparecimento e aptos positivos.
- (a) Componentes de variância de r num modelo aninhado (município dentro da UF, zona dentro do município, local dentro da zona,
  seção), pelo método dos momentos de Henderson (ANOVA aninhada desbalanceada, cada seção com peso 1), juntando as somas de
  quadrados das 27 UFs (a média de cada UF é fixa). A variância binomial conhecida de cada seção, v = 10^4 p2(1-p2)/(L2+R2) com
  p2 = L2/(L2+R2), entra exatamente nas esperanças de cada soma de quadrados e é descontada; o componente de seção que sobra é a
  variação verdadeira entre seções. Variantes: sem desconto e com o desconto dos dois turnos somados (descritivas).
  "Componente de zona" = sigma2 de zona dentro do município (pontos ao quadrado). Erro-padrão: bootstrap de municípios
  estratificado por UF, 2.000 reamostras.
- (b) Locais com coordenadas do cadastro de locais de 2026 (2º turno), r do local = média de r das suas seções. Em cada
  município com 2 zonas ou mais na base do ano, todos os pares de locais a até 1 km; pares em zonas diferentes contra pares na
  mesma zona, em faixas de 100 m (os pares da mesma zona são reponderados para a distribuição de distâncias dos pares em zonas
  diferentes). Por par, q = (r_a - r_b)^2 menos o ruído esperado das duas médias (componente de seção mais binomial, dividido
  pelo número de seções). Degrau^2 = média de q nos pares em zonas diferentes menos a dos pares na mesma zona à mesma distância;
  "degrau médio" = raiz desse valor (média quadrática do salto entre zonas vizinhas, em pontos). Erro-padrão: bootstrap de
  municípios. Em 2018 e 2022 o degrau é descritivo, com as coordenadas de 2026 ligadas pela chave UF|município|zona|seção.
- "Zonas extremas": nos municípios com 2 zonas ou mais, efeito da zona = desvio da média de r da zona em relação à média do
  município, encolhido pelo previsor linear (BLUP) com os componentes estimados; extrema = efeito acima de 2 desvios-padrão do
  componente de zona em valor absoluto. "Votos somados" = soma, nas zonas extremas a favor de Lula, do efeito (pontos/100)
  vezes os votos nos dois finalistas no 2º turno (votos de Lula deslocados pelo componente de zona); ao lado, o mesmo nas
  zonas extremas contra Lula e os votos totais dessas zonas.
- "O das referências" no critério de sem sinal = o maior das duas, como no critério de sinal.

As referências (2018 e 2022) são calculadas e gravadas antes de a base de 2026 ser lida.
Uso: python3 -I analisar_T23.py <secoes2026.json.gz> <candidatos2026_1t.json.gz> <secoes2018.json.gz> <secoes2022.json.gz>
        <pasta locais_votacao 2026> <saida.json> <saida.txt> <arquivo de referências (gravado antes de 2026)> [--reps 2000]
"""
import os as _os, sys as _sys
_sys.path.insert(0, _os.path.dirname(_os.path.abspath(__file__)))
import csv, gc, json, sys, time, warnings
import numpy as np
from scipy.spatial import cKDTree
from lib import carregar
warnings.filterwarnings('ignore')

UFS = ['AC', 'AL', 'AM', 'AP', 'BA', 'CE', 'DF', 'ES', 'GO', 'MA', 'MG', 'MS', 'MT', 'PA', 'PB', 'PE', 'PI', 'PR', 'RJ',
       'RN', 'RO', 'RR', 'RS', 'SC', 'SE', 'SP', 'TO']
GRUPOS_2026 = [('Cury', '70'), ('Renan', '14'), ('Caiado', '55'), ('Zema', '30')]
SEMENTE = 20261029
R_TERRA = 6371008.8
FAIXA_M, DIST_MAX = 100.0, 1000.0
NFAIXAS = int(DIST_MAX / FAIXA_M)
LIM_SINAL_RAZAO, LIM_SINAL_DEGRAU, LIM_SINAL_VOTOS = 2.0, 1.0, 200000
LIM_SEM_RAZAO, LIM_SEM_DEGRAU = 1.3, 0.3


def log(*a):
    print(time.strftime('%H:%M:%S'), *a, flush=True)


# ----------------------------------------------------------------------------------------------------------- dados
def ler_locais(pasta):
    """Chave da seção (UF|mun|zona|seção) -> (lat, lon) do cadastro de locais de 2026, linhas do 2º turno."""
    sec, nome = {}, {}
    for uf in UFS:
        with open(_os.path.join(pasta, f'eleitorado_local_votacao_2026_{uf}.csv'), encoding='latin1', newline='') as f:
            r = csv.reader(f, delimiter=';'); h = next(r); ix = {c: i for i, c in enumerate(h)}
            for row in r:
                if row[ix['NR_TURNO']] != '2':
                    continue
                mun, z, s = int(row[ix['CD_MUNICIPIO']]), int(row[ix['NR_ZONA']]), int(row[ix['NR_SECAO']])
                nome[f'{uf}|{mun}'] = row[ix['NM_MUNICIPIO']]
                try:
                    lat = float(row[ix['NR_LATITUDE']].replace(',', '.')); lon = float(row[ix['NR_LONGITUDE']].replace(',', '.'))
                except ValueError:
                    continue
                if lat in (-1.0, 0.0) or lon in (-1.0, 0.0):
                    continue
                sec[f'{uf}|{mun}|{z}|{s}'] = (lat, lon)
    return sec, nome


def montar(caminho, cand_caminho=None):
    """Arrays por seção. Com cand_caminho (2026), também a composição completa do 1º turno."""
    d = carregar(caminho)
    cand = carregar(cand_caminho)['secoes'] if cand_caminho else None
    K, Y, XA, XG, V1, V2, N2, COMP1, COMP2 = [], [], [], [], [], [], [], [], []
    fora = {'exterior': 0, 'sem_dois_turnos': 0, 'sem_voto_finalista_ou_comparecimento': 0}
    for k, v in d.items():
        if k.startswith('ZZ'):
            fora['exterior'] += 1; continue
        if '1' not in v or '2' not in v:
            fora['sem_dois_turnos'] += 1; continue
        a, b = v['1'], v['2']
        c28 = a.get('c28', 0)
        L1, R1, C1 = a['L'], a['R'], a['comp']; O1 = a['O'] - c28
        L2, R2, C2 = b['L'], b['R'], b['comp']; apt = b.get('apt') or a.get('apt') or 0
        n1, n2 = L1 + R1, L2 + R2
        if n1 <= 0 or n2 <= 0 or C1 <= 0 or C2 <= 0 or apt <= 0:
            fora['sem_voto_finalista_ou_comparecimento'] += 1; continue
        p1, p2 = L1 / n1, L2 / n2
        dc = 100.0 * (C2 - C1) / apt
        K.append(f"{k}|{b['loc']}")
        Y.append(100.0 * (p2 - p1))
        XA.append([100.0 * L1 / C1, 100.0 * R1 / C1, 100.0 * O1 / C1, dc])
        if cand is not None:
            cv = cand.get(k, {})
            gs = [cv.get(num, 0) for _, num in GRUPOS_2026]
            dem = O1 - sum(gs)
            if dem < 0:
                raise SystemExit(f'demais negativo em {k}')
            XG.append([100.0 * L1 / C1, 100.0 * R1 / C1] + [100.0 * g / C1 for g in gs] + [100.0 * dem / C1, dc])
        V1.append(1e4 * p1 * (1 - p1) / n1); V2.append(1e4 * p2 * (1 - p2) / n2)
        N2.append(n2); COMP1.append(C1); COMP2.append(C2)
    del d, cand; gc.collect()
    base = {'chave': K, 'y': np.array(Y), 'XA': np.array(XA), 'XG': np.array(XG) if XG else None,
            'v1': np.array(V1), 'v2': np.array(V2), 'n2': np.array(N2, float),
            'comp1': np.array(COMP1, float), 'comp2': np.array(COMP2, float), 'fora': fora}
    # códigos aninhados
    partes = [c.split('|') for c in K]
    uf = np.array([p[0] for p in partes])
    kmun = np.array([f'{p[0]}|{p[1]}' for p in partes])
    kzon = np.array([f'{p[0]}|{p[1]}|{p[2]}' for p in partes])
    kloc = np.array([f'{p[0]}|{p[1]}|{p[2]}|{p[4]}' for p in partes])
    base['sec'] = [f'{p[0]}|{p[1]}|{p[2]}|{p[3]}' for p in partes]
    base['uf'] = uf
    base['nomes_uf'], base['gu'] = np.unique(uf, return_inverse=True)
    base['nomes_mun'], base['gm'] = np.unique(kmun, return_inverse=True)
    base['nomes_zon'], base['gz'] = np.unique(kzon, return_inverse=True)
    base['nomes_loc'], base['gl'] = np.unique(kloc, return_inverse=True)
    del K, partes; gc.collect()
    return base


def residuos(y, X, uf):
    """Uma regressão MQO por UF, com constante. Devolve r e um resumo por UF."""
    r = np.empty_like(y); res = {}
    for u in np.unique(uf):
        m = uf == u
        A = np.column_stack([np.ones(m.sum()), X[m]])
        b, *_ = np.linalg.lstsq(A, y[m], rcond=None)
        e = y[m] - A @ b
        r[m] = e
        res[str(u)] = {'secoes': int(m.sum()), 'r2': float(1 - e.var() / y[m].var()), 'coef': [float(x) for x in b]}
    return r, res


# ------------------------------------------------------------------------------------- (a) componentes de variância
def estat_mun(r, v, B):
    """Estatísticas suficientes por município para a ANOVA aninhada (UF > município > zona > local > seção)."""
    gl, gz, gm, gu = B['gl'], B['gz'], B['gm'], B['gu']
    NLc, NZc, NMc = gl.max() + 1, gz.max() + 1, gm.max() + 1
    l2z = np.zeros(NLc, int); l2z[gl] = gz
    z2m = np.zeros(NZc, int); z2m[gz] = gm
    m2u = np.zeros(NMc, int); m2u[gm] = gu
    l2m = z2m[l2z]
    nl = np.bincount(gl, minlength=NLc).astype(float); Sl = np.bincount(gl, r, NLc); Vl = np.bincount(gl, v, NLc)
    nz = np.bincount(gz, minlength=NZc).astype(float); Sz = np.bincount(gz, r, NZc); Vz = np.bincount(gz, v, NZc)
    Az = np.bincount(l2z, nl ** 2, NZc)
    E = {'N': np.bincount(gm, minlength=NMc).astype(float),
         'NL': np.bincount(l2m, minlength=NMc).astype(float),
         'NZ': np.bincount(z2m, minlength=NMc).astype(float),
         'R2': np.bincount(gm, r * r, NMc),
         'SL': np.bincount(l2m, Sl ** 2 / nl, NMc),
         'SZ': np.bincount(z2m, Sz ** 2 / nz, NMc),
         'S': np.bincount(gm, r, NMc),
         'V': np.bincount(gm, v, NMc),
         'VL': np.bincount(l2m, Vl / nl, NMc),
         'VZ': np.bincount(z2m, Vz / nz, NMc),
         'AZ': np.bincount(z2m, Az / nz, NMc),
         'A': np.bincount(l2m, nl ** 2, NMc),
         'B': np.bincount(z2m, nz ** 2, NMc),
         'm2u': m2u}
    zon = {'n': nz, 'S': Sz, 'V': Vz, 'A': Az, 'z2m': z2m, 'n2': np.bincount(gz, B['n2'], NZc)}
    loc = {'n': nl, 'S': Sl, 'V': Vl, 'l2z': l2z, 'l2m': l2m}
    return E, zon, loc


def estimar(E, c):
    """Henderson I com as somas de quadrados juntadas das UFs. c: multiplicidade de cada município, (R, M)."""
    c = np.atleast_2d(np.asarray(c, float))
    U = E['m2u'].max() + 1
    Iu = np.zeros((len(E['N']), U)); Iu[np.arange(len(E['N'])), E['m2u']] = 1.0
    N = c @ E['N']; NL = c @ E['NL']; NZ = c @ E['NZ']; NM = c.sum(1)
    Nu = (c * E['N']) @ Iu
    pres = Nu > 0
    NU = pres.sum(1)

    def uf_quoc(x):
        num = (c * x) @ Iu
        return np.where(pres, num / np.where(pres, Nu, 1), 0.0)

    Su = (c * E['S']) @ Iu
    SSE = c @ (E['R2'] - E['SL'])
    SSL = c @ (E['SL'] - E['SZ'])
    SSZ = c @ (E['SZ'] - E['S'] ** 2 / E['N'])
    SSM = c @ (E['S'] ** 2 / E['N']) - np.where(pres, Su ** 2 / np.where(pres, Nu, 1), 0).sum(1)
    KE = c @ (E['V'] - E['VL']); KL = c @ (E['VL'] - E['VZ']); KZ = c @ (E['VZ'] - E['V'] / E['N'])
    KM = c @ (E['V'] / E['N']) - uf_quoc(E['V']).sum(1)
    cLL = c @ (E['N'] - E['AZ']); cLZ = c @ (E['AZ'] - E['A'] / E['N']); cLM = c @ (E['A'] / E['N']) - uf_quoc(E['A']).sum(1)
    cZZ = c @ (E['N'] - E['B'] / E['N']); cZM = c @ (E['B'] / E['N']) - uf_quoc(E['B']).sum(1)
    cMM = N - uf_quoc(E['N'] ** 2).sum(1)
    sS = (SSE - KE) / (N - NL)
    sL = (SSL - KL - (NL - NZ) * sS) / cLL
    sZ = (SSZ - KZ - (NZ - NM) * sS - cLZ * sL) / cZZ
    sM = (SSM - KM - (NM - NU) * sS - cLM * sL - cZM * sZ) / cMM
    return {'municipio': sM, 'zona': sZ, 'local': sL, 'secao': sS, 'binomial_media': (c @ E['V']) / N,
            'total_r': (SSE + SSL + SSZ + SSM) / N}


def contagens_boot(m2u, reps, rng):
    """Multiplicidades do bootstrap de municípios estratificado por UF."""
    M = len(m2u); C = np.zeros((reps, M))
    for u in np.unique(m2u):
        idx = np.where(m2u == u)[0]
        C[:, idx] = rng.multinomial(len(idx), np.full(len(idx), 1.0 / len(idx)), size=reps)
    return C


def decompor(r, v, B, C):
    E, zon, loc = estat_mun(r, v, B)
    p = {k: float(x[0]) for k, x in estimar(E, np.ones(len(E['N']))).items()}
    bt = estimar(E, C)
    ep = {k: float(np.std(x, ddof=1)) for k, x in bt.items()}
    soma = p['municipio'] + p['zona'] + p['local'] + p['secao']
    out = {'sigma2': p, 'ep': ep, 'boot_zona': bt['zona'],
           'fracao_da_variancia_de_r': {k: p[k] / p['total_r'] for k in ('municipio', 'zona', 'local', 'secao', 'binomial_media')},
           'soma_dos_quatro_componentes': soma,
           'dp_pontos': {k: float(np.sign(p[k]) * np.sqrt(abs(p[k]))) for k in ('municipio', 'zona', 'local', 'secao')},
           'municipios': int(len(E['N'])), 'municipios_2_zonas_ou_mais': int((E['NZ'] >= 2).sum()),
           'zonas_municipio': int(E['NZ'].sum()), 'zonas_em_municipios_2_ou_mais': int(E['NZ'][E['NZ'] >= 2].sum()),
           'locais': int(E['NL'].sum()), 'secoes': int(E['N'].sum()),
           'secoes_em_municipios_2_zonas_ou_mais': int(E['N'][E['NZ'] >= 2].sum())}
    return out, E, zon, loc


def por_uf(E, nomes_uf):
    out = {}
    for u, nome in enumerate(nomes_uf):
        c = (E['m2u'] == u).astype(float)
        e = estimar(E, c)
        out[str(nome)] = {k: float(e[k][0]) for k in ('municipio', 'zona', 'local', 'secao')}
        out[str(nome)]['municipios_2_zonas_ou_mais'] = int(((E['m2u'] == u) & (E['NZ'] >= 2)).sum())
    return out


# ------------------------------------------------------------------------------------------------ zonas extremas
def zonas_extremas(comp, E, zon, loc, nomes_zon):
    sZ, sL, sS = comp['zona'], comp['local'], max(comp['secao'], 0.0)
    multi = E['NZ'][zon['z2m']] >= 2
    media_m = E['S'] / E['N']
    d = zon['S'] / zon['n'] - media_m[zon['z2m']]
    tau2 = max(sL, 0.0) * zon['A'] / zon['n'] ** 2 + (sS * zon['n'] + zon['V']) / zon['n'] ** 2
    if sZ <= 0:
        lam = np.zeros_like(d)
    else:
        lam = sZ / (sZ + tau2)
    ef = np.where(multi, lam * d, 0.0)
    lim = 2 * np.sqrt(sZ) if sZ > 0 else np.inf
    pos = multi & (ef > lim); neg = multi & (ef < -lim)
    ordem = np.argsort(-np.abs(ef))[:15]
    top = [{'zona': str(nomes_zon[i]), 'efeito_pontos': float(ef[i]), 'desvio_bruto_pontos': float(d[i]),
            'secoes': int(zon['n'][i]), 'votos_finalistas_2T': int(zon['n2'][i])} for i in ordem if multi[i]]
    return {'limiar_pontos': float(lim) if np.isfinite(lim) else None,
            'zonas_avaliadas': int(multi.sum()),
            'zonas_extremas_a_favor_de_lula': int(pos.sum()), 'zonas_extremas_contra_lula': int(neg.sum()),
            'votos_somados_a_favor_de_lula': float((ef[pos] / 100 * zon['n2'][pos]).sum()),
            'votos_somados_contra_lula': float((ef[neg] / 100 * zon['n2'][neg]).sum()),
            'votos_finalistas_nas_zonas_extremas_a_favor': int(zon['n2'][pos].sum()),
            'votos_finalistas_nas_zonas_extremas_contra': int(zon['n2'][neg].sum()),
            'soma_abs_efeito_vezes_votos_todas_as_zonas': float((np.abs(ef[multi]) / 100 * zon['n2'][multi]).sum()),
            'maiores_efeitos': top}


# ------------------------------------------------------------------------------------------- (b) degrau na fronteira
def geometria(B, sec2coord, E, loc):
    """Coordenada de cada local (mediana das suas seções), pares a até 1 km dentro dos municípios com 2 zonas ou mais."""
    NLc = len(loc['n'])
    lat = np.full(NLc, np.nan); lon = np.full(NLc, np.nan)
    acum = {}
    for i, s in enumerate(B['sec']):
        c = sec2coord.get(s)
        if c is not None:
            acum.setdefault(B['gl'][i], []).append(c)
    inconsist = 0; sem = 0
    for l in range(NLc):
        cs = acum.get(l)
        if not cs:
            sem += 1; continue
        a = np.array(cs); m = np.median(a, axis=0)
        dmax = np.max(np.hypot((a[:, 0] - m[0]) * 111195, (a[:, 1] - m[1]) * 111195 * np.cos(np.radians(m[0]))))
        if dmax > DIST_MAX:
            inconsist += 1; continue
        lat[l], lon[l] = m
    ok = np.isfinite(lat)
    # coordenadas repetidas por 3 ou mais locais (robustez)
    chave = np.where(ok, np.round(np.nan_to_num(lat), 6) * 1e7 + np.round(np.nan_to_num(lon), 6), np.nan)
    _, inv, cnt = np.unique(chave[ok], return_inverse=True, return_counts=True)
    repetida = np.zeros(NLc, bool); repetida[np.where(ok)[0]] = cnt[inv] >= 3
    multi_m = np.where(E['NZ'] >= 2)[0]
    PA, PB, PM, PF, PC = [], [], [], [], []
    for m in multi_m:
        ls = np.where((loc['l2m'] == m) & ok)[0]
        if len(ls) < 2:
            continue
        la0 = np.radians(np.mean(lat[ls]))
        x = np.radians(lon[ls]) * np.cos(la0) * R_TERRA; y = np.radians(lat[ls]) * R_TERRA
        P = np.column_stack([x, y])
        pr = cKDTree(P).query_pairs(DIST_MAX, output_type='ndarray')
        if len(pr) == 0:
            continue
        dist = np.hypot(*(P[pr[:, 0]] - P[pr[:, 1]]).T)
        a, b = ls[pr[:, 0]], ls[pr[:, 1]]
        PA.append(a); PB.append(b); PM.append(np.full(len(a), m))
        PF.append(np.minimum((dist / FAIXA_M).astype(int), NFAIXAS - 1))
        PC.append(loc['l2z'][a] != loc['l2z'][b])
    G = {'a': np.concatenate(PA), 'b': np.concatenate(PB), 'm': np.concatenate(PM), 'faixa': np.concatenate(PF),
         'cruza': np.concatenate(PC), 'repetida': repetida,
         'locais_sem_coordenada': int(sem), 'locais_coordenada_inconsistente': int(inconsist),
         'locais_com_coordenada': int(ok.sum()), 'locais_total': int(NLc)}
    return G


def degrau(G, loc, sS, reps, rng, excluir_repetidas=False):
    sS = max(sS, 0.0)
    rl = loc['S'] / loc['n']
    ruido = (sS * loc['n'] + loc['V']) / loc['n'] ** 2
    sel = np.ones(len(G['a']), bool)
    if excluir_repetidas:
        sel = ~(G['repetida'][G['a']] | G['repetida'][G['b']])
    a, b, m, f, x = G['a'][sel], G['b'][sel], G['m'][sel], G['faixa'][sel], G['cruza'][sel]
    dlt = rl[a] - rl[b]
    q = dlt ** 2 - ruido[a] - ruido[b]
    um, gm = np.unique(m, return_inverse=True)
    M = len(um)
    cel = gm * (2 * NFAIXAS) + x.astype(int) * NFAIXAS + f

    def tab(w):
        return np.bincount(cel, w, M * 2 * NFAIXAS).reshape(M, 2, NFAIXAS)
    T = {'n': tab(np.ones(len(q))), 'q': tab(q), 'd2': tab(dlt ** 2), 'abs': tab(np.abs(dlt))}

    def calc(cm):
        cm = np.atleast_2d(cm)
        n = np.einsum('rm,mjf->rjf', cm, T['n'])
        res = {}
        for nome in ('q', 'd2', 'abs'):
            s = np.einsum('rm,mjf->rjf', cm, T[nome])
            med = s / np.where(n > 0, n, 1)
            ok = (n[:, 0, :] > 0) & (n[:, 1, :] > 0)
            pc = np.where(ok, n[:, 1, :], 0); pc = pc / pc.sum(1, keepdims=True)
            res[nome] = (pc * np.where(ok, med[:, 1, :] - med[:, 0, :], 0)).sum(1)
        return res
    p = {k: float(v[0]) for k, v in calc(np.ones(M)).items()}
    C = rng.multinomial(M, np.full(M, 1.0 / M), size=reps).astype(float)
    bt = calc(C)
    raiz = lambda z: np.sign(z) * np.sqrt(np.abs(z))
    nc = T['n'].sum(axis=(0, 2))
    # por município (os 10 com mais pares entre zonas)
    porm = []
    ncm = T['n'][:, 1, :].sum(1)
    for i in np.argsort(-ncm)[:10]:
        e = np.zeros(M); e[i] = 1
        pi = calc(e)
        porm.append({'municipio_codigo': int(um[i]), 'pares_zonas_diferentes': int(ncm[i]),
                     'pares_mesma_zona': int(T['n'][i, 0, :].sum()), 'degrau2': float(pi['q'][0]),
                     'degrau_pontos': float(raiz(pi['q'][0]))})
    return {'pares_zonas_diferentes': int(nc[1]), 'pares_mesma_zona': int(nc[0]), 'municipios_com_pares': int(M),
            'degrau2': p['q'], 'ep_degrau2': float(np.std(bt['q'], ddof=1)),
            'degrau_pontos': float(raiz(p['q'])), 'ep_degrau_pontos': float(np.std(raiz(bt['q']), ddof=1)),
            'ic95_degrau_pontos': [float(np.percentile(raiz(bt['q']), 2.5)), float(np.percentile(raiz(bt['q']), 97.5))],
            'sem_descontar_ruido_degrau_pontos': float(raiz(p['d2'])),
            'diferenca_media_abs_pontos': p['abs'], 'ep_diferenca_media_abs': float(np.std(bt['abs'], ddof=1)),
            'distribuicao_distancia_pares_zonas_diferentes': [int(z) for z in T['n'][:, 1, :].sum(0)],
            'maiores_municipios': porm}


# ---------------------------------------------------------------------------------------------------------- ano
def analisar_ano(rotulo, B, X, sec2coord, reps, nome_mun, G=None):
    log(rotulo, 'regressão por UF')
    r, reg = residuos(B['y'], X, B['uf'])
    rng = np.random.default_rng(SEMENTE)
    E0, _, _ = estat_mun(r, B['v2'], B)
    C = contagens_boot(E0['m2u'], reps, rng)
    out = {'secoes': int(len(r)), 'fora_da_amostra': B['fora'], 'regressao_por_uf': reg,
           'media_y': float(B['y'].mean()), 'variancia_y': float(B['y'].var()), 'variancia_r': float(r.var())}
    log(rotulo, 'componentes')
    principal, E, zon, loc = decompor(r, B['v2'], B, C)
    out['componentes'] = {k: v for k, v in principal.items() if k != 'boot_zona'}
    boot_zona = principal['boot_zona']
    out['componentes_por_uf'] = por_uf(E, B['nomes_uf'])
    var = {}
    for nome, vv in (('sem_desconto_binomial', np.zeros_like(B['v2'])), ('binomial_dos_dois_turnos', B['v1'] + B['v2'])):
        c, _, _, _ = decompor(r, vv, B, C)
        var[nome] = {'sigma2': c['sigma2'], 'ep': c['ep']}
    m50 = (B['comp1'] >= 50) & (B['comp2'] >= 50)
    Bs = sub(B, m50)
    r50, _ = residuos(Bs['y'], X[m50], Bs['uf'])
    C50 = contagens_boot(estat_mun(r50, Bs['v2'], Bs)[0]['m2u'], reps, np.random.default_rng(SEMENTE + 1))
    c50, _, _, _ = decompor(r50, Bs['v2'], Bs, C50)
    var['comparecimento_50_ou_mais_nos_dois_turnos'] = {'secoes': int(m50.sum()), 'sigma2': c50['sigma2'], 'ep': c50['ep']}
    out['variantes_descritivas'] = var
    log(rotulo, 'zonas extremas')
    ze = zonas_extremas(principal['sigma2'], E, zon, loc, B['nomes_zon'])
    for z in ze['maiores_efeitos']:
        uf, mun, _ = z['zona'].split('|'); z['municipio'] = nome_mun.get(f'{uf}|{mun}', '')
    out['zonas_extremas'] = ze
    log(rotulo, 'geometria dos pares')
    if G is None:
        G = geometria(B, sec2coord, E, loc)
    out['coordenadas'] = {k: G[k] for k in ('locais_total', 'locais_com_coordenada', 'locais_sem_coordenada',
                                            'locais_coordenada_inconsistente')}
    log(rotulo, 'degrau')
    rng2 = np.random.default_rng(SEMENTE + 2)
    dg = degrau(G, loc, principal['sigma2']['secao'], reps, rng2)
    for x in dg['maiores_municipios']:
        x['municipio'] = nome_mun.get(str(B['nomes_mun'][x['municipio_codigo']]), '')
        x['municipio_chave'] = str(B['nomes_mun'][x['municipio_codigo']])
    out['degrau'] = dg
    d2 = degrau(G, loc, principal['sigma2']['secao'], reps, np.random.default_rng(SEMENTE + 3), excluir_repetidas=True)
    out['degrau_sem_coordenadas_repetidas_por_3_ou_mais_locais'] = {k: d2[k] for k in (
        'pares_zonas_diferentes', 'pares_mesma_zona', 'degrau_pontos', 'ep_degrau_pontos', 'degrau2', 'ep_degrau2')}
    return out, boot_zona


def sub(B, m):
    """Subconjunto de seções, com os códigos refeitos."""
    S = {}
    for k in ('y', 'v1', 'v2', 'n2', 'comp1', 'comp2', 'uf'):
        S[k] = B[k][m]
    S['fora'] = B['fora']; S['sec'] = [s for s, t in zip(B['sec'], m) if t]
    for g, nomes in (('gu', 'nomes_uf'), ('gm', 'nomes_mun'), ('gz', 'nomes_zon'), ('gl', 'nomes_loc')):
        u, inv = np.unique(B[g][m], return_inverse=True)
        S[g] = inv; S[nomes] = B[nomes][u]
    return S


def resumo_ref(o):
    c = o['componentes']
    return {'sigma2_zona': c['sigma2']['zona'], 'ep_zona': c['ep']['zona'], 'degrau_pontos': o['degrau']['degrau_pontos'],
            'votos_zonas_extremas_a_favor': o['zonas_extremas']['votos_somados_a_favor_de_lula']}


def fmt(x, nd=2):
    return f'{x:+.{nd}f}'.replace('.', ',') if x is not None else 'n/d'


def fnum(x, nd=0):
    s = f'{x:,.{nd}f}'
    return s.replace(',', 'X').replace('.', ',').replace('X', '.')


def escrever_txt(out, caminho):
    L = []
    a = L.append
    a('T23. Componente de zona e degrau na fronteira de zona (Adendo 9), com o bweb completo do 2º turno de 2026')
    a('Script: scripts/analisar_T23.py. Bases: secoes2026.json.gz (1º e 2º turno, 499.206 seções), candidatos2026_1t.json.gz,')
    a('secoes2018.json.gz, secoes2022.json.gz; coordenadas: eleitorado_local_votacao_2026_<UF>.csv (linhas do 2º turno).')
    a('')
    a('Registro (Adendo 9, T23): "Resíduo r da variação da fatia de Lula por seção, de um modelo dentro da UF com a composição')
    a('completa do 1º turno e a variação do comparecimento. (a) Decompor a variância de r em município, zona dentro do município,')
    a('local dentro da zona e seção, descontando a variância binomial. (b) Nos municípios com 2 zonas ou mais, pares de locais a')
    a('até 1 km em zonas diferentes contra pares à mesma distância na mesma zona (coordenadas do cadastro de locais do TSE).')
    a('Sinal: componente de zona de pelo menos 2 vezes o maior de 2018 e 2022, degrau médio na fronteira de 1 ponto ou mais e mais')
    a('de 200 mil votos somados nas zonas extremas. Sem sinal: componente até 1,3 vez o das referências e degrau abaixo de 0,3 ponto."')
    a('')
    a('Leitura escolhida (o registro não fixa estes pontos; cada um é escolha declarada):')
    a('1. y = 100*(L2/(L2+R2) - L1/(L1+R1)), em pontos. 2018: Haddad contra Bolsonaro; 2022: Lula contra Bolsonaro; 2026: Lula')
    a('   contra Flávio. Modelo: uma regressão MQO sem peso por UF (constante e coeficientes próprios), contra as fatias do')
    a('   comparecimento do 1º turno de cada candidato (branco+nulo, com o 28 anulado como nulo, é a categoria omitida) e')
    a('   100*(C2-C1)/aptos. Exterior fora (não é UF e não tem coordenada).')
    a('2. (a) ANOVA aninhada desbalanceada (Henderson I, cada seção com peso 1), somas de quadrados juntadas nas 27 UFs. A variância')
    a('   binomial de cada seção, 10^4 p2(1-p2)/(L2+R2), entra exatamente nas esperanças e é descontada. "Componente de zona" =')
    a('   sigma2 de zona dentro do município, em pontos ao quadrado (identificado só nos municípios com 2 zonas ou mais).')
    a('   Erro-padrão: bootstrap de municípios estratificado por UF (2.000 reamostras).')
    a('3. (b) r do local = média de r das suas seções; coordenada do local = a das suas seções no cadastro de 2026. Pares a até 1 km')
    a('   no mesmo município, em faixas de 100 m; os pares da mesma zona são reponderados para a distribuição de distâncias dos pares')
    a('   em zonas diferentes. Por par, q = (r_a - r_b)^2 menos o ruído esperado das duas médias. Degrau^2 = média de q entre zonas')
    a('   menos a média na mesma zona à mesma distância; "degrau médio" = raiz (média quadrática do salto). Erro-padrão: bootstrap')
    a('   de municípios. Em 2018 e 2022 o degrau é descritivo (coordenadas de 2026 ligadas pela chave UF|município|zona|seção).')
    a('4. "Zonas extremas" = zonas (em municípios com 2 zonas ou mais) cujo efeito encolhido (BLUP do desvio da média do município)')
    a('   passa de 2 desvios-padrão do componente de zona; "votos somados" = soma do efeito/100 vezes os votos nos finalistas no 2º')
    a('   turno nas zonas extremas a favor de Lula. "O das referências" do sem sinal = o maior das duas, como no sinal.')
    a('')
    a('Desvios do registro:')
    a('- "Composição completa do 1º turno": 2026 usa Lula, Flávio, Cury, Renan, Caiado, Zema e demais. As bases de 2018 e 2022 têm')
    a('  por seção só L, R e "outros" (campo que faltou: votos por candidato no 1º turno de 2018 e 2022, QT_VOTOS por NR_VOTAVEL do')
    a('  cargo 1 no bweb, não baixado e sem rede nesta tarefa). As referências usam L, R e outros. Por isso 2026 sai também com a')
    a('  composição agregada (mesma especificação das referências), ao lado da principal.')
    a('- O critério não diz como medir o degrau, o que são "zonas extremas" nem que "votos" somar; as leituras 3 e 4 acima foram')
    a('  fixadas no script antes de rodar 2026 e as referências foram gravadas antes de a base de 2026 ser lida (primeira rodada,')
    a('  referências gravadas às 00h37min02s UTC de 29/10, 2026 lido em seguida). Depois dela só mudaram a formatação deste texto e')
    a('  campos descritivos (frações sobre a variância de r, razões contra cada referência em separado); os números do critério são')
    a('  idênticos aos da primeira rodada (sementes fixas).')
    a('')

    def bloco(rot, o):
        c = o['componentes']; s, e, fr = c['sigma2'], c['ep'], c['fracao_da_variancia_de_r']
        a(f'{rot}: {fnum(c["secoes"])} seções, {fnum(c["locais"])} locais, {fnum(c["zonas_municipio"])} zonas-município, '
          f'{fnum(c["municipios"])} municípios ({fnum(c["municipios_2_zonas_ou_mais"])} com 2 zonas ou mais, '
          f'{fnum(c["zonas_em_municipios_2_ou_mais"])} zonas neles)')
        a(f'  y médio {fmt(o["media_y"])} pontos; variância de y {fnum(o["variancia_y"], 2)}; de r {fnum(o["variancia_r"], 2)}; '
          f'binomial média {fnum(s["binomial_media"], 2)}')
        for k, nome in (('municipio', 'município'), ('zona', 'zona no município'), ('local', 'local na zona'), ('secao', 'seção (sem binomial)')):
            a(f'  {nome:22s} sigma2 {fmt(s[k], 3):>8s} (ep {fnum(e[k], 3)})  dp {fmt(c["dp_pontos"][k], 2)} ponto  '
              f'{fnum(100 * fr[k], 1)}% da variância de r')
        a(f'  {"binomial (descontada)":22s} média {fnum(s["binomial_media"], 3):>8s}                              '
          f'{fnum(100 * fr["binomial_media"], 1)}% da variância de r')
    a('(a) Componentes de variância de r (pontos ao quadrado)')
    for ano in ('2018', '2022'):
        bloco(f'{ano} (referência)', out['referencias'][ano])
    bloco('2026, composição completa (principal)', out['2026_composicao_completa'])
    bloco('2026, composição agregada como nas referências', out['2026_composicao_agregada_como_referencias'])
    a('')
    a('Critério')
    for nome, rot in (('2026_composicao_completa', 'principal'), ('2026_composicao_agregada_como_referencias', 'agregada')):
        k = out['criterio'][nome]
        a(f'  {rot}: componente de zona 2026 {fmt(k["sigma2_zona_2026"], 3)} (ep {fnum(k["ep"], 3)}) contra o maior das referências '
          f'{fmt(k["maior_referencia"], 3)} ({k["ano_da_maior_referencia"]}): razão {fnum(k["razao"], 2)} (ep bootstrap '
          f'{fnum(k["ep_razao_bootstrap"], 2)}; IC95 {fnum(k["ic95_razao_bootstrap"][0], 2)} a {fnum(k["ic95_razao_bootstrap"][1], 2)})')
        a(f'     degrau {fmt(k["degrau_pontos"], 2)} ponto (ep {fnum(k["ep_degrau"], 2)}); votos nas zonas extremas a favor de Lula '
          f'{fnum(k["votos_zonas_extremas_a_favor_de_lula"])}')
        sn = lambda b: 'sim' if b else 'não'
        a(f'     sinal: razão de 2 ou mais {sn(k["condicoes_sinal"]["razao>=2"])}, degrau de 1 ou mais {sn(k["condicoes_sinal"]["degrau>=1"])}, '
          f'mais de 200 mil votos {sn(k["condicoes_sinal"]["votos>200mil"])}; sem sinal: razão até 1,3 {sn(k["condicoes_sem_sinal"]["razao<=1.3"])}, '
          f'degrau abaixo de 0,3 {sn(k["condicoes_sem_sinal"]["degrau<0.3"])}  =>  {k["veredito"]}')
        a(f'     descritivo: razão contra 2022 só {fnum(k["razao_contra_2022"], 2)}, contra 2018 só {fnum(k["razao_contra_2018"], 2)}; '
          f'degrau 2026 menos 2022 {fmt(k["degrau_menos_2022"][0], 2)} (ep {fnum(k["degrau_menos_2022"][1], 2)}); '
          f'degrau^2 2026 menos 2022 {fmt(k["degrau2_menos_2022"][0], 3)} (ep {fnum(k["degrau2_menos_2022"][1], 3)})')
    a('')
    a('(b) Degrau na fronteira de zona (pares de locais a até 1 km, municípios com 2 zonas ou mais)')
    todos = [('2018 (descritivo)', out['referencias']['2018']), ('2022 (descritivo)', out['referencias']['2022']),
             ('2026 principal', out['2026_composicao_completa']), ('2026 agregada', out['2026_composicao_agregada_como_referencias'])]
    for rot, o in todos:
        d = o['degrau']; d2 = o['degrau_sem_coordenadas_repetidas_por_3_ou_mais_locais']; cc = o['coordenadas']
        a(f'  {rot}: {fnum(d["pares_zonas_diferentes"])} pares em zonas diferentes, {fnum(d["pares_mesma_zona"])} na mesma zona, '
          f'{d["municipios_com_pares"]} municípios; locais com coordenada {fnum(cc["locais_com_coordenada"])} de {fnum(cc["locais_total"])}')
        a(f'     degrau {fmt(d["degrau_pontos"], 2)} ponto (ep {fnum(d["ep_degrau_pontos"], 2)}; IC95 {fmt(d["ic95_degrau_pontos"][0], 2)} a '
          f'{fmt(d["ic95_degrau_pontos"][1], 2)}); degrau^2 {fmt(d["degrau2"], 3)} (ep {fnum(d["ep_degrau2"], 3)}); sem descontar o ruído '
          f'{fmt(d["sem_descontar_ruido_degrau_pontos"], 2)}; diferença média absoluta {fmt(d["diferenca_media_abs_pontos"], 3)} '
          f'(ep {fnum(d["ep_diferenca_media_abs"], 3)}); sem coordenadas repetidas {fmt(d2["degrau_pontos"], 2)} (ep {fnum(d2["ep_degrau_pontos"], 2)})')
    a('  (sinal negativo = a diferença entre zonas ficou abaixo da diferença na mesma zona; o valor é a raiz com o sinal de degrau^2)')
    a('  Municípios com mais pares entre zonas, 2026 principal (degrau do município):')
    for x in out['2026_composicao_completa']['degrau']['maiores_municipios']:
        a(f'     {x["municipio_chave"]:12s} {x["municipio"]:24s} {fnum(x["pares_zonas_diferentes"]):>6s} pares entre zonas, '
          f'{fnum(x["pares_mesma_zona"]):>7s} na mesma zona; degrau {fmt(x["degrau_pontos"], 2)}')
    a('')
    a('Zonas extremas (efeito encolhido acima de 2 dp do componente de zona)')
    for rot, o in todos:
        z = o['zonas_extremas']
        a(f'  {rot}: limiar {fmt(z["limiar_pontos"], 2) if z["limiar_pontos"] is not None else "n/d"} ponto; {z["zonas_avaliadas"]} zonas avaliadas; '
          f'{z["zonas_extremas_a_favor_de_lula"]} a favor (votos deslocados {fnum(z["votos_somados_a_favor_de_lula"])}, em zonas com '
          f'{fnum(z["votos_finalistas_nas_zonas_extremas_a_favor"])} votos), {z["zonas_extremas_contra_lula"]} contra '
          f'({fnum(z["votos_somados_contra_lula"])}); soma de |efeito| vezes votos em todas as zonas {fnum(z["soma_abs_efeito_vezes_votos_todas_as_zonas"])}')
    a('  Maiores efeitos de zona, 2026 principal:')
    for z in out['2026_composicao_completa']['zonas_extremas']['maiores_efeitos'][:10]:
        a(f'     {z["zona"]:14s} {z["municipio"]:24s} efeito {fmt(z["efeito_pontos"], 2)} (bruto {fmt(z["desvio_bruto_pontos"], 2)}), '
          f'{z["secoes"]} seções, {fnum(z["votos_finalistas_2T"])} votos')
    a('')
    a('Variantes descritivas do componente de zona (sigma2, ep)')
    for rot, o in todos:
        v = o['variantes_descritivas']
        a(f'  {rot}: sem desconto binomial {fmt(v["sem_desconto_binomial"]["sigma2"]["zona"], 3)} ({fnum(v["sem_desconto_binomial"]["ep"]["zona"], 3)}); '
          f'binomial dos dois turnos {fmt(v["binomial_dos_dois_turnos"]["sigma2"]["zona"], 3)} ({fnum(v["binomial_dos_dois_turnos"]["ep"]["zona"], 3)}); '
          f'comparecimento 50+ {fmt(v["comparecimento_50_ou_mais_nos_dois_turnos"]["sigma2"]["zona"], 3)} '
          f'({fnum(v["comparecimento_50_ou_mais_nos_dois_turnos"]["ep"]["zona"], 3)}); seção sem binomial nas três: '
          f'{fmt(v["sem_desconto_binomial"]["sigma2"]["secao"], 2)}, {fmt(v["binomial_dos_dois_turnos"]["sigma2"]["secao"], 2)}, '
          f'{fmt(v["comparecimento_50_ou_mais_nos_dois_turnos"]["sigma2"]["secao"], 2)}')
    a('')
    a('Componente de zona por UF (sigma2, ponto estimado; só UFs com município de 2 zonas ou mais): 2018 | 2022 | 2026 principal')
    u18, u22, u26 = (o['componentes_por_uf'] for o in (out['referencias']['2018'], out['referencias']['2022'], out['2026_composicao_completa']))
    for uf in sorted(u26):
        if u26[uf]['municipios_2_zonas_ou_mais'] == 0:
            continue
        g = lambda u: fmt(u[uf]['zona'], 3) if uf in u and u[uf]['municipios_2_zonas_ou_mais'] > 0 else '   n/d'
        a(f'  {uf}: {g(u18):>7s} | {g(u22):>7s} | {g(u26):>7s}   (municípios com 2 zonas ou mais em 2026: {u26[uf]["municipios_2_zonas_ou_mais"]})')
    a('')
    g, r18, r22 = out['2026_composicao_completa'], out['referencias']['2018'], out['referencias']['2022']
    k = out['criterio']['2026_composicao_completa']; ka = out['criterio']['2026_composicao_agregada_como_referencias']
    cg = g['componentes']
    a('Leitura')
    a(f'- Componente de zona: 2026 {fmt(k["sigma2_zona_2026"], 3)} (ep {fnum(k["ep"], 3)}), do tamanho do de 2022 '
      f'({fmt(r22["componentes"]["sigma2"]["zona"], 3)}, ep {fnum(r22["componentes"]["ep"]["zona"], 3)}; razão {fnum(k["razao_contra_2022"], 2)}) '
      f'e bem abaixo do de 2018 ({fmt(r18["componentes"]["sigma2"]["zona"], 3)}, ep {fnum(r18["componentes"]["ep"]["zona"], 3)}). '
      f'Razão contra o maior das referências {fnum(k["razao"], 2)} (IC95 {fnum(k["ic95_razao_bootstrap"][0], 2)} a '
      f'{fnum(k["ic95_razao_bootstrap"][1], 2)}); com a composição agregada, {fnum(ka["razao"], 2)}. A parte (a) fica dentro do sem '
      f'sinal (até 1,3 vez o maior das referências) nas duas especificações.')
    a(f'  Contra 2022 só (fora do critério, que usa o maior das duas): principal {fnum(k["razao_contra_2022"], 2)} (IC95 '
      f'{fnum(k["ic95_razao_contra_2022_bootstrap"][0], 2)} a {fnum(k["ic95_razao_contra_2022_bootstrap"][1], 2)}); agregada '
      f'{fnum(ka["razao_contra_2022"], 2)} (IC95 {fnum(ka["ic95_razao_contra_2022_bootstrap"][0], 2)} a '
      f'{fnum(ka["ic95_razao_contra_2022_bootstrap"][1], 2)}; diferença {fmt(ka["diferenca_contra_2022"][0], 3)}, ep '
      f'{fnum(ka["diferenca_contra_2022"][1], 3)}). A versão agregada põe os eliminados num bloco só; como eles pesam e transferem de modo '
      f'diferente por região, parte disso sobra no resíduo por zona. As referências têm a mesma limitação (Ciro, Alckmin, Tebet e '
      f'demais agregados), e com a composição completa de 2026 o componente cai para {fmt(k["sigma2_zona_2026"], 3)}.')
    a(f'- Degrau: {fmt(k["degrau_pontos"], 2)} ponto (ep {fnum(k["ep_degrau"], 2)}; IC95 {fmt(g["degrau"]["ic95_degrau_pontos"][0], 2)} a '
      f'{fmt(g["degrau"]["ic95_degrau_pontos"][1], 2)}). O intervalo exclui o degrau de 1 ponto do sinal, mas o ponto estimado fica '
      f'{fnum(k["degrau_pontos"] - LIM_SEM_DEGRAU, 3)} ponto acima do limite de 0,3 do sem sinal, com erro-padrão de '
      f'{fnum(k["ep_degrau"], 2)}: a medida não tem precisão para separar 0,3 de zero. Variantes: sem descontar o ruído '
      f'{fmt(g["degrau"]["sem_descontar_ruido_degrau_pontos"], 2)}; sem coordenadas repetidas '
      f'{fmt(g["degrau_sem_coordenadas_repetidas_por_3_ou_mais_locais"]["degrau_pontos"], 2)}; composição agregada {fmt(ka["degrau_pontos"], 2)}. '
      f'Referências descritivas: 2018 {fmt(r18["degrau"]["degrau_pontos"], 2)} (ep {fnum(r18["degrau"]["ep_degrau_pontos"], 2)}), '
      f'2022 {fmt(r22["degrau"]["degrau_pontos"], 2)} (ep {fnum(r22["degrau"]["ep_degrau_pontos"], 2)}); degrau^2 de 2026 menos o de 2022 '
      f'{fmt(k["degrau2_menos_2022"][0], 3)} (ep {fnum(k["degrau2_menos_2022"][1], 3)}).')
    a(f'- Zonas extremas: {fnum(k["votos_zonas_extremas_a_favor_de_lula"])} votos deslocados a favor de Lula, contra mais de 200 mil '
      f'exigidos no sinal; somando |efeito| vezes votos em todas as {g["zonas_extremas"]["zonas_avaliadas"]} zonas de municípios com 2 '
      f'zonas ou mais, {fnum(g["zonas_extremas"]["soma_abs_efeito_vezes_votos_todas_as_zonas"])} (2022: '
      f'{fnum(r22["zonas_extremas"]["soma_abs_efeito_vezes_votos_todas_as_zonas"])}; 2018: '
      f'{fnum(r18["zonas_extremas"]["soma_abs_efeito_vezes_votos_todas_as_zonas"])}).')
    a(f'- Variância binomial: a média descontada ({fnum(cg["sigma2"]["binomial_media"], 2)}) passa da variância total de r '
      f'({fnum(cg["sigma2"]["total_r"], 2)}) em 2026 e em 2022, e o componente de seção sai negativo nos três anos. A binomial de '
      f'eleitores independentes superestima o ruído da variação entre turnos, porque os eleitores da seção são os mesmos nos dois '
      f'turnos. O componente de seção não se interpreta; o de zona quase não muda com o desconto (variantes acima), porque a ANOVA o '
      f'separa pela variação dentro dos locais.')
    a(f'- Alcance: o componente de zona só se identifica nos {cg["municipios_2_zonas_ou_mais"]} municípios com 2 zonas ou mais '
      f'({fnum(cg["secoes_em_municipios_2_zonas_ou_mais"])} seções, {fnum(100 * cg["secoes_em_municipios_2_zonas_ou_mais"] / cg["secoes"], 1)}% '
      f'das seções). Nos municípios de zona única, um desvio por zona aparece como componente de município: 2026 '
      f'{fmt(cg["sigma2"]["municipio"], 3)} (ep {fnum(cg["ep"]["municipio"], 3)}), 2022 {fmt(r22["componentes"]["sigma2"]["municipio"], 3)} '
      f'(ep {fnum(r22["componentes"]["ep"]["municipio"], 3)}), 2018 {fmt(r18["componentes"]["sigma2"]["municipio"], 3)}. Um desvio igual em '
      f'todas as zonas não gera variância entre zonas e não é visto por este teste.')
    a('')
    a(f'VEREDITO PELA LETRA: {out["veredito"]}')
    with open(caminho, 'w') as f:
        f.write('\n'.join(L) + '\n')


def main():
    if '--so-texto' in sys.argv:
        out = json.load(open(sys.argv[sys.argv.index('--so-texto') + 1]))
        escrever_txt(out, sys.argv[sys.argv.index('--so-texto') + 2])
        return
    s26, cand26, s18, s22, pasta, saida_json, saida_txt, saida_ref = sys.argv[1:9]
    reps = int(sys.argv[sys.argv.index('--reps') + 1]) if '--reps' in sys.argv else 2000
    log('lendo locais de 2026')
    sec2coord, nome_mun = ler_locais(pasta)
    log('seções com coordenada no cadastro de 2026 (2º turno):', len(sec2coord))
    out = {'teste': 'T23', 'reps_bootstrap': reps, 'semente': SEMENTE, 'referencias': {}}
    boots = {}
    for ano, cam in (('2018', s18), ('2022', s22)):
        log('lendo', ano)
        B = montar(cam)
        o, bz = analisar_ano(ano, B, B['XA'], sec2coord, reps, nome_mun)
        out['referencias'][ano] = o; boots[ano] = bz
        del B; gc.collect()
    with open(saida_ref, 'w') as f:
        json.dump({'gravado_em_utc': time.strftime('%Y-%m-%dT%H:%M:%SZ', time.gmtime()),
                   'referencias': {a: resumo_ref(o) for a, o in out['referencias'].items()}}, f, ensure_ascii=False, indent=1)
    log('referências gravadas em', saida_ref)
    log('lendo 2026')
    B = montar(s26, cand26)
    o_g, bz_g = analisar_ano('2026 composição completa', B, B['XG'], sec2coord, reps, nome_mun)
    o_a, bz_a = analisar_ano('2026 composição agregada', B, B['XA'], sec2coord, reps, nome_mun)
    out['2026_composicao_completa'] = o_g
    out['2026_composicao_agregada_como_referencias'] = o_a
    # critério
    z18, z22 = (out['referencias'][a]['componentes']['sigma2']['zona'] for a in ('2018', '2022'))
    zmax = max(z18, z22); ano_max = '2018' if z18 >= z22 else '2022'
    bmax = np.maximum(boots['2018'], boots['2022'])
    crit = {}
    for nome, o, bz in (('2026_composicao_completa', o_g, bz_g), ('2026_composicao_agregada_como_referencias', o_a, bz_a)):
        z = o['componentes']['sigma2']['zona']
        razao = z / zmax
        rb = bz / bmax
        dg = o['degrau']['degrau_pontos']
        vt = o['zonas_extremas']['votos_somados_a_favor_de_lula']
        sinal = razao >= LIM_SINAL_RAZAO and dg >= LIM_SINAL_DEGRAU and vt > LIM_SINAL_VOTOS
        sem = razao <= LIM_SEM_RAZAO and dg < LIM_SEM_DEGRAU
        crit[nome] = {'sigma2_zona_2026': z, 'ep': o['componentes']['ep']['zona'],
                      'maior_referencia': zmax, 'ano_da_maior_referencia': ano_max,
                      'razao': razao, 'ep_razao_bootstrap': float(np.std(rb, ddof=1)),
                      'ic95_razao_bootstrap': [float(np.percentile(rb, 2.5)), float(np.percentile(rb, 97.5))],
                      'degrau_pontos': dg, 'ep_degrau': o['degrau']['ep_degrau_pontos'],
                      'votos_zonas_extremas_a_favor_de_lula': vt,
                      'condicoes_sinal': {'razao>=2': razao >= LIM_SINAL_RAZAO, 'degrau>=1': dg >= LIM_SINAL_DEGRAU,
                                          'votos>200mil': vt > LIM_SINAL_VOTOS},
                      'condicoes_sem_sinal': {'razao<=1.3': razao <= LIM_SEM_RAZAO, 'degrau<0.3': dg < LIM_SEM_DEGRAU},
                      'veredito': 'SINAL' if sinal else ('SEM SINAL' if sem else 'INCONCLUSIVO')}
        d22 = out['referencias']['2022']['degrau']
        crit[nome].update({
            'razao_contra_2022': z / z22, 'razao_contra_2018': z / z18,
            'ep_razao_contra_2022_bootstrap': float(np.std(bz / boots['2022'], ddof=1)),
            'ic95_razao_contra_2022_bootstrap': [float(np.percentile(bz / boots['2022'], 2.5)), float(np.percentile(bz / boots['2022'], 97.5))],
            'diferenca_contra_2022': [z - z22, float(np.hypot(o['componentes']['ep']['zona'], out['referencias']['2022']['componentes']['ep']['zona']))],
            'degrau_menos_2022': [dg - d22['degrau_pontos'], float(np.hypot(o['degrau']['ep_degrau_pontos'], d22['ep_degrau_pontos']))],
            'degrau2_menos_2022': [o['degrau']['degrau2'] - d22['degrau2'], float(np.hypot(o['degrau']['ep_degrau2'], d22['ep_degrau2']))]})
    out['criterio'] = crit
    out['rodado_em_utc'] = time.strftime('%Y-%m-%dT%H:%M:%SZ', time.gmtime())
    out['veredito'] = crit['2026_composicao_completa']['veredito']
    with open(saida_json, 'w') as f:
        json.dump(out, f, ensure_ascii=False, indent=1)
    escrever_txt(out, saida_txt)
    log('veredito', out['veredito'])
    print(json.dumps(crit, ensure_ascii=False, indent=1))


if __name__ == '__main__':
    main()
