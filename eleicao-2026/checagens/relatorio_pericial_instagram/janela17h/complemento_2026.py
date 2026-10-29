"""Complemento do analisar_janela.py para 2026 (uma leitura da base).

Uso: python3 -I complemento_2026.py <secoes2026.json.gz> <saida.json>
(1) Janelas finas em hora de Brasília (deslocamento pela hora modal de abertura do município), 2º e 1º turno:
    ate 17:00:59 | 17:01:00 a 17:02:59 (antes da liminar das 17h03) | 17:03:00 a 17:15:59 | 17:16:00 a 18:59:59 | 19h ou mais.
(2) Seções que encerraram às 19h ou depois (relógio local) nas capitais com mais delas: fatia de Lula (dois candidatos)
    no 1º e no 2º turno, contra o resto do mesmo município.
(3) Contrafactuais da margem nacional: sem as seções J2+J3 (17h16 ou depois, relógio local); e com J2+J3 levadas à
    fatia de Lula (dois candidatos) que essas mesmas seções deram no 1º turno, aplicada aos válidos do 2º turno.
"""
import collections as C, gzip, json, sys


def seg(h):
    if not h or len(h) != 8 or not h[:2].isdigit():
        return None
    a, b, c = h.split(':')
    return int(a) * 3600 + int(b) * 60 + int(c)


def main():
    base_path, saida = sys.argv[1:3]
    with gzip.open(base_path, 'rt') as f:
        b = json.load(f)
    R = {}
    for t in ('2', '1'):
        cnt = C.defaultdict(C.Counter)
        for k, d in b.items():
            s = d.get(t)
            if s and s.get('ab') and s['ab'][:2].isdigit():
                cnt[tuple(k.split('|')[:2])][int(s['ab'][:2])] += 1
        off = {m: 8 - c.most_common(1)[0][0] for m, c in cnt.items()}
        lim = [(17 * 3600 + 59, 'a_ate_17h00m59'), (17 * 3600 + 179, 'b_17h01_17h02_antes_da_liminar'),
               (17 * 3600 + 959, 'c_17h03_17h15'), (18 * 3600 + 3599, 'd_17h16_18h59'), (10 ** 9, 'e_19h_ou_mais')]
        acc = C.defaultdict(lambda: [0, 0, 0, 0, 0])
        for k, d in b.items():
            s = d.get(t)
            if not s:
                continue
            e = seg(s.get('enc'))
            if e is None:
                nome = 'sem_horario'
            else:
                e += 3600 * off.get(tuple(k.split('|')[:2]), 0)
                nome = next(n for l, n in lim if e <= l)
            x = acc[nome]
            x[0] += 1; x[1] += s['comp']; x[2] += s['L']; x[3] += s['R']; x[4] += s['L'] + s['R'] + s.get('O', 0)
        R[f'brasilia_fino_{t}t'] = {n: {'secoes': x[0], 'comp': x[1], 'L': x[2], 'R': x[3], 'validos': x[4],
                                        'pct_L_validos': round(100 * x[2] / x[4], 3), 'pct_L_dois': round(100 * x[2] / (x[2] + x[3]), 3),
                                        'margem_L_menos_R': x[2] - x[3]} for n, x in sorted(acc.items())}
    # (2) capitais
    alvo = {'SP|71072': 'SAO PAULO', 'RJ|60011': 'RIO DE JANEIRO', 'BA|38490': 'SALVADOR', 'PE|25313': 'RECIFE', 'PB|20516': 'JOAO PESSOA'}
    cap = C.defaultdict(lambda: {'J3': [0, 0, 0, 0, 0], 'resto': [0, 0, 0, 0, 0]})
    for k, d in b.items():
        m = '|'.join(k.split('|')[:2])
        if m not in alvo or '1' not in d or '2' not in d:
            continue
        e = seg(d['2'].get('enc'))
        lado = 'J3' if e is not None and e >= 19 * 3600 else 'resto'
        x = cap[m][lado]
        x[0] += 1; x[1] += d['1']['L']; x[2] += d['1']['R']; x[3] += d['2']['L']; x[4] += d['2']['R']
    R['capitais_J3_x_resto'] = {}
    for m, v in cap.items():
        R['capitais_J3_x_resto'][alvo[m]] = {
            lado: {'secoes': x[0], 'L2_1t': round(100 * x[1] / (x[1] + x[2]), 3), 'L2_2t': round(100 * x[3] / (x[3] + x[4]), 3),
                   'var_pts': round(100 * (x[3] / (x[3] + x[4]) - x[1] / (x[1] + x[2])), 3)} for lado, x in v.items()}
    # (3) contrafactuais
    tL = tR = 0; sL = sR = 0; cf = 0.0; n = 0
    for k, d in b.items():
        s2 = d.get('2')
        if not s2:
            continue
        tL += s2['L']; tR += s2['R']
        e = seg(s2.get('enc'))
        if e is not None and e >= 17 * 3600 + 16 * 60:
            n += 1; sL += s2['L']; sR += s2['R']
            s1 = d.get('1')
            if s1 and s1['L'] + s1['R'] > 0:
                p = s1['L'] / (s1['L'] + s1['R'])
            else:
                p = s2['L'] / (s2['L'] + s2['R']) if s2['L'] + s2['R'] else 0.5
            cf += (2 * p - 1) * (s2['L'] + s2['R'])
    R['contrafactual'] = {'margem_nacional': tL - tR, 'secoes_J2_J3': n, 'margem_J2_J3': sL - sR,
                          'margem_sem_J2_J3': tL - tR - (sL - sR),
                          'margem_J2_J3_com_fatia_do_1t': round(cf),
                          'margem_nacional_com_J2_J3_na_fatia_do_1t': round(tL - tR - (sL - sR) + cf)}
    json.dump(R, open(saida, 'w'), ensure_ascii=False, indent=1)
    print(json.dumps(R, ensure_ascii=False, indent=1))


if __name__ == '__main__':
    main()
