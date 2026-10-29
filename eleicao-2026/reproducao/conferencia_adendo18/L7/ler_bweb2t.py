"""Leitura própria do bweb do 2º turno (linhas de Presidente) para a conferência do L7.
Por seção: urna, carga, biometria sem habilitação, comparecimento, aptos, local, município, votos 13 e 22, tipo de urna."""
import csv, glob, gzip, io, json, os, sys, zipfile
from multiprocessing import Pool

ZDIR, SAIDA = sys.argv[1], sys.argv[2]


def ler(zp):
    z = zipfile.ZipFile(zp)
    nome = [n for n in z.namelist() if n.lower().endswith('.csv')][0]
    out = {}
    conflito = 0
    with z.open(nome) as fh:
        r = csv.reader(io.TextIOWrapper(fh, encoding='latin1', newline=''), delimiter=';', quotechar='"')
        cab = next(r)
        ix = {c: i for i, c in enumerate(cab)}
        for p in r:
            if p[ix['CD_CARGO_PERGUNTA']] != '1':
                continue
            k = f"{p[ix['SG_UF']]}|{int(p[ix['CD_MUNICIPIO']])}|{int(p[ix['NR_ZONA']])}|{int(p[ix['NR_SECAO']])}"
            base = (p[ix['NR_URNA_EFETIVADA']], p[ix['DT_CARGA_URNA_EFETIVADA']], p[ix['QT_ELEI_BIOM_SEM_HABILITACAO']],
                    p[ix['QT_COMPARECIMENTO']], p[ix['QT_APTOS']], p[ix['NR_LOCAL_VOTACAO']], p[ix['NM_MUNICIPIO']],
                    p[ix['DS_TIPO_URNA']], p[ix['DS_SECOES_AGREGADAS']])
            d = out.get(k)
            if d is None:
                d = {'urna': base[0], 'carga': base[1], 'biomsem': int(base[2]), 'comp': int(base[3]), 'apt': int(base[4]),
                     'loc': int(base[5]), 'mun': base[6], 'tipo': base[7], 'agreg': base[8], 'L': 0, 'R': 0}
                out[k] = d
            elif (d['urna'], d['carga'], d['biomsem'], d['comp']) != (base[0], base[1], int(base[2]), int(base[3])):
                conflito += 1
            nv = p[ix['NR_VOTAVEL']]
            if nv == '13':
                d['L'] += int(p[ix['QT_VOTOS']])
            elif nv == '22':
                d['R'] += int(p[ix['QT_VOTOS']])
    return os.path.basename(zp), out, conflito


if __name__ == '__main__':
    zips = sorted(glob.glob(os.path.join(ZDIR, '*.zip')))
    with Pool(4) as P:
        partes = P.map(ler, zips)
    tudo = {}
    for nome, d, c in partes:
        print(nome, len(d), 'conflitos', c)
        tudo.update(d)
    with gzip.open(SAIDA, 'wt') as f:
        json.dump(tudo, f)
    print('total', len(tudo))
