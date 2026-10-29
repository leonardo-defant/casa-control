import numpy as np
for rot in ('2026_t2','2026_t1','2022_t2','2018_t2'):
    z=np.load(rot+'.npz'); L,R,O,B,N,comp=[z[c] for c in ('L','R','O','B','N','comp')]
    uf=np.array([k.split('|')[0] for k in z['chave']]); br=uf!='ZZ'
    V=L+R+O; ok=V>0
    print(rot, 'secoes',len(L),'tipos',dict(zip(*np.unique(z['tipo'],return_counts=True))), 'V=0:',int((~ok).sum()))
    for nome,m in (('todas',np.ones_like(br)),('sem ZZ',br)):
        sL=np.where(ok,L/np.maximum(V,1),np.nan); sR=np.where(ok,R/np.maximum(V,1),np.nan)
        tL=L/np.maximum(comp,1); tR=R/np.maximum(comp,1)
        r={'100%val':((L==V)&ok&m).sum(), '100%valR':((R==V)&ok&m).sum(),
           '>90val':((sL>0.9)&m).sum(),'>90valR':((sR>0.9)&m).sum(),
           '>=90val':((sL>=0.9)&m).sum(),'>=90valR':((sR>=0.9)&m).sum(),
           '>90comp':((tL>0.9)&m).sum(),'>90compR':((tR>0.9)&m).sum(),
           '100%comp':((L==comp)&(comp>0)&m).sum(),'100%compR':((R==comp)&(comp>0)&m).sum()}
        if rot.endswith('t1'):
            sLd=np.where(L+R>0,L/np.maximum(L+R,1),np.nan)
            r.update({'>90 L/(L+R)':((sLd>0.9)&m).sum(),'>90 R/(L+R)':((sLd<0.1)&m).sum(),'100 L/(L+R)':((R==0)&(L>0)&m).sum(),'100 R/(L+R)':((L==0)&(R>0)&m).sum()})
        print('  ',nome,{k:int(v) for k,v in r.items()})
