"""T17 do pré-registro (adendos 9, 10 e 11): atributo da máquina dentro do mesmo local de votação.

y = variação da fatia de Lula entre os finalistas (2º menos 1º turno), peso L2+R2, efeito fixo de local, erro agrupado por local.
Covariáveis: log dos aptos, variação do comparecimento, fatia de Lula no 1º turno. Repete com y = variação do
branco+nulo e y = variação do comparecimento; placebo com y = fatia de Lula no 1º turno.
  Adendo 9 (só a amostra): modelo da urna do 2º turno (referência UE2022), urna diferente entre os turnos e, na
    subamostra com log, contingência no 2º turno. Contribuição nacional = coeficiente vezes a fração do grupo na frota
    (modelos) ou na amostra (urna trocada, contingência, que não têm fração nacional na base).
  Adendos 10 e 11: antigas (UE2013, UE2015) contra novas (UE2020, UE2022), só nos locais que têm os dois grupos
    (os 119 do país), com e sem as variáveis de fila do 1º turno. Na união inteira, só como robustez.
  Adendo 11: um modelo só (UE2020 contra UE2022; UE2013 contra UE2015) com a amostra mais o prefixo do Adendo 10.
Salvaguardas: cada coeficiente sai com o número de locais que o identificam (para um modelo contra a referência,
os locais que têm os dois; para um indicador isolado, os locais em que ele varia); com menos de 30, o veredito é
SEM PODER. Colunas colineares depois do efeito fixo são descartadas e listadas.
Uso: python3 -I analisar_maquina.py <secoes2026_1t.json.gz> <amostra_2t.json.gz> <T3_logs.json>
       [--extensao_pares <pasta_bu>[,...]] [--extensao_contraste <pasta_bu>[,...]]
"""
import os as _os, sys as _sys
_sys.path.insert(0, _os.path.dirname(_os.path.abspath(__file__)))
import collections, json, sys, warnings
import numpy as np
from lib import carregar, chave_local, fe_ols, demean
from modelos import modelo
warnings.filterwarnings('ignore')

REF = 'UE2022'
ANTIGAS = ('UE2013', 'UE2015')
MIN_LOCAIS = 30


def ler_extensao(pasta):
    """Boletins do 2º turno baixados para a extensão (só -bu.dat), no formato da amostra."""
    import os
    from decodificar import ler_bu, bu_para_secao
    out = {}
    for uf in sorted(os.listdir(pasta)):
        for m in sorted(os.listdir(os.path.join(pasta, uf))):
            for z in sorted(os.listdir(os.path.join(pasta, uf, m))):
                for sc in sorted(os.listdir(os.path.join(pasta, uf, m, z))):
                    p = os.path.join(pasta, uf, m, z, sc)
                    bus = sorted(f for f in os.listdir(p) if f.endswith('-bu.dat'))
                    if not bus:
                        continue
                    s, g = bu_para_secao(ler_bu(os.path.join(p, bus[-1])))
                    if s is not None:
                        out[f'{uf.upper()}|{int(m)}|{int(z)}|{int(sc)}'] = {'2': s}
    return out


def horas(x):
    x = (x or '').replace(':', '')
    try:
        return int(x[:2]) + int(x[2:4]) / 60
    except ValueError:
        return float('nan')


def montar(d1, am, logs):
    rows = []
    for k, v in am.items():
        b = v.get('2'); a = d1.get(k, {}).get('1')
        if not a or not b or a['comp'] <= 0 or b['comp'] <= 0 or a['L'] + a['R'] <= 0 or b['L'] + b['R'] <= 0:
            continue
        lg = logs.get(k)
        rows.append({'k': k, 'loc': chave_local(k, b), 'mod': modelo(b['urna'], 2026), 'dif': a['urna'] != b['urna'],
                     'enc1': horas(a.get('enc')), 'cont': (lg['contingencia'] if lg else None), 'apt': b['apt'],
                     'L1': a['L'], 'R1': a['R'], 'BN1': a['B'] + a['N'] + a.get('c28', 0), 'C1': a['comp'],
                     'L2': b['L'], 'R2': b['R'], 'BN2': b['B'] + b['N'], 'C2': b['comp']})
    return rows


def desfechos(rows):
    L1, R1, BN1, C1, L2, R2, BN2, C2, apt = [np.array([r[c] for r in rows], float) for c in
                                            ('L1', 'R1', 'BN1', 'C1', 'L2', 'R2', 'BN2', 'C2', 'apt')]
    fat1 = 100 * L1 / (L1 + R1); fat2 = 100 * L2 / (L2 + R2)
    y_comp = 100 * (C2 - C1) / apt
    la = np.log(apt)
    return {'virada': (fat2 - fat1, np.column_stack([la, y_comp, fat1]), ['log_aptos', 'var_comparecimento', 'fatia_lula_1t']),
            'var_branco_nulo': (100 * (BN2 / C2 - BN1 / C1), np.column_stack([la, y_comp, fat1]), ['log_aptos', 'var_comparecimento', 'fatia_lula_1t']),
            'var_comparecimento': (y_comp, np.column_stack([la, fat1]), ['log_aptos', 'fatia_lula_1t']),
            'placebo_fatia_1t': (fat1, la.reshape(-1, 1), ['log_aptos'])}


def regredir(rows, nomes_ind, ind, y, cov, cov_nomes):
    """Efeito fixo de local. Descarta colunas sem variação dentro do local ou colineares com as anteriores, e conta
    os locais que identificam cada indicador."""
    loc = np.array([r['loc'] for r in rows]); w = np.array([r['L2'] + r['R2'] for r in rows], float)
    X = np.column_stack([ind, cov]) if cov is not None else ind
    nomes = nomes_ind + cov_nomes
    _, g = np.unique(loc, return_inverse=True)
    Xd = demean(X, g, w) * np.sqrt(w)[:, None]
    keep, descart = [], []
    for j in range(X.shape[1]):
        ss = float(Xd[:, j] @ Xd[:, j])
        if ss <= 1e-6 * max(1.0, np.sum(w)):
            descart.append(nomes[j]); continue
        if keep:
            K = Xd[:, keep]
            res = Xd[:, j] - K @ np.linalg.lstsq(K, Xd[:, j], rcond=None)[0]
            if float(res @ res) <= 1e-8 * ss:
                descart.append(nomes[j]); continue
        keep.append(j)
    r = fe_ols(y, X[:, keep], loc, w, [nomes[j] for j in keep])
    ident = {}
    for j, nm in enumerate(nomes_ind):
        ident[nm] = int(len(np.unique(g[np.abs(Xd[:, j]) > 1e-9])))
    r['descartadas'] = descart; r['locais_identificadores'] = ident
    return r


def bloco(rows, gnomes, ind):
    res = {}
    for yn, (y, cov, cn) in desfechos(rows).items():
        r = regredir(rows, gnomes, ind, y, cov, cn)
        res[yn] = {'n': r['n'], 'locais': r['grupos'], 'descartadas': r['descartadas'],
                   'locais_identificadores': r['locais_identificadores'],
                   'coef': {g: r['coef'].get(g) for g in gnomes}, 'ep': {g: r['ep'].get(g) for g in gnomes}}
    return res


def adendo9(rows, frota):
    n = len(rows)
    mods = sorted({r['mod'] for r in rows if r['mod'] and r['mod'] != REF})
    grupos = {m: np.array([1.0 if r['mod'] == m else 0.0 for r in rows]) for m in mods}
    grupos['urna_diferente_entre_turnos'] = np.array([1.0 if r['dif'] else 0.0 for r in rows])
    frac = {m: (frota[m], 'frota') for m in mods}
    frac['urna_diferente_entre_turnos'] = (float(grupos['urna_diferente_entre_turnos'].mean()), 'amostra')
    com_mod = np.array([r['mod'] is not None for r in rows])
    reg = {'modelos': bloco([r for r, o in zip(rows, com_mod) if o], mods, np.column_stack([grupos[m][com_mod] for m in mods])),
           'urna_diferente': bloco(rows, ['urna_diferente_entre_turnos'], grupos['urna_diferente_entre_turnos'].reshape(-1, 1))}
    idx = np.array([i for i, r in enumerate(rows) if r['cont'] is not None])
    if len(idx):
        c = np.array([1.0 if rows[i]['cont'] else 0.0 for i in idx])
        frac['contingencia_2t'] = (float(c.mean()), 'subamostra com log')
        reg['contingencia_2t'] = bloco([rows[i] for i in idx], ['contingencia_2t'], c.reshape(-1, 1))
    # com vários indicadores de modelo, o coeficiente de m contra a referência só se identifica onde m e a referência
    # estão no mesmo local (locais que misturam só outros modelos identificam diferenças entre eles, não contra a referência)
    por = collections.defaultdict(set)
    for r in rows:
        if r['mod']: por[r['loc']].add(r['mod'])
    direto = {m: sum(1 for s_ in por.values() if m in s_ and REF in s_) for m in mods}
    leitura = {}; soma = 0.0
    for rg in reg.values():
        v, cp, p = rg['virada'], rg['var_comparecimento'], rg['placebo_fatia_1t']
        for gname, b in v['coef'].items():
            h = direto.get(gname, v['locais_identificadores'][gname])
            if b is None:
                leitura[gname] = {'veredito': 'NAO IDENTIFICADO', 'locais_identificadores': h}; continue
            se = v['ep'][gname]; f, fonte = frac[gname]; contrib = b * f; soma += abs(contrib)
            mde = 2.8 * se
            sinal = (contrib > 0.3 and b > 4 * se and abs(p['coef'].get(gname) or 0) < 0.1
                     and abs(cp['coef'].get(gname) or 0) < 2 * (cp['ep'].get(gname) or 0))
            ver = ('SEM PODER (poucos locais)' if h < MIN_LOCAIS else 'SINAL' if sinal else
                   'SEM PODER (efeito mínimo detectável acima de 0,5)' if mde > 0.5 else
                   'SEM SINAL' if abs(b) < 0.5 else 'INCONCLUSIVO')
            leitura[gname] = {'coef': b, 'ep': se, 'locais_identificadores': h, 'fracao': f, 'fonte_da_fracao': fonte,
                              'contribuicao_pontos': contrib, 'efeito_minimo_detectavel': mde,
                              'placebo_coef': p['coef'].get(gname), 'efeito_comparecimento': cp['coef'].get(gname),
                              'veredito': ver}
    return {'secoes': n, 'locais': len({r['loc'] for r in rows}), 'contagem_modelo': dict(collections.Counter(str(r['mod']) for r in rows)),
            'urna_diferente': int(sum(r['dif'] for r in rows)), 'regressoes': reg, 'leitura': leitura,
            'contribuicao_somada_abs': soma}


def contraste(rows, restringir=True):
    """Adendos 10 e 11: antigas contra novas, versões sem e com fila do 1º turno."""
    rows = [r for r in rows if r['mod'] is not None and np.isfinite(r['enc1'])]
    por = collections.defaultdict(set)
    for r in rows: por[r['loc']].add(r['mod'] in ANTIGAS)
    dois = {l for l, s in por.items() if len(s) == 2}
    if restringir:
        rows = [r for r in rows if r['loc'] in dois]
    out = {'secoes': len(rows), 'locais': len({r['loc'] for r in rows}), 'locais_com_os_dois_grupos': len(dois), 'versoes': {}}
    if not rows:
        out['veredito'] = 'NAO IDENTIFICADO'; return out
    ant = np.array([[1.0 if r['mod'] in ANTIGAS else 0.0] for r in rows])
    e = np.array([r['enc1'] for r in rows]); exc = np.clip(e - 17, 0, None); tarde = (e > 18).astype(float)
    ds = desfechos(rows)
    for nome, extra, en in (('sem_fila', None, []), ('com_fila', np.column_stack([exc, tarde]), ['horas_apos_17h_1t', 'encerrou_depois_18h_1t'])):
        res = {}
        for yn, (y, cov, cn) in list(ds.items()) + [('encerramento_1t_horas', (e, ds['placebo_fatia_1t'][1], ['log_aptos']))]:
            if extra is not None and yn in ('virada', 'var_branco_nulo', 'var_comparecimento'):
                cov = np.column_stack([cov, extra]); cn = cn + en
            r = regredir(rows, ['antiga'], ant, y, cov, cn)
            res[yn] = {'coef_antiga': r['coef'].get('antiga'), 'ep': r['ep'].get('antiga'), 'n': r['n'], 'locais': r['grupos'],
                       'locais_identificadores': r['locais_identificadores']['antiga'], 'descartadas': r['descartadas']}
        out['versoes'][nome] = res
    v0, v1 = out['versoes']['sem_fila'], out['versoes']['com_fila']
    b0, s0 = v0['virada']['coef_antiga'], v0['virada']['ep']; b1 = v1['virada']['coef_antiga']
    h = v0['virada']['locais_identificadores']
    if b0 is None or b1 is None:
        out['veredito'] = 'NAO IDENTIFICADO'; return out

    def sinal(v):
        b, se = v['virada']['coef_antiga'], v['virada']['ep']
        return (b <= -1.0 and -b > 4 * se and abs(v['placebo_fatia_1t']['coef_antiga']) < 1.5
                and abs(v['var_comparecimento']['coef_antiga']) < 1.0)
    out['contribuicao_se_novas_alteradas'] = -b0 * 0.80
    out['efeito_minimo_detectavel'] = 2.8 * s0
    out['veredito'] = ('SEM PODER (poucos locais)' if h < MIN_LOCAIS else 'SINAL' if sinal(v0) and sinal(v1) else
                       'SEM SINAL' if abs(b0) < 0.5 and s0 <= 0.2 and abs(b1) < 0.5 else
                       'PODER LIMITADO' if s0 > 0.3 else 'INCONCLUSIVO')
    out['leitura_de_fila'] = bool(abs(b1) < 0.5 * abs(b0) and v0['encerramento_1t_horas']['coef_antiga'] > 0)
    return out


def um_modelo(rows, frota):
    pares = {}
    for a, b in (('UE2020', 'UE2022'), ('UE2013', 'UE2015')):
        sub = [r for r in rows if r['mod'] in (a, b)]
        ind = np.array([[1.0 if r['mod'] == a else 0.0] for r in sub])
        res = {}
        for yn, (y, cov, cn) in desfechos(sub).items():
            if yn == 'var_branco_nulo':
                continue
            r = regredir(sub, [a], ind, y, cov, cn)
            res[yn] = {'coef': r['coef'].get(a), 'ep': r['ep'].get(a), 'n': r['n'], 'locais_identificadores': r['locais_identificadores'][a]}
        b_, se = res['virada']['coef'], res['virada']['ep']; h = res['virada']['locais_identificadores']
        res['ic95'] = [b_ - 1.96 * se, b_ + 1.96 * se]
        res['contribuicao_se_alterado_' + a] = b_ * frota[a]
        res['contribuicao_se_alterado_' + b] = -b_ * frota[b]
        res['efeito_necessario_para_decidir_sozinho_' + a] = 1.79 / frota[a]
        res['efeito_necessario_para_decidir_sozinho_' + b] = 1.79 / frota[b]
        res['efeito_minimo_detectavel'] = 2.8 * se
        res['veredito'] = ('SEM PODER (poucos locais)' if h < MIN_LOCAIS else
                           'SEM PODER (efeito mínimo detectável acima de 0,5)' if 2.8 * se > 0.5 else
                           'SEM SINAL' if abs(b_) < 0.5 else 'INCONCLUSIVO')
        pares[f'{a}_contra_{b}'] = res
    return pares


def main():
    d1 = carregar(sys.argv[1]); am = carregar(sys.argv[2]); logs = json.load(open(sys.argv[3]))['2']
    arg = lambda f: sys.argv[sys.argv.index(f) + 1].split(',') if f in sys.argv else []
    cont = collections.Counter(modelo(v['1']['urna'], 2026) for v in d1.values() if v.get('1'))
    tot = sum(cont.values()); frota = {m: c / tot for m, c in cont.items() if m}

    def uniao(pastas):
        u = dict(am); n = 0
        for p in pastas:
            for k, v in ler_extensao(p).items():
                if k not in u: u[k] = v; n += 1
        return u, n
    rows_am = montar(d1, am, logs)
    am_p, n_p = uniao(arg('--extensao_pares'))
    rows_p = montar(d1, am_p, logs)
    am_c, n_c = uniao(arg('--extensao_pares') + arg('--extensao_contraste'))
    rows_c = montar(d1, am_c, logs)
    out = {'frota_1t': frota, 'adendo9_amostra': adendo9(rows_am, frota),
           'adendo11_um_modelo': {'secoes': len(rows_p), 'secoes_da_extensao': n_p, 'pares': um_modelo(rows_p, frota)},
           'adendo11_um_modelo_robustez_uniao': {'secoes': len(rows_c), 'pares': um_modelo(rows_c, frota)},
           'adendo10_11_antigas_contra_novas': dict(contraste(rows_c), secoes_baixadas_extensao=n_c),
           'antigas_contra_novas_robustez_uniao_sem_restringir': contraste(rows_c, restringir=False)}
    print(json.dumps(out, ensure_ascii=False, indent=1))


if __name__ == '__main__':
    main()
