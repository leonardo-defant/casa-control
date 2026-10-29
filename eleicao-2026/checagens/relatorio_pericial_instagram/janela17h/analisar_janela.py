"""Confere os capítulos 1 e 2 do "Relatório Pericial Independente" (janela de encerramento das 17h).

Uso: python3 -I analisar_janela.py <secoes2026.json.gz> <horas2t.json.gz> <nh_secoes_2026.json.gz> <T3_logs.json>
                                   <secoes2022.json.gz> <secoes2018.json.gz> <saida.json>
Cada base é lida uma vez.
Relógios:
  local  = DT_ENCERRAMENTO como gravado (relógio da urna, hora local).
  prazo  = local deslocado pela hora modal de abertura do município: enc + (8 - hora_modal_abertura) h.
           No Brasil (2022 e 2026) isso é a hora de Brasília; no exterior (abertura 8h locais) fica a hora local,
           que é a do prazo legal lá. Em 2018 o prazo era 17h locais em todo lugar, então só o relógio local vale.
Janelas: J0 ate 17:00:59, J1 17:01:00 a 17:15:59, J2 17:16:00 a 18:59:59, J3 19:00:00 ou depois, SH sem horário.
"""
import collections as C, gzip, json, sys

JAN = ['J0_ate_17h00', 'J1_17h01_17h15', 'J2_17h16_18h59', 'J3_19h00_ou_mais', 'SH_sem_horario']


def seg(h):
    if not h or len(h) != 8 or not h[:2].isdigit():
        return None
    hh, mm, ss = h.split(':')
    return int(hh) * 3600 + int(mm) * 60 + int(ss)


def janela(s, corte0=17 * 3600 + 59):
    if s is None:
        return JAN[4]
    if s <= corte0:
        return JAN[0]
    if s < 17 * 3600 + 16 * 60:
        return JAN[1]
    if s < 19 * 3600:
        return JAN[2]
    return JAN[3]


def novo():
    return dict(secoes=0, apt=0, comp=0, L=0, R=0, O=0, B=0, N=0, NH=0, comp_nh=0)


def soma(acc, s, nh=None):
    acc['secoes'] += 1
    for c in ('apt', 'comp', 'L', 'R', 'O', 'B', 'N'):
        acc[c] += s.get(c, 0)
    if nh is not None:
        acc['NH'] += nh; acc['comp_nh'] += s['comp']


def fecha(acc):
    v = acc['L'] + acc['R'] + acc['O']
    out = dict(acc)
    out['validos'] = v
    out['pct_L_validos'] = round(100 * acc['L'] / v, 3) if v else None
    out['pct_R_validos'] = round(100 * acc['R'] / v, 3) if v else None
    out['pct_L_dois'] = round(100 * acc['L'] / (acc['L'] + acc['R']), 3) if acc['L'] + acc['R'] else None
    out['margem_L_menos_R'] = acc['L'] - acc['R']
    out['pct_NH'] = round(100 * acc['NH'] / acc['comp_nh'], 3) if acc['comp_nh'] else None
    out.pop('comp_nh')
    return out


def offsets(base, t):
    """Hora modal de abertura por município, no turno t."""
    cnt = C.defaultdict(C.Counter)
    for k, d in base.items():
        s = d.get(t)
        if s and s.get('ab') and s['ab'][:2].isdigit():
            uf, mun = k.split('|')[:2]
            cnt[(uf, mun)][int(s['ab'][:2])] += 1
    off = {m: 8 - c.most_common(1)[0][0] for m, c in cnt.items()}
    return off


def cortes(base, t, off, relogio, nh=None, corte0=17 * 3600 + 59):
    """Totais por janela (nacional e por UF) para o turno t no relógio dado."""
    tot = {j: novo() for j in JAN}
    uf_ = C.defaultdict(lambda: {j: novo() for j in JAN})
    jan_sec = {}
    for k, d in base.items():
        s = d.get(t)
        if not s:
            continue
        uf, mun = k.split('|')[:2]
        e = seg(s.get('enc'))
        if e is not None and relogio == 'prazo':
            e += 3600 * off.get((uf, mun), 0)
        j = janela(e, corte0)
        jan_sec[k] = j
        x = nh.get(k) if nh else None
        soma(tot[j], s, x); soma(uf_[uf][j], s, x)
    return ({j: fecha(v) for j, v in tot.items()},
            {u: {j: fecha(v) for j, v in d.items() if v['secoes']} for u, d in sorted(uf_.items())}, jan_sec)


def resumo_ate_depois(tot):
    a = tot[JAN[0]]
    dep = novo()
    for j in JAN[1:4]:
        for c in ('secoes', 'apt', 'comp', 'L', 'R', 'O', 'B', 'N'):
            dep[c] += tot[j][c]
    return {'ate_17h00': a, 'depois_17h00': fecha(dep)}


def histograma_minuto(base, t, off, relogio):
    """Seções e comparecimento por minuto de encerramento entre 16:50 e 17:20 e por hora cheia."""
    m = C.Counter(); mc = C.Counter(); h = C.Counter()
    for k, d in base.items():
        s = d.get(t)
        if not s:
            continue
        e = seg(s.get('enc'))
        if e is None:
            continue
        if relogio == 'prazo':
            uf, mun = k.split('|')[:2]
            e += 3600 * off.get((uf, mun), 0)
        h[e // 3600] += 1
        mi = e // 60
        if 16 * 60 + 50 <= mi <= 17 * 60 + 20:
            m[f'{mi // 60:02d}:{mi % 60:02d}'] += 1; mc[f'{mi // 60:02d}:{mi % 60:02d}'] += s['comp']
    return {'por_minuto_secoes': dict(sorted(m.items())), 'por_minuto_comp': dict(sorted(mc.items())),
            'por_hora_secoes': {f'{k:02d}h': v for k, v in sorted(h.items())}}


def mesmas_secoes(base, jan2, t_a, t_b):
    """Para as seções classificadas pela janela do turno t_b (jan2), votos de t_a e t_b nas mesmas seções."""
    acc = {j: {'a': novo(), 'b': novo()} for j in JAN}
    for k, j in jan2.items():
        d = base[k]
        if t_a in d and t_b in d:
            soma(acc[j]['a'], d[t_a]); soma(acc[j]['b'], d[t_b])
    out = {}
    for j in JAN:
        a, b = fecha(acc[j]['a']), fecha(acc[j]['b'])
        if not a['secoes']:
            continue
        out[j] = {'secoes': a['secoes'], 'turno_' + t_a: a, 'turno_' + t_b: b,
                  'var_pct_L_dois_pts': round(b['pct_L_dois'] - a['pct_L_dois'], 3) if a['pct_L_dois'] is not None else None}
    return out


def swing_dentro(base, jan2, chave_grupo, alvo):
    """Variação da fatia de Lula (dois candidatos) do 1º para o 2º turno nas seções da janela alvo, menos a variação
    das demais seções do mesmo grupo (município ou local), ponderada pelo comparecimento do 2º turno."""
    g = C.defaultdict(lambda: {'in': [0, 0, 0, 0, 0], 'out': [0, 0, 0, 0, 0]})
    for k, j in jan2.items():
        d = base[k]
        if '1' not in d or '2' not in d:
            continue
        s1, s2 = d['1'], d['2']
        if s1['L'] + s1['R'] == 0 or s2['L'] + s2['R'] == 0:
            continue
        gk = chave_grupo(k, s2)
        lado = 'in' if j in alvo else 'out'
        x = g[gk][lado]
        x[0] += s1['L']; x[1] += s1['L'] + s1['R']; x[2] += s2['L']; x[3] += s2['L'] + s2['R']; x[4] += s2['comp']
    num = den = 0; ng = 0; dif_in = dif_out = 0
    for gk, v in g.items():
        a, b = v['in'], v['out']
        if a[1] == 0 or b[1] == 0 or a[3] == 0 or b[3] == 0:
            continue
        sw_in = a[2] / a[3] - a[0] / a[1]
        sw_out = b[2] / b[3] - b[0] / b[1]
        w = a[4]
        num += w * (sw_in - sw_out); den += w; ng += 1
        dif_in += w * sw_in; dif_out += w * sw_out
    return {'grupos_com_as_duas': ng, 'comp_2t_na_janela': den,
            'swing_janela_pts': round(100 * dif_in / den, 3) if den else None,
            'swing_resto_do_grupo_pts': round(100 * dif_out / den, 3) if den else None,
            'diferenca_pts': round(100 * num / den, 3) if den else None}


def nh_por_janela_dentro(base, jan2, nh2, chave_grupo, alvo):
    """Taxa de NH (2º turno) nas seções da janela alvo contra o resto do mesmo grupo, ponderada pelo comparecimento."""
    g = C.defaultdict(lambda: {'in': [0, 0], 'out': [0, 0]})
    for k, j in jan2.items():
        x = nh2.get(k)
        if x is None:
            continue
        s2 = base[k]['2']
        lado = 'in' if j in alvo else 'out'
        g[chave_grupo(k, s2)][lado][0] += x; g[chave_grupo(k, s2)][lado][1] += s2['comp']
    tin = tout = w = 0; ng = 0
    for v in g.values():
        a, b = v['in'], v['out']
        if a[1] == 0 or b[1] == 0:
            continue
        tin += a[0]; tout += a[1] * b[0] / b[1]; w += a[1]; ng += 1
    return {'grupos': ng, 'comp_janela': w, 'pct_NH_janela': round(100 * tin / w, 3) if w else None,
            'pct_NH_resto_mesmo_grupo_ponderado': round(100 * tout / w, 3) if w else None}


def main():
    a26, ah, anh, alogs, a22, a18, saida = sys.argv[1:8]
    R = {}
    # ---------------- 2026 ----------------
    with gzip.open(a26, 'rt') as f:
        b26 = json.load(f)
    with gzip.open(ah, 'rt') as f:
        horas = json.load(f)
    with gzip.open(anh, 'rt') as f:
        nhc = json.load(f)
    nh1 = {k: v[3] for k, v in nhc['1'].items() if v[3] is not None}
    nh2 = {k: v[3] for k, v in nhc['2'].items() if v[3] is not None}
    del nhc
    # conferência: enc da base = hora do zip
    dif = sum(1 for k, v in horas.items() if b26.get(k, {}).get('2', {}).get('enc', '') != v[1][-8:])
    datas = C.Counter(v[1][:10] for v in horas.values())
    R['conferencia_2026'] = {'secoes_2t_base': sum(1 for d in b26.values() if '2' in d), 'secoes_zip': len(horas),
                             'enc_diferente_base_zip': dif, 'datas_encerramento_2t': dict(datas)}
    tot2 = novo()
    for d in b26.values():
        if '2' in d:
            soma(tot2, d['2'])
    R['totais_2t_2026'] = fecha(tot2)
    off26_2 = offsets(b26, '2'); off26_1 = offsets(b26, '1')
    esperado = {'AC': {2}, 'AM': {1, 2}, 'RO': {1}, 'RR': {1}, 'MT': {1}, 'MS': {1}}
    fora = {f'{u}|{m}': o for (u, m), o in off26_2.items() if u != 'ZZ' and o not in esperado.get(u, {0} if u != 'PE' else {0, -1})}
    R['deslocamentos_2026_2t'] = {'por_uf': {u: sorted({o for (uu, m), o in off26_2.items() if uu == u}) for u in sorted({u for u, m in off26_2})},
                                  'municipios_fora_do_esperado': fora,
                                  'municipios_por_deslocamento': dict(C.Counter(off26_2.values()))}
    # nomes dos municípios
    nomes = {}
    for k, v in horas.items():
        uf, mun = k.split('|')[:2]
        nomes[f'{uf}|{mun}'] = v[6]
    R['municipios_deslocamento_nao_zero_2026'] = {f'{u}|{m}': [nomes.get(f'{u}|{m}'), o] for (u, m), o in off26_2.items() if o not in (0,) and u != 'ZZ' and o != 1}
    for rel in ('local', 'prazo'):
        tot, ufs, jan = cortes(b26, '2', off26_2, rel, nh2)
        R[f'2026_2t_{rel}'] = {'janelas': tot, 'ate_depois': resumo_ate_depois(tot), 'por_uf': ufs,
                               'minutos': histograma_minuto(b26, '2', off26_2, rel)}
        tot0, _, _ = cortes(b26, '2', off26_2, rel, nh2, corte0=17 * 3600)
        R[f'2026_2t_{rel}']['variante_ate_17h00m00s'] = resumo_ate_depois(tot0)
        R[f'2026_2t_{rel}']['mesmas_secoes_1t'] = mesmas_secoes(b26, jan, '1', '2')
        if rel == 'local':
            jan_local = jan
        else:
            jan_prazo = jan
        tot1, ufs1, jan1 = cortes(b26, '1', off26_1, rel, nh1)
        R[f'2026_1t_{rel}'] = {'janelas': tot1, 'ate_depois': resumo_ate_depois(tot1), 'por_uf': ufs1,
                               'minutos': histograma_minuto(b26, '1', off26_1, rel)}
        # cruzamento das janelas 1t x 2t
        cx = C.Counter((jan1.get(k), j) for k, j in jan.items())
        R[f'2026_cruzamento_janela_1t_2t_{rel}'] = {f'{a}->{b}': v for (a, b), v in sorted(cx.items(), key=str)}
    # composição de J0 local: por grupo de deslocamento
    comp_j0 = C.defaultdict(novo)
    for k, j in jan_local.items():
        if j != JAN[0]:
            continue
        uf, mun = k.split('|')[:2]
        o = off26_2.get((uf, mun), 0)
        grupo = 'exterior' if uf == 'ZZ' else ('fuso_-1h_ou_-2h_(AC_AM_RO_RR_MT_MS)' if o > 0 else ('Noronha' if o < 0 else 'horario_de_Brasilia_17h00'))
        soma(comp_j0[grupo], b26[k]['2'], nh2.get(k))
    R['2026_2t_local_composicao_J0'] = {g: fecha(v) for g, v in comp_j0.items()}
    # J3 por município (local)
    j3m = C.defaultdict(lambda: {'2': novo(), '1': novo()})
    for k, j in jan_local.items():
        if j == JAN[3]:
            uf, mun = k.split('|')[:2]
            soma(j3m[f'{uf}|{mun}']['2'], b26[k]['2'], nh2.get(k))
            if '1' in b26[k]:
                soma(j3m[f'{uf}|{mun}']['1'], b26[k]['1'], nh1.get(k))
    # resto do município (não J3)
    resto = C.defaultdict(novo); ufall = C.defaultdict(novo); ufresto = C.defaultdict(novo)
    for k, j in jan_local.items():
        uf, mun = k.split('|')[:2]
        soma(ufall[uf], b26[k]['2'], nh2.get(k))
        if j != JAN[3]:
            soma(ufresto[uf], b26[k]['2'], nh2.get(k))
            if f'{uf}|{mun}' in j3m:
                soma(resto[f'{uf}|{mun}'], b26[k]['2'], nh2.get(k))
    lst = []
    for m, v in j3m.items():
        a = fecha(v['2']); b = fecha(v['1']); r = fecha(resto[m]) if m in resto else None
        lst.append({'mun': m, 'nome': nomes.get(m), 'secoes_J3': a['secoes'], 'comp': a['comp'], 'pct_L_2t': a['pct_L_validos'],
                    'pct_L_dois_1t_mesmas': b['pct_L_dois'], 'pct_L_1t_validos_mesmas': b['pct_L_validos'],
                    'pct_NH_2t': a['pct_NH'], 'resto_mun_secoes': r['secoes'] if r else 0,
                    'resto_mun_pct_L_2t': r['pct_L_validos'] if r else None, 'resto_mun_pct_NH': r['pct_NH'] if r else None})
    lst.sort(key=lambda x: -x['secoes_J3'])
    R['2026_2t_local_J3_por_municipio'] = lst
    R['2026_2t_uf_total_e_resto_sem_J3'] = {u: {'uf': fecha(ufall[u]), 'sem_J3': fecha(ufresto[u])} for u in sorted(ufall)}
    # J3 e J2 por UF com o 1º turno das mesmas seções
    for jj in (JAN[2], JAN[3]):
        pu = C.defaultdict(lambda: {'2': novo(), '1': novo()})
        for k, j in jan_local.items():
            if j == jj:
                uf = k.split('|')[0]
                soma(pu[uf]['2'], b26[k]['2'], nh2.get(k))
                if '1' in b26[k]:
                    soma(pu[uf]['1'], b26[k]['1'], nh1.get(k))
        R[f'2026_2t_local_{jj}_por_uf_com_1t'] = {u: {'2t': fecha(v['2']), '1t_mesmas': fecha(v['1'])} for u, v in sorted(pu.items())}
    # swing dentro do município e do local de votação
    gm = lambda k, s: '|'.join(k.split('|')[:2])
    gl = lambda k, s: '|'.join(k.split('|')[:3]) + '|' + str(s['loc'])
    R['swing_dentro'] = {}
    for nome_alvo, alvo in (('J3', {JAN[3]}), ('J2', {JAN[2]}), ('J2_J3', {JAN[2], JAN[3]}), ('depois_17h', {JAN[1], JAN[2], JAN[3]})):
        R['swing_dentro'][nome_alvo] = {'municipio': swing_dentro(b26, jan_local, gm, alvo), 'local': swing_dentro(b26, jan_local, gl, alvo)}
    R['nh_dentro'] = {}
    for nome_alvo, alvo in (('J3', {JAN[3]}), ('J2', {JAN[2]}), ('J2_J3', {JAN[2], JAN[3]}), ('depois_17h', {JAN[1], JAN[2], JAN[3]})):
        R['nh_dentro'][nome_alvo] = {'uf': nh_por_janela_dentro(b26, jan_local, nh2, lambda k, s: k.split('|')[0], alvo),
                                     'municipio': nh_por_janela_dentro(b26, jan_local, nh2, gm, alvo),
                                     'local': nh_por_janela_dentro(b26, jan_local, nh2, gl, alvo)}
    # NH por decil de município (taxa NH do 2º turno) e fatia de seções J3 e J2+J3 em cada decil
    mun_nh = C.defaultdict(lambda: [0, 0, 0, 0, 0])
    for k, j in jan_local.items():
        uf, mun = k.split('|')[:2]
        if uf == 'ZZ' or k not in nh2:
            continue
        x = mun_nh[f'{uf}|{mun}']
        x[0] += nh2[k]; x[1] += b26[k]['2']['comp']; x[2] += 1
        x[3] += j == JAN[3]; x[4] += j in (JAN[2], JAN[3])
    ms = sorted((v[0] / v[1], m, v) for m, v in mun_nh.items() if v[1] > 0)
    tot_sec = sum(v[2] for _, _, v in ms); dec = []
    acc = [0, 0, 0, 0, 0]; lim = tot_sec / 10; cur = 0; d = 0
    for r, m, v in ms:
        for i in range(5):
            acc[i] += v[i]
        cur += v[2]
        if cur >= lim * (d + 1) or m == ms[-1][1]:
            dec.append({'decil': d + 1, 'secoes': acc[2], 'pct_NH': round(100 * acc[0] / acc[1], 2), 'secoes_J3': acc[3], 'secoes_J2_J3': acc[4],
                        'ate_taxa_NH_mun': round(100 * r, 2)})
            acc = [0, 0, 0, 0, 0]; d += 1
    R['decis_municipio_por_NH_2t'] = dec
    # zona eleitoral: taxa NH e fatia J2+J3
    zn = C.defaultdict(lambda: [0, 0, 0, 0])
    for k, j in jan_local.items():
        if k not in nh2 or k.startswith('ZZ'):
            continue
        z = '|'.join(k.split('|')[:3])
        x = zn[z]; x[0] += nh2[k]; x[1] += b26[k]['2']['comp']; x[2] += 1; x[3] += j in (JAN[2], JAN[3])
    import math
    zs = [(v[0] / v[1], v[3] / v[2], v[1]) for v in zn.values() if v[1] > 0]
    def corr(xy, pond=True):
        sw = sum(w for _, _, w in xy) if pond else len(xy)
        mx = sum(x * (w if pond else 1) for x, _, w in xy) / sw; my = sum(y * (w if pond else 1) for _, y, w in xy) / sw
        cxy = sum((x - mx) * (y - my) * (w if pond else 1) for x, y, w in xy)
        cxx = sum((x - mx) ** 2 * (w if pond else 1) for x, _, w in xy); cyy = sum((y - my) ** 2 * (w if pond else 1) for _, y, w in xy)
        return round(cxy / math.sqrt(cxx * cyy), 4)
    R['correlacao_zona_NH_x_fatia_J2J3'] = {'zonas': len(zs), 'r_ponderado': corr(zs), 'r_simples': corr(zs, False),
                                            'zonas_com_alguma_J2J3': sum(1 for _, y, _ in zs if y > 0)}
    ms2 = [(v[0] / v[1], v[4] / v[2], v[1]) for v in mun_nh.values() if v[1] > 0]
    R['correlacao_municipio_NH_x_fatia_J2J3'] = {'municipios': len(ms2), 'r_ponderado': corr(ms2), 'r_simples': corr(ms2, False),
                                                 'municipios_com_alguma_J2J3': sum(1 for _, y, _ in ms2 if y > 0)}
    # Logs da amostra: último voto x encerramento nas seções que fecharam tarde
    logs = json.load(open(alogs))['2']
    lg = {'J0': [], 'J1': [], 'J2': [], 'J3': []}
    conf = C.Counter()
    for k, x in logs.items():
        if k not in jan_local or x.get('ultimo_voto') is None or x.get('encerramento') is None:
            continue
        j = jan_local[k][:2]
        if j == 'SH':
            continue
        e_bweb = seg(b26[k]['2']['enc'])
        conf['enc_log_igual_bweb_60s' if abs(e_bweb - x['encerramento']) <= 60 else 'enc_log_diferente'] += 1
        uf, mun = k.split('|')[:2]
        o = off26_2.get((uf, mun), 0) * 3600
        lg[j].append((x['ultimo_voto'] + o, x['encerramento'] + o, x.get('computados'), k))
    def hm(s):
        return f'{s // 3600:02d}:{(s % 3600) // 60:02d}:{s % 60:02d}'
    R['logs_amostra'] = {'conferencia': dict(conf)}
    for j, v in lg.items():
        if not v:
            continue
        uv = sorted(a for a, _, _, _ in v)
        R['logs_amostra'][j] = {'secoes': len(v), 'ultimo_voto_bsb_mediana': hm(uv[len(uv) // 2]), 'ultimo_voto_bsb_max': hm(uv[-1]),
                                'secoes_com_ultimo_voto_depois_17h00': sum(1 for a in uv if a >= 17 * 3600),
                                'secoes_com_ultimo_voto_depois_17h05': sum(1 for a in uv if a >= 17 * 3600 + 300),
                                'secoes_com_ultimo_voto_depois_18h': sum(1 for a in uv if a >= 18 * 3600),
                                'exemplos': [[k, hm(a), hm(b), c] for a, b, c, k in sorted(v, key=lambda t: -t[1])[:12]]}
    # horários de emissão e recebimento do BU nas seções J3
    em = C.Counter(); rc = C.Counter()
    for k, j in jan_local.items():
        if j == JAN[3]:
            v = horas[k]
            em[v[2][11:13]] += 1; rc[v[3][11:13]] += 1
    R['2026_2t_J3_emissao_e_recebimento_BU_por_hora'] = {'emissao': dict(sorted(em.items())), 'recebido': dict(sorted(rc.items()))}
    # Noronha
    nor = [k for k in b26 if k.startswith('PE|') and nomes.get('|'.join(k.split('|')[:2]), '').startswith('FERNANDO DE NORONHA')]
    R['noronha'] = [[k, b26[k]['2']['ab'], b26[k]['2']['enc'], b26[k].get('1', {}).get('ab'), b26[k].get('1', {}).get('enc')] for k in nor]
    # exterior
    zz = [b26[k]['2'] for k in b26 if k.startswith('ZZ|') and '2' in b26[k]]
    R['exterior_2t'] = {'secoes': len(zz), 'sem_horario': sum(1 for s in zz if not s.get('enc')),
                        'ab_hora': dict(C.Counter(s['ab'][:2] for s in zz if s.get('ab'))),
                        'enc_hora': dict(C.Counter(s['enc'][:2] for s in zz if s.get('enc')))}
    del b26, horas
    json.dump(R, open(saida, 'w'), ensure_ascii=False, indent=1)
    # ---------------- 2022 ----------------
    with gzip.open(a22, 'rt') as f:
        b22 = json.load(f)
    for t in ('2', '1'):
        off = offsets(b22, t)
        for rel in ('local', 'prazo'):
            tot, ufs, jan = cortes(b22, t, off, rel)
            R[f'2022_{t}t_{rel}'] = {'janelas': tot, 'ate_depois': resumo_ate_depois(tot), 'por_uf': ufs,
                                     'minutos': histograma_minuto(b22, t, off, rel)}
            if t == '2':
                R[f'2022_2t_{rel}']['mesmas_secoes_1t'] = mesmas_secoes(b22, jan, '1', '2')
        if t == '2':
            R['deslocamentos_2022_2t'] = dict(C.Counter(off.values()))
    del b22
    json.dump(R, open(saida, 'w'), ensure_ascii=False, indent=1)
    # ---------------- 2018 ----------------
    with gzip.open(a18, 'rt') as f:
        b18 = json.load(f)
    for t in ('2', '1'):
        off = offsets(b18, t)
        tot, ufs, jan = cortes(b18, t, off, 'local')
        R[f'2018_{t}t_local'] = {'janelas': tot, 'ate_depois': resumo_ate_depois(tot), 'por_uf': ufs,
                                 'minutos': histograma_minuto(b18, t, off, 'local')}
        if t == '2':
            R['2018_2t_local']['mesmas_secoes_1t'] = mesmas_secoes(b18, jan, '1', '2')
            R['deslocamentos_2018_2t'] = dict(C.Counter(off.values()))
    del b18
    json.dump(R, open(saida, 'w'), ensure_ascii=False, indent=1)
    print('ok')


if __name__ == '__main__':
    main()
