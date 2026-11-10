#!/usr/bin/env python3
"""R27_A2: ASSIMETRIA DO VAZAMENTO ENTRE FINALISTAS (teste D4-1 do Adendo 27, por inteiro).

Critérios: registro/adendo27/desenho_D4_proposta.json, teste D4-1 (commit 2748895, 10/11/2026
00:16:42 UTC), aplicados pela letra, sem mudar limiar. Este docstring foi escrito ANTES de
calcular qualquer resultado com votos. Uma cópia com data e SHA-256 fica em
/home/user/trabalho-eleicao/adendo27/A2/docstring_antes_de_rodar.txt.

Uso (sempre com python3 -I):
  python3 -I scripts/analisar_R27_A2.py perfil    extrai o perfil do eleitorado por seção (sem votos)
  python3 -I scripts/analisar_R27_A2.py gov2t     extrai governador do 2º turno por candidato (6 UFs)
  python3 -I scripts/analisar_R27_A2.py           roda o teste e grava resultados/R27_A2_assimetria_vazamento.json e .txt

O QUE O REGISTRO FIXA (aplicado como está escrito)
- Universo: seções apuradas nos dois turnos, diferença de aptos entre turnos de no máximo 2,
  comparecimento do 1º turno de pelo menos 30, fora do exterior, em locais com 2 ou mais seções válidas.
- Regressoras (contagens do 1º turno): L1, R1, um termo para cada eliminado com 0,5% ou mais dos
  válidos nacionais, os demais somados, B1, N1 e A1 = aptos menos comparecimento.
- Respostas (contagens do 2º turno): L2, R2, BN2 e A2.
- Estimador: mínimos quadrados com efeito fixo de local de votação, peso 1/aptos, erro agrupado por município.
- Primária: As = V menos M; V = coeficiente de R1 na equação de L2; M = coeficiente de L1 na equação de R2;
  intervalo por bootstrap de municípios, 500 réplicas.
- Secundárias: assimetria de retenção (L1 em L2 menos R1 em R2); decomposição do ganho de Lula por canal;
  coeficientes de R1 e de L1 na equação de A2.
- Variantes: (b) efeito fixo de município; (c) covariáveis de perfil; (d) eliminados somados (para comparar
  com 2014, 2018 e 2022); (e) redutos escolhidos pelo 2º turno de 2022 (75% ou mais), regressão de q sobre s e t
  com peso igual ao voto próprio do 1º turno, leitura = diferença dos interceptos; (f) As por UF e por tercil
  de escolaridade.
- Parte determinística: H = L2 menos (aptos menos R1); S = (L2 menos L1) menos (O1 + B1 + N1 + aumento de
  comparecimento, se houver); espelhos para Flávio; contagem e soma dos excessos positivos nos quatro anos.
- SINAL: As de 2026 >= 0,025; e As de 2026 >= 0,015 + maior |As| dos três anos placebo; e As >= 0,015 em (b), (c)
  e (d); e As >= 0,010 em 20 ou mais das 27 UFs; e assimetria de retenção >= 0,020 na regressão geral e nos redutos.
  Determinística: qualquer seção com H positivo vira caso individual; soma de S positivo de Lula menos a de
  Flávio >= 220 mil e >= 3 vezes a maior assimetria dos anos placebo indica excesso concentrado.
- SEM SINAL: |As| de 2026 <= 0,010 e limite superior do intervalo de 95% <= 0,015, com |As| <= 0,010 nos três
  anos placebo e com o efeito plantado de 3,57% recuperado (As sobe 0,025 ou mais) em cada ano placebo.
- INCONCLUSIVO: As entre 0,010 e 0,025; ou algum ano placebo com |As| acima de 0,015; ou variantes com sinais
  opostos; ou plantio recuperado em menos de 70%.
- Poder: plantar em 2014, 2018, 2022 e por cima de 2026 troca binomial de 0,9%, 1,8% e 3,57% dos votos de R
  para L, uniforme e concentrada em 30% das seções com o mesmo total; As deve subir cerca de 0,95 vez a fração.
- Placebos: (1) anos 2014, 2018, 2022 com eliminados somados; (2) o espelho M em 2026; (3) governador nas 6 UFs
  com 2º turno e As presidencial nas mesmas seções; (4) parte determinística nos quatro anos.

DECISÕES QUE O REGISTRO NÃO FIXA (tomadas aqui, antes de qualquer conta com votos; relatadas como desvios)
D1. "Apurada" = campo tipo igual a APURADA (sem diferenciar maiúsculas) nos dois turnos.
D2. A1 = aptos do 1º turno menos comparecimento do 1º; A2 = aptos do 2º menos comparecimento do 2º; peso =
    1/aptos do 1º turno. Como os aptos podem diferir em até 2, as linhas da matriz somam 1 só aproximadamente.
D3. Local de votação = UF, município, zona e número do local (lib.chave_local). Conferido na estrutura:
    o local nunca difere entre os turnos nas quatro bases.
D4. "Local com 2 ou mais seções válidas": contado depois dos outros filtros.
D5. Válidos nacionais do 1º turno = votos nominais dos 12 candidatos válidos (o 28, anulado, fica de fora do
    denominador). O 28 entra no termo "demais eliminados", porque a base o guarda em O.
D6. A função lib.fe_ols agrupa o erro pelo mesmo grupo do efeito fixo (o local). O registro pede efeito fixo
    de local com erro agrupado por município. Uso estimador próprio (mesma transformação within, mesmos pesos,
    erro CR1 por município, covariância entre equações pela função de influência) e confiro que os
    coeficientes são iguais aos de lib.fe_ols. Nas regressões dentro de uma UF e no placebo de governador,
    o DF (um só município) usa a zona eleitoral como grupo do erro e do bootstrap.
D7. Bootstrap: sorteio de municípios com reposição, 500 réplicas, semente 20261110, intervalo percentil
    de 2,5% a 97,5%. É feito para 2026, para os anos placebo, para as variantes e por UF.
D8. Variante (c): fonte = perfil_eleitor_secao_2026 (cadastro de 14/07/2026). Parcelas da seção: 16 a 24 anos
    (códigos 1600 a 2124), 60 anos ou mais (códigos 6064 a 9999), superior completo (código 8), mulheres
    (código 4), sobre o total de eleitores da seção no perfil. Como a regressão é em contagens, cada parcela
    entra multiplicada pelos aptos do 1º turno. Seções sem perfil ficam fora de (c). Ao lado, duas
    sensibilidades: (c_parcela) as quatro parcelas entram diretas, sem multiplicar; (c_sup2) "ensino superior"
    = completo mais incompleto.
D9. Variante (e), redutos: seção do universo de 2026 que existe com a mesma chave em 2022 e teve L+R > 0 no
    2º turno de 2022. Reduto de Lula: L/(L+R) >= 0,75 em 2022. Reduto de Flávio: R/(L+R) >= 0,75 (o 22 de 2022).
    Exige voto próprio do 1º turno > 0. s = (comparecimento do 1º menos voto próprio do 1º) / voto próprio do 1º
    (todos os demais votantes, inclusive os do adversário); t = (comparecimento do 2º menos o do 1º) / voto
    próprio do 1º. Mínimos quadrados com intercepto, sem efeito fixo, peso = voto próprio do 1º, erro agrupado
    por município. Leitura = intercepto dos redutos de Lula menos intercepto dos redutos de Flávio; intervalo
    por bootstrap conjunto de municípios (500). Placebo: 2022 com redutos escolhidos por 2018 e 2018 com
    redutos escolhidos por 2014 (2014 não tem ano anterior em disco). O efeito plantado também é medido aqui.
D10. Variante (f): As por UF = especificação principal dentro de cada UF. Tercil de escolaridade = tercis
    nacionais da parcela com superior completo entre as seções do universo com perfil; especificação principal
    dentro de cada tercil. Ao lado, sem entrar no critério: As por UF nos anos placebo, especificação (d).
D11. Parte determinística: H usa os aptos do 2º turno (ao lado, o maior entre os aptos dos dois turnos).
    S_L = (L2 - L1) - (O1 + B1 + N1 + max(0, comp2 - comp1)); S_R = (R2 - R1) - (o mesmo); H_R = R2 - (aptos - L1).
    Assimetria = soma de S_L positivo menos soma de S_R positivo. Nos anos placebo, L = PT e R = adversário;
    "maior assimetria dos anos placebo" = maior valor absoluto. Além do universo, H é varrido em todas as
    seções com os dois turnos (rede larga, inclusive exterior), relatado à parte.
D12. Placebo de governador: finalistas lidos do bweb do 2º turno; L = o finalista que venceu o 2º turno na UF,
    R = o outro (análogo do presidencial: troca do perdedor para o vencedor). Eliminado com 0,5% ou mais dos
    válidos da UF no 1º turno tem termo próprio, os demais somados. B e N são os do cargo de governador;
    A1 e A2 são os da seção. Conta por UF e conta conjunta das 6 UFs com eliminados somados. Ao lado, As
    presidencial nas mesmas seções. Leitura do placebo: valor absoluto de As.
D13. Efeito plantado: f = binomial(R2, p) por seção, tirado de R2 e somado a L2. Concentrado: 30% das seções
    sorteadas, com fração p * (soma de R2) / (soma de R2 nas sorteadas), para dar o mesmo total. Semente
    20261110 + índice do cenário. Anos placebo na especificação (d); 2026 na principal e na (d).
    Recuperação = (As plantado menos As bruto) / p. "Recuperado" = subida de 0,025 ou mais com p = 3,57%
    uniforme. "Menos de 70%" = recuperação abaixo de 0,70 no plantio uniforme de 3,57%. Espelho da calibração:
    plantar de L para R em 2026 (As deve cair o mesmo tanto). O plantio também é passado pela assimetria de
    retenção, pelos redutos e pela parte determinística, para dizer o que cada peça enxerga.
D14. Veredito da parte de regressão: SEM PODER se o plantio uniforme de 3,57% por cima de 2026 não fizer As
    subir 0,025 ou mais. Senão SINAL se todas as cláusulas do critério de sinal valerem; SEM SINAL se todas as
    do critério de sem sinal valerem; em qualquer outro caso INCONCLUSIVO, com a lista das cláusulas que
    falharam. Veredito da parte determinística: H positivo = caso individual (SINAL pontual); S pelo critério
    escrito; se o plantio de 3,57% não mover a assimetria de S em 220 mil ou mais, a parte determinística é
    declarada SEM PODER para troca espalhada (o registro já avisa disso).
D15. Tradução em votos: fração trocada estimada p = As / kappa, com kappa = recuperação medida no plantio de
    3,57% por cima de 2026; votos trocados = p / (1 - p) * 59.826.041 (voto oficial de Flávio no 2º turno);
    efeito na margem = 2 vezes isso, comparado com a margem oficial de 4.430.191. Ao lado, a conta direta
    V * (estoque de R1) menos M * (estoque de L1).
D16. Decomposição do ganho de Lula: coeficiente (para L1, coeficiente menos 1) vezes o estoque nacional do
    1º turno (todas as seções da base); o resto é o que ficou nos efeitos fixos de local.
D17. O valor bruto de 2026 aparece sempre ao lado de qualquer comparação com outro ano.

O QUE FOR FEITO DEPOIS DE VER O RESULTADO fica em funções com nome "exploratorio_" e sai marcado assim.
"""
import sys, os, gzip, json, zipfile, csv, glob, time, hashlib
import numpy as np

RAIZ = '/home/user/casa-control/eleicao-2026'
TRAB = '/home/user/trabalho-eleicao/adendo27/A2'
PERFIL_DIR = '/home/user/trabalho-eleicao/adendo21/F15_dl_perfil_secao'
ZIPS2T = '/home/user/trabalho-eleicao/trab2t/zips2t'
sys.path.insert(0, RAIZ + '/scripts')
from lib import carregar, chave_local, fe_ols, demean  # noqa: E402

SEMENTE = 20261110
NBOOT = 500
MARGEM = 4430191
L2_OFICIAL, R2_OFICIAL = 64256232, 59826041
NECESSARIO = 2215096
UFS_GOV = ['AC', 'AM', 'DF', 'ES', 'RN', 'TO']
P_PLANTIO = [0.009, 0.018, 0.0357]


# ---------------------------------------------------------------- extrações (sem resultado)
def _perfil_uf(z):
    import pandas as pd
    uf = os.path.basename(z).split('_')[-1][:2]
    jov = [1600, 1700, 1800, 1900, 2000, 2124]
    partes = []
    with zipfile.ZipFile(z) as zf:
        nome = [i.filename for i in zf.infolist() if i.filename.endswith('.csv')][0]
        with zf.open(nome) as f:
            it = pd.read_csv(f, sep=';', encoding='latin-1', chunksize=1500000,
                             usecols=['CD_MUNICIPIO', 'NR_ZONA', 'NR_SECAO', 'CD_GENERO', 'CD_FAIXA_ETARIA',
                                      'CD_GRAU_ESCOLARIDADE', 'QT_ELEITORES'])
            for ch in it:
                q = ch['QT_ELEITORES']
                ch = ch.assign(mul=q * (ch['CD_GENERO'] == 4), jov=q * ch['CD_FAIXA_ETARIA'].isin(jov),
                               ido=q * (ch['CD_FAIXA_ETARIA'] >= 6064), sup8=q * (ch['CD_GRAU_ESCOLARIDADE'] == 8),
                               sup7=q * (ch['CD_GRAU_ESCOLARIDADE'] == 7))
                partes.append(ch.groupby(['CD_MUNICIPIO', 'NR_ZONA', 'NR_SECAO'])[
                    ['QT_ELEITORES', 'mul', 'jov', 'ido', 'sup8', 'sup7']].sum())
    g = pd.concat(partes).groupby(level=[0, 1, 2]).sum()
    return {f'{uf}|{m}|{zn}|{s}': [int(x) for x in v] for (m, zn, s), v in zip(g.index, g.values)}


def extrair_perfil():
    from multiprocessing import Pool
    zips = [z for z in sorted(glob.glob(PERFIL_DIR + '/perfil_eleitor_secao_2026_*.zip')) if not z.endswith('_ZZ.zip')]
    zips.sort(key=os.path.getsize, reverse=True)
    out = {}
    with Pool(3) as p:
        for r in p.imap_unordered(_perfil_uf, zips):
            out.update(r)
            print(len(out), flush=True)
    with gzip.open(TRAB + '/perfil_secao_2026.json.gz', 'wt') as f:
        json.dump({'colunas': ['total', 'mulheres', 'de16a24', 'de60mais', 'superior_completo', 'superior_incompleto'],
                   'secoes': out}, f)
    print('perfil: secoes', len(out), 'eleitores', sum(v[0] for v in out.values()))


def extrair_gov2t():
    out = {}
    for uf in UFS_GOV:
        z = glob.glob(f'{ZIPS2T}/bweb_2t_{uf}_*.zip')[0]
        nlin = 0
        with zipfile.ZipFile(z) as zf:
            nome = [i.filename for i in zf.infolist() if i.filename.endswith('.csv')][0]
            with zf.open(nome) as f:
                cab = [c.strip('"') for c in f.readline().decode('latin-1').rstrip('\r\n').split(';')]
                ix = {c: i for i, c in enumerate(cab)}
                for raw in f:
                    if b'"Governador"' not in raw:
                        continue
                    row = next(csv.reader([raw.decode('latin-1')], delimiter=';', quotechar='"'))
                    if row[ix['CD_CARGO_PERGUNTA']] != '3':
                        continue
                    nlin += 1
                    k = f"{row[ix['SG_UF']]}|{int(row[ix['CD_MUNICIPIO']])}|{int(row[ix['NR_ZONA']])}|{int(row[ix['NR_SECAO']])}"
                    s = out.setdefault(k, {'nom': {}, 'B': 0, 'N': 0, 'outros': 0})
                    tp = row[ix['DS_TIPO_VOTAVEL']].strip().lower()
                    q = int(row[ix['QT_VOTOS']])
                    if tp == 'nominal':
                        s['nom'][row[ix['NR_VOTAVEL']]] = s['nom'].get(row[ix['NR_VOTAVEL']], 0) + q
                    elif tp == 'branco':
                        s['B'] += q
                    elif tp == 'nulo':
                        s['N'] += q
                    else:
                        s['outros'] += q
        print(uf, 'linhas do cargo 3:', nlin, flush=True)
    with gzip.open(TRAB + '/gov2t_6ufs.json.gz', 'wt') as f:
        json.dump(out, f)
    print('gov2t: secoes', len(out))


# ---------------------------------------------------------------- montagem das bases
CAMPOS = ['apt1', 'comp1', 'L1', 'R1', 'O1', 'B1', 'N1', 'apt2', 'comp2', 'L2', 'R2', 'B2', 'N2']


def montar(ano, d=None):
    """Vetores por seção com os dois turnos. Devolve dict de arrays (todas as seções com 1 e 2)."""
    d = d or carregar(f'{RAIZ}/dados/secoes{ano}.json.gz')
    ch = [k for k, v in d.items() if '1' in v and '2' in v]
    n = len(ch)
    b = {c: np.zeros(n, dtype=np.int64) for c in CAMPOS}
    uf = np.empty(n, dtype='U2'); mun = np.empty(n, dtype='U12'); zona = np.empty(n, dtype='U18'); loc = np.empty(n, dtype='U28')
    apur = np.zeros(n, dtype=bool)
    for i, k in enumerate(ch):
        v = d[k]; a, c = v['1'], v['2']
        p = k.split('|')
        uf[i] = p[0]; mun[i] = p[0] + '|' + p[1]; zona[i] = p[0] + '|' + p[1] + '|' + p[2]; loc[i] = chave_local(k, a)
        apur[i] = str(a.get('tipo', '')).upper() == 'APURADA' and str(c.get('tipo', '')).upper() == 'APURADA'
        b['apt1'][i] = a['apt']; b['comp1'][i] = a['comp']; b['L1'][i] = a['L']; b['R1'][i] = a['R']
        b['O1'][i] = a['O']; b['B1'][i] = a['B']; b['N1'][i] = a['N']
        b['apt2'][i] = c['apt']; b['comp2'][i] = c['comp']; b['L2'][i] = c['L']; b['R2'][i] = c['R']
        b['B2'][i] = c['B']; b['N2'][i] = c['N']
    b.update(chave=np.array(ch), uf=uf, mun=mun, zona=zona, loc=loc, apur=apur)
    b['A1'] = b['apt1'] - b['comp1']; b['A2'] = b['apt2'] - b['comp2']; b['BN2'] = b['B2'] + b['N2']
    # universo
    u = apur & (np.abs(b['apt1'] - b['apt2']) <= 2) & (b['comp1'] >= 30) & (uf != 'ZZ')
    _, g = np.unique(loc, return_inverse=True)
    cnt = np.bincount(g, weights=u.astype(float))
    u = u & (cnt[g] >= 2)
    b['univ'] = u
    return b


def sub(b, m):
    return {k: v[m] for k, v in b.items()}


# ---------------------------------------------------------------- estimador
class Ajuste:
    """MQO com efeito fixo (within), pesos, erro CR1 por grupo cl, várias respostas com as mesmas regressoras."""

    def __init__(self, Y, X, fe, cl, w, nx, ny):
        Y = np.asarray(Y, float); X = np.asarray(X, float); w = np.asarray(w, float)
        if Y.ndim == 1:
            Y = Y[:, None]
        _, g = np.unique(fe, return_inverse=True)
        ok = np.bincount(g)[g] >= 2
        self.ok = ok
        Y, X, w, g, cl = Y[ok], X[ok], w[ok], g[ok], np.asarray(cl)[ok]
        _, g = np.unique(g, return_inverse=True)
        _, c = np.unique(cl, return_inverse=True)
        self.n, self.k, self.m = len(g), X.shape[1], Y.shape[1]
        self.nfe, self.G = int(g.max() + 1), int(c.max() + 1)
        self.nx, self.ny = list(nx), list(ny)
        self.ix = {a: i for i, a in enumerate(nx)}; self.iy = {a: i for i, a in enumerate(ny)}
        Xd = demean(X, g, w); Yd = demean(Y, g, w)
        WX = Xd * w[:, None]
        self.WX = WX
        self.A = Xd.T @ WX
        self.Ainv = np.linalg.inv(self.A)
        self.beta = self.Ainv @ (WX.T @ Yd)
        E = Yd - Xd @ self.beta
        G, k, m = self.G, self.k, self.m
        self.Am = np.zeros((G, k, k)); self.Bm = np.zeros((G, k, m)); self.Sm = np.zeros((G, k, m))
        for i in range(k):
            for j in range(i, k):
                v = np.bincount(c, weights=WX[:, i] * Xd[:, j], minlength=G)
                self.Am[:, i, j] = v; self.Am[:, j, i] = v
            for y in range(m):
                self.Bm[:, i, y] = np.bincount(c, weights=WX[:, i] * Yd[:, y], minlength=G)
                self.Sm[:, i, y] = np.bincount(c, weights=WX[:, i] * E[:, y], minlength=G)
        self.cfac = G / (G - 1) * (self.n - 1) / (self.n - k) if G > 1 else float('nan')
        self._boot = None

    def coef(self, x, y):
        return float(self.beta[self.ix[x], self.iy[y]])

    def comb(self, termos):
        """Combinação linear de coeficientes [(x, y, sinal)]: estimativa e erro-padrão agrupado."""
        est = sum(s * self.beta[self.ix[x], self.iy[y]] for x, y, s in termos)
        psi = sum(s * (self.Sm[:, :, self.iy[y]] @ self.Ainv[self.ix[x]]) for x, y, s in termos)
        return float(est), float(np.sqrt(self.cfac * (psi ** 2).sum()))

    def boot(self, nrep=NBOOT, semente=SEMENTE):
        if self._boot is None:
            rng = np.random.default_rng(semente)
            out = np.empty((nrep, self.k, self.m))
            for r in range(nrep):
                cnt = np.bincount(rng.integers(0, self.G, self.G), minlength=self.G).astype(float)
                out[r] = np.linalg.solve(np.tensordot(cnt, self.Am, 1), np.tensordot(cnt, self.Bm, 1))
            self._boot = out
        return self._boot

    def comb_boot(self, termos):
        bt = self.boot()
        v = sum(s * bt[:, self.ix[x], self.iy[y]] for x, y, s in termos)
        return {'ic95': [float(np.percentile(v, 2.5)), float(np.percentile(v, 97.5))], 'dp_boot': float(v.std(ddof=1))}

    def novo_y(self, Y):
        """Coeficientes para outra matriz de respostas (mesmas regressoras), sem refazer o resto."""
        Y = np.asarray(Y, float)[self.ok]
        return self.Ainv @ (self.WX.T @ Y)


T_AS = [('R1', 'L2', 1), ('L1', 'R2', -1)]
T_RET = [('L1', 'L2', 1), ('R1', 'R2', -1)]
NY = ['L2', 'R2', 'BN2', 'A2']


def grupo_erro(b, dentro_de_uf=False):
    cl = b['mun'].copy()
    if dentro_de_uf:
        df = b['uf'] == 'DF'
        cl[df] = b['zona'][df]
    return cl


def regressao(b, nx, fe='loc', extra=None, nomes_extra=(), dentro_de_uf=False, boot=True, semente=SEMENTE):
    """Roda as quatro equações e devolve (ajuste, resumo). b já é o subconjunto a usar."""
    X = np.column_stack([b[c] for c in nx] + ([extra] if extra is not None else []))
    nomes = list(nx) + list(nomes_extra)
    Y = np.column_stack([b[c] for c in NY])
    aj = Ajuste(Y, X, b[fe], grupo_erro(b, dentro_de_uf), 1.0 / b['apt1'], nomes, NY)
    r = resumo(aj, boot, semente)
    return aj, r


def resumo(aj, boot=True, semente=SEMENTE):
    V, epV = aj.comb([('R1', 'L2', 1)]); M, epM = aj.comb([('L1', 'R2', 1)])
    As, epAs = aj.comb(T_AS); ret, epret = aj.comb(T_RET)
    r = {'n': aj.n, 'locais_ou_grupos_fe': aj.nfe, 'grupos_erro': aj.G,
         'V': V, 'ep_V': epV, 'M': M, 'ep_M': epM, 'As': As, 'ep_As': epAs,
         'ret_L': aj.coef('L1', 'L2'), 'ep_ret_L': aj.comb([('L1', 'L2', 1)])[1],
         'ret_R': aj.coef('R1', 'R2'), 'ep_ret_R': aj.comb([('R1', 'R2', 1)])[1],
         'assim_retencao': ret, 'ep_assim_retencao': epret,
         'R1_em_A2': aj.coef('R1', 'A2'), 'ep_R1_em_A2': aj.comb([('R1', 'A2', 1)])[1],
         'L1_em_A2': aj.coef('L1', 'A2'), 'ep_L1_em_A2': aj.comb([('L1', 'A2', 1)])[1],
         'matriz': {y: {x: aj.coef(x, y) for x in aj.nx} for y in aj.ny},
         'matriz_ep': {y: {x: aj.comb([(x, y, 1)])[1] for x in aj.nx} for y in aj.ny},
         'soma_das_linhas': {x: float(sum(aj.coef(x, y) for y in aj.ny)) for x in aj.nx}}
    if boot:
        aj.boot(NBOOT, semente)
        for nome, t in (('As', T_AS), ('V', [('R1', 'L2', 1)]), ('M', [('L1', 'R2', 1)]), ('assim_retencao', T_RET)):
            cb = aj.comb_boot(t)
            r['ic95_' + nome] = cb['ic95']; r['dp_boot_' + nome] = cb['dp_boot']
    return r


def as_de(beta, aj):
    return float(beta[aj.ix['R1'], aj.iy['L2']] - beta[aj.ix['L1'], aj.iy['R2']])


def ret_de(beta, aj):
    return float(beta[aj.ix['L1'], aj.iy['L2']] - beta[aj.ix['R1'], aj.iy['R2']])


# ---------------------------------------------------------------- plantio
def plantar(b, p, modo, rng, de='R'):
    """Devolve (L2, R2) com a troca plantada. de='R': tira de R2 e soma em L2. de='L': o contrário."""
    fonte = b['R2'] if de == 'R' else b['L2']
    if modo == 'uniforme':
        f = rng.binomial(fonte, p)
    else:
        n = len(fonte)
        sel = np.zeros(n, bool); sel[rng.permutation(n)[: int(round(0.30 * n))]] = True
        pc = p * fonte.sum() / fonte[sel].sum()
        f = np.where(sel, rng.binomial(fonte, min(pc, 1.0)), 0)
    if de == 'R':
        return b['L2'] + f, b['R2'] - f, int(f.sum())
    return b['L2'] - f, b['R2'] + f, int(f.sum())


def y_plantado(b, L2, R2):
    return np.column_stack([L2, R2, b['BN2'], b['A2']])


# ---------------------------------------------------------------- redutos
def wls_cp(y, X, w, c, G):
    WX = X * w[:, None]
    k = X.shape[1]
    Am = np.zeros((G, k, k)); Bm = np.zeros((G, k))
    for i in range(k):
        for j in range(k):
            Am[:, i, j] = np.bincount(c, weights=WX[:, i] * X[:, j], minlength=G)
        Bm[:, i] = np.bincount(c, weights=WX[:, i] * y, minlength=G)
    A = Am.sum(0); beta = np.linalg.solve(A, Bm.sum(0))
    e = y - X @ beta
    Sm = np.column_stack([np.bincount(c, weights=WX[:, i] * e, minlength=G) for i in range(k)])
    Ainv = np.linalg.inv(A)
    Gef = int((np.bincount(c, minlength=G) > 0).sum()); n = len(y)
    V = Gef / (Gef - 1) * (n - 1) / (n - k) * Ainv @ (Sm.T @ Sm) @ Ainv
    return beta, np.sqrt(np.diag(V)), Am, Bm


def redutos(b, lado_ref, L2=None, R2=None, semente=SEMENTE, boot=True):
    """b: universo do ano; lado_ref: array com parcela de L em L+R no 2º turno do ano anterior (nan sem ligação).
    Devolve interceptos dos redutos de L e de R e a diferença (L menos R)."""
    L2 = b['L2'] if L2 is None else L2; R2 = b['R2'] if R2 is None else R2
    _, c = np.unique(b['mun'], return_inverse=True); G = int(c.max() + 1)
    res = {}; cps = {}
    for lado, sel, p1, p2 in (('L', lado_ref >= 0.75, b['L1'], L2), ('R', lado_ref <= 0.25, b['R1'], R2)):
        m = sel & (p1 > 0)
        own = p1[m].astype(float)
        q = p2[m] / own; s = (b['comp1'][m] - p1[m]) / own; t = (b['comp2'][m] - b['comp1'][m]) / own
        X = np.column_stack([np.ones(m.sum()), s, t])
        beta, ep, Am, Bm = wls_cp(q, X, own, c[m], G)
        cps[lado] = (Am, Bm)
        res[lado] = {'n': int(m.sum()), 'municipios': int(len(np.unique(c[m]))), 'voto_proprio_1t': int(p1[m].sum()),
                     'intercepto': float(beta[0]), 'ep_intercepto': float(ep[0]),
                     'coef_s': float(beta[1]), 'ep_s': float(ep[1]), 'coef_t': float(beta[2]), 'ep_t': float(ep[2]),
                     'q_medio_ponderado': float(p2[m].sum() / p1[m].sum()),
                     's_medio_ponderado': float((b['comp1'][m] - p1[m]).sum() / p1[m].sum()),
                     't_medio_ponderado': float((b['comp2'][m] - b['comp1'][m]).sum() / p1[m].sum())}
    res['dif_L_menos_R'] = res['L']['intercepto'] - res['R']['intercepto']
    res['ep_dif_soma_quadrados'] = float(np.hypot(res['L']['ep_intercepto'], res['R']['ep_intercepto']))
    if boot:
        rng = np.random.default_rng(semente)
        v = np.empty(NBOOT)
        for r in range(NBOOT):
            cnt = np.bincount(rng.integers(0, G, G), minlength=G).astype(float)
            a = [np.linalg.solve(np.tensordot(cnt, cps[x][0], 1), np.tensordot(cnt, cps[x][1], 1))[0] for x in ('L', 'R')]
            v[r] = a[0] - a[1]
        res['ic95_dif'] = [float(np.percentile(v, 2.5)), float(np.percentile(v, 97.5))]
        res['dp_boot_dif'] = float(v.std(ddof=1))
    return res


def parcela_L_ano_anterior(b, ant):
    """Para cada seção de b, L/(L+R) do 2º turno na base ant (dict de arrays), pela mesma chave; nan sem ligação."""
    tot = (ant['L2'] + ant['R2']).astype(float)
    ref = dict(zip(ant['chave'].tolist(), np.where(tot > 0, ant['L2'] / np.where(tot > 0, tot, 1), np.nan).tolist()))
    return np.array([ref.get(k, np.nan) for k in b['chave'].tolist()])


# ---------------------------------------------------------------- parte determinística
def deterministica(b, L2=None, R2=None):
    L2 = b['L2'] if L2 is None else L2; R2 = b['R2'] if R2 is None else R2
    fontes = b['O1'] + b['B1'] + b['N1'] + np.maximum(0, b['comp2'] - b['comp1'])
    HL = L2 - (b['apt2'] - b['R1']); HR = R2 - (b['apt2'] - b['L1'])
    amax = np.maximum(b['apt1'], b['apt2'])
    HLm = L2 - (amax - b['R1']); HRm = R2 - (amax - b['L1'])
    SL = (L2 - b['L1']) - fontes; SR = (R2 - b['R1']) - fontes
    pos = lambda x: {'secoes': int((x > 0).sum()), 'soma': int(x[x > 0].sum())}
    r = {'n': int(len(L2)), 'H_L': pos(HL), 'H_R': pos(HR), 'H_L_aptos_max': pos(HLm), 'H_R_aptos_max': pos(HRm),
         'S_L': pos(SL), 'S_R': pos(SR)}
    r['assimetria_S'] = r['S_L']['soma'] - r['S_R']['soma']
    r['fontes_sobre_comparecimento_mediana'] = float(np.median(fontes / b['comp1']))
    r['parcela_secoes_fontes_acima_6pct'] = float((fontes / b['comp1'] > 0.06).mean())
    return r, HL, HR, SL, SR


def ic(x):
    return f'[{x[0]:+.4f}; {x[1]:+.4f}]'


# ---------------------------------------------------------------- principal
def main():
    t0 = time.time()
    S = {'teste': 'R27_A2 (D4-1) assimetria do vazamento', 'registro': 'registro/adendo27/desenho_D4_proposta.json, D4-1; commit 2748895',
         'semente': SEMENTE, 'bootstrap_replicas': NBOOT}
    doc = __doc__
    S['sha256_docstring'] = hashlib.sha256(doc.encode()).hexdigest()
    T = []  # linhas do txt

    def P(*a):
        s = ' '.join(str(x) for x in a)
        print(s, flush=True); T.append(s)

    # ---------- bases
    B = {}
    for ano in (2014, 2018, 2022, 2026):
        B[ano] = montar(ano)
        print(ano, 'montado', round(time.time() - t0), 's', flush=True)
    b26 = B[2026]
    cand = carregar(f'{RAIZ}/dados/candidatos2026_1t.json.gz')
    tot = {k: int(v) for k, v in cand['totais'].items()}
    validos1 = sum(v for k, v in tot.items() if k != '28')
    elim = sorted([k for k in tot if k not in ('13', '22', '28') and tot[k] / validos1 >= 0.005], key=lambda k: -tot[k])
    S['primeiro_turno_2026'] = {'totais': tot, 'validos_sem_28': validos1,
                                'eliminados_com_termo_proprio': {k: {'nome': cand['nomes'][k], 'votos': tot[k], 'parcela_validos': tot[k] / validos1} for k in elim}}
    sc = cand['secoes']
    for k in elim:
        b26['E' + k] = np.array([sc[c].get(k, 0) for c in b26['chave'].tolist()], dtype=np.int64)
    b26['Edem'] = b26['O1'] - sum(b26['E' + k] for k in elim)
    assert (b26['Edem'] >= 0).all()
    del cand, sc
    NX_P = ['L1', 'R1'] + ['E' + k for k in elim] + ['Edem', 'B1', 'N1', 'A1']
    NX_D = ['L1', 'R1', 'O1', 'B1', 'N1', 'A1']

    U = {ano: sub(B[ano], B[ano]['univ']) for ano in B}
    S['universo'] = {}
    for ano in B:
        b = B[ano]; u = U[ano]
        S['universo'][str(ano)] = {
            'secoes_com_dois_turnos': int(len(b['chave'])), 'apuradas_nos_dois': int(b['apur'].sum()),
            'universo_secoes': int(len(u['chave'])), 'universo_locais': int(len(np.unique(u['loc']))),
            'universo_municipios': int(len(np.unique(u['mun']))),
            'L1': int(u['L1'].sum()), 'R1': int(u['R1'].sum()), 'L2': int(u['L2'].sum()), 'R2': int(u['R2'].sum()),
            'O1': int(u['O1'].sum()), 'B1': int(u['B1'].sum()), 'N1': int(u['N1'].sum()), 'A1': int(u['A1'].sum()),
            'comp1': int(u['comp1'].sum()), 'comp2': int(u['comp2'].sum()),
            'base_inteira': {c: int(b[c].sum()) for c in ('L1', 'R1', 'O1', 'B1', 'N1', 'A1', 'L2', 'R2', 'comp1', 'comp2', 'apt1', 'apt2')},
            'cobertura_R2': float(u['R2'].sum() / b['R2'].sum()), 'cobertura_L2': float(u['L2'].sum() / b['L2'].sum())}
    u26 = U[2026]

    P('R27_A2 (D4-1): ASSIMETRIA DO VAZAMENTO ENTRE FINALISTAS')
    P('Critérios fixados antes de rodar: registro/adendo27/desenho_D4_proposta.json, D4-1 (commit 2748895).')
    P('Decisões não fixadas pelo registro: D1 a D17 do docstring de scripts/analisar_R27_A2.py, escritas antes das contas.')
    P('')
    P('1. UNIVERSO')
    for ano in (2026, 2022, 2018, 2014):
        x = S['universo'][str(ano)]
        P(f"  {ano}: {x['universo_secoes']:,} seções em {x['universo_locais']:,} locais e {x['universo_municipios']:,} municípios; "
          f"cobre {100*x['cobertura_L2']:.2f}% do voto de L e {100*x['cobertura_R2']:.2f}% do voto de R no 2º turno.".replace(',', '.'))
    P('  Eliminados com termo próprio em 2026 (0,5% ou mais dos válidos): ' + ', '.join(
        f"{k} {v['nome']} ({100*v['parcela_validos']:.2f}%)" for k, v in S['primeiro_turno_2026']['eliminados_com_termo_proprio'].items()) + '; demais somados.')

    # ---------- regressão principal 2026
    aj26, r26 = regressao(u26, NX_P)
    # conferência com lib.fe_ols (coeficientes)
    Xc = np.column_stack([u26[c] for c in NX_P])
    chk = max(abs(fe_ols(u26[y], Xc, u26['loc'], 1.0 / u26['apt1'], NX_P)['coef'][x] - aj26.coef(x, y)) for y in ('L2', 'R2') for x in NX_P)
    r26['maior_diferenca_para_lib_fe_ols'] = float(chk)
    S['principal_2026'] = r26
    # variantes
    ajb, rb = regressao(u26, NX_P, fe='mun')
    ajd, rd = regressao(u26, NX_D)
    S['variante_b_fe_municipio'] = rb; S['variante_d_eliminados_somados'] = rd

    # perfil
    with gzip.open(TRAB + '/perfil_secao_2026.json.gz', 'rt') as f:
        pf = json.load(f)['secoes']
    nan6 = [np.nan] * 6
    PF = np.array([pf.get(k, nan6) for k in u26['chave'].tolist()], dtype=float)
    del pf
    tem = np.isfinite(PF[:, 0]) & (PF[:, 0] > 0)
    par = PF[:, 1:5] / np.where(tem, PF[:, 0], np.nan)[:, None]   # mulheres, 16-24, 60+, superior completo
    par_sup2 = (PF[:, 4] + PF[:, 5]) / np.where(tem, PF[:, 0], np.nan)
    S['perfil'] = {'secoes_do_universo_com_perfil': int(tem.sum()), 'sem_perfil': int((~tem).sum()),
                   'correlacao_total_perfil_aptos': float(np.corrcoef(PF[tem, 0], u26['apt1'][tem])[0, 1]),
                   'total_perfil_igual_aptos_1t': int((PF[tem, 0] == u26['apt1'][tem]).sum()),
                   'media_parcelas': {n_: float(np.nanmean(par[:, i])) for i, n_ in enumerate(['mulheres', 'de16a24', 'de60mais', 'superior_completo'])}}
    uc = sub(u26, tem); parc = par[tem]
    nomes_c = ['c_mulheres', 'c_16a24', 'c_60mais', 'c_superior']
    ajc, rc = regressao(uc, NX_P, extra=parc * uc['apt1'][:, None], nomes_extra=nomes_c)
    _, rc_par = regressao(uc, NX_P, extra=parc, nomes_extra=nomes_c)
    parc2 = parc.copy(); parc2[:, 3] = par_sup2[tem]
    _, rc_sup2 = regressao(uc, NX_P, extra=parc2 * uc['apt1'][:, None], nomes_extra=nomes_c)
    _, rc_base = regressao(uc, NX_P, boot=False)   # principal nas mesmas seções de (c)
    S['variante_c_perfil'] = rc; S['variante_c_parcela_direta'] = rc_par; S['variante_c_sup2'] = rc_sup2
    S['principal_nas_secoes_de_c'] = {k: rc_base[k] for k in ('n', 'V', 'M', 'As', 'ep_As', 'assim_retencao')}

    # ---------- anos placebo (especificação d)
    AJ = {2026: ajd}; RD = {2026: rd}
    for ano in (2014, 2018, 2022):
        AJ[ano], RD[ano] = regressao(U[ano], NX_D)
        S[f'placebo_{ano}_d'] = RD[ano]

    P('')
    P('2. REGRESSÃO (efeito fixo de local, peso 1/aptos, erro por município; intervalo = bootstrap de municípios, 500)')
    P('  V = parcela do estoque de R do 1º turno que aparece em L no 2º. M = o espelho. As = V menos M.')

    def linha(nome, r):
        P(f"  {nome:38s} V={r['V']:+.4f} ({r['ep_V']:.4f})  M={r['M']:+.4f} ({r['ep_M']:.4f})  As={r['As']:+.4f} ({r['ep_As']:.4f}) "
          f"IC95 {ic(r['ic95_As']) if 'ic95_As' in r else 'n/d'}  ret L={r['ret_L']:.4f} R={r['ret_R']:.4f} dif={r['assim_retencao']:+.4f} ({r['ep_assim_retencao']:.4f})  n={r['n']}")
    linha('2026 principal (um termo por eliminado)', r26)
    linha('2026 (b) efeito fixo de município', rb)
    linha('2026 (c) com perfil da seção', rc)
    linha('2026 (c_parcela) sensibilidade', rc_par)
    linha('2026 (c_sup2) sensibilidade', rc_sup2)
    linha('2026 (d) eliminados somados', rd)
    for ano in (2022, 2018, 2014):
        linha(f'{ano} placebo (d)', RD[ano])
    P(f"  Conferência do estimador: maior diferença de coeficiente para lib.fe_ols = {chk:.2e}.")
    P('  Matriz de transferência de 2026 (principal): linha = origem no 1º turno; colunas L2, R2, BN2, A2; soma')
    for x in aj26.nx:
        P(f"    {x:6s} " + '  '.join(f"{aj26.coef(x, y):+.4f} ({aj26.comb([(x, y, 1)])[1]:.4f})" for y in NY) + f"   {r26['soma_das_linhas'][x]:.4f}")
    P(f"  Quem não voltou (equação de A2): R1 = {r26['R1_em_A2']:+.4f} ({r26['ep_R1_em_A2']:.4f}); L1 = {r26['L1_em_A2']:+.4f} ({r26['ep_L1_em_A2']:.4f}).")

    # ---------- decomposição do ganho de Lula
    nac = S['universo']['2026']['base_inteira']
    est = {'L1': nac['L1'], 'R1': nac['R1'], 'B1': nac['B1'], 'N1': nac['N1'], 'A1': nac['A1']}
    for k in elim:
        est['E' + k] = tot[k]
    est['Edem'] = nac['O1'] - sum(tot[k] for k in elim)
    dec = {}
    for x in aj26.nx:
        c_ = aj26.coef(x, 'L2') - (1.0 if x == 'L1' else 0.0)
        dec[x] = {'coef': aj26.coef(x, 'L2'), 'ep': aj26.comb([(x, 'L2', 1)])[1], 'estoque_nacional': int(est[x]), 'votos': float(c_ * est[x])}
    ganho = nac['L2'] - nac['L1']
    S['decomposicao_ganho_lula'] = {'canais': dec, 'ganho_nacional': int(ganho), 'soma_canais': float(sum(v['votos'] for v in dec.values())),
                                    'resto_efeitos_fixos': float(ganho - sum(v['votos'] for v in dec.values()))}
    P('')
    P(f"3. DECOMPOSIÇÃO DO GANHO DE LULA ENTRE OS TURNOS (ganho nacional = {ganho:,} votos)".replace(',', '.'))
    rot = {'L1': 'perda de retenção própria', 'R1': 'vazamento (estoque de Flávio)', 'Edem': 'demais eliminados', 'B1': 'brancos', 'N1': 'nulos', 'A1': 'abstenção do 1º turno'}
    for x in aj26.nx:
        P(f"  {rot.get(x, 'eliminado ' + x[1:]):32s} coef {dec[x]['coef']:+.4f} x estoque {dec[x]['estoque_nacional']:>11,} = {dec[x]['votos']:>+13,.0f}".replace(',', '.'))
    P(f"  soma dos canais = {S['decomposicao_ganho_lula']['soma_canais']:,.0f}; resto (efeitos fixos de local) = {S['decomposicao_ganho_lula']['resto_efeitos_fixos']:,.0f}".replace(',', '.'))

    # ---------- (f) por UF e por tercil
    ufs = sorted(set(u26['uf'].tolist()))
    S['por_uf'] = {}
    for i, uf in enumerate(ufs):
        m = u26['uf'] == uf
        _, r = regressao(sub(u26, m), NX_P, dentro_de_uf=True, semente=SEMENTE + 100 + i)
        e = {k: r[k] for k in ('n', 'grupos_erro', 'V', 'M', 'As', 'ep_As', 'ic95_As', 'assim_retencao', 'ep_assim_retencao')}
        for ano in (2014, 2018, 2022):
            mm = U[ano]['uf'] == uf
            _, ra = regressao(sub(U[ano], mm), NX_D, dentro_de_uf=True, boot=False)
            e[f'As_{ano}_d'] = ra['As']; e[f'ep_As_{ano}_d'] = ra['ep_As']
        _, rdd = regressao(sub(u26, m), NX_D, dentro_de_uf=True, boot=False)
        e['As_2026_d'] = rdd['As']
        S['por_uf'][uf] = e
    n_uf_10 = sum(1 for e in S['por_uf'].values() if e['As'] >= 0.010)
    S['ufs_com_As_ge_0010'] = n_uf_10
    S['ufs_com_As_positivo'] = sum(1 for e in S['por_uf'].values() if e['As'] > 0)
    asuf = np.array([S['por_uf'][u]['As'] for u in ufs])
    S['dispersao_As_ufs'] = {'min': float(asuf.min()), 'max': float(asuf.max()), 'dp': float(asuf.std(ddof=1)), 'mediana': float(np.median(asuf)),
                             'dp_2022_d': float(np.std([S['por_uf'][u]['As_2022_d'] for u in ufs], ddof=1)),
                             'dp_2018_d': float(np.std([S['por_uf'][u]['As_2018_d'] for u in ufs], ddof=1)),
                             'dp_2014_d': float(np.std([S['por_uf'][u]['As_2014_d'] for u in ufs], ddof=1)),
                             'dp_2026_d': float(np.std([S['por_uf'][u]['As_2026_d'] for u in ufs], ddof=1))}
    P('')
    P('4. As POR UF (2026 principal; ao lado, especificação (d) em 2026, 2022, 2018 e 2014)')
    for uf in ufs:
        e = S['por_uf'][uf]
        P(f"  {uf}: As={e['As']:+.4f} ({e['ep_As']:.4f}) IC95 {ic(e['ic95_As'])} V={e['V']:+.4f} M={e['M']:+.4f} n={e['n']:>6}  | (d) 2026 {e['As_2026_d']:+.4f}  2022 {e['As_2022_d']:+.4f}  2018 {e['As_2018_d']:+.4f}  2014 {e['As_2014_d']:+.4f}")
    P(f"  UFs com As de 0,010 ou mais: {n_uf_10} de 27 (critério de sinal pede 20). UFs com As positivo: {S['ufs_com_As_positivo']}.")
    d_ = S['dispersao_As_ufs']
    P(f"  Dispersão entre UFs (desvio-padrão de As): 2026 principal {d_['dp']:.4f}; (d) 2026 {d_['dp_2026_d']:.4f}, 2022 {d_['dp_2022_d']:.4f}, 2018 {d_['dp_2018_d']:.4f}, 2014 {d_['dp_2014_d']:.4f}.")
    # tercil de escolaridade
    sup = parc[:, 3]
    cortes = np.quantile(sup, [1 / 3, 2 / 3])
    terc = np.digitize(sup, cortes)
    S['por_tercil_escolaridade'] = {'cortes_parcela_superior_completo': cortes.tolist()}
    for t_ in range(3):
        _, r = regressao(sub(uc, terc == t_), NX_P, semente=SEMENTE + 200 + t_)
        S['por_tercil_escolaridade'][f'tercil_{t_+1}'] = {k: r[k] for k in ('n', 'V', 'ep_V', 'M', 'ep_M', 'As', 'ep_As', 'ic95_As', 'assim_retencao', 'ep_assim_retencao')}
        P(f"  Tercil {t_+1} de escolaridade: As={r['As']:+.4f} ({r['ep_As']:.4f}) IC95 {ic(r['ic95_As'])} V={r['V']:+.4f} M={r['M']:+.4f} n={r['n']}")

    # ---------- (e) redutos
    ref26 = parcela_L_ano_anterior(u26, B[2022]); ref22 = parcela_L_ano_anterior(U[2022], B[2018]); ref18 = parcela_L_ano_anterior(U[2018], B[2014])
    RED = {2026: redutos(u26, ref26), 2022: redutos(U[2022], ref22), 2018: redutos(U[2018], ref18)}
    S['redutos'] = {str(a): r for a, r in RED.items()}
    S['redutos']['ligacao'] = {'2026_com_2022': int(np.isfinite(ref26).sum()), '2022_com_2018': int(np.isfinite(ref22).sum()), '2018_com_2014': int(np.isfinite(ref18).sum())}
    P('')
    P('5. REDUTOS (escolhidos pelo 2º turno do ano anterior, 75% ou mais; intercepto = retenção com fontes zero)')
    for a in (2026, 2022, 2018):
        r = RED[a]
        P(f"  {a}: redutos de L: intercepto {r['L']['intercepto']:.4f} ({r['L']['ep_intercepto']:.4f}), n={r['L']['n']}, q médio {r['L']['q_medio_ponderado']:.4f}; "
          f"redutos de R: intercepto {r['R']['intercepto']:.4f} ({r['R']['ep_intercepto']:.4f}), n={r['R']['n']}, q médio {r['R']['q_medio_ponderado']:.4f}; "
          f"diferença L menos R = {r['dif_L_menos_R']:+.4f} IC95 {ic(r['ic95_dif'])}")

    # ---------- parte determinística
    S['deterministica'] = {}
    P('')
    P('6. PARTE DETERMINÍSTICA (sem modelo)')
    for ano in (2026, 2022, 2018, 2014):
        r, HL, HR, SL, SR = deterministica(U[ano])
        rl, HLa, HRa, _, _ = deterministica(B[ano])
        r['rede_larga_todas_as_secoes'] = {k: rl[k] for k in ('n', 'H_L', 'H_R', 'H_L_aptos_max', 'H_R_aptos_max', 'S_L', 'S_R', 'assimetria_S')}
        if ano == 2026:
            r['casos_H_L_universo'] = [{'chave': U[ano]['chave'][i], 'H': int(HL[i]), 'L1': int(U[ano]['L1'][i]), 'R1': int(U[ano]['R1'][i]), 'L2': int(U[ano]['L2'][i]), 'R2': int(U[ano]['R2'][i]),
                                        'apt1': int(U[ano]['apt1'][i]), 'apt2': int(U[ano]['apt2'][i]), 'comp1': int(U[ano]['comp1'][i]), 'comp2': int(U[ano]['comp2'][i])} for i in np.where(HL > 0)[0][:200]]
            r['casos_H_R_universo'] = [{'chave': U[ano]['chave'][i], 'H': int(HR[i]), 'L1': int(U[ano]['L1'][i]), 'R1': int(U[ano]['R1'][i]), 'L2': int(U[ano]['L2'][i]), 'R2': int(U[ano]['R2'][i]),
                                        'apt1': int(U[ano]['apt1'][i]), 'apt2': int(U[ano]['apt2'][i]), 'comp1': int(U[ano]['comp1'][i]), 'comp2': int(U[ano]['comp2'][i])} for i in np.where(HR > 0)[0][:200]]
            bb = B[ano]
            r['casos_H_rede_larga'] = [{'chave': bb['chave'][i], 'lado': 'L' if HLa[i] > 0 else 'R', 'H_L': int(HLa[i]), 'H_R': int(HRa[i]), 'L1': int(bb['L1'][i]), 'R1': int(bb['R1'][i]), 'L2': int(bb['L2'][i]), 'R2': int(bb['R2'][i]),
                                        'apt1': int(bb['apt1'][i]), 'apt2': int(bb['apt2'][i]), 'comp1': int(bb['comp1'][i]), 'comp2': int(bb['comp2'][i]), 'no_universo': bool(bb['univ'][i])} for i in np.where((HLa > 0) | (HRa > 0))[0][:400]]
            # as 20 maiores de S de cada lado, para auditoria
            for nome, v in (('maiores_S_L', SL), ('maiores_S_R', SR)):
                o = np.argsort(-v)[:20]
                r[nome] = [{'chave': U[ano]['chave'][i], 'S': int(v[i]), 'L1': int(U[ano]['L1'][i]), 'R1': int(U[ano]['R1'][i]), 'L2': int(U[ano]['L2'][i]), 'R2': int(U[ano]['R2'][i]),
                            'comp1': int(U[ano]['comp1'][i]), 'comp2': int(U[ano]['comp2'][i])} for i in o]
        S['deterministica'][str(ano)] = r
        P(f"  {ano}: H de L positivo em {r['H_L']['secoes']} seções (soma {r['H_L']['soma']}); H de R positivo em {r['H_R']['secoes']} (soma {r['H_R']['soma']}); "
          f"S de L positivo em {r['S_L']['secoes']} seções, soma {r['S_L']['soma']:,}; S de R positivo em {r['S_R']['secoes']} seções, soma {r['S_R']['soma']:,}; assimetria L menos R = {r['assimetria_S']:+,}".replace(',', '.'))
        P(f"        rede larga (todas as {rl['n']} seções com dois turnos): H de L em {rl['H_L']['secoes']}, H de R em {rl['H_R']['secoes']}; com o maior dos aptos: {rl['H_L_aptos_max']['secoes']} e {rl['H_R_aptos_max']['secoes']}.")
    P(f"  Em 2026, as fontes que não são voto de Flávio passam de 6% do comparecimento em {100*S['deterministica']['2026']['parcela_secoes_fontes_acima_6pct']:.1f}% das seções (mediana {100*S['deterministica']['2026']['fontes_sobre_comparecimento_mediana']:.1f}%).")

    # ---------- calibração por efeito plantado
    S['plantio'] = {}
    P('')
    P('7. CALIBRAÇÃO POR EFEITO PLANTADO (troca binomial de R para L no 2º turno; recuperação = subida de As / fração plantada)')
    cen = 0
    for ano in (2026, 2022, 2018, 2014):
        u = U[ano]
        ajs = [('d', AJ[ano])] + ([('principal', aj26)] if ano == 2026 else [])
        for p in P_PLANTIO:
            for modo in ('uniforme', 'concentrado30'):
                cen += 1
                rng = np.random.default_rng(SEMENTE + cen)
                L2p, R2p, nvot = plantar(u, p, modo, rng)
                Yp = y_plantado(u, L2p, R2p)
                e = {'ano': ano, 'p': p, 'modo': modo, 'votos_trocados_no_universo': nvot}
                for nome, aj in ajs:
                    bt = aj.novo_y(Yp)
                    e[f'As_{nome}'] = as_de(bt, aj); e[f'subida_As_{nome}'] = as_de(bt, aj) - as_de(aj.beta, aj)
                    e[f'recuperacao_{nome}'] = e[f'subida_As_{nome}'] / p
                    e[f'V_{nome}'] = float(bt[aj.ix['R1'], aj.iy['L2']]); e[f'M_{nome}'] = float(bt[aj.ix['L1'], aj.iy['R2']])
                    e[f'subida_assim_retencao_{nome}'] = ret_de(bt, aj) - ret_de(aj.beta, aj)
                S['plantio'][f'{ano}_{p}_{modo}'] = e
                ch = 'principal' if ano == 2026 else 'd'
                P(f"  {ano} p={100*p:.2f}% {modo:13s}: As {as_de(ajs[-1][1].beta, ajs[-1][1]):+.4f} -> {e['As_'+ch]:+.4f}; subida {e['subida_As_'+ch]:+.4f}; recuperação {e['recuperacao_'+ch]:.3f}; "
                      f"V {e['V_'+ch]:+.4f} M {e['M_'+ch]:+.4f}; assimetria de retenção sobe {e['subida_assim_retencao_'+ch]:+.4f}")
    # dispersão do plantio principal (20 sorteios) e espelho
    sub20 = []
    for i in range(20):
        rng = np.random.default_rng(SEMENTE + 1000 + i)
        L2p, R2p, _ = plantar(u26, 0.0357, 'uniforme', rng)
        sub20.append(as_de(aj26.novo_y(y_plantado(u26, L2p, R2p)), aj26) - r26['As'])
    S['plantio']['2026_0.0357_uniforme_20_sorteios'] = {'media_subida': float(np.mean(sub20)), 'dp': float(np.std(sub20, ddof=1)), 'min': float(min(sub20)), 'max': float(max(sub20))}
    kappa = S['plantio']['2026_0.0357_uniforme']['recuperacao_principal']
    S['kappa'] = kappa
    esp = {}
    for j, p in enumerate(P_PLANTIO):
        rng = np.random.default_rng(SEMENTE + 2000 + j)
        L2p, R2p, nvot = plantar(u26, p, 'uniforme', rng, de='L')
        bt = aj26.novo_y(y_plantado(u26, L2p, R2p))
        esp[str(p)] = {'As': as_de(bt, aj26), 'subida_As': as_de(bt, aj26) - r26['As'], 'recuperacao_espelho': (as_de(bt, aj26) - r26['As']) / (-p), 'votos': nvot,
                       'V': float(bt[aj26.ix['R1'], aj26.iy['L2']]), 'M': float(bt[aj26.ix['L1'], aj26.iy['R2']])}
    S['plantio']['espelho_2026_de_L_para_R'] = esp
    P(f"  20 sorteios do plantio de 3,57% uniforme em 2026: subida média {np.mean(sub20):+.5f}, desvio {np.std(sub20, ddof=1):.5f}.")
    P('  Espelho da calibração (troca plantada de L para R em 2026): ' + '; '.join(f"p={100*float(p):.2f}%: As {v['As']:+.4f}, variação {v['subida_As']:+.4f}" for p, v in esp.items()))
    # plantio nos redutos e na parte determinística
    rng = np.random.default_rng(SEMENTE + 3000)
    L2p, R2p, nv = plantar(u26, 0.0357, 'uniforme', rng)
    redp = redutos(u26, ref26, L2p, R2p, boot=False)
    detp = deterministica(u26, L2p, R2p)[0]
    rng = np.random.default_rng(SEMENTE + 3001)
    L2c, R2c, nvc = plantar(u26, 0.0357, 'concentrado30', rng)
    detc = deterministica(u26, L2c, R2c)[0]
    redc = redutos(u26, ref26, L2c, R2c, boot=False)
    S['plantio']['redutos_2026_3.57'] = {'uniforme': {'dif': redp['dif_L_menos_R'], 'subida': redp['dif_L_menos_R'] - RED[2026]['dif_L_menos_R'], 'intercepto_L': redp['L']['intercepto'], 'intercepto_R': redp['R']['intercepto']},
                                         'concentrado30': {'dif': redc['dif_L_menos_R'], 'subida': redc['dif_L_menos_R'] - RED[2026]['dif_L_menos_R']}}
    d0 = S['deterministica']['2026']
    S['plantio']['deterministica_2026_3.57'] = {
        'uniforme': {'votos': nv, 'H_L': detp['H_L'], 'S_L': detp['S_L'], 'S_R': detp['S_R'], 'assimetria_S': detp['assimetria_S'], 'subida_assimetria': detp['assimetria_S'] - d0['assimetria_S']},
        'concentrado30': {'votos': nvc, 'H_L': detc['H_L'], 'S_L': detc['S_L'], 'S_R': detc['S_R'], 'assimetria_S': detc['assimetria_S'], 'subida_assimetria': detc['assimetria_S'] - d0['assimetria_S']}}
    # plantio nos anos placebo, parte determinística
    for ano in (2022, 2018, 2014):
        rng = np.random.default_rng(SEMENTE + 3100 + ano)
        L2p_, R2p_, nv_ = plantar(U[ano], 0.0357, 'uniforme', rng)
        dp_ = deterministica(U[ano], L2p_, R2p_)[0]
        S['plantio'][f'deterministica_{ano}_3.57_uniforme'] = {'votos': nv_, 'assimetria_S': dp_['assimetria_S'], 'subida_assimetria': dp_['assimetria_S'] - S['deterministica'][str(ano)]['assimetria_S'], 'H_L': dp_['H_L']}
    P(f"  Redutos, plantio de 3,57% uniforme em 2026: diferença dos interceptos {RED[2026]['dif_L_menos_R']:+.4f} -> {redp['dif_L_menos_R']:+.4f} (subida {redp['dif_L_menos_R'] - RED[2026]['dif_L_menos_R']:+.4f}).")
    P(f"  Parte determinística, plantio de 3,57% em 2026 ({nv:,} votos): assimetria de S {d0['assimetria_S']:+,} -> {detp['assimetria_S']:+,} (uniforme) e {detc['assimetria_S']:+,} (concentrado em 30%); H de L positivo passa a {detp['H_L']['secoes']} e {detc['H_L']['secoes']} seções.".replace(',', '.'))

    # ---------- placebo de governador
    S['governador'] = governador(B[2026], NX_P, P)

    # ---------- tradução em votos
    def votos(a):
        p = a / kappa
        return p / (1 - p) * R2_OFICIAL
    v_as = votos(r26['As']); v_lo = votos(r26['ic95_As'][0]); v_hi = votos(r26['ic95_As'][1])
    direto = r26['V'] * nac['R1'] - r26['M'] * nac['L1']
    S['traducao_em_votos'] = {'kappa': kappa, 'fracao_estimada_do_voto_de_flavio': r26['As'] / kappa,
                              'votos_trocados_equivalentes': v_as, 'ic95_votos': [v_lo, v_hi],
                              'efeito_na_margem': 2 * v_as, 'ic95_efeito_na_margem': [2 * v_lo, 2 * v_hi],
                              'parcela_do_necessario': v_as / NECESSARIO, 'margem_oficial': MARGEM, 'necessario_para_virar': NECESSARIO,
                              'conta_direta_V_estoqueR_menos_M_estoqueL': float(direto), 'V_vezes_estoque_R1': float(r26['V'] * nac['R1']), 'M_vezes_estoque_L1': float(r26['M'] * nac['L1']),
                              'limite_superior_ic95_exclui_troca_acima_de_votos': v_hi}
    P('')
    P('9. TRADUÇÃO EM VOTOS DE MARGEM')
    P(f"  As de 2026 = {r26['As']:+.4f}, IC95 {ic(r26['ic95_As'])}. Com kappa = {kappa:.3f} (recuperação medida no plantio), isso equivale a uma troca de "
      f"{100*r26['As']/kappa:+.2f}% do voto de Flávio: {v_as:+,.0f} votos (IC95 de {v_lo:+,.0f} a {v_hi:+,.0f}), efeito de {2*v_as:+,.0f} na margem.".replace(',', '.'))
    P(f"  Para virar o resultado seriam precisos {NECESSARIO:,} votos trocados (margem oficial {MARGEM:,}). O ponto estimado é {100*v_as/NECESSARIO:+.1f}% disso; o limite superior do intervalo, {100*v_hi/NECESSARIO:+.1f}%.".replace(',', '.'))
    P(f"  Conta direta: V x estoque de R1 = {r26['V']*nac['R1']:+,.0f}; M x estoque de L1 = {r26['M']*nac['L1']:+,.0f}; líquido = {direto:+,.0f} votos.".replace(',', '.'))

    # ---------- veredito pela letra
    S['veredito'] = veredito(S, RED)
    P('')
    P('10. VEREDITO PELA LETRA DO REGISTRO')
    for k, v in S['veredito']['clausulas_sinal'].items():
        P(f"  sinal: {k}: {'SIM' if v['vale'] else 'NÃO'} ({v['valor']})")
    for k, v in S['veredito']['clausulas_sem_sinal'].items():
        P(f"  sem sinal: {k}: {'SIM' if v['vale'] else 'NÃO'} ({v['valor']})")
    for k, v in S['veredito']['clausulas_inconclusivo'].items():
        P(f"  inconclusivo: {k}: {'SIM' if v['vale'] else 'NÃO'} ({v['valor']})")
    P(f"  REGRESSÃO: {S['veredito']['regressao']}")
    P(f"  DETERMINÍSTICA: {S['veredito']['deterministica']}")
    S['tempo_s'] = round(time.time() - t0)
    return S, T


def governador(b, NX_P, P):
    """Placebo contemporâneo: governador nas 6 UFs com 2º turno (L = vencedor do 2º turno na UF)."""
    g1 = carregar(f'{RAIZ}/dados/candidatos_gov_2026_1t_6ufs.json.gz')['secoes']
    with gzip.open(TRAB + '/gov2t_6ufs.json.gz', 'rt') as f:
        g2 = json.load(f)
    d = carregar(f'{RAIZ}/dados/secoes2026.json.gz')
    out = {'por_uf': {}}
    P('')
    P('8. PLACEBO CONTEMPORÂNEO: GOVERNADOR NAS 6 UFs COM 2º TURNO (L = vencedor do 2º turno na UF; R = o outro finalista)')
    conj = []
    for iu, uf in enumerate(UFS_GOV):
        m = b['univ'] & (b['uf'] == uf)
        ch = b['chave'][m].tolist()
        tem = np.array([(k in g1) and (k in g2) and ('1g' in d[k]) and ('2g' in d[k]) for k in ch])
        # finalistas e eliminados, pelos totais da UF (todas as seções da UF)
        t2 = {}; t1 = {}
        for k, v in g2.items():
            if k.startswith(uf + '|'):
                for num, q in v['nom'].items():
                    t2[num] = t2.get(num, 0) + q
        for k, v in g1.items():
            if k.startswith(uf + '|'):
                for num, q in v.items():
                    t1[num] = t1.get(num, 0) + q
        fin = sorted(t2, key=lambda x: -t2[x])
        assert len(fin) == 2, (uf, t2)
        Lg, Rg = fin[0], fin[1]
        val1 = sum(t1.values())
        el = sorted([x for x in t1 if x not in fin and t1[x] / val1 >= 0.005], key=lambda x: -t1[x])
        s = sub(b, m); s = sub(s, tem); ch = s['chave'].tolist()
        n = len(ch)
        gv = {'L1': np.array([g1[k].get(Lg, 0) for k in ch]), 'R1': np.array([g1[k].get(Rg, 0) for k in ch]),
              'B1': np.array([d[k]['1g']['B'] for k in ch]), 'N1': np.array([d[k]['1g']['N'] for k in ch]),
              'L2': np.array([g2[k]['nom'].get(Lg, 0) for k in ch]), 'R2': np.array([g2[k]['nom'].get(Rg, 0) for k in ch]),
              'BN2': np.array([g2[k]['B'] + g2[k]['N'] for k in ch])}
        for x in el:
            gv['E' + x] = np.array([g1[k].get(x, 0) for k in ch])
        gv['O1'] = np.array([sum(q for num, q in g1[k].items() if num not in fin) for k in ch])
        gv['Edem'] = gv['O1'] - sum(gv['E' + x] for x in el) if el else gv['O1'].copy()
        # conferências de contabilidade
        conf = {'identidade_1t_falhas': int((gv['L1'] + gv['R1'] + gv['O1'] + gv['B1'] + gv['N1'] != s['comp1']).sum()),
                'identidade_2t_falhas': int((gv['L2'] + gv['R2'] + gv['BN2'] != s['comp2']).sum()),
                'bn2_difere_da_base': int(sum(1 for i, k in enumerate(ch) if g2[k]['B'] != d[k]['2g']['B'] or g2[k]['N'] != d[k]['2g']['N'])),
                'votos_fora_de_nominal_branco_nulo_2t': int(sum(g2[k]['outros'] for k in ch))}
        sg = dict(s); sg.update(gv)
        nx = ['L1', 'R1'] + ['E' + x for x in el] + (['Edem'] if gv['Edem'].sum() > 0 else []) + ['B1', 'N1', 'A1']
        _, rg = regressao(sg, nx, dentro_de_uf=True, semente=SEMENTE + 500 + iu)
        _, rgd = regressao(sg, ['L1', 'R1', 'O1', 'B1', 'N1', 'A1'], dentro_de_uf=True, boot=False)
        _, rp = regressao(s, NX_P, dentro_de_uf=True, semente=SEMENTE + 600 + iu)
        out['por_uf'][uf] = {'L_vencedor': Lg, 'R_outro': Rg, 'totais_2t': {Lg: t2[Lg], Rg: t2[Rg]}, 'totais_1t_finalistas': {Lg: t1.get(Lg, 0), Rg: t1.get(Rg, 0)},
                             'eliminados_com_termo': el, 'n_secoes': n, 'conferencias': conf,
                             'governador': {k: rg[k] for k in ('n', 'grupos_erro', 'V', 'ep_V', 'M', 'ep_M', 'As', 'ep_As', 'ic95_As', 'ret_L', 'ret_R', 'assim_retencao', 'ep_assim_retencao')},
                             'governador_d': {k: rgd[k] for k in ('V', 'M', 'As', 'ep_As', 'assim_retencao')},
                             'presidente_mesmas_secoes': {k: rp[k] for k in ('n', 'V', 'ep_V', 'M', 'ep_M', 'As', 'ep_As', 'ic95_As', 'assim_retencao', 'ep_assim_retencao')}}
        P(f"  {uf} (L={Lg}, R={Rg}; 1º turno {t1.get(Lg,0):,} e {t1.get(Rg,0):,}; 2º turno {t2[Lg]:,} e {t2[Rg]:,}): governador As={rg['As']:+.4f} ({rg['ep_As']:.4f}) IC95 {ic(rg['ic95_As'])} V={rg['V']:+.4f} M={rg['M']:+.4f} dif. retenção {rg['assim_retencao']:+.4f} | presidente nas mesmas seções As={rp['As']:+.4f} ({rp['ep_As']:.4f}) n={n}".replace(',', '.'))
        conj.append(sg)
    # conjunta: eliminados somados
    cj = {k: np.concatenate([x[k] for x in conj]) for k in ('L1', 'R1', 'O1', 'B1', 'N1', 'A1', 'L2', 'R2', 'BN2', 'A2', 'apt1', 'loc', 'mun', 'zona', 'uf')}
    _, rj = regressao(cj, ['L1', 'R1', 'O1', 'B1', 'N1', 'A1'], dentro_de_uf=True, semente=SEMENTE + 700)
    pj = {k: np.concatenate([b[k][b['univ'] & (b['uf'] == uf)] for uf in UFS_GOV]) for k in list(NX_P) + NY + ['apt1', 'loc', 'mun', 'zona', 'uf', 'O1']}
    _, rpj = regressao(pj, NX_P, dentro_de_uf=True, semente=SEMENTE + 701)
    out['conjunta_governador_d'] = {k: rj[k] for k in ('n', 'grupos_erro', 'V', 'ep_V', 'M', 'ep_M', 'As', 'ep_As', 'ic95_As', 'ret_L', 'ret_R', 'assim_retencao', 'ep_assim_retencao')}
    out['conjunta_presidente_mesmas_ufs'] = {k: rpj[k] for k in ('n', 'grupos_erro', 'V', 'ep_V', 'M', 'ep_M', 'As', 'ep_As', 'ic95_As', 'ret_L', 'ret_R', 'assim_retencao', 'ep_assim_retencao')}
    out['maior_abs_As_governador'] = float(max(abs(v['governador']['As']) for v in out['por_uf'].values()))
    P(f"  Conjunta das 6 UFs, governador (eliminados somados): As={rj['As']:+.4f} ({rj['ep_As']:.4f}) IC95 {ic(rj['ic95_As'])}; presidente nas mesmas UFs: As={rpj['As']:+.4f} ({rpj['ep_As']:.4f}) IC95 {ic(rpj['ic95_As'])}.")
    P(f"  Maior valor absoluto de As de governador entre as 6 UFs: {out['maior_abs_As_governador']:.4f}.")
    return out


def veredito(S, RED):
    r = S['principal_2026']; As = r['As']; hi = r['ic95_As'][1]
    pl = {a: S[f'placebo_{a}_d']['As'] for a in (2014, 2018, 2022)}
    mx = max(abs(v) for v in pl.values())
    vb, vc, vd = S['variante_b_fe_municipio']['As'], S['variante_c_perfil']['As'], S['variante_d_eliminados_somados']['As']
    ret = r['assim_retencao']; retred = RED[2026]['dif_L_menos_R']
    sub26 = S['plantio']['2026_0.0357_uniforme']['subida_As_principal']
    subpl = {a: S['plantio'][f'{a}_0.0357_uniforme']['subida_As_d'] for a in (2014, 2018, 2022)}
    cs = {
        'As de 2026 >= 0,025': {'vale': As >= 0.025, 'valor': f'{As:+.4f}'},
        'As de 2026 >= 0,015 + maior |As| placebo': {'vale': As >= 0.015 + mx, 'valor': f'{As:+.4f} contra {0.015 + mx:.4f} (2014 {pl[2014]:+.4f}, 2018 {pl[2018]:+.4f}, 2022 {pl[2022]:+.4f})'},
        'As >= 0,015 nas variantes (b), (c) e (d)': {'vale': min(vb, vc, vd) >= 0.015, 'valor': f'(b) {vb:+.4f}, (c) {vc:+.4f}, (d) {vd:+.4f}'},
        'As >= 0,010 em 20 ou mais das 27 UFs': {'vale': S['ufs_com_As_ge_0010'] >= 20, 'valor': f"{S['ufs_com_As_ge_0010']} UFs"},
        'assimetria de retenção >= 0,020 na regressão geral': {'vale': ret >= 0.020, 'valor': f'{ret:+.4f}'},
        'assimetria de retenção >= 0,020 nos redutos': {'vale': retred >= 0.020, 'valor': f'{retred:+.4f}'}}
    css = {
        '|As| de 2026 <= 0,010': {'vale': abs(As) <= 0.010, 'valor': f'{As:+.4f}'},
        'limite superior do IC95 <= 0,015': {'vale': hi <= 0.015, 'valor': f'{hi:+.4f}'},
        '|As| <= 0,010 nos três anos placebo': {'vale': mx <= 0.010, 'valor': f'maior |As| = {mx:.4f}'},
        'plantio de 3,57% recuperado (subida >= 0,025) em cada ano placebo': {'vale': min(subpl.values()) >= 0.025, 'valor': ', '.join(f'{a} {v:+.4f}' for a, v in subpl.items())}}
    sinais = [np.sign(x) for x in (As, vb, vc, vd)]
    rec = sub26 / 0.0357
    ci = {
        'As entre 0,010 e 0,025': {'vale': 0.010 < As < 0.025, 'valor': f'{As:+.4f}'},
        'algum ano placebo com |As| acima de 0,015': {'vale': mx > 0.015, 'valor': f'maior |As| = {mx:.4f}'},
        'variantes com sinais opostos': {'vale': len(set(sinais)) > 1, 'valor': f'principal {As:+.4f}, (b) {vb:+.4f}, (c) {vc:+.4f}, (d) {vd:+.4f}'},
        'plantio recuperado em menos de 70%': {'vale': rec < 0.70 or min(subpl.values()) / 0.0357 < 0.70, 'valor': f'2026 {rec:.3f}; placebo ' + ', '.join(f'{a} {v/0.0357:.3f}' for a, v in subpl.items())}}
    if sub26 < 0.025:
        reg = 'SEM PODER'
    elif all(v['vale'] for v in cs.values()):
        reg = 'SINAL'
    elif all(v['vale'] for v in css.values()) and not any(v['vale'] for v in ci.values()):
        reg = 'SEM SINAL'
    else:
        reg = 'INCONCLUSIVO'
    d = S['deterministica']
    a26 = d['2026']['assimetria_S']; mxa = max(abs(d[str(a)]['assimetria_S']) for a in (2014, 2018, 2022))
    nH = d['2026']['H_L']['secoes']
    exc = a26 >= 220000 and a26 >= 3 * mxa
    subdet = S['plantio']['deterministica_2026_3.57']['uniforme']['subida_assimetria']
    partes = []
    partes.append(f"H: {nH} seções com H de Lula positivo no universo" + (' (casos individuais para auditoria: SINAL pontual)' if nH > 0 else ' (SEM SINAL)'))
    partes.append(f"S: assimetria de 2026 = {a26:+d}; maior assimetria placebo em valor absoluto = {mxa}; critério (>= 220.000 e >= 3 vezes) {'ATENDIDO: SINAL de excesso concentrado' if exc else 'não atendido: SEM SINAL de excesso concentrado'}")
    partes.append(f"plantio de 3,57% move a assimetria de S em {subdet:+d} votos: " + ('a parte determinística enxerga a troca espalhada' if subdet >= 220000 else 'SEM PODER para troca espalhada'))
    return {'clausulas_sinal': cs, 'clausulas_sem_sinal': css, 'clausulas_inconclusivo': ci, 'regressao': reg,
            'deterministica': '; '.join(partes), 'deterministica_H_secoes': nH, 'deterministica_excesso_concentrado': bool(exc),
            'deterministica_subida_com_plantio': int(subdet)}


if __name__ == '__main__':
    os.makedirs(TRAB, exist_ok=True)
    modo = sys.argv[1] if len(sys.argv) > 1 else 'rodar'
    if modo == 'perfil':
        extrair_perfil()
    elif modo == 'gov2t':
        extrair_gov2t()
    else:
        S, T = main()
        with open(RAIZ + '/resultados/R27_A2_assimetria_vazamento.json', 'w') as f:
            json.dump(S, f, ensure_ascii=False, indent=1, default=lambda o: o.item() if hasattr(o, 'item') else str(o))
        with open(RAIZ + '/resultados/R27_A2_assimetria_vazamento.txt', 'w') as f:
            f.write('\n'.join(T) + '\n')
