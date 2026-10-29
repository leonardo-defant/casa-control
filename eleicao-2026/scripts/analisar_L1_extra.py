"""Conferência extra do L1 (fora do registro): arquivos de urna das seções que o L1 deixou sem explicação.

Seções: as 18 do 2º turno com horário impossível sem explicação no L1, mais MG|41882|320|185 (encerrou às 23h04,
apontada pela conferência do L1) e BA|33073|74|241 (abriu às 10h14 com urna trocada, apontada na mesma conferência).
Para cada uma: boletim decodificado contra o bweb (votos de Lula e Flávio, comparecimento), assinatura (saída do
verificar_assinaturas.py), e no log do dia: hora em que a urna foi ligada, zerésima, urna pronta, primeiro e último
voto, votos por hora, votos depois das 17h e das 19h, encerramento, geração do bu.dat, desligamentos, erros e
contingência. Horas do log no relógio da urna (hora local).
Uso: python3 -I analisar_L1_extra.py <pasta_arquivos> <secoes2026_2t.json.gz> <saida_assinaturas.json> <saida.json>
"""
import os as _os, sys as _sys
_sys.path.insert(0, _os.path.dirname(_os.path.abspath(__file__)))
import collections, glob, gzip, json, re, sys
from decodificar import ler_bu, bu_para_secao, _linhas_log

DATA = '25/10/2026'
RX = re.compile(r'(\d\d/\d\d/\d{4}) (\d\d):(\d\d):(\d\d)')


def seg(h):
    return int(h[0:2]) * 3600 + int(h[3:5]) * 60 + int(h[6:8])


def hms(s):
    return None if s is None else f'{s // 3600:02d}:{s % 3600 // 60:02d}:{s % 60:02d}'


def eventos(caminho):
    ev = []
    for i, bloco in enumerate(_linhas_log(caminho)):
        for l in bloco:
            p = l.split('\t')
            if len(p) < 5 or not p[0].startswith(DATA):
                continue
            m = RX.match(p[0])
            if m:
                ev.append((i, seg(p[0][11:19]), p[1], p[3], p[4]))
    return ev


def resumo_log(ev):
    def primeiro(f):
        x = [t for b, t, n, a, m in ev if f(m)]
        return x[0] if x else None

    def ultimo(f):
        x = [t for b, t, n, a, m in ev if f(m)]
        return x[-1] if x else None
    votos = [t for b, t, n, a, m in ev if m == 'O voto do eleitor foi computado']
    por_hora = collections.Counter(f'{t // 3600:02d}h' for t in votos)
    ligada = [m for b, t, n, a, m in ev if m.startswith('Urna ligada em')]
    return {
        'blocos_de_log': len({b for b, *_ in ev}),
        'urna_ligada': ligada[0][len('Urna ligada em '):] if ligada else None,
        'vezes_ligada': len(ligada),
        'desligada_pela_chave': sum(1 for *_, m in ev if m == 'Urna desligada pela chave'),
        'zeresima': hms(primeiro(lambda m: m.startswith('Imprimindo relatório [ZERÉSIMA]'))),
        'pronta': hms(primeiro(lambda m: m == 'Urna pronta para receber votos')),
        'primeiro_voto': hms(votos[0] if votos else None),
        'ultimo_voto': hms(votos[-1] if votos else None),
        'votos_log': len(votos),
        'votos_por_hora': dict(sorted(por_hora.items())),
        'votos_depois_17h': sum(1 for t in votos if t >= 17 * 3600),
        'votos_depois_19h': sum(1 for t in votos if t >= 19 * 3600),
        'encerrar_selecionado': hms(ultimo(lambda m: m == 'Operador selecionou: Encerrar votação')),
        'inicio_encerramento': hms(ultimo(lambda m: m.startswith('Inicio do Encerramento') or m.startswith('Início do Encerramento'))),
        'bu_dat_gerado': hms(ultimo(lambda m: m == 'Gerando arquivo de resultado [bu.dat] + [Término]')),
        'erros': [f'{hms(t)} {m}' for b, t, n, a, m in ev if n == 'ERRO'][:12],
        'contingencia': [f'{hms(t)} {m}' for b, t, n, a, m in ev if 'ontingência' in m][:6],
        'modo_de_carga': sorted({m for *_, m in ev if m.startswith('Modo de carga da UE')}),
        'habilitados': sum(1 for *_, m in ev if m == 'Eleitor foi habilitado'),
    }


def main():
    pasta, base_arq, assin_arq, saida = sys.argv[1:5]
    base = json.load(gzip.open(base_arq))
    t = open(assin_arq).read()
    assin = json.loads(t[t.find('{'):])
    out = {'assinaturas': {'contagem': assin.get('contagem'), 'falhas': assin.get('falhas')}, 'secoes': {}}
    for d in sorted(glob.glob(f'{pasta}/*/*/*/*')):
        uf, m5, z4, s4 = d.split('/')[-4:]
        k = f'{uf.upper()}|{int(m5)}|{int(z4)}|{int(s4)}'
        bu = glob.glob(f'{d}/*-bu.dat'); lg = glob.glob(f'{d}/*-log.jez')
        r = {}
        if bu:
            s, g = bu_para_secao(ler_bu(bu[0]))
            b = base.get(k, {}).get('2', {})
            r['bu'] = {x: s[x] for x in ('urna', 'apt', 'comp', 'L', 'R', 'B', 'N', 'ab', 'enc')}
            r['bweb'] = {x: b.get(x) for x in ('urna', 'apt', 'comp', 'L', 'R', 'B', 'N', 'ab', 'enc')}
            r['bu_igual_bweb'] = all(s[x] == b.get(x) for x in ('urna', 'apt', 'comp', 'L', 'R', 'B', 'N'))
        if lg:
            r['log'] = resumo_log(eventos(lg[0]))
            if bu:
                r['votos_log_igual_comparecimento'] = r['log']['votos_log'] == r['bu']['comp']
        out['secoes'][k] = r
    json.dump(out, open(saida, 'w'), ensure_ascii=False, indent=1)
    for k, r in out['secoes'].items():
        lg = r.get('log', {})
        print(k, '| BU=bweb' if r.get('bu_igual_bweb') else '| BU DIFERE', f"| L {r['bu']['L']} R {r['bu']['R']} comp {r['bu']['comp']}",
              f"| ligada {lg.get('urna_ligada')} x{lg.get('vezes_ligada')} | pronta {lg.get('pronta')} | votos {lg.get('primeiro_voto')}-{lg.get('ultimo_voto')}",
              f"| >17h {lg.get('votos_depois_17h')} >19h {lg.get('votos_depois_19h')} | enc {lg.get('inicio_encerramento')} | bu {lg.get('bu_dat_gerado')}",
              f"| log=comp {r.get('votos_log_igual_comparecimento')} | erros {len(lg.get('erros', []))} | {lg.get('modo_de_carga')}")


if __name__ == '__main__':
    main()
