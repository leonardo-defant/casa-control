"""Conferência independente do L2: leitura própria do bweb (todas as linhas, todos os cargos).
Por seção (UF|mun|zona|seção): conjunto de (urna, carga1, carga2, flash, dt_carga, abertura, encerramento, emissao, junta,
tipo_urna, local) em todas as linhas; votos de presidente por NR_VOTAVEL (13, 22, branco 95, nulo 96, resto), aptos e
comparecimento da linha de presidente.
Uso: python3 -I ler_bweb.py <pasta_zips> <saida.pkl.gz>
"""
import csv, glob, gzip, os, pickle, sys, time, zipfile
from multiprocessing import Pool


def ler(zpath):
    z = zipfile.ZipFile(zpath)
    nome = [n for n in z.namelist() if n.lower().endswith('.csv')][0]
    sec = {}
    linhas = 0; ruins = 0; cargos = {}
    with z.open(nome) as fh:
        cab = [c.strip().strip('"') for c in fh.readline().decode('latin1').strip().split(';')]
        assert len(cab) == 45, len(cab)
        I = {c: i for i, c in enumerate(cab)}
        for raw in fh:
            linhas += 1
            p = raw.rstrip(b'\r\n').split(b';')
            if len(p) != 45:
                ruins += 1
                p = [x.encode('latin1') for x in next(csv.reader([raw.decode('latin1').rstrip('\r\n')], delimiter=';'))]
                p = [b'"' + x + b'"' for x in p]  # recoloca aspas para o strip abaixo
                if len(p) != 45:
                    raise RuntimeError(f'linha com {len(p)} campos em {zpath}')
            q = lambda i: p[i].strip(b'"').decode('latin1')
            k = f"{q(10)}|{int(q(11))}|{int(q(13))}|{int(q(14))}"
            s = sec.get(k)
            if s is None:
                s = sec[k] = {'campos': set(), 'L': 0, 'R': 0, 'B': 0, 'N': 0, 'O': 0, 'apt': set(), 'comp': set(),
                              'pres': 0, 'cargos': set()}
            s['campos'].add((q(32), q(33), q(34), q(35), q(36), q(39), q(40), q(42), q(43), q(25), q(15)))
            cg = q(16)
            s['cargos'].add(cg)
            cargos[cg] = cargos.get(cg, 0) + 1
            if cg == '1':
                s['pres'] += 1
                nv = q(29); v = int(q(31))
                if nv == '13': s['L'] += v
                elif nv == '22': s['R'] += v
                elif nv == '95': s['B'] += v
                elif nv == '96': s['N'] += v
                else: s['O'] += v
                s['apt'].add(int(q(22))); s['comp'].add(int(q(23)))
    return os.path.basename(zpath), sec, linhas, ruins, cargos


def main():
    pasta, saida = sys.argv[1:3]
    zs = sorted(glob.glob(os.path.join(pasta, '*.zip')), key=lambda p: -os.path.getsize(p))
    t0 = time.time(); tot = {}; info = {}
    with Pool(4) as pool:
        for nome, sec, linhas, ruins, cargos in pool.imap_unordered(ler, zs):
            dup = set(sec) & set(tot)
            assert not dup, (nome, list(dup)[:5])
            tot.update(sec); info[nome] = {'secoes': len(sec), 'linhas': linhas, 'linhas_fora_de_45_campos': ruins, 'cargos': cargos}
            print(f'{time.time() - t0:7.0f}s {nome}: {len(sec)} seções, {linhas} linhas, {ruins} fora de 45', flush=True)
    with gzip.open(saida, 'wb') as f:
        pickle.dump({'secoes': tot, 'info': info}, f, protocol=4)
    print('fim', len(tot), time.time() - t0, flush=True)


if __name__ == '__main__':
    main()
