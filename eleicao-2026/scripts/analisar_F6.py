"""F6 do pré-registro (Adendo 20, commit d976d4d, 30/10/2026 12:11:50 UTC): eleitor a mais sem biometria, nas pontas.

Letra do registro
  - Do bweb dos dois turnos: variação das liberações sem biometria (QT_ELEI_BIOM_SEM_HABILITACAO, 2º turno menos 1º)
    sobre os aptos. Grupo: o 1% de seções com a maior variação, desde que a variação seja de 10 ou mais.
  - Virada de Lula do grupo contra as outras seções do mesmo local (efeito fixo de local, erro agrupado por local, peso
    pelos votos dos finalistas no 2º turno). Sinal: diferença de 2,0 pontos ou mais a favor de Lula, a mais de 4
    erros-padrão, com 1.000 seções ou mais no grupo. Sem sinal: diferença abaixo de 0,5 em valor absoluto com erro-padrão
    até 0,25. Entre os dois: inconclusivo.
  - Logs: 40 seções do grupo e 40 de controle sorteadas nos mesmos locais (semente 20261030). Rajada de fim de dia = 10 ou
    mais habilitações sem biometria depois das 16h locais. Sinal no log: a fração de seções do grupo com rajada é pelo
    menos 3 vezes a dos controles e são 5 seções ou mais.

Decisões que o registro não fixa (escritas aqui antes de calcular a virada do grupo e antes de ler qualquer log da amostra
do F6; declaradas como desvio no resultado)
  D1. Campo: QT_ELEI_BIOM_SEM_HABILITACAO das linhas do cargo 1 (Presidente) do bweb de cada turno, lido aqui mesmo dos
      zips (uma entrada por seção; as linhas da mesma seção têm de concordar, e as discordâncias são contadas). NH abaixo.
      Conferência: comparecimento, aptos e local contra secoes2026.json.gz; NH contra o cache do T21 quando dado.
  D2. Universo do 1%: seções das 27 UFs (exterior fora: lá o campo é zero em todas as seções, não há biometria) com os
      dois turnos na base e no bweb, campo válido nos dois turnos e aptos do 2º turno acima de zero.
  D3. Variação sobre os aptos: x = 100 (NH2 - NH1) / aptos do 2º turno, em pontos. Aptos diferentes entre os turnos são
      contados e saem numa robustez.
  D4. "O 1% de seções com a maior variação": as round(0,01 N) primeiras seções na ordem decrescente de x, com os empates no
      valor de corte incluídos (x >= valor da seção de posição round(0,01 N)). "Desde que a variação seja de 10 ou mais":
      NH2 - NH1 >= 10 (em liberações, não em pontos). Grupo G = as duas condições.
  D5. Regressão: só as seções do universo com voto em pelo menos um finalista em cada turno (L+R > 0 nos dois).
      y = 100 L2/(L2+R2) - 100 L1/(L1+R1) (virada de Lula, em pontos; L = 13 Lula, R = 22 Flávio). Indicador de G,
      efeito fixo de local (UF|município|zona|local do 2º turno, lib.chave_local), peso L2+R2, erro agrupado por local
      (lib.fe_ols, CR1). O coeficiente é a diferença, em pontos, entre a virada de G e a das outras seções do mesmo local.
  D6. "1.000 seções ou mais no grupo": seções de G que entram na regressão (locais com 2 ou mais seções). Ao lado, as de G
      em locais onde o indicador varia (as que identificam o coeficiente); se a contagem mudar o veredito, isso é dito.
  D7. Veredito da regressão: SINAL se N >= 1.000, coef >= +2,0 e coef/ep > 4. SEM SINAL se |coef| < 0,5 e ep <= 0,25.
      Senão INCONCLUSIVO.
  D8. Sorteio dos logs (numpy.random.default_rng(20261030)): elegíveis do grupo = seções de G na amostra da regressão cujo
      local tem pelo menos uma seção fora de G na amostra da regressão; em ordem de chave, sorteio de 40 sem reposição.
      As 40 sorteadas, em ordem de chave, recebem cada uma um controle sorteado, com o mesmo gerador, entre as seções fora
      de G do mesmo local (em ordem de chave), sem repetir controle. Sem reposição de seção cujo log falte: a falta é
      relatada e as frações usam as seções com log lido.
  D9. Download: baixar_arquivos_urna.py, pleito 3221, tipo log, TAXA=1.0, para a pasta nova F6_arq. Se o aux listar mais de
      um pacote de log, usa o de maior índice (o mais recente, como no T21c) e conta os casos.
  D10. Mensagens do log (inspecionadas antes de contar, na amostra antiga do T3, não na do F6): não existe a mensagem
      "Tipo de habilitação do eleitor [manual]" nos logs de 2026; a única variante de "Tipo de habilitação do eleitor" é
      "[biométrica]". A habilitação de eleitor com biometria cadastrada sem a biometria aparece assim: falhas de leitura
      da digital ("Timeout de reconhecimento do dedo", "Número de tentativas de reconhecimento do dedo"), depois
      "Solicitação de dado pessoal do eleitor para habilitação manual", "Dado digitado confere", "Solicita digital do
      mesário" e, em geral, "Mesário N habilitou o eleitor", e por fim "Eleitor foi habilitado". O eleitor sem biometria
      cadastrada aparece com "Ano de nascimento digitado é igual ao do cadastro" e "Eleitor foi habilitado", sem pedido de
      digital. Classe de cada "Eleitor foi habilitado" (aplicativo VOTA), pela janela de mensagens desde o último
      "Identificador do eleitor digitado pelo mesário" (ou desde a habilitação anterior, se não houver):
        B = biométrica: a janela tem "Tipo de habilitação do eleitor [biométrica]";
        M = manual (com biometria, liberado sem ela): não B, e a janela tem "Solicitação de dado pessoal do eleitor para
            habilitação manual" ou um "Tipo de habilitação do eleitor [...]" que não seja biométrica;
        S = sem biometria cadastrada (nem B nem M).
      Conferência feita antes (300 logs da amostra antiga, sorteio random.Random(1)): M igual ao NH do bweb em 294 de 294
      seções no 2º turno e em 280 de 280 no 1º turno, entre as de log completo; M+S difere do NH na maioria. (Linha
      corrigida depois de rodar o modo "validar", antes de ler os logs do F6: com "log completo" = votos computados iguais
      ao comparecimento, M = NH em 300 de 300 no 2º turno e em 295 de 300 no 1º; nas 5 restantes M = NH + 1 e o log tem
      uma habilitação a mais que votos computados, um eleitor habilitado que não chegou a votar.) Por isso
      "habilitação sem biometria" do F6 = M (a mesma coisa que o campo do bweb conta). Leitura alternativa ao lado, sem
      mudar o veredito: M+S (toda habilitação não biométrica, a definição do T9/T21c). O modo "validar" refaz a conferência.
  D11. Hora: a do relógio da urna no log (local), dia 25/10/2026. "Depois das 16h locais" = habilitação às 16:00:00 ou
      depois. Rajada = 10 ou mais habilitações M nesse intervalo, somando todos os logs do pacote (inclui o da urna original
      quando há contingência). Leitura alternativa, sem mudar o veredito: 16h de Brasília no relógio local (16h + fuso da
      UF: AC -2; AM, RO, RR, MT e MS -1), ou seja, a última hora oficial de votação mais a fila.
  D12. Sinal no log: com fG = seções de G com rajada / seções de G com log lido e fC o mesmo nos controles, SINAL NO LOG se
      as seções de G com rajada são 5 ou mais e fG >= 3 fC (com fC = 0, basta a contagem). Senão, NÃO ATINGE O SINAL NO LOG
      (o registro não define um "sem sinal" para os logs). Os dois vereditos (regressão e logs) são relatados separados.
  Robustez e controles, fora do critério (não mudam o veredito; escolhidos antes de ver a virada do grupo):
    placebo (y = fatia de Lula no 1º turno); covariáveis (variação do comparecimento sobre aptos, fatia de Lula no 1º
    turno, log dos aptos); sem peso; só seções apuradas sem agregação nos dois turnos e com aptos iguais; urna trocada como
    covariável; efeito fixo de município; y = variação do comparecimento e do branco+nulo; espelho = o 1% de menor
    variação com NH2 - NH1 <= -10 (sozinho e junto com G); dose contínua (y contra x). Nos logs: o dia do 1º turno na
    mesma urna (quando o log do pacote o traz), leitura M+S, leitura das 16h de Brasília, habilitações por hora, quem
    liberou (mesário identificado, digital nova ou digital gravada depois do registro), falhas do leitor e conferência M
    contra NH do bweb.

Uso:
  python3 -I analisar_F6.py grupo <secoes2026.json.gz> <zips 1T> <zips 2T> <cache T21 ou -> <cache_nh.json.gz> <parcial.json> <lista.txt>
  python3 -I analisar_F6.py logs <parcial.json> <pasta_arq> <cache_nh.json.gz> <saida.json> <saida.txt>
  python3 -I analisar_F6.py validar <pasta arquivos amostra antiga> <cache_nh.json.gz> <n>
  python3 -I analisar_F6.py exploratorio <saida.json> <secoes2026.json.gz> <cache_nh.json.gz> <pasta_arq> <saida.txt>
      (modo escrito depois de ver o resultado pela letra; só pistas, sem veredito)
"""
import os as _os, sys as _sys
_sys.path.insert(0, _os.path.dirname(_os.path.abspath(__file__)))
import collections, csv, glob, gzip, json, math, os, random, re, sys, time, zipfile
from multiprocessing import Pool
import numpy as np
from lib import carregar, chave_local, fe_ols

CAMPO = 'QT_ELEI_BIOM_SEM_HABILITACAO'
SEMENTE = 20261030
FRACAO, VAR_MIN = 0.01, 10
LIM_SINAL, Z_SINAL, N_MIN = 2.0, 4.0, 1000
LIM_SEM, EP_SEM = 0.5, 0.25
N_LOG, RAJ_MIN, HORA_RAJ, RAZAO_LOG, N_LOG_MIN = 40, 10, 16 * 3600, 3.0, 5
D1, D2 = '04/10/2026', '25/10/2026'
FUSO = {'AC': -2, 'AM': -1, 'RO': -1, 'RR': -1, 'MT': -1, 'MS': -1}
MSG_BIO = 'Tipo de habilitação do eleitor [biométrica]'
MSG_MAN = 'Solicitação de dado pessoal do eleitor para habilitação manual'
MSG_HAB = 'Eleitor foi habilitado'
MSG_ID = 'Identificador do eleitor digitado pelo mesário'
MSG_VOTO = 'O voto do eleitor foi computado'
RX = re.compile(r'^(\d\d/\d\d/\d{4}) (\d\d):(\d\d):(\d\d)$')


def log(*a):
    print('#', time.strftime('%H:%M:%S'), *a, file=sys.stderr, flush=True)


# ------------------------------------------------------------------ bweb

def ler_zip(zpath):
    """Linhas do cargo 1: por seção, [loc, apt, comp, NH, tipo, agregadas, urna]; conta linhas discordantes."""
    out = {}; incons = 0; invalid = collections.Counter(); linhas = 0
    z = zipfile.ZipFile(zpath)
    nome = [n for n in z.namelist() if n.lower().endswith('.csv')][0]
    with z.open(nome) as fh:
        cab = next(csv.reader([fh.readline().decode('latin1')], delimiter=';'))
        ix = {c.strip().replace('SG_ UF', 'SG_UF'): i for i, c in enumerate(cab)}
        ic = [ix[c] for c in ('SG_UF', 'CD_MUNICIPIO', 'NR_ZONA', 'NR_SECAO', 'NR_LOCAL_VOTACAO', 'QT_APTOS',
                              'QT_COMPARECIMENTO', CAMPO, 'DS_TIPO_URNA', 'DS_SECOES_AGREGADAS', 'NR_URNA_EFETIVADA',
                              'CD_CARGO_PERGUNTA')]
        for linha in fh:
            if b';1;"Presidente";' not in linha:
                continue
            r = next(csv.reader([linha.decode('latin1').rstrip('\r\n')], delimiter=';'))
            uf, mun, zon, sec, loc, apt, comp, nh, tipo, agr, urna, car = (r[i] for i in ic)
            if car != '1':
                continue
            linhas += 1
            k = f'{uf}|{int(mun)}|{int(zon)}|{int(sec)}'
            try:
                nhv = int(nh)
                if nhv < 0:
                    invalid[nh] += 1; nhv = None
            except ValueError:
                invalid[nh] += 1; nhv = None
            agr = '' if agr in ('', '#NULO#') else agr
            reg = [int(loc), int(apt), int(comp), nhv, tipo, agr, int(urna) if urna.lstrip('-').isdigit() else urna]
            if k in out:
                if out[k] != reg:
                    incons += 1
            else:
                out[k] = reg
    return os.path.basename(zpath), out, incons, dict(invalid), linhas


def ler_pasta(pasta, pool, rot):
    zs = sorted(glob.glob(os.path.join(pasta, '*.zip')), key=lambda p: -os.path.getsize(p))
    tudo = {}; info = {}
    for nome, out, inc, inv, linhas in pool.imap_unordered(ler_zip, zs):
        tudo.update(out)
        info[nome] = {'secoes': len(out), 'linhas_cargo1': linhas, 'linhas_discordantes': inc, 'valores_invalidos': inv}
        log(rot, nome, len(out), 'seções')
    return tudo, info


# ------------------------------------------------------------------ regressão

def amostra_est(g):
    _, gi = np.unique(g, return_inverse=True)
    return np.bincount(gi)[gi] >= 2


def ident(D, g):
    _, gi = np.unique(g, return_inverse=True)
    s = np.bincount(gi, weights=D.astype(float)); n = np.bincount(gi)
    varia = (s > 0) & (s < n)
    return int(D[varia[gi]].sum()), int(varia.sum())


def reg(y, cols, nomes, g, w, mask):
    m = mask & np.isfinite(y)
    for c in cols:
        m &= np.isfinite(c)
    X = np.column_stack([c[m] for c in cols])
    r = fe_ols(y[m], X, g[m], None if w is None else w[m], nomes)
    est = np.zeros(len(y), bool); est[m] = amostra_est(g[m])
    out = {'n': r['n'], 'locais': r['grupos'], 'coef': r['coef'], 'ep': r['ep'],
           'z': {k: (r['coef'][k] / r['ep'][k] if r['ep'][k] > 0 else float('nan')) for k in nomes}}
    if nomes[0] in ('grupo', 'espelho'):
        D = cols[0].astype(bool)
        out['secoes_do_indicador_na_regressao'] = int((D & est).sum())
        out['secoes_do_indicador_que_identificam'], out['locais_que_identificam'] = ident(D[est], g[est])
    return out


def leitura(c, ep, n):
    if n >= N_MIN and c >= LIM_SINAL and ep > 0 and c / ep > Z_SINAL:
        return 'SINAL'
    if abs(c) < LIM_SEM and ep <= EP_SEM:
        return 'SEM SINAL'
    return 'INCONCLUSIVO'


def modo_grupo(base, p1, p2, cache21, cache_nh, parcial, lista):
    t0 = time.time()
    if os.path.exists(cache_nh):
        c = carregar(cache_nh); b1, b2, info = c['1'], c['2'], c['info']
        log('cache lido')
    else:
        with Pool(4) as pool:
            b2, i2 = ler_pasta(p2, pool, '2T')
            b1, i1 = ler_pasta(p1, pool, '1T')
        info = {'1': i1, '2': i2}
        with gzip.open(cache_nh, 'wt') as f:
            json.dump({'info': info, '1': b1, '2': b2}, f, separators=(',', ':'))
    log(f'extração {time.time() - t0:.0f}s: 1T {len(b1)} seções, 2T {len(b2)}')
    extr = {t: {'secoes': sum(v['secoes'] for v in info[t].values()),
                'linhas_cargo1': sum(v['linhas_cargo1'] for v in info[t].values()),
                'linhas_discordantes': sum(v['linhas_discordantes'] for v in info[t].values()),
                'valores_invalidos': dict(sum((collections.Counter(v['valores_invalidos']) for v in info[t].values()),
                                              collections.Counter()))} for t in ('1', '2')}

    d = carregar(base)
    conf = collections.Counter()
    for k, v in d.items():
        for t, bb in (('1', b1), ('2', b2)):
            if t in v and k in bb:
                f = bb[k]
                if f[2] != v[t]['comp']: conf[f'comparecimento_diferente_{t}'] += 1
                if f[1] != v[t]['apt']: conf[f'aptos_diferente_{t}'] += 1
                if f[0] != v[t]['loc']: conf[f'local_diferente_{t}'] += 1
                if f[6] != v[t]['urna']: conf[f'urna_diferente_{t}'] += 1
            elif t in v:
                conf[f'na_base_e_nao_no_bweb_{t}'] += 1
    for t, bb in (('1', b1), ('2', b2)):
        conf[f'no_bweb_e_nao_na_base_{t}'] = sum(1 for k in bb if k not in d or t not in d[k])
    if cache21 != '-' and os.path.exists(cache21):
        c21 = carregar(cache21)
        for t, bb in (('1', b1), ('2', b2)):
            conf[f'NH_diferente_do_cache_T21_{t}'] = sum(1 for k, f in bb.items() if k in c21[t] and c21[t][k][3] != f[3])
            conf[f'secoes_conferidas_com_cache_T21_{t}'] = sum(1 for k in bb if k in c21[t])
    conf = dict(conf)
    log('conferência', conf)

    rows = []; excl = collections.Counter()
    for k, v in d.items():
        if k.startswith('ZZ|'):
            excl['exterior'] += 1; continue
        a, b = v.get('1'), v.get('2')
        if a is None or b is None:
            excl['sem_os_dois_turnos'] += 1; continue
        f1, f2 = b1.get(k), b2.get(k)
        if f1 is None or f2 is None:
            excl['fora_do_bweb'] += 1; continue
        if f1[3] is None or f2[3] is None:
            excl['campo_sem_valor'] += 1; continue
        if b['apt'] <= 0:
            excl['aptos_2t_zero'] += 1; continue
        rows.append((k, chave_local(k, b), k.split('|')[0], '|'.join(k.split('|')[:2]), '|'.join(k.split('|')[:3]),
                     a['L'], a['R'], b['L'], b['R'], a['comp'], b['comp'], a['apt'], b['apt'], a['B'] + a['N'],
                     b['B'] + b['N'], f1[3], f2[3], int(a['urna'] != b['urna']),
                     int(a['tipo'] == 'Apurada' and b['tipo'] == 'Apurada' and not f1[5] and not f2[5]),
                     int(bool(f1[5]) or bool(f2[5])), a['tipo'], b['tipo']))
    del d
    log('universo', len(rows), dict(excl))
    K = np.array([r[0] for r in rows]); LOC = np.array([r[1] for r in rows]); UF = np.array([r[2] for r in rows])
    MUN = np.array([r[3] for r in rows]); ZON = np.array([r[4] for r in rows])
    A = np.array([r[5:20] for r in rows], float)
    L1, R1, L2, R2, C1, C2, AP1, AP2, BN1, BN2, NH1, NH2, TROC, LIMPA, AGR = A.T
    TROC, LIMPA, AGR = TROC.astype(bool), LIMPA.astype(bool), AGR.astype(bool)
    dNH = NH2 - NH1
    x = 100 * dNH / AP2
    N = len(x)
    n1 = int(round(FRACAO * N))
    corte = float(-np.sort(-x)[n1 - 1])
    top = x >= corte
    G = top & (dNH >= VAR_MIN)
    corte_baixo = float(np.sort(x)[n1 - 1])
    bot = x <= corte_baixo
    E = bot & (dNH <= -VAR_MIN)
    log(f'N {N}, 1% = {n1}, corte x >= {corte:.3f} pts, top {top.sum()}, G {G.sum()}; espelho corte {corte_baixo:.3f}, E {E.sum()}')

    with np.errstate(divide='ignore', invalid='ignore'):
        f1 = 100 * L1 / (L1 + R1); f2 = 100 * L2 / (L2 + R2)
        y = f2 - f1
        dcomp = 100 * (C2 - C1) / AP2
        dbn = 100 * (BN2 / C2 - BN1 / C1)
    w = L2 + R2
    M = (L1 + R1 > 0) & (L2 + R2 > 0)
    Gf = G.astype(float); Ef = E.astype(float)
    principal = reg(y, [Gf], ['grupo'], LOC, w, M)
    cg, eg = principal['coef']['grupo'], principal['ep']['grupo']
    ng = principal['secoes_do_indicador_na_regressao']
    ver = leitura(cg, eg, ng)
    ver_ident = leitura(cg, eg, principal['secoes_do_indicador_que_identificam'])
    log('principal', json.dumps(principal), ver)

    rob = {}
    rob['placebo_fatia_Lula_1T'] = reg(f1, [Gf], ['grupo'], LOC, w, M)
    rob['covariaveis'] = reg(y, [Gf, dcomp, f1, np.log(AP2)], ['grupo', 'var_comparecimento_pts', 'fatia_Lula_1T', 'log_aptos'], LOC, w, M)
    rob['sem_peso'] = reg(y, [Gf], ['grupo'], LOC, None, M)
    rob['so_apuradas_sem_agregacao_aptos_iguais'] = reg(y, [Gf], ['grupo'], LOC, w, M & LIMPA & (AP1 == AP2))
    rob['urna_trocada_como_covariavel'] = reg(y, [Gf, TROC.astype(float)], ['grupo', 'urna_trocada'], LOC, w, M)
    rob['efeito_fixo_municipio'] = reg(y, [Gf], ['grupo'], MUN, w, M)
    rob['y_var_comparecimento_pts_aptos'] = reg(dcomp, [Gf], ['grupo'], LOC, w, M)
    rob['y_var_branco_nulo_pts'] = reg(dbn, [Gf], ['grupo'], LOC, w, M & (C1 > 0) & (C2 > 0))
    rob['espelho_sozinho'] = reg(y, [Ef], ['espelho'], LOC, w, M)
    rob['grupo_e_espelho_juntos'] = reg(y, [Gf, Ef], ['grupo', 'espelho'], LOC, w, M)
    rob['dose_continua_x_pts'] = reg(y, [x], ['x_var_NH_pts_aptos'], LOC, w, M)
    rob['placebo_espelho_fatia_Lula_1T'] = reg(f1, [Ef], ['espelho'], LOC, w, M)
    log('robustez feita')

    def descr(mask):
        mm = mask & M
        return {'secoes': int(mask.sum()), 'secoes_na_amostra_da_regressao': int(mm.sum()),
                'NH_1T': int(NH1[mask].sum()), 'NH_2T': int(NH2[mask].sum()), 'var_NH': int(dNH[mask].sum()),
                'comp_1T': int(C1[mask].sum()), 'comp_2T': int(C2[mask].sum()), 'var_comp': int((C2 - C1)[mask].sum()),
                'aptos_2T': int(AP2[mask].sum()),
                'pct_NH_do_comp_1T': float(100 * NH1[mask].sum() / max(C1[mask].sum(), 1)),
                'pct_NH_do_comp_2T': float(100 * NH2[mask].sum() / max(C2[mask].sum(), 1)),
                'var_NH_sobre_var_comp': float(dNH[mask].sum() / (C2 - C1)[mask].sum()) if (C2 - C1)[mask].sum() else None,
                'pct_secoes_var_NH_maior_que_var_comp': float(100 * np.mean((dNH > (C2 - C1))[mask])) if mask.any() else None,
                'mediana_x_pts': float(np.median(x[mask])) if mask.any() else None,
                'mediana_var_NH': float(np.median(dNH[mask])) if mask.any() else None,
                'max_var_NH': int(dNH[mask].max()) if mask.any() else None,
                'pct_urna_trocada': float(100 * TROC[mask].mean()) if mask.any() else None,
                'pct_com_agregacao': float(100 * AGR[mask].mean()) if mask.any() else None,
                'pct_apuradas_sem_agregacao': float(100 * LIMPA[mask].mean()) if mask.any() else None,
                'pct_aptos_diferentes': float(100 * (AP1 != AP2)[mask].mean()) if mask.any() else None,
                'virada_bruta_ponderada_pts': float(np.sum((y * w)[mm]) / np.sum(w[mm])) if mm.any() else None,
                'fatia_Lula_1T_ponderada': float(np.sum((f1 * w)[mm]) / np.sum(w[mm])) if mm.any() else None,
                'votos_finalistas_2T': int(w[mm].sum())}

    desc = {'G': descr(G), 'top_1pct_sem_condicao_10': descr(top), 'espelho_E': descr(E), 'resto': descr(~G & ~E),
            'universo': descr(np.ones(N, bool))}
    ufs = collections.Counter(UF[G]); ufs_tot = collections.Counter(UF)
    por_uf = {u: {'secoes_G': int(ufs[u]), 'secoes_UF': int(ufs_tot[u]), 'pct': 100 * ufs[u] / ufs_tot[u]} for u in sorted(ufs_tot)}
    zon = collections.Counter(ZON[G]).most_common(15)
    mun = collections.Counter(MUN[G]).most_common(15)
    loc = collections.Counter(LOC[G]).most_common(10)
    conc = {'10_zonas_com_mais_secoes_G': zon[:10], 'pct_G_nas_10_zonas': 100 * sum(c for _, c in zon[:10]) / max(G.sum(), 1),
            'municipios_top15': mun, 'locais_top10': loc,
            'zonas_com_G': int(len(set(ZON[G]))), 'municipios_com_G': int(len(set(MUN[G]))), 'locais_com_G': int(len(set(LOC[G])))}
    # margem implícita: coef x votos dos finalistas no 2º turno nas seções de G na regressão, em votos de margem (x2)
    est = np.zeros(N, bool); est[M] = amostra_est(LOC[M])
    wG = float(w[G & est].sum())
    margem_impl = 2 * cg / 100 * wG
    margem_nac = float((L2 - R2).sum())

    # ---------------- sorteio dos logs (D8)
    Mest = M & est
    nao_G_por_loc = collections.defaultdict(list)
    for i in np.where(Mest & ~G)[0]:
        nao_G_por_loc[LOC[i]].append(K[i])
    eleg = sorted(K[i] for i in np.where(Mest & G)[0] if nao_G_por_loc.get(LOC[i]))
    rng = np.random.default_rng(SEMENTE)
    escolhidas = sorted(eleg[i] for i in rng.choice(len(eleg), N_LOG, replace=False))
    idx = {k: i for i, k in enumerate(K)}
    usados = set(); pares = []
    for kg in escolhidas:
        cand = sorted(c for c in nao_G_por_loc[LOC[idx[kg]]] if c not in usados)
        kc = cand[int(rng.integers(len(cand)))] if cand else None
        if kc: usados.add(kc)
        pares.append((kg, kc))

    def ficha(k):
        i = idx[k]
        return {'k': k, 'local': LOC[i], 'NH1': int(NH1[i]), 'NH2': int(NH2[i]), 'var_NH': int(dNH[i]), 'x_pts': float(x[i]),
                'C1': int(C1[i]), 'C2': int(C2[i]), 'aptos2': int(AP2[i]), 'L1': int(L1[i]), 'R1': int(R1[i]),
                'L2': int(L2[i]), 'R2': int(R2[i]), 'virada': float(y[i]), 'urna_trocada': bool(TROC[i]),
                'agregacao': bool(AGR[i]), 'tipo1': rows[i][20], 'tipo2': rows[i][21], 'grupo': bool(G[i])}
    amostra = [{'grupo': ficha(kg), 'controle': ficha(kc) if kc else None} for kg, kc in pares]
    with open(lista, 'w') as f:
        for kg, kc in pares:
            f.write(kg + '\n')
            if kc: f.write(kc + '\n')

    out = {'teste': 'F6 do Adendo 20', 'campo': CAMPO, 'extracao': extr, 'conferencia': conf, 'exclusoes_universo': dict(excl),
           'universo_secoes': N, 'um_por_cento_n': n1, 'corte_x_pts': corte, 'top_1pct_secoes': int(top.sum()),
           'G_secoes': int(G.sum()), 'espelho_corte_x_pts': corte_baixo, 'espelho_secoes': int(E.sum()),
           'regressao_principal': principal, 'veredito_regressao': ver,
           'veredito_regressao_contando_so_as_que_identificam': ver_ident,
           'robustez': rob, 'descritivo': desc, 'por_uf': por_uf, 'concentracao': conc,
           'margem_implicita_votos': margem_impl, 'votos_finalistas_G_na_regressao': wG, 'margem_nacional_L_menos_R_2T': margem_nac,
           'sorteio': {'semente': SEMENTE, 'elegiveis_do_grupo': len(eleg), 'pares': amostra},
           'percentis_x_pts': {p: float(np.percentile(x, p)) for p in (0.5, 1, 5, 25, 50, 75, 95, 99, 99.5)},
           'percentis_var_NH': {p: float(np.percentile(dNH, p)) for p in (0.5, 1, 5, 25, 50, 75, 95, 99, 99.5)}}
    json.dump(out, open(parcial, 'w'), ensure_ascii=False, indent=1)
    log(f'feito em {time.time() - t0:.0f}s; veredito regressão {ver}; coef {cg:+.3f} ep {eg:.3f} N {ng}')


# ------------------------------------------------------------------ logs

def classificar(caminho):
    """Habilitações por dia: lista de (segundos do dia no relógio da urna, classe B/M/S, como o mesário liberou),
    votos computados, falhas do leitor e número de logs no pacote."""
    sys.path.insert(0, _os.path.dirname(_os.path.abspath(__file__)))
    from decodificar import _linhas_log
    hab = {D1: [], D2: []}; comp = collections.Counter(); falhas = collections.Counter(); tipos = collections.Counter()
    urnas = collections.defaultdict(set); contg = False
    blocos = _linhas_log(caminho)
    for bl in blocos:
        win = []
        for l in bl:
            x = l.split('\t')
            if len(x) < 5:
                continue
            dia = x[0][:10]
            if dia not in hab:
                continue
            m = RX.match(x[0])
            if not m:
                continue
            msg = x[4]
            if msg.startswith('Modo de carga da UE - Urna de contingência') or msg.startswith('Contingência executada'):
                contg = True
            if 'ERROR opening the biometric reader' in msg or (msg.startswith('Fim do teste Biometria') and not msg.endswith('SUCESSO')):
                falhas[(dia, 'leitor')] += 1
            if x[3] != 'VOTA':
                continue
            urnas[dia].add(x[2])
            if msg.startswith('Tipo de habilitação'):
                tipos[msg] += 1
            if msg.startswith('Timeout de reconhecimento do dedo'):
                falhas[(dia, 'timeout_dedo')] += 1
            if msg == MSG_ID:
                win = []
            win.append(msg)
            if msg == MSG_HAB:
                t = int(m.group(2)) * 3600 + int(m.group(3)) * 60 + int(m.group(4))
                if MSG_BIO in win:
                    cl = 'B'
                elif any(w == MSG_MAN or (w.startswith('Tipo de habilitação do eleitor [') and 'biom' not in w) for w in win):
                    cl = 'M'
                else:
                    cl = 'S'
                como = ''
                if cl == 'M':
                    if any(re.match(r'Mesário \d+ habilitou o eleitor', w) for w in win): como = 'mesario_identificado'
                    elif any(w.startswith('Não encontrou digital coletada em nenhum dos arquivos') for w in win): como = 'digital_nova'
                    elif any(w.startswith('Digital coletada bate com uma digital gravada após o registro inicial') for w in win): como = 'digital_gravada_depois_do_registro'
                    else: como = 'outro'
                hab[dia].append((t, cl, como))
                win = []
            elif msg == MSG_VOTO:
                comp[dia] += 1
    return hab, comp, falhas, tipos, {d: len(u) for d, u in urnas.items()}, contg, len(blocos)


def resumo_dia(h, uf):
    lim_bsb = (16 + FUSO.get(uf, 0)) * 3600
    r = {'hab': len(h), 'B': sum(1 for t, c, _ in h if c == 'B'), 'M': sum(1 for t, c, _ in h if c == 'M'),
         'S': sum(1 for t, c, _ in h if c == 'S')}
    r['M_16h_local'] = sum(1 for t, c, _ in h if c == 'M' and t >= HORA_RAJ)
    r['MS_16h_local'] = sum(1 for t, c, _ in h if c in 'MS' and t >= HORA_RAJ)
    r['M_16h_brasilia'] = sum(1 for t, c, _ in h if c == 'M' and t >= lim_bsb)
    r['M_17h_local'] = sum(1 for t, c, _ in h if c == 'M' and t >= 17 * 3600)
    r['hab_16h_local'] = sum(1 for t, c, _ in h if t >= HORA_RAJ)
    r['por_hora'] = {c: collections.Counter(str(t // 3600) for t, cc, _ in h if cc == c) for c in 'BMS'}
    r['como_M'] = dict(collections.Counter(como for t, c, como in h if c == 'M'))
    ts = sorted(t for t, c, _ in h if c == 'M')
    j = 0; mx = 0
    for i in range(len(ts)):
        while ts[i] - ts[j] > 1800: j += 1
        mx = max(mx, i - j + 1)
    r['max_M_em_30min'] = mx
    r['ultima_M'] = ts[-1] if ts else None
    return r


def modo_logs(parcial, pasta, cache_nh, saida_json, saida_txt):
    P = json.load(open(parcial))
    c = carregar(cache_nh)
    resultado = []
    multiplos = 0
    for par in P['sorteio']['pares']:
        for papel in ('grupo', 'controle'):
            f = par[papel]
            if f is None:
                continue
            uf, mun, zona, sec = f['k'].split('|')
            d = os.path.join(pasta, uf.lower(), f'{int(mun):05d}', f'{int(zona):04d}', f'{int(sec):04d}')
            lg = sorted((g for g in (os.listdir(d) if os.path.isdir(d) else []) if g.endswith('-log.jez')),
                        key=lambda s: int(s.split('-')[0]))
            reg_ = {'k': f['k'], 'papel': papel, 'par': par['grupo']['k'], 'ficha': f, 'logs_no_aux': len(lg)}
            if not lg:
                reg_['sem_log'] = True; resultado.append(reg_); continue
            if len(lg) > 1:
                multiplos += 1
            hab, comp, falhas, tipos, urnas, contg, nblocos = classificar(os.path.join(d, lg[-1]))
            reg_['sem_log'] = False
            reg_['blocos_de_log'] = nblocos; reg_['contingencia'] = contg; reg_['urnas_no_log'] = urnas
            reg_['tipos_de_habilitacao_vistos'] = dict(tipos)
            reg_['falhas'] = {f'{k[0]}|{k[1]}': v for k, v in falhas.items()}
            for t, dia in (('1', D1), ('2', D2)):
                rr = resumo_dia(hab[dia], uf)
                rr['computados'] = comp[dia]
                rr['log_completo'] = comp[dia] == f['C' + t] and comp[dia] > 0
                rr['NH_bweb'] = f['NH' + t]
                rr['M_igual_NH'] = rr['M'] == f['NH' + t]
                reg_['t' + t] = rr
            reg_['rajada'] = reg_['t2']['M_16h_local'] >= RAJ_MIN
            reg_['rajada_MS'] = reg_['t2']['MS_16h_local'] >= RAJ_MIN
            reg_['rajada_16h_brasilia'] = reg_['t2']['M_16h_brasilia'] >= RAJ_MIN
            reg_['rajada_1T_mesma_urna'] = reg_['t1']['M_16h_local'] >= RAJ_MIN if reg_['t1']['log_completo'] else None
            resultado.append(reg_)

    def frac(papel, chave, so_completo=False):
        rr = [r for r in resultado if r['papel'] == papel and not r['sem_log']]
        if chave == 'rajada_1T_mesma_urna':
            rr = [r for r in rr if r[chave] is not None]
        if so_completo:
            rr = [r for r in rr if r['t2']['log_completo']]
        n = len(rr); s = sum(1 for r in rr if r[chave])
        return {'secoes_com_log': n, 'com_rajada': s, 'fracao': s / n if n else None}

    def sinal(fg, fc):
        if fg['fracao'] is None or fc['fracao'] is None:
            return 'SEM DADO'
        ok = fg['com_rajada'] >= N_LOG_MIN and (fg['fracao'] >= RAZAO_LOG * fc['fracao'])
        return 'SINAL NO LOG' if ok else 'NÃO ATINGE O SINAL NO LOG'

    leituras = {}
    for nome, chave, sc in (('principal_M_16h_local', 'rajada', False), ('M_mais_S_16h_local', 'rajada_MS', False),
                            ('M_16h_brasilia', 'rajada_16h_brasilia', False), ('principal_so_logs_completos', 'rajada', True),
                            ('placebo_dia_1T_mesma_urna', 'rajada_1T_mesma_urna', False)):
        fg, fc = frac('grupo', chave, sc), frac('controle', chave, sc)
        leituras[nome] = {'grupo': fg, 'controle': fc, 'leitura': sinal(fg, fc),
                          'razao': (fg['fracao'] / fc['fracao']) if fc['fracao'] else None}
    ver_log = leituras['principal_M_16h_local']['leitura']

    # agregados por hora
    def soma_hora(papel, t, cl):
        cnt = collections.Counter()
        for r in resultado:
            if r['papel'] == papel and not r['sem_log']:
                cnt.update(r['t' + t]['por_hora'][cl])
        return {str(h): cnt.get(str(h), 0) for h in range(0, 24)}
    horas = {f'{papel}_{t}T_{cl}': soma_hora(papel, t, cl) for papel in ('grupo', 'controle') for t in '12' for cl in 'BMS'}

    def agreg(papel):
        rr = [r for r in resultado if r['papel'] == papel and not r['sem_log']]
        o = {'secoes': len(rr), 'sem_log': sum(1 for r in resultado if r['papel'] == papel and r['sem_log']),
             'logs_completos_2T': sum(1 for r in rr if r['t2']['log_completo']),
             'logs_completos_1T': sum(1 for r in rr if r['t1']['log_completo']),
             'M_igual_NH_2T_entre_completos': sum(1 for r in rr if r['t2']['log_completo'] and r['t2']['M_igual_NH']),
             'M_igual_NH_1T_entre_completos': sum(1 for r in rr if r['t1']['log_completo'] and r['t1']['M_igual_NH']),
             'contingencia': sum(1 for r in rr if r['contingencia']),
             'secoes_com_falha_do_leitor_2T': sum(1 for r in rr if r['falhas'].get(f'{D2}|leitor')),
             'secoes_com_falha_do_leitor_1T': sum(1 for r in rr if r['falhas'].get(f'{D1}|leitor')),
             'timeout_dedo_2T': sum(r['falhas'].get(f'{D2}|timeout_dedo', 0) for r in rr),
             'timeout_dedo_1T': sum(r['falhas'].get(f'{D1}|timeout_dedo', 0) for r in rr)}
        for t in '12':
            for ch in ('hab', 'B', 'M', 'S', 'M_16h_local', 'M_16h_brasilia', 'M_17h_local', 'hab_16h_local'):
                o[f'{ch}_{t}T'] = sum(r['t' + t][ch] for r in rr)
            como = collections.Counter()
            for r in rr:
                como.update(r['t' + t]['como_M'])
            o[f'como_M_{t}T'] = dict(como)
            o[f'pct_M_depois_16h_{t}T'] = 100 * o[f'M_16h_local_{t}T'] / max(o[f'M_{t}T'], 1)
            o[f'pct_hab_depois_16h_{t}T'] = 100 * o[f'hab_16h_local_{t}T'] / max(o[f'hab_{t}T'], 1)
            o[f'pct_M_das_hab_{t}T'] = 100 * o[f'M_{t}T'] / max(o[f'hab_{t}T'], 1)
            o[f'pct_M_das_hab_depois_16h_{t}T'] = 100 * o[f'M_16h_local_{t}T'] / max(o[f'hab_16h_local_{t}T'], 1)
        return o
    ag = {'grupo': agreg('grupo'), 'controle': agreg('controle')}
    # pareado na mesma seção: M do 2T menos M do 1T (logs completos nos dois dias)
    par_ = {}
    for papel in ('grupo', 'controle'):
        rr = [r for r in resultado if r['papel'] == papel and not r['sem_log'] and r['t1']['log_completo'] and r['t2']['log_completo']]
        par_[papel] = {'secoes': len(rr), 'var_M': sum(r['t2']['M'] - r['t1']['M'] for r in rr),
                       'var_M_16h': sum(r['t2']['M_16h_local'] - r['t1']['M_16h_local'] for r in rr),
                       'var_comp': sum(r['t2']['computados'] - r['t1']['computados'] for r in rr),
                       'var_B': sum(r['t2']['B'] - r['t1']['B'] for r in rr)}

    out = {'teste': 'F6 do Adendo 20, parte dos logs', 'pasta': pasta, 'pacotes_com_mais_de_um_log': multiplos,
           'veredito_logs': ver_log, 'leituras': leituras, 'agregado': ag, 'pareado_1T_2T_mesma_secao': par_,
           'por_hora': horas, 'secoes': resultado}
    P['logs'] = out
    json.dump(P, open(saida_json, 'w'), ensure_ascii=False, indent=1)
    texto(P, saida_txt)


# ------------------------------------------------------------------ texto

def f_(x, nd=3):
    return f'{x:+.{nd}f}'.replace('.', ',') if x is not None else 'sem dado'


def p_(x, nd=1):
    return f'{x:.{nd}f}'.replace('.', ',')


def m_(x):
    return f'{x:,.0f}'.replace(',', '.')


def texto(P, saida_txt):
    L = []; w = L.append
    pr = P['regressao_principal']; rb = P['robustez']; ds = P['descritivo']; LG = P.get('logs')
    w('F6 do Adendo 20: eleitor a mais sem biometria, nas pontas (bweb completo dos dois turnos de 2026 e logs de 80 seções)')
    w('Registro: PRE-REGISTRO-2026-10-26.md, Adendo 20, commit d976d4d (30/10/2026 12:11:50 UTC). Script: scripts/analisar_F6.py.')
    w('')
    w('1. Extração e conferência')
    for t in '12':
        e = P['extracao'][t]
        w(f'  {t}º turno: {m_(e["secoes"])} seções, {m_(e["linhas_cargo1"])} linhas do cargo 1, linhas discordantes na mesma seção '
          f'{e["linhas_discordantes"]}, valores inválidos do campo {e["valores_invalidos"] or "nenhum"}.')
    w(f'  Conferência com a base e com o cache do T21: {json.dumps(P["conferencia"], ensure_ascii=False)}')
    w(f'  Universo (27 UFs, dois turnos, campo válido, aptos > 0): {m_(P["universo_secoes"])} seções; fora: '
      f'{json.dumps(P["exclusoes_universo"], ensure_ascii=False)}.')
    w('')
    w('2. Grupo')
    w(f'  x = 100 (NH2 - NH1) / aptos do 2º turno. 1% do universo = {m_(P["um_por_cento_n"])} seções; corte x >= '
      f'{f_(P["corte_x_pts"])} pontos ({P["top_1pct_secoes"]} seções com empates). Com NH2 - NH1 >= 10: G = {m_(P["G_secoes"])} seções.')
    w(f'  Percentis de x (pontos): {json.dumps({str(k): round(v, 3) for k, v in P["percentis_x_pts"].items()})}')
    w(f'  Percentis de NH2 - NH1: {json.dumps({str(k): v for k, v in P["percentis_var_NH"].items()})}')
    w(f'  Espelho (1% de menor x, com NH2 - NH1 <= -10): corte x <= {f_(P["espelho_corte_x_pts"])}; {m_(P["espelho_secoes"])} seções.')
    w('')
    w(f'  {"":<34}{"G":>12}{"espelho":>12}{"resto":>12}{"universo":>12}')
    for ch, rot in (('secoes', 'seções'), ('NH_1T', 'NH 1º turno'), ('NH_2T', 'NH 2º turno'), ('var_NH', 'variação NH'),
                    ('var_comp', 'variação comparecimento'), ('pct_NH_do_comp_1T', '% NH no comparecimento 1T'),
                    ('pct_NH_do_comp_2T', '% NH no comparecimento 2T'), ('var_NH_sobre_var_comp', 'var NH / var comp'),
                    ('pct_secoes_var_NH_maior_que_var_comp', '% seções com var NH > var comp'),
                    ('mediana_var_NH', 'mediana var NH'), ('pct_urna_trocada', '% urna trocada'),
                    ('pct_com_agregacao', '% com agregação'), ('pct_aptos_diferentes', '% aptos diferentes'),
                    ('fatia_Lula_1T_ponderada', 'fatia de Lula 1T (pond.)'), ('virada_bruta_ponderada_pts', 'virada bruta (pond.)')):
        vals = []
        for g in ('G', 'espelho_E', 'resto', 'universo'):
            v = ds[g][ch]
            vals.append('sem dado' if v is None else (m_(v) if isinstance(v, int) else f'{v:.3f}'.replace('.', ',')))
        w(f'  {rot:<34}' + ''.join(f'{v:>12}' for v in vals))
    w('')
    w('3. Regressão registrada (virada de Lula contra o indicador de G, efeito fixo de local, peso L2+R2, erro agrupado por local)')
    c, e = pr['coef']['grupo'], pr['ep']['grupo']
    w(f'  Diferença G menos outras seções do mesmo local: {f_(c)} pontos (ep {p_(e, 3)}, z {f_(pr["z"]["grupo"], 2)}); '
      f'{m_(pr["n"])} seções, {m_(pr["locais"])} locais; seções de G na regressão {m_(pr["secoes_do_indicador_na_regressao"])}, '
      f'que identificam {m_(pr["secoes_do_indicador_que_identificam"])} em {m_(pr["locais_que_identificam"])} locais.')
    w(f'  Critério: sinal pede >= +2,0, z > 4 e 1.000 seções ou mais; sem sinal pede |dif| < 0,5 e ep <= 0,25.')
    w(f'  VEREDITO (regressão): {P["veredito_regressao"]}. Contando só as seções que identificam: '
      f'{P["veredito_regressao_contando_so_as_que_identificam"]}.')
    w(f'  Margem implícita (2 x dif x votos dos finalistas de G na regressão): {m_(P["margem_implicita_votos"])} votos, contra a margem '
      f'nacional Lula menos Flávio no 2º turno de {m_(P["margem_nacional_L_menos_R_2T"])}.')
    w('')
    w('  Robustez e controles (fora do critério):')
    for nome, r in rb.items():
        partes = '  '.join(f'{k} {f_(r["coef"][k])} (ep {p_(r["ep"][k], 3)}, z {f_(r["z"][k], 1)})' for k in r['coef'])
        extra = f'; indicador na regressão {r["secoes_do_indicador_na_regressao"]}' if 'secoes_do_indicador_na_regressao' in r else ''
        w(f'   {nome}: {partes}; n {m_(r["n"])}{extra}')
    w('')
    w('  Onde está G (UFs com mais seções do grupo):')
    pu = sorted(P['por_uf'].items(), key=lambda kv: -kv[1]['secoes_G'])
    w('   ' + '; '.join(f'{u} {v["secoes_G"]} ({v["pct"]:.2f}% das seções)'.replace('.', ',') for u, v in pu if v['secoes_G']))
    cc = P['concentracao']
    w(f'  Concentração: {cc["zonas_com_G"]} zonas, {cc["municipios_com_G"]} municípios, {cc["locais_com_G"]} locais; '
      f'{p_(cc["pct_G_nas_10_zonas"])}% de G nas 10 zonas com mais seções de G: '
      + ', '.join(f'{z} ({n})' for z, n in cc['10_zonas_com_mais_secoes_G']))
    w('  Locais com mais seções de G: ' + ', '.join(f'{z} ({n})' for z, n in cc['locais_top10']))
    if LG:
        w('')
        w('4. Logs (40 do grupo e 40 de controle no mesmo local, semente 20261030)')
        ag = LG['agregado']
        for papel in ('grupo', 'controle'):
            a = ag[papel]
            w(f'  {papel}: {a["secoes"]} com log, {a["sem_log"]} sem log; log completo no 2º turno {a["logs_completos_2T"]}, '
              f'no 1º {a["logs_completos_1T"]}; M igual ao NH do bweb {a["M_igual_NH_2T_entre_completos"]} de {a["logs_completos_2T"]} '
              f'(2T) e {a["M_igual_NH_1T_entre_completos"]} de {a["logs_completos_1T"]} (1T); contingência {a["contingencia"]}; '
              f'seções com falha do leitor no 2T {a["secoes_com_falha_do_leitor_2T"]}, no 1T {a["secoes_com_falha_do_leitor_1T"]}.')
            for t in '21':
                w(f'    {t}º turno: habilitações {m_(a[f"hab_{t}T"])}, B {m_(a[f"B_{t}T"])}, M {m_(a[f"M_{t}T"])} '
                  f'({p_(a[f"pct_M_das_hab_{t}T"])}%), S {m_(a[f"S_{t}T"])}; M depois das 16h locais {a[f"M_16h_local_{t}T"]} '
                  f'({p_(a[f"pct_M_depois_16h_{t}T"])}% das M; habilitações depois das 16h: {p_(a[f"pct_hab_depois_16h_{t}T"])}% '
                  f'de todas; M entre as de depois das 16h: {p_(a[f"pct_M_das_hab_depois_16h_{t}T"])}%); M depois das 17h '
                  f'{a[f"M_17h_local_{t}T"]}; timeouts de dedo {m_(a[f"timeout_dedo_{t}T"])}; como o mesário liberou as M: '
                  f'{json.dumps(a[f"como_M_{t}T"], ensure_ascii=False)}')
        w('')
        w('  Rajada de fim de dia (10 ou mais M depois das 16h locais, dia 25/10):')
        for nome, r in LG['leituras'].items():
            g, cn = r['grupo'], r['controle']
            fr = lambda v: 'sem dado' if v is None else f'{p_(100 * v)}%'
            w(f'   {nome}: grupo {g["com_rajada"]} de {g["secoes_com_log"]} ({fr(g["fracao"])}), controle {cn["com_rajada"]} de '
              f'{cn["secoes_com_log"]} ({fr(cn["fracao"])}); {r["leitura"]}')
        w(f'  VEREDITO (logs): {LG["veredito_logs"]}.')
        w('')
        w('  Habilitações M por hora do relógio da urna, soma das seções (2º turno; 1º turno entre parênteses):')
        hs = range(7, 20)
        w('   hora      ' + ''.join(f'{h:>11}' for h in hs))
        for papel in ('grupo', 'controle'):
            a2, a1 = LG['por_hora'][f'{papel}_2T_M'], LG['por_hora'][f'{papel}_1T_M']
            w(f'   {papel:<10}' + ''.join(f'{str(a2.get(str(h), 0)) + "(" + str(a1.get(str(h), 0)) + ")":>11}' for h in hs))
        w('  Todas as habilitações por hora (2º turno; 1º entre parênteses):')
        for papel in ('grupo', 'controle'):
            tot2 = {h: sum(LG['por_hora'][f'{papel}_2T_{c}'].get(str(h), 0) for c in 'BMS') for h in hs}
            tot1 = {h: sum(LG['por_hora'][f'{papel}_1T_{c}'].get(str(h), 0) for c in 'BMS') for h in hs}
            w(f'   {papel:<10}' + ''.join(f'{str(tot2[h]) + "(" + str(tot1[h]) + ")":>11}' for h in hs))
        w('')
        w('  Pareado na mesma seção (logs completos nos dois dias), 2º turno menos 1º: '
          + json.dumps(LG['pareado_1T_2T_mesma_secao'], ensure_ascii=False))
        w('')
        w('  Seções do grupo (sorteadas), com o controle do mesmo local:')
        w(f'   {"seção":<22}{"NH1":>5}{"NH2":>5}{"C1":>5}{"C2":>5}{"virada":>8}{"M16h":>6}{"maxM30":>7}{"rajada":>7}   controle: seção, NH1, NH2, M16h, rajada')
        sec = {(r['papel'], r['par']): r for r in LG['secoes']}
        for par in P['sorteio']['pares']:
            kg = par['grupo']['k']; rg = sec.get(('grupo', kg)); rc = sec.get(('controle', kg))
            if rg is None:
                continue
            fg = rg['ficha']
            mg = '-' if rg['sem_log'] else rg['t2']['M_16h_local']; mx = '-' if rg['sem_log'] else rg['t2']['max_M_em_30min']
            raj = '-' if rg['sem_log'] else ('sim' if rg['rajada'] else 'não')
            ctl = ''
            if rc is not None:
                fc = rc['ficha']
                ctl = f'{fc["k"]}, {fc["NH1"]}, {fc["NH2"]}, ' + ('sem log' if rc['sem_log'] else f'{rc["t2"]["M_16h_local"]}, {"sim" if rc["rajada"] else "não"}')
            w(f'   {kg:<22}{fg["NH1"]:>5}{fg["NH2"]:>5}{fg["C1"]:>5}{fg["C2"]:>5}{f_(fg["virada"], 1):>8}{str(mg):>6}{str(mx):>7}{raj:>7}   {ctl}')
    X = P.get('exploratorio')
    if X:
        w('')
        w('5. Exploratório, fora do registro (escrito depois de ver o resultado pela letra; pistas, sem veredito)')
        for nome, v in X['liberacao_alta'].items():
            w(f'  NH {nome.replace("_", " ")}: {v["secoes"]} seções em {v["municipios"]} municípios; virada contra o mesmo local '
              f'{f_(v["virada_contra_local"])} (ep {p_(v["ep"], 3)}); fatia de Lula no 1º turno {p_(v["fatia_Lula_1T_pond"])}%; '
              f'municípios: ' + ', '.join(f'{a} ({b})' for a, b in v['municipios_top'][:5]))
        t = X['urna_trocada']
        w(f'  Urna trocada entre os turnos ({t["secoes_urna_trocada"]} seções): variação média de NH {p_(t["media_var_NH_trocada"], 2)} contra '
          f'{p_(t["media_var_NH_mesma_urna"], 2)}; contra o mesmo local, {f_(t["var_NH_pts_comp_contra_local"])} pontos do comparecimento '
          f'(ep {p_(t["ep"], 3)}).')
        for k_, v in X['pct_M_por_hora'].items():
            w(f'  % de M entre as habilitações por hora, {k_.replace("_pct_M", "")}: ' + ', '.join(f'{h}h {p_(q)}' for h, q in v.items()))
        w(f'  Tentativas de digital antes de cada M no 2º turno (papel|tentativas: M): {json.dumps(X["tentativas_de_digital_antes_de_cada_M_2T"], ensure_ascii=False)}')
        w('  Blocos de log das seções com contingência no 2º turno:')
        for b in X['blocos_das_secoes_com_contingencia_2T']:
            w(f'   {b["k"]} ({b["papel"]}), bloco {b["bloco"]}, urna {",".join(b["urna"])}, contingência às {b["contingencia_as"]}: '
              f'{b["habilitacoes"]} habilitações de {b["de"]} a {b["a"]}, {b["M"]} M')
    w('')
    w('Desvios e decisões (o registro não fixou; escritas no docstring antes de rodar; D1 a D12 de analisar_F6.py):')
    for linha in ('D2: exterior fora do universo (campo zero em todas as seções do exterior).',
                  'D3: denominador = aptos do 2º turno.',
                  'D4: 1% = round(0,01 N) seções de maior x, empates incluídos; "variação de 10 ou mais" lida em liberações (NH2 - NH1 >= 10).',
                  'D5: virada em pontos da fatia entre os finalistas; local = UF|município|zona|local do 2º turno; só seções com L+R > 0 nos dois turnos.',
                  'D6: "1.000 seções no grupo" contadas na amostra da regressão (locais com 2 ou mais seções).',
                  'D8: sorteio de 40 do grupo entre as que têm controle no mesmo local e 1 controle por seção, mesmo gerador, sem repetir.',
                  'D10: "habilitação sem biometria" no log = habilitação manual de eleitor com biometria (pedido de dado pessoal), a mesma '
                  'coisa que o campo do bweb conta; a mensagem "Tipo de habilitação do eleitor [manual]" não existe nos logs de 2026.',
                  'D11: "depois das 16h locais" = 16:00:00 ou depois no relógio da urna, dia 25/10/2026, todos os logs do pacote.',
                  'D12: o registro não define "sem sinal" para os logs; fora do sinal, a leitura é "não atinge o sinal no log".'):
        w('  ' + linha)
    open(saida_txt, 'w').write('\n'.join(L) + '\n')
    print('\n'.join(L))


# ------------------------------------------------------------------ exploratório (fora do registro)

def modo_exploratorio(saida_json, base, cache_nh, pasta, saida_txt):
    """Escrito depois de ver o resultado pela letra; pistas, sem veredito, sem mudar nada do critério.
    (a) seções em que a liberação sem biometria passa de 30%, 50% e 80% do comparecimento, num turno ou nos dois: virada
        contra o mesmo local (mesma regressão do principal); (b) urna trocada entre os turnos contra a variação de NH;
    (c) nos 80 logs: fatia de M por hora, tentativas de digital antes de cada M, e blocos de log das seções com
        contingência (urna, horário, habilitações e M de cada bloco)."""
    sys.path.insert(0, _os.path.dirname(_os.path.abspath(__file__)))
    from decodificar import _linhas_log
    P = json.load(open(saida_json)); d = carregar(base); c = carregar(cache_nh)
    rows = []
    for k, v in d.items():
        if k.startswith('ZZ|') or '1' not in v or '2' not in v:
            continue
        a, b = v['1'], v['2']
        if min(a['L'] + a['R'], b['L'] + b['R'], a['comp'], b['comp']) <= 0:
            continue
        rows.append((k, chave_local(k, b), '|'.join(k.split('|')[:2]), c['1'][k][3], c['2'][k][3], a['comp'], b['comp'],
                     a['L'], a['R'], b['L'], b['R'], int(a['urna'] != b['urna'])))
    del d
    K = np.array([r[0] for r in rows]); LOC = np.array([r[1] for r in rows]); MUN = np.array([r[2] for r in rows])
    A = np.array([r[3:] for r in rows], float); NH1, NH2, C1, C2, L1, R1, L2, R2, TR = A.T
    s1, s2 = NH1 / C1, NH2 / C2
    y = 100 * L2 / (L2 + R2) - 100 * L1 / (L1 + R1); w = L2 + R2; f1 = 100 * L1 / (L1 + R1)
    alto = {}
    for lim in (0.3, 0.5, 0.8):
        for nome, m in (('2T', s2 > lim), ('1T', s1 > lim), ('nos_dois', (s1 > lim) & (s2 > lim))):
            r = fe_ols(y, m.astype(float)[:, None], LOC, w, ['g'])
            alto[f'acima_de_{int(100 * lim)}pct_{nome}'] = {
                'secoes': int(m.sum()), 'municipios': int(len(set(MUN[m]))), 'virada_contra_local': r['coef']['g'],
                'ep': r['ep']['g'], 'fatia_Lula_1T_pond': float(np.average(f1[m], weights=w[m])),
                'municipios_top': collections.Counter(MUN[m]).most_common(8)}
    dNH = NH2 - NH1
    r = fe_ols(100 * dNH / C2, TR[:, None], LOC, None, ['urna_trocada'])
    troca = {'secoes_urna_trocada': int(TR.sum()), 'media_var_NH_trocada': float(dNH[TR == 1].mean()),
             'media_var_NH_mesma_urna': float(dNH[TR == 0].mean()),
             'var_NH_pts_comp_contra_local': r['coef']['urna_trocada'], 'ep': r['ep']['urna_trocada']}
    # logs
    por_hora = {}
    for chave in ('grupo', 'controle'):
        for t in '12':
            M_ = P['logs']['por_hora'][f'{chave}_{t}T_M']
            tot = {h: sum(P['logs']['por_hora'][f'{chave}_{t}T_{cl}'].get(str(h), 0) for cl in 'BMS') for h in range(24)}
            por_hora[f'{chave}_{t}T_pct_M'] = {str(h): (100 * M_.get(str(h), 0) / tot[h]) for h in range(7, 18) if tot[h]}
    tent = collections.Counter(); blocos = []
    for sec in P['logs']['secoes']:
        if sec['sem_log']:
            continue
        uf, mun, zona, se = sec['k'].split('|')
        dd = os.path.join(pasta, uf.lower(), f'{int(mun):05d}', f'{int(zona):04d}', f'{int(se):04d}')
        lg = sorted((g for g in os.listdir(dd) if g.endswith('-log.jez')), key=lambda q: int(q.split('-')[0]))[-1]
        for i, bl in enumerate(_linhas_log(os.path.join(dd, lg))):
            win = []; hab = []; urn = set(); cont = None
            for l in bl:
                x = l.split('\t')
                if len(x) < 5 or not x[0].startswith(D2):
                    continue
                if x[4].startswith('Modo de carga da UE - Urna de contingência') and cont is None:
                    cont = x[0][11:]
                if x[3] != 'VOTA':
                    continue
                urn.add(x[2])
                if x[4] == MSG_ID:
                    win = []
                win.append(x[4])
                if x[4] == MSG_HAB:
                    man = MSG_BIO not in win and MSG_MAN in win
                    if man:
                        tent[(sec['papel'], sum(1 for q in win if q.startswith('Solicita digital. Tentativa')))] += 1
                    hab.append((x[0][11:], man)); win = []
            if sec['contingencia'] and hab:
                blocos.append({'k': sec['k'], 'papel': sec['papel'], 'bloco': i, 'urna': sorted(urn), 'contingencia_as': cont,
                               'habilitacoes': len(hab), 'M': sum(1 for _, m in hab if m), 'de': hab[0][0], 'a': hab[-1][0]})
    P['exploratorio'] = {'nota': 'escrito depois de ver o resultado pela letra; pistas, sem veredito',
                         'liberacao_alta': alto, 'urna_trocada': troca, 'pct_M_por_hora': por_hora,
                         'tentativas_de_digital_antes_de_cada_M_2T': {f'{a}|{b}': v for (a, b), v in sorted(tent.items())},
                         'blocos_das_secoes_com_contingencia_2T': blocos}
    json.dump(P, open(saida_json, 'w'), ensure_ascii=False, indent=1)
    texto(P, saida_txt)


# ------------------------------------------------------------------ validação da leitura do log

def modo_validar(pasta, cache_nh, n):
    c = carregar(cache_nh)
    logs = []
    for root, _, files in os.walk(pasta):
        for f in files:
            if f.endswith('-log.jez'):
                logs.append(os.path.join(root, f))
    logs.sort(); random.Random(1).shuffle(logs); logs = logs[:n]
    difM = collections.Counter(); difMS = collections.Counter(); tipos = collections.Counter()
    for p in logs:
        uf, m, z, s = p.split('/')[-5:-1]
        k = f'{uf.upper()}|{int(m)}|{int(z)}|{int(s)}'
        hab, comp, _, tp, _, _, _ = classificar(p)
        tipos.update(tp)
        for t, dia in (('1', D1), ('2', D2)):
            if k in c[t] and c[t][k][3] is not None and comp[dia] == c[t][k][2] and comp[dia] > 0:
                nm = sum(1 for _, cl, _ in hab[dia] if cl == 'M'); ns = sum(1 for _, cl, _ in hab[dia] if cl == 'S')
                difM[(t, nm - c[t][k][3])] += 1; difMS[(t, nm + ns - c[t][k][3])] += 1
    print('variantes de "Tipo de habilitação":', dict(tipos))
    for t in '12':
        tot = sum(v for (tt, _), v in difM.items() if tt == t)
        print(f'{t}º turno: logs completos {tot}; M = NH em {difM[(t, 0)]}; M+S = NH em {difMS[(t, 0)]}')


if __name__ == '__main__':
    modo = sys.argv[1]
    if modo == 'grupo':
        modo_grupo(*sys.argv[2:9])
    elif modo == 'logs':
        modo_logs(*sys.argv[2:7])
    elif modo == 'validar':
        modo_validar(sys.argv[2], sys.argv[3], int(sys.argv[4]))
    elif modo == 'exploratorio':
        modo_exploratorio(*sys.argv[2:7])
    elif modo == '--texto':
        texto(json.load(open(sys.argv[2])), sys.argv[3])
