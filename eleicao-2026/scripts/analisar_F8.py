"""F8 do Adendo 20 (PRE-REGISTRO-2026-10-26.md, commit d976d4d): o que os EUA e os observadores disseram, e a conferência
nos dados locais de cada indício concreto.

Registro (escrito antes de rodar, Adendo 20, F8):
  "Texto, data e órgão de cada declaração do governo dos EUA sobre o 2º turno de 2026, se fala em indícios de fraude e
  quais; relatórios de observação internacional (OEA, UE, Centro Carter, Parlasul e outros); posição e auditoria do PL.
  Cada indício concreto que der para conferir nos dados públicos é conferido; o que não der é relatado como tal."
  O F8 não tem limiar numérico: o veredito pela letra é DESCRITIVO, e cada indício sai como CONFERE, NÃO CONFERE,
  CONFERE EM PARTE ou NÃO CONFERÍVEL (sem dado local).

O que a pesquisa achou e motivou cada conferência (fontes no texto de saída, resultados/F8_eua_observadores.txt):
  Governo dos EUA. Trump, 26/10: "looked like another rigged election", "the way it was tabulated", "The extension given
  was very strange". 27/10 (comício no Texas): o Brasil "is doing a pretty good job also" (de fraudar), "it didn't look
  too good". 28/10: "Foi uma eleição muito estranha", "não vou me envolver". 29/10: "the election was a disgrace in
  Brazil", "a very great embarrassment", a bolsa "through the floor"; não diz se reconhece Lula. Departamento de Estado:
  nota de felicitação retida (26/10), vistos para Flávio e família (27/10), sem comentário sobre o resultado. Embaixada
  em Brasília (telegrama de 26/10, revelado pela Folha em 29/10): vitória "surpreendente, mas definitiva"; ampliação do
  horário "mal administrada"; cerca de 34 mil votos depois das 17h, uns 0,03%, contra margem de 4,4 milhões.
  Observadores. OEA (27/10): "não tem dúvidas quanto à integridade dos dados oficiais"; dados do TSE coincidem com o que
  os observadores colheram em 977 seções; a prorrogação gerou confusão; problemas de transporte. Centro Carter (27/10):
  prorrogação "controversa", decidida "after polls had closed"; resultados "within hours of polls closing". Parlasul
  (25/10): atenta às "implicações da decisão do STF de prorrogar a votação". UE: sem declaração sobre o 2º turno até
  30/10; anunciou que confrontaria amostras de boletins com o resultado oficial.
  PL e Flávio. PL (26/10): reconhece o resultado e cobra esclarecimentos (gastos sociais). Rogério Marinho (28 e 29/10):
  "não há provas". Flávio (25 a 28/10): a prorrogação mudou as regras; a ordem "só chegou depois do fim do horário
  legal, quando as urnas já estavam encerradas"; "Eleitores ficaram submetidos a regras diferentes"; Lula "acrescentou
  mais de 10 milhões de votos", uma "impossibilidade matemática"; fiscais do PL retirados da sala-cofre; no dia, pediu a
  apoiadores que vigiassem depois das 17h se mesários votavam por ausentes. Musk (26/10): "Math doesn't add up".
  Auditorias independentes (GitHub, não oficiais): soma dos boletins igual ao oficial; RDV igual ao boletim; assinaturas
  válidas; 34.319 a 34.584 votos depois das 17h; 7.353 urnas encerradas depois das 17h45; 8.632.488 eleitores liberados
  sem biometria (6,73%); "urnas encerradas após 17h: Flávio 52,40%, +1.748.468; no 1º turno 55,20%, +3.397.055";
  seções sem log ou com log trocado (Guarulhos 395/298, Santa Maria de Jetibá 9/85 e 9/112), seção sem RDV (CE
  14176/21/136), duas seções do exterior sem boletim (102 eleitores); "106 seções com zero voto para Flávio" (alegação
  que circulou).

Especificação fixada aqui antes de rodar (o registro não fixa nada disso; tudo é desvio declarado):
  E0. Fuso: o mesmo do L1 e do L8 (hora cheia modal da abertura do município no turno, sem junta; deslocamento = modal -
      8; hora de Brasília = hora local - deslocamento). Exterior (ZZ) fora das contas de horário. Antes de fixar os
      grupos de E2, olhei só a distribuição do encerramento local por UF no 2º turno (sem votos; script
      explora_enc.py na pasta de trabalho). Ela mostra o aglomerado das 19h00 a 19h15 de Brasília em RJ, SP, BA, PE,
      PB, SE, DF e poucos outros, e nada em PR e SC.
  E1. Soma (OEA, embaixada, auditorias): Lula, Flávio, branco, nulo e comparecimento do 2º turno na base, contra o oficial
      do TSE guardado em resultados/soma_oficial_2t.json (consulta das 23:27:02 de 25/10). Seções com 2º turno na base.
      Margem e fração 34.393 / comparecimento (TSE) para a frase da embaixada.
  E2. Prorrogação (Trump, embaixada, OEA, Carter, Parlasul, Flávio). Grupos por encerramento em Brasília no 2º turno, Brasil:
      "no horário" até 17:15:59; "intermediária" de 17:16:00 a 18:29:59; "mantida aberta" de 18:30:00 em diante (a ordem
      saiu às 17h03 e valia até as 19h para as seções ainda abertas). (a) Contagens por grupo e por UF; seções já
      encerradas às 17:03:00 de Brasília (hora da liminar, conforme resultados/contexto_2t_2026_e_onde_estaria_a_fraude.txt).
      (b) "Regras diferentes": municípios com pelo menos uma seção mantida aberta e pelo menos uma no horário; quantos
      e quantos eleitores. (c) "Ajudou um lado": por UF com 50 ou mais seções mantidas abertas, fatia de Lula entre os
      finalistas no 2º e no 1º turno, nas mantidas abertas e nas demais da mesma UF, e a virada (2º menos 1º, pontos).
      (d) Regressão da virada da seção contra o indicador "mantida aberta", efeito fixo de local de votação, peso
      L2+R2, erro agrupado por local (como no L8, com este corte). (e) Margem nacional sem as mantidas abertas e no pior
      caso (todo o comparecimento delas como voto líquido de Lula).
  E3. Pausa e rapidez da apuração (Trump "tabulated"; Carter "within hours"). DT_BU_RECEBIDO do 2º turno, todas as seções:
      primeiro recebimento, boletins até 17:07:59, maior intervalo sem recebimento entre 17h e 23h59, horários de 50%,
      90%, 99% e 100% das seções.
  E4. "Mais de 10 milhões" e "Math doesn't add up" (Flávio, Musk). Mesmas seções nos dois turnos (base): ganho de Lula e de
      Flávio; votos dos eliminados no 1º turno (O1); queda de branco+nulo; aumento do comparecimento; a identidade
      contábil nacional. Por seção: "folga" = O1 + max(0, BN1 - BN2) + max(0, comp2 - comp1). Contagem de seções em que
      o ganho de Lula passa a folga (só possível se eleitor de Flávio do 1º turno trocou de lado, ou se o eleitorado da
      seção mudou), soma do excesso, e o mesmo para Flávio (espelho). Também a dispersão: seções em que Lula ganha e
      Flávio perde votos. Descritivo, sem limiar.
  E5. Indícios clássicos citados nas redes e nas auditorias: seções com zero voto para um finalista (comparecimento 1 ou
      mais), nos dois turnos e nos dois lados; seções com comparecimento acima dos aptos; seções com comparecimento
      igual aos aptos e 50 aptos ou mais. Dois turnos, dois lados.
  E6. Números das auditorias independentes. (a) Urnas do Brasil encerradas depois das 17h45 de Brasília (Mateus Costa Cruz:
      7.353). (b) Soma de QT_ELEI_BIOM_SEM_HABILITACAO no 2º turno e fração do comparecimento (ioraysilva: 8.632.488,
      6,73%). (c) Tentativa de reproduzir "urnas encerradas após 17h: Flávio 52,40%, +1.748.468; 1º turno 55,20%,
      +3.397.055" com seis cortes fixados aqui: relógio local depois de 17:00:00, 17:00:59, 17:05:59; Brasília depois de
      17:00:59, 17:05:59, 17:15:59 (Brasil, mesmas seções no 1º turno). Reproduz se a fatia de Flávio bate em 0,05 ponto
      e a margem em 0,5%. (d) Seções nomeadas: Guarulhos (SP) zona 395 seção 298; Santa Maria de Jetibá (ES) zona 9
      seções 85 e 112; CE 14176/21/136; as duas seções do exterior sem boletim: o que o bweb e a base dizem delas e se
      estão na amostra de arquivos de urna (T3).
  E7. Transporte (OEA; motivo do pedido da coligação de Lula: frota de ônibus reduzida em Salvador e São Paulo):
      comparecimento / aptos no 1º e no 2º turno nas capitais Salvador e São Paulo, no resto de BA e de SP e no Brasil
      (mesmas seções). Descritivo: a frota menor deveria aparecer como comparecimento menor.
  Acrescentado depois da primeira rodada (declarado, descritivo): em E5, como estavam no 1º turno as seções com Flávio
  zerado no 2º; em E6, as seções do exterior no bweb do 2º turno (quantas, quantas com agregação, quantas sem voto),
  para comparar as duas auditorias que divergem sobre isso (2 seções contra 70).
  Fora: falas sem fato verificável (bolsa, abuso de poder, gastos sociais, sala-cofre, "dossiê") ficam como NÃO
  CONFERÍVEL no texto; o número de votos depois das 17h vem do TSE, das auditorias e do T3 (amostra), porque o bweb
  não tem a hora de cada voto.

Uso: python3 -I analisar_F8.py <cache_L1_dir> <secoes2026.json.gz> <soma_oficial_2t.json> <T3_logs_amostra.json> <saida.json>
"""
import os as _os, sys as _sys
_sys.path.insert(0, _os.path.dirname(_os.path.abspath(__file__)))
import collections, datetime as dt, json, sys
import numpy as np
from lib import carregar, fe_ols
from analisar_L1 import p_dt, log
import gzip

DIA = {1: dt.datetime(2026, 10, 4), 2: dt.datetime(2026, 10, 25)}


def pct(a, b):
    return 100.0 * a / b if b else float('nan')


def inteiro(x):
    try:
        return max(0, int(x))
    except (TypeError, ValueError):
        return 0


def ler_cache(cache, t):
    with gzip.open(_os.path.join(cache, f'bu{t}t.json.gz'), 'rt') as f:
        return json.load(f)['secoes']


def main():
    cache, base_path, oficial_path, t3_path, saida = sys.argv[1:6]
    bu = {1: ler_cache(cache, 1), 2: ler_cache(cache, 2)}
    base = carregar(base_path)
    oficial = json.load(open(oficial_path))['br']['oficial']
    t3 = json.load(open(t3_path))['2']
    log(f'bweb 1T {len(bu[1])}, 2T {len(bu[2])}; base {len(base)}; T3 {len(t3)}')
    R = {'registro': __doc__.split('Uso:')[0]}

    # ---------------------------------------------------------------- E0 fuso
    mh = {1: collections.defaultdict(collections.Counter), 2: collections.defaultdict(collections.Counter)}
    for t in (1, 2):
        for k, v in bu[t].items():
            ab = p_dt(v.get('DT_ABERTURA'))
            if ab is not None and v.get('NR_JUNTA_APURADORA', '-1') in ('-1', ''):
                uf, mun = k.split('|')[:2]
                mh[t][(uf, mun)][ab.hour] += 1
    modal = {t: {m: c.most_common(1)[0][0] for m, c in mh[t].items()} for t in (1, 2)}

    def off(t, k):
        uf, mun = k.split('|')[:2]
        hm = modal[t].get((uf, mun))
        if hm is None:
            hm = modal[3 - t].get((uf, mun), 8)
        return hm - 8

    S = {1: {}, 2: {}}
    for t in (1, 2):
        for k, v in bu[t].items():
            b = base.get(k, {}).get(str(t))
            if b is None:
                continue
            enc = p_dt(v.get('DT_ENCERRAMENTO'))
            o = off(t, k)
            S[t][k] = {'enc_loc': enc, 'enc_br': (enc - dt.timedelta(hours=o)) if enc else None,
                       'rec': p_dt(v.get('DT_BU_RECEBIDO')), 'apt': b['apt'], 'comp': b['comp'], 'L': b['L'], 'R': b['R'],
                       'O': b.get('O', 0), 'B': b['B'], 'N': b['N'], 'loc': b['loc'], 'zz': k.startswith('ZZ'),
                       'nh': inteiro(v.get('QT_ELEI_BIOM_SEM_HABILITACAO')),
                       'mun_nome': v.get('NM_MUNICIPIO', ''), 'tipo': v.get('DS_TIPO_URNA', ''),
                       'agreg': v.get('DS_SECOES_AGREGADAS', '#NULO#')}

    # ---------------------------------------------------------------- E1 soma
    tot = collections.Counter()
    n2 = 0
    for k, v in base.items():
        b = v.get('2')
        if not b:
            continue
        n2 += 1
        for c in ('L', 'R', 'B', 'N', 'comp'):
            tot[c] += b[c]
    R['E1_soma'] = {'secoes_com_2t_na_base': n2, 'base': dict(tot),
                    'oficial': {c: oficial[c] for c in ('L', 'R', 'B', 'N', 'comp')},
                    'diferenca': {c: tot[c] - oficial[c] for c in ('L', 'R', 'B', 'N', 'comp')},
                    'secoes_totalizadas_oficial': oficial.get('secoes_tot'),
                    'margem': tot['L'] - tot['R'], 'L_pct_validos': pct(tot['L'], tot['L'] + tot['R']),
                    'votos_depois_17h_TSE': 34393, 'pct_do_comparecimento': pct(34393, tot['comp']),
                    'pct_da_margem': pct(34393, tot['L'] - tot['R'])}
    log(f"E1 {R['E1_soma']['diferenca']}")

    # ---------------------------------------------------------------- E2 prorrogação
    lim_h = DIA[2].replace(hour=17, minute=15, second=59)
    lim_a = DIA[2].replace(hour=18, minute=30, second=0)
    lim_liminar = DIA[2].replace(hour=17, minute=3, second=0)

    def grupo(s):
        e = s['enc_br']
        if e is None:
            return 'sem_hora'
        if e <= lim_h:
            return 'no_horario'
        if e >= lim_a:
            return 'mantida_aberta'
        return 'intermediaria'

    br2 = {k: s for k, s in S[2].items() if not s['zz']}
    g2 = {k: grupo(s) for k, s in br2.items()}
    cont = collections.Counter(g2.values())
    por_uf = collections.defaultdict(collections.Counter)
    for k, g in g2.items():
        por_uf[k.split('|')[0]][g] += 1
    ja_enc = sum(1 for s in br2.values() if s['enc_br'] is not None and s['enc_br'] <= lim_liminar)
    ja_enc_comp = sum(s['comp'] for s in br2.values() if s['enc_br'] is not None and s['enc_br'] <= lim_liminar)
    E2 = {'secoes_brasil': len(br2), 'por_grupo': dict(cont),
          'comp_por_grupo': {g: sum(br2[k]['comp'] for k in br2 if g2[k] == g) for g in cont},
          'por_uf_mantida_aberta': {uf: c['mantida_aberta'] for uf, c in sorted(por_uf.items()) if c['mantida_aberta']},
          'por_uf_intermediaria': {uf: c['intermediaria'] for uf, c in sorted(por_uf.items()) if c['intermediaria']},
          'ja_encerradas_ate_17h03m00_brasilia': ja_enc, 'comp_ja_encerradas_ate_17h03': ja_enc_comp,
          'pct_secoes_ja_encerradas_ate_17h03': pct(ja_enc, len(br2))}
    # (b) municípios mistos
    mun = collections.defaultdict(collections.Counter)
    mun_comp = collections.Counter()
    for k, g in g2.items():
        m = '|'.join(k.split('|')[:2])
        mun[m][g] += 1
        mun_comp[m] += br2[k]['comp']
    mistos = [m for m, c in mun.items() if c['mantida_aberta'] and c['no_horario']]
    com_aberta = [m for m, c in mun.items() if c['mantida_aberta']]
    E2['municipios_com_secao_mantida_aberta'] = len(com_aberta)
    E2['municipios_mistos'] = len(mistos)
    E2['comparecimento_nos_mistos'] = sum(mun_comp[m] for m in mistos)
    E2['secoes_nos_mistos'] = {g: sum(mun[m][g] for m in mistos) for g in ('mantida_aberta', 'no_horario', 'intermediaria')}
    top = sorted(com_aberta, key=lambda m: -mun[m]['mantida_aberta'])[:15]
    nome_mun = {}
    for k, s in br2.items():
        nome_mun.setdefault('|'.join(k.split('|')[:2]), s['mun_nome'])
    E2['maiores_municipios_mantidas_abertas'] = [{'mun': m, 'nome': nome_mun.get(m), **dict(mun[m])} for m in top]
    # (c) por UF
    def fatia(ks, t):
        L = sum(S[t][k]['L'] for k in ks if k in S[t]); Rr = sum(S[t][k]['R'] for k in ks if k in S[t])
        return pct(L, L + Rr), L, Rr
    por_uf_c = {}
    for uf, c in sorted(por_uf.items()):
        if c['mantida_aberta'] < 50:
            continue
        ab = [k for k in br2 if g2[k] == 'mantida_aberta' and k.startswith(uf + '|') and k in S[1]]
        de = [k for k in br2 if g2[k] != 'mantida_aberta' and k.startswith(uf + '|') and k in S[1]]
        a2, aL2, aR2 = fatia(ab, 2); a1, aL1, aR1 = fatia(ab, 1)
        d2, _, _ = fatia(de, 2); d1, _, _ = fatia(de, 1)
        por_uf_c[uf] = {'mantidas_abertas': len(ab), 'L2_abertas': a2, 'L1_abertas': a1, 'virada_abertas': a2 - a1,
                        'L2_demais': d2, 'L1_demais': d1, 'virada_demais': d2 - d1,
                        'margem_L_abertas_2t': aL2 - aR2, 'ganho_liquido_L_abertas_2t_menos_1t': (aL2 - aR2) - (aL1 - aR1)}
    E2['por_uf_fatias'] = por_uf_c
    # (d) regressão
    ys, x, gs, ws = [], [], [], []
    for k, s2 in br2.items():
        s1 = S[1].get(k)
        if s1 is None or s2['enc_br'] is None:
            continue
        if s1['L'] + s1['R'] <= 0 or s2['L'] + s2['R'] <= 0:
            continue
        ys.append(100 * (s2['L'] / (s2['L'] + s2['R']) - s1['L'] / (s1['L'] + s1['R'])))
        x.append(1.0 if g2[k] == 'mantida_aberta' else 0.0)
        uf, mn, zona, _ = k.split('|')
        gs.append(f'{uf}|{mn}|{zona}|{s2["loc"]}')
        ws.append(s2['L'] + s2['R'])
    ys, x, ws, gs = np.asarray(ys), np.asarray(x), np.asarray(ws), np.asarray(gs)
    E2['regressao_fe_local'] = fe_ols(ys, x[:, None], gs, ws, ['mantida_aberta'])
    E2['regressao_fe_local']['n_mantida_aberta'] = int(x.sum())
    # (e) margem sem as mantidas abertas
    Lb = sum(s['L'] for s in br2.values()); Rb = sum(s['R'] for s in br2.values())
    La = sum(br2[k]['L'] for k in br2 if g2[k] == 'mantida_aberta'); Ra = sum(br2[k]['R'] for k in br2 if g2[k] == 'mantida_aberta')
    Ca = sum(br2[k]['comp'] for k in br2 if g2[k] == 'mantida_aberta')
    E2['margem_brasil'] = Lb - Rb
    E2['margem_sem_mantidas_abertas'] = (Lb - La) - (Rb - Ra)
    E2['margem_pior_caso'] = (Lb - Rb) - Ca
    E2['L_pct_mantidas_abertas'] = pct(La, La + Ra)
    R['E2_prorrogacao'] = E2
    log(f"E2 {cont} mistos {len(mistos)}")

    # ---------------------------------------------------------------- E3 pausa e rapidez
    recs = sorted(s['rec'] for s in S[2].values() if s['rec'] is not None)
    n = len(recs)
    ate_1707 = sum(1 for r in recs if r <= DIA[2].replace(hour=17, minute=7, second=59))
    gaps = [(recs[i + 1] - recs[i], recs[i], recs[i + 1]) for i in range(n - 1)
            if recs[i] >= DIA[2].replace(hour=17)]
    gmax = max(gaps)
    def q(p):
        return recs[min(n - 1, int(np.ceil(p * n)) - 1)].strftime('%H:%M:%S')
    R['E3_apuracao'] = {'secoes_com_recebimento': n, 'primeiro': recs[0].strftime('%H:%M:%S'),
                        'ate_17h07m59': ate_1707,
                        'maior_intervalo_sem_recebimento': {'de': gmax[1].strftime('%H:%M:%S'), 'ate': gmax[2].strftime('%H:%M:%S'),
                                                             'minutos': gmax[0].total_seconds() / 60},
                        'p50': q(0.5), 'p90': q(0.9), 'p99': q(0.99), 'p100': recs[-1].strftime('%H:%M:%S')}
    log(f"E3 {R['E3_apuracao']}")

    # ---------------------------------------------------------------- E4 dez milhões
    acc = collections.Counter()
    nL_exc = nR_exc = 0; excL = excR = 0
    nL_ganha_R_perde = 0
    n_mesmas = 0
    for k, v in base.items():
        a, b = v.get('1'), v.get('2')
        if not a or not b:
            continue
        n_mesmas += 1
        dL, dR = b['L'] - a['L'], b['R'] - a['R']
        bn1, bn2 = a['B'] + a['N'], b['B'] + b['N']
        dC = b['comp'] - a['comp']
        acc['dL'] += dL; acc['dR'] += dR; acc['O1'] += a['O']; acc['O2'] += b.get('O', 0)
        acc['BN1'] += bn1; acc['BN2'] += bn2; acc['C1'] += a['comp']; acc['C2'] += b['comp']
        acc['L1'] += a['L']; acc['R1'] += a['R']; acc['L2'] += b['L']; acc['R2'] += b['R']
        folga = a['O'] + max(0, bn1 - bn2) + max(0, dC)
        if dL > folga:
            nL_exc += 1; excL += dL - folga
        if dR > folga:
            nR_exc += 1; excR += dR - folga
        if dL > 0 and dR < 0:
            nL_ganha_R_perde += 1
    acc['identidade_dL_mais_dR'] = acc['dL'] + acc['dR']
    acc['identidade_O1_mais_quedaBN_mais_dC_menos_O2'] = acc['O1'] + (acc['BN1'] - acc['BN2']) + (acc['C2'] - acc['C1']) - acc['O2']
    R['E4_dez_milhoes'] = {'secoes_nos_dois_turnos': n_mesmas, 'contas': dict(acc),
                           'secoes_ganho_L_passa_folga': nL_exc, 'excesso_L_votos': excL,
                           'secoes_ganho_R_passa_folga': nR_exc, 'excesso_R_votos': excR,
                           'secoes_L_ganha_e_R_perde': nL_ganha_R_perde,
                           'L1_pct_validos_finalistas': pct(acc['L1'], acc['L1'] + acc['R1'] + acc['O1']),
                           'R1_pct_validos': pct(acc['R1'], acc['L1'] + acc['R1'] + acc['O1'])}
    log(f"E4 L exc {nL_exc} ({excL}) R exc {nR_exc} ({excR})")

    # ---------------------------------------------------------------- E5 indícios clássicos
    E5 = {}
    for t in ('1', '2'):
        c = collections.Counter(); ufs = collections.defaultdict(collections.Counter)
        for k, v in base.items():
            b = v.get(t)
            if not b or b['comp'] < 1:
                continue
            uf = k.split('|')[0]
            if b['R'] == 0 and b['L'] > 0:
                c['R_zero'] += 1; c['L_nas_R_zero'] += b['L']; ufs['R_zero'][uf] += 1
            if b['L'] == 0 and b['R'] > 0:
                c['L_zero'] += 1; c['R_nas_L_zero'] += b['R']; ufs['L_zero'][uf] += 1
            if b['comp'] > b['apt']:
                c['comp_acima_aptos'] += 1
            if b['comp'] == b['apt'] and b['apt'] >= 50:
                c['comp_igual_aptos_50mais'] += 1
        E5[t] = {**dict(c), 'ufs_R_zero': dict(ufs['R_zero'].most_common(8)), 'ufs_L_zero': dict(ufs['L_zero'].most_common(8))}
    # acrescentado depois da primeira rodada (declarado): as seções com Flávio zerado no 2º turno, como estavam no 1º
    z = [(k, v) for k, v in base.items() if v.get('2') and v['2']['comp'] >= 1 and v['2']['R'] == 0 and v['2']['L'] > 0]
    z1 = [v['1'] for _, v in z if v.get('1')]
    E5['R_zero_2t_no_1t'] = {'secoes': len(z), 'com_1t': len(z1), 'R1_zero_tambem': sum(1 for a in z1 if a['R'] == 0),
                             'R1_ate_2': sum(1 for a in z1 if a['R'] <= 2), 'R1_soma': sum(a['R'] for a in z1),
                             'L1_soma': sum(a['L'] for a in z1), 'O1_soma': sum(a['O'] for a in z1),
                             'L2_soma': sum(v['2']['L'] for _, v in z), 'comp2_soma': sum(v['2']['comp'] for _, v in z)}
    R['E5_classicos'] = E5
    log(f"E5 {E5['2']} {E5['R_zero_2t_no_1t']}")

    # ---------------------------------------------------------------- E6 auditorias
    E6 = {}
    lim1745 = DIA[2].replace(hour=17, minute=45, second=0)
    E6['urnas_brasil_encerradas_depois_17h45_brasilia'] = sum(1 for s in br2.values() if s['enc_br'] and s['enc_br'] > lim1745)
    E6['pct'] = pct(E6['urnas_brasil_encerradas_depois_17h45_brasilia'], len(br2))
    nh2 = sum(s['nh'] for s in S[2].values()); c2 = sum(s['comp'] for s in S[2].values())
    nh2b = sum(s['nh'] for s in br2.values()); c2b = sum(s['comp'] for s in br2.values())
    E6['sem_biometria_2t'] = {'todas': nh2, 'pct_comp_todas': pct(nh2, c2), 'brasil': nh2b, 'pct_comp_brasil': pct(nh2b, c2b)}
    cortes = [('local>17:00:00', 'loc', (17, 0, 0)), ('local>17:00:59', 'loc', (17, 0, 59)), ('local>17:05:59', 'loc', (17, 5, 59)),
              ('brasilia>17:00:59', 'br', (17, 0, 59)), ('brasilia>17:05:59', 'br', (17, 5, 59)), ('brasilia>17:15:59', 'br', (17, 15, 59))]
    rep = []
    for nome, campo, (hh, mm, ss) in cortes:
        lim = DIA[2].replace(hour=hh, minute=mm, second=ss)
        ks = [k for k, s in br2.items() if s['enc_' + campo] is not None and s['enc_' + campo] > lim and k in S[1]]
        L2 = sum(S[2][k]['L'] for k in ks); R2 = sum(S[2][k]['R'] for k in ks)
        L1 = sum(S[1][k]['L'] for k in ks); R1 = sum(S[1][k]['R'] for k in ks)
        r = {'corte': nome, 'secoes': len(ks), 'R_pct_2t': pct(R2, L2 + R2), 'margem_R_2t': R2 - L2,
             'R_pct_1t_mesmas': pct(R1, L1 + R1), 'margem_R_1t_mesmas': R1 - L1}
        r['reproduz'] = bool(abs(r['R_pct_2t'] - 52.40) <= 0.05 and abs(r['margem_R_2t'] - 1748468) <= 0.005 * 1748468)
        rep.append(r)
    E6['reproducao_52_40'] = rep
    nomeadas = {}
    alvo = [('SP', 'GUARULHOS', 395, 298), ('ES', 'SANTA MARIA DE JETIBÁ', 9, 85), ('ES', 'SANTA MARIA DE JETIBÁ', 9, 112)]
    for uf, nm, z, sc in alvo:
        for k, s in S[2].items():
            u, m, zz, ss = k.split('|')
            if u == uf and s['mun_nome'] == nm and int(zz) == z and int(ss) == sc:
                nomeadas[k] = {'nome': nm, 'apt': s['apt'], 'comp': s['comp'], 'L': s['L'], 'R': s['R'],
                               'enc_local': s['enc_loc'].strftime('%H:%M:%S') if s['enc_loc'] else None,
                               'tipo': s['tipo'], 'agregadas': s['agreg'], 'na_amostra_T3': k in t3,
                               'T3': t3.get(k)}
    for k in ('CE|14176|21|136',):
        s = S[2].get(k)
        nomeadas[k] = None if s is None else {'nome': s['mun_nome'], 'apt': s['apt'], 'comp': s['comp'], 'L': s['L'], 'R': s['R'],
                                              'enc_local': s['enc_loc'].strftime('%H:%M:%S') if s['enc_loc'] else None,
                                              'tipo': s['tipo'], 'agregadas': s['agreg'], 'na_amostra_T3': k in t3}
    sem = [k for k in bu[2] if k not in S[2]]
    nomeadas['bweb_2t_sem_base'] = {k: {'nome': bu[2][k].get('NM_MUNICIPIO'), 'aptos_bweb': bu[2][k].get('QT_APTOS'),
                                        'comp_bweb': bu[2][k].get('QT_COMPARECIMENTO'), 'tipo': bu[2][k].get('DS_TIPO_URNA')}
                                    for k in sem}
    E6['secoes_nomeadas'] = nomeadas
    # acrescentado depois da primeira rodada (declarado): exterior no bweb do 2º turno, para a frase "70 seções do
    # exterior sem boletim" (luiseduardoluz) contra "2 seções" (Mateus Costa Cruz)
    zz = {k: v for k, v in bu[2].items() if k.startswith('ZZ')}
    agreg = sum(len([x for x in (v.get('DS_SECOES_AGREGADAS') or '').replace('#NULO#', '').replace(';', ',').split(',') if x.strip()])
                for v in zz.values())
    E6['exterior_bweb_2t'] = {'secoes_no_bweb': len(zz), 'com_agregacao': sum(1 for v in zz.values() if (v.get('DS_SECOES_AGREGADAS') or '#NULO#') != '#NULO#'),
                              'secoes_agregadas_listadas': agreg, 'comp_zero': sum(1 for v in zz.values() if inteiro(v.get('QT_COMPARECIMENTO')) == 0)}
    E6['amostra_T3_secoes_com_log_diferente_do_bu'] = sum(1 for v in t3.values() if v.get('A1_dif_comp'))
    E6['amostra_T3_secoes'] = len(t3)
    R['E6_auditorias'] = E6
    log(f"E6 17h45 {E6['urnas_brasil_encerradas_depois_17h45_brasilia']} NH {E6['sem_biometria_2t']}")

    # ---------------------------------------------------------------- E7 transporte
    cap = {'SALVADOR': 'BA', 'SÃO PAULO': 'SP'}
    E7 = {}
    for t in (1, 2):
        acc7 = collections.defaultdict(lambda: [0, 0])
        for k, s in S[t].items():
            if s['zz'] or k not in S[3 - t]:
                continue
            uf = k.split('|')[0]
            nm = S[2][k]['mun_nome']
            if cap.get(nm) == uf:
                g = nm
            elif uf in ('BA', 'SP'):
                g = 'resto_' + uf
            else:
                g = 'outras_UFs'
            acc7[g][0] += s['comp']; acc7[g][1] += s['apt']
            acc7['brasil'][0] += s['comp']; acc7['brasil'][1] += s['apt']
        E7[str(t)] = {g: {'comp': c, 'apt': a, 'pct': pct(c, a)} for g, (c, a) in acc7.items()}
    E7['variacao_pontos'] = {g: E7['2'][g]['pct'] - E7['1'][g]['pct'] for g in E7['2']}
    R['E7_transporte'] = E7
    log(f"E7 {E7['variacao_pontos']}")

    with open(saida, 'w') as f:
        json.dump(R, f, ensure_ascii=False, indent=1, default=str)
    log(f'salvo {saida}')


if __name__ == '__main__':
    main()
