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
TRAB = '/home/user/trabalho-eleicao/adendo27/R27_W3'
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
    quer = [e for e in ents if e['nome'].endswith('-rdv.dat') or e['nome'].endswith('-bu.dat')]
    tipos = collections.Counter(e['nome'].rsplit('-', 1)[-1] for e in ents)
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
    els = [n for n in rdv if (n[0], n[1]) == (2, 1)][0][2]
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


def _chave_do_nome(nome):
    # o{pleito:5}{uf:2}{mun:5}{zona:4}{secao:4}-rdv.dat
    base = nome.split('/')[-1]
    corpo = base.split('-')[0]
    uf = corpo[6:8].upper()
    return f'{uf}|{int(corpo[8:13])}|{int(corpo[13:17])}|{int(corpo[17:21])}'


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
            if not n.endswith('-rdv.dat'):
                continue
            k = _chave_do_nome(n)
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
            if not n.endswith('-bu.dat'):
                continue
            k = _chave_do_nome(n)
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


if __name__ == '__main__':
    modo = sys.argv[1] if len(sys.argv) > 1 else ''
    if modo == 'baixar':
        baixar(sys.argv[2], sys.argv[3], sys.argv[4])
    elif modo == 'extrair':
        extrair(sys.argv[2])
    else:
        P(__doc__)
