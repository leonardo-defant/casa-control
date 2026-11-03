"""F19 do Adendo 23 (H1 da caça ao furo): o exterior, sem biometria, contra seções do Brasil de composição igual.

Registro (PRE-REGISTRO-2026-10-26.md, Adendo 23, commit 863a34e, 03/11/2026 01:13:05 UTC, antes de rodar):
  - Hipótese que se testa: um programa que fica honesto quando a urna não tem nenhuma habilitação por biometria no dia.
    Única votação real nessa condição: o exterior.
  - Pareamento: cada seção do exterior com pelo menos 30 votos nos finalistas no 2º turno é pareada com as 20 seções do
    Brasil mais próximas em: fatia de Lula entre os finalistas no 1º turno, fatia dos outros candidatos, fatia de branco
    e nulo, e variação do comparecimento entre os turnos (pontos dos aptos), distância euclidiana sobre as variáveis
    padronizadas. D = virada média (fatia de Lula entre os finalistas, 2º menos 1º turno) do exterior menos a dos pares,
    ponderada pelos votos dos finalistas no 2º turno. Erro por bootstrap de cidades do exterior (2.000, semente 20261103).
  - Robustez fixada antes: pareamento só com seções do Brasil de urna antiga (UE2013 ou UE2015, faixas do F4); só com
    seções de capital; sem a variação do comparecimento; com 10 e com 50 pares.
  - Sinal: D de -1,5 ponto ou menos a mais de 4 erros-padrão. Sem sinal: |D| abaixo de 0,5 com erro-padrão até 0,25.
    Entre os dois: inconclusivo. Relatar a fração do desvio de 1,79 ponto que D representaria.

Decisões que o registro não fixa, tomadas e escritas aqui ANTES de calcular qualquer virada (cada uma é um desvio
declarado). O que foi visto antes de escrever: a estrutura dos arquivos (campos, tipos, contagem de seções: 1.309 do
exterior no 1º turno, 1.308 no 2º, 145 códigos de cidade, 1.216 com seções agregadas; 27 seções do exterior sem horário
de abertura no 2º turno, com 2 números de urna repetidos; QT_ELEI_BIOM_SEM_HABILITACAO = 0 em todas as linhas do exterior
no bweb do 2º turno; 55.722 seções com aptos diferentes entre os turnos; urnas do exterior pelo F4: UE2013 979, UE2015
287, sem modelo 42) e os resultados já publicados do L7 (exterior 1,62 contra 2,80 no Brasil; 0,76 abaixo do previsto,
ep 0,15, na conferência). Nenhuma virada pareada foi calculada antes deste docstring.

  D1. Universo: seções com os dois turnos na base, comparecimento positivo nos dois e votos nos finalistas positivos nos
      dois. Exterior = UF ZZ com L2+R2 >= 30 (o registro). Candidatas a par = seções fora do ZZ com o mesmo piso de 30
      votos nos finalistas no 2º turno (desvio: o registro só fixa o piso para o exterior; o piso iguala o ruído
      amostral mínimo dos dois lados e tira pouquíssimas seções do Brasil).
  D2. Variáveis de pareamento: f1 = 100 L1/(L1+R1); outros = 100 O1/(L1+R1+O1), fatia dos outros candidatos nos votos
      válidos para presidente no 1º turno; bn = 100 (B1+N1)/C1, branco e nulo do 1º turno sobre o comparecimento do
      1º turno (o registro não diz o turno; no 2º turno "outros" é zero, então a composição é a do 1º turno, como na
      conferência do L7); dc = 100 (C2/A2 - C1/A1), em pontos dos aptos, cada turno com os seus aptos.
  D3. Padronização: média e desvio-padrão, sem peso, das candidatas a par do Brasil inteiro (D1). Os mesmos valores
      valem em todas as variantes (inclusive nas robustez de urna antiga e de capital), para que a métrica não mude e só
      mude o conjunto de candidatas.
  D4. Pares: as K candidatas de menor distância euclidiana, com reposição (a mesma seção do Brasil pode ser par de várias
      seções do exterior); empate desfeito pela ordem da chave UF|mun|zona|seção. Sem caliper.
  D5. Virada y = 100 L2/(L2+R2) - 100 L1/(L1+R1). Contrafactual de cada seção i do exterior: m_i = média da virada dos
      seus K pares ponderada pelo L2+R2 de cada par. D = soma de w_i (y_i - m_i) / soma de w_i, com w_i = L2+R2 da
      seção do exterior. (Leitura: a virada média do exterior, ponderada, menos a virada média dos pares, com cada
      conjunto de pares pesando o que pesa a sua seção do exterior.)
  D6. Bootstrap: cidade = código de município da seção do exterior. 2.000 réplicas, semente 20261103 (numpy
      default_rng), cidades sorteadas com reposição; os pares ficam fixos (o pareamento não é refeito em cada réplica).
      ep = desvio-padrão das réplicas (ddof 1); intervalo de 95% pelos percentis 2,5 e 97,5. Os mesmos sorteios em todas
      as variantes de 2026.
  D7. Leitura: "a mais de 4 erros-padrão" = |D| > 4 ep. SINAL: D <= -1,5 e |D| > 4 ep. SEM SINAL: |D| < 0,5 e
      ep <= 0,25. O resto: INCONCLUSIVO. O veredito vem só da especificação principal (Brasil inteiro, 4 variáveis,
      20 pares); a robustez é relatada com a leitura pelo mesmo critério e não muda o veredito.
  D8. Fração do desvio: -D / 1,79 (1,79 = margem / (2 x votos dos finalistas no 2º turno), régua do L7). Também com a
      régua recalculada da base.
  D9. Robustez registrada: (a) candidatas só com urna do 2º turno UE2013 ou UE2015 pelas faixas do F4
      (resultados/F4_modelo_urna.json, faixas.limites_usados, o classificador do F4, do F10 e do F18); (b) candidatas só
      das 27 capitais, código pelo NM_MUNICIPIO do bweb do 2º turno, sem acento, uma capital por UF (lista do T16);
      (c) sem dc (3 variáveis, mesma padronização das outras três); (d) 10 e 50 pares.
Descritivo fora do registro (não muda o veredito):
  E1. Equilíbrio: média ponderada das 4 variáveis no exterior e nos pares (pela mesma conta do D5), diferença em
      desvios-padrão do D3; distância ao K-ésimo par (mediana, p90, máximo).
  E2. Ajuste por regressão, como na conferência do L7: MQO ponderado por L2+R2 nas candidatas do Brasil, y sobre as 4
      variáveis (linear; e de 2º grau com quadrados e produtos); resíduo médio ponderado do exterior, ep pelo mesmo
      bootstrap de cidades (ajuste do Brasil fixo). Pareamento com correção de viés (Abadie e Imbens) pelo modelo linear.
  E3. Sem as seções do exterior sem horário de abertura no 2º turno; por modelo da urna do exterior (faixas do F4); por
      cidade (as 10 com mais votos nos finalistas); tirando uma cidade de cada vez (mínimo e máximo de D).
  E4. Biometria: fração QT_ELEI_BIOM_SEM_HABILITACAO / comparecimento (bweb do 2º turno) no exterior e nos pares.
  E5. Mesma conta (D1 a D6, 20 pares) em 2022 e 2018, com a fatia do candidato do PT (L na base). Só descrição: pelo
      Adendo 18 nenhuma eleição anterior é régua; se o mesmo mecanismo rodasse em todas, a diferença seria a mesma.
  E6. Suporte comum: D só nas seções do exterior cujo 20º par está a até 0,25 e a até 0,5 desvio-padrão.
  E7. PÓS-HOC, acrescentado DEPOIS de ver o resultado principal e a lista de D por cidade (não é registro, não é
      critério, só ajuda a ler): D de todas as cidades; quantas cidades e quanto do peso têm D negativo; D sem as 3
      cidades do Japão com seção no piso (TÓQUIO, NAGÓIA, HAMAMATSU), que destoaram na lista; D por terço da fatia de
      Lula no 1º turno das seções do exterior (cortes pelos tercis ponderados por w); votos que D moveria no país se
      fosse todo desvio de programa (-D/100 x votos dos finalistas do Brasil) e a margem que sobraria.

Uso: python3 -I analisar_F19.py <secoes2026.json.gz> <zips2t_dir> <F4_modelo_urna.json> <secoes2022.json.gz|->
                                <secoes2018.json.gz|-> <saida.json> <saida.txt>
"""
import os as _os, sys as _sys
_sys.path.insert(0, _os.path.dirname(_os.path.abspath(__file__)))
import collections, gc, glob, json, os, sys, time, unicodedata, zipfile
from multiprocessing import Pool
import numpy as np
from lib import carregar

PISO = 30
K_PRINC = 20
NBOOT, SEMENTE = 2000, 20261103
REGUA = 1.79
CAPITAIS = {'AC': 'RIO BRANCO', 'AL': 'MACEIO', 'AP': 'MACAPA', 'AM': 'MANAUS', 'BA': 'SALVADOR', 'CE': 'FORTALEZA',
            'DF': 'BRASILIA', 'ES': 'VITORIA', 'GO': 'GOIANIA', 'MA': 'SAO LUIS', 'MT': 'CUIABA', 'MS': 'CAMPO GRANDE',
            'MG': 'BELO HORIZONTE', 'PA': 'BELEM', 'PB': 'JOAO PESSOA', 'PR': 'CURITIBA', 'PE': 'RECIFE',
            'PI': 'TERESINA', 'RJ': 'RIO DE JANEIRO', 'RN': 'NATAL', 'RS': 'PORTO ALEGRE', 'RO': 'PORTO VELHO',
            'RR': 'BOA VISTA', 'SC': 'FLORIANOPOLIS', 'SP': 'SAO PAULO', 'SE': 'ARACAJU', 'TO': 'PALMAS'}
VARS = ['f1', 'outros', 'bn', 'dc']


def log(msg):
    print(time.strftime('%H:%M:%S'), msg, flush=True)


def sem_acento(s):
    return ''.join(ch for ch in unicodedata.normalize('NFD', s) if unicodedata.category(ch) != 'Mn').upper().strip()


# ------------------------------------------------------------------------------------------------ bweb do 2º turno
def ler_zip(zpath):
    """Nome do município e, por seção, (QT_ELEI_BIOM_SEM_HABILITACAO, QT_COMPARECIMENTO) das linhas de presidente."""
    z = zipfile.ZipFile(zpath)
    nome = [n for n in z.namelist() if n.lower().endswith('.csv')][0]
    muns, sec = {}, {}
    pres = b';1;"Presidente";'
    with z.open(nome) as fh:
        cab = [c.strip().strip('"') for c in fh.readline().decode('latin1').strip().split(';')]
        ix = {c: i for i, c in enumerate(cab)}
        for linha in fh:
            if pres not in linha:
                continue
            p = [x.strip('"') for x in linha.decode('latin1').rstrip('\r\n').split(';')]
            uf, m = p[ix['SG_UF']], int(p[ix['CD_MUNICIPIO']])
            k = f"{uf}|{m}|{int(p[ix['NR_ZONA']])}|{int(p[ix['NR_SECAO']])}"
            muns[(uf, m)] = p[ix['NM_MUNICIPIO']]
            if k not in sec:
                sec[k] = (int(p[ix['QT_ELEI_BIOM_SEM_HABILITACAO']]), int(p[ix['QT_COMPARECIMENTO']]))
    return muns, sec


def ler_bweb(zdir):
    zips = sorted(glob.glob(os.path.join(zdir, '*.zip')))
    with Pool(min(4, len(zips))) as P:
        partes = P.map(ler_zip, zips)
    muns, sec = {}, {}
    for m, s in partes:
        muns.update(m); sec.update(s)
    return muns, sec, [os.path.basename(z) for z in zips]


def codigos_capitais(muns):
    cod = {}
    for uf, nome in CAPITAIS.items():
        ach = {m for (u, m), n in muns.items() if u == uf and sem_acento(n) == nome}
        if len(ach) != 1:
            raise SystemExit(f'capital de {uf} não identificada: {ach}')
        cod[uf] = ach.pop()
    return cod


# ------------------------------------------------------------------------------------------------ faixas do F4
def faixas_F4(f4json):
    """Classificador do F4, do F10 e do F18."""
    with open(f4json) as f:
        F = json.load(f)['faixas']
    lim = F['limites_usados']; fx = F['faixas']
    minimo, maximo = lim[0][0], lim[-1][1]

    def mod(u):
        if u is None or u < minimo or u > maximo:
            return None
        for f_ in fx:
            if f_['corte_superior'] is None or u < f_['corte_superior']:
                return f_['modelo']
        return None
    return mod, lim


# ------------------------------------------------------------------------------------------------ montagem
def montar(d, mod=None):
    """Arrays das seções do D1, em ordem de chave. Devolve dicionário de arrays."""
    ks, rows = [], []
    for k in sorted(d):
        v = d[k]
        a, b = v.get('1'), v.get('2')
        if not a or not b:
            continue
        if a['comp'] <= 0 or b['comp'] <= 0 or a['L'] + a['R'] <= 0 or b['L'] + b['R'] <= 0:
            continue
        if a['apt'] <= 0 or b['apt'] <= 0:
            continue
        ks.append(k)
        rows.append((a['L'], a['R'], a['O'], a['B'] + a['N'], a['comp'], a['apt'],
                     b['L'], b['R'], b['comp'], b['apt'], b['urna'] if isinstance(b.get('urna'), int) else -1,
                     1 if str(b.get('ab', '')).strip() not in ('', '#NULO#') else 0))
    A = np.array(rows, float)
    L1, R1, O1, BN1, C1, A1, L2, R2, C2, A2, urna, temab = A.T
    out = {'k': np.array(ks), 'uf': np.array([k.split('|')[0] for k in ks]),
           'mun': np.array([int(k.split('|')[1]) for k in ks]),
           'f1': 100 * L1 / (L1 + R1), 'outros': 100 * O1 / (L1 + R1 + O1), 'bn': 100 * BN1 / C1,
           'dc': 100 * (C2 / A2 - C1 / A1), 'w': L2 + R2, 'L2': L2, 'R2': R2, 'urna': urna.astype(np.int64),
           'temab': temab.astype(bool), 'C2': C2}
    out['y'] = 100 * L2 / (L2 + R2) - out['f1']
    if mod is not None:
        out['mod'] = np.array([str(mod(int(u)) if u > 0 else None) for u in out['urna']])
    return out


def sub(T, m):
    return {c: v[m] for c, v in T.items()}


# ------------------------------------------------------------------------------------------------ pareamento
def vizinhos(Zb, Ze, K):
    """K candidatas de menor distância para cada linha de Ze; empate pela ordem do índice (ordem da chave)."""
    Ne = Ze.shape[0]
    idx = np.empty((Ne, K), np.int64); dist = np.empty((Ne, K))
    for i in range(Ne):
        dd = ((Zb - Ze[i]) ** 2).sum(1)
        t = np.partition(dd, K - 1)[K - 1]
        cand = np.flatnonzero(dd <= t)
        o = cand[np.lexsort((cand, dd[cand]))][:K]
        idx[i] = o; dist[i] = np.sqrt(dd[o])
    return idx, dist


def contrafactual(B, idx, campo='y'):
    wj = B['w'][idx]
    return (wj * B[campo][idx]).sum(1) / wj.sum(1)


def sorteios(G, semente=SEMENTE, n=NBOOT):
    rng = np.random.default_rng(semente)
    C = np.zeros((n, G))
    for r in range(n):
        C[r] = np.bincount(rng.integers(0, G, G), minlength=G)
    return C


def estimar(E, dif, cidades, C):
    """D ponderado e bootstrap de cidades (pares fixos). dif = y_i - m_i."""
    w = E['w']
    D = float((w * dif).sum() / w.sum())
    pos = {c: j for j, c in enumerate(cidades)}
    g = np.array([pos[c] for c in E['mun']])
    S = np.bincount(g, weights=w * dif, minlength=len(cidades))
    W = np.bincount(g, weights=w, minlength=len(cidades))
    num, den = C @ S, C @ W
    ok = den > 0
    bs = num[ok] / den[ok]
    ep = float(bs.std(ddof=1))
    return {'D': D, 'ep': ep, 'z': D / ep if ep > 0 else None, 'ic95_percentil': [float(np.percentile(bs, 2.5)), float(np.percentile(bs, 97.5))],
            'replicas_validas': int(ok.sum()), 'secoes_exterior': int(len(w)), 'cidades_com_secao': int((W > 0).sum()),
            'votos_finalistas_exterior': int(w.sum())}


def ler(r):
    D, ep = r['D'], r['ep']
    if D <= -1.5 and abs(D) > 4 * ep:
        return 'SINAL'
    if abs(D) < 0.5 and ep <= 0.25:
        return 'SEM SINAL'
    return 'INCONCLUSIVO'


def padronizar(B, cols):
    X = np.column_stack([B[c] for c in cols])
    mu, sd = X.mean(0), X.std(0, ddof=1)
    return mu, sd


def Z(T, cols, mu, sd):
    return (np.column_stack([T[c] for c in cols]) - mu) / sd


def rodar(E, B, cols, mu, sd, K, cidades, C, extra=None):
    """Pareamento, D, bootstrap, equilíbrio e qualidade."""
    idx, dist = vizinhos(Z(B, cols, mu, sd), Z(E, cols, mu, sd), K)
    m = contrafactual(B, idx)
    dif = E['y'] - m
    r = estimar(E, dif, cidades, C)
    w = E['w']
    r['virada_exterior'] = float((w * E['y']).sum() / w.sum())
    r['virada_pares'] = float((w * m).sum() / w.sum())
    r['leitura_pelo_criterio'] = ler(r)
    r['fracao_da_regua_1_79'] = -r['D'] / REGUA
    r['K'] = K; r['variaveis'] = list(cols); r['candidatas'] = int(len(B['w']))
    r['secoes_do_brasil_distintas_usadas'] = int(len(np.unique(idx)))
    eq = {}
    for c in VARS:
        mp = contrafactual(B, idx, c)
        me = float((w * E[c]).sum() / w.sum()); mpp = float((w * mp).sum() / w.sum())
        eq[c] = {'exterior': me, 'pares': mpp, 'dif_em_dp': (me - mpp) / float(sd_global[c])}
    r['equilibrio'] = eq
    dk = dist[:, -1]
    r['distancia_ao_ultimo_par'] = {'mediana': float(np.median(dk)), 'p90': float(np.percentile(dk, 90)), 'max': float(dk.max())}
    return r, idx, dist, dif


sd_global = {}


def main():
    arq26, zdir, f4json, arq22, arq18, saida_json, saida_txt = sys.argv[1:8]
    mod, lim = faixas_F4(f4json)
    d = carregar(arq26)
    log(f'base 2026: {len(d)} seções')
    L2t = sum(v['2']['L'] for v in d.values() if v.get('2')); R2t = sum(v['2']['R'] for v in d.values() if v.get('2'))
    regua_base = 100 * ((L2t - R2t) / 2) / (L2t + R2t)
    T = montar(d, mod)
    n_ext_total = int(sum(1 for k in d if k.startswith('ZZ|')))
    del d; gc.collect()
    muns, bw, zips = ler_bweb(zdir)
    log(f'bweb 2º turno: {len(bw)} seções, {len(muns)} municípios')
    cap = codigos_capitais(muns)
    ext = T['uf'] == 'ZZ'
    piso = T['w'] >= PISO
    E = sub(T, ext & piso); B = sub(T, (~ext) & piso)
    cont = {'secoes_exterior_na_base': n_ext_total, 'exterior_dois_turnos_validos': int(ext.sum()),
            'exterior_com_piso_30': int((ext & piso).sum()), 'brasil_dois_turnos_validos': int((~ext).sum()),
            'brasil_com_piso_30': int(((~ext) & piso).sum())}
    log(json.dumps(cont))
    mu, sd = padronizar(B, VARS)
    for c, s in zip(VARS, sd):
        sd_global[c] = s
    pad = {c: {'media': float(a), 'dp': float(b)} for c, a, b in zip(VARS, mu, sd)}
    cidades = sorted(set(E['mun'].tolist()))
    C = sorteios(len(cidades))
    nome_cid = {c: f"{muns.get(('ZZ', c), '?')} ({c})" for c in cidades}

    # ---------------- principal (com 50 pares, de onde saem 10 e 20 por prefixo, D4)
    idx50, dist50 = vizinhos(Z(B, VARS, mu, sd), Z(E, VARS, mu, sd), 50)
    res = {}
    for K in (20, 10, 50):
        idx, dist = idx50[:, :K], dist50[:, :K]
        m = contrafactual(B, idx); dif = E['y'] - m
        r = estimar(E, dif, cidades, C)
        w = E['w']
        r['virada_exterior'] = float((w * E['y']).sum() / w.sum()); r['virada_pares'] = float((w * m).sum() / w.sum())
        r['leitura_pelo_criterio'] = ler(r); r['fracao_da_regua_1_79'] = -r['D'] / REGUA
        r['fracao_da_regua_base'] = -r['D'] / regua_base
        r['K'] = K; r['variaveis'] = VARS; r['candidatas'] = int(len(B['w']))
        r['secoes_do_brasil_distintas_usadas'] = int(len(np.unique(idx)))
        eq = {}
        for c in VARS:
            mp = contrafactual(B, idx, c)
            me = float((w * E[c]).sum() / w.sum()); mpp = float((w * mp).sum() / w.sum())
            eq[c] = {'exterior': me, 'pares': mpp, 'dif_em_dp': (me - mpp) / float(sd_global[c])}
        r['equilibrio'] = eq
        dk = dist[:, -1]
        r['distancia_ao_ultimo_par'] = {'mediana': float(np.median(dk)), 'p90': float(np.percentile(dk, 90)), 'max': float(dk.max())}
        res[K] = (r, idx, dist, dif)
    P, idxP, distP, difP = res[20]
    log(f"principal: D {P['D']:.3f} ep {P['ep']:.3f} -> {P['leitura_pelo_criterio']}")

    # ---------------- robustez registrada
    rob = {}
    antiga = np.isin(B['mod'], ['UE2013', 'UE2015'])
    rob['a_so_urna_antiga'] = rodar(E, sub(B, antiga), VARS, mu, sd, 20, cidades, C)[0]
    capm = np.array([cap.get(u) == m for u, m in zip(B['uf'], B['mun'])])
    rob['b_so_capitais'] = rodar(E, sub(B, capm), VARS, mu, sd, 20, cidades, C)[0]
    j3 = [VARS.index(c) for c in ('f1', 'outros', 'bn')]
    rob['c_sem_variacao_comparecimento'] = rodar(E, B, ['f1', 'outros', 'bn'], mu[j3], sd[j3], 20, cidades, C)[0]
    rob['d_10_pares'] = res[10][0]
    rob['d_50_pares'] = res[50][0]
    for kk, r in rob.items():
        r['fracao_da_regua_base'] = -r['D'] / regua_base
        log(f"{kk}: D {r['D']:.3f} ep {r['ep']:.3f} -> {r['leitura_pelo_criterio']}")

    # ---------------- descritivos
    desc = {}
    # E2: regressão nas seções do Brasil
    w = E['w']

    def desenho(T_, grau):
        X = np.column_stack([T_[c] for c in VARS])
        cols = [np.ones(len(X))] + [X[:, j] for j in range(4)]
        if grau == 2:
            for a in range(4):
                for b in range(a, 4):
                    cols.append(X[:, a] * X[:, b])
        return np.column_stack(cols)
    reg = {}
    mu_lin_B = mu_lin_E = None
    for grau in (1, 2):
        XB = desenho(B, grau); sw = np.sqrt(B['w'])
        beta = np.linalg.lstsq(XB * sw[:, None], B['y'] * sw, rcond=None)[0]
        predE = desenho(E, grau) @ beta
        rr = estimar(E, E['y'] - predE, cidades, C)
        rr['previsto_exterior'] = float((w * predE).sum() / w.sum())
        rr['coeficientes'] = beta.tolist()
        reg['linear' if grau == 1 else 'segundo_grau'] = rr
        if grau == 1:
            mu_lin_B, mu_lin_E = XB @ beta, predE
    # correção de viés do pareamento (Abadie e Imbens), modelo linear
    Btmp = dict(B); Btmp['mulin'] = mu_lin_B
    mpar = contrafactual(Btmp, idxP, 'mulin')
    reg['pareamento_com_correcao_de_vies'] = estimar(E, difP - (mu_lin_E - mpar), cidades, C)
    desc['E2_regressao'] = reg
    # E3
    e3 = {}
    sel = E['temab']
    e3['sem_secoes_sem_horario_de_abertura'] = dict(estimar(sub(E, sel), difP[sel], cidades, C), excluidas=int((~sel).sum()))
    por_mod = {}
    for mo in sorted(set(E['mod'].tolist())):
        s = E['mod'] == mo
        por_mod[mo] = estimar(sub(E, s), difP[s], cidades, C)
    e3['por_modelo_da_urna_do_exterior'] = por_mod
    Wc = collections.Counter()
    for c, ww in zip(E['mun'], w):
        Wc[int(c)] += ww
    top = [c for c, _ in Wc.most_common(10)]
    pc = {}
    for c in top:
        s = E['mun'] == c
        pc[nome_cid[c]] = {'codigo': c, 'secoes': int(s.sum()), 'votos_finalistas': int(w[s].sum()),
                           'virada_exterior': float((w[s] * E['y'][s]).sum() / w[s].sum()),
                           'D': float((w[s] * difP[s]).sum() / w[s].sum()),
                           'f1_media': float((w[s] * E['f1'][s]).sum() / w[s].sum())}
    e3['por_cidade_10_maiores'] = pc
    loo = {}
    for c in cidades:
        s = E['mun'] != c
        loo[nome_cid[c]] = float((w[s] * difP[s]).sum() / w[s].sum())
    vmin = min(loo, key=loo.get); vmax = max(loo, key=loo.get)
    e3['tirando_uma_cidade'] = {'D_minimo': loo[vmin], 'sem_a_cidade_min': vmin, 'D_maximo': loo[vmax], 'sem_a_cidade_max': vmax}
    desc['E3'] = e3
    # E4: biometria
    def frac_sem(keys):
        num = den = 0
        for k in keys:
            t = bw.get(k)
            if t:
                num += t[0]; den += t[1]
        return num / den if den else None
    kp = B['k'][np.unique(idxP)]
    desc['E4_biometria'] = {'exterior_sem_habilitacao_sobre_comparecimento': frac_sem(E['k']),
                            'pares_sem_habilitacao_sobre_comparecimento': frac_sem(kp),
                            'brasil_candidatas_sem_habilitacao_sobre_comparecimento': frac_sem(B['k']),
                            'exterior_linhas_com_campo_positivo': int(sum(1 for k in E['k'] if bw.get(k, (0, 0))[0] > 0))}
    # E6: suporte comum
    e6 = {}
    for lim_ in (0.25, 0.5):
        s = distP[:, -1] <= lim_
        e6[str(lim_)] = estimar(sub(E, s), difP[s], cidades, C) if s.sum() else {'secoes_exterior': 0}
    desc['E6_suporte_comum'] = e6
    # E7: pós-hoc (depois de ver o resultado)
    e7 = {'aviso': 'pós-hoc, calculado depois de ver o resultado principal; não é registro nem critério'}
    todas = []
    for c in cidades:
        s = E['mun'] == c
        todas.append({'cidade': nome_cid[c], 'secoes': int(s.sum()), 'votos_finalistas': int(w[s].sum()),
                      'D': float((w[s] * difP[s]).sum() / w[s].sum()), 'virada': float((w[s] * E['y'][s]).sum() / w[s].sum()),
                      'f1': float((w[s] * E['f1'][s]).sum() / w[s].sum()), 'dc': float((w[s] * E['dc'][s]).sum() / w[s].sum())})
    todas.sort(key=lambda x: -x['votos_finalistas'])
    e7['cidades'] = todas
    e7['cidades_com_D_negativo'] = sum(1 for x in todas if x['D'] < 0)
    e7['cidades_total'] = len(todas)
    e7['peso_com_D_negativo'] = sum(x['votos_finalistas'] for x in todas if x['D'] < 0) / sum(x['votos_finalistas'] for x in todas)
    japao = {c for c in cidades if muns.get(('ZZ', c), '') in ('TÓQUIO', 'NAGÓIA', 'HAMAMATSU')}
    sj = ~np.isin(E['mun'], list(japao))
    e7['sem_japao'] = dict(estimar(sub(E, sj), difP[sj], cidades, C), cidades_tiradas=sorted(nome_cid[c] for c in japao))
    sjp = ~sj
    e7['so_japao'] = {'secoes': int(sjp.sum()), 'D': float((w[sjp] * difP[sjp]).sum() / w[sjp].sum())}
    o_ = np.argsort(E['f1']); cw = np.cumsum(w[o_]) / w.sum()
    t1 = float(E['f1'][o_][np.searchsorted(cw, 1 / 3)]); t2 = float(E['f1'][o_][np.searchsorted(cw, 2 / 3)])
    terc = {}
    for nome_t, s in (('f1 abaixo de ' + fz(t1, 1), E['f1'] < t1), ('f1 de ' + fz(t1, 1) + ' a ' + fz(t2, 1), (E['f1'] >= t1) & (E['f1'] < t2)),
                      ('f1 de ' + fz(t2, 1) + ' ou mais', E['f1'] >= t2)):
        terc[nome_t] = dict(estimar(sub(E, s), difP[s], cidades, C), virada_exterior=float((w[s] * E['y'][s]).sum() / w[s].sum()),
                            virada_pares=float((w[s] * (E['y'][s] - difP[s])).sum() / w[s].sum()))
    e7['por_terco_da_fatia_de_lula_1t'] = terc
    VB = float(B['w'].sum())
    e7['escala'] = {}
    for nome_s, Dv in (('D', P['D']), ('IC95_inferior', P['ic95_percentil'][0])):
        mov = -Dv / 100 * VB
        e7['escala'][nome_s] = {'pontos': Dv, 'votos_movidos_no_brasil': mov, 'margem_que_sobraria': (L2t - R2t) - 2 * mov}
    desc['E7_pos_hoc'] = e7
    # brutos
    desc['brutos'] = {'virada_exterior': P['virada_exterior'],
                      'virada_brasil_candidatas': float((B['w'] * B['y']).sum() / B['w'].sum()),
                      'f1_exterior': float((w * E['f1']).sum() / w.sum()), 'f1_brasil': float((B['w'] * B['f1']).sum() / B['w'].sum()),
                      'dc_exterior': float((w * E['dc']).sum() / w.sum()), 'dc_brasil': float((B['w'] * B['dc']).sum() / B['w'].sum()),
                      'outros_exterior': float((w * E['outros']).sum() / w.sum()), 'outros_brasil': float((B['w'] * B['outros']).sum() / B['w'].sum()),
                      'bn_exterior': float((w * E['bn']).sum() / w.sum()), 'bn_brasil': float((B['w'] * B['bn']).sum() / B['w'].sum())}
    del T, B; gc.collect()

    # E5: 2022 e 2018
    e5 = {}
    for ano, arq in (('2022', arq22), ('2018', arq18)):
        if arq == '-' or not os.path.exists(arq):
            continue
        dd = carregar(arq)
        L2a = sum(v['2']['L'] for v in dd.values() if v.get('2')); R2a = sum(v['2']['R'] for v in dd.values() if v.get('2'))
        Ta = montar(dd)
        del dd; gc.collect()
        exa = Ta['uf'] == 'ZZ'; pa = Ta['w'] >= PISO
        Ea = sub(Ta, exa & pa); Ba = sub(Ta, (~exa) & pa)
        mua, sda = padronizar(Ba, VARS)
        cid_a = sorted(set(Ea['mun'].tolist()))
        Ca = sorteios(len(cid_a))
        sd_bak = dict(sd_global)
        for c, s in zip(VARS, sda):
            sd_global[c] = s
        ra = rodar(Ea, Ba, VARS, mua, sda, 20, cid_a, Ca)[0]
        sd_global.clear(); sd_global.update(sd_bak)
        ra['fatia_L_2t_nacional'] = 100 * L2a / (L2a + R2a)
        ra['virada_brasil_candidatas'] = float((Ba['w'] * Ba['y']).sum() / Ba['w'].sum())
        ra['secoes_exterior_com_piso'] = int(len(Ea['w']))
        e5[ano] = ra
        log(f"{ano}: D {ra['D']:.3f} ep {ra['ep']:.3f}")
        del Ta, Ea, Ba; gc.collect()
    desc['E5_outros_anos'] = e5

    out = {'teste': 'F19 do Adendo 23 (H1): exterior sem biometria contra seções do Brasil pareadas',
           'registro': 'PRE-REGISTRO-2026-10-26.md, Adendo 23, commit 863a34e (03/11/2026 01:13:05 UTC)',
           'veredito': P['leitura_pelo_criterio'],
           'criterio': {'sinal': 'D <= -1,5 e |D| > 4 ep', 'sem_sinal': '|D| < 0,5 e ep <= 0,25', 'resto': 'INCONCLUSIVO'},
           'regua': {'registrada': REGUA, 'recalculada_da_base': regua_base, 'margem': int(L2t - R2t), 'votos_finalistas_2t': int(L2t + R2t)},
           'conferencia_L7': {'D': -0.76, 'ep': 0.15, 'fracao_da_regua': 0.76 / REGUA,
                              'fonte': 'resultados/testes_adendo18_com_conferencia.json, correções apontadas pelas conferências (L7)'},
           'contagens': cont, 'padronizacao': pad, 'capitais': cap, 'faixas_F4': lim, 'zips_2t': zips,
           'bootstrap': {'replicas': NBOOT, 'semente': SEMENTE, 'cidades': len(cidades)},
           'principal': P, 'robustez_registrada': rob, 'descritivo_fora_do_registro': desc}
    with open(saida_json, 'w') as f:
        json.dump(out, f, ensure_ascii=False, indent=1, default=lambda o: o.item() if hasattr(o, 'item') else str(o))
    escrever_txt(out, saida_txt)
    log(f'gravado {saida_json} e {saida_txt}')


# ------------------------------------------------------------------------------------------------ texto
def fz(x, c=2):
    if x is None:
        return 'n/d'
    s = f'{x:,.{c}f}'
    return s.replace(',', 'X').replace('.', ',').replace('X', '.')


def fi(x):
    return f'{int(x):,}'.replace(',', '.')


def pct(x, c=0):
    return fz(100 * x, c) + '%'


def linha_r(nome, r):
    return (f"  {nome}: D {fz(r['D'])} (ep {fz(r['ep'])}; z {fz(r['z'], 1)}; IC 95% {fz(r['ic95_percentil'][0])} a {fz(r['ic95_percentil'][1])}); "
            f"exterior {fz(r['virada_exterior'])}, pares {fz(r['virada_pares'])}; candidatas {fi(r['candidatas'])}; "
            f"fração da régua {pct(r['fracao_da_regua_1_79'])}; leitura pelo critério: {r['leitura_pelo_criterio']}")


def escrever_txt(o, caminho):
    L = []; w = L.append
    P = o['principal']; R = o['robustez_registrada']; Dd = o['descritivo_fora_do_registro']; c = o['contagens']
    w('F19 do Adendo 23 (H1 da caça ao furo): o exterior, sem biometria, contra seções do Brasil de composição igual')
    w(f"Registro: {o['registro']}. Script: scripts/analisar_F19.py.")
    w('')
    w(f"VEREDITO PELA LETRA: {o['veredito']}")
    w(f"  D = {fz(P['D'])} ponto (ep {fz(P['ep'])} por bootstrap de {o['bootstrap']['cidades']} cidades do exterior, {fi(o['bootstrap']['replicas'])} réplicas,"
      f" semente {o['bootstrap']['semente']}; z {fz(P['z'], 1)}; IC 95% {fz(P['ic95_percentil'][0])} a {fz(P['ic95_percentil'][1])}).")
    w(f"  Critério: sinal se D <= -1,5 a mais de 4 ep; sem sinal se |D| < 0,5 com ep <= 0,25; entre os dois, inconclusivo.")
    w(f"  Fração do desvio de 1,79 ponto que D representa: {pct(P['fracao_da_regua_1_79'])} (régua recalculada da base:"
      f" {fz(o['regua']['recalculada_da_base'], 3)}; fração {pct(P['fracao_da_regua_base'])}).")
    cf = o['conferencia_L7']
    w(f"  Conferência do L7 (ajuste por regressão): {fz(cf['D'])} (ep {fz(cf['ep'])}), {pct(cf['fracao_da_regua'])} da régua.")
    w('')
    w('1. Universo')
    w(f"  Exterior: {fi(c['secoes_exterior_na_base'])} seções na base; {fi(c['exterior_dois_turnos_validos'])} com os dois turnos válidos;"
      f" {fi(c['exterior_com_piso_30'])} com 30 ou mais votos nos finalistas no 2º turno ({fi(P['votos_finalistas_exterior'])} votos, {P['cidades_com_secao']} cidades).")
    w(f"  Brasil (candidatas a par): {fi(c['brasil_dois_turnos_validos'])} seções com os dois turnos válidos; {fi(c['brasil_com_piso_30'])} com o piso de 30.")
    w('  Padronização (média e desvio-padrão sem peso das candidatas): ' + '; '.join(f"{k} {fz(v['media'])} ({fz(v['dp'])})" for k, v in o['padronizacao'].items()))
    w('')
    w('2. Especificação principal (4 variáveis, 20 pares, Brasil inteiro)')
    w(linha_r('principal', P))
    w(f"  Seções distintas do Brasil usadas como par: {fi(P['secoes_do_brasil_distintas_usadas'])}."
      f" Distância ao 20º par (em desvios-padrão): mediana {fz(P['distancia_ao_ultimo_par']['mediana'], 3)},"
      f" p90 {fz(P['distancia_ao_ultimo_par']['p90'], 3)}, máximo {fz(P['distancia_ao_ultimo_par']['max'], 3)}.")
    w('  Equilíbrio (exterior x pares, média ponderada; diferença em desvios-padrão): ' + '; '.join(
        f"{k} {fz(v['exterior'])} x {fz(v['pares'])} ({fz(v['dif_em_dp'], 3)})" for k, v in P['equilibrio'].items()))
    w('')
    w('3. Robustez registrada (não muda o veredito)')
    nomes = {'a_so_urna_antiga': 'só urna antiga (UE2013/UE2015)', 'b_so_capitais': 'só capitais',
             'c_sem_variacao_comparecimento': 'sem a variação do comparecimento', 'd_10_pares': '10 pares', 'd_50_pares': '50 pares'}
    for kk, r in R.items():
        w(linha_r(nomes[kk], r))
        w('    equilíbrio: ' + '; '.join(f"{k} {fz(v['exterior'])} x {fz(v['pares'])} ({fz(v['dif_em_dp'], 2)})" for k, v in r['equilibrio'].items())
          + f"; distância ao último par: mediana {fz(r['distancia_ao_ultimo_par']['mediana'], 3)}, p90 {fz(r['distancia_ao_ultimo_par']['p90'], 3)}")
    w('')
    w('4. Descritivo fora do registro')
    b = Dd['brutos']
    w(f"  Brutos (ponderados por L2+R2): virada do exterior {fz(b['virada_exterior'])}, do Brasil {fz(b['virada_brasil_candidatas'])};"
      f" fatia de Lula no 1º turno: exterior {fz(b['f1_exterior'])}, Brasil {fz(b['f1_brasil'])}; variação do comparecimento: exterior {fz(b['dc_exterior'])}, Brasil {fz(b['dc_brasil'])} pontos dos aptos.")
    rg = Dd['E2_regressao']
    w(f"  E2. Ajuste por regressão nas seções do Brasil: linear {fz(rg['linear']['D'])} (ep {fz(rg['linear']['ep'])}), previsto {fz(rg['linear']['previsto_exterior'])};"
      f" 2º grau {fz(rg['segundo_grau']['D'])} (ep {fz(rg['segundo_grau']['ep'])}), previsto {fz(rg['segundo_grau']['previsto_exterior'])};"
      f" pareamento com correção de viés {fz(rg['pareamento_com_correcao_de_vies']['D'])} (ep {fz(rg['pareamento_com_correcao_de_vies']['ep'])}).")
    e3 = Dd['E3']
    s0 = e3['sem_secoes_sem_horario_de_abertura']
    w(f"  E3. Sem as {s0['excluidas']} seções do exterior sem horário de abertura: D {fz(s0['D'])} (ep {fz(s0['ep'])}).")
    w('      Por modelo da urna do exterior: ' + '; '.join(f"{m} D {fz(r['D'])} (ep {fz(r['ep'])}, {fi(r['secoes_exterior'])} seções)" for m, r in e3['por_modelo_da_urna_do_exterior'].items()))
    w('      10 cidades com mais votos: ' + '; '.join(f"{n} {fi(x['secoes'])} seções, virada {fz(x['virada_exterior'])}, D {fz(x['D'])}, Lula 1º turno {fz(x['f1_media'], 1)}"
                                                    for n, x in e3['por_cidade_10_maiores'].items()))
    t = e3['tirando_uma_cidade']
    w(f"      Tirando uma cidade de cada vez: D de {fz(t['D_minimo'])} (sem {t['sem_a_cidade_min']}) a {fz(t['D_maximo'])} (sem {t['sem_a_cidade_max']}).")
    e4 = Dd['E4_biometria']
    w(f"  E4. Liberações sem biometria (QT_ELEI_BIOM_SEM_HABILITACAO / comparecimento, 2º turno): exterior {pct(e4['exterior_sem_habilitacao_sobre_comparecimento'], 2)}"
      f" ({e4['exterior_linhas_com_campo_positivo']} seções com campo positivo); pares {pct(e4['pares_sem_habilitacao_sobre_comparecimento'], 2)};"
      f" Brasil {pct(e4['brasil_candidatas_sem_habilitacao_sobre_comparecimento'], 2)}.")
    for lim_, r in Dd['E6_suporte_comum'].items():
        if r.get('secoes_exterior'):
            w(f"  E6. Só seções do exterior com o 20º par a até {lim_.replace('.', ',')} dp: {fi(r['secoes_exterior'])} seções, D {fz(r['D'])} (ep {fz(r['ep'])}).")
    for ano, r in Dd['E5_outros_anos'].items():
        w(f"  E5. {ano} (fatia do candidato do PT; Adendo 18: não é régua): D {fz(r['D'])} (ep {fz(r['ep'])}); exterior {fz(r['virada_exterior'])}, pares {fz(r['virada_pares'])},"
          f" Brasil {fz(r['virada_brasil_candidatas'])}; {fi(r['secoes_exterior_com_piso'])} seções do exterior; fatia nacional do PT no 2º turno {fz(r['fatia_L_2t_nacional'])};"
          f" equilíbrio: " + '; '.join(f"{k} {fz(v['dif_em_dp'], 2)}" for k, v in r['equilibrio'].items()))
    e7 = Dd['E7_pos_hoc']
    w('')
    w('5. PÓS-HOC (acrescentado depois de ver o resultado principal; não é registro nem critério)')
    w(f"  Cidades com D negativo: {e7['cidades_com_D_negativo']} de {e7['cidades_total']} ({pct(e7['peso_com_D_negativo'])} dos votos nos finalistas).")
    sj = e7['sem_japao']
    w(f"  Sem {', '.join(sj['cidades_tiradas'])}: D {fz(sj['D'])} (ep {fz(sj['ep'])}; {fi(sj['secoes_exterior'])} seções); só essas 3 cidades: D {fz(e7['so_japao']['D'])} ({e7['so_japao']['secoes']} seções).")
    w('  Por terço da fatia de Lula no 1º turno: ' + '; '.join(f"{n}: D {fz(r['D'])} (ep {fz(r['ep'])}), exterior {fz(r['virada_exterior'])}, pares {fz(r['virada_pares'])}, {fi(r['secoes_exterior'])} seções"
                                                          for n, r in e7['por_terco_da_fatia_de_lula_1t'].items()))
    for n, r in e7['escala'].items():
        w(f"  Escala, se {n} ({fz(r['pontos'])}) fosse todo desvio de programa nas seções do Brasil: {fi(r['votos_movidos_no_brasil'])} votos de Flávio para Lula;"
          f" a margem de Lula, sem eles, seria {fi(r['margem_que_sobraria'])} votos.")
    w('  Todas as cidades (votos nos finalistas, D, virada, fatia de Lula no 1º turno): ' + '; '.join(
        f"{x['cidade']} {fi(x['votos_finalistas'])} {fz(x['D'])} {fz(x['virada'])} {fz(x['f1'], 1)}" for x in e7['cidades']))
    w('')
    w('Desvios declarados: D1 a D9 e E1 a E6 do docstring do script, escritos antes de calcular qualquer virada pareada; E7 é pós-hoc.')
    txt = '\n'.join(L) + '\n'
    for ch in (chr(0x2014), chr(0x2013)):
        txt = txt.replace(ch, '-')
    with open(caminho, 'w') as f:
        f.write(txt)


if __name__ == '__main__':
    main()
