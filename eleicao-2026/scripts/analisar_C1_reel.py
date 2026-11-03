"""C1 do pré-registro (Adendo 24, commit ca110bb, 03/11/2026 04:24:10 UTC): checagem do reel @assis.salvioli
(DfHTWubBajq), nível contra mudança pelo grau de liberação sem biometria, bweb inteiro.

Letra do registro
  - Faixas de seção pela fração QT_ELEI_BIOM_SEM_HABILITACAO / comparecimento no 2º turno (0 a 5%, 5 a 10%, mais de
    10%). Em cada faixa: margem de Lula no 2º turno, margem nas mesmas seções no 1º turno, virada (fatia de Lula entre
    os finalistas, 2º menos 1º turno).
  - Dentro do local de votação: virada contra a faixa (efeito fixo de local, erro agrupado por local, peso L2+R2).
  - Leitura fixada antes: se a faixa de mais de 10% já dava a Lula a maior parte da margem no 1º turno (que Flávio
    venceu no país) e a virada dentro do local não difere entre faixas (|diferença| abaixo de 0,5 ponto com erro-padrão
    até 0,25), o placar por faixa é composição, não desvio. Se a virada dentro do local na faixa de mais de 10% for 1,0
    ponto ou mais acima da de 0 a 5%, a mais de 4 erros-padrão, é sinal.

Decisões que o registro não fixa (escritas aqui antes de calcular qualquer número do C1; declaradas como desvio)
  D1. Campo: QT_ELEI_BIOM_SEM_HABILITACAO (NH) das linhas do cargo 1 (Presidente) do bweb de cada turno, lido aqui
      mesmo dos zips (trab2t/zips2t e bweb1t/zips), uma entrada por seção; as linhas da mesma seção têm de concordar e as
      discordâncias são contadas. Do mesmo bweb: aptos, comparecimento, local, tipo de urna, agregação, urna e os votos
      de 13 e 22. Conferência: comparecimento, aptos, local e votos de 13 e 22 contra secoes2026.json.gz; NH contra o
      cache do F6 (nh_bweb_F6.json.gz) quando dado. Votos usados nas contas: os da base ('1' e '2': L, R, O, B, N).
  D2. Universo: seções das 27 UFs (exterior fora: lá o campo é zero em todas as seções) presentes nos dois turnos na base
      e no bweb, campo válido nos dois turnos, comparecimento do 2º turno acima de zero. Para a virada e a regressão:
      também L+R > 0 nos dois turnos.
  D3. Faixas, comparação em inteiros, sem arredondamento: A = "0 a 5%" (100 NH2 <= 5 C2); B = "5 a 10%"
      (5 C2 < 100 NH2 <= 10 C2); C = "mais de 10%" (100 NH2 > 10 C2). C2 = comparecimento do 2º turno.
  D4. Por faixa: seções, comparecimento, NH, votos de Lula e Flávio nos dois turnos; margem = L - R em votos e em pontos
      dos votos nos finalistas; virada agregada = 100 soma L2 / soma (L2+R2) - 100 soma L1 / soma (L1+R1); ao lado, a
      média das viradas das seções ponderada por L2+R2 (o que a regressão compara).
  D5. Regressão: y = 100 L2/(L2+R2) - 100 L1/(L1+R1) por seção; X = indicadores das faixas B e C (A é a referência);
      efeito fixo de local (lib.chave_local: UF|município|zona|local do 2º turno), peso L2+R2, erro agrupado por local
      (lib.fe_ols, CR1; locais com uma seção só saem). Coeficiente de C = diferença C - A dentro do local; de B = B - A.
      Contadas as seções de cada faixa em locais com mais de uma faixa (as que identificam).
  D6. "A faixa de mais de 10% já dava a Lula a maior parte da margem no 1º turno": lida como margem de Lula no 1º turno
      na faixa C positiva e de pelo menos metade da margem da mesma faixa no 2º turno (M1_C >= 0,5 M2_C, M2_C > 0).
      Ao lado, sem mudar a leitura: se a faixa C no 1º turno dava a Lula mais que a margem nacional do 1º turno (as
      outras faixas davam a Flávio) e que parte da mudança da margem nacional entre os turnos vem da faixa C.
  D7. "A virada dentro do local não difere entre faixas": |B - A| < 0,5 com ep <= 0,25 e |C - A| < 0,5 com ep <= 0,25.
      COMPOSIÇÃO = D6 e D7. SINAL = C - A >= +1,0 e (C - A)/ep > 4. Tudo o mais: INCONCLUSIVO (o registro não nomeia o
      caso intermediário), com o motivo escrito.
  D8. Robustez e controles, fora do critério (não mudam o veredito; escolhidos antes de ver o resultado): placebo
      (y = fatia de Lula no 1º turno); sem peso; covariáveis (fatia de Lula no 1º turno, variação do comparecimento
      sobre aptos, log dos aptos); efeito fixo de município; sem efeito fixo (diferença bruta no país); faixa pela fração
      do 1º turno (NH1/C1); faixa por NH2/aptos; só seções apuradas, sem agregação nos dois turnos, aptos iguais e mesma
      urna; dose contínua (y contra 100 NH2/C2); faixa C dividida (10 a 20% e mais de 20%).

Pedido da tarefa, fora do Adendo 24 (descritivo, sem veredito): reproduzir o placar do reel e dizer se o "sem
biometria" dele (15.709.293 votos) é o campo do bweb (8,6 milhões) ou inclui eleitores sem biometria cadastrada.
  P1. Placar com o campo do bweb e os cortes do reel: "0 a 5%" = A; "até 10%" = A+B, acumulado (o reel põe 221.532 urnas
      em "até 10%" = 44,9% de 492.988, o total que dá com A dentro de "até 10%"); "mais de 10%" = C. Por faixa: seções,
      parte das seções, fatias de Lula e Flávio entre os finalistas, margem em votos e parte da margem nacional
      (27 UFs). Comparação com os números da tela (degravação, painéis da cena 2).
  P2. Boletins da amostra (amostra2t/arq, 3.897 pacotes do 2º turno): o boletim de 2026 traz, antes dos resultados, um
      campo [2:1] com três inteiros que somam o comparecimento. Identificação feita antes destas decisões, em 25
      pacotes (random.Random(7)) contra o classificador de log do F6: [0] = eleitores sem biometria cadastrada (classe S
      do log), [1] = habilitados por biometria (B), [2] = com biometria e liberados sem ela (M, igual ao NH do bweb).
      Aqui o script reconfere: [2] contra o NH do bweb e soma contra o comparecimento do boletim em todos os pacotes; em
      300 pacotes sorteados (numpy default_rng(20261103)), [0], [1] e [2] contra S, B e M do analisar_F6.classificar.
  P3. Na amostra: definição candidata do reel = S + M (toda habilitação que não foi por biometria). Totais, fração do
      comparecimento e distribuição das seções pelos cortes do reel nas duas definições (M e S + M). Estimativa nacional
      de S, duas: (i) razão S/C2 da amostra em cada UF vezes o C2 da UF; (ii) razão S/S_hat da amostra vezes a soma
      nacional de S_hat (P4). Erro por bootstrap de locais dentro da UF (2.000, semente 20261103). Comparação de
      NH + S estimado com 15.709.293 e de C2 - (NH + S) com os "110,9 milhões com biometria" da cena 4.
  P4. Proxy nacional por seção com o perfil do eleitorado por seção (TSE, 2026): AM, MT e SP lidos da pasta do F16
      (adendo22/F16_dl_perfil_secao), as outras UFs baixadas para adendo24/C1_dl_perfil_secao (as que o servidor
      entregar). sem_cad = QT_ELEITORES - QT_ELEITORES_BIOMETRIA; S_hat = C2 x sem_cad / QT_ELEITORES (mesmo
      comparecimento nos dois grupos). S_hat conferido contra S nos boletins da amostra (soma, correlação, erro médio).
      Placar do reel refeito com (NH + S_hat)/C2 e com sem_cad/QT_ELEITORES; contagens comparadas com 45.615, 221.532 e
      271.456. Só nas UFs com perfil; a cobertura é dita.
  P5. Fora do critério e depois da letra: a regressão D5 com as faixas pela definição do reel, (NH + S_hat)/C2 no país
      e (NH + S)/C2 exato na amostra de boletins.
  P6. Acrescentado DEPOIS de ver o resultado pela letra (exploratório, sem veredito; não muda nada acima):
      (a) a tabela D4 (margens de 1º e 2º turno e virada) pelas faixas do reel, no país com S_hat calibrado pela amostra
          e na amostra com S exato do boletim;
      (b) o proxy calibrado contra S exato na amostra: fração de seções na mesma faixa e matriz de confusão (a linha
          "faixa_igual_com_S_hat" da P4 usa S_hat sem calibrar);
      (c) a "prova 1" do reel na amostra: S, B e M por dia pelo analisar_F6.classificar nos logs da amostra (25/10 e,
          quando a urna é a mesma, 04/10), seções com log completo nos dois dias (votos computados no log iguais ao
          comparecimento da base no dia); variações e o efeito de escolher só as seções onde B caiu e S + M subiu;
          virada dessas seções contra as outras do mesmo local.
      (d) ordenação: fatia de Lula nas 45.615 seções de menor fração e nas 271.456 de maior fração, para o campo do
          bweb, para (NH + S_hat calibrado)/C2 e para S_hat calibrado sozinho (empates pela ordem de chave).

Uso:
  python3 -I analisar_C1_reel.py extrair <secoes2026.json.gz> <zips 1T> <zips 2T> <cache_F6 ou -> <pasta amostra arq>
          <cache_saida.json.gz> <pasta perfil> [<pasta perfil> ...]
  python3 -I analisar_C1_reel.py perfil <cache.json.gz> <pasta perfil> [<pasta perfil> ...]
  python3 -I analisar_C1_reel.py logs_dias <cache.json.gz> <pasta amostra arq>   (P6c)
  python3 -I analisar_C1_reel.py rodar <secoes2026.json.gz> <cache.json.gz> <saida.json> <saida.txt>
"""
import os as _os, sys as _sys
_sys.path.insert(0, _os.path.dirname(_os.path.abspath(__file__)))
import collections, csv, glob, gzip, io, json, math, os, sys, time, zipfile
from multiprocessing import Pool
import numpy as np
from lib import carregar, chave_local, fe_ols

CAMPO = 'QT_ELEI_BIOM_SEM_HABILITACAO'
SEMENTE = 20261103
N_BOOT = 2000
N_VALID_LOG = 300
LIM_COMP, EP_COMP = 0.5, 0.25
LIM_SINAL, Z_SINAL = 1.0, 4.0
REEL = {'secoes_0_5': 45615, 'secoes_ate_10': 221532, 'secoes_mais_10': 271456, 'secoes_total': 221532 + 271456,
        'margem_0_5_Flavio': 443504, 'fatia_ate_10_Lula': 50.09, 'fatia_ate_10_Flavio': 49.91,
        'margem_mais_10_Lula': 4254754, 'parte_margem_mais_10': 97.65, 'sem_biometria_total': 15709293,
        'sem_biometria_total_outro_painel': 15709193, 'com_biometria_milhoes': 110.9, 'urnas': 497897,
        'pct_ate_10_do_Brasil': 44.9, 'fatia_0_5_Flavio': 52.0, 'fatia_0_5_Lula': 48.0}


def log(*a):
    print('#', time.strftime('%H:%M:%S'), *a, file=sys.stderr, flush=True)


# ------------------------------------------------------------------ extração: bweb

def ler_zip_bweb(zpath):
    """Cargo 1, por seção: [loc, apt, comp, NH, tipo, agregadas, urna, votos13, votos22]; linhas discordantes."""
    out = {}; incons = 0; invalid = collections.Counter(); linhas = 0
    votos = collections.defaultdict(collections.Counter)
    z = zipfile.ZipFile(zpath)
    nome = [n for n in z.namelist() if n.lower().endswith('.csv')][0]
    with z.open(nome) as fh:
        cab = next(csv.reader([fh.readline().decode('latin1')], delimiter=';'))
        ix = {c.strip().replace('SG_ UF', 'SG_UF'): i for i, c in enumerate(cab)}
        ic = [ix[c] for c in ('SG_UF', 'CD_MUNICIPIO', 'NR_ZONA', 'NR_SECAO', 'NR_LOCAL_VOTACAO', 'QT_APTOS',
                              'QT_COMPARECIMENTO', CAMPO, 'DS_TIPO_URNA', 'DS_SECOES_AGREGADAS', 'NR_URNA_EFETIVADA',
                              'CD_CARGO_PERGUNTA', 'NR_VOTAVEL', 'QT_VOTOS')]
        for linha in fh:
            if b';1;"Presidente";' not in linha:
                continue
            r = next(csv.reader([linha.decode('latin1').rstrip('\r\n')], delimiter=';'))
            uf, mun, zon, sec, loc, apt, comp, nh, tipo, agr, urna, car, nv, qv = (r[i] for i in ic)
            if car != '1':
                continue
            linhas += 1
            k = f'{uf}|{int(mun)}|{int(zon)}|{int(sec)}'
            try:
                nhv = int(nh)
                if nhv < 0:
                    invalid[nh] += 1; nhv = None
            except ValueError:
                invalid[nh] += 1; nhv = None
            agr = '' if agr in ('', '#NULO#') else agr
            reg = [int(loc), int(apt), int(comp), nhv, tipo, agr, int(urna) if urna.lstrip('-').isdigit() else urna]
            if k in out:
                if out[k] != reg:
                    incons += 1
            else:
                out[k] = reg
            votos[k][nv] += int(qv)
    for k, reg in out.items():
        reg.extend([votos[k].get('13', 0), votos[k].get('22', 0)])
    return os.path.basename(zpath), out, incons, dict(invalid), linhas


def ler_pasta_bweb(pasta, pool, rot):
    zs = sorted(glob.glob(os.path.join(pasta, '*.zip')), key=lambda p: -os.path.getsize(p))
    tudo = {}; info = {}
    for nome, out, inc, inv, linhas in pool.imap_unordered(ler_zip_bweb, zs):
        tudo.update(out)
        info[nome] = {'secoes': len(out), 'linhas_cargo1': linhas, 'linhas_discordantes': inc, 'valores_invalidos': inv}
        log(rot, nome, len(out), 'seções')
    return tudo, info


# ------------------------------------------------------------------ extração: boletins da amostra

def campo_contexto(bu):
    """O nó [2:1] de nível 1 com três INTEGER (sem biometria cadastrada, por biometria, liberados sem biometria)."""
    achados = []
    for n in bu:
        if (n[0], n[1]) == (2, 1) and isinstance(n[2], list) and len(n[2]) == 3 \
                and all((c[0], c[1]) == (0, 2) for c in n[2]):
            achados.append([int.from_bytes(c[2], 'big') for c in n[2]])
    return achados


def ler_bu_amostra(p):
    from ber import parse
    from decodificar import ler_bu, bu_para_secao
    partes = p.split(os.sep)
    uf, mun, zona, sec = partes[-5].upper(), int(partes[-4]), int(partes[-3]), int(partes[-2])
    k = f'{uf}|{mun}|{zona}|{sec}'
    try:
        env = parse(open(p, 'rb').read())[0][2]
        octet = [n for n in env if (n[0], n[1]) == (0, 4)][-1][2]
        bu = parse(octet)[0][2]
        ctx = campo_contexto(bu)
        b = ler_bu(p); s, _ = bu_para_secao(b)
        return k, {'ctx': ctx, 'comp_bu': s['comp'] if s else None, 'L': s['L'] if s else None,
                   'R': s['R'] if s else None, 'mun_bu': b.get('mun'), 'zona_bu': b.get('zona'),
                   'secao_bu': b.get('secao'), 'arquivo': p}
    except Exception as e:  # conta e segue
        return k, {'erro': repr(e), 'arquivo': p}


def classificar_log(p):
    import analisar_F6 as f6
    try:
        hab, comp, *_ = f6.classificar(p)
        h = hab[f6.D2]
        return p, {c: sum(1 for t, cl, _ in h if cl == c) for c in 'BMS'}, comp[f6.D2]
    except Exception as e:
        return p, {'erro': repr(e)}, None


def classificar_log_dias(p):
    import analisar_F6 as f6
    try:
        hab, comp, *_ = f6.classificar(p)
        return p, {dia: {**{c: sum(1 for t, cl, _ in hab[dia] if cl == c) for c in 'BMS'}, 'computados': comp[dia]}
                   for dia in (f6.D1, f6.D2)}
    except Exception as e:
        return p, {'erro': repr(e)}


def modo_logs_dias(cache, pasta_amostra):
    """P6c: S, B e M por dia em todos os logs da amostra, guardados no cache."""
    c = carregar(cache)
    lgs = {}
    for k, v in c['bu'].items():
        pasta = os.path.dirname(v['arquivo'])
        lg = sorted(glob.glob(os.path.join(pasta, '*-log.jez')))
        if lg:
            lgs[lg[-1]] = k
    out = {}
    with Pool(min(8, os.cpu_count() or 2)) as pool:
        for p, r in pool.imap_unordered(classificar_log_dias, sorted(lgs), chunksize=10):
            out[lgs[p]] = r
    c['logs_dias'] = out
    log('logs por dia', len(out))
    with gzip.open(cache, 'wt') as fo:
        json.dump(c, fo)


# ------------------------------------------------------------------ extração: perfil por seção

def ler_zip_perfil(zpath):
    z = zipfile.ZipFile(zpath)
    nome = [n for n in z.namelist() if n.lower().endswith('.csv')][0]
    out = collections.defaultdict(lambda: [0, 0]); linhas = 0; invalid = 0
    with z.open(nome) as fh:
        tf = io.TextIOWrapper(fh, encoding='latin1', newline='')
        rd = csv.reader(tf, delimiter=';')
        cab = [c.strip() for c in next(rd)]
        ix = {c: i for i, c in enumerate(cab)}
        iu, im, iz, isec, ie, ib = (ix[c] for c in ('SG_UF', 'CD_MUNICIPIO', 'NR_ZONA', 'NR_SECAO', 'QT_ELEITORES',
                                                   'QT_ELEITORES_BIOMETRIA'))
        for r in rd:
            linhas += 1
            try:
                e, b = int(r[ie]), int(r[ib])
            except (ValueError, IndexError):
                invalid += 1; continue
            if e < 0 or b < 0:
                invalid += 1; continue
            k = f'{r[iu]}|{int(r[im])}|{int(r[iz])}|{int(r[isec])}'
            o = out[k]; o[0] += e; o[1] += b
    return os.path.basename(zpath), dict(out), linhas, invalid


def modo_extrair(base, p1, p2, cache_f6, pasta_amostra, saida, pastas_perfil):
    t0 = time.time()
    d = carregar(base)
    with Pool(min(8, os.cpu_count() or 2)) as pool:
        b1, info1 = ler_pasta_bweb(p1, pool, '1T')
        b2, info2 = ler_pasta_bweb(p2, pool, '2T')
        # conferência com a base
        conf = collections.Counter()
        for t, bb in (('1', b1), ('2', b2)):
            for k, reg in bb.items():
                s = d.get(k, {}).get(t)
                if s is None:
                    conf[f'no_bweb_e_nao_na_base_{t}'] += 1; continue
                conf[f'conferidas_{t}'] += 1
                if reg[2] != s['comp']: conf[f'comp_diferente_{t}'] += 1
                if reg[1] != s['apt']: conf[f'apt_diferente_{t}'] += 1
                if reg[0] != s['loc']: conf[f'loc_diferente_{t}'] += 1
                if reg[7] != s['L']: conf[f'L_diferente_{t}'] += 1
                if reg[8] != s['R']: conf[f'R_diferente_{t}'] += 1
            for k, sd in d.items():
                if t in sd and k not in bb:
                    conf[f'na_base_e_nao_no_bweb_{t}'] += 1
        if cache_f6 != '-' and os.path.exists(cache_f6):
            c6 = carregar(cache_f6)
            for t, bb in (('1', b1), ('2', b2)):
                for k, reg in c6[t].items():
                    if k in bb:
                        conf[f'NH_conferido_com_F6_{t}'] += 1
                        if bb[k][3] != reg[3]: conf[f'NH_diferente_do_F6_{t}'] += 1
                    else:
                        conf[f'no_F6_e_nao_aqui_{t}'] += 1
        log('bweb lido e conferido', dict(conf))
        # boletins da amostra
        bus = sorted(glob.glob(os.path.join(pasta_amostra, '*', '*', '*', '*', '*-bu.dat')))
        bu = {}; bu_rep = collections.Counter()
        for k, r in pool.imap_unordered(ler_bu_amostra, bus, chunksize=20):
            if k in bu:
                bu_rep['secao_repetida'] += 1
            bu[k] = r
        log('boletins lidos', len(bu))
        # validação do campo de contexto contra o log (300 pacotes sorteados)
        rng = np.random.default_rng(SEMENTE)
        ks = sorted(k for k, r in bu.items() if 'erro' not in r)
        sel = sorted(rng.choice(len(ks), size=min(N_VALID_LOG, len(ks)), replace=False).tolist())
        logs = []
        for i in sel:
            pasta = os.path.dirname(bu[ks[i]]['arquivo'])
            lg = sorted(glob.glob(os.path.join(pasta, '*-log.jez')))
            if lg:
                logs.append((ks[i], lg[-1]))
        val = {}
        res = dict((p, (cl, cp)) for p, cl, cp in pool.imap_unordered(classificar_log, [p for _, p in logs]))
        for k, p in logs:
            val[k] = {'log': res[p][0], 'computados_log': res[p][1]}
        log('logs de validação lidos', len(val))
        perfil, info_perfil = ler_perfis(pastas_perfil, pool)
    with gzip.open(saida, 'wt') as fo:
        json.dump({'1': b1, '2': b2, 'info': {'1': info1, '2': info2, 'conferencia': dict(conf),
                                              'perfil': info_perfil, 'bu_repetidos': dict(bu_rep)},
                   'bu': bu, 'validacao_log': val, 'perfil': perfil}, fo)
    log(f'extração feita em {time.time() - t0:.0f}s')


# ------------------------------------------------------------------ cálculo

def faixa_de(nh, den, cortes=(5, 10)):
    """0 = A (<= 5%), 1 = B (5 a 10%), 2 = C (> 10%), em inteiros."""
    a, b = cortes
    if 100 * nh <= a * den: return 0
    if 100 * nh <= b * den: return 1
    return 2


def ident_faixas(F, g):
    _, gi = np.unique(g, return_inverse=True)
    nf = {}
    G = gi.max() + 1
    tem = np.zeros((G, 3), bool)
    for j in range(3):
        tem[:, j] = np.bincount(gi, weights=(F == j).astype(float), minlength=G) > 0
    multi = tem.sum(1) >= 2
    for j, nome in enumerate('ABC'):
        nf[nome] = int(((F == j) & multi[gi]).sum())
    nf['locais_com_mais_de_uma_faixa'] = int(multi.sum())
    return nf


def reg_faixas(y, F, g, w, mask, extra=None, nomes_extra=None, ncat=3, nomes_cat=('B', 'C')):
    m = mask & np.isfinite(y)
    cols = [(F == j).astype(float) for j in range(1, ncat)]
    nomes = list(nomes_cat)
    if extra is not None:
        for c in extra:
            m &= np.isfinite(c)
        cols += list(extra); nomes += list(nomes_extra)
    X = np.column_stack([c[m] for c in cols])
    r = fe_ols(y[m], X, g[m], None if w is None else w[m], nomes)
    out = {'n': r['n'], 'grupos': r['grupos'], 'coef': r['coef'], 'ep': r['ep'],
           'z': {k: (r['coef'][k] / r['ep'][k] if r['ep'][k] > 0 else float('nan')) for k in nomes}}
    _, gi = np.unique(g[m], return_inverse=True)
    est = np.bincount(gi)[gi] >= 2
    if ncat == 3:
        out['identificam'] = ident_faixas(F[m][est], g[m][est])
    return out


def tabela_faixas(F, L1, R1, L2, R2, C2, NH2, ncat=3, rot='ABC'):
    out = {}
    marg_nac2 = float((L2 - R2).sum()); marg_nac1 = float((L1 - R1).sum())
    for j in range(ncat):
        s = F == j
        l1, r1, l2, r2 = (float(v[s].sum()) for v in (L1, R1, L2, R2))
        f1 = 100 * l1 / (l1 + r1) if l1 + r1 else float('nan')
        f2 = 100 * l2 / (l2 + r2) if l2 + r2 else float('nan')
        ok = s & ((L1 + R1) > 0) & ((L2 + R2) > 0)
        vir = 100 * L2[ok] / (L2[ok] + R2[ok]) - 100 * L1[ok] / (L1[ok] + R1[ok])
        wv = (L2[ok] + R2[ok]).astype(float)
        out[rot[j]] = {'secoes': int(s.sum()), 'comparecimento_2T': int(C2[s].sum()), 'NH_2T': int(NH2[s].sum()),
                       'L1': int(l1), 'R1': int(r1), 'L2': int(l2), 'R2': int(r2),
                       'margem_Lula_1T': int(l1 - r1), 'margem_Lula_2T': int(l2 - r2),
                       'margem_Lula_1T_pts': 100 * (l1 - r1) / (l1 + r1) if l1 + r1 else None,
                       'margem_Lula_2T_pts': 100 * (l2 - r2) / (l2 + r2) if l2 + r2 else None,
                       'fatia_Lula_1T': f1, 'fatia_Lula_2T': f2, 'virada_agregada': f2 - f1,
                       'virada_media_ponderada': float((vir * wv).sum() / wv.sum()) if wv.sum() else None,
                       'parte_da_margem_nacional_2T_pct': 100 * (l2 - r2) / marg_nac2 if marg_nac2 else None,
                       'parte_da_mudanca_da_margem_nacional_pct': 100 * ((l2 - r2) - (l1 - r1)) / (marg_nac2 - marg_nac1)
                       if marg_nac2 != marg_nac1 else None}
    out['_nacional'] = {'margem_Lula_1T': int(marg_nac1), 'margem_Lula_2T': int(marg_nac2), 'secoes': int(len(F))}
    return out


def placar_reel(F, L2, R2, rot=''):
    """Cortes do reel: 0 a 5% (A), até 10% acumulado (A+B), mais de 10% (C)."""
    tot = len(F); marg = float((L2 - R2).sum())
    out = {}
    for nome, s in (('0_a_5', F == 0), ('ate_10', F <= 1), ('mais_de_10', F == 2), ('5_a_10', F == 1)):
        l2, r2 = float(L2[s].sum()), float(R2[s].sum())
        out[nome] = {'secoes': int(s.sum()), 'pct_secoes': 100 * s.sum() / tot if tot else None,
                     'fatia_Lula': 100 * l2 / (l2 + r2) if l2 + r2 else None,
                     'fatia_Flavio': 100 * r2 / (l2 + r2) if l2 + r2 else None,
                     'margem_Lula': int(l2 - r2), 'parte_da_margem_pct': 100 * (l2 - r2) / marg if marg else None}
    out['_total'] = {'secoes': tot, 'margem_Lula': int(marg)}
    return out


def leitura_C1(tab, r):
    MC1, MC2 = tab['C']['margem_Lula_1T'], tab['C']['margem_Lula_2T']
    d6 = MC2 > 0 and MC1 > 0 and MC1 >= 0.5 * MC2
    cb, eb = r['coef']['B'], r['ep']['B']; cc, ec = r['coef']['C'], r['ep']['C']
    d7 = abs(cb) < LIM_COMP and eb <= EP_COMP and abs(cc) < LIM_COMP and ec <= EP_COMP
    sinal = cc >= LIM_SINAL and ec > 0 and cc / ec > Z_SINAL
    if sinal:
        v, mot = 'SINAL', 'virada da faixa C 1,0 ponto ou mais acima da A, a mais de 4 erros-padrão'
    elif d6 and d7:
        v, mot = 'COMPOSIÇÃO, NÃO DESVIO', 'faixa C já dava a Lula a maior parte da margem no 1º turno e a virada dentro do local não difere entre faixas'
    else:
        partes = []
        if not d6: partes.append('a faixa C não dava a Lula, no 1º turno, metade ou mais da margem do 2º turno')
        if not d7: partes.append('a virada dentro do local difere entre faixas além de 0,5 ponto ou com erro-padrão acima de 0,25')
        v, mot = 'INCONCLUSIVO', '; '.join(partes)
    return {'veredito': v, 'motivo': mot, 'D6_faixa_C_ja_dava_margem_no_1T': bool(d6), 'D7_virada_igual_entre_faixas': bool(d7),
            'criterio_sinal': bool(sinal), 'M1_C': MC1, 'M2_C': MC2, 'M1_C_sobre_M2_C': MC1 / MC2 if MC2 else None,
            'faixa_C_acima_da_margem_nacional_1T': bool(MC1 > tab['_nacional']['margem_Lula_1T'])}


def boot_S(keys_uf, locs, S, C2, Shat, C2_uf_nac, Shat_nac_uf, Shat_nac_total, rng, nb):
    """Estimativas (i) e (ii) da P3, com bootstrap de locais dentro da UF."""
    ufs = sorted(set(keys_uf))
    idx_uf = {u: np.where(keys_uf == u)[0] for u in ufs}
    loc_uf = {}
    for u in ufs:
        ii = idx_uf[u]
        _, gi = np.unique(locs[ii], return_inverse=True)
        loc_uf[u] = (ii, gi, gi.max() + 1)

    def est(pesos):
        e1 = 0.0
        sS = sC = sH = 0.0
        for u in ufs:
            ii, gi, G = loc_uf[u]
            w = pesos[u][gi]
            s_, c_ = (S[ii] * w).sum(), (C2[ii] * w).sum()
            e1 += (s_ / c_) * C2_uf_nac[u] if c_ > 0 else 0.0
            ok = np.isfinite(Shat[ii])
            sS += (S[ii][ok] * w[ok]).sum(); sH += (Shat[ii][ok] * w[ok]).sum()
        e2 = sS / sH * Shat_nac_total if sH > 0 else float('nan')
        return e1, e2
    um = {u: np.ones(loc_uf[u][2]) for u in ufs}
    base = est(um)
    bs = []
    for _ in range(nb):
        p = {u: np.bincount(rng.integers(0, loc_uf[u][2], loc_uf[u][2]), minlength=loc_uf[u][2]).astype(float) for u in ufs}
        bs.append(est(p))
    bs = np.array(bs)
    return {'i_razao_S_sobre_C2_por_UF': base[0], 'ep_i': float(np.nanstd(bs[:, 0], ddof=1)),
            'ii_razao_S_sobre_S_hat': base[1], 'ep_ii': float(np.nanstd(bs[:, 1], ddof=1))}


def modo_rodar(base, cache, saida_json, saida_txt):
    t0 = time.time()
    d = carregar(base)
    c = carregar(cache)
    b1, b2 = c['1'], c['2']
    info = c['info']
    # universo D2
    ks, fora = [], collections.Counter()
    for k in sorted(d):
        uf = k.split('|')[0]
        sd = d[k]
        if uf == 'ZZ': fora['exterior'] += 1; continue
        if '1' not in sd or '2' not in sd: fora['sem_os_dois_turnos_na_base'] += 1; continue
        if k not in b1 or k not in b2: fora['sem_os_dois_turnos_no_bweb'] += 1; continue
        if b1[k][3] is None or b2[k][3] is None: fora['campo_invalido'] += 1; continue
        if sd['2']['comp'] <= 0: fora['comparecimento_2T_zero'] += 1; continue
        ks.append(k)
    n = len(ks)
    log('universo', n, dict(fora))
    A = lambda f: np.array([f(k) for k in ks], float)
    L1 = A(lambda k: d[k]['1']['L']); R1 = A(lambda k: d[k]['1']['R'])
    L2 = A(lambda k: d[k]['2']['L']); R2 = A(lambda k: d[k]['2']['R'])
    C1 = A(lambda k: d[k]['1']['comp']); C2 = A(lambda k: d[k]['2']['comp'])
    AP1 = A(lambda k: d[k]['1']['apt']); AP2 = A(lambda k: d[k]['2']['apt'])
    NH1 = A(lambda k: b1[k][3]); NH2 = A(lambda k: b2[k][3])
    loc = np.array([chave_local(k, d[k]['2']) for k in ks])
    mun = np.array(['|'.join(k.split('|')[:2]) for k in ks])
    ufv = np.array([k.split('|')[0] for k in ks])
    F = np.array([faixa_de(int(NH2[i]), int(C2[i])) for i in range(n)])
    ok = ((L1 + R1) > 0) & ((L2 + R2) > 0)
    with np.errstate(divide='ignore', invalid='ignore'):
        s1 = 100 * L1 / (L1 + R1); s2 = 100 * L2 / (L2 + R2)
    y = np.where(ok, s2 - s1, np.nan)
    w = L2 + R2
    P = {'registro': 'PRE-REGISTRO-2026-10-26.md, Adendo 24, C1 (commit ca110bb, 03/11/2026 04:24:10 UTC)',
         'extracao': {'conferencia': info['conferencia'],
                      'linhas_discordantes_1T': sum(v['linhas_discordantes'] for v in info['1'].values()),
                      'linhas_discordantes_2T': sum(v['linhas_discordantes'] for v in info['2'].values()),
                      'valores_invalidos_1T': {k: v for x in info['1'].values() for k, v in x['valores_invalidos'].items()},
                      'valores_invalidos_2T': {k: v for x in info['2'].values() for k, v in x['valores_invalidos'].items()}},
         'universo': {'secoes': n, 'fora': dict(fora), 'com_L_mais_R_nos_dois_turnos': int(ok.sum()),
                      'NH_2T': int(NH2.sum()), 'NH_1T': int(NH1.sum()), 'comparecimento_2T': int(C2.sum()),
                      'comparecimento_1T': int(C1.sum()), 'L2': int(L2.sum()), 'R2': int(R2.sum()),
                      'L1': int(L1.sum()), 'R1': int(R1.sum())}}
    # exterior, para o total do reel
    ext = [k for k in d if k.startswith('ZZ|') and '2' in d[k]]
    P['exterior'] = {'secoes': len(ext), 'L2': sum(d[k]['2']['L'] for k in ext), 'R2': sum(d[k]['2']['R'] for k in ext),
                     'comp2': sum(d[k]['2']['comp'] for k in ext)}
    # universos candidatos ao total do reel (492.988 = 221.532 + 271.456), descritivo
    agr2 = np.array([bool(b2[k][5]) for k in ks]); apur2 = np.array([d[k]['2'].get('tipo') == 'Apurada' for k in ks])
    P['universos_candidatos'] = {'27_UFs': n, 'sem_agregacao_no_2T': int((~agr2).sum()), 'apuradas_no_2T': int(apur2.sum()),
                                 'apuradas_sem_agregacao_2T': int((apur2 & ~agr2).sum()),
                                 'com_L_mais_R_nos_dois_turnos': int(ok.sum()),
                                 'com_NH2_maior_que_zero': int((NH2 > 0).sum()),
                                 'margem_Lula_2T_sem_agregacao': int((L2 - R2)[~agr2].sum()),
                                 'margem_Lula_2T_apuradas': int((L2 - R2)[apur2].sum())}
    # ---- C1 pela letra
    tab = tabela_faixas(F, L1, R1, L2, R2, C2, NH2)
    P['C1_tabela'] = tab
    r = reg_faixas(y, F, loc, w, ok)
    P['C1_regressao'] = r
    P['C1_leitura'] = leitura_C1(tab, r)
    log('C1', P['C1_leitura']['veredito'], r['coef'], r['ep'])
    # ---- robustez D8
    rob = {}
    rob['placebo_y_fatia_Lula_1T'] = reg_faixas(np.where(ok, s1, np.nan), F, loc, w, ok)
    rob['sem_peso'] = reg_faixas(y, F, loc, None, ok)
    with np.errstate(divide='ignore', invalid='ignore'):
        vc = 100 * (C2 - C1) / AP2
        lap = np.log(np.where(AP2 > 0, AP2, np.nan))
    rob['covariaveis'] = reg_faixas(y, F, loc, w, ok, [s1, vc, lap], ['fatia_Lula_1T', 'var_comp_pts_aptos', 'log_aptos'])
    rob['efeito_fixo_municipio'] = reg_faixas(y, F, mun, w, ok)
    rob['sem_efeito_fixo_pais'] = reg_faixas(y, F, np.zeros(n, int), w, ok)
    rob['sem_efeito_fixo_pais']['nota'] = 'um grupo só: diferença bruta no país; erro-padrão agrupado não se aplica'
    F1 = np.array([faixa_de(int(NH1[i]), int(C1[i])) if C1[i] > 0 else -1 for i in range(n)])
    rob['faixa_pela_fracao_do_1T'] = reg_faixas(y, F1, loc, w, ok & (F1 >= 0))
    Fa = np.array([faixa_de(int(NH2[i]), int(AP2[i])) for i in range(n)])
    rob['faixa_NH2_sobre_aptos'] = reg_faixas(y, Fa, loc, w, ok)
    limpa = np.array([d[k]['1'].get('tipo') == 'Apurada' and d[k]['2'].get('tipo') == 'Apurada'
                      and not b1[k][5] and not b2[k][5] and d[k]['1']['apt'] == d[k]['2']['apt']
                      and d[k]['1'].get('urna') == d[k]['2'].get('urna') for k in ks])
    rob['so_apuradas_sem_agregacao_aptos_iguais_mesma_urna'] = reg_faixas(y, F, loc, w, ok & limpa)
    xd = 100 * NH2 / C2
    m = ok
    rr = fe_ols(y[m], xd[m][:, None], loc[m], w[m], ['pts_NH2_sobre_C2'])
    rob['dose_continua'] = {'n': rr['n'], 'grupos': rr['grupos'], 'coef': rr['coef'], 'ep': rr['ep']}
    F4 = np.where(F < 2, F, np.where(100 * NH2 <= 20 * C2, 2, 3))
    rob['faixa_C_dividida_10_20_e_mais_20'] = reg_faixas(y, F4, loc, w, ok, ncat=4, nomes_cat=('B', 'C_10_20', 'C_mais_20'))
    rob['faixa_C_dividida_10_20_e_mais_20']['secoes'] = {'C_10_20': int((F4 == 2).sum()), 'C_mais_20': int((F4 == 3).sum())}
    P['C1_robustez'] = rob
    # tabela por faixa do 1T (descritiva) e por UF
    P['C1_tabela_faixa_do_1T'] = tabela_faixas(np.where(F1 >= 0, F1, 0), L1, R1, L2, R2, C2, NH2)
    por_uf = {}
    for u in sorted(set(ufv)):
        s = ufv == u
        por_uf[u] = {nm: int(((F == j) & s).sum()) for j, nm in enumerate('ABC')}
        por_uf[u]['pct_C'] = 100 * por_uf[u]['C'] / s.sum()
        por_uf[u]['margem_Lula_2T'] = int((L2[s] - R2[s]).sum())
        por_uf[u]['fracao_NH_2T_pct'] = 100 * NH2[s].sum() / C2[s].sum()
    P['C1_faixas_por_UF'] = por_uf
    # ---- P1: placar do reel com o campo do bweb
    P['P1_placar_campo_bweb'] = placar_reel(F, L2, R2)
    P['P1_reel'] = REEL
    # ---- P2/P3: boletins da amostra
    bu = c['bu']
    val = c['validacao_log']
    erros = {k: v['erro'] for k, v in bu.items() if 'erro' in v}
    conf_bu = collections.Counter()
    S_bu, B_bu, M_bu, kb = [], [], [], []
    for k, v in sorted(bu.items()):
        if 'erro' in v: continue
        if k not in d or '1' not in d[k] or '2' not in d[k]: conf_bu['fora_da_base'] += 1; continue
        ctx = v['ctx']
        if len(ctx) != 1: conf_bu[f'campo_contexto_{len(ctx)}_vezes'] += 1; continue
        s_, b_, m_ = ctx[0]
        conf_bu['lidos'] += 1
        if s_ + b_ + m_ == v['comp_bu']: conf_bu['soma_igual_ao_comparecimento_do_boletim'] += 1
        if k in b2:
            conf_bu['no_bweb'] += 1
            if m_ == b2[k][3]: conf_bu['terceiro_igual_ao_NH_do_bweb'] += 1
            if v['comp_bu'] == b2[k][2]: conf_bu['comparecimento_igual_ao_bweb'] += 1
            if v['L'] == b2[k][7] and v['R'] == b2[k][8]: conf_bu['votos_13_22_iguais_ao_bweb'] += 1
        if (v['mun_bu'], v['zona_bu'], v['secao_bu']) == tuple(int(x) for x in k.split('|')[1:]):
            conf_bu['secao_do_boletim_igual_a_pasta'] += 1
        S_bu.append(s_); B_bu.append(b_); M_bu.append(m_); kb.append(k)
    cv = collections.Counter()
    for k, x in val.items():
        lg = x['log']
        if 'erro' in lg: cv['log_com_erro'] += 1; continue
        s_, b_, m_ = bu[k]['ctx'][0]
        cv['conferidos'] += 1
        cv['S_igual'] += lg['S'] == s_; cv['B_igual'] += lg['B'] == b_; cv['M_igual'] += lg['M'] == m_
        cv['tres_iguais'] += (lg['S'], lg['B'], lg['M']) == (s_, b_, m_)
        if x['computados_log'] == bu[k]['comp_bu']:
            cv['log_completo'] += 1
            cv['tres_iguais_log_completo'] += (lg['S'], lg['B'], lg['M']) == (s_, b_, m_)
    S_bu, B_bu, M_bu = (np.array(v, float) for v in (S_bu, B_bu, M_bu))
    C_bu = S_bu + B_bu + M_bu
    P['P2_boletins'] = {'pacotes': len(bu), 'erros_de_leitura': len(erros), 'conferencia': dict(conf_bu),
                        'validacao_log_300': dict(cv), 'erros': dict(list(erros.items())[:10])}
    tot_S, tot_M, tot_B, tot_C = S_bu.sum(), M_bu.sum(), B_bu.sum(), C_bu.sum()
    amostra = {'secoes': len(kb), 'S': int(tot_S), 'B': int(tot_B), 'M': int(tot_M), 'comparecimento': int(tot_C),
               'S_pct_comp': 100 * tot_S / tot_C, 'M_pct_comp': 100 * tot_M / tot_C, 'SM_pct_comp': 100 * (tot_S + tot_M) / tot_C,
               'S_sobre_M': tot_S / tot_M}
    # faixas do reel na amostra, duas definições
    set_ks = set(ks)
    in_u = np.array([k in set_ks for k in kb])
    idx = {k: i for i, k in enumerate(ks)}
    Lb = np.array([d[k]['2']['L'] for k in kb], float); Rb = np.array([d[k]['2']['R'] for k in kb], float)
    Fm = np.array([faixa_de(int(M_bu[i]), int(C_bu[i])) if C_bu[i] > 0 else -1 for i in range(len(kb))])
    Fsm = np.array([faixa_de(int(M_bu[i] + S_bu[i]), int(C_bu[i])) if C_bu[i] > 0 else -1 for i in range(len(kb))])
    v_ok = (C_bu > 0) & in_u
    amostra['placar_def_M'] = placar_reel(Fm[v_ok], Lb[v_ok], Rb[v_ok])
    amostra['placar_def_S_mais_M'] = placar_reel(Fsm[v_ok], Lb[v_ok], Rb[v_ok])
    P['P3_amostra'] = amostra
    # ---- P4: perfil
    perfil = c['perfil']
    ufs_perfil = sorted({k.split('|')[0] for k in perfil})
    P['P4_perfil_info'] = {'arquivos': info['perfil'], 'ufs': ufs_perfil}
    E = np.array([perfil.get(k, [np.nan, np.nan])[0] for k in ks], float)
    Bio = np.array([perfil.get(k, [np.nan, np.nan])[1] for k in ks], float)
    tem_p = np.isfinite(E) & (E > 0)
    with np.errstate(divide='ignore', invalid='ignore'):
        semcad = np.where(tem_p, (E - Bio) / E, np.nan)
        Shat = C2 * semcad
    # conferência S_hat contra S nos boletins
    ib = np.array([idx.get(k, -1) for k in kb])
    okb = (ib >= 0) & v_ok
    okb &= np.array([tem_p[i] if i >= 0 else False for i in ib])
    sh_b = np.array([Shat[i] if i >= 0 else np.nan for i in ib])
    P4c = {'secoes_amostra_com_perfil': int(okb.sum())}
    if okb.sum() > 10:
        P4c.update({'soma_S': int(S_bu[okb].sum()), 'soma_S_hat': float(sh_b[okb].sum()),
                    'razao_S_sobre_S_hat': float(S_bu[okb].sum() / sh_b[okb].sum()),
                    'correlacao_S_S_hat': float(np.corrcoef(S_bu[okb], sh_b[okb])[0, 1]),
                    'correlacao_fracoes': float(np.corrcoef(S_bu[okb] / C_bu[okb], sh_b[okb] / C_bu[okb])[0, 1]),
                    'erro_absoluto_medio_por_secao': float(np.abs(S_bu[okb] - sh_b[okb]).mean()),
                    'S_medio_por_secao': float(S_bu[okb].mean()),
                    'faixa_igual_com_S_hat': float(np.mean(
                        Fsm[okb] == np.array([faixa_de(int(M_bu[j]) + int(round(sh_b[j])), int(C_bu[j])) for j in np.where(okb)[0]])))})
        cad_b = np.array([perfil[k][0] - perfil[k][1] for k in np.array(kb)[okb]], float)
        P4c['S_sobre_aptos_sem_cadastro'] = float(S_bu[okb].sum() / cad_b.sum())
        P4c['C_sobre_aptos_na_amostra'] = float(C_bu[okb].sum() / np.array([perfil[k][0] for k in np.array(kb)[okb]], float).sum())
    P['P4_conferencia_S_hat'] = P4c
    # placar do reel com S_hat
    k_cal = P4c.get('razao_S_sobre_S_hat', 1.0)
    pl = {}
    cob = tem_p
    pl['cobertura'] = {'secoes_com_perfil': int(cob.sum()), 'secoes_universo': n, 'ufs': ufs_perfil,
                       'margem_Lula_2T_nas_UFs_com_perfil': int((L2[cob] - R2[cob]).sum())}
    if cob.sum() > 0:
        f_rel = np.array([faixa_de(int(NH2[i]) + int(round(Shat[i])), int(C2[i])) if cob[i] else -1 for i in range(n)])
        f_rel_cal = np.array([faixa_de(int(NH2[i]) + int(round(k_cal * Shat[i])), int(C2[i])) if cob[i] else -1 for i in range(n)])
        f_cad = np.array([faixa_de(int(E[i] - Bio[i]), int(E[i])) if cob[i] else -1 for i in range(n)])
        pl['def_NH_mais_S_hat'] = placar_reel(f_rel[cob], L2[cob], R2[cob])
        pl['def_NH_mais_S_hat_calibrado'] = placar_reel(f_rel_cal[cob], L2[cob], R2[cob])
        pl['def_sem_cadastro_sobre_eleitores'] = placar_reel(f_cad[cob], L2[cob], R2[cob])
        pl['def_campo_bweb_nas_mesmas_secoes'] = placar_reel(F[cob], L2[cob], R2[cob])
        pl['soma_NH_mais_S_hat'] = float(NH2[cob].sum() + Shat[cob].sum())
        pl['soma_S_hat'] = float(Shat[cob].sum())
        pl['aptos_perfil'] = float(E[cob].sum()); pl['aptos_sem_cadastro_perfil'] = float((E[cob] - Bio[cob]).sum())
        # P5: regressão com as faixas do reel (fora do critério)
        P['P5_regressao_faixas_reel_pais'] = reg_faixas(y, f_rel, loc, w, ok & cob)
        P['P5_placebo_faixas_reel_pais'] = reg_faixas(np.where(ok, s1, np.nan), f_rel, loc, w, ok & cob)
    P['P4_placar_perfil'] = pl
    # P3: estimativa nacional de S
    rng = np.random.default_rng(SEMENTE)
    kbu = np.array([k.split('|')[0] for k in kb])
    locs_b = np.array([chave_local(k, d[k]['2']) for k in kb])
    sel = v_ok.copy()
    C2_uf = {u: float(C2[ufv == u].sum()) for u in set(ufv)}
    Shat_tot = float(np.nansum(Shat[cob])) if cob.sum() else float('nan')
    ufs_amostra = sorted(set(kbu[sel]))
    est = boot_S(kbu[sel], locs_b[sel], S_bu[sel], C_bu[sel], sh_b[sel], C2_uf, None, Shat_tot, rng, N_BOOT)
    est['ufs_na_amostra'] = ufs_amostra
    est['comparecimento_UFs_fora_da_amostra'] = float(sum(v for u, v in C2_uf.items() if u not in ufs_amostra))
    est['nota_ii'] = 'S_hat nacional só nas UFs com perfil; se faltar UF, (ii) cobre só essas UFs'
    est['NH_2T_universo'] = int(NH2.sum())
    est['NH_mais_S_i'] = int(NH2.sum()) + est['i_razao_S_sobre_C2_por_UF']
    est['NH_mais_S_ii_nas_UFs_com_perfil'] = float(NH2[cob].sum()) + est['ii_razao_S_sobre_S_hat'] if cob.sum() else None
    est['comparecimento_2T_universo'] = int(C2.sum())
    est['com_biometria_i'] = int(C2.sum()) - est['NH_mais_S_i']
    est['reel_15709293_menos_NH'] = REEL['sem_biometria_total'] - int(NH2.sum())
    P['P3_estimativa_nacional'] = est
    # P5 na amostra, com S exato
    locb = locs_b
    s1b = np.array([100 * d[k]['1']['L'] / (d[k]['1']['L'] + d[k]['1']['R']) if d[k]['1']['L'] + d[k]['1']['R'] > 0 else np.nan for k in kb])
    s2b = np.array([100 * d[k]['2']['L'] / (d[k]['2']['L'] + d[k]['2']['R']) if d[k]['2']['L'] + d[k]['2']['R'] > 0 else np.nan for k in kb])
    yb = s2b - s1b; wb = Lb + Rb
    okk = v_ok & np.isfinite(yb) & (Fsm >= 0)
    try:
        P['P5_regressao_amostra_S_mais_M'] = reg_faixas(yb, Fsm, locb, wb, okk)
        P['P5_regressao_amostra_campo_M'] = reg_faixas(yb, Fm, locb, wb, okk)
        P['P5_placebo_amostra_S_mais_M'] = reg_faixas(s1b, Fsm, locb, wb, okk)
        mm = okk & np.isfinite(s1b)
        rr = fe_ols(yb[mm], np.column_stack([100 * S_bu[mm] / C_bu[mm], 100 * M_bu[mm] / C_bu[mm]]), locb[mm], wb[mm],
                    ['pts_S', 'pts_M'])
        P['P5_dose_amostra_S_e_M'] = rr
    except Exception as e:
        P['P5_amostra_erro'] = repr(e)
    # ---- P6 (depois de ver o resultado pela letra; exploratório)
    P6 = {}
    if cob.sum() > 0:
        P6['a_tabela_faixas_reel_pais_S_hat_calibrado'] = tabela_faixas(np.where(f_rel_cal >= 0, f_rel_cal, 0)[cob], L1[cob], R1[cob],
                                                                       L2[cob], R2[cob], C2[cob], NH2[cob])
        P6['a_regressao_faixas_reel_calibrado_pais'] = reg_faixas(y, f_rel_cal, loc, w, ok & cob)
        P6['a_placebo_faixas_reel_calibrado_pais'] = reg_faixas(np.where(ok, s1, np.nan), f_rel_cal, loc, w, ok & cob)
    ordem = {}
    with np.errstate(divide='ignore', invalid='ignore'):
        defs = {'campo_bweb': NH2 / C2}
        if cob.sum() > 0:
            defs['NH_mais_S_hat_calibrado'] = np.where(cob, (NH2 + k_cal * Shat) / C2, np.nan)
            defs['S_hat_calibrado_sozinho'] = np.where(cob, k_cal * Shat / C2, np.nan)
    for nome, v in defs.items():
        m_ = np.isfinite(v)
        ii = np.where(m_)[0][np.argsort(v[m_], kind='stable')]
        lo, hi = ii[:REEL['secoes_0_5']], ii[-REEL['secoes_mais_10']:]
        ordem[nome] = {'menores_45615': {'fatia_Lula': 100 * L2[lo].sum() / (L2[lo] + R2[lo]).sum(), 'margem_Lula': int((L2[lo] - R2[lo]).sum()),
                                         'fracao_max_pct': 100 * float(v[lo].max())},
                       'maiores_271456': {'fatia_Lula': 100 * L2[hi].sum() / (L2[hi] + R2[hi]).sum(), 'margem_Lula': int((L2[hi] - R2[hi]).sum()),
                                          'fracao_min_pct': 100 * float(v[hi].min())}}
    P6['d_ordenacao'] = ordem
    L1b = np.array([d[k]['1']['L'] for k in kb], float); R1b = np.array([d[k]['1']['R'] for k in kb], float)
    P6['a_tabela_faixas_reel_amostra_S_exato'] = tabela_faixas(Fsm[v_ok], L1b[v_ok], R1b[v_ok], Lb[v_ok], Rb[v_ok],
                                                               C_bu[v_ok], M_bu[v_ok])
    if okb.sum() > 10:
        fcal = np.array([faixa_de(int(M_bu[j]) + int(round(k_cal * sh_b[j])), int(C_bu[j])) for j in np.where(okb)[0]])
        conf = np.zeros((3, 3), int)
        for a_, b_ in zip(Fsm[okb], fcal):
            conf[a_, b_] += 1
        P6['b_proxy_calibrado'] = {'k_calibracao': k_cal, 'faixa_igual': float(np.mean(Fsm[okb] == fcal)),
                                   'matriz_linhas_exato_colunas_proxy_ABC': conf.tolist()}
    ld = c.get('logs_dias')
    if ld:
        D1s, D2s = '04/10/2026', '25/10/2026'
        rows = []
        cnt = collections.Counter()
        for k in kb:
            r = ld.get(k)
            if r is None: cnt['sem_log'] += 1; continue
            if 'erro' in r: cnt['erro'] += 1; continue
            a1, a2 = r[D1s], r[D2s]
            c1b, c2b = d[k]['1']['comp'], d[k]['2']['comp']
            comp1 = a1['computados'] == c1b; comp2 = a2['computados'] == c2b
            cnt['completo_2T'] += comp2; cnt['completo_1T'] += comp1
            if comp2 and a2['M'] == b2[k][3]: cnt['M2_igual_NH2_bweb'] += 1
            if comp1 and a1['M'] == b1[k][3]: cnt['M1_igual_NH1_bweb'] += 1
            if comp1 and comp2:
                rows.append((k, a1['B'], a1['S'], a1['M'], a2['B'], a2['S'], a2['M'], c1b, c2b))
        cnt['completos_nos_dois'] = len(rows)
        R_ = np.array([r[1:] for r in rows], float)
        if len(rows):
            B1_, S1_, M1_, B2_, S2_, M2_, CC1, CC2 = R_.T
            dB = B2_ - B1_; dSM = (S2_ + M2_) - (S1_ + M1_); dC = CC2 - CC1
            selp = (dB < 0) & (dSM > 0)
            selm = (dB > 0) & (dSM < 0)
            P6c = {'contagem': dict(cnt), 'soma_1T': {'B': int(B1_.sum()), 'S': int(S1_.sum()), 'M': int(M1_.sum())},
                   'soma_2T': {'B': int(B2_.sum()), 'S': int(S2_.sum()), 'M': int(M2_.sum())},
                   'var_B': int(dB.sum()), 'var_S': int((S2_ - S1_).sum()), 'var_M': int((M2_ - M1_).sum()),
                   'var_comp': int(dC.sum()),
                   'B_caiu_e_SM_subiu': {'secoes': int(selp.sum()), 'pct': 100 * selp.mean(), 'var_B': int(dB[selp].sum()),
                                         'var_SM': int(dSM[selp].sum()), 'var_comp': int(dC[selp].sum()),
                                         'reposicao_pct': 100 * dSM[selp].sum() / -dB[selp].sum() if dB[selp].sum() else None},
                   'B_subiu_e_SM_caiu': {'secoes': int(selm.sum()), 'pct': 100 * selm.mean(), 'var_B': int(dB[selm].sum()),
                                         'var_SM': int(dSM[selm].sum()), 'var_comp': int(dC[selm].sum())},
                   'correlacao_var_B_var_SM': float(np.corrcoef(dB, dSM)[0, 1]),
                   'reel': {'urnas': 95672, 'var_com_bio': -605192, 'var_sem_bio': 606644, 'reposicao_pct': 99.76}}
            ks_r = [r[0] for r in rows]
            pos = {k: i for i, k in enumerate(kb)}
            ii = np.array([pos[k] for k in ks_r])
            ind = selp.astype(float)
            mm = np.isfinite(yb[ii])
            try:
                rr = fe_ols(yb[ii][mm], ind[mm][:, None], locb[ii][mm], wb[ii][mm], ['B_caiu_SM_subiu'])
                P6c['virada_contra_o_mesmo_local'] = rr
                rr2 = fe_ols(s1b[ii][mm], ind[mm][:, None], locb[ii][mm], wb[ii][mm], ['B_caiu_SM_subiu'])
                P6c['placebo_fatia_Lula_1T'] = rr2
            except Exception as e:
                P6c['regressao_erro'] = repr(e)
            P6['c_prova_1_amostra'] = P6c
    P['P6_exploratorio_pos_resultado'] = P6
    P['tempo_s'] = time.time() - t0
    json.dump(P, open(saida_json, 'w'), ensure_ascii=False, indent=1, default=float)
    texto(P, saida_txt)
    log('feito', P['C1_leitura'])


# ------------------------------------------------------------------ texto

def n_(x):
    return f'{int(round(x)):,}'.replace(',', '.')


def f_(x, nd=2):
    if x is None or (isinstance(x, float) and not math.isfinite(x)):
        return 'n/d'
    return f'{x:+.{nd}f}'.replace('.', ',')


def p_(x, nd=2):
    if x is None or (isinstance(x, float) and not math.isfinite(x)):
        return 'n/d'
    return f'{x:.{nd}f}'.replace('.', ',')


def linha_reg(nome, r, cats=('B', 'C')):
    s = f'   {nome}: '
    z = r.get('z') or {c: (r['coef'][c] / r['ep'][c] if r['ep'][c] > 0 else float('nan')) for c in r['coef']}
    s += '  '.join(f"{c} {f_(r['coef'][c], 3)} (ep {p_(r['ep'][c], 3)}, z {f_(z[c], 1)})" for c in r['coef'])
    s += f"; n {n_(r['n'])}, grupos {n_(r['grupos'])}"
    return s


def texto(P, saida):
    L = []
    a = L.append
    a('C1 do Adendo 24: nível contra mudança pelo grau de liberação sem biometria (bweb inteiro), checagem do reel @assis.salvioli')
    a(f"Registro: {P['registro']}. Script: scripts/analisar_C1_reel.py.")
    a('')
    a('1. Extração e conferência')
    e = P['extracao']
    a(f"  Linhas discordantes do cargo 1 na mesma seção: 1º turno {e['linhas_discordantes_1T']}, 2º turno {e['linhas_discordantes_2T']}; valores inválidos do campo: 1º {e['valores_invalidos_1T'] or 'nenhum'}, 2º {e['valores_invalidos_2T'] or 'nenhum'}.")
    a(f"  Conferência com a base e com o cache do F6: {json.dumps(e['conferencia'], ensure_ascii=False)}")
    u = P['universo']
    a(f"  Universo (D2): {n_(u['secoes'])} seções; fora: {json.dumps(u['fora'], ensure_ascii=False)}; com L+R > 0 nos dois turnos: {n_(u['com_L_mais_R_nos_dois_turnos'])}.")
    a(f"  NH no 2º turno {n_(u['NH_2T'])} ({p_(100 * u['NH_2T'] / u['comparecimento_2T'], 3)}% do comparecimento de {n_(u['comparecimento_2T'])}); no 1º turno {n_(u['NH_1T'])}.")
    a(f"  Margem de Lula (27 UFs): 1º turno {n_(u['L1'] - u['R1'])}, 2º turno {n_(u['L2'] - u['R2'])}. Exterior no 2º turno: {n_(P['exterior']['secoes'])} seções, margem {n_(P['exterior']['L2'] - P['exterior']['R2'])}.")
    a(f"  Universos candidatos ao total do reel (492.988 urnas): {json.dumps(P['universos_candidatos'], ensure_ascii=False)}")
    a('')
    a('2. Faixas pela fração NH / comparecimento do 2º turno (D3, D4)')
    t = P['C1_tabela']
    a('  faixa              seções   compar. 2T      NH 2T  margem Lula 1T  margem Lula 2T  margem 1T pts  margem 2T pts  fatia L 1T  fatia L 2T  virada agreg.  virada média')
    for nm, rot in (('A', '0 a 5%'), ('B', '5 a 10%'), ('C', 'mais de 10%')):
        x = t[nm]
        a(f"  {nm} {rot:<12} {n_(x['secoes']):>10} {n_(x['comparecimento_2T']):>12} {n_(x['NH_2T']):>10} {n_(x['margem_Lula_1T']):>15} {n_(x['margem_Lula_2T']):>15} {f_(x['margem_Lula_1T_pts']):>14} {f_(x['margem_Lula_2T_pts']):>14} {p_(x['fatia_Lula_1T']):>11} {p_(x['fatia_Lula_2T']):>11} {f_(x['virada_agregada']):>14} {f_(x['virada_media_ponderada']):>13}")
    a(f"  Parte da margem nacional do 2º turno: A {p_(t['A']['parte_da_margem_nacional_2T_pct'], 1)}%, B {p_(t['B']['parte_da_margem_nacional_2T_pct'], 1)}%, C {p_(t['C']['parte_da_margem_nacional_2T_pct'], 1)}%. Parte da mudança da margem nacional entre os turnos: A {p_(t['A']['parte_da_mudanca_da_margem_nacional_pct'], 1)}%, B {p_(t['B']['parte_da_mudanca_da_margem_nacional_pct'], 1)}%, C {p_(t['C']['parte_da_mudanca_da_margem_nacional_pct'], 1)}%.")
    a('')
    a('3. Regressão registrada (virada contra a faixa, efeito fixo de local, peso L2+R2, erro agrupado por local; A é a referência)')
    r = P['C1_regressao']
    a(linha_reg('principal', r))
    a(f"   Seções que identificam (em locais com mais de uma faixa): {json.dumps(r['identificam'], ensure_ascii=False)}")
    lc = P['C1_leitura']
    a(f"  D6 (faixa C já dava a Lula metade ou mais da margem do 2º turno no 1º): {'sim' if lc['D6_faixa_C_ja_dava_margem_no_1T'] else 'não'}; M1_C = {n_(lc['M1_C'])}, M2_C = {n_(lc['M2_C'])}, razão {p_(lc['M1_C_sobre_M2_C'], 3)}; faixa C acima da margem nacional do 1º turno: {'sim' if lc['faixa_C_acima_da_margem_nacional_1T'] else 'não'}.")
    a(f"  D7 (|B - A| e |C - A| abaixo de 0,5 com ep até 0,25): {'sim' if lc['D7_virada_igual_entre_faixas'] else 'não'}. Critério de sinal (C - A >= 1,0 a mais de 4 ep): {'sim' if lc['criterio_sinal'] else 'não'}.")
    a(f"  VEREDITO: {lc['veredito']} ({lc['motivo']}).")
    gap1 = t['C']['margem_Lula_1T_pts'] - t['A']['margem_Lula_1T_pts']; gap2 = t['C']['margem_Lula_2T_pts'] - t['A']['margem_Lula_2T_pts']
    a(f"  Ao lado (D6, sem mudar o veredito): no 1º turno a faixa C era a única com Lula à frente ({n_(t['C']['margem_Lula_1T'])}), contra {n_(t['A']['margem_Lula_1T'] + t['B']['margem_Lula_1T'])} nas faixas A e B; pela leitura 'faixa C acima da margem nacional do 1º turno' a condição de nível valeria e a leitura seria composição. Distância de margem entre C e A, em pontos dos finalistas: {f_(gap1)} no 1º turno e {f_(gap2)} no 2º.")
    a('')
    a('  Robustez e controles (D8, fora do critério):')
    for k, v in P['C1_robustez'].items():
        a(linha_reg(k, v))
    a('')
    a('  Faixas por UF (seções A/B/C, % de C, fração NH 2T, margem de Lula 2T):')
    a('   ' + '; '.join(f"{u} {v['A']}/{v['B']}/{v['C']} ({p_(v['pct_C'], 1)}%, NH {p_(v['fracao_NH_2T_pct'], 1)}%, {n_(v['margem_Lula_2T'])})" for u, v in P['C1_faixas_por_UF'].items()))
    a('')
    a('4. Placar do reel (pedido da tarefa, fora do Adendo 24; descritivo)')
    R = P['P1_reel']
    a(f"  Tela do reel: 0 a 5% {n_(R['secoes_0_5'])} urnas, Flávio 52 x 48 e +{n_(R['margem_0_5_Flavio'])} para o 22; até 10% {n_(R['secoes_ate_10'])} urnas ({p_(R['pct_ate_10_do_Brasil'], 1)}%), 50,09 x 49,91; mais de 10% {n_(R['secoes_mais_10'])} urnas, +{n_(R['margem_mais_10_Lula'])} para Lula ({p_(R['parte_margem_mais_10'])}% da margem). Total implícito {n_(R['secoes_ate_10'] + R['secoes_mais_10'])} urnas; margem implícita {n_(R['margem_mais_10_Lula'] / R['parte_margem_mais_10'] * 100)}.")

    def bloco(rot, pl):
        a(f"  {rot}:")
        for nm, tt in (('0_a_5', '0 a 5%'), ('5_a_10', '5 a 10%'), ('ate_10', 'até 10%'), ('mais_de_10', 'mais de 10%')):
            x = pl[nm]
            a(f"    {tt:<12} {n_(x['secoes']):>9} seções ({p_(x['pct_secoes'], 2)}%), Lula {p_(x['fatia_Lula'])} x Flávio {p_(x['fatia_Flavio'])}, margem de Lula {n_(x['margem_Lula'])} ({p_(x['parte_da_margem_pct'], 2)}% da margem)")
        a(f"    total {n_(pl['_total']['secoes'])} seções, margem {n_(pl['_total']['margem_Lula'])}")
    bloco('Com o campo do bweb (NH / comparecimento do 2º turno), 27 UFs', P['P1_placar_campo_bweb'])
    a('')
    a('5. O que o boletim diz sobre "sem biometria" (amostra de boletins do 2º turno)')
    b = P['P2_boletins']
    a(f"  Pacotes {n_(b['pacotes'])}, erros de leitura {b['erros_de_leitura']}; conferência: {json.dumps(b['conferencia'], ensure_ascii=False)}")
    a(f"  Campo [2:1] contra o classificador de log do F6 (300 sorteados): {json.dumps(b['validacao_log_300'], ensure_ascii=False)}")
    s = P['P3_amostra']
    a(f"  Amostra: {n_(s['secoes'])} seções, comparecimento {n_(s['comparecimento'])}; sem biometria cadastrada (S) {n_(s['S'])} ({p_(s['S_pct_comp'])}%), com biometria liberados sem ela (M = campo do bweb) {n_(s['M'])} ({p_(s['M_pct_comp'])}%), S + M {p_(s['SM_pct_comp'])}%; S/M = {p_(s['S_sobre_M'], 3)}.")
    bloco('Amostra, definição M (campo do bweb)', s['placar_def_M'])
    bloco('Amostra, definição S + M (toda habilitação que não foi por biometria)', s['placar_def_S_mais_M'])
    est = P['P3_estimativa_nacional']
    a(f"  Estimativa nacional de S: (i) razão S/C2 por UF = {n_(est['i_razao_S_sobre_C2_por_UF'])} (ep {n_(est['ep_i'])}); (ii) razão S/S_hat do perfil = {n_(est['ii_razao_S_sobre_S_hat'])} (ep {n_(est['ep_ii'])}), nas UFs com perfil. UFs na amostra: {len(est['ufs_na_amostra'])}; comparecimento das UFs fora da amostra: {n_(est['comparecimento_UFs_fora_da_amostra'])}.")
    a(f"  NH + S (i) = {n_(est['NH_mais_S_i'])}, contra os 15.709.293 do reel (o reel menos NH = {n_(est['reel_15709293_menos_NH'])}); comparecimento menos (NH + S) = {n_(est['com_biometria_i'])}, contra os 110,9 milhões 'com biometria' da cena 4.")
    a('')
    a('6. Proxy nacional pelo perfil do eleitorado por seção (P4)')
    pi = P['P4_perfil_info']
    a(f"  UFs com perfil: {len(pi['ufs'])} ({', '.join(pi['ufs'])}).")
    c4 = P['P4_conferencia_S_hat']
    a(f"  Conferência S_hat contra S na amostra: {json.dumps(c4, ensure_ascii=False)}")
    pl = P['P4_placar_perfil']
    a(f"  Cobertura: {json.dumps(pl['cobertura'], ensure_ascii=False)}")
    if 'def_NH_mais_S_hat' in pl:
        a(f"  Soma NH + S_hat nas UFs com perfil {n_(pl['soma_NH_mais_S_hat'])}; S_hat {n_(pl['soma_S_hat'])}; aptos sem cadastro biométrico no perfil {n_(pl['aptos_sem_cadastro_perfil'])} de {n_(pl['aptos_perfil'])}.")
        bloco('Definição (NH + S_hat) / comparecimento', pl['def_NH_mais_S_hat'])
        bloco('Definição (NH + S_hat calibrado pela amostra) / comparecimento', pl['def_NH_mais_S_hat_calibrado'])
        bloco('Definição sem cadastro biométrico / eleitores (perfil)', pl['def_sem_cadastro_sobre_eleitores'])
        bloco('Campo do bweb nas mesmas seções', pl['def_campo_bweb_nas_mesmas_secoes'])
    a('')
    a('7. Exploratório, fora do critério (P5): a regressão do C1 com as faixas pela definição do reel')
    for k in ('P5_regressao_faixas_reel_pais', 'P5_placebo_faixas_reel_pais', 'P5_regressao_amostra_S_mais_M',
              'P5_regressao_amostra_campo_M', 'P5_placebo_amostra_S_mais_M'):
        if k in P:
            a(linha_reg(k, P[k]))
    if 'P5_dose_amostra_S_e_M' in P:
        r5 = P['P5_dose_amostra_S_e_M']
        a(f"   P5_dose_amostra_S_e_M: pts_S {f_(r5['coef']['pts_S'], 4)} (ep {p_(r5['ep']['pts_S'], 4)}), pts_M {f_(r5['coef']['pts_M'], 4)} (ep {p_(r5['ep']['pts_M'], 4)}); n {r5['n']}, locais {r5['grupos']}")
    a('')
    a('8. Exploratório acrescentado depois de ver o resultado pela letra (P6; sem veredito)')
    P6 = P.get('P6_exploratorio_pos_resultado', {})
    for chave, rot in (('a_tabela_faixas_reel_pais_S_hat_calibrado', 'Faixas do reel no país, (NH + S_hat calibrado)/C2'),
                       ('a_tabela_faixas_reel_amostra_S_exato', 'Faixas do reel na amostra, (M + S do boletim)/C2')):
        if chave in P6:
            t = P6[chave]
            a(f'  {rot}:')
            for nm, rr in (('A', '0 a 5%'), ('B', '5 a 10%'), ('C', 'mais de 10%')):
                x = t[nm]
                a(f"    {nm} {rr:<12} {n_(x['secoes']):>9} seções; margem de Lula 1T {n_(x['margem_Lula_1T'])} ({f_(x['margem_Lula_1T_pts'])} pts), 2T {n_(x['margem_Lula_2T'])} ({f_(x['margem_Lula_2T_pts'])} pts); fatia de Lula {p_(x['fatia_Lula_1T'])} -> {p_(x['fatia_Lula_2T'])}; virada agregada {f_(x['virada_agregada'])}; parte da mudança da margem {p_(x['parte_da_mudanca_da_margem_nacional_pct'], 1)}%")
    for chave in ('a_regressao_faixas_reel_calibrado_pais', 'a_placebo_faixas_reel_calibrado_pais'):
        if chave in P6:
            a(linha_reg(chave, P6[chave]))
    if 'd_ordenacao' in P6:
        a('  Ordenação (reel: Flávio 52 x 48 nas 45.615 de menor fração; +4.254.754 para Lula nas 271.456 de maior):')
        for nome, v in P6['d_ordenacao'].items():
            a(f"    {nome}: 45.615 menores Lula {p_(v['menores_45615']['fatia_Lula'])}% (margem {n_(v['menores_45615']['margem_Lula'])}, fração até {p_(v['menores_45615']['fracao_max_pct'])}%); 271.456 maiores Lula {p_(v['maiores_271456']['fatia_Lula'])}% (margem {n_(v['maiores_271456']['margem_Lula'])}, fração desde {p_(v['maiores_271456']['fracao_min_pct'])}%)")
    if 'b_proxy_calibrado' in P6:
        a(f"  Proxy calibrado contra S exato na amostra: {json.dumps(P6['b_proxy_calibrado'], ensure_ascii=False)}")
    if 'c_prova_1_amostra' in P6:
        c6 = P6['c_prova_1_amostra']
        a('  "Prova 1" do reel na amostra de logs (S, B, M por dia; seções com log completo nos dois dias):')
        a(f"    {json.dumps(c6['contagem'], ensure_ascii=False)}")
        a(f"    1º turno {json.dumps(c6['soma_1T'])}; 2º turno {json.dumps(c6['soma_2T'])}; variação B {n_(c6['var_B'])}, S {n_(c6['var_S'])}, M {n_(c6['var_M'])}, comparecimento {n_(c6['var_comp'])}; correlação entre var B e var S+M {p_(c6['correlacao_var_B_var_SM'], 3)}")
        x = c6['B_caiu_e_SM_subiu']
        a(f"    Seções onde B caiu e S+M subiu: {n_(x['secoes'])} ({p_(x['pct'], 1)}%); var B {n_(x['var_B'])}, var S+M {n_(x['var_SM'])}, var comparecimento {n_(x['var_comp'])}; reposição {p_(x['reposicao_pct'], 1)}% (reel: 95.672 urnas, -605.192 e +606.644, 99,76%)")
        x = c6['B_subiu_e_SM_caiu']
        a(f"    Espelho, seções onde B subiu e S+M caiu: {n_(x['secoes'])} ({p_(x['pct'], 1)}%); var B {n_(x['var_B'])}, var S+M {n_(x['var_SM'])}, var comparecimento {n_(x['var_comp'])}")
        for kk in ('virada_contra_o_mesmo_local', 'placebo_fatia_Lula_1T'):
            if kk in c6:
                rr = c6[kk]
                a(f"    {kk}: {f_(rr['coef']['B_caiu_SM_subiu'], 3)} (ep {p_(rr['ep']['B_caiu_SM_subiu'], 3)}); n {rr['n']}, locais {rr['grupos']}")
    a('')
    a('Desvios e decisões (o registro não fixou; escritas no docstring antes de rodar): D1 a D8 e P1 a P5 de analisar_C1_reel.py.')
    a('  D3: "0 a 5%" inclui 5% exatos; "5 a 10%" inclui 10% exatos; comparação em inteiros.')
    a('  D6: "a maior parte da margem no 1º turno" lida como M1_C >= 0,5 M2_C, com M2_C > 0.')
    a('  D7: "não difere entre faixas" exige B - A e C - A dentro do limite; o caso intermediário é INCONCLUSIVO.')
    a('  P1 a P5: pedido da tarefa, fora do Adendo 24; descritivo, sem veredito.')
    a('  P6: acrescentado depois de ver o resultado pela letra; exploratório, sem veredito.')
    open(saida, 'w').write('\n'.join(L) + '\n')


def ler_perfis(pastas_perfil, pool):
    zs = []
    for pasta in pastas_perfil:
        zs += sorted(glob.glob(os.path.join(pasta, 'perfil_eleitor_secao_2026_*.zip')))
    perfil = {}; info_perfil = {}; vistos = set(); zs_ok = []
    for z in zs:
        uf = os.path.basename(z).split('_')[-1][:2]
        if uf in vistos:
            continue
        try:
            zipfile.ZipFile(z)
        except zipfile.BadZipFile:
            info_perfil[os.path.basename(z)] = {'erro': 'zip inválido'}; continue
        vistos.add(uf); zs_ok.append(z)
    for nome, out, linhas, inv in pool.imap_unordered(ler_zip_perfil, sorted(zs_ok, key=lambda p: -os.path.getsize(p))):
        perfil.update(out)
        info_perfil[nome] = {'secoes': len(out), 'linhas': linhas, 'invalidos': inv}
        log('perfil', nome, len(out))
    return perfil, info_perfil


def modo_perfil(cache, pastas_perfil):
    """Acrescenta (ou refaz) o perfil por seção no cache da extração."""
    c = carregar(cache)
    with Pool(min(8, os.cpu_count() or 2)) as pool:
        c['perfil'], c['info']['perfil'] = ler_perfis(pastas_perfil, pool)
    with gzip.open(cache, 'wt') as fo:
        json.dump(c, fo)


if __name__ == '__main__':
    modo = sys.argv[1]
    if modo == 'extrair':
        modo_extrair(*sys.argv[2:8], sys.argv[8:])
    elif modo == 'logs_dias':
        modo_logs_dias(sys.argv[2], sys.argv[3])
    elif modo == 'perfil':
        modo_perfil(sys.argv[2], sys.argv[3:])
    elif modo == 'rodar':
        modo_rodar(*sys.argv[2:6])
    else:
        raise SystemExit(__doc__)
