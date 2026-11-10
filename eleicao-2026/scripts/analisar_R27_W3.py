"""R27_W3: TESTEMUNHAS NA TELA DE GOVERNADOR, AC e TO (teste D4-3 de registro/adendo27/desenho_D4_proposta.json, por inteiro).

Registro: Adendo 27 (commit 2748895, 10/11/2026 00:16:42 UTC), Onda D-b, e Adendo 30 (commit a7218fb, última onda).
O critério vale como está no campo do desenho D4-3. Este docstring foi escrito ANTES de qualquer conta com votos; o
que ele decide e o registro não fixa está em DECISÕES e sai no resultado como desvio. Até aqui só foi lida estrutura
sem voto: o índice dos pacotes do TSE (nomes e tamanhos dos arquivos), a lista de números de candidatos a presidente
e a governador, o formato do RDV em 20 seções do AC da amostra aleatória (contagem por eleição, cargo, tipo de voto e
quantidade de dígitos, SEM separar os dígitos digitados), o número de seções e de locais de AC e TO na base e os
códigos de escolaridade do perfil do eleitorado.

Uso (nesta ordem):
  python3 -I scripts/analisar_R27_W3.py baixar 2026 1t AC   lê o pacote do TSE em fluxo e guarda só RDV e boletim
  python3 -I scripts/analisar_R27_W3.py extrair 2026        lê os RDV guardados e monta a tabela por seção
  python3 -I scripts/analisar_R27_W3.py conferir 2026       RDV contra bweb (presidente e governador)
  python3 -I scripts/analisar_R27_W3.py etapa1              só o número de testemunhas por turno e o erro-padrão
  python3 -I scripts/analisar_R27_W3.py validade            termômetro no 1º turno (antes de abrir Theta)
  python3 -I scripts/analisar_R27_W3.py abrir               Theta, leituras secundárias, calibração, espelho, votos
  python3 -I scripts/analisar_R27_W3.py placebo             AL 2022 (se os pacotes de 2022 tiverem sido lidos)
  python3 -I scripts/analisar_R27_W3.py relatorio           grava resultados/R27_W3_testemunhas_governador.json e .txt
Trabalho e parciais: /home/user/trabalho-eleicao/adendo27/R27_W3/

Pergunta. Se a contagem de presidente foi alterada dentro da urna, por qualquer mecanismo, inclusive troca sorteada
voto a voto, o registro do cargo de governador na mesma urna não foi tocado. Parte dos eleitores digita na tela de
governador o número do seu presidenciável. Em AC e TO, 13 e 22 não são candidatos a governador em nenhum dos turnos,
e isso vira voto nulo de governador com os dígitos gravados no RDV: uma amostra da intenção presidencial que não
passa pela apuração de presidente.

O QUE O REGISTRO FIXA (aplicado à letra)
- Dados: RDV do 1º e do 2º turno, cargo governador, nulos com dígitos, de todas as seções de AC (2.270) e TO (4.384).
  Votos oficiais de presidente das mesmas seções: dados/secoes2026.json.gz. Perfil por seção para tercis de
  escolaridade.
- Por seção e turno t: g13 e g22 = nulos de governador cujos dígitos são exatamente 13 e 22. Nas seções presentes
  nos dois turnos: W_t = soma de g13 / soma de (g13 + g22); P_t = soma de L / soma de (L + R), nas mesmas seções.
  Theta = [logit P_2 menos logit P_1] menos [logit W_2 menos logit W_1].
- Erro-padrão por bootstrap de locais de votação, 2.000 réplicas.
- Abertura em duas etapas: primeiro só o número de testemunhas por turno e o erro-padrão, sem imprimir Theta; se o
  erro-padrão passar de 0,025 o teste é declarado SEM PODER; só então se abre Theta.
- Validade do termômetro, conferida no 1º turno antes de abrir: a composição das testemunhas por número (13, 22 e os
  números de eliminados que não são candidatos a governador na UF) tem de acompanhar a votação oficial do 1º turno
  por município (correlação de postos de pelo menos 0,9).
- Leituras secundárias: Theta por UF e por tercil de escolaridade da seção; intervalo do que uma conversão diferente
  dos eliminados entre os que erram a tela poderia explicar, com as testemunhas do 1º turno que digitaram número de
  eliminado.
- SINAL: Theta de pelo menos 0,045 em AC e TO somados, e Theta de pelo menos 2,5 vezes o erro total (raiz de
  erro-padrão ao quadrado mais erro sistemático ao quadrado, erro sistemático = maior entre 0,015 e |Theta| no placebo
  de 2022), com o mesmo sinal em AC e em TO separadamente e nos três tercis de escolaridade.
- SEM SINAL: |Theta| de no máximo 0,020 com erro total de no máximo 0,025.
- INCONCLUSIVO: erro total acima de 0,025; Theta entre 0,020 e 0,045; termômetro reprovado na validade do 1º turno;
  sinais opostos em AC e TO.
- Calibração: plantar a troca de 1,8% e de 3,57% dos votos de R para L só na contagem oficial dessas seções e conferir
  que Theta sobe o valor da fórmula ln[(1 + p R/L)/(1 - p)]; conferir com duas metades aleatórias das seções que a
  diferença entre metades fica dentro do erro.
- Placebos: (1) AL em 2022, dois turnos, mesma conta; (2) dentro do 1º turno de 2026, W contra P por município, em
  nível; (3) no 1º turno, a razão entre dois números de eliminados digitados na tela de governador contra os votos
  oficiais desses dois candidatos.
- Só descritivo: ES no 2º turno, DF, AM e RN.

DECISÕES QUE O REGISTRO NÃO FIXA (escritas antes de calcular; relatadas como desvios)
D1. Fonte dos RDV: os pacotes "arquivos transmitidos para totalização" do TSE por UF e turno (cdn.tse.jus.br,
    arqurnatot), e não o download seção a seção que o desenho cita. O pacote é lido em fluxo (o índice do zip vem por
    um pedido de faixa; depois um único pedido lê o arquivo do começo ao fim), nada do zip fica em disco, e só os
    membros -rdv.dat e -bu.dat são guardados, recompactados, em pacotes/. Cada membro guardado tem o CRC conferido
    contra o índice do zip. Os logs, as imagens de boletim e as assinaturas não são guardados.
D2. Universo: seções de AC e TO que estão nos dois turnos da base secoes2026 E têm RDV nos dois turnos no pacote E
    cujo RDV de presidente (13, 22, demais nominais somados, brancos, nulos) é igual ao bweb nos dois turnos. As que
    falharem em qualquer condição ficam fora da conta principal, são contadas e listadas, e a conta é repetida com
    elas quando houver RDV (sensibilidade).
D3. Testemunha: voto do RDV no cargo 3 (governador), tipo 4 (nulo com dígitos), dígitos exatamente "13" ou "22".
    Nulo sem dígitos (tipo 6), branco e qualquer outro tipo não contam. Antes de usar, confiro no próprio RDV que não
    há voto NOMINAL de governador nos números 13 e 22 em AC e TO, em nenhum turno.
D4. P_t vem do bweb (dados/secoes2026.json.gz), não do RDV. Logit natural.
D5. Bootstrap: unidade = local de votação (UF|município|zona|local do 2º turno na base); sorteio com reposição
    dentro de cada UF (a UF é fixa, não é sorteada); 2.000 réplicas; semente 20261110; erro-padrão = desvio-padrão
    das réplicas. As mesmas réplicas servem aos recortes (UF, tercil). Ao lado, intervalo de 95% por percentis.
D6. Etapa 1: imprime e grava só a soma g13 + g22 por turno (total e por UF) e os erros-padrão; não imprime nem grava
    Theta, W_2, nem g13 e g22 separados do 2º turno. O modo abrir só roda depois de etapa1 e validade gravados.
D7. Validade do termômetro (o texto do registro admite mais de uma conta; fixo aqui qual decide).
    Leitura que decide: correlação de postos (Spearman), entre municípios de AC e TO juntos, de
    W_1m = g13 / (g13 + g22) do 1º turno contra P_1m = L / (L + R) oficial do 1º turno (é o placebo 2 do registro,
    "W contra P por município, em nível (validade)"). Limiar do registro: 0,9, sem mudança.
    Problema previsto antes de olhar: o TO tem 139 municípios, a maioria pequena, e com poucas dezenas de
    testemunhas o ruído de amostragem sozinho derruba a correlação de postos abaixo de 0,9 mesmo com termômetro
    perfeito. Regra fixada para isso, usando só a contagem de testemunhas por município (sem separar 13 de 22) e os
    votos oficiais: simulo um termômetro perfeito (g13 sorteado de uma binomial com n_m = testemunhas do município e
    p = P_1m, 2.000 sorteios) e tomo n_min = o menor valor da grade 1, 50, 100, 200, 400, 800 para o qual o
    termômetro perfeito passa de 0,9 em pelo menos 95% dos sorteios, com pelo menos 10 municípios. A validade é
    decidida nos municípios com pelo menos n_min testemunhas no 1º turno. Se nenhum valor da grade servir, a
    validade decide por compatibilidade: aprovado se a correlação observada em todos os municípios ficar no
    percentil 5 ou acima do termômetro perfeito simulado, e isso é dito como desvio maior.
    Ao lado, sem poder de decisão: a mesma correlação em todos os municípios (leitura sem mínimo) com o teto de
    ruído; por UF; a correlação por células (município x número, parcela do número entre as testemunhas contra a
    parcela do candidato na votação oficial dos mesmos números); a composição por número no agregado da UF; e as
    correlações das parcelas de 13 e de 22 com os eliminados no denominador. Se a leitura sem mínimo reprovar, o
    relatório diz qual seria o veredito por ela.
    Números de eliminados que não são candidatos a governador na UF (lista de candidatos do bweb do 1º turno):
    AC: 14, 16, 27, 28, 29, 30, 35, 55, 70, 80 (o 21 é candidato a governador no AC).
    TO: 14, 16, 21, 28, 29, 70, 80 (27, 30, 35 e 55 são candidatos a governador no TO).
D8. Tercil de escolaridade da seção: perfil do eleitorado por seção (cadastro de 14/07/2026); medida = parcela dos
    eleitores da seção com até ensino fundamental incompleto (códigos 1 analfabeto, 2 lê e escreve, 3 fundamental
    incompleto) sobre os eleitores com escolaridade informada (códigos 1 a 8). Tercis com o mesmo número de seções,
    AC e TO juntos, entre as seções do universo com perfil. Tercil "baixa" = maior parcela de pouca escolaridade.
    Seções sem perfil ficam fora só dessa leitura. Sensibilidade: tercis pela parcela com superior completo
    (código 8), a medida usada no teste A2.
D9. Ordem do veredito pela letra: (1) SEM PODER se o erro-padrão de Theta (AC e TO somados) passar de 0,025, ou se a
    calibração não enxergar o plantado (D11); (2) INCONCLUSIVO se o termômetro for reprovado na validade (D7);
    (3) SEM SINAL se |Theta| <= 0,020 e erro total <= 0,025; (4) SINAL se Theta >= 0,045, Theta >= 2,5 erros totais
    e mesmo sinal em AC, em TO e nos três tercis; (5) o resto é INCONCLUSIVO. A cláusula "sinais opostos em AC e TO"
    é lida como motivo de inconclusivo quando Theta passa dos limiares de tamanho do SINAL; para o SEM SINAL valem
    só as duas condições que o registro lista. Theta abaixo de -0,020 (sentido contrário ao da tese) não tem
    cláusula no registro: fica INCONCLUSIVO pela letra e é lido no teste espelho.
D10. Erro sistemático: maior entre 0,015 e |Theta| do placebo AL 2022, à letra. Como o Léo suspeita também de 2022,
    o veredito sai duas vezes: só com o mínimo de 0,015 (sem usar outro ano) e com o placebo. Se o placebo não
    puder ser rodado, vale 0,015 e isso é dito.
D11. Calibração por efeito plantado (irregularidade): em cada seção, x ~ Binomial(R_2, p) votos oficiais do 2º turno
    passam de R para L (p = 0,018 e 0,0357; semente 20261110), só na contagem oficial; as testemunhas não mudam.
    O teste "enxerga o plantado" se, com p = 0,0357, o aumento de Theta ficar a até 10% do valor da fórmula
    ln[(1 + p R/L)/(1 - p)] (R e L = totais oficiais do 2º turno do universo) E esse aumento for de pelo menos 2,5
    erros totais (com erro sistemático mínimo de 0,015). Ao lado: o critério de SINAL aplicado ao dado com o
    plantio, do jeito que sai. Se não enxergar, o veredito é SEM PODER.
D12. Explicação inocente plantada: (i) conversão diferente dos eliminados entre os que erram a tela: no 2º turno,
    em cada seção, n = Binomial(e_s, delta * k) testemunhas passam de 13 para 22 (e_s = testemunhas de eliminados
    da seção no 1º turno, k = razão entre o total de testemunhas do 2º e do 1º turno, delta = 0,10 e 0,25,
    limitado ao g13 da seção), e Theta tem de subir o que a fórmula do intervalo prevê; (ii) queda geral da
    propensão ao erro: cada testemunha do 2º turno é mantida com probabilidade 0,5, igual para 13 e 22, e Theta não
    pode mudar além do erro.
D13. Intervalo dos eliminados: a = soma de g13 do 1º turno, b = soma de g22 do 1º turno, e = soma das testemunhas do
    1º turno com número de eliminado (lista do D7). Se, entre os que erram a tela, a parcela dos eliminados que vai
    para Lula for c_w em vez de c_0, o logit do termômetro do 2º turno muda de ln[(a + c_0 e)/(b + (1 - c_0) e)]
    para ln[(a + c_w e)/(b + (1 - c_w) e)]. Relato o deslocamento de Theta para c_w - c_0 = -0,10, -0,25 e +0,10,
    +0,25 em torno de c_0 = 0,5, e os extremos c_w = 0 e c_w = 1. É um limite do efeito possível, não estimativa.
D14. Duas metades: as seções são divididas ao acaso em duas metades, 200 vezes (semente 20261110); em cada divisão,
    diferença de Theta entre as metades dividida pelo erro (raiz da soma dos quadrados dos erros-padrão das metades,
    bootstrap de 400 réplicas por metade nas 20 primeiras divisões; nas demais uso o erro médio dessas 20). Passa
    se a fração de divisões com |z| acima de 2 for de no máximo 10%.
D15. Teste espelho: (a) a mesma regra de SINAL aplicada a -Theta (alteração a favor de Flávio); (b) onde não
    deveria dar nada: o placebo 3 (D16) e as duas metades (D14).
D16. Placebo 3: par de eliminados = 70 e 14, os dois mais votados no país que não são número de governador nem no
    AC nem no TO. No 1º turno: logit de n70/(n70 + n14) entre as testemunhas menos logit de V70/(V70 + V14)
    oficial, nas seções do universo, com erro por bootstrap de locais; por UF; e correlação de postos por município
    entre os que têm pelo menos 30 testemunhas do par. O registro só diz "deve acompanhar": sem limiar, descritivo.
D17. Tradução em votos: Theta medido em AC e TO equivale a uma fração p dos votos verdadeiros de Flávio contada
    para Lula nessas seções: P_verd = expit(logit P_2 - Theta); p = (P_2 - P_verd)/(1 - P_verd). Se a mesma fração
    valesse no país: votos trocados x = p/(1 - p) * 59.826.041, efeito na margem = 2x, comparado com 4.430.191.
    Com o intervalo de Theta mais ou menos 1,96 erro total. A extrapolação de AC e TO (1,3% das seções) para o país
    é suposição, não medida.
D18. Descritivo de ES, DF, AM e RN: feito só com os RDV da amostra aleatória nova de 3.000 seções (as seções dessas
    UFs que caíram na amostra), não com os pacotes inteiros dessas UFs (não cabem no tempo). Sem veredito.
D19. Leitura secundária acrescentada aqui (não está no registro; não decide): Theta com o lado oficial pesado pelas
    testemunhas, para tirar o efeito de as testemunhas estarem concentradas em certas seções. P*_t = soma em s de
    n_s * [L_st/(L_st + R_st)] / soma de n_s, com n_s = testemunhas (13 + 22) da seção nos dois turnos somados.
D20. Diagnóstico acrescentado aqui (não está no registro; não decide): Theta = menos a variação entre turnos de
    ln(r13/r22), onde r13 = g13/L e r22 = g22/R são as taxas de erro de tela por eleitor de cada lado. Uma mudança
    da taxa de UM lado só (por exemplo, o eleitor de um lado ficar sem candidato a governador no 2º turno e anular
    de propósito digitando o número do presidenciável) desloca Theta sem alteração de contagem. Relato r13 e r22
    por turno e UF, e Theta por tercil da parcela dos votos válidos de governador do 1º turno dada a candidatos
    eliminados na seção (tercis por seção, AC e TO juntos). Se Theta variar com essa parcela, o termômetro está
    medindo a disputa de governador, e isso pesa no erro sistemático dito no relatório.
D21. Placebo AL 2022: mesma conta (testemunha = nulo de governador com dígitos 13 ou 22; oficial =
    dados/secoes2022.json.gz; bootstrap por local; universo pelo D2 com a base de 2022). Antes de usar, confiro no
    RDV que 13 e 22 não têm voto nominal de governador em AL em 2022. Os pacotes de 2022 existem no mesmo endereço
    (1,09 GB e 1,43 GB); como a leitura é em fluxo, cabem.
D22. Contagem de cláusulas para o acaso: a principal, o espelho, 2 UFs, 3 tercis, o placebo 3 e as duas metades.

O QUE FOR FEITO DEPOIS DE VER O RESULTADO fica em funções com nome "exploratorio_" e sai marcado assim.

Aviso que vale para o teste inteiro: RDV e boletim saem do mesmo programa da urna. O teste enxerga uma alteração
que mexa só na contagem de presidente; um programa que também reescrevesse os nulos de governador de forma coerente
escaparia. Vale só para AC e TO.
"""
import sys, os, gzip, json, zipfile, zlib, struct, time, io, collections, csv, math, ssl
import urllib.request, urllib.error

RAIZ = '/home/user/casa-control/eleicao-2026'
TRAB = os.environ.get('W3_TRAB', '/home/user/trabalho-eleicao/adendo27/R27_W3')  # W3_TRAB só para ensaio com dado sintético
PERFIL_DIR = '/home/user/trabalho-eleicao/adendo21/F15_dl_perfil_secao'
BWEB1 = '/home/user/trabalho-eleicao/bweb1t/zips'
BWEB2 = '/home/user/trabalho-eleicao/trab2t/zips2t'
AAS = '/home/user/trabalho-eleicao/adendo27/aas'
sys.path.insert(0, RAIZ + '/scripts')
from ber import parse  # noqa: E402

SEMENTE = 20261110
NBOOT = 2000
MARGEM = 4430191
L2_OFICIAL, R2_OFICIAL = 64256232, 59826041
UFS = ['AC', 'TO']
ELIM = {'AC': ['14', '16', '27', '28', '29', '30', '35', '55', '70', '80'],
        'TO': ['14', '16', '21', '28', '29', '70', '80']}
PAR_PLACEBO3 = ('70', '14')
URL = 'https://cdn.tse.jus.br/estatistica/sead/eleicoes/eleicoes{ano}/arqurnatot/bu_imgbu_logjez_rdv_vscmr_{ano}_{turno}_{uf}.zip'
AGENTE = 'auditoria-eleicao (pesquisa; leitura em fluxo, 1 pedido por pacote)'
CTX = ssl.create_default_context(cafile=os.environ.get('SSL_CERT_FILE', '/root/.ccr/ca-bundle.crt'))


DECISOES_RETOMADA = """DECISÕES ACRESCENTADAS NA RETOMADA (10/11/2026, por volta de 11h UTC, ANTES de qualquer conta com votos).
O docstring acima é o do commit 6677983 (10/11/2026 10:48:36 UTC), sem mudança de uma letra. A execução anterior foi
interrompida na leitura do segundo pacote; nenhum RDV tinha sido aberto para contar voto. O que segue só completa o
que o docstring deixou sem dizer; nada muda limiar. Sai no resultado como desvio.
R1. Conferência: além da base secoes2026 (D2 e D4), o RDV é conferido direto contra os zips do bweb de AC e TO,
    candidato a candidato, brancos e nulos, para presidente e para governador, nos dois turnos. A regra do universo
    continua a do D2 (os cinco números de presidente contra a base). A lista de candidatos a governador por UF e turno
    sai do bweb, e a ausência do 13 e do 22 é conferida ali e nos votos nominais do RDV.
R2. Correlação de postos: Spearman com postos médios nos empates. Município sem nenhuma testemunha 13 ou 22 no 1º
    turno fica fora das correlações de W (W não existe). Simulações do D7 com a semente 20261110.
R3. Células do D7 (ao lado, sem decidir): por UF, números 13, 22 e os eliminados do D7; célula = município x número;
    parcela do número entre as testemunhas desses números no município contra a parcela oficial do mesmo candidato
    entre os mesmos números; Spearman sobre todas as células de municípios com pelo menos 1 testemunha, e, como a
    diferença entre números domina essa conta, também a correlação por número, entre municípios.
R4. D11: o critério "enxerga o plantado" usa o plantio com a semente 20261110. Ao lado, 200 plantios com sementes
    20261111 a 20261310 (média e desvio do aumento). O critério de SINAL no dado com plantio usa o mesmo bootstrap
    de locais. O plantio espelhado (fração p dos votos de L para R) é feito do mesmo jeito para calibrar o espelho.
    Poder dito ao lado: a menor fração p cuja fórmula alcança o maior entre 0,045 e 2,5 erros totais.
R5. D12: (i) 200 plantios; passa se o aumento médio de Theta ficar a até 10% do valor direto
    -[ln((A2 - m)/(B2 + m)) - ln(A2/B2)], com A2 e B2 = somas de g13 e g22 do 2º turno e m = média de testemunhas
    movidas; o valor da fórmula do intervalo (D13) vai ao lado. (ii) 200 sorteios; passa se o valor absoluto da
    mudança média de Theta for de no máximo metade do erro-padrão de Theta; o desvio entre sorteios vai ao lado.
R6. D18: seções de ES, DF, AM e RN da amostra aleatória nova com RDV nos dois turnos em disco. Por UF e turno:
    nulos de governador com dígitos 13 e 22 só quando o número não tem voto nominal de governador naquela UF e
    turno; taxa por mil votos oficiais do mesmo lado nas mesmas seções (g13/L, g22/R); no ES, 2º turno, W_2 ao lado
    de P_2. Sem erro além do binomial, sem veredito.
R7. D20: finalistas de governador AC 10 e 11, TO 44 e 45 (observação do desenho D4, conferida no bweb do 2º turno).
    Parcela = 1 menos os votos nominais dos dois finalistas sobre os votos nominais de governador do 1º turno da
    seção (RDV). Seção sem voto nominal de governador fica fora dessa leitura.
R8. Placebo AL 2022 (D21): os pacotes de 2022 têm outro padrão de nome (o00406-MMMMMZZZZSSSS.rdv); a chave sai do
    nome e da identificação do próprio RDV. O boletim de 2022 não é decodificado (o leitor do repositório é o de
    2026); a conferência de 2022 é RDV de presidente contra dados/secoes2022.json.gz. Sem tercis (não há perfil de
    2022 em disco). Ao lado, a validade por município em AL (mesma regra do D7) e as taxas r13 e r22 por turno.
    Para andar no tempo, o pacote de AL 2022 é lido em fluxo ao mesmo tempo que o de TO 2026 (dois fluxos no cdn,
    nada em disco além de RDV e boletim): desvio da regra de um pacote por vez, dito no relatório.
R9. Etapa 1 também grava o número de seções, de locais e de seções com pelo menos uma testemunha, e o erro-padrão
    por UF. Réplicas de bootstrap com soma zero em algum termo (logit indefinido) são contadas e ficam fora do
    desvio-padrão.
R10. Sensibilidade do D2: Theta repetido com todas as seções que têm RDV nos dois turnos, mesmo as reprovadas na
    conferência, usando os votos oficiais da base.
"""

DECISOES_RETOMADA_2 = """ACRESCENTADO ÀS 11:10 UTC DE 10/11/2026, ainda ANTES da etapa 1 e de qualquer contagem de testemunha separada por
lado (até aqui só rodaram a conferência do AC contra o bweb, que não separa 13 de 22, e ensaios do código com
testemunhas sintéticas). Não decide nada.
R11. Leitura secundária por força: Theta por tercil da parcela oficial de Lula no 1º turno da seção (L1/(L1+R1);
    tercis com o mesmo número de seções, AC e TO juntos). Sob troca proporcional uniforme de fração p dos votos de
    Flávio, Theta de cada grupo vale ln[(1 + p R/L)/(1 - p)] com R/L do 2º turno do grupo, logo cresce onde Flávio é
    forte; sob mudança uniforme de comportamento de quem erra a tela, Theta é igual nos grupos. Relato Theta por
    tercil, a diferença entre o tercil em que Lula é mais fraco e o em que é mais forte (erro pelo mesmo bootstrap)
    e a diferença que a fórmula prevê para p = 3,57%.
"""


def P(*a):
    print(*a, flush=True)


def grava(nome, obj):
    os.makedirs(TRAB, exist_ok=True)
    tmp = f'{TRAB}/{nome}.tmp'
    with open(tmp, 'w') as f:
        json.dump(obj, f, ensure_ascii=False, indent=1)
    os.replace(tmp, f'{TRAB}/{nome}')


def le(nome):
    with open(f'{TRAB}/{nome}') as f:
        return json.load(f)


# ---------------------------------------------------------------- leitura dos pacotes em fluxo (sem resultado)
def _pedido(url, ini=None, fim=None):
    req = urllib.request.Request(url, headers={'User-Agent': AGENTE})
    if ini is not None:
        req.add_header('Range', f'bytes={ini}-{"" if fim is None else fim}')
    return urllib.request.urlopen(req, timeout=180, context=CTX)


def _indice(url):
    """Lê o diretório central do zip com dois pedidos de faixa. Devolve (tamanho, cabeçalhos, entradas)."""
    req = urllib.request.Request(url, method='HEAD', headers={'User-Agent': AGENTE})
    with urllib.request.urlopen(req, timeout=120, context=CTX) as r:
        tam = int(r.headers['Content-Length'])
        cab = {k: r.headers.get(k) for k in ('Last-Modified', 'ETag', 'Content-Length')}
    time.sleep(1)
    with _pedido(url, tam - 70000, tam - 1) as r:
        fim = r.read()
    i = fim.rfind(b'PK\x05\x06')
    if i < 0:
        raise RuntimeError('fim do diretório central não achado')
    _, _, _, _, n, sz, off, _ = struct.unpack('<IHHHHIIH', fim[i:i + 22])
    if off == 0xFFFFFFFF or n == 0xFFFF:
        j = fim.rfind(b'PK\x06\x06')
        if j < 0:
            raise RuntimeError('zip64 sem registro')
        sz, off = struct.unpack('<QQ', fim[j + 40:j + 56])
        n = struct.unpack('<Q', fim[j + 32:j + 40])[0]
    time.sleep(1)
    with _pedido(url, off, off + sz - 1) as r:
        cd = r.read()
    ents = []
    i = 0
    while cd[i:i + 4] == b'PK\x01\x02':
        (_, _, _, flag, meth, _, _, crc, cs, us, nl, el, cl, _, _, _, lo) = struct.unpack('<IHHHHHHIIIHHHHHII', cd[i:i + 46])
        nome = cd[i + 46:i + 46 + nl].decode('latin1')
        extra = cd[i + 46 + nl:i + 46 + nl + el]
        if 0xFFFFFFFF in (cs, us, lo):  # campos zip64
            k = 0
            while k + 4 <= len(extra):
                hid, hsz = struct.unpack('<HH', extra[k:k + 4])
                if hid == 1:
                    d = extra[k + 4:k + 4 + hsz]
                    q = 0
                    if us == 0xFFFFFFFF:
                        us = struct.unpack('<Q', d[q:q + 8])[0]; q += 8
                    if cs == 0xFFFFFFFF:
                        cs = struct.unpack('<Q', d[q:q + 8])[0]; q += 8
                    if lo == 0xFFFFFFFF:
                        lo = struct.unpack('<Q', d[q:q + 8])[0]; q += 8
                k += 4 + hsz
        ents.append({'nome': nome, 'flag': flag, 'meth': meth, 'crc': crc, 'cs': cs, 'us': us, 'off': lo})
        i += 46 + nl + el + cl
    if len(ents) != n:
        raise RuntimeError(f'diretório central incompleto: {len(ents)} de {n}')
    ents.sort(key=lambda e: e['off'])
    return tam, cab, ents


class Fluxo:
    """Leitura sequencial de uma URL, retomando por faixa quando a conexão cai."""

    def __init__(self, url, pos, tam):
        self.url, self.pos, self.tam, self.resp, self.quedas, self.pedidos = url, pos, tam, None, 0, 0

    def _abre(self):
        self.resp = _pedido(self.url, self.pos)
        self.pedidos += 1
        if self.resp.status != 206:
            raise RuntimeError(f'resposta {self.resp.status} em pedido de faixa')

    def ler(self, n, guarda=True):
        partes = []
        falta = n
        while falta:
            try:
                if self.resp is None:
                    self._abre()
                b = self.resp.read(min(falta, 1 << 20))
                if not b:
                    raise IOError('conexão fechada antes do fim')
            except urllib.error.HTTPError as e:
                if e.code == 429:
                    raise RuntimeError('429: parei, como manda a regra')
                self._queda(e)
                continue
            except RuntimeError:
                raise
            except Exception as e:
                self._queda(e)
                continue
            if guarda:
                partes.append(b)
            falta -= len(b)
            self.pos += len(b)
        return b''.join(partes)

    def _queda(self, e):
        self.quedas += 1
        try:
            if self.resp is not None:
                self.resp.close()
        except Exception:
            pass
        self.resp = None
        if self.quedas > 40:
            raise RuntimeError(f'quedas demais: {e!r}')
        P(f'  queda {self.quedas} em {self.pos}: {e!r}; retomo')
        time.sleep(min(60, 5 * self.quedas))

    def fecha(self):
        try:
            if self.resp is not None:
                self.resp.close()
        except Exception:
            pass


def _tipo_do_nome(nome):
    # 2026: o03220ac0101500020088-rdv.dat; 2022: o00406-2785500020201.rdv
    base = nome.split('/')[-1]
    if base.endswith(('.dat', '.jez', '.vsc')) and '-' in base:
        return base.rsplit('-', 1)[-1]
    return base.rsplit('.', 1)[-1]


def baixar(ano, turno, uf):
    url = URL.format(ano=ano, turno=turno, uf=uf)
    os.makedirs(TRAB + '/pacotes', exist_ok=True)
    dest = f'{TRAB}/pacotes/rdv_bu_{ano}_{turno}_{uf}.zip'
    man = f'{TRAB}/pacotes/rdv_bu_{ano}_{turno}_{uf}.manifesto.json'
    if os.path.exists(dest) and os.path.exists(man):
        P('já existe', dest)
        return
    t0 = time.time()
    tam, cab, ents = _indice(url)
    quer = [e for e in ents if e['nome'].endswith(('-rdv.dat', '-bu.dat', '.rdv', '.bu'))]
    tipos = collections.Counter(_tipo_do_nome(e['nome']) for e in ents)
    P(f'{ano} {turno} {uf}: {tam} bytes, {len(ents)} membros, {dict(tipos)}; quero {len(quer)}')
    if any(e['flag'] & 8 for e in quer) or any(e['meth'] not in (0, 8) for e in quer):
        raise RuntimeError('membro com descritor de dados ou método não previsto')
    fl = Fluxo(url, quer[0]['off'], tam)
    time.sleep(1)
    n = 0
    with zipfile.ZipFile(dest + '.parcial', 'w', zipfile.ZIP_DEFLATED, compresslevel=6) as zo:
        for e in quer:
            if fl.pos < e['off']:
                fl.ler(e['off'] - fl.pos, guarda=False)
            if fl.pos != e['off']:
                raise RuntimeError('posição fora de ordem')
            h = fl.ler(30)
            if h[:4] != b'PK\x03\x04':
                raise RuntimeError('cabeçalho local inválido em ' + e['nome'])
            nl, el = struct.unpack('<HH', h[26:30])
            nome = fl.ler(nl + el)[:nl].decode('latin1')
            if nome != e['nome']:
                raise RuntimeError('nome local diferente do índice')
            dado = fl.ler(e['cs'])
            cru = zlib.decompress(dado, -15) if e['meth'] == 8 else dado
            if (zlib.crc32(cru) & 0xFFFFFFFF) != e['crc'] or len(cru) != e['us']:
                raise RuntimeError('CRC ou tamanho não confere em ' + e['nome'])
            zo.writestr(nome, cru)
            n += 1
            if n % 1000 == 0:
                dt = time.time() - t0
                P(f'  {n}/{len(quer)} membros, {fl.pos / 1e6:.0f} MB lidos, {fl.pos / 1e6 / dt:.1f} MB/s, quedas {fl.quedas}')
    fl.fecha()
    os.replace(dest + '.parcial', dest)
    grava(f'pacotes/rdv_bu_{ano}_{turno}_{uf}.manifesto.json',
          {'url': url, 'cabecalhos': cab, 'tamanho_pacote': tam, 'membros_no_pacote': len(ents), 'tipos_no_pacote': dict(tipos),
           'guardados': n, 'bytes_lidos': fl.pos, 'pedidos_de_fluxo': fl.pedidos, 'quedas': fl.quedas,
           'segundos': round(time.time() - t0, 1), 'lido_em_utc': time.strftime('%Y-%m-%d %H:%M:%S', time.gmtime()),
           'tamanho_guardado': os.path.getsize(dest)})
    P(f'pronto {dest}: {n} membros, {os.path.getsize(dest) / 1e6:.1f} MB em disco, {time.time() - t0:.0f} s')


# ---------------------------------------------------------------- leitura do RDV e do boletim (sem resultado)
def _int(v):
    return int.from_bytes(v, 'big', signed=False)


def _f(no):
    return no[2] if isinstance(no[2], list) else []


def ler_rdv_bytes(b):
    """Devolve (mun, zona, local, secao) do cabeçalho e a contagem por (eleição, cargo, tipo, dígitos)."""
    top = parse(b)[0][2]
    rdv = top[2][2]
    ident = None
    for n in rdv:
        f = _f(n)
        if (n[0], n[1]) == (0, 16) and len(f) == 3 and (f[0][0], f[0][1]) == (0, 16) and all((c[0], c[1]) == (0, 2) for c in f[1:]):
            mz = _f(f[0])
            ident = (_int(mz[0][2]), _int(mz[1][2]), _int(f[1][2]), _int(f[2][2]))
    # 2026: as eleições vêm no nó [2:1]; 2022: no nó [2:0]. O resto da estrutura é igual.
    els = ([n for n in rdv if (n[0], n[1]) == (2, 1)] or [n for n in rdv if (n[0], n[1]) == (2, 0)])[0][2]
    out = collections.Counter()
    for el in els:
        f = _f(el)
        ide = _int(f[0][2])
        for cargo in _f(f[1]):
            h = _f(cargo)
            cod = _int(h[0][2])
            for voto in _f(h[2]):
                e = _f(voto)
                tipo = _int(e[0][2])
                dig = e[1][2].decode() if len(e) > 1 else ''
                out[(ide, cod, tipo, dig)] += 1
    return ident, out


def _resumo_rdv(c):
    """Presidente (cargo 1) e governador (cargo 3) no formato de trabalho."""
    r = {'pn': collections.Counter(), 'pB': 0, 'pN': 0, 'pd': collections.Counter(), 'p6': 0,
         'gn': collections.Counter(), 'gB': 0, 'gN': 0, 'gd': collections.Counter(), 'g6': 0, 'outros': collections.Counter()}
    for (ide, cod, tipo, dig), q in c.items():
        if cod not in (1, 3):
            continue
        x = 'p' if cod == 1 else 'g'
        if tipo == 2:
            r[x + 'n'][str(int(dig))] += q
        elif tipo == 3:
            r[x + 'B'] += q
        elif tipo == 4:
            r[x + 'N'] += q
            r[x + 'd'][dig] += q
        elif tipo == 6:
            r[x + 'N'] += q
            r[x + '6'] += q
        else:
            r['outros'][f'{x}{tipo}'] += q
    return {k: (dict(v) if isinstance(v, collections.Counter) else v) for k, v in r.items()}


def _chave_do_nome(nome, uf=None):
    base = nome.split('/')[-1]
    if base.endswith('.dat'):  # 2026: o{pleito:5}{uf:2}{mun:5}{zona:4}{secao:4}-rdv.dat
        corpo = base.split('-')[0]
        return f'{corpo[6:8].upper()}|{int(corpo[8:13])}|{int(corpo[13:17])}|{int(corpo[17:21])}'
    corpo = base.split('-')[1].split('.')[0]  # 2022: o00406-{mun:5}{zona:4}{secao:4}.rdv
    return f'{uf}|{int(corpo[0:5])}|{int(corpo[5:9])}|{int(corpo[9:13])}'


def extrair(ano):
    import decodificar
    os.makedirs(TRAB + '/extr', exist_ok=True)
    tmp = TRAB + '/extr/_bu_tmp.dat'
    for nome_zip in sorted(os.listdir(TRAB + '/pacotes')):
        if not (nome_zip.endswith('.zip') and f'_{ano}_' in nome_zip):
            continue
        _, _, a, turno, uf = nome_zip[:-4].split('_')
        saida = f'{TRAB}/extr/rdv_{a}_{turno}_{uf}.json.gz'
        if os.path.exists(saida):
            P('já existe', saida)
            continue
        out = {}
        erros = []
        z = zipfile.ZipFile(f'{TRAB}/pacotes/{nome_zip}')
        nomes = z.namelist()
        for n in nomes:
            if not n.endswith(('-rdv.dat', '.rdv')):
                continue
            k = _chave_do_nome(n, uf)
            try:
                ident, c = ler_rdv_bytes(z.read(n))
            except Exception as e:
                erros.append((n, 'rdv: ' + repr(e)))
                continue
            r = _resumo_rdv(c)
            r['ident'] = ident
            m, zn, s = (int(x) for x in k.split('|')[1:])
            if ident is None or (ident[0], ident[1], ident[3]) != (m, zn, s):
                erros.append((n, f'identificação do RDV {ident} difere do nome'))
            r['eleicoes'] = sorted({ide for (ide, cod, tipo, dig) in c})
            if k in out:
                erros.append((n, 'seção repetida no pacote'))
            out[k] = r
        # boletim: presidente e governador, para conferência interna
        for n in nomes:
            if not n.endswith('-bu.dat'):  # o boletim de 2022 (.bu) não é decodificado (R8)
                continue
            k = _chave_do_nome(n, uf)
            try:
                with open(tmp, 'wb') as f:
                    f.write(z.read(n))
                s, g = decodificar.bu_para_secao(decodificar.ler_bu(tmp))
            except Exception as e:
                erros.append((n, 'bu: ' + repr(e)))
                continue
            if k in out:
                out[k]['bu'] = {'p': None if s is None else {x: s[x] for x in ('L', 'R', 'O', 'B', 'N', 'comp', 'apt', 'loc', 'urna')},
                                'g': None if g is None else {x: g[x] for x in ('B', 'N', 'V', 'comp')}}
        if os.path.exists(tmp):
            os.remove(tmp)
        with gzip.open(saida, 'wt') as f:
            json.dump({'secoes': out, 'erros': erros}, f)
        P(f'{nome_zip}: {len(out)} seções com RDV, {sum(1 for v in out.values() if "bu" in v)} com boletim lido, {len(erros)} erros de leitura')
        for e in erros[:10]:
            P('   ', e)


# ---------------------------------------------------------------- conferência (RDV contra bweb) e tabela por seção
def _base(ano):
    with gzip.open(f'{RAIZ}/dados/secoes{ano}.json.gz', 'rt') as f:
        return json.load(f)


def _extr(ano, turno, uf):
    with gzip.open(f'{TRAB}/extr/rdv_{ano}_{turno}_{uf}.json.gz', 'rt') as f:
        return json.load(f)


def _bweb(uf, turno):
    """bweb do TSE, direto do zip: {chave: {'1': {(tipo, numero): votos}, '3': {...}}} (presidente e governador)."""
    pasta, pref = (BWEB1, 'bweb_1t_') if turno == '1' else (BWEB2, 'bweb_2t_')
    zs = sorted(n for n in os.listdir(pasta) if n.startswith(pref + uf + '_') and n.endswith('.zip'))
    if not zs:
        return None, None
    z = zipfile.ZipFile(f'{pasta}/{zs[0]}')
    nome = [n for n in z.namelist() if n.lower().endswith('.csv')][0]
    out = {}
    with z.open(nome) as fh:
        rd = csv.reader(io.TextIOWrapper(fh, encoding='latin1', newline=''), delimiter=';')
        cab = next(rd)
        ix = {c.strip().replace('SG_ UF', 'SG_UF'): i for i, c in enumerate(cab)}
        iC, iU, iM, iZ, iS = ix['CD_CARGO_PERGUNTA'], ix['SG_UF'], ix['CD_MUNICIPIO'], ix['NR_ZONA'], ix['NR_SECAO']
        iT, iN, iQ = ix['CD_TIPO_VOTAVEL'], ix['NR_VOTAVEL'], ix['QT_VOTOS']
        for r in rd:
            c = r[iC]
            if c not in ('1', '3'):
                continue
            k = f'{r[iU]}|{int(r[iM])}|{int(r[iZ])}|{int(r[iS])}'
            d = out.setdefault(k, {'1': collections.Counter(), '3': collections.Counter()})
            d[c][(int(r[iT]), int(r[iN]))] += int(r[iQ])
    return zs[0], out


def _rdv5(r, x):
    n = r[x + 'n']
    return (n.get('13', 0), n.get('22', 0), sum(v for k, v in n.items() if k not in ('13', '22')), r[x + 'B'], r[x + 'N'])


def conferir(ano):
    ufs = UFS if ano == '2026' else ['AL']
    base = _base(ano)
    rel = {'ano': ano, 'ufs': {}}
    tab = {}
    for uf in ufs:
        ru = rel['ufs'][uf] = {}
        ex = {t: _extr(ano, f'{t}t', uf) for t in ('1', '2')}
        falha = collections.defaultdict(list)
        for t in ('1', '2'):
            secs, erros = ex[t]['secoes'], ex[t]['erros']
            bk = [k for k in base if k.startswith(uf + '|') and t in base[k]]
            c = collections.Counter()
            dif = {'pres': [], 'gov': [], 'bu': [], 'bweb_pres': [], 'bweb_gov': []}
            digs = collections.Counter()
            outros = collections.Counter()
            gov_nom_13_22 = 0
            eleicoes = collections.Counter()
            nome_bweb, bw = (_bweb(uf, t) if ano == '2026' else (None, None))
            cand_gov = collections.Counter()
            cand_gov_rdv = collections.Counter()
            if bw is not None:
                for k, d in bw.items():
                    for (tv, nv), q in d['3'].items():
                        if tv not in (2, 3):
                            cand_gov[str(nv)] += q
            for k in bk:
                b = base[k][t]
                r = secs.get(k)
                if r is None:
                    c['sem_rdv'] += 1
                    falha[k].append(f'sem RDV no {t}º turno')
                    continue
                c['com_rdv'] += 1
                eleicoes[tuple(r['eleicoes'])] += 1
                rp, bp = _rdv5(r, 'p'), (b['L'], b['R'], b['O'], b['B'], b['N'])
                if rp == bp:
                    c['pres_igual_base'] += 1
                else:
                    dif['pres'].append([k, list(rp), list(bp)])
                    falha[k].append(f'RDV de presidente difere da base no {t}º turno')
                if sum(rp) == b['comp']:
                    c['total_pres_igual_comparecimento'] += 1
                g = base[k].get(t + 'g')
                if g is not None:
                    rg, bg = (r['gB'], r['gN'], sum(r['gn'].values())), (g['B'], g['N'], g['V'])
                    if rg == bg:
                        c['gov_igual_base'] += 1
                    else:
                        dif['gov'].append([k, list(rg), list(bg)])
                bu = r.get('bu')
                if bu is not None and bu.get('p') is not None:
                    c['com_boletim'] += 1
                    q = bu['p']
                    if (q['L'], q['R'], q['O'], q['B'], q['N'], q['comp'], q['apt'], q['loc']) == (b['L'], b['R'], b['O'], b['B'], b['N'], b['comp'], b['apt'], b['loc']):
                        c['boletim_igual_base'] += 1
                    else:
                        dif['bu'].append(k)
                    if bu.get('g') is not None and (bu['g']['B'], bu['g']['N'], bu['g']['V']) == (r['gB'], r['gN'], sum(r['gn'].values())):
                        c['boletim_gov_igual_rdv'] += 1
                if bw is not None:
                    w = bw.get(k)
                    if w is None:
                        dif['bweb_pres'].append([k, 'sem linha no bweb'])
                    else:
                        for cargo, x in (('1', 'p'), ('3', 'g')):
                            wn = {str(nv): q for (tv, nv), q in w[cargo].items() if tv not in (2, 3) and q}
                            wb = sum(q for (tv, nv), q in w[cargo].items() if tv == 2)
                            wnu = sum(q for (tv, nv), q in w[cargo].items() if tv == 3)
                            rn = {n: q for n, q in r[x + 'n'].items() if q}
                            if (wn, wb, wnu) == (rn, r[x + 'B'], r[x + 'N']):
                                c['bweb_igual_' + ('pres' if x == 'p' else 'gov')] += 1
                            else:
                                dif['bweb_pres' if x == 'p' else 'bweb_gov'].append([k, cargo])
                for dg, q in r['gd'].items():
                    digs[len(dg)] += q
                for o, q in r['outros'].items():
                    outros[o] += q
                gov_nom_13_22 += r['gn'].get('13', 0) + r['gn'].get('22', 0)
                for n, q in r['gn'].items():
                    cand_gov_rdv[n] += q
                c['nulos_gov_com_digitos'] += sum(r['gd'].values())
                c['nulos_gov_sem_digitos'] += r['g6']
                c['brancos_gov'] += r['gB']
                c['nominais_gov'] += sum(r['gn'].values())
            fora = [k for k in secs if k not in base or t not in base[k]]
            ru[t] = {'secoes_na_base': len(bk), 'rdv_no_pacote': len(secs), 'rdv_fora_da_base': len(fora),
                     'erros_de_leitura': len(erros), 'erros_exemplos': erros[:5], 'contagens': dict(c),
                     'diferencas_presidente_rdv_x_base': dif['pres'][:50], 'n_diferencas_presidente': len(dif['pres']),
                     'n_diferencas_governador_rdv_x_base': len(dif['gov']), 'diferencas_governador_exemplos': dif['gov'][:20],
                     'n_boletim_diferente_da_base': len(dif['bu']),
                     'bweb_arquivo': nome_bweb, 'n_diferencas_bweb_presidente': len(dif['bweb_pres']),
                     'n_diferencas_bweb_governador': len(dif['bweb_gov']), 'diferencas_bweb_exemplos': (dif['bweb_pres'] + dif['bweb_gov'])[:20],
                     'candidatos_governador_bweb': sorted(cand_gov, key=int), 'candidatos_governador_rdv': sorted(cand_gov_rdv, key=int),
                     'votos_nominais_de_governador_em_13_ou_22_no_rdv': gov_nom_13_22,
                     'tamanho_dos_digitos_dos_nulos_de_governador': {str(a): b for a, b in sorted(digs.items())},
                     'tipos_de_voto_nao_previstos': dict(outros), 'eleicoes_no_rdv': {str(a): b for a, b in eleicoes.items()}}
            P(f'{ano} {uf} {t}º turno: base {len(bk)}, RDV {len(secs)}, presidente igual à base {c["pres_igual_base"]}, '
              f'governador igual {c["gov_igual_base"]}, boletim igual {c["boletim_igual_base"]} de {c["com_boletim"]}, '
              f'bweb direto presidente {c["bweb_igual_pres"]} governador {c["bweb_igual_gov"]}, erros de leitura {len(erros)}, '
              f'nominal de governador em 13 ou 22: {gov_nom_13_22}, candidatos a governador {sorted(cand_gov or cand_gov_rdv, key=int)}')
        # tabela por seção
        for k in base:
            if not k.startswith(uf + '|') or '1' not in base[k] or '2' not in base[k]:
                continue
            r1, r2 = ex['1']['secoes'].get(k), ex['2']['secoes'].get(k)
            b1, b2 = base[k]['1'], base[k]['2']
            _, mun, zona, sec = k.split('|')
            row = {'uf': uf, 'mun': int(mun), 'zona': int(zona), 'loc': b2['loc'], 'L1': b1['L'], 'R1': b1['R'], 'O1': b1['O'],
                   'L2': b2['L'], 'R2': b2['R'], 'comp1': b1['comp'], 'comp2': b2['comp'], 'apt2': b2['apt'],
                   'tem_rdv': r1 is not None and r2 is not None, 'ok': k not in falha, 'motivo': falha.get(k, [])}
            if row['tem_rdv']:
                row.update({'gd1': r1['gd'], 'gd2': r2['gd'], 'gn1': r1['gn'], 'gn2': r2['gn'], 'g6_1': r1['g6'], 'g6_2': r2['g6'],
                            'gB1': r1['gB'], 'gB2': r2['gB'], 'gN1': r1['gN'], 'gN2': r2['gN']})
            tab[k] = row
        ru['universo'] = {'secoes_nos_dois_turnos_da_base': sum(1 for k, v in tab.items() if v['uf'] == uf),
                          'no_universo_D2': sum(1 for k, v in tab.items() if v['uf'] == uf and v['ok']),
                          'fora': {k: v['motivo'] for k, v in tab.items() if v['uf'] == uf and not v['ok']}}
        P(f'  universo {uf}: {ru["universo"]["no_universo_D2"]} de {ru["universo"]["secoes_nos_dois_turnos_da_base"]}')
    with gzip.open(f'{TRAB}/tabela_{ano}.json.gz', 'wt') as f:
        json.dump(tab, f)
    grava(f'conferencia_{ano}.json', rel)


# ---------------------------------------------------------------- contas
import numpy as np  # noqa: E402

COLS = ['L1', 'R1', 'L2', 'R2', 'a1', 'b1', 'a2', 'b2']


def _carrega(ano, todas=False):
    with gzip.open(f'{TRAB}/tabela_{ano}.json.gz', 'rt') as f:
        tab = json.load(f)
    ks = sorted(k for k, v in tab.items() if (v['ok'] or (todas and v['tem_rdv'])))
    n = len(ks)
    X = np.zeros((n, 8))
    locs, loc = {}, np.zeros(n, int)
    uf = np.empty(n, dtype=object)
    mun = np.empty(n, dtype=object)
    for i, k in enumerate(ks):
        v = tab[k]
        X[i] = (v['L1'], v['R1'], v['L2'], v['R2'], v['gd1'].get('13', 0), v['gd1'].get('22', 0), v['gd2'].get('13', 0), v['gd2'].get('22', 0))
        lk = f"{v['uf']}|{v['mun']}|{v['zona']}|{v['loc']}"
        loc[i] = locs.setdefault(lk, len(locs))
        uf[i] = v['uf']
        mun[i] = f"{v['uf']}|{v['mun']}"
    uf_loc = np.empty(len(locs), dtype=object)
    for lk, j in locs.items():
        uf_loc[j] = lk.split('|')[0]
    return {'k': ks, 'tab': tab, 'X': X, 'loc': loc, 'nloc': len(locs), 'uf': uf, 'mun': mun, 'uf_loc': uf_loc}


def _contagens_boot(uf_loc, nboot=NBOOT, semente=SEMENTE):
    """Multiplicidade de cada local em cada réplica; sorteio com reposição dentro da UF (D5)."""
    rng = np.random.default_rng(semente)
    C = np.zeros((nboot, len(uf_loc)), dtype=np.float64)
    for u in sorted(set(uf_loc)):
        idx = np.flatnonzero(uf_loc == u)
        dr = rng.integers(0, len(idx), size=(nboot, len(idx)))
        for b in range(nboot):
            C[b, idx] = np.bincount(dr[b], minlength=len(idx))
    return C


def _theta(S):
    with np.errstate(divide='ignore', invalid='ignore'):
        return (np.log(S[..., 2] / S[..., 3]) - np.log(S[..., 0] / S[..., 1])) - (np.log(S[..., 6] / S[..., 7]) - np.log(S[..., 4] / S[..., 5]))


def _agrega(X, loc, nloc, mask=None):
    M = np.zeros((nloc, X.shape[1]))
    if mask is None:
        np.add.at(M, loc, X)
    else:
        np.add.at(M, loc[mask], X[mask])
    return M


def _conta(X, loc, nloc, C, mask=None):
    """Theta, erro-padrão por bootstrap de locais e as somas. Devolve também as réplicas."""
    Xs = X if mask is None else X[mask]
    S = Xs.sum(0)
    rep = _theta(C @ _agrega(X, loc, nloc, mask))
    ok = np.isfinite(rep)
    th = float(_theta(S))
    r = {'n_secoes': int(len(Xs)), 'n_locais': int(len(set((loc if mask is None else loc[mask]).tolist()))),
         'theta': th, 'ep': float(rep[ok].std(ddof=1)) if ok.sum() > 1 else float('nan'),
         'ic95_percentis': [float(np.percentile(rep[ok], 2.5)), float(np.percentile(rep[ok], 97.5))] if ok.sum() > 1 else None,
         'replicas_fora': int((~ok).sum()), 'somas': {c: int(v) for c, v in zip(COLS, S)},
         'P1': float(S[0] / (S[0] + S[1])), 'P2': float(S[2] / (S[2] + S[3])),
         'W1': float(S[4] / (S[4] + S[5])) if S[4] + S[5] else None, 'W2': float(S[6] / (S[6] + S[7])) if S[6] + S[7] else None,
         'dlogit_P': float(np.log(S[2] / S[3]) - np.log(S[0] / S[1])),
         'dlogit_W': float(np.log(S[6] / S[7]) - np.log(S[4] / S[5])) if min(S[4:8]) > 0 else None}
    return r, rep


def _postos(x):
    from scipy.stats import rankdata
    return rankdata(np.asarray(x, float), method='average', axis=-1)


def _spearman(x, y):
    x, y = np.asarray(x, float), np.asarray(y, float)
    if len(x) < 3:
        return None
    rx, ry = _postos(x), _postos(y)
    if rx.std() == 0 or ry.std() == 0:
        return None
    return float(np.corrcoef(rx, ry)[0, 1])


def _spearman_linhas(Wsim, p):
    """Spearman de cada linha de Wsim contra o vetor p."""
    R = _postos(Wsim)
    rp = _postos(p)
    R = R - R.mean(1, keepdims=True)
    rp = rp - rp.mean()
    den = np.sqrt((R ** 2).sum(1) * (rp ** 2).sum())
    with np.errstate(divide='ignore', invalid='ignore'):
        return (R @ rp) / den


def etapa1():
    """Só o número de testemunhas por turno e o erro-padrão. Não imprime nem grava Theta (D6)."""
    d = _carrega('2026')
    X, loc, nloc = d['X'], d['loc'], d['nloc']
    C = _contagens_boot(d['uf_loc'])
    out = {'aviso': 'etapa 1: só número de testemunhas (13 + 22 somados) por turno e erro-padrão; Theta não foi impresso nem gravado',
           'bootstrap': {'unidade': 'local de votação', 'replicas': NBOOT, 'semente': SEMENTE, 'estratos': 'UF'},
           'recortes': {}}
    for nome, mask in [('AC+TO', None)] + [(u, d['uf'] == u) for u in UFS]:
        r, rep = _conta(X, loc, nloc, C, mask)
        Xs = X if mask is None else X[mask]
        t1, t2 = Xs[:, 4] + Xs[:, 5], Xs[:, 6] + Xs[:, 7]
        comp1 = sum(d['tab'][k]['comp1'] for k, m in zip(d['k'], (np.ones(len(X), bool) if mask is None else mask)) if m)
        comp2 = sum(d['tab'][k]['comp2'] for k, m in zip(d['k'], (np.ones(len(X), bool) if mask is None else mask)) if m)
        out['recortes'][nome] = {'n_secoes': r['n_secoes'], 'n_locais': r['n_locais'],
                                 'testemunhas_1t': int(t1.sum()), 'testemunhas_2t': int(t2.sum()),
                                 'secoes_com_testemunha_1t': int((t1 > 0).sum()), 'secoes_com_testemunha_2t': int((t2 > 0).sum()),
                                 'comparecimento_1t': int(comp1), 'comparecimento_2t': int(comp2),
                                 'testemunhas_por_100_votantes_1t': float(100 * t1.sum() / comp1), 'testemunhas_por_100_votantes_2t': float(100 * t2.sum() / comp2),
                                 'erro_padrao_de_theta': r['ep'], 'replicas_fora': r['replicas_fora']}
        P(f'{nome}: {r["n_secoes"]} seções, {r["n_locais"]} locais; testemunhas (13 + 22) 1º turno {int(t1.sum())}, 2º turno {int(t2.sum())}; '
          f'erro-padrão de Theta {r["ep"]:.4f} (réplicas fora {r["replicas_fora"]})')
    ep = out['recortes']['AC+TO']['erro_padrao_de_theta']
    out['limite_do_registro'] = 0.025
    out['veredito_da_etapa1'] = 'SEM PODER' if not (ep <= 0.025) else 'segue para a validade do termômetro'
    out['erro_total_com_sistematico_minimo_0015'] = float(math.hypot(ep, 0.015))
    out['gravado_em_utc'] = time.strftime('%Y-%m-%d %H:%M:%S', time.gmtime())
    P('etapa 1:', out['veredito_da_etapa1'], '| erro total com sistemático mínimo de 0,015:', round(out['erro_total_com_sistematico_minimo_0015'], 4))
    grava('etapa1.json', out)


def _votos_1t_por_candidato(ks):
    with gzip.open(f'{RAIZ}/dados/candidatos2026_1t.json.gz', 'rt') as f:
        c = json.load(f)['secoes']
    return [c.get(k, {}) for k in ks]


def _validade_conta(mun, n_m, g13_m, P_m, rotulo, rng):
    """Regra do D7 sobre vetores por município (n_m = testemunhas 13 + 22, g13_m, P_m oficial)."""
    grade = [1, 50, 100, 200, 400, 800]
    out = {'rotulo': rotulo, 'municipios': int(len(n_m)), 'municipios_com_testemunha': int((n_m > 0).sum()), 'grade': []}
    escolhido = None
    for g in grade:
        sel = n_m >= g
        item = {'n_min': g, 'municipios': int(sel.sum())}
        if sel.sum() >= 10:
            sim = rng.binomial(n_m[sel].astype(int), P_m[sel], size=(2000, int(sel.sum()))) / n_m[sel]
            rho = _spearman_linhas(sim, P_m[sel])
            rho = rho[np.isfinite(rho)]
            item.update({'termometro_perfeito_fracao_acima_de_09': float((rho >= 0.9).mean()), 'termometro_perfeito_mediana': float(np.median(rho)),
                         'termometro_perfeito_p5': float(np.percentile(rho, 5))})
            item['observado'] = _spearman(g13_m[sel] / n_m[sel], P_m[sel])
            if escolhido is None and item['termometro_perfeito_fracao_acima_de_09'] >= 0.95:
                escolhido = g
        out['grade'].append(item)
    out['n_min_escolhido'] = escolhido
    if escolhido is not None:
        it = [x for x in out['grade'] if x['n_min'] == escolhido][0]
        out['regra'] = f'municípios com pelo menos {escolhido} testemunhas; limiar 0,9'
        out['correlacao_que_decide'] = it['observado']
        out['municipios_na_decisao'] = it['municipios']
        out['aprovado'] = bool(it['observado'] is not None and it['observado'] >= 0.9)
    else:
        it = out['grade'][0]
        out['regra'] = 'nenhum valor da grade serve; decide por compatibilidade com o termômetro perfeito (percentil 5), desvio maior'
        out['correlacao_que_decide'] = it.get('observado')
        out['municipios_na_decisao'] = it['municipios']
        out['aprovado'] = bool(it.get('observado') is not None and it['observado'] >= it['termometro_perfeito_p5'])
    it1 = out['grade'][0]
    out['leitura_sem_minimo'] = {'observado': it1.get('observado'), 'municipios': it1['municipios'],
                                 'teto_de_ruido_mediana': it1.get('termometro_perfeito_mediana'), 'teto_de_ruido_p5': it1.get('termometro_perfeito_p5'),
                                 'aprovaria_pelo_limiar_09': bool(it1.get('observado') is not None and it1['observado'] >= 0.9)}
    return out


def validade():
    """Termômetro no 1º turno (D7). Só usa dado do 1º turno."""
    if not os.path.exists(f'{TRAB}/etapa1.json'):
        raise SystemExit('rode etapa1 antes')
    d = _carrega('2026')
    ks, tab, X = d['k'], d['tab'], d['X']
    v1 = _votos_1t_por_candidato(ks)
    nums_todos = sorted(set(['13', '22'] + ELIM['AC'] + ELIM['TO']), key=int)
    W = {n: np.array([tab[k]['gd1'].get(n, 0) for k in ks], float) for n in nums_todos}   # testemunhas por número, 1º turno
    V = {n: np.array([v.get(n, 0) for v in v1], float) for n in nums_todos}               # votos oficiais por número, 1º turno
    confere = {'L1_igual_candidatos': bool((V['13'] == X[:, 0]).all()), 'R1_igual_candidatos': bool((V['22'] == X[:, 1]).all())}
    muns = sorted(set(d['mun']))
    im = {m: i for i, m in enumerate(muns)}
    idx = np.array([im[m] for m in d['mun']])
    ufm = np.array([m.split('|')[0] for m in muns], dtype=object)

    def pm(a):
        return np.bincount(idx, weights=a, minlength=len(muns))
    Wm = {n: pm(W[n]) for n in nums_todos}
    Vm = {n: pm(V[n]) for n in nums_todos}
    n_m = Wm['13'] + Wm['22']
    P_m = Vm['13'] / (Vm['13'] + Vm['22'])
    rng = np.random.default_rng(SEMENTE)
    out = {'confere_base_x_candidatos': confere, 'limiar_do_registro': 0.9}
    out['principal_AC_TO'] = _validade_conta(muns, n_m, Wm['13'], P_m, 'AC e TO juntos', rng)
    out['por_uf'] = {}
    for u in UFS:
        s = ufm == u
        out['por_uf'][u] = _validade_conta([m for m in muns if m.startswith(u)], n_m[s], Wm['13'][s], P_m[s], u, rng)
    # composição por número no agregado da UF, células e correlações com os eliminados no denominador
    out['composicao_por_uf'] = {}
    cel_w, cel_v, cel_num = [], [], []
    for u in UFS:
        s = ufm == u
        nums = ['13', '22'] + ELIM[u]
        tw = sum(Wm[n][s].sum() for n in nums)
        tv = sum(Vm[n][s].sum() for n in nums)
        out['composicao_por_uf'][u] = {n: {'testemunhas': int(Wm[n][s].sum()), 'parcela_entre_testemunhas': float(Wm[n][s].sum() / tw),
                                           'votos_oficiais': int(Vm[n][s].sum()), 'parcela_oficial': float(Vm[n][s].sum() / tv)} for n in nums}
        out['composicao_por_uf'][u]['_postos_entre_numeros'] = _spearman([Wm[n][s].sum() / tw for n in nums], [Vm[n][s].sum() / tv for n in nums])
        twm = sum(Wm[n] for n in nums)
        tvm = sum(Vm[n] for n in nums)
        for n in nums:
            ok = s & (twm > 0)
            cel_w += list(Wm[n][ok] / twm[ok])
            cel_v += list(Vm[n][ok] / tvm[ok])
            cel_num += [n] * int(ok.sum())
    cel_w, cel_v, cel_num = np.array(cel_w), np.array(cel_v), np.array(cel_num)
    out['celulas_municipio_x_numero'] = {'n_celulas': int(len(cel_w)), 'spearman': _spearman(cel_w, cel_v), 'pearson': float(np.corrcoef(cel_w, cel_v)[0, 1]),
                                         'por_numero': {n: {'n': int((cel_num == n).sum()), 'spearman': _spearman(cel_w[cel_num == n], cel_v[cel_num == n])}
                                                        for n in nums_todos}}
    # parcelas de 13 e de 22 com os eliminados no denominador, por município (AC e TO juntos; denominador da própria UF)
    den_w = np.zeros(len(muns))
    den_v = np.zeros(len(muns))
    for u in UFS:
        s = ufm == u
        for n in ['13', '22'] + ELIM[u]:
            den_w[s] += Wm[n][s]
            den_v[s] += Vm[n][s]
    ok = den_w > 0
    out['parcelas_com_eliminados_no_denominador'] = {
        'municipios': int(ok.sum()),
        'parcela_13': _spearman(Wm['13'][ok] / den_w[ok], Vm['13'][ok] / den_v[ok]),
        'parcela_22': _spearman(Wm['22'][ok] / den_w[ok], Vm['22'][ok] / den_v[ok]),
        'parcela_eliminados': _spearman(1 - (Wm['13'][ok] + Wm['22'][ok]) / den_w[ok], 1 - (Vm['13'][ok] + Vm['22'][ok]) / den_v[ok])}
    # nível: W_1 contra P_1 no agregado (o termômetro não precisa acertar o nível, só acompanhar)
    out['nivel_1t'] = {u: {'W1': float(Wm['13'][ufm == u].sum() / n_m[ufm == u].sum()), 'P1': float(Vm['13'][ufm == u].sum() / (Vm['13'][ufm == u].sum() + Vm['22'][ufm == u].sum())),
                           'testemunhas_13_22': int(n_m[ufm == u].sum()), 'testemunhas_eliminados': int(sum(Wm[n][ufm == u].sum() for n in ELIM[u]))} for u in UFS}
    out['por_municipio'] = [{'mun': m, 'testemunhas_13_22': int(n_m[i]), 'W1': (float(Wm['13'][i] / n_m[i]) if n_m[i] else None), 'P1': float(P_m[i])} for i, m in enumerate(muns)]
    out['aprovado'] = out['principal_AC_TO']['aprovado']
    out['gravado_em_utc'] = time.strftime('%Y-%m-%d %H:%M:%S', time.gmtime())
    pr = out['principal_AC_TO']
    P(f'validade (D7): n_min {pr["n_min_escolhido"]}, municípios na decisão {pr["municipios_na_decisao"]}, correlação de postos {pr["correlacao_que_decide"]}, '
      f'aprovado: {pr["aprovado"]}')
    P('  grade:', json.dumps(pr['grade']))
    P('  leitura sem mínimo:', json.dumps(pr['leitura_sem_minimo']))
    for u in UFS:
        q = out['por_uf'][u]
        P(f'  {u}: n_min {q["n_min_escolhido"]}, decide {q["correlacao_que_decide"]} em {q["municipios_na_decisao"]} municípios, sem mínimo {q["leitura_sem_minimo"]["observado"]}')
    P('  células:', out['celulas_municipio_x_numero']['n_celulas'], out['celulas_municipio_x_numero']['spearman'], '| com eliminados no denominador:', out['parcelas_com_eliminados_no_denominador'])
    P('  nível 1º turno:', out['nivel_1t'])
    grava('validade.json', out)


def _perfil():
    """Eleitores por grau de escolaridade (códigos 1 a 8; 0 = não informado) por seção de AC e TO."""
    if os.path.exists(f'{TRAB}/perfil_escolaridade.json'):
        return le('perfil_escolaridade.json')
    out = {}
    for uf in UFS:
        z = zipfile.ZipFile(f'{PERFIL_DIR}/perfil_eleitor_secao_2026_{uf}.zip')
        nome = [n for n in z.namelist() if n.lower().endswith('.csv')][0]
        with z.open(nome) as fh:
            rd = csv.reader(io.TextIOWrapper(fh, encoding='latin1', newline=''), delimiter=';')
            cab = next(rd)
            ix = {c.strip(): i for i, c in enumerate(cab)}
            iU, iM, iZ, iS, iE, iQ = (ix[c] for c in ('SG_UF', 'CD_MUNICIPIO', 'NR_ZONA', 'NR_SECAO', 'CD_GRAU_ESCOLARIDADE', 'QT_ELEITORES'))
            for r in rd:
                k = f'{r[iU]}|{int(r[iM])}|{int(r[iZ])}|{int(r[iS])}'
                e = int(r[iE])
                dd = out.setdefault(k, [0] * 9)
                dd[e if 1 <= e <= 8 else 0] += int(r[iQ])
    grava('perfil_escolaridade.json', out)
    return out


def _tercis(valores):
    """Três grupos com o mesmo número de seções; 0 = menores valores, 2 = maiores. Empate desfeito pela chave."""
    ks = sorted(valores, key=lambda k: (valores[k], k))
    n = len(ks)
    return {k: min(2, i * 3 // n) for i, k in enumerate(ks)}


def _mascaras_tercil(ks, grupos, nomes):
    return {nomes[g]: np.array([grupos.get(k) == g for k in ks]) for g in sorted(nomes, reverse=True)}


def _bateria(X, d, C, masc_terc):
    """Theta principal com erro, e Theta por UF e por tercil (para os critérios de sinal)."""
    r, _ = _conta(X, d['loc'], d['nloc'], C)
    b = {'theta': r['theta'], 'ep': r['ep'], 'por_uf': {}, 'por_tercil': {}}
    for u in sorted(set(d['uf'])):
        b['por_uf'][u] = float(_theta(X[d['uf'] == u].sum(0)))
    for nome, m in (masc_terc or {}).items():
        b['por_tercil'][nome] = float(_theta(X[m].sum(0)))
    return b


def _criterio_sinal(b, sis, espelho=False):
    """Critério de SINAL do registro aplicado a uma bateria (ou ao espelho: a mesma regra em -Theta)."""
    sg = -1.0 if espelho else 1.0
    th = sg * b['theta']
    err = math.hypot(b['ep'], sis)
    partes = [sg * v for v in list(b['por_uf'].values()) + list(b['por_tercil'].values())]
    c = {'theta': th, 'erro_total': err, 'theta_sobre_erro_total': th / err, 'tamanho_ok': bool(th >= 0.045), 'razao_ok': bool(th >= 2.5 * err),
         'mesmo_sinal_ufs_e_tercis': bool(all(v > 0 for v in partes)), 'n_recortes': len(partes)}
    c['sinal'] = bool(c['tamanho_ok'] and c['razao_ok'] and c['mesmo_sinal_ufs_e_tercis'])
    return c


def _traduz(theta, P2, R2u, L2u):
    """D17: fração dos votos verdadeiros de um lado contada para o outro, e o que isso seria no país."""
    lg = math.log(P2 / (1 - P2))
    Pv = 1 / (1 + math.exp(-(lg - theta)))
    if theta >= 0:
        p = (P2 - Pv) / (1 - Pv)          # fração dos votos verdadeiros de Flávio contada para Lula
        x = p / (1 - p) * R2_OFICIAL
        xl = p / (1 - p) * R2u
        return {'theta': theta, 'P2_oficial': P2, 'P2_verdadeiro_implicito': Pv, 'sentido': 'de Flávio para Lula', 'fracao_p': p,
                'votos_trocados_no_pais_se_uniforme': x, 'efeito_na_margem_no_pais': 2 * x, 'fracao_da_margem': 2 * x / MARGEM,
                'votos_trocados_em_AC_e_TO': xl}
    q = (Pv - P2) / Pv                    # fração dos votos verdadeiros de Lula contada para Flávio
    x = q / (1 - q) * L2_OFICIAL
    xl = q / (1 - q) * L2u
    return {'theta': theta, 'P2_oficial': P2, 'P2_verdadeiro_implicito': Pv, 'sentido': 'de Lula para Flávio', 'fracao_p': -q,
            'votos_trocados_no_pais_se_uniforme': -x, 'efeito_na_margem_no_pais': -2 * x, 'fracao_da_margem': -2 * x / MARGEM,
            'votos_trocados_em_AC_e_TO': -xl}


def _taxas(S):
    """D20: taxas de erro de tela por eleitor de cada lado e a decomposição de Theta."""
    L1, R1, L2, R2, a1, b1, a2, b2 = (float(x) for x in S)
    r = {'r13_1t': a1 / L1, 'r22_1t': b1 / R1, 'r13_2t': a2 / L2, 'r22_2t': b2 / R2}
    r['dln_r13'] = math.log(r['r13_2t'] / r['r13_1t'])
    r['dln_r22'] = math.log(r['r22_2t'] / r['r22_1t'])
    r['theta_igual_a_menos_a_diferenca'] = -(r['dln_r13'] - r['dln_r22'])
    r['multiplicador_r13'] = r['r13_2t'] / r['r13_1t']
    r['multiplicador_r22'] = r['r22_2t'] / r['r22_1t']
    return r


def _descritivo_aas():
    """D18 e R6: ES, DF, AM e RN, só com os RDV da amostra aleatória nova. Sem veredito."""
    base = _base('2026')
    out = {}
    for uf in ('ES', 'DF', 'AM', 'RN'):
        acc = {t: collections.Counter() for t in ('1', '2')}
        nsec = 0
        raiz2 = f'{AAS}/t2/{uf.lower()}'
        for dp, _, fs in sorted(os.walk(raiz2)):
            f2 = [f for f in fs if f.endswith('-rdv.dat')]
            if not f2:
                continue
            rel = os.path.relpath(dp, raiz2)
            dp1 = f'{AAS}/t1/{uf.lower()}/{rel}'
            f1 = [f for f in os.listdir(dp1) if f.endswith('-rdv.dat')] if os.path.isdir(dp1) else []
            if not f1:
                continue
            mun, zona, sec = (int(x) for x in rel.split('/'))
            k = f'{uf}|{mun}|{zona}|{sec}'
            if k not in base or '1' not in base[k] or '2' not in base[k]:
                continue
            lidos = {}
            try:
                for t, cam in (('1', f'{dp1}/{f1[0]}'), ('2', f'{dp}/{f2[0]}')):
                    with open(cam, 'rb') as f:
                        lidos[t] = _resumo_rdv(ler_rdv_bytes(f.read())[1])
            except Exception:
                continue
            ok = all(_rdv5(lidos[t], 'p') == (base[k][t]['L'], base[k][t]['R'], base[k][t]['O'], base[k][t]['B'], base[k][t]['N']) for t in ('1', '2'))
            if not ok:
                acc['1']['rdv_diferente_da_base'] += 1
                continue
            nsec += 1
            for t in ('1', '2'):
                r, b = lidos[t], base[k][t]
                a = acc[t]
                a['L'] += b['L']; a['R'] += b['R']; a['comp'] += b['comp']
                a['g13'] += r['gd'].get('13', 0); a['g22'] += r['gd'].get('22', 0)
                a['nominal_gov_13'] += r['gn'].get('13', 0); a['nominal_gov_22'] += r['gn'].get('22', 0)
                a['nulos_gov_com_digitos'] += sum(r['gd'].values()); a['nominais_gov'] += sum(r['gn'].values())
        ou = out[uf] = {'secoes': nsec, 'rdv_diferente_da_base': acc['1']['rdv_diferente_da_base']}
        for t in ('1', '2'):
            a = acc[t]
            q = {'L': a['L'], 'R': a['R'], 'comparecimento': a['comp'], 'nominal_gov_13': a['nominal_gov_13'], 'nominal_gov_22': a['nominal_gov_22'],
                 'nulos_gov_com_digitos': a['nulos_gov_com_digitos']}
            for n, lado in (('13', 'L'), ('22', 'R')):
                if a['nominal_gov_' + n] == 0 and a['nominais_gov'] > 0:
                    q['g' + n] = a['g' + n]
                    q[f'g{n}_por_mil_votos_de_{lado}'] = 1000 * a['g' + n] / a[lado] if a[lado] else None
                else:
                    q['g' + n] = None  # o número é candidato a governador nessa UF e turno (ou não houve eleição de governador)
            if q.get('g13') is not None and q.get('g22') is not None and q['g13'] + q['g22'] > 0:
                q['W'] = q['g13'] / (q['g13'] + q['g22'])
                q['P'] = a['L'] / (a['L'] + a['R'])
                q['logit_W_menos_logit_P'] = math.log(q['g13'] / q['g22']) - math.log(a['L'] / a['R']) if min(q['g13'], q['g22']) > 0 else None
            ou[f'{t}t'] = q
    return out


def abrir():
    """Segunda etapa: Theta, leituras secundárias, calibração, espelho e tradução em votos."""
    for a in ('etapa1.json', 'validade.json'):
        if not os.path.exists(f'{TRAB}/{a}'):
            raise SystemExit(f'falta {a}: a abertura só roda depois da etapa 1 e da validade')
    d = _carrega('2026')
    X, loc, nloc, ks, tab = d['X'], d['loc'], d['nloc'], d['k'], d['tab']
    n = len(ks)
    C = _contagens_boot(d['uf_loc'])
    out = {'aberto_em_utc': time.strftime('%Y-%m-%d %H:%M:%S', time.gmtime())}
    princ, rep = _conta(X, loc, nloc, C)
    out['principal'] = princ
    out['por_uf'] = {u: _conta(X, loc, nloc, C, d['uf'] == u)[0] for u in UFS}
    # tercis de escolaridade (D8)
    perf = _perfil()
    baixa, sup = {}, {}
    for k in ks:
        q = perf.get(k)
        if q and sum(q[1:9]) > 0:
            baixa[k] = (q[1] + q[2] + q[3]) / sum(q[1:9])
            sup[k] = q[8] / sum(q[1:9])
    g_baixa = _tercis(baixa)                      # 2 = mais eleitores de pouca escolaridade
    g_sup = _tercis({k: -v for k, v in sup.items()})   # 2 = menos eleitores com superior
    nomes = {2: 'baixa', 1: 'media', 0: 'alta'}
    mt = _mascaras_tercil(ks, g_baixa, nomes)
    mts = _mascaras_tercil(ks, g_sup, nomes)
    out['por_tercil_escolaridade'] = {'secoes_com_perfil': len(baixa), 'secoes_sem_perfil': n - len(baixa), 'medida': 'parcela com até fundamental incompleto'}
    for nome, m in mt.items():
        r = _conta(X, loc, nloc, C, m)[0]
        vs = [baixa[k] for k, mm in zip(ks, m) if mm]
        r['faixa_da_medida'] = [min(vs), max(vs)]
        out['por_tercil_escolaridade'][nome] = r
    out['por_tercil_superior_sensibilidade'] = {nome: _conta(X, loc, nloc, C, m)[0] for nome, m in mts.items()}
    bat = _bateria(X, d, C, mt)
    out['bateria'] = bat
    S = X.sum(0)
    L2u, R2u = float(S[2]), float(S[3])

    # D13: intervalo dos eliminados
    e_s = np.array([sum(tab[k]['gd1'].get(nm, 0) for nm in ELIM[tab[k]['uf']]) for k in ks], float)
    a, b_, e = float(S[4]), float(S[5]), float(e_s.sum())
    def desl(cw, c0=0.5):
        return -(math.log((a + cw * e) / (b_ + (1 - cw) * e)) - math.log((a + c0 * e) / (b_ + (1 - c0) * e)))
    out['intervalo_dos_eliminados'] = {'g13_1t': a, 'g22_1t': b_, 'testemunhas_de_eliminados_1t': e, 'parcela_de_eliminados_entre_testemunhas_1t': e / (a + b_ + e),
                                       'por_numero': {u: {nm: int(sum(tab[k]['gd1'].get(nm, 0) for k in ks if tab[k]['uf'] == u)) for nm in ELIM[u]} for u in UFS},
                                       'deslocamento_de_theta': {'cw_0,40': desl(0.4), 'cw_0,25': desl(0.25), 'cw_0,60': desl(0.6), 'cw_0,75': desl(0.75), 'cw_0': desl(0.0), 'cw_1': desl(1.0)},
                                       'nota': 'limite do que uma conversão dos eliminados diferente de 50% entre os que erram a tela deslocaria; não é estimativa'}

    # D11: calibração por efeito plantado (irregularidade) e o espelho do plantio (R4)
    cal = {}
    for lado in ('R_para_L', 'L_para_R'):
        cal[lado] = {}
        for p in (0.018, 0.0357):
            rng = np.random.default_rng(SEMENTE)
            Xp = X.copy()
            if lado == 'R_para_L':
                x = rng.binomial(X[:, 3].astype(int), p)
                Xp[:, 2] += x; Xp[:, 3] -= x
                formula = math.log((1 + p * R2u / L2u) / (1 - p))
            else:
                x = rng.binomial(X[:, 2].astype(int), p)
                Xp[:, 2] -= x; Xp[:, 3] += x
                formula = -math.log((1 + p * L2u / R2u) / (1 - p))
            bp = _bateria(Xp, d, C, mt)
            aum = bp['theta'] - princ['theta']
            varios = []
            for j in range(1, 201):
                rg = np.random.default_rng(SEMENTE + j)
                Xq = X.copy()
                if lado == 'R_para_L':
                    xx = rg.binomial(X[:, 3].astype(int), p); Xq[:, 2] += xx; Xq[:, 3] -= xx
                else:
                    xx = rg.binomial(X[:, 2].astype(int), p); Xq[:, 2] -= xx; Xq[:, 3] += xx
                varios.append(float(_theta(Xq.sum(0))) - princ['theta'])
            err015 = math.hypot(princ['ep'], 0.015)
            item = {'p': p, 'votos_movidos': int(x.sum()), 'formula': formula, 'aumento_de_theta': aum, 'razao_aumento_formula': aum / formula,
                    'aumento_em_erros_totais_com_sis_0015': abs(aum) / err015, 'duzentos_plantios_media': float(np.mean(varios)), 'duzentos_plantios_desvio': float(np.std(varios, ddof=1)),
                    'bateria_com_plantio': bp,
                    'criterio_de_sinal_no_dado_com_plantio_sis_0015': _criterio_sinal(bp, 0.015, espelho=(lado == 'L_para_R'))}
            item['enxerga'] = bool(abs(aum / formula - 1) <= 0.10 and abs(aum) >= 2.5 * err015)
            cal[lado][f'p_{p}'] = item
    out['calibracao_plantio'] = cal
    out['enxerga_o_plantado'] = cal['R_para_L']['p_0.0357']['enxerga']
    err015 = math.hypot(princ['ep'], 0.015)
    alvo = max(0.045, 2.5 * err015)
    lo, hi = 0.0, 0.5
    for _ in range(60):
        mid = (lo + hi) / 2
        if math.log((1 + mid * R2u / L2u) / (1 - mid)) >= alvo:
            hi = mid
        else:
            lo = mid
    out['poder'] = {'erro_total_sis_0015': err015, 'theta_minimo_para_sinal': alvo, 'menor_p_que_alcanca': hi,
                    'menor_p_em_fracao_da_margem_se_uniforme_no_pais': 2 * hi / (1 - hi) * R2_OFICIAL / MARGEM,
                    'formula_p_0357': math.log((1 + 0.0357 * R2u / L2u) / (1 - 0.0357)), 'formula_p_018': math.log((1 + 0.018 * R2u / L2u) / (1 - 0.018)), 'R_sobre_L_2t_universo': R2u / L2u}

    # D12: explicações inocentes plantadas
    k_razao = float((S[6] + S[7]) / (S[4] + S[5]))
    ino = {'k_razao_testemunhas_2t_sobre_1t': k_razao, 'conversao_dos_eliminados': {}, 'queda_geral_da_propensao': {}}
    for delta in (0.10, 0.25):
        incs, movs = [], []
        for j in range(200):
            rg = np.random.default_rng(SEMENTE + 1000 + j)
            mv = np.minimum(rg.binomial(e_s.astype(int), min(1.0, delta * k_razao)), X[:, 6])
            Xq = X.copy(); Xq[:, 6] -= mv; Xq[:, 7] += mv
            incs.append(float(_theta(Xq.sum(0))) - princ['theta']); movs.append(float(mv.sum()))
        m = float(np.mean(movs))
        direto = -(math.log((S[6] - m) / (S[7] + m)) - math.log(S[6] / S[7]))
        ino['conversao_dos_eliminados'][f'delta_{delta}'] = {'testemunhas_movidas_media': m, 'aumento_medio_de_theta': float(np.mean(incs)), 'desvio': float(np.std(incs, ddof=1)),
                                                             'valor_direto': float(direto), 'razao': float(np.mean(incs) / direto), 'formula_do_intervalo_D13': desl(0.5 - delta),
                                                             'passa': bool(abs(np.mean(incs) / direto - 1) <= 0.10)}
    muds = []
    for j in range(200):
        rg = np.random.default_rng(SEMENTE + 2000 + j)
        Xq = X.copy(); Xq[:, 6] = rg.binomial(X[:, 6].astype(int), 0.5); Xq[:, 7] = rg.binomial(X[:, 7].astype(int), 0.5)
        muds.append(float(_theta(Xq.sum(0))) - princ['theta'])
    ino['queda_geral_da_propensao'] = {'mudanca_media_de_theta': float(np.mean(muds)), 'desvio_entre_sorteios': float(np.std(muds, ddof=1)),
                                       'limite_meio_erro_padrao': princ['ep'] / 2, 'passa': bool(abs(np.mean(muds)) <= princ['ep'] / 2)}
    out['explicacao_inocente_plantada'] = ino

    # D14: duas metades
    rng = np.random.default_rng(SEMENTE)
    zs, eps, difs = [], [], []
    for j in range(200):
        perm = rng.permutation(n)
        mA = np.zeros(n, bool); mA[perm[:n // 2]] = True
        dif = float(_theta(X[mA].sum(0)) - _theta(X[~mA].sum(0)))
        if j < 20:
            ra = _theta(C[:400] @ _agrega(X, loc, nloc, mA)); rb = _theta(C[:400] @ _agrega(X, loc, nloc, ~mA))
            eps.append(math.hypot(float(ra[np.isfinite(ra)].std(ddof=1)), float(rb[np.isfinite(rb)].std(ddof=1))))
            er = eps[-1]
        else:
            er = float(np.mean(eps))
        difs.append(dif); zs.append(dif / er)
    zs = np.array(zs)
    out['duas_metades'] = {'divisoes': 200, 'erro_medio_da_diferenca': float(np.mean(eps)), 'desvio_das_diferencas': float(np.std(difs, ddof=1)),
                           'fracao_com_z_acima_de_2': float((np.abs(zs) > 2).mean()), 'maior_z': float(np.abs(zs).max()), 'passa': bool((np.abs(zs) > 2).mean() <= 0.10)}

    # D16: placebo 3 (par de eliminados 70 e 14)
    v1 = _votos_1t_por_candidato(ks)
    n70 = np.array([tab[k]['gd1'].get(PAR_PLACEBO3[0], 0) for k in ks], float); n14 = np.array([tab[k]['gd1'].get(PAR_PLACEBO3[1], 0) for k in ks], float)
    V70 = np.array([v.get(PAR_PLACEBO3[0], 0) for v in v1], float); V14 = np.array([v.get(PAR_PLACEBO3[1], 0) for v in v1], float)
    Q = np.column_stack([n70, n14, V70, V14])
    def est(Sq):
        with np.errstate(divide='ignore', invalid='ignore'):
            return np.log(Sq[..., 0] / Sq[..., 1]) - np.log(Sq[..., 2] / Sq[..., 3])
    pl3 = {'par': list(PAR_PLACEBO3)}
    for nome, m in [('AC+TO', np.ones(n, bool))] + [(u, d['uf'] == u) for u in UFS]:
        rp = est(C @ _agrega(Q, loc, nloc, m)); okk = np.isfinite(rp)
        Sq = Q[m].sum(0)
        pl3[nome] = {'testemunhas_70': int(Sq[0]), 'testemunhas_14': int(Sq[1]), 'votos_70': int(Sq[2]), 'votos_14': int(Sq[3]),
                     'parcela_70_testemunhas': float(Sq[0] / (Sq[0] + Sq[1])) if Sq[0] + Sq[1] else None, 'parcela_70_oficial': float(Sq[2] / (Sq[2] + Sq[3])),
                     'diferenca_de_logits': float(est(Sq)) if min(Sq[0], Sq[1]) > 0 else None, 'ep': float(rp[okk].std(ddof=1)) if okk.sum() > 1 else None, 'replicas_fora': int((~okk).sum())}
    muns = sorted(set(d['mun'])); im = {mm: i for i, mm in enumerate(muns)}; idx = np.array([im[mm] for mm in d['mun']])
    Qm = np.zeros((len(muns), 4)); np.add.at(Qm, idx, Q)
    sel = (Qm[:, 0] + Qm[:, 1]) >= 30
    pl3['por_municipio'] = {'municipios_com_30_ou_mais': int(sel.sum()),
                            'spearman': _spearman(Qm[sel, 0] / (Qm[sel, 0] + Qm[sel, 1]), Qm[sel, 2] / (Qm[sel, 2] + Qm[sel, 3])) if sel.sum() >= 3 else None}
    out['placebo3_par_de_eliminados'] = pl3

    # D19: lado oficial pesado pelas testemunhas
    ns = X[:, 4:8].sum(1)
    okp = ((X[:, 0] + X[:, 1]) > 0) & ((X[:, 2] + X[:, 3]) > 0)
    p1 = np.where(okp, X[:, 0] / np.maximum(X[:, 0] + X[:, 1], 1), 0); p2 = np.where(okp, X[:, 2] / np.maximum(X[:, 2] + X[:, 3], 1), 0)
    Xs = X.copy(); Xs[:, 0] = ns * p1; Xs[:, 1] = ns * (1 - p1); Xs[:, 2] = ns * p2; Xs[:, 3] = ns * (1 - p2)
    r19 = _conta(Xs, loc, nloc, C, okp)[0]
    r19.pop('somas')
    out['oficial_pesado_pelas_testemunhas'] = {'AC+TO': r19, **{u: {kk: vv for kk, vv in _conta(Xs, loc, nloc, C, okp & (d['uf'] == u))[0].items() if kk != 'somas'} for u in UFS}}

    # D20: taxas de erro de tela por lado e a disputa de governador
    out['taxas_de_erro_de_tela'] = {'AC+TO': _taxas(S), **{u: _taxas(X[d['uf'] == u].sum(0)) for u in UFS}}
    fin = {'AC': ('10', '11'), 'TO': ('44', '45')}
    pe = {}
    for k in ks:
        g = tab[k]['gn1']; tot = sum(g.values())
        if tot > 0:
            pe[k] = 1 - sum(g.get(f, 0) for f in fin[tab[k]['uf']]) / tot
    g_pe = _tercis(pe)
    out['por_tercil_da_parcela_de_governador_eliminado'] = {'secoes': len(pe)}
    for nome, m in _mascaras_tercil(ks, g_pe, {2: 'maior', 1: 'media', 0: 'menor'}).items():
        r = _conta(X, loc, nloc, C, m)[0]
        vs = [pe[k] for k, mm in zip(ks, m) if mm]
        r['faixa_da_parcela'] = [min(vs), max(vs)]; r['taxas'] = _taxas(X[m].sum(0))
        out['por_tercil_da_parcela_de_governador_eliminado'][nome] = r
    gov = {}
    for u in UFS:
        mu = [k for k in ks if tab[k]['uf'] == u]
        gov[u] = {}
        for t in ('1', '2'):
            nom = collections.Counter()
            for k in mu:
                for c_, q in tab[k]['gn' + t].items():
                    nom[c_] += q
            dig = collections.Counter()
            for k in mu:
                for c_, q in tab[k]['gd' + t].items():
                    dig[c_] += q
            gov[u][f'{t}t'] = {'nominais_por_candidato': dict(sorted(nom.items(), key=lambda kv: -kv[1])), 'brancos': sum(tab[k]['gB' + t] for k in mu),
                               'nulos': sum(tab[k]['gN' + t] for k in mu), 'nulos_sem_digitos': sum(tab[k]['g6_' + t] for k in mu),
                               'nulos_com_digitos_mais_frequentes': dict(sorted(dig.items(), key=lambda kv: -kv[1])[:15]),
                               'comparecimento': sum(tab[k]['comp' + t] for k in mu)}
    out['governador_descritivo'] = gov

    # R11: Theta por força de Lula no 1º turno
    p1s = {k: X[i, 0] / (X[i, 0] + X[i, 1]) for i, k in enumerate(ks) if X[i, 0] + X[i, 1] > 0}
    mf = _mascaras_tercil(ks, _tercis(p1s), {2: 'lula_forte', 1: 'meio', 0: 'lula_fraco'})
    pf, reps = {}, {}
    for nome, m in mf.items():
        r, rp = _conta(X, loc, nloc, C, m)
        vs = [p1s[k] for k, mm in zip(ks, m) if mm]
        r['faixa_de_P1'] = [min(vs), max(vs)]
        r['R_sobre_L_2t'] = r['somas']['R2'] / r['somas']['L2']
        r['formula_p_0357'] = math.log((1 + 0.0357 * r['R_sobre_L_2t']) / (1 - 0.0357))
        pf[nome] = r; reps[nome] = rp
    dr = reps['lula_fraco'] - reps['lula_forte']
    okd = np.isfinite(dr)
    pf['diferenca_fraco_menos_forte'] = {'observada': pf['lula_fraco']['theta'] - pf['lula_forte']['theta'], 'ep': float(dr[okd].std(ddof=1)),
                                         'prevista_pela_formula_p_0357': pf['lula_fraco']['formula_p_0357'] - pf['lula_forte']['formula_p_0357']}
    out['por_tercil_de_forca_de_lula_1t'] = pf

    # D17: tradução em votos
    out['traducao_em_votos'] = {'ponto': _traduz(princ['theta'], princ['P2'], R2u, L2u)}
    for sis_nome, sis in (('sis_0015', 0.015),):
        err = math.hypot(princ['ep'], sis)
        out['traducao_em_votos'][sis_nome] = {'erro_total': err, 'theta_menos_196_erros': _traduz(princ['theta'] - 1.96 * err, princ['P2'], R2u, L2u),
                                              'theta_mais_196_erros': _traduz(princ['theta'] + 1.96 * err, princ['P2'], R2u, L2u)}
    out['traducao_em_votos']['referencia_troca_que_vira'] = {'p': 0.0357, 'theta_previsto_no_universo': math.log((1 + 0.0357 * R2u / L2u) / (1 - 0.0357)), 'margem': MARGEM}

    # R10: sensibilidade com as seções reprovadas na conferência
    dt = _carrega('2026', todas=True)
    if len(dt['k']) != n:
        Ct = _contagens_boot(dt['uf_loc'])
        out['sensibilidade_com_reprovadas_D2'] = _conta(dt['X'], dt['loc'], dt['nloc'], Ct)[0]
    else:
        out['sensibilidade_com_reprovadas_D2'] = {'nota': 'nenhuma seção reprovada com RDV nos dois turnos; conta idêntica à principal'}

    # D18: descritivo das outras UFs com 2º turno de governador
    try:
        out['descritivo_ES_DF_AM_RN_amostra'] = _descritivo_aas()
    except Exception as ex:  # descritivo não derruba a abertura
        out['descritivo_ES_DF_AM_RN_amostra'] = {'erro': repr(ex)}
    grava('aberto.json', out)
    P(f'Theta AC+TO = {princ["theta"]:+.4f} (ep {princ["ep"]:.4f}; IC95 percentis {princ["ic95_percentis"][0]:+.4f} a {princ["ic95_percentis"][1]:+.4f}; n {princ["n_secoes"]} seções)')
    P('  P1, P2, W1, W2:', round(princ['P1'], 4), round(princ['P2'], 4), round(princ['W1'], 4), round(princ['W2'], 4), '| somas', princ['somas'])
    for u in UFS:
        q = out['por_uf'][u]
        P(f'  {u}: Theta {q["theta"]:+.4f} (ep {q["ep"]:.4f}) P1 {q["P1"]:.4f} P2 {q["P2"]:.4f} W1 {q["W1"]:.4f} W2 {q["W2"]:.4f} somas {q["somas"]}')
    for nome in ('baixa', 'media', 'alta'):
        q = out['por_tercil_escolaridade'][nome]
        P(f'  tercil {nome}: Theta {q["theta"]:+.4f} (ep {q["ep"]:.4f}) n {q["n_secoes"]}')
    P('  enxerga o plantado:', out['enxerga_o_plantado'], json.dumps({k_: {kk: vv for kk, vv in v_.items() if kk in ('formula', 'aumento_de_theta', 'razao_aumento_formula', 'aumento_em_erros_totais_com_sis_0015')} for k_, v_ in cal['R_para_L'].items()}))
    P('  poder:', json.dumps(out['poder']))
    P('  intervalo dos eliminados:', json.dumps(out['intervalo_dos_eliminados']['deslocamento_de_theta']), 'e =', e)
    P('  inocente:', json.dumps(ino))
    P('  metades:', json.dumps(out['duas_metades']))
    P('  placebo 3:', json.dumps(pl3))
    P('  pesado pelas testemunhas:', json.dumps({k_: (v_['theta'], v_['ep']) for k_, v_ in out['oficial_pesado_pelas_testemunhas'].items()}))
    P('  taxas:', json.dumps(out['taxas_de_erro_de_tela']))
    P('  tercil gov eliminado:', json.dumps({k_: (v_['theta'], v_['ep']) for k_, v_ in out['por_tercil_da_parcela_de_governador_eliminado'].items() if isinstance(v_, dict)}))
    P('  tradução:', json.dumps(out['traducao_em_votos']['ponto']))
    P('  por força:', json.dumps({k_: ((v_['theta'], v_['ep'], v_['formula_p_0357']) if 'theta' in v_ else v_) for k_, v_ in pf.items()}))


def placebo():
    """D21: AL 2022, mesma conta. Sem tercis (R8)."""
    d = _carrega('2022')
    X, loc, nloc, ks, tab = d['X'], d['loc'], d['nloc'], d['k'], d['tab']
    C = _contagens_boot(d['uf_loc'])
    r, rep = _conta(X, loc, nloc, C)
    out = {'uf': 'AL', 'ano': 2022, 'principal': r, 'taxas_de_erro_de_tela': _taxas(X.sum(0)),
           'testemunhas_1t': int(X[:, 4:6].sum()), 'testemunhas_2t': int(X[:, 6:8].sum())}
    muns = sorted(set(d['mun'])); im = {m: i for i, m in enumerate(muns)}; idx = np.array([im[m] for m in d['mun']])
    Xm = np.zeros((len(muns), 8)); np.add.at(Xm, idx, X)
    n_m = Xm[:, 4] + Xm[:, 5]
    rng = np.random.default_rng(SEMENTE)
    out['validade_1t_por_municipio'] = _validade_conta(muns, n_m, Xm[:, 4], Xm[:, 0] / (Xm[:, 0] + Xm[:, 1]), 'AL 2022, 1º turno', rng)
    n2 = Xm[:, 6] + Xm[:, 7]
    ok = n2 > 0
    out['nivel_2t_por_municipio_spearman'] = _spearman(Xm[ok, 6] / n2[ok], Xm[ok, 2] / (Xm[ok, 2] + Xm[ok, 3]))
    # metades, para saber se o placebo é estável
    rng = np.random.default_rng(SEMENTE)
    n = len(ks); difs = []
    for j in range(200):
        perm = rng.permutation(n); mA = np.zeros(n, bool); mA[perm[:n // 2]] = True
        difs.append(float(_theta(X[mA].sum(0)) - _theta(X[~mA].sum(0))))
    out['duas_metades_desvio_das_diferencas'] = float(np.std(difs, ddof=1))
    gov = {}
    for t in ('1', '2'):
        nom = collections.Counter(); dig = collections.Counter()
        for k in ks:
            for c_, q in tab[k]['gn' + t].items():
                nom[c_] += q
            for c_, q in tab[k]['gd' + t].items():
                dig[c_] += q
        gov[f'{t}t'] = {'nominais_por_candidato': dict(sorted(nom.items(), key=lambda kv: -kv[1])), 'nulos_com_digitos_mais_frequentes': dict(sorted(dig.items(), key=lambda kv: -kv[1])[:15]),
                        'comparecimento': sum(tab[k]['comp' + t] for k in ks)}
    out['governador_descritivo'] = gov
    out['gravado_em_utc'] = time.strftime('%Y-%m-%d %H:%M:%S', time.gmtime())
    grava('placebo_AL_2022.json', out)
    P(f'placebo AL 2022: Theta {r["theta"]:+.4f} (ep {r["ep"]:.4f}); n {r["n_secoes"]} seções; testemunhas {out["testemunhas_1t"]} e {out["testemunhas_2t"]}')
    P('  P1, P2, W1, W2:', r['P1'], r['P2'], r['W1'], r['W2'], r['somas'])
    P('  taxas:', json.dumps(out['taxas_de_erro_de_tela']))
    P('  validade 1t:', json.dumps({k_: v_ for k_, v_ in out['validade_1t_por_municipio'].items() if k_ != 'grade'}))


# ---------------------------------------------------------------- exploratório (DEPOIS de ver Theta; não decide nada)
def _mqo_cluster(y, Xr, grupos):
    """MQO sem intercepto com erro agrupado por local (CR1)."""
    b, *_ = np.linalg.lstsq(Xr, y, rcond=None)
    e = y - Xr @ b
    inv = np.linalg.inv(Xr.T @ Xr)
    G = int(grupos.max()) + 1
    Sg = np.zeros((G, Xr.shape[1]))
    np.add.at(Sg, grupos, Xr * e[:, None])
    n, k = Xr.shape
    V = inv @ (Sg.T @ Sg) @ inv * (G / (G - 1)) * ((n - 1) / (n - k))
    return b, np.sqrt(np.diag(V))


def exploratorio():
    """Escrito DEPOIS de abrir Theta (-0,15, no sentido contrário ao da tese, com AC -0,33 e TO -0,09).
    Pergunta: o que move o termômetro entre os turnos, a disputa de governador ou a contagem de presidente?
    E1. Por seção e por UF: nulos de governador com 13 (e com 22) no 2º turno contra votos oficiais de Lula e de Flávio
        no 2º turno, as testemunhas do mesmo número no 1º turno e os votos de cada candidato a governador eliminado no
        1º turno. Se o que sobra de 13 no 2º turno acompanha os votos de um governador eliminado, é a disputa de governador.
    E2. Theta por décimos da parcela dos votos de governador do 1º turno dada a eliminados (dentro de cada UF) e a reta
        até parcela zero (o que o termômetro diria sem eleitor órfão de governador).
    E3. Quanto de 13 a mais (ou de 22 a menos) no 2º turno basta para levar Theta a zero, ao lado dos votos dos eliminados.
    E4. Theta por tercil de força de Lula dentro de cada UF (o R11 misturava AC e TO).
    E5. Leitura a favor da tese que o sinal negativo admite: cédulas inteiras fabricadas ou trocadas para Lula com o 13
        repetido em governador. Teto em votos se TODO o excesso de 13 fosse isso, e o que a regressão E1 diz: o excesso
        acompanha Lula e Flávio no 2º turno ou os eliminados de governador?
    """
    d = _carrega('2026')
    X, loc, nloc, ks, tab = d['X'], d['loc'], d['nloc'], d['k'], d['tab']
    C = _contagens_boot(d['uf_loc'])
    fin = {'AC': ('10', '11'), 'TO': ('44', '45')}
    out = {'aviso': 'exploratório, feito depois de ver o resultado; não decide nada'}
    S = X.sum(0)
    # E3
    dP = math.log(S[2] / S[3]) - math.log(S[0] / S[1])
    a2_zero = S[7] * (S[4] / S[5]) * math.exp(dP)
    b2_zero = S[6] / ((S[4] / S[5]) * math.exp(dP))
    out['E3_quanto_basta'] = {'g13_2t_observado': int(S[6]), 'g13_2t_que_daria_theta_zero': a2_zero, 'excesso_de_13': S[6] - a2_zero, 'excesso_de_13_por_cento_dos_votos_de_lula_2t': 100 * (S[6] - a2_zero) / S[2],
                              'g22_2t_observado': int(S[7]), 'g22_2t_que_daria_theta_zero': b2_zero, 'falta_de_22': b2_zero - S[7], 'falta_de_22_por_cento_dos_votos_de_flavio_2t': 100 * (b2_zero - S[7]) / S[3],
                              'por_uf': {}}
    for u in UFS:
        Su = X[d['uf'] == u].sum(0)
        dPu = math.log(Su[2] / Su[3]) - math.log(Su[0] / Su[1])
        az = Su[7] * (Su[4] / Su[5]) * math.exp(dPu)
        elim = collections.Counter()
        for k in ks:
            if tab[k]['uf'] == u:
                for c_, q in tab[k]['gn1'].items():
                    if c_ not in fin[u]:
                        elim[c_] += q
        out['E3_quanto_basta']['por_uf'][u] = {'excesso_de_13': Su[6] - az, 'excesso_por_cento_dos_votos_de_lula_2t': 100 * (Su[6] - az) / Su[2],
                                               'votos_de_governador_eliminado_1t': dict(elim), 'excesso_sobre_votos_dos_eliminados': (Su[6] - az) / sum(elim.values())}
    # E1
    out['E1_regressao_por_secao'] = {}
    for u in UFS:
        m = d['uf'] == u
        kk = [k for k, mm in zip(ks, m) if mm]
        cands = sorted({c_ for k in kk for c_ in tab[k]['gn1'] if c_ not in fin[u]}, key=int)
        tot = {c_: sum(tab[k]['gn1'].get(c_, 0) for k in kk) for c_ in cands}
        cands = [c_ for c_ in cands if tot[c_] >= 3000]
        E = np.array([[tab[k]['gn1'].get(c_, 0) for c_ in cands] for k in kk], float)
        Xu = X[m]
        _, g = np.unique(loc[m], return_inverse=True)
        res = {}
        for alvo, col2, col1 in (('g13_2t', 6, 4), ('g22_2t', 7, 5)):
            Xr = np.column_stack([Xu[:, 2], Xu[:, 3], Xu[:, col1], E])
            b, se = _mqo_cluster(Xu[:, col2], Xr, g)
            nomes = ['por voto de Lula no 2º turno', 'por voto de Flávio no 2º turno', 'por testemunha do mesmo número no 1º turno'] + [f'por voto do governador eliminado {c_} no 1º turno' for c_ in cands]
            res[alvo] = {nm: {'coef': float(bb), 'ep': float(ss)} for nm, bb, ss in zip(nomes, b, se)}
            res[alvo]['_explicado_pelos_eliminados'] = {c_: float(bb * tot[c_]) for c_, bb in zip(cands, b[3:])}
        res['votos_dos_eliminados_1t'] = {c_: tot[c_] for c_ in cands}
        res['n_secoes'] = int(m.sum())
        out['E1_regressao_por_secao'][u] = res
    # Theta depois de tirar das testemunhas do 2º turno o que a regressão atribui aos eleitores de governador eliminado
    Xc = X.copy()
    for u in UFS:
        m = np.flatnonzero(d['uf'] == u)
        res = out['E1_regressao_por_secao'][u]
        cands = list(res['votos_dos_eliminados_1t'])
        E = np.array([[tab[ks[i]]['gn1'].get(c_, 0) for c_ in cands] for i in m], float)
        for alvo, col2 in (('g13_2t', 6), ('g22_2t', 7)):
            bet = np.array([res[alvo][f'por voto do governador eliminado {c_} no 1º turno']['coef'] for c_ in cands])
            Xc[m, col2] = X[m, col2] - E @ bet
    out['theta_sem_a_parte_atribuida_aos_eliminados_de_governador'] = {'AC+TO': float(_theta(Xc.sum(0))), **{u: float(_theta(Xc[d['uf'] == u].sum(0))) for u in UFS},
                                                                      'nota': 'conta de modelo, ecológica; serve para ver a ordem de grandeza, não para decidir'}
    # E2
    pe = {}
    for k in ks:
        g_ = tab[k]['gn1']; t_ = sum(g_.values())
        if t_ > 0:
            pe[k] = 1 - sum(g_.get(f, 0) for f in fin[tab[k]['uf']]) / t_
    out['E2_decimos'] = {}
    for u in UFS:
        ku = sorted((k for k in pe if tab[k]['uf'] == u), key=lambda k: (pe[k], k))
        n = len(ku)
        grupo = {k: min(9, i * 10 // n) for i, k in enumerate(ku)}
        linhas, reps, xs = [], [], []
        for gq in range(10):
            mm = np.array([grupo.get(k) == gq for k in ks])
            r, rp = _conta(X, loc, nloc, C, mm)
            xm = float(np.mean([pe[k] for k in ku if grupo[k] == gq]))
            tx = _taxas(X[mm].sum(0))
            linhas.append({'decimo': gq + 1, 'parcela_media': xm, 'theta': r['theta'], 'ep': r['ep'], 'multiplicador_r13': tx['multiplicador_r13'], 'multiplicador_r22': tx['multiplicador_r22']})
            reps.append(rp); xs.append(xm)
        xs = np.array(xs); th = np.array([l['theta'] for l in linhas]); w = 1 / np.array([l['ep'] for l in linhas]) ** 2
        def reta(y):
            A_ = np.column_stack([np.ones(10), xs]) * np.sqrt(w)[:, None]
            return np.linalg.lstsq(A_, y * np.sqrt(w), rcond=None)[0]
        b0 = reta(th)
        R = np.array(reps)
        okr = np.isfinite(R).all(0)
        bb = np.array([reta(R[:, j]) for j in np.flatnonzero(okr)])
        out['E2_decimos'][u] = {'linhas': linhas, 'reta': {'theta_na_parcela_zero': float(b0[0]), 'ep': float(bb[:, 0].std(ddof=1)), 'inclinacao': float(b0[1]), 'ep_inclinacao': float(bb[:, 1].std(ddof=1))}}
    # E2b: Theta só nas seções da metade de baixo da parcela de governador eliminado, por UF
    out['E2b_metade_de_baixo'] = {}
    for u in UFS:
        ku = sorted((k for k in pe if tab[k]['uf'] == u), key=lambda k: (pe[k], k))
        baixo = set(ku[:len(ku) // 2])
        mm = np.array([k in baixo for k in ks])
        r, _ = _conta(X, loc, nloc, C, mm)
        out['E2b_metade_de_baixo'][u] = {'theta': r['theta'], 'ep': r['ep'], 'n_secoes': r['n_secoes'], 'parcela_maxima': max(pe[k] for k in baixo),
                                         'formula_p_0357': math.log((1 + 0.0357 * r['somas']['R2'] / r['somas']['L2']) / (1 - 0.0357)), 'taxas': _taxas(X[mm].sum(0))}
    # E4
    out['E4_forca_dentro_da_uf'] = {}
    for u in UFS:
        p1s = {k: X[i, 0] / (X[i, 0] + X[i, 1]) for i, k in enumerate(ks) if tab[k]['uf'] == u and X[i, 0] + X[i, 1] > 0}
        mf = _mascaras_tercil(ks, _tercis(p1s), {2: 'lula_forte', 1: 'meio', 0: 'lula_fraco'})
        q = {}
        rr = {}
        for nome, mm in mf.items():
            r, rp = _conta(X, loc, nloc, C, mm)
            q[nome] = {'theta': r['theta'], 'ep': r['ep'], 'R_sobre_L_2t': r['somas']['R2'] / r['somas']['L2'], 'formula_p_0357': math.log((1 + 0.0357 * r['somas']['R2'] / r['somas']['L2']) / (1 - 0.0357))}
            rr[nome] = rp
        dr = rr['lula_fraco'] - rr['lula_forte']
        q['diferenca_fraco_menos_forte'] = {'observada': q['lula_fraco']['theta'] - q['lula_forte']['theta'], 'ep': float(dr[np.isfinite(dr)].std(ddof=1)), 'prevista_p_0357': q['lula_fraco']['formula_p_0357'] - q['lula_forte']['formula_p_0357']}
        out['E4_forca_dentro_da_uf'][u] = q
    # E5
    exc = out['E3_quanto_basta']['excesso_de_13']
    val2 = float(S[2] + S[3])
    out['E5_leitura_a_favor_cedula_inteira'] = {
        'hipotese': 'cédulas inteiras fabricadas ou trocadas para Lula com o 13 repetido em governador deixariam 13 a mais entre os nulos de governador',
        'excesso_de_13_em_AC_e_TO': exc, 'por_cento_dos_validos_de_AC_e_TO': 100 * exc / val2,
        'se_todo_o_excesso_fosse_isso_e_igual_no_pais_cedulas': exc / val2 * (L2_OFICIAL + R2_OFICIAL),
        'efeito_na_margem_se_fabricadas': exc / val2 * (L2_OFICIAL + R2_OFICIAL), 'efeito_na_margem_se_trocadas': 2 * exc / val2 * (L2_OFICIAL + R2_OFICIAL),
        'fracao_da_margem_se_fabricadas': exc / val2 * (L2_OFICIAL + R2_OFICIAL) / MARGEM, 'fracao_da_margem_se_trocadas': 2 * exc / val2 * (L2_OFICIAL + R2_OFICIAL) / MARGEM,
        'nota': 'teto: atribui à fraude todo o excesso, inclusive a parte que a regressão E1 liga aos eleitores de governador eliminado'}
    # E6: o 13 a mais acompanha o aumento de comparecimento da seção? (cédula fabricada com 13 nos dois cargos daria perto de 1)
    out['E6_comparecimento'] = {}
    for u in UFS:
        m = d['uf'] == u
        kk = [k for k, mm in zip(ks, m) if mm]
        Xu = X[m]
        dc = np.array([tab[k]['comp2'] - tab[k]['comp1'] for k in kk], float)
        _, g = np.unique(loc[m], return_inverse=True)
        cands = list(out['E1_regressao_por_secao'][u]['votos_dos_eliminados_1t'])
        E = np.array([[tab[k]['gn1'].get(c_, 0) for c_ in cands] for k in kk], float)
        r6 = {'variacao_do_comparecimento_total': float(dc.sum()), 'secoes_com_aumento': int((dc > 0).sum()), 'aumento_somado_nas_que_subiram': float(dc[dc > 0].sum())}
        for alvo, col2, col1 in (('g13_2t', 6, 4), ('g22_2t', 7, 5)):
            Xr = np.column_stack([Xu[:, 2], Xu[:, 3], Xu[:, col1], E, np.maximum(dc, 0), np.minimum(dc, 0)])
            b_, se_ = _mqo_cluster(Xu[:, col2], Xr, g)
            r6[alvo] = {'por_eleitor_a_mais_na_secao': {'coef': float(b_[-2]), 'ep': float(se_[-2])}, 'por_eleitor_a_menos_na_secao': {'coef': float(b_[-1]), 'ep': float(se_[-1])}}
        out['E6_comparecimento'][u] = r6
    # E7: a mesma regressão (E1) e os mesmos décimos (E2) no placebo AL 2022, onde quem ficou sem candidato a governador no
    # 2º turno foi o lado de Bolsonaro (o 14 foi eliminado) e Theta saiu positivo
    if os.path.exists(f'{TRAB}/tabela_2022.json.gz'):
        d2 = _carrega('2022')
        X2, loc2, ks2, tab2 = d2['X'], d2['loc'], d2['k'], d2['tab']
        C2 = _contagens_boot(d2['uf_loc'])
        fin2 = ('15', '44')
        cands = sorted({c_ for k in ks2 for c_ in tab2[k]['gn1'] if c_ not in fin2}, key=int)
        tot = {c_: sum(tab2[k]['gn1'].get(c_, 0) for k in ks2) for c_ in cands}
        cands = [c_ for c_ in cands if tot[c_] >= 3000]
        E = np.array([[tab2[k]['gn1'].get(c_, 0) for c_ in cands] for k in ks2], float)
        _, g = np.unique(loc2, return_inverse=True)
        res = {'votos_dos_eliminados_1t': {c_: tot[c_] for c_ in cands}, 'n_secoes': len(ks2)}
        for alvo, col2, col1 in (('g13_2t', 6, 4), ('g22_2t', 7, 5)):
            Xr = np.column_stack([X2[:, 2], X2[:, 3], X2[:, col1], E])
            b_, se_ = _mqo_cluster(X2[:, col2], Xr, g)
            nomes = ['por voto de Lula no 2º turno', 'por voto de Bolsonaro no 2º turno', 'por testemunha do mesmo número no 1º turno'] + [f'por voto do governador eliminado {c_} no 1º turno' for c_ in cands]
            res[alvo] = {nm: {'coef': float(bb), 'ep': float(ss)} for nm, bb, ss in zip(nomes, b_, se_)}
            res[alvo]['_explicado_pelos_eliminados'] = {c_: float(bb * tot[c_]) for c_, bb in zip(cands, b_[3:])}
        pe2 = {}
        for k in ks2:
            g_ = tab2[k]['gn1']; t_ = sum(g_.values())
            if t_ > 0:
                pe2[k] = 1 - sum(g_.get(f, 0) for f in fin2) / t_
        ku = sorted(pe2, key=lambda k: (pe2[k], k))
        n2 = len(ku)
        grupo = {k: min(9, i * 10 // n2) for i, k in enumerate(ku)}
        linhas, reps, xs = [], [], []
        for gq in range(10):
            mm = np.array([grupo.get(k) == gq for k in ks2])
            r, rp = _conta(X2, loc2, d2['nloc'], C2, mm)
            tx = _taxas(X2[mm].sum(0))
            xm = float(np.mean([pe2[k] for k in ku if grupo[k] == gq]))
            linhas.append({'decimo': gq + 1, 'parcela_media': xm, 'theta': r['theta'], 'ep': r['ep'], 'multiplicador_r13': tx['multiplicador_r13'], 'multiplicador_r22': tx['multiplicador_r22']})
            reps.append(rp); xs.append(xm)
        xs = np.array(xs); th = np.array([l['theta'] for l in linhas]); w = 1 / np.array([l['ep'] for l in linhas]) ** 2
        def reta2(y):
            A_ = np.column_stack([np.ones(10), xs]) * np.sqrt(w)[:, None]
            return np.linalg.lstsq(A_, y * np.sqrt(w), rcond=None)[0]
        b0 = reta2(th)
        R = np.array(reps)
        bb = np.array([reta2(R[:, j]) for j in np.flatnonzero(np.isfinite(R).all(0))])
        S2 = X2.sum(0)
        dP2 = math.log(S2[2] / S2[3]) - math.log(S2[0] / S2[1])
        out['E7_placebo_AL_2022'] = {'regressao': res, 'decimos': linhas,
                                     'reta': {'theta_na_parcela_zero': float(b0[0]), 'ep': float(bb[:, 0].std(ddof=1)), 'inclinacao': float(b0[1]), 'ep_inclinacao': float(bb[:, 1].std(ddof=1))},
                                     'excesso_de_22_no_2t_para_theta_zero': float(S2[7] - S2[6] / ((S2[4] / S2[5]) * math.exp(dP2))),
                                     'traducao_literal': _traduz(float(_theta(S2)), float(S2[2] / (S2[2] + S2[3])), float(S2[3]), float(S2[2]))}
    # E8: de que lado era o eleitor de cada candidato a governador? Correlação, por seção, entre a parcela do candidato nos
    # votos nominais de governador do 1º turno e a parcela de Lula (L/(L+R)) no 1º turno. Só descreve; não usa partido.
    out['E8_lado_dos_candidatos_a_governador'] = {}
    for ano, ufs_ in (('2026', UFS), ('2022', ['AL'])):
        if not os.path.exists(f'{TRAB}/tabela_{ano}.json.gz'):
            continue
        dd = d if ano == '2026' else _carrega(ano)
        for u in ufs_:
            idx = [i for i, k in enumerate(dd['k']) if dd['tab'][k]['uf'] == u and dd['X'][i, 0] + dd['X'][i, 1] > 0 and sum(dd['tab'][k]['gn1'].values()) > 0]
            p1 = np.array([dd['X'][i, 0] / (dd['X'][i, 0] + dd['X'][i, 1]) for i in idx])
            tot = collections.Counter()
            for i in idx:
                for c_, q in dd['tab'][dd['k'][i]]['gn1'].items():
                    tot[c_] += q
            r8 = {}
            for c_, q in sorted(tot.items(), key=lambda kv: -kv[1]):
                if q < 3000:
                    continue
                sh = np.array([dd['tab'][dd['k'][i]]['gn1'].get(c_, 0) / sum(dd['tab'][dd['k'][i]]['gn1'].values()) for i in idx])
                r8[c_] = {'votos_1t': int(q), 'parcela': float(q / sum(tot.values())), 'correlacao_com_a_parcela_de_lula_1t': float(np.corrcoef(sh, p1)[0, 1])}
            out['E8_lado_dos_candidatos_a_governador'][f'{u} {ano}'] = r8
    grava('exploratorio_calculos.json', out)
    P(json.dumps(out.get('E8_lado_dos_candidatos_a_governador'), ensure_ascii=False))


# ---------------------------------------------------------------- veredito e relatório
def _veredito(ab, val, sis):
    """Ordem do D9, à letra. sis = erro sistemático usado."""
    th, ep = ab['principal']['theta'], ab['principal']['ep']
    err = math.hypot(ep, sis)
    cs = _criterio_sinal(ab['bateria'], sis)
    ce = _criterio_sinal(ab['bateria'], sis, espelho=True)
    base = {'theta': th, 'erro_padrao': ep, 'erro_sistematico': sis, 'erro_total': err, 'criterio_de_sinal': cs, 'criterio_de_sinal_no_espelho': ce}
    if ep > 0.025:
        return dict(base, veredito='SEM PODER', motivos=['erro-padrão de Theta acima de 0,025'])
    if not ab['enxerga_o_plantado']:
        return dict(base, veredito='SEM PODER', motivos=['a calibração não enxerga a troca plantada de 3,57%'])
    if not val['aprovado']:
        return dict(base, veredito='INCONCLUSIVO', motivos=['termômetro reprovado na validade do 1º turno'])
    if abs(th) <= 0.020 and err <= 0.025:
        return dict(base, veredito='SEM SINAL', motivos=['|Theta| de no máximo 0,020 com erro total de no máximo 0,025'])
    if cs['sinal']:
        return dict(base, veredito='SINAL', motivos=['Theta de pelo menos 0,045, de pelo menos 2,5 erros totais, com o mesmo sinal em AC, TO e nos três tercis'])
    m = []
    if err > 0.025:
        m.append('erro total acima de 0,025')
    if 0.020 < th < 0.045:
        m.append('Theta entre 0,020 e 0,045')
    if th >= 0.045 and not cs['razao_ok']:
        m.append('Theta acima de 0,045 mas abaixo de 2,5 erros totais')
    if th >= 0.045 and not cs['mesmo_sinal_ufs_e_tercis']:
        m.append('sinais diferentes entre AC, TO ou os tercis')
    if th < -0.020:
        m.append('Theta abaixo de -0,020, no sentido contrário ao da tese: o registro não tem cláusula para isso')
    return dict(base, veredito='INCONCLUSIVO', motivos=m)


def fv(x, n=4, sinal=True):
    if x is None or (isinstance(x, float) and not math.isfinite(x)):
        return 'n/d'
    return (f'{x:+.{n}f}' if sinal else f'{x:.{n}f}').replace('.', ',')


def fi(x):
    return f'{int(round(x)):,}'.replace(',', '.')


def fpc(x, n=1):
    return (f'{100 * x:.{n}f}').replace('.', ',') + '%'


def _quebra(txt, larg=118, rec='  '):
    import textwrap
    out = []
    for par in txt.split('\n'):
        if not par.strip():
            out.append('')
            continue
        ind = len(par) - len(par.lstrip(' '))
        out += textwrap.wrap(par.strip(), width=larg, initial_indent=' ' * ind, subsequent_indent=' ' * ind + (rec if ind == 0 else ''), break_long_words=False, break_on_hyphens=False)
    return '\n'.join(out)


def leitura():
    """Textos de leitura, escritos DEPOIS de ver o resultado. Os números saem dos arquivos de trabalho."""
    et1, val, ab, pla, ex = le('etapa1.json'), le('validade.json'), le('aberto.json'), le('placebo_AL_2022.json'), le('exploratorio_calculos.json')
    pr = ab['principal']
    th, ep = pr['theta'], pr['ep']
    cal = ab['calibracao_plantio']['R_para_L']['p_0.0357']
    tx = ab['taxas_de_erro_de_tela']
    tg = ab['por_tercil_da_parcela_de_governador_eliminado']
    pf = ab['por_tercil_de_forca_de_lula_1t']
    e1, e2, e2b, e3, e4, e5, e6, e7, e8 = (ex[k] for k in ('E1_regressao_por_secao', 'E2_decimos', 'E2b_metade_de_baixo', 'E3_quanto_basta', 'E4_forca_dentro_da_uf', 'E5_leitura_a_favor_cedula_inteira', 'E6_comparecimento', 'E7_placebo_AL_2022', 'E8_lado_dos_candidatos_a_governador'))
    tp = pla['principal']['theta']
    cF = {u: e1[u]['g13_2t']['por voto de Flávio no 2º turno'] for u in UFS}
    teto = {u: cF[u]['coef'] + 1.96 * cF[u]['ep'] for u in UFS}
    neg_dec = sum(1 for u in UFS for l in e2[u]['linhas'] if l['theta'] < 0)
    sis_int = abs(ab['por_uf']['AC']['theta'] - ab['por_uf']['TO']['theta']) / 2
    L = {}
    L['erro_sistematico_interno_2026_exploratorio'] = {'definicao': 'metade da diferença de Theta entre AC e TO (só 2026, escolhido depois de ver)', 'valor': sis_int,
                                                       'erro_total': math.hypot(ep, sis_int), 'menos_theta_sobre_erro_total': -th / math.hypot(ep, sis_int)}
    L['uma_frase'] = (f'INCONCLUSIVO pela letra, e o teste não decide. Theta saiu {fv(th)} (ep {fv(ep, 4, False)}), no sentido CONTRÁRIO ao da tese: as testemunhas andaram para Lula mais do que a contagem oficial, não menos. '
                      f'Pela mesma régua, o espelho (a favor de Flávio) daria SINAL com o erro sistemático mínimo, mas o placebo (AL 2022: {fv(tp)}) e os recortes de 2026 (AC {fv(ab["por_uf"]["AC"]["theta"], 2)}, TO {fv(ab["por_uf"]["TO"]["theta"], 2)}; de {fv(tg["menor"]["theta"], 2)} a {fv(tg["maior"]["theta"], 2)} conforme a disputa de governador) '
                      f'mostram que o termômetro muda entre os turnos por causa da eleição de governador, em tamanho de 2 a 4 vezes o efeito procurado ({fv(ab["poder"]["formula_p_0357"], 3)}). Não acusa e não absolve.')
    L['a_favor'] = [
        f'1. O teste não absolve. O zero do termômetro está fora do lugar ({fv(th, 2)} em AC e TO, {fv(ab["por_uf"]["AC"]["theta"], 2)} no AC). Com a troca de 3,57% plantada na contagem, Theta sobe o valor exato da fórmula ({fv(cal["aumento_de_theta"])}), mas fica em {fv(cal["bateria_com_plantio"]["theta"])} e o critério de SINAL não dispara. '
        f'Não dá para excluir que o comportamento de quem anula o governador, sozinho, desse {fv(th - ab["poder"]["formula_p_0357"], 2)} e a contagem somasse {fv(ab["poder"]["formula_p_0357"], 2)}.',
        f'2. Quando se tenta tirar o efeito da disputa de governador (exploratório, conta de modelo), o TO passa para o lado positivo: a reta até a parcela zero de governador eliminado dá {fv(e2["TO"]["reta"]["theta_na_parcela_zero"])} (ep {fv(e2["TO"]["reta"]["ep"], 4, False)}) e a regressão por seção dá {fv(ex["theta_sem_a_parte_atribuida_aos_eliminados_de_governador"]["TO"])}. '
        f'A troca que vira o resultado daria {fv(math.log((1 + 0.0357 * ab["por_uf"]["TO"]["somas"]["R2"] / ab["por_uf"]["TO"]["somas"]["L2"]) / (1 - 0.0357)), 3)} no TO. Esses dois números são compatíveis com zero e com a troca; não separam.',
        f'3. Dentro do AC, Theta é menos negativo onde Lula é fraco: diferença de {fv(e4["AC"]["diferenca_fraco_menos_forte"]["observada"])} (ep {fv(e4["AC"]["diferenca_fraco_menos_forte"]["ep"], 4, False)}) entre os tercis, o sentido que uma troca proporcional prevê ({fv(e4["AC"]["diferenca_fraco_menos_forte"]["prevista_p_0357"])} para 3,57%), embora 2,7 vezes maior do que essa troca daria.',
        f'4. O sinal negativo admite uma leitura a favor da tese: cédulas inteiras fabricadas ou trocadas para Lula, com o 13 repetido na tela de governador, deixariam 13 a mais entre os nulos de governador. O excesso é de {fi(e5["excesso_de_13_em_AC_e_TO"])} votos ({fv(e5["por_cento_dos_validos_de_AC_e_TO"], 2, False)}% dos válidos de AC e TO). '
        f'Lido inteiro como fraude e estendido ao país, valeria {fpc(e5["fracao_da_margem_se_fabricadas"])} da margem se fabricadas e {fpc(e5["fracao_da_margem_se_trocadas"])} se trocadas. É teto, e os itens 4 e 5 do que pesa contra o reduzem.',
        f'5. O placebo lido ao pé da letra aponta no sentido da tese do Léo para 2022: em AL 2022 a contagem andou para Lula mais do que as testemunhas, Theta {fv(tp)} ({fv(tp / pla["principal"]["ep"], 1, False)} ep). Mas o tamanho ({fpc(e7["traducao_literal"]["fracao_p"])} dos votos de Bolsonaro) é mais de 6 vezes a fração que viraria 2022 (1,8%), e o sinal troca de 2022 para 2026 com o mesmo vencedor.',
        '6. RDV, boletim e bweb saem do mesmo programa. Um programa que reescrevesse os nulos de governador junto com o voto de presidente escaparia deste teste por construção.']
    L['contra'] = [
        f'1. Theta é negativo em todos os recortes registrados antes: AC ({fv(ab["por_uf"]["AC"]["theta"], 3)}), TO ({fv(ab["por_uf"]["TO"]["theta"], 3)}), os três tercis de escolaridade ({fv(ab["por_tercil_escolaridade"]["baixa"]["theta"], 3)}, {fv(ab["por_tercil_escolaridade"]["media"]["theta"], 3)}, {fv(ab["por_tercil_escolaridade"]["alta"]["theta"], 3)}), '
        f'os três de governador eliminado e os três de força de Lula; e em {neg_dec} de 20 décimos (exploratório). Em nenhum a contagem oficial andou para Lula mais do que as testemunhas. A marca prevista pela tese era positiva: {fv(ab["poder"]["formula_p_0357"])}.',
        f'2. No TO, na metade das seções com menos voto de governador eliminado ({fi(e2b["TO"]["n_secoes"])} seções), onde o termômetro é menos contaminado, Theta = {fv(e2b["TO"]["theta"])} (ep {fv(e2b["TO"]["ep"], 4, False)}); a troca que vira daria {fv(e2b["TO"]["formula_p_0357"])}, que fica a {fv((e2b["TO"]["formula_p_0357"] - e2b["TO"]["theta"]) / e2b["TO"]["ep"], 1, False)} ep (exploratório, só erro de amostra).',
        f'3. A inclinação por força de Lula (R11, fixada antes de abrir) tem o sinal contrário ao da troca proporcional: {fv(pf["diferenca_fraco_menos_forte"]["observada"])} (ep {fv(pf["diferenca_fraco_menos_forte"]["ep"], 4, False)}) contra {fv(pf["diferenca_fraco_menos_forte"]["prevista_pela_formula_p_0357"])} previsto; dentro do TO, {fv(e4["TO"]["diferenca_fraco_menos_forte"]["observada"])} (ep {fv(e4["TO"]["diferenca_fraco_menos_forte"]["ep"], 4, False)}) contra {fv(e4["TO"]["diferenca_fraco_menos_forte"]["prevista_p_0357"])}.',
        f'4. O 13 a mais do 2º turno não acompanha os votos de Flávio da seção (AC {fv(cF["AC"]["coef"])}, ep {fv(cF["AC"]["ep"], 4, False)}; TO {fv(cF["TO"]["coef"])}, ep {fv(cF["TO"]["ep"], 4, False)} por voto de Flávio). Cédula inteira trocada de Flávio para Lula com o 13 repetido fica limitada a {fpc(teto["AC"], 2)} (AC) e {fpc(teto["TO"], 2)} (TO) dos votos de Flávio, no teto de 95%: menos de um décimo dos 3,57% (exploratório, conta de modelo).',
        f'5. Também não acompanha comparecimento novo: no AC o comparecimento caiu {fi(-e6["AC"]["variacao_do_comparecimento_total"])} e só {fi(e6["AC"]["secoes_com_aumento"])} seções subiram, somando {fi(e6["AC"]["aumento_somado_nas_que_subiram"])} eleitores; no TO caiu {fi(-e6["TO"]["variacao_do_comparecimento_total"])}, com {fi(e6["TO"]["aumento_somado_nas_que_subiram"])} eleitores a mais em {fi(e6["TO"]["secoes_com_aumento"])} seções. '
        f'Por eleitor a mais aparecem {fv(e6["AC"]["g13_2t"]["por_eleitor_a_mais_na_secao"]["coef"], 2, False)} (ep {fv(e6["AC"]["g13_2t"]["por_eleitor_a_mais_na_secao"]["ep"], 2, False)}) e {fv(e6["TO"]["g13_2t"]["por_eleitor_a_mais_na_secao"]["coef"], 2, False)} (ep {fv(e6["TO"]["g13_2t"]["por_eleitor_a_mais_na_secao"]["ep"], 2, False)}) nulos com 13; cédula fabricada com 13 nos dois cargos daria perto de 1.',
        f'6. O termômetro acompanha a eleição de governador, não quem ganhou a presidência: Theta foi {fv(tp, 2)} em AL 2022 e {fv(th, 2)} em AC e TO 2026, com Lula vencendo as duas; e dentro de cada UF muda com a parcela dos votos de governador dada a eliminados (TO: de {fv(e2["TO"]["linhas"][1]["theta"], 2)} a {fv(e2["TO"]["linhas"][9]["theta"], 2)}; inclinação {fv(e2["TO"]["reta"]["inclinacao"], 2)}, ep {fv(e2["TO"]["reta"]["ep_inclinacao"], 2, False)}). '
        'Uma alteração só na contagem de presidente não tem por que depender da disputa de governador.',
        f'7. Os RDV conferem com o bweb em {fi(pr["n_secoes"])} seções, nos dois turnos e nos dois cargos, candidato a candidato. Isso fecha alteração depois da urna nessas seções; não pesa contra programa adulterado na origem.']
    L['significa'] = [
        f'O desenho supunha que quem digita o número do presidenciável na tela de governador é uma amostra estável da intenção presidencial entre os turnos. Não é. No 1º turno são {fi(pr["somas"]["a1"] + pr["somas"]["b1"])} testemunhas ({fv(et1["recortes"]["AC+TO"]["testemunhas_por_100_votantes_1t"], 1, False)} por 100 votantes), MAIS do que no 2º ({fi(pr["somas"]["a2"] + pr["somas"]["b2"])}; {fv(et1["recortes"]["AC+TO"]["testemunhas_por_100_votantes_2t"], 1, False)} por 100): '
        f'é sobretudo voto de legenda de quem não tem candidato a governador do seu partido, não erro de tela. A taxa por eleitor cai entre os turnos em fatores diferentes de cada lado (13: vezes {fv(tx["AC+TO"]["multiplicador_r13"], 2, False)}; 22: vezes {fv(tx["AC+TO"]["multiplicador_r22"], 2, False)}), e os fatores mudam com a UF e com a disputa de governador.',
        f'O erro sistemático real do instrumento é da ordem de 0,1 a 0,3 (AL 2022 {fv(tp, 2)}; AC {fv(ab["por_uf"]["AC"]["theta"], 2)}; TO {fv(ab["por_uf"]["TO"]["theta"], 2)}), contra 0,015 suposto no registro e {fv(ab["poder"]["formula_p_0357"], 3)} procurado. O teste tinha erro de amostra de sobra (ep {fv(ep, 4, False)}) e termômetro aprovado no 1º turno ({fv(val["principal_AC_TO"]["correlacao_que_decide"], 3, False)}), mas a validade em nível num turno não garante estabilidade entre os turnos.',
        f'O SINAL do espelho pela letra (só com 2026) não conta como indício de fraude a favor de Flávio. Das três condições do Adendo 27, falha a calibração: a explicação inocente plantada desloca Theta do mesmo jeito que a troca, e o deslocamento medido acompanha a disputa de governador. Com o placebo o erro total vai a {fv(math.hypot(ep, abs(tp)), 3, False)} e o espelho cai para {fv(-th / math.hypot(ep, abs(tp)), 2, False)} erro. '
        f'Só com 2026, usando como erro sistemático metade da diferença entre AC e TO ({fv(sis_int, 3, False)}; exploratório), cai para {fv(-th / math.hypot(ep, sis_int), 2, False)} erro.',
        'Consequência para a investigação: este era um dos dois únicos desenhos registrados que, em princípio, enxergariam uma troca sorteada e coerente dentro da urna. Em AC e TO ele não enxerga nada do tamanho necessário, nem para acusar nem para absolver. A porta continua aberta e sobra o D4-4 (nulos de digitação no próprio voto de presidente), que não passa pela eleição de governador.']
    L['pistas'] = [
        '1. D4-4 no universo, não em amostra: os pacotes de arquivos transmitidos do TSE podem ser lidos em fluxo guardando só RDV e boletim (uma UF inteira ocupa de 4 a 64 MB). Com todas as UFs o erro do D4-4 cai para perto de 0,007 e ele não depende da eleição de governador.',
        '2. Medir a instabilidade do termômetro de governador com mais casos: a mesma conta em todas as UFs e anos em que 13 e o número do adversário não eram candidatos a governador nos dois turnos (2018 e 2022 estão no mesmo endereço). Se a dispersão ficar em 0,2 ou mais, o desenho D4-3 deve ser abandonado de vez.',
        f'3. AC: a taxa do 13 quase não caiu no 2º turno (vezes {fv(tx["AC"]["multiplicador_r13"], 2, False)}, contra {fv(tx["TO"]["multiplicador_r13"], 2, False)} no TO e {fv(pla["taxas_de_erro_de_tela"]["multiplicador_r13"], 2, False)} em AL 2022) e passa de 1 onde mais votos de governador foram para eliminados. É o número mais fora da curva do teste. Conferir na imprensa local quem PT e PL apoiaram no 2º turno de governador do AC e do TO (não conferido aqui).',
        '4. Pacote do TSE do TO, 2º turno: há um membro a mais, de 47 bytes, chamado 5Nim5OYPO-buOO056ziCIDfG3kH3gPCuilBllCcL8yE=.id, cujo conteúdo é o próprio nome. Não tem voto e parece marca de ferramenta de armazenamento; vale perguntar ao TSE o que é. Os outros três pacotes de 2026 não têm.',
        '5. Para o conferente: refazer com código próprio a partir dos quatro pacotes; os números a bater são as somas 13/22 por UF e turno (seção 4) e Theta. Conferir em especial se a leitura do nulo com dígitos (tipo 4 do RDV, cargo 3) é a mesma.']
    L['desvios'] = [
        'Fonte: pacotes de arquivos transmitidos do TSE por UF e turno, lidos em fluxo (nada do zip em disco; só RDV e boletim guardados, com CRC conferido), em vez do download seção a seção do desenho.',
        'Execução retomada depois de interrupção: o docstring é o do commit 6677983, sem mudança. As decisões que faltavam (R1 a R10, 10:57 UTC) e a regra do veredito em código estão no commit 9a8dd54 (11:07:41 UTC, feito pela sessão principal), anterior à etapa 1 (11:27 UTC); o SHA-256 do bloco nesse commit é o mesmo de registro_decisoes.json. A leitura R11 (11:09 UTC) só tem horário local, não tem commit anterior ao resultado. Este agente não fez commit.',
        f'Dois fluxos ao mesmo tempo no cdn do TSE (TO 2026 e AL 2022), contra a regra de um pacote por vez; nada além de RDV e boletim foi a disco ({fv(sum(os.path.getsize(TRAB + "/pacotes/" + a_) for a_ in os.listdir(TRAB + "/pacotes") if a_.endswith(".zip")) / 1e6, 0, False)} MB nos seis pacotes guardados).',
        f'Validade (D7): a regra do mínimo de testemunhas por município escolheu 1, isto é, todos os {val["principal_AC_TO"]["municipios_na_decisao"]} municípios; igual à leitura sem mínimo. Passa do limiar de 0,9 ({fv(val["principal_AC_TO"]["correlacao_que_decide"], 3, False)}), mas fica abaixo do percentil 5 de um termômetro perfeito ({fv(val["principal_AC_TO"]["grade"][0]["termometro_perfeito_p5"], 3, False)}); o TO sozinho dá {fv(val["por_uf"]["TO"]["leitura_sem_minimo"]["observado"], 3, False)}.',
        'Veredito (D9): Theta abaixo de -0,020 não tem cláusula no registro; ficou INCONCLUSIVO pela letra e foi lido no espelho.',
        f'Calibração (D11): "enxerga o plantado" foi definido antes como o aumento de Theta igual ao da fórmula e de pelo menos 2,5 erros totais; cumpre ({fv(cal["aumento_em_erros_totais_com_sis_0015"], 2, False)} erros). Se "enxergar" for lido como o critério de SINAL disparar no dado com o plantio, NÃO cumpre (Theta fica em {fv(cal["bateria_com_plantio"]["theta"])}) e o veredito seria SEM PODER. As duas leituras levam à mesma conclusão prática: o teste não decide.',
        f'Tercis de escolaridade: {ab["por_tercil_escolaridade"]["secoes_sem_perfil"]} seções sem perfil ficaram fora dessa leitura.',
        'Descritivo de ES, DF, AM e RN: só as seções da amostra aleatória nova (175 seções). Correção ao desenho: no ES o 22 também não tem voto nominal de governador no 1º turno.',
        'Placebo AL 2022: sem tercis (não há perfil de 2022 em disco); boletim de 2022 não decodificado; o leitor de RDV foi adaptado ao formato de 2022 (o nó das eleições tem outro rótulo), antes da etapa 1.',
        'Exploratório (seção 15): tudo o que está lá foi feito depois de ver Theta e não decide nada.']
    L['exploratorio_leitura'] = [
        'E7, placebo AL 2022, as mesmas contas: nulos com 22 no 2º turno por voto do governador eliminado 14 ' + f'{fv(e7["regressao"]["g22_2t"]["por voto do governador eliminado 14 no 1º turno"]["coef"])} (ep {fv(e7["regressao"]["g22_2t"]["por voto do governador eliminado 14 no 1º turno"]["ep"], 4, False)}); nulos com 13, {fv(e7["regressao"]["g13_2t"]["por voto do governador eliminado 14 no 1º turno"]["coef"])} (ep {fv(e7["regressao"]["g13_2t"]["por voto do governador eliminado 14 no 1º turno"]["ep"], 4, False)}). '
        + 'Theta por décimo da parcela de governador eliminado: ' + '; '.join(f'{fpc(l["parcela_media"])}: {fv(l["theta"], 3)}' for l in e7['decimos']) + f'. Reta até zero: {fv(e7["reta"]["theta_na_parcela_zero"])} (ep {fv(e7["reta"]["ep"], 4, False)}); inclinação {fv(e7["reta"]["inclinacao"], 2)} (ep {fv(e7["reta"]["ep_inclinacao"], 2, False)}). '
        + f'Em AL 2022 o Theta positivo NÃO some onde há pouco voto de governador eliminado: ali o que muda entre os turnos é a taxa do 13, que cai mais (vezes {fv(pla["taxas_de_erro_de_tela"]["multiplicador_r13"], 2, False)}) que a do 22 (vezes {fv(pla["taxas_de_erro_de_tela"]["multiplicador_r22"], 2, False)}). Lido ao pé da letra seriam {fpc(e7["traducao_literal"]["fracao_p"])} dos votos de Bolsonaro contados para Lula em AL, {fi(e7["traducao_literal"]["votos_trocados_no_pais_se_uniforme"])} votos se fosse igual no país.',
        'E8, de que lado era o eleitor de cada candidato a governador (correlação, por seção, entre a parcela do candidato e a parcela de Lula no 1º turno): ' + '; '.join(f'{rot}: ' + ', '.join(f'{c_} {fv(q_["correlacao_com_a_parcela_de_lula_1t"], 2)} ({fi(q_["votos_1t"])} votos)' for c_, q_ in dd.items()) for rot, dd in e8.items())
        + '. Em AL 2022 o eliminado 14 era o candidato do eleitorado de Bolsonaro e o finalista 15 o do eleitorado de Lula; no AC 2026 os dois finalistas (11 e 10) são neutros e os eliminados se dividem (40 do lado de Lula, 45 do lado de Flávio); no TO o 55 é neutro.',
        'Leitura do exploratório: a explicação "o lado que ficou sem candidato a governador continua anulando com o seu número" combina com o sinal por UF (AL 2022 positivo, AC e TO 2026 negativos) e com a inclinação dentro do TO, mas não com a inclinação dentro de AL 2022. O que os dados sustentam sem depender dela: a diferença entre turnos do termômetro muda com a eleição de governador em tamanho maior que o efeito procurado. O porquê fica em aberto.']
    grava('leitura.json', L)
    P('leitura gravada')


def relatorio():
    import ast, hashlib
    et1, val, ab, conf = le('etapa1.json'), le('validade.json'), le('aberto.json'), le('conferencia_2026.json')
    pla = le('placebo_AL_2022.json') if os.path.exists(f'{TRAB}/placebo_AL_2022.json') else None
    conf22 = le('conferencia_2022.json') if os.path.exists(f'{TRAB}/conferencia_2022.json') else None
    lei = le('leitura.json') if os.path.exists(f'{TRAB}/leitura.json') else {}
    expl = le('exploratorio_calculos.json') if os.path.exists(f'{TRAB}/exploratorio_calculos.json') else None
    src = open(RAIZ + '/scripts/analisar_R27_W3.py').read()
    doc = ast.get_docstring(ast.parse(src), clean=False)
    reg = le('registro_decisoes.json')
    man = {}
    for a in sorted(os.listdir(TRAB + '/pacotes')):
        if a.endswith('.manifesto.json'):
            man[a.replace('.manifesto.json', '')] = le('pacotes/' + a)
    pr = ab['principal']
    v015 = _veredito(ab, val, 0.015)
    sis_pl = max(0.015, abs(pla['principal']['theta'])) if pla else None
    vpl = _veredito(ab, val, sis_pl) if pla else None
    trad = dict(ab['traducao_em_votos'])
    L2u, R2u = pr['somas']['L2'], pr['somas']['R2']
    if pla:
        err = math.hypot(pr['ep'], sis_pl)
        trad['sis_placebo'] = {'erro_total': err, 'theta_menos_196_erros': _traduz(pr['theta'] - 1.96 * err, pr['P2'], R2u, L2u), 'theta_mais_196_erros': _traduz(pr['theta'] + 1.96 * err, pr['P2'], R2u, L2u)}
    clausulas = {'lista': ['principal', 'espelho', 'AC', 'TO', 'tercil baixa', 'tercil media', 'tercil alta', 'placebo 3', 'duas metades'], 'n': 9,
                 'sinais_que_o_acaso_daria_a_5_por_cento': 0.45}
    J = {'teste': 'R27_W3: testemunhas na tela de governador (D4-3), AC e TO',
         'registro': {'adendo': 'Adendo 27 (commit 2748895, 10/11/2026 00:16:42 UTC), Onda D-b; Adendo 30 (commit a7218fb)', 'criterio': 'registro/adendo27/desenho_D4_proposta.json, teste D4-3',
                      'docstring_sha256': hashlib.sha256(doc.encode()).hexdigest(), 'docstring_no_commit': '6677983 (10/11/2026 10:48:36 UTC), antes de qualquer conta com votos',
                      'decisoes_da_retomada_no_commit': '9a8dd54 (10/11/2026 11:07:41 UTC): bloco R1 a R10 e regra do veredito, antes da etapa 1 (11:27 UTC); R11 só com horário local (11:09 UTC)',
                      'decisoes_da_retomada': reg},
         'fonte': {'pacotes': man, 'endereco': URL},
         'conferencia_rdv_x_bweb_2026': conf, 'conferencia_rdv_x_base_2022': conf22,
         'etapa1': et1, 'validade_do_termometro': val, 'aberto': ab, 'placebo_AL_2022': pla,
         'veredito': {'so_com_2026_erro_sistematico_minimo_0015': v015, 'com_placebo_AL_2022': vpl, 'erro_sistematico_com_placebo': sis_pl},
         'veredito_por_parte': {'parte1_a_favor_de_lula': {'so_2026': v015['veredito'], 'com_placebo': vpl['veredito'] if vpl else None, 'leitura_alternativa_da_calibracao': 'SEM PODER (o critério de SINAL não dispara no dado com a troca de 3,57% plantada)'},
                                'parte2_espelho_a_favor_de_flavio': {'so_2026': 'SINAL' if v015['criterio_de_sinal_no_espelho']['sinal'] else 'sem sinal', 'com_placebo': ('SINAL' if vpl['criterio_de_sinal_no_espelho']['sinal'] else 'sem sinal') if vpl else None,
                                                                    'conta_como_indicio': False},
                                'parte3_poder_etapa1': et1['veredito_da_etapa1'], 'parte3_enxerga_o_plantado_D11': ab['enxerga_o_plantado'], 'parte4_validade_aprovada': val['aprovado']},
         'traducao_em_votos_de_margem': trad, 'contagem_de_clausulas': clausulas,
         'decisoes_retomada_texto': DECISOES_RETOMADA, 'decisoes_retomada_2_texto': DECISOES_RETOMADA_2, 'leitura_escrita_depois_de_ver_o_resultado': lei, 'exploratorio_depois_de_ver_o_resultado': expl}
    with open(RAIZ + '/resultados/R27_W3_testemunhas_governador.json', 'w') as f:
        json.dump(J, f, ensure_ascii=False, indent=1)

    # ---------------- texto
    T = []
    A = T.append
    A('R27 W3: TESTEMUNHAS NA TELA DE GOVERNADOR, AC E TO (Adendo 27, teste D4-3)')
    A('')
    A('Registro: PRE-REGISTRO-2026-10-26.md, Adendo 27 (commit 2748895, 10/11/2026 00:16:42 UTC), Onda D-b, e Adendo 30 (commit a7218fb). Critério: registro/adendo27/desenho_D4_proposta.json, teste D4-3, à letra. '
      f'Decisões que o registro não fixa: docstring de scripts/analisar_R27_W3.py, no commit 6677983 (10:48:36 UTC) antes de qualquer conta com votos (SHA-256 {reg["docstring_sha256"][:16]}...), e o bloco de decisões da retomada, '
      f'gravado às {reg["gravado_em_utc"][11:16]} UTC (SHA-256 {reg["decisoes_retomada_sha256"][:16]}...; está no commit 9a8dd54, de 11:07:41 UTC), também antes da etapa 1 (11:27 UTC).')
    A('A ideia: parte dos eleitores digita na tela de governador o número do seu presidenciável. Em AC e TO, 13 e 22 não são candidatos a governador em nenhum turno, e isso vira nulo de governador com os dígitos gravados no RDV. '
      'É uma amostra da intenção presidencial que não passa pela contagem de presidente. W = parcela de 13 entre as testemunhas (13 + 22); P = parcela oficial de Lula entre Lula + Flávio nas mesmas seções. '
      'Theta = [logit P do 2º turno menos logit P do 1º] menos [logit W do 2º menos logit W do 1º]. Troca de votos de Flávio para Lula só na contagem de presidente do 2º turno dá Theta positivo: '
      f'{fv(ab["poder"]["formula_p_0357"])} para a troca de 3,57% que vira o resultado, nessas seções (R/L = {fv(ab["poder"]["R_sobre_L_2t_universo"], 3, False)}).')
    A('')
    A('VEREDITO PELA LETRA')
    nums = (f'Theta = {fv(pr["theta"])} (erro-padrão {fv(pr["ep"], 4, False)}; n = {fi(pr["n_secoes"])} seções em {fi(pr["n_locais"])} locais; {fi(pr["somas"]["a1"] + pr["somas"]["b1"])} testemunhas no 1º turno e {fi(pr["somas"]["a2"] + pr["somas"]["b2"])} no 2º)')
    A(f'  Parte 1, alteração a favor de Lula (o critério registrado): INCONCLUSIVO. {nums}. O sinal é o CONTRÁRIO do previsto pela tese: a troca que vira o resultado daria {fv(ab["poder"]["formula_p_0357"])}.')
    A(f'    só com 2026 (erro sistemático mínimo de 0,015, sem usar outro ano; erro total {fv(v015["erro_total"], 4, False)}): {v015["veredito"]}. Motivo: ' + '; '.join(v015['motivos']) + '.')
    if vpl:
        A(f'    com o placebo AL 2022 (Theta do placebo {fv(pla["principal"]["theta"])}, ep {fv(pla["principal"]["ep"], 4, False)}; erro sistemático {fv(sis_pl, 4, False)}; erro total {fv(vpl["erro_total"], 4, False)}): {vpl["veredito"]}. Motivo: ' + '; '.join(vpl['motivos']) + '.')
    else:
        A('    placebo AL 2022: não rodado; vale o erro sistemático mínimo de 0,015.')
    ce15 = v015['criterio_de_sinal_no_espelho']
    A(f'  Parte 2, espelho (a mesma regra a favor de Flávio): {"SINAL" if ce15["sinal"] else "sem sinal"} pela letra só com 2026 (menos Theta = {fv(ce15["theta"])}, {fv(ce15["theta_sobre_erro_total"], 2, False)} erros totais, mesmo sinal em AC, TO e nos três tercis)'
      + (f'; {"SINAL" if vpl["criterio_de_sinal_no_espelho"]["sinal"] else "sem sinal"} com o placebo ({fv(vpl["criterio_de_sinal_no_espelho"]["theta_sobre_erro_total"], 2, False)} erro total).' if vpl else '.')
      + ' Não conta como indício de fraude a favor de Flávio: ver a seção 13.')
    calp = ab['calibracao_plantio']['R_para_L']['p_0.0357']
    A(f'  Parte 3, poder e calibração: a etapa 1 passa (erro-padrão {fv(et1["recortes"]["AC+TO"]["erro_padrao_de_theta"], 4, False)}, limite 0,025). A troca de 3,57% plantada aumenta Theta em {fv(calp["aumento_de_theta"])} ({fpc(calp["razao_aumento_formula"])} da fórmula; {fv(calp["aumento_em_erros_totais_com_sis_0015"], 2, False)} erros totais): pela regra escrita antes (D11), o teste '
      f'{"enxerga" if ab["enxerga_o_plantado"] else "NÃO enxerga"} o plantado. Mas o critério de SINAL aplicado ao dado com o plantio {"dispara" if calp["criterio_de_sinal_no_dado_com_plantio_sis_0015"]["sinal"] else "NÃO dispara"} (Theta fica em {fv(calp["bateria_com_plantio"]["theta"])}): se "enxergar" for lido assim, o veredito da parte 1 é SEM PODER. As duas leituras dão a mesma conclusão prática.')
    A(f'  Parte 4, validade do termômetro no 1º turno: {"APROVADO" if val["aprovado"] else "REPROVADO"} (correlação de postos {fv(val["principal_AC_TO"]["correlacao_que_decide"], 3, False)} em {val["principal_AC_TO"]["municipios_na_decisao"]} municípios; limiar 0,9).')
    if lei.get('uma_frase'):
        A('  Em uma frase: ' + lei['uma_frase'])
    A('')
    A('1. FONTE E CONFERÊNCIA DOS RDV CONTRA O BWEB')
    for nome, m in man.items():
        A(f'  {nome}: pacote de {fi(m["tamanho_pacote"])} bytes ({m["cabecalhos"].get("Last-Modified")}), {fi(m["membros_no_pacote"])} membros; guardados {fi(m["guardados"])} (RDV e boletim), CRC de cada um conferido; '
          f'{m["pedidos_de_fluxo"]} pedido(s) de fluxo, {m["quedas"]} queda(s).')
    for uf in UFS:
        for t in ('1', '2'):
            q = conf['ufs'][uf][t]; c = q['contagens']
            A(f'  {uf}, {t}º turno: {fi(q["secoes_na_base"])} seções na base, {fi(q["rdv_no_pacote"])} RDV no pacote, {q["erros_de_leitura"]} erros de leitura. Presidente (13, 22, demais, brancos, nulos) igual à base em '
              f'{fi(c.get("pres_igual_base", 0))}; governador (brancos, nulos, nominais) igual em {fi(c.get("gov_igual_base", 0))}; boletim do pacote igual à base em {fi(c.get("boletim_igual_base", 0))} de {fi(c.get("com_boletim", 0))}. '
              f'Direto contra o zip do bweb, candidato a candidato: presidente igual em {fi(c.get("bweb_igual_pres", 0))}, governador igual em {fi(c.get("bweb_igual_gov", 0))}. '
              f'Candidatos a governador: {", ".join(q["candidatos_governador_bweb"])}. Votos nominais de governador em 13 ou 22: {q["votos_nominais_de_governador_em_13_ou_22_no_rdv"]}. '
              f'Nulos de governador com dígitos: {fi(c.get("nulos_gov_com_digitos", 0))} (todos com {", ".join(q["tamanho_dos_digitos_dos_nulos_de_governador"])} dígitos); sem dígitos: {fi(c.get("nulos_gov_sem_digitos", 0))}.')
        u = conf['ufs'][uf]['universo']
        A(f'  {uf}: universo (D2) = {fi(u["no_universo_D2"])} de {fi(u["secoes_nos_dois_turnos_da_base"])} seções.' + (f' Fora: {json.dumps(u["fora"], ensure_ascii=False)}.' if u['fora'] else ''))
    A('  Limite: RDV, boletim e bweb saem do mesmo programa da urna. A igualdade fecha alteração depois da urna nessas seções e não pesa contra a hipótese de programa adulterado na origem. O que o teste tem de próprio é comparar dois cargos dentro do mesmo RDV.')
    A('')
    A('2. ETAPA 1 (sem abrir Theta): NÚMERO DE TESTEMUNHAS E ERRO-PADRÃO')
    for nome, q in et1['recortes'].items():
        A(f'  {nome}: {fi(q["n_secoes"])} seções, {fi(q["n_locais"])} locais; testemunhas (13 + 22) {fi(q["testemunhas_1t"])} no 1º turno ({fv(q["testemunhas_por_100_votantes_1t"], 2, False)} por 100 votantes) e {fi(q["testemunhas_2t"])} no 2º '
          f'({fv(q["testemunhas_por_100_votantes_2t"], 2, False)} por 100); erro-padrão de Theta {fv(q["erro_padrao_de_theta"], 4, False)} (bootstrap de locais, 2.000 réplicas).')
    A(f'  Decisão da etapa 1, gravada às {et1["gravado_em_utc"][11:16]} UTC: {et1["veredito_da_etapa1"]}. Erro total com o sistemático mínimo: {fv(et1["erro_total_com_sistematico_minimo_0015"], 4, False)}.')
    A('')
    A('3. VALIDADE DO TERMÔMETRO NO 1º TURNO (antes de abrir)')
    vp = val['principal_AC_TO']
    A(f'  Regra (D7): correlação de postos, entre municípios, de W do 1º turno contra P oficial do 1º turno; limiar 0,9. Mínimo de testemunhas por município escolhido pela simulação do termômetro perfeito: {vp["n_min_escolhido"]}. '
      f'Correlação que decide: {fv(vp["correlacao_que_decide"], 3, False)} em {vp["municipios_na_decisao"]} municípios: {"APROVADO" if vp["aprovado"] else "REPROVADO"}.')
    for g in vp['grade']:
        if 'observado' in g:
            A(f'    mínimo {g["n_min"]}: {g["municipios"]} municípios; observado {fv(g["observado"], 3, False)}; termômetro perfeito: mediana {fv(g["termometro_perfeito_mediana"], 3, False)}, percentil 5 {fv(g["termometro_perfeito_p5"], 3, False)}, passa de 0,9 em {fpc(g["termometro_perfeito_fracao_acima_de_09"])} dos sorteios.')
        else:
            A(f'    mínimo {g["n_min"]}: {g["municipios"]} municípios (menos de 10, fora da grade).')
    ls = vp['leitura_sem_minimo']
    A(f'  Leitura sem mínimo (todos os {ls["municipios"]} municípios com testemunha): {fv(ls["observado"], 3, False)}; teto de ruído (termômetro perfeito) mediana {fv(ls["teto_de_ruido_mediana"], 3, False)}, percentil 5 {fv(ls["teto_de_ruido_p5"], 3, False)}. '
      f'Por essa leitura o termômetro {"passaria" if ls["aprovaria_pelo_limiar_09"] else "NÃO passaria"} de 0,9' + ('' if ls['aprovaria_pelo_limiar_09'] else ' e o veredito seria INCONCLUSIVO; nem um termômetro perfeito passaria, pelo ruído dos municípios pequenos') + '.')
    for u in UFS:
        q = val['por_uf'][u]
        A(f'  {u}: sem mínimo {fv(q["leitura_sem_minimo"]["observado"], 3, False)} em {q["leitura_sem_minimo"]["municipios"]} municípios (teto de ruído {fv(q["leitura_sem_minimo"]["teto_de_ruido_mediana"], 3, False)}); '
          f'nível no 1º turno: W = {fv(val["nivel_1t"][u]["W1"], 4, False)}, P = {fv(val["nivel_1t"][u]["P1"], 4, False)}; testemunhas de eliminados {fi(val["nivel_1t"][u]["testemunhas_eliminados"])}.')
    ce = val['celulas_municipio_x_numero']; pe = val['parcelas_com_eliminados_no_denominador']
    A(f'  Células município x número (13, 22 e eliminados): {fi(ce["n_celulas"])} células, correlação de postos {fv(ce["spearman"], 3, False)}. Com os eliminados no denominador: parcela do 13 {fv(pe["parcela_13"], 3, False)}, do 22 {fv(pe["parcela_22"], 3, False)}, dos eliminados {fv(pe["parcela_eliminados"], 3, False)}.')
    for u in UFS:
        comp = val['composicao_por_uf'][u]
        A(f'  Composição no {u} (testemunhas contra oficial, 1º turno): ' + '; '.join(f'{nm} {fpc(q["parcela_entre_testemunhas"])} contra {fpc(q["parcela_oficial"])}' for nm, q in comp.items() if not nm.startswith('_')) + f'. Postos entre números: {fv(comp["_postos_entre_numeros"], 3, False)}.')
    A('')
    A('4. THETA (aberto depois da etapa 1 e da validade)')
    def lin(nome, q):
        A(f'  {nome}: Theta {fv(q["theta"])} (ep {fv(q["ep"], 4, False)}; {fv(q["theta"] / q["ep"], 2)} ep); P {fv(q["P1"], 4, False)} para {fv(q["P2"], 4, False)} (logit {fv(q["dlogit_P"])}); '
          f'W {fv(q["W1"], 4, False)} para {fv(q["W2"], 4, False)} (logit {fv(q["dlogit_W"])}); testemunhas 13/22: {fi(q["somas"]["a1"])}/{fi(q["somas"]["b1"])} no 1º turno, {fi(q["somas"]["a2"])}/{fi(q["somas"]["b2"])} no 2º; {fi(q["n_secoes"])} seções.')
    lin('AC + TO', pr)
    A(f'    intervalo de 95% por percentis do bootstrap: {fv(pr["ic95_percentis"][0])} a {fv(pr["ic95_percentis"][1])}.')
    for u in UFS:
        lin(u, ab['por_uf'][u])
    for nome in ('baixa', 'media', 'alta'):
        lin(f'tercil de escolaridade {nome}', ab['por_tercil_escolaridade'][nome])
    A('  Sensibilidade (tercis pela parcela com superior completo): ' + '; '.join(f'{nome} {fv(q["theta"])} (ep {fv(q["ep"], 4, False)})' for nome, q in ab['por_tercil_superior_sensibilidade'].items()) + '.')
    sr = ab['sensibilidade_com_reprovadas_D2']
    A('  Sensibilidade com as seções reprovadas na conferência: ' + (sr['nota'] if 'nota' in sr else f'Theta {fv(sr["theta"])} (ep {fv(sr["ep"], 4, False)}), {fi(sr["n_secoes"])} seções.'))
    A('')
    A('5. CRITÉRIOS, UM A UM')
    for rot, v in (('sistemático 0,015', v015),) + ((('sistemático do placebo', vpl),) if vpl else ()):
        cs, cesp = v['criterio_de_sinal'], v['criterio_de_sinal_no_espelho']
        A(f'  Com {rot}: erro total {fv(v["erro_total"], 4, False)}. SINAL pede Theta >= 0,045 ({"sim" if cs["tamanho_ok"] else "não"}), Theta >= 2,5 erros totais ({fv(cs["theta_sobre_erro_total"], 2)}: {"sim" if cs["razao_ok"] else "não"}) e mesmo sinal em AC, TO e nos três tercis ({"sim" if cs["mesmo_sinal_ufs_e_tercis"] else "não"}). '
          f'SEM SINAL pede |Theta| <= 0,020 ({"sim" if abs(v["theta"]) <= 0.020 else "não"}) e erro total <= 0,025 ({"sim" if v["erro_total"] <= 0.025 else "não"}). Veredito: {v["veredito"]}. '
          f'Espelho: -Theta >= 0,045 ({"sim" if cesp["tamanho_ok"] else "não"}), >= 2,5 erros ({fv(cesp["theta_sobre_erro_total"], 2)}: {"sim" if cesp["razao_ok"] else "não"}), mesmo sinal ({"sim" if cesp["mesmo_sinal_ufs_e_tercis"] else "não"}): {"SINAL no espelho" if cesp["sinal"] else "sem sinal no espelho"}.')
    A('')
    A('6. CALIBRAÇÃO POR EFEITO PLANTADO NOS DADOS DE 2026')
    for lado, rot in (('R_para_L', 'troca de votos de Flávio para Lula, só na contagem oficial do 2º turno'), ('L_para_R', 'espelho: de Lula para Flávio')):
        for pk, q in ab['calibracao_plantio'][lado].items():
            cs = q['criterio_de_sinal_no_dado_com_plantio_sis_0015']
            A(f'  {rot}, p = {fpc(q["p"], 2)} ({fi(q["votos_movidos"])} votos): fórmula {fv(q["formula"])}; Theta mudou {fv(q["aumento_de_theta"])} ({fpc(q["razao_aumento_formula"])} da fórmula; {fv(q["aumento_em_erros_totais_com_sis_0015"], 2, False)} erros totais); '
              f'200 plantios: média {fv(q["duzentos_plantios_media"])}, desvio {fv(q["duzentos_plantios_desvio"], 4, False)}. ' + (f'Enxerga pelo D11 (que decide com 3,57%): {"sim" if q["enxerga"] else "não"}. ' if abs(q["p"] - 0.0357) < 1e-9 else '') + f'Critério de SINAL{" do espelho" if lado == "L_para_R" else ""} no dado com o plantio, do jeito que sai: {"SINAL" if cs["sinal"] else "não dá sinal"} ({"menos " if lado == "L_para_R" else ""}Theta {fv(cs["theta"])}, {fv(cs["theta_sobre_erro_total"], 2)} erros).')
    A('  Aviso: o espelho já dá SINAL pela letra sem plantio nenhum (seção 5); o plantio do espelho só confirma que a conta responde nos dois sentidos.')
    po = ab['poder']
    A(f'  Poder: com erro total de {fv(po["erro_total_sis_0015"], 4, False)}, o SINAL pede Theta de {fv(po["theta_minimo_para_sinal"], 4, False)} ou mais; a menor troca uniforme que alcança isso é p = {fpc(po["menor_p_que_alcanca"], 2)} dos votos de Flávio '
      f'({fpc(po["menor_p_em_fracao_da_margem_se_uniforme_no_pais"])} da margem, se fosse igual no país). A troca que vira o resultado (3,57%) daria {fv(po["formula_p_0357"])}; a de 1,8%, {fv(po["formula_p_018"])}.')
    ino = ab['explicacao_inocente_plantada']
    for dk, q in ino['conversao_dos_eliminados'].items():
        A(f'  Explicação inocente plantada (i), conversão diferente dos eliminados, {dk.replace("delta_", "delta = ").replace(".", ",")}: {fi(q["testemunhas_movidas_media"])} testemunhas do 2º turno passam de 13 para 22; Theta sobe {fv(q["aumento_medio_de_theta"])} '
          f'(valor direto {fv(q["valor_direto"])}; fórmula do intervalo {fv(q["formula_do_intervalo_D13"])}): {"passa" if q["passa"] else "não passa"}. O teste NÃO separa isso de troca na contagem: é o erro sistemático.')
    q = ino['queda_geral_da_propensao']
    A(f'  Explicação inocente plantada (ii), queda geral da propensão ao erro (metade das testemunhas do 2º turno retirada ao acaso): Theta muda {fv(q["mudanca_media_de_theta"])} em média (desvio entre sorteios {fv(q["desvio_entre_sorteios"], 4, False)}): {"passa" if q["passa"] else "não passa"}; cancela, como previsto.')
    q = ab['duas_metades']
    A(f'  Duas metades aleatórias das seções (200 divisões): {fpc(q["fracao_com_z_acima_de_2"])} com diferença acima de 2 erros (limite 10%); desvio das diferenças {fv(q["desvio_das_diferencas"], 4, False)} contra erro previsto {fv(q["erro_medio_da_diferenca"], 4, False)}: {"passa" if q["passa"] else "não passa"}.')
    A('')
    A('7. PLACEBOS')
    if pla:
        q = pla['principal']; tx = pla['taxas_de_erro_de_tela']
        A(f'  (1) AL 2022, dois turnos, mesma conta: Theta {fv(q["theta"])} (ep {fv(q["ep"], 4, False)}; {fv(q["theta"] / q["ep"], 2)} ep); {fi(q["n_secoes"])} seções, {fi(q["n_locais"])} locais; testemunhas 13/22: {fi(q["somas"]["a1"])}/{fi(q["somas"]["b1"])} no 1º turno e {fi(q["somas"]["a2"])}/{fi(q["somas"]["b2"])} no 2º. '
          f'P {fv(q["P1"], 4, False)} para {fv(q["P2"], 4, False)}; W {fv(q["W1"], 4, False)} para {fv(q["W2"], 4, False)}. Taxa de erro de tela por mil eleitores do lado: 13 de {fv(1000 * tx["r13_1t"], 2, False)} para {fv(1000 * tx["r13_2t"], 2, False)}; 22 de {fv(1000 * tx["r22_1t"], 2, False)} para {fv(1000 * tx["r22_2t"], 2, False)}.')
        if conf22:
            for t in ('1', '2'):
                c22 = conf22['ufs']['AL'][t]
                A(f'      conferência AL 2022, {t}º turno: {fi(c22["rdv_no_pacote"])} RDV, {c22["erros_de_leitura"]} erros de leitura, presidente igual à base em {fi(c22["contagens"].get("pres_igual_base", 0))} de {fi(c22["secoes_na_base"])}; governador igual em {fi(c22["contagens"].get("gov_igual_base", 0))}; nominais de governador em 13 ou 22: {c22["votos_nominais_de_governador_em_13_ou_22_no_rdv"]}; candidatos a governador no RDV: {", ".join(c22["candidatos_governador_rdv"])}.')
        vq = pla['validade_1t_por_municipio']
        A(f'      validade em AL 2022 (mesma regra): mínimo {vq["n_min_escolhido"]}, correlação {fv(vq["correlacao_que_decide"], 3, False)} em {vq["municipios_na_decisao"]} municípios; sem mínimo {fv(vq["leitura_sem_minimo"]["observado"], 3, False)}.')
        A(f'      Aviso: o Léo suspeita também de 2022. Se 2022 tivesse a mesma alteração, o placebo seria positivo e inflaria o erro; por isso o veredito sai também só com 2026.')
    else:
        A('  (1) AL 2022: não rodado.')
    A('  (2) W contra P por município no 1º turno de 2026, em nível: é a validade da seção 3.')
    q = ab['placebo3_par_de_eliminados']
    for nome in ('AC+TO', 'AC', 'TO'):
        z = q[nome]
        A(f'  (3) par de eliminados 70 e 14 no 1º turno, {nome}: {fi(z["testemunhas_70"])} e {fi(z["testemunhas_14"])} testemunhas; parcela do 70 entre as duas {fpc(z["parcela_70_testemunhas"]) if z["parcela_70_testemunhas"] is not None else "n/d"} contra {fpc(z["parcela_70_oficial"])} oficial; diferença de logits {fv(z["diferenca_de_logits"])} (ep {fv(z["ep"], 4, False)}).')
    A(f'      por município com 30 ou mais testemunhas do par: {q["por_municipio"]["municipios_com_30_ou_mais"]} municípios, correlação de postos {fv(q["por_municipio"]["spearman"], 3, False)}. Sem limiar no registro: descritivo.')
    A('')
    A('8. LEITURAS SECUNDÁRIAS')
    ie = ab['intervalo_dos_eliminados']; dd = ie['deslocamento_de_theta']
    A(f'  Intervalo dos eliminados: no 1º turno, {fi(ie["testemunhas_de_eliminados_1t"])} testemunhas digitaram número de eliminado ({fpc(ie["parcela_de_eliminados_entre_testemunhas_1t"])} das testemunhas). Se entre os que erram a tela a parcela dos eliminados que foi para Lula fosse 40% em vez de 50%, Theta subiria {fv(dd["cw_0,40"])}; 25%, {fv(dd["cw_0,25"])}; 60%, {fv(dd["cw_0,60"])}; 75%, {fv(dd["cw_0,75"])}; extremos {fv(dd["cw_0"])} (nenhum para Lula) e {fv(dd["cw_1"])} (todos). É limite, não estimativa.')
    q = ab['oficial_pesado_pelas_testemunhas']
    A('  Lado oficial pesado pelas testemunhas (D19, não decide): ' + '; '.join(f'{nome} {fv(z["theta"])} (ep {fv(z["ep"], 4, False)})' for nome, z in q.items()) + '.')
    for nome, tx in ab['taxas_de_erro_de_tela'].items():
        A(f'  Taxas de erro de tela, {nome} (D20, não decide), por mil eleitores do lado: 13 de {fv(1000 * tx["r13_1t"], 2, False)} para {fv(1000 * tx["r13_2t"], 2, False)} (vezes {fv(tx["multiplicador_r13"], 3, False)}); 22 de {fv(1000 * tx["r22_1t"], 2, False)} para {fv(1000 * tx["r22_2t"], 2, False)} (vezes {fv(tx["multiplicador_r22"], 3, False)}). Theta = ln do multiplicador do 22 menos ln do multiplicador do 13.')
    q = ab['por_tercil_da_parcela_de_governador_eliminado']
    A('  Theta por tercil da parcela dos votos de governador do 1º turno dada a candidatos eliminados na seção (D20): ' + '; '.join(f'{nome} {fv(z["theta"])} (ep {fv(z["ep"], 4, False)}; parcela de {fpc(z["faixa_da_parcela"][0])} a {fpc(z["faixa_da_parcela"][1])})' for nome, z in q.items() if isinstance(z, dict)) + '.')
    q = ab['por_tercil_de_forca_de_lula_1t']
    A('  Theta por tercil da força de Lula no 1º turno da seção (R11, não decide): ' + '; '.join(f'{nome.replace("_", " ")} {fv(q[nome]["theta"])} (ep {fv(q[nome]["ep"], 4, False)}; R/L {fv(q[nome]["R_sobre_L_2t"], 2, False)}; a troca de 3,57% daria {fv(q[nome]["formula_p_0357"])})' for nome in ('lula_fraco', 'meio', 'lula_forte'))
      + f'. Diferença entre fraco e forte: {fv(q["diferenca_fraco_menos_forte"]["observada"])} (ep {fv(q["diferenca_fraco_menos_forte"]["ep"], 4, False)}); a troca proporcional de 3,57% preveria {fv(q["diferenca_fraco_menos_forte"]["prevista_pela_formula_p_0357"])}.')
    for u in UFS:
        g = ab['governador_descritivo'][u]
        dz = lambda dd, n_=8: ', '.join(f'{c_}: {fi(q_)}' for c_, q_ in list(dd.items())[:n_])
        A(f'  Governador no {u}: 1º turno, comparecimento {fi(g["1t"]["comparecimento"])}, nominais por candidato ({dz(g["1t"]["nominais_por_candidato"])}), brancos {fi(g["1t"]["brancos"])}, nulos {fi(g["1t"]["nulos"])}, dígitos mais digitados nos nulos ({dz(g["1t"]["nulos_com_digitos_mais_frequentes"])}); '
          f'2º turno, comparecimento {fi(g["2t"]["comparecimento"])}, nominais ({dz(g["2t"]["nominais_por_candidato"])}), brancos {fi(g["2t"]["brancos"])}, nulos {fi(g["2t"]["nulos"])}, dígitos ({dz(g["2t"]["nulos_com_digitos_mais_frequentes"])}).')
    A('')
    A('9. TRADUÇÃO EM VOTOS DE MARGEM')
    tp = trad['ponto']
    A(f'  Theta medido em AC e TO equivale a {fpc(abs(tp["fracao_p"]), 2)} dos votos verdadeiros contados para o outro lado, no sentido {tp["sentido"]} ({fi(abs(tp["votos_trocados_em_AC_e_TO"]))} votos em AC e TO). Se a mesma fração valesse no país (suposição, não medida): {fi(abs(tp["votos_trocados_no_pais_se_uniforme"]))} votos, efeito de {fi(tp["efeito_na_margem_no_pais"])} na margem ({fpc(tp["fracao_da_margem"])} de 4.430.191).')
    for rot, kk in (('sistemático 0,015', 'sis_0015'), ('sistemático do placebo', 'sis_placebo')):
        if kk in trad:
            z = trad[kk]
            A(f'  Intervalo de Theta mais ou menos 1,96 erro total ({rot}; erro total {fv(z["erro_total"], 4, False)}): Theta de {fv(z["theta_menos_196_erros"]["theta"])} a {fv(z["theta_mais_196_erros"]["theta"])}; efeito na margem, se uniforme no país, de {fi(z["theta_menos_196_erros"]["efeito_na_margem_no_pais"])} a {fi(z["theta_mais_196_erros"]["efeito_na_margem_no_pais"])} ({fpc(z["theta_menos_196_erros"]["fracao_da_margem"])} a {fpc(z["theta_mais_196_erros"]["fracao_da_margem"])} da margem).')
    A(f'  Referência: a troca que vira o resultado (3,57% dos votos de Flávio, 100% da margem) daria Theta de {fv(trad["referencia_troca_que_vira"]["theta_previsto_no_universo"])} nessas seções.')
    A('')
    A('10. SÓ DESCRITIVO: ES, DF, AM E RN (seções da amostra aleatória nova; sem veredito)')
    de = ab['descritivo_ES_DF_AM_RN_amostra']
    if 'erro' in de:
        A('  não rodado: ' + de['erro'])
    else:
        for uf, q in de.items():
            partes = []
            for t in ('1t', '2t'):
                z = q[t]
                p_ = [f'{t}: L {fi(z["L"])}, R {fi(z["R"])}']
                for nm, lado in (('13', 'L'), ('22', 'R')):
                    if z.get('g' + nm) is not None:
                        p_.append(f'nulos de governador com {nm}: {fi(z["g" + nm])} ({fv(z[f"g{nm}_por_mil_votos_de_{lado}"], 2, False)} por mil votos do lado)')
                    else:
                        p_.append(f'{nm} é candidato a governador (ou não houve disputa): não serve')
                if z.get('W') is not None:
                    p_.append(f'W {fv(z["W"], 4, False)} contra P {fv(z["P"], 4, False)}')
                partes.append(', '.join(p_))
            A(f'  {uf} ({q["secoes"]} seções): ' + ' | '.join(partes) + '.')
        mult = []
        for uf, q in de.items():
            for nm, lado in (('13', 'L'), ('22', 'R')):
                a1_, a2_ = q['1t'].get('g' + nm), q['2t'].get('g' + nm)
                if a1_ and a2_:
                    m_ = (a2_ / q['2t'][lado]) / (a1_ / q['1t'][lado])
                    mult.append(f'{uf}, {nm}: vezes {fv(m_, 2, False)} (ln {fv(math.log(m_), 2)}, erro de contagem {fv(math.sqrt(1 / a1_ + 1 / a2_), 2, False)})')
        A('  Multiplicador da taxa por eleitor do lado, do 1º para o 2º turno, onde o número é inválido nos dois turnos: ' + '; '.join(mult) + f'. Em AC e TO: 13 vezes {fv(ab["taxas_de_erro_de_tela"]["AC+TO"]["multiplicador_r13"], 2, False)}, 22 vezes {fv(ab["taxas_de_erro_de_tela"]["AC+TO"]["multiplicador_r22"], 2, False)}. A taxa cai entre os turnos em toda parte; o quanto cai muda de UF para UF.')
    A('')
    if lei:
        for tit, kk in (('11. O QUE PESA A FAVOR DA TESE', 'a_favor'), ('12. O QUE PESA CONTRA A TESE', 'contra'), ('13. O QUE ISSO SIGNIFICA', 'significa'), ('14. PISTAS', 'pistas')):
            if lei.get(kk):
                A(tit + ' (leitura escrita depois de ver o resultado)')
                for x in lei[kk]:
                    A('  ' + x)
                A('')
    if expl:
        A('15. EXPLORATÓRIO (feito depois de ver o resultado; não decide nada)')
        A('  Pergunta: o que move o termômetro entre os turnos, a disputa de governador ou a contagem de presidente?')
        e3 = expl['E3_quanto_basta']
        A(f'  E3, quanto basta: Theta seria zero com {fi(e3["excesso_de_13"])} nulos de governador com 13 a menos no 2º turno ({fv(e3["excesso_de_13_por_cento_dos_votos_de_lula_2t"], 2, False)}% dos votos de Lula; AC {fi(e3["por_uf"]["AC"]["excesso_de_13"])}, TO {fi(e3["por_uf"]["TO"]["excesso_de_13"])}) '
          f'ou com {fi(e3["falta_de_22"])} com 22 a mais ({fv(e3["falta_de_22_por_cento_dos_votos_de_flavio_2t"], 2, False)}% dos votos de Flávio). Votos dados no 1º turno a candidatos a governador eliminados: '
          + '; '.join(f'{u} {fi(sum(e3["por_uf"][u]["votos_de_governador_eliminado_1t"].values()))} (' + ', '.join(f'{c_}: {fi(q_)}' for c_, q_ in sorted(e3["por_uf"][u]["votos_de_governador_eliminado_1t"].items(), key=lambda kv: -kv[1])[:3]) + ')' for u in UFS) + '.')
        for u in UFS:
            r1 = expl['E1_regressao_por_secao'][u]
            for alvo, rot in (('g13_2t', 'nulos com 13 no 2º turno'), ('g22_2t', 'nulos com 22 no 2º turno')):
                A(f'  E1, {u}, {rot}, por seção ({fi(r1["n_secoes"])} seções, erro por local): ' + '; '.join(f'{nm} {fv(q_["coef"])} (ep {fv(q_["ep"], 4, False)})' for nm, q_ in r1[alvo].items() if not nm.startswith('_'))
                  + '. Total que a regressão liga a cada eliminado: ' + ', '.join(f'{c_}: {fi(q_)}' for c_, q_ in r1[alvo]['_explicado_pelos_eliminados'].items()) + '.')
        ts = expl['theta_sem_a_parte_atribuida_aos_eliminados_de_governador']
        A(f'  Theta sem a parte que a regressão liga aos eleitores de governador eliminado (conta de modelo, ecológica): AC + TO {fv(ts["AC+TO"])}; AC {fv(ts["AC"])}; TO {fv(ts["TO"])}.')
        for u in UFS:
            e2 = expl['E2_decimos'][u]
            A(f'  E2, {u}, Theta por décimo da parcela dos votos de governador do 1º turno dada a eliminados (parcela média: Theta; multiplicador da taxa do 13 e do 22): ' + '; '.join(f'{fpc(l["parcela_media"])}: {fv(l["theta"], 3)} ({fv(l["multiplicador_r13"], 2, False)} e {fv(l["multiplicador_r22"], 2, False)})' for l in e2['linhas'])
              + f'. Reta até a parcela zero: Theta {fv(e2["reta"]["theta_na_parcela_zero"])} (ep {fv(e2["reta"]["ep"], 4, False)}); inclinação {fv(e2["reta"]["inclinacao"], 2)} (ep {fv(e2["reta"]["ep_inclinacao"], 2, False)}).')
        A('  E2b, só a metade das seções com menor parcela de governador eliminado: ' + '; '.join(f'{u} Theta {fv(q_["theta"])} (ep {fv(q_["ep"], 4, False)}; {fi(q_["n_secoes"])} seções; parcela até {fpc(q_["parcela_maxima"])}; a troca de 3,57% daria {fv(q_["formula_p_0357"])})' for u, q_ in expl['E2b_metade_de_baixo'].items()) + '.')
        for u in UFS:
            e4 = expl['E4_forca_dentro_da_uf'][u]
            A(f'  E4, {u}, Theta por tercil de força de Lula dentro da UF: ' + '; '.join(f'{nome.replace("_", " ")} {fv(e4[nome]["theta"])} (ep {fv(e4[nome]["ep"], 4, False)})' for nome in ('lula_fraco', 'meio', 'lula_forte'))
              + f'. Fraco menos forte: {fv(e4["diferenca_fraco_menos_forte"]["observada"])} (ep {fv(e4["diferenca_fraco_menos_forte"]["ep"], 4, False)}); a troca proporcional de 3,57% preveria {fv(e4["diferenca_fraco_menos_forte"]["prevista_p_0357"])}.')
        e5 = expl['E5_leitura_a_favor_cedula_inteira']
        A(f'  E5, leitura a favor da tese que o sinal negativo admite (cédula inteira fabricada ou trocada para Lula, com o 13 repetido em governador): o excesso de 13 é de {fi(e5["excesso_de_13_em_AC_e_TO"])} votos, {fv(e5["por_cento_dos_validos_de_AC_e_TO"], 2, False)}% dos válidos de AC e TO. '
          f'Se TODO o excesso fosse isso e valesse igual no país: {fi(e5["se_todo_o_excesso_fosse_isso_e_igual_no_pais_cedulas"])} cédulas, {fpc(e5["fracao_da_margem_se_fabricadas"])} da margem se fabricadas e {fpc(e5["fracao_da_margem_se_trocadas"])} se trocadas. É teto, não estimativa.')
        for u in UFS:
            e6 = expl['E6_comparecimento'][u]
            A(f'  E6, {u}: o comparecimento variou {fi(e6["variacao_do_comparecimento_total"])} entre os turnos; {fi(e6["secoes_com_aumento"])} seções subiram, somando {fi(e6["aumento_somado_nas_que_subiram"])} eleitores. Nulos com 13 por eleitor a mais na seção: {fv(e6["g13_2t"]["por_eleitor_a_mais_na_secao"]["coef"], 3)} (ep {fv(e6["g13_2t"]["por_eleitor_a_mais_na_secao"]["ep"], 3, False)}); '
              f'com 22: {fv(e6["g22_2t"]["por_eleitor_a_mais_na_secao"]["coef"], 3)} (ep {fv(e6["g22_2t"]["por_eleitor_a_mais_na_secao"]["ep"], 3, False)}). Cédula fabricada com 13 nos dois cargos daria perto de 1 no 13.')
        for x in lei.get('exploratorio_leitura', []):
            A('  ' + x)
        A('')
    A('DESVIOS E DECISÕES FORA DO REGISTRO')
    for x in lei.get('desvios', []):
        A('  ' + x)
    A(f'  Cláusulas contadas para o acaso: {clausulas["n"]} ({", ".join(clausulas["lista"])}); a 5% cada, o acaso daria {fv(clausulas["sinais_que_o_acaso_daria_a_5_por_cento"], 2, False)} sinal.')
    A('')
    A('AVISO QUE VALE PARA O TESTE INTEIRO')
    A('  RDV e boletim saem do mesmo programa da urna. O teste enxerga uma alteração que mexa só na contagem de presidente; um programa que também reescrevesse os nulos de governador de forma coerente escaparia. Vale só para AC e TO (1,3% das seções do país).')
    txt = _quebra('\n'.join(T))
    for ch in (chr(0x2014), chr(0x2013)):  # nenhum travessão no texto
        assert ch not in txt
    with open(RAIZ + '/resultados/R27_W3_testemunhas_governador.txt', 'w') as f:
        f.write(txt + '\n')
    P('gravado: resultados/R27_W3_testemunhas_governador.json e .txt')
    P('veredito só com 2026:', v015['veredito'], v015['motivos'])
    if vpl:
        P('veredito com placebo:', vpl['veredito'], vpl['motivos'], 'sis', sis_pl)


# Ordem completa usada: baixar (2026 1t e 2t de AC e TO; 2022 1t e 2t de AL), extrair 2026, conferir 2026, etapa1, validade,
# abrir, extrair 2022, conferir 2022, placebo, exploratorio, leitura, relatorio. Os modos exploratorio e leitura foram
# escritos depois de ver Theta e não decidem nada.
if __name__ == '__main__':
    modo = sys.argv[1] if len(sys.argv) > 1 else ''
    if modo == 'baixar':
        baixar(sys.argv[2], sys.argv[3], sys.argv[4])
    elif modo == 'extrair':
        extrair(sys.argv[2])
    elif modo == 'conferir':
        conferir(sys.argv[2])
    elif modo == 'etapa1':
        etapa1()
    elif modo == 'validade':
        validade()
    elif modo == 'abrir':
        abrir()
    elif modo == 'placebo':
        placebo()
    elif modo == 'relatorio':
        relatorio()
    elif modo == 'exploratorio':
        exploratorio()
    elif modo == 'leitura':
        leitura()
    else:
        P(__doc__)
