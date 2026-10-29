"""Conferência independente do L1 do Adendo 18 (horários impossíveis), com código próprio.

Entradas:
  ext1/ e ext2/: uma linha por combinação distinta dos campos de seção do bweb (extraídas por bin/ext.sh direto dos zips,
     sem passar pelo cache do outro agente). Campos: uf mun nome zona sec loc rec apt comp tipo urna c1 c2 flash carga agr
     ab enc em junta turma pleito turno.
  secoes2026.json.gz: votos de presidente (L=13, R=22), comparecimento de presidente, local e urna por turno.

Regras do registro (Adendo 18, L1), aplicadas com data e hora completas:
  A: comparecimento > 0 e encerramento (Brasília) < 17:00:00 do dia.
  B: emissão < encerramento.
  C: recebimento (Brasília, relógio do TSE) < emissão convertida para Brasília.
  D: abertura (Brasília) < 07:00:00 ou > 10:00:00, sem urna de contingência.
  E: carga fora da janela de carga do turno na UF.
Explicações aceitas pelo registro: fuso, contingência, junta.

Uso: python3 -I conferir_L1.py <dir_trabalho> <secoes2026.json.gz> <saida.json>
"""
import collections, datetime as dt, glob, gzip, json, math, os, sys, zoneinfo
import numpy as np

W, BASE, OUT = sys.argv[1:4]
DIA = {1: dt.datetime(2026, 10, 4), 2: dt.datetime(2026, 10, 25)}
NOMES = 'uf mun nome zona sec loc rec apt comp tipo urna c1 c2 flash carga agr ab enc em junta turma pleito turno'.split()


def pdt(s):
    try:
        return dt.datetime.strptime(s, '%Y-%m-%d %H:%M:%S')
    except (ValueError, TypeError):
        return None


def ler(turno):
    g = collections.defaultdict(list)
    for f in sorted(glob.glob(os.path.join(W, f'ext{turno}', '*.txt'))):
        for l in open(f, 'rb').read().decode('latin1').split('\n'):
            if not l:
                continue
            r = [x.strip().strip('"') for x in l.replace('\r', '').split(';')]
            k = f"{r[0]}|{int(r[1])}|{int(r[3])}|{int(r[4])}"
            g[k].append(dict(zip(NOMES, r)))
    S = {}
    difs = collections.Counter()
    for k, L in g.items():
        d = tuple(n for n in NOMES if len({x[n] for x in L}) > 1)
        if d:
            difs[d] += 1
        x = L[0]
        S[k] = {'ab': pdt(x['ab']), 'enc': pdt(x['enc']), 'em': pdt(x['em']), 'rec': pdt(x['rec']), 'carga': pdt(x['carga']),
                'urna': x['urna'], 'junta': x['junta'] not in ('-1', ''), 'nome': x['nome'], 'loc': int(x['loc']),
                'comp_max': max(int(y['comp']) for y in L), 'apt': int(x['apt']), 'tipo': x['tipo'], 'agr': x['agr'],
                'campos_tempo_distintos': [n for n in ('ab', 'enc', 'em', 'rec', 'carga', 'urna') if n in d]}
    return S, difs


base = json.load(gzip.open(BASE, 'rt'))
S = {}
DIFS = {}
for t in (1, 2):
    S[t], DIFS[t] = ler(t)
R = {'secoes': {t: len(S[t]) for t in (1, 2)}, 'campos_que_variam_entre_cargos': {t: {'+'.join(k): v for k, v in DIFS[t].items()} for t in (1, 2)}}

# ---- fuso do município: hora cheia modal da abertura (seções sem junta com abertura), por turno
modal = {}
for t in (1, 2):
    c = collections.defaultdict(collections.Counter)
    for k, s in S[t].items():
        if s['ab'] and not s['junta']:
            c['|'.join(k.split('|')[:2])][s['ab'].hour] += 1
    modal[t] = {m: cc.most_common(1)[0][0] for m, cc in c.items()}
R['fuso_modal'] = {t: dict(collections.Counter(('ZZ' if m.startswith('ZZ') else 'BR') + '|' + str(h) for m, h in modal[t].items())) for t in (1, 2)}
R['fuso_muda_entre_turnos'] = sum(1 for m in modal[1] if m in modal[2] and modal[1][m] != modal[2][m])


def off(t, k):
    m = '|'.join(k.split('|')[:2])
    return modal[t].get(m, modal[3 - t].get(m, 8)) - 8


TZ = {  # cidade do exterior -> zona tz (dado de conhecimento geral; conferido abaixo pela distribuição do intervalo)
    'KATMANDU': 'Asia/Kathmandu', 'ABIDJÃ': 'Africa/Abidjan', 'ABU DHABI': 'Asia/Dubai', 'ACCRA': 'Africa/Accra', 'AMÃ': 'Asia/Amman',
    'ANCARA': 'Europe/Istanbul', 'ARGEL': 'Africa/Algiers', 'ARTIGAS': 'America/Montevideo', 'ASSUNÇÃO': 'America/Asuncion',
    'ATENAS': 'Europe/Athens', 'BANGKOK': 'Asia/Bangkok', 'BARCELONA': 'Europe/Madrid', 'BEIRUTE': 'Asia/Beirut',
    'BELGRADO': 'Europe/Belgrade', 'BERLIM': 'Europe/Berlin', 'BISSAU': 'Africa/Bissau', 'BOGOTÁ': 'America/Bogota',
    'BOSTON': 'America/New_York', 'BRUXELAS': 'Europe/Brussels', 'BUCARESTE': 'Europe/Bucharest', 'BUDAPESTE': 'Europe/Budapest',
    'BUENOS AIRES': 'America/Argentina/Buenos_Aires', 'CAIENA': 'America/Cayenne', 'CAIRO': 'Africa/Cairo',
    'CAMBERRA': 'Australia/Sydney', 'CARACAS': 'America/Caracas', 'CHICAGO': 'America/Chicago',
    'CIDADE DO CABO': 'Africa/Johannesburg', 'SINGAPURA': 'Asia/Singapore', 'CIUDAD DEL ESTE': 'America/Asuncion',
    'CIUDAD GUAYANA': 'America/Caracas', 'COCHABAMBA': 'America/La_Paz', 'CONCEPCIÓN': 'America/Asuncion',
    'COPENHAGUE': 'Europe/Copenhagen', 'CÓRDOBA': 'America/Argentina/Cordoba', 'DACAR': 'Africa/Dakar',
    'DAMASCO': 'Asia/Damascus', 'DÍLI': 'Asia/Dili', 'DOHA': 'Asia/Qatar', 'DUBLIN': 'Europe/Dublin',
    'ENCARNACIÓN': 'America/Asuncion', 'ESTOCOLMO': 'Europe/Stockholm', 'FRANKFURT': 'Europe/Berlin', 'GENEBRA': 'Europe/Zurich',
    'GEORGETOWN': 'America/Guyana', 'HAMAMATSU': 'Asia/Tokyo', 'HANÓI': 'Asia/Ho_Chi_Minh', 'HAVANA': 'America/Havana',
    'HELSINQUE': 'Europe/Helsinki', 'HONG KONG': 'Asia/Hong_Kong', 'HOUSTON': 'America/Chicago', 'JACARTA': 'Asia/Jakarta',
    'KIEV': 'Europe/Kyiv', 'KUAITE': 'Asia/Kuwait', 'KUALA LUMPUR': 'Asia/Kuala_Lumpur', 'LA PAZ': 'America/La_Paz',
    'LAGOS': 'Africa/Lagos', 'LIMA': 'America/Lima', 'LISBOA': 'Europe/Lisbon', 'LONDRES': 'Europe/London',
    'LOS ANGELES': 'America/Los_Angeles', 'LUANDA': 'Africa/Luanda', 'MADRI': 'Europe/Madrid', 'MANÁGUA': 'America/Managua',
    'MANILA': 'Asia/Manila', 'MAPUTO': 'Africa/Maputo', 'MEXICO': 'America/Mexico_City', 'MIAMI': 'America/New_York',
    'MILÃO': 'Europe/Rome', 'MONTEVIDÉU': 'America/Montevideo', 'MONTREAL': 'America/Toronto', 'MOSCOU': 'Europe/Moscow',
    'MUMBAI': 'Asia/Kolkata', 'MUNIQUE': 'Europe/Berlin', 'NAGÓIA': 'Asia/Tokyo', 'NAIRÓBI': 'Africa/Nairobi',
    'NOVA DELHI': 'Asia/Kolkata', 'NOVA YORK': 'America/New_York', 'OSLO': 'Europe/Oslo', 'OTTAWA': 'America/Toronto',
    'PANAMA': 'America/Panama', 'PARAMARIBO': 'America/Paramaribo', 'PARIS': 'Europe/Paris',
    'PASO LOS LIBRES': 'America/Argentina/Buenos_Aires', 'PEDRO JUAN CABALLERO': 'America/Asuncion', 'PEQUIM': 'Asia/Shanghai',
    'PORT OF SPAIN': 'America/Port_of_Spain', 'PORTO PRÍNCIPE': 'America/Port-au-Prince', 'PORTO': 'Europe/Lisbon',
    'PRAGA': 'Europe/Prague', 'PRAIA': 'Atlantic/Cape_Verde', 'PRETÓRIA': 'Africa/Johannesburg', 'QUITO': 'America/Guayaquil',
    'RABAT': 'Africa/Casablanca', 'RAMALLAH': 'Asia/Hebron', 'RIADE': 'Asia/Riyadh', 'RIO BRANCO': 'America/Montevideo',
    'ROMA': 'Europe/Rome', 'AMSTERDÃ': 'Europe/Amsterdam', 'SALTO DEL GUAIRÁ': 'America/Asuncion',
    'SANTA CRUZ DE LA SIERRA': 'America/La_Paz', 'SANTIAGO': 'America/Santiago', 'SÃO DOMINGOS': 'America/Santo_Domingo',
    'SÃO FRANCISCO': 'America/Los_Angeles', 'SÃO JOSÉ': 'America/Costa_Rica', 'SÃO SALVADOR': 'America/El_Salvador',
    'SEUL': 'Asia/Seoul', 'SÓFIA': 'Europe/Sofia', 'SYDNEY': 'Australia/Sydney', 'TAIPÉ': 'Asia/Taipei', 'TEERÃ': 'Asia/Tehran',
    'TEGUCIGALPA': 'America/Tegucigalpa', 'TEL AVIV': 'Asia/Jerusalem', 'TÓQUIO': 'Asia/Tokyo', 'TORONTO': 'America/Toronto',
    'CANTÃO': 'Asia/Shanghai', 'TRÍPOLI': 'Africa/Tripoli', 'TUNIS': 'Africa/Tunis', 'VARSÓVIA': 'Europe/Warsaw',
    'VIENA': 'Europe/Vienna', 'WASHINGTON': 'America/New_York', 'WELLINGTON': 'Pacific/Auckland', 'WINDHOEK': 'Africa/Windhoek',
    'XANGAI': 'Asia/Shanghai', 'ZURIQUE': 'Europe/Zurich', 'HARTFORD': 'America/New_York', 'FARO': 'Europe/Lisbon',
    'DAR ES SALAAM': 'Africa/Dar_es_Salaam', 'MENDOZA': 'America/Argentina/Mendoza', 'ZAGREB': 'Europe/Zagreb',
    'VANCOUVER': 'America/Vancouver', 'ATLANTA': 'America/New_York', 'MASCATE': 'Asia/Muscat', 'LIUBLIANA': 'Europe/Ljubljana',
    'BRATISLAVA': 'Europe/Bratislava', 'ISTAMBUL': 'Europe/Istanbul', 'NICOSIA': 'Asia/Nicosia', 'GUATEMALA': 'America/Guatemala',
    'PUERTO IGUAZÚ': 'America/Argentina/Cordoba', 'NASSAU': 'America/Nassau', 'TALIN': 'Europe/Tallinn',
    'KINGSTON-JAMAICA': 'America/Jamaica', 'BAREIN': 'Asia/Bahrain', 'ORLANDO': 'America/New_York', 'EDIMBURGO': 'Europe/London',
    'MARSELHA': 'Europe/Paris'}


def off_real(nome, quando):
    """Hora local da cidade menos hora de Brasília (h), no instante local dado."""
    z = TZ.get(nome)
    if z is None or quando is None:
        return None
    return quando.replace(tzinfo=zoneinfo.ZoneInfo(z)).utcoffset().total_seconds() / 3600 + 3


def regras(t, s, o, comp, cont, oC=None):
    dia = DIA[t]; v = []
    h = dt.timedelta(hours=o)
    if s['enc'] and comp > 0 and s['enc'] - h < dia.replace(hour=17):
        v.append('A')
    if s['em'] and s['enc'] and s['em'] < s['enc']:
        v.append('B')
    hc = h if oC is None else dt.timedelta(hours=oC)
    if s['em'] and s['rec'] and s['rec'] < s['em'] - hc:
        v.append('C')
    if s['ab'] and not cont:
        a = s['ab'] - h
        if a < dia.replace(hour=7) or a > dia.replace(hour=10):
            v.append('D')
    return v


JAN = {1: (dt.datetime(2026, 9, 4), dt.datetime(2026, 10, 5)), 2: (dt.datetime(2026, 9, 4), dt.datetime(2026, 10, 26))}


def avaliar(t, cont_def='a_ou_b', janela=None):
    """Lista de seções que violam alguma regra, com explicação. cont_def: 'a_ou_b' (registro lido como o outro agente),
    'b' (só carga no dia), 'nenhuma'. janela: função (uf, carga) -> True se dentro (padrão: JAN do turno)."""
    out = []
    for k, s in S[t].items():
        uf = k.split('|')[0]
        b = base.get(k, {}).get(str(t))
        comp = b['comp'] if b else s['comp_max']
        u_outro = base.get(k, {}).get(str(3 - t), {}).get('urna')
        troca = (u_outro is not None and s['urna'] not in ('', '0', '-1') and str(u_outro) != s['urna'])
        no_dia = s['carga'] is not None and s['carga'].date() == DIA[t].date()
        cont = {'a_ou_b': troca or no_dia, 'b': no_dia, 'nenhuma': False}[cont_def]
        o = off(t, k)
        ext = uf == 'ZZ'
        v = [] if (s['junta'] or (s['ab'] is None and s['enc'] is None)) else regras(t, s, o, comp, cont)
        if s['carga'] is not None:
            dentro = janela(uf, s['carga'], troca) if janela else (JAN[t][0] <= s['carga'] < JAN[t][1])
            if not dentro:
                v.append('E')
        if not v:
            continue
        ex = []
        if s['junta']:
            ex.append('junta')
        fuso_ok = False; o_alt = None
        if any(x in 'ACD' for x in v) and not s['junta']:
            if ext:
                orr = off_real(s['nome'], s['em'] or s['enc'])
                if orr is not None and not any(x in 'ACD' for x in regras(t, s, o, comp, cont, oC=orr)):
                    fuso_ok = True; o_alt = orr
            else:
                for o2 in (-2, -1, 0, 1):
                    if o2 != o and not any(x in 'ACD' for x in regras(t, s, o2, comp, cont)):
                        fuso_ok = True; o_alt = o2
                        break
        if fuso_ok and all(x in 'ACD' for x in v):
            ex.append('fuso')
        if cont:
            ex.append('contingencia')
        r = {'k': k, 'regras': v, 'ex': ex, 'o': o, 'o_alt': o_alt, 'troca': troca, 'carga_no_dia': no_dia, 'nome': s['nome'],
             'ab': str(s['ab']), 'enc': str(s['enc']), 'em': str(s['em']), 'rec': str(s['rec']), 'carga': str(s['carga']), 'comp': comp}
        if s['em'] and s['rec']:
            r['rec_menos_em_s'] = (s['rec'] - (s['em'] - dt.timedelta(hours=o))).total_seconds()
            if o_alt is not None:
                r['rec_menos_em_alt_s'] = (s['rec'] - (s['em'] - dt.timedelta(hours=o_alt))).total_seconds()
        out.append(r)
    return out


# ---- virada e d contra o local (votos somados das outras seções) e contra a média simples das outras seções
X = {}; LOC = {}
for k, b in base.items():
    if '1' in b and '2' in b:
        L1, R1, L2, R2 = b['1']['L'], b['1']['R'], b['2']['L'], b['2']['R']
        if L1 + R1 > 0 and L2 + R2 > 0:
            X[k] = np.array([L1, R1, L2, R2], float)
            LOC[k] = '|'.join(k.split('|')[:3]) + '|' + str(b['2']['loc'])
vir = lambda x: 100 * (x[2] / (x[2] + x[3]) - x[0] / (x[0] + x[1]))
porloc = collections.defaultdict(list)
for k in X:
    porloc[LOC[k]].append(k)
D = {}
for k, x in X.items():
    outros = [j for j in porloc[LOC[k]] if j != k]
    if outros:
        tot = sum(X[j] for j in outros)
        D[k] = {'d_pool': vir(x) - vir(tot), 'd_media': vir(x) - float(np.mean([vir(X[j]) for j in outros])),
                'vir': vir(x), 'vir_outros': vir(tot), 'n_outros': len(outros), 'votos2': x[2] + x[3]}
dd = np.array([v['d_pool'] for v in D.values()]); vv = np.array([v['votos2'] for v in D.values()])
R['d_todas'] = {'n': int(len(dd)), 'media': float(dd.mean()), 'dp': float(dd.std()), 'frac_ge3': float((dd >= 3).mean())}


def frac_ge3_vizinhas(votos):
    """Frequência de d >= 3 entre as seções com votos nos finalistas entre 0,8 e 1,25 vezes os da seção."""
    m = (vv >= votos * 0.8) & (vv <= votos * 1.25)
    return float((dd[m] >= 3).mean()), int(m.sum())


def resumo(lista, t, rotulo):
    sem = [r for r in lista if not r['ex']]
    com_d = [r for r in sem if r['k'] in D]
    ge3 = [r for r in com_d if D[r['k']]['d_pool'] >= 3]
    ge3m = [r for r in com_d if D[r['k']]['d_media'] >= 3]
    p_nada = 1.0
    for r in com_d:
        p_nada *= 1 - frac_ge3_vizinhas(D[r['k']]['votos2'])[0]
    if com_d:
        ys = np.array([D[r['k']]['d_pool'] for r in com_d]); gs = [LOC[r['k']] for r in com_d]
        _, gi = np.unique(gs, return_inverse=True); G = gi.max() + 1
        m = ys.mean(); Sg = np.bincount(gi, weights=ys - m)
        ep = math.sqrt((Sg ** 2).sum() / len(ys) ** 2 * G / (G - 1)) if G > 1 else float('nan')
    else:
        m = ep = float('nan'); G = 0
    if len(sem) >= 100:
        ver = 'INCOERÊNCIA'
    elif ge3:
        ver = 'INCOERÊNCIA'
    elif not sem:
        ver = 'COERENTE'
    else:
        ver = 'INCONCLUSIVO'
    ver_grupo = 'INCOERÊNCIA' if (len(sem) >= 100 or (com_d and m >= 3)) else ('COERENTE' if not sem else 'INCONCLUSIVO')
    return {'rotulo': rotulo, 'turno': t, 'violam': len(lista), 'por_regra': dict(collections.Counter(x for r in lista for x in r['regras'])),
            'por_explicacao': dict(collections.Counter('+'.join(r['ex']) or 'nenhuma' for r in lista)),
            'sem_explicacao': len(sem), 'sem_por_regra': dict(collections.Counter('+'.join(r['regras']) for r in sem)),
            'sem_com_d': len(com_d), 'd_ge3_pool': [(r['k'], round(D[r['k']]['d_pool'], 3)) for r in ge3],
            'd_ge3_media_simples': [(r['k'], round(D[r['k']]['d_media'], 3)) for r in ge3m],
            'media_d': m, 'ep_media_d': ep, 'locais': int(G), 'prob_acaso_alguma_ge3': 1 - p_nada,
            'veredito_letra': ver, 'veredito_grupo': ver_grupo,
            'lista_sem': [dict(r, **({'d_pool': round(D[r['k']]['d_pool'], 3), 'd_media': round(D[r['k']]['d_media'], 3),
                                      'n_outros': D[r['k']]['n_outros'], 'votos2': int(D[r['k']]['votos2'])} if r['k'] in D else {}))
                          for r in sem]}


res = {}
for t in (1, 2):
    L = avaliar(t)
    res[f'{t}_registro'] = resumo(L, t, 'leitura do outro agente: contingência = troca de urna ou carga no dia; janela 04/09 ao dia')
    # exterior: conferir a explicação por fuso real (intervalo mínimo e máximo depois do ajuste)
    gaps = [r['rec_menos_em_alt_s'] for r in L if r['k'].startswith('ZZ') and 'rec_menos_em_alt_s' in r]
    res[f'{t}_registro']['exterior_gap_fuso_real_s'] = [min(gaps), float(np.median(gaps)), max(gaps)] if gaps else None
    res[f'{t}_registro']['exterior_sem_tz'] = sorted({r['nome'] for r in L if r['k'].startswith('ZZ') and r['o_alt'] is None})
    for cd in ('b', 'nenhuma'):
        res[f'{t}_contingencia_{cd}'] = resumo(avaliar(t, cont_def=cd), t, f'contingência só por {cd}')

# ---- janela de carga estrita onde a imprensa deu datas (robustez): 1º turno SE 18 a 28/09, SP a partir de 23/09;
#      2º turno: carga do 1º turno (mesma janela do 1º) ou preparação do 2º turno PR 12 a 20/10, BA 14 a 22/10, CE 14 a 16/10,
#      PB até 16/10, MS até 17/10, SP até 23/10; mais o dia da votação (contingência). Fora dessas UFs, a janela do registro.
J1 = {'SE': (dt.datetime(2026, 9, 18), dt.datetime(2026, 9, 29)), 'SP': (dt.datetime(2026, 9, 23), dt.datetime(2026, 10, 1))}
J2 = {'PR': (dt.datetime(2026, 10, 12), dt.datetime(2026, 10, 21)), 'BA': (dt.datetime(2026, 10, 14), dt.datetime(2026, 10, 23)),
      'CE': (dt.datetime(2026, 10, 14), dt.datetime(2026, 10, 17)), 'PB': (dt.datetime(2026, 10, 5), dt.datetime(2026, 10, 17)),
      'MS': (dt.datetime(2026, 10, 5), dt.datetime(2026, 10, 18)), 'SP': (dt.datetime(2026, 10, 5), dt.datetime(2026, 10, 24))}


def jan_estrita(t):
    def f(uf, c, troca):
        if c.date() == DIA[t].date():
            return True
        if t == 1:
            if uf in J1:
                return J1[uf][0] <= c < J1[uf][1]
            return JAN[1][0] <= c < JAN[1][1]
        # 2º turno: carga do 1º turno ou da preparação do 2º
        if c < dt.datetime(2026, 10, 5):
            if uf in J1:
                return J1[uf][0] <= c < J1[uf][1]
            return JAN[1][0] <= c
        if uf in J2:
            return J2[uf][0] <= c < J2[uf][1]
        return c < JAN[2][1]
    return f


for t in (1, 2):
    L = avaliar(t, janela=jan_estrita(t))
    res[f'{t}_janela_estrita'] = resumo(L, t, 'janela de carga estrita nas UFs com datas na imprensa (véspera fora da janela)')

# ---- cargas do 2º turno feitas depois do 1º, por UF e dia (para comparar com os cronogramas)
c2 = collections.defaultdict(collections.Counter)
for k, s in S[2].items():
    if s['carga'] and s['carga'] >= dt.datetime(2026, 10, 5):
        c2[k.split('|')[0]][s['carga'].strftime('%d/%m')] += 1
R['carga_2t_pos_1t_por_uf_dia'] = {uf: dict(sorted(v.items())) for uf, v in sorted(c2.items())}

# ---- seções impossíveis no 2º turno por regra D com marca de contingência (fora da regra por definição): d de cada uma
excl = []
for k, s in S[2].items():
    if s['junta'] or not s['ab']:
        continue
    a = s['ab'] - dt.timedelta(hours=off(2, k))
    if a < DIA[2].replace(hour=7) or a > DIA[2].replace(hour=10):
        excl.append({'k': k, 'ab_brasilia': str(a), 'urna2': s['urna'], 'urna1': base.get(k, {}).get('1', {}).get('urna'),
                     'carga': str(s['carga']), 'd_pool': round(D[k]['d_pool'], 3) if k in D else None,
                     'vir': round(vir(X[k]), 3) if k in X else None})
R['abertura_fora_7_10_todas_2t'] = excl

# ---- campos ausentes (não testáveis) entre as seções sem junta
aus = {}
for t in (1, 2):
    c = collections.Counter()
    for k, s in S[t].items():
        if s['junta']:
            continue
        for n in ('ab', 'enc', 'em', 'rec', 'carga'):
            if s[n] is None:
                c[n] += 1
    aus[t] = dict(c)
R['campos_ausentes_sem_junta'] = aus
R['junta'] = {t: sum(1 for s in S[t].values() if s['junta']) for t in (1, 2)}
R['tipo_urna'] = {t: dict(collections.Counter(s['tipo'] for s in S[t].values())) for t in (1, 2)}

# ---- o gatilho: local 1295 de Inácio Martins (todas as seções do local) e seções da zona 34
g = {}
for k in base:
    if k.startswith('PR|75990|34|'):
        b = base[k]
        g[k] = {'loc1': b['1']['loc'], 'loc2': b.get('2', {}).get('loc'), 'apt2': b.get('2', {}).get('apt'),
                'comp1': b['1']['comp'], 'comp2': b.get('2', {}).get('comp'), 'ab1': b['1']['ab'], 'ab2': b.get('2', {}).get('ab'),
                'L1R1L2R2': [b['1']['L'], b['1']['R'], b.get('2', {}).get('L'), b.get('2', {}).get('R')],
                'agr2': S[2].get(k, {}).get('agr'), 'agr1': S[1].get(k, {}).get('agr'), 'junta2': S[2].get(k, {}).get('junta')}
R['inacio_martins_zona34'] = g

# ---- descritivo: contra o município (Jacareacanga e Óbidos)
mun = collections.defaultdict(lambda: np.zeros(4))
for k, x in X.items():
    mun['|'.join(k.split('|')[:2])] += x
Dm = {k: vir(x) - vir(mun['|'.join(k.split('|')[:2])] - x) for k, x in X.items() if (mun['|'.join(k.split('|')[:2])] - x)[[0, 2]].sum() > 0}
dm = np.array(list(Dm.values())); vm = np.array([X[k][2] + X[k][3] for k in Dm])
ext = {}
for k in ('PA|4200|102|54', 'PA|5010|22|259'):
    sel = (vm > 100) & (vm <= 200) if X[k][2] + X[k][3] > 100 else (vm > 50) & (vm <= 100)
    fr = float((dm[sel] >= Dm[k]).mean()) if Dm[k] > 0 else float((dm[sel] <= Dm[k]).mean())
    ext[k] = {'d_mun': Dm[k], 'faixa_n': int(sel.sum()), 'freq': fr, 'L1R1L2R2': X[k].tolist()}
R['extremos_municipio'] = ext
R['resultados'] = res
json.dump(R, open(OUT, 'w'), ensure_ascii=False, indent=1, default=str)
for nm, r in res.items():
    print(nm, '| violam', r['violam'], r['por_regra'], '| explic', r['por_explicacao'], '| sem', r['sem_explicacao'], r['sem_por_regra'],
          '| com d', r['sem_com_d'], '| d>=3', r['d_ge3_pool'], '| d>=3 (média simples)', r['d_ge3_media_simples'],
          '| média d', round(r['media_d'], 3) if r['media_d'] == r['media_d'] else None, 'ep', round(r['ep_media_d'], 3) if r['ep_media_d'] == r['ep_media_d'] else None,
          '| P(acaso)', round(r['prob_acaso_alguma_ge3'], 3), '|', r['veredito_letra'], '/', r['veredito_grupo'])
    if 'exterior_gap_fuso_real_s' in r:
        print('   exterior gap fuso real', r['exterior_gap_fuso_real_s'], 'sem tz', r['exterior_sem_tz'])
print('fuso', R['fuso_modal'], 'muda', R['fuso_muda_entre_turnos'])
print('ausentes', R['campos_ausentes_sem_junta'], 'junta', R['junta'], 'tipo', R['tipo_urna'])
print('difs', R['campos_que_variam_entre_cargos'])
print('d todas', R['d_todas'])
print('extremos', ext)
