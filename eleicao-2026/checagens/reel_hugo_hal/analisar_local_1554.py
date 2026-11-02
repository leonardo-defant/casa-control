"""Checagem do reel de @hugo.hal: liberações sem biometria na seção 280 da zona 180 de Lauro de Freitas (BA).

Para cada seção do local 1554 (as 8 seções do prédio), nos dois turnos (o log do 2º turno traz também o dia do
1º turno quando a urna é a mesma): votos computados, habilitações, liberações manuais (pedido de dado pessoal e
"Dado digitado confere"), quem autorizou cada liberação (mesário identificado pela digital; digital nova salva em
arquivo; digital igual a uma gravada depois do registro de mesários), tempo do pedido do dado pessoal até a
confirmação, maior sequência de liberações manuais seguidas, e votos de Lula e Flávio com a virada entre os turnos.
Uso: python3 -I analisar_local_1554.py <pasta_arq> <secoes2026.json.gz> <saida.json>
"""
import os as _os, sys as _sys
_sys.path.insert(0, _os.path.join(_os.path.dirname(_os.path.abspath(__file__)), '..', '..', 'scripts'))
import collections, glob, gzip, json, re, statistics, sys
from decodificar import _linhas_log, ler_bu, bu_para_secao

RX = re.compile(r'(\d\d/\d\d/\d{4}) (\d\d):(\d\d):(\d\d)')


def dia(blocos, data):
    ev = []
    for b in blocos:
        for l in b:
            p = l.split('\t')
            if len(p) >= 5 and p[0].startswith(data):
                m = RX.match(p[0])
                if m:
                    ev.append((int(m.group(2)) * 3600 + int(m.group(3)) * 60 + int(m.group(4)), p[4]))
    if not any(m == 'O voto do eleitor foi computado' for t, m in ev):
        return None
    votos = hab = 0; manual = 0; t_pedido = None; tempos = []
    quem = collections.Counter(); seq = []; atual_manual = False
    for t, m in ev:
        if m == 'Solicitação de dado pessoal do eleitor para habilitação manual':
            t_pedido = t; atual_manual = True
        elif m == 'Dado digitado confere' and t_pedido is not None:
            tempos.append(t - t_pedido); t_pedido = None
        elif m.startswith('Mesário ') and m.endswith('habilitou o eleitor'):
            quem['mesario_identificado'] += 1
        elif m.startswith('Não encontrou digital coletada em nenhum dos arquivos'):
            quem['digital_nova_salva'] += 1
        elif m.startswith('Digital coletada bate com uma digital gravada após o registro inicial de mesário'):
            quem['digital_gravada_no_dia'] += 1
        elif m == 'Eleitor foi habilitado':
            hab += 1
        elif m == 'O voto do eleitor foi computado':
            votos += 1; seq.append(atual_manual); atual_manual = False
    manual = sum(seq)
    maior = cur = 0
    for x in seq:
        cur = cur + 1 if x else 0; maior = max(maior, cur)
    return {'votos': votos, 'habilitados': hab, 'liberacoes_manuais': manual,
            'pct_manual': round(100 * manual / votos, 1), 'quem_autorizou': dict(quem),
            'maior_sequencia_manual': maior,
            'seg_pedido_ate_confere': {'mediana': statistics.median(tempos) if tempos else None,
                                       'min': min(tempos) if tempos else None, 'p90': sorted(tempos)[int(0.9 * len(tempos))] if tempos else None,
                                       'ate_3s': sum(1 for x in tempos if x <= 3), 'n': len(tempos)}}


def main():
    pasta, basef, saida = sys.argv[1:4]
    base = json.load(gzip.open(basef)); out = {}
    for d in sorted(glob.glob(f'{pasta}/*/*/*/*')):
        uf, m5, z4, s4 = d.split('/')[-4:]
        k = f'{uf.upper()}|{int(m5)}|{int(z4)}|{int(s4)}'
        lg = glob.glob(f'{d}/*-log.jez'); bu = glob.glob(f'{d}/*-bu.dat')
        bl = _linhas_log(lg[0])
        s = base[k]; a, b = s['1'], s['2']
        sb, _ = bu_para_secao(ler_bu(bu[0]))
        out[k] = {'urna_1t_2t': [a['urna'], b['urna']], 'comp_1t_2t': [a['comp'], b['comp']], 'aptos': b['apt'],
                  'lula_flavio_1t': [a['L'], a['R']], 'lula_flavio_2t': [b['L'], b['R']],
                  'virada_pts': round(100 * b['L'] / (b['L'] + b['R']) - 100 * a['L'] / (a['L'] + a['R']), 2),
                  'bu_igual_bweb': all(sb[x] == b[x] for x in ('L', 'R', 'B', 'N', 'comp')),
                  '2t': dia(bl, '25/10/2026'), '1t_mesma_urna': dia(bl, '04/10/2026')}
    json.dump(out, open(saida, 'w'), ensure_ascii=False, indent=1)
    for k, v in out.items():
        t2 = v['2t']; t1 = v['1t_mesma_urna']
        print(k, '| virada', v['virada_pts'], '| comp', v['comp_1t_2t'], '| BU=bweb', v['bu_igual_bweb'],
              '| 2T manual', t2['liberacoes_manuais'], f"({t2['pct_manual']}%)", t2['quem_autorizou'], 'seq', t2['maior_sequencia_manual'],
              'tempo', t2['seg_pedido_ate_confere'],
              '| 1T manual', (t1 or {}).get('liberacoes_manuais'), (t1 or {}).get('pct_manual'))


if __name__ == '__main__':
    main()
