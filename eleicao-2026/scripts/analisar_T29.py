"""T29 do pré-registro (Adendo 9): matriz de transferência por UF com inferência ecológica calibrada (bweb completo).

Especificação, fixada neste arquivo antes de rodar qualquer número de 2026 (as escolhas que o registro não fixou estão
na lista DESVIOS, no fim):

Modelo multinomial-Dirichlet de transição (Brown e Payne, 1986; é a média do modelo RxC de Rosen, Jiang, King e
Tanner, 2001). Em cada seção i da UF u, os eleitores da linha r (o que fizeram no 1º turno) se repartem entre as
colunas c (o que fizeram no 2º turno) com probabilidades sorteadas de uma Dirichlet de média B_u[r, :]; a contagem do
2º turno da seção é a soma dessas multinomiais. Então E[Y_ic] = N_i * theta_ic, com theta_i = X_i B_u, e a variância
é a multinomial inflada por (1 + (N_i - 1) rho_u).
  Linhas (frações dos aptos do 1º turno da seção): L (esquerda), R (direita), outros, branco+nulo, abstenção.
  Colunas (contagens do 2º turno; N_i = aptos do 2º turno): L, R, branco+nulo, abstenção.
  2018: L = Haddad, R = Bolsonaro. 2022: L = Lula, R = Bolsonaro. 2026: L = Lula, R = Flávio.
Estimação de B_u, em cada uma das 27 UFs: quase-verossimilhança do Dirichlet-multinomial, isto é, maximizar
sum_i w_i sum_c Y_ic log(theta_ic) com cada linha de B_u no simplex (algoritmo EM, acelerado por SQUAREM; o problema
é côncavo, o máximo é único), com w_i = 1 / (1 + (N_i - 1) rho_u) e rho_u pelo método dos momentos (estatística de
Pearson) do ajuste sem peso; uma reponderação.
Erro-padrão: sanduíche agrupado por local de votação (cobre a superdispersão da Dirichlet e a correlação dentro do
local), nas células livres; célula na fronteira (abaixo de 1e-7) fica fixa em zero e é marcada.
País: a célula de cada UF ponderada pelo número de eleitores daquela linha na UF (sum_i X_ir N_i); erro-padrão pela soma
das variâncias das UFs (conjuntos disjuntos de locais). Intervalo: estimativa mais ou menos 1,96 erro-padrão.

Célula de interesse: eleitores do adversário no 1º turno que votaram em quem ganhou terreno no 2º:
  2018 Bolsonaro para Haddad (R para L); 2022 Lula para Bolsonaro (L para R); 2026 Flávio para Lula (R para L).

Validação, antes de abrir 2026 (gravada em <saida>.referencias.json antes de a base de 2026 ser lida): em 2022, uma
fração s = 2% dos votos do adversário (Lula) no 2º turno de cada seção passa para Bolsonaro (valor esperado, sem
sortear, como no T14 e no T16); o modelo é reajustado do zero com o mesmo procedimento. A troca plantada na célula é
s vezes a fração dos eleitores de Lula no 1º turno que votaram nele no 2º (célula L para L estimada sem troca).
Erro de recuperação = (célula com a troca - célula sem a troca) - troca plantada na célula. Passa se o erro for de até
1 ponto no país e em pelo menos 20 UFs (o número que o critério de sinal usa). Se não passar: SEM PODER.
O mesmo em 2018 (2% dos votos de Bolsonaro para Haddad) sai como robustez.

Critério (registro):
  SINAL: célula Flávio para Lula de 3% ou mais no país e em pelo menos 20 UFs, com o limite inferior do intervalo de
         95% acima de 1%, acima da faixa de 2018 e 2022 (no país, as células nacionais das referências; em cada UF, as
         células daquela UF nas referências).
  SEM SINAL: célula do país até 2% e dentro da faixa das duas células nacionais das referências.
  Entre os dois: INCONCLUSIVO.

Robustez e descritivos (fora do critério): 2026 com os eliminados separados (Cury 70, Renan 14, Caiado 55, Zema 30,
demais), como no T16; a matriz inteira do país em cada ano; rho por UF; leitura da faixa de cada UF contra a faixa
de todas as UFs das referências e contra a faixa nacional; limite determinístico inferior da célula (método dos
limites de Duncan e Davis, a base do King): soma de max(0, votos do ganhador no 2º turno - eleitores que não eram do
adversário no 1º) sobre os eleitores do adversário.

Uso: python3 -I analisar_T29.py <secoes2026.json.gz> <candidatos2026_1t.json.gz> <secoes2018.json.gz>
        <secoes2022.json.gz> <saida.json> <saida.txt>
"""
import os as _os, sys as _sys
_sys.path.insert(0, _os.path.dirname(_os.path.abspath(__file__)))
import collections, gc, json, sys, time, warnings
import numpy as np
from lib import carregar, chave_local
warnings.filterwarnings('ignore')

UFS = ['AC', 'AL', 'AM', 'AP', 'BA', 'CE', 'DF', 'ES', 'GO', 'MA', 'MG', 'MS', 'MT', 'PA', 'PB', 'PE', 'PI', 'PR',
       'RJ', 'RN', 'RO', 'RR', 'RS', 'SC', 'SE', 'SP', 'TO']
COLUNAS = ['L', 'R', 'branco_nulo', 'abstencao']
LINHAS5 = ['L', 'R', 'outros', 'branco_nulo', 'abstencao']
GRUPOS_2026 = [('Cury', '70'), ('Renan', '14'), ('Caiado', '55'), ('Zema', '30')]
LINHAS9 = ['L', 'R'] + [g for g, _ in GRUPOS_2026] + ['demais', 'branco_nulo', 'abstencao']
TROCA = 0.02
Z95 = 1.959963984540054
FRONTEIRA = 1e-7
TOL, MAXIT = 1e-12, 200000
ANOS = {'2018': {'ganhador': 'L', 'adversario': 'R', 'nome_g': 'Haddad', 'nome_a': 'Bolsonaro'},
        '2022': {'ganhador': 'R', 'adversario': 'L', 'nome_g': 'Bolsonaro', 'nome_a': 'Lula'},
        '2026': {'ganhador': 'L', 'adversario': 'R', 'nome_g': 'Lula', 'nome_a': 'Flávio'}}


def log(msg):
    print(f'# {time.strftime("%H:%M:%S", time.gmtime())} UTC {msg}', file=sys.stderr, flush=True)


# ------------------------------------------------------------------ dados
def montar(caminho, cand=None):
    """Arrays por UF: contagens do 1º turno por linha (n1), aptos do 1º turno, contagens do 2º turno (Y), local."""
    d = carregar(caminho)
    acc = {u: {'n1': [], 'apt1': [], 'Y': [], 'loc': []} for u in UFS}
    excl = collections.Counter()
    for k, v in d.items():
        uf = k.split('|')[0]
        if uf not in acc:
            excl['exterior'] += 1; continue
        if '1' not in v or '2' not in v:
            excl['sem_os_dois_turnos'] += 1; continue
        a, b = v['1'], v['2']
        if a['tipo'].strip().lower() != 'apurada' or b['tipo'].strip().lower() != 'apurada':
            excl['nao_apurada_em_algum_turno'] += 1; continue
        if a['apt'] <= 0 or b['apt'] <= 0:
            excl['sem_aptos'] += 1; continue
        if b['O'] != 0 or b.get('c28', 0) != 0:
            raise SystemExit(f'2º turno com outros votos nominais: {k}')
        c28 = a.get('c28', 0)   # candidatura anulada: conta como nulo, como no total oficial (Adendo 6)
        o1, bn1, ab1 = a['O'] - c28, a['B'] + a['N'] + c28, a['apt'] - a['comp']
        if cand is None:
            linha = [a['L'], a['R'], o1, bn1, ab1]
        else:
            cv = cand.get(k, {})
            if cv.get('13', 0) != a['L'] or cv.get('22', 0) != a['R']:
                raise SystemExit(f'candidatos do 1º turno não batem com a base: {k}')
            gs = [sum(cv.get(n, 0) for n in nums.split(',')) for _, nums in GRUPOS_2026]
            dem = o1 - sum(gs)
            if dem < 0:
                raise SystemExit(f'demais negativo: {k}')
            linha = [a['L'], a['R']] + gs + [dem, bn1, ab1]
        if min(linha) < 0 or a['comp'] > a['apt'] or b['comp'] > b['apt']:
            raise SystemExit(f'contagem negativa: {k}')
        s = acc[uf]
        s['n1'].append(linha); s['apt1'].append(a['apt'])
        s['Y'].append([b['L'], b['R'], b['B'] + b['N'], b['apt'] - b['comp']])
        s['loc'].append(chave_local(k, b))
    del d; gc.collect()
    out = {}
    for u in UFS:
        s = acc[u]
        n1 = np.array(s['n1'], float); apt1 = np.array(s['apt1'], float)
        _, g = np.unique(np.array(s['loc']), return_inverse=True)
        out[u] = {'X': n1 / apt1[:, None], 'Y': np.array(s['Y'], float), 'g': g, 'n1': n1}
    return out, dict(excl)


# ------------------------------------------------------------------ estimação
def passo_em(B, X, Yw):
    th = X @ B
    G = X.T @ np.where(Yw > 0, Yw / np.where(th > 0, th, 1.0), 0.0)
    Bn = B * G
    return Bn / Bn.sum(1, keepdims=True)


def logver(B, X, Yw):
    th = X @ B
    return float(np.where(Yw > 0, Yw * np.log(np.where(th > 0, th, 1e-300)), 0.0).sum())


def ajustar(X, Y, w=None, B0=None):
    """Máximo de sum_i w_i sum_c Y_ic log((X_i B)_c), linhas de B no simplex. EM com aceleração SQUAREM (SqS3)."""
    R, C = X.shape[1], Y.shape[1]
    Yw = Y if w is None else Y * w[:, None]
    if B0 is None:
        B = np.tile(Yw.sum(0) / Yw.sum(), (R, 1))
    else:
        B = np.clip(B0, 1e-6, None); B = B / B.sum(1, keepdims=True)
    lv = logver(B, X, Yw); it = 0; aval = 0
    while it < MAXIT:
        it += 1
        B1 = passo_em(B, X, Yw); B2 = passo_em(B1, X, Yw); aval += 2
        r = B1 - B; v = B2 - 2 * B1 + B
        nr, nv = np.sqrt((r * r).sum()), np.sqrt((v * v).sum())
        if nr < TOL:
            B = B2; break
        alfa = -nr / nv if nv > 0 else -1.0
        alfa = min(alfa, -1.0)
        while True:
            Bp = B - 2 * alfa * r + alfa * alfa * v
            if (Bp > 0).all() or alfa >= -1.0:
                break
            alfa = (alfa - 1.0) / 2.0
        if not (Bp > 0).all():
            Bp = B2
        Bp = passo_em(Bp, X, Yw); aval += 1
        lp = logver(Bp, X, Yw); l2 = logver(B2, X, Yw)
        if lp < l2:
            Bp, lp = B2, l2
        mud = np.abs(Bp - B).max()
        B, lv_ant, lv = Bp, lv, lp
        if mud < TOL or (abs(lv - lv_ant) < 1e-13 * abs(lv) and mud < 1e-9):
            break
    return B, {'iteracoes': it, 'avaliacoes_em': aval, 'logver': logver(B, X, Yw), 'convergiu': it < MAXIT}


def pearson_rho(B, X, Y):
    N = Y.sum(1); E = N[:, None] * (X @ B)
    P = np.where(E > 0, (Y - E) ** 2 / np.where(E > 0, E, 1.0), 0.0).sum(1)
    C = Y.shape[1]
    rho = (P.sum() - (C - 1) * len(N)) / ((C - 1) * (N - 1).sum())
    return max(0.0, float(rho)), float(P.sum() / ((C - 1) * len(N)))


def sanduiche(B, X, Y, w, g):
    """Variância agrupada por local das células de B (células livres; a de referência de cada linha por delta)."""
    R, C = B.shape
    th = X @ B
    U = w[:, None] * np.where(Y > 0, Y / th, 0.0)
    ref = B.argmax(1)
    livres = [(r, c) for r in range(R) for c in range(C) if c != ref[r] and B[r, c] > FRONTEIRA]
    P = len(livres)
    S = np.empty((len(Y), P))
    for p, (r, c) in enumerate(livres):
        S[:, p] = X[:, r] * (U[:, c] - U[:, ref[r]])
    H = np.zeros((P, P))
    for k in range(C):
        Wk = w * np.where(Y[:, k] > 0, Y[:, k] / th[:, k] ** 2, 0.0)
        D = np.zeros((len(Y), P))
        for p, (r, c) in enumerate(livres):
            if k == c:
                D[:, p] = X[:, r]
            elif k == ref[r]:
                D[:, p] = -X[:, r]
        H -= D.T @ (D * Wk[:, None])
    G = int(g.max()) + 1
    Sg = np.column_stack([np.bincount(g, weights=S[:, p], minlength=G) for p in range(P)])
    M = Sg.T @ Sg * (G / (G - 1))
    Hi = np.linalg.inv(H)
    V = Hi @ M @ Hi
    EP = np.zeros((R, C)); fronteira = np.zeros((R, C), bool)
    pos = {rc: p for p, rc in enumerate(livres)}
    for r in range(R):
        idx = [pos[(r, c)] for c in range(C) if (r, c) in pos]
        for c in range(C):
            if (r, c) in pos:
                EP[r, c] = np.sqrt(V[pos[(r, c)], pos[(r, c)]])
            elif c == ref[r]:
                EP[r, c] = np.sqrt(V[np.ix_(idx, idx)].sum()) if idx else 0.0
            else:
                fronteira[r, c] = True
    # escore total nas células livres (deve ser ~0 no máximo): conferência de convergência
    escore_max = float(np.abs(S.sum(0)).max() / max(1.0, np.abs(S).sum(0).max())) if P else 0.0
    return EP, fronteira, {'locais': G, 'parametros_livres': P, 'escore_relativo_max': escore_max}


def estimar_uf(X, Y, g):
    B1, i1 = ajustar(X, Y)
    rho, disp = pearson_rho(B1, X, Y)
    N = Y.sum(1)
    w = 1.0 / (1.0 + (N - 1.0) * rho)
    w = w / w.mean()
    B, i2 = ajustar(X, Y, w, B0=B1)
    EP, fr, inf = sanduiche(B, X, Y, w, g)
    return {'B': B, 'EP': EP, 'fronteira': fr, 'rho': rho, 'pearson_por_gl': disp, 'secoes': int(len(Y)),
            'ajuste_sem_peso': i1, 'ajuste_com_peso': i2, **inf, 'B_sem_peso': B1}


def plantar(Y, s, ganhador, adversario):
    Yp = Y.copy(); m = s * Y[:, COLUNAS.index(adversario)]
    Yp[:, COLUNAS.index(adversario)] -= m; Yp[:, COLUNAS.index(ganhador)] += m
    return Yp


def rodar_ano(base, linhas, rotulo, troca=0.0, ganhador=None, adversario=None):
    out = {}
    t0 = time.time()
    for u in UFS:
        b = base[u]
        Y = b['Y'] if troca == 0 else plantar(b['Y'], troca, ganhador, adversario)
        r = estimar_uf(b['X'], Y, b['g'])
        r['eleitores_por_linha'] = (b['X'] * b['Y'].sum(1)[:, None]).sum(0)
        r['votos_1t_por_linha'] = b['n1'].sum(0)
        out[u] = r
    log(f'{rotulo}: 27 UFs em {time.time() - t0:.0f}s')
    return out


def nacional(por_uf):
    R, C = por_uf[UFS[0]]['B'].shape
    W = np.array([por_uf[u]['eleitores_por_linha'] for u in UFS])          # UF x R
    Bs = np.array([por_uf[u]['B'] for u in UFS]); Es = np.array([por_uf[u]['EP'] for u in UFS])
    pesos = W / W.sum(0)
    A = (pesos[:, :, None] * Bs).sum(0)
    EA = np.sqrt(((pesos[:, :, None] * Es) ** 2).sum(0))
    return A, EA


def celula(por_uf, linhas, de, para):
    r, c = linhas.index(de), COLUNAS.index(para)
    A, EA = nacional(por_uf)
    uf = {u: {'celula': float(por_uf[u]['B'][r, c]), 'ep': float(por_uf[u]['EP'][r, c]),
              'fronteira': bool(por_uf[u]['fronteira'][r, c]), 'secoes': por_uf[u]['secoes'],
              'locais': por_uf[u]['locais'], 'rho': por_uf[u]['rho'],
              'celula_sem_peso': float(por_uf[u]['B_sem_peso'][r, c])} for u in UFS}
    return {'pais': float(A[r, c]), 'ep_pais': float(EA[r, c]), 'por_UF': uf}


def matriz_json(M):
    return [[float(x) for x in linha] for linha in M]


def resumo_ano(por_uf, linhas):
    A, EA = nacional(por_uf)
    return {'linhas': linhas, 'colunas': COLUNAS, 'matriz_pais': matriz_json(A), 'ep_pais': matriz_json(EA),
            'por_UF': {u: {'B': matriz_json(por_uf[u]['B']), 'EP': matriz_json(por_uf[u]['EP']),
                           'fronteira': [[bool(x) for x in l] for l in por_uf[u]['fronteira']],
                           'rho': por_uf[u]['rho'], 'pearson_por_gl': por_uf[u]['pearson_por_gl'],
                           'secoes': por_uf[u]['secoes'], 'locais': por_uf[u]['locais'],
                           'escore_relativo_max': por_uf[u]['escore_relativo_max'],
                           'iteracoes': [por_uf[u]['ajuste_sem_peso']['iteracoes'], por_uf[u]['ajuste_com_peso']['iteracoes']],
                           'convergiu': por_uf[u]['ajuste_sem_peso']['convergiu'] and por_uf[u]['ajuste_com_peso']['convergiu'],
                           'eleitores_por_linha': [float(x) for x in por_uf[u]['eleitores_por_linha']]}
                       for u in UFS}}


def limite_inferior(base, linhas, de, para):
    """Duncan e Davis: em cada seção, ao menos max(0, theta_para - (1 - X_de)) do eleitorado veio de 'de' para 'para'."""
    num = den = 0.0; secoes_pos = 0; n = 0
    porU = {}
    for u in UFS:
        b = base[u]; N = b['Y'].sum(1); th = b['Y'][:, COLUNAS.index(para)] / N; x = b['X'][:, linhas.index(de)]
        lo = np.maximum(0.0, th - (1.0 - x))
        nu, de_ = float((N * lo).sum()), float((N * x).sum())
        porU[u] = nu / de_
        num += nu; den += de_; secoes_pos += int((lo > 0).sum()); n += len(N)
    return {'pais': num / den, 'secoes_com_limite_positivo': secoes_pos, 'secoes': n, 'por_UF': porU}


def validacao(base, linhas, ano, sem, com):
    cfg = ANOS[ano]; a, gnh = cfg['adversario'], cfg['ganhador']
    r, c, cc = linhas.index(a), COLUNAS.index(gnh), COLUNAS.index(a)
    A0, _ = nacional(sem); A1, EA1 = nacional(com)
    plantada_pais = TROCA * A0[r, cc]
    rec_pais = A1[r, c] - A0[r, c]
    uf = {}
    for u in UFS:
        pl = TROCA * sem[u]['B'][r, cc]; rec = com[u]['B'][r, c] - sem[u]['B'][r, c]
        uf[u] = {'recuperada': float(rec), 'plantada_na_celula': float(pl), 'erro': float(rec - pl),
                 'erro_contra_2pct': float(rec - TROCA), 'passa': bool(abs(rec - pl) <= 0.01),
                 'celula_sem_troca': float(sem[u]['B'][r, c]), 'celula_com_troca': float(com[u]['B'][r, c])}
    n_ok = sum(x['passa'] for x in uf.values())
    passa_pais = abs(rec_pais - plantada_pais) <= 0.01
    return {'ano': ano, 'troca': TROCA, 'celula': f'{a} para {gnh}',
            'pais': {'celula_sem_troca': float(A0[r, c]), 'celula_com_troca': float(A1[r, c]), 'ep_com_troca': float(EA1[r, c]),
                     'recuperada': float(rec_pais), 'plantada_na_celula': float(plantada_pais),
                     'erro': float(rec_pais - plantada_pais), 'erro_contra_2pct': float(rec_pais - TROCA),
                     'passa': bool(passa_pais)},
            'UFs_que_passam': n_ok, 'por_UF': uf,
            'erro_max_abs_UF': float(max(abs(x['erro']) for x in uf.values())),
            'passa': bool(passa_pais and n_ok >= 20)}


# ------------------------------------------------------------------ principal
def main():
    a26, cand26, a18, a22, saida, saida_txt = sys.argv[1:7]
    saida_ref = saida + '.referencias.json'
    res = {'teste': 'T29', 'registro': 'PRE-REGISTRO-2026-10-26.md, Adendo 9',
           'modelo': 'multinomial-Dirichlet por UF, quase-verossimilhança com peso 1/(1+(N-1)rho), EM+SQUAREM, '
                     'erro-padrão sanduíche agrupado por local', 'troca_plantada': TROCA, 'referencias': {},
           'validacao': {}, 'exclusoes': {}}
    cel_ref = {}
    # 1) referências e validação, gravadas antes de ler 2026
    for ano, arq in (('2018', a18), ('2022', a22)):
        cfg = ANOS[ano]
        base, excl = montar(arq); res['exclusoes'][ano] = excl
        log(f'{ano}: {sum(base[u]["Y"].shape[0] for u in UFS)} seções')
        sem = rodar_ano(base, LINHAS5, f'{ano} sem troca')
        com = rodar_ano(base, LINHAS5, f'{ano} com troca de 2%', TROCA, cfg['ganhador'], cfg['adversario'])
        cel = celula(sem, LINHAS5, cfg['adversario'], cfg['ganhador'])
        cel_ref[ano] = cel
        res['referencias'][ano] = {**cfg, 'celula_adversario_para_ganhador': cel, 'matriz': resumo_ano(sem, LINHAS5),
                                   'limite_inferior_duncan_davis': limite_inferior(base, LINHAS5, cfg['adversario'], cfg['ganhador'])}
        res['validacao'][ano] = validacao(base, LINHAS5, ano, sem, com)
        res['validacao'][ano]['matriz_pais_com_troca'] = matriz_json(nacional(com)[0])
        v = res['validacao'][ano]
        log(f'{ano}: célula {cel["pais"]:.4f} ({cel["ep_pais"]:.4f}); recuperada {v["pais"]["recuperada"]:.4f} '
            f'plantada {v["pais"]["plantada_na_celula"]:.4f}; UFs que passam {v["UFs_que_passam"]}')
        del base, sem, com; gc.collect()
    res['validacao_registrada'] = '2022'
    res['validacao_passa'] = res['validacao']['2022']['passa']
    res['referencias_gravadas_utc'] = time.strftime('%Y-%m-%d %H:%M:%S', time.gmtime())
    json.dump(res, open(saida_ref, 'w'), ensure_ascii=False, indent=1)
    log(f'referências e validação gravadas em {saida_ref}')

    # 2) 2026
    cand = carregar(cand26)['secoes']
    base, excl = montar(a26); res['exclusoes']['2026'] = excl
    log(f'2026: {sum(base[u]["Y"].shape[0] for u in UFS)} seções')
    sem26 = rodar_ano(base, LINHAS5, '2026 (principal, 5 linhas)')
    cfg = ANOS['2026']
    cel26 = celula(sem26, LINHAS5, 'R', 'L')
    res['2026'] = {**cfg, 'celula_flavio_para_lula': cel26, 'matriz': resumo_ano(sem26, LINHAS5),
                   'limite_inferior_duncan_davis': limite_inferior(base, LINHAS5, 'R', 'L')}
    del base, sem26; gc.collect()
    base9, _ = montar(a26, cand); del cand; gc.collect()
    sem9 = rodar_ano(base9, LINHAS9, '2026 (robustez, eliminados separados)')
    res['2026_eliminados_separados'] = {'celula_flavio_para_lula': celula(sem9, LINHAS9, 'R', 'L'),
                                        'matriz': resumo_ano(sem9, LINHAS9)}
    del base9, sem9; gc.collect()

    # 3) critério
    ref_pais = {a: cel_ref[a]['pais'] for a in cel_ref}
    faixa = [min(ref_pais.values()), max(ref_pais.values())]
    c, ep = cel26['pais'], cel26['ep_pais']
    lo = c - Z95 * ep
    todas_ref_uf = [cel_ref[a]['por_UF'][u]['celula'] for a in cel_ref for u in UFS]
    ufs = {}
    for u in UFS:
        x = cel26['por_UF'][u]; xl = x['celula'] - Z95 * x['ep']
        fu = [min(cel_ref[a]['por_UF'][u]['celula'] for a in cel_ref), max(cel_ref[a]['por_UF'][u]['celula'] for a in cel_ref)]
        ufs[u] = {'celula': x['celula'], 'ep': x['ep'], 'limite_inferior_95': xl, 'faixa_referencias_UF': fu,
                  'acima_3pct': x['celula'] >= 0.03, 'intervalo_acima_1pct': xl > 0.01,
                  'acima_da_faixa_da_UF': x['celula'] > fu[1],
                  'acima_da_faixa_de_todas_as_UFs': x['celula'] > max(todas_ref_uf),
                  'acima_da_faixa_nacional': x['celula'] > faixa[1]}
        ufs[u]['conta_para_sinal'] = ufs[u]['acima_3pct'] and ufs[u]['intervalo_acima_1pct'] and ufs[u]['acima_da_faixa_da_UF']
        ufs[u]['conta_leitura_todas_UFs'] = ufs[u]['acima_3pct'] and ufs[u]['intervalo_acima_1pct'] and ufs[u]['acima_da_faixa_de_todas_as_UFs']
        ufs[u]['conta_leitura_faixa_nacional'] = ufs[u]['acima_3pct'] and ufs[u]['intervalo_acima_1pct'] and ufs[u]['acima_da_faixa_nacional']
    n_uf = sum(x['conta_para_sinal'] for x in ufs.values())
    pais_sinal = c >= 0.03 and lo > 0.01 and c > faixa[1]
    sinal = pais_sinal and n_uf >= 20
    sem_sinal = c <= 0.02 and faixa[0] <= c <= faixa[1]
    if not res['validacao_passa']:
        ver = 'SEM PODER'
    elif sinal:
        ver = 'SINAL'
    elif sem_sinal:
        ver = 'SEM SINAL'
    else:
        ver = 'INCONCLUSIVO'
    res['criterio'] = {'celula_pais_2026': c, 'ep': ep, 'ic95': [lo, c + Z95 * ep],
                       'referencias_pais': ref_pais, 'faixa_referencias_pais': faixa,
                       'pais_cumpre_sinal': pais_sinal, 'UFs_que_cumprem_sinal': n_uf,
                       'UFs_leitura_faixa_de_todas_as_UFs': sum(x['conta_leitura_todas_UFs'] for x in ufs.values()),
                       'UFs_leitura_faixa_nacional': sum(x['conta_leitura_faixa_nacional'] for x in ufs.values()),
                       'UFs_com_3pct_ou_mais': sum(x['acima_3pct'] for x in ufs.values()),
                       'faixa_de_todas_as_UFs_das_referencias': [min(todas_ref_uf), max(todas_ref_uf)],
                       'pais_ate_2pct': c <= 0.02, 'pais_dentro_da_faixa': faixa[0] <= c <= faixa[1],
                       'por_UF': ufs, 'veredito_pela_letra': ver}
    res['veredito'] = ver
    res['desvios_e_escolhas'] = DESVIOS
    json.dump(res, open(saida, 'w'), ensure_ascii=False, indent=1)
    escrever_txt(res, saida_txt)
    log(f'veredito: {ver}')


def p(x, nd=2):
    return f'{100 * x:+.{nd}f}'.replace('.', ',')


def q(x, nd=2):
    return f'{100 * x:.{nd}f}'.replace('.', ',')


def escrever_txt(res, caminho):
    L = []; P = L.append
    cr = res['criterio']
    P('T29. Matriz de transferência por UF com inferência ecológica calibrada (bweb completo do 2º turno de 2026)')
    P('Registro: PRE-REGISTRO-2026-10-26.md, Adendo 9.')
    P('Modelo: multinomial-Dirichlet de transição (Brown e Payne; média do modelo RxC de Rosen, Jiang, King e Tanner),')
    P('ajustado em cada UF por quase-verossimilhança (peso 1/(1+(N-1)rho) por seção, EM acelerado), seções como unidades.')
    P('Linhas: o que o eleitor fez no 1º turno (esquerda, direita, outros, branco+nulo, abstenção; frações dos aptos).')
    P('Colunas: o que fez no 2º turno (esquerda, direita, branco+nulo, abstenção). Erro-padrão sanduíche agrupado por local.')
    P('País = células das UFs ponderadas pelo eleitorado da linha. Valores em % dos eleitores da linha (pontos).')
    P('')
    P('1) Validação registrada (antes de abrir 2026): troca de 2% dos votos do adversário plantada no 2º turno.')
    for ano in ('2022', '2018'):
        v = res['validacao'][ano]; vp = v['pais']
        rot = 'registrada' if ano == '2022' else 'robustez'
        P(f'  {ano} ({rot}), célula {ANOS[ano]["nome_a"]} para {ANOS[ano]["nome_g"]}: sem troca {q(vp["celula_sem_troca"])}%, '
          f'com troca {q(vp["celula_com_troca"])}%; recuperado {q(vp["recuperada"])} pontos contra {q(vp["plantada_na_celula"])} '
          f'plantados na célula (erro {p(vp["erro"])}; contra 2,00: {p(vp["erro_contra_2pct"])}).')
        P(f'     UFs com erro de até 1 ponto: {v["UFs_que_passam"]} de 27; maior erro absoluto numa UF: {q(v["erro_max_abs_UF"])} ponto. '
          f'Passa: {"sim" if v["passa"] else "não"}.')
    P(f'  Validação do registro (2022): {"PASSA" if res["validacao_passa"] else "NÃO PASSA (teste sem poder)"}.')
    P('')
    P('2) Célula do adversário para quem ganhou terreno (país, com erro-padrão):')
    for ano in ('2018', '2022'):
        c = res['referencias'][ano]['celula_adversario_para_ganhador']
        P(f'  {ano} {ANOS[ano]["nome_a"]} para {ANOS[ano]["nome_g"]}: {q(c["pais"])}% (ep {q(c["ep_pais"])})')
    c = res['2026']['celula_flavio_para_lula']
    P(f'  2026 Flávio para Lula: {q(c["pais"])}% (ep {q(c["ep_pais"])}; IC95 {q(cr["ic95"][0])} a {q(cr["ic95"][1])})')
    c9 = res['2026_eliminados_separados']['celula_flavio_para_lula']
    P(f'  2026 com os eliminados separados (robustez): {q(c9["pais"])}% (ep {q(c9["ep_pais"])})')
    P('')
    P('3) Por UF (célula em %, ep; referências 2018 e 2022 da mesma UF; rho de 2026; marca * = conta para o sinal):')
    P('   UF   2026 (ep)        lim.inf.95   2018     2022     eliminados separados   seções')
    for u in sorted(UFS, key=lambda u: -cr['por_UF'][u]['celula']):
        x = cr['por_UF'][u]; r18 = res['referencias']['2018']['celula_adversario_para_ganhador']['por_UF'][u]
        r22 = res['referencias']['2022']['celula_adversario_para_ganhador']['por_UF'][u]
        e9 = c9['por_UF'][u]
        fr = ' (fronteira)' if c['por_UF'][u]['fronteira'] else ''
        P(f'   {u}  {q(x["celula"]):>6s} ({q(x["ep"])}){fr:12s} {q(x["limite_inferior_95"]):>6s}   {q(r18["celula"]):>6s}   '
          f'{q(r22["celula"]):>6s}   {q(e9["celula"]):>6s} ({q(e9["ep"])})   {c["por_UF"][u]["secoes"]:6d}'
          f'{"  *" if x["conta_para_sinal"] else ""}')
    P('')
    P('4) Matriz do país em cada ano (linha = 1º turno, coluna = 2º turno, % dos eleitores da linha):')
    for ano, m in (('2018', res['referencias']['2018']['matriz']), ('2022', res['referencias']['2022']['matriz']),
                   ('2026', res['2026']['matriz']), ('2026 eliminados separados', res['2026_eliminados_separados']['matriz'])):
        P(f'  {ano}:            ' + '  '.join(f'{c:>12s}' for c in m['colunas']))
        for i, ln in enumerate(m['linhas']):
            P(f'    {ln:16s}' + '  '.join(f'{q(m["matriz_pais"][i][j]):>6s} ({q(m["ep_pais"][i][j])})' for j in range(len(m['colunas']))))
    P('')
    P('5) Descritivos:')
    for ano in ('2018', '2022'):
        li = res['referencias'][ano]['limite_inferior_duncan_davis']
        P(f'  Limite inferior determinístico (Duncan e Davis) da célula, {ano}: {q(li["pais"], 3)}% '
          f'({li["secoes_com_limite_positivo"]} de {li["secoes"]} seções com limite positivo)')
    li = res['2026']['limite_inferior_duncan_davis']
    P(f'  Limite inferior determinístico (Duncan e Davis) da célula, 2026: {q(li["pais"], 3)}% '
      f'({li["secoes_com_limite_positivo"]} de {li["secoes"]} seções com limite positivo)')
    rh = {a: [res['referencias'][a]['matriz']['por_UF'][u]['rho'] for u in UFS] for a in ('2018', '2022')}
    rh['2026'] = [res['2026']['matriz']['por_UF'][u]['rho'] for u in UFS]
    P('  rho (superdispersão da Dirichlet) entre as UFs, mínimo e máximo: ' +
      '; '.join(f'{a} {min(v):.4f} a {max(v):.4f}'.replace('.', ',') for a, v in rh.items()))
    P(f'  UFs de 2026 com célula de 3% ou mais: {cr["UFs_com_3pct_ou_mais"]}; que cumprem as três condições com a faixa da '
      f'própria UF: {cr["UFs_que_cumprem_sinal"]}; com a faixa de todas as UFs das referências '
      f'({q(cr["faixa_de_todas_as_UFs_das_referencias"][0])} a {q(cr["faixa_de_todas_as_UFs_das_referencias"][1])}): '
      f'{cr["UFs_leitura_faixa_de_todas_as_UFs"]}; com a faixa nacional: {cr["UFs_leitura_faixa_nacional"]}.')
    P('')
    P('6) Critério registrado:')
    P('  Sinal: célula Flávio para Lula de 3% ou mais no país e em pelo menos 20 UFs, com intervalo acima de 1%, fora da')
    P('         faixa de 2018 e 2022 para quem ganhou terreno.')
    P('  Sem sinal: célula até 2% no país e dentro da faixa das referências.')
    P(f'  País: {q(cr["celula_pais_2026"])}% (IC95 {q(cr["ic95"][0])} a {q(cr["ic95"][1])}); faixa das referências '
      f'{q(cr["faixa_referencias_pais"][0])} a {q(cr["faixa_referencias_pais"][1])}.')
    P(f'  País cumpre o sinal: {"sim" if cr["pais_cumpre_sinal"] else "não"}; UFs que cumprem: {cr["UFs_que_cumprem_sinal"]} '
      f'(precisa de 20). País até 2%: {"sim" if cr["pais_ate_2pct"] else "não"}; dentro da faixa: '
      f'{"sim" if cr["pais_dentro_da_faixa"] else "não"}.')
    P(f'  Veredito pela letra: {cr["veredito_pela_letra"]}')
    P('')
    P('Escolhas e desvios do registro:')
    for t in res['desvios_e_escolhas']:
        P('  - ' + t)
    open(caminho, 'w').write('\n'.join(L) + '\n')


DESVIOS = [
    'Estimador: o registro diz "multinomial-Dirichlet ou King" sem fixar a estimação. Usei o modelo multinomial-Dirichlet '
    'de transição (Brown e Payne, 1986), cuja média é a do modelo RxC de Rosen, Jiang, King e Tanner (2001), estimado por '
    'quase-verossimilhança do Dirichlet-multinomial, com uma matriz por UF comum às seções da UF. Não rodei a versão '
    'hierárquica bayesiana (uma matriz por seção, por MCMC, como no ei.MD.bayes do R): com cerca de 470 mil seções por '
    'ano e 15 parâmetros livres por seção, o MCMC não converge em tempo útil nesta máquina, e o resultado dependeria do '
    'número de iterações. A versão usada tem o mesmo modelo de média e a mesma superdispersão da Dirichlet.',
    'Unidade: seção eleitoral (as mesmas nos dois turnos), sem efeito fixo de local: o registro pede a matriz por UF. '
    'Fora: exterior, seções sem os dois turnos, seções não apuradas em algum turno (anuladas) e seções sem aptos.',
    'Linhas e colunas: incluem branco+nulo e abstenção, porque os aptos mudam entre os turnos e a matriz precisa fechar o '
    'eleitorado. Os aptos do 1º e do 2º turno diferem em cerca de 10% das seções (em poucos eleitores); por isso as '
    'linhas entram como frações dos aptos do 1º turno e as colunas como contagens do 2º turno. O candidato 28 '
    '(candidatura anulada) conta como nulo no 1º turno de 2026, como no total oficial (5.246 votos).',
    'Referências com outros candidatos somados (as bases de 2018 e 2022 não têm voto por candidato). Em 2026 a versão '
    'principal também soma os outros, para ser comparável; a versão com Cury, Renan, Caiado, Zema e demais separados sai '
    'como robustez.',
    'Validação: a troca plantada segue a convenção do T14 e do T16 (2% dos votos do adversário no 2º turno, pelo valor '
    'esperado). Na célula, isso planta 2% vezes a fração dos eleitores do adversário que votaram nele no 2º turno (cerca '
    'de 1,9 ponto); o erro é medido contra esse valor e também contra 2,00. Leitura de "recuperação": a diferença entre a '
    'célula com e sem a troca. Exigi o erro de até 1 ponto no país e em pelo menos 20 UFs, porque o critério de sinal usa '
    'o país e 20 UFs.',
    '"Intervalo acima de 1%": limite inferior do intervalo de 95% (estimativa menos 1,96 erro-padrão) acima de 1%.',
    '"Fora da faixa de 2018 e 2022": no país, acima da maior das duas células nacionais das referências; em cada UF, acima '
    'da maior das duas células daquela UF. As leituras com a faixa de todas as UFs das referências e com a faixa nacional '
    'saem ao lado. "Dentro da faixa" (sem sinal): entre a menor e a maior célula nacional das referências, pela letra.',
    'Ordem: as referências e a validação são calculadas e gravadas antes de a base de 2026 ser lida neste script, mas o '
    'bweb de 2026 já tinha sido aberto por outros testes (T8, T14, T16 e outros, com efeito fixo de local). Nenhuma '
    'matriz de transferência do 2º turno de 2026 por UF tinha sido calculada.',
    'Exterior fora do país, como no T16.',
]

if __name__ == '__main__':
    main()
