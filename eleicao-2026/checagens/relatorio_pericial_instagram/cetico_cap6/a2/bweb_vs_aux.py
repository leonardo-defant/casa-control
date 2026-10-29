import zipfile, io, csv, sys, os, json, collections, glob
zdir, arq = sys.argv[1], sys.argv[2]
for uf in ['AC','AP','DF','AL']:
    z = glob.glob(os.path.join(zdir, f'bweb_2t_{uf}_*.zip'))[0]
    zf = zipfile.ZipFile(z)
    nm = [n for n in zf.namelist() if n.lower().endswith('.csv')][0]
    rec = {}; ger = collections.Counter()
    with zf.open(nm) as fh:
        r = csv.reader(io.TextIOWrapper(fh, encoding='latin1'), delimiter=';')
        h = next(r)
        if uf == 'AC': print('header', h)
        ix = {k: i for i, k in enumerate(h)}
        for row in r:
            ger[(row[ix['DT_GERACAO']], row[ix['HH_GERACAO']])] += 1
            k = (row[ix['CD_MUNICIPIO']].zfill(5), row[ix['NR_ZONA']].zfill(4), row[ix['NR_SECAO']].zfill(4))
            rec[k] = (row[ix['DT_BU_RECEBIDO']], row[ix['DT_ENCERRAMENTO']] if 'DT_ENCERRAMENTO' in ix else None, row[ix['DT_ABERTURA']] if 'DT_ABERTURA' in ix else None)
    print(uf, 'geracao', dict(ger))
    # compare with aux
    n = 0; iguais = 0; difs = collections.Counter(); ex = []
    for p in glob.glob(os.path.join(arq, uf.lower(), '*', '*', '*', 'aux.json')):
        parts = p.split('/')
        k = (parts[-4], parts[-3], parts[-2])
        j = json.load(open(p, encoding='utf-8'))
        if k not in rec: continue
        hs = j['hashes'][-1]
        aux_dr = hs['dr'][6:10] + '-' + hs['dr'][3:5] + '-' + hs['dr'][0:2] + ' ' + hs['hr']
        b = rec[k][0]
        n += 1
        if b.startswith(aux_dr[:16]) or b == aux_dr: iguais += 1
        else:
            if len(ex) < 3: ex.append((k, aux_dr, rec[k]))
    print(uf, 'secoes comparadas', n, 'DT_BU_RECEBIDO == dr do aux (ate o minuto)', iguais, 'exemplos diferentes', ex)
    print(uf, 'exemplo bweb', list(rec.items())[:2])
