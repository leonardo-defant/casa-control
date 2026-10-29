"""T28 do pré-registro (Adendo 9): cauda de comparecimento extremo com voto concentrado, com o bweb completo.

Registro (PRE-REGISTRO-2026-10-26.md, Adendo 9, antes dos dados):
  Seções com 100 aptos ou mais, sem as especiais. Esperado por beta-binomial em torno da média do local, calibrado por
  simulação nula como no T4. Contar observados e esperados de comparecimento de 95% ou mais com fatia de Lula de 80% ou
  mais, o mesmo para Flávio, e aumento de comparecimento de 15 pontos ou mais.
  Sinal: O/E calibrado de Lula de pelo menos 1,5 vez o maior das referências (2º turno de 2022 e 1º de 2026), com excesso
  acima de 3 vezes a raiz do esperado e O/E de Flávio normal.
  Sem sinal: O/E até 1,1 vez o das referências.

Implementação (as escolhas de leitura estão em LEITURAS e são gravadas no resultado):
  Evento L: comparecimento >= 95% dos aptos e Lula >= 80% dos votos válidos da seção (no 2º turno, válidos = 13 + 22;
  no 1º turno de 2026, válidos = nominais menos o 28 cassado). Evento F: o mesmo com Flávio (22; em 2018, 17).
  Evento C (descritivo): só comparecimento >= 95%.
  Esperado por seção, como no T4 (analisar_zeros.estimar): taxa das outras seções do mesmo local (ou do município, se o
  local tiver uma seção só); superdispersão rho por método dos momentos.
    P(C >= ceil(0,95 A)) com C ~ BB(A, p_comp, rho_comp);
    P(X >= ceil(0,8 V*)) com X ~ BB(V*, p_cand, rho_cand), V* = válidos esperados na cauda de comparecimento
    (E[C | C >= 0,95 A] vezes a fração de válidos da própria seção);
    P(evento) = produto das duas (independência na nula).
  Evento D (aumento de comparecimento de 15 pontos ou mais, 2º contra 1º turno na mesma seção): C2 ~ BB(A2, p2, rho),
    p2 = comparecimento do 1º turno da seção + variação média do comparecimento das outras seções do local (ou município).
  Calibração (Adendo 6, como no T4): dados simulados sob a nula (beta-binomial em torno da taxa do local, rho verdadeiro
  ajustado em 3 passos para que o estimador nos dados simulados reproduza o rho observado), o mesmo estimador aplicado,
  R_nulo = média de 5 simulações; Rc = (O/E) / R_nulo. Esperado calibrado = E x R_nulo.
  Erro-padrão de O/E: bootstrap de locais (2.000 reamostras de Poisson), somado ao da média das simulações.

Uso: python3 -I analisar_T28.py <secoes2026.json.gz> <secoes2022.json.gz> <secoes2018.json.gz> <zips bweb 1T>
        <zips bweb 2T> <pasta locais de votação> <saida.json> <saida.txt>
"""
import os as _os, sys as _sys
_sys.path.insert(0, _os.path.dirname(_os.path.abspath(__file__)))
import collections, csv, gc, glob, io, json, math, os, sys, time, zipfile
import numpy as np
from scipy.special import gammaln
from lib import carregar, chave_local
from analisar_zeros import estimar, grupos_ids

SEMENTE = 20261026
NSIM = 5
NSIM_ROBUSTEZ = 25
NBOOT = 2000
APT_MIN = 100
P_MIN = 1e-13          # abaixo disso a probabilidade do comparecimento extremo é tratada como zero no produto
LOCAIS_ESPECIAIS = ('Preso provisório', 'Voto em trânsito')

CRITERIO = ("Seções com 100 aptos ou mais, sem as especiais. Esperado por beta-binomial em torno da média do local, "
            "calibrado por simulação nula como no T4. Contar observados e esperados de comparecimento de 95% ou mais com "
            "fatia de Lula de 80% ou mais, o mesmo para Flávio, e aumento de comparecimento de 15 pontos ou mais. "
            "Sinal: O/E calibrado de Lula de pelo menos 1,5 vez o maior das referências (2º turno de 2022 e 1º de 2026), "
            "com excesso acima de 3 vezes a raiz do esperado e O/E de Flávio normal. "
            "Sem sinal: O/E até 1,1 vez o das referências.")

LEITURAS = [
    "Seções especiais: as da definição do T15 (seções em situação especial): boletim não apurado ou anulado, "
    "comparecimento zero, boletim emitido por junta apuradora (campo NR_JUNTA_APURADORA do bweb; só existe para 2026) "
    "e seção não instalada (sem boletim). É a única definição de 'especiais' escrita no pré-registro e a única aplicável "
    "às três eleições com os arquivos locais. A leitura 'seções especiais' do TSE (presídio e voto em trânsito) só é "
    "identificável em 2026 (cadastro de locais de 2026) e vai como robustez R1, comparando 2026 com 2026.",
    "Fatia de Lula (e de Flávio): votos do candidato sobre os votos válidos da seção no turno. No 2º turno é a fatia entre "
    "os dois. No 1º turno de 2026 os válidos excluem o 28 cassado (Adendo 6). A fatia entre os dois no 1º turno vai como "
    "robustez R2.",
    "'Contar ... e aumento de comparecimento de 15 pontos ou mais' foi lido como uma terceira contagem, separada "
    "(comparecimento do 2º turno menos o do 1º na mesma seção, em pontos dos aptos). O critério de sinal só fala de Lula "
    "e Flávio, então essa contagem é relatada sem veredito próprio, com o 2º turno de 2022 como referência (o 1º turno "
    "de 2026 não tem turno anterior). As combinações aumento de 15 pontos com fatia de 80% vão como descritivo.",
    "'O/E de Flávio normal': O/E calibrado de Flávio no 2º turno de 2026 até 1,1 vez o maior das referências (a mesma "
    "faixa do 'sem sinal').",
    "'Excesso acima de 3 vezes a raiz do esperado': excesso = observados menos o esperado calibrado (E x R_nulo), como "
    "o campo excesso_Z0_vs_nulo do T4; a forma do T4 original (esperado vezes o maior das referências) vai ao lado.",
    "'O/E até 1,1 vez o das referências' (sem sinal): comparado ao maior O/E calibrado das referências, o mesmo termo de "
    "comparação do sinal.",
    "Na nula, comparecimento e fatia do candidato são independentes dentro do local; a fração de válidos do comparecimento "
    "é a da própria seção. Na simulação, os votos de Lula e de Flávio são sorteados cada um pela sua beta-binomial (o "
    "estimador de cada evento só usa os votos do próprio candidato).",
    "Evento de aumento: seções com os dois turnos, 100 aptos ou mais nos dois, nenhuma especial em nenhum dos dois; nula "
    "condicional ao comparecimento do 1º turno da própria seção (a média do local é a da variação).",
    "Referências descritivas, fora do critério: 2º turno de 2018 (Haddad e Bolsonaro) e 1º turno de 2022.",
]


# ---------------------------------------------------------------- beta-binomial

def ab(p, rho):
    p = np.clip(p, 1e-6, 1 - 1e-6); s = 1.0 / rho - 1.0
    return p * s, (1 - p) * s


def bb_cauda(m, n, a, b, media=False, linhas=20000):
    """P(X >= m) para X ~ BetaBinomial(n, a, b), seção a seção; com media=True devolve também E[X | X >= m]."""
    m = np.asarray(m, np.int64); n = np.asarray(n, np.int64)
    a = np.asarray(a, float); b = np.asarray(b, float)
    N = len(n)
    m = np.clip(m, 0, n + 1)
    J = n - m + 1
    sf = np.zeros(N); mu = np.full(N, np.nan)
    lb = gammaln(a) + gammaln(b) - gammaln(a + b)
    ordem = np.argsort(J, kind='stable')
    for s in range(0, N, linhas):
        idx = ordem[s:s + linhas]
        Jm = int(J[idx].max()) if len(idx) else 0
        if Jm <= 0:
            continue
        k = m[idx, None] + np.arange(Jm)[None, :]
        nn = n[idx, None]
        val = k <= nn
        kk = np.minimum(k, nn).astype(float); nf = nn.astype(float)
        aa = a[idx, None]; bb = b[idx, None]
        lp = (gammaln(nf + 1) - gammaln(kk + 1) - gammaln(nf - kk + 1)
              + gammaln(kk + aa) + gammaln(nf - kk + bb) - gammaln(nf + aa + bb) - lb[idx, None])
        p = np.where(val, np.exp(lp), 0.0)
        sf[idx] = p.sum(1)
        if media:
            with np.errstate(invalid='ignore', divide='ignore'):
                mu[idx] = (p * kk).sum(1) / sf[idx]
    return (sf, mu) if media else sf


def mom_rho(x, n, p, nout):
    """Superdispersão pelo método dos momentos, a mesma fórmula do T4 (analisar_zeros.calcular_arrays)."""
    p = np.clip(p, 1e-6, 1 - 1e-6); q = p * (1 - p)
    resid = (x - n * p) ** 2 - n * q - n ** 2 * q / nout
    return max(float(resid.sum() / (n * (n - 1) * q).sum()), 1e-6)


def taxa_cheia(x, n, gL, gM):
    """Taxa do local inteiro (ou do município, se o local tiver uma seção só): a média verdadeira da nula, como no T4."""
    sxL = np.bincount(gL, weights=x); snL = np.bincount(gL, weights=n); cL = np.bincount(gL)
    sxM = np.bincount(gM, weights=x); snM = np.bincount(gM, weights=n)
    with np.errstate(invalid='ignore', divide='ignore'):
        return np.where(cL[gL] >= 2, sxL[gL] / np.maximum(snL[gL], 1e-12), sxM[gM] / np.maximum(snM[gM], 1e-12))


def bb_sorteio(n, p, rho, rng):
    a, b = ab(p, rho)
    return rng.binomial(np.asarray(n, np.int64), rng.beta(a, b)).astype(np.int64)


# ---------------------------------------------------------------- eventos de nível (comparecimento e fatia)

def estimador_nivel(A, C, V, L, R, gL, gM, so_rho=False):
    """Probabilidades por seção sob a nula e eventos observados. A, C, V, L, R: inteiros."""
    Af, Cf, Vf, Lf, Rf = (x.astype(float) for x in (A, C, V, L, R))
    pc, noc, ok = estimar(Cf, Af, gL, gM)
    pl, nol, _ = estimar(Lf, Vf, gL, gM)
    pr, nor, _ = estimar(Rf, Vf, gL, gM)
    # seção cujas outras seções do local (ou município) não têm voto válido fica sem média (só ocorre em dados simulados
    # de locais do exterior com comparecimento quase nulo)
    with np.errstate(invalid='ignore'):
        ok = ok & np.isfinite(pl) & np.isfinite(pr) & (nol > 0)
    rho = {'comp': mom_rho(Cf[ok], Af[ok], pc[ok], noc[ok]),
           'L': mom_rho(Lf[ok], Vf[ok], pl[ok], nol[ok]),
           'R': mom_rho(Rf[ok], Vf[ok], pr[ok], nor[ok])}
    if so_rho:
        return {'rho': rho}
    A, C, V, L, R = A[ok], C[ok], V[ok], L[ok], R[ok]
    m_c = (95 * A + 99) // 100
    Pc, Ec = bb_cauda(m_c, A, *ab(pc[ok], rho['comp']), media=True)
    Ec = np.where(np.isfinite(Ec), Ec, m_c)
    vr = np.where(C > 0, V / np.maximum(C, 1), 0.0)
    Vs = np.maximum(np.rint(Ec * vr).astype(np.int64), 1)
    m_v = (8 * Vs + 9) // 10
    PL = np.zeros(len(A)); PR = np.zeros(len(A))
    j = Pc > P_MIN
    PL[j] = bb_cauda(m_v[j], Vs[j], *ab(pl[ok][j], rho['L']))
    PR[j] = bb_cauda(m_v[j], Vs[j], *ab(pr[ok][j], rho['R']))
    oc = 100 * C >= 95 * A
    return {'ok': ok, 'rho': rho,
            'P': {'C': Pc, 'L': Pc * PL, 'F': Pc * PR},
            'O': {'C': oc, 'L': oc & (10 * L >= 8 * V), 'F': oc & (10 * R >= 8 * V)}}


def simular_nivel(A, C, V, L, R, gL, gM, rho_v, rng):
    pc = taxa_cheia(C.astype(float), A.astype(float), gL, gM)
    pl = taxa_cheia(L.astype(float), V.astype(float), gL, gM)
    pr = taxa_cheia(R.astype(float), V.astype(float), gL, gM)
    vr = np.where(C > 0, V / np.maximum(C, 1), 0.0)
    Cs = bb_sorteio(A, pc, rho_v['comp'], rng)
    Vs = rng.binomial(Cs, np.clip(vr, 0, 1)).astype(np.int64)
    Ls = bb_sorteio(Vs, pl, rho_v['L'], rng)
    Rs = bb_sorteio(Vs, pr, rho_v['R'], rng)
    return A, Cs, Vs, Ls, Rs


# ---------------------------------------------------------------- evento de aumento do comparecimento

def estimador_aumento(A1, C1, A2, C2, V2, L2, R2, gL, gM, so_rho=False):
    A1f, C1f, A2f, C2f, V2f, L2f, R2f = (x.astype(float) for x in (A1, C1, A2, C2, V2, L2, R2))
    cL = np.bincount(gL); cM = np.bincount(gM)

    def loo(g):
        sc2 = np.bincount(g, weights=C2f); sa2 = np.bincount(g, weights=A2f)
        sc1 = np.bincount(g, weights=C1f); sa1 = np.bincount(g, weights=A1f)
        with np.errstate(invalid='ignore', divide='ignore'):
            d = (sc2[g] - C2f) / (sa2[g] - A2f) - (sc1[g] - C1f) / (sa1[g] - A1f)
        return d, sa2[g] - A2f
    dL, nL = loo(gL); dM, nM = loo(gM)
    usaL = cL[gL] >= 2; usaM = (~usaL) & (cM[gM] >= 2); ok = usaL | usaM
    d = np.where(usaL, dL, dM); nout = np.where(usaL, nL, nM)
    p2 = C1f / A1f + d
    pl, nol, _ = estimar(L2f, V2f, gL, gM)
    pr, nor, _ = estimar(R2f, V2f, gL, gM)
    with np.errstate(invalid='ignore'):
        ok = ok & np.isfinite(pl) & np.isfinite(pr) & (nol > 0) & np.isfinite(p2)
    rho = {'aum': mom_rho(C2f[ok], A2f[ok], p2[ok], nout[ok]),
           'L': mom_rho(L2f[ok], V2f[ok], pl[ok], nol[ok]),
           'R': mom_rho(R2f[ok], V2f[ok], pr[ok], nor[ok])}
    if so_rho:
        return {'rho': rho}
    A1, C1, A2, C2, V2, L2, R2 = A1[ok], C1[ok], A2[ok], C2[ok], V2[ok], L2[ok], R2[ok]
    m = (A2 * (100 * C1 + 15 * A1) + 100 * A1 - 1) // (100 * A1)
    P, Em = bb_cauda(m, A2, *ab(p2[ok], rho['aum']), media=True)
    Em = np.where(np.isfinite(Em), Em, np.minimum(m, A2))
    vr = np.where(C2 > 0, V2 / np.maximum(C2, 1), 0.0)
    Vs = np.maximum(np.rint(Em * vr).astype(np.int64), 1)
    m_v = (8 * Vs + 9) // 10
    PL = np.zeros(len(A2)); PR = np.zeros(len(A2))
    j = P > P_MIN
    PL[j] = bb_cauda(m_v[j], Vs[j], *ab(pl[ok][j], rho['L']))
    PR[j] = bb_cauda(m_v[j], Vs[j], *ab(pr[ok][j], rho['R']))
    od = 100 * A1 * C2 >= A2 * (100 * C1 + 15 * A1)
    return {'ok': ok, 'rho': rho,
            'P': {'D': P, 'DL': P * PL, 'DF': P * PR},
            'O': {'D': od, 'DL': od & (10 * L2 >= 8 * V2), 'DF': od & (10 * R2 >= 8 * V2)}}


def simular_aumento(A1, C1, A2, C2, V2, L2, R2, gL, gM, rho_v, rng):
    dfull = taxa_cheia(C2.astype(float), A2.astype(float), gL, gM) - taxa_cheia(C1.astype(float), A1.astype(float), gL, gM)
    p2 = C1 / A1 + dfull
    pl = taxa_cheia(L2.astype(float), V2.astype(float), gL, gM)
    pr = taxa_cheia(R2.astype(float), V2.astype(float), gL, gM)
    vr = np.where(C2 > 0, V2 / np.maximum(C2, 1), 0.0)
    Cs = bb_sorteio(A2, p2, rho_v['aum'], rng)
    Vs = rng.binomial(Cs, np.clip(vr, 0, 1)).astype(np.int64)
    Ls = bb_sorteio(Vs, pl, rho_v['L'], rng)
    Rs = bb_sorteio(Vs, pr, rho_v['R'], rng)
    return A1, C1, A2, Cs, Vs, Ls, Rs


# ---------------------------------------------------------------- calibração, erro-padrão e resumo

def boot_razao(O, P, g, rng, B=NBOOT):
    """Erro-padrão de sum(O)/sum(P) por bootstrap de Poisson sobre os locais."""
    Og = np.bincount(g, weights=O.astype(float)); Pg = np.bincount(g, weights=P)
    j = (Og > 0) | (Pg > 1e-15)
    Og, Pg = Og[j], Pg[j]
    rs = []
    for s in range(0, B, 100):
        W = rng.poisson(1.0, size=(min(100, B - s), len(Og)))
        rs.append((W @ Og) / (W @ Pg))
    rs = np.concatenate(rs)
    return float(np.std(rs, ddof=1))


def rodar(nome, arrays, estimador, simulador, eventos, gL_full, nsim=NSIM, semente=SEMENTE, guardar_secoes=None):
    """Estimador nos dados, ajuste do rho verdadeiro, nsim simulações nulas e resumo por evento."""
    t0 = time.time()
    rng = np.random.default_rng(semente)
    gL, gM = arrays['gL'], arrays['gM']
    dados = arrays['dados']
    obs = estimador(*dados, gL, gM)
    rho_v = dict(obs['rho'])
    for _ in range(3):
        r_sim = estimador(*simulador(*dados, gL, gM, rho_v, rng), gL, gM, so_rho=True)['rho']
        rho_v = {k: max(rho_v[k] * obs['rho'][k] / r_sim[k], 1e-6) for k in rho_v}
    nul = {e: [] for e in eventos}
    nul_O = {e: [] for e in eventos}
    for _ in range(nsim):
        s = estimador(*simulador(*dados, gL, gM, rho_v, rng), gL, gM)
        for e in eventos:
            Es = float(s['P'][e].sum()); Os = int(s['O'][e].sum())
            nul[e].append(Os / Es if Es > 0 else float('nan')); nul_O[e].append(Os)
    ok = obs['ok']
    g_ok = gL_full[ok]
    _, g_ok = np.unique(g_ok, return_inverse=True)
    rb = np.random.default_rng(semente + 1)
    out = {'secoes_com_media': int(ok.sum()), 'rho_observado': obs['rho'], 'rho_verdadeiro_ajustado': rho_v, 'eventos': {}}
    for e in eventos:
        O = int(obs['O'][e].sum()); E = float(obs['P'][e].sum())
        R = O / E if E > 0 else float('nan')
        seR = boot_razao(obs['O'][e], obs['P'][e], g_ok, rb) if E > 0 else float('nan')
        Rn = float(np.mean(nul[e])); Rn_dp = float(np.std(nul[e], ddof=1)) if nsim > 1 else float('nan')
        se_Rn = Rn_dp / math.sqrt(nsim)
        Rc = R / Rn
        se_Rc = Rc * math.sqrt((seR / R) ** 2 + (se_Rn / Rn) ** 2) if O > 0 else float('nan')
        Ecal = E * Rn
        out['eventos'][e] = {'O': O, 'E_bruto': E, 'R_bruto': R, 'R_bruto_ep_bootstrap_locais': seR,
                             'R_nulo': Rn, 'R_nulo_dp': Rn_dp, 'R_nulo_ep_media': se_Rn,
                             'R_nulo_por_simulacao': nul[e], 'O_nas_simulacoes': nul_O[e],
                             'Rc': Rc, 'Rc_ep': se_Rc, 'E_calibrado': Ecal, 'excesso_vs_calibrado': O - Ecal,
                             'z_excesso': (O - Ecal) / math.sqrt(Ecal) if Ecal > 0 else float('nan')}
    out['segundos'] = round(time.time() - t0, 1)
    if guardar_secoes:
        out['_obs'] = obs
    print(f"  {nome}: {out['secoes_com_media']} seções, {out['segundos']} s; "
          + '; '.join(f"{e} O {out['eventos'][e]['O']} E {out['eventos'][e]['E_bruto']:.1f} Rc {out['eventos'][e]['Rc']:.3f}"
                      for e in eventos), flush=True)
    return out


# ---------------------------------------------------------------- montagem das amostras

def especial(s, k, junta):
    return s.get('tipo', '').upper() != 'APURADA' or s['comp'] == 0 or k in junta


def montar_nivel(d, t, junta=frozenset(), excluir=frozenset(), dois=False):
    cont = collections.Counter(); rows = []
    for k, v in d.items():
        s = v.get(t)
        if s is None:
            continue
        cont['boletins'] += 1
        if especial(s, k, junta):
            cont['especiais'] += 1; continue
        if s['apt'] < APT_MIN:
            cont['menos_de_100_aptos'] += 1; continue
        if k in excluir:
            cont['excluidas_presidio_ou_transito'] += 1; continue
        V = s['L'] + s['R'] if dois else s['L'] + s['R'] + s['O'] - s.get('c28', 0)
        if V <= 0:
            cont['sem_voto_valido'] += 1; continue
        rows.append((k, chave_local(k, s), '|'.join(k.split('|')[:2]), s['apt'], s['comp'], V, s['L'], s['R']))
    cont['na_amostra'] = len(rows)
    gL = grupos_ids([r[1] for r in rows]); gM = grupos_ids([r[2] for r in rows])
    A, C, V, L, R = (np.array([r[i] for r in rows], np.int64) for i in range(3, 8))
    return {'chaves': [r[0] for r in rows], 'gL': gL, 'gM': gM, 'dados': (A, C, V, L, R), 'contagem': dict(cont)}


def montar_aumento(d, junta1=frozenset(), junta2=frozenset(), excluir=frozenset()):
    cont = collections.Counter(); rows = []
    for k, v in d.items():
        if '2' not in v:
            continue
        cont['boletins_2T'] += 1
        if '1' not in v:
            cont['sem_1T'] += 1; continue
        s1, s2 = v['1'], v['2']
        if especial(s1, k, junta1) or especial(s2, k, junta2):
            cont['especiais_em_algum_turno'] += 1; continue
        if s1['apt'] < APT_MIN or s2['apt'] < APT_MIN:
            cont['menos_de_100_aptos_em_algum_turno'] += 1; continue
        if k in excluir:
            cont['excluidas_presidio_ou_transito'] += 1; continue
        V2 = s2['L'] + s2['R'] + s2['O']
        if V2 <= 0:
            cont['sem_voto_valido_2T'] += 1; continue
        rows.append((k, chave_local(k, s2), '|'.join(k.split('|')[:2]), s1['apt'], s1['comp'], s2['apt'], s2['comp'],
                     V2, s2['L'], s2['R']))
    cont['na_amostra'] = len(rows)
    gL = grupos_ids([r[1] for r in rows]); gM = grupos_ids([r[2] for r in rows])
    arr = tuple(np.array([r[i] for r in rows], np.int64) for i in range(3, 10))
    return {'chaves': [r[0] for r in rows], 'gL': gL, 'gM': gM, 'dados': arr, 'contagem': dict(cont)}


def juntas_zz(pasta):
    """Seções com boletim emitido por junta apuradora (NR_JUNTA_APURADORA preenchido), lidas do zip do exterior."""
    out = set()
    for zp in glob.glob(os.path.join(pasta, 'bweb_*_ZZ_*.zip')):
        z = zipfile.ZipFile(zp)
        nome = [n for n in z.namelist() if n.lower().endswith('.csv')][0]
        rd = csv.reader(io.TextIOWrapper(z.open(nome), encoding='latin1', newline=''), delimiter=';')
        ix = {c.strip(): i for i, c in enumerate(next(rd))}
        for r in rd:
            if r[ix['CD_CARGO_PERGUNTA']] not in ('1', '-1'):
                continue
            if r[ix['NR_JUNTA_APURADORA']] not in ('-1', '', '#NULO#'):
                out.add(f"{r[ix['SG_UF']]}|{int(r[ix['CD_MUNICIPIO']])}|{int(r[ix['NR_ZONA']])}|{int(r[ix['NR_SECAO']])}")
    return out


def locais_especiais(pasta):
    """Seções (principal) em local de presídio ou de voto em trânsito, por turno, no cadastro de locais de 2026."""
    out = {'1': set(), '2': set()}; temp = {'1': set(), '2': set()}
    for f in sorted(glob.glob(os.path.join(pasta, 'eleitorado_local_votacao_2026_??.csv'))):
        with open(f, encoding='latin1') as fh:
            r = csv.reader(fh, delimiter=';'); h = next(r); i = {c: j for j, c in enumerate(h)}
            for row in r:
                t = row[i['NR_TURNO']]
                uf, m, z, sec = row[i['SG_UF']], int(row[i['CD_MUNICIPIO']]), int(row[i['NR_ZONA']]), int(row[i['NR_SECAO']])
                princ = int(row[i['NR_SECAO_PRINCIPAL']])
                pk = f'{uf}|{m}|{z}|{sec if princ in (-1, 0) or row[i["DS_TIPO_SECAO_AGREGADA"]] == "Principal" else princ}'
                if row[i['DS_TIPO_LOCAL']] in LOCAIS_ESPECIAIS:
                    out[t].add(pk)
                elif row[i['DS_TIPO_LOCAL']] == 'Temporário':
                    temp[t].add(pk)
    return out, temp


# ---------------------------------------------------------------- critério

def criterio(res, chaveL, refsL, eventoL='L', eventoF='F'):
    """Aplica o critério do registro a um conjunto de resultados."""
    a = res[chaveL]['eventos']
    refs = {r: res[r]['eventos'] for r in refsL}
    out = {}
    for e in (eventoL, eventoF):
        mx_nome = max(refs, key=lambda r: refs[r][e]['Rc'])
        mx = refs[mx_nome][e]
        razao = a[e]['Rc'] / mx['Rc']
        ep = razao * math.sqrt((a[e]['Rc_ep'] / a[e]['Rc']) ** 2 + (mx['Rc_ep'] / mx['Rc']) ** 2)
        Eref = a[e]['E_calibrado'] * mx['Rc']
        out[e] = {'Rc_2026_2T': a[e]['Rc'], 'Rc_2026_2T_ep': a[e]['Rc_ep'], 'maior_referencia': mx_nome,
                  'Rc_maior_referencia': mx['Rc'], 'Rc_maior_referencia_ep': mx['Rc_ep'],
                  'Rc_referencias': {r: refs[r][e]['Rc'] for r in refs},
                  'razao_sobre_maior_referencia': razao, 'razao_ep': ep,
                  'excesso_vs_calibrado': a[e]['excesso_vs_calibrado'], 'raiz_E_calibrado_x3': 3 * math.sqrt(a[e]['E_calibrado']),
                  'z_excesso': a[e]['z_excesso'],
                  'forma_T4_original': {'esperado_x_maior_referencia': Eref, 'excesso': a[e]['O'] - Eref,
                                        'z': (a[e]['O'] - Eref) / math.sqrt(Eref) if Eref > 0 else float('nan')}}
    L, F = out[eventoL], out[eventoF]
    flavio_normal = F['razao_sobre_maior_referencia'] <= 1.1
    exc_ok = L['excesso_vs_calibrado'] > L['raiz_E_calibrado_x3']
    if L['razao_sobre_maior_referencia'] >= 1.5 and exc_ok and flavio_normal:
        v = 'SINAL'
    elif L['razao_sobre_maior_referencia'] <= 1.1:
        v = 'SEM SINAL'
    else:
        v = 'INCONCLUSIVO'
    out['condicoes'] = {'razao_Lula_>=_1,5': L['razao_sobre_maior_referencia'] >= 1.5,
                        'excesso_Lula_>_3_raiz_E': exc_ok, 'Flavio_normal_(razao_<=_1,1)': flavio_normal,
                        'razao_Lula_<=_1,1': L['razao_sobre_maior_referencia'] <= 1.1}
    out['veredito'] = v
    return out


def por_uf(chaves, obs, Rn, eventos):
    ok = obs['ok']; ks = [k for k, o in zip(chaves, ok) if o]
    ufs = np.array([k.split('|')[0] for k in ks])
    out = {}
    for u in sorted(set(ufs)):
        j = ufs == u
        out[u] = {e: {'O': int(obs['O'][e][j].sum()), 'E_calibrado': float(obs['P'][e][j].sum() * Rn[e])} for e in eventos}
    return out


def lista_secoes(chaves, arrays, obs, Rn, e):
    ok = obs['ok']
    ks = np.array(chaves)[ok]
    A, C, V, L, R = (x[ok] for x in arrays['dados'])
    j = np.where(obs['O'][e])[0]
    return [{'secao': str(ks[i]), 'aptos': int(A[i]), 'comparecimento': int(C[i]), 'validos': int(V[i]),
             'lula': int(L[i]), 'flavio': int(R[i]), 'p_nula_calibrada': float(obs['P'][e][i] * Rn[e])} for i in j]


# ---------------------------------------------------------------- principal

def main():
    b26, b22, b18, z1, z2, pasta_locais, saida_json, saida_txt = sys.argv[1:9]
    T0 = time.time()
    out = {'teste': 'T28', 'registro': 'PRE-REGISTRO-2026-10-26.md, Adendo 9', 'criterio_registrado': CRITERIO,
           'leituras_declaradas': LEITURAS, 'parametros': {'semente': SEMENTE, 'simulacoes': NSIM, 'bootstrap': NBOOT,
                                                         'aptos_minimo': APT_MIN, 'p_min_produto': P_MIN}}
    junta1 = juntas_zz(z1); junta2 = juntas_zz(z2)
    esp_loc, temp_loc = locais_especiais(pasta_locais)
    out['juntas_2026'] = {'1T': sorted(junta1), '2T': sorted(junta2)}
    out['locais_presidio_ou_transito_2026'] = {t: len(v) for t, v in esp_loc.items()}
    print(f'juntas: 1T {len(junta1)}, 2T {len(junta2)}; seções em presídio ou trânsito: 1T {len(esp_loc["1"])}, 2T {len(esp_loc["2"])}', flush=True)

    EV = ['L', 'F', 'C']; EVD = ['D', 'DL', 'DF']
    res = {}; amostras = {}; extras = {}

    # ---- 2026
    print('lendo 2026', flush=True)
    d = carregar(b26)
    a262 = montar_nivel(d, '2', junta2); a261 = montar_nivel(d, '1', junta1)
    a26D = montar_aumento(d, junta1, junta2)
    r1_2 = montar_nivel(d, '2', junta2, esp_loc['2']); r1_1 = montar_nivel(d, '1', junta1, esp_loc['1'])
    r1_D = montar_aumento(d, junta1, junta2, esp_loc['2'] | esp_loc['1'])
    r2_1 = montar_nivel(d, '1', junta1, dois=True)
    del d; gc.collect()
    for nome, a in [('2026_2T', a262), ('2026_1T', a261), ('2026_aumento', a26D), ('R1_2026_2T', r1_2), ('R1_2026_1T', r1_1),
                    ('R1_2026_aumento', r1_D), ('R2_2026_1T_fatia_entre_os_dois', r2_1)]:
        amostras[nome] = a['contagem']
    print('2026 montado', {k: v['na_amostra'] for k, v in amostras.items()}, flush=True)
    res['2026_2T'] = rodar('2026 2T', a262, estimador_nivel, simular_nivel, EV, a262['gL'], guardar_secoes=True)
    res['2026_1T'] = rodar('2026 1T', a261, estimador_nivel, simular_nivel, EV, a261['gL'], guardar_secoes=True)
    res['2026_aumento'] = rodar('2026 aumento', a26D, estimador_aumento, simular_aumento, EVD, a26D['gL'], guardar_secoes=True)
    res['R1_2026_2T'] = rodar('R1 2026 2T', r1_2, estimador_nivel, simular_nivel, EV, r1_2['gL'])
    res['R1_2026_1T'] = rodar('R1 2026 1T', r1_1, estimador_nivel, simular_nivel, EV, r1_1['gL'])
    res['R1_2026_aumento'] = rodar('R1 2026 aumento', r1_D, estimador_aumento, simular_aumento, EVD, r1_D['gL'])
    res['R2_2026_1T_fatia_entre_os_dois'] = rodar('R2 2026 1T entre os dois', r2_1, estimador_nivel, simular_nivel, EV, r2_1['gL'])
    res['R3_2026_2T_25sim'] = rodar('R3 2026 2T 25 sim', a262, estimador_nivel, simular_nivel, EV, a262['gL'], nsim=NSIM_ROBUSTEZ, semente=SEMENTE + 7)
    res['R3_2026_1T_25sim'] = rodar('R3 2026 1T 25 sim', a261, estimador_nivel, simular_nivel, EV, a261['gL'], nsim=NSIM_ROBUSTEZ, semente=SEMENTE + 7)

    # descritivos de 2026: por UF, lista das seções, escala em votos, locais temporários
    Rn = {e: res['2026_2T']['eventos'][e]['R_nulo'] for e in EV}
    extras['por_uf_2026_2T'] = por_uf(a262['chaves'], res['2026_2T']['_obs'], Rn, ['L', 'F'])
    Rn1 = {e: res['2026_1T']['eventos'][e]['R_nulo'] for e in EV}
    extras['por_uf_2026_1T'] = por_uf(a261['chaves'], res['2026_1T']['_obs'], Rn1, ['L', 'F'])
    secL = lista_secoes(a262['chaves'], a262, res['2026_2T']['_obs'], Rn, 'L')
    secF = lista_secoes(a262['chaves'], a262, res['2026_2T']['_obs'], Rn, 'F')
    extras['secoes_evento_L_2026_2T'] = secL
    extras['secoes_evento_F_2026_2T'] = secF
    esc = {}
    for nome, lst in (('L', secL), ('F', secF)):
        esc[nome] = {'secoes': len(lst), 'comparecimento': sum(x['comparecimento'] for x in lst),
                     'votos_lula': sum(x['lula'] for x in lst), 'votos_flavio': sum(x['flavio'] for x in lst),
                     'margem_lula_menos_flavio': sum(x['lula'] - x['flavio'] for x in lst),
                     'em_presidio_ou_transito': sum(x['secao'] in esp_loc['2'] for x in lst),
                     'em_local_temporario': sum(x['secao'] in temp_loc['2'] for x in lst)}
    extras['escala_2026_2T'] = esc
    # seções do evento L no 2º turno: estavam no evento L no 1º turno?
    obs1 = res['2026_1T']['_obs']; k1 = set(np.array(a261['chaves'])[obs1['ok']][obs1['O']['L']].tolist())
    extras['evento_L_2T_tambem_no_1T'] = sum(x['secao'] in k1 for x in secL)
    # aumento: lista curta
    oD = res['2026_aumento']['_obs']; ksD = np.array(a26D['chaves'])[oD['ok']]
    extras['secoes_evento_DL_2026'] = ksD[oD['O']['DL']].tolist()
    extras['secoes_evento_DF_2026'] = ksD[oD['O']['DF']].tolist()
    extras['por_uf_2026_aumento'] = por_uf(a26D['chaves'], oD, {e: res['2026_aumento']['eventos'][e]['R_nulo'] for e in EVD}, ['D'])
    for r in ('2026_2T', '2026_1T', '2026_aumento'):
        res[r].pop('_obs', None)
    del a262, a261, a26D, r1_2, r1_1, r1_D, r2_1; gc.collect()

    # ---- 2022
    print('lendo 2022', flush=True)
    d = carregar(b22)
    a222 = montar_nivel(d, '2'); a221 = montar_nivel(d, '1'); a22D = montar_aumento(d)
    r2_221 = montar_nivel(d, '1', dois=True)
    del d; gc.collect()
    for nome, a in [('2022_2T', a222), ('2022_1T', a221), ('2022_aumento', a22D), ('R2_2022_1T_fatia_entre_os_dois', r2_221)]:
        amostras[nome] = a['contagem']
    res['2022_2T'] = rodar('2022 2T', a222, estimador_nivel, simular_nivel, EV, a222['gL'], guardar_secoes=True)
    res['2022_1T'] = rodar('2022 1T', a221, estimador_nivel, simular_nivel, EV, a221['gL'])
    res['2022_aumento'] = rodar('2022 aumento', a22D, estimador_aumento, simular_aumento, EVD, a22D['gL'])
    res['R2_2022_1T_fatia_entre_os_dois'] = rodar('R2 2022 1T entre os dois', r2_221, estimador_nivel, simular_nivel, EV, r2_221['gL'])
    res['R3_2022_2T_25sim'] = rodar('R3 2022 2T 25 sim', a222, estimador_nivel, simular_nivel, EV, a222['gL'], nsim=NSIM_ROBUSTEZ, semente=SEMENTE + 7)
    Rn22 = {e: res['2022_2T']['eventos'][e]['R_nulo'] for e in EV}
    extras['por_uf_2022_2T'] = por_uf(a222['chaves'], res['2022_2T']['_obs'], Rn22, ['L', 'F'])
    res['2022_2T'].pop('_obs', None)
    del a222, a221, a22D, r2_221; gc.collect()

    # ---- 2018 (descritivo)
    print('lendo 2018', flush=True)
    d = carregar(b18)
    a182 = montar_nivel(d, '2'); a18D = montar_aumento(d)
    del d; gc.collect()
    amostras['2018_2T'] = a182['contagem']; amostras['2018_aumento'] = a18D['contagem']
    res['2018_2T'] = rodar('2018 2T', a182, estimador_nivel, simular_nivel, EV, a182['gL'])
    res['2018_aumento'] = rodar('2018 aumento', a18D, estimador_aumento, simular_aumento, EVD, a18D['gL'])
    del a182, a18D; gc.collect()

    # ---- critério e robustez
    crit = criterio(res, '2026_2T', ['2022_2T', '2026_1T'])
    rob = {
        'R1_presidio_e_transito_fora_(so_2026)': criterio(res, 'R1_2026_2T', ['R1_2026_1T']),
        'R1b_principal_contra_so_2026_1T': criterio(res, '2026_2T', ['2026_1T']),
        'R2_fatia_entre_os_dois_no_1T': criterio(res, '2026_2T', ['2022_2T', 'R2_2026_1T_fatia_entre_os_dois']),
        'R3_25_simulacoes': criterio(res, 'R3_2026_2T_25sim', ['R3_2022_2T_25sim', 'R3_2026_1T_25sim']),
        'D_todas_as_referencias_descritivo': criterio(res, '2026_2T', ['2022_2T', '2026_1T', '2018_2T', '2022_1T']),
    }
    aum = {}
    for e in EVD:
        a = res['2026_aumento']['eventos'][e]; r22 = res['2022_aumento']['eventos'][e]; r18 = res['2018_aumento']['eventos'][e]
        aum[e] = {'Rc_2026': a['Rc'], 'Rc_2026_ep': a['Rc_ep'], 'Rc_2022': r22['Rc'], 'Rc_2022_ep': r22['Rc_ep'],
                  'Rc_2018_descritivo': r18['Rc'], 'razao_2026_sobre_2022': a['Rc'] / r22['Rc'] if r22['Rc'] > 0 else float('nan'),
                  'O_2026': a['O'], 'E_calibrado_2026': a['E_calibrado'], 'O_2022': r22['O'], 'E_calibrado_2022': r22['E_calibrado']}
    out.update({'amostras': amostras, 'resultados': res, 'criterio': crit, 'robustez': rob, 'aumento_de_comparecimento': aum,
                'descritivo': extras, 'veredito': crit['veredito'], 'segundos_total': round(time.time() - T0, 1)})
    with open(saida_json, 'w') as f:
        json.dump(out, f, ensure_ascii=False, indent=1, default=lambda x: x.tolist() if hasattr(x, 'tolist') else str(x))
    escrever_txt(out, saida_txt)
    print('veredito', crit['veredito'], 'em', out['segundos_total'], 's')


# ---------------------------------------------------------------- texto

def br(x, nd=0):
    s = f'{x:,.{nd}f}'
    return s.replace(',', 'X').replace('.', ',').replace('X', '.')


def escrever_txt(o, caminho):
    T = []; A = T.append
    res = o['resultados']; c = o['criterio']
    A('T28. Cauda de comparecimento extremo com voto concentrado, com o bweb completo do 2º turno de 2026 (Adendo 9)')
    A('Script: scripts/analisar_T28.py. Números completos: resultados/T28_bweb.json.')
    A('')
    A('Critério registrado (PRE-REGISTRO-2026-10-26.md, Adendo 9, antes dos dados):')
    A('- Seções com 100 aptos ou mais, sem as especiais. Esperado por beta-binomial em torno da média do local, calibrado por')
    A('  simulação nula como no T4. Contar observados e esperados de comparecimento de 95% ou mais com fatia de Lula de 80% ou')
    A('  mais, o mesmo para Flávio, e aumento de comparecimento de 15 pontos ou mais.')
    A('- Sinal: O/E calibrado de Lula de pelo menos 1,5 vez o maior das referências (2º turno de 2022 e 1º de 2026), com excesso')
    A('  acima de 3 vezes a raiz do esperado e O/E de Flávio normal.')
    A('- Sem sinal: O/E até 1,1 vez o das referências.')
    A('')
    A(f"VEREDITO PELA LETRA: {o['veredito']}")
    A('')
    L, F = c['L'], c['F']
    A('Resumo')
    A(f"- Lula (comparecimento >= 95% e Lula >= 80% dos válidos): O/E calibrado no 2º turno de 2026 = {L['Rc_2026_2T']:.3f} (ep {L['Rc_2026_2T_ep']:.3f});")
    A(f"  referências: 2º turno de 2022 {L['Rc_referencias']['2022_2T']:.3f}, 1º turno de 2026 {L['Rc_referencias']['2026_1T']:.3f}; maior = {L['maior_referencia']} "
      f"({L['Rc_maior_referencia']:.3f}, ep {L['Rc_maior_referencia_ep']:.3f}).")
    A(f"  Razão 2026 sobre a maior referência: {L['razao_sobre_maior_referencia']:.3f} (ep {L['razao_ep']:.3f}). Limiar de sinal 1,5; de sem sinal 1,1.")
    A(f"- Flávio (o mesmo com Flávio >= 80%): O/E calibrado {F['Rc_2026_2T']:.3f} (ep {F['Rc_2026_2T_ep']:.3f}); referências 2022 {F['Rc_referencias']['2022_2T']:.3f}, "
      f"2026 1T {F['Rc_referencias']['2026_1T']:.3f}; razão {F['razao_sobre_maior_referencia']:.3f} (ep {F['razao_ep']:.3f}).")
    e = res['2026_2T']['eventos']['L']
    A(f"- Excesso de Lula sobre o esperado calibrado: {e['O']} observadas contra {e['E_calibrado']:.1f} esperadas, excesso {e['excesso_vs_calibrado']:+.1f}, "
      f"3 x raiz do esperado = {L['raiz_E_calibrado_x3']:.1f} (z {e['z_excesso']:+.1f}).")
    cd = c['condicoes']
    A(f"- Condições: razão de Lula >= 1,5: {'sim' if cd['razao_Lula_>=_1,5'] else 'não'}; excesso > 3 raiz(E): {'sim' if cd['excesso_Lula_>_3_raiz_E'] else 'não'}; "
      f"Flávio normal (razão <= 1,1): {'sim' if cd['Flavio_normal_(razao_<=_1,1)'] else 'não'}; razão de Lula <= 1,1: {'sim' if cd['razao_Lula_<=_1,1'] else 'não'}.")
    esc = o['descritivo']['escala_2026_2T']
    A(f"- Escala: as {esc['L']['secoes']} seções do evento de Lula no 2º turno somam {br(esc['L']['comparecimento'])} votantes e margem de Lula sobre Flávio de "
      f"{br(esc['L']['margem_lula_menos_flavio'])} votos; as {esc['F']['secoes']} de Flávio, margem de Flávio de {br(-esc['F']['margem_lula_menos_flavio'])}. "
      f"A virada exigiria 2,22 milhões (troca) ou 4,43 milhões (acréscimo).")
    A('')
    A('1. Leituras declaradas (pontos em que o registro é ambíguo; marcadas como desvio do registro)')
    for i, x in enumerate(o['leituras_declaradas'], 1):
        A(f'  {i}. {x}')
    A('')
    A('2. Amostras')
    for k, v in o['amostras'].items():
        A(f'  {k}: ' + ', '.join(f'{a} {br(b)}' for a, b in v.items()))
    A(f"  Juntas apuradoras (só exterior): 1º turno {len(o['juntas_2026']['1T'])}, 2º turno {len(o['juntas_2026']['2T'])} seções. "
      f"Seções em presídio ou voto em trânsito no cadastro de 2026: 1º turno {o['locais_presidio_ou_transito_2026']['1']}, 2º turno {o['locais_presidio_ou_transito_2026']['2']}.")
    A('')
    A('3. Resultados por eleição e turno (O = observadas; E = esperado bruto; R = O/E; R_nulo = O/E médio nas simulações nulas; Rc = R/R_nulo)')
    nomes = {'L': 'esquerda>=80%', 'F': 'direita>=80%', 'C': 'só comparecimento', 'D': 'aumento>=15', 'DL': 'aumento e esq>=80%', 'DF': 'aumento e dir>=80%'}
    A(f"  {'conjunto':38s} {'evento':20s} {'O':>6s} {'E':>9s} {'R':>7s} {'ep':>6s} {'R_nulo':>7s} {'dp':>6s} {'Rc':>7s} {'ep':>6s} {'E cal':>8s}")
    for k, r in res.items():
        for ev, x in r['eventos'].items():
            A(f"  {k:38s} {nomes[ev]:20s} {x['O']:6d} {x['E_bruto']:9.1f} {x['R_bruto']:7.3f} {x['R_bruto_ep_bootstrap_locais']:6.3f} "
              f"{x['R_nulo']:7.3f} {x['R_nulo_dp']:6.3f} {x['Rc']:7.3f} {x['Rc_ep']:6.3f} {x['E_calibrado']:8.1f}")
        A(f"  {'':38s} rho observado " + ', '.join(f'{a} {b:.5f}' for a, b in r['rho_observado'].items())
          + '; ajustado ' + ', '.join(f'{a} {b:.5f}' for a, b in r['rho_verdadeiro_ajustado'].items()))
    A('  Em 2018, esquerda = Haddad (13), direita = Bolsonaro (17); em 2022, Lula (13) e Bolsonaro (22); em 2026, Lula (13) e Flávio (22).')
    A('')
    A('4. Critério (principal)')
    for ev in ('L', 'F'):
        x = c[ev]
        A(f"  {'Lula' if ev == 'L' else 'Flávio'}: Rc 2026 2T {x['Rc_2026_2T']:.3f} ({x['Rc_2026_2T_ep']:.3f}); maior referência {x['maior_referencia']} {x['Rc_maior_referencia']:.3f} "
          f"({x['Rc_maior_referencia_ep']:.3f}); razão {x['razao_sobre_maior_referencia']:.3f} ({x['razao_ep']:.3f}); excesso {x['excesso_vs_calibrado']:+.1f} contra 3 raiz(E) "
          f"{x['raiz_E_calibrado_x3']:.1f}; forma do T4 original: esperado x maior referência {x['forma_T4_original']['esperado_x_maior_referencia']:.1f}, "
          f"excesso {x['forma_T4_original']['excesso']:+.1f} (z {x['forma_T4_original']['z']:+.2f})")
    A(f"  Veredito: {c['veredito']}")
    A('')
    A('5. Robustez (relatada ao lado, sem substituir o critério)')
    for k, x in o['robustez'].items():
        A(f"  {k}: Lula razão {x['L']['razao_sobre_maior_referencia']:.3f} (ep {x['L']['razao_ep']:.3f}; Rc {x['L']['Rc_2026_2T']:.3f} contra {x['L']['maior_referencia']} "
          f"{x['L']['Rc_maior_referencia']:.3f}); Flávio razão {x['F']['razao_sobre_maior_referencia']:.3f} (ep {x['F']['razao_ep']:.3f}); veredito pela mesma regra: {x['veredito']}")
    A('')
    A('6. Aumento de comparecimento de 15 pontos ou mais (2º contra 1º turno na mesma seção; sem critério próprio de sinal)')
    for ev, x in o['aumento_de_comparecimento'].items():
        A(f"  {nomes[ev]:20s}: 2026 O {x['O_2026']} E cal {x['E_calibrado_2026']:.1f} Rc {x['Rc_2026']:.3f} ({x['Rc_2026_ep']:.3f}); "
          f"2022 O {x['O_2022']} E cal {x['E_calibrado_2022']:.1f} Rc {x['Rc_2022']:.3f} ({x['Rc_2022_ep']:.3f}); razão 2026/2022 {x['razao_2026_sobre_2022']:.3f}; "
          f"2018 (descritivo) Rc {x['Rc_2018_descritivo']:.3f}")
    A('')
    A('7. Descritivo')
    ex = o['descritivo']
    A(f"  Evento de Lula no 2º turno de 2026: {esc['L']['secoes']} seções; {esc['L']['em_presidio_ou_transito']} em presídio ou trânsito; "
      f"{esc['L']['em_local_temporario']} em local temporário; {ex['evento_L_2T_tambem_no_1T']} também estavam no evento de Lula no 1º turno.")
    A(f"  Votos nessas seções: Lula {br(esc['L']['votos_lula'])}, Flávio {br(esc['L']['votos_flavio'])}, comparecimento {br(esc['L']['comparecimento'])}.")
    A(f"  Evento de Flávio no 2º turno de 2026: {esc['F']['secoes']} seções; Flávio {br(esc['F']['votos_flavio'])}, Lula {br(esc['F']['votos_lula'])}.")
    A('  Por UF, evento de Lula (O / esperado calibrado): 2026 2T | 2026 1T | 2022 2T')
    u26, u261, u22 = ex['por_uf_2026_2T'], ex['por_uf_2026_1T'], ex['por_uf_2022_2T']
    for u in sorted(set(u26) | set(u22)):
        g = lambda dd: f"{dd[u]['L']['O']:4d} / {dd[u]['L']['E_calibrado']:6.1f}" if u in dd else '   - /    -  '
        A(f"    {u}: {g(u26)} | {g(u261)} | {g(u22)}")
    A('  Por UF, evento de Flávio (O / esperado calibrado): 2026 2T | 2026 1T | 2022 2T')
    for u in sorted(set(u26) | set(u22)):
        g = lambda dd: f"{dd[u]['F']['O']:4d} / {dd[u]['F']['E_calibrado']:6.1f}" if u in dd else '   - /    -  '
        if any(u in dd and (dd[u]['F']['O'] or dd[u]['F']['E_calibrado'] >= 0.5) for dd in (u26, u261, u22)):
            A(f"    {u}: {g(u26)} | {g(u261)} | {g(u22)}")
    A(f"  Seções do evento aumento e Lula >= 80% (2026): {len(ex['secoes_evento_DL_2026'])}; aumento e Flávio >= 80%: {len(ex['secoes_evento_DF_2026'])}.")
    A('  A lista das seções de cada evento, com a probabilidade calibrada sob a nula, está no JSON (serve ao T27).')
    A('')
    A('8. Limites')
    A('- O teste só vê enchimento ou troca concentrada em poucas seções (comparecimento perto de 100% e voto quase todo num lado).')
    A('  Uma troca espalhada de poucos votos por seção não muda essa cauda.')
    A('- A nula trata comparecimento e fatia como independentes dentro do local e todas as seções do local com a mesma média;')
    A('  o que não for capturado por isso aparece também nas referências, e por isso a comparação é contra elas.')
    A('- O cadastro de locais de 2022 não está nos arquivos locais: presídios e voto em trânsito não podem ser retirados em 2022.')
    A(f"\nRodado em {time.strftime('%d/%m/%Y %H:%M', time.gmtime())} UTC, {o['segundos_total']} s.")
    with open(caminho, 'w') as f:
        f.write('\n'.join(T) + '\n')


if __name__ == '__main__':
    main()
