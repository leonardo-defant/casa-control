"""F4 do Adendo 20: modelo de urna no bweb inteiro.

Registro (Adendo 20, commit d976d4d):
  - Mapa do número da urna para o modelo pelos logs da amostra (o log informa o modelo; o boletim, o número). Só se
    aplica ao bweb se as faixas forem limpas: cada faixa com um modelo só em 99% ou mais das urnas da amostra. Se não
    forem, o teste fica SEM PODER.
  - Virada de Lula (fatia entre os dois finalistas, 2º turno menos 1º) com efeito fixo de local, erro agrupado por
    local, peso pelos votos dos finalistas no 2º turno, um indicador por modelo (referência: o mais comum). Placebo: a
    fatia do 1º turno como variável.
  - Sinal: algum modelo com 5.000 seções ou mais e diferença de 1,0 ponto ou mais a favor de Lula, a mais de 4
    erros-padrão. Sem sinal: todos com diferença abaixo de 0,3 em valor absoluto e erro-padrão até 0,15. Entre os
    dois: inconclusivo.

Decisões tomadas antes de calcular a regressão (o registro não fixa estes pontos; cada uma é declarada como desvio):
  D1. Mapa: toda linha "Identificação do Modelo de Urna: UExxxx" de todo logd.dat do pacote de log da amostra do 2º
      turno, inclusive os .jez aninhados (log da urna original quando houve contingência). O número da urna é o da
      própria linha (terceira coluna do log, sem os zeros à esquerda). Cada número distinto de urna conta uma vez. Um
      número com mais de um modelo nos logs é um conflito e entra na pureza como urna que não bate com a faixa.
  D2. Elo com o boletim: para cada seção da amostra, o número da urna do boletim do 2º turno (base decodificada da
      amostra) tem de aparecer entre os números do log da seção; a taxa de acerto é relatada. A pureza principal usa
      todos os números distintos dos logs; a pureza só com a urna do boletim de cada seção é relatada ao lado.
  D3. Faixas: o registro não define os limites. Faixa = um intervalo contínuo de números por modelo, na ordem da
      mediana dos números de cada modelo na amostra; os pontos de corte são os que maximizam o número de urnas da
      amostra cujo modelo é o da sua faixa (busca exata por programação dinâmica sobre os números ordenados), com o
      corte no meio entre dois números vizinhos da amostra. A faixa vai do menor ao maior número da amostra que cai
      nela. Faixa limpa = modelo da faixa em 99% ou mais das urnas da amostra que caem nela. As faixas antigas do
      repositório (scripts/modelos.py, ano 2026) são avaliadas do mesmo jeito, só como segunda leitura.
  D4. Aplicação ao bweb: número da urna do 2º turno de cada seção (NR_URNA_EFETIVADA do bweb do 2º turno). O modelo é
      o da faixa entre os cortes; número abaixo do menor ou acima do maior número da amostra fica sem modelo e sai
      (contagem relatada). Números entre o último da amostra de uma faixa e o primeiro da seguinte (zona de corte)
      recebem o modelo pelo corte e são contados à parte.
  D5. Amostra da regressão: todas as seções do bweb (Brasil e exterior) com os dois turnos, comparecimento e votos
      dos finalistas positivos nos dois turnos e modelo definido. y = 100 x [L2/(L2+R2) - L1/(L1+R1)]; peso L2+R2;
      local = UF|município|zona|local de votação do 2º turno; erro agrupado por local (CR1, scripts/lib.py); locais
      com uma seção só saem (não informam com efeito fixo). Sem covariáveis, porque o registro não lista nenhuma.
      Referência = o modelo com mais seções na amostra da regressão. Placebo: y = 100 x L1/(L1+R1), mesmos
      indicadores, pesos e efeito fixo.
  D6. "5.000 seções ou mais": seções do modelo na amostra da regressão (depois de sair os locais de uma seção). As
      seções do modelo em locais com mais de um modelo (as que identificam o coeficiente) são relatadas ao lado.
  D7. "A favor de Lula": coeficiente positivo do indicador do modelo na virada, contra a referência. Leitura
      complementar, fora do veredito: todos os pares de modelos (a regressão refeita com cada modelo como referência),
      para o caso de o modelo alterado ser a própria referência.
  D8. "A mais de 4 erros-padrão": coeficiente maior que 4 vezes o seu erro-padrão.
  D9. "Sem sinal" vale para todos os indicadores de modelo, qualquer que seja o tamanho do modelo.
  D10. Se as faixas não forem limpas, o veredito é SEM PODER; a regressão ainda é rodada e relatada como descritiva.
  Robustez (descritiva, fora do veredito): (a) com as covariáveis do T17 (log dos aptos, variação do comparecimento,
  fatia de Lula no 1º turno); (b) só seções com a mesma urna nos dois turnos; (c) sem o exterior; (d) com as faixas de
  scripts/modelos.py; (e) sem as urnas da zona de corte.
  Conferência fora do registro (não muda o veredito): erro-padrão por bootstrap de locais (200 réplicas, semente
  20261030) nos locais com mais de um modelo; combinações de modelos por local; quanto cada modelo sozinho teria de
  mover para responder pela margem nacional.

Uso: python3 -I analisar_F4.py <secoes2026.json.gz> <pasta_arq_amostra_2t> <secoes2026_2t_amostra.json.gz>
                               <saida.json> <saida.txt>
"""
import os as _os, sys as _sys
_sys.path.insert(0, _os.path.dirname(_os.path.abspath(__file__)))
import collections, json, os, re, sys, warnings
from multiprocessing import Pool
import numpy as np
from lib import carregar, chave_local, fe_ols, demean
from decodificar import _linhas_log
from modelos import FAIXAS as FAIXAS_ANTIGAS
warnings.filterwarnings('ignore')

RX_MOD = re.compile(r'Identifica\S* do [Mm]odelo de [Uu]rna:\s*(\S+)')
PUREZA_MIN = 0.99
MIN_SECOES = 5000


# ---------------------------------------------------------------- mapa pelos logs da amostra
def ler_pacote(caminho):
    """Pares (número da urna, modelo) de todas as linhas de modelo e todos os números de urna do pacote de log."""
    pares = collections.Counter(); urnas = set(); blocos = 0
    try:
        bl = _linhas_log(caminho)
    except Exception as e:  # pacote ilegível
        return {'erro': repr(e)}
    for b in bl:
        blocos += 1
        for l in b:
            p = l.split('\t')
            if len(p) < 5:
                continue
            u = p[2].strip()
            if u.isdigit():
                urnas.add(int(u))
            m = RX_MOD.search(p[4])
            if m and u.isdigit():
                pares[(int(u), m.group(1).strip())] += 1
    return {'pares': [[u, m, q] for (u, m), q in pares.items()], 'urnas': sorted(urnas), 'blocos': blocos}


def secoes_amostra(pasta):
    out = []
    for uf in sorted(os.listdir(pasta)):
        for m in sorted(os.listdir(os.path.join(pasta, uf))):
            for z in sorted(os.listdir(os.path.join(pasta, uf, m))):
                for sc in sorted(os.listdir(os.path.join(pasta, uf, m, z))):
                    p = os.path.join(pasta, uf, m, z, sc)
                    if not os.path.isdir(p):
                        continue
                    logs = sorted(f for f in os.listdir(p) if f.endswith('-log.jez'))
                    out.append((f'{uf.upper()}|{int(m)}|{int(z)}|{int(sc)}', [os.path.join(p, f) for f in logs]))
    return out


def _trabalho(item):
    k, arqs = item
    return k, [ler_pacote(a) for a in arqs]


def montar_mapa(pasta, am):
    itens = secoes_amostra(pasta)
    with Pool(4) as pool:
        res = dict(pool.map(_trabalho, itens, chunksize=20))
    modelos_por_urna = collections.defaultdict(collections.Counter)
    elo = {'secoes_na_pasta': len(itens), 'secoes_com_log': 0, 'pacotes_ilegiveis': 0, 'secoes_na_base_decodificada': 0,
           'urna_do_boletim_no_log': 0, 'urna_do_boletim_com_linha_de_modelo': 0, 'urna_do_boletim_fora_do_log': []}
    urna_bu = {}
    for k, pacotes in res.items():
        if pacotes:
            elo['secoes_com_log'] += 1
        urnas_sec = set(); com_mod = set()
        for pk in pacotes:
            if 'erro' in pk:
                elo['pacotes_ilegiveis'] += 1; continue
            urnas_sec.update(pk['urnas'])
            for u, mo, q in pk['pares']:
                modelos_por_urna[u][mo] += q; com_mod.add(u)
        b = am.get(k, {}).get('2')
        if b is None:
            continue
        elo['secoes_na_base_decodificada'] += 1
        urna_bu[k] = b['urna']
        if b['urna'] in urnas_sec:
            elo['urna_do_boletim_no_log'] += 1
        else:
            elo['urna_do_boletim_fora_do_log'].append(k)
        if b['urna'] in com_mod:
            elo['urna_do_boletim_com_linha_de_modelo'] += 1
    conflitos = {u: dict(c) for u, c in modelos_por_urna.items() if len(c) > 1}
    mapa = {u: (c.most_common(1)[0][0] if len(c) == 1 else 'CONFLITO:' + '+'.join(sorted(c))) for u, c in modelos_por_urna.items()}
    return mapa, conflitos, urna_bu, elo


# ---------------------------------------------------------------- faixas
def faixas_otimas(mapa):
    """Um intervalo por modelo, na ordem da mediana; cortes que maximizam os acertos (programação dinâmica)."""
    itens = sorted((u, m) for u, m in mapa.items() if not m.startswith('CONFLITO'))
    mods = sorted({m for _, m in itens}, key=lambda m: float(np.median([u for u, mm in itens if mm == m])))
    N, K = len(itens), len(mods)
    P = np.zeros((K, N + 1), int)
    for j, m in enumerate(mods):
        P[j, 1:] = np.cumsum([1 if mm == m else 0 for _, mm in itens])
    NEG = -10 ** 9
    dp = np.full((K + 1, N + 1), NEG, int); arg = np.zeros((K + 1, N + 1), int)
    dp[0, 0] = 0
    for j in range(1, K + 1):
        best, bi = NEG, 0
        for i in range(N + 1):
            v = dp[j - 1, i] - P[j - 1, i]
            if v > best:
                best, bi = v, i
            dp[j, i] = best + P[j - 1, i]; arg[j, i] = bi
    cortes_idx = []; i = N
    for j in range(K, 0, -1):
        i0 = arg[j, i]; cortes_idx.append((i0, i)); i = i0
    cortes_idx = cortes_idx[::-1]
    faixas = []
    for j, (a, b) in enumerate(cortes_idx):
        nums = [u for u, _ in itens[a:b]]
        faixas.append({'modelo': mods[j], 'primeiro_da_amostra': nums[0] if nums else None,
                       'ultimo_da_amostra': nums[-1] if nums else None})
    # cortes no meio entre vizinhos
    for j in range(K - 1):
        a = faixas[j]['ultimo_da_amostra']; b = faixas[j + 1]['primeiro_da_amostra']
        faixas[j]['corte_superior'] = (a + b) / 2 if a is not None and b is not None else None
    faixas[-1]['corte_superior'] = None
    return faixas, int(dp[K, N]), N


def classificar(u, faixas, minimo, maximo):
    if u < minimo or u > maximo:
        return None
    for f in faixas:
        if f['corte_superior'] is None or u < f['corte_superior']:
            return f['modelo']
    return None


def pureza(mapa_sub, faixas_lim):
    """faixas_lim: lista (lo, hi, modelo). Pureza de cada faixa e urnas fora de toda faixa."""
    out = []; fora = 0
    cont = [collections.Counter() for _ in faixas_lim]
    for u, m in mapa_sub.items():
        achou = False
        for i, (lo, hi, mo) in enumerate(faixas_lim):
            if lo <= u <= hi:
                cont[i][m] += 1; achou = True; break
        if not achou:
            fora += 1
    for (lo, hi, mo), c in zip(faixas_lim, cont):
        n = sum(c.values())
        out.append({'faixa': [lo, hi], 'modelo': mo, 'urnas_da_amostra': n, 'do_modelo': c.get(mo, 0),
                    'pureza': (c.get(mo, 0) / n) if n else None, 'outros_modelos': {k: v for k, v in c.items() if k != mo}})
    return out, fora


# ---------------------------------------------------------------- regressão
def montar_linhas(d, mod_de):
    rows = []
    for k, v in d.items():
        a, b = v.get('1'), v.get('2')
        if not a or not b:
            continue
        if a['comp'] <= 0 or b['comp'] <= 0 or a['L'] + a['R'] <= 0 or b['L'] + b['R'] <= 0:
            continue
        rows.append({'k': k, 'uf': k.split('|')[0], 'loc': chave_local(k, b), 'urna': b['urna'], 'urna1': a['urna'],
                     'mod': mod_de(b['urna']), 'mod1': mod_de(a['urna']), 'apt': b['apt'],
                     'L1': a['L'], 'R1': a['R'], 'C1': a['comp'], 'L2': b['L'], 'R2': b['R'], 'C2': b['comp']})
    return rows


def regressao(rows, ref=None, covariaveis=False):
    rows = [r for r in rows if r['mod'] is not None]
    cnt = collections.Counter(r['mod'] for r in rows)
    ref = ref or cnt.most_common(1)[0][0]
    mods = sorted(m for m in cnt if m != ref)
    loc = np.array([r['loc'] for r in rows])
    L1, R1, C1, L2, R2, C2, apt = [np.array([r[c] for r in rows], float) for c in ('L1', 'R1', 'C1', 'L2', 'R2', 'C2', 'apt')]
    w = L2 + R2
    f1 = 100 * L1 / (L1 + R1); f2 = 100 * L2 / (L2 + R2)
    D = np.column_stack([np.array([1.0 if r['mod'] == m else 0.0 for r in rows]) for m in mods]) if mods else np.zeros((len(rows), 0))
    nomes = list(mods)
    if covariaveis:
        D = np.column_stack([D, np.log(apt), 100 * (C2 - C1) / apt, f1]); nomes += ['log_aptos', 'var_comparecimento', 'fatia_lula_1t']
    # seções que ficam (locais com 2 ou mais seções) e seções em locais com mais de um modelo
    porloc = collections.Counter(loc.tolist())
    fica = np.array([porloc[l] >= 2 for l in loc.tolist()])
    mods_loc = collections.defaultdict(set)
    for r in rows:
        mods_loc[r['loc']].add(r['mod'])
    misto = np.array([len(mods_loc[r['loc']]) >= 2 for r in rows])
    out = {'referencia': ref, 'secoes_por_modelo': {m: int(sum(1 for r, f in zip(rows, fica) if f and r['mod'] == m)) for m in [ref] + mods},
           'secoes_por_modelo_em_locais_mistos': {m: int(sum(1 for r, f in zip(rows, misto) if f and r['mod'] == m)) for m in [ref] + mods},
           'locais_mistos': int(sum(1 for s in mods_loc.values() if len(s) >= 2)),
           'locais_com_modelo_e_referencia': {m: int(sum(1 for s in mods_loc.values() if m in s and ref in s)) for m in mods}}
    for nome, y, X, nm in (('virada', f2 - f1, D, nomes), ('placebo_fatia_1t', f1, D[:, :len(mods)], list(mods))):
        r = fe_ols(y, X, loc, w, nm)
        out[nome] = {'n': r['n'], 'locais': r['grupos'], 'coef': {m: r['coef'][m] for m in nm},
                     'ep': {m: r['ep'][m] for m in nm}}
    # médias brutas ponderadas por modelo (descritivo)
    out['media_bruta_ponderada'] = {}
    for m in [ref] + mods:
        s = np.array([r['mod'] == m for r in rows])
        out['media_bruta_ponderada'][m] = {'virada': float(np.average((f2 - f1)[s], weights=w[s])),
                                           'fatia_lula_1t': float(np.average(f1[s], weights=w[s])),
                                           'fatia_lula_2t': float(np.average(f2[s], weights=w[s])),
                                           'secoes': int(s.sum())}
    return out


def veredito(reg, faixas_limpas):
    v = reg['virada']; mods = [m for m in v['coef'] if m in reg['secoes_por_modelo']]
    linhas = {}
    sinal = False; sem = True
    for m in mods:
        b, se = v['coef'][m], v['ep'][m]; n = reg['secoes_por_modelo'][m]
        s_m = n >= MIN_SECOES and b >= 1.0 and b > 4 * se
        sinal |= s_m
        sem &= abs(b) < 0.3 and se <= 0.15
        linhas[m] = {'coef': b, 'ep': se, 'z': b / se if se > 0 else None, 'secoes': n,
                     'efeito_minimo_detectavel_80pc': 2.8 * se, 'sinal_neste_modelo': bool(s_m),
                     'dentro_do_sem_sinal': bool(abs(b) < 0.3 and se <= 0.15)}
    pela_regressao = 'SINAL' if sinal else 'SEM SINAL' if sem else 'INCONCLUSIVO'
    final = pela_regressao if faixas_limpas else 'SEM PODER'
    return {'por_modelo': linhas, 'pela_regressao': pela_regressao, 'veredito': final}


def bootstrap_locais(rows, ref, reps=200, semente=20261030):
    """Conferência do erro-padrão (fora do registro): bootstrap por local nos locais com mais de um modelo, que são os
    únicos que informam os indicadores quando não há covariáveis."""
    rows = [r for r in rows if r['mod'] is not None]
    ml = collections.defaultdict(set)
    for r in rows:
        ml[r['loc']].add(r['mod'])
    rows = [r for r in rows if len(ml[r['loc']]) >= 2]
    mods = sorted({r['mod'] for r in rows} - {ref})
    loc = np.array([r['loc'] for r in rows]); _, g = np.unique(loc, return_inverse=True)
    L1, R1, L2, R2 = [np.array([r[c] for r in rows], float) for c in ('L1', 'R1', 'L2', 'R2')]
    w = L2 + R2; y = 100 * (L2 / w - L1 / (L1 + R1))
    X = np.column_stack([[1.0 if r['mod'] == m else 0.0 for r in rows] for m in mods])

    def est(y, X, g, w):
        Z = demean(np.column_stack([y, X]), g, w); yd, Xd = Z[:, 0], Z[:, 1:]
        return np.linalg.solve((Xd * w[:, None]).T @ Xd, (Xd * w[:, None]).T @ yd)
    G = g.max() + 1
    por = [np.where(g == i)[0] for i in range(G)]
    rng = np.random.default_rng(semente); bs = []
    for _ in range(reps):
        pick = rng.integers(0, G, G)
        ii = np.concatenate([por[i] for i in pick])
        gg = np.concatenate([np.full(len(por[i]), j) for j, i in enumerate(pick)])
        try:
            bs.append(est(y[ii], X[ii], gg, w[ii]))
        except np.linalg.LinAlgError:
            pass
    bs = np.array(bs)
    return {'secoes': len(rows), 'locais': int(G), 'replicas_validas': int(len(bs)), 'semente': semente,
            'coef_nos_locais_mistos': dict(zip(mods, est(y, X, g, w).tolist())),
            'ep_bootstrap': dict(zip(mods, bs.std(0, ddof=1).tolist()))}


def combinacoes(rows):
    ml = collections.defaultdict(set)
    for r in rows:
        if r['mod']:
            ml[r['loc']].add(r['mod'])
    c = collections.Counter(); uf = collections.defaultdict(collections.Counter)
    for lo, st in ml.items():
        if len(st) >= 2:
            t = '+'.join(sorted(st)); c[t] += 1; uf[t][lo.split('|')[0]] += 1
    return {t: {'locais': n, 'por_uf': dict(uf[t].most_common(6))} for t, n in c.most_common()}


def contexto_nacional(d, rows, reg):
    """Quanto um modelo sozinho teria de mudar a fatia nas suas seções para responder pela margem inteira."""
    L = sum(v['2']['L'] for v in d.values() if v.get('2')); R = sum(v['2']['R'] for v in d.values() if v.get('2'))
    meia = (L - R) / 2
    out = {'lula_2t': L, 'flavio_2t': R, 'votos_para_inverter': meia, 'por_modelo': {}}
    for m in reg['secoes_por_modelo']:
        V = sum(r['L2'] + r['R2'] for r in rows if r['mod'] == m)
        x = {'votos_finalistas_2t': V, 'pontos_necessarios_so_neste_modelo': 100 * meia / V if V else None}
        if m in reg['virada']['coef']:
            b, se = reg['virada']['coef'][m], reg['virada']['ep'][m]
            x['ic95_contra_referencia'] = [b - 1.96 * se, b + 1.96 * se]
        out['por_modelo'][m] = x
    return out


# ---------------------------------------------------------------- texto
def fz(x, c=2):
    if x is None:
        return 'n/d'
    s = f'{x:,.{c}f}'
    return s.replace(',', 'X').replace('.', ',').replace('X', '.')


def fi(x):
    return f'{int(x):,}'.replace(',', '.')


def main():
    arq_d, pasta, arq_am, saida_json, saida_txt = sys.argv[1:6]
    d = carregar(arq_d); am = carregar(arq_am)
    mapa, conflitos, urna_bu, elo = montar_mapa(pasta, am)
    modelos_cont = collections.Counter(m for m in mapa.values())
    faixas, acertos, N = faixas_otimas(mapa)
    minimo = min(u for u, m in mapa.items() if not m.startswith('CONFLITO'))
    maximo = max(u for u, m in mapa.items() if not m.startswith('CONFLITO'))
    lim = []
    for j, f in enumerate(faixas):
        lo = minimo if j == 0 else faixas[j - 1]['corte_superior']
        hi = maximo if f['corte_superior'] is None else f['corte_superior']
        lim.append((lo, hi, f['modelo']))
    # pureza: todas as urnas dos logs (conflito conta como não batendo) e só a urna do boletim
    pz_todas, fora_todas = pureza(mapa, lim)
    mapa_bu = {u: mapa[u] for u in set(urna_bu.values()) if u in mapa}
    pz_bu, fora_bu = pureza(mapa_bu, lim)
    limpas = all(p['pureza'] is not None and p['pureza'] >= PUREZA_MIN for p in pz_todas) and \
        all(p['pureza'] is None or p['pureza'] >= PUREZA_MIN for p in pz_bu)
    ant = [(a, b, m) for a, b, m in FAIXAS_ANTIGAS[2026]]
    pz_ant, fora_ant = pureza(mapa, ant)

    def mod_de(u):
        return classificar(u, faixas, minimo, maximo)

    def mod_ant(u):
        for a, b, m in ant:
            if a <= u <= b:
                return m
        return None

    # zonas de corte (entre o último da amostra de uma faixa e o primeiro da seguinte)
    zonas = [(faixas[j]['ultimo_da_amostra'], faixas[j + 1]['primeiro_da_amostra']) for j in range(len(faixas) - 1)]

    def na_zona(u):
        return any(a < u < b for a, b in zonas)

    rows = montar_linhas(d, mod_de)
    todas2 = [v['2']['urna'] for v in d.values() if v.get('2')]
    aplic = {'secoes_bweb_2t': len(todas2), 'secoes_sem_modelo_fora_da_amostra': int(sum(1 for u in todas2 if mod_de(u) is None)),
             'secoes_na_zona_de_corte': int(sum(1 for u in todas2 if na_zona(u))),
             'modelos_no_bweb_2t': dict(collections.Counter(str(mod_de(u)) for u in todas2)),
             'modelos_no_bweb_2t_faixas_antigas': dict(collections.Counter(str(mod_ant(u)) for u in todas2)),
             'concordancia_faixas_novas_e_antigas': float(np.mean([mod_de(u) == mod_ant(u) for u in todas2])),
             'secoes_na_regressao_antes_do_efeito_fixo': len(rows)}
    # conferência: urna do bweb do 2º turno nas seções da amostra contra a do boletim e o modelo do log
    conf = {'secoes': 0, 'urna_igual_ao_boletim': 0, 'modelo_da_faixa_igual_ao_log': 0, 'diferentes': []}
    for k, u in urna_bu.items():
        b = d.get(k, {}).get('2')
        if not b:
            continue
        conf['secoes'] += 1
        conf['urna_igual_ao_boletim'] += int(b['urna'] == u)
        ml = mapa.get(b['urna'])
        if ml is not None:
            if mod_de(b['urna']) == ml:
                conf['modelo_da_faixa_igual_ao_log'] += 1
            else:
                conf['diferentes'].append([k, b['urna'], ml, mod_de(b['urna'])])

    reg = regressao(rows)
    ver = veredito(reg, limpas)
    # pares (cada modelo como referência)
    pares = {}
    for m in sorted({r['mod'] for r in rows if r['mod']}):
        rr = regressao(rows, ref=m)
        pares[m] = {o: {'coef': rr['virada']['coef'][o], 'ep': rr['virada']['ep'][o]} for o in rr['virada']['coef']}
    rob = {'a_covariaveis_T17': regressao(rows, ref=reg['referencia'], covariaveis=True),
           'b_mesma_urna_nos_dois_turnos': regressao([r for r in rows if r['urna'] == r['urna1']], ref=reg['referencia']),
           'c_sem_exterior': regressao([r for r in rows if r['uf'] != 'ZZ'], ref=reg['referencia']),
           'd_faixas_antigas_modelos_py': regressao([dict(r, mod=mod_ant(r['urna'])) for r in rows], ref=reg['referencia']),
           'e_sem_zona_de_corte': regressao([r for r in rows if not na_zona(r['urna'])], ref=reg['referencia'])}
    for kk in rob:
        rob[kk]['leitura_pelo_criterio'] = veredito(rob[kk], True)['pela_regressao']
    boot = bootstrap_locais(rows, reg['referencia'])
    combos = combinacoes(rows)
    ctx = contexto_nacional(d, rows, reg)
    ext_ced = sorted(k for k, v in d.items() if k.startswith('ZZ|') and v.get('2') and not v['2']['ab'].strip())
    # pistas descritivas
    urnas_rep = collections.Counter(v['2']['urna'] for v in d.values() if v.get('2'))
    rep = {str(u): sorted(k for k, v in d.items() if v.get('2') and v['2']['urna'] == u) for u, c in urnas_rep.items() if c > 1}
    troca = collections.Counter((str(r['mod1']), str(r['mod'])) for r in rows if r['urna'] != r['urna1'])
    por_uf = collections.defaultdict(collections.Counter)
    for r in rows:
        por_uf[r['uf']][str(r['mod'])] += 1

    out = {'teste': 'F4 do Adendo 20: modelo de urna no bweb inteiro',
           'mapa': {'urnas_distintas_nos_logs': len(mapa), 'modelos': dict(modelos_cont), 'conflitos': {str(k): v for k, v in conflitos.items()},
                    'elo_com_o_boletim': dict(elo, urna_do_boletim_fora_do_log=elo['urna_do_boletim_fora_do_log'][:50],
                                              n_urna_do_boletim_fora_do_log=len(elo['urna_do_boletim_fora_do_log']))},
           'faixas': {'definicao': 'um intervalo por modelo, cortes que maximizam acertos, corte no meio entre vizinhos',
                      'faixas': faixas, 'limites_usados': lim, 'acertos': acertos, 'urnas': N,
                      'pureza_todas_as_urnas_dos_logs': pz_todas, 'fora_de_faixa_todas': fora_todas,
                      'pureza_so_urna_do_boletim': pz_bu, 'fora_de_faixa_boletim': fora_bu,
                      'pureza_minima_exigida': PUREZA_MIN, 'faixas_limpas': bool(limpas),
                      'faixas_antigas_modelos_py': {'faixas': ant, 'pureza': pz_ant, 'urnas_da_amostra_fora_delas': fora_ant}},
           'aplicacao_ao_bweb': aplic, 'conferencia_amostra_bweb': dict(conf, diferentes=conf['diferentes'][:50], n_diferentes=len(conf['diferentes'])),
           'regressao_registrada': reg, 'veredito': ver, 'todos_os_pares_de_modelos': pares, 'robustez_descritiva': rob,
           'conferencia_bootstrap_por_local': boot, 'combinacoes_de_modelos_nos_locais': combos, 'contexto_nacional': ctx,
           'pistas': {'urnas_em_mais_de_uma_secao_no_2t': rep, 'troca_de_urna_entre_turnos_modelo_1t_para_2t': {f'{a}->{b}': c for (a, b), c in troca.items()},
                      'modelos_por_uf': {u: dict(c) for u, c in sorted(por_uf.items())},
                      'exterior_sem_horario_no_bweb_2t': {'secoes': len(ext_ced), 'chaves': ext_ced}}}
    with open(saida_json, 'w') as f:
        json.dump(out, f, ensure_ascii=False, indent=1)
    escrever_txt(out, saida_txt)


def escrever_txt(o, caminho):
    L = []; w = L.append
    M = o['mapa']; F = o['faixas']; A = o['aplicacao_ao_bweb']; R = o['regressao_registrada']; V = o['veredito']
    w('F4 do Adendo 20: modelo de urna no bweb inteiro')
    w('Registro: PRE-REGISTRO-2026-10-26.md, Adendo 20 (commit d976d4d). Script: scripts/analisar_F4.py.')
    w('')
    w(f"VEREDITO PELA LETRA: {V['veredito']}" + ('' if F['faixas_limpas'] else ' (faixas da amostra não são limpas)'))
    w(f"Leitura da regressão pelo critério: {V['pela_regressao']}")
    fora = [m for m, q in V['por_modelo'].items() if not q['dentro_do_sem_sinal']]
    if V['pela_regressao'] == 'INCONCLUSIVO':
        w('  Por quê: nenhum modelo chega perto do sinal (1,0 ponto a favor de Lula a mais de 4 erros-padrão), mas o "sem sinal"')
        w('  exige diferença abaixo de 0,3 e erro-padrão até 0,15 em todos, e ' + ', '.join(
            f"{m} (diferença {fz(V['por_modelo'][m]['coef'], 3)}, erro-padrão {fz(V['por_modelo'][m]['ep'], 3)})" for m in fora) + ' passam do limite.')
    w('')
    w('1. Mapa número da urna para modelo (logs da amostra do 2º turno)')
    e = M['elo_com_o_boletim']
    w(f"  Seções na pasta: {fi(e['secoes_na_pasta'])}; com log: {fi(e['secoes_com_log'])}; pacotes ilegíveis: {e['pacotes_ilegiveis']}.")
    w(f"  Urnas distintas com linha 'Identificação do Modelo de Urna': {fi(M['urnas_distintas_nos_logs'])}; conflitos (mais de um modelo para o mesmo número): {len(M['conflitos'])}.")
    w('  Urnas por modelo nos logs: ' + ', '.join(f'{k} {fi(v)}' for k, v in sorted(M['modelos'].items())))
    w(f"  Urna do boletim presente no log da seção: {fi(e['urna_do_boletim_no_log'])} de {fi(e['secoes_na_base_decodificada'])}; com linha de modelo: {fi(e['urna_do_boletim_com_linha_de_modelo'])}.")
    w('')
    w('2. Faixas (um intervalo por modelo, cortes que maximizam acertos)')
    w(f"  Acertos: {fi(F['acertos'])} de {fi(F['urnas'])} urnas.")
    for p, f in zip(F['pureza_todas_as_urnas_dos_logs'], F['faixas']):
        w(f"  {p['modelo']}: de {fi(p['faixa'][0])} a {fi(p['faixa'][1])}; urnas da amostra {fi(p['urnas_da_amostra'])}, do modelo {fi(p['do_modelo'])}"
          f" (pureza {fz(100 * p['pureza'], 2) if p['pureza'] is not None else 'n/d'}%); outros: {p['outros_modelos'] or 'nenhum'};"
          f" primeiro e último número da amostra {fi(f['primeiro_da_amostra'])} e {fi(f['ultimo_da_amostra'])}.")
    w('  Só a urna do boletim de cada seção: ' + '; '.join(f"{p['modelo']} {fz(100 * p['pureza'], 2) if p['pureza'] is not None else 'n/d'}% de {fi(p['urnas_da_amostra'])}" for p in F['pureza_so_urna_do_boletim']))
    w(f"  Faixas limpas (99% ou mais em todas): {'SIM' if F['faixas_limpas'] else 'NÃO'}.")
    fa = F['faixas_antigas_modelos_py']
    w('  Segunda leitura, faixas antigas de scripts/modelos.py: ' + '; '.join(
        f"{p['modelo']} {fi(p['faixa'][0])}-{fi(p['faixa'][1])}: {fz(100 * p['pureza'], 2) if p['pureza'] is not None else 'n/d'}% de {fi(p['urnas_da_amostra'])}" for p in fa['pureza'])
      + f"; urnas da amostra fora delas: {fa['urnas_da_amostra_fora_delas']}.")
    w('')
    w('3. Aplicação ao bweb do 2º turno')
    w(f"  Seções do bweb: {fi(A['secoes_bweb_2t'])}; sem modelo (número fora do intervalo da amostra): {fi(A['secoes_sem_modelo_fora_da_amostra'])};"
      f" na zona de corte: {fi(A['secoes_na_zona_de_corte'])}.")
    w('  Seções por modelo: ' + ', '.join(f'{k} {fi(v)}' for k, v in sorted(A['modelos_no_bweb_2t'].items())))
    w(f"  Concordância com as faixas antigas: {fz(100 * A['concordancia_faixas_novas_e_antigas'], 3)}% das seções.")
    c = o['conferencia_amostra_bweb']
    w(f"  Conferência nas seções da amostra: urna do bweb igual à do boletim em {fi(c['urna_igual_ao_boletim'])} de {fi(c['secoes'])};"
      f" modelo pela faixa igual ao do log em {fi(c['modelo_da_faixa_igual_ao_log'])} (diferentes: {c['n_diferentes']}).")
    w('')
    w('4. Regressão registrada (virada de Lula, efeito fixo de local, peso L2+R2, erro agrupado por local)')
    v = R['virada']; p = R['placebo_fatia_1t']
    w(f"  Seções: {fi(v['n'])}; locais: {fi(v['locais'])}; locais com mais de um modelo: {fi(R['locais_mistos'])}. Referência: {R['referencia']}.")
    for m in v['coef']:
        q = V['por_modelo'][m]
        w(f"  {m} contra {R['referencia']}: {fz(v['coef'][m], 3)} ponto (erro-padrão {fz(v['ep'][m], 3)}; z {fz(q['z'], 1)}); seções {fi(q['secoes'])},"
          f" em locais mistos {fi(R['secoes_por_modelo_em_locais_mistos'][m])}; locais com o modelo e a referência {fi(R['locais_com_modelo_e_referencia'][m])};"
          f" placebo (fatia do 1º turno) {fz(p['coef'][m], 3)} ({fz(p['ep'][m], 3)}).")
    w(f"  Referência {R['referencia']}: {fi(R['secoes_por_modelo'][R['referencia']])} seções, {fi(R['secoes_por_modelo_em_locais_mistos'][R['referencia']])} em locais mistos.")
    w('  Médias brutas ponderadas (sem efeito fixo, só descritivo): ' + '; '.join(
        f"{m} virada {fz(x['virada'])}, fatia de Lula 1º turno {fz(x['fatia_lula_1t'])}, 2º turno {fz(x['fatia_lula_2t'])} ({fi(x['secoes'])} seções)"
        for m, x in R['media_bruta_ponderada'].items()))
    C = o['contexto_nacional']
    w(f"  Intervalo de 95% e o que seria preciso: a margem do 2º turno no bweb é de {fi(C['lula_2t'] - C['flavio_2t'])} votos; para inverter,")
    w(f"  {fi(C['votos_para_inverter'])} votos teriam de ter passado de Flávio para Lula.")
    for m, x in C['por_modelo'].items():
        ic = x.get('ic95_contra_referencia')
        w(f"  {m}: {fi(x['votos_finalistas_2t'])} votos nos finalistas; se só este modelo respondesse pela margem, a fatia de Lula nele teria de"
          f" estar {fz(x['pontos_necessarios_so_neste_modelo'], 1)} pontos acima" + (f"; intervalo de 95% contra {R['referencia']}: {fz(ic[0], 2)} a {fz(ic[1], 2)}." if ic else ' (é a referência).'))
    B = o['conferencia_bootstrap_por_local']
    w(f"  Conferência fora do registro (bootstrap por local, {B['replicas_validas']} réplicas, semente {B['semente']}, {fi(B['locais'])} locais mistos): "
      + '; '.join(f"{m} {fz(B['coef_nos_locais_mistos'][m], 3)}, erro-padrão {fz(B['ep_bootstrap'][m], 3)}" for m in B['ep_bootstrap']) + '.')
    w('  Locais com mais de um modelo, por combinação: ' + '; '.join(f"{t} {fi(x['locais'])} ({', '.join(f'{u} {fi(n)}' for u, n in x['por_uf'].items())})"
                                                              for t, x in o['combinacoes_de_modelos_nos_locais'].items()))
    w('')
    w('5. Todos os pares de modelos (fora do veredito)')
    for ref, d_ in o['todos_os_pares_de_modelos'].items():
        w(f"  contra {ref}: " + '; '.join(f"{m} {fz(x['coef'], 3)} ({fz(x['ep'], 3)})" for m, x in d_.items()))
    w('')
    w('6. Robustez (descritiva, fora do veredito)')
    for kk, rr in o['robustez_descritiva'].items():
        vv = rr['virada']
        w(f"  {kk}: n {fi(vv['n'])}, locais {fi(vv['locais'])}; " + '; '.join(f"{m} {fz(vv['coef'][m], 3)} ({fz(vv['ep'][m], 3)})" for m in vv['coef'] if m.startswith('UE'))
          + f"; leitura pelo critério: {rr['leitura_pelo_criterio']}")
    w('')
    w('7. Pistas descritivas')
    P = o['pistas']
    w(f"  Urnas que aparecem em mais de uma seção do 2º turno no bweb: {len(P['urnas_em_mais_de_uma_secao_no_2t'])}: " +
      '; '.join(f"{u} em {len(ks)} seções ({', '.join(ks[:4])}{'...' if len(ks) > 4 else ''})" for u, ks in P['urnas_em_mais_de_uma_secao_no_2t'].items()))
    w(f"  Seções do exterior sem horário de abertura no bweb do 2º turno: {P['exterior_sem_horario_no_bweb_2t']['secoes']} (as das urnas repetidas acima estão entre elas).")
    w('  Troca de urna entre os turnos (modelo do 1º para o do 2º): ' + ', '.join(f'{k} {fi(x)}' for k, x in sorted(P['troca_de_urna_entre_turnos_modelo_1t_para_2t'].items(), key=lambda t: -t[1])))
    w('')
    w('Desvios declarados (decisões que o registro não fixa, tomadas antes de calcular a regressão): ver o docstring do script, D1 a D10.')
    txt = '\n'.join(L) + '\n'
    for ch in (chr(0x2014), chr(0x2013)):
        txt = txt.replace(ch, '-')
    with open(caminho, 'w') as f:
        f.write(txt)


if __name__ == '__main__':
    main()
