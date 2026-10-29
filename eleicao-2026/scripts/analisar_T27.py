"""T27 do pré-registro (Adendo 9): teto somado dos vetores medidos, com o bweb completo do 2º turno de 2026.

Registro (PRE-REGISTRO-2026-10-26.md, Adendo 9, antes dos dados):
  "Por seção, o excesso de cada vetor sobre a maior taxa de 2018, 2022 e do 1º turno de 2026, em votos (T21, votos depois
  das 17h, T15, T7, T28, T17, T23). Cada voto entra uma vez, no vetor de maior valor da seção. Somar e comparar com 2,22
  milhões (troca) e 4,43 milhões (acréscimo). Sem sinal: soma até 0,5 milhão. Sinal: 2,2 milhões ou mais. Entre os dois:
  inconclusivo. Chegar perto não prova fraude."

Leituras (fixadas neste arquivo antes de rodar; cada uma sai no resultado e as que o registro não fixa são desvio declarado):
  L1. "Taxa" de um vetor numa eleição = total do vetor dividido pelo total da sua base, com a regra do teste que o mediu.
      "A maior" = o máximo entre as referências que têm o dado. Excesso da seção = quantidade do vetor na seção no 2º turno
      de 2026 menos essa taxa vezes a base da seção, em votos (a forma do T4: observados menos esperados vezes a maior
      referência). A taxa da própria seção em cada referência sai como robustez (R1, só onde existe: T21).
  L2. A seção entra com max(0, maior excesso entre os vetores): um déficit não compensa o excesso de outra seção (leitura de
      teto) e cada voto entra uma vez, no vetor de maior valor da seção. A soma líquida de cada vetor sai ao lado.
  L3. Vetores e quantidades por seção (votos):
      T21: q = NH2 - NH1 (liberações sem biometria de quem tem biometria cadastrada, campo QT_ELEI_BIOM_SEM_HABILITACAO,
           a mais no 2º turno); base = C2 - C1; taxa = NH/comparecimento (a "proporção" do T21). Só as 27 UFs (no exterior o
           campo é zero nos dois turnos).
      T15: q = max(0, C2 - A1) (votantes do 2º turno acima dos aptos da seção no 1º turno; inclui o comparecimento acima dos
           aptos do 2º turno, que é zero) + saldo positivo das seções especiais (votos tirados de Flávio; o de 2026 é -2, a
           favor de Flávio, e entra como zero); base = C2; taxa nas referências pela mesma conta entre os turnos.
      T7:  q = max(0, ganho - bolo) do candidato que mais ganhou (a conta do T7); base = max(0, ganho); taxa = soma de q
           sobre soma da base (2018 Haddad, 2022 Bolsonaro).
      T28: evento L (comparecimento >= 95% e Lula >= 80% dos válidos): q = votos de Lula na seção do evento; esperado =
           Rc da maior referência vezes a probabilidade calibrada da seção sob a nula (P x R_nulo do T28). Evento D (aumento
           de comparecimento de 15 pontos ou mais): q = C2 - C1 na seção do evento, esperado pela mesma regra com o Rc do
           evento D das referências. O valor do T28 na seção é o maior dos dois.
      T23: q = efeito encolhido da zona (BLUP do T23, pontos/100) vezes os votos nos finalistas da seção, nas zonas extremas
           a favor do 13 (a medida em votos do próprio T23); base = votos nos finalistas; taxa nas referências pela mesma conta.
  L4. Referências: 2018, 2022 e 1º turno de 2026 onde o vetor existe. O 1º turno de 2026 não tem turno anterior, então não
      define taxa para T7, T15 (aptos entre turnos), T23 e evento D; para T15 o comparecimento acima dos aptos do 1º turno
      de 2026 é zero. T21: as bases de 2018 e 2022 não têm o campo de biometria (falta QT_ELEITORES_BIOMETRIA_NH do bweb
      de 2018 e 2022, que não está nos arquivos locais); só o 1º turno de 2026 dá a taxa.
  L5. Fora da soma, por falta de dado por seção na base completa: T17 (atributo da máquina: o teste só existe na amostra e na
      extensão dos Adendos 10 e 11) e votos depois das 17h (só os logs da amostra registram a hora de cada voto; o bweb
      traz só a hora de encerramento da seção).
  Erro-padrão da soma: bootstrap de Poisson dos locais de votação, calculado na forma fechada (variância = soma dos
  quadrados das somas por local), com as taxas de referência fixas.

Uso: python3 -I analisar_T27.py <secoes2026.json.gz> <secoes2022.json.gz> <secoes2018.json.gz> <candidatos2026_1t.json.gz>
        <nh_secoes_2026.json.gz> <pasta zips bweb 1T> <pasta zips bweb 2T> <resultados/> <saida.json> <saida.txt>
        [<tabela por seção .tsv.gz>]
"""
import os as _os, sys as _sys
_sys.path.insert(0, _os.path.dirname(_os.path.abspath(__file__)))
import collections, gc, gzip, json, math, sys, time
import numpy as np
from lib import carregar, chave_local
import analisar_T23 as T23
import analisar_T28 as T28

SEM_SINAL, SINAL = 500_000, 2_200_000
TROCA, ACRESCIMO = 2_220_000, 4_430_000
VETORES = ['T21', 'T15', 'T7', 'T28', 'T23']

CRITERIO = ("Por seção, o excesso de cada vetor sobre a maior taxa de 2018, 2022 e do 1º turno de 2026, em votos (T21, "
            "votos depois das 17h, T15, T7, T28, T17, T23). Cada voto entra uma vez, no vetor de maior valor da seção. "
            "Somar e comparar com 2,22 milhões (troca) e 4,43 milhões (acréscimo). Sem sinal: soma até 0,5 milhão. "
            "Sinal: 2,2 milhões ou mais. Entre os dois: inconclusivo. Chegar perto não prova fraude.")


def log(*a):
    print(time.strftime('%H:%M:%S'), *a, flush=True)


# cache simples para o analisar_T23.montar não ler de novo a base já carregada
_CACHE = {}


def carregar_cache(c):
    if c not in _CACHE:
        _CACHE[c] = carregar(c)
    return _CACHE[c]


def limpar_cache():
    _CACHE.clear(); gc.collect()


T23.carregar = carregar_cache


# ---------------------------------------------------------------------------------------------- vetores por seção
def t7_t15(d, c):
    """T7 (candidato c) e T15 por seção com os dois turnos. Devolve chaves e arrays."""
    K, X, G, Q15, C2, A1, A2, C1, A1b = [], [], [], [], [], [], [], [], []
    acima_2t = acima_1t = 0
    for k, v in d.items():
        if '1' in v and v['1']['comp'] > v['1']['apt']:
            acima_1t += 1
        if '2' in v and v['2']['comp'] > v['2']['apt']:
            acima_2t += 1
        if '1' not in v or '2' not in v:
            continue
        a, b = v['1'], v['2']
        g = b[c] - a[c]
        bolo = a['O'] + max(0, (a['B'] + a['N']) - (b['B'] + b['N'])) + max(0, b['comp'] - a['comp'])
        K.append(k); G.append(g); X.append(max(0, g - bolo))
        Q15.append(max(0, b['comp'] - a['apt']) + max(0, b['comp'] - b['apt']))
        C2.append(b['comp']); C1.append(a['comp']); A1.append(a['apt']); A2.append(b['apt'])
    f = lambda z: np.array(z, float)
    return {'chaves': K, 'x7': f(X), 'g7': f(G), 'q15': f(Q15), 'C2': f(C2), 'C1': f(C1), 'A1': f(A1), 'A2': f(A2),
            'acima_aptos_2T': acima_2t, 'acima_aptos_1T': acima_1t}


def zonas(B, X):
    """Efeito encolhido de cada zona (a mesma conta de analisar_T23.zonas_extremas), levado às seções."""
    r, _ = T23.residuos(B['y'], X, B['uf'])
    E, zon, loc = T23.estat_mun(r, B['v2'], B)
    comp = {k: float(v[0]) for k, v in T23.estimar(E, np.ones(len(E['N']))).items()}
    sZ, sL, sS = comp['zona'], comp['local'], max(comp['secao'], 0.0)
    multi = E['NZ'][zon['z2m']] >= 2
    media_m = E['S'] / E['N']
    dz = zon['S'] / zon['n'] - media_m[zon['z2m']]
    tau2 = max(sL, 0.0) * zon['A'] / zon['n'] ** 2 + (sS * zon['n'] + zon['V']) / zon['n'] ** 2
    lam = np.zeros_like(dz) if sZ <= 0 else sZ / (sZ + tau2)
    ef = np.where(multi, lam * dz, 0.0)
    lim = 2 * math.sqrt(sZ) if sZ > 0 else math.inf
    pos = multi & (ef > lim)
    gz = B['gz']; n2 = B['n2']
    q_ext = np.where(pos[gz], ef[gz] / 100 * n2, 0.0)
    q_pos = np.where(multi[gz] & (ef[gz] > 0), ef[gz] / 100 * n2, 0.0)
    return {'sec': list(B['sec']), 'n2': n2, 'q_ext': q_ext, 'q_pos': q_pos, 'sigma2_zona': sZ, 'limiar_pontos': lim,
            'zonas_extremas_a_favor': int(pos.sum()), 'votos_ext': float(q_ext.sum()), 'votos_pos': float(q_pos.sum()),
            'votos_finalistas': float(n2.sum())}


def referencia(ano, caminho, c):
    log('referência', ano)
    d = carregar_cache(caminho)
    t = t7_t15(d, c)
    B = T23.montar(caminho)
    z = zonas(B, B['XA'])
    del B
    limpar_cache(); del d; gc.collect()
    g = t['g7']; x = t['x7']
    out = {'T7': {'excesso_total': float(x.sum()), 'ganho_total': float(g.sum()), 'ganho_positivo_total': float(np.maximum(g, 0).sum()),
                  'taxa_sobre_ganho_positivo': float(x.sum() / np.maximum(g, 0).sum()),
                  'taxa_registrada_b_sobre_ganho_liquido': float(x.sum() / g.sum())},
           'T15': {'q_total': float(t['q15'].sum()), 'comparecimento_2T': float(t['C2'].sum()),
                   'taxa': float(t['q15'].sum() / t['C2'].sum()), 'secoes_com_q': int((t['q15'] > 0).sum()),
                   'secoes_comparecimento_acima_dos_aptos_2T': t['acima_aptos_2T'],
                   'secoes_comparecimento_acima_dos_aptos_1T': t['acima_aptos_1T']},
           'T23': {'sigma2_zona': z['sigma2_zona'], 'limiar_pontos': z['limiar_pontos'],
                   'zonas_extremas_a_favor_do_13': z['zonas_extremas_a_favor'],
                   'votos_zonas_extremas_a_favor_do_13': z['votos_ext'], 'votos_zonas_positivas_do_13': z['votos_pos'],
                   'votos_finalistas_2T': z['votos_finalistas'],
                   'taxa_extremas': z['votos_ext'] / z['votos_finalistas'], 'taxa_positivas': z['votos_pos'] / z['votos_finalistas']},
           'secoes_com_os_dois_turnos': len(t['chaves'])}
    return out


# ---------------------------------------------------------------------------------------------- principal
def main():
    (b26, b22, b18, cand26, nh, z1, z2, pres, saida_json, saida_txt) = sys.argv[1:11]
    tabela = sys.argv[11] if len(sys.argv) > 11 else None
    T0 = time.time()
    J = lambda n: json.load(open(_os.path.join(pres, n)))
    r28 = J('T28_bweb.json'); r23 = J('T23_bweb.json'); r7 = J('T7_T14_bweb.json'); r15 = J('T15_bweb.json'); r21 = J('T21_bweb.json')

    out = {'teste': 'T27', 'registro': 'PRE-REGISTRO-2026-10-26.md, Adendo 9', 'criterio_registrado': CRITERIO,
           'leituras': __doc__.split('Leituras')[1].split('Uso:')[0].strip(), 'conferencias': {}}

    # ---------------- referências (2018 e 2022), gravadas antes de ler 2026
    refs = {'2018': referencia('2018', b18, 'L'), '2022': referencia('2022', b22, 'R')}
    out['referencias'] = refs
    # conferência com os resultados já registrados
    c7 = {a: (refs[a]['T7']['excesso_total'], r7['referencias'][a]['T7_ganhador']['excesso_total'],
              refs[a]['T7']['ganho_total'], r7['referencias'][a]['T7_ganhador']['ganho_total']) for a in refs}
    c23 = {a: (refs[a]['T23']['votos_zonas_extremas_a_favor_do_13'],
               r23['referencias'][a]['zonas_extremas']['votos_somados_a_favor_de_lula']) for a in refs}
    out['conferencias']['T7_referencias_iguais_ao_T7'] = all(abs(v[0] - v[1]) < 1e-6 and abs(v[2] - v[3]) < 1e-6 for v in c7.values())
    out['conferencias']['T23_referencias_iguais_ao_T23'] = all(abs(v[0] - v[1]) < 1e-6 * max(1, abs(v[1])) for v in c23.values())
    out['conferencias']['T23_valores'] = c23
    log('conferências das referências', out['conferencias'])

    # taxas máximas
    tx = {}
    tx['T7'] = max((refs[a]['T7']['taxa_sobre_ganho_positivo'], a) for a in refs)
    tx['T15'] = max([(refs[a]['T15']['taxa'], a) for a in refs] + [(0.0, '2026_1T')])
    tx['T23'] = max((refs[a]['T23']['taxa_extremas'], a) for a in refs)
    tx['T23_positivas'] = max((refs[a]['T23']['taxa_positivas'], a) for a in refs)
    RcL = {'2022_2T': r28['resultados']['2022_2T']['eventos']['L']['Rc'], '2026_1T': r28['resultados']['2026_1T']['eventos']['L']['Rc'],
           '2018_2T': r28['resultados']['2018_2T']['eventos']['L']['Rc']}
    RcL_ep = {'2022_2T': r28['resultados']['2022_2T']['eventos']['L']['Rc_ep'], '2026_1T': r28['resultados']['2026_1T']['eventos']['L']['Rc_ep'],
              '2018_2T': r28['resultados']['2018_2T']['eventos']['L']['Rc_ep']}
    RcD = {'2022': r28['aumento_de_comparecimento']['D']['Rc_2022'], '2018': r28['aumento_de_comparecimento']['D']['Rc_2018_descritivo']}
    tx['T28_L'] = max((v, k) for k, v in RcL.items())
    tx['T28_D'] = max((v, k) for k, v in RcD.items())

    # ---------------- 2026
    log('lendo 2026')
    d = carregar_cache(b26)
    mestre = [k for k, v in d.items() if '2' in v]
    idx = {k: i for i, k in enumerate(mestre)}
    N = len(mestre)
    uf = np.array([k.split('|')[0] for k in mestre])
    loc_ids = np.unique(np.array([chave_local(k, d[k]['2']) for k in mestre]), return_inverse=True)[1]
    VAL = {v: np.full(N, -np.inf) for v in VETORES}
    EXTRA = {}

    # T7 e T15
    t = t7_t15(d, 'L')
    ii = np.array([idx[k] for k in t['chaves']])
    out['conferencias']['T7_2026_igual_ao_T7'] = (abs(t['x7'].sum() - r7['2026']['T7_Lula']['excesso_total']) < 1e-6 and
                                                abs(t['g7'].sum() - r7['2026']['T7_Lula']['ganho_total']) < 1e-6)
    gpos = np.maximum(t['g7'], 0)
    e7 = t['x7'] - tx['T7'][0] * gpos
    VAL['T7'][ii] = e7
    e15 = t['q15'] - tx['T15'][0] * t['C2']
    VAL['T15'][ii] = e15
    t15_2026 = {'q_total': float(t['q15'].sum()), 'secoes_com_q': int((t['q15'] > 0).sum()),
                'taxa_2026': float(t['q15'].sum() / t['C2'].sum()),
                'secoes_comparecimento_acima_dos_aptos_2T': t['acima_aptos_2T'],
                'secoes_comparecimento_acima_dos_aptos_1T': t['acima_aptos_1T'],
                'saldo_secoes_especiais_2026': r15['saldo_tirado_pelas_secoes_especiais']['2026']['saldo'],
                'saldo_secoes_especiais_2022': r15['saldo_tirado_pelas_secoes_especiais']['2022']['saldo'],
                'saldo_secoes_especiais_2018': r15['saldo_tirado_pelas_secoes_especiais']['2018_descritivo']['saldo']}
    t7_2026 = {'excesso_total': float(t['x7'].sum()), 'ganho_total': float(t['g7'].sum()), 'ganho_positivo_total': float(gpos.sum()),
               'taxa_sobre_ganho_positivo': float(t['x7'].sum() / gpos.sum())}
    # chave da seção do T15 que mudou de conjunto entre os turnos (só 2T, comparecimento 0): sem efeito
    del t; gc.collect()

    # T28: evento L (lista do T28) e evento D (estimador do T28, sem simulação nova; R_nulo gravado)
    lst = r28['descritivo']['secoes_evento_L_2026_2T']
    out['conferencias']['T28_L_secoes_e_votos'] = [len(lst), sum(x['lula'] for x in lst),
                                                   r28['descritivo']['escala_2026_2T']['L']['secoes'],
                                                   r28['descritivo']['escala_2026_2T']['L']['votos_lula']]
    e28L = np.full(N, -np.inf); e28L_marg = np.full(N, -np.inf); e28L_comp = np.full(N, -np.inf)
    for x in lst:
        i = idx[x['secao']]; f = 1 - tx['T28_L'][0] * x['p_nula_calibrada']
        e28L[i] = f * x['lula']; e28L_marg[i] = f * (x['lula'] - x['flavio']); e28L_comp[i] = f * x['comparecimento']
        if d[x['secao']]['2']['L'] != x['lula']:
            raise SystemExit('lista do T28 não confere com a base: ' + x['secao'])
    log('T28: juntas e evento D')
    junta1 = T28.juntas_zz(z1); junta2 = T28.juntas_zz(z2)
    aD = T28.montar_aumento(d, junta1, junta2)
    oD = T28.estimador_aumento(*aD['dados'], aD['gL'], aD['gM'])
    RnD = r28['resultados']['2026_aumento']['eventos']['D']['R_nulo']
    ks = np.array(aD['chaves'])[oD['ok']]
    A1, C1, A2, C2 = (z[oD['ok']] for z in aD['dados'][:4])
    ev = oD['O']['D']
    out['conferencias']['T28_D_O_e_E_bruto'] = [int(ev.sum()), float(oD['P']['D'].sum()),
                                                r28['resultados']['2026_aumento']['eventos']['D']['O'],
                                                r28['resultados']['2026_aumento']['eventos']['D']['E_bruto']]
    e28D = np.full(N, -np.inf)
    lstD = []
    for j in np.where(ev)[0]:
        k = str(ks[j]); pc = float(oD['P']['D'][j] * RnD); dc = float(C2[j] - C1[j])
        e28D[idx[k]] = (1 - tx['T28_D'][0] * pc) * max(dc, 0.0)
        lstD.append({'secao': k, 'aumento_votantes': int(dc), 'p_nula_calibrada': pc})
    del aD, oD; gc.collect()
    VAL['T28'] = np.maximum(e28L, e28D)

    # T23: efeito de zona de 2026 (composição completa, a principal do T23)
    log('T23 2026')
    B = T23.montar(b26, cand26)
    z = zonas(B, B['XG'])
    del B; gc.collect()
    out['conferencias']['T23_2026_igual_ao_T23'] = [z['votos_ext'], r23['2026_composicao_completa']['zonas_extremas']['votos_somados_a_favor_de_lula']]
    iz = np.array([idx[k] for k in z['sec']])
    VAL['T23'][iz] = z['q_ext'] - tx['T23'][0] * z['n2']
    e23_pos = np.full(N, -np.inf); e23_pos[iz] = z['q_pos'] - tx['T23_positivas'][0] * z['n2']
    t23_2026 = {'sigma2_zona': z['sigma2_zona'], 'limiar_pontos': z['limiar_pontos'], 'zonas_extremas_a_favor': z['zonas_extremas_a_favor'],
                'votos_ext': z['votos_ext'], 'votos_pos': z['votos_pos'], 'votos_finalistas': z['votos_finalistas'],
                'taxa_extremas': z['votos_ext'] / z['votos_finalistas'], 'taxa_positivas': z['votos_pos'] / z['votos_finalistas']}
    del z; gc.collect()

    # T21: liberações sem biometria (cache do T21)
    log('T21')
    c = carregar(nh); s1, s2 = c['1'], c['2']
    NH1t = sum(v[3] for k, v in s1.items() if not k.startswith('ZZ')); C1t = sum(v[1] for k, v in s1.items() if not k.startswith('ZZ'))
    NH2t = sum(v[3] for k, v in s2.items() if not k.startswith('ZZ')); C2t = sum(v[1] for k, v in s2.items() if not k.startswith('ZZ'))
    tx['T21'] = (NH1t / C1t, '2026_1T')
    out['conferencias']['T21_totais_NH_27_UFs'] = [NH1t, NH2t]
    e21 = np.full(N, -np.inf); e21_own = np.full(N, -np.inf); dc21 = np.zeros(N)
    n21 = 0; difcomp = 0
    for k, i in idx.items():
        if k.startswith('ZZ') or k not in s1 or k not in s2:
            continue
        a, b = s1[k], s2[k]
        if a[1] != d[k]['1']['comp'] or b[1] != d[k]['2']['comp']:
            difcomp += 1
        dnh = b[3] - a[3]; dc = b[1] - a[1]
        e21[i] = dnh - tx['T21'][0] * dc; dc21[i] = dc
        if a[1] > 0:
            e21_own[i] = b[3] - a[3] * b[1] / a[1]
        n21 += 1
    out['conferencias']['T21_secoes_e_comparecimento_diferente_da_base'] = [n21, difcomp]
    VAL['T21'] = e21
    del c, s1, s2; gc.collect()

    # dados por seção para os votos de Lula, margem e UF
    L2 = np.array([d[k]['2']['L'] for k in mestre], float)
    limpar_cache(); del d; gc.collect()

    # ---------------- soma
    def resumo(vals, rotulo):
        M = np.vstack([vals[v] for v in VETORES])
        mx = M.max(0)
        E = np.maximum(mx, 0.0)
        venc = np.where(E > 0, M.argmax(0), -1)
        S = np.bincount(loc_ids, weights=E)
        tot = float(E.sum()); ep = float(np.sqrt((S ** 2).sum()))
        por_vetor = {}
        for j, v in enumerate(VETORES):
            m = venc == j
            por_vetor[v] = {'secoes_em_que_e_o_maior': int(m.sum()), 'votos_atribuidos': float(E[m].sum())}
        por_uf = {}
        for u in sorted(set(uf)):
            m = uf == u
            por_uf[u] = float(E[m].sum())
        return {'rotulo': rotulo, 'soma': tot, 'ep': ep, 'secoes_com_excesso': int((E > 0).sum()), 'por_vetor_vencedor': por_vetor,
                'por_uf': por_uf, 'fracao_de_2_22_milhoes': tot / TROCA, 'fracao_de_4_43_milhoes': tot / ACRESCIMO}, E

    def vetor_sozinho(e):
        ok = np.isfinite(e)
        pos = np.maximum(e[ok], 0); neg = np.minimum(e[ok], 0)
        S = np.bincount(loc_ids[ok], weights=pos, minlength=loc_ids.max() + 1)
        Sn = np.bincount(loc_ids[ok], weights=e[ok], minlength=loc_ids.max() + 1)
        return {'secoes_com_valor': int(ok.sum()), 'secoes_com_excesso_positivo': int((e[ok] > 0).sum()),
                'soma_das_partes_positivas': float(pos.sum()), 'ep': float(np.sqrt((S ** 2).sum())),
                'soma_das_partes_negativas': float(neg.sum()), 'soma_liquida': float(e[ok].sum()),
                'ep_soma_liquida': float(np.sqrt((Sn ** 2).sum()))}

    principal, Eprin = resumo(VAL, 'principal')
    out['principal'] = principal
    out['vetores'] = {v: vetor_sozinho(VAL[v]) for v in VETORES}
    out['vetores']['T28']['evento_L'] = vetor_sozinho(e28L)
    out['vetores']['T28']['evento_D'] = vetor_sozinho(e28D)
    out['vetores']['T28']['nota_soma_liquida'] = ('a soma líquida do T28 só cobre as seções dos eventos (a probabilidade das demais '
                                                 'não foi gravada no T28); o excesso em seções contra a maior referência vai ao lado')
    out['vetores']['T28']['excesso_L_em_secoes_contra_maior_referencia'] = (
        r28['resultados']['2026_2T']['eventos']['L']['O'] - tx['T28_L'][0] * r28['resultados']['2026_2T']['eventos']['L']['E_calibrado'])
    out['vetores']['T28']['excesso_D_em_secoes_contra_maior_referencia'] = (
        r28['resultados']['2026_aumento']['eventos']['D']['O'] - tx['T28_D'][0] * r28['resultados']['2026_aumento']['eventos']['D']['E_calibrado'])

    # robustez
    rob = {}
    v = dict(VAL); v['T21'] = e21_own
    rob['R1_T21_taxa_da_propria_secao_no_1T'] = resumo(v, 'R1')[0]
    out['vetores']['T21_R1_taxa_da_propria_secao'] = vetor_sozinho(e21_own)
    v = dict(VAL); v['T28'] = np.maximum(e28L_marg, e28D)
    rob['R2a_T28_margem_de_Lula'] = resumo(v, 'R2a')[0]
    v = dict(VAL); v['T28'] = np.maximum(e28L_comp, e28D)
    rob['R2b_T28_comparecimento'] = resumo(v, 'R2b')[0]
    v = dict(VAL); v['T23'] = e23_pos
    rob['R3_T23_todas_as_zonas_com_efeito_a_favor_do_13'] = resumo(v, 'R3')[0]
    out['vetores']['T23_R3_zonas_positivas'] = vetor_sozinho(e23_pos)
    v = dict(VAL); v['T21'] = np.full(N, -np.inf)
    rob['R4_sem_o_T21'] = resumo(v, 'R4')[0]
    v = dict(VAL); v['T21'] = np.full(N, -np.inf); v['T28'] = np.maximum(e28L_comp, e28D); v['T23'] = e23_pos
    rob['R5_sem_o_T21_e_com_as_leituras_mais_largas_de_T28_e_T23'] = resumo(v, 'R5')[0]
    # sensibilidade do T21 à taxa que falta (2018 e 2022): taxa do 1º turno mais ou menos 0,5 ponto (descritivo)
    for dlt in (-0.005, +0.005):
        v = dict(VAL); v['T21'] = np.where(np.isfinite(e21), e21 - dlt * dc21, -np.inf)
        rob[f'R6_T21_taxa_{"menos" if dlt < 0 else "mais"}_0,5_ponto'] = resumo(v, 'R6')[0]
    # R7: sem o piso em zero (soma do maior excesso da seção, negativo inclusive)
    M = np.vstack([VAL[v] for v in VETORES]); mx = M.max(0); okm = np.isfinite(mx)
    Sn = np.bincount(loc_ids[okm], weights=mx[okm], minlength=loc_ids.max() + 1)
    rob['R7_sem_piso_em_zero'] = {'soma': float(mx[okm].sum()), 'ep': float(np.sqrt((Sn ** 2).sum())), 'secoes': int(okm.sum())}
    del M, mx
    out['robustez'] = rob
    # descritivos fora do registro
    desc = {}
    desc['soma_sem_deduplicar'] = float(sum(out['vetores'][k]['soma_das_partes_positivas'] for k in VETORES))
    desc['soma_das_somas_liquidas'] = float(sum(out['vetores'][k]['soma_liquida'] for k in VETORES))
    e = e21[np.isfinite(e21)]
    fx = {}
    for lo, hi in ((0, 5), (5, 20), (20, 50), (50, math.inf)):
        mp = (e > lo) & (e <= hi); mn = (-e > lo) & (-e <= hi)
        fx[f'{lo}-{hi if math.isfinite(hi) else "mais"}'] = {'secoes_positivas': int(mp.sum()), 'votos_positivos': float(e[mp].sum()),
                                                            'secoes_negativas': int(mn.sum()), 'votos_negativos': float(-e[mn].sum())}
    desc['T21_por_tamanho_do_excesso'] = fx
    desc['T21_espelho_excesso_do_1T_sobre_o_2T'] = float(-out['vetores']['T21']['soma_das_partes_negativas'])
    desc['T21b_coeficientes'] = {'sem_biometria': r21['b_regressoes']['principal']['coef']['sem_biometria'],
                                 'ep_sem': r21['b_regressoes']['principal']['ep']['sem_biometria'],
                                 'com_biometria': r21['b_regressoes']['principal']['coef']['com_biometria'],
                                 'ep_com': r21['b_regressoes']['principal']['ep']['com_biometria']}
    out['descritivo_fora_do_registro'] = desc

    # taxas
    out['taxas_de_referencia'] = {
        'T21': {'maior': tx['T21'][0], 'de': tx['T21'][1], 'disponiveis': {'2026_1T': tx['T21'][0]},
                'ausentes': {'2018': 'sem o campo de biometria nas bases locais', '2022': 'sem o campo de biometria nas bases locais'},
                '2026_2T_para_comparar': NH2t / C2t},
        'T15': {'maior': tx['T15'][0], 'de': tx['T15'][1], 'disponiveis': {a: refs[a]['T15']['taxa'] for a in refs} | {'2026_1T': 0.0},
                '2026_2T_para_comparar': t15_2026['taxa_2026']},
        'T7': {'maior': tx['T7'][0], 'de': tx['T7'][1], 'disponiveis': {a: refs[a]['T7']['taxa_sobre_ganho_positivo'] for a in refs},
               '2026_2T_para_comparar': t7_2026['taxa_sobre_ganho_positivo'], 'ausente': {'2026_1T': 'não há turno anterior'}},
        'T28_L': {'maior': tx['T28_L'][0], 'de': tx['T28_L'][1], 'disponiveis': RcL, 'ep': RcL_ep,
                  '2026_2T_para_comparar': r28['resultados']['2026_2T']['eventos']['L']['Rc']},
        'T28_D': {'maior': tx['T28_D'][0], 'de': tx['T28_D'][1], 'disponiveis': RcD,
                  '2026_2T_para_comparar': r28['aumento_de_comparecimento']['D']['Rc_2026'], 'ausente': {'2026_1T': 'não há turno anterior'}},
        'T23': {'maior': tx['T23'][0], 'de': tx['T23'][1], 'disponiveis': {a: refs[a]['T23']['taxa_extremas'] for a in refs},
                '2026_2T_para_comparar': t23_2026['taxa_extremas'], 'ausente': {'2026_1T': 'não há turno anterior'}},
        'T23_positivas_R3': {'maior': tx['T23_positivas'][0], 'de': tx['T23_positivas'][1],
                             'disponiveis': {a: refs[a]['T23']['taxa_positivas'] for a in refs}, '2026_2T_para_comparar': t23_2026['taxa_positivas']}}
    out['descritivo_2026'] = {'T7': t7_2026, 'T15': t15_2026, 'T23': t23_2026, 'T21': {'NH1': NH1t, 'C1': C1t, 'NH2': NH2t, 'C2': C2t},
                              'T28_secoes_evento_D': lstD}
    soma = principal['soma']; ep = principal['ep']
    veredito = 'SEM SINAL' if soma <= SEM_SINAL else ('SINAL' if soma >= SINAL else 'INCONCLUSIVO')
    out['veredito'] = veredito
    out['fora_da_soma'] = {
        'T17': 'atributo da máquina: o teste só foi rodado na amostra (3.897 seções) e nos locais dos Adendos 10 e 11; não há '
               'coeficiente nem valor por seção na base completa',
        'votos_depois_das_17h': 'a hora de cada voto só existe nos logs da amostra; o bweb traz só a hora de encerramento da seção'}
    out['segundos'] = round(time.time() - T0, 1)
    out['rodado_em_utc'] = time.strftime('%Y-%m-%dT%H:%M:%SZ', time.gmtime())
    for k in list(out['robustez']):
        if out['robustez'][k] is None:
            del out['robustez'][k]
    with open(saida_json, 'w') as f:
        json.dump(out, f, ensure_ascii=False, indent=1, default=lambda x: x.item() if hasattr(x, 'item') else str(x))
    if tabela:
        with gzip.open(tabela, 'wt') as f:
            f.write('secao\tlocal\t' + '\t'.join(VETORES) + '\tmaior\n')
            for i, k in enumerate(mestre):
                vals = [VAL[v][i] for v in VETORES]
                if max(vals) > 0:
                    f.write(k + '\t' + str(loc_ids[i]) + '\t' + '\t'.join('' if not np.isfinite(x) else f'{x:.3f}' for x in vals)
                            + f'\t{Eprin[i]:.3f}\n')
    log('soma', soma, 'ep', ep, veredito)
    escrever_txt(out, saida_txt)


# ---------------------------------------------------------------------------------------------- texto
def fn(x, nd=0):
    s = f'{x:,.{nd}f}'
    return s.replace(',', 'X').replace('.', ',').replace('X', '.')


def pct(x, nd=3):
    return fn(100 * x, nd) + '%'


def escrever_txt(o, caminho):
    L = []; A = L.append
    p = o['principal']; t = o['taxas_de_referencia']; v = o['vetores']; r = o['referencias']; d26 = o['descritivo_2026']
    A('T27. Teto somado dos vetores medidos (Adendo 9), com o bweb completo do 2º turno de 2026')
    A('Script: scripts/analisar_T27.py. Números completos: resultados/T27_bweb.json.')
    A('Bases: secoes2026.json.gz (1º e 2º turno), secoes2018.json.gz, secoes2022.json.gz, candidatos2026_1t.json.gz, o cache de')
    A('biometria do T21 (nh_secoes_2026.json.gz, lido dos zips do bweb dos dois turnos), os zips do exterior (juntas, como no T28) e')
    A('os resultados já gravados de T7, T15, T21, T23 e T28 (resultados/*_bweb.json).')
    A('')
    A('Critério registrado (PRE-REGISTRO-2026-10-26.md, Adendo 9, antes dos dados):')
    A('  "' + o['criterio_registrado'] + '"')
    A('')
    A(f'VEREDITO PELA LETRA: {o["veredito"]}')
    A('')
    A('Resumo')
    A(f'- Soma dos excessos por seção, cada voto uma vez no vetor de maior valor da seção: {fn(p["soma"])} votos '
      f'(ep {fn(p["ep"])}), em {fn(p["secoes_com_excesso"])} seções.')
    A(f'  Limites: sem sinal até 500.000; sinal 2.200.000 ou mais. A soma é {pct(p["fracao_de_2_22_milhoes"], 1)} dos 2,22 milhões da troca e '
      f'{pct(p["fracao_de_4_43_milhoes"], 1)} dos 4,43 milhões do acréscimo.')
    pv = p['por_vetor_vencedor']
    A('- Votos atribuídos a cada vetor (o maior da seção): ' + '; '.join(
        f'{k} {fn(pv[k]["votos_atribuidos"])} ({fn(pv[k]["secoes_em_que_e_o_maior"])} seções)' for k in VETORES) + '.')
    A('- Fora da soma, sem dado por seção na base completa: T17 (o teste só existe na amostra de 3.897 seções e nos locais dos')
    A('  Adendos 10 e 11) e votos depois das 17h (a hora de cada voto só está nos logs da amostra; o bweb tem só a hora de')
    A('  encerramento da seção). Os dois ficam listados e não entram na soma.')
    A('')
    A('1. Leituras declaradas (o registro não fixa estes pontos; cada um é desvio declarado do registro)')
    for linha in o['leituras'].splitlines():
        A('  ' + linha.strip())
    A('')
    A('2. Conferências (o código reproduz os números já registrados antes de somar)')
    cf = o['conferencias']
    A(f'  T7 de 2018 e 2022 iguais ao T7 registrado: {"sim" if cf["T7_referencias_iguais_ao_T7"] else "NÃO"}; '
      f'T7 de 2026 igual: {"sim" if cf["T7_2026_igual_ao_T7"] else "NÃO"}.')
    A(f'  T23, votos nas zonas extremas a favor do 13: 2018 {fn(cf["T23_valores"]["2018"][0], 1)} (registrado {fn(cf["T23_valores"]["2018"][1], 1)}), '
      f'2022 {fn(cf["T23_valores"]["2022"][0], 1)} ({fn(cf["T23_valores"]["2022"][1], 1)}), 2026 {fn(cf["T23_2026_igual_ao_T23"][0], 1)} '
      f'({fn(cf["T23_2026_igual_ao_T23"][1], 1)}).')
    A(f'  T28, evento de Lula: {cf["T28_L_secoes_e_votos"][0]} seções e {fn(cf["T28_L_secoes_e_votos"][1])} votos de Lula na lista '
      f'(registrado {cf["T28_L_secoes_e_votos"][2]} e {fn(cf["T28_L_secoes_e_votos"][3])}); evento de aumento: O {cf["T28_D_O_e_E_bruto"][0]} '
      f'e esperado bruto {fn(cf["T28_D_O_e_E_bruto"][1], 1)} (registrado {cf["T28_D_O_e_E_bruto"][2]} e {fn(cf["T28_D_O_e_E_bruto"][3], 1)}).')
    A(f'  T21: NH das 27 UFs {fn(cf["T21_totais_NH_27_UFs"][0])} no 1º turno e {fn(cf["T21_totais_NH_27_UFs"][1])} no 2º (T21: 8.342.249 e 8.632.488); '
      f'{fn(cf["T21_secoes_e_comparecimento_diferente_da_base"][0])} seções, comparecimento diferente da base em '
      f'{cf["T21_secoes_e_comparecimento_diferente_da_base"][1]}.')
    A('')
    A('3. Taxas de referência (a maior entra no cálculo)')
    A(f'  T21 (NH por votante): 1º turno de 2026 {pct(t["T21"]["maior"])}; 2018 e 2022 sem o campo (QT_ELEITORES_BIOMETRIA_NH) nas bases')
    A(f'       locais. Para comparar, 2º turno de 2026: {pct(t["T21"]["2026_2T_para_comparar"])}.')
    A(f'  T15 (votantes acima dos aptos do 1º turno, por votante do 2º): 2018 {pct(t["T15"]["disponiveis"]["2018"], 4)}, 2022 '
      f'{pct(t["T15"]["disponiveis"]["2022"], 4)}, 1º turno de 2026 0 (comparecimento acima dos aptos: 0 seções); maior {t["T15"]["de"]}. '
      f'2026: {pct(t["T15"]["2026_2T_para_comparar"], 4)}.')
    A(f'  T7 (excesso sobre o ganho positivo): 2018 {pct(t["T7"]["disponiveis"]["2018"])}, 2022 {pct(t["T7"]["disponiveis"]["2022"])}; '
      f'maior {t["T7"]["de"]}. 2026: {pct(t["T7"]["2026_2T_para_comparar"])}. (O (b) registrado, sobre o ganho líquido: '
      f'2018 {pct(r["2018"]["T7"]["taxa_registrada_b_sobre_ganho_liquido"])}, 2022 {pct(r["2022"]["T7"]["taxa_registrada_b_sobre_ganho_liquido"])}.)')
    A(f'  T28 evento de Lula (O/E calibrado): 2022 2T {fn(t["T28_L"]["disponiveis"]["2022_2T"], 3)} (ep {fn(t["T28_L"]["ep"]["2022_2T"], 3)}), '
      f'2026 1T {fn(t["T28_L"]["disponiveis"]["2026_1T"], 3)} (ep {fn(t["T28_L"]["ep"]["2026_1T"], 3)}), 2018 2T '
      f'{fn(t["T28_L"]["disponiveis"]["2018_2T"], 3)}; maior {t["T28_L"]["de"]}. 2026 2T: {fn(t["T28_L"]["2026_2T_para_comparar"], 3)}.')
    A(f'  T28 evento de aumento de 15 pontos (O/E calibrado): 2022 {fn(t["T28_D"]["disponiveis"]["2022"], 3)}, 2018 '
      f'{fn(t["T28_D"]["disponiveis"]["2018"], 3)}; maior {t["T28_D"]["de"]}. 2026: {fn(t["T28_D"]["2026_2T_para_comparar"], 3)}.')
    A(f'  T23 (votos deslocados nas zonas extremas a favor do 13, por voto nos finalistas): 2018 {pct(t["T23"]["disponiveis"]["2018"], 4)}, '
      f'2022 {pct(t["T23"]["disponiveis"]["2022"], 4)}; maior {t["T23"]["de"]}. 2026: {pct(t["T23"]["2026_2T_para_comparar"], 4)}.')
    A('')
    A('4. Cada vetor sozinho (excesso por seção sobre a maior taxa; partes positivas, partes negativas e soma líquida, em votos)')
    for k in VETORES:
        x = v[k]
        A(f'  {k:4s}: {fn(x["secoes_com_valor"])} seções com valor, {fn(x["secoes_com_excesso_positivo"])} com excesso positivo; '
          f'positivas {fn(x["soma_das_partes_positivas"])} (ep {fn(x["ep"])}); negativas {fn(x["soma_das_partes_negativas"])}; '
          f'líquida {fn(x["soma_liquida"])} (ep {fn(x["ep_soma_liquida"])})')
    A(f'        T28 por evento: Lula {fn(v["T28"]["evento_L"]["soma_das_partes_positivas"])} votos em '
      f'{v["T28"]["evento_L"]["secoes_com_excesso_positivo"]} seções; aumento {fn(v["T28"]["evento_D"]["soma_das_partes_positivas"])} '
      f'em {v["T28"]["evento_D"]["secoes_com_excesso_positivo"]}. A soma líquida do T28 só cobre as seções dos eventos; em seções, o '
      f'excesso contra a maior referência é {fn(v["T28"]["excesso_L_em_secoes_contra_maior_referencia"], 1)} (Lula) e '
      f'{fn(v["T28"]["excesso_D_em_secoes_contra_maior_referencia"], 1)} (aumento); negativo quer dizer menos seções do que a maior referência daria.')
    x = v['T21_R1_taxa_da_propria_secao']
    A(f'  T21 com a taxa da própria seção no 1º turno (R1): positivas {fn(x["soma_das_partes_positivas"])} (ep {fn(x["ep"])}); negativas '
      f'{fn(x["soma_das_partes_negativas"])}; líquida {fn(x["soma_liquida"])} (ep {fn(x["ep_soma_liquida"])}).')
    x = v['T23_R3_zonas_positivas']
    A(f'  T23 com todas as zonas de efeito a favor do 13 (R3): positivas {fn(x["soma_das_partes_positivas"])}; líquida {fn(x["soma_liquida"])}.')
    A('')
    A('5. Soma do T27 e robustez (cada voto uma vez, no vetor de maior valor da seção)')
    A(f'  principal: {fn(p["soma"])} (ep {fn(p["ep"])}) => {o["veredito"]}')
    for k, x in o['robustez'].items():
        ver = 'SEM SINAL' if x['soma'] <= SEM_SINAL else ('SINAL' if x['soma'] >= SINAL else 'INCONCLUSIVO')
        A(f'  {k}: {fn(x["soma"])} (ep {fn(x["ep"])}) => pela mesma regra, {ver}')
    A('')
    ds = o['descritivo_fora_do_registro']
    A('  Descritivo: sem deduplicar (soma das partes positivas de cada vetor) ' + fn(ds['soma_sem_deduplicar']) +
      '; soma das somas líquidas dos vetores ' + fn(ds['soma_das_somas_liquidas']) + ' (a do T28 só nas seções dos eventos).')
    A('')
    A('6. Por UF, soma principal (votos)')
    pu = p['por_uf']
    A('  ' + '; '.join(f'{u} {fn(pu[u])}' for u in sorted(pu, key=lambda u: -pu[u])))
    A('')
    A('7. T21 por tamanho do excesso da seção (descritivo, fora do registro)')
    A('  faixa (votos) | seções com excesso | votos | seções com déficit | votos')
    for k, x in ds['T21_por_tamanho_do_excesso'].items():
        A(f'  {k:10s} | {fn(x["secoes_positivas"]):>9s} | {fn(x["votos_positivos"]):>9s} | {fn(x["secoes_negativas"]):>9s} | {fn(x["votos_negativos"]):>9s}')
    A('')
    A('8. Leitura')
    v21 = v['T21']; tot = p['soma']; pv = p['por_vetor_vencedor']
    sem21 = o['robustez']['R4_sem_o_T21']['soma']
    A(f'- Pela letra, {fn(tot)} votos ficam entre 0,5 e 2,2 milhões: {o["veredito"]}. A distância é grande nos dois sentidos em erros-padrão '
      f'({fn((tot - SEM_SINAL) / p["ep"])} ep acima de 0,5 milhão e {fn((SINAL - tot) / p["ep"])} abaixo de 2,2 milhões); o erro-padrão mede só a variação')
    A('  entre locais e não a escolha de leitura, que pesa muito mais (abaixo).')
    A(f'- O T21 responde por {fn(pv["T21"]["votos_atribuidos"])} dos {fn(tot)} votos ({pct(pv["T21"]["votos_atribuidos"] / tot, 1)}). As partes positivas do')
    A(f'  T21 ({fn(v21["soma_das_partes_positivas"])}) e as negativas ({fn(-v21["soma_das_partes_negativas"])}) quase se anulam: a soma líquida é '
      f'{fn(v21["soma_liquida"])} (ep {fn(v21["ep_soma_liquida"])}), o mesmo excesso nacional')
    A('  sobre a proporção do 1º turno que o T21 relatou (+95.224). O teto por seção soma a metade positiva da variação das liberações sem')
    A('  biometria de uma seção para outra entre os turnos; a mesma conta com os turnos trocados e a mesma taxa (excesso do 1º turno sobre o 2º) daria')
    rb = o['robustez']
    A(f'  {fn(ds["T21_espelho_excesso_do_1T_sobre_o_2T"])}. Com a taxa da própria seção (R1) o total vai a {fn(rb["R1_T21_taxa_da_propria_secao_no_1T"]["soma"])}; com a taxa do')
    A(f'  1º turno 0,5 ponto abaixo ou acima (R6, no lugar das referências de 2018 e 2022 que faltam), a {fn(rb["R6_T21_taxa_menos_0,5_ponto"]["soma"])} e '
      f'{fn(rb["R6_T21_taxa_mais_0,5_ponto"]["soma"])}.')
    A(f'- Sem o T21, os outros vetores somam {fn(sem21)} (ep {fn(o["robustez"]["R4_sem_o_T21"]["ep"])}), '
      f'{"abaixo" if sem21 <= SEM_SINAL else "acima"} de 0,5 milhão; com as leituras mais largas de T28 e')
    A(f'  T23, {fn(o["robustez"]["R5_sem_o_T21_e_com_as_leituras_mais_largas_de_T28_e_T23"]["soma"])}. O T7 dá {fn(pv["T7"]["votos_atribuidos"])}, o T28 '
      f'{fn(pv["T28"]["votos_atribuidos"])}, o T23 {fn(pv["T23"]["votos_atribuidos"])} e o T15 {fn(pv["T15"]["votos_atribuidos"])}.')
    A('- Teto não é estimativa de fraude: ele conta cada liberação sem biometria a mais como um voto que poderia ter sido inserido. O')
    cb = ds['T21b_coeficientes']
    A(f'  T21(b) mediu, dentro do local, {fn(cb["sem_biometria"], 3)} voto de Lula por liberação sem biometria a mais (ep {fn(cb["ep_sem"], 3)}) e '
      f'{fn(cb["com_biometria"], 3)} por habilitação com biometria a mais')
    A(f'  (ep {fn(cb["ep_com"], 3)}); votos inseridos para Lula dariam perto de 1. Isso é outro teste e não entra na conta do T27.')
    A(f'- Mesmo como teto, a soma fica em {pct(tot / TROCA, 1)} dos 2,22 milhões que a troca exigiria e em {pct(tot / ACRESCIMO, 1)} dos 4,43 milhões do acréscimo.')
    A('  "Chegar perto não prova fraude" (registro); ' + ('aqui a soma não chega ao limite de sinal.' if tot < SINAL else 'a soma passa do limite de sinal.'))
    A('- Ficam de fora, sem dado por seção na base completa: T17 e votos depois das 17h. Na amostra, o T17 de urnas antigas contra novas')
    A('  deu 0,0 ponto (ep 0,14) e o T30 por horário foi lido como composição (resultados/ADENDO9_resultados_amostra.txt); nenhum dos dois')
    A('  tem valor por seção para entrar aqui. O bweb tem o número da urna nos dois turnos, o que permitiria refazer parte do T17')
    A('  (modelo e urna trocada, sem contingência) na base completa; isso não foi feito nesta rodada.')
    A('')
    A('9. Desvios do registro')
    A('- Todas as leituras L1 a L5 acima: o registro não diz o que é "taxa" de cada vetor, qual base multiplica a taxa, se a seção sem')
    A('  excesso entra com zero, nem que votos contar em T28 e T23. A leitura escolhida é a mais literal que conseguimos: taxa de cada')
    A(f'  eleição como um número, a forma do T4 para o excesso e piso em zero por seção. Sem o piso (R7) a soma é {fn(rb["R7_sem_piso_em_zero"]["soma"])}: o T15')
    A('  vale cerca de zero em toda seção, então o máximo entre os vetores já fica perto de zero ou acima dele.')
    A('- T21 sem as referências de 2018 e 2022 (campo de biometria ausente nas bases locais); só o 1º turno de 2026 dá a taxa.')
    A('- T7, T15 (aptos entre turnos), T23 e o evento de aumento do T28 não têm taxa no 1º turno de 2026 (não há turno anterior).')
    A('- T7 usa como base o ganho positivo da seção (e a taxa das referências pela mesma base), para que a seção em que Lula perdeu votos')
    A('  não ganhe excesso; o (b) registrado usa o ganho líquido (1,086% em 2022 contra 1,078% aqui).')
    A('- T17 e votos depois das 17h ficam fora da soma (sem dado por seção na base completa).')
    A('- Ordem: a principal e as robustez R1 a R6 estavam no script na primeira rodada completa (29/10, 03h21 UTC, mesmo número da')
    A('  principal); depois dela entraram só a R7, o descritivo da seção 7 e o texto de leitura, sem mudar a principal.')
    with open(caminho, 'w') as f:
        f.write('\n'.join(L) + '\n')


if __name__ == '__main__':
    if '--so-texto' in sys.argv:
        o = json.load(open(sys.argv[sys.argv.index('--so-texto') + 1]))
        escrever_txt(o, sys.argv[sys.argv.index('--so-texto') + 2])
    else:
        main()
