"""Conferência independente do L2 (Adendo 18). Usa só a leitura própria do bweb (ler_bweb.py), sem a base nem o cache do
outro agente, e um estimador within próprio (forma fechada, pandas), sem lib.fe_ols.
Uso: python3 -I conferir_L2.py <bweb1t.pkl.gz> <bweb2t.pkl.gz> <saida.json>
"""
import collections, datetime, gzip, json, math, pickle, sys
import numpy as np
import pandas as pd

b1p, b2p, saida = sys.argv[1:4]
B1 = pickle.load(gzip.open(b1p, 'rb'))['secoes']
B2 = pickle.load(gzip.open(b2p, 'rb'))['secoes']
OUT = {}


def um(s):
    assert len(s['campos']) == 1, s['campos']
    return next(iter(s['campos']))


OUT['secoes_bweb'] = {'1T': len(B1), '2T': len(B2),
                      'multi_campos_1T': sum(len(s['campos']) > 1 for s in B1.values()),
                      'multi_campos_2T': sum(len(s['campos']) > 1 for s in B2.values()),
                      'sem_presidente_1T': [k for k, s in B1.items() if s['pres'] == 0],
                      'sem_presidente_2T': [k for k, s in B2.items() if s['pres'] == 0],
                      'so_1T': [k for k in B1 if k not in B2], 'so_2T': [k for k in B2 if k not in B1]}
print(json.dumps({k: (v if not isinstance(v, list) else v[:10]) for k, v in OUT['secoes_bweb'].items()}), flush=True)

rec = []
for k, s2 in B2.items():
    s1 = B1.get(k)
    if s1 is None or s1['pres'] == 0 or s2['pres'] == 0:
        continue
    f1, f2 = um(s1), um(s2)
    uf, mun, zona, sec = k.split('|')
    rec.append(dict(k=k, uf=uf, mun=f'{uf}|{mun}', zona=f'{uf}|{mun}|{zona}', loc=f'{uf}|{mun}|{zona}|{int(f2[10])}',
                    loc1=f'{uf}|{mun}|{zona}|{int(f1[10])}', u1=f1[0], u2=f2[0], L1=s1['L'], R1=s1['R'], L2=s2['L'], R2=s2['R'],
                    apt1=next(iter(s1['apt'])), apt2=next(iter(s2['apt'])), c1=next(iter(s1['comp'])), c2=next(iter(s2['comp'])),
                    BN1=s1['B'] + s1['N'], BN2=s2['B'] + s2['N'], dt2=f2[4], dt1=f1[4], cod1=(f1[1], f1[2], f1[3]),
                    cod2=(f2[1], f2[2], f2[3]), ab1=f1[5], ab2=f2[5], em1=f1[7], em2=f2[7], j2=f2[8], j1=f1[8]))
df = pd.DataFrame(rec)
OUT['universo_dois_turnos_com_presidente'] = len(df)
df = df[(df.L1 + df.R1 > 0) & (df.L2 + df.R2 > 0)].reset_index(drop=True)
OUT['universo_com_finalista_nos_dois'] = len(df)
OUT['local_mudou'] = int((df['loc'] != df['loc1']).sum())
df['fat1'] = 100 * df.L1 / (df.L1 + df.R1)
df['fat2'] = 100 * df.L2 / (df.L2 + df.R2)
df['y'] = df.fat2 - df.fat1
df['w2'] = df.L2 + df.R2
df['w1'] = df.L1 + df.R1
df['dcomp'] = 100 * (df.c2 / df.apt2 - df.c1 / df.apt1)
df['U'] = (df.u1 != df.u2).astype(float)


def tsec(s):
    return (datetime.datetime.strptime(s, '%Y-%m-%d %H:%M:%S') - datetime.datetime(2026, 1, 1)).total_seconds()


# grupo C: percentis 1 e 99 por UF sobre todas as seções do bweb do 2º turno (campo DT_CARGA_URNA_EFETIVADA)
todas = [(k.split('|')[0], k, tsec(um(s)[4])) for k, s in B2.items()]
T = pd.DataFrame(todas, columns=['uf', 'k', 't'])
T['dia'] = np.floor(T.t / 86400)
lims = {}
for metodo in ('linear', 'lower', 'higher', 'nearest', 'midpoint'):
    for campo in ('t', 'dia'):
        p = T.groupby('uf')[campo].apply(lambda x: np.percentile(x.values, [1, 99], method=metodo))
        lo = T.uf.map(lambda u: p[u][0]); hi = T.uf.map(lambda u: p[u][1])
        fora = (T[campo] < lo) | (T[campo] > hi)
        lado = np.where(T[campo] < lo, 'cedo', np.where(T[campo] > hi, 'tarde', ''))
        nome = f'C_{campo}_{metodo}'
        lims[nome] = dict(zip(T.k, lado))
        OUT.setdefault('tamanho_C_todas_secoes_bweb2T', {})[nome] = int(fora.sum())
for nome, mp in lims.items():
    df[nome] = df.k.map(lambda k: mp[k] != '').astype(float)
df['C'] = df['C_t_linear']
df['C_cedo'] = df.k.map(lambda k: lims['C_t_linear'][k] == 'cedo').astype(float)
df['C_tarde'] = df.k.map(lambda k: lims['C_t_linear'][k] == 'tarde').astype(float)
# percentis só sobre o universo (leitura alternativa)
p = df.assign(t=df.dt2.map(tsec)).groupby('uf')['t'].apply(lambda x: np.percentile(x.values, [1, 99]))
tt = df.dt2.map(tsec)
df['C_universo'] = ((tt < df.uf.map(lambda u: p[u][0])) | (tt > df.uf.map(lambda u: p[u][1]))).astype(float)


def fe1(d, D, y='y', w='w2', g='loc', extra=None):
    """y = b D + efeito fixo de g, MQP; forma fechada; erro agrupado por g (CR1 com K=1: G/(G-1))."""
    x = d[[y, D, g]].copy()
    x['w'] = 1.0 if w is None else d[w].astype(float)
    x = x[np.isfinite(x[y])]
    n = x.groupby(g)[y].transform('size')
    x = x[n >= 2]
    sw = x.groupby(g)['w'].transform('sum')
    xb = (x.w * x[D]).groupby(x[g]).transform('sum') / sw
    yb = (x.w * x[y]).groupby(x[g]).transform('sum') / sw
    dt = x[D] - xb; yt = x[y] - yb
    sxx = (x.w * dt * dt).sum()
    b = (x.w * dt * yt).sum() / sxx
    e = yt - b * dt
    sg = (x.w * dt * e).groupby(x[g]).sum()
    G = x[g].nunique(); N = len(x)
    V0 = (sg ** 2).sum() / sxx ** 2
    se = math.sqrt(G / (G - 1) * V0)
    varia = (x.groupby(g)[D].transform('min') < x.groupby(g)[D].transform('max'))
    r = dict(coef=b, ep=se, z=b / se, n=N, locais=G, n_grupo=int(x[D].sum()), n_grupo_identifica=int(x[D][varia].sum()),
             locais_identificam=int(x[g][varia].nunique()))
    if extra:
        # cauda: resíduo within das seções do grupo e das outras, só nos locais onde o grupo varia
        rr = yt[varia]; dd = x[D][varia]; ww = x.w[varia]
        cauda = {}
        for lim in (2, 3, 5, 10):
            a = float(np.average(rr[dd == 1] > lim, weights=ww[dd == 1])); c = float(np.average(rr[dd == 0] > lim, weights=ww[dd == 0]))
            a2 = float(np.average(rr[dd == 1] < -lim, weights=ww[dd == 1])); c2 = float(np.average(rr[dd == 0] < -lim, weights=ww[dd == 0]))
            cauda[f'>+{lim}'] = {'grupo': a, 'outras': c}
            cauda[f'<-{lim}'] = {'grupo': a2, 'outras': c2}
        r['cauda_residuo_within_ponderada'] = cauda
        r['quantis_residuo_grupo'] = {q: float(np.quantile(rr[dd == 1], q)) for q in (0.01, 0.05, 0.25, 0.5, 0.75, 0.95, 0.99)}
        r['quantis_residuo_outras'] = {q: float(np.quantile(rr[dd == 0], q)) for q in (0.01, 0.05, 0.25, 0.5, 0.75, 0.95, 0.99)}
    return r


def leitura(r):
    if r['n_grupo'] >= 500 and r['coef'] >= 1.0 and r['coef'] / r['ep'] > 4:
        return 'SINAL'
    if abs(r['coef']) < 0.3 and r['ep'] <= 0.15:
        return 'SEM SINAL'
    return 'ENTRE OS DOIS'


princ = {}
for nome in ('U', 'C'):
    r = fe1(df, nome, extra=True)
    r['leitura'] = leitura(r)
    r['secoes_grupo_universo'] = int(df[nome].sum())
    r['votos_finalistas_2T_grupo'] = float(df.w2[df[nome] == 1].sum())
    r['lim_sup_95_votos_Lula'] = (r['coef'] + 1.96 * r['ep']) / 100 * r['votos_finalistas_2T_grupo']
    princ[nome] = r
    print(nome, {k: v for k, v in r.items() if 'cauda' not in k and 'quantis' not in k}, flush=True)
OUT['principal'] = princ
ls = [r['leitura'] for r in princ.values()]
OUT['veredito'] = 'INCOERÊNCIA' if 'SINAL' in ls else ('COERENTE' if all(l == 'SEM SINAL' for l in ls) else 'INCONCLUSIVO')
print('VEREDITO', OUT['veredito'], flush=True)

rob = {}
for nome in ('U', 'C'):
    rob[f'{nome}_placebo_fat1'] = fe1(df, nome, y='fat1')
    rob[f'{nome}_sem_peso'] = fe1(df, nome, w=None)
    rob[f'{nome}_peso_1T'] = fe1(df, nome, w='w1')
    rob[f'{nome}_fe_zona'] = fe1(df, nome, g='zona')
    rob[f'{nome}_fe_municipio'] = fe1(df, nome, g='mun')
    rob[f'{nome}_y_dcomp'] = fe1(df, nome, y='dcomp')
for nome in [c for c in df.columns if c.startswith('C_t_') or c.startswith('C_dia_')] + ['C_universo']:
    rob[nome] = fe1(df, nome)
rob['C_cedo_vs_dentro'] = fe1(df[df.C_tarde == 0], 'C_cedo')
rob['C_tarde_vs_dentro'] = fe1(df[df.C_cedo == 0], 'C_tarde')
df['UouC'] = ((df.U + df.C) > 0).astype(float)
rob['U_ou_C'] = fe1(df, 'UouC')
# carga do 2º turno depois do dia do 1º turno (recarga), qualquer seção
df['pos1t'] = (df.dt2.str[:10] > '2026-10-04').astype(float)
rob['carga2T_depois_do_1T'] = fe1(df, 'pos1t')
for k, r in rob.items():
    r['leitura_mesma_regua'] = leitura(r)
OUT['robustez'] = rob
for k, r in rob.items():
    print(k, f"{r['coef']:+.3f} ({r['ep']:.3f}) n_grupo {r['n_grupo']} id {r['n_grupo_identifica']} -> {r['leitura_mesma_regua']}", flush=True)

# escala
OUT['escala'] = {'L2': int(df.L2.sum()), 'R2': int(df.R2.sum()), 'margem_2T': int(df.L2.sum() - df.R2.sum()),
                 'L1': int(df.L1.sum()), 'R1': int(df.R1.sum()),
                 'virada_nacional_ponderada': float(np.average(df.y, weights=df.w2))}

# conferências de ordem lógica
co = {}
for rot, BB in (('1T', B1), ('2T', B2)):
    pa = []; pe = []; dup = collections.defaultdict(list); dupj = collections.defaultdict(list)
    for k, s in BB.items():
        f = um(s)
        if f[4] and f[5] and f[4] > f[5]:
            pa.append((k, f[4], f[5], f[3]))
        if f[4] and f[7] and f[4] > f[7]:
            pe.append((k, f[4], f[7]))
        dupj[f[0]].append(k)
        if f[8] == '-1':
            dup[f[0]].append(k)
    co[rot] = {'carga_depois_abertura': pa, 'carga_depois_emissao': pe,
               'urna_em_2_secoes_fora_junta': {u: v for u, v in dup.items() if len(v) > 1},
               'urna_em_2_secoes_com_junta': {u: v for u, v in dupj.items() if len(v) > 1 and u not in ('-1', '')}}
m = df[df.U == 0]
cd = m[m.cod1 != m.cod2]
co['mesma_urna'] = {'secoes': len(m), 'codigo_diferente': len(cd),
                    'codigo_diferente_carga2_ate_dia_1T': int((cd.dt2.str[:10] <= '2026-10-04').sum()),
                    'codigo_diferente_carga2_antes_emissao1': int((cd.dt2 <= cd.em1).sum()),
                    'mesmo_codigo_data_diferente': int(((m.cod1 == m.cod2) & (m.dt1 != m.dt2)).sum())}
urna1 = {}
for k, s in B1.items():
    urna1.setdefault(um(s)[0], []).append(k)
tr = df[df.U == 1]
reuso = []
for _, r in tr.iterrows():
    o = urna1.get(r.u2)
    if o:
        f1o = um(B1[o[0]])
        reuso.append({'k': r.k, 'secao_1T': o[0], 'carga_nova': (f1o[1], f1o[2], f1o[3]) != r.cod2, 'dt2': r.dt2, 'em1_origem': f1o[7],
                      'carga_depois_emissao1': r.dt2 > f1o[7]})
co['urna_do_2T_votou_no_1T_em_outra'] = {'n': len(reuso), 'sem_carga_nova_ou_antes_emissao': [x for x in reuso if not (x['carga_nova'] and x['carga_depois_emissao1'])]}
OUT['conferencias'] = {k: ({kk: (len(vv) if isinstance(vv, (list, dict)) else vv) for kk, vv in v.items()} if isinstance(v, dict) else v) for k, v in co.items()}
OUT['conferencias_lista'] = {'1T_carga_depois_abertura': co['1T']['carga_depois_abertura'], '2T_carga_depois_abertura': co['2T']['carga_depois_abertura'],
                             '1T_dup_com_junta': dict(list(co['1T']['urna_em_2_secoes_com_junta'].items())[:20]),
                             '2T_dup_com_junta': dict(list(co['2T']['urna_em_2_secoes_com_junta'].items())[:20])}
print(json.dumps(OUT['conferencias'], ensure_ascii=False), flush=True)
print(json.dumps(OUT['conferencias_lista'], ensure_ascii=False)[:3000], flush=True)
print(json.dumps(OUT['escala']), flush=True)
json.dump(OUT, open(saida, 'w'), ensure_ascii=False, indent=1, default=str)
print('ok')
