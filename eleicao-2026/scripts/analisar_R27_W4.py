"""R27_W4: NULOS DE DIGITAÇÃO NO RDV DE PRESIDENTE, PRIMEIRA ETAPA (teste D4-4 de registro/adendo27/desenho_D4_proposta.json).

Registro: Adendo 27 (commit 2748895, 10/11/2026 00:16:42 UTC), Adendo 28 (938be19) e Adendo 30 (a7218fb, 10/11/2026
10:08:24 UTC). O Adendo 30 manda fazer aqui só a primeira etapa: com os RDV da amostra aleatória nova, o número de
testemunhas e o erro-padrão, sem abrir o resultado, para decidir a extensão. O pedido desta onda acrescenta: depois
disso, abrir Theta e aplicar o critério, declarando SEM PODER se o erro total passar do limite.

Este docstring foi escrito ANTES de qualquer conta com votos. Até aqui só foi lida estrutura: a lista de arquivos, o
tamanho médio dos RDV (15.147 bytes no 1º turno, 2.754 no 2º), os códigos de registro do RDV de presidente nos 400
primeiros arquivos de cada turno (tipo 2 nominal com 2 dígitos, 3 branco, 4 nulo com 2 dígitos, 6 nulo sem dígitos;
somas por tipo, nunca por número digitado), os nomes e números dos 13 candidatos do 1º turno (com os totais nacionais
oficiais, que são públicos e já estavam no repositório), as chaves das bases e o formato do perfil do eleitorado.
Nenhuma contagem por número digitado, por lado ou por seção foi olhada.

Uso (nesta ordem; cada etapa grava parcial em /home/user/trabalho-eleicao/adendo27/R27_W4/):
  python3 -I scripts/analisar_R27_W4.py ler      lê os RDV (principal e o que houver da extensão) e a base oficial
  python3 -I scripts/analisar_R27_W4.py pureza   etapa 1: pureza dos códigos no 1º turno
  python3 -I scripts/analisar_R27_W4.py cego     etapas 2 e 3: testemunhas por turno, erro-padrão, regra de parada (sem Theta)
  python3 -I scripts/analisar_R27_W4.py abrir    etapa 4: Theta, critério, calibração, espelho, descritivos; grava
                                                 resultados/R27_W4_nulos_de_digitacao.json e .txt
  (opção --ext em pureza, cego e abrir: junta as seções da extensão que tiverem RDV dos dois turnos)

HIPÓTESE, MARCA, TESTE (do desenho)
O eleitor que erra uma tecla ao digitar 13 ou 22 e confirma gera um voto nulo com os dígitos gravados no RDV. Uma
alteração da contagem (troca ou acréscimo) mexe nos votos válidos, não nos erros de digitação, que continuam
proporcionais a quem quis votar em cada um. Marca: a proporção entre erros vizinhos do 13 e erros vizinhos do 22 anda
menos do 1º para o 2º turno do que a proporção oficial. Theta perto de 0,071 para a troca que vira o resultado, perto
de zero sem alteração.

O QUE O REGISTRO FIXA (aplicado à letra)
- Códigos-testemunha: 32 e 52 para o 22; 31 para o 13. Excluídos de antemão: 12, 23, 21, 16, 25, 43, 11, 33.
- N22_t = nulos de presidente com dígitos 32 ou 52; N13_t = nulos com dígitos 31. No 1º turno o 52 também pode ser
  erro de quem votava 55: regressão de Poisson por seção da contagem de 52 sobre R1 e sobre os votos do 55, e só entra
  a parte atribuída a R1.
- Pureza, antes de abrir, no 1º turno: regressão de Poisson de cada código sobre L1, R1 e demais votos; código com
  menos de 80% da contagem atribuída ao lado previsto é descartado.
- W_t = N13_t / (N13_t + N22_t); P_t oficial nas mesmas seções; Theta = [logit P_2 - logit P_1] - [logit W_2 - logit W_1].
- Erro por bootstrap de municípios. Duas etapas cegas: primeiro só o número de testemunhas por turno e o erro-padrão,
  sem imprimir Theta. Regra de parada: blocos de 10 mil seções até o erro-padrão chegar a 0,022 ou até 60 mil seções.
- SINAL: Theta de pelo menos 0,045 e de pelo menos 2,5 vezes o erro total (raiz de erro-padrão ao quadrado mais erro
  sistemático ao quadrado; erro sistemático = o maior entre 0,015 e o valor absoluto do placebo de 2022), com o mesmo
  sinal em pelo menos 4 das 5 regiões e nos três tercis de escolaridade.
- SEM SINAL: valor absoluto de Theta de no máximo 0,020 com erro total de no máximo 0,027.
- INCONCLUSIVO: erro-padrão acima de 0,022 ao chegar em 60 mil seções; código reprovado na pureza sem substituto;
  Theta entre 0,020 e 0,045; D4-3 e D4-4 com sinais opostos.
- Calibração: plantar a troca de 3,57% na contagem oficial das seções da amostra e conferir que Theta sobe 0,071.
- Dos avisos do Adendo 27: calibração por efeito plantado nos dados de 2026 (se o teste não enxergar o plantado, SEM
  PODER), teste espelho, valor bruto de 2026 ao lado de qualquer comparação com outro ano (este teste não usa outro
  ano nesta etapa), tradução em votos de margem.

DECISÕES QUE O REGISTRO NÃO FIXA (tomadas aqui, antes de calcular qualquer coisa com votos; saem como desvios)
D1. Amostra. Principal: as 3.000 seções de registro/adendo27/amostra_aas_principal.txt (amostra aleatória simples das
    499.205 seções do 2º turno), com RDV dos dois turnos em /home/user/trabalho-eleicao/adendo27/aas/t1 e t2. A
    extensão (amostra_aas_extensao.txt, ext_t1 e ext_t2) só entra com a opção --ext e só nas seções com RDV dos dois
    turnos já baixados; o número é dito. As etapas 1 a 4 são feitas primeiro só com a principal. Se a extensão for
    juntada depois, a conta com ela é a mesma, mas já não é cega (Theta da principal terá sido aberto), e isso é dito.
    Entra a seção que tiver RDV legível nos dois turnos e constar da base oficial nos dois turnos. Se a pasta tiver
    mais de um RDV (mais de um pacote), vale o último listado, e os casos são contados.
D2. Testemunha = voto nulo de presidente (cargo 1, registro tipo 4) cujos dígitos são exatamente o código. Nulo sem
    dígitos (tipo 6) não é testemunha. Seções do exterior ficam nos totais nacionais e fora das regiões.
D3. Votos oficiais: dados/secoes2026.json.gz (bweb); votos por candidato do 1º turno: dados/candidatos2026_1t.json.gz.
    P_t = soma de L_t sobre soma de (L_t + R_t), nas mesmas seções. Conferência do leitor: nominais por número,
    brancos e nulos do RDV contra o oficial, seção por seção; discordâncias são contadas e nenhuma seção é retirada.
D4. Regressão de Poisson: ligação identidade (taxa de erro por eleitor de cada grupo), sem intercepto, coeficientes
    não negativos, máxima verossimilhança (algoritmo EM), unidade = seção, sem peso. "Parte atribuída" ao regressor j
    = coeficiente j vezes a soma do regressor j, sobre a soma da contagem (as partes somam 1).
    Pureza (letra): contagem do código no 1º turno sobre L1, R1 e D1, com D1 = comparecimento - L1 - R1 - a própria
    contagem (todos os demais votos de presidente da seção: nominais em outros candidatos, brancos e os outros
    nulos). Lado previsto: 31 em L1; 32 e 52 em R1. Descarta se a parte for menor que 0,80 (estimativa pontual).
    Ao lado, sem decidir: intervalo percentil de 95% por bootstrap de municípios (1.000 réplicas); variante com
    D1 = só nominais em outros candidatos; variante com cinco regressores (L1, R1, votos do 55, demais nominais,
    brancos mais outros nulos).
    Correção do 52 (letra): contagem de 52 no 1º turno sobre R1 e votos do 55; f52 = parte atribuída a R1.
    N22_1 = n32_1 + f52 x n52_1; N22_2 = n32_2 + n52_2; N13_t = n31_t.
    Se um código for reprovado: 52 reprovado, N22_t = n32_t; 32 reprovado, N22_1 = f52 x n52_1 e N22_2 = n52_2; os
    dois reprovados ou o 31 reprovado, não há substituto (INCONCLUSIVO pela letra) e Theta com os três códigos é
    mostrado só como descritivo.
D5. Erro-padrão: bootstrap de municípios (UF e código do município; no exterior, a cidade), 2.000 réplicas, semente
    20261110; cada réplica refaz f52, P_t, W_t e Theta; erro = desvio-padrão das réplicas. Ao lado: bootstrap de
    seções (2.000) e a fórmula analítica raiz(1/N13_1 + 1/N22_1 + 1/N13_2 + 1/N22_2). Réplica com contagem zero em
    algum lado é descartada e contada.
D6. Etapa 2 (cega): imprime N13_1 e N22_1 (já expostos pela pureza), o total N13_2 + N22_2 do 2º turno sem separar
    lado nem código, o total de nulos com dígitos por turno e os erros-padrão. Nada mais que dependa da divisão por
    lado no 2º turno.
D7. Etapa 3: seções necessárias = n x (erro-padrão / 0,022)^2, arredondado para cima em blocos de 10 mil, teto de 60
    mil; projeção do erro em 6 mil, 10 mil, ..., 60 mil seções e no universo. Custo de download a 1 requisição por
    segundo: 2 requisições por seção e turno (o aux.json e o RDV; o voto oficial vem do bweb), 4 por seção;
    descontadas as seções já em disco (principal) e, à parte, as da extensão em curso. Ao lado, o custo com boletim
    junto (6 por seção) e o disco pelo tamanho médio do RDV.
D8. Etapa 4. Erro sistemático = o maior entre 0,015 e o valor absoluto do placebo de 2022. O placebo de 2022 não foi
    rodado (não há RDV de 2022 em disco; o desenho o põe na fase de download), então vale o piso de 0,015 e o erro
    total = raiz(erro-padrão^2 + 0,015^2) é um limite inferior. Veredito: SEM PODER se o erro total passar de 0,027
    (o limite do critério de sem sinal), qualquer que seja Theta; ao lado diz-se, condição por condição, o que a
    aritmética do critério de sinal e do de sem sinal daria. Dentro do limite: SINAL, SEM SINAL ou INCONCLUSIVO pela
    letra. Regiões: N (AC AM AP PA RO RR TO), NE (AL BA CE MA PB PE PI RN SE), SE (ES MG RJ SP), S (PR RS SC), CO (DF
    GO MS MT). Tercis de escolaridade: tercis nacionais da parcela do eleitorado da seção com superior completo
    (mesma definição e mesmo arquivo do teste A2, perfil de 14/07/2026), calculados sobre as seções do universo do
    2º turno com perfil; seção sem perfil fica fora dos tercis. Nos subgrupos f52 é o nacional e o erro sai do
    bootstrap de municípios dentro do subgrupo (1.000 réplicas). "Mesmo sinal" = sinal da estimativa pontual do
    subgrupo igual ao do Theta nacional.
D9. Leituras secundárias fixadas antes de abrir (não decidem): (a) Theta só com o 32 do lado do 22; (b) só com o 52
    corrigido; (c) sem a correção do 52 (f52 = 1); (d) taxas de erro por lado, a_t = N13_t / L_t e b_t = N22_t / R_t
    (Theta = ln(b_2/b_1) - ln(a_2/a_1): quanto a taxa de erro do lado do 22 subiu a mais que a do lado do 13);
    (e) só seções com a mesma urna e os mesmos aptos nos dois turnos; (f) validade em nível: seções em cinco grupos
    pelos quintis de P_t oficial da seção, inclinação de logit W sobre logit P entre os grupos, por turno, por
    mínimos quadrados ponderados (esperado 1 se a testemunha acompanha a intenção; abaixo de 1 mede impureza);
    (g) duas metades aleatórias da amostra (semente 20261110) e a diferença sobre o erro; (h) códigos de controle 00
    e 99: parcela nos nulos com dígitos, por turno.
    Motivo de (a) e (b), escrito antes: o 52 no 2º turno pode ganhar erros de quem votou 55 no 1º e passou a digitar
    22 (mistura dos dois números), o que inflaria N22_2 e empurraria Theta para cima sem alteração de contagem.
D10. Calibração por efeito plantado, nas tabelas da amostra (nunca nos arquivos), semente 20261110.
    A. Plantio na contagem oficial, com as testemunhas reais, 200 cópias cada:
       A1 troca de 3,57%: k ~ Binomial(R2, 0,0357) por seção, sai de R2 e entra em L2. Esperado pela fórmula do
          desenho: ln[(1 + p R2/L2) / (1 - p)] com os totais da amostra.
       A2 troca de 1,8% (meia dose).
       A3 acréscimo do tamanho da margem: k ~ Binomial(aptos2 - comparecimento2, 4.430.191 / 30.508.903) por seção,
          somado a L2 (30.508.903 = faltosos do 2º turno no país: 158.744.977 aptos menos 128.236.074). Esperado:
          ln(1 + soma de k / soma de L2).
       A4 espelhos: troca de 3,57% dos votos de Lula para Flávio; acréscimo da margem para Flávio.
       Em cada um: deslocamento médio de Theta, deslocamento sobre o erro-padrão e sobre o erro total, e o veredito
       que a letra daria no dado plantado.
    B. Simulação com testemunhas refeitas (distribuição amostral), 1.000 conjuntos por cenário: por seção e turno,
       n31 ~ Poisson(a31 x L), n32 ~ Poisson(b32 x R), n52 ~ Poisson(b52 x R + c55 x V55 [só no 1º turno]), com taxas
       por eleitor iguais nos dois turnos (a31 = (n31_1 + n31_2) / (L1 + L2); b32 igual com R; b52 = (f52 x n52_1 +
       n52_2) / (R1 + R2); c55 = (1 - f52) x n52_1 / soma de V55), aplicadas à "intenção":
       B0 nulo: intenção = contagem oficial.
       B1 troca que vira o resultado: a oficial é a verdadeira com 3,57% dos votos de Flávio trocados; intenção
          R2 = R2 / (1 - p), L2 = L2 - p R2 / (1 - p).
       B2 acréscimo: intenção L2 = L2 - 4.430.191 x (aptos2 - comparecimento2) / 30.508.903 (mínimo zero).
       B3 inocente, impureza: uma fração e da contagem de cada código não segue o lado (gerada proporcional ao
          comparecimento do turno, com taxa por eleitor igual nos dois turnos); e = 0,20 (a tolerância da letra) e
          e = o estimado na pureza.
       B4 inocente, conversão diferente: entre os que erram a tecla, os eleitores de eliminados se dividem 10 pontos
          mais para um lado: intenção L2 +/- 0,10 x O1 e R2 -/+ 0,10 x O1.
       Em cada um: média e desvio de Theta, fração dos conjuntos que cumpririam a aritmética de SINAL (Theta >= 0,045
       e >= 2,5 x erro total real) e a de SEM SINAL; e o poder projetado por aproximação normal em 6 mil, 35 mil,
       50 mil e 60 mil seções (erro-padrão vezes raiz(n0/n), sistemático 0,015), sem contar as condições de região e
       tercil (teto do poder).
    Regra (fixada aqui): o teste "enxerga o plantado" se, no cenário B1, a aritmética de SINAL for cumprida em pelo
    menos 80% dos conjuntos e o deslocamento plantado for de pelo menos 2,5 vezes o erro total. Senão, SEM PODER.
D11. Espelho: (i) os plantios em sentido contrário (A4); (ii) o critério espelhado no dado real (Theta de -0,045 ou
    menos e de -2,5 erros totais ou menos seria sinal a favor de Flávio); (iii) as duas metades.
D12. Tradução em votos de margem, com os totais nacionais do 2º turno (L = 64.256.232, R = 59.826.041): votos
    trocados equivalentes k = L R (e^Theta - 1) / (L + R e^Theta), efeito na margem 2k; acréscimo equivalente
    a = L (1 - e^(-Theta)). Para Theta e para Theta mais ou menos 1,96 x erro total (e x erro-padrão).
D13. Descritivos, abertos só na etapa 4 (a tabela mostra os códigos-testemunha do 2º turno): os 40 dígitos nulos mais
    frequentes de cada turno (contagem, parcela dos nulos com dígitos, por 10 mil votantes, rótulo). E os números dos
    11 eliminados (14, 16, 21, 27, 28, 29, 30, 35, 55, 70, 80) digitados como nulo no 2º turno: contagem, parcela dos
    nulos com dígitos, por 10 mil votantes, por 100 votos do próprio candidato no 1º turno nas mesmas seções, com
    erro por bootstrap de municípios; e a regressão de Poisson da contagem sobre os votos do próprio candidato no
    1º turno e sobre o resto do comparecimento do 2º turno (parte atribuída aos próprios eleitores).
D14. Tudo o que for feito depois de ver Theta e não estiver nesta lista é marcado EXPLORATÓRIO.
"""
import os as _os, sys as _sys
_sys.path.insert(0, _os.path.dirname(_os.path.abspath(__file__)))
import collections, glob, gzip, hashlib, json, math, os, sys, time
import numpy as np
from decodificar import ler_rdv
from lib import carregar

RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
TRAB = '/home/user/trabalho-eleicao/adendo27/R27_W4'
AAS = '/home/user/trabalho-eleicao/adendo27/aas'
REG = RAIZ + '/registro/adendo27'
PERFIL = '/home/user/trabalho-eleicao/adendo27/A2/perfil_secao_2026.json.gz'
SAIDA_JSON = RAIZ + '/resultados/R27_W4_nulos_de_digitacao.json'
SAIDA_TXT = RAIZ + '/resultados/R27_W4_nulos_de_digitacao.txt'
SEMENTE = 20261110
N_UNIVERSO = 499205
L_NAC, R_NAC = 64256232, 59826041
MARGEM = 4430191
FALTOSOS_2T = 158744977 - 128236074
P_TROCA = 0.0357
COD13, COD22 = ['31'], ['32', '52']
EXCLUIDOS = {'12': 'vizinho dos dois', '23': 'vizinho dos dois', '21': 'candidato do 1º turno',
             '16': 'candidato do 1º turno', '25': 'número de partido', '43': 'número de partido',
             '11': 'número de partido', '33': 'número de partido'}
ELIMINADOS = ['14', '16', '21', '27', '28', '29', '30', '35', '55', '70', '80']
PARTIDOS = {10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 25, 27, 28, 29, 30, 33, 35, 36, 40, 43, 44, 45, 50,
            51, 55, 65, 70, 77, 80, 90}
REGIOES = {'N': 'AC AM AP PA RO RR TO', 'NE': 'AL BA CE MA PB PE PI RN SE', 'SE': 'ES MG RJ SP', 'S': 'PR RS SC',
           'CO': 'DF GO MS MT'}
UF_REG = {u: r for r, us in REGIOES.items() for u in us.split()}
LIM_EP, LIM_ETOT, SIS_PISO = 0.022, 0.027, 0.015


def agora():
    return time.strftime('%Y-%m-%d %H:%M:%S UTC', time.gmtime())


def grava(nome, obj):
    os.makedirs(TRAB, exist_ok=True)
    p = os.path.join(TRAB, nome)
    with open(p + '.part', 'w') as f:
        json.dump(obj, f, ensure_ascii=False, indent=1)
    os.replace(p + '.part', p)


def le(nome):
    with open(os.path.join(TRAB, nome)) as f:
        return json.load(f)


# ---------------------------------------------------------------- leitura (sem resultado)
def pasta_secao(base, chave):
    uf, mun, zona, sec = chave.split('|')
    return os.path.join(base, uf.lower(), f'{int(mun):05d}', f'{int(zona):04d}', f'{int(sec):04d}')


def ler_um(base, chave):
    fs = sorted(glob.glob(pasta_secao(base, chave) + '/*-rdv.dat'))
    if not fs:
        return None
    c = ler_rdv(fs[-1])
    nom = collections.Counter(); nul = collections.Counter(); out = collections.Counter(); b = n6 = tot = 0
    for (ide, cod, tipo, dig), q in c.items():
        if cod != 1:
            continue
        tot += q
        if tipo == 2: nom[dig] += q
        elif tipo == 3: b += q
        elif tipo == 4: nul[dig] += q
        elif tipo == 6: n6 += q
        else: out[str(tipo)] += q
    return {'nom': dict(nom), 'B': b, 'nul': dict(nul), 'n6': n6, 'tot': tot, 'outros': dict(out), 'narq': len(fs),
            'bytes': os.path.getsize(fs[-1])}


def etapa_ler():
    os.makedirs(TRAB, exist_ok=True)
    listas = {'principal': [l.strip() for l in open(REG + '/amostra_aas_principal.txt') if l.strip()],
              'extensao': [l.strip() for l in open(REG + '/amostra_aas_extensao.txt') if l.strip()]}
    pastas = {'principal': (AAS + '/t1', AAS + '/t2'), 'extensao': (AAS + '/ext_t1', AAS + '/ext_t2')}
    rdv = {}; rel = {}
    for nome, chaves in listas.items():
        tem = [0, 0, 0]; multi = 0; erros = []
        for k in chaves:
            r = {}
            for t, base in zip('12', pastas[nome]):
                try:
                    x = ler_um(base, k)
                except Exception as e:  # arquivo ilegível: conta e segue
                    erros.append([k, t, repr(e)[:80]]); x = None
                if x is not None:
                    r[t] = x; tem[int(t) - 1] += 1; multi += x['narq'] > 1
            if len(r) == 2:
                tem[2] += 1
            if r:
                rdv[k] = dict(r, amostra=nome)
        rel[nome] = {'lista': len(chaves), 'com_rdv_1t': tem[0], 'com_rdv_2t': tem[1], 'com_os_dois': tem[2],
                     'pastas_com_mais_de_um_rdv': int(multi), 'ilegiveis': erros}
        print(nome, rel[nome], flush=True)
    with gzip.open(TRAB + '/rdv_nulos.json.gz', 'wt') as f:
        json.dump(rdv, f)
    # base oficial das seções das duas listas
    b26 = carregar(RAIZ + '/dados/secoes2026.json.gz')
    cand = carregar(RAIZ + '/dados/candidatos2026_1t.json.gz')['secoes']
    with gzip.open(PERFIL, 'rt') as f:
        pf = json.load(f)['secoes']
    sup_univ = []
    for k, v in b26.items():
        if '2' in v and k in pf and pf[k][0] > 0:
            sup_univ.append(pf[k][4] / pf[k][0])
    cortes = np.quantile(np.array(sup_univ), [1 / 3, 2 / 3]).tolist()
    base = {}
    for nome, chaves in listas.items():
        for k in chaves:
            v = b26.get(k, {})
            e = {'amostra': nome}
            for t in '12':
                if t in v:
                    e[t] = {c: v[t][c] for c in ('L', 'R', 'O', 'B', 'N', 'comp', 'apt', 'urna')}
            e['cand1'] = cand.get(k, {})
            if k in pf and pf[k][0] > 0:
                e['sup'] = pf[k][4] / pf[k][0]
            base[k] = e
    grava('base_oficial.json', {'secoes': base, 'cortes_tercil_superior_completo': cortes,
                                'secoes_do_universo_com_perfil': len(sup_univ), 'universo_2t': sum('2' in v for v in b26.values())})
    rel['cortes_tercil_superior_completo'] = cortes
    rel['quando'] = agora()
    grava('etapa0_leitura.json', rel)
    print('cortes do tercil (parcela com superior completo):', cortes, 'secoes com perfil:', len(sup_univ))


# ---------------------------------------------------------------- montagem das tabelas
def montar(ext=False):
    with gzip.open(TRAB + '/rdv_nulos.json.gz', 'rt') as f:
        rdv = json.load(f)
    bo = le('base_oficial.json')
    base, cortes = bo['secoes'], bo['cortes_tercil_superior_completo']
    ordem = [l.strip() for l in open(REG + '/amostra_aas_principal.txt') if l.strip()]
    if ext:
        ordem += [l.strip() for l in open(REG + '/amostra_aas_extensao.txt') if l.strip()]
    chaves = [k for k in ordem if k in rdv and '1' in rdv[k] and '2' in rdv[k] and '1' in base[k] and '2' in base[k]]
    n = len(chaves)
    D = {'chaves': chaves, 'n': n, 'n_principal': sum(base[k]['amostra'] == 'principal' for k in chaves),
         'n_extensao': sum(base[k]['amostra'] == 'extensao' for k in chaves)}
    D['uf'] = np.array([k.split('|')[0] for k in chaves])
    D['mun'] = np.array(['|'.join(k.split('|')[:2]) for k in chaves])
    D['reg'] = np.array([UF_REG.get(u, 'EX') for u in D['uf']])
    for t in '12':
        for c in ('L', 'R', 'O', 'B', 'N', 'comp', 'apt', 'urna'):
            D[c + t] = np.array([base[k][t][c] for k in chaves], dtype=float)
        D['nuld' + t] = np.array([sum(rdv[k][t]['nul'].values()) for k in chaves], dtype=float)
        D['n6_' + t] = np.array([rdv[k][t]['n6'] for k in chaves], dtype=float)
    for c in ELIMINADOS:
        D['V' + c] = np.array([base[k]['cand1'].get(c, 0) for k in chaves], dtype=float)
    sup = np.array([base[k].get('sup', np.nan) for k in chaves], dtype=float)
    D['sup'] = sup
    terc = np.full(n, -1)
    terc[~np.isnan(sup)] = np.digitize(sup[~np.isnan(sup)], cortes)
    D['terc'] = terc
    D['_rdv'] = rdv
    D['_base'] = base
    return D


def cont(D, cod, t):
    """Contagem por seção do nulo com dígitos `cod` no turno t."""
    rdv = D['_rdv']
    return np.array([rdv[k][t]['nul'].get(cod, 0) for k in D['chaves']], dtype=float)


def conferir_leitor(D):
    rdv, base = D['_rdv'], D['_base']
    r = {}
    for t in '12':
        dis = collections.Counter()
        for k in D['chaves']:
            x, o = rdv[k][t], base[k][t]
            nom = {int(a): b for a, b in x['nom'].items()}
            if nom.get(13, 0) != o['L']: dis['L'] += 1
            if nom.get(22, 0) != o['R']: dis['R'] += 1
            if sum(v for a, v in nom.items() if a not in (13, 22)) != o['O']: dis['O'] += 1
            if x['B'] != o['B']: dis['B'] += 1
            if sum(x['nul'].values()) + x['n6'] != o['N']: dis['N'] += 1
            if x['tot'] != o['comp']: dis['comparecimento'] += 1
            if x['outros']: dis['tipos_fora_de_2_3_4_6'] += 1
        r[t] = {c: int(dis.get(c, 0)) for c in ('L', 'R', 'O', 'B', 'N', 'comparecimento', 'tipos_fora_de_2_3_4_6')}
    return r


# ---------------------------------------------------------------- Poisson com ligação identidade (EM)
def poisson_em(y, X, it=200000, tol=1e-12):
    """Máxima verossimilhança de y ~ Poisson(X b), b >= 0. Devolve b, partes atribuídas, n usado."""
    y = np.asarray(y, float); X = np.asarray(X, float)
    ok = X.sum(1) > 0
    yy, XX = y[ok], X[ok]
    sx = XX.sum(0)
    k = X.shape[1]
    b = np.full(k, yy.sum() / max(sx.sum(), 1e-300))
    pos = yy > 0
    Xp, yp = XX[pos], yy[pos]
    for i in range(it):
        mu = np.maximum(Xp @ b, 1e-300)
        nb = b * (Xp.T @ (yp / mu)) / np.where(sx > 0, sx, 1.0)
        fim = np.max(np.abs(nb - b)) <= tol * max(nb.max(), 1e-300)
        b = nb
        if fim:
            break
    tot = y.sum()
    partes = (b * X.sum(0) / tot) if tot > 0 else np.full(k, np.nan)
    return b, partes, {'n': int(ok.sum()), 'contagem_total': float(tot), 'contagem_fora_da_regressao': float(y[~ok].sum()),
                       'iteracoes': i + 1}


def em_lote(y, X, W, it=4000):
    """O mesmo para B conjuntos de pesos W (B x n). Devolve as partes atribuídas (B x k)."""
    y = np.asarray(y, float); X = np.asarray(X, float)
    ok = X.sum(1) > 0
    Wo = W[:, ok]; Xo = X[ok]; yo = y[ok]
    sx = Wo @ Xo
    pos = yo > 0
    Xp = Xo[pos]; Wy = Wo[:, pos] * yo[pos]
    tot_reg = Wy.sum(1)
    b = np.repeat((tot_reg / np.maximum(sx.sum(1), 1e-300))[:, None], X.shape[1], 1)
    den = np.where(sx > 0, sx, 1.0)
    for i in range(it):
        mu = np.maximum(b @ Xp.T, 1e-300)
        nb = b * ((Wy / mu) @ Xp) / den
        if i % 25 == 0 and np.max(np.abs(nb - b) / np.maximum(nb.max(1, keepdims=True), 1e-300)) < 1e-10:
            b = nb; break
        b = nb
    tot = W @ y
    return b * (W @ X) / np.where(tot > 0, tot, np.nan)[:, None]


def em_lote_y(Y, X, it=3000):
    """O mesmo para S contagens simuladas Y (S x n), sem peso. Devolve as partes atribuídas (S x k)."""
    X = np.asarray(X, float)
    ok = X.sum(1) > 0
    Yo = Y[:, ok]; Xo = X[ok]
    sx = Xo.sum(0)
    b = np.repeat((Yo.sum(1) / sx.sum())[:, None], X.shape[1], 1)
    den = np.where(sx > 0, sx, 1.0)
    for i in range(it):
        mu = np.maximum(b @ Xo.T, 1e-300)
        nb = b * ((Yo / mu) @ Xo) / den
        if i % 25 == 0 and np.max(np.abs(nb - b) / np.maximum(nb.max(1, keepdims=True), 1e-300)) < 1e-9:
            b = nb; break
        b = nb
    tot = Y.sum(1)
    return b * X.sum(0) / np.where(tot > 0, tot, np.nan)[:, None]


def pesos_boot(grupos, B, rng):
    ug, gi = np.unique(grupos, return_inverse=True)
    G = len(ug)
    cnt = rng.multinomial(G, np.full(G, 1.0 / G), size=B)
    return cnt[:, gi].astype(float), G


# ---------------------------------------------------------------- Theta
COLS = ['L1', 'R1', 'L2', 'R2', 'n31_1', 'n32_1', 'n52_1', 'n31_2', 'n32_2', 'n52_2']


def tabela(D):
    T = {c: D[c] for c in ('L1', 'R1', 'L2', 'R2')}
    for cod in ('31', '32', '52'):
        for t in '12':
            T[f'n{cod}_{t}'] = cont(D, cod, t)
    return T


def theta_de(S, f52, usa):
    """S: dicionário de somas (escalares ou vetores). usa: códigos em uso. Devolve Theta e as peças."""
    z = np.zeros_like(np.asarray(S['L1'], float))
    N13_1 = S['n31_1'] + z; N13_2 = S['n31_2'] + z
    N22_1 = (S['n32_1'] if '32' in usa else 0) + (f52 * S['n52_1'] if '52' in usa else 0) + z
    N22_2 = (S['n32_2'] if '32' in usa else 0) + (S['n52_2'] if '52' in usa else 0) + z
    with np.errstate(divide='ignore', invalid='ignore'):
        dP = np.log(S['L2'] / S['R2']) - np.log(S['L1'] / S['R1'])
        dW = np.log(N13_2 / N22_2) - np.log(N13_1 / N22_1)
    return dP - dW, {'N13_1': N13_1, 'N22_1': N22_1, 'N13_2': N13_2, 'N22_2': N22_2, 'dP': dP, 'dW': dW}


def somas(T, mask=None):
    return {c: float(T[c].sum() if mask is None else T[c][mask].sum()) for c in COLS}


def f52_de(T, D, mask=None):
    m = slice(None) if mask is None else mask
    _, partes, info = poisson_em(T['n52_1'][m], np.column_stack([D['R1'][m], D['V55'][m]]))
    return float(partes[0]), partes, info


def boot_theta(T, D, grupos, B, rng, usa, mask=None, f52_fixo=None):
    idx = np.arange(D['n']) if mask is None else np.where(mask)[0]
    W, G = pesos_boot(grupos[idx], B, rng)
    Q = np.column_stack([T[c][idx] for c in COLS])
    Sb = W @ Q
    S = {c: Sb[:, j] for j, c in enumerate(COLS)}
    if f52_fixo is None and '52' in usa:
        f = em_lote(T['n52_1'][idx], np.column_stack([D['R1'][idx], D['V55'][idx]]), W)[:, 0]
    else:
        f = np.full(B, 1.0 if f52_fixo is None else f52_fixo)
    th, pe = theta_de(S, f, usa)
    bom = np.isfinite(th)
    return th[bom], int((~bom).sum()), G, f


def analitico(pe):
    v = sum(1.0 / pe[c] for c in ('N13_1', 'N22_1', 'N13_2', 'N22_2') if pe[c] > 0)
    return float(math.sqrt(v)) if all(pe[c] > 0 for c in ('N13_1', 'N22_1', 'N13_2', 'N22_2')) else float('nan')


def votos_de_margem(th):
    e = math.exp(th)
    k = L_NAC * R_NAC * (e - 1) / (L_NAC + R_NAC * e)
    return {'theta': th, 'votos_trocados_equivalentes': k, 'efeito_na_margem_por_troca': 2 * k,
            'fracao_da_margem_por_troca': 2 * k / MARGEM, 'acrescimo_equivalente': L_NAC * (1 - math.exp(-th)),
            'fracao_da_margem_por_acrescimo': L_NAC * (1 - math.exp(-th)) / MARGEM}


def phi(x):
    return 0.5 * (1 + math.erf(x / math.sqrt(2)))


# ---------------------------------------------------------------- etapa 1: pureza
def etapa_pureza(ext=False):
    D = montar(ext); T = tabela(D)
    rng = np.random.default_rng(SEMENTE + 1)
    R = {'quando': agora(), 'n_secoes': D['n'], 'n_principal': D['n_principal'], 'n_extensao': D['n_extensao'],
         'municipios': int(len(set(D['mun']))), 'conferencia_do_leitor_rdv_contra_oficial': conferir_leitor(D),
         'votos_1t': {c: float(D[c + '1'].sum()) for c in ('L', 'R', 'O', 'B', 'N', 'comp')},
         'nulos_com_digitos_1t': float(D['nuld1'].sum()), 'nulos_sem_digitos_1t': float(D['n6_1'].sum()), 'codigos': {}}
    W, G = pesos_boot(D['mun'], 1000, rng)
    L1, R1, O1, C1, V55 = D['L1'], D['R1'], D['O1'], D['comp1'], D['V55']
    for cod, lado in (('31', 0), ('32', 1), ('52', 1)):
        y = T[f'n{cod}_1']
        Dm = np.maximum(C1 - L1 - R1 - y, 0)
        X = np.column_stack([L1, R1, Dm])
        b, partes, info = poisson_em(y, X)
        pb = em_lote(y, X, W)
        ic = np.nanpercentile(pb[:, lado], [2.5, 97.5]).tolist()
        # variantes ao lado
        Xo = np.column_stack([L1, R1, O1])
        b2, p2, i2 = poisson_em(y, Xo)
        BNo = np.maximum(D['B1'] + D['N1'] - y, 0)
        X5 = np.column_stack([L1, R1, V55, np.maximum(O1 - V55, 0), BNo])
        b5, p5, i5 = poisson_em(y, X5)
        R['codigos'][cod] = {
            'lado_previsto': 'L1 (13)' if lado == 0 else 'R1 (22)', 'contagem_1t': float(y.sum()),
            'secoes_com_pelo_menos_um': int((y > 0).sum()), 'maximo_numa_secao': float(y.max()),
            'por_10_mil_votantes': float(1e4 * y.sum() / C1.sum()),
            'principal_L1_R1_demais': {'taxa_por_eleitor': dict(zip(['L1', 'R1', 'demais'], b.tolist())),
                                       'parte': dict(zip(['L1', 'R1', 'demais'], partes.tolist())), 'info': info,
                                       'parte_lado_previsto': float(partes[lado]), 'ic95_boot_municipios': ic,
                                       'ep_boot': float(np.nanstd(pb[:, lado], ddof=1))},
            'variante_demais_so_nominais': {'parte': dict(zip(['L1', 'R1', 'outros_nominais'], p2.tolist())),
                                            'parte_lado_previsto': float(p2[lado])},
            'variante_cinco_regressores': {'parte': dict(zip(['L1', 'R1', 'V55', 'demais_nominais', 'brancos_e_outros_nulos'], p5.tolist())),
                                           'taxa_por_eleitor': dict(zip(['L1', 'R1', 'V55', 'demais_nominais', 'brancos_e_outros_nulos'], b5.tolist())),
                                           'parte_lado_previsto': float(p5[lado])},
            'aprovado': bool(partes[lado] >= 0.80)}
    # correção do 52 (letra): R1 e votos do 55
    y = T['n52_1']
    f52, partes, info = f52_de(T, D)
    fb = em_lote(y, np.column_stack([R1, V55]), W)[:, 0]
    b52, _, _ = poisson_em(y, np.column_stack([R1, V55]))
    R['correcao_do_52'] = {'f52_parte_atribuida_a_R1': f52, 'parte_atribuida_ao_55': float(partes[1]),
                           'taxa_por_eleitor': {'R1': float(b52[0]), 'V55': float(b52[1])},
                           'ep_boot': float(np.nanstd(fb, ddof=1)), 'ic95_boot': np.nanpercentile(fb, [2.5, 97.5]).tolist(),
                           'info': info, 'votos_do_55_na_amostra': float(V55.sum())}
    ap = {c: R['codigos'][c]['aprovado'] for c in ('31', '32', '52')}
    if not ap['31'] or (not ap['32'] and not ap['52']):
        usa, sit = ['31', '32', '52'], 'REPROVADO SEM SUBSTITUTO (inconclusivo pela letra; Theta com os três códigos só como descritivo)'
    else:
        usa = ['31'] + [c for c in ('32', '52') if ap[c]]
        sit = 'aprovados: ' + ', '.join(usa) + ('' if len(usa) == 3 else '; descartado: ' + ', '.join(c for c in ('32', '52') if not ap[c]))
    R['codigos_em_uso'] = usa; R['situacao'] = sit
    R['sem_substituto'] = bool(not ap['31'] or (not ap['32'] and not ap['52']))
    grava('etapa1_pureza' + ('_ext' if ext else '') + '.json', R)
    print('ETAPA 1, PUREZA (1º turno), n =', D['n'], 'seções,', R['municipios'], 'municípios')
    print(' conferência RDV contra oficial (seções discordantes):', R['conferencia_do_leitor_rdv_contra_oficial'])
    for cod in ('31', '32', '52'):
        c = R['codigos'][cod]; p = c['principal_L1_R1_demais']
        print(f" código {cod}: contagem {c['contagem_1t']:.0f}, lado previsto {c['lado_previsto']}, partes "
              f"L1 {p['parte']['L1']:.3f} R1 {p['parte']['R1']:.3f} demais {p['parte']['demais']:.3f}; lado previsto "
              f"{p['parte_lado_previsto']:.3f} (ep {p['ep_boot']:.3f}; IC95 {p['ic95_boot_municipios'][0]:.3f} a {p['ic95_boot_municipios'][1]:.3f}) "
              f"{'APROVADO' if c['aprovado'] else 'REPROVADO'}; variantes: só nominais {c['variante_demais_so_nominais']['parte_lado_previsto']:.3f}, "
              f"cinco regressores {c['variante_cinco_regressores']['parte_lado_previsto']:.3f}")
    x = R['correcao_do_52']
    print(f" correção do 52: f52 = {x['f52_parte_atribuida_a_R1']:.3f} (ep {x['ep_boot']:.3f}); parte do 55 = {x['parte_atribuida_ao_55']:.3f}")
    print(' situação:', sit)
    return R


# ---------------------------------------------------------------- etapas 2 e 3: cego
def etapa_cego(ext=False):
    suf = '_ext' if ext else ''
    pz = le('etapa1_pureza' + suf + '.json')
    usa = pz['codigos_em_uso']
    D = montar(ext); T = tabela(D)
    f52, _, _ = f52_de(T, D)
    S = somas(T)
    th, pe = theta_de(S, f52, usa)          # calculado e NÃO impresso nem gravado nesta etapa
    rng = np.random.default_rng(SEMENTE)
    tb, ruins, G, _ = boot_theta(T, D, D['mun'], 2000, rng, usa)
    ep_mun = float(np.std(tb, ddof=1))
    ts, ruins_s, _, _ = boot_theta(T, D, np.arange(D['n']), 2000, np.random.default_rng(SEMENTE + 2), usa)
    ep_sec = float(np.std(ts, ddof=1))
    ep_an = analitico(pe)
    n = D['n']
    R = {'quando': agora(), 'n_secoes': n, 'n_principal': D['n_principal'], 'n_extensao': D['n_extensao'],
         'municipios': G, 'codigos_em_uso': usa, 'f52': f52,
         'testemunhas_1t': {'N13_1': float(pe['N13_1']), 'N22_1': float(pe['N22_1']), 'total': float(pe['N13_1'] + pe['N22_1']),
                            'n31': S['n31_1'], 'n32': S['n32_1'], 'n52_bruto': S['n52_1']},
         'testemunhas_2t_total_sem_separar_lado': float(pe['N13_2'] + pe['N22_2']),
         'votantes': {'1t': float(D['comp1'].sum()), '2t': float(D['comp2'].sum())},
         'nulos_com_digitos': {'1t': float(D['nuld1'].sum()), '2t': float(D['nuld2'].sum())},
         'erro_padrao': {'bootstrap_municipios_2000': ep_mun, 'bootstrap_secoes_2000': ep_sec, 'analitico': ep_an,
                         'replicas_descartadas': ruins},
         'theta': 'NÃO ABERTO NESTA ETAPA'}
    N1 = R['testemunhas_1t']['total']; N2 = R['testemunhas_2t_total_sem_separar_lado']
    R['testemunhas_por_10_mil_votantes'] = {'1t': 1e4 * N1 / R['votantes']['1t'], '2t': 1e4 * N2 / R['votantes']['2t']}
    R['testemunhas_no_universo_estimadas'] = {'1t': N1 / n * N_UNIVERSO, '2t': N2 / n * N_UNIVERSO}
    ep = ep_mun
    etot = math.sqrt(ep ** 2 + SIS_PISO ** 2)
    # etapa 3: regra de parada
    nec = n * (ep / LIM_EP) ** 2
    blocos = int(math.ceil(nec / 10000.0) * 10000)
    proj = {str(m): ep * math.sqrt(n / m) for m in (6000, 10000, 20000, 30000, 35000, 40000, 50000, 55000, 60000, N_UNIVERSO)}
    arq = [x for k in D['chaves'] for x in [D['_rdv'][k]]]
    by1 = float(np.mean([x['1']['bytes'] for x in arq])); by2 = float(np.mean([x['2']['bytes'] for x in arq]))

    def custo(m, ja):
        falta = max(m - ja, 0)
        return {'secoes_a_baixar': falta, 'requisicoes_so_rdv': 4 * falta, 'horas_so_rdv': 4 * falta / 3600.0,
                'dias_so_rdv': 4 * falta / 86400.0, 'requisicoes_com_boletim': 6 * falta, 'horas_com_boletim': 6 * falta / 3600.0,
                'disco_MB_rdv': falta * (by1 + by2) / 1e6}
    alvo = min(blocos, 60000)
    R['regra_de_parada'] = {
        'limite_ep': LIM_EP, 'ep_atual': ep, 'erro_total_atual_com_piso_sistematico': etot,
        'secoes_necessarias_exato': nec, 'secoes_necessarias_em_blocos_de_10_mil': blocos,
        'passa_do_teto_de_60_mil': bool(blocos > 60000), 'alvo': alvo, 'ep_projetado': proj,
        'ep_projetado_no_alvo': ep * math.sqrt(n / alvo),
        'erro_total_projetado_no_alvo': math.sqrt(ep ** 2 * n / alvo + SIS_PISO ** 2),
        'bytes_medios_rdv': {'1t': by1, '2t': by2},
        'custo_ate_o_alvo_descontando_a_principal': custo(alvo, 3000),
        'custo_ate_o_alvo_descontando_principal_e_extensao': custo(alvo, 6000),
        'custo_ate_60_mil_descontando_principal_e_extensao': custo(60000, 6000),
        'custo_do_placebo_2022_15_mil_secoes': {'requisicoes': 4 * 15000, 'horas': 4 * 15000 / 3600.0}}
    R['sem_poder_nesta_etapa'] = bool(etot > LIM_ETOT)
    grava('etapa2_3_cego' + suf + '.json', R)
    print('ETAPAS 2 E 3 (CEGAS), n =', n, 'seções,', G, 'municípios; códigos em uso', usa, f'f52 = {f52:.3f}')
    print(f" testemunhas 1º turno: N13 = {pe['N13_1']:.1f}, N22 = {pe['N22_1']:.1f}, total {N1:.1f} ({R['testemunhas_por_10_mil_votantes']['1t']:.2f} por 10 mil votantes)")
    print(f" testemunhas 2º turno: total {N2:.0f} ({R['testemunhas_por_10_mil_votantes']['2t']:.2f} por 10 mil votantes), sem separar lado")
    print(f" erro-padrão de Theta: bootstrap de municípios {ep_mun:.4f}; de seções {ep_sec:.4f}; analítico {ep_an:.4f}; réplicas descartadas {ruins}")
    print(f" erro total com piso sistemático 0,015: {etot:.4f} (limite 0,027) -> {'SEM PODER nesta etapa' if etot > LIM_ETOT else 'dentro do limite'}")
    print(f" regra de parada: {nec:.0f} seções para o erro chegar a 0,022; em blocos de 10 mil: {blocos}; alvo {alvo}")
    print('  projeção do erro-padrão:', {k: round(v, 4) for k, v in proj.items()})
    for k in ('custo_ate_o_alvo_descontando_a_principal', 'custo_ate_o_alvo_descontando_principal_e_extensao', 'custo_ate_60_mil_descontando_principal_e_extensao'):
        c = R['regra_de_parada'][k]
        print(f"  {k}: {c['secoes_a_baixar']} seções, {c['requisicoes_so_rdv']} requisições, {c['horas_so_rdv']:.1f} h ({c['dias_so_rdv']:.2f} dias), {c['disco_MB_rdv']:.0f} MB")
    return R


# ---------------------------------------------------------------- etapa 4: abrir
def veredito_letra(th, ep, sis, n_reg_mesmo_sinal, n_terc_mesmo_sinal, sem_substituto):
    etot = math.sqrt(ep ** 2 + sis ** 2)
    c = {'theta_ge_0045': bool(th >= 0.045), 'theta_ge_2e5_erro_total': bool(th >= 2.5 * etot),
         'regioes_mesmo_sinal_ge_4': bool(n_reg_mesmo_sinal >= 4), 'tercis_mesmo_sinal_3': bool(n_terc_mesmo_sinal == 3),
         'abs_theta_le_0020': bool(abs(th) <= 0.020), 'erro_total_le_0027': bool(etot <= LIM_ETOT),
         'ep_le_0022': bool(ep <= LIM_EP), 'pureza_com_substituto': bool(not sem_substituto)}
    sinal = c['theta_ge_0045'] and c['theta_ge_2e5_erro_total'] and c['regioes_mesmo_sinal_ge_4'] and c['tercis_mesmo_sinal_3']
    sem = c['abs_theta_le_0020'] and c['erro_total_le_0027']
    if etot > LIM_ETOT:
        v = 'SEM PODER'
    elif sem_substituto:
        v = 'INCONCLUSIVO'
    elif sinal:
        v = 'SINAL'
    elif sem:
        v = 'SEM SINAL'
    else:
        v = 'INCONCLUSIVO'
    return v, etot, c, bool(sinal), bool(sem)


def rotulo(dig):
    if dig in COD13: return 'testemunha do 13 (dígitos invertidos)'
    if dig in COD22: return 'testemunha do 22 (tecla vizinha no 1º dígito)'
    if dig in EXCLUIDOS: return 'excluído de antemão: ' + EXCLUIDOS[dig]
    if dig in ('13', '22'): return 'número de finalista'
    if dig in ELIMINADOS: return 'número de candidato do 1º turno (eliminado)'
    if dig in ('00', '99'): return 'código de controle'
    if dig.isdigit() and int(dig) in PARTIDOS: return 'número de partido'
    return ''


def etapa_abrir(ext=False):
    suf = '_ext' if ext else ''
    pz = le('etapa1_pureza' + suf + '.json'); cg = le('etapa2_3_cego' + suf + '.json')
    usa = pz['codigos_em_uso']
    D = montar(ext); T = tabela(D); n = D['n']
    assert cg['n_secoes'] == n and pz['n_secoes'] == n, 'as etapas cegas foram feitas com outro conjunto de seções'
    f52, _, _ = f52_de(T, D)
    S = somas(T)
    th, pe = theta_de(S, f52, usa); th = float(th)
    ep = cg['erro_padrao']['bootstrap_municipios_2000']
    rng = np.random.default_rng(SEMENTE)
    tb, ruins, G, fb = boot_theta(T, D, D['mun'], 2000, rng, usa)
    assert abs(float(np.std(tb, ddof=1)) - ep) < 1e-12, 'o erro-padrão não reproduz o da etapa cega'
    R = {'quando': agora(), 'n_secoes': n, 'n_principal': D['n_principal'], 'n_extensao': D['n_extensao'], 'municipios': G,
         'codigos_em_uso': usa, 'f52': f52}
    P1 = S['L1'] / (S['L1'] + S['R1']); P2 = S['L2'] / (S['L2'] + S['R2'])
    W1 = float(pe['N13_1'] / (pe['N13_1'] + pe['N22_1'])); W2 = float(pe['N13_2'] / (pe['N13_2'] + pe['N22_2']))
    R['bruto_2026'] = {
        'oficial': {'L1': S['L1'], 'R1': S['R1'], 'L2': S['L2'], 'R2': S['R2'], 'P1': P1, 'P2': P2,
                    'logit_P1': math.log(S['L1'] / S['R1']), 'logit_P2': math.log(S['L2'] / S['R2']), 'delta_logit_P': float(pe['dP'])},
        'testemunhas': {'n31_1': S['n31_1'], 'n32_1': S['n32_1'], 'n52_1_bruto': S['n52_1'], 'n31_2': S['n31_2'], 'n32_2': S['n32_2'],
                        'n52_2': S['n52_2'], 'N13_1': float(pe['N13_1']), 'N22_1': float(pe['N22_1']), 'N13_2': float(pe['N13_2']),
                        'N22_2': float(pe['N22_2']), 'W1': W1, 'W2': W2,
                        'logit_W1': math.log(pe['N13_1'] / pe['N22_1']), 'logit_W2': math.log(pe['N13_2'] / pe['N22_2']),
                        'delta_logit_W': float(pe['dW'])},
        'taxas_por_10_mil_eleitores_do_lado': {'a1_13': 1e4 * pe['N13_1'] / S['L1'], 'a2_13': 1e4 * pe['N13_2'] / S['L2'],
                                               'b1_22': 1e4 * pe['N22_1'] / S['R1'], 'b2_22': 1e4 * pe['N22_2'] / S['R2'],
                                               'ln_a2_sobre_a1': math.log((pe['N13_2'] / S['L2']) / (pe['N13_1'] / S['L1'])),
                                               'ln_b2_sobre_b1': math.log((pe['N22_2'] / S['R2']) / (pe['N22_1'] / S['R1']))}}
    R['theta'] = th
    R['erro_padrao'] = cg['erro_padrao']
    R['ic95_percentil_boot'] = np.percentile(tb, [2.5, 97.5]).tolist()
    # regiões e tercis
    sub = {}
    for nome, mask in [(r, D['reg'] == r) for r in REGIOES] + [(f'tercil_{i+1}', D['terc'] == i) for i in range(3)] + \
                      [('exterior', D['reg'] == 'EX'), ('sem_perfil', D['terc'] == -1)]:
        Sg = somas(T, mask); tg, pg = theta_de(Sg, f52, usa)
        e = {'n': int(mask.sum()), 'N13_1': float(pg['N13_1']), 'N22_1': float(pg['N22_1']), 'N13_2': float(pg['N13_2']),
             'N22_2': float(pg['N22_2']), 'delta_logit_P': float(pg['dP']) if np.isfinite(pg['dP']) else None,
             'theta': float(tg) if np.isfinite(tg) else None}
        if e['theta'] is not None and mask.sum() >= 20:
            tgb, rg, Gg, _ = boot_theta(T, D, D['mun'], 1000, np.random.default_rng(SEMENTE + 10 + len(sub)), usa, mask=mask, f52_fixo=f52)
            e.update(ep=float(np.std(tgb, ddof=1)), replicas_descartadas=rg, municipios=Gg, ep_analitico=analitico(pg))
        sub[nome] = e
    R['subgrupos'] = sub
    sg = 1 if th >= 0 else -1
    nreg = sum(1 for r in REGIOES if sub[r]['theta'] is not None and (sub[r]['theta'] >= 0) == (sg > 0))
    nter = sum(1 for i in range(3) if sub[f'tercil_{i+1}']['theta'] is not None and (sub[f'tercil_{i+1}']['theta'] >= 0) == (sg > 0))
    v, etot, cond, sinal_arit, sem_arit = veredito_letra(th, ep, SIS_PISO, nreg, nter, pz['sem_substituto'])
    R['erro_sistematico'] = {'valor': SIS_PISO, 'nota': 'piso do registro; o placebo de 2022 não foi rodado nesta etapa'}
    R['erro_total'] = etot
    R['criterio'] = {'veredito_pela_letra': v, 'condicoes': cond, 'regioes_com_o_mesmo_sinal': nreg, 'tercis_com_o_mesmo_sinal': nter,
                     'aritmetica_de_sinal_cumprida': sinal_arit, 'aritmetica_de_sem_sinal_cumprida': sem_arit,
                     'theta_sobre_ep': th / ep, 'theta_sobre_erro_total': th / etot,
                     'limiar_de_sinal_com_este_erro': max(0.045, 2.5 * etot),
                     'espelho_theta_le_menos_0045_e_menos_2e5_erro': bool(th <= -0.045 and th <= -2.5 * etot)}
    # leituras secundárias (D9)
    sec = {}
    for nome, u, f in (('a_so_32', ['31', '32'], f52), ('b_so_52_corrigido', ['31', '52'], f52), ('c_sem_correcao_do_52', ['31', '32', '52'], 1.0)):
        t2, p2 = theta_de(S, f, u)
        tb2, r2, _, _ = boot_theta(T, D, D['mun'], 2000, np.random.default_rng(SEMENTE), u, f52_fixo=(1.0 if nome.startswith('c') else None))
        sec[nome] = {'theta': float(t2), 'ep': float(np.std(tb2, ddof=1)), 'N22_1': float(p2['N22_1']), 'N22_2': float(p2['N22_2']),
                     'ep_analitico': analitico(p2)}
    # diferença entre só 32 e só 52, com o erro da diferença no mesmo bootstrap
    ta, _, _, _ = boot_theta(T, D, D['mun'], 2000, np.random.default_rng(SEMENTE), ['31', '32'])
    tb5, _, _, _ = boot_theta(T, D, D['mun'], 2000, np.random.default_rng(SEMENTE), ['31', '52'])
    if len(ta) == len(tb5):
        sec['diferenca_so52_menos_so32'] = {'valor': sec['b_so_52_corrigido']['theta'] - sec['a_so_32']['theta'],
                                           'ep': float(np.std(tb5 - ta, ddof=1))}
    mesma = (D['urna1'] == D['urna2']) & (D['apt1'] == D['apt2'])
    Sm = somas(T, mesma); f52m, _, _ = f52_de(T, D, mesma); tm, pm = theta_de(Sm, f52m, usa)
    tbm, _, _, _ = boot_theta(T, D, D['mun'], 1000, np.random.default_rng(SEMENTE + 3), usa, mask=mesma)
    sec['e_mesma_urna_e_mesmos_aptos'] = {'n': int(mesma.sum()), 'theta': float(tm), 'ep': float(np.std(tbm, ddof=1))}
    # (f) validade em nível
    val = {}
    for t in '12':
        Lt, Rt = D['L' + t], D['R' + t]
        okp = (Lt + Rt) > 0
        p = np.where(okp, Lt / np.maximum(Lt + Rt, 1), np.nan)
        q = np.nanquantile(p, [0.2, 0.4, 0.6, 0.8])
        g = np.digitize(p, q); g[~okp] = -1
        xs, ys, ws, linhas = [], [], [], []
        for j in range(5):
            m = g == j
            n13 = T[f'n31_{t}'][m].sum()
            n22 = (T[f'n32_{t}'][m].sum() if '32' in usa else 0) + ((f52 if t == '1' else 1.0) * T[f'n52_{t}'][m].sum() if '52' in usa else 0)
            lp = math.log(Lt[m].sum() / Rt[m].sum())
            lw = math.log(n13 / n22) if n13 > 0 and n22 > 0 else None
            linhas.append({'grupo': j + 1, 'n': int(m.sum()), 'P_oficial': float(Lt[m].sum() / (Lt[m].sum() + Rt[m].sum())), 'logit_P': lp,
                           'N13': float(n13), 'N22': float(n22), 'W': float(n13 / (n13 + n22)) if n13 + n22 > 0 else None, 'logit_W': lw})
            if lw is not None:
                xs.append(lp); ys.append(lw); ws.append(1.0 / (1.0 / n13 + 1.0 / n22))
        xs, ys, ws = np.array(xs), np.array(ys), np.array(ws)
        xm = (ws * xs).sum() / ws.sum(); ym = (ws * ys).sum() / ws.sum()
        sxx = (ws * (xs - xm) ** 2).sum()
        incl = float((ws * (xs - xm) * (ys - ym)).sum() / sxx)
        val[t] = {'grupos': linhas, 'inclinacao': incl, 'ep_inclinacao': float(1.0 / math.sqrt(sxx)), 'intercepto_no_centro': float(ym - incl * 0),
                  'cortes_quintis_P': q.tolist()}
    sec['f_validade_em_nivel'] = val
    # (g) metades
    perm = np.random.default_rng(SEMENTE).permutation(n)
    h = np.zeros(n, bool); h[perm[: n // 2]] = True
    met = []
    for m in (h, ~h):
        Sg = somas(T, m); tg, pg = theta_de(Sg, f52, usa)
        tgb, _, _, _ = boot_theta(T, D, D['mun'], 1000, np.random.default_rng(SEMENTE + 5 + len(met)), usa, mask=m, f52_fixo=f52)
        met.append({'n': int(m.sum()), 'theta': float(tg), 'ep': float(np.std(tgb, ddof=1)), 'ep_analitico': analitico(pg)})
    dif = met[0]['theta'] - met[1]['theta']; epd = math.sqrt(met[0]['ep'] ** 2 + met[1]['ep'] ** 2)
    sec['g_metades'] = {'metades': met, 'diferenca': dif, 'ep_da_diferenca': epd, 'z': dif / epd}
    # (h) controles 00 e 99
    ctrl = {}
    for cod in ('00', '99'):
        ctrl[cod] = {}
        for t in '12':
            y = cont(D, cod, t)
            Wb, _ = pesos_boot(D['mun'], 1000, np.random.default_rng(SEMENTE + 7))
            fr = (Wb @ y) / (Wb @ D['nuld' + t])
            ctrl[cod][t] = {'contagem': float(y.sum()), 'parcela_dos_nulos_com_digitos': float(y.sum() / D['nuld' + t].sum()),
                            'ep': float(np.std(fr, ddof=1)), 'por_10_mil_votantes': float(1e4 * y.sum() / D['comp' + t].sum())}
    sec['h_controles_00_99'] = ctrl
    R['leituras_secundarias'] = sec
    grava('etapa4_parcial_theta' + suf + '.json', R)

    # ------------------------------------------------ calibração A: plantio na contagem oficial
    rng = np.random.default_rng(SEMENTE + 20)
    L2, R2 = D['L2'].astype(np.int64), D['R2'].astype(np.int64)
    falt = np.maximum(D['apt2'] - D['comp2'], 0).astype(np.int64)
    calA = {}

    def planta(nome, fn, esperado):
        ds = []; vs = collections.Counter()
        for i in range(200):
            l2, r2 = fn()
            Sp = dict(S, L2=float(l2.sum()), R2=float(r2.sum()))
            tp, _ = theta_de(Sp, f52, usa); tp = float(tp)
            ds.append(tp - th)
            vv, _, _, _, _ = veredito_letra(tp, ep, SIS_PISO, nreg, nter, pz['sem_substituto'])
            vs[vv] += 1
        d = float(np.mean(ds))
        calA[nome] = {'deslocamento_medio': d, 'dp_entre_copias': float(np.std(ds, ddof=1)), 'esperado_pela_formula': esperado,
                      'deslocamento_sobre_ep': d / ep, 'deslocamento_sobre_erro_total': d / etot,
                      'theta_plantado_medio': th + d, 'veredito_no_dado_plantado': dict(vs),
                      'aritmetica_de_sinal_no_plantado_medio': bool(th + d >= 0.045 and th + d >= 2.5 * etot),
                      'enxerga_a_2e5_erros': bool(abs(d) >= 2.5 * etot)}

    def troca(p, de='R'):
        def f():
            if de == 'R':
                k = rng.binomial(R2, p); return L2 + k, R2 - k
            k = rng.binomial(L2, p); return L2 - k, R2 + k
        return f

    def acresc(para='L'):
        def f():
            k = rng.binomial(falt, MARGEM / FALTOSOS_2T)
            return (L2 + k, R2) if para == 'L' else (L2, R2 + k)
        return f
    planta('A1_troca_3e57', troca(P_TROCA), math.log((1 + P_TROCA * S['R2'] / S['L2']) / (1 - P_TROCA)))
    planta('A2_troca_1e8', troca(0.018), math.log((1 + 0.018 * S['R2'] / S['L2']) / (1 - 0.018)))
    kesp = float(falt.sum()) * MARGEM / FALTOSOS_2T
    planta('A3_acrescimo_da_margem_para_Lula', acresc('L'), math.log(1 + kesp / S['L2']))
    planta('A4_espelho_troca_3e57_de_Lula_para_Flavio', troca(P_TROCA, 'L'), -math.log((1 + P_TROCA * S['L2'] / S['R2']) / (1 - P_TROCA)))
    planta('A4_espelho_acrescimo_da_margem_para_Flavio', acresc('R'), -math.log(1 + kesp / S['R2']))
    calA['nota'] = ('acréscimo esperado na amostra: %.0f votos (%.0f por seção); no país 4.430.191. Fórmula nacional da troca: %.4f; do acréscimo sobre o oficial: %.4f; '
                    'do acréscimo visto pela testemunha (ln de L oficial sobre L verdadeiro): %.4f'
                    % (kesp, kesp / n, math.log((1 + P_TROCA * R_NAC / L_NAC) / (1 - P_TROCA)), math.log(1 + MARGEM / L_NAC), math.log(L_NAC / (L_NAC - MARGEM))))
    R['calibracao_A_plantio_na_contagem_oficial'] = calA
    grava('etapa4_parcial_calA' + suf + '.json', calA)

    # ------------------------------------------------ calibração B: testemunhas refeitas
    rngB = np.random.default_rng(SEMENTE + 30)
    L1v, R1v, L2v, R2v, O1v, V55 = D['L1'], D['R1'], D['L2'], D['R2'], D['O1'], D['V55']
    C1, C2 = D['comp1'], D['comp2']
    a31 = (S['n31_1'] + S['n31_2']) / (S['L1'] + S['L2'])
    b32 = (S['n32_1'] + S['n32_2']) / (S['R1'] + S['R2'])
    b52 = (f52 * S['n52_1'] + S['n52_2']) / (S['R1'] + S['R2'])
    c55 = (1 - f52) * S['n52_1'] / max(V55.sum(), 1)
    NS = 1000
    pur = pz['codigos']
    e_est = {'31': max(0.0, 1 - pur['31']['principal_L1_R1_demais']['parte_lado_previsto']),
             '32': max(0.0, 1 - pur['32']['principal_L1_R1_demais']['parte_lado_previsto']),
             '52': max(0.0, 1 - pur['52']['variante_cinco_regressores']['parte']['R1'] - pur['52']['variante_cinco_regressores']['parte']['V55'])}
    XR = np.column_stack([R1v, V55])

    def simula(nome, Li2, Ri2, eps=None):
        eps = eps or {'31': 0.0, '32': 0.0, '52': 0.0}
        tot_side = {'31': S['L1'] + S['L2'], '32': S['R1'] + S['R2'], '52': S['R1'] + S['R2']}
        taxa = {'31': a31, '32': b32, '52': b52}
        lam = {}
        for cod, lado1, lado2 in (('31', L1v, Li2), ('32', R1v, Ri2), ('52', R1v, Ri2)):
            rho = eps[cod] * taxa[cod] * tot_side[cod] / (C1.sum() + C2.sum())
            lam[cod + '_1'] = (1 - eps[cod]) * taxa[cod] * lado1 + rho * C1
            lam[cod + '_2'] = (1 - eps[cod]) * taxa[cod] * lado2 + rho * C2
        lam['52_1'] = lam['52_1'] + c55 * V55
        Y = {k: rngB.poisson(np.maximum(v, 0), size=(NS, n)).astype(float) for k, v in lam.items()}
        fs = em_lote_y(Y['52_1'], XR)[:, 0] if '52' in usa else np.ones(NS)
        Ss = {'L1': S['L1'], 'R1': S['R1'], 'L2': S['L2'], 'R2': S['R2'], 'n31_1': Y['31_1'].sum(1), 'n32_1': Y['32_1'].sum(1),
              'n52_1': Y['52_1'].sum(1), 'n31_2': Y['31_2'].sum(1), 'n32_2': Y['32_2'].sum(1), 'n52_2': Y['52_2'].sum(1)}
        ths, _ = theta_de(Ss, fs, usa)
        ths = ths[np.isfinite(ths)]
        # esperado sem ruído
        Se = dict(Ss); f_e = f52
        for k in ('31_1', '32_1', '52_1', '31_2', '32_2', '52_2'):
            Se['n' + k] = float(lam[k].sum())
        f_e = float((1 - eps['52']) * b52 * S['R1'] + eps['52'] * b52 * (S['R1'] + S['R2']) / (C1.sum() + C2.sum()) * C1.sum()) / Se['n52_1'] if eps['52'] == 0 else float(np.nanmean(fs))
        te, _ = theta_de(Se, f_e, usa)
        lim = max(0.045, 2.5 * etot)
        m, sd = float(np.mean(ths)), float(np.std(ths, ddof=1))
        proj = {}
        for nn in (n, 6000, 35000, 50000, 60000):
            epn = ep * math.sqrt(n / nn); etn = math.sqrt(epn ** 2 + SIS_PISO ** 2); limn = max(0.045, 2.5 * etn)
            proj[str(nn)] = {'ep': epn, 'erro_total': etn, 'limiar_de_sinal': limn,
                             'prob_aritmetica_de_sinal': 1 - phi((limn - m) / epn),
                             'prob_aritmetica_de_sem_sinal': (phi((0.020 - m) / epn) - phi((-0.020 - m) / epn)) if etn <= LIM_ETOT else 0.0}
        return {'conjuntos': int(len(ths)), 'theta_medio': m, 'dp_de_theta': sd, 'ep_da_media': sd / math.sqrt(len(ths)),
                'theta_esperado_sem_ruido': float(te), 'f52_medio': float(np.nanmean(fs)),
                'fracao_aritmetica_de_sinal_com_o_erro_real': float(np.mean((ths >= lim))),
                'fracao_aritmetica_de_sinal_espelhada': float(np.mean((ths <= -lim))),
                'fracao_aritmetica_de_sem_sinal': float(np.mean(np.abs(ths) <= 0.020)) if etot <= LIM_ETOT else 0.0,
                'fracao_abs_theta_le_0020_ignorando_o_erro': float(np.mean(np.abs(ths) <= 0.020)),
                'projecao_normal': proj}
    calB = {'taxas_por_10_mil': {'a31': 1e4 * a31, 'b32': 1e4 * b32, 'b52': 1e4 * b52, 'c55': 1e4 * c55}, 'impureza_estimada': e_est}
    calB['B0_nulo'] = simula('B0', L2v, R2v); grava('etapa4_parcial_calB' + suf + '.json', calB)
    calB['B1_troca_que_vira'] = simula('B1', L2v - P_TROCA * R2v / (1 - P_TROCA), R2v / (1 - P_TROCA)); grava('etapa4_parcial_calB' + suf + '.json', calB)
    calB['B2_acrescimo_da_margem'] = simula('B2', np.maximum(L2v - MARGEM * falt / FALTOSOS_2T, 0), R2v); grava('etapa4_parcial_calB' + suf + '.json', calB)
    calB['B3_inocente_impureza_020'] = simula('B3a', L2v, R2v, {'31': 0.2, '32': 0.2, '52': 0.2})
    calB['B3_inocente_impureza_estimada'] = simula('B3b', L2v, R2v, e_est); grava('etapa4_parcial_calB' + suf + '.json', calB)
    calB['B4_inocente_eliminados_10_pontos_a_mais_para_Lula'] = simula('B4a', L2v + 0.10 * O1v, np.maximum(R2v - 0.10 * O1v, 0))
    calB['B4_inocente_eliminados_10_pontos_a_mais_para_Flavio'] = simula('B4b', np.maximum(L2v - 0.10 * O1v, 0), R2v + 0.10 * O1v)
    b1 = calB['B1_troca_que_vira']
    calB['enxerga_o_plantado'] = bool(b1['fracao_aritmetica_de_sinal_com_o_erro_real'] >= 0.80 and
                                      calA['A1_troca_3e57']['deslocamento_medio'] >= 2.5 * etot)
    R['calibracao_B_testemunhas_refeitas'] = calB
    grava('etapa4_parcial_calB' + suf + '.json', calB)
    if not calB['enxerga_o_plantado'] and v != 'SEM PODER':
        R['criterio']['veredito_pela_letra_antes_da_calibracao'] = v
        v = 'SEM PODER'; R['criterio']['veredito_pela_letra'] = v
    R['criterio']['enxerga_o_plantado'] = calB['enxerga_o_plantado']

    # ------------------------------------------------ tradução em votos
    R['votos_de_margem'] = {'theta': votos_de_margem(th), 'theta_menos_196_erro_total': votos_de_margem(th - 1.96 * etot),
                            'theta_mais_196_erro_total': votos_de_margem(th + 1.96 * etot),
                            'theta_menos_196_ep': votos_de_margem(th - 1.96 * ep), 'theta_mais_196_ep': votos_de_margem(th + 1.96 * ep),
                            'referencia_troca_que_vira': votos_de_margem(math.log((1 + P_TROCA * R_NAC / L_NAC) / (1 - P_TROCA))),
                            'menor_efeito_que_a_aritmetica_de_sinal_alcanca': votos_de_margem(max(0.045, 2.5 * etot))}

    # ------------------------------------------------ descritivos (D13)
    rdv = D['_rdv']
    desc = {}
    for t in '12':
        c = collections.Counter()
        for k in D['chaves']:
            c.update(rdv[k][t]['nul'])
        tot = sum(c.values()); comp = D['comp' + t].sum()
        desc[t] = {'nulos_com_digitos': tot, 'nulos_sem_digitos': float(D['n6_' + t].sum()), 'brancos': float(D['B' + t].sum()),
                   'votantes': float(comp), 'codigos_distintos': len(c),
                   'tabela': [{'digitos': d, 'contagem': q, 'parcela_dos_nulos_com_digitos': q / tot, 'por_10_mil_votantes': 1e4 * q / comp,
                               'rotulo': rotulo(d)} for d, q in c.most_common(40)],
                   'todos': dict(c)}
    R['descritivo_digitos_nulos'] = desc
    Wb, _ = pesos_boot(D['mun'], 1000, np.random.default_rng(SEMENTE + 40))
    el = {}
    tot2 = D['nuld2'].sum()
    soma_y = np.zeros(n)
    for cod in ELIMINADOS:
        y2 = cont(D, cod, '2'); y1 = cont(D, cod, '1'); V = D['V' + cod]
        soma_y += y2
        e = {'contagem_2t': float(y2.sum()), 'contagem_como_nulo_no_1t': float(y1.sum()), 'votos_do_candidato_1t_na_amostra': float(V.sum()),
             'parcela_dos_nulos_com_digitos_2t': float(y2.sum() / tot2), 'ep_parcela': float(np.std((Wb @ y2) / (Wb @ D['nuld2']), ddof=1)),
             'por_10_mil_votantes_2t': float(1e4 * y2.sum() / C2.sum()),
             'por_100_votos_do_proprio_candidato_no_1t': float(100 * y2.sum() / V.sum()) if V.sum() > 0 else None}
        if V.sum() > 0:
            rr = 100 * (Wb @ y2) / np.maximum(Wb @ V, 1e-9)
            e['ep_por_100_votos'] = float(np.std(rr, ddof=1))
        if y2.sum() >= 20 and V.sum() > 0:
            b, partes, info = poisson_em(y2, np.column_stack([V, np.maximum(C2 - y2, 0)]))
            e['poisson_parte_atribuida_aos_proprios_eleitores'] = float(partes[0])
            e['poisson_taxa_por_100_eleitores_proprios'] = float(100 * b[0])
            e['poisson_taxa_de_fundo_por_10_mil_votantes'] = float(1e4 * b[1])
        el[cod] = e
    Vt = sum(D['V' + c] for c in ELIMINADOS)
    el['todos_os_11'] = {'contagem_2t': float(soma_y.sum()), 'parcela_dos_nulos_com_digitos_2t': float(soma_y.sum() / tot2),
                         'ep_parcela': float(np.std((Wb @ soma_y) / (Wb @ D['nuld2']), ddof=1)),
                         'por_10_mil_votantes_2t': float(1e4 * soma_y.sum() / C2.sum()),
                         'por_100_votos_de_eliminados_no_1t': float(100 * soma_y.sum() / Vt.sum()),
                         'ep_por_100_votos': float(np.std(100 * (Wb @ soma_y) / (Wb @ Vt), ddof=1)),
                         'estimativa_no_pais': float(soma_y.sum() / n * N_UNIVERSO)}
    for cod in ('13', '22'):
        y2 = cont(D, cod, '2'); y1 = cont(D, cod, '1')
        el['finalista_' + cod + '_digitado_como_nulo'] = {'1t': float(y1.sum()), '2t': float(y2.sum())}
    R['descritivo_eliminados_digitados_no_2t'] = el
    R['etapa1_pureza'] = pz; R['etapas_2_3_cego'] = cg
    grava('etapa4_tudo' + suf + '.json', R)
    return R, D


# ---------------------------------------------------------------- relatório
def fm(x, d=4):
    if x is None or (isinstance(x, float) and not math.isfinite(x)):
        return 'n/d'
    return f'{x:+.{d}f}'


def mil(x):
    return f'{x:,.0f}'.replace(',', '.')


def relatorio(R, ext=False):
    pz, cg = R['etapa1_pureza'], R['etapas_2_3_cego']
    L = []
    P = L.append
    n = R['n_secoes']
    P('R27_W4: NULOS DE DIGITAÇÃO NO RDV DE PRESIDENTE, PRIMEIRA ETAPA (teste D4-4 do desenho D4)')
    P('')
    P('Registro: Adendo 27 (commit 2748895, 10/11/2026 00:16:42 UTC) e Adendo 30 (commit a7218fb, 10/11/2026 10:08:24 UTC), antes')
    P('de rodar. Critério: registro/adendo27/desenho_D4_proposta.json, teste D4-4, aplicado à letra. Decisões que o registro não')
    P('fixa: docstring de scripts/analisar_R27_W4.py, escrito antes de qualquer conta com votos (cópia com hora e SHA-256 em')
    P('/home/user/trabalho-eleicao/adendo27/R27_W4/docstring_antes_de_rodar.txt).')
    P(f"Amostra: {n} seções ({R['n_principal']} da amostra aleatória principal, {R['n_extensao']} da extensão), {R['municipios']} municípios, RDV dos dois turnos.")
    P(f"Rodado em {R['quando']}.")
    P('')
    P('ETAPA 1. PUREZA DOS CÓDIGOS NO 1º TURNO (fixado antes; regressão de Poisson sobre L1, R1 e demais votos)')
    cf = pz['conferencia_do_leitor_rdv_contra_oficial']
    P(f"  Leitor conferido: seções em que o RDV discorda do oficial (bweb): 1º turno {cf['1']}; 2º turno {cf['2']}.")
    v1 = pz['votos_1t']
    P(f"  Na amostra, 1º turno: {mil(v1['comp'])} votantes; Lula {mil(v1['L'])}, Flávio {mil(v1['R'])}, outros {mil(v1['O'])}, brancos {mil(v1['B'])}, nulos {mil(v1['N'])} "
      f"(com dígitos {mil(pz['nulos_com_digitos_1t'])}, sem dígitos {mil(pz['nulos_sem_digitos_1t'])}).")
    for cod in ('31', '32', '52'):
        c = pz['codigos'][cod]; p = c['principal_L1_R1_demais']
        P(f"  Código {cod} (lado previsto {c['lado_previsto']}): {c['contagem_1t']:.0f} nulos em {c['secoes_com_pelo_menos_um']} seções ({c['por_10_mil_votantes']:.2f} por 10 mil votantes).")
        P(f"     Partes atribuídas: Lula {p['parte']['L1']:.3f}, Flávio {p['parte']['R1']:.3f}, demais {p['parte']['demais']:.3f}. Lado previsto: {p['parte_lado_previsto']:.3f} "
          f"(ep {p['ep_boot']:.3f}; IC95 {p['ic95_boot_municipios'][0]:.3f} a {p['ic95_boot_municipios'][1]:.3f}). Limite 0,80: {'APROVADO' if c['aprovado'] else 'REPROVADO'}.")
        P(f"     Ao lado: demais = só nominais em outros candidatos {c['variante_demais_so_nominais']['parte_lado_previsto']:.3f}; cinco regressores {c['variante_cinco_regressores']['parte_lado_previsto']:.3f}.")
    x = pz['correcao_do_52']
    P(f"  Correção do 52 no 1º turno (Poisson sobre R1 e votos do 55): parte de Flávio f52 = {x['f52_parte_atribuida_a_R1']:.3f} (ep {x['ep_boot']:.3f}; IC95 {x['ic95_boot'][0]:.3f} a {x['ic95_boot'][1]:.3f}); "
      f"parte do 55 = {x['parte_atribuida_ao_55']:.3f}.")
    P(f"     Taxa de erro por 10 mil eleitores: de Flávio {1e4*x['taxa_por_eleitor']['R1']:.2f}; do 55 {1e4*x['taxa_por_eleitor']['V55']:.2f} ({mil(x['votos_do_55_na_amostra'])} votos do 55 na amostra).")
    P(f"  Situação: {pz['situacao']}.")
    P('')
    P('ETAPA 2. TESTEMUNHAS POR TURNO E ERRO-PADRÃO, SEM ABRIR THETA (fixado antes)')
    t1 = cg['testemunhas_1t']
    P(f"  1º turno: N13 = {t1['N13_1']:.0f} (código 31); N22 = {t1['N22_1']:.1f} (32: {t1['n32']:.0f}; 52: {t1['n52_bruto']:.0f} x f52). Total {t1['total']:.1f} "
      f"({cg['testemunhas_por_10_mil_votantes']['1t']:.2f} por 10 mil votantes; cerca de {mil(cg['testemunhas_no_universo_estimadas']['1t'])} no país).")
    P(f"  2º turno: total {cg['testemunhas_2t_total_sem_separar_lado']:.0f} ({cg['testemunhas_por_10_mil_votantes']['2t']:.2f} por 10 mil votantes; cerca de {mil(cg['testemunhas_no_universo_estimadas']['2t'])} no país).")
    P(f"  Nulos com dígitos na amostra: {mil(cg['nulos_com_digitos']['1t'])} no 1º turno e {mil(cg['nulos_com_digitos']['2t'])} no 2º; votantes {mil(cg['votantes']['1t'])} e {mil(cg['votantes']['2t'])}.")
    e = cg['erro_padrao']
    P(f"  Erro-padrão de Theta: {e['bootstrap_municipios_2000']:.4f} (bootstrap de municípios, 2.000 réplicas, a letra); {e['bootstrap_secoes_2000']:.4f} (bootstrap de seções); {e['analitico']:.4f} (fórmula). "
      f"Réplicas descartadas: {e['replicas_descartadas']}.")
    rp = cg['regra_de_parada']
    P(f"  Erro total com o piso sistemático de 0,015: {rp['erro_total_atual_com_piso_sistematico']:.4f}. Limite do critério de sem sinal: 0,027. "
      f"{'O teste NÃO tem poder com esta amostra.' if cg['sem_poder_nesta_etapa'] else 'Dentro do limite.'}")
    P('')
    P('ETAPA 3. REGRA DE PARADA DO DESENHO (blocos de 10 mil até o erro-padrão chegar a 0,022 ou até 60 mil seções)')
    P(f"  Seções necessárias para o erro-padrão chegar a 0,022: {mil(rp['secoes_necessarias_exato'])} (erro cai com a raiz do número de seções). Em blocos de 10 mil: {mil(rp['secoes_necessarias_em_blocos_de_10_mil'])}"
      f"{' , ACIMA do teto de 60 mil' if rp['passa_do_teto_de_60_mil'] else ''}. Alvo: {mil(rp['alvo'])}.")
    pj = rp['ep_projetado']
    P('  Erro-padrão projetado: ' + '; '.join(f"{mil(int(k))} seções {v:.4f}" for k, v in pj.items() if int(k) != N_UNIVERSO) + f"; universo ({mil(N_UNIVERSO)}) {pj[str(N_UNIVERSO)]:.4f}.")
    P(f"  No alvo: erro-padrão {rp['ep_projetado_no_alvo']:.4f}, erro total {rp['erro_total_projetado_no_alvo']:.4f} (com o piso de 0,015).")
    for k, nome in (('custo_ate_o_alvo_descontando_a_principal', 'até o alvo, descontadas as 3.000 da principal'),
                    ('custo_ate_o_alvo_descontando_principal_e_extensao', 'até o alvo, descontadas a principal e a extensão em curso (6.000)'),
                    ('custo_ate_60_mil_descontando_principal_e_extensao', 'até o teto de 60 mil, descontadas as 6.000')):
        c = rp[k]
        P(f"  Download {nome}: {mil(c['secoes_a_baixar'])} seções, {mil(c['requisicoes_so_rdv'])} requisições (aux e RDV, dois turnos), {c['horas_so_rdv']:.1f} horas = {c['dias_so_rdv']:.1f} dias a 1 por segundo; "
          f"{c['disco_MB_rdv']:.0f} MB de RDV. Com boletim junto: {c['horas_com_boletim']:.1f} horas.")
    P(f"  Tamanho médio do RDV: {rp['bytes_medios_rdv']['1t']:.0f} bytes no 1º turno e {rp['bytes_medios_rdv']['2t']:.0f} no 2º. Placebo de 2022 (15 mil seções, dois turnos): mais {rp['custo_do_placebo_2022_15_mil_secoes']['horas']:.1f} horas.")
    P('')
    P('ETAPA 4. THETA ABERTO (depois das etapas 1 a 3)')
    b = R['bruto_2026']; o, w = b['oficial'], b['testemunhas']
    P('  Valor bruto de 2026, nas seções da amostra:')
    P(f"    Oficial: 1º turno Lula {mil(o['L1'])}, Flávio {mil(o['R1'])}, P1 = {o['P1']:.4f}; 2º turno Lula {mil(o['L2'])}, Flávio {mil(o['R2'])}, P2 = {o['P2']:.4f}. Variação do logit oficial: {fm(o['delta_logit_P'])}.")
    P(f"    Testemunhas: 1º turno N13 = {w['N13_1']:.0f}, N22 = {w['N22_1']:.1f} (32: {w['n32_1']:.0f}; 52: {w['n52_1_bruto']:.0f} bruto), W1 = {w['W1']:.4f}; "
      f"2º turno N13 = {w['N13_2']:.0f}, N22 = {w['N22_2']:.0f} (32: {w['n32_2']:.0f}; 52: {w['n52_2']:.0f}), W2 = {w['W2']:.4f}. Variação do logit das testemunhas: {fm(w['delta_logit_W'])}.")
    tx = b['taxas_por_10_mil_eleitores_do_lado']
    P(f"    Taxa de erro por 10 mil eleitores do lado: 13: {tx['a1_13']:.2f} no 1º turno e {tx['a2_13']:.2f} no 2º (ln da razão {fm(tx['ln_a2_sobre_a1'])}); 22: {tx['b1_22']:.2f} e {tx['b2_22']:.2f} (ln da razão {fm(tx['ln_b2_sobre_b1'])}).")
    cr = R['criterio']
    P(f"  THETA = {fm(R['theta'])}; erro-padrão {R['erro_padrao']['bootstrap_municipios_2000']:.4f}; erro sistemático {R['erro_sistematico']['valor']:.3f} (piso; placebo de 2022 não rodado); erro total {R['erro_total']:.4f}.")
    P(f"    Theta sobre o erro-padrão: {cr['theta_sobre_ep']:+.2f}; sobre o erro total: {cr['theta_sobre_erro_total']:+.2f}. IC95 percentil do bootstrap: {fm(R['ic95_percentil_boot'][0])} a {fm(R['ic95_percentil_boot'][1])}.")
    P(f"    Referência: a troca que vira o resultado daria +0,071; o limiar de sinal com este erro é {cr['limiar_de_sinal_com_este_erro']:.3f}.")
    c = cr['condicoes']
    sn = lambda z: 'sim' if z else 'não'
    P(f"  Condições, uma a uma: Theta >= 0,045: {sn(c['theta_ge_0045'])}; Theta >= 2,5 x erro total: {sn(c['theta_ge_2e5_erro_total'])}; mesmo sinal em 4 de 5 regiões: {sn(c['regioes_mesmo_sinal_ge_4'])} ({cr['regioes_com_o_mesmo_sinal']} de 5); "
      f"nos três tercis: {sn(c['tercis_mesmo_sinal_3'])} ({cr['tercis_com_o_mesmo_sinal']} de 3); |Theta| <= 0,020: {sn(c['abs_theta_le_0020'])}; erro total <= 0,027: {sn(c['erro_total_le_0027'])}; erro-padrão <= 0,022: {sn(c['ep_le_0022'])}.")
    P(f"    Aritmética de SINAL cumprida: {sn(cr['aritmetica_de_sinal_cumprida'])}. Aritmética de SEM SINAL cumprida: {sn(cr['aritmetica_de_sem_sinal_cumprida'])}. Espelho (sinal a favor de Flávio): {sn(cr['espelho_theta_le_menos_0045_e_menos_2e5_erro'])}.")
    P(f"  VEREDITO PELA LETRA: {cr['veredito_pela_letra']}.")
    P('  Por região e por tercil de escolaridade (f52 nacional; erro por bootstrap de municípios dentro do subgrupo):')
    for nome, s in R['subgrupos'].items():
        P(f"    {nome:<11} n = {s['n']:>5}; testemunhas 1º turno {s['N13_1']:.0f} e {s['N22_1']:.1f}, 2º turno {s['N13_2']:.0f} e {s['N22_2']:.0f}; Theta = {fm(s['theta'])}"
          + (f" (ep {s['ep']:.3f})" if 'ep' in s else ''))
    P('')
    P('LEITURAS SECUNDÁRIAS FIXADAS ANTES DE ABRIR (não decidem)')
    s = R['leituras_secundarias']
    P(f"  (a) só o 32 do lado do 22: Theta = {fm(s['a_so_32']['theta'])} (ep {s['a_so_32']['ep']:.4f}); (b) só o 52 corrigido: {fm(s['b_so_52_corrigido']['theta'])} (ep {s['b_so_52_corrigido']['ep']:.4f}); "
      f"(c) sem a correção do 52: {fm(s['c_sem_correcao_do_52']['theta'])} (ep {s['c_sem_correcao_do_52']['ep']:.4f}).")
    if 'diferenca_so52_menos_so32' in s:
        P(f"      Diferença (b) menos (a): {fm(s['diferenca_so52_menos_so32']['valor'])} (ep {s['diferenca_so52_menos_so32']['ep']:.4f}).")
    P(f"  (e) só seções com a mesma urna e os mesmos aptos nos dois turnos (n = {s['e_mesma_urna_e_mesmos_aptos']['n']}): Theta = {fm(s['e_mesma_urna_e_mesmos_aptos']['theta'])} (ep {s['e_mesma_urna_e_mesmos_aptos']['ep']:.4f}).")
    for t in '12':
        vv = s['f_validade_em_nivel'][t]
        P(f"  (f) validade em nível, {t}º turno: inclinação de logit W sobre logit P entre cinco grupos de seções = {vv['inclinacao']:.3f} (ep {vv['ep_inclinacao']:.3f}); esperado 1.")
        P('      ' + '; '.join(f"grupo {g['grupo']}: P {g['P_oficial']:.3f}, W {g['W']:.3f} ({g['N13']:.0f} e {g['N22']:.0f})" for g in vv['grupos']))
    g = s['g_metades']
    P(f"  (g) duas metades aleatórias: {fm(g['metades'][0]['theta'])} (ep {g['metades'][0]['ep']:.3f}) e {fm(g['metades'][1]['theta'])} (ep {g['metades'][1]['ep']:.3f}); diferença {fm(g['diferenca'])} (ep {g['ep_da_diferenca']:.3f}; z = {g['z']:+.2f}).")
    h = s['h_controles_00_99']
    P('  (h) códigos de controle: ' + '; '.join(f"{cod}: {h[cod]['1']['contagem']:.0f} no 1º turno ({100*h[cod]['1']['parcela_dos_nulos_com_digitos']:.2f}% dos nulos com dígitos, ep {100*h[cod]['1']['ep']:.2f}) e "
                                                 f"{h[cod]['2']['contagem']:.0f} no 2º ({100*h[cod]['2']['parcela_dos_nulos_com_digitos']:.2f}%, ep {100*h[cod]['2']['ep']:.2f})" for cod in ('00', '99')) + '.')
    P('')
    P('CALIBRAÇÃO POR EFEITO PLANTADO NOS DADOS DE 2026')
    P('  A. Plantio na contagem oficial das seções da amostra, com as testemunhas reais (200 cópias):')
    ca = R['calibracao_A_plantio_na_contagem_oficial']
    for k, nome in (('A1_troca_3e57', 'troca de 3,57% dos votos de Flávio para Lula'), ('A2_troca_1e8', 'troca de 1,8% (meia dose)'),
                    ('A3_acrescimo_da_margem_para_Lula', 'acréscimo de 4.430.191 votos para Lula (pelos faltosos)'),
                    ('A4_espelho_troca_3e57_de_Lula_para_Flavio', 'espelho: troca de 3,57% dos votos de Lula para Flávio'),
                    ('A4_espelho_acrescimo_da_margem_para_Flavio', 'espelho: acréscimo da margem para Flávio')):
        x = ca[k]
        P(f"    {nome}: Theta desloca {fm(x['deslocamento_medio'])} (fórmula {fm(x['esperado_pela_formula'])}); isso é {x['deslocamento_sobre_ep']:+.2f} erros-padrão e {x['deslocamento_sobre_erro_total']:+.2f} erros totais. "
          f"Veredito no dado plantado: {', '.join(f'{a} em {b_}' for a, b_ in x['veredito_no_dado_plantado'].items())} de 200. Enxerga a 2,5 erros: {sn(x['enxerga_a_2e5_erros'])}.")
    P('    ' + ca['nota'] + '.')
    cb = R['calibracao_B_testemunhas_refeitas']
    P('  B. Testemunhas refeitas por sorteio (1.000 conjuntos por cenário; taxas de erro por eleitor iguais nos dois turnos):')
    tx = cb['taxas_por_10_mil']
    P(f"    Taxas usadas, por 10 mil eleitores: 31 por eleitor de Lula {tx['a31']:.2f}; 32 por eleitor de Flávio {tx['b32']:.2f}; 52 por eleitor de Flávio {tx['b52']:.2f}; 52 por eleitor do 55 {tx['c55']:.2f}.")
    for k, nome in (('B0_nulo', 'B0 sem alteração'), ('B1_troca_que_vira', 'B1 troca que vira o resultado (3,57%)'), ('B2_acrescimo_da_margem', 'B2 acréscimo da margem para Lula'),
                    ('B3_inocente_impureza_020', 'B3 inocente: 20% das testemunhas não seguem o lado'), ('B3_inocente_impureza_estimada', 'B3 inocente: impureza estimada na pureza'),
                    ('B4_inocente_eliminados_10_pontos_a_mais_para_Lula', 'B4 inocente: eliminados que erram tecla 10 pontos a mais para Lula'),
                    ('B4_inocente_eliminados_10_pontos_a_mais_para_Flavio', 'B4 inocente: eliminados que erram tecla 10 pontos a mais para Flávio')):
        x = cb[k]
        P(f"    {nome}: Theta médio {fm(x['theta_medio'])} (desvio entre conjuntos {x['dp_de_theta']:.4f}; esperado sem ruído {fm(x['theta_esperado_sem_ruido'])}). "
          f"Aritmética de SINAL em {100*x['fracao_aritmetica_de_sinal_com_o_erro_real']:.1f}% dos conjuntos; espelhada em {100*x['fracao_aritmetica_de_sinal_espelhada']:.1f}%; |Theta| <= 0,020 em {100*x['fracao_abs_theta_le_0020_ignorando_o_erro']:.1f}%.")
    P(f"    Impureza estimada usada em B3: {', '.join(f'{k} = {v:.3f}' for k, v in cb['impureza_estimada'].items())}.")
    P('    Poder projetado (aproximação normal, sem contar as condições de região e tercil; erro sistemático 0,015):')
    for nn in list(cb['B1_troca_que_vira']['projecao_normal'].keys()):
        x0 = cb['B0_nulo']['projecao_normal'][nn]; x1 = cb['B1_troca_que_vira']['projecao_normal'][nn]
        P(f"      {mil(int(nn)):>7} seções: erro-padrão {x1['ep']:.4f}, erro total {x1['erro_total']:.4f}, limiar de sinal {x1['limiar_de_sinal']:.3f}; chance de SINAL com a troca que vira: {100*x1['prob_aritmetica_de_sinal']:.1f}%; "
          f"sem alteração: SINAL em {100*x0['prob_aritmetica_de_sinal']:.2f}%, SEM SINAL em {100*x0['prob_aritmetica_de_sem_sinal']:.1f}%; com a troca, SEM SINAL (absolvição errada) em {100*x1['prob_aritmetica_de_sem_sinal']:.1f}%.")
    P(f"  O teste enxerga o plantado (regra do docstring: SINAL em 80% ou mais dos conjuntos de B1 e deslocamento de 2,5 erros totais ou mais)? {sn(cb['enxerga_o_plantado'])}.")
    P('')
    P('TRADUÇÃO EM VOTOS DE MARGEM (totais nacionais do 2º turno; margem oficial 4.430.191)')
    vm = R['votos_de_margem']
    for k, nome in (('theta', 'Theta medido'), ('theta_menos_196_erro_total', 'Theta menos 1,96 erro total'), ('theta_mais_196_erro_total', 'Theta mais 1,96 erro total'),
                    ('theta_menos_196_ep', 'Theta menos 1,96 erro-padrão'), ('theta_mais_196_ep', 'Theta mais 1,96 erro-padrão'),
                    ('referencia_troca_que_vira', 'referência: a troca que vira'), ('menor_efeito_que_a_aritmetica_de_sinal_alcanca', 'menor Theta que daria SINAL com este erro')):
        x = vm[k]
        P(f"  {nome}: Theta {fm(x['theta'])} = troca de {mil(x['votos_trocados_equivalentes'])} votos, efeito na margem {mil(x['efeito_na_margem_por_troca'])} ({100*x['fracao_da_margem_por_troca']:+.0f}% da margem); "
          f"ou acréscimo de {mil(x['acrescimo_equivalente'])} votos ({100*x['fracao_da_margem_por_acrescimo']:+.0f}% da margem).")
    P('')
    P('DESCRITIVO: O QUE OS ELEITORES DIGITAM NOS VOTOS NULOS DE PRESIDENTE (aberto só na etapa 4)')
    for t in '12':
        d = R['descritivo_digitos_nulos'][t]
        P(f"  {t}º turno: {mil(d['votantes'])} votantes na amostra; {mil(d['nulos_com_digitos'])} nulos com dígitos ({100*d['nulos_com_digitos']/d['votantes']:.2f}%), {mil(d['nulos_sem_digitos'])} nulos sem dígitos, {mil(d['brancos'])} brancos; {d['codigos_distintos']} números distintos.")
        P('    número  contagem  % dos nulos  por 10 mil votantes  rótulo')
        for x in d['tabela']:
            P(f"    {x['digitos']:>4}    {x['contagem']:>6}     {100*x['parcela_dos_nulos_com_digitos']:>6.2f}       {x['por_10_mil_votantes']:>8.2f}         {x['rotulo']}")
    P('')
    P('DESCRITIVO: NÚMEROS DE CANDIDATOS ELIMINADOS DIGITADOS COMO NULO NO 2º TURNO')
    el = R['descritivo_eliminados_digitados_no_2t']
    P('    número  nulos no 2º turno  % dos nulos (ep)   por 10 mil votantes  votos próprios no 1º turno  por 100 votos próprios (ep)  parte dos próprios eleitores (Poisson)')
    for cod in ELIMINADOS:
        x = el[cod]
        pp = x.get('poisson_parte_atribuida_aos_proprios_eleitores')
        r100 = x.get('por_100_votos_do_proprio_candidato_no_1t')
        P(f"    {cod:>4}    {x['contagem_2t']:>8.0f}          {100*x['parcela_dos_nulos_com_digitos_2t']:>5.2f} ({100*x['ep_parcela']:.2f})       {x['por_10_mil_votantes_2t']:>7.2f}            {x['votos_do_candidato_1t_na_amostra']:>9.0f}              "
          + (f"{r100:>6.2f} ({x.get('ep_por_100_votos', float('nan')):.2f})" if r100 is not None else '   n/d') + (f"                 {pp:.3f}" if pp is not None else '                 n/d'))
    x = el['todos_os_11']
    P(f"    Os 11 juntos: {x['contagem_2t']:.0f} nulos ({100*x['parcela_dos_nulos_com_digitos_2t']:.2f}% dos nulos com dígitos, ep {100*x['ep_parcela']:.2f}); {x['por_10_mil_votantes_2t']:.2f} por 10 mil votantes; "
      f"{x['por_100_votos_de_eliminados_no_1t']:.2f} por 100 votos de eliminados no 1º turno (ep {x['ep_por_100_votos']:.2f}); cerca de {mil(x['estimativa_no_pais'])} no país.")
    P(f"    Número de finalista gravado como nulo: 13 em {el['finalista_13_digitado_como_nulo']['1t']:.0f} (1º turno) e {el['finalista_13_digitado_como_nulo']['2t']:.0f} (2º); 22 em {el['finalista_22_digitado_como_nulo']['1t']:.0f} e {el['finalista_22_digitado_como_nulo']['2t']:.0f}.")
    P('')
    for bloco in R.get('texto_final', []):
        P(bloco)
    return '\n'.join(L) + '\n'


def finalizar(ext=False):
    suf = '_ext' if ext else ''
    R = le('etapa4_tudo' + suf + '.json')
    extra = os.path.join(TRAB, 'texto_final' + suf + '.json')
    if os.path.exists(extra):
        R.update(json.load(open(extra)))
    R['arquivos'] = {'script': 'scripts/analisar_R27_W4.py', 'trabalho': TRAB,
                     'docstring_antes_de_rodar': TRAB + '/docstring_antes_de_rodar.txt'}
    txt = relatorio(R, ext)
    assert '—' not in txt and '–' not in txt
    sj = SAIDA_JSON if not ext else SAIDA_JSON.replace('.json', '_com_extensao.json')
    st = SAIDA_TXT if not ext else SAIDA_TXT.replace('.txt', '_com_extensao.txt')
    with open(sj, 'w') as f:
        json.dump(R, f, ensure_ascii=False, indent=1)
    with open(st, 'w') as f:
        f.write(txt)
    print(txt)


if __name__ == '__main__':
    modo = sys.argv[1] if len(sys.argv) > 1 else ''
    ext = '--ext' in sys.argv
    if modo == 'ler':
        etapa_ler()
    elif modo == 'pureza':
        etapa_pureza(ext)
    elif modo == 'cego':
        etapa_cego(ext)
    elif modo == 'abrir':
        if not os.path.exists(os.path.join(TRAB, 'etapa2_3_cego' + ('_ext' if ext else '') + '.json')):
            sys.exit('rode antes as etapas cegas (pureza e cego)')
        etapa_abrir(ext)
        finalizar(ext)
    elif modo == 'relatorio':
        finalizar(ext)
    else:
        sys.exit(__doc__)
