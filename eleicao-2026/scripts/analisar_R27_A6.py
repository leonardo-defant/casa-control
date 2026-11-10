"""R27_A6: TIPO DE HABILITAÇÃO (teste D1.5 de registro/adendo27/desenho_D1_proposta.json, por inteiro).

Adendo 27 do pré-registro (commit 2748895, 10/11/2026 00:16:42 UTC), Onda A, item A6. O critério vale como escrito
no D1.5 e nas DEFINIÇÕES COMUNS do campo "frente" do mesmo arquivo. Este docstring foi escrito ANTES de qualquer
conta com votos; o que ele decide e o registro não fixa está listado abaixo como DECISÕES e sai no resultado como
desvio. Até aqui só foi lida estrutura sem voto: campos da urna no bweb (estrutura_1t e estrutura_2t do desenhista),
tipo de habilitação por eleitor no log (log_eleitor do desenhista) e o perfil do eleitorado (F15).

Hipótese (D1.5): para não ser pego no teste de integridade, o programa só alteraria o voto de quem foi habilitado
por biometria, ou trataria de modo diferente os liberados pelo mesário. Marca: quanto maior a fração de eleitores
liberados sem biometria na seção, menor o ganho de Lula além do previsto pelo 1º turno; para zerar a margem,
2,04 p.p. entre uma seção toda biométrica e uma toda manual. O efeito tem de vir da habilitação do dia (m2), não
do tipo de eleitor (m1, nb).

Uso:
  python3 -I scripts/analisar_R27_A6.py perfil   extrai o perfil do eleitorado por seção (F15, sem votos)
  python3 -I scripts/analisar_R27_A6.py gov2t    extrai governador do 2º turno das 6 UFs (bweb do 2º turno)
  python3 -I scripts/analisar_R27_A6.py rodar    monta a base, roda tudo e grava resultados/R27_A6_tipo_habilitacao.json e .txt
Trabalho e parciais: /home/user/trabalho-eleicao/adendo27/R27_A6/

O QUE O REGISTRO FIXA (aplicado à letra)
- Universo U: seções do 2º turno de 2026 pareadas com o 1º turno pela chave, com L2 + R2 de 30 ou mais, fora o
  exterior e as 27 seções com junta apuradora no 2º turno.
- Desfecho y = 100 x L2 / (L2 + R2). Peso V = L2 + R2. Efeito fixo de local de votação. Erro agrupado por município.
- Referência interna X (1º turno na mesma seção): fração de cada candidato sobre o comparecimento do 1º turno (13,
  22, cada um dos demais com 0,5% ou mais no país, resto agrupado), brancos, nulos, abstenção do 1º turno, variação
  da abstenção entre os turnos, perfil do eleitorado (faixas etárias, sexo, escolaridade, fração com biometria),
  logaritmo dos aptos e posição da seção dentro do local.
- Dose m2 = QT_ELEI_BIOM_SEM_HABILITACAO do 2º turno / comparecimento do 2º turno; m1 = o mesmo no 1º turno;
  nb = 1 menos eleitores com biometria / eleitores (F15). Modelo: y = local + X + b x m2 + k x m1 + r x nb +
  modelo da urna + erro. Phi = menos b / 2,04.
- SINAL: b de menos 0,51 ou abaixo, z de 3,3 ou mais em módulo, |k| menor que metade de |b|, mesmo sentido no
  experimento natural e na amostra de logs, e em 4 das 5 regiões. Sinal contrário (b de mais 0,51 ou acima) é
  relatado do mesmo jeito. Da regra geral da frente: placebo limpo (Phi do placebo de no máximo um terço em módulo).
- SEM SINAL: intervalo de 99% de b entre menos 0,51 e mais 0,51 e experimento natural com diferença dentro de
  0,6 p.p. para cada lado.
- INCONCLUSIVO: b significativo acompanhado de k do mesmo tamanho, ou intervalo mais largo que o limite, ou o resto.
- Complementos: (i) experimento natural: seções com m2 de 0,5 ou mais contra as vizinhas do mesmo local; seções
  com m2 de 0,2 ou mais e m1 abaixo de 0,1 ("leitor caiu no 2º turno"); espelho (m1 de 0,2 ou mais e m2 abaixo de
  0,1) como placebo. (ii) amostra de logs: frações exatas de M e de S no 2º turno como doses, as do 1º turno como
  controles. (iii) y_BN = 100 x (B2 + N2) / comparecimento do 2º turno nas mesmas contas.
- Desfecho alternativo: y_alt = y menos a fração de 2022 na mesma seção, com controles de 2022.
- Placebos: de período anterior (m2 e m1 de 2026 na virada de 2022 das mesmas seções); de turno trocado (desfecho
  do 1º turno de 2026 contra 2022, m1 como dose e m2 como controle); de cargo (governador do 2º turno nas 6 UFs);
  espelho do experimento natural.
- Calibração: plantar em cópia, movendo de R para L um binomial com taxa f x (1 menos m2) por seção, f para
  Phi = 0,25; 0,5 e 1; 200 repetições; conferir que b recupera menos 2,04 x Phi e que k fica em zero.

DECISÕES QUE O REGISTRO NÃO FIXA (tomadas aqui, antes de calcular qualquer coisa com votos)
D1. Junta apuradora = NR_JUNTA_APURADORA igual a 1 na estrutura do 2º turno (27 seções). As seções com junta só no
    1º turno ficam em U (a letra só tira as do 2º); sensibilidade sem elas. Seção sem perfil no F15 sai das contas
    que usam perfil (a contagem é relatada). Como em lib.fe_ols, local com uma única seção em U não informa.
D2. "0,5% ou mais no país" = votos do candidato no 1º turno divididos pelo comparecimento nacional do 1º turno
    (todas as seções, com exterior). As frações da seção são sobre o comparecimento do 1º turno da seção. O "resto
    agrupado" (demais candidatos e votos do candidato anulado) é a categoria de referência: fica fora da matriz
    porque as frações somam 1.
D3. Abstenção do 1º turno = 1 menos comparecimento/aptos do 1º turno; variação = abstenção do 2º menos a do 1º.
    Logaritmo dos aptos = ln(aptos do 2º turno). Posição no local = (ordem da seção pelo número entre as seções do
    2º turno do mesmo local, menos 1) / (seções do local menos 1); zero em local de seção única.
D4. Perfil (F15, cadastro de 14/07/2026, lido em fluxo): fração de mulheres; frações de idade em 8 faixas (16 e 17;
    18 a 24; 25 a 34; 35 a 44; 45 a 59; 60 a 69; 70 a 79; 80 ou mais), referência 35 a 44; frações de escolaridade
    nos 8 graus do cadastro, referência ensino médio completo. Denominador: total de eleitores da seção no perfil.
    Em seção com agregadas (DS_SECOES_AGREGADAS do bweb do 2º turno) o perfil é a soma da principal com as
    agregadas. A "fração com biometria" do X é a mesma variável que nb (nb = 1 menos ela): entra uma vez, como nb.
D5. Modelo da urna: pelo número de série da urna efetivada no 2º turno (scripts/modelos.py, faixas de 2026);
    indicadoras de UE2013, UE2015 e UE2022, referência UE2020; série fora das faixas ganha indicadora própria.
    Coluna sem variação dentro dos locais é retirada e isso é relatado.
D6. Erro agrupado por município (UF mais código): lib.fe_ols agrupa o erro pelo mesmo grupo do efeito fixo, então a
    conta é feita por função própria (classe Reg), com a mesma fórmula CR1 de lib.fe_ols e o município como
    agrupamento; a função é conferida contra lib.fe_ols com agrupamento por local. Sensibilidade: erro por local.
D7. z = b / erro-padrão. Intervalo de 99% = b mais ou menos 2,5758 x erro-padrão. Phi da letra = menos b / 2,04.
    Ao lado, sem decidir: Phi pela fórmula geral da frente, 2 x (menos b) x soma((1 menos m2) x V) / 100 / 4.430.191.
D8. Regiões: Norte (AC AM AP PA RO RR TO), Nordeste (AL BA CE MA PB PE PI RN SE), Sudeste (ES MG RJ SP), Sul (PR RS
    SC), Centro-Oeste (DF GO MS MT). "Mesmo sentido" = sinal do b da região igual ao do b nacional.
D9. Experimento natural: três regressões separadas, cada uma com uma indicadora no lugar da dose: A = m2 de 0,5 ou
    mais; B = m2 de 0,2 ou mais e m1 abaixo de 0,1; C (espelho, placebo) = m1 de 0,2 ou mais e m2 abaixo de 0,1.
    Modelo: y = local + X + d x indicadora + r x nb + modelo da urna + erro, sem m1 e sem m2 (a indicadora é função
    deles); as vizinhas são todas as outras seções de U no mesmo local. Ao lado: a mesma conta com m1 como controle,
    a diferença bruta (sem X) da seção contra as vizinhas em y e no 1º turno, a diferença média de m2 entre tratadas
    e vizinhas, e o Phi equivalente = menos d / (2,04 x diferença média de m2). O limite de 0,6 p.p. do critério
    SEM SINAL aplica-se ao grupo A (é metade do 1,2 p.p. que o registro espera para esse grupo). "Mesmo sentido no
    experimento natural" = sinal de d do grupo A igual ao de b; o grupo B é relatado ao lado e, se tiver sinal
    oposto com |z| de 2 ou mais, isso é dito como contradição.
D10. Amostra de logs: seções da amostra com os dois turnos no log e dentro de U. Frações por turno entre os eleitores
    com voto computado no log: M (liberado pelo mesário), S (sem linha de tipo, eleitor sem biometria), B
    (biométrica). Duas contas, as duas com o modelo base (X, modelo da urna, efeito fixo de local, peso V) estimado
    dentro da amostra: (a) a da letra, com fM2 e fS2 como doses e fM1 e fS1 como controles; (b) a restrita, com
    u2 = fM2 + fS2 como dose e u1 = fM1 + fS1 como controle. nb não entra (fS é a medida exata dele). "Mesmo sentido
    na amostra de logs" = sinal do coeficiente de u2 na conta (b) igual ao de b; os coeficientes de fM2 e fS2 da
    conta (a) saem ao lado. Erro por município, e por local ao lado.
D11. y_BN: as mesmas contas (dose, regiões, experimento natural, logs) com y_BN = 100 x (B2 + N2) / comparecimento
    do 2º turno, mesmo peso V da letra. Escala: Phi_BN = b_BN / 100 x soma((1 menos m2) x comparecimento do 2º
    turno) / 4.430.191 (cada voto convertido vale um voto de margem). Hipótese de conversão entre os habilitados
    por biometria dá b_BN positivo (mais branco e nulo onde há mais liberação manual). y_BN não diz para quem o voto
    convertido foi. Limites: os do D1.5 (|Phi_BN| de 0,25, z de 3,3, |k| menor que metade de |b|).
D12. y_alt = y menos 100 x L2/(L2+R2) de 2022 na mesma seção (pareada pela chave, com L2+R2 de 2022 de 30 ou mais).
    Controles de 2022 no lugar dos do 1º turno de 2026: frações de L, R, brancos e nulos sobre o comparecimento do
    1º turno de 2022 (outros = referência), a própria fração de 2022 do 2º turno (coeficiente livre), abstenção do
    1º turno de 2022, variação da abstenção de 2022 entre os turnos, abstenção do 2º turno de 2026 menos a do 2º de
    2022; perfil, ln dos aptos, posição, m1, nb e modelo da urna como no modelo base. Efeito fixo do local de 2026.
    Sensibilidade: só seções com o mesmo código de local em 2022 e 2026.
D13. Placebo de período anterior: desfecho 100 x L2/(L2+R2) de 2022; X = frações de L, R, brancos e nulos do 1º
    turno de 2022, abstenção do 1º turno de 2022, variação da abstenção de 2022, perfil de 2026, ln dos aptos do 2º
    turno de 2022, posição; dose m2 de 2026, controles m1 e nb de 2026 e modelo da urna de 2026; peso L2+R2 de
    2022; efeito fixo do local de 2026; mesmas seções de U com par em 2022. Phi do placebo = menos b / 2,04.
    Placebo de turno trocado: desfecho 100 x L1/(L1+R1) do 1º turno de 2026 (L1+R1 de 30 ou mais), controles de
    2022 (fração de 2022 do 2º turno, frações de L, R, brancos e nulos do 1º turno de 2022, abstenção do 1º turno de
    2022, abstenção do 1º de 2026 menos a do 1º de 2022), perfil, ln dos aptos do 1º turno, posição; dose m1,
    controles m2 e nb, modelo da urna do 1º turno; peso L1+R1. Este também serve de teste da hipótese no 1º turno.
    Placebo de cargo: governador do 2º turno em AC, AM, DF, ES, RN e TO, uma regressão por UF: desfecho = 100 x
    votos do candidato "do lado de Lula" / votos dos dois, onde "do lado de Lula" é, dos dois, aquele cuja fração por
    seção tem correlação ponderada positiva com y na UF; X = frações de cada candidato a governador do 1º turno com
    0,5% ou mais do comparecimento da UF (resto = referência), brancos e nulos de governador do 1º turno, abstenção
    do 1º turno, variação da abstenção, perfil, ln dos aptos, posição; dose m2, controles m1, nb e modelo da urna;
    peso = votos dos dois. Erro por local (o DF é um município só); por município ao lado onde houver 30 ou mais.
    Resumo das 6 UFs: média ponderada pelo inverso da variância e qui-quadrado dos 6 z (não depende do lado).
    Um placebo é "limpo" se |Phi| for de no máximo um terço (|b| de até 0,68); o espelho do experimento natural é
    "limpo" se |z| for menor que 3,3. Os placebos decidem só se as condições numéricas de SINAL estiverem presentes.
D14. Calibração por efeito plantado nos dados de 2026 (semente 20261110, 200 repetições por tamanho):
    (a) principal: T ~ Binomial(R2, f x (1 menos m2)) passa de R para L em cada seção de U, com
        f = Phi x 2.215.096 / soma em U de (1 menos m2) x R2; Phi = 0,25; 0,5; 1. Em cada cópia: b, k, erros, e os d
        do experimento natural. Medidas: delta_b = b da cópia menos b observado; recuperação rho = média de delta_b /
        (menos 2,04 x Phi); delta_k; poder pi(Phi) = fração das cópias com delta_b / erro de 3,3 ou mais em módulo
        no sentido plantado; eps(Phi) = fração das cópias em que a cópia, como está, NÃO passaria pelo critério
        SEM SINAL; e a fração das cópias que cumpre as condições numéricas de SINAL como estão (b, z e k).
    (b) espelho do plantio: o mesmo de L para R (a favor de Flávio), com f = Phi x 2.215.096 / soma de (1 menos m2)
        x L2; espera delta_b de mais 2,04 x Phi.
    (c) logs: na amostra, T ~ Binomial(R2, g x fB2), com g tal que a fração de R movida na amostra seja
        Phi x 2.215.096 / 59.826.041; mede o coeficiente de u2 e os de fM2 e fS2.
    (d) y_BN: T ~ Binomial(B2 + N2, f x (1 menos m2)) sai de brancos e nulos, f = Phi_BN x 4.430.191 / soma de
        (1 menos m2) x (B2 + N2), para Phi_BN = 0,25; 0,5; 1 (tamanho pulado se a taxa passar de 1).
D15. Regra de SEM PODER (o registro pede a calibração mas não diz como ela decide). O teste "enxerga" um tamanho se
    pi for de 95% ou mais. Veredito SEM PODER para a parte principal se a recuperação rho de Phi = 1 ficar fora de
    0,80 a 1,25, ou se pi(1) for menor que 95%, ou se eps(0,25) for menor que 95%. O campo "poder" do D1.5 já previa
    t de 2,4 a 3,6 para Phi = 0,25, isto é, pi(0,25) abaixo de 95%: nesse caso o SEM SINAL, se vier, vale pelo
    critério próprio do D1.5 (intervalo de 99% dentro de 0,51) e o resultado diz que pela regra geral da frente
    (poder de 95% para Phi = 0,25 com z de 3,3) faltaria poder; também é relatado o menor Phi com pi de 95%.
    Para as outras partes: experimento natural e logs são SEM PODER se nem o Phi = 1 plantado for enxergado
    (delta / erro de 3,3 ou mais em módulo em 95% das cópias); y_BN é SEM PODER se pi_BN(1) for menor que 95%.
D16. Veredito do teste (pela letra, combinado), nesta ordem: SEM PODER pela D15; SINAL se todas as condições do
    critério estiverem presentes (qualquer dos dois sentidos, dito qual); SEM SINAL se o intervalo de 99% de b
    couber em menos 0,51 a mais 0,51 e |d| do grupo A for de até 0,6; INCONCLUSIVO no resto.
    Rótulo de cada parte:
    - dose (y): SINAL se |b| de 0,51 ou mais, |z| de 3,3 ou mais, |k| menor que metade de |b| e 4 das 5 regiões no
      mesmo sentido; SEM SINAL se o intervalo de 99% couber em 0,51 para cada lado; INCONCLUSIVO no resto.
    - experimento natural, grupo A: SEM PODER pela D15; SINAL se |d| maior que 0,6 com |z| de 3,3 ou mais e espelho
      limpo; SEM SINAL se |d| de até 0,6; INCONCLUSIVO no resto. Grupo B: SEM PODER pela D15; SINAL se |z| de 3,3
      ou mais; SEM SINAL se o intervalo de 99% de d excluir o deslocamento médio do Phi = 1 plantado; INCONCLUSIVO
      no resto.
    - logs (coeficiente de u2): SINAL se |b| de 0,51 ou mais, |z| de 3,3 ou mais e |k de u1| menor que metade de
      |b|; SEM PODER pela D15; SEM SINAL se o intervalo de 99% couber em 0,51 para cada lado; INCONCLUSIVO no resto.
    - y_BN: SINAL se |Phi_BN| de 0,25 ou mais, |z| de 3,3 ou mais e |k| menor que metade de |b|; SEM PODER pela
      D15; SEM SINAL se o intervalo de 99% de Phi_BN couber em 0,25 para cada lado; INCONCLUSIVO no resto.
    - y_alt: as condições numéricas da dose aplicadas a b_alt (sem regiões).
D17. Teste espelho (obrigatório): (i) o critério é simétrico e o sentido contrário é relatado igual; (ii) plantio
    espelho da D14(b); (iii) grupo C do experimento natural; (iv) os três placebos de regressão da D13.
D18. Valor bruto de 2026 (obrigatório, ao lado de toda comparação com outro ano): tabela por faixa de m2 (abaixo de
    0,03; 0,03 a 0,06; 0,06 a 0,10; 0,10 a 0,20; 0,20 a 0,50; 0,50 ou mais) com n, V, y médio ponderado, a fração
    de Lula sobre Lula mais Flávio no 1º turno, a diferença entre os dois e y_BN; e as diferenças brutas do
    experimento natural. As contas principais usam só 2026; 2022 entra só em y_alt e nos dois placebos, e isso é
    dito no veredito de cada um.
D19. Tradução em votos: votos trocados = Phi x 2.215.096 e votos de margem = Phi x 4.430.191, com o intervalo de
    99%; para y_BN, votos convertidos = Phi_BN x 4.430.191.
D20. Sensibilidades que não decidem: sem peso; erro por local; sem o bloco de perfil (mantém nb); sem a variação da
    abstenção; só seções com a mesma urna nos dois turnos; sem as seções com junta no 1º turno; só m2 (sem m1),
    para medir o componente de tipo de eleitor; e o exterior à parte (modelo sem perfil e sem nb, se houver
    variação de m2 lá).
D21. Contagem de testes: o resultado diz quantas estatísticas com limiar de z rodaram e quantos sinais o acaso daria.

O QUE FOR FEITO DEPOIS DE VER O RESULTADO fica em funções com nome "exploratorio_" e sai marcado como exploratório.
"""
import sys, os, gzip, json, zipfile, csv, io, glob, time, hashlib, collections
import numpy as np

RAIZ = '/home/user/casa-control/eleicao-2026'
DADOS = RAIZ + '/dados'
TRAB = '/home/user/trabalho-eleicao/adendo27/R27_A6'
D1DIR = '/home/user/trabalho-eleicao/adendo27/desenho_D1'
PERFIL_DIR = '/home/user/trabalho-eleicao/adendo21/F15_dl_perfil_secao'
ZIPS2T = '/home/user/trabalho-eleicao/trab2t/zips2t'
sys.path.insert(0, RAIZ + '/scripts')
from lib import carregar, fe_ols  # noqa: E402
from modelos import modelo as modelo_urna  # noqa: E402

SEMENTE = 20261110
NREP = 200
MARGEM = 4430191
NECESSARIO = 2215096
L2_OFICIAL, R2_OFICIAL = 64256232, 59826041
ESCALA = 2.04
LIM_B = 0.51
LIM_NAT = 0.6
Z_LIM = 3.3
Z99 = 2.5758293035489
PHIS = [0.25, 0.5, 1.0]
UFS_GOV = ['AC', 'AM', 'DF', 'ES', 'RN', 'TO']
REGIOES = {'Norte': ['AC', 'AM', 'AP', 'PA', 'RO', 'RR', 'TO'],
           'Nordeste': ['AL', 'BA', 'CE', 'MA', 'PB', 'PE', 'PI', 'RN', 'SE'],
           'Sudeste': ['ES', 'MG', 'RJ', 'SP'], 'Sul': ['PR', 'RS', 'SC'], 'Centro-Oeste': ['DF', 'GO', 'MS', 'MT']}
COLS_PERFIL = ['total', 'biometria', 'mulheres', 'i1617', 'i1824', 'i2534', 'i3544', 'i4559', 'i6069', 'i7079', 'i80m',
               'e1', 'e2', 'e3', 'e4', 'e5', 'e6', 'e7', 'e8']
FAIXAS_IDADE = {'i1617': [1600, 1700], 'i1824': [1800, 1900, 2000, 2124], 'i2534': [2529, 3034], 'i3544': [3539, 4044],
                'i4559': [4549, 5054, 5559], 'i6069': [6064, 6569], 'i7079': [7074, 7579],
                'i80m': [8084, 8589, 9094, 9599, 9999]}
PERFIL_X = ['mulheres', 'i1617', 'i1824', 'i2534', 'i4559', 'i6069', 'i7079', 'i80m',
            'e1', 'e2', 'e3', 'e4', 'e5', 'e7', 'e8']
T0 = time.time()


def log(*a):
    print(f'[{time.time() - T0:7.1f}s]', *a, flush=True)


def _jd(o):
    if isinstance(o, (np.integer,)): return int(o)
    if isinstance(o, (np.floating,)): return float(o)
    if isinstance(o, np.ndarray): return o.tolist()
    if isinstance(o, (np.bool_,)): return bool(o)
    raise TypeError(str(type(o)))


def gravar(nome, obj):
    with open(f'{TRAB}/{nome}.tmp', 'w') as f:
        json.dump(obj, f, ensure_ascii=False, indent=1, default=_jd)
    os.replace(f'{TRAB}/{nome}.tmp', f'{TRAB}/{nome}')


# ---------------------------------------------------------------- extrações (sem resultado)
def _perfil_uf(z):
    import pandas as pd
    uf = os.path.basename(z).split('_')[-1][:2]
    partes = []
    with zipfile.ZipFile(z) as zf:
        nome = [i.filename for i in zf.infolist() if i.filename.lower().endswith('.csv')][0]
        with zf.open(nome) as f:
            it = pd.read_csv(f, sep=';', encoding='latin-1', chunksize=1500000,
                             usecols=['CD_MUNICIPIO', 'NR_ZONA', 'NR_SECAO', 'CD_GENERO', 'CD_FAIXA_ETARIA',
                                      'CD_GRAU_ESCOLARIDADE', 'QT_ELEITORES', 'QT_ELEITORES_BIOMETRIA'])
            for ch in it:
                q = ch['QT_ELEITORES']
                d = {'total': q, 'biometria': ch['QT_ELEITORES_BIOMETRIA'], 'mulheres': q * (ch['CD_GENERO'] == 4)}
                for nm, cods in FAIXAS_IDADE.items():
                    d[nm] = q * ch['CD_FAIXA_ETARIA'].isin(cods)
                for e in range(1, 9):
                    d[f'e{e}'] = q * (ch['CD_GRAU_ESCOLARIDADE'] == e)
                t = pd.DataFrame(d)
                t['m'] = ch['CD_MUNICIPIO'].values; t['z'] = ch['NR_ZONA'].values; t['s'] = ch['NR_SECAO'].values
                partes.append(t.groupby(['m', 'z', 's'])[COLS_PERFIL].sum())
    g = pd.concat(partes).groupby(level=[0, 1, 2]).sum()
    return {f'{uf}|{int(m)}|{int(zn)}|{int(s)}': [int(x) for x in v] for (m, zn, s), v in zip(g.index, g.values)}


def extrair_perfil():
    from multiprocessing import Pool
    zips = [z for z in sorted(glob.glob(PERFIL_DIR + '/perfil_eleitor_secao_2026_*.zip')) if not z.endswith('_ZZ.zip')]
    zips.sort(key=os.path.getsize, reverse=True)
    out = {}
    with Pool(3) as p:
        for r in p.imap_unordered(_perfil_uf, zips):
            out.update(r)
            print(len(out), flush=True)
    with gzip.open(TRAB + '/perfil_secao_2026_A6.json.gz', 'wt') as f:
        json.dump({'colunas': COLS_PERFIL, 'secoes': out}, f, separators=(',', ':'))
    print('perfil: secoes', len(out), 'eleitores', sum(v[0] for v in out.values()),
          'biometria', sum(v[1] for v in out.values()))


def extrair_gov2t():
    """Governador do 2º turno por candidato e por seção, nas 6 UFs (bweb do 2º turno, cargo 3)."""
    out = {}
    for uf in UFS_GOV:
        z = glob.glob(f'{ZIPS2T}/bweb_2t_{uf}_*.zip')[0]
        with zipfile.ZipFile(z) as zf:
            nome = [n for n in zf.namelist() if n.lower().endswith('.csv')][0]
            with zf.open(nome) as fh:
                rd = csv.reader(io.TextIOWrapper(fh, encoding='latin1', newline=''), delimiter=';')
                cab = next(rd); ix = {c.strip(): i for i, c in enumerate(cab)}
                for r in rd:
                    if r[ix['CD_CARGO_PERGUNTA']] != '3':
                        continue
                    k = f"{r[ix['SG_UF']]}|{int(r[ix['CD_MUNICIPIO']])}|{int(r[ix['NR_ZONA']])}|{int(r[ix['NR_SECAO']])}"
                    o = out.setdefault(k, {'c': {}, 'B': 0, 'N': 0})
                    tp = r[ix['CD_TIPO_VOTAVEL']]; q = int(r[ix['QT_VOTOS']])
                    if tp == '1':
                        o['c'][r[ix['NR_VOTAVEL']]] = o['c'].get(r[ix['NR_VOTAVEL']], 0) + q
                    elif tp == '2':
                        o['B'] += q
                    else:
                        o['N'] += q
        print(uf, len(out), flush=True)
    with gzip.open(TRAB + '/gov2t_6ufs_A6.json.gz', 'wt') as f:
        json.dump(out, f, separators=(',', ':'))
    print('gov2t: secoes', len(out))


# ---------------------------------------------------------------- regressão
class Reg:
    """MQO com efeito fixo de grupo (within), pesos e erro agrupado CR1 por um agrupamento que contém os grupos do
    efeito fixo. Mesma fórmula de lib.fe_ols; quando cl é o próprio grupo, dá os mesmos números."""

    def __init__(self, X, fe, cl, w, nomes):
        X = np.asarray(X, float)
        _, g = np.unique(fe, return_inverse=True)
        cnt = np.bincount(g)
        ok = cnt[g] >= 2
        self.ok = ok
        _, g = np.unique(g[ok], return_inverse=True)
        self.g = g; self.ng = int(g.max()) + 1
        self.w = np.asarray(w, float)[ok]
        self.sw = np.bincount(g, weights=self.w, minlength=self.ng)
        _, c = np.unique(np.asarray(cl)[ok], return_inverse=True)
        self.c = c; self.G = int(c.max()) + 1
        Xd = np.empty((int(ok.sum()), X.shape[1]))
        for j in range(X.shape[1]):
            Xd[:, j] = self._dm(X[ok, j])
        # retira coluna sem variação dentro dos grupos
        var = (Xd ** 2 * self.w[:, None]).sum(0)
        tot = (X[ok] ** 2 * self.w[:, None]).sum(0) + 1e-300
        fica = var / tot > 1e-12
        # retira também coluna que, dentro dos grupos, é combinação linear das anteriores (na ordem da matriz:
        # dose e controles primeiro, modelo da urna por último); sem isso a matriz não inverte
        C = (Xd * self.w[:, None]).T @ Xd
        dg = np.sqrt(np.where(np.diag(C) > 0, np.diag(C), 1.0)); C = C / np.outer(dg, dg)
        mant = []
        for j in range(X.shape[1]):
            if not fica[j]: continue
            if mant:
                cj = C[np.ix_(mant, [j])][:, 0]
                resto = 1.0 - cj @ np.linalg.solve(C[np.ix_(mant, mant)], cj)
                if resto < 1e-8:
                    fica[j] = False; continue
            mant.append(j)
        self.retiradas = [n for n, f in zip(nomes, fica) if not f]
        self.nomes = [n for n, f in zip(nomes, fica) if f]
        self.Xd = Xd[:, fica]
        self.XtX = (self.Xd * self.w[:, None]).T @ self.Xd
        self.inv = np.linalg.inv(self.XtX)
        self.N, self.k = self.Xd.shape
        self.fator = self.G / (self.G - 1) * (self.N - 1) / (self.N - self.k) if self.G > 1 else float('nan')
        self._Z = {}

    def _dm(self, v):
        m = np.bincount(self.g, weights=self.w * v, minlength=self.ng) / self.sw
        return v - m[self.g]

    def fit(self, y):
        yd = self._dm(np.asarray(y, float)[self.ok])
        b = self.inv @ (self.Xd.T @ (self.w * yd))
        e = yd - self.Xd @ b
        S = np.empty((self.G, self.k))
        we = self.w * e
        for j in range(self.k):
            S[:, j] = np.bincount(self.c, weights=we * self.Xd[:, j], minlength=self.G)
        V = self.fator * self.inv @ (S.T @ S) @ self.inv
        se = np.sqrt(np.diag(V))
        r2 = 1 - (self.w * e * e).sum() / (self.w * yd * yd).sum()
        return {'n': int(self.N), 'locais': int(self.ng), 'agrupamentos': int(self.G),
                'coef': dict(zip(self.nomes, b.tolist())), 'ep': dict(zip(self.nomes, se.tolist())),
                'r2_dentro': float(r2), 'dp_residuo_pond': float(np.sqrt((self.w * e * e).sum() / self.w.sum())),
                'retiradas': self.retiradas}

    def rapido(self, y, quais):
        """Coeficiente e erro agrupado só das colunas pedidas (para as repetições da calibração)."""
        yd = self._dm(np.asarray(y, float)[self.ok])
        b = self.inv @ (self.Xd.T @ (self.w * yd))
        we = self.w * (yd - self.Xd @ b)
        out = {}
        for q in quais:
            j = self.nomes.index(q)
            if j not in self._Z:
                self._Z[j] = self.Xd @ self.inv[j]
            s = np.bincount(self.c, weights=we * self._Z[j], minlength=self.G)
            out[q] = (float(b[j]), float(np.sqrt(self.fator * (s @ s))))
        return out


def linha(r, nome):
    b = r['coef'][nome]; ep = r['ep'][nome]
    return {'coef': b, 'ep': ep, 'z': b / ep if ep > 0 else None, 'ic99': [b - Z99 * ep, b + Z99 * ep]}


def wmean(x, w):
    return float((x * w).sum() / w.sum())


# ---------------------------------------------------------------- base
def _int(x):
    try:
        return int(x)
    except Exception:
        return 0


def montar_base():
    log('lendo bases')
    d = carregar(DADOS + '/secoes2026.json.gz')
    cand = carregar(DADOS + '/candidatos2026_1t.json.gz')
    with gzip.open(D1DIR + '/estrutura_1t.json.gz', 'rt') as f: e1 = json.load(f)
    with gzip.open(D1DIR + '/estrutura_2t.json.gz', 'rt') as f: e2 = json.load(f)
    with gzip.open(TRAB + '/perfil_secao_2026_A6.json.gz', 'rt') as f: pf = json.load(f)
    assert pf['colunas'] == COLS_PERFIL
    pf = pf['secoes']
    conf = {}
    # conferência dos totais oficiais e do comparecimento nacional do 1º turno
    conf['L2_total_base'] = sum(v['2']['L'] for v in d.values() if '2' in v)
    conf['R2_total_base'] = sum(v['2']['R'] for v in d.values() if '2' in v)
    conf['L2_oficial'] = L2_OFICIAL; conf['R2_oficial'] = R2_OFICIAL
    comp1_nac = sum(v['1']['comp'] for v in d.values() if '1' in v)
    tot_c = collections.Counter()
    for v in cand['secoes'].values():
        for n, q in v.items(): tot_c[n] += q
    conf['comparecimento_1t_nacional'] = comp1_nac
    conf['candidatos_1t_fracao_do_comparecimento'] = {n: tot_c[n] / comp1_nac for n in sorted(tot_c, key=lambda x: -tot_c[x])}
    conf['candidatos_1t_votos'] = {n: int(tot_c[n]) for n in sorted(tot_c, key=lambda x: -tot_c[x])}
    conf['candidatos_nomes'] = cand['nomes']
    demais = [n for n in sorted(tot_c, key=lambda x: -tot_c[x]) if n not in ('13', '22') and tot_c[n] / comp1_nac >= 0.005]
    conf['demais_com_0_5_ou_mais'] = demais
    chaves = sorted(k for k, v in d.items() if '1' in v and '2' in v and not k.startswith('ZZ|') and k in e1 and k in e2)
    conf['secoes_2t_base'] = sum(1 for v in d.values() if '2' in v)
    conf['pareadas_fora_exterior'] = len(chaves)
    conf['exterior_2t'] = sum(1 for k, v in d.items() if '2' in v and k.startswith('ZZ|'))
    n = len(chaves)
    B = {'chave': np.array(chaves)}
    B['uf'] = np.array([k.split('|')[0] for k in chaves])
    B['mun'] = np.array(['|'.join(k.split('|')[:2]) for k in chaves])
    B['secao'] = np.array([int(k.split('|')[3]) for k in chaves], dtype=np.int32)
    B['local'] = np.array(['|'.join(k.split('|')[:3]) + '|' + str(d[k]['2']['loc']) for k in chaves])
    for t in ('1', '2'):
        for c in ('L', 'R', 'O', 'B', 'N', 'comp', 'apt'):
            B[c + t] = np.array([d[k][t][c] for k in chaves], dtype=np.int64)
    for nm in ['13', '22'] + demais:
        B['c' + nm] = np.array([cand['secoes'].get(k, {}).get(nm, 0) for k in chaves], dtype=np.int64)
    conf['c13_igual_L1'] = int((B['c13'] == B['L1']).sum()); conf['c22_igual_R1'] = int((B['c22'] == B['R1']).sum())
    B['bsh1'] = np.array([_int(e1[k][12]) for k in chaves], dtype=np.int64)
    B['bsh2'] = np.array([_int(e2[k][12]) for k in chaves], dtype=np.int64)
    B['junta2'] = np.array([e2[k][16] == '1' for k in chaves]); B['junta1'] = np.array([e1[k][16] == '1' for k in chaves])
    B['serie1'] = np.array([_int(e1[k][3]) for k in chaves], dtype=np.int64)
    B['serie2'] = np.array([_int(e2[k][3]) for k in chaves], dtype=np.int64)
    conf['comp2_estrutura_igual_base'] = int(sum(_int(e2[k][14]) == d[k]['2']['comp'] for k in chaves))
    conf['comp1_estrutura_igual_base'] = int(sum(_int(e1[k][14]) == d[k]['1']['comp'] for k in chaves))
    conf['local_estrutura_igual_base'] = int(sum(str(e2[k][0]) == str(d[k]['2']['loc']) for k in chaves))
    # perfil com agregadas
    P = np.zeros((n, len(COLS_PERFIL)), dtype=np.int64); nag = 0
    for i, k in enumerate(chaves):
        uf, mu, zo, se = k.split('|')
        secs = [se]
        a = e2[k][15]
        if a and a != '#NULO#':
            secs += [x.strip() for x in a.split('/') if x.strip()]; nag += 1
        for s in secs:
            v = pf.get(f'{uf}|{mu}|{zo}|{_int(s)}')
            if v is not None: P[i] += v
    B['perfil'] = P
    conf['secoes_com_agregadas'] = nag
    conf['perfil_total_igual_aptos_2t'] = int((P[:, 0] == B['apt2']).sum())
    conf['perfil_total_igual_aptos_1t'] = int((P[:, 0] == B['apt1']).sum())
    conf['sem_perfil'] = int((P[:, 0] == 0).sum())
    # posição no local (entre todas as seções do 2º turno do local)
    _, g = np.unique(B['local'], return_inverse=True)
    ordem = np.lexsort((B['secao'], g)); pos = np.zeros(n)
    cnt = np.bincount(g); ini = np.concatenate([[0], np.cumsum(cnt)[:-1]])
    rank = np.empty(n); rank[ordem] = np.arange(n) - ini[g[ordem]]
    B['pos'] = np.where(cnt[g] > 1, rank / np.maximum(cnt[g] - 1, 1), 0.0)
    # 2022
    d22 = carregar(DADOS + '/secoes2022.json.gz')
    tem = np.array([k in d22 and '1' in d22[k] and '2' in d22[k] for k in chaves])
    B['tem22'] = tem
    for t in ('1', '2'):
        for c in ('L', 'R', 'O', 'B', 'N', 'comp', 'apt'):
            B[f'{c}{t}_22'] = np.array([d22[k][t][c] if ok else 0 for k, ok in zip(chaves, tem)], dtype=np.int64)
    B['mesmo_local_22'] = np.array([ok and str(d22[k]['2']['loc']) == str(d[k]['2']['loc']) for k, ok in zip(chaves, tem)])
    conf['pareadas_2022'] = int(tem.sum()); conf['pareadas_2022_mesmo_codigo_de_local'] = int(B['mesmo_local_22'].sum())
    del d22
    # governador
    gc = carregar(DADOS + '/candidatos_gov_2026_1t_6ufs.json.gz')
    with gzip.open(TRAB + '/gov2t_6ufs_A6.json.gz', 'rt') as f: g2 = json.load(f)
    idx = {k: i for i, k in enumerate(chaves)}
    G = {}
    for uf in UFS_GOV:
        ks = [k for k in chaves if k.startswith(uf + '|') and k in g2 and '1g' in d[k]]
        ii = np.array([idx[k] for k in ks])
        n1 = sorted({c for k in ks for c in gc['secoes'].get(k, {})})
        n2 = sorted({c for k in ks for c in g2[k]['c']})
        G[uf] = {'i': ii, 'nums1': n1, 'nums2': n2,
                 'v1': np.array([[gc['secoes'].get(k, {}).get(c, 0) for c in n1] for k in ks], dtype=np.int64),
                 'v2': np.array([[g2[k]['c'].get(c, 0) for c in n2] for k in ks], dtype=np.int64),
                 'B1': np.array([d[k]['1g']['B'] for k in ks], dtype=np.int64),
                 'N1': np.array([d[k]['1g']['N'] for k in ks], dtype=np.int64),
                 'comp1': np.array([d[k]['1g']['comp'] for k in ks], dtype=np.int64),
                 'V2base': np.array([d[k].get('2g', {}).get('V', -1) for k in ks], dtype=np.int64)}
    conf['gov2t_validos_iguais_a_base'] = {uf: int((G[uf]['v2'].sum(1) == G[uf]['V2base']).sum()) for uf in UFS_GOV}
    conf['gov2t_secoes'] = {uf: int(len(G[uf]['i'])) for uf in UFS_GOV}
    conf['gov_nomes'] = gc.get('nomes', {})
    # logs
    with gzip.open(D1DIR + '/log_eleitor.json.gz', 'rt') as f: LG = json.load(f)
    lg = np.full((n, 8), -1, dtype=np.int64)  # B1 M1 S1 n1 B2 M2 S2 n2
    for k, v in LG.items():
        i = idx.get(k)
        if i is None or not v.get('1') or not v.get('2'): continue
        for t, off in (('1', 0), ('2', 4)):
            c = collections.Counter(e[3] for e in v[t]['el'])
            lg[i, off:off + 4] = [c.get('B', 0), c.get('M', 0), c.get('S', 0), len(v[t]['el'])]
    B['log'] = lg
    conf['amostra_logs_total'] = len(LG)
    conf['amostra_logs_dois_turnos_na_base'] = int((lg[:, 0] >= 0).sum())
    okl = lg[:, 0] >= 0
    conf['log_M2_igual_bweb'] = int((lg[okl, 5] == B['bsh2'][okl]).sum()); conf['log_M1_igual_bweb'] = int((lg[okl, 1] == B['bsh1'][okl]).sum())
    conf['log_n2_igual_comparecimento'] = int((lg[okl, 7] == B['comp2'][okl]).sum())
    conf['log_n1_igual_comparecimento'] = int((lg[okl, 3] == B['comp1'][okl]).sum())
    # exterior (à parte)
    kz = sorted(k for k, v in d.items() if '1' in v and '2' in v and k.startswith('ZZ|') and k in e1 and k in e2)
    Z = {'chave': np.array(kz), 'local': np.array(['|'.join(k.split('|')[:3]) + '|' + str(d[k]['2']['loc']) for k in kz]),
         'mun': np.array(['|'.join(k.split('|')[:2]) for k in kz])}
    for t in ('1', '2'):
        for c in ('L', 'R', 'O', 'B', 'N', 'comp', 'apt'):
            Z[c + t] = np.array([d[k][t][c] for k in kz], dtype=np.int64)
    Z['bsh1'] = np.array([_int(e1[k][12]) for k in kz], dtype=np.int64); Z['bsh2'] = np.array([_int(e2[k][12]) for k in kz], dtype=np.int64)
    for nm in ['13', '22'] + demais:
        Z['c' + nm] = np.array([cand['secoes'].get(k, {}).get(nm, 0) for k in kz], dtype=np.int64)
    return B, G, Z, conf, demais


# ---------------------------------------------------------------- variáveis
def variaveis(B, demais):
    """Monta desfechos, doses e as colunas de X (D2 a D5)."""
    S = {}
    f = lambda a, b: a / np.maximum(b, 1)
    V = (B['L2'] + B['R2']).astype(float)
    S['V'] = V
    S['y'] = 100 * f(B['L2'], V)
    S['yBN'] = 100 * f(B['B2'] + B['N2'], B['comp2'])
    S['m2'] = f(B['bsh2'], B['comp2']); S['m1'] = f(B['bsh1'], B['comp1'])
    P = B['perfil'].astype(float); tot = np.maximum(P[:, 0], 1)
    S['nb'] = 1 - P[:, 1] / tot
    X = {}
    X['p13'] = f(B['c13'], B['comp1']); X['p22'] = f(B['c22'], B['comp1'])
    for nm in demais: X['p' + nm] = f(B['c' + nm], B['comp1'])
    X['pB'] = f(B['B1'], B['comp1']); X['pN'] = f(B['N1'], B['comp1'])
    X['abst1'] = 1 - f(B['comp1'], B['apt1'])
    X['dabst'] = (1 - f(B['comp2'], B['apt2'])) - X['abst1']
    for c in PERFIL_X: X[c] = P[:, COLS_PERFIL.index(c)] / tot
    X['lnapt'] = np.log(np.maximum(B['apt2'], 1))
    X['pos'] = B['pos']
    S['X'] = X
    S['Xnomes'] = list(X.keys())
    md = np.array([modelo_urna(int(s), 2026) or 'outro' for s in B['serie2']])
    md1 = np.array([modelo_urna(int(s), 2026) or 'outro' for s in B['serie1']])
    S['modelo2'] = md; S['modelo1'] = md1
    S['MD'] = {m: (md == m).astype(float) for m in ['UE2013', 'UE2015', 'UE2022', 'outro'] if (md == m).any()}
    S['MD1'] = {m: (md1 == m).astype(float) for m in ['UE2013', 'UE2015', 'UE2022', 'outro'] if (md1 == m).any()}
    S['U'] = (~B['junta2']) & (V >= 30)
    S['temperfil'] = P[:, 0] > 0
    S['regiao'] = np.array([next(r for r, ufs in REGIOES.items() if u in ufs) for u in B['uf']])
    return S


def mat(cols):
    nomes = list(cols.keys())
    return np.column_stack([cols[c] for c in nomes]), nomes


def cols_base(S, dose, controles, sem=(), extra=None):
    c = collections.OrderedDict()
    for q, v in dose.items(): c[q] = v
    for q, v in controles.items(): c[q] = v
    for q in S['Xnomes']:
        if q in sem: continue
        c[q] = S['X'][q]
    for m, v in S['MD'].items(): c[m] = v
    if extra:
        for q, v in extra.items(): c[q] = v
    return c


def resumo_dose(r, nome_b='m2', nome_k='m1', S=None, m=None):
    o = {'n': r['n'], 'locais': r['locais'], 'agrupamentos': r['agrupamentos'], 'r2_dentro': r['r2_dentro'],
         'dp_residuo_pond': r['dp_residuo_pond'], 'b': linha(r, nome_b)}
    if nome_k and nome_k in r['coef']: o['k'] = linha(r, nome_k)
    if 'nb' in r['coef']: o['r_nb'] = linha(r, 'nb')
    b = o['b']
    o['Phi_letra'] = -b['coef'] / ESCALA
    o['Phi_letra_ic99'] = sorted([-b['ic99'][0] / ESCALA, -b['ic99'][1] / ESCALA])
    o['votos_trocados'] = o['Phi_letra'] * NECESSARIO
    o['votos_trocados_ic99'] = [x * NECESSARIO for x in o['Phi_letra_ic99']]
    o['votos_de_margem'] = o['Phi_letra'] * MARGEM
    o['votos_de_margem_ic99'] = [x * MARGEM for x in o['Phi_letra_ic99']]
    if 'k' in o: o['razao_k_sobre_b'] = abs(o['k']['coef']) / abs(b['coef']) if b['coef'] != 0 else None
    o['modelo_urna'] = {q: linha(r, q) for q in ('UE2013', 'UE2015', 'UE2022', 'outro') if q in r['coef']}
    o['retiradas'] = r['retiradas']
    return o


# ---------------------------------------------------------------- regressões do teste
def reg_dose(S, B, mask, cl=None, w=None, sem=(), so_m2=False):
    dose = {'m2': S['m2']}
    ctrl = collections.OrderedDict()
    if not so_m2: ctrl['m1'] = S['m1']
    ctrl['nb'] = S['nb']
    Xm, nomes = mat(cols_base(S, dose, ctrl, sem=sem))
    return Reg(Xm[mask], B['local'][mask], (B['mun'] if cl is None else cl)[mask], (S['V'] if w is None else w)[mask], nomes)


def reg_ind(S, B, mask, ind, com_m1=False):
    ctrl = collections.OrderedDict()
    if com_m1: ctrl['m1'] = S['m1']
    ctrl['nb'] = S['nb']
    Xm, nomes = mat(cols_base(S, {'ind': ind.astype(float)}, ctrl))
    return Reg(Xm[mask], B['local'][mask], B['mun'][mask], S['V'][mask], nomes)


def descr_ind(S, B, mask, ind):
    """Contagens e diferenças brutas (sem X) das tratadas contra as vizinhas do mesmo local."""
    loc = B['local'][mask]; t = ind[mask]; V = S['V'][mask]
    _, g = np.unique(loc, return_inverse=True); ng = g.max() + 1
    nt = np.bincount(g, weights=t, minlength=ng); nc = np.bincount(g, weights=~t, minlength=ng)
    inf = (nt > 0) & (nc > 0)
    o = {'tratadas_em_U': int(t.sum()), 'tratadas_em_local_com_vizinha': int(t[inf[g]].sum()),
         'locais_informativos': int(inf.sum()), 'vizinhas': int((~t)[inf[g]].sum())}
    if not inf.any(): return o
    y1 = 100 * B['L1'][mask] / np.maximum(B['L1'][mask] + B['R1'][mask], 1)
    Vt = np.bincount(g, weights=V * t, minlength=ng); Vc = np.bincount(g, weights=V * (~t), minlength=ng)

    def dif(x):
        mt = np.bincount(g, weights=V * t * x, minlength=ng)[inf] / Vt[inf]
        mc = np.bincount(g, weights=V * (~t) * x, minlength=ng)[inf] / Vc[inf]
        return float(((mt - mc) * Vt[inf]).sum() / Vt[inf].sum()), float((mt * Vt[inf]).sum() / Vt[inf].sum()), float((mc * Vt[inf]).sum() / Vt[inf].sum())
    for nm, x in (('m2', S['m2'][mask]), ('m1', S['m1'][mask]), ('y_2t', S['y'][mask]), ('y_1t', y1),
                  ('ganho_2t_menos_1t', S['y'][mask] - y1), ('yBN', S['yBN'][mask]), ('nb', S['nb'][mask])):
        d_, a_, c_ = dif(x)
        o['bruto_' + nm] = {'tratadas': a_, 'vizinhas': c_, 'diferenca': d_}
    o['votos_V_das_tratadas'] = float(Vt[inf].sum())
    o['comparecimento_2t_das_tratadas'] = float((B['comp2'][mask] * t)[inf[g]].sum())
    return o


def resumo_ind(r, desc, nome='ind'):
    o = dict(desc); o.update({'n': r['n'], 'locais': r['locais'], 'agrupamentos': r['agrupamentos'], 'd': linha(r, nome)})
    dm = desc.get('bruto_m2', {}).get('diferenca')
    if dm:
        o['esperado_para_Phi_1'] = -ESCALA * dm
        o['Phi_equivalente'] = -o['d']['coef'] / (ESCALA * dm)
        o['Phi_equivalente_ic99'] = sorted([-o['d']['ic99'][0] / (ESCALA * dm), -o['d']['ic99'][1] / (ESCALA * dm)])
    return o


def cols22(B, S):
    f = lambda a, b: a / np.maximum(b, 1)
    c = collections.OrderedDict()
    c['pL22'] = f(B['L1_22'], B['comp1_22']); c['pR22'] = f(B['R1_22'], B['comp1_22'])
    c['pB22'] = f(B['B1_22'], B['comp1_22']); c['pN22'] = f(B['N1_22'], B['comp1_22'])
    V22 = (B['L2_22'] + B['R2_22']).astype(float)
    y22 = 100 * f(B['L2_22'], V22)
    a1 = 1 - f(B['comp1_22'], B['apt1_22']); a2 = 1 - f(B['comp2_22'], B['apt2_22'])
    return c, y22, V22, a1, a2


def tabela_bruta(S, B, mask):
    faixas = [(0, 0.03), (0.03, 0.06), (0.06, 0.10), (0.10, 0.20), (0.20, 0.50), (0.50, 1.01)]
    y1 = 100 * B['L1'] / np.maximum(B['L1'] + B['R1'], 1)
    out = []
    for a, b in faixas:
        m = mask & (S['m2'] >= a) & (S['m2'] < b)
        if not m.any(): continue
        V = S['V'][m]
        out.append({'faixa_m2': [a, min(b, 1.0)], 'n': int(m.sum()), 'V': float(V.sum()), 'm2_medio': wmean(S['m2'][m], V),
                    'm1_medio': wmean(S['m1'][m], V), 'nb_medio': wmean(S['nb'][m], V),
                    'y_2t': float(100 * B['L2'][m].sum() / V.sum()),
                    'y_1t': float(100 * B['L1'][m].sum() / (B['L1'][m].sum() + B['R1'][m].sum())),
                    'yBN_2t': float(100 * (B['B2'][m] + B['N2'][m]).sum() / B['comp2'][m].sum()),
                    'yBN_1t': float(100 * (B['B1'][m] + B['N1'][m]).sum() / B['comp1'][m].sum())})
        out[-1]['ganho_2t_menos_1t'] = out[-1]['y_2t'] - out[-1]['y_1t']
    return out


# ---------------------------------------------------------------- calibração
def resumo_cal(arr_b, arr_ep, b0, alvo, sentido):
    """arr_b, arr_ep: coeficiente e erro das cópias; b0: observado; alvo: deslocamento esperado (com sinal)."""
    db = arr_b - b0
    s = np.sign(alvo)
    return {'delta_medio': float(db.mean()), 'delta_dp': float(db.std(ddof=1)), 'ep_medio': float(arr_ep.mean()),
            'esperado': float(alvo), 'recuperacao': float(db.mean() / alvo),
            'poder_z33': float((s * db / arr_ep >= Z_LIM).mean()), 't_medio': float((db / arr_ep).mean())}


def calibrar_principal(S, B, mask, R, RA, RB, RC, obs, rng, PAR):
    """D14 (a) e (b): plantio de R para L e, no espelho, de L para R. Mede b, k e os d do experimento natural."""
    L2 = B['L2'][mask]; R2 = B['R2'][mask]; V = S['V'][mask]; e = 1 - S['m2'][mask]
    out = {}
    for sent, orig, sinal in (('R_para_L', R2, 1), ('L_para_R', L2, -1)):
        for Phi in PHIS:
            chave = f'{sent}_Phi_{Phi}'
            if chave in PAR: out[chave] = PAR[chave]; continue
            f = Phi * NECESSARIO / float((e * orig).sum())
            rng = np.random.default_rng([SEMENTE, 10 + (0 if sinal == 1 else 3) + PHIS.index(Phi)])
            tb = np.empty(NREP); te = np.empty(NREP); tk = np.empty(NREP); tke = np.empty(NREP)
            nat = {q: (np.empty(NREP), np.empty(NREP)) for q in ('A', 'B', 'C')}
            mov = np.empty(NREP)
            for i in range(NREP):
                T = rng.binomial(orig, np.minimum(f * e, 1.0))
                yp = 100 * (L2 + sinal * T) / V
                q = R.rapido(yp, ['m2', 'm1'])
                tb[i], te[i] = q['m2']; tk[i], tke[i] = q['m1']; mov[i] = T.sum()
                for nm, RR in (('A', RA), ('B', RB), ('C', RC)):
                    nat[nm][0][i], nat[nm][1][i] = RR.rapido(yp, ['ind'])['ind']
            o = {'Phi': Phi, 'sentido': sent, 'f': f, 'votos_movidos_medio': float(mov.mean()), 'repeticoes': NREP}
            o['b'] = resumo_cal(tb, te, obs['b'], -sinal * ESCALA * Phi, sent)
            o['k'] = {'delta_medio': float((tk - obs['k']).mean()), 'delta_dp': float((tk - obs['k']).std(ddof=1)),
                      'razao_delta_k_sobre_delta_b': float(abs((tk - obs['k']).mean()) / abs((tb - obs['b']).mean()))}
            # como está: condições numéricas de SINAL e de SEM SINAL aplicadas à cópia
            z = tb / te
            o['copia_cumpre_SINAL_numerico'] = float(((np.abs(tb) >= LIM_B) & (np.abs(z) >= Z_LIM) & (np.abs(tk) < np.abs(tb) / 2) & (np.sign(tb) == -sinal)).mean())
            dentro = (tb - Z99 * te >= -LIM_B) & (tb + Z99 * te <= LIM_B)
            o['eps_copia_nao_passa_SEM_SINAL'] = float((~dentro).mean())
            # recentrado: como se o observado fosse zero
            db = tb - obs['b']
            dentro0 = (db - Z99 * te >= -LIM_B) & (db + Z99 * te <= LIM_B)
            o['eps_recentrado'] = float((~dentro0).mean())
            o['SINAL_numerico_recentrado'] = float(((np.abs(db) >= LIM_B) & (np.abs(db / te) >= Z_LIM)).mean())
            for nm in ('A', 'B', 'C'):
                dd = nat[nm][0] - obs['d' + nm]
                o['nat_' + nm] = {'delta_medio': float(dd.mean()), 'delta_dp': float(dd.std(ddof=1)), 'ep_medio': float(nat[nm][1].mean()),
                                  't_medio': float((dd / nat[nm][1]).mean()),
                                  'poder_z33': float((sinal * dd / nat[nm][1] <= -Z_LIM).mean())}
            out[chave] = o; PAR[chave] = o
            gravar('parcial_calibracao_principal.json', PAR)
            log('calibração', chave, 'delta b', round(o['b']['delta_medio'], 4), 'rec', round(o['b']['recuperacao'], 3), 'poder', o['b']['poder_z33'])
    return out


def calibrar_bn(S, B, mask, R, obs_b, rng, escala_bn):
    BN = (B['B2'] + B['N2'])[mask]; comp = B['comp2'][mask]; e = 1 - S['m2'][mask]
    out = {}
    for Phi in PHIS:
        f = Phi * MARGEM / float((e * BN).sum())
        if f * e.max() > 1:
            out[f'Phi_BN_{Phi}'] = {'Phi_BN': Phi, 'f': f, 'pulado': 'taxa maior que 1'}; continue
        tb = np.empty(NREP); te = np.empty(NREP); mov = np.empty(NREP)
        for i in range(NREP):
            T = rng.binomial(BN, f * e)
            q = R.rapido(100 * (BN - T) / np.maximum(comp, 1), ['m2'])
            tb[i], te[i] = q['m2']; mov[i] = T.sum()
        o = {'Phi_BN': Phi, 'f': f, 'votos_convertidos_medio': float(mov.mean()), 'repeticoes': NREP}
        dPhi = (tb - obs_b) * escala_bn
        o['delta_b_medio'] = float((tb - obs_b).mean()); o['ep_medio'] = float(te.mean())
        o['delta_Phi_BN_medio'] = float(dPhi.mean()); o['recuperacao'] = float(dPhi.mean() / Phi)
        o['poder_z33'] = float(((tb - obs_b) / te >= Z_LIM).mean()); o['t_medio'] = float(((tb - obs_b) / te).mean())
        out[f'Phi_BN_{Phi}'] = o
        log('calibração BN', Phi, o['delta_Phi_BN_medio'], o['poder_z33'])
    return out


def calibrar_logs(S, B, mask, Ra, Rb, fB2, obs, rng):
    L2 = B['L2'][mask]; R2 = B['R2'][mask]; V = S['V'][mask]; e = fB2[mask]
    out = {}
    for Phi in PHIS:
        g = Phi * (NECESSARIO / R2_OFICIAL) * float(R2.sum()) / float((e * R2).sum())
        tb = np.empty(NREP); te = np.empty(NREP); tm = np.empty(NREP); tme = np.empty(NREP); ts = np.empty(NREP); tse = np.empty(NREP)
        for i in range(NREP):
            T = rng.binomial(R2, g * e)
            yp = 100 * (L2 + T) / V
            tb[i], te[i] = Rb.rapido(yp, ['u2'])['u2']
            q = Ra.rapido(yp, ['fM2', 'fS2']); tm[i], tme[i] = q['fM2']; ts[i], tse[i] = q['fS2']
        o = {'Phi': Phi, 'g': g, 'repeticoes': NREP,
             'u2': resumo_cal(tb, te, obs['u2'], -ESCALA * Phi, ''), 'fM2': resumo_cal(tm, tme, obs['fM2'], -ESCALA * Phi, ''),
             'fS2': resumo_cal(ts, tse, obs['fS2'], -ESCALA * Phi, '')}
        out[f'Phi_{Phi}'] = o
        log('calibração logs', Phi, o['u2']['delta_medio'], o['u2']['poder_z33'])
    return out


# ---------------------------------------------------------------- vereditos (regras D15 e D16, escritas antes de rodar)
def dentro_ic(l, lim):
    return l['ic99'][0] >= -lim and l['ic99'][1] <= lim


def vereditos(res):
    v = {}
    P = res['principal']; cal = res['calibracao_principal']; nat = res['experimento_natural']
    b = P['b']; k = P['k']
    c1 = cal['R_para_L_Phi_1.0']; c25 = cal['R_para_L_Phi_0.25']
    sem_poder = (not (0.80 <= c1['b']['recuperacao'] <= 1.25)) or c1['b']['poder_z33'] < 0.95 or c25['eps_copia_nao_passa_SEM_SINAL'] < 0.95
    reg_ok = res['regioes']['mesmo_sentido_que_o_nacional'] >= 4
    num_sinal = abs(b['coef']) >= LIM_B and abs(b['z']) >= Z_LIM and abs(k['coef']) < abs(b['coef']) / 2
    dA = nat['A']['d']
    nat_mesmo = np.sign(dA['coef']) == np.sign(b['coef'])
    lg = res['logs']['conta_b_restrita']['b']
    log_mesmo = np.sign(lg['coef']) == np.sign(b['coef'])
    plc = res['placebos']
    plc_limpo = all(abs(plc[q]['Phi_letra']) <= 1 / 3 for q in ('periodo_anterior', 'turno_trocado', 'cargo_governador')) and abs(nat['C']['d']['z']) < Z_LIM
    # parte dose
    if num_sinal and reg_ok: v['dose_y'] = 'SINAL'
    elif dentro_ic(b, LIM_B): v['dose_y'] = 'SEM SINAL'
    else: v['dose_y'] = 'INCONCLUSIVO'
    if sem_poder: v['dose_y'] = 'SEM PODER'
    # combinado pela letra
    if sem_poder: v['teste_pela_letra'] = 'SEM PODER'
    elif num_sinal and reg_ok and nat_mesmo and log_mesmo and plc_limpo:
        v['teste_pela_letra'] = 'SINAL' + (' (a favor de Lula)' if b['coef'] < 0 else ' CONTRÁRIO (a favor de Flávio)')
    elif dentro_ic(b, LIM_B) and abs(dA['coef']) <= LIM_NAT: v['teste_pela_letra'] = 'SEM SINAL'
    else: v['teste_pela_letra'] = 'INCONCLUSIVO'
    v['condicoes'] = {'sem_poder_D15': bool(sem_poder), 'b_no_limite_ou_alem': bool(abs(b['coef']) >= LIM_B), 'z_3_3': bool(abs(b['z']) >= Z_LIM),
                      'k_menor_que_metade_de_b': bool(abs(k['coef']) < abs(b['coef']) / 2), 'regioes_4_de_5': bool(reg_ok),
                      'mesmo_sentido_experimento_natural_A': bool(nat_mesmo), 'mesmo_sentido_logs': bool(log_mesmo),
                      'placebos_limpos': bool(plc_limpo), 'ic99_de_b_dentro_de_0_51': bool(dentro_ic(b, LIM_B)),
                      'd_A_dentro_de_0_6': bool(abs(dA['coef']) <= LIM_NAT),
                      'poder_95_para_Phi_0_25_regra_geral': bool(c25['b']['poder_z33'] >= 0.95)}
    # experimento natural
    pA = c1['nat_A']['poder_z33']; pB = c1['nat_B']['poder_z33']
    if pA < 0.95: v['experimento_natural_A'] = 'SEM PODER'
    elif abs(dA['coef']) > LIM_NAT and abs(dA['z']) >= Z_LIM and abs(nat['C']['d']['z']) < Z_LIM: v['experimento_natural_A'] = 'SINAL'
    elif abs(dA['coef']) <= LIM_NAT: v['experimento_natural_A'] = 'SEM SINAL'
    else: v['experimento_natural_A'] = 'INCONCLUSIVO'
    dB = nat['B']['d']; alvoB = c1['nat_B']['delta_medio']
    if pB < 0.95: v['experimento_natural_B'] = 'SEM PODER'
    elif abs(dB['z']) >= Z_LIM: v['experimento_natural_B'] = 'SINAL'
    elif not (dB['ic99'][0] <= alvoB <= dB['ic99'][1]): v['experimento_natural_B'] = 'SEM SINAL'
    else: v['experimento_natural_B'] = 'INCONCLUSIVO'
    v['experimento_natural_A_pela_letra_sem_olhar_poder'] = 'dentro de 0,6' if abs(dA['coef']) <= LIM_NAT else 'fora de 0,6'
    # logs
    kl = res['logs']['conta_b_restrita']['k']
    cl1 = res['calibracao_logs']['Phi_1.0']['u2']
    if abs(lg['coef']) >= LIM_B and abs(lg['z']) >= Z_LIM and abs(kl['coef']) < abs(lg['coef']) / 2: v['logs'] = 'SINAL'
    elif cl1['poder_z33'] < 0.95: v['logs'] = 'SEM PODER'
    elif dentro_ic(lg, LIM_B): v['logs'] = 'SEM SINAL'
    else: v['logs'] = 'INCONCLUSIVO'
    # y_BN
    bn = res['yBN']['principal']
    plantados = [res['calibracao_yBN'][q] for q in sorted(res['calibracao_yBN']) if 'poder_z33' in res['calibracao_yBN'][q]]
    cbn = plantados[-1] if plantados else {}  # Phi_BN = 1 não pôde ser plantado (taxa maior que 1): vale o maior tamanho plantado
    phi = bn['Phi_BN']; ic = bn['Phi_BN_ic99']
    if abs(phi) >= 0.25 and abs(bn['b']['z']) >= Z_LIM and abs(bn['k']['coef']) < abs(bn['b']['coef']) / 2: v['yBN'] = 'SINAL'
    elif cbn.get('poder_z33', 0) < 0.95: v['yBN'] = 'SEM PODER'
    elif ic[0] >= -0.25 and ic[1] <= 0.25: v['yBN'] = 'SEM SINAL'
    else: v['yBN'] = 'INCONCLUSIVO'
    # y_alt
    a = res['y_alt']['principal']
    if abs(a['b']['coef']) >= LIM_B and abs(a['b']['z']) >= Z_LIM and abs(a['k']['coef']) < abs(a['b']['coef']) / 2: v['y_alt'] = 'SINAL'
    elif dentro_ic(a['b'], LIM_B): v['y_alt'] = 'SEM SINAL'
    else: v['y_alt'] = 'INCONCLUSIVO'
    v['placebos'] = {q: ('limpo' if abs(plc[q]['Phi_letra']) <= 1 / 3 else 'não limpo') for q in ('periodo_anterior', 'turno_trocado', 'cargo_governador')}
    v['placebos']['espelho_experimento_natural_C'] = 'limpo' if abs(nat['C']['d']['z']) < Z_LIM else 'não limpo'
    return v


def wcorr(a, b, w):
    ma = (a * w).sum() / w.sum(); mb = (b * w).sum() / w.sum()
    return float((w * (a - ma) * (b - mb)).sum() / np.sqrt((w * (a - ma) ** 2).sum() * (w * (b - mb) ** 2).sum()))


def placebo_governador(S, B, G, U):
    from scipy.stats import chi2
    out = {'por_uf': {}}
    bs = []; eps = []
    for uf in UFS_GOV:
        g = G[uf]; i = g['i']
        o = {'secoes_com_governador': int(len(i)), 'candidatos_2t': g['nums2']}
        if g['v2'].shape[1] != 2:
            o['erro'] = 'não há exatamente dois candidatos no 2º turno'; out['por_uf'][uf] = o; continue
        V2 = g['v2'].sum(1).astype(float)
        m = U[i] & (V2 >= 30) & (g['comp1'] > 0)
        yA = 100 * g['v2'][:, 0] / np.maximum(V2, 1)
        cor = wcorr(yA[m], S['y'][i][m], V2[m])
        lado = 0 if cor >= 0 else 1
        yg = yA if lado == 0 else 100 - yA
        o['lado_de_Lula'] = g['nums2'][lado]; o['correlacao_com_y'] = cor if lado == 0 else -cor
        comp1 = np.maximum(g['comp1'], 1).astype(float)
        frac = g['v1'].sum(0) / g['comp1'].sum()
        inc = [j for j in np.argsort(-frac) if frac[j] >= 0.005]
        if len(inc) == g['v1'].shape[1]: inc = inc[:-1]  # sem resto: o menor vira a referência
        c = collections.OrderedDict()
        c['m2'] = S['m2'][i]; c['m1'] = S['m1'][i]; c['nb'] = S['nb'][i]
        for j in inc: c['g' + g['nums1'][j]] = g['v1'][:, j] / comp1
        c['gB'] = g['B1'] / comp1; c['gN'] = g['N1'] / comp1
        for q in ['abst1', 'dabst'] + PERFIL_X + ['lnapt', 'pos']: c[q] = S['X'][q][i]
        for q, vv in S['MD'].items(): c[q] = vv[i]
        Xm, nomes = mat(c)
        R = Reg(Xm[m], B['local'][i][m], B['local'][i][m], V2[m], nomes)
        r = R.fit(yg[m])
        o.update({'n': r['n'], 'locais': r['locais'], 'b': linha(r, 'm2'), 'k': linha(r, 'm1'), 'erro': 'agrupado por local',
                  'candidatos_1t_no_X': [g['nums1'][j] for j in inc], 'retiradas': r['retiradas']})
        nm = len(set(B['mun'][i][m]))
        o['municipios'] = nm
        if nm >= 30:
            r2 = Reg(Xm[m], B['local'][i][m], B['mun'][i][m], V2[m], nomes).fit(yg[m])
            o['b_erro_por_municipio'] = linha(r2, 'm2')
        out['por_uf'][uf] = o; bs.append(o['b']['coef']); eps.append(o['b']['ep'])
    bs = np.array(bs); eps = np.array(eps); w = 1 / eps ** 2
    bp = float((bs * w).sum() / w.sum()); ep = float(np.sqrt(1 / w.sum()))
    q = float(((bs / eps) ** 2).sum())
    out.update({'b': {'coef': bp, 'ep': ep, 'z': bp / ep, 'ic99': [bp - Z99 * ep, bp + Z99 * ep]}, 'ufs': int(len(bs)),
                'qui2_dos_z': q, 'gl': int(len(bs)), 'p_qui2': float(chi2.sf(q, len(bs))), 'Phi_letra': -bp / ESCALA})
    return out


def exterior(Z, demais):
    f = lambda a, b: a / np.maximum(b, 1)
    V = (Z['L2'] + Z['R2']).astype(float); m = V >= 30
    m2 = f(Z['bsh2'], Z['comp2']); m1 = f(Z['bsh1'], Z['comp1'])
    o = {'secoes_pareadas': int(len(V)), 'com_30_ou_mais': int(m.sum()), 'm2_medio': wmean(m2[m], V[m]) if m.any() else None,
         'm1_medio': wmean(m1[m], V[m]) if m.any() else None, 'secoes_com_m2_maior_que_zero': int((m2[m] > 0).sum()),
         'soma_biom_sem_habilitacao_2t': int(Z['bsh2'].sum()), 'comparecimento_2t': int(Z['comp2'].sum())}
    if (m2[m] > 0).sum() < 30:
        o['modelo'] = 'não rodado: m2 quase sem variação no exterior'; return o
    c = collections.OrderedDict()
    c['m2'] = m2; c['m1'] = m1
    c['p13'] = f(Z['c13'], Z['comp1']); c['p22'] = f(Z['c22'], Z['comp1'])
    for nm in demais: c['p' + nm] = f(Z['c' + nm], Z['comp1'])
    c['pB'] = f(Z['B1'], Z['comp1']); c['pN'] = f(Z['N1'], Z['comp1'])
    c['abst1'] = 1 - f(Z['comp1'], Z['apt1']); c['dabst'] = (1 - f(Z['comp2'], Z['apt2'])) - c['abst1']
    c['lnapt'] = np.log(np.maximum(Z['apt2'], 1))
    Xm, nomes = mat(c)
    try:
        r = Reg(Xm[m], Z['local'][m], Z['mun'][m], V[m], nomes).fit((100 * f(Z['L2'], V))[m])
        o['modelo'] = {'n': r['n'], 'locais': r['locais'], 'agrupamentos': r['agrupamentos'], 'b': linha(r, 'm2'), 'k': linha(r, 'm1'),
                       'nota': 'sem perfil, sem nb, sem modelo da urna e sem posição; erro agrupado por cidade do exterior'}
    except Exception as e:
        o['modelo'] = 'não rodado: ' + str(e)
    return o


# ---------------------------------------------------------------- EXPLORATÓRIO (feito depois de ver o resultado)
def exploratorio_nb_por_idade(S, B, U, y, y22, V22, M22, c22, a1_22, a2_22):
    """EXPLORATÓRIO. O coeficiente de nb (eleitores sem biometria no cadastro) saiu negativo e forte. O registro já
    dizia que nb é traço do eleitorado e não decide. Pergunta: o coeficiente é igual para o eleitor sem biometria de
    qualquer idade (como seria se fosse exposição ao programa) ou muda com a idade (tipo de eleitor)?"""
    arq = TRAB + '/perfil_nb_idade_A6.json.gz'
    if not os.path.exists(arq): return {'nao_rodado': 'falta ' + arq}
    with gzip.open(arq, 'rt') as f: pf = json.load(f)
    cols = pf['colunas']; pf = pf['secoes']
    with gzip.open(D1DIR + '/estrutura_2t.json.gz', 'rt') as f: e2 = json.load(f)
    n = len(B['chave']); P = np.zeros((n, len(cols)))
    for i, k in enumerate(B['chave']):
        uf, mu, zo, se = k.split('|'); secs = [se]; a = e2[k][15]
        if a and a != '#NULO#': secs += [x.strip() for x in a.split('/') if x.strip()]
        for q in secs:
            v = pf.get(f'{uf}|{mu}|{zo}|{_int(q)}')
            if v is not None: P[i] += v
    del e2, pf
    tot = np.maximum(B['perfil'][:, 0], 1).astype(float)
    ix = {c: j for j, c in enumerate(cols)}
    comp = collections.OrderedDict()
    comp['nb_16a19'] = (P[:, ix['n1617']] + P[:, ix['n1819']]) / tot
    comp['nb_20a24'] = P[:, ix['n2024']] / tot
    comp['nb_25a44'] = (P[:, ix['n2534']] + P[:, ix['n3544']]) / tot
    comp['nb_45a59'] = P[:, ix['n4559']] / tot
    comp['nb_60mais'] = (P[:, ix['n6069']] + P[:, ix['n70m']]) / tot
    soma = sum(comp.values())
    o = {'nota': 'EXPLORATÓRIO, feito depois de ver o resultado; não decide',
         'sem_biometria_no_pais_por_idade': {c: int(P[U][:, ix[c]].sum()) for c in cols if c.startswith('n')},
         'fracao_sem_biometria_entre_18_e_19': float(P[U][:, ix['n1819']].sum() / max(P[U][:, ix['t1819']].sum(), 1)),
         'fracao_sem_biometria_entre_20_e_24': float(P[U][:, ix['n2024']].sum() / max(P[U][:, ix['t2024']].sum(), 1)),
         'sem_biometria_total_perfil': int((B['perfil'][U][:, 0] - B['perfil'][U][:, 1]).sum()),
         'correlacao_soma_das_faixas_com_nb': float(np.corrcoef(soma[U], S['nb'][U])[0, 1])}
    o['parcela_dos_sem_biometria_com_20_a_24_anos'] = o['sem_biometria_no_pais_por_idade']['n2024'] / max(o['sem_biometria_total_perfil'], 1)
    # modelo base com nb aberto por idade (2026)
    ctrl = collections.OrderedDict([('m1', S['m1'])]); ctrl.update(comp)
    c = collections.OrderedDict([('m2', S['m2'])]); c.update(ctrl)
    for q in S['Xnomes']: c[q] = S['X'][q]
    for q, vv in S['MD'].items(): c[q] = vv
    Xm, nomes = mat(c)
    r = Reg(Xm[U], B['local'][U], B['mun'][U], S['V'][U], nomes).fit(y[U])
    o['modelo_2026_nb_aberto_por_idade'] = {q: linha(r, q) for q in ['m2', 'm1'] + list(comp)}
    del Xm
    # mesma abertura na virada de 2022 (placebo de período anterior)
    ex = collections.OrderedDict(c22); ex['abst1_22'] = a1_22; ex['dabst_22'] = a2_22 - a1_22
    ex['lnapt22'] = np.log(np.maximum(B['apt2_22'], 1)); ex['pos'] = S['X']['pos']
    c = collections.OrderedDict([('m2', S['m2']), ('m1', S['m1'])]); c.update(comp); c.update(ex)
    for q in PERFIL_X: c[q] = S['X'][q]
    for q, vv in S['MD'].items(): c[q] = vv
    Xm, nomes = mat(c)
    r2 = Reg(Xm[M22], B['local'][M22], B['mun'][M22], V22[M22], nomes).fit(y22[M22])
    o['virada_de_2022_nb_aberto_por_idade'] = {q: linha(r2, q) for q in ['m2', 'm1'] + list(comp)}
    return o


def exploratorio_logs(S, B, U, y):
    """EXPLORATÓRIO. Na amostra de logs a fração S do dia saiu com coeficiente positivo e grande, com o do 1º turno do
    mesmo tamanho e sinal oposto. Reescreve a conta em nível e variação, roda o modelo nacional só na amostra e mede
    quem compareceu a mais no 2º turno por tipo de habilitação (estrutura)."""
    lg = B['log']; UL = U & (lg[:, 0] >= 0)
    fr = lambda j, t: lg[:, j] / np.maximum(lg[:, t], 1)
    fM1, fS1, fM2, fS2 = fr(1, 3), fr(2, 3), fr(5, 7), fr(6, 7)
    c = collections.OrderedDict([('S_variacao', fS2 - fS1), ('S_nivel_1t', fS1), ('M_variacao', fM2 - fM1), ('M_nivel_1t', fM1)])
    for q in S['Xnomes']: c[q] = S['X'][q]
    for q, vv in S['MD'].items(): c[q] = vv
    Xm, nomes = mat(c)
    r = Reg(Xm[UL], B['local'][UL], B['mun'][UL], S['V'][UL], nomes).fit(y[UL])
    o = {'nota': 'EXPLORATÓRIO, feito depois de ver o resultado; não decide',
         'nivel_e_variacao': {q: linha(r, q) for q in ('S_variacao', 'S_nivel_1t', 'M_variacao', 'M_nivel_1t')}}
    Rn = reg_dose(S, B, UL); rn = Rn.fit(y[UL])
    o['modelo_nacional_so_na_amostra'] = {'n': rn['n'], 'b_m2': linha(rn, 'm2'), 'k_m1': linha(rn, 'm1'), 'r_nb': linha(rn, 'nb')}
    o['comparecimento_por_tipo_na_amostra'] = {t: {'1t': int(lg[UL, a].sum()), '2t': int(lg[UL, b].sum()), 'variacao_pct': float(100 * (lg[UL, b].sum() / lg[UL, a].sum() - 1))}
                                               for t, a, b in (('B_biometrica', 0, 4), ('M_mesario', 1, 5), ('S_sem_biometria', 2, 6))}
    dS = (fS2 - fS1)[UL]
    o['dp_da_variacao_de_S'] = float(dS.std()); o['efeito_de_um_dp_da_variacao_de_S_em_pp'] = float(dS.std() * r['coef']['S_variacao'])
    _, g = np.unique(B['local'][UL], return_inverse=True); cn = np.bincount(g); ok = cn[g] >= 2
    wm = lambda x: (x - (np.bincount(g, weights=x) / cn)[g])[ok]
    o['correlacao_dentro_do_local_fS2_com'] = {q: float(np.corrcoef(wm(fS2[UL]), wm(S['X'][q][UL]))[0, 1]) for q in ('i1617', 'i1824', 'i2534', 'i6069', 'i7079', 'i80m')}
    return o


def exploratorio_bruto_por_nb(S, B, U):
    """EXPLORATÓRIO. Valor bruto de 2026 por faixa de nb (eleitores sem biometria no cadastro)."""
    y1 = lambda m: float(100 * B['L1'][m].sum() / (B['L1'][m].sum() + B['R1'][m].sum()))
    qs = np.quantile(S['nb'][U], [0, 0.2, 0.4, 0.6, 0.8, 1.0]); out = []
    for i in range(5):
        m = U & (S['nb'] >= qs[i]) & ((S['nb'] < qs[i + 1]) if i < 4 else (S['nb'] <= qs[i + 1]))
        a = float(100 * B['L2'][m].sum() / S['V'][m].sum()); b = y1(m)
        out.append({'quinto_de_nb': i + 1, 'nb_de': float(qs[i]), 'nb_ate': float(qs[i + 1]), 'n': int(m.sum()), 'V': float(S['V'][m].sum()),
                    'nb_medio': wmean(S['nb'][m], S['V'][m]), 'y_2t': a, 'y_1t': b, 'ganho_2t_menos_1t': a - b})
    return out


def exploratorio_escada(S, B, U, y):
    """EXPLORATÓRIO. No bruto o ganho de Lula entre os turnos cai conforme m2 sobe. A escada mostra a inclinação do
    ganho bruto (y menos a fração de Lula sobre Lula mais Flávio no 1º turno) em m2, comparando vizinhos cada vez
    mais próximos: país, UF, município, local, e por fim o modelo do registro."""
    y1 = 100 * B['L1'] / np.maximum(B['L1'] + B['R1'], 1)
    ganho = y - y1
    out = {}
    for nome, fe in (('sem_efeito_fixo', np.zeros(len(y), dtype=int)), ('efeito_fixo_de_UF', B['uf']), ('efeito_fixo_de_municipio', B['mun']),
                     ('efeito_fixo_de_local', B['local'])):
        r = Reg(S['m2'][U][:, None], fe[U], B['mun'][U], S['V'][U], ['m2']).fit(ganho[U])
        r2 = Reg(np.column_stack([S['m2'][U], S['m1'][U]]), fe[U], B['mun'][U], S['V'][U], ['m2', 'm1']).fit(ganho[U])
        out[nome] = {'n': r['n'], 'so_m2': linha(r, 'm2'), 'com_m1': {'m2': linha(r2, 'm2'), 'm1': linha(r2, 'm1')}}
    # dentro do local: que bloco de controles desfaz a inclinação (desfecho y, como no registro)
    blocos = collections.OrderedDict()
    blocos['votos_do_1t'] = ['p13', 'p22'] + [q for q in S['Xnomes'] if q.startswith('p') and q not in ('p13', 'p22', 'pos')]
    blocos['abstencao'] = ['abst1', 'dabst']
    blocos['nb'] = ['nb']
    blocos['perfil_aptos_posicao_modelo'] = PERFIL_X + ['lnapt', 'pos'] + list(S['MD'])
    cols = collections.OrderedDict([('m2', S['m2']), ('m1', S['m1'])]); esc = {}
    y1c = collections.OrderedDict([('y1', y1)])
    r0 = Reg(np.column_stack([S['m2'][U], S['m1'][U], y1[U]]), B['local'][U], B['mun'][U], S['V'][U], ['m2', 'm1', 'y1']).fit(y[U])
    esc['so_a_fracao_de_Lula_no_1t_como_controle'] = {'m2': linha(r0, 'm2'), 'm1': linha(r0, 'm1')}
    for nome, lista in blocos.items():
        for q in lista:
            cols[q] = S['nb'] if q == 'nb' else (S['MD'][q] if q in S['MD'] else S['X'][q])
        Xm, nomes = mat(cols)
        rr = Reg(Xm[U], B['local'][U], B['mun'][U], S['V'][U], nomes).fit(y[U])
        esc['ate_' + nome] = {'m2': linha(rr, 'm2'), 'm1': linha(rr, 'm1')}
    out['dentro_do_local_acrescentando_blocos'] = esc
    # dose e resposta no ganho bruto dentro do local: inclinação abaixo e acima de m2 = 0,2 e o grupo A sem controles
    lo = np.minimum(S['m2'], 0.2); hi = np.maximum(S['m2'] - 0.2, 0)
    rs = Reg(np.column_stack([lo[U], hi[U]]), B['local'][U], B['mun'][U], S['V'][U], ['m2_ate_0_2', 'm2_acima_de_0_2']).fit(ganho[U])
    out['ganho_bruto_dentro_do_local_por_trecho_de_m2'] = {q: linha(rs, q) for q in ('m2_ate_0_2', 'm2_acima_de_0_2')}
    out['secoes_com_m2_acima_de_0_2'] = int((S['m2'][U] > 0.2).sum())
    for nome, ind in (('A_m2_0_5_ou_mais', S['m2'] >= 0.5), ('B_leitor_caiu', (S['m2'] >= 0.2) & (S['m1'] < 0.1)), ('C_espelho', (S['m1'] >= 0.2) & (S['m2'] < 0.1))):
        ri = Reg(ind[U].astype(float)[:, None], B['local'][U], B['mun'][U], S['V'][U], ['ind']).fit(ganho[U])
        out['ganho_bruto_dentro_do_local_grupo_' + nome] = linha(ri, 'ind')
    return out


def conferencia_pandas(Xm, nomes, y, w, local, mun):
    """Refaz b e o erro agrupado por município por outro caminho (pandas e lstsq), sem usar a classe Reg."""
    import pandas as pd
    g = pd.Series(local); W = pd.Series(w); sw = W.groupby(g).transform('sum').values
    dm = lambda v: v - (pd.Series(v * w).groupby(g).transform('sum').values / sw)
    Xd = np.column_stack([dm(Xm[:, j]) for j in range(Xm.shape[1])]); yd = dm(y)
    rw = np.sqrt(w)
    coef, *_ = np.linalg.lstsq(Xd * rw[:, None], yd * rw, rcond=None)
    e = yd - Xd @ coef
    sc = pd.DataFrame(Xd * (w * e)[:, None]).groupby(pd.Series(mun).values).sum().values
    bread = np.linalg.inv((Xd * w[:, None]).T @ Xd)
    Vc = bread @ (sc.T @ sc) @ bread
    G = sc.shape[0]
    j = nomes.index('m2')
    return {'b': float(coef[j]), 'ep_sem_correcao_de_amostra_finita': float(np.sqrt(Vc[j, j])), 'ep_com_G_sobre_G_menos_1': float(np.sqrt(Vc[j, j] * G / (G - 1))), 'municipios': int(G)}


def sha_docstring():
    return hashlib.sha256(__doc__.encode()).hexdigest()


def base_em_cache():
    """Guarda a base montada em disco (pickle compactado) para não reler os JSON a cada rodada."""
    import pickle
    arq = TRAB + '/base_A6.pkl.gz'
    if os.path.exists(arq):
        with gzip.open(arq, 'rb') as fh: return pickle.load(fh)
    t = montar_base()
    with gzip.open(arq + '.tmp', 'wb', compresslevel=3) as fh: pickle.dump(t, fh, protocol=4)
    os.replace(arq + '.tmp', arq)
    return t


def rodar():
    os.makedirs(TRAB, exist_ok=True)
    B, G, Z, conf, demais = base_em_cache()
    S = variaveis(B, demais)
    res = {'teste': 'R27_A6: tipo de habilitação (D1.5 de desenho_D1_proposta.json)',
           'registro': 'PRE-REGISTRO-2026-10-26.md, Adendo 27 (commit 2748895); registro/adendo27/desenho_D1_proposta.json, teste D1.5 e definições comuns',
           'docstring_sha256': sha_docstring(), 'semente': SEMENTE, 'repeticoes': NREP, 'conferencias': conf}
    U0 = S['U']; U = U0 & S['temperfil']
    V = S['V']; y = S['y']; yBN = S['yBN']
    # resto dos candidatos tem variação? (senão as frações somariam 1 com o efeito fixo)
    resto = 1 - sum(S['X'][q] for q in ['p13', 'p22'] + ['p' + n for n in demais] + ['pB', 'pN'])
    conf['perfil_total_dentro_de_2_por_cento_dos_aptos_2t'] = int((np.abs(B['perfil'][:, 0] / np.maximum(B['apt2'], 1) - 1) <= 0.02).sum())
    conf['resto_agrupado_fracao_media'] = wmean(resto[U], B['comp1'][U]); conf['resto_agrupado_maximo'] = float(resto[U].max())
    _, gl = np.unique(B['local'][U], return_inverse=True); cnt = np.bincount(gl); inf = cnt[gl] >= 2
    wm = lambda x: x - (np.bincount(gl, weights=x) / cnt)[gl]
    res['universo'] = {
        'pareadas_fora_exterior': int(len(V)), 'junta_2t': int(B['junta2'].sum()), 'junta_1t': int(B['junta1'].sum()),
        'L2_mais_R2_abaixo_de_30': int(((V < 30) & ~B['junta2']).sum()), 'U_pela_letra': int(U0.sum()),
        'sem_perfil_em_U': int((U0 & ~S['temperfil']).sum()), 'U_com_perfil': int(U.sum()),
        'U_em_local_com_2_ou_mais': int(inf.sum()), 'locais_com_2_ou_mais': int((cnt >= 2).sum()),
        'municipios': int(len(set(B['mun'][U]))), 'V_total': float(V[U].sum()), 'L2': int(B['L2'][U].sum()), 'R2': int(B['R2'][U].sum()),
        'y_agregado': float(100 * B['L2'][U].sum() / V[U].sum()),
        'm2_medio_pond': wmean(S['m2'][U], V[U]), 'm1_medio_pond': wmean(S['m1'][U], V[U]), 'nb_medio_pond': wmean(S['nb'][U], V[U]),
        'm2_mediana': float(np.median(S['m2'][U])), 'correlacao_m1_m2': float(np.corrcoef(S['m1'][U], S['m2'][U])[0, 1]),
        'dp_m2_dentro_do_local': float(wm(S['m2'][U])[inf].std()), 'dp_m2_menos_m1_dentro_do_local': float(wm(S['m2'][U] - S['m1'][U])[inf].std()),
        'soma_1_menos_m2_vezes_V': float(((1 - S['m2'][U]) * V[U]).sum()),
        'biom_sem_habilitacao_2t_sobre_comparecimento': float(B['bsh2'][U].sum() / B['comp2'][U].sum()),
        'modelos_de_urna_2t': {q: int((S['modelo2'][U] == q).sum()) for q in sorted(set(S['modelo2'][U]))},
        'mesma_urna_nos_dois_turnos': int((B['serie1'][U] == B['serie2'][U]).sum()),
        'colunas_X': S['Xnomes'], 'demais_candidatos_no_X': demais}
    gravar('parcial_resultado.json', res)
    log('universo', res['universo']['U_com_perfil'])

    # ---------------- 1. dose principal
    R = reg_dose(S, B, U)
    assert np.linalg.cond(R.XtX / np.sqrt(np.outer(np.diag(R.XtX), np.diag(R.XtX)))) < 1e10
    r = R.fit(y[U]); P = resumo_dose(r)
    P['Phi_formula_geral'] = 2 * (-P['b']['coef']) * res['universo']['soma_1_menos_m2_vezes_V'] / 100 / MARGEM
    P['coeficientes_todos'] = {q: [r['coef'][q], r['ep'][q]] for q in r['coef']}
    res['principal'] = P
    # conferência da função própria contra lib.fe_ols (erro por local)
    Xm, nomes = mat(cols_base(S, {'m2': S['m2']}, collections.OrderedDict([('m1', S['m1']), ('nb', S['nb'])])))
    Rl = Reg(Xm[U], B['local'][U], B['local'][U], V[U], nomes); rl = Rl.fit(y[U])
    lb = fe_ols(y[U], Xm[U][:, [nomes.index(q) for q in Rl.nomes]], B['local'][U], w=V[U], nomes=Rl.nomes)
    conf['Reg_contra_lib_fe_ols'] = {'b_Reg': rl['coef']['m2'], 'b_lib': lb['coef']['m2'], 'ep_Reg_por_local': rl['ep']['m2'], 'ep_lib': lb['ep']['m2'],
                                     'maior_diferenca_coef': float(max(abs(rl['coef'][q] - lb['coef'][q]) for q in Rl.nomes)),
                                     'maior_diferenca_ep': float(max(abs(rl['ep'][q] - lb['ep'][q]) for q in Rl.nomes))}
    conf['conferencia_por_pandas'] = conferencia_pandas(Xm[U], nomes, y[U], V[U], B['local'][U], B['mun'][U])
    del Xm
    rbn = R.fit(yBN[U]); PBN = resumo_dose(rbn)
    escala_bn = float(((1 - S['m2'][U]) * B['comp2'][U]).sum()) / 100 / MARGEM

    def com_bn(o):
        o['Phi_BN'] = o['b']['coef'] * escala_bn; o['Phi_BN_ic99'] = [o['b']['ic99'][0] * escala_bn, o['b']['ic99'][1] * escala_bn]
        o['votos_convertidos'] = o['Phi_BN'] * MARGEM; o['votos_convertidos_ic99'] = [x * MARGEM for x in o['Phi_BN_ic99']]
        for q in ('Phi_letra', 'Phi_letra_ic99', 'votos_trocados', 'votos_trocados_ic99', 'votos_de_margem', 'votos_de_margem_ic99'): o.pop(q, None)
        return o
    res['yBN'] = {'principal': com_bn(PBN), 'escala_Phi_BN_por_pp': escala_bn}
    gravar('parcial_resultado.json', res)
    log('principal b', P['b'], 'k', P['k'])

    # ---------------- 2. regiões
    reg = {}
    for nm in REGIOES:
        mr = U & (S['regiao'] == nm)
        Rr = reg_dose(S, B, mr)
        a = resumo_dose(Rr.fit(y[mr])); bb = com_bn(resumo_dose(Rr.fit(yBN[mr])))
        reg[nm] = {'y': {q: a[q] for q in ('n', 'locais', 'agrupamentos', 'b', 'k', 'Phi_letra')}, 'yBN': {q: bb[q] for q in ('b', 'k')}}
        del Rr
    sg = np.sign(P['b']['coef'])
    res['regioes'] = {'por_regiao': reg, 'mesmo_sentido_que_o_nacional': int(sum(np.sign(reg[q]['y']['b']['coef']) == sg for q in reg)),
                      'negativas': int(sum(reg[q]['y']['b']['coef'] < 0 for q in reg))}
    gravar('parcial_resultado.json', res)
    log('regiões', {q: round(reg[q]['y']['b']['coef'], 3) for q in reg})

    # ---------------- 3. sensibilidades (não decidem)
    sens = {}

    def um(nome, Rs, ms):
        a = resumo_dose(Rs.fit(y[ms])); bb = resumo_dose(Rs.fit(yBN[ms]))
        sens[nome] = {'n': a['n'], 'b': a['b'], 'k': a.get('k'), 'Phi_letra': a['Phi_letra'], 'yBN_b': bb['b'], 'yBN_k': bb.get('k')}
    um('sem_peso', reg_dose(S, B, U, w=np.ones(len(V))), U)
    um('erro_por_local', reg_dose(S, B, U, cl=B['local']), U)
    um('sem_bloco_de_perfil', reg_dose(S, B, U, sem=PERFIL_X), U)
    um('sem_variacao_da_abstencao', reg_dose(S, B, U, sem=('dabst',)), U)
    mu = U & (B['serie1'] == B['serie2']); um('mesma_urna_nos_dois_turnos', reg_dose(S, B, mu), mu)
    mj = U & ~B['junta1']; um('sem_junta_no_1t', reg_dose(S, B, mj), mj)
    um('so_m2_sem_m1', reg_dose(S, B, U, so_m2=True), U)
    res['sensibilidades'] = sens
    gravar('parcial_resultado.json', res)
    log('sensibilidades', {q: round(sens[q]['b']['coef'], 3) for q in sens})

    # ---------------- 4. experimento natural
    m2 = S['m2']; m1 = S['m1']
    inds = {'A': m2 >= 0.5, 'B': (m2 >= 0.2) & (m1 < 0.1), 'C': (m1 >= 0.2) & (m2 < 0.1)}
    nomes_ind = {'A': 'm2 de 0,5 ou mais', 'B': 'm2 de 0,2 ou mais e m1 abaixo de 0,1 (leitor caiu no 2º turno)',
                 'C': 'espelho: m1 de 0,2 ou mais e m2 abaixo de 0,1 (placebo)'}
    nat = {}; RN = {}
    for q, ind in inds.items():
        ds = descr_ind(S, B, U, ind)
        RN[q] = reg_ind(S, B, U, ind)
        o = resumo_ind(RN[q].fit(y[U]), ds); o['definicao'] = nomes_ind[q]
        o['em_todas_as_pareadas_fora_exterior'] = int(ind.sum())
        o['secoes'] = [str(k) for k in B['chave'][U & ind]]
        rb = RN[q].fit(yBN[U]); o['yBN_d'] = linha(rb, 'ind')
        Rm = reg_ind(S, B, U, ind, com_m1=True); o['d_com_m1_de_controle'] = linha(Rm.fit(y[U]), 'ind'); del Rm
        nat[q] = o
    res['experimento_natural'] = nat
    gravar('parcial_resultado.json', res)
    log('natural', {q: (round(nat[q]['d']['coef'], 3), round(nat[q]['d']['ep'], 3)) for q in nat})

    # ---------------- 5. amostra de logs
    lg = B['log']; okl = lg[:, 0] >= 0; UL = U & okl
    fr = lambda j, t: lg[:, j] / np.maximum(lg[:, t], 1)
    fB1, fM1, fS1 = fr(0, 3), fr(1, 3), fr(2, 3); fB2, fM2, fS2 = fr(4, 7), fr(5, 7), fr(6, 7)

    def reg_log(dose_ctrl, cl):
        c = collections.OrderedDict(dose_ctrl)
        for q in S['Xnomes']: c[q] = S['X'][q]
        for q, vv in S['MD'].items(): c[q] = vv
        Xm_, nomes_ = mat(c)
        return Reg(Xm_[UL], B['local'][UL], cl[UL], V[UL], nomes_)
    dc_a = [('fM2', fM2), ('fS2', fS2), ('fM1', fM1), ('fS1', fS1)]; dc_b = [('u2', fM2 + fS2), ('u1', fM1 + fS1)]
    Ra = reg_log(dc_a, B['mun']); Rb = reg_log(dc_b, B['mun'])
    ra = Ra.fit(y[UL]); rb = Rb.fit(y[UL]); ral = reg_log(dc_a, B['local']).fit(y[UL]); rbl = reg_log(dc_b, B['local']).fit(y[UL])
    ra_bn = Ra.fit(yBN[UL]); rb_bn = Rb.fit(yBN[UL])
    _, gL = np.unique(B['local'][UL], return_inverse=True); cL = np.bincount(gL); iL = cL[gL] >= 2
    wmL = lambda x: x - (np.bincount(gL, weights=x) / cL)[gL]
    L = {'secoes_na_amostra_com_dois_turnos_em_U': int(UL.sum()), 'n': ra['n'], 'locais': ra['locais'], 'municipios': ra['agrupamentos'],
         'fracoes_2t_na_amostra': {'B': float(lg[UL, 4].sum() / lg[UL, 7].sum()), 'M': float(lg[UL, 5].sum() / lg[UL, 7].sum()), 'S': float(lg[UL, 6].sum() / lg[UL, 7].sum())},
         'fracoes_1t_na_amostra': {'B': float(lg[UL, 0].sum() / lg[UL, 3].sum()), 'M': float(lg[UL, 1].sum() / lg[UL, 3].sum()), 'S': float(lg[UL, 2].sum() / lg[UL, 3].sum())},
         'dp_dentro_do_local': {'fM2': float(wmL(fM2[UL])[iL].std()), 'fS2': float(wmL(fS2[UL])[iL].std()), 'u2': float(wmL((fM2 + fS2)[UL])[iL].std()),
                                'u2_menos_u1': float(wmL((fM2 + fS2 - fM1 - fS1)[UL])[iL].std())},
         'correlacao_fS2_nb': float(np.corrcoef(fS2[UL], S['nb'][UL])[0, 1]), 'correlacao_fS2_fS1': float(np.corrcoef(fS2[UL], fS1[UL])[0, 1]),
         'correlacao_fM2_fM1': float(np.corrcoef(fM2[UL], fM1[UL])[0, 1]),
         'conta_a_letra': {q: linha(ra, q) for q in ('fM2', 'fS2', 'fM1', 'fS1')},
         'conta_a_letra_erro_por_local': {q: linha(ral, q) for q in ('fM2', 'fS2', 'fM1', 'fS1')},
         'conta_b_restrita': {'b': linha(rb, 'u2'), 'k': linha(rb, 'u1'), 'Phi_letra': -rb['coef']['u2'] / ESCALA,
                              'Phi_letra_ic99': sorted([-(rb['coef']['u2'] - Z99 * rb['ep']['u2']) / ESCALA, -(rb['coef']['u2'] + Z99 * rb['ep']['u2']) / ESCALA])},
         'conta_b_restrita_erro_por_local': {'b': linha(rbl, 'u2'), 'k': linha(rbl, 'u1')},
         'yBN_conta_a': {q: linha(ra_bn, q) for q in ('fM2', 'fS2', 'fM1', 'fS1')},
         'yBN_conta_b': {'b': linha(rb_bn, 'u2'), 'k': linha(rb_bn, 'u1')}, 'retiradas': ra['retiradas']}
    res['logs'] = L
    gravar('parcial_resultado.json', res)
    log('logs', L['conta_b_restrita']['b'], L['conta_a_letra']['fM2'], L['conta_a_letra']['fS2'])

    # ---------------- 6. y_alt e placebos com 2022
    c22, y22, V22, a1_22, a2_22 = cols22(B, S)
    f = lambda a, b: a / np.maximum(b, 1)
    M22 = U & B['tem22'] & (V22 >= 30) & (B['comp1_22'] > 0) & (B['apt1_22'] > 0) & (B['apt2_22'] > 0)
    perf = collections.OrderedDict((q, S['X'][q]) for q in PERFIL_X)
    a2_26 = 1 - f(B['comp2'], B['apt2']); a1_26 = 1 - f(B['comp1'], B['apt1'])

    def monta(dose, ctrl, extras, md):
        c = collections.OrderedDict(dose); c.update(ctrl); c.update(extras); c.update(perf)
        for q, vv in md.items(): c[q] = vv
        return mat(c)
    # y_alt
    ex = collections.OrderedDict(c22); ex['y22'] = y22; ex['abst1_22'] = a1_22; ex['dabst_22'] = a2_22 - a1_22; ex['dabst_26_22'] = a2_26 - a2_22
    ex['lnapt'] = S['X']['lnapt']; ex['pos'] = S['X']['pos']
    Xa, na = monta([('m2', S['m2'])], [('m1', S['m1']), ('nb', S['nb'])], ex, S['MD'])
    yalt = y - y22
    Ralt = Reg(Xa[M22], B['local'][M22], B['mun'][M22], V[M22], na); ralt = Ralt.fit(yalt[M22])
    A = resumo_dose(ralt); A['coef_y22'] = linha(ralt, 'y22')
    A['bruto_2026'] = {'y_2026_agregado': float(100 * B['L2'][M22].sum() / V[M22].sum()), 'y_2022_agregado': float(100 * B['L2_22'][M22].sum() / V22[M22].sum())}
    Mm = M22 & B['mesmo_local_22']
    ralt2 = Reg(Xa[Mm], B['local'][Mm], B['mun'][Mm], V[Mm], na).fit(yalt[Mm])
    res['y_alt'] = {'principal': A, 'so_mesmo_codigo_de_local': {'n': ralt2['n'], 'b': linha(ralt2, 'm2'), 'k': linha(ralt2, 'm1')},
                    'pareamento': {'secoes': int(M22.sum()), 'mesmo_codigo_de_local': int(Mm.sum()),
                                   'aptos_2022_dentro_de_10_por_cento_dos_de_2026': int((np.abs(B['apt2_22'][M22] / np.maximum(B['apt2'][M22], 1) - 1) <= 0.10).sum())}}
    del Xa, Ralt
    # placebo de período anterior
    ex = collections.OrderedDict(c22); ex['abst1_22'] = a1_22; ex['dabst_22'] = a2_22 - a1_22
    ex['lnapt22'] = np.log(np.maximum(B['apt2_22'], 1)); ex['pos'] = S['X']['pos']
    Xp, npn = monta([('m2', S['m2'])], [('m1', S['m1']), ('nb', S['nb'])], ex, S['MD'])
    rp = Reg(Xp[M22], B['local'][M22], B['mun'][M22], V22[M22], npn).fit(y22[M22])
    P1 = resumo_dose(rp)
    rp2 = Reg(Xp[Mm], B['local'][Mm], B['mun'][Mm], V22[Mm], npn).fit(y22[Mm])
    P1['so_mesmo_codigo_de_local'] = {'n': rp2['n'], 'b': linha(rp2, 'm2'), 'k': linha(rp2, 'm1')}
    del Xp
    # placebo de turno trocado
    V1 = (B['L1'] + B['R1']).astype(float); y1 = 100 * f(B['L1'], V1)
    Mt = M22 & (V1 >= 30)
    ex = collections.OrderedDict(c22); ex['y22'] = y22; ex['abst1_22'] = a1_22; ex['dabst1_26_22'] = a1_26 - a1_22
    ex['lnapt1'] = np.log(np.maximum(B['apt1'], 1)); ex['pos'] = S['X']['pos']
    Xt, nt = monta([('m1', S['m1'])], [('m2', S['m2']), ('nb', S['nb'])], ex, S['MD1'])
    rt = Reg(Xt[Mt], B['local'][Mt], B['mun'][Mt], V1[Mt], nt).fit(y1[Mt])
    P2 = resumo_dose(rt, nome_b='m1', nome_k='m2')
    P2['bruto_2026'] = {'y_1t_2026_agregado': float(100 * B['L1'][Mt].sum() / V1[Mt].sum()), 'y_2t_2022_agregado': float(100 * B['L2_22'][Mt].sum() / V22[Mt].sum())}
    del Xt
    P3 = placebo_governador(S, B, G, U)
    res['placebos'] = {'periodo_anterior': P1, 'turno_trocado': P2, 'cargo_governador': P3}
    gravar('parcial_resultado.json', res)
    log('y_alt', A['b'], 'placebos', P1['b'], P2['b'], P3['b'])

    # ---------------- 7. valor bruto e exterior
    res['bruto_2026_por_faixa_de_m2'] = tabela_bruta(S, B, U)
    res['exterior_a_parte'] = exterior(Z, demais)
    gravar('parcial_resultado.json', res)

    # ---------------- 8. calibrações
    PAR = {}
    if os.path.exists(TRAB + '/parcial_calibracao_principal.json'):
        with open(TRAB + '/parcial_calibracao_principal.json') as fh: PAR = json.load(fh)
        if PAR.get('_docstring') != sha_docstring() or PAR.get('_b_obs') != P['b']['coef']: PAR = {}
    PAR['_docstring'] = sha_docstring(); PAR['_b_obs'] = P['b']['coef']
    obs = {'b': P['b']['coef'], 'k': P['k']['coef'], 'dA': nat['A']['d']['coef'], 'dB': nat['B']['d']['coef'], 'dC': nat['C']['d']['coef']}
    cal = calibrar_principal(S, B, U, R, RN['A'], RN['B'], RN['C'], obs, None, PAR)
    res['calibracao_principal'] = cal
    ep = P['b']['ep']; rec = cal['R_para_L_Phi_1.0']['b']['recuperacao']
    res['calibracao_principal_resumo'] = {
        'menor_Phi_com_poder_de_95_por_cento_a_z_3_3': (Z_LIM + 1.6449) * ep / (ESCALA * rec),
        'ep_de_b': ep, 'meia_largura_ic99_em_Phi': Z99 * ep / ESCALA,
        't_esperado_para_Phi': {str(p): ESCALA * rec * p / ep for p in PHIS}}
    gravar('parcial_resultado.json', res)
    res['calibracao_yBN'] = calibrar_bn(S, B, U, R, PBN['b']['coef'], np.random.default_rng([SEMENTE, 30]), escala_bn)
    gravar('parcial_resultado.json', res)
    res['calibracao_logs'] = calibrar_logs(S, B, UL, Ra, Rb, fB2, {'u2': rb['coef']['u2'], 'fM2': ra['coef']['fM2'], 'fS2': ra['coef']['fS2']},
                                           np.random.default_rng([SEMENTE, 40]))
    gravar('parcial_resultado.json', res)

    # ---------------- 9. vereditos e contagem de testes
    res['vereditos'] = vereditos(res)
    nz = 1 + 5 + 3 + 2 + 1 + 1 + 3  # dose, regiões, natural A B C, logs (u2 e a conta da letra), y_BN, y_alt, placebos de regressão
    res['contagem_de_testes'] = {'estatisticas_com_limiar_de_z_3_3': nz, 'p_bicaudal_de_z_3_3': 0.000967,
                                 'sinais_esperados_pelo_acaso': nz * 0.000967,
                                 'nota': 'dose principal, 5 regiões, 3 grupos do experimento natural, 2 contas da amostra de logs, y_BN, y_alt e 3 placebos de regressão; as sensibilidades não decidem'}
    gravar('parcial_resultado.json', res)
    log('vereditos', res['vereditos'])

    # ---------------- 10. EXPLORATÓRIO (depois de ver o resultado)
    rec = cal['R_para_L_Phi_1.0']['b']['recuperacao']; bb = P['b']
    res['exploratorio'] = {
        'aviso': 'tudo neste bloco foi feito depois de ver o resultado e não muda veredito',
        'leituras_derivadas': {
            'escala_calibrada_pp_por_Phi': ESCALA * rec,
            'Phi_calibrado': -bb['coef'] / (ESCALA * rec),
            'Phi_calibrado_ic99': sorted([-bb['ic99'][0] / (ESCALA * rec), -bb['ic99'][1] / (ESCALA * rec)]),
            'limite_de_99_5_por_cento_no_sentido_da_tese_Phi_letra': -bb['ic99'][0] / ESCALA,
            'limite_no_sentido_da_tese_votos_de_margem': -bb['ic99'][0] / ESCALA * MARGEM,
            'limite_no_sentido_da_tese_Phi_calibrado': -bb['ic99'][0] / (ESCALA * rec),
            'limite_no_sentido_da_tese_votos_de_margem_calibrado': -bb['ic99'][0] / (ESCALA * rec) * MARGEM,
            'quanto_o_ic99_passa_do_limite_no_lado_contrario': bb['ic99'][1] - LIM_B,
            'z_contra_b_de_menos_0_51': (bb['coef'] + LIM_B) / bb['ep'], 'z_contra_b_de_menos_2_04': (bb['coef'] + ESCALA) / bb['ep'],
            'experimento_natural_A_z_contra_Phi_1_plantado': (nat['A']['d']['coef'] - cal['R_para_L_Phi_1.0']['nat_A']['delta_medio']) / nat['A']['d']['ep'],
            'experimento_natural_A_Phi_calibrado': nat['A']['d']['coef'] / cal['R_para_L_Phi_1.0']['nat_A']['delta_medio'],
            'experimento_natural_A_Phi_calibrado_ic99': sorted([x / cal['R_para_L_Phi_1.0']['nat_A']['delta_medio'] for x in nat['A']['d']['ic99']]),
            'nb_se_fosse_exposicao_Phi': -P['r_nb']['coef'] / (ESCALA * rec),
            'nb_se_fosse_exposicao_votos_de_margem': -P['r_nb']['coef'] / (ESCALA * rec) * MARGEM},
        'bruto_2026_por_faixa_de_nb': exploratorio_bruto_por_nb(S, B, U),
        'escada_do_ganho_bruto': exploratorio_escada(S, B, U, y),
        'logs': exploratorio_logs(S, B, U, y),
        'nb_por_idade': exploratorio_nb_por_idade(S, B, U, y, y22, V22, M22, c22, a1_22, a2_22)}
    with open(TRAB + '/resultado_completo.json', 'w') as fh:
        json.dump(res, fh, ensure_ascii=False, indent=1, default=_jd)
    log('fim das contas')
    escrever(res)
    return res


# ---------------------------------------------------------------- saída
def n_(x, d=3, s=False):
    if x is None: return 'n/d'
    t = f'{x:+.{d}f}' if s else f'{x:.{d}f}'
    return t.replace('.', ',')


def i_(x):
    return f'{int(round(x)):,}'.replace(',', '.')


def L_(l, d=3):
    return f"{n_(l['coef'], d, True)} (erro {n_(l['ep'], d)}; z {n_(l['z'], 2, True)}; IC99 {n_(l['ic99'][0], d, True)} a {n_(l['ic99'][1], d, True)})"


def escrever(res):
    P = res['principal']; U = res['universo']; V = res['vereditos']; nat = res['experimento_natural']; lg = res['logs']
    cal = res['calibracao_principal']; calr = res['calibracao_principal_resumo']; plc = res['placebos']; ex = res['exploratorio']
    ld = ex['leituras_derivadas']; bn = res['yBN']['principal']; alt = res['y_alt']; conf = res['conferencias']
    b = P['b']; k = P['k']; A = nat['A']; Bn = nat['B']; C = nat['C']
    c1 = cal['R_para_L_Phi_1.0']; c5 = cal['R_para_L_Phi_0.5']; c25 = cal['R_para_L_Phi_0.25']
    esc = ex['escada_do_ganho_bruto']; nbi = ex['nb_por_idade']; el = ex['logs']
    frase = (f"Nenhum SINAL: a habilitação do dia não mostra a marca da tese (b = {n_(b['coef'], 3, True)} p.p. por unidade de m2, erro {n_(b['ep'])}, "
             f"z = {n_(b['z'], 2, True)}, sentido contrário ao previsto) e, no sentido da tese, o intervalo de 99% só admite até {n_(100 * ld['limite_de_99_5_por_cento_no_sentido_da_tese_Phi_letra'], 1)}% "
             f"da margem ({i_(ld['limite_no_sentido_da_tese_votos_de_margem'])} votos de margem; {i_(ld['limite_no_sentido_da_tese_votos_de_margem_calibrado'])} com a escala calibrada); "
             f"pela letra, porém, o teste fica INCONCLUSIVO, porque o limite de cima do intervalo ({n_(b['ic99'][1], 4, True)}) passa em {n_(ld['quanto_o_ic99_passa_do_limite_no_lado_contrario'], 4)} "
             f"o limite de 0,51 do critério SEM SINAL, do lado contrário ao da tese.")
    partes = collections.OrderedDict()
    partes['teste pela letra (combinado)'] = V['teste_pela_letra']
    partes['dose do dia (y)'] = V['dose_y']
    partes['experimento natural, grupo A (m2 de 0,5 ou mais)'] = V['experimento_natural_A'] + (' (enxerga a margem inteira plantada; meia margem, não)' if V['experimento_natural_A'] == 'SEM SINAL' else '')
    partes['experimento natural, grupo B (leitor caiu no 2º turno)'] = V['experimento_natural_B']
    partes['espelho do experimento natural, grupo C (placebo)'] = V['placebos']['espelho_experimento_natural_C']
    partes['amostra de logs'] = V['logs']
    partes['brancos e nulos (y_BN)'] = V['yBN']
    partes['desfecho contra 2022 (y_alt)'] = V['y_alt']
    partes['placebo de período anterior'] = V['placebos']['periodo_anterior']
    partes['placebo de turno trocado'] = V['placebos']['turno_trocado']
    partes['placebo de cargo (governador)'] = V['placebos']['cargo_governador'] + f" pela regra, mas sem precisão (erro de {n_(plc['cargo_governador']['b']['ep'], 2)} p.p.)"

    a_favor = [
        f"Pela letra o teste não fecha como SEM SINAL: o intervalo de 99% de b vai de {n_(b['ic99'][0], 4, True)} a {n_(b['ic99'][1], 4, True)} e o critério pedia que coubesse entre -0,51 e +0,51. O excesso é de {n_(ld['quanto_o_ic99_passa_do_limite_no_lado_contrario'], 4)} e fica do lado contrário ao da tese (a favor de Flávio), mas o registro não distingue os lados.",
        f"O coeficiente de nb (fração de eleitores sem biometria no cadastro) é {L_(P['r_nb'])}: seções com mais eleitores sem biometria deram menos ganho a Lula do que o 1º turno previa, que é o sentido da marca. Lido como exposição ao programa valeria Phi de {n_(ld['nb_se_fosse_exposicao_Phi'], 2)} ({i_(ld['nb_se_fosse_exposicao_votos_de_margem'])} votos de margem). O registro, antes de ver o dado, tratou nb como traço do eleitor que não decide; o mesmo coeficiente aparece na virada de 2022 ({L_(plc['periodo_anterior']['r_nb'])}) e no 1º turno de 2026 contra 2022 ({L_(plc['turno_trocado']['r_nb'])}), e como o Léo suspeita também de 2022 esse placebo não limpa a dúvida.",
        f"No bruto de 2026 o ganho de Lula entre os turnos cai conforme sobe a liberação manual: {n_(res['bruto_2026_por_faixa_de_m2'][0]['ganho_2t_menos_1t'], 2, True)} p.p. nas seções com m2 abaixo de 3% e {n_(res['bruto_2026_por_faixa_de_m2'][4]['ganho_2t_menos_1t'], 2, True)} p.p. nas de 20% a 50%. Dentro do mesmo local e sem controles a inclinação é {L_(esc['efeito_fixo_de_local']['so_m2'])} (exploratório). Com só parte dos controles do registro (votos do 1º turno, abstenção e nb) b sai {L_(esc['dentro_do_local_acrescentando_blocos']['ate_nb']['m2'])} (exploratório); acrescentando aptos, posição e modelo da urna vai a {n_(res['sensibilidades']['sem_bloco_de_perfil']['b']['coef'], 3, True)} (sensibilidade fixada antes) e, com o perfil, a {n_(b['coef'], 3, True)}: o resultado depende de quais controles entram.",
        f"O coeficiente de m1 é negativo ({L_(k)}) e o experimento natural do grupo A também ({L_(A['d'])}); os dois no sentido da tese, nenhum com significância.",
        f"Poder limitado: o menor efeito que o teste enxerga com 95% de chance a z de 3,3 é Phi de {n_(calr['menor_Phi_com_poder_de_95_por_cento_a_z_3_3'], 3)} ({i_(calr['menor_Phi_com_poder_de_95_por_cento_a_z_3_3'] * MARGEM)} votos de margem). Um quarto da margem plantado só passou de z 3,3 em {n_(100 * c25['b']['poder_z33'], 0)}% das cópias. A amostra de logs e o grupo B do experimento natural não enxergam nem a margem inteira, e o placebo de governador tem erro de {n_(plc['cargo_governador']['b']['ep'], 2)} p.p.",
        "Este desenho só testa a versão parcial da hipótese (o programa trata diferente quem não passou na biometria). Uma troca igual para todo eleitor, com ou sem biometria, não deixa marca aqui: o teste nada diz sobre ela.",
    ]
    contra = [
        f"A dose do dia tem o sinal contrário ao da tese: b = {L_(b)}. A marca pedia b de -0,51 ou abaixo para um quarto da margem e -2,04 para a margem inteira; o observado está a {n_(ld['z_contra_b_de_menos_0_51'], 1)} erros-padrão de -0,51 e a {n_(ld['z_contra_b_de_menos_2_04'], 1)} de -2,04. No sentido da tese o intervalo de 99% admite no máximo Phi de {n_(ld['limite_de_99_5_por_cento_no_sentido_da_tese_Phi_letra'], 3)} pela letra ({i_(ld['limite_no_sentido_da_tese_votos_de_margem'])} votos de margem) ou {n_(ld['limite_no_sentido_da_tese_Phi_calibrado'], 3)} com a escala calibrada ({i_(ld['limite_no_sentido_da_tese_votos_de_margem_calibrado'])}), contra 4.430.191 de margem.",
        f"Experimento natural, grupo A: nas {A['tratadas_em_local_com_vizinha']} seções com metade ou mais dos eleitores liberados sem biometria (média de {n_(100 * A['bruto_m2']['tratadas'], 1)}% contra {n_(100 * A['bruto_m2']['vizinhas'], 1)}% nas {A['vizinhas']} vizinhas de prédio) o ganho bruto de Lula entre os turnos foi {n_(A['bruto_ganho_2t_menos_1t']['tratadas'], 3, True)} p.p. contra {n_(A['bruto_ganho_2t_menos_1t']['vizinhas'], 3, True)} nas vizinhas (diferença {n_(A['bruto_ganho_2t_menos_1t']['diferenca'], 3, True)}); com o modelo, d = {L_(A['d'])}. A margem inteira plantada desloca esse d em {n_(c1['nat_A']['delta_medio'], 2, True)}: o observado está a {n_(ld['experimento_natural_A_z_contra_Phi_1_plantado'], 1)} erros-padrão disso.",
        f"Dose e resposta (exploratório): dentro do local, a inclinação negativa do ganho bruto só existe abaixo de m2 = 0,2 ({L_(esc['ganho_bruto_dentro_do_local_por_trecho_de_m2']['m2_ate_0_2'])}) e some acima ({L_(esc['ganho_bruto_dentro_do_local_por_trecho_de_m2']['m2_acima_de_0_2'])}; {i_(esc['secoes_com_m2_acima_de_0_2'])} seções), justamente onde a exposição mais varia. Basta pôr a fração de Lula do 1º turno como controle para a inclinação dentro do local cair a {L_(esc['dentro_do_local_acrescentando_blocos']['so_a_fracao_de_Lula_no_1t_como_controle']['m2'])}.",
        f"nb por idade (exploratório): o coeficiente de nb não é igual para todo eleitor sem biometria, como seria numa regra de programa. Para os de 20 a 24 anos ({n_(100 * nbi['parcela_dos_sem_biometria_com_20_a_24_anos'], 1)}% dos sem biometria) é {L_(nbi['modelo_2026_nb_aberto_por_idade']['nb_20a24'])}; para os de 45 a 59 é {L_(nbi['modelo_2026_nb_aberto_por_idade']['nb_45a59'])}. O mesmo desenho por idade aparece na virada de 2022 ({n_(nbi['virada_de_2022_nb_aberto_por_idade']['nb_20a24']['coef'], 2, True)} e {n_(nbi['virada_de_2022_nb_aberto_por_idade']['nb_45a59']['coef'], 2, True)}). No bruto, o ganho de Lula é maior, não menor, no quinto de seções com mais eleitores sem biometria ({n_(ex['bruto_2026_por_faixa_de_nb'][4]['ganho_2t_menos_1t'], 2, True)} contra {n_(ex['bruto_2026_por_faixa_de_nb'][0]['ganho_2t_menos_1t'], 2, True)} p.p.).",
        f"A calibração mostra que o modelo não esconde um efeito de exposição: plantado nos dados de 2026, ele recupera {n_(100 * c1['b']['recuperacao'], 0)}% do tamanho (de R para L) e {n_(100 * cal['L_para_R_Phi_1.0']['b']['recuperacao'], 0)}% no espelho (de L para R), com o coeficiente de m1 parado (delta de {n_(c1['k']['delta_medio'], 3, True)}). Meia margem plantada é vista em {n_(100 * c5['b']['poder_z33'], 0)}% das cópias; a margem inteira, em {n_(100 * c1['b']['poder_z33'], 0)}%.",
        f"Amostra de logs: a fração exata de eleitores sem biometria no dia (S) tem coeficiente positivo ({L_(lg['conta_a_letra']['fS2'], 2)}), o contrário da marca, com o controle do 1º turno do mesmo tamanho e sinal oposto ({n_(lg['conta_a_letra']['fS1']['coef'], 2, True)}): o que conta é quem compareceu a mais no 2º turno, não o nível. A parte não tem poder e não decide.",
        f"Brancos e nulos: b = {L_(bn['b'])}, Phi_BN = {n_(bn['Phi_BN'], 3, True)} (IC99 {n_(bn['Phi_BN_ic99'][0], 3, True)} a {n_(bn['Phi_BN_ic99'][1], 3, True)}), isto é, {i_(bn['votos_convertidos'])} votos convertidos (IC99 {i_(bn['votos_convertidos_ic99'][0])} a {i_(bn['votos_convertidos_ic99'][1])}); um quarto da margem plantado em brancos e nulos é visto em 100% das cópias.",
        f"Placebos e espelhos limpos: período anterior {L_(plc['periodo_anterior']['b'])}; turno trocado {L_(plc['turno_trocado']['b'])}; governador {L_(plc['cargo_governador']['b'], 2)}; grupo C {L_(C['d'])}. Nenhuma região tem b com |z| de 2 ou mais; 4 das 5 têm b positivo.",
    ]
    pistas = [
        "Pedir ao TSE o comparecimento por eleitor com e sem biometria (o cadastro de comparecimento e abstenção por seção, com faixa etária) dos dois turnos: é o dado que separa de vez composição do comparecimento de exposição ao programa no coeficiente de nb, que hoje é o número mais forte deste teste no sentido da tese.",
        "Pedir ao TSE e aos TREs a lista e as atas do Teste de Integridade com biometria do 2º turno (eleitores reais emprestam a digital para habilitar a urna auditada): se houve urnas auditadas com habilitação biométrica real e sem divergência, a premissa da hipótese (o programa reconhece o teste pela falta do dedo) cai por medida direta, de fora do programa.",
        f"As {A['tratadas_em_U']} seções do grupo A (lista no JSON, campo experimento_natural.A.secoes) são o melhor lugar para uma perícia olhar: ali a urna quase não viu digital. Hoje elas não mostram nada, mas são poucas ({i_(A['votos_V_das_tratadas'])} votos); pedir os logs dessas seções confirmaria que a liberação foi mesmo manual e por quê.",
        f"A dose S (eleitor sem biometria no dia) só existe no log. Para a amostra de logs enxergar a margem inteira seriam precisas cerca de {i_(lg['n'] * ((res['calibracao_logs']['Phi_1.0']['u2']['ep_medio'] * (Z_LIM + 1.6449) / abs(res['calibracao_logs']['Phi_1.0']['u2']['delta_medio'])) ** 2))} seções com log (hoje {i_(lg['n'])}). Se a amostra aleatória nova da Onda D trouxer logs, vale repetir a parte (ii).",
        "O resultado da dose depende dos controles (de -0,43 a +0,20 conforme o bloco, exploratório). O conferente independente deve refazer com código próprio o modelo completo do registro e a escada de blocos.",
    ]
    desvios = [
        "D1 a D21 do docstring (decisões que o registro não fixa, escritas antes de qualquer conta com votos; sha256 do docstring no JSON): definição de 0,5% no país, faixas de idade e escolaridade, perfil somado nas seções agregadas, modelo da urna pela série, erro por município em função própria conferida contra lib.fe_ols, regras de SEM PODER e de veredito por parte, calibrações dos logs e de y_BN.",
        f"As 27 seções com junta apuradora do 2º turno estão todas no exterior; tirar o exterior já as tira. Ficaram em U {U['junta_1t']} seções com junta só no 1º turno (a sensibilidade sem elas não muda nada). {U['sem_perfil_em_U']} seções de U não têm perfil no F15 e saem; U com perfil tem {i_(U['U_com_perfil'])} seções, das quais {i_(P['n'])} em {i_(P['locais'])} locais com 2 ou mais seções informam o efeito fixo.",
        "Colunas colineares dentro dos locais: além de coluna sem variação (D5), a função retira coluna que é combinação linear das anteriores (indicadoras de modelo da urna em regiões e na amostra de logs, onde UE2013 e UE2015 só se misturam entre si). Isso foi acrescentado depois que a primeira rodada devolveu coeficientes absurdos em duas regiões por matriz singular; o resultado nacional não mudou em nenhuma casa.",
        "Erro de programação corrigido depois da segunda rodada: o poder do experimento natural na calibração era contado com o sinal trocado (dava 0% sempre). A regra da D15 não mudou; só a conta.",
        "Phi_BN = 1 não pôde ser plantado (pediria converter mais brancos e nulos do que existem, taxa de 1,15); para a regra de poder de y_BN vale o maior tamanho plantado (0,5), que é mais exigente.",
        f"A calibração recupera {n_(100 * c1['b']['recuperacao'], 0)}% e não 100% do b esperado: a escala real é de {n_(ld['escala_calibrada_pp_por_Phi'], 3)} p.p. por unidade de Phi e não 2,04 (o registro usou 0,876 de fração biométrica, que inclui os eleitores sem biometria, e a troca plantada é proporcional ao voto de Flávio na seção). O veredito usa a letra (2,04); o Phi calibrado sai ao lado.",
        f"Contagens do experimento natural em U: A {A['tratadas_em_U']} ({A['tratadas_em_local_com_vizinha']} com vizinha), B {Bn['tratadas_em_U']} ({Bn['tratadas_em_local_com_vizinha']}), C {C['tratadas_em_U']} ({C['tratadas_em_local_com_vizinha']}); o registro citava 97, 43 e 98.",
        "Placebo de governador com erro agrupado por local (o DF é um município só). O exterior não tem nenhuma habilitação registrada no campo (m2 = 0 em todas as seções): não há o que relatar à parte.",
        "Feito depois de ver o resultado e marcado como EXPLORATÓRIO: leituras derivadas (escala calibrada, limites de um lado só), valor bruto por faixa de nb, escada do ganho bruto e dos blocos de controle, dose e resposta por trecho de m2, nb aberto por idade, conta dos logs em nível e variação e o modelo nacional só na amostra.",
    ]
    res['resumo'] = {'veredito_pela_letra': partes, 'resumo_em_uma_frase': frase, 'a_favor_da_tese': a_favor, 'contra_a_tese': contra,
                     'pistas': pistas, 'desvios': desvios,
                     'fixado_antes': 'universo, desfecho, X, dose, controles, limiares, complementos, placebos e calibração (registro); D1 a D21 do docstring (antes de qualquer conta com votos)',
                     'exploratorio': 'bloco "exploratorio" do JSON e seção 15 do txt'}
    T = []
    P_ = T.append
    P_('R27_A6: TIPO DE HABILITAÇÃO (teste D1.5 do desenho D1; Adendo 27, Onda A, item A6)')
    P_('Gerado por scripts/analisar_R27_A6.py. Critérios: registro/adendo27/desenho_D1_proposta.json (D1.5 e definições comuns), commit 2748895.')
    P_(f"Docstring com as decisões D1 a D21 gravado antes de qualquer conta com votos (10/11/2026 02:18 UTC), sha256 {res['docstring_sha256']}.")
    P_('O desenho D1 é cego (escrito sem ver resultado). Testa só a versão PARCIAL da hipótese: o programa trataria diferente quem não passou na biometria.')
    P_('')
    P_('VEREDITO PELA LETRA')
    for q, v in partes.items(): P_(f'  {q}: {v}')
    P_('')
    P_('RESUMO EM UMA FRASE')
    P_('  ' + frase)
    P_('')
    P_('1. O QUE FOI TESTADO')
    P_('  Hipótese: para escapar do teste de integridade, o programa só alteraria o voto de quem foi habilitado por biometria.')
    P_('  Marca: quanto maior a fração liberada sem biometria na seção no 2º turno (m2), menor o ganho de Lula além do previsto pelo 1º turno;')
    P_('  -2,04 p.p. por unidade de m2 zeraria a margem (Phi = 1); -0,51 vale um quarto da margem (Phi = 0,25).')
    P_('  Modelo: y = 100 x L2/(L2+R2) = efeito fixo de local + X do 1º turno + b x m2 + k x m1 + r x nb + modelo da urna; peso L2+R2; erro por município.')
    P_('  m2 e m1 = QT_ELEI_BIOM_SEM_HABILITACAO / comparecimento (2º e 1º turno); nb = 1 menos eleitores com biometria / eleitores (cadastro).')
    P_('')
    P_('2. UNIVERSO E CONFERÊNCIAS')
    P_(f"  Seções pareadas fora do exterior: {i_(U['pareadas_fora_exterior'])}. Com L2+R2 abaixo de 30: {U['L2_mais_R2_abaixo_de_30']}. U pela letra: {i_(U['U_pela_letra'])}. Sem perfil: {U['sem_perfil_em_U']}. U com perfil: {i_(U['U_com_perfil'])}.")
    P_(f"  Informam o efeito fixo: {i_(P['n'])} seções em {i_(P['locais'])} locais e {i_(P['agrupamentos'])} municípios. Votos em U: Lula {i_(U['L2'])}, Flávio {i_(U['R2'])} (y agregado {n_(U['y_agregado'], 3)}%).")
    P_(f"  m2 médio ponderado {n_(U['m2_medio_pond'], 4)}, m1 {n_(U['m1_medio_pond'], 4)}, nb {n_(U['nb_medio_pond'], 4)}; correlação m1 e m2 {n_(U['correlacao_m1_m2'], 3)}; desvio de m2 dentro do local {n_(U['dp_m2_dentro_do_local'], 4)}; de m2 menos m1 {n_(U['dp_m2_menos_m1_dentro_do_local'], 4)}.")
    P_(f"  Base confere com o oficial: Lula {i_(conf['L2_total_base'])}, Flávio {i_(conf['R2_total_base'])}. Comparecimento e local da estrutura iguais aos da base em {i_(conf['comp2_estrutura_igual_base'])} de {i_(U['pareadas_fora_exterior'])} seções.")
    P_(f"  Função própria contra lib.fe_ols (erro por local): b {n_(conf['Reg_contra_lib_fe_ols']['b_Reg'], 6)} e {n_(conf['Reg_contra_lib_fe_ols']['b_lib'], 6)}; maior diferença de coeficiente {conf['Reg_contra_lib_fe_ols']['maior_diferenca_coef']:.1e}, de erro {conf['Reg_contra_lib_fe_ols']['maior_diferenca_ep']:.1e}.")
    P_(f"  Perfil: total do cadastro dentro de 2% dos aptos em {i_(conf['perfil_total_dentro_de_2_por_cento_dos_aptos_2t'])} seções; {i_(conf['secoes_com_agregadas'])} seções com agregadas somadas. Demais candidatos no X: {', '.join(U['demais_candidatos_no_X'])}.")
    cp = conf['conferencia_por_pandas']
    P_(f"  Conferência por outro caminho de código (pandas e lstsq): b {n_(cp['b'], 6)}; erro por município {n_(cp['ep_com_G_sobre_G_menos_1'], 6)} (o da classe Reg é {n_(b['ep'], 6)}).")
    P_(f"  Log contra bweb: liberados pelo mesário iguais ao campo do bweb em {conf['log_M2_igual_bweb']} de {conf['amostra_logs_dois_turnos_na_base']} seções no 2º turno ({conf['log_M1_igual_bweb']} no 1º).")
    P_('')
    P_('3. DOSE PRINCIPAL (2026, só dados de 2026)')
    P_(f"  b (m2, habilitação do dia)  = {L_(b)}")
    P_(f"  k (m1, mesmo campo no 1º turno) = {L_(k)}")
    P_(f"  r (nb, sem biometria no cadastro) = {L_(P['r_nb'])}")
    P_(f"  Phi pela letra (-b/2,04) = {n_(P['Phi_letra'], 3, True)} (IC99 {n_(P['Phi_letra_ic99'][0], 3, True)} a {n_(P['Phi_letra_ic99'][1], 3, True)}). Pela fórmula geral da frente: {n_(P['Phi_formula_geral'], 3, True)}. Calibrado: {n_(ld['Phi_calibrado'], 3, True)} (IC99 {n_(ld['Phi_calibrado_ic99'][0], 3, True)} a {n_(ld['Phi_calibrado_ic99'][1], 3, True)}).")
    P_(f"  Sinal positivo de Phi = a favor de Lula (sentido da tese); negativo = a favor de Flávio. R2 dentro do local {n_(P['r2_dentro'], 3)}; resíduo {n_(P['dp_residuo_pond'], 2)} p.p.")
    P_(f"  Critério SINAL: b de -0,51 ou abaixo (ou +0,51 ou acima) com |z| de 3,3. Observado: não. Critério SEM SINAL: IC99 entre -0,51 e +0,51. Observado: {n_(b['ic99'][0], 4, True)} a {n_(b['ic99'][1], 4, True)}; passa em {n_(ld['quanto_o_ic99_passa_do_limite_no_lado_contrario'], 4)} no lado positivo.")
    P_(f"  A distância entre INCONCLUSIVO e SEM SINAL aqui é de {n_(ld['quanto_o_ic99_passa_do_limite_no_lado_contrario'], 4)} p.p.: com o erro agrupado por local (sensibilidade fixada antes) o intervalo cabe ({n_(res['sensibilidades']['erro_por_local']['b']['ic99'][0], 3, True)} a {n_(res['sensibilidades']['erro_por_local']['b']['ic99'][1], 3, True)}); com o erro por município, que é o da letra, não cabe.")
    P_('')
    P_('4. REGIÕES')
    for q, v in res['regioes']['por_regiao'].items():
        P_(f"  {q:13s} n {i_(v['y']['n']):>8s}  b = {L_(v['y']['b'])}   k = {n_(v['y']['k']['coef'], 3, True)} ({n_(v['y']['k']['ep'])})")
    P_(f"  Mesmo sentido do nacional em {res['regioes']['mesmo_sentido_que_o_nacional']} de 5; b negativo em {res['regioes']['negativas']} de 5.")
    P_('')
    P_('5. EXPERIMENTO NATURAL (indicadora no lugar da dose; vizinhas = outras seções do mesmo local)')
    for q, o in (('A', A), ('B', Bn), ('C', C)):
        P_(f"  Grupo {q}: {o['definicao']}. Em U: {o['tratadas_em_U']}; com vizinha: {o['tratadas_em_local_com_vizinha']} em {o['locais_informativos']} locais; vizinhas: {o['vizinhas']}; votos das tratadas: {i_(o['votos_V_das_tratadas'])}.")
        P_(f"    m2 médio {n_(o['bruto_m2']['tratadas'], 3)} contra {n_(o['bruto_m2']['vizinhas'], 3)}; m1 {n_(o['bruto_m1']['tratadas'], 3)} contra {n_(o['bruto_m1']['vizinhas'], 3)}.")
        P_(f"    Bruto: y do 2º turno {n_(o['bruto_y_2t']['tratadas'], 2)} contra {n_(o['bruto_y_2t']['vizinhas'], 2)}; 1º turno {n_(o['bruto_y_1t']['tratadas'], 2)} contra {n_(o['bruto_y_1t']['vizinhas'], 2)}; ganho entre turnos {n_(o['bruto_ganho_2t_menos_1t']['tratadas'], 3, True)} contra {n_(o['bruto_ganho_2t_menos_1t']['vizinhas'], 3, True)} (diferença {n_(o['bruto_ganho_2t_menos_1t']['diferenca'], 3, True)}).")
        P_(f"    d = {L_(o['d'])}; com m1 de controle {n_(o['d_com_m1_de_controle']['coef'], 3, True)} ({n_(o['d_com_m1_de_controle']['ep'])}). Esperado para Phi = 1 pela letra: {n_(o['esperado_para_Phi_1'], 3, True)}; plantado de fato: {n_(c1['nat_' + q]['delta_medio'], 3, True)} (t {n_(c1['nat_' + q]['t_medio'], 1, True)}).")
        P_(f"    y_BN: d = {L_(o['yBN_d'])}.")
    P_(f"  Limite do critério para o grupo A: |d| de até 0,6. Observado {n_(abs(A['d']['coef']), 3)}. Phi calibrado do grupo A: {n_(ld['experimento_natural_A_Phi_calibrado'], 3, True)} (IC99 {n_(ld['experimento_natural_A_Phi_calibrado_ic99'][0], 3, True)} a {n_(ld['experimento_natural_A_Phi_calibrado_ic99'][1], 3, True)}).")
    P_('')
    P_('6. AMOSTRA DE LOGS (tipo de habilitação exato por eleitor; amostra estratificada, contraste dentro do local)')
    P_(f"  {i_(lg['n'])} seções em {lg['locais']} locais e {lg['municipios']} municípios. Frações no 2º turno: biométrica {n_(100 * lg['fracoes_2t_na_amostra']['B'], 2)}%, mesário (M) {n_(100 * lg['fracoes_2t_na_amostra']['M'], 2)}%, sem biometria (S) {n_(100 * lg['fracoes_2t_na_amostra']['S'], 2)}%.")
    P_(f"  Conta da letra: fM2 = {L_(lg['conta_a_letra']['fM2'], 2)}; fS2 = {L_(lg['conta_a_letra']['fS2'], 2)};")
    P_(f"    controles fM1 = {L_(lg['conta_a_letra']['fM1'], 2)}; fS1 = {L_(lg['conta_a_letra']['fS1'], 2)}.")
    P_(f"  Conta restrita (u2 = M + S do dia): b = {L_(lg['conta_b_restrita']['b'], 2)}; k (u1) = {L_(lg['conta_b_restrita']['k'], 2)}; erro por local {n_(lg['conta_b_restrita_erro_por_local']['b']['ep'], 2)}.")
    P_(f"  A marca pedia coeficiente NEGATIVO (até -2,04 para a margem inteira). O observado é positivo; lido como troca valeria {n_(abs(lg['conta_b_restrita']['Phi_letra']), 1)} margens a favor de Flávio (u2) ou {n_(abs(lg['conta_a_letra']['fS2']['coef']) / ESCALA, 1)} (fS2), tamanho que, para o campo M, a conta nacional exclui (IC99 de b até {n_(b['ic99'][1], 3, True)}); para S não existe conta nacional. O controle do 1º turno tem o mesmo tamanho e sinal oposto: é o desenho de quem compareceu a mais, não do nível.")
    P_(f"  Poder: a margem inteira plantada desloca u2 em {n_(res['calibracao_logs']['Phi_1.0']['u2']['delta_medio'], 2, True)} com erro {n_(res['calibracao_logs']['Phi_1.0']['u2']['ep_medio'], 2)} (t {n_(res['calibracao_logs']['Phi_1.0']['u2']['t_medio'], 1, True)}); vista em {n_(100 * res['calibracao_logs']['Phi_1.0']['u2']['poder_z33'], 0)}% das cópias. SEM PODER.")
    P_(f"  y_BN na amostra: u2 = {L_(lg['yBN_conta_b']['b'], 2)}.")
    P_('')
    P_('7. BRANCOS E NULOS (y_BN = 100 x (B2+N2)/comparecimento)')
    P_(f"  b = {L_(bn['b'])}; k = {L_(bn['k'])}; r (nb) = {L_(bn['r_nb'])}.")
    P_(f"  Phi_BN = {n_(bn['Phi_BN'], 3, True)} (IC99 {n_(bn['Phi_BN_ic99'][0], 3, True)} a {n_(bn['Phi_BN_ic99'][1], 3, True)}); votos convertidos {i_(bn['votos_convertidos'])} (IC99 {i_(bn['votos_convertidos_ic99'][0])} a {i_(bn['votos_convertidos_ic99'][1])}).")
    for q, o in res['calibracao_yBN'].items():
        if 'pulado' in o: P_(f"  Plantio Phi_BN {n_(o['Phi_BN'], 2)}: não plantado ({o['pulado']}; taxa {n_(o['f'], 2)}).")
        else: P_(f"  Plantio Phi_BN {n_(o['Phi_BN'], 2)}: {i_(o['votos_convertidos_medio'])} votos; delta de b {n_(o['delta_b_medio'], 3, True)}; recupera {n_(100 * o['recuperacao'], 0)}%; visto em {n_(100 * o['poder_z33'], 0)}% das cópias.")
    P_('')
    P_('8. DESFECHO CONTRA 2022 (y_alt; usa 2022 como referência, que o Léo não aceita como régua limpa)')
    P_(f"  {i_(alt['principal']['n'])} seções. b = {L_(alt['principal']['b'])}; k = {L_(alt['principal']['k'])}; r (nb) = {L_(alt['principal']['r_nb'])}.")
    P_(f"  Bruto: y de 2026 {n_(alt['principal']['bruto_2026']['y_2026_agregado'], 3)}% e de 2022 {n_(alt['principal']['bruto_2026']['y_2022_agregado'], 3)}% nas mesmas seções. Só mesmo código de local: b = {n_(alt['so_mesmo_codigo_de_local']['b']['coef'], 3, True)} ({n_(alt['so_mesmo_codigo_de_local']['b']['ep'])}).")
    P_(f"  Pareamento com 2022: {i_(alt['pareamento']['secoes'])} seções, {i_(alt['pareamento']['mesmo_codigo_de_local'])} com o mesmo código de local, {i_(alt['pareamento']['aptos_2022_dentro_de_10_por_cento_dos_de_2026'])} com aptos dentro de 10%. Veredito depende de 2022: INCONCLUSIVO por intervalo largo.")
    P_('')
    P_('9. PLACEBOS E ESPELHOS')
    P_(f"  Período anterior (virada de 2022 com m2 e m1 de 2026): b = {L_(plc['periodo_anterior']['b'])}; Phi {n_(plc['periodo_anterior']['Phi_letra'], 3, True)}; r (nb) = {n_(plc['periodo_anterior']['r_nb']['coef'], 3, True)} ({n_(plc['periodo_anterior']['r_nb']['ep'])}).")
    P_(f"  Turno trocado (1º turno de 2026 contra 2022, dose m1): b = {L_(plc['turno_trocado']['b'])}; Phi {n_(plc['turno_trocado']['Phi_letra'], 3, True)}; r (nb) = {n_(plc['turno_trocado']['r_nb']['coef'], 3, True)} ({n_(plc['turno_trocado']['r_nb']['ep'])}).")
    g = plc['cargo_governador']
    P_(f"  Cargo (governador do 2º turno, 6 UFs): b = {L_(g['b'], 2)}; qui-quadrado dos 6 z = {n_(g['qui2_dos_z'], 2)} (p = {n_(g['p_qui2'], 3)}); Phi {n_(g['Phi_letra'], 3, True)}.")
    for uf, o in g['por_uf'].items():
        P_(f"    {uf}: n {i_(o['n'])}; candidato do lado de Lula {o['lado_de_Lula']} (correlação {n_(o['correlacao_com_y'], 2)}); b = {n_(o['b']['coef'], 2, True)} ({n_(o['b']['ep'], 2)}; z {n_(o['b']['z'], 2, True)})")
    P_(f"  Espelho do experimento natural (grupo C): d = {L_(C['d'])}.")
    P_('  Espelho do critério: sinal contrário teria o mesmo destaque; não houve nos dois sentidos. Espelho do plantio: na seção 10.')
    P_('')
    P_('10. CALIBRAÇÃO POR EFEITO PLANTADO NOS DADOS DE 2026 (200 cópias por tamanho)')
    P_('  sentido    Phi   votos movidos   delta de b (esperado)   recupera   delta de k   visto a z 3,3   cópia cumpre SINAL   cópia não passa em SEM SINAL   grupo A: delta (t; visto)')
    for q, o in cal.items():
        if q.startswith('_'): continue
        P_(f"  {o['sentido']:9s} {n_(o['Phi'], 2):>5s} {i_(o['votos_movidos_medio']):>13s}   {n_(o['b']['delta_medio'], 3, True)} ({n_(o['b']['esperado'], 2, True)})       {n_(100 * o['b']['recuperacao'], 0):>4s}%     {n_(o['k']['delta_medio'], 3, True)}       {n_(100 * o['b']['poder_z33'], 0):>4s}%            {n_(100 * o['copia_cumpre_SINAL_numerico'], 0):>4s}%                  {n_(100 * o['eps_copia_nao_passa_SEM_SINAL'], 0):>4s}%               {n_(o['nat_A']['delta_medio'], 2, True)} ({n_(o['nat_A']['t_medio'], 1, True)}; {n_(100 * o['nat_A']['poder_z33'], 0)}%)")
    P_(f"  Menor Phi visto com 95% de chance a z de 3,3: {n_(calr['menor_Phi_com_poder_de_95_por_cento_a_z_3_3'], 3)}. Meia largura do IC99 em Phi: {n_(calr['meia_largura_ic99_em_Phi'], 3)}. Regra geral da frente (95% para Phi 0,25): não cumprida, como o registro previa.")
    P_(f"  Regra da D15: recuperação de Phi = 1 entre 0,80 e 1,25 ({n_(c1['b']['recuperacao'], 3)}), visto em 95% ou mais ({n_(100 * c1['b']['poder_z33'], 0)}%), cópia com um quarto da margem não passa por SEM SINAL ({n_(100 * c25['eps_copia_nao_passa_SEM_SINAL'], 0)}%): o teste TEM PODER para meia margem ou mais.")
    P_('')
    P_('11. VALOR BRUTO DE 2026 POR FAIXA DE m2 (sem modelo)')
    P_('  faixa de m2      seções        votos    y 2º turno   y 1º turno   ganho    brancos e nulos 2º (1º)')
    for t in res['bruto_2026_por_faixa_de_m2']:
        P_(f"  {n_(t['faixa_m2'][0], 2)} a {n_(t['faixa_m2'][1], 2)}  {i_(t['n']):>9s} {i_(t['V']):>12s}   {n_(t['y_2t'], 2):>8s}    {n_(t['y_1t'], 2):>8s}    {n_(t['ganho_2t_menos_1t'], 2, True)}    {n_(t['yBN_2t'], 2)} ({n_(t['yBN_1t'], 2)})")
    P_('  O ganho cai com m2 no bruto. As seções com mais liberação manual ficam em lugares onde Lula já era mais forte no 1º turno; a seção 15 mostra o que sobra ao comparar vizinhos.')
    P_('')
    P_('12. SENSIBILIDADES (fixadas antes; não decidem)')
    for q, o in res['sensibilidades'].items():
        P_(f"  {q:28s} b = {L_(o['b'])}" + (f"; k = {n_(o['k']['coef'], 3, True)} ({n_(o['k']['ep'])})" if o.get('k') else ''))
    P_('')
    P_('13. TRADUÇÃO EM VOTOS')
    P_(f"  Dose do dia: Phi {n_(P['Phi_letra'], 3, True)} = {i_(P['votos_trocados'])} votos trocados = {i_(P['votos_de_margem'])} votos de margem (negativo = a favor de Flávio).")
    P_(f"  IC99: de {i_(P['votos_de_margem_ic99'][0])} a {i_(P['votos_de_margem_ic99'][1])} votos de margem, contra 4.430.191 da margem oficial. No sentido da tese o teto é {i_(ld['limite_no_sentido_da_tese_votos_de_margem'])} ({i_(ld['limite_no_sentido_da_tese_votos_de_margem_calibrado'])} calibrado).")
    P_(f"  Brancos e nulos: {i_(bn['votos_convertidos'])} votos convertidos (IC99 {i_(bn['votos_convertidos_ic99'][0])} a {i_(bn['votos_convertidos_ic99'][1])}).")
    P_('')
    P_('14. O QUE PESA A FAVOR DA TESE')
    for i, t in enumerate(a_favor): P_(f'  ({i + 1}) {t}')
    P_('')
    P_('    O QUE PESA CONTRA A TESE')
    for i, t in enumerate(contra): P_(f'  ({i + 1}) {t}')
    P_('')
    P_('15. EXPLORATÓRIO (feito depois de ver o resultado; não muda veredito)')
    P_('  Escada do ganho bruto (y menos a fração de Lula no 1º turno) em m2:')
    for q in ('sem_efeito_fixo', 'efeito_fixo_de_UF', 'efeito_fixo_de_municipio', 'efeito_fixo_de_local'):
        o = esc[q]; P_(f"    {q:26s} só m2: {L_(o['so_m2'])}; com m1: m2 {n_(o['com_m1']['m2']['coef'], 3, True)} ({n_(o['com_m1']['m2']['ep'])}), m1 {n_(o['com_m1']['m1']['coef'], 3, True)} ({n_(o['com_m1']['m1']['ep'])})")
    P_('  Dentro do local, desfecho y, acrescentando os blocos de controle do registro (m2 e m1 sempre presentes):')
    for q, o in esc['dentro_do_local_acrescentando_blocos'].items():
        P_(f"    {q:42s} m2 {L_(o['m2'])}; m1 {n_(o['m1']['coef'], 3, True)} ({n_(o['m1']['ep'])})")
    P_(f"  Dose e resposta no ganho bruto dentro do local: até 0,2: {L_(esc['ganho_bruto_dentro_do_local_por_trecho_de_m2']['m2_ate_0_2'])}; acima de 0,2: {L_(esc['ganho_bruto_dentro_do_local_por_trecho_de_m2']['m2_acima_de_0_2'])}.")
    P_(f"  Grupos sem controles: A {L_(esc['ganho_bruto_dentro_do_local_grupo_A_m2_0_5_ou_mais'])}; B {L_(esc['ganho_bruto_dentro_do_local_grupo_B_leitor_caiu'])}; C {L_(esc['ganho_bruto_dentro_do_local_grupo_C_espelho'])}.")
    P_('  nb aberto por idade (modelo completo de 2026 | virada de 2022):')
    for q in ('nb_16a19', 'nb_20a24', 'nb_25a44', 'nb_45a59', 'nb_60mais'):
        a = nbi['modelo_2026_nb_aberto_por_idade'][q]; c = nbi['virada_de_2022_nb_aberto_por_idade'][q]
        P_(f"    {q:10s} {n_(a['coef'], 3, True)} ({n_(a['ep'])}; z {n_(a['z'], 1, True)})  |  {n_(c['coef'], 3, True)} ({n_(c['ep'])}; z {n_(c['z'], 1, True)})")
    P_(f"    Eleitores sem biometria no cadastro de U: {i_(nbi['sem_biometria_total_perfil'])}; de 20 a 24 anos: {i_(nbi['sem_biometria_no_pais_por_idade']['n2024'])} ({n_(100 * nbi['fracao_sem_biometria_entre_20_e_24'], 1)}% dos eleitores dessa idade).")
    P_('  Valor bruto de 2026 por quinto de nb: ' + '; '.join(f"{n_(t['nb_medio'], 3)}: ganho {n_(t['ganho_2t_menos_1t'], 2, True)}" for t in ex['bruto_2026_por_faixa_de_nb']) + '.')
    P_(f"  Logs em nível e variação: variação de S {L_(el['nivel_e_variacao']['S_variacao'], 2)}; nível de S {L_(el['nivel_e_variacao']['S_nivel_1t'], 2)}; variação de M {L_(el['nivel_e_variacao']['M_variacao'], 2)}; nível de M {L_(el['nivel_e_variacao']['M_nivel_1t'], 2)}.")
    P_(f"    Um desvio-padrão da variação de S ({n_(el['dp_da_variacao_de_S'], 4)}) vale {n_(el['efeito_de_um_dp_da_variacao_de_S_em_pp'], 2, True)} p.p. Comparecimento do 1º para o 2º turno na amostra: biométrica {n_(el['comparecimento_por_tipo_na_amostra']['B_biometrica']['variacao_pct'], 1, True)}%, mesário {n_(el['comparecimento_por_tipo_na_amostra']['M_mesario']['variacao_pct'], 1, True)}%, sem biometria {n_(el['comparecimento_por_tipo_na_amostra']['S_sem_biometria']['variacao_pct'], 1, True)}%.")
    P_(f"    Modelo nacional rodado só na amostra: b = {L_(el['modelo_nacional_so_na_amostra']['b_m2'], 2)}. O campo M é o mesmo do bweb; a conta nacional ({n_(b['coef'], 3, True)}, erro {n_(b['ep'])}) é {n_((el['modelo_nacional_so_na_amostra']['b_m2']['ep'] / b['ep']) ** 2, 0)} vezes mais precisa.")
    P_(f"    Correlação dentro do local entre a fração S e a fração de eleitores de 18 a 24 anos: {n_(el['correlacao_dentro_do_local_fS2_com']['i1824'], 2, True)}.")
    P_('')
    P_('16. CONTAGEM DE TESTES')
    ct = res['contagem_de_testes']
    P_(f"  {ct['estatisticas_com_limiar_de_z_3_3']} estatísticas com limiar de z 3,3 ({ct['nota']}). Sinais esperados pelo acaso: {n_(ct['sinais_esperados_pelo_acaso'], 3)}.")
    P_(f"  Passaram de 3,3 em módulo: nenhuma das que decidem. Na conta da letra dos logs, fS2 tem z {n_(lg['conta_a_letra']['fS2']['z'], 2, True)}, no sentido contrário ao da tese, numa parte sem poder. O coeficiente de nb (z {n_(P['r_nb']['z'], 2, True)}) é controle, não estatística de teste.")
    P_('')
    P_('17. DESVIOS E DECISÕES')
    for i, t in enumerate(desvios): P_(f'  ({i + 1}) {t}')
    P_('')
    P_('18. PISTAS')
    for i, t in enumerate(pistas): P_(f'  ({i + 1}) {t}')
    P_('')
    P_('19. LIMITES')
    P_('  O teste usa só arquivos da própria urna (boletim e log): vale contra a versão parcial da hipótese, não contra programa adulterado que troque voto de todo eleitor.')
    P_('  SINAL ou SEM SINAL deste teste só contam depois de o conferente independente reproduzir com código próprio.')
    txt = '\n'.join(T) + '\n'
    assert chr(8212) not in txt and chr(8211) not in txt
    js = json.dumps(res, ensure_ascii=False, indent=1, default=_jd)
    assert chr(8212) not in js and chr(8211) not in js
    with open(RAIZ + '/resultados/R27_A6_tipo_habilitacao.txt', 'w') as fh: fh.write(txt)
    with open(RAIZ + '/resultados/R27_A6_tipo_habilitacao.json', 'w') as fh: fh.write(js)
    with open(TRAB + '/sha256_finais.json', 'w') as fh:
        json.dump({'txt': hashlib.sha256(txt.encode()).hexdigest(), 'json': hashlib.sha256(js.encode()).hexdigest(), 'docstring': sha_docstring()}, fh, indent=1)
    log('saídas gravadas')


if __name__ == '__main__':
    modo = sys.argv[1] if len(sys.argv) > 1 else ''
    if modo == 'perfil':
        extrair_perfil()
    elif modo == 'gov2t':
        extrair_gov2t()
    elif modo == 'rodar':
        rodar()
    elif modo == 'txt':
        with open(TRAB + '/resultado_completo.json') as fh:
            escrever(json.load(fh))
    else:
        print(__doc__)
