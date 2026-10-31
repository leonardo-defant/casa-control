"""F16 do Adendo 22: urnas antigas com o perfil do eleitorado por seção.

Registro (PRE-REGISTRO-2026-10-26.md, Adendo 22, commit f12121e, 31/10/2026 14:52:48 UTC, antes de rodar):
  - Dado aberto do TSE: perfil do eleitorado por seção eleitoral de 2026 (faixa etária, gênero, instrução), nas UFs dos
    119 locais mistos do F10 (SP, AM, MT).
  - Na amostra do F10 (mesmas seções, mesmo peso L1+R1, efeito fixo de local), regressão da fatia de Lula no 1º turno
    sobre o indicador de urna antiga, o índice do F10 e o perfil da seção (fração de 16 a 34 anos, de 60 ou mais, de
    mulheres, com superior completo e com fundamental incompleto ou menos). Erro por bootstrap de locais (2.000, semente
    20261031).
  - Sinal de máquina: coeficiente da urna antiga de +0,5 ponto ou mais a mais de 3 erros-padrão. Sem sinal: valor absoluto
    abaixo de 0,3 com erro-padrão até 0,2. Entre os dois: inconclusivo.
  Pedido junto com a tarefa (fora do registro, descritivo): dizer se, nas zonas 420 de SP (São Paulo, município 71072) e
  70 de Manaus (AM, município 2550), as seções com urna antiga têm perfil diferente das novas do mesmo local.

O que já tinha sido visto antes de escrever este arquivo (transparência): todo o F10 (resultados/F10_urnas_antigas_cargos.*,
inclusive dP 0,744, dI 0,262, D 0,441, a exploração E1 em que a zona 70 de Manaus e a zona 420 de SP são as que mais movem
D, e a E5 em que, no AM, as seções antigas têm os menores números do local, -0,541). Dos arquivos do perfil, só o
cabeçalho, as primeiras linhas e a contagem de códigos do arquivo inteiro do AM (gênero 2 e 4; faixas 1600 a 9999 e -3
inválida; escolaridade 1 a 8; data de geração 14/07/2026). Nenhum número do perfil por seção, por modelo de urna ou por
local foi olhado antes de fixar as decisões abaixo.

Arquivos (baixados de novo para o F16 em /home/user/trabalho-eleicao/adendo22/F16_dl_perfil_secao, 31/10/2026 14:54 UTC):
  https://cdn.tse.jus.br/estatistica/sead/odsele/perfil_eleitor_secao/perfil_eleitor_secao_2026_{SP,AM,MT}.zip
  (conjunto "Eleitorado - 2026" do portal de dados abertos do TSE). O sha256 de cada um é registrado na saída.

Decisões que o registro não fixa (tomadas antes de calcular; cada uma é declarada como desvio):
  G1. Amostra do F10: reconstruída com o próprio código do F10 (analisar_F10.montar e analisar_F10.desenho, com as mesmas
      entradas: base por seção, cache dos cargos 5 a 8 do bweb do 1º turno, cadastro de candidaturas e faixas do F4). Antes
      de qualquer conta, confere-se que dá 1.332 seções em 119 locais, com as mesmas contagens de seções antigas e novas por
      local do F10 (por_local do JSON do F10) e o mesmo dP, dI e D. Se não bater, o script para.
  G2. Junção: chave UF|CD_MUNICIPIO|NR_ZONA|NR_SECAO (código TSE do município, como no bweb). O perfil da seção é a soma
      das linhas da própria seção e das seções agregadas a ela no 1º turno (campo agr do turno 1 da base, mesmo município e
      zona), porque os votos da urna incluem os eleitores dessas seções. Seção da amostra sem nenhuma linha no perfil sai
      (contagem relatada); se um local perder a mistura de antiga e nova, sai também. Conferência relatada, sem tirar
      seções: total de eleitores no perfil contra os aptos do 1º turno no bweb; local de votação do perfil (julho) contra o
      do 1º turno.
  G3. Frações, em pontos (0 a 100), cada uma sobre os eleitores com aquela dimensão informada:
      jovem = 16 a 34 anos (faixas 1600, 1700, 1800, 1900, 2000, 2124, 2529, 3034) sobre as faixas válidas (1600 a 9999);
      idoso = 60 ou mais (6064 a 9999, inclusive 100 anos ou mais) sobre as faixas válidas;
      mulher = CD_GENERO 4 sobre gênero 2 ou 4;
      superior = superior completo (CD_GRAU_ESCOLARIDADE 8) sobre escolaridade 1 a 8;
      fund_inc = fundamental incompleto ou menos (1 analfabeto, 2 lê e escreve, 3 fundamental incompleto) sobre 1 a 8.
      Códigos fora dessas listas (faixa inválida, gênero ou escolaridade não informados) ficam fora do denominador da sua
      dimensão; a quantidade é relatada. Categorias de referência implícitas: 35 a 59 anos; homens; fundamental completo a
      superior incompleto.
  G4. Fatia de Lula: P = 100 x L1/(L1+R1), a do F10 (D4 do F10). Índice: I do F10 (média simples das fatias da federação
      PT/PCdoB/PV para deputado federal e estadual e do campo de Lula para senador). Urna antiga = UE2013 ou UE2015 pelas
      faixas do F4 (D1 do F10).
  G5. Modelo: uma regressão só, P em [antiga, I, jovem, idoso, mulher, superior, fund_inc], com efeito fixo de local
      (transformação within ponderada), peso L1+R1, mínimos quadrados ponderados. Estatística: o coeficiente de antiga.
  G6. Bootstrap: como o do F10 (D10): 2.000 réplicas, semente 20261031 (numpy default_rng, um sorteio integers(0, G, G)
      por réplica), sorteio com reposição dos locais, cada local sorteado como um grupo próprio; os valores centrados no
      local não mudam na réplica, então cada réplica sai das somas, ponderadas pela contagem do sorteio, dos produtos
      cruzados de cada local. ep = desvio-padrão das réplicas (ddof=1). Réplica com matriz singular é descartada e contada.
      Conferência: a regressão da amostra inteira é refeita com lib.fe_ols (erro CR1 por local).
  G7. Veredito: SINAL DE MÁQUINA se coef >= 0,5 e coef > 3 x ep (lido a partir de zero, como no F10). SEM SINAL se
      |coef| < 0,3 e ep <= 0,2. Senão INCONCLUSIVO. Só o lado positivo é sinal (como no F10, D11); um coeficiente negativo
      grande seria INCONCLUSIVO pela letra e iria para as pistas.
  Robustez e leituras descritivas, fixadas agora e fora do veredito:
    R1. Decomposição: só antiga (= dP do F10); antiga e I (= R3 do F10); antiga e perfil, sem I.
    R2. Perfil mais fino no lugar dos cinco: faixas 16-17, 18-24, 25-34, 45-59, 60-69, 70 ou mais (referência 35-44),
        mulher, e cada nível de escolaridade (referência ensino médio completo), com I.
    R3. Sem peso.
    R4. Só SP; sem SP (AM e MT).
    R5. Perfil só da seção principal (sem somar as agregadas); e sem as seções com agregação no 1º turno.
    R6. Só seções em que o total do perfil é igual aos aptos do 1º turno no bweb.
    R7. Fatia de Lula no 2º turno (P2) e virada (P2 - P) no lugar de P, com os mesmos regressores.
    R8. Calibração do método nas três UFs, onde não há antiga contra nova: UE2022 contra UE2020 nos locais que têm as duas,
        e UE2013 contra UE2015 nos locais que têm as duas, mesma regressão e mesmo bootstrap.
    R9. Cada modelo antigo separado (UE2013 contra novas; UE2015 contra novas).
    R10. Diferença antiga menos nova de cada variável de perfil no mesmo desenho do F10 (efeito fixo de local, peso L1+R1,
         bootstrap de locais), e a parte de dP que o perfil explica: soma dos coeficientes do perfil na regressão principal
         vezes as diferenças do perfil. Ao lado, a fração com biometria (QT_ELEITORES_BIOMETRIA), só descritiva.
  Zonas 420 de SP (SP|71072|420) e 70 de Manaus (AM|2550|70), pedido descritivo, sem critério de sinal:
    Z1. Seções da amostra do F10 nessas zonas. Para cada uma das cinco frações (G3): diferença antiga menos nova dentro do
        local (efeito fixo de local, peso L1+R1), e as médias simples de cada grupo ao lado.
    Z2. Incerteza: permutação do rótulo "antiga" entre as seções do mesmo local (mantém quantas antigas cada local tem),
        2.000 permutações, semente 20261031; p bilateral = (1 + permutações com |d| >= |d observado|) / 2.001. Teste
        conjunto: soma dos cinco (d_j / dp_j)^2, com dp_j o desvio-padrão de d_j nas permutações, p pela mesma regra.
        Na zona 420 (20 locais) sai também o ep por bootstrap de locais; em Manaus (3 locais) o bootstrap não informa e
        não é usado.
    Z3. Leitura fixada agora: "perfil diferente" se o p conjunto for menor que 0,05; "sem diferença detectada" se for 0,05
        ou mais. Ao lado: dP e dI da zona, a parte de dP que o perfil explica (coeficientes do perfil da regressão
        principal vezes os d_j da zona) e o coeficiente de antiga na regressão G5 feita só com as seções da zona (com o
        aviso de que em Manaus são 3 locais).

Acrescentado DEPOIS de ver o resultado (exploração, fora do registro e do veredito; como foi escolhida depois de ver os
números, não vale como teste e serve só para dizer onde olhar). Motivo: na zona 420, a seção com urna antiga costuma ser
uma só por local e ter eleitorado bem mais velho e com mais biometria que as novas do mesmo local, o que lembra seção
com acessibilidade.
    E1. Seção com acessibilidade (CD_SITU_SECAO_ACESSIBILIDADE = 1 no eleitorado por local de votação de 2026, 1º turno,
        https://cdn.tse.jus.br/estatistica/sead/odsele/eleitorado_locais_votacao/eleitorado_local_votacao_2026.zip):
        fração entre antigas e novas e diferença dentro do local (mesmo desenho e bootstrap), no todo e nas duas zonas.
    E2. Fração de eleitores com deficiência (QT_ELEITORES_DEFICIENCIA / QT_ELEITORES do perfil), a mesma diferença.
    E3. Regressão G5 com acessibilidade, deficiência e biometria acrescentadas (cada uma e as três), no todo e só em SP.
    E4. Regressão G5 sem a zona 70 de Manaus, sem a zona 420 de SP e sem as duas.
    O perfil passa a guardar também QT_ELEITORES_DEFICIENCIA (cache novo); a parte registrada não muda.

Uso: python3 -I analisar_F16.py <secoes2026.json.gz> <zips_bweb_1t> <consulta_cand_2026.zip> <F4_modelo_urna.json>
                                <cache_cargos.json.gz> <dir_perfil_secao> <F10_urnas_antigas_cargos.json> <dir_trabalho>
                                <saida.json> <saida.txt> [eleitorado_local_votacao_2026.zip]
"""
import os as _os, sys as _sys
_sys.path.insert(0, _os.path.dirname(_os.path.abspath(__file__)))
import collections, csv, glob, gzip, hashlib, io, json, math, os, sys, time, zipfile
from multiprocessing import Pool
import numpy as np
from lib import carregar, fe_ols
import analisar_F10 as F10

REPS = 2000
SEMENTE = 20261031
UFS = ('SP', 'AM', 'MT')
ANTIGAS = ('UE2013', 'UE2015')
NOVAS = ('UE2020', 'UE2022')
FAIXAS = [1600, 1700, 1800, 1900, 2000, 2124, 2529, 3034, 3539, 4044, 4549, 5054, 5559, 6064, 6569, 7074, 7579, 8084,
          8589, 9094, 9599, 9999]
# vetor de contagens por seção: 22 faixas + faixa_outra, gênero 2, 4, outro, escolaridade 1..8, outra, total, biometria
NF = len(FAIXAS)
IFX = {f: i for i, f in enumerate(FAIXAS)}
I_FX_OUT = NF
I_G2, I_G4, I_GO = NF + 1, NF + 2, NF + 3
I_E0 = NF + 4                     # escolaridade 1..8 em I_E0 + (c - 1)
I_EO = I_E0 + 8
I_TOT = I_EO + 1
I_BIO = I_TOT + 1
I_DEF = I_BIO + 1
NV = I_DEF + 1
PERFIL5 = ['jovem', 'idoso', 'mulher', 'superior', 'fund_inc']
FINO = ['a1617', 'a1824', 'a2534', 'a4559', 'a6069', 'a70', 'mulher', 'e1', 'e2', 'e3', 'e4', 'e5', 'e7', 'e8']
ZONAS = {'SP_zona_420': 'SP|71072|420', 'Manaus_zona_70': 'AM|2550|70'}


def log(*a):
    print('#', time.strftime('%H:%M:%S'), *a, file=sys.stderr, flush=True)


# ---------------------------------------------------------------- perfil do eleitorado por seção

def ler_perfil(zpath):
    S = {}
    LOC = {}
    nl = 0; fb = 0; ger = collections.Counter(); outros = collections.Counter()
    with zipfile.ZipFile(zpath) as z:
        nome = [n for n in z.namelist() if n.lower().endswith('.csv')][0]
        info = z.getinfo(nome)
        with z.open(nome) as fh:
            txt = io.TextIOWrapper(fh, encoding='latin1', newline='')
            cab = next(csv.reader([txt.readline()], delimiter=';'))
            ix = {c: i for i, c in enumerate(cab)}; n = len(cab)
            iU, iM, iZ, iS, iL = ix['SG_UF'], ix['CD_MUNICIPIO'], ix['NR_ZONA'], ix['NR_SECAO'], ix['NR_LOCAL_VOTACAO']
            iG, iF, iE, iQ, iB = ix['CD_GENERO'], ix['CD_FAIXA_ETARIA'], ix['CD_GRAU_ESCOLARIDADE'], ix['QT_ELEITORES'], ix['QT_ELEITORES_BIOMETRIA']
            iDf = ix['QT_ELEITORES_DEFICIENCIA']
            iD, iH = ix['DT_GERACAO'], ix['HH_GERACAO']
            for ln in txt:
                ln = ln.rstrip('\r\n')
                if not ln:
                    continue
                f = ln.split(';')
                if len(f) != n:
                    f = next(csv.reader([ln], delimiter=';')); fb += 1
                else:
                    f = [x[1:-1] if len(x) >= 2 and x[0] == '"' and x[-1] == '"' else x for x in f]
                nl += 1
                if nl % 200000 == 1:
                    ger[f[iD] + ' ' + f[iH]] += 1
                k = f'{f[iU]}|{int(f[iM])}|{int(f[iZ])}|{int(f[iS])}'
                v = S.get(k)
                if v is None:
                    v = S[k] = [0] * NV
                    LOC[k] = collections.Counter()
                q = int(f[iQ]); b = int(f[iB])
                LOC[k][int(f[iL])] += q
                j = IFX.get(int(f[iF]))
                if j is None:
                    v[I_FX_OUT] += q; outros['faixa ' + f[iF]] += q
                else:
                    v[j] += q
                g = f[iG]
                if g == '2':
                    v[I_G2] += q
                elif g == '4':
                    v[I_G4] += q
                else:
                    v[I_GO] += q; outros['genero ' + g] += q
                e = int(f[iE])
                if 1 <= e <= 8:
                    v[I_E0 + e - 1] += q
                else:
                    v[I_EO] += q; outros['escolaridade ' + f[iE]] += q
                v[I_TOT] += q; v[I_BIO] += b; v[I_DEF] += int(f[iDf])
    loc = {k: (c.most_common(1)[0][0], len(c)) for k, c in LOC.items()}
    meta = {'arquivo': os.path.basename(zpath), 'membro': nome, 'tamanho_csv': info.file_size,
            'data_hora_do_membro_no_zip': '%04d-%02d-%02d %02d:%02d:%02d' % info.date_time, 'linhas': nl,
            'linhas_lidas_pelo_csv': fb, 'geracao_amostrada': dict(ger), 'codigos_fora_das_listas': dict(outros),
            'secoes': len(S)}
    return zpath, S, loc, meta


def sha256(p):
    h = hashlib.sha256()
    with open(p, 'rb') as f:
        for b in iter(lambda: f.read(1 << 22), b''):
            h.update(b)
    return h.hexdigest()


def perfil_todas(pasta, trab):
    cache = os.path.join(trab, 'perfil_secao_SP_AM_MT_v2.json.gz')
    zips = [os.path.join(pasta, f'perfil_eleitor_secao_2026_{u}.zip') for u in UFS]
    hashes = {os.path.basename(p): sha256(p) for p in zips}
    if os.path.exists(cache):
        with gzip.open(cache, 'rt') as f:
            c = json.load(f)
        if c.get('hashes') == hashes:
            log('cache do perfil', cache)
            return c
    S = {}; LOC = {}; meta = {}
    with Pool(3) as p:
        for zp, s, loc, m in p.imap_unordered(ler_perfil, zips):
            log('perfil', os.path.basename(zp), m['linhas'], 'linhas', m['secoes'], 'seções')
            S.update(s); LOC.update(loc); meta[os.path.basename(zp)] = m
    c = {'hashes': hashes, 'S': S, 'LOC': LOC, 'meta': meta}
    os.makedirs(trab, exist_ok=True)
    with gzip.open(cache, 'wt') as f:
        json.dump(c, f, separators=(',', ':'))
    return c


def fracoes(v):
    v = np.asarray(v, float)
    fx = v[:NF]; nfx = fx.sum()
    gen = v[I_G2] + v[I_G4]
    esc = v[I_E0:I_E0 + 8]; nesc = esc.sum()
    o = {}
    pct = lambda a, b: 100 * a / b if b > 0 else np.nan
    o['jovem'] = pct(fx[:8].sum(), nfx)
    o['idoso'] = pct(fx[13:].sum(), nfx)
    o['mulher'] = pct(v[I_G4], gen)
    o['superior'] = pct(esc[7], nesc)
    o['fund_inc'] = pct(esc[:3].sum(), nesc)
    o['a1617'] = pct(fx[0:2].sum(), nfx); o['a1824'] = pct(fx[2:6].sum(), nfx); o['a2534'] = pct(fx[6:8].sum(), nfx)
    o['a3544'] = pct(fx[8:10].sum(), nfx); o['a4559'] = pct(fx[10:13].sum(), nfx); o['a6069'] = pct(fx[13:15].sum(), nfx)
    o['a70'] = pct(fx[15:].sum(), nfx)
    for c in range(1, 9):
        o[f'e{c}'] = pct(esc[c - 1], nesc)
    o['biometria'] = pct(v[I_BIO], v[I_TOT])
    o['deficiencia'] = pct(v[I_DEF], v[I_TOT])
    o['total_perfil'] = v[I_TOT]
    o['nao_informado'] = v[I_FX_OUT] + v[I_GO] + v[I_EO]
    return o


def juntar(X, d, P):
    """Perfil por seção (principal + agregadas do 1º turno) e perfil só da principal, alinhados a X['k']."""
    S, LOC = P['S'], P['LOC']
    n = len(X['k'])
    cols = PERFIL5 + ['a1617', 'a1824', 'a2534', 'a3544', 'a4559', 'a6069', 'a70'] + [f'e{c}' for c in range(1, 9)] + \
        ['biometria', 'deficiencia', 'total_perfil', 'nao_informado']
    A = {c: np.full(n, np.nan) for c in cols}
    A1 = {c: np.full(n, np.nan) for c in PERFIL5}
    agr = np.zeros(n, bool); falta_agr = np.zeros(n, bool); tem = np.zeros(n, bool)
    loc_ok = np.full(n, np.nan); n_agr = np.zeros(n)
    for i, k in enumerate(X['k']):
        if X['uf'][i] not in UFS:
            continue
        a = d[k]['1']
        uf, mun, zona, sec = k.split('|')
        ag = [x.strip() for x in a.get('agr', '').split('/') if x.strip()]
        agr[i] = bool(ag); n_agr[i] = len(ag)
        vs = []
        if k in S:
            vs.append(S[k])
        for s in ag:
            kk = f'{uf}|{mun}|{zona}|{int(s)}'
            if kk in S:
                vs.append(S[kk])
            else:
                falta_agr[i] = True
        if k not in S:
            continue
        tem[i] = True
        tot = np.sum(np.array(vs, float), axis=0)
        fr = fracoes(tot)
        for c in cols:
            A[c][i] = fr[c]
        fr1 = fracoes(S[k])
        for c in PERFIL5:
            A1[c][i] = fr1[c]
        loc_ok[i] = float(LOC[k][0] == a['loc'])
    return A, A1, {'agr': agr, 'falta_agr': falta_agr, 'tem': tem, 'loc_igual': loc_ok, 'n_agr': n_agr}


# ---------------------------------------------------------------- regressão com efeito fixo e bootstrap de locais

def coef(M, nomes, y, xs):
    p = {n_: i for i, n_ in enumerate(nomes)}
    ix = [p[x] for x in xs]
    A = M[np.ix_(ix, ix)]; bv = M[ix, p[y]]
    return np.linalg.solve(A, bv)


def reg(X, sel, t, y, xs, peso=True, reps=REPS, semente=SEMENTE):
    """y em [t] + xs, efeito fixo de local, só locais com t=1 e t=0. Devolve coeficientes e ep por bootstrap de locais."""
    vars_ = [y] + [x for x in xs if x != y]
    dz = F10.desenho(X, sel, t, vars_, peso)
    G = dz['G']
    if G < 2:
        return {'secoes': int(len(dz['idx'])), 'locais': G, 'erro': 'menos de 2 locais'}
    nomes = dz['nomes']; regs = ['t'] + list(xs)
    Mt = dz['M'].sum(0)
    try:
        b = coef(Mt, nomes, y, regs)
    except np.linalg.LinAlgError:
        return {'secoes': int(len(dz['idx'])), 'locais': G, 'erro': 'matriz singular'}
    rng = np.random.default_rng(semente)
    bs = []; desc = 0
    for _ in range(reps):
        c = np.bincount(rng.integers(0, G, G), minlength=G).astype(float)
        Mb = np.tensordot(c, dz['M'], axes=1)
        try:
            bb = coef(Mb, nomes, y, regs)
        except np.linalg.LinAlgError:
            desc += 1; continue
        if not np.all(np.isfinite(bb)):
            desc += 1; continue
        bs.append(bb)
    bs = np.array(bs)
    nm = ['antiga'] + list(xs)
    tt = t[dz['idx']]
    out = {'secoes': int(len(dz['idx'])), 'locais': int(G), 'secoes_t1': int(tt.sum()), 'secoes_t0': int((1 - tt).sum()),
           'peso': 'L1+R1' if peso else 'nenhum', 'replicas': reps, 'replicas_descartadas': desc, 'semente': semente,
           'coef': {n_: float(v) for n_, v in zip(nm, b)},
           'ep': {n_: float(v) for n_, v in zip(nm, bs.std(0, ddof=1))},
           'ic95': {n_: [float(np.percentile(bs[:, j], 2.5)), float(np.percentile(bs[:, j], 97.5))] for j, n_ in enumerate(nm)}}
    out['z_antiga'] = out['coef']['antiga'] / out['ep']['antiga'] if out['ep']['antiga'] > 0 else None
    out['_dz'] = dz; out['_bs'] = bs
    return out


def veredito(c, ep):
    if c >= 0.5 and c > 3 * ep:
        return 'SINAL DE MÁQUINA'
    if abs(c) < 0.3 and ep <= 0.2:
        return 'SEM SINAL'
    return 'INCONCLUSIVO'


def limpar(r):
    return {k: v for k, v in r.items() if not k.startswith('_')}


def dif_within(v, t, g, w):
    """Coeficiente de t na regressão de v em t com efeito fixo de grupo g (within ponderado)."""
    G = g.max() + 1
    sw = np.bincount(g, weights=w, minlength=G)
    tc = t - (np.bincount(g, weights=w * t, minlength=G) / sw)[g]
    vc = v - (np.bincount(g, weights=w * v, minlength=G) / sw)[g]
    return float(np.sum(w * tc * vc) / np.sum(w * tc * tc))


# ---------------------------------------------------------------- zonas 420 de SP e 70 de Manaus

def zona(X, idx, t, zchave, g_perfil, princ_coefs):
    zz = np.array(['|'.join(l.split('|')[:3]) for l in X['loc'][idx]])
    ii = idx[zz == zchave]
    locs = X['loc'][ii]; w = X['w'][ii]; tt = t[ii].astype(float)
    _, g = np.unique(locs, return_inverse=True)
    o = {'zona': zchave, 'secoes': int(len(ii)), 'locais': int(g.max() + 1), 'antigas': int(tt.sum()), 'novas': int((1 - tt).sum())}
    obs = {c: dif_within(X[c][ii], tt, g, w) for c in PERFIL5 + ['P', 'I', 'biometria']}
    med = {c: {'antigas': float(X[c][ii][tt == 1].mean()), 'novas': float(X[c][ii][tt == 0].mean())} for c in PERFIL5 + ['P', 'I', 'biometria']}
    rng = np.random.default_rng(SEMENTE)
    grupos = [np.where(g == j)[0] for j in range(g.max() + 1)]
    perm = np.zeros((REPS, len(PERFIL5) + 3))
    allc = PERFIL5 + ['P', 'I', 'biometria']
    for r in range(REPS):
        tp = tt.copy()
        for gi in grupos:
            tp[gi] = tt[gi][rng.permutation(len(gi))]
        perm[r] = [dif_within(X[c][ii], tp, g, w) for c in allc]
    sd = perm.std(0, ddof=1)
    pv = {c: float((1 + np.sum(np.abs(perm[:, j]) >= abs(obs[c]) - 1e-12)) / (REPS + 1)) for j, c in enumerate(allc)}
    k5 = len(PERFIL5)
    est_obs = float(sum((obs[c] / sd[j]) ** 2 for j, c in enumerate(PERFIL5)))
    est_perm = np.sum((perm[:, :k5] / sd[:k5]) ** 2, axis=1)
    p_conj = float((1 + np.sum(est_perm >= est_obs - 1e-12)) / (REPS + 1))
    o['diferenca_antiga_menos_nova'] = obs
    o['medias_simples'] = med
    o['permutacao'] = {'p_bilateral': pv, 'dp_permutacao': {c: float(sd[j]) for j, c in enumerate(allc)},
                       'estatistica_conjunta_5_fracoes': est_obs, 'p_conjunto': p_conj, 'permutacoes': REPS, 'semente': SEMENTE}
    o['leitura'] = 'perfil diferente' if p_conj < 0.05 else 'sem diferença detectada'
    o['parte_de_dP_explicada_pelo_perfil'] = float(sum(princ_coefs[c] * obs[c] for c in PERFIL5))
    # bootstrap de locais para a zona 420 (e regressão G5 só com a zona)
    sel = np.zeros(len(X['k']), bool); sel[ii] = True
    r = reg(X, sel, t, 'P', ['I'] + PERFIL5)
    o['regressao_G5_so_na_zona'] = limpar(r) if 'erro' not in r else r
    if o['locais'] >= 10:
        bsd = {}
        for c in PERFIL5:
            rr = reg(X, sel, t, c, [])
            bsd[c] = {'d': rr['coef']['antiga'], 'ep_bootstrap_locais': rr['ep']['antiga']}
        o['bootstrap_de_locais'] = bsd
    else:
        o['bootstrap_de_locais'] = 'não usado (menos de 10 locais)'
    # perfil por local
    pl = []
    for j, gi in enumerate(grupos):
        a_ = gi[tt[gi] == 1]; n_ = gi[tt[gi] == 0]
        e = {'local': str(locs[gi[0]]), 'antigas': int(len(a_)), 'novas': int(len(n_))}
        for c in PERFIL5 + ['P']:
            e[c] = [float(np.average(X[c][ii][a_], weights=w[a_])), float(np.average(X[c][ii][n_], weights=w[n_]))]
        pl.append(e)
    o['por_local_antigas_e_novas_ponderado'] = pl
    return o


# ---------------------------------------------------------------- exploração depois de ver o resultado (fora do registro)

def ler_locais(zpath):
    out = {}
    with zipfile.ZipFile(zpath) as z:
        for uf in UFS:
            r = csv.DictReader(io.TextIOWrapper(z.open(f'eleitorado_local_votacao_2026_{uf}.csv'), encoding='latin1', newline=''),
                               delimiter=';')
            for x in r:
                if x['NR_TURNO'] != '1':
                    continue
                k = f"{x['SG_UF']}|{int(x['CD_MUNICIPIO'])}|{int(x['NR_ZONA'])}|{int(x['NR_SECAO'])}"
                out[k] = (int(x['CD_SITU_SECAO_ACESSIBILIDADE']), int(x['QT_ELEITOR_SECAO']), int(x['NR_LOCAL_VOTACAO']))
    return out


def exploracao(X, ii, t, sel_a, arq_loc):
    loc = ler_locais(arq_loc)
    n = len(X['k']); ac = np.full(n, np.nan); mesmo_local = np.full(n, np.nan)
    for i in np.where(np.isin(X['uf'], UFS))[0]:
        v = loc.get(X['k'][i])
        if v:
            ac[i] = 100.0 * (v[0] == 1)
    for i in ii:
        v = loc.get(X['k'][i])
        if v:
            mesmo_local[i] = float(v[2] == int(X['loc'][i].split('|')[3]))
    X['acess'] = ac
    tt = t[ii]
    o = {'aviso': 'escolhida depois de ver o resultado; fora do registro e do veredito',
         'fonte': {'arquivo': os.path.basename(arq_loc), 'sha256': sha256(arq_loc)},
         'cobertura': {'amostra': int(len(ii)), 'com_acessibilidade_informada': int(np.isfinite(ac[ii]).sum()),
                       'local_igual_ao_da_base': int(np.nansum(mesmo_local[ii]))},
         'E1_fracao_com_acessibilidade_simples': {'antigas': float(np.nanmean(ac[ii][tt == 1])), 'novas': float(np.nanmean(ac[ii][tt == 0]))}}
    for c in ('acess', 'deficiencia', 'biometria'):
        r = reg(X, sel_a, t, c, [])
        o['E1_E2_diferenca_' + c] = {'d': r['coef']['antiga'], 'ep': r['ep']['antiga'], 'z': r['z_antiga']}
    zon = np.array(['|'.join(l.split('|')[:3]) for l in X['loc']], dtype=object)
    for nm, zc in ZONAS.items():
        jj = ii[zon[ii] == zc]
        tz = t[jj]
        _, g = np.unique(X['loc'][jj], return_inverse=True)
        o['E1_E2_' + nm] = {'antigas_com_acessibilidade': int(np.nansum(ac[jj][tz == 1] > 0)), 'antigas': int((tz == 1).sum()),
                            'novas_com_acessibilidade': int(np.nansum(ac[jj][tz == 0] > 0)), 'novas': int((tz == 0).sum()),
                            'dif_acess_dentro_do_local': dif_within(ac[jj], tz, g, X['w'][jj]),
                            'dif_deficiencia_dentro_do_local': dif_within(X['deficiencia'][jj], tz, g, X['w'][jj]),
                            'deficiencia_media_simples': [float(X['deficiencia'][jj][tz == 1].mean()), float(X['deficiencia'][jj][tz == 0].mean())]}
    base = ['I'] + PERFIL5
    e3 = {}
    for nome, extra in (('acess', ['acess']), ('deficiencia', ['deficiencia']), ('biometria', ['biometria']),
                        ('as_tres', ['acess', 'deficiencia', 'biometria'])):
        for rot, m in (('todos', sel_a), ('so_SP', sel_a & (X['uf'] == 'SP')), ('sem_SP', sel_a & (X['uf'] != 'SP'))):
            r = reg(X, m, t, 'P', base + extra)
            if 'coef' not in r:
                e3[f'{nome}|{rot}'] = r; continue
            e3[f'{nome}|{rot}'] = {'secoes': r['secoes'], 'locais': r['locais'], 'antiga': r['coef']['antiga'], 'ep': r['ep']['antiga'],
                                   'z': r['z_antiga'], 'extras': {x: [r['coef'][x], r['ep'][x]] for x in extra},
                                   'leitura_se_fosse_o_registrado': veredito(r['coef']['antiga'], r['ep']['antiga'])}
    o['E3_G5_com_extras'] = e3
    e4 = {}
    for rot, excl in (('sem_Manaus_70', ['AM|2550|70']), ('sem_SP_420', ['SP|71072|420']), ('sem_as_duas', list(ZONAS.values()))):
        r = reg(X, sel_a & ~np.isin(zon, excl), t, 'P', base)
        e4[rot] = {'secoes': r['secoes'], 'locais': r['locais'], 'antiga': r['coef']['antiga'], 'ep': r['ep']['antiga'], 'z': r['z_antiga'],
                   'leitura_se_fosse_o_registrado': veredito(r['coef']['antiga'], r['ep']['antiga'])}
    o['E4_G5_sem_zonas'] = e4
    return o


# ---------------------------------------------------------------- principal

def main():
    (arq_d, zdir, arq_cand, arq_f4, cache, dperf, arq_f10, trab, saida_json, saida_txt) = sys.argv[1:11]
    arq_loc = sys.argv[11] if len(sys.argv) > 11 else None
    A_, B_, fonte, _ = F10.campo_lula(arq_cand)
    cg = F10.extrair(zdir, cache)
    d = carregar(arq_d)
    mod, na_zona, fx = F10.faixas_F4(arq_f4)
    X, conf, _ = F10.montar(d, cg['secoes'], mod, na_zona, A_, B_)
    del cg
    log('seções na base', len(X['k']))
    antiga = np.isin(X['mod'], ANTIGAS); nova = np.isin(X['mod'], NOVAS)
    t_old = antiga.astype(float)
    sel_main = antiga | nova

    # G1: reconstrução da amostra do F10 e conferência
    base = F10.rodar(X, sel_main, t_old, [('principal', 'P', 'I', None, False)], ['P', 'I'], reps=2)
    dzb = base['_dz']; idx = dzb['idx']
    f10 = json.load(open(arq_f10))
    E10 = f10['principal']['estatisticas']['principal']
    cnt = collections.defaultdict(lambda: [0, 0])
    for l, a in zip(X['loc'][idx], t_old[idx]):
        cnt[l][0 if a == 1 else 1] += 1
    pl10 = {p['local']: [p['secoes_antigas'], p['secoes_novas']] for p in f10['por_local']}
    eb = base['estatisticas']['principal']
    g1 = {'secoes': int(len(idx)), 'locais': int(dzb['G']),
          'por_local_igual_ao_F10': {l: list(v) for l, v in cnt.items()} == pl10,
          'dP': eb['dP'], 'dI': eb['dI'], 'D': eb['D'], 'dP_F10': E10['dP'], 'dI_F10': E10['dI'], 'D_F10': E10['D']}
    ok = (g1['secoes'] == 1332 and g1['locais'] == 119 and g1['por_local_igual_ao_F10']
          and all(abs(g1[c] - g1[c + '_F10']) < 1e-9 for c in ('dP', 'dI', 'D')))
    g1['confere'] = bool(ok)
    log('G1', g1)
    if not ok:
        raise SystemExit('amostra do F10 não reproduzida')
    amostra = np.zeros(len(X['k']), bool); amostra[idx] = True

    # perfil
    P = perfil_todas(dperf, trab)
    A, A1, J = juntar(X, d, P)
    del d
    for c, v in A.items():
        X[c] = v
    for c, v in A1.items():
        X[c + '_so_principal'] = v
    # conferências da junção na amostra
    tem = J['tem']
    cj = {'secoes_da_amostra': int(amostra.sum()), 'com_perfil': int((amostra & tem).sum()),
          'sem_perfil': [str(k) for k in X['k'][amostra & ~tem]],
          'com_agregadas_no_1t': int((amostra & J['agr']).sum()),
          'agregada_sem_linha_no_perfil': int((amostra & J['falta_agr']).sum()),
          'local_do_perfil_igual_ao_do_1t': int(np.nansum(J['loc_igual'][amostra])),
          'local_do_perfil_diferente': [str(k) for k in X['k'][amostra & (J['loc_igual'] == 0)]]}
    dif = X['total_perfil'][amostra] - X['apt'][amostra]
    dif = dif[np.isfinite(dif)]
    cj['total_perfil_menos_aptos_1t'] = {'iguais': int((dif == 0).sum()), 'diferentes': int((dif != 0).sum()),
                                          'media': float(dif.mean()), 'min': float(dif.min()), 'max': float(dif.max()),
                                          'abs_acima_de_5pct_dos_aptos': int((np.abs(X['total_perfil'][amostra] - X['apt'][amostra])
                                                                              > 0.05 * X['apt'][amostra]).sum())}
    cj['nao_informados_na_amostra'] = float(np.nansum(X['nao_informado'][amostra]))
    cj['eleitores_no_perfil_na_amostra'] = float(np.nansum(X['total_perfil'][amostra]))
    # cobertura nas três UFs (para a calibração)
    tres = np.isin(X['uf'], UFS)
    cj['tres_UFs'] = {'secoes_na_base': int(tres.sum()), 'com_perfil': int((tres & tem).sum())}
    log('junção', {k: v for k, v in cj.items() if not isinstance(v, list)})

    # G5: regressão registrada
    sel_a = amostra & tem
    log('principal')
    princ = reg(X, sel_a, t_old, 'P', ['I'] + PERFIL5)
    c0, e0 = princ['coef']['antiga'], princ['ep']['antiga']
    ver = veredito(c0, e0)
    log('coef antiga', c0, 'ep', e0, ver)
    ii = princ['_dz']['idx']
    if len(ii) != int(sel_a.sum()):
        log('aviso: seções na regressão', len(ii), 'selecionadas', int(sel_a.sum()))
    r_lib = fe_ols(X['P'][ii], np.column_stack([t_old[ii], X['I'][ii]] + [X[c][ii] for c in PERFIL5]), X['loc'][ii], X['w'][ii],
                   ['antiga', 'I'] + PERFIL5)

    # robustez
    log('robustez')
    rob = {}
    rob['R1_so_antiga'] = reg(X, sel_a, t_old, 'P', [])
    rob['R1_antiga_e_I'] = reg(X, sel_a, t_old, 'P', ['I'])
    rob['R1_antiga_e_perfil_sem_I'] = reg(X, sel_a, t_old, 'P', PERFIL5)
    rob['R2_perfil_fino'] = reg(X, sel_a, t_old, 'P', ['I'] + FINO)
    rob['R3_sem_peso'] = reg(X, sel_a, t_old, 'P', ['I'] + PERFIL5, peso=False)
    rob['R4_so_SP'] = reg(X, sel_a & (X['uf'] == 'SP'), t_old, 'P', ['I'] + PERFIL5)
    rob['R4_sem_SP'] = reg(X, sel_a & (X['uf'] != 'SP'), t_old, 'P', ['I'] + PERFIL5)
    rob['R5_perfil_so_da_secao_principal'] = reg(X, sel_a, t_old, 'P', ['I'] + [c + '_so_principal' for c in PERFIL5])
    rob['R5_sem_secoes_com_agregacao'] = reg(X, sel_a & ~J['agr'], t_old, 'P', ['I'] + PERFIL5)
    rob['R6_perfil_igual_aos_aptos'] = reg(X, sel_a & (X['total_perfil'] == X['apt']), t_old, 'P', ['I'] + PERFIL5)
    rob['R7_presidente_2t'] = reg(X, sel_a & np.isfinite(X['P2']), t_old, 'P2', ['I'] + PERFIL5)
    rob['R7_virada'] = reg(X, sel_a & np.isfinite(X['virada']), t_old, 'virada', ['I'] + PERFIL5)
    novas3 = tres & tem & nova
    rob['R8_calibracao_UE2022_contra_UE2020'] = reg(X, novas3, (X['mod'] == 'UE2022').astype(float), 'P', ['I'] + PERFIL5)
    ant3 = tres & tem & antiga
    rob['R8_calibracao_UE2013_contra_UE2015'] = reg(X, ant3, (X['mod'] == 'UE2013').astype(float), 'P', ['I'] + PERFIL5)
    for m in ANTIGAS:
        s_ = sel_a & ((X['mod'] == m) | nova)
        rob[f'R9_{m}_contra_novas'] = reg(X, s_, (X['mod'] == m).astype(float), 'P', ['I'] + PERFIL5)
    for k_, r_ in rob.items():
        if 'coef' in r_:
            r_['leitura_pelo_criterio'] = veredito(r_['coef']['antiga'], r_['ep']['antiga'])

    # R10: diferenças do perfil e parte de dP explicada
    log('R10')
    difs = {}
    for c in PERFIL5 + ['biometria', 'a1617', 'a1824', 'a2534', 'a3544', 'a4559', 'a6069', 'a70'] + [f'e{j}' for j in range(1, 9)]:
        r_ = reg(X, sel_a, t_old, c, [])
        difs[c] = {'d': r_['coef']['antiga'], 'ep': r_['ep']['antiga'], 'ic95': r_['ic95']['antiga'], 'z': r_['z_antiga']}
    pc = princ['coef']
    expl = float(sum(pc[c] * difs[c]['d'] for c in PERFIL5))
    # bootstrap da parte explicada (mesmas réplicas: mesma semente e mesmo desenho)
    dz = princ['_dz']; Mz = dz['M']; nomes = dz['nomes']
    rng = np.random.default_rng(SEMENTE); G = dz['G']; ex_bs = []
    pidx = {n_: i for i, n_ in enumerate(nomes)}
    for _ in range(REPS):
        cc = np.bincount(rng.integers(0, G, G), minlength=G).astype(float)
        Mb = np.tensordot(cc, Mz, axes=1)
        try:
            bb = coef(Mb, nomes, 'P', ['t', 'I'] + PERFIL5)
        except np.linalg.LinAlgError:
            continue
        dd = [Mb[pidx['t'], pidx[c]] / Mb[pidx['t'], pidx['t']] for c in PERFIL5]
        ex_bs.append(sum(bb[2 + j] * dd[j] for j in range(len(PERFIL5))))
    ex_bs = np.array(ex_bs)
    decomp = {'dP_F10': E10['dP'], 'parte_do_perfil': expl, 'ep_parte_do_perfil': float(ex_bs.std(ddof=1)),
              'parte_do_I': float(pc['I'] * reg(X, sel_a, t_old, 'I', [])['coef']['antiga']),
              'coef_antiga': c0}

    # zonas
    log('zonas')
    zonas = {nm: zona(X, ii, t_old, zc, PERFIL5, pc) for nm, zc in ZONAS.items()}
    expl = None
    if arq_loc and os.path.exists(arq_loc):
        log('exploração posterior')
        expl = exploracao(X, ii, t_old, sel_a, arq_loc)

    # médias simples por modelo na amostra (descritivo)
    medias = {}
    for m in ('UE2013', 'UE2015', 'UE2020', 'UE2022'):
        s_ = X['mod'][ii] == m
        if s_.sum():
            medias[m] = {c: float(np.average(X[c][ii][s_], weights=X['w'][ii][s_])) for c in PERFIL5 + ['P', 'I', 'biometria']}
            medias[m]['secoes'] = int(s_.sum())

    out = {'teste': 'F16 do Adendo 22: urnas antigas com o perfil do eleitorado por seção',
           'registro': 'PRE-REGISTRO-2026-10-26.md, Adendo 22 (commit f12121e, 31/10/2026 14:52:48 UTC)',
           'veredito': ver, 'coef_antiga': c0, 'ep_antiga': e0, 'z_antiga': princ['z_antiga'],
           'criterio': 'sinal de máquina se coef >= +0,5 a mais de 3 erros-padrão; sem sinal se |coef| < 0,3 com ep <= 0,2; senão inconclusivo',
           'principal': limpar(princ),
           'conferencia_lib_fe_ols_CR1': r_lib,
           'G1_amostra_do_F10': g1,
           'juncao': cj,
           'robustez': {k: limpar(v) for k, v in rob.items()},
           'R10_diferencas_de_perfil_antiga_menos_nova': difs,
           'R10_decomposicao_de_dP': decomp,
           'medias_ponderadas_por_modelo_na_amostra': medias,
           'zonas': zonas,
           'exploracao_depois_de_ver_o_resultado_fora_do_registro': expl,
           'fontes':{'perfil': {k: {'sha256': P['hashes'][k], **P['meta'][k],
                                     'url': 'https://cdn.tse.jus.br/estatistica/sead/odsele/perfil_eleitor_secao/' + k}
                                 for k in P['hashes']},
                      'senado_campo_de_Lula': fonte, 'faixas_F4': fx, 'filtros_da_base_F10': conf}}
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


NOMES = {'antiga': 'antiga', 'I': 'índice I', 'jovem': '16 a 34', 'idoso': '60 ou mais', 'mulher': 'mulheres',
         'superior': 'superior completo', 'fund_inc': 'fundamental incompleto ou menos', 'biometria': 'com biometria',
         'acess': 'seção com acessibilidade', 'deficiencia': 'com deficiência',
         'P': 'fatia de Lula 1º turno', 'a1617': '16-17', 'a1824': '18-24', 'a2534': '25-34', 'a3544': '35-44',
         'a4559': '45-59', 'a6069': '60-69', 'a70': '70+', 'e1': 'analfabeto', 'e2': 'lê e escreve',
         'e3': 'fundamental incompleto', 'e4': 'fundamental completo', 'e5': 'médio incompleto', 'e6': 'médio completo',
         'e7': 'superior incompleto', 'e8': 'superior completo'}


def linha_reg(nome, r, so_antiga=False):
    if 'coef' not in r:
        return f'  {nome}: {r}'
    c, e = r['coef'], r['ep']
    s = (f"  {nome} ({fi(r['secoes'])} seções, {fi(r['locais'])} locais): antiga {fz(c['antiga'], 3)} (ep {fz(e['antiga'], 3)};"
         f" z {fz(r['z_antiga'], 1)}; IC95 {fz(r['ic95']['antiga'][0], 2)} a {fz(r['ic95']['antiga'][1], 2)})")
    if 'leitura_pelo_criterio' in r:
        s += f"; leitura pelo critério: {r['leitura_pelo_criterio']}"
    if not so_antiga and len(c) > 1:
        s += '; outros: ' + ', '.join(f"{NOMES.get(k, k)} {fz(v, 3)} ({fz(e[k], 3)})" for k, v in c.items() if k != 'antiga')
    return s


def escrever_txt(o, caminho):
    L = []; w = L.append
    P = o['principal']
    w(o['teste'])
    w(f"Registro: {o['registro']}. Script: scripts/analisar_F16.py.")
    w('')
    w(f"VEREDITO PELA LETRA: {o['veredito']}")
    w(f"  Coeficiente da urna antiga = {fz(o['coef_antiga'], 3)} ponto, erro-padrão por bootstrap de locais {fz(o['ep_antiga'], 3)}"
      f" ({P['replicas'] - P['replicas_descartadas']} réplicas válidas, semente {P['semente']}); z {fz(o['z_antiga'], 2)};"
      f" IC95 percentil {fz(P['ic95']['antiga'][0], 2)} a {fz(P['ic95']['antiga'][1], 2)}.")
    w('  Critério: ' + o['criterio'] + '.')
    w('')
    g = o['G1_amostra_do_F10']; j = o['juncao']
    w('1. Amostra e junção')
    w(f"  Amostra do F10 reconstruída com o código do F10: {fi(g['secoes'])} seções, {fi(g['locais'])} locais; contagens por local iguais às do F10:"
      f" {'sim' if g['por_local_igual_ao_F10'] else 'não'}; dP {fz(g['dP'], 3)}, dI {fz(g['dI'], 3)}, D {fz(g['D'], 3)} (F10: {fz(g['dP_F10'], 3)},"
      f" {fz(g['dI_F10'], 3)}, {fz(g['D_F10'], 3)}).")
    w(f"  Com perfil: {fi(j['com_perfil'])} de {fi(j['secoes_da_amostra'])}; sem perfil: {j['sem_perfil'] or 'nenhuma'}.")
    w(f"  Seções com agregadas no 1º turno: {fi(j['com_agregadas_no_1t'])} (agregada sem linha no perfil: {j['agregada_sem_linha_no_perfil']}).")
    t_ = j['total_perfil_menos_aptos_1t']
    w(f"  Total de eleitores no perfil (14/07/2026) contra aptos do 1º turno no bweb: iguais {fi(t_['iguais'])}, diferentes {fi(t_['diferentes'])}"
      f" (média {fz(t_['media'], 2)}, mínimo {fz(t_['min'], 0)}, máximo {fz(t_['max'], 0)}; diferença acima de 5% dos aptos: {t_['abs_acima_de_5pct_dos_aptos']}).")
    w(f"  Local de votação do perfil igual ao do 1º turno: {fi(j['local_do_perfil_igual_ao_do_1t'])}; diferente: {len(j['local_do_perfil_diferente'])}"
      + (f" ({', '.join(j['local_do_perfil_diferente'][:10])})" if j['local_do_perfil_diferente'] else '') + '.')
    w(f"  Eleitores no perfil das seções da amostra: {fi(j['eleitores_no_perfil_na_amostra'])}; com algum código não informado: {fi(j['nao_informados_na_amostra'])}.")
    w(f"  Três UFs (para a calibração): {fi(j['tres_UFs']['secoes_na_base'])} seções na base do F10, {fi(j['tres_UFs']['com_perfil'])} com perfil.")
    w('  Arquivos: ' + '; '.join(f"{k} (sha256 {v['sha256'][:16]}..., {fi(v['linhas'])} linhas, {fi(v['secoes'])} seções, CSV de"
                                f" {v['data_hora_do_membro_no_zip']}, geração {', '.join(v['geracao_amostrada'])})" for k, v in o['fontes']['perfil'].items()))
    w('')
    w('2. Regressão registrada (P em antiga, I e as cinco frações; efeito fixo de local; peso L1+R1)')
    w(linha_reg('principal', P))
    c = o['conferencia_lib_fe_ols_CR1']
    w('  Conferência com lib.fe_ols (CR1): ' + ', '.join(f"{NOMES.get(k, k)} {fz(v, 3)} ({fz(c['ep'][k], 3)})" for k, v in c['coef'].items()))
    w('')
    w('3. Perfil das seções antigas contra as novas do mesmo local (R10, efeito fixo de local, peso L1+R1, bootstrap de locais)')
    for k, v in o['R10_diferencas_de_perfil_antiga_menos_nova'].items():
        w(f"  {NOMES.get(k, k)}: {fz(v['d'], 3)} ponto (ep {fz(v['ep'], 3)}; z {fz(v['z'], 1)})")
    dc = o['R10_decomposicao_de_dP']
    w(f"  Decomposição: dP do F10 {fz(dc['dP_F10'], 3)} = parte do perfil {fz(dc['parte_do_perfil'], 3)} (ep {fz(dc['ep_parte_do_perfil'], 3)})"
      f" + parte do índice {fz(dc['parte_do_I'], 3)} + coeficiente da antiga {fz(dc['coef_antiga'], 3)}"
      f" (soma {fz(dc['parte_do_perfil'] + dc['parte_do_I'] + dc['coef_antiga'], 3)}).")
    w('  Médias ponderadas por modelo na amostra (sem efeito fixo, só descritivo): ' + '; '.join(
        f"{m}: " + ', '.join(f"{NOMES.get(k, k)} {fz(x[k])}" for k in PERFIL5 + ['P', 'I']) + f" ({fi(x['secoes'])} seções)"
        for m, x in o['medias_ponderadas_por_modelo_na_amostra'].items()))
    w('')
    w('4. Robustez (fora do veredito)')
    for k, r in o['robustez'].items():
        w(linha_reg(k, r, so_antiga=k not in ('R1_antiga_e_perfil_sem_I', 'R1_antiga_e_I')))
    w('')
    w('5. Zonas 420 de SP e 70 de Manaus: perfil das antigas contra as novas do mesmo local (pedido descritivo, sem critério de sinal)')
    for nm, z in o['zonas'].items():
        pm = z['permutacao']
        w(f"  {nm} ({z['zona']}): {z['secoes']} seções em {z['locais']} locais ({z['antigas']} antigas, {z['novas']} novas). Leitura fixada antes: {z['leitura'].upper()}"
          f" (p conjunto da permutação dentro do local {fz(pm['p_conjunto'], 4)}).")
        for k in PERFIL5 + ['biometria', 'P', 'I']:
            md = z['medias_simples'][k]
            w(f"    {NOMES.get(k, k)}: antiga menos nova {fz(z['diferenca_antiga_menos_nova'][k], 2)} ponto (p permutação {fz(pm['p_bilateral'][k], 4)};"
              f" dp permutação {fz(pm['dp_permutacao'][k], 2)}); médias simples antigas {fz(md['antigas'])}, novas {fz(md['novas'])}")
        w(f"    Parte da diferença em P que o perfil explica (coeficientes da regressão principal): {fz(z['parte_de_dP_explicada_pelo_perfil'], 3)} ponto.")
        rz = z['regressao_G5_so_na_zona']
        if 'coef' in rz:
            w('  ' + linha_reg('regressão G5 só nesta zona', rz, so_antiga=True).strip())
        if isinstance(z['bootstrap_de_locais'], dict):
            w('    Bootstrap de locais: ' + ', '.join(f"{NOMES.get(k, k)} {fz(v['d'], 2)} (ep {fz(v['ep_bootstrap_locais'], 2)})" for k, v in z['bootstrap_de_locais'].items()))
        else:
            w('    Bootstrap de locais: ' + z['bootstrap_de_locais'])
    w('')
    E = o.get('exploracao_depois_de_ver_o_resultado_fora_do_registro')
    if E:
        w('6. Exploração DEPOIS de ver o resultado (fora do registro e do veredito; escolhida depois, não vale como teste)')
        cb = E['cobertura']
        w(f"  Fonte: {E['fonte']['arquivo']} (sha256 {E['fonte']['sha256'][:16]}...). Seções da amostra com acessibilidade informada:"
          f" {fi(cb['com_acessibilidade_informada'])} de {fi(cb['amostra'])}; local igual ao da base: {fi(cb['local_igual_ao_da_base'])}.")
        s = E['E1_fracao_com_acessibilidade_simples']
        w(f"  E1. Seções com acessibilidade: antigas {fz(s['antigas'], 1)}%, novas {fz(s['novas'], 1)}% (médias simples).")
        for c in ('acess', 'deficiencia', 'biometria'):
            x = E['E1_E2_diferenca_' + c]
            w(f"  E1/E2. Diferença antiga menos nova dentro do local em {({'acess': 'acessibilidade (pontos percentuais)', 'deficiencia': 'fração com deficiência', 'biometria': 'fração com biometria'})[c]}:"
              f" {fz(x['d'], 3)} (ep {fz(x['ep'], 3)}; z {fz(x['z'], 1)})")
        for nm in ZONAS:
            x = E['E1_E2_' + nm]
            w(f"  E1/E2 {nm}: antigas com acessibilidade {x['antigas_com_acessibilidade']} de {x['antigas']}; novas {x['novas_com_acessibilidade']} de {x['novas']};"
              f" diferença dentro do local em acessibilidade {fz(x['dif_acess_dentro_do_local'], 1)} pontos; em deficiência {fz(x['dif_deficiencia_dentro_do_local'], 2)} ponto"
              f" (médias simples {fz(x['deficiencia_media_simples'][0], 2)} e {fz(x['deficiencia_media_simples'][1], 2)}).")
        for k, x in E['E3_G5_com_extras'].items():
            if 'antiga' not in x:
                w(f'  E3 {k}: {x}'); continue
            w(f"  E3 G5 + {k} ({fi(x['secoes'])} seções, {fi(x['locais'])} locais): antiga {fz(x['antiga'], 3)} (ep {fz(x['ep'], 3)}; z {fz(x['z'], 1)});"
              f" extras " + ', '.join(f"{NOMES.get(a, a)} {fz(b[0], 3)} ({fz(b[1], 3)})" for a, b in x['extras'].items())
              + f"; leitura se fosse o registrado: {x['leitura_se_fosse_o_registrado']}")
        for k, x in E['E4_G5_sem_zonas'].items():
            w(f"  E4 G5 {k} ({fi(x['secoes'])} seções, {fi(x['locais'])} locais): antiga {fz(x['antiga'], 3)} (ep {fz(x['ep'], 3)}; z {fz(x['z'], 1)});"
              f" leitura se fosse o registrado: {x['leitura_se_fosse_o_registrado']}")
        w('')
    w('Desvios declarados (decisões que o registro não fixa, tomadas antes de calcular): ver o docstring do script, G1 a G7, R1 a R10 e Z1 a Z3.'
      ' A exploração E1 a E4 foi acrescentada depois de ver o resultado.')
    txt = '\n'.join(L) + '\n'
    for ch in (chr(0x2014), chr(0x2013)):
        txt = txt.replace(ch, '-')
    with open(caminho, 'w') as f:
        f.write(txt)


if __name__ == '__main__':
    main()
