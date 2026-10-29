"""Le os zips bweb do 2o turno 2026 diretamente (sem usar a base json) e grava uma tabela por secao."""
import sys, zipfile, io, csv, glob, gzip, json, collections
pasta = sys.argv[1]; saida = sys.argv[2]
sec = {}
tipos = collections.Counter(); dup = 0
for z in sorted(glob.glob(pasta + '/*.zip')):
    with zipfile.ZipFile(z) as zf:
        nome = [n for n in zf.namelist() if n.endswith('.csv')][0]
        with zf.open(nome) as fb:
            f = io.TextIOWrapper(fb, encoding='latin1', newline='')
            r = csv.reader(f, delimiter=';')
            h = next(r); ix = {c: i for i, c in enumerate(h)}
            iuf, imun, izon, isec = ix['SG_UF'], ix['CD_MUNICIPIO'], ix['NR_ZONA'], ix['NR_SECAO']
            icar, ivot, iqt, itv = ix['CD_CARGO_PERGUNTA'], ix['NR_VOTAVEL'], ix['QT_VOTOS'], ix['DS_TIPO_VOTAVEL']
            for row in r:
                if row[icar] != '1':
                    continue
                k = f"{row[iuf]}|{row[imun]}|{row[izon]}|{row[isec]}"
                s = sec.get(k)
                if s is None:
                    s = {'uf': row[iuf], 'mun': row[imun], 'nmun': row[ix['NM_MUNICIPIO']], 'loc': row[ix['NR_LOCAL_VOTACAO']],
                         'apt': int(row[ix['QT_APTOS']]), 'comp': int(row[ix['QT_COMPARECIMENTO']]),
                         'tipo': row[ix['DS_TIPO_URNA']], 'ab': row[ix['DT_ABERTURA']], 'enc': row[ix['DT_ENCERRAMENTO']],
                         'nh': row[ix['QT_ELEI_BIOM_SEM_HABILITACAO']], 'rec': row[ix['DT_BU_RECEBIDO']],
                         'emi': row[ix['DT_EMISSAO_BU']], 'agr': row[ix['DS_SECOES_AGREGADAS']], 'L': 0, 'R': 0, 'B': 0, 'N': 0, 'X': 0, 'urna': row[ix['NR_URNA_EFETIVADA']]}
                    sec[k] = s
                    tipos[s['tipo']] += 1
                else:
                    if s['urna'] != row[ix['NR_URNA_EFETIVADA']] or s['enc'] != row[ix['DT_ENCERRAMENTO']]:
                        dup += 1
                q = int(row[iqt]); v = row[ivot]
                if v == '13': s['L'] += q
                elif v == '22': s['R'] += q
                elif v == '95': s['B'] += q
                elif v == '96': s['N'] += q
                else: s['X'] += q
    print(z.split('/')[-1], len(sec), flush=True)
print('tipos', tipos, 'linhas com urna/enc divergente na mesma secao', dup)
with gzip.open(saida, 'wt') as f:
    json.dump(sec, f)
