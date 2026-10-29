"""L4 do Adendo 18: os eleitores dos candidatos que apoiaram Flávio, no estado de cada um (bweb completo dos dois turnos).

Registro (PRE-REGISTRO-2026-10-26.md, Adendo 18, commit bc7decb de 2026-10-29 05:13:35 UTC, antes de rodar):
  - Lógica: Caiado (GO) e Zema (MG) apoiaram Flávio e governam esses estados; Cury (SP) também apoiou. Os eleitores
    deles no 1º turno deveriam ir mais para Flávio que para Lula, principalmente em casa.
  - Em GO (Caiado), MG (Zema) e SP (Cury): regressão do T8 com os grupos dos eliminados, dentro da UF, efeito fixo de
    local. s = b_L / (b_L + b_F) para o grupo do candidato da casa: fatia de Lula entre os eleitores dele que a urna
    põe num finalista.
  - Referência externa (não passa pela urna): a mesma fatia declarada nas pesquisas do 2º turno com cruzamento por voto
    no 1º turno (mediana dos institutos; Quaest já conhecida: Caiado 36%, Cury 47%, Zema 36%).
  - Incoerência: s acima de 50% e acima da referência das pesquisas em 15 pontos ou mais, a mais de 3 erros-padrão, em
    pelo menos 2 das 3 UFs. Coerente: s até a referência mais 5 pontos nas 3. Entre os dois: inconclusivo. Limite: a
    regressão entre seções erra quando o eleitor de um candidato mora junto com outro tipo de eleitor; o resultado é
    indício, não prova.

Especificação fixada neste arquivo antes de calcular qualquer coeficiente dentro de GO, MG ou SP (o que o registro não
fixou; tudo listado também no texto de saída como leitura ou desvio):
  1. Universo: seções da base com os dois turnos, da UF (GO, MG ou SP). Fora de casa: todas as outras seções da base com
     os dois turnos (as outras 26 UFs e o exterior), como o T37 nacional.
  2. Regressão do T8 com grupos, como registrada para 2026 (analisar_fluxo_regressao.py, analisar_T7_T14.t8 e
     analisar_eliminados.py): para c em {Lula, Flávio}, y = votos de c no 2º turno menos no 1º; X = votos de Cury (70),
     Renan (14), Caiado (55), Zema (30) e demais no 1º turno, queda do branco+nulo (1º menos 2º, sem truncar), variação
     do comparecimento (2º menos 1º), votos do adversário no 1º turno e votos do próprio no 1º turno; efeito fixo de
     local (UF|município|zona|local do 2º turno, lib.chave_local), sem peso, erro agrupado por local (CR1). Lula e Flávio
     empilhados (efeito fixo de local por candidato, erro agrupado por local, analisar_pres_gov.ols_cluster), o que dá
     os mesmos coeficientes das duas regressões separadas e a covariância entre b_L e b_F.
  3. s = b_L / (b_L + b_F) do grupo do candidato da casa; erro-padrão pelo método delta com a covariância empilhada.
     Como y_L + y_R = outros + queda do branco+nulo + variação do comparecimento por construção, b_L + b_F = 1 (Adendo
     17) e s = b_L; o código confere.
  4. Referência: para cada candidato da casa, a última rodada de cada instituto que publicou esse candidato separado no
     cruzamento por voto no 1º turno, com os valores conferidos em resultados/contexto_2t_2026_pesquisa_verificada.json;
     fatia declarada = Lula / (Lula + Flávio); referência = mediana entre os institutos.
       Caiado: PoderData 23-24/10, Quaest 17-20/10, AtlasIntel 13-18/10, Ipespe 13-15/10, Nexus 10-12/10.
       Cury: PoderData 23-24/10, Quaest 17-20/10, AtlasIntel 13-18/10, Ipespe 13-15/10 (Meio/Ideia 15-19/10 fica de fora
         na principal: atribuição da rodada não confirmada; entra numa leitura ao lado).
       Zema: PoderData 5-7/10 (última rodada do PoderData com Zema separado; depois ele entra em "outro") e Nexus
         10-12/10. O Datafolha só publicou o agregado dos quatro eliminados e fica fora da mediana por candidato.
     Os números escritos no registro como "Quaest já conhecida" (Caiado 36%, Cury 47%, Zema 36%) não batem com nenhuma
     Quaest publicada e conferida (a Quaest não separou Zema); viram uma leitura ao lado, e o desvio é declarado.
  5. Veredito por UF. INCOERÊNCIA na UF: s > 0,50, s - ref >= 0,15 e "a mais de 3 erros-padrão" lido a partir de zero
     para as duas comparações ((s - 0,50)/ep > 3 e (s - ref)/ep > 3; principal, mesma leitura do L3); ao lado, a leitura
     a partir do limiar ((s - ref - 0,15)/ep > 3). COERENTE na UF: s <= ref + 0,05 (estimativa pontual). Teste:
     INCOERÊNCIA se a UF dá incoerência em 2 ou mais das 3; COERENTE se as 3 dão coerente; senão INCONCLUSIVO. O
     erro-padrão é o da regressão (a urna); o erro da pesquisa não entra no critério e sai ao lado.
  Fora do critério (não muda o veredito), escolhido antes de ver s em GO, MG e SP:
  - s dos quatro grupos nas três UFs; s do candidato da casa fora de casa e no país (conferência com o T37);
  - leituras da referência: os números do registro ("Quaest já conhecida"), a mediana de todas as rodadas conferidas,
    a primeira rodada após o 1º turno, a maior fatia declarada por algum instituto e a leitura do T37 para o PoderData
    (sem Zema); com a Ideia para Cury;
  - incerteza da pesquisa: dispersão entre os institutos (desvio-padrão e erro da mediana aproximado por
    1,2533 * dp / raiz(k)), somada ao erro da urna;
  - especificação: efeito fixo de zona e de município (erro agrupado no mesmo nível), e peso pelo comparecimento do 1º
    turno (lib.fe_ols, Lula e Flávio separados);
  - heterogeneidade: s em terços de seções pela fatia do candidato da casa nos válidos do 1º turno da seção, dentro da UF
    (se s muda muito entre os terços, a hipótese de transferência constante da regressão ecológica não vale);
  - calibração: desvio simulado de uma fração fixa dos votos de Flávio no 2º turno para Lula, por cima dos dados, em todas
    as seções (1% e a fração que equivale a virar o resultado nacional), para ver quanto s se move com uma fraude que
    não escolhe o eleitor dos eliminados.

Uso: python3 -I analisar_L4.py <secoes2026.json.gz> <candidatos2026_1t.json.gz> <saida.json> <saida.txt>
"""
import os as _os, sys as _sys
_sys.path.insert(0, _os.path.dirname(_os.path.abspath(__file__)))
import json, sys, time, warnings
import numpy as np
from lib import carregar, chave_local, fe_ols
from analisar_pres_gov import ols_cluster
warnings.filterwarnings('ignore')

GRUPOS = [('Cury', '70'), ('Renan', '14'), ('Caiado', '55'), ('Zema', '30')]
GI = {g: i for i, (g, _) in enumerate(GRUPOS)}
NOMES = [g for g, _ in GRUPOS] + ['demais_outros', 'queda_branco_nulo', 'var_comparecimento', 'adversario_1T', 'proprio_1T']
K = len(NOMES)
CASA = {'GO': 'Caiado', 'MG': 'Zema', 'SP': 'Cury'}
LIM_50, LIM_DIF, LIM_COER, Z = 0.50, 0.15, 0.05, 3.0
VERIF = 'resultados/contexto_2t_2026_pesquisa_verificada.json'

# Cruzamentos declarados (Flávio, Lula), em %, conferidos em resultados/contexto_2t_2026_pesquisa_verificada.json.
# 'ultima' marca a última rodada do instituto com o candidato separado (principal).
DECL = {
    'Caiado': [
        ('PoderData', '23-24/10', 46, 30, True), ('PoderData', '19-21/10', 49, 30, False), ('PoderData', '16-18/10', 46, 19, False),
        ('PoderData', '13-15/10', 50, 30, False), ('PoderData', '10-12/10', 44, 30, False), ('PoderData', '5-7/10', 57, 19, False),
        ('Quaest', '17-20/10', 57, 21, True), ('Quaest', '10-13/10', 42, 23, False),
        ('AtlasIntel', '13-18/10', 69.8, 24.5, True), ('AtlasIntel', '3-8/10', 54.9, 26.9, False),
        ('Ipespe', '13-15/10', 59, 18, True), ('Ipespe', '6-8/10', 56, 15, False),
        ('Nexus', '10-12/10', 55, 27, True)],
    'Cury': [
        ('PoderData', '23-24/10', 58, 29, True), ('PoderData', '19-21/10', 42, 48, False), ('PoderData', '16-18/10', 56, 31, False),
        ('PoderData', '13-15/10', 47, 36, False), ('PoderData', '10-12/10', 45, 43, False), ('PoderData', '5-7/10', 56, 27, False),
        ('Quaest', '17-20/10', 33, 48, True), ('Quaest', '10-13/10', 30, 34, False),
        ('AtlasIntel', '13-18/10', 42.4, 52.1, True), ('AtlasIntel', '3-8/10', 38.9, 50.4, False),
        ('Ipespe', '13-15/10', 50, 31, True), ('Ipespe', '6-8/10', 50, 29, False)],
    'Zema': [
        ('PoderData', '5-7/10', 72, 10, True), ('Nexus', '10-12/10', 80, 12, True)],
}
IDEIA_CURY = ('Meio/Ideia', '15-19/10', 36, 48)          # atribuição da rodada não confirmada (confiança baixa)
DATAFOLHA_AGREG = [('Datafolha', '13-14/10', 46, 27), ('Datafolha', '6-7/10', 46, 32)]  # os quatro eliminados somados
QUAEST_REGISTRO = {'Caiado': 0.36, 'Cury': 0.47, 'Zema': 0.36}   # como escrito no Adendo 18
PRIMEIRA = {'Caiado': ['PoderData|5-7/10', 'Quaest|10-13/10', 'AtlasIntel|3-8/10', 'Ipespe|6-8/10', 'Nexus|10-12/10'],
            'Cury': ['PoderData|5-7/10', 'Quaest|10-13/10', 'AtlasIntel|3-8/10', 'Ipespe|6-8/10'],
            'Zema': ['PoderData|5-7/10', 'Nexus|10-12/10']}
APOIOS = {
    'Zema': {'data': '05/10/2026', 'como': 'apoio explícito a Flávio, o primeiro presidenciável derrotado a anunciar; o Novo formalizou em 07/10',
             'fonte': 'https://sbtnews.sbt.com.br/noticia/eleicoes/apos-zema-novo-anuncia-apoio-a-flavio-bolsonaro-no-2-turno (07/10/2026 15:48)'},
    'Caiado': {'data': '06/10/2026', 'como': 'apoio individual em ato em Goiânia; o PSD ficou neutro e liberou os filiados',
               'fonte': 'https://www.diariodepernambuco.com.br/politica/2026/10/11726017-caiado-declara-apoio-a-flavio-bolsonaro-no-segundo-turno-em-ato-em-goiania.html (06/10/2026 21:24)'},
    'Cury': {'data': '08/10/2026', 'como': 'apoio condicionado a um termo de 8 compromissos assinado por Flávio; em 05/10 tinha anunciado "neutralidade absoluta"',
             'fonte': 'https://www.dgabc.com.br/Noticia/4351753/cury-oficializa-apoio-a-flavio-bolsonaro-sob-condicao-de-pacificacao-nacional (08/10/2026 19:23); neutralidade: https://tribunadejundiai.com.br/politica/eleicoes-2026/segundo-turno-posicionamento-candidatos-derrotados-2026/ (05/10/2026 16:31)'},
}


def log(msg):
    print(time.strftime('%H:%M:%S'), msg, file=sys.stderr, flush=True)


def fatia(f, l):
    return l / (l + f)


def referencias():
    out = {}
    for cand, linhas in DECL.items():
        ult = [(i, r, fatia(f, l)) for i, r, f, l, u in linhas if u]
        todas = [fatia(f, l) for _, _, f, l, _ in linhas]
        prim = [fatia(f, l) for i, r, f, l, _ in linhas if f'{i}|{r}' in PRIMEIRA[cand]]
        v = np.array([x for _, _, x in ult])
        k = len(v); dp = float(np.std(v, ddof=1)) if k > 1 else float('nan')
        o = {'institutos_ultima_rodada': [{'instituto': i, 'rodada': r, 'fatia_lula': x} for i, r, x in ult],
             'mediana': float(np.median(v)), 'minimo': float(v.min()), 'maximo': float(v.max()), 'k': k,
             'dp_entre_institutos': dp, 'ep_mediana_aprox': 1.2533 * dp / np.sqrt(k) if k > 1 else float('nan'),
             'mediana_todas_rodadas': float(np.median(todas)), 'n_rodadas': len(todas),
             'mediana_primeira_rodada': float(np.median(prim)), 'quaest_registro': QUAEST_REGISTRO[cand]}
        if cand == 'Cury':
            vi = np.append(v, fatia(IDEIA_CURY[2], IDEIA_CURY[3]))
            o['mediana_com_ideia'] = float(np.median(vi))
        if cand == 'Zema':
            o['leitura_T37_so_nexus'] = fatia(80, 12)
        out[cand] = o
    out['Datafolha_agregado_quatro'] = [{'rodada': r, 'fatia_lula': fatia(f, l)} for _, r, f, l in DATAFOLHA_AGREG]
    return out


# ---------------------------------------------------------------- base

def montar(d, cand):
    uf, mun, zona, loc = [], [], [], []
    M = []
    for k, v in d.items():
        if '1' not in v or '2' not in v:
            continue
        a, b = v['1'], v['2']; cv = cand.get(k, {})
        u, m, z, _ = k.split('|')
        uf.append(u); mun.append(f'{u}|{m}'); zona.append(f'{u}|{m}|{z}'); loc.append(chave_local(k, b))
        g = [cv.get(n, 0) for _, n in GRUPOS]
        M.append(g + [a['O'] - sum(g), a['B'] + a['N'], b['B'] + b['N'], a['comp'], b['comp'], a['L'], a['R'], b['L'], b['R'], a['O']])
    M = np.array(M, float)
    cod = lambda xs: np.unique(np.array(xs), return_inverse=True)[1]
    return {'uf': np.array(uf), 'mun': cod(mun), 'zona': cod(zona), 'loc': cod(loc), 'M': M}


C = {n: i for i, n in enumerate(['g0', 'g1', 'g2', 'g3', 'dem', 'BN1', 'BN2', 'comp1', 'comp2', 'L1', 'R1', 'L2', 'R2', 'O1'])}


def desenho(M, L2=None, R2=None):
    G = M[:, 0:4]; dem = M[:, C['dem']]
    qbn = M[:, C['BN1']] - M[:, C['BN2']]; dcomp = M[:, C['comp2']] - M[:, C['comp1']]
    L1, R1 = M[:, C['L1']], M[:, C['R1']]
    L2 = M[:, C['L2']] if L2 is None else L2; R2 = M[:, C['R2']] if R2 is None else R2
    base = np.column_stack([G, dem, qbn, dcomp])
    XL = np.column_stack([base, R1, L1]); yL = L2 - L1
    XR = np.column_stack([base, L1, R1]); yR = R2 - R1
    return XL, yL, XR, yR


def empilhado(B, mask, fe='loc', cl='loc', L2=None, R2=None):
    M = B['M'][mask]
    XL, yL, XR, yR = desenho(M, None if L2 is None else L2[mask], None if R2 is None else R2[mask])
    n = len(yL); Z0 = np.zeros((n, K))
    X = np.vstack([np.hstack([XL, Z0]), np.hstack([Z0, XR])]); y = np.concatenate([yL, yR])
    f = B[fe][mask]; c = B[cl][mask]
    FE = np.concatenate([2 * f, 2 * f + 1]); CL = np.concatenate([c, c])
    b, V, N, Gc = ols_cluster(y, X, FE, CL)
    out = {'secoes': int(n), 'linhas_informativas': N, 'clusters': Gc, 'por_grupo': {}}
    for i, (nm, _) in enumerate(GRUPOS):
        bl, bf = b[i], b[K + i]
        vl, vf, cov = V[i, i], V[K + i, K + i], V[i, K + i]
        t = bl + bf
        g = np.array([bf / t ** 2, -bl / t ** 2])
        vs = g @ np.array([[vl, cov], [cov, vf]]) @ g
        out['por_grupo'][nm] = {'b_L': float(bl), 'ep_b_L': float(np.sqrt(vl)), 'b_F': float(bf), 'ep_b_F': float(np.sqrt(vf)),
                                'soma': float(t), 's': float(bl / t), 'ep_s': float(np.sqrt(vs))}
    out['outros_coef'] = {('L:' if j == 0 else 'F:') + nm: [float(b[j * K + i]), float(np.sqrt(V[j * K + i, j * K + i]))]
                          for j in (0, 1) for i, nm in enumerate(NOMES) if i >= len(GRUPOS)}
    return out


def ponderado(B, mask, grupo):
    """Lula e Flávio separados (lib.fe_ols) com peso pelo comparecimento do 1º turno; s = b_L/(b_L+b_F), ep de b_L."""
    M = B['M'][mask]; XL, yL, XR, yR = desenho(M); w = M[:, C['comp1']]; g = B['loc'][mask]
    rl = fe_ols(yL, XL, g, w, NOMES); rr = fe_ols(yR, XR, g, w, NOMES)
    bl, bf = rl['coef'][grupo], rr['coef'][grupo]
    return {'b_L': bl, 'b_F': bf, 'soma': bl + bf, 's': bl / (bl + bf), 'ep_b_L': rl['ep'][grupo], 'ep_b_F': rr['ep'][grupo]}


def separado_sem_peso(B, mask, grupo):
    """Conferência: Lula sozinho por lib.fe_ols, sem peso (deve dar o mesmo b_L do empilhado)."""
    M = B['M'][mask]; XL, yL, _, _ = desenho(M)
    r = fe_ols(yL, XL, B['loc'][mask], None, NOMES)
    return {'b_L': r['coef'][grupo], 'ep_b_L': r['ep'][grupo]}


# ---------------------------------------------------------------- veredito

def veredito_uf(s, ep, ref):
    z50 = (s - LIM_50) / ep; zref = (s - ref) / ep; zlim = (s - ref - LIM_DIF) / ep
    inc = (s > LIM_50) and (s - ref >= LIM_DIF) and (z50 > Z) and (zref > Z)
    inc_lim = (s > LIM_50) and (s - ref >= LIM_DIF) and (z50 > Z) and (zlim > Z)
    coer = s <= ref + LIM_COER
    return {'s': s, 'ep': ep, 'ref': ref, 's_menos_ref': s - ref, 'z_contra_50': z50, 'z_contra_ref': zref,
            'z_contra_ref_mais_15': zlim, 'incoerencia': bool(inc), 'incoerencia_leitura_limiar': bool(inc_lim),
            'coerente': bool(coer), 'faixa': 'INCOERÊNCIA' if inc else ('COERENTE' if coer else 'ENTRE OS DOIS')}


def veredito(vs, chave='incoerencia'):
    n_inc = sum(v[chave] for v in vs.values()); n_coer = sum(v['coerente'] for v in vs.values())
    if n_inc >= 2:
        return 'INCOERÊNCIA'
    if n_coer == 3:
        return 'COERENTE'
    return 'INCONCLUSIVO'


# ---------------------------------------------------------------- principal

def main():
    d = carregar(sys.argv[1]); cand = carregar(sys.argv[2])['secoes']
    B = montar(d, cand); del d, cand
    M = B['M']; uf = B['uf']
    log(f"seções com os dois turnos: {len(uf)}")
    # identidade de b_L + b_F = 1: y_L + y_R = outros + queda do branco+nulo + variação do comparecimento
    XL, yL, XR, yR = desenho(M)
    ident = float(np.abs((yL + yR) - (M[:, C['O1']] + (M[:, C['BN1']] - M[:, C['BN2']]) + (M[:, C['comp2']] - M[:, C['comp1']]))).max())
    ref = referencias()
    res = {'teste': 'L4', 'registro': 'PRE-REGISTRO-2026-10-26.md, Adendo 18 (commit bc7decb, 2026-10-29 05:13:35 UTC)',
           'secoes_com_dois_turnos': int(len(uf)), 'identidade_max_desvio': ident, 'referencias': ref, 'apoios': APOIOS,
           'contexto_uf': {}, 'casa': {}, 'fora_de_casa': {}, 'robustez': {}, 'tercos': {}, 'calibracao': {}}

    # conferência com o T37 nacional (resultados/T7_T14_bweb.txt: Cury 0,596, Renan 0,542, Caiado 0,488, Zema 0,361)
    todos = np.ones(len(uf), bool)
    res['nacional'] = empilhado(B, todos); log('nacional ' + json.dumps({g: round(x['s'], 4) for g, x in res['nacional']['por_grupo'].items()}))

    for u, cnd in CASA.items():
        m = uf == u; Mi = M[m]; gi = GI[cnd]
        V1 = Mi[:, C['L1']] + Mi[:, C['R1']] + Mi[:, C['O1']]
        tot_nac = float(M[:, gi].sum())
        res['contexto_uf'][u] = {'candidato': cnd, 'secoes': int(m.sum()), 'votos_1T_candidato': float(Mi[:, gi].sum()),
                                 'pct_validos_1T_UF': 100 * float(Mi[:, gi].sum() / V1.sum()),
                                 'pct_do_total_nacional_dele': 100 * float(Mi[:, gi].sum() / tot_nac),
                                 'L1': float(Mi[:, C['L1']].sum()), 'R1': float(Mi[:, C['R1']].sum()),
                                 'L2': float(Mi[:, C['L2']].sum()), 'R2': float(Mi[:, C['R2']].sum()),
                                 'grupos_1T': {g: float(Mi[:, GI[g]].sum()) for g, _ in GRUPOS}}
        r = empilhado(B, m); res['casa'][u] = r
        log(f"{u} {cnd}: s {r['por_grupo'][cnd]['s']:.4f} ({r['por_grupo'][cnd]['ep_s']:.4f})")
        res['casa'][u]['conferencia_fe_ols_sem_peso'] = separado_sem_peso(B, m, cnd)
        res['fora_de_casa'][cnd] = empilhado(B, ~m)['por_grupo'][cnd]
        rob = {}
        rob['fe_zona'] = empilhado(B, m, fe='zona', cl='zona')['por_grupo'][cnd]
        rob['fe_municipio'] = empilhado(B, m, fe='mun', cl='mun')['por_grupo'][cnd]
        rob['peso_comparecimento_1T'] = ponderado(B, m, cnd)
        res['robustez'][u] = rob
        # terços pela fatia do candidato da casa nos válidos do 1º turno da seção
        sh = np.where(V1 > 0, Mi[:, gi] / np.where(V1 > 0, V1, 1), 0)
        q1, q2 = np.quantile(sh, [1 / 3, 2 / 3])
        idx = np.where(m)[0]; tt = {}
        for nm, sel in (('T1', sh <= q1), ('T2', (sh > q1) & (sh <= q2)), ('T3', sh > q2)):
            mm = np.zeros(len(uf), bool); mm[idx[sel]] = True
            x = empilhado(B, mm)['por_grupo'][cnd]
            x['fatia_media_pct'] = 100 * float(Mi[sel, gi].sum() / V1[sel].sum()); x['secoes'] = int(sel.sum())
            tt[nm] = x
        res['tercos'][u] = {'cortes_pct': [100 * float(q1), 100 * float(q2)], 'por_terco': tt}
        log(f"{u} robustez e terços prontos")

    # calibração: desvio de uma fração fixa dos votos de Flávio no 2º turno para Lula, em todas as seções
    L2, R2 = M[:, C['L2']], M[:, C['R2']]
    f_vira = float((L2.sum() - R2.sum()) / (2 * R2.sum()))
    res['calibracao']['fracao_que_vira'] = f_vira
    for nome, f in (('1pct', 0.01), ('vira', f_vira)):
        L2s, R2s = L2 + f * R2, R2 - f * R2
        res['calibracao'][nome] = {u: empilhado(B, uf == u, L2=L2s, R2=R2s)['por_grupo'][c] for u, c in CASA.items()}
    log('calibração pronta')

    # veredito
    vs, vs_reg, vs_todas, vs_prim, vs_max = {}, {}, {}, {}, {}
    for u, cnd in CASA.items():
        x = res['casa'][u]['por_grupo'][cnd]; rf = ref[cnd]
        vs[u] = veredito_uf(x['s'], x['ep_s'], rf['mediana'])
        vs_reg[u] = veredito_uf(x['s'], x['ep_s'], rf['quaest_registro'])
        vs_todas[u] = veredito_uf(x['s'], x['ep_s'], rf['mediana_todas_rodadas'])
        vs_prim[u] = veredito_uf(x['s'], x['ep_s'], rf['mediana_primeira_rodada'])
        vs_max[u] = veredito_uf(x['s'], x['ep_s'], rf['maximo'])
        # erro combinado (urna + dispersão entre institutos), fora do critério
        epc = float(np.sqrt(x['ep_s'] ** 2 + rf['ep_mediana_aprox'] ** 2)) if np.isfinite(rf['ep_mediana_aprox']) else float('nan')
        vs[u]['ep_combinado_com_pesquisa'] = epc
        vs[u]['z_contra_ref_combinado'] = (x['s'] - rf['mediana']) / epc if np.isfinite(epc) else float('nan')
    res['veredito'] = {'por_uf': vs, 'letra': veredito(vs), 'leitura_limiar': veredito(vs, 'incoerencia_leitura_limiar'),
                       'com_numeros_do_registro': {'por_uf': vs_reg, 'letra': veredito(vs_reg)},
                       'mediana_todas_rodadas': {'por_uf': vs_todas, 'letra': veredito(vs_todas)},
                       'primeira_rodada': {'por_uf': vs_prim, 'letra': veredito(vs_prim)},
                       'contra_maior_fatia_declarada': {'por_uf': vs_max, 'letra': veredito(vs_max)}}
    json.dump(res, open(sys.argv[3], 'w'), ensure_ascii=False, indent=1)
    open(sys.argv[4], 'w').write(texto(res))
    log('veredito ' + res['veredito']['letra'])


# ---------------------------------------------------------------- texto

def fn(x, nd=3, sinal=False):
    s = f'{x:+.{nd}f}' if sinal else f'{x:.{nd}f}'
    return s.replace('.', ',')


def fp(x, nd=1, sinal=False):
    return fn(100 * x, nd, sinal) + '%'


def fi(x):
    return f'{int(round(x)):,}'.replace(',', '.')


def texto(r):
    L = []; w = L.append
    ref = r['referencias']; ve = r['veredito']
    w('L4 do Adendo 18: os eleitores dos candidatos que apoiaram Flávio, no estado de cada um (bweb completo dos dois turnos)')
    w('Script: scripts/analisar_L4.py. Números completos: resultados/L4_bweb.json. Rodado em 29/10/2026 com secoes2026.json.gz')
    w('(bweb do 1º e do 2º turno) e candidatos2026_1t.json.gz (votos por candidato a presidente no 1º turno, por seção).')
    w('')
    w('Critério registrado (PRE-REGISTRO-2026-10-26.md, Adendo 18, commit bc7decb, 29/10/2026 05:13:35 UTC, antes de rodar):')
    w('  "Em GO (Caiado), MG (Zema) e SP (Cury): regressão do T8 com os grupos dos eliminados, dentro da UF, efeito fixo de')
    w('  local. s = b_L / (b_L + b_F) para o grupo do candidato da casa [...]. Referência externa: a mesma fatia declarada nas')
    w('  pesquisas do 2º turno com cruzamento por voto no 1º turno (mediana dos institutos [...]). Incoerência: s acima de 50%')
    w('  e acima da referência das pesquisas em 15 pontos ou mais, a mais de 3 erros-padrão, em pelo menos 2 das 3 UFs.')
    w('  Coerente: s até a referência mais 5 pontos nas 3. Entre os dois: inconclusivo."')
    w('')
    w(f'VEREDITO PELA LETRA: {ve["letra"]}')
    for u, cnd in CASA.items():
        v = ve['por_uf'][u]
        w(f'  {u} ({cnd}): s {fp(v["s"])} (ep {fn(100 * v["ep"], 2)} ponto), referência {fp(v["ref"])}, diferença {fn(100 * v["s_menos_ref"], 1, True)} pontos'
          f' (z {fn(v["z_contra_ref"], 1)}); contra 50%: z {fn(v["z_contra_50"], 1)}. Faixa: {v["faixa"]}.')
    w(f'  Leitura do "a mais de 3 erros-padrão" a partir do limiar (s - ref - 0,15): {ve["leitura_limiar"]}.')
    w('')
    w('Conferências:')
    w(f'  Identidade y_L + y_R = outros + queda do branco+nulo + variação do comparecimento: desvio máximo {fn(r["identidade_max_desvio"], 6)}')
    w('  voto, então b_L + b_F = 1 em cada regressão (soma na tabela abaixo).')
    nac = r['nacional']['por_grupo']
    w('  T37 nacional refeito com este código (registrado em resultados/T7_T14_bweb.txt: Cury 0,596, Renan 0,542, Caiado 0,488,')
    w('  Zema 0,361): ' + ', '.join(f'{g} {fn(x["b_L"])}' for g, x in nac.items()) + '.')
    for u, cnd in CASA.items():
        cf = r['casa'][u]['conferencia_fe_ols_sem_peso']; x = r['casa'][u]['por_grupo'][cnd]
        w(f'  {u}: b_L de {cnd} por lib.fe_ols (Lula sozinho) {fn(cf["b_L"], 4)} (ep {fn(cf["ep_b_L"], 4)}); empilhado {fn(x["b_L"], 4)} (ep {fn(x["ep_b_L"], 4)}).')
    w('')
    w('1. Apoios a Flávio no 2º turno (imprensa; conferido em resultados/contexto_2t_2026_pesquisa_verificada.json e de novo hoje)')
    for cnd, a in APOIOS.items():
        w(f'  {cnd}: {a["data"]}, {a["como"]}.')
        w(f'    {a["fonte"]}')
    w('')
    w('2. Contexto nas três UFs (soma das seções do bweb com os dois turnos)')
    for u, c in r['contexto_uf'].items():
        vl1 = c['L1'] / (c['L1'] + c['R1']); vl2 = c['L2'] / (c['L2'] + c['R2'])
        w(f'  {u}: {fi(c["secoes"])} seções; {c["candidato"]} {fi(c["votos_1T_candidato"])} votos no 1º turno ({fn(c["pct_validos_1T_UF"], 1)}% dos válidos da UF;'
          f' {fn(c["pct_do_total_nacional_dele"], 1)}% do total nacional dele).')
        w(f'      Lula entre os dois finalistas: {fp(vl1)} no 1º turno, {fp(vl2)} no 2º ({fn(100 * (vl2 - vl1), 2, True)} pontos).'
          f' Grupos no 1º turno: ' + ', '.join(f'{g} {fi(q)}' for g, q in c['grupos_1T'].items()) + '.')
    w('')
    w('3. Urna: regressão do T8 com grupos dentro da UF (Lula e Flávio empilhados, efeito fixo de local por candidato, erro agrupado por local)')
    for u, cnd in CASA.items():
        rr = r['casa'][u]
        w(f'  {u}: {fi(rr["secoes"])} seções, {fi(rr["linhas_informativas"])} linhas informativas, {fi(rr["clusters"])} locais.')
        for g, x in rr['por_grupo'].items():
            mark = '  <- candidato da casa' if g == cnd else ''
            w(f'    {g:<7} b_L {fn(x["b_L"])} ({fn(x["ep_b_L"])}) | b_F {fn(x["b_F"])} ({fn(x["ep_b_F"])}) | soma {fn(x["soma"], 4)} | s {fp(x["s"])} (ep {fn(100 * x["ep_s"], 2)}){mark}')
        oc = rr['outros_coef']
        w(f'    próprio no 1º turno: Lula {fn(oc["L:proprio_1T"][0], 3, True)}, Flávio {fn(oc["F:proprio_1T"][0], 3, True)}; adversário: Lula {fn(oc["L:adversario_1T"][0], 3, True)},'
          f' Flávio {fn(oc["F:adversario_1T"][0], 3, True)}.')
    w('  Em casa contra fora de casa (mesma regressão nas outras 26 UFs e no exterior) e no país (T37):')
    for u, cnd in CASA.items():
        x = r['casa'][u]['por_grupo'][cnd]; fo = r['fora_de_casa'][cnd]; na = nac[cnd]
        w(f'    {cnd}: em casa ({u}) {fp(x["s"])} ({fn(100 * x["ep_s"], 2)}); fora de casa {fp(fo["s"])} ({fn(100 * fo["ep_s"], 2)}); país {fp(na["s"])} ({fn(100 * na["ep_s"], 2)}).')
    w('')
    w('4. Referência: fatia de Lula entre os que escolheram um finalista, declarada nas pesquisas por voto no 1º turno')
    for cnd in ('Caiado', 'Cury', 'Zema'):
        rf = ref[cnd]
        w(f'  {cnd}: ' + '; '.join(f'{x["instituto"]} {x["rodada"]} {fp(x["fatia_lula"])}' for x in rf['institutos_ultima_rodada'])
          + f'. Mediana {fp(rf["mediana"])} ({rf["k"]} institutos; de {fp(rf["minimo"])} a {fp(rf["maximo"])}).')
        extra = f'    Todas as {rf["n_rodadas"]} rodadas conferidas: mediana {fp(rf["mediana_todas_rodadas"])}; primeira rodada após o 1º turno: {fp(rf["mediana_primeira_rodada"])};'
        extra += f' número escrito no registro ("Quaest já conhecida"): {fp(rf["quaest_registro"], 0)}.'
        if 'mediana_com_ideia' in rf:
            extra += f' Com a Meio/Ideia (rodada não confirmada, 57,1%): {fp(rf["mediana_com_ideia"])}.'
        if 'leitura_T37_so_nexus' in rf:
            extra += f' Leitura do T37 (só Nexus): {fp(rf["leitura_T37_so_nexus"])}.'
        w(extra)
        if np.isfinite(rf['ep_mediana_aprox']):
            w(f'    Dispersão entre institutos: dp {fn(100 * rf["dp_entre_institutos"], 1)} pontos; erro da mediana aproximado {fn(100 * rf["ep_mediana_aprox"], 1)} pontos.')
    w('  Datafolha (só o agregado dos quatro eliminados, fora da mediana): ' + '; '.join(f'{x["rodada"]} {fp(x["fatia_lula"])}' for x in ref['Datafolha_agregado_quatro']) + '.')
    w('  Nenhuma pesquisa estadual de GO, MG ou SP feita depois do 1º turno com cruzamento por voto no 1º turno foi encontrada (buscas')
    w('  de hoje; as estaduais achadas são de julho a setembro, antes do 1º turno). A referência é nacional; a urna é da UF.')
    w('')
    w('5. Critério aplicado, por UF')
    w('  UF | s urna | ref | s - ref | z (s-ref) | z (s-50%) | incoerência? | coerente (s <= ref+5)? | z com erro da pesquisa')
    for u, cnd in CASA.items():
        v = ve['por_uf'][u]
        w(f'  {u} | {fp(v["s"])} | {fp(v["ref"])} | {fn(100 * v["s_menos_ref"], 1, True)} | {fn(v["z_contra_ref"], 1)} | {fn(v["z_contra_50"], 1)} | '
          f'{"sim" if v["incoerencia"] else "não"} | {"sim" if v["coerente"] else "não"} | {fn(v["z_contra_ref_combinado"], 1) if np.isfinite(v["z_contra_ref_combinado"]) else "sem dado"}')
    w('  Leituras da referência (fora da principal):')
    for nome, chave in (('números escritos no registro', 'com_numeros_do_registro'), ('mediana de todas as rodadas', 'mediana_todas_rodadas'),
                        ('primeira rodada após o 1º turno', 'primeira_rodada'), ('maior fatia declarada por um instituto', 'contra_maior_fatia_declarada')):
        x = ve[chave]
        w(f'    {nome}: {x["letra"]} (' + '; '.join(f'{u} s - ref {fn(100 * x["por_uf"][u]["s_menos_ref"], 1, True)}, {x["por_uf"][u]["faixa"]}' for u in CASA) + ')')
    w('')
    w('6. Robustez da urna (fora do critério): s do candidato da casa')
    w('  UF | principal (efeito fixo de local) | efeito fixo de zona | efeito fixo de município | peso pelo comparecimento do 1º turno')
    for u, cnd in CASA.items():
        x = r['casa'][u]['por_grupo'][cnd]; rb = r['robustez'][u]
        w(f'  {u} | {fp(x["s"])} ({fn(100 * x["ep_s"], 2)}) | {fp(rb["fe_zona"]["s"])} ({fn(100 * rb["fe_zona"]["ep_s"], 2)}) | '
          f'{fp(rb["fe_municipio"]["s"])} ({fn(100 * rb["fe_municipio"]["ep_s"], 2)}) | {fp(rb["peso_comparecimento_1T"]["s"])} ({fn(100 * rb["peso_comparecimento_1T"]["ep_b_L"], 2)})')
    w('  Heterogeneidade: s em terços de seções pela fatia do candidato da casa nos válidos do 1º turno (dentro da UF)')
    for u, cnd in CASA.items():
        t = r['tercos'][u]
        w(f'  {u} ({cnd}; cortes {fn(t["cortes_pct"][0], 1)}% e {fn(t["cortes_pct"][1], 1)}%): ' + '; '.join(
            f'{k} (fatia média {fn(x["fatia_media_pct"], 1)}%) s {fp(x["s"])} ({fn(100 * x["ep_s"], 2)})' for k, x in t['por_terco'].items()))
    w('')
    w('7. Calibração (fora do critério): desvio simulado de uma fração fixa dos votos de Flávio no 2º turno para Lula, em todas as seções')
    cb = r['calibracao']
    w(f'  Fração que equivale a virar o resultado nacional: {fp(cb["fracao_que_vira"], 2)} dos votos de Flávio no 2º turno.')
    for nome, rot in (('1pct', '1%'), ('vira', fp(cb['fracao_que_vira'], 2))):
        w(f'  Desvio de {rot}: ' + '; '.join(f'{u} s {fp(cb[nome][u]["s"])} (sem desvio {fp(r["casa"][u]["por_grupo"][c]["s"])})' for u, c in CASA.items()) + '.')
    w('  Um desvio que tira uma fração fixa de todos os votos de Flávio mexe pouco em s: ele cai quase todo no coeficiente dos próprios')
    w('  votos de Flávio. O L4 só enxerga um desvio que pegue justamente os eleitores dos eliminados, ou que se concentre onde eles moram.')
    w('')
    # comparação post hoc com Renan (neutro), feita depois de ver s; não muda o veredito
    rn = [fatia(43, 33), fatia(51, 25), fatia(33.5, 31.9), fatia(40, 20)]
    med_rn = float(np.median(rn)); s_rn = nac['Renan']['s']
    w('8. Leitura')
    ok50 = [u for u, c in CASA.items() if r['casa'][u]['por_grupo'][c]['s'] < LIM_50]
    w(f'  - A premissa lógica do teste ("os eleitores deles deveriam ir mais para Flávio que para Lula, principalmente em casa") é o que a')
    w(f'    própria urna mostra em {" e ".join(ok50)}: entre os eleitores de Caiado em GO que escolheram um finalista, '
      f'{fp(1 - r["casa"]["GO"]["por_grupo"]["Caiado"]["s"])} foram para Flávio; entre os de Zema em MG,'
      f' {fp(1 - r["casa"]["MG"]["por_grupo"]["Zema"]["s"])}. Em SP, os de Cury foram {fp(r["casa"]["SP"]["por_grupo"]["Cury"]["s"])} para Lula,')
    w('    mas duas das quatro pesquisas que separaram Cury (Quaest e AtlasIntel) também davam maioria para Lula nesse grupo.')
    w('  - Como s fica abaixo de 50% em GO e MG a mais de 5 erros-padrão, a INCOERÊNCIA do registro (que pede s acima de 50% em 2 das 3)')
    w('    não sai com nenhuma leitura da referência, nem com efeito fixo de zona ou de município, nem com peso.')
    w('  - Também não dá COERENTE: nas três UFs a urna põe mais eleitores do candidato da casa em Lula do que as pesquisas declaravam, de')
    w(f'    {fn(100 * min(ve["por_uf"][u]["s_menos_ref"] for u in CASA), 1)} a {fn(100 * max(ve["por_uf"][u]["s_menos_ref"] for u in CASA), 1)} pontos.'
      ' É o mesmo desvio que o T37 já tinha mostrado no país inteiro.')
    dif = {c: (r['casa'][u]['por_grupo'][c]['s'] - r['fora_de_casa'][c]['s'],
               np.sqrt(r['casa'][u]['por_grupo'][c]['ep_s'] ** 2 + r['fora_de_casa'][c]['ep_s'] ** 2)) for u, c in CASA.items()}
    w('  - Em casa contra fora de casa: em casa a fatia de Lula é menor para os três (' + '; '.join(
        f'{c} {fn(100 * x, 1, True)} pontos, z {fn(x / e, 1, True)}' for c, (x, e) in dif.items()) + '), como a lógica do')
    w('    apoio prevê; a diferença é pequena perto da distância entre a urna e as pesquisas.')
    w(f'  - Comparação post hoc (feita depois de ver s, fora do critério): Renan, que não apoiou ninguém, tem o mesmo desvio. Urna no')
    w(f'    país {fp(s_rn)}; mediana declarada da última rodada de PoderData, Quaest, AtlasIntel e Ipespe {fp(med_rn)}'
      f' ({fn(100 * (s_rn - med_rn), 1, True)} pontos). Nos três estados, Renan fica em ' + ', '.join(
        f'{u} {fp(r["casa"][u]["por_grupo"]["Renan"]["s"])}' for u in CASA) + '.')
    w('    Ou seja, a distância entre urna e pesquisa não é maior para os eleitores de quem apoiou Flávio do que para os do neutro.')
    w('  - O que o teste não consegue separar: a distância urna menos pesquisa aparece igual se (a) a regressão ecológica erra (o')
    w('    eleitor de Caiado não é a seção que tem mais votos de Caiado), (b) as subamostras das pesquisas erram (cada grupo tem cerca')
    w('    de 2% da amostra; a Quaest deu margem de 17 a 24 pontos nesses grupos, e o PoderData variou de 42% a 58% de Flávio entre os')
    w('    eleitores de Cury em seis rodadas), (c) houve decisão tardia ou voto escondido nesses grupos, ou (d) houve desvio de votos')
    mv = max(abs(r['calibracao']['vira'][u]['s'] - r['casa'][u]['por_grupo'][c]['s']) for u, c in CASA.items())
    dmin = min(ve['por_uf'][u]['s_menos_ref'] for u in CASA); dmax = max(ve['por_uf'][u]['s_menos_ref'] for u in CASA)
    w(f'    dirigido a esses eleitores. Pela calibração, um desvio do tamanho do que vira o resultado, sem escolher o eleitor, move s em')
    w(f'    até {fn(100 * mv, 1)} pontos; a distância de {fn(100 * dmin, 0)} a {fn(100 * dmax, 0)} pontos não vem de um desvio uniforme. Ela teria de vir de (a), (b),')
    w('    (c) ou de um desvio dirigido a esses eleitores.')
    w('')
    w('9. Desvios e leituras declaradas')
    w('  - Referência: "mediana dos institutos" lida como a mediana, entre institutos, da última rodada de cada um que publicou o')
    w('    candidato separado (uma rodada por instituto). Para Zema, a última do PoderData com Zema separado é a de 5-7/10 (depois ele')
    w('    entra em "outro"); o T37 tinha usado só a Nexus. As duas dão perto de 13%.')
    w('  - Os números escritos no registro como "Quaest já conhecida" (Caiado 36%, Cury 47%, Zema 36%) não batem com nenhuma Quaest')
    w('    publicada e conferida: a Quaest de 17-20/10 dá Caiado 26,9% e Cury 59,3%, a de 10-13/10 dá Caiado 35,4% e Cury 53,1%, e a')
    w('    Quaest nunca separou Zema. O 47% de Cury coincide com a mediana dos quatro institutos e o 36% de Zema coincide com o b_L')
    w('    nacional da urna no T37 (0,361); parece erro na hora de escrever. A principal usa os valores conferidos; os números do')
    w('    registro entram como leitura ao lado e dão o mesmo veredito.')
    w('  - "A mais de 3 erros-padrão" lido a partir de zero para as duas comparações ((s - 50%)/ep e (s - ref)/ep); a leitura a')
    w('    partir do limiar ((s - ref - 15 pontos)/ep) dá o mesmo veredito.')
    w('  - O erro-padrão do critério é só o da urna (regressão). O da pesquisa, bem maior, sai ao lado (seção 5); com Zema, a')
    w('    dispersão de dois institutos que concordam subestima esse erro.')
    w('  - A referência é nacional e a urna é da UF: nenhuma pesquisa estadual pós-1º turno com o cruzamento foi achada. Como a urna')
    w('    mostra o eleitor da casa um pouco mais Flávio que o de fora, uma referência estadual com o mesmo padrão seria ainda mais')
    w('    baixa que a nacional, o que aumentaria a distância, não a diminuiria.')
    w('  - Meio/Ideia (Cury, rodada não confirmada) e Datafolha (só o agregado dos quatro) ficam fora da mediana por candidato.')
    w('  - Regressão: a do T8 registrado para 2026, com os grupos dos eliminados, efeito fixo de local, sem peso, erro agrupado por')
    w('    local; Lula e Flávio empilhados para ter a covariância (os coeficientes são os mesmos das regressões separadas, conferido).')
    w('')
    w('10. O que ficou de fora e limites')
    w('  - Inferência ecológica dentro do local de votação: s não é o voto de cada eleitor de Caiado, Zema ou Cury. Mistura quem mudou')
    w('    de voto com a troca de eleitores entre os turnos. Em MG, onde Zema teve 0,8% dos válidos, s muda muito com a especificação')
    w(f'    ({fp(r["casa"]["MG"]["por_grupo"]["Zema"]["s"])} com efeito fixo de local, {fp(r["robustez"]["MG"]["fe_zona"]["s"])} de zona, {fp(r["robustez"]["MG"]["fe_municipio"]["s"])} de município): o número de MG é frágil.')
    w('  - Tamanho das subamostras das pesquisas não publicado; só percentuais. Não há pesquisa com Zema separado depois de 12/10.')
    w('  - Nenhuma eleição anterior foi usada. A régua é externa à urna (pesquisas de 2026) e interna a 2026 (fora de casa, Renan).')
    w('  - O L4 não testa a contagem da urna em si; isso fica para os testes físicos e documentais (L7, L8).')
    return '\n'.join(L) + '\n'


if __name__ == '__main__':
    main()
