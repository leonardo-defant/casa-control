"""Conferência PAINEL, passo 4: refazer, com os dados da própria Tabela Mestra v21 do painel, os números do reel.

Uso: python3 -I p4_tabela_numeros.py <Painel_Tabela_Mestra_Auditoria_v21.html.gz> <secoes2026.json.gz> <saida.json>

A tabela do painel é lida como TEXTO (bloco <script id="raw-data" type="text/plain">, 40 campos por linha, nomes dos
campos no comentário do próprio arquivo). Nada do site é executado.

Decisões fixadas antes de calcular (desvios, porque o Adendo 24 não fixa nada para o painel):
  E1. Campos: 0 uf_id, 1 mun_id, 2 zona, 3 secao, 4 nr_local, 5 loc_id, 6 mod_id, 7 par, 8 c1, 9 c2, 10 v13_2, 11 v22_2,
      12 p13_1, 13 p13_2, 14 swing_13, 15 esc_norm_m, 16 desv_esc, 17 b1, 18 b2, 19 dbio, 20 t1_2, 21 t4_2, 22 cm2,
      23 sm1, 24 sm2, 25 na2, 26 dn2, 27 max_bl, 28 q_bl10, 29 v_bl10, 30 sens_id, 31..37 cronometria, 38 f_mask,
      39 score (lista do comentário do arquivo). Campo vazio = ausente.
  E2. "Sem biometria" da seção (SemBio) testado em três leituras: c2 - b2; t4_2 + (c2 - b2 - t4_2) (igual); e
      cm2 + sm2 (só liberação manual). A faixa usa SemBio / c2, com cortes 5 e 10; testo os dois lados de cada corte
      (<= e <) e fico com o que reproduzir as contagens de urnas do painel (45.615 / 175.917 / 271.456).
  E3. Universo de 492.988: testo filtros simples (par = 1; p13_1 presente; c1 > 0; b1 presente) e registro qual bate.
  E4. Comparação com a base oficial (secoes2026.json.gz, chave UF, zona, seção): c2 contra comp do 2º turno,
      v13_2 contra L, v22_2 contra R, c1 contra comp do 1º turno, nr_local contra loc.
  E5. Margem = v13_2 - v22_2 (votos de Lula menos de Flávio). Fatia de Lula = v13 / (v13 + v22).
"""
import gzip
import json
import re
import sys
from collections import Counter, defaultdict


def ler_tabela(cam):
    src = gzip.open(cam, 'rb').read().decode('utf-8', errors='replace')
    m = re.search(r'<script id="raw-data" type="text/plain">', src)
    fim = src.find('</script>', m.end())
    corpo = src[m.end():fim].strip('\n')
    i = src.find('const DICT = ') + len('const DICT = ')
    dicio, _ = json.JSONDecoder().raw_decode(src, i)
    linhas = []
    for ln in corpo.split('\n'):
        p = ln.strip().split(',')
        if len(p) != 40:
            continue
        linhas.append([None if x == '' else (float(x) if ('.' in x or 'e' in x) else int(x)) for x in p])
    return linhas, dicio


def main():
    tab, D = ler_tabela(sys.argv[1])
    base = json.load(gzip.open(sys.argv[2]))
    R = {}
    R['n_linhas'] = len(tab)
    R['n_par'] = sum(1 for r in tab if r[7] == 1)
    nomes = {8: 'c1', 9: 'c2', 10: 'v13_2', 11: 'v22_2', 17: 'b1', 18: 'b2', 20: 't1_2', 21: 't4_2', 22: 'cm2',
             23: 'sm1', 24: 'sm2', 25: 'na2', 26: 'dn2', 29: 'v_bl10', 37: 'susp2'}
    R['somas'] = {v: sum((r[k] or 0) for r in tab) for k, v in nomes.items()}
    R['ausentes'] = {v: sum(1 for r in tab if r[k] is None) for k, v in list(nomes.items()) + [(12, 'p13_1'), (13, 'p13_2'), (15, 'esc'), (16, 'desv')]}
    R['sm2_igual_na2_mais_dn2'] = sum(1 for r in tab if (r[24] or 0) == (r[25] or 0) + (r[26] or 0))
    R['sm2_maior_na2_mais_dn2'] = sum(1 for r in tab if (r[24] or 0) > (r[25] or 0) + (r[26] or 0))
    R['t4_2_igual_cm2_mais_sm2'] = sum(1 for r in tab if (r[21] or 0) == (r[22] or 0) + (r[24] or 0))
    R['margem_total'] = R['somas']['v13_2'] - R['somas']['v22_2']
    R['c2_menos_b2'] = R['somas']['c2'] - R['somas']['b2']
    R['c1_menos_b1'] = R['somas']['c1'] - R['somas']['b1']
    R['c2_menos_b2_menos_t4_2'] = R['c2_menos_b2'] - R['somas']['t4_2']
    R['c2_menos_b2_menos_cm2_sm2'] = R['c2_menos_b2'] - R['somas']['cm2'] - R['somas']['sm2']

    # faixas (E2, E3)
    def faixas(filtro, semb, le5, le10):
        out = defaultdict(lambda: [0, 0, 0, 0])
        for r in tab:
            if not filtro(r):
                continue
            c2 = r[9] or 0
            if c2 <= 0:
                continue
            f = 100.0 * semb(r) / c2
            a = (f <= 5) if le5 else (f < 5)
            b = (f <= 10) if le10 else (f < 10)
            k = 'A' if a else ('B' if b else 'C')
            o = out[k]
            o[0] += 1
            o[1] += r[10] or 0
            o[2] += r[11] or 0
            o[3] += semb(r)
        return {k: {'urnas': v[0], 'L': v[1], 'F': v[2], 'margem': v[1] - v[2],
                    'pctL': round(100.0 * v[1] / (v[1] + v[2]), 2), 'semb': v[3]} for k, v in sorted(out.items())}

    filtros = {
        'todas': lambda r: True,
        'par1': lambda r: r[7] == 1,
        'p13_1_presente': lambda r: r[12] is not None,
        'b1_presente': lambda r: r[17] is not None,
        'c1_pos': lambda r: (r[8] or 0) > 0,
        'esc_presente': lambda r: r[15] is not None,
    }
    semb = {
        'c2_menos_b2': lambda r: (r[9] or 0) - (r[18] or 0),
        'cm2_mais_sm2': lambda r: (r[22] or 0) + (r[24] or 0),
        't4_2': lambda r: (r[21] or 0),
    }
    alvo = {'A': 45615, 'B': 175917, 'C': 271456}
    R['faixas'] = {}
    for fn, f in filtros.items():
        R['faixas'][fn] = {'n': sum(1 for r in tab if f(r))}
        for sn, s in semb.items():
            for le5 in (True, False):
                for le10 in (True, False):
                    fx = faixas(f, s, le5, le10)
                    chave = '%s|%s|%s' % (sn, '<=5' if le5 else '<5', '<=10' if le10 else '<10')
                    bate = all(fx.get(k, {}).get('urnas') == v for k, v in alvo.items())
                    R['faixas'][fn][chave] = {'bate_urnas': bate, 'fx': fx}

    # comparação com a base oficial (E4)
    idx = {}
    for k, v in base.items():
        uf, mun, z, s = k.split('|')
        idx[(uf, int(z), int(s))] = (k, v)
    n27 = sum(1 for k, v in base.items() if k.split('|')[0] != 'ZZ' and '2' in v)
    R['base_secoes_27uf_com_2t'] = n27
    dif = Counter()
    exemplos = defaultdict(list)
    achadas = set()
    for r in tab:
        uf = D['ufs'][r[0]]
        key = (uf, r[2], r[3])
        if key not in idx:
            dif['sem_par_na_base'] += 1
            if len(exemplos['sem_par_na_base']) < 5:
                exemplos['sem_par_na_base'].append([uf, D['muns'][r[1]], r[2], r[3]])
            continue
        achadas.add(key)
        k, v = idx[key]
        s2 = v.get('2', {})
        s1 = v.get('1', {})
        for nome, a, b in (('c2', r[9], s2.get('comp')), ('L', r[10], s2.get('L')), ('R', r[11], s2.get('R')),
                           ('c1', r[8], s1.get('comp')), ('loc', r[4], s2.get('loc'))):
            if a != b:
                dif[nome] += 1
                if len(exemplos[nome]) < 5:
                    exemplos[nome].append([k, a, b])
    faltam = [k for k, v in base.items() if k.split('|')[0] != 'ZZ' and '2' in v
              and (k.split('|')[0], int(k.split('|')[2]), int(k.split('|')[3])) not in achadas]
    R['comparacao_base'] = {'diferencas': dict(dif), 'exemplos': dict(exemplos), 'n_faltam_na_tabela': len(faltam),
                            'faltam_exemplos': faltam[:15]}
    L27 = sum(v['2']['L'] for k, v in base.items() if k.split('|')[0] != 'ZZ' and '2' in v)
    F27 = sum(v['2']['R'] for k, v in base.items() if k.split('|')[0] != 'ZZ' and '2' in v)
    C27 = sum(v['2']['comp'] for k, v in base.items() if k.split('|')[0] != 'ZZ' and '2' in v)
    R['base_27uf'] = {'L': L27, 'F': F27, 'margem': L27 - F27, 'comp': C27}
    json.dump(R, open(sys.argv[3], 'w'), ensure_ascii=False, indent=1)
    print(json.dumps({k: v for k, v in R.items() if k != 'faixas'}, ensure_ascii=False, indent=1))
    for fn, d in R['faixas'].items():
        for ch, x in d.items():
            if ch != 'n' and x['bate_urnas']:
                print('BATE', fn, d['n'], ch, json.dumps(x['fx'], ensure_ascii=False))


if __name__ == '__main__':
    main()
