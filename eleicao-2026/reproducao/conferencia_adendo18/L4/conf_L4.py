"""Conferência independente do L4 (Adendo 18). Código próprio, sem lib.py nem analisar_L4.py.

Lê as linhas de Presidente extraídas direto dos zips do bweb (extrair.sh), monta a seção (UF|mun|zona|seção), o local do
2º turno (UF|mun|zona|NR_LOCAL_VOTACAO do 2º turno) e roda a regressão do T8 com grupos para Lula e para Flávio
separadamente: y = c2 - c1; X = Cury, Renan, Caiado, Zema, demais outros (1º turno), queda do branco+nulo (1º - 2º),
variação do comparecimento (2º - 1º), adversário no 1º turno, próprio no 1º turno; efeito fixo de local (within por
pandas groupby), erro CR1 agrupado por local. s = b_L / (b_L + b_F).

Uso: python3 -I conf_L4.py <dir_extr> <saida.json>
"""
import gzip, json, sys
import numpy as np
import pandas as pd

GRUPOS = {'Cury': 70, 'Renan': 14, 'Caiado': 55, 'Zema': 30}
CASA = {'GO': 'Caiado', 'MG': 'Zema', 'SP': 'Cury'}
COLS = ['uf', 'mun', 'zona', 'secao', 'local', 'aptos', 'comp', 'tipo_urna', 'tipo_votavel', 'nr', 'votos', 'nr_urna', 'agreg']


def ler(path):
    df = pd.read_csv(path, sep=';', header=None, names=COLS, dtype={'uf': str, 'agreg': str}, compression='gzip')
    df['k'] = df['uf'] + '|' + df['mun'].astype(str) + '|' + df['zona'].astype(str) + '|' + df['secao'].astype(str)
    return df


def por_secao(df, turno):
    # votos por número
    v = df.pivot_table(index='k', columns='nr', values='votos', aggfunc='sum', fill_value=0)
    # comparecimento: uma vez por boletim (k, nr_urna, tipo_urna); soma entre boletins distintos da mesma seção
    bu = df.drop_duplicates(['k', 'nr_urna', 'tipo_urna'])
    nbu = bu.groupby('k').size()
    comp = bu.groupby('k')['comp'].sum()
    loc = df.groupby('k')['local'].first()
    out = pd.DataFrame(index=v.index)
    out['L'] = v.get(13, 0); out['R'] = v.get(22, 0)
    out['B'] = v.get(95, 0); out['N'] = v.get(96, 0)
    outros = [c for c in v.columns if c not in (13, 22, 95, 96)]
    out['O'] = v[outros].sum(1)
    if turno == '1':
        for g, n in GRUPOS.items():
            out[g] = v.get(n, 0)
    out['comp'] = comp
    out['nbu'] = nbu
    out['local'] = loc
    out.columns = [c + turno if c not in GRUPOS else c for c in out.columns]
    return out


def within(D, g):
    return D - D.groupby(g).transform('mean')


def reg(y, X, g, nomes):
    d = pd.DataFrame(np.column_stack([y, X]), columns=['y'] + nomes)
    cnt = pd.Series(g).map(pd.Series(g).value_counts())
    ok = (cnt >= 2).values
    d = d[ok].reset_index(drop=True); gg = pd.Series(g[ok])
    Z = within(d, gg.values)
    yd = Z['y'].values; Xd = Z[nomes].values
    b, *_ = np.linalg.lstsq(Xd, yd, rcond=None)
    e = yd - Xd @ b
    codes = pd.factorize(gg)[0]; G = codes.max() + 1
    S = np.zeros((G, Xd.shape[1]))
    for j in range(Xd.shape[1]):
        S[:, j] = np.bincount(codes, weights=Xd[:, j] * e, minlength=G)
    inv = np.linalg.inv(Xd.T @ Xd); N, k = Xd.shape
    V = G / (G - 1) * (N - 1) / (N - k) * inv @ (S.T @ S) @ inv
    return dict(zip(nomes, b)), dict(zip(nomes, np.sqrt(np.diag(V)))), int(N), int(G), Xd, e, codes


def main():
    dirx, saida = sys.argv[1], sys.argv[2]
    res = {}
    for uf, casa in CASA.items():
        a = por_secao(ler(f'{dirx}/p1_{uf}.csv.gz'), '1')
        b = por_secao(ler(f'{dirx}/p2_{uf}.csv.gz'), '2')
        m = a.join(b, how='inner')
        info = {'secoes_1t': len(a), 'secoes_2t': len(b), 'secoes_dois_turnos': len(m),
                'bu_multiplos_1t': int((a['nbu1'] > 1).sum()), 'bu_multiplos_2t': int((b['nbu2'] > 1).sum())}
        # identidade comp = L + R + O + B + N
        for t in '12':
            info[f'identidade_max_{t}'] = float((m['comp' + t] - m['L' + t] - m['R' + t] - m['O' + t] - m['B' + t] - m['N' + t]).abs().max())
        dem = m['O1'] - m[list(GRUPOS)].sum(1)
        qbn = (m['B1'] + m['N1']) - (m['B2'] + m['N2'])
        dcomp = m['comp2'] - m['comp1']
        lockey = (m.index.str.rsplit('|', n=1).str[0] + '|' + m['local2'].astype(str)).values
        nomes = list(GRUPOS) + ['dem', 'qbn', 'dcomp', 'adv', 'prop']
        base = np.column_stack([m[list(GRUPOS)].values, dem, qbn, dcomp])
        XL = np.column_stack([base, m['R1'], m['L1']]); yL = (m['L2'] - m['L1']).values
        XF = np.column_stack([base, m['L1'], m['R1']]); yF = (m['R2'] - m['R1']).values
        bL, eL, N, G, XdL, resL, codes = reg(yL, XL.astype(float), lockey, nomes)
        bF, eF, _, _, XdF, resF, _ = reg(yF, XF.astype(float), lockey, nomes)
        grupos = {}
        for g in GRUPOS:
            t = bL[g] + bF[g]
            grupos[g] = {'b_L': bL[g], 'ep_b_L': eL[g], 'b_F': bF[g], 'ep_b_F': eF[g], 'soma': t, 's': bL[g] / t}
        info.update({'linhas': N, 'locais': G, 'grupos': grupos,
                     'outros_L': {k: bL[k] for k in nomes[4:]}, 'outros_F': {k: bF[k] for k in nomes[4:]},
                     'casa': casa, 'votos_casa_1t': float(m[casa].sum()),
                     'lula_fatia_1t': float(m['L1'].sum() / (m['L1'].sum() + m['R1'].sum())),
                     'lula_fatia_2t': float(m['L2'].sum() / (m['L2'].sum() + m['R2'].sum())),
                     'max_abs_resL_mais_resF': float(np.abs(resL + resF).max())})
        # robustez independente: FE de município e de zona
        for nome, chave in (('fe_zona', m.index.str.rsplit('|', n=1).str[0].values),
                            ('fe_mun', m.index.str.rsplit('|', n=2).str[0].values)):
            bl, el, *_ = reg(yL, XL.astype(float), chave, nomes)
            bf, ef, *_ = reg(yF, XF.astype(float), chave, nomes)
            info[nome] = {'s': bl[casa] / (bl[casa] + bf[casa]), 'ep': el[casa]}
        # sem efeito fixo nenhum (MQO puro com constante) para ver o quanto o FE pesa
        Xc = np.column_stack([np.ones(len(yL)), XL]); bb = np.linalg.lstsq(Xc, yL, rcond=None)[0]
        info['sem_fe_s'] = float(bb[1 + list(GRUPOS).index(casa)])
        res[uf] = info
        print(uf, json.dumps({g: round(x['s'], 4) for g, x in grupos.items()}), 'ep casa', round(grupos[casa]['ep_b_L'], 4),
              'zona', round(info['fe_zona']['s'], 4), 'mun', round(info['fe_mun']['s'], 4), 'semFE', round(info['sem_fe_s'], 4), flush=True)
        # salva base por seção para outras conferências
        m.assign(lockey=lockey).to_csv(f'{dirx}/base_{uf}.csv.gz', compression='gzip')
    json.dump(res, open(saida, 'w'), ensure_ascii=False, indent=1, default=float)


if __name__ == '__main__':
    main()
