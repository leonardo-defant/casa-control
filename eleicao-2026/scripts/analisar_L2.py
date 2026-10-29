"""L2 do Adendo 18: urna trocada entre os turnos e carga fora do padrão, em todas as seções (bweb completo).

Registro (PRE-REGISTRO-2026-10-26.md, Adendo 18, commit bc7decb de 2026-10-29 05:13:35 UTC, antes de rodar):
  - Grupos: seções cujo número de urna mudou entre o 1º e o 2º turno; seções cuja data de carga do 2º turno fica fora
    da faixa entre os percentis 1 e 99 da sua UF.
  - y = virada de Lula (fatia entre os dois finalistas, 2º menos 1º turno), efeito fixo de local, erro agrupado por
    local, peso pelos votos dos finalistas.
  - Sinal: algum grupo com 500 seções ou mais e diferença de 1,0 ponto ou mais a favor de Lula, a mais de 4
    erros-padrão. Sem sinal: diferença abaixo de 0,3 ponto em valor absoluto, com erro-padrão até 0,15.
    Entre os dois: inconclusivo.

Especificação fixada neste arquivo antes de calcular a virada de qualquer grupo (o que o registro não fixou; tudo
listado também no texto de saída como leitura ou desvio):
  1. Universo: seções da base com os dois turnos e voto em pelo menos um finalista em cada turno (L+R > 0).
     Local = UF|município|zona|local de votação do 2º turno (lib.chave_local, como nos outros testes).
  2. y = 100 L2/(L2+R2) - 100 L1/(L1+R1), em pontos. L = 13 (Lula), R = 22 (Flávio).
  3. Peso = L2 + R2 (votos dos finalistas no 2º turno). O registro diz "votos dos finalistas" sem dizer o turno; é
     a convenção do T17 (pré-registro, linha do T17: "peso votos de Lula mais Flávio no 2º turno").
  4. Grupo U (urna trocada): NR_URNA_EFETIVADA do 1º turno diferente do do 2º turno (campo urna da base, conferido
     seção a seção com o bweb do 2º turno; o do 1º turno é conferido com os zips do 1º turno quando lidos).
  5. Grupo C (carga fora do padrão): DT_CARGA_URNA_EFETIVADA do bweb do 2º turno ("Data da carga da urna efetivada",
     no leiame do TSE), com o valor que o campo traz (data e hora). Percentis 1 e 99 por UF (o exterior, ZZ, conta
     como uma UF) sobre todas as seções da UF no bweb do 2º turno com o campo válido; numpy.percentile linear.
     Fora = estritamente antes do percentil 1 ou estritamente depois do percentil 99. Leitura com a data truncada no
     dia sai como robustez.
  6. Modelo, um grupo por vez: y contra o indicador do grupo, efeito fixo de local, peso do item 3, erro agrupado por
     local (lib.fe_ols, CR1). O coeficiente é a diferença, em pontos, entre a virada das seções do grupo e a das
     outras seções do mesmo local. Locais com uma seção só saem (não informam, como em toda regressão within).
  7. "Grupo com 500 seções ou mais": seções do grupo que entram na regressão (depois de sair os locais de uma seção).
     Ao lado, as seções do grupo em locais onde o indicador varia (as que identificam o coeficiente); se a contagem
     mudar o veredito, isso é dito.
  8. Veredito do teste: INCOERÊNCIA (o "sinal" do registro) se algum grupo tem N >= 500, coef >= +1,0 e
     coef/ep > 4. COERENTE (o "sem sinal") se os dois grupos têm |coef| < 0,3 e ep <= 0,15. Senão INCONCLUSIVO.
     Um grupo sozinho recebe a mesma leitura (SINAL, SEM SINAL, ENTRE OS DOIS).
  Robustez (fora do critério, não muda o veredito): placebo (y = fatia de Lula no 1º turno); covariáveis do T17 (log
  dos aptos, variação do comparecimento, fatia de Lula no 1º turno); sem peso; os dois grupos no mesmo modelo; grupo C
  com a data no dia; grupo C só no lado cedo e só no lado tarde; sem as seções de junta; efeito fixo de município;
  y = variação do comparecimento e do branco+nulo.
  Descritivo (fora do registro, escolhido antes de ver a virada dos grupos): subgrupos pela data da carga da urna do
  2º turno (antes do 1º turno, no dia, depois); urna igual com carga nova; e conferências de ordem lógica dos campos
  de carga (mesma urna com código de carga diferente sem recarga depois do 1º turno; carga depois da abertura ou da
  emissão do boletim; a mesma urna em duas seções no mesmo turno).

Uso: python3 -I analisar_L2.py <secoes2026.json.gz> <zips2t_dir> <zips1t_dir|-> <cache_1t.json.gz> <saida.json> <saida.txt>
"""
import os as _os, sys as _sys
_sys.path.insert(0, _os.path.dirname(_os.path.abspath(__file__)))
import collections, csv, datetime, gc, glob, gzip, io, json, math, os, sys, time, zipfile
from multiprocessing import Pool
import numpy as np
from lib import carregar, chave_local, fe_ols

LIM_SINAL, Z_SINAL, N_MIN = 1.0, 4.0, 500
LIM_SEM, EP_SEM = 0.3, 0.15
DIA_1T = datetime.date(2026, 10, 4)
DIA_2T = datetime.date(2026, 10, 25)
CAMPOS = ['NR_URNA_EFETIVADA', 'CD_CARGA_1_URNA_EFETIVADA', 'CD_CARGA_2_URNA_EFETIVADA', 'CD_FLASHCARD_URNA_EFETIVADA',
          'DT_CARGA_URNA_EFETIVADA', 'NR_JUNTA_APURADORA', 'DT_ABERTURA', 'DT_ENCERRAMENTO', 'DT_EMISSAO_BU',
          'DT_BU_RECEBIDO', 'NR_LOCAL_VOTACAO', 'DS_SECOES_AGREGADAS']


def log(msg):
    print(time.strftime('%H:%M:%S'), msg, flush=True)


# ---------------------------------------------------------------- leitura do bweb

def ler_zip(zpath):
    """Linhas de presidente (cargo 1) e de seção sem voto (cargo -1): campos da urna e da carga por seção.
    Filtro no texto cru (rápido para os arquivos grandes do 1º turno) e leitura com o csv só das linhas que passam."""
    z = zipfile.ZipFile(zpath)
    nome = [n for n in z.namelist() if n.lower().endswith('.csv')][0]
    out = {}; linhas = 0; passaram = 0
    pres = b';1;"Presidente";'; semvoto = b';-1;"#NULO#";-1;'
    with z.open(nome) as fh:
        cab = [c.strip().strip('"') for c in fh.readline().decode('latin1').strip().split(';')]
        ix = {c: i for i, c in enumerate(cab)}
        ic = [ix[c] for c in CAMPOS]
        for linha in fh:
            linhas += 1
            if pres not in linha and semvoto not in linha:
                continue
            r = next(csv.reader([linha.decode('latin1').rstrip('\r\n')], delimiter=';'))
            if r[ix['CD_CARGO_PERGUNTA']] not in ('1', '-1'):
                continue
            passaram += 1
            k = f"{r[ix['SG_UF']]}|{int(r[ix['CD_MUNICIPIO']])}|{int(r[ix['NR_ZONA']])}|{int(r[ix['NR_SECAO']])}"
            out.setdefault(k, set()).add(tuple(r[i] for i in ic))
    return os.path.basename(zpath), {k: sorted(v) for k, v in out.items()}, linhas, passaram


def ler_pasta(pasta, rotulo):
    zs = sorted(glob.glob(os.path.join(pasta, '*.zip')), key=lambda p: -os.path.getsize(p))
    log(f'{rotulo}: {len(zs)} zips')
    tot = {}; info = {}
    with Pool(4) as p:
        for nome, out, linhas, passaram in p.imap_unordered(ler_zip, zs):
            info[nome] = {'secoes': len(out), 'linhas': linhas, 'linhas_presidente_ou_sem_voto': passaram}
            tot.update(out)
            log(f'  {nome}: {len(out)} seções')
    return tot, info


def ts(s):
    try:
        return datetime.datetime.strptime(s, '%Y-%m-%d %H:%M:%S')
    except (ValueError, TypeError):
        return None


# ---------------------------------------------------------------- montagem

def montar(base, b2, b1):
    d = carregar(base)
    rows = []
    for k, v in d.items():
        a, b = v.get('1'), v.get('2')
        if a is None or b is None:
            continue
        rows.append({'k': k, 'uf': k.split('|')[0], 'mun': '|'.join(k.split('|')[:2]), 'loc': chave_local(k, b),
                     'loc1': chave_local(k, a), 'u1': a['urna'], 'u2': b['urna'],
                     'L1': a['L'], 'R1': a['R'], 'L2': b['L'], 'R2': b['R'], 'apt1': a['apt'], 'apt2': b['apt'],
                     'c1': a['comp'], 'c2': b['comp'], 'BN1': a['B'] + a['N'], 'BN2': b['B'] + b['N'],
                     'f2': b2.get(k), 'f1': b1.get(k) if b1 is not None else None})
    del d; gc.collect()
    return rows


def grupo_C(b2):
    """Percentis 1 e 99 da data de carga do 2º turno por UF, sobre todas as seções do bweb do 2º turno."""
    por = collections.defaultdict(list); invalidos = []
    for k, v in b2.items():
        t = ts(v[0][4])
        if t is None:
            invalidos.append(k); continue
        por[k.split('|')[0]].append((k, t))
    fora = {}; fora_dia = {}; lim = {}
    for uf, lst in sorted(por.items()):
        x = np.array([(t - datetime.datetime(2026, 1, 1)).total_seconds() for _, t in lst])
        dd = np.array([t.date().toordinal() for _, t in lst], float)
        p1, p99 = np.percentile(x, [1, 99]); q1, q99 = np.percentile(dd, [1, 99])
        b0 = datetime.datetime(2026, 1, 1)
        lim[uf] = {'secoes': len(lst), 'p1': str(b0 + datetime.timedelta(seconds=float(p1))),
                   'p99': str(b0 + datetime.timedelta(seconds=float(p99))),
                   'p1_dia': q1, 'p99_dia': q99,
                   'p1_dia_txt': str(datetime.date.fromordinal(int(math.floor(q1)))) + (f' + {q1 % 1:.2f} dia' if q1 % 1 else ''),
                   'p99_dia_txt': str(datetime.date.fromordinal(int(math.floor(q99)))) + (f' + {q99 % 1:.2f} dia' if q99 % 1 else ''),
                   'min': str(min(t for _, t in lst)), 'max': str(max(t for _, t in lst))}
        for (k, _), xi, di in zip(lst, x, dd):
            if xi < p1: fora[k] = 'cedo'
            elif xi > p99: fora[k] = 'tarde'
            if di < q1: fora_dia[k] = 'cedo'
            elif di > q99: fora_dia[k] = 'tarde'
        lim[uf]['fora'] = sum(1 for k, _ in lst if k in fora)
        lim[uf]['fora_dia'] = sum(1 for k, _ in lst if k in fora_dia)
    return fora, fora_dia, lim, invalidos


# ---------------------------------------------------------------- regressões

def regressao(y, X, loc, w, nomes):
    r = fe_ols(y, X, loc, w, nomes)
    return r


def amostra_est(loc):
    """Máscara das seções que ficam na regressão within (local com 2 ou mais seções)."""
    _, g = np.unique(loc, return_inverse=True)
    return np.bincount(g)[g] >= 2


def ident(D, loc, m):
    """Seções do grupo e locais em que o indicador varia, dentro da amostra m."""
    _, g = np.unique(loc[m], return_inverse=True)
    Dm = D[m]
    s = np.bincount(g, weights=Dm); n = np.bincount(g)
    varia = (s > 0) & (s < n)
    return int(Dm[varia[g]].sum()), int(varia.sum())


def leitura_grupo(c, ep, n):
    if n >= N_MIN and c >= LIM_SINAL and ep > 0 and c / ep > Z_SINAL:
        return 'SINAL'
    if abs(c) < LIM_SEM and ep <= EP_SEM:
        return 'SEM SINAL'
    return 'ENTRE OS DOIS'


def bloco(rot, D, A, mask=None, covs=False, peso=True, fe='loc', y='virada'):
    m = np.ones(len(D), bool) if mask is None else mask.copy()
    yy = A[y]
    X = [D]; nomes = ['grupo']
    if covs:
        X += [A['logapt'], A['dcomp'], A['fat1']]; nomes += ['log_aptos', 'var_comparecimento', 'fatia_Lula_1T']
    X = np.column_stack(X)
    ok = m & np.isfinite(yy) & np.all(np.isfinite(X), 1)
    g = A[fe]
    est = ok & np.zeros(len(D), bool)
    est[ok] = amostra_est(g[ok])
    r = fe_ols(yy[ok], X[ok], g[ok], A['w'][ok] if peso else None, nomes)
    n_grupo = int(D[est].sum())
    n_id, loc_id = ident(D.astype(float), g, est)
    c, e = r['coef']['grupo'], r['ep']['grupo']
    out = {'rotulo': rot, 'n': r['n'], 'locais': r['grupos'], 'n_grupo': n_grupo, 'n_grupo_identifica': n_id,
           'locais_identificam': loc_id, 'coef': c, 'ep': e, 'z': c / e if e > 0 else float('nan'),
           'coef_todos': r['coef'], 'ep_todos': r['ep']}
    return out


# ---------------------------------------------------------------- conferências de ordem lógica (descritivo)

def conferencias(rows, b1, b2):
    res = {}
    # carga depois da abertura ou da emissão do boletim, 2º turno (hora local da urna nos dois campos)
    pos_ab = []; pos_em = []; dia_2t = []
    for k, v in b2.items():
        f = v[0]; tc = ts(f[4]); ta = ts(f[6]); te = ts(f[8])
        if tc is not None and tc.date() >= DIA_2T:
            dia_2t.append({'k': k, 'carga': f[4], 'abertura': f[6], 'emissao': f[8], 'urna': f[0], 'junta': f[5]})
        if tc is not None and ta is not None and tc > ta:
            pos_ab.append(k)
        if tc is not None and te is not None and tc > te:
            pos_em.append(k)
    res['carga_no_dia_do_2T'] = dia_2t
    res['carga_depois_da_abertura_2T'] = pos_ab
    res['carga_depois_da_emissao_2T'] = pos_em
    if b1 is not None:
        pos_ab = []; pos_em = []; dia_1t = []
        for k, v in b1.items():
            f = v[0]; tc = ts(f[4]); ta = ts(f[6]); te = ts(f[8])
            if tc is not None and tc.date() >= DIA_1T:
                dia_1t.append({'k': k, 'carga': f[4], 'abertura': f[6], 'emissao': f[8], 'urna': f[0], 'junta': f[5],
                               'flash_de_carga': f[3]})
            if tc is not None and ta is not None and tc > ta:
                pos_ab.append(k)
            if tc is not None and te is not None and tc > te:
                pos_em.append(k)
        res['carga_no_dia_do_1T_ou_depois'] = dia_1t
        res['carga_depois_da_abertura_1T'] = pos_ab
        res['carga_depois_da_emissao_1T'] = pos_em
    # mesma urna em duas seções no mesmo turno (fora de junta)
    for rot, bb in (('2T', b2), ('1T', b1)):
        if bb is None:
            continue
        cont = collections.defaultdict(list)
        for k, v in bb.items():
            f = v[0]
            if f[5] != '-1':
                continue
            cont[f[0]].append(k)
        dup = {u: ks for u, ks in cont.items() if len(ks) > 1}
        res[f'urna_em_mais_de_uma_secao_{rot}'] = {'urnas': len(dup), 'exemplos': dict(list(sorted(dup.items()))[:20])}
    if b1 is None:
        return res
    # mesma urna nos dois turnos: código e data de carga
    iguais = 0; cod_dif = []; cod_dif_sem_recarga = []; mesmo_cod_data_dif = []; carga2_antes_carga1 = []
    for r in rows:
        f1, f2 = r['f1'], r['f2']
        if f1 is None or f2 is None or r['u1'] != r['u2']:
            continue
        iguais += 1
        a, b = f1[0], f2[0]
        k1, k2 = (a[1], a[2], a[3]), (b[1], b[2], b[3])
        t1, t2 = ts(a[4]), ts(b[4]); em1 = ts(a[8])
        if k1 != k2:
            cod_dif.append(r['k'])
            if t2 is not None and (em1 is None or t2 <= em1) and t2.date() <= DIA_1T:
                cod_dif_sem_recarga.append({'k': r['k'], 'carga1': a[4], 'carga2': b[4], 'emissao1': a[8]})
        elif a[4] != b[4]:
            mesmo_cod_data_dif.append({'k': r['k'], 'carga1': a[4], 'carga2': b[4]})
        if t1 is not None and t2 is not None and t2 < t1:
            carga2_antes_carga1.append({'k': r['k'], 'carga1': a[4], 'carga2': b[4]})
    res['mesma_urna'] = {'secoes': iguais, 'codigo_de_carga_diferente': len(cod_dif),
                         'codigo_diferente_sem_recarga_depois_do_1T': cod_dif_sem_recarga,
                         'mesmo_codigo_data_diferente': mesmo_cod_data_dif,
                         'carga_2T_anterior_a_carga_1T': carga2_antes_carga1}
    # urna trocada: a urna do 2º turno já tinha sido usada no 1º turno em outra seção?
    urna1_secao = {}
    for k, v in b1.items():
        f = v[0]
        if f[5] == '-1':
            urna1_secao.setdefault(f[0], []).append(k)
    onde = collections.Counter(); carga = collections.Counter(); ex = []; sem_carga_nova = []
    for r in rows:
        if r['u1'] == r['u2'] or r['f2'] is None:
            continue
        u2 = str(r['u2'])
        outros = urna1_secao.get(u2)
        if not outros:
            onde['nao_votou_no_1T'] += 1; continue
        o = outros[0]
        if o == r['k']:
            onde['mesma_secao(?)'] += 1
        elif o.split('|')[:3] == r['k'].split('|')[:3]:
            onde['mesmo_municipio_e_zona'] += 1
        elif o.split('|')[:2] == r['k'].split('|')[:2]:
            onde['mesmo_municipio_outra_zona'] += 1
        else:
            onde['outro_municipio'] += 1
        a = b1[o][0]; b = r['f2'][0]
        nova = (a[1], a[2], a[3]) != (b[1], b[2], b[3])
        t2 = ts(b[4]); em1 = ts(a[8])
        depois = t2 is not None and em1 is not None and t2 > em1
        carga[f"codigo_{'novo' if nova else 'igual'}_carga_{'depois' if depois else 'antes'}_da_emissao_1T"] += 1
        if not (nova and depois):
            sem_carga_nova.append({'k': r['k'], 'urna_2T': u2, 'secao_no_1T': o, 'carga_1T': a[4], 'carga_2T': b[4]})
        if len(ex) < 15:
            ex.append({'k': r['k'], 'urna_2T': u2, 'secao_no_1T': o, 'carga_1T': a[4], 'carga_2T': b[4]})
    res['urna_do_2T_usada_no_1T'] = {'contagem': dict(onde), 'carga': dict(carga), 'sem_carga_nova': sem_carga_nova,
                                     'exemplos': ex}
    return res


# ---------------------------------------------------------------- principal

def main():
    base, zips2, zips1, cache1, saida_json, saida_txt = sys.argv[1:7]
    t0 = time.time()
    b2, info2 = ler_pasta(zips2, '2º turno')
    multi2 = [k for k, v in b2.items() if len(v) > 1]
    b1 = None; info1 = None
    if zips1 != '-':
        if os.path.exists(cache1):
            log(f'1º turno: lendo o cache {cache1}')
            with gzip.open(cache1, 'rt') as f:
                c = json.load(f)
            b1, info1 = c['secoes'], c['info']
        else:
            b1, info1 = ler_pasta(zips1, '1º turno')
            with gzip.open(cache1, 'wt') as f:
                json.dump({'secoes': b1, 'info': info1}, f)
    multi1 = [k for k, v in b1.items() if len(v) > 1] if b1 is not None else []
    log('montando')
    rows = montar(base, b2, b1)

    # conferência do número da urna: base contra bweb
    conf = {'secoes_base_dois_turnos': len(rows), 'sem_bweb_2T': [], 'urna2_difere_bweb': [], 'urna1_difere_bweb': [],
            'sem_bweb_1T': [], 'secoes_com_mais_de_um_valor_2T': multi2, 'secoes_com_mais_de_um_valor_1T': multi1,
            'local_mudou_entre_turnos': sum(1 for r in rows if r['loc'] != r['loc1'])}
    for r in rows:
        if r['f2'] is None:
            conf['sem_bweb_2T'].append(r['k'])
        elif str(r['u2']) != r['f2'][0][0]:
            conf['urna2_difere_bweb'].append(r['k'])
        if b1 is not None:
            if r['f1'] is None:
                conf['sem_bweb_1T'].append(r['k'])
            elif str(r['u1']) != r['f1'][0][0]:
                conf['urna1_difere_bweb'].append(r['k'])

    fora, fora_dia, lim, invalidos = grupo_C(b2)

    # vetores
    ok = [r for r in rows if r['L1'] + r['R1'] > 0 and r['L2'] + r['R2'] > 0 and r['f2'] is not None]
    sem_fatia = [r['k'] for r in rows if not (r['L1'] + r['R1'] > 0 and r['L2'] + r['R2'] > 0)]
    A = {}
    f = lambda c: np.array([r[c] for r in ok], float)
    L1, R1, L2, R2 = f('L1'), f('R1'), f('L2'), f('R2')
    A['fat1'] = 100 * L1 / (L1 + R1); A['fat2'] = 100 * L2 / (L2 + R2)
    A['virada'] = A['fat2'] - A['fat1']
    A['w'] = L2 + R2
    apt1, apt2, c1, c2 = f('apt1'), f('apt2'), f('c1'), f('c2')
    with np.errstate(invalid='ignore', divide='ignore'):
        A['logapt'] = np.log(np.maximum(apt2, 1))
        A['dcomp'] = 100 * (c2 / apt2 - c1 / apt1)
        A['dbn'] = 100 * (f('BN2') / c2 - f('BN1') / c1)
    A['loc'] = np.array([r['loc'] for r in ok]); A['mun'] = np.array([r['mun'] for r in ok])
    uf = np.array([r['uf'] for r in ok]); keys = [r['k'] for r in ok]
    DU = np.array([r['u1'] != r['u2'] for r in ok], float)
    DC = np.array([r['k'] in fora for r in ok], float)
    DCd = np.array([r['k'] in fora_dia for r in ok], float)
    DCcedo = np.array([fora.get(r['k']) == 'cedo' for r in ok], float)
    DCtarde = np.array([fora.get(r['k']) == 'tarde' for r in ok], float)
    junta = np.array([r['f2'][0][5] != '-1' for r in ok])
    dcarga = [ts(r['f2'][0][4]) for r in ok]
    pos1t = np.array([t is not None and t.date() > DIA_1T for t in dcarga], float)
    dia1t = np.array([t is not None and t.date() == DIA_1T for t in dcarga], float)
    pre1t = np.array([t is not None and t.date() < DIA_1T for t in dcarga], float)
    log(f'amostra: {len(ok)} seções; U = {int(DU.sum())}; C = {int(DC.sum())}')

    res = {'registro': 'PRE-REGISTRO-2026-10-26.md, Adendo 18, L2 (commit bc7decb, 2026-10-29 05:13:35 UTC)',
           'conferencia': {k: (v if not isinstance(v, list) else {'n': len(v), 'exemplos': v[:20]}) for k, v in conf.items()},
           'info_zips_2T': info2, 'info_zips_1T': info1,
           'carga_por_uf': lim, 'carga_invalida_2T': invalidos,
           'amostra': {'secoes': len(ok), 'sem_fatia_em_algum_turno': len(sem_fatia), 'exemplos_sem_fatia': sem_fatia[:20]},
           'grupos': {}, 'robustez': {}, 'descritivo': {}}

    # principal
    princ = {}
    for nome, D in (('U_urna_trocada', DU), ('C_carga_fora_p1_p99', DC)):
        b = bloco(nome, D, A)
        b['leitura'] = leitura_grupo(b['coef'], b['ep'], b['n_grupo'])
        b['leitura_com_n_que_identifica'] = leitura_grupo(b['coef'], b['ep'], b['n_grupo_identifica'])
        b['efeito_minimo_detectavel_80pct'] = 2.8 * b['ep']
        b['secoes_no_grupo_na_base'] = int(D.sum())
        b['votos_finalistas_2T_no_grupo'] = float(A['w'][D > 0].sum())
        b['virada_media_ponderada_grupo'] = float(np.average(A['virada'][D > 0], weights=A['w'][D > 0]))
        b['virada_media_ponderada_resto'] = float(np.average(A['virada'][D == 0], weights=A['w'][D == 0]))
        princ[nome] = b
        log(f"{nome}: coef {b['coef']:+.3f} ep {b['ep']:.3f} n_grupo {b['n_grupo']} -> {b['leitura']}")
    res['grupos'] = princ
    ls = [b['leitura'] for b in princ.values()]
    if 'SINAL' in ls:
        ver = 'INCOERÊNCIA'
    elif all(l == 'SEM SINAL' for l in ls):
        ver = 'COERENTE'
    else:
        ver = 'INCONCLUSIVO'
    ls2 = [b['leitura_com_n_que_identifica'] for b in princ.values()]
    ver2 = 'INCOERÊNCIA' if 'SINAL' in ls2 else ('COERENTE' if all(l == 'SEM SINAL' for l in ls2) else 'INCONCLUSIVO')
    res['veredito'] = ver; res['veredito_com_n_que_identifica'] = ver2

    # robustez
    rob = {}
    for nome, D in (('U', DU), ('C', DC)):
        rob[f'{nome}_placebo_fatia_Lula_1T'] = bloco(nome, D, A, y='fat1')
        rob[f'{nome}_covariaveis_T17'] = bloco(nome, D, A, covs=True)
        rob[f'{nome}_sem_peso'] = bloco(nome, D, A, peso=False)
        rob[f'{nome}_sem_juntas'] = bloco(nome, D, A, mask=~junta)
        rob[f'{nome}_efeito_fixo_municipio'] = bloco(nome, D, A, fe='mun')
        rob[f'{nome}_y_var_comparecimento'] = bloco(nome, D, A, y='dcomp')
        rob[f'{nome}_y_var_branco_nulo'] = bloco(nome, D, A, y='dbn')
    rob['C_data_no_dia'] = bloco('C_dia', DCd, A)
    rob['C_data_no_dia_placebo'] = bloco('C_dia', DCd, A, y='fat1')
    rob['C_so_cedo'] = bloco('C_cedo', DCcedo, A, mask=DCtarde == 0)
    rob['C_so_tarde'] = bloco('C_tarde', DCtarde, A, mask=DCcedo == 0)
    rob['C_so_tarde_placebo'] = bloco('C_tarde', DCtarde, A, mask=DCcedo == 0, y='fat1')
    # conferência por outro caminho: em cada local com seções dentro e fora do grupo, virada média ponderada do grupo menos a das
    # outras; média simples dessas diferenças entre os locais, erro-padrão entre locais
    for nome, D in (('U', DU), ('C', DC)):
        _, gl = np.unique(A['loc'], return_inverse=True)
        sw_g = np.bincount(gl, weights=A['w'] * D); sy_g = np.bincount(gl, weights=A['w'] * D * A['virada'])
        sw_o = np.bincount(gl, weights=A['w'] * (1 - D)); sy_o = np.bincount(gl, weights=A['w'] * (1 - D) * A['virada'])
        okl = (sw_g > 0) & (sw_o > 0)
        dl = sy_g[okl] / sw_g[okl] - sy_o[okl] / sw_o[okl]
        rob[f'{nome}_comparacao_direta_por_local'] = {'locais': int(okl.sum()), 'media': float(dl.mean()),
                                                      'ep': float(dl.std(ddof=1) / math.sqrt(len(dl))),
                                                      'media_ponderada_votos_do_grupo': float(np.average(dl, weights=sw_g[okl]))}
    # os dois no mesmo modelo
    X = np.column_stack([DU, DC])
    r = fe_ols(A['virada'], X, A['loc'], A['w'], ['U', 'C'])
    rob['U_e_C_juntos'] = r
    for k, b in rob.items():
        if 'coef' in b and 'grupo' in b.get('coef_todos', {}):
            b['leitura_pela_mesma_regua'] = leitura_grupo(b['coef'], b['ep'], b['n_grupo'])
    res['robustez'] = rob

    # descritivo: subgrupos pela data da carga da urna do 2º turno
    des = {}
    for nome, D, m in (('U_carga_2T_antes_do_1T', DU * pre1t, None), ('U_carga_2T_no_dia_do_1T', DU * dia1t, None),
                       ('U_carga_2T_depois_do_1T', DU * pos1t, None), ('mesma_urna_carga_2T_depois_do_1T', (1 - DU) * pos1t, None),
                       ('qualquer_carga_2T_depois_do_1T', pos1t, None)):
        b = bloco(nome, D, A, mask=m)
        b['placebo'] = bloco(nome, D, A, mask=m, y='fat1')
        b['var_comparecimento'] = bloco(nome, D, A, mask=m, y='dcomp')
        b['secoes_no_grupo_na_base'] = int(D.sum())
        des[nome] = b
    # por UF, grupo U (só onde tem 100 ou mais seções do grupo)
    por_uf = {}
    for u in sorted(set(uf.tolist())):
        m = uf == u
        for nome, D in (('U', DU), ('C', DC)):
            if D[m].sum() >= 100:
                try:
                    b = bloco(f'{nome}_{u}', D, A, mask=m)
                    por_uf[f'{nome}_{u}'] = {kk: b[kk] for kk in ('n_grupo', 'n_grupo_identifica', 'coef', 'ep', 'z')}
                except Exception as e:  # noqa
                    por_uf[f'{nome}_{u}'] = {'erro': str(e)}
    des['por_uf_grupos_com_100_ou_mais'] = por_uf
    des['tamanho'] = {'U_por_uf': dict(collections.Counter(uf[DU > 0].tolist())),
                      'C_por_uf': dict(collections.Counter(uf[DC > 0].tolist())),
                      'U_e_C': int((DU * DC).sum()), 'U_sem_C': int((DU * (1 - DC)).sum()), 'C_sem_U': int(((1 - DU) * DC).sum()),
                      'carga_2T_por_dia': dict(sorted(collections.Counter(str(t.date()) for t in dcarga if t is not None).items()))}
    # escala: votos que o coeficiente do grupo representa e a margem nacional
    Ltot, Rtot = float(L2.sum()), float(R2.sum())
    des['escala'] = {'L2_total_amostra': Ltot, 'R2_total_amostra': Rtot, 'margem_2T_amostra': Ltot - Rtot,
                     'fatia_Lula_2T_amostra': 100 * Ltot / (Ltot + Rtot),
                     'virada_nacional_ponderada': float(np.average(A['virada'], weights=A['w']))}
    for nome, b in princ.items():
        votos = b['coef'] / 100 * b['votos_finalistas_2T_no_grupo']
        des['escala'][nome] = {'votos_de_Lula_a_mais_pelo_coef': votos, 'margem_equivalente': 2 * votos,
                               'limite_superior_95_votos': (b['coef'] + 1.96 * b['ep']) / 100 * b['votos_finalistas_2T_no_grupo']}
    des['conferencias_de_ordem'] = conferencias(rows, b1, b2)
    res['descritivo'] = des
    res['segundos'] = time.time() - t0

    def conv(o):
        if isinstance(o, (np.floating,)): return float(o)
        if isinstance(o, (np.integer,)): return int(o)
        if isinstance(o, np.ndarray): return o.tolist()
        if isinstance(o, set): return sorted(o)
        raise TypeError(type(o))
    with open(saida_json, 'w') as fj:
        json.dump(res, fj, ensure_ascii=False, indent=1, default=conv)
    log(f'json em {saida_json}')
    escrever_txt(res, saida_txt)
    log(f'txt em {saida_txt}')


# ---------------------------------------------------------------- texto

def n(x, nd=2):
    if x is None or (isinstance(x, float) and not math.isfinite(x)):
        return 'indefinido'
    s = f'{x:+.{nd}f}' if nd >= 0 else str(x)
    return s.replace('.', ',')


def u(x, nd=2):
    if x is None or (isinstance(x, float) and not math.isfinite(x)):
        return 'indefinido'
    return f'{x:.{nd}f}'.replace('.', ',')


def ni(x):
    return f'{int(round(x)):,}'.replace(',', '.')


def linha_bloco(b):
    return (f"diferença {n(b['coef'])} ponto (ep {u(b['ep'])}, z {n(b['z'])}); {ni(b['n'])} seções em {ni(b['locais'])} locais; "
            f"{ni(b['n_grupo'])} do grupo na regressão, {ni(b['n_grupo_identifica'])} em {ni(b['locais_identificam'])} locais onde o grupo varia")


def escrever_txt(res, caminho):
    L = []
    w = L.append
    g = res['grupos']; rb = res['robustez']; de = res['descritivo']; cf = res['conferencia']
    U, C = g['U_urna_trocada'], g['C_carga_fora_p1_p99']
    w('L2. Urna trocada entre os turnos e carga fora do padrão (Adendo 18), com o bweb completo dos dois turnos de 2026')
    w('Script: scripts/analisar_L2.py. Números completos: resultados/L2_bweb.json.')
    w(f"Rodado em {datetime.date.today()} com a base por seção dos dois turnos (secoes2026.json.gz), os 28 zips do bweb do 2º turno")
    w('(26/10, 07h42) e os 28 zips do bweb do 1º turno (05/10, 14h03), sem baixar nada.')
    w('')
    w('Critério registrado (PRE-REGISTRO-2026-10-26.md, Adendo 18, commit bc7decb de 29/10 05h13 UTC, antes de rodar):')
    w('- Grupos: seções cujo número de urna mudou entre o 1º e o 2º turno; seções cuja data de carga do 2º turno fica fora da')
    w('  faixa entre os percentis 1 e 99 da sua UF.')
    w('- y = virada de Lula (fatia entre os dois finalistas, 2º menos 1º turno), efeito fixo de local, erro agrupado por local,')
    w('  peso pelos votos dos finalistas.')
    w('- Sinal (aqui, INCOERÊNCIA): algum grupo com 500 seções ou mais e diferença de 1,0 ponto ou mais a favor de Lula, a mais')
    w('  de 4 erros-padrão. Sem sinal (aqui, COERENTE): diferença abaixo de 0,3 ponto em valor absoluto, com erro-padrão até 0,15.')
    w('  Entre os dois: INCONCLUSIVO.')
    w('')
    w(f"VEREDITO PELA LETRA: {res['veredito']}")
    w(f"- Grupo U (urna trocada): {U['leitura']}. {linha_bloco(U)}.")
    w(f"- Grupo C (carga fora dos percentis 1 a 99 da UF): {C['leitura']}. {linha_bloco(C)}.")
    if res['veredito_com_n_que_identifica'] != res['veredito']:
        w(f"- Contando só as seções do grupo em locais onde ele varia, o veredito seria {res['veredito_com_n_que_identifica']}.")
    else:
        w('- Contar só as seções do grupo em locais onde o grupo varia (as que identificam a diferença) não muda o veredito.')
    es = res['descritivo']['escala']
    w('')
    w('Resumo')
    w(f"- As {ni(U['secoes_no_grupo_na_base'])} seções que votaram em urna diferente nos dois turnos tiveram a mesma virada de Lula que as outras"
      f" seções do mesmo local: diferença {n(U['coef'])} ponto, com erro-padrão {u(U['ep'])}. O mesmo nas {ni(C['secoes_no_grupo_na_base'])}"
      f" seções com carga da urna fora da faixa da UF: {n(C['coef'])} ({u(C['ep'])}). O teste conseguiria ver uma diferença de cerca de"
      f" {u(2.8 * max(U['ep'], C['ep']))} ponto; o registro pedia 1,0 ponto para sinal.")
    e1 = es['U_urna_trocada']; e2 = es['C_carga_fora_p1_p99']
    w(f"- Em votos: no limite de cima do intervalo de 95%, as urnas trocadas dariam a Lula {ni(e1['limite_superior_95_votos'])} votos a mais,"
      f" e as de carga fora da faixa {ni(e2['limite_superior_95_votos'])}; a margem do 2º turno foi de {ni(es['margem_2T_amostra'])} votos.")
    co = res['descritivo']['conferencias_de_ordem']
    cont = {'carga depois da abertura (2º turno)': len(co['carga_depois_da_abertura_2T']),
            'carga depois da emissão do boletim (2º turno)': len(co['carga_depois_da_emissao_2T']),
            'carga depois da abertura (1º turno)': len(co.get('carga_depois_da_abertura_1T', [])),
            'carga depois da emissão do boletim (1º turno)': len(co.get('carga_depois_da_emissao_1T', [])),
            'mesma urna com código de carga diferente sem recarga depois do 1º turno':
                len(co.get('mesma_urna', {}).get('codigo_diferente_sem_recarga_depois_do_1T', [])),
            'mesma urna, mesmo código, data diferente': len(co.get('mesma_urna', {}).get('mesmo_codigo_data_diferente', [])),
            'mesma urna em duas seções no 2º turno': co.get('urna_em_mais_de_uma_secao_2T', {}).get('urnas', 0),
            'mesma urna em duas seções no 1º turno': co.get('urna_em_mais_de_uma_secao_1T', {}).get('urnas', 0),
            'urna que votou no 1º turno em outra seção e voltou no 2º sem carga nova':
                len(co.get('urna_do_2T_usada_no_1T', {}).get('sem_carga_nova', []))}
    zero = [k for k, v in cont.items() if v == 0]; nz = {k: v for k, v in cont.items() if v}
    w('- Fora do registro, conferências de ordem lógica dos campos de carga (item 7): '
      + (f"nenhum caso de {'; '.join(zero)}." if zero else '')
      + (f" Com casos: {'; '.join(f'{k}: {v}' for k, v in nz.items())}." if nz else ''))
    w('')
    return_txt_corpo(res, w)
    with open(caminho, 'w') as f:
        f.write('\n'.join(L) + '\n')


def return_txt_corpo(res, w):
    """Corpo do texto; todos os números vêm do json."""
    g = res['grupos']; rb = res['robustez']; de = res['descritivo']; cf = res['conferencia']
    U, C = g['U_urna_trocada'], g['C_carga_fora_p1_p99']
    am = res['amostra']['secoes']; t = de['tamanho']; es = de['escala']; co = de['conferencias_de_ordem']
    w('1. Dados e conferências')
    w(f"- Seções com os dois turnos na base: {ni(cf['secoes_base_dois_turnos'])}; com voto em finalista nos dois turnos e no bweb do 2º"
      f" turno: {ni(am)} (sem fatia em algum turno: {ni(res['amostra']['sem_fatia_em_algum_turno'])}).")
    w(f"- Número da urna da base contra o bweb: 2º turno, {ni(cf['urna2_difere_bweb']['n'])} diferenças; 1º turno, {ni(cf['urna1_difere_bweb']['n'])}"
      f" diferenças. Seções da base sem bweb do 2º turno: {ni(cf['sem_bweb_2T']['n'])}; sem bweb do 1º: {ni(cf['sem_bweb_1T']['n'])}.")
    w(f"- Seções com mais de um valor de urna, carga ou horário nas linhas do mesmo boletim: 2º turno {ni(cf['secoes_com_mais_de_um_valor_2T']['n'])},"
      f" 1º turno {ni(cf['secoes_com_mais_de_um_valor_1T']['n'])}. Seções cujo local mudou entre os turnos: {ni(cf['local_mudou_entre_turnos'])}"
      f" (vale o local do 2º turno). Data de carga inválida no 2º turno: {len(res['carga_invalida_2T'])}.")
    w('')
    w('2. Os grupos')
    w(f"- U, urna trocada: {ni(U['secoes_no_grupo_na_base'])} seções ({u(100 * U['secoes_no_grupo_na_base'] / am)}% da amostra),"
      f" {ni(U['votos_finalistas_2T_no_grupo'])} votos nos finalistas no 2º turno.")
    w(f"- C, carga fora dos percentis 1 e 99 da UF: {ni(C['secoes_no_grupo_na_base'])} seções ({u(100 * C['secoes_no_grupo_na_base'] / am)}%),"
      f" {ni(C['votos_finalistas_2T_no_grupo'])} votos. Pela construção, cerca de 2% de cada UF: 1% mais cedo e 1% mais tarde.")
    w(f"- Nos dois grupos: {ni(t['U_e_C'])}; só U: {ni(t['U_sem_C'])}; só C: {ni(t['C_sem_U'])}.")
    dias = t['carga_2T_por_dia']
    pre = sum(v for k, v in dias.items() if k < '2026-10-04'); d1 = dias.get('2026-10-04', 0)
    pos = sum(v for k, v in dias.items() if k > '2026-10-04')
    w(f"- Data da carga da urna que votou no 2º turno, seções da amostra: antes do dia do 1º turno {ni(pre)}, no dia do 1º turno {ni(d1)},"
      f" depois do 1º turno {ni(pos)} (de {min(dias)} a {max(dias)}).")
    w('  Faixa por UF (percentis 1 e 99 do campo, com hora; seções fora):')
    for ufx, v in res['carga_por_uf'].items():
        w(f"    {ufx}: {v['p1'][:16]} a {v['p99'][:16]}, fora {v['fora']} de {v['secoes']}; no dia: {v['p1_dia_txt']} a {v['p99_dia_txt']}, fora {v['fora_dia']}")
    w('')
    w('3. Resultado principal (y = virada de Lula em pontos, efeito fixo de local, peso L2+R2, erro agrupado por local)')
    for rot, b in (('U, urna trocada', U), ('C, carga fora do padrão', C)):
        w(f"- {rot}: {linha_bloco(b)}.")
        w(f"  Leitura pela régua: {b['leitura']}. Efeito mínimo detectável (80% de poder a 5%, 2,8 erros-padrão):"
          f" {u(b.get('efeito_minimo_detectavel_80pct', 2.8 * b['ep']))} ponto. Virada média ponderada no grupo"
          f" {n(b['virada_media_ponderada_grupo'])}, no resto {n(b['virada_media_ponderada_resto'])} (sem controlar o local).")
    w(f"- Virada nacional ponderada na amostra: {n(es['virada_nacional_ponderada'])} ponto.")
    w('')
    w('4. Robustez (fora do critério; não muda o veredito)')
    rot_rob = [('placebo_fatia_Lula_1T', 'placebo, y = fatia de Lula no 1º turno'), ('covariaveis_T17', 'com as covariáveis do T17'),
               ('sem_peso', 'sem peso'), ('sem_juntas', 'sem as seções de junta'), ('efeito_fixo_municipio', 'efeito fixo de município'),
               ('y_var_comparecimento', 'y = variação do comparecimento (pontos dos aptos)'),
               ('y_var_branco_nulo', 'y = variação do branco+nulo (pontos do comparecimento)')]
    for gnome in ('U', 'C'):
        for kk, rot in rot_rob:
            b = rb[f'{gnome}_{kk}']
            w(f"- {gnome}, {rot}: {n(b['coef'])} (ep {u(b['ep'])}, z {n(b['z'])}), {ni(b['n_grupo'])} do grupo.")
    for kk, rot in (('C_data_no_dia', 'C com a data no dia'), ('C_data_no_dia_placebo', 'C com a data no dia, placebo'),
                    ('C_so_cedo', 'C só o lado cedo (contra as seções dentro da faixa)'),
                    ('C_so_tarde', 'C só o lado tarde (contra as seções dentro da faixa)'),
                    ('C_so_tarde_placebo', 'C só o lado tarde, placebo')):
        b = rb[kk]
        w(f"- {rot}: {n(b['coef'])} (ep {u(b['ep'])}, z {n(b['z'])}), {ni(b['n_grupo'])} do grupo, {ni(b['n_grupo_identifica'])} identificam.")
    for gnome in ('U', 'C'):
        x = rb.get(f'{gnome}_comparacao_direta_por_local')
        if x:
            w(f"- {gnome}, conferência por outro caminho (diferença dentro de cada local, média entre os {ni(x['locais'])} locais):"
              f" {n(x['media'])} (ep {u(x['ep'])}); ponderada pelos votos do grupo {n(x['media_ponderada_votos_do_grupo'])}.")
    j = rb['U_e_C_juntos']
    w(f"- U e C no mesmo modelo: U {n(j['coef']['U'])} (ep {u(j['ep']['U'])}), C {n(j['coef']['C'])} (ep {u(j['ep']['C'])}).")
    w('')
    w('5. Descritivo (fora do registro): pela data da carga da urna do 2º turno')
    for kk, rot in (('U_carga_2T_antes_do_1T', 'urna trocada, urna do 2º turno carregada antes do 1º turno'),
                    ('U_carga_2T_no_dia_do_1T', 'urna trocada, carregada no dia do 1º turno'),
                    ('U_carga_2T_depois_do_1T', 'urna trocada, carregada depois do 1º turno'),
                    ('mesma_urna_carga_2T_depois_do_1T', 'mesma urna, carga com data depois do 1º turno'),
                    ('qualquer_carga_2T_depois_do_1T', 'qualquer seção com carga depois do 1º turno')):
        b = de[kk]
        try:
            vc = b.get('var_comparecimento')
            w(f"- {rot}: {ni(b['secoes_no_grupo_na_base'])} seções; virada {n(b['coef'])} (ep {u(b['ep'])}, z {n(b['z'])});"
              f" placebo {n(b['placebo']['coef'])} (ep {u(b['placebo']['ep'])})"
              + (f"; variação do comparecimento {n(vc['coef'])} (ep {u(vc['ep'])})" if vc else '')
              + f"; {ni(b['n_grupo_identifica'])} identificam.")
        except Exception:
            w(f"- {rot}: sem estimativa.")
    w('- Por UF, onde o grupo tem 100 seções ou mais:')
    for kk, b in de['por_uf_grupos_com_100_ou_mais'].items():
        if 'erro' in b:
            w(f"    {kk}: sem estimativa ({b['erro']})")
        else:
            w(f"    {kk}: {n(b['coef'])} (ep {u(b['ep'])}), {ni(b['n_grupo'])} do grupo, {ni(b['n_grupo_identifica'])} identificam")
    w('')
    w('6. Escala: quanto o grupo poderia mover')
    w(f"- Margem de Lula no 2º turno na amostra: {ni(es['margem_2T_amostra'])} votos ({u(es['fatia_Lula_2T_amostra'])}% dos votos nos finalistas).")
    for nome, rot in (('U_urna_trocada', 'U'), ('C_carga_fora_p1_p99', 'C')):
        e = es[nome]
        w(f"- {rot}: o coeficiente equivale a {ni(e['votos_de_Lula_a_mais_pelo_coef'])} votos de Lula a mais (margem {ni(e['margem_equivalente'])});"
          f" no limite de 95% de cima, {ni(e['limite_superior_95_votos'])} votos (margem {ni(2 * e['limite_superior_95_votos'])}).")
    w('')
    w('7. Conferências de ordem lógica dos campos de carga (descritivo, fora do registro)')
    w(f"- Carga com data no dia do 2º turno: {len(co['carga_no_dia_do_2T'])} seções; carga depois da abertura do 2º turno:"
      f" {len(co['carga_depois_da_abertura_2T'])}; carga depois da emissão do boletim: {len(co['carga_depois_da_emissao_2T'])}.")
    for x in co['carga_no_dia_do_2T'][:10]:
        w(f"    {x['k']}: carga {x['carga']}, abertura {x['abertura']}, emissão {x['emissao']}, urna {x['urna']}")
    if 'carga_no_dia_do_1T_ou_depois' in co:
        w(f"- 1º turno: carga com data no dia do 1º turno ou depois: {len(co['carga_no_dia_do_1T_ou_depois'])} seções; carga depois da"
          f" abertura: {len(co['carga_depois_da_abertura_1T'])}; depois da emissão do boletim: {len(co['carga_depois_da_emissao_1T'])}.")
        for x in co['carga_no_dia_do_1T_ou_depois'][:12]:
            w(f"    {x['k']}: carga {x['carga']}, abertura {x['abertura']}, emissão {x['emissao']}, urna {x['urna']},"
              f" flash de carga {x.get('flash_de_carga', '?')}")
        if co['carga_depois_da_abertura_1T']:
            w(f"  Carga depois da abertura no 1º turno: {', '.join(co['carga_depois_da_abertura_1T'])}. A leitura compatível com o procedimento é")
            w('  urna de contingência carregada no dia, que recebeu a votação começada na urna original (a abertura registrada é a da original);')
            w('  não há log dessas seções nos arquivos locais para confirmar. Janela de carga é assunto do L1; aqui só ficam listadas.')
    for rot in ('2T', '1T'):
        kk = f'urna_em_mais_de_uma_secao_{rot}'
        if kk in co:
            w(f"- Mesma urna em mais de uma seção no {rot[0]}º turno (fora de junta): {co[kk]['urnas']} urnas."
              + (f" Exemplos: {json.dumps(dict(list(co[kk]['exemplos'].items())[:5]), ensure_ascii=False)}" if co[kk]['urnas'] else ''))
    if 'mesma_urna' in co:
        m = co['mesma_urna']
        w(f"- Mesma urna nos dois turnos: {ni(m['secoes'])} seções; código de carga diferente entre os turnos: {ni(m['codigo_de_carga_diferente'])};"
          f" desses, com a carga do 2º turno datada antes da emissão do boletim do 1º turno (recarga impossível): {len(m['codigo_diferente_sem_recarga_depois_do_1T'])};"
          f" mesmo código com data diferente: {len(m['mesmo_codigo_data_diferente'])}; carga do 2º turno anterior à do 1º: {len(m['carga_2T_anterior_a_carga_1T'])}.")
        for x in (m['codigo_diferente_sem_recarga_depois_do_1T'][:10] + m['mesmo_codigo_data_diferente'][:5] + m['carga_2T_anterior_a_carga_1T'][:5]):
            w(f"    {json.dumps(x, ensure_ascii=False)}")
    if 'urna_do_2T_usada_no_1T' in co:
        x = co['urna_do_2T_usada_no_1T']
        w(f"- Urna trocada: a urna do 2º turno já tinha votado no 1º turno em outra seção? {json.dumps(x['contagem'], ensure_ascii=False)}.")
        if 'carga' in x:
            w(f"  Carga dessas urnas reaproveitadas: {json.dumps(x['carga'], ensure_ascii=False)}. Reaproveitadas sem carga nova depois do"
              f" 1º turno: {len(x['sem_carga_nova'])}.")
            for e in x['sem_carga_nova'][:10]:
                w(f"    {json.dumps(e, ensure_ascii=False)}")
    w('')
    w('8. Leituras e desvios (o que o registro não fixou; escolhido antes de ver a virada dos grupos)')
    w('- Peso: "votos dos finalistas" sem dizer o turno; usado L2+R2 (2º turno), a convenção do T17. Sem peso, o resultado não muda (item 4).')
    w('- Data de carga: o campo DT_CARGA_URNA_EFETIVADA do bweb do 2º turno, que o leiame do TSE chama de "Data da carga da urna efetivada",')
    w('  com o valor que ele traz (data e hora, ao minuto). Leitura alternativa, com a data truncada no dia, no item 4: mesmo resultado.')
    w('- Percentis 1 e 99 por UF sobre todas as seções do bweb do 2º turno da UF (exterior como uma UF), numpy.percentile linear; fora = estritamente')
    w('  antes do p1 ou depois do p99. Com o campo ao minuto, o grupo tem cerca de 2% de cada UF por construção, metade de cada lado.')
    w('- "Grupo com 500 seções ou mais": seções do grupo na regressão (sai o local de uma seção só). Contar só as dos locais onde o grupo varia')
    w(f"  não muda o veredito (U: {ni(U['n_grupo_identifica'])}; C: {ni(C['n_grupo_identifica'])}).")
    w('- Veredito do teste: INCOERÊNCIA se algum grupo dá sinal; COERENTE só se os dois dão sem sinal; senão INCONCLUSIVO.')
    w(f"- Local: o do 2º turno ({ni(cf['local_mudou_entre_turnos'])} seções mudaram de local entre os turnos). Universo: as {ni(cf['secoes_base_dois_turnos'])} seções com os dois turnos; ficam de fora")
    w('  ZZ|30686|1|443 (só 1º turno na base) e ZZ|29564|1|91 (só no bweb do 2º turno, sem comparecimento).')
    w('')
    w('9. O que este teste não vê')
    w('- Ele compara as urnas trocadas, e as de carga fora da faixa, com as outras seções do mesmo local. Uma alteração que agisse igual em todas')
    w('  as urnas, trocadas ou não, não aparece aqui: o teste só responde se a troca de urna ou a carga fora de hora serviram de caminho.')
    w('- O bweb mostra só a urna que gerou o boletim. Troca no meio do dia do 2º turno (votos em duas urnas) só aparece no log da urna,')
    w('  que não foi lido para todas as seções. Também não diz se a urna de contingência foi usada no 1º turno.')
    w('- A data de carga é a que a própria urna registrou. Não foi comparada com as atas de carga e lacre dos TREs, que não foram obtidas, nem os')
    w('  códigos de carga com o relatório de carga de cada zona.')
    w('- Horários: a carga e a abertura são horas locais da urna; o teste de ordem compara campos do mesmo boletim, sem conversão de fuso.')
    w('')


if __name__ == '__main__':
    if len(sys.argv) > 1 and sys.argv[1] == '--so_texto':
        with open(sys.argv[2]) as fj:
            escrever_txt(json.load(fj), sys.argv[3])
    else:
        main()
