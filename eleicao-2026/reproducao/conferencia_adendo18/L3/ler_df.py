"""Conferência independente do L3: leitura própria das linhas de deputado federal do bweb do 1º turno.
Caminho diferente do script do outro agente: pandas read_csv com colunas nomeadas, filtro pelo código do cargo (sem
filtro de bytes), agregação por groupby. Também conta o partido pelo prefixo do NR_VOTAVEL, como segunda definição.
Uso: python3 -I ler_df.py <dir_zips> <saida.parquet-ou-csv.gz>
"""
import glob, os, sys, zipfile, time
from multiprocessing import Pool
import numpy as np
import pandas as pd

COLS = ['SG_UF', 'CD_MUNICIPIO', 'NR_ZONA', 'NR_SECAO', 'CD_CARGO_PERGUNTA', 'NR_PARTIDO', 'QT_COMPARECIMENTO',
        'CD_TIPO_VOTAVEL', 'NR_VOTAVEL', 'QT_VOTOS']


def um(zp):
    t0 = time.time()
    z = zipfile.ZipFile(zp)
    nome = [n for n in z.namelist() if n.lower().endswith('.csv')][0]
    partes = []
    n_tot = 0
    with z.open(nome) as fh:
        it = pd.read_csv(fh, sep=';', encoding='latin1', usecols=lambda c: c.strip() in COLS or c.strip() == 'SG_ UF',
                         dtype=str, chunksize=1_000_000, quotechar='"')
        for ch in it:
            ch.columns = [c.strip().replace('SG_ UF', 'SG_UF') for c in ch.columns]
            n_tot += len(ch)
            ch = ch[ch['CD_CARGO_PERGUNTA'].astype(int) == 6]
            if len(ch) == 0:
                continue
            q = ch['QT_VOTOS'].astype(np.int64)
            tv = ch['CD_TIPO_VOTAVEL'].astype(int)
            p = ch['NR_PARTIDO'].astype(str).str.strip()
            nv = ch['NR_VOTAVEL'].astype(str).str.strip()
            val = tv.isin([1, 4])
            df = pd.DataFrame({
                'k': ch['SG_UF'].str.strip() + '|' + ch['CD_MUNICIPIO'].astype(int).astype(str) + '|' +
                     ch['NR_ZONA'].astype(int).astype(str) + '|' + ch['NR_SECAO'].astype(int).astype(str),
                'comp_min': ch['QT_COMPARECIMENTO'].astype(np.int64),
                'comp_max': ch['QT_COMPARECIMENTO'].astype(np.int64),
                'validos': np.where(val, q, 0),
                'bra': np.where(tv == 2, q, 0),
                'nul': np.where(tv == 3, q, 0),
                'outro_tipo': np.where(~tv.isin([1, 2, 3, 4]), q, 0),
                'pl': np.where(val & (p == '22'), q, 0),
                'pt': np.where(val & (p == '13'), q, 0),
                'pl_prefixo': np.where(val & nv.str.startswith('22'), q, 0),
                'pt_prefixo': np.where(val & nv.str.startswith('13'), q, 0),
                'leg': np.where(tv == 4, q, 0),
                'pl_leg': np.where((tv == 4) & (p == '22'), q, 0),
            })
            g = df.groupby('k').agg(comp_min=('comp_min', 'min'), comp_max=('comp_max', 'max'), validos=('validos', 'sum'),
                                     bra=('bra', 'sum'), nul=('nul', 'sum'), outro_tipo=('outro_tipo', 'sum'), pl=('pl', 'sum'),
                                     pt=('pt', 'sum'), pl_prefixo=('pl_prefixo', 'sum'), pt_prefixo=('pt_prefixo', 'sum'),
                                     leg=('leg', 'sum'), pl_leg=('pl_leg', 'sum'))
            partes.append(g)
    if not partes:
        return os.path.basename(zp), None, n_tot
    g = pd.concat(partes)
    g = g.groupby(level=0).agg({'comp_min': 'min', 'comp_max': 'max', 'validos': 'sum', 'bra': 'sum', 'nul': 'sum',
                                'outro_tipo': 'sum', 'pl': 'sum', 'pt': 'sum', 'pl_prefixo': 'sum', 'pt_prefixo': 'sum',
                                'leg': 'sum', 'pl_leg': 'sum'})
    print(f'{os.path.basename(zp)}: {n_tot} linhas, {len(g)} seções, {time.time()-t0:.0f}s', file=sys.stderr, flush=True)
    return os.path.basename(zp), g, n_tot


if __name__ == '__main__':
    zips = sorted(glob.glob(os.path.join(sys.argv[1], '*.zip')), key=lambda p: -os.path.getsize(p))
    out = []
    with Pool(4) as pool:
        for nome, g, n in pool.imap_unordered(um, zips):
            if g is not None:
                out.append(g)
    G = pd.concat(out)
    assert not G.index.duplicated().any(), 'seção repetida entre zips'
    G.to_csv(sys.argv[2], compression='gzip')
    print('total', len(G), file=sys.stderr)
