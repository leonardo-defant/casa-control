"""T31 do pré-registro (Adendo 9): seções votadas em cédula, com o bweb completo do 2º turno.

Registro (PRE-REGISTRO-2026-10-26.md, Adendo 9, escrito antes dos dados):
  - Seções do 2º turno de 2026 e de 2022 apuradas pela junta por cédula. Para cada uma, variação da fatia de Lula menos
    a média das outras seções do local (ou município). Estimativa conjunta com intervalo e efeito mínimo detectável
    calculado antes.
  - Sinal: efeito de -1,8 ponto ou menos a mais de 2,5 erros-padrão, com 30 seções ou mais.
  - Sem sinal: entre -0,7 e +0,7 com efeito mínimo detectável até 1,8. Acima de 1,8, sem poder.

Especificação fixada neste arquivo antes de calcular qualquer variação das seções de cédula (escolhas que o registro não
fixou; todas listadas também no texto de saída como leitura ou desvio):
  1. Seção de cédula, 2026: boletim do 2º turno emitido por junta apuradora (NR_JUNTA_APURADORA diferente de -1 no
     bweb do 2º turno). O bweb não tem campo que separe cédula de recuperação de dados pela junta; toda seção com
     boletim de junta entra. 2022: a base secoes2022.json.gz não tem o campo de junta e os zips do bweb de 2022 não
     estão nos arquivos locais (a regra da rodada proíbe baixar). Marca usada: boletim do 2º turno sem hora de
     abertura e sem hora de encerramento (a urna não abriu votação; o boletim saiu do sistema de apuração). A marca é
     conferida em 2026, onde existem os dois campos: tem de coincidir, seção a seção, com o campo de junta em todos os
     28 arquivos do 2º turno e nos arquivos do 1º turno do exterior e de MG.
  2. Fatia de Lula = 100 L / (L + R) em cada turno (entre os dois finalistas, como no T17); variação = 2º menos 1º
     turno, em pontos. 2022: L = Lula, R = Bolsonaro. Seção sem voto num finalista em algum turno não tem fatia e sai.
  3. "Outras seções do local (ou município)": leitura literal. Todas as outras seções do mesmo local de votação
     (UF|município|zona|local do 2º turno) com fatia nos dois turnos; se não houver nenhuma, as outras seções do mesmo
     município. Sem nenhuma das duas, a seção não entra na estimativa (listada). Média simples das variações.
  4. Estimativa conjunta, por ano: média simples de d_i = variação da seção de cédula menos a média das outras.
     Erro-padrão agrupado por município (CR1 para a média), porque seções do mesmo município podem dividir as
     mesmas seções de comparação; o erro-padrão sem agrupar sai ao lado. Intervalo de 95% com t de Student
     (graus de liberdade = municípios menos 1).
  5. Efeito mínimo detectável (EMD) calculado antes: só com as seções de urna eletrônica (que fazem o papel de placebo)
     e com o tamanho das seções de cédula, sem usar a variação destas. Para cada seção de urna com comparação (mesma
     regra do item 3), d_j; variância de d_j por território (exterior ou Brasil) e faixa de votos nos dois finalistas
     no 2º turno (1-10, 11-25, 26-50, 51-100, 101-200, 201-400, 401 ou mais). EP antes = raiz da soma das variâncias
     das faixas das seções de cédula utilizáveis, dividida pelo número delas. EMD = 2,8 EP antes (80% de poder a 5%,
     a mesma convenção do T17). Sem nenhuma seção utilizável, EMD indefinido (infinito).
  6. Veredito, pela letra, para o 2º turno de 2026 (2022 é a referência registrada e recebe a mesma leitura):
     SINAL se N >= 30, efeito <= -1,8 e efeito/EP <= -2,5; senão SEM SINAL se -0,7 <= efeito <= +0,7 e EMD <= 1,8;
     senão SEM PODER se EMD > 1,8 (ou indefinido); senão INCONCLUSIVO.
  Robustez (fora do critério, sem mudar o veredito): comparação só com seções de urna eletrônica (sem as outras de
  cédula); média das outras ponderada por votos (fatia somada das outras); média de d ponderada pelos votos da seção;
  teste por reamostragem do placebo (sorteios de seções de urna da mesma faixa e território); 2022 só exterior e só
  Brasil; 2026 e 2022 juntos.
  Descritivo fora do registro: no exterior, seções de cédula contra todas as seções de urna do exterior (mesma faixa
  de votos), em 2026 e em 2022, e a diferença entre os dois anos.

Uso: python3 -I analisar_T31.py <zips2t_dir> <zips1t_dir> <secoes2026.json.gz> <secoes2022.json.gz> <saida.json> <saida.txt>
"""
import os as _os, sys as _sys
_sys.path.insert(0, _os.path.dirname(_os.path.abspath(__file__)))
import collections, csv, gc, glob, io, json, math, os, sys, time, zipfile
from multiprocessing import Pool
import numpy as np
from lib import carregar, chave_local

FAIXAS = [0, 10, 25, 50, 100, 200, 400, 10 ** 9]
SEMENTE = 20261029
N_SORTEIOS = 20000
LIM_SINAL, Z_SINAL, N_MIN = -1.8, -2.5, 30
FAIXA_SEM_SINAL, EMD_MAX = 0.7, 1.8
FATOR_EMD = 2.8


def log(msg):
    print(time.strftime('%H:%M:%S'), msg, flush=True)


# ---------------------------------------------------------------- leitura dos campos de junta no bweb

def ler_zip_2t(zpath):
    """Todas as linhas de presidente (cargo 1) e de seção sem voto (cargo -1) do 2º turno: campos do boletim."""
    out = {}
    z = zipfile.ZipFile(zpath)
    nome = [n for n in z.namelist() if n.lower().endswith('.csv')][0]
    with z.open(nome) as fh:
        rd = csv.reader(io.TextIOWrapper(fh, encoding='latin1', newline=''), delimiter=';')
        cab = next(rd); ix = {c.strip(): i for i, c in enumerate(cab)}
        for r in rd:
            cargo = r[ix['CD_CARGO_PERGUNTA']]
            if cargo not in ('1', '-1'):
                continue
            k = f"{r[ix['SG_UF']]}|{int(r[ix['CD_MUNICIPIO']])}|{int(r[ix['NR_ZONA']])}|{int(r[ix['NR_SECAO']])}"
            s = out.get(k)
            if s is None:
                s = out[k] = {'junta': r[ix['NR_JUNTA_APURADORA']], 'turma': r[ix['NR_TURMA_APURADORA']],
                              'ab': r[ix['DT_ABERTURA']], 'enc': r[ix['DT_ENCERRAMENTO']],
                              'urna': r[ix['NR_URNA_EFETIVADA']], 'emissao': r[ix['DT_EMISSAO_BU']],
                              'tipo': r[ix['DS_TIPO_URNA']], 'apt': int(r[ix['QT_APTOS']]),
                              'comp': int(r[ix['QT_COMPARECIMENTO']]), 'nm': r[ix['NM_MUNICIPIO']],
                              'L': 0, 'R': 0, 'B': 0, 'N': 0, 'sem_votos': cargo == '-1', 'campos': set()}
            s['campos'].add((r[ix['NR_JUNTA_APURADORA']], r[ix['DT_ABERTURA']], r[ix['DT_ENCERRAMENTO']]))
            if cargo == '1':
                tv = int(r[ix['CD_TIPO_VOTAVEL']]); nv = int(r[ix['NR_VOTAVEL']]); q = int(r[ix['QT_VOTOS']])
                if tv == 2: s['B'] += q
                elif tv == 3: s['N'] += q
                elif nv == 13: s['L'] += q
                elif nv == 22: s['R'] += q
    for s in out.values():
        s['campos'] = sorted(s['campos'])
    return os.path.basename(zpath), out


def ler_zip_1t_marcas(zpath):
    """1º turno: só as linhas de presidente com junta diferente de -1 ou sem hora de abertura/encerramento.
    Filtro rápido no texto cru (linha que termina em "-1";"-1" e não tem campo vazio é pulada) e leitura completa
    das demais. Conta também as seções com presidente, para o denominador."""
    z = zipfile.ZipFile(zpath)
    nome = [n for n in z.namelist() if n.lower().endswith('.csv')][0]
    marcadas = {}; secoes = set(); linhas = 0
    with z.open(nome) as fh:
        cab = [c.strip().strip('"') for c in fh.readline().decode('latin1').strip().split(';')]
        ix = {c: i for i, c in enumerate(cab)}
        fim_normal = b'"-1";"-1"'
        pres = b';1;"Presidente";'
        for linha in fh:
            linhas += 1
            if pres not in linha:
                continue
            t = linha.rstrip(b'\r\n')
            campos_cru = t.split(b';')
            secoes.add((campos_cru[ix['CD_MUNICIPIO']], campos_cru[ix['NR_ZONA']], campos_cru[ix['NR_SECAO']]))
            if t.endswith(fim_normal) and b';"";' not in t and b';;' not in t:
                continue
            r = next(csv.reader([t.decode('latin1')], delimiter=';'))
            if r[ix['CD_CARGO_PERGUNTA']] != '1':
                continue
            k = f"{r[ix['SG_UF']]}|{int(r[ix['CD_MUNICIPIO']])}|{int(r[ix['NR_ZONA']])}|{int(r[ix['NR_SECAO']])}"
            m = marcadas.setdefault(k, set())
            m.add((r[ix['NR_JUNTA_APURADORA']], r[ix['DT_ABERTURA']], r[ix['DT_ENCERRAMENTO']], r[ix['NR_URNA_EFETIVADA']]))
    return os.path.basename(zpath), {k: sorted(v) for k, v in marcadas.items()}, len(secoes), linhas


# ---------------------------------------------------------------- montagem das seções

def montar(base, junta2=None):
    """Seções com os dois turnos. junta2: conjunto de seções de junta do 2º turno (campo do bweb); se None, usa a marca
    (boletim do 2º turno sem abertura e sem encerramento)."""
    d = carregar(base)
    rows = []
    marca2 = set(); marca1 = set(); apt_marca2 = {}
    for k, v in d.items():
        b = v.get('2')
        if b is not None and b.get('ab', 'x') == '' and b.get('enc', 'x') == '':
            marca2.add(k); apt_marca2[k] = b['apt']
        a = v.get('1')
        if a is not None and a.get('ab', 'x') == '' and a.get('enc', 'x') == '':
            marca1.add(k)
        if a is None or b is None:
            continue
        uf, mun, zona, sec = k.split('|')
        rows.append((k, uf, f'{uf}|{mun}', chave_local(k, b), a['L'], a['R'], b['L'], b['R'], b['apt']))
    del d; gc.collect()
    J = set(junta2) if junta2 is not None else set(marca2)
    return rows, J, marca2, marca1, apt_marca2


def variacoes(rows, J):
    """Para cada seção com fatia nos dois turnos: variação; comparação literal (outras do local, senão do município),
    só com urna eletrônica (robustez) e ponderada por votos (robustez)."""
    keys = [r[0] for r in rows]
    L1 = np.array([r[4] for r in rows], float); R1 = np.array([r[5] for r in rows], float)
    L2 = np.array([r[6] for r in rows], float); R2 = np.array([r[7] for r in rows], float)
    apt = np.array([r[8] for r in rows], float)
    ok = (L1 + R1 > 0) & (L2 + R2 > 0)
    idx = np.nonzero(ok)[0]
    keys = [keys[i] for i in idx]
    uf = np.array([rows[i][1] for i in idx]); mun = [rows[i][2] for i in idx]; loc = [rows[i][3] for i in idx]
    L1, R1, L2, R2, apt = L1[ok], R1[ok], L2[ok], R2[ok], apt[ok]
    V1, V2 = L1 + R1, L2 + R2
    delta = 100 * (L2 / V2 - L1 / V1)
    isJ = np.array([k in J for k in keys])
    _, gl = np.unique(loc, return_inverse=True)
    _, gm = np.unique(mun, return_inverse=True)

    res = {}
    for nome, inset in (('literal', np.ones(len(keys))), ('so_urna', (~isJ).astype(float))):
        # inset = 1 se a seção pode servir de comparação nesta variante; a própria seção sai das "outras"
        def ag(g, x):
            return np.bincount(g, weights=inset * x)
        um = np.ones(len(keys))
        n_out_l = ag(gl, um)[gl] - inset
        n_out_m = ag(gm, um)[gm] - inset
        nivel = np.where(n_out_l > 0, 1, np.where(n_out_m > 0, 2, 0))  # 1 local, 2 município, 0 nenhum
        media = np.full(len(keys), np.nan)
        media = np.where(nivel == 1, (ag(gl, delta)[gl] - inset * delta) / np.where(n_out_l > 0, n_out_l, 1), media)
        media = np.where(nivel == 2, (ag(gm, delta)[gm] - inset * delta) / np.where(n_out_m > 0, n_out_m, 1), media)
        pond = np.full(len(keys), np.nan)
        for niv, g in ((1, gl), (2, gm)):
            l1 = ag(g, L1)[g] - inset * L1; v1 = ag(g, V1)[g] - inset * V1
            l2 = ag(g, L2)[g] - inset * L2; v2 = ag(g, V2)[g] - inset * V2
            with np.errstate(invalid='ignore', divide='ignore'):
                p = 100 * (l2 / v2 - l1 / v1)
            pond = np.where((nivel == niv) & (v1 > 0) & (v2 > 0), p, pond)
        n_out = np.where(nivel == 1, n_out_l, np.where(nivel == 2, n_out_m, 0))
        jf = isJ.astype(float)
        nJ_out = np.where(nivel == 1, ag(gl, jf)[gl] - inset * jf, np.where(nivel == 2, ag(gm, jf)[gm] - inset * jf, 0))
        res[nome] = {'nivel': nivel, 'media': media, 'pond': pond, 'n_out': n_out, 'nJ_out': nJ_out}
    terr = np.where(uf == 'ZZ', 'ZZ', 'BR')
    faixa = np.digitize(V2, FAIXAS[1:-1], right=True)
    return {'keys': keys, 'uf': uf, 'mun': np.array(mun), 'loc': np.array(loc), 'L1': L1, 'R1': R1, 'L2': L2,
            'R2': R2, 'V2': V2, 'apt': apt, 'delta': delta, 'isJ': isJ, 'terr': terr, 'faixa': faixa, 'cmp': res}


# ---------------------------------------------------------------- estatísticas

def ep_media_agrupado(x, g):
    x = np.asarray(x, float); n = len(x)
    if n < 2:
        return float('nan'), 0
    _, gi = np.unique(g, return_inverse=True); G = gi.max() + 1
    e = x - x.mean()
    S = np.bincount(gi, weights=e)
    if G < 2:
        return float('nan'), int(G)
    v = G / (G - 1) * (S ** 2).sum() / n ** 2
    return float(math.sqrt(v)), int(G)


def t_quantil(df, p=0.975):
    """Quantil da t de Student por bissecção na função de distribuição (sem scipy)."""
    if df is None or df < 1 or not math.isfinite(df):
        return 1.959964
    def cdf(t):
        x = df / (df + t * t)
        # função beta incompleta regularizada por fração contínua (Numerical Recipes)
        a, b = df / 2.0, 0.5
        def betacf(a, b, x):
            qab, qap, qam = a + b, a + 1, a - 1
            c, d = 1.0, 1 - qab * x / qap
            d = 1 / (d if abs(d) > 1e-30 else 1e-30); h = d
            for m in range(1, 300):
                m2 = 2 * m
                aa = m * (b - m) * x / ((qam + m2) * (a + m2))
                d = 1 + aa * d; d = 1 / (d if abs(d) > 1e-30 else 1e-30)
                c = 1 + aa / c if abs(c) > 1e-30 else 1e30
                h *= d * c
                aa = -(a + m) * (qab + m) * x / ((a + m2) * (qap + m2))
                d = 1 + aa * d; d = 1 / (d if abs(d) > 1e-30 else 1e-30)
                c = 1 + aa / c if abs(c) > 1e-30 else 1e30
                de = d * c; h *= de
                if abs(de - 1) < 1e-12:
                    break
            return h
        lbeta = math.lgamma(a) + math.lgamma(b) - math.lgamma(a + b)
        bt = math.exp(a * math.log(x) + b * math.log(1 - x) - lbeta) if 0 < x < 1 else 0.0
        if x < (a + 1) / (a + b + 2):
            ib = bt * betacf(a, b, x) / a
        else:
            ib = 1 - bt * betacf(b, a, 1 - x) / b
        return 1 - 0.5 * ib if t > 0 else 0.5 * ib
    lo, hi = 0.0, 100.0
    for _ in range(200):
        mid = (lo + hi) / 2
        if cdf(mid) < p: lo = mid
        else: hi = mid
    return (lo + hi) / 2


def placebo_variancias(V, mask_pool):
    """Variância e média de d das seções de urna por (território, faixa), na comparação literal."""
    c = V['cmp']['literal']
    d = V['delta'] - c['media']
    tab = {}
    for terr in ('ZZ', 'BR'):
        for f in range(len(FAIXAS) - 1):
            m = mask_pool & (V['terr'] == terr) & (V['faixa'] == f) & (c['nivel'] > 0)
            x = d[m]
            if len(x) >= 2:
                tab[(terr, f)] = {'n': int(len(x)), 'media': float(x.mean()), 'var': float(x.var(ddof=1)),
                                  'dp': float(x.std(ddof=1)), 'idx': np.nonzero(m)[0]}
            else:
                tab[(terr, f)] = {'n': int(len(x)), 'media': float('nan'), 'var': float('nan'), 'dp': float('nan'), 'idx': np.nonzero(m)[0]}
    return tab, d


def faixa_rot(f):
    a, b = FAIXAS[f] + 1, FAIXAS[f + 1]
    return f'{a} ou mais' if b >= 10 ** 9 else f'{a}-{b}'


def emd_antes(V, sel, tab):
    """EP antes e EMD, só com o tamanho das seções de cédula utilizáveis e a variância do placebo."""
    if len(sel) == 0:
        return {'N': 0, 'ep_antes': None, 'emd': None, 'emd_texto': 'indefinido (nenhuma seção utilizável)'}
    vs = []
    faltou = []; usadas = collections.Counter(); n_placebo = {}
    for i in sel:
        t = tab[(V['terr'][i], V['faixa'][i])]
        if not math.isfinite(t['var']):
            faltou.append(V['keys'][i]); continue
        vs.append(t['var'])
        rot = f"{V['terr'][i]}|{faixa_rot(int(V['faixa'][i]))}"
        usadas[rot] += 1; n_placebo[rot] = t['n']
    ep = math.sqrt(sum(vs)) / len(vs) if vs else float('nan')
    return {'N': int(len(sel)), 'ep_antes': ep, 'emd': FATOR_EMD * ep, 'faixas_sem_placebo': faltou,
            'faixas_usadas': {k: {'secoes_de_cedula': v, 'secoes_de_urna_no_placebo': n_placebo[k]} for k, v in usadas.items()}}


def sorteio_placebo(V, sel, tab, rng, n=N_SORTEIOS):
    """Médias de d em conjuntos sorteados de seções de urna, mesma faixa e território de cada seção de cédula."""
    if len(sel) == 0:
        return None
    c = V['cmp']['literal']; d = V['delta'] - c['media']
    tot = np.zeros(n); usados = 0
    for i in sel:
        pool = tab[(V['terr'][i], V['faixa'][i])]['idx']
        if len(pool) == 0:
            continue
        tot += d[pool[rng.integers(0, len(pool), n)]]; usados += 1
    return tot / usados if usados else None


def estimar(V, sel, tab, rng, rotulo):
    c = V['cmp']['literal']
    out = {'rotulo': rotulo, 'N': int(len(sel))}
    out['emd_antes'] = emd_antes(V, sel, tab)
    if len(sel) == 0:
        out['efeito'] = None
        return out
    d = V['delta'][sel] - c['media'][sel]
    mun = V['mun'][sel]
    ep_g, G = ep_media_agrupado(d, mun)
    ep_iid = float(d.std(ddof=1) / math.sqrt(len(d))) if len(d) > 1 else float('nan')
    tq = t_quantil(G - 1) if G >= 2 else float('nan')
    est = float(d.mean())
    out.update({'efeito': est, 'ep': ep_g, 'municipios': G, 'ep_sem_agrupar': ep_iid,
                'z': est / ep_g if ep_g and math.isfinite(ep_g) and ep_g > 0 else None,
                'ic95': [est - tq * ep_g, est + tq * ep_g] if math.isfinite(tq) and math.isfinite(ep_g) else None,
                't_975': tq, 'emd_com_ep_realizado': FATOR_EMD * ep_g if math.isfinite(ep_g) else None})
    # robustez
    rob = {}
    cu = V['cmp']['so_urna']
    m2 = sel[cu['nivel'][sel] > 0]
    if len(m2):
        d2 = V['delta'][m2] - cu['media'][m2]; e2, g2 = ep_media_agrupado(d2, V['mun'][m2])
        rob['so_urna_na_comparacao'] = {'N': int(len(m2)), 'efeito': float(d2.mean()), 'ep': e2}
    m3 = sel[np.isfinite(c['pond'][sel])]
    if len(m3):
        d3 = V['delta'][m3] - c['pond'][m3]; e3, _ = ep_media_agrupado(d3, V['mun'][m3])
        rob['outras_ponderadas_por_votos'] = {'N': int(len(m3)), 'efeito': float(d3.mean()), 'ep': e3}
    w = V['V2'][sel]
    ew = float((w * d).sum() / w.sum())
    # erro agrupado da média ponderada
    _, gi = np.unique(mun, return_inverse=True); G2 = gi.max() + 1
    S = np.bincount(gi, weights=w * (d - ew))
    epw = float(math.sqrt(G2 / (G2 - 1) * (S ** 2).sum()) / w.sum()) if G2 > 1 else float('nan')
    rob['media_ponderada_pelos_votos_da_secao'] = {'N': int(len(sel)), 'efeito': ew, 'ep': epw}
    # viés esperado do placebo (média de d nas seções de urna da mesma faixa) e efeito descontado
    vies = float(np.mean([tab[(V['terr'][i], V['faixa'][i])]['media'] for i in sel]))
    rob['media_do_placebo_mesma_faixa'] = vies
    rob['efeito_menos_media_do_placebo'] = est - vies
    sp = sorteio_placebo(V, sel, tab, rng)
    if sp is not None:
        rob['placebo_sorteios'] = {'n': int(len(sp)), 'media': float(sp.mean()), 'dp': float(sp.std(ddof=1)),
                                   'p_unilateral_inferior': float((np.sum(sp <= est) + 1) / (len(sp) + 1)),
                                   'p_bilateral': float((np.sum(np.abs(sp - sp.mean()) >= abs(est - sp.mean())) + 1) / (len(sp) + 1))}
    out['robustez'] = rob
    out['secoes'] = [{'secao': V['keys'][i], 'nivel': ['nenhum', 'local', 'municipio'][int(c['nivel'][i])],
                      'n_outras': int(c['n_out'][i]), 'L1': int(V['L1'][i]), 'R1': int(V['R1'][i]),
                      'L2': int(V['L2'][i]), 'R2': int(V['R2'][i]), 'variacao': float(V['delta'][i]),
                      'media_outras': float(c['media'][i]), 'd': float(V['delta'][i] - c['media'][i]),
                      'outras_de_junta_na_comparacao': int(c['nJ_out'][i])} for i in sel]
    return out


def veredito(e):
    emd = e['emd_antes'].get('emd')
    sem_poder = emd is None or not math.isfinite(emd) or emd > EMD_MAX
    if e.get('efeito') is None:
        return 'SEM PODER', 'nenhuma seção de cédula com seção de comparação no local ou no município; EMD indefinido'
    est, z, N = e['efeito'], e.get('z'), e['N']
    if N >= N_MIN and est <= LIM_SINAL and z is not None and z <= Z_SINAL:
        return 'SINAL', f'N = {N} >= 30, efeito {est:.2f} <= -1,8 e z {z:.2f} <= -2,5'
    if -FAIXA_SEM_SINAL <= est <= FAIXA_SEM_SINAL and not sem_poder:
        return 'SEM SINAL', f'efeito {est:.2f} entre -0,7 e +0,7 e EMD {emd:.2f} <= 1,8'
    if sem_poder:
        return 'SEM PODER', f'EMD calculado antes {emd:.2f} > 1,8' if emd is not None else 'EMD indefinido'
    return 'INCONCLUSIVO', 'nem sinal nem sem sinal, com EMD até 1,8'


def descritivo_exterior(V, max_aptos=None):
    """Fora do registro: no exterior, variação da fatia de Lula nas seções de cédula contra a das seções de urna.
    max_aptos: se dado, só as seções de cédula com até esse número de aptos no 2º turno."""
    zz = V['terr'] == 'ZZ'
    J = V['isJ'] & zz
    if max_aptos is not None:
        J = J & (V['apt'] <= max_aptos)
    U = (~V['isJ']) & zz
    out = {'N_cedula': int(J.sum()), 'N_urna': int(U.sum()), 'max_aptos': max_aptos}
    if J.sum() < 2:
        return out
    dJ = V['delta'][J]; dU = V['delta'][U]
    eJ = float(dJ.std(ddof=1) / math.sqrt(len(dJ))); eU = float(dU.std(ddof=1) / math.sqrt(len(dU)))
    out.update({'media_variacao_cedula': float(dJ.mean()), 'ep_cedula': eJ,
                'media_variacao_urna': float(dU.mean()), 'ep_urna': eU,
                'dif': float(dJ.mean() - dU.mean()), 'ep_dif': math.sqrt(eJ ** 2 + eU ** 2)})
    out['emd_com_ep_realizado'] = FATOR_EMD * out['ep_dif']
    out['mediana_votos_finalistas_2T'] = {'cedula': float(np.median(V['V2'][J])), 'urna': float(np.median(V['V2'][U]))}
    out['urna_com_ate_100_votos'] = int((U & (V['V2'] <= 100)).sum())
    Us = U & (V['V2'] <= 100)
    if Us.sum() >= 2:
        dS = V['delta'][Us]
        out['urna_ate_100_votos_media_variacao'] = float(dS.mean()); out['urna_ate_100_votos_ep'] = float(dS.std(ddof=1) / math.sqrt(len(dS)))
        out['dif_vs_urna_ate_100_votos'] = float(dJ.mean() - dS.mean())
        out['ep_dif_vs_urna_ate_100_votos'] = math.sqrt(eJ ** 2 + out['urna_ate_100_votos_ep'] ** 2)
    sJ = lambda a: float(a[J].sum()); sU = lambda a: float(a[U].sum())
    out['fatia_somada_cedula'] = {'1T': 100 * sJ(V['L1']) / (sJ(V['L1']) + sJ(V['R1'])), '2T': 100 * sJ(V['L2']) / (sJ(V['L2']) + sJ(V['R2']))}
    out['fatia_somada_urna'] = {'1T': 100 * sU(V['L1']) / (sU(V['L1']) + sU(V['R1'])), '2T': 100 * sU(V['L2']) / (sU(V['L2']) + sU(V['R2']))}
    out['votos_finalistas_cedula'] = {'1T': int(sJ(V['L1']) + sJ(V['R1'])), '2T': int(sJ(V['L2']) + sJ(V['R2']))}
    out['cidades_cedula'] = sorted(set(V['mun'][J].tolist()))
    return out


# ---------------------------------------------------------------- principal

def main():
    zips2, zips1, base26, base22, saida_json, saida_txt = sys.argv[1:7]
    rng = np.random.default_rng(SEMENTE)
    res = {'teste': 'T31', 'registro': 'PRE-REGISTRO-2026-10-26.md, Adendo 9', 'rodado_em': time.strftime('%Y-%m-%dT%H:%M:%SZ', time.gmtime())}

    # 1) campos de junta no bweb do 2º turno de 2026 (28 arquivos) e do 1º turno (exterior e MG)
    z2 = sorted(glob.glob(os.path.join(zips2, 'bweb_2t_*.zip')))
    z1 = sorted(p for p in glob.glob(os.path.join(zips1, 'bweb_1t_*.zip')) if os.path.basename(p).split('_')[2] in ('ZZ', 'MG'))
    log(f'lendo {len(z2)} zips do 2º turno e {len(z1)} do 1º turno')
    bw2 = {}
    with Pool(3) as p:
        r1 = p.map_async(ler_zip_1t_marcas, z1)
        for nome, o in p.imap_unordered(ler_zip_2t, z2):
            bw2.update(o)
        r1 = r1.get()
    log(f'2º turno: {len(bw2)} seções')
    J26 = sorted(k for k, s in bw2.items() if any(c[0] not in ('-1', '', '#NULO#') for c in s['campos']))
    vaz26 = sorted(k for k, s in bw2.items() if any(c[1] == '' and c[2] == '' for c in s['campos']))
    mistura = sorted(k for k, s in bw2.items() if len(s['campos']) > 1)
    jun_uf = collections.Counter(k.split('|')[0] for k in J26)
    jun_det = []
    for k in J26:
        s = bw2[k]
        jun_det.append({'secao': k, 'cidade': s['nm'], 'junta': s['junta'], 'turma': s['turma'], 'urna': s['urna'],
                        'emissao_bu': s['emissao'], 'tipo': s['tipo'], 'aptos': s['apt'], 'comparecimento': s['comp'],
                        'sem_votos': s['sem_votos']})
    marca_1t = {}
    for nome, marc, nsec, nlin in r1:
        uf = nome.split('_')[2]
        j = sorted(k for k, v in marc.items() if any(c[0] not in ('-1', '', '#NULO#') for c in v))
        e = sorted(k for k, v in marc.items() if any(c[1] == '' and c[2] == '' for c in v))
        marca_1t[uf] = {'secoes_com_presidente': nsec, 'linhas': nlin, 'junta': j, 'sem_abertura_e_encerramento': e,
                        'coincidem': j == e, 'urnas_junta': sorted({c[3] for k in j for c in marc[k]})}
    res['identificacao'] = {
        '2026_2T_secoes_no_bweb': len(bw2), '2026_2T_junta': len(J26), '2026_2T_junta_por_UF': dict(jun_uf),
        '2026_2T_sem_abertura_e_encerramento': len(vaz26), '2026_2T_marca_coincide_com_junta': J26 == vaz26,
        '2026_2T_secoes_com_campos_diferentes_entre_linhas': len(mistura),
        '2026_2T_tipo_de_urna': dict(collections.Counter(s['tipo'] for s in bw2.values())),
        '2026_2T_junta_detalhe': jun_det,
        '2026_1T_exterior_e_MG': marca_1t,
    }
    log(f'junta 2T 2026: {len(J26)} {dict(jun_uf)}; marca coincide: {J26 == vaz26}; 1T: ' +
        str({u: (len(v["junta"]), len(v["sem_abertura_e_encerramento"]), v["coincidem"]) for u, v in marca_1t.items()}))
    del bw2; gc.collect()

    # 2) 2026: seções e variações
    rows26, J, marca2_26, marca1_26, _ = montar(base26, set(J26))
    j1 = set()
    for v in marca_1t.values():
        j1 |= set(v['junta'])
    res['identificacao']['2026_2T_junta_tambem_de_junta_no_1T'] = len(set(J26) & j1)
    res['identificacao']['2026_base_secoes_dois_turnos'] = len(rows26)
    res['identificacao']['2026_base_marca_2T'] = len(marca2_26)
    res['identificacao']['2026_base_marca_2T_contida_na_junta'] = marca2_26 <= set(J26)
    res['identificacao']['2026_base_marca_1T'] = sorted(marca1_26)
    V26 = variacoes(rows26, J); del rows26; gc.collect()
    log(f'2026: {len(V26["keys"])} seções com fatia nos dois turnos; cédula com fatia: {int(V26["isJ"].sum())}')

    # 3) 2022: seções e variações (marca)
    rows22, J22, marca2_22, marca1_22, apt22 = montar(base22, None)
    res['identificacao']['2022_marca_2T_exterior'] = sum(1 for k in marca2_22 if k.startswith('ZZ|'))
    res['identificacao']['2022_marca_2T_brasil'] = sum(1 for k in marca2_22 if not k.startswith('ZZ|'))
    res['identificacao']['2022_marca_2T_exterior_mais_de_300_aptos'] = sorted(k for k in marca2_22 if k.startswith('ZZ|') and apt22[k] > 300)
    res['identificacao']['2022_marca_2T_aptos'] = apt22
    res['identificacao']['2022_marca_2T'] = len(marca2_22)
    res['identificacao']['2022_marca_2T_por_UF'] = dict(collections.Counter(k.split('|')[0] for k in marca2_22))
    res['identificacao']['2022_marca_2T_lista'] = sorted(marca2_22)
    res['identificacao']['2022_marca_1T'] = len(marca1_22)
    res['identificacao']['2022_marca_nos_dois_turnos'] = len(marca2_22 & marca1_22)
    V22 = variacoes(rows22, J22); del rows22; gc.collect()
    log(f'2022: {len(V22["keys"])} seções com fatia nos dois turnos; cédula com fatia: {int(V22["isJ"].sum())}')

    # 4) seções de cédula utilizáveis (com fatia e comparação) e placebo; EMD antes, depois estimativa
    anos = {}
    for ano, V, Jset in (('2026', V26, J), ('2022', V22, J22)):
        c = V['cmp']['literal']
        selJ = np.nonzero(V['isJ'])[0]
        util = selJ[c['nivel'][selJ] > 0]
        sem_cmp = [V['keys'][i] for i in selJ if c['nivel'][i] == 0]
        sem_fatia = sorted(set(Jset) - set(V['keys'][i] for i in selJ))
        tab, _ = placebo_variancias(V, ~V['isJ'])
        a = {'cedula_total': len(Jset), 'cedula_com_fatia_nos_dois_turnos': int(len(selJ)),
             'cedula_sem_fatia_ou_sem_1T': sem_fatia, 'cedula_sem_secao_de_comparacao': sem_cmp,
             'cedula_utilizaveis': int(len(util)),
             'utilizaveis_por_nivel': dict(collections.Counter(['local', 'municipio'][int(c['nivel'][i]) - 1] for i in util)),
             'placebo': {f'{t}|{faixa_rot(f)}': {kk: vv for kk, vv in v.items() if kk != 'idx'} for (t, f), v in tab.items()}}
        a['emd_antes'] = emd_antes(V, util, tab)
        log(f'{ano}: cédula {len(Jset)}, com fatia {len(selJ)}, utilizáveis {len(util)}; EMD antes {a["emd_antes"]}')
        a['estimativa'] = estimar(V, util, tab, rng, ano)
        a['veredito_pela_letra'] = veredito(a['estimativa'])
        # subconjuntos (robustez)
        if ano == '2022':
            for nome_s, msk in (('so_exterior', V['terr'][util] == 'ZZ'), ('so_brasil', V['terr'][util] == 'BR')):
                e = estimar(V, util[msk], tab, rng, f'2022 {nome_s}')
                a[f'robustez_{nome_s}'] = {kk: vv for kk, vv in e.items() if kk != 'secoes'}
        a['descritivo_exterior_fora_do_registro'] = {'todas': descritivo_exterior(V), 'ate_300_aptos': descritivo_exterior(V, 300)}
        a['_util'] = util; a['_tab'] = tab
        anos[ano] = a
    # 2026 e 2022 juntos (robustez): concatena as seções de cédula utilizáveis dos dois anos
    jnt = {}
    partes = []
    for ano, V in (('2026', V26), ('2022', V22)):
        u = anos[ano]['_util']; c = V['cmp']['literal']
        for i in u:
            partes.append((V['delta'][i] - c['media'][i], f"{ano}|{V['mun'][i]}", anos[ano]['_tab'][(V['terr'][i], V['faixa'][i])]['var']))
    if partes:
        d = np.array([x[0] for x in partes]); g = np.array([x[1] for x in partes])
        e, G = ep_media_agrupado(d, g)
        jnt = {'N': len(partes), 'efeito': float(d.mean()), 'ep': e, 'municipios': G,
               'ep_antes': math.sqrt(sum(x[2] for x in partes)) / len(partes)}
        jnt['emd_antes'] = FATOR_EMD * jnt['ep_antes']
    res['2026_e_2022_juntos_robustez'] = jnt
    # diferença entre anos no descritivo do exterior
    dif_anos = {}
    for nome in ('todas', 'ate_300_aptos'):
        d26 = anos['2026']['descritivo_exterior_fora_do_registro'][nome]; d22 = anos['2022']['descritivo_exterior_fora_do_registro'][nome]
        if 'dif' in d26 and 'dif' in d22:
            dif_anos[nome] = {'dif': d26['dif'] - d22['dif'], 'ep': math.sqrt(d26['ep_dif'] ** 2 + d22['ep_dif'] ** 2),
                              'cidades_em_comum': len(set(d26['cidades_cedula']) & set(d22['cidades_cedula']))}
            dif_anos[nome]['z'] = dif_anos[nome]['dif'] / dif_anos[nome]['ep']
    res['descritivo_exterior_2026_menos_2022'] = dif_anos
    for a in anos.values():
        a.pop('_util'); a.pop('_tab')
    res['anos'] = anos
    res['veredito'] = anos['2026']['veredito_pela_letra'][0]
    res['motivo_veredito'] = anos['2026']['veredito_pela_letra'][1]

    def conv(o):
        if isinstance(o, dict): return {str(k): conv(v) for k, v in o.items()}
        if isinstance(o, (list, tuple)): return [conv(v) for v in o]
        if isinstance(o, (np.integer,)): return int(o)
        if isinstance(o, (np.floating,)): return None if not np.isfinite(o) else float(o)
        if isinstance(o, float) and not math.isfinite(o): return None
        if isinstance(o, set): return sorted(conv(v) for v in o)
        return o
    json.dump(conv(res), open(saida_json, 'w'), ensure_ascii=False, indent=1)
    escrever_txt(conv(res), saida_txt)
    log(f'veredito: {res["veredito"]} ({res["motivo_veredito"]})')


def n(x, nd=2):
    if x is None:
        return 'n/d'
    s = f'{x:,.{nd}f}'
    return s.replace(',', 'X').replace('.', ',').replace('X', '.')


def ni(x):
    return f'{int(x):,}'.replace(',', '.')


def s(x, nd=2):
    if x is None:
        return 'n/d'
    return ('+' if x >= 0 else '') + n(x, nd)


def escrever_txt(res, caminho):
    L = []; P = L.append
    idf = res['identificacao']; a26 = res['anos']['2026']; a22 = res['anos']['2022']
    P('T31. Seções votadas em cédula (Adendo 9), com o bweb completo do 2º turno de 2026')
    P('Script: scripts/analisar_T31.py. Números completos: resultados/T31_bweb.json.')
    P(f"Rodado em {res['rodado_em'][:10]} com o bweb do 2º turno (zips de 26/10, 07h42, hash conferido antes), a base por seção")
    P('dos dois turnos de 2026 (secoes2026.json.gz), os zips do 1º turno do exterior e de MG e a base de 2022 (secoes2022.json.gz).')
    P('')
    P('Critério registrado (PRE-REGISTRO-2026-10-26.md, Adendo 9, antes dos dados):')
    P('- Seções do 2º turno de 2026 e de 2022 apuradas pela junta por cédula. Para cada uma, variação da fatia de Lula menos a média')
    P('  das outras seções do local (ou município). Estimativa conjunta com intervalo e efeito mínimo detectável calculado antes.')
    P('- Sinal: efeito de -1,8 ponto ou menos a mais de 2,5 erros-padrão, com 30 seções ou mais. Sem sinal: entre -0,7 e +0,7 com')
    P('  efeito mínimo detectável até 1,8. Acima de 1,8, sem poder.')
    P('')
    P(f"VEREDITO PELA LETRA: {res['veredito']}")
    P(f"Motivo: {res['motivo_veredito']}.")
    P('')
    P('Resumo')
    P(f"- No 2º turno de 2026 nenhuma seção das 27 UFs teve boletim de junta: as {idf['2026_2T_junta']} seções apuradas por junta estão todas no")
    P(f"  exterior ({', '.join(f'{v} em {k}' for k, v in idf['2026_2T_junta_por_UF'].items())}). Delas, {a26['cedula_com_fatia_nos_dois_turnos']} têm voto nos dois finalistas nos dois turnos e")
    unica = len(a26['cedula_sem_secao_de_comparacao']) == a26['cedula_com_fatia_nos_dois_turnos']
    P(f"  {a26['cedula_utilizaveis']} têm outra seção no mesmo local ou na mesma cidade para comparar"
      + (": cada uma é a única seção da sua cidade." if unica else "."))
    P('  A comparação registrada não existe para nenhuma seção de cédula de 2026; não há efeito estimado e o efeito mínimo detectável')
    P('  é indefinido. O registro pede 30 seções ou mais para sinal e efeito mínimo detectável até 1,8 para sem sinal; nenhuma das')
    P('  duas pernas pode ser cumprida.')
    e22 = a22['estimativa']
    P(f"- Referência de 2022: {idf['2022_marca_2T']} seções do 2º turno com boletim de junta pela marca (sem abertura e sem encerramento),")
    P(f"  {a22['cedula_utilizaveis']} com comparação. Efeito {s(e22.get('efeito'))} ponto (ep {n(e22.get('ep'))}), efeito mínimo detectável calculado antes")
    P(f"  {n(a22['emd_antes'].get('emd'))}: pela mesma letra, 2022 daria {a22['veredito_pela_letra'][0]} (e com 14 seções, abaixo das 30 que o sinal pede).")
    d26 = a26['descritivo_exterior_fora_do_registro']['todas']; d22 = a22['descritivo_exterior_fora_do_registro']['todas']
    dd = res.get('descritivo_exterior_2026_menos_2022', {}).get('todas')
    if 'dif' in d26 and 'dif' in d22 and dd:
        P(f"- Fora do registro (descritivo, sem peso no veredito): no exterior, a variação da fatia de Lula nas {d26['N_cedula']} seções de cédula de 2026")
        P(f"  ficou {s(d26['dif'])} ponto em relação à das seções de urna do exterior (ep {n(d26['ep_dif'])}); em 2022, {s(d22['dif'])} (ep {n(d22['ep_dif'])}).")
        P(f"  Diferença entre os anos {s(dd['dif'])} (ep {n(dd['ep'])}, z {n(dd['z'])}). Contra as seções de urna do exterior com até 100 votos, a")
        P(f"  diferença de 2026 cai para {s(d26.get('dif_vs_urna_ate_100_votos'))} (ep {n(d26.get('ep_dif_vs_urna_ate_100_votos'))}). Comparação escolhida depois de ver que o")
        P(f"  registro não tinha comparação, entre comunidades diferentes, com efeito mínimo detectável de {n(d26['emd_com_ep_realizado'])} pontos (item 6).")
    P('')
    P('1. Identificação das seções de cédula')
    P(f"- 2026, 2º turno: campo NR_JUNTA_APURADORA do bweb, lido nos 28 arquivos ({ni(idf['2026_2T_secoes_no_bweb'])} seções com linha de presidente ou")
    P(f"  de seção sem voto). Seções com boletim de junta: {idf['2026_2T_junta']}, todas no exterior. Tipo de urna no bweb: {idf['2026_2T_tipo_de_urna']}")
    P('  (o bweb de 2026 não marca a cédula pelo tipo de urna). Todas as de junta são da junta 1, turma 1, e o boletim saiu de duas')
    urnas = collections.Counter(x['urna'] for x in idf['2026_2T_junta_detalhe'])
    P(f"  urnas da junta ({dict(urnas)}), com emissão entre {min(x['emissao_bu'] for x in idf['2026_2T_junta_detalhe'])} e {max(x['emissao_bu'] for x in idf['2026_2T_junta_detalhe'])}.")
    sv = [x['secao'] for x in idf['2026_2T_junta_detalhe'] if x['sem_votos'] or x['comparecimento'] == 0]
    P(f"  Com comparecimento zero: {len(sv)} ({', '.join(sv)}).")
    P(f"- A marca usada em 2022 (boletim sem hora de abertura e sem hora de encerramento) coincide com o campo de junta em 2026, seção a")
    P(f"  seção: 2º turno, {idf['2026_2T_sem_abertura_e_encerramento']} sem as duas horas contra {idf['2026_2T_junta']} de junta, coincidem: {'sim' if idf['2026_2T_marca_coincide_com_junta'] else 'não'}.")
    for uf, v in idf['2026_1T_exterior_e_MG'].items():
        P(f"  1º turno, {uf}: {len(v['junta'])} de junta e {len(v['sem_abertura_e_encerramento'])} sem as duas horas, coincidem: {'sim' if v['coincidem'] else 'não'}"
          f" ({ni(v['secoes_com_presidente'])} seções com presidente no arquivo; urnas da junta {', '.join(v['urnas_junta'])}).")
    m1 = idf['2026_base_marca_1T']; m1br = [k for k in m1 if not k.startswith('ZZ|')]
    P(f"  Na base de 2026, as seções sem as duas horas no 1º turno são {len(m1)}: {len(m1) - len(m1br)} do exterior e {', '.join(m1br)}.")
    P('  As de MG tiveram boletim de junta no 1º turno sem que houvesse votação em cédula no Brasil, segundo o TSE: boletim de junta no')
    P('  Brasil pode ser recuperação de dados de urna, não cédula.')
    P(f"- 2022, 2º turno, pela marca: {idf['2022_marca_2T']} seções ({idf['2022_marca_2T_por_UF']}); {idf['2022_marca_nos_dois_turnos']} delas também no 1º turno.")
    P('  O campo de junta não está na base de 2022, e o bweb de 2022 não está nos arquivos locais. Não há campo público nesses arquivos')
    gr = idf['2022_marca_2T_exterior_mais_de_300_aptos']
    P(f"  que separe a votação em cédula da recuperação de dados pela junta; as {idf['2022_marca_2T_brasil']} seções do Brasil e as {len(gr)} do exterior")
    P(f"  com mais de 300 aptos ({', '.join(gr)}) podem ser urna que falhou e foi apurada pela junta, não votação toda em cédula.")
    P(f"  As outras {idf['2022_marca_2T_exterior'] - len(gr)} do exterior são seções pequenas, como as de 2026.")
    P('')
    P('2. Quantas entram na estimativa')
    for ano, a in (('2026', a26), ('2022', a22)):
        P(f"- {ano}: {a['cedula_total']} seções de junta no 2º turno; {a['cedula_com_fatia_nos_dois_turnos']} com voto nos dois finalistas nos dois turnos;"
          f" {len(a['cedula_sem_secao_de_comparacao'])} sem nenhuma outra seção no local nem no município; utilizáveis: {a['cedula_utilizaveis']} {a['utilizaveis_por_nivel']}.")
        if a['cedula_sem_fatia_ou_sem_1T']:
            P(f"  Sem fatia nos dois turnos ou sem 1º turno: {', '.join(a['cedula_sem_fatia_ou_sem_1T'])}.")
    P('')
    P('3. Efeito mínimo detectável, calculado antes da estimativa')
    P('- Só com as seções de urna (placebo) e o tamanho das seções de cédula: variância de d (variação menos a média das outras do')
    P('  local ou município) nas seções de urna da mesma faixa de votos nos finalistas e do mesmo território; EMD = 2,8 erros-padrão.')
    for ano, a in (('2026', a26), ('2022', a22)):
        em = a['emd_antes']
        if em.get('emd') is None:
            P(f"- {ano}: {em.get('emd_texto', 'indefinido')}.")
        else:
            P(f"- {ano}: N = {em['N']}, erro-padrão antes {n(em['ep_antes'])}, EMD {n(em['emd'])} ponto.")
    pz = a26['placebo']
    fu = a22['emd_antes'].get('faixas_usadas', {})
    poucas = {k: v for k, v in fu.items() if v['secoes_de_urna_no_placebo'] < 30}
    if poucas:
        P(f"  O EMD de 2022 usa faixas com menos de 30 seções de urna no placebo: " +
          '; '.join(f"{k} ({v['secoes_de_cedula']} de cédula, {v['secoes_de_urna_no_placebo']} de urna)" for k, v in poucas.items()) +
          '. O número fica no limite de 1,8 e não é estável.')
    P('- Desvio-padrão de d nas seções de urna de 2026, por faixa de votos nos finalistas no 2º turno (para escala):')
    P('  exterior: ' + '; '.join(f"{k.split('|')[1]}: {n(v['dp'], 1)} (n {ni(v['n'])})" for k, v in pz.items() if k.startswith('ZZ|') and v['n'] >= 2))
    P('  Brasil: ' + '; '.join(f"{k.split('|')[1]}: {n(v['dp'], 1)} (n {ni(v['n'])})" for k, v in pz.items() if k.startswith('BR|') and v['n'] >= 2))
    dpb = pz.get('BR|26-50', {}).get('dp')
    if dpb:
        P(f"  No Brasil, uma seção de 26 a 50 votos tem desvio de d de {n(dpb, 1)} pontos; 30 seções de cédula desse tamanho (o das de 2026)")
        P(f"  dariam EMD de cerca de {n(FATOR_EMD * dpb / math.sqrt(30), 1)} pontos, acima de 1,8, mesmo que tivessem com o que comparar.")
    P('')
    P('4. Estimativa conjunta')
    for ano, a in (('2026', a26), ('2022', a22)):
        e = a['estimativa']
        if e.get('efeito') is None:
            P(f"- {ano}: sem estimativa (nenhuma seção utilizável).")
            continue
        ic = e.get('ic95') or [None, None]
        P(f"- {ano}: efeito {s(e['efeito'])} ponto, ep agrupado por município {n(e['ep'])} ({e['municipios']} municípios; sem agrupar {n(e['ep_sem_agrupar'])}),"
          f" z {n(e['z'])}, IC95 {s(ic[0])} a {s(ic[1])}; N = {e['N']}.")
        r = e.get('robustez', {})
        for nome, rot in (('so_urna_na_comparacao', 'comparação só com seções de urna'), ('outras_ponderadas_por_votos', 'outras ponderadas por votos'),
                          ('media_ponderada_pelos_votos_da_secao', 'média ponderada pelos votos da seção')):
            if nome in r:
                P(f"    robustez, {rot}: {s(r[nome]['efeito'])} (ep {n(r[nome]['ep'])}, N {r[nome]['N']})")
        if 'placebo_sorteios' in r:
            ps = r['placebo_sorteios']
            P(f"    placebo (20.000 sorteios de seções de urna da mesma faixa e território): média {s(ps['media'])}, dp {n(ps['dp'])};"
              f" p unilateral inferior {n(ps['p_unilateral_inferior'], 3)}, p bilateral {n(ps['p_bilateral'], 3)}")
            P(f"    média de d no placebo da mesma faixa {s(r['media_do_placebo_mesma_faixa'])}; efeito descontado {s(r['efeito_menos_media_do_placebo'])}")
        for nome in ('robustez_so_exterior', 'robustez_so_brasil'):
            if nome in a and a[nome].get('efeito') is not None:
                x = a[nome]
                P(f"    {nome.replace('robustez_', '').replace('_', ' ')}: {s(x['efeito'])} (ep {n(x['ep'])}, N {x['N']}, EMD antes {n(x['emd_antes'].get('emd'))})")
    j = res.get('2026_e_2022_juntos_robustez') or {}
    if j:
        P(f"- 2026 e 2022 juntos (robustez): N = {j['N']}, efeito {s(j['efeito'])} (ep {n(j['ep'])}), EMD antes {n(j['emd_antes'])}. Só as seções de 2022 entram.")
    if a22['estimativa'].get('secoes'):
        cj = [x['secao'] for x in a22['estimativa']['secoes'] if x['outras_de_junta_na_comparacao'] > 0]
        if cj:
            P(f"- Na leitura literal, {len(cj)} seções de 2022 têm outras seções de junta entre as de comparação ({', '.join(cj)});")
            P('  quando todas as outras do local são de junta, a seção é comparada só com cédula. A robustez "só com seções de urna" trata isso.')
        P('- Seções de 2022 na estimativa (variação da fatia de Lula; média das outras; d):')
        for x in a22['estimativa']['secoes']:
            P(f"    {x['secao']}: 1T {x['L1']}/{x['R1']}, 2T {x['L2']}/{x['R2']}; variação {s(x['variacao'])}; outras ({x['nivel']}, {x['n_outras']}, {x['outras_de_junta_na_comparacao']} de junta) {s(x['media_outras'])}; d {s(x['d'])}")
    P('')
    P('5. Leitura de cada perna do critério (2º turno de 2026)')
    e = a26['estimativa']
    P(f"- Sinal (efeito <= -1,8 a mais de 2,5 ep, com 30 seções ou mais): não pode ser cumprido; seções utilizáveis {e['N']}.")
    P(f"- Sem sinal (efeito entre -0,7 e +0,7 com EMD até 1,8): não pode ser cumprido; sem efeito estimado e EMD indefinido.")
    P(f"- Sem poder (EMD acima de 1,8): sim. Veredito: {res['veredito']}.")
    P('')
    P('6. Descritivo fora do registro (sem peso no veredito): exterior, cédula contra urna')
    P('- As seções de cédula do exterior são cidades pequenas com uma seção só. A comparação que sobra é com todas as seções de urna do')
    cid = sorted({x['cidade'] for x in idf['2026_2T_junta_detalhe']})
    P('  exterior. Não é o desenho registrado: compara cidades e países diferentes. As de cédula de 2026 são comunidades pequenas:')
    P('  ' + ', '.join(cid) + '.')
    P('  As de urna são as das comunidades com urna, em geral maiores (tamanho mediano abaixo). Comparação escolhida depois de ver que o')
    P('  registro não tinha comparação; a versão de 2022 só com seções de até 300 aptos sai ao lado porque as 4 grandes de 2022 podem não ser cédula.')
    for nome, rot in (('todas', 'todas as seções de junta'), ('ate_300_aptos', 'só as de junta com até 300 aptos')):
        P(f"- {rot}:")
        for ano, a in (('2026', a26), ('2022', a22)):
            dz = a['descritivo_exterior_fora_do_registro'][nome]
            if 'dif' not in dz:
                continue
            fc, fu = dz['fatia_somada_cedula'], dz['fatia_somada_urna']
            P(f"    {ano}: {dz['N_cedula']} de cédula ({ni(dz['votos_finalistas_cedula']['2T'])} votos nos finalistas no 2º turno; mediana {n(dz['mediana_votos_finalistas_2T']['cedula'], 0)}"
              f" por seção) e {ni(dz['N_urna'])} de urna (mediana {n(dz['mediana_votos_finalistas_2T']['urna'], 0)}; {dz['urna_com_ate_100_votos']} com até 100 votos).")
            P(f"      variação média por seção: cédula {s(dz['media_variacao_cedula'])} (ep {n(dz['ep_cedula'])}), urna {s(dz['media_variacao_urna'])} (ep {n(dz['ep_urna'])});"
              f" diferença {s(dz['dif'])} (ep {n(dz['ep_dif'])}; EMD com esse ep {n(dz['emd_com_ep_realizado'])})")
            P(f"      fatia somada de Lula: cédula 1T {n(fc['1T'], 1)}, 2T {n(fc['2T'], 1)} (variação {s(fc['2T'] - fc['1T'], 1)}); urna 1T {n(fu['1T'], 1)}, 2T {n(fu['2T'], 1)} (variação {s(fu['2T'] - fu['1T'], 1)})")
            if 'urna_ate_100_votos_media_variacao' in dz:
                P(f"      controle de tamanho: seções de urna do exterior com até 100 votos, variação média {s(dz['urna_ate_100_votos_media_variacao'])} (ep {n(dz['urna_ate_100_votos_ep'])}, {dz['urna_com_ate_100_votos']} seções);"
                  f" cédula menos essas {s(dz['dif_vs_urna_ate_100_votos'])} (ep {n(dz['ep_dif_vs_urna_ate_100_votos'])})")
        dd = res.get('descritivo_exterior_2026_menos_2022', {}).get(nome)
        if dd:
            P(f"    2026 menos 2022: {s(dd['dif'])} (ep {n(dd['ep'])}, z {n(dd['z'])}); cidades de cédula em comum entre os anos: {dd['cidades_em_comum']}.")
    d26 = a26['descritivo_exterior_fora_do_registro']['todas']; d22 = a22['descritivo_exterior_fora_do_registro']['todas']
    if 'dif' in d26 and 'dif' in d22:
        sent = lambda x: 'menor' if x < 0 else 'maior'
        P(f"- Leitura: em 2026 a variação da fatia de Lula nas seções de cédula do exterior foi {sent(d26['dif'])} que nas de urna do exterior"
          f" ({s(d26['dif'])}, z {n(d26['dif'] / d26['ep_dif'])}); em 2022, {sent(d22['dif'])} ({s(d22['dif'])}, z {n(d22['dif'] / d22['ep_dif'])}).")
        P('  Um ganho menor de Lula na cédula é o sentido que a tese preveria. Isso não é resultado do T31: a comparação foi escolhida')
        P(f"  depois, junta grupos de eleitores diferentes, as seções de cédula somam {ni(d26['votos_finalistas_cedula']['2T'])} votos nos finalistas em 2026,")
        P(f"  o efeito mínimo detectável desta leitura é de {n(d26['emd_com_ep_realizado'])} pontos em 2026 (acima de 1,8) e a diferença entre os anos")
        P('  só isola a urna se as comunidades pequenas e as grandes mudarem igual nos dois anos, o que nada garante (em 2022 os eliminados')
        P('  do 1º turno eram Ciro e Tebet; em 2026, Renan, Caiado, Zema e Cury).')
    P('')
    P('7. Escolhas de leitura e desvios do registro')
    P('- "Apuradas pela junta por cédula": em 2026, boletim com NR_JUNTA_APURADORA diferente de -1. O bweb não separa cédula de')
    P('  recuperação de dados pela junta; toda seção de junta entrou. Em 2026 todas são do exterior, onde a votação em cédula das')
    P('  seções pequenas estava prevista. Desvio de leitura.')
    P('- 2022: o campo de junta não está na base nem nos arquivos locais; marca usada: boletim do 2º turno sem hora de abertura e de')
    P('  encerramento, conferida contra o campo em 2026 (coincide seção a seção). Desvio de dado: a marca não é o campo do registro.')
    P('- "Variação da fatia de Lula": fatia entre os dois finalistas, 2º menos 1º turno, em pontos, como no T17.')
    P('- "Outras seções do local (ou município)": leitura literal, todas as outras (inclusive outras de junta), local primeiro, município')
    P('  se o local não tiver outra; seção sem nenhuma das duas fica fora. Média simples. Só com seções de urna sai como robustez.')
    P('- "Estimativa conjunta": média simples de d por ano, erro-padrão agrupado por município, IC95 com t. 2026 e 2022 juntos sai como')
    P('  robustez. O veredito é o do 2º turno de 2026; 2022 recebe a mesma leitura, como referência.')
    P('- "Efeito mínimo detectável calculado antes": 2,8 erros-padrão (convenção do T17), com o erro-padrão tirado das seções de urna da')
    P('  mesma faixa de votos e território, sem usar a variação das seções de cédula. Com zero seções utilizáveis, indefinido.')
    P('- Com zero seções utilizáveis em 2026, o veredito SEM PODER vem da perna "acima de 1,8, sem poder" lida com EMD indefinido.')
    P('  Não é SEM DADO: o dado existe (o bweb identifica as seções de junta); o que falta é seção de comparação no local ou na cidade.')
    P('- O descritivo do item 6 não estava registrado e não entra no veredito.')
    P('')
    P('8. Limites')
    P('- No Brasil, nenhuma seção votou em cédula no 2º turno de 2026, então o T31 não tem como servir de contraprova física da urna')
    dz = a26['descritivo_exterior_fora_do_registro']['todas']
    P(f"  no Brasil. As {dz.get('N_cedula', 0)} seções de cédula do exterior com fatia somam {dz.get('votos_finalistas_cedula', {}).get('2T', 0)} votos nos finalistas no 2º turno;")
    P(f"  {idf['2026_2T_junta_tambem_de_junta_no_1T']} das {idf['2026_2T_junta']} de junta do 2º turno também tiveram boletim de junta no 1º turno (campo do bweb do 1º turno).")
    P('- Uma troca feita pelo programa só no Brasil, ou só em urnas que votaram, não seria vista nestas seções de qualquer forma.')
    open(caminho, 'w').write('\n'.join(L) + '\n')


if __name__ == '__main__':
    main()
