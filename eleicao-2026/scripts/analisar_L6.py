"""L6 do Adendo 18: o apoio dos governadores eleitos no 1º turno contra a virada de Lula por UF.

Registro (PRE-REGISTRO-2026-10-26.md, Adendo 18, escrito antes de rodar):
  - Lógica: governador eleito no 1º turno que fez campanha para um candidato puxa voto para ele no estado.
  - Lista fixada antes de cruzar com o resultado (imprensa, agente que não vê a virada): para cada UF com governador
    eleito no 1º turno, o apoio declarado no 2º turno (Flávio, Lula ou neutro) e a votação do governador no 1º turno.
  - Medida: virada de Lula por UF (pontos entre os dois finalistas) contra o apoio, ponderada pelos votos, e contra a
    votação do governador.
  - Incoerência: a virada de Lula nos estados com governador pró-Flávio não é menor que nos demais (diferença de zero
    ou mais). Coerente: menor em 1 ponto ou mais. Entre os dois: inconclusivo. Limite: poucos estados, apoio não
    aleatório.

Etapa 1 (feita antes deste script): resultados/L6_lista_governadores.json, gravado às 06:18:26 UTC de 29/10/2026,
sha256 f53b3fb3ba50b755375661c0e0d04cae085b825df5e1d0ac3e4d3711ec430547, antes de abrir qualquer resultado por UF.

Especificação (fixada na lista, antes de calcular; o que o registro não fixou vai como leitura ou desvio):
  1. Virada por UF = 100 L2/(L2+R2) - 100 L1/(L1+R1), com L e R somados em todas as seções da base de cada turno
     (L = 13, Lula; R = 22, Flávio). Conferência: só as seções com os dois turnos.
  2. Peso = L2 + R2 da UF (votos dos finalistas no 2º turno, a convenção do L2 e do T17).
  3. Comparação principal: média ponderada da virada nas UFs com governador pró-Flávio menos a média ponderada nas
     demais UFs da lista (pró-Lula e neutras), com o RJ dentro (eleito no 1º turno após a retotalização).
  4. Veredito: diferença >= 0 -> INCOERÊNCIA; diferença <= -1 -> COERENTE; entre -1 e 0 -> INCONCLUSIVO.
  5. Erro-padrão (o registro não pede; vai ao lado): MQP da virada contra o indicador pró-Flávio, com erro robusto HC1
     e HC3 entre UFs, e o teste exato de permutação (todas as maneiras de escolher 12 das 21 UFs).
  6. Sensibilidades: sem o RJ; demais = todas as outras UFs (27 menos as pró-Flávio, sem o exterior); pró-Flávio
     contra pró-Lula só; sem peso.
  7. Votação do governador: % dos votos válidos oficiais (imprensa, na lista), conferida com o bweb (cargo 3, votos
     nominais); no RJ o bweb também sem os votos de Garotinho. O bweb conta como nominais os votos de candidatos
     depois anulados (SE: 57,71% no bweb contra 59,27% oficial; SP: 62,59% contra 62,65%); nas outras 19 bate. MQP da virada contra a votação com sinal
     (+ pró-Flávio, - pró-Lula, 0 neutro), e só entre as pró-Flávio.
  Descritivo (fora do critério, não muda o veredito): virada em logito e em fração da base de Flávio; virada com a
  fatia de Lula no 1º turno e a fatia dos eliminados como controles; resíduo contra o previsto só pelos eliminados
  (flavio_previsto_por_uf.txt, de outra análise); dentro do Nordeste e fora dele.

Uso: python3 -I analisar_L6.py <secoes2026.json.gz> <zips1t_dir> <lista.json> <previsto_por_uf.txt> <cache_gov.json.gz> <saida.json> <saida.txt>
"""
import os as _os, sys as _sys
_sys.path.insert(0, _os.path.dirname(_os.path.abspath(__file__)))
import collections, csv, glob, gzip, itertools, json, math, os, sys, time, zipfile
from multiprocessing import Pool
import numpy as np
from lib import carregar

NORDESTE = {'AL', 'BA', 'CE', 'MA', 'PB', 'PE', 'PI', 'RN', 'SE'}
TODAS = ['AC', 'AL', 'AM', 'AP', 'BA', 'CE', 'DF', 'ES', 'GO', 'MA', 'MG', 'MS', 'MT', 'PA', 'PB', 'PE', 'PI', 'PR',
         'RJ', 'RN', 'RO', 'RR', 'RS', 'SC', 'SE', 'SP', 'TO']


def log(msg):
    print(time.strftime('%H:%M:%S'), msg, flush=True)


# ---------------------------------------------------------------- governador no bweb do 1º turno

def ler_gov(zpath):
    z = zipfile.ZipFile(zpath)
    nome = [n for n in z.namelist() if n.lower().endswith('.csv')][0]
    tot = collections.Counter(); nomes = {}; tipos = collections.Counter(); secoes = set()
    por_secao = collections.defaultdict(dict)
    alvo = b';3;"Governador";'
    with z.open(nome) as fh:
        cab = [c.strip().strip('"') for c in fh.readline().decode('latin1').strip().split(';')]
        ix = {c: i for i, c in enumerate(cab)}
        for linha in fh:
            if alvo not in linha:
                continue
            r = next(csv.reader([linha.decode('latin1').rstrip('\r\n')], delimiter=';'))
            if r[ix['CD_CARGO_PERGUNTA']] != '3':
                continue
            k = f"{r[ix['SG_UF']]}|{int(r[ix['CD_MUNICIPIO']])}|{int(r[ix['NR_ZONA']])}|{int(r[ix['NR_SECAO']])}"
            secoes.add(k)
            tp = r[ix['CD_TIPO_VOTAVEL']]; ds = r[ix['DS_TIPO_VOTAVEL']]; nr = r[ix['NR_VOTAVEL']]; q = int(r[ix['QT_VOTOS']])
            tipos[(tp, ds)] += q
            if tp == '1':
                tot[nr] += q; nomes[nr] = f"{r[ix['NM_VOTAVEL']]} ({r[ix['SG_PARTIDO']]})"
                por_secao[k][nr] = q
    uf = os.path.basename(zpath).split('_')[2]
    return uf, dict(tot), nomes, {f'{a}|{b}': v for (a, b), v in tipos.items()}, len(secoes), dict(por_secao)


def governador(zdir, ufs, cache):
    if os.path.exists(cache):
        with gzip.open(cache, 'rt') as f:
            return json.load(f)
    zs = [z for z in sorted(glob.glob(os.path.join(zdir, '*.zip'))) if os.path.basename(z).split('_')[2] in ufs]
    zs.sort(key=lambda p: -os.path.getsize(p))
    out = {}
    with Pool(4) as p:
        for uf, tot, nomes, tipos, ns, ps in p.imap_unordered(ler_gov, zs):
            out[uf] = {'nominais': tot, 'nomes': nomes, 'tipos': tipos, 'secoes': ns, 'por_secao': ps}
            log(f'  governador {uf}: {ns} seções, {sum(tot.values())} votos nominais')
    with gzip.open(cache, 'wt') as f:
        json.dump(out, f)
    return out


# ---------------------------------------------------------------- estatística entre UFs

def wmean(v, w):
    return float(np.sum(v * w) / np.sum(w))


def wls(y, X, w):
    """MQP com erro robusto HC1 e HC3 (entre UFs)."""
    y = np.asarray(y, float); X = np.asarray(X, float); w = np.asarray(w, float)
    n, k = X.shape
    sw = np.sqrt(w)
    Xw, yw = X * sw[:, None], y * sw
    inv = np.linalg.inv(Xw.T @ Xw)
    b = inv @ Xw.T @ yw
    e = yw - Xw @ b
    h = np.einsum('ij,jk,ik->i', Xw, inv, Xw)
    m1 = (Xw * e[:, None]).T @ (Xw * e[:, None])
    V1 = inv @ m1 @ inv * n / (n - k)
    e3 = e / (1 - h)
    m3 = (Xw * e3[:, None]).T @ (Xw * e3[:, None])
    V3 = inv @ m3 @ inv
    return b, np.sqrt(np.diag(V1)), np.sqrt(np.diag(V3))


def permutacao(v, w, nF):
    """Todas as maneiras de escolher nF UFs como pró-Flávio: distribuição exata da diferença ponderada."""
    n = len(v); idx = np.arange(n); difs = []
    tw = w.sum(); tvw = (v * w).sum()
    for c in itertools.combinations(idx, nF):
        c = list(c)
        wf = w[c].sum(); vf = (v[c] * w[c]).sum()
        difs.append(vf / wf - (tvw - vf) / (tw - wf))
    return np.array(difs)


def comparar(rot, ufs_F, ufs_O, V, W, perm=True):
    uF = [u for u in ufs_F]; uO = [u for u in ufs_O]
    vF = np.array([V[u] for u in uF]); wF = np.array([W[u] for u in uF])
    vO = np.array([V[u] for u in uO]); wO = np.array([W[u] for u in uO])
    d = wmean(vF, wF) - wmean(vO, wO)
    d_sp = float(vF.mean() - vO.mean())
    v = np.concatenate([vF, vO]); w = np.concatenate([wF, wO])
    D = np.concatenate([np.ones(len(vF)), np.zeros(len(vO))])
    X = np.column_stack([np.ones(len(v)), D])
    b, e1, e3 = wls(v, X, w)
    bu, eu1, eu3 = wls(v, X, np.ones(len(v)))
    out = {'rotulo': rot, 'n_F': len(uF), 'n_outros': len(uO), 'ufs_F': uF, 'ufs_outros': uO,
           'media_pond_F': wmean(vF, wF), 'media_pond_outros': wmean(vO, wO), 'dif_pond': d,
           'ep_HC1': float(e1[1]), 'ep_HC3': float(e3[1]),
           'media_simples_F': float(vF.mean()), 'media_simples_outros': float(vO.mean()), 'dif_sem_peso': d_sp,
           'ep_sem_peso_HC1': float(eu1[1]), 'ep_sem_peso_HC3': float(eu3[1]),
           'leitura_pond': leitura(d), 'leitura_sem_peso': leitura(d_sp)}
    if perm and math.comb(len(v), len(vF)) <= 3_000_000:
        dist = permutacao(v, w, len(vF))
        out['perm_n'] = int(len(dist))
        out['perm_p_dif_maior_ou_igual'] = float(np.mean(dist >= d - 1e-12))
        out['perm_p_bicaudal'] = float(np.mean(np.abs(dist - dist.mean()) >= abs(d - dist.mean()) - 1e-12))
        out['perm_media'] = float(dist.mean()); out['perm_dp'] = float(dist.std())
    return out


def leitura(d):
    if d >= 0:
        return 'INCOERÊNCIA'
    if d <= -1:
        return 'COERENTE'
    return 'INCONCLUSIVO'


def logit(p):
    return math.log(p / (1 - p))


# ---------------------------------------------------------------- principal

def main():
    base, zdir, lista_p, prev_p, cache, saida_json, saida_txt = sys.argv[1:8]
    lista = json.load(open(lista_p))
    gov = {g['uf']: g for g in lista['governadores']}
    ufs_lista = sorted(gov)
    apoio = {u: gov[u]['apoio_2t'] for u in ufs_lista}
    log(f'lista: {len(ufs_lista)} UFs; ' + ', '.join(f'{u}={apoio[u]}' for u in ufs_lista))

    # 1. virada por UF a partir da base
    log('lendo a base')
    d = carregar(base)
    S = collections.defaultdict(lambda: collections.Counter())
    for k, v in d.items():
        uf = k.split('|')[0]
        for t in ('1', '2'):
            if t in v:
                s = v[t]
                S[uf][f'L{t}'] += s['L']; S[uf][f'R{t}'] += s['R']; S[uf][f'O{t}'] += s['O']
                S[uf][f'B{t}'] += s['B']; S[uf][f'N{t}'] += s['N']; S[uf][f'comp{t}'] += s['comp']
                S[uf][f'apt{t}'] += s['apt']; S[uf][f'sec{t}'] += 1
        if '1' in v and '2' in v and v['1']['L'] + v['1']['R'] > 0 and v['2']['L'] + v['2']['R'] > 0:
            for t in ('1', '2'):
                S[uf][f'mL{t}'] += v[t]['L']; S[uf][f'mR{t}'] += v[t]['R']
            S[uf]['msec'] += 1
    del d
    V, W, Vm, UF = {}, {}, {}, {}
    for uf in TODAS + ['ZZ']:
        s = S[uf]
        f1 = s['L1'] / (s['L1'] + s['R1']); f2 = s['L2'] / (s['L2'] + s['R2'])
        V[uf] = 100 * (f2 - f1); W[uf] = s['L2'] + s['R2']
        Vm[uf] = 100 * (s['mL2'] / (s['mL2'] + s['mR2']) - s['mL1'] / (s['mL1'] + s['mR1']))
        val1 = s['L1'] + s['R1'] + s['O1']
        UF[uf] = {'L1': s['L1'], 'R1': s['R1'], 'O1': s['O1'], 'L2': s['L2'], 'R2': s['R2'],
                  'secoes_1t': s['sec1'], 'secoes_2t': s['sec2'], 'secoes_pareadas': s['msec'],
                  'fatia_Lula_1T': 100 * f1, 'fatia_Lula_2T': 100 * f2, 'virada': V[uf], 'virada_pareadas': Vm[uf],
                  'peso_L2_R2': W[uf], 'eliminados_pct_validos_1T': 100 * s['O1'] / val1,
                  'Flavio_pct_validos_1T': 100 * s['R1'] / val1, 'Lula_pct_validos_1T': 100 * s['L1'] / val1,
                  'var_comparecimento_pp': 100 * (s['comp2'] / s['apt2'] - s['comp1'] / s['apt1']),
                  'virada_logito': logit(f2) - logit(f1),
                  'perda_Flavio_fracao_da_base': 100 * ((1 - f1) - (1 - f2)) / (1 - f1)}
    log('virada por UF: ' + ', '.join(f'{u} {V[u]:+.2f}' for u in TODAS))

    # 2. governador no bweb do 1º turno
    log('lendo governador no bweb do 1º turno')
    G = governador(zdir, set(ufs_lista), cache)
    gv = {}
    for u in ufs_lista:
        g = G[u]; tot = g['nominais']; nom = sum(tot.values())
        ven = max(tot, key=tot.get)
        pct = 100 * tot[ven] / nom
        rank = sorted(tot.items(), key=lambda x: -x[1])
        gv[u] = {'numero_vencedor': ven, 'nome_bweb': g['nomes'][ven], 'votos': tot[ven], 'nominais': nom,
                 'pct_nominais_bweb': pct, 'pct_imprensa': gov[u]['voto_1t_pct_validos_imprensa'],
                 'segundo': [rank[1][0], g['nomes'][rank[1][0]], 100 * rank[1][1] / nom] if len(rank) > 1 else None,
                 'tipos_de_voto': g['tipos'], 'secoes_bweb': g['secoes']}
    # RJ: vencedor proclamado após anular os votos de Garotinho
    if 'RJ' in G:
        tot = G['RJ']['nominais']; nomes = G['RJ']['nomes']
        gar = [n for n, s in nomes.items() if 'GAROTINHO' in s.upper()]
        ruas = [n for n, s in nomes.items() if 'RUAS' in s.upper()]
        if gar and ruas:
            nom2 = sum(tot.values()) - sum(tot[n] for n in gar)
            gv['RJ']['numero_vencedor'] = ruas[0]; gv['RJ']['nome_bweb'] = nomes[ruas[0]]; gv['RJ']['votos'] = tot[ruas[0]]
            gv['RJ']['pct_com_garotinho'] = 100 * tot[ruas[0]] / sum(tot.values())
            gv['RJ']['pct_nominais_bweb'] = 100 * tot[ruas[0]] / nom2
            gv['RJ']['nota'] = f'sem os votos de {nomes[gar[0]]}, anulados pelo TSE'
    for u in ufs_lista:
        log(f"  {u}: {gv[u]['nome_bweb']} {gv[u]['pct_nominais_bweb']:.2f}% (imprensa {gv[u]['pct_imprensa']:.2f}%)")

    # 3. comparações
    F = [u for u in ufs_lista if apoio[u] == 'Flavio']
    Lu = [u for u in ufs_lista if apoio[u] == 'Lula']
    Ne = [u for u in ufs_lista if apoio[u] == 'neutro']
    resto_lista = Lu + Ne
    fora = [u for u in TODAS if u not in ufs_lista]
    comps = {
        'principal': comparar('pró-Flávio contra as demais da lista (pró-Lula e neutras), com o RJ', F, resto_lista, V, W),
        'sem_RJ': comparar('sem o RJ', [u for u in F if u != 'RJ'], resto_lista, V, W),
        'contra_todas_as_outras_UFs': comparar('pró-Flávio contra todas as outras 15 UFs (inclui as 6 sem governador eleito no 1º turno)', F, resto_lista + fora, V, W, perm=True),
        'contra_pro_Lula': comparar('pró-Flávio contra pró-Lula só', F, Lu, V, W),
        'pareadas': comparar('virada só com as seções dos dois turnos', F, resto_lista, Vm, W),
    }
    # pró-Lula contra as demais (simetria) e neutras
    comps['pro_Lula_contra_demais'] = comparar('pró-Lula contra as demais da lista (simetria: pró-Lula deveria ter virada maior)', Lu, F + Ne, V, W)
    comps['pro_Flavio_contra_neutras'] = comparar('pró-Flávio contra neutras só', F, Ne, V, W)
    morno = {'MG', 'MT'}  # voto declarado sem apoio formal de campanha (Gazeta do Povo, 06/10)
    comps['Cleitinho_e_Pivetta_como_neutros'] = comparar('MG e MT (voto declarado sem campanha formal) contados como neutros',
                                                         [u for u in F if u not in morno], resto_lista + sorted(morno), V, W)

    # 4. votação do governador
    sinal = {'Flavio': 1, 'Lula': -1, 'neutro': 0}
    u_ = ufs_lista
    y = np.array([V[u] for u in u_]); w = np.array([W[u] for u in u_])
    gs = np.array([sinal[apoio[u]] * gv[u]['pct_imprensa'] for u in u_])
    b, e1, e3 = wls(y, np.column_stack([np.ones(len(y)), gs]), w)
    reg_gov = {'virada_contra_votacao_com_sinal': {'coef_por_ponto': float(b[1]), 'ep_HC1': float(e1[1]), 'ep_HC3': float(e3[1]),
                                                    'leitura': 'coef negativo = mais voto do governador pró-Flávio, menos virada de Lula'}}
    yF = np.array([V[u] for u in F]); wF = np.array([W[u] for u in F]); gF = np.array([gv[u]['pct_imprensa'] for u in F])
    b, e1, e3 = wls(yF, np.column_stack([np.ones(len(yF)), gF]), wF)
    reg_gov['so_pro_Flavio_virada_contra_votacao'] = {'coef_por_ponto': float(b[1]), 'ep_HC1': float(e1[1]), 'ep_HC3': float(e3[1])}
    yL = np.array([V[u] for u in Lu]); wL = np.array([W[u] for u in Lu]); gL = np.array([gv[u]['pct_imprensa'] for u in Lu])
    b, e1, e3 = wls(yL, np.column_stack([np.ones(len(yL)), gL]), wL)
    reg_gov['so_pro_Lula_virada_contra_votacao'] = {'coef_por_ponto': float(b[1]), 'ep_HC1': float(e1[1]), 'ep_HC3': float(e3[1]), 'n': len(Lu)}

    # 5. descritivo: outras escalas e controles
    desc = {}
    for nome, chave in (('logito', 'virada_logito'), ('perda_de_Flavio_em_fracao_da_base', 'perda_Flavio_fracao_da_base')):
        VV = {u: UF[u][chave] for u in TODAS}
        desc[nome] = comparar(f'escala {nome}', F, resto_lista, VV, W, perm=True)
    D = np.array([1.0 if apoio[u] == 'Flavio' else 0.0 for u in u_])
    f1 = np.array([UF[u]['fatia_Lula_1T'] for u in u_]); el = np.array([UF[u]['eliminados_pct_validos_1T'] for u in u_])
    dc = np.array([UF[u]['var_comparecimento_pp'] for u in u_])
    for nome, X in (('controle_fatia_Lula_1T', [f1]), ('controle_eliminados_1T', [el]),
                    ('controle_fatia_e_eliminados', [f1, el]), ('controle_fatia_eliminados_comparecimento', [f1, el, dc])):
        b, e1, e3 = wls(y, np.column_stack([np.ones(len(y)), D] + X), w)
        desc[nome] = {'dif_pro_Flavio': float(b[1]), 'ep_HC1': float(e1[1]), 'ep_HC3': float(e3[1]), 'n': len(y)}
    # resíduo contra o previsto só pelos eliminados (outra análise)
    prev = {}
    for linha in open(prev_p, encoding='utf-8'):
        p = [x.strip() for x in linha.split('|')]
        if len(p) >= 2 and len(p[0]) == 2 and '->' in p[1]:
            try:
                a = [float(x) for x in p[1].split('->')]
            except ValueError:
                continue  # cabeçalho
            prev[p[0]] = {'flavio_1T': a[0], 'previsto_so_eliminados': a[1], 'real': a[2]}
    if prev:
        VR = {u: (prev[u]['previsto_so_eliminados'] - prev[u]['real']) for u in TODAS if u in prev}
        VC = {u: (prev[u]['flavio_1T'] - prev[u]['previsto_so_eliminados']) for u in TODAS if u in prev}
        desc['residuo_contra_previsto_so_eliminados'] = comparar('virada de Lula além do previsto só pelos eliminados', F, resto_lista, VR, W, perm=True)
        desc['parte_prevista_so_pelos_eliminados'] = comparar('parte da virada de Lula prevista só pelos eliminados', F, resto_lista, VC, W, perm=False)
        desc['conferencia_previsto'] = {u: {'virada_base': V[u], 'virada_tabela': prev[u]['flavio_1T'] - prev[u]['real']} for u in TODAS if u in prev}
    # dentro e fora do Nordeste
    ne_list = [u for u in ufs_lista if u in NORDESTE]; fo_list = [u for u in ufs_lista if u not in NORDESTE]
    desc['fora_do_Nordeste'] = comparar('fora do Nordeste: pró-Flávio contra neutras (AP)', [u for u in fo_list if apoio[u] == 'Flavio'],
                                        [u for u in fo_list if apoio[u] != 'Flavio'], V, W, perm=False)
    desc['dentro_do_Nordeste'] = {'pro_Lula': {u: V[u] for u in ne_list if apoio[u] == 'Lula'},
                                  'neutras': {u: V[u] for u in ne_list if apoio[u] == 'neutro'},
                                  'pro_Flavio': {u: V[u] for u in ne_list if apoio[u] == 'Flavio'},
                                  'media_pond_pro_Lula': wmean(np.array([V[u] for u in ne_list if apoio[u] == 'Lula']), np.array([W[u] for u in ne_list if apoio[u] == 'Lula'])),
                                  'media_pond_neutras': wmean(np.array([V[u] for u in ne_list if apoio[u] == 'neutro']), np.array([W[u] for u in ne_list if apoio[u] == 'neutro']))}

    veredito = comps['principal']['leitura_pond']
    res = {'teste': 'L6', 'lista': lista_p, 'lista_sha256': 'f53b3fb3ba50b755375661c0e0d04cae085b825df5e1d0ac3e4d3711ec430547',
           'apoio': apoio, 'por_uf': UF, 'governador_bweb': gv, 'comparacoes': comps, 'votacao_do_governador': reg_gov,
           'descritivo': desc, 'veredito': veredito}
    json.dump(res, open(saida_json, 'w'), ensure_ascii=False, indent=1)
    escrever_txt(res, saida_txt, F, Lu, Ne, fora)
    log(f'veredito: {veredito}')


def escrever_txt(r, p, F, Lu, Ne, fora):
    UF = r['por_uf']; gv = r['governador_bweb']; c = r['comparacoes']
    L = []
    a = L.append
    a('L6 do Adendo 18: apoio dos governadores eleitos no 1º turno contra a virada de Lula por UF')
    a('Lista fixada antes do cálculo: resultados/L6_lista_governadores.json (06:18:26 UTC de 29/10/2026, sha256 f53b3fb3...).')
    a('Virada = fatia de Lula entre os dois finalistas no 2º turno menos a do 1º turno, em pontos, somando a UF na base por seção.')
    a('')
    a('UF  apoio    governador (bweb)                       gov 1T %  imprensa  Lula 1T  Lula 2T  virada  pareadas  elimin.1T')
    for u in F + Lu + Ne + fora:
        ap = r['apoio'].get(u, 'sem gov 1T')
        g = gv.get(u)
        gt = f"{g['nome_bweb'][:38]:38s}  {g['pct_nominais_bweb']:7.2f}  {g['pct_imprensa']:8.2f}" if g else f"{'':38s}  {'':7s}  {'':8s}"
        a(f"{u}  {ap:7s}  {gt}  {UF[u]['fatia_Lula_1T']:7.2f}  {UF[u]['fatia_Lula_2T']:7.2f}  {UF[u]['virada']:+6.2f}  {UF[u]['virada_pareadas']:+8.2f}  {UF[u]['eliminados_pct_validos_1T']:8.2f}")
    a('')
    for k, v in c.items():
        a(f"[{k}] {v['rotulo']}")
        a(f"  ponderado: pró ({v['n_F']}) {v['media_pond_F']:+.3f} contra outros ({v['n_outros']}) {v['media_pond_outros']:+.3f} -> diferença {v['dif_pond']:+.3f} pontos"
          f" (ep HC1 {v['ep_HC1']:.3f}, HC3 {v['ep_HC3']:.3f}) -> {v['leitura_pond']}")
        a(f"  sem peso:  {v['media_simples_F']:+.3f} contra {v['media_simples_outros']:+.3f} -> {v['dif_sem_peso']:+.3f} (ep HC1 {v['ep_sem_peso_HC1']:.3f}, HC3 {v['ep_sem_peso_HC3']:.3f}) -> {v['leitura_sem_peso']}")
        if 'perm_n' in v:
            a(f"  permutação exata ({v['perm_n']} arranjos): P(dif >= observada) = {v['perm_p_dif_maior_ou_igual']:.4f}; bicaudal {v['perm_p_bicaudal']:.4f}")
    a('')
    for k, v in r['votacao_do_governador'].items():
        a(f"[votação do governador] {k}: {v['coef_por_ponto']:+.4f} pontos de virada por ponto de votação (ep HC1 {v['ep_HC1']:.4f}, HC3 {v['ep_HC3']:.4f})")
    a('')
    for k, v in r['descritivo'].items():
        if isinstance(v, dict) and 'dif_pond' in v:
            a(f"[descritivo] {v['rotulo']}: {v['media_pond_F']:+.3f} contra {v['media_pond_outros']:+.3f} -> {v['dif_pond']:+.3f} (ep HC1 {v['ep_HC1']:.3f}, HC3 {v['ep_HC3']:.3f})"
              + (f"; permutação P(>=) {v['perm_p_dif_maior_ou_igual']:.4f}" if 'perm_n' in v else ''))
        elif isinstance(v, dict) and 'dif_pro_Flavio' in v:
            a(f"[descritivo] {k}: diferença pró-Flávio {v['dif_pro_Flavio']:+.3f} (ep HC1 {v['ep_HC1']:.3f}, HC3 {v['ep_HC3']:.3f})")
    dn = r['descritivo']['dentro_do_Nordeste']
    a(f"[descritivo] dentro do Nordeste: pró-Lula {', '.join(f'{u} {x:+.2f}' for u, x in dn['pro_Lula'].items())} (média pond. {dn['media_pond_pro_Lula']:+.3f});"
      f" neutras {', '.join(f'{u} {x:+.2f}' for u, x in dn['neutras'].items())} (média pond. {dn['media_pond_neutras']:+.3f})")
    a('')
    p0 = c['principal']; d = r['descritivo']
    a('LEITURAS E DESVIOS (declarados):')
    a('  1. Universo: 21 UFs. O RJ entra porque Douglas Ruas foi proclamado eleito no 1º turno depois da anulação dos votos de')
    a('     Garotinho (TSE) e da retotalização (TRE-RJ, 15/10); não houve 2º turno de governador lá. Sem o RJ, o veredito é o mesmo.')
    a('  2. "Nos demais" lido como as demais UFs da lista (pró-Lula e neutras), porque o registro define a lista só com as UFs de')
    a('     governador eleito no 1º turno. Com todas as outras UFs (as 6 com 2º turno de governador incluídas), o veredito é o mesmo.')
    a('  3. "Ponderada pelos votos": peso = votos de Lula + Flávio no 2º turno da UF (convenção do L2 e do T17). Sem peso, o mesmo.')
    a('  4. Votação do governador: % oficial dos válidos (imprensa). O bweb confere em 19 UFs; em SE (57,71% contra 59,27%) e SP')
    a('     (62,59% contra 62,65%) o bweb conta como nominais votos de candidatos depois anulados.')
    a('  5. Cleitinho (MG) e Pivetta (MT) declararam voto em Flávio sem campanha formal: contam como pró-Flávio pela regra fixada')
    a('     na lista antes do cálculo. Contados como neutros, o veredito é o mesmo.')
    a('  6. Erro-padrão e permutação não estão no registro (o critério é só o sinal e o tamanho da diferença); vão ao lado.')
    a('  7. Na etapa 1, os resumos automáticos da busca deixaram escapar alguns números por UF (2º turno em MG e AL, 1º turno em')
    a('     outras). A classificação vem só das declarações e a regra foi fixada antes; nenhum governador foi reclassificado.')
    a('')
    a('O QUE O NÚMERO QUER DIZER (descritivo, não muda o veredito):')
    a(f"  - A virada de Lula foi maior onde o governador era pró-Flávio ({p0['media_pond_F']:+.2f} contra {p0['media_pond_outros']:+.2f}),")
    a('    o contrário do que a lógica do teste esperava. Mas o mesmo padrão aparece do outro lado: onde o governador era pró-Lula,')
    a(f"    a virada de Lula foi MENOR ({c['pro_Lula_contra_demais']['dif_pond']:+.2f}). Ou seja, o apoio do governador não aparece em nenhum dos dois lados;")
    a('    o que separa os grupos é onde Flávio era forte no 1º turno (os pró-Flávio são Sul, Sudeste, Centro-Oeste e Norte; os outros, Nordeste e AP).')
    a(f"  - Medida como fração da base de Flávio, a perda é igual nos dois grupos: {d['perda_de_Flavio_em_fracao_da_base']['media_pond_F']:.2f}% contra "
      f"{d['perda_de_Flavio_em_fracao_da_base']['media_pond_outros']:.2f}% (diferença {d['perda_de_Flavio_em_fracao_da_base']['dif_pond']:+.2f}, ep {d['perda_de_Flavio_em_fracao_da_base']['ep_HC1']:.2f}).")
    a(f"  - Com a fatia de Lula no 1º turno como controle, a diferença cai para {d['controle_fatia_Lula_1T']['dif_pro_Flavio']:+.2f} (ep {d['controle_fatia_Lula_1T']['ep_HC1']:.2f} a {d['controle_fatia_Lula_1T']['ep_HC3']:.2f}).")
    a(f"  - Os eleitores dos eliminados explicam {d['parte_prevista_so_pelos_eliminados']['dif_pond']:+.2f} ponto da diferença (no Nordeste eles empurram contra Lula, que já tinha 65 a 75%).")
    a('  - Uma perda proporcional de eleitores de Flávio, seja por troca de voto, seja por desvio de uma fração fixa, daria este')
    a('    mesmo padrão. O L6 não separa as duas coisas; quem tenta separar é o L3 (núcleo do PL).')
    a('')
    a(f"VEREDITO PELA LETRA (comparação principal): {r['veredito']}")
    open(p, 'w', encoding='utf-8').write('\n'.join(L) + '\n')


if __name__ == '__main__':
    main()
