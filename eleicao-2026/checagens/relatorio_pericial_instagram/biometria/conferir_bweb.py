"""Conferência independente (código novo, sem a lib do projeto) do campo QT_ELEI_BIOM_SEM_HABILITACAO e da margem.

Lê TODOS os zips do bweb do 2º turno de 2026 (só linhas de Presidente) e soma, por seção única:
NH (QT_ELEI_BIOM_SEM_HABILITACAO), comparecimento, votos 13 e 22, brancos e nulos.
Compara seção a seção com o cache do T21 (nh_secoes_2026.json.gz) e com a base secoes2026.json.gz.
Do 1º turno (4,8 GB) lê só AC, AP, RR e SE e compara NH com o cache.

Uso: python3 -I conferir_bweb.py <zips2t> <zips1t> <cache_t21> <base2026> <saida.json>
"""
import csv, glob, gzip, io, json, os, sys, zipfile, collections


def ler(zpath):
    z = zipfile.ZipFile(zpath)
    nome = [n for n in z.namelist() if n.lower().endswith('.csv')][0]
    sec = {}
    incons = 0
    with z.open(nome) as fh:
        tf = io.TextIOWrapper(fh, encoding='latin1', newline='')
        rd = csv.reader(tf, delimiter=';')
        cab = [c.strip() for c in next(rd)]
        ix = {c: i for i, c in enumerate(cab)}
        g = lambda r, c: r[ix[c]]
        for r in rd:
            if r[ix['CD_CARGO_PERGUNTA']] != '1':
                continue
            k = f"{g(r,'SG_UF')}|{int(g(r,'CD_MUNICIPIO'))}|{int(g(r,'NR_ZONA'))}|{int(g(r,'NR_SECAO'))}"
            nh = int(g(r, 'QT_ELEI_BIOM_SEM_HABILITACAO'))
            comp = int(g(r, 'QT_COMPARECIMENTO'))
            s = sec.get(k)
            if s is None:
                s = sec[k] = {'NH': nh, 'comp': comp, 'L': 0, 'R': 0, 'B': 0, 'N': 0, 'O': 0}
            elif s['NH'] != nh or s['comp'] != comp:
                incons += 1
            tv = g(r, 'DS_TIPO_VOTAVEL'); v = int(g(r, 'QT_VOTOS')); nr = g(r, 'NR_VOTAVEL')
            if tv == 'Nominal' or tv == 'Legenda':
                if nr == '13': s['L'] += v
                elif nr == '22': s['R'] += v
                else: s['O'] += v
            elif tv == 'Branco': s['B'] += v
            elif tv == 'Nulo': s['N'] += v
            else: s['O'] += v
    return sec, incons


def main():
    z2, z1, cache_p, base_p, out_p = sys.argv[1:6]
    tot = collections.Counter(); por_uf = collections.defaultdict(collections.Counter)
    sec2 = {}; incons = 0
    for zp in sorted(glob.glob(os.path.join(z2, '*.zip'))):
        s, inc = ler(zp); incons += inc
        sec2.update(s)
        print('2T', os.path.basename(zp), len(s), flush=True)
    for k, s in sec2.items():
        uf = k.split('|')[0]
        for c in ('NH', 'comp', 'L', 'R', 'B', 'N', 'O'):
            tot[c] += s[c]; por_uf[uf][c] += s[c]
    tot['secoes'] = len(sec2)
    cache = json.load(gzip.open(cache_p, 'rt'))
    dif_cache2 = sum(1 for k, s in sec2.items() if k not in cache['2'] or cache['2'][k][3] != s['NH'] or cache['2'][k][1] != s['comp'])
    base = json.load(gzip.open(base_p, 'rt'))
    dif_base2 = collections.Counter()
    for k, s in sec2.items():
        b = base.get(k, {}).get('2')
        if b is None:
            dif_base2['ausente'] += 1; continue
        for c in ('comp', 'L', 'R', 'B', 'N'):
            if b[c] != s[c]:
                dif_base2[c] += 1
    del base
    # 1º turno, UFs pequenas
    conf1 = {}
    for uf in ('AC', 'AP', 'RR', 'SE'):
        zp = glob.glob(os.path.join(z1, f'bweb_1t_{uf}_*.zip'))[0]
        s, inc = ler(zp)
        d = sum(1 for k, v in s.items() if k not in cache['1'] or cache['1'][k][3] != v['NH'])
        conf1[uf] = {'secoes': len(s), 'NH': sum(v['NH'] for v in s.values()), 'NH_cache': sum(cache['1'][k][3] for k in s if k in cache['1']),
                     'secoes_diferentes_do_cache': d, 'linhas_inconsistentes': inc}
        print('1T', uf, conf1[uf], flush=True)
    out = {'turno2_total': dict(tot), 'turno2_por_uf': {u: dict(c) for u, c in sorted(por_uf.items())},
           'margem_L_menos_R': tot['L'] - tot['R'], 'pct_NH_do_comparecimento_total': 100 * tot['NH'] / tot['comp'],
           'pct_NH_do_comparecimento_27UF': 100 * (tot['NH'] - por_uf['ZZ']['NH']) / (tot['comp'] - por_uf['ZZ']['comp']),
           'razao_NH_sobre_margem': tot['NH'] / (tot['L'] - tot['R']),
           'linhas_inconsistentes_2t': incons, 'secoes_2t_diferentes_do_cache_T21': dif_cache2,
           'secoes_2t_diferentes_da_base': dict(dif_base2), 'turno1_ufs_pequenas': conf1}
    json.dump(out, open(out_p, 'w'), indent=1, ensure_ascii=False)
    print(json.dumps({k: v for k, v in out.items() if k != 'turno2_por_uf'}, indent=1, ensure_ascii=False))


if __name__ == '__main__':
    main()
