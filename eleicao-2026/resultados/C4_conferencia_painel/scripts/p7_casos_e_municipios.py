"""Conferência PAINEL, passo 7: conferir os exemplos que o painel e o dossiê citam (seções e municípios) contra a
Tabela Mestra v21 do próprio painel e contra a base oficial; e a margem do 1º turno por faixa (definição do painel).

Uso: python3 -I p7_casos_e_municipios.py <tabela.html.gz> <secoes2026.json.gz> <saida.json>
Decisões fixadas antes de rodar:
  K1. Seção citada = (UF, zona, seção) como o painel escreve; confiro município e escola pelos nomes da própria
      tabela (DICT) e votos pela base oficial.
  K2. Município citado no dossiê = nome em maiúsculas sem acento comparado ao DICT.muns da tabela, dentro da UF.
      Conto urnas, comparecimento, SemBio = c2 - b2, cm2, dn2, sm2 e fatia de Lula entre os dois.
  K3. Faixas pela definição do painel (SemBio = c2 - b2, cortes <= 5 e <= 10, sobre o comparecimento do 2º turno);
      margem e fatia de Lula do 1º turno nas mesmas seções, pela base oficial.
"""
import gzip
import json
import re
import sys
import unicodedata
from collections import defaultdict


def sem_acento(s):
    return ''.join(c for c in unicodedata.normalize('NFD', s) if unicodedata.category(c) != 'Mn').upper().strip()


SECOES_PAINEL = [  # (rótulo, UF, município como escrito, zona, seção, escola como escrita, extra)
    ('pagina_caso1', 'MA', 'Pedro do Rosário', 15, 350, 'Escola Municipal São José', {'L': 162, 'F': 6}),
    ('pagina_caso2', 'BA', 'Xique-Xique', None, 82, None, {'L': 252, 'F': 65}),
    ('rank2', 'BA', 'Curaçá', 82, 120, 'Colégio Estadual de Curaçá', {}),
    ('rank3', 'BA', 'Salvador', 1, 45, 'Instituto Federal da Bahia', {}),
    ('rank4', 'PI', 'Coronel José Dias', 23, 12, 'Unidade Escolar Maria José', {}),
    ('rank5', 'PA', 'Belém', 2, 555, 'Escola Técnica Federal', {}),
    ('rank6', 'AM', 'Manaus', 31, 210, 'Colégio Militar de Manaus', {}),
    ('rank7', 'CE', 'Fortaleza', 3, 912, 'Escola Estadual Justiniano', {}),
    ('rank8', 'RN', 'Natal', 1, 33, 'Escola Municipal Natal', {}),
    ('dossie_SaoLuis', 'MA', 'São Luís', 2, 97, 'IFMA Campus Monte Castelo', {'c2': 158, 'sb': 152, 'dn': 86, 'pL': 70.1}),
    ('dossie_SaoPaulo', 'SP', 'São Paulo', 392, 40, 'EMEF Dona Jenny Gomes', {'c2': 210, 'sb': 145, 'dn': 80, 'dbio': -88, 'pL': 54.0}),
    ('dossie_NovaIguacu', 'RJ', 'Nova Iguaçu', 158, 48, 'CIEP 021 General Osório', {'sb': 66, 'dn': 33, 'dbio': -23, 'pL': 51.8}),
    ('dossie_GovValadares', 'MG', 'Governador Valadares', 118, 79, 'EE Israel Pinheiro', {'c2': 243, 'sb': 59, 'dn': 55, 'dbio': -9, 'pL': 35.7}),
    ('dossie_MonsenhorPaulo', 'MG', 'Monsenhor Paulo', 61, 27, 'EM Professor João Mestre', {'c2': 257, 'sb': 92, 'dn': 27, 'dbio': -11, 'pL': 51.4}),
    ('dossie_BeloOriente', 'MG', 'Belo Oriente', 176, 156, 'EM José Lagares de Lima', {'c2': 199, 'sb': 54, 'dn': 25, 'dbio': -9, 'pL': 56.2}),
    ('dossie_Teresina', 'PI', 'Teresina', 63, 189, 'EM Centro dos Afonsinhos', {'c2': 276, 'sb': 40, 'dn': 33, 'dbio': 1, 'pL': 90.3}),
]

MUNICIPIOS_DOSSIE = [  # (município, UF, urnas, comp, sembio, commes, orfas, pL)
    ('Monsenhor Paulo', 'MG', 20, 5504, 1551, 238, 89, 49.2), ('Rio Grande', 'RS', 460, 113317, 28860, 5505, 1933, 63.9),
    ('Belo Oriente', 'MG', 70, 15768, 3691, 857, 206, 50.1), ('Itaú de Minas', 'MG', 35, 9703, 1990, 468, 183, 41.5),
    ('Lajedo', 'PE', 91, 27998, 4345, 1579, 309, 69.7), ('Araruama', 'RJ', 325, 85207, 13278, 3536, 973, 35.2),
    ('Nova Iguaçu', 'RJ', 1830, 483076, 74479, 18644, 5050, 41.0), ('Barra Mansa', 'RJ', 452, 107377, 16547, 5272, 1362, 47.6),
    ('Arcoverde', 'PE', 171, 43757, 5444, 2489, 506, 75.1), ('São Paulo', 'SP', 26683, 7284071, 879482, 279856, 80932, 55.5),
    ('Várzea Grande', 'MT', 581, 159751, 18928, 9171, 2211, 42.6), ('São Luís', 'MA', 2273, 638743, 72207, 33360, 10601, 62.1),
    ('Sumaré', 'SP', 579, 159487, 16935, 4850, 1240, 43.4), ('Monte Alto', 'SP', 116, 28759, 2978, 1189, 300, 31.2),
    ('Vitória', 'ES', 799, 221625, 22601, 9228, 2452, 48.2), ('Governador Valadares', 'MG', 661, 152142, 14809, 6409, 1708, 39.6),
    ('Parnamirim', 'RN', 427, 125381, 11908, 4554, 1032, 48.9), ('Medianeira', 'PR', 126, 30827, 2808, 1588, 389, 30.7),
    ('Redenção', 'PA', 205, 49733, 4522, 1719, 285, 28.0), ('Teresina', 'PI', 1843, 510258, 44512, 19636, 4652, 68.0),
    ('Macapá', 'AP', 1027, 251314, 20923, 7556, 1636, 51.0), ('Alvorada', 'TO', 31, 6174, 494, 277, 74, 40.3),
    ('São Caetano do Sul', 'SP', 391, 126104, 9964, 5028, 1542, 41.7), ('Bom Jesus do Oeste', 'SC', 9, 1677, 133, 110, 3, 32.1),
    ('Jundiaí', 'SP', 974, 273936, 20709, 13371, 3409, 38.3), ('Uberlândia', 'MG', 1703, 443275, 33402, 15812, 4319, 47.6),
    ('Queimados', 'RJ', 326, 87195, 6119, 2608, 702, 44.5), ('Campo Grande', 'MS', 2189, 527124, 35342, 20640, 4583, 38.9),
    ('Londrina', 'PR', 1200, 325335, 19504, 13948, 2929, 30.8),
]


def main():
    src = gzip.open(sys.argv[1], 'rb').read().decode('utf-8', errors='replace')
    m = re.search(r'<script id="raw-data" type="text/plain">', src)
    corpo = src[m.end():src.find('</script>', m.end())].strip('\n')
    i = src.find('const DICT = ') + len('const DICT = ')
    D, _ = json.JSONDecoder().raw_decode(src, i)
    base = json.load(gzip.open(sys.argv[2]))
    idx = {}
    for k, v in base.items():
        uf, mun, z, s = k.split('|')
        idx.setdefault((uf, int(s)), []).append((int(z), mun, v))
        idx[(uf, int(z), int(s))] = (mun, v)
    tab = []
    for ln in corpo.split('\n'):
        p = ln.strip().split(',')
        if len(p) != 40:
            continue
        tab.append({'uf': D['ufs'][int(p[0])], 'mun': D['muns'][int(p[1])], 'zona': int(p[2]), 'secao': int(p[3]),
                    'nr_local': int(p[4]), 'escola': D['locs'][int(p[5])], 'c2': int(p[9]), 'L2': int(p[10]),
                    'R2': int(p[11]), 'b2': int(p[18]), 'dbio': int(p[19]), 'cm2': int(p[22]), 'sm2': int(p[24]),
                    'dn2': int(p[26]), 'score': int(p[39])})
    porkey = {(t['uf'], t['zona'], t['secao']): t for t in tab}
    R = {'secoes': {}, 'municipios': {}, 'faixas_1T': {}}
    for rot, uf, mun, z, s, esc, extra in SECOES_PAINEL:
        if z is None:
            cands = [t for t in tab if t['uf'] == uf and sem_acento(t['mun']) == sem_acento(mun) and t['secao'] == s]
        else:
            t = porkey.get((uf, z, s))
            cands = [t] if t else []
        out = []
        for t in cands:
            tot = t['L2'] + t['R2']
            out.append({'mun_tabela': t['mun'], 'zona': t['zona'], 'secao': t['secao'], 'escola_tabela': t['escola'],
                        'c2': t['c2'], 'L2': t['L2'], 'R2': t['R2'], 'pL': round(100 * t['L2'] / tot, 1) if tot else None,
                        'sembio': t['c2'] - t['b2'], 'dn2': t['dn2'], 'sm2': t['sm2'], 'dbio': t['dbio'],
                        'score_0a7': t['score']})
        mesmo_mun = [t for t in tab if t['uf'] == uf and sem_acento(t['mun']) == sem_acento(mun)]
        R['secoes'][rot] = {'citado': {'uf': uf, 'mun': mun, 'zona': z, 'secao': s, 'escola': esc, **extra},
                            'achado': out, 'secoes_do_municipio_na_tabela': len(mesmo_mun),
                            'zonas_do_municipio': sorted({t['zona'] for t in mesmo_mun})[:12],
                            'max_secao_do_municipio': max([t['secao'] for t in mesmo_mun], default=None)}
    for mun, uf, urnas, comp, sb, cm, orf, pl in MUNICIPIOS_DOSSIE:
        ts = [t for t in tab if t['uf'] == uf and sem_acento(t['mun']) == sem_acento(mun)]
        L = sum(t['L2'] for t in ts)
        F = sum(t['R2'] for t in ts)
        R['municipios'][mun + '/' + uf] = {
            'dossie': [urnas, comp, sb, cm, orf, pl],
            'tabela': [len(ts), sum(t['c2'] for t in ts), sum(t['c2'] - t['b2'] for t in ts), sum(t['cm2'] for t in ts),
                       sum(t['dn2'] for t in ts), round(100 * L / (L + F), 1) if L + F else None],
            'tabela_sm2': sum(t['sm2'] for t in ts)}
    acc = defaultdict(lambda: [0, 0, 0, 0, 0, 0])
    for t in tab:
        mun_code, v = idx[(t['uf'], t['zona'], t['secao'])]
        s1 = v.get('1')
        f = 100.0 * (t['c2'] - t['b2']) / t['c2'] if t['c2'] else 0
        k = 'A_0a5' if f <= 5 else ('B_5a10' if f <= 10 else 'C_mais10')
        a = acc[k]
        a[0] += 1
        a[1] += t['L2']
        a[2] += t['R2']
        if s1:
            a[3] += s1['L']
            a[4] += s1['R']
            a[5] += 1
    for k, a in sorted(acc.items()):
        R['faixas_1T'][k] = {'urnas': a[0], 'margem_2T': a[1] - a[2], 'pL_2T': round(100 * a[1] / (a[1] + a[2]), 2),
                             'margem_1T': a[3] - a[4], 'pL_1T_H2H': round(100 * a[3] / (a[3] + a[4]), 2),
                             'virada_pp': round(100 * a[1] / (a[1] + a[2]) - 100 * a[3] / (a[3] + a[4]), 2),
                             'com_1T': a[5]}
    json.dump(R, open(sys.argv[3], 'w'), ensure_ascii=False, indent=1)
    print(json.dumps(R, ensure_ascii=False, indent=1))


if __name__ == '__main__':
    main()
