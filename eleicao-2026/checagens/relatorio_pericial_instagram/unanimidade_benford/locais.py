"""Cadastro de locais de votação 2026: por turno e seção (chave UF|mun|zona|secao), nome do município e do local,
endereço, bairro, tipo de local e flags de local indígena e rural pelo texto (nome, endereço, bairro).
Uso: python3 -I locais.py <pasta_locais> <saida.json.gz>"""
import csv, glob, gzip, json, os, re, sys, unicodedata

IND = re.compile(r'INDIGEN|ALDEIA|\bMALOCA\b')
RUR = re.compile(r'ZONA RURAL|\bRURAL\b|POVOADO|\bPOV\b|\bSITIO\b|\bFAZENDA\b|\bFAZ\b|ASSENTAMENTO|\bASSENT\b|AGROVILA|'
                 r'COMUNIDADE|\bCOM\b|\bRAMAL\b|IGARAPE|VICINAL|\bLOCALIDADE\b|\bGLEBA\b|\bCOLONIA\b|RIBEIRINH|\bINTERIOR\b|\bLINHA\b|\bRIO [A-Z]+ ?KM|\bKM\b')


def norm(s):
    s = unicodedata.normalize('NFKD', s.upper())
    return re.sub(r'[^A-Z0-9 ]', ' ', ''.join(c for c in s if not unicodedata.combining(c)))


pasta, saida = sys.argv[1:3]
out = {'1': {}, '2': {}}
for f in sorted(glob.glob(os.path.join(pasta, 'eleitorado_local_votacao_2026_??.csv'))):
    with open(f, encoding='latin1') as fh:
        r = csv.reader(fh, delimiter=';'); h = next(r); i = {c: j for j, c in enumerate(h)}
        for row in r:
            if row[i['DS_TIPO_SECAO_AGREGADA']] != 'Principal':
                continue
            t = row[i['NR_TURNO']]
            k = f"{row[i['SG_UF']]}|{int(row[i['CD_MUNICIPIO']])}|{int(row[i['NR_ZONA']])}|{int(row[i['NR_SECAO']])}"
            nome, end, bai = row[i['NM_LOCAL_VOTACAO']], row[i['DS_ENDERECO']], row[i['NM_BAIRRO']]
            tx = norm(' '.join((nome, end, bai)))
            out[t][k] = [row[i['NM_MUNICIPIO']], int(row[i['NR_LOCAL_VOTACAO']]), nome, end, bai, row[i['DS_TIPO_LOCAL']],
                         int(bool(IND.search(tx))), int(bool(RUR.search(tx))), row[i['NR_LATITUDE']], row[i['NR_LONGITUDE']]]
for t in out:
    print('turno', t, 'secoes', len(out[t]), 'indigena', sum(v[6] for v in out[t].values()), 'rural', sum(v[7] for v in out[t].values()))
with gzip.open(saida, 'wt') as fz:
    json.dump(out, fz, separators=(',', ':'))
