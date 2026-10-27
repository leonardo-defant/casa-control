"""T38 por município (Adendo 16, descritivo) e o número das "213 cidades viradas".
1º turno: soma das seções do bweb; 2º turno: arquivo de totais do município no site de resultados (baixar_municipios.py).
Uso: python3 -I analisar_municipios.py <secoes2026_1t.json.gz> <pasta_mun2t> <saida.json> [--nomes <pasta CSV eleitorado_local_votacao_2026>]
"""
import os as _os, sys as _sys
_sys.path.insert(0, _os.path.dirname(_os.path.abspath(__file__)))
import collections, csv, glob, json, os, sys
from lib import carregar


def main():
    base, pasta, saida = sys.argv[1:4]
    nomes = {}
    if '--nomes' in sys.argv:
        for f in glob.glob(os.path.join(sys.argv[sys.argv.index('--nomes') + 1], 'eleitorado_local_votacao_2026_??.csv')):
            with open(f, encoding='latin1') as fh:
                r = csv.reader(fh, delimiter=';'); h = next(r); i = {c: j for j, c in enumerate(h)}
                for row in r:
                    nomes[(row[i['SG_UF']], int(row[i['CD_MUNICIPIO']]))] = row[i['NM_MUNICIPIO']]
    t1 = collections.defaultdict(collections.Counter)
    for k, v in carregar(base).items():
        if '1' in v and not k.startswith('ZZ|'):
            a = v['1']; uf, m = k.split('|')[:2]
            t1[(uf, int(m))].update({'L': a['L'], 'R': a['R'], 'V': a['L'] + a['R'] + a['O'] - a.get('c28', 0)})
    rows = []
    for f in sorted(os.listdir(pasta)):
        if not f.endswith('.json'):
            continue
        uf, m = f[:2].upper(), int(f[2:7]); o = json.load(open(os.path.join(pasta, f)))
        c = {x['n']: int(x['vap']) for a in o['carg'][0]['agr'] for p in a['par'] for x in p['cand']}
        a = t1.get((uf, m))
        if not a or a['V'] <= 0:
            continue
        L2, R2 = c.get('13', 0), c.get('22', 0)
        if L2 + R2 <= 0:
            continue
        completo = o['s']['st'] == o['s']['ts']
        rows.append({'uf': uf, 'mun': m, 'nome': nomes.get((uf, m), ''), 'L1': a['L'], 'R1': a['R'], 'V1': a['V'], 'L2': L2, 'R2': R2,
                     'gL': L2 - a['L'], 'gR': R2 - a['R'], 'pL': 100 * (L2 / (L2 + R2) - a['L'] / a['V']),
                     'pR': 100 * (R2 / (L2 + R2) - a['R'] / a['V']), 'completo': completo})
    n = len(rows)
    mais_votos = [r for r in rows if r['gR'] > r['gL']]; mais_pontos = [r for r in rows if r['pR'] > r['pL']]
    virou_lula = [r for r in rows if r['R1'] > r['L1'] and r['L2'] > r['R2']]
    virou_flavio = [r for r in rows if r['L1'] > r['R1'] and r['R2'] > r['L2']]
    por_uf = collections.defaultdict(lambda: [0, 0, 0, 0, 0])
    for r in rows:
        u = por_uf[r['uf']]; u[0] += 1; u[1] += r['gR'] > r['gL']; u[2] += r['pR'] > r['pL']
        u[3] += r in virou_lula; u[4] += r in virou_flavio
    out = {'municipios': n, 'soma_L2': sum(r['L2'] for r in rows), 'soma_R2': sum(r['R2'] for r in rows), 'totalizacao_incompleta': sum(1 for r in rows if not r['completo']),
           'flavio_mais_votos_que_lula': len(mais_votos), 'flavio_mais_pontos_que_lula': len(mais_pontos),
           'viraram_de_flavio_para_lula': len(virou_lula), 'viraram_de_lula_para_flavio': len(virou_flavio),
           'por_uf_[municipios,mais_votos,mais_pontos,viraram_p_Lula,viraram_p_Flavio]': dict(sorted(por_uf.items())),
           'lista_flavio_mais_pontos': sorted(({k: r[k] for k in ('uf', 'mun', 'nome', 'gL', 'gR', 'pL', 'pR')} for r in mais_pontos), key=lambda r: r['pL'] - r['pR']),
           'lista_viraram_para_flavio': [{k: r[k] for k in ('uf', 'mun', 'nome', 'L1', 'R1', 'L2', 'R2')} for r in virou_flavio]}
    # vitórias, empates e uniformidade da virada (variação da margem de Flávio, em pontos dos válidos)
    out['vitorias'] = {'Lula_1T': sum(r['L1'] > r['R1'] for r in rows), 'empates_1T': sum(r['L1'] == r['R1'] for r in rows),
                       'Lula_2T': sum(r['L2'] > r['R2'] for r in rows), 'empates_2T': sum(r['L2'] == r['R2'] for r in rows),
                       'empate_1T_e_Lula_2T': sum(r['L1'] == r['R1'] and r['L2'] > r['R2'] for r in rows),
                       'Lula_mais_votos': sum(r['gL'] > r['gR'] for r in rows), 'empates_no_ganho': sum(r['gL'] == r['gR'] for r in rows)}
    import math, statistics
    sw = [r['pR'] - r['pL'] for r in rows]
    def prev(x):
        m, d = statistics.mean(x), statistics.stdev(x)
        return m, d, 50 * math.erfc(-m / (d * math.sqrt(2)))  # % previsto andando para Flávio por uma normal
    m, d, pv = prev(sw)
    uni = {'media': m, 'mediana': statistics.median(sw), 'desvio': d, 'previsto_para_Flavio_pct': pv,
           'observado_para_Flavio_pct': 100 * sum(x > 0 for x in sw) / n, 'por_uf': {}, 'por_faixa_Flavio_1T': {}}
    for uf in sorted({r['uf'] for r in rows}):
        x = [r['pR'] - r['pL'] for r in rows if r['uf'] == uf]
        if len(x) >= 10:
            mu, du, pu = prev(x)
            uni['por_uf'][uf] = {'cidades': len(x), 'media': mu, 'desvio': du, 'previsto_para_Flavio_pct': pu,
                                 'observado_para_Flavio_pct': 100 * sum(v > 0 for v in x) / len(x)}
    for lo, hi in [(0, 30), (30, 45), (45, 55), (55, 65), (65, 101)]:
        x = [r['pR'] - r['pL'] for r in rows if lo <= 100 * r['R1'] / r['V1'] < hi]
        uni['por_faixa_Flavio_1T'][f'{lo}-{hi}'] = {'cidades': len(x), 'media': statistics.mean(x),
                                                     'para_Flavio_pct': 100 * sum(v > 0 for v in x) / len(x)}
    out['uniformidade'] = uni
    json.dump(out, open(saida, 'w'), ensure_ascii=False, indent=1)
    print(json.dumps({k: v for k, v in out.items() if not k.startswith('lista') and k != 'uniformidade'}, ensure_ascii=False))
    print(json.dumps({k: v for k, v in uni.items() if k != 'por_uf'}, ensure_ascii=False))
    print({u: (round(v['previsto_para_Flavio_pct'], 1), round(v['observado_para_Flavio_pct'], 1)) for u, v in uni['por_uf'].items() if u in ('RS', 'SC', 'GO', 'BA', 'SP')})
    for r in out['lista_flavio_mais_pontos'][:15]:
        print('  Flávio ganhou mais pontos:', r['uf'], r['nome'], f"Flávio {r['pR']:+.2f} pts ({r['gR']:+,}) x Lula {r['pL']:+.2f} pts ({r['gL']:+,})")


if __name__ == '__main__':
    main()
