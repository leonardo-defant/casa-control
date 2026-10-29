"""Extrai, de um zip do bweb, uma linha por BU de Presidente: chave, local, aptos, comparecimento,
tipo de urna, NH (QT_ELEI_BIOM_SEM_HABILITACAO), votos 13, 22, outros nominais, brancos, nulos.
Uso: python3 -I extrai.py <zip> <saida.tsv>
Lê o CSV via unzip -p filtrado por grep (só linhas de Presidente), sem gravar o CSV inteiro."""
import subprocess, sys, csv, io

zp, out = sys.argv[1], sys.argv[2]
p1 = subprocess.Popen(['unzip', '-p', zp, '*.csv'], stdout=subprocess.PIPE)
p2 = subprocess.Popen(['grep', '-a', '-F', ';"Presidente";'], stdin=p1.stdout, stdout=subprocess.PIPE,
                      env={'LC_ALL': 'C', 'PATH': '/usr/bin:/bin'})
p1.stdout.close()
# cabeçalho: lê à parte
h = subprocess.run(f"unzip -p '{zp}' '*.csv' | head -1", shell=True, capture_output=True).stdout.decode('latin1')
cols = next(csv.reader([h.strip()], delimiter=';'))
ix = {c: i for i, c in enumerate(cols)}
need = ['SG_UF', 'CD_MUNICIPIO', 'NR_ZONA', 'NR_SECAO', 'NR_LOCAL_VOTACAO', 'CD_CARGO_PERGUNTA', 'DS_CARGO_PERGUNTA',
        'QT_APTOS', 'QT_COMPARECIMENTO', 'DS_TIPO_URNA', 'DS_TIPO_VOTAVEL', 'NR_VOTAVEL', 'QT_VOTOS',
        'QT_ELEI_BIOM_SEM_HABILITACAO', 'NR_TURNO', 'DS_SECOES_AGREGADAS']
for c in need:
    assert c in ix, c
d = {}
incons = 0
nlin = 0
rd = csv.reader(io.TextIOWrapper(p2.stdout, encoding='latin1'), delimiter=';')
for r in rd:
    if len(r) != len(cols):
        incons += 1
        continue
    if r[ix['DS_CARGO_PERGUNTA']] != 'Presidente' or r[ix['CD_CARGO_PERGUNTA']] != '1':
        continue
    nlin += 1
    k = (r[ix['SG_UF']], r[ix['CD_MUNICIPIO']], r[ix['NR_ZONA']], r[ix['NR_SECAO']])
    sec = (r[ix['NR_LOCAL_VOTACAO']], r[ix['QT_APTOS']], r[ix['QT_COMPARECIMENTO']], r[ix['DS_TIPO_URNA']],
           r[ix['QT_ELEI_BIOM_SEM_HABILITACAO']], r[ix['NR_TURNO']], r[ix['DS_SECOES_AGREGADAS']])
    e = d.get(k)
    if e is None:
        e = d[k] = {'sec': sec, 'L': 0, 'R': 0, 'O': 0, 'B': 0, 'N': 0, 'rows': 0, 'diff': 0}
    elif e['sec'] != sec:
        e['diff'] += 1
    e['rows'] += 1
    tv = r[ix['DS_TIPO_VOTAVEL']]; nv = r[ix['NR_VOTAVEL']]; q = int(r[ix['QT_VOTOS']])
    if tv == 'Nominal':
        if nv == '13': e['L'] += q
        elif nv == '22': e['R'] += q
        else: e['O'] += q
    elif tv == 'Branco': e['B'] += q
    elif tv == 'Nulo': e['N'] += q
    else:
        e['O'] += q  # legenda ou outro tipo (não deve haver para Presidente)
        e['diff'] += 1000
p2.wait()
with open(out, 'w') as f:
    f.write('uf\tmun\tzona\tsecao\tloc\tapt\tcomp\turna\tNH\tturno\tagreg\tL\tR\tO\tB\tN\trows\tdiff\n')
    for k, e in d.items():
        s = e['sec']
        f.write('\t'.join(list(k) + list(s) + [str(e[x]) for x in ('L', 'R', 'O', 'B', 'N', 'rows', 'diff')]) + '\n')
sys.stderr.write(f"{zp.split('/')[-1]} secoes {len(d)} linhas {nlin} incons {incons}\n")
