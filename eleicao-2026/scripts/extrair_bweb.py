"""Extrai Presidente (cargo 1) e Governador (cargo 3) dos zips bweb_* do TSE.

Uso: python3 -I extrair_bweb.py <turno 1|2> <saida.json.gz> <zip> [<zip> ...]
Saída: {"UF|mun|zona|secao": {"<t>": {loc, urna, tipo, apt, comp, ab, enc, L, R, O, B, N, agr},
                               "<t>g": {B, N, V, comp}}}
L = 13, R = 22 (2026), O = demais nominais (inclui o 28 cassado, também em c28), B = branco, N = nulo.
"""
import csv, gzip, io, json, sys, zipfile
from multiprocessing import Pool

ESQ, DIR = 13, 22

def processa(args):
    zpath, turno = args
    out = {}
    z = zipfile.ZipFile(zpath)
    nome = [n for n in z.namelist() if n.lower().endswith('.csv')][0]
    with z.open(nome) as fh:
        txt = io.TextIOWrapper(fh, encoding='latin1', newline='')
        rd = csv.reader(txt, delimiter=';')
        cab = next(rd)
        ix = {c.strip().replace('SG_ UF', 'SG_UF'): i for i, c in enumerate(cab)}
        g = lambda r, c: r[ix[c]]
        iC = ix['CD_CARGO_PERGUNTA']
        for r in rd:
            cargo = r[iC]
            if cargo not in ('1', '3'):
                continue
            k = f"{g(r,'SG_UF')}|{int(g(r,'CD_MUNICIPIO'))}|{int(g(r,'NR_ZONA'))}|{int(g(r,'NR_SECAO'))}"
            d = out.setdefault(k, {})
            tv = int(g(r, 'CD_TIPO_VOTAVEL')); nv = int(g(r, 'NR_VOTAVEL')); q = int(g(r, 'QT_VOTOS'))
            if cargo == '1':
                s = d.get(turno)
                if s is None:
                    s = d[turno] = {'loc': int(g(r, 'NR_LOCAL_VOTACAO')), 'urna': int(g(r, 'NR_URNA_EFETIVADA') or 0),
                                    'tipo': g(r, 'DS_TIPO_URNA'), 'apt': int(g(r, 'QT_APTOS')),
                                    'comp': int(g(r, 'QT_COMPARECIMENTO')),
                                    'ab': g(r, 'DT_ABERTURA')[-8:], 'enc': g(r, 'DT_ENCERRAMENTO')[-8:],
                                    'L': 0, 'R': 0, 'O': 0, 'B': 0, 'N': 0}
                    agr = g(r, 'DS_SECOES_AGREGADAS') if 'DS_SECOES_AGREGADAS' in ix else ''
                    if agr and agr != '#NULO#':
                        s['agr'] = agr
                if tv == 2: s['B'] += q
                elif tv == 3: s['N'] += q
                elif nv == ESQ: s['L'] += q
                elif nv == DIR: s['R'] += q
                else:
                    s['O'] += q
                    if nv == 28: s['c28'] = s.get('c28', 0) + q
            else:
                s = d.get(turno + 'g')
                if s is None:
                    s = d[turno + 'g'] = {'B': 0, 'N': 0, 'V': 0, 'comp': int(g(r, 'QT_COMPARECIMENTO'))}
                if tv == 2: s['B'] += q
                elif tv == 3: s['N'] += q
                else: s['V'] += q
    return zpath, out

if __name__ == '__main__':
    turno, saida, zips = sys.argv[1], sys.argv[2], sys.argv[3:]
    zips.sort(key=lambda p: -__import__('os').path.getsize(p))
    tudo = {}
    with Pool(4) as p:
        for zp, out in p.imap_unordered(processa, [(z, turno) for z in zips]):
            print('ok', zp.split('/')[-1], len(out), flush=True)
            for k, v in out.items():
                tudo.setdefault(k, {}).update(v)
    with gzip.open(saida, 'wt') as f:
        json.dump(tudo, f, separators=(',', ':'))
    print('secoes', len(tudo))
