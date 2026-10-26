"""T36 do pré-registro (Adendo 16): nulos atribuídos por suspensão no log contra os nulos do boletim, por seção e turno.
Uso: python3 -I analisar_nulo_suspensao.py <pasta_arquivos_2t> <secoes2026.json.gz> <saida.json>
A pasta tem uf/mun/zona/secao/ com o -log.jez (o pacote do 2º turno traz também o log do 1º turno da mesma urna).
"""
import os as _os, sys as _sys
_sys.path.insert(0, _os.path.dirname(_os.path.abspath(__file__)))
import collections, json, os, sys
from decodificar import _linhas_log
from lib import carregar

DIAS = {'1': '04/10/2026', '2': '25/10/2026'}
MSG = 'Atribuido voto nulo por suspensão [Presidente]'


def main():
    pasta, base, saida = sys.argv[1:4]
    d = carregar(base); out = {'secoes_com_log': 0}; por = []
    for uf in sorted(os.listdir(pasta)):
        for m in sorted(os.listdir(os.path.join(pasta, uf))):
            for z in sorted(os.listdir(os.path.join(pasta, uf, m))):
                for s in sorted(os.listdir(os.path.join(pasta, uf, m, z))):
                    p = os.path.join(pasta, uf, m, z, s); k = f'{uf.upper()}|{int(m)}|{int(z)}|{int(s)}'
                    logs = [f for f in os.listdir(p) if f.endswith('-log.jez')]
                    if not logs or k not in d:
                        continue
                    out['secoes_com_log'] += 1
                    cont = collections.Counter(); urnas = set()
                    for f in logs:
                        for bloco in _linhas_log(os.path.join(p, f)):
                            for l in bloco:
                                q = l.split('\t')
                                if len(q) < 5:
                                    continue
                                for t, dia in DIAS.items():
                                    if q[0].startswith(dia):
                                        if q[4] == MSG:
                                            cont[t] += 1
                                        if q[3] == 'VOTA':
                                            urnas.add((t, q[2]))
                    for t in DIAS:
                        if t in d[k]:
                            por.append({'k': k, 't': t, 'S': cont[t], 'N': d[k][t]['N'], 'B': d[k][t]['B'],
                                        'urnas_no_log': len({u for tt, u in urnas if tt == t})})
    for t in DIAS:
        r = [x for x in por if x['t'] == t]
        com = [x for x in r if x['S'] >= 1]
        viol = [x for x in com if x['N'] < x['S']]
        out[t] = {'secoes': len(r), 'secoes_com_S': len(com), 'eventos_S': sum(x['S'] for x in r),
                  'nulos_N_nas_secoes_com_S': sum(x['N'] for x in com), 'violacoes_N_menor_que_S': viol,
                  'N_igual_S': sum(1 for x in com if x['N'] == x['S']),
                  'distribuicao_N_menos_S': dict(sorted(collections.Counter(min(x['N'] - x['S'], 10) for x in com).items()))}
    out['veredito_2t'] = ('SINAL (conferir à mão)' if out['2']['violacoes_N_menor_que_S'] else
                          'SEM SINAL' if out['2']['secoes_com_S'] >= 100 else 'SEM PODER (menos de 100 seções com S)')
    json.dump(out, open(saida, 'w'), ensure_ascii=False, indent=1)
    print(json.dumps({t: {k: v for k, v in out[t].items() if k != 'violacoes_N_menor_que_S'} | {'n_violacoes': len(out[t]['violacoes_N_menor_que_S'])} for t in DIAS}, ensure_ascii=False, indent=1))
    print(out['veredito_2t'])


if __name__ == '__main__':
    main()
