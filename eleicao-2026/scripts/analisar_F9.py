"""F9 do Adendo 21: computador que gerou a mídia de resultado (MR) do 2º turno.

Registro (PRE-REGISTRO-2026-10-26.md, Adendo 21, commit 913af7a, 31/10/2026 10:36:29 UTC):
  - No 2º turno a urna fica com a carga do 1º e recebe uma mídia nova, gerada nos computadores das zonas. O log
    registra "MR gerada pelo computador", a data e o usuário. Uma mídia adulterada num computador apareceria nas
    urnas dele.
  - Para cada seção da amostra de logs: resíduo da virada de Lula (fatia entre os finalistas, 2º turno menos 1º)
    contra as outras seções do mesmo local no bweb, ponderado pelos votos dos finalistas. Média do resíduo por
    computador. Estatística: variância ponderada entre computadores; referência: 2.000 permutações dos computadores
    entre as seções da mesma UF.
  - Sinal: p da permutação abaixo de 0,001 e pelo menos um computador com 10 ou mais seções da amostra e resíduo médio
    de +2,0 pontos ou mais a favor de Lula a mais de 4 erros-padrão. Sem sinal: p acima de 0,05. Entre os dois:
    inconclusivo.
  - Descritivo: datas de geração da mídia fora da janela de 05 a 23/10, usuário e computador fora da zona da seção.

Decisões tomadas antes de calcular qualquer resíduo (o registro não fixa estes pontos; cada uma é declarada como
desvio). Antes de escrevê-las foram olhados só a estrutura do log e os identificadores (tipos de mensagem, formato
dos nomes dos computadores e dos usuários, datas), nunca a virada.
  D1. Amostra de logs: as seções de amostra2t/arq com pacote -log.jez (3.897; outras 6 pastas da amostra não têm
      log baixado e ficam fora, como nos Adendos 12 e 13). Lidos todos os logd.dat do pacote, inclusive os .jez
      aninhados (scripts/decodificar.py, _linhas_log).
  D2. Bloco de MR: no log, a sequência "Número de série da MR: X", "Aplicativo(s) presente(s) na MR [..]",
      "MR gerada pelo computador: N", "Data e hora da geração da MR: D", "MR gerada pelo usuário: U", na mesma urna e
      na ordem das linhas. MR do 2º turno = bloco com "Aplicativo presente na MR [VOTA]". Blocos de outras mídias
      ([SA,RED,VPP,ATUE], [VPP], [ADH], [RED]: apuração, recuperação e testes) não são a mídia do 2º turno e só
      entram no descritivo.
  D3. Computador da seção: o da MR [VOTA] lida imediatamente antes da linha "Urna transitada para 2º Turno" (a
      transição é o momento em que os dados do 2º turno passam da MR para a urna), no mesmo logd e na mesma urna. Se
      houver mais de uma transição, vale a última da urna do boletim do 2º turno (número da urna do bweb do 2º turno
      igual ao número da terceira coluna do log). Sem transição dessa urna: a última transição do pacote. Sem
      transição nenhuma: a última MR [VOTA] lida pela urna do boletim em 25/10/2026; depois, a última MR [VOTA] do
      pacote. A regra usada fica anotada por seção. O identificador do computador é o nome como aparece no log.
  D4. Virada: y = 100 x [L2/(L2+R2) - L1/(L1+R1)], do bweb (trab2t/secoes2026.json.gz), para toda seção com os dois
      turnos e votos dos finalistas positivos nos dois. Local = UF|município|zona|local de votação do 2º turno.
  D5. Resíduo da seção s: r = y_s - média de y nas outras seções válidas do mesmo local no bweb (todas, inclusive as
      outras seções da amostra), ponderada por L2+R2. Seção sem outra seção válida no local sai (contagem relatada).
  D6. Peso da seção: w = L2+R2 (votos dos finalistas no 2º turno). Média do computador c: soma de w r sobre soma de
      w nas seções da amostra com esse computador (D3) e resíduo definido.
  D7. Estatística: V = soma_c W_c (média_c - média geral)^2 / soma_c W_c, com W_c = soma dos pesos das seções do
      computador e média geral ponderada de todas as seções que entram. Entram todos os computadores, inclusive os de
      uma seção só.
  D8. Referência: 2.000 permutações; em cada uma, os rótulos de computador são embaralhados entre as seções da
      amostra da mesma UF (a contagem de seções de cada computador fica fixa). Semente 20261031.
      p = (1 + número de permutações com V >= V observado) / (1 + 2.000).
  D9. Erro-padrão da média de um computador: agrupado por local de votação, EP^2 = G/(G-1) soma_g (soma_{s em g}
      w_s (r_s - média_c))^2 / W_c^2, com G = número de locais do computador na amostra. Com G = 1, cada seção vira
      um grupo (fator n/(n-1)) e o caso é marcado. Com uma seção só, sem erro-padrão.
  D10. Critério de computador: 10 ou mais seções que entram na estatística (D5), média >= +2,0 pontos e média/EP > 4.
      Sinal: p < 0,001 e pelo menos um computador que cumpre o critério. Sem sinal: p > 0,05 (pela letra, qualquer
      que seja o resto). Entre os dois: INCONCLUSIVO (inclusive p < 0,001 sem computador que cumpra o critério).
  D11. Descritivo do registro:
      (a) Datas fora da janela: data de geração da MR do 2º turno da seção (D3) fora de 05/10/2026 a 23/10/2026,
          inclusive as pontas. Contadas também as outras MR [VOTA] lidas no pacote (rejeitadas ou trocadas).
      (b) Computador fora da zona: nome no padrão Z<UF><zona de 3 dígitos>... ou C<UF><zona de 3 dígitos>...: fora da
          zona quando a UF ou a zona do nome difere da seção. Nomes que começam com R (máquinas do TRE, sem zona no
          nome) são contados à parte como "sem zona no nome"; outros padrões, como "padrão desconhecido".
      (c) Usuário fora da zona: o usuário é o número de 12 dígitos do log. A zona do usuário é a zona mais comum
          entre as seções da amostra em que ele aparece como gerador da MR do 2º turno (empate: a menor). A seção
          fica "com usuário fora da zona" quando a sua zona difere dessa. Relatados também os usuários que aparecem em
          duas ou mais zonas e, como leitura do número, a UF do título de eleitor (dígitos 9 e 10, conferidos pelos
          dígitos verificadores do título: módulo 11, resto 10 vira 0).
  Leituras complementares, fora do veredito (decididas antes de rodar):
  C1. Identificação: o resíduo contra o próprio local só enxerga diferença entre computadores dentro do local. Conta-se
      quantas seções estão em locais com dois ou mais computadores na amostra, e V é refeito só nelas, com a mesma
      permutação dentro da UF e com permutação dentro do local.
  C2. Poder: para cada computador com 10 ou mais seções, soma-se +2, +5 e +10 pontos à virada de todas as seções da
      amostra com esse computador (as do mesmo local entram na comparação já somadas; as fora da amostra ficam como
      estão), refazendo resíduo, média, EP e, para +2 e +5, o p de V com as mesmas 2.000 permutações. Relata-se a
      fração do deslocamento que sobrevive ao resíduo (atenuação) e quantos computadores cumpririam o critério.
  C3. Erro-padrão alternativo: desvio-padrão da média do computador nas 2.000 permutações.
  C4. Média do resíduo nos grupos do descritivo (datas fora da janela, computador fora da zona, computador sem zona
      no nome, usuário fora da zona).
  C5. Conferências: (i) a data da MR escolhida contra a extração independente do T10 (amostra2t/T10_software.json,
      835 seções); (ii) MR presente no dia da eleição igual à da transição; (iii) MR lida antes da data de geração;
      (iv) mesmo número de série de MR em mais de uma seção; (v) erros e alertas ligados à MR.

Correções e acréscimos feitos depois da primeira execução (31/10/2026; nenhum toca a estatística, o p ou o veredito):
  P1. Dígito verificador do título (D11c): a primeira versão aplicou só "resto 10 vira 0" e deu 441 de 466 usuários
      válidos; a regra do título manda também, para SP e MG, "resto 0 vira 1". Corrigida, os 466 são válidos. A
      contagem de seções com UF do título diferente da UF da seção passou a usar todos os usuários válidos.
  P2. C2: o p de V passou a ser calculado também com +10 pontos, para medir até onde vai a falta de poder.
  P3. Texto: acrescentados os casos de mesmo número de série em duas seções, as seções com duas ou mais MR [VOTA] e
      a observação sobre o erro-padrão agrupado quase nulo quando o computador cobre locais inteiros.

Uso: python3 -I analisar_F9.py <secoes2026.json.gz> <pasta_arq_amostra_2t> <T10_software.json> <saida.json> <saida.txt>
"""
import os as _os, sys as _sys
_sys.path.insert(0, _os.path.dirname(_os.path.abspath(__file__)))
import collections, datetime as dt, json, os, re, sys
from multiprocessing import Pool
import numpy as np
from lib import carregar
from decodificar import _linhas_log

SEMENTE = 20261031
NPERM = 2000
JAN_INI, JAN_FIM = dt.date(2026, 10, 5), dt.date(2026, 10, 23)
DIA_ELEICAO = '25/10/2026'
UF_TITULO = {'01': 'SP', '02': 'MG', '03': 'RJ', '04': 'RS', '05': 'BA', '06': 'PR', '07': 'CE', '08': 'PE', '09': 'SC',
             '10': 'GO', '11': 'MA', '12': 'PB', '13': 'PA', '14': 'ES', '15': 'PI', '16': 'RN', '17': 'AL', '18': 'MT',
             '19': 'MS', '20': 'DF', '21': 'SE', '22': 'AM', '23': 'RO', '24': 'AC', '25': 'AP', '26': 'RR', '27': 'TO',
             '28': 'ZZ'}
RX_TS = re.compile(r'^(\d\d)/(\d\d)/(\d{4}) (\d\d):(\d\d):(\d\d)$')
RX_DMR = re.compile(r'(\d\d)/(\d\d)/(\d{4}) às (\d\d):(\d\d):(\d\d)')
RX_ZONA_NOME = re.compile(r'^([ZC])([A-Z]{2})(\d{3})')
RX_ERRO_MR = re.compile(r'(m[íi]dia de resultado|\bMR\b|turno2)', re.I)
RX_RUIM = re.compile(r'(rro|nválid|alha|ausente|não estava presente)', re.I)


def ts(s):
    m = RX_TS.match(s)
    if not m:
        return None
    d, mo, a, h, mi, se = map(int, m.groups())
    try:
        return dt.datetime(a, mo, d, h, mi, se)
    except ValueError:
        return None


def ts_mr(s):
    m = RX_DMR.search(s or '')
    if not m:
        return None
    d, mo, a, h, mi, se = map(int, m.groups())
    try:
        return dt.datetime(a, mo, d, h, mi, se)
    except ValueError:
        return None


# ---------------------------------------------------------------- leitura dos logs
def ler_pacote(caminho):
    """Eventos ligados à MR, carga e mídia de votação, por logd do pacote, na ordem das linhas."""
    try:
        blocos = _linhas_log(caminho)
    except Exception as e:
        return {'erro': repr(e)}
    ev = []; outros = collections.Counter(); carga = set(); mv = set()
    for bi, b in enumerate(blocos):
        cur = None
        for li, l in enumerate(b):
            p = l.split('\t')
            if len(p) < 5:
                continue
            t, nivel, urna, app, msg = p[0], p[1], p[2].strip(), p[3], p[4]
            if msg.startswith('Número de série da MR'):
                cur = {'tipo': 'MR', 'ts': t, 'urna': urna, 'app': app, 'bloco': bi, 'linha': li,
                       'serie': msg.split(':', 1)[1].strip()}
                ev.append(cur); continue
            if cur is not None and urna == cur['urna']:
                if msg.startswith('Aplicativo presente na MR') or msg.startswith('Aplicativos presentes na MR'):
                    cur['apps'] = msg[msg.find('['):].strip(); continue
                if msg.startswith('MR gerada pelo computador'):
                    cur['comp'] = msg.split(':', 1)[1].strip(); continue
                if msg.startswith('Data e hora da geração da MR'):
                    cur['data'] = msg.split(':', 1)[1].strip(); continue
                if msg.startswith('MR gerada pelo usuário'):
                    cur['user'] = msg.split(':', 1)[1].strip(); cur = None; continue
            if msg.startswith('Urna transitada para 2'):
                ev.append({'tipo': 'TRANS', 'ts': t, 'urna': urna, 'bloco': bi, 'linha': li}); continue
            if msg.startswith('Mídia de carga gerada pelo computador'):
                carga.add(msg.split(':', 1)[1].split(' - ')[0].strip()); continue
            if msg.startswith('Mídia de votação gerada pelo computador'):
                mv.add(msg.split(':', 1)[1].split(' - ')[0].strip()); continue
            if RX_ERRO_MR.search(msg) and (nivel in ('ERRO', 'ALERTA', 'WHAT') or RX_RUIM.search(msg)):
                if msg.startswith('Problema ao desmontar a MR'):
                    outros['Problema ao desmontar a MR'] += 1
                else:
                    ev.append({'tipo': 'ERRO', 'ts': t, 'urna': urna, 'app': app, 'bloco': bi, 'linha': li,
                               'nivel': nivel, 'msg': msg[:300]})
    return {'ev': ev, 'outros': dict(outros), 'carga': sorted(carga), 'mv': sorted(mv), 'blocos': len(blocos)}


def secoes_amostra(pasta):
    out = []
    for uf in sorted(os.listdir(pasta)):
        for m in sorted(os.listdir(os.path.join(pasta, uf))):
            for z in sorted(os.listdir(os.path.join(pasta, uf, m))):
                for sc in sorted(os.listdir(os.path.join(pasta, uf, m, z))):
                    p = os.path.join(pasta, uf, m, z, sc)
                    if not os.path.isdir(p):
                        continue
                    logs = sorted(f for f in os.listdir(p) if f.endswith('-log.jez'))
                    out.append((f'{uf.upper()}|{int(m)}|{int(z)}|{int(sc)}', [os.path.join(p, f) for f in logs]))
    return out


def _trabalho(item):
    k, arqs = item
    return k, [ler_pacote(a) for a in arqs]


def escolher_mr(pac, urna_bu):
    """Regra D3. Devolve (bloco da MR escolhida, regra, lista de MR [VOTA], transições, MR presente em 25/10)."""
    ev = []
    for pi, p in enumerate(pac):
        for e in p.get('ev', []):
            e = dict(e); e['pac'] = pi; ev.append(e)
    mrs = [e for e in ev if e['tipo'] == 'MR' and e.get('apps') == '[VOTA]']
    trans = [e for e in ev if e['tipo'] == 'TRANS']

    def antes(t):
        c = [m for m in mrs if m['pac'] == t['pac'] and m['bloco'] == t['bloco'] and m['urna'] == t['urna']
             and m['linha'] < t['linha']]
        return c[-1] if c else None

    def chave(e):
        return (ts(e['ts']) or dt.datetime.min, e['pac'], e['bloco'], e['linha'])

    nbu = lambda u: u.isdigit() and int(u) == urna_bu
    escolhida = None; regra = None
    tb = sorted([t for t in trans if nbu(t['urna'])], key=chave)
    if tb and antes(tb[-1]):
        escolhida, regra = antes(tb[-1]), 'transicao_da_urna_do_boletim'
    elif trans and antes(sorted(trans, key=chave)[-1]):
        escolhida, regra = antes(sorted(trans, key=chave)[-1]), 'transicao_de_outra_urna'
    else:
        d25 = sorted([m for m in mrs if m['ts'].startswith(DIA_ELEICAO) and nbu(m['urna'])], key=chave)
        if d25:
            escolhida, regra = d25[-1], 'lida_em_25_10_pela_urna_do_boletim'
        elif mrs:
            escolhida, regra = sorted(mrs, key=chave)[-1], 'ultima_mr_do_pacote'
    d25 = sorted([m for m in mrs if m['ts'].startswith(DIA_ELEICAO)], key=chave)
    return escolhida, regra, mrs, trans, (d25[-1] if d25 else None), ev


# ---------------------------------------------------------------- estatística
def V_de(lab, w, r, K):
    W = np.bincount(lab, weights=w, minlength=K); R = np.bincount(lab, weights=w * r, minlength=K)
    ok = W > 0
    sw = w.sum(); m = (w * r).sum() / sw
    return float((np.sum(R[ok] ** 2 / W[ok]) - sw * m * m) / sw)


def V_perm(P, w, r, K):
    """V para cada linha da matriz de permutações P (rótulos já permutados)."""
    B, n = P.shape
    flat = (P + K * np.arange(B)[:, None]).ravel()
    W = np.bincount(flat, weights=np.tile(w, B), minlength=B * K).reshape(B, K)
    R = np.bincount(flat, weights=np.tile(w * r, B), minlength=B * K).reshape(B, K)
    sw = w.sum(); m = (w * r).sum() / sw
    with np.errstate(divide='ignore', invalid='ignore'):
        Q = np.where(W > 0, R ** 2 / np.where(W > 0, W, 1), 0.0)
    return (Q.sum(axis=1) - sw * m * m) / sw, R, W


def media_ep(idx, w, r, loc):
    """Média ponderada e EP agrupado por local (D9)."""
    ww = w[idx]; rr = r[idx]; W = ww.sum(); m = float((ww * rr).sum() / W); n = len(idx)
    if n < 2:
        return m, None, 'sem_ep', 1
    g = collections.defaultdict(float)
    for i, wi, ri in zip(idx, ww, rr):
        g[loc[i]] += wi * (ri - m)
    G = len(g)
    if G >= 2:
        return m, float(np.sqrt(G / (G - 1) * sum(v * v for v in g.values())) / W), 'agrupado_por_local', G
    e = ww * (rr - m)
    return m, float(np.sqrt(n / (n - 1) * np.sum(e * e)) / W), 'por_secao_um_local_so', 1


def fmt(x, d=3):
    if x is None:
        return 'n/d'
    if isinstance(x, (int, np.integer)):
        return f'{int(x):,}'.replace(',', '.')
    s = f'{x:,.{d}f}'
    return s.replace(',', '_').replace('.', ',').replace('_', '.')


def main():
    arq_bweb, pasta, arq_t10, saida_json, saida_txt = sys.argv[1:6]
    rng = np.random.default_rng(SEMENTE)

    # 1. logs
    itens = secoes_amostra(pasta)
    with Pool(4) as pool:
        pac = dict(pool.map(_trabalho, itens, chunksize=20))
    sem_log = sorted(k for k, a in pac.items() if not a)
    ilegiveis = sorted(k for k, a in pac.items() if any('erro' in p for p in a))

    # 2. bweb
    bw = carregar(arq_bweb)
    y = {}; wsec = {}; loc_de = {}
    soma_W = collections.defaultdict(float); soma_S = collections.defaultdict(float)
    for k, s in bw.items():
        a, b = s.get('1'), s.get('2')
        if not a or not b:
            continue
        uf, mun, z, _ = k.split('|')
        loc_de[k] = f'{uf}|{mun}|{z}|{b["loc"]}'
        n1, n2 = a['L'] + a['R'], b['L'] + b['R']
        if n1 <= 0 or n2 <= 0:
            continue
        y[k] = 100 * (b['L'] / n2 - a['L'] / n1); wsec[k] = float(n2)
        soma_W[loc_de[k]] += n2; soma_S[loc_de[k]] += n2 * y[k]

    # 3. MR por seção
    secs = {}
    regras = collections.Counter(); sem_mr = []
    for k, a in sorted(pac.items()):
        if not a:
            continue
        urna_bu = bw.get(k, {}).get('2', {}).get('urna')
        esc, regra, mrs, trans, mr25, ev = escolher_mr(a, urna_bu)
        if esc is None:
            sem_mr.append(k); continue
        regras[regra] += 1
        uf, mun, z, sc = k.split('|')
        secs[k] = {'uf': uf, 'zona': int(z), 'comp': esc.get('comp'), 'data': esc.get('data'), 'user': esc.get('user'),
                   'serie': esc.get('serie'), 'lida_em': esc['ts'], 'urna_log': esc['urna'], 'regra': regra,
                   'urna_bu': urna_bu, 'transicoes': len(trans),
                   'comps_vota': sorted({m.get('comp') for m in mrs if m.get('comp')}),
                   'series_vota': sorted({m.get('serie') for m in mrs}),
                   'datas_vota': sorted({m.get('data') for m in mrs if m.get('data')}),
                   'serie_25_10': mr25['serie'] if mr25 else None,
                   'outras_mr': sorted({(m.get('apps'), m.get('comp'), m.get('data'), m.get('user'))
                                        for m in ev if m['tipo'] == 'MR' and m.get('apps') != '[VOTA]'},
                                       key=lambda t: tuple(str(x) for x in t)),
                   'erros': [(e['ts'], e['app'], e['nivel'], e['msg']) for e in ev if e['tipo'] == 'ERRO'],
                   'desmontar': sum(p.get('outros', {}).get('Problema ao desmontar a MR', 0) for p in a),
                   'carga': sorted({c for p in a for c in p.get('carga', [])}),
                   'mv': sorted({c for p in a for c in p.get('mv', [])})}

    # 4. resíduo
    fora_resid = collections.Counter(); ks = []
    for k, s in secs.items():
        if k not in loc_de:
            fora_resid['sem_os_dois_turnos_no_bweb'] += 1; continue
        if k not in y:
            fora_resid['finalistas_zerados_em_um_turno'] += 1; continue
        L = loc_de[k]; Wo = soma_W[L] - wsec[k]
        if Wo <= 0:
            fora_resid['sem_outra_secao_valida_no_local'] += 1; continue
        m_o = (soma_S[L] - wsec[k] * y[k]) / Wo
        s['y'] = y[k]; s['w'] = wsec[k]; s['m_outras'] = m_o; s['r'] = y[k] - m_o; s['local'] = L
        s['n_local_bweb'] = None
        ks.append(k)
    ks.sort()
    n = len(ks)
    comps = sorted({secs[k]['comp'] for k in ks})
    cid = {c: i for i, c in enumerate(comps)}; K = len(comps)
    ufs = sorted({secs[k]['uf'] for k in ks}); uid = {u: i for i, u in enumerate(ufs)}
    lab = np.array([cid[secs[k]['comp']] for k in ks]); uu = np.array([uid[secs[k]['uf']] for k in ks])
    w = np.array([secs[k]['w'] for k in ks]); r = np.array([secs[k]['r'] for k in ks])
    locs = [secs[k]['local'] for k in ks]
    yv = np.array([secs[k]['y'] for k in ks])

    # 5. permutações dentro da UF
    P = np.empty((NPERM, n), dtype=np.int32)
    grupos_uf = [np.where(uu == i)[0] for i in range(len(ufs))]
    for b in range(NPERM):
        lb = lab.copy()
        for g in grupos_uf:
            lb[g] = lab[g][rng.permutation(len(g))]
        P[b] = lb
    V_obs = V_de(lab, w, r, K)
    Vp, Rp, Wp = V_perm(P, w, r, K)
    p = (1 + int(np.sum(Vp >= V_obs))) / (1 + NPERM)

    # 6. por computador
    por_c = {}
    with np.errstate(divide='ignore', invalid='ignore'):
        Mp = np.where(Wp > 0, Rp / np.where(Wp > 0, Wp, 1), np.nan)
    for c in comps:
        idx = np.where(lab == cid[c])[0]
        m, ep, tipo, G = media_ep(idx, w, r, locs)
        sdp = float(np.nanstd(Mp[:, cid[c]])); mp = float(np.nanmean(Mp[:, cid[c]]))
        ufc = sorted({secs[ks[i]]['uf'] for i in idx})
        zn = RX_ZONA_NOME.match(c or '')
        por_c[c] = {'n': int(len(idx)), 'W': float(w[idx].sum()), 'media': m, 'ep': ep, 'tipo_ep': tipo, 'locais': G,
                    'z': (m / ep if ep else None), 'ep_permutacao': sdp, 'media_permutacao': mp,
                    'z_permutacao': ((m - mp) / sdp if sdp > 0 else None), 'ufs': ufc,
                    'zonas_das_secoes': sorted({secs[ks[i]]['zona'] for i in idx}),
                    'zona_no_nome': (int(zn.group(3)) if zn else None)}
    crit = lambda d: d['n'] >= 10 and d['media'] >= 2.0 and d['ep'] is not None and d['ep'] > 0 and d['media'] / d['ep'] > 4
    cumprem = sorted([c for c, d in por_c.items() if crit(d)], key=lambda c: -por_c[c]['media'])
    cumprem_perm = sorted([c for c, d in por_c.items() if d['n'] >= 10 and d['media'] >= 2.0 and d['z_permutacao']
                           and d['z_permutacao'] > 4])
    if p < 0.001 and cumprem:
        veredito = 'SINAL'
    elif p > 0.05:
        veredito = 'SEM SINAL'
    else:
        veredito = 'INCONCLUSIVO'

    # 7. C1: identificação dentro do local
    comps_loc = collections.defaultdict(set)
    for i, k in enumerate(ks):
        comps_loc[locs[i]].add(secs[k]['comp'])
    mix = np.array([len(comps_loc[locs[i]]) >= 2 for i in range(n)])
    loc_amostra = collections.Counter(locs)
    c1 = {'locais_na_estatistica': len(loc_amostra),
          'locais_com_2_ou_mais_secoes': sum(1 for v in loc_amostra.values() if v >= 2),
          'locais_com_2_ou_mais_computadores': sum(1 for L, v in comps_loc.items() if len(v) >= 2),
          'secoes_em_locais_com_2_ou_mais_computadores': int(mix.sum()),
          'peso_em_locais_com_2_ou_mais_computadores_pct': float(100 * w[mix].sum() / w.sum())}
    if mix.sum() >= 2:
        im = np.where(mix)[0]
        lab_m = lab[im]; w_m = w[im]; r_m = r[im]
        Vm = V_de(lab_m, w_m, r_m, K)
        Pm_uf = np.empty((NPERM, len(im)), dtype=np.int32); Pm_loc = np.empty((NPERM, len(im)), dtype=np.int32)
        rng2 = np.random.default_rng(SEMENTE + 1)
        gu = [np.where(uu[im] == i)[0] for i in range(len(ufs))]
        lm = [locs[i] for i in im]; gl = collections.defaultdict(list)
        for j, L in enumerate(lm):
            gl[L].append(j)
        gl = [np.array(v) for v in gl.values()]
        for b in range(NPERM):
            a1 = lab_m.copy(); a2 = lab_m.copy()
            for g in gu:
                if len(g): a1[g] = lab_m[g][rng2.permutation(len(g))]
            for g in gl:
                a2[g] = lab_m[g][rng2.permutation(len(g))]
            Pm_uf[b] = a1; Pm_loc[b] = a2
        v1, _, _ = V_perm(Pm_uf, w_m, r_m, K); v2, _, _ = V_perm(Pm_loc, w_m, r_m, K)
        c1.update({'V': Vm, 'p_permutacao_na_uf': (1 + int(np.sum(v1 >= Vm))) / (1 + NPERM),
                   'p_permutacao_no_local': (1 + int(np.sum(v2 >= Vm))) / (1 + NPERM)})
        pc_m = {}
        for c in sorted(set(lab_m.tolist())):
            idx = im[lab_m == c]
            m, ep, tipo, G = media_ep(idx, w, r, locs)
            pc_m[comps[c]] = {'n': int(len(idx)), 'media': m, 'ep': ep, 'tipo_ep': tipo, 'locais': G}
        c1['computadores_nas_secoes_mistas_com_10_ou_mais'] = {c: d for c, d in sorted(pc_m.items(), key=lambda t: -t[1]['n'])
                                                            if d['n'] >= 10}

    # 8. C2: poder
    loc_arr = np.array([loc_de[k] for k in ks])
    Wloc = np.array([soma_W[L] for L in loc_arr]); Sloc = np.array([soma_S[L] for L in loc_arr])

    def residuo_com(delta, c):
        sel = (lab == cid[c])
        y2 = yv + delta * sel
        add = collections.defaultdict(float)
        for i in np.where(sel)[0]:
            add[loc_arr[i]] += delta * w[i]
        S2 = Sloc + np.array([add.get(L, 0.0) for L in loc_arr])
        return y2 - (S2 - w * y2) / (Wloc - w)

    poder = {}
    grandes = [c for c, d in por_c.items() if d['n'] >= 10]
    for c in grandes:
        idx = np.where(lab == cid[c])[0]
        out = {}
        for delta in (2.0, 5.0, 10.0):
            r2 = residuo_com(delta, c)
            m, ep, tipo, G = media_ep(idx, w, r2, locs)
            o = {'media': m, 'ep': ep, 'atenuacao': (m - por_c[c]['media']) / delta,
                 'cumpre_criterio_do_computador': bool(m >= 2.0 and ep and m / ep > 4)}
            if delta in (2.0, 5.0, 10.0):
                V2 = V_de(lab, w, r2, K); Vp2, _, _ = V_perm(P, w, r2, K)
                o['p'] = (1 + int(np.sum(Vp2 >= V2))) / (1 + NPERM)
                o['sinal_completo'] = bool(o['p'] < 0.001 and o['cumpre_criterio_do_computador'])
            out[str(int(delta))] = o
        poder[c] = out
    at = np.array([poder[c]['2']['atenuacao'] for c in grandes]) if grandes else np.array([])
    resumo_poder = {
        'computadores_com_10_ou_mais': len(grandes),
        'atenuacao_percentis': ({str(q): float(np.percentile(at, q)) for q in (10, 25, 50, 75, 90)} if len(at) else None),
        'atenuacao_abaixo_de_0_1': int(np.sum(at < 0.1)) if len(at) else 0,
        'cumpririam_criterio_do_computador': {d: sum(1 for c in grandes if poder[c][d]['cumpre_criterio_do_computador'])
                                              for d in ('2', '5', '10')},
        'dariam_sinal_completo': {d: sum(1 for c in grandes if poder[c][d]['sinal_completo']) for d in ('2', '5', '10')},
        'menor_p_com_deslocamento': {d: (min(poder[c][d]['p'] for c in grandes) if grandes else None) for d in ('2', '5', '10')},
        'computadores_com_p_abaixo_de_0_05': {d: sum(1 for c in grandes if poder[c][d]['p'] < 0.05) for d in ('2', '5', '10')},
    }

    # 9. Descritivo do registro
    def data_mr(s):
        t = ts_mr(s)
        return t.date() if t else None
    fora_jan = [k for k, s in secs.items() if (data_mr(s['data']) is None or not (JAN_INI <= data_mr(s['data']) <= JAN_FIM))]
    fora_jan_outras = sorted({(k, d) for k, s in secs.items() for d in s['datas_vota']
                              if d != s['data'] and (data_mr(d) is None or not (JAN_INI <= data_mr(d) <= JAN_FIM))})
    dist_datas = collections.Counter(str(data_mr(s['data'])) for s in secs.values())
    cls_comp = collections.Counter(); comp_fora = []
    for k, s in secs.items():
        c = s['comp'] or ''
        mz = RX_ZONA_NOME.match(c)
        if mz:
            if mz.group(2) != s['uf'] or int(mz.group(3)) != s['zona']:
                cls_comp['fora_da_zona'] += 1; comp_fora.append(k); s['comp_classe'] = 'fora_da_zona'
            else:
                cls_comp['na_zona'] += 1; s['comp_classe'] = 'na_zona'
        elif re.match(r'^R[A-Z]{2}', c):
            cls_comp['sem_zona_no_nome_R'] += 1; s['comp_classe'] = 'sem_zona_no_nome'
        else:
            cls_comp['padrao_desconhecido'] += 1; s['comp_classe'] = 'padrao_desconhecido'
    comp_fora_uf = [k for k, s in secs.items() if s['comp'] and s['comp'][1:3] != s['uf']]
    fora_por_comp = collections.Counter(secs[k]['comp'] for k in comp_fora)
    zonas_user = collections.defaultdict(collections.Counter)
    for k, s in secs.items():
        zonas_user[s['user']][s['zona']] += 1
    zona_user = {u: sorted(c.items(), key=lambda t: (-t[1], t[0]))[0][0] for u, c in zonas_user.items()}
    user_fora = [k for k, s in secs.items() if s['zona'] != zona_user[s['user']]]
    for k in user_fora:
        secs[k]['user_fora'] = True
    users_multi = {u: dict(c) for u, c in zonas_user.items() if len(c) >= 2}

    def dv_ok(t):
        if not (t and len(t) == 12 and t.isdigit()):
            return None
        d = [int(x) for x in t]; spmg = t[8:10] in ('01', '02')
        r1 = sum(d[i] * (i + 2) for i in range(8)) % 11
        r1 = 0 if r1 == 10 else (1 if (r1 == 0 and spmg) else r1)
        r2 = (d[8] * 7 + d[9] * 8 + r1 * 9) % 11
        r2 = 0 if r2 == 10 else (1 if (r2 == 0 and spmg) else r2)
        return r1 == d[10] and r2 == d[11]
    users = sorted({s['user'] for s in secs.values()})
    titulo = {'usuarios': len(users), 'dv_valido': sum(1 for u in users if dv_ok(u)),
              'secoes_com_uf_do_titulo_diferente_da_secao': sum(1 for s in secs.values() if dv_ok(s['user']) and
                                                               UF_TITULO.get(s['user'][8:10]) != s['uf'])}

    # C4: médias do resíduo nos grupos
    ipos = {k: i for i, k in enumerate(ks)}
    def grupo(lista):
        idx = np.array([ipos[k] for k in lista if k in ipos], dtype=int)
        if len(idx) == 0:
            return {'n': 0}
        m, ep, tipo, G = media_ep(idx, w, r, locs)
        return {'n': int(len(idx)), 'media': m, 'ep': ep, 'tipo_ep': tipo, 'locais': G}
    c4 = {'data_fora_da_janela': grupo(fora_jan), 'computador_fora_da_zona': grupo(comp_fora),
          'computador_sem_zona_no_nome': grupo([k for k, s in secs.items() if s['comp_classe'] == 'sem_zona_no_nome']),
          'computador_na_zona': grupo([k for k, s in secs.items() if s['comp_classe'] == 'na_zona']),
          'usuario_fora_da_zona': grupo(user_fora)}

    # C5: conferências
    t10 = json.load(open(arq_t10))['por_urna']
    conf_t10 = collections.Counter(); conf_t10_dif = []
    for kk, v in t10.items():
        uf, m5, z4, s4 = kk.split('/')
        k = f'{uf.upper()}|{int(m5)}|{int(z4)}|{int(s4)}'
        if k not in secs:
            conf_t10['fora_da_extracao'] += 1; continue
        if secs[k]['data'] in v['mr']:
            conf_t10['data_da_mr_escolhida_na_lista_do_T10'] += 1
        else:
            conf_t10['diferente'] += 1; conf_t10_dif.append((k, secs[k]['data'], v['mr']))
    mesma_25 = collections.Counter(('sem_mr_lida_em_25_10' if s['serie_25_10'] is None else
                                    ('igual' if s['serie_25_10'] == s['serie'] else 'diferente')) for s in secs.values())
    lida_antes = []
    for k, s in secs.items():
        g = ts_mr(s['data']); l = ts(s['lida_em'])
        if g and l and l < g:
            lida_antes.append((k, s['data'], s['lida_em']))
    serie_secs = collections.defaultdict(list)
    for k, s in secs.items():
        serie_secs[s['serie']].append(k)
    serie_rep = {x: v for x, v in serie_secs.items() if len(v) >= 2}
    tipos_erro = collections.Counter(); erro_secs = collections.defaultdict(set)
    for k, s in secs.items():
        for (t, app, nv, msg) in s['erros']:
            tm = re.sub(r'\(\d+\)', '(#)', msg.split(' Desligue')[0])[:160]
            tipos_erro[(app, nv, tm)] += 1; erro_secs[(app, nv, tm)].add(k)
    multi_comp = {k: s['comps_vota'] for k, s in secs.items() if len(s['comps_vota']) >= 2}
    multi_serie = {k: s['series_vota'] for k, s in secs.items() if len(s['series_vota']) >= 2}
    outras_mr = collections.Counter(m[0] for s in secs.values() for m in s['outras_mr'])
    comp_igual_carga = collections.Counter(('carga_sem_nome' if not s['carga'] else
                                            ('mesmo_computador_da_carga' if s['comp'] in s['carga'] else
                                             'computador_diferente_da_carga')) for s in secs.values())

    # ranking
    tab = sorted(((c, d) for c, d in por_c.items() if d['n'] >= 10), key=lambda t: -(t[1]['z'] or -1e9))
    def linha_c(c, d):
        return {'computador': c, **{k2: d[k2] for k2 in ('n', 'locais', 'media', 'ep', 'tipo_ep', 'z', 'ep_permutacao',
                                                          'z_permutacao', 'ufs', 'zona_no_nome', 'zonas_das_secoes')}}

    res = {
        'teste': 'F9 do Adendo 21: computador que gerou a mídia de resultado do 2º turno',
        'registro': 'PRE-REGISTRO-2026-10-26.md, Adendo 21, commit 913af7a (31/10/2026 10:36:29 UTC)',
        'script': 'scripts/analisar_F9.py',
        'entradas': {'bweb': arq_bweb, 'amostra': pasta, 't10': arq_t10},
        'extracao': {'pastas_na_amostra': len(itens), 'secoes_com_log': len(itens) - len(sem_log), 'sem_log': sem_log,
                     'pacotes_ilegiveis': ilegiveis, 'secoes_sem_mr_vota': sem_mr, 'regra_D3': dict(regras),
                     'secoes_com_mr': len(secs), 'fora_do_residuo': dict(fora_resid), 'secoes_na_estatistica': n,
                     'computadores_na_estatistica': K, 'ufs': len(ufs),
                     'computadores_com_10_ou_mais_secoes': sum(1 for d in por_c.values() if d['n'] >= 10),
                     'secoes_por_computador_percentis': {str(q): float(np.percentile([d['n'] for d in por_c.values()], q))
                                                         for q in (25, 50, 75, 90, 99)}},
        'estatistica_registrada': {'V_observado': V_obs, 'permutacoes': NPERM, 'semente': SEMENTE, 'p': p,
                                   'V_permutado_percentis': {str(q): float(np.percentile(Vp, q)) for q in (1, 5, 50, 95, 99, 99.9)},
                                   'V_observado_sobre_mediana_permutada': V_obs / float(np.median(Vp)),
                                   'media_geral_do_residuo': float((w * r).sum() / w.sum()),
                                   'computadores_que_cumprem_o_criterio': [linha_c(c, por_c[c]) for c in cumprem],
                                   'leitura_C3_com_ep_da_permutacao': [linha_c(c, por_c[c]) for c in cumprem_perm]},
        'veredito': veredito,
        'computadores_10_ou_mais_por_z': [linha_c(c, d) for c, d in tab],
        'computadores_maior_media_10_ou_mais': [linha_c(c, d) for c, d in sorted(tab, key=lambda t: -t[1]['media'])[:15]],
        'descritivo': {
            'datas_de_geracao_da_mr_do_2t': dict(sorted(dist_datas.items())),
            'mr_do_2t_fora_da_janela_05_a_23_10': [{'secao': k, 'data': secs[k]['data'], 'computador': secs[k]['comp'],
                                                    'usuario': secs[k]['user'], 'serie': secs[k]['serie'],
                                                    'lida_em': secs[k]['lida_em'], 'regra': secs[k]['regra'],
                                                    'r': secs[k].get('r')} for k in sorted(fora_jan)],
            'outras_mr_vota_do_pacote_fora_da_janela': fora_jan_outras,
            'computador_classe': dict(cls_comp),
            'computador_fora_da_zona_por_computador': dict(fora_por_comp.most_common()),
            'computador_com_uf_diferente_da_secao': comp_fora_uf,
            'usuario_fora_da_zona_secoes': len(user_fora),
            'usuarios_em_2_ou_mais_zonas': users_multi,
            'titulo_de_eleitor_do_usuario': titulo,
        },
        'complementar_fora_do_veredito': {
            'C1_identificacao_dentro_do_local': c1,
            'C2_poder': {'resumo': resumo_poder, 'por_computador': poder},
            'C3_ep_da_permutacao': {'computadores_que_cumpririam_com_ep_da_permutacao': cumprem_perm},
            'C4_residuo_nos_grupos_do_descritivo': c4,
            'C5_conferencias': {
                'T10_data_da_mr': dict(conf_t10), 'T10_diferencas': conf_t10_dif[:50],
                'mr_presente_em_25_10_igual_a_da_transicao': dict(mesma_25),
                'mr_lida_antes_da_data_de_geracao': lida_antes,
                'numero_de_serie_em_2_ou_mais_secoes': serie_rep,
                'secoes_com_2_ou_mais_computadores_de_mr_vota': multi_comp,
                'secoes_com_2_ou_mais_series_de_mr_vota': multi_serie,
                'outras_mr_no_pacote_por_aplicativo': dict(outras_mr),
                'erros_ligados_a_mr': [{'app': a, 'nivel': nv, 'mensagem': m, 'ocorrencias': q,
                                        'secoes': sorted(erro_secs[(a, nv, m)])[:40], 'n_secoes': len(erro_secs[(a, nv, m)])}
                                       for (a, nv, m), q in tipos_erro.most_common()],
                'problema_ao_desmontar_a_mr': {'ocorrencias': sum(s['desmontar'] for s in secs.values()),
                                               'secoes_com': sum(1 for s in secs.values() if s['desmontar'])},
                'computador_da_mr_e_o_da_carga': dict(comp_igual_carga),
            },
        },
        'por_secao': {k: {kk: v for kk, v in s.items() if kk not in ('erros',)} for k, s in sorted(secs.items())},
    }
    json.dump(res, open(saida_json, 'w'), ensure_ascii=False, indent=1, default=str)
    escrever_txt(res, saida_txt, secs)
    print(veredito, 'p =', p, 'V =', V_obs, 'n =', n, 'K =', K)


def escrever_txt(R, caminho, secs):
    e = R['extracao']; s = R['estatistica_registrada']; d = R['descritivo']; c = R['complementar_fora_do_veredito']
    L = []
    L.append('F9 do Adendo 21: computador que gerou a mídia de resultado (MR) do 2º turno')
    L.append('Registro: PRE-REGISTRO-2026-10-26.md, Adendo 21, commit 913af7a (31/10/2026 10:36:29 UTC). Script: scripts/analisar_F9.py.')
    L.append('')
    L.append(f'VEREDITO PELA LETRA: {R["veredito"]}')
    L.append(f'  p da permutação = {fmt(s["p"], 4)} (V observado {fmt(s["V_observado"], 4)}; mediana das permutações '
             f'{fmt(s["V_permutado_percentis"]["50"], 4)}; percentil 95 {fmt(s["V_permutado_percentis"]["95"], 4)}).')
    L.append(f'  Computadores com 10 ou mais seções, média de +2,0 ou mais e mais de 4 erros-padrão: '
             f'{len(s["computadores_que_cumprem_o_criterio"])}.')
    L.append('')
    L.append('1. Extração dos logs')
    L.append(f'  Pastas da amostra: {fmt(e["pastas_na_amostra"])}; com log: {fmt(e["secoes_com_log"])}; sem log: {len(e["sem_log"])} '
             f'({", ".join(e["sem_log"])}); pacotes ilegíveis: {len(e["pacotes_ilegiveis"])}.')
    L.append(f'  Seções com MR [VOTA] identificada: {fmt(e["secoes_com_mr"])}; sem: {len(e["secoes_sem_mr_vota"])}.')
    L.append(f'  Regra usada (D3): {json.dumps(e["regra_D3"], ensure_ascii=False)}')
    L.append(f'  Fora do resíduo: {json.dumps(e["fora_do_residuo"], ensure_ascii=False)}')
    L.append(f'  Na estatística: {fmt(e["secoes_na_estatistica"])} seções, {fmt(e["computadores_na_estatistica"])} computadores, '
             f'{e["ufs"]} UFs; computadores com 10 ou mais seções: {e["computadores_com_10_ou_mais_secoes"]}.')
    L.append(f'  Seções por computador (percentis 25, 50, 75, 90, 99): '
             f'{", ".join(fmt(v, 0) for v in e["secoes_por_computador_percentis"].values())}.')
    L.append('')
    L.append('2. Estatística registrada')
    L.append(f'  Média geral do resíduo (ponderada): {fmt(s["media_geral_do_residuo"])} ponto.')
    L.append(f'  V observado / mediana permutada: {fmt(s["V_observado_sobre_mediana_permutada"])}.')
    L.append(f'  Percentis de V nas permutações: ' + ', '.join(f'{q}: {fmt(v, 4)}' for q, v in s['V_permutado_percentis'].items()))
    L.append('  Computadores com 10 ou mais seções, ordenados por média/EP (primeiros 15 e últimos 5):')
    L.append(f'    {"computador":<18}{"seções":>7}{"locais":>7}{"média":>9}{"EP":>8}{"z":>8}{"EP perm":>9}{"z perm":>8}  zonas das seções')
    tab = R['computadores_10_ou_mais_por_z']
    for x in tab[:15] + ([None] if len(tab) > 20 else []) + tab[-5:]:
        if x is None:
            L.append('    ...'); continue
        L.append(f'    {x["computador"]:<18}{x["n"]:>7}{x["locais"]:>7}{fmt(x["media"]):>9}{fmt(x["ep"]):>8}{fmt(x["z"], 2):>8}'
                 f'{fmt(x["ep_permutacao"]):>9}{fmt(x["z_permutacao"], 2):>8}  {",".join(map(str, x["zonas_das_secoes"][:6]))}'
                 f'{" (EP por seção: um local só)" if x["tipo_ep"] == "por_secao_um_local_so" else ""}')
    L.append('  Observação: quando um computador cobre locais inteiros da amostra, os resíduos se anulam dentro de cada local e')
    L.append('  o erro-padrão agrupado fica quase nulo (z de dezenas ou centenas com média perto de zero). Esses z não indicam')
    L.append('  desvio; a coluna "EP perm" (C3) é a leitura estável. Nenhum deles chega perto de +2,0 pontos.')
    L.append('  Maiores médias (10 ou mais seções):')
    for x in R['computadores_maior_media_10_ou_mais'][:8]:
        L.append(f'    {x["computador"]:<18} n {x["n"]}, locais {x["locais"]}, média {fmt(x["media"])}, EP {fmt(x["ep"])}, z {fmt(x["z"], 2)}')
    L.append('')
    L.append('3. Descritivo do registro')
    L.append(f'  Datas de geração da MR do 2º turno (dia: seções): ' + ', '.join(f'{k}: {v}' for k, v in d['datas_de_geracao_da_mr_do_2t'].items()))
    L.append(f'  Fora da janela de 05 a 23/10: {len(d["mr_do_2t_fora_da_janela_05_a_23_10"])} seção(ões).')
    for x in d['mr_do_2t_fora_da_janela_05_a_23_10']:
        L.append(f'    {x["secao"]}: gerada {x["data"]}, lida {x["lida_em"]}, computador {x["computador"]}, usuário {x["usuario"]}, '
                 f'série {x["serie"]}, resíduo {fmt(x["r"])}')
    L.append(f'  Outras MR [VOTA] do pacote fora da janela: {len(d["outras_mr_vota_do_pacote_fora_da_janela"])}.')
    L.append(f'  Computador e zona: {json.dumps(d["computador_classe"], ensure_ascii=False)}')
    fz = d['computador_fora_da_zona_por_computador']
    L.append(f'  Computadores fora da zona da seção (computador: seções): ' + ', '.join(f'{k}: {v}' for k, v in list(fz.items())[:25])
             + (' ...' if len(fz) > 25 else ''))
    L.append(f'  Computador com UF diferente da seção: {len(d["computador_com_uf_diferente_da_secao"])}.')
    L.append(f'  Usuário fora da zona (zona mais comum do usuário na amostra): {d["usuario_fora_da_zona_secoes"]} seções; '
             f'usuários em 2 ou mais zonas: {len(d["usuarios_em_2_ou_mais_zonas"])}.')
    for u, z in list(d['usuarios_em_2_ou_mais_zonas'].items())[:20]:
        L.append(f'    {u}: zonas {json.dumps(z)}')
    t = d['titulo_de_eleitor_do_usuario']
    L.append(f'  Usuários: {t["usuarios"]}; com dígitos verificadores de título válidos: {t["dv_valido"]}; seções em que a UF do '
             f'título do usuário difere da UF da seção: {t["secoes_com_uf_do_titulo_diferente_da_secao"]}.')
    L.append('')
    L.append('4. Leituras complementares (fora do veredito)')
    c1 = c['C1_identificacao_dentro_do_local']
    L.append(f'  C1. Locais na estatística: {c1["locais_na_estatistica"]}; com 2 ou mais seções da amostra: {c1["locais_com_2_ou_mais_secoes"]}; '
             f'com 2 ou mais computadores: {c1["locais_com_2_ou_mais_computadores"]}; seções nesses locais: '
             f'{c1["secoes_em_locais_com_2_ou_mais_computadores"]} ({fmt(c1["peso_em_locais_com_2_ou_mais_computadores_pct"], 1)}% do peso).')
    if 'V' in c1:
        L.append(f'      Só nesses locais: V {fmt(c1["V"], 4)}; p permutando na UF {fmt(c1["p_permutacao_na_uf"], 4)}; '
                 f'p permutando dentro do local {fmt(c1["p_permutacao_no_local"], 4)}.')
        for k2, x in list(c1['computadores_nas_secoes_mistas_com_10_ou_mais'].items())[:10]:
            L.append(f'      {k2:<18} n {x["n"]}, locais {x["locais"]}, média {fmt(x["media"])}, EP {fmt(x["ep"])}')
    p2 = c['C2_poder']['resumo']
    L.append(f'  C2. Poder ({p2["computadores_com_10_ou_mais"]} computadores com 10 ou mais seções). Fração do deslocamento que '
             f'sobrevive ao resíduo (percentis 10, 25, 50, 75, 90): '
             + (', '.join(fmt(v, 2) for v in p2['atenuacao_percentis'].values()) if p2['atenuacao_percentis'] else 'n/d')
             + f'; abaixo de 0,1: {p2["atenuacao_abaixo_de_0_1"]}.')
    L.append(f'      Cumpririam o critério do computador com +2, +5 e +10 pontos: {json.dumps(p2["cumpririam_criterio_do_computador"])}; '
             f'dariam sinal completo (com p < 0,001) com +2, +5 e +10: {json.dumps(p2["dariam_sinal_completo"])}.')
    L.append(f'      Menor p de V com o deslocamento num computador só (+2, +5, +10): '
             + ', '.join(fmt(v, 4) for v in p2['menor_p_com_deslocamento'].values())
             + f'; computadores com p < 0,05: {json.dumps(p2["computadores_com_p_abaixo_de_0_05"])}.')
    L.append(f'  C3. Com o EP da permutação, cumpririam o critério: {c["C3_ep_da_permutacao"]["computadores_que_cumpririam_com_ep_da_permutacao"]}.')
    L.append('  C4. Resíduo médio nos grupos do descritivo:')
    for k2, x in c['C4_residuo_nos_grupos_do_descritivo'].items():
        L.append(f'      {k2}: n {x["n"]}' + (f', média {fmt(x["media"])}, EP {fmt(x["ep"])}, locais {x["locais"]}' if x['n'] else ''))
    c5 = c['C5_conferencias']
    L.append(f'  C5. Data da MR contra a extração do T10: {json.dumps(c5["T10_data_da_mr"], ensure_ascii=False)}')
    L.append(f'      MR presente em 25/10 igual à da transição: {json.dumps(c5["mr_presente_em_25_10_igual_a_da_transicao"], ensure_ascii=False)}')
    L.append(f'      MR lida antes da data de geração: {len(c5["mr_lida_antes_da_data_de_geracao"])}; número de série em 2 ou mais seções: '
             f'{len(c5["numero_de_serie_em_2_ou_mais_secoes"])}.')
    L.append(f'      Seções com 2 ou mais computadores de MR [VOTA]: {json.dumps(c5["secoes_com_2_ou_mais_computadores_de_mr_vota"], ensure_ascii=False)}')
    for x, v in c5['numero_de_serie_em_2_ou_mais_secoes'].items():
        L.append(f'      Série {x} em: ' + '; '.join(
            f'{k} (urna {secs[k]["urna_log"]}, local {secs[k].get("local")}, computador {secs[k]["comp"]}, gerada {secs[k]["data"]}, '
            f'transição lida em {secs[k]["lida_em"]}, série em 25/10: {secs[k]["serie_25_10"]}, resíduo {fmt(secs[k].get("r"))})' for k in v))
    L.append(f'      Seções com 2 ou mais números de série de MR [VOTA]: {len(c5["secoes_com_2_ou_mais_series_de_mr_vota"])} '
             + json.dumps(c5['secoes_com_2_ou_mais_series_de_mr_vota'], ensure_ascii=False))
    L.append(f'      Outras MR no pacote: {json.dumps(c5["outras_mr_no_pacote_por_aplicativo"], ensure_ascii=False)}')
    L.append(f'      Computador da MR do 2º turno e o da mídia de carga: {json.dumps(c5["computador_da_mr_e_o_da_carga"], ensure_ascii=False)}')
    L.append(f'      "Problema ao desmontar a MR" (rotina): {c5["problema_ao_desmontar_a_mr"]["ocorrencias"]} linhas em '
             f'{c5["problema_ao_desmontar_a_mr"]["secoes_com"]} seções.')
    L.append('      Erros e alertas ligados à MR (aplicativo, nível, mensagem: linhas, seções):')
    for x in c5['erros_ligados_a_mr']:
        L.append(f'        {x["app"]} {x["nivel"]} "{x["mensagem"]}": {x["ocorrencias"]} linhas, {x["n_secoes"]} seções'
                 + (f' ({", ".join(x["secoes"][:6])})' if x['n_secoes'] <= 6 else ''))
    c1 = c['C1_identificacao_dentro_do_local']; p2 = c['C2_poder']['resumo']
    L.append('')
    L.append('5. O que isso significa')
    L.append(f'  Pela letra, {R["veredito"]}: p = {fmt(s["p"], 4)}, acima de 0,05, e nenhum computador com 10 ou mais seções chega a')
    L.append('  +2,0 pontos. Mas o p perto de 1 não é sinal de limpeza: é efeito do desenho. A amostra é feita de locais inteiros e')
    L.append(f'  só {c1["locais_com_2_ou_mais_computadores"]} dos {c1["locais_com_2_ou_mais_secoes"]} locais com duas ou mais seções têm mais de um computador; '
             'o resíduo contra o próprio local')
    L.append('  zera a média de um computador que cobre o local inteiro, e a permutação dentro da UF não respeita isso, por isso o V')
    L.append('  observado fica abaixo de todas as permutações.')
    at50 = p2['atenuacao_percentis']['50'] if p2['atenuacao_percentis'] else None
    L.append(f'  Poder: na mediana dos computadores com 10 ou mais seções, sobrevive {fmt(at50, 2)} do deslocamento; um desvio de +2, +5')
    L.append(f'  ou +10 pontos num computador daria sinal completo em {p2["dariam_sinal_completo"]["2"]}, {p2["dariam_sinal_completo"]["5"]} '
             f'e {p2["dariam_sinal_completo"]["10"]} dos {p2["computadores_com_10_ou_mais"]} computadores.')
    L.append('  Ou seja: o F9, como registrado, não enxergaria uma mídia adulterada que fosse usada em todas as urnas de um local.')
    if 'p_permutacao_no_local' in c1:
        L.append(f'  Onde o teste enxerga (locais com mais de um computador, {c1["secoes_em_locais_com_2_ou_mais_computadores"]} seções), '
                 f'a permutação dentro do local dá p = {fmt(c1["p_permutacao_no_local"], 4)}:')
        L.append('  nenhuma diferença entre computadores do mesmo local além do acaso.')
    L.append('  O descritivo não traz, sozinho, indício de adulteração: uma MR fora da janela (gerada na véspera, 24/10, e lida 12')
    L.append('  minutos depois), computadores fora da zona concentrados em poucas UFs (DF, PR, AC e um caso em PE), nenhuma MR lida')
    L.append('  antes de gerada. Entre 05 e 25/10 só há duas falhas de conteúdo da MR do 2º turno: MG|51632|247|72 (assinatura do')
    L.append('  turno2.vsc recusada 4 vezes, MR trocada por outra do mesmo computador antes da transição) e PE|26018|61|89 (erro ao')
    L.append('  descompactar os dados do 2º turno depois da transição; a urna passou a usar uma MR gerada 6 minutos antes num')
    L.append('  computador de outra zona). As demais mensagens de erro de MR são de setembro e do 1º turno, ou de montagem e')
    L.append('  desmontagem. Um caso pede conferência física: a mesma série de MR em duas urnas de locais diferentes no dia da eleição.')
    open(caminho, 'w').write('\n'.join(L) + '\n')


if __name__ == '__main__':
    main()
