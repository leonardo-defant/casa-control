"""L8 do Adendo 18 (PRE-REGISTRO-2026-10-26.md): o "dossiê" dos EUA citado na imprensa, conferência das afirmações técnicas.

Registro (escrito antes de rodar, Adendo 18):
  "Achar o documento ou a reportagem, separar o que é afirmação técnica conferível nos dados públicos e conferir cada uma;
  o que não for conferível é relatado como tal."
  O L8 não tem limiar numérico; o veredito pela letra é DESCRITIVO. Cada afirmação sai como: confere com a base, não confere,
  ou não conferível (sem dado local).

O que a pesquisa achou (antes de rodar este script; fontes no texto de saída):
  Não há documento publicado. A origem é uma fala, numa análise ao vivo da CNN Brasil de 28/10/2026, de que o Departamento de
  Estado "já tem todo um dossiê pronto" sobre o que considera abusos no Brasil, repetida no mesmo dia por sites (Jornal da
  Cidade Online às 07h28, Topic News, Visão da Direita, Pagina1, Folha do Estado, Infoverus, Gazeta do Povo e outros). As
  afirmações técnicas sobre votos, urnas, apuração ou prorrogação atribuídas ao "dossiê" nessas reproduções são só estas:
    D1. a decisão de Zanin de "adiar o fechamento das urnas" / prorrogar a votação;
    D2. a ordem de Moraes para recolher os passaportes de Flávio "minutos depois" do anúncio da derrota (a parte técnica é a
        hora em que o resultado ficou definido);
    D3. "para Trump, quem venceu a eleição foi o senador Flávio Bolsonaro" (Jornal da Cidade Online, atribuído à CNN).
  O resto (corrupção de ministros do STF, prisões, narcotráfico, ações militares) não trata de votos nem de urnas e não é
  conferível com a base.
  Vizinhas, que as mesmas matérias citam como contexto (não são do "dossiê"; conferidas à parte e marcadas como tal):
    V1. Trump, 26/10: "The extension given was very strange" (mesma conta de D1);
    V2. Trump, 26/10: "the way it was tabulated" e a pausa da totalização das 17h06 às 19h (TSE: 1.225 de 499.248 seções
        apuradas na pausa, Lula com 57,66% nessa parcial; números do arquivo de contexto já verificado);
    V3. carta de Flávio (28/10): Zanin "permitiu" que Lula ganhasse "mais de 10 milhões de votos".

Especificação fixada aqui antes de rodar (leituras declaradas):
  E1. Fuso: o mesmo do L1 (hora cheia modal da abertura do município no turno; deslocamento o = hora modal - 8; hora de
      Brasília = hora local da urna - o). DT_BU_RECEBIDO já está em hora de Brasília (verificado no L1). Exterior (ZZ) fica
      fora das contas da prorrogação (a liminar valeu no Brasil, e lá a votação é das 8h às 17h locais) e entra nas contas da
      apuração.
  E2. D1/V1/V3 (prorrogação). Cortes de encerramento em hora de Brasília: depois de 17:00:59, 17:05:59, 17:15:59, 17:59:59,
      18:59:59. Para cada corte, no 2º turno: seções e comparecimento que encerraram depois do corte; votos de Lula (13) e
      Flávio (22) nelas; a margem de Lula sem essas seções (todas as seções retiradas por inteiro, inclusive os votos dados
      antes das 17h: limite superior do efeito da prorrogação) e a margem no pior caso (todo o comparecimento dessas seções
      contado como voto líquido de Lula a retirar). O bweb não diz quantos votos vieram depois das 17h; isso só os logs dão.
      Comparação descritiva com o 1º turno de 2026 (mesma eleição, sem prorrogação): as mesmas contas nas mesmas seções.
  E3. D1, leitura de seção (descritivo): y = virada de Lula na seção, 100 [L2/(L2+R2) - L1/(L1+R1)]; x = 1 se a seção
      encerrou o 2º turno depois de 17:15:59 de Brasília; efeito fixo do local de votação do 2º turno; peso L2+R2; erro
      agrupado por local. (b) o mesmo com o indicador de encerramento depois de 17:15:59 no 1º turno como controle (fila
      habitual do local). Sem limiar: o registro do L8 não tem.
  E4. V2 (pausa). Distribuição de DT_BU_RECEBIDO no 2º turno: boletins recebidos até 17:06:59 e até 17:07:59; recebidos
      de 17:08:00 a 18:59:59; primeiro recebimento depois disso. Fatia de Lula nos válidos (L+R) entre os recebidos até
      17:06:59 e até 17:07:59, e UFs deles. Compara com 1.225 seções e 57,66%. O 1º turno sai ao lado.
      Acrescentado depois da primeira rodada (pós-registro, declarado): a fatia de Lula nos 1.225 primeiros boletins
      recebidos e a hora do 1.225º; e, para "the way it was tabulated", a virada de Lula na seção (definida em E3) por
      décimo da ordem de chegada do boletim ao TSE no 2º turno e a regressão da virada contra a posição na fila de chegada
      (0 = primeiro, 1 = último), com efeito fixo de local, peso L2+R2 e erro agrupado por local. Uma inserção de votos
      no fim da apuração apareceria como virada maior nos boletins que chegaram por último dentro do mesmo local.
  E5. D2 (hora em que o resultado ficou definido). Ordenando as seções do 2º turno por DT_BU_RECEBIDO: (a) primeiro instante
      em que a margem de Lula entre os recebidos passa a soma dos eleitores aptos das seções ainda não recebidas (definição sem
      olhar o futuro); (b) o mesmo com o comparecimento final das não recebidas (com o futuro); (c) horários de 50%, 90%, 99%,
      99,9% e 100% das seções recebidas. Compara com os horários da imprensa: TSE confirma 21h09, pedido da PF 21h16 (O Globo,
      conferido em checagem anterior).
  E6. D3 (quem venceu). Soma de todos os boletins do 2º turno: votos de Lula e de Flávio, margem, contra o total oficial do TSE
      (64.256.232 e 59.826.041). Também quem lidera entre as seções encerradas até 17:00:59 de Brasília (recorte por horário,
      que seleciona seções; descritivo).

Uso: python3 -I analisar_L8.py <cache_L1_dir> <zips1t_dir> <zips2t_dir> <secoes2026.json.gz> <saida.json>
(o texto com a pesquisa e as fontes fica em resultados/L8_dossie_eua.txt, escrito à parte)
"""
import os as _os, sys as _sys
_sys.path.insert(0, _os.path.dirname(_os.path.abspath(__file__)))
import collections, datetime as dt, json, math, sys
import numpy as np
from lib import carregar, fe_ols
from analisar_L1 import ler_ou_extrair, p_dt, fz, fi, log

DIA = {1: dt.datetime(2026, 10, 4), 2: dt.datetime(2026, 10, 25)}
CORTES = [('17:00:59', (17, 0, 59)), ('17:05:59', (17, 5, 59)), ('17:15:59', (17, 15, 59)),
          ('17:59:59', (17, 59, 59)), ('18:59:59', (18, 59, 59))]
OFICIAL = {'L': 64256232, 'R': 59826041}


def pct(a, b):
    return 100.0 * a / b if b else float('nan')


def main():
    cache, zdir1, zdir2, base_path, saida_json = sys.argv[1:6]
    bu = {1: ler_ou_extrair(1, zdir1, cache), 2: ler_ou_extrair(2, zdir2, cache)}
    base = carregar(base_path)
    log(f'seções bweb: 1T {len(bu[1])}, 2T {len(bu[2])}; base {len(base)}')
    R = {'registro': __doc__.split('Uso:')[0]}

    # ------------------------------------------------ fuso (E1, igual ao L1)
    mh = {1: collections.defaultdict(collections.Counter), 2: collections.defaultdict(collections.Counter)}
    for t in (1, 2):
        for k, v in bu[t].items():
            ab = p_dt(v.get('DT_ABERTURA'))
            junta = v.get('NR_JUNTA_APURADORA', '-1') not in ('-1', '')
            if ab is not None and not junta:
                uf, mun = k.split('|')[:2]
                mh[t][(uf, mun)][ab.hour] += 1
    modal = {t: {m: c.most_common(1)[0][0] for m, c in mh[t].items()} for t in (1, 2)}

    def off(t, k):
        uf, mun = k.split('|')[:2]
        hm = modal[t].get((uf, mun))
        if hm is None:
            hm = modal[3 - t].get((uf, mun), 8)
        return hm - 8

    # ------------------------------------------------ tabela por seção
    S = {1: {}, 2: {}}
    sem_base = {1: [], 2: []}
    for t in (1, 2):
        for k, v in bu[t].items():
            b = base.get(k, {}).get(str(t))
            if b is None:
                sem_base[t].append(k)
                continue
            enc = p_dt(v.get('DT_ENCERRAMENTO'))
            o = off(t, k)
            S[t][k] = {'enc_br': (enc - dt.timedelta(hours=o)) if enc else None, 'rec': p_dt(v.get('DT_BU_RECEBIDO')),
                       'apt': int(v.get('QT_APTOS') or 0), 'comp': b['comp'], 'L': b['L'], 'R': b['R'], 'loc': b['loc'],
                       'zz': k.startswith('ZZ'), 'junta': v.get('NR_JUNTA_APURADORA', '-1') not in ('-1', ''), 'off': o}
    R['seções'] = {'bweb_1t': len(bu[1]), 'bweb_2t': len(bu[2]), 'base': len(base),
                   'bweb_sem_base_1t': sem_base[1], 'bweb_sem_base_2t': sem_base[2]}
    R['fuso_deslocamentos_2t'] = dict(collections.Counter(str(s['off']) + ('|ZZ' if s['zz'] else '') for s in S[2].values()))

    # ------------------------------------------------ E6 (D3): quem venceu
    L2 = sum(s['L'] for s in S[2].values()); R2 = sum(s['R'] for s in S[2].values())
    C2 = sum(s['comp'] for s in S[2].values())
    R['D3_resultado'] = {'L': L2, 'R': R2, 'margem': L2 - R2, 'comparecimento': C2, 'L_pct_validos': pct(L2, L2 + R2),
                         'oficial_L': OFICIAL['L'], 'oficial_R': OFICIAL['R'],
                         'dif_L': L2 - OFICIAL['L'], 'dif_R': R2 - OFICIAL['R'],
                         'secoes_lula_na_frente': sum(1 for s in S[2].values() if s['L'] > s['R']),
                         'secoes_flavio_na_frente': sum(1 for s in S[2].values() if s['R'] > s['L']),
                         'secoes_empate': sum(1 for s in S[2].values() if s['R'] == s['L'])}

    # ------------------------------------------------ E2 (D1, V1, V3): prorrogação
    def bloco_cortes(t):
        out = []
        br = [(k, s) for k, s in S[t].items() if not s['zz']]
        Lt = sum(s['L'] for _, s in br); Rt = sum(s['R'] for _, s in br); Ct = sum(s['comp'] for _, s in br)
        sem_enc = [k for k, s in br if s['enc_br'] is None]
        for nome, (hh, mm, ss) in CORTES:
            lim = DIA[t].replace(hour=hh, minute=mm, second=ss)
            tarde = [s for _, s in br if s['enc_br'] is not None and s['enc_br'] > lim]
            Lx = sum(s['L'] for s in tarde); Rx = sum(s['R'] for s in tarde); Cx = sum(s['comp'] for s in tarde)
            out.append({'corte_brasilia': nome, 'secoes_depois': len(tarde), 'comp_depois': Cx, 'L_depois': Lx, 'R_depois': Rx,
                        'L_pct_validos_depois': pct(Lx, Lx + Rx),
                        'L_pct_validos_ate_o_corte': pct(Lt - Lx, (Lt - Lx) + (Rt - Rx)),
                        'margem_sem_essas_secoes': (Lt - Lx) - (Rt - Rx),
                        'margem_pior_caso_comp_todo_lula': (Lt - Rt) - Cx,
                        'comp_depois_pct_do_comp': pct(Cx, Ct)})
        return {'L': Lt, 'R': Rt, 'comp': Ct, 'margem_brasil_sem_exterior': Lt - Rt, 'secoes_sem_encerramento': len(sem_enc),
                'cortes': out}
    R['D1_prorrogacao'] = {'2t': bloco_cortes(2), '1t_mesma_eleicao_sem_prorrogacao': bloco_cortes(1)}
    # mesmas seções nos dois turnos: atraso do encerramento no 2º turno contra o 1º
    lim1 = DIA[1].replace(hour=17, minute=15, second=59); lim2 = DIA[2].replace(hour=17, minute=15, second=59)
    tab = collections.Counter()
    for k, s2 in S[2].items():
        s1 = S[1].get(k)
        if s1 is None or s2['zz'] or s1['enc_br'] is None or s2['enc_br'] is None:
            continue
        tab[(s1['enc_br'] > lim1, s2['enc_br'] > lim2)] += 1
    R['D1_prorrogacao']['mesmas_secoes_tarde_1t_x_tarde_2t_corte_17h15'] = {f'1t_{a}|2t_{b}': n for (a, b), n in tab.items()}
    # distribuição do encerramento em Brasília por faixa de 15 min, 16h45 a 19h15
    def faixas(t):
        c = collections.Counter()
        for s in S[t].values():
            if s['zz'] or s['enc_br'] is None:
                continue
            e = s['enc_br']
            mins = (e - DIA[t]).total_seconds() / 60
            if mins < 16 * 60 + 45:
                c['antes_16h45'] += 1
            elif mins >= 19 * 60 + 15:
                c['19h15_ou_depois'] += 1
            else:
                b0 = int((mins - (16 * 60 + 45)) // 15) * 15 + 16 * 60 + 45
                c[f'{b0 // 60:02d}h{b0 % 60:02d}'] += 1
        return dict(sorted(c.items()))
    R['D1_prorrogacao']['faixas_encerramento_brasilia'] = {'1t': faixas(1), '2t': faixas(2)}
    ult = max((s['enc_br'], k) for k, s in S[2].items() if not s['zz'] and s['enc_br'] is not None)
    R['D1_prorrogacao']['ultimo_encerramento_2t'] = {'secao': ult[1], 'brasilia': ult[0].strftime('%d/%m %H:%M:%S')}

    # E3: leitura de seção
    ys, x2, x1, gs, ws = [], [], [], [], []
    for k, s2 in S[2].items():
        s1 = S[1].get(k)
        if s1 is None or s2['zz'] or s2['enc_br'] is None or s1['enc_br'] is None:
            continue
        if s1['L'] + s1['R'] <= 0 or s2['L'] + s2['R'] <= 0:
            continue
        ys.append(100 * (s2['L'] / (s2['L'] + s2['R']) - s1['L'] / (s1['L'] + s1['R'])))
        x2.append(1.0 if s2['enc_br'] > lim2 else 0.0)
        x1.append(1.0 if s1['enc_br'] > lim1 else 0.0)
        uf, mun, zona, _ = k.split('|')
        gs.append(f'{uf}|{mun}|{zona}|{s2["loc"]}')
        ws.append(s2['L'] + s2['R'])
    ys, x2, x1, ws = map(np.asarray, (ys, x2, x1, ws))
    gs = np.asarray(gs)
    ra = fe_ols(ys, x2[:, None], gs, ws, ['tarde_2t'])
    rb = fe_ols(ys, np.column_stack([x2, x1]), gs, ws, ['tarde_2t', 'tarde_1t'])
    R['D1_secao'] = {'a_so_tarde_2t': ra, 'b_com_tarde_1t': rb, 'n_secoes': int(len(ys)), 'n_tarde_2t': int(x2.sum()),
                     'n_tarde_1t': int(x1.sum()),
                     'virada_media_ponderada_tarde_2t': float((ys * ws)[x2 == 1].sum() / ws[x2 == 1].sum()),
                     'virada_media_ponderada_demais': float((ys * ws)[x2 == 0].sum() / ws[x2 == 0].sum())}

    # V3: "mais de 10 milhões" de Lula pela prorrogação
    L1b = sum(S[1][k]['L'] for k in S[2] if k in S[1]); L2b = sum(S[2][k]['L'] for k in S[2] if k in S[1])
    ganho_tarde = {}
    for nome, (hh, mm, ss) in CORTES:
        lim = DIA[2].replace(hour=hh, minute=mm, second=ss)
        ks = [k for k, s in S[2].items() if not s['zz'] and s['enc_br'] is not None and s['enc_br'] > lim and k in S[1]]
        ganho_tarde[nome] = {'ganho_lula_nessas_secoes': sum(S[2][k]['L'] - S[1][k]['L'] for k in ks),
                             'ganho_flavio_nessas_secoes': sum(S[2][k]['R'] - S[1][k]['R'] for k in ks),
                             'comp_2t_nessas_secoes': sum(S[2][k]['comp'] for k in ks)}
    R['V3_dez_milhoes'] = {'ganho_lula_total_mesmas_secoes': L2b - L1b, 'por_corte': ganho_tarde}

    # ------------------------------------------------ E4 (V2): pausa da totalização
    def recebimento(t):
        rr = sorted((s['rec'], k) for k, s in S[t].items() if s['rec'] is not None)
        dia = DIA[t]
        a = dia.replace(hour=17, minute=6, second=59); b = dia.replace(hour=17, minute=7, second=59)
        c = dia.replace(hour=18, minute=59, second=59)
        ate_a = [k for r, k in rr if r <= a]; ate_b = [k for r, k in rr if r <= b]
        meio = [k for r, k in rr if b < r <= c]
        depois = [(r, k) for r, k in rr if r > c]

        def resumo(ks):
            Lx = sum(S[t][k]['L'] for k in ks); Rx = sum(S[t][k]['R'] for k in ks)
            ufs = collections.Counter(k.split('|')[0] for k in ks)
            return {'secoes': len(ks), 'L': Lx, 'R': Rx, 'L_pct_validos': pct(Lx, Lx + Rx), 'ufs': dict(ufs.most_common())}
        por_min = collections.Counter(r.strftime('%H:%M') for r, _ in rr if dia.replace(hour=16, minute=55) <= r <= dia.replace(hour=19, minute=10))
        return {'primeiro': rr[0][0].strftime('%d/%m %H:%M:%S') if rr else None,
                'ultimo': rr[-1][0].strftime('%d/%m %H:%M:%S') if rr else None,
                'sem_recebimento': len(S[t]) - len(rr),
                'ate_17h06m59': resumo(ate_a), 'ate_17h07m59': resumo(ate_b), 'de_17h08_a_18h59m59': resumo(meio),
                'primeiro_depois_de_18h59m59': depois[0][0].strftime('%d/%m %H:%M:%S') if depois else None,
                'por_minuto_16h55_19h10': dict(sorted(por_min.items()))}
    rr2 = sorted((s['rec'], k) for k, s in S[2].items() if s['rec'] is not None)
    k1225 = [k for _, k in rr2[:1225]]
    L_ = sum(S[2][k]['L'] for k in k1225); R_ = sum(S[2][k]['R'] for k in k1225)
    primeiras = {'secoes': 1225, 'hora_do_1225o': rr2[1224][0].strftime('%d/%m %H:%M:%S'), 'L': L_, 'R': R_,
                 'L_pct_validos': pct(L_, L_ + R_), 'ufs': dict(collections.Counter(k.split('|')[0] for k in k1225).most_common())}
    # virada por ordem de chegada
    pos = {k: i / (len(rr2) - 1) for i, (_, k) in enumerate(rr2)}
    yv, xv, gv, wv = [], [], [], []
    for k, s2 in S[2].items():
        s1 = S[1].get(k)
        if s1 is None or s2['zz'] or k not in pos or s1['L'] + s1['R'] <= 0 or s2['L'] + s2['R'] <= 0:
            continue
        yv.append(100 * (s2['L'] / (s2['L'] + s2['R']) - s1['L'] / (s1['L'] + s1['R'])))
        xv.append(pos[k])
        uf, mun, zona, _ = k.split('|')
        gv.append(f'{uf}|{mun}|{zona}|{s2["loc"]}')
        wv.append(s2['L'] + s2['R'])
    yv, xv, wv = map(np.asarray, (yv, xv, wv)); gv = np.asarray(gv)
    dec = np.minimum((xv * 10).astype(int), 9)
    por_dec = {}
    for d_ in range(10):
        m = dec == d_
        por_dec[f'd{d_ + 1}'] = {'secoes': int(m.sum()), 'virada_media_ponderada': float((yv * wv)[m].sum() / wv[m].sum())}
    reg_ordem = fe_ols(yv, xv[:, None], gv, wv, ['posicao_na_chegada'])
    R['V2_ordem_de_chegada'] = {'por_decimo': por_dec, 'regressao_fe_local': reg_ordem}
    R['V2_pausa'] = {'2t': recebimento(2), '1t': recebimento(1), 'primeiros_1225_recebidos_2t': primeiras,
                     'referencia_imprensa': {'secoes': 1225, 'total_secoes': 499248, 'L_pct_validos': 57.66,
                                             'fonte': 'Agência Brasil e TSE, via resultados/contexto_2t_2026_e_onde_estaria_a_fraude.txt'}}

    # ------------------------------------------------ E5 (D2): quando o resultado ficou definido
    rr = sorted((s['rec'], k) for k, s in S[2].items() if s['rec'] is not None)
    apt_rest = sum(S[2][k]['apt'] for _, k in rr); comp_rest = sum(S[2][k]['comp'] for _, k in rr)
    marg = 0; t_apt = t_comp = None; n = len(rr); marcos = {}
    alvo = {0.5: '50%', 0.9: '90%', 0.99: '99%', 0.999: '99,9%', 1.0: '100%'}
    for i, (r, k) in enumerate(rr, 1):
        s = S[2][k]
        marg += s['L'] - s['R']; apt_rest -= s['apt']; comp_rest -= s['comp']
        if t_apt is None and marg > apt_rest:
            t_apt = (r, i, marg, apt_rest)
        if t_comp is None and marg > comp_rest:
            t_comp = (r, i, marg, comp_rest)
        for f, nome in alvo.items():
            if nome not in marcos and i >= math.ceil(f * n):
                marcos[nome] = r.strftime('%d/%m %H:%M:%S')

    def fmt(x):
        return None if x is None else {'hora': x[0].strftime('%d/%m %H:%M:%S'), 'secoes_recebidas': x[1],
                                       'pct_secoes': pct(x[1], n), 'margem_lula': x[2], 'resto': x[3]}
    # margem em instantes fixos
    inst = {}
    for hh, mm in ((19, 30), (20, 0), (20, 30), (21, 0), (21, 9), (21, 16)):
        lim = DIA[2].replace(hour=hh, minute=mm, second=59)
        ks = [k for r, k in rr if r <= lim]
        Lx = sum(S[2][k]['L'] for k in ks); Rx = sum(S[2][k]['R'] for k in ks)
        inst[f'{hh:02d}h{mm:02d}'] = {'secoes': len(ks), 'pct_secoes': pct(len(ks), n), 'L_pct_validos': pct(Lx, Lx + Rx),
                                     'margem_lula': Lx - Rx,
                                     'aptos_nao_recebidos': sum(S[2][k]['apt'] for r, k in rr if r > lim)}
    R['D2_definicao'] = {'sem_olhar_o_futuro_aptos': fmt(t_apt), 'com_o_futuro_comparecimento': fmt(t_comp),
                         'marcos_recebimento': marcos, 'instantes': inst,
                         'referencia_imprensa': {'tse_confirma': '21h09', 'pedido_pf': '21h16',
                                                 'fonte': 'O Globo, via checagens/relatorio_pericial_instagram/checagem_e_conferencias.json'}}

    # D3 por recorte de horário: quem lidera entre as seções encerradas até 17:00:59 (Brasil)
    lim = DIA[2].replace(hour=17, minute=0, second=59)
    ate = [s for s in S[2].values() if not s['zz'] and s['enc_br'] is not None and s['enc_br'] <= lim]
    La = sum(s['L'] for s in ate); Ra = sum(s['R'] for s in ate)
    R['D3_resultado']['recorte_encerradas_ate_17h00m59_brasil'] = {'secoes': len(ate), 'L': La, 'R': Ra, 'margem': La - Ra,
                                                                    'L_pct_validos': pct(La, La + Ra)}

    with open(saida_json, 'w') as f:
        json.dump(R, f, ensure_ascii=False, indent=1, default=str)
    log(f'gravado {saida_json}')
    print(json.dumps({k: v for k, v in R.items() if k != 'registro'}, ensure_ascii=False, indent=1, default=str)[:20000])


if __name__ == '__main__':
    main()
