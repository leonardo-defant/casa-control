"""NH (QT_ELEI_BIOM_SEM_HABILITACAO) por seção, lido das linhas de Presidente do bweb (stdin = CSV latin1 já filtrado ou completo).
Uso: unzip -p zip | python3 -I c_nh.py <turno> >> saida.tsv"""
import sys, csv, io
t = sys.argv[1]
r = csv.reader(io.TextIOWrapper(sys.stdin.buffer, encoding='latin1'), delimiter=';')
h = None; vistos = set(); w = sys.stdout
for row in r:
    if row[0] == 'DT_GERACAO':
        h = {c: j for j, c in enumerate(row)}; continue
    if row[h['DS_CARGO_PERGUNTA']] != 'Presidente':
        continue
    k = f"{row[h['SG_UF']]}|{int(row[h['CD_MUNICIPIO']])}|{int(row[h['NR_ZONA']])}|{int(row[h['NR_SECAO']])}"
    if k in vistos:
        continue
    vistos.add(k)
    w.write('\t'.join((t, k, row[h['QT_ELEI_BIOM_SEM_HABILITACAO']], row[h['QT_COMPARECIMENTO']], row[h['DS_TIPO_URNA']], row[h['QT_APTOS']])) + '\n')
