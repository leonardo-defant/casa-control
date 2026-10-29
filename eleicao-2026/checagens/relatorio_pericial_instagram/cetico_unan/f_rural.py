import pickle, re, unicodedata, collections, json
import numpy as np
Q = '/tmp/claude-0/-home-user-casa-control/ce2a8c88-e5ad-504f-8950-6f5ee14ae721/scratchpad/relatorio_pericial/cetico_unan/'
LOC, nsl = pickle.load(open(Q + 'locais.pkl', 'rb'))
s = pickle.load(open(Q + '2026.pkl', 'rb'))['2']
def norm(x):
    x = unicodedata.normalize('NFKD', x.upper())
    return re.sub(r'[^A-Z0-9 ]', ' ', ''.join(c for c in x if not unicodedata.combining(c)))
IND = re.compile(r'INDIGEN|ALDEIA|\bMALOCA\b')
RUR_A = re.compile(r'ZONA RURAL|\bRURAL\b|POVOADO|\bPOV\b|\bSITIO\b|\bFAZENDA\b|\bFAZ\b|ASSENTAMENTO|\bASSENT\b|AGROVILA|'
                 r'COMUNIDADE|\bCOM\b|\bRAMAL\b|IGARAPE|VICINAL|\bLOCALIDADE\b|\bGLEBA\b|\bCOLONIA\b|RIBEIRINH|\bINTERIOR\b|\bLINHA\b|\bRIO [A-Z]+ ?KM|\bKM\b')
# estrita: só termos inequivocamente rurais
RUR_E = re.compile(r'ZONA RURAL|\bRURAL\b|POVOADO|\bPOV\b|\bSITIO\b|\bFAZENDA\b|\bFAZ\b|ASSENTAMENTO|\bASSENT\b|AGROVILA|VICINAL|\bGLEBA\b|RIBEIRINH|QUILOMB')
ks = s['k']; L, R = s['L'], s['R']; V = L + R; sL = L / np.maximum(V, 1)
br = np.array([k in LOC for k in ks])
tx = [norm(' '.join(LOC[k][1:4])) if k in LOC else '' for k in ks]
ind = np.array([bool(IND.search(t)) for t in tx]); ra = np.array([bool(RUR_A.search(t)) for t in tx]); re_ = np.array([bool(RUR_E.search(t)) for t in tx])
# só COM / KM / LINHA / COMUNIDADE etc. sem termo estrito
ns = np.array([nsl[LOC[k][5]] if k in LOC else 0 for k in ks])
peq = ns <= 2
m90 = (sL >= .9) & (V > 0); m106 = (V > 0) & (R == 0); mR90 = (V > 0) & (R / np.maximum(V, 1) >= .9)
def p(m):
    mb = m & br
    return {'n': int(mb.sum()), 'rural_A_ou_ind': round(100*float((ra|ind)[mb].mean()), 1), 'rural_A': round(100*float(ra[mb].mean()), 1),
            'rural_estrito_ou_ind': round(100*float((re_|ind)[mb].mean()), 1), 'indigena': round(100*float(ind[mb].mean()), 2),
            'local_ate_2_secoes': round(100*float(peq[mb].mean()), 1), 'secoes_no_local_mediana': float(np.median(ns[mb]))}
out = {'pais': p(np.ones(len(ks), bool)), 'Lula>=90': p(m90), 'Lula100': p(m106), 'Flavio>=90': p(mR90), 'n_ind_total': int((ind & br).sum()),
       'ind_com_Lula>=90': int((ind & m90).sum())}
# quais termos disparam a classificação A sem estrito, entre Lula>=90
cnt = collections.Counter()
for j in np.where(m90 & br & ra & ~re_ & ~ind)[0]:
    for t in ('COMUNIDADE', ' COM ', 'IGARAPE', 'LOCALIDADE', 'COLONIA', 'INTERIOR', 'LINHA', ' KM ', 'RAMAL'):
        if t in ' ' + tx[j] + ' ': cnt[t] += 1
out['termos_soA_Lula90'] = cnt.most_common()
# falsos positivos possíveis de ALDEIA no país: locais indígenas em municípios grandes
big = collections.Counter()
for j in np.where(ind & br)[0]:
    if 'ALDEIA' in tx[j] and 'INDIGEN' not in tx[j]:
        big[LOC[ks[j]][0]] += 1
out['ALDEIA_sem_INDIGEN_por_mun_top'] = big.most_common(10)
print(json.dumps(out, ensure_ascii=False, indent=0))
# lista das 106 e 4
for nome, m in (('L100', m106), ('R100', (V > 0) & (L == 0))):
    print('====', nome)
    for j in np.where(m)[0]:
        k = ks[j]; l = LOC.get(k, ('?',)*6)
        print(k, '|', l[0], '|', l[1], '|', l[3], '|', l[4], '| ind' if ind[j] else '', '| rurA' if ra[j] else '', '| rurE' if re_[j] else '', '| nsec', ns[j], '| V', V[j])
