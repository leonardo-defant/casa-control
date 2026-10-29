"""Extrai dos zips bweb do 2º turno de 2026 os campos de horário completos (com data), por seção (linha de Presidente).

Uso: python3 -I extrair_horas_2t.py <pasta_zips> <saida.json.gz>
Saída: {"UF|mun|zona|secao": [DT_ABERTURA, DT_ENCERRAMENTO, DT_EMISSAO_BU, DT_BU_RECEBIDO, NH, DS_TIPO_URNA, NM_MUNICIPIO, agregadas]}
"""
import csv, glob, gzip, json, os, sys, zipfile
from multiprocessing import Pool


def ler(zpath):
    out = {}; incons = 0
    z = zipfile.ZipFile(zpath)
    nome = [n for n in z.namelist() if n.lower().endswith('.csv')][0]
    with z.open(nome) as fh:
        cab = next(csv.reader([fh.readline().decode('latin1')], delimiter=';'))
        ix = {c.strip().replace('SG_ UF', 'SG_UF'): i for i, c in enumerate(cab)}
        for linha in fh:
            if b';1;"Presidente";' not in linha:
                continue
            r = next(csv.reader([linha.decode('latin1')], delimiter=';'))
            if r[ix['CD_CARGO_PERGUNTA']] != '1':
                continue
            k = f"{r[ix['SG_UF']]}|{int(r[ix['CD_MUNICIPIO']])}|{int(r[ix['NR_ZONA']])}|{int(r[ix['NR_SECAO']])}"
            try:
                nh = int(r[ix['QT_ELEI_BIOM_SEM_HABILITACAO']])
            except ValueError:
                nh = None
            agr = r[ix['DS_SECOES_AGREGADAS']]
            agr = '' if agr in ('', '#NULO#') else agr
            reg = [r[ix['DT_ABERTURA']], r[ix['DT_ENCERRAMENTO']], r[ix['DT_EMISSAO_BU']], r[ix['DT_BU_RECEBIDO']],
                   nh, r[ix['DS_TIPO_URNA']], r[ix['NM_MUNICIPIO']], agr]
            if k in out and out[k] != reg:
                incons += 1
            out.setdefault(k, reg)
    return os.path.basename(zpath), out, incons


if __name__ == '__main__':
    pasta, saida = sys.argv[1], sys.argv[2]
    zips = sorted(glob.glob(os.path.join(pasta, '*.zip')), key=lambda p: -os.path.getsize(p))
    tudo = {}; inc = 0
    with Pool(2) as p:
        for nome, out, i in p.imap_unordered(ler, zips):
            print('ok', nome, len(out), i, flush=True)
            tudo.update(out); inc += i
    with gzip.open(saida, 'wt') as f:
        json.dump(tudo, f, separators=(',', ':'))
    print('secoes', len(tudo), 'inconsistentes', inc)
