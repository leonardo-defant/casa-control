"""P2 do pré-registro, Adendo 26 (commit 5174ff5, 07/11/2026 13:57:56 UTC): métricas de 2014, 2018, 2022 e 2026 lado a
lado, para checar a postagem "2014 parecida com 2026" (@FelipeCecilio_, X). Sem veredito de fraude.
Escrito antes de calcular qualquer métrica de P2 (07/11/2026, cerca de 14h UTC).

O QUE O REGISTRO FIXA
- Base por seção dos quatro anos, sem o exterior.
- (a) fatia do candidato do PT nos válidos do 2º turno; (b) variação da fatia do PT entre os finalistas, do 1º para o 2º
  turno; (c) quem liderou o 1º turno; (d) variação do comparecimento e (e) de brancos mais nulos, do 1º para o 2º turno;
  (f) parte da margem do PT que veio do Nordeste; (g) correlação, por município, da fatia do PT no 2º turno de 2026 com a
  de cada outro ano; (h) dispersão da fatia do PT entre seções (desvio-padrão; fração de seções acima de 80% e abaixo de
  20%); (i) curva por faixa e erro das pesquisas, do F21, sem recalcular.
- Semelhança: em cada métrica, o ano mais perto de 2026. "2014 parecida" naquela métrica se 2014 for o mais perto.
  Relatar a contagem.
- Leitura fixada antes: semelhança numa métrica de resultado, composição ou comportamento (todas de P2) não é indício de
  fraude, porque eleições limpas com a mesma geografia se parecem.

SABIDO ANTES DE ESCREVER ESTE SCRIPT (não é resultado de P2)
- Os totais oficiais com exterior (resultados/contexto_virada_2t.txt) já mostravam, de forma aproximada, (a) a (e):
  Dilma liderou o 1º turno de 2014, Bolsonaro o de 2018, Lula o de 2022 e Flávio o de 2026; o comparecimento caiu do 1º
  para o 2º turno em 2014 e 2018 e subiu em 2022 e 2026. O F21 (Adendo 23) já dava a curva por faixa e o erro das
  pesquisas, que aqui só são copiados.

O QUE O REGISTRO NÃO FIXA, DECIDIDO AQUI ANTES DE CALCULAR (relatado como desvio)
D1. Universo de cada ano: as seções da base daquele ano com 1º e 2º turno ('1' e '2'), com UF diferente de ZZ. Os anos
    não são ligados entre si (cada ano usa todas as suas seções). Seções com um turno anulado (tipo "Anulada") ficam como
    a base as registra (votos do turno anulado como nulo); são contadas e relatadas. Seções com L+R = 0 no 2º turno saem
    só de (h), onde a fatia não existe. O registro não pede ligar as seções entre anos e P2 não faz isso.
D2. 2026, 1º turno: os votos do 28 (candidato cassado, campo c28, que a base também soma em O) contam como nulo e não
    como válido, como no total oficial (válidos oficiais = L+R+O-c28; nulos oficiais = N+c28). Vale para (c) e (e). Em
    2014, 2018 e 2022 não há c28. Se houver c28 no 2º turno de algum ano, a mesma regra vale.
D3. (a) fatia = L2/(L2+R2) no universo (no 2º turno não há outros nominais, então é a fatia nos válidos). Conferência:
    a mesma conta na base com o exterior e com todas as seções com 2º turno, contra o oficial (2014 51,64; 2018 44,87;
    2022 50,90; 2026 51,79). Relatados os dois (sem exterior e oficial).
D4. (b) variação = 100 x (L2/(L2+R2) - L1/(L1+R1)), somas do universo, em pontos percentuais.
D5. (c) líder = o finalista (candidato do PT ou adversário) com mais votos no 1º turno, no universo; margem em votos e
    em pontos dos válidos do 1º turno. Semelhança: "igual" se o líder é do mesmo lado que em 2026 (o adversário do PT);
    todos os anos "iguais" empatam como mais perto; a margem não desempata (é relatada).
D6. (d) comparecimento: em votos, comp2 - comp1; em pontos dos aptos, 100 x (comp2/apt2 - comp1/apt1), com os aptos de
    cada turno somados no universo. Semelhança pela variação em pontos dos aptos (o eleitorado muda de tamanho entre os
    anos e a variação em votos acompanha esse tamanho); a variação em votos entra só na contagem desagregada.
D7. (e) brancos mais nulos: o mesmo de D6 com B+N (+c28, D2).
D8. (f) Nordeste = AL, BA, CE, MA, PB, PE, PI, RN, SE. Margem do PT no 2º turno = L2 - R2. Parte do Nordeste =
    100 x margem do Nordeste / margem total (sem exterior). Margem fora do Nordeste = margem total - margem do Nordeste,
    em votos e em pontos dos válidos do 2º turno do universo; também a contribuição do Nordeste em pontos desses válidos.
    Semelhança pela parte (a letra do registro). Se a margem total for negativa (o PT perdeu, caso de 2018), a parte fica
    negativa e não é uma fração; a conta e a distância ficam as mesmas, sem reinterpretar. A margem fora do Nordeste em
    pontos entra só na contagem desagregada.
D9. (g) município = UF|código do município da base (código do TSE, o mesmo nos quatro anos). Fatia do PT no 2º turno do
    município = soma de L2 / soma de (L2+R2) das seções do universo. Para cada par (2026, ano): municípios presentes nos
    dois anos com L2+R2 > 0 nos dois. Pearson bruta (cada município peso 1) e ponderada pelos válidos do 2º turno de 2026
    do município. Erro-padrão por bootstrap de municípios (2.000 reamostragens, semente 20261107). Semelhança pela maior
    correlação bruta; a ponderada entra só na contagem desagregada. Robustez: nos municípios presentes nos quatro anos,
    diferença entre a maior correlação e a de cada outro ano, com erro-padrão por bootstrap pareado (mesma semente).
D10. (h) fatia por seção s = L2/(L2+R2), seções do universo com L2+R2 > 0. Desvio-padrão simples (cada seção peso 1,
    população, ddof 0) e ponderado pelos válidos da seção (em torno da média ponderada, que é a fatia agregada). Frações
    de seções com s > 0,80 e com s < 0,20 (desigualdade estrita), sobre o número de seções. Semelhança pelo
    desvio-padrão simples (a seção é a unidade, como nas frações); os outros três números entram só na contagem
    desagregada.
D11. (i) copiado de resultados/F21_serie_anos.json, sem recalcular: (i1) curva = d por faixa de força do adversário (4
    faixas, série principal do F21, 331.087 seções, com o universo do F21, que não é o de P2); distância ao ano de 2026 =
    média das diferenças absolutas de d nas 4 faixas; (i2) erro médio das pesquisas no candidato do PT (urna menos
    pesquisa; 2026 só Datafolha); distância absoluta. (i) conta como duas métricas, porque o registro nomeia ali duas
    medidas diferentes.
D12. Contagem principal: 10 métricas (a, b, c, d, e, f, g, h, i1, i2), cada uma pelo número primário de D3 a D11.
    Empate exato (diferença de distância abaixo de 1e-12): todos os anos empatados são "mais perto"; 2014 conta se estiver
    entre eles, e o empate é marcado. Contagem desagregada (robustez, fixada aqui): cada número separado, 17 números (a;
    b; c; d em votos; d em pontos; e em votos; e em pontos; f parte; f fora do Nordeste em pontos; g bruta; g ponderada;
    h desvio simples; h desvio ponderado; h acima de 80%; h abaixo de 20%; i1; i2).
D13. "Diferente de modo marcante" (ao lado, sem mudar a leitura), regra fixada aqui: (1) categoria diferente: lado do
    líder do 1º turno (c) e lado do vencedor do 2º turno (sinal de a - 50); (2) sinal diferente entre 2014 e 2026 numa
    variação, margem ou erro com sinal: (b); (d) em votos e em pontos; (e) em votos e em pontos; parte do Nordeste e
    margem fora do Nordeste (f); d de cada faixa de (i1); (i2). Diferença de nível sem troca de sinal não entra na lista;
    a tabela mostra, por métrica, a ordem das distâncias, e quando 2014 é o mais longe de 2026 isso é dito.
D14. Erros-padrão: (a) a (f) e (h) são contas sobre todas as seções (população inteira, não amostra) e não têm erro
    amostral; (g) tem bootstrap; (i) traz os erros-padrão do F21.
D15. As distâncias usam os números sem arredondar; o texto arredonda só na impressão.

ALTERAÇÕES DEPOIS DE RODAR (07/11/2026, cerca de 14h10 UTC; o docstring acima, D1 a D15, ficou como estava; cópia com
sha1 e hora em /home/user/trabalho-eleicao/adendo26/P2/docstring_antes_de_rodar.txt)
- Só formato do texto: rótulos mais curtos na tabela, acentos, votos sem casas decimais, faixas com vírgula.
- Bloco exploratório (função exploratorio), marcado como feito depois de ver o resultado, fora da contagem e da leitura:
  contribuição do Nordeste e margem total em pontos dos válidos, (a) pelo oficial com exterior, ordem das correlações.

Uso:
  python3 -I analisar_P2_2014.py <secoes2014.json.gz> <secoes2018.json.gz> <secoes2022.json.gz> <secoes2026.json.gz>
          <F21_serie_anos.json> <saida.json> <saida.txt>
"""
import os as _os, sys as _sys
_sys.path.insert(0, _os.path.dirname(_os.path.abspath(__file__)))
import json, sys
import numpy as np
from lib import carregar

ANOS = [2014, 2018, 2022, 2026]
REF = 2026
OUTROS = [2014, 2018, 2022]
NE = {'AL', 'BA', 'CE', 'MA', 'PB', 'PE', 'PI', 'RN', 'SE'}
OFICIAL_A = {2014: 51.64, 2018: 44.87, 2022: 50.90, 2026: 51.79}
CAND = {2014: ('Dilma', 'Aécio'), 2018: ('Haddad', 'Bolsonaro'), 2022: ('Lula', 'Bolsonaro'), 2026: ('Lula', 'Flávio')}
SEMENTE, NBOOT, TOL = 20261107, 2000, 1e-12
CAMPOS = ['L', 'R', 'O', 'B', 'N', 'comp', 'apt', 'c28']


# ------------------------------------------------------------------------------------------------ leitura
def ler_ano(caminho):
    d = carregar(caminho)
    t1 = {c: [] for c in CAMPOS}
    t2 = {c: [] for c in CAMPOS}
    uf, mun = [], []
    cont = {'chaves': len(d), 'exterior': 0, 'sem_os_dois_turnos': 0, 'anuladas_mantidas': 0}
    ofi = {'L2': 0, 'R2': 0, 'secoes_2t': 0}
    for k, v in d.items():
        if '2' in v:
            ofi['L2'] += v['2']['L']; ofi['R2'] += v['2']['R']; ofi['secoes_2t'] += 1
        u, m, _, _ = k.split('|')
        if u == 'ZZ':
            cont['exterior'] += 1
            continue
        if '1' not in v or '2' not in v:
            cont['sem_os_dois_turnos'] += 1
            continue
        a, b = v['1'], v['2']
        for c in CAMPOS:
            t1[c].append(a.get(c, 0)); t2[c].append(b.get(c, 0))
        if str(a.get('tipo', '')).lower() == 'anulada' or str(b.get('tipo', '')).lower() == 'anulada':
            cont['anuladas_mantidas'] += 1
        uf.append(u); mun.append(f'{u}|{m}')
    del d
    t1 = {c: np.asarray(x, dtype=np.int64) for c, x in t1.items()}
    t2 = {c: np.asarray(x, dtype=np.int64) for c, x in t2.items()}
    cont['universo'] = int(len(uf))
    return {'t1': t1, 't2': t2, 'uf': np.asarray(uf), 'mun': np.asarray(mun), 'cont': cont, 'ofi': ofi}


# ------------------------------------------------------------------------------------------------ métricas por ano
def metricas_ano(D):
    t1, t2 = D['t1'], D['t2']
    S1 = {c: int(t1[c].sum()) for c in CAMPOS}
    S2 = {c: int(t2[c].sum()) for c in CAMPOS}
    val1 = S1['L'] + S1['R'] + S1['O'] - S1['c28']
    val2 = S2['L'] + S2['R'] + S2['O'] - S2['c28']
    m = {'somas_1t': S1, 'somas_2t': S2, 'validos_1t': val1, 'validos_2t': val2}
    # (a)
    m['a'] = 100 * S2['L'] / (S2['L'] + S2['R'])
    ofi = D['ofi']
    m['a_base_com_exterior'] = 100 * ofi['L2'] / (ofi['L2'] + ofi['R2'])
    # (b)
    f1 = S1['L'] / (S1['L'] + S1['R']); f2 = S2['L'] / (S2['L'] + S2['R'])
    m['b'] = 100 * (f2 - f1); m['b_fatia_finalistas_1t'] = 100 * f1; m['b_fatia_finalistas_2t'] = 100 * f2
    # (c)
    mg = S1['L'] - S1['R']
    m['c_lider'] = 'PT' if mg > 0 else ('adversario' if mg < 0 else 'empate')
    m['c_margem_pt_votos'] = mg
    m['c_margem_lider_votos'] = abs(mg)
    m['c_margem_lider_pontos_validos'] = 100 * abs(mg) / val1
    m['c_pt_pct_validos_1t'] = 100 * S1['L'] / val1; m['c_adv_pct_validos_1t'] = 100 * S1['R'] / val1
    # (d)
    m['d_votos'] = S2['comp'] - S1['comp']
    m['d_taxa_1t'] = 100 * S1['comp'] / S1['apt']; m['d_taxa_2t'] = 100 * S2['comp'] / S2['apt']
    m['d_pontos'] = m['d_taxa_2t'] - m['d_taxa_1t']
    # (e)
    bn1 = S1['B'] + S1['N'] + S1['c28']; bn2 = S2['B'] + S2['N'] + S2['c28']
    m['e_bn_1t'] = bn1; m['e_bn_2t'] = bn2; m['e_votos'] = bn2 - bn1
    m['e_pct_aptos_1t'] = 100 * bn1 / S1['apt']; m['e_pct_aptos_2t'] = 100 * bn2 / S2['apt']
    m['e_pontos'] = m['e_pct_aptos_2t'] - m['e_pct_aptos_1t']
    # (f)
    ne = np.isin(D['uf'], list(NE))
    mt = S2['L'] - S2['R']
    mne = int(t2['L'][ne].sum() - t2['R'][ne].sum())
    m['f_margem_total_votos'] = mt; m['f_margem_ne_votos'] = mne; m['f_margem_fora_votos'] = mt - mne
    m['f_parte_ne_pct'] = 100 * mne / mt
    m['f_margem_total_pontos'] = 100 * mt / val2
    m['f_contrib_ne_pontos'] = 100 * mne / val2
    m['f_margem_fora_pontos'] = 100 * (mt - mne) / val2
    m['f_validos_ne'] = int(t2['L'][ne].sum() + t2['R'][ne].sum())
    m['f_fatia_pt_ne'] = 100 * t2['L'][ne].sum() / m['f_validos_ne']
    m['f_fatia_pt_fora'] = 100 * t2['L'][~ne].sum() / (val2 - m['f_validos_ne'])
    # (h)
    v = t2['L'] + t2['R']
    ok = v > 0
    s = t2['L'][ok] / v[ok]; w = v[ok].astype(float)
    mu_w = (w * s).sum() / w.sum()
    m['h_secoes'] = int(ok.sum()); m['h_secoes_sem_validos'] = int((~ok).sum())
    m['h_dp_simples'] = 100 * float(s.std(ddof=0))
    m['h_dp_ponderado'] = 100 * float(np.sqrt((w * (s - mu_w) ** 2).sum() / w.sum()))
    m['h_media_simples'] = 100 * float(s.mean())
    m['h_acima_80_pct'] = 100 * float((s > 0.80).mean()); m['h_abaixo_20_pct'] = 100 * float((s < 0.20).mean())
    m['h_acima_80_n'] = int((s > 0.80).sum()); m['h_abaixo_20_n'] = int((s < 0.20).sum())
    return m


def municipios(D):
    t2 = D['t2']
    u, inv = np.unique(D['mun'], return_inverse=True)
    L = np.bincount(inv, weights=t2['L'], minlength=len(u))
    V = np.bincount(inv, weights=t2['L'] + t2['R'], minlength=len(u))
    ok = V > 0
    return {k: (l / vv, vv) for k, l, vv in zip(u[ok], L[ok], V[ok])}, int((~ok).sum())


# ------------------------------------------------------------------------------------------------ correlações
def wcorr(x, y, w):
    w = w / w.sum()
    mx, my = (w * x).sum(), (w * y).sum()
    dx, dy = x - mx, y - my
    return float((w * dx * dy).sum() / np.sqrt((w * dx * dx).sum() * (w * dy * dy).sum()))


def corr(x, y):
    return float(np.corrcoef(x, y)[0, 1])


def correlacoes(M):
    """M[ano] = {mun: (fatia, validos)}. Pearson bruta e ponderada (válidos de 2026), com bootstrap."""
    rng = np.random.default_rng(SEMENTE)
    out = {}
    ref = M[REF]
    for a in OUTROS:
        ks = sorted(set(ref) & set(M[a]))
        x = np.array([ref[k][0] for k in ks]); w = np.array([ref[k][1] for k in ks])
        y = np.array([M[a][k][0] for k in ks])
        n = len(ks)
        rb, rp = corr(x, y), wcorr(x, y, w)
        bb, bp = np.empty(NBOOT), np.empty(NBOOT)
        for i in range(NBOOT):
            j = rng.integers(0, n, n)
            bb[i] = corr(x[j], y[j]); bp[i] = wcorr(x[j], y[j], w[j])
        out[str(a)] = {'municipios': n, 'so_em_2026': len(set(ref) - set(M[a])), 'so_no_outro_ano': len(set(M[a]) - set(ref)),
                       'bruta': rb, 'bruta_ep': float(bb.std(ddof=1)),
                       'ponderada': rp, 'ponderada_ep': float(bp.std(ddof=1))}
    # robustez: municípios presentes nos quatro anos, bootstrap pareado
    ks = sorted(set.intersection(*[set(M[a]) for a in ANOS]))
    x = np.array([ref[k][0] for k in ks]); w = np.array([ref[k][1] for k in ks])
    Y = {a: np.array([M[a][k][0] for k in ks]) for a in OUTROS}
    n = len(ks)
    pt = {a: (corr(x, Y[a]), wcorr(x, Y[a], w)) for a in OUTROS}
    B = {a: np.empty((NBOOT, 2)) for a in OUTROS}
    for i in range(NBOOT):
        j = rng.integers(0, n, n)
        for a in OUTROS:
            B[a][i] = (corr(x[j], Y[a][j]), wcorr(x[j], Y[a][j], w[j]))
    rob = {'municipios_nos_4_anos': n}
    for q, nome in ((0, 'bruta'), (1, 'ponderada')):
        top = max(OUTROS, key=lambda a: pt[a][q])
        rob[nome] = {'por_ano': {str(a): pt[a][q] for a in OUTROS}, 'maior': top, 'diferencas_para_a_maior': {}}
        for a in OUTROS:
            if a == top:
                continue
            dif = B[top][:, q] - B[a][:, q]
            rob[nome]['diferencas_para_a_maior'][str(a)] = {'dif': pt[top][q] - pt[a][q], 'ep': float(dif.std(ddof=1))}
    out['robustez_4_anos'] = rob
    return out


# ------------------------------------------------------------------------------------------------ semelhança
def mais_perto(valores, tipo):
    """valores[ano]; tipo 'abs' (distância absoluta), 'max' (maior valor), 'igual' (categoria), 'vetor' (média |dif|)."""
    ref = valores[REF]
    dist = {}
    for a in OUTROS:
        v = valores[a]
        if tipo == 'abs':
            dist[a] = abs(v - ref)
        elif tipo == 'max':
            dist[a] = -v
        elif tipo == 'igual':
            dist[a] = 0.0 if v == ref else 1.0
        elif tipo == 'vetor':
            dist[a] = float(np.mean(np.abs(np.asarray(v) - np.asarray(ref))))
    mn = min(dist.values())
    perto = [a for a in OUTROS if dist[a] - mn <= TOL]
    if tipo == 'igual' and mn > 0:
        perto = []  # nenhum ano igual a 2026
    ordem = sorted(OUTROS, key=lambda a: dist[a])
    return {'distancia': {str(a): dist[a] for a in OUTROS}, 'mais_perto': perto, 'empate': len(perto) > 1,
            'ordem_do_mais_perto_ao_mais_longe': ordem, '2014_mais_perto': 2014 in perto,
            '2014_mais_longe': ordem[-1] == 2014 and dist[2014] - dist[ordem[-2]] > TOL}


def sinal(x):
    return 1 if x > 0 else (-1 if x < 0 else 0)


# ------------------------------------------------------------------------------------------------ texto
def fn(x, nd=2, s=False):
    t = f'{x:+,.{nd}f}' if s else f'{x:,.{nd}f}'
    return t.replace(',', '_').replace('.', ',').replace('_', '.')


def fi(x, s=False):
    t = f'{int(x):+,d}' if s else f'{int(x):,d}'
    return t.replace(',', '.')


def main():
    p14, p18, p22, p26, pf21, sj, st = sys.argv[1:8]
    caminhos = {2014: p14, 2018: p18, 2022: p22, 2026: p26}
    R, M, cont, sem_val_mun = {}, {}, {}, {}
    for a in ANOS:
        D = ler_ano(caminhos[a])
        R[a] = metricas_ano(D)
        M[a], sem_val_mun[a] = municipios(D)
        cont[a] = D['cont']; cont[a]['municipios'] = len(M[a]); cont[a]['municipios_sem_validos_2t'] = sem_val_mun[a]
        cont[a]['ofi_secoes_2t_com_exterior'] = D['ofi']['secoes_2t']
        del D
    G = correlacoes(M)
    F21 = json.load(open(pf21))
    i1 = {a: [f['d'][0] for f in F21['A_serie_principal'][str(a)]['faixas']] for a in ANOS}
    i1_ep = {a: [f['d'][1] for f in F21['A_serie_principal'][str(a)]['faixas']] for a in ANOS}
    faixas = [f['faixa'] for f in F21['A_serie_principal']['2026']['faixas']]
    serie = {s_['ano']: s_ for s_ in F21['serie']}
    i2 = {a: serie[a]['erro_medio_pesquisa_pt'] for a in ANOS}
    A21 = {a: serie[a]['A'] for a in ANOS}

    val = lambda k: {a: R[a][k] for a in ANOS}
    gb = {a: G[str(a)]['bruta'] for a in OUTROS}; gb[REF] = 1.0
    gp = {a: G[str(a)]['ponderada'] for a in OUTROS}; gp[REF] = 1.0
    PRIM = [
        ('a', 'fatia do PT nos válidos, 2º turno (%)', val('a'), 'abs'),
        ('b', 'variação da fatia do PT, 1º para 2º turno', val('b'), 'abs'),
        ('c', 'lado do líder do 1º turno', val('c_lider'), 'igual'),
        ('d', 'variação do comparecimento (pontos dos aptos)', val('d_pontos'), 'abs'),
        ('e', 'variação de brancos+nulos (pontos dos aptos)', val('e_pontos'), 'abs'),
        ('f', 'parte da margem do PT vinda do Nordeste (%)', val('f_parte_ne_pct'), 'abs'),
        ('g', 'correlação municipal com 2026 (bruta)', gb, 'max'),
        ('h', 'desvio-padrão simples entre seções (pontos)', val('h_dp_simples'), 'abs'),
        ('i1', 'curva por faixa, F21 (distância a 2026)', i1, 'vetor'),
        ('i2', 'erro das pesquisas no PT, F21 (pontos)', i2, 'abs'),
    ]
    DESAG = [
        ('a', val('a'), 'abs'), ('b', val('b'), 'abs'), ('c', val('c_lider'), 'igual'),
        ('d_votos', val('d_votos'), 'abs'), ('d_pontos', val('d_pontos'), 'abs'),
        ('e_votos', val('e_votos'), 'abs'), ('e_pontos', val('e_pontos'), 'abs'),
        ('f_parte', val('f_parte_ne_pct'), 'abs'), ('f_fora_pontos', val('f_margem_fora_pontos'), 'abs'),
        ('g_bruta', gb, 'max'), ('g_ponderada', gp, 'max'),
        ('h_dp_simples', val('h_dp_simples'), 'abs'), ('h_dp_ponderado', val('h_dp_ponderado'), 'abs'),
        ('h_acima_80', val('h_acima_80_pct'), 'abs'), ('h_abaixo_20', val('h_abaixo_20_pct'), 'abs'),
        ('i1', i1, 'vetor'), ('i2', i2, 'abs'),
    ]
    sem = {k: dict(mais_perto(v, t), rotulo=r, valores={str(a): v[a] for a in ANOS}) for k, r, v, t in PRIM}
    des = {k: mais_perto(v, t) for k, v, t in DESAG}
    n14 = sum(1 for k in sem if sem[k]['2014_mais_perto'])
    n14_des = sum(1 for k in des if des[k]['2014_mais_perto'])
    cont_ano = {str(a): sum(1 for k in sem if a in sem[k]['mais_perto']) for a in OUTROS}
    cont_ano_des = {str(a): sum(1 for k in des if a in des[k]['mais_perto']) for a in OUTROS}

    # D13: diferenças marcantes 2014 x 2026
    marc = []
    def cmp_cat(nome, x14, x26):
        marc.append({'item': nome, '2014': x14, '2026': x26, 'diferente': x14 != x26})
    cmp_cat('lado do líder do 1º turno (c)', R[2014]['c_lider'], R[2026]['c_lider'])
    cmp_cat('lado do vencedor do 2º turno (sinal de a - 50)', 'PT' if R[2014]['a'] > 50 else 'adversario',
            'PT' if R[2026]['a'] > 50 else 'adversario')
    for nome, x14, x26 in [
        ('sinal da variação da fatia do PT entre finalistas (b)', R[2014]['b'], R[2026]['b']),
        ('sinal da variação do comparecimento em votos (d)', R[2014]['d_votos'], R[2026]['d_votos']),
        ('sinal da variação do comparecimento em pontos (d)', R[2014]['d_pontos'], R[2026]['d_pontos']),
        ('sinal da variação de brancos+nulos em votos (e)', R[2014]['e_votos'], R[2026]['e_votos']),
        ('sinal da variação de brancos+nulos em pontos (e)', R[2014]['e_pontos'], R[2026]['e_pontos']),
        ('sinal da parte do Nordeste (f)', R[2014]['f_parte_ne_pct'], R[2026]['f_parte_ne_pct']),
        ('sinal da margem do PT fora do Nordeste (f)', R[2014]['f_margem_fora_votos'], R[2026]['f_margem_fora_votos']),
    ] + [(f'sinal de d na faixa {faixas[j].replace(".", ",")} (i1)', i1[2014][j], i1[2026][j]) for j in range(4)] + [
        ('sinal do erro das pesquisas no PT (i2)', i2[2014], i2[2026])]:
        marc.append({'item': nome, '2014': x14, '2026': x26, 'diferente': sinal(x14) != sinal(x26)})

    out = {
        'teste': 'P2, Adendo 26 (commit 5174ff5, 07/11/2026 13:57:56 UTC)',
        'universo': {str(a): cont[a] for a in ANOS},
        'metricas_por_ano': {str(a): R[a] for a in ANOS},
        'oficial_a_com_exterior': {str(a): OFICIAL_A[a] for a in ANOS},
        'g_correlacoes': G,
        'i_copiado_do_F21': {'faixas': faixas, 'd': {str(a): i1[a] for a in ANOS}, 'd_ep': {str(a): i1_ep[a] for a in ANOS},
                             'A': {str(a): A21[a] for a in ANOS}, 'erro_pesquisa_pt': {str(a): i2[a] for a in ANOS},
                             'fonte': 'resultados/F21_serie_anos.json (A_serie_principal e serie)'},
        'semelhanca_principal': sem,
        'contagem_principal': {'2014_mais_perto': n14, 'metricas': len(sem), 'por_ano_mais_perto': cont_ano},
        'semelhanca_desagregada': des,
        'contagem_desagregada': {'2014_mais_perto': n14_des, 'numeros': len(des), 'por_ano_mais_perto': cont_ano_des},
        'diferencas_marcantes_2014_2026_regra_D13': marc,
        'leitura_fixada': 'semelhança numa métrica de resultado, composição ou comportamento (todas de P2) não é indício '
                          'de fraude, porque eleições limpas com a mesma geografia se parecem',
        'parametros': {'semente': SEMENTE, 'bootstrap': NBOOT, 'nordeste': sorted(NE)},
        'desvios': DESVIOS,
    }
    X = exploratorio(R, G)
    out['exploratorio_depois_de_ver'] = X
    json.dump(out, open(sj, 'w'), ensure_ascii=False, indent=1, default=lambda o: o.item() if hasattr(o, 'item') else str(o))
    open(st, 'w').write(texto(out, R, G, i1, i1_ep, i2, faixas, A21, cont, sem, des, n14, n14_des, cont_ano, cont_ano_des,
                              marc, X))
    print(open(st).read())


DESVIOS = [
    'D1. Universo: por ano, seções com os dois turnos e sem o exterior, sem ligar seções entre anos; seções com um turno '
    'anulado ficam como a base as registra (1 em 2014, 3 em 2018); seções sem válidos no 2º turno saem só de (h).',
    'D2. 2026: votos do 28 cassado (c28, 1º turno) contados como nulo, como no total oficial.',
    'D3. (a) = L/(L+R) do 2º turno no universo; conferência com exterior contra o oficial.',
    'D4. (b) = diferença de L/(L+R) entre os turnos, somas do universo, em pontos.',
    'D5. (c) semelhança = mesmo lado do líder (PT ou adversário); a margem não desempata.',
    'D6. (d) semelhança pela variação em pontos dos aptos; em votos só na contagem desagregada.',
    'D7. (e) idem com brancos+nulos.',
    'D8. (f) parte = margem do Nordeste / margem total; com margem total negativa (2018) a parte fica negativa, sem '
    'reinterpretar; margem fora do Nordeste em pontos só na contagem desagregada.',
    'D9. (g) Pearson por município (UF|código), bruta (primária) e ponderada pelos válidos de 2026; bootstrap de '
    'municípios (2.000, semente 20261107); robustez nos municípios dos 4 anos com bootstrap pareado.',
    'D10. (h) semelhança pelo desvio-padrão simples (seção como unidade); ponderado e frações só na desagregada; '
    'frações com desigualdade estrita.',
    'D11. (i) copiado do F21 sem recalcular e contado como duas métricas: (i1) curva por faixa (distância = média das '
    'diferenças absolutas de d nas 4 faixas, universo do F21) e (i2) erro das pesquisas.',
    'D12. Contagem principal em 10 métricas; empate exato conta para todos os empatados; contagem desagregada em 17 '
    'números como robustez.',
    'D13. "Diferente de modo marcante" = categoria ou sinal diferente (lista fixada antes); diferença só de nível não entra.',
    'D14. (a) a (f) e (h) são contas sobre todas as seções, sem erro amostral; (g) com bootstrap; (i) com os erros-padrão '
    'do F21.',
    'D15. Distâncias com os números sem arredondar.',
]


def exploratorio(R, G):
    """Feito DEPOIS de ver o resultado (07/11/2026, cerca de 14h10 UTC). Fora da contagem e da leitura."""
    x = {'nota': 'exploratório, depois de ver o resultado; não entra na contagem nem na leitura'}
    for k in ('f_contrib_ne_pontos', 'f_margem_total_pontos', 'f_fatia_pt_ne', 'f_fatia_pt_fora'):
        v = {a: R[a][k] for a in ANOS}
        x[k] = dict(mais_perto(v, 'abs'), valores={str(a): v[a] for a in ANOS})
    x['a_oficial_com_exterior'] = dict(mais_perto(OFICIAL_A, 'abs'), valores={str(a): OFICIAL_A[a] for a in ANOS})
    x['g_ordem_bruta'] = sorted(OUTROS, key=lambda a: -G[str(a)]['bruta'])
    x['g_ordem_ponderada'] = sorted(OUTROS, key=lambda a: -G[str(a)]['ponderada'])
    return x


def texto(out, R, G, i1, i1_ep, i2, faixas, A21, cont, sem, des, n14, n14_des, cont_ano, cont_ano_des, marc, X):
    L = []
    w = L.append
    lado = lambda c, a: (f'PT ({CAND[a][0]})' if c == 'PT' else f'adversário ({CAND[a][1]})')
    fx = [f.replace('.', ',') for f in faixas]
    w('P2 (Adendo 26): métricas de 2014, 2018, 2022 e 2026 lado a lado. Checagem da postagem "2014 parecida com 2026"')
    w('(@FelipeCecilio_, X). Sem veredito de fraude.')
    w('Registro: PRE-REGISTRO-2026-10-26.md, Adendo 26, commit 5174ff5 (07/11/2026 13:57:56 UTC), antes de rodar.')
    w('Script: scripts/analisar_P2_2014.py (python3 -I). Números completos: resultados/P2_metricas_2014_2026.json.')
    w('Universo: por ano, seções com os dois turnos, sem o exterior (UF ZZ). L = candidato do PT; R = adversário.')
    for a in ANOS:
        c = cont[a]
        w(f'  {a} ({CAND[a][0]} x {CAND[a][1]}): {fi(c["universo"])} seções, {fi(c["municipios"])} municípios; fora: '
          f'exterior {fi(c["exterior"])}, sem os dois turnos {fi(c["sem_os_dois_turnos"])}; com um turno anulado, '
          f'mantidas: {c["anuladas_mantidas"]}')
    w('')
    w('1. Tabela (2026 é a referência; mais perto = menor distância a 2026; em (g), maior correlação; em (c), mesmo lado)')
    w(f'{"métrica":<50} | {"2014":>8} | {"2018":>8} | {"2022":>8} | {"2026":>8} | mais perto | 2014 mais perto')

    def v2s(k, x):
        if k == 'c':
            return 'PT' if x == 'PT' else 'advers.'
        if k == 'g':
            return fn(x, 3)
        return fn(x, 2, s=k in ('b', 'd', 'e', 'i2'))
    for k, s_ in sem.items():
        if k == 'i1':
            vals = [fn(s_['distancia'][str(a)], 4) for a in OUTROS] + ['ref.']
        else:
            vals = [v2s(k, s_['valores'][str(a)]) for a in ANOS]
        if k == 'g':
            vals[3] = 'ref.'
        pp = ', '.join(str(a) for a in s_['mais_perto']) or 'nenhum'
        sim = ('sim' + (' (empate)' if s_['empate'] else '')) if s_['2014_mais_perto'] else 'não'
        w(f'{"(" + k + ") " + s_["rotulo"]:<50} | {vals[0]:>8} | {vals[1]:>8} | {vals[2]:>8} | {vals[3]:>8} | {pp:<10} | {sim}')
    w('(b) em pontos; (i1) mostra a distância de cada ano a 2026 (média das diferenças absolutas de d nas 4 faixas).')
    w('Sem erro amostral em (a) a (f) e (h): são contas sobre todas as seções. Erros-padrão de (g) e (i) no item 2.')
    w('')
    w('2. Detalhes')
    for a in ANOS:
        r = R[a]
        w(f'  {a}: (a) sem exterior {fn(r["a"], 2)}%; base com exterior {fn(r["a_base_com_exterior"], 2)}%; oficial '
          f'{fn(OFICIAL_A[a], 2)}%. (b) PT entre finalistas {fn(r["b_fatia_finalistas_1t"], 2)}% no 1º turno, '
          f'{fn(r["b_fatia_finalistas_2t"], 2)}% no 2º.')
        w(f'     (c) liderou {lado(r["c_lider"], a)} por {fi(r["c_margem_lider_votos"])} votos, '
          f'{fn(r["c_margem_lider_pontos_validos"], 2)} pontos dos válidos (PT {fn(r["c_pt_pct_validos_1t"], 2)}%, '
          f'adversário {fn(r["c_adv_pct_validos_1t"], 2)}%).')
        w(f'     (d) comparecimento {fn(r["d_taxa_1t"], 2)}% para {fn(r["d_taxa_2t"], 2)}% dos aptos: {fi(r["d_votos"], True)} votos, '
          f'{fn(r["d_pontos"], 2, True)} pontos. (e) brancos+nulos {fn(r["e_pct_aptos_1t"], 2)}% para {fn(r["e_pct_aptos_2t"], 2)}%: '
          f'{fi(r["e_votos"], True)} votos, {fn(r["e_pontos"], 2, True)} pontos.')
        w(f'     (f) margem do PT {fi(r["f_margem_total_votos"], True)} ({fn(r["f_margem_total_pontos"], 2, True)} pontos); '
          f'Nordeste {fi(r["f_margem_ne_votos"], True)} ({fn(r["f_contrib_ne_pontos"], 2, True)} pontos), parte '
          f'{fn(r["f_parte_ne_pct"], 1)}%; fora do Nordeste {fi(r["f_margem_fora_votos"], True)} '
          f'({fn(r["f_margem_fora_pontos"], 2, True)} pontos).')
        w(f'     (h) {fi(r["h_secoes"])} seções: desvio-padrão simples {fn(r["h_dp_simples"], 2)}, ponderado '
          f'{fn(r["h_dp_ponderado"], 2)} pontos; acima de 80%: {fn(r["h_acima_80_pct"], 2)}% ({fi(r["h_acima_80_n"])}); '
          f'abaixo de 20%: {fn(r["h_abaixo_20_pct"], 2)}% ({fi(r["h_abaixo_20_n"])}).')
    w('  (g) correlação por município com 2026 (erro-padrão por bootstrap de municípios, 2.000 reamostragens):')
    for a in OUTROS:
        g = G[str(a)]
        w(f'     {a}: {fi(g["municipios"])} municípios; bruta {fn(g["bruta"], 4)} ({fn(g["bruta_ep"], 4)}); '
          f'ponderada pelos válidos de 2026 {fn(g["ponderada"], 4)} ({fn(g["ponderada_ep"], 4)})')
    rb = G['robustez_4_anos']
    for nome in ('bruta', 'ponderada'):
        q = rb[nome]
        difs = '; '.join(f'para {a} {fn(v["dif"], 4)} ({fn(v["ep"], 4)})' for a, v in q['diferencas_para_a_maior'].items())
        w(f'     robustez ({fi(rb["municipios_nos_4_anos"])} municípios dos 4 anos), {nome}: maior {q["maior"]}; '
          f'diferença da maior {difs}')
    w('  (i) copiado do F21 (série principal, 331.087 seções, sem recalcular): d por faixa de força do adversário')
    w('     (erro-padrão), faixas ' + '; '.join(fx))
    for a in ANOS:
        w(f'     {a}: ' + '; '.join(f'{fn(x, 4, True)} ({fn(e, 4)})' for x, e in zip(i1[a], i1_ep[a]))
          + f'. A {fn(A21[a][0], 4, True)} ({fn(A21[a][1], 4)}). Erro das pesquisas no PT {fn(i2[a], 2, True)}')
    w('')
    longe = [k for k in sem if sem[k]['2014_mais_longe']]
    w(f'3. Contagem: 2014 é o mais perto de 2026 em {n14} de {len(sem)} métricas '
      f'({", ".join(k for k in sem if sem[k]["2014_mais_perto"]) or "nenhuma"}). Mais perto por ano: 2014 em '
      f'{cont_ano["2014"]}, 2018 em {cont_ano["2018"]}, 2022 em {cont_ano["2022"]}. '
      f'{"Com empate em " + ", ".join(k for k in sem if sem[k]["empate"]) if any(sem[k]["empate"] for k in sem) else "Sem empates"}.')
    w(f'   Desagregada (17 números, robustez fixada antes): 2014 em {n14_des} '
      f'({", ".join(k for k in des if des[k]["2014_mais_perto"]) or "nenhum"}), 2018 em {cont_ano_des["2018"]}, '
      f'2022 em {cont_ano_des["2022"]}.')
    w(f'   2014 é o mais longe de 2026 em {len(longe)} métricas: {", ".join(longe) or "nenhuma"}.')
    w('')
    w('4. Leitura fixada no registro: semelhança numa métrica de resultado, composição ou comportamento (todas de P2) não é')
    w('   indício de fraude, porque eleições limpas com a mesma geografia se parecem. "2014 parecida" vale em ' +
      ', '.join(k for k in sem if sem[k]['2014_mais_perto']) + '; P2 não dá veredito de fraude.')
    w('')
    w('5. Ao lado, sem mudar a leitura (regra D13, fixada antes): onde 2014 e 2026 são diferentes de modo marcante')

    def fmt(x):
        if isinstance(x, str):
            return 'PT' if x == 'PT' else 'adversário'
        if isinstance(x, (int, np.integer)):
            return fi(x, True)
        return fn(x, 4 if abs(x) < 0.1 else 2, True)
    for m in marc:
        if m['diferente']:
            w(f'   DIFERENTE: {m["item"]}: 2014 {fmt(m["2014"])}, 2026 {fmt(m["2026"])}')
    w('   Iguais (mesmo lado ou mesmo sinal): ' + '; '.join(m['item'] for m in marc if not m['diferente']) + '.')
    w('')
    w('6. O que isso significa')
    top = max(OUTROS, key=lambda a: cont_ano[str(a)])
    w(f'   2014 é o ano mais perto de 2026 em {n14} das {len(sem)} métricas; {top} é o mais perto em mais delas '
      f'({cont_ano[str(top)]}, e {cont_ano_des[str(top)]} dos 17 números). '
      + ('Pela contagem, 2014 não é o ano mais parecido com 2026.' if top != 2014 else 'Pela contagem, 2014 é o ano mais parecido com 2026.'))
    w('   Onde 2014 se parece: o resultado final (PT perto de 51,7% nos dois anos), o peso do Nordeste na margem e a curva')
    w('   por faixa do F21. Onde difere: quem liderou o 1º turno, o sentido da variação do PT entre os turnos, o sentido')
    w('   do comparecimento e o sinal do erro das pesquisas. Pela leitura registrada, nenhuma semelhança daqui é indício')
    w('   de fraude, em 2014 ou em 2026; a postagem não diz quais métricas usou (P1).')
    w('')
    w('7. Exploratório (depois de ver o resultado; fora da contagem e da leitura)')
    ce, mt = X['f_contrib_ne_pontos'], X['f_margem_total_pontos']
    w('   (a) e (f) não são independentes: parte do Nordeste = contribuição do Nordeste / margem total.')
    w('   Contribuição do Nordeste, em pontos dos válidos: ' +
      ', '.join(f'{a} {fn(ce["valores"][str(a)], 2, True)}' for a in ANOS) +
      f'; a mais perto de 2026 é a de {", ".join(map(str, ce["mais_perto"]))}.')
    w('   Margem total, em pontos dos válidos: ' + ', '.join(f'{a} {fn(mt["valores"][str(a)], 2, True)}' for a in ANOS) +
      f'; a mais perto de 2026 é a de {", ".join(map(str, mt["mais_perto"]))}.')
    w('   A parte de 2014 fica perto da de 2026 pelo denominador (a margem total), que é o mesmo fato de (a): duas')
    w('   vitórias apertadas do PT. Das 3 métricas em que 2014 é o mais perto, duas contam esse mesmo fato.')
    w('   A semelhança da curva (i1) já estava no F21 (pista 1), onde o sentido de d nas faixas de 35% para cima')
    w('   acompanhava quem estava no governo (Dilma em 2014, Lula em 2026; também post hoc).')
    ao = X['a_oficial_com_exterior']
    w(f'   (a) pelo oficial com exterior: mais perto {", ".join(map(str, ao["mais_perto"]))} (distâncias ' +
      ', '.join(f'{a} {fn(ao["distancia"][str(a)], 2)}' for a in OUTROS) + ').')
    w(f'   (g): a correlação com 2026 cai com a distância no tempo (bruta, da maior para a menor: '
      f'{", ".join(map(str, X["g_ordem_bruta"]))}; ponderada: {", ".join(map(str, X["g_ordem_ponderada"]))}).')
    w('')
    w('8. Decisões que o registro não fixa (no docstring antes de calcular; relatadas como desvios)')
    for d in DESVIOS:
        w('   ' + d)
    w('   Sabido antes: os totais oficiais com exterior (contexto_virada_2t) já davam (a) a (e) de forma aproximada, e o')
    w('   F21 já dava (i). Depois de rodar mudou só o formato do texto e entrou o item 7 (marcado).')
    return '\n'.join(L) + '\n'


if __name__ == '__main__':
    main()
