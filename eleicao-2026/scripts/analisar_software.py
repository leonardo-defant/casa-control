"""T10 do pré-registro: versão do aplicativo, mídia de votação, assinaturas e mídia de resultado, por urna, nos dois turnos.
Uso: python3 -I analisar_software.py <pasta_arq_2t> <saida.json>
"""
import collections, json, os, re, sys, zipfile

D1, D2 = '04/10/2026', '25/10/2026'
pasta, saida = sys.argv[1], sys.argv[2]
res = {}; agg = collections.Counter(); versoes = collections.Counter(); midias_dia = collections.Counter(); mr = collections.Counter()
falhas_assin = []; novos = []; problemas = []
for raiz, dirs, arqs in os.walk(pasta):
    logs = sorted(a for a in arqs if a.endswith('-log.jez'))
    if not logs: continue
    p = os.path.join(raiz, logs[-1])
    try:
        z = zipfile.ZipFile(p); nome = [n for n in z.namelist() if n.startswith('logd')][0]
        L = [l.split('\t') for l in z.read(nome).decode('latin1').splitlines()]
    except Exception as e:
        problemas.append((p, str(e))); continue
    L = [x for x in L if len(x) >= 5]
    r = {'versoes': sorted({x[4].split(': ', 1)[1] for x in L if x[4].startswith('Versão da aplicação')}),
         'urnas': sorted({x[2] for x in L}),
         'datas': sorted({x[0][:10] for x in L}, key=lambda d: d[6:] + d[3:5] + d[:2])}
    def midia(dia):
        return sorted({x[4].split(': ', 1)[1] for x in L if x[0].startswith(dia) and x[4].startswith('Data e hora da geração da mídia de votação')})
    r['midia_1t'], r['midia_2t'] = midia(D1), midia(D2)
    r['mr'] = sorted({x[4].split(': ', 1)[1] for x in L if x[4].startswith('Data e hora da geração da MR')})
    ass = [x for x in L if x[4].startswith('Verificação de assinatura')]
    r['assinaturas'] = len(ass); r['assinaturas_sem_sucesso'] = [x[0] + ' ' + x[4] for x in ass if '[SUCESSO]' not in x[4]]
    comp = lambda dia: {re.sub(r'o0\d{4}', 'oPLEITO', re.search(r'\[(/[^\]]+)\]', x[4]).group(1)) for x in ass if x[0].startswith(dia) and re.search(r'\[(/[^\]]+)\]', x[4])}
    c1, c2 = comp(D1), comp(D2)
    r['componentes_novos_2t'] = sorted(c2 - c1) if c1 else None
    r['contingencia'] = any('contingência' in x[4] for x in L)
    r['tem_1t_no_log'] = any(x[0].startswith(D1) for x in L)
    k = raiz.split('arq/')[-1]
    res[k] = r
    agg['urnas'] += 1; agg['com_1t_no_log'] += r['tem_1t_no_log']; agg['contingencia'] += r['contingencia']
    for v in r['versoes']: versoes[v] += 1
    midias_dia[(tuple(r['midia_1t']) == tuple(r['midia_2t']), bool(r['midia_1t']))] += 1
    for m in r['mr']: mr[m[:10]] += 1
    if r['assinaturas_sem_sucesso']: falhas_assin.append((k, r['assinaturas_sem_sucesso'][:3]))
    if r['componentes_novos_2t']: novos.append((k, r['componentes_novos_2t']))
json.dump({'por_urna': res, 'problemas': problemas}, open(saida, 'w'), ensure_ascii=False)
print('logs analisados:', dict(agg))
print('versoes do aplicativo:', dict(versoes))
print('midia de votacao igual no dia do 1T e do 2T (igual, tem_1T):', dict(midias_dia))
print('datas de geracao das midias de resultado (dia):', dict(sorted(mr.items())))
print('urnas com verificacao de assinatura sem SUCESSO:', len(falhas_assin), falhas_assin[:5])
print('urnas com componente novo no 2T:', len(novos), novos[:5])
print('logs ilegiveis:', len(problemas))
