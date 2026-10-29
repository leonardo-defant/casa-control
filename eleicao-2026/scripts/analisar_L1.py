"""L1 do Adendo 18 (PRE-REGISTRO-2026-10-26.md): horários impossíveis em todas as seções, bweb dos dois turnos de 2026.

Registro (escrito antes de rodar):
  - Por seção: abertura, encerramento, emissão do boletim, recebimento pelo TSE e data de carga da urna, com o fuso de
    cada município (deslocamento pela hora de abertura mais comum do município).
  - Impossível: encerramento antes das 17h00 de Brasília com comparecimento acima de zero; emissão do boletim antes do
    encerramento; recebimento antes da emissão; abertura antes das 7h ou depois das 10h de Brasília sem urna de
    contingência; carga fora da janela de carga do turno na UF.
  - Sinal: 100 ou mais seções impossíveis no 2º turno sem explicação por fuso, contingência ou junta, ou qualquer número
    delas em que a virada de Lula supere a das outras seções do mesmo local em 3 pontos ou mais. Sem sinal: nenhuma
    seção impossível sem explicação. Entre os dois: inconclusivo, com a lista das seções para conferência.

Relógios (verificados nos dados antes de aplicar as regras; ver a seção 1 do texto de saída):
  - DT_ABERTURA, DT_ENCERRAMENTO e DT_EMISSAO_BU estão no relógio da urna, em hora local: a emissão vem cerca de 2 min
    depois do encerramento em todos os fusos, e o encerramento modal é 17h, 16h e 15h nos fusos de Brasília, -1 e -2.
  - DT_BU_RECEBIDO está em hora de Brasília (relógio do TSE): a distribuição da hora de recebimento é a mesma em todos os
    fusos, e o menor intervalo entre emissão (local) e recebimento é de 1 h no fuso -1 e de 2 h no fuso -2.
  - No exterior, as três primeiras estão em hora local da cidade (abertura modal 8h local em todas as cidades) e o
    recebimento em hora de Brasília.

Especificação fixada neste arquivo antes de contar as seções impossíveis (o registro não fixa estes pontos; cada um sai
no texto como leitura declarada):
  E1. Fuso do município: hora cheia da abertura mais comum entre as seções do município com abertura, em cada turno;
      deslocamento o = hora modal - 8 (a votação vai das 8h às 17h de Brasília no país inteiro). Hora de Brasília
      equivalente = hora local da urna - o. No exterior a votação é das 8h às 17h locais; o mesmo cálculo dá o = 0 e as
      regras de abertura e encerramento ficam no horário oficial local, que é o que "de Brasília" significa lá.
  E2. Regras, com a data e a hora completas (dia da votação: 04/10/2026 e 25/10/2026):
      A: comparecimento de presidente > 0 e encerramento (Brasília) < 17:00:00 do dia.
      B: emissão < encerramento (mesmo relógio, sem conversão).
      C: recebimento (Brasília) < emissão convertida para Brasília pelo deslocamento do município.
      D: abertura (Brasília) < 07:00:00 ou > 10:00:00 do dia, e a seção sem marca de contingência (E4).
      E: data e hora da carga da urna efetivada fora da janela do turno (E5).
  E3. Junta: NR_JUNTA_APURADORA diferente de -1 (boletim emitido pela junta; as seções sem abertura e encerramento
      são todas de junta). Seção de junta não tem os horários da urna e é contada como explicada por junta.
  E4. Contingência (marca no bweb): (a) número da urna efetivada diferente entre o 1º e o 2º turno (vale para os dois
      turnos, porque o bweb não diz em qual deles entrou a urna de contingência); ou (b) carga da urna efetivada no
      próprio dia da votação do turno. Robustez fora do registro: (c) carga do 2º turno feita depois do 1º turno
      (art. 109 da Res. TSE 23.751/2026: nova carga ou nova urna quando a preparação do 2º turno falha).
  E5. Janela de carga do turno: não há data nacional de carga no calendário (Res. TSE 23.760/2026); a carga é marcada
      por cada TRE depois da assinatura e lacração dos sistemas no TSE, em 04/09/2026. No 2º turno a urna é a do 1º
      com nova mídia de resultado, sem nova carga (art. 108 da Res. 23.751/2026); nova carga ou nova urna só quando a
      preparação falha (art. 109) ou na contingência do dia (arts. 99 a 101). Janela usada: 1º turno, de 04/09/2026
      00:00 até o fim do dia 04/10/2026; 2º turno, de 04/09/2026 00:00 até o fim do dia 25/10/2026. Os cronogramas
      estaduais achados na imprensa saem no texto, sem entrar na regra.
  E6. Explicação por fuso: com outro deslocamento do Brasil (o' em -2, -1, 0, +1, diferente do do município) as regras
      A, C e D passam todas (a urna com o relógio em outro fuso desloca abertura, encerramento e emissão juntos). No
      exterior: a regra C refeita com o fuso real da cidade (base tz do sistema, versão gravada na saída), com A e D no
      horário local. B e E não mudam com o fuso.
  E7. Seção explicada = junta, ou fuso, ou contingência (marca E4 a ou b), para qualquer regra que ela viole (leitura
      literal: o registro lista as três explicações sem ligar cada uma a uma regra). A tabela por regra mostra qual
      explicação cobre cada caso, para o leitor ver se a explicação é pertinente.
  E8. Virada de Lula da seção = 100 [L2/(L2+R2) - L1/(L1+R1)], L = 13, R = 22, seção com voto nos dois finalistas nos
      dois turnos. "A das outras seções do mesmo local" = a mesma conta com os votos somados das outras seções do local
      de votação do 2º turno (UF|município|zona|local) com voto nos finalistas nos dois turnos. d = diferença das duas.
      Leitura literal do "qualquer número delas em que a virada de Lula supere ... em 3 pontos ou mais": cada seção
      impossível sem explicação do 2º turno é comparada com o seu local; uma ou mais com d >= 3 dá sinal. A leitura
      em grupo (média de d das seções sem explicação >= 3) sai ao lado, com o erro-padrão agrupado por local, e a
      frequência de d >= 3 entre todas as seções (o acaso).

Uso: python3 -I analisar_L1.py <zips1t_dir> <zips2t_dir> <secoes2026.json.gz> <cache_dir> <arq_logs_2t_dir|-> <saida.json> <saida.txt>
"""
import os as _os, sys as _sys
_sys.path.insert(0, _os.path.dirname(_os.path.abspath(__file__)))
import collections, datetime as dt, glob, gzip, json, math, os, re, sys, time, zipfile
from multiprocessing import Pool
import numpy as np
from lib import carregar

DIA = {1: dt.datetime(2026, 10, 4), 2: dt.datetime(2026, 10, 25)}
INICIO_JANELA = dt.datetime(2026, 9, 4)
OFFS_BR = (-2, -1, 0, 1)
BRT = dt.timezone(dt.timedelta(hours=-3))

CAMPOS = ['NR_LOCAL_VOTACAO', 'NM_MUNICIPIO', 'DT_BU_RECEBIDO', 'QT_APTOS', 'QT_COMPARECIMENTO', 'CD_TIPO_URNA', 'DS_TIPO_URNA',
          'NR_URNA_EFETIVADA', 'CD_CARGA_1_URNA_EFETIVADA', 'CD_CARGA_2_URNA_EFETIVADA', 'CD_FLASHCARD_URNA_EFETIVADA',
          'DT_CARGA_URNA_EFETIVADA', 'DS_CARGO_PERGUNTA_SECAO', 'DS_SECOES_AGREGADAS', 'DT_ABERTURA', 'DT_ENCERRAMENTO',
          'QT_ELEI_BIOM_SEM_HABILITACAO', 'DT_EMISSAO_BU', 'NR_JUNTA_APURADORA', 'NR_TURMA_APURADORA', 'DT_PLEITO']

# fuso das cidades do exterior (nome do município no bweb -> zona da base tz)
TZ_EXTERIOR = {
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


def log(msg):
    print(time.strftime('%H:%M:%S'), msg, flush=True)


# ---------------------------------------------------------------- extração (uma linha por seção, todos os cargos)

def extrair_zip(zpath):
    out = {}; difs = {}; cargos = {}
    z = zipfile.ZipFile(zpath)
    nome = [n for n in z.namelist() if n.lower().endswith('.csv')][0]
    with z.open(nome) as fh:
        cab = [c.strip().strip('"').replace('SG_ UF', 'SG_UF') for c in fh.readline().decode('latin1').rstrip('\r\n').split(';')]
        ix = {c: i for i, c in enumerate(cab)}
        iu, im, iz, isc, ic = ix['SG_UF'], ix['CD_MUNICIPIO'], ix['NR_ZONA'], ix['NR_SECAO'], ix['CD_CARGO_PERGUNTA']
        sel = [ix[c] for c in CAMPOS if c in ix]
        nomes = [c for c in CAMPOS if c in ix]
        for raw in fh:
            r = raw.decode('latin1').rstrip('\r\n').split(';')
            k = (r[iu], r[im], r[iz], r[isc])
            v = tuple(r[i] for i in sel)
            cg = r[ic].strip('"')
            o = out.get(k)
            if o is None:
                out[k] = v; cargos[k] = {cg}
            else:
                cargos[k].add(cg)
                if o != v:
                    d = difs.setdefault(k, set())
                    for j, (a, b) in enumerate(zip(o, v)):
                        if a != b:
                            d.add(nomes[j])
    res = {}
    for k, v in out.items():
        kk = f"{k[0].strip(chr(34))}|{int(k[1].strip(chr(34)))}|{int(k[2].strip(chr(34)))}|{int(k[3].strip(chr(34)))}"
        d = {n: x.strip('"') for n, x in zip(nomes, v)}
        d['cargos'] = sorted(cargos[k])
        if k in difs:
            d['difs'] = sorted(difs[k])
        res[kk] = d
    return zpath, res


def extrair(turno, zips, saida):
    zips = sorted(zips, key=lambda p: -os.path.getsize(p))
    tudo = {}
    with Pool(4) as p:
        for zp, res in p.imap_unordered(extrair_zip, zips):
            log(f'extraido {os.path.basename(zp)} {len(res)}')
            tudo.update(res)
    with gzip.open(saida, 'wt') as f:
        json.dump({'turno': str(turno), 'secoes': tudo}, f, separators=(',', ':'))
    return tudo


def ler_ou_extrair(turno, zdir, cache):
    nome = os.path.join(cache, f'bu{turno}t.json.gz')
    if os.path.exists(nome):
        log(f'cache {nome}')
        with gzip.open(nome, 'rt') as f:
            return json.load(f)['secoes']
    return extrair(turno, glob.glob(os.path.join(zdir, '*.zip')), nome)


# ---------------------------------------------------------------- utilidades

def p_dt(s):
    if not s or s.startswith('#'):
        return None
    try:
        return dt.datetime.strptime(s, '%Y-%m-%d %H:%M:%S')
    except ValueError:
        return None


def h(x):
    return x.strftime('%d/%m %H:%M:%S') if x else '-'


def fz(x, n=2):
    if x is None or (isinstance(x, float) and not math.isfinite(x)):
        return '-'
    s = f'{x:,.{n}f}'
    return s.replace(',', 'X').replace('.', ',').replace('X', '.')


def fi(x):
    return f'{x:,}'.replace(',', '.')


def tz_offset_brasilia(nome_mun, local_dt):
    """Diferença (horas) entre a hora local da cidade e a de Brasília no instante local dado; None se a cidade não está no mapa."""
    import zoneinfo
    tz = TZ_EXTERIOR.get(nome_mun)
    if tz is None or local_dt is None:
        return None
    off = local_dt.replace(tzinfo=zoneinfo.ZoneInfo(tz)).utcoffset()
    return off.total_seconds() / 3600 + 3


def regras(t, s, o, comp, cont, alt_c_off=None):
    """Regras A a D com deslocamento o (horas). alt_c_off: deslocamento só para a regra C (exterior com fuso real)."""
    dia = DIA[t]
    ab, enc, em, rec = s['ab'], s['enc'], s['em'], s['rec']
    viol = []
    sh = dt.timedelta(hours=o)
    if enc is not None and comp > 0 and enc - sh < dia.replace(hour=17):
        viol.append('A')
    if em is not None and enc is not None and em < enc:
        viol.append('B')
    oc = o if alt_c_off is None else alt_c_off
    if em is not None and rec is not None and rec < em - dt.timedelta(hours=oc):
        viol.append('C')
    if ab is not None and not cont:
        abb = ab - sh
        if abb < dia.replace(hour=7) or abb > dia.replace(hour=10):
            viol.append('D')
    return viol


def cluster_mean(y, g):
    """Média simples e erro-padrão agrupado (CR1) da média."""
    y = np.asarray(y, float); n = len(y)
    if n == 0:
        return float('nan'), float('nan'), 0
    m = y.mean()
    _, gi = np.unique(np.asarray(g), return_inverse=True)
    G = gi.max() + 1
    S = np.bincount(gi, weights=y - m, minlength=G)
    v = (S ** 2).sum() / n ** 2 * (G / (G - 1) if G > 1 else float('nan'))
    return float(m), float(math.sqrt(v)) if G > 1 else float('nan'), int(G)


def cluster_wmean(y, w, g):
    y = np.asarray(y, float); w = np.asarray(w, float)
    if len(y) == 0 or w.sum() <= 0:
        return float('nan'), float('nan')
    m = (w * y).sum() / w.sum()
    _, gi = np.unique(np.asarray(g), return_inverse=True)
    G = gi.max() + 1
    S = np.bincount(gi, weights=w * (y - m), minlength=G)
    v = (S ** 2).sum() / w.sum() ** 2 * (G / (G - 1) if G > 1 else float('nan'))
    return float(m), float(math.sqrt(v)) if G > 1 else float('nan')


# ---------------------------------------------------------------- análise

def main():
    zdir1, zdir2, base_path, cache, arqdir, saida_json, saida_txt = sys.argv[1:8]
    os.makedirs(cache, exist_ok=True)
    bu = {1: ler_ou_extrair(1, zdir1, cache), 2: ler_ou_extrair(2, zdir2, cache)}
    base = carregar(base_path)
    log(f'seções: 1T {len(bu[1])}, 2T {len(bu[2])}, base {len(base)}')
    R = {'registro': __doc__.split('Uso:')[0]}

    # ---- campos por seção e turno
    S = {1: {}, 2: {}}
    for t in (1, 2):
        for k, v in bu[t].items():
            b = base.get(k, {}).get(str(t))
            S[t][k] = {'ab': p_dt(v.get('DT_ABERTURA')), 'enc': p_dt(v.get('DT_ENCERRAMENTO')), 'em': p_dt(v.get('DT_EMISSAO_BU')),
                       'rec': p_dt(v.get('DT_BU_RECEBIDO')), 'carga': p_dt(v.get('DT_CARGA_URNA_EFETIVADA')),
                       'urna': v.get('NR_URNA_EFETIVADA'), 'c1': v.get('CD_CARGA_1_URNA_EFETIVADA'),
                       'c2': v.get('CD_CARGA_2_URNA_EFETIVADA'), 'flash': v.get('CD_FLASHCARD_URNA_EFETIVADA'),
                       'junta': v.get('NR_JUNTA_APURADORA', '-1') not in ('-1', ''), 'mun': v.get('NM_MUNICIPIO'),
                       'comp': (b['comp'] if b else int(v.get('QT_COMPARECIMENTO') or 0)),
                       'comp_bweb': int(v.get('QT_COMPARECIMENTO') or 0), 'apt': int(v.get('QT_APTOS') or 0),
                       'loc': int(v.get('NR_LOCAL_VOTACAO') or 0), 'agr': v.get('DS_SECOES_AGREGADAS'),
                       'L': b['L'] if b else None, 'R': b['R'] if b else None, 'cargos': v.get('cargos')}

    # ---- 1. relógios
    mh = {1: collections.defaultdict(collections.Counter), 2: collections.defaultdict(collections.Counter)}
    for t in (1, 2):
        for k, s in S[t].items():
            if s['ab'] is not None and not s['junta']:
                uf, mun = k.split('|')[:2]
                mh[t][(uf, mun)][s['ab'].hour] += 1
    modal = {t: {m: c.most_common(1)[0][0] for m, c in mh[t].items()} for t in (1, 2)}
    concord = collections.Counter()
    for m in set(modal[1]) | set(modal[2]):
        concord[(modal[1].get(m), modal[2].get(m))] += 1
    R['fuso_municipios'] = {f'{t}': dict(collections.Counter(('ZZ' if m[0] == 'ZZ' else 'BR', h_) for m, h_ in modal[t].items()).most_common()) for t in (1, 2)}
    R['fuso_municipios'] = {t: {f'{a}|{b}': n for (a, b), n in v.items()} for t, v in R['fuso_municipios'].items()}
    R['fuso_concordancia_turnos'] = {f'{a}|{b}': n for (a, b), n in concord.items()}
    # fração da hora modal no município
    pureza = {t: [] for t in (1, 2)}
    for t in (1, 2):
        for m, c in mh[t].items():
            pureza[t].append(c.most_common(1)[0][1] / sum(c.values()))

    def off_of(t, k):
        uf, mun = k.split('|')[:2]
        hm = modal[t].get((uf, mun))
        if hm is None:
            hm = modal[3 - t].get((uf, mun), 8)
        return hm - 8

    relogio = {}
    for t in (1, 2):
        g = collections.defaultdict(lambda: collections.defaultdict(list))
        for k, s in S[t].items():
            if s['junta']:
                continue
            grp = 'ZZ' if k.startswith('ZZ') else str(off_of(t, k))
            if s['enc'] and s['em']: g[grp]['emissao_menos_encerramento_min'].append((s['em'] - s['enc']).total_seconds() / 60)
            if s['em'] and s['rec']: g[grp]['recebimento_menos_emissao_bruto_min'].append((s['rec'] - s['em']).total_seconds() / 60)
            if s['enc']: g[grp]['encerramento_hora_local'].append(s['enc'].hour + s['enc'].minute / 60)
            if s['rec']: g[grp]['recebimento_hora'].append(s['rec'].hour + s['rec'].minute / 60)
            if s['ab']: g[grp]['abertura_hora_local'].append(s['ab'].hour + s['ab'].minute / 60)
        relogio[t] = {grp: {f: dict(zip(['min', 'p0.1', 'p1', 'p10', 'p50', 'p90', 'p99', 'p99.9', 'max', 'n'],
                                       [round(float(x), 2) for x in np.percentile(v, [0, .1, 1, 10, 50, 90, 99, 99.9, 100])] + [len(v)]))
                            for f, v in fs.items()} for grp, fs in g.items()}
    R['relogios'] = relogio

    # ---- 2. carga: distribuição por UF e turno
    carga = {}
    for t in (1, 2):
        porUF = collections.defaultdict(list)
        for k, s in S[t].items():
            if s['carga']:
                porUF[k.split('|')[0]].append(s['carga'])
        carga[t] = {}
        for uf, L in sorted(porUF.items()):
            L.sort(); n = len(L)
            q = lambda f: L[min(n - 1, int(f * n))].strftime('%d/%m')
            dias = collections.Counter(x.date() for x in L)
            carga[t][uf] = {'n': n, 'min': L[0].strftime('%d/%m %H:%M'), 'p1': q(.01), 'p5': q(.05), 'p50': q(.5), 'p95': q(.95),
                            'p99': q(.99), 'max': L[-1].strftime('%d/%m %H:%M'),
                            'antes_de_04_09': sum(1 for x in L if x < INICIO_JANELA),
                            'de_05_10_a_23_10': sum(1 for x in L if dt.datetime(2026, 10, 5) <= x < dt.datetime(2026, 10, 24)),
                            'em_24_10': dias.get(dt.date(2026, 10, 24), 0), 'em_25_10': dias.get(dt.date(2026, 10, 25), 0),
                            'em_03_10': dias.get(dt.date(2026, 10, 3), 0), 'em_04_10': dias.get(dt.date(2026, 10, 4), 0),
                            'depois_do_dia_do_turno': sum(1 for x in L if x >= DIA[t] + dt.timedelta(days=1))}
    R['carga_por_uf'] = carga
    dias_carga = {t: collections.Counter(s['carga'].strftime('%Y-%m-%d') for s in S[t].values() if s['carga']) for t in (1, 2)}
    R['carga_por_dia'] = {t: dict(sorted(v.items())) for t, v in dias_carga.items()}

    # ---- 3. troca de urna e recarga entre os turnos
    troca = {}; mesma_carga = collections.Counter()
    for k in set(S[1]) & set(S[2]):
        u1, u2 = S[1][k]['urna'], S[2][k]['urna']
        if u1 and u2 and u1 not in ('0', '-1') and u2 not in ('0', '-1'):
            troca[k] = (u1 != u2)
            if u1 == u2:
                mesma_carga[(S[1][k]['c1'] == S[2][k]['c1'], S[1][k]['carga'] == S[2][k]['carga'])] += 1
    R['troca_entre_turnos'] = {'secoes_com_urna_nos_dois': len(troca), 'urna_diferente': sum(troca.values()),
                               'mesma_urna_carga_igual_codigo_e_data': {f'{a}|{b}': n for (a, b), n in mesma_carga.items()}}

    def cont_marca(t, k):
        s = S[t][k]
        a = troca.get(k, False)
        b = s['carga'] is not None and s['carga'].date() == DIA[t].date()
        c = (t == 2 and s['carga'] is not None and s['carga'] >= dt.datetime(2026, 10, 5))
        return a, b, c

    # ---- 4. regras, explicações
    imp = {1: [], 2: []}
    contagem = {}
    tzver = None
    try:
        tzver = open('/usr/share/zoneinfo/tzdata.zi').readline().strip()
    except OSError:
        pass
    R['tz_versao'] = tzver
    excl_D = {1: [], 2: []}        # abertura fora de 7h a 10h com marca de contingência (fora da regra D por definição)
    carga_pos_abertura = {1: [], 2: []}
    for t in (1, 2):
        cnt = collections.Counter()
        for k, s in S[t].items():
            cnt['secoes'] += 1
            ca, cb, cc = cont_marca(t, k)
            cont = ca or cb
            o = off_of(t, k)
            ext = k.startswith('ZZ')
            if s['junta'] or (s['ab'] is None and s['enc'] is None):
                cnt['junta_ou_sem_horario'] += 1
                v = []
            else:
                v = regras(t, s, o, s['comp'], cont)
                if s['ab'] is not None and cont:
                    abb = s['ab'] - dt.timedelta(hours=o)
                    if abb < DIA[t].replace(hour=7) or abb > DIA[t].replace(hour=10):
                        excl_D[t].append({'k': k, 'ab_brasilia': h(abb), 'carga': h(s['carga']), 'troca': ca, 'carga_no_dia': cb,
                                          'urna': s['urna'], 'urna_outro_turno': S[3 - t].get(k, {}).get('urna')})
            if s['carga'] is not None and s['ab'] is not None and s['carga'] > s['ab']:
                carga_pos_abertura[t].append({'k': k, 'carga': h(s['carga']), 'ab': h(s['ab']), 'troca': ca, 'carga_no_dia': cb,
                                              'urna': s['urna'], 'urna_outro_turno': S[3 - t].get(k, {}).get('urna')})
            if s['carga'] is None:
                cnt['sem_data_de_carga'] += 1
            elif s['carga'] < INICIO_JANELA or s['carga'] >= DIA[t] + dt.timedelta(days=1):
                v = v + ['E']
            if not v:
                continue
            ex = []
            if s['junta']:
                ex.append('junta')
            fuso_ok = False; fuso_alt = None; fuso_estrito = False
            if any(x in 'ACD' for x in v) and not s['junta'] and s['ab'] is not None:
                if ext:
                    off_real = tz_offset_brasilia(s['mun'], s['em'] or s['enc'])
                    if off_real is not None:
                        v2 = regras(t, s, o, s['comp'], cont, alt_c_off=off_real)
                        if not any(x in 'ACD' for x in v2):
                            fuso_ok = True; fuso_alt = off_real; fuso_estrito = True
                else:
                    for o2 in OFFS_BR:
                        if o2 == o:
                            continue
                        v2 = regras(t, s, o2, s['comp'], cont)
                        if not any(x in 'ACD' for x in v2):
                            fuso_ok = True; fuso_alt = o2
                            abb2 = s['ab'] - dt.timedelta(hours=o2)
                            # robustez fora do registro: com o fuso alternativo a abertura cai na hora normal (7h a 9h)
                            fuso_estrito = DIA[t].replace(hour=7) <= abb2 <= DIA[t].replace(hour=9)
                            break
            if fuso_ok and all(x in 'ACD' for x in v):
                ex.append('fuso')
            if cont:
                ex.append('contingencia')
            rec = {'k': k, 't': t, 'regras': v, 'explicacao': ex, 'fuso_estrito': fuso_estrito if 'fuso' in ex else None,
                   'cont_a_troca': ca, 'cont_b_carga_no_dia': cb, 'cont_c_carga_2t_pos_1t': cc, 'fuso_mun': o, 'fuso_alt': fuso_alt,
                   'mun': s['mun'], 'ab': h(s['ab']), 'enc': h(s['enc']), 'em': h(s['em']), 'rec': h(s['rec']),
                   'carga': s['carga'].strftime('%d/%m/%Y %H:%M') if s['carga'] else None, 'urna': s['urna'],
                   'urna_outro_turno': S[3 - t].get(k, {}).get('urna'), 'flash': s['flash'], 'comp': s['comp'],
                   'comp_outro_turno': S[3 - t].get(k, {}).get('comp'), 'apt': s['apt'], 'L': s['L'], 'R': s['R'],
                   'loc': s['loc'], 'agr': s['agr']}
            if s['ab'] is not None:
                rec['ab_brasilia'] = h(s['ab'] - dt.timedelta(hours=o))
            if s['enc'] is not None:
                rec['enc_brasilia'] = h(s['enc'] - dt.timedelta(hours=o))
            if s['em'] is not None:
                rec['em_brasilia'] = h(s['em'] - dt.timedelta(hours=o))
            if s['em'] is not None and s['rec'] is not None:
                rec['rec_menos_em_brasilia_s'] = (s['rec'] - (s['em'] - dt.timedelta(hours=o))).total_seconds()
                if ext and fuso_alt is not None:
                    rec['rec_menos_em_fuso_real_s'] = (s['rec'] - (s['em'] - dt.timedelta(hours=fuso_alt))).total_seconds()
            if s['em'] is not None and s['enc'] is not None:
                rec['em_menos_enc_s'] = (s['em'] - s['enc']).total_seconds()
            imp[t].append(rec)
            for x in v:
                cnt['regra_' + x] += 1
        contagem[t] = cnt
    R['contagem'] = {t: dict(c) for t, c in contagem.items()}
    R['abertura_fora_com_contingencia'] = excl_D
    R['carga_depois_da_abertura'] = carga_pos_abertura

    # ---- 5. virada de Lula por seção e comparação com o local (e com o município, descritivo)
    def okLR(k):
        b = base.get(k)
        if not b or '1' not in b or '2' not in b:
            return None
        L1, R1, L2, R2 = b['1']['L'], b['1']['R'], b['2']['L'], b['2']['R']
        if L1 + R1 <= 0 or L2 + R2 <= 0:
            return None
        return np.array([L1, R1, L2, R2], float)
    loc_tot = collections.defaultdict(lambda: np.zeros(4)); mun_tot = collections.defaultdict(lambda: np.zeros(4))
    chave_loc = {}; X = {}
    for k in base:
        x = okLR(k)
        if x is None:
            continue
        X[k] = x
        ck = '|'.join(k.split('|')[:3]) + f"|{base[k]['2']['loc']}"
        chave_loc[k] = ck
        loc_tot[ck] += x
        mun_tot['|'.join(k.split('|')[:2])] += x

    def vir(x):
        return 100 * (x[2] / (x[2] + x[3]) - x[0] / (x[0] + x[1]))
    dsec = {}; dmun = {}
    for k, x in X.items():
        o_ = loc_tot[chave_loc[k]] - x
        if o_[0] + o_[1] > 0 and o_[2] + o_[3] > 0:
            dsec[k] = (vir(x) - vir(o_), vir(x), vir(o_), x[2] + x[3])
        m_ = mun_tot['|'.join(k.split('|')[:2])] - x
        if m_[0] + m_[1] > 0 and m_[2] + m_[3] > 0:
            dmun[k] = vir(x) - vir(m_)
    dall = np.array([v[0] for v in dsec.values()])
    acaso = {'secoes_com_d': int(len(dall)), 'media': float(dall.mean()), 'dp': float(dall.std()),
             'fracao_d_maior_igual_3': float((dall >= 3).mean())}
    faixas = [(0, 50), (50, 100), (100, 200), (200, 400), (400, 10 ** 9)]
    acaso['por_faixa'] = {}
    for a, b_ in faixas:
        sel = np.array([v[0] for v in dsec.values() if a < v[3] <= b_])
        if len(sel):
            acaso['por_faixa'][f'{a + 1}-{b_ if b_ < 10 ** 9 else "mais"}'] = {'n': int(len(sel)), 'dp': float(sel.std()),
                                                                               'fracao_d_ge_3': float((sel >= 3).mean())}
    R['acaso_d'] = acaso

    def faixa_frac(vf):
        for a, b_ in faixas:
            if a < vf <= b_:
                return acaso['por_faixa'][f'{a + 1}-{b_ if b_ < 10 ** 9 else "mais"}']['fracao_d_ge_3']
        return acaso['fracao_d_maior_igual_3']

    for t in (1, 2):
        for r in imp[t]:
            v = dsec.get(r['k'])
            r['d'] = None if v is None else round(v[0], 3)
            r['virada_secao'] = None if v is None else round(v[1], 3)
            r['virada_outras'] = None if v is None else round(v[2], 3)
            r['votos_finalistas_2t'] = None if v is None else int(v[3])
            r['local'] = chave_loc.get(r['k'])
            r['d_municipio'] = None if r['k'] not in dmun else round(dmun[r['k']], 3)
            if r['virada_secao'] is None and r['k'] in X:
                r['virada_secao'] = round(vir(X[r['k']]), 3)
                r['votos_finalistas_2t'] = int(X[r['k']][2] + X[r['k']][3])

    # ---- 6. grupos (descritivo) e veredito
    def grupo(t, r):
        terr = 'exterior' if r['k'].startswith('ZZ') else 'Brasil'
        return f"{terr} | regras {'+'.join(r['regras'])} | {'+'.join(r['explicacao']) or 'sem explicação'}"
    grupos = {}
    for t in (1, 2):
        G = collections.defaultdict(list)
        for r in imp[t]:
            G[grupo(t, r)].append(r)
        grupos[t] = {}
        for g, L in sorted(G.items(), key=lambda x: -len(x[1])):
            com = [r for r in L if r['d'] is not None]
            m = cluster_mean([r['d'] for r in com], [r['local'] for r in com]) if com else (float('nan'), float('nan'), 0)
            gaps = [r['rec_menos_em_brasilia_s'] for r in L if 'rec_menos_em_brasilia_s' in r]
            grupos[t][g] = {'n': len(L), 'com_d': len(com), 'media_d': m[0], 'ep_media_d': m[1],
                            'ufs': dict(collections.Counter(r['k'].split('|')[0] for r in L).most_common()),
                            'rec_menos_em_s_min_max': [min(gaps), max(gaps)] if gaps else None}
    R['grupos'] = grupos

    sem = [r for r in imp[2] if not r['explicacao']]
    sem_d = [r for r in sem if r['d'] is not None]
    d_ge3 = [r for r in sem_d if r['d'] >= 3]
    gm = cluster_mean([r['d'] for r in sem_d], [r['local'] for r in sem_d])
    gw = cluster_wmean([r['d'] for r in sem_d], [r['votos_finalistas_2t'] for r in sem_d], [r['local'] for r in sem_d])
    n_sem = len(sem)
    p_algum = 1 - float(np.prod([1 - faixa_frac(r['votos_finalistas_2t']) for r in sem_d])) if sem_d else 0.0
    if n_sem >= 100:
        ver = 'INCOERÊNCIA'; mot = f'{n_sem} seções impossíveis sem explicação no 2º turno (limite 100)'
    elif d_ge3:
        ver = 'INCOERÊNCIA'
        mot = (f'{n_sem} seções impossíveis sem explicação no 2º turno (abaixo de 100), e {len(d_ge3)} delas com virada de Lula '
               f'3 pontos ou mais acima das outras seções do mesmo local (leitura literal, seção a seção)')
    elif n_sem == 0:
        ver = 'COERENTE'; mot = 'nenhuma seção impossível sem explicação no 2º turno'
    else:
        ver = 'INCONCLUSIVO'; mot = f'{n_sem} seções impossíveis sem explicação, abaixo de 100, nenhuma com virada 3 pontos acima do local'
    if n_sem >= 100 or (sem_d and gm[0] >= 3):
        ver_grupo = 'INCOERÊNCIA'
    elif n_sem == 0:
        ver_grupo = 'COERENTE'
    else:
        ver_grupo = 'INCONCLUSIVO'
    sem1 = [r for r in imp[1] if not r['explicacao']]
    sem1_estrito = [r for r in imp[1] if not r['explicacao'] or (r['explicacao'] == ['fuso'] and not r['fuso_estrito'])]
    sem2_estrito = [r for r in imp[2] if not r['explicacao'] or (r['explicacao'] == ['fuso'] and not r['fuso_estrito'])]
    R['veredito'] = {'letra': ver, 'motivo': mot, 'leitura_em_grupo': ver_grupo,
                     'n_impossiveis_2t': len(imp[2]), 'n_sem_explicacao_2t': n_sem, 'n_sem_explicacao_com_d': len(sem_d),
                     'n_d_ge_3': len(d_ge3), 'secoes_d_ge_3': [r['k'] for r in d_ge3],
                     'media_d': gm[0], 'ep_media_d': gm[1], 'locais': gm[2],
                     'media_d_ponderada': gw[0], 'ep_media_d_ponderada': gw[1],
                     'prob_acaso_alguma_d_ge_3': p_algum,
                     'n_impossiveis_1t': len(imp[1]), 'n_sem_explicacao_1t': len(sem1),
                     'n_sem_explicacao_1t_fuso_estrito': len(sem1_estrito), 'n_sem_explicacao_2t_fuso_estrito': len(sem2_estrito)}
    # descritivo: extremos de d contra o município entre as sem explicação do 2º turno
    ext_m = []
    dm_arr = np.array([dmun[k] for k in dmun]); vf_arr = np.array([X[k][2] + X[k][3] for k in dmun])
    com_m = [r for r in sem if r['d_municipio'] is not None]
    if com_m:
        for r in (max(com_m, key=lambda r: r['d_municipio']), min(com_m, key=lambda r: r['d_municipio'])):
            pre = '|'.join(r['k'].split('|')[:2]) + '|'
            vs = sorted(vir(x) for kk, x in X.items() if kk.startswith(pre))
            ext_m.append({'k': r['k'], 'mun': r['mun'], 'd_municipio': r['d_municipio'], 'virada_secao': r['virada_secao'],
                          'secoes_municipio': len(vs), 'dp_virada_municipio': float(np.std(vs)),
                          'posicao': 1 + sum(1 for v_ in vs if v_ > r['virada_secao'] + 1e-9),
                          'L1R1L2R2': [int(v_) for v_ in X[r['k']]]})
            vfr = X[r['k']][2] + X[r['k']][3]
            fa = [(a_, b_) for a_, b_ in faixas if a_ < vfr <= b_][0]
            sel = dm_arr[(vf_arr > fa[0]) & (vf_arr <= fa[1])]
            fr = float((sel >= r['d_municipio']).mean()) if r['d_municipio'] > 0 else float((sel <= r['d_municipio']).mean())
            ext_m[-1].update({'faixa_votos': f'{fa[0] + 1}-{fa[1]}', 'secoes_na_faixa': int(len(sel)), 'freq_tao_extremo_na_faixa': fr,
                              'prob_alguma_entre_as_sem_explicacao': 1 - (1 - fr) ** len(com_m), 'n_sem_explicacao_com_d_mun': len(com_m)})
    R['veredito']['extremos_municipio_2t'] = ext_m
    recs2 = sorted(s_['rec'] for k_, s_ in S[2].items() if s_['rec'] is not None and not k_.startswith('ZZ'))
    lim = DIA[2].replace(hour=17, minute=10)
    R['recebimento_2t'] = {'brasil_ate_17h10': sum(1 for x in recs2 if x < lim), 'primeiro': h(recs2[0]),
                           'primeiro_depois_de_17h10': h(min(x for x in recs2 if x >= lim))}
    R['impossiveis'] = {t: imp[t] for t in (1, 2)}
    with open(saida_json, 'w') as f:
        json.dump(R, f, ensure_ascii=False, indent=1, default=str)
    log(f'json gravado {saida_json}')
    escrever_txt(R, imp, saida_txt, arqdir)
    log(f'texto gravado {saida_txt}')


# ---------------------------------------------------------------- log da urna (amostra), para as seções que tiverem

def eventos_log(arqdir, k, dia):
    if not arqdir or arqdir == '-':
        return None
    uf, mun, zona, sec = k.split('|')
    pasta = os.path.join(arqdir, uf.lower(), f'{int(mun):05d}', f'{int(zona):04d}', f'{int(sec):04d}')
    if not os.path.isdir(pasta):
        return None
    logs = sorted(a for a in os.listdir(pasta) if a.endswith('-log.jez'))
    if not logs:
        return None
    from decodificar import _linhas_log
    out = []
    for bl in _linhas_log(os.path.join(pasta, logs[-1])):
        for l in bl:
            if l.startswith(dia) and any(x in l for x in ('Gerando relatório [BU] [INÍCIO]', 'Mídia de resultado retirada',
                                                          'Votação encerrada', 'Inicio do Encerramento', 'Urna pronta para receber votos',
                                                          'contingência')):
                c = l.split('\t')
                out.append(f'{c[0]} {c[4]}')
    return out


# ---------------------------------------------------------------- texto

def escrever_txt(R, imp, saida_txt, arqdir):
    V = R['veredito']; C = R['contagem']; A = R['acaso_d']
    L = []
    w = L.append
    w('L1. Horários impossíveis em todas as seções, bweb dos dois turnos de 2026 (Adendo 18)')
    w('Script: scripts/analisar_L1.py. Números completos e a lista de todas as seções impossíveis: resultados/L1_horarios.json.')
    w('Bases: bweb do 1º turno (28 zips de 05/10/2026 14h03) e do 2º turno (28 zips de 26/10/2026 07h42), todos os cargos, uma linha')
    w('por seção (campos de horário, carga e urna); votos de presidente por seção dos dois turnos (secoes2026.json.gz).')
    w('')
    w('Critério registrado (PRE-REGISTRO-2026-10-26.md, Adendo 18, L1, antes de rodar):')
    w('  "Impossível: encerramento antes das 17h00 de Brasília com comparecimento acima de zero; emissão do boletim antes do')
    w('  encerramento; recebimento antes da emissão; abertura antes das 7h ou depois das 10h de Brasília sem urna de contingência;')
    w('  carga fora da janela de carga do turno na UF." "Sinal: 100 ou mais seções impossíveis no 2º turno sem explicação por fuso,')
    w('  contingência ou junta, ou qualquer número delas em que a virada de Lula supere a das outras seções do mesmo local em 3 pontos')
    w('  ou mais. Sem sinal: nenhuma seção impossível sem explicação. Entre os dois: inconclusivo, com a lista das seções para conferência."')
    w('')
    w(f"VEREDITO PELA LETRA: {V['letra']}")
    w(f"Motivo: {V['motivo']}.")
    w(f"Na leitura em grupo do mesmo trecho (média das seções sem explicação): {V['leitura_em_grupo']}.")
    w('')
    sem2 = [r for r in imp[2] if not r['explicacao']]
    w('Resumo')
    w(f"- 2º turno: {fi(C[2]['secoes'])} seções; {fi(V['n_impossiveis_2t'])} violam alguma regra; {V['n_sem_explicacao_2t']} ficam sem explicação por fuso,")
    w(f"  contingência ou junta. As outras {fi(V['n_impossiveis_2t'] - V['n_sem_explicacao_2t'])} são do exterior, onde a hora local da cidade é")
    w('  comparada com o recebimento em hora de Brasília; com o fuso real de cada cidade, todas ficam possíveis.')
    w(f"- As {V['n_sem_explicacao_2t']} do 2º turno formam dois grupos: {sum(1 for r in sem2 if r['regras'] == ['D'])} abriram depois das 10h (atraso, sem troca de urna),")
    w(f"  {sum(1 for r in sem2 if r['regras'] == ['C'])} tiveram o boletim recebido pelo TSE de 5 a 52 segundos antes da hora de emissão marcada pela urna")
    w('  (relógio da urna adiantado; todas recebidas entre 17h05 e 17h07, as transmissões mais rápidas do país).')
    w(f"- Nenhum encerramento antes das 17h, nenhuma emissão antes do encerramento e nenhuma carga fora da janela, nos dois turnos.")
    w(f"- O gatilho do sinal: {V['n_d_ge_3']} das {V['n_sem_explicacao_com_d']} seções sem explicação com seção de comparação no local tem virada de Lula")
    w(f"  3 pontos ou mais acima das outras do local ({', '.join(V['secoes_d_ge_3'])}). Média das {V['n_sem_explicacao_com_d']}: {fz(V['media_d'])} ponto")
    w(f"  (ep {fz(V['ep_media_d'])}, {V['locais']} locais); ponderada pelos votos: {fz(V['media_d_ponderada'])} (ep {fz(V['ep_media_d_ponderada'])}).")
    w(f"  Probabilidade de pelo menos uma de {V['n_sem_explicacao_com_d']} seções ter d >= 3 só pelo acaso (frequência de d >= 3 entre todas as")
    w(f"  seções da mesma faixa de votos): {fz(100 * V['prob_acaso_alguma_d_ge_3'], 0)}%.")
    w(f"- 1º turno, mesma régua, mesma eleição: {fi(V['n_impossiveis_1t'])} violam alguma regra e {V['n_sem_explicacao_1t']} ficam sem explicação")
    w(f"  ({V['n_sem_explicacao_1t_fuso_estrito']} se a explicação por fuso exigir abertura normal depois do ajuste; ver item 4). Os dois turnos")
    w(f"  têm o mesmo tipo e quase o mesmo número de casos ({V['n_sem_explicacao_2t']} no 2º).")
    dm = [r['d_municipio'] for r in sem2 if r['d_municipio'] is not None]
    w(f"- Descritivo, fora do registro: contra as outras seções do município, as {len(dm)} sem explicação do 2º turno têm d médio de")
    em_ = V['extremos_municipio_2t']
    w(f"  {fz(float(np.mean(dm)))} ponto (de {fz(min(dm))} a {fz(max(dm))}); a maior a favor de Lula é {em_[0]['k']} ({em_[0]['mun']}), a maior a")
    w(f"  favor de Flávio é {em_[1]['k']} ({em_[1]['mun']}); as duas não têm outra seção no mesmo local e ficam fora da medida registrada (item 6).")
    w('')

    # 1. relógios
    w('1. Em que relógio está cada campo (verificado antes de aplicar as regras)')
    for t in (1, 2):
        rl = R['relogios'][t]
        w(f'  {t}º turno, por grupo de deslocamento do município (0 = Brasília; ZZ = exterior):')
        for g in sorted(rl, key=lambda x: (x == 'ZZ', x)):
            x = rl[g]
            e = x.get('emissao_menos_encerramento_min', {}); r_ = x.get('recebimento_menos_emissao_bruto_min', {})
            enc = x.get('encerramento_hora_local', {}); rh = x.get('recebimento_hora', {})
            w(f"    {g:>3}: {fi(e.get('n', 0))} seções; emissão menos encerramento (min) p1 {fz(e.get('p1'), 1)}, mediana {fz(e.get('p50'), 1)}, "
              f"p99 {fz(e.get('p99'), 1)}; encerramento local mediano {fz(enc.get('p50'), 2)} h; recebimento (relógio do TSE) "
              f"p1 {fz(rh.get('p1'), 2)} h, mediana {fz(rh.get('p50'), 2)} h; recebimento menos emissão bruta, mínimo {fz(r_.get('min'), 1)} min")
    w('  Leitura: abertura, encerramento e emissão estão no relógio da urna, em hora local (a emissão vem cerca de 2 minutos depois')
    w('  do encerramento em todos os fusos; o encerramento mediano é 17h, 16h e 15h nos fusos 0, -1 e -2). O recebimento está em')
    w('  hora de Brasília: a hora de recebimento tem a mesma distribuição em todos os fusos, e o menor intervalo bruto entre emissão e')
    w('  recebimento é de cerca de 1 hora no fuso -1 e de 2 horas no fuso -2, a diferença de fuso. A carga está em hora local (as cargas')
    w('  do AC se concentram das 8h às 17h locais, com a pausa do almoço ao meio-dia, como no resto do país).')
    fm = R['fuso_municipios']['2']
    w(f"  Fuso dos municípios (hora modal de abertura): {', '.join(f'{k} {fi(v)}' for k, v in fm.items())} "
      f"(BR|8 = Brasília; BR|7 = MT, MS, RO, RR e parte do AM; BR|6 = AC e oeste do AM; BR|9 = Fernando de Noronha; ZZ|8 = exterior, hora local).")
    w(f"  O fuso modal é o mesmo nos dois turnos em todos os municípios: {R['fuso_concordancia_turnos']}.")
    w(f"  Base de fusos do exterior: {R['tz_versao']} (a Europa saiu do horário de verão na madrugada de 25/10/2026; os EUA só em 01/11).")
    w('')

    # 2. janela de carga
    w('2. Janela oficial de carga e datas de carga por UF')
    w('  O que diz a norma (fontes no fim):')
    w('  - Calendário eleitoral de 2026 (Res. TSE 23.760/2026): não fixa data nacional para a carga das urnas.')
    w('  - Sistemas assinados digitalmente e lacrados no TSE em 04/09/2026; a carga só pode usar os sistemas lacrados. Cada TRE marca as')
    w('    cerimônias de carga das suas zonas, com convocação dos partidos, MP e OAB pelo menos 2 dias antes (art. 100 da Res. TSE 23.751/2026).')
    w('  - 2º turno: as urnas são as mesmas do 1º; recebem só a nova mídia de resultado, e os lacres são mantidos, menos o da mídia de')
    w('    resultado (art. 108 da Res. 23.751/2026; TRE-PB: "não exige uma nova carga"; TRE-MG: "as urnas são as mesmas"). Se a preparação')
    w('    falha, faz-se nova carga ou prepara-se nova urna (art. 109). No dia, a urna que falha é trocada pela de contingência (arts. 99 a 101).')
    w('  - Cronogramas estaduais achados na imprensa: 1º turno, SE de 18 a 28/09, MT 21 e 22/09 na capital, SP a partir de 23/09; preparação')
    w('    do 2º turno, PR de 12 a 20/10, BA de 14 a 22/10, CE de 14 a 16/10, PB até 16/10, MS até 17/10, SP até 23/10.')
    w('  Janela aplicada (leitura declarada): 1º turno, de 04/09/2026 até o fim de 04/10/2026; 2º turno, de 04/09/2026 até o fim de 25/10/2026,')
    w('  porque a urna do 2º turno guarda a carga feita para o 1º (art. 108) e as cargas novas (art. 109, contingência) vêm depois do 1º turno.')
    w('  O que os dados mostram:')
    cd = R['carga_por_dia']
    for t in (1, 2):
        dd = cd[t]
        tot = sum(dd.values())
        set_ = sum(v for k, v in dd.items() if k < '2026-10-01')
        w(f"  - {t}º turno: {fi(tot)} seções com data de carga; primeira {min(dd)}, última {max(dd)}; antes de 01/10: {fi(set_)} "
          f"({fz(100 * set_ / tot, 2)}%).")
    d2 = cd[2]
    out_ = sum(v for k, v in d2.items() if '2026-10-05' <= k <= '2026-10-23')
    w(f"    No 2º turno, {fi(out_)} seções têm carga de 05/10 a 23/10 (urnas recarregadas ou novas na preparação do 2º turno, art. 109),")
    w(f"    {fi(d2.get('2026-10-24', 0))} têm carga na véspera (24/10) e {fi(d2.get('2026-10-25', 0))} no próprio dia 25/10.")
    c24 = {uf: v['em_24_10'] for uf, v in R['carga_por_uf'][2].items() if v['em_24_10']}
    w(f"    Véspera por UF: {', '.join(f'{uf} {n}' for uf, n in sorted(c24.items(), key=lambda x: -x[1]))}.")
    w('    O padrão (cerca de 20 por UF e mais nas UFs grandes) é o do teste de integridade: a urna sorteada sai da seção na véspera e outra')
    w('    é carregada para a seção (o 2º turno teve 20 urnas na maior parte das UFs, 27 em PR, RS, PE e CE e 33 em SP, MG, RJ e BA, segundo a')
    w('    Agência Brasil); 706 das 709 têm número de urna diferente do 1º turno.')
    c03 = {uf: v['em_03_10'] for uf, v in R['carga_por_uf'][1].items() if v['em_03_10']}
    w(f"    1º turno, véspera (03/10) por UF: {', '.join(f'{uf} {n}' for uf, n in sorted(c03.items(), key=lambda x: -x[1]))}.")
    w('  Datas de carga por UF (percentis 1, 50 e 99; mínimo e máximo):')
    for t in (1, 2):
        w(f'   {t}º turno:')
        for uf, v in R['carga_por_uf'][t].items():
            w(f"    {uf}: n {fi(v['n'])}; mín {v['min']}; p1 {v['p1']}; mediana {v['p50']}; p99 {v['p99']}; máx {v['max']}"
              + (f"; de 05 a 23/10: {v['de_05_10_a_23_10']}; 24/10: {v['em_24_10']}; 25/10: {v['em_25_10']}" if t == 2 else
                 f"; 03/10: {v['em_03_10']}; 04/10: {v['em_04_10']}"))
    T_ = R['troca_entre_turnos']
    w(f"  Urna efetivada diferente entre os turnos: {fi(T_['urna_diferente'])} de {fi(T_['secoes_com_urna_nos_dois'])} seções. Nas que mantiveram a urna,")
    w(f"  código e data da carga iguais nos dois turnos: {fi(T_['mesma_urna_carga_igual_codigo_e_data'].get('True|True', 0))}; os dois diferentes (urna")
    w(f"  recarregada entre os turnos): {fi(T_['mesma_urna_carga_igual_codigo_e_data'].get('False|False', 0))}.")
    w('')

    # 3. contagem
    w('3. Contagem por regra')
    for t in (1, 2):
        c = C[t]
        w(f"  {t}º turno: A (encerramento antes das 17h) {c.get('regra_A', 0)}; B (emissão antes do encerramento) {c.get('regra_B', 0)}; "
          f"C (recebimento antes da emissão) {c.get('regra_C', 0)}; D (abertura antes das 7h ou depois das 10h, sem contingência) "
          f"{c.get('regra_D', 0)}; E (carga fora da janela) {c.get('regra_E', 0)}; junta ou sem horário {c.get('junta_ou_sem_horario', 0)}; "
          f"sem data de carga {c.get('sem_data_de_carga', 0)}.")
        ex = R['abertura_fora_com_contingencia'][t]
        w(f"     Abertura fora de 7h a 10h que a regra D deixa de fora por ter marca de contingência: {len(ex)}"
          + (': ' + '; '.join(f"{e['k']} abriu {e['ab_brasilia'][6:]} (Brasília), carga {e['carga']}, urna {e['urna']} (outro turno {e['urna_outro_turno']})" for e in ex) if ex else '') + '.')
        cp = R['carga_depois_da_abertura'][t]
        w(f"     Fora do registro: carga da urna efetivada depois da abertura do mesmo boletim: {len(cp)}"
          + (': ' + '; '.join(f"{e['k']} carga {e['carga']}, abertura {e['ab']}, troca {'sim' if e['troca'] else 'não'}, carga no dia {'sim' if e['carga_no_dia'] else 'não'}" for e in cp) if cp else '') + '.')
        w('     (A urna que recebe a mídia de votação de outra no meio do dia traz a abertura da primeira; é o retrato da contingência.)')
    w('')

    # 4. grupos
    w('4. Grupos de seções impossíveis e explicação de cada um')
    for t in (1, 2):
        w(f'  {t}º turno:')
        for g, x in R['grupos'][t].items():
            w(f"    {g}: {x['n']} seções; UFs {x['ufs']}; recebimento menos emissão (s, Brasília pelo fuso do município) "
              f"{x['rec_menos_em_s_min_max']}; d médio {fz(x['media_d'])} (ep {fz(x['ep_media_d'])}, {x['com_d']} com comparação)")
    w('  Explicação de cada grupo:')
    w('  - Exterior, regra C, explicada por fuso: a urna marca a emissão na hora local da cidade e o TSE marca o recebimento em hora de')
    w('    Brasília. Nas cidades a leste de Brasília (Europa, África, Ásia, Oceania) a emissão "acontece depois" do recebimento no relógio')
    w('    bruto. Com o fuso real de cada cidade, todas passam a ter recebimento depois da emissão.')
    w('  - Brasil, regra C, sem explicação (2º turno, 8 seções; 1º turno, 4): recebimento de 5 a 150 segundos antes da emissão marcada pela')
    w('    urna, sempre nas transmissões mais rápidas (boletim recebido nos primeiros minutos depois das 17h). O relógio da urna é acertado')
    w('    na carga e anda sozinho por semanas; um relógio alguns segundos ou minutos adiantado faz isso quando a transmissão é imediata.')
    w('    Quatro das 8 do 2º turno são da zona 16 de Afuá (PA), todas carregadas em 22/09 no mesmo dia; a mesma zona tem uma no 1º turno.')
    rc = R['recebimento_2t']
    w(f"    No 2º turno o recebimento parou depois das 17h10 (pausa da totalização): {fi(rc['brasil_ate_17h10'])} boletins do Brasil chegaram")
    w(f"    até 17h10 (o primeiro às {rc['primeiro'][6:]}) e o seguinte só às {rc['primeiro_depois_de_17h10'][6:]}; as 8 estão entre esses primeiros.")
    w('  - Brasil, regra D, sem explicação: abertura depois das 10h sem troca de urna e sem carga no dia (atraso de abertura). Não é o')
    w('    que a urna faz sozinha: a abertura é comandada pela mesa. O registro chama de "impossível", mas atraso de abertura acontece; os')
    w('    casos estão listados abaixo para conferência na ata da seção.')
    w('  - Brasil, regra C ou D, explicada por fuso (1º turno): o relógio da urna estava em outro fuso. 53 são da zona 53 do MT (Querência,')
    w('    Bom Jesus do Araguaia e Serra Nova Dourada) com o relógio em hora de Brasília; uma em Sapiranga (RS) com o relógio 1 hora')
    w('    adiantado (com troca de urna entre os turnos); duas em Maués (AM). Na leitura estrita (fora do registro: depois do ajuste de fuso')
    w('    a abertura tem de cair entre 7h e 9h de Brasília), as 10 aberturas tardias do 1º turno "explicadas" por um relógio 1 hora')
    w('    adiantado deixam de ser explicadas: são atrasos de abertura com encerramento tardio por fila, não fuso.')
    w('  - Contingência (marca a ou b) junto com fuso: seções do exterior e do Brasil com troca de urna entre os turnos.')
    w('')

    # 5. lista das sem explicação
    w('5. Lista das seções impossíveis sem explicação (para conferência)')
    w('  Horas de abertura, encerramento e emissão convertidas para Brasília pelo fuso do município; recebimento no relógio do TSE.')
    w('  d local = virada da seção menos a das outras seções do local (a medida do registro); d município = o mesmo contra as outras')
    w('  seções do município (descritivo, fora do registro).')
    for t in (2, 1):
        w(f'  {t}º turno:')
        sem = [r for r in imp[t] if not r['explicacao'] or (t == 1 and r['explicacao'] == ['fuso'] and not r['fuso_estrito'])]
        for r in sorted(sem, key=lambda r: (r['regras'], r['k'])):
            tag = '' if not r['explicacao'] else ' [explicada por fuso só na leitura do registro]'
            gap = r.get('rec_menos_em_brasilia_s')
            w(f"    {r['k']} {r['mun']} | regra {'+'.join(r['regras'])}{tag} | abertura {r.get('ab_brasilia', '-')[6:]}, encerramento "
              f"{r.get('enc_brasilia', '-')[6:]}, emissão {r.get('em_brasilia', '-')[6:]}, recebimento {r['rec'][6:]}"
              + (f", recebimento menos emissão {gap:+.0f} s" if gap is not None and 'C' in r['regras'] else '')
              + f" | carga {r['carga']} | urna {r['urna']} (outro turno {r['urna_outro_turno']}) | comparecimento {r['comp']} "
              f"(outro turno {r['comp_outro_turno']}) de {r['apt']} | virada da seção {fz(r['virada_secao'])}, d local {fz(r['d'])}, "
              f"d município {fz(r['d_municipio'])}")
            ev = eventos_log(arqdir, r['k'], '25/10/2026' if t == 2 else '04/10/2026')
            if ev:
                w('       log da urna (amostra): ' + '; '.join(ev[-4:]))
    w('')

    # 6. o gatilho
    w('6. O gatilho da virada (3 pontos acima do local)')
    for k in V['secoes_d_ge_3']:
        r = [x for x in imp[2] if x['k'] == k][0]
        w(f"  {k} ({r['mun']}): {r['votos_finalistas_2t']} votos nos finalistas no 2º turno; virada da seção {fz(r['virada_secao'])}; das")
        w(f"  outras do local {fz(r['virada_outras'])}; d {fz(r['d'])}. Comparecimento {r['comp_outro_turno']} no 1º turno e {r['comp']} no 2º.")
    w('  A seção 133 de Inácio Martins (PR) votou com 18 eleitores no 2º turno (170 no 1º). A única outra seção do local, a 189, também')
    w('  abriu depois das 10h e tem d de -6,51: as duas se espelham. Com 18 votos a fatia de Lula muda 5,6 pontos por voto. Nas seções de')
    w(f"  até 50 votos nos finalistas, o desvio-padrão de d é {fz(A['por_faixa']['1-50']['dp'])} pontos e {fz(100 * A['por_faixa']['1-50']['fracao_d_ge_3'], 0)}% delas")
    w(f"  têm d >= 3 (em todas as seções: dp {fz(A['dp'])}, {fz(100 * A['fracao_d_maior_igual_3'], 1)}% com d >= 3). O gatilho dispara pelo acaso.")
    w('  Inácio Martins teve 5 seções, em 4 locais da zona 34, abertas entre 10h02 e 10h59 no 2º turno (no 1º, as mesmas abriram às 8h ou')
    w('  9h25); o comparecimento dessas 5 caiu de 800 para 534. A causa não foi achada na imprensa.')
    w('  Fora do registro, contra o município (as duas seções sem outra no local):')
    for e in V['extremos_municipio_2t']:
        L1_, R1_, L2_, R2_ = e['L1R1L2R2']
        w(f"  {e['k']} ({e['mun']}): Lula {L1_} e Flávio {R1_} no 1º turno, {L2_} e {R2_} no 2º; virada {fz(e['virada_secao'])}, d contra o município")
        w(f"  {fz(e['d_municipio'])}; é a {e['posicao']}ª maior virada entre as {e['secoes_municipio']} seções do município (desvio-padrão {fz(e['dp_virada_municipio'])}).")
        w(f"  No país, entre as {fi(e['secoes_na_faixa'])} seções com {e['faixa_votos']} votos nos finalistas, {fz(100 * e['freq_tao_extremo_na_faixa'], 3)}% têm d contra o")
        w(f"  município tão extremo nessa direção; a chance de pelo menos uma das {e['n_sem_explicacao_com_d_mun']} seções sem explicação chegar a isso é "
          f"{fz(100 * e['prob_alguma_entre_as_sem_explicacao'], 1)}%.")
    w('  Leitura: os dois extremos são raros para o tamanho da seção, um para cada lado, e foram achados depois de olhar (a comparação com')
    w('  o município não é a do registro). As duas são seções isoladas do Pará: Óbidos 22/259 abriu às 10h45 e às 11h nos dois turnos')
    w('  (atraso repetido nos dois turnos; a causa não está nos dados); Jacareacanga 102/54 teve o boletim recebido 5 s antes da emissão marcada,')
    w('  o que exige transmissão feita no próprio local logo depois da emissão (antes da pausa no recebimento, de 17h10 a 19h03). Jacareacanga tem')
    w('  grande parte do território em terra indígena e dispersão de virada acima da do país. O que tiraria a dúvida sobre 102/54: o boletim impresso afixado na seção (ou a')
    w('  foto de fiscal) contra o do TSE, e a assinatura do arquivo do boletim; a seção não está na amostra com assinatura conferida (T18).')
    w('')

    # 7. leituras e desvios
    w('7. Leituras declaradas e desvios')
    w('  - "Qualquer número delas em que a virada de Lula supere a das outras seções do mesmo local": leitura literal seção a seção (uma')
    w('    basta). É o que dá o veredito. A leitura em grupo (média das seções sem explicação) dá INCONCLUSIVO. A leitura seção a seção dispara')
    w(f"    pelo acaso com probabilidade de {fz(100 * V['prob_acaso_alguma_d_ge_3'], 0)}% com {V['n_sem_explicacao_com_d']} seções; o registro não previu isso.")
    w('  - Janela de carga: o calendário não traz data nacional e os sites do TSE e dos TREs bloquearam a leitura direta (HTTP 403); a')
    w('    janela usada é a dos limites da norma (04/09 até o dia da votação), não a de cada UF. Com ela nenhuma carga fica fora. As datas')
    w('    estaduais achadas na imprensa batem com o começo das cargas nos dados (SE 18/09, SP 23/09).')
    w('  - Contingência pelo bweb: o bweb não marca a urna de contingência; usei troca do número da urna entre os turnos ou carga no dia.')
    w('    Uma urna de contingência que entrou no 1º turno e ficou na seção no 2º não muda de número e só é pega se a carga foi no dia.')
    w('  - Explicação por fuso no Brasil: outro deslocamento do país (-2, -1, 0, +1) que deixa A, C e D possíveis ao mesmo tempo. No')
    w('    exterior, o fuso real da cidade (base tz). A leitura estrita (abertura entre 7h e 9h depois do ajuste) é robustez fora do registro;')
    w('    só muda o 1º turno.')
    w('  - "Comparecimento acima de zero": comparecimento de presidente da base por seção.')
    w('  - Seções de junta (29 no 2º turno, 30 no 1º) não têm horário de urna e contam como explicadas por junta.')
    w('  - Não usei outras eleições como régua (pedido do Adendo 18); o 1º turno de 2026 aparece só como comparação dentro da mesma eleição.')
    w('')
    w('8. O que ficou de fora')
    w('  - A causa dos atrasos de abertura: a ata da mesa de cada seção diz o motivo; não é pública nos dados abertos.')
    w('  - O relógio de cada urna contra uma hora de referência: o log da urna não tem hora externa. Na amostra, a seção 16/80 de Afuá')
    w('    (2º turno) gerou o boletim às 17h06min02s no relógio da urna e o TSE o recebeu às 17h05min12s; a seção 16/10 (1º turno) retirou')
    w('    a mídia de resultado às 17h13min58s no relógio da urna e o boletim chegou ao TSE às 17h09min54s: o relógio dessas urnas estava')
    w('    pelo menos 4 minutos adiantado. Os boletins da amostra têm assinatura válida da urna (T18), então não é boletim feito fora dela.')
    w('  - A janela de carga por UF, que depende dos editais dos TREs (não lidos, HTTP 403).')
    w('')
    w('Fontes')
    w('  Res. TSE 23.760/2026 (calendário): https://www.tse.jus.br/legislacao/compilada/res/2026/resolucao-no-23-760-de-2-de-marco-de-2026')
    w('  Res. TSE 23.751/2026 (atos gerais; arts. 87, 99 a 101, 100, 108 e 109, lidos por excertos do buscador): https://www.tse.jus.br/legislacao/compilada/res/2026/resolucao-no-23-751-de-26-de-fevereiro-de-2026')
    w('  Lacração dos sistemas em 04/09/2026: https://www.tse.jus.br/comunicacao/noticias/2026/Setembro/sistemas-das-eleicoes-gerais-de-2026-sao-assinados-digitalmente-e-lacrados-pelo-tse ;')
    w('    https://www12.senado.leg.br/noticias/materias/2026/09/04/tse-conclui-assinatura-e-lacracao-dos-sistemas-das-eleicoes-de-2026')
    w('  Carga do 1º turno: https://www.tre-se.jus.br/comunicacao/noticias/2026/Setembro/justica-eleitoral-inicia-carga-e-lacracao-das-urnas-eletronicas-para-as-eleicoes-2026 ;')
    w('    https://www.tre-sp.jus.br/comunicacao/noticias/2026/Setembro/eleicoes-2026-cerimonia-publica-da-inicio-a-preparacao-de-114-mil-urnas-para-o-1o-turno-em-sao-paulo-1 ;')
    w('    https://www.tre-mt.jus.br/comunicacao/noticias/2026/Setembro/cerimonias-de-carga-e-lacre-marcam-reta-final-de-preparacao-de-urnas-eletronicas')
    w('  Preparação do 2º turno: https://www.tre-pb.jus.br/comunicacao/noticias/2026/Outubro/preparacao-das-urnas-eletronicas-para-o-2deg-turno-acontece-ate-sexta-feira-16 ;')
    w('    https://www.tre-mg.jus.br/comunicacao/noticias/2026/Outubro/urnas-eletronicas-estao-sendo-preparadas-para-o-2o-turno-das-eleicoes-2026 ;')
    w('    https://www.tre-ba.jus.br/comunicacao/noticias/2026/Outubro/eleicoes-2026-tre-ba-inicia-preparacao-das-urnas-para-o-2o-turno-nesta-quarta-feira-14 ;')
    w('    https://www.tre-pr.jus.br/comunicacao/noticias/2026/Outubro/justica-eleitoral-do-parana-inicia-preparacao-das-urnas-eletronicas-para-o-2o-turno-das-eleicoes-2026 ;')
    w('    https://www.opovo.com.br/noticias/politica/eleicoes/2026/10/15/tre-ce-realiza-carga-das-eletronicas-urnas-para-o-2-turno.html ;')
    w('    https://acritica.net/justica/tre-ms-inicia-carga-e-lacracao-de-urnas-para-o-segundo-turno/ ; https://www.dgabc.com.br/Noticia/4352037/urnas-do-2-turno-comecam-a-ser-preparadas-na-quarta-feira')
    w('  Teste de integridade do 2º turno por UF: https://agenciabrasil.ebc.com.br/justica/noticia/2026-10/tribunais-eleitorais-definem-urnas-que-serao-auditadas-no-2o-turno')
    w('  Urnas substituídas no 2º turno: https://bmcnews.com.br/politica/tse-registra-1-516-urnas-substituidas-ate-as-18h-no-segundo-turno/')
    with open(saida_txt, 'w') as f:
        f.write('\n'.join(L) + '\n')


if __name__ == '__main__':
    main()
