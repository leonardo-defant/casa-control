"""R27_A4 (Adendo 27, onda A, teste A4): CURVA POR FORÇA COM A SÉRIE LONGA.
Fragilidade "T35 (curva de perda própria por força local do adversário)" de registro/adendo27/equipe_vermelha_relatorio.json,
com a ponderação principal fixada no Adendo 27 do PRE-REGISTRO-2026-10-26.md (commit 2748895, 10/11/2026 00:16:42 UTC).
Docstring escrito em 10/11/2026, por volta de 01:45 UTC, ANTES de somar ou regredir qualquer voto de 2002, 2006 e 2010 e
antes de recalcular qualquer A. Não havia execução anterior deste teste em disco (sem script, sem pasta A4).

O QUE EU JÁ TINHA VISTO AO ESCREVER ISTO
- Os números publicados: resultados/T35_curva_forca_bweb.json (2018, 2022 e 2026, faixa a faixa, nas seções de 2026) e
  resultados/F21_serie_anos.json e .txt (2014, 2018, 2022 e 2026 nas 331.087 seções comuns), e a conta da equipe vermelha
  com pesos iguais (2026 -0,0381; 2014 -0,034; 2022 +0,034). Portanto o sinal de A em 2014, 2018, 2022 e 2026 já é
  conhecido, e já se sabe que 2022 (Bolsonaro no governo) tem A positivo: "A acompanha o PT em todos os anos" já está
  contrariado por 2022 antes de eu rodar. O que é novo e decide é 2002, 2006 e 2010.
- A estrutura do arquivo votacao_secao_2002_BR.zip (cabeçalho, códigos de votável, contagem de linhas por código, UFs,
  validade do número do local). Nenhuma soma de votos, nenhuma regressão de 2002, 2006 ou 2010.
- Não vi: nenhum valor de A de 2002, 2006 e 2010; os A de pesos iguais de 2014, 2018 e 2022 no universo próprio de cada ano.

O QUE O REGISTRO FIXA (aplicado pela letra)
- Estatística A do T35 (Adendo 15): faixas pela fatia do adversário no 1º turno entre os válidos do local de votação
  (menos de 35%, 35 a 50%, 50 a 65%, 65% ou mais); em cada faixa a regressão do T8 sem grupos (variação dos votos do
  candidato entre os turnos contra outros do 1º turno, queda do branco+nulo, variação do comparecimento, adversário no 1º
  turno, próprios no 1º turno), efeito fixo de local por candidato, as duas candidaturas empilhadas, erro CR1 agrupado por
  local; d = coeficiente próprio da direita menos coeficiente próprio da esquerda (PT); só entram faixas em que as duas
  candidaturas têm pelo menos 30 locais com 2 ou mais seções.
- Ponderação principal (Adendo 27): pesos iguais nas quatro faixas. Ao lado: inverso da variância (a original) e peso por votos.
- Série: 2002, 2006 e 2010 pela votação por seção do TSE, com 2014, 2018, 2022 e 2026. PT = 13 (esquerda, L). Adversário
  (direita, R): 45 em 2002 (Serra), 2006 (Alckmin), 2010 (Serra) e 2014 (Aécio); 17 em 2018; 22 em 2022 e 2026.
- Governo candidato: 2002 PSDB (Serra, lado R); 2006, 2010, 2014 e 2026 PT (lado L); 2022 Bolsonaro (lado R); 2018 sem.
- Critério (equipe vermelha, fragilidade T35, campo criterio_proposto):
  INDÍCIO além da incumbência: |A de pesos iguais| de 2026 acima do maior |A| dos anos com governo candidato em 0,015 ou
  mais, a mais de 3 vezes o ruído entre conjuntos de seções (0,01, F21 item 7).
  SEM SINAL: 2026 a até 0,010 do espelho de 2022 e de 2014.
- Aviso do registro que vale aqui: o reteste foi escolhido por quem já conhecia os resultados antigos; o Léo suspeita
  também de 2014, 2018 e 2022, então esses anos (e 2002 a 2010) não são régua limpa. O valor bruto de 2026 vai ao lado de
  toda comparação.

O QUE O REGISTRO NÃO FIXA, DECIDIDO AQUI ANTES DE CALCULAR (relatado como desvio)
D1. Código próprio. A regressão é refeita por somas dentro do local (numpy), sem importar analisar_curva_forca.py nem
    lib.py. Conferência obrigatória antes de ler qualquer resultado novo: reproduzir, na ponderação original (inverso da
    variância), (a) o T35 publicado (2018 e 2022 nas chaves de 2026 com os dois turnos, 2026 inteiro) e (b) o F21 publicado
    (2014, 2018, 2022 e 2026 nas 331.087 seções comuns, e 2014 no universo r2). Tolerância: mesmas contagens de seções e
    locais, e diferença absoluta de até 5e-7 em cada d, em cada erro-padrão e em A. Se não reproduzir, paro e relato.
D2. Universo principal: "universo próprio do ano" = todas as seções da base do ano com 1º e 2º turno, sem filtro de tipo,
    com exterior (como a função publicada). É a única definição aplicável igual aos sete anos, e para 2026 é o número do
    JSON publicado que o Adendo 27 cita (-0,0381). Ao lado, com o mesmo critério aplicado em cada um: U_T35 (2018, 2022 e
    2026 nas chaves de 2026), U_F21 (2014 a 2026 nas seções comuns aos quatro anos), U_0210 (2002, 2006 e 2010 nas seções
    comuns aos três, pela chave UF|município|zona|seção) e U_7 (seções comuns aos sete anos, se sobrar pelo menos 30
    locais por candidato em 3 das 4 faixas em todos os anos; o tamanho é relatado de qualquer modo).
    "Ruído entre conjuntos de seções" medido aqui: maior diferença absoluta do A de pesos iguais do mesmo ano entre os
    universos em que o ano foi calculado.
D3. Ponderações. Principal: média simples de d nas faixas válidas do ano. Se um ano tiver menos de quatro faixas válidas,
    o A de pesos iguais é a média das faixas válidas, o ano é marcado, e relato também todos os anos só nas faixas válidas
    nos sete anos ("faixas comuns"). Erro-padrão do A de pesos iguais: (a) como na conta da equipe vermelha, raiz da soma
    das variâncias dividida pelo número de faixas (faixas tratadas como independentes); (b) agrupado por local também
    entre as faixas (função de influência por local, o mesmo local pode estar numa faixa para um candidato e noutra para
    o outro). Ao lado: inverso da variância (original); peso por votos (peso da faixa = votos de 1º turno dos dois
    finalistas nas seções deles da faixa); peso pelas seções da direita na faixa (reproduz o -0,0304 da equipe vermelha);
    e "cada um com os seus votos" (média do coeficiente próprio de cada candidato pesada pelos votos dele, depois a
    diferença). Nenhuma das ponderações ao lado decide.
D4. Leitura do critério.
    Anos de comparação ("anos com governo candidato"): 2002, 2006, 2010, 2014 e 2022 (2026 é o alvo; 2018 fica fora).
    E = |A_iguais(2026)| - max |A_iguais(ano)| nesses anos.
    INDÍCIO (escrevo SINAL no veredito): E >= 0,015 E E > 3 x 0,01 = 0,03. Pela letra o ruído é o número do registro
    (0,01), o que torna a segunda condição a que manda (E > 0,03). Ao lado, a leitura com o ruído medido aqui (D2):
    E >= 0,015 e E > 3 x ruído medido. Se as duas leituras divergirem, o veredito diz.
    SEM SINAL: |A_iguais(2026) - (-A_iguais(2022))| <= 0,010 E |A_iguais(2026) - A_iguais(2014)| <= 0,010 ("espelho" só
    de 2022, porque em 2014 o governo era do mesmo lado de 2026).
    Nem um nem outro: INCONCLUSIVO (o registro não nomeia o caso do meio).
    Se algum dos anos 2002, 2006 e 2010 não rodar, o máximo é sobre os que rodaram e o veredito diz qual faltou.
D5. A pergunta que decide (quem governa ou PT), sem critério numérico no registro. Fixado aqui:
    p(ano) = -A_iguais (vantagem do PT: o PT perde menos dos próprios). g(ano) = vantagem do candidato do governo
    = -A_iguais se o governo é o PT, +A_iguais se o governo é a direita. Anos que separam: 2002 e 2022 (g = -p).
    Limiar 0,015 (o do F21; 1,5 vez o ruído de 0,01).
    "ACOMPANHA QUEM GOVERNA": g >= +0,015 em 2002 e em 2022 e em pelo menos 3 dos 4 anos de governo do PT (2006, 2010,
    2014, 2026).
    "ACOMPANHA O PT": p >= +0,015 em 2002 e em 2022 e em pelo menos 3 dos 4 anos de governo do PT.
    Qualquer outra coisa: "NEM UM NEM OUTRO", descrito ano a ano. Como 2022 já é conhecido (p negativo), "acompanha o PT"
    não pode mais sair; o que está aberto é 2002 (governo de um lado, PT do outro) e o tamanho em 2006 e 2010.
    Placebo da explicação "quem governa": 2018, sem governo candidato, deveria ter |A_iguais| abaixo de 0,015.
    Descritivo ao lado, sem veredito: tabela do sinal de A por ano contra quatro atributos (lado do governo, lado do PT,
    lado de quem venceu o 2º turno, lado de quem liderou o 1º turno), com a contagem de anos em que cada um acerta o sinal.
D6. Extração de 2002, 2006 e 2010. Fonte: cdn.tse.jus.br/estatistica/sead/odsele/votacao_secao/votacao_secao_AAAA_BR.zip
    (só presidente, dois turnos; tamanhos pelo pedido de cabeçalho: 19.858.557, 22.094.673 e 23.737.900 bytes). Um ano por
    vez, em pasta nova, com curl sem cabeçalho extra; conferido o tamanho contra o content-length e o CRC do zip; lido em
    fluxo como dado; zip apagado depois da extração; SHA-256 guardado no JSON.
    Chave UF|CD_MUNICIPIO|NR_ZONA|NR_SECAO (a mesma das bases de dados/). Por seção e turno: L = 13; R = 45; B = 95;
    N = 96 mais 97 (voto anulado e apurado em separado); O = demais votáveis; comp = soma de todos os votos de presidente
    da seção no turno (o arquivo não traz aptos nem comparecimento; A não usa aptos); loc = NR_LOCAL_VOTACAO das linhas
    do 2º turno (o mais frequente, se houver mais de um). Linhas repetidas somam.
    Conferência contra o total oficial do TSE, escrito aqui de memória antes de somar:
      2002 1º turno Lula 39.455.233, Serra 19.705.445; 2º turno Lula 52.793.364, Serra 33.370.739
      2006 1º turno Lula 46.662.365, Alckmin 39.968.369; 2º turno Lula 58.295.042, Alckmin 37.543.178
      2010 1º turno Dilma 47.651.434, Serra 33.132.283; 2º turno Dilma 55.752.529, Serra 43.711.388
    Um ano "liga" (roda) se: arquivo íntegro; os dois turnos presentes; cada finalista em cada turno a até 0,05% do
    oficial; seções com os dois turnos >= 98% das seções do 2º turno; local válido (inteiro positivo) em >= 95% delas;
    pelo menos 3 das 4 faixas válidas. Se falhar, o ano fica como NÃO RODADO, sem substituto.
D7. Calibração por efeito plantado, nos dados de 2026 (universo próprio), irregularidade = troca uniforme de votos de
    Flávio para Lula no 2º turno, em toda seção: R2' = R2 - s.R2, L2' = L2 + s.R2 (fração exata, sem arredondar; brancos,
    nulos e comparecimento intactos). Tamanho do registro: s = 3,57% (a troca que vira o resultado). Grade ao lado:
    0,5; 1; 1,5; 2; 2,5; 3; 3,57; 4; 5; 6 e 8%. Conferência com sorteio binomial por seção (semente 2704) em 3,57%.
    O teste "enxerga" o plantado se o critério D4, aplicado a 2026 com o plantado e aos anos de comparação como estão,
    der INDÍCIO pela letra. Se não der em 3,57%, o veredito pela letra é SEM PODER, e relato a menor fração da grade
    que seria enxergada em cada leitura (letra; só a primeira condição de 0,015; ruído medido).
    Limite dito antes: a base onde planto já é o resultado oficial. Se o oficial já contiver uma troca desse tamanho, o que
    o critério julga é o próprio oficial; por isso relato também o "desplantado" (R2'' = R2/(1-s), L2'' = L2 - s.R2/(1-s),
    s = 3,5704%, que zera a margem) e o A que essa eleição "limpa" teria. Descritivo: o deslocamento de d por faixa causado
    pelo plantado, ao lado da forma observada da curva.
D8. Espelho. (i) O mesmo critério de INDÍCIO com cada ano de governo candidato como alvo e os demais como comparação
    (algum outro ano seria apontado, em especial 2022 a favor de Bolsonaro e 2002?). (ii) 2018 como placebo (D5).
    (iii) O plantado no sentido contrário (s.L2 de Lula para Flávio, s = 3,57%): o teste deve responder com o sinal oposto
    e tamanho parecido.
D9. Tradução em votos. Inclinação k = variação de A_iguais por ponto de s, medida no plantado. Para uma diferença x de A:
    s equivalente = x / k; votos trocados = s x 59.826.041; efeito na margem = 2 x votos, contra a margem de 4.430.191
    (2.215.096 votos trocados). Relatado para: o A bruto de 2026 inteiro; o excesso E; 2026 menos 2014; 2026 menos o
    espelho de 2022; e o ruído de 0,01.
D10. Exploratório: tudo o que for feito depois de ver os resultados é marcado como exploratório no JSON e no texto.
D11. Arquivos de trabalho em /home/user/trabalho-eleicao/adendo27/R27_A4/ (bases extraídas de 2002, 2006 e 2010 em
    json.gz, no formato de dados/, e parciais por ano e universo). Nada é alterado no repositório além dos três arquivos
    novos deste teste.

Uso:
  python3 -I analisar_R27_A4.py extrair <votacao_secao_AAAA_BR.zip> <ano> <pasta_trabalho>
  python3 -I analisar_R27_A4.py rodar <pasta dados/> <pasta resultados/> <pasta_trabalho> <saida.json> <saida.txt>
"""
import collections, csv, gzip, hashlib, io, json, os, sys, zipfile
import numpy as np

FAIXAS = [(0, .35), (.35, .50), (.50, .65), (.65, 1.01)]
NOME_FAIXA = ['0.00-0.35', '0.35-0.50', '0.50-0.65', '0.65-1.00']
ANOS = [2002, 2006, 2010, 2014, 2018, 2022, 2026]
INFO = {
    2002: dict(pt='Lula', direita='Serra (45)', governo='R', venceu='L', lider1t='L'),
    2006: dict(pt='Lula', direita='Alckmin (45)', governo='L', venceu='L', lider1t='L'),
    2010: dict(pt='Dilma', direita='Serra (45)', governo='L', venceu='L', lider1t='L'),
    2014: dict(pt='Dilma', direita='Aécio (45)', governo='L', venceu='L', lider1t='L'),
    2018: dict(pt='Haddad', direita='Bolsonaro (17)', governo=None, venceu='R', lider1t='R'),
    2022: dict(pt='Lula', direita='Bolsonaro (22)', governo='R', venceu='L', lider1t='L'),
    2026: dict(pt='Lula', direita='Flávio (22)', governo='L', venceu='L', lider1t='R'),
}
# Totais oficiais escritos de memória no docstring (D6), antes de somar.
OFICIAL = {
    2002: {'1': {'L': 39455233, 'R': 19705445}, '2': {'L': 52793364, 'R': 33370739}},
    2006: {'1': {'L': 46662365, 'R': 39968369}, '2': {'L': 58295042, 'R': 37543178}},
    2010: {'1': {'L': 47651434, 'R': 33132283}, '2': {'L': 55752529, 'R': 43711388}},
}
VOTOS_FLAVIO_2T, VOTOS_LULA_2T, MARGEM = 59826041, 64256232, 4430191
S_REGISTRO = 0.0357
S_DESPLANTA = (MARGEM / 2) / (VOTOS_FLAVIO_2T + MARGEM / 2)   # 3,5704%: fração dos votos "verdadeiros" de Flávio
GRADE = [0.005, 0.01, 0.015, 0.02, 0.025, 0.03, 0.0357, 0.04, 0.05, 0.06, 0.08]
LIM_INDICIO, RUIDO_REGISTRO, LIM_SEM = 0.015, 0.01, 0.010
LIM_GOV = 0.015
SEMENTE = 2704


def sha256(p):
    h = hashlib.sha256()
    with open(p, 'rb') as f:
        for b in iter(lambda: f.read(1 << 20), b''):
            h.update(b)
    return h.hexdigest()


def gravar(obj, caminho):
    tmp = caminho + '.tmp'
    with open(tmp, 'w', encoding='utf-8') as f:
        json.dump(obj, f, ensure_ascii=False, indent=1)
    os.replace(tmp, caminho)


# ---------------------------------------------------------------- extração de 2002, 2006 e 2010 (D6)
def extrair(zp, ano, pasta):
    meta = {'ano': ano, 'zip': os.path.basename(zp), 'bytes': os.path.getsize(zp), 'sha256': sha256(zp)}
    z = zipfile.ZipFile(zp)
    meta['crc_ok'] = z.testzip() is None
    csvs = [i for i in z.infolist() if i.filename.lower().endswith('.csv')]
    assert len(csvs) == 1, [i.filename for i in z.infolist()]
    meta['csv'] = csvs[0].filename; meta['csv_bytes'] = csvs[0].file_size
    sec = {}
    tot = collections.Counter(); nomes = {}; fora = collections.Counter(); linhas = 0
    locruim = 0
    with z.open(csvs[0]) as f:
        r = csv.reader(io.TextIOWrapper(f, encoding='latin-1', newline=''), delimiter=';')
        h = next(r); ix = {k: i for i, k in enumerate(h)}
        meta['colunas'] = h
        iA, iC, iT, iTE = ix['ANO_ELEICAO'], ix['CD_CARGO'], ix['NR_TURNO'], ix['CD_TIPO_ELEICAO']
        iU, iM, iZ, iS = ix['SG_UF'], ix['CD_MUNICIPIO'], ix['NR_ZONA'], ix['NR_SECAO']
        iV, iN, iQ, iL = ix['NR_VOTAVEL'], ix['NM_VOTAVEL'], ix['QT_VOTOS'], ix['NR_LOCAL_VOTACAO']
        for row in r:
            linhas += 1
            t = row[iT]
            if int(row[iA]) != ano or row[iC] != '1' or t not in ('1', '2') or row[iTE] != '2':
                fora[(row[iA], row[iC], t, row[iTE])] += 1
                continue
            k = f'{row[iU]}|{int(row[iM])}|{int(row[iZ])}|{int(row[iS])}'
            v = row[iV]; q = int(row[iQ])
            tot[(t, v)] += q; nomes[v] = row[iN]
            s = sec.get(k)
            if s is None:
                s = sec[k] = {}
            x = s.get(t)
            if x is None:
                x = s[t] = [0, 0, 0, 0, 0, 0, collections.Counter()]   # L R O B N comp locais
            j = 0 if v == '13' else 1 if v == '45' else 3 if v == '95' else 4 if v in ('96', '97') else 2
            x[j] += q; x[5] += q
            x[6][row[iL]] += 1
    base = {}
    n1 = n2 = n12 = locdif = locmais = 0
    for k, s in sec.items():
        o = {}
        for t, x in s.items():
            loc = x[6].most_common(1)[0][0]
            if len(x[6]) > 1:
                locmais += 1
            try:
                li = int(loc)
            except ValueError:
                li = -1
            o[t] = {'loc': li, 'comp': x[5], 'L': x[0], 'R': x[1], 'O': x[2], 'B': x[3], 'N': x[4]}
        n1 += '1' in o; n2 += '2' in o
        if '1' in o and '2' in o:
            n12 += 1
            locdif += o['1']['loc'] != o['2']['loc']
            locruim += o['2']['loc'] <= 0
        base[k] = o
    meta.update(linhas=linhas, linhas_fora=[[list(k), v] for k, v in fora.items()],
                secoes_1t=n1, secoes_2t=n2, secoes_dois_turnos=n12,
                frac_dois_turnos_sobre_2t=n12 / n2 if n2 else None,
                secoes_com_local_invalido_2t=locruim, secoes_com_mais_de_um_local_no_turno=locmais,
                secoes_com_local_diferente_entre_turnos=locdif,
                votaveis={t: {v: [nomes[v], tot[(t, v)]] for (tt, v) in sorted(tot) if tt == t} for t in ('1', '2')})
    conf = {}
    okc = True
    for t in ('1', '2'):
        conf[t] = {}
        for c, num in (('L', '13'), ('R', '45')):
            b = tot[(t, num)]; of = OFICIAL[ano][t][c]
            conf[t][c] = {'base': b, 'oficial_de_memoria': of, 'dif': b - of, 'dif_rel': (b - of) / of}
            okc &= abs(b - of) / of <= 0.0005
        conf[t]['comparecimento_soma_dos_votos'] = sum(q for (tt, v), q in tot.items() if tt == t)
        conf[t]['validos'] = sum(q for (tt, v), q in tot.items() if tt == t and v not in ('95', '96', '97'))
    meta['conferencia_oficial'] = conf
    meta['liga_ate_aqui'] = bool(meta['crc_ok'] and n1 > 0 and n2 > 0 and okc and n12 / n2 >= 0.98
                                 and (n12 - locruim) / n12 >= 0.95)
    with gzip.open(os.path.join(pasta, f'secoes{ano}.json.gz'), 'wt') as f:
        json.dump(base, f, separators=(',', ':'))
    gravar(meta, os.path.join(pasta, f'extracao_{ano}_meta.json'))
    print(json.dumps({k: v for k, v in meta.items() if k != 'colunas'}, ensure_ascii=False, indent=1))


# ---------------------------------------------------------------- leitura das bases em matrizes
class Base:
    pass


def ler_base(caminho):
    with gzip.open(caminho, 'rt') as f:
        d = json.load(f)
    ks = [k for k, v in d.items() if '1' in v and '2' in v]
    n = len(ks)
    arr = np.zeros((n, 10)); loc = np.zeros(n, np.int64); ids = {}
    c28 = 0
    for i, k in enumerate(ks):
        v = d[k]; a = v['1']; b = v['2']
        uf, mun, zona, _ = k.split('|')
        loc[i] = ids.setdefault(f"{uf}|{mun}|{zona}|{b['loc']}", len(ids))
        c = a.get('c28', 0); c28 += c > 0
        arr[i] = (a['L'], a['R'], a['O'], a['B'] + a['N'], a['comp'], c, b['L'], b['R'], b['B'] + b['N'], b['comp'])
    B = Base(); B.chaves = ks; B.n = n; B.arr = arr; B.loc = loc; B.nloc = len(ids); B.c28 = int(c28)
    B.total_na_base = len(d)
    return B


def mascara(B, conjunto):
    return np.fromiter((k in conjunto for k in B.chaves), bool, B.n)


# ---------------------------------------------------------------- estatística A (código próprio, D1 e D3)
def estat(B, m=None, L2=None, R2=None):
    idx = np.arange(B.n) if m is None else np.flatnonzero(m)
    _, g = np.unique(B.loc[idx], return_inverse=True); nl = int(g.max()) + 1
    L1, R1, O1, BN1, C1, c28 = (B.arr[idx, j] for j in range(6))
    L2v = (B.arr[:, 6] if L2 is None else L2)[idx]; R2v = (B.arr[:, 7] if R2 is None else R2)[idx]
    BN2, C2 = B.arr[idx, 8], B.arr[idx, 9]
    den = np.bincount(g, L1 + R1 + O1 - c28, nl); ok = den > 0
    den1 = np.where(ok, den, 1.0)
    fR = np.bincount(g, R1, nl) / den1; fL = np.bincount(g, L1, nl) / den1
    comum = [O1, BN1 - BN2, C2 - C1]
    dados = {'L': (np.column_stack(comum + [R1, L1]), L2v - L1, fR, L1),
             'R': (np.column_stack(comum + [L1, R1]), R2v - R1, fL, R1)}
    faixas = []; val = []
    for i, (lo, hi) in enumerate(FAIXAS):
        item = {'faixa': NOME_FAIXA[i]}; par = {}
        for c in 'LR':
            X, y, fadv, own = dados[c]
            sel = (ok & (fadv >= lo) & (fadv < hi))[g]
            cnt = np.bincount(g[sel], minlength=nl)
            par[c] = (sel, cnt)
            item['secoes_' + c] = int(sel.sum()); item['locais_' + c] = int((cnt >= 2).sum())
        if min(item['locais_L'], item['locais_R']) < 30:
            item['fora'] = 'menos de 30 locais'; faixas.append(item); continue
        reg = {}
        for c in 'LR':
            X, y, fadv, own = dados[c]; sel, cnt = par[c]
            keep = sel & (cnt[g] >= 2)
            gk = g[keep]; Xk = X[keep]; yk = y[keep]
            nk = np.bincount(gk, minlength=nl).astype(float); nk1 = np.where(nk > 0, nk, 1.0)
            Xd = np.empty_like(Xk)
            for j in range(5):
                Xd[:, j] = Xk[:, j] - (np.bincount(gk, Xk[:, j], nl) / nk1)[gk]
            yd = yk - (np.bincount(gk, yk, nl) / nk1)[gk]
            XtX = Xd.T @ Xd; b = np.linalg.solve(XtX, Xd.T @ yd); e = yd - Xd @ b
            S = np.column_stack([np.bincount(gk, Xd[:, j] * e, nl) for j in range(5)])
            reg[c] = dict(b=b, inv=np.linalg.inv(XtX), S=S, N=int(keep.sum()), locs=nk > 0, votos=float(own[keep].sum()))
        N = reg['L']['N'] + reg['R']['N']; G = int((reg['L']['locs'] | reg['R']['locs']).sum())
        corr = G / (G - 1) * (N - 1) / (N - 10)
        infl = {c: (reg[c]['S'] @ reg[c]['inv'])[:, 4] * np.sqrt(corr) for c in 'LR'}
        for c in 'LR':
            item['proprio_' + c] = [float(reg[c]['b'][4]), float(np.sqrt((infl[c] ** 2).sum()))]
            item['adversario_' + c] = float(reg[c]['b'][3])
            item['coef_' + c] = [float(x) for x in reg[c]['b']]
            item['votos1t_' + c] = reg[c]['votos']; item['n_' + c] = reg[c]['N']
        ifd = infl['R'] - infl['L']
        item['d'] = [float(reg['R']['b'][4] - reg['L']['b'][4]), float(np.sqrt((ifd ** 2).sum()))]
        item['grupos'] = G
        faixas.append(item); val.append((i, item, infl))
    out = {'secoes': int(len(idx)), 'locais': nl, 'faixas': faixas, 'faixas_validas': [NOME_FAIXA[i] for i, _, _ in val]}
    if val:
        d = np.array([it['d'][0] for _, it, _ in val]); se = np.array([it['d'][1] for _, it, _ in val])
        IFd = np.column_stack([inf['R'] - inf['L'] for _, _, inf in val])

        def pesa(w):
            w = np.asarray(w, float); w = w / w.sum()
            return [float((w * d).sum()), float(np.sqrt((w ** 2 * se ** 2).sum())), float(np.sqrt(((IFd @ w) ** 2).sum()))]
        A = {'iguais': pesa(np.ones(len(d))), 'inv_var': pesa(1 / se ** 2),
             'votos': pesa([it['votos1t_L'] + it['votos1t_R'] for _, it, _ in val]),
             'secoes_direita': pesa([it['secoes_R'] for _, it, _ in val])}
        wL = np.array([it['votos1t_L'] for _, it, _ in val]); wL = wL / wL.sum()
        wR = np.array([it['votos1t_R'] for _, it, _ in val]); wR = wR / wR.sum()
        bL = np.array([it['proprio_L'][0] for _, it, _ in val]); bR = np.array([it['proprio_R'][0] for _, it, _ in val])
        IFc = np.column_stack([inf['R'] for _, _, inf in val]) @ wR - np.column_stack([inf['L'] for _, _, inf in val]) @ wL
        A['cada_um_seus_votos'] = [float((wR * bR).sum() - (wL * bL).sum()), None, float(np.sqrt((IFc ** 2).sum()))]
        A['media_proprio_L_pelos_votos'] = float((wL * bL).sum()); A['media_proprio_R_pelos_votos'] = float((wR * bR).sum())
        out['A'] = A
        out['legenda_A'] = '[valor, ep com faixas independentes, ep agrupado por local entre as faixas]'
    else:
        out['A'] = None
    return out


def a_nas_faixas(res, nomes):
    """Média simples de d só nas faixas pedidas (erro-padrão com faixas independentes)."""
    ds = [f['d'] for f in res['faixas'] if 'd' in f and f['faixa'] in nomes]
    if len(ds) != len(nomes):
        return None
    return [float(np.mean([x for x, _ in ds])), float(np.sqrt(sum(s * s for _, s in ds)) / len(ds))]


# ---------------------------------------------------------------- critério (D4), pergunta que decide (D5), espelho (D8)
def anos_de_governo(Aig, alvo):
    return [y for y in ANOS if INFO[y]['governo'] and y != alvo and y in Aig]


def criterio(Aig, alvo=2026, ruido=RUIDO_REGISTRO):
    comp = anos_de_governo(Aig, alvo)
    if alvo not in Aig or not comp:
        return {'veredito': 'NÃO RODADO'}
    ymax = max(comp, key=lambda y: abs(Aig[y])); mx = abs(Aig[ymax])
    E = abs(Aig[alvo]) - mx
    o = {'alvo': alvo, 'A_alvo': Aig[alvo], 'anos_de_comparacao': comp, 'maior_abs_A': mx, 'ano_do_maior': ymax,
         'E': E, 'ruido': ruido, 'cond_0015': bool(E >= LIM_INDICIO), 'cond_3_ruidos': bool(E > 3 * ruido)}
    o['indicio'] = o['cond_0015'] and o['cond_3_ruidos']
    if alvo == 2026 and 2022 in Aig and 2014 in Aig:
        o['dist_espelho_2022'] = abs(Aig[2026] + Aig[2022]); o['dist_2014'] = abs(Aig[2026] - Aig[2014])
        o['sem_sinal'] = bool(o['dist_espelho_2022'] <= LIM_SEM and o['dist_2014'] <= LIM_SEM)
        o['veredito'] = 'SINAL' if o['indicio'] else 'SEM SINAL' if o['sem_sinal'] else 'INCONCLUSIVO'
    return o


def quem_governa_ou_pt(Aig):
    lin = []
    for y in ANOS:
        if y not in Aig:
            lin.append({'ano': y, 'rodado': False}); continue
        A = Aig[y]; gov = INFO[y]['governo']
        g = None if gov is None else (-A if gov == 'L' else A)
        lin.append({'ano': y, 'rodado': True, 'A_iguais': A, 'vantagem_PT': -A, 'governo': gov, 'vantagem_governo': g,
                    'lado_que_perde_menos': 'L' if A < 0 else 'R', 'venceu': INFO[y]['venceu'], 'lider1t': INFO[y]['lider1t']})
    r = {y['ano']: y for y in lin if y['rodado']}
    sep = [y for y in (2002, 2022) if y in r]; ptg = [y for y in (2006, 2010, 2014, 2026) if y in r]
    o = {'anos': lin, 'anos_que_separam_rodados': sep, 'anos_governo_PT_rodados': ptg}
    if len(sep) == 2:
        ng = sum(r[y]['vantagem_governo'] >= LIM_GOV for y in ptg)
        gov_ok = all(r[y]['vantagem_governo'] >= LIM_GOV for y in sep) and ng >= 3
        pt_ok = all(r[y]['vantagem_PT'] >= LIM_GOV for y in sep) and sum(r[y]['vantagem_PT'] >= LIM_GOV for y in ptg) >= 3
        o['anos_governo_PT_com_vantagem_do_governo'] = int(ng)
        o['classificacao'] = 'ACOMPANHA QUEM GOVERNA' if gov_ok else 'ACOMPANHA O PT' if pt_ok else 'NEM UM NEM OUTRO'
    else:
        o['classificacao'] = 'NÃO DECIDE (falta 2002 ou 2022)'
    if 2018 in r:
        o['placebo_2018'] = {'A_iguais': r[2018]['A_iguais'], 'abaixo_de_0015': bool(abs(r[2018]['A_iguais']) < LIM_GOV)}
    acerto = {}
    for nome, chave in (('lado do governo', 'governo'), ('lado do PT', None), ('quem venceu o 2º turno', 'venceu'),
                        ('quem liderou o 1º turno', 'lider1t')):
        ac = []; tot = []
        for y in lin:
            if not y['rodado']:
                continue
            lado = 'L' if chave is None else y[chave]
            if lado is None:
                continue
            tot.append(y['ano'])
            if y['lado_que_perde_menos'] == lado:
                ac.append(y['ano'])
        acerto[nome] = {'anos_com_o_atributo': tot, 'anos_em_que_o_lado_perde_menos': ac, 'acertos': len(ac), 'de': len(tot)}
    o['sinal_de_A_contra_atributos'] = acerto
    return o


# ---------------------------------------------------------------- execução
def rodar(p_dados, p_res, p_trab, saida_json, saida_txt):
    parc = os.path.join(p_trab, 'parcial'); os.makedirs(parc, exist_ok=True)
    out = {'teste': 'R27_A4, curva por força com a série longa (fragilidade T35, Adendo 27)',
           'registro': 'PRE-REGISTRO-2026-10-26.md, Adendo 27, commit 2748895 (10/11/2026 00:16:42 UTC); '
                       'registro/adendo27/equipe_vermelha_relatorio.json, fragilidade T35',
           'docstring_antes_de_rodar': {'arquivo': os.path.join(p_trab, 'docstring_antes_de_rodar.txt'),
                                        'sha256': sha256(os.path.join(p_trab, 'docstring_antes_de_rodar.txt'))}}

    def parcial(nome, fn):
        p = os.path.join(parc, nome + '.json')
        if os.path.exists(p):
            return json.load(open(p, encoding='utf-8'))
        r = fn(); gravar(r, p); return r

    # bases
    caminho = {y: os.path.join(p_dados, f'secoes{y}.json.gz') for y in (2014, 2018, 2022, 2026)}
    out['extracao'] = {}; nao_rodados = {}
    for y in (2002, 2006, 2010):
        pm = os.path.join(p_trab, f'extracao_{y}_meta.json'); pb = os.path.join(p_trab, f'secoes{y}.json.gz')
        if not (os.path.exists(pm) and os.path.exists(pb)):
            nao_rodados[y] = 'arquivo não baixado ou não extraído'; continue
        meta = json.load(open(pm, encoding='utf-8')); meta.pop('colunas', None)
        out['extracao'][y] = meta
        if not meta['liga_ate_aqui']:
            nao_rodados[y] = 'não cumpre a regra de ligação D6'; continue
        caminho[y] = pb
    Bs = {}
    for y in sorted(caminho):
        Bs[y] = ler_base(caminho[y])
        print('base', y, Bs[y].n, 'seções com dois turnos,', Bs[y].nloc, 'locais', flush=True)
    out['secoes_com_dois_turnos'] = {y: Bs[y].n for y in Bs}
    out['c28_presente'] = {y: Bs[y].c28 for y in Bs}
    conj = {y: set(Bs[y].chaves) for y in Bs}

    # D1: conferência contra o publicado, na ponderação original
    t35 = json.load(open(os.path.join(p_res, 'T35_curva_forca_bweb.json'), encoding='utf-8'))
    f21 = json.load(open(os.path.join(p_res, 'F21_serie_anos.json'), encoding='utf-8'))
    u_t35 = conj[2026]
    u_f21 = conj[2014] & conj[2018] & conj[2022] & conj[2026]
    res = {}   # res[universo][ano]

    def calc(nome_u, y, conjunto=None):
        r = parcial(f'A_{y}_{nome_u}', lambda: estat(Bs[y], None if conjunto is None else mascara(Bs[y], conjunto)))
        res.setdefault(nome_u, {})[y] = r
        gravar({'res': res_json(res)}, os.path.join(p_trab, 'andamento.json'))
        return r

    for y in (2018, 2022, 2026):
        calc('U_T35', y, u_t35)
    for y in (2014, 2018, 2022, 2026):
        calc('U_F21', y, u_f21)
    calc('U_T35', 2014, u_t35)   # o r2 do F21: 2014 nas chaves de 2026

    def compara(meu, pub):
        dif = []; cont = meu['secoes'] == pub['secoes']
        for a, b in zip(meu['faixas'], pub['faixas']):
            for k in ('secoes_L', 'secoes_R', 'locais_L', 'locais_R'):
                cont &= a[k] == b[k]
            for k in ('proprio_L', 'proprio_R', 'd'):
                if (k in a) != (k in b):
                    cont = False; continue
                if k in a:
                    dif += [abs(a[k][0] - b[k][0]), abs(a[k][1] - b[k][1])]
        dif += [abs(meu['A']['inv_var'][0] - pub['A'][0]), abs(meu['A']['inv_var'][1] - pub['A'][1])]
        return {'contagens_iguais': bool(cont), 'maior_diferenca_absoluta': float(max(dif)),
                'A_meu': meu['A']['inv_var'][:2], 'A_publicado': pub['A'], 'reproduz': bool(cont and max(dif) <= 5e-7)}
    conf = {'T35_bweb': {str(y): compara(res['U_T35'][y], t35[str(y)]) for y in (2018, 2022, 2026)},
            'F21_serie_principal': {str(y): compara(res['U_F21'][y], f21['A_serie_principal'][str(y)]) for y in (2014, 2018, 2022, 2026)},
            'F21_r2_2014': compara(res['U_T35'][2014], f21['A_r2_universo_T35']['2014'])}
    conf['tudo_reproduz'] = bool(all(v['reproduz'] for v in conf['T35_bweb'].values())
                                 and all(v['reproduz'] for v in conf['F21_serie_principal'].values())
                                 and conf['F21_r2_2014']['reproduz'])
    out['conferencia_D1'] = conf
    print('conferência D1:', json.dumps(conf, ensure_ascii=False), flush=True)
    if not conf['tudo_reproduz']:
        out['veredito'] = 'PARADO: o código próprio não reproduz o publicado (D1)'
        gravar(out, saida_json); return

    # série principal: universo próprio de cada ano (D2)
    for y in sorted(Bs):
        r = calc('U_proprio', y)
        if y in (2002, 2006, 2010) and len(r['faixas_validas']) < 3:
            nao_rodados[y] = 'menos de 3 faixas válidas (D6)'
    out['nao_rodados'] = {str(y): m for y, m in nao_rodados.items()}
    rodados = [y for y in sorted(Bs) if y not in nao_rodados]
    velhos = [y for y in (2002, 2006, 2010) if y in rodados]
    # universos ao lado
    if len(velhos) >= 2:
        u_0210 = set.intersection(*(conj[y] for y in velhos))
        for y in velhos:
            calc('U_0210', y, u_0210)
        out['U_0210'] = {'anos': velhos, 'secoes': len(u_0210)}
    u_7 = set.intersection(*(conj[y] for y in rodados))
    out['U_7'] = {'anos': rodados, 'secoes': len(u_7), 'frac_das_secoes_2026': len(u_7) / Bs[2026].n}
    r7 = {y: parcial(f'A_{y}_U_7', lambda y=y: estat(Bs[y], mascara(Bs[y], u_7))) for y in rodados}
    out['U_7']['entra'] = bool(all(len(r['faixas_validas']) >= 3 for r in r7.values()))
    res['U_7'] = r7
    out['intersecoes'] = {f'{a}-{b}': len(conj[a] & conj[b]) for i, a in enumerate(rodados) for b in rodados[i + 1:]}
    out['resultados_por_universo'] = res_json(res)

    def aig(u, chave='iguais'):
        return {y: res[u][y]['A'][chave][0] for y in res.get(u, {}) if y not in nao_rodados and res[u][y]['A']}
    A_princ = aig('U_proprio')
    # ruído entre conjuntos de seções, medido aqui (D2)
    ruido = {}
    for y in rodados:
        vals = {u: res[u][y]['A']['iguais'][0] for u in res if y in res[u] and res[u][y]['A'] and (u != 'U_7' or out['U_7']['entra'])}
        ruido[y] = {'por_universo': vals, 'amplitude': float(max(vals.values()) - min(vals.values())) if len(vals) > 1 else None}
    amp = [v['amplitude'] for v in ruido.values() if v['amplitude'] is not None]
    ruido_medido = max(amp) if amp else None
    out['ruido_entre_conjuntos'] = {'por_ano': ruido, 'maior_amplitude': ruido_medido, 'do_registro': RUIDO_REGISTRO}

    # critério D4 no universo principal e ao lado
    def aplica(Aig):
        c = criterio(Aig)
        if ruido_medido is not None and 'E' in c:
            c['leitura_ruido_medido'] = {'ruido': ruido_medido, 'indicio': bool(c['E'] >= LIM_INDICIO and c['E'] > 3 * ruido_medido)}
            c['leitura_so_primeira_condicao'] = {'indicio': bool(c['E'] >= LIM_INDICIO)}
        return c
    out['criterio_principal'] = aplica(A_princ)
    ep = {y: res['U_proprio'][y]['A']['iguais'][2] for y in rodados}   # agrupado por local entre as faixas
    out['A_iguais_principal'] = {str(y): {'A': A_princ[y], 'ep_faixas_independentes': res['U_proprio'][y]['A']['iguais'][1],
                                          'ep_agrupado_entre_faixas': ep[y], 'secoes': res['U_proprio'][y]['secoes']} for y in rodados}
    if 'dist_2014' in out['criterio_principal']:
        out['criterio_principal']['ep_dist_espelho_2022'] = float(np.hypot(ep[2026], ep[2022]))
        out['criterio_principal']['ep_dist_2014'] = float(np.hypot(ep[2026], ep[2014]))
    lado = {}
    for chave in ('inv_var', 'votos', 'secoes_direita', 'cada_um_seus_votos'):
        lado['U_proprio, ponderação ' + chave] = aplica(aig('U_proprio', chave))
    # universos ao lado: cada ano no universo indicado; os anos que o universo não tem entram pelo universo próprio
    mist = dict(A_princ); mist.update(aig('U_F21')); lado['2014 a 2026 em U_F21, 2002 a 2010 no universo próprio'] = aplica(mist)
    mist = dict(A_princ); mist.update(aig('U_T35')); lado['2014 a 2026 em U_T35 (chaves de 2026), 2002 a 2010 no universo próprio'] = aplica(mist)
    if 'U_0210' in res:
        mist = dict(A_princ); mist.update(aig('U_0210')); lado['2002 a 2010 em U_0210, demais no universo próprio'] = aplica(mist)
        mist = dict(A_princ); mist.update(aig('U_F21')); mist.update(aig('U_0210')); lado['2002 a 2010 em U_0210 e 2014 a 2026 em U_F21'] = aplica(mist)
    if out['U_7']['entra']:
        lado['U_7 (seções comuns aos sete anos)'] = aplica(aig('U_7'))
    comuns = [n for n in NOME_FAIXA if all(n in res['U_proprio'][y]['faixas_validas'] for y in rodados)]
    fc = {y: a_nas_faixas(res['U_proprio'][y], comuns) for y in rodados}
    out['faixas_comuns'] = {'faixas': comuns, 'A_iguais': {str(y): v for y, v in fc.items()}}
    if len(comuns) < 4:
        lado['U_proprio, só nas faixas válidas em todos os anos'] = aplica({y: v[0] for y, v in fc.items()})
    out['criterio_ao_lado'] = lado
    out['quem_governa_ou_pt'] = quem_governa_ou_pt(A_princ)
    out['quem_governa_ou_pt_ao_lado'] = {
        'U_F21 para 2014 a 2026': quem_governa_ou_pt({**A_princ, **aig('U_F21')}),
        'inverso da variância': quem_governa_ou_pt(aig('U_proprio', 'inv_var')),
        'peso por votos': quem_governa_ou_pt(aig('U_proprio', 'votos'))}
    # descritivo: posição de 2026 entre os anos de governo candidato
    gv = [abs(A_princ[y]) for y in anos_de_governo(A_princ, 2026)]
    out['descritivo_anos_de_governo'] = {'abs_A': {str(y): abs(A_princ[y]) for y in anos_de_governo(A_princ, 2026)},
                                         'media': float(np.mean(gv)), 'desvio_padrao_amostral': float(np.std(gv, ddof=1)) if len(gv) > 1 else None,
                                         'abs_A_2026': abs(A_princ[2026])}
    # espelho (i): cada ano de governo candidato como alvo
    out['espelho_cada_ano_como_alvo'] = {str(y): criterio(A_princ, alvo=y) for y in rodados if INFO[y]['governo']}
    gravar(out, saida_json)

    # D7: calibração por efeito plantado em 2026 (universo próprio)
    B = Bs[2026]; L2 = B.arr[:, 6]; R2 = B.arr[:, 7]
    base26 = res['U_proprio'][2026]

    def planta(nome, L2p, R2p):
        r = parcial('plantado_' + nome, lambda: estat(B, None, L2p, R2p))
        Aig = dict(A_princ); Aig[2026] = r['A']['iguais'][0]
        return {'A': r['A'], 'd_por_faixa': [f['d'][0] for f in r['faixas'] if 'd' in f],
                'proprio_L': [f['proprio_L'][0] for f in r['faixas'] if 'd' in f],
                'proprio_R': [f['proprio_R'][0] for f in r['faixas'] if 'd' in f],
                'deslocamento_de_d_por_faixa': [f['d'][0] - g['d'][0] for f, g in zip(r['faixas'], base26['faixas']) if 'd' in f],
                'deslocamento_A_iguais': r['A']['iguais'][0] - base26['A']['iguais'][0],
                'criterio': aplica(Aig)}
    cal = {'base': 'seções de 2026, universo próprio, votos oficiais', 'A_iguais_oficial': base26['A']['iguais'], 'grade': {}}
    for s in GRADE:
        t = s * R2
        cal['grade'][f'{s:.4f}'] = dict(planta(f'F_para_L_{s:.4f}', L2 + t, R2 - t), s=s, votos_movidos=float(t.sum()))
        gravar(cal, os.path.join(p_trab, 'calibracao_andamento.json'))
    reg = cal['grade'][f'{S_REGISTRO:.4f}']
    cal['inclinacao_k'] = reg['deslocamento_A_iguais'] / S_REGISTRO
    ss = np.array(GRADE); da = np.array([cal['grade'][f'{s:.4f}']['deslocamento_A_iguais'] for s in GRADE])
    cal['inclinacao_pela_grade_sem_intercepto'] = float((ss * da).sum() / (ss * ss).sum())
    rng = np.random.default_rng(SEMENTE); tb = rng.binomial(R2.astype(np.int64), S_REGISTRO).astype(float)
    cal['binomial_3_57'] = dict(planta('F_para_L_binomial', L2 + tb, R2 - tb), semente=SEMENTE, votos_movidos=float(tb.sum()))
    te = S_REGISTRO * L2
    cal['espelho_L_para_F_3_57'] = dict(planta('L_para_F_0.0357', L2 - te, R2 + te), votos_movidos=float(te.sum()))
    td = S_DESPLANTA * R2 / (1 - S_DESPLANTA)
    cal['desplantado'] = dict(planta('desplantado', L2 - td, R2 + td), s=S_DESPLANTA, votos_devolvidos=float(td.sum()),
                              margem_resultante=float((L2 - td).sum() - (R2 + td).sum()))
    cal['enxerga_3_57_pela_letra'] = bool(reg['criterio']['indicio'])
    for nome, f in (('letra', lambda c: c['indicio']), ('so_primeira_condicao', lambda c: c['leitura_so_primeira_condicao']['indicio']),
                    ('ruido_medido', lambda c: c['leitura_ruido_medido']['indicio'])):
        vis = [s for s in GRADE if f(cal['grade'][f'{s:.4f}']['criterio'])]
        cal['menor_fracao_enxergada_' + nome] = min(vis) if vis else None
    out['calibracao'] = cal

    # D9: tradução em votos
    k = cal['inclinacao_k']

    def votos(x):
        s = x / k
        return {'diferenca_de_A': x, 's_equivalente': s, 'votos_trocados': s * VOTOS_FLAVIO_2T, 'efeito_na_margem': 2 * s * VOTOS_FLAVIO_2T,
                'fracao_da_margem': 2 * s * VOTOS_FLAVIO_2T / MARGEM}
    cp = out['criterio_principal']
    out['traducao_em_votos'] = {
        'inclinacao_k_A_por_unidade_de_s': k, 'margem_oficial': MARGEM, 'votos_trocados_que_viram': MARGEM / 2,
        'A_bruto_de_2026_inteiro': votos(A_princ[2026]),
        'excesso_E_sobre_o_maior_ano_de_governo': votos(-cp['E']),
        '2026_menos_2014': votos(A_princ[2026] - A_princ[2014]),
        '2026_menos_espelho_de_2022': votos(A_princ[2026] + A_princ[2022]),
        '2026_menos_media_dos_anos_de_governo': votos(-(abs(A_princ[2026]) - out['descritivo_anos_de_governo']['media'])),
        'ruido_de_0_01': votos(-RUIDO_REGISTRO), 'limiar_de_0_03': votos(-0.03), 'limiar_de_0_015': votos(-0.015)}
    # veredito pela letra
    v = cp['veredito']
    if not cal['enxerga_3_57_pela_letra']:
        v_final = 'SEM PODER'
    else:
        v_final = v
    out['veredito_do_criterio_sem_olhar_o_poder'] = v
    out['veredito'] = v_final
    out['veredito_por_parte'] = {
        'parte 1, indício além da incumbência (critério da equipe vermelha)': v_final,
        'parte 1, leitura do critério sozinho, sem a regra do poder': v,
        'parte 2, o sinal de A acompanha quem governa ou o PT (regra D5, pesos iguais)': out['quem_governa_ou_pt']['classificacao']}
    # calibração da parte 2 com o que já foi calculado: a classificação com 2026 "desplantado"
    Ad = dict(A_princ); Ad[2026] = cal['desplantado']['A']['iguais'][0]
    out['quem_governa_ou_pt_com_2026_desplantado'] = quem_governa_ou_pt(Ad)['classificacao']
    gravar(out, saida_json)

    # ------------------------------------------------------------ EXPLORATÓRIO (feito depois de ver os resultados)
    ex = {'aviso': 'tudo neste bloco foi decidido depois de ver os resultados; não entra no veredito'}
    # E1: o critério sem 2006 entre os anos de comparação (2006 domina o máximo)
    def sem2006(A26):
        comp = [y for y in anos_de_governo(A_princ, 2026) if y != 2006]
        ymax = max(comp, key=lambda y: abs(A_princ[y])); E = abs(A26) - abs(A_princ[ymax])
        return {'anos_de_comparacao': comp, 'ano_do_maior': ymax, 'maior_abs_A': abs(A_princ[ymax]), 'E': E,
                'indicio_letra': bool(E >= LIM_INDICIO and E > 3 * RUIDO_REGISTRO), 'indicio_so_0015': bool(E >= LIM_INDICIO)}
    e1 = {'oficial': sem2006(A_princ[2026]), 'grade': {k: sem2006(v['A']['iguais'][0]) for k, v in cal['grade'].items()}}
    for nome in ('indicio_letra', 'indicio_so_0015'):
        vis = [float(k) for k, v in e1['grade'].items() if v[nome]]
        e1['menor_fracao_enxergada_' + nome] = min(vis) if vis else None
    ex['E1_criterio_sem_2006'] = e1
    # E2: razão bruta entre os votos do 2º e do 1º turno por faixa (conferência de sentido, sem regressão)
    e2 = {}
    for y in rodados:
        Bq = Bs[y]; _, g = np.unique(Bq.loc, return_inverse=True); nl = int(g.max()) + 1
        L1, R1, O1, BN1, C1, c28, L2q, R2q, BN2, C2 = Bq.arr.T
        den = np.bincount(g, L1 + R1 + O1 - c28, nl); ok = den > 0; den1 = np.where(ok, den, 1.0)
        fR = np.bincount(g, R1, nl) / den1; fL = np.bincount(g, L1, nl) / den1
        e2[str(y)] = {'total_L': [float(L1.sum()), float(L2q.sum())], 'total_R': [float(R1.sum()), float(R2q.sum())], 'faixas': []}
        for i, (lo, hi) in enumerate(FAIXAS):
            sL = (ok & (fR >= lo) & (fR < hi))[g]; sR = (ok & (fL >= lo) & (fL < hi))[g]
            e2[str(y)]['faixas'].append({'faixa': NOME_FAIXA[i], 'razao_L': float(L2q[sL].sum() / L1[sL].sum()),
                                         'razao_R': float(R2q[sR].sum() / R1[sR].sum())})
    ex['E2_razao_bruta_2T_sobre_1T'] = e2
    # E3: o que o braço SEM SINAL enxerga na grade (menor fração plantada que tira 2026 de SEM SINAL)
    sai = [float(k) for k, v in cal['grade'].items() if v['criterio']['veredito'] != 'SEM SINAL']
    ex['E3_menor_fracao_que_tira_de_SEM_SINAL'] = min(sai) if sai else None
    # E4: fração de troca uniforme que o braço INDÍCIO exigiria, pela inclinação k
    ex['E4_fracao_exigida_pelo_indicio'] = {
        'com_2006': (-(cp['maior_abs_A'] + 3 * RUIDO_REGISTRO) - A_princ[2026]) / k,
        'sem_2006': (-(e1['oficial']['maior_abs_A'] + 3 * RUIDO_REGISTRO) - A_princ[2026]) / k}
    # E5: ruído entre conjuntos sem o U_7
    amp2 = {}
    for y in rodados:
        vals = [res[u][y]['A']['iguais'][0] for u in res if u != 'U_7' and y in res[u] and res[u][y]['A']]
        if len(vals) > 1:
            amp2[str(y)] = float(max(vals) - min(vals))
    ex['E5_amplitude_sem_U_7'] = amp2
    # E6: d de 2026 contra 2014 e contra o espelho de 2022, faixa a faixa
    f26, f14, f22 = (res['U_proprio'][y]['faixas'] for y in (2026, 2014, 2022))
    ex['E6_d_de_2026_contra_2014_e_espelho_de_2022_por_faixa'] = {
        '2026_menos_2014': [[a['d'][0] - b['d'][0], float(np.hypot(a['d'][1], b['d'][1]))] for a, b in zip(f26, f14)],
        '2026_menos_espelho_de_2022': [[a['d'][0] + b['d'][0], float(np.hypot(a['d'][1], b['d'][1]))] for a, b in zip(f26, f22)],
        'd_faixa_menos_de_35_por_ano': {str(y): res['U_proprio'][y]['faixas'][0]['d'][0] for y in rodados}}
    # E7: plantado a favor do PT (3,57% dos votos da direita para o PT) nos dois anos que separam governo de PT
    e7 = {'anos': {}}; Ap = dict(A_princ)
    for y in (2002, 2022):
        if y not in rodados:
            continue
        By = Bs[y]; t = S_REGISTRO * By.arr[:, 7]
        r = parcial(f'plantado_PT_{y}', lambda: estat(By, None, By.arr[:, 6] + t, By.arr[:, 7] - t))
        Ap[y] = r['A']['iguais'][0]
        e7['anos'][str(y)] = {'A_oficial': A_princ[y], 'A_plantado': Ap[y], 'vantagem_governo_plantado': Ap[y],
                              'votos_movidos': float(t.sum())}
    e7['classificacao_com_os_dois_plantados'] = quem_governa_ou_pt(Ap)['classificacao']
    ex['E7_plantado_a_favor_do_PT_nos_anos_que_separam'] = e7
    out['exploratorio'] = ex
    out['desvios'] = DESVIOS
    pc_ = os.path.join(p_trab, 'conferencia_funcao_publicada.json')   # conferência extra, feita por fora (ver o texto)
    if os.path.exists(pc_):
        out['conferencia_extra_funcao_publicada_nas_bases_novas'] = json.load(open(pc_, encoding='utf-8'))
    out['contagem_de_leituras'] = {
        'vereditos_registrados': 1, 'leituras_ao_lado_do_criterio': len(out['criterio_ao_lado']),
        'alvos_do_espelho': len(out['espelho_cada_ano_como_alvo']),
        'sinais_em_2026': int(out['criterio_principal']['indicio']) + sum(int(v['indicio']) for v in out['criterio_ao_lado'].values())}
    gravar(out, saida_json)
    print('veredito', v_final, '| critério', v, '| quem governa ou PT:', out['quem_governa_ou_pt']['classificacao'], flush=True)
    escrever(out, saida_txt)


def res_json(res):
    return {u: {str(y): r for y, r in d.items()} for u, d in res.items()}


# ---------------------------------------------------------------- texto
ROT_FAIXA = {'0.00-0.35': 'menos de 35%', '0.35-0.50': '35 a 50%', '0.50-0.65': '50 a 65%', '0.65-1.00': '65% ou mais'}
ROT_GOV = {'L': 'PT', 'R': 'direita', None: 'sem'}


def n4(x):
    return f'{x:+.4f}'.replace('.', ',')


def u4(x):
    return f'{x:.4f}'.replace('.', ',')


def mil(x):
    return f'{int(round(x)):,}'.replace(',', '.')


def pc(x, nd=2):
    return f'{100 * x:.{nd}f}%'.replace('.', ',')


def dec(x, nd=1):
    return f'{x:.{nd}f}'.replace('.', ',')


def fr(x):
    return 'nenhuma até 8%' if x is None else pc(x, 1)


DESVIOS = [
    'D1. Código próprio; conferência contra T35 e F21 publicados com tolerância de 5e-7 (deu 2e-15).',
    'D2. Universo principal = todas as seções do ano com os dois turnos. Ao lado: U_T35, U_F21, U_0210 e U_7. Ruído medido = maior amplitude do A de pesos iguais do mesmo ano entre universos.',
    'D3. Pesos iguais = média simples de d nas faixas válidas; erro-padrão agrupado por local entre as faixas. Ao lado: inverso da variância, votos dos dois finalistas, seções da direita, cada um com os seus votos.',
    'D4. Leitura do critério: anos de comparação 2002, 2006, 2010, 2014 e 2022; INDÍCIO = E de 0,015 ou mais E acima de 0,03 (ruído do registro, 0,01); SEM SINAL = 2026 a até 0,010 de menos A(2022) e de A(2014); o resto INCONCLUSIVO.',
    'D5. Regra para "acompanha quem governa" e "acompanha o PT" (limiar 0,015; 2002 e 2022 e pelo menos 3 dos 4 anos de governo do PT); 2018 como placebo; tabela dos quatro atributos.',
    'D6. Extração de 2002, 2006 e 2010: 13 = PT, 45 = adversário, 95 branco, 96 e 97 nulo, comparecimento = soma dos votos; local do 2º turno; regra para o ano "ligar" (os três cumpriram).',
    'D7. Calibração: troca uniforme de s dos votos de Flávio para Lula; s = 3,57% e grade; "enxerga" = INDÍCIO pela letra; se não, SEM PODER; relato do desplantado.',
    'D8. Espelho: cada ano como alvo; 2018; plantado ao contrário.',
    'D9. Tradução em votos pela inclinação medida no plantado.',
    'D10 e D11. Exploratório marcado; arquivos de trabalho fora do repositório.',
    'Não feito aqui: o cruzamento com o teste de capacidade de troca do T14, que o reteste proposto menciona, é da onda A3.']


def escrever(out, saida_txt):
    out = json.loads(json.dumps(out))   # chaves de ano como texto
    R = out['resultados_por_universo']; P = R['U_proprio']; ap = out['A_iguais_principal']
    cp = out['criterio_principal']; q = out['quem_governa_ou_pt']; cal = out['calibracao']; tr = out['traducao_em_votos']
    ex = out['exploratorio']; rodados = [int(y) for y in ap]
    A = {y: ap[str(y)]['A'] for y in rodados}; EP = {y: ap[str(y)]['ep_agrupado_entre_faixas'] for y in rodados}
    T = []
    w = T.append
    w('R27_A4 (Adendo 27, onda A, teste A4): CURVA POR FORÇA COM A SÉRIE LONGA, 2002 a 2026')
    w('Registro: PRE-REGISTRO-2026-10-26.md, Adendo 27, commit 2748895 (10/11/2026 00:16:42 UTC), e registro/adendo27/equipe_vermelha_relatorio.json, fragilidade "T35 (curva de perda própria por força local do adversário)".')
    w('Script: scripts/analisar_R27_A4.py (python3 -I). Números completos: resultados/R27_A4_curva_forca_serie.json.')
    w('Decisões que o registro não fixa: escritas no docstring antes de somar qualquer voto de 2002, 2006 e 2010 (cópia com hora em /home/user/trabalho-eleicao/adendo27/R27_A4/docstring_antes_de_rodar.txt, SHA-256 ' + out['docstring_antes_de_rodar']['sha256'] + ').')
    w('Aviso do registro: este reteste foi escolhido por quem já conhecia os resultados antigos (o critério é novo, a escolha do que retestar não é cega). O Léo suspeita também de 2014, 2018 e 2022; esses anos, e 2002 a 2010, não são régua limpa. Por isso o valor bruto de 2026 vai ao lado de toda comparação.')
    w('')
    w('VEREDITO PELA LETRA')
    w(f'  Parte 1, indício além da incumbência: {out["veredito"]}. O critério, lido sozinho, dá {out["veredito_do_criterio_sem_olhar_o_poder"]} (2026 a {u4(cp["dist_espelho_2022"])} do espelho de 2022 e a {u4(cp["dist_2014"])} de 2014; limite 0,010). Mas o braço de INDÍCIO não enxerga a troca plantada de 3,57%: o maior |A| dos anos com governo candidato é o de {cp["ano_do_maior"]} ({u4(cp["maior_abs_A"])}), e nenhuma fração da grade até 8% chega lá. Pela regra da calibração, o veredito é SEM PODER.')
    w(f'  Parte 2, o sinal de A acompanha quem governa ou o PT (regra D5 do docstring, pesos iguais): {q["classificacao"]}. O candidato do governo perde menos dos próprios eleitores nos {q["sinal_de_A_contra_atributos"]["lado do governo"]["acertos"]} anos com governo candidato, inclusive 2002 (Serra) e 2022 (Bolsonaro), em que o governo não era o PT. Frágil em 2002 ({n4(A[2002])}, limiar 0,015) e dependente da ponderação (com inverso da variância e com peso por votos a regra dá NEM UM NEM OUTRO).')
    w('')
    w('0. O QUE É A ESTATÍSTICA')
    w('   Em cada ano, os locais de votação são separados em quatro faixas pela fatia do adversário no 1º turno. Em cada faixa, uma regressão por seção (com efeito fixo de local) mede quanto cada finalista perde, do 1º para o 2º turno, dos próprios votos do 1º turno. d = perda da direita menos perda do PT (negativo: a direita perde mais dos próprios). A = média de d nas quatro faixas, com pesos iguais (ponderação principal do Adendo 27). Uma troca de votos da direita para o PT dentro da urna aparece como a direita "perdendo" os próprios eleitores, ou seja, A negativo.')
    w('')
    w('1. BASES')
    w('   2014, 2018, 2022 e 2026: dados/secoesAAAA.json.gz, como estão. 2002, 2006 e 2010: votação por seção do TSE (cdn.tse.jus.br/estatistica/sead/odsele/votacao_secao/votacao_secao_AAAA_BR.zip, só presidente), um ano por vez, tamanho conferido pelo pedido de cabeçalho, CRC do zip conferido, lido em fluxo, zip apagado depois.')
    for y in (2002, 2006, 2010):
        m = out['extracao'].get(str(y))
        if not m:
            w(f'   {y}: NÃO RODADO ({out["nao_rodados"].get(str(y))})'); continue
        c = m['conferencia_oficial']
        w(f'   {y}: {mil(m["bytes"])} bytes, SHA-256 {m["sha256"]}; {mil(m["linhas"])} linhas; seções {mil(m["secoes_1t"])} no 1º turno, {mil(m["secoes_2t"])} no 2º, {mil(m["secoes_dois_turnos"])} com os dois; local inválido em {m["secoes_com_local_invalido_2t"]}; local diferente entre os turnos em {m["secoes_com_local_diferente_entre_turnos"]}.')
        w(f'         soma das seções contra o total oficial: 1º turno PT {mil(c["1"]["L"]["base"])} (dif {c["1"]["L"]["dif"]:+d}), 45 {mil(c["1"]["R"]["base"])} (dif {c["1"]["R"]["dif"]:+d}); 2º turno PT {mil(c["2"]["L"]["base"])} (dif {c["2"]["L"]["dif"]:+d}), 45 {mil(c["2"]["R"]["base"])} (dif {c["2"]["R"]["dif"]:+d}).')
    w('   Os totais oficiais de 2002, 2006 e 2010 foram escritos de memória no docstring antes de somar; os doze batem voto a voto. O arquivo do TSE não traz aptos nem comparecimento: comparecimento = soma dos votos de presidente da seção (A não usa aptos).')
    if out['nao_rodados']:
        w('   NÃO RODADOS: ' + '; '.join(f'{y}: {m}' for y, m in out['nao_rodados'].items()))
    else:
        w('   Nenhum ano ficou sem rodar.')
    w('')
    w('2. CONFERÊNCIA DO CÓDIGO PRÓPRIO CONTRA O PUBLICADO (D1), na ponderação original (inverso da variância)')
    cf = out['conferencia_D1']
    for y, v in cf['T35_bweb'].items():
        w(f'   T35_curva_forca_bweb.json {y}: A aqui {n4(v["A_meu"][0])} ({u4(v["A_meu"][1])}), publicado {n4(v["A_publicado"][0])} ({u4(v["A_publicado"][1])}); contagens iguais; maior diferença {v["maior_diferenca_absoluta"]:.1e}')
    for y, v in cf['F21_serie_principal'].items():
        w(f'   F21_serie_anos.json {y} (331.087 seções): A aqui {n4(v["A_meu"][0])} ({u4(v["A_meu"][1])}), publicado {n4(v["A_publicado"][0])} ({u4(v["A_publicado"][1])}); maior diferença {v["maior_diferenca_absoluta"]:.1e}')
    v = cf['F21_r2_2014']
    w(f'   F21 r2, 2014 nas chaves de 2026 (340.005 seções): A aqui {n4(v["A_meu"][0])}, publicado {n4(v["A_publicado"][0])}; maior diferença {v["maior_diferenca_absoluta"]:.1e}')
    w('   Reproduz tudo: ' + ('sim' if cf['tudo_reproduz'] else 'NÃO') + ' (faixa a faixa: seções, locais, coeficientes próprios, d, erros-padrão e A). O código é próprio (somas dentro do local em numpy), não importa analisar_curva_forca.py nem lib.py.')
    cx = out.get('conferencia_extra_funcao_publicada_nas_bases_novas')
    if cx:
        w('   Conferência extra, depois da rodada (confere_funcao_publicada.py, na pasta de trabalho): a função publicada do T35, rodada nas bases novas, dá os mesmos números do código próprio: ' + '; '.join(f'{y} A original {n4(v["A_inv_var_publicada"][0])} e pesos iguais {n4(v["A_iguais_publicada"])}, maior diferença em d {v["maior_diferenca_d"]:.1e}' for y, v in cx.items()) + '.')
    w('')
    w('3. SÉRIE PRINCIPAL: universo próprio de cada ano (todas as seções com os dois turnos), pesos iguais nas quatro faixas')
    w('   A = média de d; ep = erro-padrão agrupado por local, também entre as faixas. "Vantagem do governo" = quanto o candidato do governo perde a menos dos próprios eleitores.')
    w('   ano  | governo  | seções  | A pesos iguais (ep)   | vantagem do governo | vantagem do PT | A inverso da variância | A peso por votos')
    for y in rodados:
        r = P[str(y)]; g = INFO[y]['governo']
        vg = '        sem' if g is None else n4(-A[y] if g == 'L' else A[y]).rjust(11)
        w(f'   {y} | {ROT_GOV[g]:8s} | {mil(r["secoes"])} | {n4(A[y])} ({u4(EP[y])})    | {vg}         | {n4(-A[y])}        | {n4(r["A"]["inv_var"][0])}                | {n4(r["A"]["votos"][0])}')
    w('   Candidatos: ' + '; '.join(f'{y} {INFO[y]["pt"]} (13) contra {INFO[y]["direita"]}' for y in rodados) + '.')
    w('')
    w('   Faixa a faixa (fatia do adversário no local, 1º turno): coeficiente dos próprios votos do PT e da direita (erro-padrão), d, e locais com 2 ou mais seções (PT/direita)')
    for y in rodados:
        for f in P[str(y)]['faixas']:
            if 'd' in f:
                w(f'   {y} {ROT_FAIXA[f["faixa"]]:12s}: PT {n4(f["proprio_L"][0])} ({u4(f["proprio_L"][1])}), direita {n4(f["proprio_R"][0])} ({u4(f["proprio_R"][1])}), d {n4(f["d"][0])} ({u4(f["d"][1])}); locais {mil(f["locais_L"])}/{mil(f["locais_R"])}')
            else:
                w(f'   {y} {ROT_FAIXA[f["faixa"]]:12s}: fora (menos de 30 locais)')
    w('   As quatro faixas são válidas nos sete anos.' if len(out['faixas_comuns']['faixas']) == 4 else '   Faixas válidas em todos os anos: ' + ', '.join(out['faixas_comuns']['faixas']))
    w('')
    w('4. O CRITÉRIO, PELA LETRA (pesos iguais, universo próprio)')
    w(f'   Valor bruto de 2026: A = {n4(A[2026])} (ep {u4(EP[2026])}; {mil(P["2026"]["secoes"])} seções).')
    w('   Anos com governo candidato usados na comparação: ' + ', '.join(f'{y} |A| = {u4(abs(A[y]))}' for y in cp['anos_de_comparacao']) + '.')
    w(f'   INDÍCIO além da incumbência pede |A(2026)| acima do maior desses em 0,015 ou mais, a mais de 3 vezes o ruído de 0,01 (ou seja, mais de 0,03). Excesso E = {u4(abs(A[2026]))} - {u4(cp["maior_abs_A"])} ({cp["ano_do_maior"]}) = {n4(cp["E"])}. Não cumpre nenhuma das duas condições.')
    w(f'   SEM SINAL pede 2026 a até 0,010 do espelho de 2022 e de 2014: |{n4(A[2026])} - ({n4(-A[2022])})| = {u4(cp["dist_espelho_2022"])} (ep {u4(cp["ep_dist_espelho_2022"])}) e |{n4(A[2026])} - ({n4(A[2014])})| = {u4(cp["dist_2014"])} (ep {u4(cp["ep_dist_2014"])}). Cumpre as duas.')
    w(f'   Critério lido sozinho: {cp["veredito"]}. O resultado é o que a equipe vermelha previu como provável: 2026 repete 2014 e espelha 2022.')
    w('')
    w('5. A PERGUNTA QUE DECIDE: O SINAL DE A ACOMPANHA QUEM GOVERNA OU ACOMPANHA O PT?')
    w('   Regra fixada no docstring (D5), limiar 0,015: "acompanha quem governa" se o candidato do governo tiver vantagem de 0,015 ou mais em 2002 e em 2022 (os dois anos em que governo e PT estão em lados opostos) e em pelo menos 3 dos 4 anos de governo do PT.')
    for y in q['anos']:
        if not y['rodado']:
            w(f'   {y["ano"]}: não rodado'); continue
        yy = y['ano']; g = y['governo']
        quem = 'sem candidato do governo' if g is None else ('governo = PT' if g == 'L' else 'governo = direita, PT na oposição')
        vg = '' if g is None else f'; vantagem do governo {n4(y["vantagem_governo"])} ({"cumpre" if y["vantagem_governo"] >= LIM_GOV else "não cumpre"} 0,015)'
        w(f'   {yy} ({quem}): A {n4(y["A_iguais"])} (ep {u4(EP[yy])}); quem perde menos dos próprios: {"PT" if y["lado_que_perde_menos"] == "L" else "direita"}{vg}')
    w(f'   Classificação pela regra: {q["classificacao"]} (2002 e 2022 cumprem; anos de governo do PT que cumprem: {q["anos_governo_PT_com_vantagem_do_governo"]} de 4).')
    p18 = q.get('placebo_2018')
    if p18:
        w(f'   Placebo da explicação "quem governa": 2018, sem candidato do governo, tem A = {n4(p18["A_iguais"])}, o menor |A| da série; ' + ('abaixo de 0,015, como a explicação pede.' if p18['abaixo_de_0015'] else 'NÃO fica abaixo de 0,015.'))
    w('   Sinal de A contra quatro atributos (em quantos anos o lado indicado é o que perde menos dos próprios):')
    for nome, v in q['sinal_de_A_contra_atributos'].items():
        falha = [y for y in v['anos_com_o_atributo'] if y not in v['anos_em_que_o_lado_perde_menos']]
        w(f'     {nome}: {v["acertos"]} de {v["de"]}' + (f' (falha em {", ".join(str(y) for y in falha)})' if falha else ''))
    w(f'   Fragilidade de 2002: {n4(A[2002])} com ep {u4(EP[2002])}; passa o limiar de 0,015 por {u4(A[2002] - LIM_GOV)}, isto é, {dec((A[2002] - LIM_GOV) / EP[2002], 2)} erro-padrão; fica a {dec(A[2002] / EP[2002], 1)} erros-padrão de zero. Nas seções comuns: {n4(R["U_0210"]["2002"]["A"]["iguais"][0])} (U_0210) e {n4(R["U_7"]["2002"]["A"]["iguais"][0])} (U_7), abaixo do limiar.')
    al = out['quem_governa_ou_pt_ao_lado']
    w('   Ao lado: ' + '; '.join(f'{k}: {v["classificacao"]}' for k, v in al.items()) + '.')
    w(f'   Com inverso da variância os A são: ' + ', '.join(f'{y} {n4(P[str(y)]["A"]["inv_var"][0])}' for y in rodados) + '. Com peso por votos: ' + ', '.join(f'{y} {n4(P[str(y)]["A"]["votos"][0])}' for y in rodados) + '. Nessas duas, 2010 e 2014 ficam perto de zero (governo do PT sem vantagem) e 2018 passa de 0,015 a favor de Bolsonaro; 2002, 2006, 2022 e 2026 continuam a favor do governo.')
    w(f'   A classificação não depende de 2026: com 2026 "desplantado" (item 6), a regra dá {out["quem_governa_ou_pt_com_2026_desplantado"]}.')
    w('')
    w('6. CALIBRAÇÃO POR EFEITO PLANTADO (dados de 2026, universo próprio)')
    w('   Irregularidade plantada: troca uniforme de uma fração s dos votos de Flávio para Lula no 2º turno, em toda seção (brancos, nulos e comparecimento intactos).')
    w('   s      | votos movidos | A pesos iguais | deslocamento | d por faixa (menos de 35, 35 a 50, 50 a 65, 65 ou mais) | critério')
    for k_, v in cal['grade'].items():
        c = v['criterio']
        w(f'   {pc(v["s"]):6s} | {mil(v["votos_movidos"]):>13s} | {n4(v["A"]["iguais"][0])}        | {n4(v["deslocamento_A_iguais"])}      | ' + ', '.join(n4(x) for x in v['d_por_faixa']) + f' | E {n4(c["E"])}: {c["veredito"]}')
    g357 = cal['grade'][f'{S_REGISTRO:.4f}']; b = cal['binomial_3_57']; e = cal['espelho_L_para_F_3_57']; dp = cal['desplantado']
    w(f'   Tamanho do registro, s = 3,57% ({mil(g357["votos_movidos"])} votos, efeito de {mil(2 * g357["votos_movidos"])} na margem): A vai de {n4(A[2026])} a {n4(g357["A"]["iguais"][0])} (deslocamento {n4(g357["deslocamento_A_iguais"])}; por faixa ' + ', '.join(n4(x) for x in g357['deslocamento_de_d_por_faixa']) + f'). Com sorteio binomial por seção (semente {b["semente"]}, {mil(b["votos_movidos"])} votos): {n4(b["A"]["iguais"][0])}.')
    w(f'   Inclinação: A muda {n4(cal["inclinacao_k"])} por unidade de s (cada 1% dos votos de Flávio trocado desloca A em {n4(cal["inclinacao_k"] / 100)}).')
    w(f'   O braço de INDÍCIO enxerga os 3,57%? NÃO: E = {n4(g357["criterio"]["E"])} (precisava passar de +0,03). Menor fração da grade enxergada: pela letra, {fr(cal["menor_fracao_enxergada_letra"])}; só pela primeira condição (0,015), {fr(cal["menor_fracao_enxergada_so_primeira_condicao"])}; com o ruído medido aqui, {fr(cal["menor_fracao_enxergada_ruido_medido"])}. Motivo: 2006 ({u4(cp["maior_abs_A"])}) está entre os anos de comparação. VEREDITO PELA LETRA: SEM PODER.')
    w(f'   O que o teste ainda enxerga: com o plantado o critério deixa de dar SEM SINAL e passa a INCONCLUSIVO (2026 fica a {u4(g357["criterio"]["dist_espelho_2022"])} do espelho de 2022 e a {u4(g357["criterio"]["dist_2014"])} de 2014).')
    w(f'   "Desplantado": se o resultado oficial já contivesse a troca que zera a margem (s = {pc(dp["s"], 4)} dos votos verdadeiros de Flávio, {mil(dp["votos_devolvidos"])} votos devolvidos, margem resultante {mil(dp["margem_resultante"])}), a eleição "limpa" teria A = {n4(dp["A"]["iguais"][0])}, com d por faixa ' + ', '.join(n4(x) for x in dp['d_por_faixa']) + ' e coeficiente próprio de Flávio ' + ', '.join(n4(x) for x in dp['proprio_R']) + '.')
    w('   Limite dito antes de rodar: a base onde se planta já é o resultado oficial. O plantado mostra o que uma troca A MAIS faria. Se a troca já estiver no oficial, o que o critério julga é o próprio oficial, comparado com anos que não são régua limpa.')
    w('')
    w('7. ESPELHO')
    w('   (i) O mesmo critério de INDÍCIO com cada ano de governo candidato como alvo e os demais como comparação:')
    for y, v in out['espelho_cada_ano_como_alvo'].items():
        w(f'       {y}: |A| {u4(abs(v["A_alvo"]))}, maior dos demais {u4(v["maior_abs_A"])} ({v["ano_do_maior"]}), E {n4(v["E"])}: ' + ('INDÍCIO' if v['indicio'] else 'não'))
    w('       O único ano que o critério aponta é 2006 (a favor de Lula, então presidente), não 2026 nem 2022.')
    if p18:
        w(f'   (ii) 2018, onde não deveria dar nada pela explicação "quem governa": {n4(p18["A_iguais"])} com pesos iguais (abaixo de 0,015). Não é zero: em outros conjuntos de seções vai de {n4(min(out["ruido_entre_conjuntos"]["por_ano"]["2018"]["por_universo"].values()))} a {n4(max(out["ruido_entre_conjuntos"]["por_ano"]["2018"]["por_universo"].values()))}.')
    w(f'   (iii) Plantado no sentido contrário (3,57% dos votos de Lula para Flávio, {mil(e["votos_movidos"])} votos): A vai a {n4(e["A"]["iguais"][0])} (deslocamento {n4(e["deslocamento_A_iguais"])}). O teste responde com o sinal oposto e tamanho parecido: não tem viés de lado.')
    w('')
    w('8. VALOR BRUTO DE 2026 E TRADUÇÃO EM VOTOS DE MARGEM')
    w(f'   Régua: pela calibração, A = {n4(tr["inclinacao_k_A_por_unidade_de_s"])} x s. Margem oficial {mil(MARGEM)}; viram o resultado {mil(MARGEM / 2)} votos trocados.')
    for nome, rot in (('A_bruto_de_2026_inteiro', 'O A bruto de 2026 inteiro, se fosse todo atribuído a uma troca uniforme'),
                      ('2026_menos_2014', '2026 menos 2014 (outro ano com o PT no governo)'),
                      ('2026_menos_espelho_de_2022', '2026 menos o espelho de 2022 (Bolsonaro no governo)'),
                      ('ruido_de_0_01', 'O ruído de 0,01 entre conjuntos de seções'),
                      ('limiar_de_0_03', 'O limiar de 0,03 (3 ruídos)')):
        v = tr[nome]
        w(f'   {rot}: diferença de A {n4(v["diferenca_de_A"])} = troca de {pc(v["s_equivalente"])} dos votos de Flávio = {mil(v["votos_trocados"])} votos = {mil(v["efeito_na_margem"])} de margem ({pc(v["fracao_da_margem"], 1)} da margem oficial).')
    w(f'   Para o braço de INDÍCIO acusar 2026, com 2006 na comparação, |A| teria de passar de {u4(cp["maior_abs_A"] + 0.03)}: uma troca uniforme de {pc(ex["E4_fracao_exigida_pelo_indicio"]["com_2006"], 1)} dos votos de Flávio, {mil(ex["E4_fracao_exigida_pelo_indicio"]["com_2006"] * VOTOS_FLAVIO_2T)} votos (conta feita depois de ver, E4).')
    w('')
    w('9. AO LADO: OUTROS CONJUNTOS DE SEÇÕES, OUTRAS PONDERAÇÕES E O RUÍDO')
    w(f'   Seções comuns: 2002, 2006 e 2010 (U_0210) {mil(out["U_0210"]["secoes"])}; 2014 a 2026 (U_F21) 331.087; os sete anos (U_7) {mil(out["U_7"]["secoes"])} ({pc(out["U_7"]["frac_das_secoes_2026"], 1)} das seções de 2026).')
    w('   A de pesos iguais por conjunto de seções:')
    for y in rodados:
        pu = out['ruido_entre_conjuntos']['por_ano'][str(y)]['por_universo']
        w(f'     {y}: ' + ', '.join(f'{u} {n4(v)}' for u, v in pu.items()) + f'; amplitude {u4(out["ruido_entre_conjuntos"]["por_ano"][str(y)]["amplitude"])}')
    w(f'   Ruído medido aqui (maior amplitude): {u4(out["ruido_entre_conjuntos"]["maior_amplitude"])}, em 2018, quase quatro vezes o 0,01 do registro. Sem o U_7 (exploratório): ' + ', '.join(f'{y} {u4(v)}' for y, v in ex['E5_amplitude_sem_U_7'].items()) + '.')
    w('   O critério em cada leitura ao lado (nenhuma decide):')
    for nome, v in out['criterio_ao_lado'].items():
        w(f'     {nome}: A(2026) {n4(v["A_alvo"])}, maior |A| {u4(v["maior_abs_A"])} ({v["ano_do_maior"]}), E {n4(v["E"])}, distância ao espelho de 2022 {u4(v["dist_espelho_2022"])}, a 2014 {u4(v["dist_2014"])}: {v["veredito"]}')
    w('')
    w('10. A FAVOR DA TESE (o que este teste deixa em pé)')
    w(f'   a) O valor bruto. Em 2026 Flávio perde mais dos próprios eleitores que Lula em 3 das 4 faixas (d de {n4(P["2026"]["faixas"][1]["d"][0])}, {n4(P["2026"]["faixas"][2]["d"][0])} e {n4(P["2026"]["faixas"][3]["d"][0])}), A = {n4(A[2026])}, a {dec(abs(A[2026]) / EP[2026], 0)} erros-padrão de zero. Lido como troca uniforme, esse A inteiro vale {pc(tr["A_bruto_de_2026_inteiro"]["s_equivalente"])} dos votos de Flávio, {mil(tr["A_bruto_de_2026_inteiro"]["votos_trocados"])} votos, {mil(tr["A_bruto_de_2026_inteiro"]["efeito_na_margem"])} de margem: {pc(tr["A_bruto_de_2026_inteiro"]["fracao_da_margem"], 0)} da margem oficial. Tirando do oficial a troca que zera a margem, o A de 2026 cai para {n4(dp["A"]["iguais"][0])}, praticamente zero. O tamanho do sinal bruto é o de uma troca que vira a eleição.')
    w(f'   b) O braço de INDÍCIO não tem poder. Com 2006 na régua, só uma troca de {pc(ex["E4_fracao_exigida_pelo_indicio"]["com_2006"], 0)} seria acusada. "Não deu indício" aqui não é evidência de ausência.')
    w(f'   c) A régua não é limpa. O teste compara 2026 com anos de que o Léo também suspeita. Um mecanismo "a favor de quem está no governo" em toda eleição produziria exatamente esta série; o teste separa "a favor do PT sempre" de "a favor do governo", não separa "vantagem natural de quem governa" de "mecanismo a favor do governo".')
    w(f'   d) Na ponderação original (inverso da variância) e no peso por votos, 2026 NÃO repete 2014 nem 2010: 2026 {n4(P["2026"]["A"]["inv_var"][0])} e {n4(P["2026"]["A"]["votos"][0])}, contra 2014 {n4(P["2014"]["A"]["inv_var"][0])} e {n4(P["2014"]["A"]["votos"][0])} e 2010 {n4(P["2010"]["A"]["inv_var"][0])} e {n4(P["2010"]["A"]["votos"][0])}. Nessas leituras o critério dá INCONCLUSIVO (distância a 2014 de {u4(out["criterio_ao_lado"]["U_proprio, ponderação inv_var"]["dist_2014"])}, cerca de {pc(out["criterio_ao_lado"]["U_proprio, ponderação inv_var"]["dist_2014"] / abs(cal["inclinacao_k"]))} de troca equivalente). A vantagem do governo do PT que aparece em 2010 e 2014 com pesos iguais vem das três faixas de 35% para cima; na faixa de menos de 35%, a de mais locais e a que mais pesa no inverso da variância, d é positivo nesses anos (o PT perde mais).')
    w(f'   e) 2002, o ano novo que mais importa para separar "governo" de "PT", passa o limiar por pouco ({n4(A[2002])}, ep {u4(EP[2002])}) e fica abaixo dele nas seções comuns ({n4(R["U_0210"]["2002"]["A"]["iguais"][0])} em U_0210 e {n4(R["U_7"]["2002"]["A"]["iguais"][0])} em U_7). O sinal é o mesmo em todos os conjuntos e ponderações de A (positivo, a favor de Serra), mas o tamanho é pequeno. A separação "governo, não PT" apoia-se com folga só em 2022.')
    w(f'   f) O ruído entre conjuntos de seções medido aqui ({u4(out["ruido_entre_conjuntos"]["maior_amplitude"])}) é maior que o 0,01 que o critério supôs. Nas seções comuns aos sete anos o critério dá INCONCLUSIVO, não SEM SINAL.')
    w('')
    w('11. CONTRA A TESE')
    w(f'   a) 2026 não se destaca dos outros anos com governo candidato. Com pesos iguais: 2014 {n4(A[2014])}, 2026 {n4(A[2026])}, 2022 espelhado {n4(-A[2022])}, 2010 {n4(A[2010])}. A diferença de 2026 para 2014 ({u4(cp["dist_2014"])}) e para o espelho de 2022 ({u4(cp["dist_espelho_2022"])}) vale cerca de {pc(tr["2026_menos_2014"]["s_equivalente"])} de troca, {mil(tr["2026_menos_2014"]["votos_trocados"])} a {mil(tr["2026_menos_espelho_de_2022"]["votos_trocados"])} votos, perto de um décimo da margem, e fica abaixo do ruído de 0,01.')
    w(f'   b) O sinal de A acompanha o governo, não o PT. Em 2002 (PSDB no governo, Lula eleito com 61%) quem perde menos dos próprios é Serra ({n4(A[2002])}); em 2022 (Bolsonaro no governo, Lula eleito) é Bolsonaro ({n4(A[2022])}). Um mecanismo a favor do PT em toda eleição pede A negativo nesses dois anos; os dois são positivos. Lado do governo: 6 de 6; lado do PT: 4 de 7; quem venceu: 5 de 7; quem liderou o 1º turno: 4 de 7.')
    c06 = out['extracao']['2006']['conferencia_oficial']
    w(f'   c) O ano extremo é 2006, não 2026: |A| = {u4(abs(A[2006]))}, {dec(abs(A[2006]) / abs(A[2026]), 1)} vezes o de 2026. Em 2006 Alckmin teve MENOS votos no 2º turno que no 1º ({mil(c06["1"]["R"]["base"])} para {mil(c06["2"]["R"]["base"])}, total oficial). Pela mesma régua (aproximação) isso equivaleria a uma troca de cerca de {pc(abs(A[2006]) / abs(cal["inclinacao_k"]), 0)} dos votos dele. A estatística responde, e muito, ao movimento do eleitor entre os turnos; não mede só troca dentro da urna. Ressalva: quem suspeita de 2006 lê o mesmo número como sinal; este teste não separa as duas leituras.')
    w(f'   d) Sem candidato do governo (2018), A é o menor da série ({n4(A[2018])}).')
    mx1 = max(max(P[str(y)]['faixas'][0]['proprio_L'][0], P[str(y)]['faixas'][0]['proprio_R'][0]) for y in rodados)
    mxd = max(P[str(y)]['faixas'][0]['d'][0] for y in rodados)
    w(f'   e) A forma. Uma troca uniforme desloca d por igual nas quatro faixas (' + ', '.join(n4(x) for x in g357['deslocamento_de_d_por_faixa']) + f' para 3,57%). O d observado em 2026 vai de {n4(P["2026"]["faixas"][0]["d"][0])} na faixa de menos de 35% a {n4(P["2026"]["faixas"][3]["d"][0])} na de 65% ou mais, uma escada parecida com a de 2010 ({n4(P["2010"]["faixas"][0]["d"][0])} a {n4(P["2010"]["faixas"][3]["d"][0])}) e a de 2014 ({n4(P["2014"]["faixas"][0]["d"][0])} a {n4(P["2014"]["faixas"][3]["d"][0])}), deslocada para baixo na primeira faixa (ver E6). Na eleição "desplantada", Flávio teria coeficiente próprio de {n4(dp["proprio_R"][0])} na primeira faixa (ganharia votos onde já tinha mais) e d de {n4(dp["d_por_faixa"][0])}; nos sete anos nenhum candidato tem coeficiente próprio positivo nessa faixa (o maior é {n4(mx1)}) e o maior d dela é {n4(mxd)}. Isso pesa contra uma troca UNIFORME desse tamanho; não exclui troca concentrada onde Lula é forte.')
    w('')
    w('12. O QUE ISSO SIGNIFICA')
    w('   A série longa responde à pergunta que o Adendo 27 fez: o sinal de A acompanha quem governa, não o PT. Os dois anos que separam (2002 e 2022) vão contra o PT, um com folga (2022) e um no limite (2002).')
    w('   Para a tese de fraude em 2026, o teste não decide. O critério dá SEM SINAL porque 2026 repete 2014 e espelha 2022, mas o braço que acusaria fraude não tem poder, e a comparação é com anos que também estão sob suspeita. O que fica de pé é a pergunta sobre a série inteira: por que o candidato do governo perde menos dos próprios eleitores em toda eleição desde 2002, seja de que partido for. Vantagem natural de quem governa (este teste não mede de onde ela viria) e mecanismo a favor do governo dão o mesmo desenho aqui. O que distingue as duas não está neste teste: são os testes que olham dentro da urna e os que comparam com fontes independentes da urna.')
    w('   O valor bruto de 2026 tem o tamanho de uma troca que viraria a eleição. Isso é fato e não é prova: 2014 tem o mesmo tamanho com Dilma no governo e a urna abaixo das pesquisas para o PT (F21), 2022 tem o mesmo tamanho a favor de Bolsonaro, que perdeu, e 2006 tem mais de cinco vezes esse tamanho.')
    w('')
    w('13. PISTAS (para outros testes; nada aqui foi registrado antes)')
    w('   1. A pergunta passa a ser da série: medir a mesma estatística em 2º turno de governador (2018, 2022 e 2026) e de prefeito, onde o governante candidato é de partidos dos dois lados no mesmo dia. Se o governante candidato de oposição ao governo federal tiver a mesma vantagem, um mecanismo central a favor do governo federal não a explica; se a vantagem só aparecer para presidente, a pista fica.')
    w('   2. A forma por faixa separa troca uniforme de troca concentrada: o que resta para a tese é uma troca maior onde Lula é forte. O teste de capacidade de troca do T14 (onda A3) e o teste das testemunhas (D4-3 e D4-4) são os que enxergam isso.')
    w('   3. Nas seções comuns aos sete anos (as mais antigas), 2018 muda de sinal (' + n4(R['U_7']['2018']['A']['iguais'][0]) + ') e 2014 cresce (' + n4(R['U_7']['2014']['A']['iguais'][0]) + '). A estatística depende da idade da seção; vale olhar A por data de criação da seção antes de comparar anos.')
    w('')
    w('14. EXPLORATÓRIO (feito depois de ver os resultados; não entra no veredito)')
    e1 = ex['E1_criterio_sem_2006']
    w(f'   E1. O critério sem 2006 na comparação (2006 domina o máximo): maior |A| passa a ser {u4(e1["oficial"]["maior_abs_A"])} ({e1["oficial"]["ano_do_maior"]}); E de 2026 = {n4(e1["oficial"]["E"])}, não é INDÍCIO. Nessa leitura o teste teria poder: enxergaria o plantado a partir de {pc(e1["menor_fracao_enxergada_indicio_letra"], 1)} pela letra e de {pc(e1["menor_fracao_enxergada_indicio_so_0015"], 1)} só pela primeira condição; 3,57% daria E = {n4(e1["grade"][f"{S_REGISTRO:.4f}"]["E"])}, INDÍCIO. Fração exigida pela letra: {pc(ex["E4_fracao_exigida_pelo_indicio"]["sem_2006"])}.')
    w(f'   E2. Razão bruta entre os votos do 2º e do 1º turno por faixa, sem regressão (conferência de sentido). 2006, direita: ' + ', '.join(f'{f["razao_R"]:.3f}'.replace('.', ',') for f in ex['E2_razao_bruta_2T_sobre_1T']['2006']['faixas']) + '; PT: ' + ', '.join(f'{f["razao_L"]:.3f}'.replace('.', ',') for f in ex['E2_razao_bruta_2T_sobre_1T']['2006']['faixas']) + '. 2026, direita: ' + ', '.join(f'{f["razao_R"]:.3f}'.replace('.', ',') for f in ex['E2_razao_bruta_2T_sobre_1T']['2026']['faixas']) + '; PT: ' + ', '.join(f'{f["razao_L"]:.3f}'.replace('.', ',') for f in ex['E2_razao_bruta_2T_sobre_1T']['2026']['faixas']) + '. Os sete anos estão no JSON.')
    w(f'   E3. Menor fração plantada da grade que tira 2026 de SEM SINAL: {pc(ex["E3_menor_fracao_que_tira_de_SEM_SINAL"], 1)}.')
    w(f'   E4 e E5. Usados nos itens 8 e 9: fração de troca que o braço de INDÍCIO exigiria ({pc(ex["E4_fracao_exigida_pelo_indicio"]["com_2006"], 1)} com 2006, {pc(ex["E4_fracao_exigida_pelo_indicio"]["sem_2006"])} sem 2006) e amplitude de A entre conjuntos de seções sem o U_7.')
    e6 = ex['E6_d_de_2026_contra_2014_e_espelho_de_2022_por_faixa']
    w('   E6. d de 2026 menos d de 2014, por faixa (erro-padrão): ' + ', '.join(f'{n4(x[0])} ({u4(x[1])})' for x in e6['2026_menos_2014']) + '. d de 2026 menos o espelho de 2022: ' + ', '.join(f'{n4(x[0])} ({u4(x[1])})' for x in e6['2026_menos_espelho_de_2022']) + '. Uma troca uniforme daria a mesma diferença nas quatro faixas; não é o que aparece (o sinal muda de faixa para faixa). Na faixa de menos de 35%, d por ano: ' + ', '.join(f'{y} {n4(v)}' for y, v in e6['d_faixa_menos_de_35_por_ano'].items()) + '. Aí 2026 fica abaixo de 2010 e 2014 em cerca de 0,015 a 0,017 (a favor da tese: nessa faixa, a maior, 2026 não repete os outros anos de governo do PT; contra: nas faixas de 35 a 50% 2026 fica ACIMA de 2014).')
    e7 = ex['E7_plantado_a_favor_do_PT_nos_anos_que_separam']
    w('   E7. A parte 2 enxergaria uma troca a favor do PT nos anos que separam? Plantando 3,57% dos votos da direita para o PT: ' + '; '.join(f'{y}: A de {n4(v["A_oficial"])} para {n4(v["A_plantado"])} (vantagem do governo {n4(v["vantagem_governo_plantado"])})' for y, v in e7['anos'].items()) + f'. Com os dois plantados a regra daria {e7["classificacao_com_os_dois_plantados"]}. Ou seja, a regra reage a uma troca desse tamanho; e, lida ao contrário, o A positivo de 2002 e de 2022 não prova que não houve troca a favor do PT nesses anos, só que, se houve, foi menor que a vantagem do candidato do governo.')
    w('')
    w('15. DESVIOS (decisões que o registro não fixa, escritas no docstring antes de calcular)')
    for d in DESVIOS:
        w('   ' + d)
    w('')
    cl = out['contagem_de_leituras']
    w('16. CONTAGEM')
    w(f'   Um veredito registrado (parte 1) e uma classificação com regra fixada no docstring (parte 2). Ao lado: {cl["leituras_ao_lado_do_criterio"]} leituras do critério em outros universos e ponderações e {cl["alvos_do_espelho"]} alvos no espelho. SINAL em 2026: {cl["sinais_em_2026"]} de {1 + cl["leituras_ao_lado_do_criterio"]}. No espelho, 1 de {cl["alvos_do_espelho"]} (2006). O limiar é de 3 ruídos, sem distribuição de referência (cinco anos de comparação): não dá para dizer quantos sinais o acaso daria; dá para dizer que nenhum apareceu em 2026.')
    w('   Falta: a conferência independente por outro agente com código próprio (regra do Adendo 27).')
    txt = '\n'.join(T) + '\n'
    assert chr(0x2014) not in txt and chr(0x2013) not in txt   # sem travessão longo nem meio
    with open(saida_txt, 'w', encoding='utf-8') as f:
        f.write(txt)


def main():
    if len(sys.argv) > 1 and sys.argv[1] == 'extrair':
        extrair(sys.argv[2], int(sys.argv[3]), sys.argv[4])
    elif len(sys.argv) > 1 and sys.argv[1] == 'rodar':
        rodar(*sys.argv[2:7])
    else:
        raise SystemExit(__doc__)


if __name__ == '__main__':
    main()
