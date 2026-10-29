import json, numpy as np
U = json.load(open('urna_totais.json')); T1, T2, E = U['T1'], U['T2'], U['E']
grp = {'Cury':['70'],'Renan':['14'],'Caiado':['55'],'Outro':['30','80','16','27','21','35','29']}
gv = {g: sum(E[x] for x in xs) for g, xs in grp.items()}
PD = {'Cury':(58,29,13),'Renan':(43,33,24),'Caiado':(46,30,24),'Outro':(65,15,20)}
gL = T2['L']-T1['L']; gF = T2['R']-T1['R']
rng = np.random.default_rng(7)
for deff in (1, 2):
    nv = 4000*0.89/deff
    n = {g: max(5, round(nv*gv[g]/T1['comp'])) for g in gv}
    nF = round(nv*T1['R']/T1['comp']); nL = round(nv*T1['L']/T1['comp'])
    out100, outfid = [], []
    for _ in range(20000):
        eF = eL = 0
        for g in gv:
            q = rng.multinomial(n[g], np.array(PD[g])/100)/n[g]
            eF += q[0]*gv[g]; eL += q[1]*gv[g]
        rL = gL-eL; rF = gF-eF; out100.append(rL/(rL+rF))
        f = rng.multinomial(nF, [.94,.05,.01])/nF; l = rng.multinomial(nL, [.05,.94,.01])/nL
        rL2 = rL + T1['L']*(l[0]+l[2]) - T1['R']*f[1]; rF2 = rF + T1['R']*(f[1]+f[2]) - T1['L']*l[0]
        outfid.append(rL2/(rL2+rF2))
    a, b = np.array(out100), np.array(outfid)
    se_p = np.sqrt(0.658*0.342/(170*0.76))
    print('deff', deff, 'subamostras', n, 'fid100 ep %.1f  fid decl ep %.1f' % (100*a.std(), 100*b.std()),
          'z fid100 %.1f z decl %.1f' % ((1.153-0.958)/np.hypot(a.std(), se_p), (1.044-0.958)/np.hypot(b.std(), se_p)),
          'P(fid decl < 0.958) %.2f' % (b < 0.958).mean())
