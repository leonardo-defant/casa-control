import csv, glob, re, unicodedata, pickle, json, collections
import numpy as np
P = '/tmp/claude-0/-home-user-casa-control/ce2a8c88-e5ad-504f-8950-6f5ee14ae721/scratchpad/'
Q = P + 'relatorio_pericial/cetico_unan/'
def norm(s):
    s = unicodedata.normalize('NFKD', s.upper())
    return re.sub(r'[^A-Z0-9 ]', ' ', ''.join(c for c in s if not unicodedata.combining(c)))
LOC = {}; nsec_local = collections.Counter()
for f in sorted(glob.glob(P + 'locais_votacao/eleitorado_local_votacao_2026_??.csv')):
    with open(f, encoding='latin1') as fh:
        r = csv.reader(fh, delimiter=';'); h = next(r); i = {c: j for j, c in enumerate(h)}
        for row in r:
            if row[i['NR_TURNO']] != '2': continue
            if row[i['DS_TIPO_SECAO_AGREGADA']] != 'Principal': continue
            k = f"{row[i['SG_UF']]}|{int(row[i['CD_MUNICIPIO']])}|{int(row[i['NR_ZONA']])}|{int(row[i['NR_SECAO']])}"
            loc = f"{row[i['SG_UF']]}|{int(row[i['CD_MUNICIPIO']])}|{row[i['NR_LOCAL_VOTACAO']]}"
            LOC[k] = (row[i['NM_MUNICIPIO']], row[i['NM_LOCAL_VOTACAO']], row[i['DS_ENDERECO']], row[i['NM_BAIRRO']], row[i['DS_TIPO_LOCAL']], loc)
            nsec_local[loc] += 1
pickle.dump((LOC, nsec_local), open(Q + 'locais.pkl', 'wb'))
print('secoes', len(LOC), 'locais', len(nsec_local))
