"""C3 do pré-registro (Adendo 24, commit ca110bb, 03/11/2026 04:24:10 UTC): casos citados no reel, arquivo por arquivo.

Letra do registro
  - Baixar boletim, RDV, log e assinatura de todas as seções do 2º turno de Xique-Xique (BA) e de Coronel José Dias (PI).
    Contar por seção: "Dado digitado não confere", liberações, digitais órfãs, "O eleitor identificado já votou",
    respostas "Todas as pessoas presentes já votaram? SIM" seguidas de retomada da votação depois das 17h. Conferir
    assinatura, boletim contra bweb, RDV contra boletim, votos no log contra comparecimento, e a virada da seção contra as
    outras do mesmo local e do município.
  - Sinal: assinatura inválida, boletim diferente do bweb, RDV diferente do boletim, votos no log diferentes do
    comparecimento, voto computado sem habilitação, ou seção com muitos erros de ano de nascimento cuja virada passe a das
    outras do mesmo local em 5 pontos ou mais.
  O que o reel diz (degravação do Léo): "erra o ano de nascimento até 139 vezes na mesma seção"; no painel, "139 erros em
  Xique-Xique/BA e 79 em Coronel José Dias/PI".

Decisões que o registro não fixa (escritas aqui antes de baixar qualquer arquivo destas seções e antes de abrir qualquer
log, boletim ou voto delas; declaradas como desvio no resultado)
  D1. Municípios: no bweb do 2º turno (zip mais recente de BA e de PI em trab2t/zips2t), NM_MUNICIPIO "XIQUE-XIQUE" (BA,
      CD_MUNICIPIO 39713, zona 68) e "CORONEL JOSÉ DIAS" (PI, CD_MUNICIPIO 10243, zona 13), achados pelo nome (a única
      coincidência de cada nome no zip da UF). Seções: todas as que têm linha do cargo 1 no bweb do 2º turno com esses
      códigos (seção agregada vem dentro da principal, como no bweb e no site do TSE). Conferência: as mesmas chaves na base
      secoes2026.json.gz com o 2º turno.
  D2. Download: scripts/baixar_arquivos_urna.py, pleito 3221, tipos bu,rdv,log,vota, TAXA=1.0, para a pasta nova e vazia
      /home/user/trabalho-eleicao/adendo24/C3_arq; lista, saída da assinatura e o resto do trabalho em
      /home/user/trabalho-eleicao/adendo24/C3_trab (outra pasta nova). python3 -I, rodando de fora da pasta baixada. Se o
      aux.json listar mais de um pacote, vale o de maior índice (o mais recente), e o caso é contado (F14 D5).
  D3. Conferências, com as funções do F14 sem mudança (analisar_F14.conferir_secao, ler_bweb_tudo, ler_assin):
      boletim contra o bweb no presidente (comparecimento, aptos, número da urna, votos por número, branco e nulo; BA e PI
      não tiveram 2º turno de governador), RDV contra boletim (mesmos itens), votos computados no log de 25/10 (todos os
      blocos do pacote, inclusive o log da urna original aninhado quando há contingência) contra o comparecimento do
      presidente no boletim (no bweb, se faltar o boletim), e "voto computado sem habilitação" = A3 do T3
      (decodificar.ler_log: voto computado sem "Eleitor foi habilitado" desde o voto anterior, no mesmo bloco).
      Assinatura: scripts/verificar_assinaturas.py na pasta baixada, saída gravada em C3_trab; inválida = qualquer falha
      listada para a seção ou vsc listado no aux.json e não baixado (F14 D10). Aux sem vsc: "sem arquivo" no item.
      A2, A4 e A5 do T3 (que estavam no sinal do F14, mas não estão no do C3) só são relatados.
  D4. Contagens por seção, no dia 25/10/2026 (e no dia 04/10/2026 do mesmo log, como descritivo, quando o log do pacote
      traz o 1º turno, isto é, quando a urna é a mesma), aplicativo VOTA, todos os blocos do pacote:
      a) "Dado digitado não confere" (linhas). É a contagem que o registro nomeia: erro no dado pessoal pedido na liberação
         manual do eleitor com biometria cadastrada (o dado pedido é o ano de nascimento).
      b) "Ano de nascimento digitado é diferente do cadastro" e "Ano de nascimento inválido" (linhas): o mesmo erro de ano de
         nascimento no eleitor sem biometria cadastrada. O registro não as nomeia; o reel fala em "erros de ano de
         nascimento" sem dizer qual mensagem contou.
         Erros de ano de nascimento = a + b. As duas partes saem separadas, para ver qual delas dá os números do reel.
      c) Liberações: as classes do C2 (analisar_C2_reel.contar, sem mudança), por habilitação e por voto: MI (mesário
         identificado), DG (digital gravada no dia), OR (digital órfã), MX (manual sem nenhuma das três); M = MI+DG+OR+MX é a
         liberação sem biometria de eleitor com biometria cadastrada (o campo QT_ELEI_BIOM_SEM_HABILITACAO do bweb, que é
         conferido ao lado); S = eleitor sem biometria cadastrada; B = biometria do eleitor.
      d) Digitais órfãs: habilitações da classe OR e linhas brutas "Não encontrou digital coletada em nenhum dos arquivos",
         com o score (maior score da janela e se todos são zero, como no C2).
      e) "O eleitor identificado já votou" (linhas) e a maior sequência seguida: ocorrências sem nenhum "Eleitor foi
         habilitado" entre uma e a seguinte, no mesmo bloco; com a hora da primeira e da última da sequência.
      f) "Todas as pessoas presentes já votaram? SIM" (linhas) e, entre elas, as "seguidas de retomada da votação depois das
         17h": depois da resposta, no mesmo bloco, pelo menos um "O voto do eleitor foi computado" às 17:00:00 ou depois
         (hora da urna). Ao lado: respostas seguidas de "Operador cancelou o encerramento da votação" antes do próximo
         "Inicio do Encerramento", votos e habilitações depois de cada resposta, e as respostas NÃO.
  D5. "Muitos erros de ano de nascimento": 20 ou mais erros (a + b, D4) no dia 25/10 na seção. Fixado antes de abrir
      qualquer log das duas cidades; o único log olhado antes foi a amostra nacional, só no vocabulário de mensagens (600
      logs sorteados com random.Random(7): "Dado digitado não confere" em 150 de 600 seções, 225 linhas; "Ano de nascimento
      digitado é diferente do cadastro" em 92 seções, 146 linhas; "Ano de nascimento inválido" em 9 seções, 10 linhas).
      Fora do sinal, a seção com mais erros de cada município também é descrita, mesmo abaixo de 20.
  D6. Virada: v = 100 L2/(L2+R2) - 100 L1/(L1+R1), da base secoes2026 (mesma chave nos dois turnos; L = 13 Lula,
      R = 22 Flávio). Local = UF|município|zona|local do 2º turno (lib.chave_local). Diferença contra o local = v da seção
      menos a média de v das outras seções do mesmo local, ponderada por L2+R2 (o peso de todos os testes do programa);
      contra o município, o mesmo com as outras seções do município. Item do sinal: seção com muitos erros (D5) e diferença
      contra o local de +5,0 pontos ou mais (no sentido de Lula, o do reel). Seção sozinha no local (ou com as outras sem
      voto nos finalistas): item "sem comparação", que não conta como sinal, e a diferença contra o município é relatada.
      Ao lado, sem mudar o item: média simples das outras, |diferença| e a diferença de todas as seções (não só as de muitos
      erros). Agregação diferente entre os turnos (campo agr da base) é marcada.
  D7. Veredito: SINAL se pelo menos uma seção tiver pelo menos um dos seis itens (assinatura inválida, boletim diferente do
      bweb, RDV diferente do boletim, votos no log diferentes do comparecimento, voto computado sem habilitação, muitos
      erros com virada +5 contra o local). Senão, SEM SINAL (o registro só define o sinal; "sem sinal" = nenhum dos seis
      itens em nenhuma seção com arquivo). Arquivo que não vem fica "sem arquivo" no item e é relatado (F14 D11).
  D8. Descrição das seções com muitos erros e da maior de cada município: cada tentativa de habilitação com erro de ano
      de nascimento (janela desde "Identificador do eleitor digitado pelo mesário" até "Eleitor foi habilitado", até
      "Habilitação cancelada..." ou até o identificador seguinte, no mesmo bloco): hora, número de erros de cada tipo,
      desfecho (habilitado, e por qual classe do C2, com o mesário em pseudônimo; cancelada; sem desfecho), hora da
      habilitação, se houve "O voto do eleitor foi computado" depois dela e quando. Quando a tentativa não termina em
      habilitação, também a tentativa seguinte (intervalo em segundos e desfecho): o log não identifica o eleitor, então
      "o mesmo eleitor voltou e foi liberado" é inferência pelo intervalo, e é escrito assim. Por seção: erros por hora,
      tentativas com erro, maior número de erros numa tentativa, desfechos, votos computados depois do último erro, e a
      urna e as contagens do 1º turno na mesma urna.
  D9. Mesários em pseudônimo (A, B, C...) na ordem da primeira aparição do título em qualquer mensagem de mesário do
      aplicativo de votação, comparados como número (F14 D17). Nenhum título, CPF ou número de mais de 6 dígitos sai nas
      saídas.
  D10. Contexto (descritivo, sem veredito): nos 3.897 logs da amostra amostra2t/arq, a distribuição por seção de a, b e
      a + b no dia 25/10 (só contagem de mensagens, sem voto), para situar os números das duas cidades e os do reel
      (139 e 79): percentis, máximo e quantas seções têm 20 ou mais.
  D11. Horas: relógio da urna; BA e PI estão no horário de Brasília.

Acrescentado depois de ver o resultado pela letra (modo exploratorio; não muda o veredito; marcado como exploratório nas
saídas). Motivo: nenhuma contagem por seção do 25/10 dá 139 ou 79, e o maior número de Xique-Xique é 6.
  E1. As três mensagens de erro de ano de nascimento em todos os dias que o log do pacote traz (preparação, 1º turno na
      mesma urna e 2º turno), por seção e por município, e as contagens mais próximas de 139 e de 79.
  E2. O dia 04/10 na mesma urna (o log do 2º turno o traz em todas as seções com a mesma urna): seções com 20 ou mais erros
      nesse dia, com o mesmo resumo do D8.
  E3. "O eleitor identificado já votou": a maior sequência de cada município em cada dia, a hora, os votos computados
      depois da sequência e a hora do próximo "Operador selecionou: Encerrar votação".
  E4. Respostas SIM seguidas de voto: a classe de cada habilitação depois da resposta (classes do C2).
  E5. Todas as seções com |diferença contra o local| de 5 pontos ou mais, com os erros de cada uma (descritivo).

Uso:
  python3 -I analisar_C3_reel.py lista <zips 2T> <secoes2026.json.gz> <parcial.json> <lista.txt>
  python3 -I analisar_C3_reel.py arquivos <parcial.json> <pasta_arq> <assin.json> <zips 2T> <zips 1T> <secoes2026.json.gz>
          <pasta arq da amostra> <saida.json> <saida.txt>
  python3 -I analisar_C3_reel.py exploratorio <saida.json> <pasta_arq> <saida.txt>
  python3 -I analisar_C3_reel.py --texto <saida.json>
"""
import os as _os, sys as _sys
_sys.path.insert(0, _os.path.dirname(_os.path.abspath(__file__)))
import collections, csv, glob, io, json, os, re, sys, time, zipfile
import numpy as np

D1, D2 = '04/10/2026', '25/10/2026'
TURNO = {D1: '1', D2: '2'}
MUNICIPIOS = [('BA', 'XIQUE-XIQUE'), ('PI', 'CORONEL JOSÉ DIAS')]
LIM_MUITOS = 20
LIM_VIRADA = 5.0
H17 = 17 * 3600
REEL = {'BA': 139, 'PI': 79}
RXH = re.compile(r'^(\d\d/\d\d/\d{4}) (\d\d):(\d\d):(\d\d)$')
MSG_ID = 'Identificador do eleitor digitado pelo mesário'
MSG_HAB = 'Eleitor foi habilitado'
MSG_VOTO = 'O voto do eleitor foi computado'
MSG_NAOCONF = 'Dado digitado não confere'
MSG_ANO_DIF = 'Ano de nascimento digitado é diferente do cadastro'
MSG_ANO_INV = 'Ano de nascimento inválido'
MSG_JAVOTOU = 'O eleitor identificado já votou'
MSG_SIM = 'Todas as pessoas presentes já votaram? SIM'
MSG_NAO = 'Todas as pessoas presentes já votaram? NÃO'
MSG_CANC_ENC = 'Operador cancelou o encerramento da votação'
MSG_CANC_HAB = 'Habilitação cancelada'
RX_MES_ANY = re.compile(r'^(?:Pedido de leitura da biometria do mesário (\d+)|Mesário (\d+) é eleitor da seção|Mesário (\d+) registrado'
                        r'|Biometria do mesário (\d+) encontrada.*|Mesário (\d+) habilitou o eleitor)$')
RX_MESOK = re.compile(r'^Mesário (\d+) habilitou o eleitor')


def log(*a):
    print('#', time.strftime('%H:%M:%S'), *a, file=sys.stderr, flush=True)


def hms(s):
    return None if s is None else f'{s // 3600:02d}:{s % 3600 // 60:02d}:{s % 60:02d}'


def pasta_secao(pasta, k):
    uf, mun, zona, sec = k.split('|')
    return os.path.join(pasta, uf.lower(), f'{int(mun):05d}', f'{int(zona):04d}', f'{int(sec):04d}')


def ordem(k):
    uf, m, z, s = k.split('|')
    return (uf, int(m), int(z), int(s))


# ================================================================ parte 1: lista
def lista(zips2, arq_secoes, parcial, lista_txt):
    from lib import carregar
    out = {'municipios': {}, 'secoes': []}
    for uf, nome in MUNICIPIOS:
        z = zipfile.ZipFile(sorted(glob.glob(os.path.join(zips2, f'bweb_2t_{uf}_*.zip')))[-1])
        csvn = [x for x in z.namelist() if x.lower().endswith('.csv')][0]
        cods = collections.Counter(); secs = {}
        with z.open(csvn) as fh:
            rd = csv.reader(io.TextIOWrapper(fh, encoding='latin1', newline=''), delimiter=';')
            cab = next(rd); ix = {c.strip().replace('SG_ UF', 'SG_UF'): i for i, c in enumerate(cab)}
            for r in rd:
                if r[ix['NM_MUNICIPIO']] != nome:
                    continue
                cods[r[ix['CD_MUNICIPIO']]] += 1
                if r[ix['CD_CARGO_PERGUNTA']] != '1':
                    continue
                k = f"{uf}|{int(r[ix['CD_MUNICIPIO']])}|{int(r[ix['NR_ZONA']])}|{int(r[ix['NR_SECAO']])}"
                secs.setdefault(k, {'local': r[ix['NR_LOCAL_VOTACAO']], 'agregadas': r[ix['DS_SECOES_AGREGADAS']],
                                    'tipo_urna': r[ix['DS_TIPO_URNA']], 'junta': r[ix['NR_JUNTA_APURADORA']]})
        out['municipios'][f'{uf}|{nome}'] = {'codigos_no_bweb': dict(cods), 'secoes': len(secs),
                                             'zonas': sorted({int(k.split('|')[2]) for k in secs}),
                                             'locais': len({v['local'] for v in secs.values()}),
                                             'com_agregadas': sum(1 for v in secs.values() if v['agregadas'] not in ('', '#NULO#')),
                                             'tipos_urna': dict(collections.Counter(v['tipo_urna'] for v in secs.values()))}
        out['secoes'] += sorted(secs, key=ordem)
        out.setdefault('bweb_2t', {}).update(secs)
    base = carregar(arq_secoes)
    pref = {'|'.join(k.split('|')[:2]) for k in out['secoes']}
    na_base = sorted((k for k in base if '|'.join(k.split('|')[:2]) in pref and '2' in base[k]), key=ordem)
    out['conferencia_base'] = {'na_base_com_2T': len(na_base), 'no_bweb': len(out['secoes']),
                               'so_no_bweb': [k for k in out['secoes'] if k not in base],
                               'so_na_base': [k for k in na_base if k not in out['secoes']]}
    json.dump(out, open(parcial, 'w'), ensure_ascii=False, indent=1)
    with open(lista_txt, 'w') as fh:
        for k in out['secoes']:
            fh.write(k + '\n')
    log('lista:', {m: v['secoes'] for m, v in out['municipios'].items()}, out['conferencia_base'])


# ================================================================ parte 2: leitura do log (D4, D8, D9)
def eventos_dia(blocos, dia):
    """Por bloco, as linhas do aplicativo VOTA do dia: (segundos, nível, mensagem)."""
    out = []
    for bl in blocos:
        ev = []
        for l in bl:
            x = l.split('\t')
            if len(x) < 5 or not x[0].startswith(dia) or x[3] != 'VOTA':
                continue
            m = RXH.match(x[0])
            if m:
                ev.append((int(m.group(2)) * 3600 + int(m.group(3)) * 60 + int(m.group(4)), x[1], x[4]))
        out.append(ev)
    return out


def pseudonimos(evb):
    """Títulos de mesário -> letra, pela ordem da primeira aparição em qualquer mensagem de mesário (D9)."""
    mp = {}
    for ev in evb:
        for t, nv, m in ev:
            a = RX_MES_ANY.match(m)
            if a:
                tt = int(next(g for g in a.groups() if g))
                if tt not in mp:
                    i = len(mp); mp[tt] = chr(65 + i) if i < 26 else f'Z{i}'
    return mp


def eh_erro_ano(m):
    return m == MSG_NAOCONF or m.startswith(MSG_ANO_DIF) or m.startswith(MSG_ANO_INV)


def ler_c3(caminho, dia):
    """Contagens do D4 e tentativas de habilitação do D8 num dia, somando os blocos do pacote."""
    from decodificar import _linhas_log
    from analisar_C2_reel import classe_da_janela
    evb = eventos_dia(_linhas_log(caminho), dia)
    mp = pseudonimos(evb)
    r = {'nao_confere': 0, 'ano_diferente': 0, 'ano_invalido': 0, 'ja_votou': 0, 'ja_votou_maior_seq': 0,
         'ja_votou_maior_seq_horas': None, 'sim': 0, 'nao': 0, 'sim_retomada_17h': 0, 'sim_com_voto_depois': 0,
         'sim_cancelado': 0, 'sim_detalhe': [], 'erros_por_hora': collections.Counter(), 'votos': 0, 'habilitacoes': 0,
         'blocos_com_evento': sum(1 for ev in evb if ev), 'mesarios_no_log': len(mp)}
    tent = []
    for bi, ev in enumerate(evb):
        if not ev:
            continue
        votos_t = [t for t, nv, m in ev if m == MSG_VOTO]
        r['votos'] += len(votos_t); r['habilitacoes'] += sum(1 for t, nv, m in ev if m == MSG_HAB)
        seq = 0; ini = None
        for i, (t, nv, m) in enumerate(ev):
            if m == MSG_NAOCONF: r['nao_confere'] += 1
            elif m.startswith(MSG_ANO_DIF): r['ano_diferente'] += 1
            elif m.startswith(MSG_ANO_INV): r['ano_invalido'] += 1
            if eh_erro_ano(m): r['erros_por_hora'][f'{t // 3600:02d}h'] += 1
            if m == MSG_JAVOTOU:
                r['ja_votou'] += 1
                if seq == 0: ini = t
                seq += 1
                if seq > r['ja_votou_maior_seq']:
                    r['ja_votou_maior_seq'] = seq; r['ja_votou_maior_seq_horas'] = [hms(ini), hms(t), bi]
            elif m == MSG_HAB:
                seq = 0
            if m == MSG_NAO: r['nao'] += 1
            if m == MSG_SIM:
                r['sim'] += 1
                depois = ev[i + 1:]
                vd = [u for u, _, mm in depois if mm == MSG_VOTO]
                hd = [u for u, _, mm in depois if mm == MSG_HAB]
                prox = next((mm for u, _, mm in depois if mm in (MSG_CANC_ENC, 'Inicio do Encerramento', 'Início do Encerramento',
                                                                  'Operador selecionou: Encerrar votação')
                             or mm.startswith('Título digitado para encerramento')), None)
                canc = prox == MSG_CANC_ENC
                ret17 = any(u >= H17 for u in vd)
                r['sim_cancelado'] += canc; r['sim_com_voto_depois'] += bool(vd); r['sim_retomada_17h'] += ret17
                r['sim_detalhe'].append({'bloco': bi, 'hora': hms(t), 'cancelou_o_encerramento': canc,
                                         'votos_depois': len(vd), 'habilitacoes_depois': len(hd),
                                         'primeiro_voto_depois': hms(vd[0]) if vd else None,
                                         'ultimo_voto_depois': hms(vd[-1]) if vd else None, 'retomada_depois_das_17h': ret17})
        # tentativas de habilitação (D8)
        cur = None
        def fecha(c, desf, t_fim):
            c['desfecho'] = desf; c['fim'] = t_fim; tent.append(c)
        for i, (t, nv, m) in enumerate(ev):
            if m == MSG_ID:
                if cur is not None:
                    fecha(cur, 'sem desfecho (nova identificação)', cur['ult'])
                cur = {'bloco': bi, 'inicio': t, 'win': [], 'nao_confere': 0, 'ano_dif': 0, 'ano_inv': 0, 'ult': t,
                       'hora_erros': []}
            if cur is None:
                continue
            cur['win'].append(m); cur['ult'] = t
            if m == MSG_NAOCONF: cur['nao_confere'] += 1; cur['hora_erros'].append(t)
            elif m.startswith(MSG_ANO_DIF): cur['ano_dif'] += 1; cur['hora_erros'].append(t)
            elif m.startswith(MSG_ANO_INV): cur['ano_inv'] += 1; cur['hora_erros'].append(t)
            if m == MSG_HAB:
                cl, sub, bsl, n_aut = classe_da_janela(cur['win'])
                mm_ = [RX_MESOK.match(w) for w in cur['win']]
                tit = [int(a.group(1)) for a in mm_ if a]
                cur['classe'] = cl; cur['mesario'] = mp.get(tit[-1]) if tit else None; cur['hora_hab'] = t
                vt = None
                for u, _, mm in ev[i + 1:]:
                    if mm == MSG_VOTO: vt = u; break
                    if mm == MSG_ID or mm == MSG_HAB: break
                cur['hora_voto'] = vt
                fecha(cur, 'habilitado', t); cur = None
            elif m.startswith(MSG_CANC_HAB):
                cur['msg_cancelamento'] = m
                fecha(cur, 'cancelada', t); cur = None
            elif m == MSG_JAVOTOU:
                fecha(cur, 'eleitor já votou', t); cur = None
            elif m.startswith('Eleitor impedido') or m == 'Justificativa recebida':
                fecha(cur, m, t); cur = None
        if cur is not None:
            fecha(cur, 'sem desfecho (fim do bloco)', cur['ult'])
    # tentativas com erro e a tentativa seguinte
    tent.sort(key=lambda c: (c['bloco'], c['inicio']))
    com_erro = []
    for j, c in enumerate(tent):
        n = c['nao_confere'] + c['ano_dif'] + c['ano_inv']
        if not n:
            continue
        e = {'bloco': c['bloco'], 'inicio': hms(c['inicio']), 'primeiro_erro': hms(c['hora_erros'][0]),
             'ultimo_erro': hms(c['hora_erros'][-1]), 'erros': n, 'nao_confere': c['nao_confere'],
             'ano_diferente': c['ano_dif'], 'ano_invalido': c['ano_inv'], 'desfecho': c['desfecho'],
             'classe': c.get('classe'), 'mesario': c.get('mesario'), 'hora_habilitacao': hms(c.get('hora_hab')),
             'hora_voto': hms(c.get('hora_voto')), 'votou': c.get('hora_voto') is not None,
             'cancelamento': c.get('msg_cancelamento')}
        if c['desfecho'] != 'habilitado':
            nx = tent[j + 1] if j + 1 < len(tent) and tent[j + 1]['bloco'] == c['bloco'] else None
            if nx:
                e['seguinte'] = {'intervalo_s': nx['inicio'] - c['fim'], 'desfecho': nx['desfecho'], 'classe': nx.get('classe'),
                                 'mesario': nx.get('mesario'), 'erros': nx['nao_confere'] + nx['ano_dif'] + nx['ano_inv'],
                                 'votou': nx.get('hora_voto') is not None, 'hora_voto': hms(nx.get('hora_voto'))}
        com_erro.append(e)
    r['tentativas'] = len(tent)
    r['tentativas_com_erro'] = com_erro
    r['erros_ano'] = r['nao_confere'] + r['ano_diferente'] + r['ano_invalido']
    r['erros_por_hora'] = dict(sorted(r['erros_por_hora'].items()))
    # resumo das tentativas com erro
    rs = collections.Counter(); por_cl = collections.Counter(); por_mes = collections.Counter()
    for e in com_erro:
        rs[e['desfecho']] += 1
        if e['desfecho'] == 'habilitado':
            por_cl[e['classe']] += 1
            if e['mesario']: por_mes[e['mesario']] += 1
            rs['habilitado_e_votou'] += e['votou']
        elif e.get('seguinte'):
            s = e['seguinte']
            rs['nao_habilitado_e_a_seguinte_habilitada_em_ate_120s'] += (s['desfecho'] == 'habilitado' and s['intervalo_s'] <= 120)
    r['resumo_tentativas_com_erro'] = {'n': len(com_erro), 'desfechos': dict(rs), 'classe_dos_habilitados': dict(por_cl),
                                       'mesario_dos_habilitados_MI': dict(por_mes),
                                       'maior_numero_de_erros_numa_tentativa': max((e['erros'] for e in com_erro), default=0)}
    ult_err = max((c['hora_erros'][-1] for c in tent if c['hora_erros']), default=None)
    r['ultimo_erro'] = hms(ult_err)
    r['votos_depois_do_ultimo_erro'] = (sum(1 for ev in evb for t, nv, m in ev if m == MSG_VOTO and t > ult_err)
                                       if ult_err is not None else None)
    r['primeiro_voto'] = hms(min((t for ev in evb for t, nv, m in ev if m == MSG_VOTO), default=None))
    r['ultimo_voto'] = hms(max((t for ev in evb for t, nv, m in ev if m == MSG_VOTO), default=None))
    return r


def contar_contexto(caminho):
    """D10: só as mensagens de erro de ano de nascimento no dia 25/10 de um log da amostra."""
    from decodificar import _linhas_log
    a = b = 0
    try:
        for bl in _linhas_log(caminho):
            for l in bl:
                x = l.split('\t')
                if len(x) < 5 or not x[0].startswith(D2) or x[3] != 'VOTA':
                    continue
                if x[4] == MSG_NAOCONF: a += 1
                elif x[4].startswith(MSG_ANO_DIF) or x[4].startswith(MSG_ANO_INV): b += 1
    except Exception as e:
        return caminho, None
    return caminho, (a, b)


# ================================================================ parte 3: arquivos
def media_pond(xs):
    w = sum(p for v, p in xs)
    return (sum(v * p for v, p in xs) / w) if w > 0 else None


def viradas(chaves, base):
    """D6: virada de cada seção e diferença contra as outras do local e do município."""
    from lib import chave_local
    V = {}
    for k in chaves:
        s = base.get(k, {})
        a, b = s.get('1'), s.get('2')
        if not a or not b or a['L'] + a['R'] <= 0 or b['L'] + b['R'] <= 0:
            V[k] = None; continue
        V[k] = {'v': 100 * b['L'] / (b['L'] + b['R']) - 100 * a['L'] / (a['L'] + a['R']), 'w': b['L'] + b['R'],
                'loc': chave_local(k, b), 'mun': '|'.join(k.split('|')[:2]),
                'fatia_1T': 100 * a['L'] / (a['L'] + a['R']), 'fatia_2T': 100 * b['L'] / (b['L'] + b['R']),
                'agregacao_difere': a.get('agr') != b.get('agr'), 'agr_1T': a.get('agr'), 'agr_2T': b.get('agr'),
                'comp_1T': a['comp'], 'comp_2T': b['comp'], 'urna_1T': a['urna'], 'urna_2T': b['urna']}
    out = {}
    for k in chaves:
        x = V[k]
        if x is None:
            out[k] = None; continue
        ol = [(V[j]['v'], V[j]['w']) for j in chaves if j != k and V[j] and V[j]['loc'] == x['loc']]
        om = [(V[j]['v'], V[j]['w']) for j in chaves if j != k and V[j] and V[j]['mun'] == x['mun']]
        ml, mm = media_pond(ol), media_pond(om)
        out[k] = dict(x, outras_no_local=len(ol), virada_outras_local=ml,
                      virada_outras_local_simples=(sum(v for v, p in ol) / len(ol)) if ol else None,
                      dif_local=(x['v'] - ml) if ml is not None else None, virada_outras_municipio=mm,
                      dif_municipio=(x['v'] - mm) if mm is not None else None)
    return out


def ultimo(fs, suf):
    xs = [f for f in fs if f.endswith(suf)]
    return sorted(xs, key=lambda q: int(q.split('-')[0]))[-1] if xs else None


def arquivos(parcial, pasta, assin, zips2, zips1, arq_secoes, pasta_amostra, saida_json, saida_txt):
    from multiprocessing import Pool
    from lib import carregar
    from analisar_F14 import conferir_secao, ler_bweb_tudo, ler_assin
    from analisar_C2_reel import contar
    P = json.load(open(parcial))
    chaves = P['secoes']
    A, fp = ler_assin(assin)
    bw2 = ler_bweb_tudo(zips2, '2t', chaves)
    bw1 = ler_bweb_tudo(zips1, '1t', chaves)
    base = carregar(arq_secoes)
    VV = viradas(chaves, base)
    res = []
    for k in chaves:
        o = conferir_secao(k, pasta, D2, bw2, bw1, base.get(k, {}).get('2'), fp, 2)
        d = pasta_secao(pasta, k)
        fs = sorted(os.listdir(d)) if os.path.isdir(d) else []
        flog = ultimo(fs, '-log.jez')
        c = {'secao': k, 'municipio': P['bweb_2t'][k] and next(m for m in P['municipios'] if m.startswith(k.split('|')[0] + '|')),
             'local_bweb': P['bweb_2t'][k]['local'], 'faltando': o['faltando'], 'sem_aux': o['sem_aux'],
             'pacotes': (o.get('aux') or {}).get('pacotes'),
             'bu_igual_bweb': o.get('bu_igual_bweb'), 'bu_vs_bweb_diferencas': o.get('bu_vs_bweb_diferencas'),
             'bu_igual_base_secoes2026': o.get('bu_igual_base_secoes2026'),
             'rdv_igual_bu': o.get('rdv_igual_bu'), 'rdv_vs_bu_diferencas': o.get('rdv_vs_bu_diferencas'),
             'votos_log_igual_comparecimento': o.get('votos_log_igual_comparecimento'),
             'assinatura_ok': o.get('assinatura_ok'), 'assinatura_falhas': o.get('assinatura_falhas'),
             'vsc_listado_nao_baixado': o.get('vsc_listado_nao_baixado'),
             'T3': o.get('T3'), 'M_log_contra_NH_bweb': o.get('M_log_contra_NH_bweb'),
             'M_log_outro_dia_contra_NH_bweb': o.get('M_log_outro_dia_contra_NH_bweb'),
             'liberacoes_F6': o.get('liberacoes'), 'contingencia_F6': o.get('contingencia_F6'),
             'blocos_de_log': o.get('blocos_de_log'),
             'eventos': {x: (o.get('eventos') or {}).get(x) for x in ('blocos', 'mesarios_que_liberaram', 'mesarios_no_log',
                                                                     'mesarios_registrados', 'eventos_de_encerramento',
                                                                     'quem_encerrou', 'linha_do_tempo_depois_do_ultimo_voto',
                                                                     'eventos_raros_resumo', 'modelo', 'modo_de_carga')},
             'bweb': (o.get('bweb') or {}).get('1'), 'bweb_1T': o.get('bweb_outro_turno_presidente'),
             'base': {t: {x: y for x, y in base.get(k, {}).get(t, {}).items() if x != 'cand'} for t in ('1', '2') if t in base.get(k, {})},
             'virada': VV.get(k)}
        if c['bweb']:
            c['bweb'] = {x: y for x, y in c['bweb'].items() if x not in ('votos',)} | {'votos': c['bweb'].get('votos')}
        if flog:
            cam = os.path.join(d, flog)
            _, c2 = contar(cam)
            for t in ('1', '2'):
                q = c2[t]
                c2[t] = {x: q[x] for x in ('hab', 'votos', 'computados', 'voto_sem_hab', 'hab_sem_voto', 'sub_MI', 'B_sem_linha',
                                           'linhas_OR', 'linhas_DG', 'linhas_MI', 'nao_confere', 'OR_todos_zero', 'OR_sem_score',
                                           'OR_por_hora', 'contingencia', 'n_mesarios', 'urnas', 'blocos_com_voto')}
                q2 = q.get('OR_max_score') or []
                c2[t]['OR_max_score_max'] = max(q2) if q2 else None
                c2[t]['M'] = sum(c2[t]['hab'][x] for x in ('MI', 'DG', 'OR', 'MX'))
            c['C2'] = c2
            c['log'] = {TURNO[D2]: ler_c3(cam, D2), TURNO[D1]: ler_c3(cam, D1)}
        # itens do sinal (D7)
        it = []
        if c['assinatura_ok'] is False: it.append('assinatura inválida')
        if c['bu_igual_bweb'] is False: it.append('boletim diferente do bweb')
        if c['rdv_igual_bu'] is False: it.append('RDV diferente do boletim')
        if c['votos_log_igual_comparecimento'] is False: it.append('votos no log diferentes do comparecimento')
        if (c['T3'] or {}).get('A3_sem_habilitacao'): it.append('voto computado sem habilitação')
        lg2 = (c.get('log') or {}).get('2')
        c['muitos_erros'] = bool(lg2 and lg2['erros_ano'] >= LIM_MUITOS)
        vk = c['virada']
        if c['muitos_erros']:
            if vk is None or vk['dif_local'] is None:
                c['item_virada'] = 'sem comparação'
            else:
                c['item_virada'] = vk['dif_local'] >= LIM_VIRADA
                if c['item_virada']: it.append('muitos erros de ano de nascimento e virada +5 contra o local')
        c['sinais'] = it
        res.append(c)
        log(k, 'erros', lg2 and lg2['erros_ano'], 'sinais', it)
    # contexto da amostra (D10)
    logs = sorted(glob.glob(os.path.join(pasta_amostra, '*/*/*/*/*-log.jez')))
    with Pool(4) as pool:
        cx = dict(pool.map(contar_contexto, logs, chunksize=25))
    # uma seção por pasta: o log de maior índice
    porsec = {}
    for cam, v in cx.items():
        dd = os.path.dirname(cam)
        if v is None: continue
        i = int(os.path.basename(cam).split('-')[0])
        if dd not in porsec or i > porsec[dd][0]:
            porsec[dd] = (i, v)
    va = np.array([v[1][0] for v in porsec.values()]); vb = np.array([v[1][1] for v in porsec.values()]); vs = va + vb
    def dist(x):
        return {'secoes': int(len(x)), 'media': float(x.mean()), 'p50': float(np.percentile(x, 50)), 'p90': float(np.percentile(x, 90)),
                'p99': float(np.percentile(x, 99)), 'p999': float(np.percentile(x, 99.9)), 'max': int(x.max()),
                'com_zero': int((x == 0).sum()), 'com_10_ou_mais': int((x >= 10).sum()), 'com_20_ou_mais': int((x >= LIM_MUITOS).sum())}
    contexto = {'logs': len(logs), 'secoes_lidas': len(porsec), 'nao_confere': dist(va), 'ano_diferente_ou_invalido': dist(vb),
                'erros_ano': dist(vs),
                'maiores_erros_ano': sorted(([int(a + b), int(a), int(b), '|'.join(dd.split('/')[-4:])] for dd, (i, (a, b)) in porsec.items()),
                                            reverse=True)[:15]}
    # resumo
    todas = res
    com_sinal = [c['secao'] for c in todas if c['sinais']]
    def cnt(campo, val=True): return sum(1 for c in todas if c.get(campo) is val)
    def den(campo): return sum(1 for c in todas if c.get(campo) is not None)
    resumo = {'secoes': len(todas), 'bu_igual_bweb': [cnt('bu_igual_bweb'), den('bu_igual_bweb')],
              'rdv_igual_bu': [cnt('rdv_igual_bu'), den('rdv_igual_bu')],
              'votos_log_igual_comparecimento': [cnt('votos_log_igual_comparecimento'), den('votos_log_igual_comparecimento')],
              'assinatura_ok': [cnt('assinatura_ok'), den('assinatura_ok')],
              'voto_sem_habilitacao_A3': sum((c['T3'] or {}).get('A3_sem_habilitacao', 0) for c in todas),
              'outras_T3': {a: sum((c['T3'] or {}).get(a, 0) for c in todas) for a in ('A2_antes', 'A2_depois', 'A4_menos_2s', 'A5_rajadas')},
              'secoes_com_muitos_erros': [c['secao'] for c in todas if c['muitos_erros']],
              'item_virada': {c['secao']: c.get('item_virada') for c in todas if c['muitos_erros']},
              'faltando': {c['secao']: c['faltando'] for c in todas if c['faltando']},
              'sem_aux': [c['secao'] for c in todas if c['sem_aux']],
              'pacotes_multiplos': [c['secao'] for c in todas if (c['pacotes'] or 1) > 1]}
    # por município
    pm = {}
    for mun in P['municipios']:
        xs = [c for c in todas if c['municipio'] == mun and c.get('log')]
        def soma(t, f): return sum(f(c['log'][t]) for c in xs if c['log'].get(t))
        def soma2(t, f): return sum(f(c['C2'][t]) for c in xs)
        pm[mun] = {'secoes': sum(1 for c in todas if c['municipio'] == mun), 'com_log': len(xs)}
        for t in ('2', '1'):
            pm[mun][t] = {'votos_log': soma(t, lambda r: r['votos']), 'nao_confere': soma(t, lambda r: r['nao_confere']),
                          'ano_diferente': soma(t, lambda r: r['ano_diferente']), 'ano_invalido': soma(t, lambda r: r['ano_invalido']),
                          'erros_ano': soma(t, lambda r: r['erros_ano']), 'ja_votou': soma(t, lambda r: r['ja_votou']),
                          'sim': soma(t, lambda r: r['sim']), 'sim_retomada_17h': soma(t, lambda r: r['sim_retomada_17h']),
                          'sim_cancelado': soma(t, lambda r: r['sim_cancelado']),
                          'M': soma2(t, lambda r: r['M']), 'OR': soma2(t, lambda r: r['hab']['OR']),
                          'DG': soma2(t, lambda r: r['hab']['DG']), 'MI': soma2(t, lambda r: r['hab']['MI']),
                          'S': soma2(t, lambda r: r['hab']['S']), 'B': soma2(t, lambda r: r['hab']['B']),
                          'secoes_com_o_dia': sum(1 for c in xs if c['log'][t]['votos'] > 0),
                          'max_erros_ano': max(((c['log'][t]['erros_ano'], c['secao']) for c in xs), default=None),
                          'max_nao_confere': max(((c['log'][t]['nao_confere'], c['secao']) for c in xs), default=None),
                          'max_ano_diferente': max(((c['log'][t]['ano_diferente'], c['secao']) for c in xs), default=None),
                          'max_ja_votou_seq': max(((c['log'][t]['ja_votou_maior_seq'], c['secao']) for c in xs), default=None)}
        vv = [c['virada'] for c in todas if c['municipio'] == mun and c['virada']]
        pm[mun]['virada_municipio_pond'] = media_pond([(v['v'], v['w']) for v in vv])
    # números do reel: onde aparecem 139 e 79
    achados = []
    for c in todas:
        for t in ('2', '1'):
            r = (c.get('log') or {}).get(t)
            if not r: continue
            for campo in ('nao_confere', 'ano_diferente', 'erros_ano', 'ja_votou', 'tentativas'):
                if r[campo] in (139, 79): achados.append([c['secao'], t, campo, r[campo]])
            for campo, v in (c.get('C2') or {}).get(t, {}).get('hab', {}).items():
                if v in (139, 79): achados.append([c['secao'], t, 'hab_' + campo, v])
            if (c['C2'][t]['M'] if c.get('C2') else None) in (139, 79): achados.append([c['secao'], t, 'M', c['C2'][t]['M']])
    descrever = set(resumo['secoes_com_muitos_erros'])
    for mun, x in pm.items():
        if x['2']['max_erros_ano']: descrever.add(x['2']['max_erros_ano'][1])
        if x['2']['max_nao_confere']: descrever.add(x['2']['max_nao_confere'][1])
    out = {'teste': 'C3 (Adendo 24): casos citados no reel, arquivo por arquivo',
           'registro': 'PRE-REGISTRO-2026-10-26.md, Adendo 24, commit ca110bb (03/11/2026 04:24:10 UTC)',
           'municipios': P['municipios'], 'conferencia_base': P['conferencia_base'],
           'assinaturas': {'contagem': A.get('contagem'), 'falhas': A.get('falhas'), 'emissores': A.get('emissores'),
                           'modo': A.get('modo_da_assinatura'), 'validade': A.get('validade_certificados'),
                           'chaves_software': A.get('chaves_software'), 'tipos_de_chave': A.get('tipos_de_chave')},
           'resumo': resumo, 'secoes_com_sinal': com_sinal, 'veredito': 'SINAL' if com_sinal else 'SEM SINAL',
           'por_municipio': pm, 'numeros_do_reel_encontrados': achados, 'secoes_descritas': sorted(descrever, key=ordem),
           'contexto_amostra': contexto, 'por_secao': res}
    json.dump(out, open(saida_json, 'w'), ensure_ascii=False, indent=1, default=str)
    open(saida_txt, 'w').write(texto(out))
    log('veredito', out['veredito'], com_sinal)


# ================================================================ exploratório (E1 a E5, depois do resultado pela letra)
def todos_os_dias(caminho):
    from decodificar import _linhas_log
    c = collections.defaultdict(collections.Counter)
    for bl in _linhas_log(caminho):
        for l in bl:
            x = l.split('\t')
            if len(x) < 5 or x[3] != 'VOTA':
                continue
            m = x[4]; d = x[0][:10]
            if m == MSG_NAOCONF: c[d]['nao_confere'] += 1
            elif m.startswith(MSG_ANO_DIF): c[d]['ano_diferente'] += 1
            elif m.startswith(MSG_ANO_INV): c[d]['ano_invalido'] += 1
    return {d: dict(v, erros=sum(v.values())) for d, v in sorted(c.items())}


def depois_de(caminho, dia, hora):
    """Votos computados depois de uma hora (todos os blocos) e a hora do próximo pedido de encerramento."""
    from decodificar import _linhas_log
    h = int(hora[:2]) * 3600 + int(hora[3:5]) * 60 + int(hora[6:8])
    evb = eventos_dia(_linhas_log(caminho), dia)
    vot = sum(1 for ev in evb for t, nv, m in ev if m == MSG_VOTO and t > h)
    enc = min((t for ev in evb for t, nv, m in ev if m == 'Operador selecionou: Encerrar votação' and t > h), default=None)
    return vot, hms(enc)


def classes_depois(caminho, dia, hora):
    """E4: classe (C2) de cada habilitação depois de uma hora, com a hora do voto."""
    from decodificar import _linhas_log
    from analisar_C2_reel import classe_da_janela
    h = int(hora[:2]) * 3600 + int(hora[3:5]) * 60 + int(hora[6:8])
    out = []
    for ev in eventos_dia(_linhas_log(caminho), dia):
        win = []
        for i, (t, nv, m) in enumerate(ev):
            if m == MSG_ID: win = []
            win.append(m)
            if m == MSG_HAB:
                if t > h:
                    vt = next((u for u, _, mm in ev[i + 1:] if mm == MSG_VOTO), None)
                    out.append({'hora_habilitacao': hms(t), 'classe': classe_da_janela(win)[0], 'hora_voto': hms(vt)})
                win = []
    return out


def exploratorio(saida_json, pasta, saida_txt):
    R = json.load(open(saida_json))
    X = {'nota': 'escrito depois de ver o resultado pela letra; contexto, sem veredito'}
    cam = {}
    for c in R['por_secao']:
        d = pasta_secao(pasta, c['secao'])
        fl = ultimo(sorted(os.listdir(d)), '-log.jez') if os.path.isdir(d) else None
        if fl: cam[c['secao']] = os.path.join(d, fl)
    # E1
    td = {k: todos_os_dias(v) for k, v in cam.items()}
    tot = {k: sum(x['erros'] for x in v.values()) for k, v in td.items()}
    mun = collections.defaultdict(lambda: collections.defaultdict(collections.Counter))
    for k, v in td.items():
        for d, x in v.items():
            mun['|'.join(k.split('|')[:2])][d].update(x)
    cand = []
    for k, v in td.items():
        cand.append((tot[k], f'{k} todos os dias'))
        for d, x in v.items():
            for campo, q in x.items():
                cand.append((q, f'{k} {d} {campo}'))
    for m, v in mun.items():
        cand.append((sum(x['erros'] for x in v.values()), f'município {m} todos os dias'))
        for d, x in v.items():
            for campo, q in x.items():
                cand.append((q, f'município {m} {d} {campo}'))
    X['E1'] = {'por_secao_todos_os_dias': {k: td[k] for k in sorted(td, key=lambda k: -tot[k])[:8]},
               'total_por_secao_todos_os_dias_top': sorted(([q, k] for k, q in tot.items()), reverse=True)[:8],
               'por_municipio': {m: {d: dict(x) for d, x in sorted(v.items())} for m, v in mun.items()},
               'mais_proximos_de_139': sorted(cand, key=lambda z: (abs(z[0] - 139), z[1]))[:5],
               'mais_proximos_de_79': sorted(cand, key=lambda z: (abs(z[0] - 79), z[1]))[:5],
               'igual_a_139_ou_79': [z for z in cand if z[0] in (139, 79)]}
    # E2
    e2 = []
    for c in R['por_secao']:
        l1 = (c.get('log') or {}).get('1')
        if l1 and l1['erros_ano'] >= LIM_MUITOS:
            e2.append({'secao': c['secao'], 'urna_igual': (c.get('virada') or {}).get('urna_1T') == (c.get('virada') or {}).get('urna_2T'),
                       'votos': l1['votos'], 'erros_ano': l1['erros_ano'], 'nao_confere': l1['nao_confere'],
                       'ano_diferente': l1['ano_diferente'], 'ano_invalido': l1['ano_invalido'], 'erros_por_hora': l1['erros_por_hora'],
                       'resumo': l1['resumo_tentativas_com_erro'], 'liberacoes': c['C2']['1']['hab'],
                       'ultimo_erro': l1['ultimo_erro'], 'votos_depois_do_ultimo_erro': l1['votos_depois_do_ultimo_erro'],
                       'erros_25_10': c['log']['2']['erros_ano']})
    X['E2'] = e2
    # E3
    e3 = {}
    for m in R['municipios']:
        for t, dia in (('2', D2), ('1', D1)):
            xs = [c for c in R['por_secao'] if c['municipio'] == m and (c.get('log') or {}).get(t)]
            top = sorted(xs, key=lambda c: -c['log'][t]['ja_votou_maior_seq'])[:3]
            lst = []
            for c in top:
                r = c['log'][t]
                if not r['ja_votou_maior_seq']: continue
                ini, fim, bl = r['ja_votou_maior_seq_horas']
                vot, enc = depois_de(cam[c['secao']], dia, fim)
                lst.append({'secao': c['secao'], 'sequencia': r['ja_votou_maior_seq'], 'de': ini, 'ate': fim, 'total_no_dia': r['ja_votou'],
                            'votos_depois_da_sequencia': vot, 'proximo_pedido_de_encerramento': enc})
            e3[f'{m} {TURNO[dia]}T'] = lst
    X['E3'] = e3
    # E4
    e4 = []
    for c in R['por_secao']:
        for t, dia in (('2', D2), ('1', D1)):
            for s in ((c.get('log') or {}).get(t) or {}).get('sim_detalhe', []):
                if s['votos_depois']:
                    e4.append({'secao': c['secao'], 'turno': t, 'sim': s['hora'], 'cancelou': s['cancelou_o_encerramento'],
                               'habilitacoes_depois': classes_depois(cam[c['secao']], dia, s['hora'])})
    X['E4'] = e4
    # E5
    X['E5'] = [{'secao': c['secao'], 'dif_local': c['virada']['dif_local'], 'outras_no_local': c['virada']['outras_no_local'],
                'virada': c['virada']['v'], 'erros_25_10': c['log']['2']['erros_ano'], 'M': c['C2']['2']['M'], 'OR': c['C2']['2']['hab']['OR'],
                'votos': c['log']['2']['votos']}
               for c in R['por_secao'] if c.get('virada') and c['virada']['dif_local'] is not None and abs(c['virada']['dif_local']) >= LIM_VIRADA]
    R['exploratorio'] = X
    json.dump(R, open(saida_json, 'w'), ensure_ascii=False, indent=1, default=str)
    open(saida_txt, 'w').write(texto(R))
    log('exploratorio gravado')


# ================================================================ texto
def fn(x, nd=1, sinal=False):
    if x is None: return '-'
    s = f'{x:+,.{nd}f}' if sinal else f'{x:,.{nd}f}'
    return s.replace(',', 'X').replace('.', ',').replace('X', '.')


def desc_tentativa(e):
    q = f"{e['primeiro_erro']}" + (f"-{e['ultimo_erro']}" if e['ultimo_erro'] != e['primeiro_erro'] else '')
    partes = []
    if e['nao_confere']: partes.append(f"não confere {e['nao_confere']}")
    if e['ano_diferente']: partes.append(f"ano diferente {e['ano_diferente']}")
    if e['ano_invalido']: partes.append(f"ano inválido {e['ano_invalido']}")
    s = f"{q} {e['erros']} erro(s) ({', '.join(partes)}) -> "
    if e['desfecho'] == 'habilitado':
        s += f"habilitado {e['hora_habilitacao']} por {e['classe']}" + (f" (mesário {e['mesario']})" if e['mesario'] else '')
        s += f", votou {e['hora_voto']}" if e['votou'] else ', sem voto computado em seguida'
    else:
        s += e['desfecho']
        sg = e.get('seguinte')
        if sg:
            s += f"; tentativa seguinte {sg['intervalo_s']} s depois: {sg['desfecho']}"
            if sg['desfecho'] == 'habilitado':
                s += f" por {sg['classe']}" + (f" (mesário {sg['mesario']})" if sg['mesario'] else '')
                s += f", votou {sg['hora_voto']}" if sg['votou'] else ', sem voto'
            if sg['erros']: s += f", com {sg['erros']} erro(s)"
    return s


def linha_curta(c):
    lg = (c.get('log') or {}).get('2') or {}; c2 = (c.get('C2') or {}).get('2') or {}; h = c2.get('hab', {})
    v = c.get('virada') or {}
    t3 = c.get('T3') or {}
    ok = lambda x: 'ok' if x is True else ('DIF' if x is False else '-')
    return (f"{c['secao']:<18} loc {c['local_bweb']:>5} votos {lg.get('votos', '-'):>4} | erros {lg.get('erros_ano', '-'):>3}"
            f" (nc {lg.get('nao_confere', '-')}, ad {lg.get('ano_diferente', '-')}, ai {lg.get('ano_invalido', '-')})"
            f" | M {c2.get('M', '-')} (MI {h.get('MI', '-')}, DG {h.get('DG', '-')}, OR {h.get('OR', '-')}) S {h.get('S', '-')}"
            f" | já votou {lg.get('ja_votou', '-')} (seq {lg.get('ja_votou_maior_seq', '-')}) | SIM {lg.get('sim', '-')}"
            f" ret17 {lg.get('sim_retomada_17h', '-')} canc {lg.get('sim_cancelado', '-')}"
            f" | virada {fn(v.get('v'), 1, True)} local {fn(v.get('dif_local'), 1, True)} ({v.get('outras_no_local', '-')})"
            f" mun {fn(v.get('dif_municipio'), 1, True)}"
            f" | BU {ok(c['bu_igual_bweb'])} RDV {ok(c['rdv_igual_bu'])} log {ok(c['votos_log_igual_comparecimento'])}"
            f" ass {ok(c['assinatura_ok'])} A3 {t3.get('A3_sem_habilitacao', '-')}")


def leitura(R):
    """O que isso quer dizer (texto montado dos números do resultado)."""
    L = []; w = L.append
    S = R['resumo']; P = R['por_municipio']; sec = {c['secao']: c for c in R['por_secao']}
    ba, pi = P['BA|XIQUE-XIQUE'], P['PI|CORONEL JOSÉ DIAS']
    ctx = R['contexto_amostra']['erros_ano']
    w('')
    w('O que isso quer dizer')
    w(f"- Nas {S['secoes']} seções dos dois municípios, o boletim é igual ao bweb, o RDV é igual ao boletim, o log conta os mesmos votos do")
    w('  comparecimento, não há voto computado sem habilitação, e a assinatura de hardware de cada urna confere. O limite é o de sempre: os')
    w('  quatro arquivos saem do mesmo software; um software adulterado que gravasse tudo coerente não seria visto aqui.')
    mb, mp = ba['2']['max_erros_ano'], pi['2']['max_erros_ano']
    w(f"- Erros de ano de nascimento no 2º turno: em Xique-Xique, {ba['2']['erros_ano']} na cidade inteira ({ba['2']['secoes_com_o_dia']} seções), no máximo")
    w(f"  {mb[0]} numa seção ({mb[1]}). Em Coronel José Dias, {pi['2']['erros_ano']} na cidade, {mp[0]} deles numa só seção ({mp[1]}). Nenhuma seção")
    w('  tem 139 nem 79 erros, nem 139 ou 79 liberações, órfãs, "já votou" ou tentativas, em nenhum dos dois dias que o log traz (as únicas')
    w('  coincidências são o número de habilitações biométricas de 4 seções, que nada têm a ver com erro). Na amostra nacional de '
      f"{R['contexto_amostra']['secoes_lidas']} seções, o máximo por seção é {ctx['max']} e o percentil 99 é {fn(ctx['p99'], 0)}: a seção {mp[1]}")
    w('  é real e fora da curva; Xique-Xique não é.')
    x = sec.get(mp[1])
    if x:
        lg = x['log']['2']; l1 = x['log']['1']; rs = lg['resumo_tentativas_com_erro']; h = x['C2']['2']['hab']; h1 = x['C2']['1']['hab']
        r1 = l1['resumo_tentativas_com_erro']; v = x['virada']
        w(f"- Em {mp[1]} os erros não são um eleitor errando {lg['erros_ano']} vezes: são {rs['n']} tentativas de habilitação com erro ao longo do dia")
        w(f"  ({lg['erros_por_hora']}), com no máximo {rs['maior_numero_de_erros_numa_tentativa']} erros numa tentativa (a urna cancela depois do segundo dado errado).")
        w(f"  Em {rs['desfechos'].get('habilitado', 0)} delas o eleitor foi liberado logo depois, na mesma tentativa, e votou; quem autorizou: digital gravada")
        w(f"  no dia {rs['classe_dos_habilitados'].get('DG', 0)}, digital órfã {rs['classe_dos_habilitados'].get('OR', 0)}, mesário identificado {rs['classe_dos_habilitados'].get('MI', 0)},"
          f" sem biometria cadastrada {rs['classe_dos_habilitados'].get('S', 0)}.")
        um = sum(1 for e in lg['tentativas_com_erro'] if e['erros'] == 1 and e['nao_confere'] == 1 and e['desfecho'] == 'habilitado'
                 and e['classe'] in ('MI', 'DG', 'OR', 'MX'))
        w(f"  Em {um} das {rs['n']} o roteiro é o mesmo: a biometria do eleitor falha, a urna pede o dado pessoal, o mesário digita o ano, \"não")
        w('  confere", digita de novo, "confere", e uma digital autoriza no lugar do mesário. O log não grava o que foi digitado.')
        c1 = r1['classe_dos_habilitados']
        w(f"  Na mesma urna, no 1º turno (que Flávio venceu no país), o mesmo quadro: {l1['erros_ano']} erros, {r1['desfechos'].get('habilitado', 0)} liberados"
          f" na mesma tentativa (mesário identificado {c1.get('MI', 0)}, digital gravada no dia {c1.get('DG', 0)}, órfã {c1.get('OR', 0)}, sem biometria"
          f" cadastrada {c1.get('S', 0)}).")
        w(f"  Lula já tinha {fn(v['fatia_1T'], 1)}% dos votos dos finalistas no 1º turno e foi a {fn(v['fatia_2T'], 1)}%: virada de {fn(v['v'], 2, True)}, contra"
          f" {fn(v['virada_outras_municipio'], 2, True)} das outras seções do município. A seção é a única do seu local, então o item do sinal fica \"sem")
        w('  comparação" pela regra fixada; contra o município a diferença é de ' + fn(v['dif_municipio'], 2, True) + ' pontos, longe dos 5.')
    j1 = max(ba['1']['max_ja_votou_seq'], pi['1']['max_ja_votou_seq']); j2 = max(ba['2']['max_ja_votou_seq'], pi['2']['max_ja_votou_seq'])
    w(f"- \"Já votou\": a maior sequência é de {j1[0]} no 1º turno ({j1[1]}) e de {j2[0]} no 2º turno ({j2[1]}). Cada linha é a urna recusando")
    w('  um título de quem já tinha votado: a mensagem não habilita ninguém.')
    E3 = (R.get('exploratorio') or {}).get('E3') or {}
    gr = [x for xs in E3.values() for x in xs if x['sequencia'] >= 6]
    if gr:
        w(f"  As sequências de 6 ou mais ({'; '.join(x['secao'] + ' ' + str(x['sequencia']) + ' de ' + x['de'] + ' a ' + x['ate'] for x in gr)})")
        w(f"  ficam a minutos do pedido de encerramento e {'nenhuma é seguida de voto' if all(x['votos_depois_da_sequencia'] == 0 for x in gr) else 'algumas são seguidas de voto'} (E3).")
    w(f"- SIM seguida de retomada depois das 17h: {ba['2']['sim_retomada_17h'] + pi['2']['sim_retomada_17h']} caso em {S['secoes']} seções no 2º turno (ver E4).")
    w(f"- Liberações sem biometria nas mesmas urnas: Xique-Xique {ba['1']['M']} no 1º turno e {ba['2']['M']} no 2º (órfãs {ba['1']['OR']} e {ba['2']['OR']});"
      f" Coronel José Dias {pi['1']['M']} e {pi['2']['M']} (órfãs {pi['1']['OR']} e {pi['2']['OR']}). O volume é o mesmo nos dois turnos.")
    xs = R['por_secao']
    nh_ok = sum(1 for c in xs if c.get('C2') and c['C2']['2']['M'] == (c.get('M_log_contra_NH_bweb') or {}).get('NH_bweb'))
    w(f"  M do log (classes do C2) igual ao QT_ELEI_BIOM_SEM_HABILITACAO do bweb em {nh_ok} de {len(xs)} seções.")
    for t, rot in (('2', '2º turno'), ('1', '1º turno')):
        orf = sum(c['C2'][t]['hab']['OR'] for c in xs if c.get('C2')); z = sum(c['C2'][t]['OR_todos_zero'] for c in xs if c.get('C2'))
        ss = sum(c['C2'][t]['OR_sem_score'] for c in xs if c.get('C2'))
        mx = max(((c['C2'][t]['OR_max_score_max'] or 0) for c in xs if c.get('C2')), default=None)
        w(f"  \"Score zero\" ({rot}): das {orf} liberações por digital órfã nas duas cidades, {z} {'tem' if z == 1 else 'têm'} todos os scores da comparação iguais a")
        w(f"  zero, {ss} não têm linha de score, e o maior score de uma órfã é {mx} (baixo, por isso não bateu com nenhum mesário; não é zero).")
    top = sorted((c for c in xs if c.get('C2')), key=lambda c: -c['C2']['2']['hab']['OR'])[:5]
    w('  As seções com mais órfãs no 2º turno têm quase o mesmo número no 1º turno na mesma urna (2º e 1º turno; virada contra o município): ' +
      '; '.join(f"{c['secao']} {c['C2']['2']['hab']['OR']} e {c['C2']['1']['hab']['OR']} ({fn(c['virada']['dif_municipio'], 1, True)})"
                for c in top) + '.')
    w(f"- Virada dos municípios: Xique-Xique {fn(ba['virada_municipio_pond'], 2, True)}, Coronel José Dias {fn(pi['virada_municipio_pond'], 2, True)} pontos.")
    return L


def texto_exploratorio(R):
    X = R['exploratorio']; L = []; w = L.append
    w('')
    w('Exploratório, fora do registro (escrito depois de ver o resultado pela letra; contexto, sem veredito)')
    e1 = X['E1']
    w('- E1. Erros de ano de nascimento em todos os dias do log (preparação, 04/10 e 25/10): maiores por seção ' +
      '; '.join(f'{k} {q}' for q, k in e1['total_por_secao_todos_os_dias_top'][:5]) + '.')
    for m, v in e1['por_municipio'].items():
        w(f"  Município {m}: " + '; '.join(f"{d}: {x.get('erros', 0)} (não confere {x.get('nao_confere', 0)}, ano diferente {x.get('ano_diferente', 0)},"
                                          f" inválido {x.get('ano_invalido', 0)})" for d, x in v.items()) + '.')
    w('  Mais perto de 139: ' + '; '.join(f'{q} ({k})' for q, k in e1['mais_proximos_de_139'][:3]) + '.')
    w('  Mais perto de 79: ' + '; '.join(f'{q} ({k})' for q, k in e1['mais_proximos_de_79'][:3]) + '.')
    w('  Iguais a 139 ou 79: ' + ('; '.join(f'{q} ({k})' for q, k in e1['igual_a_139_ou_79']) if e1['igual_a_139_ou_79'] else 'nenhuma') + '.')
    w('- E2. Dia 04/10 na mesma urna, seções com 20 ou mais erros:')
    for e in X['E2']:
        r = e['resumo']
        w(f"  {e['secao']}: {e['erros_ano']} erros (não confere {e['nao_confere']}, ano diferente {e['ano_diferente']}), por hora {e['erros_por_hora']};"
          f" {r['n']} tentativas com erro, desfechos {r['desfechos']}, classe dos habilitados {r['classe_dos_habilitados']}; liberações do dia"
          f" {e['liberacoes']}; votos depois do último erro {e['votos_depois_do_ultimo_erro']}; erros no 25/10: {e['erros_25_10']}.")
    w('- E3. Maior sequência de "O eleitor identificado já votou" (sem habilitação entre uma e outra), por município e turno:')
    for g, xs in X['E3'].items():
        if xs:
            w(f"  {g}: " + '; '.join(f"{x['secao']} {x['sequencia']} seguidas de {x['de']} a {x['ate']}, {x['votos_depois_da_sequencia']} votos depois,"
                                     f" pedido de encerramento às {x['proximo_pedido_de_encerramento']}" for x in xs[:2]) + '.')
    w('- E4. Respostas SIM seguidas de voto: ' + ('; '.join(
        f"{e['secao']} ({e['turno']}º turno): SIM às {e['sim']}" + (', encerramento cancelado' if e['cancelou'] else '') + ', depois '
        + ', '.join(f"habilitação {h['hora_habilitacao']} classe {h['classe']} e voto {h['hora_voto']}" for h in e['habilitacoes_depois'])
        for e in X['E4']) if X['E4'] else 'nenhuma') + '.')
    w('- E5. Seções com diferença contra o local de 5 pontos ou mais (em valor absoluto): ' + ('; '.join(
        f"{e['secao']} {fn(e['dif_local'], 2, True)} ({e['outras_no_local']} outra(s) no local; {e['erros_25_10']} erros; M {e['M']}, OR {e['OR']}; {e['votos']} votos)"
        for e in X['E5']) if X['E5'] else 'nenhuma') + '.')
    return L


def texto(R):
    L = []; w = L.append
    w('C3 (Adendo 24): casos citados no reel de @assis.salvioli, arquivo por arquivo (Xique-Xique/BA e Coronel José Dias/PI)')
    w('Registro: PRE-REGISTRO-2026-10-26.md, Adendo 24 (commit ca110bb, 03/11/2026 04:24:10 UTC). Script: scripts/analisar_C3_reel.py.')
    w('')
    w('Letra do registro')
    w('- Boletim, RDV, log e assinatura de todas as seções do 2º turno de Xique-Xique (BA) e de Coronel José Dias (PI). Contar por seção:')
    w('  "Dado digitado não confere", liberações, digitais órfãs, "O eleitor identificado já votou", respostas "Todas as pessoas presentes')
    w('  já votaram? SIM" seguidas de retomada da votação depois das 17h. Conferir assinatura, boletim contra bweb, RDV contra boletim, votos')
    w('  no log contra comparecimento, e a virada da seção contra as outras do mesmo local e do município.')
    w('- Sinal: assinatura inválida, boletim diferente do bweb, RDV diferente do boletim, votos no log diferentes do comparecimento, voto')
    w('  computado sem habilitação, ou seção com muitos erros de ano de nascimento cuja virada passe a das outras do mesmo local em 5 pontos ou mais.')
    w('- O reel: "erra o ano de nascimento até 139 vezes na mesma seção"; painel: "139 erros em Xique-Xique/BA e 79 em Coronel José Dias/PI".')
    w('')
    w('Seleção')
    for m, x in R['municipios'].items():
        w(f"- {m}: código {', '.join(x['codigos_no_bweb'])} no bweb do 2º turno, zona {', '.join(map(str, x['zonas']))}, {x['secoes']} seções"
          f" ({x['com_agregadas']} com seção agregada), {x['locais']} locais.")
    cb = R['conferencia_base']
    w(f"- Base secoes2026: {cb['na_base_com_2T']} seções com 2º turno nos dois códigos, as mesmas do bweb ({cb['no_bweb']}).")
    S = R['resumo']; A = R['assinaturas']; cc = A.get('contagem') or {}
    w('')
    w('Resultado pela letra')
    w(f"- Boletim igual ao bweb: {S['bu_igual_bweb'][0]} de {S['bu_igual_bweb'][1]}. RDV igual ao boletim: {S['rdv_igual_bu'][0]} de {S['rdv_igual_bu'][1]}."
      f" Votos no log = comparecimento: {S['votos_log_igual_comparecimento'][0]} de {S['votos_log_igual_comparecimento'][1]}."
      f" Assinatura ok: {S['assinatura_ok'][0]} de {S['assinatura_ok'][1]}.")
    w(f"- Voto computado sem habilitação (A3): {S['voto_sem_habilitacao_A3']}. Fora do sinal do C3: " +
      ', '.join(f'{k} {v}' for k, v in S['outras_T3'].items()) + '.')
    w(f"- Assinaturas (verificar_assinaturas.py): seções com vsc {cc.get('secoes_com_vsc')}, bloco de hardware ok {cc.get('bloco_hw_assinatura_ok')},"
      f" arquivos com assinatura ok {cc.get('assinatura_arquivo_ok')} de {cc.get('arquivos_listados')}, resumos ok {cc.get('resumo_ok')} de"
      f" {cc.get('arquivos_baixados_conferidos')}, SHA-256 do vsc igual ao aux {cc.get('vsc_sha256_igual_ao_aux')}, urna do certificado igual"
      f" à do boletim {cc.get('urna_cert_igual_bu')}; falhas {len(A.get('falhas') or [])}.")
    w(f"- Seções com muitos erros de ano de nascimento (20 ou mais no 25/10, D5): {len(S['secoes_com_muitos_erros'])}"
      + (': ' + ', '.join(f"{k} (item da virada: {v})" for k, v in S['item_virada'].items()) if S['item_virada'] else '') + '.')
    if S['faltando']: w('- Arquivos que não vieram: ' + '; '.join(f"{k}: {', '.join(x)}" for k, x in S['faltando'].items()))
    if S['sem_aux']: w('- Sem aux.json: ' + ', '.join(S['sem_aux']))
    if S['pacotes_multiplos']: w('- Mais de um pacote no aux: ' + ', '.join(S['pacotes_multiplos']))
    w(f"- Seções com sinal: {len(R['secoes_com_sinal'])}" + (': ' + ', '.join(R['secoes_com_sinal']) if R['secoes_com_sinal'] else '') + '.')
    w(f"- VEREDITO: {R['veredito']}.")
    w('')
    w('Contagens por município (log do pacote; 2º turno em 25/10; 1º turno = dia 04/10 no mesmo log, só nas seções em que a urna é a mesma)')
    for m, x in R['por_municipio'].items():
        for t, rot in (('2', '2º turno'), ('1', '1º turno, mesma urna')):
            y = x[t]
            w(f"- {m}, {rot} ({y['secoes_com_o_dia']} seções com o dia no log, {y['votos_log']} votos): erros de ano de nascimento {y['erros_ano']}"
              f" (\"Dado digitado não confere\" {y['nao_confere']}, \"Ano de nascimento digitado é diferente do cadastro\" {y['ano_diferente']},"
              f" inválido {y['ano_invalido']}); maior por seção: {y['max_erros_ano'][0] if y['max_erros_ano'] else '-'}"
              f" ({y['max_erros_ano'][1] if y['max_erros_ano'] else '-'}); maior \"não confere\" por seção {y['max_nao_confere'][0] if y['max_nao_confere'] else '-'}.")
            w(f"    liberações sem biometria (M) {y['M']}: mesário identificado {y['MI']}, digital gravada no dia {y['DG']}, digital órfã {y['OR']};"
              f" sem biometria cadastrada {y['S']}; biometria {y['B']}. \"O eleitor identificado já votou\" {y['ja_votou']} (maior sequência numa"
              f" seção {y['max_ja_votou_seq'][0] if y['max_ja_votou_seq'] else '-'}); respostas SIM {y['sim']}, seguidas de voto depois das 17h"
              f" {y['sim_retomada_17h']}, seguidas de cancelamento do encerramento {y['sim_cancelado']}.")
        w(f"    virada do município (média das seções ponderada por L2+R2): {fn(x['virada_municipio_pond'], 2, True)} pontos.")
    w('')
    w('Os números do reel (139 e 79)')
    if R['numeros_do_reel_encontrados']:
        w('- Contagens por seção iguais a 139 ou 79: ' + '; '.join(f'{a} turno {b} {c}={d}' for a, b, c, d in R['numeros_do_reel_encontrados']))
    else:
        w('- Nenhuma contagem por seção (erros, "não confere", "ano diferente", "já votou", tentativas, classes de liberação, M) é 139 ou 79,')
        w('  em nenhum dos dois dias.')
    ctx = R['contexto_amostra']; ea = ctx['erros_ano']; nc = ctx['nao_confere']
    w(f"- Contexto (D10), amostra nacional de {ctx['secoes_lidas']} seções do 2º turno: erros de ano de nascimento por seção em 25/10 com média"
      f" {fn(ea['media'], 2)}, mediana {fn(ea['p50'], 0)}, p90 {fn(ea['p90'], 0)}, p99 {fn(ea['p99'], 0)}, máximo {ea['max']};"
      f" {ea['com_20_ou_mais']} seções com 20 ou mais. Só \"não confere\": p99 {fn(nc['p99'], 0)}, máximo {nc['max']}.")
    w('  Maiores da amostra (erros, não confere, ano diferente/inválido, seção): ' +
      '; '.join(f'{a} ({b}, {c}) {d}' for a, b, c, d in ctx['maiores_erros_ano'][:8]) + '.')
    L.extend(leitura(R))
    w('')
    w('Seção por seção, 2º turno (nc = "Dado digitado não confere", ad = ano diferente, ai = ano inválido; M = liberação sem biometria de eleitor com')
    w('biometria cadastrada, MI mesário identificado, DG digital gravada no dia, OR digital órfã; S = sem biometria cadastrada; seq = maior sequência')
    w('de "já votou"; ret17 = respostas SIM seguidas de voto às 17h ou depois; virada em pontos; local/mun = diferença contra as outras seções')
    w('do local (número de outras entre parênteses) e do município, ponderada por L2+R2)')
    for mun in R['municipios']:
        w(''); w(mun)
        for c in R['por_secao']:
            if c['municipio'] == mun:
                w('  ' + linha_curta(c))
    w('')
    w('Seções descritas (D8): as de muitos erros e, em cada município, a de mais erros de ano de nascimento e a de mais "não confere"')
    for k in R['secoes_descritas']:
        c = next(x for x in R['por_secao'] if x['secao'] == k)
        lg = c['log']['2']; l1 = c['log']['1']; c2 = c['C2']['2']; v = c['virada'] or {}
        rs = lg['resumo_tentativas_com_erro']
        w('')
        w(f"* {k} (local {c['local_bweb']}; {'MUITOS ERROS' if c['muitos_erros'] else 'abaixo de 20 erros'}):"
          f" {lg['erros_ano']} erros de ano de nascimento em 25/10 (não confere {lg['nao_confere']}, ano diferente {lg['ano_diferente']},"
          f" ano inválido {lg['ano_invalido']}); erros por hora {lg['erros_por_hora']}; último erro {lg['ultimo_erro']}, votos depois dele"
          f" {lg['votos_depois_do_ultimo_erro']}; votos {lg['primeiro_voto']} a {lg['ultimo_voto']}.")
        w(f"    {rs['n']} tentativas de habilitação com erro (maior número de erros numa tentativa: {rs['maior_numero_de_erros_numa_tentativa']});"
          f" desfechos {rs['desfechos']}; classe dos habilitados {rs['classe_dos_habilitados']}; mesário (pseudônimo) dos MI {rs['mesario_dos_habilitados_MI']}.")
        w(f"    liberações no dia: M {c2['M']} (MI {c2['hab']['MI']}, DG {c2['hab']['DG']}, OR {c2['hab']['OR']}, MX {c2['hab']['MX']}),"
          f" S {c2['hab']['S']}, B {c2['hab']['B']}; NH do bweb {(c['M_log_contra_NH_bweb'] or {}).get('NH_bweb')}; mesários no log {lg['mesarios_no_log']}.")
        w(f"    virada {fn(v.get('v'), 2, True)} (Lula {fn(v.get('fatia_1T'), 1)}% no 1º turno, {fn(v.get('fatia_2T'), 1)}% no 2º); outras {v.get('outras_no_local')}"
          f" do local {fn(v.get('virada_outras_local'), 2, True)} (diferença {fn(v.get('dif_local'), 2, True)}); município sem ela"
          f" {fn(v.get('virada_outras_municipio'), 2, True)} (diferença {fn(v.get('dif_municipio'), 2, True)}); urna 1T {v.get('urna_1T')} 2T {v.get('urna_2T')};"
          f" agregação {v.get('agr_1T')}/{v.get('agr_2T')}.")
        if l1 and l1['votos']:
            r1 = l1['resumo_tentativas_com_erro']; h1 = c['C2']['1']['hab']
            w(f"    mesma urna no 1º turno (04/10): {l1['votos']} votos, {l1['erros_ano']} erros de ano de nascimento (não confere {l1['nao_confere']},"
              f" ano diferente {l1['ano_diferente']}), erros por hora {l1['erros_por_hora']}; {r1['n']} tentativas com erro, desfechos {r1['desfechos']},"
              f" classe dos habilitados {r1['classe_dos_habilitados']}, mesário dos MI {r1['mesario_dos_habilitados_MI']}; M {c['C2']['1']['M']}"
              f" (MI {h1['MI']}, DG {h1['DG']}, OR {h1['OR']}), S {h1['S']}, B {h1['B']}.")
        w(f"    \"já votou\" {lg['ja_votou']} (maior sequência {lg['ja_votou_maior_seq']} {lg['ja_votou_maior_seq_horas']}); SIM: " +
          '; '.join(f"{s['hora']} ({'cancelou o encerramento, ' if s['cancelou_o_encerramento'] else ''}{s['votos_depois']} votos depois"
                    + (f", {s['primeiro_voto_depois']} a {s['ultimo_voto_depois']}" if s['votos_depois'] else '') + ')' for s in lg['sim_detalhe']))
        tt = lg['tentativas_com_erro']
        w(f"    tentativas com erro ({len(tt)}" + (', as 80 primeiras' if len(tt) > 80 else '') + '):')
        for e in tt[:80]:
            w('      ' + desc_tentativa(e))
    if R.get('exploratorio'):
        L.extend(texto_exploratorio(R))
    w('')
    w('Desvios declarados (decisões que o registro não fixa, tomadas antes de baixar e de abrir qualquer log; ver o docstring do script):')
    w('D1 municípios pelo nome no bweb do 2º turno; D2 download e pacote mais recente; D3 conferências com as funções do F14, A3 como "voto')
    w('computado sem habilitação"; D4 erros de ano de nascimento = "Dado digitado não confere" (o que o registro nomeia) mais "Ano de nascimento')
    w('digitado é diferente do cadastro" e "Ano de nascimento inválido", separados; liberações e órfãs pelas classes do C2; "já votou" seguido sem')
    w('habilitação entre um e outro; SIM seguida de voto às 17h ou depois no mesmo bloco; D5 "muitos" = 20 ou mais erros em 25/10; D6 virada')
    w('contra as outras do local ponderada por L2+R2, +5 no sentido de Lula; D7 "sem sinal" = nenhum dos seis itens; D8 a D11 descritivos.')
    return '\n'.join(L) + '\n'


if __name__ == '__main__':
    if sys.argv[1] == 'lista':
        lista(*sys.argv[2:6])
    elif sys.argv[1] == 'arquivos':
        arquivos(*sys.argv[2:11])
    elif sys.argv[1] == 'exploratorio':
        exploratorio(*sys.argv[2:5])
    elif sys.argv[1] == '--texto':
        print(texto(json.load(open(sys.argv[2]))), end='')
