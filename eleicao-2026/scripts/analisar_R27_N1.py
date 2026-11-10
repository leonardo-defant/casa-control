"""R27_N1: POR ONDE ENTRARAM OS VOTOS A MAIS (teste N1 do Adendo 28 do pré-registro, por inteiro).

Adendo 28 (commit 938be19, 10/11/2026 04:36:33 UTC), escrito depois da Onda A e antes de rodar. O critério vale como
está no adendo. Este docstring foi escrito ANTES de qualquer conta com votos; o que ele decide e o registro não fixa
está em DECISÕES e sai no resultado como desvio. Até aqui só foi lida estrutura sem voto: o formato dos 6.000 boletins
da amostra (campo de habilitações, comparecimento e aptos), a coerência desses campos com o bweb, os totais de
comparecimento e de M do bweb inteiro (já conhecidos do registro) e os códigos de tipo de voto. Um único boletim (PI,
município 10090, zona 8, seção 116) foi aberto por inteiro para ver o formato, e nele os votos do 2º turno apareceram
na tela (158 e 27); nenhuma soma, média ou comparação de votos foi feita.

Uso:
  python3 -I scripts/analisar_R27_N1.py bweb 1|2   uma passada no bweb do turno (filtro por bytes): tabela de toda seção
                                                   (aptos, comparecimento, M) e as linhas de Presidente da amostra
  python3 -I scripts/analisar_R27_N1.py bu         lê os 6.000 boletins (S, B, M, comparecimento, aptos, votos)
  python3 -I scripts/analisar_R27_N1.py rodar      confere, calcula tudo e grava resultados/R27_N1_canal_de_entrada.json e .txt
Trabalho e parciais: /home/user/trabalho-eleicao/adendo27/R27_N1/

Pergunta. A virada passa pelo comparecimento (Onda A). O comparecimento subiu 2.960.239 entre os turnos. Cada boletim
conta os eleitores por tipo de habilitação: B (a urna reconheceu a digital do eleitor), M (eleitor com biometria no
cadastro liberado pelo mesário, sem o dedo dele) e S (eleitor sem biometria no cadastro, liberado pelo ano de
nascimento). Voto lançado pela mesa em nome de quem faltou só entra por M ou por S. Se os votos a mais entraram por B,
a mesa não foi o portador; se entraram por S + M, a hipótese de voto lançado na mesa ganha um caminho.

O QUE O REGISTRO FIXA (aplicado à letra)
- Dados: boletins do 1º e do 2º turno das 3.000 seções de registro/adendo27/amostra_aas_principal.txt (amostra
  aleatória simples das 499.205 seções do 2º turno, semente em sorteio_aas.json).
- Estimativas nacionais da variação entre os turnos de B, M e S: média amostral vezes 499.205; erro de amostra
  aleatória simples com correção de população finita. Conferidas contra o exato: comparecimento +2.960.239 e
  M +290.239 pelo bweb.
- Por seção, com efeito fixo de UF: ganho de Lula e ganho de Flávio contra as variações de B e de S + M.
- SINAL: variação de S + M de 1.107.548 ou mais (25% da margem), com limite inferior de 95% de 443.019 ou mais, e
  coeficiente de Lula em S + M maior que o de B em 0,25 ou mais, a mais de 3 erros-padrão.
- SEM SINAL: limite superior de 95% da variação de S + M abaixo de 443.019 (10% da margem). Entre os dois: INCONCLUSIVO.
- Leitura fixada antes: se B responder por 90% ou mais do aumento líquido, os votos a mais entraram por eleitores cuja
  digital a urna reconheceu; fica excluído voto lançado pela mesa como portador da margem e sobra só a hipótese de
  programa que registre biometria falsa, que dado público não testa e que só caderno de votação decide.
- Ao lado: a mesma decomposição para as saídas (seções em que B caiu) e a assimetria das caudas (seções com S + M
  subindo 10 ou mais contra caindo 10 ou mais).
- Do pedido desta onda, descritivo: a mesma decomposição por região e nas UFs PI, MA, TO, PB, CE contra RS, RJ, SC,
  SP, PR.
- Dos avisos do Adendo 27: calibração por efeito plantado nos dados de 2026, teste espelho, valor bruto de 2026 ao
  lado de qualquer comparação com outro ano (este teste não usa outro ano), tradução em votos de margem. Teste feito
  só com arquivos da urna não vale como contrapeso à hipótese de programa adulterado na origem.

FATOS DE ESTRUTURA JÁ CONHECIDOS AO ESCREVER (sem voto)
- Os 3.000 boletins existem nos dois turnos. Nas 2.990 seções do Brasil o boletim traz as três contagens nos dois
  turnos, [S, B, M] no campo de contexto 1, com S + B + M igual ao comparecimento e M igual ao
  QT_ELEI_BIOM_SEM_HABILITACAO do bweb em 2.990 de 2.990, nos dois turnos. A cláusula "se o boletim do 1º turno não
  trouxer as três" não é acionada: nada é estimado pelo perfil do eleitorado.
- As 10 seções do exterior (ZZ) da amostra não trazem o campo em nenhum turno (a urna de lá não usa biometria); o bweb
  dá M = 0 nas 1.308 seções do exterior.
- O universo do sorteio é o 2º turno (499.205 seções). Uma seção do exterior existe só no 1º turno (comparecimento 2):
  no universo a variação exata do comparecimento é +2.960.241 e a de M é +290.239.
- Como M sozinho subiu 290.239 (9,80% do aumento líquido), a leitura dos 90% só pode ser atendida se S não subir mais
  que cerca de 5,8 mil eleitores no país. Isso sai dos números exatos e era sabido antes de abrir os boletins.

DECISÕES QUE O REGISTRO NÃO FIXA (tomadas aqui, antes de calcular qualquer coisa com votos)
D1. Variação por seção: dX = X do 2º turno menos X do 1º turno na mesma chave (UF, município, zona, seção), para X em
    B, M, S, S + M e comparecimento. Todas as 3.000 seções da amostra têm os dois turnos; nenhuma é retirada das
    estimativas nacionais (nem por mudança de aptos, nem por troca de urna). N = 499.205, n = 3.000.
D2. Exterior: nas seções sem o campo de habilitações, B = 0, M = 0 (como no bweb) e S = comparecimento, porque ali
    ninguém é habilitado por biometria e o voto lançado na mesa entraria por esse caminho. Ao lado: a mesma conta só
    com o Brasil (N = 497.897, n = 2.990, domínio de tamanho conhecido) somada ao exato do exterior pelo bweb.
D3. Estimador da letra: T = N x média amostral de dX; erro = N x desvio-padrão amostral (n menos 1) / raiz(n) x
    raiz(1 menos n/N); intervalo de 95% = T mais ou menos 1,96 x erro. "Limite inferior" e "limite superior" do
    critério são os desse intervalo. Conferência contra o exato: z = (T menos exato) / erro para o comparecimento e
    para M; a amostra é dada como coerente se |z| ficar abaixo de 3 nos dois (e isso é relatado de qualquer modo).
D4. Ao lado, sem decidir o veredito: estimador ancorado nos totais exatos. Regressão amostral de dS sobre constante,
    d(comparecimento) e dM; T_S ancorado = N x [média de dS + b_c x (média exata de dcomp menos média amostral) +
    b_M x (média exata de dM menos média amostral)]; erro pelo resíduo. Daí T_(S+M) ancorado = 290.239 + T_S ancorado
    e T_B ancorado = 2.960.241 menos 290.239 menos T_S ancorado. Se o veredito pela letra e o ancorado divergirem,
    vale a letra e a divergência é dita no veredito. Também ao lado: erro por reamostragem das seções (1.000 réplicas).
D5. Leitura dos 90%: fração de B = T_B / T_comp pelas estimativas da letra (razão das médias amostrais), erro por
    linearização; "atendida" se a fração estimada for de 0,90 ou mais; ao lado o intervalo de 95% e a versão ancorada
    (T_B ancorado / 2.960.241). É dito se o intervalo contém 0,90. "Aumento líquido" = variação do comparecimento.
D6. Regressão da letra: universo = as 2.990 seções do Brasil da amostra (no exterior não há três contagens; ao lado, a
    conta com as 10 do exterior, com efeito fixo próprio). Desfechos em votos: gL = Lula 2º turno menos Lula 1º turno;
    gF = Flávio 2º menos Flávio 1º. Regressores: dB e d(S+M), em eleitores. Efeito fixo de UF. Sem peso (cada seção
    vale 1, como no sorteio). O coeficiente é "votos ganhos por eleitor a mais naquele canal".
    Contraste D_L = coeficiente de Lula em d(S+M) menos o de dB; D_F = o mesmo para Flávio (espelho). O erro do
    contraste sai da matriz de covariância completa.
D7. Erro-padrão da regressão (a letra não diz qual): principal = robusto a heterocedasticidade por seção (HC1, com os
    efeitos fixos contados nos graus de liberdade), que é o erro de desenho de uma amostra aleatória simples de
    seções. Ao lado: agrupado por UF (o de lib.fe_ols, conferido contra a função da biblioteca), agrupado por
    município e por reamostragem das seções. "A mais de 3 erros-padrão" é julgado pelo principal; se o agrupado por UF
    mudar a conclusão, isso é dito no veredito.
D8. Regressões ao lado, descritivas (não decidem): (a) dM e dS separados; (b) com controles do 1º turno (votos de Lula,
    de Flávio, dos eliminados, brancos mais nulos, abstenção do 1º turno e variação dos aptos); (c) só seções com a
    mesma urna e os mesmos aptos nos dois turnos; (d) desfechos brancos mais nulos (gBN = BN2 menos BN1) e eliminados
    (gO = menos O1), que fecham a identidade gL + gF + gBN + gO = dB + d(S+M): os quatro coeficientes de cada regressor
    somam 1 e os quatro contrastes somam 0; (e) margem gL menos gF.
D9. Saídas ("seções em que B caiu"): três domínios pela variação de B (caiu, igual, subiu). Em cada um: número de
    seções estimado no país, totais estimados de dB, dM, dS, d(S+M), dcomp, de gL e de gF (N x média de dX x indicador
    do domínio, erro de amostra aleatória simples) e a regressão da letra dentro do domínio (descritiva). Ao lado, o
    mesmo corte pelo comparecimento (caiu, igual, subiu).
D10. Caudas: A+ = seções com d(S+M) de +10 ou mais; A- = seções com d(S+M) de -10 ou menos. Número estimado de cada
    uma no país, soma de d(S+M) em cada (X+ e X-, em eleitores), assimetria = X+ menos |X-|, com erro de amostra
    aleatória simples; ganho médio de Lula e de Flávio e variação média do comparecimento em cada cauda e no resto; e,
    nas caudas, quanto veio de M e quanto de S, quantas trocaram de urna. Ao lado, as somas de todas as altas e de
    todas as quedas de d(S+M) por seção (bruto positivo e bruto negativo).
D11. Excesso sobre a proporcionalidade (descritivo, para separar "entrou mais gente" de "entrou gente por outro canal"):
    E_X = soma de [X2 menos X1 x comp2/comp1] para X em B, M, S (soma zero por construção), nas seções com comp1 > 0.
    Estimativa nacional pela amostra; para M, também o valor exato no bweb inteiro.
D12. Regiões: Norte (AC AM AP PA RO RR TO), Nordeste (AL BA CE MA PB PE PI RN SE), Sudeste (ES MG RJ SP), Sul (PR RS
    SC), Centro-Oeste (DF GO MS MT), Exterior (ZZ). Grupos: "cinco de maior diferença" = PI MA TO PB CE; "cinco de
    menor" = RS RJ SC SP PR (os da Onda A). Em cada domínio: n, N do domínio (exato), estimativas pós-estratificadas
    (N do domínio x média no domínio, com correção de população finita do domínio) de dB, dM, dS, d(S+M) e dcomp; ao
    lado o exato de dcomp e de dM pelo bweb; fração de B no aumento; excesso de D11; ganhos médios de Lula e de Flávio;
    e a regressão da letra nos dois grupos de cinco e nas regiões (descritiva; UF com menos de 60 seções na amostra
    não ganha regressão própria).
D13. Calibração por efeito plantado, nas tabelas da amostra (nunca nos arquivos), semente 20261110, 200 cópias por
    cenário. A2 = aptos menos comparecimento do 2º turno (faltosos da seção); soma exata de A2 no país pelo bweb.
    IRREGULARIDADE (voto lançado pela mesa em nome de faltoso, para Lula): k votos somados a Lula, ao comparecimento
    e ao canal sem biometria (a M com probabilidade igual à fração de B + M no comparecimento da seção, a S com o
    resto; no exterior, a S). Tamanhos K = 443.019 (10% da margem), 1.107.548 (25%) e 4.430.191 (margem inteira).
      PA, espalhada: k ~ Binomial(A2, K / soma de A2 no país) em toda seção.
      PB, concentrada: o mesmo K em 5% das seções sorteadas (25% das seções quando K é a margem inteira, porque em 5%
          não cabe), k ~ Binomial(A2, K / (fração x soma de A2)).
      PE, espelho do plantio: PA e PB a favor de Flávio (K = 1.107.548).
    EXPLICAÇÕES INOCENTES:
      I1, abstenção pura: T ~ Binomial(Flávio 2º turno, 0,036) sai do voto de Flávio e do comparecimento; o canal de
          cada eleitor que sai é sorteado na composição B, M, S da seção no 2º turno (hipergeométrica).
      I2, entrada de eleitores reais para Lula: os mesmos k de PA e de PB (K = 443.019, 1.107.548 e 4.430.191;
          concentrada em 1.107.548 e na margem inteira), com o canal sorteado na composição B, M, S da própria seção
          no 2º turno.
      I3, leitor pior no 2º turno (os mesmos eleitores e os mesmos votos, mais liberações): m ~ Binomial(B2, K / soma
          estimada de B2 no país) passa de B para M, espalhado e concentrado em 5% das seções, K = 1.107.548.
    Em cada cópia: T de S + M, limites, fração de B, D_L, D_F, as três condições de SINAL, a condição de SEM SINAL e a
    tradução em votos de margem de D16.
D14. Regra de poder (o registro pede a calibração mas não diz como ela decide):
    Nível (variação de S + M): "enxerga" se, com PA de 1.107.548, a estimativa subir em média entre 0,9 K e 1,1 K e
    no máximo 5% das cópias cumprirem SEM SINAL, e se com PA de 443.019 no máximo 5% das cópias cumprirem SEM SINAL
    (o teste não absolve 10% da margem plantada). Se o veredito for SEM SINAL e essa regra falhar, vira SEM PODER.
    Regressão (contraste D_L): "enxerga" uma forma (espalhada ou concentrada) se, com 1.107.548 plantados nela, 95% ou
    mais das cópias tiverem D_L de 0,25 ou mais a mais de 3 erros-padrão. Se nenhuma forma for vista nem com a margem
    inteira, a cláusula da regressão é SEM PODER. O SINAL pela letra exige as duas partes: se só a concentrada for
    vista, o resultado diz que o SINAL não alcança a forma espalhada.
    Distinção: o teste "distingue" a irregularidade da explicação inocente se, com I2 e I3 do mesmo tamanho, no máximo
    5% das cópias cumprirem SINAL. A abstenção pura (I1) e a retirada de eleitores de Flávio do registro deixam o
    mesmo boletim: este teste não as separa, só mede entradas.
D15. Veredito por partes e combinado:
    Parte 1, nível: "acima dos dois limiares" (T de S + M de 1.107.548 ou mais e limite inferior de 443.019 ou mais),
    SEM SINAL (limite superior abaixo de 443.019), senão INCONCLUSIVO; SEM PODER pela D14.
    Parte 2, regressão: SINAL se D_L for de 0,25 ou mais a mais de 3 erros-padrão; SEM SINAL se D_L + 1,96 x erro
    ficar abaixo de 0,25 e a calibração enxergar pelo menos a forma concentrada com 1.107.548; SEM PODER se a
    calibração não enxergar nenhuma forma com 1.107.548; senão INCONCLUSIVO. (O rótulo SEM SINAL desta parte não está
    na letra; serve para dizer o que a regressão sozinha mostra.)
    Parte 3, leitura dos 90%: atendida ou não atendida pela D5.
    Combinado, pela letra: SINAL se as três condições do registro valerem; SEM SINAL se o limite superior de S + M
    ficar abaixo de 443.019; senão INCONCLUSIVO. Um SINAL só conta como indício com as três condições do Adendo 27:
    conferente, calibração que enxerga e espelho sem o mesmo (espelho = D_F de 0,25 ou mais a mais de 3 erros-padrão).
D16. Tradução em votos de margem. (a) T de S + M e seu limite superior divididos por 4.430.191: teto do que o canal
    sem biometria carrega em saldo se cada eleitor a mais desse canal fosse um voto lançado para Lula (vale 1 voto de
    margem cada). (b) Pela regressão: margem que acompanha o saldo de S + M além do que acompanharia se fossem
    eleitores do canal B = (D_L menos D_F) x T de S + M, erro por método delta tratando as duas partes como
    independentes; e a versão bruta (D_L menos D_F) x soma das altas de D10. (c) Na calibração, quanto da quantia
    plantada cada tradução devolve. (d) Limite dito antes: o saldo esconde entradas compensadas por saídas no mesmo
    canal; por isso as caudas e os brutos de D10 vão ao lado, e nada aqui limita um programa que registre biometria
    falsa (todos os campos saem do mesmo programa).
D17. Conferência dos boletins contra o bweb (achado, se houver diferença): nas 3.000 seções e nos dois turnos, chave,
    aptos, comparecimento, M, e os votos de Presidente candidato a candidato, brancos e nulos; também contra a base
    dados/secoes2026.json.gz. Diferenças são listadas uma a uma. Se houver diferença, as contas usam o boletim (o
    teste é sobre o boletim) e a sensibilidade com o bweb é relatada.
"""
import collections, glob, gzip, hashlib, io, json, os, sys, time, zipfile

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(REPO, 'scripts'))
W = '/home/user/trabalho-eleicao/adendo27/R27_N1'
AAS = '/home/user/trabalho-eleicao/adendo27/aas'
LISTA = os.path.join(REPO, 'registro/adendo27/amostra_aas_principal.txt')
ZIPS = {'1': '/home/user/trabalho-eleicao/bweb1t/zips/*.zip', '2': '/home/user/trabalho-eleicao/trab2t/zips2t/*.zip'}
PADRAO = b';1;"Presidente";'
OUT_JSON = os.path.join(REPO, 'resultados/R27_N1_canal_de_entrada.json')
OUT_TXT = os.path.join(REPO, 'resultados/R27_N1_canal_de_entrada.txt')

N_U = 499205
MARGEM = 4430191
L25 = 1107548
L10 = 443019
EXATO_COMP_PAIS = 2960239
EXATO_M_PAIS = 290239
SEMENTE = 20261110
REPS = 200
REGIOES = {'Norte': 'AC AM AP PA RO RR TO', 'Nordeste': 'AL BA CE MA PB PE PI RN SE', 'Sudeste': 'ES MG RJ SP',
           'Sul': 'PR RS SC', 'Centro-Oeste': 'DF GO MS MT', 'Exterior': 'ZZ'}
G_ALTO = ['PI', 'MA', 'TO', 'PB', 'CE']
G_BAIXO = ['RS', 'RJ', 'SC', 'SP', 'PR']


def log(*a):
    print(time.strftime('%H:%M:%S'), *a, flush=True)


def amostra():
    return [l.strip() for l in open(LISTA) if l.strip()]


# ---------------------------------------------------------------------------------------------------------------
# Preparo de dados (sem conta com votos)
# ---------------------------------------------------------------------------------------------------------------
def _bweb_zip(a):
    zp, alvo = a
    z = zipfile.ZipFile(zp)
    nome = [n for n in z.namelist() if n.lower().endswith('.csv')][0]
    pop = {}; am = {}
    with z.open(nome) as raw:
        fh = io.BufferedReader(raw, 1 << 22)
        cab = [c.strip().strip('"').replace('SG_ UF', 'SG_UF') for c in fh.readline().decode('latin1').strip().split(';')]
        ix = {c: i for i, c in enumerate(cab)}
        iUF, iMUN, iZ, iS, iC = ix['SG_UF'], ix['CD_MUNICIPIO'], ix['NR_ZONA'], ix['NR_SECAO'], ix['CD_CARGO_PERGUNTA']
        campos = ['NR_LOCAL_VOTACAO', 'QT_APTOS', 'QT_COMPARECIMENTO', 'QT_ABSTENCOES', 'CD_TIPO_URNA', 'DS_TIPO_URNA',
                  'NR_URNA_EFETIVADA', 'QT_ELEI_BIOM_SEM_HABILITACAO', 'DS_SECOES_AGREGADAS', 'NR_JUNTA_APURADORA',
                  'DT_ABERTURA', 'DT_ENCERRAMENTO']
        iv = [ix[c] for c in campos]
        iTV, iNV, iQ, iNM = ix['CD_TIPO_VOTAVEL'], ix['NR_VOTAVEL'], ix['QT_VOTOS'], ix['NM_VOTAVEL']
        n = 0
        for linha in fh:
            if PADRAO not in linha:  # filtro por bytes antes de separar os campos
                continue
            a_ = linha.rstrip(b'\r\n').split(b';')
            if len(a_) != len(cab):  # ponto e vírgula dentro de aspas: usa o leitor de csv nessa linha
                import csv
                a_ = [b'"' + x.encode('latin1') + b'"' for x in next(csv.reader([linha.decode('latin1')], delimiter=';'))]
            if a_[iC].strip(b'"') != b'1':
                continue
            n += 1
            k = f"{a_[iUF].strip(b'\"').decode()}|{int(a_[iMUN].strip(b'\"'))}|{int(a_[iZ].strip(b'\"'))}|{int(a_[iS].strip(b'\"'))}"
            if k not in pop:
                v = [a_[i].strip(b'"').decode('latin1') for i in iv]
                pop[k] = [int(v[0]), int(v[1]), int(v[2]), int(v[3]), v[4], v[5], v[6], int(v[7]), v[8], v[9], v[10], v[11]]
            if k in alvo:
                am.setdefault(k, []).append([int(a_[iTV].strip(b'"')), int(a_[iNV].strip(b'"')), int(a_[iQ].strip(b'"')),
                                             a_[iNM].strip(b'"').decode('latin1')])
    return os.path.basename(zp), n, pop, am


def cmd_bweb(turno):
    from multiprocessing import Pool
    os.makedirs(W, exist_ok=True)
    alvo = set(amostra())
    zs = sorted(glob.glob(ZIPS[turno]), key=lambda p: -os.path.getsize(p))
    pop = {}; am = {}; linhas = 0
    with Pool(4) as P:
        for nome, n, p, a in P.imap_unordered(_bweb_zip, [(z, alvo) for z in zs]):
            pop.update(p); am.update(a); linhas += n
            log('ok', nome, n, len(p), len(a))
    with gzip.open(f'{W}/bweb_pop_{turno}t.json.gz', 'wt') as f:
        json.dump({'campos': ['loc', 'apt', 'comp', 'abst', 'cd_tipo', 'ds_tipo', 'urna', 'M', 'agregadas', 'junta', 'ab', 'enc'],
                   'secoes': pop}, f, separators=(',', ':'), ensure_ascii=False)
    json.dump(am, open(f'{W}/bweb_amostra_{turno}t.json', 'w'), separators=(',', ':'), ensure_ascii=False)
    log('turno', turno, 'linhas de presidente', linhas, 'secoes', len(pop), 'amostra', len(am))


def _int(v):
    return int.from_bytes(v, 'big')


def _ler_bu(a):
    k, t = a
    from ber import parse
    import decodificar
    uf, mun, zona, sec = k.split('|')
    d = f'{AAS}/t{t}/{uf.lower()}/{int(mun):05d}/{int(zona):04d}/{int(sec):04d}'
    fs = sorted(glob.glob(d + '/*-bu.dat'))
    if len(fs) != 1:
        return k, t, {'erro': f'{len(fs)} arquivos de boletim'}
    try:
        # leitor próprio (BER) das três contagens [S, B, M] e do comparecimento da seção
        env = parse(open(fs[0], 'rb').read())[0][2]
        octet = [n for n in env if (n[0], n[1]) == (0, 4)][-1][2]
        bu = parse(octet)[0][2]
        ctx = [[_int(c[2]) for c in n[2]] for n in bu
               if (n[0], n[1]) == (2, 1) and isinstance(n[2], list) and len(n[2]) == 3 and all((c[0], c[1]) == (0, 2) for c in n[2])]
        ints = [_int(n[2]) for n in bu if (n[0], n[1]) == (0, 2)]
        b = decodificar.ler_bu(fs[0])
        chave_bu = f"{uf}|{b.get('mun')}|{b.get('zona')}|{b.get('secao')}"
        pres = None
        for ide, rec in b['eleicoes'].items():
            c = rec['cargos'].get(1)
            if c is not None:
                pres = {'eleicao': ide, 'apt': rec['apt'], 'comp': c['comp'],
                        'votos': [[tp, (-1 if nn is None else nn), q] for (tp, nn), q in
                                  sorted(c['votos'].items(), key=lambda x: (x[0][0], -1 if x[0][1] is None else x[0][1]))]}
        return k, t, {'arq': os.path.basename(fs[0]), 'chave_bu': chave_bu, 'loc': b.get('loc'), 'urna': b.get('urna'),
                      'versao': b.get('versao'), 'ab': b.get('ab'), 'enc': b.get('enc'), 'sbm': ctx, 'comp_secao': ints,
                      'pres': pres, 'eleicoes': sorted(b['eleicoes'])}
    except Exception as e:
        return k, t, {'erro': repr(e)}


def cmd_bu():
    from multiprocessing import Pool
    os.makedirs(W, exist_ok=True)
    ks = amostra()
    out = {k: {} for k in ks}
    with Pool(4) as P:
        for k, t, r in P.imap_unordered(_ler_bu, [(k, t) for k in ks for t in ('1', '2')], chunksize=50):
            out[k][t] = r
    json.dump(out, open(f'{W}/bu_amostra.json', 'w'), separators=(',', ':'))
    log('boletins lidos', sum(1 for k in ks for t in ('1', '2') if 'erro' not in out[k][t]), 'erros',
        sum(1 for k in ks for t in ('1', '2') if 'erro' in out[k][t]))


# ---------------------------------------------------------------------------------------------------------------
# Conferência boletim x bweb x base (D17) e montagem das tabelas
# ---------------------------------------------------------------------------------------------------------------
def _votos_bu(pres):
    nom = {}; br = nu = 0; outros = []
    for tp, nn, q in pres['votos']:
        if tp == 1: nom[nn] = nom.get(nn, 0) + q
        elif tp == 2: br += q
        elif tp == 3: nu += q
        else: outros.append([tp, nn, q])
    return nom, br, nu, outros


def _votos_bweb(linhas):
    nom = {}; br = nu = 0; outros = []
    for tv, nv, q, nm in linhas:
        if tv == 1: nom[nv] = nom.get(nv, 0) + q
        elif tv == 2: br += q
        elif tv == 3: nu += q
        else: outros.append([tv, nv, q])
    return nom, br, nu, outros


def montar():
    """Lê tudo, confere boletim contra bweb e base, devolve as tabelas da amostra e os exatos da população."""
    import numpy as np
    from lib import carregar
    ks = amostra()
    bu = json.load(open(f'{W}/bu_amostra.json'))
    bw = {t: json.load(open(f'{W}/bweb_amostra_{t}t.json')) for t in ('1', '2')}
    pop = {t: json.load(gzip.open(f'{W}/bweb_pop_{t}t.json.gz'))['secoes'] for t in ('1', '2')}
    base = carregar(os.path.join(REPO, 'dados/secoes2026.json.gz'))
    assert len(pop['2']) == N_U and len(ks) == 3000 and len(set(ks)) == 3000 and all(k in pop['2'] for k in ks)
    conf = {'secoes': len(ks), 'por_turno': {}, 'diferencas': []}
    col = collections.defaultdict(list)
    for t in ('1', '2'):
        c = collections.Counter()
        for k in ks:
            r = bu[k][t]
            if 'erro' in r:
                c['boletim_ilegivel'] += 1; conf['diferencas'].append([k, t, 'boletim ilegível', r['erro']]); continue
            p = pop[t].get(k); l = bw[t].get(k)
            if p is None or l is None:
                c['sem_bweb'] += 1; conf['diferencas'].append([k, t, 'seção sem linha no bweb', '']); continue
            c['boletins'] += 1
            ok = r['chave_bu'] == k; c['chave_igual'] += ok
            if not ok: conf['diferencas'].append([k, t, 'chave', r['chave_bu']])
            ok = r['pres']['apt'] == p[1]; c['aptos_iguais'] += ok
            if not ok: conf['diferencas'].append([k, t, 'aptos', [r['pres']['apt'], p[1]]])
            comp = r['comp_secao'][0] if len(r['comp_secao']) == 1 else None
            ok = (r['pres']['comp'] == p[2]) and comp == p[2]; c['comparecimento_igual'] += ok
            if not ok: conf['diferencas'].append([k, t, 'comparecimento', [r['pres']['comp'], comp, p[2]]])
            if len(r['sbm']) == 1:
                s, b, m = r['sbm'][0]
                c['com_tres_contagens'] += 1
                ok = s + b + m == p[2]; c['S+B+M_igual_ao_comparecimento'] += ok
                if not ok: conf['diferencas'].append([k, t, 'S+B+M diferente do comparecimento', [s, b, m, p[2]]])
                ok = m == p[7]; c['M_igual_ao_bweb'] += ok
                if not ok: conf['diferencas'].append([k, t, 'M diferente do bweb', [m, p[7]]])
            else:
                c['sem_tres_contagens'] += 1
                c['sem_tres_contagens_exterior'] += k.startswith('ZZ|')
                c['sem_tres_contagens_M_bweb_zero'] += p[7] == 0
                s, b, m = p[2], 0, 0  # D2
            nb, bb, ub, ob = _votos_bu(r['pres']); nw, bw_, uw, ow = _votos_bweb(l)
            cands = sorted(set(nb) | set(nw))
            dif = [[n_, nb.get(n_, 0), nw.get(n_, 0)] for n_ in cands if nb.get(n_, 0) != nw.get(n_, 0)]
            if bb != bw_: dif.append(['branco', bb, bw_])
            if ub != uw: dif.append(['nulo', ub, uw])
            if ob or ow: dif.append(['outros tipos', ob, ow])
            c['votos_iguais_ao_bweb'] += not dif
            c['linhas_de_voto_comparadas'] += len(cands) + 2
            if dif: conf['diferencas'].append([k, t, 'votos boletim x bweb', dif])
            tot = sum(nb.values()) + bb + ub
            ok = tot == r['pres']['comp']; c['soma_dos_votos_igual_ao_comparecimento'] += ok
            if not ok: conf['diferencas'].append([k, t, 'soma dos votos diferente do comparecimento', [tot, r['pres']['comp']]])
            L = nb.get(13, 0); R = nb.get(22, 0); O = sum(q for n_, q in nb.items() if n_ not in (13, 22))
            sb = base.get(k, {}).get(t)
            ok = sb is not None and (sb['L'], sb['R'], sb['O'], sb['B'], sb['N'], sb['comp'], sb['apt']) == (L, R, O, bb, ub, r['pres']['comp'], r['pres']['apt'])
            c['igual_a_base_do_repositorio'] += ok
            if not ok: conf['diferencas'].append([k, t, 'boletim x base do repositório', [sb, [L, R, O, bb, ub]]])
            col['S' + t].append(s); col['B' + t].append(b); col['M' + t].append(m); col['comp' + t].append(r['pres']['comp'])
            col['apt' + t].append(r['pres']['apt']); col['L' + t].append(L); col['R' + t].append(R); col['O' + t].append(O)
            col['BN' + t].append(bb + ub); col['urna' + t].append(int(r['urna'] or 0)); col['Mbweb' + t].append(p[7])
        conf['por_turno'][t] = dict(c)
    assert all(len(v) == 3000 for v in col.values()), {k: len(v) for k, v in col.items()}
    T = {k: np.array(v, dtype=np.int64) for k, v in col.items()}
    T['uf'] = np.array([k.split('|')[0] for k in ks]); T['mun'] = np.array(['|'.join(k.split('|')[:2]) for k in ks])
    T['ext'] = T['uf'] == 'ZZ'; T['chave'] = np.array(ks)
    # exatos da população (bweb inteiro, tabelas próprias): por UF, do universo do 2º turno
    ex = {}
    for k, p2 in pop['2'].items():
        uf = k[:2]; e = ex.setdefault(uf, collections.Counter())
        p1 = pop['1'].get(k)
        e['N'] += 1; e['comp2'] += p2[2]; e['M2'] += p2[7]; e['apt2'] += p2[1]; e['A2'] += p2[1] - p2[2]
        if p1 is not None:
            e['comp1'] += p1[2]; e['M1'] += p1[7]; e['apt1'] += p1[1]
            if p1[2] > 0: e['E_M'] += p2[7] - p1[7] * p2[2] / p1[2]; e['com_comp1'] += 1
            e['mesma_urna'] += p1[6] == p2[6]; e['mesmos_aptos'] += p1[1] == p2[1]
        else:
            e['sem_1t'] += 1
        sb = base.get(k)
        if sb is not None and '2' in sb:
            e['L2'] += sb['2']['L']; e['R2'] += sb['2']['R']; e['BN2'] += sb['2']['B'] + sb['2']['N']
            if '1' in sb:
                e['L1'] += sb['1']['L']; e['R1'] += sb['1']['R']; e['O1'] += sb['1']['O']; e['BN1'] += sb['1']['B'] + sb['1']['N']
    so1 = [k for k in pop['1'] if k not in pop['2']]
    exato = {'por_uf': {u: {a: (float(b) if a == 'E_M' else int(b)) for a, b in e.items()} for u, e in ex.items()},
             'secoes_so_no_1t': so1, 'comp_das_secoes_so_no_1t': int(sum(pop['1'][k][2] for k in so1)),
             'M_das_secoes_so_no_1t': int(sum(pop['1'][k][7] for k in so1))}
    return T, conf, exato


# ---------------------------------------------------------------------------------------------------------------
# Estatística
# ---------------------------------------------------------------------------------------------------------------
def tot_aas(x, N=N_U, n_total=None):
    """Total nacional pela letra: N x média, erro de amostra aleatória simples com correção de população finita."""
    import numpy as np
    x = np.asarray(x, float); n = len(x) if n_total is None else n_total
    m = x.mean(); s = x.std(ddof=1)
    ep = N * s / np.sqrt(n) * np.sqrt(1 - n / N)
    return {'total': float(N * m), 'ep': float(ep), 'li95': float(N * m - 1.96 * ep), 'ls95': float(N * m + 1.96 * ep),
            'media_por_secao': float(m), 'dp_por_secao': float(s), 'n': int(n), 'N': int(N)}


def razao(num, den, N=N_U):
    """Razão de médias com erro por linearização (amostra aleatória simples)."""
    import numpy as np
    num = np.asarray(num, float); den = np.asarray(den, float); n = len(num)
    r = num.mean() / den.mean()
    u = num - r * den
    ep = np.sqrt((1 - n / N) / n) * u.std(ddof=1) / abs(den.mean())
    return {'razao': float(r), 'ep': float(ep), 'li95': float(r - 1.96 * ep), 'ls95': float(r + 1.96 * ep)}


def reg(y, X, fe, nomes, cl_mun=None, contraste=None):
    """MQO com efeito fixo (transformação within), sem peso. Erros: HC1 por seção (principal), agrupado pelo grupo do
    efeito fixo (fórmula de lib.fe_ols) e agrupado por município. contraste = (i, j): coef[i] menos coef[j]."""
    import numpy as np
    y = np.asarray(y, float); X = np.asarray(X, float)
    if X.ndim == 1: X = X[:, None]
    _, g = np.unique(fe, return_inverse=True)
    cnt = np.bincount(g); ok = cnt[g] >= 2
    y, X, g = y[ok], X[ok], g[ok]
    _, g = np.unique(g, return_inverse=True)
    G = g.max() + 1; N, k = X.shape
    def dm(v):
        return v - (np.bincount(g, weights=v, minlength=G) / np.bincount(g, minlength=G))[g]
    yd = dm(y); Xd = np.column_stack([dm(X[:, j]) for j in range(k)])
    XtX = Xd.T @ Xd; inv = np.linalg.inv(XtX)
    b = inv @ (Xd.T @ yd); e = yd - Xd @ b
    out = {'n': int(N), 'grupos_ef': int(G), 'coef': dict(zip(nomes, b.tolist()))}
    Xe = Xd * e[:, None]
    V = {}
    V['hc1'] = (N / (N - k - G)) * inv @ (Xe.T @ Xe) @ inv
    S = np.column_stack([np.bincount(g, weights=Xe[:, j], minlength=G) for j in range(k)])
    V['uf'] = (G / (G - 1) * (N - 1) / (N - k)) * inv @ (S.T @ S) @ inv if G > 1 else np.full((k, k), np.nan)
    if cl_mun is not None:
        _, gm = np.unique(np.asarray(cl_mun)[ok], return_inverse=True); Gm = gm.max() + 1
        Sm = np.column_stack([np.bincount(gm, weights=Xe[:, j], minlength=Gm) for j in range(k)])
        V['mun'] = (Gm / (Gm - 1) * (N - 1) / (N - k - G)) * inv @ (Sm.T @ Sm) @ inv
        out['municipios'] = int(Gm)
    for nome, v in V.items():
        out['ep_' + nome] = dict(zip(nomes, np.sqrt(np.clip(np.diag(v), 0, None)).tolist()))
    out['r2_within'] = float(1 - (e @ e) / (yd @ yd)) if yd @ yd > 0 else None
    if contraste is not None:
        i, j = contraste
        d = float(b[i] - b[j]); out['contraste'] = d
        for nome, v in V.items():
            ep = float(np.sqrt(max(0.0, v[i, i] + v[j, j] - 2 * v[i, j])))
            out['contraste_ep_' + nome] = ep
            out['contraste_z_' + nome] = d / ep if ep > 0 else None
    return out


def nucleo(a, fe, mun, br, completo=False):
    """As quantidades do critério numa tabela (observada ou cópia com efeito plantado)."""
    import numpy as np
    dB = a['B2'] - a['B1']; dM = a['M2'] - a['M1']; dS = a['S2'] - a['S1']; dSM = dS + dM; dC = a['comp2'] - a['comp1']
    gL = a['L2'] - a['L1']; gF = a['R2'] - a['R1']
    t = tot_aas(dSM); tB = tot_aas(dB); tC = tot_aas(dC)
    fB = razao(dB, dC)
    X = np.column_stack([dB[br], dSM[br]])
    rL = reg(gL[br], X, fe[br], ['dB', 'dSM'], cl_mun=mun[br] if completo else None, contraste=(1, 0))
    rF = reg(gF[br], X, fe[br], ['dB', 'dSM'], cl_mun=mun[br] if completo else None, contraste=(1, 0))
    DL, eL = rL['contraste'], rL['contraste_ep_hc1']; DF, eF = rF['contraste'], rF['contraste_ep_hc1']
    c1 = t['total'] >= L25; c2 = t['li95'] >= L10; c3 = DL >= 0.25 and DL / eL > 3
    altas = float(N_U * np.clip(dSM, 0, None).mean())
    trad = (DL - DF) * t['total']
    o = {'T_SM': t['total'], 'ep_SM': t['ep'], 'li_SM': t['li95'], 'ls_SM': t['ls95'], 'T_B': tB['total'], 'T_comp': tC['total'],
         'fracao_B': fB['razao'], 'fracao_B_ep': fB['ep'], 'D_L': DL, 'D_L_ep': eL, 'D_L_z': DL / eL, 'D_F': DF, 'D_F_ep': eF, 'D_F_z': DF / eF,
         'bL_B': rL['coef']['dB'], 'bL_SM': rL['coef']['dSM'], 'bF_B': rF['coef']['dB'], 'bF_SM': rF['coef']['dSM'],
         'c1_T_ge_25': bool(c1), 'c2_li_ge_10': bool(c2), 'c3_contraste': bool(c3), 'SINAL': bool(c1 and c2 and c3),
         'SEM_SINAL': bool(t['ls95'] < L10), 'espelho_c3': bool(DF >= 0.25 and DF / eF > 3), 'leitura_90': bool(fB['razao'] >= 0.90),
         'traducao_saldo': float(trad), 'traducao_bruta': float((DL - DF) * altas), 'altas': altas}
    if completo:
        o['_rL'] = rL; o['_rF'] = rF; o['_t'] = {'SM': t, 'B': tB, 'comp': tC}; o['_fB'] = fB
    return o


def plantar(a, cen, K, rng, A2_pais, B2_pais, frac=None, alvo='L'):
    """Devolve cópia da tabela com o cenário plantado (D13) e o total plantado na amostra."""
    import numpy as np
    c = {k: v.copy() for k, v in a.items()}
    n = len(c['comp2']); A2 = np.clip(c['apt2'] - c['comp2'], 0, None)
    sel = np.ones(n, bool) if frac is None else rng.random(n) < frac
    f = 1.0 if frac is None else frac
    if cen in ('mesa', 'reais'):
        p = min(1.0, K / (f * A2_pais))
        k = np.where(sel, rng.binomial(A2, p), 0)
        if cen == 'mesa':
            pm = np.where(c['comp2'] > 0, (c['B2'] + c['M2']) / np.maximum(c['comp2'], 1), 0.0)
            pm = np.where(a['ext'], 0.0, pm)
            km = rng.binomial(k, pm); c['M2'] = c['M2'] + km; c['S2'] = c['S2'] + (k - km)
        else:
            comp = np.maximum(c['comp2'], 1)
            pB = np.where(c['comp2'] > 0, c['B2'] / comp, 0.0); kb = rng.binomial(k, pB)
            rest = k - kb
            pM = np.where((c['M2'] + c['S2']) > 0, c['M2'] / np.maximum(c['M2'] + c['S2'], 1), 0.0)
            km = rng.binomial(rest, pM)
            c['B2'] = c['B2'] + kb; c['M2'] = c['M2'] + km; c['S2'] = c['S2'] + (rest - km)
        c['comp2'] = c['comp2'] + k
        c[alvo + '2'] = c[alvo + '2'] + k
        return c, int(k.sum())
    if cen == 'abst':
        Tt = rng.binomial(c['R2'], K)  # aqui K é a taxa (0,036)
        nb = np.zeros(n, np.int64); nm = np.zeros(n, np.int64); ns = np.zeros(n, np.int64)
        for i in np.nonzero(Tt)[0]:
            cores = [int(c['B2'][i]), int(c['M2'][i]), int(c['S2'][i])]
            x = rng.multivariate_hypergeometric(cores, int(Tt[i]))
            nb[i], nm[i], ns[i] = x
        c['B2'] = c['B2'] - nb; c['M2'] = c['M2'] - nm; c['S2'] = c['S2'] - ns
        c['comp2'] = c['comp2'] - Tt; c['R2'] = c['R2'] - Tt
        return c, int(Tt.sum())
    if cen == 'leitor':
        p = min(1.0, K / (f * B2_pais))
        m = np.where(sel, rng.binomial(c['B2'], p), 0)
        c['B2'] = c['B2'] - m; c['M2'] = c['M2'] + m
        return c, int(m.sum())
    raise ValueError(cen)


def resumo_copias(obs, copias, plantado, K):
    import numpy as np
    def col(k): return np.array([c[k] for c in copias], float)
    r = {'copias': len(copias), 'plantado_medio_expandido': float(np.mean(plantado) * N_U / 3000)}
    for k in ('T_SM', 'T_B', 'fracao_B', 'D_L', 'D_L_z', 'D_F', 'D_F_z', 'bL_B', 'bL_SM', 'bF_B', 'bF_SM', 'traducao_saldo', 'traducao_bruta', 'ls_SM', 'li_SM'):
        v = col(k); r[k + '_media'] = float(v.mean()); r[k + '_dp'] = float(v.std(ddof=1))
        r[k + '_delta_medio'] = float((v - obs[k]).mean())
    for k in ('c1_T_ge_25', 'c2_li_ge_10', 'c3_contraste', 'SINAL', 'SEM_SINAL', 'espelho_c3', 'leitura_90'):
        r['fracao_' + k] = float(col(k).mean())
    if K:
        r['recuperacao_nivel'] = r['T_SM_delta_medio'] / K
        r['traducao_saldo_devolve'] = r['traducao_saldo_delta_medio'] / K
        r['traducao_bruta_devolve'] = r['traducao_bruta_delta_medio'] / K
    return r


def dominio_tot(x, ind, N=N_U):
    import numpy as np
    return tot_aas(np.where(ind, x, 0.0), N=N)


def rodar():
    import numpy as np
    from lib import fe_ols
    os.makedirs(W, exist_ok=True)
    doc = __doc__
    R = {'teste': 'R27 N1: por onde entraram os votos a mais (Adendo 28, N1)',
         'registro': 'PRE-REGISTRO-2026-10-26.md, Adendo 28 (commit 938be19, 10/11/2026 04:36:33 UTC); avisos do Adendo 27 (commit 2748895)',
         'docstring_sha256': hashlib.sha256(doc.encode()).hexdigest()}
    T, conf, exato = montar()
    R['conferencia_boletim_bweb'] = conf
    R['conferencia_do_sorteio'] = conferir_sorteio()
    json.dump(R, open(f'{W}/parcial_conferencia.json', 'w'), ensure_ascii=False, indent=1)
    log('conferência', conf['por_turno'], 'diferenças', len(conf['diferencas']))
    a = {k: T[k] for k in ('B1', 'M1', 'S1', 'B2', 'M2', 'S2', 'comp1', 'comp2', 'apt1', 'apt2', 'L1', 'R1', 'O1', 'BN1', 'L2', 'R2', 'BN2')}
    a['ext'] = T['ext']
    uf = T['uf']; mun = T['mun']; br = ~T['ext']
    n = len(uf)
    ex_uf = exato['por_uf']
    def soma_ex(campo, ufs=None):
        return sum(e.get(campo, 0) for u, e in ex_uf.items() if ufs is None or u in ufs)
    EX = {'N': soma_ex('N'), 'dcomp': soma_ex('comp2') - soma_ex('comp1'), 'dM': soma_ex('M2') - soma_ex('M1'),
          'A2': soma_ex('A2'), 'comp1': soma_ex('comp1'), 'comp2': soma_ex('comp2'), 'M1': soma_ex('M1'), 'M2': soma_ex('M2'),
          'E_M': soma_ex('E_M'), 'gL': soma_ex('L2') - soma_ex('L1'), 'gF': soma_ex('R2') - soma_ex('R1'),
          'L2': soma_ex('L2'), 'R2': soma_ex('R2'), 'O1': soma_ex('O1'), 'gBN': soma_ex('BN2') - soma_ex('BN1'),
          'apt1': soma_ex('apt1'), 'apt2': soma_ex('apt2'),
          'secoes_so_no_1t': exato['secoes_so_no_1t'], 'comp_das_secoes_so_no_1t': exato['comp_das_secoes_so_no_1t'],
          'dcomp_pais_com_a_secao_so_do_1t': soma_ex('comp2') - soma_ex('comp1') - exato['comp_das_secoes_so_no_1t'],
          'dM_pais_com_a_secao_so_do_1t': soma_ex('M2') - soma_ex('M1') - exato['M_das_secoes_so_no_1t'],
          'mesma_urna': soma_ex('mesma_urna'), 'mesmos_aptos': soma_ex('mesmos_aptos'),
          'exterior': {'N': ex_uf['ZZ']['N'], 'dcomp': ex_uf['ZZ']['comp2'] - ex_uf['ZZ']['comp1'], 'comp1': ex_uf['ZZ']['comp1'], 'comp2': ex_uf['ZZ']['comp2']}}
    assert EX['N'] == N_U
    R['exato_bweb_universo_2t'] = EX
    dB = a['B2'] - a['B1']; dM = a['M2'] - a['M1']; dS = a['S2'] - a['S1']; dSM = dS + dM; dC = a['comp2'] - a['comp1']
    gL = a['L2'] - a['L1']; gF = a['R2'] - a['R1']; gBN = a['BN2'] - a['BN1']; gO = -a['O1']
    assert np.all(dB + dM + dS == dC) and np.all(gL + gF + gBN + gO == dC)

    # ---- 1. Estimativas nacionais pela letra (D3) e conferência contra o exato
    est = {nome: tot_aas(x) for nome, x in (('dB', dB), ('dM', dM), ('dS', dS), ('dSM', dSM), ('dcomp', dC), ('gL', gL), ('gF', gF), ('gBN', gBN), ('gO', gO))}
    for nome, exv in (('dcomp', EX['dcomp']), ('dM', EX['dM']), ('gL', EX['gL']), ('gF', EX['gF']), ('gBN', EX['gBN']), ('gO', -EX['O1'])):
        est[nome]['exato'] = int(exv); est[nome]['z_contra_o_exato'] = (est[nome]['total'] - exv) / est[nome]['ep']
    niveis = {}
    for t in ('1', '2'):
        for X in ('B', 'M', 'S'):
            niveis[X + t] = tot_aas(a[X + t]); niveis['fracao_' + X + t] = razao(a[X + t], a['comp' + t])
        niveis['comp' + t] = tot_aas(a['comp' + t]); niveis['comp' + t]['exato'] = EX['comp' + t]
        niveis['comp' + t]['z_contra_o_exato'] = (niveis['comp' + t]['total'] - EX['comp' + t]) / niveis['comp' + t]['ep']
        niveis['M' + t]['exato'] = EX['M' + t]; niveis['M' + t]['z_contra_o_exato'] = (niveis['M' + t]['total'] - EX['M' + t]) / niveis['M' + t]['ep']
    amostra_coerente = abs(est['dcomp']['z_contra_o_exato']) < 3 and abs(est['dM']['z_contra_o_exato']) < 3
    R['nacional_pela_letra'] = {'variacoes': est, 'niveis_por_turno': niveis, 'amostra_coerente_com_o_exato': bool(amostra_coerente)}

    # ---- D4: estimador ancorado nos totais exatos
    Xg = np.column_stack([np.ones(n), dC, dM]).astype(float)
    bg, *_ = np.linalg.lstsq(Xg, dS.astype(float), rcond=None)
    res = dS - Xg @ bg
    mS_anc = dS.mean() + bg[1] * (EX['dcomp'] / N_U - dC.mean()) + bg[2] * (EX['dM'] / N_U - dM.mean())
    ep_anc = N_U * np.sqrt((1 - n / N_U) / n) * np.sqrt((res @ res) / (n - 3))
    TS_anc = N_U * mS_anc
    anc = {'coef_dS_sobre_dcomp': float(bg[1]), 'coef_dS_sobre_dM': float(bg[2]),
           'dS': {'total': float(TS_anc), 'ep': float(ep_anc), 'li95': float(TS_anc - 1.96 * ep_anc), 'ls95': float(TS_anc + 1.96 * ep_anc)},
           'dSM': {'total': float(EX['dM'] + TS_anc), 'ep': float(ep_anc), 'li95': float(EX['dM'] + TS_anc - 1.96 * ep_anc), 'ls95': float(EX['dM'] + TS_anc + 1.96 * ep_anc)},
           'dB': {'total': float(EX['dcomp'] - EX['dM'] - TS_anc), 'ep': float(ep_anc)},
           'fracao_B': {'razao': float((EX['dcomp'] - EX['dM'] - TS_anc) / EX['dcomp']), 'ep': float(ep_anc / EX['dcomp'])}}
    anc['fracao_B']['li95'] = anc['fracao_B']['razao'] - 1.96 * anc['fracao_B']['ep']; anc['fracao_B']['ls95'] = anc['fracao_B']['razao'] + 1.96 * anc['fracao_B']['ep']
    anc['fracao_M_exata'] = EX['dM'] / EX['dcomp']
    # só Brasil + exterior exato (D2)
    N_BR = N_U - EX['exterior']['N']; nbr = int(br.sum())
    def tot_br(x):
        x = np.asarray(x, float)[br]; s = x.std(ddof=1)
        ep = N_BR * s / np.sqrt(nbr) * np.sqrt(1 - nbr / N_BR)
        return {'total': float(N_BR * x.mean()), 'ep': float(ep), 'li95': float(N_BR * x.mean() - 1.96 * ep), 'ls95': float(N_BR * x.mean() + 1.96 * ep), 'n': nbr, 'N': int(N_BR)}
    sobr = {nome: tot_br(x) for nome, x in (('dB', dB), ('dM', dM), ('dS', dS), ('dSM', dSM), ('dcomp', dC))}
    sobr['dSM_brasil_mais_exterior_exato'] = {'total': sobr['dSM']['total'] + EX['exterior']['dcomp'], 'ep': sobr['dSM']['ep'],
                                              'ls95': sobr['dSM']['ls95'] + EX['exterior']['dcomp'], 'li95': sobr['dSM']['li95'] + EX['exterior']['dcomp']}
    sobr['exato_brasil'] = {'dcomp': EX['dcomp'] - EX['exterior']['dcomp'], 'dM': EX['dM']}
    R['ancorado_nos_exatos'] = anc; R['so_brasil'] = sobr

    # ---- D5: leitura dos 90%
    fB = razao(dB, dC); fM = razao(dM, dC); fS = razao(dS, dC); fSM = razao(dSM, dC)
    R['fracao_do_aumento_liquido'] = {'B': fB, 'M': fM, 'S': fS, 'S+M': fSM, 'B_ancorada': anc['fracao_B'], 'M_exata': anc['fracao_M_exata'],
                                      'teto_de_B_se_S_nao_cair': 1 - anc['fracao_M_exata'],
                                      'leitura_90_atendida_pela_letra': bool(fB['razao'] >= 0.90), 'intervalo_contem_0,90': bool(fB['li95'] <= 0.90 <= fB['ls95']),
                                      'leitura_90_atendida_ancorada': bool(anc['fracao_B']['razao'] >= 0.90),
                                      'intervalo_ancorado_contem_0,90': bool(anc['fracao_B']['li95'] <= 0.90 <= anc['fracao_B']['ls95'])}

    # ---- D11: excesso sobre a proporcionalidade
    c1ok = a['comp1'] > 0
    def exc(X):
        v = np.where(c1ok, a[X + '2'] - a[X + '1'] * a['comp2'] / np.maximum(a['comp1'], 1), 0.0)
        return tot_aas(v)
    R['excesso_sobre_a_proporcionalidade'] = {'B': exc('B'), 'M': exc('M'), 'S': exc('S'), 'M_exato_bweb': EX['E_M'],
                                              'secoes_da_amostra_sem_comparecimento_no_1t': int((~c1ok).sum())}
    R['excesso_sobre_a_proporcionalidade']['S+M'] = tot_aas(np.where(c1ok, (a['S2'] + a['M2']) - (a['S1'] + a['M1']) * a['comp2'] / np.maximum(a['comp1'], 1), 0.0))
    R['excesso_sobre_a_proporcionalidade']['M']['z_contra_o_exato'] = (R['excesso_sobre_a_proporcionalidade']['M']['total'] - EX['E_M']) / R['excesso_sobre_a_proporcionalidade']['M']['ep']

    # ---- 2. Regressões (D6, D7, D8)
    obs = nucleo(a, uf, mun, br, completo=True)
    rL, rF = obs['_rL'], obs['_rF']
    # conferência do erro agrupado por UF contra lib.fe_ols
    chk = fe_ols(gL[br], np.column_stack([dB[br], dSM[br]]), uf[br], nomes=['dB', 'dSM'])
    assert abs(chk['coef']['dSM'] - rL['coef']['dSM']) < 1e-9 and abs(chk['ep']['dSM'] - rL['ep_uf']['dSM']) < 1e-9, (chk, rL)
    Xl = np.column_stack([dB, dSM])
    regs = {'letra': {'Lula': rL, 'Flavio': rF,
                      'brancos_e_nulos': reg(gBN[br], Xl[br], uf[br], ['dB', 'dSM'], cl_mun=mun[br], contraste=(1, 0)),
                      'eliminados': reg(gO[br], Xl[br], uf[br], ['dB', 'dSM'], cl_mun=mun[br], contraste=(1, 0)),
                      'margem': reg((gL - gF)[br], Xl[br], uf[br], ['dB', 'dSM'], cl_mun=mun[br], contraste=(1, 0)),
                      'conferido_contra_lib_fe_ols': True}}
    # reamostragem das seções (erro ao lado, D4 e D7)
    rng = np.random.default_rng(SEMENTE)
    bt = {'T_SM': [], 'D_L': [], 'D_F': [], 'fracao_B': []}
    idx_all = np.arange(n)
    for _ in range(1000):
        ii = rng.choice(idx_all, n, replace=True)
        bb = ii[br[ii]]
        bt['T_SM'].append(N_U * dSM[ii].mean()); bt['fracao_B'].append(dB[ii].mean() / dC[ii].mean())
        try:
            r1 = reg(gL[bb], Xl[bb], uf[bb], ['dB', 'dSM'], contraste=(1, 0)); r2 = reg(gF[bb], Xl[bb], uf[bb], ['dB', 'dSM'], contraste=(1, 0))
            bt['D_L'].append(r1['contraste']); bt['D_F'].append(r2['contraste'])
        except Exception:
            pass
    R['reamostragem_das_secoes'] = {k: {'dp': float(np.std(v, ddof=1)), 'p2,5': float(np.percentile(v, 2.5)), 'p97,5': float(np.percentile(v, 97.5)), 'replicas': len(v)} for k, v in bt.items()}
    # (a) dM e dS separados
    X3 = np.column_stack([dB, dM, dS])
    regs['M_e_S_separados'] = {nm: reg(y[br], X3[br], uf[br], ['dB', 'dM', 'dS'], cl_mun=mun[br]) for nm, y in (('Lula', gL), ('Flavio', gF), ('margem', gL - gF))}
    for nm, y in (('Lula', gL), ('Flavio', gF)):
        regs['M_e_S_separados'][nm + '_contraste_M_menos_B'] = {k: v for k, v in reg(y[br], X3[br], uf[br], ['dB', 'dM', 'dS'], contraste=(1, 0)).items() if k.startswith('contraste')}
        regs['M_e_S_separados'][nm + '_contraste_S_menos_B'] = {k: v for k, v in reg(y[br], X3[br], uf[br], ['dB', 'dM', 'dS'], contraste=(2, 0)).items() if k.startswith('contraste')}
    # (b) com controles do 1º turno
    ctrl = np.column_stack([a['L1'], a['R1'], a['O1'], a['BN1'], a['apt1'] - a['comp1'], a['apt2'] - a['apt1']]).astype(float)
    Xc = np.column_stack([dB, dSM, ctrl]); nomes_c = ['dB', 'dSM', 'L1', 'R1', 'O1', 'BN1', 'abst1', 'daptos']
    regs['com_controles_do_1t'] = {nm: reg(y[br], Xc[br], uf[br], nomes_c, cl_mun=mun[br], contraste=(1, 0)) for nm, y in (('Lula', gL), ('Flavio', gF))}
    # (c) mesma urna e mesmos aptos
    est_ = br & (T['urna1'] == T['urna2']) & (a['apt1'] == a['apt2'])
    regs['mesma_urna_e_mesmos_aptos'] = {nm: reg(y[est_], Xl[est_], uf[est_], ['dB', 'dSM'], cl_mun=mun[est_], contraste=(1, 0)) for nm, y in (('Lula', gL), ('Flavio', gF))}
    regs['mesma_urna_e_mesmos_aptos']['secoes'] = int(est_.sum())
    regs['mesma_urna_e_mesmos_aptos']['secoes_com_urna_trocada'] = int((br & (T['urna1'] != T['urna2'])).sum())
    regs['mesma_urna_e_mesmos_aptos']['secoes_com_aptos_diferentes'] = int((br & (a['apt1'] != a['apt2'])).sum())
    # com o exterior (efeito fixo próprio)
    todos = np.ones(n, bool)
    regs['com_o_exterior'] = {nm: reg(y, Xl, uf, ['dB', 'dSM'], cl_mun=mun, contraste=(1, 0)) for nm, y in (('Lula', gL), ('Flavio', gF))}
    R['regressoes'] = regs
    R['observado_nucleo'] = {k: v for k, v in obs.items() if not k.startswith('_')}
    json.dump(R, open(f'{W}/parcial_observado.json', 'w'), ensure_ascii=False, indent=1)
    log('observado', {k: (round(v, 4) if isinstance(v, float) else v) for k, v in R['observado_nucleo'].items()})

    # ---- 3. Saídas (D9) e caudas (D10)
    def decomp_dom(ind, com_reg=True):
        o = {'secoes_na_amostra': int(ind.sum()), 'secoes_no_pais': tot_aas(ind.astype(float))}
        for nome, x in (('dB', dB), ('dM', dM), ('dS', dS), ('dSM', dSM), ('dcomp', dC), ('gL', gL), ('gF', gF), ('gBN', gBN), ('gO', gO)):
            o[nome] = dominio_tot(x, ind)
        if ind.sum() > 0:
            o['medias_por_secao'] = {nome: float(x[ind].mean()) for nome, x in (('dB', dB), ('dM', dM), ('dS', dS), ('dcomp', dC), ('gL', gL), ('gF', gF))}
            o['fracao_B_na_variacao'] = float(dB[ind].sum() / dC[ind].sum()) if dC[ind].sum() != 0 else None
        ib = ind & br
        if com_reg and ib.sum() >= 60:
            try:
                o['regressao_Lula'] = reg(gL[ib], Xl[ib], uf[ib], ['dB', 'dSM'], contraste=(1, 0))
                o['regressao_Flavio'] = reg(gF[ib], Xl[ib], uf[ib], ['dB', 'dSM'], contraste=(1, 0))
            except Exception as e:
                o['regressao_erro'] = repr(e)
        return o
    R['saidas_por_variacao_de_B'] = {'B_caiu': decomp_dom(dB < 0), 'B_igual': decomp_dom(dB == 0, False), 'B_subiu': decomp_dom(dB > 0)}
    R['saidas_por_variacao_do_comparecimento'] = {'caiu': decomp_dom(dC < 0), 'igual': decomp_dom(dC == 0, False), 'subiu': decomp_dom(dC > 0)}
    cau = {}
    for nome, x in (('S+M', dSM), ('M', dM), ('S', dS)):
        up = x >= 10; dn = x <= -10; meio = ~(up | dn)
        Xp = tot_aas(np.where(up, x, 0.0)); Xn = tot_aas(np.where(dn, x, 0.0)); As = tot_aas(np.where(up, x, 0.0) + np.where(dn, x, 0.0))
        c_ = {'subiu_10_ou_mais': {'na_amostra': int(up.sum()), 'no_pais': tot_aas(up.astype(float)), 'soma': Xp},
              'caiu_10_ou_mais': {'na_amostra': int(dn.sum()), 'no_pais': tot_aas(dn.astype(float)), 'soma': Xn},
              'assimetria_X+_menos_|X-|': As,
              'razao_de_contagens': float(up.sum() / dn.sum()) if dn.sum() else None,
              'diferenca_de_contagens_no_pais': tot_aas(up.astype(float) - dn.astype(float)),
              'soma_de_todas_as_altas': tot_aas(np.clip(x, 0, None)), 'soma_de_todas_as_quedas': tot_aas(np.clip(x, None, 0))}
        for rot, ind in (('subiu_10_ou_mais', up), ('caiu_10_ou_mais', dn), ('resto', meio)):
            if ind.sum():
                c_.setdefault(rot, {})['medias'] = {'dB': float(dB[ind].mean()), 'dM': float(dM[ind].mean()), 'dS': float(dS[ind].mean()), 'dcomp': float(dC[ind].mean()),
                                                    'gL': float(gL[ind].mean()), 'gF': float(gF[ind].mean()), 'gL_menos_gF': float((gL - gF)[ind].mean()),
                                                    'ep_gL_menos_gF': float((gL - gF)[ind].std(ddof=1) / np.sqrt(ind.sum())) if ind.sum() > 1 else None,
                                                    'urna_trocada': int((T['urna1'] != T['urna2'])[ind].sum()), 'aptos_diferentes': int((a['apt1'] != a['apt2'])[ind].sum()),
                                                    'comp2_medio': float(a['comp2'][ind].mean())}
        cau[nome] = c_
    # ganho de margem nas caudas além do que a regressão da letra prevê para o resto (descritivo)
    R['caudas'] = cau
    json.dump(R, open(f'{W}/parcial_saidas_caudas.json', 'w'), ensure_ascii=False, indent=1)

    # ---- 4. Regiões e UFs (D12)
    def dom(ufs, com_reg=True):
        ind = np.isin(uf, ufs); nd = int(ind.sum()); Nd = soma_ex('N', ufs)
        o = {'ufs': list(ufs), 'n': nd, 'N': int(Nd)}
        if nd < 2: return o
        def t_(x):
            x = np.asarray(x, float)[ind]; s = x.std(ddof=1); ep = Nd * s / np.sqrt(nd) * np.sqrt(1 - nd / Nd)
            return {'total': float(Nd * x.mean()), 'ep': float(ep), 'media_por_secao': float(x.mean())}
        for nome, x in (('dB', dB), ('dM', dM), ('dS', dS), ('dSM', dSM), ('dcomp', dC), ('gL', gL), ('gF', gF)):
            o[nome] = t_(x)
        o['exato'] = {'dcomp': int(soma_ex('comp2', ufs) - soma_ex('comp1', ufs)), 'dM': int(soma_ex('M2', ufs) - soma_ex('M1', ufs)),
                      'gL': int(soma_ex('L2', ufs) - soma_ex('L1', ufs)), 'gF': int(soma_ex('R2', ufs) - soma_ex('R1', ufs)),
                      'comp1': int(soma_ex('comp1', ufs)), 'E_M': float(soma_ex('E_M', ufs))}
        o['exato']['dcomp_sobre_comp1'] = o['exato']['dcomp'] / o['exato']['comp1']
        # ancorado no domínio com os coeficientes nacionais
        rd = (dS - Xg @ bg)[ind]
        mS = dS[ind].mean() + bg[1] * (o['exato']['dcomp'] / Nd - dC[ind].mean()) + bg[2] * (o['exato']['dM'] / Nd - dM[ind].mean())
        epd = Nd * np.sqrt((1 - nd / Nd) / nd) * rd.std(ddof=1)
        o['ancorado'] = {'dS': float(Nd * mS), 'ep': float(epd), 'dSM': float(o['exato']['dM'] + Nd * mS), 'dB': float(o['exato']['dcomp'] - o['exato']['dM'] - Nd * mS)}
        o['ancorado']['fracao_B'] = o['ancorado']['dB'] / o['exato']['dcomp'] if o['exato']['dcomp'] else None
        o['ancorado']['fracao_B_ep'] = float(epd / abs(o['exato']['dcomp'])) if o['exato']['dcomp'] else None
        o['ancorado']['fracao_SM'] = o['ancorado']['dSM'] / o['exato']['dcomp'] if o['exato']['dcomp'] else None
        if dC[ind].mean() != 0:
            o['fracao_B_amostral'] = razao(dB[ind], dC[ind], N=Nd)
        o['composicao_1t'] = {X: float(a[X + '1'][ind].sum() / a['comp1'][ind].sum()) for X in ('B', 'M', 'S')}
        o['composicao_2t'] = {X: float(a[X + '2'][ind].sum() / a['comp2'][ind].sum()) for X in ('B', 'M', 'S')}
        ok1 = ind & c1ok
        for X in ('B', 'M', 'S'):
            v = (a[X + '2'] - a[X + '1'] * a['comp2'] / np.maximum(a['comp1'], 1))[ok1]
            o.setdefault('excesso', {})[X] = {'total': float(Nd * v.sum() / nd), 'ep': float(Nd * np.where(ok1, a[X + '2'] - a[X + '1'] * a['comp2'] / np.maximum(a['comp1'], 1), 0.0)[ind].std(ddof=1) / np.sqrt(nd) * np.sqrt(1 - nd / Nd))}
        ib = ind & br
        if com_reg and ib.sum() >= 60 and len(set(uf[ib])) >= 1:
            fe_ = uf[ib]
            try:
                o['regressao_Lula'] = reg(gL[ib], Xl[ib], fe_, ['dB', 'dSM'], contraste=(1, 0))
                o['regressao_Flavio'] = reg(gF[ib], Xl[ib], fe_, ['dB', 'dSM'], contraste=(1, 0))
            except Exception as e:
                o['regressao_erro'] = repr(e)
        return o
    regioes = {nome: dom(ufs.split()) for nome, ufs in REGIOES.items()}
    R['por_regiao'] = regioes
    R['por_uf_dos_dois_grupos'] = {u: dom([u]) for u in G_ALTO + G_BAIXO}
    R['grupos_de_cinco'] = {'maior_diferenca_PI_MA_TO_PB_CE': dom(G_ALTO), 'menor_diferenca_RS_RJ_SC_SP_PR': dom(G_BAIXO),
                            'demais_UFs': dom(sorted(u for u in ex_uf if u not in G_ALTO + G_BAIXO and u != 'ZZ'))}
    R['todas_as_ufs_resumo'] = {u: {k: v for k, v in dom([u], False).items() if k in ('n', 'N', 'exato', 'ancorado', 'dSM', 'dB', 'dcomp')} for u in sorted(ex_uf)}
    json.dump(R, open(f'{W}/parcial_regioes.json', 'w'), ensure_ascii=False, indent=1)
    log('regiões prontas')

    # ---- 5. Calibração por efeito plantado (D13, D14)
    obs_n = R['observado_nucleo']
    B2_pais = niveis['B2']['total']
    cen = []
    for K, rot in ((L10, '10% da margem'), (L25, '25% da margem'), (MARGEM, 'margem inteira')):
        cen.append((f'PA mesa espalhada, {rot}', 'mesa', K, None, 'L'))
        cen.append((f'PB mesa concentrada, {rot}', 'mesa', K, 0.25 if K == MARGEM else 0.05, 'L'))
    cen.append(('PE espelho: mesa espalhada a favor de Flávio, 25% da margem', 'mesa', L25, None, 'R'))
    cen.append(('PE espelho: mesa concentrada a favor de Flávio, 25% da margem', 'mesa', L25, 0.05, 'R'))
    cen.append(('I1 abstenção pura de 3,6% dos votos de Flávio', 'abst', 0.036, None, 'R'))
    for K, rot in ((L10, '10% da margem'), (L25, '25% da margem'), (MARGEM, 'margem inteira')):
        cen.append((f'I2 eleitores reais para Lula espalhados, {rot}', 'reais', K, None, 'L'))
    cen.append(('I2 eleitores reais para Lula concentrados, 25% da margem', 'reais', L25, 0.05, 'L'))
    cen.append(('I2 eleitores reais para Lula concentrados, margem inteira', 'reais', MARGEM, 0.25, 'L'))
    cen.append(('I3 leitor pior espalhado, 25% da margem', 'leitor', L25, None, 'L'))
    cen.append(('I3 leitor pior concentrado, 25% da margem', 'leitor', L25, 0.05, 'L'))
    cal = {}
    rng = np.random.default_rng(SEMENTE + 1)
    for rot, tipo, K, frac, alvo in cen:
        copias = []; plantado = []
        for _ in range(REPS):
            c, tp = plantar(a, tipo, K, rng, EX['A2'], B2_pais, frac=frac, alvo=alvo)
            copias.append(nucleo(c, uf, mun, br)); plantado.append(tp)
        cal[rot] = resumo_copias(obs_n, copias, plantado, K if tipo != 'abst' else None)
        cal[rot].update({'tipo': tipo, 'K': K, 'fracao_das_secoes': frac, 'a_favor_de': 'Lula' if alvo == 'L' else 'Flávio'})
        json.dump(cal, open(f'{W}/parcial_calibracao.json', 'w'), ensure_ascii=False, indent=1)
        log('calibração', rot, 'T_SM +', round(cal[rot]['T_SM_delta_medio']), 'D_L', round(cal[rot]['D_L_media'], 3), 'c3', cal[rot]['fracao_c3_contraste'], 'SINAL', cal[rot]['fracao_SINAL'], 'SEM', cal[rot]['fracao_SEM_SINAL'])
    R['calibracao'] = cal
    pa25 = cal['PA mesa espalhada, 25% da margem']; pa10 = cal['PA mesa espalhada, 10% da margem']; pb25 = cal['PB mesa concentrada, 25% da margem']
    pam = cal['PA mesa espalhada, margem inteira']; pbm = cal['PB mesa concentrada, margem inteira']
    poder_nivel = (0.9 <= pa25['recuperacao_nivel'] <= 1.1) and pa25['fracao_SEM_SINAL'] <= 0.05 and pa10['fracao_SEM_SINAL'] <= 0.05
    ve_esp = pa25['fracao_c3_contraste'] >= 0.95; ve_con = pb25['fracao_c3_contraste'] >= 0.95
    ve_esp_m = pam['fracao_c3_contraste'] >= 0.95; ve_con_m = pbm['fracao_c3_contraste'] >= 0.95
    inoc = [k for k in cal if k.startswith('I2') or k.startswith('I3')]
    distingue = all(cal[k]['fracao_SINAL'] <= 0.05 for k in inoc)
    R['poder'] = {'nivel_enxerga': bool(poder_nivel), 'regressao_enxerga_espalhada_25': bool(ve_esp), 'regressao_enxerga_concentrada_25': bool(ve_con),
                  'regressao_enxerga_espalhada_margem_inteira': bool(ve_esp_m), 'regressao_enxerga_concentrada_margem_inteira': bool(ve_con_m),
                  'distingue_das_inocentes': bool(distingue),
                  'fracao_SINAL_pela_letra': {k: cal[k]['fracao_SINAL'] for k in cal},
                  'fracao_c3_nas_inocentes': {k: cal[k]['fracao_c3_contraste'] for k in inoc}}

    # ---- 6. Veredito (D15) e tradução (D16)
    tSM = est['dSM']
    c1 = tSM['total'] >= L25; c2 = tSM['li95'] >= L10
    DL, eL, zL = obs['D_L'], obs['D_L_ep'], obs['D_L_z']; DF, eF, zF = obs['D_F'], obs['D_F_ep'], obs['D_F_z']
    c3 = DL >= 0.25 and zL > 3
    sem = tSM['ls95'] < L10
    if sem: p1 = 'SEM SINAL' if poder_nivel else 'SEM PODER'
    elif c1 and c2: p1 = 'ACIMA DOS DOIS LIMIARES (condição de nível do SINAL presente)'
    else: p1 = 'INCONCLUSIVO'
    if c3: p2 = 'SINAL'
    elif not (ve_esp or ve_con): p2 = 'SEM PODER'
    elif DL + 1.96 * eL < 0.25: p2 = 'SEM SINAL'
    else: p2 = 'INCONCLUSIVO'
    p3 = 'ATENDIDA' if fB['razao'] >= 0.90 else 'NÃO ATENDIDA'
    if c1 and c2 and c3: comb = 'SINAL'
    elif sem: comb = 'SEM SINAL' if poder_nivel else 'SEM PODER'
    else: comb = 'INCONCLUSIVO'
    zL_uf = rL['contraste_z_uf']; c3_uf = DL >= 0.25 and zL_uf > 3
    sem_anc = anc['dSM']['ls95'] < L10; c1_anc = anc['dSM']['total'] >= L25; c2_anc = anc['dSM']['li95'] >= L10
    comb_anc = 'SINAL' if (c1_anc and c2_anc and c3) else ('SEM SINAL' if sem_anc else 'INCONCLUSIVO')
    R['veredito'] = {'parte_1_nivel_de_S+M': p1, 'parte_2_regressao': p2, 'parte_3_leitura_dos_90': p3, 'combinado_pela_letra': comb,
                     'condicoes': {'T_SM_ge_1107548': bool(c1), 'li95_ge_443019': bool(c2), 'D_L_ge_0,25_a_mais_de_3_ep': bool(c3), 'ls95_lt_443019': bool(sem)},
                     'com_erro_agrupado_por_UF': {'D_L_z': zL_uf, 'condicao_3': bool(c3_uf), 'muda_a_conclusao': bool(c3_uf != c3)},
                     'com_estimador_ancorado': {'combinado': comb_anc, 'diverge_da_letra': bool(comb_anc != comb)},
                     'espelho_Flavio': {'D_F': DF, 'ep': eF, 'z': zF, 'mostra_o_mesmo': bool(DF >= 0.25 and zF > 3)}}
    altas = cau['S+M']['soma_de_todas_as_altas']
    dd = DL - DF; e_dd = float(np.sqrt(eL ** 2 + eF ** 2))
    # erro de (D_L - D_F) pela regressão da margem (o contraste da margem é exatamente D_L - D_F)
    rm = regs['letra']['margem']; e_dd = rm['contraste_ep_hc1']; assert abs(rm['contraste'] - dd) < 1e-9
    trad_saldo = dd * tSM['total']; ep_ts = float(np.sqrt((dd * tSM['ep']) ** 2 + (tSM['total'] * e_dd) ** 2))
    trad_bruta = dd * altas['total']; ep_tb = float(np.sqrt((dd * altas['ep']) ** 2 + (altas['total'] * e_dd) ** 2))
    R['traducao_em_votos_de_margem'] = {
        'a_teto_pelo_saldo': {'T_SM': tSM['total'], 'fracao_da_margem': tSM['total'] / MARGEM, 'ls95': tSM['ls95'], 'ls95_fracao_da_margem': tSM['ls95'] / MARGEM,
                              'li95': tSM['li95'], 'li95_fracao_da_margem': tSM['li95'] / MARGEM,
                              'ancorado_T_SM': anc['dSM']['total'], 'ancorado_ls95': anc['dSM']['ls95'], 'ancorado_ls95_fracao_da_margem': anc['dSM']['ls95'] / MARGEM},
        'b_pela_regressao': {'D_L_menos_D_F': dd, 'ep': e_dd, 'x_saldo': trad_saldo, 'x_saldo_ep': ep_ts, 'x_saldo_fracao_da_margem': trad_saldo / MARGEM,
                             'x_bruto_das_altas': trad_bruta, 'x_bruto_ep': ep_tb, 'x_bruto_fracao_da_margem': trad_bruta / MARGEM,
                             'margem_por_eleitor_a_mais_em_S+M': rm['coef']['dSM'], 'margem_por_eleitor_a_mais_em_B': rm['coef']['dB']},
        'c_calibracao_da_traducao': {k: {'saldo_devolve': cal[k].get('traducao_saldo_devolve'), 'bruta_devolve': cal[k].get('traducao_bruta_devolve')} for k in cal if cal[k]['tipo'] in ('mesa', 'reais', 'leitor')},
        'excesso_sobre_a_proporcionalidade_S+M': R['excesso_sobre_a_proporcionalidade']['S+M'],
        'margem': MARGEM}
    R['contagem_de_testes'] = {'clausulas_com_veredito': 3, 'sinais_pela_letra': int(comb == 'SINAL') + int(p2 == 'SINAL'),
                               'nota': 'N1 tem um veredito combinado e três partes; o resto é descritivo e não foi desenhado para decidir.'}
    R['exploratorio_depois_de_ver_o_resultado'] = exploratorio(T, a, R, EX, exato, obs, cal, regs)
    R = limpar(R)
    json.dump(R, open(f'{W}/parcial_tudo.json', 'w'), ensure_ascii=False, indent=1)
    return R


PERFIL_A5 = '/home/user/trabalho-eleicao/adendo27/R27_A5/perfil_secao.json.gz'


def exploratorio(T, a, R, EX, exato, obs, cal, regs):
    """EXPLORATÓRIO: tudo aqui foi escolhido DEPOIS de ver o resultado da letra (rodada 1, 10/11/2026 05:38 UTC) e
    não muda nenhum veredito. Serve para ler o resultado: réguas inocentes alternativas para a entrada por S e M,
    caudas recentradas, o que a regressão enxerga de fato, o Brasil separado do exterior e uma lista de seções."""
    import re
    import numpy as np
    X = {'aviso': 'Exploratório: escolhido depois de ver o resultado da letra; não decide nada.'}
    n = len(T['uf']); uf = T['uf']; br = ~T['ext']
    dB = a['B2'] - a['B1']; dM = a['M2'] - a['M1']; dS = a['S2'] - a['S1']; dSM = dS + dM; dC = a['comp2'] - a['comp1']
    gL = a['L2'] - a['L1']; gF = a['R2'] - a['R1']
    anc = R['ancorado_nos_exatos']; niv = R['nacional_pela_letra']['niveis_por_turno']
    # X4 (vem antes porque o X1 usa): Brasil ancorado nos exatos do Brasil, mais o exterior exato
    N_BR = N_U - EX['exterior']['N']; nbr = int(br.sum())
    dcomp_br = EX['dcomp'] - EX['exterior']['dcomp']
    Xg = np.column_stack([np.ones(nbr), dC[br], dM[br]]).astype(float)
    bg = np.linalg.lstsq(Xg, dS[br].astype(float), rcond=None)[0]; rr = dS[br] - Xg @ bg
    mS = dS[br].mean() + bg[1] * (dcomp_br / N_BR - dC[br].mean()) + bg[2] * (EX['dM'] / N_BR - dM[br].mean())
    ep = float(N_BR * np.sqrt((1 - nbr / N_BR) / nbr) * np.sqrt((rr @ rr) / (nbr - 3)))
    TS = float(N_BR * mS)
    X['X4_brasil_e_exterior'] = {'brasil': {'dcomp_exato': int(dcomp_br), 'dM_exato': int(EX['dM']), 'dS_ancorado': TS, 'ep': ep, 'dSM': EX['dM'] + TS,
                                             'dSM_li95': EX['dM'] + TS - 1.96 * ep, 'dSM_ls95': EX['dM'] + TS + 1.96 * ep,
                                             'dB': dcomp_br - EX['dM'] - TS, 'fracao_B': (dcomp_br - EX['dM'] - TS) / dcomp_br, 'fracao_B_ep': ep / dcomp_br,
                                             'dSM_sobre_a_margem': (EX['dM'] + TS) / MARGEM, 'dSM_ls95_sobre_a_margem': (EX['dM'] + TS + 1.96 * ep) / MARGEM},
                                 'exterior_exato': {'dcomp': int(EX['exterior']['dcomp']), 'comp1': int(EX['exterior']['comp1']), 'variacao_relativa': EX['exterior']['dcomp'] / EX['exterior']['comp1'],
                                                    'gL': int(exato['por_uf']['ZZ']['L2'] - exato['por_uf']['ZZ']['L1']), 'gF': int(exato['por_uf']['ZZ']['R2'] - exato['por_uf']['ZZ']['R1'])},
                                 'pais_brasil_ancorado_mais_exterior_exato': {'dSM': EX['dM'] + TS + EX['exterior']['dcomp'], 'ep': ep,
                                                                              'li95': EX['dM'] + TS + EX['exterior']['dcomp'] - 1.96 * ep, 'ls95': EX['dM'] + TS + EX['exterior']['dcomp'] + 1.96 * ep,
                                                                              'sobre_a_margem': (EX['dM'] + TS + EX['exterior']['dcomp']) / MARGEM,
                                                                              'ls95_sobre_a_margem': (EX['dM'] + TS + EX['exterior']['dcomp'] + 1.96 * ep) / MARGEM}}
    # X1: réguas inocentes para a entrada dos eleitores a mais, só no Brasil (no exterior não há biometria)
    perfil = json.load(gzip.open(PERFIL_A5))['secoes']
    tot_el = sum(v[0] for k, v in perfil.items() if not k.startswith('ZZ|')); tot_bio = sum(v[1] for k, v in perfil.items() if not k.startswith('ZZ|'))
    pop2 = json.load(gzip.open(f'{W}/bweb_pop_2t.json.gz'))['secoes']
    el = np.zeros(n); bio = np.zeros(n); tem = np.zeros(n, bool)
    for i, k in enumerate(T['chave']):
        if k.startswith('ZZ|'): continue
        u, mun, zona, sec = k.split('|'); partes = [k]
        agr = pop2[k][8]
        if agr != '#NULO#':
            partes += [f'{u}|{mun}|{zona}|{int(x)}' for x in re.findall(r'\d+', agr)]
        if all(p_ in perfil for p_ in partes):
            el[i] = sum(perfil[p_][0] for p_ in partes); bio[i] = sum(perfil[p_][1] for p_ in partes); tem[i] = True
    nb = el - bio; BM1 = a['B1'] + a['M1']; BM2 = a['B2'] + a['M2']
    def rz(num, den, m):
        r = razao(num[m], den[m]); return {'razao': r['razao'], 'ep': r['ep']}
    tS1 = rz(a['S1'].astype(float), nb, tem); tS2 = rz(a['S2'].astype(float), nb, tem); tdS = rz(dS.astype(float), nb, tem)
    tB1 = rz(BM1.astype(float), bio, tem); tB2 = rz(BM2.astype(float), bio, tem); tdB = rz((dB + dM).astype(float), bio, tem)
    m = tem; rS = dS[m].sum() / nb[m].sum(); rB = (dB + dM)[m].sum() / bio[m].sum()
    u_ = (dS[m] - rS * nb[m]) / nb[m].mean() - ((dB + dM)[m] - rB * bio[m]) / bio[m].mean()
    ep_dif = float(np.sqrt((1 - m.sum() / N_U) / m.sum()) * u_.std(ddof=1))
    S1_frac = float(a['S1'][br].sum() / a['comp1'][br].sum()); B1_frac = float(a['B1'][br].sum() / a['comp1'][br].sum())
    M1_frac = EX['M1'] / (EX['comp1'] - EX['exterior']['comp1'])
    falt1_nb = (nb - a['S1'])[tem].sum(); falt1 = (el - a['comp1'])[tem].sum()
    xb = X['X4_brasil_e_exterior']['brasil']
    esp_b_S = rB * (tot_el - tot_bio)
    esp_b_M = (dcomp_br - esp_b_S) * (EX['M1'] / (EX['comp1'] - EX['exterior']['comp1'])) / (1 - S1_frac)
    X['X1_reguas_inocentes_no_brasil'] = {
        'perfil_do_eleitorado_do_brasil': {'eleitores': int(tot_el), 'com_biometria': int(tot_bio), 'sem_biometria': int(tot_el - tot_bio), 'fracao_sem_biometria': (tot_el - tot_bio) / tot_el,
                                           'secoes_da_amostra_com_perfil': int(tem.sum()), 'com_eleitores_do_perfil_iguais_aos_aptos_do_2t': int((el == a['apt2'])[tem].sum()),
                                           'secoes_com_S_maior_que_o_estoque_sem_biometria_do_perfil': {'1t': int((a['S1'] > nb)[tem].sum()), '2t': int((a['S2'] > nb)[tem].sum())},
                                           'secoes_com_B+M_maior_que_o_estoque_com_biometria_do_perfil': {'1t': int((BM1 > bio)[tem].sum()), '2t': int((BM2 > bio)[tem].sum())},
                                           'nota': 'O perfil (cadastro de 14/07/2026) não é o estoque exato do dia: os aptos da seção diferem do perfil na maioria das seções e mudam entre os turnos em 11% delas (a soma nacional é igual). Por isso "S maior que o estoque" não vale como contagem impossível; as taxas são aproximadas.'},
        'comparecimento_dos_eleitores_sem_biometria': {'1t': tS1, '2t': tS2, 'variacao_em_pontos': {'valor': 100 * tdS['razao'], 'ep': 100 * tdS['ep']}},
        'comparecimento_dos_eleitores_com_biometria': {'1t': tB1, '2t': tB2, 'variacao_em_pontos': {'valor': 100 * tdB['razao'], 'ep': 100 * tdB['ep']}},
        'diferenca_das_variacoes_em_pontos_sem_menos_com': {'valor': 100 * (rS - rB), 'ep': 100 * ep_dif,
                                                           'em_eleitores_no_brasil': (rS - rB) * (tot_el - tot_bio), 'ls95_em_eleitores': (rS - rB + 1.96 * ep_dif) * (tot_el - tot_bio),
                                                           'li95_em_eleitores': (rS - rB - 1.96 * ep_dif) * (tot_el - tot_bio)},
        'fracao_sem_biometria_entre_os_faltosos_do_1t_na_amostra': float(falt1_nb / falt1),
        'dS_esperado_no_brasil': {'a_proporcional_ao_comparecimento_do_1t': S1_frac * dcomp_br, 'b_mesma_variacao_em_pontos_dos_eleitores_com_biometria': esp_b_S,
                                  'c_proporcional_aos_faltosos_do_1t': float(falt1_nb / falt1) * dcomp_br,
                                  'observado_amostra': R['so_brasil']['dS']['total'], 'observado_amostra_ep': R['so_brasil']['dS']['ep'],
                                  'observado_ancorado': xb['dS_ancorado'], 'observado_ancorado_ep': xb['ep']},
        'dM_esperado_no_brasil': {'a_proporcional_ao_comparecimento_do_1t': M1_frac * dcomp_br, 'b_proporcional_aos_eleitores_com_biometria_que_entraram': esp_b_M,
                                  'observado_exato': EX['dM'], 'excesso_exato_por_secao_D11': EX['E_M']},
        'dSM_esperado_no_brasil': {'a': S1_frac * dcomp_br + M1_frac * dcomp_br, 'b': esp_b_S + esp_b_M, 'observado_ancorado': xb['dSM'],
                                   'sobra_sobre_a': xb['dSM'] - (S1_frac + M1_frac) * dcomp_br, 'sobra_sobre_b': xb['dSM'] - esp_b_S - esp_b_M, 'ep_da_sobra': xb['ep']},
        'fracao_de_B_esperada_no_brasil': {'a_proporcional_ao_comparecimento_do_1t': B1_frac, 'b_mesmos_pontos_por_tipo_de_eleitor_e_M_proporcional': (dcomp_br - esp_b_S - esp_b_M) / dcomp_br,
                                           'observada_ancorada': xb['fracao_B'], 'ep': xb['fracao_B_ep']}}
    # X2: caudas recentradas na média e resíduo de margem nas caudas
    mu = dSM.mean(); z = dSM - mu
    up = z >= 10; dn = z <= -10
    Xl = np.column_stack([dB, dSM]).astype(float)
    _, g = np.unique(uf, return_inverse=True); G = g.max() + 1
    def dm(v):
        return v - (np.bincount(g, weights=v, minlength=G) / np.bincount(g, minlength=G))[g]
    yd = dm((gL - gF).astype(float)); Xd = np.column_stack([dm(Xl[:, 0]), dm(Xl[:, 1])])
    bb = np.linalg.lstsq(Xd, yd, rcond=None)[0]; res = yd - Xd @ bb
    # resíduo de margem contra o canal B: quanto a margem ficou acima do que os mesmos eleitores a mais dariam se fossem do canal B
    exc_B = dm((gL - gF).astype(float)) - bb[0] * (Xd[:, 0] + Xd[:, 1])
    up0 = dSM >= 10; dn0 = dSM <= -10
    def med(v, m_):
        return {'media': float(v[m_].mean()), 'ep': float(v[m_].std(ddof=1) / np.sqrt(m_.sum())), 'n': int(m_.sum())}
    sk = float(((z / dSM.std(ddof=1)) ** 3).mean())
    X['X2_caudas'] = {'media_de_d(S+M)': float(mu), 'dp': float(dSM.std(ddof=1)), 'assimetria_de_Fisher': sk,
                      'recentradas_na_media': {'subiu_10_ou_mais': int(up.sum()), 'caiu_10_ou_mais': int(dn.sum()), 'razao': float(up.sum() / dn.sum()) if dn.sum() else None,
                                               'diferenca_no_pais': tot_aas(up.astype(float) - dn.astype(float))},
                      'margem_nas_caudas_da_letra': {'residuo_da_regressao_da_margem': {'subiu_10_ou_mais': med(res, up0), 'caiu_10_ou_mais': med(res, dn0)},
                                                     'margem_acima_do_que_daria_o_canal_B': {'subiu_10_ou_mais': med(exc_B, up0), 'caiu_10_ou_mais': med(exc_B, dn0)},
                                                     'd(S+M)_medio_na_cauda_de_alta': float(dSM[up0].mean()),
                                                     'se_tudo_fosse_voto_lancado_para_Lula_a_margem_ficaria_acima_do_canal_B_em': float((1 - bb[0]) * dSM[up0].mean())}}
    # X3: o que a regressão enxerga (sem o limiar de 0,25, que tem teto)
    eL = obs['D_L_ep']; eF = obs['D_F_ep']
    X['X3_o_que_a_regressao_enxerga'] = {
        'teto_do_contraste_de_Lula': 1 - obs['bL_B'], 'teto_do_contraste_de_Flavio_no_espelho': 1 - obs['bF_B'],
        'nota': 'O contraste de Lula não pode passar de 1 menos o coeficiente de B (um eleitor a mais não rende mais que um voto). Com o coeficiente de B em 0,74, o limiar registrado de 0,25 fica colado no teto de 0,26.',
        'cenarios': {k: {'delta_D_L': c['D_L_delta_medio'], 'delta_D_L_em_ep_do_observado': c['D_L_delta_medio'] / eL, 'delta_D_F': c['D_F_delta_medio'],
                         'delta_D_F_em_ep_do_observado': c['D_F_delta_medio'] / eF,
                         'fracao_das_copias_com_D_L_a_mais_de_3_ep': None, 'D_L_z_medio': c['D_L_z_media'], 'D_F_z_medio': c['D_F_z_media']} for k, c in cal.items()},
        'observado': {'D_L': obs['D_L'], 'D_L_ep': eL, 'D_F': obs['D_F'], 'D_F_ep': eF,
                      'com_controles': {'D_L': regs['com_controles_do_1t']['Lula']['contraste'], 'ep': regs['com_controles_do_1t']['Lula']['contraste_ep_hc1'],
                                        'D_F': regs['com_controles_do_1t']['Flavio']['contraste'], 'ep_F': regs['com_controles_do_1t']['Flavio']['contraste_ep_hc1']}}}
    # X5: saldo de S + M contra a virada de margem do lugar
    x5 = {}
    for nome, o in list(R['grupos_de_cinco'].items()) + list(R['por_regiao'].items()) + list(R['por_uf_dos_dois_grupos'].items()):
        if 'exato' not in o: continue
        vm = o['exato']['gL'] - o['exato']['gF']
        x5[nome] = {'d(S+M)_ancorado': o['ancorado']['dSM'], 'ep': o['ancorado']['ep'], 'ganho_de_Lula_menos_ganho_de_Flavio_exato': vm,
                    'razao': o['ancorado']['dSM'] / vm if vm else None, 'dcomp_exato': o['exato']['dcomp'], 'dM_exato': o['exato']['dM'], 'excesso_de_M_exato': o['exato']['E_M']}
    X['X5_saldo_de_S+M_contra_a_virada_do_lugar'] = x5
    # X7: seções da amostra para conferência de caderno (maiores altas de S + M; todas as altas de S de 10 ou mais)
    ordem = np.argsort(-dSM)[:30]
    def lin(i):
        return {'secao': str(T['chave'][i]), 'dB': int(dB[i]), 'dM': int(dM[i]), 'dS': int(dS[i]), 'dcomp': int(dC[i]), 'ganho_Lula': int(gL[i]), 'ganho_Flavio': int(gF[i]),
                'comp2': int(a['comp2'][i]), 'aptos_1t_2t': [int(a['apt1'][i]), int(a['apt2'][i])], 'urna_trocada': bool(T['urna1'][i] != T['urna2'][i])}
    X['X7_secoes_para_conferencia'] = {'trinta_maiores_altas_de_S+M_na_amostra': [lin(i) for i in ordem],
                                       'altas_de_S_de_10_ou_mais': [lin(i) for i in np.nonzero(dS >= 10)[0]],
                                       'nota': 'Amostra aleatória: cada seção listada representa cerca de 166 no país. A lista não acusa a seção; serve para pedir caderno de votação e ata.'}
    return X


def conferir_sorteio():
    """Refaz o sorteio registrado (ordem do SHA-256 de semente + chave) no universo do bweb do 2º turno lido aqui."""
    reg_ = json.load(open(os.path.join(REPO, 'registro/adendo27/sorteio_aas.json')))
    pop2 = json.load(gzip.open(f'{W}/bweb_pop_2t.json.gz'))['secoes']
    ks = sorted(pop2)
    o = sorted(ks, key=lambda k: hashlib.sha256((reg_['semente'] + '|' + k).encode('utf-8')).hexdigest())[:3000]
    lista = amostra()
    return {'universo': len(ks), 'sha256_universo_confere': hashlib.sha256('\n'.join(ks).encode()).hexdigest() == reg_['sha256_universo'],
            'sha256_da_lista_confere': hashlib.sha256(('\n'.join(lista) + '\n').encode()).hexdigest() == reg_['sha256_principal'],
            'sorteio_refeito_igual_a_lista': o == lista}


def limpar(o):
    """Troca NaN e infinito por None e tipos do numpy por tipos do Python, para o JSON sair válido."""
    import math
    import numpy as np
    if isinstance(o, dict):
        return {str(k): limpar(v) for k, v in o.items() if not str(k).startswith('_')}
    if isinstance(o, (list, tuple)):
        return [limpar(v) for v in o]
    if isinstance(o, (np.bool_,)):
        return bool(o)
    if isinstance(o, np.integer):
        return int(o)
    if isinstance(o, (float, np.floating)):
        o = float(o)
        return o if math.isfinite(o) else None
    if isinstance(o, np.ndarray):
        return limpar(o.tolist())
    return o


# ---------------------------------------------------------------------------------------------------------------
# Texto e JSON finais
# ---------------------------------------------------------------------------------------------------------------
def fi(x):
    if x is None: return 'n/d'
    return f'{int(round(x)):,}'.replace(',', '.')


def fs(x):
    if x is None: return 'n/d'
    return ('+' if x >= 0 else '-') + fi(abs(x))


def fz(x, d=3):
    if x is None: return 'n/d'
    return f'{x:.{d}f}'.replace('.', ',')


def fzs(x, d=3):
    if x is None: return 'n/d'
    return ('+' if x >= 0 else '-') + fz(abs(x), d)


def pc(x, d=1):
    if x is None: return 'n/d'
    return fz(100 * x, d) + '%'


def escrever(R):
    V = R['nacional_pela_letra']['variacoes']; NV = R['nacional_pela_letra']['niveis_por_turno']; anc = R['ancorado_nos_exatos']
    EX = R['exato_bweb_universo_2t']; fr = R['fracao_do_aumento_liquido']; rg = R['regressoes']; cal = R['calibracao']
    X = R['exploratorio_depois_de_ver_o_resultado']; ver = R['veredito']; tr = R['traducao_em_votos_de_margem']; ob = R['observado_nucleo']
    cf = R['conferencia_boletim_bweb']; ex = R['excesso_sobre_a_proporcionalidade']; cau = R['caudas']; sd = R['saidas_por_variacao_de_B']
    x1 = X['X1_reguas_inocentes_no_brasil']; x2 = X['X2_caudas']; x3 = X['X3_o_que_a_regressao_enxerga']; x4 = X['X4_brasil_e_exterior']; x5 = X['X5_saldo_de_S+M_contra_a_virada_do_lugar']
    rL = rg['letra']['Lula']; rF = rg['letra']['Flavio']; rM = rg['letra']['margem']; sp = rg['M_e_S_separados']
    cL = rg['com_controles_do_1t']['Lula']; cF = rg['com_controles_do_1t']['Flavio']
    sm = V['dSM']; g5a = R['grupos_de_cinco']['maior_diferenca_PI_MA_TO_PB_CE']; g5b = R['grupos_de_cinco']['menor_diferenca_RS_RJ_SC_SP_PR']
    pais = x4['pais_brasil_ancorado_mais_exterior_exato']; xb = x4['brasil']
    pa10 = cal['PA mesa espalhada, 10% da margem']; pa25 = cal['PA mesa espalhada, 25% da margem']; pam = cal['PA mesa espalhada, margem inteira']
    pb10 = cal['PB mesa concentrada, 10% da margem']; pb25 = cal['PB mesa concentrada, 25% da margem']; pbm = cal['PB mesa concentrada, margem inteira']
    i1 = cal['I1 abstenção pura de 3,6% dos votos de Flávio']; i2m = cal['I2 eleitores reais para Lula espalhados, margem inteira']; i2_25 = cal['I2 eleitores reais para Lula espalhados, 25% da margem']
    i3e = cal['I3 leitor pior espalhado, 25% da margem']; i3c = cal['I3 leitor pior concentrado, 25% da margem']
    pee = cal['PE espelho: mesa espalhada a favor de Flávio, 25% da margem']; pec = cal['PE espelho: mesa concentrada a favor de Flávio, 25% da margem']
    nl = sum(cf['por_turno'][t]['linhas_de_voto_comparadas'] for t in ('1', '2'))
    cup = cau['S+M']['subiu_10_ou_mais']; cdn = cau['S+M']['caiu_10_ou_mais']
    x2m = x2['margem_nas_caudas_da_letra']

    resumo = (f"INCONCLUSIVO pela letra: o canal sem biometria (S + M) ganhou {fi(sm['total'])} eleitores entre os turnos (ep {fi(sm['ep'])}; "
              f"{fi(anc['dSM']['total'])} com os totais exatos do bweb como âncora), {pc(sm['total'] / MARGEM)} a {pc(anc['dSM']['total'] / MARGEM)} da margem: acima do limiar de 10% que "
              f"daria SEM SINAL e muito abaixo do de 25% que daria SINAL; B responde por {pc(anc['fracao_B']['razao'])} a {pc(fr['B']['razao'])} do aumento, não por 90%; "
              f"o eleitor a mais de S + M rende a Lula o mesmo que o de B ({fz(ob['bL_SM'], 2)} contra {fz(ob['bL_B'], 2)}), mas essa cláusula não tinha poder; S subiu o que a régua inocente prevê e o que passa da régua é a alta de M, "
              f"de {fi(EX['E_M'])} a {fi(EX['dM'] - x1['dM_esperado_no_brasil']['b_proporcional_aos_eleitores_com_biometria_que_entraram'])} liberações.")
    v1 = (f"Parte 1, nível de S + M: {ver['parte_1_nivel_de_S+M']}. Variação estimada de S + M = {fs(sm['total'])} (ep {fi(sm['ep'])}; IC 95% de {fi(sm['li95'])} a {fi(sm['ls95'])}; n = 3.000), "
          f"{pc(sm['total'] / MARGEM)} da margem (IC de {pc(sm['li95'] / MARGEM)} a {pc(sm['ls95'] / MARGEM)}). Não chega a 1.107.548 (falta {fz((L25 - sm['total']) / sm['ep'], 1)} ep) e o limite superior não desce abaixo de 443.019. "
          f"Com os totais exatos como âncora: {fs(anc['dSM']['total'])} (ep {fi(anc['dSM']['ep'])}; IC de {fi(anc['dSM']['li95'])} a {fi(anc['dSM']['ls95'])}), mesmo veredito.")
    v2 = (f"Parte 2, regressão: {ver['parte_2_regressao']}. Coeficiente de Lula em S + M {fz(ob['bL_SM'])} contra {fz(ob['bL_B'])} em B; contraste D_L = {fzs(ob['D_L'])} (ep {fz(ob['D_L_ep'])}; {fz(ob['D_L_z'], 2)} ep), longe de 0,25. "
          f"A condição não se cumpre, mas não podia se cumprir: o contraste tem teto de {fz(x3['teto_do_contraste_de_Lula'])} (1 menos o coeficiente de B) e na calibração nem a margem inteira plantada pela mesa chega a 0,25 "
          f"(D_L médio de {fz(pam['D_L_media'])} espalhada e {fz(pbm['D_L_media'])} concentrada; 0% das cópias cumprem).")
    v3 = (f"Parte 3, leitura dos 90%: {ver['parte_3_leitura_dos_90']}. B responde por {pc(fr['B']['razao'])} do aumento líquido (ep {fz(100 * fr['B']['ep'], 1)} ponto; IC 95% de {pc(fr['B']['li95'])} a {pc(fr['B']['ls95'])}); "
          f"ancorado nos exatos, {pc(anc['fracao_B']['razao'])} (IC de {pc(anc['fracao_B']['li95'])} a {pc(anc['fracao_B']['ls95'])}). Aviso da calibração: a leitura também não seria atendida com entrada inocente de eleitores reais "
          f"(B é {pc(NV['fracao_B1']['razao'])} do comparecimento do 1º turno; 0% das cópias inocentes passam de 90%).")
    vc = f"Combinado pela letra: {ver['combinado_pela_letra']} (nem SINAL, nem SEM SINAL). Espelho (Flávio): D_F = {fzs(ob['D_F'])} (ep {fz(ob['D_F_ep'])}), não mostra o mesmo."

    favor = [
        f"A leitura fixada antes NÃO foi atendida: B (digital reconhecida) responde por {pc(fr['B']['razao'])} do aumento líquido pela letra e {pc(anc['fracao_B']['razao'])} com os totais exatos, não por 90%. "
        f"S + M, que eram {pc(NV['fracao_S1']['razao'] + NV['fracao_M1']['razao'])} do comparecimento do 1º turno, carregam {pc(1 - anc['fracao_B']['razao'])} do aumento.",
        f"O teste não consegue dizer SEM SINAL: o saldo de S + M é de {fi(sm['total'])} (letra) a {fi(anc['dSM']['total'])} (ancorado) eleitores e o limite inferior de 95% ({fi(sm['li95'])}; ancorado {fi(anc['dSM']['li95'])}) fica acima de 10% da margem.",
        f"Os canais sem biometria cresceram mais depressa que o da digital: B {fzs(100 * V['dB']['total'] / NV['B1']['total'], 2)}%, M {fzs(100 * EX['dM'] / EX['M1'], 2)}% (exato), S {fzs(100 * V['dS']['total'] / NV['S1']['total'], 2)}%. "
        f"Sobre o que a composição do 1º turno daria, sobram {fs(ex['S']['total'])} em S (ep {fi(ex['S']['ep'])}) e {fs(EX['E_M'])} em M (exato, bweb inteiro).",
        f"A alta de M (liberação pelo mesário) passa das réguas de proporção: M subiu {fi(EX['dM'])} (exato) quando a proporção daria de {fi(x1['dM_esperado_no_brasil']['b_proporcional_aos_eleitores_com_biometria_que_entraram'])} a {fi(x1['dM_esperado_no_brasil']['a_proporcional_ao_comparecimento_do_1t'])}. "
        f"A sobra, de {fi(EX['E_M'])} a {fi(EX['dM'] - x1['dM_esperado_no_brasil']['b_proporcional_aos_eleitores_com_biometria_que_entraram'])} liberações ({pc(EX['E_M'] / MARGEM)} a {pc((EX['dM'] - x1['dM_esperado_no_brasil']['b_proporcional_aos_eleitores_com_biometria_que_entraram']) / MARGEM)} da margem), pode ser leitor pior ou liberação indevida, e o boletim não separa. Ela está no Nordeste "
        f"(excesso exato de M {fs(R['por_regiao']['Nordeste']['exato']['E_M'])}) e no RJ ({fs(R['por_uf_dos_dois_grupos']['RJ']['exato']['E_M'])}). No PI o comparecimento ficou parado ({fs(R['por_uf_dos_dois_grupos']['PI']['exato']['dcomp'])}) "
        f"e M subiu {fi(R['por_uf_dos_dois_grupos']['PI']['exato']['dM'])}; no MA o comparecimento caiu {fi(-R['por_uf_dos_dois_grupos']['MA']['exato']['dcomp'])} e M subiu {fi(R['por_uf_dos_dois_grupos']['MA']['exato']['dM'])}.",
        f"Nas cinco UFs de maior diferença (PI, MA, TO, PB, CE) B responde por só {pc(g5a['ancorado']['fracao_B'])} do aumento líquido (ep {fz(100 * g5a['ancorado']['fracao_B_ep'], 1)} ponto), contra {pc(g5b['ancorado']['fracao_B'])} nas cinco de menor (RS, RJ, SC, SP, PR). Ressalva: nas cinco de maior o saldo é pequeno ({fzs(100 * g5a['exato']['dcomp_sobre_comp1'], 2)}% do comparecimento), então a fração é de pouca coisa.",
        f"Caudas: há {fz(cau['S+M']['razao_de_contagens'], 2)} seções com S + M subindo 10 ou mais para cada seção caindo 10 ou mais ({fi(cup['no_pais']['total'])} contra {fi(cdn['no_pais']['total'])} no país; "
        f"assimetria de {fs(cau['S+M']['assimetria_X+_menos_|X-|']['total'])} eleitores, {fz(cau['S+M']['assimetria_X+_menos_|X-|']['total'] / cau['S+M']['assimetria_X+_menos_|X-|']['ep'], 1)} ep). "
        f"Nas seções de alta o comparecimento subiu {fz(cup['medias']['dcomp'], 1)} com B caindo {fz(-cup['medias']['dB'], 1)}: ali todo o aumento entrou sem digital reconhecida.",
        f"O eleitor a mais de S (sem biometria no cadastro) rende a Lula {fz(sp['Lula']['coef']['dS'], 2)} voto e a Flávio {fz(sp['Flavio']['coef']['dS'], 2)}, contra {fz(sp['Lula']['coef']['dB'], 2)} e {fz(sp['Flavio']['coef']['dB'], 2)} no canal B: a direção é a da tese, sem passar de {fz(sp['Lula_contraste_S_menos_B']['contraste_z_hc1'], 1)} ep.",
        f"A regressão é cega para voto lançado de forma espalhada: 25% da margem plantados assim mexem o contraste em só {fzs(pa25['D_L_delta_medio'])}, do mesmo tamanho do contraste observado ({fzs(ob['D_L'])}). Ela não absolve essa forma.",
        "Limite do teste, dito antes: saldo esconde entradas compensadas por saídas no mesmo canal, e todos os campos saem do programa da urna. N1 não pesa contra a hipótese de programa que registre biometria falsa.",
    ]
    contra = [
        f"Tamanho: mesmo que cada eleitor a mais de S e de M fosse um voto lançado pela mesa para Lula, seriam {fi(anc['dSM']['total'])} votos (teto de 95%: {fi(anc['dSM']['ls95'])}), {pc(anc['dSM']['total'] / MARGEM)} da margem (teto {pc(anc['dSM']['ls95'] / MARGEM)}). "
        f"Faltam {fz((L25 - sm['total']) / sm['ep'], 1)} ep para o limiar de SINAL pela letra. Pelo menos 85% da margem não entrou, em saldo, por S nem por M.",
        f"S subiu o que a régua inocente prevê: o comparecimento dos eleitores sem biometria subiu {fz(x1['comparecimento_dos_eleitores_sem_biometria']['variacao_em_pontos']['valor'], 2)} ponto (de {pc(x1['comparecimento_dos_eleitores_sem_biometria']['1t']['razao'])} para {pc(x1['comparecimento_dos_eleitores_sem_biometria']['2t']['razao'])}) "
        f"e o dos eleitores com biometria {fz(x1['comparecimento_dos_eleitores_com_biometria']['variacao_em_pontos']['valor'], 2)} ponto (de {pc(x1['comparecimento_dos_eleitores_com_biometria']['1t']['razao'])} para {pc(x1['comparecimento_dos_eleitores_com_biometria']['2t']['razao'])}). "
        f"Diferença de {fz(x1['diferenca_das_variacoes_em_pontos_sem_menos_com']['valor'], 2)} ponto (ep {fz(x1['diferenca_das_variacoes_em_pontos_sem_menos_com']['ep'], 2)}): {fs(x1['diferenca_das_variacoes_em_pontos_sem_menos_com']['em_eleitores_no_brasil'])} eleitores, no máximo {fs(x1['diferenca_das_variacoes_em_pontos_sem_menos_com']['ls95_em_eleitores'])} (exploratório). "
        f"Se a mesa votasse por quem faltou, o alvo fácil seria o eleitor sem biometria (59% deles faltam e basta o ano de nascimento); o comparecimento deles não subiu mais que o dos outros.",
        f"O eleitor a mais de S + M divide o voto como o eleitor a mais de B: Lula {fz(ob['bL_SM'])} contra {fz(ob['bL_B'])}, Flávio {fz(ob['bF_SM'])} contra {fz(ob['bF_B'])}. Voto lançado para Lula daria 1 e 0. "
        f"Para cada 100 eleitores a mais em S + M, Flávio ganhou {fz(100 * ob['bF_SM'], 0)} votos ({fz(rF['coef']['dSM'] / rF['ep_hc1']['dSM'], 0)} ep acima de zero). Em S sozinho, que não sofre com erro de leitor, Flávio ganha {fz(sp['Flavio']['coef']['dS'], 2)} por eleitor a mais ({fz(sp['Flavio']['coef']['dS'] / sp['Flavio']['ep_hc1']['dS'], 1)} ep acima de zero). Com controles do 1º turno os contrastes são {fzs(cL['contraste'])} (ep {fz(cL['contraste_ep_hc1'])}) e {fzs(cF['contraste'])} (ep {fz(cF['contraste_ep_hc1'])}).",
        f"Forma concentrada: 10% da margem lançados pela mesa em 5% das seções mexeriam o contraste de Flávio em {fzs(pb10['D_F_delta_medio'])} ({fz(abs(pb10['D_F_delta_medio']) / ob['D_F_ep'], 1)} ep) e 25% em {fzs(pb25['D_F_delta_medio'])}; o observado é {fzs(ob['D_F'])} (ep {fz(ob['D_F_ep'])}). "
        f"Essa forma teria aparecido (leitura exploratória, sem o limiar de 0,25).",
        f"A assimetria das caudas é só o deslocamento da média: recentrando na média de {fzs(x2['media_de_d(S+M)'], 2)}, são {x2['recentradas_na_media']['subiu_10_ou_mais']} seções da amostra acima de +10 contra {x2['recentradas_na_media']['caiu_10_ou_mais']} abaixo de -10. "
        f"Nas seções de alta a margem de Lula ficou {fzs(x2m['margem_acima_do_que_daria_o_canal_B']['subiu_10_ou_mais']['media'], 2)} voto (ep {fz(x2m['margem_acima_do_que_daria_o_canal_B']['subiu_10_ou_mais']['ep'], 2)}) acima do que os mesmos eleitores dariam pelo canal B; "
        f"se a alta fosse voto lançado, ficaria {fzs(x2m['se_tudo_fosse_voto_lancado_para_Lula_a_margem_ficaria_acima_do_canal_B_em'], 1)} (exploratório).",
        f"M anda ao contrário de B, como reclassificação do mesmo eleitor: nas {fi(sd['B_caiu']['secoes_no_pais']['total'])} seções em que B caiu ({fs(sd['B_caiu']['dB']['total'])}), M subiu {fi(sd['B_caiu']['dM']['total'])}; onde B subiu ({fs(sd['B_subiu']['dB']['total'])}), M caiu {fi(-sd['B_subiu']['dM']['total'])}. "
        f"O plantio de 'leitor pior' reproduz alta de S + M sem mudar voto nenhum.",
        f"Onde o indício da Onda A é mais forte, o canal sem biometria é pequeno: em PI, MA, TO, PB e CE o saldo de S + M é {fs(g5a['ancorado']['dSM'])} (ep {fi(g5a['ancorado']['ep'])}), {pc(x5['maior_diferenca_PI_MA_TO_PB_CE']['razao'])} da virada de margem dessas UFs "
        f"({fi(x5['maior_diferenca_PI_MA_TO_PB_CE']['ganho_de_Lula_menos_ganho_de_Flavio_exato'])} votos). No país, {pc(anc['dSM']['total'] / (EX['gL'] - EX['gF']))} da virada de {fi(EX['gL'] - EX['gF'])}.",
        f"Boletim igual ao bweb em 3.000 de 3.000 seções nos dois turnos ({fi(nl)} linhas de voto, aptos, comparecimento e M), sorteio refeito e igual à lista. Isso fecha alteração depois da urna nessas seções; não diz nada sobre o programa.",
        "A leitura dos 90% falharia mesmo sem fraude: B é 87,6% do comparecimento, então entrada proporcional de eleitores reais dá menos de 90%. A falha da leitura, sozinha, não é indício.",
    ]
    m_sobra = EX['dM'] - x1['dM_esperado_no_brasil']['b_proporcional_aos_eleitores_com_biometria_que_entraram']
    saida_f = 0.0267 * (EX['R2'] - EX['gF']) * (NV['fracao_S1']['razao'] + NV['fracao_M1']['razao'])
    lista_s = X['X7_secoes_para_conferencia']['altas_de_S_de_10_ou_mais']
    ufs_s = collections.Counter(l['secao'].split('|')[0] for l in lista_s)
    significado = (
        f"N1 não decide a tese e estreita o caminho da mesa. Os votos a mais entraram em sua maior parte ({pc(anc['fracao_B']['razao'])} a {pc(fr['B']['razao'])}) por eleitores cuja digital a urna registrou como reconhecida, e o restante "
        f"({fi(anc['dSM']['total'])} eleitores, {pc(anc['dSM']['total'] / MARGEM)} da margem) por S e M. Desse restante, S está na régua inocente e a parte que passa da régua é a alta de M, da ordem de {fi(EX['E_M'])} a {fi(m_sobra)} "
        f"liberações ({pc(EX['E_M'] / MARGEM)} a {pc(m_sobra / MARGEM)} da margem). Voto lançado pela mesa não pode ser o portador da margem em saldo (teto de {pc(anc['dSM']['ls95'] / MARGEM)}); "
        f"somando ao saldo a saída de eleitores de Flávio que a Onda A estimou (2,67% dos votos dele no 1º turno, dos quais cerca de {fi(saida_f)} votariam por S ou M), o teto fica perto de {pc((anc['dSM']['ls95'] + saida_f) / MARGEM, 0)} da margem (conta ilustrativa, exploratória). "
        f"A leitura registrada (B com 90% ou mais) não foi atendida e o critério de SEM SINAL também não: fica INCONCLUSIVO. "
        f"O 'dobro da taxa' da Onda A reaparece aqui dentro do canal da digital: cada eleitor a mais em B rende {fz(ob['bL_B'], 2)} voto a Lula e {fz(ob['bF_B'], 2)} a Flávio. Portanto, se a virada pelo comparecimento for irregular, "
        f"a irregularidade teria de estar no registro da biometria pelo programa (que dado público não testa) ou na retirada de eleitores de Flávio (que boletim não distingue de abstenção). As duas só se decidem com caderno de votação. "
        f"Se for mobilização desigual, é o que estes números mostram sem precisar de mais nada.")
    pistas = [
        f"Liberação manual (M) no Nordeste e no RJ: excesso exato de M de {fs(R['por_regiao']['Nordeste']['exato']['E_M'])} no Nordeste (PI {fs(R['por_uf_dos_dois_grupos']['PI']['exato']['E_M'])}, MA {fs(R['por_uf_dos_dois_grupos']['MA']['exato']['E_M'])}, "
        f"CE {fs(R['por_uf_dos_dois_grupos']['CE']['exato']['E_M'])}, PB {fs(R['por_uf_dos_dois_grupos']['PB']['exato']['E_M'])}) e {fs(R['por_uf_dos_dois_grupos']['RJ']['exato']['E_M'])} no RJ, contra {fs(R['por_uf_dos_dois_grupos']['PR']['exato']['E_M'])} no PR e {fs(R['por_uf_dos_dois_grupos']['SP']['exato']['E_M'])} em SP. "
        "É o objeto do B2 (D2-1) e do C1 (logs: quem liberou e a que horas): começar por PI e MA, onde M subiu com o comparecimento parado ou caindo.",
        f"Cadernos de votação: pedir primeiro nas seções da amostra com as maiores altas de S + M (lista de 30 no JSON, campo X7) e nas seções de PI, MA, PB e CE em que M subiu e B caiu. Cada seção da amostra representa cerca de 166 do país.",
        f"Exterior: sem biometria nenhuma, o comparecimento subiu {fi(x4['exterior_exato']['dcomp'])} ({pc(x4['exterior_exato']['variacao_relativa'])}), com Lula {fs(x4['exterior_exato']['gL'])} e Flávio {fs(x4['exterior_exato']['gF'])}. É onde a mesa não deixa marca no boletim; liga com o A5.",
        f"Seções com muito eleitor sem biometria (RS com S de {pc(R['por_uf_dos_dois_grupos']['RS']['composicao_2t']['S'])} do comparecimento, RJ {pc(R['por_uf_dos_dois_grupos']['RJ']['composicao_2t']['S'])}, contra PR {pc(R['por_uf_dos_dois_grupos']['PR']['composicao_2t']['S'])}): "
        f"as {len(lista_s)} seções da amostra com S subindo 10 ou mais estão listadas no JSON ({ufs_s.get('ZZ', 0)} no exterior; as outras em " + ', '.join(f'{u} {q}' for u, q in sorted(ufs_s.items()) if u != 'ZZ') + ").",
        "Perfil do comparecimento do 2º turno (o TSE ainda não publicou): com ele dá para refazer a régua de S por idade, que aqui é só aproximada pelo cadastro de julho.",
        "O que N1 não alcança: programa que registre biometria falsa e eleitor de Flávio dado como ausente. Para os dois, só caderno de votação e o comprovante no e-Título, nas UFs do indício.",
    ]
    desvios = [
        "Nenhum limiar foi mudado. Decisões que o registro não fixava foram escritas no docstring antes de qualquer conta com votos (SHA-256 do docstring no JSON; cópia em /home/user/trabalho-eleicao/adendo27/R27_N1/docstring_antes_de_rodar.txt, 05:37 UTC).",
        "D2: nas 10 seções do exterior, que não trazem o campo de habilitações, S = comparecimento, B = M = 0. Só com o Brasil o saldo de S + M é " + f"{fi(R['so_brasil']['dSM']['total'])} (ep {fi(R['so_brasil']['dSM']['ep'])}); ancorado, {fi(xb['dSM'])} (ep {fi(xb['ep'])}). O veredito não muda.",
        "D6 e D7: a regressão usa as 2.990 seções do Brasil, sem peso, com erro robusto por seção (HC1). Com erro agrupado por UF (o de lib.fe_ols) " + f"o contraste fica a {fz(ver['com_erro_agrupado_por_UF']['D_L_z'], 2)} ep; a conclusão não muda.",
        "D4: o estimador ancorado nos totais exatos do bweb vai ao lado; o veredito é o da letra e os dois coincidem.",
        "D14 e D15: a regra de poder e os rótulos por parte são meus. Por ela a cláusula da regressão é SEM PODER: o limiar registrado de 0,25 fica colado no teto de 0,257 e nenhuma irregularidade plantada o alcança. O SINAL pela letra não podia ocorrer para Lula (para Flávio podia: o espelho plantado concentrado dispara em 100% das cópias).",
        "Leitura dos 90% julgada pela estimativa pontual (D5). Ela é inatingível também na entrada inocente plantada; isso é dito no veredito.",
        "PB com a margem inteira usa 25% das seções em vez de 5% (em 5% não cabem os votos); o I3 usa a soma de B estimada pela amostra.",
        "Ordem dos fatos: a extração do bweb e dos boletins rodou primeiro por uma cópia das mesmas funções na pasta de trabalho (extrair_N1.py), sem conta nenhuma; depois foi refeita pelo script final e o resultado é idêntico. Antes do docstring, um boletim (PI, 10090, zona 8, seção 116) foi aberto para ver o formato e mostrou os votos dessa seção.",
        "Exploratório (escolhido depois de ver o resultado, não decide nada): réguas inocentes X1 (com o perfil do eleitorado extraído pelo A5, que não refiz), caudas recentradas X2, leitura da regressão sem o limiar X3, Brasil separado do exterior X4, saldo contra a virada por lugar X5 e lista de seções X7.",
        "O exato do comparecimento no universo do sorteio é +2.960.241 (o +2.960.239 nacional inclui uma seção do exterior que só existiu no 1º turno, com 2 votos).",
        "Não há comparação com outro ano neste teste: todos os números são os brutos de 2026.",
    ]
    arquivos = [os.path.join(REPO, 'scripts/analisar_R27_N1.py'), OUT_JSON, OUT_TXT,
                f'{W}/docstring_antes_de_rodar.txt', f'{W}/docstring_antes_de_rodar.sha256', f'{W}/analisar_R27_N1_antes_de_rodar.py',
                f'{W}/bu_amostra.json', f'{W}/bweb_amostra_1t.json', f'{W}/bweb_amostra_2t.json', f'{W}/bweb_pop_1t.json.gz', f'{W}/bweb_pop_2t.json.gz',
                f'{W}/parcial_tudo.json', f'{W}/parcial_calibracao.json']
    R['resumo'] = {'veredito_em_uma_frase': resumo, 'parte_1': v1, 'parte_2': v2, 'parte_3': v3, 'combinado': vc, 'a_favor_da_tese': favor, 'contra_a_tese': contra,
                   'o_que_isso_significa': significado, 'pistas': pistas, 'desvios': desvios, 'arquivos': arquivos,
                   'fixado_antes': 'Tudo o que está em nacional_pela_letra, ancorado_nos_exatos, so_brasil, fracao_do_aumento_liquido, excesso_sobre_a_proporcionalidade, regressoes, saidas, caudas, por_regiao, por_uf, grupos_de_cinco, calibracao, poder, veredito e traducao foi decidido no docstring antes de rodar (critério do Adendo 28; decisões D1 a D17).',
                   'exploratorio': 'Só o bloco exploratorio_depois_de_ver_o_resultado (X1 a X7).'}
    R = limpar(R)
    json.dump(R, open(OUT_JSON, 'w'), ensure_ascii=False, indent=1)

    L = []
    w = L.append
    def par(t, ind=0, larg=118):
        import textwrap
        for linha in textwrap.wrap(t, larg - ind, break_long_words=False, break_on_hyphens=False):
            w(' ' * ind + linha)
    w('R27 N1: POR ONDE ENTRARAM OS VOTOS A MAIS (Adendo 28, teste N1)')
    w('')
    par(f"Registro: PRE-REGISTRO-2026-10-26.md, Adendo 28 (commit 938be19, 10/11/2026 04:36:33 UTC), antes de rodar. Decisões que o registro não fixa: docstring de scripts/analisar_R27_N1.py, fechado às 05:37 UTC de 10/11/2026 antes de qualquer conta com votos (SHA-256 {R['docstring_sha256'][:16]}...). Dados: boletins de urna dos dois turnos das 3.000 seções da amostra aleatória simples nova (universo de 499.205 seções do 2º turno), conferidos contra o bweb.")
    par("B = eleitor com a digital reconhecida pela urna. M = eleitor com biometria liberado pelo mesário. S = eleitor sem biometria no cadastro. Margem do 2º turno: 4.430.191. Limiares: 25% da margem = 1.107.548; 10% = 443.019.")
    w('')
    w('VEREDITO PELA LETRA')
    for t in (v1, v2, v3, vc):
        par(t, 2)
    par('Em uma frase: ' + resumo, 2)
    w('')
    w('1. CONFERÊNCIA DOS BOLETINS CONTRA O BWEB (achado, se houvesse diferença)')
    for t in ('1', '2'):
        c = cf['por_turno'][t]
        par(f"{t}º turno: {fi(c['boletins'])} boletins lidos; chave igual {fi(c['chave_igual'])}; aptos iguais {fi(c['aptos_iguais'])}; comparecimento igual {fi(c['comparecimento_igual'])}; com as três contagens {fi(c['com_tres_contagens'])} "
            f"(as {c['sem_tres_contagens']} sem o campo são do exterior, com M = 0 no bweb); S + B + M igual ao comparecimento {fi(c['S+B+M_igual_ao_comparecimento'])}; M igual ao QT_ELEI_BIOM_SEM_HABILITACAO {fi(c['M_igual_ao_bweb'])}; "
            f"votos de Presidente iguais ao bweb, candidato a candidato, brancos e nulos {fi(c['votos_iguais_ao_bweb'])} ({fi(c['linhas_de_voto_comparadas'])} linhas); iguais à base do repositório {fi(c['igual_a_base_do_repositorio'])}.", 2)
    par(f"Diferenças encontradas: {len(cf['diferencas'])}. Sorteio refeito com a semente registrada no universo lido aqui: {'igual à lista' if R['conferencia_do_sorteio']['sorteio_refeito_igual_a_lista'] else 'DIFERENTE da lista'}; SHA-256 da lista e do universo conferem: {'sim' if R['conferencia_do_sorteio']['sha256_da_lista_confere'] and R['conferencia_do_sorteio']['sha256_universo_confere'] else 'NÃO'}.", 2)
    par("Limite: boletim, bweb e log saem do mesmo programa. A igualdade fecha alteração depois da urna nessas seções e não pesa contra a hipótese de programa adulterado na origem.", 2)
    w('')
    w('2. ESTIMATIVAS NACIONAIS DA VARIAÇÃO ENTRE OS TURNOS (letra: média x 499.205, erro de amostra aleatória simples)')
    w('     canal            estimativa     ep        IC 95%                       exato (bweb)   z contra o exato')
    for nome, rot in (('dB', 'B (digital)'), ('dM', 'M (mesário)'), ('dS', 'S (sem biom.)'), ('dSM', 'S + M'), ('dcomp', 'comparecimento')):
        v = V[nome]
        w(f"     {rot:<15} {fs(v['total']):>11} {fi(v['ep']):>8}   {fi(v['li95']):>10} a {fi(v['ls95']):<10}   {(fs(v['exato']) if 'exato' in v else 'não existe'):>12}   {(fzs(v['z_contra_o_exato'], 2) if 'z_contra_o_exato' in v else ''):>6}")
    par(f"A amostra bate com o que se sabe exato: comparecimento {fs(V['dcomp']['total'])} contra {fs(EX['dcomp'])} ({fzs(V['dcomp']['z_contra_o_exato'], 2)} ep) e M {fs(V['dM']['total'])} contra {fs(EX['dM'])} ({fzs(V['dM']['z_contra_o_exato'], 2)} ep). "
        f"Votos: ganho de Lula {fs(V['gL']['total'])} contra {fs(EX['gL'])} exato; ganho de Flávio {fs(V['gF']['total'])} contra {fs(EX['gF'])}.", 2)
    par(f"Ancorado nos totais exatos (ao lado): S {fs(anc['dS']['total'])} (ep {fi(anc['dS']['ep'])}); S + M {fs(anc['dSM']['total'])} (IC de {fi(anc['dSM']['li95'])} a {fi(anc['dSM']['ls95'])}); B {fs(anc['dB']['total'])}. "
        f"Só o Brasil, ancorado: S + M {fs(xb['dSM'])} (IC de {fi(xb['dSM_li95'])} a {fi(xb['dSM_ls95'])}); exterior, exato: {fs(x4['exterior_exato']['dcomp'])}, tudo contado como S. Erro por reamostragem das seções: {fi(R['reamostragem_das_secoes']['T_SM']['dp'])} (igual ao da fórmula).", 2)
    par(f"Níveis: no 1º turno B era {pc(NV['fracao_B1']['razao'], 2)} do comparecimento, M {pc(NV['fracao_M1']['razao'], 2)} e S {pc(NV['fracao_S1']['razao'], 2)}; no 2º, {pc(NV['fracao_B2']['razao'], 2)}, {pc(NV['fracao_M2']['razao'], 2)} e {pc(NV['fracao_S2']['razao'], 2)}. "
        f"Crescimento: B {fzs(100 * V['dB']['total'] / NV['B1']['total'], 2)}%, M {fzs(100 * EX['dM'] / EX['M1'], 2)}% (exato), S {fzs(100 * V['dS']['total'] / NV['S1']['total'], 2)}%, comparecimento {fzs(100 * EX['dcomp'] / EX['comp1'], 2)}% (exato).", 2)
    par(f"Excesso sobre a composição do 1º turno da própria seção (D11): S {fs(ex['S']['total'])} (ep {fi(ex['S']['ep'])}); M {fs(ex['M']['total'])} (ep {fi(ex['M']['ep'])}) pela amostra e {fs(EX['E_M'])} exato no bweb inteiro; B {fs(ex['B']['total'])} (ep {fi(ex['B']['ep'])}).", 2)
    w('')
    w('3. LEITURA DOS 90%')
    par(f"Fração do aumento líquido: B {pc(fr['B']['razao'])} (ep {fz(100 * fr['B']['ep'], 1)}), M {pc(fr['M']['razao'])} (exato {pc(fr['M_exata'])}), S {pc(fr['S']['razao'])} (ep {fz(100 * fr['S']['ep'], 1)}). Ancorada: B {pc(anc['fracao_B']['razao'])} (IC de {pc(anc['fracao_B']['li95'])} a {pc(anc['fracao_B']['ls95'])}). "
        f"Como M sozinho já é {pc(fr['M_exata'])} do aumento, o teto de B era {pc(fr['teto_de_B_se_S_nao_cair'])} se S não subisse nada. NÃO ATENDIDA. O intervalo não contém 90%.", 2)
    par(f"O que a leitura valia: plantando eleitores reais para Lula (canal sorteado na composição da seção), a fração de B fica em {pc(i2_25['fracao_B_media'])} com 25% da margem e {pc(i2m['fracao_B_media'])} com a margem inteira. Nunca chega a 90%. A leitura não separava as duas hipóteses.", 2)
    w('')
    w('4. REGRESSÃO POR SEÇÃO (efeito fixo de UF, 2.990 seções do Brasil, votos ganhos por eleitor a mais no canal)')
    w('     desfecho                 coef. em B (ep)      coef. em S + M (ep)   contraste (ep)        ep por UF   ep por município')
    for nome, r in (('ganho de Lula', rL), ('ganho de Flávio (espelho)', rF), ('brancos e nulos (placebo)', rg['letra']['brancos_e_nulos']), ('eliminados', rg['letra']['eliminados']), ('margem (Lula - Flávio)', rM)):
        w(f"     {nome:<25} {fzs(r['coef']['dB']):>7} ({fz(r['ep_hc1']['dB'])})   {fzs(r['coef']['dSM']):>7} ({fz(r['ep_hc1']['dSM'])})    {fzs(r['contraste']):>7} ({fz(r['contraste_ep_hc1'])})   {fz(r['contraste_ep_uf']):>7}     {fz(r['contraste_ep_mun']):>7}")
    par(f"Critério: contraste de Lula de 0,25 ou mais a mais de 3 ep. Observado {fzs(ob['D_L'])}, a {fz(ob['D_L_z'], 2)} ep (por UF {fz(rL['contraste_z_uf'], 2)}; reamostragem: ep {fz(R['reamostragem_das_secoes']['D_L']['dp'])}). Espelho de Flávio {fzs(ob['D_F'])}, a {fz(ob['D_F_z'], 2)} ep.", 2)
    par(f"Ao lado. M e S separados, Lula: B {fz(sp['Lula']['coef']['dB'])}, M {fz(sp['Lula']['coef']['dM'])} (ep {fz(sp['Lula']['ep_hc1']['dM'])}), S {fz(sp['Lula']['coef']['dS'])} (ep {fz(sp['Lula']['ep_hc1']['dS'])}); Flávio: B {fz(sp['Flavio']['coef']['dB'])}, M {fz(sp['Flavio']['coef']['dM'])} (ep {fz(sp['Flavio']['ep_hc1']['dM'])}), S {fz(sp['Flavio']['coef']['dS'])} (ep {fz(sp['Flavio']['ep_hc1']['dS'])}). "
        f"Contraste S menos B: Lula {fzs(sp['Lula_contraste_S_menos_B']['contraste'])} ({fz(sp['Lula_contraste_S_menos_B']['contraste_z_hc1'], 2)} ep), Flávio {fzs(sp['Flavio_contraste_S_menos_B']['contraste'])} ({fz(sp['Flavio_contraste_S_menos_B']['contraste_z_hc1'], 2)} ep). "
        f"Com controles do 1º turno: D_L {fzs(cL['contraste'])} (ep {fz(cL['contraste_ep_hc1'])}), D_F {fzs(cF['contraste'])} (ep {fz(cF['contraste_ep_hc1'])}). "
        f"Mesma urna e mesmos aptos ({fi(rg['mesma_urna_e_mesmos_aptos']['secoes'])} seções): D_L {fzs(rg['mesma_urna_e_mesmos_aptos']['Lula']['contraste'])} (ep {fz(rg['mesma_urna_e_mesmos_aptos']['Lula']['contraste_ep_hc1'])}), D_F {fzs(rg['mesma_urna_e_mesmos_aptos']['Flavio']['contraste'])} (ep {fz(rg['mesma_urna_e_mesmos_aptos']['Flavio']['contraste_ep_hc1'])}). "
        f"Com as 10 do exterior: D_L {fzs(rg['com_o_exterior']['Lula']['contraste'])}, D_F {fzs(rg['com_o_exterior']['Flavio']['contraste'])}.", 2)
    w('')
    w('5. CALIBRAÇÃO POR EFEITO PLANTADO NOS DADOS DE 2026 (200 cópias por cenário, semente 20261110)')
    w('     cenário                                                        plantado   alta de S+M   fração B   D_L     D_F    nível>=25%  contraste  SINAL  SEM SINAL')
    for k, c in cal.items():
        w(f"     {k[:62]:<62} {fi(c['plantado_medio_expandido']):>9} {fs(c['T_SM_delta_medio']):>12}   {pc(c['fracao_B_media']):>7}  {fzs(c['D_L_media']):>6} {fzs(c['D_F_media']):>6}    {pc(c['fracao_c1_T_ge_25'], 0):>5}      {pc(c['fracao_c3_contraste'], 0):>5}   {pc(c['fracao_SINAL'], 0):>4}    {pc(c['fracao_SEM_SINAL'], 0):>4}")
    par(f"Nível: o teste enxerga. A quantia plantada pela mesa volta inteira na estimativa de S + M (recuperação de {fz(pa25['recuperacao_nivel'], 3)}) e nenhuma cópia com 10% da margem plantados é absolvida. "
        f"O nível sozinho não separa mesa de leitor pior (I3 sobe S + M do mesmo tanto) nem de entrada grande de eleitores reais (a margem inteira em eleitores reais sobe S + M em {fi(i2m['T_SM_delta_medio'])}).", 2)
    par(f"Regressão: SEM PODER no limiar registrado. O contraste de Lula sobe para {fz(pa25['D_L_media'])} (espalhada) e {fz(pb25['D_L_media'])} (concentrada) com 25% da margem, e para {fz(pam['D_L_media'])} e {fz(pbm['D_L_media'])} com a margem inteira; 0,25 nunca é alcançado. "
        f"Motivo: o eleitor a mais de B já rende {fz(ob['bL_B'])} voto a Lula, então o teto do contraste é {fz(x3['teto_do_contraste_de_Lula'])}. No espelho o teto é {fz(x3['teto_do_contraste_de_Flavio_no_espelho'])}: a mesma fraude a favor de Flávio, concentrada, daria D_F de {fz(pec['D_F_media'])} e dispararia em {pc(pec['fracao_espelho_c3'], 0)} das cópias. "
        f"O critério registrado ficou, sem que isso tivesse sido notado ao registrar, alcançável a favor de Flávio e inalcançável a favor de Lula.", 2)
    par(f"O que a regressão enxerga sem o limiar (exploratório): forma concentrada sim (10% da margem mexe D_F em {fzs(pb10['D_F_delta_medio'])}, {fz(abs(pb10['D_F_delta_medio']) / ob['D_F_ep'], 1)} ep do observado; 25% em {fzs(pb25['D_F_delta_medio'])}); forma espalhada não (25% mexe D_L em {fzs(pa25['D_L_delta_medio'])} e D_F em {fzs(pa25['D_F_delta_medio'])}, cerca de 1 ep).", 2)
    par(f"Distinção: nenhuma explicação inocente plantada vira SINAL (0% das cópias), mas só porque nada vira. Abstenção pura de 3,6% dos votos de Flávio derruba o saldo de S + M em {fi(-i1['T_SM_delta_medio'])} e faria o teste dizer SEM SINAL em {pc(i1['fracao_SEM_SINAL'], 0)} das cópias: o saldo mistura entrada e saída. "
        f"Retirada de eleitores de Flávio do registro deixa o mesmo boletim que abstenção: este teste não a vê.", 2)
    w('')
    w('6. SAÍDAS (seções em que B caiu) E CAUDAS')
    w('     domínio        seções no país     dB            dM           dS          dcomp        ganho Lula   ganho Flávio')
    for nome, rot in (('B_caiu', 'B caiu'), ('B_igual', 'B igual'), ('B_subiu', 'B subiu')):
        d = sd[nome]
        w(f"     {rot:<12} {fi(d['secoes_no_pais']['total']):>10} ({d['secoes_na_amostra']:>4})  {fs(d['dB']['total']):>11}  {fs(d['dM']['total']):>10}  {fs(d['dS']['total']):>10}  {fs(d['dcomp']['total']):>11}  {fs(d['gL']['total']):>11}  {fs(d['gF']['total']):>11}")
    par(f"Erros-padrão no JSON (dM onde B caiu: {fi(sd['B_caiu']['dM']['ep'])}; dS onde B subiu: {fi(sd['B_subiu']['dS']['ep'])}). Onde B caiu, mais da metade da queda reaparece em M; S quase não se mexe ({fs(sd['B_caiu']['dS']['total'])}). Onde B subiu, S sobe junto ({fs(sd['B_subiu']['dS']['total'])}) e M cai. "
        f"Regressão dentro de 'B caiu': Lula {fz(sd['B_caiu']['regressao_Lula']['coef']['dB'])} em B e {fz(sd['B_caiu']['regressao_Lula']['coef']['dSM'])} em S + M (contraste {fzs(sd['B_caiu']['regressao_Lula']['contraste'])}, ep {fz(sd['B_caiu']['regressao_Lula']['contraste_ep_hc1'])}); "
        f"Flávio {fz(sd['B_caiu']['regressao_Flavio']['coef']['dB'])} e {fz(sd['B_caiu']['regressao_Flavio']['coef']['dSM'])} (contraste {fzs(sd['B_caiu']['regressao_Flavio']['contraste'])}, ep {fz(sd['B_caiu']['regressao_Flavio']['contraste_ep_hc1'])}).", 2)
    for nome in ('S+M', 'M', 'S'):
        c = cau[nome]
        par(f"Caudas de {nome}: subiu 10 ou mais em {c['subiu_10_ou_mais']['na_amostra']} seções da amostra ({fi(c['subiu_10_ou_mais']['no_pais']['total'])} no país, soma {fs(c['subiu_10_ou_mais']['soma']['total'])}); caiu 10 ou mais em {c['caiu_10_ou_mais']['na_amostra']} ({fi(c['caiu_10_ou_mais']['no_pais']['total'])}, soma {fs(c['caiu_10_ou_mais']['soma']['total'])}); "
            f"assimetria {fs(c['assimetria_X+_menos_|X-|']['total'])} (ep {fi(c['assimetria_X+_menos_|X-|']['ep'])}). Todas as altas somadas: {fs(c['soma_de_todas_as_altas']['total'])}; todas as quedas: {fs(c['soma_de_todas_as_quedas']['total'])}.", 2)
    par(f"Nas seções com S + M subindo 10 ou mais: dB {fzs(cup['medias']['dB'], 2)}, dM {fzs(cup['medias']['dM'], 2)}, dS {fzs(cup['medias']['dS'], 2)}, comparecimento {fzs(cup['medias']['dcomp'], 2)}, ganho de Lula {fzs(cup['medias']['gL'], 2)}, de Flávio {fzs(cup['medias']['gF'], 2)}. "
        f"Caindo 10 ou mais: dB {fzs(cdn['medias']['dB'], 2)}, dM {fzs(cdn['medias']['dM'], 2)}, comparecimento {fzs(cdn['medias']['dcomp'], 2)}, Lula {fzs(cdn['medias']['gL'], 2)}, Flávio {fzs(cdn['medias']['gF'], 2)}. "
        f"Resto: comparecimento {fzs(cau['S+M']['resto']['medias']['dcomp'], 2)}, Lula {fzs(cau['S+M']['resto']['medias']['gL'], 2)}, Flávio {fzs(cau['S+M']['resto']['medias']['gF'], 2)}. "
        f"Margem (Lula menos Flávio): {fzs(cup['medias']['gL_menos_gF'], 2)} (ep {fz(cup['medias']['ep_gL_menos_gF'], 2)}) na alta, {fzs(cdn['medias']['gL_menos_gF'], 2)} (ep {fz(cdn['medias']['ep_gL_menos_gF'], 2)}) na queda, {fzs(cau['S+M']['resto']['medias']['gL_menos_gF'], 2)} (ep {fz(cau['S+M']['resto']['medias']['ep_gL_menos_gF'], 2)}) no resto.", 2)
    par(f"Exploratório (X2): recentrando na média ({fzs(x2['media_de_d(S+M)'], 2)}), {x2['recentradas_na_media']['subiu_10_ou_mais']} seções sobem 10 ou mais e {x2['recentradas_na_media']['caiu_10_ou_mais']} caem 10 ou mais: a assimetria some. "
        f"Margem acima do que os mesmos eleitores dariam pelo canal B: {fzs(x2m['margem_acima_do_que_daria_o_canal_B']['subiu_10_ou_mais']['media'], 2)} (ep {fz(x2m['margem_acima_do_que_daria_o_canal_B']['subiu_10_ou_mais']['ep'], 2)}) na cauda de alta, contra {fzs(x2m['se_tudo_fosse_voto_lancado_para_Lula_a_margem_ficaria_acima_do_canal_B_em'], 1)} se a alta fosse voto lançado para Lula.", 2)
    w('')
    w('7. A MESMA DECOMPOSIÇÃO POR REGIÃO E POR UF (descritivo; dcomp e dM exatos do bweb, S ancorado, B por diferença)')
    w('     lugar                  n     dcomp exato   (%)       dM exato   dS (ep)             S + M      fração de B (ep)   excesso de M   ganho Lula   ganho Flávio   D_L (ep)')
    def linha_dom(rot, o):
        if 'exato' not in o: return
        e = o['exato']; a_ = o['ancorado']
        dl = f"{fzs(o['regressao_Lula']['contraste'], 2)} ({fz(o['regressao_Lula']['contraste_ep_hc1'], 2)})" if 'regressao_Lula' in o else 'n/d'
        fb = f"{pc(a_['fracao_B'])} ({fz(100 * a_['fracao_B_ep'], 1)})" if a_['fracao_B'] is not None and abs(e['dcomp_sobre_comp1']) >= 0.005 else 'saldo perto de 0'
        w(f"     {rot:<20} {o['n']:>4}  {fs(e['dcomp']):>11}  {fzs(100 * e['dcomp_sobre_comp1'], 2):>6}  {fs(e['dM']):>10}  {fs(a_['dS']):>9} ({fi(a_['ep']):>6})  {fs(a_['dSM']):>9}   {fb:>17}  {fs(e['E_M']):>10}  {fs(e['gL']):>11}  {fs(e['gF']):>11}   {dl}")
    for nome, o in R['por_regiao'].items(): linha_dom(nome, o)
    linha_dom('PI MA TO PB CE', g5a); linha_dom('RS RJ SC SP PR', g5b); linha_dom('demais UFs', R['grupos_de_cinco']['demais_UFs'])
    for u in G_ALTO + G_BAIXO: linha_dom(u, R['por_uf_dos_dois_grupos'][u])
    par(f"Leitura: nas cinco UFs de maior diferença o comparecimento quase não subiu ({fzs(100 * g5a['exato']['dcomp_sobre_comp1'], 2)}%), Lula ganhou {fi(g5a['exato']['gL'])} e Flávio {fi(g5a['exato']['gF'])}; M responde por {fi(g5a['exato']['dM'])} do saldo de {fi(g5a['exato']['dcomp'])} e S ficou parado ({fs(g5a['ancorado']['dS'])}). "
        f"O saldo de S + M ali é {pc(x5['maior_diferenca_PI_MA_TO_PB_CE']['razao'])} da virada de margem das cinco UFs; nas cinco de menor diferença, {pc(x5['menor_diferenca_RS_RJ_SC_SP_PR']['razao'])}. "
        f"Composição do comparecimento do 1º turno nas cinco de maior: B {pc(g5a['composicao_1t']['B'])}, M {pc(g5a['composicao_1t']['M'])}, S {pc(g5a['composicao_1t']['S'])}; nas de menor: B {pc(g5b['composicao_1t']['B'])}, M {pc(g5b['composicao_1t']['M'])}, S {pc(g5b['composicao_1t']['S'])}. "
        "Com n de 25 a 128 por UF, os números de S por UF são grossos; os de comparecimento e de M são exatos. Onde o comparecimento caiu (Norte, MA, TO), a 'fração de B' é a parte de B na queda.", 2)
    w('')
    w('8. TRADUÇÃO EM VOTOS DE MARGEM')
    par(f"(a) Teto pelo saldo: se cada eleitor a mais de S e de M fosse um voto lançado para Lula, {fi(sm['total'])} votos pela letra ({pc(sm['total'] / MARGEM)} da margem; IC de {pc(sm['li95'] / MARGEM)} a {pc(sm['ls95'] / MARGEM)}) e {fi(anc['dSM']['total'])} ancorado ({pc(anc['dSM']['total'] / MARGEM)}; teto de 95% {fi(anc['dSM']['ls95'])}, {pc(anc['dSM']['ls95'] / MARGEM)}). "
        f"Só o Brasil: {fi(xb['dSM'])} ({pc(xb['dSM_sobre_a_margem'])}).", 2)
    par(f"(b) Pela regressão: a margem que acompanha o saldo de S + M além do que acompanharia pelo canal B é {fs(tr['b_pela_regressao']['x_saldo'])} votos (ep {fi(tr['b_pela_regressao']['x_saldo_ep'])}), {pc(tr['b_pela_regressao']['x_saldo_fracao_da_margem'], 2)} da margem; "
        f"sobre a soma das altas, {fs(tr['b_pela_regressao']['x_bruto_das_altas'])} (ep {fi(tr['b_pela_regressao']['x_bruto_ep'])}). Na calibração essa tradução devolve só {pc(pa25['traducao_saldo_devolve'], 0)} da quantia plantada espalhada e {pc(pb25['traducao_saldo_devolve'], 0)} da concentrada (25% da margem): vale como piso grosso, não como medida.", 2)
    par(f"(c) Pelas réguas inocentes (exploratório, Brasil): S + M esperado de {fi(x1['dSM_esperado_no_brasil']['a'])} (proporcional ao comparecimento do 1º turno) a {fi(x1['dSM_esperado_no_brasil']['b'])} (mesma alta em pontos para eleitores com e sem biometria, M proporcional); "
        f"observado {fi(xb['dSM'])}; sobra de {fi(x1['dSM_esperado_no_brasil']['sobra_sobre_b'])} a {fi(x1['dSM_esperado_no_brasil']['sobra_sobre_a'])} (ep {fi(x1['dSM_esperado_no_brasil']['ep_da_sobra'])}), {pc(x1['dSM_esperado_no_brasil']['sobra_sobre_b'] / MARGEM)} a {pc(x1['dSM_esperado_no_brasil']['sobra_sobre_a'] / MARGEM)} da margem. "
        f"Pela régua b, S esperado {fi(x1['dS_esperado_no_brasil']['b_mesma_variacao_em_pontos_dos_eleitores_com_biometria'])} e observado {fi(x1['dS_esperado_no_brasil']['observado_ancorado'])} (ep {fi(x1['dS_esperado_no_brasil']['observado_ancorado_ep'])}): a sobra é toda de M. "
        f"Se a entrada fosse proporcional aos faltosos, S subiria {fi(x1['dS_esperado_no_brasil']['c_proporcional_aos_faltosos_do_1t'])} (os sem biometria são {pc(x1['fracao_sem_biometria_entre_os_faltosos_do_1t_na_amostra'])} dos faltosos).", 2)
    w('')
    w('9. A FAVOR DA TESE (sem suavizar)')
    for i, t in enumerate(favor, 1): par(f'{i}. {t}', 2)
    w('')
    w('10. CONTRA A TESE (sem suavizar)')
    for i, t in enumerate(contra, 1): par(f'{i}. {t}', 2)
    w('')
    w('11. O QUE ISSO SIGNIFICA')
    par(significado, 2)
    w('')
    w('12. PISTAS')
    for i, t in enumerate(pistas, 1): par(f'{i}. {t}', 2)
    w('')
    w('13. DESVIOS E DECISÕES')
    for i, t in enumerate(desvios, 1): par(f'{i}. {t}', 2)
    w('')
    w('14. O QUE FOI FIXADO ANTES E O QUE É EXPLORATÓRIO')
    par("Fixado no Adendo 28 antes de rodar: os dados, o estimador, a regressão, os limiares de SINAL e de SEM SINAL, a leitura dos 90%, as saídas e as caudas. Fixado no docstring antes de qualquer conta com votos: D1 a D17 (exterior, tipo de erro, estimador ancorado, cenários e regra de poder da calibração, rótulos por parte, tradução, conferência). "
        "Exploratório, depois de ver o resultado: X1 a X7 e as frases marcadas como exploratórias. Contagem: um veredito combinado e três partes, nenhum SINAL; no exploratório foram olhadas cerca de doze comparações, das quais nenhuma a mais de 3 ep na direção da tese depois de descontada a régua (o acaso daria 0,03).", 2)
    par("Condições do Adendo 27 para um resultado contar como indício: (i) conferente independente, ainda não feito; (ii) calibração, feita (nível com poder, regressão sem); (iii) espelho, feito (Flávio não mostra o mesmo).", 2)
    w('')
    w('15. ARQUIVOS')
    for a_ in arquivos: w('  ' + a_)
    open(OUT_TXT, 'w').write('\n'.join(L) + '\n')
    log('gravado', OUT_JSON, OUT_TXT)


if __name__ == '__main__':
    cmd = sys.argv[1] if len(sys.argv) > 1 else ''
    if cmd == 'bweb':
        cmd_bweb(sys.argv[2])
    elif cmd == 'bu':
        cmd_bu()
    elif cmd == 'rodar':
        R = rodar()
        escrever(R)
    else:
        print(__doc__)
