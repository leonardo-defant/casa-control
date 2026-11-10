"""R27_DA (Adendo 27, onda D-a; mantido pelo Adendo 30): AMOSTRA ALEATÓRIA NOVA DE PONTA A PONTA.

Testes D3-1 (resumo publicado, assinatura da urna, boletim e bweb) e D3-3 (coerência entre boletim, RDV e log da mesma
urna, identidades I1 a I11) de registro/adendo27/desenho_D3_proposta.json, por inteiro, nas 3.000 seções de
registro/adendo27/amostra_aas_principal.txt (amostra aleatória simples das 499.205 seções com boletim no bweb do 2º turno),
mais as listas C1 (27 seções de junta) e P (400 prorrogadas), relatadas à parte e nunca somadas. Do D3-2, a parte que o B5
não fez e que cabe aqui: os aux.json (resumo e estado de cada pacote), na amostra nova e, para a estabilidade, na amostra
antiga baixada em 26/10.

Critérios: a letra do desenho D3 (campos estatistica, criterio_sinal, criterio_sem_sinal, poder, placebo), sem mudar limiar.
Aviso de alcance, do próprio registro: todos os arquivos conferidos aqui saem da mesma urna e do mesmo canal. O teste
enxerga alteração DEPOIS da assinatura da urna (transmissão, recepção, banco da totalização, publicação) e pacote montado
fora da urna. É cego para um programa de urna que conte errado de forma coerente: nesse caso boletim, RDV, log e assinatura
concordam entre si.

DECISÕES QUE O REGISTRO NÃO FIXA, ESCRITAS ANTES DE QUALQUER CONTA COM VOTOS (todas relatadas como desvios)
Antes de escrever esta lista só olhei estrutura: campos do aux.json, árvore BER de um boletim, de um RDV e de um vota.vsc,
modelos de linha do log (500 logs da amostra ANTIGA, sem contar votos), cabeçalho do bweb e a contagem de tipos e estados
dos aux.json das pastas. Na inspeção da árvore de um RDV apareceram na tela os seis primeiros votos de presidente de uma
seção (PA|5355|83|374); não usei isso para nada.

 1. Conjuntos. p2: amostra principal, 2º turno (aas/t2: aux.json, bu, rdv, log, vota.vsc). p1: as mesmas seções no 1º turno
    (aas/t1: aux.json, bu, rdv, vota.vsc; o log do 1º turno não foi baixado, como manda o desenho). pp: lista P (aas/c1p_t2).
    c1: lista C1. As 27 seções de junta publicam busa.dat, sa.vsc e logsa.jez no lugar de bu.dat, vota.vsc e log.jez, e o
    download da onda só pediu bu, rdv, log e vota; por isso este script baixa esses três tipos das 27 seções (pasta nova
    R27_DA/dl_c1, 1 requisição por segundo, parando em qualquer 429). ant: amostra antiga de 3.903 pastas
    (amostra2t/arq), só como réplica, nunca como estimativa nacional. e2 e e1: o prefixo já baixado da extensão (só boletim
    e RDV), ao lado, sem peso no veredito.
 2. Pacote da seção: todos os itens de "hashes" do aux.json. Havendo mais de um, todos são lidos e (f) compara os votos
    entre eles. As demais conferências usam o pacote com estado "Totalizado" (se for um só) ou, na falta, o último listado.
 3. Dois caminhos de leitura do boletim: (A) scripts/decodificar.py (ler_bu, bu_para_secao), que procura os campos por
    forma; (B) leitor próprio deste script, por posição, seguindo a especificação ASN.1 do TSE (bu.asn1 e rdv.asn1 do
    pacote formato-arquivos-bu-rdv-ass-digital-v2). Uma quebra só conta se aparecer nos dois. Diferença entre A e B sem
    diferença contra o bweb é problema de leitor e vai relatada à parte.
 4. (a) bweb contra bu.dat, cargo 1: votos por número do votável (no bweb, NR_VOTAVEL; 95 branco e 96 nulo; no boletim,
    número do candidato, tipo 2 = branco, tipo 3 = nulo). Qualquer diferença em qualquer votável é quebra de classe A.
    Diferença no comparecimento também entra como classe A (o pior caso do desenho é medido em comparecimento; é leitura
    mais dura que a letra). Diferença só em aptos entra como classe B. Governador (cargo 3) é conferido ao lado, sem peso.
 5. (b) SHA-512 e tamanho de cada arquivo baixado (bu, rdv, log) contra a entrada do bloco de hardware do vota.vsc.
    Classe A para o bu.dat, classe B para rdv e log, como no desenho. Ao lado: bloco de software igual ao de hardware
    (tamanho e resumo de cada arquivo) e resumo de cada bloco igual ao do cabeçalho.
 6. (c) Assinatura de hardware, com a chave pública do certificado embutido no vota.vsc: (i) de cada um dos arquivos
    listados no bloco de hardware, contra o resumo listado; (ii) do bloco inteiro. UE2013 e UE2015: ECDSA P-521 (biblioteca
    cryptography); UE2020 e UE2022: Ed521 (scripts/ed521.py). É a verificação de scripts/verificar_assinaturas.py (T18),
    reusada. Para um arquivo baixado cujo SHA-512 difere do listado, a assinatura é verificada contra o resumo do arquivo
    do disco (é assim que um byte trocado no boletim aparece em (b) e em (c)). Quebra de (c): assinatura inválida de bu,
    rdv, log ou do bloco. Assinatura inválida de outro arquivo listado (não baixável) é relatada à parte como (c2).
    NÃO verificado, e dito no relatório: a assinatura de software (bloco 0, formato próprio de 4.765 bytes, chave SEVIN
    que não é pública): só o resumo é comparado.
 7. (d) Certificado. (d1) emitido por uma das AC publicadas: identificador da AC (AKI) igual ao SKI de AC URNA, AC UE2020
    ou AC UE2022, emissor igual ao titular da AC e assinatura do certificado válida com a chave da AC (ECDSA P-521 com
    SHA-512 ou Ed521), como no F12; fonte das AC: a mesma do F12 (pacote de documentação do TSE, cópia de terceiros, igual
    em 4 fontes). (d2) nome do certificado = UEAO + número da urna do boletim, do bweb e (no 2º turno) do log. (d3) a
    mesma chave pública em duas seções do mesmo turno, ou chaves diferentes para a mesma urna entre os turnos.
    NÃO verificado: a cadeia das AC até a raiz (AC RAIZ UE e AC URNA v2 não estão publicadas onde este ambiente alcança)
    e a lista de revogados (os endereços do certificado só servem HTTP simples; faço uma tentativa por endereço e relato).
    A validade das datas fica descritiva (o F12 já mostrou que o certificado publicado da AC URNA venceu em 18/07/2026);
    o registro não a põe no critério.
 8. (e) SHA-256 do vota.vsc (base64, com "/" trocado por "-", como o site grava) contra o campo hash do aux.json.
 9. (g), classe B: município, zona e seção de dentro do boletim (envelope e conteúdo) contra a chave; data e hora de
    recebimento do pacote no aux.json (dr, hr) contra DT_BU_RECEBIDO (igualdade exata); código de carga (só dígitos),
    número da urna, abertura, encerramento e emissão do boletim contra o bweb (igualdade exata). Ao lado, sem entrar na
    contagem de (g) porque o desenho não lista: mídia de carga, data da carga e local de votação contra o bweb; pleito e
    fase do cabeçalho; aptos.
10. Seção "sem arquivo" = sem aux.json no site ou sem boletim listado e baixado. "Assinatura que não se consegue
    verificar" = sem vota.vsc (ou sa.vsc), arquivo ilegível ou algoritmo desconhecido.
11. Reconferência: o desenho pede baixar de novo "em outro dia" antes de contar uma quebra de classe A. Os arquivos foram
    baixados em 10/11; se houver quebra, baixo de novo no mesmo dia (pasta nova R27_DA/rebaixar) e digo que a confirmação
    em outro dia fica para o conferente.
12. Alcance (como no desenho): limite superior de 95% de Clopper e Pearson; K = teto(N x limite); dano máximo = 2 x soma
    do comparecimento das K maiores seções do 2º turno (dados/secoes2026.json.gz). Com m seções sem arquivo, soma-se o
    limite superior de m/n. As 8 UFs de publicação em lote (AC, AM, DF, ES, MT, PR, RN, TO) vão em separado.
13. D3-3, dia do turno: 25/10/2026 (04/10/2026 no 1º). Linhas de todos os logd.dat do pacote, inclusive o .jez aninhado da
    urna substituída. "Bloco final" = o logd.dat que tem a última linha "Gerando arquivo de resultado [bu.dat]" do dia do
    turno (na falta, o último com linha no dia).
    I1: contagem do RDV para presidente (nominal por número digitado; branco = tipos 3 e 5; nulo = tipos 4, 6, 7, 8 e 9)
        contra o boletim. Governador ao lado.
    I2: linhas "O voto do eleitor foi computado" no dia do turno (todos os blocos) contra o comparecimento do boletim e
        contra o do bweb.
    I3: "Voto confirmado para [Presidente]" mais "Atribuido voto nulo por suspensão [Presidente]" no dia do turno contra o
        total de votos do cargo no boletim. Governador ao lado.
    I4: número da urna nas linhas do dia do turno do bloco final (a da linha que gera o bu.dat) contra o boletim, o bweb
        e o nome do certificado.
    I5: última linha "Código de carga ... gravado", última "Identificador da mídia de carga" e última "Data e hora que foi
        digitada pelo operador" do bloco final contra o boletim (igualdade exata; nos 300 logs da amostra antiga que olhei
        para definir isto as três batem em 300) e contra o bweb.
    I6: linhas "Município:", "Zona Eleitoral:" e "Seção Eleitoral:" do bloco final no dia do turno contra a chave (se não
        houver nenhuma no dia, as últimas anteriores).
    I7: (i) primeira "Urna pronta para receber votos" do dia (qualquer bloco) contra a abertura do boletim, 1 segundo;
        (ii) última "Procedimento de encerramento confirmado" do dia contra o encerramento, 1 segundo; (iii) emissão do
        boletim entre a última "Inicio do Encerramento" e a "Gerando arquivo de resultado [bu.dat]" seguinte, 5 segundos;
        (iv) carimbo do vota.vsc. O log publicado termina em "Gerando arquivo de resultado [log.jez]", ANTES da assinatura,
        então o intervalo de assinatura do 2º turno não está no log do 2º turno. Leitura fixada: é violação o carimbo do
        vota.vsc anterior à última linha do log menos 5 segundos. O limite de cima fica com I8 (recebimento). Ao lado: a
        distância entre a última linha do log e o carimbo, e, quando a urna é a mesma, o carimbo do vota.vsc do 1º turno
        contra o intervalo "Início/Término do procedimento de assinatura" de 04/10 que o log do 2º turno traz (5 s).
    I8: (i) voto computado antes da primeira "Urna pronta" do dia no mesmo bloco, ou depois da última "Procedimento de
        encerramento confirmado" do bloco; (ii) recebimento (Brasília) anterior ao carimbo do vota.vsc convertido para
        Brasília, com 2 minutos de tolerância. Fuso do município = 8 menos a hora modal de abertura das seções dele no
        bweb (como no desenho). No exterior a abertura é sempre 8h locais e o fuso não sai dos arquivos: (ii) não se
        aplica e isso é contado.
    I9: votos computados em 04/10 no log do pacote do 2º turno contra o comparecimento do 1º turno no bweb, quando a
        urna do bweb é a mesma nos dois turnos.
    I10: carimbo de hora menor que o da linha anterior, no mesmo logd.dat, sem que a própria linha ou alguma das 12
        anteriores seja de ajuste ("Data e hora solicitadas", "Data e hora que foi digitada pelo operador" ou "Data e
        hora atualizada"; as linhas "Data e hora da geração da mídia ..." NÃO contam como ajuste). Na amostra antiga
        todos os passos para trás que vi (279 em 500 logs) são a linha "Data e hora atualizada" da carga.
    I11: votos de presidente na ordem do arquivo, 13 ou não 13; número de sequências R contra a permutação aleatória
        (E = 1 + 2ab/n; V = 2ab(2ab - n)/(n²(n - 1)), a e b as contagens); z por seção; Z = soma dos z sobre a raiz do
        número de seções com V > 0; fração com |z| > 3. O mesmo no 1º turno. "Igual nos dois turnos" (critério de sem
        sinal) = mesmo sinal e |Z2 - Z1|/raiz(2) < 3. Espelho: a mesma conta com 22 ou não 22.
    Evento do log que explica (lista fixada antes): pacote com mais de um logd.dat; linha de contingência ("Contingência",
    "Urna de contingência"); tipo de urna do boletim diferente de 1 (seção); tipo de arquivo diferente de 1 (recuperador
    de dados ou sistema de apuração); boletim de junta. "Votação suspensa" e ajuste de data e hora no dia do turno são
    contados e citados, mas não explicam diferença de contagem.
    Critério de sem sinal, parte dos horários: "menos de 0,5% com violação de horário sem explicação" é lido como I7, I8
    e I10 juntos (mais duro que o critério de sinal, que cita só I7 e I8).
14. Calibração por efeito plantado (campo poder do desenho), com sementes fixas (20261110 + número do plantio):
    P1: em cópia das linhas do bweb, mover 5 votos do 22 para o 13 em 30 seções sorteadas da amostra (com 5 ou mais votos
        do 22): (a) tem de apontar as 30 e só elas.
    P2: trocar 1 byte (posição sorteada) em cópia do bu.dat de 10 seções: (b) e (c) têm de apontar as 10.
    P3: trocar o vota.vsc entre 5 pares de seções (10 seções): (d) e (e) têm de apontar as 10.
    P4: 10.000 sorteios de 5.857 seções alteradas ao acaso, e o conjunto das 5.857 maiores: em quantos a amostra fixa
        contém pelo menos uma.
    P5 a P8 (D3-3), em cópias dos dados decodificados, 30 seções sorteadas cada: mover 3 votos entre 22 e 13 só no boletim
        (I1); somar 5 ao comparecimento e aos votos do 13 no boletim (I2 e I3); atrasar o encerramento do boletim em 10
        minutos (I7); ordenar os votos do RDV por candidato (I11).
    Explicação inocente plantada: (E1) reembaralhar ao acaso o RDV de 30 seções (I11 não pode acusar); (E2) deslocar em
        +1 hora todos os horários da urna (boletim, log e vota.vsc) em 30 seções, como relógio digitado errado na carga:
        I7 não pode acusar; o que I8 (ii) faz é relatado; (E3) arquivo corrompido no download: é o P2, que some ao reler
        o arquivo original.
    Se o plantado não for apontado, o veredito da parte é SEM PODER.
15. Espelho. Conferências exatas não têm sentido por candidato; o espelho delas é o 1º turno das mesmas seções (onde
    Flávio ficou à frente) e o sinal de cada diferença achada (a favor do 13 ou do 22). I11 tem espelho próprio (22).
16. D3-2, parte dos aux.json. Na amostra nova: estado da seção e do pacote, data de geração do índice, número de pacotes,
    tipos listados. Estabilidade: baixo hoje o aux.json das seções da amostra antiga (3.903 do 2º turno e as 80 do 1º,
    pasta nova R27_DA/aux_hoje, 1 requisição por segundo, parando em qualquer 429) e comparo hash, data e hora de
    recebimento e estado com os de 26/10. Onde o hash mudou, baixo o pacote novo e comparo os votos. Pela letra do D3-2:
    sinal se um pacote teve os votos mudados depois de 26/10; sem sinal (só desta parte) se nenhum resumo mudou.
    As seções da amostra nova que também estão na amostra antiga são comparadas arquivo a arquivo.
17. Tradução em votos de margem: com X = 0, o teto do pior caso absoluto (K seções maiores com todos os votos invertidos),
    em votos e em fração de 4.430.191. Com X > 0, N x média amostral de [(13 - 22) do bweb menos (13 - 22) do boletim],
    com erro-padrão de amostra aleatória simples e correção de população finita.

O QUE É EXPLORATÓRIO: tudo o que aparecer no relatório sob o título EXPLORATÓRIO foi decidido depois de ver resultado.

Modos: baixar_c1, baixar_aux, ler <conjunto>, calibrar, rodar, rebaixar <chave> <turno>.
Uso: python3 -I scripts/analisar_R27_DA.py <modo> [...]
"""
import os as _os, sys as _sys
_sys.path.insert(0, _os.path.dirname(_os.path.abspath(__file__)))
import base64, collections, copy, datetime as dt, glob, gzip, hashlib, io, json, math, os, random, re, shutil, ssl, sys, time, zipfile
import urllib.error, urllib.request

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
REG = os.path.join(REPO, 'registro', 'adendo27')
W = '/home/user/trabalho-eleicao/adendo27/R27_DA'
AAS = '/home/user/trabalho-eleicao/adendo27/aas'
ANTIGA = '/home/user/trabalho-eleicao/amostra2t/arq'
ANTIGA1 = '/home/user/trabalho-eleicao/amostra2t/arq1t'
ZIP_AC = '/home/user/trabalho-eleicao/adendo21/F12_dl_doccaz/docv2/formato-arquivos-bu-rdv-ass-digital-v2.zip'
SAIDA_JSON = os.path.join(REPO, 'resultados', 'R27_DA_amostra_ponta_a_ponta.json')
SAIDA_TXT = os.path.join(REPO, 'resultados', 'R27_DA_amostra_ponta_a_ponta.txt')
BASE = 'https://resultados.tse.jus.br/oficial/ele2026/arquivo-urna'
PLEITO = {1: 3220, 2: 3221}
DIA = {1: '04/10/2026', 2: '25/10/2026'}
N_U = 499205
MARGEM = 4430191
UFS8 = ('AC', 'AM', 'DF', 'ES', 'MT', 'PR', 'RN', 'TO')
SEMENTE = 20261110

CONJ = {
    'p2': {'pasta': f'{AAS}/t2', 'lista': 'amostra_aas_principal.txt', 'turno': 2},
    'p1': {'pasta': f'{AAS}/t1', 'lista': 'amostra_aas_principal.txt', 'turno': 1},
    'pp': {'pasta': f'{AAS}/c1p_t2', 'lista': 'estrato_P_prorrogadas_400.txt', 'turno': 2},
    'c1': {'pasta': f'{W}/dl_c1', 'lista': 'estrato_C1_junta.txt', 'turno': 2},
    'ant': {'pasta': ANTIGA, 'lista': None, 'turno': 2},
    'e2': {'pasta': f'{AAS}/ext_t2', 'lista': 'amostra_aas_extensao.txt', 'turno': 2},
    'e1': {'pasta': f'{AAS}/ext_t1', 'lista': 'amostra_aas_extensao.txt', 'turno': 1},
}


def diz(*a):
    print(time.strftime('%H:%M:%S'), *a, flush=True)


def grava(nome, obj, gz=False):
    os.makedirs(W, exist_ok=True)
    cam = os.path.join(W, nome)
    if gz:
        with gzip.open(cam + '.part', 'wt') as f:
            json.dump(obj, f, separators=(',', ':'), ensure_ascii=False, default=str)
    else:
        with open(cam + '.part', 'w') as f:
            json.dump(obj, f, indent=1, ensure_ascii=False, default=str)
    os.replace(cam + '.part', cam)


def le(nome):
    cam = os.path.join(W, nome)
    if not os.path.exists(cam):
        return None
    if cam.endswith('.gz'):
        with gzip.open(cam, 'rt') as f:
            return json.load(f)
    return json.load(open(cam))


def lista(conj):
    c = CONJ[conj]
    if c['lista']:
        return [l.strip() for l in open(os.path.join(REG, c['lista'])) if l.strip()]
    out = []
    for d in sorted(glob.glob(os.path.join(c['pasta'], '*/*/*/*/'))):
        uf, m, z, s = d.rstrip('/').split('/')[-4:]
        out.append(f'{uf.upper()}|{int(m)}|{int(z)}|{int(s)}')
    return out


def pasta_secao(base, k):
    uf, m, z, s = k.split('|')
    return os.path.join(base, uf.lower(), f'{int(m):05d}', f'{int(z):04d}', f'{int(s):04d}')


# =====================================================================================================================
# Download (1 requisição por segundo, uma conexão, para em qualquer 429)
# =====================================================================================================================
_CTX = None
_ult = [0.0]


class Parar(Exception):
    pass


def pega(url):
    """Uma requisição. None para 404. Levanta Parar em 429 ou em página de bloqueio."""
    global _CTX
    if _CTX is None:
        _CTX = ssl.create_default_context(cafile=os.environ.get('SSL_CERT_FILE', '/root/.ccr/ca-bundle.crt'))
    for tent in range(4):
        esp = _ult[0] + 1.0 - time.time()
        if esp > 0:
            time.sleep(esp)
        _ult[0] = time.time()
        try:
            req = urllib.request.Request(url, headers={'User-Agent': 'auditoria-eleicao-2026 (pesquisa)'})
            with urllib.request.urlopen(req, timeout=60, context=_CTX) as r:
                b = r.read()
            if b[:200].lower().lstrip().startswith((b'<!doctype html', b'<html')):
                raise Parar('pagina de bloqueio em ' + url)
            return b
        except urllib.error.HTTPError as e:
            if e.code == 404:
                return None
            if e.code == 429:
                raise Parar('429 em ' + url)
            time.sleep(5 * (tent + 1))
        except Parar:
            raise
        except Exception:  # noqa: BLE001
            time.sleep(5 * (tent + 1))
    return b''  # falhou sem 404 nem 429: tratado como ausente por falha de rede, e contado


def url_aux(turno, k):
    uf, m, z, s = k.split('|')
    uf = uf.lower(); m5 = f'{int(m):05d}'; z4 = f'{int(z):04d}'; s4 = f'{int(s):04d}'
    b = f'{BASE}/{PLEITO[turno]}/dados/{uf}/{m5}/{z4}/{s4}'
    return b, f'{b}/p00{PLEITO[turno]}-{uf}-m{m5}-z{z4}-s{s4}-aux.json'


def baixar_secao(turno, k, saida, tipos, log):
    d = pasta_secao(saida, k); os.makedirs(d, exist_ok=True)
    base, ua = url_aux(turno, k)
    pa = os.path.join(d, 'aux.json')
    if not os.path.exists(pa):
        b = pega(ua); log['req'] += 1
        if b is None:
            open(os.path.join(d, 'SEM_AUX'), 'w').close(); log['sem_aux'] += 1; return
        if b == b'':
            log['falha'] += 1; return
        open(pa, 'wb').write(b)
    if not tipos:
        return
    aux = json.loads(open(pa, 'rb').read().decode('utf-8'))
    for i, h in enumerate(aux.get('hashes', [])):
        for a in h.get('arq', []):
            if a.get('tp') not in tipos:
                continue
            dest = os.path.join(d, f"{i}-{a['nm']}")
            if os.path.exists(dest):
                continue
            b = pega(f"{base}/{h['hash']}/{a['nm']}"); log['req'] += 1
            if b:
                open(dest + '.part', 'wb').write(b); os.replace(dest + '.part', dest); log['bytes'] += len(b)
            else:
                log['falha' if b == b'' else 'ausente'] += 1


def modo_baixar_c1():
    """As 27 seções de junta: busa.dat, sa.vsc, logsa.jez e rdv.dat (pasta nova)."""
    saida = CONJ['c1']['pasta']; log = collections.Counter(); t0 = time.time()
    try:
        for k in lista('c1'):
            baixar_secao(2, k, saida, {'busa', 'sa', 'logsa', 'rdv', 'bu', 'vota', 'log'}, log)
    except Parar as e:
        log['PAROU'] = str(e)
    log['segundos'] = round(time.time() - t0)
    grava('download_c1.json', dict(log)); diz('c1', dict(log))


def modo_baixar_aux():
    """aux.json de hoje das seções da amostra antiga (2º turno) e das 80 do 1º turno. Só o índice, sem arquivos."""
    log = collections.Counter(); t0 = time.time()
    tarefas = [(2, k, f'{W}/aux_hoje/2t') for k in lista('ant')]
    for d in sorted(glob.glob(os.path.join(ANTIGA1, '*/*/*/*/'))):
        uf, m, z, s = d.rstrip('/').split('/')[-4:]
        tarefas.append((1, f'{uf.upper()}|{int(m)}|{int(z)}|{int(s)}', f'{W}/aux_hoje/1t'))
    # ordem embaralhada com semente fixa: se parar no meio, o que foi baixado é amostra ao acaso da lista
    random.Random(SEMENTE).shuffle(tarefas)
    try:
        for i, (turno, k, saida) in enumerate(tarefas):
            baixar_secao(turno, k, saida, set(), log)
            if i % 200 == 0:
                grava('download_aux_hoje.json', dict(log, feitas=i + 1, total=len(tarefas), segundos=round(time.time() - t0)))
    except Parar as e:
        log['PAROU'] = str(e)
    grava('download_aux_hoje.json', dict(log, total=len(tarefas), segundos=round(time.time() - t0), fim=time.strftime('%Y-%m-%d %H:%M:%S UTC', time.gmtime())))
    diz('aux_hoje', dict(log))


# =====================================================================================================================
# Leitores (nenhuma conta aqui: só extraem fatos dos arquivos)
# =====================================================================================================================
import calendar
from ber import parse, read_tlv
from decodificar import ler_bu as ler_bu_A, bu_para_secao, ler_rdv as ler_rdv_A, rdv_para_bu, _linhas_log

RX_TS = re.compile(r'^(\d\d)/(\d\d)/(\d{4}) (\d\d):(\d\d):(\d\d)$')
RX_JE = re.compile(r'^(\d{4})(\d\d)(\d\d)T(\d\d)(\d\d)(\d\d)$')
RX_BW = re.compile(r'^(\d{4})-(\d\d)-(\d\d) (\d\d):(\d\d):(\d\d)$')
RX_CONF = re.compile(r'^Voto confirmado para \[([^\]]+)\]')
RX_NSUSP = re.compile(r'^Atribuido voto nulo por suspensão \[([^\]]+)\]')


def t_log(s):
    m = RX_TS.match(s)
    if not m:
        return None
    d, mo, y, h, mi, se = map(int, m.groups())
    try:
        return calendar.timegm((y, mo, d, h, mi, se))
    except Exception:  # noqa: BLE001
        return None


def t_je(s):
    """'YYYYMMDDThhmmss' (formato da Justiça Eleitoral) -> segundos."""
    m = RX_JE.match(s or '')
    return calendar.timegm(tuple(map(int, m.groups()))) if m else None


def t_bw(s):
    """'YYYY-MM-DD hh:mm:ss' (bweb) -> segundos."""
    m = RX_BW.match(s or '')
    return calendar.timegm(tuple(map(int, m.groups()))) if m else None


def t_aux(dr, hr):
    try:
        d, mo, y = map(int, dr.split('/')); h, mi, se = map(int, hr.split(':'))
        return calendar.timegm((y, mo, d, h, mi, se))
    except Exception:  # noqa: BLE001
        return None


def hms(t):
    return time.strftime('%d/%m %H:%M:%S', time.gmtime(t)) if t is not None else None


def _i(v):
    return int.from_bytes(v, 'big')


def _s(v):
    return v.decode('latin1')


def _ident_secao(no):
    f = no[2]; mz = f[0][2]
    return {'mun': _i(mz[0][2]), 'zona': _i(mz[1][2]), 'loc': _i(f[1][2]), 'secao': _i(f[2][2])}


def _ident(no):
    """IdentificacaoUrna: [0] seção, [1] contingência."""
    if no[1] == 0:
        return dict(_ident_secao(no), tipo=0)
    mz = no[2][0][2]
    return {'mun': _i(mz[0][2]), 'zona': _i(mz[1][2]), 'tipo': 1}


def _urna(no):
    u = no[2]
    o = {'tipo_urna': _i(u[0][2]), 'versao': _s(u[1][2])}
    corr = u[2][2]
    o['corr'] = _ident(corr[0])
    cg = corr[1][2]
    o.update({'urna': _i(cg[0][2]), 'fc': cg[1][2].hex().upper(), 'ger': [_s(x[2]) for x in cg[2][2]],
              'dt_carga': _s(cg[3][2]), 'cod_carga': _s(cg[4][2])})
    o['tipo_arq'] = _i(u[3][2]); o['fv'] = u[4][2].hex().upper(); o['motivo_sa'] = len(u) > 5
    return o


def ler_bu_B(bruto):
    """Caminho B: leitura por posição, pela especificação bu.asn1 do TSE (EntidadeEnvelopeGenerico > EntidadeBoletimUrna)."""
    env = parse(bruto)[0][2]
    o = {}
    cab = env[0][2]
    o['env_data'] = _s(cab[0][2]); o['env_idtipo'] = cab[1][1]; o['env_id'] = _i(cab[1][2])
    o['env_fase'] = _i(env[1][2])
    i = 2
    if (env[i][0], env[i][1]) == (0, 16):  # urna, opcional no envelope
        i += 1
    o['env'] = _ident(env[i]); o['env_tipo'] = _i(env[i + 1][2])
    resto = env[i + 2:]
    o['cifrado'] = any((n[0], n[1]) == (0, 16) for n in resto)
    conteudo = [n for n in resto if (n[0], n[1]) == (0, 4)][-1][2]
    bu = parse(conteudo)[0][2]
    cab = bu[0][2]
    o['data'] = _s(cab[0][2]); o['idtipo'] = cab[1][1]; o['id'] = _i(cab[1][2])
    o['fase'] = _i(bu[1][2])
    o.update(_urna(bu[2]))
    o['sec'] = _ident_secao(bu[3])
    o['emissao'] = _s(bu[4][2])
    ds = bu[5]
    if ds[1] == 0:
        o['ab'] = _s(ds[2][0][2]); o['enc'] = _s(ds[2][1][2]); o['sa'] = None
    else:
        f = ds[2]
        o['ab'] = o['enc'] = None
        o['sa'] = {'junta': _i(f[0][2]), 'turma': _i(f[1][2]), 'urna_origem': _i(f[2][2]) if len(f) > 2 else None}
    o['comp'] = _i(bu[6][2])
    j = 7; o['det'] = None
    if (bu[j][0], bu[j][1]) == (2, 1):
        o['det'] = [_i(x[2]) for x in bu[j][2]]; j += 1
    o['eleicoes'] = {}
    for el in bu[j][2]:
        f = el[2]
        rec = {'apt': _i(f[1][2]), 'apt_secao': _i(f[2][2]), 'apt_tte': _i(f[3][2]), 'cargos': {}}
        for rv in f[4][2]:
            g = rv[2]; tipo_cargo = _i(g[0][2]); comp = _i(g[1][2])
            for tc in g[2][2]:
                h = tc[2]; cc = h[0]
                cargo = ('c' if cc[1] == 1 else 'l') + str(_i(cc[2]))
                votos = {}
                for vv in h[2][2]:
                    e = vv[2]
                    tipo = _i(e[0][2]); q = _i(e[1][2]); cand = ''
                    if len(e) > 2 and (e[2][0], e[2][1]) == (2, 3):
                        cand = str(_i(e[2][2][1][2]))
                    ch = f'{tipo}:{cand}'
                    votos[ch] = votos.get(ch, 0) + q
                rec['cargos'][cargo] = {'tipo': tipo_cargo, 'comp': comp, 'votos': votos}
        o['eleicoes'][str(_i(f[0][2]))] = rec
    o['hist'] = [_s(x[2]) for x in bu[j + 1][2]] if len(bu) > j + 1 and isinstance(bu[j + 1][2], list) else []
    return o


def ler_rdv_B(bruto):
    """RDV por posição, pela especificação rdv.asn1. Guarda a ORDEM dos votos de presidente e de governador."""
    top = parse(bruto)[0][2]
    o = {}
    cab = top[0][2]
    o['data'] = _s(cab[0][2]); o['id'] = _i(cab[1][2])
    o.update(_urna(top[1]))
    r = top[2][2]
    o['pleito'] = _i(r[0][2]); o['fase'] = _i(r[1][2]); o['sec'] = _ident_secao(r[2])
    o['hist'] = [_s(x[2]) for x in r[3][2]]
    el = r[4]; o['tipo_eleicoes'] = el[1]
    o['cargos'] = {}
    for e in el[2]:
        f = e[2]; ide = _i(f[0][2])
        for cargo in f[-1][2]:
            h = cargo[2]; cc = h[0]
            ck = f"{ide}|{'c' if cc[1] == 1 else 'l'}{_i(cc[2])}"
            reg = o['cargos'].setdefault(ck, {'n': 0, 'cont': {}, 'seq': []})
            guarda = cc[1] == 1 and _i(cc[2]) in (1, 3)
            for voto in h[2][2]:
                ev = voto[2]; tipo = _i(ev[0][2]); dig = _s(ev[1][2]) if len(ev) > 1 else ''
                reg['n'] += 1
                if guarda:
                    ch = f'{tipo}:{dig}'
                    reg['cont'][ch] = reg['cont'].get(ch, 0) + 1
                    reg['seq'].append(dig if tipo == 2 else ('B' if tipo in (3, 5) else 'N'))
            if not guarda:
                reg.pop('seq', None); reg.pop('cont', None)
    for ck, reg in o['cargos'].items():
        if 'seq' in reg:
            reg['seq'] = ','.join(reg['seq'])
    return o


EVENTOS = (('contingencia', ('ontingência',)), ('recuperador', ('ecuperador de dados', 'ecuperador de Dados')), ('suspensa', ('Votação suspensa',)),
           ('sincronismo', ('Sincronismo de mídia',)))
AJUSTE = ('Data e hora solicitadas', 'Data e hora que foi digitada pelo operador', 'Data e hora atualizada')


def _dia_novo():
    return {'comp': 0, 'conf': {}, 'nsusp': {}, 'pronta': [], 'encconf': [], 'inienc': [], 'gerabu': [], 'geralog': [],
            'assini': [], 'assfim': [], 'vt': [], 'ids': {}, 'mun': [], 'zona': [], 'secao': [], 'ult_t': None, 'ult_msg': None,
            'ajuste': 0, 'suspensa': 0, 'erros': 0, 'hab': 0, 'cancel_enc': 0}


def ler_log_B(caminho):
    """Fatos do log, por bloco (logd.dat do pacote e os aninhados) e, dentro do bloco, por dia de votação."""
    blocos = _linhas_log(caminho)
    out = []
    dias = set(DIA.values())
    for linhas in blocos:
        B = {'n': len(linhas), 'ids': {}, 'cod': [], 'fc': [], 'dig': [], 'retro': [], 'n_retro': 0, 'n_retro_aj': 0, 'curtas': 0,
             'ts_ruim': 0, 'dias': {}, 'ult': {'mun': None, 'zona': None, 'secao': None}, 'ev': {}, 'prim_t': None, 'ult_t': None,
             'apps': {}}
        prev = None; jan = collections.deque(maxlen=12)
        for li, l in enumerate(linhas):
            p = l.split('\t')
            if len(p) < 5:
                B['curtas'] += 1; continue
            t = t_log(p[0])
            if t is None:
                B['ts_ruim'] += 1; continue
            uid, app, msg = p[2], p[3], p[4]
            B['ids'][uid] = B['ids'].get(uid, 0) + 1
            B['apps'][app] = B['apps'].get(app, 0) + 1
            if B['prim_t'] is None:
                B['prim_t'] = t
            B['ult_t'] = t
            if prev is not None and t < prev:
                B['n_retro'] += 1
                if msg.startswith(AJUSTE) or any(m.startswith(AJUSTE) for m in jan):
                    B['n_retro_aj'] += 1
                elif len(B['retro']) < 20:
                    B['retro'].append([li, prev, t, app, msg[:80]])
            prev = t; jan.append(msg)
            if msg.startswith('Código de carga'):
                B['cod'].append(re.sub(r'\D', '', msg.split(' gravado')[0]))
            elif msg.startswith('Identificador da mídia de carga:'):
                B['fc'].append(msg.split(':', 1)[1].strip().upper())
            elif msg.startswith('Data e hora que foi digitada pelo operador:'):
                try:
                    a, b = msg.split(':', 1)[1].strip().split(' - ')
                    d_, m_, y_ = a.split('/')
                    B['dig'].append(y_ + m_ + d_ + 'T' + b.replace(':', ''))
                except Exception:  # noqa: BLE001
                    B['dig'].append('?' + msg[-30:])
            for nome, pads in EVENTOS:
                if any(x in msg for x in pads):
                    B['ev'][nome] = B['ev'].get(nome, 0) + 1
            campo = 'mun' if msg.startswith('Município:') else 'zona' if msg.startswith('Zona Eleitoral:') else 'secao' if msg.startswith('Seção Eleitoral:') else None
            if campo:
                val = msg.split(':', 1)[1].strip()
                B['ult'][campo] = val
            dia = p[0][:10]
            if dia not in dias:
                continue
            D = B['dias'].get(dia)
            if D is None:
                D = B['dias'][dia] = _dia_novo()
            D['ids'][uid] = D['ids'].get(uid, 0) + 1
            D['ult_t'] = t; D['ult_msg'] = msg[:70]
            if campo:
                if val not in D[campo]:
                    D[campo].append(val)
            if p[1] == 'ERRO':
                D['erros'] += 1
            if msg == 'O voto do eleitor foi computado':
                D['comp'] += 1; D['vt'].append(t)
            elif msg.startswith('Voto confirmado para ['):
                c = RX_CONF.match(msg).group(1); D['conf'][c] = D['conf'].get(c, 0) + 1
            elif msg.startswith('Atribuido voto nulo por suspensão ['):
                c = RX_NSUSP.match(msg).group(1); D['nsusp'][c] = D['nsusp'].get(c, 0) + 1
            elif msg == 'Eleitor foi habilitado':
                D['hab'] += 1
            elif msg == 'Urna pronta para receber votos':
                D['pronta'].append(t)
            elif msg == 'Procedimento de encerramento confirmado':
                D['encconf'].append(t)
            elif msg in ('Inicio do Encerramento', 'Início do Encerramento'):
                D['inienc'].append(t)
            elif msg.startswith('Gerando arquivo de resultado [bu.dat]'):
                D['gerabu'].append([t, uid])
            elif msg.startswith('Gerando arquivo de resultado [log.jez]'):
                D['geralog'].append(t)
            elif msg.startswith('Início do procedimento de assinatura dos arquivos de resultados'):
                D['assini'].append(t)
            elif msg.startswith('Término do procedimento de assinatura dos arquivos de resultados'):
                D['assfim'].append(t)
            elif msg.startswith(AJUSTE):
                D['ajuste'] += 1
            elif msg == 'Votação suspensa':
                D['suspensa'] += 1
            elif msg in ('Operador cancelou o encerramento da votação', 'Procedimento de encerramento abortado'):
                D['cancel_enc'] += 1
        for D in B['dias'].values():
            vt = D.pop('vt')
            D['v_prim'] = vt[0] if vt else None; D['v_ult'] = vt[-1] if vt else None
            D['v_min'] = min(vt) if vt else None; D['v_max'] = max(vt) if vt else None
            p0 = min(D['pronta']) if D['pronta'] else None
            e1 = max(D['encconf']) if D['encconf'] else None
            D['v_antes'] = sum(1 for x in vt if p0 is not None and x < p0)
            D['v_sem_pronta'] = len(vt) if (vt and p0 is None) else 0
            D['v_depois'] = sum(1 for x in vt if e1 is not None and x > e1)
        out.append(B)
    return out


# ---------------------------------------------------------------------------------------------------------------------
# Assinatura e certificado (reuso de verificar_assinaturas.py, T18, e de analisar_F12.py, F12)
# ---------------------------------------------------------------------------------------------------------------------
ACS = None


def carrega_acs():
    """AC publicadas, da mesma fonte do F12 (pacote de documentação do TSE, constante _AC_RAIZ_UE_PEMS)."""
    from cryptography import x509
    from analisar_F12 import pems_do_texto_mr_util, chave_da, ext, cn
    zf = zipfile.ZipFile(ZIP_AC)
    blocos, _ = pems_do_texto_mr_util(zf.read('python/lib/mr_util.py').decode('utf-8'))
    acs = {}
    for _, der in blocos:
        c = x509.load_der_x509_certificate(der)
        tipo, k = chave_da(c)
        acs[cn(c.subject)] = {'cert': c, 'tipo': tipo, 'chave': k, 'ski': ext(c, x509.SubjectKeyIdentifier).digest.hex(),
                              'subject_der': c.subject.public_bytes(), 'sha256_der': hashlib.sha256(der).hexdigest(),
                              'fim': c.not_valid_after_utc.isoformat(), 'inicio': c.not_valid_before_utc.isoformat()}
    return acs


def _init_pool():
    global ACS
    ACS = carrega_acs()


def fatos_vsc(bruto, disco):
    """disco: {nome listado: sha512 (bytes) do arquivo baixado}. Devolve os fatos do vota.vsc, com as verificações."""
    from cryptography import x509
    from cryptography.exceptions import UnsupportedAlgorithm
    from cryptography.hazmat.primitives.serialization import Encoding, PublicFormat
    from verificar_assinaturas import entradas, verifica_ass, chave_bruta
    from analisar_F12 import verifica as verifica_cert, ext, cn
    global ACS
    if ACS is None:
        ACS = carrega_acs()
    top = parse(bruto)[0][2]
    b0, b1 = top[0][2], top[1][2]
    cab0 = b0[2][2]; cab1 = b1[2][2]
    o = {'sw_quando': _s(b0[0][2]), 'hw_quando': _s(b1[0][2]),
         'sw_chave': f"{_s(cab0[0][2][0][2])} {_i(cab0[0][2][1][2])}", 'titular': _s(cab1[0][2][0][2]),
         'bloco2': [_i(x[2]) for x in top[2][2]] if len(top) > 2 and isinstance(top[2][2], list) else None}
    sw_cont = b0[3][2]; hw_cont = b1[3][2]
    sw_e = entradas(sw_cont); hw_e = entradas(hw_cont)
    sw_cab = {'tam': _i(cab0[3][2][0][2]), 'sha512': cab0[3][2][1][2]}
    hw_cab = {'tam': _i(cab1[3][2][0][2]), 'sha512': cab1[3][2][1][2], 'ass': cab1[3][2][2][2]}
    o['bloco_sw_resumo_ok'] = hashlib.sha512(sw_cont).digest() == sw_cab['sha512'] and len(sw_cont) == sw_cab['tam']
    o['bloco_hw_resumo_ok'] = hashlib.sha512(hw_cont).digest() == hw_cab['sha512'] and len(hw_cont) == hw_cab['tam']
    cert_b = next((n[2] for n in b1 if (n[0], n[1]) == (2, 1)), None)
    if cert_b is None and len(b1) > 4 and isinstance(b1[4][2], bytes):
        cert_b = b1[4][2]
    pub = ked = None; cert = None
    if cert_b is not None:
        if cert_b.lstrip().startswith(b'-----'):
            cert = x509.load_pem_x509_certificate(cert_b); formato = 'PEM'
        else:
            fim = read_tlv(cert_b, 0)[4]
            cert = x509.load_der_x509_certificate(cert_b[:fim]); formato = 'DER'
        try:
            pub = cert.public_key(); kb = pub.public_bytes(Encoding.X962, PublicFormat.UncompressedPoint); tipo_ch = type(pub).__name__
        except UnsupportedAlgorithm:
            ked = chave_bruta(cert); kb = ked; tipo_ch = 'ed521'
        aki = ext(cert, x509.AuthorityKeyIdentifier)
        aki = aki.key_identifier.hex() if aki and aki.key_identifier else None
        c = {'cn': cn(cert.subject), 'emissor_cn': cn(cert.issuer), 'aki': aki, 'serial': str(cert.serial_number),
             'inicio': cert.not_valid_before_utc.isoformat(), 'fim': cert.not_valid_after_utc.isoformat(),
             'alg': cert.signature_algorithm_oid.dotted_string, 'tipo_chave': tipo_ch, 'formato': formato,
             'sha256_chave': hashlib.sha256(kb).hexdigest(), 'sha256_cert': hashlib.sha256(cert.public_bytes(Encoding.DER)).hexdigest()}
        ac = next((n for n, a in ACS.items() if a['ski'] == aki), None)
        c['ac'] = ac; c['ac_dn_igual'] = c['ac_ass_ok'] = None
        if ac:
            a = ACS[ac]
            c['ac_dn_igual'] = cert.issuer.public_bytes() == a['subject_der']
            c['ac_ass_ok'] = bool(verifica_cert(a['tipo'], a['chave'], cert.signature, cert.tbs_certificate_bytes))
            c['ac_fim'] = a['fim']
        o['cert'] = c
    else:
        o['cert'] = None
    o['bloco_hw_ass'] = verifica_ass(pub, ked, hw_cab['ass'], hashlib.sha512(hw_cont).digest()) if (pub or ked) else None
    ent = {}
    for nm, e in hw_e.items():
        s0 = sw_e.get(nm)
        r = {'tam': e['tam'], 'sha512': e['sha512'].hex(), 'ass': verifica_ass(pub, ked, e['ass'], e['sha512']) if (pub or ked) else None,
             'sw_igual': bool(s0 is not None and s0['sha512'] == e['sha512'] and s0['tam'] == e['tam'])}
        if nm in disco and disco[nm] != e['sha512']:
            r['ass_disco'] = verifica_ass(pub, ked, e['ass'], disco[nm]) if (pub or ked) else None
        ent[nm] = r
    o['entradas'] = ent
    o['sw_so'] = sorted(set(sw_e) - set(hw_e))
    return o


TIPO_DE = {'bu': 'bu', 'busa': 'bu', 'rdv': 'rdv', 'log': 'log', 'logsa': 'log', 'vota': 'vsc', 'sa': 'vsc'}


def ler_secao(arg):
    """Todos os fatos de uma seção. arg = (chave, pasta da seção, turno). Não compara nada com o bweb."""
    k, d, turno = arg[:3]
    o = {'k': k, 'turno': turno, 'aux': None, 'pacotes': [], 'erros': []}
    if not os.path.isdir(d):
        o['erros'].append('pasta ausente'); return o
    fs = sorted(os.listdir(d)); o['arquivos'] = fs
    try:
        aux = json.loads(open(os.path.join(d, 'aux.json'), 'rb').read().decode('utf-8'))
    except Exception as e:  # noqa: BLE001
        o['erros'].append('aux.json: ' + repr(e)[:80]); return o
    o['aux'] = {x: aux.get(x) for x in ('dg', 'hg', 'idg', 'f', 'st')}
    o['aux']['n_hashes'] = len(aux.get('hashes', []))
    for i, h in enumerate(aux.get('hashes', [])):
        pac = {'i': i, 'hash': h.get('hash'), 'st': h.get('st'), 'dr': h.get('dr'), 'hr': h.get('hr'),
               'listados': [[a.get('nm'), a.get('tp')] for a in h.get('arq', [])], 'arq': {}}
        brutos = {}
        for nm, tp in pac['listados']:
            t = TIPO_DE.get(tp)
            if t is None:
                continue
            cam = os.path.join(d, f'{i}-{nm}')
            if not os.path.exists(cam):
                continue
            b = open(cam, 'rb').read()
            brutos[t] = (nm, b)
            pac['arq'][t] = {'nome': nm, 'tp': tp, 'tam': len(b), 'sha512': hashlib.sha512(b).hexdigest()}
        if 'vsc' in brutos:
            nm, b = brutos['vsc']
            calc = base64.b64encode(hashlib.sha256(b).digest()).decode().replace('/', '-')
            try:
                esperado = bytes.fromhex(pac['hash']).decode()
            except Exception:  # noqa: BLE001
                esperado = None
            pac['vsc_sha256'] = calc; pac['aux_hash_txt'] = esperado
            try:
                disco = {brutos[t][0]: bytes.fromhex(pac['arq'][t]['sha512']) for t in ('bu', 'rdv', 'log') if t in brutos}
                pac['vsc'] = fatos_vsc(b, disco)
            except Exception as e:  # noqa: BLE001
                pac['vsc'] = None; o['erros'].append(f'vsc {i}: ' + repr(e)[:120])
        if 'bu' in brutos:
            nm, b = brutos['bu']
            bu = {}
            try:
                A = ler_bu_A(os.path.join(d, f'{i}-{nm}'))
                s, g = bu_para_secao(A)
                bu['A'] = {'mun': A.get('mun'), 'zona': A.get('zona'), 'secao': A.get('secao'), 'loc': A.get('loc'), 'urna': A.get('urna'),
                           'ab': A.get('ab'), 'enc': A.get('enc'), 'pres': s and {x: s[x] for x in ('apt', 'comp', 'B', 'N', 'cand')},
                           'gov': g and {x: g[x] for x in ('comp', 'B', 'N', 'cand')}}
            except Exception as e:  # noqa: BLE001
                bu['A'] = None; o['erros'].append(f'bu A {i}: ' + repr(e)[:120])
            try:
                bu['B'] = ler_bu_B(b)
            except Exception as e:  # noqa: BLE001
                bu['B'] = None; o['erros'].append(f'bu B {i}: ' + repr(e)[:120])
            pac['bu'] = bu
        if 'rdv' in brutos:
            nm, b = brutos['rdv']
            try:
                pac['rdv'] = ler_rdv_B(b)
            except Exception as e:  # noqa: BLE001
                pac['rdv'] = None; o['erros'].append(f'rdv B {i}: ' + repr(e)[:120])
            try:
                ra = rdv_para_bu(ler_rdv_A(os.path.join(d, f'{i}-{nm}')))
                pac['rdv_A'] = {str(c): {x: v for x, v in r.items()} for c, r in ra.items() if c in (1, 3)}
            except Exception as e:  # noqa: BLE001
                pac['rdv_A'] = None; o['erros'].append(f'rdv A {i}: ' + repr(e)[:120])
        if 'log' in brutos:
            nm, b = brutos['log']
            try:
                pac['log'] = ler_log_B(os.path.join(d, f'{i}-{nm}'))
            except Exception as e:  # noqa: BLE001
                pac['log'] = None; o['erros'].append(f'log {i}: ' + repr(e)[:120])
        o['pacotes'].append(pac)
    return o


def modo_ler(conj, limite=None, proc=3):
    from multiprocessing import Pool
    c = CONJ[conj]
    ks = lista(conj)
    if conj in ('e2', 'e1'):
        # prefixo já baixado da extensão, na ordem do sorteio (qualquer prefixo é amostra aleatória simples)
        pre = []
        for k in ks:
            d = pasta_secao(c['pasta'], k)
            if not (os.path.isdir(d) and (os.path.exists(os.path.join(d, 'aux.json')) or os.path.exists(os.path.join(d, 'SEM_AUX')))):
                break
            pre.append(k)
        ks = pre[:-2] if len(pre) > 2 else []  # as duas últimas podem estar no meio do download
    if limite:
        ks = ks[:limite]
    t0 = time.time(); out = {}
    with Pool(proc, initializer=_init_pool) as P:
        for n, r in enumerate(P.imap(ler_secao, [(k, pasta_secao(c['pasta'], k), c['turno']) for k in ks], chunksize=4)):
            out[r['k']] = r
            if (n + 1) % 500 == 0:
                diz(conj, n + 1, 'de', len(ks), round(time.time() - t0), 's')
    grava(f'fatos_{conj}.json.gz', {'conjunto': conj, 'turno': c['turno'], 'n': len(ks), 'ordem': ks, 'secoes': out,
                                    'lido_em': time.strftime('%Y-%m-%d %H:%M:%S UTC', time.gmtime())}, gz=True)
    diz(conj, 'lidas', len(out), 'em', round(time.time() - t0), 's; com erro de leitura:', sum(1 for r in out.values() if r['erros']))


# =====================================================================================================================
# Conferências (D3-1: a até g; D3-3: I1 a I11), por seção
# =====================================================================================================================
def escolhe_pacote(f):
    pacs = f.get('pacotes') or []
    tot = [p for p in pacs if p.get('st') == 'Totalizado']
    if len(tot) == 1:
        return tot[0]
    return pacs[-1] if pacs else None


def votos_bweb(linhas):
    v = {}
    for tv, ds, nr, nm, q in linhas:
        v[nr] = v.get(nr, 0) + q
    return {a: q for a, q in v.items() if q}


def votos_bu_B(bu, cargo='c1'):
    """({número: votos} com 95 branco e 96 nulo, comparecimento do cargo, aptos, eleição), pelo caminho B."""
    for ide, el in bu['eleicoes'].items():
        c = el['cargos'].get(cargo)
        if c is not None:
            v = {}
            for ch, q in c['votos'].items():
                tipo, cand = ch.split(':')
                n = 95 if tipo == '2' else 96 if tipo == '3' else int(cand) if cand else -int(tipo)
                v[n] = v.get(n, 0) + q
            return {a: q for a, q in v.items() if q}, c['comp'], el['apt'], ide
    return None, None, None, None


def votos_bu_A(buA, qual='pres'):
    s = buA.get(qual) if buA else None
    if not s:
        return None
    v = {int(n): q for n, q in s['cand'].items()}
    v[95] = v.get(95, 0) + s['B']; v[96] = v.get(96, 0) + s['N']
    return {a: q for a, q in v.items() if q}


def votos_rdv(rd, cargo='c1'):
    for ck, reg in rd['cargos'].items():
        if ck.endswith('|' + cargo) and 'cont' in reg:
            v = {}
            for ch, q in reg['cont'].items():
                tipo, dig = ch.split(':')
                tipo = int(tipo)
                n = 95 if tipo in (3, 5) else 96 if tipo in (4, 6, 7, 8, 9) else int(dig) if dig.isdigit() else -tipo
                v[n] = v.get(n, 0) + q
            return {a: q for a, q in v.items() if q}, reg['n'], reg.get('seq', '')
    return None, None, None


def dif_votos(x, y):
    """Diferenças x - y por votável (só as não nulas)."""
    return {str(n): x.get(n, 0) - y.get(n, 0) for n in sorted(set(x) | set(y)) if x.get(n, 0) != y.get(n, 0)}


def bloco_final(log, dia):
    cand = [B for B in log if dia in B['dias'] and B['dias'][dia]['gerabu']]
    if cand:
        return max(cand, key=lambda B: B['dias'][dia]['gerabu'][-1][0])
    cand = [B for B in log if dia in B['dias']]
    return cand[-1] if cand else None


def num_cert(cn_):
    if cn_ and cn_.upper().startswith('UEAO') and cn_[4:].isdigit():
        return int(cn_[4:])
    return None


def z_runs(seq, alvo):
    """Teste de sequências (Wald e Wolfowitz) na ordem do arquivo: alvo ou não alvo. Devolve (z, n, a) ou None se V = 0."""
    x = [1 if t == alvo else 0 for t in seq]
    n = len(x); a = sum(x); b = n - a
    if n < 2 or a == 0 or b == 0:
        return None
    r = 1 + sum(1 for i in range(1, n) if x[i] != x[i - 1])
    e = 1 + 2 * a * b / n
    v = 2 * a * b * (2 * a * b - n) / (n * n * (n - 1))
    if v <= 0:
        return None
    return (r - e) / math.sqrt(v), n, a


def conferir(f, bw, turno, fuso_h=None, bw1=None, f1=None):
    """Todas as conferências de uma seção.
    f: fatos (ler_secao); bw: registro do bweb do mesmo turno; fuso_h: hora modal de abertura do município (None no exterior);
    bw1 e f1: bweb e fatos do 1º turno da mesma seção (só para I9 e para o carimbo do vsc do 1º turno).
    Devolve A (classe A), B (classe B), lado (fora do critério), I (identidades violadas), nv (não verificável), inf."""
    k = f['k']; uf, mun, zona, sec = k.split('|')
    R = {'k': k, 'A': {}, 'B': {}, 'lado': {}, 'I': {}, 'nv': [], 'inf': {}, 'sem_arquivo': None}
    if f.get('aux') is None:
        R['sem_arquivo'] = 'sem aux.json'; return R
    R['inf']['aux'] = f['aux']
    pacs = f['pacotes']
    pac = escolhe_pacote(f)
    if pac is None or 'bu' not in pac['arq']:
        R['sem_arquivo'] = 'sem boletim listado e baixado'
        if pac is None:
            return R
    R['inf']['pacote_st'] = pac.get('st'); R['inf']['n_pacotes'] = len(pacs)
    buB = (pac.get('bu') or {}).get('B'); buA = (pac.get('bu') or {}).get('A')
    vsc = pac.get('vsc'); log = pac.get('log'); rd = pac.get('rdv')
    dia = DIA[turno]
    meta = bw['meta'] if bw else None
    # ---------------- (e) resumo publicado do vota.vsc
    if 'vsc' in pac['arq']:
        if pac.get('vsc_sha256') != pac.get('aux_hash_txt'):
            R['A']['e'] = {'aux': pac.get('aux_hash_txt'), 'calculado': pac.get('vsc_sha256')}
    else:
        R['nv'].append('e')
    # ---------------- (b) e (c)
    if vsc is None:
        R['nv'] += ['b', 'c', 'd']
    else:
        ent = vsc['entradas']
        for t in ('bu', 'rdv', 'log'):
            a = pac['arq'].get(t)
            if a is None:
                continue
            e = ent.get(a['nome'])
            cls = R['A'] if t == 'bu' else R['B']
            if e is None:
                cls['b_' + t] = 'arquivo baixado que o vsc não lista'; R['A']['c_' + t] = 'sem assinatura para o arquivo'
                continue
            if e['sha512'] != a['sha512'] or e['tam'] != a['tam']:
                cls['b_' + t] = {'tam_vsc': e['tam'], 'tam_disco': a['tam']}
                if not e.get('ass_disco'):
                    R['A']['c_' + t] = 'assinatura não confere com o arquivo do disco'
            if not e['ass']:
                R['A']['c_' + t] = 'assinatura inválida para o resumo listado'
            if not e['sw_igual']:
                R['lado']['sw_dif_' + t] = True
        if not vsc['bloco_hw_ass'] or not vsc['bloco_hw_resumo_ok']:
            R['A']['c_bloco'] = {'assinatura': vsc['bloco_hw_ass'], 'resumo_ok': vsc['bloco_hw_resumo_ok']}
        if not vsc['bloco_sw_resumo_ok']:
            R['lado']['bloco_sw_resumo'] = True
        outros = [nm for nm, e in ent.items() if not e['ass'] and nm not in {a['nome'] for a in pac['arq'].values()}]
        if outros:
            R['lado']['c2'] = outros
        R['inf']['modo_ass'] = vsc['bloco_hw_ass']
        R['inf']['n_arquivos_conferidos'] = sum(1 for t in ('bu', 'rdv', 'log') if t in pac['arq'])
        R['inf']['n_entradas'] = len(ent); R['inf']['n_entradas_ass_ok'] = sum(1 for e in ent.values() if e['ass'])
        R['inf']['hw_quando'] = vsc['hw_quando']; R['inf']['sw_chave'] = vsc['sw_chave']; R['inf']['bloco2'] = vsc['bloco2']
        # ---------------- (d) certificado
        c = vsc.get('cert')
        if c is None:
            R['nv'].append('d')
        else:
            R['inf']['ac'] = c['ac']; R['inf']['chave'] = c['sha256_chave']; R['inf']['cert_cn'] = c['cn']
            R['inf']['cert_inicio'] = c['inicio']; R['inf']['cert_fim'] = c['fim']
            if c['ac'] is None:
                R['A']['d1'] = {'motivo': 'identificador de AC que não é de nenhuma AC publicada', 'aki': c['aki'], 'emissor': c['emissor_cn']}
            elif not c['ac_dn_igual'] or not c['ac_ass_ok']:
                R['A']['d1'] = {'motivo': 'emissor ou assinatura do certificado não confere com a AC', 'ac': c['ac'],
                                'dn': c['ac_dn_igual'], 'assinatura': c['ac_ass_ok']}
            nc = num_cert(c['cn'])
            div = {}
            if buB is not None and nc != buB['urna']:
                div['boletim'] = buB['urna']
            if meta is not None and meta['NR_URNA_EFETIVADA'].lstrip('-').isdigit() and int(meta['NR_URNA_EFETIVADA']) > 0 and nc != int(meta['NR_URNA_EFETIVADA']):
                div['bweb'] = meta['NR_URNA_EFETIVADA']
            if div and not (buB is not None and buB.get('sa')):
                R['A']['d2'] = dict(div, certificado=c['cn'])
            elif div:
                R['lado']['d2_junta'] = dict(div, certificado=c['cn'])
    # ---------------- (f) mais de um pacote
    if len(pacs) > 1:
        vs = []
        for p in pacs:
            b = (p.get('bu') or {}).get('B')
            vs.append(votos_bu_B(b)[0] if b else None)
        R['inf']['pacotes'] = [{'i': p['i'], 'st': p['st'], 'dr': p['dr'], 'hr': p['hr'], 'votos': v} for p, v in zip(pacs, vs)]
        lidos = [json.dumps(v, sort_keys=True) for v in vs if v is not None]
        if len(set(lidos)) > 1:
            R['A']['f'] = R['inf']['pacotes']
    # ---------------- boletim: (a) e (g)
    if buB is None and buA is None:
        if 'bu' in pac['arq']:
            R['nv'].append('a'); R['lado']['boletim_ilegivel'] = True
        return R
    vB = cB = aptB = ide = None
    if buB is not None:
        vB, cB, aptB, ide = votos_bu_B(buB)
    vA = votos_bu_A(buA)
    if vA is not None and vB is not None and vA != vB:
        R['lado']['leitores_A_B_diferem'] = dif_votos(vA, vB)
    R['inf']['comp'] = buB['comp'] if buB else None
    R['inf']['explica'] = []
    if buB is not None:
        if buB['tipo_urna'] != 1:
            R['inf']['explica'].append(f"tipo de urna {buB['tipo_urna']}")
        if buB['tipo_arq'] != 1:
            R['inf']['explica'].append(f"tipo de arquivo {buB['tipo_arq']}")
        if buB.get('sa'):
            R['inf']['explica'].append('boletim de junta')
    if bw is not None:
        vW = votos_bweb(bw['v1'])
        dA = dif_votos(vW, vA) if vA is not None else None
        dB = dif_votos(vW, vB) if vB is not None else None
        if (dA or vA is None) and (dB or vB is None) and (dA or dB):
            R['A']['a'] = {'bweb_menos_boletim': dB if dB is not None else dA,
                           'efeito_13_menos_22': (vW.get(13, 0) - vW.get(22, 0)) - ((vB or vA).get(13, 0) - (vB or vA).get(22, 0))}
        elif dA or dB:
            R['lado']['a_so_um_leitor'] = {'A': dA, 'B': dB}
        if buB is not None:
            if int(meta['QT_COMPARECIMENTO']) != buB['comp'] or (cB is not None and cB != buB['comp']):
                R['A']['a_comp'] = {'bweb': int(meta['QT_COMPARECIMENTO']), 'boletim': buB['comp'], 'cargo': cB}
            if aptB is not None and int(meta['QT_APTOS']) != aptB:
                R['B']['a_aptos'] = {'bweb': int(meta['QT_APTOS']), 'boletim': aptB}
            # governador, ao lado
            vG = votos_bu_B(buB, 'c3')[0]
            if vG is not None or bw['v3']:
                dG = dif_votos(votos_bweb(bw['v3']), vG or {})
                if dG:
                    R['lado']['a_governador'] = dG
                R['inf']['tem_gov'] = True
            # (g)
            g = {}
            for nome, idt in (('envelope', buB['env']), ('conteudo', buB['sec'])):
                if (idt.get('mun'), idt.get('zona'), idt.get('secao', int(sec))) != (int(mun), int(zona), int(sec)):
                    g['chave_' + nome] = idt
            if (pac.get('dr'), pac.get('hr')) != (None, None):
                ta = t_aux(pac['dr'], pac['hr']); tb = t_bw(meta['DT_BU_RECEBIDO'])
                if ta != tb:
                    g['recebimento'] = {'aux': f"{pac['dr']} {pac['hr']}", 'bweb': meta['DT_BU_RECEBIDO'], 'dif_s': (ta - tb) if (ta and tb) else None}
            cod_bw = re.sub(r'\D', '', meta['CD_CARGA_1_URNA_EFETIVADA'] + meta['CD_CARGA_2_URNA_EFETIVADA'])
            if cod_bw != buB['cod_carga']:
                g['carga'] = {'bweb': cod_bw, 'boletim': buB['cod_carga']}
            if str(buB['urna']) != meta['NR_URNA_EFETIVADA']:
                g['urna'] = {'bweb': meta['NR_URNA_EFETIVADA'], 'boletim': buB['urna']}
            for nome, campo, val in (('abertura', 'DT_ABERTURA', buB['ab']), ('encerramento', 'DT_ENCERRAMENTO', buB['enc']),
                                     ('emissao', 'DT_EMISSAO_BU', buB['emissao'])):
                if t_bw(meta[campo]) != t_je(val):
                    g[nome] = {'bweb': meta[campo], 'boletim': val}
            if g:
                if buB.get('sa') and set(g) <= {'abertura', 'encerramento', 'carga', 'urna', 'emissao'}:
                    R['lado']['g_junta'] = g
                else:
                    R['B']['g'] = g
            lado = {}
            if meta['CD_FLASHCARD_URNA_EFETIVADA'].upper() != buB['fc']:
                lado['midia_de_carga'] = {'bweb': meta['CD_FLASHCARD_URNA_EFETIVADA'], 'boletim': buB['fc']}
            if t_bw(meta['DT_CARGA_URNA_EFETIVADA']) != t_je(buB['dt_carga']):
                lado['data_da_carga'] = {'bweb': meta['DT_CARGA_URNA_EFETIVADA'], 'boletim': buB['dt_carga']}
            if meta['NR_LOCAL_VOTACAO'] != str(buB['sec']['loc']):
                lado['local'] = {'bweb': meta['NR_LOCAL_VOTACAO'], 'boletim': buB['sec']['loc']}
            if buB['id'] != PLEITO[turno] or buB['fase'] != 2 or buB['env_id'] != PLEITO[turno] or buB['env_fase'] != 2:
                lado['pleito_fase'] = {'id': buB['id'], 'fase': buB['fase'], 'env_id': buB['env_id'], 'env_fase': buB['env_fase']}
            if lado:
                R['lado']['g2'] = lado
    else:
        R['nv'].append('a')
    if buB is None:
        return R
    # =============================== D3-3
    I = R['I']; inf = R['inf']
    if log:
        if len(log) > 1:
            inf['explica'].append(f'pacote com {len(log)} logs')
        if any(B['ev'].get('contingencia') for B in log):
            inf['explica'].append('linha de contingência no log')
        if any(B['ev'].get('recuperador') or 'RED' in B['apps'] for B in log):
            inf['explica'].append('recuperador de dados no log')
    # I1 e I11
    if rd is None:
        R['nv'] += ['I1', 'I11']
    else:
        vR, nR, seq = votos_rdv(rd)
        if vR is None:
            R['nv'] += ['I1', 'I11']
        else:
            d = dif_votos(vR, vB or {})
            if d:
                I['I1'] = {'rdv_menos_boletim': d}
            ra = (pac.get('rdv_A') or {}).get('1')
            if ra is not None:
                vRA = {int(x[4:]): q for x, q in ra.items() if x.startswith('num:')}
                vRA[95] = ra.get('B', 0); vRA[96] = ra.get('N', 0)
                vRA = {a: q for a, q in vRA.items() if q}
                if vRA != vR:
                    R['lado']['leitores_rdv_diferem'] = dif_votos(vRA, vR)
            toks = seq.split(',') if seq else []
            z13 = z_runs(toks, '13'); z22 = z_runs(toks, '22')
            inf['I11'] = {'z13': z13[0] if z13 else None, 'z22': z22[0] if z22 else None, 'n': len(toks)}
            gR, _, _ = votos_rdv(rd, 'c3')
            if gR is not None:
                gB = votos_bu_B(buB, 'c3')[0]
                dg = dif_votos(gR, gB or {})
                if dg:
                    R['lado']['I1_governador'] = dg
            for campo in ('urna', 'cod_carga', 'fc', 'dt_carga'):
                if rd.get(campo) != buB.get(campo):
                    R['lado'].setdefault('rdv_cabecalho', {})[campo] = [rd.get(campo), buB.get(campo)]
            if (rd['sec']['mun'], rd['sec']['zona'], rd['sec']['secao']) != (int(mun), int(zona), int(sec)):
                R['lado'].setdefault('rdv_cabecalho', {})['secao'] = rd['sec']
    if turno != 2:
        return R
    if not log:
        R['nv'] += ['I2', 'I3', 'I4', 'I5', 'I6', 'I7', 'I8', 'I9', 'I10']
        return R
    Ds = [B['dias'][dia] for B in log if dia in B['dias']]
    BF = bloco_final(log, dia)
    DF = BF['dias'][dia] if BF else None
    # I2
    comp_log = sum(D['comp'] for D in Ds)
    inf['comp_log'] = comp_log
    d2 = {}
    if comp_log != buB['comp']:
        d2['boletim'] = buB['comp']
    if meta is not None and comp_log != int(meta['QT_COMPARECIMENTO']):
        d2['bweb'] = int(meta['QT_COMPARECIMENTO'])
    if d2:
        I['I2'] = dict(d2, log=comp_log)
    # I3
    tot_pres = sum((vB or {}).values())
    c3 = sum(D['conf'].get('Presidente', 0) + D['nsusp'].get('Presidente', 0) for D in Ds)
    if c3 != tot_pres:
        I['I3'] = {'log': c3, 'boletim': tot_pres, 'nulo_por_suspensao': sum(D['nsusp'].get('Presidente', 0) for D in Ds)}
    inf['nsusp_pres'] = sum(D['nsusp'].get('Presidente', 0) for D in Ds)
    vG = votos_bu_B(buB, 'c3')[0]
    if vG is not None:
        cg = sum(D['conf'].get('Governador', 0) + D['nsusp'].get('Governador', 0) for D in Ds)
        if cg != sum(vG.values()):
            R['lado']['I3_governador'] = {'log': cg, 'boletim': sum(vG.values())}
    # I4
    if DF is None:
        R['nv'] += ['I4', 'I5', 'I6', 'I7']
    else:
        uid = DF['gerabu'][-1][1] if DF['gerabu'] else (max(DF['ids'], key=DF['ids'].get) if DF['ids'] else None)
        d4 = {}
        try:
            nlog = int(uid)
        except Exception:  # noqa: BLE001
            nlog = None
        if nlog != buB['urna']:
            d4['boletim'] = buB['urna']
        if meta is not None and str(nlog) != meta['NR_URNA_EFETIVADA']:
            d4['bweb'] = meta['NR_URNA_EFETIVADA']
        if vsc and vsc.get('cert') and num_cert(vsc['cert']['cn']) != nlog:
            d4['certificado'] = vsc['cert']['cn']
        if len(DF['ids']) > 1:
            d4['mais_de_uma_urna_no_dia'] = DF['ids']
        if d4:
            I['I4'] = dict(d4, log=uid)
        # I5
        d5 = {}
        for nome, vals, vbu in (('codigo', BF['cod'], buB['cod_carga']), ('midia', BF['fc'], buB['fc']), ('data', BF['dig'], buB['dt_carga'])):
            if not vals:
                d5[nome] = {'log': None, 'boletim': vbu}
            elif vals[-1] != vbu:
                d5[nome] = {'log': vals[-1], 'boletim': vbu, 'algum_igual': vbu in vals}
        if meta is not None:
            cod_bw = re.sub(r'\D', '', meta['CD_CARGA_1_URNA_EFETIVADA'] + meta['CD_CARGA_2_URNA_EFETIVADA'])
            if BF['cod'] and BF['cod'][-1] != cod_bw:
                d5['codigo_bweb'] = {'log': BF['cod'][-1], 'bweb': cod_bw}
            if BF['fc'] and BF['fc'][-1] != meta['CD_FLASHCARD_URNA_EFETIVADA'].upper():
                d5['midia_bweb'] = {'log': BF['fc'][-1], 'bweb': meta['CD_FLASHCARD_URNA_EFETIVADA']}
            if BF['dig'] and t_je(BF['dig'][-1]) != t_bw(meta['DT_CARGA_URNA_EFETIVADA']):
                d5['data_bweb'] = {'log': BF['dig'][-1], 'bweb': meta['DT_CARGA_URNA_EFETIVADA']}
        if d5:
            I['I5'] = d5
        # I6
        d6 = {}
        for campo, esperado in (('mun', int(mun)), ('zona', int(zona)), ('secao', int(sec))):
            vals = DF[campo] or ([BF['ult'][campo]] if BF['ult'][campo] is not None else [])
            if not vals:
                d6[campo] = 'sem linha no log'
            elif any((not v.isdigit()) or int(v) != esperado for v in vals):
                d6[campo] = vals
        if d6:
            I['I6'] = d6
        # I7
        d7 = {}
        prontas = [t for D in Ds for t in D['pronta']]
        ab = t_je(buB['ab']); enc = t_je(buB['enc']); emi = t_je(buB['emissao'])
        if ab is not None:
            if not prontas:
                d7['i'] = {'log': None, 'boletim': buB['ab']}
            elif abs(min(prontas) - ab) > 1:
                d7['i'] = {'log': hms(min(prontas)), 'boletim': buB['ab'], 'dif_s': min(prontas) - ab}
        if enc is not None:
            if not DF['encconf']:
                d7['ii'] = {'log': None, 'boletim': buB['enc']}
            elif abs(max(DF['encconf']) - enc) > 1:
                d7['ii'] = {'log': hms(max(DF['encconf'])), 'boletim': buB['enc'], 'dif_s': max(DF['encconf']) - enc}
        if emi is not None:
            if not DF['inienc'] or not DF['gerabu']:
                d7['iii'] = {'inicio': DF['inienc'][-1:] or None, 'gera_bu': DF['gerabu'][-1:] or None, 'boletim': buB['emissao']}
            else:
                lo = max(DF['inienc']); gs = [t for t, _ in DF['gerabu'] if t >= lo]
                hi = min(gs) if gs else max(t for t, _ in DF['gerabu'])
                if emi < lo - 5 or emi > hi + 5:
                    d7['iii'] = {'inicio': hms(lo), 'gera_bu': hms(hi), 'boletim': buB['emissao'], 'dif_inicio_s': emi - lo, 'dif_fim_s': emi - hi}
        tv = t_je(vsc['hw_quando']) if vsc else None
        if tv is not None and DF['ult_t'] is not None:
            inf['vsc_menos_fim_do_log_s'] = tv - DF['ult_t']
            if tv < DF['ult_t'] - 5:
                d7['iv'] = {'vsc': vsc['hw_quando'], 'fim_do_log': hms(DF['ult_t']), 'dif_s': tv - DF['ult_t']}
        if d7:
            I['I7'] = d7
    # I8
    d8 = {}
    va = sum(D['v_antes'] for D in Ds); vd = sum(D['v_depois'] for D in Ds); vs_ = sum(D['v_sem_pronta'] for D in Ds)
    if va or vd or vs_:
        d8['i'] = {'antes_da_urna_pronta': va, 'depois_do_encerramento': vd, 'em_bloco_sem_urna_pronta': vs_}
    tv = t_je(vsc['hw_quando']) if vsc else None
    ta = t_aux(pac['dr'], pac['hr']) if pac.get('dr') else None
    if tv is not None and ta is not None:
        if fuso_h is None:
            inf['I8ii_nao_se_aplica'] = True
        else:
            tv_bsb = tv - (fuso_h - 8) * 3600
            inf['recebimento_menos_vsc_s'] = ta - tv_bsb
            if ta < tv_bsb - 120:
                d8['ii'] = {'recebimento_brasilia': f"{pac['dr']} {pac['hr']}", 'vsc_local': vsc['hw_quando'], 'fuso_h': fuso_h - 8, 'dif_s': ta - tv_bsb}
    if d8:
        I['I8'] = d8
    # I9 e carimbo do vsc do 1º turno
    d1 = DIA[1]
    D1s = [B['dias'][d1] for B in log if d1 in B['dias']]
    if bw1 is not None and meta is not None and bw1['meta']['NR_URNA_EFETIVADA'] == meta['NR_URNA_EFETIVADA']:
        inf['mesma_urna'] = True
        c1 = sum(D['comp'] for D in D1s)
        if c1 != int(bw1['meta']['QT_COMPARECIMENTO']):
            I['I9'] = {'log_0410': c1, 'bweb_1t': int(bw1['meta']['QT_COMPARECIMENTO'])}
        if f1 is not None:
            p1 = escolhe_pacote(f1)
            v1 = p1.get('vsc') if p1 else None
            ai = [t for D in D1s for t in D['assini']]; af = [t for D in D1s for t in D['assfim']]
            if v1 and ai and af:
                t1 = t_je(v1['hw_quando'])
                inf['vsc1t_no_intervalo'] = bool(min(ai) - 5 <= t1 <= max(af) + 5)
                inf['vsc1t_dif_s'] = [t1 - min(ai), t1 - max(af)]
                gl = [t for D in D1s for t in D['geralog']]
                if gl:
                    inf['vsc1t_menos_geralog_s'] = t1 - max(gl)
    else:
        inf['mesma_urna'] = False
    # I10
    retro = [r for B in log for r in B['retro']]
    n_retro = sum(B['n_retro'] - B['n_retro_aj'] for B in log)
    if n_retro:
        I['I10'] = {'passos': n_retro, 'exemplos': [[r[0], hms(r[1]), hms(r[2]), r[3], r[4]] for r in retro[:4]]}
    inf['retro_com_ajuste'] = sum(B['n_retro_aj'] for B in log)
    inf['ajuste_no_dia'] = sum(D['ajuste'] for D in Ds); inf['suspensa'] = sum(D['suspensa'] for D in Ds)
    inf['cancel_enc'] = sum(D['cancel_enc'] for D in Ds)
    return R


# =====================================================================================================================
# Agregação, alcance e calibração
# =====================================================================================================================
def cp(x, n):
    """Clopper e Pearson. Com x = 0, o limite superior do desenho: 1 - 0,05^(1/n). Com x > 0, intervalo bilateral de 95%."""
    from scipy.stats import beta
    if not n:
        return None, None
    if x == 0:
        return 0.0, 1 - 0.05 ** (1 / n)
    lo = float(beta.ppf(0.025, x, n - x + 1))
    hi = 1.0 if x == n else float(beta.ppf(0.975, x + 1, n - x))
    return lo, hi


_U = {}


def universo():
    if not _U:
        from lib import carregar
        d = carregar(os.path.join(REPO, 'dados', 'secoes2026.json.gz'))
        comps = []; horas = collections.defaultdict(collections.Counter); chaves = []
        for k, v in d.items():
            s2 = v.get('2')
            if not s2:
                continue
            comps.append(s2['comp']); chaves.append(k)
            uf, mun = k.split('|')[:2]
            if uf != 'ZZ' and s2.get('ab'):
                horas[uf + '|' + mun][int(s2['ab'][:2]) + (1 if int(s2['ab'][3:5]) >= 30 else 0)] += 1
        ordem = sorted(comps, reverse=True)
        ac = [0]
        for c in ordem:
            ac.append(ac[-1] + c)
        _U.update({'acum': ac, 'n': len(comps), 'comp_total': sum(comps), 'chaves': chaves, 'comps': comps,
                   'fuso': {m: h.most_common(1)[0][0] for m, h in horas.items()}})
    return _U


def dano(K):
    """Pior caso absoluto: todos os votos das K maiores seções invertidos."""
    U = universo()
    return 2 * U['acum'][min(K, U['n'])]


def alcance(x, n, m=0):
    lo, hi = cp(x, n)
    K = math.ceil(N_U * hi - 1e-9)
    o = {'x': x, 'n': n, 'limite_inferior': lo, 'limite_superior': hi, 'secoes_no_pais_teto': K, 'dano_maximo_votos': dano(K),
         'fracao_da_margem': dano(K) / MARGEM}
    if m:
        _, him = cp(m, n)
        Km = math.ceil(N_U * him - 1e-9)
        o.update({'ausentes': m, 'limite_superior_ausentes': him, 'secoes_teto_com_ausentes': K + Km,
                  'dano_maximo_com_ausentes': dano(K + Km), 'fracao_da_margem_com_ausentes': dano(K + Km) / MARGEM})
    return o


def fuso_de(k):
    uf, mun = k.split('|')[:2]
    return None if uf == 'ZZ' else universo()['fuso'].get(uf + '|' + mun)


def conferir_conjunto(F, bw, turno, bw1=None, F1=None, so=None):
    out = []
    for k in (so or F['ordem']):
        f = F['secoes'][k]
        out.append(conferir(f, bw.get(k), turno, fuso_de(k), bw1.get(k) if bw1 else None, F1['secoes'].get(k) if F1 else None))
    return out


IDS = ('I1', 'I2', 'I3', 'I4', 'I5', 'I6', 'I7', 'I8', 'I9', 'I10')


def stats_I11(res, campo='z13'):
    zs = [r['inf']['I11'][campo] for r in res if r['inf'].get('I11') and r['inf']['I11'][campo] is not None]
    m = len(zs)
    if not m:
        return {'m': 0}
    med = sum(zs) / m
    dp = math.sqrt(sum((z - med) ** 2 for z in zs) / (m - 1)) if m > 1 else None
    return {'m': m, 'Z': sum(zs) / math.sqrt(m), 'media_z': med, 'dp_z': dp, 'fracao_abs_z_maior_3': sum(1 for z in zs if abs(z) > 3) / m,
            'n_abs_z_maior_3': sum(1 for z in zs if abs(z) > 3), 'z_min': min(zs), 'z_max': max(zs)}


def resumir(nome, res, turno, pasta):
    n = len(res)
    S = {'conjunto': nome, 'turno': turno, 'n': n}
    S['sem_arquivo'] = [[r['k'], r['sem_arquivo']] for r in res if r['sem_arquivo']]
    cA = collections.Counter(); cB = collections.Counter(); cL = collections.Counter(); cN = collections.Counter()
    for r in res:
        for c in r['A']: cA[c] += 1
        for c in r['B']: cB[c] += 1
        for c in r['lado']: cL[c] += 1
        for c in set(r['nv']): cN[c] += 1
    S['classe_A_por_conferencia'] = dict(cA); S['classe_B_por_conferencia'] = dict(cB); S['ao_lado'] = dict(cL); S['nao_verificavel'] = dict(cN)
    S['X_classe_A'] = sum(1 for r in res if r['A'])
    S['secoes_com_classe_B'] = sum(1 for r in res if r['B'])
    S['secoes_so_com_classe_B'] = sum(1 for r in res if r['B'] and not r['A'])
    gdet = collections.Counter()
    for r in res:
        for c in (r['B'].get('g') or {}):
            gdet[c] += 1
    S['g_por_campo'] = dict(gdet)
    S['assinatura_nao_verificavel'] = sum(1 for r in res if 'c' in r['nv'])
    S['arquivos_com_resumo_conferido'] = sum(r['inf'].get('n_arquivos_conferidos', 0) for r in res)
    S['assinaturas_de_arquivo_verificadas'] = sum(r['inf'].get('n_entradas_ass_ok', 0) for r in res)
    S['entradas_listadas_nos_vsc'] = sum(r['inf'].get('n_entradas', 0) for r in res)
    S['blocos_de_hardware_com_assinatura_valida'] = sum(1 for r in res if r['inf'].get('modo_ass'))
    S['chave_de_software'] = dict(collections.Counter(str(r['inf'].get('sw_chave')) for r in res if 'sw_chave' in r['inf']))
    S['modelo_e_algoritmo_do_vsc'] = dict(collections.Counter(str(r['inf'].get('bloco2')) for r in res if 'bloco2' in r['inf']))
    val = [r for r in res if r['inf'].get('cert_inicio') and r['inf'].get('hw_quando')]
    S['certificado_valido_no_carimbo_do_vsc'] = sum(1 for r in val if r['inf']['cert_inicio'][:10].replace('-', '') <= r['inf']['hw_quando'][:8] <= r['inf']['cert_fim'][:10].replace('-', ''))
    S['certificados_com_datas'] = len(val)
    S['por_ac'] = dict(collections.Counter(str(r['inf'].get('ac')) for r in res if 'ac' in r['inf']))
    S['modo_da_assinatura'] = dict(collections.Counter(str(r['inf'].get('modo_ass')) for r in res if 'modo_ass' in r['inf']))
    S['aux_estado'] = dict(collections.Counter(str((r['inf'].get('aux') or {}).get('st')) for r in res))
    S['aux_data_geracao'] = dict(collections.Counter(str((r['inf'].get('aux') or {}).get('dg')) for r in res))
    S['pacote_estado'] = dict(collections.Counter(str(r['inf'].get('pacote_st')) for r in res))
    S['n_pacotes'] = dict(collections.Counter(str(r['inf'].get('n_pacotes')) for r in res))
    # (d3) mesma chave em duas seções
    ch = collections.defaultdict(list)
    for r in res:
        if r['inf'].get('chave'):
            ch[r['inf']['chave']].append(r['k'])
    S['d3_chave_repetida'] = [v for v in ch.values() if len(v) > 1]
    # efeito (a)
    ef = [r['A']['a']['efeito_13_menos_22'] if 'a' in r['A'] else 0 for r in res]
    if n > 1:
        med = sum(ef) / n; var = sum((e - med) ** 2 for e in ef) / (n - 1)
        S['efeito_a'] = {'media_por_secao': med, 'nacional': N_U * med, 'ep_nacional': N_U * math.sqrt(var / n * (1 - n / N_U)),
                         'a_favor_do_13': sum(1 for e in ef if e > 0), 'a_favor_do_22': sum(1 for e in ef if e < 0)}
    # identidades
    Iq = {}
    for j in IDS + ('I11',):
        den = sum(1 for r in res if j not in r['nv'] and not r['sem_arquivo'])
        v = [r for r in res if j in r['I']]
        ex = [r for r in v if r['inf'].get('explica')]
        lo, hi = cp(len(v), den) if den else (None, None)
        Iq[j] = {'verificadas': den, 'violam': len(v), 'explicadas_por_evento': len(ex), 'sem_explicacao': len(v) - len(ex),
                 'proporcao': len(v) / den if den else None, 'ic95': [lo, hi], 'estimativa_nacional': N_U * len(v) / den if den else None}
    for j in ('I7', 'I8'):
        sub = collections.Counter()
        for r in res:
            for c in (r['I'].get(j) or {}):
                sub[c] += 1
        Iq[j]['por_item'] = dict(sub)
    S['identidades'] = Iq
    S['violam_I7_ou_I8'] = sum(1 for r in res if 'I7' in r['I'] or 'I8' in r['I'])
    S['violam_horario_I7_I8_I10'] = sum(1 for r in res if any(j in r['I'] for j in ('I7', 'I8', 'I10')))
    S['violam_horario_sem_explicacao'] = sum(1 for r in res if any(j in r['I'] for j in ('I7', 'I8', 'I10')) and not r['inf'].get('explica'))
    S['violam_alguma_identidade'] = sum(1 for r in res if r['I'])
    S['violam_alguma_sem_explicacao'] = sum(1 for r in res if r['I'] and not r['inf'].get('explica'))
    S['rdv_ausente'] = sum(1 for r in res if 'I1' in r['nv'])
    S['com_evento_que_explica'] = sum(1 for r in res if r['inf'].get('explica'))
    S['eventos'] = dict(collections.Counter(e.split(' com ')[0] if e.startswith('pacote') else e for r in res for e in r['inf'].get('explica', [])))
    S['I11_13'] = stats_I11(res, 'z13'); S['I11_22'] = stats_I11(res, 'z22')
    if turno == 2:
        ds = sorted(r['inf']['vsc_menos_fim_do_log_s'] for r in res if 'vsc_menos_fim_do_log_s' in r['inf'])
        if ds:
            S['vsc_menos_fim_do_log_s'] = {'n': len(ds), 'min': ds[0], 'p01': ds[len(ds) // 100], 'mediana': ds[len(ds) // 2], 'p99': ds[(len(ds) * 99) // 100],
                                           'max': ds[-1], 'acima_de_120s': sum(1 for d in ds if d > 120)}
        ds = sorted(r['inf']['recebimento_menos_vsc_s'] for r in res if 'recebimento_menos_vsc_s' in r['inf'])
        if ds:
            S['recebimento_menos_vsc_s'] = {'n': len(ds), 'min': ds[0], 'p01': ds[len(ds) // 100], 'mediana': ds[len(ds) // 2], 'max': ds[-1],
                                            'nao_se_aplica_exterior': sum(1 for r in res if r['inf'].get('I8ii_nao_se_aplica'))}
        mu = [r for r in res if r['inf'].get('mesma_urna')]
        S['mesma_urna_nos_dois_turnos'] = len(mu)
        v1 = [r for r in mu if 'vsc1t_no_intervalo' in r['inf']]
        S['vsc1t_no_intervalo_de_assinatura'] = {'verificadas': len(v1), 'dentro': sum(1 for r in v1 if r['inf']['vsc1t_no_intervalo']),
                                                 'fora': [[r['k'], r['inf']['vsc1t_dif_s']] for r in v1 if not r['inf']['vsc1t_no_intervalo']][:20]}
        dd = sorted(r['inf']['vsc1t_menos_geralog_s'] for r in mu if 'vsc1t_menos_geralog_s' in r['inf'])
        if dd:
            S['vsc1t_menos_geralog_s'] = {'n': len(dd), 'min': dd[0], 'mediana': dd[len(dd) // 2], 'p99': dd[(len(dd) * 99) // 100], 'max': dd[-1]}
        S['nulo_por_suspensao_presidente'] = sum(r['inf'].get('nsusp_pres', 0) for r in res)
        S['secoes_com_votacao_suspensa'] = sum(1 for r in res if r['inf'].get('suspensa'))
        S['secoes_com_ajuste_de_hora_no_dia'] = sum(1 for r in res if r['inf'].get('ajuste_no_dia'))
        S['passos_para_tras_com_ajuste'] = sum(r['inf'].get('retro_com_ajuste', 0) for r in res)
    # casos individuais
    casos = []
    for r in res:
        relev = {c: v for c, v in r['lado'].items() if c not in ('g2',)}
        if r['A'] or r['B'] or r['I'] or r['sem_arquivo'] or relev or r['lado'].get('g2'):
            d = pasta_secao(pasta, r['k'])
            casos.append({'secao': r['k'], 'pasta': d, 'arquivos': sorted(os.listdir(d)) if os.path.isdir(d) else None,
                          'classe_A': r['A'], 'classe_B': r['B'], 'identidades': r['I'], 'ao_lado': r['lado'], 'sem_arquivo': r['sem_arquivo'],
                          'evento_que_explica': r['inf'].get('explica'), 'aux': r['inf'].get('aux'), 'pacote_estado': r['inf'].get('pacote_st'),
                          'comparecimento': r['inf'].get('comp')})
    return S, casos


# ---------------------------------------------------------------------------------------------------------------------
# Calibração por efeito plantado (campo "poder" do desenho) e explicações inocentes plantadas
# ---------------------------------------------------------------------------------------------------------------------
def je(t):
    return time.strftime('%Y%m%dT%H%M%S', time.gmtime(t))


def _move_bweb(rec, de, para, q):
    rec = copy.deepcopy(rec); achou = False
    for l in rec['v1']:
        if l[2] == de:
            l[4] -= q
        if l[2] == para:
            l[4] += q; achou = True
    if not achou:
        rec['v1'].append([1, 'Nominal', para, '', q])
    return rec


def _bu_c1(f):
    pac = escolhe_pacote(f); bu = pac['bu']
    for el in bu['B']['eleicoes'].values():
        if 'c1' in el['cargos']:
            return pac, bu, el['cargos']['c1']
    return pac, bu, None


def _copia_secao(k, origem, destino):
    d0 = pasta_secao(origem, k); d1 = pasta_secao(destino, k)
    if os.path.isdir(d1):
        shutil.rmtree(d1)
    os.makedirs(os.path.dirname(d1), exist_ok=True)
    shutil.copytree(d0, d1)
    return d1


def calibrar(F2, bw2, bw1, F1, res_obs, pasta2):
    rng = random.Random
    ordem = F2['ordem']
    base = {r['k']: r for r in res_obs}
    cal = {}

    def novos(res, campo, cod):
        return {r['k'] for r in res if cod in r[campo] and cod not in base[r['k']][campo]}

    # P1: 5 votos do 22 para o 13 em 30 seções, só no bweb
    g = rng(SEMENTE + 1)
    elig = [k for k in ordem if bw2.get(k) and votos_bweb(bw2[k]['v1']).get(22, 0) >= 5]
    alvo = set(g.sample(elig, 30))
    bwm = dict(bw2)
    for k in alvo:
        bwm[k] = _move_bweb(bw2[k], 22, 13, 5)
    res = conferir_conjunto(F2, bwm, 2, bw1, F1)
    ap = novos(res, 'A', 'a')
    ef = sum(r['A']['a']['efeito_13_menos_22'] for r in res if r['k'] in ap)
    cal['P1_bweb_5_votos_em_30'] = {'plantadas': 30, 'apontadas_por_a': len(ap & alvo), 'apontadas_fora_do_plantio': len(ap - alvo),
                                    'exato': ap == alvo, 'efeito_medido_13_menos_22': ef, 'efeito_plantado': 30 * 10}
    # P5: 3 votos do 22 para o 13 só no boletim decodificado
    g = rng(SEMENTE + 5)
    elig = [k for k in ordem if (lambda x: x[2] is not None and x[2]['votos'].get('1:22', 0) >= 3)(_bu_c1(F2['secoes'][k])) and escolhe_pacote(F2['secoes'][k]).get('rdv')]
    alvo = set(g.sample(elig, 30)); Fm = {'ordem': ordem, 'secoes': dict(F2['secoes'])}
    for k in alvo:
        f = copy.deepcopy(F2['secoes'][k]); pac, bu, c1 = _bu_c1(f)
        c1['votos']['1:22'] -= 3; c1['votos']['1:13'] = c1['votos'].get('1:13', 0) + 3
        if bu.get('A') and bu['A'].get('pres'):
            cand = bu['A']['pres']['cand']; cand['22'] = cand.get('22', 0) - 3; cand['13'] = cand.get('13', 0) + 3
        Fm['secoes'][k] = f
    res = conferir_conjunto(Fm, bw2, 2, bw1, F1)
    ap = {r['k'] for r in res if 'I1' in r['I'] and 'I1' not in base[r['k']]['I']}
    cal['P5_boletim_3_votos_em_30'] = {'plantadas': 30, 'apontadas_por_I1': len(ap & alvo), 'fora_do_plantio': len(ap - alvo), 'exato': ap == alvo,
                                       'tambem_apontadas_por_a': len(novos(res, 'A', 'a') & alvo)}
    # P6: 5 a mais no comparecimento e nos votos do 13, só no boletim
    g = rng(SEMENTE + 6)
    elig = [k for k in ordem if _bu_c1(F2['secoes'][k])[2] is not None and escolhe_pacote(F2['secoes'][k]).get('log')]
    alvo = set(g.sample(elig, 30)); Fm = {'ordem': ordem, 'secoes': dict(F2['secoes'])}
    for k in alvo:
        f = copy.deepcopy(F2['secoes'][k]); pac, bu, c1 = _bu_c1(f)
        bu['B']['comp'] += 5; c1['comp'] += 5; c1['votos']['1:13'] = c1['votos'].get('1:13', 0) + 5
        Fm['secoes'][k] = f
    res = conferir_conjunto(Fm, bw2, 2, bw1, F1)
    ap2 = {r['k'] for r in res if 'I2' in r['I'] and 'I2' not in base[r['k']]['I']}
    ap3 = {r['k'] for r in res if 'I3' in r['I'] and 'I3' not in base[r['k']]['I']}
    cal['P6_comparecimento_mais_5_em_30'] = {'plantadas': 30, 'apontadas_por_I2': len(ap2 & alvo), 'apontadas_por_I3': len(ap3 & alvo),
                                             'fora_do_plantio': len((ap2 | ap3) - alvo), 'exato': ap2 == alvo and ap3 == alvo}
    # P7: encerramento do boletim 10 minutos mais tarde
    g = rng(SEMENTE + 7)
    elig = [k for k in elig if _bu_c1(F2['secoes'][k])[1]['B'].get('enc')]
    alvo = set(g.sample(elig, 30)); Fm = {'ordem': ordem, 'secoes': dict(F2['secoes'])}
    for k in alvo:
        f = copy.deepcopy(F2['secoes'][k]); pac, bu, c1 = _bu_c1(f)
        bu['B']['enc'] = je(t_je(bu['B']['enc']) + 600)
        Fm['secoes'][k] = f
    res = conferir_conjunto(Fm, bw2, 2, bw1, F1)
    ap = {r['k'] for r in res if 'ii' in (r['I'].get('I7') or {}) and 'ii' not in (base[r['k']]['I'].get('I7') or {})}
    cal['P7_encerramento_mais_10min_em_30'] = {'plantadas': 30, 'apontadas_por_I7': len(ap & alvo), 'fora_do_plantio': len(ap - alvo), 'exato': ap == alvo}
    # P8 e E1: ordem do RDV
    def rdv_c1(f):
        pac = escolhe_pacote(f); rd = pac.get('rdv') if pac else None
        if not rd:
            return None
        for ck, reg in rd['cargos'].items():
            if ck.endswith('|c1') and reg.get('seq'):
                return reg
        return None
    elig = [k for k in ordem if rdv_c1(F2['secoes'][k]) and base[k]['inf'].get('I11') and base[k]['inf']['I11']['z13'] is not None]
    for nome, sem, fn in (('P8_rdv_ordenado_em_30', 8, 'ordena'), ('E1_rdv_reembaralhado_em_30', 11, 'embaralha')):
        g = rng(SEMENTE + sem)
        alvo = set(g.sample(elig, 30)); Fm = {'ordem': ordem, 'secoes': dict(F2['secoes'])}
        for k in alvo:
            f = copy.deepcopy(F2['secoes'][k]); reg = rdv_c1(f); toks = reg['seq'].split(',')
            if fn == 'ordena':
                toks.sort()
            else:
                g.shuffle(toks)
            reg['seq'] = ','.join(toks); Fm['secoes'][k] = f
        res = conferir_conjunto(Fm, bw2, 2, bw1, F1)
        zs = [r['inf']['I11']['z13'] for r in res if r['k'] in alvo]
        st = stats_I11(res, 'z13'); st0 = stats_I11(res_obs, 'z13')
        cal[nome] = {'plantadas': 30, 'com_abs_z_maior_4': sum(1 for z in zs if abs(z) > 4), 'com_abs_z_maior_3': sum(1 for z in zs if abs(z) > 3),
                     'z_mediano_das_plantadas': sorted(zs)[15], 'Z_agregado_com_plantio': st['Z'], 'Z_agregado_observado': st0['Z'],
                     'deslocamento_de_Z': st['Z'] - st0['Z'], 'fracao_abs_z_maior_3_com_plantio': st['fracao_abs_z_maior_3']}
    # placebo sintético de I11: reembaralhar TODAS as seções (o que o acaso dá)
    g = rng(SEMENTE + 12); zs = []
    for k in elig:
        toks = rdv_c1(F2['secoes'][k])['seq'].split(','); g.shuffle(toks)
        z = z_runs(toks, '13')
        if z:
            zs.append(z[0])
    cal['I11_todas_reembaralhadas'] = {'m': len(zs), 'Z': sum(zs) / math.sqrt(len(zs)), 'fracao_abs_z_maior_3': sum(1 for z in zs if abs(z) > 3) / len(zs)}
    # E2: relógio da urna 1 hora adiantado (boletim, log e vsc), 30 seções
    g = rng(SEMENTE + 13)
    elig2 = [k for k in ordem if escolhe_pacote(F2['secoes'][k]) and escolhe_pacote(F2['secoes'][k]).get('log') and escolhe_pacote(F2['secoes'][k]).get('vsc')
             and _bu_c1(F2['secoes'][k])[1]['B'].get('enc') and not base[k]['I'].get('I7') and not base[k]['I'].get('I8')]
    alvo = set(g.sample(elig2, 30)); Fm = {'ordem': ordem, 'secoes': dict(F2['secoes'])}
    for k in alvo:
        f = copy.deepcopy(F2['secoes'][k]); pac, bu, c1 = _bu_c1(f)
        for c in ('ab', 'enc', 'emissao'):
            bu['B'][c] = je(t_je(bu['B'][c]) + 3600)
        pac['vsc']['hw_quando'] = je(t_je(pac['vsc']['hw_quando']) + 3600)
        for B in pac['log']:
            D = B['dias'].get(DIA[2])
            if not D:
                continue
            for c in ('pronta', 'encconf', 'inienc', 'geralog', 'assini', 'assfim'):
                D[c] = [t + 3600 for t in D[c]]
            D['gerabu'] = [[t + 3600, u] for t, u in D['gerabu']]
            D['ult_t'] = D['ult_t'] + 3600 if D['ult_t'] is not None else None
        Fm['secoes'][k] = f
    res = conferir_conjunto(Fm, bw2, 2, bw1, F1, so=sorted(alvo))
    cal['E2_relogio_1h_adiantado_em_30'] = {'plantadas': 30, 'apontadas_por_I7': sum(1 for r in res if r['I'].get('I7')),
                                            'apontadas_por_I8_ii': sum(1 for r in res if 'ii' in (r['I'].get('I8') or {})),
                                            'apontadas_por_g': sum(1 for r in res if r['B'].get('g')),
                                            'nota': 'relógio errado desloca boletim, log e vsc por igual: I7 não acusa. (g) acusa aqui só porque o plantio não mexe no bweb; numa urna de relógio errado o bweb traria o mesmo horário do boletim. I8 (ii) só acusaria quem transmitiu a menos de 1h02 da assinatura'}
    # P2: 1 byte trocado no bu.dat de 10 seções (arquivos de verdade, em cópia)
    _init_pool()
    dest = os.path.join(W, 'plantio')
    if os.path.isdir(dest):
        shutil.rmtree(dest)
    g = rng(SEMENTE + 2)
    alvo = g.sample([k for k in ordem if not base[k]['A'] and 'bu' in escolhe_pacote(F2['secoes'][k])['arq']], 10)
    det = []
    for k in alvo:
        d = _copia_secao(k, pasta2, os.path.join(dest, 'P2'))
        pac = escolhe_pacote(F2['secoes'][k]); nm = f"{pac['i']}-{pac['arq']['bu']['nome']}"
        b = bytearray(open(os.path.join(d, nm), 'rb').read()); pos = g.randrange(len(b)); b[pos] ^= 0x01
        open(os.path.join(d, nm), 'wb').write(bytes(b))
        r = conferir(ler_secao((k, d, 2)), bw2.get(k), 2, fuso_de(k), bw1.get(k), F1['secoes'].get(k) if F1 else None)
        det.append({'secao': k, 'byte': pos, 'b': 'b_bu' in r['A'], 'c': 'c_bu' in r['A'], 'a': 'a' in r['A'] or 'a_comp' in r['A'],
                    'boletim_ilegivel': bool(r['lado'].get('boletim_ilegivel')), 'outras': sorted(set(r['A']) - {'b_bu', 'c_bu'})})
    cal['P2_um_byte_no_boletim_em_10'] = {'plantadas': 10, 'apontadas_por_b': sum(x['b'] for x in det), 'apontadas_por_c': sum(x['c'] for x in det),
                                          'tambem_por_a_ou_ilegivel': sum(1 for x in det if x['a'] or x['boletim_ilegivel']), 'detalhe': det}
    # P3: vota.vsc trocado entre 5 pares de seções
    g = rng(SEMENTE + 3)
    alvo = g.sample([k for k in ordem if not base[k]['A'] and 'vsc' in escolhe_pacote(F2['secoes'][k])['arq']], 10)
    det = []
    for a, b_ in zip(alvo[::2], alvo[1::2]):
        da = _copia_secao(a, pasta2, os.path.join(dest, 'P3')); db = _copia_secao(b_, pasta2, os.path.join(dest, 'P3'))
        pa = escolhe_pacote(F2['secoes'][a]); pb = escolhe_pacote(F2['secoes'][b_])
        na = os.path.join(da, f"{pa['i']}-{pa['arq']['vsc']['nome']}"); nb = os.path.join(db, f"{pb['i']}-{pb['arq']['vsc']['nome']}")
        xa = open(na, 'rb').read(); xb = open(nb, 'rb').read()
        open(na, 'wb').write(xb); open(nb, 'wb').write(xa)
        for k, d in ((a, da), (b_, db)):
            r = conferir(ler_secao((k, d, 2)), bw2.get(k), 2, fuso_de(k), bw1.get(k), F1['secoes'].get(k) if F1 else None)
            det.append({'secao': k, 'e': 'e' in r['A'], 'd': 'd2' in r['A'] or 'd1' in r['A'], 'b': 'b_bu' in r['A'], 'c': 'c_bu' in r['A'],
                        'I4': 'I4' in r['I'], 'todas': sorted(r['A'])})
    cal['P3_vsc_trocado_em_5_pares'] = {'plantadas': 10, 'apontadas_por_e': sum(x['e'] for x in det), 'apontadas_por_d': sum(x['d'] for x in det),
                                        'apontadas_por_b': sum(x['b'] for x in det), 'apontadas_por_I4': sum(x['I4'] for x in det), 'detalhe': det}
    shutil.rmtree(dest, ignore_errors=True)
    # P4: cobertura da amostra contra 5.857 seções alteradas
    import numpy as np
    U = universo(); pos = {k: i for i, k in enumerate(U['chaves'])}
    na_amostra = np.zeros(U['n'], bool)
    for k in ordem:
        na_amostra[pos[k]] = True
    comps = np.array(U['comps'])
    maiores = np.argsort(-comps, kind='stable')[:5857]
    r = np.random.default_rng(SEMENTE + 4); cont = 0; menor = 10 ** 9
    for _ in range(10000):
        idx = r.choice(U['n'], 5857, replace=False)
        c = int(na_amostra[idx].sum()); cont += c > 0; menor = min(menor, c)
    cal['P4_cobertura'] = {'sorteios_ao_acaso': 10000, 'sorteios_em_que_a_amostra_contem_alguma': cont, 'menor_numero_de_secoes_apanhadas': menor,
                           'esperado_por_sorteio': 5857 * len(ordem) / U['n'], 'secoes_da_amostra_entre_as_5857_maiores': int(na_amostra[maiores].sum()),
                           'probabilidade_teorica_de_nenhuma': math.exp(sum(math.log((U['n'] - len(ordem) - i) / (U['n'] - i)) for i in range(5857)))}
    return cal


# ---------------------------------------------------------------------------------------------------------------------
# D3-2, parte dos aux.json
# ---------------------------------------------------------------------------------------------------------------------
def _aux_resumo(cam):
    try:
        a = json.loads(open(cam, 'rb').read().decode('utf-8'))
    except Exception:  # noqa: BLE001
        return None
    return {'st': a.get('st'), 'dg': a.get('dg'), 'hg': a.get('hg'), 'idg': a.get('idg'), 'f': a.get('f'),
            'hashes': [{'hash': h.get('hash'), 'dr': h.get('dr'), 'hr': h.get('hr'), 'st': h.get('st'),
                        'arq': sorted((x.get('nm'), x.get('tp')) for x in h.get('arq', []))} for h in a.get('hashes', [])]}


def aux_estabilidade():
    """aux.json de hoje contra o baixado em 26/10 (amostra antiga, 2º turno) e contra o das 80 seções do 1º turno."""
    out = {}
    for nome, antiga, hoje in (('2t', ANTIGA, f'{W}/aux_hoje/2t'), ('1t', ANTIGA1, f'{W}/aux_hoje/1t')):
        c = collections.Counter(); mudou = []; datas0 = collections.Counter(); datas1 = collections.Counter(); mt = []
        for d in sorted(glob.glob(os.path.join(antiga, '*/*/*/*/'))):
            uf, m, z, s = d.rstrip('/').split('/')[-4:]
            k = f'{uf.upper()}|{int(m)}|{int(z)}|{int(s)}'
            a0 = _aux_resumo(os.path.join(d, 'aux.json'))
            dh = pasta_secao(hoje, k)
            if a0 is None:
                c['sem_aux_antigo'] += 1; continue
            c['com_aux_antigo'] += 1
            if os.path.exists(os.path.join(dh, 'SEM_AUX')):
                c['hoje_sem_aux_no_site'] += 1; mudou.append({'secao': k, 'mudou': ['aux.json sumiu do site']}); continue
            a1 = _aux_resumo(os.path.join(dh, 'aux.json'))
            if a1 is None:
                c['hoje_nao_baixado'] += 1; continue
            c['comparadas'] += 1
            datas0[a0['dg']] += 1; datas1[a1['dg']] += 1
            mt.append(os.path.getmtime(os.path.join(d, 'aux.json')))
            dif = []
            h0 = [h['hash'] for h in a0['hashes']]; h1 = [h['hash'] for h in a1['hashes']]
            if h0 != h1:
                dif.append('hash')
            if [(h['dr'], h['hr']) for h in a0['hashes']] != [(h['dr'], h['hr']) for h in a1['hashes']]:
                dif.append('recebimento')
            if a0['st'] != a1['st'] or [h['st'] for h in a0['hashes']] != [h['st'] for h in a1['hashes']]:
                dif.append('estado')
            if [h['arq'] for h in a0['hashes']] != [h['arq'] for h in a1['hashes']]:
                dif.append('lista de arquivos')
            if (a0['dg'], a0['hg'], a0['idg']) != (a1['dg'], a1['hg'], a1['idg']):
                dif.append('indice regerado')
            if a0['f'] != a1['f']:
                dif.append('campo f')
            for x in dif:
                c['mudou: ' + x] += 1
            if not dif:
                c['iguais em tudo'] += 1
            if set(dif) - {'indice regerado'}:
                mudou.append({'secao': k, 'mudou': dif, 'antes': a0, 'hoje': a1})
        out[nome] = {'contagem': dict(c), 'data_de_geracao_antes': dict(datas0), 'data_de_geracao_hoje': dict(datas1),
                     'baixado_antes_entre': [time.strftime('%Y-%m-%d %H:%M', time.gmtime(min(mt))), time.strftime('%Y-%m-%d %H:%M', time.gmtime(max(mt)))] if mt else None,
                     'casos_com_mudanca_alem_da_data': mudou}
    out['download'] = le('download_aux_hoje.json')
    return out


def sobreposicao(F2, Fant):
    """Seções que estão na amostra nova e na antiga: mesmos arquivos nos dois downloads (26/10 e 10/11)?"""
    com = [k for k in F2['ordem'] if k in Fant['secoes']]
    out = {'secoes_em_comum': len(com), 'arquivos_comparados': 0, 'iguais': 0, 'diferentes': []}
    for k in com:
        p2 = escolhe_pacote(F2['secoes'][k]); pa = escolhe_pacote(Fant['secoes'][k])
        if not p2 or not pa:
            continue
        for t in ('bu', 'rdv', 'log', 'vsc'):
            if t in p2['arq'] and t in pa['arq']:
                out['arquivos_comparados'] += 1
                if p2['arq'][t]['sha512'] == pa['arq'][t]['sha512']:
                    out['iguais'] += 1
                else:
                    out['diferentes'].append([k, t])
        if p2.get('hash') != pa.get('hash'):
            out['diferentes'].append([k, 'hash do aux.json'])
    return out


# ---------------------------------------------------------------------------------------------------------------------
# Rodada
# ---------------------------------------------------------------------------------------------------------------------
def modo_rodar(so_obs=False):
    t0 = time.time()
    bw1 = le('bweb_1t.json.gz')['secoes']; bw2 = le('bweb_2t.json.gz')['secoes']
    F = {}
    for c in CONJ:
        x = le(f'fatos_{c}.json.gz')
        if x is not None:
            F[c] = x
    diz('conjuntos lidos:', {c: F[c]['n'] for c in F})
    R = {'teste': 'R27_DA', 'registro': 'Adendo 27 (commit 2748895), onda D-a; desenho D3 (D3-1, D3-3 e a parte dos aux.json do D3-2); mantido pelo Adendo 30 (commit a7218fb)',
         'rodado_em': time.strftime('%Y-%m-%d %H:%M:%S UTC', time.gmtime()), 'universo': N_U, 'margem': MARGEM}
    RES = {}
    pares = {'p2': (bw2, 2, bw1, F.get('p1')), 'p1': (bw1, 1, None, None), 'pp': (bw2, 2, bw1, None), 'c1': (bw2, 2, bw1, None),
             'ant': (bw2, 2, bw1, None), 'e2': (bw2, 2, bw1, F.get('e1')), 'e1': (bw1, 1, None, None)}
    R['conjuntos'] = {}; R['casos'] = {}
    for c in F:
        bw, turno, b1, f1 = pares[c]
        RES[c] = conferir_conjunto(F[c], bw, turno, b1, f1)
        S, casos = resumir(c, RES[c], turno, CONJ[c]['pasta'])
        S['lido_em'] = F[c].get('lido_em'); S['pasta'] = CONJ[c]['pasta']
        S['erros_de_leitura'] = [[k, f['erros']] for k, f in F[c]['secoes'].items() if f['erros']][:50]
        S['n_erros_de_leitura'] = sum(1 for f in F[c]['secoes'].values() if f['erros'])
        R['conjuntos'][c] = S; R['casos'][c] = casos
        grava(f'parcial_res_{c}.json.gz', RES[c], gz=True)
        diz(c, 'n', S['n'], 'X classe A', S['X_classe_A'], 'B', S['secoes_com_classe_B'], 'sem arquivo', len(S['sem_arquivo']),
            {j: v['violam'] for j, v in S['identidades'].items() if v['violam']})
    grava('parcial_observado.json', R)
    if so_obs:
        return R
    # alcance (D3-1)
    S2 = R['conjuntos']['p2']
    R['alcance'] = {'principal': alcance(S2['X_classe_A'], S2['n'], len(S2['sem_arquivo'])),
                    'referencia_do_desenho_n3000_x0': alcance(0, 3000)}
    r8 = [r for r in RES['p2'] if r['k'].split('|')[0] in UFS8]
    U = universo()
    c8 = sorted((c for k, c in zip(U['chaves'], U['comps']) if k.split('|')[0] in UFS8), reverse=True)
    lo8, hi8 = cp(sum(1 for r in r8 if r['A']), len(r8))
    K8 = math.ceil(len(c8) * hi8 - 1e-9)
    R['alcance']['oito_UFs_de_publicacao_em_lote'] = {'ufs': list(UFS8), 'x': sum(1 for r in r8 if r['A']), 'n': len(r8), 'limite_superior': hi8,
                                                      'secoes_nessas_UFs': len(c8), 'teto_de_secoes_nessas_UFs': K8, 'dano_maximo_nessas_UFs': 2 * sum(c8[:K8]),
                                                      'fracao_da_margem': 2 * sum(c8[:K8]) / MARGEM,
                                                      'classe_B': sum(1 for r in r8 if r['B']), 'identidades': sum(1 for r in r8 if r['I'])}
    for c in ('pp', 'c1'):
        if c in RES:
            S = R['conjuntos'][c]
            lo, hi = cp(S['X_classe_A'], S['n'])
            R['alcance'][c] = {'x': S['X_classe_A'], 'n': S['n'], 'limite_superior_na_lista': hi}
    # ordem do sorteio conferida
    ordem = F['p2']['ordem']
    R['amostra'] = {'sha256_da_lista': hashlib.sha256(open(os.path.join(REG, 'amostra_aas_principal.txt'), 'rb').read()).hexdigest(),
                    'n': len(ordem), 'por_UF': dict(collections.Counter(k.split('|')[0] for k in ordem)),
                    'comparecimento_medio': sum(r['inf'].get('comp') or 0 for r in RES['p2']) / len(ordem),
                    'todas_no_bweb': all(k in bw2 for k in ordem)}
    # (d3) entre conjuntos e entre turnos
    porchave = collections.defaultdict(set); porurna = collections.defaultdict(set)
    for c in ('p2', 'pp', 'ant'):
        for r in RES.get(c, []):
            if r['inf'].get('chave'):
                porchave[r['inf']['chave']].add(r['k']); porurna[r['inf']['cert_cn'].lower()].add(r['inf']['chave'])
    d3 = {'secoes_distintas_2t_com_chave': len({k for v in porchave.values() for k in v}), 'chaves_distintas': len(porchave),
          'chave_em_mais_de_uma_secao': [sorted(v) for v in porchave.values() if len(v) > 1],
          'urna_com_mais_de_uma_chave': [u for u, v in porurna.items() if len(v) > 1]}
    if 'p1' in RES:
        k1 = {r['k']: r['inf'] for r in RES['p1'] if r['inf'].get('chave')}
        mesma_urna = mesma_urna_chave_dif = urna_dif = urna_dif_chave_igual = 0
        for r in RES['p2']:
            i2 = r['inf']; i1 = k1.get(r['k'])
            if not i1 or not i2.get('chave'):
                continue
            if i1['cert_cn'].lower() == i2['cert_cn'].lower():
                mesma_urna += 1; mesma_urna_chave_dif += i1['chave'] != i2['chave']
            else:
                urna_dif += 1; urna_dif_chave_igual += i1['chave'] == i2['chave']
        d3['entre_turnos'] = {'mesma_urna_no_certificado': mesma_urna, 'mesma_urna_com_chave_diferente': mesma_urna_chave_dif,
                              'urna_diferente': urna_dif, 'urna_diferente_com_a_mesma_chave': urna_dif_chave_igual}
        ch1 = collections.defaultdict(set)
        for k, i1 in k1.items():
            ch1[i1['chave']].add(k)
        d3['chave_em_mais_de_uma_secao_no_1t'] = [sorted(v) for v in ch1.values() if len(v) > 1]
    R['d3_chaves'] = d3
    # D3-2 aux
    R['aux_estabilidade'] = aux_estabilidade()
    if 'ant' in F:
        R['sobreposicao_nova_antiga'] = sobreposicao(F['p2'], F['ant'])
    grava('parcial_observado.json', R)
    # calibração
    diz('calibrando')
    R['calibracao'] = calibrar(F['p2'], bw2, bw1, F.get('p1'), RES['p2'], CONJ['p2']['pasta'])
    grava('parcial_calibracao.json', R['calibracao'])
    R['vereditos'] = vereditos(R)
    diz('exploratorio')
    R['exploratorio'] = exploratorio(F, RES)
    grava('parcial_tudo.json', R)
    diz('fim da rodada', round(time.time() - t0), 's')
    return R


# ---------------------------------------------------------------------------------------------------------------------
# EXPLORATÓRIO (decidido depois de ver os resultados; não muda veredito)
# ---------------------------------------------------------------------------------------------------------------------
def _log_da_secao(pasta, k):
    fs = sorted(glob.glob(os.path.join(pasta_secao(pasta, k), '*-log*.jez')))
    return fs[-1] if fs else None


def detalhe_I3(pasta, k, dia):
    """Confirmações de voto para presidente sem a linha de voto computado depois, com o que o log registra em seguida."""
    f = _log_da_secao(pasta, k); out = []
    if not f:
        return out
    marcas = ('Urna desligada', 'Urna ligada em', 'reinício da votação', 'Início das operações do logd', 'carga crítica', 'Votação suspensa', 'Desligando')
    for linhas in _linhas_log(f):
        L = [l.split('\t') for l in linhas]; pend = None

        def desc(a, b):
            return {'linha': a, 'linhas_seguintes': [' | '.join(x[:5])[:130] for x in L[a:a + 5]],
                    'eventos_ate_o_proximo_voto': [x[0][11:] + ' ' + x[4][:60] for x in L[a:b] if len(x) > 4 and any(y in x[4] for y in marcas)][:8]}
        for i, p in enumerate(L):
            if len(p) < 5 or not p[0].startswith(dia):
                continue
            m = p[4]
            if m.startswith('Voto confirmado para [Presidente]') or m.startswith('Atribuido voto nulo por suspensão [Presidente]'):
                if pend is not None:
                    out.append(desc(pend, i))
                pend = i
            elif m == 'O voto do eleitor foi computado':
                pend = None
        if pend is not None:
            out.append(desc(pend, len(L)))
    return out


def detalhe_I10(pasta, k):
    f = _log_da_secao(pasta, k); c = collections.Counter(); fuso = 0
    if not f:
        return {}
    for linhas in _linhas_log(f):
        L = [l.split('\t') for l in linhas]; prev = None
        fuso += sum(1 for x in L if len(x) > 4 and 'por ajuste de fuso horário' in x[4])
        tem_fuso = any(len(x) > 4 and 'por ajuste de fuso horário' in x[4] for x in L)
        for i, p in enumerate(L):
            if len(p) < 5:
                continue
            t = t_log(p[0])
            if t is None:
                continue
            if prev is not None and t < prev:
                jan = [x[4] for x in L[max(0, i - 12):i + 1] if len(x) > 4]
                if any(m.startswith(AJUSTE) for m in jan):
                    c['ajuste da carga (lista fixada antes)'] += 1
                elif any(m.startswith('Data e hora da urna alterada') for m in jan):
                    c['linha "Data e hora da urna alterada ... por ajuste de fuso horário" na janela'] += 1
                elif p[4].startswith('Início das operações do logd') and tem_fuso:
                    c['partida da urna com o relógio de antes do ajuste de fuso'] += 1
                else:
                    c['outro'] += 1
            prev = t
    return {'passos': dict(c), 'linhas_de_ajuste_de_fuso': fuso}


def exploratorio(F, RES):
    X = {}

    def agrup(Fc, cargo):
        tot = ok = 0; ordens = collections.Counter()
        for k in Fc['ordem']:
            p = escolhe_pacote(Fc['secoes'][k]); rd = p.get('rdv') if p else None
            if not rd:
                continue
            for ck, reg in rd['cargos'].items():
                if ck.endswith('|' + cargo) and reg.get('seq'):
                    toks = reg['seq'].split(','); runs = [toks[0]] + [t for a, t in zip(toks, toks[1:]) if t != a]
                    tot += 1; g = len(runs) == len(set(toks)); ok += g
                    nums = [int(t) for t in runs if t.isdigit()]
                    cres = nums == sorted(nums) and all(not t.isdigit() for t in runs[len(nums):]) and runs[len(nums):] in ([], ['B'], ['N'], ['B', 'N'])
                    ordens['números em ordem crescente, depois branco, depois nulo' if (g and cres) else 'outra'] += 1
        return {'rdv': tot, 'agrupados_por_votavel': ok, 'ordem': dict(ordens)}
    X['X1_rdv_publicado_vem_agrupado'] = {c: {'presidente': agrup(F[c], 'c1'), 'governador': agrup(F[c], 'c3')} for c in F}
    x2 = {}
    for c in RES:
        if CONJ[c]['turno'] != 2 or c == 'c1':
            continue
        for r in RES[c]:
            if 'I3' in r['I'] and not r['inf'].get('explica'):
                x2[f"{c}:{r['k']}"] = {'I3': r['I']['I3'], 'I2_fecha': 'I2' not in r['I'], 'I1_fecha': 'I1' not in r['I'],
                                       'detalhe': detalhe_I3(CONJ[c]['pasta'], r['k'], DIA[2])}
    X['X2_I3_confirmacao_sem_voto_computado'] = x2
    x3 = {}
    for c in RES:
        if CONJ[c]['turno'] != 2 or c == 'c1':
            continue
        for r in RES[c]:
            if 'I10' in r['I']:
                x3[f"{c}:{r['k']}"] = detalhe_I10(CONJ[c]['pasta'], r['k'])
    X['X3_I10_passos_para_tras'] = {'por_secao': x3, 'secoes': len(x3), 'no_exterior': sum(1 for a in x3 if ':ZZ|' in a),
                                    'com_passo_do_tipo_outro': sorted(a for a, v in x3.items() if v.get('passos', {}).get('outro'))}
    for c in ('p2', 'p1', 'pp', 'ant'):
        if c not in RES:
            continue
        cl = collections.Counter()
        for r in RES[c]:
            g = (r['B'].get('g') or {}).get('recebimento')
            st = r['inf'].get('pacote_st')
            if not g:
                cl[f'{st}: igual'] += 1 if 'aux' in r['inf'] else 0
            else:
                d = g['dif_s']
                cl[f"{st}: " + ('sem hora' if d is None else 'aux antes do bweb' if d < 0 else '1 s' if d == 1 else '2 a 9 s' if d < 10 else '10 s a 1 h' if d <= 3600 else 'mais de 1 h')] += 1
        X.setdefault('X4_hora_de_recebimento_aux_menos_bweb', {})[c] = dict(cl)
    if 'p2' in RES:
        Fp = F['p2']; multi = 0; multi_i3 = 0
        for r in RES['p2']:
            p = escolhe_pacote(Fp['secoes'][r['k']]); lg = p.get('log') if p else None
            if not lg:
                continue
            npr = sum(len(B['dias'][DIA[2]]['pronta']) for B in lg if DIA[2] in B['dias'])
            if npr > 1:
                multi += 1; multi_i3 += 'I3' in r['I']
        X['X5_reinicio_da_votacao_no_dia'] = {'secoes_com_mais_de_uma_urna_pronta_no_dia': multi, 'delas_com_I3': multi_i3}
        rec = []
        for r in RES['p2']:
            if r['inf'].get('pacote_st') != 'Totalizado':
                p = escolhe_pacote(Fp['secoes'][r['k']]); b = p['bu']['B']
                rec.append({'secao': r['k'], 'estado': p['st'], 'recebido_no_site': f"{p['dr']} {p['hr']}", 'indice_gerado': f"{r['inf']['aux']['dg']} {r['inf']['aux']['hg']}",
                            'emissao_do_boletim': b['emissao'], 'carimbo_do_vsc': p['vsc']['hw_quando'], 'tipos_listados': sorted(t for _, t in p['listados']),
                            'classe_A': sorted(r['A']), 'identidades': sorted(r['I']), 'comparecimento': b['comp']})
        X['X6_pacotes_em_estado_Recebido'] = rec
    if 'p2' in RES:
        # X7: o que os boletins assinados da amostra dizem do país (N x média amostral, com correção de população finita)
        Fp = F['p2']; L = []; Rr = []; C = []
        for k in Fp['ordem']:
            p = escolhe_pacote(Fp['secoes'][k]); v, comp, apt, ide = votos_bu_B(p['bu']['B'])
            L.append(v.get(13, 0)); Rr.append(v.get(22, 0)); C.append(comp)
        n = len(L)

        def est(x):
            m = sum(x) / n; var = sum((a - m) ** 2 for a in x) / (n - 1)
            return {'estimativa': N_U * m, 'ep': N_U * math.sqrt(var / n * (1 - n / N_U))}
        D = [a - b for a, b in zip(L, Rr)]
        X['X7_pais_estimado_pelos_boletins_assinados_da_amostra'] = {
            'votos_conferidos_um_a_um': sum(C), 'lula': est(L), 'flavio': est(Rr), 'margem': est(D), 'comparecimento': est(C),
            'oficial': {'lula': 64256232, 'flavio': 59826041, 'margem': MARGEM, 'comparecimento': 128236074},
            'soma_na_amostra': {'lula': sum(L), 'flavio': sum(Rr)}}
    return X


# ---------------------------------------------------------------------------------------------------------------------
# Vereditos pela letra
# ---------------------------------------------------------------------------------------------------------------------
def vereditos(R):
    S = R['conjuntos']['p2']; S1 = R['conjuntos'].get('p1'); cal = R['calibracao']; n = S['n']
    V = {}
    poder1 = (cal['P1_bweb_5_votos_em_30']['exato'] and cal['P2_um_byte_no_boletim_em_10']['apontadas_por_b'] == 10
              and cal['P2_um_byte_no_boletim_em_10']['apontadas_por_c'] == 10 and cal['P3_vsc_trocado_em_5_pares']['apontadas_por_e'] == 10
              and cal['P3_vsc_trocado_em_5_pares']['apontadas_por_d'] == 10 and cal['P4_cobertura']['sorteios_em_que_a_amostra_contem_alguma'] == 10000)
    X = S['X_classe_A']; m = len(S['sem_arquivo']); nb = S['secoes_com_classe_B']; nv = S['assinatura_nao_verificavel']
    if not poder1:
        v = 'SEM PODER'
    elif X >= 1:
        ef = S['efeito_a']
        v = 'SINAL' + (' COM ALCANCE' if ef['nacional'] - 1.96 * ef['ep_nacional'] > 0.1 * MARGEM else ' LOCAL')
    elif m >= 8 or nv / n > 0.005 or nb > 0:
        v = 'INCONCLUSIVO'
    elif n == 3000 and m <= 7:
        v = 'SEM SINAL'
    else:
        v = 'INCONCLUSIVO'
    V['D3-1'] = {'veredito': v, 'poder': poder1, 'X_classe_A': X, 'sem_arquivo': m, 'secoes_com_classe_B': nb, 'assinatura_nao_verificavel': nv,
                 'motivo': ('zero quebra de classe A; ' + (f'{nb} seções só com quebra de classe B (hora de recebimento)' if nb else 'nenhuma de classe B')) if X == 0 else f'{X} seções com quebra de classe A'}
    I = S['identidades']
    poder3 = (cal['P5_boletim_3_votos_em_30']['exato'] and cal['P6_comparecimento_mais_5_em_30']['exato'] and cal['P7_encerramento_mais_10min_em_30']['exato'])
    poder11 = abs(cal['P8_rdv_ordenado_em_30']['deslocamento_de_Z']) > 4
    Z2 = S['I11_13']['Z']; Z1 = S1['I11_13']['Z'] if S1 else None
    s_a = sum(I[j]['sem_explicacao'] for j in ('I1', 'I2', 'I3'))
    s_b = sum(I[j]['violam'] for j in ('I4', 'I5', 'I6')); s_b_sem = sum(I[j]['sem_explicacao'] for j in ('I4', 'I5', 'I6'))
    s_c = S['violam_I7_ou_I8'] / n >= 0.005
    s_d = Z1 is not None and abs(Z2) > 4 and abs(Z1) < 3
    igual = Z1 is not None and (Z2 * Z1 > 0) and abs(Z2 - Z1) / math.sqrt(2) < 3
    sem = (sum(I[j]['violam'] for j in ('I1', 'I2', 'I3', 'I4', 'I5', 'I6', 'I9')) == 0 and S['violam_horario_sem_explicacao'] / n < 0.005
           and (abs(Z2) < 3 or igual))
    V['D3-3'] = {'poder_I1_I2_I3_I7': poder3, 'poder_I11': poder11, 'I1_I2_I3_sem_explicacao': s_a, 'I4_I5_I6_violam': s_b, 'I4_I5_I6_sem_explicacao': s_b_sem,
                 'I7_ou_I8': S['violam_I7_ou_I8'], 'limiar_I7_I8': math.ceil(0.005 * n), 'horario_sem_explicacao_I7_I8_I10': S['violam_horario_sem_explicacao'],
                 'I11_Z_2t': Z2, 'I11_Z_1t': Z1, 'I11_igual_nos_dois_turnos_pela_definicao_do_docstring': igual,
                 'I11_dif_sobre_raiz2': abs(Z2 - Z1) / math.sqrt(2) if Z1 is not None else None,
                 'clausula_sinal_I1_I2_I3': s_a > 0, 'clausula_sinal_I4_I5_I6_pela_letra_estrita': s_b > 0, 'clausula_sinal_horarios': s_c,
                 'clausula_sinal_I11': s_d, 'clausula_sem_sinal_inteira': sem, 'rdv_ausente': S['rdv_ausente'],
                 'explicadas_por_contingencia_fracao': S['com_evento_que_explica'] / n}
    return V


if __name__ == '__main__':
    modo = sys.argv[1] if len(sys.argv) > 1 else ''
    if modo == 'baixar_c1':
        modo_baixar_c1()
    elif modo == 'baixar_aux':
        modo_baixar_aux()
    elif modo == 'ler':
        modo_ler(sys.argv[2], int(sys.argv[3]) if len(sys.argv) > 3 else None)
    elif modo == 'rodar':
        modo_rodar(so_obs=len(sys.argv) > 2 and sys.argv[2] == 'obs')
    else:
        print(__doc__)
