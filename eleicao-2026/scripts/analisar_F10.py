"""F10 do Adendo 21: urnas antigas, o mesmo desvio aparece nos outros cargos?

Registro (PRE-REGISTRO-2026-10-26.md, Adendo 21, commit 913af7a, 31/10/2026 10:36:29 UTC, antes de rodar):
  - Nos locais com urna antiga (UE2013 ou UE2015) e nova (UE2020 ou UE2022) no 1º turno: diferença antiga menos nova,
    dentro do local, na fatia de Lula entre os finalistas (presidente) e num índice de perfil feito só com os outros
    cargos do 1º turno (fatia da federação PT/PCdoB/PV nos válidos para deputado federal e para deputado estadual, e
    fatia do candidato a senador do campo de Lula, quando houver).
  - Escala: inclinação b da fatia de Lula sobre o índice, entre seções, dentro do local, nas seções desses locais.
    Estatística: D = (diferença no presidente) - b x (diferença no índice), erro por bootstrap de locais (2.000).
  - Sinal de máquina: D de +0,5 ponto ou mais a mais de 3 erros-padrão. Sem sinal: |D| abaixo de 0,3 com erro-padrão
    até 0,2. Entre os dois: inconclusivo.

O que já tinha sido visto antes de escrever este arquivo (transparência): o placebo do F4 (fatia de Lula no 1º turno,
urnas antigas contra UE2020 no mesmo local: UE2013 +0,852, ep 0,301; UE2015 +0,718, ep 0,295) e a exploração do F4 nos
123 locais que misturam antiga e nova (+0,75 no 1º turno). Nenhum número de deputado ou senador por modelo de urna foi
olhado antes de fixar as decisões abaixo. A lista de candidatos a senador do campo de Lula foi montada só com o cadastro
de candidaturas do TSE (sem votos), antes de ler o bweb dos outros cargos.

Decisões que o registro não fixa (tomadas antes de calcular qualquer diferença; cada uma é declarada como desvio):
  D1. Urna e modelo: NR_URNA_EFETIVADA do 1º turno (campo 'urna' do turno '1' em secoes2026.json.gz). Modelo pelas
      faixas do F4, lidas de resultados/F4_modelo_urna.json (faixas.limites_usados), com o mesmo classificador do F4:
      número abaixo do menor ou acima do maior da amostra de logs fica sem modelo e sai; número na zona de corte recebe
      o modelo do corte. Antiga = UE2013 ou UE2015; nova = UE2020 ou UE2022.
  D2. Local: UF|município|zona|local de votação do 1º turno (lib.chave_local com o registro do 1º turno).
  D3. Seções: Brasil (o exterior não vota para deputado nem senador e fica de fora), comparecimento do 1º turno acima de
      zero, L1+R1 acima de zero, válidos acima de zero nos três cargos (deputado federal, deputado estadual ou distrital,
      senador) e modelo definido. Local "com urna antiga e nova" = pelo menos uma seção antiga e uma nova entre as seções
      que passaram nesses filtros. Entram todas as seções desses locais. Sem limiar de votantes (o F10 não fixa; o de 20
      votantes do Adendo 11 entra como robustez).
  D4. Fatia de Lula no presidente: a do 1º turno, P = 100 x L1/(L1+R1). Motivo: o F10 compara a mesma urna, no mesmo
      dia, com os outros cargos do 1º turno, e o desvio de partida das urnas antigas visto no F4 é o do 1º turno. A fatia
      do 2º turno e a virada saem como leitura descritiva, fora do veredito.
  D5. Deputados: linhas CD_CARGO_PERGUNTA 6 (federal) e 7 (estadual) do bweb do 1º turno (zips de 05/10/2026, 14h03);
      no DF, o 8 (distrital) no lugar do estadual. Válidos = nominal (CD_TIPO_VOTAVEL 1) + legenda (4), como o bweb traz.
      Federação = nominal + legenda com NR_PARTIDO 13, 65 ou 43. Fatia em pontos.
  D6. Senador: em 2026 são duas vagas e cada eleitor dá dois votos. Candidato do campo de Lula = todo candidato a senador
      registrado pela coligação que inclui a Federação Brasil da Esperança (PT/PCdoB/PV) ou pela própria federação,
      segundo o cadastro de candidaturas do TSE (consulta_cand_2026, arquivo BRASIL, CD_CARGO 5: DS_COMPOSICAO_COLIGACAO
      contém "BRASIL DA ESPERAN" ou NR_FEDERACAO 101). Fatia = soma dos votos desses candidatos / votos nominais para
      senador (os dois votos de cada eleitor contam). Quando a coligação lançou dois, entram os dois: o registro fala em
      "o candidato", mas com duas vagas a coligação pode lançar dois e não há critério sem voto para escolher um. UF sem
      candidato pela regra: índice só com os deputados. Leitura alternativa (robustez): só candidatos de PT, PCdoB ou PV.
  D7. Índice de perfil I: média simples, em pontos, das fatias disponíveis (federal, estadual e senador).
  D8. Peso: votos dos finalistas no 1º turno (L1+R1), o mesmo nas três regressões. Sem covariáveis.
  D9. Diferença antiga menos nova: coeficiente do indicador "antiga" na regressão com efeito fixo de local (within
      ponderado), para P (dP) e para I (dI). b: coeficiente de I na regressão de P em I com efeito fixo de local, nas
      mesmas seções, sem o indicador (como está no registro). D = dP - b x dI.
  D10. Erro-padrão: bootstrap de locais, 2.000 réplicas, semente 20261031 (numpy default_rng): sorteio com reposição dos
      locais mistos, cada local sorteado como um grupo próprio; dP, dI, b e D recalculados juntos em cada réplica;
      ep = desvio-padrão das réplicas (ddof=1). Cálculo exato e rápido: com efeito fixo por local, os valores centrados
      de cada local não mudam na réplica, então cada estatística sai da soma, ponderada pelas contagens do sorteio, dos
      produtos cruzados de cada local. Conferência: os coeficientes da amostra inteira são refeitos com lib.fe_ols (CR1).
  D11. Veredito: SINAL DE MÁQUINA se D >= +0,5 e D > 3 x ep (a mais de 3 erros-padrão, lido a partir de zero). SEM
      SINAL se |D| < 0,3 e ep <= 0,2. Senão INCONCLUSIVO. O registro só chama de sinal o lado positivo (urna antiga mais
      Lula do que o perfil prevê); um D negativo grande seria INCONCLUSIVO pela letra e iria para as pistas.
  D12. Conferências do bweb (contadas e relatadas, sem tirar seções da principal): comparecimento de cada cargo igual ao
      do presidente; nominal + legenda + branco + nulo igual ao comparecimento nos deputados; nominal + branco + nulo
      igual a 2 x comparecimento no senador; tipos de voto fora de 1 a 4; candidatos do campo de Lula presentes no bweb
      com o partido do cadastro. Robustez sem as seções que falham alguma conferência.
  Robustez e leituras descritivas, fixadas agora e fora do veredito:
    R1. fatia de Lula no 2º turno e virada (2º menos 1º) no lugar de P, com o mesmo índice;
    R2. cada componente sozinho (federal, estadual, senador), índice só com deputados, senador só com PT/PCdoB/PV;
    R3. b com o indicador de urna antiga na mesma regressão (inclinação dentro do modelo; D vira o coeficiente da antiga);
    R4. sem peso;
    R5. só seções com 20 ou mais votantes no 1º turno (mistura recalculada);
    R6. faixas de scripts/modelos.py; sem as urnas da zona de corte;
    R7. só SP; sem SP;
    R8. atenuação de b: variável instrumental dentro do local (federal instrumentado pelo estadual, estadual pelo
        federal, média dos deputados pelo senador), D com a inclinação instrumentada;
    R9. calibração do método onde não há urna antiga com nova: UE2022 contra UE2020 nos locais que têm as duas, e
        UE2013 contra UE2015 nos locais que têm as duas, com a mesma conta e o mesmo bootstrap;
    R10. cada modelo antigo separado (UE2013 contra nova, UE2015 contra nova);
    R11. diferenças descritivas no mesmo desenho: fatia do PL (22) para deputado federal e estadual, comparecimento
         sobre aptos, branco+nulo de presidente, log dos aptos.

Acrescentado DEPOIS de ver o resultado (exploração, fora do registro e do veredito; como foi escolhida depois de ver
os números, não vale como teste e serve só para dizer onde olhar):
    E1. D sem cada zona eleitoral (quanto uma zona sozinha move D);
    E2. só AM, só MT, sem AM (os 3 locais de Manaus, zona 70, foram os que mais moveram D em E1);
    E3. índice de dois lados (índice registrado menos a média da fatia do PL para deputado federal e estadual) e só o
        PL, motivado pelo AM, onde o PL separa as seções e a federação quase não;
    E4. só locais com 2 ou mais seções antigas e 2 ou mais novas;
    E5. posição relativa da seção antiga no local (pelo número da seção) e P com o índice e essa posição;
    E6. arquivos de urna do 1º turno das 40 seções dos 3 locais de Manaus (script à parte, conferir_AM_arquivos.py, na
        pasta de trabalho): modelo no log, número da urna, presidente e senador do boletim contra o bweb. Entra no
        texto se o JSON for passado como oitavo argumento.

Uso: python3 -I analisar_F10.py <secoes2026.json.gz> <zips_bweb_1t> <consulta_cand_2026.zip> <F4_modelo_urna.json>
                                <cache_cargos.json.gz> <saida.json> <saida.txt> [conferencia_AM_2550_70.json]
"""
import os as _os, sys as _sys
_sys.path.insert(0, _os.path.dirname(_os.path.abspath(__file__)))
import collections, csv, glob, gzip, hashlib, io, json, math, os, sys, time, zipfile
from multiprocessing import Pool
import numpy as np
from lib import carregar, chave_local, fe_ols
from modelos import FAIXAS as FAIXAS_ANTIGAS

REPS = 2000
SEMENTE = 20261031
FED = ('13', '65', '43')
ANTIGAS = ('UE2013', 'UE2015')
NOVAS = ('UE2020', 'UE2022')
# vetor por seção e cargo: comp, nominal, legenda, branco, nulo, federação, PL, linhas, comp_varia, tipo_estranho
CV = ['comp', 'nom', 'leg', 'bra', 'nul', 'fed', 'pl', 'linhas', 'comp_varia', 'tipo_estranho']
IC = {c: i for i, c in enumerate(CV)}


def log(*a):
    print('#', time.strftime('%H:%M:%S'), *a, file=sys.stderr, flush=True)


# ---------------------------------------------------------------- bweb do 1º turno, cargos 5, 6, 7 e 8

def ler_zip(zpath):
    z = zipfile.ZipFile(zpath)
    nome = [n for n in z.namelist() if n.lower().endswith('.csv')][0]
    out = {}; linhas = 0; usadas = 0; fallback = 0
    sen_tot = collections.defaultdict(int); sen_part = collections.defaultdict(collections.Counter)
    tipos = collections.Counter()
    with z.open(nome) as fh:
        cab = [c.strip().strip('"').replace('SG_ UF', 'SG_UF') for c in fh.readline().decode('latin1').strip().split(';')]
        ix = {c: i for i, c in enumerate(cab)}; nc = len(cab)
        iu, im, iz, iS = ix['SG_UF'], ix['CD_MUNICIPIO'], ix['NR_ZONA'], ix['NR_SECAO']
        icg, ip, ico, it, iv, iq = (ix['CD_CARGO_PERGUNTA'], ix['NR_PARTIDO'], ix['QT_COMPARECIMENTO'],
                                    ix['CD_TIPO_VOTAVEL'], ix['NR_VOTAVEL'], ix['QT_VOTOS'])
        for linha in fh:
            linhas += 1
            f = linha.decode('latin1').rstrip('\r\n').split(';')
            if len(f) != nc:
                f = next(csv.reader([linha.decode('latin1').rstrip('\r\n')], delimiter=';')); fallback += 1
            cg = f[icg].strip('"')
            if cg not in ('5', '6', '7', '8'):
                continue
            usadas += 1
            uf = f[iu].strip('"')
            k = f"{uf}|{int(f[im].strip(chr(34)))}|{int(f[iz].strip(chr(34)))}|{int(f[iS].strip(chr(34)))}"
            s = out.get(k)
            if s is None:
                s = out[k] = {}
            v = s.get(cg)
            comp = int(f[ico].strip('"'))
            if v is None:
                v = s[cg] = [0] * len(CV); v[0] = comp
            elif v[0] != comp:
                v[IC['comp_varia']] = 1
            v[IC['linhas']] += 1
            tv = f[it].strip('"'); q = int(f[iq].strip('"')); p = f[ip].strip('"'); nv = f[iv].strip('"')
            tipos[(cg, tv)] += 1
            if tv == '1' or tv == '4':
                v[IC['nom' if tv == '1' else 'leg']] += q
                if p in FED:
                    v[IC['fed']] += q
                elif p == '22':
                    v[IC['pl']] += q
                if cg == '5' and tv == '1':
                    sv = s.get('s')
                    if sv is None:
                        sv = s['s'] = {}
                    sv[nv] = sv.get(nv, 0) + q
                    sen_tot[uf + '|' + nv] += q; sen_part[uf + '|' + nv][p] += 1
            elif tv == '2':
                v[IC['bra']] += q
            elif tv == '3':
                v[IC['nul']] += q
            else:
                v[IC['tipo_estranho']] += q
    meta = {'linhas': linhas, 'linhas_cargos_5_a_8': usadas, 'fallback_csv': fallback,
            'tipos': {f'{a}|{b}': c for (a, b), c in tipos.items()},
            'senado_total_por_numero': dict(sen_tot),
            'senado_partido_por_numero': {k: dict(c) for k, c in sen_part.items()}}
    return os.path.basename(zpath), out, meta


def extrair(zdir, cache):
    if os.path.exists(cache):
        log('cache', cache)
        with gzip.open(cache, 'rt') as f:
            return json.load(f)
    zips = sorted(glob.glob(os.path.join(zdir, '*.zip')), key=lambda p: -os.path.getsize(p))
    tudo = {}; meta = {}; dup = []
    with Pool(4) as pool:
        for nome, out, m in pool.imap_unordered(ler_zip, zips):
            log(nome, m['linhas_cargos_5_a_8'], 'linhas dos cargos 5 a 8;', len(out), 'seções')
            meta[nome] = m
            for k, v in out.items():
                if k in tudo:
                    dup.append(k)
                tudo[k] = v
    res = {'colunas': CV, 'secoes': tudo, 'meta': meta, 'duplicadas': dup}
    os.makedirs(os.path.dirname(os.path.abspath(cache)), exist_ok=True)
    with gzip.open(cache, 'wt') as f:
        json.dump(res, f, separators=(',', ':'))
    return res


# ---------------------------------------------------------------- candidatos a senador do campo de Lula (cadastro TSE)

def campo_lula(zpath):
    h = hashlib.sha256(open(zpath, 'rb').read()).hexdigest()
    z = zipfile.ZipFile(zpath)
    nome = [n for n in z.namelist() if n.endswith('_BRASIL.csv')][0]
    info = z.getinfo(nome)
    t = io.TextIOWrapper(z.open(nome), encoding='latin1')
    r = csv.reader(t, delimiter=';'); cab = next(r); ix = {c: i for i, c in enumerate(cab)}
    A = collections.defaultdict(dict); B = collections.defaultdict(dict); ger = set(); todos = collections.defaultdict(list)
    for x in r:
        if x[ix['CD_CARGO']] != '5':
            continue
        ger.add(x[ix['DT_GERACAO']] + ' ' + x[ix['HH_GERACAO']])
        uf = x[ix['SG_UF']]; nr = x[ix['NR_CANDIDATO']]
        reg = {'nome_urna': x[ix['NM_URNA_CANDIDATO']], 'partido': x[ix['SG_PARTIDO']], 'nr_partido': x[ix['NR_PARTIDO']],
               'coligacao': x[ix['NM_COLIGACAO']], 'composicao': x[ix['DS_COMPOSICAO_COLIGACAO']],
               'federacao': x[ix['SG_FEDERACAO']]}
        todos[uf].append(nr)
        if 'BRASIL DA ESPERAN' in x[ix['DS_COMPOSICAO_COLIGACAO']] or x[ix['NR_FEDERACAO']] == '101':
            A[uf][nr] = reg
        if x[ix['NR_PARTIDO']] in FED:
            B[uf][nr] = reg
    fonte = {'arquivo': os.path.basename(zpath), 'membro': nome, 'sha256_zip': h,
             'data_hora_do_membro_no_zip': '%04d-%02d-%02d %02d:%02d:%02d' % info.date_time,
             'dt_geracao_no_csv': sorted(ger),
             'url': 'https://cdn.tse.jus.br/estatistica/sead/odsele/consulta_cand/consulta_cand_2026.zip',
             'regra_principal': 'candidato a senador registrado pela coligação que inclui a Federação Brasil da Esperança '
                                '(PT/PCdoB/PV) ou pela própria federação',
             'regra_alternativa': 'candidato a senador de PT, PCdoB ou PV'}
    return dict(A), dict(B), fonte, {u: len(v) for u, v in todos.items()}


# ---------------------------------------------------------------- modelo

def faixas_F4(f4json):
    with open(f4json) as f:
        F = json.load(f)['faixas']
    lim = F['limites_usados']; fx = F['faixas']
    minimo, maximo = lim[0][0], lim[-1][1]
    zonas = [(fx[j]['ultimo_da_amostra'], fx[j + 1]['primeiro_da_amostra']) for j in range(len(fx) - 1)]

    def mod(u):
        if u is None or u < minimo or u > maximo:
            return None
        for f_ in fx:
            if f_['corte_superior'] is None or u < f_['corte_superior']:
                return f_['modelo']
        return None

    def na_zona(u):
        return u is not None and any(a < u < b for a, b in zonas)
    return mod, na_zona, {'limites_usados': lim, 'zonas_de_corte': zonas}


def mod_antigas(u):
    for a, b, m in FAIXAS_ANTIGAS[2026]:
        if a <= u <= b:
            return m
    return None


# ---------------------------------------------------------------- base por seção

def montar(d, cg, mod, na_zona, A, B):
    R = collections.defaultdict(list)
    conf = collections.Counter(); exemplos = collections.defaultdict(list)
    for k, v in d.items():
        a = v.get('1')
        if not a:
            continue
        uf = k.split('|')[0]
        if uf == 'ZZ':
            conf['exterior'] += 1; continue
        if a['comp'] <= 0 or a['L'] + a['R'] <= 0:
            conf['sem_comparecimento_ou_finalistas'] += 1; continue
        s = cg.get(k)
        if s is None:
            conf['sem_linhas_dos_outros_cargos'] += 1; continue
        cde = '8' if uf == 'DF' else '7'
        df_, de_, se_ = s.get('6'), s.get(cde), s.get('5')
        if df_ is None or de_ is None or se_ is None:
            conf['falta_algum_cargo'] += 1; continue
        vdf = df_[1] + df_[2]; vde = de_[1] + de_[2]; vse = se_[1]
        if vdf <= 0 or vde <= 0 or vse <= 0:
            conf['validos_zero_em_algum_cargo'] += 1; continue
        m = mod(a['urna'])
        if m is None:
            conf['sem_modelo'] += 1; continue
        falha = []
        for nomec, x, fator in (('federal', df_, 1), ('estadual', de_, 1), ('senador', se_, 2)):
            if x[0] != a['comp']:
                falha.append(f'comp_{nomec}')
            if x[1] + x[2] + x[3] + x[4] != fator * x[0]:
                falha.append(f'soma_{nomec}')
            if x[IC['comp_varia']]:
                falha.append(f'comp_varia_{nomec}')
            if x[IC['tipo_estranho']]:
                falha.append(f'tipo_estranho_{nomec}')
        for fl in falha:
            conf['conferencia_' + fl] += 1
            if len(exemplos[fl]) < 5:
                exemplos[fl].append(k)
        sv = s.get('s', {})
        la = sum(sv.get(n, 0) for n in A.get(uf, {})) if A.get(uf) else None
        lb = sum(sv.get(n, 0) for n in B.get(uf, {})) if B.get(uf) else None
        b2 = v.get('2')
        ok2 = bool(b2) and b2['L'] + b2['R'] > 0
        R['k'].append(k); R['uf'].append(uf); R['loc'].append(chave_local(k, a)); R['mod'].append(m)
        R['mod_ant'].append(mod_antigas(a['urna'])); R['zona_corte'].append(na_zona(a['urna']))
        R['L1'].append(a['L']); R['R1'].append(a['R']); R['C1'].append(a['comp']); R['apt'].append(a['apt'])
        R['BN1'].append(a['B'] + a['N'])
        R['L2'].append(b2['L'] if ok2 else np.nan); R['R2'].append(b2['R'] if ok2 else np.nan)
        R['vdf'].append(vdf); R['fdf'].append(df_[5]); R['pdf'].append(df_[6])
        R['vde'].append(vde); R['fde'].append(de_[5]); R['pde'].append(de_[6])
        R['vse'].append(vse); R['la'].append(np.nan if la is None else la); R['lb'].append(np.nan if lb is None else lb)
        R['falha'].append(bool(falha))
        conf['na_base'] += 1
    X = {c: (np.array(v, dtype=float) if c not in ('k', 'uf', 'loc', 'mod', 'mod_ant') else np.array(v, dtype=object))
         for c, v in R.items()}
    X['zona_corte'] = np.array(R['zona_corte'], bool); X['falha'] = np.array(R['falha'], bool)
    w = X['L1'] + X['R1']
    X['w'] = w
    X['P'] = 100 * X['L1'] / w
    X['P2'] = 100 * X['L2'] / (X['L2'] + X['R2'])
    X['virada'] = X['P2'] - X['P']
    X['Idf'] = 100 * X['fdf'] / X['vdf']; X['Ide'] = 100 * X['fde'] / X['vde']
    X['IsA'] = 100 * X['la'] / X['vse']; X['IsB'] = 100 * X['lb'] / X['vse']
    X['Idep'] = (X['Idf'] + X['Ide']) / 2
    X['I'] = np.where(np.isfinite(X['IsA']), (X['Idf'] + X['Ide'] + np.nan_to_num(X['IsA'])) / 3, X['Idep'])
    X['IB'] = np.where(np.isfinite(X['IsB']), (X['Idf'] + X['Ide'] + np.nan_to_num(X['IsB'])) / 3, X['Idep'])
    X['PLdf'] = 100 * X['pdf'] / X['vdf']; X['PLde'] = 100 * X['pde'] / X['vde']
    X['comp_pct'] = 100 * X['C1'] / X['apt']; X['bn_pct'] = 100 * X['BN1'] / X['C1']; X['log_apt'] = np.log(X['apt'])
    return X, dict(conf), {k: v for k, v in exemplos.items()}


# ---------------------------------------------------------------- estimador

VARS = ['P', 'I', 'Idf', 'Ide', 'IsA', 'Idep', 'IB', 'IsB', 'P2', 'virada', 'PLdf', 'PLde', 'comp_pct', 'bn_pct', 'log_apt']


def desenho(X, sel, t, vars_, peso=True):
    """Seleciona locais com t=1 e t=0 entre as seções selecionadas; devolve matrizes de produtos cruzados por local."""
    sel = sel.copy()
    for c in vars_:
        sel &= np.isfinite(X[c])
    loc = X['loc'][sel]; tt = t[sel].astype(float)
    _, g = np.unique(loc, return_inverse=True)
    n1 = np.bincount(g, weights=tt); n = np.bincount(g)
    misto = (n1 > 0) & (n1 < n)
    keep = misto[g]
    idx = np.where(sel)[0][keep]
    loc = X['loc'][idx]
    _, g = np.unique(loc, return_inverse=True)
    G = int(g.max() + 1) if len(g) else 0
    w = X['w'][idx] if peso else np.ones(len(idx))
    cols = np.column_stack([t[idx].astype(float)] + [X[c][idx] for c in vars_]) if len(idx) else np.zeros((0, 1 + len(vars_)))
    sw = np.bincount(g, weights=w, minlength=G)
    Z = np.empty_like(cols)
    for j in range(cols.shape[1]):
        m = np.bincount(g, weights=w * cols[:, j], minlength=G) / sw
        Z[:, j] = cols[:, j] - m[g]
    K = cols.shape[1]
    M = np.zeros((G, K, K))
    for a_ in range(K):
        for b_ in range(a_, K):
            s = np.bincount(g, weights=w * Z[:, a_] * Z[:, b_], minlength=G)
            M[:, a_, b_] = s; M[:, b_, a_] = s
    nomes = ['t'] + list(vars_)
    return {'idx': idx, 'g': g, 'G': G, 'M': M, 'nomes': nomes, 'w': w, 'Z': Z}


def stats(M, nomes, pares):
    """pares: lista de (rotulo, y, x[, z]) -> D = dy - b dx, com b de y em x (ou IV com z)."""
    p = {n: i for i, n in enumerate(nomes)}; t = p['t']
    out = {}
    for rot, y, x, z, conj in pares:
        iy, ix_ = p[y], p[x]
        dy = M[t, iy] / M[t, t]; dx = M[t, ix_] / M[t, t]
        if z is not None:
            b = M[p[z], iy] / M[p[z], ix_]
        elif conj:
            A2 = np.array([[M[ix_, ix_], M[ix_, t]], [M[t, ix_], M[t, t]]])
            sol = np.linalg.solve(A2, np.array([M[ix_, iy], M[t, iy]]))
            b = sol[0]
        else:
            b = M[ix_, iy] / M[ix_, ix_]
        out[rot] = {'dP': dy, 'dI': dx, 'b': b, 'D': dy - b * dx}
    return out


def rodar(X, sel, t, pares, vars_, peso=True, reps=REPS, semente=SEMENTE):
    dz = desenho(X, sel, t, vars_, peso)
    if dz['G'] < 2:
        return {'secoes': int(len(dz['idx'])), 'locais': dz['G'], 'erro': 'menos de 2 locais'}
    Mt = dz['M'].sum(0)
    est = stats(Mt, dz['nomes'], pares)
    rng = np.random.default_rng(semente)
    G = dz['G']
    bs = {r: {c: [] for c in ('dP', 'dI', 'b', 'D')} for r, *_ in pares}
    for _ in range(reps):
        c = np.bincount(rng.integers(0, G, G), minlength=G).astype(float)
        Mb = np.tensordot(c, dz['M'], axes=1)
        try:
            sb = stats(Mb, dz['nomes'], pares)
        except (np.linalg.LinAlgError, ZeroDivisionError, FloatingPointError):
            continue
        for r in sb:
            for cc in ('dP', 'dI', 'b', 'D'):
                bs[r][cc].append(sb[r][cc])
    idx = dz['idx']
    tt = t[idx]
    out = {'secoes': int(len(idx)), 'locais': int(G), 'secoes_t1': int(tt.sum()), 'secoes_t0': int((~tt.astype(bool)).sum()),
           'peso': 'L1+R1' if peso else 'nenhum', 'replicas': reps, 'semente': semente, 'estatisticas': {}}
    for r in est:
        e = est[r]; o = {}
        for cc in ('dP', 'dI', 'b', 'D'):
            arr = np.array(bs[r][cc], float); arr = arr[np.isfinite(arr)]
            o[cc] = float(e[cc]); o['ep_' + cc] = float(arr.std(ddof=1)) if len(arr) > 1 else None
            o['ic95_' + cc] = [float(np.percentile(arr, 2.5)), float(np.percentile(arr, 97.5))] if len(arr) > 1 else None
        o['replicas_validas'] = int(len(bs[r]['D']))
        o['z_D'] = o['D'] / o['ep_D'] if o['ep_D'] else None
        o['razao_dP_sobre_dI'] = o['dP'] / o['dI'] if o['dI'] != 0 else None
        out['estatisticas'][r] = o
    out['_dz'] = dz
    return out


def veredito(D, ep):
    if D >= 0.5 and D > 3 * ep:
        return 'SINAL DE MÁQUINA'
    if abs(D) < 0.3 and ep <= 0.2:
        return 'SEM SINAL'
    return 'INCONCLUSIVO'


def limpar(r):
    return {k: v for k, v in r.items() if not k.startswith('_')}


# ---------------------------------------------------------------- exploração depois de ver o resultado (fora do registro)

def exploracao(X, ant, nov, t):
    PP = [('principal', 'P', 'I', None, False)]
    sel = ant | nov
    o = {'aviso': 'escolhida depois de ver o resultado; fora do registro e do veredito'}
    base = rodar(X, sel, t, PP, ['P', 'I'], reps=2)
    dz = base['_dz']; M = dz['M']; nomes = dz['nomes']
    ul = np.unique(X['loc'][dz['idx']])
    zon = np.array(['|'.join(l.split('|')[:3]) for l in ul])
    jz = []
    for z in np.unique(zon):
        Mi = M.sum(0) - M[zon == z].sum(0)
        jz.append([float(stats(Mi, nomes, PP)['principal']['D']), str(z), int((zon == z).sum())])
    jz.sort()
    o['E1_D_sem_cada_zona'] = {'menores': jz[:5], 'maiores': jz[-5:], 'zonas': len(jz)}
    X = dict(X)
    X['PLdep'] = (X['PLdf'] + X['PLde']) / 2
    X['I2'] = X['I'] - X['PLdep']
    pares = PP + [('I_dois_lados', 'P', 'I2', None, False), ('so_PL_deputados', 'P', 'PLdep', None, False)]
    for rot, m in (('todos', np.ones(len(t), bool)), ('so_AM', X['uf'] == 'AM'), ('so_MT', X['uf'] == 'MT'),
                   ('sem_AM', X['uf'] != 'AM'), ('so_SP', X['uf'] == 'SP')):
        r = rodar(X, sel & m, t, pares, ['P', 'I', 'I2', 'PLdep'])
        o['E2_E3_' + rot] = {k: {c: v[c] for c in ('dP', 'dI', 'b', 'D', 'ep_D', 'z_D')} for k, v in r['estatisticas'].items()}
        o['E2_E3_' + rot]['secoes'] = r['secoes']; o['E2_E3_' + rot]['locais'] = r['locais']
        for k, v in o['E2_E3_' + rot].items():
            if isinstance(v, dict):
                v['leitura_pelo_criterio_se_fosse_o_registrado'] = veredito(v['D'], v['ep_D'])
    idx = dz['idx']
    cnt = collections.defaultdict(lambda: [0, 0])
    for l, a_ in zip(X['loc'][idx], t[idx]):
        cnt[l][int(a_)] += 1
    bons = [l for l, c in cnt.items() if c[0] >= 2 and c[1] >= 2]
    r = rodar(X, sel & np.isin(X['loc'], bons), t, PP, ['P', 'I'])
    e = r['estatisticas']['principal']
    o['E4_locais_com_2_ou_mais_de_cada'] = {c: e[c] for c in ('dP', 'dI', 'b', 'D', 'ep_D')} | {'secoes': r['secoes'], 'locais': r['locais']}
    locs = X['loc'][idx]
    sec = np.array([int(k.split('|')[3]) for k in X['k'][idx]])
    pos = np.zeros(len(idx))
    for l in np.unique(locs):
        mm = locs == l
        pos[mm] = sec[mm].argsort().argsort() / max(1, mm.sum() - 1)
    w = X['w'][idx]
    r1 = fe_ols(pos, t[idx], locs, w, ['antiga'])
    r2 = fe_ols(X['P'][idx], np.column_stack([t[idx], X['I'][idx], pos]), locs, w, ['antiga', 'I', 'posicao'])
    am = X['uf'][idx] == 'AM'
    r3 = fe_ols(pos[am], t[idx][am], locs[am], w[am], ['antiga'])
    o['E5_posicao_relativa'] = {'antiga_menos_nova_todos': [r1['coef']['antiga'], r1['ep']['antiga']],
                                'antiga_menos_nova_AM': [r3['coef']['antiga'], r3['ep']['antiga']],
                                'P_em_antiga_I_posicao': {'coef': r2['coef'], 'ep_CR1': r2['ep']}}
    return o


# ---------------------------------------------------------------- principal

def main():
    arq_d, zdir, arq_cand, arq_f4, cache, saida_json, saida_txt = sys.argv[1:8]
    arq_am = sys.argv[8] if len(sys.argv) > 8 else None
    A, B, fonte, n_sen = campo_lula(arq_cand)
    log('campo de Lula (regra principal):', {u: list(v) for u, v in sorted(A.items())})
    cg = extrair(zdir, cache)
    d = carregar(arq_d)
    mod, na_zona, fx = faixas_F4(arq_f4)
    X, conf, exemplos = montar(d, cg['secoes'], mod, na_zona, A, B)
    del d
    log('seções na base', len(X['k']))
    antiga = np.isin(X['mod'], ANTIGAS)
    nova = np.isin(X['mod'], NOVAS)
    todas = np.ones(len(antiga), bool)

    P_PRINC = [('principal', 'P', 'I', None, False)]
    pares_main = P_PRINC + [
        ('R2_federal', 'P', 'Idf', None, False), ('R2_estadual', 'P', 'Ide', None, False),
        ('R2_senador', 'P', 'IsA', None, False), ('R2_so_deputados', 'P', 'Idep', None, False),
        ('R2_senador_so_PT_PCdoB_PV_no_indice', 'P', 'IB', None, False),
        ('R3_b_com_indicador', 'P', 'I', None, True),
        ('R8_federal_instrumentado_pelo_estadual', 'P', 'Idf', 'Ide', False),
        ('R8_estadual_instrumentado_pelo_federal', 'P', 'Ide', 'Idf', False),
        ('R8_deputados_instrumentado_pelo_senador', 'P', 'Idep', 'IsA', False)]
    vars_main = ['P', 'I', 'Idf', 'Ide', 'IsA', 'Idep', 'IB']
    t_old = antiga.astype(float)
    sel_main = antiga | nova
    log('principal')
    princ = rodar(X, sel_main, t_old, pares_main, vars_main)
    dz = princ['_dz']
    E = princ['estatisticas']['principal']
    ver = veredito(E['D'], E['ep_D'])

    # conferência com lib.fe_ols (CR1) na amostra principal
    ii = dz['idx']; locs = X['loc'][ii]; w = X['w'][ii]
    r1 = fe_ols(X['P'][ii], t_old[ii], locs, w, ['antiga'])
    r2 = fe_ols(X['I'][ii], t_old[ii], locs, w, ['antiga'])
    r3 = fe_ols(X['P'][ii], X['I'][ii], locs, w, ['I'])
    r4 = fe_ols(X['P'][ii], np.column_stack([X['I'][ii], t_old[ii]]), locs, w, ['I', 'antiga'])
    conf_lib = {'dP': [r1['coef']['antiga'], r1['ep']['antiga']], 'dI': [r2['coef']['antiga'], r2['ep']['antiga']],
                'b': [r3['coef']['I'], r3['ep']['I']], 'conjunta_I_e_antiga': [r4['coef'], r4['ep']],
                'delta_metodo_ep_D_ignorando_covariancias': math.sqrt(r1['ep']['antiga'] ** 2 + (r3['coef']['I'] * r2['ep']['antiga']) ** 2
                                                                     + (r2['coef']['antiga'] * r3['ep']['I']) ** 2)}

    # composição da amostra principal
    comp_uf = collections.Counter(X['uf'][ii]); comp_mod = collections.Counter(X['mod'][ii])
    locs_uf = collections.Counter(l.split('|')[0] for l in set(locs.tolist()))
    combos = collections.Counter()
    ml = collections.defaultdict(set)
    for l, m in zip(locs.tolist(), X['mod'][ii].tolist()):
        ml[l].add(m)
    for s in ml.values():
        combos['+'.join(sorted(s))] += 1
    medias = {}
    for m in sorted(comp_mod):
        s = X['mod'][ii] == m
        medias[m] = {c: float(np.average(X[c][ii][s], weights=w[s])) for c in ('P', 'I', 'Idf', 'Ide', 'IsA', 'PLdf', 'PLde')}
        medias[m]['secoes'] = int(s.sum())
    por_local = []
    for l in sorted(ml):
        s = locs == l
        o = s & (t_old[ii] == 1); n_ = s & (t_old[ii] == 0)
        por_local.append({'local': l, 'modelos': sorted(ml[l]), 'secoes_antigas': int(o.sum()), 'secoes_novas': int(n_.sum()),
                          'P_antigas': float(np.average(X['P'][ii][o], weights=w[o])), 'P_novas': float(np.average(X['P'][ii][n_], weights=w[n_])),
                          'I_antigas': float(np.average(X['I'][ii][o], weights=w[o])), 'I_novas': float(np.average(X['I'][ii][n_], weights=w[n_]))})

    # robustez
    log('robustez')
    rob = {}
    rob['R1_presidente_2t'] = rodar(X, sel_main, t_old, [('P2', 'P2', 'I', None, False)], ['P2', 'I'])
    rob['R1_virada'] = rodar(X, sel_main, t_old, [('virada', 'virada', 'I', None, False)], ['virada', 'I'])
    rob['R1_presidente_1t_mesma_amostra_do_2t'] = rodar(X, sel_main & np.isfinite(X['P2']), t_old, P_PRINC, ['P', 'I'])
    rob['R4_sem_peso'] = rodar(X, sel_main, t_old, P_PRINC, ['P', 'I'], peso=False)
    rob['R5_20_ou_mais_votantes'] = rodar(X, sel_main & (X['C1'] >= 20), t_old, P_PRINC, ['P', 'I'])
    ant_m = X['mod_ant']
    t_ant = np.isin(ant_m, ANTIGAS).astype(float)
    rob['R6_faixas_modelos_py'] = rodar(X, np.isin(ant_m, ANTIGAS) | np.isin(ant_m, NOVAS), t_ant, P_PRINC, ['P', 'I'])
    rob['R6_sem_zona_de_corte'] = rodar(X, sel_main & ~X['zona_corte'], t_old, P_PRINC, ['P', 'I'])
    rob['R7_so_SP'] = rodar(X, sel_main & (X['uf'] == 'SP'), t_old, P_PRINC, ['P', 'I'])
    rob['R7_sem_SP'] = rodar(X, sel_main & (X['uf'] != 'SP'), t_old, P_PRINC, ['P', 'I'])
    rob['D12_sem_secoes_com_conferencia_falha'] = rodar(X, sel_main & ~X['falha'], t_old, P_PRINC, ['P', 'I'])
    for m in ANTIGAS:
        rob[f'R10_{m}_contra_novas'] = rodar(X, (X['mod'] == m) | nova, (X['mod'] == m).astype(float), P_PRINC, ['P', 'I'])
    log('calibração')
    rob['R9_calibracao_UE2022_contra_UE2020'] = rodar(X, np.isin(X['mod'], NOVAS), (X['mod'] == 'UE2022').astype(float),
                                                      P_PRINC + [('R3_b_com_indicador', 'P', 'I', None, True)], ['P', 'I'])
    rob['R9_calibracao_UE2013_contra_UE2015'] = rodar(X, np.isin(X['mod'], ANTIGAS), (X['mod'] == 'UE2013').astype(float),
                                                      P_PRINC + [('R3_b_com_indicador', 'P', 'I', None, True)], ['P', 'I'])
    # R11 diferenças descritivas (só a diferença dentro do local, mesmo desenho e bootstrap)
    desc = {}
    for c in ('PLdf', 'PLde', 'comp_pct', 'bn_pct', 'log_apt', 'Idf', 'Ide', 'IsA', 'IsB', 'P2', 'virada'):
        r_ = rodar(X, sel_main, t_old, [(c, c, 'I', None, False)], [c, 'I'])
        if 'estatisticas' not in r_:
            desc[c] = {'diferenca_antiga_menos_nova': None, 'ep_bootstrap': None, 'secoes': r_['secoes'], 'locais': r_['locais'],
                       'nota': r_.get('erro')}
            continue
        e_ = r_['estatisticas'][c]
        desc[c] = {'diferenca_antiga_menos_nova': e_['dP'], 'ep_bootstrap': e_['ep_dP'], 'secoes': r_['secoes'], 'locais': r_['locais']}
    for r_, e_ in princ['estatisticas'].items():
        if r_ != 'principal':
            e_['leitura_pelo_criterio'] = veredito(e_['D'], e_['ep_D'])
    for kk in rob:
        if 'estatisticas' in rob[kk]:
            for r_, e_ in rob[kk]['estatisticas'].items():
                e_['leitura_pelo_criterio'] = veredito(e_['D'], e_['ep_D'])

    # conferência dos candidatos no bweb
    sen_tot = collections.Counter(); sen_part = collections.defaultdict(collections.Counter)
    for nome, m in cg['meta'].items():
        for kk, q in m['senado_total_por_numero'].items():
            sen_tot[kk] += q
        for kk, c in m['senado_partido_por_numero'].items():
            sen_part[kk].update(c)
    cand_conf = {}
    for uf in sorted(set(A) | set(B)):
        for nr, reg in sorted({**A.get(uf, {}), **B.get(uf, {})}.items()):
            kk = f'{uf}|{nr}'
            cand_conf[kk] = {'nome_urna': reg['nome_urna'], 'partido_cadastro': reg['partido'], 'nr_partido_cadastro': reg['nr_partido'],
                             'coligacao': reg['coligacao'], 'regra_principal': nr in A.get(uf, {}), 'regra_alternativa': nr in B.get(uf, {}),
                             'no_bweb': kk in sen_tot, 'votos_no_estado': sen_tot.get(kk, 0),
                             'nr_partido_no_bweb': dict(sen_part.get(kk, {}))}
    ufs_sem_A = sorted(set(n_sen) - set(A)); ufs_sem_B = sorted(set(n_sen) - set(B))
    tipos_tot = collections.Counter()
    for m in cg['meta'].values():
        tipos_tot.update(m['tipos'])

    log('exploração posterior')
    expl = exploracao(X, antiga, nova, t_old)
    if arq_am and os.path.exists(arq_am):
        with open(arq_am) as f:
            expl['E6_arquivos_de_urna_Manaus_zona_70'] = json.load(f)['resumo']

    out = {'teste': 'F10 do Adendo 21: urnas antigas, o mesmo desvio aparece nos outros cargos?',
           'registro': 'PRE-REGISTRO-2026-10-26.md, Adendo 21 (commit 913af7a, 31/10/2026 10:36:29 UTC)',
           'veredito': ver, 'D': E['D'], 'ep_D': E['ep_D'], 'z_D': E['z_D'],
           'principal': limpar(princ), 'conferencia_lib_fe_ols_CR1': conf_lib,
           'composicao': {'secoes_por_uf': dict(comp_uf), 'locais_por_uf': dict(locs_uf), 'secoes_por_modelo': dict(comp_mod),
                          'combinacoes_de_modelo_nos_locais': dict(combos), 'medias_ponderadas_por_modelo_na_amostra': medias},
           'por_local': por_local,
           'robustez_descritiva': {k: limpar(v) for k, v in rob.items()},
           'diferencas_descritivas_R11': desc,
           'exploracao_depois_de_ver_o_resultado_fora_do_registro': expl,
           'senado_campo_de_Lula': {'fonte': fonte, 'regra_principal': {u: {n: r['nome_urna'] + ' (' + r['partido'] + ')' for n, r in v.items()} for u, v in sorted(A.items())},
                                    'regra_alternativa': {u: {n: r['nome_urna'] + ' (' + r['partido'] + ')' for n, r in v.items()} for u, v in sorted(B.items())},
                                    'ufs_sem_candidato_regra_principal': ufs_sem_A, 'ufs_sem_candidato_regra_alternativa': ufs_sem_B,
                                    'candidatos_ao_senado_no_cadastro_por_uf': n_sen, 'conferencia_no_bweb': cand_conf},
           'faixas_F4': fx,
           'base': {'filtros': conf, 'exemplos_de_conferencia_falha': exemplos, 'secoes_na_base': int(len(X['k'])),
                    'zips': {n: {kk: m[kk] for kk in ('linhas', 'linhas_cargos_5_a_8', 'fallback_csv')} for n, m in cg['meta'].items()},
                    'tipos_de_voto_por_cargo': dict(tipos_tot), 'secoes_duplicadas_entre_zips': len(cg['duplicadas'])}}
    with open(saida_json, 'w') as f:
        json.dump(out, f, ensure_ascii=False, indent=1, default=lambda o: o.tolist() if hasattr(o, 'tolist') else str(o))
    escrever_txt(out, saida_txt)
    log('fim')


# ---------------------------------------------------------------- texto

def fz(x, c=2):
    if x is None or (isinstance(x, float) and not math.isfinite(x)):
        return 'n/d'
    s = f'{x:,.{c}f}'
    return s.replace(',', 'X').replace('.', ',').replace('X', '.')


def fi(x):
    return f'{int(x):,}'.replace(',', '.')


def linha_est(nome, e):
    return (f"  {nome}: dP {fz(e['dP'], 3)} (ep {fz(e['ep_dP'], 3)}); dI {fz(e['dI'], 3)} (ep {fz(e['ep_dI'], 3)}); b {fz(e['b'], 3)} "
            f"(ep {fz(e['ep_b'], 3)}); D {fz(e['D'], 3)} (ep {fz(e['ep_D'], 3)}; z {fz(e['z_D'], 1)}; IC95 {fz(e['ic95_D'][0], 2)} a {fz(e['ic95_D'][1], 2)})"
            + (f"; leitura pelo critério: {e['leitura_pelo_criterio']}" if 'leitura_pelo_criterio' in e else ''))


def escrever_txt(o, caminho):
    L = []; w = L.append
    P = o['principal']; E = P['estatisticas']['principal']
    w('F10 do Adendo 21: urnas antigas, o mesmo desvio aparece nos outros cargos?')
    w('Registro: PRE-REGISTRO-2026-10-26.md, Adendo 21 (commit 913af7a, 31/10/2026 10:36:29 UTC). Script: scripts/analisar_F10.py.')
    w('')
    w(f"VEREDITO PELA LETRA: {o['veredito']}")
    w(f"  D = {fz(E['D'], 3)} ponto, erro-padrão por bootstrap de locais {fz(E['ep_D'], 3)} ({E['replicas_validas']} réplicas, semente {P['semente']}); z {fz(E['z_D'], 2)}.")
    w('  Critério: sinal de máquina se D >= +0,5 a mais de 3 erros-padrão; sem sinal se |D| < 0,3 com erro-padrão até 0,2; senão inconclusivo.')
    w('')
    w('1. Amostra')
    fl = o['base']['filtros']
    w(f"  Seções na base (Brasil, 1º turno, três cargos com válidos, modelo definido): {fi(o['base']['secoes_na_base'])}. Fora: exterior {fi(fl.get('exterior', 0))},"
      f" sem modelo {fi(fl.get('sem_modelo', 0))}, outros filtros {fi(sum(v for k, v in fl.items() if k not in ('na_base', 'exterior', 'sem_modelo') and not k.startswith('conferencia')))}.")
    w(f"  Conferência: comparecimento de presidente diferente do dos outros cargos em {fi(fl.get('conferencia_comp_federal', 0))} seções (sempre maior no presidente;"
      " compatível com eleitor em trânsito de outra UF, que só vota para presidente). Soma dos votos igual ao comparecimento em todos os cargos"
      f" (falhas: {', '.join(k.replace('conferencia_', '') + ' ' + fi(v) for k, v in fl.items() if k.startswith('conferencia_soma')) or 'nenhuma'}).")
    C = o['composicao']
    w(f"  Locais com urna antiga e nova: {fi(P['locais'])}; seções {fi(P['secoes'])} (antigas {fi(P['secoes_t1'])}, novas {fi(P['secoes_t0'])}).")
    w('  Locais por UF: ' + ', '.join(f'{u} {fi(n)}' for u, n in sorted(C['locais_por_uf'].items(), key=lambda t: -t[1])))
    w('  Seções por modelo: ' + ', '.join(f'{m} {fi(n)}' for m, n in sorted(C['secoes_por_modelo'].items())))
    w('  Combinações de modelo nos locais: ' + '; '.join(f'{c} {fi(n)}' for c, n in sorted(C['combinacoes_de_modelo_nos_locais'].items(), key=lambda t: -t[1])))
    w('  Médias ponderadas por modelo na amostra (sem efeito fixo, só descritivo): ' + '; '.join(
        f"{m}: P {fz(x['P'])}, I {fz(x['I'])}, federal {fz(x['Idf'])}, estadual {fz(x['Ide'])}, senador {fz(x['IsA'])} ({fi(x['secoes'])} seções)"
        for m, x in C['medias_ponderadas_por_modelo_na_amostra'].items()))
    w('')
    w('2. Estatística registrada (efeito fixo de local, peso L1+R1)')
    w(f"  Diferença antiga menos nova no presidente (fatia de Lula no 1º turno), dP: {fz(E['dP'], 3)} (ep {fz(E['ep_dP'], 3)}).")
    w(f"  Diferença antiga menos nova no índice de perfil, dI: {fz(E['dI'], 3)} (ep {fz(E['ep_dI'], 3)}).")
    w(f"  Inclinação b da fatia de Lula sobre o índice, dentro do local: {fz(E['b'], 3)} (ep {fz(E['ep_b'], 3)}).")
    w(f"  D = dP - b x dI = {fz(E['dP'], 3)} - {fz(E['b'], 3)} x {fz(E['dI'], 3)} = {fz(E['D'], 3)}; IC95 percentil {fz(E['ic95_D'][0], 2)} a {fz(E['ic95_D'][1], 2)}.")
    w(f"  Inclinação que zeraria D (dP/dI): {fz(E['razao_dP_sobre_dI'], 3)}.")
    c = o['conferencia_lib_fe_ols_CR1']
    w(f"  Conferência com lib.fe_ols (CR1): dP {fz(c['dP'][0], 3)} ({fz(c['dP'][1], 3)}); dI {fz(c['dI'][0], 3)} ({fz(c['dI'][1], 3)}); b {fz(c['b'][0], 3)} ({fz(c['b'][1], 3)}); "
      f"ep de D pelo método delta sem covariâncias {fz(c['delta_metodo_ep_D_ignorando_covariancias'], 3)}.")
    w('')
    w('3. Componentes do índice e leituras da inclinação (mesma amostra, fora do veredito)')
    for r, e in P['estatisticas'].items():
        if r != 'principal':
            w(linha_est(r, e))
    w('')
    w('4. Robustez (fora do veredito)')
    for k, r in o['robustez_descritiva'].items():
        if 'estatisticas' not in r:
            w(f"  {k}: {r}"); continue
        for rr, e in r['estatisticas'].items():
            w(linha_est(f"{k} [{rr}] ({fi(r['secoes'])} seções, {fi(r['locais'])} locais)", e))
    w('')
    w('5. Diferenças descritivas antiga menos nova no mesmo desenho (R11)')
    for k, x in o['diferencas_descritivas_R11'].items():
        w(f"  {k}: {fz(x['diferenca_antiga_menos_nova'], 3)} (ep {fz(x['ep_bootstrap'], 3)}; {fi(x['secoes'])} seções, {fi(x['locais'])} locais)")
    w('')
    S = o['senado_campo_de_Lula']
    w('6. Senador: candidatos do campo de Lula')
    w(f"  Fonte: TSE, {S['fonte']['url']} ({S['fonte']['membro']}, gerado {', '.join(S['fonte']['dt_geracao_no_csv'])}; sha256 do zip {S['fonte']['sha256_zip'][:16]}...).")
    w(f"  Regra principal: {S['fonte']['regra_principal']}.")
    for u, v in S['regra_principal'].items():
        w(f"    {u}: " + '; '.join(f'{n} {x}' for n, x in v.items()))
    w(f"  UFs sem candidato pela regra principal: {', '.join(S['ufs_sem_candidato_regra_principal']) or 'nenhuma'}.")
    w(f"  Regra alternativa ({S['fonte']['regra_alternativa']}); UFs sem candidato: {', '.join(S['ufs_sem_candidato_regra_alternativa']) or 'nenhuma'}.")
    falt = [k for k, x in S['conferencia_no_bweb'].items() if not x['no_bweb']]
    part = [k for k, x in S['conferencia_no_bweb'].items() if x['no_bweb'] and list(x['nr_partido_no_bweb']) != [x['nr_partido_cadastro']]]
    w(f"  Conferência no bweb: candidatos ausentes {falt or 'nenhum'}; partido no bweb diferente do cadastro {part or 'nenhum'}.")
    w('')
    w('7. Conferências do bweb')
    w(f"  Tipos de voto (cargo|tipo: linhas): {o['base']['tipos_de_voto_por_cargo']}")
    w(f"  Seções duplicadas entre zips: {o['base']['secoes_duplicadas_entre_zips']}.")
    w('')
    X_ = o['exploracao_depois_de_ver_o_resultado_fora_do_registro']
    w('8. Exploração DEPOIS de ver o resultado (fora do registro e do veredito; escolhida depois, não vale como teste)')
    e1 = X_['E1_D_sem_cada_zona']
    w(f"  E1. D sem cada zona ({e1['zonas']} zonas): menores " + '; '.join(f'sem {z} ({n} locais) {fz(dv, 3)}' for dv, z, n in e1['menores'][:3])
      + '; maiores ' + '; '.join(f'sem {z} ({n} locais) {fz(dv, 3)}' for dv, z, n in e1['maiores'][-3:]) + '.')
    for rot in ('todos', 'so_AM', 'so_MT', 'sem_AM', 'so_SP'):
        x = X_['E2_E3_' + rot]
        w(f"  E2/E3 {rot} ({fi(x['secoes'])} seções, {fi(x['locais'])} locais): " + '; '.join(
            f"{k}: dP {fz(v['dP'], 3)}, dI {fz(v['dI'], 3)}, b {fz(v['b'], 3)}, D {fz(v['D'], 3)} (ep {fz(v['ep_D'], 3)}; leitura se fosse o registrado: {v['leitura_pelo_criterio_se_fosse_o_registrado']})"
            for k, v in x.items() if isinstance(v, dict)))
    e4 = X_['E4_locais_com_2_ou_mais_de_cada']
    w(f"  E4. Só locais com 2 ou mais seções de cada grupo ({fi(e4['secoes'])} seções, {fi(e4['locais'])} locais): D {fz(e4['D'], 3)} (ep {fz(e4['ep_D'], 3)}).")
    e5 = X_['E5_posicao_relativa']
    w(f"  E5. Posição relativa da seção antiga no local (0 = menor número, 1 = maior): antiga menos nova {fz(e5['antiga_menos_nova_todos'][0], 3)}"
      f" (ep {fz(e5['antiga_menos_nova_todos'][1], 3)}); no AM {fz(e5['antiga_menos_nova_AM'][0], 3)} (ep {fz(e5['antiga_menos_nova_AM'][1], 3)});"
      f" coeficiente da antiga em P com índice e posição {fz(e5['P_em_antiga_I_posicao']['coef']['antiga'], 3)} (ep CR1 {fz(e5['P_em_antiga_I_posicao']['ep_CR1']['antiga'], 3)}).")
    if 'E6_arquivos_de_urna_Manaus_zona_70' in X_:
        e6 = X_['E6_arquivos_de_urna_Manaus_zona_70']
        w(f"  E6. Arquivos de urna do 1º turno das {e6['secoes']} seções dos 3 locais de Manaus, zona 70: modelo do log igual ao da faixa em {e6['modelo_log_igual_faixa']},"
          f" urna do boletim igual à do bweb em {e6['urna_bu_igual_bweb']}, presidente do boletim igual ao bweb em {e6['pres_igual']}, senador em {e6['sen_igual']};"
          f" versão {', '.join(e6['versoes'])}.")
    w('')
    w('Desvios declarados (decisões que o registro não fixa, tomadas antes de calcular): ver o docstring do script, D1 a D12 e R1 a R11.')
    txt = '\n'.join(L) + '\n'
    for ch in (chr(0x2014), chr(0x2013)):
        txt = txt.replace(ch, '-')
    with open(caminho, 'w') as f:
        f.write(txt)


if __name__ == '__main__':
    main()
