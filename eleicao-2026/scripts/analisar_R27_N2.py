"""R27_N2: QUEM NÃO VOLTOU. Mobilização do 1º turno ou retirada (teste N2 do Adendo 28 do pré-registro, por inteiro).

Adendo 28 (commit 938be19, 10/11/2026 04:36:33 UTC), escrito depois da Onda A e antes de rodar. O critério vale como
está no adendo. Este docstring foi escrito ANTES de qualquer conta com votos deste teste; o que ele decide e o registro
não fixa está em DECISÕES e sai no resultado como desvio. Até aqui só foi lida estrutura sem voto: o formato do bweb
(45 colunas, cargo 6 = Deputado Federal, tipos de voto 1 Nominal, 2 Branco, 3 Nulo, 4 Legenda), as chaves das bases de
dados/, a contagem de seções do universo (442.491 de 497.897 com aptos iguais nos dois turnos), a contagem das que
ligam com 2022 (409.088), o número de municípios (5.571) e de zonas (2.640) e as UFs com bloco de governador no 2º
turno. O que eu já conhecia de resultado: o texto de resultados/ADENDO27_ondaA_resultados.txt (o indício do
comparecimento, 2,67% contra -0,85%, e a ordem das UFs: PI, MA, TO, PB, CE no alto; RS, RJ, SC, SP no pé). Não li os
resultados de N1, B2 e B3.

Uso:
  python3 -I scripts/analisar_R27_N2.py extrair   uma passada no bweb do 1º turno (filtro por bytes): deputado federal
                                                  por seção (partidos 22 e 13, nominal e legenda) e nomes de município
  python3 -I scripts/analisar_R27_N2.py base      monta os vetores do universo (2026, ligação com 2022) e os outros anos
  python3 -I scripts/analisar_R27_N2.py rodar     calcula tudo e grava resultados/R27_N2_quem_nao_voltou.json
  python3 -I scripts/analisar_R27_N2.py texto     escreve resultados/R27_N2_quem_nao_voltou.txt a partir do JSON
Trabalho e parciais: /home/user/trabalho-eleicao/adendo27/R27_N2/

Pergunta. A Onda A mostrou que o eleitor de Flávio do 1º turno não voltou no 2º muito mais que o de Lula. Duas
leituras: (a) mobilização local do 1º turno (campanhas de deputado, senador e governador) que não se repetiu no 2º;
(b) retirada, isto é, eleitor de Flávio que votou e ficou registrado como ausente, ou voto dele que não entrou.
Limite dito no registro: boletim não distingue quem ficou em casa de quem foi registrado como ausente. O teste mede
se a explicação sem fraude deixa as marcas que deveria deixar.

O QUE O REGISTRO FIXA (aplicado à letra)
- Universo: seções das 27 UFs com aptos iguais nos dois turnos de 2026.
- y = (comparecimento do 2º turno menos o do 1º) sobre aptos.
- Modelo 0: y contra as fatias sobre aptos de Flávio, Lula, eliminados e branco mais nulo no 1º turno, efeito fixo de
  município, peso aptos, erro por município. Assimetria = coeficiente de Flávio menos o de Lula.
- Marca (i): a assimetria diminui quando se controla o "puxão local" do 1º turno, medido por seção como a fatia dos
  candidatos do partido 22 a deputado federal sobre aptos menos a fatia de Flávio sobre aptos, e pelo comparecimento
  do 1º turno de 2026 menos o de 2022 na mesma seção (onde a chave liga).
- Marca (ii): a assimetria é maior nos municípios pequenos e nas UFs sem 2º turno de governador.
- Leitura: "explicada pela mobilização" se a assimetria cair 50% ou mais com os controles e as duas marcas de (ii)
  aparecerem a mais de 3 erros-padrão; "não explicada" se cair menos de 20%; entre os dois, inconclusivo.
- Calibração: retirada plantada de 3,6% dos votos de Flávio (para a abstenção, em toda seção) tem de aumentar a
  assimetria no modelo com controles tanto quanto no modelo sem controles.
- Descritivo: a assimetria por UF, por porte do município e por faixa de força de Lula, com mapa das 20 zonas de
  maior valor para conferência de cadernos.
- Dos avisos do Adendo 27 e das regras desta onda: calibração por efeito plantado nos dados de 2026, plantio também
  da explicação inocente, teste espelho, valor bruto de 2026 ao lado de qualquer comparação com outro ano, tradução
  em votos de margem.

DECISÕES QUE O REGISTRO NÃO FIXA (tomadas aqui, antes de calcular qualquer coisa com votos)
D1. Universo U: chaves de dados/secoes2026.json.gz com UF diferente de ZZ, com os blocos "1" e "2" e aptos do 1º
    turno iguais aos do 2º e maiores que zero. Nenhum outro filtro (nenhuma seção de U tem comparecimento zero).
    Seção sem linha de deputado federal no bweb do 1º turno sai dos modelos com o puxão e é contada.
D2. Variáveis, todas sobre aptos da seção: F = Flávio 1º turno; L = Lula 1º turno; E = eliminados (campo O da base,
    que inclui o 28 anulado); BN = brancos mais nulos do 1º turno. A categoria omitida é a abstenção do 1º turno, de
    modo que cada coeficiente é "variação do comparecimento por eleitor daquele tipo, em relação a um faltoso".
D3. Modelo 0: mínimos quadrados com peso aptos, efeito fixo de município (UF|código), erro agrupado por município
    (CR1, a mesma fórmula de scripts/lib.py, com código próprio e conferência contra lib.fe_ols). A0 = bF menos bL,
    erro pela covariância agrupada. Convenção: A negativa quer dizer que o eleitor de Flávio voltou menos que o de
    Lula; "tamanho" da assimetria = menos A. "Diminuir", "cair" e "maior" referem-se ao tamanho.
D4. Controles da marca (i), pela letra:
    P = D22/aptos menos F, onde D22 = votos NOMINAIS dos candidatos do partido 22 a deputado federal na seção no 1º
        turno (bweb, CD_CARGO_PERGUNTA 6, tipo Nominal, NR_PARTIDO 22). O voto de legenda no 22 não é voto em
        candidato e fica fora da conta principal; ao lado, P com nominais mais legenda.
    T = comparecimento do 1º turno de 2026 sobre aptos de 2026 menos comparecimento do 1º turno de 2022 sobre aptos
        do 1º turno de 2022, na mesma chave UF|município|zona|seção de dados/secoes2022.json.gz (aptos de 2022
        maiores que zero). Subuniverso U22 = seções de U em que a chave liga. Ao lado: só as seções em que os aptos
        de 2022 ficam a 20% dos de 2026 (a mesma chave pode ter passado a outro grupo de eleitores).
    Modelos: M0 em U; M0+P em U; em U22: M0, M0+T, M0+P e M0+P+T.
    Queda principal Q = 1 menos A(M0+P+T em U22) / A(M0 em U22), os dois na mesma amostra. Ao lado: Q só com P (em U
    e em U22) e Q só com T. Erro de Q por reamostragem de municípios (999 réplicas, semente 20261110) e intervalo de
    95% por percentis. A leitura usa a estimativa pontual de Q (o registro não fixa erro para os 50% e 20%); se o
    intervalo cruzar um limiar, isso é dito.
    Aviso de parametrização, escrito antes de rodar: com P no modelo, o coeficiente de F passa a medir "mais F e mais
    D22 juntos" (porque P contém menos F). O mesmo ajuste com D22/aptos no lugar de P dá outro coeficiente de F
    (a diferença é o coeficiente de P). A conta principal é a da letra (P como escrito). Ao lado, sempre, a versão
    "D" (D22/aptos como regressor). Para T a escolha não muda a assimetria (T desloca os quatro coeficientes por
    igual). O plantio inocente (D8) diz qual das duas parametrizações distingue mobilização de retirada. Se as duas
    derem leituras diferentes, o veredito pela letra é o de P e a divergência entra no veredito.
D5. Marcas (ii), no modelo 0 em U:
    Município pequeno = menos de 20.000 aptos no 1º turno de 2026 (soma de todas as seções do município na base).
    Ao lado: cortes de 10.000 e 50.000. UFs com 2º turno de governador: AC, AM, DF, ES, RN, TO (bloco "2g" da base);
    as outras 21 são o grupo "sem". Estimativa: modelo 0 separado em cada grupo (os grupos são conjuntos de
    municípios, logo independentes no erro agrupado); D = A(grupo da marca) menos A(complemento), erro = raiz da soma
    das variâncias. A marca "aparece" se D tiver o sinal de A0 (assimetria de tamanho maior nos pequenos, ou nas UFs
    sem governador) e |D|/erro passar de 3. Ao lado, para a marca das UFs (só 27 unidades): assimetria de cada UF e
    teste de permutação exato das 296.010 escolhas de 6 UFs em 27 (média simples e média ponderada pelos votos de
    Flávio). O que decide é a letra (erro por município).
D6. Leitura e veredito:
    Q de 0,50 ou mais e as duas marcas (ii): "explicada pela mobilização" = SEM SINAL.
    Q abaixo de 0,20 (inclusive Q negativo, assimetria que cresce com os controles): "não explicada" = SINAL, no
    sentido estreito de que a explicação inocente não deixou a marca (i); pelo limite dito no registro, isso não prova
    retirada. Qualquer outro caso (inclusive Q de 0,50 ou mais sem as duas marcas): INCONCLUSIVO.
    Se A0 não for negativa a mais de 3 erros-padrão, não há assimetria a explicar e o teste é relatado como sem objeto.
D7. Calibração do registro (retirada plantada): em cada seção de U, x ~ Binomial(votos de Flávio no 2º turno; 0,036),
    semente 20261110; esses eleitores passam à abstenção do 2º turno (y cai x/aptos). "Votos de Flávio" = os do 2º
    turno, porque é ali que a retirada operaria (3,57% dos votos de Flávio do 2º turno é o tamanho que vira o
    resultado por troca). Ao lado: 3,6% dos votos de Flávio do 1º turno e a versão sem sorteio (0,036 x votos).
    Medida: dA0 = variação de A no modelo 0; dA1 = variação de A no modelo com controles, mesma amostra; r = dA1/dA0.
    "Tanto quanto" = r de 0,80 ou mais (os controles engolem menos de 20% de uma retirada real, o mesmo 20% da
    leitura). Se r ficar abaixo de 0,80, os controles engolem retirada verdadeira, uma queda de A deixa de distinguir
    mobilização de retirada, e o veredito é SEM PODER.
D8. Plantio da explicação inocente (exigência desta onda), sempre com o MESMO total de eleitores do plantio D7:
    Inocente A (puxão do deputado do 22): x ~ Binomial(D22; tA) em cada seção de U, tA = total do D7 / soma de D22.
      Quem veio no 1º turno puxado pelo candidato a deputado do 22 não volta, a taxa constante.
    Inocente B (comparecimento extra do 1º turno): só em U22, x = tB x max(T, 0) x aptos, tB tal que o total em U22
      seja o do D7 em U22 (sem sorteio; se tB passar de 1 fica em 1 e o total alcançado é dito).
      Quem compareceu no 1º turno de 2026 a mais do que em 2022 não volta.
    Medida: a mesma r do D7. O teste "distingue" as duas leituras se a retirada (D7) tiver r de 0,80 ou mais e o
    plantio inocente tiver r de 0,50 ou menos (os controles engolem metade ou mais). Se o plantio inocente não for
    engolido, o resultado "não explicada" só quer dizer "estes dois controles não explicam", não "mobilização
    excluída", e isso entra no veredito como falta de poder para acusar. Também é relatado se o plantio D7 mexe nas
    marcas (ii) (não deveria: é uniforme) e a diferença mínima que cada marca (ii) detecta a 3 erros-padrão.
D9. Espelhos:
    E1 (controle espelho): P13 = D13/aptos menos L (candidatos do partido 13 a deputado federal) no lugar de P. Se a
        assimetria cair com o puxão do PT tanto quanto com o do 22, a queda não é marca da mobilização da direita.
    E2 (plantio espelho): retirada de 3,6% dos votos de Lula do 2º turno; tem de mover A no sentido contrário, com e
        sem controles.
    E3 (onde não deveria dar o mesmo): modelo 0, marcas (ii) e controle T (contra a eleição anterior, onde a base
        liga) em 2014, 2018 e 2022, com as UFs de 2º turno de governador de cada ano (2018 e 2022 pelo bloco "2g";
        2014 pela lista publicada em R27_A1: AC, AM, AP, CE, DF, GO, MS, PA, PB, RJ, RN, RO, RR, RS), sempre com o
        valor bruto de 2026 ao lado. O controle P não existe para outros anos (o bweb deles não está em disco).
        O Léo suspeita também desses anos: eles entram como comparação, não como régua de inocência.
D10. Votos de margem: V = menos A x (votos de Flávio no 1º turno no universo) = eleitores de Flávio que não voltaram
    acima da taxa do eleitor de Lula. Cada um vale 1 voto de margem (não 2, porque não vira voto de Lula). V0 pelo
    modelo 0, V1 pelo modelo com controles; V0 menos V1 = parte que os controles absorvem. Ao lado a margem oficial
    (4.430.191) e o plantio de 3,6% em votos.
D11. Descritivo: A do modelo 0 estimada dentro de cada recorte, com efeito fixo de município.
    Por UF: erro por município; no DF (um município só) erro por zona.
    Por porte (aptos do município no 1º turno): até 10 mil; 10 a 20 mil; 20 a 50 mil; 50 a 200 mil; 200 mil ou mais.
    Por faixa de força de Lula na seção (Lula sobre válidos do 1º turno): menos de 35%; 35 a 50; 50 a 65; 65 ou mais.
    Por zona eleitoral (UF|zona): efeito fixo de município dentro da zona, erro robusto por seção (HC1); só zonas com
    50 ou mais seções em U. Lista das 20 zonas de maior tamanho de assimetria (menos A), com erro, seções, municípios,
    votos de Flávio, V da zona e a coordenada mediana dos locais de votação (cadastro do TSE). Como a estimativa por
    zona é ruidosa, cada zona da lista traz também o limite conservador (tamanho menos 1,645 erro) e é dito quantas
    das 20 ficam acima do tamanho nacional por esse limite. Ao lado, a lista das 20 pelo limite conservador.
D12. Sensibilidades (não decidem): sem peso; efeito fixo de local de votação (UF|município|zona|local) com erro por
    município; P com legenda; cortes de município pequeno de 10 e 50 mil; ligação com 2022 restrita a aptos a 20%.
D13. Tudo o que for feito depois de ver resultado fica na chave "exploratorio" do JSON e marcado no texto.
"""
# Comandos acrescentados DEPOIS de ver o resultado de "rodar" (bloco exploratório, não muda veredito):
#   explorar           efeito fixo em outros níveis, faixas e portes por ano, 2026 contra 2022 por UF, zonas por votos
#   extrair_partidos   segunda passada no bweb do 1º turno: deputado federal por partido, por seção
#   explorar2          puxão medido pelos candidatos a deputado federal de todos os partidos
# Ordem completa: extrair, base, rodar, explorar, extrair_partidos, explorar2, texto.
import collections
import csv
import glob
import gzip
import hashlib
import io
import itertools
import json
import os
import sys
import time
import zipfile

import numpy as np

AQUI = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.dirname(AQUI)
DADOS = os.path.join(REPO, 'dados')
TRAB = '/home/user/trabalho-eleicao/adendo27/R27_N2'
ZIPS1 = '/home/user/trabalho-eleicao/bweb1t/zips'
LOCAIS = '/home/user/trabalho-eleicao/adendo21/F14_dl_locais/eleitorado_local_votacao_2026.zip'
SAIDA_JSON = os.path.join(REPO, 'resultados', 'R27_N2_quem_nao_voltou.json')
SAIDA_TXT = os.path.join(REPO, 'resultados', 'R27_N2_quem_nao_voltou.txt')
SEMENTE = 20261110
MARGEM = 4430191
TAXA = 0.036
GOV = {2026: ['AC', 'AM', 'DF', 'ES', 'RN', 'TO'],
       2022: ['AL', 'AM', 'BA', 'ES', 'MS', 'PB', 'PE', 'RO', 'RS', 'SC', 'SE', 'SP'],
       2018: ['AM', 'AP', 'DF', 'MG', 'MS', 'PA', 'RJ', 'RN', 'RO', 'RR', 'RS', 'SC', 'SE', 'SP'],
       2014: ['AC', 'AM', 'AP', 'CE', 'DF', 'GO', 'MS', 'PA', 'PB', 'RJ', 'RN', 'RO', 'RR', 'RS']}
PEQUENO = 20000
PORTES = [(0, 10000, 'até 10 mil'), (10000, 20000, '10 a 20 mil'), (20000, 50000, '20 a 50 mil'),
          (50000, 200000, '50 a 200 mil'), (200000, 10 ** 9, '200 mil ou mais')]
FAIXAS = [(0.0, 0.35, 'menos de 35%'), (0.35, 0.50, '35 a 50%'), (0.50, 0.65, '50 a 65%'), (0.65, 1.01, '65% ou mais')]
NCOL = 45
I_UF, I_MUN, I_NMUN, I_ZONA, I_SEC, I_CARGO, I_PART = 10, 11, 12, 13, 14, 16, 18
I_TV, I_NV, I_Q = 27, 29, 31


def diga(*a):
    print(time.strftime('%H:%M:%S'), *a, flush=True)


def grava(nome, obj):
    os.makedirs(TRAB, exist_ok=True)
    tmp = os.path.join(TRAB, nome + '.tmp')
    with open(tmp, 'w') as f:
        json.dump(obj, f, ensure_ascii=False, indent=1)
    os.replace(tmp, os.path.join(TRAB, nome))


# ---------------------------------------------------------------- extração do bweb (deputado federal, 1º turno)
def _campos(linha):
    p = linha.rstrip(b'\r\n').split(b';')
    if len(p) == NCOL:
        return p, 0
    r = next(csv.reader([linha.decode('latin1')], delimiter=';'))
    return [x.encode('latin1') for x in r], 1


def _extrai_zip(zp):
    z = zipfile.ZipFile(zp)
    nome = [n for n in z.namelist() if n.lower().endswith('.csv')][0]
    sec = {}
    nomes = {}
    nlin = ndf = ncsv = nruim = 0
    tipos = collections.Counter()
    with z.open(nome) as fh:
        bf = io.BufferedReader(fh, 1 << 24)
        cab = [c.strip().strip('"') for c in bf.readline().decode('latin1').rstrip('\r\n').split(';')]
        assert len(cab) == NCOL, (zp, len(cab))
        esperado = {I_UF: 'SG_UF', I_MUN: 'CD_MUNICIPIO', I_NMUN: 'NM_MUNICIPIO', I_ZONA: 'NR_ZONA', I_SEC: 'NR_SECAO',
                    I_CARGO: 'CD_CARGO_PERGUNTA', I_PART: 'NR_PARTIDO', I_TV: 'CD_TIPO_VOTAVEL', I_NV: 'NR_VOTAVEL',
                    I_Q: 'QT_VOTOS'}
        for i, n in esperado.items():
            assert cab[i] == n, (zp, i, cab[i])
        for l in bf:
            nlin += 1
            if b';6;"Deputado Federal";' not in l:
                continue
            p, fb = _campos(l)
            if len(p) != NCOL:
                nruim += 1
                continue
            if p[I_CARGO].strip(b'"') != b'6':
                continue
            ncsv += fb
            ndf += 1
            uf = p[I_UF].strip(b'"').decode()
            mun = int(p[I_MUN].strip(b'"'))
            zona = int(p[I_ZONA].strip(b'"'))
            secao = int(p[I_SEC].strip(b'"'))
            k = f"{uf}|{mun}|{zona}|{secao}"
            tv = int(p[I_TV].strip(b'"'))
            q = int(p[I_Q].strip(b'"'))
            tipos[tv] += q
            s = sec.get(k)
            if s is None:
                # nominal 22, legenda 22, nominal 13, legenda 13, nominais, legendas, brancos, nulos
                s = sec[k] = [0, 0, 0, 0, 0, 0, 0, 0]
                if (uf, mun) not in nomes:
                    nomes[(uf, mun)] = p[I_NMUN].strip(b'"').decode('latin1')
            if tv == 1:
                s[4] += q
                part = int(p[I_PART].strip(b'"'))
                if part == 22:
                    s[0] += q
                elif part == 13:
                    s[2] += q
            elif tv == 4:
                s[5] += q
                part = int(p[I_PART].strip(b'"'))
                if part == 22:
                    s[1] += q
                elif part == 13:
                    s[3] += q
            elif tv == 2:
                s[6] += q
            elif tv == 3:
                s[7] += q
            else:
                tipos['estranho'] += 1
    return os.path.basename(zp), sec, {f'{a}|{b}': n for (a, b), n in nomes.items()}, nlin, ndf, ncsv, nruim, dict(tipos)


def extrair():
    from multiprocessing import Pool
    os.makedirs(TRAB, exist_ok=True)
    zs = sorted(glob.glob(ZIPS1 + '/*.zip'), key=lambda p: -os.path.getsize(p))
    tudo = {}
    nomes = {}
    meta = {'zips': {}, 'tipos_votos': collections.Counter()}
    t0 = time.time()
    with Pool(4) as pool:
        for nome, sec, nm, nlin, ndf, ncsv, nruim, tipos in pool.imap_unordered(_extrai_zip, zs):
            dup = sum(1 for k in sec if k in tudo)
            tudo.update(sec)
            nomes.update(nm)
            meta['zips'][nome] = {'linhas': nlin, 'linhas_depfed': ndf, 'linhas_csv': ncsv, 'linhas_ruins': nruim,
                                  'secoes': len(sec), 'duplicadas': dup}
            for t, c in tipos.items():
                meta['tipos_votos'][str(t)] += c
            diga(f'[{time.time() - t0:5.0f}s] {nome}: {nlin} linhas, {ndf} de deputado federal, {len(sec)} seções')
    meta['tipos_votos'] = dict(meta['tipos_votos'])
    meta['linhas_total'] = sum(v['linhas'] for v in meta['zips'].values())
    meta['linhas_depfed'] = sum(v['linhas_depfed'] for v in meta['zips'].values())
    meta['secoes'] = len(tudo)
    cols = ['nom22', 'leg22', 'nom13', 'leg13', 'nominais', 'legendas', 'brancos', 'nulos']
    meta['totais'] = {c: int(sum(v[i] for v in tudo.values())) for i, c in enumerate(cols)}
    chaves = sorted(tudo)
    M = np.array([tudo[k] for k in chaves], dtype=np.int32)
    np.savez_compressed(os.path.join(TRAB, 'depfed_1t.npz'), chaves=np.array(chaves), M=M, cols=np.array(cols))
    grava('depfed_meta.json', meta)
    grava('nomes_municipios.json', nomes)
    diga('deputado federal gravado', len(tudo), 'seções', meta['totais'])


# ---------------------------------------------------------------- base
def _carrega(ano):
    with gzip.open(os.path.join(DADOS, f'secoes{ano}.json.gz'), 'rt') as f:
        return json.load(f)


def _vetores(S, ano):
    """Vetores do universo (27 UFs, dois turnos, aptos iguais e maiores que zero) de um ano."""
    ks = sorted(k for k, v in S.items() if not k.startswith('ZZ|') and '1' in v and '2' in v
                and v['1']['apt'] == v['2']['apt'] and v['1']['apt'] > 0)
    n = len(ks)
    a = {c: np.zeros(n, dtype=np.int64) for c in ('apt', 'c1', 'c2', 'L1', 'R1', 'O1', 'B1', 'N1', 'L2', 'R2', 'B2', 'N2', 'loc')}
    for i, k in enumerate(ks):
        v1 = S[k]['1']
        v2 = S[k]['2']
        a['apt'][i] = v1['apt']
        a['c1'][i] = v1['comp']
        a['c2'][i] = v2['comp']
        a['L1'][i] = v1['L']; a['R1'][i] = v1['R']; a['O1'][i] = v1['O']; a['B1'][i] = v1['B']; a['N1'][i] = v1['N']
        a['L2'][i] = v2['L']; a['R2'][i] = v2['R']; a['B2'][i] = v2['B']; a['N2'][i] = v2['N']
        a['loc'][i] = v1.get('loc', -1) if v1.get('loc') is not None else -1
    # aptos do município no 1º turno: todas as seções do município na base
    am = collections.Counter()
    for k, v in S.items():
        if '1' in v and not k.startswith('ZZ|'):
            am[k.rsplit('|', 2)[0]] += v['1']['apt']
    a['apt_mun'] = np.array([am[k.rsplit('|', 2)[0]] for k in ks], dtype=np.int64)
    return ks, a


def base():
    os.makedirs(TRAB, exist_ok=True)
    info = {}
    diga('carregando 2026')
    S26 = _carrega(2026)
    info['secoes_27ufs_dois_turnos'] = sum(1 for k, v in S26.items() if not k.startswith('ZZ|') and '1' in v and '2' in v)
    gov26 = sorted({k.split('|')[0] for k, v in S26.items() if '2g' in v})
    assert gov26 == GOV[2026], gov26
    ks, a = _vetores(S26, 2026)
    del S26
    n = len(ks)
    info['universo'] = n
    assert np.all(a['c1'] == a['L1'] + a['R1'] + a['O1'] + a['B1'] + a['N1'])
    # deputado federal
    d = np.load(os.path.join(TRAB, 'depfed_1t.npz'))
    pos = {k: i for i, k in enumerate(d['chaves'].tolist())}
    idx = np.array([pos.get(k, -1) for k in ks])
    info['universo_sem_depfed'] = int((idx < 0).sum())
    M = d['M']
    for j, c in enumerate(d['cols'].tolist()):
        v = np.where(idx >= 0, M[np.maximum(idx, 0), j], -1)
        a['df_' + c] = v.astype(np.int64)
    a['tem_df'] = (idx >= 0)
    # ligação com 2022
    diga('carregando 2022')
    S22 = _carrega(2022)
    c22 = np.full(n, -1, dtype=np.int64)
    a22 = np.full(n, -1, dtype=np.int64)
    for i, k in enumerate(ks):
        v = S22.get(k)
        if v is not None and '1' in v and v['1']['apt'] > 0:
            c22[i] = v['1']['comp']
            a22[i] = v['1']['apt']
    a['c1_2022'] = c22
    a['apt_2022'] = a22
    info['liga_2022'] = int((a22 > 0).sum())
    np.savez_compressed(os.path.join(TRAB, 'base_2026.npz'), chaves=np.array(ks), **a)
    diga('2026 gravado', n, info)
    # outros anos (modelo 0, marcas ii e controle T contra a eleição anterior)
    ant = None
    Sant = None
    for ano in (2022, 2018, 2014):
        S = S22 if ano == 2022 else _carrega(ano)
        if ano in (2022, 2018):
            g = sorted({k.split('|')[0] for k, v in S.items() if '2g' in v})
            assert g == GOV[ano], (ano, g)
        ksa, aa = _vetores(S, ano)
        np.savez_compressed(os.path.join(TRAB, f'base_{ano}.npz'), chaves=np.array(ksa), **aa)
        info[f'universo_{ano}'] = len(ksa)
        if ant is not None:
            # liga o ano posterior (ant) com este (anterior no tempo): comparecimento do 1º turno deste ano
            ksp = np.load(os.path.join(TRAB, f'base_{ant}.npz'))['chaves'].tolist()
            cc = np.full(len(ksp), -1, dtype=np.int64)
            ap = np.full(len(ksp), -1, dtype=np.int64)
            for i, k in enumerate(ksp):
                v = S.get(k)
                if v is not None and '1' in v and v['1']['apt'] > 0:
                    cc[i] = v['1']['comp']
                    ap[i] = v['1']['apt']
            np.savez_compressed(os.path.join(TRAB, f'liga_{ant}_{ano}.npz'), c1_ant=cc, apt_ant=ap)
            info[f'liga_{ant}_{ano}'] = int((ap > 0).sum())
        ant = ano
        del S
        diga(ano, 'gravado', len(ksa))
    S22 = None
    grava('base_info.json', info)
    diga(info)


# ---------------------------------------------------------------- regressão
def _cod(v):
    _, g = np.unique(v, return_inverse=True)
    return g


def fe_wls(y, X, fe, cl, w=None):
    """MQO com peso, efeito fixo (fe) e erro agrupado por cl (CR1, como scripts/lib.py). cl=None: robusto por seção (HC1).
    Grupos do efeito fixo com menos de 2 seções saem. Devolve b, V, N, G."""
    y = np.asarray(y, float)
    X = np.asarray(X, float)
    if X.ndim == 1:
        X = X[:, None]
    n, k = X.shape
    w = np.ones(n) if w is None else np.asarray(w, float)
    g = _cod(fe)
    ok = np.bincount(g)[g] >= 2
    y, X, w, g = y[ok], X[ok], w[ok], g[ok]
    c = None if cl is None else np.asarray(cl)[ok]
    g = _cod(g)
    ng = g.max() + 1
    sw = np.bincount(g, weights=w, minlength=ng)

    def dm(v):
        return v - (np.bincount(g, weights=w * v, minlength=ng) / sw)[g]
    yd = dm(y)
    Xd = np.column_stack([dm(X[:, j]) for j in range(k)])
    XtX = (Xd * w[:, None]).T @ Xd
    b = np.linalg.solve(XtX, (Xd * w[:, None]).T @ yd)
    e = yd - Xd @ b
    N = len(y)
    if c is None:
        S = Xd * (w * e)[:, None]
        G = N
        corr = N / (N - k)
    else:
        cg = _cod(c)
        G = int(cg.max() + 1)
        S = np.column_stack([np.bincount(cg, weights=w * Xd[:, j] * e, minlength=G) for j in range(k)])
        corr = G / (G - 1) * (N - 1) / (N - k) if G > 1 else float('nan')
    inv = np.linalg.inv(XtX)
    V = corr * inv @ (S.T @ S) @ inv
    return b, V, int(N), int(G)


def assim(y, X, fe, cl, w, nomes):
    """Ajusta e devolve coeficientes, erros e a assimetria A = b[F] menos b[L] (as duas primeiras colunas)."""
    b, V, N, G = fe_wls(y, X, fe, cl, w)
    se = np.sqrt(np.diag(V))
    A = b[0] - b[1]
    epA = float(np.sqrt(V[0, 0] + V[1, 1] - 2 * V[0, 1]))
    return {'n': N, 'grupos_erro': G, 'coef': {nm: float(x) for nm, x in zip(nomes, b)},
            'ep': {nm: float(x) for nm, x in zip(nomes, se)}, 'A': float(A), 'ep_A': epA,
            'z_A': float(A / epA) if epA > 0 else None}


def cruz(Z, w, g, ng):
    """Produtos cruzados ponderados dentro do grupo (ng x m x m), para reamostrar municípios sem refazer a conta."""
    m = Z.shape[1]
    sw = np.bincount(g, weights=w, minlength=ng)
    sw1 = np.where(sw > 0, sw, 1)
    sz = np.column_stack([np.bincount(g, weights=w * Z[:, j], minlength=ng) for j in range(m)])
    C = np.empty((ng, m, m))
    for j in range(m):
        wz = w * Z[:, j]
        for l in range(j, m):
            s = np.bincount(g, weights=wz * Z[:, l], minlength=ng) - sz[:, j] * sz[:, l] / sw1
            C[:, j, l] = s
            C[:, l, j] = s
    return C


def a_de_cruz(Cs, iy, ix):
    """Assimetria (b0 menos b1) a partir da soma de produtos cruzados Cs (m x m)."""
    b = np.linalg.solve(Cs[np.ix_(ix, ix)], Cs[ix, iy])
    return b[0] - b[1]


# ---------------------------------------------------------------- análise
def _le_base(ano):
    d = np.load(os.path.join(TRAB, f'base_{ano}.npz'))
    return {k: d[k] for k in d.files}


def _mun_de(chaves):
    return np.array([k.rsplit('|', 2)[0] for k in chaves])


def _uf_de(chaves):
    return np.array([k.split('|', 1)[0] for k in chaves])


def _zona_de(chaves):
    out = []
    for k in chaves:
        p = k.split('|')
        out.append(p[0] + '|' + p[2])
    return np.array(out)


def _marcas(y, X4, mun, w, grupo_a, nomes_grupos, A0):
    """Modelo 0 em dois conjuntos de municípios; D = A(grupo a) menos A(complemento)."""
    ra = assim(y[grupo_a], X4[grupo_a], mun[grupo_a], mun[grupo_a], w[grupo_a], ['F', 'L', 'E', 'BN'])
    rb = assim(y[~grupo_a], X4[~grupo_a], mun[~grupo_a], mun[~grupo_a], w[~grupo_a], ['F', 'L', 'E', 'BN'])
    D = ra['A'] - rb['A']
    ep = float(np.sqrt(ra['ep_A'] ** 2 + rb['ep_A'] ** 2))
    z = D / ep
    return {nomes_grupos[0]: ra, nomes_grupos[1]: rb, 'D': float(D), 'ep_D': ep, 'z': float(z),
            'mesmo_sinal_de_A0': bool(np.sign(D) == np.sign(A0)),
            'aparece': bool(np.sign(D) == np.sign(A0) and abs(z) > 3),
            'diferenca_minima_detectavel_a_3ep': 3 * ep}


def rodar():
    t0 = time.time()
    R = {'teste': 'R27_N2 (Adendo 28, N2): quem não voltou', 'gerado_em_utc': time.strftime('%Y-%m-%d %H:%M:%S', time.gmtime()),
         'registro': 'PRE-REGISTRO-2026-10-26.md, Adendo 28, commit 938be19 (10/11/2026 04:36:33 UTC)'}
    with open(os.path.join(TRAB, 'docstring_antes_de_rodar.sha256')) as f:
        R['docstring_antes_de_rodar'] = f.read().split()
    R['extracao_depfed'] = json.load(open(os.path.join(TRAB, 'depfed_meta.json')))
    R['extracao_depfed'].pop('zips', None)
    R['base_info'] = json.load(open(os.path.join(TRAB, 'base_info.json')))
    B = _le_base(2026)
    ks = B['chaves'].tolist()
    n = len(ks)
    mun = _mun_de(ks)
    uf = _uf_de(ks)
    zona = _zona_de(ks)
    apt = B['apt'].astype(float)
    w = apt
    y = (B['c2'] - B['c1']) / apt
    F = B['R1'] / apt
    L = B['L1'] / apt
    E = B['O1'] / apt
    BN = (B['B1'] + B['N1']) / apt
    X4 = np.column_stack([F, L, E, BN])
    N4 = ['F', 'L', 'E', 'BN']
    tem_df = B['tem_df'].astype(bool)
    D22 = np.where(tem_df, B['df_nom22'], 0).astype(float)
    D22leg = np.where(tem_df, B['df_nom22'] + B['df_leg22'], 0).astype(float)
    D13 = np.where(tem_df, B['df_nom13'], 0).astype(float)
    P = D22 / apt - F
    Pleg = D22leg / apt - F
    Dd = D22 / apt
    P13 = D13 / apt - L
    liga = (B['apt_2022'] > 0)
    T = np.where(liga, B['c1'] / apt - B['c1_2022'] / np.maximum(B['apt_2022'], 1), 0.0)
    U22 = liga & tem_df
    R['universo'] = {
        'secoes': n, 'municipios': int(len(set(mun.tolist()))), 'zonas': int(len(set(zona.tolist()))),
        'aptos': int(B['apt'].sum()), 'comparecimento_1t': int(B['c1'].sum()), 'comparecimento_2t': int(B['c2'].sum()),
        'flavio_1t': int(B['R1'].sum()), 'lula_1t': int(B['L1'].sum()), 'eliminados_1t': int(B['O1'].sum()),
        'bn_1t': int((B['B1'] + B['N1']).sum()), 'flavio_2t': int(B['R2'].sum()), 'lula_2t': int(B['L2'].sum()),
        'margem_2t_no_universo': int(B['L2'].sum() - B['R2'].sum()),
        'sem_depfed': int((~tem_df).sum()), 'liga_2022': int(liga.sum()), 'U22': int(U22.sum()),
        'depfed_nominal_22': int(D22.sum()), 'depfed_legenda_22': int((D22leg - D22).sum()), 'depfed_nominal_13': int(D13.sum()),
        'secoes_com_P_positivo': int((P[tem_df] > 0).sum()),
        'media_ponderada': {'y': float(np.average(y, weights=w)), 'F': float(np.average(F, weights=w)), 'L': float(np.average(L, weights=w)),
                            'E': float(np.average(E, weights=w)), 'BN': float(np.average(BN, weights=w)),
                            'P': float(np.average(P[tem_df], weights=w[tem_df])), 'T_em_U22': float(np.average(T[U22], weights=w[U22]))},
        'dp_ponderado_dentro_do_municipio': {},
    }
    gm = _cod(mun)
    swm = np.bincount(gm, weights=w)

    def dp_dentro(v, mask=None):
        mk_ = np.ones(n, bool) if mask is None else mask
        g_ = _cod(mun[mk_])
        sw_ = np.bincount(g_, weights=w[mk_])
        d_ = v[mk_] - (np.bincount(g_, weights=w[mk_] * v[mk_]) / sw_)[g_]
        return float(np.sqrt(np.average(d_ ** 2, weights=w[mk_])))
    R['universo']['dp_ponderado_dentro_do_municipio'] = {'y': dp_dentro(y), 'F': dp_dentro(F), 'L': dp_dentro(L), 'E': dp_dentro(E), 'BN': dp_dentro(BN),
                                                         'P': dp_dentro(P), 'D': dp_dentro(Dd), 'T_em_U22': dp_dentro(T, U22)}
    # ---------- modelo 0 e conferência contra lib.fe_ols
    m0 = assim(y, X4, mun, mun, w, N4)
    sys.path.insert(0, AQUI)
    import lib
    ref = lib.fe_ols(y, X4, mun, w, N4)
    m0['confere_lib_fe_ols'] = {'max_dif_coef': float(max(abs(ref['coef'][k] - m0['coef'][k]) for k in N4)),
                                'max_dif_ep': float(max(abs(ref['ep'][k] - m0['ep'][k]) for k in N4))}
    A0 = m0['A']
    R['modelo0'] = m0
    diga('modelo 0', m0)
    grava('parcial_modelo0.json', R)

    # ---------- marca (i): controles
    def modelos(mask, yv, lista):
        out = {}
        for nome, cols, nomes in lista:
            out[nome] = assim(yv[mask], np.column_stack([X4[mask]] + [c[mask] for c in cols]), mun[mask], mun[mask], w[mask], N4 + nomes)
        return out
    U = tem_df
    ctl = {'U': modelos(U, y, [('M0', [], []), ('M0+P', [P], ['P']), ('M0+D', [Dd], ['D']), ('M0+Pleg', [Pleg], ['Pleg']),
                               ('M0+P13', [P13], ['P13']), ('M0+P+P13', [P, P13], ['P', 'P13'])]),
           'U22': modelos(U22, y, [('M0', [], []), ('M0+T', [T], ['T']), ('M0+P', [P], ['P']), ('M0+P+T', [P, T], ['P', 'T']),
                                   ('M0+D', [Dd], ['D']), ('M0+D+T', [Dd, T], ['D', 'T']), ('M0+Pleg+T', [Pleg, T], ['Pleg', 'T']),
                                   ('M0+P13+T', [P13, T], ['P13', 'T']), ('M0+P+P13+T', [P, P13, T], ['P', 'P13', 'T'])])}

    def q(a1, a0):
        return float(1 - a1 / a0)
    Q = {'principal_M0+P+T_em_U22': q(ctl['U22']['M0+P+T']['A'], ctl['U22']['M0']['A']),
         'so_P_em_U': q(ctl['U']['M0+P']['A'], ctl['U']['M0']['A']),
         'so_P_em_U22': q(ctl['U22']['M0+P']['A'], ctl['U22']['M0']['A']),
         'so_T_em_U22': q(ctl['U22']['M0+T']['A'], ctl['U22']['M0']['A']),
         'versao_D_M0+D+T_em_U22': q(ctl['U22']['M0+D+T']['A'], ctl['U22']['M0']['A']),
         'versao_D_so_D_em_U': q(ctl['U']['M0+D']['A'], ctl['U']['M0']['A']),
         'P_com_legenda_M0+Pleg+T_em_U22': q(ctl['U22']['M0+Pleg+T']['A'], ctl['U22']['M0']['A']),
         'espelho_P13_M0+P13+T_em_U22': q(ctl['U22']['M0+P13+T']['A'], ctl['U22']['M0']['A']),
         'espelho_so_P13_em_U': q(ctl['U']['M0+P13']['A'], ctl['U']['M0']['A'])}
    R['controles'] = {'modelos': ctl, 'Q': Q}
    diga('Q', Q)
    grava('parcial_controles.json', R)

    # ---------- plantios
    rng = np.random.default_rng(SEMENTE)
    xF = rng.binomial(B['R2'], TAXA).astype(float)
    xF1 = rng.binomial(B['R1'], TAXA).astype(float)
    xL = rng.binomial(B['L2'], TAXA).astype(float)
    tA = xF[U].sum() / D22[U].sum()
    xA = rng.binomial(D22.astype(np.int64), min(tA, 1.0)).astype(float)
    extra = np.where(U22, np.maximum(T, 0) * apt, 0.0)
    tB = min(xF[U22].sum() / extra.sum(), 1.0)
    xB = tB * extra
    ys = {'real': y, 'retirada_2t': y - xF / apt, 'retirada_2t_sem_sorteio': y - TAXA * B['R2'] / apt,
          'retirada_1t': y - xF1 / apt, 'inocente_A': y - xA / apt, 'inocente_B': y - xB / apt,
          'espelho_lula_2t': y - xL / apt}
    R['plantios'] = {'taxa': TAXA, 'semente': SEMENTE,
                     'retirada_2t_eleitores_em_U': float(xF.sum()), 'retirada_2t_eleitores_em_U22': float(xF[U22].sum()),
                     'retirada_1t_eleitores_em_U': float(xF1.sum()),
                     'inocente_A_taxa': float(tA), 'inocente_A_eleitores_em_U': float(xA[U].sum()), 'inocente_A_eleitores_em_U22': float(xA[U22].sum()),
                     'inocente_B_taxa': float(tB), 'inocente_B_eleitores_em_U22': float(xB.sum()),
                     'inocente_B_comparecimento_extra_total_em_U22': float(extra.sum()),
                     'espelho_lula_eleitores_em_U': float(xL.sum())}
    pares = {'U: M0+P (letra, só P)': ('U', U, [P], ['P']), 'U: M0+D (versão D, só D)': ('U', U, [Dd], ['D']),
             'U22: M0+P+T (principal)': ('U22', U22, [P, T], ['P', 'T']), 'U22: M0+D+T (versão D)': ('U22', U22, [Dd, T], ['D', 'T']),
             'U22: M0+T': ('U22', U22, [T], ['T']), 'U22: M0+P': ('U22', U22, [P], ['P'])}
    cal = {}
    for npl, yv in ys.items():
        if npl == 'real':
            continue
        cal[npl] = {}
        for nome, (un, mask, cols, nomes) in pares.items():
            if npl == 'inocente_B' and un == 'U':
                continue
            a0r = ctl[un]['M0']['A']
            a1r = assim(y[mask], np.column_stack([X4[mask]] + [c[mask] for c in cols]), mun[mask], mun[mask], w[mask], N4 + nomes)['A']
            a0p = assim(yv[mask], X4[mask], mun[mask], mun[mask], w[mask], N4)
            a1p = assim(yv[mask], np.column_stack([X4[mask]] + [c[mask] for c in cols]), mun[mask], mun[mask], w[mask], N4 + nomes)
            d0 = a0p['A'] - a0r
            d1 = a1p['A'] - a1r
            cal[npl][nome] = {'A0_real': a0r, 'A1_real': a1r, 'A0_plantado': a0p['A'], 'A1_plantado': a1p['A'],
                              'dA0': float(d0), 'dA1': float(d1), 'r': float(d1 / d0) if d0 != 0 else None,
                              'Q_do_proprio_plantio': float(1 - d1 / d0) if d0 != 0 else None,
                              'Q_com_o_plantio_somado_ao_real': float(1 - a1p['A'] / a0p['A']),
                              'coef_controles_plantado': {k2: a1p['coef'][k2] for k2 in nomes},
                              'coef_F_L_modelo0_plantado': [a0p['coef']['F'], a0p['coef']['L']]}
    R['calibracao'] = cal
    diga('calibração', {k: {m: round(v['r'], 3) for m, v in d.items()} for k, d in cal.items()})
    grava('parcial_calibracao.json', R)

    # ---------- marcas (ii)
    pequeno = B['apt_mun'] < PEQUENO
    semgov = ~np.isin(uf, GOV[2026])
    mk = {'municipio_pequeno_20mil': _marcas(y, X4, mun, w, pequeno, ['pequenos', 'demais'], A0),
          'uf_sem_2t_governador': _marcas(y, X4, mun, w, semgov, ['sem_governador_21', 'com_governador_6'], A0),
          'ao_lado_corte_10mil': _marcas(y, X4, mun, w, B['apt_mun'] < 10000, ['pequenos', 'demais'], A0),
          'ao_lado_corte_50mil': _marcas(y, X4, mun, w, B['apt_mun'] < 50000, ['pequenos', 'demais'], A0)}
    for nome, g in (('municipio_pequeno_20mil', pequeno), ('uf_sem_2t_governador', semgov)):
        mk[nome]['secoes_grupo'] = int(g.sum())
        mk[nome]['municipios_grupo'] = int(len(set(mun[g].tolist())))
        mk[nome]['flavio_1t_grupo'] = int(B['R1'][g].sum())
        mk[nome]['flavio_1t_complemento'] = int(B['R1'][~g].sum())
        mk[nome]['D_em_votos_no_grupo'] = float(-mk[nome]['D'] * B['R1'][g].sum())
    # com a retirada plantada (não deveria mexer)
    yv = ys['retirada_2t']
    mk['com_retirada_plantada'] = {
        'municipio_pequeno_20mil': {k2: _marcas(yv, X4, mun, w, pequeno, ['pequenos', 'demais'], A0)[k2] for k2 in ('D', 'ep_D', 'z')},
        'uf_sem_2t_governador': {k2: _marcas(yv, X4, mun, w, semgov, ['sem', 'com'], A0)[k2] for k2 in ('D', 'ep_D', 'z')}}
    R['marcas_ii'] = mk
    diga('marcas', {k: (round(v['D'], 4), round(v['z'], 2)) for k, v in mk.items() if 'D' in v})
    grava('parcial_marcas.json', R)

    # ---------- descritivo por UF, porte, faixa
    des = {'uf': {}, 'porte': {}, 'faixa_forca_lula': {}}
    for u in sorted(set(uf.tolist())):
        m = uf == u
        nm = len(set(mun[m].tolist()))
        cl = mun[m] if nm >= 10 else zona[m]
        r = assim(y[m], X4[m], mun[m], cl, w[m], N4)
        r.update({'municipios': nm, 'erro_por': 'município' if nm >= 10 else 'zona', 'flavio_1t': int(B['R1'][m].sum()), 'lula_1t': int(B['L1'][m].sum()),
                  'V': float(-r['A'] * B['R1'][m].sum()), 'aptos': int(B['apt'][m].sum()),
                  'd_comp_sobre_aptos': float((B['c2'][m].sum() - B['c1'][m].sum()) / B['apt'][m].sum()),
                  'flavio_2t_menos_1t': int(B['R2'][m].sum() - B['R1'][m].sum()), 'lula_2t_menos_1t': int(B['L2'][m].sum() - B['L1'][m].sum()),
                  'com_2t_governador': u in GOV[2026]})
        if U22[m].sum() > 100 and len(set(mun[m & U22].tolist())) >= 10:
            mm = m & U22
            r0 = assim(y[mm], X4[mm], mun[mm], mun[mm], w[mm], N4)
            r1 = assim(y[mm], np.column_stack([X4[mm], P[mm], T[mm]]), mun[mm], mun[mm], w[mm], N4 + ['P', 'T'])
            r2 = assim(y[mm], np.column_stack([X4[mm], Dd[mm], T[mm]]), mun[mm], mun[mm], w[mm], N4 + ['D', 'T'])
            r.update({'U22_A0': r0['A'], 'U22_A_com_P_T': r1['A'], 'U22_A_com_D_T': r2['A'], 'U22_ep_A_com_P_T': r1['ep_A'],
                      'Q_P_T': float(1 - r1['A'] / r0['A']), 'Q_D_T': float(1 - r2['A'] / r0['A'])})
        des['uf'][u] = r
    for lo, hi, nome in PORTES:
        m = (B['apt_mun'] >= lo) & (B['apt_mun'] < hi)
        r = assim(y[m], X4[m], mun[m], mun[m], w[m], N4)
        r.update({'municipios': int(len(set(mun[m].tolist()))), 'flavio_1t': int(B['R1'][m].sum()), 'V': float(-r['A'] * B['R1'][m].sum())})
        mm = m & U22
        r0 = assim(y[mm], X4[mm], mun[mm], mun[mm], w[mm], N4)
        r1 = assim(y[mm], np.column_stack([X4[mm], P[mm], T[mm]]), mun[mm], mun[mm], w[mm], N4 + ['P', 'T'])
        r2 = assim(y[mm], np.column_stack([X4[mm], Dd[mm], T[mm]]), mun[mm], mun[mm], w[mm], N4 + ['D', 'T'])
        r.update({'U22_A0': r0['A'], 'U22_A_com_P_T': r1['A'], 'U22_A_com_D_T': r2['A'], 'Q_P_T': float(1 - r1['A'] / r0['A']), 'Q_D_T': float(1 - r2['A'] / r0['A'])})
        des['porte'][nome] = r
    val = (B['L1'] + B['R1'] + B['O1']).astype(float)
    fl = np.where(val > 0, B['L1'] / np.maximum(val, 1), np.nan)
    for lo, hi, nome in FAIXAS:
        m = (fl >= lo) & (fl < hi)
        r = assim(y[m], X4[m], mun[m], mun[m], w[m], N4)
        r.update({'flavio_1t': int(B['R1'][m].sum()), 'V': float(-r['A'] * B['R1'][m].sum())})
        mm = m & U22
        r0 = assim(y[mm], X4[mm], mun[mm], mun[mm], w[mm], N4)
        r1 = assim(y[mm], np.column_stack([X4[mm], P[mm], T[mm]]), mun[mm], mun[mm], w[mm], N4 + ['P', 'T'])
        r2 = assim(y[mm], np.column_stack([X4[mm], Dd[mm], T[mm]]), mun[mm], mun[mm], w[mm], N4 + ['D', 'T'])
        r.update({'U22_A0': r0['A'], 'U22_A_com_P_T': r1['A'], 'U22_A_com_D_T': r2['A'], 'Q_P_T': float(1 - r1['A'] / r0['A']), 'Q_D_T': float(1 - r2['A'] / r0['A'])})
        des['faixa_forca_lula'][nome] = r
    # permutação exata da marca das UFs
    ufs = sorted(des['uf'])
    Au = np.array([des['uf'][u]['A'] for u in ufs])
    Fu = np.array([des['uf'][u]['flavio_1t'] for u in ufs], float)
    com = np.array([u in GOV[2026] for u in ufs])
    comb = np.array(list(itertools.combinations(range(27), 6)))
    tot = Au.sum()
    s6 = Au[comb].sum(1)
    st = (tot - s6) / 21 - s6 / 6
    obs = Au[~com].mean() - Au[com].mean()
    totw = (Au * Fu).sum()
    totf = Fu.sum()
    s6w = (Au * Fu)[comb].sum(1)
    f6 = Fu[comb].sum(1)
    stw = (totw - s6w) / (totf - f6) - s6w / f6
    obsw = (Au * Fu)[~com].sum() / Fu[~com].sum() - (Au * Fu)[com].sum() / Fu[com].sum()
    mk['uf_sem_2t_governador']['permutacao_exata'] = {
        'escolhas': int(len(comb)), 'media_simples_sem_menos_com': float(obs),
        'p_unilateral_simples': float((st <= obs + 1e-15).mean()), 'p_bilateral_simples': float((np.abs(st) >= abs(obs) - 1e-15).mean()),
        'media_ponderada_sem_menos_com': float(obsw),
        'p_unilateral_ponderada': float((stw <= obsw + 1e-15).mean()), 'p_bilateral_ponderada': float((np.abs(stw) >= abs(obsw) - 1e-15).mean()),
        'nota': 'unilateral = fração das escolhas com diferença igual ou mais negativa (assimetria de tamanho maior nas UFs sem governador)'}
    R['descritivo'] = des
    grava('parcial_descritivo.json', R)
    diga('descritivo por UF, porte e faixa pronto', round(time.time() - t0), 's')

    # ---------- zonas
    ordem = np.argsort(zona, kind='stable')
    zs = zona[ordem]
    cortes = np.flatnonzero(np.r_[True, zs[1:] != zs[:-1], True])
    nomes_mun = json.load(open(os.path.join(TRAB, 'nomes_municipios.json')))
    Z = []
    for a_, b_ in zip(cortes[:-1], cortes[1:]):
        ii = ordem[a_:b_]
        if len(ii) < 50:
            continue
        try:
            b, V, N, G = fe_wls(y[ii], X4[ii], mun[ii], None, w[ii])
        except Exception:
            continue
        A = b[0] - b[1]
        ep = float(np.sqrt(max(V[0, 0] + V[1, 1] - 2 * V[0, 1], 0)))
        f1 = int(B['R1'][ii].sum())
        ms = sorted(set(mun[ii].tolist()))
        Z.append({'zona': zs[a_], 'uf': zs[a_].split('|')[0], 'secoes': int(len(ii)), 'n_modelo': N, 'A': float(A), 'ep': ep,
                  'tamanho': float(-A), 'limite_conservador': float(-A - 1.645 * ep),
                  'aptos': int(B['apt'][ii].sum()), 'flavio_1t': f1, 'lula_1t': int(B['L1'][ii].sum()), 'flavio_2t': int(B['R2'][ii].sum()),
                  'lula_2t': int(B['L2'][ii].sum()), 'comp_1t': int(B['c1'][ii].sum()), 'comp_2t': int(B['c2'][ii].sum()),
                  'V': float(-A * f1), 'municipios': [nomes_mun.get(m_, m_) for m_ in ms], 'codigos_municipio': ms})
    tam0 = -A0
    top = sorted(Z, key=lambda r: -r['tamanho'])[:20]
    topc = sorted(Z, key=lambda r: -r['limite_conservador'])[:20]
    # coordenadas medianas dos locais (cadastro do TSE), só para as zonas listadas
    quer = {r['zona'] for r in top} | {r['zona'] for r in topc}
    coord = _coordenadas(quer)
    for r in top + topc:
        r['coordenada_mediana'] = coord.get(r['zona'])
    tam = np.array([r['tamanho'] for r in Z])
    epz = np.array([r['ep'] for r in Z])
    wz = np.array([r['flavio_1t'] for r in Z], float)
    des_z = {'zonas_com_50_ou_mais_secoes': len(Z), 'tamanho_nacional': float(tam0),
             'mediana_tamanho': float(np.median(tam)), 'p10': float(np.percentile(tam, 10)), 'p90': float(np.percentile(tam, 90)),
             'mediana_ep': float(np.median(epz)),
             'zonas_com_tamanho_positivo_a_2ep': int((tam - 2 * epz > 0).sum()), 'zonas_com_tamanho_negativo_a_2ep': int((tam + 2 * epz < 0).sum()),
             'top20_por_tamanho': top, 'top20_por_limite_conservador': topc,
             'top20_acima_do_nacional_pelo_limite_conservador': int(sum(1 for r in top if r['limite_conservador'] > tam0)),
             'top20_UFs': dict(collections.Counter(r['uf'] for r in top)), 'top20_conservador_UFs': dict(collections.Counter(r['uf'] for r in topc)),
             'todas': [{k2: r[k2] for k2 in ('zona', 'secoes', 'A', 'ep', 'flavio_1t', 'V')} for r in Z]}
    R['descritivo']['zonas'] = des_z
    grava('parcial_zonas.json', R)
    diga('zonas prontas', len(Z), round(time.time() - t0), 's')

    # ---------- reamostragem de municípios para Q e r
    def boot(mask, colunas, modelos_ix, nrep=999):
        g = _cod(mun[mask])
        ng = int(g.max() + 1)
        C = cruz(np.column_stack(colunas)[mask] if isinstance(colunas, list) else colunas[mask], w[mask], g, ng)
        rg = np.random.default_rng(SEMENTE)
        base_ = C.sum(0)
        est = {k2: f(base_) for k2, f in modelos_ix.items()}
        reps = {k2: np.empty(nrep) for k2 in modelos_ix}
        for r_ in range(nrep):
            cnt = rg.multinomial(ng, np.full(ng, 1.0 / ng))
            Cb = np.tensordot(cnt, C, axes=1)
            for k2, f in modelos_ix.items():
                reps[k2][r_] = f(Cb)
        return {k2: {'estimativa': float(est[k2]), 'ep': float(reps[k2].std(ddof=1)), 'ic95': [float(np.percentile(reps[k2], 2.5)), float(np.percentile(reps[k2], 97.5))]}
                for k2 in modelos_ix}
    # colunas: 0 y, 1 y_ret, 2 y_inocA, 3 y_inocB, 4 F, 5 L, 6 E, 7 BN, 8 P, 9 T, 10 D
    cols = [ys['real'], ys['retirada_2t'], ys['inocente_A'], ys['inocente_B'], F, L, E, BN, P, T, Dd]
    i0 = [4, 5, 6, 7]
    fq = {
        'A0_U22': lambda C: a_de_cruz(C, 0, i0),
        'A1_U22_P_T': lambda C: a_de_cruz(C, 0, i0 + [8, 9]),
        'Q_principal': lambda C: 1 - a_de_cruz(C, 0, i0 + [8, 9]) / a_de_cruz(C, 0, i0),
        'Q_so_P': lambda C: 1 - a_de_cruz(C, 0, i0 + [8]) / a_de_cruz(C, 0, i0),
        'Q_so_T': lambda C: 1 - a_de_cruz(C, 0, i0 + [9]) / a_de_cruz(C, 0, i0),
        'Q_versao_D': lambda C: 1 - a_de_cruz(C, 0, i0 + [10, 9]) / a_de_cruz(C, 0, i0),
        'r_retirada_principal': lambda C: (a_de_cruz(C, 1, i0 + [8, 9]) - a_de_cruz(C, 0, i0 + [8, 9])) / (a_de_cruz(C, 1, i0) - a_de_cruz(C, 0, i0)),
        'r_retirada_versao_D': lambda C: (a_de_cruz(C, 1, i0 + [10, 9]) - a_de_cruz(C, 0, i0 + [10, 9])) / (a_de_cruz(C, 1, i0) - a_de_cruz(C, 0, i0)),
        'r_inocente_A_principal': lambda C: (a_de_cruz(C, 2, i0 + [8, 9]) - a_de_cruz(C, 0, i0 + [8, 9])) / (a_de_cruz(C, 2, i0) - a_de_cruz(C, 0, i0)),
        'r_inocente_A_versao_D': lambda C: (a_de_cruz(C, 2, i0 + [10, 9]) - a_de_cruz(C, 0, i0 + [10, 9])) / (a_de_cruz(C, 2, i0) - a_de_cruz(C, 0, i0)),
        'r_inocente_B_principal': lambda C: (a_de_cruz(C, 3, i0 + [8, 9]) - a_de_cruz(C, 0, i0 + [8, 9])) / (a_de_cruz(C, 3, i0) - a_de_cruz(C, 0, i0)),
        'r_inocente_B_versao_D': lambda C: (a_de_cruz(C, 3, i0 + [10, 9]) - a_de_cruz(C, 0, i0 + [10, 9])) / (a_de_cruz(C, 3, i0) - a_de_cruz(C, 0, i0)),
    }
    bt = boot(U22, cols, fq)
    fu = {'A0_U': lambda C: a_de_cruz(C, 0, i0),
          'Q_so_P_em_U': lambda C: 1 - a_de_cruz(C, 0, i0 + [8]) / a_de_cruz(C, 0, i0),
          'Q_so_D_em_U': lambda C: 1 - a_de_cruz(C, 0, i0 + [10]) / a_de_cruz(C, 0, i0)}
    bt.update(boot(U, cols, fu))
    R['reamostragem_municipios'] = {'replicas': 999, 'semente': SEMENTE, 'resultados': bt}
    diga('reamostragem', {k2: (round(v['estimativa'], 4), round(v['ep'], 4)) for k2, v in bt.items()})
    grava('parcial_boot.json', R)

    # ---------- sensibilidades
    sens = {}
    um = np.ones(n)
    s0 = assim(y[U22], X4[U22], mun[U22], mun[U22], um[U22], N4)
    s1 = assim(y[U22], np.column_stack([X4[U22], P[U22], T[U22]]), mun[U22], mun[U22], um[U22], N4 + ['P', 'T'])
    s2 = assim(y[U22], np.column_stack([X4[U22], Dd[U22], T[U22]]), mun[U22], mun[U22], um[U22], N4 + ['D', 'T'])
    sens['sem_peso'] = {'A0_em_U': assim(y, X4, mun, mun, um, N4)['A'], 'A0_em_U22': s0['A'], 'A_com_P_T': s1['A'], 'A_com_D_T': s2['A'],
                        'Q_P_T': float(1 - s1['A'] / s0['A']), 'Q_D_T': float(1 - s2['A'] / s0['A'])}
    local = np.array([f'{m_}|{z_.split("|")[1]}|{l_}' for m_, z_, l_ in zip(mun.tolist(), zona.tolist(), B['loc'].tolist())])
    s0 = assim(y[U22], X4[U22], local[U22], mun[U22], w[U22], N4)
    s1 = assim(y[U22], np.column_stack([X4[U22], P[U22], T[U22]]), local[U22], mun[U22], w[U22], N4 + ['P', 'T'])
    s2 = assim(y[U22], np.column_stack([X4[U22], Dd[U22], T[U22]]), local[U22], mun[U22], w[U22], N4 + ['D', 'T'])
    sl = assim(y, X4, local, mun, w, N4)
    sens['efeito_fixo_de_local'] = {'A0_em_U': sl['A'], 'ep_A0_em_U': sl['ep_A'], 'n_em_U': sl['n'], 'A0_em_U22': s0['A'], 'A_com_P_T': s1['A'], 'A_com_D_T': s2['A'],
                                    'Q_P_T': float(1 - s1['A'] / s0['A']), 'Q_D_T': float(1 - s2['A'] / s0['A'])}
    perto = U22 & (np.abs(B['apt_2022'] / apt - 1) <= 0.20)
    s0 = assim(y[perto], X4[perto], mun[perto], mun[perto], w[perto], N4)
    s1 = assim(y[perto], np.column_stack([X4[perto], P[perto], T[perto]]), mun[perto], mun[perto], w[perto], N4 + ['P', 'T'])
    s2 = assim(y[perto], np.column_stack([X4[perto], Dd[perto], T[perto]]), mun[perto], mun[perto], w[perto], N4 + ['D', 'T'])
    sens['ligacao_2022_aptos_a_20pct'] = {'secoes': int(perto.sum()), 'A0': s0['A'], 'A_com_P_T': s1['A'], 'A_com_D_T': s2['A'],
                                          'Q_P_T': float(1 - s1['A'] / s0['A']), 'Q_D_T': float(1 - s2['A'] / s0['A'])}
    sens['P_com_legenda'] = {'Q_M0+Pleg+T_em_U22': Q['P_com_legenda_M0+Pleg+T_em_U22'], 'Q_so_Pleg_em_U': q(ctl['U']['M0+Pleg']['A'], ctl['U']['M0']['A'])}
    sens['fora_de_U22'] = {'secoes': int((U & ~U22).sum()), 'A0': assim(y[U & ~U22], X4[U & ~U22], mun[U & ~U22], mun[U & ~U22], w[U & ~U22], N4)['A']}
    R['sensibilidades'] = sens
    grava('parcial_sens.json', R)

    # ---------- outros anos (E3)
    oa = {'2026': {'A0': m0['A'], 'ep_A0': m0['ep_A'], 'coef': m0['coef'], 'secoes': m0['n'],
                   'marca_pequenos_D': mk['municipio_pequeno_20mil']['D'], 'marca_pequenos_z': mk['municipio_pequeno_20mil']['z'],
                   'marca_uf_D': mk['uf_sem_2t_governador']['D'], 'marca_uf_z': mk['uf_sem_2t_governador']['z'],
                   'A0_onde_liga_com_a_eleicao_anterior': ctl['U22']['M0']['A'], 'A_com_T': ctl['U22']['M0+T']['A'], 'Q_so_T': Q['so_T_em_U22'],
                   'coef_T': ctl['U22']['M0+T']['coef']['T'], 'ufs_com_2t_governador': GOV[2026]}}
    for ano in (2022, 2018, 2014):
        Bo = _le_base(ano)
        ko = Bo['chaves'].tolist()
        muno = _mun_de(ko)
        ufo = _uf_de(ko)
        ao = Bo['apt'].astype(float)
        yo = (Bo['c2'] - Bo['c1']) / ao
        Xo = np.column_stack([Bo['R1'] / ao, Bo['L1'] / ao, Bo['O1'] / ao, (Bo['B1'] + Bo['N1']) / ao])
        r0 = assim(yo, Xo, muno, muno, ao, ['R', 'L', 'E', 'BN'])
        peq = Bo['apt_mun'] < PEQUENO
        sg = ~np.isin(ufo, GOV[ano])
        m1 = _marcas(yo, Xo, muno, ao, peq, ['pequenos', 'demais'], r0['A'])
        m2 = _marcas(yo, Xo, muno, ao, sg, ['sem', 'com'], r0['A'])
        item = {'A0': r0['A'], 'ep_A0': r0['ep_A'], 'coef': r0['coef'], 'secoes': r0['n'], 'adversario_1t': int(Bo['R1'].sum()), 'pt_1t': int(Bo['L1'].sum()),
                'marca_pequenos_D': m1['D'], 'marca_pequenos_ep': m1['ep_D'], 'marca_pequenos_z': m1['z'], 'marca_pequenos_mesmo_sinal_de_A0': m1['mesmo_sinal_de_A0'],
                'marca_uf_D': m2['D'], 'marca_uf_ep': m2['ep_D'], 'marca_uf_z': m2['z'], 'marca_uf_mesmo_sinal_de_A0': m2['mesmo_sinal_de_A0'],
                'ufs_com_2t_governador': GOV[ano]}
        ant = {2022: 2018, 2018: 2014}.get(ano)
        if ant:
            lg = np.load(os.path.join(TRAB, f'liga_{ano}_{ant}.npz'))
            ok = lg['apt_ant'] > 0
            To = np.where(ok, Bo['c1'] / ao - lg['c1_ant'] / np.maximum(lg['apt_ant'], 1), 0.0)
            q0 = assim(yo[ok], Xo[ok], muno[ok], muno[ok], ao[ok], ['R', 'L', 'E', 'BN'])
            q1 = assim(yo[ok], np.column_stack([Xo[ok], To[ok]]), muno[ok], muno[ok], ao[ok], ['R', 'L', 'E', 'BN', 'T'])
            item.update({'liga_com': ant, 'secoes_ligadas': int(ok.sum()), 'A0_onde_liga_com_a_eleicao_anterior': q0['A'], 'A_com_T': q1['A'],
                         'Q_so_T': float(1 - q1['A'] / q0['A']), 'coef_T': q1['coef']['T']})
        oa[str(ano)] = item
        del Bo
    R['outros_anos'] = oa
    grava('parcial_outros_anos.json', R)
    diga('outros anos', {a_: (round(v['A0'], 4), round(v['marca_pequenos_z'], 1), round(v['marca_uf_z'], 1)) for a_, v in oa.items()})

    # ---------- votos de margem
    f1U = float(B['R1'].sum())
    f1U22 = float(B['R1'][U22].sum())
    a0_22 = ctl['U22']['M0']['A']
    a1_22 = ctl['U22']['M0+P+T']['A']
    a1d_22 = ctl['U22']['M0+D+T']['A']
    R['votos'] = {'margem_oficial': MARGEM, 'flavio_1t_em_U': f1U, 'flavio_1t_em_U22': f1U22,
                  'V0_em_U': -A0 * f1U, 'ep_V0_em_U': m0['ep_A'] * f1U, 'V0_em_U_sobre_margem': -A0 * f1U / MARGEM,
                  'V0_em_U22': -a0_22 * f1U22, 'V1_em_U22_com_P_T': -a1_22 * f1U22, 'V1_em_U22_com_D_T': -a1d_22 * f1U22,
                  'absorvido_pelos_controles_letra': (-a0_22 + a1_22) * f1U22, 'absorvido_pelos_controles_versao_D': (-a0_22 + a1d_22) * f1U22,
                  'retirada_plantada_em_votos_U': float(xF.sum()),
                  'nota': 'V = menos A vezes votos de Flávio no 1º turno; cada eleitor vale 1 voto de margem'}

    # ---------- leitura e veredito pela letra
    Qp = Q['principal_M0+P+T_em_U22']
    icq = bt['Q_principal']['ic95']
    marca1 = mk['municipio_pequeno_20mil']['aparece']
    marca2 = mk['uf_sem_2t_governador']['aparece']
    tem_objeto = bool(m0['A'] < 0 and abs(m0['z_A']) > 3)
    r_ret = cal['retirada_2t']['U22: M0+P+T (principal)']['r']
    r_inA = cal['inocente_A']['U22: M0+P+T (principal)']['r']
    r_inB = cal['inocente_B']['U22: M0+P+T (principal)']['r']
    if not tem_objeto:
        leitura, ver = 'sem objeto (não há assimetria contra Flávio a mais de 3 erros-padrão)', 'SEM OBJETO'
    elif Qp >= 0.5 and marca1 and marca2:
        leitura, ver = 'explicada pela mobilização', 'SEM SINAL'
    elif Qp < 0.2:
        leitura, ver = 'não explicada', 'SINAL'
    else:
        leitura, ver = 'entre os dois', 'INCONCLUSIVO'
    cal_ok = bool(r_ret is not None and r_ret >= 0.80)
    R['veredito'] = {
        'Q_principal': Qp, 'Q_ic95_reamostragem': icq, 'ic_cruza_0.20': bool(icq[0] < 0.2 < icq[1]), 'ic_cruza_0.50': bool(icq[0] < 0.5 < icq[1]),
        'marca_ii_municipios_pequenos': marca1, 'marca_ii_ufs_sem_governador': marca2,
        'leitura_pela_letra': leitura, 'veredito_pela_letra_antes_da_calibracao': ver,
        'calibracao_retirada_r': r_ret, 'calibracao_passa_(r>=0.80)': cal_ok,
        'inocente_A_r': r_inA, 'inocente_B_r': r_inB,
        'distingue_inocente_A_(r<=0.50)': bool(r_inA is not None and r_inA <= 0.5),
        'distingue_inocente_B_(r<=0.50)': bool(r_inB is not None and r_inB <= 0.5),
        'veredito_pela_letra': ver if cal_ok else 'SEM PODER',
        'versao_D': {'Q': Q['versao_D_M0+D+T_em_U22'], 'ic95': bt['Q_versao_D']['ic95'],
                     'r_retirada': cal['retirada_2t']['U22: M0+D+T (versão D)']['r'],
                     'r_inocente_A': cal['inocente_A']['U22: M0+D+T (versão D)']['r'],
                     'r_inocente_B': cal['inocente_B']['U22: M0+D+T (versão D)']['r']}}
    R['tempo_s'] = round(time.time() - t0)
    with open(SAIDA_JSON + '.tmp', 'w') as f:
        json.dump(R, f, ensure_ascii=False, indent=1)
    os.replace(SAIDA_JSON + '.tmp', SAIDA_JSON)
    diga('veredito', R['veredito'])
    diga('gravado', SAIDA_JSON)


def explorar():
    """EXPLORATÓRIO: tudo aqui foi decidido DEPOIS de ver o resultado de 'rodar'. Não muda veredito."""
    t0 = time.time()
    R = json.load(open(SAIDA_JSON))
    X = {'aviso': 'Bloco feito depois de ver os resultados registrados; não decide veredito.'}
    PTF = [(0.0, 0.35, 'menos de 35%'), (0.35, 0.50, '35 a 50%'), (0.50, 0.65, '50 a 65%'), (0.65, 1.01, '65% ou mais')]
    por_ano = {}
    guard = {}
    for ano in (2026, 2022, 2018, 2014):
        B = _le_base(ano)
        ks = B['chaves'].tolist()
        mun = _mun_de(ks)
        uf = _uf_de(ks)
        zona = _zona_de(ks)
        apt = B['apt'].astype(float)
        y = (B['c2'] - B['c1']) / apt
        X4 = np.column_stack([B['R1'] / apt, B['L1'] / apt, B['O1'] / apt, (B['B1'] + B['N1']) / apt])
        N4 = ['F', 'L', 'E', 'BN']
        f1 = float(B['R1'].sum())
        local = np.array([f'{m_}|{z_.split("|")[1]}|{l_}' for m_, z_, l_ in zip(mun.tolist(), zona.tolist(), B['loc'].tolist())])
        item = {'adversario_do_PT_1t_no_universo': f1, 'efeito_fixo': {}}
        for nome, fe in (('nenhum (constante)', np.zeros(len(ks), dtype=int)), ('UF', uf), ('zona', zona), ('município (registro)', mun), ('local de votação', local)):
            r = assim(y, X4, fe, mun, apt, N4)
            item['efeito_fixo'][nome] = {'A': r['A'], 'ep_A': r['ep_A'], 'n': r['n'], 'V': -r['A'] * f1, 'bF': r['coef']['F'], 'bL': r['coef']['L']}
        item['porte'] = {}
        for lo, hi, nome in PORTES:
            m = (B['apt_mun'] >= lo) & (B['apt_mun'] < hi)
            r = assim(y[m], X4[m], mun[m], mun[m], apt[m], N4)
            item['porte'][nome] = {'A': r['A'], 'ep_A': r['ep_A'], 'n': r['n']}
        peq = B['apt_mun'] < PEQUENO
        for nome, m in (('pequenos (menos de 20 mil)', peq), ('demais', ~peq)):
            r = assim(y[m], X4[m], mun[m], mun[m], apt[m], N4)
            item['porte'][nome] = {'A': r['A'], 'ep_A': r['ep_A'], 'n': r['n']}
        val = (B['L1'] + B['R1'] + B['O1']).astype(float)
        fl = np.where(val > 0, B['L1'] / np.maximum(val, 1), np.nan)
        item['faixa_forca_PT'] = {}
        for lo, hi, nome in PTF:
            m = (fl >= lo) & (fl < hi)
            r = assim(y[m], X4[m], mun[m], mun[m], apt[m], N4)
            r2 = assim(y[m], X4[m], local[m], mun[m], apt[m], N4)
            item['faixa_forca_PT'][nome] = {'A': r['A'], 'ep_A': r['ep_A'], 'n': r['n'], 'A_efeito_fixo_local': r2['A'], 'ep_A_efeito_fixo_local': r2['ep_A'],
                                            'adversario_1t': int(B['R1'][m].sum())}
        item['uf'] = {}
        for u in sorted(set(uf.tolist())):
            m = uf == u
            nm = len(set(mun[m].tolist()))
            r = assim(y[m], X4[m], mun[m], mun[m] if nm >= 10 else zona[m], apt[m], N4)
            item['uf'][u] = {'A': r['A'], 'ep_A': r['ep_A']}
        por_ano[str(ano)] = item
        if ano == 2026:
            guard = {'B': B, 'mun': mun, 'uf': uf, 'zona': zona, 'apt': apt, 'y': y, 'X4': X4, 'local': local, 'ks': ks}
        diga('exploratório', ano, {k: round(v['A'], 4) for k, v in item['efeito_fixo'].items()})
    X['por_ano'] = por_ano
    X['uf_2026_menos_2022'] = {u: por_ano['2026']['uf'][u]['A'] - por_ano['2022']['uf'][u]['A'] for u in por_ano['2026']['uf']}
    X['equivalente_em_retirada_uniforme'] = {
        'nota': 'retirada uniforme de t% dos votos de Flávio desloca A em cerca de -t (plantio: -0,0363 para 3,6%). Equivalente = (régua menos A de 2026) / 1,008.',
        'regua_zero': -por_ano['2026']['efeito_fixo']['município (registro)']['A'] / 1.008,
        'regua_2022': (por_ano['2022']['efeito_fixo']['município (registro)']['A'] - por_ano['2026']['efeito_fixo']['município (registro)']['A']) / 1.008,
        'regua_2018': (por_ano['2018']['efeito_fixo']['município (registro)']['A'] - por_ano['2026']['efeito_fixo']['município (registro)']['A']) / 1.008,
        'regua_2014': (por_ano['2014']['efeito_fixo']['município (registro)']['A'] - por_ano['2026']['efeito_fixo']['município (registro)']['A']) / 1.008}
    # 2026: controles com efeito fixo de local e controle simétrico, com reamostragem
    g = guard
    B = g['B']
    mun, apt, y, X4, local = g['mun'], g['apt'], g['y'], g['X4'], g['local']
    n = len(apt)
    F = X4[:, 0]
    L = X4[:, 1]
    D22 = B['df_nom22'].astype(float)
    D13 = B['df_nom13'].astype(float)
    P = D22 / apt - F
    Dd = D22 / apt
    P13 = D13 / apt - L
    D13d = D13 / apt
    liga = B['apt_2022'] > 0
    T = np.where(liga, B['c1'] / apt - B['c1_2022'] / np.maximum(B['apt_2022'], 1), 0.0)
    U22 = liga
    N4 = ['F', 'L', 'E', 'BN']
    sim = {}
    for nome, cols, nomes in (('M0', [], []), ('M0+D+T', [Dd, T], ['D', 'T']), ('M0+D+D13+T', [Dd, D13d, T], ['D', 'D13', 'T']),
                              ('M0+P+P13+T', [P, P13, T], ['P', 'P13', 'T']), ('M0+P+T', [P, T], ['P', 'T'])):
        r = assim(y[U22], np.column_stack([X4[U22]] + [c[U22] for c in cols]), mun[U22], mun[U22], apt[U22], N4 + nomes)
        r2 = assim(y[U22], np.column_stack([X4[U22]] + [c[U22] for c in cols]), local[U22], mun[U22], apt[U22], N4 + nomes)
        sim[nome] = {'A': r['A'], 'ep_A': r['ep_A'], 'coef': r['coef'], 'ep': r['ep'], 'A_efeito_fixo_local': r2['A'], 'ep_A_efeito_fixo_local': r2['ep_A'],
                     'coef_efeito_fixo_local': r2['coef'], 'ep_efeito_fixo_local': r2['ep']}
    for nome in list(sim):
        if nome != 'M0':
            sim[nome]['Q'] = 1 - sim[nome]['A'] / sim['M0']['A']
            sim[nome]['Q_efeito_fixo_local'] = 1 - sim[nome]['A_efeito_fixo_local'] / sim['M0']['A_efeito_fixo_local']
    # reamostragem de municípios: controle dos dois lados
    gm = _cod(mun[U22])
    ng = int(gm.max() + 1)
    C = cruz(np.column_stack([y, F, L, X4[:, 2], X4[:, 3], P, P13, T, Dd, D13d])[U22], apt[U22], gm, ng)
    rg = np.random.default_rng(SEMENTE)
    i0 = [1, 2, 3, 4]
    fs = {'Q_P_P13_T': lambda c: 1 - a_de_cruz(c, 0, i0 + [5, 6, 7]) / a_de_cruz(c, 0, i0),
          'Q_D_D13_T': lambda c: 1 - a_de_cruz(c, 0, i0 + [8, 9, 7]) / a_de_cruz(c, 0, i0)}
    reps = {k: np.empty(999) for k in fs}
    for r_ in range(999):
        Cb = np.tensordot(rg.multinomial(ng, np.full(ng, 1.0 / ng)), C, axes=1)
        for k, f in fs.items():
            reps[k][r_] = f(Cb)
    Cs = C.sum(0)
    sim['reamostragem'] = {k: {'estimativa': float(f(Cs)), 'ep': float(reps[k].std(ddof=1)), 'ic95': [float(np.percentile(reps[k], 2.5)), float(np.percentile(reps[k], 97.5))]}
                           for k, f in fs.items()}
    X['controle_dos_dois_lados_2026'] = sim
    # zonas: as 20 de maior V (votos) com tamanho positivo a 2 erros-padrão
    Zt = R['descritivo']['zonas']['todas']
    nomes_mun = json.load(open(os.path.join(TRAB, 'nomes_municipios.json')))
    zmun = collections.defaultdict(set)
    for k_, m_ in zip(g['zona'].tolist(), mun.tolist()):
        zmun[k_].add(m_)
    sig = [z for z in Zt if -z['A'] - 2 * z['ep'] > 0]
    neg = [z for z in Zt if -z['A'] + 2 * z['ep'] < 0]
    topv = sorted(sig, key=lambda z: -z['V'])[:20]
    coord = _coordenadas({z['zona'] for z in topv})
    X['zonas_por_votos'] = {
        'zonas_com_tamanho_positivo_a_2ep': len(sig), 'V_somado_nessas': float(sum(z['V'] for z in sig)),
        'zonas_com_tamanho_negativo_a_2ep': len(neg), 'V_somado_nas_negativas': float(sum(z['V'] for z in neg)),
        'V_somado_em_todas_as_zonas_com_50_secoes': float(sum(z['V'] for z in Zt)),
        'top20_por_V': [{'zona': z['zona'], 'secoes': z['secoes'], 'tamanho': -z['A'], 'ep': z['ep'], 'flavio_1t': z['flavio_1t'], 'V': z['V'],
                         'municipios': [nomes_mun.get(m_, m_) for m_ in sorted(zmun[z['zona']])], 'coordenada_mediana': coord.get(z['zona'])} for z in topv],
        'top20_registrado_V_somado': float(sum(z['V'] for z in R['descritivo']['zonas']['top20_por_tamanho']))}
    # soma dos V por UF e total de Flávio no 1º turno em todas as seções das 27 UFs
    X['V_somado_por_UF'] = float(sum(v['V'] for v in R['descritivo']['uf'].values()))
    X['V_positivos_por_UF'] = float(sum(v['V'] for v in R['descritivo']['uf'].values() if v['V'] > 0))
    S = _carrega(2026)
    f_all = sum(v['1']['R'] for k, v in S.items() if not k.startswith('ZZ|') and '1' in v)
    f2_all = sum(v['2']['R'] for k, v in S.items() if not k.startswith('ZZ|') and '2' in v)
    del S
    A0 = R['modelo0']['A']
    Aloc = por_ano['2026']['efeito_fixo']['local de votação']['A']
    X['escala_27_UFs'] = {'flavio_1t_todas_as_secoes_27_UFs': int(f_all), 'flavio_2t_todas_as_secoes_27_UFs': int(f2_all),
                          'V0_registro_escalado': -A0 * f_all, 'V0_registro_escalado_sobre_margem': -A0 * f_all / MARGEM,
                          'V_efeito_fixo_local_escalado': -Aloc * f_all, 'V_efeito_fixo_local_escalado_sobre_margem': -Aloc * f_all / MARGEM,
                          'nota': 'extrapolação: aplica a assimetria do universo aos votos de Flávio das seções fora dele (aptos diferentes entre os turnos)'}
    R['exploratorio'] = X
    with open(SAIDA_JSON + '.tmp', 'w') as f:
        json.dump(R, f, ensure_ascii=False, indent=1)
    os.replace(SAIDA_JSON + '.tmp', SAIDA_JSON)
    grava('parcial_exploratorio.json', X)
    diga('exploratório gravado', round(time.time() - t0), 's')


def _extrai_partidos_zip(zp):
    """EXPLORATÓRIO: votos nominais de deputado federal por partido (coluna = número do partido) em cada seção."""
    z = zipfile.ZipFile(zp)
    nome = [n for n in z.namelist() if n.lower().endswith('.csv')][0]
    pos = {}
    M = np.zeros((4096, 100), dtype=np.int32)
    with z.open(nome) as fh:
        bf = io.BufferedReader(fh, 1 << 24)
        bf.readline()
        for l in bf:
            if b';6;"Deputado Federal";' not in l:
                continue
            p, _ = _campos(l)
            if len(p) != NCOL or p[I_CARGO].strip(b'"') != b'6' or p[I_TV].strip(b'"') != b'1':
                continue
            uf_ = p[I_UF].strip(b'"').decode()
            mun_ = int(p[I_MUN].strip(b'"'))
            zona_ = int(p[I_ZONA].strip(b'"'))
            sec_ = int(p[I_SEC].strip(b'"'))
            k = f"{uf_}|{mun_}|{zona_}|{sec_}"
            i = pos.get(k)
            if i is None:
                i = pos[k] = len(pos)
                if i >= M.shape[0]:
                    M = np.vstack([M, np.zeros_like(M)])
            M[i, int(p[I_PART].strip(b'"'))] += int(p[I_Q].strip(b'"'))
    ks = sorted(pos, key=pos.get)
    return os.path.basename(zp), ks, M[:len(ks)]


def extrair_partidos():
    from multiprocessing import Pool
    zs = sorted(glob.glob(ZIPS1 + '/*.zip'), key=lambda p: -os.path.getsize(p))
    chaves = []
    blocos = []
    with Pool(4) as pool:
        for nome, ks, M in pool.imap_unordered(_extrai_partidos_zip, zs):
            chaves += ks
            blocos.append(M)
            diga(nome, len(ks))
    M = np.vstack(blocos)
    np.savez_compressed(os.path.join(TRAB, 'depfed_partidos_1t.npz'), chaves=np.array(chaves), M=M)
    diga('partidos gravado', M.shape, int(M.sum()), {int(j): int(M[:, j].sum()) for j in np.flatnonzero(M.sum(0))})


def explorar2():
    """EXPLORATÓRIO (depois de ver o resultado): o puxão medido pelos candidatos a deputado federal de TODOS os partidos.
    Modelo 0 mais a fatia sobre aptos dos votos nominais de cada partido com 1% ou mais dos nominais do país, os demais
    somados e a legenda; categoria omitida = branco e nulo de deputado. Versão D (fatias como regressores)."""
    R = json.load(open(SAIDA_JSON))
    B = _le_base(2026)
    ks = B['chaves'].tolist()
    d = np.load(os.path.join(TRAB, 'depfed_partidos_1t.npz'))
    pos = {k: i for i, k in enumerate(d['chaves'].tolist())}
    idx = np.array([pos[k] for k in ks])
    M = d['M'][idx].astype(float)
    assert np.all(M.sum(1) == B['df_nominais']), 'nominais por partido diferem da primeira extração'
    assert np.all(M[:, 22] == B['df_nom22']) and np.all(M[:, 13] == B['df_nom13'])
    tot = M.sum(0)
    grandes = [int(j) for j in np.flatnonzero(tot >= 0.01 * tot.sum())]
    outros = M[:, [j for j in range(100) if j not in grandes]].sum(1)
    mun = _mun_de(ks)
    zona = _zona_de(ks)
    apt = B['apt'].astype(float)
    y = (B['c2'] - B['c1']) / apt
    X4 = np.column_stack([B['R1'] / apt, B['L1'] / apt, B['O1'] / apt, (B['B1'] + B['N1']) / apt])
    N4 = ['F', 'L', 'E', 'BN']
    local = np.array([f'{m_}|{z_.split("|")[1]}|{l_}' for m_, z_, l_ in zip(mun.tolist(), zona.tolist(), B['loc'].tolist())])
    liga = B['apt_2022'] > 0
    T = np.where(liga, B['c1'] / apt - B['c1_2022'] / np.maximum(B['apt_2022'], 1), 0.0)
    leg = (B['df_legendas']) / apt
    cols = [M[:, j] / apt for j in grandes] + [outros / apt, leg]
    nomes = [f'dep_{j}' for j in grandes] + ['dep_outros', 'dep_legenda']
    out = {'partidos_com_1pct_ou_mais_dos_nominais': grandes, 'nominais_por_partido_no_universo': {str(j): int(tot[j]) for j in grandes},
           'nota': 'coeficiente de dep_NN = variação do comparecimento por eleitor que votou em candidato a deputado federal do partido NN, em relação a quem votou branco ou nulo para deputado, com os votos de presidente fixos'}
    for nome_u, mask in (('U', np.ones(len(ks), bool)), ('U22', liga)):
        for nome_fe, fe in (('município', mun), ('local', local)):
            r0 = assim(y[mask], X4[mask], fe[mask], mun[mask], apt[mask], N4)
            ex = [c[mask] for c in cols] + ([T[mask]] if nome_u == 'U22' else [])
            nx = nomes + (['T'] if nome_u == 'U22' else [])
            r1 = assim(y[mask], np.column_stack([X4[mask]] + ex), fe[mask], mun[mask], apt[mask], N4 + nx)
            # par típico: eleitor de Flávio que votou em deputado do 22 contra eleitor de Lula que votou em deputado do 13
            bb, VV, _, _ = fe_wls(y[mask], np.column_stack([X4[mask]] + ex), fe[mask], mun[mask], apt[mask])
            cv = np.zeros(len(bb))
            cv[0], cv[1] = 1, -1
            cv[4 + nomes.index('dep_22')] = 1
            cv[4 + nomes.index('dep_13')] = -1
            out[f'{nome_u}, efeito fixo de {nome_fe}'] = {'A0': r0['A'], 'ep_A0': r0['ep_A'], 'A_com_todos_os_partidos': r1['A'], 'ep_A': r1['ep_A'],
                                                         'Q': 1 - r1['A'] / r0['A'], 'coef': r1['coef'], 'ep': r1['ep'], 'n': r1['n'],
                                                         'A_par_tipico_F_com_dep22_contra_L_com_dep13': float(cv @ bb), 'ep_par_tipico': float(np.sqrt(cv @ VV @ cv)),
                                                         'Q_par_tipico': float(1 - (cv @ bb) / r0['A'])}
    # reamostragem de municípios do Q em U22 (efeito fixo de município)
    g = _cod(mun[liga])
    ng = int(g.max() + 1)
    Z = np.column_stack([y, X4] + cols + [T])[liga]
    C = cruz(Z, apt[liga], g, ng)
    i0 = [1, 2, 3, 4]
    it = i0 + list(range(5, Z.shape[1]))
    rg = np.random.default_rng(SEMENTE)
    reps = np.empty(999)
    for r_ in range(999):
        Cb = np.tensordot(rg.multinomial(ng, np.full(ng, 1.0 / ng)), C, axes=1)
        reps[r_] = 1 - a_de_cruz(Cb, 0, it) / a_de_cruz(Cb, 0, i0)
    Cs = C.sum(0)
    out['Q_U22_reamostragem'] = {'estimativa': float(1 - a_de_cruz(Cs, 0, it) / a_de_cruz(Cs, 0, i0)), 'ep': float(reps.std(ddof=1)),
                                 'ic95': [float(np.percentile(reps, 2.5)), float(np.percentile(reps, 97.5))]}
    # plantio inocente A e retirada nesse modelo (o modelo engole o puxão do 22 e preserva a retirada?)
    rng = np.random.default_rng(SEMENTE)
    xF = rng.binomial(B['R2'], TAXA).astype(float)
    rng.binomial(B['R1'], TAXA)
    rng.binomial(B['L2'], TAXA)
    tA = xF.sum() / B['df_nom22'].sum()
    xA = rng.binomial(B['df_nom22'], min(tA, 1.0)).astype(float)
    mask = liga
    Xc = np.column_stack([X4[mask]] + [c[mask] for c in cols] + [T[mask]])
    nx = N4 + nomes + ['T']
    a0 = assim(y[mask], X4[mask], mun[mask], mun[mask], apt[mask], N4)['A']
    a1 = assim(y[mask], Xc, mun[mask], mun[mask], apt[mask], nx)['A']
    for npl, x in (('retirada_2t', xF), ('inocente_A', xA)):
        yv = y - x / apt
        b0 = assim(yv[mask], X4[mask], mun[mask], mun[mask], apt[mask], N4)['A']
        b1 = assim(yv[mask], Xc, mun[mask], mun[mask], apt[mask], nx)['A']
        out[f'calibracao_{npl}'] = {'dA0': b0 - a0, 'dA1': b1 - a1, 'r': (b1 - a1) / (b0 - a0)}
    R['exploratorio']['puxao_de_todos_os_partidos'] = out
    with open(SAIDA_JSON + '.tmp', 'w') as f:
        json.dump(R, f, ensure_ascii=False, indent=1)
    os.replace(SAIDA_JSON + '.tmp', SAIDA_JSON)
    grava('parcial_exploratorio2.json', out)
    diga({k: (round(v['A0'], 4), round(v['A_com_todos_os_partidos'], 4), round(v['Q'], 3)) for k, v in out.items() if isinstance(v, dict) and 'A0' in v})
    diga(out['Q_U22_reamostragem'], out['calibracao_retirada_2t'], out['calibracao_inocente_A'])
    u = out['U22, efeito fixo de município']
    diga({k: (round(v, 4), round(u['ep'][k], 4)) for k, v in u['coef'].items()})


# ---------------------------------------------------------------- texto
def fz(x, d=4, sinal=True):
    if x is None or (isinstance(x, float) and x != x):
        return 'n/d'
    t = f'{x:+.{d}f}' if sinal else f'{x:.{d}f}'
    return t.replace('.', ',')


def fi(x):
    return f'{int(round(x)):,}'.replace(',', '.')


def pc(x, d=1, sinal=False):
    return fz(100 * x, d, sinal) + '%'


DESVIOS = [
    'Parametrização do puxão (D4): a conta principal usa P como escrito no registro (D22/aptos menos F). Ao lado, a versão D (D22/aptos como regressor), que dá o mesmo ajuste e outro coeficiente de Flávio. O aviso foi escrito antes de rodar; o plantio inocente mostrou que só a versão D separa mobilização de retirada. O veredito pela letra é o de P.',
    'A queda principal Q compara o modelo com P e T contra o modelo 0 nas mesmas seções que ligam com 2022 (409.088 de 442.491); o registro não diz em que amostra comparar. Erro de Q por reamostragem de municípios (999 réplicas).',
    'P usa só votos nominais dos candidatos do 22 (o registro diz "candidatos"); com legenda, ao lado. T liga pela chave UF, município, zona e seção; ao lado, só seções com aptos de 2022 a 20% dos de 2026.',
    'Município pequeno = menos de 20.000 aptos (o registro não fixa corte); 10 e 50 mil ao lado. Marcas (ii) por modelo 0 separado em cada grupo e diferença a mais de 3 erros-padrão no sentido de A0; para as UFs, permutação exata ao lado.',
    'Tradução da leitura em veredito: "explicada" = SEM SINAL; "não explicada" = SINAL no sentido estreito (a marca inocente não apareceu); o resto = INCONCLUSIVO; SEM PODER se a retirada plantada for engolida pelos controles (razão abaixo de 0,80).',
    'Retirada plantada sobre os votos de Flávio do 2º turno, por sorteio binomial (semente 20261110); "tanto quanto" = razão de 0,80 ou mais. Versões sem sorteio e sobre o 1º turno ao lado.',
    'Plantios inocentes A (puxão do deputado do 22) e B (comparecimento extra contra 2022) não estão no registro; são exigência desta onda. Limiar de "distingue": retirada com razão de 0,80 ou mais e inocente com 0,50 ou menos.',
    'Espelhos: puxão do 13 como controle, retirada plantada de Lula, e os anos de 2014, 2018 e 2022 (UFs de governador de cada ano; 2014 pela lista publicada no R27_A1). O controle P não existe para outros anos.',
    'Descritivo por zona: só zonas com 50 ou mais seções, erro robusto por seção, lista pelo tamanho com o limite conservador ao lado; coordenada = mediana dos locais no cadastro do TSE. No DF (um município) o erro é por zona.',
    'O que eu conhecia antes: o texto dos resultados da Onda A. Não li N1, B2 nem B3.',
    'EXPLORATÓRIO, depois de ver o resultado (item 10): efeito fixo em outros níveis, faixas e portes por ano, diferença contra 2022 por UF, controle dos dois puxões, deputado de todos os partidos (segunda passada no bweb), zonas por votos, extrapolação às seções fora do universo.',
    'Nenhum limiar do registro foi mudado.',
]


def texto():
    import textwrap
    R = json.load(open(SAIDA_JSON))
    R['desvios'] = DESVIOS
    U = R['universo']; m0 = R['modelo0']; C = R['controles']['modelos']; Q = R['controles']['Q']; bt = R['reamostragem_municipios']['resultados']
    mk = R['marcas_ii']; cal = R['calibracao']; pl = R['plantios']; V = R['votos']; des = R['descritivo']; sen = R['sensibilidades']
    oa = R['outros_anos']; ver = R['veredito']; X = R['exploratorio']; xa = X['por_ano']
    L = []

    def par(t):
        ind = len(t) - len(t.lstrip(' '))
        for ln in textwrap.wrap(t.strip(), 116 - ind):
            L.append(' ' * ind + ln)

    def item(t, ind=2):
        ls = textwrap.wrap(t, 116 - ind - 2)
        L.append(' ' * ind + '- ' + ls[0])
        for ln in ls[1:]:
            L.append(' ' * (ind + 2) + ln)

    P1 = 'U22: M0+P+T (principal)'
    D1 = 'U22: M0+D+T (versão D)'
    a0, a22, a1, ad = m0['A'], C['U22']['M0']['A'], C['U22']['M0+P+T']['A'], C['U22']['M0+D+T']['A']
    peq, guf = mk['municipio_pequeno_20mil'], mk['uf_sem_2t_governador']
    xs = X['controle_dos_dois_lados_2026']; xp = X['puxao_de_todos_os_partidos']; xe = X['escala_27_UFs']; xz = X['zonas_por_votos']
    ef = {a: xa[a]['efeito_fixo'] for a in xa}
    eq = X['equivalente_em_retirada_uniforme']
    xu = xp['U22, efeito fixo de município']; xl = xp['U22, efeito fixo de local']
    todosq = [Q['principal_M0+P+T_em_U22'], Q['so_P_em_U'], Q['so_P_em_U22'], Q['versao_D_M0+D+T_em_U22'], Q['versao_D_so_D_em_U'], Q['P_com_legenda_M0+Pleg+T_em_U22'],
              xs['M0+P+P13+T']['Q'], xs['M0+D+D13+T']['Q'], xu['Q'], xu['Q_par_tipico'], xp['U, efeito fixo de município']['Q'], xp['U, efeito fixo de município']['Q_par_tipico'],
              sen['sem_peso']['Q_P_T'], sen['sem_peso']['Q_D_T'], sen['efeito_fixo_de_local']['Q_P_T'], sen['efeito_fixo_de_local']['Q_D_T'],
              sen['ligacao_2022_aptos_a_20pct']['Q_P_T'], sen['ligacao_2022_aptos_a_20pct']['Q_D_T'], xl['Q'], xl['Q_par_tipico']]
    ret = cal['retirada_2t']; ia = cal['inocente_A']; ib = cal['inocente_B']

    L.append('R27_N2 (ADENDO 28, N2): QUEM NÃO VOLTOU. MOBILIZAÇÃO DO 1º TURNO OU RETIRADA')
    L.append('')
    par(f"Registro: {R['registro']}, escrito depois da Onda A e antes de rodar. Decisões que o registro não fixa: docstring de "
        f"scripts/analisar_R27_N2.py, gravado antes de qualquer conta com votos (cópia e SHA-256 {R['docstring_antes_de_rodar'][0][:16]}... "
        f"em /home/user/trabalho-eleicao/adendo27/R27_N2/, {R['docstring_antes_de_rodar'][2]}). Limite dito no registro e que vale para tudo abaixo: "
        "boletim não distingue eleitor que ficou em casa de eleitor registrado como ausente. O teste só mede se a explicação sem fraude "
        "(mobilização local do 1º turno que não se repetiu) deixa as marcas que deveria.")
    L.append('')
    L.append('VEREDITO PELA LETRA: INCONCLUSIVO')
    item(f"Marca (i), controles pela letra (puxão P e comparecimento contra 2022, T): a assimetria cai {pc(ver['Q_principal'])} "
         f"(intervalo de 95% por reamostragem de municípios: {pc(ver['Q_ic95_reamostragem'][0])} a {pc(ver['Q_ic95_reamostragem'][1])}). "
         "Fica entre os 20% (não explicada) e os 50% (explicada): INCONCLUSIVO. O intervalo cruza os dois limiares.")
    item(f"Marca (ii), municípios pequenos: APARECE (diferença {fz(peq['D'])}, ep {fz(peq['ep_D'], 4, False)}, {fz(abs(peq['z']), 1, False)} erros-padrão). "
         f"Mas aparece com o mesmo sinal e tamanho parecido em 2014 ({fz(oa['2014']['marca_pequenos_D'], 3)}), 2018 ({fz(oa['2018']['marca_pequenos_D'], 3)}) e 2022 ({fz(oa['2022']['marca_pequenos_D'], 3)}): não é marca própria de 2026.")
    item(f"Marca (ii), UFs sem 2º turno de governador: NÃO APARECE (diferença {fz(guf['D'])}, ep {fz(guf['ep_D'], 4, False)}, {fz(abs(guf['z']), 1, False)} erro-padrão). "
         f"Com só 6 UFs do outro lado, a marca só passaria de 3 erros-padrão com diferença de {fz(guf['diferenca_minima_detectavel_a_3ep'], 3, False)}, maior que a própria assimetria: pouco poder.")
    item(f"Calibração do registro (retirada plantada de 3,6%): PASSA. A retirada aumenta a assimetria em {fz(ret[P1]['dA0'])} sem controles e em "
         f"{fz(ret[P1]['dA1'])} com controles (razão {fz(ver['calibracao_retirada_r'], 3, False)}). Os controles não escondem uma retirada real. Não é SEM PODER por esse critério.")
    item(f"Plantio da explicação inocente: a marca (i) PELA LETRA NÃO DISTINGUE as duas leituras. Um puxão de deputado do 22 plantado, do mesmo tamanho, "
         f"em vez de ser absorvido é ampliado pelo controle da letra (razão {fz(ver['inocente_A_r'], 2, False)}; precisava ser 0,50 ou menos). "
         f"Na versão D (fatia do deputado do 22 como regressor, descrita antes de rodar), o puxão plantado é absorvido (razão {fz(ver['versao_D']['r_inocente_A'], 3, False)}) e a retirada "
         f"plantada fica (razão {fz(ver['versao_D']['r_retirada'], 3, False)}). Nessa versão a assimetria de 2026 NÃO cai: cresce {pc(-ver['versao_D']['Q'])} "
         f"(Q = {fz(ver['versao_D']['Q'], 3)}; intervalo {fz(ver['versao_D']['ic95'][0], 3)} a {fz(ver['versao_D']['ic95'][1], 3)}), o que pela régua do registro seria \"não explicada\". "
         f"Com o voto de deputado de todos os partidos (exploratório, também separa os plantios) cai {pc(xu['Q'])} (intervalo {pc(xp['Q_U22_reamostragem']['ic95'][0])} a {pc(xp['Q_U22_reamostragem']['ic95'][1])}). "
         f"Em nenhuma forma de pôr o voto de deputado no modelo a assimetria cai pela metade (Q de {fz(min(todosq), 2)} a {fz(max(todosq), 2)}).")
    par("Resumo em uma frase: a assimetria existe no modelo do registro e as duas medidas de mobilização local que o registro escolheu não a explicam, "
        "mas ela não tem a forma de uma retirada uniforme e o mesmo desenho por porte e por força do PT aparece em eleições anteriores; "
        "o teste não decide entre abstenção e retirada.")
    L.append('')
    L.append('1. UNIVERSO E MODELO 0')
    par(f"Universo (letra): {fi(U['secoes'])} seções das 27 UFs com aptos iguais nos dois turnos (de {fi(R['base_info']['secoes_27ufs_dois_turnos'])} com os dois turnos; "
        f"{fi(R['base_info']['secoes_27ufs_dois_turnos'] - U['secoes'])} ficam fora por aptos diferentes), {fi(U['municipios'])} municípios, {fi(U['aptos'])} aptos. "
        f"Comparecimento {fi(U['comparecimento_1t'])} no 1º turno e {fi(U['comparecimento_2t'])} no 2º. Flávio {fi(U['flavio_1t'])} e {fi(U['flavio_2t'])}; "
        f"Lula {fi(U['lula_1t'])} e {fi(U['lula_2t'])}; margem do 2º turno no universo {fi(U['margem_2t_no_universo'])}.")
    par(f"Modelo 0 (y = variação do comparecimento sobre aptos; fatias do 1º turno sobre aptos; efeito fixo de município; peso aptos; erro por município; n = {fi(m0['n'])}): "
        f"Flávio {fz(m0['coef']['F'])} (ep {fz(m0['ep']['F'], 4, False)}), Lula {fz(m0['coef']['L'])} (ep {fz(m0['ep']['L'], 4, False)}), "
        f"eliminados {fz(m0['coef']['E'])} (ep {fz(m0['ep']['E'], 4, False)}), branco e nulo {fz(m0['coef']['BN'])} (ep {fz(m0['ep']['BN'], 4, False)}). "
        "Cada coeficiente é a variação do comparecimento por eleitor daquele tipo, em relação a um faltoso do 1º turno. Código próprio; bate com scripts/lib.py "
        f"(diferença máxima {m0['confere_lib_fe_ols']['max_dif_coef']:.0e}).")
    par(f"ASSIMETRIA A0 = Flávio menos Lula = {fz(a0)} (ep {fz(m0['ep_A'], 4, False)}; {fz(abs(m0['z_A']), 1, False)} erros-padrão). Em palavras: dentro do mesmo município, "
        f"de cada 100 eleitores de Flávio do 1º turno voltaram {fz(-100 * a0, 2, False)} a menos do que de cada 100 eleitores de Lula "
        "(leitura por seção, não por eleitor: é inferência, não contagem). "
        f"Em votos: {fi(V['V0_em_U'])} (ep {fi(V['ep_V0_em_U'])}), {pc(V['V0_em_U_sobre_margem'])} da margem oficial de {fi(MARGEM)}. "
        "Cada um vale 1 voto de margem, não 2, porque não vira voto de Lula.")
    par("Aviso: este número não é o da Onda A (2,67% contra -0,85%, 3,5 pontos, 1,73 milhão). O modelo do registro, com efeito fixo de município, mede "
        f"{fz(-100 * a0, 2, False)} ponto. A diferença está explicada no item 10 (o tamanho depende do nível da comparação).")
    L.append('')
    L.append('2. MARCA (i): A ASSIMETRIA DIMINUI COM OS CONTROLES DO PUXÃO LOCAL?')
    par(f"P = votos nominais dos candidatos do 22 a deputado federal sobre aptos menos a fatia de Flávio (bweb do 1º turno: {fi(R['extracao_depfed']['linhas_depfed'])} linhas de "
        f"deputado federal em {fi(R['extracao_depfed']['secoes'])} seções, de {fi(R['extracao_depfed']['linhas_total'])} linhas lidas; {fi(U['depfed_nominal_22'])} votos nominais do 22 no universo). "
        f"T = comparecimento do 1º turno de 2026 menos o de 2022 na mesma seção; a chave liga em {fi(U['U22'])} seções (U22). Tabela (A, ep, n):")
    for un, nome in (('U', 'M0'), ('U', 'M0+P'), ('U', 'M0+D'), ('U22', 'M0'), ('U22', 'M0+T'), ('U22', 'M0+P'), ('U22', 'M0+P+T'), ('U22', 'M0+D+T')):
        r = C[un][nome]
        ex = ', '.join(f"{k} {fz(r['coef'][k])} (ep {fz(r['ep'][k], 4, False)})" for k in r['coef'] if k not in ('F', 'L', 'E', 'BN'))
        L.append(f"    {un:<3} {nome:<8} A = {fz(r['A'])}  ep {fz(r['ep_A'], 4, False)}  n = {fi(r['n'])}" + (f"   controles: {ex}" if ex else ''))
    par(f"Queda principal (letra), M0+P+T contra M0 nas mesmas {fi(U['U22'])} seções: Q = {fz(Q['principal_M0+P+T_em_U22'], 3)} "
        f"(ep {fz(bt['Q_principal']['ep'], 3, False)}; intervalo de 95% {fz(bt['Q_principal']['ic95'][0], 3)} a {fz(bt['Q_principal']['ic95'][1], 3)}). "
        f"Só P: {fz(Q['so_P_em_U'], 3)} em U ({fz(bt['Q_so_P_em_U']['ic95'][0], 3)} a {fz(bt['Q_so_P_em_U']['ic95'][1], 3)}). "
        f"Só T: {fz(Q['so_T_em_U22'], 3)} ({fz(bt['Q_so_T']['ic95'][0], 3)} a {fz(bt['Q_so_T']['ic95'][1], 3)}): T não mexe na assimetria.")
    par("O que os controles dizem, em português simples:")
    zt = abs(C['U22']['M0+T']['coef']['T'] / C['U22']['M0+T']['ep']['T'])
    item(f"O coeficiente de T é forte ({fz(C['U22']['M0+T']['coef']['T'], 3)}, {fz(zt, 0, False)} erros-padrão): seção que compareceu mais no 1º turno de 2026 "
         "do que em 2022 perdeu mais comparecimento no 2º. A marca do \"comparecimento extra que não volta\" existe, mas vale igual para os dois lados e não muda a assimetria. "
         f"E é a mesma em 2022 ({fz(oa['2022']['coef_T'], 3)}) e em 2018 ({fz(oa['2018']['coef_T'], 3)}).")
    item(f"O coeficiente do puxão do 22 é POSITIVO ({fz(C['U']['M0+P']['coef']['P'], 4)}, ep {fz(C['U']['M0+P']['ep']['P'], 4, False)}): onde os candidatos a deputado do 22 tiveram mais voto, "
         "com o voto de Flávio fixo, o comparecimento se segurou um pouco MELHOR. A hipótese da mobilização previa o contrário (quem veio pelo deputado não volta).")
    item(f"Por isso a \"queda\" de {pc(Q['principal_M0+P+T_em_U22'])} pela letra é efeito de álgebra: P contém menos F, então com P no modelo o coeficiente de Flávio soma o coeficiente "
         f"(positivo) do puxão. Com a fatia do deputado do 22 como regressor (versão D, mesmo ajuste), A vai de {fz(a22)} para {fz(ad)}: cresce {pc(-Q['versao_D_M0+D+T_em_U22'])}. "
         f"Dito de outro modo: o eleitor de Flávio que também votou em deputado do 22 tem assimetria {fz(a1)}; o que votou em Flávio sem votar em deputado do 22, {fz(ad)}. "
         "Os dois tipos voltaram menos que o eleitor de Lula, e o que veio \"pelo deputado\" voltou um pouco mais, não menos.")
    L.append('')
    L.append('3. MARCAS (ii)')
    par(f"Municípios pequenos (menos de 20.000 aptos; {fi(peq['municipios_grupo'])} municípios, {fi(peq['secoes_grupo'])} seções, {fi(peq['flavio_1t_grupo'])} votos de Flávio): "
        f"A = {fz(peq['pequenos']['A'])} (ep {fz(peq['pequenos']['ep_A'], 4, False)}) contra {fz(peq['demais']['A'])} (ep {fz(peq['demais']['ep_A'], 4, False)}) nos demais. "
        f"Diferença {fz(peq['D'])} (ep {fz(peq['ep_D'], 4, False)}), {fz(abs(peq['z']), 2, False)} erros-padrão: a marca aparece. "
        f"Cortes ao lado: 10 mil {fz(mk['ao_lado_corte_10mil']['D'])} ({fz(abs(mk['ao_lado_corte_10mil']['z']), 1, False)} ep); 50 mil {fz(mk['ao_lado_corte_50mil']['D'])} ({fz(abs(mk['ao_lado_corte_50mil']['z']), 1, False)} ep).")
    par(f"UFs sem 2º turno de governador (21) contra as 6 com (AC, AM, DF, ES, RN, TO): A = {fz(guf['sem_governador_21']['A'])} (ep {fz(guf['sem_governador_21']['ep_A'], 4, False)}) contra "
        f"{fz(guf['com_governador_6']['A'])} (ep {fz(guf['com_governador_6']['ep_A'], 4, False)}). Diferença {fz(guf['D'])} (ep {fz(guf['ep_D'], 4, False)}), {fz(abs(guf['z']), 2, False)} erro-padrão: não aparece. "
        f"Permutação exata das {fi(guf['permutacao_exata']['escolhas'])} escolhas de 6 UFs: p unilateral {fz(guf['permutacao_exata']['p_unilateral_simples'], 2, False)} (média simples) e "
        f"{fz(guf['permutacao_exata']['p_unilateral_ponderada'], 2, False)} (ponderada).")
    cr = mk['com_retirada_plantada']
    par(f"Com a retirada plantada as marcas quase não mudam (pequenos {fz(cr['municipio_pequeno_20mil']['D'])}, {fz(abs(cr['municipio_pequeno_20mil']['z']), 1, False)} ep; "
        f"UFs {fz(cr['uf_sem_2t_governador']['D'])}, {fz(abs(cr['uf_sem_2t_governador']['z']), 1, False)} ep): as marcas (ii) existiriam com ou sem retirada uniforme. "
        "Elas são condição para a leitura inocente, não prova dela.")
    L.append('')
    L.append('4. CALIBRAÇÃO POR EFEITO PLANTADO (dados de 2026)')
    par(f"Retirada (a irregularidade do registro): em cada seção, Binomial(votos de Flávio no 2º turno; 0,036) eleitores passam à abstenção: {fi(pl['retirada_2t_eleitores_em_U'])} no universo. "
        f"A assimetria aumenta {fz(ret[P1]['dA0'])} no modelo 0 e {fz(ret[P1]['dA1'])} com P e T: razão {fz(ret[P1]['r'], 3, False)} (reamostragem: {fz(bt['r_retirada_principal']['ic95'][0], 3, False)} a {fz(bt['r_retirada_principal']['ic95'][1], 3, False)}). "
        f"Versão D: {fz(ret[D1]['r'], 3, False)}. Sem sorteio: {fz(cal['retirada_2t_sem_sorteio'][P1]['r'], 3, False)}. Com 3,6% dos votos do 1º turno: {fz(cal['retirada_1t'][P1]['r'], 3, False)}. "
        "O teste enxerga a retirada do tamanho registrado e os controles não a engolem (critério: 0,80 ou mais).")
    par(f"Inocente A (puxão do deputado do 22 que não volta): Binomial(votos nominais do 22; {pc(pl['inocente_A_taxa'], 2)}), {fi(pl['inocente_A_eleitores_em_U'])} eleitores, o mesmo total. "
        f"Aumenta a assimetria {fz(ia[P1]['dA0'])} no modelo 0. Com os controles da letra o aumento vira {fz(ia[P1]['dA1'])} (razão {fz(ia[P1]['r'], 2, False)}): a letra não reconhece o puxão, amplia. "
        f"Na versão D o aumento vira {fz(ia[D1]['dA1'])} (razão {fz(ia[D1]['r'], 3, False)}): absorvido. "
        "Ressalva: o plantio A é proporcional a D22 por construção, então a versão D o absorve quase por definição; o que não é trivial é a letra ampliar.")
    par(f"Inocente B (comparecimento extra do 1º turno contra 2022 que não volta): {fi(pl['inocente_B_eleitores_em_U22'])} eleitores, {pc(pl['inocente_B_taxa'])} do comparecimento extra "
        f"({fi(pl['inocente_B_comparecimento_extra_total_em_U22'])}). No modelo 0 a assimetria anda {fz(ib[P1]['dA0'])}, isto é, no sentido CONTRÁRIO: dentro dos municípios, "
        "o comparecimento a mais do que em 2022 esteve mais nas seções de Lula. Essa forma de mobilização não tem como produzir a assimetria observada, e a razão "
        f"({fz(ib[P1]['r'], 2, False)}) não tem leitura.")
    par("Conclusão da calibração: pelo critério do registro o teste tem poder. Mas a marca (i) como escrita não separa mobilização de retirada: "
        f"tanto a retirada plantada (Q do próprio plantio {fz(ret[P1]['Q_do_proprio_plantio'], 2)}) quanto o puxão plantado ({fz(ia[P1]['Q_do_proprio_plantio'], 2)}) dariam \"não explicada\". "
        f"Quem separa é a versão D ({fz(ret[D1]['Q_do_proprio_plantio'], 2)} contra {fz(ia[D1]['Q_do_proprio_plantio'], 2)}), e nela o dado de 2026 dá {fz(Q['versao_D_M0+D+T_em_U22'], 2)}. "
        f"O modelo com deputado de todos os partidos (exploratório, item 10e) também separa e dá {fz(xu['Q'], 2)}.")
    L.append('')
    L.append('5. ESPELHOS')
    vezes = abs((C['U22']['M0+P13+T']['A'] - a22) / (a1 - a22))
    item(f"E1, controle espelho (puxão dos candidatos do 13, P13 = D13/aptos menos L): A vai de {fz(a22)} para {fz(C['U22']['M0+P13+T']['A'])} (Q = {fz(Q['espelho_P13_M0+P13+T_em_U22'], 2)}). "
         f"O mesmo cálculo feito para o lado do PT mexe {fz(vezes, 1, False)} vezes mais e no sentido contrário. Com os dois puxões juntos (exploratório): "
         f"A = {fz(xs['M0+P+P13+T']['A'])}, Q = {fz(xs['reamostragem']['Q_P_P13_T']['estimativa'], 2)} (intervalo {fz(xs['reamostragem']['Q_P_P13_T']['ic95'][0], 2)} a {fz(xs['reamostragem']['Q_P_P13_T']['ic95'][1], 2)}). "
         f"Tratando os dois lados do mesmo jeito, a assimetria cresce. A queda de {pc(Q['principal_M0+P+T_em_U22'], 0)} da letra não é marca da mobilização da direita.")
    item(f"E2, plantio espelho (3,6% dos votos de Lula do 2º turno, {fi(pl['espelho_lula_eleitores_em_U'])} eleitores): A anda {fz(cal['espelho_lula_2t'][P1]['dA0'])} sem controles e "
         f"{fz(cal['espelho_lula_2t'][P1]['dA1'])} com (razão {fz(cal['espelho_lula_2t'][P1]['r'], 3, False)}). Simétrico, como devia.")
    item("E3, outros anos: item 6.")
    L.append('')
    L.append('6. OUTROS ANOS, COM O VALOR BRUTO DE 2026 AO LADO (comparação, não régua de inocência: o Léo suspeita também deles)')
    L.append('    ano   A0 (adversário menos PT)  ep       pequenos menos demais           sem menos com governador        coef. T   Q só T')
    for a in ('2026', '2022', '2018', '2014'):
        v = oa[a]
        if a == '2026':
            pe, ue = peq['ep_D'], guf['ep_D']
        else:
            pe, ue = v['marca_pequenos_ep'], v['marca_uf_ep']
        ct = fz(v.get('coef_T'), 3) if v.get('coef_T') is not None else ' n/d  '
        qt = fz(v.get('Q_so_T'), 2) if v.get('Q_so_T') is not None else 'n/d'
        L.append(f"    {a}  {fz(v['A0']):>9}                {fz(v['ep_A0'], 4, False)}   {fz(v['marca_pequenos_D'])} (ep {fz(pe, 4, False)}; {fz(abs(v['marca_pequenos_z']), 1, False)} ep)   "
                 f"{fz(v['marca_uf_D'])} (ep {fz(ue, 4, False)}; {fz(abs(v['marca_uf_z']), 1, False)} ep)   {ct}    {qt}")
    par("2026 é o único dos quatro anos em que o eleitor do adversário do PT voltou menos que o do PT neste modelo. Contra 2022 a diferença é "
        f"{fz(oa['2026']['A0'] - oa['2022']['A0'], 3)}. A diferença entre municípios pequenos e os demais tem o mesmo sinal e tamanho parecido nos quatro anos: "
        "é um traço fixo (no município pequeno o eleitor da direita volta menos, em relação ao do PT, do que na cidade grande), não uma novidade de 2026. "
        "UFs com 2º turno de governador: " + '; '.join(f"{a}: {', '.join(oa[a]['ufs_com_2t_governador'])}" for a in ('2026', '2022', '2018', '2014')) + '.')
    L.append('')
    L.append('7. VOTOS DE MARGEM')
    item(f"Modelo do registro: {fi(V['V0_em_U'])} eleitores de Flávio que não voltaram acima da taxa do eleitor de Lula (ep {fi(V['ep_V0_em_U'])}), {pc(V['V0_em_U_sobre_margem'])} da margem. "
         f"Estendido às seções fora do universo (extrapolação): {fi(xe['V0_registro_escalado'])}, {pc(xe['V0_registro_escalado_sobre_margem'])}.")
    item(f"Em U22: {fi(V['V0_em_U22'])} sem controles; {fi(V['V1_em_U22_com_P_T'])} com P e T (os controles da letra \"absorvem\" {fi(V['absorvido_pelos_controles_letra'])}); "
         f"{fi(V['V1_em_U22_com_D_T'])} na versão D (cresce {fi(-V['absorvido_pelos_controles_versao_D'])}).")
    item(f"Tamanho de comparação: a retirada plantada de 3,6% são {fi(pl['retirada_2t_eleitores_em_U'])} eleitores e desloca A em {fz(cal['retirada_2t']['U: M0+P (letra, só P)']['dA0'])}. "
         f"A assimetria observada ({fz(a0)}) equivale a uma retirada uniforme de {pc(eq['regua_zero'])} dos votos de Flávio se a régua natural for zero; "
         f"de {pc(eq['regua_2022'])} se for a de 2022; {pc(eq['regua_2018'])} se for a de 2018; "
         f"{pc(eq['regua_2014'])} se for a de 2014. Nenhuma régua é segura (o Léo suspeita de todos os anos).")
    item("Sozinho este canal não vira o resultado: para virar só por retirada seriam precisos 4,43 milhões de eleitores de Flávio.")
    L.append('')
    L.append('8. DESCRITIVO (modelo 0 dentro de cada recorte)')
    L.append('  Por UF (A, ep, erros-padrão, votos V; * = UF com 2º turno de governador):')
    ufs = sorted(des['uf'].items(), key=lambda kv: kv[1]['A'])
    for u, v in ufs:
        L.append(f"    {u}{'*' if v['com_2t_governador'] else ' '}  A = {fz(v['A'])}  ep {fz(v['ep_A'], 4, False)}  ({fz(abs(v['z_A']), 1, False):>4} ep)  seções {fi(v['n']):>7}  Flávio 1º turno {fi(v['flavio_1t']):>10}  V = {fi(v['V']):>8}")
    nneg = sum(1 for _, v in ufs if v['A'] < 0)
    n3 = sum(1 for _, v in ufs if v['z_A'] < -3)
    par(f"  {nneg} de 27 UFs têm A negativa; {n3} a mais de 3 erros-padrão. Invertida (o eleitor de Flávio voltou MAIS): RJ ({fz(des['uf']['RJ']['A'])}, {fz(des['uf']['RJ']['z_A'], 1, False)} ep), PA, AM e AP. "
        f"Em votos pesa SP ({fi(des['uf']['SP']['V'])}), depois MG, BA, CE e PE. Soma das 27: {fi(X['V_somado_por_UF'])}.")
    par(f"  Diferem da Onda A: aqui PI {fz(des['uf']['PI']['A'], 3)}, MA {fz(des['uf']['MA']['A'], 3)}, TO {fz(des['uf']['TO']['A'], 3)}, PB {fz(des['uf']['PB']['A'], 3)}, CE {fz(des['uf']['CE']['A'], 3)} "
        "(a Onda A dava de 8 a 15 pontos nessas UFs). O efeito fixo de município tira a parte que é diferença entre municípios inteiros.")
    L.append('  Por porte do município (aptos no 1º turno):')
    for k, v in des['porte'].items():
        L.append(f"    {k:<16} A = {fz(v['A'])}  ep {fz(v['ep_A'], 4, False)}  municípios {fi(v['municipios']):>5}  seções {fi(v['n']):>7}  Flávio {fi(v['flavio_1t']):>10}  V = {fi(v['V']):>8}")
    L.append('  Por força de Lula na seção (Lula sobre válidos do 1º turno):')
    for k, v in des['faixa_forca_lula'].items():
        L.append(f"    {k:<13} A = {fz(v['A'])}  ep {fz(v['ep_A'], 4, False)}  seções {fi(v['n']):>7}  Flávio {fi(v['flavio_1t']):>10}  V = {fi(v['V']):>8}")
    par("  A assimetria é quase zero onde Flávio é forte e cresce com a força de Lula e com o município menor. Não é uniforme.")
    z = des['zonas']
    L.append('')
    L.append('  AS 20 ZONAS DE MAIOR ASSIMETRIA (para conferência de cadernos de votação)')
    par(f"  Zonas com 50 ou mais seções no universo: {fi(z['zonas_com_50_ou_mais_secoes'])}. Tamanho = menos A da zona (efeito fixo de município, erro robusto por seção). "
        f"Mediana {fz(z['mediana_tamanho'], 3)}; {z['zonas_com_tamanho_positivo_a_2ep']} zonas com tamanho positivo a 2 erros-padrão e {z['zonas_com_tamanho_negativo_a_2ep']} com negativo "
        "(o acaso daria cerca de 58 de cada lado). A estimativa por zona é ruidosa: o limite conservador é tamanho menos 1,645 ep. "
        f"As 20 ficam todas acima do tamanho nacional por esse limite, mas somam só {fi(xz['top20_registrado_V_somado'])} votos: são zonas pequenas, quase todas reduto de Lula.")
    L.append('    zona     seções tam.   ep    limite Flávio 1T/2T   Lula 1T/2T      comp. 1T/2T       V   lat, lon          municípios')
    for r_ in z['top20_por_tamanho']:
        cm = r_.get('coordenada_mediana')
        co = f"{cm[0]:.2f}, {cm[1]:.2f}".replace('.', ',') if cm else 'n/d'
        ms = ', '.join(r_['municipios'][:4]) + (f" e mais {len(r_['municipios']) - 4}" if len(r_['municipios']) > 4 else '')
        L.append(f"    {r_['zona']:<8} {r_['secoes']:>5}  {fz(r_['tamanho'], 3, False)} {fz(r_['ep'], 3, False)} {fz(r_['limite_conservador'], 3, False)}  {fi(r_['flavio_1t']):>6}/{fi(r_['flavio_2t']):<6} {fi(r_['lula_1t']):>6}/{fi(r_['lula_2t']):<6}  "
                 f"{fi(r_['comp_1t']):>6}/{fi(r_['comp_2t']):<6} {fi(r_['V']):>5}  {co:<16} {ms}")
    so = [r_['zona'] for r_ in z['top20_por_limite_conservador'] if r_['zona'] not in {t['zona'] for t in z['top20_por_tamanho']}]
    par(f"  Pela ordem do limite conservador entram no lugar de outras: {', '.join(so)}. UFs das 20: " + ', '.join(f'{u} {n_}' for u, n_ in sorted(z['top20_UFs'].items(), key=lambda kv: -kv[1])) + '.')
    L.append('')
    L.append('9. SENSIBILIDADES (fixadas antes; não decidem)')
    item(f"Sem peso: A0 = {fz(sen['sem_peso']['A0_em_U'])}; Q da letra {fz(sen['sem_peso']['Q_P_T'], 3)}; versão D {fz(sen['sem_peso']['Q_D_T'], 3)}.")
    item(f"Efeito fixo de local de votação (compara seções da mesma escola): A0 = {fz(sen['efeito_fixo_de_local']['A0_em_U'])} (ep {fz(sen['efeito_fixo_de_local']['ep_A0_em_U'], 4, False)}), o dobro do modelo do registro; "
         f"Q da letra {fz(sen['efeito_fixo_de_local']['Q_P_T'], 3)}; versão D {fz(sen['efeito_fixo_de_local']['Q_D_T'], 3)}.")
    item(f"Ligação com 2022 só com aptos a 20% ({fi(sen['ligacao_2022_aptos_a_20pct']['secoes'])} seções): Q da letra {fz(sen['ligacao_2022_aptos_a_20pct']['Q_P_T'], 3)}; versão D {fz(sen['ligacao_2022_aptos_a_20pct']['Q_D_T'], 3)}.")
    item(f"P com legenda: Q = {fz(sen['P_com_legenda']['Q_M0+Pleg+T_em_U22'], 3)}. Seções que não ligam com 2022 ({fi(sen['fora_de_U22']['secoes'])}): A0 = {fz(sen['fora_de_U22']['A0'])}.")
    qs = [Q['principal_M0+P+T_em_U22'], sen['sem_peso']['Q_P_T'], sen['efeito_fixo_de_local']['Q_P_T'], sen['ligacao_2022_aptos_a_20pct']['Q_P_T'], sen['P_com_legenda']['Q_M0+Pleg+T_em_U22']]
    par(f"  O Q da letra fica entre {fz(min(qs), 2)} e {fz(max(qs), 2)} conforme a variante: nunca chega a 0,50; em {sum(1 for q_ in qs if q_ < 0.2)} das {len(qs)} fica abaixo de 0,20. "
        "A versão D é negativa em todas.")
    L.append('')
    L.append('10. EXPLORATÓRIO (feito DEPOIS de ver os resultados acima; não muda veredito; cerca de 200 números olhados)')
    par("  (a) O tamanho e até o sinal de A dependem do nível da comparação. A (adversário menos PT), erro por município entre parênteses:")
    L.append('      efeito fixo               2026               2022               2018               2014')
    for nome in ('nenhum (constante)', 'UF', 'zona', 'município (registro)', 'local de votação'):
        L.append(f"      {nome:<22}" + ''.join(f"  {fz(ef[a][nome]['A'])} ({fz(ef[a][nome]['ep_A'], 4, False)})" for a in ('2026', '2022', '2018', '2014')))
    par(f"  Em 2026, comparando seções do país inteiro ou da mesma UF, o eleitor de Flávio NÃO aparece voltando menos ({fz(ef['2026']['UF']['A'])} com efeito fixo de UF). "
        f"A assimetria só aparece dentro do município ({fz(ef['2026']['município (registro)']['A'])}) e dobra dentro do mesmo local de votação ({fz(ef['2026']['local de votação']['A'])}, "
        f"{fi(ef['2026']['local de votação']['V'])} votos; estendido a todas as seções, {fi(xe['V_efeito_fixo_local_escalado'])}, {pc(xe['V_efeito_fixo_local_escalado_sobre_margem'])} da margem). "
        "É esse número, o de dentro do local, que fica do tamanho do 1,73 milhão da Onda A (não conferi qual comparação a Onda A usou). "
        "Do efeito fixo de UF ao de local, em todos os anos A fica mais negativa quanto mais fina a comparação; "
        f"2026 fica abaixo de 2022 em todos os níveis (de {fz(ef['2026']['nenhum (constante)']['A'] - ef['2022']['nenhum (constante)']['A'], 3)} a {fz(ef['2026']['local de votação']['A'] - ef['2022']['local de votação']['A'], 3)}).")
    par("  (b) Por força do PT na seção, A com efeito fixo de município e, entre colchetes, de local:")
    L.append('      faixa do PT       2026                2022                2018                2014')
    for nome in ('menos de 35%', '35 a 50%', '50 a 65%', '65% ou mais'):
        L.append(f"      {nome:<13}" + ''.join(f"  {fz(xa[a]['faixa_forca_PT'][nome]['A'], 3)} [{fz(xa[a]['faixa_forca_PT'][nome]['A_efeito_fixo_local'], 3)}]" for a in ('2026', '2022', '2018', '2014')))
    par("  O degrau \"onde o PT é forte o eleitor da direita volta menos\" existe em 2018 e 2022 também. Dentro do local, 2026 repete 2018 em três das quatro faixas "
        f"e passa dele na faixa de 65% ou mais ({fz(xa['2026']['faixa_forca_PT']['65% ou mais']['A_efeito_fixo_local'], 3)} contra {fz(xa['2018']['faixa_forca_PT']['65% ou mais']['A_efeito_fixo_local'], 3)}; "
        f"essa faixa tem {fi(xa['2026']['faixa_forca_PT']['65% ou mais']['adversario_1t'])} votos de Flávio). Contra 2022 a diferença é parecida em todas as faixas (de 3 a 8 pontos).")
    par("  (c) Por porte, A por ano (efeito fixo de município):")
    L.append('      porte              2026      2022      2018      2014')
    for nome in ('até 10 mil', '10 a 20 mil', '20 a 50 mil', '50 a 200 mil', '200 mil ou mais'):
        L.append(f"      {nome:<16}" + ''.join(f"  {fz(xa[a]['porte'][nome]['A'], 4)}" for a in ('2026', '2022', '2018', '2014')))
    d22 = X['uf_2026_menos_2022']
    od = sorted(d22.items(), key=lambda kv: kv[1])
    par("  (d) A de 2026 menos A de 2022 por UF: negativa nas 27. Maiores: " + ', '.join(f"{u} {fz(v, 3)}" for u, v in od[:6]) + ". Menores: " + ', '.join(f"{u} {fz(v, 3)}" for u, v in od[-6:]) +
        ". As UFs que a Onda A apontou (PI, MA, CE, TO, PB) estão entre as que MENOS mudaram contra 2022: ali o eleitor da direita já voltava menos em 2022 "
        f"(PI {fz(xa['2022']['uf']['PI']['A'], 3)}, MA {fz(xa['2022']['uf']['MA']['A'], 3)}, CE {fz(xa['2022']['uf']['CE']['A'], 3)}). A mudança é nacional, não regional.")
    par("  (e) Puxão medido pelos candidatos a deputado federal de TODOS os partidos (fatia de cada partido com 1% ou mais dos nominais, demais somados, legenda; "
        f"referência = branco e nulo de deputado), mais T: A vai de {fz(xu['A0'])} para {fz(xu['A_com_todos_os_partidos'])}, Q = {fz(xu['Q'], 3)} "
        f"(intervalo {fz(xp['Q_U22_reamostragem']['ic95'][0], 3)} a {fz(xp['Q_U22_reamostragem']['ic95'][1], 3)}). Esse modelo preserva a retirada plantada "
        f"(razão {fz(xp['calibracao_retirada_2t']['r'], 3, False)}) e absorve o puxão plantado ({fz(xp['calibracao_inocente_A']['r'], 3, False)}). Com efeito fixo de local: de {fz(xl['A0'])} para "
        f"{fz(xl['A_com_todos_os_partidos'])} (Q = {fz(xl['Q'], 3)}, cresce). Leitura: nesse modelo A compara eleitores de Flávio e de Lula que NÃO votaram em deputado (branco ou nulo). "
        f"Quase todo coeficiente de partido é positivo (quem vota em deputado volta mais, o contrário do que o puxão previa), e o do 13 ({fz(xu['coef']['dep_13'], 3)}) é maior que o do 22 ({fz(xu['coef']['dep_22'], 3)}). "
        f"Para o par típico (Flávio com deputado do 22 contra Lula com deputado do 13) a assimetria é {fz(xu['A_par_tipico_F_com_dep22_contra_L_com_dep13'])} (ep {fz(xu['ep_par_tipico'], 4, False)}), maior que A0. "
        "O voto de deputado explica no máximo um terço da assimetria dentro do município, e isso só entre quem não votou em deputado; dentro do local, nada. "
        f"Só um partido tem coeficiente negativo: o 14, MISSÃO ({fz(xu['coef']['dep_14'], 3)}, ep {fz(xu['ep']['dep_14'], 3, False)}): quem votou em deputado dele voltou menos.")
    par(f"  (f) Zonas por votos: as {xz['zonas_com_tamanho_positivo_a_2ep']} zonas com tamanho positivo a 2 erros-padrão somam {fi(xz['V_somado_nessas'])} votos; as {xz['zonas_com_tamanho_negativo_a_2ep']} "
        f"com negativo, {fi(xz['V_somado_nas_negativas'])}. As 20 de maior V (onde cadernos renderiam mais votos conferidos):")
    for r_ in xz['top20_por_V']:
        cm = r_.get('coordenada_mediana')
        co = f"{cm[0]:.2f}, {cm[1]:.2f}".replace('.', ',') if cm else 'n/d'
        ms = ', '.join(r_['municipios'][:3]) + (f" e mais {len(r_['municipios']) - 3}" if len(r_['municipios']) > 3 else '')
        L.append(f"      {r_['zona']:<8} seções {r_['secoes']:>4}  tamanho {fz(r_['tamanho'], 3, False)} (ep {fz(r_['ep'], 3, False)})  Flávio {fi(r_['flavio_1t']):>6}  V = {fi(r_['V']):>5}  {co:<16} {ms}")
    par("  (g) Quem liderou o 1º turno: em 2014 (PT na frente) A0 = " + fz(oa['2014']['A0'], 3) + "; em 2022 (PT na frente) " + fz(oa['2022']['A0'], 3) + "; em 2026 (Flávio na frente) " + fz(oa['2026']['A0'], 3) +
        "; em 2018 (Bolsonaro na frente) " + fz(oa['2018']['A0'], 3) + ". Em três dos quatro anos, quem voltou menos foi o eleitor de quem liderou o 1º turno; 2018 não segue a regra. "
        "Quatro pontos não fazem lei, e o Léo suspeita dos quatro anos.")
    L.append('')
    L.append('A FAVOR DA TESE')
    favor = [
        f"A assimetria existe no modelo fixado antes: {fz(a0)} ({fz(abs(m0['z_A']), 1, False)} ep), {fi(V['V0_em_U'])} votos; dentro do mesmo local de votação é o dobro ({fz(ef['2026']['local de votação']['A'])}, cerca de {fi(ef['2026']['local de votação']['V'])} votos).",
        "A explicação inocente, na forma em que foi registrada, não deixou as marcas: o puxão do deputado do 22 tem sinal contrário ao previsto; o comparecimento a mais do que em 2022 não muda a assimetria "
        f"e esteve do lado de Lula; a marca das UFs sem governador não aparece; na versão D a assimetria cresce {pc(-Q['versao_D_M0+D+T_em_U22'], 0)} em vez de cair; "
        f"em nenhuma das {len(todosq)} formas calculadas de pôr o voto de deputado no modelo ela cai pela metade (Q de {fz(min(todosq), 2)} a {fz(max(todosq), 2)}).",
        f"Os controles não escondem retirada: uma retirada de 3,6% plantada passa inteira (razão {fz(ret[P1]['r'], 2, False)}).",
        f"2026 é o único dos quatro anos com A negativa neste modelo, e fica abaixo de 2022 nas 27 UFs (de {fz(max(X['uf_2026_menos_2022'].values()), 3)} a {fz(min(X['uf_2026_menos_2022'].values()), 3)}) e em todas as faixas e portes (cerca de 4 pontos, do tamanho de uma retirada uniforme de {pc(eq['regua_2022'])} dos votos de Flávio se 2022 fosse a régua).",
        f"Nos redutos de Lula (65% ou mais), dentro do mesmo local, a diferença chega a {fz(xa['2026']['faixa_forca_PT']['65% ou mais']['A_efeito_fixo_local'], 3)}: maior que em 2018 ({fz(xa['2018']['faixa_forca_PT']['65% ou mais']['A_efeito_fixo_local'], 3)}) e 2022 ({fz(xa['2022']['faixa_forca_PT']['65% ou mais']['A_efeito_fixo_local'], 3)}) (exploratório).",
    ]
    contra = [
        f"Não tem a forma de retirada uniforme por programa: é {fz(des['faixa_forca_lula']['menos de 35%']['A'], 3)} onde Flávio é forte ({pc(des['faixa_forca_lula']['menos de 35%']['flavio_1t'] / U['flavio_1t'], 0)} dos votos dele) e {fz(des['faixa_forca_lula']['65% ou mais']['A'], 3)} nos redutos de Lula; "
        f"{fz(des['porte']['até 10 mil']['A'], 3)} nos municípios até 10 mil e {fz(des['porte']['50 a 200 mil']['A'], 3)} nos de 50 a 200 mil; invertida no RJ ({fz(des['uf']['RJ']['z_A'], 1, False)} ep), PA, AM e AP. "
        "Para ser fraude teria de ser operada local a local, não uma regra única.",
        f"O mesmo desenho aparece antes: a diferença entre município pequeno e os demais tem o mesmo sinal e tamanho parecido em 2014 ({fz(oa['2014']['marca_pequenos_D'], 3)}), 2018 ({fz(oa['2018']['marca_pequenos_D'], 3)}) e 2022 ({fz(oa['2022']['marca_pequenos_D'], 3)}), contra {fz(peq['D'], 3)} em 2026; "
        "o degrau por força do PT existe em 2018 (mais forte que em 2026 no modelo do registro) e em 2022; "
        "dentro do local, 2026 repete 2018, eleição que a direita venceu, em três das quatro faixas (exploratório).",
        f"O sinal depende do nível: com efeito fixo de UF A é {fz(ef['2026']['UF']['A'])}, sem efeito fixo {fz(ef['2026']['nenhum (constante)']['A'])}. No agregado deste modelo o eleitor de Flávio não voltou menos; isso só aparece em comparações finas (exploratório).",
        f"Com o voto de deputado de todos os partidos (exploratório) a assimetria cai {pc(xu['Q'], 0)} (intervalo de {pc(xp['Q_U22_reamostragem']['ic95'][0], 0)} a {pc(xp['Q_U22_reamostragem']['ic95'][1], 0)}), dentro da faixa inconclusiva: "
        "parte dela anda junto com o eleitor de Lula votar mais em deputado do próprio partido, e quem vota em deputado volta mais.",
        f"Tamanho: {pc(V['V0_em_U_sobre_margem'])} da margem no modelo do registro (até {pc(xe['V_efeito_fixo_local_escalado_sobre_margem'])} na leitura mais larga, exploratória). Não vira o resultado sozinho.",
        f"Em 2014 ({fz(oa['2014']['A0'], 3)}) e 2022 ({fz(oa['2022']['A0'], 3)}) a assimetria foi maior em tamanho e contra o PT, que venceu as duas. Assimetria deste tipo não é, por si, marca de quem perde por fraude.",
        "Limite do próprio teste: o boletim não separa quem ficou em casa de quem foi registrado como ausente. Nada aqui prova retirada.",
    ]
    for t in favor:
        item(t)
    L.append('CONTRA A TESE')
    for t in contra:
        item(t)
    L.append('O QUE ISSO SIGNIFICA')
    significa = ("O teste foi desenhado para dar à explicação sem fraude a chance de se mostrar: se o eleitor de Flávio não voltou porque no 1º turno tinha sido puxado por campanhas locais, "
                 "isso deveria aparecer onde os deputados do partido dele foram fortes, onde o comparecimento subiu contra 2022, nos municípios pequenos e nas UFs sem 2º turno de governador. "
                 "Das quatro marcas, só a dos municípios pequenos apareceu, e ela existe em todas as eleições. Logo, a mobilização local, do jeito que foi medida, NÃO explica o que a Onda A achou. "
                 f"Isso mantém o indício de pé. Mas o mesmo teste mostra que o indício é menor no modelo fixado ({fz(V['V0_em_U'] / 1e6, 2, False)} milhão, não 1,73), que ele não é uniforme e que tem geografia social "
                 "(redutos de Lula, cidade pequena) repetida de outras eleições. Essa geografia combina com comportamento de eleitor em minoria local e combina também com "
                 "irregularidade feita na mesa onde o adversário tem pouca fiscalização; o que ela torna pouco provável é uma regra única de programa aplicada igual em todo o país. "
                 "As duas leituras continuam abertas; só documento de fora da urna decide (caderno de votação, comprovante no e-Título, perfil do comparecimento do 2º turno).")
    par('  ' + significa)
    L.append('PISTAS')
    pistas = [
        "Cadernos de votação: as 20 zonas do item 8 (assimetria extrema, redutos de Lula, poucos votos) e as 20 do item 10(f) (onde há mais votos: zonas da capital e da Grande São Paulo, Baixada Santista, Campos, Contagem, Águas Lindas, Salvador, Cruzeiro do Sul, Dourados, Santa Rita).",
        "Registrar antes de rodar um teste por local de votação: nas seções com Lula a 65% ou mais, a diferença de 2026 contra 2018 e 2022 dentro do mesmo local (hoje exploratória).",
        "Perfil do comparecimento do 2º turno, quando o TSE publicar: a assimetria dobra dentro do mesmo local, onde as seções costumam diferir pela época do alistamento (idade do eleitor); o perfil diz se quem faltou tem idade de voto facultativo.",
        f"SP soma {fi(des['uf']['SP']['V'])} dos {fi(X['V_somado_por_UF'])} votos da soma por UF e passou de {fz(xa['2022']['uf']['SP']['A'], 3)} em 2022 para {fz(des['uf']['SP']['A'], 3)}; AC e MS são as UFs que mais mudaram contra 2022. As UFs da Onda A (PI, MA, CE) quase não mudaram.",
        "O partido MISSÃO (14) é o único cujo voto de deputado anda junto com perda de comparecimento: vale cruzar com o destino dos eleitores dos eliminados (L4, T37).",
        f"Na síntese, dizer de qual modelo sai cada número do \"eleitor que não voltou\": {fz(V['V0_em_U'] / 1e6, 2, False)} milhão (dentro do município), {fz(ef['2026']['local de votação']['V'] / 1e6, 2, False)} milhão (dentro do local), nenhum (dentro da UF).",
    ]
    for t in pistas:
        item(t)
    L.append('DESVIOS E DECISÕES FORA DO REGISTRO (escritas no docstring antes de calcular, salvo o exploratório)')
    for t in DESVIOS:
        item(t)
    L.append('')
    par("Contagem: uma leitura por limiar (Q), duas marcas a 3 erros-padrão (o acaso daria uma marca falsa em 0,13% das vezes), uma calibração do registro, dois plantios inocentes, três espelhos. "
        "O bloco exploratório olhou cerca de 200 números; nada dele entra como indício sem teste registrado e conferência independente. Teste feito só com boletins e cadastro: "
        "não é contrapeso à hipótese de programa adulterado na origem.")
    par("Arquivos: scripts/analisar_R27_N2.py; resultados/R27_N2_quem_nao_voltou.json; trabalho e parciais em /home/user/trabalho-eleicao/adendo27/R27_N2/ "
        "(base_2026.npz, depfed_1t.npz, depfed_partidos_1t.npz, parciais e o resultado registrado antes do exploratório).")
    txt = '\n'.join(L) + '\n'
    assert chr(8212) not in txt and chr(8211) not in txt
    with open(SAIDA_TXT, 'w') as f:
        f.write(txt)
    R['resumo'] = {
        'veredito_pela_letra': 'INCONCLUSIVO',
        'partes': {
            'marca_i_pela_letra': f"INCONCLUSIVO: Q = {fz(ver['Q_principal'], 3)} (IC95 {fz(ver['Q_ic95_reamostragem'][0], 3)} a {fz(ver['Q_ic95_reamostragem'][1], 3)}), entre 0,20 e 0,50",
            'marca_i_versao_D': f"não explicada (SINAL no sentido estreito, fora da letra): Q = {fz(ver['versao_D']['Q'], 3)} (IC95 {fz(ver['versao_D']['ic95'][0], 3)} a {fz(ver['versao_D']['ic95'][1], 3)})",
            'marca_i_todos_os_partidos_exploratorio': f"Q = {fz(xu['Q'], 3)} (IC95 {fz(xp['Q_U22_reamostragem']['ic95'][0], 3)} a {fz(xp['Q_U22_reamostragem']['ic95'][1], 3)}); par típico Q = {fz(xu['Q_par_tipico'], 3)}",
            'marca_i_todas_as_formas': f"Q de {fz(min(todosq), 2)} a {fz(max(todosq), 2)} em {len(todosq)} formas; nenhuma chega a 0,50",
            'marca_ii_municipios_pequenos': f"aparece ({fz(abs(peq['z']), 2, False)} ep), mas com o mesmo sinal e tamanho parecido em 2014, 2018 e 2022",
            'marca_ii_ufs_sem_governador': f"não aparece ({fz(abs(guf['z']), 2, False)} ep); pouco poder",
            'calibracao_do_registro': f"passa (razão {fz(ver['calibracao_retirada_r'], 3, False)})",
            'plantio_inocente': f"a letra não distingue (razão {fz(ver['inocente_A_r'], 2, False)}); a versão D distingue ({fz(ver['versao_D']['r_inocente_A'], 3, False)} contra {fz(ver['versao_D']['r_retirada'], 3, False)})"},
        'a_favor': favor, 'contra': contra, 'o_que_significa': significa, 'pistas': pistas}
    with open(SAIDA_JSON + '.tmp', 'w') as f:
        json.dump(R, f, ensure_ascii=False, indent=1)
    os.replace(SAIDA_JSON + '.tmp', SAIDA_JSON)
    diga('gravado', SAIDA_TXT, len(L), 'linhas')


def _coordenadas(zonas):
    """Mediana de latitude e longitude dos locais de votação de cada zona pedida (cadastro do TSE, 1º turno)."""
    por_uf = collections.defaultdict(set)
    for z in zonas:
        u, zn = z.split('|')
        por_uf[u].add(int(zn))
    out = {}
    try:
        zf = zipfile.ZipFile(LOCAIS)
    except Exception:
        return out
    for u, zs in por_uf.items():
        nome = f'eleitorado_local_votacao_2026_{u}.csv'
        if nome not in zf.namelist():
            continue
        lat = collections.defaultdict(list)
        lon = collections.defaultdict(list)
        with zf.open(nome) as fh:
            rd = csv.reader(io.TextIOWrapper(fh, encoding='latin1'), delimiter=';')
            cab = next(rd)
            iz, ila, ilo, itu = cab.index('NR_ZONA'), cab.index('NR_LATITUDE'), cab.index('NR_LONGITUDE'), cab.index('NR_TURNO')
            for p in rd:
                try:
                    zn = int(p[iz])
                    if zn not in zs or p[itu] != '1':
                        continue
                    la = float(p[ila].replace(',', '.'))
                    lo = float(p[ilo].replace(',', '.'))
                except Exception:
                    continue
                if la == -1 or lo == -1 or not (-34.5 < la < 6 and -75 < lo < -28):
                    continue
                lat[zn].append(la)
                lon[zn].append(lo)
        for zn in zs:
            if lat[zn]:
                out[f'{u}|{zn}'] = [round(float(np.median(lat[zn])), 4), round(float(np.median(lon[zn])), 4), len(lat[zn])]
    return out




if __name__ == '__main__':
    cmd = sys.argv[1] if len(sys.argv) > 1 else ''
    if cmd == 'extrair':
        extrair()
    elif cmd == 'base':
        base()
    elif cmd == 'rodar':
        rodar()
    elif cmd == 'explorar':
        explorar()
    elif cmd == 'texto':
        texto()
    elif cmd == 'extrair_partidos':
        extrair_partidos()
    elif cmd == 'explorar2':
        explorar2()
    else:
        print(__doc__)
