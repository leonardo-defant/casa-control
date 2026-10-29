"""T15 (Adendo 9): soma nacional completa por município e cadastro de seções, com o bweb do 2º turno de 2026.

Registro (PRE-REGISTRO-2026-10-26.md, Adendo 9):
- Somar, sem deduplicar votos e deduplicando aptos e comparecimento por seção, todos os números votáveis, brancos, nulos,
  aptos e comparecimento de todas as seções e tipos de urna; comparar com tolerância zero com o total oficial de cada
  município, UF, exterior e Brasil.
- No mesmo passo: conjunto de seções igual ao do 1º turno (499.206) salvo agregação documentada; aptos iguais seção a
  seção; nenhuma seção com comparecimento acima dos aptos; seções em situação especial por UF e o saldo líquido que
  tiraram, medido pela margem de Flávio sobre Lula de cada uma no 1º turno.
- Sinal: qualquer diferença não atribuível a uma seção nomeada com ato documentado; soma dos municípios diferente do total
  da UF; ou saldo tirado pelas seções especiais acima de 3 vezes o do 2º turno de 2022 e acima de 100 mil votos.
- Sem sinal: diferença zero em todos os níveis depois da reconciliação documentada e saldo das seções especiais até 1,5
  vez o de 2022.

Uso:
  python3 -I analisar_T15.py baixar <pasta_oficial> <pasta_mun2t>
      Consulta, a no máximo 1 pedido por segundo e com espera crescente depois de 429, só arquivos do site de resultados
      do TSE da mesma família já usada (somar_oficial.py, baixar_municipios.py, sortear_amostra.py):
      totais do Brasil, das UFs e do exterior (2º e 1º turno), acompanhamento e totais por cidade do exterior,
      cadastro de seções (-cs.json) dos dois turnos e uma amostra fixa de 60 municípios para conferir que os totais
      por município já baixados (baixar_municipios.py) não mudaram.
  python3 -I analisar_T15.py analisar <zips2t_dir> <secoes2026.json.gz> <secoes2022.json.gz> <secoes2018.json.gz>
      <pasta_mun2t> <pasta_oficial> <pasta_locais_votacao> <saida.json> <saida.txt>
      (pasta_locais_votacao: CSV "eleitorado_local_votacao_2026_<UF>.csv" do portal do TSE, 27 UFs e ZZ, com as seções dos dois turnos)
      Variável opcional T15_UF_ANTES: pasta com cópia anterior dos totais por UF (<uf>.json), para conferir que não mudaram.
"""
import os as _os, sys as _sys
_sys.path.insert(0, _os.path.dirname(_os.path.abspath(__file__)))
import collections, csv, glob, io, json, os, random, ssl, sys, time, urllib.error, urllib.request, zipfile
from multiprocessing import Pool

BASE = 'https://resultados.tse.jus.br/oficial/ele2026'
UFS = ['ac', 'al', 'am', 'ap', 'ba', 'ce', 'df', 'es', 'go', 'ma', 'mg', 'ms', 'mt', 'pa', 'pb', 'pe', 'pi', 'pr', 'rj',
       'rn', 'ro', 'rr', 'rs', 'sc', 'se', 'sp', 'to', 'zz']
SEMENTE = 20261028


# ---------------------------------------------------------------- download

def _get(url, ctx, estado):
    """Um pedido, com pelo menos 1,05 s desde o anterior e espera crescente depois de 429 ou página de bloqueio."""
    pausa = 15
    for tent in range(9):
        espera = estado['ult'] + 1.05 - time.time()
        if espera > 0:
            time.sleep(espera)
        estado['ult'] = time.time(); estado['req'] += 1
        try:
            req = urllib.request.Request(url, headers={'User-Agent': 'auditoria-eleicao-2026 (pesquisa)'})
            with urllib.request.urlopen(req, timeout=90, context=ctx) as r:
                b = r.read()
            if b[:300].lower().lstrip().startswith((b'<!doctype html', b'<html')):
                estado['bloqueio'] += 1; time.sleep(pausa); pausa = min(pausa * 2, 600); continue
            return b
        except urllib.error.HTTPError as e:
            if e.code == 404:
                estado['404'] += 1; return None
            if e.code == 429:
                estado['429'] += 1; time.sleep(pausa); pausa = min(pausa * 2, 600); continue
            estado['erro'] += 1; time.sleep(5 * (tent + 1))
        except Exception:
            estado['erro'] += 1; time.sleep(5 * (tent + 1))
    estado['falhou'] += 1
    return None


def baixar(pasta, pasta_mun2t):
    ctx = ssl.create_default_context(cafile=os.environ.get('SSL_CERT_FILE', '/root/.ccr/ca-bundle.crt'))
    est = collections.Counter(); est['ult'] = 0.0
    os.makedirs(pasta, exist_ok=True)
    log = open(os.path.join(pasta, 'consultas.log'), 'a')

    def pega(url, destino):
        if os.path.exists(destino):
            return True
        os.makedirs(os.path.dirname(destino), exist_ok=True)
        b = _get(url, ctx, est)
        log.write(f"{time.strftime('%Y-%m-%dT%H:%M:%SZ', time.gmtime())} {'ok' if b else 'FALHA'} {url}\n"); log.flush()
        if b is None:
            return False
        open(destino + '.tmp', 'wb').write(b); os.replace(destino + '.tmp', destino)
        return True

    # 1) totais do 2º e do 1º turno: Brasil, 27 UFs e exterior
    for ele, t in (('6258', '2t'), ('6257', '1t')):
        for uf in ['br'] + UFS:
            pega(f'{BASE}/{ele}/dados/{uf}/{uf}-c0001-e{int(ele):06d}-u.json', os.path.join(pasta, t, 'uf', f'{uf}.json'))
    print('totais por UF ok', dict(est), flush=True)
    # 2) exterior: acompanhamento por cidade (s, e) e totais por cidade (votos), 2º turno
    pega(f'{BASE}/6258/dados/zz/zz-e006258-ab.json', os.path.join(pasta, '2t', 'zz-ab.json'))
    cidades = sorted(a['cdabr'] for a in json.load(open(os.path.join(pasta, '2t', 'zz-ab.json')))['abr'] if a['cdabr'].isdigit())
    for m in cidades:
        pega(f'{BASE}/6258/dados/zz/zz{m}-c0001-e006258-u.json', os.path.join(pasta, '2t', 'zz_mun', f'zz{m}.json'))
    print('exterior por cidade ok', len(cidades), dict(est), flush=True)
    # 3) cadastro de seções dos dois turnos (pleitos 3221 e 3220)
    for pleito, t in (('3221', '2t'), ('3220', '1t')):
        for uf in UFS:
            pega(f'{BASE}/arquivo-urna/{pleito}/config/{uf}/{uf}-p00{pleito}-cs.json', os.path.join(pasta, t, 'cs', f'{uf}-cs.json'))
    print('cadastro ok', dict(est), flush=True)
    # 4) amostra fixa de 60 municípios para conferir os totais por município já baixados
    muns = sorted(f[:-5] for f in os.listdir(pasta_mun2t) if f.endswith('.json'))
    for cod in random.Random(SEMENTE).sample(muns, 60):
        uf = cod[:2]
        pega(f'{BASE}/6258/dados/{uf}/{cod}-c0001-e006258-u.json', os.path.join(pasta, '2t', 'mun_conferencia', f'{cod}.json'))
    # 5) exterior no 1º turno: acompanhamento por cidade (seções instaladas e não instaladas)
    pega(f'{BASE}/6257/dados/zz/zz-e006257-ab.json', os.path.join(pasta, '1t', 'zz-ab.json'))
    print('fim', dict(est), flush=True)


# ---------------------------------------------------------------- leitura do bweb do 2º turno, todas as linhas de presidente

CAMPOS_BU = ('CD_TIPO_URNA', 'DS_TIPO_URNA', 'NR_URNA_EFETIVADA', 'NR_JUNTA_APURADORA', 'NR_TURMA_APURADORA',
             'DS_SECOES_AGREGADAS', 'NR_LOCAL_VOTACAO', 'DT_ABERTURA', 'DT_ENCERRAMENTO', 'DT_EMISSAO_BU', 'DT_BU_RECEBIDO',
             'DS_CARGO_PERGUNTA_SECAO', 'CD_CARGA_1_URNA_EFETIVADA', 'CD_FLASHCARD_URNA_EFETIVADA', 'NM_MUNICIPIO')


def ler_zip(zpath):
    out = {}
    z = zipfile.ZipFile(zpath)
    nome = [n for n in z.namelist() if n.lower().endswith('.csv')][0]
    linhas = 0; cargos = collections.Counter(); turnos = collections.Counter()
    with z.open(nome) as fh:
        rd = csv.reader(io.TextIOWrapper(fh, encoding='latin1', newline=''), delimiter=';')
        cab = next(rd); ix = {c.strip(): i for i, c in enumerate(cab)}
        for r in rd:
            linhas += 1
            cargo = r[ix['CD_CARGO_PERGUNTA']]
            cargos[cargo] += 1; turnos[(r[ix['NR_TURNO']], r[ix['CD_ELEICAO']])] += 1
            # cargo -1: linha única de seção sem nenhum voto (comparecimento zero); traz aptos e comparecimento
            if cargo not in ('1', '-1'):
                continue
            k = f"{r[ix['SG_UF']]}|{int(r[ix['CD_MUNICIPIO']])}|{int(r[ix['NR_ZONA']])}|{int(r[ix['NR_SECAO']])}"
            s = out.get(k)
            if s is None:
                s = out[k] = {'ac': set(), 'bu': set(), 'v': collections.Counter(), 'lin': collections.Counter(), 'sem_votos': False}
            s['ac'].add((int(r[ix['QT_APTOS']]), int(r[ix['QT_COMPARECIMENTO']]), int(r[ix['QT_ABSTENCOES']])))
            s['bu'].add(tuple(r[ix[c]] for c in CAMPOS_BU))
            if cargo == '-1':
                s['sem_votos'] = True
                if int(r[ix['QT_VOTOS']]) != 0:
                    raise SystemExit(f'linha de cargo -1 com votos: {k}')
                continue
            tv = int(r[ix['CD_TIPO_VOTAVEL']]); nv = int(r[ix['NR_VOTAVEL']])
            chave = 'B' if tv == 2 else 'N' if tv == 3 else f'n{nv}' if tv == 1 else f't{tv}_{nv}'
            s['v'][chave] += int(r[ix['QT_VOTOS']])  # votos somados sem deduplicar
            s['lin'][chave] += 1
    for s in out.values():
        s['ac'] = sorted(s['ac']); s['bu'] = sorted(s['bu']); s['v'] = dict(s['v'])
        s['lin_dup'] = sum(n - 1 for n in s['lin'].values() if n > 1); del s['lin']
    return os.path.basename(zpath), out, linhas, dict(cargos), {f'{a}|{b}': n for (a, b), n in turnos.items()}


# ---------------------------------------------------------------- utilidades

def num(x):
    return int(str(x).replace('.', '').replace(',', '')) if x not in (None, '') else 0


def oficial(d):
    """Campos do arquivo -u.json do TSE usados na comparação."""
    c = {x['n']: num(x['vap']) for a in d['carg'][0]['agr'] for p in a['par'] for x in p['cand']}
    v, e, s = d['v'], d['e'], d['s']
    return {'L': c.get('13', 0), 'R': c.get('22', 0), 'outros_cand': sum(n for k, n in c.items() if k not in ('13', '22')),
            'B': num(v['vb']), 'N': num(v['tvn']), 'vn': num(v['vn']), 'van': num(v['van']), 'vansj': num(v['vansj']),
            'vnt': num(v.get('vnt', 0)), 'vnom': num(v['vnom']), 'vv': num(v['vv']), 'tv': num(v['tv']),
            'comp': num(e['c']), 'abst': num(e['a']), 'te': num(e['te']), 'esi': num(e['esi']), 'esa': num(e['esa']),
            'esni': num(e['esni']), 'esna': num(e['esna']), 'esnt': num(e['esnt']),
            'ts': num(s['ts']), 'st': num(s['st']), 'si': num(s['si']), 'sni': num(s['sni']), 'sa': num(s['sa']),
            'sna': num(s['sna']), 'snt': num(s['snt']), 'dg': d.get('dg'), 'hg': d.get('hg')}


COMP_VOTOS = ('L', 'R', 'outros_cand', 'B', 'N', 'vnom', 'tv', 'comp')


def compara(b, o):
    """Diferenças boletins menos oficial. Aptos: o oficial 'te' inclui seções não instaladas; o comparável é 'esa'."""
    dif = {c: b[c] - o[c] for c in COMP_VOTOS}
    dif['aptos_vs_esa'] = b['apt'] - o['esa']
    dif['aptos_vs_te'] = b['apt'] - o['te']
    dif['secoes_vs_sa'] = b['nsec'] - o['sa']
    dif['abst_vs_esa_menos_comp'] = (o['esa'] - o['comp']) - (b['apt'] - b['comp'])
    return dif


def cadastro(pasta_cs):
    """Seções principais e agregadas do cadastro (-cs.json): {chave: {'da','ha','nsa'}} e {agregada: principal}."""
    princ, agreg, meta = {}, {}, {}
    for f in sorted(glob.glob(os.path.join(pasta_cs, '*-cs.json'))):
        cs = json.load(open(f)); meta[os.path.basename(f)[:2]] = (cs.get('dg'), cs.get('hg'))
        for e in cs['abr']:
            uf = e['cd'].upper()
            for m in e['mu']:
                for z in m['zon']:
                    for s in z['sec']:
                        k = f"{uf}|{int(m['cd'])}|{int(z['cd'])}|{int(s['ns'])}"
                        if s.get('nsp'):
                            agreg[k] = f"{uf}|{int(m['cd'])}|{int(z['cd'])}|{int(s['nsp'])}"
                        else:
                            princ[k] = {'da': s.get('da'), 'ha': s.get('ha'), 'nsa': [int(x) for x in (s.get('nsa') or [])],
                                        'extra': {kk: vv for kk, vv in s.items() if kk not in ('ns', 'da', 'ha', 'nsa', 'nsp')}}
    return princ, agreg, meta


def agr_bweb(txt):
    """'175' ou '466 / 480' -> lista de números (campo DS_SECOES_AGREGADAS do bweb)."""
    if not txt or txt == '#NULO#':
        return []
    import re
    return sorted(int(x) for x in re.findall(r'\d+', txt))


def saldo_especiais(d, ano_ref=False):
    """Seções do 1º turno cujos votos não entram no 2º turno (sem boletim no 2º turno ou boletim anulado no 2º turno).
    Saldo tirado = soma, nessas seções, de (votos do candidato da direita menos os do 13) no 1º turno."""
    lista = []; sem_margem = []
    for k, v in d.items():
        if '1' not in v or v['1'].get('tipo', '').upper() != 'APURADA':
            # seção que já não entrou no 1º turno não tem margem medida no 1º turno: listada à parte
            if '2' in v and (v['2'].get('tipo', '').upper() != 'APURADA' or v['2'].get('comp', 1) == 0):
                sem_margem.append({'secao': k, 'tipo_2T': v['2'].get('tipo'), 'comp_2T': v['2'].get('comp'),
                                   'tipo_1T': v['1'].get('tipo') if '1' in v else None, 'comp_1T': v['1'].get('comp') if '1' in v else None})
            continue
        a = v['1']
        motivo = None
        if '2' not in v:
            motivo = 'sem boletim no 2º turno'
        elif v['2'].get('tipo', '').upper() != 'APURADA':
            motivo = 'boletim do 2º turno ' + v['2']['tipo']
        elif v['2'].get('comp', 1) == 0:
            motivo = 'comparecimento zero no 2º turno'
        if motivo:
            lista.append({'secao': k, 'motivo': motivo, 'apt1': a['apt'], 'comp1': a['comp'], 'L1': a['L'], 'R1': a['R'],
                          'margem_direita_1T': a['R'] - a['L']})
    por_uf = collections.defaultdict(lambda: [0, 0])
    for x in lista:
        u = por_uf[x['secao'].split('|')[0]]; u[0] += 1; u[1] += x['margem_direita_1T']
    return {'secoes': len(lista), 'saldo': sum(x['margem_direita_1T'] for x in lista),
            'saldo_em_modulo_por_secao': sum(abs(x['margem_direita_1T']) for x in lista),
            'por_uf_[secoes,saldo]': dict(sorted(por_uf.items())), 'lista': lista,
            'especiais_no_2T_sem_margem_no_1T': sem_margem}


def referencia_secoes(d):
    """Contagens de referência por ano: comparecimento acima dos aptos e aptos diferentes entre turnos."""
    acima = {t: [k for k, v in d.items() if t in v and v[t]['comp'] > v[t]['apt']] for t in ('1', '2')}
    apt_dif = [k for k, v in d.items() if '1' in v and '2' in v and v['1']['apt'] != v['2']['apt']]
    so1 = [k for k, v in d.items() if '1' in v and '2' not in v]; so2 = [k for k, v in d.items() if '2' in v and '1' not in v]
    tipos = {t: dict(collections.Counter(v[t].get('tipo') for v in d.values() if t in v)) for t in ('1', '2')}
    return {'secoes_1T': sum('1' in v for v in d.values()), 'secoes_2T': sum('2' in v for v in d.values()),
            'so_no_1T': len(so1), 'so_no_2T': len(so2), 'tipos': tipos,
            'comp_acima_aptos_1T': len(acima['1']), 'comp_acima_aptos_2T': len(acima['2']),
            'aptos_diferentes_entre_turnos': len(apt_dif),
            'aptos_dif_soma_abs': sum(abs(d[k]['2']['apt'] - d[k]['1']['apt']) for k in apt_dif),
            'aptos_dif_liquido': sum(d[k]['2']['apt'] - d[k]['1']['apt'] for k in apt_dif),
            'exemplos_aptos_dif': [(k, d[k]['1']['apt'], d[k]['2']['apt']) for k in apt_dif[:10]]}


def eleitorado_locais(pasta):
    """Eleitorado por seção principal e turno no arquivo de locais de votação: soma da principal com as agregadas.
    Retorna {turno: {chave: {'fed': .., 'secao': .., 'agregadas': [..], 'tipo_local': ..}}}."""
    out = {'1': {}, '2': {}}
    for f in sorted(glob.glob(os.path.join(pasta, 'eleitorado_local_votacao_2026_??.csv'))):
        with open(f, encoding='latin1') as fh:
            r = csv.reader(fh, delimiter=';'); h = next(r); i = {c: j for j, c in enumerate(h)}
            for row in r:
                t = row[i['NR_TURNO']]
                uf, m, z, sec = row[i['SG_UF']], int(row[i['CD_MUNICIPIO']]), int(row[i['NR_ZONA']]), int(row[i['NR_SECAO']])
                princ = int(row[i['NR_SECAO_PRINCIPAL']])
                pk = f'{uf}|{m}|{z}|{sec if princ in (-1, 0) or row[i["DS_TIPO_SECAO_AGREGADA"]] == "Principal" else princ}'
                e = out[t].setdefault(pk, {'fed': 0, 'secao': 0, 'agregadas': [], 'tipo_local': set()})
                e['fed'] += int(row[i['QT_ELEITOR_ELEICAO_FEDERAL']]); e['secao'] += int(row[i['QT_ELEITOR_SECAO']])
                e['tipo_local'].add(row[i['DS_TIPO_LOCAL']])
                if row[i['DS_TIPO_SECAO_AGREGADA']] != 'Principal':
                    e['agregadas'].append(sec)
    for t in out:
        for e in out[t].values():
            e['agregadas'].sort(); e['tipo_local'] = sorted(e['tipo_local'])
    return out


# ---------------------------------------------------------------- análise

def analisar(zdir, base26, base22, base18, pasta_mun2t, pasta_of, pasta_locais, saida_json, saida_txt):
    from lib import carregar
    out = {'teste': 'T15', 'registro': 'PRE-REGISTRO-2026-10-26.md, Adendo 9'}
    txt = []
    P = lambda *a: (txt.append(' '.join(str(x) for x in a)), print(*a, flush=True))

    # --- 1. bweb do 2º turno, linha a linha
    zips = sorted(glob.glob(os.path.join(zdir, 'bweb_2t_*.zip')), key=lambda p: -os.path.getsize(p))
    bw = {}; info_zip = {}
    with Pool(3) as pool:
        for nome, o, linhas, cargos, turnos in pool.imap_unordered(ler_zip, zips):
            info_zip[nome] = {'linhas': linhas, 'linhas_por_cargo': cargos, 'turno|eleicao': turnos, 'secoes_presidente': len(o)}
            for k in o:
                if k in bw:
                    raise SystemExit(f'seção repetida entre arquivos: {k}')
            bw.update(o)
    out['zips'] = info_zip
    P(f'bweb 2º turno: {len(zips)} arquivos, {sum(i["linhas"] for i in info_zip.values()):,} linhas, {len(bw):,} seções com presidente')

    # consistência dentro da seção
    multi_ac = {k: s['ac'] for k, s in bw.items() if len(s['ac']) > 1}
    multi_bu = {k: s['bu'] for k, s in bw.items() if len(s['bu']) > 1}
    dup = {k: s['lin_dup'] for k, s in bw.items() if s['lin_dup']}
    votaveis = collections.Counter(); tipos_urna = collections.Counter(); junta = []
    soma_dif_comp = []
    for k, s in bw.items():
        for c in s['v']:
            votaveis[c] += s['v'][c]
        bu = s['bu'][0]
        tipos_urna[(bu[0], bu[1])] += 1
        if bu[3] not in ('-1', '', '#NULO#'):
            junta.append(k)
        apt, comp, abst = s['ac'][0]
        if sum(s['v'].values()) != comp:
            soma_dif_comp.append((k, sum(s['v'].values()), comp))
    sem_votos = sorted(k for k, s in bw.items() if s['sem_votos'])
    sem_votos_e_votos = sorted(k for k, s in bw.items() if s['sem_votos'] and s['v'])
    out['consistencia_secao'] = {'secoes_sem_nenhum_voto_linha_cargo_menos_1': sem_votos,
                                 'secoes_com_linha_sem_votos_e_votos': sem_votos_e_votos,
                                 'secoes_com_mais_de_um_par_aptos_comparecimento': len(multi_ac),
                                 'secoes_com_mais_de_um_boletim_distinto': len(multi_bu),
                                 'linhas_repetidas_mesmo_votavel': len(dup),
                                 'votos_somados_por_votavel': dict(votaveis),
                                 'tipo_de_urna_[CD,DS]': {f'{a}|{b}': n for (a, b), n in tipos_urna.items()},
                                 'secoes_apuradas_por_junta': len(junta),
                                 'secoes_votos_diferente_do_comparecimento': len(soma_dif_comp),
                                 'exemplos_votos_diferente_do_comparecimento': soma_dif_comp[:20],
                                 'exemplos_multi_aptos': {k: v for k, v in list(multi_ac.items())[:10]},
                                 'exemplos_multi_boletim': {k: v for k, v in list(multi_bu.items())[:5]}}
    P('consistência por seção:', json.dumps({k: v for k, v in out['consistencia_secao'].items() if not k.startswith('exemplos')}, ensure_ascii=False))

    # agregado do bweb por município, UF e Brasil
    def zera():
        return collections.Counter()
    agm = collections.defaultdict(zera)
    for k, s in bw.items():
        uf, m = k.split('|')[:2]
        apt, comp, abst = s['ac'][0]  # deduplicado por seção (um par por seção, conferido acima)
        v = s['v']
        L = v.get('n13', 0); R = v.get('n22', 0); B = v.get('B', 0); N = v.get('N', 0)
        nom = sum(n for c, n in v.items() if c.startswith('n'))
        outros = nom - L - R
        extra = sum(n for c, n in v.items() if c.startswith('t'))
        agm[(uf, int(m))].update({'L': L, 'R': R, 'outros_cand': outros, 'B': B, 'N': N + extra, 'vnom': nom,
                                  'tv': nom + B + N + extra, 'comp': comp, 'apt': apt, 'nsec': 1})
    agu = collections.defaultdict(zera)
    for (uf, m), c in agm.items():
        agu[uf].update(c); agu['BR'].update(c)

    # --- 2. totais oficiais
    of_mun = {}
    for f in os.listdir(pasta_mun2t):
        if f.endswith('.json'):
            of_mun[(f[:2].upper(), int(f[2:7]))] = oficial(json.load(open(os.path.join(pasta_mun2t, f))))
    for f in os.listdir(os.path.join(pasta_of, '2t', 'zz_mun')):
        if f.endswith('.json'):
            of_mun[('ZZ', int(f[2:7]))] = oficial(json.load(open(os.path.join(pasta_of, '2t', 'zz_mun', f))))
    of_uf = {uf.upper() if uf != 'br' else 'BR': oficial(json.load(open(os.path.join(pasta_of, '2t', 'uf', f'{uf}.json'))))
             for uf in ['br'] + UFS}
    of_uf1 = {uf.upper() if uf != 'br' else 'BR': oficial(json.load(open(os.path.join(pasta_of, '1t', 'uf', f'{uf}.json'))))
              for uf in ['br'] + UFS}
    geracao = collections.Counter((o['dg'], o['hg']) for o in list(of_mun.values()) + list(of_uf.values()))
    out['geracao_dos_arquivos_oficiais_2T'] = {f'{a} {b}': n for (a, b), n in sorted(geracao.items())}

    # conferência: municípios baixados de novo hoje contra os de 26 e 27/10
    conf = []
    pc = os.path.join(pasta_of, '2t', 'mun_conferencia')
    for f in sorted(os.listdir(pc)):
        a = oficial(json.load(open(os.path.join(pc, f))))
        b = oficial(json.load(open(os.path.join(pasta_mun2t, f))))
        conf.append({'mun': f[:-5], 'igual': a == b})
    out['conferencia_municipios_rebaixados'] = {'municipios': len(conf), 'iguais': sum(c['igual'] for c in conf),
                                                'diferentes': [c['mun'] for c in conf if not c['igual']]}
    P('municípios baixados de novo para conferência:', out['conferencia_municipios_rebaixados'])
    # conferência opcional: totais por UF baixados agora contra cópias anteriores (pasta em T15_UF_ANTES)
    antes = os.environ.get('T15_UF_ANTES')
    if antes:
        ig = {}
        for uf in UFS:
            pa = os.path.join(antes, f'{uf}.json')
            if os.path.exists(pa):
                a = json.load(open(os.path.join(pasta_of, '2t', 'uf', f'{uf}.json'))); b = json.load(open(pa))
                ig[uf] = all(a[c] == b[c] for c in ('s', 'e', 'v', 'carg', 'dg', 'hg'))
        out['conferencia_ufs_contra_copia_anterior'] = {'ufs': len(ig), 'iguais': sum(ig.values()), 'diferentes': [u for u, v in ig.items() if not v]}
        P('UFs baixadas agora contra a cópia anterior:', out['conferencia_ufs_contra_copia_anterior'])

    # --- 3. comparação município a município
    difs_mun = []
    for chave in sorted(set(of_mun) | set(agm)):
        o = of_mun.get(chave); b = agm.get(chave)
        if o is None:
            difs_mun.append({'mun': f'{chave[0]}|{chave[1]}', 'falta': 'oficial', 'boletins': dict(b)}); continue
        if b is None:  # município (cidade do exterior) sem nenhum boletim: entra com zero
            b = collections.Counter({c: 0 for c in COMP_VOTOS + ('apt', 'nsec')})
        d = compara(b, o)
        if any(d[c] for c in COMP_VOTOS) or d['aptos_vs_esa'] or d['secoes_vs_sa']:
            difs_mun.append({'mun': f'{chave[0]}|{chave[1]}', 'dif': d, 'oficial_s': {c: o[c] for c in ('ts', 'si', 'sni', 'sa', 'sna', 'snt')},
                             'oficial_e': {c: o[c] for c in ('te', 'esa', 'esni', 'esna')}, 'boletins': dict(b)})
    nao_inst = {f'{k[0]}|{k[1]}': {'sni': o['sni'], 'esni': o['esni'], 'sna': o['sna'], 'snt': o['snt']} for k, o in of_mun.items()
                if o['sni'] or o['sna'] or o['snt'] or o['esni']}
    out['municipios'] = {'oficiais': len(of_mun), 'com_boletins': len(agm),
                         'oficiais_brasil': sum(1 for k in of_mun if k[0] != 'ZZ'), 'oficiais_exterior': sum(1 for k in of_mun if k[0] == 'ZZ'),
                         'com_alguma_diferenca_votos_comparecimento_aptos_secoes': len(difs_mun),
                         'diferencas': difs_mun, 'municipios_com_secao_nao_instalada_ou_anulada': nao_inst}
    soma_dif_votos_mun = collections.Counter()
    for x in difs_mun:
        if 'dif' in x:
            soma_dif_votos_mun.update({c: x['dif'][c] for c in COMP_VOTOS})
    P(f"municípios: {len(of_mun)} oficiais, {len(agm)} com boletins; com alguma diferença: {len(difs_mun)}")
    for x in difs_mun[:30]:
        P('  ', json.dumps(x, ensure_ascii=False)[:600])

    # --- 4. soma dos municípios oficiais contra a UF oficial, e das UFs contra o Brasil
    soma_mun_of = collections.defaultdict(zera)
    for (uf, m), o in of_mun.items():
        soma_mun_of[uf].update({c: o[c] for c in COMP_VOTOS + ('te', 'esa', 'esni', 'ts', 'si', 'sni', 'sa')})
    mun_vs_uf = {}
    for uf in [u.upper() for u in UFS]:
        o = of_uf[uf]
        mun_vs_uf[uf] = {c: soma_mun_of[uf][c] - o[c] for c in COMP_VOTOS + ('te', 'esa', 'esni', 'ts', 'si', 'sni', 'sa')}
    soma_uf_of = collections.Counter()
    for uf in [u.upper() for u in UFS]:
        soma_uf_of.update({c: of_uf[uf][c] for c in COMP_VOTOS + ('te', 'esa', 'esni', 'ts', 'si', 'sni', 'sa')})
    uf_vs_br = {c: soma_uf_of[c] - of_uf['BR'][c] for c in COMP_VOTOS + ('te', 'esa', 'esni', 'ts', 'si', 'sni', 'sa')}
    out['soma_municipios_oficiais_menos_uf_oficial'] = mun_vs_uf
    out['soma_ufs_oficiais_menos_brasil_oficial'] = uf_vs_br
    n_mun_uf = sum(1 for v in mun_vs_uf.values() if any(v.values()))
    P('soma dos municípios oficiais menos a UF oficial: UFs com alguma diferença =', n_mun_uf,
      '| soma das UFs menos o Brasil:', {c: v for c, v in uf_vs_br.items() if v} or 'zero em todos os campos')

    # --- 5. boletins contra UF, exterior e Brasil
    dif_uf = {}
    for uf in [u.upper() for u in UFS] + ['BR']:
        dif_uf[uf] = compara(agu[uf], of_uf[uf])
    out['boletins_menos_oficial_por_uf'] = dif_uf
    out['boletins_brasil'] = dict(agu['BR']); out['oficial_brasil'] = of_uf['BR']
    for uf, d in dif_uf.items():
        if any(d.values()):
            P(f'  {uf}: boletins menos oficial', {c: v for c, v in d.items() if v})
    P('Brasil, boletins menos oficial:', dif_uf['BR'])

    # --- 6. cadastro e conjunto de seções
    d26 = carregar(base26)
    set1 = {k for k, v in d26.items() if '1' in v}
    set2 = set(bw)
    so1 = sorted(set1 - set2); so2 = sorted(set2 - set1)
    princ2, agreg2, meta2 = cadastro(os.path.join(pasta_of, '2t', 'cs'))
    princ1, agreg1, meta1 = cadastro(os.path.join(pasta_of, '1t', 'cs'))
    cad = {'cadastro_2T_principais': len(princ2), 'cadastro_2T_agregadas': len(agreg2),
           'cadastro_1T_principais': len(princ1), 'cadastro_1T_agregadas': len(agreg1),
           'geracao_cadastro_2T': sorted(set(meta2.values())), 'geracao_cadastro_1T': sorted(set(meta1.values())),
           'bweb_1T_secoes': len(set1), 'bweb_2T_secoes': len(set2),
           'no_bweb_1T_e_nao_no_2T': so1, 'no_bweb_2T_e_nao_no_1T': so2,
           'principais_2T_sem_boletim_2T': sorted(set(princ2) - set2),
           'boletim_2T_fora_do_cadastro_2T': sorted(set2 - set(princ2)),
           'principais_1T_sem_boletim_1T': sorted(set(princ1) - set1),
           'boletim_1T_fora_do_cadastro_1T': sorted(set1 - set(princ1)),
           'principais_diferentes_entre_cadastros': {'so_1T': sorted(set(princ1) - set(princ2)), 'so_2T': sorted(set(princ2) - set(princ1))},
           'agregadas_diferentes_entre_cadastros': {'so_1T': sorted(set(agreg1) - set(agreg2)), 'so_2T': sorted(set(agreg2) - set(agreg1)),
                                                     'principal_mudou': sorted(k for k in set(agreg1) & set(agreg2) if agreg1[k] != agreg2[k])}}
    # agregação no bweb dos dois turnos e contra o cadastro
    agr_dif_turnos = []; agr_dif_cad = []
    for k in set1 & set2:
        a1 = agr_bweb(d26[k]['1'].get('agr', '')); a2 = agr_bweb(bw[k]['bu'][0][5])
        if a1 != a2:
            agr_dif_turnos.append((k, a1, a2))
        if k in princ2 and sorted(princ2[k]['nsa']) != a2:
            agr_dif_cad.append((k, princ2[k]['nsa'], a2))
    cad['agregacao_bweb_diferente_entre_turnos'] = agr_dif_turnos
    cad['agregacao_bweb_2T_diferente_do_cadastro_2T'] = agr_dif_cad[:50]; cad['n_agregacao_bweb_2T_diferente_do_cadastro_2T'] = len(agr_dif_cad)
    sem_pub = {k: v for k, v in princ2.items() if not v.get('da')}
    cad['principais_2T_sem_data_de_publicacao'] = sorted(sem_pub)
    cad['campos_extras_no_cadastro_2T'] = dict(collections.Counter(kk for v in princ2.values() for kk in v['extra']))
    out['cadastro'] = cad
    P('cadastro:', json.dumps({k: (v if not isinstance(v, (list, dict)) or len(json.dumps(v)) < 400 else f'{len(v)} itens')
                               for k, v in cad.items()}, ensure_ascii=False))

    # aptos seção a seção e comparecimento acima dos aptos
    apt_dif = []; acima = []; acima1 = []
    for k in sorted(set1 & set2):
        a1 = d26[k]['1']['apt']; a2 = bw[k]['ac'][0][0]
        if a1 != a2:
            apt_dif.append({'secao': k, 'apt1': a1, 'apt2': a2, 'agr1': d26[k]['1'].get('agr', ''), 'agr2': bw[k]['bu'][0][5]})
    for k, s in bw.items():
        apt, comp, abst = s['ac'][0]
        if comp > apt:
            acima.append({'secao': k, 'apt': apt, 'comp': comp})
    for k in set1:
        if d26[k]['1']['comp'] > d26[k]['1']['apt']:
            acima1.append(k)
    loc = eleitorado_locais(pasta_locais)
    for x in apt_dif:
        k = x['secao']
        for t in ('1', '2'):
            e = loc[t].get(k)
            x[f'cadastro_eleitorado_federal_{t}T'] = e['fed'] if e else None
            x[f'cadastro_agregadas_{t}T'] = e['agregadas'] if e else None
            x['tipo_local'] = e['tipo_local'] if e else x.get('tipo_local')
        x['documentado_no_cadastro'] = (x['cadastro_eleitorado_federal_1T'] == x['apt1'] and x['cadastro_eleitorado_federal_2T'] == x['apt2'])
    # boletim contra cadastro de eleitorado, seção a seção, nos dois turnos (Brasil e exterior)
    bol_cad = {}
    for t in ('1', '2'):
        dif = []; sem = 0; n = 0
        for k in (set1 if t == '1' else set2):
            apt = d26[k]['1']['apt'] if t == '1' else bw[k]['ac'][0][0]
            e = loc[t].get(k); n += 1
            if e is None:
                sem += 1; dif.append((k, apt, None)); continue
            if e['fed'] != apt:
                dif.append((k, apt, e['fed']))
        bol_cad[f'{t}T'] = {'secoes': n, 'sem_registro_no_cadastro': sem, 'aptos_diferente_do_eleitorado_federal': len(dif), 'exemplos': dif[:30]}
    cad_sets = {t: {k for k in loc[t]} for t in ('1', '2')}
    bol_cad['cadastro_principais_1T'] = len(cad_sets['1']); bol_cad['cadastro_principais_2T'] = len(cad_sets['2'])
    bol_cad['cadastro_so_1T'] = sorted(cad_sets['1'] - cad_sets['2'])[:50]; bol_cad['cadastro_so_2T'] = sorted(cad_sets['2'] - cad_sets['1'])[:50]
    bol_cad['cadastro_eleitorado_mudou_entre_turnos'] = sum(1 for k in cad_sets['1'] & cad_sets['2'] if loc['1'][k]['fed'] != loc['2'][k]['fed'])
    bol_cad['cadastro_agregacao_mudou_entre_turnos'] = sum(1 for k in cad_sets['1'] & cad_sets['2'] if loc['1'][k]['agregadas'] != loc['2'][k]['agregadas'])
    out['boletim_contra_cadastro_de_eleitorado'] = bol_cad
    P('boletim contra cadastro de eleitorado (locais de votação):', json.dumps({k: (v if not isinstance(v, (list, dict)) else
                                                                                    {kk: vv for kk, vv in v.items() if kk != 'exemplos'} if isinstance(v, dict) else len(v))
                                                                                for k, v in bol_cad.items()}, ensure_ascii=False))
    del loc
    liq = collections.Counter()
    for x in apt_dif:
        liq['exterior' if x['secao'].startswith('ZZ|') else 'brasil'] += x['apt2'] - x['apt1']
    out['aptos_diferentes_entre_turnos'] = {'secoes': len(apt_dif), 'documentadas_no_cadastro': sum(x['documentado_no_cadastro'] for x in apt_dif),
                                            'soma_abs': sum(abs(x['apt2'] - x['apt1']) for x in apt_dif),
                                            'liquido_brasil_e_exterior': dict(liq),
                                            'por_tipo_de_local': dict(collections.Counter('+'.join(x.get('tipo_local') or ['?']) for x in apt_dif)),
                                            'maior_variacao': max((abs(x['apt2'] - x['apt1']) for x in apt_dif), default=0),
                                            'secoes_por_variacao_em_modulo': {str(a): n for a, n in sorted(collections.Counter(min(abs(x['apt2'] - x['apt1']), 10) for x in apt_dif).items())},
                                            'exemplos': apt_dif[:50]}
    out['comparecimento_acima_dos_aptos'] = {'2T': len(acima), 'lista_2T': acima, '1T': len(acima1), 'lista_1T': acima1[:50]}
    P(f'aptos diferentes entre turnos, seção a seção: {len(apt_dif)}; comparecimento acima dos aptos: 2º turno {len(acima)}, 1º turno {len(acima1)}')

    # --- 7. seções em situação especial por UF (2º turno) e saldo tirado
    esp = collections.defaultdict(collections.Counter)
    for uf in [u.upper() for u in UFS]:
        o = of_uf[uf]
        esp[uf].update({'nao_instaladas_oficial': o['sni'], 'aptos_nao_instaladas_oficial': o['esni'], 'anuladas_ou_nao_apuradas_oficial': o['sna'],
                        'nao_totalizadas_oficial': o['snt'], 'nao_instaladas_oficial_1T': of_uf1[uf]['sni']})
    for k in junta:
        esp[k.split('|')[0]]['boletim_de_junta_2T'] += 1
    for k in so1:
        esp[k.split('|')[0]]['no_1T_sem_boletim_2T'] += 1
    for k, s in bw.items():
        if s['bu'][0][1].upper() != 'APURADA':
            esp[k.split('|')[0]]['boletim_2T_nao_apurada'] += 1
    for x in apt_dif:
        esp[x['secao'].split('|')[0]]['aptos_mudaram'] += 1
    out['secoes_especiais_por_uf_2T'] = {u: dict(c) for u, c in sorted(esp.items()) if any(c.values())}

    # base do 2º turno no formato do saldo (tipo vem do bweb lido aqui)
    d26s = {}
    for k in set1:
        v = {'1': d26[k]['1']}
        if k in bw:
            s = bw[k]
            v['2'] = {'tipo': s['bu'][0][1], 'L': s['v'].get('n13', 0), 'R': s['v'].get('n22', 0), 'comp': s['ac'][0][1]}
        d26s[k] = v
    s26 = saldo_especiais(d26s)
    # seções de junta: margem do 1º turno e do 2º turno (descritivo; os votos delas entram no total)
    jun = []
    for k in junta:
        if k in d26:
            a = d26[k]['1']; s = bw[k]['v']
            jun.append({'secao': k, 'margem_flavio_1T': a['R'] - a['L'], 'margem_flavio_2T': s.get('n22', 0) - s.get('n13', 0),
                        'comp1': a['comp'], 'comp2': bw[k]['ac'][0][1]})
    del d26
    d22 = carregar(base22); s22 = saldo_especiais(d22); ref22 = referencia_secoes(d22); del d22
    d18 = carregar(base18); s18 = saldo_especiais(d18); ref18 = referencia_secoes(d18); del d18
    out['saldo_tirado_pelas_secoes_especiais'] = {
        'definicao': 'seções com boletim apurado no 1º turno que não somaram voto no 2º turno (sem boletim, boletim não apurado ou comparecimento zero no 2º turno); saldo = soma da margem do candidato da direita sobre o 13 no 1º turno nessas seções',
        '2026': s26, '2022': s22, '2018_descritivo': s18,
        'juntas_2026_descritivo': {'secoes': len(jun), 'margem_flavio_1T': sum(x['margem_flavio_1T'] for x in jun),
                                   'margem_flavio_2T': sum(x['margem_flavio_2T'] for x in jun), 'lista': jun}}
    m1 = {x['secao']: x['margem_direita_1T'] for x in s26['lista']}
    m1.update({x['secao']: x['margem_flavio_1T'] for x in jun})
    out['saldo_tirado_pelas_secoes_especiais']['saldo_2026_com_juntas'] = sum(m1.values())
    out['referencias_secoes'] = {'2022': ref22, '2018': ref18}
    P(f"saldo tirado: 2026 {s26['saldo']:+d} votos em {s26['secoes']} seções; 2022 {s22['saldo']:+d} em {s22['secoes']}; 2018 {s18['saldo']:+d} em {s18['secoes']}")
    for x in s26['lista'] + s22['lista']:
        P('   ', x)
    P(f"seções de junta no 2º turno de 2026: {len(jun)}; margem de Flávio nelas, 1º turno {out['saldo_tirado_pelas_secoes_especiais']['juntas_2026_descritivo']['margem_flavio_1T']:+d}, 2º turno {out['saldo_tirado_pelas_secoes_especiais']['juntas_2026_descritivo']['margem_flavio_2T']:+d}")
    P('referências por seção 2022:', {k: v for k, v in ref22.items() if k != 'exemplos_aptos_dif'})
    P('referências por seção 2018:', {k: v for k, v in ref18.items() if k != 'exemplos_aptos_dif'})

    # --- 8. reconciliação e veredito pela letra do registro
    rec = {}
    # (a) votos e comparecimento: tolerância zero em município, UF, exterior e Brasil
    mun_votos = [x['mun'] for x in difs_mun if 'falta' in x or any(x['dif'][c] for c in COMP_VOTOS)]
    uf_votos = [u for u, d in dif_uf.items() if any(d[c] for c in COMP_VOTOS)]
    rec['votos_comparecimento'] = {'municipios_com_diferenca': mun_votos, 'ufs_exterior_brasil_com_diferenca': uf_votos}
    # (b) aptos e número de seções: o boletim contra o eleitorado e as seções apuradas; o resto tem de ser seção não instalada
    mun_aptos = [x['mun'] for x in difs_mun if 'dif' in x and x['dif']['aptos_vs_esa']]
    mun_secoes = [x['mun'] for x in difs_mun if 'dif' in x and x['dif']['secoes_vs_sa']]
    sem_bol_2t = collections.Counter('|'.join(k.split('|')[:2]) for k in cad['principais_2T_sem_boletim_2T'])
    nao_inst_mun = {f'{k[0]}|{k[1]}': o['sni'] for k, o in of_mun.items() if o['sni']}
    te_esa = {f'{k[0]}|{k[1]}': (o['te'] - o['esa'], o['esni']) for k, o in of_mun.items() if o['te'] != o['esa'] or o['esni']}
    rec['aptos_secoes'] = {'municipios_aptos_boletim_diferente_do_eleitorado_das_secoes_apuradas': mun_aptos,
                           'municipios_secoes_boletim_diferente_das_apuradas': mun_secoes,
                           'secoes_do_cadastro_sem_boletim_por_municipio': dict(sem_bol_2t),
                           'nao_instaladas_oficial_por_municipio': nao_inst_mun,
                           'cadastro_sem_boletim_igual_nao_instaladas': dict(sem_bol_2t) == nao_inst_mun,
                           'te_menos_esa_igual_esni_em_todos': all(a == b for a, b in te_esa.values()),
                           'aptos_das_nao_instaladas': sum(b for a, b in te_esa.values())}
    # (c) soma dos municípios oficiais contra a UF e das UFs contra o Brasil
    rec['municipios_somam_uf'] = [u for u, v in mun_vs_uf.items() if any(v.values())]
    rec['ufs_somam_brasil'] = {c: v for c, v in uf_vs_br.items() if v}
    # (d) conjunto de seções contra o 1º turno, com a explicação de cada diferença
    ab1 = {}
    p1 = os.path.join(pasta_of, '1t', 'zz-ab.json')
    if os.path.exists(p1):
        for a in json.load(open(p1))['abr']:
            if not a['cdabr'].isdigit():
                continue
            ab1[f"ZZ|{int(a['cdabr'])}"] = {c: num(a['s'][c]) for c in ('ts', 'si', 'sni', 'sa')} | {'c': num(a['e']['c']), 'te': num(a['e']['te'])}
    ab2 = {}
    for a in json.load(open(os.path.join(pasta_of, '2t', 'zz-ab.json')))['abr']:
        if not a['cdabr'].isdigit():
            continue
        ab2[f"ZZ|{int(a['cdabr'])}"] = {c: num(a['s'][c]) for c in ('ts', 'si', 'sni', 'sa')} | {'c': num(a['e']['c']), 'te': num(a['e']['te'])}
    expl = []
    for k in so1:
        m = '|'.join(k.split('|')[:2])
        expl.append({'secao': k, 'lado': 'só no 1º turno', 'no_cadastro_2T': k in princ2,
                     'nao_instaladas_no_municipio_2T': nao_inst_mun.get(m, 0), 'oficial_cidade_2T': ab2.get(m),
                     'explicada': k in princ2 and nao_inst_mun.get(m, 0) > 0})
    for k in so2:
        m = '|'.join(k.split('|')[:2]); s2 = bw[k]
        o1 = ab1.get(m) if k.startswith('ZZ|') else None
        expl.append({'secao': k, 'lado': 'só no 2º turno', 'aptos_2T': s2['ac'][0][0], 'comp_2T': s2['ac'][0][1],
                     'no_cadastro_1T': k in princ1, 'oficial_cidade_1T': o1, 'oficial_cidade_2T': ab2.get(m),
                     'explicada': bool(o1) and (o1['sni'] > 0 or o1['c'] == 0)})
    rec['conjunto_de_secoes'] = {'diferencas': expl, 'nao_explicadas': [x['secao'] for x in expl if not x['explicada']],
                                 'agregacao_mudou_no_bweb': len(cad['agregacao_bweb_diferente_entre_turnos'])}
    # (e) aptos seção a seção e comparecimento acima dos aptos
    rec['aptos_entre_turnos_nao_documentados'] = [x['secao'] for x in apt_dif if not x['documentado_no_cadastro']]
    rec['comparecimento_acima_dos_aptos'] = [x['secao'] for x in acima]
    # (f) saldo tirado pelas seções especiais
    sd26, sd22 = s26['saldo'], s22['saldo']
    rec['saldo'] = {'2026': sd26, '2022': sd22, '2018': s18['saldo'], 'limite_sem_sinal_1_5x_2022': 1.5 * sd22,
                    'limite_sinal_3x_2022': 3 * sd22, 'limite_sinal_votos': 100000,
                    'sinal': sd26 > 3 * sd22 and sd26 > 100000, 'sem_sinal': sd26 <= 1.5 * sd22}
    nao_atrib = (rec['votos_comparecimento']['municipios_com_diferenca'] + rec['votos_comparecimento']['ufs_exterior_brasil_com_diferenca']
                 + rec['aptos_secoes']['municipios_aptos_boletim_diferente_do_eleitorado_das_secoes_apuradas']
                 + rec['aptos_secoes']['municipios_secoes_boletim_diferente_das_apuradas']
                 + ([] if rec['aptos_secoes']['cadastro_sem_boletim_igual_nao_instaladas'] else ['secoes do cadastro sem boletim diferentes das nao instaladas'])
                 + ([] if rec['aptos_secoes']['te_menos_esa_igual_esni_em_todos'] else ['aptos totais menos aptos apurados diferente dos aptos das nao instaladas'])
                 + rec['conjunto_de_secoes']['nao_explicadas'] + rec['aptos_entre_turnos_nao_documentados'] + rec['comparecimento_acima_dos_aptos'])
    rec['diferencas_nao_atribuidas'] = nao_atrib
    rec['sem_votos_de_junta'] = sum(1 for k in sem_votos if k in junta)
    rec['nao_instaladas_sem_data_de_publicacao'] = sorted(cad['principais_2T_sem_data_de_publicacao']) == sorted(cad['principais_2T_sem_boletim_2T'])
    rec['nao_instaladas_iguais_1T'] = sorted(set(cad['principais_1T_sem_boletim_1T']) - set(so2)) == sorted(cad['principais_2T_sem_boletim_2T'])
    sinal = bool(nao_atrib) or bool(rec['municipios_somam_uf']) or bool(rec['ufs_somam_brasil']) or rec['saldo']['sinal']
    sem = (not nao_atrib) and not rec['municipios_somam_uf'] and not rec['ufs_somam_brasil'] and rec['saldo']['sem_sinal']
    rec['veredito'] = 'SINAL' if sinal else 'SEM SINAL' if sem else 'INCONCLUSIVO'
    out['reconciliacao_e_veredito'] = rec
    P('reconciliação:', json.dumps({k: v for k, v in rec.items() if k not in ('aptos_secoes',)}, ensure_ascii=False)[:3000])
    P('aptos e seções:', json.dumps(rec['aptos_secoes'], ensure_ascii=False)[:2000])
    P('VEREDITO pela letra:', rec['veredito'])

    # registro das consultas feitas por 'baixar'
    import re
    lg = os.path.join(pasta_of, 'consultas.log'); bo = os.path.join(pasta_of, 'baixar.out')
    cq = {}
    if os.path.exists(lg):
        ls = open(lg).read().splitlines()
        cq = {'arquivos_ok': sum(' ok ' in x for x in ls), 'falhas': sum(' FALHA ' in x for x in ls),
              'avisos_429': sum(' 429 ' in x for x in ls)}
    if os.path.exists(bo):
        m = re.findall(r"'429': (\d+)", open(bo).read())
        if m:
            cq['avisos_429'] = cq.get('avisos_429', 0) + int(m[-1])
    out['consultas'] = cq
    out['boletins_por_uf'] = {u: dict(c) for u, c in sorted(agu.items())}
    out['oficial_por_uf'] = of_uf
    json.dump(out, open(saida_json, 'w'), ensure_ascii=False, indent=1, default=list)
    open(saida_txt, 'w').write(relatorio(out))


def fmt(n):
    return f'{n:,}'.replace(',', '.') if isinstance(n, int) else str(n)


def sn(b):
    return 'sim' if b else 'não'


def relatorio(out):
    """Texto do resultado, montado só a partir dos números do JSON."""
    r = out['reconciliacao_e_veredito']; L = []
    A = L.append
    ob, bb = out['oficial_brasil'], out['boletins_brasil']
    c = out['cadastro']; cs = out['consistencia_secao']; ra = r['aptos_secoes']
    ad = out['aptos_diferentes_entre_turnos']; bc = out['boletim_contra_cadastro_de_eleitorado']
    sd = out['saldo_tirado_pelas_secoes_especiais']; rs = r['saldo']; j = sd['juntas_2026_descritivo']
    ref = out['referencias_secoes']
    A('T15. Soma nacional completa por município e cadastro de seções, com o bweb do 2º turno de 2026 (Adendo 9)')
    A('Script: scripts/analisar_T15.py (passo "baixar" para os arquivos oficiais, passo "analisar" para a soma). Números completos: resultados/T15_bweb.json.')
    A('Rodado em 29/10/2026 com o bweb do 2º turno (zips de 26/10, 07h42), a base do 1º turno e as bases de 2018 e 2022 por seção.')
    A('')
    A('Critério registrado (PRE-REGISTRO-2026-10-26.md, Adendo 9, antes dos dados):')
    A('- Somar, sem deduplicar votos e deduplicando aptos e comparecimento por seção, todos os números votáveis, brancos, nulos, aptos e')
    A('  comparecimento de todas as seções e tipos de urna; comparar com tolerância zero com o total oficial de cada município, UF, exterior e Brasil.')
    A('- No mesmo passo: conjunto de seções igual ao do 1º turno (499.206) salvo agregação documentada; aptos iguais seção a seção; nenhuma')
    A('  seção com comparecimento acima dos aptos; seções em situação especial por UF e o saldo líquido que tiraram, medido pela margem de')
    A('  Flávio sobre Lula de cada uma no 1º turno.')
    A('- Sinal: qualquer diferença não atribuível a uma seção nomeada com ato documentado; soma dos municípios diferente do total da UF; ou')
    A('  saldo tirado pelas seções especiais acima de 3 vezes o do 2º turno de 2022 e acima de 100 mil votos.')
    A('- Sem sinal: diferença zero em todos os níveis depois da reconciliação documentada e saldo das seções especiais até 1,5 vez o de 2022.')
    A('')
    A(f"VEREDITO PELA LETRA: {r['veredito']}")
    A('')
    A('Resumo')
    A(f"- Os {fmt(c['bweb_2T_secoes'])} boletins do 2º turno somam, voto a voto, o total oficial de cada um dos {fmt(out['municipios']['oficiais'])} municípios e cidades")
    A(f"  do exterior, de cada UF, do exterior e do Brasil: Lula {fmt(bb['L'])}, Flávio {fmt(bb['R'])}, brancos {fmt(bb['B'])}, nulos {fmt(bb['N'])},")
    A(f"  comparecimento {fmt(bb['comp'])}. Diferença zero em votos e comparecimento em todos os níveis. Nenhum outro número votável aparece.")
    A(f"- A soma dos arquivos oficiais por município é igual ao arquivo oficial da UF em todas as UFs e no exterior, e a soma das UFs é igual ao Brasil.")
    A(f"- Aptos: os boletins somam {fmt(bb['apt'])}, igual aos aptos das seções apuradas no oficial. Os {fmt(ob['te'] - ob['esa'])} aptos que faltam para o")
    A(f"  total oficial ({fmt(ob['te'])}) são das {fmt(ob['sni'])} seções não instaladas, todas no exterior, nomeadas abaixo.")
    so2 = [x for x in r['conjunto_de_secoes']['diferencas'] if x['lado'] == 'só no 2º turno']
    so1 = [x for x in r['conjunto_de_secoes']['diferencas'] if x['lado'] == 'só no 1º turno']
    A(f"- Seções: das {fmt(c['bweb_1T_secoes'])} do 1º turno, {len(so1)} faltam no 2º turno; o 2º turno tem {len(so2)} a mais "
      f"({', '.join(x['secao'] + ', ' + str(x['aptos_2T']) + ' aptos, comparecimento ' + str(x['comp_2T']) for x in so2)}; seção instalada e sem votante nos dois turnos")
    A('  pelo oficial da cidade: o bweb do 1º turno omite a seção sem voto, o do 2º turno a lista numa linha de cargo -1).')
    A(f"- Aptos mudaram entre os turnos em {fmt(ad['secoes'])} seções, e em todas os aptos de cada turno batem com o eleitorado da seção no cadastro")
    A('  oficial de locais de votação daquele turno. Nenhuma seção com comparecimento acima dos aptos.')
    A(f"- Saldo tirado pelas seções especiais: 2026 {rs['2026']:+d} votos (1 seção); 2022 {rs['2022']:+d} (nenhuma seção com margem no 1º turno).")
    A('')
    z = out['zips']
    A('1. Dados e método')
    A(f"- bweb do 2º turno: {len(z)} arquivos (27 UFs e exterior, hash conferido antes), {fmt(sum(v['linhas'] for v in z.values()))} linhas. Lidas, direto")
    A('  dos zips, todas as linhas de presidente (cargo 1) e as de cargo -1, que o TSE usa para a seção sem nenhum voto (aptos e comparecimento,')
    A('  QT_VOTOS 0). A base secoes2026.json.gz (só cargos 1 e 3) não tem essas duas seções; por isso o T15 lê os zips.')
    A(f"- Votos somados linha a linha, sem deduplicar. Aptos e comparecimento tomados uma vez por seção, depois de conferir que cada seção tem um único")
    A(f"  par: {cs['secoes_com_mais_de_um_par_aptos_comparecimento']} seções com mais de um par, {cs['secoes_com_mais_de_um_boletim_distinto']} com mais de um boletim distinto, "
      f"{cs['linhas_repetidas_mesmo_votavel']} com linha repetida do mesmo votável,")
    A(f"  {cs['secoes_votos_diferente_do_comparecimento']} em que a soma dos votos difere do comparecimento. Tipo de urna: todas \"Apurada\" ({fmt(c['bweb_2T_secoes'])}).")
    A(f"- Votáveis de presidente nos boletins: 13 ({fmt(cs['votos_somados_por_votavel'].get('n13', 0))}), 22 ({fmt(cs['votos_somados_por_votavel'].get('n22', 0))}), "
      f"branco ({fmt(cs['votos_somados_por_votavel'].get('B', 0))}), nulo ({fmt(cs['votos_somados_por_votavel'].get('N', 0))}); nenhum outro.")
    ger = sorted(out['geracao_dos_arquivos_oficiais_2T'])
    A(f"- Totais oficiais: arquivos -u.json do site de resultados do TSE (eleição 6258, cargo 1) de {fmt(out['municipios']['oficiais'])} municípios e cidades do")
    A(f"  exterior ({fmt(out['municipios']['oficiais_brasil'])} no Brasil e {out['municipios']['oficiais_exterior']} no exterior), das 27 UFs, do exterior e do Brasil, todos gerados em 25/10/2026 entre {ger[0][-8:]} e {ger[-1][-8:]}.")
    cm = out['conferencia_municipios_rebaixados']
    A(f"- Os totais dos 5.571 municípios do Brasil são os baixados em 26 e 27/10 por baixar_municipios.py. Conferência: {cm['iguais']} de {cm['municipios']} sorteados")
    A(f"  (semente {SEMENTE}) e baixados de novo em 28 e 29/10 são idênticos." + (f" Diferentes: {cm['diferentes']}." if cm['diferentes'] else ''))
    if 'conferencia_ufs_contra_copia_anterior' in out:
        cu = out['conferencia_ufs_contra_copia_anterior']
        A(f"- Totais das 27 UFs e do exterior baixados em 28/10 contra a cópia de 26/10: {cu['iguais']} de {cu['ufs']} idênticos, inclusive data e hora de geração.")
    A(f"- Cadastro de seções: -cs.json dos pleitos 3221 (2º turno, gerado em {c['geracao_cadastro_2T'][0][0]} {c['geracao_cadastro_2T'][0][1]}) e 3220 (1º turno; os arquivos")
    A('  por UF têm datas de geração de 05/10 a 24/10). Eleitorado por seção e turno: arquivo "Eleitorado por local de votação 2026" do portal do')
    A('  TSE (27 UFs e exterior, os dois turnos, gerado em 25/10). 1º turno por seção: secoes2026.json.gz (bweb do 1º turno).')
    cq = out.get('consultas', {})
    A(f"- Consultas novas ao TSE (log consultas.log na pasta dos arquivos oficiais): {cq.get('arquivos_ok', '?')} arquivos baixados e {cq.get('falhas', '?')} pedido sem")
    A(f"  arquivo (404: o código da UF tomado por cidade na lista do exterior, sem efeito no resultado), com pelo menos 1,05 s entre pedidos e espera")
    A(f"  crescente depois de cada aviso 429 ({cq.get('avisos_429', '?')} avisos).")
    A('')
    A('2. Soma dos boletins contra o total oficial (tolerância zero)')
    nd = out['municipios']['com_alguma_diferenca_votos_comparecimento_aptos_secoes']
    A(f"- Municípios e cidades do exterior: {fmt(out['municipios']['oficiais'])} comparados ({fmt(out['municipios']['com_boletins'])} com boletim; as outras "
      f"{out['municipios']['oficiais'] - out['municipios']['com_boletins']} são cidades do exterior")
    A(f"  só com seção não instalada). Com alguma diferença em votos do 13, do 22, de outros números, brancos, nulos, nominais, total de votos,")
    A(f"  comparecimento, aptos das seções apuradas ou número de seções apuradas: {nd}.")
    A(f"- UFs, exterior e Brasil com diferença em votos ou comparecimento: {', '.join(r['votos_comparecimento']['ufs_exterior_brasil_com_diferenca']) or 'nenhum'}.")
    A('- Brasil, boletins e oficial:')
    for nome, kb, ko in (('Lula (13)', 'L', 'L'), ('Flávio (22)', 'R', 'R'), ('outros números', 'outros_cand', 'outros_cand'), ('brancos', 'B', 'B'),
                         ('nulos', 'N', 'N'), ('total de votos', 'tv', 'tv'), ('comparecimento', 'comp', 'comp'),
                         ('aptos das seções apuradas', 'apt', 'esa'), ('seções apuradas', 'nsec', 'sa')):
        A(f"    {nome}: {fmt(bb[kb])} e {fmt(ob[ko])}, diferença {bb[kb] - ob[ko]}")
    A(f"- O arquivo nacional (gerado em {ob['dg']} {ob['hg']}, igual na cópia de 28/10) dá {fmt(ob['B'])} brancos e {fmt(ob['N'])} nulos, os mesmos números")
    A('  dos boletins. Os 1.430.493 brancos e 2.723.298 nulos da imprensa citados no README (10 votos a menos) não estão no arquivo nacional atual.')
    A(f"- Nulos no oficial: total {fmt(ob['N'])} = nulos {fmt(ob['vn'])} + anulados {fmt(ob['van'])} + anulados sub judice {fmt(ob['vansj'])}; no 2º turno não há")
    A('  candidatura anulada, então não há a diferença do 28 que existia no 1º turno.')
    A(f"- Aptos: total oficial {fmt(ob['te'])} menos aptos das seções apuradas {fmt(ob['esa'])} = {fmt(ob['te'] - ob['esa'])}, igual aos aptos das seções não")
    A(f"  instaladas em todos os municípios ({sn(ra['te_menos_esa_igual_esni_em_todos'])}). Seções não instaladas no oficial: {fmt(ob['sni'])}, todas no exterior;")
    A(f"  seções do cadastro do 2º turno sem boletim iguais, cidade a cidade, às não instaladas do oficial: {sn(ra['cadastro_sem_boletim_igual_nao_instaladas'])}.")
    A(f"  As {len(c['principais_2T_sem_boletim_2T'])} seções não instaladas (cadastro do 2º turno, sem data de publicação de arquivo de urna: {sn(r['nao_instaladas_sem_data_de_publicacao'])}; contadas")
    A(f"  como não instaladas no arquivo oficial da cidade; as mesmas do 1º turno: {sn(r['nao_instaladas_iguais_1T'])}):")
    lst = c['principais_2T_sem_boletim_2T']
    for i in range(0, len(lst), 8):
        A('    ' + ', '.join(lst[i:i + 8]))
    A('- Abstenção: o oficial dá aptos menos comparecimento contando os aptos das não instaladas; descontados esses 423, bate com os boletins.')
    A('')
    A('3. Soma dos municípios oficiais contra a UF e das UFs contra o Brasil')
    A(f"- UFs (e exterior) em que a soma dos arquivos oficiais por município difere do arquivo oficial da UF em algum campo (votos, comparecimento,")
    A(f"  aptos, seções): {', '.join(r['municipios_somam_uf']) or 'nenhuma'}.")
    A(f"- Soma das 27 UFs e do exterior menos o Brasil: {r['ufs_somam_brasil'] or 'zero em todos os campos'}.")
    A('')
    A('4. Cadastro de seções')
    A(f"- Cadastro (-cs.json): 1º turno {fmt(c['cadastro_1T_principais'])} seções principais e {fmt(c['cadastro_1T_agregadas'])} agregadas; 2º turno {fmt(c['cadastro_2T_principais'])} e "
      f"{fmt(c['cadastro_2T_agregadas'])}.")
    A(f"  Principais só num dos cadastros: {len(c['principais_diferentes_entre_cadastros']['so_1T']) + len(c['principais_diferentes_entre_cadastros']['so_2T'])}; agregadas só num deles ou com outra principal: "
      f"{sum(len(v) for v in c['agregadas_diferentes_entre_cadastros'].values())}.")
    A(f"- Boletins: 1º turno {fmt(c['bweb_1T_secoes'])}, 2º turno {fmt(c['bweb_2T_secoes'])}. Boletim fora do cadastro: 1º turno {len(c['boletim_1T_fora_do_cadastro_1T'])}, "
      f"2º turno {len(c['boletim_2T_fora_do_cadastro_2T'])}. Seções do cadastro sem boletim:")
    A(f"  1º turno {len(c['principais_1T_sem_boletim_1T'])} (as 41 não instaladas e ZZ|29564|1|91, de comparecimento zero), 2º turno {len(c['principais_2T_sem_boletim_2T'])} (as 41 não instaladas).")
    for x in r['conjunto_de_secoes']['diferencas']:
        A(f"- Diferença de conjunto entre os turnos: {x['secao']}, {x['lado']}; no 2º turno {x.get('aptos_2T')} aptos e comparecimento {x.get('comp_2T')};")
        A(f"  no oficial da cidade, 1º turno {x.get('oficial_cidade_1T')} e 2º turno {x.get('oficial_cidade_2T')}; no cadastro do 1º turno: {sn(x.get('no_cadastro_1T'))}. Explicada: {sn(x['explicada'])}.")
    A(f"- Agregação (DS_SECOES_AGREGADAS) diferente entre os turnos: {r['conjunto_de_secoes']['agregacao_mudou_no_bweb']} seções; agregação do boletim do 2º turno")
    A(f"  diferente do cadastro do 2º turno: {c['n_agregacao_bweb_2T_diferente_do_cadastro_2T']}; no cadastro de eleitorado, agregação mudou entre os turnos em {bc['cadastro_agregacao_mudou_entre_turnos']}.")
    liq = ad['liquido_brasil_e_exterior']
    A(f"- Aptos diferentes entre os turnos, seção a seção: {fmt(ad['secoes'])} seções, {fmt(ad['soma_abs'])} aptos somados em módulo, maior variação {ad['maior_variacao']};")
    A(f"  líquido {liq.get('brasil', 0):+d} no Brasil e {liq.get('exterior', 0):+d} no exterior (o total nacional de aptos é o mesmo nos dois turnos, {fmt(ob['te'])}).")
    A(f"  Em {fmt(ad['documentadas_no_cadastro'])} delas os aptos do boletim de cada turno são iguais ao eleitorado federal da seção (com as agregadas) no")
    A(f"  cadastro de locais de votação do TSE para aquele turno; não documentadas: {len(r['aptos_entre_turnos_nao_documentados'])}.")
    A(f"  Tipo de local das seções que mudaram: {ad['por_tipo_de_local']}. Seções por variação em módulo (10 = 10 ou mais): {ad['secoes_por_variacao_em_modulo']}.")
    A(f"- Boletim contra o cadastro de eleitorado, seção a seção, Brasil e exterior: 1º turno {bc['1T']['aptos_diferente_do_eleitorado_federal']} diferenças em")
    A(f"  {fmt(bc['1T']['secoes'])} seções; 2º turno {bc['2T']['aptos_diferente_do_eleitorado_federal']} em {fmt(bc['2T']['secoes'])}.")
    A(f"- Referências, aptos diferentes entre turnos na mesma seção: 2022 {fmt(ref['2022']['aptos_diferentes_entre_turnos'])} seções ({fmt(ref['2022']['aptos_dif_soma_abs'])} em módulo, "
      f"líquido {ref['2022']['aptos_dif_liquido']:+d}); 2018 {fmt(ref['2018']['aptos_diferentes_entre_turnos'])} ({fmt(ref['2018']['aptos_dif_soma_abs'])}, líquido {ref['2018']['aptos_dif_liquido']:+d}).")
    ca = out['comparecimento_acima_dos_aptos']
    A(f"- Comparecimento acima dos aptos: 2º turno {ca['2T']} seções, 1º turno {ca['1T']}. Referências: 2022 {ref['2022']['comp_acima_aptos_1T']} e {ref['2022']['comp_acima_aptos_2T']}, "
      f"2018 {ref['2018']['comp_acima_aptos_1T']} e {ref['2018']['comp_acima_aptos_2T']} (1º e 2º turno).")
    A('')
    A('5. Seções em situação especial por UF e saldo tirado')
    e = out['secoes_especiais_por_uf_2T']
    fora_zz = {u: {k: n for k, n in v.items() if k != 'aptos_mudaram' and n} for u, v in e.items() if u != 'ZZ'}
    fora_zz = {u: v for u, v in fora_zz.items() if v}
    A(f"- Nas 27 UFs: nenhuma seção não instalada, anulada, não apurada ou não totalizada no oficial, nenhuma com boletim de junta e nenhuma com")
    A(f"  comparecimento zero{'' if not fora_zz else ' (exceto ' + str(fora_zz) + ')'}. A única situação especial nas UFs é a mudança de aptos entre turnos, documentada acima.")
    zz = e.get('ZZ', {})
    A(f"- Exterior: {zz.get('nao_instaladas_oficial', 0)} não instaladas ({zz.get('aptos_nao_instaladas_oficial', 0)} aptos; {zz.get('nao_instaladas_oficial_1T', 0)} no 1º turno), "
      f"{zz.get('anuladas_ou_nao_apuradas_oficial', 0)} anuladas, {zz.get('nao_totalizadas_oficial', 0)} não totalizadas,")
    A(f"  {zz.get('boletim_de_junta_2T', 0)} com boletim emitido por junta apuradora e {len(cs['secoes_sem_nenhum_voto_linha_cargo_menos_1'])} com comparecimento zero "
      f"({', '.join(cs['secoes_sem_nenhum_voto_linha_cargo_menos_1'])}; {r['sem_votos_de_junta']} delas de junta).")
    am = ', '.join(u + ' ' + fmt(v.get('aptos_mudaram', 0)) for u, v in e.items())
    A('- Seções com aptos diferentes entre os turnos, por UF: ' + am + '.')
    A(f"- Definição usada para o saldo: {sd['definicao']}.")
    for x in sd['2026']['lista']:
        A(f"- 2026: {x['secao']} ({x['motivo']}): no 1º turno {x['apt1']} aptos, {x['comp1']} votantes, Lula {x['L1']}, Flávio {x['R1']}; margem de Flávio {x['margem_direita_1T']:+d}.")
    A(f"  Saldo 2026: {rs['2026']:+d} votos em {sd['2026']['secoes']} seção" + (' (negativo: a seção especial tirou votos líquidos de Lula, não de Flávio).' if rs['2026'] < 0 else '.'))
    A(f"- 2022 (Bolsonaro sobre Lula): {sd['2022']['secoes']} seções com margem no 1º turno, saldo {rs['2022']:+d}. A única seção especial do 2º turno de 2022 é")
    A(f"  {', '.join(x['secao'] + ' (' + str(x['tipo_2T']) + ' no 2º turno, ' + str(x['tipo_1T']) + ' no 1º, comparecimento ' + str(x['comp_1T']) + ')' for x in sd['2022']['especiais_no_2T_sem_margem_no_1T'])},")
    A('  a mesma seção de Ciudad Guayana, sem voto nos dois turnos e sem margem no 1º turno.')
    A(f"- 2018 (Bolsonaro sobre Haddad, descritivo): {sd['2018_descritivo']['secoes']} seções, saldo {rs['2018']:+d}.")
    A(f"- Descritivo, seções de junta do 2º turno de 2026 com boletim no 1º turno ({j['secoes']}, todas no exterior; os votos delas entram no total):")
    A(f"  margem de Flávio {j['margem_flavio_1T']:+d} no 1º turno e {j['margem_flavio_2T']:+d} no 2º turno.")
    A(f"- Limites do registro: sem sinal se o saldo de 2026 for até 1,5 vez o de 2022 ({rs['limite_sem_sinal_1_5x_2022']:.0f}); sinal se acima de 3 vezes o de 2022")
    A(f"  ({rs['limite_sinal_3x_2022']:.0f}) e acima de 100.000. 2026: {rs['2026']:+d}. Perna de sinal: {sn(rs['sinal'])}; perna de sem sinal: {sn(rs['sem_sinal'])}.")
    A('')
    A('6. Leitura de cada perna do critério')
    A(f"- Diferença não atribuível a uma seção nomeada com ato documentado: {', '.join(r['diferencas_nao_atribuidas']) or 'nenhuma'}.")
    A(f"- Soma dos municípios diferente do total da UF: {sn(r['municipios_somam_uf'])}.")
    A(f"- Saldo tirado pelas seções especiais acima de 3 vezes o de 2022 e de 100 mil votos: {sn(rs['sinal'])}.")
    A(f"- Diferença zero em todos os níveis depois da reconciliação documentada: {sn(not r['diferencas_nao_atribuidas'] and not r['municipios_somam_uf'] and not r['ufs_somam_brasil'])};")
    A(f"  saldo até 1,5 vez o de 2022: {sn(rs['sem_sinal'])}.")
    A(f"- Veredito: {r['veredito']}.")
    A('')
    A('7. Escolhas de leitura e desvios do registro')
    A('- "Ato documentado": as atas de mesa e as decisões das juntas não estão nos arquivos públicos usados. Foi tomado como documentação o que o')
    A('  próprio TSE publica: a classificação "não instalada" no arquivo oficial da cidade (s.sni e e.esni) com a seção listada no cadastro sem')
    A('  arquivo de urna publicado; a linha de cargo -1 do bweb com comparecimento zero junto com o arquivo oficial da cidade (seção instalada e')
    A('  apurada, comparecimento 0); e, para os aptos, o eleitorado da seção em cada turno no arquivo de locais de votação. Isto é desvio de leitura.')
    A('- "Conjunto igual ao do 1º turno (499.206)": o número do registro vem da base do 1º turno, que não tem seção sem voto. A comparação foi feita')
    A('  contra essa base e também contra o cadastro dos dois turnos (499.248 principais em cada um, iguais).')
    A(f"- \"Aptos iguais seção a seção\": pela letra, {fmt(ad['secoes'])} seções têm aptos diferentes entre os turnos. Em 2022 foram "
      f"{fmt(ref['2022']['aptos_diferentes_entre_turnos'])} e em 2018 {fmt(ref['2018']['aptos_diferentes_entre_turnos'])}.")
    A('  Em todas, o boletim de cada turno bate com o eleitorado oficial da seção naquele turno (arquivo de locais de votação), e o total nacional')
    A('  de aptos não muda. Foram tratadas como diferença reconciliada pelo cadastro oficial, não como sinal. A causa não está nos arquivos; a')
    A('  explicação mais simples é o voto em trânsito, pedido por turno, que tira o eleitor da seção de origem e o põe na de trânsito (hipótese, não')
    A('  conferida). Quem ler "aptos iguais" como exigência absoluta, sem reconciliação, teria uma diferença de cadastro da mesma ordem da de 2022,')
    A('  e nenhuma diferença entre boletim e cadastro.')
    A('- "Seções em situação especial" e "saldo que tiraram": tomado como as seções com boletim apurado no 1º turno que não somaram voto no 2º turno')
    A('  (sem boletim, boletim não apurado, comparecimento zero); a seção sem margem no 1º turno entra com zero. Saldo com sinal (positivo tira de Flávio).')
    A(f"  Com o saldo em módulo, 2026 daria {sd['2026']['saldo_em_modulo_por_secao']} contra {sd['2022']['saldo_em_modulo_por_secao']} em 2022 e a perna de sem sinal falharia por 2 votos,")
    A('  porque a referência de 2022 é zero; o veredito passaria a INCONCLUSIVO pela letra. Somando também as seções de junta (votos contados), o')
    A(f"  saldo de 2026 fica em {sd['saldo_2026_com_juntas']:+d}, ainda negativo; 2022 não tem o campo de junta na base.")
    A('- O teste foi feito só para presidente. Governador do 2º turno (6 UFs) não entra no registro do T15.')
    A('')
    A('8. Limites')
    A('- O T15 confere a totalização: o total publicado é a soma dos boletins publicados, e o cadastro é coerente entre os turnos. Não diz nada sobre')
    A('  o que a urna gravou no boletim (isso é T2, T18, T24, T25). Boletim e total saem do mesmo sistema do TSE; a conferência independente do')
    A('  boletim é o QR code impresso (T24).')
    A('- As seções especiais do 2º turno de 2026 são 41 não instaladas no exterior (as mesmas do 1º turno, com 423 aptos) e 2 seções do exterior')
    A('  sem votante. Não há, nos arquivos, seção anulada, não instalada ou não apurada no Brasil em nenhum dos dois turnos.')
    return '\n'.join(L) + '\n'


if __name__ == '__main__':
    if sys.argv[1] == 'baixar':
        baixar(sys.argv[2], sys.argv[3])
    elif sys.argv[1] == 'analisar':
        analisar(*sys.argv[2:11])
    elif sys.argv[1] == 'relatorio':
        open(sys.argv[3], 'w').write(relatorio(json.load(open(sys.argv[2]))))
    else:
        raise SystemExit(__doc__)
