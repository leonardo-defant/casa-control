"""Dados do mapa de pontos do vídeo (video/dados/cidades.json): uma linha por cidade com posição e resultado.
Posição: média das coordenadas dos locais de votação do 2º turno. 1º turno: soma das seções do bweb. 2º turno: totais do
município no site de resultados (baixar_municipios.py). As réguas são as mesmas do T38 (analisar_municipios.py):
quem ganhou mais votos (gL contra gR) e para que lado andou a margem em pontos dos válidos (pL contra pR).
Uso: python3 -I montar_cidades_video.py <secoes2026_1t.json.gz> <pasta_mun2t> <pasta CSV eleitorado_local_votacao_2026> <saida.json>
"""
import os as _os, sys as _sys
_sys.path.insert(0, _os.path.dirname(_os.path.abspath(__file__)))
import collections, csv, glob, json, os, sys
from lib import carregar


def sinal(a, b):
    return 1 if a > b else (-1 if b > a else 0)


def main():
    base, pasta, locais, saida = sys.argv[1:5]
    pos = collections.defaultdict(lambda: [0.0, 0.0, 0])
    for f in glob.glob(os.path.join(locais, 'eleitorado_local_votacao_2026_??.csv')):
        with open(f, encoding='latin1') as fh:
            r = csv.reader(fh, delimiter=';'); h = next(r); i = {c: j for j, c in enumerate(h)}
            vistos = set()
            for row in r:
                if row[i['NR_TURNO']] != '2':
                    continue
                try:
                    la = float(row[i['NR_LATITUDE']].replace(',', '.')); lo = float(row[i['NR_LONGITUDE']].replace(',', '.'))
                except ValueError:
                    continue
                if la == -1 or lo == -1 or not (-34.5 < la < 6 and -74.5 < lo < -28.5):
                    continue
                key = (row[i['SG_UF']], int(row[i['CD_MUNICIPIO']])); lv = (key, row[i['NR_LOCAL_VOTACAO']])
                if lv in vistos:
                    continue
                vistos.add(lv); p = pos[key]; p[0] += la; p[1] += lo; p[2] += 1
    t1 = collections.defaultdict(collections.Counter)
    for k, v in carregar(base).items():
        if '1' in v and not k.startswith('ZZ|'):
            a = v['1']; uf, m = k.split('|')[:2]
            t1[(uf, int(m))].update({'L': a['L'], 'R': a['R'], 'V': a['L'] + a['R'] + a['O'] - a.get('c28', 0)})
    cid, sem = [], 0
    for f in sorted(os.listdir(pasta)):
        if not f.endswith('.json'):
            continue
        uf, m = f[:2].upper(), int(f[2:7]); o = json.load(open(os.path.join(pasta, f)))
        c = {x['n']: int(x['vap']) for a in o['carg'][0]['agr'] for p in a['par'] for x in p['cand']}
        a = t1[(uf, m)]; L2, R2 = c.get('13', 0), c.get('22', 0); p = pos.get((uf, m))
        if not p or p[2] == 0 or a['V'] <= 0 or L2 + R2 <= 0:
            sem += 1
            continue
        pL = 100 * (L2 / (L2 + R2) - a['L'] / a['V']); pR = 100 * (R2 / (L2 + R2) - a['R'] / a['V'])
        cid.append([round(p[0] / p[2], 4), round(p[1] / p[2], 4), sinal(L2 - a['L'], R2 - a['R']),
                    round(100 * a['R'] / a['V'], 3), L2 + R2, uf, sinal(pL, pR)])
    json.dump({'campos': ['lat', 'lon', 'quem_ganhou_mais_votos(1=Lula,-1=Flavio,0=empate)', 'fatia_Flavio_1T',
                          'votos_validos_2T', 'uf', 'para_onde_andou_a_margem_em_pontos(1=Lula,-1=Flavio,0=empate)'],
               'cidades': cid}, open(saida, 'w'), separators=(',', ':'))
    red = [x for x in cid if x[3] >= 65]
    print('cidades:', len(cid), '| fora do mapa:', sem)
    print('redutos (>= 65% de Flávio no 1º turno):', len(red), '| margem andou para Lula:', sum(x[6] == 1 for x in red),
          f'({100 * sum(x[6] == 1 for x in red) / len(red):.1f}%)', '| Lula ganhou mais votos:', sum(x[2] == 1 for x in red))


if __name__ == '__main__':
    main()
