"""Conferencia independente do L5 (Adendo 18). Numeros das pesquisas digitados de novo a partir de
resultados/nacionais_2026_pesquisas_verificadas.txt e do PDF do PoderData 23-24/10 reaberto (pd24.txt)."""
import json, math, itertools, statistics as st
U = json.load(open('urna_totais.json'))
T1, T2, E = U['T1'], U['T2'], U['E']
el = sum(E.values()); v1 = T1['L'] + T1['R'] + el; v2 = T2['L'] + T2['R']
F1 = 100*T1['R']/v1; L1 = 100*T1['L']/v1; O1 = 100*el/v1; F2 = 100*T2['R']/v2; L2 = 100 - F2
print('urna F1 %.3f L1 %.3f O1 %.3f F2 %.3f L2 %.3f' % (F1, L1, O1, F2, L2))
# (instituto, F1, L1, F2) validos publicados
P = [('Datafolha',42,45,51),('Quaest',45,46,51),('AtlasIntel',44.1,47,50.8),('CNT/MDA',42.1,47.8,50.7),
     ('PoderData',43,45,51),('Nexus',39,44,50.5),('RTBD',41,46,52),('Futura',44.8,42.6,50.1),('Gerp',46,44,52),
     ('Verita',47,45,51.56),('Vox',100*41.2/89.8,100*40.4/89.8,49.4)]
def resumo(P, rot):
    e1 = [F1-p[1] for p in P]; e2 = [F2-p[3] for p in P]; vir = [b-a for a,b in zip(e1,e2)]
    pad = sum(1 for a,b in zip(e1,e2) if a>0 and b<0); mesmo = sum(1 for a,b in zip(e1,e2) if (a>0)==(b>0))
    m = st.mean(vir); se = st.stdev(vir)/math.sqrt(len(vir))
    eL1 = st.mean([L1-p[2] for p in P]); eO1 = st.mean([O1-(100-p[1]-p[2]) for p in P]); eL2 = st.mean([L2-(100-p[3]) for p in P])
    # erro no 1T so entre os dois finalistas (fatia de Flavio em F+L)
    tp = st.mean([100*F1/(F1+L1) - 100*p[1]/(p[1]+p[2]) for p in P])
    print(f'{rot}: k={len(P)} padrao={pad} mesmo_sinal={mesmo} virada_media={m:.2f} ep_entre={se:.2f} '
          f'min_virada={max(vir):.2f} | erro1T F {st.mean(e1):.2f} L {eL1:.2f} elim {eO1:.2f} | erro2T F {st.mean(e2):.2f} L {eL2:.2f} | erro1T F na fatia F/(F+L) {tp:.2f}')
    return vir
vir = resumo(P, 'base')
for p, v in zip(P, vir): print('   %-11s e1 %+.2f e2 %+.2f virada %+.2f' % (p[0], F1-p[1], F2-p[3], v))
# sensibilidades
alt = dict((p[0], p) for p in P)
def troca(**kw):
    Q = []
    for p in P:
        if p[0] in kw: Q.append((p[0],) + kw[p[0]])
        else: Q.append(p)
    return Q
resumo(troca(Verita=(45.14,44.65,51.56), AtlasIntel=(43.1,47,50.8)), 'alt Verita 45,14 Atlas 43,1')
# validos derivados dos totais (onde os totais publicados nao fecham com os validos)
resumo(troca(Datafolha=(100*40/93,100*42/93,100*48/95), Quaest=(100*38/87,100*40/87,100*46/91)), 'Datafolha/Quaest pelos totais')
resumo([p for p in P if p[0] not in ('Vox','Verita')], 'sem Vox e Verita')
resumo([p for p in P if p[0] != 'Nexus'], 'sem Nexus (1T de 25-27/9)')
resumo([p for p in P if p[0] in ('Datafolha','CNT/MDA','PoderData','AtlasIntel')], 'so os 4 com validos publicados nos dois turnos e ficha')
# pior caso: tirar os 3 com maior virada
s = sorted(P, key=lambda p: (F2-p[3])-(F1-p[1]))
resumo(s[3:], 'sem as 3 maiores viradas')
resumo(s[5:], 'sem as 5 maiores viradas')
# 2T, Lula abaixo da urna: inclui Ipespe 49,5
L2p = [100-p[3] for p in P] + [49.5]
print('2T erro Lula (12 pesquisas): media %.2f min %.2f max %.2f todos positivos: %s' % (st.mean([L2-x for x in L2p]), min(L2-x for x in L2p), max(L2-x for x in L2p), all(L2-x>0 for x in L2p)))

# ------------------------------------------------ (b) PoderData 23-24/10 reaberto
# 2T por voto no 1T (Flavio, Lula, branco/nulo, nao sabe)
PD = {'Cury':(58,29,11,2),'Renan':(43,33,19,5),'Caiado':(46,30,20,4),'Outro':(65,15,0,20),'F':(94,5,1,0),'L':(5,94,1,0),'BN':(26,50,21,3)}
grp = {'Cury':['70'],'Renan':['14'],'Caiado':['55'],'Outro':['30','80','16','27','21','35','29']}
gv = {g: sum(E[x] for x in xs) for g, xs in grp.items()}
gL = T2['L']-T1['L']; gF = T2['R']-T1['R']
eF = sum(PD[g][0]/100*gv[g] for g in gv); eL = sum(PD[g][1]/100*gv[g] for g in gv)
print('\n(b) ganho L %d F %d | dos eliminados pela PoderData: F %.0f L %.0f' % (gL, gF, eF, eL))
rL = gL - eL; rF = gF - eF
print('  fid 100%%: saldo L %.0f F %.0f total %.0f fatia L %.1f%%' % (rL, rF, rL+rF, 100*rL/(rL+rF)))
# fidelidade declarada: Lula perde 5% para F e 1% para nenhum; Flavio idem
rL2 = rL + T1['L']*0.06 - T1['R']*0.05; rF2 = rF + T1['R']*0.06 - T1['L']*0.05
print('  fid declarada: saldo L %.0f F %.0f total %.0f fatia L %.1f%%' % (rL2, rF2, rL2+rF2, 100*rL2/(rL2+rF2)))
lim = 100*50/76 + 30
print('  analogo PoderData BN no 1T: fatia %.1f%%, limite %.1f%%' % (100*50/76, lim))
# equivalencia: saldo dividido como 65,8%
S = rL2 + rF2; m = 50/76
Ls = T2['L'] - rL2 + m*S; Fs = T2['R'] - rF2 + (1-m)*S
print('  equivalencia: L validos %.2f%% ganho L %.0f F %.0f diferenca na margem %.0f' % (100*Ls/(Ls+Fs), Ls-T1['L'], Fs-T1['R'], (T2['L']-T2['R'])-(Ls-Fs)))
# o que a PoderData implica diretamente para o 2T, aplicando a tabela inteira ao eleitorado do 1T (inclui BN e abstencao)
bn1 = T1['B'] + T1['N'] + U['n28']; ab1 = T1['apt'] - T1['comp']
# nao votou no 1T: 35 F 50 L 15 BN; ponderar pela intencao de comparecimento: entre quem nao votou 65% com certeza
cands = {'F':T1['R'],'L':T1['L'],'BN':bn1}; cands.update(gv)
Fp = sum(PD[g][0]/100*v for g, v in cands.items()); Lp = sum(PD[g][1]/100*v for g, v in cands.items())
print('  tabela PoderData aplicada aos votantes do 1T: F %.0f L %.0f -> L %.2f%% dos validos' % (Fp, Lp, 100*Lp/(Fp+Lp)))
for frac in (0.0, 0.05, 0.10, 0.15, 0.20):
    Fq = Fp + frac*ab1*0.35; Lq = Lp + frac*ab1*0.50
    print('    + %.0f%% dos abstencionistas do 1T votando como "nao votou" (35/50): L %.2f%%' % (100*frac, 100*Lq/(Fq+Lq)))
# o que seria preciso nos eliminados para fechar a urna, mantendo o resto da tabela PoderData
# L2 - F2 real vs. com tabela; quanto da margem os eliminados precisariam mudar
