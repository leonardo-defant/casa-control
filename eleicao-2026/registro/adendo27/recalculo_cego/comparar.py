"""Compara o recálculo cego (Adendo 27) com o gabarito. Uso: python3 -I comparar.py"""
import json, math
R='/home/user/trabalho-eleicao/adendo27/recalculo/'
g=json.load(open(R+'gabarito_recalculo.json'))
resp={}
for f in ('resposta_cega_ABCD.json','resposta_cega_EFGH.json'):
    resp.update(json.load(open(R+f)))
def num(x):
    if isinstance(x,bool): return None
    if isinstance(x,(int,float)): return float(x)
    if isinstance(x,str):
        try: return float(x.replace(',','.'))
        except Exception: return None
    return None
linhas=[]; tot=dict(itens=0,principal_bate=0,principal_fora=0,principal_ausente=0,saidas=0,saidas_batem=0,saidas_fora=0,saidas_ausentes=0,saidas_nao_numericas=0)
fora=[]
for it in g['itens']:
    i=it['id']; r=resp.get(i,{}); tot['itens']+=1
    st_princ=None
    for k,s in it['saidas'].items():
        tot['saidas']+=1
        v=s['valor']; tol=s['tolerancia']; t=tol.get('tipo')
        if k not in r:
            tot['saidas_ausentes']+=1; st='ausente'; rv=None
        else:
            rv=r[k]
            a=num(v); b=num(rv)
            if a is None or b is None:
                st='igual' if str(v).strip()==str(rv).strip() else 'nao_numerica_diferente'
                if st=='igual': tot['saidas_batem']+=1
                else: tot['saidas_nao_numericas']+=1
            else:
                d=abs(a-b)
                if t=='exato': ok=(d==0)
                elif t in('absoluta','coeficiente'): ok=(d<=tol.get('limite',0)+1e-12)
                elif t=='relativa': ok=(d<=tol.get('fracao',0.05)*abs(a)+1e-12)
                else: ok=(d==0)
                st='bate' if ok else 'fora'
                tot['saidas_batem' if ok else 'saidas_fora']+=1
        if st in('fora','ausente','nao_numerica_diferente'):
            fora.append(dict(id=i,saida=k,principal=(k==it['saida_principal']),publicado=v,recalculado=rv,tolerancia=tol,estado=st,titulo=it['titulo_neutro'],origem=it['teste_de_origem']))
        if k==it['saida_principal']: st_princ=st
    if st_princ in('bate','igual'): tot['principal_bate']+=1
    elif st_princ=='ausente' or st_princ is None: tot['principal_ausente']+=1
    else: tot['principal_fora']+=1
json.dump(dict(totais=tot,fora=fora),open('comparacao.json','w'),ensure_ascii=False,indent=1)
print(tot)
for f in fora:
    print(('PRINCIPAL ' if f['principal'] else '          ')+f['id'],f['saida'],'|',f['estado'],'| publicado',f['publicado'],'| cego',f['recalculado'],'|',json.dumps(f['tolerancia'],ensure_ascii=False)[:80])
