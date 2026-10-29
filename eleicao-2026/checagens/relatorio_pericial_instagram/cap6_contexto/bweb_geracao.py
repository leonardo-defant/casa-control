import zipfile, sys, io, csv, collections
for z in sys.argv[1:]:
    zf = zipfile.ZipFile(z)
    nm = [n for n in zf.namelist() if n.lower().endswith('.csv')][0]
    with zf.open(nm) as fh:
        r = csv.reader(io.TextIOWrapper(fh, encoding='latin1'), delimiter=';')
        h = next(r)
        i_dg, i_hg = h.index('DT_GERACAO'), h.index('HH_GERACAO')
        i_rec = h.index('DT_BU_RECEBIDO') if 'DT_BU_RECEBIDO' in h else None
        ger = collections.Counter(); mx = None; mn = None
        for k, row in enumerate(r):
            ger[(row[i_dg], row[i_hg])] += 1
            if i_rec is not None:
                v = row[i_rec]
                # formato dd/mm/aaaa hh:mm:ss
                key = (v[6:10], v[3:5], v[0:2], v[11:])
                mx = key if mx is None or key > mx else mx
                mn = key if mn is None or key < mn else mn
        print(z.split('/')[-1], 'linhas', k + 1, 'geracao', dict(ger), 'BU recebido min', mn, 'max', mx)
