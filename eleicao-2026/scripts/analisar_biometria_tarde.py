"""T21(c) do pré-registro (adendo 9), descritivo: habilitações sem biometria nos últimos 90 minutos da votação.

Por urna e por dia, cada 'Eleitor foi habilitado' conta como biométrico se for precedido, desde a habilitação
anterior, por 'Tipo de habilitação do eleitor [biométrica]' (mesma definição do T9). Janela: das 15h30 de Brasília
em diante (inclui a fila depois das 17h). O fuso sai da UF, como no T30.
Só entram urnas cujo log cobre os dois dias inteiros (votos computados iguais ao comparecimento do boletim e do bweb).
Uso: python3 -I analisar_biometria_tarde.py <pasta_arq_2t> <secoes2026_1t.json.gz> <amostra_2t.json.gz>
"""
import os as _os, sys as _sys
_sys.path.insert(0, _os.path.dirname(_os.path.abspath(__file__)))
import collections, json, os, sys
import numpy as np
from decodificar import _linhas_log, RX
from lib import carregar, chave_local, fe_ols

D1, D2 = '04/10/2026', '25/10/2026'
FUSO = {'AC': -2, 'AM': -1, 'RO': -1, 'RR': -1, 'MT': -1, 'MS': -1}
JANELA = 15.5


def secoes(pasta):
    for uf in sorted(os.listdir(pasta)):
        for m in sorted(os.listdir(os.path.join(pasta, uf))):
            for z in sorted(os.listdir(os.path.join(pasta, uf, m))):
                for s in sorted(os.listdir(os.path.join(pasta, uf, m, z))):
                    yield f'{uf.upper()}|{int(m)}|{int(z)}|{int(s)}', os.path.join(pasta, uf, m, z, s)


def habilitacoes(caminho, uf):
    out = {D1: [], D2: []}; comp = collections.Counter()
    for bl in _linhas_log(caminho):
        bio = False
        for l in bl:
            x = l.split('\t')
            if len(x) < 5:
                continue
            dia = x[0][:10]
            if dia not in out:
                continue
            m = RX.match(x[0])
            if not m:
                continue
            h = int(m.group(2)) + int(m.group(3)) / 60 + int(m.group(4)) / 3600 - FUSO.get(uf, 0)
            if x[4] == 'Tipo de habilitação do eleitor [biométrica]':
                bio = True
            elif x[4] == 'Eleitor foi habilitado':
                out[dia].append((h, bio)); bio = False
            elif x[4] == 'O voto do eleitor foi computado':
                comp[dia] += 1
    return out, comp


def main():
    pasta, base1, amostra = sys.argv[1:4]
    d1 = carregar(base1); am = carregar(amostra)
    rows = []; tot = collections.Counter(); fora = 0
    for k, p in secoes(pasta):
        lg = sorted(f for f in os.listdir(p) if f.endswith('-log.jez'))
        if not lg or k not in am or '2' not in am[k] or '1' not in d1.get(k, {}):
            continue
        hab, comp = habilitacoes(os.path.join(p, lg[-1]), k.split('|')[0])
        a, b = d1[k]['1'], am[k]['2']
        if comp[D1] != a['comp'] or comp[D2] != b['comp'] or not hab[D1] or not hab[D2]:
            fora += 1; continue
        r = {'k': k, 'loc': chave_local(k, b)}
        for t, dia in (('1', D1), ('2', D2)):
            j = [bio for h, bio in hab[dia] if h >= JANELA]
            r['hab' + t] = len(hab[dia]); r['nb' + t] = sum(1 for h, bio in hab[dia] if not bio)
            r['jan' + t] = len(j); r['nbjan' + t] = sum(1 for bio in j if not bio)
            for c in ('hab', 'nb', 'jan', 'nbjan'):
                tot[c + t] += r[c + t]
        r['dL'] = b['L'] - a['L']
        rows.append(r)
    out = {'urnas': len(rows), 'urnas_fora_por_log_incompleto': fora, 'totais': dict(tot)}
    for t in '12':
        out[f'turno{t}'] = {'pct_sem_biometria_no_dia': 100 * tot['nb' + t] / tot['hab' + t],
                            'pct_sem_biometria_na_janela': 100 * tot['nbjan' + t] / max(tot['jan' + t], 1),
                            'pct_das_sem_biometria_que_caem_na_janela': 100 * tot['nbjan' + t] / max(tot['nb' + t], 1),
                            'pct_das_habilitacoes_na_janela': 100 * tot['jan' + t] / tot['hab' + t]}
    # pareado na mesma urna: variação, do 1º para o 2º turno, da fração sem biometria na janela
    dif = [100 * (r['nbjan2'] / r['jan2'] - r['nbjan1'] / r['jan1']) for r in rows if r['jan1'] >= 5 and r['jan2'] >= 5]
    if dif:
        out['pareado_janela'] = {'urnas_com_5_ou_mais_na_janela_nos_dois': len(dif), 'media_pontos': float(np.mean(dif)),
                                 'ep': float(np.std(dif, ddof=1) / np.sqrt(len(dif)))}
    # descritivo: ganho de Lula nas variações de habilitação na janela (efeito fixo de local)
    y = np.array([r['dL'] for r in rows], float)
    X = np.column_stack([[r['nbjan2'] - r['nbjan1'] for r in rows], [(r['jan2'] - r['nbjan2']) - (r['jan1'] - r['nbjan1']) for r in rows],
                         [(r['hab2'] - r['jan2']) - (r['hab1'] - r['jan1']) for r in rows]]).astype(float)
    try:
        g = fe_ols(y, X, [r['loc'] for r in rows], None, ['var_sem_bio_janela', 'var_bio_janela', 'var_antes_da_janela'])
        out['ganho_lula_por_habilitacao'] = {'coef': g['coef'], 'ep': g['ep'], 'n': g['n'], 'locais': g['grupos']}
    except ValueError as e:
        out['ganho_lula_por_habilitacao'] = f'sem estimativa: {e}'
    print(json.dumps(out, ensure_ascii=False, indent=1))


if __name__ == '__main__':
    main()
