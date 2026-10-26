"""T20 do pré-registro (adendo 9): fechamento das pendências do T10 e identidade dos candidatos nos boletins.

Pendências do T10, por urna:
  sem_1t_no_log      o log não tem o dia do 1º turno
  midia_diferente    a mídia de votação lida no dia do 1º turno difere da lida no dia do 2º, ou falta a leitura num dos dias
  mr_fora            alguma MR gerada fora de 10 a 15/10
Cada explicação é ligada ao evento que a sustenta, no bloco de log em que ele ocorre (o logd.dat e os .jez internos,
que guardam papéis anteriores da urna, são blocos diferentes):
  sem_1t_no_log      número da urna no bweb do 1º turno diferente do boletim do 2º (troca); ou carga como urna de
                     contingência no período do 2º turno (a partir de 05/10). Carga de contingência só em setembro
                     é relatada à parte (a urna foi reserva antes de ser recarregada para votação).
  midia_diferente    mesma mídia nos dois turnos quando se olha também a véspera de cada um (03/10 e 24/10), sem mídia
                     nova; ou mídia nova com contingência de mídia de votação registrada em 24 ou 25/10.
  mr_fora            MR só de aplicativos (sem VOTA); MR lida numa carga de urna de contingência do 2º turno;
                     carga nova (SCUE) da urna no mesmo bloco entre a geração da MR e a primeira leitura; recuperador
                     de dados no mesmo bloco entre a geração e a leitura.
Depois confere, em todos os boletins da amostra, que os únicos votáveis de presidente são 13 e 22 e que os de
governador formam o mesmo par dentro de cada UF.
Uso: python3 -I analisar_pendencias.py <pasta_arq_2t> <T10_software.json> <secoes2026_1t.json.gz> <amostra_2t.json.gz>
"""
import os as _os, sys as _sys
_sys.path.insert(0, _os.path.dirname(_os.path.abspath(__file__)))
import collections, datetime, json, os, re, sys
from decodificar import _linhas_log
from lib import carregar

MIDIA = 'Data e hora da geração da mídia de votação: '
MR = 'Data e hora da geração da MR'
APPS = ('Aplicativo presente na MR', 'Aplicativos presentes na MR')
INICIO_2T = datetime.datetime(2026, 10, 5)
RX_DH = re.compile(r'(\d\d)/(\d\d)/(\d{4})\D+(\d\d):(\d\d):(\d\d)')


def dh(s):
    m = RX_DH.search(s)
    if not m:
        return None
    d, mo, a, h, mi, se = map(int, m.groups())
    return datetime.datetime(a, mo, d, h, mi, se)


def ler(caminho):
    """Eventos por bloco de log, com data e hora e o modo de carga em vigor."""
    blocos = []
    for bl in _linhas_log(caminho):
        b = {'modo_carga': [], 'contingencia_mv': [], 'contingencia_executada': [], 'recuperador': [], 'carga_scue': [],
             'midias': collections.defaultdict(set), 'mrs': []}
        modo = None; apps = None
        for l in bl:
            x = l.split('\t')
            if len(x) < 5:
                continue
            t = dh(x[0]); app, msg = x[3], x[4]
            if t is None:
                continue
            if msg.startswith('Modo de carga da UE - '):
                modo = msg[len('Modo de carga da UE - '):]; b['modo_carga'].append((t, modo))
            elif msg.startswith('Contingência de MV executada com sucesso') or msg.startswith('Serial da MV nova registrada na MI'):
                b['contingencia_mv'].append(t)
            elif msg.startswith('Contingência executada com sucesso'):
                b['contingencia_executada'].append(t)
            elif msg.startswith('Iniciando aplicação RECUPERADOR DE DADOS'):
                b['recuperador'].append(t)
            elif app == 'SCUE' and msg.startswith('Código de carga'):
                b['carga_scue'].append(t)
            if msg.startswith(MIDIA):
                b['midias'][x[0][:10]].add(msg[len(MIDIA):])
            if msg.startswith(APPS):
                apps = msg.split('MR', 1)[1].strip()
            if msg.startswith(MR):
                ger = msg.split(': ', 1)[-1]
                b['mrs'].append({'gerada': ger, 'gerada_dh': dh(ger), 'lida': t, 'apps': apps, 'modo': modo}); apps = None
        blocos.append(b)
    return blocos


def explica_sem_1t(blocos, u1, u2):
    e = []
    if u1 is not None and u2 is not None and u1 != u2:
        e.append(f'urna do 1º turno no bweb ({u1}) diferente da do 2º ({u2}): troca entre os turnos')
    c2 = sorted({t.strftime('%d/%m/%Y') for b in blocos for t, m in b['modo_carga'] if 'contingência' in m and t >= INICIO_2T})
    if c2:
        e.append('carregada como urna de contingência no período do 2º turno em ' + ','.join(c2))
    nota = None
    c1 = sorted({t.strftime('%d/%m/%Y') for b in blocos for t, m in b['modo_carga'] if 'contingência' in m and t < INICIO_2T})
    if c1 and not c2:
        nota = 'foi urna de contingência (reserva) em ' + ','.join(c1) + ', depois recarregada para votação'
    return e, nota


def explica_midia(blocos):
    m = collections.defaultdict(set)
    for b in blocos:
        for d, s in b['midias'].items():
            m[d] |= s
    m1 = m['03/10/2026'] | m['04/10/2026']; m24, m25 = m['24/10/2026'], m['25/10/2026']; m2 = m24 | m25
    if not m1 or not m2:
        return ['SEM EXPLICACAO: sem leitura de mídia na véspera nem no dia de um dos turnos']
    novas = m2 - m1
    if not novas:
        dias = [d for d, s in (('03/10', m['03/10/2026']), ('04/10', m['04/10/2026']), ('24/10', m24), ('25/10', m25)) if s]
        return ['mesma mídia nos dois turnos; leituras em ' + ', '.join(dias) + ' (urna ligada na véspera quando falta o dia)']
    cmv = sorted({t.strftime('%d/%m/%Y %H:%M') for b in blocos for t in b['contingencia_mv'] if t.date() >= datetime.date(2026, 10, 24)})
    if cmv:
        return [f'mídia nova ({len(novas)}) com contingência de mídia de votação em ' + ','.join(cmv)]
    return ['SEM EXPLICACAO: mídia nova sem contingência de mídia de votação']


def explica_mr(blocos, fora, u1, u2):
    e = []
    for g in fora:
        lid = [(i, r) for i, b in enumerate(blocos) for r in b['mrs'] if r['gerada'] == g]
        if not lid:
            e.append(f'SEM EXPLICACAO: MR de {g[:10]} sem leitura no log'); continue
        apps = {r['apps'] for _, r in lid}
        if all(a and 'VOTA' not in a for a in apps):
            e.append(f'MR de {g[:10]} só de aplicativos {sorted(apps)}, sem o aplicativo de votação'); continue
        gdh = lid[0][1]['gerada_dh']
        cont = [r for _, r in lid if r['modo'] and 'contingência' in r['modo'] and r['lida'] >= INICIO_2T]
        if cont:
            e.append(f'MR de {g[:10]} lida numa carga de urna de contingência do 2º turno ({cont[0]["lida"]:%d/%m %H:%M})'); continue
        i0, r0 = min(lid, key=lambda x: x[1]['lida'])
        sc = [t for t in blocos[i0]['carga_scue'] if gdh and gdh <= t <= r0['lida']]
        if sc:
            txt = f'MR de {g[:10]} lida depois de carga nova da urna no mesmo bloco ({sc[0]:%d/%m %H:%M})'
            if u1 is not None and u2 is not None and u1 != u2:
                txt += ', urna trocada entre os turnos'
            e.append(txt); continue
        rec = [t for t in blocos[i0]['recuperador'] if gdh and gdh <= t <= r0['lida']]
        if rec:
            e.append(f'MR de {g[:10]} com recuperador de dados no mesmo bloco antes da leitura'); continue
        e.append(f'SEM EXPLICACAO: MR de {g[:10]} com {sorted(map(str, apps))}')
    return e


def main():
    pasta, t10, base1, amostra = sys.argv[1:5]
    por = json.load(open(t10))['por_urna']
    d1 = carregar(base1); am = carregar(amostra)
    linhas = []
    for k, v in sorted(por.items()):
        tipos = []
        if v['tem_1t_no_log'] and (v['midia_1t'] != v['midia_2t'] or not v['midia_1t'] or not v['midia_2t']):
            tipos.append('midia_diferente')
        if not v['tem_1t_no_log']: tipos.append('sem_1t_no_log')
        fora = [m for m in v['mr'] if not (m[3:10] == '10/2026' and 10 <= int(m[:2]) <= 15)]
        if fora: tipos.append('mr_fora')
        if not tipos:
            continue
        p = os.path.join(pasta, k)
        lg = sorted(f for f in os.listdir(p) if f.endswith('-log.jez'))
        blocos = ler(os.path.join(p, lg[-1]))
        uf, mun, zona, sec = k.split('/')
        chave = f'{uf.upper()}|{int(mun)}|{int(zona)}|{int(sec)}'
        u1 = d1.get(chave, {}).get('1', {}).get('urna'); u2 = am.get(chave, {}).get('2', {}).get('urna')
        expl = {}; notas = []
        if 'sem_1t_no_log' in tipos:
            expl['sem_1t_no_log'], nota = explica_sem_1t(blocos, u1, u2)
            if nota: notas.append(nota)
        if 'midia_diferente' in tipos:
            expl['midia_diferente'] = explica_midia(blocos)
        if 'mr_fora' in tipos:
            expl['mr_fora'] = explica_mr(blocos, fora, u1, u2)
        ok = all(expl[t] and not any(x.startswith('SEM EXPLICACAO') for x in expl[t]) for t in tipos)
        linhas.append({'secao': k, 'pendencias': tipos, 'explicacao': expl, 'notas': notas, 'explicada': ok,
                       'urna_1t_bweb': u1, 'urna_2t_bu': u2, 'blocos_de_log': len(blocos)})
    pres = collections.Counter(); gov = collections.defaultdict(collections.Counter)
    for k, v in am.items():
        s = v.get('2')
        if s:
            for n in s.get('cand', {}):
                pres[n] += 1
        g = v.get('2g')
        if g:
            for n in g.get('cand', {}):
                gov[k.split('|')[0]][n] += 1
    cont = collections.Counter(t for x in linhas for t in x['pendencias'])
    out = {'pendencias': len(linhas), 'por_tipo': dict(cont), 'explicadas': sum(x['explicada'] for x in linhas),
           'nao_explicadas': [x['secao'] for x in linhas if not x['explicada']], 'detalhe': linhas,
           'votaveis_presidente_nos_boletins': dict(pres), 'votaveis_governador_por_uf': {u: dict(c) for u, c in gov.items()},
           'secoes_2t_na_amostra': sum('2' in v for v in am.values())}
    print(json.dumps(out, ensure_ascii=False, indent=1, default=str))


if __name__ == '__main__':
    main()
