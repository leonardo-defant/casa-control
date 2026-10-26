"""T30 do pré-registro (adendo 9): gatilho por horário ou por contagem de votos.

Horário: fração f das confirmações de voto depois das 12h, 14h e 16h (hora de Brasília) em cada turno, lida do log da urna.
O fuso de cada urna sai da UF (o pré-registro previa tirá-lo do horário em que a urna ficou pronta; 3 urnas da amostra
abriram depois das 8h30 no 1º turno e teriam o fuso errado por essa regra, por isso a UF).
Regressão da variação da fatia de Lula em f2, controlando f1 e a variação do comparecimento, efeito fixo de município.
Contagem: variação da fatia de Lula em max(0, votantes - N) / votantes, N = 50, 100, 150, 200, efeito fixo de local.
Uso: python3 -I analisar_gatilhos.py <pasta_arq_2t> <secoes2026_1t.json.gz> <amostra_2t.json.gz> [<secoes2022.json.gz>]
"""
import os as _os, sys as _sys
_sys.path.insert(0, _os.path.dirname(_os.path.abspath(__file__)))
import json, os, sys, warnings
import numpy as np
from decodificar import _linhas_log, RX
from lib import carregar, chave_local, fe_ols
warnings.filterwarnings('ignore')
CORTES_H = (12, 14, 16)
CORTES_N = (50, 100, 150, 200)
FUSO = {'AC': -2, 'AM': -1, 'RO': -1, 'RR': -1, 'MT': -1, 'MS': -1}  # horas da hora local para a de Brasília


def horarios(caminho, data):
    """Segundos do dia de cada voto computado e da urna pronta, somando todos os logs do pacote."""
    votos, pronta = [], []
    for linhas in _linhas_log(caminho):
        for l in linhas:
            p = l.split('\t')
            if len(p) < 5 or not p[0].startswith(data):
                continue
            m = RX.match(p[0])
            if not m:
                continue
            t = int(m.group(2)) * 3600 + int(m.group(3)) * 60 + int(m.group(4))
            if p[4] == 'O voto do eleitor foi computado':
                votos.append(t)
            elif p[4] == 'Urna pronta para receber votos':
                pronta.append(t)
    return votos, (min(pronta) if pronta else None)


def fracoes(votos, pronta, uf):
    if not votos or pronta is None:
        return None
    desloc = FUSO.get(uf, 0)
    v = np.array(votos) / 3600 - desloc
    return {h: float((v >= h).mean()) for h in CORTES_H}, desloc


def secoes(pasta):
    for uf in sorted(os.listdir(pasta)):
        for m in sorted(os.listdir(os.path.join(pasta, uf))):
            for z in sorted(os.listdir(os.path.join(pasta, uf, m))):
                for s in sorted(os.listdir(os.path.join(pasta, uf, m, z))):
                    yield f'{uf.upper()}|{int(m)}|{int(z)}|{int(s)}', os.path.join(pasta, uf, m, z, s)


def horario(pasta, d1, am):
    rows = []; sem = 0; deslocs = {}
    for k, p in secoes(pasta):
        lg = sorted(f for f in os.listdir(p) if f.endswith('-log.jez'))
        if not lg or k not in am or '2' not in am[k] or '1' not in d1.get(k, {}):
            continue
        v2, p2 = horarios(os.path.join(p, lg[-1]), '25/10/2026')
        v1, p1 = horarios(os.path.join(p, lg[-1]), '04/10/2026')
        f2 = fracoes(v2, p2, k.split('|')[0]); f1 = fracoes(v1, p1, k.split('|')[0])
        if not f2 or not f1:
            sem += 1; continue
        a, b = d1[k]['1'], am[k]['2']
        if a['L'] + a['R'] <= 0 or b['L'] + b['R'] <= 0:
            continue
        deslocs[k.split('|')[0]] = deslocs.get(k.split('|')[0], set()) | {f2[1], f1[1]}
        rows.append((k, f1[0], f2[0], a, b))
    out = {'secoes': len(rows), 'sem_log_dos_dois_turnos': sem, 'fuso_por_uf': {u: sorted(s) for u, s in deslocs.items()},
           'cortes': {}}
    mun = ['|'.join(r[0].split('|')[:2]) for r in rows]
    loc = [chave_local(r[0], r[4]) for r in rows]
    fat1 = np.array([100 * r[3]['L'] / (r[3]['L'] + r[3]['R']) for r in rows])
    fat2 = np.array([100 * r[4]['L'] / (r[4]['L'] + r[4]['R']) for r in rows])
    dcomp = np.array([100 * (r[4]['comp'] - r[3]['comp']) / r[4]['apt'] for r in rows])
    w = np.array([r[4]['L'] + r[4]['R'] for r in rows], float)
    lapt = np.log([r[4]['apt'] for r in rows])
    for h in CORTES_H:
        F1 = np.array([r[1][h] for r in rows]); F2 = np.array([r[2][h] for r in rows])
        X = np.column_stack([F2, F1, dcomp])
        r2 = fe_ols(fat2 - fat1, X, mun, w, ['f2', 'f1', 'dcomp'])
        rp = fe_ols(fat1, np.column_stack([F1, lapt]), mun, w, ['f1', 'lapt'])
        b, se = r2['coef']['f2'], r2['ep']['f2']
        out['cortes'][f'{h}h'] = {'media_f1': float(F1.mean()), 'media_f2': float(F2.mean()), 'n': r2['n'], 'municipios': r2['grupos'],
                                  'inclinacao_f2': b, 'ep': se, 'z': b / se,
                                  'placebo_1t_inclinacao_f1': rp['coef']['f1'], 'placebo_ep': rp['ep']['f1'],
                                  'sinal': bool(b >= 4 and b / se > 2.93 and abs(rp['coef']['f1']) < 2 * rp['ep']['f1']),
                                  'sem_sinal': bool(abs(b) <= 1.5 and se <= 0.6), 'sem_poder': bool(se > 0.6)}
        # robustez (fora do pré-registro): efeito fixo de local, mais grupos para o erro agrupado
        rl = fe_ols(fat2 - fat1, X, loc, w, ['f2', 'f1', 'dcomp'])
        rlp = fe_ols(fat1, np.column_stack([F1, lapt]), loc, w, ['f1', 'lapt'])
        out['cortes'][f'{h}h']['robustez_local'] = {'n': rl['n'], 'locais': rl['grupos'], 'inclinacao_f2': rl['coef']['f2'],
                                                    'ep': rl['ep']['f2'], 'placebo_1t': rlp['coef']['f1'], 'placebo_ep': rlp['ep']['f1']}
    return out


def contagem(d1, d2, turno_a='1', turno_b='2'):
    """d1 e d2 podem ser o mesmo dicionário (2022) ou bases separadas (2026: 1º turno do bweb, 2º da amostra)."""
    rows = []
    for k, v in d2.items():
        b = v.get(turno_b); a = d1.get(k, {}).get(turno_a)
        if not a or not b or a['L'] + a['R'] <= 0 or b['L'] + b['R'] <= 0 or b['comp'] < 20:
            continue
        rows.append((chave_local(k, b), a, b))
    loc = [r[0] for r in rows]
    fat1 = np.array([100 * r[1]['L'] / (r[1]['L'] + r[1]['R']) for r in rows])
    fat2 = np.array([100 * r[2]['L'] / (r[2]['L'] + r[2]['R']) for r in rows])
    v = np.array([r[2]['comp'] for r in rows], float)
    dcomp = np.array([100 * (r[2]['comp'] - r[1]['comp']) / r[2]['apt'] for r in rows])
    w = np.array([r[2]['L'] + r[2]['R'] for r in rows], float)
    out = {'secoes': len(rows), 'cortes': {}}
    for N in CORTES_N:
        x = np.maximum(0, v - N) / v
        r = fe_ols(fat2 - fat1, np.column_stack([x, dcomp]), loc, w, ['x', 'dcomp'])
        b, se = r['coef']['x'], r['ep']['x']
        out['cortes'][N] = {'n': r['n'], 'locais': r['grupos'], 'fracao_com_votantes_acima': float((v > N).mean()),
                            'coef': b, 'ep': se, 'z': b / se}
    return out


def main():
    pasta, base1, amostra = sys.argv[1:4]
    d1 = carregar(base1); am = carregar(amostra)
    res = {'horario': horario(pasta, d1, am), 'contagem_2026': contagem(d1, am)}
    if len(sys.argv) > 4:
        d22 = carregar(sys.argv[4])
        res['contagem_2022_placebo'] = contagem(d22, d22)
        for N, c in res['contagem_2026']['cortes'].items():
            p = res['contagem_2022_placebo']['cortes'][N]
            c['sinal'] = bool(c['coef'] >= 4 and c['z'] > 3.02 and abs(p['coef']) < 1.5)
            c['sem_sinal'] = bool(abs(c['coef']) <= 1.5)
    print(json.dumps(res, ensure_ascii=False, indent=1))


if __name__ == '__main__':
    main()
