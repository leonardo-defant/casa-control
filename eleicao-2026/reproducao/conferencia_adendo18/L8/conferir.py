"""Conferência independente do L8 (Adendo 18). Código próprio, lendo a extração própria dos zips (extrair.py).
Fuso por outro caminho que o do agente: deslocamento do município = piso do percentil 10 de (recebimento no TSE - emissão
do boletim) no 1º turno, em horas (o 1º turno não teve pausa na recepção). Confronto com o fuso esperado por UF e com o
método do agente (hora modal de abertura).
Uso: python3 -I conferir.py <dir_ext1> <dir_ext2> <secoes2026.json.gz> <saida.json>"""
import collections, datetime as dt, glob, gzip, json, math, os, sys
import numpy as np

P = lambda s: dt.datetime.strptime(s, '%Y-%m-%d %H:%M:%S') if s and s[:4] == '2026' else None
OFICIAL = {'L': 64256232, 'R': 59826041}
DIA = {1: dt.datetime(2026, 10, 4), 2: dt.datetime(2026, 10, 25)}


def ler(d):
    out = {}
    for f in sorted(glob.glob(os.path.join(d, '*.json.gz'))):
        with gzip.open(f, 'rt') as h:
            out.update(json.load(h))
    return out


def fe_cluster(y, X, g, w):
    """MQO ponderado com efeito fixo (within) e erro agrupado CR1. Implementação própria."""
    y = np.asarray(y, float); X = np.asarray(X, float).reshape(len(y), -1); w = np.asarray(w, float)
    _, gi = np.unique(g, return_inverse=True)
    cnt = np.bincount(gi)
    keep = cnt[gi] > 1
    y, X, w, gi = y[keep], X[keep], w[keep], gi[keep]
    _, gi = np.unique(gi, return_inverse=True)
    G = gi.max() + 1
    sw = np.bincount(gi, w, G)
    def dm(v):
        return v - (np.bincount(gi, w * v, G) / sw)[gi]
    yd = dm(y); Xd = np.column_stack([dm(X[:, j]) for j in range(X.shape[1])])
    A = (Xd * w[:, None]).T @ Xd
    b = np.linalg.solve(A, (Xd * w[:, None]).T @ yd)
    e = yd - Xd @ b
    sc = np.column_stack([np.bincount(gi, w * Xd[:, j] * e, G) for j in range(Xd.shape[1])])
    Ai = np.linalg.inv(A)
    N, k = len(y), X.shape[1]
    V = Ai @ (sc.T @ sc) @ Ai * (G / (G - 1)) * ((N - 1) / (N - k))
    return {'b': b.tolist(), 'ep': np.sqrt(np.diag(V)).tolist(), 'n': int(N), 'G': int(G)}


def main():
    d1, d2, base_path, saida = sys.argv[1:5]
    T = {1: ler(d1), 2: ler(d2)}
    R = {}
    R['n_secoes'] = {t: len(T[t]) for t in T}
    R['conflitos_linhas'] = {t: sum(1 for s in T[t].values() if s['conflito']) for t in T}
    R['agregadas_2t'] = sum(1 for s in T[2].values() if s['agreg'] not in ('#NULO#', '', '-1'))
    R['agregadas_2t_n_secoes_extra'] = sum(len([x for x in s['agreg'].split(',') if x.strip()]) for s in T[2].values()
                                           if s['agreg'] not in ('#NULO#', '', '-1'))
    R['tipos_urna_2t'] = dict(collections.Counter(s['tipo'] for s in T[2].values()))

    # ---------------- D3: soma
    L2 = sum(s['L'] for s in T[2].values()); R2 = sum(s['R'] for s in T[2].values())
    R['D3'] = {'L': L2, 'R': R2, 'dif_L_oficial': L2 - OFICIAL['L'], 'dif_R_oficial': R2 - OFICIAL['R'],
               'margem': L2 - R2, 'L_pct': 100 * L2 / (L2 + R2),
               'secoes_L_frente': sum(s['L'] > s['R'] for s in T[2].values()),
               'secoes_R_frente': sum(s['R'] > s['L'] for s in T[2].values()),
               'empates': sum(s['R'] == s['L'] for s in T[2].values())}
    # confronto com a base do projeto
    base = json.load(gzip.open(base_path, 'rt'))
    difs = 0; faltam = []
    for k, s in T[2].items():
        b = base.get(k, {}).get('2')
        if b is None:
            faltam.append(k); continue
        if (b['L'], b['R'], b['comp']) != (s['L'], s['R'], s['comp']):
            difs += 1
    R['confronto_base_2t'] = {'faltam_na_base': faltam[:20], 'n_faltam': len(faltam), 'diferencas_L_R_comp': difs}

    # ---------------- fuso: hora modal de ENCERRAMENTO do município (17 em Brasília), por turno; o agente usou a abertura
    # (o recebimento menos a emissão não serve: no 1º turno a mediana da demora em SP foi de 100 minutos)
    mh_enc = {1: collections.defaultdict(collections.Counter), 2: collections.defaultdict(collections.Counter)}
    for t in (1, 2):
        for k, s in T[t].items():
            e = P(s['enc'])
            if e and s['junta'] in ('-1', ''):
                mh_enc[t][tuple(k.split('|')[:2])][e.hour] += 1
    offt = {t: {m: 17 - c.most_common(1)[0][0] for m, c in mh_enc[t].items()} for t in (1, 2)}
    esperado = {'AC': 2, 'AM': 1, 'RO': 1, 'RR': 1, 'MT': 1, 'MS': 1}
    disc = collections.Counter(); lista_disc = []
    for t in (1, 2):
        for (uf, mun), o in offt[t].items():
            if uf == 'ZZ':
                continue
            e = esperado.get(uf, 0)
            if o != e:
                disc[(t, uf, o)] += 1
                lista_disc.append((t, uf, mun, T[t][next(k for k in T[t] if k.startswith(uf + '|' + mun + '|'))]['mun'], o))
    R['fuso_discordancias_com_UF'] = {f'{t}|{u}|{o}': n for (t, u, o), n in disc.items()}
    R['fuso_discordancias_lista'] = sorted(lista_disc)
    R['fuso_1t_x_2t_diferentes'] = sorted([m for m in offt[2] if m in offt[1] and offt[1][m] != offt[2][m]])
    mh = collections.defaultdict(collections.Counter)
    for k, s in T[2].items():
        a = P(s['ab'])
        if a and s['junta'] in ('-1', ''):
            mh[tuple(k.split('|')[:2])][a.hour] += 1
    off_ag = {m: 8 - c.most_common(1)[0][0] for m, c in mh.items()}
    conf = collections.Counter()
    for m, o in offt[2].items():
        if m[0] == 'ZZ' or m not in off_ag:
            continue
        conf['igual' if o == off_ag[m] else f'dif|{m[0]}|meu{o}|agente{off_ag[m]}'] += 1
    R['fuso_meu_x_agente_2t'] = dict(conf)

    # Fuso usado (meu): tabela por UF; exceções achadas nos dados e iguais nos dois turnos e nos dois campos (abertura e
    # encerramento): os municípios do AM com hora modal de encerramento 15h nos dois turnos ficam em -5 (deslocamento 2);
    # Fernando de Noronha em -2 (deslocamento -1). O encerramento modal não serve como fuso no 1º turno (fila passou das 18h
    # em municípios do Nordeste) nem nos municípios onde a prorrogação segurou a maioria das seções até as 19h.
    am5 = sorted(m for m in offt[1] if m[0] == 'AM' and offt[1].get(m) == 2 and offt[2].get(m) == 2)
    R['fuso_AM_menos5'] = am5
    def desloc(m):
        if m in am5:
            return 2
        if m == ('PE', '30015'):
            return -1
        return esperado.get(m[0], 0)
    # confronto da tabela com o método do agente (abertura modal) nos dois turnos
    for t in (1, 2):
        mh_ab = collections.defaultdict(collections.Counter)
        for k, s in T[t].items():
            a = P(s['ab'])
            if a and s['junta'] in ('-1', ''):
                mh_ab[tuple(k.split('|')[:2])][a.hour] += 1
        ag = {m: 8 - c.most_common(1)[0][0] for m, c in mh_ab.items()}
        cc = collections.Counter()
        lst = []
        for m, o in ag.items():
            if m[0] == 'ZZ':
                continue
            if o == desloc(m):
                cc['igual'] += 1
            else:
                cc['dif'] += 1; lst.append((m, o, desloc(m)))
        R[f'tabela_x_agente_{t}t'] = {'cont': dict(cc), 'lista': lst}

    def enc_br(t, k, s):
        e = P(s['enc'])
        if e is None:
            return None
        return e + dt.timedelta(hours=desloc(tuple(k.split('|')[:2])))

    EB = {t: {k: enc_br(t, k, s) for k, s in T[t].items() if not k.startswith('ZZ')} for t in (1, 2)}

    # ---------------- D1: cortes
    def cortes(t):
        br = {k: T[t][k] for k in EB[t]}
        Lt = sum(s['L'] for s in br.values()); Rt = sum(s['R'] for s in br.values()); Ct = sum(s['comp'] for s in br.values())
        out = {'L': Lt, 'R': Rt, 'comp': Ct, 'margem': Lt - Rt, 'sem_enc': sum(1 for v in EB[t].values() if v is None)}
        for hh, mm, ss in ((17, 0, 59), (17, 5, 59), (17, 15, 59), (17, 59, 59), (18, 59, 59)):
            lim = DIA[t].replace(hour=hh, minute=mm, second=ss)
            ks = [k for k, v in EB[t].items() if v is not None and v > lim]
            Lx = sum(br[k]['L'] for k in ks); Rx = sum(br[k]['R'] for k in ks); Cx = sum(br[k]['comp'] for k in ks)
            out[f'{hh}:{mm:02d}:{ss}'] = {'secoes': len(ks), 'comp': Cx, 'L_pct': 100 * Lx / (Lx + Rx) if Lx + Rx else None,
                                         'margem_sem': (Lt - Lx) - (Rt - Rx), 'pior_caso': (Lt - Rt) - Cx}
        return out
    R['D1'] = {'2t': cortes(2), '1t': cortes(1)}
    # faixas de 15 minutos
    def faixas(t):
        c = collections.Counter()
        for v in EB[t].values():
            if v is None:
                continue
            mins = (v - DIA[t]).total_seconds() / 60
            if mins < 17 * 60:
                c['<17h00'] += 1
            elif mins >= 19 * 60 + 15:
                c['>=19h15'] += 1
            else:
                b0 = int((mins - 17 * 60) // 15) * 15 + 17 * 60
                c[f'{b0 // 60:02d}h{b0 % 60:02d}'] += 1
        return dict(sorted(c.items()))
    R['D1_faixas'] = {'1t': faixas(1), '2t': faixas(2)}

    # E3: virada na seção, encerrou depois de 17:15:59 de Brasília, efeito fixo de local
    lim1 = DIA[1].replace(hour=17, minute=15, second=59); lim2 = DIA[2].replace(hour=17, minute=15, second=59)
    y, x2, x1, g, w = [], [], [], [], []
    for k, s2 in T[2].items():
        if k.startswith('ZZ'):
            continue
        s1 = T[1].get(k)
        if s1 is None or EB[2].get(k) is None or EB[1].get(k) is None:
            continue
        if s1['L'] + s1['R'] == 0 or s2['L'] + s2['R'] == 0:
            continue
        y.append(100 * (s2['L'] / (s2['L'] + s2['R']) - s1['L'] / (s1['L'] + s1['R'])))
        x2.append(float(EB[2][k] > lim2)); x1.append(float(EB[1][k] > lim1))
        uf, mun, z, _ = k.split('|'); g.append(f'{uf}|{mun}|{z}|{s2["loc"]}'); w.append(s2['L'] + s2['R'])
    R['E3_a'] = fe_cluster(y, np.array(x2)[:, None], np.array(g), w)
    R['E3_b'] = fe_cluster(y, np.column_stack([x2, x1]), np.array(g), w)
    # leitura extra (minha): sem peso, e com o corte 18:59:59
    R['E3_sem_peso'] = fe_cluster(y, np.array(x2)[:, None], np.array(g), np.ones(len(y)))
    lim19 = DIA[2].replace(hour=18, minute=59, second=59)
    x19 = []
    for k, s2 in T[2].items():
        if k.startswith('ZZ'):
            continue
        s1 = T[1].get(k)
        if s1 is None or EB[2].get(k) is None or EB[1].get(k) is None or s1['L'] + s1['R'] == 0 or s2['L'] + s2['R'] == 0:
            continue
        x19.append(float(EB[2][k] > lim19))
    R['E3_corte_19h'] = fe_cluster(y, np.array(x19)[:, None], np.array(g), w)
    R['E3_n'] = {'n': len(y), 'tarde2': int(sum(x2)), 'tarde1': int(sum(x1)), 'tarde19': int(sum(x19))}

    # V3
    comuns = [k for k in T[2] if k in T[1]]
    R['V3'] = {'ganho_L_total': sum(T[2][k]['L'] - T[1][k]['L'] for k in comuns),
               'ganho_R_total': sum(T[2][k]['R'] - T[1][k]['R'] for k in comuns),
               'ganho_L_tarde_17h15': sum(T[2][k]['L'] - T[1][k]['L'] for k in comuns if EB[2].get(k) and EB[2][k] > lim2),
               'ganho_R_tarde_17h15': sum(T[2][k]['R'] - T[1][k]['R'] for k in comuns if EB[2].get(k) and EB[2][k] > lim2)}

    # ---------------- V2: recebimento
    rr = sorted((P(s['rec']), k) for k, s in T[2].items() if P(s['rec']))
    R['V2'] = {'sem_rec': len(T[2]) - len(rr), 'primeiro': str(rr[0][0]), 'ultimo': str(rr[-1][0])}
    d = DIA[2]
    a, b = d.replace(hour=17, minute=8), d.replace(hour=19, minute=3, second=36)
    R['V2']['entre_17h08_e_19h03m36'] = sum(1 for r, _ in rr if a <= r <= b)
    antes = [(r, k) for r, k in rr if r < a]
    R['V2']['antes_17h08'] = len(antes)
    R['V2']['ultimo_antes'] = str(antes[-1][0]) if antes else None
    R['V2']['primeiro_depois'] = str(next(r for r, _ in rr if r > b))
    for n in (1225, len(antes)):
        ks = [k for _, k in rr[:n]]
        Lx = sum(T[2][k]['L'] for k in ks); Rx = sum(T[2][k]['R'] for k in ks)
        R['V2'][f'primeiros_{n}'] = {'hora_ultimo': str(rr[n - 1][0]), 'L_pct': 100 * Lx / (Lx + Rx), 'L': Lx, 'R': Rx,
                                     'ufs': dict(collections.Counter(k.split('|')[0] for k in ks).most_common())}
    # quantos recebidos até cada segundo das 17h06
    R['V2']['acumulado_por_minuto'] = {m: sum(1 for r, _ in rr if r < d.replace(hour=17, minute=m)) for m in range(5, 9)}
    # 1º turno
    rr1 = sorted((P(s['rec']), k) for k, s in T[1].items() if P(s['rec']))
    R['V2']['1t_primeiro'] = str(rr1[0][0])
    gaps = []
    for i in range(1, len(rr1)):
        gap = (rr1[i][0] - rr1[i - 1][0]).total_seconds()
        if gap > 120 and rr1[i][0] < DIA[1].replace(hour=23):
            gaps.append((str(rr1[i - 1][0]), str(rr1[i][0]), gap))
    R['V2']['1t_lacunas_maiores_2min_ate_23h'] = gaps[:20]
    gaps2 = []
    for i in range(1, len(rr)):
        gap = (rr[i][0] - rr[i - 1][0]).total_seconds()
        if gap > 120 and rr[i][0] < DIA[2].replace(hour=23):
            gaps2.append((str(rr[i - 1][0]), str(rr[i][0]), gap))
    R['V2']['2t_lacunas_maiores_2min_ate_23h'] = gaps2[:20]

    # ---------------- D2: definição matemática
    apt_rest = sum(T[2][k]['apt'] for _, k in rr); marg = 0; hit = None
    for i, (r, k) in enumerate(rr, 1):
        s = T[2][k]; marg += s['L'] - s['R']; apt_rest -= s['apt']
        if hit is None and marg > apt_rest:
            hit = {'hora': str(r), 'i': i, 'pct': 100 * i / len(rr), 'margem': marg, 'aptos_rest': apt_rest}
    R['D2'] = hit
    # quem lidera por instantes
    inst = {}
    for hh, mm in ((19, 30), (20, 0), (20, 30), (21, 0)):
        lim = d.replace(hour=hh, minute=mm, second=59)
        ks = [k for r, k in rr if r <= lim]
        Lx = sum(T[2][k]['L'] for k in ks); Rx = sum(T[2][k]['R'] for k in ks)
        inst[f'{hh}h{mm:02d}'] = {'n': len(ks), 'L_pct': 100 * Lx / (Lx + Rx)}
    R['D2_instantes'] = inst

    # ordem de chegada: virada por posição, efeito fixo de local
    pos = {k: i / (len(rr) - 1) for i, (_, k) in enumerate(rr)}
    yv, xv, gv, wv = [], [], [], []
    for k, s2 in T[2].items():
        s1 = T[1].get(k)
        if k.startswith('ZZ') or s1 is None or k not in pos or s1['L'] + s1['R'] == 0 or s2['L'] + s2['R'] == 0:
            continue
        yv.append(100 * (s2['L'] / (s2['L'] + s2['R']) - s1['L'] / (s1['L'] + s1['R']))); xv.append(pos[k])
        uf, mun, z, _ = k.split('|'); gv.append(f'{uf}|{mun}|{z}|{s2["loc"]}'); wv.append(s2['L'] + s2['R'])
    R['V2_ordem'] = fe_cluster(yv, np.array(xv)[:, None], np.array(gv), wv)
    yv, xv, wv = map(np.asarray, (yv, xv, wv))
    dec = np.minimum((xv * 10).astype(int), 9)
    R['V2_ordem_decimos'] = [float((yv * wv)[dec == i].sum() / wv[dec == i].sum()) for i in range(10)]

    # D3 recorte até 17:00:59
    lim = DIA[2].replace(hour=17, minute=0, second=59)
    ks = [k for k, v in EB[2].items() if v is not None and v <= lim]
    La = sum(T[2][k]['L'] for k in ks); Ra = sum(T[2][k]['R'] for k in ks)
    R['D3_ate_17h00m59'] = {'n': len(ks), 'L_pct': 100 * La / (La + Ra), 'margem': La - Ra}
    lim1b = DIA[1].replace(hour=17, minute=0, second=59)
    ks1 = [k for k, v in EB[1].items() if v is not None and v <= lim1b]
    La = sum(T[1][k]['L'] for k in ks1); Ra = sum(T[1][k]['R'] for k in ks1)
    ks1b = [k for k, v in EB[1].items() if v is not None and v > lim1b]
    Lb = sum(T[1][k]['L'] for k in ks1b); Rb = sum(T[1][k]['R'] for k in ks1b)
    R['D3_1t_ate_17h00m59'] = {'n': len(ks1), 'L_pct': 100 * La / (La + Ra), 'demais_L_pct': 100 * Lb / (Lb + Rb)}

    with open(saida, 'w') as f:
        json.dump(R, f, ensure_ascii=False, indent=1, default=str)
    print(json.dumps(R, ensure_ascii=False, indent=1, default=str))


if __name__ == '__main__':
    main()
