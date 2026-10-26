"""Analisa a amostra de arquivos de urna baixada do site de resultados.

Uso: python3 -I analisar_amostra.py <pasta_arq_2t> <pasta_arq_1t> <secoes2026_1t.json.gz> <lista_municipios.txt|-> <saida_dir>
Saídas:
  secoes2026_2t_amostra.json.gz   2º turno no formato das bases ('2' e '2g'), lido dos -bu.dat
  validacao_decodificador_1t.json 1º turno: boletim decodificado contra o bweb (mesma seção)
  T1_soma_municipios.json         soma dos boletins dos municípios inteiros contra o oficial do município
  T2_rdv_bu.json                  RDV contra boletim, por seção e turno
  T3_logs.json                    métricas de log por seção e turno
"""
import os as _os, sys as _sys
_sys.path.insert(0, _os.path.dirname(_os.path.abspath(__file__)))
import collections, gzip, json, os, ssl, sys, time, urllib.request
from decodificar import ler_bu, bu_para_secao, ler_rdv, rdv_para_bu, ler_log
from lib import carregar

arq2, arq1, base1, lista_mun, saida = sys.argv[1:6]
os.makedirs(saida, exist_ok=True)
d1 = carregar(base1)
_cp = os.path.join(os.path.dirname(base1), 'candidatos2026_1t.json.gz')
CAND = carregar(_cp)['secoes'] if os.path.exists(_cp) else None
CTX = ssl.create_default_context(cafile='/root/.ccr/ca-bundle.crt')


def secoes(pasta):
    for uf in sorted(os.listdir(pasta)):
        for m in sorted(os.listdir(os.path.join(pasta, uf))):
            for z in sorted(os.listdir(os.path.join(pasta, uf, m))):
                for s in sorted(os.listdir(os.path.join(pasta, uf, m, z))):
                    p = os.path.join(pasta, uf, m, z, s)
                    yield f'{uf.upper()}|{int(m)}|{int(z)}|{int(s)}', p


def arquivos(p, sufixo):
    return sorted(os.path.join(p, f) for f in os.listdir(p) if f.endswith(sufixo))


def hashes(p):
    try:
        a = json.load(open(os.path.join(p, 'aux.json')))
        return [(h.get('st'), h.get('dr'), h.get('hr')) for h in a.get('hashes', [])]
    except Exception:
        return None


def processar(pasta, turno, data):
    base, t2, t3, prob = {}, {}, {}, []
    for k, p in secoes(pasta):
        bus = arquivos(p, '-bu.dat'); rdvs = arquivos(p, '-rdv.dat'); logs = arquivos(p, '-log.jez')
        hs = hashes(p)
        if not bus:
            prob.append((k, 'sem bu', hs)); continue
        b = ler_bu(bus[-1]); s, g = bu_para_secao(b)
        if s is None:
            prob.append((k, 'bu sem presidente', hs)); continue
        rec = {turno: s}
        if g: rec[turno + 'g'] = g
        base[k] = rec
        if len(bus) > 1 or (hs and len(hs) > 1):
            prob.append((k, f'{len(bus)} boletins / {len(hs) if hs else 0} hashes', hs))
        if rdvs:
            r = rdv_para_bu(ler_rdv(rdvs[-1]))
            dif = {}
            for cargo, ref in ((1, s), (3, g)):
                if ref is None: continue
                rc = r.get(cargo, collections.Counter())
                campos = ('L', 'R', 'O', 'B', 'N') if cargo == 1 else ('V', 'B', 'N')
                dd = {c: rc.get(c, 0) - ref[c] for c in campos if rc.get(c, 0) != ref[c]}
                nums = set(ref.get('cand', {})) | {x[4:] for x in rc if x.startswith('num:')}
                for n in nums:
                    a_, b_ = rc.get('num:' + n, 0), ref.get('cand', {}).get(n, 0)
                    if a_ != b_: dd['cand' + n] = a_ - b_
                for x in rc:
                    if x.startswith('tipo'): dd[x] = rc[x]
                if rc.get('total', 0) != ref['comp']: dd['total_vs_comp'] = rc.get('total', 0) - ref['comp']
                if dd: dif[cargo] = dd
            t2[k] = dif
        if logs:
            try:
                m = ler_log(logs[-1], data)
                m['comp_bu'] = s['comp']
                m['A1_dif_comp'] = m['computados'] - s['comp']
                t3[k] = m
            except Exception as e:
                prob.append((k, f'log ilegivel: {e}', hs))
    return base, t2, t3, prob


b2, t2_2, t3_2, prob2 = processar(arq2, '2', '25/10/2026')
with gzip.open(os.path.join(saida, 'secoes2026_2t_amostra.json.gz'), 'wt') as f:
    json.dump(b2, f, separators=(',', ':'))
print('2T: secoes com boletim', len(b2), 'com rdv', len(t2_2), 'com log', len(t3_2), 'problemas', len(prob2))

b1, t2_1, t3_1, prob1 = processar(arq1, '1', '04/10/2026') if os.path.isdir(arq1) else ({}, {}, {}, [])
# validação do decodificador: 1º turno decodificado contra o bweb
val = {'secoes': 0, 'iguais': 0, 'diferentes': []}
for k, v in b1.items():
    s = v['1']; r = d1.get(k, {}).get('1')
    if r is None: continue
    val['secoes'] += 1
    campos = ('L', 'R', 'O', 'B', 'N', 'comp', 'apt', 'urna', 'loc')
    dd = {c: (s[c], r[c]) for c in campos if s[c] != r[c]}
    if CAND is not None:
        ref_c = {n: q for n, q in CAND.get(k, {}).items()}
        for n in set(ref_c) | set(s.get('cand', {})):
            if ref_c.get(n, 0) != s.get('cand', {}).get(n, 0): dd['cand' + n] = (s.get('cand', {}).get(n, 0), ref_c.get(n, 0))
    g1, gr = v.get('1g'), d1[k].get('1g')
    if g1 and gr:
        dd.update({'g' + c: (g1[c], gr[c]) for c in ('B', 'N', 'V', 'comp') if g1[c] != gr[c]})
    if dd: val['diferentes'].append((k, dd))
    else: val['iguais'] += 1
json.dump(val, open(os.path.join(saida, 'validacao_decodificador_1t.json'), 'w'), ensure_ascii=False, indent=1)
print('validacao 1T: secoes', val['secoes'], 'iguais', val['iguais'], 'diferentes', len(val['diferentes']))
if val['secoes'] == 0:
    print('AVISO: decodificador NAO validado contra o bweb (nenhum boletim do 1T); T1 a T3 sao provisorios pela regra 3 do pre-registro')

# T1: municípios inteiros
t1 = {}
if lista_mun != '-':
    muns = sorted({'|'.join(l.split('|')[:2]) for l in open(lista_mun).read().split()})
    lista_sec = collections.defaultdict(set)
    for l in open(lista_mun).read().split(): lista_sec['|'.join(l.split('|')[:2])].add(l)
    for mu in muns:
        uf, m = mu.split('|')
        tem = [k for k in lista_sec[mu] if k in b2]
        soma = collections.Counter()
        for k in tem:
            for c in ('L', 'R', 'B', 'N', 'comp'): soma[c] += b2[k]['2'][c]
        u = f'https://resultados.tse.jus.br/oficial/ele2026/6258/dados/{uf.lower()}/{uf.lower()}{int(m):05d}-c0001-e006258-u.json'
        try:
            with urllib.request.urlopen(u, timeout=60, context=CTX) as r:
                o = json.load(r)
            c = {x['n']: int(x['vap']) for a in o['carg'][0]['agr'] for p in a['par'] for x in p['cand']}
            of = {'L': c.get('13', 0), 'R': c.get('22', 0), 'B': int(o['v']['vb']), 'N': int(o['v']['tvn']), 'comp': int(o['e']['c'])}
            completo = len(tem) == len(lista_sec[mu])
            t1[mu] = {'secoes_lista': len(lista_sec[mu]), 'secoes_com_bu': len(tem), 'completo': completo, 'boletins': dict(soma), 'oficial': of,
                      'diferenca': ({c: soma[c] - of[c] for c in of} if completo else 'INCOMPLETO: faltam boletins baixados'),
                      'secoes_totalizadas_oficial': o['s']['st'], 'secoes_oficial': o['s']['ts']}
        except Exception as e:
            t1[mu] = {'erro': str(e)}
        time.sleep(1)
    json.dump(t1, open(os.path.join(saida, 'T1_soma_municipios.json'), 'w'), ensure_ascii=False, indent=1)
    for mu, r in t1.items(): print('T1', mu, r.get('secoes_com_bu'), '/', r.get('secoes_lista'), 'dif', r.get('diferenca', r.get('erro')))

json.dump({'2': t2_2, '1': t2_1}, open(os.path.join(saida, 'T2_rdv_bu.json'), 'w'), ensure_ascii=False)
for t, tt in (('2', t2_2), ('1', t2_1)):
    print(f'T2 turno {t}: secoes {len(tt)}, com diferenca {sum(1 for v in tt.values() if v)}')
json.dump({'2': t3_2, '1': t3_1, 'problemas_2': prob2, 'problemas_1': prob1}, open(os.path.join(saida, 'T3_logs.json'), 'w'), ensure_ascii=False)
for t, tt in (('2', t3_2), ('1', t3_1)):
    n = len(tt)
    if not n: continue
    agg = {a: sum(1 for v in tt.values() if v[a] != 0) for a in ('A1_dif_comp', 'A2_antes', 'A2_depois', 'A3_sem_habilitacao', 'A4_menos_2s', 'A5_rajadas')}
    print(f'T3 turno {t}: secoes {n}; secoes com cada anomalia: {agg}; total A4 {sum(v["A4_menos_2s"] for v in tt.values())}')
