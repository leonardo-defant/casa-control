import glob, numpy as np, os
D=os.path.dirname(os.path.abspath(__file__))
def ler(t):
    d={}
    for f in glob.glob(f'{D}/{t}/*.tsv'):
        fh=open(f); h=fh.readline().rstrip('\n').split('\t')
        for line in fh:
            r=dict(zip(h,line.rstrip('\n').split('\t')))
            d[f"{r['uf']}|{r['mun']}|{r['zona']}|{r['secao']}"]={x:int(r[x]) for x in ('loc','comp','NH','L','R')}
    return d
for t in ('t2','t1'):
    T=ler(t)
    ks=[k for k in T if not k.startswith('ZZ') and T[k]['comp']>0]
    loc=np.array(['|'.join(k.split('|')[:3])+'|'+str(T[k]['loc']) for k in ks]); _,g=np.unique(loc,return_inverse=True)
    x=np.array([T[k]['NH']/T[k]['comp'] for k in ks]); c=np.bincount(g)
    mu=np.bincount(g,weights=x)/c; m=c[g]>=2
    L=np.array([T[k]['L'] for k in ks],float); R=np.array([T[k]['R'] for k in ks],float)
    for nome,sel in (('Lula>90',(10*L>9*(L+R))&(L+R>0)),('Flavio>90',(10*R>9*(L+R))&(L+R>0))):
        s=sel&m
        # excesso dentro do local: taxa da seção menos média das OUTRAS seções do mesmo local
        mu_out=(mu[g]*c[g]-x)/np.maximum(c[g]-1,1)
        print(t,nome,'secoes',sel.sum(),'em locais 2+',s.sum(),'excesso medio vs media do local %.3f pp; vs outras secoes do local %.3f pp'%(100*np.mean(x[s]-mu[g][s]),100*np.mean(x[s]-mu_out[s])))
