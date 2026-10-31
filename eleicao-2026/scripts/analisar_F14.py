"""F14 do pré-registro (Adendo 21, commit 913af7a, 31/10/2026 10:36:29 UTC): casos pendentes, arquivo por arquivo.

Letra do registro
  Boletim, RDV, log e assinatura de: as 37 seções com mais de 80% de liberação sem biometria nos dois turnos (F6),
  ES|56995|53|978 e as outras seções do local, as 17 seções da zona 90 de Volta Redonda mantidas abertas, AC|1554|3|160,
  AC|1040|4|160, AC|1066|4|313, RR|3026|6|97 e AM|2097|18|37 e 39; e o 1º turno de AM|2399|45|63 se o arquivo existir.
  Sinal: assinatura inválida, boletim diferente do bweb, RDV diferente do boletim, votos no log diferentes do
  comparecimento, ou anomalia A2 a A5. Descritivo: quem liberou (mesário identificado ou não), horário das liberações e
  contingências.
  A2 a A5 são as do T3 (cabeçalho do registro): A2 voto computado antes de "Urna pronta para receber votos" ou depois de
  "Inicio do Encerramento"; A3 voto computado sem "Eleitor foi habilitado" desde o voto anterior; A4 menos de 2 segundos
  entre "Eleitor foi habilitado" e "O voto do eleitor foi computado"; A5 rajada de 10 ou mais votos seguidos com menos
  de 15 segundos entre um e o seguinte.

Decisões que o registro não fixa (escritas aqui antes de baixar qualquer arquivo destas seções e antes de calcular
qualquer conferência; declaradas como desvio no resultado)
  D1. As 37 seções: a definição do modo exploratório do F6 (analisar_F6.modo_exploratorio), refeita aqui do zero:
      seções da base secoes2026.json.gz fora do exterior, com os dois turnos, com min(L1+R1, L2+R2, comp1, comp2) > 0;
      NH = QT_ELEI_BIOM_SEM_HABILITACAO das linhas do cargo 1 do bweb de cada turno (analisar_F6.ler_zip, a mesma leitura
      do F6); grupo = NH1/comp1 > 0,8 e NH2/comp2 > 0,8 (comparecimento da base). Conferência contra
      resultados/F6_sem_biometria.json (exploratorio.liberacao_alta.acima_de_80pct_nos_dois): número de seções,
      municípios e coeficiente da virada contra o local (mesma regressão do F6). Se não bater, a diferença é relatada e
      vale a lista refeita.
  D2. O local de ES|56995|53|978: UF|município|zona|NR_LOCAL_VOTACAO do 2º turno na base (lib.chave_local). Entram todas
      as seções da base com 2º turno nesse local.
  D3. Volta Redonda: o município é o de NM_MUNICIPIO "VOLTA REDONDA" no bweb do 2º turno do RJ. Fuso pela abertura
      modal do município (como no L1, L8 e F8): hora cheia mais comum de DT_ABERTURA nas seções do município no 2º turno
      sem junta (NR_JUNTA_APURADORA = -1); deslocamento = modal - 8; hora de Brasília = hora local - deslocamento.
      "Mantida aberta" = DT_ENCERRAMENTO em Brasília depois das 19:15:00 de 25/10/2026 (estritamente maior). Ao lado, a
      contagem com 19:16:00 ou depois. Se a regra não der 17 seções, isso é relatado e vale o que a regra der.
  D4. As seções nomeadas, como estão no registro. 1º turno de AM|2399|45|63: pleito 3220 (o código dos nomes
      o03220... na pasta arq1t da amostra).
  D5. Download: scripts/baixar_arquivos_urna.py, tipos bu,rdv,log,vota, TAXA=1.0. 2º turno (pleito 3221) para a pasta nova
      /home/user/trabalho-eleicao/adendo21/F14_arq; 1º turno (pleito 3220) para outra pasta nova, F14_arq1t. Uma seção
      que esteja em mais de um grupo é baixada uma vez e conferida uma vez, com todos os rótulos. Se o aux.json listar
      mais de um pacote, vale o de maior índice (o mais recente) e o caso é contado e relatado.
  D6. Boletim contra o bweb: para cada cargo majoritário que decodificar.ler_bu lê no boletim (presidente, e governador
      onde houve 2º turno de governador; no 1º turno de AM|2399|45|63, presidente e governador), o comparecimento do
      cargo, os votos por número de candidato, o branco e o nulo, mais o número da urna e os aptos, contra as linhas do
      mesmo cargo no zip bweb do turno, lidas aqui mesmo (CD_TIPO_VOTAVEL 1 nominal por NR_VOTAVEL, 2 branco, 3 nulo;
      outro tipo num cargo majoritário vira diferença). Senador no 1º turno: comparado só como descritivo (o
      decodificador não foi validado para as duas vagas). Ao lado, o presidente do boletim contra a base secoes2026.
  D7. RDV contra boletim: os mesmos cargos de D6, votos por número, branco e nulo (decodificar.rdv_para_bu: tipo 4 e o
      nulo sem dígitos, tipo 6, contam como nulo, como no boletim) contra o boletim.
  D8. Votos no log contra o comparecimento: decodificar.ler_log no dia da eleição (25/10/2026 no 2º turno, 04/10/2026 no
      1º), somando todos os logs do pacote (inclui o da urna original quando há contingência), contra o comparecimento
      do presidente no boletim (no bweb, se faltar o boletim).
  D9. A2 a A5: as contagens de ler_log no mesmo dia. Pela letra, qualquer contagem acima de zero é anomalia e entra no
      sinal. Cada ocorrência é descrita (se o log documenta contingência, reinício ou votação por cédula), sem mudar a
      contagem.
  D10. Assinatura: scripts/verificar_assinaturas.py em cada pasta baixada (saída guardada fora da pasta baixada). Uma
      seção tem assinatura inválida se aparecer na lista de falhas (qualquer tipo, como no F5) ou se o aux.json listar o
      vsc e ele não tiver vindo. Se o aux não listar vsc, a seção fica "sem arquivo" nesse item.
  D11. Veredito: SINAL se pelo menos uma seção (as do 2º turno e o 1º turno de AM|2399|45|63) tiver pelo menos um dos
      cinco itens. Senão, SEM SINAL. O registro só define o sinal; "sem sinal" aqui quer dizer que nenhum dos cinco itens
      aparece em nenhuma seção com arquivo. Arquivo que não vem fica "sem arquivo" no item (não conta como sinal, é
      relatado), como no F5.
  D12. Descritivo das liberações: a classe de cada "Eleitor foi habilitado" é a do F6 (analisar_F6.classificar): B
      biométrica, M liberada sem biometria (eleitor com biometria cadastrada; é o que o campo do bweb conta), S sem
      biometria cadastrada. "Quem liberou", para cada M, pela janela de mensagens da habilitação (regra do F6):
      mesário identificado ("Mesário N habilitou o eleitor"), digital nova (não bateu com nenhum arquivo, foi gravada em
      arquivo novo), digital gravada depois do registro inicial de mesário (o log diz que não dá para associar a um
      mesário), outro. Os títulos de eleitor dos mesários que aparecem no log não são gravados nas saídas: cada mesário
      vira uma letra (A, B, C...) na ordem da primeira liberação dele na seção. Horários: M por hora do relógio da urna,
      primeira e última M, M depois das 16h e das 17h locais, maior número de M em 30 minutos. Ao lado, M do log contra
      o NH do bweb em cada turno.
  D13. Contingências e eventos: por bloco de log do pacote (urna, primeiro e último evento do dia, habilitações, M,
      votos), as linhas com "ontingência", "Urna desligada pela chave", "inspeção", "Reinício"/"reiniciad", erros e o
      modo de carga (com D17, também "crítica", de bateria, e cada "Urna ligada em"). Ao lado, o dia do 1º turno na
      mesma urna, quando o log do pacote o traz (métricas de analisar_F5.metricas_dia).
  D14. Volta Redonda (e, como descritivo, todas as seções): votos e habilitações depois das 17h e das 19h locais, último
      voto, eventos de encerramento (cada "Operador selecionou: Encerrar votação", "Operador cancelou o encerramento da
      votação", "Título digitado para encerramento", "Procedimento de encerramento confirmado", "Inicio do
      Encerramento"; com D17, também "Operador indagado se todas as pessoas presentes votaram" e a resposta) com hora,
      e se o título digitado para encerrar é o de um mesário que liberou eleitor na seção
      (pela letra do D12, sem gravar o número). Também as mensagens do aplicativo de votação entre o último voto e o
      encerramento que não são do fluxo de voto. O log não registra decisão de manter a seção aberta; o que ele mostra é
      quem encerrou (título digitado), quando, e se houve tentativa de encerrar cancelada antes.
  D15. Horas: todas no relógio da urna (local), salvo quando escrito "de Brasília".
  D16. (Escrita depois de rodar a seleção e antes de baixar qualquer arquivo.) A regra do D3 deu 18 seções, não 17
      (todas encerradas entre 19:16:28 e 19:47:21 de Brasília; com 19:16:00 ou depois também são 18). Vale a regra: as
      18 entram no veredito. Extra, fora da letra e fora do veredito: as seções da zona 90 de Volta Redonda encerradas
      entre 19:00:00 e 19:15:00 de Brasília (rótulo extra_vr_19h00_a_19h15), baixadas e conferidas do mesmo jeito e
      relatadas à parte.
  D17. (Escrita depois de testar o código só no 1º turno de AM|2399|45|63 e antes de abrir qualquer arquivo do 2º turno.)
      As letras dos mesários (D12) passam a seguir a ordem da primeira aparição do título em qualquer mensagem de mesário
      do aplicativo de votação ("Pedido de leitura da biometria do mesário N", "Mesário N é eleitor da seção", "Mesário N
      registrado", "Biometria do mesário N encontrada...", "Mesário N habilitou o eleitor"), e o título digitado para
      encerrar (D14) é comparado com todos esses (mesário registrado no log ou não, e se liberou eleitor). Nada do
      critério muda. Os títulos são comparados como número (sem zeros à esquerda): o log grava o mesmo título com e sem
      zeros à esquerda em mensagens diferentes (correção de leitura feita depois da primeira rodada do 2º turno, que só
      afetava esse descritivo). Também com D14: a linha do tempo depois do último voto (urna ligada, desligada pela
      chave, votação suspensa, reinício confirmado, urna pronta, encerrar, título, início do encerramento), com hora.

  Exploratório (modo exploratorio, escrito depois de ver o resultado pela letra; só contexto, sem veredito): nos logs do
  2º turno da amostra de 3.897 seções (amostra2t/arq), com a mesma leitura (ler_log_eventos), a fração de seções em que
  o título digitado para encerrar é de um mesário registrado na urna, a fração com "Votação suspensa" depois do último
  voto e antes do encerramento, e o intervalo entre o último voto e o "Inicio do Encerramento"; por UF e no RJ. E, nas
  seções do F14, quem encerrou em pseudônimo comum a todas (P1, P2...): se o título que encerrou foi registrado como
  mesário na própria seção, em outra seção do F14, e se encerrou outras seções. Nenhum título sai nas saídas. Com o zip
  do eleitorado por local de votação de 2026 (dado aberto do TSE), nome, endereço e coordenadas dos locais 1104 e 1376 da
  zona 90 e a distância em linha reta entre eles; e a hora em que cada urna de Volta Redonda foi religada. Controle:
  RJ|59250|90|232, a única seção dos dois locais encerrada no horário (17:00:46), baixada depois (pasta nova
  F14_arq_controle232) e lida com as mesmas funções, fora do veredito.

Uso:
  python3 -I analisar_F14.py exploratorio <pasta arq da amostra> <pasta_arq_2t> <saida.json> <saida.txt> [eleitorado_local_votacao_2026.zip
          <pasta do controle RJ|59250|90|232> <assin_controle.json> <zips 2T> <zips 1T>]
  python3 -I analisar_F14.py lista <secoes2026.json.gz> <zips 1T> <zips 2T> <F6_sem_biometria.json> <parcial.json> <lista2t.txt> <lista1t.txt>
  python3 -I analisar_F14.py arquivos <parcial.json> <pasta_arq_2t> <assin_2t.json> <pasta_arq_1t> <assin_1t.json>
          <zips 2T> <zips 1T> <secoes2026.json.gz> <saida.json> <saida.txt>
  python3 -I analisar_F14.py --texto <saida.json>
"""
import os as _os, sys as _sys
_sys.path.insert(0, _os.path.dirname(_os.path.abspath(__file__)))
import collections, csv, datetime as dt, glob, io, json, os, re, sys, time, zipfile
import numpy as np

D1, D2 = '04/10/2026', '25/10/2026'
LIM_80 = 0.8
NOMEADAS = ['AC|1554|3|160', 'AC|1040|4|160', 'AC|1066|4|313', 'RR|3026|6|97', 'AM|2097|18|37', 'AM|2097|18|39']
ES_SECAO = 'ES|56995|53|978'
VR_NOME, VR_ZONA = 'VOLTA REDONDA', 90
CASO_1T = 'AM|2399|45|63'
EXTRA = 'extra_vr_19h00_a_19h15'
CONTROLE = 'RJ|59250|90|232'
LIM_VR = dt.datetime(2026, 10, 25, 19, 15, 0)
LIM_VR2 = dt.datetime(2026, 10, 25, 19, 16, 0)
RXH = re.compile(r'^(\d\d/\d\d/\d{4}) (\d\d):(\d\d):(\d\d)$')
RX_MES = re.compile(r'^Mesário (\d+) habilitou o eleitor$')
RX_TIT = re.compile(r'^Título digitado para encerramento: (\d+)$')
LINHA_TEMPO = {'Urna desligada pela chave', 'Votação suspensa', 'Mesário confirmou o reinício da votação',
               'Urna pronta para receber votos', 'Operador selecionou: Encerrar votação',
               'Operador cancelou o encerramento da votação', 'Inicio do Encerramento', 'Início do Encerramento',
               'Contingência executada com sucesso', 'Reiniciando a urna'}
RX_MES_ANY = re.compile(r'^(?:Pedido de leitura da biometria do mesário (\d+)|Mesário (\d+) é eleitor da seção|Mesário (\d+) registrado'
                        r'|Biometria do mesário (\d+) encontrada.*|Mesário (\d+) habilitou o eleitor)$')


def log(*a):
    print('#', time.strftime('%H:%M:%S'), *a, file=sys.stderr, flush=True)


def p_dt(s):
    try:
        return dt.datetime.strptime(s.strip(), '%Y-%m-%d %H:%M:%S')
    except (ValueError, AttributeError):
        return None


def hms(s):
    return None if s is None else f'{s // 3600:02d}:{s % 3600 // 60:02d}:{s % 60:02d}'


def pasta_secao(pasta, k):
    uf, mun, zona, sec = k.split('|')
    return os.path.join(pasta, uf.lower(), f'{int(mun):05d}', f'{int(zona):04d}', f'{int(sec):04d}')


# ================================================================ parte 1: lista
def ler_municipio(zpath, nome_mun):
    """Linhas do cargo 1 de um município (pelo nome) no bweb: abertura, encerramento, junta, zona, seção."""
    z = zipfile.ZipFile(zpath)
    nome = [x for x in z.namelist() if x.lower().endswith('.csv')][0]
    out = {}
    with z.open(nome) as fh:
        rd = csv.reader(io.TextIOWrapper(fh, encoding='latin1', newline=''), delimiter=';')
        cab = next(rd); ix = {c.strip().replace('SG_ UF', 'SG_UF'): i for i, c in enumerate(cab)}
        for r in rd:
            if r[ix['CD_CARGO_PERGUNTA']] != '1' or r[ix['NM_MUNICIPIO']] != nome_mun:
                continue
            k = f"{r[ix['SG_UF']]}|{int(r[ix['CD_MUNICIPIO']])}|{int(r[ix['NR_ZONA']])}|{int(r[ix['NR_SECAO']])}"
            if k not in out:
                out[k] = {c: r[ix[c]] for c in ('DT_ABERTURA', 'DT_ENCERRAMENTO', 'NR_JUNTA_APURADORA', 'NR_ZONA', 'NR_SECAO',
                                                'NR_LOCAL_VOTACAO', 'DS_TIPO_URNA', 'QT_COMPARECIMENTO', 'QT_APTOS',
                                                'NR_URNA_EFETIVADA', 'DT_BU_RECEBIDO', 'DS_SECOES_AGREGADAS')}
    return out


def lista(arq_secoes, zips1, zips2, arq_f6, parcial, lista2, lista1):
    from multiprocessing import Pool
    from lib import carregar, chave_local, fe_ols
    from analisar_F6 import ler_pasta
    t0 = time.time()
    with Pool(4) as pool:
        b2, _ = ler_pasta(zips2, pool, '2T')
        b1, _ = ler_pasta(zips1, pool, '1T')
    log(f'bweb lido em {time.time() - t0:.0f}s: 1T {len(b1)}, 2T {len(b2)}')
    d = carregar(arq_secoes)
    # ---- D1: as 37
    rows = []; fora = collections.Counter()
    for k, v in d.items():
        if k.startswith('ZZ|') or '1' not in v or '2' not in v:
            continue
        a, b = v['1'], v['2']
        if min(a['L'] + a['R'], b['L'] + b['R'], a['comp'], b['comp']) <= 0:
            continue
        f1, f2 = b1.get(k), b2.get(k)
        if f1 is None or f2 is None:
            fora['fora_do_bweb'] += 1; continue
        rows.append((k, chave_local(k, b), '|'.join(k.split('|')[:2]), f1[3], f2[3], a['comp'], b['comp'],
                     a['L'], a['R'], b['L'], b['R']))
    K = np.array([r[0] for r in rows]); LOC = np.array([r[1] for r in rows]); MUN = np.array([r[2] for r in rows])
    A = np.array([r[3:] for r in rows], float)
    NH1, NH2, C1, C2, L1, R1, L2, R2 = A.T
    s1, s2 = NH1 / C1, NH2 / C2
    m = (s1 > LIM_80) & (s2 > LIM_80)
    y = 100 * L2 / (L2 + R2) - 100 * L1 / (L1 + R1); w = L2 + R2; f1p = 100 * L1 / (L1 + R1)
    r = fe_ols(y, m.astype(float)[:, None], LOC, w, ['g'])
    ref = json.load(open(arq_f6))['exploratorio']['liberacao_alta']['acima_de_80pct_nos_dois']
    conf37 = {'secoes_refeitas': int(m.sum()), 'secoes_F6': ref['secoes'],
              'municipios_refeitos': int(len(set(MUN[m]))), 'municipios_F6': ref['municipios'],
              'virada_contra_local_refeita': r['coef']['g'], 'virada_F6': ref['virada_contra_local'],
              'ep_refeito': r['ep']['g'], 'ep_F6': ref['ep'],
              'fatia_Lula_1T_pond_refeita': float(np.average(f1p[m], weights=w[m])), 'fatia_F6': ref['fatia_Lula_1T_pond'],
              'municipios_top_refeitos': collections.Counter(MUN[m]).most_common(8), 'municipios_top_F6': ref['municipios_top'],
              'linhas_no_universo': len(rows), 'excluidas_fora_do_bweb': dict(fora)}
    conf37['bate'] = (conf37['secoes_refeitas'] == conf37['secoes_F6'] and conf37['municipios_refeitos'] == conf37['municipios_F6']
                      and abs(conf37['virada_contra_local_refeita'] - conf37['virada_F6']) < 1e-9)
    g37 = sorted(K[m].tolist())
    ficha37 = {}
    for i in np.where(m)[0]:
        ficha37[K[i]] = {'NH1': int(NH1[i]), 'NH2': int(NH2[i]), 'comp1': int(C1[i]), 'comp2': int(C2[i]),
                         'pct_NH1': float(100 * s1[i]), 'pct_NH2': float(100 * s2[i]),
                         'L1': int(L1[i]), 'R1': int(R1[i]), 'L2': int(L2[i]), 'R2': int(R2[i]), 'virada': float(y[i])}
    log('37:', conf37['secoes_refeitas'], 'bate com o F6:', conf37['bate'])
    # ---- D2: local da ES
    lo = chave_local(ES_SECAO, d[ES_SECAO]['2'])
    gES = sorted(k for k, v in d.items() if '2' in v and k.split('|')[0] == 'ES' and chave_local(k, v['2']) == lo)
    # ---- D3: Volta Redonda
    zrj = sorted(glob.glob(os.path.join(zips2, 'bweb_2t_RJ_*.zip')))[-1]
    vr = ler_municipio(zrj, VR_NOME)
    mods = collections.Counter(p_dt(v['DT_ABERTURA']).hour for v in vr.values()
                               if p_dt(v['DT_ABERTURA']) and v['NR_JUNTA_APURADORA'] in ('-1', ''))
    modal = mods.most_common(1)[0][0]; desloc = modal - 8
    z90 = {k: v for k, v in vr.items() if int(v['NR_ZONA']) == VR_ZONA}
    def enc_br(v):
        e = p_dt(v['DT_ENCERRAMENTO'])
        return e - dt.timedelta(hours=desloc) if e else None
    gVR = sorted(k for k, v in z90.items() if enc_br(v) and enc_br(v) > LIM_VR)
    gVR2 = sorted(k for k, v in z90.items() if enc_br(v) and enc_br(v) >= LIM_VR2)
    gVRx = sorted(k for k, v in z90.items() if enc_br(v) and dt.datetime(2026, 10, 25, 19, 0, 0) <= enc_br(v) <= LIM_VR)
    mun_vr = sorted({k.split('|')[1] for k in vr})
    vr_info = {'codigo_municipio': mun_vr, 'secoes_no_municipio': len(vr), 'aberturas_por_hora': dict(sorted(mods.items())),
               'hora_modal': modal, 'deslocamento_h': desloc, 'secoes_zona_90': len(z90),
               'mantidas_abertas_depois_19h15': len(gVR), 'com_19h16_ou_depois': len(gVR2),
               'zona_90': {k: {'abertura': v['DT_ABERTURA'][11:], 'encerramento': v['DT_ENCERRAMENTO'][11:],
                               'encerramento_brasilia': enc_br(v).strftime('%H:%M:%S') if enc_br(v) else None,
                               'local': v['NR_LOCAL_VOTACAO'], 'comparecimento': v['QT_COMPARECIMENTO'],
                               'tipo': v['DS_TIPO_URNA'], 'junta': v['NR_JUNTA_APURADORA'], 'mantida_aberta': k in gVR}
                           for k, v in sorted(z90.items(), key=lambda kv: int(kv[0].split('|')[3]))}}
    log('Volta Redonda: modal', modal, 'zona 90', len(z90), 'mantidas', len(gVR), '(19h16:', len(gVR2), ')')
    # ---- união
    grupos = collections.defaultdict(list)
    for k in g37: grupos[k].append('liberacao_alta_37')
    for k in gES: grupos[k].append('local_ES_56995_53')
    for k in gVR: grupos[k].append('volta_redonda_z90')
    for k in NOMEADAS: grupos[k].append('nomeada')
    for k in gVRx: grupos[k].append(EXTRA)
    falta_base = [k for k in grupos if k not in d]
    out = {'teste': 'F14 (Adendo 21): casos pendentes', 'registro': 'PRE-REGISTRO-2026-10-26.md, Adendo 21, commit 913af7a',
           'conferencia_37': conf37, 'grupo_37': g37, 'ficha_37': ficha37, 'local_ES': lo, 'grupo_ES': gES,
           'volta_redonda': vr_info, 'grupo_VR': gVR, 'grupo_VR_19h16': gVR2, 'extra_VR_19h00_a_19h15': gVRx, 'nomeadas': NOMEADAS,
           'secoes_2t': {k: grupos[k] for k in sorted(grupos)}, 'secoes_fora_da_base': falta_base, 'caso_1t': CASO_1T}
    json.dump(out, open(parcial, 'w'), ensure_ascii=False, indent=1)
    with open(lista2, 'w') as fh:
        for k in sorted(grupos): fh.write(k + '\n')
    with open(lista1, 'w') as fh:
        fh.write(CASO_1T + '\n')
    log(f'lista: {len(grupos)} seções do 2º turno ({len(g37)} das 37, {len(gES)} do local ES, {len(gVR)} de Volta Redonda, '
        f'{len(NOMEADAS)} nomeadas) e 1 do 1º turno')


# ================================================================ parte 2: arquivos
CAMPOS = ['NR_LOCAL_VOTACAO', 'QT_APTOS', 'QT_COMPARECIMENTO', 'DS_TIPO_URNA', 'NR_URNA_EFETIVADA', 'DT_CARGA_URNA_EFETIVADA',
          'DS_SECOES_AGREGADAS', 'DT_ABERTURA', 'DT_ENCERRAMENTO', 'QT_ELEI_BIOM_SEM_HABILITACAO', 'DT_EMISSAO_BU',
          'DT_BU_RECEBIDO', 'NR_JUNTA_APURADORA', 'NR_TURMA_APURADORA', 'NM_MUNICIPIO']


def ler_bweb_tudo(pasta, rotulo, chaves):
    """Todas as linhas (todos os cargos) das seções pedidas, direto dos zips do TSE."""
    ufs = sorted({k.split('|')[0] for k in chaves})
    out = {}
    for uf in ufs:
        zs = sorted(glob.glob(os.path.join(pasta, f'bweb_{rotulo}_{uf}_*.zip')))
        if not zs:
            continue
        z = zipfile.ZipFile(zs[-1])
        nome = [x for x in z.namelist() if x.lower().endswith('.csv')][0]
        log('lendo', zs[-1].split('/')[-1])
        alvo = {k for k in chaves if k.startswith(uf + '|')}
        with z.open(nome) as fh:
            rd = csv.reader(io.TextIOWrapper(fh, encoding='latin1', newline=''), delimiter=';')
            cab = next(rd); ix = {c.strip().replace('SG_ UF', 'SG_UF'): i for i, c in enumerate(cab)}
            iC, iU, iM, iZ, iS = (ix[c] for c in ('CD_CARGO_PERGUNTA', 'SG_UF', 'CD_MUNICIPIO', 'NR_ZONA', 'NR_SECAO'))
            for r in rd:
                k = f'{r[iU]}|{int(r[iM])}|{int(r[iZ])}|{int(r[iS])}'
                if k not in alvo:
                    continue
                s = out.setdefault(k, {'cargos': {}})
                car = int(r[iC])
                c = s['cargos'].get(car)
                if c is None:
                    c = s['cargos'][car] = {'campos': {x: r[ix[x]] for x in CAMPOS if x in ix}, 'votos': collections.Counter(),
                                            'linhas': 0, 'campos_discordantes': 0}
                else:
                    if any(c['campos'][x] != r[ix[x]] for x in ('QT_APTOS', 'QT_COMPARECIMENTO', 'NR_URNA_EFETIVADA')):
                        c['campos_discordantes'] += 1
                c['linhas'] += 1
                tv = int(r[ix['CD_TIPO_VOTAVEL']]); nv = int(r[ix['NR_VOTAVEL']]); q = int(r[ix['QT_VOTOS']])
                if tv == 1: c['votos'][str(nv)] += q
                elif tv == 2: c['votos']['B'] += q
                elif tv == 3: c['votos']['N'] += q
                else: c['votos'][f'tipo{tv}:{nv}'] += q
    return out


def votos_bu_cargo(c):
    """Votos de um cargo do boletim (decodificar.ler_bu) no mesmo formato do bweb."""
    v = collections.Counter()
    for (t, n), q in c['votos'].items():
        if t == 1: v[str(n)] += q
        elif t == 2: v['B'] += q
        elif t == 3: v['N'] += q
        else: v[f'tipo{t}:{n}'] += q
    return v


def votos_rdv_cargo(r):
    v = collections.Counter()
    for key, q in r.items():
        if key.startswith('num:'): v[key[4:]] += q
        elif key in ('B', 'N'): v[key] += q
        elif key.startswith('tipo'): v[key] += q
    return v


def dif_counter(a, b):
    ks = sorted(set(a) | set(b))
    return {x: [int(a.get(x, 0)), int(b.get(x, 0))] for x in ks if int(a.get(x, 0)) != int(b.get(x, 0))}


def ler_log_eventos(caminho, dia):
    """Leitura descritiva do log no dia (D12 a D14): blocos, mesários (pseudônimos), encerramento, eventos raros."""
    from decodificar import _linhas_log
    blocos = _linhas_log(caminho)
    mes_ord = {}  # título -> letra (ordem da primeira liberação)
    def letra(t):
        if t not in mes_ord:
            i = len(mes_ord); mes_ord[t] = (chr(65 + i) if i < 26 else f'Z{i}')
        return mes_ord[t]
    por_bloco = []; enc_ev = []; raros = []; tit_enc = []; carga = set(); modelo = set()
    pos_ultimo = []
    mes_cont = collections.Counter(); mes_por_hora = collections.defaultdict(collections.Counter)
    registrados, eleitor_da_secao, liberou = set(), set(), set()
    linha_tempo = []
    for bi, bl in enumerate(blocos):
        ev = []
        for l in bl:
            x = l.split('\t')
            if len(x) < 5 or not x[0].startswith(dia):
                continue
            mm = RXH.match(x[0])
            if not mm:
                continue
            t = int(mm.group(2)) * 3600 + int(mm.group(3)) * 60 + int(mm.group(4))
            ev.append((t, x[1], x[2], x[3], x[4]))
        if not ev:
            continue
        votos = [t for t, nv, u, ap, m in ev if m == 'O voto do eleitor foi computado']
        habs = [t for t, nv, u, ap, m in ev if m == 'Eleitor foi habilitado']
        urnas = sorted({u for t, nv, u, ap, m in ev})
        ult = votos[-1] if votos else None
        for t, nv, u, ap, m in ev:
            ma = RX_MES_ANY.match(m) if ap == 'VOTA' else None
            if ma:
                tt = str(int(next(g for g in ma.groups() if g)))
                letra(tt)
                if m.endswith('registrado'): registrados.add(tt)
                if 'encontrada em eleitores' in m or m.endswith('é eleitor da seção'): eleitor_da_secao.add(tt)
            mt = RX_MES.match(m)
            if mt:
                tm = str(int(mt.group(1)))
                L = letra(tm); mes_cont[L] += 1; mes_por_hora[L][f'{t // 3600:02d}h'] += 1
                liberou.add(tm)
            if m.startswith('Modo de carga da UE'):
                carga.add(m)
            if m.startswith('Identificação do Modelo de Urna:'):
                modelo.add(m.split(': ', 1)[1])
            if m in ('Operador selecionou: Encerrar votação', 'Operador cancelou o encerramento da votação',
                     'Procedimento de encerramento confirmado') or m.startswith('Inicio do Encerramento') \
                    or m.startswith('Início do Encerramento') or m.startswith('Todas as pessoas presentes') \
                    or m.startswith('Operador indagado se todas as pessoas'):
                enc_ev.append({'bloco': bi, 'hora': hms(t), 'msg': m})
            mt = RX_TIT.match(m)
            if mt:
                tit_enc.append({'bloco': bi, 'hora': hms(t), 'titulo': str(int(mt.group(1)))})
                enc_ev.append({'bloco': bi, 'hora': hms(t), 'msg': 'Título digitado para encerramento: [título]'})
            ml = m.lower()
            if ('ontingência' in m or 'desligada pela chave' in ml or 'inspeção' in ml or 'reinici' in ml
                    or 'cédula' in ml or nv == 'ERRO' or 'substitu' in ml or 'crítica' in ml or m.startswith('Urna ligada em ')):
                raros.append({'bloco': bi, 'hora': hms(t), 'nivel': nv, 'app': ap, 'msg': re.sub(r'\d{10,}', '[número]', m)})
            if ult is not None and t > ult and ap == 'VOTA' and m not in ('O voto do eleitor foi computado',):
                pos_ultimo.append(re.sub(r'\d{10,}', '[número]', m))
            if ult is not None and t > ult and (m in LINHA_TEMPO or m.startswith('Urna ligada em ')
                                                or m.startswith('Todas as pessoas presentes') or RX_TIT.match(m)):
                linha_tempo.append(f"{hms(t)} [{bi}] " + ('Título digitado para encerramento' if RX_TIT.match(m)
                                                          else re.sub(r' em \d\d/\d\d/\d{4} às .*', '', m)))
        por_bloco.append({'bloco': bi, 'urnas': urnas, 'primeiro_evento': hms(ev[0][0]), 'ultimo_evento': hms(ev[-1][0]),
                          'habilitacoes': len(habs), 'votos': len(votos), 'primeiro_voto': hms(votos[0] if votos else None),
                          'ultimo_voto': hms(ult), 'votos_depois_17h': sum(1 for t in votos if t >= 17 * 3600),
                          'votos_depois_19h': sum(1 for t in votos if t >= 19 * 3600),
                          'habilitacoes_depois_17h': sum(1 for t in habs if t >= 17 * 3600)})
    # o título que encerrou: é de algum mesário que liberou eleitor?
    enc_quem = []
    for te in tit_enc:
        enc_quem.append({'bloco': te['bloco'], 'hora': te['hora'],
                         'titulo_e_de_mesario_que_liberou': te['titulo'] in liberou,
                         'titulo_e_de_mesario_registrado': te['titulo'] in registrados,
                         'titulo_aparece_como_mesario_no_log': te['titulo'] in mes_ord,
                         'mesario': mes_ord.get(te['titulo'])})
    return {'blocos': por_bloco, 'mesarios_que_liberaram': dict(mes_cont),
            'mesarios_no_log': len(mes_ord), 'mesarios_registrados': sorted(mes_ord[t] for t in registrados),
            'mesarios_eleitores_da_secao': sorted(mes_ord[t] for t in eleitor_da_secao),
            'mesarios_por_hora': {k: dict(sorted(v.items())) for k, v in mes_por_hora.items()},
            'eventos_de_encerramento': enc_ev, 'quem_encerrou': enc_quem, 'eventos_raros': raros[:200],
            'eventos_raros_resumo': resumo_raros(raros),
            'eventos_raros_total': len(raros), 'modo_de_carga': sorted(carga), 'modelo': sorted(modelo),
            'vota_depois_do_ultimo_voto': dict(collections.Counter(pos_ultimo)),
            'linha_do_tempo_depois_do_ultimo_voto': linha_tempo}


def resumo_raros(raros):
    r = {}
    for e in raros:
        chave = re.sub(r'\d\d/\d\d/\d{4} às \d\d:\d\d:\d\d', '[hora]', e['msg'])
        x = r.setdefault(chave, {'n': 0, 'primeira': e['hora'], 'ultima': e['hora'], 'blocos': []})
        x['n'] += 1; x['ultima'] = e['hora']
        if e['bloco'] not in x['blocos']: x['blocos'].append(e['bloco'])
    return r


def conferir_secao(k, pasta, dia, bweb, bweb_outro, base_sec, falhas_por, turno):
    """Os cinco itens do sinal e o descritivo de uma seção (D6 a D14)."""
    from decodificar import ler_bu, bu_para_secao, ler_rdv, rdv_para_bu, ler_log
    from analisar_F5 import metricas_dia
    from analisar_F6 import classificar, resumo_dia
    d = pasta_secao(pasta, k)
    fs = sorted(os.listdir(d)) if os.path.isdir(d) else []
    o = {'secao': k, 'turno': turno, 'arquivos': [f for f in fs if f != 'aux.json'], 'sem_aux': 'SEM_AUX' in fs}
    aux = None
    if 'aux.json' in fs:
        aux = json.load(open(os.path.join(d, 'aux.json')))
        o['aux'] = {'st': aux.get('st'), 'pacotes': len(aux.get('hashes', [])),
                    'pacotes_detalhe': [{'dr': h.get('dr'), 'hr': h.get('hr'), 'st': h.get('st'),
                                         'tipos': sorted(a.get('tp') for a in h.get('arq', []))} for h in aux.get('hashes', [])]}
    listados_vsc = [f'{i}-' + a['nm'] for i, h in enumerate((aux or {}).get('hashes', [])) for a in h.get('arq', []) if a.get('tp') == 'vota']

    def ult(suf):
        xs = [f for f in fs if f.endswith(suf)]
        return sorted(xs, key=lambda q: int(q.split('-')[0]))[-1] if xs else None
    fbu, frdv, flog, fvsc = ult('-bu.dat'), ult('-rdv.dat'), ult('-log.jez'), ult('-vota.vsc')
    o['faltando'] = [x for x, v in (('bu', fbu), ('rdv', frdv), ('log', flog), ('vsc', fvsc)) if not v]
    sinais = []
    bw = bweb.get(k, {'cargos': {}})
    o['bweb'] = {str(c): dict(v['campos'], votos=dict(v['votos']), linhas=v['linhas'], campos_discordantes=v['campos_discordantes'])
                 for c, v in bw['cargos'].items() if c in (1, 3, 5)}
    bo = bweb_outro.get(k, {'cargos': {}})
    o['bweb_outro_turno_presidente'] = (dict(bo['cargos'][1]['campos'], votos=dict(bo['cargos'][1]['votos']))
                                        if 1 in bo['cargos'] else None)
    cargos_verd = (1, 3)
    bu = None
    if fbu:
        bu = ler_bu(os.path.join(d, fbu))
        s, g = bu_para_secao(bu)
        o['bu'] = {'urna': bu['urna'], 'versao': bu.get('versao'), 'ab': bu.get('ab'), 'enc': bu.get('enc'),
                   'loc': bu.get('loc'), 'eleicoes': {}}
        cargos_bu = {}
        for ide, rec in bu['eleicoes'].items():
            o['bu']['eleicoes'][str(ide)] = {'apt': rec['apt'], 'cargos': sorted(rec['cargos'])}
            for car, c in rec['cargos'].items():
                cargos_bu[car] = {'apt': rec['apt'], 'comp': c['comp'], 'votos': votos_bu_cargo(c)}
        o['bu']['cargos'] = {str(c): {'apt': v['apt'], 'comp': v['comp'], 'votos': dict(v['votos'])} for c, v in cargos_bu.items()}
        difs = {}; difs_desc = {}
        for car, cb in cargos_bu.items():
            linha = bw['cargos'].get(car)
            alvo = difs if car in cargos_verd else difs_desc
            if linha is None:
                alvo[str(car)] = 'cargo no boletim e não no bweb'; continue
            cp = linha['campos']
            dd = {}
            if int(cp['QT_COMPARECIMENTO']) != cb['comp']: dd['comparecimento'] = [cb['comp'], int(cp['QT_COMPARECIMENTO'])]
            if int(cp['QT_APTOS']) != cb['apt']: dd['aptos'] = [cb['apt'], int(cp['QT_APTOS'])]
            if int(cp['NR_URNA_EFETIVADA'] or 0) != bu['urna']: dd['urna'] = [bu['urna'], int(cp['NR_URNA_EFETIVADA'] or 0)]
            dv = dif_counter(cb['votos'], linha['votos'])
            if dv: dd['votos'] = dv
            if linha['campos_discordantes']: dd['linhas_do_bweb_discordantes'] = linha['campos_discordantes']
            if dd: alvo[str(car)] = dd
        for car in bw['cargos']:
            if car in cargos_verd and car not in cargos_bu:
                difs[str(car)] = 'cargo no bweb e não no boletim'
        o['bu_vs_bweb_diferencas'] = difs; o['bu_vs_bweb_diferencas_descritivo'] = difs_desc
        o['bu_igual_bweb'] = (not difs) if bw['cargos'] else None
        if bw['cargos'] and difs: sinais.append('boletim diferente do bweb')
        if not bw['cargos']: o['bu_vs_bweb_nota'] = 'seção sem linhas no bweb'
        if turno == 2 and s:
            bb = base_sec or {}
            o['bu_igual_base_secoes2026'] = all(s[x] == bb.get(x) for x in ('urna', 'apt', 'comp', 'L', 'R', 'B', 'N'))
        # RDV
        if frdv:
            rv = rdv_para_bu(ler_rdv(os.path.join(d, frdv)))
            difr = {}; difr_desc = {}
            o['rdv'] = {}
            for car, cb in cargos_bu.items():
                vr = votos_rdv_cargo(rv.get(car, collections.Counter()))
                o['rdv'][str(car)] = {'votos': dict(vr), 'total': int(rv.get(car, collections.Counter()).get('total', 0)),
                                      'nulo_tipo6': int(rv.get(car, collections.Counter()).get('nulo_tipo6', 0))}
                dv = dif_counter(vr, cb['votos'])
                if dv:
                    (difr if car in cargos_verd else difr_desc)[str(car)] = dv
            o['rdv_vs_bu_diferencas'] = difr; o['rdv_vs_bu_diferencas_descritivo'] = difr_desc
            o['rdv_igual_bu'] = not difr
            if difr: sinais.append('RDV diferente do boletim')
        else:
            o['rdv_igual_bu'] = None
    else:
        o['bu_igual_bweb'] = None; o['rdv_igual_bu'] = None
    # log
    comp_ref = None
    if bu:
        for ide, rec in bu['eleicoes'].items():
            if 1 in rec['cargos']: comp_ref = rec['cargos'][1]['comp']
    elif 1 in bw['cargos']:
        comp_ref = int(bw['cargos'][1]['campos']['QT_COMPARECIMENTO'])
    if flog:
        caminho = os.path.join(d, flog)
        Lg = ler_log(caminho, dia)
        o['T3'] = {x: Lg[x] for x in ('logs_no_pacote', 'computados', 'habilitados', 'A2_antes', 'A2_depois', 'A3_sem_habilitacao',
                                      'A4_menos_2s', 'A5_rajadas', 'maior_sequencia_rapida', 'dur_mediana', 'dur_min',
                                      'contingencia', 'urnas_no_log', 'erros', 'primeiro_voto', 'ultimo_voto', 'pronta',
                                      'encerramento')}
        o['votos_log_igual_comparecimento'] = (Lg['computados'] == comp_ref) if comp_ref is not None else None
        if comp_ref is not None and Lg['computados'] != comp_ref: sinais.append('votos no log diferentes do comparecimento')
        for a in ('A2_antes', 'A2_depois', 'A3_sem_habilitacao', 'A4_menos_2s', 'A5_rajadas'):
            if Lg[a]: sinais.append(f'anomalia {a}')
        from decodificar import _linhas_log
        blocos = _linhas_log(caminho)
        outro = D1 if dia == D2 else D2
        o['log_dia'] = metricas_dia(blocos, dia)
        o['log_outro_dia_mesma_urna'] = metricas_dia(blocos, outro)
        hab, comp, falhas, tipos, urnas, contg, nbl = classificar(caminho)
        uf = k.split('|')[0]
        rd_ = resumo_dia(hab[dia], uf); rd_['computados'] = comp[dia]
        rd_o = resumo_dia(hab[outro], uf); rd_o['computados'] = comp[outro]
        for rr in (rd_, rd_o):
            rr['ultima_M'] = hms(rr['ultima_M'])
            rr['por_hora'] = {c: dict(sorted(v.items(), key=lambda kv: int(kv[0]))) for c, v in rr['por_hora'].items()}
        Ms = sorted(t for t, c, _ in hab[dia] if c == 'M')
        rd_['primeira_M'] = hms(Ms[0]) if Ms else None
        rd_['M_19h_local'] = sum(1 for t in Ms if t >= 19 * 3600)
        o['liberacoes'] = rd_; o['liberacoes_outro_dia_mesma_urna'] = rd_o
        o['falhas_leitor'] = {f'{a}|{b}': v for (a, b), v in falhas.items()}
        o['contingencia_F6'] = contg; o['blocos_de_log'] = nbl
        ev = ler_log_eventos(caminho, dia)
        o['eventos'] = ev
        nh_bw = bw['cargos'].get(1, {}).get('campos', {}).get('QT_ELEI_BIOM_SEM_HABILITACAO')
        o['M_log_contra_NH_bweb'] = {'M_log': rd_['M'], 'NH_bweb': (int(nh_bw) if nh_bw not in (None, '') else None),
                                     'log_completo': comp[dia] == comp_ref}
        nh_o = (bo['cargos'].get(1, {}).get('campos', {}).get('QT_ELEI_BIOM_SEM_HABILITACAO') if bo['cargos'] else None)
        o['M_log_outro_dia_contra_NH_bweb'] = {'M_log': rd_o['M'], 'NH_bweb': (int(nh_o) if nh_o not in (None, '') else None),
                                               'votos_log': comp[outro]}
    else:
        o['votos_log_igual_comparecimento'] = None
    # assinatura
    if listados_vsc:
        fl = falhas_por.get(k, [])
        falta = [f for f in listados_vsc if f not in fs]
        o['assinatura_falhas'] = fl; o['vsc_listado_nao_baixado'] = falta
        o['assinatura_ok'] = not fl and not falta
        if not o['assinatura_ok']: sinais.append('assinatura inválida')
    else:
        o['assinatura_ok'] = None
    o['sinais'] = sinais
    return o


def ler_assin(arq):
    t = open(arq).read(); a = json.loads(t[t.find('{'):])
    fp = collections.defaultdict(list)
    for fl in a.get('falhas', []):
        fp[fl[0]].append(fl[1:])
    return a, fp


def arquivos(parcial, pasta2, assin2, pasta1, assin1, zips2, zips1, arq_secoes, saida_json, saida_txt):
    from lib import carregar
    P = json.load(open(parcial))
    chaves2 = list(P['secoes_2t'])
    a2, fp2 = ler_assin(assin2)
    a1, fp1 = ler_assin(assin1) if os.path.exists(assin1) else ({}, {})
    bw2 = ler_bweb_tudo(zips2, '2t', chaves2 + [P['caso_1t']])
    bw1 = ler_bweb_tudo(zips1, '1t', chaves2 + [P['caso_1t']])
    base = carregar(arq_secoes)
    res = []
    for k in chaves2:
        o = conferir_secao(k, pasta2, D2, bw2, bw1, base.get(k, {}).get('2'), fp2, 2)
        o['grupos'] = P['secoes_2t'][k]
        o['base'] = {t: {x: y for x, y in base.get(k, {}).get(t, {}).items() if x != 'cand'} for t in ('1', '2') if t in base.get(k, {})}
        res.append(o)
    k1 = P['caso_1t']
    d1 = pasta_secao(pasta1, k1)
    o1 = None
    if os.path.isdir(d1):
        o1 = conferir_secao(k1, pasta1, D1, bw1, bw2, base.get(k1, {}).get('1'), fp1, 1)
        o1['grupos'] = ['caso_1t']
        o1['base'] = {t: {x: y for x, y in base.get(k1, {}).get(t, {}).items() if x != 'cand'} for t in ('1', '2') if t in base.get(k1, {})}
    extras = [o for o in res if set(o['grupos']) == {EXTRA}]
    todas = [o for o in res if set(o['grupos']) != {EXTRA}] + ([o1] if o1 else [])
    com_sinal = [o['secao'] + (' (1º turno)' if o['turno'] == 1 else '') for o in todas if o['sinais']]
    ver = 'SINAL' if com_sinal else 'SEM SINAL'
    extras_sinal = [o['secao'] for o in extras if o['sinais']]
    def cnt(campo, val=True, xs=todas): return sum(1 for o in xs if o.get(campo) is val)
    def den(campo, xs=todas): return sum(1 for o in xs if o.get(campo) is not None)
    resumo = {'secoes_2t_no_veredito': len(todas) - (1 if o1 else 0), 'secoes_extra_fora_do_veredito': len(extras),
              'extras_com_sinal': extras_sinal,
              'secao_1t_existe': o1 is not None and not o1.get('sem_aux'),
              'bu_igual_bweb': [cnt('bu_igual_bweb'), den('bu_igual_bweb')],
              'rdv_igual_bu': [cnt('rdv_igual_bu'), den('rdv_igual_bu')],
              'votos_log_igual_comparecimento': [cnt('votos_log_igual_comparecimento'), den('votos_log_igual_comparecimento')],
              'assinatura_ok': [cnt('assinatura_ok'), den('assinatura_ok')],
              'anomalias_T3': {a: sum((o.get('T3') or {}).get(a, 0) for o in todas)
                               for a in ('A2_antes', 'A2_depois', 'A3_sem_habilitacao', 'A4_menos_2s', 'A5_rajadas')},
              'faltando': {o['secao'] + ('|1T' if o['turno'] == 1 else ''): o['faltando'] for o in todas if o['faltando']},
              'sem_aux': [o['secao'] for o in todas if o.get('sem_aux')],
              'pacotes_multiplos': [o['secao'] for o in todas if (o.get('aux') or {}).get('pacotes', 1) > 1]}
    # agregados descritivos por grupo
    agg = {}
    for gname in ('liberacao_alta_37', 'local_ES_56995_53', 'volta_redonda_z90', 'nomeada', EXTRA):
        xs = [o for o in res if gname in o['grupos'] and o.get('liberacoes')]
        como = collections.Counter(); hora = collections.Counter(); M = H = 0
        for o in xs:
            como.update(o['liberacoes']['como_M']); M += o['liberacoes']['M']; H += o['liberacoes']['hab']
            hora.update(o['liberacoes']['por_hora']['M'])
        agg[gname] = {'secoes_com_log': len(xs), 'habilitacoes': H, 'M': M, 'como_M': dict(como),
                      'M_por_hora': dict(sorted(hora.items(), key=lambda kv: int(kv[0]))),
                      'M_igual_NH_bweb': sum(1 for o in xs if o['M_log_contra_NH_bweb']['M_log'] == o['M_log_contra_NH_bweb']['NH_bweb']),
                      'contingencia': sum(1 for o in xs if (o.get('T3') or {}).get('contingencia')),
                      'votos_depois_17h': sum(b['votos_depois_17h'] for o in xs for b in o['eventos']['blocos']),
                      'votos_depois_19h': sum(b['votos_depois_19h'] for o in xs for b in o['eventos']['blocos'])}
    out = dict(P)
    out['assinaturas_2t'] = {'contagem': a2.get('contagem'), 'falhas': a2.get('falhas'), 'emissores': a2.get('emissores'),
                             'modo': a2.get('modo_da_assinatura'), 'validade': a2.get('validade_certificados'),
                             'chaves_software': a2.get('chaves_software')}
    out['assinaturas_1t'] = {'contagem': a1.get('contagem'), 'falhas': a1.get('falhas'), 'emissores': a1.get('emissores'),
                             'validade': a1.get('validade_certificados')} if a1 else None
    out['resumo'] = resumo; out['secoes_com_sinal'] = com_sinal; out['veredito'] = ver
    out['agregado_por_grupo'] = agg
    out['por_secao'] = res; out['caso_1t_resultado'] = o1
    json.dump(out, open(saida_json, 'w'), ensure_ascii=False, indent=1, default=str)
    open(saida_txt, 'w').write(texto(out))
    log('veredito', ver, com_sinal)


# ================================================================ exploratório
def _expl_um(caminho):
    try:
        e = ler_log_eventos(caminho, D2)
    except Exception as x:
        return caminho, {'erro': str(x)}
    lt = e['linha_do_tempo_depois_do_ultimo_voto']
    ult = max((b['ultimo_voto'] for b in e['blocos'] if b['ultimo_voto']), default=None)
    ini = [x for x in e['eventos_de_encerramento'] if x['msg'].startswith('Inicio do Encerramento')]
    def seg(h): return int(h[:2]) * 3600 + int(h[3:5]) * 60 + int(h[6:8])
    return caminho, {'q': e['quem_encerrou'][-1] if e['quem_encerrou'] else None, 'registrados': len(e['mesarios_registrados']),
                     'suspensa_depois_do_ultimo': any('Votação suspensa' in x for x in lt),
                     'ligada_depois_do_ultimo': sum(1 for x in lt if 'Urna ligada' in x),
                     'ultimo_voto': ult, 'inicio_enc': ini[-1]['hora'] if ini else None,
                     'gap_min': (seg(ini[-1]['hora']) - seg(ult)) / 60 if ini and ult else None,
                     'contingencia': any('ontingência' in r['msg'] for r in e['eventos_raros'])}


def titulos_secao(caminho, dia):
    """Títulos (normalizados) registrados como mesário e digitados para encerrar, só para comparação interna."""
    from decodificar import _linhas_log
    reg = set(); lib = set(); enc = []
    for bl in _linhas_log(caminho):
        for l in bl:
            x = l.split('\t')
            if len(x) < 5 or not x[0].startswith(dia) or x[3] != 'VOTA':
                continue
            m = x[4]
            a = re.match(r'^Mesário (\d+) registrado$', m)
            if a: reg.add(int(a.group(1)))
            a = RX_MES.match(m)
            if a: lib.add(int(a.group(1)))
            a = RX_TIT.match(m)
            if a: enc.append((x[0][11:], int(a.group(1))))
    return reg, lib, enc


def cruzar_titulos(pasta_f14, chaves, extras=None):
    """Pseudônimos P1, P2... para os títulos que encerraram as seções do F14 (nenhum número sai daqui)."""
    dados = {}
    pastas = {k: pasta_f14 for k in chaves}
    pastas.update(extras or {})
    chaves = list(chaves) + [k for k in (extras or {}) if k not in chaves]
    for k in chaves:
        fs = glob.glob(os.path.join(pasta_secao(pastas[k], k), '*-log.jez'))
        if fs:
            dados[k] = titulos_secao(sorted(fs)[-1], D2)
    pseud = {}
    for k in chaves:
        for h, tt in (dados.get(k) or (set(), set(), []))[2]:
            if tt not in pseud: pseud[tt] = f'P{len(pseud) + 1}'
    reg_em = collections.defaultdict(list); lib_em = collections.defaultdict(list)
    for k, (reg, lib, enc) in dados.items():
        for tt in reg: reg_em[tt].append(k)
        for tt in lib: lib_em[tt].append(k)
    out = {}
    for k in chaves:
        if k not in dados: continue
        reg, lib, enc = dados[k]
        out[k] = [{'hora': h, 'quem': pseud[tt], 'registrado_nesta_secao': tt in reg, 'liberou_nesta_secao': tt in lib,
                   'registrado_em_outras_secoes_do_F14': [x for x in reg_em.get(tt, []) if x != k],
                   'encerrou_outras_secoes_do_F14': sorted(x for x, (_, _, e2) in dados.items() if x != k and any(t2 == tt for _, t2 in e2))}
                  for h, tt in enc]
    return out


def locais_vr(zip_locais, locais):
    """Endereço e coordenadas dos locais da zona 90 de Volta Redonda no dado aberto do TSE (eleitorado por local de votação)."""
    import math
    z = zipfile.ZipFile(zip_locais)
    nome = [x for x in z.namelist() if x.endswith('_RJ.csv')][0]
    out = {}
    with z.open(nome) as fh:
        rd = csv.reader(io.TextIOWrapper(fh, encoding='latin1', newline=''), delimiter=';')
        cab = next(rd); ix = {c: i for i, c in enumerate(cab)}
        for r in rd:
            if r[ix['CD_MUNICIPIO']] == '59250' and r[ix['NR_ZONA']] == str(VR_ZONA) and r[ix['NR_TURNO']] == '2' \
                    and r[ix['NR_LOCAL_VOTACAO']] in locais and r[ix['NR_LOCAL_VOTACAO']] not in out:
                out[r[ix['NR_LOCAL_VOTACAO']]] = {c: r[ix[c]] for c in ('NM_LOCAL_VOTACAO', 'DS_ENDERECO', 'NM_BAIRRO', 'NR_LATITUDE', 'NR_LONGITUDE')}
    ks = sorted(out)
    if len(ks) == 2:
        (a1, o1), (a2, o2) = ((float(out[k]['NR_LATITUDE'].replace(',', '.')), float(out[k]['NR_LONGITUDE'].replace(',', '.'))) for k in ks)
        R_ = 6371000.0
        f1, f2 = math.radians(a1), math.radians(a2); df = f2 - f1; dl = math.radians(o2 - o1)
        h = math.sin(df / 2) ** 2 + math.cos(f1) * math.cos(f2) * math.sin(dl / 2) ** 2
        out['distancia_em_linha_reta_m'] = 2 * R_ * math.asin(math.sqrt(h))
    return out


def exploratorio(pasta_amostra, pasta_f14, saida_json, saida_txt, zip_locais=None, pasta_controle=None, assin_controle=None,
                 zips2=None, zips1=None):
    from multiprocessing import Pool
    logs = sorted(glob.glob(os.path.join(pasta_amostra, '*/*/*/*/*-log.jez')))
    with Pool(4) as pool:
        res = dict(pool.map(_expl_um, logs, chunksize=20))
    por = collections.defaultdict(collections.Counter)
    gaps = collections.defaultdict(list)
    for c, r in res.items():
        uf = c.split('/')[-5].upper()
        for g in (uf, 'BR'):
            P_ = por[g]; P_['logs'] += 1
            if 'erro' in r: P_['erro'] += 1; continue
            q = r['q']
            if q is None: P_['sem_titulo_de_encerramento'] += 1
            else:
                P_['com_titulo'] += 1
                P_['titulo_de_mesario_registrado'] += q['titulo_e_de_mesario_registrado']
                P_['titulo_de_mesario_que_liberou'] += q['titulo_e_de_mesario_que_liberou']
                P_['titulo_aparece_como_mesario'] += q['titulo_aparece_como_mesario_no_log']
                if r['registrados'] == 0: P_['sem_mesario_registrado'] += 1
            P_['votacao_suspensa_depois_do_ultimo_voto'] += r['suspensa_depois_do_ultimo']
            P_['urna_religada_depois_do_ultimo_voto'] += r['ligada_depois_do_ultimo'] > 0
            if r['gap_min'] is not None:
                gaps[g].append(r['gap_min'])
                P_['encerramento_mais_de_60_min_depois_do_ultimo_voto'] += r['gap_min'] > 60
                P_['suspensa_e_mais_de_60_min'] += r['suspensa_depois_do_ultimo'] and r['gap_min'] > 60
    out = {'nota': 'escrito depois de ver o resultado pela letra; contexto, sem veredito', 'logs': len(logs),
           'por_uf': {g: dict(v) for g, v in sorted(por.items())},
           'mediana_min_ultimo_voto_ao_encerramento': {g: float(np.median(v)) for g, v in sorted(gaps.items()) if v},
           'exemplos_suspensa_e_mais_de_60_min': sorted('|'.join(c.split('/')[-5:-1]) for c, r in res.items()
                                                       if r.get('suspensa_depois_do_ultimo') and (r.get('gap_min') or 0) > 60)[:60]}
    exc = []
    for c, r in res.items():
        q = r.get('q')
        if q and not q['titulo_e_de_mesario_registrado']:
            exc.append({'secao': '|'.join(c.split('/')[-5:-1]), 'mesarios_registrados': r['registrados'],
                        'suspensa_depois_do_ultimo': r['suspensa_depois_do_ultimo'], 'religada': r['ligada_depois_do_ultimo'],
                        'contingencia': r['contingencia'], 'minutos_ultimo_voto_ao_encerramento': r['gap_min']})
    out['amostra_titulo_de_encerramento_fora_dos_registrados'] = exc
    R = json.load(open(saida_json)); R['exploratorio_amostra'] = out
    extras = {CONTROLE: pasta_controle} if pasta_controle else None
    R['exploratorio_titulos_de_encerramento_F14'] = cruzar_titulos(pasta_f14, list(R['secoes_2t']), extras)
    if pasta_controle:
        _, fpc = ler_assin(assin_controle)
        bw2c = ler_bweb_tudo(zips2, '2t', [CONTROLE]); bw1c = ler_bweb_tudo(zips1, '1t', [CONTROLE])
        oc = conferir_secao(CONTROLE, pasta_controle, D2, bw2c, bw1c, None, fpc, 2)
        oc.pop('bu_igual_base_secoes2026', None)
        oc['grupos'] = ['controle_local_1376']; oc['base'] = {}
        R['exploratorio_controle_232'] = oc
    if zip_locais:
        R['exploratorio_locais_volta_redonda'] = locais_vr(zip_locais, {'1104', '1376'})
    # religamento das urnas de Volta Redonda: hora do último "Urna ligada" antes do encerramento, por local
    rel = {}
    for o in R['por_secao']:
        if 'volta_redonda_z90' in o['grupos'] or EXTRA in o['grupos']:
            lt = o['eventos']['linha_do_tempo_depois_do_ultimo_voto']
            lig = [x[:8] for x in lt if 'Urna ligada' in x]
            rel[o['secao']] = {'local': R['volta_redonda']['zona_90'][o['secao']]['local'], 'ultima_vez_ligada': lig[-1] if lig else None}
    R['exploratorio_religamento_volta_redonda'] = rel
    json.dump(R, open(saida_json, 'w'), ensure_ascii=False, indent=1, default=str)
    open(saida_txt, 'w').write(texto(R))


# ================================================================ texto
def fn(x, nd=1):
    if x is None: return '-'
    return f'{x:,.{nd}f}'.replace(',', 'X').replace('.', ',').replace('X', '.')


def linha_secao(o):
    L = []; w = L.append
    b = o.get('base', {}); b1 = b.get('1', {}); b2 = b.get('2', {})
    lb = o.get('liberacoes') or {}; ev = o.get('eventos') or {}; t3 = o.get('T3') or {}
    nh = o.get('M_log_contra_NH_bweb') or {}; nho = o.get('M_log_outro_dia_contra_NH_bweb') or {}
    lbo = o.get('liberacoes_outro_dia_mesma_urna') or {}
    turno = o['turno']
    w(f"* {o['secao']}{' (1º turno)' if turno == 1 else ''} [{', '.join(o.get('grupos', []))}]: "
      f"{'; '.join(o['sinais']) if o['sinais'] else 'sem sinal'}"
      + (f"; falta {', '.join(o['faltando'])}" if o['faltando'] else ''))
    bw1 = (o.get('bweb') or {}).get('1', {})
    w(f"    município {bw1.get('NM_MUNICIPIO', '-')}; 1T L/R {b1.get('L')}/{b1.get('R')} comp {b1.get('comp')}, 2T L/R {b2.get('L')}/{b2.get('R')}"
      f" comp {b2.get('comp')}; urna 1T {b1.get('urna')} 2T {b2.get('urna')}; bweb abertura {bw1.get('DT_ABERTURA', '-')[11:]} encerramento"
      f" {bw1.get('DT_ENCERRAMENTO', '-')[11:]}")
    w(f"    conferências: boletim=bweb {o.get('bu_igual_bweb')}, RDV=boletim {o.get('rdv_igual_bu')}, log=comparecimento"
      f" {o.get('votos_log_igual_comparecimento')} ({t3.get('computados')} votos no log), assinatura ok {o.get('assinatura_ok')};"
      f" A2 {t3.get('A2_antes', 0)}+{t3.get('A2_depois', 0)}, A3 {t3.get('A3_sem_habilitacao', 0)}, A4 {t3.get('A4_menos_2s', 0)},"
      f" A5 {t3.get('A5_rajadas', 0)} (maior sequência rápida {t3.get('maior_sequencia_rapida')}, duração mediana {t3.get('dur_mediana')} s)")
    if o.get('bu_vs_bweb_diferencas'): w(f"    diferenças boletim x bweb: {o['bu_vs_bweb_diferencas']}")
    if o.get('bu_vs_bweb_diferencas_descritivo'): w(f"    (descritivo, senador) boletim x bweb: {o['bu_vs_bweb_diferencas_descritivo']}")
    if o.get('rdv_vs_bu_diferencas'): w(f"    diferenças RDV x boletim: {o['rdv_vs_bu_diferencas']}")
    if o.get('rdv_vs_bu_diferencas_descritivo'): w(f"    (descritivo, senador) RDV x boletim: {o['rdv_vs_bu_diferencas_descritivo']}")
    if o.get('assinatura_falhas'): w(f"    falhas de assinatura: {o['assinatura_falhas']}")
    if lb:
        w(f"    liberações no dia: {lb.get('hab')} habilitações, B {lb.get('B')}, M (sem biometria, com cadastro) {lb.get('M')}, S {lb.get('S')};"
          f" M do log {nh.get('M_log')} contra NH do bweb {nh.get('NH_bweb')}; quem liberou as M: {lb.get('como_M')};"
          f" mesários que liberaram (pseudônimos): {ev.get('mesarios_que_liberaram')}")
        w(f"    horário das M: primeira {lb.get('primeira_M')}, última {lb.get('ultima_M')}, depois das 16h {lb.get('M_16h_local')},"
          f" depois das 17h {lb.get('M_17h_local')}, maior número em 30 min {lb.get('max_M_em_30min')}; M por hora {lb.get('por_hora', {}).get('M')}")
        if lbo.get('hab'):
            w(f"    outro turno na mesma urna (log do pacote): {lbo.get('hab')} habilitações, M {lbo.get('M')} (NH do bweb {nho.get('NH_bweb')}),"
              f" votos no log {nho.get('votos_log')}; quem liberou {lbo.get('como_M')}")
    for bl in ev.get('blocos', []):
        w(f"    bloco {bl['bloco']}: urna {','.join(bl['urnas'])}, eventos {bl['primeiro_evento']} a {bl['ultimo_evento']}, habilitações {bl['habilitacoes']},"
          f" votos {bl['votos']} ({bl['primeiro_voto']} a {bl['ultimo_voto']}), depois das 17h {bl['votos_depois_17h']}, depois das 19h {bl['votos_depois_19h']}")
    if ev.get('eventos_de_encerramento'):
        w('    encerramento: ' + '; '.join(f"{e['hora']} {e['msg']}" for e in ev['eventos_de_encerramento']))
    if ev.get('quem_encerrou'):
        w('    quem encerrou: ' + '; '.join(f"{q['hora']} mesário {q['mesario'] or 'que não aparece como mesário no log'}"
                                         f" (registrado: {'sim' if q['titulo_e_de_mesario_registrado'] else 'não'}; liberou eleitor: "
                                         f"{'sim' if q['titulo_e_de_mesario_que_liberou'] else 'não'})" for q in ev['quem_encerrou'])
          + f"; mesários no log {ev.get('mesarios_no_log')}, registrados {ev.get('mesarios_registrados')}")
    if ev.get('linha_do_tempo_depois_do_ultimo_voto'):
        w('    depois do último voto: ' + '; '.join(ev['linha_do_tempo_depois_do_ultimo_voto']))
    if ev.get('eventos_raros_resumo'):
        w(f"    eventos (ligada, contingência, chave, inspeção, bateria crítica, erro; {ev.get('eventos_raros_total')} no total): "
          + '; '.join(f"{m} x{x['n']} ({x['primeira']}{' a ' + x['ultima'] if x['n'] > 1 else ''}, bloco {','.join(map(str, x['blocos']))})"
                      for m, x in ev['eventos_raros_resumo'].items()))
    return L


def todas_secoes(R):
    return [o for o in R['por_secao'] if set(o['grupos']) != {EXTRA}] + ([R['caso_1t_resultado']] if R.get('caso_1t_resultado') else [])


def texto(R):
    L = []; w = L.append
    w('F14 (Adendo 21): casos pendentes, arquivo por arquivo')
    w('Registro: PRE-REGISTRO-2026-10-26.md, Adendo 21 (commit 913af7a, 31/10/2026 10:36:29 UTC). Script: scripts/analisar_F14.py.')
    w('')
    w('Letra do registro')
    w('- Boletim, RDV, log e assinatura das 37 seções com mais de 80% de liberação sem biometria nos dois turnos (F6), de ES|56995|53|978 e')
    w('  das outras seções do local, das 17 seções da zona 90 de Volta Redonda mantidas abertas, de AC|1554|3|160, AC|1040|4|160,')
    w('  AC|1066|4|313, RR|3026|6|97, AM|2097|18|37 e 39, e o 1º turno de AM|2399|45|63 se o arquivo existir.')
    w('- Sinal: assinatura inválida, boletim diferente do bweb, RDV diferente do boletim, votos no log diferentes do comparecimento, ou')
    w('  anomalia A2 a A5. Descritivo: quem liberou (mesário identificado ou não), horário das liberações e contingências.')
    w('')
    c = R['conferencia_37']
    w('Seleção')
    w(f"- As 37 (D1), refeitas do bweb: {c['secoes_refeitas']} seções (F6: {c['secoes_F6']}), {c['municipios_refeitos']} municípios (F6: {c['municipios_F6']}),"
      f" virada contra o local {c['virada_contra_local_refeita']:+.4f} (F6: {c['virada_F6']:+.4f}); bate: {c['bate']}.")
    w(f"- Local da ES|56995|53|978 (D2): {R['local_ES']}, {len(R['grupo_ES'])} seções.")
    v = R['volta_redonda']
    w(f"- Volta Redonda (D3): município {','.join(v['codigo_municipio'])}, {v['secoes_no_municipio']} seções; abertura modal às {v['hora_modal']}h"
      f" (deslocamento {v['deslocamento_h']} h); zona 90 com {v['secoes_zona_90']} seções; encerradas depois das 19:15:00 de Brasília:"
      f" {v['mantidas_abertas_depois_19h15']} (19:16:00 ou depois: {v['com_19h16_ou_depois']}).")
    w(f"- Extra (D16): {', '.join(R.get('extra_VR_19h00_a_19h15', []))}.")
    w(f"- Nomeadas: {', '.join(R['nomeadas'])}. Total do 2º turno: {len(R['secoes_2t'])} seções distintas (com o extra). 1º turno: {R['caso_1t']}.")
    if 'resumo' not in R:
        return '\n'.join(L) + '\n'
    S = R['resumo']; A = R['assinaturas_2t'] or {}; cc = A.get('contagem') or {}
    w('')
    w('Resultado pela letra')
    w(f"- Boletim igual ao bweb: {S['bu_igual_bweb'][0]} de {S['bu_igual_bweb'][1]}. RDV igual ao boletim: {S['rdv_igual_bu'][0]} de {S['rdv_igual_bu'][1]}."
      f" Votos no log = comparecimento: {S['votos_log_igual_comparecimento'][0]} de {S['votos_log_igual_comparecimento'][1]}."
      f" Assinatura ok: {S['assinatura_ok'][0]} de {S['assinatura_ok'][1]}.")
    w('- Anomalias do T3 somadas: ' + ', '.join(f'{k} {x}' for k, x in S['anomalias_T3'].items()) + '.')
    w(f"- Assinaturas do 2º turno (verificar_assinaturas.py): seções com vsc {cc.get('secoes_com_vsc')}, bloco de hardware ok {cc.get('bloco_hw_assinatura_ok')},"
      f" arquivos com assinatura ok {cc.get('assinatura_arquivo_ok')} de {cc.get('arquivos_listados')}, resumos ok {cc.get('resumo_ok')} de"
      f" {cc.get('arquivos_baixados_conferidos')}, SHA-256 do vsc igual ao aux {cc.get('vsc_sha256_igual_ao_aux')}, urna do certificado igual à do"
      f" boletim {cc.get('urna_cert_igual_bu')}; falhas {len(A.get('falhas') or [])}.")
    A1 = R.get('assinaturas_1t') or {}
    if A1:
        c1 = A1.get('contagem') or {}
        w(f"- Assinatura do 1º turno de {R['caso_1t']}: seções com vsc {c1.get('secoes_com_vsc')}, bloco ok {c1.get('bloco_hw_assinatura_ok')},"
          f" arquivos ok {c1.get('assinatura_arquivo_ok')} de {c1.get('arquivos_listados')}, resumos ok {c1.get('resumo_ok')} de"
          f" {c1.get('arquivos_baixados_conferidos')}, urna do certificado igual {c1.get('urna_cert_igual_bu')}; falhas {len(A1.get('falhas') or [])}.")
    if S['faltando']: w('- Arquivos que não vieram: ' + '; '.join(f"{k}: {', '.join(x)}" for k, x in S['faltando'].items()))
    if S['sem_aux']: w('- Sem aux.json: ' + ', '.join(S['sem_aux']))
    if S['pacotes_multiplos']: w('- Mais de um pacote no aux: ' + ', '.join(S['pacotes_multiplos']))
    w(f"- Seções com sinal: {len(R['secoes_com_sinal'])}" + (': ' + ', '.join(R['secoes_com_sinal']) if R['secoes_com_sinal'] else '') + '.')
    w(f"- VEREDITO: {R['veredito']}.")
    w(f"- Extra fora do veredito (D16): {S['secoes_extra_fora_do_veredito']} seções; com algum dos cinco itens: "
      f"{', '.join(S['extras_com_sinal']) if S['extras_com_sinal'] else 'nenhuma'}.")
    vr = [o for o in R['por_secao'] if 'volta_redonda_z90' in o['grupos']]
    def tempos(o, chave):
        return [x[:8] for x in o['eventos']['linha_do_tempo_depois_do_ultimo_voto'] if chave in x]
    susp = [o for o in vr if tempos(o, 'Votação suspensa')]
    ult = [b['ultimo_voto'] for o in vr for b in o['eventos']['blocos'] if b['ultimo_voto']]
    off = [tempos(o, 'Votação suspensa')[0] for o in susp]
    rel = [tempos(o, 'Urna ligada')[-1] for o in susp if tempos(o, 'Urna ligada')]
    w('')
    w('O que isso quer dizer')
    w(f"- Nas {len(todas_secoes(R))} seções conferidas (as do registro e o 1º turno de {R['caso_1t']}), o boletim é igual ao bweb, o RDV é igual ao")
    w('  boletim, o log conta os mesmos votos do comparecimento, não há voto fora da janela, sem habilitação, em menos de 2 segundos ou em')
    w('  rajada, e a assinatura de hardware de cada urna confere. O limite é o de sempre: os quatro arquivos saem do mesmo software; um')
    w('  software adulterado que gravasse tudo coerente não seria visto aqui, e a assinatura de software (SEVIN) não é verificável com o pacote.')
    if vr:
        w(f"- Volta Redonda, zona 90: nenhuma das {len(vr)} seções recebeu voto depois das 17h (último voto entre {min(ult)} e {max(ult)}). Em {len(susp)} delas")
        breve = [o for o in susp if any('17:00:00' <= h <= '17:10:00' for h in tempos(o, 'Urna ligada'))]
        w(f"  a urna foi desligada pela chave entre {min(off)} e {max(off)} (\"Votação suspensa\"; em {len(breve)} houve um religamento breve entre 17h e")
        w(f"  17h10 sem reinício da votação), ficou desligada e foi religada entre {min(rel) if rel else '-'} e")
        w(f"  {max(rel) if rel else '-'} só para encerrar. O \"encerramento depois das 19h15\" do bweb é a hora desse encerramento tardio, não de urna recebendo")
        w('  eleitor. O log não diz quem decidiu; mostra que um único título, que não é de mesário registrado em nenhuma delas, encerrou todas')
        w('  (ver o exploratório no fim).')
    w('')
    w('Descritivo por grupo (2º turno)')
    for g, a in R['agregado_por_grupo'].items():
        w(f"- {g}: {a['secoes_com_log']} seções com log; {a['habilitacoes']} habilitações, {a['M']} sem biometria (M); quem liberou {a['como_M']};"
          f" M = NH do bweb em {a['M_igual_NH_bweb']}; contingência em {a['contingencia']}; votos depois das 17h {a['votos_depois_17h']},"
          f" depois das 19h {a['votos_depois_19h']}; M por hora {a['M_por_hora']}")
    w('')
    w('Seção por seção (horas no relógio da urna; M = liberação sem biometria de eleitor com biometria cadastrada)')
    ordem = [('Volta Redonda, zona 90 (mantidas abertas)', 'volta_redonda_z90'), ('Local de ES|56995|53|978', 'local_ES_56995_53'),
             ('Nomeadas', 'nomeada'), ('As 37 com mais de 80% sem biometria nos dois turnos', 'liberacao_alta_37'),
             ('Extra, fora da letra e do veredito (D16): zona 90 de Volta Redonda encerradas de 19:00:00 a 19:15:00', EXTRA)]
    vistos = set()
    for titulo, g in ordem:
        w(''); w(titulo)
        for o in R['por_secao']:
            if g in o['grupos'] and o['secao'] not in vistos:
                vistos.add(o['secao']); L.extend(linha_secao(o))
            elif g in o['grupos']:
                w(f"* {o['secao']}: ver acima")
    if R.get('caso_1t_resultado'):
        w(''); w(f"1º turno de {R['caso_1t']}")
        L.extend(linha_secao(R['caso_1t_resultado']))
    X = R.get('exploratorio_amostra'); T = R.get('exploratorio_titulos_de_encerramento_F14')
    if X or T:
        w('')
        w('Exploratório, fora do registro (escrito depois de ver o resultado pela letra; contexto, sem veredito)')
    if X:
        b = X['por_uf']['BR']; rj = X['por_uf'].get('RJ', {})
        w(f"- Amostra de {X['logs']} logs do 2º turno: o título digitado para encerrar é de um mesário registrado na própria urna em"
          f" {b.get('titulo_de_mesario_registrado', 0)} de {b.get('com_titulo', 0)} ({fn(100 * b.get('titulo_de_mesario_registrado', 0) / max(b.get('com_titulo', 1), 1), 1)}%);"
          f" no RJ, {rj.get('titulo_de_mesario_registrado', 0)} de {rj.get('com_titulo', 0)}.")
        exc = X.get('amostra_titulo_de_encerramento_fora_dos_registrados', [])
        gm = [e['minutos_ultimo_voto_ao_encerramento'] for e in exc if e['minutos_ultimo_voto_ao_encerramento'] is not None]
        w(f"  As {len(exc)} exceções da amostra: nenhuma com votação suspensa ou urna religada depois do último voto"
          if not any(e['suspensa_depois_do_ultimo'] or e['religada'] for e in exc) else f"  As {len(exc)} exceções da amostra: algumas com suspensão")
        if gm: w(f"  (intervalo entre o último voto e o encerramento de {fn(min(gm), 1)} a {fn(max(gm), 1)} minutos).")
        w(f"- \"Votação suspensa\" depois do último voto: {b.get('votacao_suspensa_depois_do_ultimo_voto', 0)} de {b['logs']} seções da amostra;"
          f" suspensa e encerrada mais de 60 minutos depois do último voto: {b.get('suspensa_e_mais_de_60_min', 0)}. Intervalo mediano entre o último voto e"
          f" o início do encerramento: {fn(X['mediana_min_ultimo_voto_ao_encerramento'].get('BR'), 1)} minutos (RJ: {fn(X['mediana_min_ultimo_voto_ao_encerramento'].get('RJ'), 1)}).")
    if T:
        cnt = collections.Counter(x['quem'] for v in T.values() for x in v)
        multi = {q: sorted({k for k, v in T.items() for x in v if x['quem'] == q}, key=lambda s: int(s.split('|')[3])) for q, n in cnt.items()
                 if len({k for k, v in T.items() for x in v if x['quem'] == q}) > 1}
        proprio = sum(1 for k, v in T.items() if v and all(x['registrado_nesta_secao'] for x in v))
        w(f"- Nas {len(T)} seções do F14 com log: o título que encerrou é de mesário registrado na própria urna em {proprio}.")
        for q, ks in multi.items():
            horas = sorted((x['hora'], k) for k, v in T.items() for x in v if x['quem'] == q)
            locs = collections.Counter(R['volta_redonda']['zona_90'].get(k, {}).get('local') for k in ks)
            w(f"  O mesmo título ({q}) encerrou {len(ks)} seções: {', '.join(ks)}; não é mesário registrado em nenhuma delas;"
              f" locais {dict(locs)}; horas {horas[0][0]} a {horas[-1][0]}:")
            w('    ' + '; '.join(f"{h} {k.split('|')[3]} (local {R['volta_redonda']['zona_90'].get(k, {}).get('local')})" for h, k in horas))
    LV = R.get('exploratorio_locais_volta_redonda')
    if LV:
        for k in ('1104', '1376'):
            if k in LV:
                w(f"- Local {k}: {LV[k]['NM_LOCAL_VOTACAO']}, {LV[k]['DS_ENDERECO']}, {LV[k]['NM_BAIRRO']} ({LV[k]['NR_LATITUDE']}, {LV[k]['NR_LONGITUDE']}).")
        if 'distancia_em_linha_reta_m' in LV:
            w(f"  Distância em linha reta entre os dois locais: {fn(LV['distancia_em_linha_reta_m'], 0)} m.")
    OC = R.get('exploratorio_controle_232')
    if OC:
        w(f"- Controle {CONTROLE} (local 1376, encerrada às 17:00:46; fora do veredito):")
        L.extend(linha_secao(OC))
        tc = (T or {}).get(CONTROLE) or []
        if tc:
            w('    título que encerrou: ' + '; '.join(f"{x['hora']} {x['quem']} (registrado nesta seção: {'sim' if x['registrado_nesta_secao'] else 'não'};"
                                                   f" encerrou outras do F14: {len(x['encerrou_outras_secoes_do_F14'])})" for x in tc))
    RV = R.get('exploratorio_religamento_volta_redonda')
    if RV:
        ordem_ = sorted((v['ultima_vez_ligada'] or '', k.split('|')[3], v['local']) for k, v in RV.items())
        w('- Hora em que cada urna foi religada para encerrar (seção, local): ' + '; '.join(f'{h} {s} ({l})' for h, s, l in ordem_))
    w('')
    w('Desvios declarados (decisões que o registro não fixa, tomadas antes de baixar e de conferir; ver o docstring do script): D1 as 37')
    w('refeitas pela definição do exploratório do F6; D2 local do 2º turno; D3 fuso pela abertura modal e "depois das 19h15" estrito; D4 pleito')
    w('3220 para o 1º turno; D5 download e pacote mais recente; D6 boletim contra o bweb em presidente e governador (senador descritivo); D7 RDV')
    w('contra boletim nos mesmos cargos; D8 log com todos os blocos do pacote; D9 qualquer A2 a A5 conta; D10 qualquer falha de assinatura')
    w('conta; D11 "sem sinal" = nenhum dos cinco itens; D12 a D14 leitura descritiva do log, com mesários em pseudônimo; D15 horas locais.')
    return '\n'.join(L) + '\n'


if __name__ == '__main__':
    if sys.argv[1] == 'lista':
        lista(*sys.argv[2:9])
    elif sys.argv[1] == 'arquivos':
        arquivos(*sys.argv[2:12])
    elif sys.argv[1] == 'exploratorio':
        exploratorio(*sys.argv[2:11])
    elif sys.argv[1] == '--texto':
        print(texto(json.load(open(sys.argv[2]))), end='')
