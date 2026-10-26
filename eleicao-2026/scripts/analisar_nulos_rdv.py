"""T19 do pré-registro (adendo 9): o que foi digitado nos votos nulos do RDV.

(a) nulos de presidente digitados 13 ou 22; nulos de governador digitados com o número de um finalista da UF.
(b) por seção, nulos digitados com o número de um eliminado contra os votos dele no 1º turno (efeito fixo de município).
(c) razão branco/(branco+nulo) por seção, 1º contra 2º turno (descritivo).
(d) seções com o mesmo número nulo raro repetido 5 vezes ou mais (lista para conferência).
Uso: python3 -I analisar_nulos_rdv.py <pasta_arq_2t> <secoes2026_1t.json.gz> <candidatos2026_1t.json.gz> <amostra_2t.json.gz> [--ano 2022 --base22 <secoes2022.json.gz>]
"""
import os as _os, sys as _sys
_sys.path.insert(0, _os.path.dirname(_os.path.abspath(__file__)))
import collections, json, os, sys
import numpy as np
from decodificar import ler_rdv, ler_bu, bu_para_secao
from lib import carregar, fe_ols

# números de partido (prefeito em 2024 usa o número do partido) e de presidenciáveis de 2022 e 2026
PARTIDOS = {10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 25, 27, 28, 29, 30, 33, 35, 36, 40, 43, 44, 45, 50, 51,
            55, 65, 70, 77, 80, 90}
ELIMINADOS_2026 = {'70': 'Cury', '14': 'Renan Santos', '55': 'Caiado', '30': 'Zema'}
ELIMINADOS_2022 = {'12': 'Ciro', '15': 'Tebet'}


def secoes(pasta):
    for uf in sorted(os.listdir(pasta)):
        for m in sorted(os.listdir(os.path.join(pasta, uf))):
            for z in sorted(os.listdir(os.path.join(pasta, uf, m))):
                for s in sorted(os.listdir(os.path.join(pasta, uf, m, z))):
                    yield f'{uf.upper()}|{int(m)}|{int(z)}|{int(s)}', os.path.join(pasta, uf, m, z, s)


def ler_pasta(pasta):
    out = {}
    for k, p in secoes(pasta):
        rd = sorted(f for f in os.listdir(p) if f.endswith('-rdv.dat'))
        if not rd:
            continue
        c = ler_rdv(os.path.join(p, rd[-1]))
        pres = collections.Counter(); gov = collections.Counter(); nul_p = collections.Counter(); nul_g = collections.Counter()
        for (ide, cod, tipo, dig), q in c.items():
            alvo = pres if cod == 1 else gov if cod == 3 else None
            if alvo is None:
                continue
            alvo[{2: 'V', 3: 'B', 4: 'N', 6: 'N'}.get(tipo, f't{tipo}')] += q
            if tipo == 2:
                alvo['n' + dig] += q
            if tipo == 4:
                (nul_p if cod == 1 else nul_g)[dig] += q
        out[k] = {'pres': pres, 'gov': gov, 'nul_p': nul_p, 'nul_g': nul_g}
    return out


def inclinacao(ks, y, x, grupos):
    if len(ks) < 10:
        return None
    r = fe_ols(np.array(y, float), np.array(x, float).reshape(-1, 1), grupos, nomes=['x'])
    return {'n': r['n'], 'coef': r['coef']['x'], 'ep': r['ep']['x'], 'razao_bruta': float(sum(y) / max(sum(x), 1))}


def main():
    pasta, base1, cand1, amostra = sys.argv[1:5]
    ano = sys.argv[sys.argv.index('--ano') + 1] if '--ano' in sys.argv else '2026'
    r = ler_pasta(pasta)
    res = {'ano': ano, 'secoes_com_rdv': len(r)}
    elim = ELIMINADOS_2026 if ano == '2026' else ELIMINADOS_2022
    finalistas_p = {'13', '22'}

    # (a)
    fin_g = collections.defaultdict(set)
    for k, v in r.items():
        for x in v['gov']:
            if x.startswith('n'):
                fin_g[k.split('|')[0]].add(x[1:])
    a_p = {k: {d: v['nul_p'][d] for d in finalistas_p if v['nul_p'][d]} for k, v in r.items()}
    a_p = {k: x for k, x in a_p.items() if x}
    a_g = {k: {d: v['nul_g'][d] for d in fin_g[k.split('|')[0]] if v['nul_g'][d]} for k, v in r.items()}
    a_g = {k: x for k, x in a_g.items() if x}
    res['a'] = {'nulos_pres_total': sum(sum(v['nul_p'].values()) for v in r.values()),
                'nulos_pres_com_13_ou_22': sum(sum(x.values()) for x in a_p.values()), 'secoes_pres': a_p,
                'finalistas_gov_por_uf': {u: sorted(s) for u, s in fin_g.items()},
                'nulos_gov_total': sum(sum(v['nul_g'].values()) for v in r.values()),
                'nulos_gov_com_finalista': sum(sum(x.values()) for x in a_g.values()), 'secoes_gov': a_g}

    # (b)
    if ano == '2026':
        c1 = carregar(cand1)['secoes']
        votos1 = lambda k, n: c1.get(k, {}).get(n, 0)
    else:
        c1 = None
        b22 = carregar(sys.argv[sys.argv.index('--base22') + 1])
        votos1 = lambda k, n: b22.get(k, {}).get('1', {}).get('cand', {}).get(n, 0)
    b = {}
    ks = [k for k in r if sum(r[k]['pres'].values()) >= 50]
    mun = ['|'.join(k.split('|')[:2]) for k in ks]
    tot_y = tot_x = 0
    for n, nome in elim.items():
        y = [r[k]['nul_p'][n] for k in ks]; x = [votos1(k, n) for k in ks]
        tot_y += sum(y); tot_x += sum(x)
        b[nome] = inclinacao(ks, y, x, mun)
    # empilhado: uma linha por seção e eliminado, efeito fixo de município x candidato
    ky, yy, xx, gg = [], [], [], []
    for n in elim:
        for k, m in zip(ks, mun):
            ky.append(k); yy.append(r[k]['nul_p'][n]); xx.append(votos1(k, n)); gg.append(m + '|' + n)
    b['empilhado'] = inclinacao(ky, yy, xx, gg)
    b['total_nulos_com_numero_de_eliminado'] = tot_y; b['total_votos_1t_dos_eliminados'] = tot_x
    # outros números nulos mais digitados
    geral = collections.Counter()
    for v in r.values():
        geral.update(v['nul_p'])
    b['nulos_pres_mais_digitados'] = geral.most_common(25)
    res['b'] = b

    # (c) razão branco/(branco+nulo), mesmas seções
    if ano == '2026':
        d1 = carregar(base1); am = carregar(amostra)
        rz1, rz2 = [], []
        for k in am:
            s1 = d1.get(k, {}).get('1'); s2 = am[k].get('2')
            if not s1 or not s2 or s1['B'] + s1['N'] < 5 or s2['B'] + s2['N'] < 5:
                continue
            rz1.append(s1['B'] / (s1['B'] + s1['N'] + s1.get('c28', 0))); rz2.append(s2['B'] / (s2['B'] + s2['N']))
        sb1 = sum(d1[k]['1']['B'] for k in am if k in d1 and '1' in d1[k] and '2' in am[k])
        sn1 = sum(d1[k]['1']['N'] + d1[k]['1'].get('c28', 0) for k in am if k in d1 and '1' in d1[k] and '2' in am[k])
        sb2 = sum(am[k]['2']['B'] for k in am if '2' in am[k]); sn2 = sum(am[k]['2']['N'] for k in am if '2' in am[k])
        res['c'] = {'secoes': len(rz1), 'media_razao_1t': float(np.mean(rz1)), 'media_razao_2t': float(np.mean(rz2)),
                    'agregado_1t': sb1 / (sb1 + sn1), 'agregado_2t': sb2 / (sb2 + sn2),
                    'brancos_1t': sb1, 'nulos_1t': sn1, 'brancos_2t': sb2, 'nulos_2t': sn2}

    # (d)
    d = []
    for k, v in r.items():
        for dig, q in v['nul_p'].items():
            if q >= 5 and dig not in ('00', '99') and not (dig.isdigit() and int(dig) in PARTIDOS):
                d.append((k, dig, q))
    res['d'] = sorted(d, key=lambda t: -t[2])
    print(json.dumps(res, ensure_ascii=False, indent=1, default=str))


if __name__ == '__main__':
    main()
