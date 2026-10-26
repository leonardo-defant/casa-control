"""T17 do pré-registro (adendo 9): atributo da máquina dentro do mesmo local de votação.

y = variação da fatia de Lula entre os finalistas (2º menos 1º turno), peso L2+R2, efeito fixo de local, erro agrupado por local.
Indicadores: modelo da urna do 2º turno (referência UE2022), urna diferente entre os turnos e, na subamostra com log,
contingência no 2º turno. Covariáveis: log dos aptos, variação do comparecimento, fatia de Lula no 1º turno.
Repete com y = variação do branco+nulo e y = variação do comparecimento; placebo com y = fatia de Lula no 1º turno.
Adendo 10: contraste urnas antigas (UE2013, UE2015) contra novas (UE2020, UE2022), com e sem as variáveis de fila
do 1º turno (horário de encerramento e encerramento depois das 18h), na união da amostra com a extensão dirigida.
Uso: python3 -I analisar_maquina.py <secoes2026_1t.json.gz> <amostra_2t.json.gz> <T3_logs.json> [--extensao <pasta_bu>]
"""
import os as _os, sys as _sys
_sys.path.insert(0, _os.path.dirname(_os.path.abspath(__file__)))
import collections, json, sys, warnings
import numpy as np
from lib import carregar, chave_local, fe_ols, demean
from modelos import modelo
warnings.filterwarnings('ignore')

REF = 'UE2022'


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
                     'enc1': horas(a.get('enc')),
                     'cont': (lg['contingencia'] if lg else None), 'apt': b['apt'],
                     'L1': a['L'], 'R1': a['R'], 'BN1': a['B'] + a['N'] + a.get('c28', 0), 'C1': a['comp'],
                     'L2': b['L'], 'R2': b['R'], 'BN2': b['B'] + b['N'], 'C2': b['comp']})
    return rows


def regredir(rows, nomes_ind, ind, y, cov, cov_nomes):
    """Retira colunas sem variação dentro do local antes de estimar."""
    loc = np.array([r['loc'] for r in rows]); w = np.array([r['L2'] + r['R2'] for r in rows], float)
    X = np.column_stack([ind, cov]) if cov is not None else ind
    nomes = nomes_ind + cov_nomes
    _, g = np.unique(loc, return_inverse=True)
    Xd = demean(X, g, w)
    keep = [j for j in range(X.shape[1]) if np.sum(w * Xd[:, j] ** 2) > 1e-6 * max(1.0, np.sum(w))]
    r = fe_ols(y, X[:, keep], loc, w, [nomes[j] for j in keep])
    return r


def contraste(rows, y_virada, y_bn, y_comp, fat1, apt):
    """Adendo 10: antigas contra novas, versões sem e com fila do 1º turno."""
    ant = np.array([1.0 if r['mod'] in ('UE2013', 'UE2015') else 0.0 for r in rows])
    ok = np.array([r['mod'] is not None for r in rows])
    enc1 = np.array([r['enc1'] for r in rows]); ok &= np.isfinite(enc1)
    sub = [r for r, o in zip(rows, ok) if o]
    e = enc1[ok]; tarde = (e > 18).astype(float); exc = np.clip(e - 17, 0, None)
    out = {'secoes': int(ok.sum()), 'locais_com_os_dois_grupos': 0, 'versoes': {}}
    por = collections.defaultdict(set)
    for r in sub: por[r['loc']].add(r['mod'] in ('UE2013', 'UE2015'))
    out['locais_com_os_dois_grupos'] = sum(1 for v in por.values() if len(v) == 2)
    base = [np.log(apt[ok]), y_comp[ok], fat1[ok]]
    for nome, cov, cn in (('sem_fila', base, ['log_aptos', 'var_comparecimento', 'fatia_lula_1t']),
                          ('com_fila', base + [exc, tarde], ['log_aptos', 'var_comparecimento', 'fatia_lula_1t', 'horas_apos_17h_1t', 'encerrou_depois_18h_1t'])):
        res = {}
        for yn, y, cv, cnn in (('virada', y_virada[ok], cov, cn), ('var_branco_nulo', y_bn[ok], cov, cn),
                               ('var_comparecimento', y_comp[ok], [c for c, n in zip(cov, cn) if n != 'var_comparecimento'], [n for n in cn if n != 'var_comparecimento']),
                               ('placebo_fatia_1t', fat1[ok], [np.log(apt[ok])], ['log_aptos']),
                               ('encerramento_1t_horas', e, [np.log(apt[ok])], ['log_aptos'])):
            r = regredir(sub, ['antiga'], ant[ok].reshape(-1, 1), y, np.column_stack(cv), cnn)
            res[yn] = {'coef_antiga': r['coef'].get('antiga'), 'ep': r['ep'].get('antiga'), 'n': r['n'], 'locais': r['grupos']}
        out['versoes'][nome] = res
    v0 = out['versoes']['sem_fila']; v1 = out['versoes']['com_fila']
    def sinal(v):
        b, se = v['virada']['coef_antiga'], v['virada']['ep']
        return (b is not None and b <= -1.0 and -b > 4 * se and abs(v['placebo_fatia_1t']['coef_antiga']) < 1.5
                and abs(v['var_comparecimento']['coef_antiga']) < 1.0)
    b0, s0 = v0['virada']['coef_antiga'], v0['virada']['ep']
    out['contribuicao_se_novas_alteradas'] = -b0 * 0.80
    out['veredito'] = ('SINAL' if sinal(v0) and sinal(v1) else
                       'SEM SINAL' if abs(b0) < 0.5 and s0 <= 0.2 and abs(v1['virada']['coef_antiga']) < 0.5 else 'INCONCLUSIVO')
    out['leitura_de_fila'] = bool(abs(v1['virada']['coef_antiga']) < 0.5 * abs(b0)
                                  and v0['encerramento_1t_horas']['coef_antiga'] > 0)
    return out


def main():
    d1 = carregar(sys.argv[1]); am = carregar(sys.argv[2]); logs = json.load(open(sys.argv[3]))['2']
    novos = 0
    if '--extensao' in sys.argv:
        am = dict(am)
        for pasta in sys.argv[sys.argv.index('--extensao') + 1].split(','):
            for k, v in ler_extensao(pasta).items():
                if k not in am:
                    am[k] = v; novos += 1
    rows = montar(d1, am, logs)
    n = len(rows)
    L1, R1, BN1, C1, L2, R2, BN2, C2, apt = [np.array([r[c] for r in rows], float) for c in
                                            ('L1', 'R1', 'BN1', 'C1', 'L2', 'R2', 'BN2', 'C2', 'apt')]
    fat1 = 100 * L1 / (L1 + R1); fat2 = 100 * L2 / (L2 + R2)
    y_virada = fat2 - fat1
    y_bn = 100 * (BN2 / C2 - BN1 / C1)
    y_comp = 100 * (C2 - C1) / apt
    cov_full = np.column_stack([np.log(apt), y_comp, fat1]); cn_full = ['log_aptos', 'var_comparecimento', 'fatia_lula_1t']
    cov_semcomp = np.column_stack([np.log(apt), fat1]); cn_semcomp = ['log_aptos', 'fatia_lula_1t']
    cov_plac = np.column_stack([np.log(apt)]); cn_plac = ['log_aptos']

    mods = sorted({r['mod'] for r in rows if r['mod'] and r['mod'] != REF})
    grupos = {}
    for m in mods:
        grupos[m] = np.array([1.0 if r['mod'] == m else 0.0 for r in rows])
    grupos['modelo_desconhecido'] = np.array([1.0 if r['mod'] is None else 0.0 for r in rows])
    grupos['urna_diferente_entre_turnos'] = np.array([1.0 if r['dif'] else 0.0 for r in rows])
    out = {'secoes': n, 'secoes_da_extensao': novos, 'locais': len({r['loc'] for r in rows}),
           'contagem_modelo': dict(collections.Counter(str(r['mod']) for r in rows)),
           'urna_diferente': int(sum(r['dif'] for r in rows)),
           'subamostra_log': int(sum(r['cont'] is not None for r in rows)),
           'contingencia_2t': int(sum(bool(r['cont']) for r in rows)), 'regressoes': {}}
    frac = {g: float(v.mean()) for g, v in grupos.items()}
    out['fracao_secoes'] = frac

    def bloco(nome, gnomes, idx=None):
        sel = np.arange(n) if idx is None else idx
        sub = [rows[i] for i in sel]
        ind = np.column_stack([grupos[g][sel] for g in gnomes])
        res = {}
        for yn, y, cov, cn in (('virada', y_virada, cov_full, cn_full), ('var_branco_nulo', y_bn, cov_full, cn_full),
                               ('var_comparecimento', y_comp, cov_semcomp, cn_semcomp),
                               ('placebo_fatia_1t', fat1, cov_plac, cn_plac)):
            r = regredir(sub, gnomes, ind, y[sel], cov[sel], cn)
            res[yn] = {'n': r['n'], 'locais': r['grupos'],
                       'coef': {g: r['coef'].get(g) for g in gnomes}, 'ep': {g: r['ep'].get(g) for g in gnomes}}
        out['regressoes'][nome] = res

    bloco('modelos', mods + ['modelo_desconhecido'])
    bloco('urna_diferente', ['urna_diferente_entre_turnos'])
    bloco('conjunto', mods + ['modelo_desconhecido', 'urna_diferente_entre_turnos'])
    idx = np.array([i for i, r in enumerate(rows) if r['cont'] is not None])
    if len(idx):
        grupos['contingencia_2t'] = np.array([1.0 if r['cont'] else 0.0 for r in rows])
        frac['contingencia_2t'] = float(grupos['contingencia_2t'][idx].mean())
        try:
            bloco('contingencia_subamostra_log', ['contingencia_2t'], idx)
        except Exception as e:
            out['regressoes']['contingencia_subamostra_log'] = f'sem estimativa: {e}'

    # critério do adendo 9
    leitura = {}
    soma_contrib = 0.0
    for nome in ('modelos', 'urna_diferente', 'contingencia_subamostra_log'):
        rg = out['regressoes'].get(nome)
        if not isinstance(rg, dict):
            continue
        v = rg['virada']; c = rg['var_comparecimento']; p = rg['placebo_fatia_1t']
        for g, b in v['coef'].items():
            if b is None:
                leitura[g] = 'sem variação dentro do local'; continue
            se = v['ep'][g]; f = frac[g]
            contrib = b * f
            soma_contrib += abs(contrib)
            sinal = (contrib > 0.3 and b > 4 * se and abs(p['coef'].get(g) or 0) < 0.1
                     and abs(c['coef'].get(g) or 0) < 2 * (c['ep'].get(g) or 0))
            leitura[g] = {'coef': b, 'ep': se, 'fracao': f, 'contribuicao_pontos': contrib,
                          'efeito_minimo_detectavel': 2.8 * se, 'sem_poder_na_amostra': 2.8 * se > 0.5,
                          'placebo_coef': p['coef'].get(g), 'efeito_comparecimento': c['coef'].get(g),
                          'sinal': bool(sinal), 'abaixo_de_0_5': abs(b) < 0.5}
    out['leitura'] = leitura
    out['contribuicao_somada_abs'] = soma_contrib
    ok = [x for x in leitura.values() if isinstance(x, dict)]
    out['veredito'] = ('SINAL' if any(x['sinal'] for x in ok) else
                       'SEM SINAL' if all(x['abaixo_de_0_5'] for x in ok) and soma_contrib < 0.15 else 'INCONCLUSIVO')
    out['adendo10_antigas_contra_novas'] = contraste(rows, y_virada, y_bn, y_comp, fat1, apt)
    # Adendo 11: contrastes de um modelo só, nos locais que têm os dois modelos do par
    frota = {'UE2020': 0.4016, 'UE2022': 0.3981, 'UE2015': 0.1764, 'UE2013': 0.0239}
    pares = {}
    for a, b in (('UE2020', 'UE2022'), ('UE2013', 'UE2015')):
        idx = np.array([i for i, r in enumerate(rows) if r['mod'] in (a, b)])
        sub = [rows[i] for i in idx]
        por = collections.defaultdict(set)
        for r in sub: por[r['loc']].add(r['mod'])
        ind = np.array([[1.0 if r['mod'] == a else 0.0] for r in sub])
        res = {'locais_com_os_dois': sum(1 for v in por.values() if len(v) == 2)}
        for yn, y, cov, cn in (('virada', y_virada, cov_full, cn_full), ('var_comparecimento', y_comp, cov_semcomp, cn_semcomp),
                               ('placebo_fatia_1t', fat1, cov_plac, cn_plac)):
            r = regredir(sub, [a], ind, y[idx], cov[idx], cn)
            res[yn] = {'coef': r['coef'].get(a), 'ep': r['ep'].get(a), 'n': r['n']}
        b_, se = res['virada']['coef'], res['virada']['ep']
        res['contribuicao_se_alterado_' + a] = b_ * frota[a]
        res['contribuicao_se_alterado_' + b] = -b_ * frota[b]
        res['efeito_minimo_detectavel'] = 2.8 * se
        pares[f'{a}_contra_{b}'] = res
    out['adendo11_um_modelo'] = pares
    print(json.dumps(out, ensure_ascii=False, indent=1))


if __name__ == '__main__':
    main()
