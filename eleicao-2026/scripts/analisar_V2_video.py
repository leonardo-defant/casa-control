"""V2 do pré-registro (Adendo 25, commit 587cc65, 07/11/2026 12:10:37 UTC): checagem do vídeo "10 votos extras para
Lula por urna". Marca de "k votos fixos por urna" nos dados por seção (bweb inteiro).

Letra do registro (V2)
  - Literal: com 10 votos a mais para Lula em toda urna, toda seção teria pelo menos 10 votos de Lula no 2º turno.
    Contar seções com L2 abaixo de 10 e os votos de Lula que elas somam.
  - Dose pelo tamanho: um acréscimo fixo de k votos muda a fatia de Lula entre os finalistas em cerca de k x c / N
    (N = L2 + R2; c entre 0,5, se o voto é acrescentado, e 1, se é trocado de Flávio para Lula). Regressão dentro do
    local: virada (fatia do 2º menos a do 1º turno, em fração) contra 1/N, efeito fixo de local, peso N, erro agrupado
    por local. O coeficiente b fica em votos por urna: a afirmação prevê b de 5 a 10; sem acréscimo fixo, perto de zero.
  - Comparecimento: regressão dentro do local da variação da taxa de comparecimento (2º menos 1º turno) contra
    1/aptos; um acréscimo de k eleitores por urna daria coeficiente perto de k.
  - Faixas de tamanho (N até 50, 51 a 100, 101 a 200, 201 a 300, mais de 300): virada menos a média do local, por faixa.
  - Placebos, lado a lado, com a mesma especificação: 2022 (Lula e Bolsonaro, 1º para 2º turno) e 2018 (Haddad e
    Bolsonaro); nível do 1º turno de 2026 contra 1/N do 1º turno.
  - Sinal: b de 2,5 ou mais (metade do menor valor previsto) a mais de 4 erros-padrão. Sem sinal: b + 2 erros-padrão
    abaixo de 2,5. Entre os dois: inconclusivo. Os placebos e a regressão do comparecimento são relatados ao lado e não
    mudam o veredito.

Decisões que o registro não fixa (escritas aqui antes de calcular qualquer número do V2; relatadas como desvios)
  D1. Dados: base por seção trab2t/secoes2026.json.gz (bweb inteiro dos dois turnos, cargo 1, montada por
      extrair_bweb.py: L = 13 Lula, R = 22 Flávio, O = demais nominais, B = branco, N = nulo; loc, urna, tipo, apt,
      comp, agr). O C1 já conferiu a base contra o bweb (comparecimento, aptos, local, votos de 13 e 22). Aqui o modo
      "conferir" relê os zips do bweb dos dois turnos (filtro por bytes ';"Presidente";' e CD_CARGO_PERGUNTA = 1) e
      confere, por seção e turno, local, urna, tipo, aptos, comparecimento, agregação, L, R, O, B e N; discordâncias são
      contadas e relatadas. As contas usam a base.
  D2. Exterior: chaves com UF "ZZ" (1.309 seções no 1º turno, 1.308 no 2º), fora de todos os itens, como nas 497.897
      urnas do vídeo. Universo U: seções das 27 UFs presentes nos dois turnos na base (todas "Apurada" nos dois turnos).
      Nas regressões: também L+R > 0 em cada turno usado e aptos > 0 nos dois turnos (no comparecimento).
  D3. Item literal: L2 < 10 (votos de Lula no 2º turno) nas seções das 27 UFs com 2º turno. Relatados: seções,
      soma de L2 nelas, seções com L2 = 0, distribuição de L2 de 0 a 9, e por UF (seções da UF, seções com L2 < 10,
      votos de Lula nelas). Ao lado, das seções com L2 < 10: quantas têm comparecimento do 2º turno abaixo de 10, quantas
      são agregadas, soma de L1 nelas. Descritivo: L2 - L1 < 10 (seções, soma de L2 - L1 nelas, por UF) e, ao lado,
      L2 - L1 < 0.
  D4. Item 2 (dose, regressão principal, a única que decide): y = L2/(L2+R2) - L1/(L1+R1), em fração; x = 1/N2 com
      N2 = L2 + R2; efeito fixo de local do 2º turno, lib.chave_local(chave, seção do 2º turno) = UF|município|zona|
      NR_LOCAL_VOTACAO; peso N2; erro agrupado por local (lib.fe_ols, CR1; locais com uma seção só saem, como no lib).
      b = coeficiente de x, em votos por urna. Relatados: b, ep, z = b/ep, seções usadas, locais (grupos), seções em
      locais de uma seção só (que saem).
  D5. Robustez da dose (fora do critério, não muda o veredito; fixada aqui antes): (a) x = 1/apt2 (aptos do 2º turno);
      (b) sem peso; (c) efeito fixo de município (UF|município), com erro agrupado por município (lib.fe_ols agrupa no
      mesmo grupo do efeito fixo); (d) só seções com a mesma urna (NR_URNA_EFETIVADA igual) e apuradas ("Apurada") nos
      dois turnos; (e) sem seções agregadas (campo agr, isto é DS_SECOES_AGREGADAS diferente de #NULO#, em qualquer dos
      dois turnos). Acrescentados aqui, também antes: (f) d e e juntos; (g) x = 1/N1 (tamanho do 1º turno, que não
      contém um acréscimo feito no 2º; x = 1/N2 tem o resultado do 2º turno no denominador).
  D6. Leitura de b: com acréscimo de k votos a Lula, a fatia do 2º turno é exatamente s + k(1 - s)/N2 (s = fatia sem o
      acréscimo), logo b = k(1 - s); com troca de k votos de Flávio para Lula, s + k/N2, b = k. A afirmação (k = 10)
      prevê b entre 10(1 - s_bar) e 10, s_bar = fatia de Lula entre os finalistas no 2º turno nas 27 UFs (o registro
      arredonda para 5 a 10).
  D7. Calibração (fora do critério, fixada antes): plantar em toda seção de U k = 10 e k = 1 votos, (i) acrescentados a
      L2 e (ii) trocados de R2 para L2 (até R2), e refazer a regressão principal; relatar b plantado menos b real contra
      o previsto (k vezes 1 - s_bar no acréscimo; k na troca).
  D8. Item 3 (comparecimento): y = comp2/apt2 - comp1/apt1 (fração); x = 1/apt2; efeito fixo de local do 2º turno, peso
      apt2, erro agrupado por local; U com apt1 > 0 e apt2 > 0. Ao lado, fixado antes: o mesmo só nas seções com aptos
      iguais nos dois turnos, mesma urna e sem agregação (os aptos mudam entre os turnos em parte das seções).
  D9. Item 4 (faixas de N2 = L2 + R2: até 50; 51 a 100; 101 a 200; 201 a 300; mais de 300): d = y da seção menos a
      média de y das outras seções do mesmo local do 2º turno, ponderada por N2 (sem a própria seção); seções sozinhas no
      local saem e são contadas. Por faixa: seções, média simples de d (cada urna pesa 1) com erro-padrão agrupado por
      local (CR1, d contra as indicadoras das faixas, sem constante e sem efeito fixo); ao lado, média ponderada por N2
      com o mesmo erro. Em pontos (100 d). Ao lado, o previsto pela afirmação na faixa: 10 c vezes a média de
      (1/N2 da seção menos a média de 1/N2 das outras seções do local, ponderada por N2), com c = 1 - s_bar e c = 1.
  D10. Item 5 (placebos), especificação do D4 (y, x = 1/N2, efeito fixo de local do 2º turno, peso N2, erro agrupado):
      2022 (dados_ref/secoes2022.json.gz; L = Lula 13, R = Bolsonaro 22) e 2018 (dados_ref/secoes2018.json.gz;
      L = Haddad 13, R = Bolsonaro 17; conferido em analisar_T29.py e analisar_T28.py e nos totais da base: 2º turno de
      2018 com L 47.040.906 e R 57.797.847). Universo: 27 UFs (sem ZZ), seções com os dois turnos e L+R > 0 nos dois,
      sem filtro de tipo (como no principal). Nível de 2026: y = L1/(L1+R1), x = 1/N1, efeito fixo de local do 1º turno
      (chave_local com a seção do 1º turno), peso N1, erro agrupado; seções das 27 UFs com 1º turno e N1 > 0.
      Ao lado, fixado antes: nível do 2º turno de 2026 (y = L2/N2 contra 1/N2, efeito fixo de local do 2º turno).
  D11. Item 6 (veredito, só com o D4): SINAL se b >= 2,5 e b/ep > 4; SEM SINAL se b + 2 ep < 2,5; senão INCONCLUSIVO.
  D12. Item 7 (votos): um efeito fixo por urna de tamanho b equivale, na troca, a k = b votos de Flávio para Lula por
      urna (margem 2b por urna) e, no acréscimo, a k = b/(1 - s_bar) votos novos para Lula (margem k por urna). No país,
      vezes o número de seções de U (as "urnas" do vídeo), com b, b - 2 ep e b + 2 ep; comparado com 4.978.970
      (10 x 497.897) e com a margem de Lula no 2º turno nas 27 UFs (soma de L2 - R2 em U).
  D13. Formato: contagens exatas; coeficientes com 3 casas e ep; pontos com 2 casas. O que for acrescentado depois de
      ver o resultado vai numa seção marcada "exploratório" e não muda o veredito.

Exploratório (acrescentado DEPOIS de ver o resultado pela letra, em 07/11/2026; sem veredito, não muda nada acima).
Motivo: b principal de 2026 saiu positivo (+0,951, ep 0,068) e os placebos de 2022 e 2018 saíram negativos (perto de
-1); a pergunta é se essa diferença entre anos é estável ou depende da especificação.
  E1. Placebos 2022 e 2018 com as mesmas variantes do D5 (a, b, c, f, g) e a regressão do comparecimento do D8 em 2022 e
      2018 (mesma especificação).
  E2. Calibração do D7 (k = 10, acréscimo e troca) refeita em cada variante, para mostrar quanto um efeito fixo real
      por urna mudaria cada uma. No acréscimo, k entra também no comparecimento do 2º turno (só pesa no E5).
  E3. Covariável: fatia dos outros candidatos no 1º turno, O1/(L1+R1+O1), ao lado de 1/N2, nos três anos (a terceira
      via some no 2º turno e sua fatia varia entre seções do mesmo local).
  E4. Diferença do b de 2026 para o b de cada placebo, em cada variante, com ep = raiz(ep26^2 + ep_ref^2) (amostras
      independentes); e o que a diferença da especificação principal valeria em votos pela conta do D12, se fosse toda
      um efeito fixo por urna (leitura extrema, não estimativa).
  E5. Transparência: num protótipo rodado antes de escrever este bloco, também foi rodada a regressão principal com
      cinco regressores (1/N2, fatia dos outros no 1º turno, brancos e nulos sobre comparecimento no 1º turno,
      variação da taxa de comparecimento, log dos aptos do 2º turno), à moda das covariáveis do C1. Ela é relatada aqui
      com a calibração, mas não serve como teste de dose: log dos aptos é outra função do tamanho (o coeficiente de
      1/N2 passa a medir só a curvatura) e a variação do comparecimento é consequência do 2º turno. Fica fora da faixa
      de diferenças do E4.
  E6. Leitura sem conta nova: o b pela fatia do candidato que ganhou terreno no 2º turno (2026 Lula, 2022 Bolsonaro,
      2018 Haddad). Como a fatia de R entre os finalistas é 1 menos a de L, o b de Bolsonaro em 2022 é o de Lula com o
      sinal trocado.

Uso:
  python3 -I analisar_V2_video.py conferir <secoes2026.json.gz> <zips 1T> <zips 2T> <saida.json>
  python3 -I analisar_V2_video.py rodar <secoes2026.json.gz> <secoes2022.json.gz> <secoes2018.json.gz>
          <conferencia.json ou -> <saida.json> <saida.txt>
"""
import os as _os, sys as _sys
_sys.path.insert(0, _os.path.dirname(_os.path.abspath(__file__)))
import collections, csv, glob, gzip, json, os, sys, time, zipfile
from multiprocessing import Pool
import numpy as np
from lib import carregar, chave_local, fe_ols

K_VIDEO = 10
URNAS_VIDEO = 497897
VOTOS_VIDEO = 4978970
LIM_SINAL, Z_SINAL = 2.5, 4.0
FAIXAS = [('ate_50', 1, 50), ('51_100', 51, 100), ('101_200', 101, 200), ('201_300', 201, 300),
          ('mais_300', 301, 10 ** 9)]
NOME_FAIXA = {'ate_50': 'até 50', '51_100': '51 a 100', '101_200': '101 a 200', '201_300': '201 a 300',
              'mais_300': 'mais de 300'}


def log(*a):
    print('#', time.strftime('%H:%M:%S'), *a, file=sys.stderr, flush=True)


# ------------------------------------------------------------------ conferência com o bweb (D1)

def ler_zip(zpath):
    out = {}; incons = 0; linhas = 0
    z = zipfile.ZipFile(zpath)
    nome = [n for n in z.namelist() if n.lower().endswith('.csv')][0]
    with z.open(nome) as fh:
        cab = next(csv.reader([fh.readline().decode('latin1')], delimiter=';'))
        ix = {c.strip().replace('SG_ UF', 'SG_UF'): i for i, c in enumerate(cab)}
        cols = ('SG_UF', 'CD_MUNICIPIO', 'NR_ZONA', 'NR_SECAO', 'NR_LOCAL_VOTACAO', 'NR_URNA_EFETIVADA', 'DS_TIPO_URNA',
                'QT_APTOS', 'QT_COMPARECIMENTO', 'DS_SECOES_AGREGADAS', 'CD_CARGO_PERGUNTA', 'CD_TIPO_VOTAVEL',
                'NR_VOTAVEL', 'QT_VOTOS')
        ic = [ix[c] for c in cols]
        for linha in fh:
            if b';"Presidente";' not in linha:
                continue
            r = next(csv.reader([linha.decode('latin1').rstrip('\r\n')], delimiter=';'))
            uf, mun, zon, sec, loc, urna, tipo, apt, comp, agr, car, tv, nv, qv = (r[i] for i in ic)
            if car != '1':
                continue
            linhas += 1
            k = f'{uf}|{int(mun)}|{int(zon)}|{int(sec)}'
            agr = '' if agr in ('', '#NULO#') else agr
            cabeca = (int(loc), int(urna or 0), tipo, int(apt), int(comp), agr)
            s = out.get(k)
            if s is None:
                s = out[k] = {'cab': cabeca, 'L': 0, 'R': 0, 'O': 0, 'B': 0, 'N': 0}
            elif s['cab'] != cabeca:
                incons += 1
            tv = int(tv); nv = int(nv); q = int(qv)
            if tv == 2: s['B'] += q
            elif tv == 3: s['N'] += q
            elif nv == 13: s['L'] += q
            elif nv == 22: s['R'] += q
            else: s['O'] += q
    return os.path.basename(zpath), out, incons, linhas


def conferir(base_path, pasta1, pasta2, saida):
    base = carregar(base_path)
    res = {}
    with Pool(4) as pool:
        for t, pasta in (('1', pasta1), ('2', pasta2)):
            zs = sorted(glob.glob(os.path.join(pasta, '*.zip')), key=lambda p: -os.path.getsize(p))
            bw = {}; info = {}
            for nome, out, inc, linhas in pool.imap_unordered(ler_zip, zs):
                bw.update(out); info[nome] = {'secoes': len(out), 'linhas_cargo1': linhas, 'linhas_discordantes': inc}
                log('turno', t, nome, len(out))
            disc = collections.Counter(); exemplos = collections.defaultdict(list)
            na_base = {k for k, v in base.items() if t in v}
            so_bweb = [k for k in bw if k not in na_base]
            so_base = [k for k in na_base if k not in bw]
            for k, s in bw.items():
                if k not in na_base:
                    continue
                b = base[k][t]
                loc, urna, tipo, apt, comp, agr = s['cab']
                pares = {'loc': (loc, b['loc']), 'urna': (urna, b['urna']), 'tipo': (tipo, b['tipo']),
                         'apt': (apt, b['apt']), 'comp': (comp, b['comp']), 'agr': (agr, b.get('agr', ''))}
                for c in 'LROBN':
                    pares[c] = (s[c], b[c])
                for c, (u, v) in pares.items():
                    if u != v:
                        disc[c] += 1
                        if len(exemplos[c]) < 3:
                            exemplos[c].append([k, u, v])
            res[t] = {'secoes_bweb': len(bw), 'secoes_base': len(na_base), 'so_no_bweb': len(so_bweb),
                      'so_na_base': len(so_base), 'conferidas': len(bw) - len(so_bweb),
                      'discordancias_por_campo': dict(disc), 'exemplos': dict(exemplos),
                      'linhas_discordantes_na_secao': sum(i['linhas_discordantes'] for i in info.values()),
                      'linhas_cargo1': sum(i['linhas_cargo1'] for i in info.values()), 'arquivos': info}
            del bw
    with open(saida, 'w') as f:
        json.dump(res, f, ensure_ascii=False, indent=1)
    log('conferência gravada', saida)


# ------------------------------------------------------------------ utilidades

def fi(n):
    return f'{int(n):,}'.replace(',', '.')


def fn(x, d=3, sinal=False):
    if x is None or (isinstance(x, float) and not np.isfinite(x)):
        return 'n/d'
    s = f'{x:+,.{d}f}' if sinal else f'{x:,.{d}f}'
    return s.replace(',', '_').replace('.', ',').replace('_', '.')


def ols_cluster(y, X, g, w=None):
    """MQO sem efeito fixo, pesos opcionais, erro agrupado CR1 (para médias por faixa)."""
    y = np.asarray(y, float); X = np.asarray(X, float)
    n, k = X.shape
    w = np.ones(n) if w is None else np.asarray(w, float)
    _, g = np.unique(g, return_inverse=True)
    sw = np.sqrt(w)
    Xw, yw = X * sw[:, None], y * sw
    XtX = Xw.T @ Xw
    b = np.linalg.solve(XtX, Xw.T @ yw)
    e = y - X @ b
    G = g.max() + 1
    S = np.zeros((G, k))
    for j in range(k):
        S[:, j] = np.bincount(g, weights=w * X[:, j] * e, minlength=G)
    inv = np.linalg.inv(XtX)
    c = G / (G - 1) * (n - 1) / (n - k)
    V = c * inv @ (S.T @ S) @ inv
    return b, np.sqrt(np.diag(V)), int(G)


def reg(y, x, grupos, w, nome='x'):
    r = fe_ols(y, x, grupos, w=w, nomes=[nome])
    b, ep = r['coef'][nome], r['ep'][nome]
    _, gi = np.unique(grupos, return_inverse=True)
    cnt = np.bincount(gi)
    return {'b': b, 'ep': ep, 'z': b / ep if ep > 0 else float('nan'), 'n_secoes': r['n'], 'n_locais': r['grupos'],
            'secoes_no_universo': int(len(y)), 'secoes_sozinhas_no_grupo': int((cnt[gi] < 2).sum()),
            'grupos_no_universo': int(len(cnt))}


def arrays_dose(d, excluir='ZZ'):
    """Seções com os dois turnos, fora do exterior, L+R > 0 nos dois turnos."""
    ks = [k for k, v in d.items() if not k.startswith(excluir + '|') and '1' in v and '2' in v
          and v['1']['L'] + v['1']['R'] > 0 and v['2']['L'] + v['2']['R'] > 0]
    A = {}
    for t in '12':
        for c in ('L', 'R', 'O', 'B', 'N', 'apt', 'comp', 'urna'):
            A[c + t] = np.array([d[k][t][c] for k in ks], dtype=np.int64)
        A['tipo' + t] = np.array([d[k][t]['tipo'] for k in ks])
        A['agr' + t] = np.array(['agr' in d[k][t] for k in ks])
        A['loc' + t] = np.array([chave_local(k, d[k][t]) for k in ks])
    A['mun'] = np.array(['|'.join(k.split('|')[:2]) for k in ks])
    A['uf'] = np.array([k.split('|')[0] for k in ks])
    A['chaves'] = ks
    return A


def dose_spec(A, x='N2', peso=True, grupo='loc2', filtro=None, L2=None, R2=None):
    L1, R1 = A['L1'].astype(float), A['R1'].astype(float)
    L2 = A['L2'].astype(float) if L2 is None else L2
    R2 = A['R2'].astype(float) if R2 is None else R2
    N1, N2 = L1 + R1, L2 + R2
    y = L2 / N2 - L1 / N1
    xs = {'N2': 1 / N2, 'apt2': 1 / A['apt2'].astype(float), 'N1': 1 / N1}[x]
    w = N2 if peso else np.ones(len(y))
    g = A[grupo]
    m = np.ones(len(y), bool) if filtro is None else filtro
    return reg(y[m], xs[m], g[m], w[m], nome='inv_' + x)


# ------------------------------------------------------------------ exploratório (depois do resultado)

VARIANTES = [('principal', {}), ('a_x_1_sobre_apt2', {'x': 'apt2'}), ('b_sem_peso', {'peso': False}),
             ('c_efeito_fixo_municipio', {'grupo': 'mun'}), ('f_mesma_urna_apuradas_sem_agregadas', {'filtro': 'f'}),
             ('g_x_1_sobre_N1', {'x': 'N1'}), ('E3_fatia_outros_1T', {'cov': ('fatiaO1',)}),
             ('E5_cinco_regressores', {'cov': ('fatiaO1', 'BN1', 'dcomp', 'logapt')})]


def dose_expl(A, x='N2', peso=True, grupo='loc2', filtro=None, cov=(), k=0, modo=None):
    f = lambda c: A[c].astype(float)
    L1, R1, O1, B1, NN1, c1, apt1 = (f(c) for c in ('L1', 'R1', 'O1', 'B1', 'N1', 'comp1', 'apt1'))
    L2, R2, c2, apt2 = (f(c) for c in ('L2', 'R2', 'comp2', 'apt2'))
    if modo == 'acrescimo':
        L2 = L2 + k; c2 = c2 + k
    elif modo == 'troca':
        t = np.minimum(k, R2); L2 = L2 + t; R2 = R2 - t
    N1, N2 = L1 + R1, L2 + R2
    apt1s, apt2s = np.where(apt1 > 0, apt1, 1), np.where(apt2 > 0, apt2, 1)
    y = L2 / N2 - L1 / N1
    xs = {'N2': 1 / N2, 'apt2': 1 / apt2s, 'N1': 1 / N1}[x]
    covs = {'fatiaO1': O1 / (L1 + R1 + O1), 'BN1': (B1 + NN1) / c1, 'dcomp': c2 / apt2s - c1 / apt1s,
            'logapt': np.log(apt2s)}
    X = np.column_stack([xs] + [covs[c] for c in cov])
    w = N2 if peso else np.ones(len(y))
    m = (apt1 > 0) & (apt2 > 0)
    if filtro == 'f':
        apur = (np.char.lower(A['tipo1'].astype(str)) == 'apurada') & (np.char.lower(A['tipo2'].astype(str)) == 'apurada')
        m &= (A['urna1'] == A['urna2']) & apur & ~A['agr1'] & ~A['agr2']
    r = fe_ols(y[m], X[m], A[grupo][m], w=w[m], nomes=['x'] + list(cov))
    return {'b': r['coef']['x'], 'ep': r['ep']['x'], 'n_secoes': r['n'], 'n_grupos': r['grupos'],
            'cov': {c: [r['coef'][c], r['ep'][c]] for c in cov}}


def comparecimento(A, filtro=None):
    apt1, apt2 = A['apt1'].astype(float), A['apt2'].astype(float)
    c1, c2 = A['comp1'].astype(float), A['comp2'].astype(float)
    ok = (apt1 > 0) & (apt2 > 0)
    return reg(c2[ok] / apt2[ok] - c1[ok] / apt1[ok], 1 / apt2[ok], A['loc2'][ok], apt2[ok], 'inv_apt2')


def exploratorio_ano(A, calibrar=False):
    out = {'variantes': {nm: dose_expl(A, **kw) for nm, kw in VARIANTES}, 'comparecimento': comparecimento(A)}
    if calibrar:
        cal = {}
        for nm, kw in VARIANTES:
            base_b = out['variantes'][nm]['b']
            cal[nm] = {}
            for modo in ('acrescimo', 'troca'):
                r = dose_expl(A, k=K_VIDEO, modo=modo, **kw)
                cal[nm][modo] = {'b': r['b'], 'ep': r['ep'], 'delta_b': r['b'] - base_b}
        out['calibracao_k10'] = cal
    return out


def veredito(b, ep):
    if b >= LIM_SINAL and b / ep > Z_SINAL:
        return 'SINAL'
    if b + 2 * ep < LIM_SINAL:
        return 'SEM SINAL'
    return 'INCONCLUSIVO'


# ------------------------------------------------------------------ análise

def rodar(p26, p22, p18, pconf, saida_json, saida_txt):
    R = {'registro': 'PRE-REGISTRO-2026-10-26.md, Adendo 25, V2 (commit 587cc65, 07/11/2026 12:10:37 UTC)',
         'script': 'scripts/analisar_V2_video.py'}
    if pconf and pconf != '-' and os.path.exists(pconf):
        conf = json.load(open(pconf))
        for t in conf.values():
            t.pop('arquivos', None)
        R['conferencia_bweb'] = conf
    d = carregar(p26)
    log('base 2026', len(d))

    # ---------------- universo
    ext1 = sum(1 for k, v in d.items() if k.startswith('ZZ|') and '1' in v)
    ext2 = sum(1 for k, v in d.items() if k.startswith('ZZ|') and '2' in v)
    k2 = [k for k, v in d.items() if not k.startswith('ZZ|') and '2' in v]
    U = [k for k in k2 if '1' in d[k]]
    R['universo'] = {'secoes_27UF_com_2T': len(k2), 'secoes_27UF_dois_turnos': len(U),
                     'exterior_1T': ext1, 'exterior_2T': ext2}

    # ---------------- item 1: literal
    porUF = collections.defaultdict(lambda: collections.Counter())
    lit = {'secoes': 0, 'votos_Lula_2T': 0, 'secoes_L2_zero': 0, 'dist_L2': collections.Counter(),
           'comp2_abaixo_10': 0, 'N2_abaixo_10': 0, 'agregadas': 0, 'mesma_urna': 0, 'votos_Lula_1T_mesmas': 0,
           'comparecimento_2T_mesmas': 0}
    desc = {'secoes': 0, 'soma_L2_menos_L1': 0, 'soma_L2': 0, 'secoes_L2_menos_L1_negativo': 0,
            'soma_L2_menos_L1_negativas': 0}
    for k in k2:
        s2 = d[k]['2']; uf = k.split('|')[0]
        porUF[uf]['secoes'] += 1
        porUF[uf]['votos_Lula_2T_UF'] += s2['L']
        if s2['L'] < K_VIDEO:
            lit['secoes'] += 1; lit['votos_Lula_2T'] += s2['L']; lit['dist_L2'][s2['L']] += 1
            lit['secoes_L2_zero'] += s2['L'] == 0
            lit['comp2_abaixo_10'] += s2['comp'] < K_VIDEO
            lit['N2_abaixo_10'] += s2['L'] + s2['R'] < K_VIDEO
            lit['agregadas'] += 'agr' in s2 or 'agr' in d[k].get('1', {})
            lit['comparecimento_2T_mesmas'] += s2['comp']
            if '1' in d[k]:
                lit['mesma_urna'] += d[k]['1']['urna'] == s2['urna']
                lit['votos_Lula_1T_mesmas'] += d[k]['1']['L']
            porUF[uf]['secoes_L2_menor_10'] += 1
            porUF[uf]['votos_Lula_nelas'] += s2['L']
        if '1' in d[k]:
            dl = s2['L'] - d[k]['1']['L']
            if dl < K_VIDEO:
                desc['secoes'] += 1; desc['soma_L2_menos_L1'] += dl; desc['soma_L2'] += s2['L']
                porUF[uf]['secoes_L2_menos_L1_menor_10'] += 1
            if dl < 0:
                desc['secoes_L2_menos_L1_negativo'] += 1; desc['soma_L2_menos_L1_negativas'] += dl
                porUF[uf]['secoes_L2_menos_L1_negativo'] += 1
    lit['dist_L2'] = {str(i): lit['dist_L2'].get(i, 0) for i in range(K_VIDEO)}
    R['item1_literal'] = {'L2_menor_10': lit, 'L2_menos_L1_menor_10': desc,
                          'por_UF': {uf: dict(c) for uf, c in sorted(porUF.items())}}
    log('item 1 ok')

    # ---------------- arrays
    A = arrays_dose(d)
    n = len(A['chaves'])
    L1, R1, L2, R2 = (A[c].astype(float) for c in ('L1', 'R1', 'L2', 'R2'))
    N1, N2 = L1 + R1, L2 + R2
    s_bar = L2.sum() / N2.sum()
    R['totais_U'] = {'secoes': n, 'L1': int(L1.sum()), 'R1': int(R1.sum()), 'L2': int(L2.sum()), 'R2': int(R2.sum()),
                     'margem_1T': int(L1.sum() - R1.sum()), 'margem_2T': int(L2.sum() - R2.sum()),
                     'fatia_Lula_2T': s_bar, 'fatia_Lula_1T': L1.sum() / N1.sum(),
                     'previsto_b_acrescimo': K_VIDEO * (1 - s_bar), 'previsto_b_troca': float(K_VIDEO)}

    # ---------------- item 2: dose
    mesma = (A['urna1'] == A['urna2']) & (A['tipo1'] == 'Apurada') & (A['tipo2'] == 'Apurada')
    sem_agr = ~A['agr1'] & ~A['agr2']
    principal = dose_spec(A)
    rob = {
        'a_x_1_sobre_apt2': dose_spec(A, x='apt2'),
        'b_sem_peso': dose_spec(A, peso=False),
        'c_efeito_fixo_municipio': dose_spec(A, grupo='mun'),
        'd_mesma_urna_apuradas': dose_spec(A, filtro=mesma),
        'e_sem_agregadas': dose_spec(A, filtro=sem_agr),
        'f_d_e_juntos': dose_spec(A, filtro=mesma & sem_agr),
        'g_x_1_sobre_N1': dose_spec(A, x='N1'),
    }
    rob_cont = {'d_mesma_urna_apuradas': int(mesma.sum()), 'e_sem_agregadas': int(sem_agr.sum()),
                'f_d_e_juntos': int((mesma & sem_agr).sum())}
    log('item 2 ok', principal)
    calib = {}
    for k in (10, 1):
        ad = dose_spec(A, L2=L2 + k, R2=R2)
        tr = dose_spec(A, L2=L2 + np.minimum(k, R2), R2=R2 - np.minimum(k, R2))
        calib[f'k{k}'] = {'acrescimo': {'b': ad['b'], 'ep': ad['ep'], 'delta_b': ad['b'] - principal['b'],
                                        'previsto': k * (1 - s_bar)},
                          'troca': {'b': tr['b'], 'ep': tr['ep'], 'delta_b': tr['b'] - principal['b'],
                                    'previsto': float(k)}}
    R['item2_dose'] = {'principal': principal, 'robustez': rob, 'secoes_nos_filtros': rob_cont, 'calibracao': calib}

    # ---------------- item 3: comparecimento
    apt1, apt2 = A['apt1'].astype(float), A['apt2'].astype(float)
    c1, c2 = A['comp1'].astype(float), A['comp2'].astype(float)
    okc = (apt1 > 0) & (apt2 > 0)
    yc = np.where(okc, c2 / np.where(apt2 > 0, apt2, 1) - c1 / np.where(apt1 > 0, apt1, 1), 0)
    xc = 1 / np.where(apt2 > 0, apt2, 1)
    comp_p = reg(yc[okc], xc[okc], A['loc2'][okc], apt2[okc], 'inv_apt2')
    m2 = okc & (A['apt1'] == A['apt2']) & mesma & sem_agr
    comp_s = reg(yc[m2], xc[m2], A['loc2'][m2], apt2[m2], 'inv_apt2')
    R['item3_comparecimento'] = {'principal': comp_p, 'aptos_iguais_mesma_urna_sem_agregacao': comp_s,
                                 'secoes_aptos_diferentes': int((A['apt1'] != A['apt2']).sum()),
                                 'variacao_comparecimento_total': int(c2.sum() - c1.sum()),
                                 'comparecimento_1T': int(c1.sum()), 'comparecimento_2T': int(c2.sum())}
    log('item 3 ok', comp_p)

    # ---------------- item 4: faixas
    y = L2 / N2 - L1 / N1
    xinv = 1 / N2
    _, g = np.unique(A['loc2'], return_inverse=True)
    G = g.max() + 1
    cnt = np.bincount(g, minlength=G)
    Sw = np.bincount(g, weights=N2, minlength=G)
    Swy = np.bincount(g, weights=N2 * y, minlength=G)
    Swx = np.bincount(g, weights=N2 * xinv, minlength=G)
    ok4 = cnt[g] >= 2
    den = Sw[g] - N2
    loo_y = np.where(ok4, (Swy[g] - N2 * y) / np.where(den > 0, den, 1), np.nan)
    loo_x = np.where(ok4, (Swx[g] - N2 * xinv) / np.where(den > 0, den, 1), np.nan)
    dv = y - loo_y; dx = xinv - loo_x
    fa = []
    Nint = A['L2'] + A['R2']
    D = np.zeros((n, len(FAIXAS)))
    for j, (nm, lo, hi) in enumerate(FAIXAS):
        D[:, j] = (Nint >= lo) & (Nint <= hi)
    bs, es, Gs = ols_cluster(dv[ok4], D[ok4], g[ok4])
    bw_, ew_, _ = ols_cluster(dv[ok4], D[ok4], g[ok4], w=N2[ok4])
    for j, (nm, lo, hi) in enumerate(FAIXAS):
        mj = ok4 & (D[:, j] == 1)
        fa.append({'faixa': nm, 'secoes': int(((D[:, j] == 1)).sum()), 'secoes_com_vizinhas': int(mj.sum()),
                   'media_pts': 100 * bs[j], 'ep_pts': 100 * es[j], 'media_ponderada_pts': 100 * bw_[j],
                   'ep_ponderada_pts': 100 * ew_[j],
                   'previsto_pts_c_acrescimo': 100 * K_VIDEO * (1 - s_bar) * float(dx[mj].mean()) if mj.any() else None,
                   'previsto_pts_c_troca': 100 * K_VIDEO * float(dx[mj].mean()) if mj.any() else None,
                   'N2_medio': float(N2[D[:, j] == 1].mean()) if (D[:, j] == 1).any() else None})
    R['item4_faixas'] = {'faixas': fa, 'secoes_sozinhas_no_local': int((~ok4).sum()), 'locais_agrupados': Gs}
    log('item 4 ok')

    # ---------------- item 5: placebos
    plac = {}
    expl = {'2026': exploratorio_ano(A, calibrar=True)}
    log('exploratório 2026 ok')
    for ano, p in (('2022', p22), ('2018', p18)):
        dd = carregar(p)
        AA = arrays_dose(dd)
        plac[ano] = dose_spec(AA)
        plac[ano]['totais'] = {'L1': int(AA['L1'].sum()), 'R1': int(AA['R1'].sum()), 'L2': int(AA['L2'].sum()),
                               'R2': int(AA['R2'].sum())}
        expl[ano] = exploratorio_ano(AA)
        del dd, AA
        log('placebo', ano, plac[ano])
    dif = {}
    for ref in ('2022', '2018'):
        dif[ref] = {}
        for nm, _ in VARIANTES:
            a, r_ = expl['2026']['variantes'][nm], expl[ref]['variantes'][nm]
            dif[ref][nm] = {'dif': a['b'] - r_['b'], 'ep': float(np.hypot(a['ep'], r_['ep']))}
        a, r_ = expl['2026']['comparecimento'], expl[ref]['comparecimento']
        dif[ref]['comparecimento'] = {'dif': a['b'] - r_['b'], 'ep': float(np.hypot(a['ep'], r_['ep']))}
    expl['diferenca_2026_menos_ref'] = dif
    k1 = [k for k, v in d.items() if not k.startswith('ZZ|') and '1' in v and v['1']['L'] + v['1']['R'] > 0]
    L1n = np.array([d[k]['1']['L'] for k in k1], float); N1n = np.array([d[k]['1']['L'] + d[k]['1']['R'] for k in k1], float)
    loc1 = np.array([chave_local(k, d[k]['1']) for k in k1])
    plac['nivel_1T_2026'] = reg(L1n / N1n, 1 / N1n, loc1, N1n, 'inv_N1')
    plac['nivel_2T_2026_ao_lado'] = reg(L2 / N2, 1 / N2, A['loc2'], N2, 'inv_N2')
    R['item5_placebos'] = plac

    # ---------------- item 6: veredito
    b, ep = principal['b'], principal['ep']
    R['item6_veredito'] = {'b': b, 'ep': ep, 'z': b / ep, 'b_mais_2ep': b + 2 * ep, 'limiar': LIM_SINAL,
                           'z_minimo': Z_SINAL, 'veredito': veredito(b, ep)}

    # ---------------- item 7: votos
    nU = n
    marg2 = int(L2.sum() - R2.sum()); marg1 = int(L1.sum() - R1.sum())
    tr = {}
    for nome, bb in (('b', b), ('b_menos_2ep', b - 2 * ep), ('b_mais_2ep', b + 2 * ep)):
        k_ad = bb / (1 - s_bar)
        tr[nome] = {'b': bb,
                    'troca': {'k_por_urna': bb, 'votos_Lula': bb * nU, 'margem': 2 * bb * nU},
                    'acrescimo': {'k_por_urna': k_ad, 'votos_Lula': k_ad * nU, 'margem': k_ad * nU}}
    R['item7_votos'] = {'urnas': nU, 'votos_video': VOTOS_VIDEO, 'margem_2T': marg2, 'margem_1T': marg1,
                        'variacao_margem': marg2 - marg1, 's_bar': s_bar, 'traducao': tr}
    e4 = {}
    for ref in ('2022', '2018'):
        dd = dif[ref]['principal']['dif']
        e4[ref] = {'dif_b': dd, 'margem_troca': 2 * dd * nU, 'votos_Lula_troca': dd * nU,
                   'margem_acrescimo': dd / (1 - s_bar) * nU,
                   'faixa_das_diferencas_nas_variantes': [min(v['dif'] for kk, v in dif[ref].items()
                                                              if kk not in ('comparecimento', 'E5_cinco_regressores')),
                                                          max(v['dif'] for kk, v in dif[ref].items()
                                                              if kk not in ('comparecimento', 'E5_cinco_regressores'))]}
    expl['E4_votos'] = e4
    R['exploratorio'] = expl

    with open(saida_json, 'w') as f:
        json.dump(R, f, ensure_ascii=False, indent=1, default=lambda o: o.item() if hasattr(o, 'item') else str(o))
    texto = escrever(R)
    with open(saida_txt, 'w') as f:
        f.write(texto)
    print(texto)


def lin_reg(nome, r, d=3):
    return (f'   {nome}: b {fn(r["b"], d, True)} (ep {fn(r["ep"], d)}, z {fn(r["z"], 1, True)}); '
            f'{fi(r["n_secoes"])} seções em {fi(r["n_locais"])} grupos')


def fs(n):
    return ('+' if n > 0 else '') + fi(n)


def pct(a, b, d=2):
    return fn(100 * a / b, d)


NOME_VAR = {'principal': 'principal (item 2)', 'a_x_1_sobre_apt2': 'a) x = 1/aptos do 2º turno',
            'b_sem_peso': 'b) sem peso', 'c_efeito_fixo_municipio': 'c) efeito fixo de município',
            'd_mesma_urna_apuradas': 'd) mesma urna e apuradas nos dois turnos',
            'e_sem_agregadas': 'e) sem seções agregadas', 'f_d_e_juntos': 'f) d e e juntos',
            'f_mesma_urna_apuradas_sem_agregadas': 'f) mesma urna, apuradas, sem agregadas',
            'g_x_1_sobre_N1': 'g) x = 1/N1 (tamanho do 1º turno)', 'E3_fatia_outros_1T': 'E3) com fatia dos outros no 1º turno',
            'E5_cinco_regressores': 'E5) cinco regressores (não é teste de dose)'}


def escrever(R):
    o = []
    A = o.append
    U, T = R['universo'], R['totais_U']
    A('V2 do Adendo 25: marca de "k votos fixos por urna" nos dados por seção (checagem do vídeo "10 votos extras para '
      'Lula por urna")')
    A(f'Registro: {R["registro"]}. Script: {R["script"]}.')
    A('Decisões que o registro não fixa: no docstring do script, gravadas antes de calcular (cópia com hora UTC e hash em '
      'adendo25/V2/docstring_antes_de_rodar.txt). Exploratório marcado como tal.')
    A('')
    A('0. Dados')
    c = R.get('conferencia_bweb')
    if c:
        d1 = sum(c['1']['discordancias_por_campo'].values()); d2 = sum(c['2']['discordancias_por_campo'].values())
        A(f'  Base por seção (trab2t/secoes2026.json.gz) conferida contra o bweb inteiro: {fi(c["1"]["conferidas"])} '
          f'seções no 1º turno e {fi(c["2"]["conferidas"])} no 2º, {fi(c["1"]["so_no_bweb"] + c["1"]["so_na_base"])} e '
          f'{fi(c["2"]["so_no_bweb"] + c["2"]["so_na_base"])} sem par; discordâncias em local, urna, tipo, aptos, '
          f'comparecimento, agregação, L, R, O, B e N: {fi(d1)} e {fi(d2)}.')
    A(f'  Universo: {fi(U["secoes_27UF_dois_turnos"])} seções das 27 UFs com os dois turnos, todas apuradas e com '
      f'L+R > 0 nos dois. Exterior (UF ZZ na chave) fora: {fi(U["exterior_1T"])} seções no 1º turno, '
      f'{fi(U["exterior_2T"])} no 2º.')
    A(f'  1º turno: Lula {fi(T["L1"])}, Flávio {fi(T["R1"])} (margem de Lula {fs(T["margem_1T"])}). 2º turno: Lula '
      f'{fi(T["L2"])}, Flávio {fi(T["R2"])} (margem {fs(T["margem_2T"])}). Fatia de Lula entre os finalistas: '
      f'{fn(100 * T["fatia_Lula_1T"], 2)}% e {fn(100 * T["fatia_Lula_2T"], 2)}%.')
    A('')

    # 1
    l = R['item1_literal']['L2_menor_10']; ds = R['item1_literal']['L2_menos_L1_menor_10']
    pu = R['item1_literal']['por_UF']; n2 = U['secoes_27UF_com_2T']
    A('1. Literal: seções com menos de 10 votos de Lula no 2º turno')
    A(f'  {fi(l["secoes"])} de {fi(n2)} seções ({pct(l["secoes"], n2, 3)}%) têm L2 < 10 e somam {fi(l["votos_Lula_2T"])} '
      f'votos de Lula; {fi(l["secoes_L2_zero"])} têm L2 = 0. Seções por valor de L2, de 0 a 9: '
      + ', '.join(f'{v}: {fi(l["dist_L2"][str(v)])}' for v in range(K_VIDEO)) + '.')
    A(f'  Dessas {fi(l["secoes"])}: {fi(l["comp2_abaixo_10"])} com comparecimento do 2º turno abaixo de 10 (nas demais '
      f'cabiam 10 votos); {fi(l["agregadas"])} agregadas; {fi(l["mesma_urna"])} com a mesma urna nos dois turnos. Lula '
      f'tinha {fi(l["votos_Lula_1T_mesmas"])} votos nelas no 1º turno.')
    com = [f'{uf} {fi(v.get("secoes_L2_menor_10", 0))} ({fi(v.get("votos_Lula_nelas", 0))} '
           f'{"voto" if v.get("votos_Lula_nelas", 0) == 1 else "votos"})'
           for uf, v in pu.items() if v.get('secoes_L2_menor_10', 0)]
    sem = [uf for uf, v in pu.items() if not v.get('secoes_L2_menor_10', 0)]
    A('  Por UF (seções com L2 < 10 e votos de Lula nelas): ' + '; '.join(com) + '. Nenhuma em ' + ', '.join(sem) + '.')
    A(f'  Descritivo: L2 - L1 < 10 em {fi(ds["secoes"])} seções ({pct(ds["secoes"], n2)}%), com soma de L2 - L1 de '
      f'{fs(ds["soma_L2_menos_L1"])} nelas; Lula perdeu votos (L2 < L1) em {fi(ds["secoes_L2_menos_L1_negativo"])} '
      f'(soma {fs(ds["soma_L2_menos_L1_negativas"])}).')
    A('  Por UF, seções com L2 - L1 < 10: ' + '; '.join(
        f'{uf} {fi(v.get("secoes_L2_menos_L1_menor_10", 0))}' for uf, v in pu.items()) + '.')
    A('')

    # 2
    p = R['item2_dose']['principal']; rb = R['item2_dose']['robustez']; cal = R['item2_dose']['calibracao']
    A('2. Dose pelo tamanho (regressão do veredito)')
    A('  y = fatia de Lula entre os finalistas no 2º turno menos a do 1º (fração); x = 1/N2, N2 = L2 + R2; efeito fixo '
      'de local do 2º turno; peso N2; erro agrupado por local (lib.fe_ols, CR1).')
    A(f'  b = {fn(p["b"], 3, True)} votos por urna (ep {fn(p["ep"])}, z {fn(p["z"], 1, True)}); {fi(p["n_secoes"])} '
      f'seções em {fi(p["n_locais"])} locais ({fi(p["secoes_sozinhas_no_grupo"])} seções sozinhas no local saem).')
    A(f'  Previsto por 10 votos por urna: b = {fn(T["previsto_b_acrescimo"])} se acrescentados (10 x (1 - '
      f'{fn(T["fatia_Lula_2T"], 3)})); b = 10 se trocados de Flávio para Lula. Sem efeito fixo: perto de zero.')
    A('  Robustez (fixada antes, não muda o veredito):')
    for nm, r in rb.items():
        A(lin_reg(NOME_VAR[nm], r).replace(' grupos', ' locais' if nm != 'c_efeito_fixo_municipio' else ' municípios'))
    A('  Calibração (k plantado em toda seção, regressão principal refeita):')
    for kk in ('k10', 'k1'):
        a_, t_ = cal[kk]['acrescimo'], cal[kk]['troca']
        A(f'   {kk[1:]} por urna: acrescentados b {fn(a_["b"], 3, True)} (variação {fn(a_["delta_b"], 3, True)}, prevista '
          f'{fn(a_["previsto"], 3, True)}); trocados b {fn(t_["b"], 3, True)} (variação {fn(t_["delta_b"], 3, True)}, '
          f'prevista {fn(t_["previsto"], 3, True)}).')
    A('')

    # 3
    cp = R['item3_comparecimento']
    A('3. Comparecimento')
    A('  y = comp2/apt2 - comp1/apt1; x = 1/apt2; efeito fixo de local do 2º turno, peso apt2, erro agrupado por local. '
      'Um acréscimo de k eleitores por urna daria coeficiente perto de k.')
    A(lin_reg('coeficiente', cp['principal']).replace(' grupos', ' locais'))
    A(lin_reg('só aptos iguais, mesma urna, sem agregação', cp['aptos_iguais_mesma_urna_sem_agregacao']
              ).replace(' grupos', ' locais'))
    A(f'  Comparecimento: {fi(cp["comparecimento_1T"])} no 1º turno, {fi(cp["comparecimento_2T"])} no 2º '
      f'({fs(cp["variacao_comparecimento_total"])}); {fi(cp["secoes_aptos_diferentes"])} seções com aptos diferentes '
      'entre os turnos.')
    A('')

    # 4
    f4 = R['item4_faixas']
    A('4. Faixas de N2: virada da seção menos a média (ponderada por N2) das outras seções do mesmo local, em pontos')
    A('  faixa          seções  com vizinhas  N2 médio   média simples (ep)   ponderada por N2 (ep)   previsto por 10/urna: '
      'acréscimo  troca')
    for r in f4['faixas']:
        A(f'  {NOME_FAIXA[r["faixa"]]:<12} {fi(r["secoes"]):>8} {fi(r["secoes_com_vizinhas"]):>12} '
          f'{fn(r["N2_medio"], 1):>9}   {fn(r["media_pts"], 3, True):>7} ({fn(r["ep_pts"], 3)})      '
          f'{fn(r["media_ponderada_pts"], 3, True):>7} ({fn(r["ep_ponderada_pts"], 3)})        '
          f'{fn(r["previsto_pts_c_acrescimo"], 2, True):>7}  {fn(r["previsto_pts_c_troca"], 2, True):>7}')
    A(f'  Seções sozinhas no local (fora): {fi(f4["secoes_sozinhas_no_local"])}. Erro agrupado por local '
      f'({fi(f4["locais_agrupados"])} locais).')
    A('')

    # 5
    pl = R['item5_placebos']
    A('5. Placebos (mesma especificação do item 2)')
    A(lin_reg('2022, Lula e Bolsonaro, 1º para 2º turno', pl['2022']).replace(' grupos', ' locais'))
    A(lin_reg('2018, Haddad e Bolsonaro, 1º para 2º turno', pl['2018']).replace(' grupos', ' locais'))
    A(lin_reg('nível do 1º turno de 2026 (fatia de Lula contra 1/N1, local do 1º turno)', pl['nivel_1T_2026']
              ).replace(' grupos', ' locais'))
    A(lin_reg('ao lado: nível do 2º turno de 2026 (fatia de Lula contra 1/N2)', pl['nivel_2T_2026_ao_lado']
              ).replace(' grupos', ' locais'))
    A('')

    # 6
    v = R['item6_veredito']
    A('6. Veredito pela letra')
    A(f'  b = {fn(v["b"], 3, True)}, ep {fn(v["ep"])}, z {fn(v["z"], 1, True)}; b + 2 ep = {fn(v["b_mais_2ep"], 3, True)}. '
      f'Sinal exige b >= 2,5 a mais de 4 ep; sem sinal, b + 2 ep < 2,5.')
    A(f'  VEREDITO: {v["veredito"]}. Placebos e comparecimento ficam ao lado e não mudam o veredito.')
    A('')

    # 7
    t = R['item7_votos']; tr = t['traducao']
    A('7. Em votos')
    A(f'  Margem de Lula no 2º turno nas 27 UFs: {fs(t["margem_2T"])} (1º turno {fs(t["margem_1T"])}; mudança '
      f'{fs(t["variacao_margem"])}). O vídeo: {fi(t["votos_video"])} votos (10 x {fi(URNAS_VIDEO)}).')
    for nm, rot in (('b', 'com b'), ('b_menos_2ep', 'com b - 2 ep'), ('b_mais_2ep', 'com b + 2 ep')):
        x = tr[nm]
        A(f'  {rot} ({fn(x["b"], 3, True)}), nas {fi(t["urnas"])} urnas: troca de Flávio para Lula, '
          f'{fi(round(x["troca"]["votos_Lula"]))} votos e {fi(round(x["troca"]["margem"]))} de margem; acréscimo '
          f'({fn(x["acrescimo"]["k_por_urna"], 2)} por urna), {fi(round(x["acrescimo"]["margem"]))} votos e de margem.')
    mx = max(tr['b_mais_2ep']['troca']['margem'], tr['b_mais_2ep']['acrescimo']['margem'])
    A(f'  Mesmo lendo todo o b como efeito fixo por urna, o limite de cima ({fi(round(mx))} de margem) é '
      f'{pct(mx, t["votos_video"], 1)}% dos {fi(t["votos_video"])} do vídeo e {pct(mx, t["margem_2T"], 1)}% da margem.')
    A('')

    # 8
    e = R['exploratorio']
    A('8. Exploratório (acrescentado depois de ver o resultado; sem veredito)')
    A('  O b de 2026 é positivo e os dos placebos, negativos. As mesmas variantes nos três anos, b (ep), e o quanto um '
      'efeito fixo real de 10 por urna mudaria cada variante em 2026 (calibração):')
    A('  variante                                       2026              2022              2018         '
      '2026-2022  2026-2018   +10 acresc.  +10 troca')
    for nm, _ in VARIANTES:
        a_, b_, c_ = (e[ano]['variantes'][nm] for ano in ('2026', '2022', '2018'))
        d22, d18 = e['diferenca_2026_menos_ref']['2022'][nm], e['diferenca_2026_menos_ref']['2018'][nm]
        k_ = e['2026']['calibracao_k10'][nm]
        A(f'  {NOME_VAR[nm]:<44} {fn(a_["b"], 3, True):>7} ({fn(a_["ep"])})  {fn(b_["b"], 3, True):>7} ({fn(b_["ep"])})  '
          f'{fn(c_["b"], 3, True):>7} ({fn(c_["ep"])})  {fn(d22["dif"], 2, True):>8}  {fn(d18["dif"], 2, True):>8}   '
          f'{fn(k_["acrescimo"]["delta_b"], 2, True):>8}   {fn(k_["troca"]["delta_b"], 2, True):>8}')
    A('  Comparecimento (item 3) nos três anos: ' + '; '.join(
        f'{ano} {fn(e[ano]["comparecimento"]["b"], 3, True)} (ep {fn(e[ano]["comparecimento"]["ep"])})'
        for ano in ('2026', '2022', '2018')) + '.')
    e4 = e['E4_votos']
    A('  E4, leitura extrema (não é estimativa): se toda a diferença da especificação principal para o placebo fosse '
      'efeito fixo por urna:')
    for ref in ('2022', '2018'):
        x = e4[ref]; fx = x['faixa_das_diferencas_nas_variantes']
        A(f'   contra {ref}: diferença {fn(x["dif_b"], 3, True)} (ep '
          f'{fn(e["diferenca_2026_menos_ref"][ref]["principal"]["ep"])}), {fi(round(x["margem_troca"]))} de margem na '
          f'troca, {fi(round(x["margem_acrescimo"]))} no acréscimo; nas variantes a, b, c, f, g e E3 a diferença vai '
          f'de {fn(fx[0], 2, True)} a {fn(fx[1], 2, True)}.')
    g26, g22, g18 = (e['2026']['variantes']['principal']['b'], -e['2022']['variantes']['principal']['b'],
                     e['2018']['variantes']['principal']['b'])
    A(f'  E6: pela fatia de quem ganhou terreno no 2º turno, b = {fn(g26, 3, True)} (Lula, 2026), {fn(g22, 3, True)} '
      f'(Bolsonaro, 2022) e {fn(g18, 3, True)} (Haddad, 2018).')
    A('')

    # 9
    fx22 = e4['2022']['faixa_das_diferencas_nas_variantes']
    cal_lo = min(min(e['2026']['calibracao_k10'][nm]['acrescimo']['delta_b'], e['2026']['calibracao_k10'][nm]['troca']['delta_b'])
                 for nm, _ in VARIANTES if nm != 'E5_cinco_regressores')
    cal_hi = max(max(e['2026']['calibracao_k10'][nm]['acrescimo']['delta_b'], e['2026']['calibracao_k10'][nm]['troca']['delta_b'])
                 for nm, _ in VARIANTES if nm != 'E5_cinco_regressores')
    fa = {r['faixa']: r for r in f4['faixas']}
    mx4 = max(e4['2022']['margem_troca'], e4['2022']['margem_acrescimo'], e4['2018']['margem_troca'],
              e4['2018']['margem_acrescimo'])
    A('9. Leitura')
    A(f'  Literal: {fi(l["secoes"])} urnas ({fi(l["secoes"] - l["comp2_abaixo_10"])} com comparecimento de 10 ou mais) '
      'têm menos de 10 votos de Lula no 2º turno. "10 a mais em toda urna" não se sustenta ao pé da letra.')
    A(f'  Dose: b = {fn(p["b"], 3, True)} (ep {fn(p["ep"])}), contra {fn(T["previsto_b_acrescimo"])} a 10 previstos; '
      f'plantar 10 por urna levaria b a {fn(cal["k10"]["acrescimo"]["b"], 3, True)} (acréscimo) ou '
      f'{fn(cal["k10"]["troca"]["b"], 3, True)} (troca). Pela letra: {v["veredito"]}.')
    A(f'  Faixas: onde 10 votos pesariam mais, a virada fica a {fn(fa["ate_50"]["media_pts"], 2, True)} (ep '
      f'{fn(fa["ate_50"]["ep_pts"], 2)}) pontos da média do local nas seções até 50 e a '
      f'{fn(fa["51_100"]["media_pts"], 2, True)} (ep {fn(fa["51_100"]["ep_pts"], 2)}) de 51 a 100, contra '
      f'{fn(fa["ate_50"]["previsto_pts_c_acrescimo"], 2, True)} a {fn(fa["ate_50"]["previsto_pts_c_troca"], 2, True)} e '
      f'{fn(fa["51_100"]["previsto_pts_c_acrescimo"], 2, True)} a {fn(fa["51_100"]["previsto_pts_c_troca"], 2, True)} '
      'previstos.')
    A(f'  Comparecimento: coeficiente {fn(cp["principal"]["b"], 3, True)}, o oposto dos +10 que 10 eleitores a mais por '
      f'urna dariam, e abaixo de 2022 ({fn(e["2022"]["comparecimento"]["b"], 3, True)}) e 2018 '
      f'({fn(e["2018"]["comparecimento"]["b"], 3, True)}).')
    A(f'  Ressalva (exploratório): o b de 2026 difere de zero e dos placebos ({fn(e4["2022"]["dif_b"], 2, True)} contra '
      f'2022, {fn(e4["2018"]["dif_b"], 2, True)} contra 2018). Essa diferença muda de tamanho e de sinal entre variantes '
      f'({fn(fx22[0], 2, True)} a {fn(fx22[1], 2, True)} contra 2022), enquanto um efeito fixo real de 10 por urna '
      f'deslocaria todas, de {fn(cal_lo, 2, True)} a {fn(cal_hi, 2, True)}. Pela fatia de quem ganhou terreno, 2022 deu '
      f'{fn(g22, 3, True)} a Bolsonaro, do tamanho dos {fn(g26, 3, True)} de Lula em 2026. Mesmo lendo toda a diferença '
      f'como efeito fixo por urna, daria até {fi(round(mx4))} de margem, {pct(mx4, VOTOS_VIDEO, 1)}% dos '
      f'{fi(VOTOS_VIDEO)} e {pct(mx4, t["margem_2T"], 1)}% da margem.')
    A('  O V2 testa um acréscimo fixo por urna. Não testa fraude proporcional nem concentrada em poucas urnas; a origem dos '
      '5.354.957 é o V1.')
    A('')

    # 10
    A('10. Desvios (decisões que o registro não fixa, escritas no docstring antes de calcular)')
    for linha in (
            'D1: contas na base por seção, não relendo o bweb a cada conta; a base foi conferida campo a campo contra o '
            'bweb dos dois turnos (item 0).',
            'D2: exterior (UF ZZ) fora; universo de 497.897 seções; nas regressões, L+R > 0 nos dois turnos (nenhuma '
            'seção saiu por isso).',
            'D3: L2 < 10 contado nas seções das 27 UFs com 2º turno; ao lado, distribuição, comparecimento abaixo de 10, '
            'agregadas, L2 - L1 < 10 e L2 < L1.',
            'D4: local = UF|município|zona|NR_LOCAL_VOTACAO do 2º turno (lib.chave_local); locais com uma seção só '
            f'saem da regressão ({fi(p["secoes_sozinhas_no_grupo"])} seções), como no lib.fe_ols.',
            'D5: robustez fixada antes, com (c) agrupando o erro por município e (f) e (g) acrescentados antes de rodar.',
            'D6: previsto exato 4,822 (acréscimo, 10 x (1 - fatia de Lula no 2º turno)) a 10 (troca); o registro '
            'arredonda para 5 a 10.',
            'D7: calibração por k plantado (10 e 1, acréscimo e troca), fora do critério.',
            'D8: comparecimento com peso apt2; ao lado, só aptos iguais, mesma urna e sem agregação.',
            'D9: faixas pela média das outras seções do local ponderada por N2 (sem a própria); seções sozinhas no '
            'local fora; média simples e ponderada; ep agrupado por local.',
            'D10: placebos sem filtro de tipo de urna; L e R de 2018 e 2022 conferidos no código e nos totais; nível do '
            '2º turno de 2026 ao lado.',
            'D11: "a mais de 4 erros-padrão" lido como b/ep > 4.',
            'D12: votos por troca (margem 2b por urna) e por acréscimo (b/(1 - fatia) por urna), vezes 497.897.',
            'Exploratório E1 a E6 acrescentado depois de ver o resultado; o E5 veio de um protótipo rodado antes de o '
            'bloco ser escrito e está aqui por transparência.'):
        A('  ' + linha)
    return '\n'.join(o) + '\n'


if __name__ == '__main__':
    modo = sys.argv[1]
    if modo == 'conferir':
        conferir(*sys.argv[2:6])
    elif modo == 'rodar':
        rodar(*sys.argv[2:8])
    else:
        sys.exit(__doc__)
