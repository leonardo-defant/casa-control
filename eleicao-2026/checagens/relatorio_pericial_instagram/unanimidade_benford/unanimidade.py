"""Capítulo 4: seções quase unânimes. Reprodução e comparação com 2026 1T, 2022 2T e 2018 2T, geografia e biometria.
Entradas: npz gerados por extrair.py (cada base lida uma vez), cadastro de locais (locais.py), cache de NH do T21.
Uso: python3 -I unanimidade.py <pasta_npz> <locais2026.json.gz> <nh_secoes_2026.json.gz> <saida.json>"""
import gzip, json, sys, os, collections
import numpy as np

pasta, locp, nhp, saida = sys.argv[1:5]
with gzip.open(locp, 'rt') as f:
    LOC = json.load(f)
with gzip.open(nhp, 'rt') as f:
    NHc = json.load(f)
R = {}


def carregar(rot):
    z = np.load(os.path.join(pasta, rot + '.npz'))
    d = {c: z[c] for c in z.files}
    p = np.array([k.split('|') for k in d['chave']])
    d['uf'] = p[:, 0]; d['mun'] = (p[:, 0] + '|' + p[:, 1])
    return d


def conj(d, turno1=False, dois=False):
    """Fatia de cada candidato nos válidos (no 1T, com dois=True, fatia entre os dois finalistas)."""
    L, Rr, O = d['L'], d['R'], d['O']
    V = L + Rr if dois else L + Rr + O
    ok = V > 0
    sL = np.where(ok, L / np.maximum(V, 1), np.nan); sR = np.where(ok, Rr / np.maximum(V, 1), np.nan)
    return {'L100': ok & (L == V), 'R100': ok & (Rr == V), 'L90': sL >= 0.9, 'R90': sR >= 0.9,
            'L90e': sL > 0.9, 'R90e': sR > 0.9}, sL, sR, V


DS = {'2026_2T': ('2026_t2', 'Lula', 'Flávio'), '2026_1T': ('2026_t1', 'Lula', 'Flávio'),
      '2022_2T': ('2022_t2', 'Lula', 'Bolsonaro'), '2018_2T': ('2018_t2', 'Haddad', 'Bolsonaro'),
      '2022_1T': ('2022_t1', 'Lula', 'Bolsonaro'), '2018_1T': ('2018_t1', 'Haddad', 'Bolsonaro')}
dados = {}
contagem = {}
for nome, (rot, cl, cr) in DS.items():
    d = carregar(rot); dados[nome] = d
    for variante, dois in (('validos', False), ('dois_finalistas', True)):
        if nome.endswith('2T') and dois:
            continue
        c, sL, sR, V = conj(d, dois=dois)
        br = d['uf'] != 'ZZ'
        tot = {k: int(v.sum()) for k, v in c.items()}
        tot_br = {k: int((v & br).sum()) for k, v in c.items()}
        nacL = d['L'].sum() / V.sum()
        x = sL[~np.isnan(sL)]
        mu, sd = float(x.mean()), float(x.std())
        sk = float(((x - mu) ** 3).mean() / sd ** 3); ku = float(((x - mu) ** 4).mean() / sd ** 4 - 3)
        from math import erfc, sqrt
        n = len(x)
        gauss_L90 = n * 0.5 * erfc((0.9 - mu) / sd / sqrt(2)); gauss_R90 = n * 0.5 * erfc((mu - 0.1) / sd / sqrt(2))
        hist = np.histogram(x, bins=np.linspace(0, 1, 21))[0].tolist()
        contagem[f'{nome}|{variante}'] = {
            'candidatos': [cl, cr], 'secoes': int(len(d['L'])), 'secoes_com_voto_valido': n,
            'fatia_nacional_L': round(float(nacL), 5),
            'todas': tot, 'sem_exterior': tot_br,
            'razao_100': round(tot['L100'] / max(tot['R100'], 1), 2), 'razao_90': round(tot['L90'] / max(tot['R90'], 1), 2),
            'pct_secoes_L90': round(100 * tot['L90'] / n, 3), 'pct_secoes_R90': round(100 * tot['R90'] / n, 3),
            'dist_fatia_L': {'media': round(mu, 4), 'dp': round(sd, 4), 'assimetria': round(sk, 3), 'curtose_excesso': round(ku, 3)},
            'normal_mesma_media_dp_esperado': {'L>=90': round(gauss_L90), 'R>=90': round(gauss_R90)},
            'histograma_fatia_L_5pp': hist}
R['contagem'] = contagem

# ---------------- 2026 2T: geografia, tamanho, biometria, persistência
d2, d1, d22, d18 = dados['2026_2T'], dados['2026_1T'], dados['2022_2T'], dados['2018_2T']
c2, sL2, sR2, V2 = conj(d2)
k2 = d2['chave']
L2 = LOC['2']
ind = np.array([L2[k][6] if k in L2 else -1 for k in k2]); rur = np.array([L2[k][7] if k in L2 else -1 for k in k2])
tipo_local = np.array([L2[k][5] if k in L2 else 'exterior/sem cadastro' for k in k2])
nh = np.array([NHc['2'][k][3] if k in NHc['2'] and NHc['2'][k][3] is not None else 0 for k in k2])
nh1 = np.array([NHc['1'][k][3] if k in NHc['1'] and NHc['1'][k][3] is not None else 0 for k in k2])
br = d2['uf'] != 'ZZ'
# tamanho do município (aptos 2T)
apt_mun = collections.Counter()
for m, a in zip(d2['mun'], d2['apt']):
    apt_mun[m] += int(a)
munap = np.array([apt_mun[m] for m in d2['mun']])
pequeno = munap < 10000
R['cadastro_cobertura'] = {'secoes_2T': int(len(k2)), 'com_cadastro': int((ind >= 0).sum()),
                           'indigena_brasil': int((ind == 1).sum()), 'rural_brasil': int((rur == 1).sum())}

# NH do 1T alinhado (mesma seção)
comp1_por_chave = dict(zip(d1['chave'], d1['comp']))
comp1 = np.array([comp1_por_chave.get(k, 0) for k in k2])


def perfil(m, rotulo):
    mb = m & br
    out = {'n': int(m.sum()), 'exterior': int((m & ~br).sum()), 'brasil': int(mb.sum())}
    if mb.sum() == 0:
        return out
    out['pct_indigena'] = round(100 * (ind[mb] == 1).mean(), 1)
    out['pct_rural_texto'] = round(100 * (rur[mb] == 1).mean(), 1)
    out['pct_rural_ou_indigena'] = round(100 * ((rur[mb] == 1) | (ind[mb] == 1)).mean(), 1)
    out['pct_municipio_<10mil_aptos'] = round(100 * pequeno[mb].mean(), 1)
    out['comp_mediano'] = float(np.median(d2['comp'][mb])); out['apt_mediano'] = float(np.median(d2['apt'][mb]))
    out['pct_comparecimento'] = round(100 * d2['comp'][mb].sum() / d2['apt'][mb].sum(), 2)
    out['NH_2T_pct_comp'] = round(100 * nh[mb].sum() / d2['comp'][mb].sum(), 2)
    out['NH_1T_pct_comp_mesmas_secoes'] = round(100 * nh1[mb].sum() / max(comp1[mb].sum(), 1), 2)
    out['NH_2T_mediana_por_secao_pct'] = round(float(np.median(100 * nh[mb] / np.maximum(d2['comp'][mb], 1))), 2)
    uf = collections.Counter(d2['uf'][m]); out['por_UF'] = dict(uf.most_common())
    out['tipo_local'] = dict(collections.Counter(tipo_local[m]).most_common())
    return out


R['perfil_2026_2T'] = {'todas_secoes': perfil(np.ones(len(k2), bool), 'todas'),
                       'Lula_100': perfil(c2['L100'], 'L100'), 'Flavio_100': perfil(c2['R100'], 'R100'),
                       'Lula_>=90': perfil(c2['L90'], 'L90'), 'Flavio_>=90': perfil(c2['R90'], 'R90')}

# participação de indígena/rural entre as quase unânimes e o inverso
R['indigena_rural_2026_2T'] = {
    'secoes_indigenas': int((ind == 1).sum()),
    'indigenas_com_Lula_>=90': int(((ind == 1) & c2['L90']).sum()),
    'indigenas_com_Flavio_>=90': int(((ind == 1) & c2['R90']).sum()),
    'indigenas_fatia_Lula_ponderada': round(float(d2['L'][ind == 1].sum() / V2[ind == 1].sum()), 4),
    'rurais_texto': int((rur == 1).sum()),
    'rurais_fatia_Lula_ponderada': round(float(d2['L'][rur == 1].sum() / V2[rur == 1].sum()), 4),
    'nao_rurais_fatia_Lula_ponderada': round(float(d2['L'][(rur == 0)].sum() / V2[(rur == 0)].sum()), 4)}

# NH por faixa da fatia de Lula (2T), só Brasil
faixas = [0, .1, .2, .3, .4, .5, .6, .7, .8, .9, 1.0001]
tab = []
for a, b in zip(faixas[:-1], faixas[1:]):
    m = br & (sL2 >= a) & (sL2 < b)
    tab.append({'faixa_Lula': f'{int(a*100)}-{min(int(b*100),100)}%', 'secoes': int(m.sum()),
                'NH_2T_pct': round(100 * nh[m].sum() / max(d2['comp'][m].sum(), 1), 2),
                'NH_1T_pct_mesmas': round(100 * nh1[m].sum() / max(comp1[m].sum(), 1), 2),
                'pct_rural_texto': round(100 * (rur[m] == 1).mean(), 1), 'pct_indigena': round(100 * (ind[m] == 1).mean(), 2)})
R['NH_por_faixa_Lula_2026_2T'] = tab
# NH dentro do NE apenas, por faixa (controle regional grosseiro)
NE = np.isin(d2['uf'], ['AL', 'BA', 'CE', 'MA', 'PB', 'PE', 'PI', 'RN', 'SE'])
tab = []
for a, b in zip(faixas[:-1], faixas[1:]):
    m = NE & (sL2 >= a) & (sL2 < b)
    if m.sum() == 0: continue
    tab.append({'faixa_Lula': f'{int(a*100)}-{min(int(b*100),100)}%', 'secoes': int(m.sum()),
                'NH_2T_pct': round(100 * nh[m].sum() / max(d2['comp'][m].sum(), 1), 2)})
R['NH_por_faixa_Lula_2026_2T_so_Nordeste'] = tab


# ---------------- persistência: as mesmas seções antes
def fatia_por_chave(d, dois):
    L, Rr, O = d['L'], d['R'], d['O']
    V = L + Rr if dois else L + Rr + O
    return {k: (l / v if v > 0 else np.nan) for k, l, v in zip(d['chave'], L, V)}


f1v = fatia_por_chave(d1, False); f1d = fatia_por_chave(d1, True)
f22 = fatia_por_chave(d22, False); f18 = fatia_por_chave(d18, False)


def persist(m, lado):
    ks = k2[m]; out = {'n': int(len(ks))}
    for nome, f in (('2026_1T_validos', f1v), ('2026_1T_entre_os_dois', f1d), ('2022_2T', f22), ('2018_2T', f18)):
        v = np.array([f.get(k, np.nan) for k in ks]); ok = ~np.isnan(v)
        x = v[ok] if lado == 'L' else 1 - v[ok]
        out[nome] = {'casadas': int(ok.sum()), 'fatia_mediana_mesmo_lado': round(float(np.median(x)), 4) if ok.sum() else None,
                     'pct_>=90_mesmo_lado': round(100 * float((x >= 0.9).mean()), 1) if ok.sum() else None,
                     'pct_>=80_mesmo_lado': round(100 * float((x >= 0.8).mean()), 1) if ok.sum() else None}
    return out


R['persistencia_2026_2T'] = {'Lula_100': persist(c2['L100'], 'L'), 'Flavio_100': persist(c2['R100'], 'R'),
                             'Lula_>=90': persist(c2['L90'], 'L'), 'Flavio_>=90': persist(c2['R90'], 'R')}
# inverso: das seções com PT >=90% em 2022 2T (casadas), quantas seguem >=90% em 2026 2T
f26 = dict(zip(k2, sL2))
for nome, d in (('2022_2T', d22), ('2018_2T', d18)):
    c, sL, sR, V = conj(d)
    for lado, m in (('PT', c['L90']), ('Bolsonaro', c['R90'])):
        ks = d['chave'][m]; v = np.array([f26.get(k, np.nan) for k in ks]); ok = ~np.isnan(v)
        x = v[ok] if lado == 'PT' else 1 - v[ok]
        R.setdefault('persistencia_inversa', {})[f'{nome}_{lado}_>=90'] = {
            'n': int(len(ks)), 'casadas_2026': int(ok.sum()), 'pct_seguem_>=90_em_2026_2T': round(100 * float((x >= .9).mean()), 1),
            'fatia_mediana_2026_2T_mesmo_lado': round(float(np.median(x)), 4)}

# correlação seção a seção entre 2022 2T e 2026 2T (fatia do PT), Brasil
v22 = np.array([f22.get(k, np.nan) for k in k2]); ok = ~np.isnan(v22) & ~np.isnan(sL2) & br
R['correlacao_secao_2022_2026_2T'] = {'n': int(ok.sum()), 'r': round(float(np.corrcoef(v22[ok], sL2[ok])[0, 1]), 4),
                                      'mudanca_media_pp': round(100 * float((sL2[ok] - v22[ok]).mean()), 2)}

# ---------------- geografia por UF nas outras eleições (só UF)
for nome in ('2026_1T', '2022_2T', '2018_2T'):
    d = dados[nome]; c, *_ = conj(d)
    R.setdefault('UF_outras', {})[nome] = {lado: dict(collections.Counter(d['uf'][c[lado]]).most_common(12))
                                           for lado in ('L100', 'R100', 'L90', 'R90')}

# ---------------- listas: as 4 de Flávio a 100% e amostra das 106 de Lula
def descr(i):
    k = k2[i]; l = L2.get(k)
    return {'chave': str(k), 'municipio': l[0] if l else None, 'local': l[2] if l else None, 'bairro': l[4] if l else None,
            'apt': int(d2['apt'][i]), 'comp': int(d2['comp'][i]), 'L': int(d2['L'][i]), 'R': int(d2['R'][i]),
            'B': int(d2['B'][i]), 'N': int(d2['N'][i]), 'NH': int(nh[i]), 'indigena': int(ind[i]), 'rural': int(rur[i]),
            '2022_2T_fatia_PT': None if np.isnan(f22.get(str(k), np.nan)) else round(float(f22[str(k)]), 3),
            '2026_1T_fatia_Lula_validos': None if np.isnan(f1v.get(str(k), np.nan)) else round(float(f1v[str(k)]), 3)}


R['Flavio_100_lista'] = [descr(i) for i in np.where(c2['R100'])[0]]
R['Lula_100_lista'] = [descr(i) for i in np.where(c2['L100'])[0]]
# municípios com mais seções Lula >=90
mc = collections.Counter(); mcr = collections.Counter()
for i in np.where(c2['L90'])[0]:
    l = L2.get(k2[i]); mc[(d2['uf'][i], l[0] if l else '?')] += 1
for i in np.where(c2['R90'])[0]:
    l = L2.get(k2[i]); mcr[(d2['uf'][i], l[0] if l else 'exterior')] += 1
R['municipios_top_Lula_>=90'] = [[f'{a}/{b}', n] for (a, b), n in mc.most_common(15)]
R['municipios_top_Flavio_>=90'] = [[f'{a}/{b}', n] for (a, b), n in mcr.most_common(15)]
with open(saida, 'w') as f:
    json.dump(R, f, ensure_ascii=False, indent=1, default=lambda o: o.item() if hasattr(o, 'item') else str(o))
print('ok')
