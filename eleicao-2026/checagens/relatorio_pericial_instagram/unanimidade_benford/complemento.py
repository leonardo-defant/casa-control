"""Complementos: (1) Benford em votos sintéticos com a fatia nacional (nenhuma informação de voto local) e distância
entre dígitos reais e sintéticos; (2) biometria (NH) por local rural/indígena e composição das seções com NH mais alto.
Uso: python3 -I complemento.py <pasta_npz> <locais2026.json.gz> <nh_secoes_2026.json.gz> <saida.json>"""
import gzip, json, os, sys
import numpy as np

pasta, locp, nhp, saida = sys.argv[1:5]
d1 = np.log10(1 + 1 / np.arange(1, 10))
R = {}
rng = np.random.default_rng(7)


def p1(x):
    a = x[x > 0]; f = a // 10 ** np.floor(np.log10(a)).astype(np.int64)
    o = np.bincount(f, minlength=10)[1:10]; return o / o.sum()


def p2(x):
    b = x[x >= 10]; s = (b // 10 ** (np.floor(np.log10(b)).astype(np.int64) - 1)) % 10
    o = np.bincount(s, minlength=10); return o / o.sum(), float(s.mean())


for rot, nome in (('2026_t2', '2026_2T'), ('2026_t1', '2026_1T'), ('2022_t2', '2022_2T')):
    z = np.load(os.path.join(pasta, rot + '.npz')); L, Rr, O = z['L'], z['R'], z['O']; V = L + Rr + O; ok = V > 0
    pL = L.sum() / V.sum(); pR = Rr.sum() / V.sum()
    sL = rng.binomial(V, pL); sR = rng.binomial(V - sL, pR / (1 - pL))
    out = {}
    for c, real, sint in (('L', L, sL), ('R', Rr, sR)):
        a, b = p1(real[ok]), p1(sint[ok])
        (a2, m2), (b2, n2) = p2(real[ok]), p2(sint[ok])
        out[c] = {'1BL_real_pct': [round(100 * v, 2) for v in a], '1BL_sint_nacional_pct': [round(100 * v, 2) for v in b],
                  'MAD_real_vs_Benford': round(float(np.abs(a - d1).mean()), 4), 'MAD_sint_nacional_vs_Benford': round(float(np.abs(b - d1).mean()), 4),
                  'MAD_real_vs_sint_nacional': round(float(np.abs(a - b).mean()), 4),
                  '2BL_media_real': round(m2, 4), '2BL_media_sint_nacional': round(n2, 4)}
    R[f'sintetico_nacional_{nome}'] = out

# MAD real x sintético local (lido do resultado_benford.json)
B = json.load(open(os.path.join(pasta, 'resultado_benford.json')))
dist = {}
for nome, cands in (('2026_2T', ('Lula', 'Flávio')), ('2026_1T', ('Lula', 'Flávio')), ('2022_2T', ('Lula', 'Bolsonaro')), ('2018_2T', ('Haddad', 'Bolsonaro'))):
    for c in cands:
        for nivel in ('local', 'municipio'):
            for teste in ('1BL', '2BL'):
                a = np.array(B[nome][c][teste]['obs_pct']) / 100; b = np.array(B[nome][f'sintetico_{nivel}_{c}'][teste]['obs_pct']) / 100
                dist[f'{nome}|{c}|{nivel}|{teste}'] = {'MAD_real_vs_sintetico': round(float(np.abs(a - b).mean()), 4),
                                                       'MAD_real_vs_Benford': B[nome][c][teste]['MAD']}
R['distancia_real_sintetico'] = dist

# biometria por rural/indígena (2026 2T e 1T, Brasil)
with gzip.open(locp, 'rt') as f:
    LOC = json.load(f)
with gzip.open(nhp, 'rt') as f:
    NHc = json.load(f)
for rot, t in (('2026_t2', '2'), ('2026_t1', '1')):
    z = np.load(os.path.join(pasta, rot + '.npz')); ch = z['chave']; comp = z['comp']; L, Rr, O = z['L'], z['R'], z['O']
    Lc = LOC[t]
    ind = np.array([Lc[k][6] if k in Lc else -1 for k in ch]); rur = np.array([Lc[k][7] if k in Lc else -1 for k in ch])
    nh = np.array([NHc[t][k][3] if k in NHc[t] and NHc[t][k][3] is not None else 0 for k in ch])
    br = ind >= 0
    out = {}
    for nomeg, m in (('indigena', br & (ind == 1)), ('rural_texto_nao_indigena', br & (rur == 1) & (ind == 0)), ('demais', br & (rur == 0) & (ind == 0)), ('brasil', br)):
        out[nomeg] = {'secoes': int(m.sum()), 'NH_pct_comp': round(100 * nh[m].sum() / comp[m].sum(), 2)}
    # 1% das seções com maior taxa NH (comp >= 50)
    taxa = nh / np.maximum(comp, 1); ok = br & (comp >= 50)
    corte = np.percentile(taxa[ok], 99); top = ok & (taxa >= corte)
    V2 = L + Rr + O; sL = L / np.maximum(V2, 1); sR = Rr / np.maximum(V2, 1)
    out['top1pct_NH'] = {'corte_taxa_pct': round(100 * float(corte), 2), 'secoes': int(top.sum()),
                         'pct_Lula_>=90_no_top': round(100 * float((sL[top] >= .9).mean()), 2), 'pct_Lula_>=90_geral': round(100 * float((sL[ok] >= .9).mean()), 2),
                         'pct_Flavio_>=90_no_top': round(100 * float((sR[top] >= .9).mean()), 2), 'pct_Flavio_>=90_geral': round(100 * float((sR[ok] >= .9).mean()), 2),
                         'fatia_Lula_ponderada_no_top': round(float(L[top].sum() / V2[top].sum()), 4), 'fatia_Lula_ponderada_geral': round(float(L[ok].sum() / V2[ok].sum()), 4),
                         'por_UF_top10': dict(sorted({u: int(n) for u, n in zip(*np.unique(np.array([k.split('|')[0] for k in ch[top]]), return_counts=True))}.items(), key=lambda x: -x[1])[:10])}
    R[f'NH_por_tipo_{rot}'] = out
with open(saida, 'w') as f:
    json.dump(R, f, ensure_ascii=False, indent=1)
print(json.dumps(R, ensure_ascii=False)[:6000])
