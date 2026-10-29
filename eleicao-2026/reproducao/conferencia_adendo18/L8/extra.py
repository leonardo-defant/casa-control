"""Conferência L8, leituras extras (minhas, declaradas como tal): onde ficam as seções que fecharam tarde, excesso de
comparecimento nelas contra as do mesmo local, ordem da parcial de 1.225 seções e cruzamento tarde 1T x tarde 2T.
Uso: python3 -I extra.py <dir_ext1> <dir_ext2> <saida.json>"""
import collections, datetime as dt, glob, gzip, json, os, sys
import numpy as np
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from conferir import fe_cluster, ler, P, DIA

AM5 = {('AM', m) for m in ('2020', '2054', '2135', '2291', '2313', '2399', '2496', '2755', '2917', '98370', '98477')}
ESP = {'AC': 2, 'AM': 1, 'RO': 1, 'RR': 1, 'MT': 1, 'MS': 1}


def desloc(k):
    m = tuple(k.split('|')[:2])
    if m in AM5:
        return 2
    if m == ('PE', '30015'):
        return -1
    return ESP.get(m[0], 0)


def main():
    d1, d2, saida = sys.argv[1:4]
    T = {1: ler(d1), 2: ler(d2)}
    R = {}
    EB = {t: {k: P(s['enc']) + dt.timedelta(hours=desloc(k)) for k, s in T[t].items() if not k.startswith('ZZ') and P(s['enc'])}
          for t in (1, 2)}
    lim2 = {n: DIA[2].replace(hour=h, minute=m, second=s) for n, (h, m, s) in
            {'17h03': (17, 3, 0), '17h15m59': (17, 15, 59), '18h59m59': (18, 59, 59)}.items()}
    # abertas às 17h03 (hora da liminar) e quantas ficaram até 19h
    R['abertas_17h03_2t'] = sum(1 for v in EB[2].values() if v > lim2['17h03'])
    R['fecharam_depois_18h59m59_2t'] = sum(1 for v in EB[2].values() if v > lim2['18h59m59'])
    lim1 = DIA[1].replace(hour=17, minute=3)
    R['abertas_17h03_1t'] = sum(1 for v in EB[1].values() if v > lim1)
    # UFs e municípios das que fecharam depois das 18h59m59
    tarde = [k for k, v in EB[2].items() if v > lim2['18h59m59']]
    R['tarde19_por_uf'] = dict(collections.Counter(k.split('|')[0] for k in tarde).most_common())
    mun = collections.Counter((k.split('|')[0], T[2][k]['mun']) for k in tarde)
    R['tarde19_top_municipios'] = [(f'{u}|{m}', n) for (u, m), n in mun.most_common(25)]
    R['tarde19_n_municipios'] = len(mun)
    # quanto do eleitorado e quanto de Lula 1T/2T nessas seções
    L1 = sum(T[1][k]['L'] for k in tarde if k in T[1]); R1 = sum(T[1][k]['R'] for k in tarde if k in T[1])
    L2 = sum(T[2][k]['L'] for k in tarde); R2 = sum(T[2][k]['R'] for k in tarde)
    R['tarde19_lula_1t_2t'] = {'1t': 100 * L1 / (L1 + R1), '2t': 100 * L2 / (L2 + R2)}
    # cruzamento tarde 17h15 1T x 2T
    l1 = DIA[1].replace(hour=17, minute=15, second=59)
    c = collections.Counter()
    for k, v in EB[2].items():
        if k in EB[1]:
            c[(EB[1][k] > l1, v > lim2['17h15m59'])] += 1
    R['tarde_1t_x_2t'] = {f'1t_{a}|2t_{b}': n for (a, b), n in c.items()}
    # excesso de comparecimento (2T - 1T, em pontos do eleitorado) nas que fecharam tarde, contra o mesmo local
    y, x, x19, g, w, apt = [], [], [], [], [], []
    for k, s2 in T[2].items():
        if k.startswith('ZZ') or k not in T[1] or k not in EB[2]:
            continue
        s1 = T[1][k]
        if s1['apt'] == 0 or s2['apt'] == 0:
            continue
        y.append(100 * (s2['comp'] / s2['apt'] - s1['comp'] / s1['apt']))
        x.append(float(EB[2][k] > lim2['17h15m59'])); x19.append(float(EB[2][k] > lim2['18h59m59']))
        uf, mu, z, _ = k.split('|'); g.append(f'{uf}|{mu}|{z}|{s2["loc"]}'); w.append(s2['apt']); apt.append(s2['apt'])
    g = np.array(g)
    r = fe_cluster(y, np.array(x)[:, None], g, w)
    r19 = fe_cluster(y, np.array(x19)[:, None], g, w)
    apt = np.array(apt); x = np.array(x); x19 = np.array(x19)
    R['excesso_comparecimento_tarde17h15'] = {**r, 'aptos_nessas': int(apt[x == 1].sum()),
                                             'eleitores_extra_estimados': r['b'][0] / 100 * apt[x == 1].sum(),
                                             'ic95': [(r['b'][0] - 1.96 * r['ep'][0]) / 100 * apt[x == 1].sum(),
                                                      (r['b'][0] + 1.96 * r['ep'][0]) / 100 * apt[x == 1].sum()]}
    R['excesso_comparecimento_tarde19h'] = {**r19, 'aptos_nessas': int(apt[x19 == 1].sum()),
                                           'eleitores_extra_estimados': r19['b'][0] / 100 * apt[x19 == 1].sum(),
                                           'ic95': [(r19['b'][0] - 1.96 * r19['ep'][0]) / 100 * apt[x19 == 1].sum(),
                                                    (r19['b'][0] + 1.96 * r19['ep'][0]) / 100 * apt[x19 == 1].sum()]}
    # parcial da pausa: TSE 1.225 seções, Lula 193.574, Flávio 142.169 (Forte no Recôncavo, print do boletim do TSE)
    rr = sorted((P(s['rec']), k) for k, s in T[2].items())
    pref = []
    Lc = Rc = 0
    for i, (r_, k) in enumerate(rr[:1868], 1):
        Lc += T[2][k]['L']; Rc += T[2][k]['R']
        if i in (1100, 1150, 1200, 1225, 1250, 1300, 1868) or (Lc == 193574 and Rc == 142169):
            pref.append((i, str(r_), Lc, Rc, round(100 * Lc / (Lc + Rc), 3)))
    R['prefixos_recebimento'] = pref
    # mesma coisa ordenando os 1.868 primeiros pela emissão do boletim em hora de Brasília (exterior: sem conversão)
    em = sorted(((P(T[2][k]['emi']) + dt.timedelta(hours=0 if k.startswith('ZZ') else desloc(k))), k) for _, k in rr[:1868])
    Lc = sum(T[2][k]['L'] for _, k in em[:1225]); Rc = sum(T[2][k]['R'] for _, k in em[:1225])
    R['primeiros_1225_por_emissao_entre_os_1868'] = (Lc, Rc, round(100 * Lc / (Lc + Rc), 3))
    # o TSE divulga "seções totalizadas": quantas das 1.868 têm L+R e aptos > 0
    R['parcial_tse'] = {'secoes': 1225, 'L': 193574, 'R': 142169, 'L_pct': round(100 * 193574 / (193574 + 142169), 3),
                        'fonte': 'https://www.fortenoreconcavo.com.br/2026/10/tse-suspende-totalizacao-dos-votos-do-2.html'}
    with open(saida, 'w') as f:
        json.dump(R, f, ensure_ascii=False, indent=1, default=str)
    print(json.dumps(R, ensure_ascii=False, default=str))


if __name__ == '__main__':
    main()
