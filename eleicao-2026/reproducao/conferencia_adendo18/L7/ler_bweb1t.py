"""Leitura própria do bweb do 1º turno: por seção, urna e data de carga (linhas de Presidente)."""
import glob, gzip, json, os, sys, zipfile
from multiprocessing import Pool

ZDIR, SAIDA = sys.argv[1], sys.argv[2]
MARCA = b';"Presidente";'


def ler(zp):
    z = zipfile.ZipFile(zp)
    nome = [n for n in z.namelist() if n.lower().endswith('.csv')][0]
    out = {}
    with z.open(nome) as fh:
        cab = [c.strip().strip('"') for c in fh.readline().decode('latin1').strip().split(';')]
        ix = {c: i for i, c in enumerate(cab)}
        iu, im, iz, isec = ix['SG_UF'], ix['CD_MUNICIPIO'], ix['NR_ZONA'], ix['NR_SECAO']
        iurna, icarga, icargo = ix['NR_URNA_EFETIVADA'], ix['DT_CARGA_URNA_EFETIVADA'], ix['CD_CARGO_PERGUNTA']
        for linha in fh:
            if MARCA not in linha:
                continue
            p = linha.decode('latin1').rstrip('\r\n').split(';')
            if p[icargo] != '1':
                continue
            k = f"{p[iu].strip(chr(34))}|{int(p[im])}|{int(p[iz])}|{int(p[isec])}"
            if k not in out:
                out[k] = (p[iurna].strip('"'), p[icarga].strip('"'))
    return os.path.basename(zp), out


if __name__ == '__main__':
    zips = sorted(glob.glob(os.path.join(ZDIR, '*.zip')))
    with Pool(4) as P:
        partes = P.map(ler, zips)
    tudo = {}
    for nome, d in partes:
        print(nome, len(d), flush=True)
        tudo.update(d)
    with gzip.open(SAIDA, 'wt') as f:
        json.dump(tudo, f)
    print('total', len(tudo))
