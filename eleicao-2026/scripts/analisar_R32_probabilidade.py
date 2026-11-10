"""R32 (Adendo 32): frequência histórica de cada movimento da eleição de 2026.

Descritivo, sem veredito de fraude. Régua fixada no Adendo 32 (commit cbd7577) antes destas contas.
Fontes, todas em disco:
- presidente 2002 a 2026: totais oficiais conferidos no R27_A4 (resultados/R27_A4_curva_forca_serie.json);
- presidente por UF 2014 a 2026: dados/secoesAAAA.json.gz;
- governador 2018 e 2022: extração por seção e candidato do teste T22
  (/home/user/trabalho-eleicao/adendo27/R27_T22/gov), 26 segundos turnos;
- governador 2026: dados/candidatos_gov_2026_1t_6ufs.json.gz e gov2t_2026_6ufs.json.gz do T22.
Decisões: "líder" = o mais votado do 1º turno entre os dois finalistas; fatia a dois = votos do líder sobre a soma
dos dois finalistas; movimento = fatia a dois do 2º turno menos a do 1º; vantagem = fatia a dois do 1º turno menos 50.
Uso: python3 -I scripts/analisar_R32_probabilidade.py
"""
import json, gzip, glob, os, sys
AQUI = os.path.dirname(os.path.abspath(__file__)); RAIZ = os.path.dirname(AQUI)
T22 = '/home/user/trabalho-eleicao/adendo27/R27_T22'
out = {}

# 1. Presidente, país, 2002 a 2026
a4 = json.load(open(os.path.join(RAIZ, 'resultados', 'R27_A4_curva_forca_serie.json')))
tot = a4['exploratorio']['E2_razao_bruta_2T_sobre_1T']
ofi = {}
for ano in ('2002', '2006', '2010'):
    c = a4['extracao'][ano]['conferencia_oficial']
    ofi[ano] = dict(L1=c['1']['L']['base'], R1=c['1']['R']['base'], L2=c['2']['L']['base'], R2=c['2']['R']['base'],
                    comp1=c['1']['comparecimento_soma_dos_votos'], comp2=c['2']['comparecimento_soma_dos_votos'])
pres = []
def linha(ano, L1, R1, L2, R2, comp1=None, comp2=None):
    lider = 'PT' if L1 > R1 else 'adversário'
    a1 = (max(L1, R1)) / (L1 + R1) * 100
    a2 = (L2 if L1 > R1 else R2) / (L2 + R2) * 100
    return dict(ano=int(ano), lider_1t=lider, fatia_a_dois_lider_1t=round(a1, 3), fatia_a_dois_lider_2t=round(a2, 3),
                movimento_do_lider=round(a2 - a1, 3), vantagem_sobre_50=round(a1 - 50, 3), virou=bool(a2 < 50),
                comp1=comp1, comp2=comp2, var_comp=(comp2 - comp1) if comp1 else None)
for ano in ('2002', '2006', '2010'):
    o = ofi[ano]; pres.append(linha(ano, o['L1'], o['R1'], o['L2'], o['R2'], o['comp1'], o['comp2']))
sec = {}
for ano in (2014, 2018, 2022, 2026):
    d = json.load(gzip.open(os.path.join(RAIZ, 'dados', f'secoes{ano}.json.gz')))
    sec[ano] = d
    s = {t: dict(L=0, R=0, comp=0, B=0, N=0, apt=0) for t in ('1', '2')}
    for k, v in d.items():
        for t in ('1', '2'):
            if t in v:
                for c in ('L', 'R', 'comp', 'B', 'N', 'apt'):
                    s[t][c] += v[t].get(c, 0)
    pres.append(linha(ano, s['1']['L'], s['1']['R'], s['2']['L'], s['2']['R'], s['1']['comp'], s['2']['comp']))
    pres[-1]['bn1'] = s['1']['B'] + s['1']['N']; pres[-1]['bn2'] = s['2']['B'] + s['2']['N']
out['presidente_pais'] = pres

# 2. Presidente por UF, 2014 a 2026: movimento do líder nacional em cada UF, votos absolutos, comparecimento
uf_tab = {}
for ano, d in sec.items():
    U = {}
    for k, v in d.items():
        uf = k.split('|')[0]
        if uf == 'ZZ' or '1' not in v or '2' not in v: continue
        u = U.setdefault(uf, dict(L1=0, R1=0, L2=0, R2=0, c1=0, c2=0, a1=0, a2=0))
        u['L1'] += v['1']['L']; u['R1'] += v['1']['R']; u['L2'] += v['2']['L']; u['R2'] += v['2']['R']
        u['c1'] += v['1']['comp']; u['c2'] += v['2']['comp']; u['a1'] += v['1']['apt']; u['a2'] += v['2']['apt']
    lider_pt = sum(u['L1'] for u in U.values()) > sum(u['R1'] for u in U.values())
    n_lider_caiu = 0; perde_abs_L = []; perde_abs_R = []; comp_cai = []; comp_sobe_185 = []
    for uf, u in U.items():
        f1 = (u['L1'] if lider_pt else u['R1']) / (u['L1'] + u['R1']); f2 = (u['L2'] if lider_pt else u['R2']) / (u['L2'] + u['R2'])
        if f2 < f1: n_lider_caiu += 1
        if u['L2'] < u['L1']: perde_abs_L.append(uf)
        if u['R2'] < u['R1']: perde_abs_R.append(uf)
        dc = (u['c2'] / u['a2'] - u['c1'] / u['a1']) * 100
        if dc < 0: comp_cai.append(uf)
        if dc >= 1.85: comp_sobe_185.append(uf)
    uf_tab[ano] = dict(n_ufs=len(U), lider_nacional='PT' if lider_pt else 'adversário', ufs_em_que_o_lider_caiu=n_lider_caiu,
                       ufs_pt_perde_votos_absolutos=sorted(perde_abs_L), ufs_adversario_perde_votos_absolutos=sorted(perde_abs_R),
                       ufs_comparecimento_cai=sorted(comp_cai), ufs_comparecimento_sobe_1_85_ou_mais=sorted(comp_sobe_185))
out['presidente_por_uf'] = uf_tab

# 3. Governador: 26 segundos turnos de 2018 e 2022 e 6 de 2026
gov = []
for f in sorted(glob.glob(os.path.join(T22, 'gov', 'gov_*.json.gz'))):
    d = json.load(gzip.open(f)); t1 = {}; t2 = {}
    for k, v in d['secoes'].items():
        for c, q in v.get('1', {}).items(): t1[c] = t1.get(c, 0) + q
        for c, q in v.get('2', {}).items(): t2[c] = t2.get(c, 0) + q
    fin = [c for c in t2 if c not in ('95', '96')]
    if len(fin) != 2: continue
    a, b = sorted(fin, key=lambda c: -t1.get(c, 0))
    f1 = t1[a] / (t1[a] + t1[b]) * 100; f2 = t2[a] / (t2[a] + t2[b]) * 100
    gov.append(dict(ano=d['ano'], uf=d['uf'], lider=d['nomes']['1'].get(a, a), fatia_a_dois_lider_1t=round(f1, 3),
                    fatia_a_dois_lider_2t=round(f2, 3), movimento_do_lider=round(f2 - f1, 3), vantagem_sobre_50=round(f1 - 50, 3),
                    virou=bool(f2 < 50), comp1=sum(t1.values()), comp2=sum(t2.values())))
g1 = json.load(gzip.open(os.path.join(RAIZ, 'dados', 'candidatos_gov_2026_1t_6ufs.json.gz')))
g2 = json.load(gzip.open(os.path.join(T22, 'gov2t_2026_6ufs.json.gz')))
t1 = {}; t2 = {}
for k, v in g1['secoes'].items():
    uf = k.split('|')[0]
    for c, q in v.items(): t1.setdefault(uf, {}); t1[uf][c] = t1[uf].get(c, 0) + q
for k, v in g2['secoes'].items():
    uf = k.split('|')[0]
    for c, q in v['cand'].items(): t2.setdefault(uf, {}); t2[uf][c] = t2[uf].get(c, 0) + q
for uf in sorted(t2):
    fin = list(t2[uf])
    if len(fin) != 2: continue
    a, b = sorted(fin, key=lambda c: -t1[uf].get(c, 0))
    f1 = t1[uf][a] / (t1[uf][a] + t1[uf][b]) * 100; f2 = t2[uf][a] / (t2[uf][a] + t2[uf][b]) * 100
    gov.append(dict(ano=2026, uf=uf, lider=a, fatia_a_dois_lider_1t=round(f1, 3), fatia_a_dois_lider_2t=round(f2, 3),
                    movimento_do_lider=round(f2 - f1, 3), vantagem_sobre_50=round(f1 - 50, 3), virou=bool(f2 < 50)))
out['governador'] = gov
json.dump(out, open(os.path.join(RAIZ, 'resultados', 'R32_frequencias.json'), 'w'), ensure_ascii=False, indent=1)

print('PRESIDENTE, PAÍS')
for p in pres: print(p['ano'], p['lider_1t'], 'vantagem', p['vantagem_sobre_50'], 'movimento', p['movimento_do_lider'], 'virou', p['virou'], 'comp', p['var_comp'], 'bn', p.get('bn1'), p.get('bn2'))
print('PRESIDENTE POR UF')
for ano, u in uf_tab.items(): print(ano, json.dumps(u, ensure_ascii=False))
print('GOVERNADOR')
for g in gov: print(g['ano'], g['uf'], 'vantagem', g['vantagem_sobre_50'], 'movimento', g['movimento_do_lider'], 'virou', g['virou'])
ant = [g for g in gov if g['ano'] != 2026]
print('26 antes de 2026: líder caiu em', sum(1 for g in ant if g['movimento_do_lider'] < 0), '; caiu 1,01 ou mais em', sum(1 for g in ant if g['movimento_do_lider'] <= -1.01), '; caiu 2,80 ou mais em', sum(1 for g in ant if g['movimento_do_lider'] <= -2.80), '; virou em', sum(1 for g in ant if g['virou']), 'de', len(ant))
ap = [g for g in ant if g['vantagem_sobre_50'] <= 3]
print('com vantagem de até 3 pontos:', len(ap), 'viradas', sum(1 for g in ap if g['virou']))
print('6 de 2026: líder caiu em', sum(1 for g in gov if g['ano'] == 2026 and g['movimento_do_lider'] < 0), 'virou em', sum(1 for g in gov if g['ano'] == 2026 and g['virou']))
