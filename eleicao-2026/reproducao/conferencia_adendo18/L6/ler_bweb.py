"""Conferência L6: leitura independente do bweb (presidente nos dois turnos, governador no 1º turno), direto dos zips.

Não usa a base por seção nem o cache do outro agente. Saída: um json.gz por turno com, por seção,
votos de Lula (13), Flávio (22), outros nominais, brancos e nulos de presidente; no 1º turno também os votos
nominais de governador por número de candidato.
Uso: python3 -I ler_bweb.py <dir_zips> <turno 1|2> <saida.json.gz>
"""
import collections, glob, gzip, json, os, sys, zipfile
from multiprocessing import Pool

PRES = b';1;"Presidente";'
GOV = b';3;"Governador";'


def campos(linha):
    s = linha.decode('latin1').rstrip('\r\n')
    return [c[1:-1] if len(c) >= 2 and c[0] == '"' and c[-1] == '"' else c for c in s.split(';')]


def ler(zpath):
    z = zipfile.ZipFile(zpath)
    nome = [n for n in z.namelist() if n.lower().endswith('.csv')][0]
    pres = collections.defaultdict(lambda: [0, 0, 0, 0, 0])  # L, R, outros nominais, branco, nulo
    gov = collections.defaultdict(collections.Counter)
    gov_nomes = {}
    with z.open(nome) as fh:
        cab = campos(fh.readline())
        ix = {c: i for i, c in enumerate(cab)}
        iuf, imun, izn, isc = ix['SG_UF'], ix['CD_MUNICIPIO'], ix['NR_ZONA'], ix['NR_SECAO']
        icg, itp, inr, iq, inm, ipt = ix['CD_CARGO_PERGUNTA'], ix['CD_TIPO_VOTAVEL'], ix['NR_VOTAVEL'], ix['QT_VOTOS'], ix['NM_VOTAVEL'], ix['SG_PARTIDO']
        for linha in fh:
            ehp = PRES in linha
            ehg = (not ehp) and GOV in linha
            if not (ehp or ehg):
                continue
            r = campos(linha)
            k = f'{r[iuf]}|{int(r[imun])}|{int(r[izn])}|{int(r[isc])}'
            q = int(r[iq]); tp = r[itp]
            if ehp and r[icg] == '1':
                p = pres[k]
                if tp == '1':
                    if r[inr] == '13':
                        p[0] += q
                    elif r[inr] == '22':
                        p[1] += q
                    else:
                        p[2] += q
                elif tp == '2':
                    p[3] += q
                else:
                    p[4] += q
            elif ehg and r[icg] == '3' and tp == '1':
                gov[k][r[inr]] += q
                gov_nomes[r[inr]] = f'{r[inm]} ({r[ipt]})'
    uf = os.path.basename(zpath).split('_')[2]
    return uf, dict(pres), {k: dict(v) for k, v in gov.items()}, gov_nomes


def main():
    zdir, turno, saida = sys.argv[1:4]
    zs = sorted(glob.glob(os.path.join(zdir, f'bweb_{turno}t_*.zip')), key=lambda p: -os.path.getsize(p))
    out = {}
    with Pool(4) as pool:
        for uf, pres, gov, nomes in pool.imap_unordered(ler, zs):
            out[uf] = {'pres': pres, 'gov': gov, 'gov_nomes': nomes}
            L = sum(v[0] for v in pres.values()); R = sum(v[1] for v in pres.values())
            print(uf, len(pres), 'secoes', L, R, flush=True)
    with gzip.open(saida, 'wt') as f:
        json.dump(out, f)


if __name__ == '__main__':
    main()
