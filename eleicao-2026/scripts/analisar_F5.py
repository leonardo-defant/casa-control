"""F5 do pré-registro (Adendo 20, commit d976d4d, 30/10/2026 12:11:50 UTC): caudas, seções que destoam do previsto pelo
próprio 1º turno, e os arquivos de urna das 30 seções de maior z e das 10 de menor z.

Letra do registro
  Previsão: a regressão do T8 com efeito fixo de local (ganho de Lula e de Flávio contra os votos do 1º turno da seção) dá
  L2 e R2 previstos e a fatia prevista p. Para cada seção, z = (fatia observada - p) / raiz(p(1-p)/n), n = votos dos
  finalistas no 2º turno.
  Sinal: número de seções com z > +4 de pelo menos 1,3 vez o de seções com z < -4, com 200 ou mais acima de +4, e pelo
  menos 30% das seções acima de +4 em até 10 zonas. Sem sinal: razão entre 0,8 e 1,25. Entre os dois: inconclusivo.
  Relatar a margem líquida movida pelas duas caudas.
  Arquivos (boletim, RDV, log e assinatura) das 30 de maior z e das 10 de menor z. Sinal no arquivo: assinatura inválida,
  boletim diferente do bweb, RDV diferente do boletim, votos no log diferentes do comparecimento, ou anomalia A2 a A5 do
  T3, em qualquer uma delas.

Regressão (a mesma do T8/T14 de analisar_T7_T14.py, função t8 com grupos): para c em {Lula, Flávio},
  y = votos de c no 2º turno menos no 1º; X = votos no 1º turno de Cury (70), Renan (14), Caiado (55), Zema (30), demais
  outros (O1 menos esses quatro), queda do branco+nulo, variação do comparecimento, votos do adversário no 1º turno e os
  próprios; efeito fixo de local de votação (UF|mun|zona|local); sem peso; lib.fe_ols. A base é a de montar() do mesmo
  script: as 499.205 seções com os dois turnos, exterior incluído (como no T8). Os coeficientes são conferidos contra os
  gravados em resultados/T7_T14_bweb.json.
  Previsto: yhat = X b + efeito do local, com o efeito do local = média de (y - X b) nas seções do local (a solução do
  efeito fixo no MQO sem peso). L2 previsto = L1 + yhat_L; R2 previsto = R1 + yhat_R. Como o ganho somado de Lula e Flávio
  é, por identidade, outros + queda do branco+nulo + variação do comparecimento (todos no X), L2 previsto + R2 previsto =
  L2 + R2 = n em cada seção; p = L2 previsto / n e o resíduo de Flávio é o de Lula com o sinal trocado (o espelho).

Decisões que o registro não fixa (tomadas antes de calcular qualquer z; declaradas como desvio no resultado)
  D1. Previsto "dentro da amostra": o efeito do local é estimado com a própria seção (é o valor ajustado da regressão do T8).
      Sensibilidade, ao lado: efeito do local sem a própria seção (deixa uma fora), que multiplica o resíduo por m/(m-1),
      m = seções do local.
  D2. Seção sozinha no local: o efeito fixo é ela mesma (resíduo zero), sem previsão independente; fica fora (contada).
  D3. Fora do cálculo de z: n = 0, ou L2 previsto <= 0 ou >= n (p fora de 0 a 1). Contadas.
  D4. Zona = UF + número da zona (a numeração das zonas é por UF). Exterior (ZZ) incluído, como no T8; sensibilidade sem ele.
  D5. Margem líquida movida por uma cauda = soma, nas seções da cauda, de (L2 - R2) - (L2 previsto - R2 previsto)
      = 2 x (L2 - L2 previsto), em votos; comparada com a margem nacional Lula - Flávio do 2º turno (soma do bweb).
  D6. 30 de maior z e 10 de menor z: ordem pelo z da versão principal (D1); empate pela chave da seção.
  D7. Controles descritivos (não mudam o veredito): (a) contagem limpa simulada, 200 sorteios de L2* ~ Binomial(n, p) com
      o mesmo p (semente 20261030), quantas seções passariam de +4 e de -4 só pelo acaso binomial; (b) o espelho é a cauda
      de baixo (z < -4, Flávio acima do previsto); (c) caudas em +-3, +-5 e +-6; (d) só n >= 50; sem exterior; sem seções
      agregadas (DS_SECOES_AGREGADAS); deixa uma fora; (e) distribuição de z (desvio-padrão robusto pela mediana dos
      desvios absolutos), para medir quanto a dispersão real passa da binomial.
  D8. Concentração: as 10 zonas com mais seções acima de +4; fração das seções acima de +4 nelas. O mesmo para a de baixo.
  D9. Arquivos: baixados com baixar_arquivos_urna.py (pleito 3221, tipos bu,rdv,log,vota, TAXA=1.0) para uma pasta nova.
      Boletim contra o bweb: urna, aptos, comparecimento, Lula, Flávio, branco e nulo do -bu.dat (decodificar.ler_bu) contra
      as linhas do cargo 1 do zip bweb do 2º turno lidas aqui mesmo (e contra secoes2026.json.gz). RDV contra boletim:
      Lula, Flávio, branco e nulo do cargo 1 (rdv_para_bu) contra o -bu.dat. Log contra comparecimento: votos computados em
      25/10/2026 em todos os logs do pacote (inclui o da urna original se houver contingência; decodificar.ler_log) contra o
      comparecimento do boletim. A2 a A5: as contagens de ler_log no dia do 2º turno. Assinatura: saída de
      verificar_assinaturas.py na pasta; uma seção tem assinatura inválida se aparecer na lista de falhas ou se o vsc não
      estiver lá. Uma seção sem um dos arquivos fica "sem arquivo" naquele item (não conta como sinal, é relatada).
  D10. Leitura do log de cada uma (descritiva): hora em que a urna foi ligada, zerésima, "urna pronta", primeiro e último
      voto, votos por hora, votos depois das 17h, encerramento, contingência, modelo, e fração biométrica: uma habilitação
      conta como biométrica se for precedida, desde a habilitação anterior, por "Tipo de habilitação do eleitor
      [biométrica]" (definição do T9/T21c). As mesmas métricas no dia do 1º turno quando o log do pacote o traz (mesma
      urna), como controle na própria máquina. Horas no relógio da urna (local).
  D11. Razão abaixo de 0,8: o registro não diz o que é (o sinal pede 1,3 ou mais; o "sem sinal", de 0,8 a 1,25). O código,
      escrito antes de rodar, classifica como INCONCLUSIVO tudo o que não é SINAL nem SEM SINAL. Esta linha do docstring foi
      escrita depois de ver o resultado (razão 0,23), para deixar a regra explícita; a regra do código não mudou.
  Exploratório (função exploratorio, escrita depois de ver o resultado pela letra; só pistas, sem veredito): z recalibrado pela
  dispersão observada, seções longe da fronteira, resíduo em pontos, virada bruta e colapso de um finalista.

Uso:
  python3 -I analisar_F5.py caudas <secoes2026.json.gz> <candidatos2026_1t.json.gz> <T7_T14_bweb.json> <parcial.json> <lista40.txt>
  python3 -I analisar_F5.py arquivos <parcial.json> <pasta_arq> <assinaturas.json> <pasta zips 2t> <pasta zips 1t>
          <secoes2026.json.gz> <saida.json> <saida.txt>
  python3 -I analisar_F5.py perfil <saida.json> <pasta arq da amostra> <pasta_arq> <secoes2026.json.gz> <saida.txt>   (exploratório)
  python3 -I analisar_F5.py --texto <saida.json>
"""
import os as _os, sys as _sys
_sys.path.insert(0, _os.path.dirname(_os.path.abspath(__file__)))
import collections, csv, glob, gzip, io, json, os, re, sys, time, zipfile
import numpy as np

SEMENTE = 20261030
LIM = 4.0
D1, D2 = '04/10/2026', '25/10/2026'


def log(*a):
    print('#', time.strftime('%H:%M:%S'), *a, file=sys.stderr, flush=True)


# ================================================================ parte 1: caudas
def ajustar(B, c):
    """Regressão do T8 com grupos (igual a analisar_T7_T14.t8) e valores ajustados com o efeito fixo de local."""
    from analisar_T7_T14 import C, GRUPOS
    from lib import fe_ols
    A = B['A']; adv = 'R' if c == 'L' else 'L'
    y = (A[:, C[c + '2']] - A[:, C[c + '1']]).astype(float)
    rabo = [(A[:, C['B1']] + A[:, C['N1']]) - (A[:, C['B2']] + A[:, C['N2']]), A[:, C['comp2']] - A[:, C['comp1']],
            A[:, C[adv + '1']], A[:, C[c + '1']]]
    Gm = B['G']
    X = np.column_stack([Gm, A[:, C['O1']] - Gm.sum(1)] + rabo).astype(float)
    nomes = [g for g, _ in GRUPOS] + ['demais_outros', 'queda_branco_nulo', 'var_comparecimento', 'adversario_1T', 'proprio_1T']
    r = fe_ols(y, X, B['loc'], None, nomes)
    b = np.array([r['coef'][n] for n in nomes])
    e = y - X @ b
    loc = B['loc']; m = np.bincount(loc)
    alfa = np.bincount(loc, weights=e) / np.maximum(m, 1)
    res = e - alfa[loc]
    return r, y - res, res, m[loc]


def contar(z, mask, lim=LIM):
    zz = z[mask]
    return int((zz > lim).sum()), int((zz < -lim).sum())


def razao(a, b):
    return a / b if b else (float('inf') if a else None)


def zonas_top(keys, sel, k=10):
    zon = collections.Counter()
    for kk in keys[sel]:
        uf, mun, zona, _ = kk.split('|'); zon[f'{uf}|{zona}'] += 1
    tot = int(sel.sum()); top = zon.most_common(k)
    return {'secoes': tot, 'zonas_distintas': len(zon), 'top10': [[z, n] for z, n in top],
            'pct_nas_top10': 100 * sum(n for _, n in top) / tot if tot else None}


def caudas(arq_secoes, arq_cand, arq_t8, saida, lista):
    from analisar_T7_T14 import montar, C
    from lib import carregar
    log('carregando'); d = carregar(arq_secoes); cand = carregar(arq_cand)['secoes']
    agr = {k for k, v in d.items() if '2' in v and 'agr' in v['2']}
    margem_nacional = int(sum(v['2']['L'] - v['2']['R'] for v in d.values() if '2' in v))
    votos_fin = int(sum(v['2']['L'] + v['2']['R'] for v in d.values() if '2' in v))
    B = montar(d, cand); del d, cand
    A = B['A']; keys = B['keys']; N = len(A)
    log('secoes', N)
    rL, yhL, resL, msz = ajustar(B, 'L')
    rR, yhR, resR, _ = ajustar(B, 'R')
    ref = json.load(open(arq_t8))['2026']
    conf = {c: max(abs(r['coef'][n] - ref[k]['coef'][n]) for n in r['coef'])
            for c, r, k in (('L', rL, 'T14_com_grupos'), ('R', rR, 'T8_Flavio_com_grupos'))}
    log('dif. max. dos coeficientes contra o T8 gravado', conf)
    L1, R1, L2, R2 = (A[:, C[x]].astype(float) for x in ('L1', 'R1', 'L2', 'R2'))
    n = L2 + R2
    L2h = L1 + yhL; R2h = R1 + yhR
    ident = float(np.max(np.abs(L2h + R2h - n)))
    log('identidade L2h+R2h=n, maior desvio', ident)
    sozinha = msz < 2
    ok_base = (~sozinha) & (n > 0)
    ok = ok_base & (L2h > 0) & (L2h < n)
    p = np.where(ok, L2h / np.where(n > 0, n, 1), np.nan)
    f = np.where(n > 0, L2 / np.where(n > 0, n, 1), np.nan)
    sd = np.sqrt(p * (1 - p) / np.where(n > 0, n, 1))
    z = np.where(ok, (f - p) / sd, np.nan)
    # deixa uma fora
    fator = np.where(msz >= 2, msz / np.maximum(msz - 1, 1), np.nan)
    L2h_loo = L2 - resL * fator
    ok_loo = ok_base & (L2h_loo > 0) & (L2h_loo < n)
    p_loo = np.where(ok_loo, L2h_loo / np.where(n > 0, n, 1), np.nan)
    z_loo = np.where(ok_loo, (f - p_loo) / np.sqrt(p_loo * (1 - p_loo) / np.where(n > 0, n, 1)), np.nan)

    zz = np.array([k.startswith('ZZ|') for k in keys])
    ag = np.array([k in agr for k in keys])
    up = ok & (z > LIM); dn = ok & (z < -LIM)
    nu, nd = int(up.sum()), int(dn.sum())
    R = razao(nu, nd)
    zu = zonas_top(keys, up); zd = zonas_top(keys, dn)
    mov = 2 * (L2 - L2h)
    margem = {'margem_nacional_lula_menos_flavio': margem_nacional, 'votos_dos_finalistas_2t': votos_fin,
              'cauda_de_cima_votos': float(mov[up].sum()), 'cauda_de_baixo_votos': float(mov[dn].sum()),
              'liquida_votos': float(mov[up].sum() + mov[dn].sum())}
    margem['liquida_pct_da_margem_nacional'] = 100 * margem['liquida_votos'] / margem_nacional
    margem['liquida_pontos_da_fatia'] = 100 * margem['liquida_votos'] / 2 / votos_fin
    margem['votos_finalistas_nas_caudas'] = {'cima': float(n[up].sum()), 'baixo': float(n[dn].sum())}

    if R is not None and R >= 1.3 and nu >= 200 and (zu['pct_nas_top10'] or 0) >= 30:
        ver = 'SINAL'
    elif R is not None and 0.8 <= R <= 1.25:
        ver = 'SEM SINAL'
    else:
        ver = 'INCONCLUSIVO'

    # controles e sensibilidades (D7)
    rng = np.random.default_rng(SEMENTE)
    idx = np.where(ok)[0]; nn = n[idx].astype(np.int64); pp = p[idx]; ss = sd[idx]
    sims = []
    for _ in range(200):
        Ls = rng.binomial(nn, pp)
        zs = (Ls / nn - pp) / ss
        sims.append(((zs > LIM).sum(), (zs < -LIM).sum()))
    sims = np.array(sims)
    zv = z[ok]
    mad = float(np.median(np.abs(zv - np.median(zv))) * 1.4826)
    sens = {}
    for nome, mk, zx in (('principal', ok, z), ('n>=50', ok & (n >= 50), z), ('sem_exterior', ok & ~zz, z),
                         ('sem_secoes_agregadas', ok & ~ag, z), ('deixa_uma_fora', ok_loo, z_loo),
                         ('deixa_uma_fora_n>=50', ok_loo & (n >= 50), z_loo)):
        a_, b_ = contar(zx, mk)
        sens[nome] = {'secoes_com_z': int(mk.sum()), 'acima_+4': a_, 'abaixo_-4': b_, 'razao': razao(a_, b_)}
    sens['deixa_uma_fora']['pct_acima_+4_em_10_zonas'] = zonas_top(keys, ok_loo & (z_loo > LIM))['pct_nas_top10']
    limiares = {}
    for lim in (3.0, 5.0, 6.0, 8.0, 10.0):
        a_, b_ = contar(z, ok, lim)
        limiares[f'{lim:g}'] = {'acima': a_, 'abaixo': b_, 'razao': razao(a_, b_)}
    por_uf = collections.defaultdict(lambda: [0, 0, 0])
    for i in np.where(ok)[0]:
        u = keys[i].split('|')[0]; por_uf[u][0] += 1
        if z[i] > LIM: por_uf[u][1] += 1
        elif z[i] < -LIM: por_uf[u][2] += 1
    # por tamanho da seção (n)
    faixas_n = {}
    for lo, hi in ((1, 50), (50, 150), (150, 300), (300, 10 ** 6)):
        mk = ok & (n >= lo) & (n < hi); a_, b_ = contar(z, mk)
        faixas_n[f'{lo}-{hi if hi < 10**6 else "mais"}'] = {'secoes': int(mk.sum()), 'acima': a_, 'abaixo': b_, 'razao': razao(a_, b_)}
    # por fatia prevista p
    faixas_p = {}
    for lo, hi in ((0, .2), (.2, .4), (.4, .6), (.6, .8), (.8, 1.0001)):
        mk = ok & (p >= lo) & (p < hi); a_, b_ = contar(z, mk)
        faixas_p[f'{lo:.1f}-{min(hi,1):.1f}'] = {'secoes': int(mk.sum()), 'acima': a_, 'abaixo': b_, 'razao': razao(a_, b_)}

    def linha(i):
        uf, mun, zona, sec = keys[i].split('|')
        return {'secao': keys[i], 'zona': f'{uf}|{zona}', 'z': float(z[i]), 'z_deixa_uma_fora': (None if np.isnan(z_loo[i]) else float(z_loo[i])),
                'n': int(n[i]), 'L1': int(L1[i]), 'R1': int(R1[i]), 'L2': int(L2[i]), 'R2': int(R2[i]),
                'O1': int(A[i, C['O1']]), 'BN1': int(A[i, C['B1']] + A[i, C['N1']]), 'BN2': int(A[i, C['B2']] + A[i, C['N2']]),
                'comp1': int(A[i, C['comp1']]), 'comp2': int(A[i, C['comp2']]),
                'fatia_1t': (float(L1[i] / (L1[i] + R1[i])) if L1[i] + R1[i] else None), 'fatia_2t': float(f[i]),
                'p_previsto': float(p[i]), 'L2_previsto': float(L2h[i]), 'margem_movida_votos': float(mov[i]),
                'secoes_no_local': int(msz[i]), 'agregada': bool(ag[i])}
    ordem = np.where(ok)[0]
    ordem = ordem[np.lexsort((keys[ordem], -z[ordem]))]
    top30 = [linha(i) for i in ordem[:30]]
    ordem_b = np.where(ok)[0]; ordem_b = ordem_b[np.lexsort((keys[ordem_b], z[ordem_b]))]
    bot10 = [linha(i) for i in ordem_b[:10]]
    cauda_cima = [linha(i) for i in np.where(up)[0]]
    cauda_baixo = [linha(i) for i in np.where(dn)[0]]
    out = {'teste': 'F5 (Adendo 20): caudas', 'registro': 'PRE-REGISTRO-2026-10-26.md, Adendo 20, commit d976d4d',
           'conferencia_coeficientes_T8_dif_max': conf, 'identidade_previsto_soma_n_maior_desvio': ident,
           'coeficientes': {'L': rL['coef'], 'R': rR['coef']}, 'ep': {'L': rL['ep'], 'R': rR['ep']},
           'secoes_base': N, 'secoes_sozinhas_no_local': int((sozinha).sum()), 'secoes_n_zero': int(((~sozinha) & (n <= 0)).sum()),
           'secoes_p_fora_0_1': int((ok_base & ~ok).sum()), 'secoes_com_z': int(ok.sum()),
           'acima_+4': nu, 'abaixo_-4': nd, 'razao': R, 'concentracao_cima': zu, 'concentracao_baixo': zd,
           'margem': margem, 'veredito_caudas': ver,
           'dispersao': {'desvio_padrao_z': float(np.std(zv)), 'desvio_robusto_mad': mad, 'mediana_z': float(np.median(zv)),
                         'quantis_z': {q: float(np.quantile(zv, q / 100)) for q in (0.1, 1, 5, 25, 50, 75, 95, 99, 99.9)},
                         'pct_abs_z_maior_4': 100 * (nu + nd) / int(ok.sum())},
           'simulacao_contagem_limpa': {'sorteios': 200, 'semente': SEMENTE, 'media_acima_+4': float(sims[:, 0].mean()),
                                        'media_abaixo_-4': float(sims[:, 1].mean()), 'max_acima_+4': int(sims[:, 0].max()),
                                        'max_abaixo_-4': int(sims[:, 1].max())},
           'sensibilidade': sens, 'limiares': limiares, 'por_faixa_n': faixas_n, 'por_faixa_p': faixas_p,
           'por_uf': {u: {'secoes': v[0], 'acima': v[1], 'abaixo': v[2]} for u, v in sorted(por_uf.items())},
           'caudas_no_exterior': {'acima': int((up & zz).sum()), 'abaixo': int((dn & zz).sum())},
           'caudas_agregadas': {'acima': int((up & ag).sum()), 'abaixo': int((dn & ag).sum()), 'agregadas_com_z': int((ok & ag).sum())},
           'top30': top30, 'bot10': bot10}
    out['exploratorio_fora_do_registro'] = exploratorio(keys, ok, z, f, p, n, L1, R1, L2, R2, A, C, mad, linha)
    json.dump(out, open(saida, 'w'), ensure_ascii=False, indent=1)
    with gzip.open(saida.replace('.json', '_caudas_completas.json.gz'), 'wt') as fh:
        json.dump({'cima': cauda_cima, 'baixo': cauda_baixo}, fh, ensure_ascii=False)
    with open(lista, 'w') as fh:
        for r in top30 + bot10:
            fh.write(r['secao'] + '\n')
    log('acima', nu, 'abaixo', nd, 'razao', R, 'veredito', ver)


def exploratorio(keys, ok, z, f, p, n, L1, R1, L2, R2, A, C, mad, linha):
    """Fora do registro (escrito depois de ver o resultado pela letra; só pistas, sem veredito):
    (a) z recalibrado pela dispersão observada (z dividido pelo desvio robusto), limiar 4; (b) só seções longe da fronteira
    (p entre 0,1 e 0,9); (c) resíduo em pontos da fatia, n >= 100, limiares de 10, 15, 20 e 30 pontos; (d) virada bruta
    (fatia do 2º menos a do 1º turno) acima de 30 pontos para cada lado, n >= 100; (e) colapso de um finalista: seções
    com 30 ou mais votos dele no 1º turno e menos de 20% disso no 2º, para os dois lados."""
    o = {}
    zc = z / mad
    a_, b_ = contar(zc, ok)
    o['z_recalibrado'] = {'desvio_robusto': mad, 'acima_+4': a_, 'abaixo_-4': b_, 'razao': razao(a_, b_)}
    lon = ok & (p >= .1) & (p <= .9)
    a_, b_ = contar(z, lon); a2, b2 = contar(zc, lon)
    o['longe_da_fronteira_p_0,1_a_0,9'] = {'secoes': int(lon.sum()), 'z_acima_+4': a_, 'z_abaixo_-4': b_, 'razao': razao(a_, b_),
                                           'z_recal_acima_+4': a2, 'z_recal_abaixo_-4': b2, 'razao_recal': razao(a2, b2)}
    r = 100 * (f - p); m100 = ok & (n >= 100)
    o['residuo_pontos_n>=100'] = {'secoes': int(m100.sum()), 'desvio_padrao': float(np.std(r[m100])),
                                  'quantis': {q: float(np.quantile(r[m100], q / 100)) for q in (0.1, 1, 50, 99, 99.9)}}
    for lim in (10, 15, 20, 30):
        a_, b_ = contar(r, m100, lim)
        o['residuo_pontos_n>=100'][f'alem_de_{lim}'] = {'acima': a_, 'abaixo': b_, 'razao': razao(a_, b_)}
    ordem = np.where(m100)[0]
    o['maiores_residuos_pontos_n>=100'] = {
        'cima': [dict(linha(i), residuo_pontos=float(r[i])) for i in ordem[np.argsort(-r[ordem])][:15]],
        'baixo': [dict(linha(i), residuo_pontos=float(r[i])) for i in ordem[np.argsort(r[ordem])][:15]]}
    f1 = np.where(L1 + R1 > 0, L1 / np.maximum(L1 + R1, 1), np.nan)
    v = 100 * (f - f1); mv = m100 & ~np.isnan(v)
    o['virada_bruta_n>=100'] = {'media': float(np.mean(v[mv])), 'desvio_padrao': float(np.std(v[mv]))}
    for lim in (20, 30, 40):
        a_ = int((mv & (v > lim)).sum()); b_ = int((mv & (v < -lim)).sum())
        o['virada_bruta_n>=100'][f'alem_de_{lim}'] = {'para_lula': a_, 'para_flavio': b_, 'razao': razao(a_, b_)}
    col = {}
    for nome, c1, c2 in (('flavio', R1, R2), ('lula', L1, L2)):
        mk = (c1 >= 30) & (c2 < 0.2 * c1)
        col[nome] = {'secoes': int(mk.sum()), 'votos_1t': int(c1[mk].sum()), 'votos_2t': int(c2[mk].sum()),
                     'exemplos': [{'secao': keys[i], 'L1': int(L1[i]), 'R1': int(R1[i]), 'L2': int(L2[i]), 'R2': int(R2[i]),
                                   'comp1': int(A[i, C['comp1']]), 'comp2': int(A[i, C['comp2']])}
                                  for i in np.where(mk)[0][np.argsort(-(c1 - c2)[mk])][:25]],
                     'por_uf': dict(collections.Counter(keys[i].split('|')[0] for i in np.where(mk)[0]).most_common())}
    o['colapso_de_um_finalista'] = col
    return o


# ================================================================ parte 2: arquivos
CAMPOS_BWEB = ['NR_LOCAL_VOTACAO', 'QT_APTOS', 'QT_COMPARECIMENTO', 'QT_ABSTENCOES', 'DS_TIPO_URNA', 'NR_URNA_EFETIVADA',
               'CD_CARGA_1_URNA_EFETIVADA', 'CD_CARGA_2_URNA_EFETIVADA', 'CD_FLASHCARD_URNA_EFETIVADA', 'DT_CARGA_URNA_EFETIVADA',
               'DS_SECOES_AGREGADAS', 'DT_ABERTURA', 'DT_ENCERRAMENTO', 'QT_ELEI_BIOM_SEM_HABILITACAO', 'DT_EMISSAO_BU',
               'DT_BU_RECEBIDO', 'NR_JUNTA_APURADORA', 'NR_TURMA_APURADORA', 'NM_MUNICIPIO']


def ler_bweb(pasta, chaves, rotulo):
    """Linhas do cargo 1 (presidente) do bweb para as chaves pedidas, direto dos zips do TSE."""
    ufs = sorted({k.split('|')[0] for k in chaves})
    out = {}
    for uf in ufs:
        zs = sorted(glob.glob(os.path.join(pasta, f'bweb_{rotulo}_{uf}_*.zip')))
        if not zs:
            continue
        z = zipfile.ZipFile(zs[-1])
        nome = [x for x in z.namelist() if x.lower().endswith('.csv')][0]
        log('lendo', zs[-1].split('/')[-1])
        alvo = {k for k in chaves if k.startswith(uf + '|')}
        with z.open(nome) as fh:
            rd = csv.reader(io.TextIOWrapper(fh, encoding='latin1', newline=''), delimiter=';')
            cab = next(rd); ix = {c.strip().replace('SG_ UF', 'SG_UF'): i for i, c in enumerate(cab)}
            iC, iU, iM, iZ, iS = (ix[c] for c in ('CD_CARGO_PERGUNTA', 'SG_UF', 'CD_MUNICIPIO', 'NR_ZONA', 'NR_SECAO'))
            for r in rd:
                if r[iC] != '1':
                    continue
                k = f'{r[iU]}|{int(r[iM])}|{int(r[iZ])}|{int(r[iS])}'
                if k not in alvo:
                    continue
                s = out.get(k)
                if s is None:
                    s = out[k] = {c: r[ix[c]] for c in CAMPOS_BWEB if c in ix}
                    s['L'] = s['R'] = s['O'] = s['B'] = s['N'] = 0
                tv = int(r[ix['CD_TIPO_VOTAVEL']]); nv = int(r[ix['NR_VOTAVEL']]); q = int(r[ix['QT_VOTOS']])
                if tv == 2: s['B'] += q
                elif tv == 3: s['N'] += q
                elif nv == 13: s['L'] += q
                elif nv == 22: s['R'] += q
                else: s['O'] += q
    return out


RXH = re.compile(r'(\d\d/\d\d/\d{4}) (\d\d):(\d\d):(\d\d)')


def hms(s):
    return None if s is None else f'{s // 3600:02d}:{s % 3600 // 60:02d}:{s % 60:02d}'


def metricas_dia(blocos, data):
    """Leitura descritiva do log num dia (D10)."""
    ev = []
    for i, bl in enumerate(blocos):
        for l in bl:
            q = l.split('\t')
            if len(q) < 5 or not q[0].startswith(data):
                continue
            m = RXH.match(q[0])
            if m:
                ev.append((i, int(m.group(2)) * 3600 + int(m.group(3)) * 60 + int(m.group(4)), q[1], q[4]))
    if not ev:
        return None
    votos = [t for b, t, nv, m in ev if m == 'O voto do eleitor foi computado']
    hab = bio = 0; flag = {}; nb_16h = 0; nb_tempos = []
    for b, t, nv, m in ev:
        if m == 'Tipo de habilitação do eleitor [biométrica]':
            flag[b] = True
        elif m == 'Eleitor foi habilitado':
            hab += 1
            if flag.get(b):
                bio += 1
            else:
                nb_tempos.append(t)
                if t >= 16 * 3600: nb_16h += 1
            flag[b] = False
    ligada = [m[len('Urna ligada em '):] for b, t, nv, m in ev if m.startswith('Urna ligada em ')]
    pronta = [t for b, t, nv, m in ev if m == 'Urna pronta para receber votos']
    enc = [t for b, t, nv, m in ev if m.startswith('Inicio do Encerramento') or m.startswith('Início do Encerramento')]
    zer = [t for b, t, nv, m in ev if m.startswith('Imprimindo relatório [ZERÉSIMA]')]
    budat = [t for b, t, nv, m in ev if m == 'Gerando arquivo de resultado [bu.dat] + [Término]']
    modelo = sorted({m.split(': ', 1)[1] for b, t, nv, m in ev if m.startswith('Identificação do Modelo de Urna:')})
    carga = sorted({m for b, t, nv, m in ev if m.startswith('Modo de carga da UE')})
    cont = [f'{hms(t)} {m}' for b, t, nv, m in ev if 'ontingência' in m]
    erros = [f'{hms(t)} {m}' for b, t, nv, m in ev if nv == 'ERRO']
    gaps = np.diff(votos) if len(votos) > 1 else np.array([])
    return {'blocos_de_log': len({b for b, *_ in ev}), 'urna_ligada': ligada[:4], 'vezes_ligada': len(ligada),
            'modelo': modelo, 'modo_de_carga': carga, 'zeresima': hms(zer[0] if zer else None),
            'pronta': hms(pronta[0] if pronta else None), 'primeiro_voto': hms(votos[0] if votos else None),
            'ultimo_voto': hms(votos[-1] if votos else None), 'inicio_encerramento': hms(enc[-1] if enc else None),
            'bu_dat_gerado': hms(budat[-1] if budat else None), 'votos_log': len(votos),
            'votos_por_hora': dict(sorted(collections.Counter(f'{t // 3600:02d}h' for t in votos).items())),
            'votos_depois_17h': sum(1 for t in votos if t >= 17 * 3600),
            'intervalo_mediano_entre_votos_s': (float(np.median(gaps)) if len(gaps) else None),
            'menor_intervalo_entre_votos_s': (int(gaps.min()) if len(gaps) else None),
            'habilitados': hab, 'habilitados_biometria': bio, 'fracao_biometrica': (bio / hab if hab else None),
            'habilitados_sem_biometria': hab - bio, 'sem_biometria_depois_16h': nb_16h,
            'sem_biometria_por_hora': dict(sorted(collections.Counter(f'{t // 3600:02d}h' for t in nb_tempos).items())),
            'contingencia_linhas': cont[:6], 'erros': len(erros), 'erros_amostra': erros[:6]}


def arquivos(parcial, pasta, arq_assin, zips2t, zips1t, arq_secoes, saida_json, saida_txt):
    from decodificar import ler_bu, bu_para_secao, ler_rdv, rdv_para_bu, ler_log, _linhas_log
    from lib import carregar
    P = json.load(open(parcial))
    alvo = [('cima', r) for r in P['top30']] + [('baixo', r) for r in P['bot10']]
    chaves = [r['secao'] for _, r in alvo]
    t = open(arq_assin).read(); assin = json.loads(t[t.find('{'):])
    falhas_por = collections.defaultdict(list)
    for fl in assin.get('falhas', []):
        falhas_por[fl[0]].append(fl[1:])
    bw2 = ler_bweb(zips2t, chaves, '2t'); bw1 = ler_bweb(zips1t, chaves, '1t')
    base = carregar(arq_secoes)
    res = []
    for lado, r in alvo:
        k = r['secao']; uf, mun, zona, sec = k.split('|')
        d = os.path.join(pasta, uf.lower(), f'{int(mun):05d}', f'{int(zona):04d}', f'{int(sec):04d}')
        fs = sorted(os.listdir(d)) if os.path.isdir(d) else []
        o = {'secao': k, 'lado': lado, 'z': r['z'], 'n': r['n'], 'fatia_1t': r['fatia_1t'], 'fatia_2t': r['fatia_2t'],
             'p_previsto': r['p_previsto'], 'L1': r['L1'], 'R1': r['R1'], 'L2': r['L2'], 'R2': r['R2'],
             'comp1': r['comp1'], 'comp2': r['comp2'], 'O1': r['O1'], 'BN1': r['BN1'], 'BN2': r['BN2'],
             'secoes_no_local': r['secoes_no_local'], 'agregada': r['agregada'], 'arquivos': [f for f in fs if f != 'aux.json'],
             'sem_aux': 'SEM_AUX' in fs}
        b2 = bw2.get(k); b1 = bw1.get(k)
        o['bweb_2t'] = b2; o['bweb_1t'] = b1
        bus = [f for f in fs if f.endswith('-bu.dat')]; rdvs = [f for f in fs if f.endswith('-rdv.dat')]
        logs = [f for f in fs if f.endswith('-log.jez')]; vscs = [f for f in fs if f.endswith('-vota.vsc')]
        sinais = []
        bu = None
        if bus:
            s, g = bu_para_secao(ler_bu(os.path.join(d, bus[-1])))
            bu = s
            o['bu'] = {x: s[x] for x in ('urna', 'apt', 'comp', 'L', 'R', 'O', 'B', 'N', 'ab', 'enc')}
            if b2:
                comp = {'urna': int(b2['NR_URNA_EFETIVADA'] or 0), 'apt': int(b2['QT_APTOS']), 'comp': int(b2['QT_COMPARECIMENTO']),
                        'L': b2['L'], 'R': b2['R'], 'B': b2['B'], 'N': b2['N']}
                dif = {x: [s[x], comp[x]] for x in comp if s[x] != comp[x]}
                o['bu_vs_bweb_diferencas'] = dif
                o['bu_igual_bweb'] = not dif
                if dif: sinais.append('boletim diferente do bweb')
            else:
                o['bu_igual_bweb'] = None
            bb = base.get(k, {}).get('2', {})
            o['bu_igual_base_secoes2026'] = all(s[x] == bb.get(x) for x in ('urna', 'apt', 'comp', 'L', 'R', 'B', 'N'))
        else:
            o['bu_igual_bweb'] = None
        if rdvs and bu:
            rv = rdv_para_bu(ler_rdv(os.path.join(d, rdvs[-1]))).get(1, collections.Counter())
            o['rdv'] = {x: int(rv.get(x, 0)) for x in ('L', 'R', 'O', 'B', 'N', 'total', 'nulo_tipo6')}
            dif = {x: [int(rv.get(x, 0)), bu[x]] for x in ('L', 'R', 'O', 'B', 'N') if int(rv.get(x, 0)) != bu[x]}
            o['rdv_vs_bu_diferencas'] = dif; o['rdv_igual_bu'] = not dif
            if dif: sinais.append('RDV diferente do boletim')
        else:
            o['rdv_igual_bu'] = None
        if logs:
            caminho = os.path.join(d, logs[-1])
            L2 = ler_log(caminho, D2); L1 = ler_log(caminho, D1)
            o['T3_2t'] = {x: L2[x] for x in ('logs_no_pacote', 'computados', 'habilitados', 'A2_antes', 'A2_depois', 'A3_sem_habilitacao',
                                             'A4_menos_2s', 'A5_rajadas', 'maior_sequencia_rapida', 'dur_mediana', 'dur_min',
                                             'contingencia', 'urnas_no_log', 'erros')}
            o['T3_1t_mesma_urna'] = {x: L1[x] for x in ('logs_no_pacote', 'computados', 'habilitados', 'A2_antes', 'A2_depois',
                                                        'A3_sem_habilitacao', 'A4_menos_2s', 'A5_rajadas', 'maior_sequencia_rapida',
                                                        'dur_mediana', 'contingencia')}
            comp_ref = bu['comp'] if bu else (int(b2['QT_COMPARECIMENTO']) if b2 else None)
            o['votos_log_igual_comparecimento'] = (L2['computados'] == comp_ref) if comp_ref is not None else None
            if comp_ref is not None and L2['computados'] != comp_ref: sinais.append('votos no log diferentes do comparecimento')
            for a in ('A2_antes', 'A2_depois', 'A3_sem_habilitacao', 'A4_menos_2s', 'A5_rajadas'):
                if L2[a]: sinais.append(f'anomalia {a}')
            blocos = _linhas_log(caminho)
            o['log_2t'] = metricas_dia(blocos, D2)
            o['log_1t'] = metricas_dia(blocos, D1)
            # o comparecimento do 1º turno no log, quando é a mesma urna
            if o['log_1t'] and b1:
                o['log_1t_votos_igual_comp_1t'] = o['log_1t']['votos_log'] == int(b1['QT_COMPARECIMENTO'])
        else:
            o['votos_log_igual_comparecimento'] = None
        if vscs:
            fl = falhas_por.get(k, [])
            o['assinatura_falhas'] = fl; o['assinatura_ok'] = not fl
            if fl: sinais.append('assinatura inválida')
        else:
            o['assinatura_ok'] = None
        o['faltando'] = [x for x, v in (('bu', bus), ('rdv', rdvs), ('log', logs), ('vsc', vscs)) if not v]
        o['sinais'] = sinais
        res.append(o)
    com_sinal = [o['secao'] for o in res if o['sinais']]
    ver_arq = 'SINAL' if com_sinal else 'SEM SINAL'
    out = dict(P)
    out['arquivos'] = {'secoes': len(res), 'assinaturas_contagem': assin.get('contagem'), 'assinaturas_falhas': assin.get('falhas'),
                       'secoes_com_sinal': com_sinal, 'veredito_arquivos': ver_arq,
                       'faltando': {o['secao']: o['faltando'] for o in res if o['faltando']}, 'por_secao': res}
    json.dump(out, open(saida_json, 'w'), ensure_ascii=False, indent=1)
    open(saida_txt, 'w').write(texto(out))


def _perfil_log(caminho, _linhas_log):
    out = {}
    for dia in (D2, D1):
        pronta = None; votos = []
        for b in _linhas_log(caminho):
            for l in b:
                q = l.split('\t')
                if len(q) < 5 or not q[0].startswith(dia):
                    continue
                t = int(q[0][11:13]) * 3600 + int(q[0][14:16]) * 60 + int(q[0][17:19])
                if q[4] == 'Urna pronta para receber votos' and pronta is None:
                    pronta = t
                elif q[4] == 'O voto do eleitor foi computado':
                    votos.append(t)
        if pronta is not None and len(votos) >= 30:
            v = np.array(votos)
            out[dia] = float(np.mean(v < pronta + 5 * 3600))
    return out


def perfil(saida_json, pasta_amostra, pasta_f5, arq_secoes, saida_txt):
    """Exploratório (fora do registro, escrito depois de ler os logs das 40): fração dos votos do dia nas 5 primeiras horas
    depois de "urna pronta", no 2º e no 1º turno, nas 40 seções e na amostra de 3.897 logs; e, na amostra, a virada de Lula
    (pontos da fatia entre os finalistas, 2º menos 1º turno) das seções com 85% ou mais dos votos nas 5 primeiras horas."""
    from decodificar import _linhas_log
    from lib import carregar
    R = json.load(open(saida_json)); d = carregar(arq_secoes)

    def ler(pasta):
        out = {}
        for lg in sorted(glob.glob(os.path.join(pasta, '*/*/*/*/*-log.jez'))):
            uf, m, z, s = os.path.dirname(lg).split('/')[-4:]
            k = f'{uf.upper()}|{int(m)}|{int(z)}|{int(s)}'
            if k not in out:
                out[k] = _perfil_log(lg, _linhas_log)
        return out
    res = {}
    for nome, pasta in (('amostra', pasta_amostra), ('F5_40', pasta_f5)):
        log('perfil', nome); pf = ler(pasta); r = {}
        for dia in (D2, D1):
            f = np.array([v[dia] for v in pf.values() if dia in v])
            r[dia] = {'secoes': int(len(f)), 'media': float(f.mean()), 'p90': float(np.quantile(f, .9)), 'p99': float(np.quantile(f, .99)),
                      'secoes_com_90pct_ou_mais': int((f >= .9).sum())}
        r['concentradas_85pct_2t'] = [[k, round(v[D2], 3), round(v.get(D1, float('nan')), 3)] for k, v in pf.items() if v.get(D2, 0) >= .85]
        if nome == 'amostra':
            vir = []
            for k, v in pf.items():
                s = d.get(k)
                if D2 in v and s and '1' in s and '2' in s and s['1']['L'] + s['1']['R'] > 0 and s['2']['L'] + s['2']['R'] > 0:
                    a, b = s['1'], s['2']
                    vir.append((v[D2] >= .85, 100 * (b['L'] / (b['L'] + b['R']) - a['L'] / (a['L'] + a['R']))))
            hi = [x for c, x in vir if c]; lo = [x for c, x in vir if not c]
            r['virada_lula_concentradas'] = {'secoes': len(hi), 'media': float(np.mean(hi)) if hi else None}
            r['virada_lula_demais'] = {'secoes': len(lo), 'media': float(np.mean(lo))}
        res[nome] = r
    R['exploratorio_perfil_horario'] = res
    json.dump(R, open(saida_json, 'w'), ensure_ascii=False, indent=1)
    open(saida_txt, 'w').write(texto(R))


# ================================================================ texto
def fn(x, nd=2):
    if x is None: return '-'
    if isinstance(x, float) and (x != x): return '-'
    s = f'{x:,.{nd}f}'
    return s.replace(',', 'X').replace('.', ',').replace('X', '.')


def fi(x):
    return '-' if x is None else f'{int(x):,}'.replace(',', '.')


def texto(R):
    L = []; w = L.append
    w('F5 (Adendo 20): caudas, seções que destoam do previsto pelo próprio 1º turno')
    w('Registro: PRE-REGISTRO-2026-10-26.md, Adendo 20 (commit d976d4d, 30/10/2026 12:11:50 UTC). Script: scripts/analisar_F5.py.')
    w('')
    w('Letra do registro')
    w('- Previsão pela regressão do T8 com efeito fixo de local; z = (fatia observada - p) / raiz(p(1-p)/n), n = votos dos finalistas no 2º turno.')
    w('- Sinal: seções com z > +4 em número de pelo menos 1,3 vez as com z < -4, com 200 ou mais acima de +4, e pelo menos 30% das de')
    w('  cima em até 10 zonas. Sem sinal: razão entre 0,8 e 1,25. Entre os dois: inconclusivo. Relatar a margem líquida movida.')
    w('- Arquivos das 30 de maior z e das 10 de menor z. Sinal no arquivo: assinatura inválida, boletim diferente do bweb, RDV diferente')
    w('  do boletim, votos no log diferentes do comparecimento, ou anomalia A2 a A5 do T3, em qualquer uma delas.')
    w('')
    w('Regressão (reproduz o T8/T14 gravado): diferença máxima dos coeficientes contra resultados/T7_T14_bweb.json: '
      f"Lula {R['conferencia_coeficientes_T8_dif_max']['L']:.1e}, Flávio {R['conferencia_coeficientes_T8_dif_max']['R']:.1e}.")
    w(f"Identidade L2 previsto + R2 previsto = n: maior desvio {R['identidade_previsto_soma_n_maior_desvio']:.1e} voto.")
    w(f"Seções na base: {fi(R['secoes_base'])}; sozinhas no local (sem previsão própria, D2): {fi(R['secoes_sozinhas_no_local'])}; "
      f"n = 0: {fi(R['secoes_n_zero'])}; p fora de (0,1) (D3): {fi(R['secoes_p_fora_0_1'])}; com z: {fi(R['secoes_com_z'])}.")
    w('')
    w('Resultado pela letra')
    w(f"- Acima de +4: {fi(R['acima_+4'])}. Abaixo de -4: {fi(R['abaixo_-4'])}. Razão: {fn(R['razao'], 3)}.")
    cu = R['concentracao_cima']; cb = R['concentracao_baixo']
    w(f"- Concentração das de cima: {fi(cu['secoes'])} seções em {fi(cu['zonas_distintas'])} zonas; as 10 zonas com mais têm {fn(cu['pct_nas_top10'], 1)}%.")
    w('  ' + '; '.join(f'{z} {n}' for z, n in cu['top10']))
    w(f"- Espelho (as de baixo): {fi(cb['secoes'])} seções em {fi(cb['zonas_distintas'])} zonas; 10 zonas com mais: {fn(cb['pct_nas_top10'], 1)}%.")
    w('  ' + '; '.join(f'{z} {n}' for z, n in cb['top10']))
    m = R['margem']
    w(f"- Margem movida (D5): cauda de cima {fi(m['cauda_de_cima_votos'])} votos de margem para Lula; cauda de baixo {fi(m['cauda_de_baixo_votos'])};")
    w(f"  líquida {fi(m['liquida_votos'])} votos = {fn(m['liquida_pct_da_margem_nacional'], 2)}% da margem nacional de {fi(m['margem_nacional_lula_menos_flavio'])}"
      f" ({fn(m['liquida_pontos_da_fatia'], 3)} ponto da fatia de Lula entre os finalistas).")
    w(f"- VEREDITO (caudas): {R['veredito_caudas']}.")
    w('')
    w('Controles e sensibilidades (descritivos, D7)')
    dsp = R['dispersao']; sm = R['simulacao_contagem_limpa']
    w(f"- Contagem limpa simulada (binomial com o mesmo p, 200 sorteios): média de {fn(sm['media_acima_+4'], 1)} acima de +4 e {fn(sm['media_abaixo_-4'], 1)}"
      f" abaixo de -4 (máximos {sm['max_acima_+4']} e {sm['max_abaixo_-4']}).")
    w(f"- Dispersão de z: desvio-padrão {fn(dsp['desvio_padrao_z'])}, robusto (MAD) {fn(dsp['desvio_robusto_mad'])}, mediana {fn(dsp['mediana_z'], 3)}; "
      f"|z| > 4 em {fn(dsp['pct_abs_z_maior_4'])}% das seções. Quantis: " + ', '.join(f'{k}%: {fn(v)}' for k, v in dsp['quantis_z'].items()))
    for k, v in R['sensibilidade'].items():
        extra = f", 10 zonas: {fn(v['pct_acima_+4_em_10_zonas'], 1)}%" if 'pct_acima_+4_em_10_zonas' in v else ''
        w(f"  {k:24s} seções {fi(v['secoes_com_z']):>9s} | acima {fi(v['acima_+4']):>7s} | abaixo {fi(v['abaixo_-4']):>7s} | razão {fn(v['razao'], 3)}{extra}")
    w('- Outros limiares (versão principal): ' + '; '.join(f"|z|>{k}: {fi(v['acima'])} contra {fi(v['abaixo'])} (razão {fn(v['razao'], 2)})" for k, v in R['limiares'].items()))
    w('- Por tamanho (n): ' + '; '.join(f"{k}: {fi(v['acima'])}/{fi(v['abaixo'])} (razão {fn(v['razao'], 2)}, {fi(v['secoes'])} seções)" for k, v in R['por_faixa_n'].items()))
    w('- Por fatia prevista p: ' + '; '.join(f"{k}: {fi(v['acima'])}/{fi(v['abaixo'])} (razão {fn(v['razao'], 2)})" for k, v in R['por_faixa_p'].items()))
    w('- Por UF (acima/abaixo): ' + '; '.join(f"{u} {v['acima']}/{v['abaixo']}" for u, v in R['por_uf'].items()))
    w(f"- No exterior: {R['caudas_no_exterior']['acima']} acima e {R['caudas_no_exterior']['abaixo']} abaixo. Seções agregadas: "
      f"{R['caudas_agregadas']['acima']} acima e {R['caudas_agregadas']['abaixo']} abaixo (de {fi(R['caudas_agregadas']['agregadas_com_z'])} agregadas com z).")
    E = R.get('exploratorio_fora_do_registro')
    if E:
        w('')
        w('Exploratório, fora do registro (escrito depois de ver o resultado pela letra; pistas, sem veredito)')
        zr = E['z_recalibrado']; lf = E['longe_da_fronteira_p_0,1_a_0,9']; rp = E['residuo_pontos_n>=100']; vb = E['virada_bruta_n>=100']
        w(f"- z dividido pelo desvio robusto ({fn(zr['desvio_robusto'], 3)}): {zr['acima_+4']} acima de +4 e {zr['abaixo_-4']} abaixo de -4 (razão {fn(zr['razao'], 2)}).")
        w(f"- Só seções longe da fronteira (p de 0,1 a 0,9; {fi(lf['secoes'])} seções): z bruto {lf['z_acima_+4']} contra {lf['z_abaixo_-4']} (razão {fn(lf['razao'], 2)});"
          f" recalibrado {lf['z_recal_acima_+4']} contra {lf['z_recal_abaixo_-4']} (razão {fn(lf['razao_recal'], 2)}).")
        w(f"- Resíduo em pontos da fatia, n >= 100 ({fi(rp['secoes'])} seções): desvio-padrão {fn(rp['desvio_padrao'])} ponto; "
          + '; '.join(f"além de {k.split('_')[-1]}: {v['acima']} para Lula e {v['abaixo']} para Flávio" for k, v in rp.items() if k.startswith('alem_de')))
        w(f"- Virada bruta (fatia 2T menos 1T), n >= 100: média {fn(vb['media'])} pontos, desvio {fn(vb['desvio_padrao'])}; "
          + '; '.join(f"além de {k.split('_')[-1]}: {v['para_lula']} para Lula e {v['para_flavio']} para Flávio" for k, v in vb.items() if k.startswith('alem_de')))
        for lado in ('cima', 'baixo'):
            w(f"- Maiores resíduos em pontos ({'a favor de Lula' if lado == 'cima' else 'a favor de Flávio'}), n >= 100:")
            for x in E['maiores_residuos_pontos_n>=100'][lado][:8]:
                w(f"    {x['secao']:20s} {fn(x['residuo_pontos'], 1):>6s} pontos | {x['L1']}/{x['R1']} -> {x['L2']}/{x['R2']} | comp {x['comp1']}->{x['comp2']} | BN {x['BN1']}->{x['BN2']} | z {fn(x['z'], 1)}")
        for nome, v in E['colapso_de_um_finalista'].items():
            w(f"- Colapso de {({'flavio': 'Flávio', 'lula': 'Lula'})[nome]} (30 ou mais votos no 1T e menos de 20% disso no 2T): {v['secoes']} seção(ões), {v['votos_1t']} -> {v['votos_2t']} votos: "
              + '; '.join(f"{x['secao']} {x['L1']}/{x['R1']} -> {x['L2']}/{x['R2']} (comp {x['comp1']}->{x['comp2']})" for x in v['exemplos']))
    w('')
    w('As 30 de maior z e as 10 de menor z')
    w('  seção                    z      n   fatia1T fatia2T  p prev | L1/R1 -> L2/R2 | comp1->comp2 | O1 BN1->BN2 | locais')
    for r in R['top30'] + R['bot10']:
        w(f"  {r['secao']:22s} {fn(r['z'], 1):>6s} {r['n']:5d}  {fn(100 * (r['fatia_1t'] or 0), 1):>6s} {fn(100 * r['fatia_2t'], 1):>6s} {fn(100 * r['p_previsto'], 1):>6s} |"
          f" {r['L1']}/{r['R1']} -> {r['L2']}/{r['R2']} | {r['comp1']}->{r['comp2']} | {r['O1']} {r['BN1']}->{r['BN2']} | {r['secoes_no_local']}{' agregada' if r['agregada'] else ''}")
    A = R.get('arquivos')
    if A:
        w('')
        w('Arquivos de urna das 40 seções')
        c = A['assinaturas_contagem'] or {}
        w(f"- Assinaturas (verificar_assinaturas.py): seções com vsc {c.get('secoes_com_vsc')}, bloco de hardware ok {c.get('bloco_hw_assinatura_ok')},"
          f" arquivos com assinatura ok {c.get('assinatura_arquivo_ok')} de {c.get('arquivos_listados')}, resumos ok {c.get('resumo_ok')} de"
          f" {c.get('arquivos_baixados_conferidos')}, urna do certificado igual à do boletim {c.get('urna_cert_igual_bu')}; falhas: {len(A['assinaturas_falhas'] or [])}.")
        ps = A['por_secao']
        def cnt(campo, val=True): return sum(1 for o in ps if o.get(campo) is val)
        w(f"- Boletim igual ao bweb: {cnt('bu_igual_bweb')} de {sum(1 for o in ps if o.get('bu_igual_bweb') is not None)}. RDV igual ao boletim: "
          f"{cnt('rdv_igual_bu')} de {sum(1 for o in ps if o.get('rdv_igual_bu') is not None)}. Votos no log = comparecimento: "
          f"{cnt('votos_log_igual_comparecimento')} de {sum(1 for o in ps if o.get('votos_log_igual_comparecimento') is not None)}.")
        a2 = {a: sum(o.get('T3_2t', {}).get(a, 0) for o in ps) for a in ('A2_antes', 'A2_depois', 'A3_sem_habilitacao', 'A4_menos_2s', 'A5_rajadas')}
        w('- Anomalias do T3 no 2º turno, somadas nas 40: ' + ', '.join(f'{k} {v}' for k, v in a2.items()) + '.')
        if A['faltando']:
            w('- Arquivos que não vieram: ' + '; '.join(f"{k}: {', '.join(v)}" for k, v in A['faltando'].items()))
        w(f"- Seções com sinal no arquivo: {len(A['secoes_com_sinal'])}" + (': ' + ', '.join(A['secoes_com_sinal']) if A['secoes_com_sinal'] else '') + '.')
        w(f"- VEREDITO (arquivos): {A['veredito_arquivos']}.")
        w('')
        w('O que o log mostra em cada uma (horas no relógio da urna; 2º turno, e entre colchetes o 1º turno na mesma urna quando o log traz)')
        for o in ps:
            g = o.get('log_2t') or {}; g1 = o.get('log_1t') or {}
            b2 = o.get('bweb_2t') or {}; b1 = o.get('bweb_1t') or {}
            fb = g.get('fracao_biometrica'); fb1 = g1.get('fracao_biometrica')
            w(f"  {o['secao']} ({o['lado']}, z {fn(o['z'], 1)}): {', '.join(o['sinais']) if o['sinais'] else 'sem sinal'}; modelo {','.join(g.get('modelo') or []) or '-'};"
              f" ligada {', '.join(x[-8:] for x in (g.get('urna_ligada') or [])[:3]) or '-'} (x{g.get('vezes_ligada')}); zerésima {g.get('zeresima')};"
              f" pronta {g.get('pronta')}; votos {g.get('primeiro_voto')} a {g.get('ultimo_voto')} ({g.get('votos_log')} no log, comp {o['comp2']});"
              f" depois das 17h {g.get('votos_depois_17h')}; encerramento {g.get('inicio_encerramento')}; contingência {'sim' if (o.get('T3_2t') or {}).get('contingencia') else 'não'};"
              f" biometria {fn(100 * fb, 1) if fb is not None else '-'}% [{fn(100 * fb1, 1) if fb1 is not None else '-'}%];"
              f" sem biometria {g.get('habilitados_sem_biometria')} (depois das 16h {g.get('sem_biometria_depois_16h')}) [{g1.get('habilitados_sem_biometria')}];"
              f" bweb sem biometria {b2.get('QT_ELEI_BIOM_SEM_HABILITACAO')} [{b1.get('QT_ELEI_BIOM_SEM_HABILITACAO')}];"
              f" urna {b2.get('NR_URNA_EFETIVADA')} [{b1.get('NR_URNA_EFETIVADA')}]; carga {b2.get('DT_CARGA_URNA_EFETIVADA')};"
              f" votos por hora {g.get('votos_por_hora')}; menor intervalo entre votos {g.get('menor_intervalo_entre_votos_s')} s;"
              f" maior sequência rápida {(o.get('T3_2t') or {}).get('maior_sequencia_rapida')}; erros {g.get('erros')}"
              f" ({'; '.join(sorted({e[9:] for e in g.get('erros_amostra') or []})) or '-'}); município {b2.get('NM_MUNICIPIO')}")
        w('  (No exterior a urna não usa biometria; "sem biometria" do log inclui quem não tem biometria cadastrada, por isso é maior')
        w('  ou igual ao QT_ELEI_BIOM_SEM_HABILITACAO do bweb, que conta só quem tinha biometria e foi liberado sem ela.)')
    P = R.get('exploratorio_perfil_horario')
    if P:
        w('')
        w('Exploratório, fora do registro: fração dos votos do dia nas 5 primeiras horas depois de "urna pronta"')
        for nome, r in P.items():
            for dia in (D2, D1):
                x = r[dia]
                w(f"- {nome} {dia}: {x['secoes']} seções, média {fn(100 * x['media'], 1)}%, p90 {fn(100 * x['p90'], 1)}%, p99 {fn(100 * x['p99'], 1)}%,"
                  f" com 90% ou mais: {x['secoes_com_90pct_ou_mais']}")
            w('  85% ou mais no 2º turno [2º, 1º turno]: ' + '; '.join(f'{k} [{fn(100 * a, 1)}%, {fn(100 * b, 1)}%]' for k, a, b in r['concentradas_85pct_2t']))
            if 'virada_lula_concentradas' in r:
                w(f"  Virada de Lula na amostra: concentradas {fn(r['virada_lula_concentradas']['media'], 2)} pontos ({r['virada_lula_concentradas']['secoes']} seções);"
                  f" demais {fn(r['virada_lula_demais']['media'], 2)} pontos ({r['virada_lula_demais']['secoes']}).")
    w('')
    w('Desvios declarados (decisões que o registro não fixa, tomadas antes de calcular; ver o docstring do script): D1 previsto dentro da amostra')
    w('(efeito do local com a própria seção), deixa uma fora ao lado; D2 seções sozinhas no local fora; D3 p fora de (0,1) fora; D4 zona = UF +')
    w('número, exterior incluído; D5 margem = 2 x (L2 - L2 previsto); D6 ordem pelo z principal; D7 controles descritivos; D8 concentração')
    w('pelas 10 zonas com mais seções; D9 comparações dos arquivos; D10 leitura do log; D11 razão abaixo de 0,8 (não prevista no registro)')
    w('fica INCONCLUSIVO pela regra do código, escrita antes de rodar. Os blocos "exploratório" foram escritos depois de ver o resultado.')
    return '\n'.join(L) + '\n'


if __name__ == '__main__':
    if sys.argv[1] == 'caudas':
        caudas(*sys.argv[2:7])
    elif sys.argv[1] == 'arquivos':
        arquivos(*sys.argv[2:10])
    elif sys.argv[1] == 'perfil':
        perfil(*sys.argv[2:7])
    elif sys.argv[1] == '--texto':
        print(texto(json.load(open(sys.argv[2]))), end='')
