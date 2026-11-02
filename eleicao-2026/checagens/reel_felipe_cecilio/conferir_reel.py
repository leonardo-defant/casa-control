"""Checagem do reel de Felipe Cecílio (28/10/2026): comparecimento entre os turnos e ritmo de votação nas seções.

(1) Comparecimento e válidos nos dois turnos de 2026, pela base por seção (bweb), com e sem o exterior.
(2) Seções em que o comparecimento caiu, ficou igual ou subiu do 1º para o 2º turno.
(3) Cenário extremo: margem de Lula se todo o comparecimento a mais tivesse sido voto dele.
(4) Ritmo nas urnas da amostra de logs (a mesma urna nos dois turnos): duração mediana da habilitação ao voto,
    votos por hora no pico e minutos de urna parada entre eleitores, 1º turno (04/10) contra 2º turno (25/10).
Uso: python3 -I conferir_reel.py <secoes2026.json.gz> <pasta_arq_amostra> <saida.json>
"""
import os as _os, sys as _sys
_sys.path.insert(0, _os.path.join(_os.path.dirname(_os.path.abspath(__file__)), '..', '..', 'scripts'))
import collections, glob, gzip, json, re, statistics, sys
from decodificar import _linhas_log

RX = re.compile(r'(\d\d/\d\d/\d{4}) (\d\d):(\d\d):(\d\d)')


def ritmo(blocos, data):
    hab = None; dur = []; votos = []
    for b in blocos:
        for l in b:
            p = l.split('\t')
            if len(p) < 5 or not p[0].startswith(data):
                continue
            m = RX.match(p[0])
            if not m:
                continue
            t = int(m.group(2)) * 3600 + int(m.group(3)) * 60 + int(m.group(4))
            if p[4] == 'Eleitor foi habilitado':
                hab = t
            elif p[4] == 'O voto do eleitor foi computado':
                votos.append(t)
                if hab is not None:
                    dur.append(t - hab)
                hab = None
    if not votos:
        return None
    votos.sort()
    por_hora = collections.Counter(t // 3600 for t in votos)
    gaps = [votos[i] - votos[i - 1] for i in range(1, len(votos))]
    return {'votos': len(votos), 'dur_mediana_s': statistics.median(dur) if dur else None,
            'pico_votos_hora': max(por_hora.values()), 'gap_mediano_s': statistics.median(gaps) if gaps else None}


def main():
    base = json.load(gzip.open(sys.argv[1]))
    out = {}
    for rotulo, filtro in (('brasil_e_exterior', lambda k: True), ('so_brasil', lambda k: not k.startswith('ZZ|'))):
        c = collections.Counter()
        for k, s in base.items():
            if not filtro(k):
                continue
            for t in ('1', '2'):
                if t in s:
                    c['comp' + t] += s[t]['comp']; c['apt' + t] += s[t]['apt']
                    c['val' + t] += s[t]['L'] + s[t]['R'] + s[t].get('O', 0)
                    c['bn' + t] += s[t]['B'] + s[t]['N']
        c['dif_comp'] = c['comp2'] - c['comp1']; c['dif_val'] = c['val2'] - c['val1']
        c['abst1_pct'] = round(100 - 100 * c['comp1'] / c['apt1'], 2); c['abst2_pct'] = round(100 - 100 * c['comp2'] / c['apt2'], 2)
        out[rotulo] = dict(c)
    ambos = [(s['1'], s['2']) for k, s in base.items() if '1' in s and '2' in s and not k.startswith('ZZ|') and s['1']['apt'] > 0]
    caiu = sum(1 for a, b in ambos if b['comp'] < a['comp']); igual = sum(1 for a, b in ambos if b['comp'] == a['comp'])
    caiu5 = sum(1 for a, b in ambos if b['comp'] < 0.95 * a['comp'])
    out['secoes'] = {'n': len(ambos), 'comparecimento_caiu': caiu, 'igual': igual, 'subiu': len(ambos) - caiu - igual,
                     'caiu_mais_de_5pct': caiu5, 'pct_caiu': round(100 * caiu / len(ambos), 2)}
    L2 = sum(s['2']['L'] for s in base.values() if '2' in s); R2 = sum(s['2']['R'] for s in base.values() if '2' in s)
    out['cenario_extremo'] = {'margem_lula': L2 - R2, 'aumento_comparecimento': out['brasil_e_exterior']['dif_comp'],
                              'margem_sem_nenhum_eleitor_a_mais_supondo_todos_lula': L2 - R2 - out['brasil_e_exterior']['dif_comp']}
    r1 = []; r2 = []
    for f in glob.glob(f'{sys.argv[2]}/*/*/*/*/*-log.jez'):
        try:
            bl = _linhas_log(f)
        except Exception:
            continue
        a = ritmo(bl, '04/10/2026'); b = ritmo(bl, '25/10/2026')
        if a and b:
            r1.append(a); r2.append(b)
    med = lambda xs: statistics.median([x for x in xs if x is not None])
    out['ritmo_amostra'] = {'urnas_com_os_dois_dias': len(r1),
                            'dur_mediana_s': {'1t': med([x['dur_mediana_s'] for x in r1]), '2t': med([x['dur_mediana_s'] for x in r2])},
                            'pico_votos_hora': {'1t': med([x['pico_votos_hora'] for x in r1]), '2t': med([x['pico_votos_hora'] for x in r2])},
                            'gap_mediano_s': {'1t': med([x['gap_mediano_s'] for x in r1]), '2t': med([x['gap_mediano_s'] for x in r2])},
                            'votos_por_urna': {'1t': med([x['votos'] for x in r1]), '2t': med([x['votos'] for x in r2])}}
    json.dump(out, open(sys.argv[3], 'w'), ensure_ascii=False, indent=1)
    print(json.dumps(out, ensure_ascii=False, indent=1))


if __name__ == '__main__':
    main()
