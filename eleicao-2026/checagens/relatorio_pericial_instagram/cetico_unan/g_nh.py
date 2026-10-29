import pickle, re, unicodedata, collections, json
import numpy as np
Q = '/tmp/claude-0/-home-user-casa-control/ce2a8c88-e5ad-504f-8950-6f5ee14ae721/scratchpad/relatorio_pericial/cetico_unan/'
LOC, nsl = pickle.load(open(Q + 'locais.pkl', 'rb'))
B = pickle.load(open(Q + '2026.pkl', 'rb')); s = B['2']; s1 = B['1']
NH = {'1': {}, '2': {}}; CB = {'1': {}, '2': {}}
for f in ('nh1t.tsv', 'nh2t.tsv'):
    for ln in open(Q + f):
        t, k, nh, comp, tu, apt = ln.rstrip('\n').split('\t')
        NH[t][k] = int(nh) if nh.lstrip('-').isdigit() else None; CB[t][k] = int(comp)
print('NH lidos', {t: len(v) for t, v in NH.items()}, 'invalidos', {t: sum(x is None or x < 0 for x in v.values()) for t, v in NH.items()})
ks = s['k']; L, R, comp = s['L'], s['R'], s['comp']; V = L + R; sL = L / np.maximum(V, 1); sR = R / np.maximum(V, 1)
dif = sum(CB['2'].get(k) != c for k, c in zip(ks, comp)); print('comp bweb x base diferentes (2T):', dif)
nh = np.array([max(NH['2'].get(k) or 0, 0) for k in ks])
i1 = {k: j for j, k in enumerate(s1['k'])}
comp1 = np.array([s1['comp'][i1[k]] for k in ks]); nh1 = np.array([max(NH['1'].get(k) or 0, 0) for k in ks])
br = np.array([not k.startswith('ZZ|') for k in ks]); uf = np.array([k.split('|')[0] for k in ks])
def norm(x):
    x = unicodedata.normalize('NFKD', x.upper()); return re.sub(r'[^A-Z0-9 ]', ' ', ''.join(c for c in x if not unicodedata.combining(c)))
IND = re.compile(r'INDIGEN|ALDEIA|\bMALOCA\b')
RUR_E = re.compile(r'ZONA RURAL|\bRURAL\b|POVOADO|\bPOV\b|\bSITIO\b|\bFAZENDA\b|\bFAZ\b|ASSENTAMENTO|\bASSENT\b|AGROVILA|VICINAL|\bGLEBA\b|RIBEIRINH|QUILOMB|\bLINHA\b|\bINTERIOR\b|\bCOLONIA\b')
tx = [norm(' '.join(LOC[k][1:4])) if k in LOC else '' for k in ks]
ind = np.array([bool(IND.search(t)) for t in tx]); rur = np.array([bool(RUR_E.search(t)) for t in tx])
ns = np.array([nsl[LOC[k][5]] if k in LOC else 0 for k in ks])
def taxa(m, t=2):
    m = m & br
    return round(100 * (nh if t == 2 else nh1)[m].sum() / (comp if t == 2 else comp1)[m].sum(), 2)
out = {'pais_2T_BR': taxa(np.ones(len(ks), bool)), 'pais_2T_total_incl_ZZ': round(100*nh.sum()/comp.sum(), 3), 'NH_2T_total': int(nh.sum()),
       'pais_1T_BR': taxa(np.ones(len(ks), bool), 1), 'NH_1T_total': int(sum(max(v or 0, 0) for v in NH['1'].values()))}
grupos = {'L100': (V > 0) & (R == 0), 'R100': (V > 0) & (L == 0), 'L>=90': sL >= .9, 'R>=90': (V > 0) & (sR >= .9)}
for g, m in grupos.items():
    out[g] = {'n_BR': int((m & br).sum()), 'NH2T': taxa(m), 'NH1T_mesmas': taxa(m, 1)}
faixas = [0, .1, .2, .3, .4, .5, .6, .7, .8, .9, 1.01]
out['faixas'] = [(f'{int(a*100)}-{int(min(b,1)*100)}', int(((sL >= a) & (sL < b) & br).sum()), taxa((sL >= a) & (sL < b)), taxa((sL >= a) & (sL < b), 1)) for a, b in zip(faixas[:-1], faixas[1:])]
NE = np.isin(uf, ['AL', 'BA', 'CE', 'MA', 'PB', 'PE', 'PI', 'RN', 'SE'])
out['faixas_NE'] = [(f'{int(a*100)}-{int(min(b,1)*100)}', int(((sL >= a) & (sL < b) & NE).sum()), taxa((sL >= a) & (sL < b) & NE)) for a, b in zip(faixas[:-1], faixas[1:]) if ((sL >= a) & (sL < b) & NE).sum()]
out['tipo'] = {'indigena': taxa(ind), 'rural_estrito_nao_ind': taxa(rur & ~ind), 'demais': taxa(~rur & ~ind),
               'local_<=2_secoes': taxa(ns <= 2), 'local_>2': taxa(ns > 2)}
# dentro de locais pequenos (<=2 seções), Lula>=90 vs Flávio>=90 vs resto
pq = ns <= 2
out['locais_pequenos'] = {'L>=90': taxa(pq & (sL >= .9)), 'R>=90': taxa(pq & (sR >= .9)), 'resto': taxa(pq & (sL < .9) & (sR < .9))}
# top 1% por taxa (comp >= 50)
tx_ = nh / np.maximum(comp, 1); ok = br & (comp >= 50); c = np.percentile(tx_[ok], 99); top = ok & (tx_ >= c)
out['top1'] = {'corte': round(100*float(c), 2), 'n': int(top.sum()), 'UF': collections.Counter(uf[top]).most_common(6),
               'pct_L>=90_no_top': round(100*float((sL[top] >= .9).mean()), 2), 'pct_L>=90_geral': round(100*float((sL[ok] >= .9).mean()), 2),
               'fatia_L_top': round(float(L[top].sum()/V[top].sum()), 4), 'fatia_L_geral': round(float(L[ok].sum()/V[ok].sum()), 4)}
# correlação ponderada entre taxa NH e fatia de Lula, e variação entre turnos nas L>=90
r_ = np.corrcoef(tx_[ok], sL[ok])[0, 1]; out['corr_NH_fatiaL_secao'] = round(float(r_), 4)
# o que cabe nas 106: quanto do NH delas
out['NH_abs_106'] = int(nh[grupos['L100']].sum()); out['NH_abs_L90'] = int(nh[grupos['L>=90'] & br].sum())
print(json.dumps(out, ensure_ascii=False, indent=0))
