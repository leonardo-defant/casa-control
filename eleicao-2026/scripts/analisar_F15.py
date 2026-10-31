"""F15 do pré-registro (Adendo 21, commit 913af7a, 31/10/2026 10:36:29 UTC): quem foi votar a mais, perfil do comparecimento.

Letra do registro
  - Dado aberto do TSE de comparecimento e abstenção por zona, faixa etária, gênero e escolaridade, nos dois turnos de 2026.
  - (a) Conferência: comparecimento por zona no perfil contra a soma do bweb. Sinal: alguma zona com diferença acima de 0,5%
    sem explicação.
  - (b) Entre as zonas da mesma UF, relação entre a variação do comparecimento de 16 a 34 anos (em pontos) e a virada de Lula
    na zona, ponderada pelos votos dos finalistas. Incoerência: inclinação negativa a mais de 3 erros-padrão. Coerente:
    positiva a mais de 3 erros-padrão. Entre os dois: inconclusivo.
  - (c) Descritivo: variação do comparecimento por faixa etária, gênero e escolaridade no país.

O que existe no portal (verificado em 31/10/2026, antes de escrever estas decisões)
  - Conjunto CKAN "comparecimento-e-abstencao-2026" (criado 21/10/2026 13:19 UTC, sem alteração depois), recurso
    cdn.tse.jus.br/estatistica/sead/odsele/perfil_comparecimento_abstencao/perfil_comparecimento_abstencao_2026.zip
    (Last-Modified 21/10/2026 16:40:26 GMT, 229.213.668 bytes, sha256 abd1af8f...f034). Todas as linhas de todos os CSVs têm
    NR_TURNO = 1 e DT_GERACAO = 13/10/2026. Não há o 2º turno: o arquivo é anterior a 25/10.
  - O mesmo vale para os arquivos de transferência temporária (TTE) e de pessoas com deficiência do mesmo conjunto.
  - O painel de estatísticas do TSE (sig.tse.jus.br) responde 403 (Akamai, "Access Denied"); não foi contornado.
  - O detalhe da apuração por município e zona (detalhe_votacao_munzona_2026.zip, Last-Modified 30/10/2026 22:46:49 GMT)
    já traz o 2º turno, mas sem perfil (só aptos, comparecimento, abstenção e votos por zona).
  - O perfil do eleitorado por seção (perfil_eleitor_secao_2026_<UF>.zip, gerado em 14/07/2026) traz aptos por seção, faixa
    etária, gênero e escolaridade; não traz comparecimento.
  Por isso: (a) roda no 1º turno; (b) e a variação de (c) não rodam pela letra (SEM DADO); o script roda tudo sozinho quando o
  arquivo do perfil passar a trazer NR_TURNO = 2. Ao lado, fora do critério, uma estimativa ecológica (X abaixo).

Decisões que o registro não fixa (escritas aqui antes de calcular qualquer número de (a), (b), (c) ou X; declaradas como desvio)
  A1. Zona = UF|NR_ZONA (a zona eleitoral; o perfil vem por UF|município|zona e as linhas dos municípios da zona são somadas).
      Leitura secundária, mais fina: UF|município|zona. O exterior (ZZ) entra como mais uma "UF".
  A2. Perfil: soma de QT_COMPARECIMENTO (e de QT_APTOS, descritivo) de todas as linhas da zona nos CSVs por UF (o _BRASIL.csv
      fica de fora da soma e é conferido contra a soma das UFs). Linhas com QT_APTOS diferente de QT_COMPARECIMENTO +
      QT_ABSTENCAO são contadas.
  A3. bweb: lido aqui mesmo dos zips de cada turno (bweb1t/zips e trab2t/zips2t), linhas do cargo 1 (Presidente),
      QT_COMPARECIMENTO e QT_APTOS uma vez por seção (UF|município|zona|seção); as linhas da mesma seção têm de concordar
      (discordâncias contadas). Conferência: seções e somas contra secoes2026.json.gz.
  A4. Diferença d = perfil - bweb; relativa r = d / bweb da zona. "Acima de 0,5%": |r| > 0,005. Zona presente só num dos dois
      lados: |r| = 100%.
  A5. Explicações aceitas, fixadas antes da comparação (qualquer outra coisa é "sem explicação"):
      E1 (transferência temporária): o eleitor com TTE (voto em trânsito, preso provisório, militar ou policial em serviço,
         mesário, etc.) vota numa seção da zona de destino, e o perfil pode contá-lo na zona de origem. Ajuste:
         perfil_aj(z) = perfil(z) - comparecimento TTE com origem z + comparecimento TTE com destino z, pelo arquivo
         perfil_comparecimento_abstencao_eleitor_tte_2026 do mesmo turno (todos os tipos somados; o leiame admite que o
         mesmo eleitor apareça em dois tipos, o que não dá para separar). A zona com |r| > 0,5% fica explicada por E1 se
         |r_aj| <= 0,5%.
      E2 (seção não instalada): a zona tem eleitores em seções não instaladas no detalhe_votacao_munzona do mesmo turno
         (cargo 1) e |d| e |d_aj| (o menor) não passam desse número.
      Sinal de (a), por turno: alguma zona com |r| > 0,5% e |r_aj| > 0,5% e não coberta por E2. Sem sinal: nenhuma. (O
      registro não escreve o "sem sinal"; aqui é o complemento.) Descritivo ao lado: se o QT_COMPARECIMENTO_TTE do perfil por
      zona bate com a soma do arquivo TTE por origem ou por destino (diz em que zona o perfil põe o eleitor transferido).
  A6. Fora do critério: comparecimento por zona do detalhe_votacao_munzona_2026 (arquivo _BR.csv, cargo 1, que tem os dois
      turnos) contra a soma do bweb, com a mesma régua de 0,5%. Não é o perfil; é a única conferência por zona que existe
      para o 2º turno.
  B1. (b), quando houver o 2º turno no perfil: zonas UF|NR_ZONA das 27 UFs (exterior fora), presentes nos dois turnos do perfil
      e na base, com aptos de 16 a 34 anos e votos de finalistas positivos nos dois turnos.
  B2. x = 100 (C2/A2 - C1/A1), C e A = soma de QT_COMPARECIMENTO e QT_APTOS das faixas 1600, 1700, 1800, 1900, 2000, 2124,
      2529 e 3034 (16 a 34 anos) na zona, em cada turno (pontos).
  B3. y = virada de Lula = 100 L2/(L2+R2) - 100 L1/(L1+R1), com L (13) e R (22) somados nas seções da zona que têm os dois
      turnos em secoes2026.json.gz. Peso L2+R2 da zona.
  B4. Regressão de y em x com efeito fixo de UF ("entre as zonas da mesma UF"), peso L2+R2, erro-padrão agrupado por UF
      (lib.fe_ols, CR1, 27 grupos). Leitura alternativa: erro robusto HC1 (cada zona é um grupo); se ela mudar o veredito,
      isso é dito, mas vale a principal.
  B5. Veredito: INCOERÊNCIA se coef < 0 e |coef| > 3 ep; COERENTE se coef > 0 e coef > 3 ep; senão INCONCLUSIVO.
  C1. (c) "No país" = 27 UFs, exterior numa linha à parte. Taxa = QT_COMPARECIMENTO / QT_APTOS por grupo e turno; variação em
      pontos (2º menos 1º); parcela do aumento líquido = (C2 - C1 do grupo) / (C2 - C1 total). Grupos: cada faixa etária do
      TSE e faixas somadas (16-17, 18-24, 25-34, 35-44, 45-59, 60-69, 70-79, 80 ou mais), CD_GENERO, CD_GRAU_INSTRUCAO.
      Códigos inválidos ou não informados ficam como grupo próprio. Sem o 2º turno, (c) relata só as taxas do 1º turno.
  X. Estimativa ecológica, fora do critério, sem veredito (só indicação enquanto o TSE não publica o perfil do 2º turno):
  X1. Composição etária de cada seção: QT_ELEITORES do perfil_eleitor_secao_2026 por faixa, em quatro grupos: J = 16 a 34,
      M = 35 a 59, V = 60 a 69, W = 70 ou mais. Faixa inválida fora do denominador.
  X2. Seções da base (27 UFs) com os dois turnos e aptos positivos nos dois. Seção principal soma o perfil das seções
      agregadas a ela (campo agr da base; se a agregação mudar entre os turnos, a seção sai). Seção sem perfil (voto em
      trânsito e seções criadas depois de julho) sai. Contagens relatadas.
  X3. T1 = comp1/apt1 e T2 = comp2/apt2 da seção (bweb); D = T2 - T1.
  X4. Por zona (UF|NR_ZONA), MQO ponderado por apt2, sem intercepto, de T1 sobre as quatro frações (Goodman) dá t1 estimado
      por grupo; o mesmo com D dá a variação estimada por grupo. Só zonas com 30 seções ou mais e matriz com número de
      condição abaixo de 1e8.
  X5. Calibração no 1º turno, contra o perfil verdadeiro do 1º turno: por zona, t1 estimado de J contra o C1/A1 de 16 a 34
      do perfil (correlação ponderada por A1 de J, erro médio absoluto ponderado em pontos, inclinação do verdadeiro sobre o
      estimado); o mesmo para M, V e W; e o agregado nacional de cada grupo. A estimativa do 2º turno só é comentada se a
      calibração de J tiver correlação de 0,5 ou mais e erro médio absoluto de 5 pontos ou menos; senão é declarada
      imprestável.
  X6. Indicação para (b): a regressão de B4 com x = 100 x variação estimada de J na zona (mesmo peso, efeito fixo e erro).
      Erro de medida em x puxa o coeficiente para zero. Relatado com coef, ep e a leitura que a régua de B5 daria, marcada
      como exploratória.
  X7. Indicação para (c): variação estimada nacional por grupo = média das variações estimadas das zonas ponderada pelos
      eleitores do grupo nas seções usadas.
  X8. Dentro do local, todas as seções: regressão de D (e de T1, para calibrar) nas frações J, V e W (M como referência), com
      efeito fixo de local de votação (lib.chave_local, 2º turno), peso apt2, erro agrupado por local. Mede se o comparecimento
      subiu mais nas seções com mais jovens do mesmo prédio. A calibração compara o coeficiente de T1 com as diferenças
      nacionais verdadeiras do 1º turno (t de J menos t de M, etc.).
  X9. Ao lado, descritivo: y de B3 contra a variação total do comparecimento da zona no bweb (pontos), mesma regressão.

Acrescentado depois de rodar (31/10/2026, entre 12h41 e 12h50 UTC, depois de ver o resultado; pós-hoc, sem correção de múltiplos
testes, não muda nenhum veredito; as decisões acima não foram alteradas):
  P1. Resíduo de todas as zonas depois do ajuste E1 (não só as acima de 0,5%), com o município de cada resíduo positivo de 10
      ou mais e o nome dele (detalhe_votacao_munzona).
  P2. Exterior: cidades em que o perfil marca comparecimento igual aos aptos do perfil e o bweb registra menos, e cidades sem
      boletim com comparecimento no perfil.
  P3. Virada de Lula na seção contra as frações J, V e W (M como referência), efeito fixo de local, peso L2+R2, erro agrupado
      por local, com e sem a variação do comparecimento da seção; e virada da zona contra a variação estimada de cada grupo
      (X4), efeito fixo de UF, peso L2+R2, erro agrupado por UF.
  Rótulos: código 0 de gênero e instrução = "não informado" (visto no CSV de SP depois de rodar).

Uso:
  python3 -I analisar_F15.py rodar <perfil.zip> <tte.zip> <munzona.zip> <dir zips 1T> <dir zips 2T> <secoes2026.json.gz>
                                   <dir perfil_eleitor_secao> <dir trabalho> <saida.json> <saida.txt>
  Os passos pesados guardam cache em <dir trabalho> (apague para refazer).
"""
import os as _os, sys as _sys
_sys.path.insert(0, _os.path.dirname(_os.path.abspath(__file__)))
import collections, csv, glob, gzip, hashlib, io, json, math, os, pickle, re, sys, time, zipfile
from multiprocessing import Pool
import numpy as np
import lib

FX_J = {1600, 1700, 1800, 1900, 2000, 2124, 2529, 3034}
FX_M = {3539, 4044, 4549, 5054, 5559}
FX_V = {6064, 6569}
FAIXAS_AGR = [('16-17', {1600, 1700}), ('18-24', {1800, 1900, 2000, 2124}), ('25-34', {2529, 3034}),
              ('35-44', {3539, 4044}), ('45-59', {4549, 5054, 5559}), ('60-69', {6064, 6569}),
              ('70-79', {7074, 7579}), ('80 ou mais', {8084, 8589, 9094, 9599, 9999})]
GRUPOS_X = ['J', 'M', 'V', 'W']


def grupo_x(fx):
    if fx in FX_J: return 0
    if fx in FX_M: return 1
    if fx in FX_V: return 2
    if fx >= 7074: return 3
    return 4  # inválido


def sha256(p):
    h = hashlib.sha256()
    with open(p, 'rb') as f:
        for b in iter(lambda: f.read(1 << 20), b''):
            h.update(b)
    return h.hexdigest()


def linhas(fh, ncols):
    """Linhas de um CSV do TSE (latin1, ';', aspas): caminho rápido por split, csv quando o número de campos não bate."""
    txt = io.TextIOWrapper(fh, encoding='latin1', newline='')
    cab = next(csv.reader([txt.readline()], delimiter=';'))
    yield cab
    n = len(cab)
    for ln in txt:
        ln = ln.rstrip('\r\n')
        if not ln:
            continue
        f = ln.split(';')
        if len(f) != n:
            f = next(csv.reader([ln], delimiter=';'))
        else:
            f = [x[1:-1] if len(x) >= 2 and x[0] == '"' and x[-1] == '"' else x for x in f]
        yield f


# ---------------------------------------------------------------- perfil de comparecimento
def ler_perfil_uf(args):
    zpath, nome = args
    Z = collections.defaultdict(lambda: [0, 0, 0, 0, 0])      # (t, UF|mun|zona) -> apt, comp, abst, comp_tte, abst_tte
    ZF = collections.defaultdict(lambda: [0, 0])              # (t, UF|zona, fx) -> apt, comp
    N = collections.defaultdict(lambda: [0, 0])               # (t, uf, dim, cod) -> apt, comp
    ruins = 0; nl = 0; ger = collections.Counter()
    with zipfile.ZipFile(zpath) as z, z.open(nome) as fh:
        it = linhas(fh, None)
        cab = next(it); ix = {c: i for i, c in enumerate(cab)}
        iT, iU, iM, iZ = ix['NR_TURNO'], ix['SG_UF'], ix['CD_MUNICIPIO'], ix['NR_ZONA']
        iF, iG, iI = ix['CD_FAIXA_ETARIA'], ix['CD_GENERO'], ix['CD_GRAU_INSTRUCAO']
        iA, iC, iB = ix['QT_APTOS'], ix['QT_COMPARECIMENTO'], ix['QT_ABSTENCAO']
        iCT, iBT = ix['QT_COMPARECIMENTO_TTE'], ix['QT_ABSTENCAO_TTE']
        iDG = ix['DT_GERACAO']
        for r in it:
            nl += 1
            t = int(r[iT]); uf = r[iU]; mun = int(r[iM]); zona = int(r[iZ])
            a, c, b = int(r[iA]), int(r[iC]), int(r[iB])
            ct, bt = int(r[iCT]), int(r[iBT])
            if a != c + b: ruins += 1
            ger[r[iDG]] += 1
            v = Z[(t, f'{uf}|{mun}|{zona}')]
            v[0] += a; v[1] += c; v[2] += b; v[3] += ct; v[4] += bt
            fx = int(r[iF])
            w = ZF[(t, f'{uf}|{zona}', fx)]; w[0] += a; w[1] += c
            for dim, cod in (('fx', fx), ('g', int(r[iG])), ('i', int(r[iI]))):
                u = N[(t, uf, dim, cod)]; u[0] += a; u[1] += c
    return nome, dict(Z), dict(ZF), dict(N), ruins, nl, dict(ger)


def ler_perfil_brasil(args):
    zpath, nome = args
    S = collections.defaultdict(lambda: [0, 0, 0]); nl = 0
    with zipfile.ZipFile(zpath) as z, z.open(nome) as fh:
        it = linhas(fh, None)
        cab = next(it); ix = {c: i for i, c in enumerate(cab)}
        iT, iU, iA, iC = ix['NR_TURNO'], ix['SG_UF'], ix['QT_APTOS'], ix['QT_COMPARECIMENTO']
        for r in it:
            nl += 1
            v = S[(int(r[iT]), r[iU])]; v[0] += int(r[iA]); v[1] += int(r[iC]); v[2] += 1
    return nome, dict(S), nl


def ler_tte(zpath):
    O = collections.defaultdict(int); D = collections.defaultdict(int)       # (t, chave) -> comp
    O2 = collections.defaultdict(int); D2 = collections.defaultdict(int)
    tipos = collections.Counter(); nl = 0
    with zipfile.ZipFile(zpath) as z:
        nome = [n for n in z.namelist() if n.lower().endswith('.csv')][0]
        with z.open(nome) as fh:
            it = linhas(fh, None)
            cab = next(it); ix = {c: i for i, c in enumerate(cab)}
            for r in it:
                nl += 1
                t = int(r[ix['NR_TURNO']]); c = int(r[ix['QT_COMPARECIMENTO_TTE']])
                uo, mo, zo = r[ix['SG_UF_ORIGEM']], int(r[ix['CD_MUNICIPIO_ORIGEM']]), int(r[ix['NR_ZONA_ORIGEM']])
                ud, md, zd = r[ix['SG_UF_DESTINO']], int(r[ix['CD_MUNICIPIO_DESTINO']]), int(r[ix['NR_ZONA_DESTINO']])
                O[(t, f'{uo}|{zo}')] += c; D[(t, f'{ud}|{zd}')] += c
                O2[(t, f'{uo}|{mo}|{zo}')] += c; D2[(t, f'{ud}|{md}|{zd}')] += c
                tipos[(t, r[ix['DS_TIPO_TRANSFERENCIA']])] += c
    return {'O': dict(O), 'D': dict(D), 'O2': dict(O2), 'D2': dict(D2),
            'tipos': {f'{k[0]}|{k[1]}': v for k, v in tipos.items()}, 'linhas': nl}


def ler_munzona(zpath):
    M = collections.defaultdict(lambda: [0, 0, 0, 0])   # (t, UF|mun|zona) -> apt, comp, eleitores não instaladas, seções não instaladas
    with zipfile.ZipFile(zpath) as z:
        with z.open('detalhe_votacao_munzona_2026_BR.csv') as fh:
            it = linhas(fh, None)
            cab = next(it); ix = {c: i for i, c in enumerate(cab)}
            for r in it:
                if r[ix['CD_CARGO']] != '1':
                    continue
                t = int(r[ix['NR_TURNO']])
                k = f"{r[ix['SG_UF']]}|{int(r[ix['CD_MUNICIPIO']])}|{int(r[ix['NR_ZONA']])}"
                v = M[(t, k)]
                v[0] += int(r[ix['QT_APTOS']]); v[1] += int(r[ix['QT_COMPARECIMENTO']])
                v[2] += int(r[ix['QT_ELEITORES_SECOES_NAO_INSTALADAS']]); v[3] += int(r[ix['QT_SECOES_NAO_INSTALADAS']])
    return dict(M)


# ---------------------------------------------------------------- bweb
def ler_bweb_zip(zpath):
    S = {}; disc = 0; turnos = collections.Counter()
    with zipfile.ZipFile(zpath) as z:
        nome = [n for n in z.namelist() if n.lower().endswith('.csv')][0]
        with z.open(nome) as fh:
            it = linhas(fh, None)
            cab = [c.strip().replace('SG_ UF', 'SG_UF') for c in next(it)]
            ix = {c: i for i, c in enumerate(cab)}
            iC = ix['CD_CARGO_PERGUNTA']; iU, iM, iZ, iS = ix['SG_UF'], ix['CD_MUNICIPIO'], ix['NR_ZONA'], ix['NR_SECAO']
            iA, iP, iT = ix['QT_APTOS'], ix['QT_COMPARECIMENTO'], ix['NR_TURNO']
            for r in it:
                if r[iC] != '1':
                    continue
                k = f'{r[iU]}|{int(r[iM])}|{int(r[iZ])}|{int(r[iS])}'
                v = (int(r[iA]), int(r[iP]))
                turnos[r[iT]] += 1
                o = S.get(k)
                if o is None:
                    S[k] = v
                elif o != v:
                    disc += 1
    return zpath, S, disc, dict(turnos)


# ---------------------------------------------------------------- perfil do eleitorado por seção
def ler_perfil_secao(zpath):
    S = collections.defaultdict(lambda: [0, 0, 0, 0, 0])
    nl = 0
    with zipfile.ZipFile(zpath) as z:
        nome = [n for n in z.namelist() if n.lower().endswith('.csv')][0]
        with z.open(nome) as fh:
            it = linhas(fh, None)
            cab = next(it); ix = {c: i for i, c in enumerate(cab)}
            iU, iM, iZ, iS = ix['SG_UF'], ix['CD_MUNICIPIO'], ix['NR_ZONA'], ix['NR_SECAO']
            iF, iQ = ix['CD_FAIXA_ETARIA'], ix['QT_ELEITORES']
            for r in it:
                nl += 1
                k = f'{r[iU]}|{int(r[iM])}|{int(r[iZ])}|{int(r[iS])}'
                S[k][grupo_x(int(r[iF]))] += int(r[iQ])
    return zpath, dict(S), nl


# ---------------------------------------------------------------- estatística
def fe_hc1(y, X, fe, w):
    """Efeito fixo (within) com erro HC1 (cada observação é um grupo)."""
    y = np.asarray(y, float); X = np.asarray(X, float)
    if X.ndim == 1: X = X[:, None]
    _, g = np.unique(fe, return_inverse=True)
    Z = lib.demean(np.column_stack([y, X]), g, w)
    yd, Xd = Z[:, 0], Z[:, 1:]
    sw = np.sqrt(w)
    Xw, yw = Xd * sw[:, None], yd * sw
    XtX = Xw.T @ Xw
    b = np.linalg.solve(XtX, Xw.T @ yw)
    e = yd - Xd @ b
    inv = np.linalg.inv(XtX)
    meat = (Xd * (w * e)[:, None]).T @ (Xd * (w * e)[:, None])
    n, k = Xd.shape
    G = g.max() + 1
    V = n / (n - k - G) * inv @ meat @ inv
    return b, np.sqrt(np.diag(V))


def wcorr(a, b, w):
    a = np.asarray(a, float); b = np.asarray(b, float); w = np.asarray(w, float)
    ma, mb = np.average(a, weights=w), np.average(b, weights=w)
    va = np.average((a - ma) ** 2, weights=w); vb = np.average((b - mb) ** 2, weights=w)
    return float(np.average((a - ma) * (b - mb), weights=w) / math.sqrt(va * vb))


def wslope(yv, xv, w):
    X = np.column_stack([np.ones(len(xv)), xv]); W = np.asarray(w, float)
    b = np.linalg.solve(X.T @ (X * W[:, None]), X.T @ (W * yv))
    return float(b[1]), float(b[0])


def veredito_b(coef, ep):
    if coef < 0 and abs(coef) > 3 * ep: return 'INCOERÊNCIA'
    if coef > 0 and coef > 3 * ep: return 'COERENTE'
    return 'INCONCLUSIVO'


def cache(trab, nome, fn):
    p = os.path.join(trab, nome)
    if os.path.exists(p):
        with gzip.open(p, 'rb') as f:
            return pickle.load(f)
    t0 = time.time(); v = fn()
    with gzip.open(p, 'wb') as f:
        pickle.dump(v, f)
    print(f'  {nome}: {time.time() - t0:.0f}s', flush=True)
    return v


def pct(x, nd=2):
    return f'{x:.{nd}f}'.replace('.', ',')


def milhar(n):
    return f'{n:,}'.replace(',', '.')


# ---------------------------------------------------------------- passos
def passo_perfil(zperfil):
    nomes = [n for n in zipfile.ZipFile(zperfil).namelist() if n.lower().endswith('.csv')]
    ufs = sorted(n for n in nomes if not n.endswith('_BRASIL.csv'))
    bra = [n for n in nomes if n.endswith('_BRASIL.csv')]
    Z, ZF, N = {}, {}, {}
    ruins = 0; nl = 0; ger = collections.Counter(); bras = None
    with Pool(4) as p:
        rb = p.map_async(ler_perfil_brasil, [(zperfil, n) for n in bra])
        for nome, z, zf, n, r, l, g in p.imap_unordered(ler_perfil_uf, [(zperfil, n) for n in ufs]):
            print('   perfil', nome, l, flush=True)
            Z.update(z); ZF.update(zf); N.update(n); ruins += r; nl += l; ger.update(g)
        bras = rb.get()
    return {'Z': Z, 'ZF': ZF, 'N': N, 'ruins': ruins, 'linhas': nl, 'geracao': dict(ger), 'arquivos': ufs,
            'brasil': bras}


def passo_bweb(pasta):
    zips = sorted(glob.glob(os.path.join(pasta, '*.zip')), key=lambda p: -os.path.getsize(p))
    S = {}; disc = 0; turnos = collections.Counter(); arqs = []
    with Pool(4) as p:
        for zp, s, d, t in p.imap_unordered(ler_bweb_zip, zips):
            print('   bweb', os.path.basename(zp), len(s), flush=True)
            S.update(s); disc += d; turnos.update(t); arqs.append(os.path.basename(zp))
    return {'S': S, 'disc': disc, 'turnos': dict(turnos), 'arquivos': sorted(arqs)}


def passo_perfil_secao(pasta):
    zips = sorted(glob.glob(os.path.join(pasta, 'perfil_eleitor_secao_2026_*.zip')), key=lambda p: -os.path.getsize(p))
    S = {}; nl = 0
    with Pool(4) as p:
        for zp, s, l in p.imap_unordered(ler_perfil_secao, zips):
            print('   perfil_secao', os.path.basename(zp), len(s), l, flush=True)
            S.update(s); nl += l
    return {'S': S, 'linhas': nl, 'arquivos': [os.path.basename(z) for z in zips]}


def zona_de(k):
    p = k.split('|')
    return f'{p[0]}|{p[2]}' if len(p) == 3 else f'{p[0]}|{p[2]}'


def conferencia(t, perfil, bweb_S, tte, munz):
    """(a) para o turno t. Devolve dicionário com os números e a lista de zonas."""
    pz = collections.defaultdict(lambda: [0, 0, 0]); pz2 = collections.defaultdict(lambda: [0, 0, 0])
    for (tt, k), v in perfil['Z'].items():
        if tt != t: continue
        uf, mun, zona = k.split('|')
        a = pz[f'{uf}|{zona}']; a[0] += v[0]; a[1] += v[1]; a[2] += v[3]
        b = pz2[k]; b[0] += v[0]; b[1] += v[1]; b[2] += v[3]
    bz = collections.defaultdict(lambda: [0, 0, 0]); bz2 = collections.defaultdict(lambda: [0, 0, 0])
    for k, (a, c) in bweb_S.items():
        uf, mun, zona, _ = k.split('|')
        x = bz[f'{uf}|{zona}']; x[0] += a; x[1] += c; x[2] += 1
        y = bz2[f'{uf}|{mun}|{zona}']; y[0] += a; y[1] += c; y[2] += 1
    ni = collections.defaultdict(int); ni2 = collections.defaultdict(int)
    for (tt, k), v in munz.items():
        if tt != t: continue
        uf, mun, zona = k.split('|')
        ni[f'{uf}|{zona}'] += v[2]; ni2[k] += v[2]

    def compara(P, B, O, D, NI):
        linhas_z = []; cont = collections.Counter()
        for z in sorted(set(P) | set(B)):
            p = P.get(z, [0, 0, 0]); b = B.get(z, [0, 0, 0])
            d = p[1] - b[1]
            aj = p[1] - O.get((t, z), 0) + D.get((t, z), 0)
            daj = aj - b[1]
            r = d / b[1] if b[1] > 0 else (0.0 if d == 0 else 1.0)
            raj = daj / b[1] if b[1] > 0 else (0.0 if daj == 0 else 1.0)
            so = 'perfil' if z not in B else ('bweb' if z not in P else '')
            if so: r = raj = 1.0 if so == 'perfil' else -1.0
            cont['zonas'] += 1
            if d == 0: cont['iguais'] += 1
            if abs(r) > 0.005:
                cont['acima_bruto'] += 1
                if abs(raj) <= 0.005:
                    cont['explicada_E1'] += 1; exp = 'E1'
                elif NI.get(z, 0) > 0 and min(abs(d), abs(daj)) <= NI.get(z, 0):
                    cont['explicada_E2'] += 1; exp = 'E2'
                else:
                    cont['sem_explicacao'] += 1; exp = ''
                linhas_z.append({'zona': z, 'perfil': p[1], 'bweb': b[1], 'd': d, 'r_pct': 100 * r,
                                 'perfil_aj': aj, 'd_aj': daj, 'r_aj_pct': 100 * raj,
                                 'tte_origem': O.get((t, z), 0), 'tte_destino': D.get((t, z), 0),
                                 'perfil_tte_col': p[2], 'nao_instaladas': NI.get(z, 0), 'explicacao': exp,
                                 'so_em': so, 'aptos_perfil': p[0], 'aptos_bweb': b[0], 'secoes_bweb': b[2]})
            if abs(raj) > 0.005: cont['acima_ajustado'] += 1
            if daj == 0: cont['iguais_ajustado'] += 1
        # onde o perfil põe o eleitor com TTE: coluna QT_COMPARECIMENTO_TTE do perfil contra a soma por origem e por destino
        io_ = sum(1 for z in P if P[z][2] == O.get((t, z), 0)); id_ = sum(1 for z in P if P[z][2] == D.get((t, z), 0))
        cont['tte_col_igual_origem'] = io_; cont['tte_col_igual_destino'] = id_
        tot = {'perfil_comp': sum(v[1] for v in P.values()), 'bweb_comp': sum(v[1] for v in B.values()),
               'perfil_apt': sum(v[0] for v in P.values()), 'bweb_apt': sum(v[0] for v in B.values())}
        dist = sorted(abs((P.get(z, [0, 0])[1] - B[z][1]) / B[z][1]) for z in B if B[z][1] > 0)
        q = {f'p{int(x*100)}': 100 * dist[min(len(dist) - 1, int(x * len(dist)))] for x in (0.5, 0.9, 0.99)}
        q['max'] = 100 * dist[-1] if dist else None
        linhas_z.sort(key=lambda x: -abs(x['r_aj_pct']))
        return {'contagens': dict(cont), 'totais': tot, 'quantis_abs_r_bruto_pct': q, 'zonas_acima': linhas_z}

    res = {'zona': compara(pz, bz, tte['O'], tte['D'], ni),
           'zona_municipio': compara(pz2, bz2, tte['O2'], tte['D2'], ni2)}
    res['veredito'] = 'SINAL' if res['zona']['contagens'].get('sem_explicacao', 0) > 0 else 'SEM SINAL'
    res['veredito_zona_municipio'] = 'SINAL' if res['zona_municipio']['contagens'].get('sem_explicacao', 0) > 0 else 'SEM SINAL'
    return res


def conferencia_munzona(t, munz, bweb_S):
    M = collections.defaultdict(lambda: [0, 0]); M2 = {}
    for (tt, k), v in munz.items():
        if tt != t: continue
        uf, mun, zona = k.split('|')
        a = M[f'{uf}|{zona}']; a[0] += v[0]; a[1] += v[1]; M2[k] = v[:2]
    B = collections.defaultdict(lambda: [0, 0]); B2 = collections.defaultdict(lambda: [0, 0])
    for k, (a, c) in bweb_S.items():
        uf, mun, zona, _ = k.split('|')
        x = B[f'{uf}|{zona}']; x[0] += a; x[1] += c
        y = B2[f'{uf}|{mun}|{zona}']; y[0] += a; y[1] += c
    out = {}
    for nome, P, Q in (('zona', M, B), ('zona_municipio', M2, B2)):
        cont = collections.Counter(); lst = []
        for z in sorted(set(P) | set(Q)):
            p = P.get(z, [0, 0]); b = Q.get(z, [0, 0])
            d = p[1] - b[1]; da = p[0] - b[0]
            cont['zonas'] += 1
            if d == 0: cont['comp_iguais'] += 1
            if da == 0: cont['apt_iguais'] += 1
            r = d / b[1] if b[1] else (0.0 if d == 0 else 1.0)
            if abs(r) > 0.005:
                cont['acima_0_5'] += 1
            if d != 0 or da != 0:
                lst.append({'zona': z, 'munzona_comp': p[1], 'bweb_comp': b[1], 'd_comp': d, 'munzona_apt': p[0],
                            'bweb_apt': b[0], 'd_apt': da})
        out[nome] = {'contagens': dict(cont), 'diferentes': lst[:200], 'n_diferentes': len(lst),
                     'totais': {'munzona_comp': sum(v[1] for v in P.values()), 'bweb_comp': sum(v[1] for v in Q.values()),
                                'munzona_apt': sum(v[0] for v in P.values()), 'bweb_apt': sum(v[0] for v in Q.values())}}
    return out


def descritivo(perfil, turnos):
    out = {}
    for escopo in ('pais', 'exterior'):
        E = {}
        for t in turnos:
            G = collections.defaultdict(lambda: [0, 0])
            for (tt, uf, dim, cod), v in perfil['N'].items():
                if tt != t: continue
                if (uf == 'ZZ') != (escopo == 'exterior'): continue
                g = G[(dim, cod)]; g[0] += v[0]; g[1] += v[1]
                if dim == 'fx':
                    for nome, cods in FAIXAS_AGR:
                        if cod in cods:
                            h = G[('fxa', nome)]; h[0] += v[0]; h[1] += v[1]
                    if cod in FX_J:
                        h = G[('fxa', '16-34')]; h[0] += v[0]; h[1] += v[1]
                    h = G[('total', 0)]; h[0] += v[0]; h[1] += v[1]
            E[t] = G
        tab = []
        chaves = sorted(set().union(*[set(E[t]) for t in turnos]), key=lambda x: (x[0], str(x[1])))
        for ch in chaves:
            lin = {'dim': ch[0], 'cod': ch[1]}
            for t in turnos:
                a, c = E[t].get(ch, [0, 0])
                lin[f'apt{t}'] = a; lin[f'comp{t}'] = c; lin[f'taxa{t}'] = 100 * c / a if a else None
            if len(turnos) == 2 and lin['apt1'] and lin['apt2']:
                lin['var_pontos'] = lin['taxa2'] - lin['taxa1']
                dt = E[2][('total', 0)][1] - E[1][('total', 0)][1]
                lin['parcela_aumento'] = (lin['comp2'] - lin['comp1']) / dt if dt else None
            tab.append(lin)
        out[escopo] = tab
    return out


def goodman(A, y, w):
    W = w[:, None]
    M = A.T @ (A * W)
    c = np.linalg.cond(M)
    if not np.isfinite(c) or c > 1e8:
        return None, c
    return np.linalg.solve(M, A.T @ (w * y)), c


def ecologico(base, psec, perfil):
    """Estimativa ecológica X1 a X9."""
    cont = collections.Counter()
    linhas_s = []
    PS = psec['S']
    for k, v in base.items():
        uf = k.split('|')[0]
        if uf == 'ZZ': continue
        if '1' not in v or '2' not in v: cont['sem_dois_turnos'] += 1; continue
        s1, s2 = v['1'], v['2']
        if s1['apt'] <= 0 or s2['apt'] <= 0: cont['aptos_zero'] += 1; continue
        if s1.get('agr', '') != s2.get('agr', ''): cont['agregacao_mudou'] += 1; continue
        uf_, mun, zona, sec = k.split('|')
        secs = [sec] + [x.strip() for x in s2.get('agr', '').split('/') if x.strip()]
        comp = np.zeros(5); falta = False
        for s in secs:
            pk = f'{uf_}|{mun}|{zona}|{int(s)}'
            if pk not in PS: falta = True; break
            comp += np.array(PS[pk])
        if falta: cont['sem_perfil'] += 1; continue
        tot = comp[:4].sum()
        if tot <= 0: cont['perfil_vazio'] += 1; continue
        cont['usadas'] += 1
        if s2.get('agr'): cont['usadas_com_agregadas'] += 1
        T1 = s1['comp'] / s1['apt']; T2 = s2['comp'] / s2['apt']
        linhas_s.append((k, f'{uf_}|{zona}', lib.chave_local(k, s2), comp[:4] / tot, comp[:4], T1, T2, s2['apt'],
                         s1['L'], s1['R'], s2['L'], s2['R'], s1['apt'], s1['comp'], s2['comp']))
    # perfil verdadeiro do 1º turno por zona e grupo
    V1 = collections.defaultdict(lambda: np.zeros((4, 2)))
    for (t, z, fx), (a, c) in perfil['ZF'].items():
        if t != 1: continue
        g = grupo_x(fx)
        if g < 4:
            V1[z][g] += (a, c)
    porzona = collections.defaultdict(list)
    for i, l in enumerate(linhas_s):
        porzona[l[1]].append(i)
    Z = {}
    for z, ids in porzona.items():
        if len(ids) < 30: cont['zonas_menos_30'] += 1; continue
        A = np.array([linhas_s[i][3] for i in ids]); w = np.array([linhas_s[i][7] for i in ids], float)
        y1 = np.array([linhas_s[i][5] for i in ids]); dd = np.array([linhas_s[i][6] - linhas_s[i][5] for i in ids])
        b1, c1 = goodman(A, y1, w); bd, cd = goodman(A, dd, w)
        if b1 is None or bd is None: cont['zonas_mal_condicionadas'] += 1; continue
        E = np.array([linhas_s[i][4] for i in ids]).sum(0)
        Z[z] = {'t1': b1.tolist(), 'delta': bd.tolist(), 'cond': float(c1), 'n': len(ids), 'eleitores': E.tolist(),
                'verdadeiro_t1': [(V1[z][g][1] / V1[z][g][0]) if V1[z][g][0] > 0 else None for g in range(4)],
                'A1': V1[z][:, 0].tolist()}
    cont['zonas_estimadas'] = len(Z)
    # X5 calibração
    cal = {}
    for g, nome in enumerate(GRUPOS_X):
        zs = [z for z in Z if Z[z]['verdadeiro_t1'][g] is not None and Z[z]['A1'][g] > 0]
        est = np.array([100 * Z[z]['t1'][g] for z in zs]); ver = np.array([100 * Z[z]['verdadeiro_t1'][g] for z in zs])
        w = np.array([Z[z]['A1'][g] for z in zs])
        sl, ic = wslope(ver, est, w)
        cal[nome] = {'zonas': len(zs), 'corr_ponderada': wcorr(est, ver, w),
                     'erro_medio_abs_pontos': float(np.average(np.abs(est - ver), weights=w)),
                     'vies_medio_pontos': float(np.average(est - ver, weights=w)),
                     'inclinacao_verdadeiro_sobre_estimado': sl, 'intercepto': ic,
                     'nacional_estimado': float(np.average(est, weights=w)), 'nacional_verdadeiro': float(np.average(ver, weights=w)),
                     'p10_estimado': float(np.percentile(est, 10)), 'p90_estimado': float(np.percentile(est, 90)),
                     'p10_verdadeiro': float(np.percentile(ver, 10)), 'p90_verdadeiro': float(np.percentile(ver, 90))}
    cal['utilizavel'] = bool(cal['J']['corr_ponderada'] >= 0.5 and cal['J']['erro_medio_abs_pontos'] <= 5)
    # X7 variação nacional estimada por grupo
    nac = {}
    for g, nome in enumerate(GRUPOS_X):
        zs = list(Z); w = np.array([Z[z]['eleitores'][g] for z in zs]); d = np.array([100 * Z[z]['delta'][g] for z in zs])
        nac[nome] = {'variacao_estimada_pontos': float(np.average(d, weights=w)), 'p10': float(np.percentile(d, 10)),
                     'p50': float(np.percentile(d, 50)), 'p90': float(np.percentile(d, 90))}
    # variação observada total nas mesmas seções
    a1 = sum(l[12] for l in linhas_s); c1 = sum(l[13] for l in linhas_s)
    a2 = sum(l[7] for l in linhas_s); c2 = sum(l[14] for l in linhas_s)
    nac['observado_total_mesmas_secoes'] = {'taxa1': 100 * c1 / a1, 'taxa2': 100 * c2 / a2, 'variacao_pontos': 100 * (c2 / a2 - c1 / a1)}
    # zona: virada e regressões (X6, X9)
    ZV = collections.defaultdict(lambda: np.zeros(8))
    for l in linhas_s:
        ZV[l[1]] += (l[8], l[9], l[10], l[11], l[12], l[13], l[7], l[14])
    reg = {}
    zs = [z for z in Z if ZV[z][0] + ZV[z][1] > 0 and ZV[z][2] + ZV[z][3] > 0]
    y = np.array([100 * ZV[z][2] / (ZV[z][2] + ZV[z][3]) - 100 * ZV[z][0] / (ZV[z][0] + ZV[z][1]) for z in zs])
    w = np.array([ZV[z][2] + ZV[z][3] for z in zs])
    uf = np.array([z.split('|')[0] for z in zs])
    for nome, x in (('X6_variacao_estimada_J', np.array([100 * Z[z]['delta'][0] for z in zs])),
                    ('X9_variacao_total_bweb', np.array([100 * (ZV[z][7] / ZV[z][6] - ZV[z][5] / ZV[z][4]) for z in zs]))):
        r = lib.fe_ols(y, x[:, None], uf, w, nomes=['x'])
        bh, sh = fe_hc1(y, x[:, None], uf, w)
        reg[nome] = {'n_zonas': r['n'], 'ufs': r['grupos'], 'coef': r['coef']['x'], 'ep_uf': r['ep']['x'],
                     't_uf': r['coef']['x'] / r['ep']['x'], 'ep_hc1': float(sh[0]), 't_hc1': float(bh[0] / sh[0]),
                     'leitura_regua_B5_uf': veredito_b(r['coef']['x'], r['ep']['x']),
                     'leitura_regua_B5_hc1': veredito_b(float(bh[0]), float(sh[0])),
                     'x_media_pond': float(np.average(x, weights=w)), 'x_dp_pond': float(np.sqrt(np.average((x - np.average(x, weights=w)) ** 2, weights=w))),
                     'y_media_pond': float(np.average(y, weights=w))}
    # X8 dentro do local
    loc = np.array([l[2] for l in linhas_s]); A = np.array([l[3] for l in linhas_s])
    X = A[:, [0, 2, 3]]; wl = np.array([l[7] for l in linhas_s], float)
    T1 = np.array([l[5] for l in linhas_s]); D = np.array([l[6] - l[5] for l in linhas_s])
    x8 = {}
    for nome, yy in (('T1', 100 * T1), ('D', 100 * D)):
        r = lib.fe_ols(yy, X, loc, wl, nomes=['J', 'V', 'W'])
        x8[nome] = {'n': r['n'], 'locais': r['grupos'], 'coef': r['coef'], 'ep': r['ep']}
    # verdade nacional do 1º turno, diferenças contra M
    tv = np.zeros((4, 2))
    for z in V1:
        if z.split('|')[0] != 'ZZ':
            tv += V1[z]
    tt = 100 * tv[:, 1] / tv[:, 0]
    x8['verdade_1t_diferenca_contra_M'] = {'J': tt[0] - tt[1], 'V': tt[2] - tt[1], 'W': tt[3] - tt[1]}
    x8['verdade_1t_taxas'] = dict(zip(GRUPOS_X, tt.tolist()))
    zonas_ex = {z: {k: Z[z][k] for k in ('t1', 'delta', 'verdadeiro_t1', 'n')} for z in Z}
    return {'contagens': dict(cont), 'calibracao': cal, 'nacional': nac, 'regressoes_zona': reg, 'dentro_do_local': x8,
            'zonas': zonas_ex}


def nomes_munzona(zpath):
    N = {}
    with zipfile.ZipFile(zpath) as z:
        with z.open('detalhe_votacao_munzona_2026_BR.csv') as fh:
            it = linhas(fh, None)
            cab = next(it); ix = {c: i for i, c in enumerate(cab)}
            for r in it:
                N[f"{r[ix['SG_UF']]}|{int(r[ix['CD_MUNICIPIO']])}"] = r[ix['NM_MUNICIPIO']]
    return N


def pos_execucao(perfil, tte, bweb1, munz, psec, base, zmunz, X):
    """P1 a P3 (pós-hoc, depois de ver o resultado)."""
    nomes = nomes_munzona(zmunz)
    pz = collections.Counter(); pm = collections.Counter(); pam = collections.Counter()
    for (t, k), v in perfil['Z'].items():
        if t != 1: continue
        uf, m, z = k.split('|'); pz[f'{uf}|{z}'] += v[1]; pm[k] += v[1]; pam[k] += v[0]
    bz = collections.Counter(); bm = collections.Counter(); bam = collections.Counter(); ns = collections.Counter()
    for k, (a, c) in bweb1.items():
        uf, m, z, s = k.split('|'); bz[f'{uf}|{z}'] += c; bm[f'{uf}|{m}|{z}'] += c; bam[f'{uf}|{m}|{z}'] += a
        ns[f'{uf}|{m}|{z}'] += 1
    res = []
    for z in sorted(set(pz) | set(bz)):
        d = pz[z] - tte['O'].get((1, z), 0) + tte['D'].get((1, z), 0) - bz[z]
        if d:
            item = {'zona': z, 'residuo': d, 'bweb': bz[z], 'pct': 100 * d / bz[z] if bz[z] else None, 'municipios': []}
            if d >= 10:
                uf, zn = z.split('|')
                for k in sorted(set(pm) | set(bm)):
                    u, m, zz = k.split('|')
                    if u == uf and zz == zn:
                        dm = pm[k] - tte['O2'].get((1, k), 0) + tte['D2'].get((1, k), 0) - bm[k]
                        if dm:
                            item['municipios'].append({'municipio': k, 'nome': nomes.get(f'{u}|{m}', ''), 'residuo': dm,
                                                       'perfil_comp': pm[k], 'bweb_comp': bm[k], 'perfil_apt': pam[k],
                                                       'bweb_apt': bam[k], 'secoes': ns[k],
                                                       'tte_origem': tte['O2'].get((1, k), 0), 'tte_destino': tte['D2'].get((1, k), 0),
                                                       'pct_municipio': 100 * dm / bm[k] if bm[k] else None})
            res.append(item)
    res.sort(key=lambda x: x['residuo'])
    p1 = {'zonas_com_residuo': len(res), 'soma': sum(r['residuo'] for r in res),
          'positivos': sum(1 for r in res if r['residuo'] > 0), 'soma_positivos': sum(r['residuo'] for r in res if r['residuo'] > 0),
          'negativos': sum(1 for r in res if r['residuo'] < 0), 'soma_negativos': sum(r['residuo'] for r in res if r['residuo'] < 0),
          'zonas': res}
    ext = []
    for k in sorted(set(pm) | set(bm)):
        if not k.startswith('ZZ|'): continue
        if pm[k] > bm[k] and (pm[k] == pam[k] or bm[k] == 0):
            u, m, zz = k.split('|')
            ext.append({'cidade': k, 'nome': nomes.get(f'{u}|{m}', ''), 'perfil_apt': pam[k], 'perfil_comp': pm[k],
                        'bweb_apt': bam[k], 'bweb_comp': bm[k], 'secoes_bweb': ns[k],
                        'eleitores_nao_instaladas': munz.get((1, k), [0, 0, 0, 0])[2]})
    p2 = {'cidades': len(ext), 'excesso_perfil': sum(e['perfil_comp'] - e['bweb_comp'] for e in ext),
          'com_secao_no_bweb_e_perfil_100pct': sum(1 for e in ext if e['secoes_bweb'] > 0 and e['perfil_comp'] == e['perfil_apt']),
          'sem_boletim': sum(1 for e in ext if e['secoes_bweb'] == 0), 'lista': ext}
    # P3
    PS = psec['S']
    ys, Xs, ws, locs, ds = [], [], [], [], []
    ZV = collections.defaultdict(lambda: np.zeros(4))
    for k, v in base.items():
        if k.startswith('ZZ') or '1' not in v or '2' not in v: continue
        s1, s2 = v['1'], v['2']
        if s1.get('agr', '') != s2.get('agr', '') or s1['apt'] <= 0 or s2['apt'] <= 0: continue
        if s1['L'] + s1['R'] <= 0 or s2['L'] + s2['R'] <= 0: continue
        uf, mun, zona, sec = k.split('|')
        secs = [sec] + [x.strip() for x in s2.get('agr', '').split('/') if x.strip()]
        if any(f'{uf}|{mun}|{zona}|{int(s)}' not in PS for s in secs): continue
        c = np.sum([PS[f'{uf}|{mun}|{zona}|{int(s)}'] for s in secs], axis=0)[:4]
        if c.sum() <= 0: continue
        a = c / c.sum()
        ys.append(100 * s2['L'] / (s2['L'] + s2['R']) - 100 * s1['L'] / (s1['L'] + s1['R']))
        Xs.append(a[[0, 2, 3]]); ws.append(s2['L'] + s2['R']); locs.append(lib.chave_local(k, s2))
        ds.append(100 * (s2['comp'] / s2['apt'] - s1['comp'] / s1['apt']))
        ZV[f'{uf}|{zona}'] += (s1['L'], s1['R'], s2['L'], s2['R'])
    y = np.array(ys); Xa = np.array(Xs); w = np.array(ws, float); dd = np.array(ds); loc = np.array(locs)
    p3 = {'secao_fracoes': lib.fe_ols(y, Xa, loc, w, nomes=['J', 'V', 'W']),
          'secao_fracoes_e_variacao_comp': lib.fe_ols(y, np.column_stack([Xa, dd]), loc, w, nomes=['J', 'V', 'W', 'dcomp']),
          'zona_variacao_estimada': {}}
    Z = X['zonas']
    zs = [z for z in Z if z in ZV and ZV[z][0] + ZV[z][1] > 0 and ZV[z][2] + ZV[z][3] > 0]
    yz = np.array([100 * ZV[z][2] / (ZV[z][2] + ZV[z][3]) - 100 * ZV[z][0] / (ZV[z][0] + ZV[z][1]) for z in zs])
    wz = np.array([ZV[z][2] + ZV[z][3] for z in zs]); ufz = np.array([z.split('|')[0] for z in zs])
    for g, nome in enumerate(GRUPOS_X):
        x = np.array([100 * Z[z]['delta'][g] for z in zs])
        rr = lib.fe_ols(yz, x[:, None], ufz, wz, nomes=['x'])
        p3['zona_variacao_estimada'][nome] = {'n': rr['n'], 'coef': rr['coef']['x'], 'ep_uf': rr['ep']['x'],
                                              't': rr['coef']['x'] / rr['ep']['x']}
    return {'P1_residuos': p1, 'P2_exterior': p2, 'P3_virada_e_idade': p3}


def regressao_b(perfil, base):
    """(b) pela letra, só com os dois turnos no perfil."""
    C = collections.defaultdict(lambda: np.zeros((2, 2)))
    for (t, z, fx), (a, c) in perfil['ZF'].items():
        if fx in FX_J and t in (1, 2):
            C[z][t - 1] += (a, c)
    ZV = collections.defaultdict(lambda: np.zeros(4))
    for k, v in base.items():
        if '1' in v and '2' in v and not k.startswith('ZZ'):
            uf, mun, zona, _ = k.split('|')
            ZV[f'{uf}|{zona}'] += (v['1']['L'], v['1']['R'], v['2']['L'], v['2']['R'])
    zs = [z for z in C if not z.startswith('ZZ') and C[z][0][0] > 0 and C[z][1][0] > 0 and z in ZV
          and ZV[z][0] + ZV[z][1] > 0 and ZV[z][2] + ZV[z][3] > 0]
    x = np.array([100 * (C[z][1][1] / C[z][1][0] - C[z][0][1] / C[z][0][0]) for z in zs])
    y = np.array([100 * ZV[z][2] / (ZV[z][2] + ZV[z][3]) - 100 * ZV[z][0] / (ZV[z][0] + ZV[z][1]) for z in zs])
    w = np.array([ZV[z][2] + ZV[z][3] for z in zs]); uf = np.array([z.split('|')[0] for z in zs])
    r = lib.fe_ols(y, x[:, None], uf, w, nomes=['x'])
    bh, sh = fe_hc1(y, x[:, None], uf, w)
    v = veredito_b(r['coef']['x'], r['ep']['x']); vh = veredito_b(float(bh[0]), float(sh[0]))
    return {'n_zonas': r['n'], 'coef': r['coef']['x'], 'ep_uf': r['ep']['x'], 't_uf': r['coef']['x'] / r['ep']['x'],
            'ep_hc1': float(sh[0]), 'veredito': v, 'veredito_hc1': vh}


# ---------------------------------------------------------------- relatório
def escrever_txt(R, caminho):
    L = []; w = L.append
    w('F15. Quem foi votar a mais: perfil do comparecimento (Adendo 21, commit 913af7a, 31/10/2026 10:36:29 UTC)')
    w('Script: scripts/analisar_F15.py. Números completos: resultados/F15_perfil_comparecimento.json.')
    w(f"Rodado em {R['rodado_em']} UTC. Decisões escritas no docstring do script antes de calcular (sha256 do script no momento"
      f" das decisões: {R['sha256_script_decisoes'][:16]}...).")
    w('')
    w('Critério registrado (PRE-REGISTRO-2026-10-26.md, Adendo 21, antes de rodar):')
    w('- Dado aberto do TSE de comparecimento e abstenção por zona, faixa etária, gênero e escolaridade, nos dois turnos de 2026.')
    w('- (a) Conferência: comparecimento por zona no perfil contra a soma do bweb. Sinal: alguma zona com diferença acima de 0,5%')
    w('  sem explicação.')
    w('- (b) Entre as zonas da mesma UF, relação entre a variação do comparecimento de 16 a 34 anos (em pontos) e a virada de Lula')
    w('  na zona, ponderada pelos votos dos finalistas. Incoerência: inclinação negativa a mais de 3 erros-padrão. Coerente:')
    w('  positiva a mais de 3 erros-padrão. Entre os dois: inconclusivo.')
    w('- (c) Descritivo: variação do comparecimento por faixa etária, gênero e escolaridade no país.')
    w('')
    D = R['disponibilidade']
    w('VEREDITO PELA LETRA')
    for linha in R['veredito_linhas']:
        w('- ' + linha)
    w('')
    w('1. O que o TSE publicou (verificado em 31/10/2026)')
    for linha in D['texto']:
        w('- ' + linha)
    w('')
    A = R['a']
    w('2. (a) Conferência do perfil contra o bweb')
    for t, res in A['por_turno'].items():
        if res is None:
            w(f'- {t}º turno: sem dado (o perfil não traz este turno).'); continue
        c = res['zona']['contagens']; tot = res['zona']['totais']; q = res['zona']['quantis_abs_r_bruto_pct']
        w(f"- {t}º turno, zona (UF|zona): {c['zonas']} zonas. Comparecimento total: perfil {milhar(tot['perfil_comp'])},"
          f" bweb {milhar(tot['bweb_comp'])} (diferença {milhar(tot['perfil_comp'] - tot['bweb_comp'])}). Aptos: perfil"
          f" {milhar(tot['perfil_apt'])}, bweb {milhar(tot['bweb_apt'])}.")
        w(f"  Zonas com comparecimento idêntico: {c.get('iguais', 0)}. Diferença relativa absoluta: mediana {pct(q['p50'], 3)}%,"
          f" p90 {pct(q['p90'], 3)}%, p99 {pct(q['p99'], 3)}%, máxima {pct(q['max'], 3)}%.")
        w(f"  Acima de 0,5% sem ajuste: {c.get('acima_bruto', 0)}; explicadas pela transferência temporária (E1):"
          f" {c.get('explicada_E1', 0)}; por seção não instalada (E2): {c.get('explicada_E2', 0)}; sem explicação:"
          f" {c.get('sem_explicacao', 0)}. Com o ajuste E1 aplicado a todas: {c.get('iguais_ajustado', 0)} zonas idênticas,"
          f" {c.get('acima_ajustado', 0)} acima de 0,5%.")
        w(f"  Coluna QT_COMPARECIMENTO_TTE do perfil igual à soma do arquivo TTE por origem em {c.get('tte_col_igual_origem', 0)}"
          f" zonas e por destino em {c.get('tte_col_igual_destino', 0)}.")
        c2 = res['zona_municipio']['contagens']
        w(f"  Leitura fina (UF|município|zona): {c2['zonas']} unidades, {c2.get('acima_bruto', 0)} acima de 0,5% sem ajuste,"
          f" {c2.get('explicada_E1', 0)} explicadas por E1, {c2.get('explicada_E2', 0)} por E2, {c2.get('sem_explicacao', 0)}"
          f" sem explicação.")
        lst = [z for z in res['zona']['zonas_acima'] if not z['explicacao']][:15]
        if lst:
            w('  Zonas sem explicação (maiores primeiro):')
            for z in lst:
                w(f"    {z['zona']}: perfil {z['perfil']}, bweb {z['bweb']}, d {z['d']} ({pct(z['r_pct'], 2)}%), ajustado"
                  f" {z['perfil_aj']} ({pct(z['r_aj_pct'], 2)}%), TTE origem {z['tte_origem']}, destino {z['tte_destino']},"
                  f" só em: {z['so_em'] or 'os dois'}")
        lst = [z for z in res['zona']['zonas_acima'] if z['explicacao']][:10]
        if lst:
            w('  Exemplos de zonas acima de 0,5% explicadas:')
            for z in lst:
                w(f"    {z['zona']}: perfil {z['perfil']}, bweb {z['bweb']} ({pct(z['r_pct'], 2)}%), TTE origem {z['tte_origem']},"
                  f" destino {z['tte_destino']}, ajustado {z['perfil_aj']} ({pct(z['r_aj_pct'], 2)}%), {z['explicacao']}")
    bw = R['a']['bweb_conferencia']
    for t, x in bw.items():
        w(f"- bweb do {t}º turno lido dos zips: {milhar(x['secoes'])} seções, {x['discordancias']} linhas discordantes na mesma"
          f" seção; contra a base: {x['secoes_so_zip']} seções só no zip, {x['secoes_so_base']} só na base,"
          f" {x['secoes_comp_diferente']} com comparecimento diferente.")
    p = R['a']['perfil_conferencia']
    w(f"- Perfil: {milhar(p['linhas'])} linhas nos CSVs por UF, {p['linhas_apt_diferente_comp_mais_abst']} com aptos diferente"
      f" de comparecimento + abstenção; _BRASIL.csv contra a soma das UFs: {p['brasil_contra_ufs']}.")
    w('')
    w('3. Fora do critério: detalhe da apuração por zona (TSE, 30/10/2026) contra a soma do bweb, cargo Presidente')
    for t, res in R['a_extra_munzona'].items():
        c = res['zona']['contagens']; tot = res['zona']['totais']
        w(f"- {t}º turno: {c['zonas']} zonas; comparecimento idêntico em {c.get('comp_iguais', 0)}, aptos idênticos em"
          f" {c.get('apt_iguais', 0)}, acima de 0,5% em {c.get('acima_0_5', 0)}. Totais: munzona {milhar(tot['munzona_comp'])},"
          f" bweb {milhar(tot['bweb_comp'])}; aptos munzona {milhar(tot['munzona_apt'])}, bweb {milhar(tot['bweb_apt'])}.")
        c2 = res['zona_municipio']['contagens']
        w(f"  Leitura fina (UF|município|zona): {c2['zonas']} unidades, comparecimento idêntico em {c2.get('comp_iguais', 0)},"
          f" aptos idênticos em {c2.get('apt_iguais', 0)}, acima de 0,5% em {c2.get('acima_0_5', 0)}.")
        for z in res['zona']['diferentes'][:8]:
            w(f"    {z['zona']}: comparecimento munzona {z['munzona_comp']} x bweb {z['bweb_comp']} (d {z['d_comp']}); aptos"
              f" {z['munzona_apt']} x {z['bweb_apt']} (d {z['d_apt']})")
    w('')
    w('4. (b) Variação do comparecimento de 16 a 34 anos contra a virada de Lula, entre zonas da mesma UF')
    b = R['b']
    if b.get('veredito') == 'SEM DADO':
        w('- SEM DADO: o perfil publicado não tem o 2º turno, então a variação de 16 a 34 anos por zona não existe no dado oficial.')
    else:
        w(f"- {b['n_zonas']} zonas; coef {pct(b['coef'], 4)} ponto de virada por ponto de comparecimento jovem, ep (UF)"
          f" {pct(b['ep_uf'], 4)}, t {pct(b['t_uf'], 2)}; ep HC1 {pct(b['ep_hc1'], 4)}. Veredito: {b['veredito']}"
          f" (HC1: {b['veredito_hc1']}).")
    w('')
    w('5. (c) Comparecimento por faixa etária, gênero e escolaridade no país (27 UFs)')
    C = R['c']
    turnos = R['disponibilidade']['turnos_perfil']
    if len(turnos) < 2:
        w('- A variação entre turnos não existe no dado oficial. Taxas do 1º turno (o que existe):')
    for lin in C['pais']:
        if lin['dim'] in ('fxa', 'g', 'i', 'total'):
            nome = {'fxa': 'faixa', 'g': 'gênero', 'i': 'instrução', 'total': 'total'}[lin['dim']]
            rot = C['rotulos'].get(f"{lin['dim']}|{lin['cod']}", str(lin['cod']))
            s = f"  {nome} {rot}: aptos {milhar(lin['apt1'])}, compareceram {milhar(lin['comp1'])}, taxa {pct(lin['taxa1'] or 0, 2)}%"
            if 'var_pontos' in lin:
                s += f"; 2º turno {pct(lin['taxa2'], 2)}%, variação {pct(lin['var_pontos'], 2)} ponto, parcela do aumento {pct(100 * lin['parcela_aumento'], 1)}%"
            w(s)
    w('')
    X = R['exploratorio']
    w('6. Fora do critério, sem veredito: estimativa ecológica (perfil do eleitorado por seção + bweb dos dois turnos)')
    c = X['contagens']
    w(f"- Seções usadas: {milhar(c.get('usadas', 0))} (sem perfil por seção: {c.get('sem_perfil', 0)}; agregação mudou entre os"
      f" turnos: {c.get('agregacao_mudou', 0)}; sem os dois turnos: {c.get('sem_dois_turnos', 0)}). Zonas estimadas:"
      f" {c.get('zonas_estimadas', 0)} (com menos de 30 seções: {c.get('zonas_menos_30', 0)}; mal condicionadas:"
      f" {c.get('zonas_mal_condicionadas', 0)}).")
    cal = X['calibracao']
    w('- Calibração no 1º turno (estimado por zona contra o perfil verdadeiro do 1º turno):')
    for g in GRUPOS_X:
        k = cal[g]
        w(f"    {ROT_X[g]}: {k['zonas']} zonas, correlação {pct(k['corr_ponderada'], 3)}, erro médio absoluto"
          f" {pct(k['erro_medio_abs_pontos'], 2)} pontos, viés {pct(k['vies_medio_pontos'], 2)}, inclinação do verdadeiro sobre o"
          f" estimado {pct(k['inclinacao_verdadeiro_sobre_estimado'], 3)}; nacional estimado {pct(k['nacional_estimado'], 2)}% x"
          f" verdadeiro {pct(k['nacional_verdadeiro'], 2)}%; p10 a p90 estimado {pct(k['p10_estimado'], 1)} a"
          f" {pct(k['p90_estimado'], 1)}, verdadeiro {pct(k['p10_verdadeiro'], 1)} a {pct(k['p90_verdadeiro'], 1)}.")
    w(f"    Pela régua escrita antes (J com correlação de 0,5 ou mais e erro médio absoluto de 5 pontos ou menos): "
      f"{'UTILIZÁVEL' if cal['utilizavel'] else 'IMPRESTÁVEL, a estimativa do 2º turno não é comentada'}.")
    nac = X['nacional']
    o = nac['observado_total_mesmas_secoes']
    w(f"- Nas seções usadas, o comparecimento foi de {pct(o['taxa1'], 2)}% para {pct(o['taxa2'], 2)}% ({pct(o['variacao_pontos'], 2)} ponto).")
    if cal['utilizavel']:
        w('- Variação estimada por grupo (média das zonas ponderada pelos eleitores do grupo):')
        for g in GRUPOS_X:
            k = nac[g]
            w(f"    {ROT_X[g]}: {pct(k['variacao_estimada_pontos'], 2)} ponto (p10 {pct(k['p10'], 1)}, mediana {pct(k['p50'], 1)},"
              f" p90 {pct(k['p90'], 1)} entre zonas)")
        r = X['regressoes_zona']['X6_variacao_estimada_J']
        w(f"- Indicação para (b): {r['n_zonas']} zonas, coef {pct(r['coef'], 4)}, ep (UF) {pct(r['ep_uf'], 4)}, t {pct(r['t_uf'], 2)};"
          f" ep HC1 {pct(r['ep_hc1'], 4)}, t {pct(r['t_hc1'], 2)}. A régua de B5 leria {r['leitura_regua_B5_uf']} (HC1:"
          f" {r['leitura_regua_B5_hc1']}). Exploratório: não é o teste registrado.")
    r = X['regressoes_zona']['X9_variacao_total_bweb']
    w(f"- Descritivo: virada de Lula contra a variação total do comparecimento da zona (bweb): {r['n_zonas']} zonas, coef"
      f" {pct(r['coef'], 4)}, ep (UF) {pct(r['ep_uf'], 4)}, t {pct(r['t_uf'], 2)}; ep HC1 {pct(r['ep_hc1'], 4)}, t {pct(r['t_hc1'], 2)}.")
    x8 = X['dentro_do_local']
    w('- Dentro do mesmo local de votação (efeito fixo de local, peso aptos do 2º turno, erro agrupado por local; referência 35 a 59):')
    for nome, rot in (('T1', 'comparecimento do 1º turno'), ('D', 'variação do comparecimento')):
        k = x8[nome]
        w(f"    {rot}: {milhar(k['n'])} seções, {milhar(k['locais'])} locais; J {pct(k['coef']['J'], 2)} (ep {pct(k['ep']['J'], 2)}),"
          f" V {pct(k['coef']['V'], 2)} (ep {pct(k['ep']['V'], 2)}), W {pct(k['coef']['W'], 2)} (ep {pct(k['ep']['W'], 2)})"
          f" pontos por fração inteira do grupo")
    v = x8['verdade_1t_diferenca_contra_M']
    w(f"    verdade do 1º turno no país (perfil): J menos M {pct(v['J'], 2)}, V menos M {pct(v['V'], 2)}, W menos M {pct(v['W'], 2)} pontos")
    w('')
    w('7. Desvios e decisões (todas escritas no docstring antes de calcular)')
    for d in R['desvios']:
        w('- ' + d)
    w('')
    w('8. O que fica sem teste')
    for d in R['sem_teste']:
        w('- ' + d)
    w('')
    P = R['pos_execucao']
    w('9. Depois de rodar (pós-hoc, fora do registro, não muda nenhum veredito)')
    p1 = P['P1_residuos']
    w(f"- P1. Zonas com resíduo depois do ajuste E1: {p1['zonas_com_residuo']} de {A['por_turno']['1']['zona']['contagens']['zonas']}"
      f" (soma {p1['soma']}). Negativos: {p1['negativos']} zonas, soma {p1['soma_negativos']} (de -1 a -8, compatível com o mesmo"
      f" eleitor em dois tipos de transferência, que o leiame admite). Positivos (perfil acima do bweb): {p1['positivos']} zonas,"
      f" soma {p1['soma_positivos']}, todos abaixo de 0,5% da zona:")
    for z in [z for z in p1['zonas'] if z['residuo'] > 0][::-1]:
        mm = sorted(z['municipios'], key=lambda m: -abs(m['residuo']))
        ms = '; '.join(f"{m['nome']} ({m['municipio']}) {m['residuo']:+d}, {pct(m['pct_municipio'] or 0, 2)}% do município,"
                       f" {m['secoes']} seções, TTE origem {m['tte_origem']} destino {m['tte_destino']}" for m in mm[:4])
        if len(mm) > 4:
            ms += f"; e mais {len(mm) - 4} unidades (lista no JSON)"
        w(f"    {z['zona']}: {z['residuo']:+d} ({pct(z['pct'] or 0, 3)}% da zona)" + (f": {ms}" if ms else ''))
    p2 = P['P2_exterior']
    w(f"- P2. Exterior: {p2['cidades']} cidades em que o perfil marca mais presentes que o bweb e (perfil com 100% dos aptos"
      f" presentes ou sem boletim): {p2['com_secao_no_bweb_e_perfil_100pct']} com seção no bweb e 100% no perfil,"
      f" {p2['sem_boletim']} sem boletim; excesso do perfil {p2['excesso_perfil']}. Exemplos:")
    for e in sorted(p2['lista'], key=lambda e: -(e['perfil_comp'] - e['bweb_comp']))[:12]:
        w(f"    {e['nome']} ({e['cidade']}): perfil {e['perfil_comp']} de {e['perfil_apt']} aptos; bweb {e['bweb_comp']} de"
          f" {e['bweb_apt']} ({e['secoes_bweb']} seção); eleitores em seção não instalada (munzona) {e['eleitores_nao_instaladas']}")
    p3 = P['P3_virada_e_idade']
    s = p3['secao_fracoes']; s2 = p3['secao_fracoes_e_variacao_comp']
    w(f"- P3. Virada de Lula na seção contra a composição etária, dentro do local ({milhar(s['n'])} seções, {milhar(s['grupos'])}"
      f" locais; pontos de virada por fração inteira do grupo, referência 35 a 59): J {pct(s['coef']['J'], 2)} (ep"
      f" {pct(s['ep']['J'], 2)}), V {pct(s['coef']['V'], 2)} (ep {pct(s['ep']['V'], 2)}), W {pct(s['coef']['W'], 2)} (ep"
      f" {pct(s['ep']['W'], 2)}). Com a variação do comparecimento da seção: J {pct(s2['coef']['J'], 2)}, V {pct(s2['coef']['V'], 2)},"
      f" W {pct(s2['coef']['W'], 2)}, variação do comparecimento {pct(s2['coef']['dcomp'], 4)} (ep {pct(s2['ep']['dcomp'], 4)}).")
    zz = p3['zona_variacao_estimada']
    w('    Virada da zona contra a variação estimada de cada grupo (efeito fixo de UF, erro agrupado por UF): ' +
      '; '.join(f"{ROT_X[g]} coef {pct(zz[g]['coef'], 4)}, t {pct(zz[g]['t'], 2)}" for g in GRUPOS_X) + '.')
    w('')
    w('10. O que os números significam')
    c1 = A['por_turno']['1']['zona']['contagens']
    w(f"- (a) no 1º turno: o perfil põe o eleitor com transferência temporária na zona de origem (a coluna de TTE do perfil bate"
      f" com a soma por origem em {c1['tte_col_igual_origem']} de {c1['zonas']} zonas), e o bweb o conta onde ele votou. Feita essa"
      f" troca, {c1['iguais_ajustado']} zonas batem voto a voto e nenhuma passa de 0,5%. Pela letra, sem sinal. O cadastro de"
      f" presença e os boletins do 1º turno contam a mesma coisa, com resíduo total de {p1['soma']} eleitores em 125 milhões.")
    mp = [m for z in p1['zonas'] if z['residuo'] > 0 and not z['zona'].startswith('ZZ') for m in z['municipios'] if m['residuo'] > 0]
    mx = max(mp, key=lambda m: m['pct_municipio'] or 0) if mp else None
    w(f"- O que sobra e não tem explicação documentada é pequeno e sempre no mesmo sentido (perfil acima do bweb): o exterior"
      f" ({p2['excesso_perfil']} a mais nas cidades listadas em P2, onde o perfil dá 100% de presença ou não há boletim, o que"
      f" parece regra de cadastro para quem não pôde votar, mas o leiame não diz) e {len(mp)} municípios do Brasil com"
      f" {min(m['residuo'] for m in mp):+d} a {max(m['residuo'] for m in mp):+d}" +
      (f", o maior em proporção {mx['nome']} ({mx['municipio']}), {mx['residuo']:+d}, {pct(mx['pct_municipio'], 2)}% do município"
       if mx else '') + '. Nada disso mexe em votos: é o cadastro de presença com mais gente do que os boletins.')
    cj = X['calibracao']['J']; r6 = X['regressoes_zona']['X6_variacao_estimada_J']; nw = X['nacional']
    w(f"- (b) e a variação de (c) não existem no dado oficial. A estimativa ecológica {'passou' if cal['utilizavel'] else 'não passou'}"
      f" na régua de utilidade (erro médio de {pct(cj['erro_medio_abs_pontos'], 1)} pontos contra o limite de 5, correlação"
      f" {pct(cj['corr_ponderada'], 2)}, viés de {pct(cj['vies_medio_pontos'], 1)} pontos, inclinação"
      f" {pct(cj['inclinacao_verdadeiro_sobre_estimado'], 2)}: as estimativas por zona são mais espalhadas que o real). Ela indica"
      f" variação de {pct(nw['J']['variacao_estimada_pontos'], 1)} ponto nos de 16 a 34, {pct(nw['M']['variacao_estimada_pontos'], 1)}"
      f" nos de 35 a 59, {pct(nw['V']['variacao_estimada_pontos'], 1)} nos de 60 a 69 e {pct(nw['W']['variacao_estimada_pontos'], 1)}"
      f" nos de 70 ou mais: o comparecimento a mais veio sobretudo dos mais velhos e pouco dos jovens. A relação com a virada é"
      f" positiva e fraca nos jovens (t {pct(r6['t_uf'], 2)} com erro por UF) e negativa nos de 70 ou mais (t"
      f" {pct(zz['W']['t'], 2)}, pós-hoc): onde os idosos foram mais votar, Lula virou menos. Isso não é a incoerência que o"
      f" registro procura; é o sentido esperado se os idosos a mais votaram mais em Flávio. Vale como pista, não como teste,"
      f" até o TSE publicar o perfil do 2º turno.")
    txt = '\n'.join(L) + '\n'
    assert chr(0x2014) not in txt and chr(0x2013) not in txt
    with open(caminho, 'w') as f:
        f.write(txt)


ROT_X = {'J': '16 a 34', 'M': '35 a 59', 'V': '60 a 69', 'W': '70 ou mais'}


def rodar(zperfil, ztte, zmunz, d1, d2, fbase, dpsec, trab, sjson, stxt, sha_dec):
    os.makedirs(trab, exist_ok=True)
    print('perfil', flush=True)
    perfil = cache(trab, 'perfil.pkl.gz', lambda: passo_perfil(zperfil))
    print('tte', flush=True)
    tte = cache(trab, 'tte.pkl.gz', lambda: ler_tte(ztte))
    print('munzona', flush=True)
    munz = cache(trab, 'munzona.pkl.gz', lambda: ler_munzona(zmunz))
    print('bweb', flush=True)
    bweb = {1: cache(trab, 'bweb1.pkl.gz', lambda: passo_bweb(d1)), 2: cache(trab, 'bweb2.pkl.gz', lambda: passo_bweb(d2))}
    print('base', flush=True)
    base = lib.carregar(fbase)
    turnos = sorted({t for (t, _) in perfil['Z']})
    # conferência do bweb lido contra a base
    bconf = {}
    for t in (1, 2):
        S = bweb[t]['S']; ts = str(t)
        bk = {k for k, v in base.items() if ts in v}
        bconf[t] = {'secoes': len(S), 'discordancias': bweb[t]['disc'], 'turnos_nas_linhas': bweb[t]['turnos'],
                    'secoes_so_zip': len(set(S) - bk), 'secoes_so_base': len(bk - set(S)),
                    'secoes_comp_diferente': sum(1 for k in set(S) & bk if S[k][1] != base[k][ts]['comp'] or S[k][0] != base[k][ts]['apt'])}
    # BRASIL contra UFs
    soma_uf = collections.defaultdict(lambda: [0, 0])
    for (t, k), v in perfil['Z'].items():
        u = soma_uf[(t, k.split('|')[0])]; u[0] += v[0]; u[1] += v[1]
    bra_ok = 'sem arquivo _BRASIL'
    if perfil['brasil']:
        _, S, nl = perfil['brasil'][0]
        dif = [k for k in set(S) | set(soma_uf) if tuple(S.get(k, [0, 0, 0])[:2]) != tuple(soma_uf.get(k, [0, 0]))]
        bra_ok = f'{len(S)} pares turno-UF, {len(dif)} diferentes, {milhar(nl)} linhas' + (f' ({sorted(dif)[:5]})' if dif else '')
    print('a', flush=True)
    a = {'por_turno': {}, 'bweb_conferencia': bconf,
         'perfil_conferencia': {'linhas': perfil['linhas'], 'linhas_apt_diferente_comp_mais_abst': perfil['ruins'],
                                'geracao': perfil['geracao'], 'brasil_contra_ufs': bra_ok}}
    for t in (1, 2):
        a['por_turno'][t] = conferencia(t, perfil, bweb[t]['S'], tte, munz) if t in turnos else None
    extra = {t: conferencia_munzona(t, munz, bweb[t]['S']) for t in (1, 2)}
    print('c', flush=True)
    c = descritivo(perfil, turnos)
    rot = {}
    with zipfile.ZipFile(zperfil) as z:
        with z.open('perfil_comparecimento_abstencao_2026_AC.csv') as fh:
            it = linhas(fh, None); cab = next(it); ix = {x: i for i, x in enumerate(cab)}
            for r in it:
                rot[f"fx|{int(r[ix['CD_FAIXA_ETARIA']])}"] = r[ix['DS_FAIXA_ETARIA']]
                rot[f"g|{int(r[ix['CD_GENERO']])}"] = r[ix['DS_GENERO']].lower()
                rot[f"i|{int(r[ix['CD_GRAU_INSTRUCAO']])}"] = r[ix['DS_GRAU_INSTRUCAO']].lower()
    for nome, _ in FAIXAS_AGR + [('16-34', None)]:
        rot[f'fxa|{nome}'] = nome
    rot['total|0'] = 'todos'
    rot.setdefault('g|0', 'não informado'); rot.setdefault('i|0', 'não informado')
    rot.setdefault('fx|-3', 'inválido')
    c['rotulos'] = rot
    print('b', flush=True)
    b = regressao_b(perfil, base) if 2 in turnos else {'veredito': 'SEM DADO'}
    print('ecologico', flush=True)
    psec = cache(trab, 'perfil_secao.pkl.gz', lambda: passo_perfil_secao(dpsec))
    X = ecologico(base, psec, perfil)
    X['linhas_perfil_secao'] = psec['linhas']; X['arquivos_perfil_secao'] = psec['arquivos']
    print('pos_execucao', flush=True)
    PX = pos_execucao(perfil, tte, bweb[1]['S'], munz, psec, base, zmunz, X)

    va1 = a['por_turno'][1]['veredito'] if a['por_turno'][1] else 'SEM DADO'
    va2 = a['por_turno'][2]['veredito'] if a['por_turno'][2] else 'SEM DADO'
    ver = [f'(a) 1º turno: {va1}. (a) 2º turno: {va2}' + (' (o perfil publicado não tem o 2º turno).' if va2 == 'SEM DADO' else '.'),
           f"(b): {b['veredito']}" + (' (sem o 2º turno no perfil não existe a variação de 16 a 34 anos por zona).' if b['veredito'] == 'SEM DADO' else '.'),
           '(c): ' + ('variação entre turnos SEM DADO; só as taxas do 1º turno são descritas.' if len(turnos) < 2 else 'descritivo abaixo.'),
           'F15 como um todo: INCOMPLETO. O registro pede os dois turnos e o TSE só publicou o 1º (arquivo de 21/10/2026, gerado em'
           ' 13/10/2026). O script roda as três partes sozinho quando o arquivo passar a ter NR_TURNO = 2.']
    disp = {'turnos_perfil': turnos, 'texto': [
        'Conjunto "Comparecimento e Abstenção - 2026" (dadosabertos.tse.jus.br, comparecimento-e-abstencao-2026), criado em'
        ' 21/10/2026 13:19 UTC e não alterado depois. Arquivo perfil_comparecimento_abstencao_2026.zip (cdn.tse.jus.br,'
        f" Last-Modified 21/10/2026 16:40:26 GMT, 229.213.668 bytes, sha256 {sha256(zperfil)}).",
        f"Turnos presentes no perfil: {turnos}; data de geração das linhas: {sorted(perfil['geracao'])}.",
        f"Arquivo de transferência temporária (sha256 {sha256(ztte)}): só o 1º turno, {milhar(tte['linhas'])} linhas.",
        'Painel de estatísticas do TSE (sig.tse.jus.br): 403 do servidor (Akamai, Access Denied); não foi contornado.',
        f"Detalhe da apuração por município e zona (Last-Modified 30/10/2026 22:46:49 GMT, sha256 {sha256(zmunz)}): tem os dois"
        ' turnos, sem perfil; usado na conferência fora do critério (seção 3).',
        f"Perfil do eleitorado por seção, julho de 2026 ({len(psec['arquivos'])} arquivos, {milhar(psec['linhas'])} linhas):"
        ' aptos por seção e faixa, sem comparecimento; usado na estimativa ecológica (seção 6).']}
    desvios = [
        'A1: zona = UF|NR_ZONA (municípios da zona somados); leitura secundária UF|município|zona.',
        'A3: bweb lido dos zips, cargo Presidente, uma linha por seção; conferido contra a base.',
        'A4: 0,5% medido sobre o comparecimento do bweb da zona, em valor absoluto.',
        'A5: explicações aceitas fixadas antes: E1 transferência temporária (ajuste origem e destino pelo arquivo TTE do TSE),'
        ' E2 seção não instalada; "sem sinal" de (a) = complemento do sinal.',
        'A6: conferência por zona com o detalhe da apuração (munzona), fora do critério, porque é o único dado por zona do 2º turno.',
        'B1 a B5: unidade, faixa 16 a 34 com 16 e 17, efeito fixo de UF, erro agrupado por UF, HC1 ao lado (só valem quando sair o 2º turno).',
        'C1: país = 27 UFs; sem o 2º turno, (c) só descreve o 1º.',
        'X1 a X9: estimativa ecológica fora do critério, com calibração no 1º turno e régua de utilidade escrita antes; não tem veredito.']
    sem_teste = [
        'Quem de fato compareceu a mais no 2º turno por idade, gênero e escolaridade: só o perfil oficial do 2º turno responde.',
        '(b) pela letra e a variação de (c) pela letra.',
        '(a) do 2º turno pela letra (perfil contra bweb).',
        'A estimativa ecológica não separa quem votou: ela supõe que, dentro da zona, a taxa de cada grupo não depende da seção.']
    R = {'teste': 'F15', 'registro': 'PRE-REGISTRO-2026-10-26.md, Adendo 21, commit 913af7a (31/10/2026 10:36:29 UTC)',
         'rodado_em': time.strftime('%d/%m/%Y %H:%M', time.gmtime()), 'sha256_script_decisoes': sha_dec,
         'sha256_script_rodado': sha256(os.path.abspath(__file__)),
         'veredito_linhas': ver, 'disponibilidade': disp, 'a': a, 'a_extra_munzona': extra, 'b': b, 'c': c,
         'exploratorio': X, 'pos_execucao': PX, 'desvios': desvios, 'sem_teste': sem_teste,
         'fontes': {'perfil': zperfil, 'tte': ztte, 'munzona': zmunz, 'bweb1t': d1, 'bweb2t': d2, 'base': fbase,
                    'perfil_secao': dpsec}}

    def limpa(o):
        if isinstance(o, dict): return {str(k): limpa(v) for k, v in o.items()}
        if isinstance(o, (list, tuple)): return [limpa(v) for v in o]
        if isinstance(o, (np.floating,)): return float(o)
        if isinstance(o, (np.integer,)): return int(o)
        if isinstance(o, float) and not math.isfinite(o): return None
        return o
    with open(sjson, 'w') as f:
        json.dump(limpa(R), f, ensure_ascii=False, indent=1)
    escrever_txt(limpa(R), stxt)
    print('ok', sjson, stxt)


if __name__ == '__main__':
    if len(sys.argv) >= 2 and sys.argv[1] == 'rodar':
        args = sys.argv[2:12]
        sha_dec = sys.argv[12] if len(sys.argv) > 12 else ''
        rodar(*args, sha_dec)
    else:
        print(__doc__)
        sys.exit(1)
