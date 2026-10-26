"""T20 do pré-registro (adendo 9): fechamento das pendências do T10 e identidade dos candidatos nos boletins.

Para cada urna que o T10 deixou em aberto, procura no log completo (inclusive os logs internos de contingência) o
evento que explica a pendência:
  sem o 1º turno no log   -> urna carregada como contingência ou urna diferente da do 1º turno no bweb
  mídia de votação diferente -> mesma mídia quando se olha também a véspera (urna ligada no dia anterior) ou contingência de MV
  MR fora de 10 a 15/10   -> MR só de aplicativos (sem VOTA, ex.: verificação de assinaturas), MR lida no período do
                             1º turno (data da linha até 04/10) ou MR de urna de contingência
Depois confere, em todos os boletins da amostra, que os únicos votáveis de presidente são 13 e 22 e que os de
governador formam o mesmo par dentro de cada UF.
Uso: python3 -I analisar_pendencias.py <pasta_arq_2t> <T10_software.json> <secoes2026_1t.json.gz> <amostra_2t.json.gz>
"""
import os as _os, sys as _sys
_sys.path.insert(0, _os.path.dirname(_os.path.abspath(__file__)))
import collections, json, os, sys
from decodificar import _linhas_log
from lib import carregar

EV = {'carga_contingencia': ('Modo de carga da UE - Urna de contingência', 'Urna de contingência pronta para eleição'),
      'contingencia_executada': ('Contingência executada com sucesso',),
      'contingencia_mv': ('Contingência de MV executada com sucesso', 'Serial da MV nova registrada na MI'),
      'recuperador': ('Iniciando aplicação RECUPERADOR DE DADOS',)}
MIDIA = 'Data e hora da geração da mídia de votação: '
MR = 'Data e hora da geração da MR'


def ordem(d):
    return d[6:10] + d[3:5] + d[:2]


def ler(caminho):
    ev = collections.defaultdict(list); midias = collections.defaultdict(set); mrs = []; apps = None
    for bl in _linhas_log(caminho):
        for l in bl:
            x = l.split('\t')
            if len(x) < 5:
                continue
            dia, msg = x[0][:10], x[4]
            for nome, pref in EV.items():
                if any(msg.startswith(p) for p in pref):
                    ev[nome].append(dia)
            if msg.startswith(MIDIA):
                midias[dia].add(msg[len(MIDIA):])
            if msg.startswith('Aplicativo presente na MR') or msg.startswith('Aplicativos presentes na MR'):
                apps = msg.split('MR', 1)[1].strip()
            if msg.startswith(MR):
                mrs.append((dia, msg.split(': ', 1)[-1], apps)); apps = None
    return ev, midias, mrs


def main():
    pasta, t10, base1, amostra = sys.argv[1:5]
    por = json.load(open(t10))['por_urna']
    d1 = carregar(base1); am = carregar(amostra)
    linhas = []
    for k, v in sorted(por.items()):
        tipos = []
        if v['tem_1t_no_log'] and v['midia_1t'] != v['midia_2t']: tipos.append('midia_diferente')
        if not v['tem_1t_no_log']: tipos.append('sem_1t_no_log')
        fora = [m for m in v['mr'] if not (m[3:10] == '10/2026' and 10 <= int(m[:2]) <= 15)]
        if fora: tipos.append('mr_fora')
        if not tipos:
            continue
        p = os.path.join(pasta, k)
        lg = sorted(f for f in os.listdir(p) if f.endswith('-log.jez'))
        ev, midias, mrs = ler(os.path.join(p, lg[-1]))
        uf, mun, zona, sec = k.split('/')
        chave = f'{uf.upper()}|{int(mun)}|{int(zona)}|{int(sec)}'
        u1 = d1.get(chave, {}).get('1', {}).get('urna'); u2 = am.get(chave, {}).get('2', {}).get('urna')
        expl = {}
        for t in tipos:
            if t == 'sem_1t_no_log':
                e = []
                if ev['carga_contingencia']: e.append('carregada como urna de contingência em ' + ','.join(sorted(set(ev['carga_contingencia']), key=ordem)))
                if u1 is not None and u2 is not None and u1 != u2: e.append(f'urna do 1º turno no bweb ({u1}) diferente da do 2º ({u2})')
                expl[t] = e
            elif t == 'midia_diferente':
                m1 = midias.get('03/10/2026', set()) | midias.get('04/10/2026', set())
                m2 = midias.get('24/10/2026', set()) | midias.get('25/10/2026', set())
                e = []
                if m1 and m1 & m2: e.append('mesma mídia do 1º turno, lida na véspera do 2º turno (urna ligada no dia anterior)')
                if ev['contingencia_mv']: e.append('contingência de mídia de votação em ' + ','.join(sorted(set(ev['contingencia_mv']), key=ordem)))
                expl[t] = e
            elif t == 'mr_fora':
                e = []
                for m in fora:
                    dias = sorted({dia for dia, x, a in mrs if x == m}, key=ordem)
                    ap = {a for dia, x, a in mrs if x == m}
                    if ap and all(a and 'VOTA' not in a for a in ap):
                        e.append(f'MR de {m[:10]} só de aplicativos {sorted(ap)}, sem o aplicativo de votação')
                    elif dias and ordem(dias[0]) <= '20261004':
                        e.append(f'MR de {m[:10]} lida no período do 1º turno ({dias[0]})')
                    elif ev['carga_contingencia'] or ev['contingencia_executada']:
                        e.append(f'MR de {m[:10]} em urna com contingência registrada')
                    elif ev['recuperador']:
                        e.append(f'MR de {m[:10]} com recuperação de dados registrada')
                expl[t] = e if len(e) == len(fora) else e + ['SEM EXPLICACAO para parte das MR']
        linhas.append({'secao': k, 'pendencias': tipos, 'explicacao': expl,
                       'explicada': all(expl[t] and 'SEM EXPLICACAO para parte das MR' not in expl[t] for t in tipos),
                       'urna_1t_bweb': u1, 'urna_2t_bu': u2, 'eventos': {n: sorted(set(d), key=ordem) for n, d in ev.items()}})
    # identidade dos votáveis
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
    out = {'pendencias': len(linhas), 'explicadas': sum(x['explicada'] for x in linhas),
           'nao_explicadas': [x['secao'] for x in linhas if not x['explicada']], 'detalhe': linhas,
           'votaveis_presidente_nos_boletins': dict(pres), 'votaveis_governador_por_uf': {u: dict(c) for u, c in gov.items()},
           'secoes_2t_na_amostra': sum('2' in v for v in am.values())}
    print(json.dumps(out, ensure_ascii=False, indent=1))


if __name__ == '__main__':
    main()
