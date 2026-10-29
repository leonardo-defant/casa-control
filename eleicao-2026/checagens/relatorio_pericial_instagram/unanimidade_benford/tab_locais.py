import csv, glob, collections, sys
P='/tmp/claude-0/-home-user-casa-control/ce2a8c88-e5ad-504f-8950-6f5ee14ae721/scratchpad/locais_votacao/'
c=collections.Counter(); s=collections.Counter(); z=collections.Counter()
for f in sorted(glob.glob(P+'eleitorado_local_votacao_2026_??.csv')):
    with open(f,encoding='latin1') as fh:
        r=csv.reader(fh,delimiter=';'); h=next(r); i={k:j for j,k in enumerate(h)}
        for row in r:
            if row[i['NR_TURNO']]!='2': continue
            c[(row[i['CD_TIPO_LOCAL']],row[i['DS_TIPO_LOCAL']])]+=1
            s[(row[i['CD_SITU_LOCALIDADE']],row[i['DS_SITU_LOCALIDADE']])]+=1
            z[(row[i['CD_SITU_ZONA']],row[i['DS_SITU_ZONA']])]+=1
print(c.most_common()); print(s.most_common()); print(z.most_common())
