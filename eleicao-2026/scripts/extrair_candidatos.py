"""Votos por candidato e por seção (1º turno), para a análise de fluxos. Padrão: presidente (cargo 1).
Uso: python3 -I extrair_candidatos.py <saida.json.gz> [--cargo 3] <zip> [<zip> ...]
Saída: {"UF|mun|zona|secao": {"<numero>": votos, ...}} só com votos nominais de presidente; e totais nacionais com nomes.
"""
import csv, gzip, io, json, sys, zipfile, collections
from functools import partial
from multiprocessing import Pool


def proc(zp, cargo='1'):
    out = {}; nomes = {}
    z = zipfile.ZipFile(zp)
    nome = [n for n in z.namelist() if n.lower().endswith('.csv')][0]
    with z.open(nome) as fh:
        rd = csv.reader(io.TextIOWrapper(fh, encoding='latin1', newline=''), delimiter=';')
        cab = next(rd); ix = {c.strip(): i for i, c in enumerate(cab)}
        for r in rd:
            if r[ix['CD_CARGO_PERGUNTA']] != cargo or r[ix['CD_TIPO_VOTAVEL']] != '1':
                continue
            k = f"{r[ix['SG_UF']]}|{int(r[ix['CD_MUNICIPIO']])}|{int(r[ix['NR_ZONA']])}|{int(r[ix['NR_SECAO']])}"
            n = r[ix['NR_VOTAVEL']]; nomes[n] = r[ix['NM_VOTAVEL']]
            out.setdefault(k, {})[n] = out.get(k, {}).get(n, 0) + int(r[ix['QT_VOTOS']])
    return out, nomes


if __name__ == '__main__':
    tudo = {}; nomes = {}; tot = collections.Counter()
    args = sys.argv[2:]; cargo = '1'
    if '--cargo' in args:
        i = args.index('--cargo'); cargo = args[i + 1]; args = args[:i] + args[i + 2:]
    with Pool(4) as p:
        for out, nm in p.imap_unordered(partial(proc, cargo=cargo), sorted(args, key=lambda x: -__import__('os').path.getsize(x))):
            tudo.update(out); nomes.update(nm)
    for v in tudo.values():
        for n, q in v.items(): tot[n] += q
    with gzip.open(sys.argv[1], 'wt') as f:
        json.dump({'secoes': tudo, 'nomes': nomes, 'totais': tot}, f, separators=(',', ':'))
    for n, q in tot.most_common(): print(n, nomes[n], q)
