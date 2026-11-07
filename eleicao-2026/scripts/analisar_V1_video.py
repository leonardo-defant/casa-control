"""V1 do Adendo 25: reprodução e origem dos números do vídeo "10 votos extras para Lula por urna".

Registro: PRE-REGISTRO-2026-10-26.md, Adendo 25, V1 (commit 587cc65, 07/11/2026 12:10:37 UTC).
V1 é descritivo e não tem veredito de sinal. Este script não muda limiar nenhum do registro.

Uso (python3 -I sempre):
  python3 -I scripts/analisar_V1_video.py <secoes2026.json.gz> <zips_1t> <zips_2t> <secoes2022.json.gz>
          <secoes2018.json.gz> <pasta_de_trabalho> <saida.json> <saida.txt>
Exemplo:
  python3 -I scripts/analisar_V1_video.py /home/user/trabalho-eleicao/trab2t/secoes2026.json.gz \
      /home/user/trabalho-eleicao/bweb1t/zips /home/user/trabalho-eleicao/trab2t/zips2t \
      /home/user/trabalho-eleicao/dados_ref/secoes2022.json.gz /home/user/trabalho-eleicao/dados_ref/secoes2018.json.gz \
      /home/user/trabalho-eleicao/adendo25/V1 resultados/V1_aritmetica_video.json resultados/V1_aritmetica_video.txt

Afirmações do vídeo (números da tela, pelo resumo do Léo): 4.781.485 votos nominais novos; 497.897 urnas sem o
exterior; 4.781.485 / 497.897 = 9,60; ganho de Lula 10.333.927; "transferência da terceira via" 5.354.957; sobra
4.978.970 = 10 x 497.897; fechamento 5.354.957 + 4.978.970 + 42.767 (exterior) = 10.376.694.

DECISÕES QUE O REGISTRO NÃO FIXA (escritas aqui antes de calcular os resultados; relatadas como desvios)

D1. Universos. Chave da seção "UF|municipio|zona|secao". O exterior aparece como UF "ZZ" (visto na estrutura da
    base: 1.309 chaves no 1º turno, 1.308 no 2º). "27 UFs" = todas as outras UFs. "Total" = 27 UFs + exterior.
    Cada turno é somado sobre todas as seções que têm boletim naquele turno, como o TSE totaliza. A versão
    "pareada" (só seções com boletim nos dois turnos) vai ao lado.
D2. Fonte principal: o bweb dos dois turnos, lido aqui. Para caber no tempo, cada linha só é passada ao csv se
    contiver os bytes ;"Presidente"; e depois o cargo é conferido (CD_CARGO_PERGUNTA 1). A base por seção
    (secoes2026.json.gz, feita com o csv sobre todas as linhas) serve de conferência seção a seção (L, R, O, B,
    N, comparecimento, aptos, urna, tipo, agregação): se as duas leituras baterem em todas as seções, o filtro
    por bytes não perdeu linha. O que foi lido do bweb fica em <pasta_de_trabalho>/bweb{1,2}t_presidente.json.gz
    (pequeno) e é reaproveitado se o script rodar de novo.
D3. Definições. L = NR_VOTAVEL 13, R = 22, O = demais nominais (CD_TIPO_VOTAVEL 1), com o 28 (candidatura
    anulada, que o TSE conta como nulo) contado à parte. B = CD_TIPO_VOTAVEL 2, N = 3; outro tipo, se houver, é
    relatado à parte. "Nominais" = L+R+O com o 28; "válidos" = L+R+O sem o 28. O vídeo diz "nominais"; o
    4.781.485 é procurado nas duas definições, nos três universos, com todas as seções e com as pareadas.
D4. Eliminados no 1º turno = todo NR_VOTAVEL nominal do 1º turno diferente de 13 e 22, com nome (NM_VOTAVEL)
    do próprio bweb. Busca de subconjuntos: elementos = cada eliminado sem o 28, mais o 28, mais brancos, mais
    nulos (cada um pode entrar ou não). Todos os subconjuntos não vazios, em cada universo (27 UFs, exterior,
    total). Critério do registro: |soma - 5.354.957| <= 535. Relato o mais próximo sem brancos e nulos, o mais
    próximo com brancos ou nulos, e quantos ficam dentro da tolerância.
D5. Frações redondas: p = 1,0%, 1,5%, ..., 100,0% (199 valores) de três bases em cada universo: O1 sem o 28;
    O1 com o 28; O1 + B1 + N1 com o 28 (todo voto do 1º turno fora dos finalistas). Distância =
    |p x base - 5.354.957|, sem arredondar o produto.
D6. Estimativas de transferência gravadas no repositório (família d), lista fechada:
    (i) L5 (b), resultados/L5_pesquisas.json, para cada uma das 12 rodadas e para a mediana dos institutos:
        "dos_eliminados_L" (eleitores dos eliminados que a pesquisa manda para Lula) e "do_saldo_L", nas duas
        fidelidades. O "dos_eliminados_L" é refeito aqui com as taxas e os grupos gravados (conferência).
        Erro-padrão da transferência do PoderData final: binomial por grupo com as subamostras estimadas no L5
        (efeito de desenho 1 e 2), sem covariância entre grupos.
    (ii) L5 (b), regressão da urna (so_urna_regressao): b_L_eliminados x eliminados do 1º turno (9.316.747,
        universo do L5) e x O1 sem o 28 das 27 UFs; coef_L_queda_branco_nulo x queda do branco+nulo;
        coef_L_var_comparecimento x aumento do comparecimento; a soma desses dois; a soma dos três;
        coef_L_votos_Flavio_1T x votos de Flávio no 1º turno. Erro-padrão = ep do coeficiente x base (somas sem
        covariância).
    (iii) L5 (b) equivalencia_com_erro_2T: ganho_esperado_L.
    (iv) Contexto da virada (resultados/contexto_virada_2t.json): os números de 2026 em votos (bolo, eliminados,
        aumento do comparecimento, queda dos não válidos). O "ADENDO18 L5b" é o mesmo L5 (b) e já está em (i)-(iii).
    (v) Varredura ampla, ao lado: todo número de L5_pesquisas.json, contexto_virada_2t.json e
        testes_adendo18_com_conferencia.json entre 100.000 e 100.000.000; relato o mais próximo e quantos ficam a
        535 votos ou menos.
D7. Pesquisas finais (família e), L5 (a)/institutos (11 institutos), com os válidos reais gravados no L5
    (V1 = 119.300.786, V2 = 124.082.273) e Lula real no 1º turno do L5: L2p x V2; L1p x V1; L2p x V2 - L1 real
    (ganho implícito); L2p x V2 - L1p x V1; outros1p x V1 (eliminados pela pesquisa); (L2p - L1p) x V2. As
    taxas de transferência das pesquisas estão em (d)(i).
D8. Família extra (fora da lista do registro, declarada aqui antes de calcular, relatada à parte): quantidades dos
    totais que não usam o ganho de Lula nem o número de urnas: O1 - ganho de Flávio; aumento do comparecimento;
    queda do branco+nulo; nominais novos; nos três universos.
D9. Urnas e boletins do 2º turno: boletins = seções com linha de Presidente no bweb do 2º turno, por universo;
    urnas distintas = valores distintos de NR_URNA_EFETIVADA nessas linhas; "urna repetida" = mesmo número em mais
    de um boletim. Seção agregada: boletim com DS_SECOES_AGREGADAS diferente de "#NULO#" e de vazio; o número de
    seções agregadas é a quantidade de números listados no campo (separados por "/", "," ou ";"). Seções
    eleitorais = boletins + seções agregadas. Urna trocada: seção com boletim nos dois turnos e
    NR_URNA_EFETIVADA diferente; tipo de urna diferente de "Apurada" em qualquer turno é contado à parte e junto.
    Referência: secoes_tot do resultado oficial (resultados/soma_oficial_2t.json).
D10. Mesma conta em outros casos. U = boletins do 2º turno nas 27 UFs do ano (2026 pelo bweb; 2022 e 2018 pelas
    bases de referência; nelas, L = Lula em 2022 e Haddad em 2018, R = Bolsonaro, conforme
    scripts/contexto_virada_2t.py, função teste_secoes, que confere as bases contra o oficial). Ganho nas 27 UFs,
    somando todas as seções de cada turno. k em {5, 8, 10, 12, 15} para todos os casos; T(k) = ganho - k x U;
    k de volta = (ganho - T(k)) / U. Casos do registro: Lula e Flávio 2026, Lula e Bolsonaro 2022 (com U de
    2022). Extra, fora do registro: Haddad e Bolsonaro 2018. Ao lado: k implícito, k* = (ganho - T) / U, para
    T vindo das estimativas independentes de (d) (regressão da urna nas 27 UFs e PoderData final).
D11. Identidade contábil: ganho L + ganho R = (nominais 2T - nominais 1T) + O1, que vale se O2 = 0 (conferido).
    Conferida com "nominais" (O1 com o 28) e com "válidos" (O1 sem o 28), nos três universos. Não
    identificabilidade: com só os totais, toda divisão ganho_L = T + V com 0 <= T <= O1 fecha as contas; o vídeo
    escolhe uma. Também mostro o que a divisão do vídeo implica para Flávio, se os "votos novos" fossem os
    nominais novos.
D12. Comparação dos 4.978.970 "votos novos" com os nominais novos (27 UFs e total) e com o aumento do
    comparecimento (27 UFs e total): diferença e razão.

Transparência: antes de escrever este script eu já tinha visto, em arquivos gravados, os válidos oficiais de 2026
(1º turno 119.300.788, 2º 124.082.273, diferença 4.781.485, em resultados/contexto_virada_2t.txt), Lula no 1º turno
53.879.538 (candidatos_1t_2026_totais.txt), o ganho de Lula nas seções com os dois turnos (10.376.696,
L5_pesquisas.txt), as 497.897 seções das 27 UFs (C1) e, na estrutura da base, a seção ZZ|30686|1|443, só com
1º turno (2 votos de Lula). Os testes acima foram desenhados sabendo disso.

ACRESCENTADO DEPOIS DE VER O RESULTADO (exploratório; não muda limiar nem a leitura pela letra):
X1. A primeira rodada achou somas de subconjunto de (b) a 535 votos ou menos de 5.354.957 e contava universos em vez de
    subconjuntos na frase final (erro de contagem, corrigido). Para saber se esses acertos dizem algo, conto, para cada
    número inteiro a até 500.000 votos de 5.354.957, quantos subconjuntos (os mesmos elementos de D4) ficam a 535 votos
    ou menos e a que distância fica o mais próximo; com todos os elementos e só com os eliminados (com o 28); 27 UFs e total.
X2. Somas de grupos políticos dos eliminados (todos; Cury, Renan, Caiado e Zema; Cury, Renan e Caiado; os que apoiaram
    Flávio; os que apoiaram Lula; Renan e Rui Costa Pimenta), pelos apoios gravados em resultados/contexto_virada_2t.txt.
X3. A conta do vídeo com o subconjunto mais próximo no lugar de 5.354.957: sobra, sobra por urna e resto da divisão.
"""
import csv, collections, glob, gzip, itertools, json, math, os, re, sys, zipfile
from multiprocessing import Pool

ALVO = 5354957
TOL = 535
VIDEO = dict(nominais_novos=4781485, urnas=497897, ganho_L_27UF=10333927, transferencia=5354957,
             votos_novos=4978970, exterior=42767, total=10376694, k=10)
PAT = b';"Presidente";'
KS = [5, 8, 10, 12, 15]
AQUI = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.dirname(AQUI)
RES = os.path.join(REPO, 'resultados')


# ---------------------------------------------------------------- leitura do bweb
def ler_zip(zpath):
    z = zipfile.ZipFile(zpath)
    nome = [n for n in z.namelist() if n.lower().endswith('.csv')][0]
    secs = {}
    cand = collections.Counter()
    nomes = {}
    tipos_vot = collections.Counter()
    cont = dict(linhas=0, linhas_filtradas=0, cargo_errado=0, incoerentes=0)
    with z.open(nome) as fh:
        cab = [c.strip().strip('"').replace('SG_ UF', 'SG_UF') for c in fh.readline().decode('latin1').rstrip('\r\n').split(';')]
        ix = {c: i for i, c in enumerate(cab)}

        def filtradas():
            for line in fh:
                cont['linhas'] += 1
                if PAT in line:
                    cont['linhas_filtradas'] += 1
                    yield line.decode('latin1')

        iC, iD = ix['CD_CARGO_PERGUNTA'], ix['DS_CARGO_PERGUNTA']
        iUF, iM, iZ, iS = ix['SG_UF'], ix['CD_MUNICIPIO'], ix['NR_ZONA'], ix['NR_SECAO']
        iTV, iNV, iNM, iQ = ix['CD_TIPO_VOTAVEL'], ix['NR_VOTAVEL'], ix['NM_VOTAVEL'], ix['QT_VOTOS']
        iU, iT, iA, iCo = ix['NR_URNA_EFETIVADA'], ix['DS_TIPO_URNA'], ix['QT_APTOS'], ix['QT_COMPARECIMENTO']
        iAg, iL = ix['DS_SECOES_AGREGADAS'], ix['NR_LOCAL_VOTACAO']
        for r in csv.reader(filtradas(), delimiter=';'):
            if r[iC] != '1' or r[iD] != 'Presidente':
                cont['cargo_errado'] += 1
                continue
            uf = r[iUF]
            k = f"{uf}|{int(r[iM])}|{int(r[iZ])}|{int(r[iS])}"
            tv = int(r[iTV]); nv = int(r[iNV]); q = int(r[iQ])
            base = [r[iU], r[iT], int(r[iA]), int(r[iCo]), r[iAg], int(r[iL])]
            s = secs.get(k)
            if s is None:
                s = secs[k] = base + [0, 0, 0, 0, 0, 0, 0]  # 6 L, 7 R, 8 O(com 28), 9 B, 10 N, 11 c28, 12 outro tipo
            elif s[:6] != base:
                cont['incoerentes'] += 1
            tipos_vot[f'{tv}|{r[ix["DS_TIPO_VOTAVEL"]]}'] += 1
            if tv == 1:
                cand[(uf, nv)] += q
                nomes[nv] = r[iNM]
                if nv == 13: s[6] += q
                elif nv == 22: s[7] += q
                else:
                    s[8] += q
                    if nv == 28: s[11] += q
            elif tv == 2: s[9] += q
            elif tv == 3: s[10] += q
            else: s[12] += q
    return zpath, secs, {f'{u}|{n}': v for (u, n), v in cand.items()}, nomes, dict(tipos_vot), cont


def ler_bweb(pasta, cache):
    if os.path.exists(cache):
        with gzip.open(cache, 'rt') as f:
            d = json.load(f)
        d['de_cache'] = True
        return d
    zips = sorted(glob.glob(os.path.join(pasta, '*.zip')), key=lambda p: -os.path.getsize(p))
    secs, cand, nomes = {}, collections.Counter(), {}
    tipos_vot, cont = collections.Counter(), collections.Counter()
    arquivos = []
    with Pool(4) as p:
        for zp, s, c, nm, tv, ct in p.imap_unordered(ler_zip, zips):
            print('lido', os.path.basename(zp), len(s), ct, flush=True)
            dup = set(s) & set(secs)
            if dup:
                raise SystemExit(f'seção repetida entre arquivos: {list(dup)[:3]}')
            secs.update(s); cand.update(c); nomes.update({str(k): v for k, v in nm.items()})
            tipos_vot.update(tv); cont.update(ct); arquivos.append(os.path.basename(zp))
    d = dict(secs=secs, cand=dict(cand), nomes=nomes, tipos_votavel=dict(tipos_vot), contagens=dict(cont),
             arquivos=sorted(arquivos))
    with gzip.open(cache, 'wt') as f:
        json.dump(d, f, separators=(',', ':'))
    d['de_cache'] = False
    return d


# ---------------------------------------------------------------- utilidades
def univ(k):
    return 'exterior' if k.startswith('ZZ|') else '27UF'


UNIVS = ('27UF', 'exterior', 'total')


def br(x, nd=0):
    if x is None:
        return 'n/d'
    if isinstance(x, float) and (math.isnan(x) or math.isinf(x)):
        return 'n/d'
    s = f'{x:,.{nd}f}'
    return s.replace(',', 'X').replace('.', ',').replace('X', '.')


def pct(x, nd=2):
    return br(100 * x, nd) + '%'


def somar(secs, chaves=None):
    out = {u: collections.Counter() for u in UNIVS}
    for k, s in secs.items():
        if chaves is not None and k not in chaves:
            continue
        u = univ(k)
        for t in (out[u], out['total']):
            t['boletins'] += 1
            t['apt'] += s[2]; t['comp'] += s[3]
            t['L'] += s[6]; t['R'] += s[7]; t['O'] += s[8]; t['B'] += s[9]; t['N'] += s[10]; t['c28'] += s[11]
            t['outro_tipo'] += s[12]
    for t in out.values():
        t['nominais'] = t['L'] + t['R'] + t['O']
        t['validos'] = t['nominais'] - t['c28']
        t['O_sem28'] = t['O'] - t['c28']
        t['N_com28'] = t['N'] + t['c28']
        t['nao_finalistas'] = t['O'] + t['B'] + t['N']
    return {u: dict(v) for u, v in out.items()}


def n_agregadas(agr):
    if not agr or agr == '#NULO#':
        return 0
    return len([x for x in re.split(r'[/,;]', agr) if x.strip()])


def coletar_numeros(x, caminho=''):
    if isinstance(x, bool):
        return
    if isinstance(x, (int, float)):
        yield caminho, x
    elif isinstance(x, dict):
        for k, v in x.items():
            yield from coletar_numeros(v, f'{caminho}/{k}')
    elif isinstance(x, list):
        for i, v in enumerate(x):
            yield from coletar_numeros(v, f'{caminho}[{i}]')


def mais_proximo(itens):
    """itens: lista de (rotulo, valor[, ep]) -> ordena por distância ao alvo."""
    lst = []
    for it in itens:
        rot, v = it[0], it[1]
        ep = it[2] if len(it) > 2 else None
        lst.append(dict(item=rot, valor=v, distancia=abs(v - ALVO), sinal=v - ALVO, ep=ep,
                        dist_em_ep=(abs(v - ALVO) / ep) if ep else None, dentro=abs(v - ALVO) <= TOL))
    lst.sort(key=lambda d: d['distancia'])
    return lst


# ---------------------------------------------------------------- principal
def main():
    a26, z1, z2, a22, a18, trab, saida_json, saida_txt = sys.argv[1:9]
    os.makedirs(trab, exist_ok=True)
    print('lendo bweb do 1º turno', flush=True)
    b1 = ler_bweb(z1, os.path.join(trab, 'bweb1t_presidente.json.gz'))
    print('lendo bweb do 2º turno', flush=True)
    b2 = ler_bweb(z2, os.path.join(trab, 'bweb2t_presidente.json.gz'))
    s1, s2 = b1['secs'], b2['secs']
    J = dict(teste='V1 do Adendo 25 (descritivo)',
             registro='PRE-REGISTRO-2026-10-26.md, Adendo 25, V1, commit 587cc65 (07/11/2026 12:10:37 UTC)',
             video=VIDEO, alvo=ALVO, tolerancia=TOL)
    J['leitura_bweb'] = {t: dict(arquivos=len(b['arquivos']), de_cache=b['de_cache'], secoes=len(b['secs']),
                                 contagens=b['contagens'], tipos_votavel=b['tipos_votavel'])
                         for t, b in (('1', b1), ('2', b2))}

    # ---- conferência com a base por seção
    with gzip.open(a26, 'rt') as f:
        base = json.load(f)
    conf = {}
    for t, ss in (('1', s1), ('2', s2)):
        c = collections.Counter()
        kb = {k for k, v in base.items() if t in v}
        c['so_no_bweb'] = len(set(ss) - kb); c['so_na_base'] = len(kb - set(ss))
        for k in set(ss) & kb:
            s, v = ss[k], base[k][t]
            ok = (s[6] == v['L'] and s[7] == v['R'] and s[8] == v['O'] and s[9] == v['B'] and s[10] == v['N']
                  and s[3] == v['comp'] and s[2] == v['apt'] and int(s[0] or 0) == v['urna'] and s[1] == v['tipo']
                  and s[11] == v.get('c28', 0) and (s[4] if s[4] not in ('', '#NULO#') else None) == v.get('agr'))
            c['iguais' if ok else 'diferentes'] += 1
        conf[t] = dict(c)
    J['conferencia_base'] = conf
    del base

    # ---- 1. totais
    tot1, tot2 = somar(s1), somar(s2)
    par = set(s1) & set(s2)
    p1, p2 = somar(s1, par), somar(s2, par)
    T = {}
    for nome, A, B_ in (('todas', tot1, tot2), ('pareadas', p1, p2)):
        T[nome] = {}
        for u in UNIVS:
            x, y = A[u], B_[u]
            T[nome][u] = dict(
                boletins_1t=x['boletins'], boletins_2t=y['boletins'],
                L1=x['L'], R1=x['R'], O1_com28=x['O'], c28_1=x['c28'], O1_sem28=x['O_sem28'], B1=x['B'], N1=x['N'],
                comp1=x['comp'], apt1=x['apt'], outro_tipo1=x['outro_tipo'],
                L2=y['L'], R2=y['R'], O2=y['O'], B2=y['B'], N2=y['N'], comp2=y['comp'], apt2=y['apt'],
                outro_tipo2=y['outro_tipo'],
                nominais1=x['nominais'], nominais2=y['nominais'], validos1=x['validos'], validos2=y['validos'],
                d_nominais=y['nominais'] - x['nominais'], d_validos=y['validos'] - x['validos'],
                ganho_L=y['L'] - x['L'], ganho_R=y['R'] - x['R'],
                d_comp=y['comp'] - x['comp'], queda_BN=(x['B'] + x['N']) - (y['B'] + y['N']),
                queda_BN_com28=(x['B'] + x['N'] + x['c28']) - (y['B'] + y['N'] + y['c28']))
    J['totais'] = T
    # onde aparecem os números do vídeo
    achados = {}
    for nv, val in (('nominais_novos', VIDEO['nominais_novos']), ('ganho_L_27UF', VIDEO['ganho_L_27UF']),
                    ('exterior', VIDEO['exterior']), ('total', VIDEO['total']), ('urnas', VIDEO['urnas'])):
        hits = []
        for nome in T:
            for u in UNIVS:
                for c, v in T[nome][u].items():
                    if v == val:
                        hits.append(f'{nome}/{u}/{c}')
        achados[nv] = hits
    J['numeros_do_video_encontrados'] = achados

    # ---- 2. boletins, urnas, agregação, troca
    U2 = {}
    for u in UNIVS:
        ks = [k for k in s2 if u == 'total' or univ(k) == u]
        urnas = collections.Counter(s2[k][0] for k in ks)
        agreg = [k for k in ks if n_agregadas(s2[k][4]) > 0]
        n_ag = sum(n_agregadas(s2[k][4]) for k in ks)
        com1 = [k for k in ks if k in s1]
        troca = [k for k in com1 if s1[k][0] != s2[k][0]]
        nao_ap1 = [k for k in com1 if s1[k][1] != 'Apurada']
        nao_ap2 = [k for k in ks if s2[k][1] != 'Apurada']
        troca_ou_tipo = set(troca) | set(nao_ap1) | set(nao_ap2)
        ks1 = [k for k in s1 if u == 'total' or univ(k) == u]
        U2[u] = dict(boletins_2t=len(ks), urnas_distintas_2t=len(urnas),
                     urnas_em_mais_de_um_boletin=sum(1 for v in urnas.values() if v > 1),
                     urna_vazia_ou_zero=sum(1 for k in ks if s2[k][0] in ('', '0')),
                     boletins_com_agregacao=len(agreg), secoes_agregadas=n_ag, secoes_eleitorais_2t=len(ks) + n_ag,
                     boletins_1t=len(ks1), urnas_distintas_1t=len(collections.Counter(s1[k][0] for k in ks1)),
                     boletins_com_agregacao_1t=sum(1 for k in ks1 if n_agregadas(s1[k][4]) > 0),
                     secoes_agregadas_1t=sum(n_agregadas(s1[k][4]) for k in ks1),
                     secoes_com_os_dois_turnos=len(com1), urna_trocada=len(troca),
                     tipo_nao_apurada_1t=len(nao_ap1), tipo_nao_apurada_2t=len(nao_ap2),
                     urna_trocada_ou_tipo_diferente=len(troca_ou_tipo),
                     tipos_urna_2t=dict(collections.Counter(s2[k][1] for k in ks)),
                     tipos_urna_1t=dict(collections.Counter(s1[k][1] for k in ks1)),
                     so_1t=sorted(set(ks1) - set(ks))[:10], so_2t=sorted(set(ks) - set(ks1))[:10])
    try:
        of = json.load(open(os.path.join(RES, 'soma_oficial_2t.json')))
        st = {uf: v['oficial'].get('secoes_tot') for uf, v in of.items()}
        U2['oficial_secoes_tot'] = dict(br=st.get('br'), zz=st.get('zz'),
                                        uf27=sum(v for k, v in st.items() if k not in ('br', 'zz') and v))
    except Exception as e:  # noqa
        U2['oficial_secoes_tot'] = f'não lido: {e}'
    J['urnas'] = U2
    U = U2['27UF']['boletins_2t']

    # ---- 3. origem dos 5.354.957
    O = {}
    O['a_conta'] = dict(ganho=VIDEO['ganho_L_27UF'], k=10, urnas=VIDEO['urnas'],
                        resultado=VIDEO['ganho_L_27UF'] - 10 * VIDEO['urnas'],
                        igual=VIDEO['ganho_L_27UF'] - 10 * VIDEO['urnas'] == ALVO)
    # (b) eliminados
    elim = {}
    for key, v in b1['cand'].items():
        uf, nv = key.split('|'); nv = int(nv)
        if nv in (13, 22):
            continue
        u = 'exterior' if uf == 'ZZ' else '27UF'
        for uu in (u, 'total'):
            elim.setdefault(uu, collections.Counter())[nv] += v
    nomes = b1['nomes']
    tabela_elim = {u: sorted(([nv, nomes.get(str(nv), '?'), q] for nv, q in elim[u].items()), key=lambda x: -x[2])
                   for u in UNIVS}
    busca = {}
    for u in UNIVS:
        el = [(f"{nv} {nomes.get(str(nv), '?')}", q) for nv, q in elim[u].items() if nv != 28]
        el.append(('28 (anulado)', elim[u].get(28, 0)))
        el.append(('brancos', tot1[u]['B']))
        el.append(('nulos', tot1[u]['N']))
        n = len(el)
        sem_bn, com_bn = [], []
        dentro = 0
        lista_dentro = []
        for m in range(1, 1 << n):
            ssum = 0; rot = []
            for i in range(n):
                if m >> i & 1:
                    ssum += el[i][1]; rot.append(el[i][0])
            d = abs(ssum - ALVO)
            if d <= TOL:
                dentro += 1
                lista_dentro.append(dict(distancia=d, soma=ssum, itens=' + '.join(rot)))
            tem_bn = (m >> (n - 1) & 1) or (m >> (n - 2) & 1)
            reg = (d, ssum, ' + '.join(rot))
            if tem_bn:
                com_bn.append(reg)
            else:
                sem_bn.append(reg)
        sem_bn.sort(); com_bn.sort()
        busca[u] = dict(elementos=[[r, q] for r, q in el], subconjuntos=(1 << n) - 1, dentro_da_tolerancia=dentro,
                        lista_dentro=sorted(lista_dentro, key=lambda x: x['distancia']),
                        mais_proximos_sem_branco_nulo=[dict(distancia=d, soma=s, itens=r) for d, s, r in sem_bn[:5]],
                        mais_proximos_com_branco_ou_nulo=[dict(distancia=d, soma=s, itens=r) for d, s, r in com_bn[:5]])
    O['b_eliminados'] = dict(votos_por_eliminado=tabela_elim, busca=busca)
    # (c) frações redondas
    fr = {}
    ps = [x / 2 for x in range(2, 201)]
    for u in UNIVS:
        x = tot1[u]
        bases = {'O1_sem28': x['O_sem28'], 'O1_com28': x['O'], 'O1_mais_B1_N1': x['O'] + x['B'] + x['N']}
        for nb, bv in bases.items():
            lst = sorted(((abs(p / 100 * bv - ALVO), p, p / 100 * bv) for p in ps))
            fr[f'{u}/{nb}'] = dict(base=bv, fracao_exata=ALVO / bv if bv else None,
                                   mais_proximas=[dict(p=p, valor=v, distancia=d) for d, p, v in lst[:3]],
                                   dentro=sum(1 for d, _, _ in lst if d <= TOL))
    O['c_fracoes'] = fr
    # (d) estimativas de transferência
    L5 = json.load(open(os.path.join(RES, 'L5_pesquisas.json')))
    CV = json.load(open(os.path.join(RES, 'contexto_virada_2t.json')))
    A18 = json.load(open(os.path.join(RES, 'testes_adendo18_com_conferencia.json')))
    bL5 = L5['b']; grupos = L5['urna_totais']['grupos']
    itens_d = []
    conf_taxas = {}
    for nome, p in list(bL5['por_pesquisa'].items()) + [('mediana dos institutos', bL5['mediana_institutos'])]:
        for fid in ('fidelidade_100', 'fidelidade_declarada'):
            r = p.get(fid)
            if not r:
                continue
            itens_d.append((f'L5b {nome}: dos eliminados para Lula ({fid})', r['dos_eliminados_L']))
            itens_d.append((f'L5b {nome}: do saldo para Lula ({fid})', r['do_saldo_L']))
        tx = p['taxas']
        refeito = sum(grupos[g] * tx[g][1] for g in grupos)
        conf_taxas[nome] = refeito - p['fidelidade_100']['dos_eliminados_L']
    # ep do PoderData final
    pdf = bL5['por_pesquisa']['PoderData 23-24/10 (final)']
    ep_pd = {}
    for ea in pdf['erro_amostral']:
        var = sum(grupos[g] ** 2 * pdf['taxas'][g][1] * (1 - pdf['taxas'][g][1]) / ea['tamanhos_subamostra'][g]
                  for g in grupos)
        ep_pd[f"deff_{ea['deff']:g}"] = math.sqrt(var)
    T_pd = pdf['fidelidade_100']['dos_eliminados_L']
    itens_d.append(('L5b PoderData final: dos eliminados para Lula, com ep (efeito de desenho 1)', T_pd, ep_pd['deff_1']))
    reg = bL5['so_urna_regressao']; ub = bL5['urna']
    bE, eE = reg['b_L_eliminados_somado']
    bB, eB = reg['coef_L_queda_branco_nulo']
    bC, eC = reg['coef_L_var_comparecimento']
    bF, eF = reg['coef_L_votos_Flavio_1T']
    O27 = tot1['27UF']['O_sem28']
    reg_itens = [
        ('regressão da urna: b_L_eliminados x eliminados (9.316.747, universo do L5)', bE * ub['eliminados_1T'], eE * ub['eliminados_1T']),
        ('regressão da urna: b_L_eliminados x O1 sem o 28 das 27 UFs', bE * O27, eE * O27),
        ('regressão da urna: fatia na queda do branco+nulo x queda', bB * ub['queda_branco_nulo'], eB * ub['queda_branco_nulo']),
        ('regressão da urna: fatia no aumento do comparecimento x aumento', bC * ub['aumento_comparecimento'], eC * ub['aumento_comparecimento']),
        ('regressão da urna: branco+nulo e comparecimento somados', bB * ub['queda_branco_nulo'] + bC * ub['aumento_comparecimento'],
         math.hypot(eB * ub['queda_branco_nulo'], eC * ub['aumento_comparecimento'])),
        ('regressão da urna: eliminados + branco+nulo + comparecimento', bE * ub['eliminados_1T'] + bB * ub['queda_branco_nulo'] + bC * ub['aumento_comparecimento'],
         math.sqrt((eE * ub['eliminados_1T']) ** 2 + (eB * ub['queda_branco_nulo']) ** 2 + (eC * ub['aumento_comparecimento']) ** 2)),
        ('regressão da urna: troca de Flávio para Lula (coef x Flávio 1T)', bF * L5['urna_totais']['F1'], eF * L5['urna_totais']['F1']),
    ]
    itens_d += reg_itens
    itens_d.append(('L5b equivalência: ganho esperado de Lula com o saldo como a pesquisa', bL5['equivalencia_com_erro_2T']['ganho_esperado_L']))
    e26 = CV['eleicoes']['2026'] if '2026' in CV['eleicoes'] else CV['eleicoes'][2026]
    for c, v in coletar_numeros(e26):
        if isinstance(v, (int, float)) and 1e5 <= abs(v) <= 1e8:
            itens_d.append((f'contexto da virada 2026{c}', v))
    d_ord = mais_proximo(itens_d)
    varredura = []
    for nome_arq, obj in (('L5_pesquisas.json', L5), ('contexto_virada_2t.json', CV), ('testes_adendo18_com_conferencia.json', A18)):
        for c, v in coletar_numeros(obj):
            if 1e5 <= v <= 1e8:
                varredura.append((f'{nome_arq}{c}', v))
    v_ord = mais_proximo(varredura)
    O['d_transferencias'] = dict(conferencia_taxas_L5=conf_taxas, ep_PoderData_final=ep_pd,
                                 itens=d_ord, dentro=sum(1 for x in d_ord if x['dentro']),
                                 varredura=dict(numeros=len(v_ord), mais_proximos=v_ord[:5],
                                                dentro=sum(1 for x in v_ord if x['dentro'])))
    # (e) pesquisas finais
    V1r, V2r = L5['a']['real']['validos1'], L5['a']['real']['validos2']
    L1r = L5['urna_totais']['L1']
    itens_e = []
    for it in L5['a']['institutos']:
        n = it['instituto']; L1p, L2p, Op = it['L1_pesquisa'] / 100, it['L2_pesquisa'] / 100, it['outros1_pesquisa'] / 100
        itens_e += [(f'{n}: Lula 2T pesquisa x válidos 2T', L2p * V2r), (f'{n}: Lula 1T pesquisa x válidos 1T', L1p * V1r),
                    (f'{n}: ganho implícito (pesquisa 2T x válidos 2T menos Lula real 1T)', L2p * V2r - L1r),
                    (f'{n}: ganho pelas duas pesquisas', L2p * V2r - L1p * V1r),
                    (f'{n}: eliminados pela pesquisa do 1T x válidos 1T', Op * V1r),
                    (f'{n}: (Lula 2T menos Lula 1T, pesquisa) x válidos 2T', (L2p - L1p) * V2r)]
    e_ord = mais_proximo(itens_e)
    O['e_pesquisas'] = dict(itens=e_ord, dentro=sum(1 for x in e_ord if x['dentro']))
    # (f) extra
    itens_f = []
    for u in UNIVS:
        t = T['todas'][u]
        itens_f += [(f'{u}: O1 sem o 28 menos ganho de Flávio', t['O1_sem28'] - t['ganho_R']),
                    (f'{u}: O1 com o 28 menos ganho de Flávio', t['O1_com28'] - t['ganho_R']),
                    (f'{u}: aumento do comparecimento', t['d_comp']), (f'{u}: queda do branco+nulo', t['queda_BN']),
                    (f'{u}: nominais novos', t['d_nominais']), (f'{u}: válidos novos', t['d_validos'])]
    f_ord = mais_proximo(itens_f)
    O['f_extra'] = dict(itens=f_ord, dentro=sum(1 for x in f_ord if x['dentro']))
    por_familia = dict(b_subconjuntos={u: busca[u]['dentro_da_tolerancia'] for u in UNIVS},
                       c_fracoes=sum(fr[k]['dentro'] for k in fr), d_transferencias=O['d_transferencias']['dentro'],
                       d_varredura=O['d_transferencias']['varredura']['dentro'], e_pesquisas=O['e_pesquisas']['dentro'])
    independentes_dentro = (sum(busca[u]['dentro_da_tolerancia'] for u in UNIVS)
                            + por_familia['c_fracoes'] + por_familia['d_transferencias'] + por_familia['e_pesquisas'])
    O['dentro_da_tolerancia_por_familia'] = por_familia
    O['quantidades_independentes_dentro_da_tolerancia'] = independentes_dentro
    O['clausula_nada_bate'] = independentes_dentro == 0
    O['conclusao_pela_letra'] = ('resíduo da conta (nada bate)' if independentes_dentro == 0 else
                                 'a cláusula "se nada bater" não se cumpre: há somas de subconjunto na tolerância')

    # ---- EXPLORATÓRIO (feito depois de ver o resultado de (b); não muda limiar nem a leitura pela letra)
    import numpy as np
    EXP = dict(nota='exploratório, feito depois de ver que (b) tinha somas de subconjunto dentro da tolerância')
    acaso = {}
    for u in ('27UF', 'total'):
        el = busca[u]['elementos']
        for nome_conj, elems in (('todos os elementos', el),
                                 ('só eliminados, com o 28', [e for e in el if e[0] not in ('brancos', 'nulos')])):
            sums = np.array([0], dtype=np.int64)
            for _, q in elems:
                sums = np.concatenate([sums, sums + q])
            sums = np.sort(sums[1:])
            alvos = np.arange(ALVO - 500000, ALVO + 500001, dtype=np.int64)
            cnt = np.searchsorted(sums, alvos + TOL, 'right') - np.searchsorted(sums, alvos - TOL, 'left')
            i = np.searchsorted(sums, alvos)
            lo = sums[np.clip(i - 1, 0, len(sums) - 1)]; hi = sums[np.clip(i, 0, len(sums) - 1)]
            dmin = np.minimum(np.abs(alvos - lo), np.abs(hi - alvos))
            obs_cnt = int(np.sum(np.abs(sums - ALVO) <= TOL)); obs_d = int(np.min(np.abs(sums - ALVO)))
            acaso[f'{u}/{nome_conj}'] = dict(
                subconjuntos=int(len(sums)), alvos=int(len(alvos)), faixa=[int(alvos[0]), int(alvos[-1])],
                media_acertos_por_alvo=float(cnt.mean()), fracao_alvos_com_1_ou_mais=float((cnt >= 1).mean()),
                acertos_observados=obs_cnt, fracao_alvos_com_pelo_menos_os_observados=float((cnt >= obs_cnt).mean()) if obs_cnt else None,
                menor_distancia_observada=obs_d, fracao_alvos_com_distancia_ate_a_observada=float((dmin <= obs_d).mean()),
                mediana_da_menor_distancia=float(np.median(dmin)))
    EXP['acaso_subconjuntos'] = acaso
    nat = {'todos os eliminados (sem o 28)': [70, 14, 55, 30, 80, 16, 27, 21, 35, 29],
           'Cury, Renan, Caiado e Zema': [70, 14, 55, 30], 'Cury, Renan e Caiado': [70, 14, 55],
           'apoiaram Flávio (Zema, Caiado, Clariana, Cury, Grassi)': [30, 55, 27, 70, 35],
           'apoiaram Lula (Samara, Hertz, Edmilson)': [80, 16, 21], 'Renan (liberou) e Rui Costa Pimenta (PCO, nulo)': [14, 29]}
    EXP['grupos_politicos'] = {u: {g: dict(soma=sum(elim[u].get(nv, 0) for nv in ns),
                                          distancia=abs(sum(elim[u].get(nv, 0) for nv in ns) - ALVO)) for g, ns in nat.items()}
                               for u in ('27UF', 'total')}
    melhor = busca['27UF']['lista_dentro'][0] if busca['27UF']['lista_dentro'] else None
    if melhor:
        Vm = VIDEO['ganho_L_27UF'] - melhor['soma']
        EXP['melhor_subconjunto_na_conta_do_video'] = dict(T=melhor['soma'], itens=melhor['itens'], sobra=Vm,
                                                           sobra_por_urna=Vm / VIDEO['urnas'], resto_da_divisao_por_urnas=Vm % VIDEO['urnas'])
    O['exploratorio'] = EXP
    O['conclusao'] = 'resíduo da conta' if independentes_dentro == 0 else 'resíduo da conta, com ressalva pela letra'
    J['origem_5354957'] = O

    # ---- 4. mesma conta em outros casos
    def ganhos_ref(path):
        with gzip.open(path, 'rt') as f:
            d = json.load(f)
        g = collections.Counter()
        for k, v in d.items():
            if k.startswith('ZZ|'):
                continue
            for t in ('1', '2'):
                if t in v:
                    g['L' + t] += v[t]['L']; g['R' + t] += v[t]['R']; g['n' + t] += 1
        return dict(g)
    g22, g18 = ganhos_ref(a22), ganhos_ref(a18)
    t27 = T['todas']['27UF']
    casos = [('Lula 2026', t27['ganho_L'], U, True), ('Flávio 2026', t27['ganho_R'], U, True),
             ('Lula 2022', g22['L2'] - g22['L1'], g22['n2'], True), ('Bolsonaro 2022', g22['R2'] - g22['R1'], g22['n2'], True),
             ('Haddad 2018 (extra)', g18['L2'] - g18['L1'], g18['n2'], False),
             ('Bolsonaro 2018 (extra)', g18['R2'] - g18['R1'], g18['n2'], False)]
    T_reg27 = bE * O27
    outros = []
    for nome, g, Un, noreg in casos:
        linhas = []
        for k in KS:
            Tk = g - k * Un
            linhas.append(dict(k=k, transferencia=Tk, votos_novos=k * Un, k_de_volta=(g - Tk) / Un,
                               exato=(g - Tk) == k * Un))
        outros.append(dict(caso=nome, no_registro=noreg, ganho=g, urnas=Un, ganho_por_urna=g / Un, contas=linhas))
    J['mesma_conta'] = dict(casos=outros, base_2022=g22, base_2018=g18,
                            k_implicito_Lula_2026=dict(
                                regressao_urna_27UF=dict(T=T_reg27, ep_T=eE * O27, k=(t27['ganho_L'] - T_reg27) / U, ep_k=eE * O27 / U),
                                PoderData_final=dict(T=T_pd, ep_T=ep_pd['deff_1'], k=(t27['ganho_L'] - T_pd) / U, ep_k=ep_pd['deff_1'] / U),
                                mediana_institutos=dict(T=bL5['mediana_institutos']['fidelidade_100']['dos_eliminados_L'],
                                                        k=(t27['ganho_L'] - bL5['mediana_institutos']['fidelidade_100']['dos_eliminados_L']) / U)))

    # ---- 5. identidade e não identificabilidade
    ID = {}
    for nome in T:
        for u in UNIVS:
            t = T[nome][u]
            ID[f'{nome}/{u}'] = dict(
                O2=t['O2'],
                nominais=dict(esquerda=t['ganho_L'] + t['ganho_R'], direita=t['d_nominais'] + t['O1_com28'],
                              diferenca=t['ganho_L'] + t['ganho_R'] - t['d_nominais'] - t['O1_com28']),
                validos=dict(esquerda=t['ganho_L'] + t['ganho_R'], direita=t['d_validos'] + t['O1_sem28'],
                             diferenca=t['ganho_L'] + t['ganho_R'] - t['d_validos'] - t['O1_sem28']),
                comp_menos_BN=t['d_comp'] + t['queda_BN_com28'] - t['d_validos'])
    gL, gR = t27['ganho_L'], t27['ganho_R']
    NI = dict(
        ganho_L=gL, ganho_R=gR, O1_sem28=t27['O1_sem28'], d_validos=t27['d_validos'], d_nominais=t27['d_nominais'],
        divisao_video=dict(T=ALVO, V=gL - ALVO),
        extremos=dict(T_zero=dict(T=0, V=gL), T_maximo=dict(T=min(t27['O1_sem28'], gL), V=gL - min(t27['O1_sem28'], gL))),
        implicacao_para_Flavio=dict(
            votos_novos_de_Flavio_se_os_novos_fossem_os_validos_novos=t27['d_validos'] - (gL - ALVO),
            votos_novos_de_Flavio_com_o_numero_do_video=VIDEO['nominais_novos'] - VIDEO['votos_novos'],
            eliminados_para_Flavio_nesse_caso=gR - (t27['d_validos'] - (gL - ALVO)),
            eliminados_que_sobram_para_ninguem=t27['O1_sem28'] - ALVO - (gR - (t27['d_validos'] - (gL - ALVO)))),
        estimativas_repositorio=dict(
            regressao_urna=dict(fatia=bE, ep=eE, T=T_reg27, ep_T=eE * O27, V=gL - T_reg27),
            PoderData_final=dict(T=T_pd, ep_T_deff1=ep_pd['deff_1'], ep_T_deff2=ep_pd['deff_2'], V=gL - T_pd),
            pesquisas_faixa=dict(minimo=min(p['fidelidade_100']['dos_eliminados_L'] for p in bL5['por_pesquisa'].values()),
                                 maximo=max(p['fidelidade_100']['dos_eliminados_L'] for p in bL5['por_pesquisa'].values()))))
    ID['nao_identificabilidade'] = NI
    cmp_ = {}
    for u in ('27UF', 'total'):
        t = T['todas'][u]
        cmp_[u] = dict(votos_novos_video=VIDEO['votos_novos'], nominais_novos=t['d_nominais'], validos_novos=t['d_validos'],
                       aumento_comparecimento=t['d_comp'],
                       excesso_sobre_validos_novos=VIDEO['votos_novos'] - t['d_validos'],
                       excesso_sobre_comparecimento=VIDEO['votos_novos'] - t['d_comp'],
                       razao_sobre_comparecimento=VIDEO['votos_novos'] / t['d_comp'])
    cmp_['video'] = dict(votos_novos=VIDEO['votos_novos'], nominais_novos_do_video=VIDEO['nominais_novos'],
                         excesso=VIDEO['votos_novos'] - VIDEO['nominais_novos'],
                         por_urna_video=VIDEO['nominais_novos'] / VIDEO['urnas'])
    ID['comparacao_votos_novos'] = cmp_
    J['identidade'] = ID
    J['veredito'] = 'DESCRITIVO'
    with open(saida_json, 'w') as f:
        json.dump(J, f, ensure_ascii=False, indent=1, default=str)
    escrever_txt(J, saida_txt)
    print('ok')


# ---------------------------------------------------------------- texto
def escrever_txt(J, caminho):
    L = []
    w = L.append
    T = J['totais']; t27 = T['todas']['27UF']; tex = T['todas']['exterior']; tt = T['todas']['total']
    U2 = J['urnas']; O = J['origem_5354957']; ID = J['identidade']; NI = ID['nao_identificabilidade']
    w('V1 do Adendo 25: os números do vídeo "10 votos extras para Lula por urna" (reprodução e origem; descritivo)')
    w('Registro: PRE-REGISTRO-2026-10-26.md, Adendo 25, V1 (commit 587cc65, 07/11/2026 12:10:37 UTC). Sem veredito de sinal.')
    w('Script: scripts/analisar_V1_video.py (python3 -I). Números: resultados/V1_aritmetica_video.json.')
    w('Fonte: bweb dos dois turnos (linhas de Presidente), conferido seção a seção com a base secoes2026.json.gz.')
    c1, c2 = J['conferencia_base']['1'], J['conferencia_base']['2']
    w(f"  Conferência com a base: 1º turno {br(c1.get('iguais', 0))} seções iguais, {br(c1.get('diferentes', 0))} diferentes, "
      f"{br(c1.get('so_no_bweb', 0))} só no bweb, {br(c1.get('so_na_base', 0))} só na base; 2º turno {br(c2.get('iguais', 0))} iguais, "
      f"{br(c2.get('diferentes', 0))} diferentes, {br(c2.get('so_no_bweb', 0))} só no bweb, {br(c2.get('so_na_base', 0))} só na base.")
    w('')
    w('1. Os números do vídeo nos dados (todas as seções de cada turno; exterior = UF "ZZ")')
    w('                              27 UFs         exterior          total')
    def lin(rot, c):
        w(f'  {rot:<26}{br(t27[c]):>13}  {br(tex[c]):>15}  {br(tt[c]):>13}')
    for rot, c in (('boletins 1º turno', 'boletins_1t'), ('boletins 2º turno', 'boletins_2t'),
                   ('Lula 1º turno', 'L1'), ('Lula 2º turno', 'L2'), ('ganho de Lula', 'ganho_L'),
                   ('Flávio 1º turno', 'R1'), ('Flávio 2º turno', 'R2'), ('ganho de Flávio', 'ganho_R'),
                   ('eliminados 1T (sem o 28)', 'O1_sem28'), ('28 anulado (1º turno)', 'c28_1'),
                   ('válidos 1º turno', 'validos1'), ('válidos 2º turno', 'validos2'), ('válidos novos', 'd_validos'),
                   ('nominais 1T (com o 28)', 'nominais1'), ('nominais novos (com o 28)', 'd_nominais'),
                   ('brancos 1º turno', 'B1'), ('brancos 2º turno', 'B2'), ('nulos 1º turno (sem 28)', 'N1'),
                   ('nulos 2º turno', 'N2'), ('comparecimento 1º turno', 'comp1'), ('comparecimento 2º turno', 'comp2'),
                   ('aumento do comparecimento', 'd_comp'), ('queda do branco+nulo', 'queda_BN')):
        lin(rot, c)
    ach = J['numeros_do_video_encontrados']
    w(f"  Onde cada número do vídeo aparece exatamente: " + '; '.join(f"{k} {br(J['video'][k])}: {', '.join(v) if v else 'em nenhum'}"
                                                         for k, v in ach.items()))
    w(f"  4.781.485 = válidos novos (sem o 28) do total, Brasil mais exterior, com todas as seções; nas 27 UFs os válidos novos são "
      f"{br(t27['d_validos'])}. O vídeo divide um número que inclui o exterior por um número de urnas que o exclui.")
    w(f"  4.781.485 / 497.897 = {br(4781485 / 497897, 4)}; o certo nas 27 UFs seria {br(t27['d_validos'])} / {br(U2['27UF']['boletins_2t'])} = "
      f"{br(t27['d_validos'] / U2['27UF']['boletins_2t'], 4)}.")
    w(f"  10.333.927 é o ganho de Lula nas 27 UFs ({'sim' if t27['ganho_L'] == 10333927 else 'não'}); 42.767 é o ganho no exterior "
      f"({'sim' if tex['ganho_L'] == 42767 else 'não'}); 10.376.694 é o ganho total ({'sim' if tt['ganho_L'] == 10376694 else 'não'}).")
    pt = T['pareadas']['total']
    w(f"  Só com seções que têm os dois turnos, o ganho total é {br(pt['ganho_L'])} (o exterior tem uma seção só no 1º turno, "
      f"{', '.join(U2['exterior']['so_1t'])}).")
    w('')
    w('2. Urnas, boletins e seções no 2º turno')
    for u in ('27UF', 'exterior', 'total'):
        x = U2[u]
        w(f"  {u}: boletins {br(x['boletins_2t'])}; urnas distintas (NR_URNA_EFETIVADA) {br(x['urnas_distintas_2t'])}; urna em mais de um "
          f"boletim {br(x['urnas_em_mais_de_um_boletin'])}; boletins com seção agregada {br(x['boletins_com_agregacao'])} "
          f"({br(x['secoes_agregadas'])} seções agregadas; seções eleitorais {br(x['secoes_eleitorais_2t'])}); urna trocada entre os turnos "
          f"{br(x['urna_trocada'])}; tipo diferente de apurada {br(x['tipo_nao_apurada_1t'])} (1º) e {br(x['tipo_nao_apurada_2t'])} (2º); "
          f"troca ou tipo {br(x['urna_trocada_ou_tipo_diferente'])}.")
    w(f"  Oficial (secoes_tot): {U2['oficial_secoes_tot']}.")
    w(f"  497.897 é o número de boletins (seções com boletim) do 2º turno nas 27 UFs ({'sim' if U2['27UF']['boletins_2t'] == 497897 else 'não'}) e "
      f"também o de urnas distintas ({'sim' if U2['27UF']['urnas_distintas_2t'] == 497897 else 'não'}). Não é o número de seções eleitorais "
      f"({br(U2['27UF']['secoes_eleitorais_2t'])}, contando as agregadas).")
    w('')
    w('3. De onde vêm os 5.354.957')
    a = O['a_conta']
    w(f"  (a) 10.333.927 menos 10 x 497.897 = {br(a['resultado'])} ({'igual' if a['igual'] else 'diferente'}). O número sai da própria conta.")
    w(f"  Critério do registro: alguma quantidade calculada sem o ganho de Lula e sem o número de urnas a 535 votos ou menos.")
    bb = O['b_eliminados']
    w('  (b) Votos de cada eliminado no 1º turno (bweb):')
    w('      ' + '; '.join(f"{nv} {nm} {br(q)}" for nv, nm, q in bb['votos_por_eliminado']['total']) + ' (total)')
    w('      27 UFs: ' + '; '.join(f"{nv} {br(q)}" for nv, nm, q in bb['votos_por_eliminado']['27UF']))
    w('      exterior: ' + '; '.join(f"{nv} {br(q)}" for nv, nm, q in bb['votos_por_eliminado']['exterior']))
    for u in ('27UF', 'exterior', 'total'):
        x = bb['busca'][u]
        m1 = x['mais_proximos_sem_branco_nulo'][0]; m2 = x['mais_proximos_com_branco_ou_nulo'][0]
        w(f"      {u}: {br(x['subconjuntos'])} subconjuntos, {x['dentro_da_tolerancia']} a 535 votos ou menos. Mais próximo sem branco e nulo: "
          f"{br(m1['soma'])} (distância {br(m1['distancia'])}: {m1['itens']}); com branco ou nulo: {br(m2['soma'])} (distância "
          f"{br(m2['distancia'])}: {m2['itens']}).")
    w('  (c) Frações redondas (1% a 100%, passo 0,5%):')
    for k, x in O['c_fracoes'].items():
        m = x['mais_proximas'][0]
        w(f"      {k}: base {br(x['base'])}; fração exata {pct(x['fracao_exata'], 3) if x['fracao_exata'] else 'n/d'}; mais próxima "
          f"{br(m['p'], 1)}% = {br(m['valor'], 1)} (distância {br(m['distancia'], 1)}); dentro {x['dentro']}.")
    d = O['d_transferencias']
    w(f"  (d) Estimativas de transferência do repositório ({len(d['itens'])} números; dentro da tolerância: {d['dentro']}). As 5 mais próximas:")
    for x in d['itens'][:5]:
        e = f", ep {br(x['ep'])}, distância de {br(x['dist_em_ep'], 1)} ep" if x['ep'] else ''
        w(f"      {x['item']}: {br(x['valor'])} (distância {br(x['distancia'])}{e})")
    w(f"      Conferência das taxas do L5 (refeito menos gravado): máx. |dif| {br(max(abs(v) for v in d['conferencia_taxas_L5'].values()), 2)}.")
    w(f"      Varredura ampla ({br(d['varredura']['numeros'])} números de 100 mil a 100 milhões em três JSON): mais próximo "
      f"{d['varredura']['mais_proximos'][0]['item']} = {br(d['varredura']['mais_proximos'][0]['valor'], 1)} (distância "
      f"{br(d['varredura']['mais_proximos'][0]['distancia'], 1)}); dentro {d['varredura']['dentro']}.")
    e = O['e_pesquisas']
    w(f"  (e) Pesquisas finais do L5 ({len(e['itens'])} números; dentro {e['dentro']}). Mais próximas:")
    for x in e['itens'][:3]:
        w(f"      {x['item']}: {br(x['valor'])} (distância {br(x['distancia'])})")
    f_ = O['f_extra']
    w(f"  Extra, fora do registro (totais sem o ganho de Lula e sem urnas; dentro {f_['dentro']}). Mais próximas:")
    for x in f_['itens'][:3]:
        w(f"      {x['item']}: {br(x['valor'])} (distância {br(x['distancia'])})")
    pf = O['dentro_da_tolerancia_por_familia']
    w(f"  Resultado pela letra: dentro de 535 votos ficam {pf['b_subconjuntos']['27UF']} somas de subconjunto nas 27 UFs, "
      f"{pf['b_subconjuntos']['exterior']} no exterior e {pf['b_subconjuntos']['total']} no total (família b); frações {pf['c_fracoes']}; "
      f"transferências do repositório {pf['d_transferencias']} (varredura {pf['d_varredura']}); pesquisas {pf['e_pesquisas']}.")
    for u in ('27UF', 'total'):
        for x in O['b_eliminados']['busca'][u]['lista_dentro']:
            w(f"      na tolerância, {u}: {br(x['soma'])} (distância {br(x['distancia'])}): {x['itens']}")
    w(f"  Como há somas na tolerância, a cláusula do registro 'se nada bater, fica registrado como resíduo' não se cumpre pela letra.")
    EX = O['exploratorio']
    w('  Exploratório (feito depois de ver esses acertos; não muda limiar nem a leitura pela letra):')
    for k, x in EX['acaso_subconjuntos'].items():
        w(f"      {k}: {br(x['subconjuntos'])} subconjuntos; um número inteiro qualquer entre {br(x['faixa'][0])} e {br(x['faixa'][1])} "
          f"tem em média {br(x['media_acertos_por_alvo'], 2)} subconjuntos a 535 votos ou menos; {pct(x['fracao_alvos_com_1_ou_mais'], 1)} desses números "
          f"têm pelo menos um"
          + (f", {pct(x['fracao_alvos_com_pelo_menos_os_observados'], 1)} têm {x['acertos_observados']} ou mais (5.354.957 tem {x['acertos_observados']})"
             if x['acertos_observados'] else ' (5.354.957 tem 0)')
          + f"; {pct(x['fracao_alvos_com_distancia_ate_a_observada'], 1)} têm um subconjunto a {br(x['menor_distancia_observada'])} votos ou menos "
          f"(a menor distância achada para 5.354.957).")
    for u in ('27UF', 'total'):
        w(f"      grupos políticos, {u}: " + '; '.join(f"{g} {br(x['soma'])} (distância {br(x['distancia'])})"
                                                      for g, x in EX['grupos_politicos'][u].items()))
    if 'melhor_subconjunto_na_conta_do_video' in EX:
        m = EX['melhor_subconjunto_na_conta_do_video']
        w(f"      Com o subconjunto mais próximo no lugar dos 5.354.957, a sobra seria {br(m['sobra'])} = {br(m['sobra_por_urna'], 5)} por urna "
          f"(resto {br(m['resto_da_divisao_por_urnas'])} na divisão por 497.897): o '10 exato' só sai com o resíduo.")
    w(f"  Leitura: os acertos são combinações sem sentido político (misturam candidatos que apoiaram Flávio, Lula e o nulo, com o 28 "
      f"anulado), nenhum é exato, e o número de acertos é o que qualquer alvo dessa faixa tem por acaso. Nenhuma estimativa de "
      f"transferência nem número de pesquisa chega perto. O 5.354.957 só sai exato como 10.333.927 menos 10 x 497.897.")
    w('')
    w('4. A mesma conta em outros casos: com a "transferência" escolhida como ganho menos k x urnas, qualquer k sai exato')
    for c in J['mesma_conta']['casos']:
        w(f"  {c['caso']}: ganho {br(c['ganho'])}, urnas (boletins do 2º turno, 27 UFs) {br(c['urnas'])}, ganho por urna {br(c['ganho_por_urna'], 2)}")
        w('     ' + '; '.join(f"k={x['k']}: transferência {br(x['transferencia'])}, sobra {br(x['votos_novos'])} = {x['k']} x urnas"
                              for x in c['contas']))
    ki = J['mesma_conta']['k_implicito_Lula_2026']
    w(f"  Com uma transferência estimada de forma independente, o 'k' não sai inteiro: regressão da urna T = {br(ki['regressao_urna_27UF']['T'])} "
      f"(ep {br(ki['regressao_urna_27UF']['ep_T'])}) dá k = {br(ki['regressao_urna_27UF']['k'], 3)} (ep {br(ki['regressao_urna_27UF']['ep_k'], 3)}); "
      f"PoderData final T = {br(ki['PoderData_final']['T'])} (ep {br(ki['PoderData_final']['ep_T'])}) dá k = {br(ki['PoderData_final']['k'], 2)} "
      f"(ep {br(ki['PoderData_final']['ep_k'], 2)}); mediana dos institutos T = {br(ki['mediana_institutos']['T'])} dá k = {br(ki['mediana_institutos']['k'], 2)}.")
    w('  Esse k é só o resto médio por urna: inclui o que Lula ganhou com a queda do branco+nulo, com o aumento do comparecimento e com a')
    w('  troca entre as bases, que a mesma regressão atribui em parte a Lula (L5b). Um resto médio por urna existe para qualquer candidato e')
    w('  qualquer eleição; ele não diz que cada urna recebeu o mesmo acréscimo. Essa é a pergunta do V2.')
    w('')
    w('5. Identidade contábil: ganho de Lula + ganho de Flávio = nominais novos + votos dos eliminados no 1º turno')
    for k in ('todas/27UF', 'todas/exterior', 'todas/total', 'pareadas/total'):
        x = ID[k]
        w(f"  {k}: O2 = {x['O2']}; com o 28 como nominal {br(x['nominais']['esquerda'])} = {br(x['nominais']['direita'])} (diferença "
          f"{x['nominais']['diferenca']}); em válidos {br(x['validos']['esquerda'])} = {br(x['validos']['direita'])} (diferença {x['validos']['diferenca']}).")
    w(f"  A divisão do ganho de Lula ({br(NI['ganho_L'])}, 27 UFs) entre transferência T e votos novos V não é identificável pelos totais:")
    w(f"  os totais dão duas equações (ganho de Lula e de Flávio) e há mais incógnitas (eliminados para Lula, para Flávio e para ninguém;")
    w(f"  branco, nulo e abstenção para cada lado; troca entre as bases; quem votou no 1º turno e faltou no 2º). Qualquer T de 0 a")
    w(f"  {br(NI['extremos']['T_maximo']['T'])} (todos os eliminados) fecha as mesmas contas; o vídeo escolheu T = 5.354.957 sem mostrar a origem.")
    im = NI['implicacao_para_Flavio']
    w(f"  O que a divisão do vídeo implica: se os 'votos novos' fossem os válidos novos das 27 UFs ({br(NI['d_validos'])}), Flávio teria "
      f"{br(im['votos_novos_de_Flavio_se_os_novos_fossem_os_validos_novos'])} votos novos (negativo), e o ganho dele ({br(NI['ganho_R'])}) "
      f"exigiria {br(im['eliminados_para_Flavio_nesse_caso'])} votos dos eliminados (pela identidade, essa leitura põe todo eleitor dos "
      f"eliminados num dos dois; sobram {br(im['eliminados_que_sobram_para_ninguem'])}). Com os números do próprio vídeo, 4.781.485 menos "
      f"4.978.970 = {br(im['votos_novos_de_Flavio_com_o_numero_do_video'])}.")
    er = NI['estimativas_repositorio']
    w(f"  O que o repositório estima para essa divisão: regressão da urna (L5b, ecológica, mesmo local) {pct(er['regressao_urna']['fatia'], 2)} "
      f"(ep {pct(er['regressao_urna']['ep'], 2)}) dos eliminados para Lula, T = {br(er['regressao_urna']['T'])} (ep {br(er['regressao_urna']['ep_T'])}) "
      f"nas 27 UFs, V = {br(er['regressao_urna']['V'])}; pesquisas (L5b, taxas declaradas) T de {br(er['pesquisas_faixa']['minimo'])} a "
      f"{br(er['pesquisas_faixa']['maximo'])}; PoderData final {br(er['PoderData_final']['T'])} (ep {br(er['PoderData_final']['ep_T_deff1'])} "
      f"com efeito de desenho 1, {br(er['PoderData_final']['ep_T_deff2'])} com 2). As duas fontes discordam entre si (é o erro do 2º turno do L5a);")
    w(f"  distância a 5.354.957: regressão {br(ALVO - er['regressao_urna']['T'])} votos "
      f"({br(abs(ALVO - er['regressao_urna']['T']) / er['regressao_urna']['ep_T'], 1)} ep); pesquisas de "
      f"{br(ALVO - er['pesquisas_faixa']['maximo'])} a {br(ALVO - er['pesquisas_faixa']['minimo'])} votos.")
    cv = ID['comparacao_votos_novos']
    w(f"  Os 4.978.970 'votos novos' do vídeo passam dos válidos novos que ele mesmo cita (4.781.485) em {br(cv['video']['excesso'])}, "
      f"dos válidos novos das 27 UFs ({br(cv['27UF']['validos_novos'])}) em {br(cv['27UF']['excesso_sobre_validos_novos'])}, e do aumento do "
      f"comparecimento nas 27 UFs ({br(cv['27UF']['aumento_comparecimento'])}) em {br(cv['27UF']['excesso_sobre_comparecimento'])} "
      f"({br(cv['27UF']['razao_sobre_comparecimento'], 2)} vezes). 'Votos acrescentados' sem eleitor a mais exigiriam comparecimento a mais;")
    w(f"  o aumento real de comparecimento dá {br(cv['27UF']['aumento_comparecimento'] / J['urnas']['27UF']['boletins_2t'], 2)} eleitores por urna, para os dois candidatos juntos.")
    w('')
    w('6. Conclusão (DESCRITIVO)')
    w(f"  Números do vídeo achados exatamente nos dados: " + '; '.join(f"{br(J['video'][k])} {'sim' if v else 'não'}" for k, v in ach.items()) + '.')
    if O['quantidades_independentes_dentro_da_tolerancia'] == 0:
        w(f"  O 5.354.957 não tem origem independente: nenhum eliminado, nenhuma soma de eliminados (com ou sem branco e nulo), nenhuma")
        w(f"  fração redonda, nenhuma estimativa de transferência do repositório e nenhum número das pesquisas finais fica a 535 votos ou")
        w(f"  menos dele. Ele é 10.333.927 menos 10 x 497.897: a igualdade '4.978.970 = 10 x 497.897' é construída pela escolha da")
        w(f"  transferência. A mesma escolha dá qualquer k para Lula, para Flávio e para 2022.")
    else:
        pf = O['dentro_da_tolerancia_por_familia']
        w(f"  Origem do 5.354.957: resíduo da conta (10.333.927 menos 10 x 497.897, exato), com uma ressalva pela letra. Na busca de")
        w(f"  subconjuntos, {pf['b_subconjuntos']['27UF']} somas nas 27 UFs e {pf['b_subconjuntos']['total']} no total ficam a 535 votos ou menos (a melhor a "
          f"{br(O['b_eliminados']['busca']['27UF']['lista_dentro'][0]['distancia'])} votos),")
        w(f"  então a cláusula 'se nada bater' não se cumpre literalmente. O exploratório mostra que esses acertos são o que qualquer número")
        w(f"  dessa faixa tem por acaso, que nenhum é exato nem é um grupo político, e as outras famílias (frações, transferências estimadas,")
        w(f"  pesquisas) não chegam perto. A igualdade '4.978.970 = 10 x 497.897' é construída pela escolha da transferência; a mesma")
        w(f"  escolha dá qualquer k para Lula, para Flávio e para 2022.")
    w(f"  O V1 não testa se houve acréscimo fixo por urna; isso é o V2.")
    w('')
    w('Desvios e decisões fora do registro (escritas no docstring antes de calcular): D1 a D12 do script. Os principais: universo')
    w('"27 UFs" = UF diferente de ZZ e todas as seções de cada turno (pareadas ao lado); o 28 tratado nas duas definições; elementos')
    w('da busca de subconjuntos (eliminados, o 28, brancos e nulos); três bases para as frações; lista fechada de estimativas de')
    w('transferência e de números das pesquisas, mais uma varredura de todos os números de três JSON; família extra (O1 menos ganho')
    w('de Flávio, comparecimento, branco+nulo), fora do registro; Haddad e Bolsonaro 2018, fora do registro; erro-padrão das')
    w('transferências da regressão (ep do coeficiente vezes a base) e do PoderData final (binomial com as subamostras do L5).')
    w('Exploratório, feito depois de ver o resultado (X1 a X3 no docstring): acaso das somas de subconjunto, grupos políticos dos')
    w('eliminados e a conta do vídeo com o subconjunto mais próximo. A primeira rodada contava universos em vez de subconjuntos na')
    w('frase de resultado (dizia 2 em vez de 4); corrigido antes desta versão.')
    txt = '\n'.join(L) + '\n'
    for ch in (chr(0x2014), chr(0x2013)):
        if ch in txt:
            raise SystemExit('travessão no texto')
    with open(caminho, 'w') as f:
        f.write(txt)


if __name__ == '__main__':
    main()
