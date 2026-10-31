"""F11 do Adendo 21: arquivos públicos do teste de integridade do 2º turno.

Registro (PRE-REGISTRO-2026-10-26.md, Adendo 21, commit 913af7a, 31/10/2026 10:36:29 UTC, antes de rodar):
  "Achar o que o TSE e os TREs publicaram (lista de urnas, relatórios, boletins, logs, RDV, vídeos, contagem das
  cédulas). Se houver arquivos de urna: conferir boletim contra a contagem das cédulas, versão do programa e verificação
  de assinatura no log contra as urnas reais, e o modo de habilitação usado. Sinal: alguma urna de teste com boletim
  diferente das cédulas sem explicação documentada, ou com programa diferente das urnas reais. Sem critério para o resto."

Decisões que o registro não fixa, tomadas e escritas aqui ANTES de baixar ou ler qualquer arquivo de urna das seções
do teste (declaradas como desvio no resultado):

  D1. "Arquivos de urna" do teste = boletim, RDV e log gravados pela urna testada no dia 25/10/2026. O inventário diz,
      item por item, o que foi achado publicado (fonte, data, confiança). Páginas jus.br que dão HTTP 403 não são
      contornadas: o que vem delas sai do resumo do buscador e fica marcado com confiança média ou baixa.
  D2. "Explicação documentada": causa da divergência dada em texto oficial (TSE, TRE, ata, relatório) ou em texto da
      imprensa que cita a autoridade do teste pelo nome. Causa dada sem urna, cargo, número de votos ou direção conta
      como explicação documentada INCOMPLETA: não aciona o sinal, vai para as pistas, e o resultado diz também como
      ficaria a leitura estrita (que exige ata ou relatório publicado com o voto identificado).
  D3. Conferência indireta do programa (fora da letra, que fala dos arquivos do teste). Na rotina de 2026 a urna do 2º
      turno fica com a carga do 1º (T10: mídia de votação igual nos dois turnos em 3.842 das 3.897 urnas da amostra) e,
      no teste de integridade, a urna da seção escolhida vai para o teste e a seção vota numa urna reserva carregada no
      sábado 24/10. Logo, a urna testada é a urna efetivada da seção no 1º turno (NR_URNA_EFETIVADA do 1º turno), e os
      arquivos públicos dela no 1º turno (pleito 3220) mostram o programa instalado nela, com a mesma carga.
      Grupo T (urnas de teste identificadas): seções das listas publicadas de integridade (com e sem biometria) que estão
      no grupo S do L7 (urna do 2º turno diferente da do 1º e carga em 24/10/2026). Seção de lista fora de S é relatada
      e não entra em T.
      Para cada urna de T, nos arquivos do 1º turno: versão no boletim; "Versão da aplicação" no log; modelo
      ("Identificação do Modelo de Urna"); todas as linhas "Verificação de assinatura" (resultado e componente);
      assinatura do pacote (-vota.vsc) pelo verificar_assinaturas.py (resumos, assinatura de cada arquivo e do bloco,
      número da urna no certificado contra o boletim); número da urna no boletim igual ao NR_URNA_EFETIVADA do bweb.
      Referência "urnas reais": as 3.897 urnas da amostra do 2º turno (amostra2t/arq), cujos logs trazem também o 1º
      turno. Programa diferente, para esta conferência indireta, é qualquer um destes: (a) versão do aplicativo (log ou
      boletim) diferente da versão das urnas reais; (b) componente verificado no dia 04/10/2026 que nenhuma urna real do
      mesmo modelo verificou nesse dia (caminho normalizado: seção, pleito e UF trocados por marcadores); (c) verificação
      de assinatura sem [SUCESSO] no dia 04/10/2026; (d) falha no .vsc (resumo, assinatura de arquivo ou do bloco, ou
      urna do certificado diferente da do boletim). Qualquer um deles em urna de T conta como sinal por extensão, com a
      ressalva de que é o 1º turno da mesma urna, não o arquivo do teste.
  D4. Urnas reserva que votaram nas seções de T no 25/10 (arquivos públicos do 2º turno, pleito 3221): as mesmas
      conferências de (a) a (d), no dia 25/10, mais data e hora da carga no log e no bweb. São urnas reais, não de teste:
      descritivo, e uma conferência de que a carga de sábado levou o mesmo programa.
  D5. Coerência da identificação: a urna do 1º turno de cada seção de T não pode aparecer como urna efetivada de nenhuma
      seção no 2º turno (passou o dia no teste). Contada para T e para todo S.
  D6. Superconjunto S (todas as 706 seções do L7, que contêm as urnas de teste de todas as UFs, inclusive as sem lista
      publicada): as mesmas conferências (a) a (d) nas urnas do 1º turno, descritivo, para cobrir as UFs sem lista.
      Controles das listas: seções do teste de autenticidade e de "gestão de riscos" (SP), relatadas à parte.
  D7. Modo de habilitação: o do teste vem só das listas (I = ambiente controlado, caderno de votação; B = com
      biometria). O da votação real nas urnas de T (1º turno) e nas reservas (2º turno) é descritivo: parte das
      habilitações por biometria no log ("Tipo de habilitação do eleitor [biométrica]" sobre "Eleitor foi habilitado").
  D8. Boletim contra cédulas: sem arquivo do teste, só o que foi publicado (urnas e votos conferidos, divergências e
      explicação), por UF, com fonte. Cada divergência publicada é classificada por D2.

Uso:
  python3 -I analisar_F11.py selecionar <secoes2026.json.gz> <zips2t_dir> <pasta_trabalho>
  (baixar com baixar_arquivos_urna.py: pleitos 3220 e 3221, tipos bu,log,vota, listas lista_prioritaria.txt e
   lista_S_resto.txt, cada download numa pasta nova)
  python3 -I analisar_F11.py analisar <pasta_trabalho> <dl_1t_prior> <dl_2t_prior> <dl_1t_S> <dl_2t_S>
          <amostra_arq_2t> <zips do Gedai do 2º turno, separados por vírgula> <secoes2026.json.gz> <saida.json> <saida.txt>
"""
import os as _os, sys as _sys
_sys.path.insert(0, _os.path.dirname(_os.path.abspath(__file__)))
import collections, glob, gzip, json, os, re, subprocess, sys, unicodedata, zipfile

VESPERA_2T = '2026-10-24'
D1T, D2T = '04/10/2026', '25/10/2026'

# Listas publicadas do 2º turno: (UF, município como publicado, zona, seção, tipo). Tipos: I integridade em ambiente
# controlado, B integridade com biometria, A autenticidade, R gestão de riscos (SP, reserva).
LISTA_AL = [('MACEIÓ', 2, 365, 'B'), ('MACEIÓ', 2, 355, 'B'), ('MACEIÓ', 1, 375, 'I'), ('TRAIPU', 20, 84, 'I'),
            ('MACEIÓ', 54, 566, 'I'), ('MARECHAL DEODORO', 26, 29, 'I'), ('SANTANA DO IPANEMA', 19, 234, 'I'),
            ('BRANQUINHA', 9, 12, 'I'), ('MONTEIRÓPOLIS', 29, 76, 'I'), ('POÇO DAS TRINCHEIRAS', 50, 37, 'I'),
            ('ÁGUA BRANCA', 39, 63, 'I'), ('GIRAU DO PONCIANO', 44, 32, 'I'), ('CORURIPE', 7, 150, 'I'),
            ('MARAGOGI', 14, 129, 'I'), ('FEIRA GRANDE', 49, 80, 'I'), ('PÃO DE AÇÚCAR', 11, 15, 'I'),
            ('JOAQUIM GOMES', 53, 5, 'I'), ('SÃO JOSÉ DA TAPERA', 51, 90, 'I'), ('IGREJA NOVA', 37, 187, 'I'),
            ('TEOTÔNIO VILELA', 34, 96, 'I'), ('SÃO LUÍS DO QUITUNDE', 17, 150, 'A'), ('JEQUIÁ DA PRAIA', 18, 187, 'A'),
            ('ARAPIRACA', 22, 519, 'A')]
FONTE_AL = 'Assessoria TRE/AL, 24/10/2026 10h33, reproduzida em https://francesnews.com.br/post/2026/10/26/43576-treal-sorteia-23-urnas-eletronicas-para-auditoria-no-segundo-turno-das-eleicoes-2026'
# São Paulo: lista do TRE-SP (arquivo_urnas_testes.pdf) reproduzida pela TV São Bernardo em 24/10/2026. Capital = SÃO PAULO.
LISTA_SP = [('SÃO PAULO', 5, 36, 'I'), ('SÃO PAULO', 255, 72, 'I'), ('SÃO PAULO', 327, 256, 'I'), ('SÃO PAULO', 247, 68, 'I'),
            ('SÃO PAULO', 20, 25, 'I'), ('SÃO PAULO', 320, 521, 'I'), ('SÃO PAULO', 405, 256, 'I'),
            ('CARAPICUÍBA', 303, 3, 'I'), ('IGARATÁ', 115, 7, 'I'), ('SANTOS', 273, 270, 'I'), ('POÁ', 219, 488, 'I'),
            ('GUARAREMA', 319, 160, 'I'), ('ITANHAÉM', 189, 131, 'I'), ('CAIEIRAS', 192, 27, 'I'), ('PIQUETE', 68, 211, 'I'),
            ('TAUBATÉ', 141, 1, 'I'), ('PAULÍNIA', 323, 75, 'I'), ('VINHEDO', 345, 16, 'I'), ('CAMPINAS', 275, 377, 'I'),
            ('DIVINOLÂNDIA', 229, 138, 'I'), ('CABREÚVA', 59, 9, 'I'), ('IBIÚNA', 191, 13, 'I'), ('ADAMANTINA', 157, 71, 'I'),
            ('ANDRADINA', 9, 22, 'I'), ('ARAÇATUBA', 299, 72, 'I'), ('BARRETOS', 21, 234, 'I'), ('DOIS CÓRREGOS', 241, 113, 'I'),
            ('AREIÓPOLIS', 129, 4, 'I'), ('PONTAL', 135, 332, 'I'), ('IBATÉ', 410, 19, 'I'),
            ('SÃO PAULO', 6, 61, 'B'), ('SÃO PAULO', 6, 315, 'B'), ('SÃO PAULO', 6, 310, 'B'),
            ('RIBEIRÃO PIRES', 183, 59, 'A'), ('MOGI MIRIM', 75, 369, 'A'), ('ALFREDO MARCONDES', 182, 4, 'A'),
            ('VALINHOS', 34, 88, 'A'), ('SANTA CRUZ DO RIO PARDO', 114, 27, 'A'), ('SANTO ANDRÉ', 264, 34, 'A'),
            ('TAIAÇU', 61, 62, 'A'), ('OSASCO', 277, 97, 'A'), ('OSASCO', 315, 206, 'A'), ('PEDERNEIRAS', 86, 168, 'A'),
            ('SÃO PAULO', 253, 302, 'R'), ('SÃO PAULO', 248, 13, 'R'), ('SÃO PAULO', 418, 293, 'R'), ('SÃO PAULO', 373, 144, 'R'),
            ('SÃO PAULO', 371, 501, 'R'), ('SÃO PAULO', 254, 453, 'R'), ('SÃO PAULO', 389, 219, 'R'), ('SÃO PAULO', 346, 66, 'R')]
FONTE_SP = 'TRE-SP, arquivo_urnas_testes.pdf, reproduzido em https://tvsaobernardo.com/eleicoes-2026-fiscalizadores-definem-urnas-para-os-testes-de-integridade-e-de-autenticidade-do-2o-turno/ (24/10/2026)'
# Paraíba: a reprodução publicada traz número de seção só para 4 das 19 de integridade e para as 3 de autenticidade;
# zona só para João Pessoa. Casamento por município e seção; com mais de uma seção possível, fica ambíguo.
LISTA_PB = [('JOÃO PESSOA', 1, 297, 'B'), ('CABEDELO', None, 181, 'I'), ('CAMPINA GRANDE', None, 171, 'I'),
            ('CAMPINA GRANDE', None, 254, 'I'), ('BELÉM', None, 161, 'A'), ('SANTA CRUZ', None, 143, 'A'),
            ('SOLÂNEA', None, 24, 'A')]
FONTE_PB = 'PB Agora, reproduzido em https://www.paraibamix.com.br/eleicoes-2026-confira-as-secoes-eleitorais-da-paraiba-selecionadas-para-auditoria-no-2o-turno/ (24/10/2026)'


def norm(s):
    return ''.join(c for c in unicodedata.normalize('NFD', s.upper()) if unicodedata.category(c) != 'Mn').strip()


def ler_zip(zpath):
    """Uma linha por seção do 2º turno: urna, carga, município, local."""
    z = zipfile.ZipFile(zpath)
    nome = [n for n in z.namelist() if n.lower().endswith('.csv')][0]
    out = {}
    pres = b';1;"Presidente";'; semvoto = b';-1;"#NULO#";-1;'
    with z.open(nome) as fh:
        cab = [c.strip().strip('"') for c in fh.readline().decode('latin1').strip().split(';')]
        ix = {c: i for i, c in enumerate(cab)}
        for linha in fh:
            if pres not in linha and semvoto not in linha:
                continue
            p = [x.strip('"') for x in linha.decode('latin1').rstrip('\r\n').split(';')]
            k = f"{p[ix['SG_UF']]}|{int(p[ix['CD_MUNICIPIO']])}|{int(p[ix['NR_ZONA']])}|{int(p[ix['NR_SECAO']])}"
            out.setdefault(k, {'urna2': int(p[ix['NR_URNA_EFETIVADA']]), 'carga2': p[ix['DT_CARGA_URNA_EFETIVADA']],
                               'mun_nome': p[ix['NM_MUNICIPIO']], 'local': p[ix['NR_LOCAL_VOTACAO']],
                               'agregadas': p[ix['DS_SECOES_AGREGADAS']], 'tipo_urna': p[ix['DS_TIPO_URNA']]})
    return out


def selecionar(secoes_gz, zips_dir, trab):
    from modelos import modelo
    os.makedirs(trab, exist_ok=True)
    base = json.load(gzip.open(secoes_gz))
    bw = {}
    for zp in sorted(glob.glob(os.path.join(zips_dir, 'bweb_2t_*.zip'))):
        bw.update(ler_zip(zp))
        print('lido', os.path.basename(zp), len(bw), flush=True)
    # urnas efetivadas no 2º turno, em qualquer seção (D5)
    urnas2 = collections.defaultdict(list)
    for k, v in bw.items():
        urnas2[v['urna2']].append(k)
    S = {}
    for k, v in bw.items():
        b1 = base.get(k, {}).get('1')
        if not b1 or b1.get('urna') is None:
            continue
        if v['carga2'][:10] == VESPERA_2T and v['urna2'] != b1['urna']:
            S[k] = {'urna1': b1['urna'], 'urna2': v['urna2'], 'carga2': v['carga2'], 'mun_nome': v['mun_nome'],
                    'modelo_urna1': modelo(b1['urna'], 2026), 'modelo_urna2': modelo(v['urna2'], 2026),
                    'urna1_efetivada_no_2t_em': urnas2.get(b1['urna'], []), 'local': v['local']}
    # casamento das listas
    por_uf_zs = collections.defaultdict(list); por_uf_mun_s = collections.defaultdict(list)
    for k, v in bw.items():
        uf, m, z, s = k.split('|')
        por_uf_zs[(uf, int(z), int(s))].append(k)
        por_uf_mun_s[(uf, norm(v['mun_nome']), int(s))].append(k)
    listadas = []
    for uf, lista, fonte in (('AL', LISTA_AL, FONTE_AL), ('SP', LISTA_SP, FONTE_SP), ('PB', LISTA_PB, FONTE_PB)):
        for mun, z, s, tipo in lista:
            if z is not None:
                cand = por_uf_zs.get((uf, z, s), [])
                cand_mun = [c for c in cand if norm(bw[c]['mun_nome']) == norm(mun)]
            else:
                cand = cand_mun = por_uf_mun_s.get((uf, norm(mun), s), [])
            reg = {'uf': uf, 'municipio_publicado': mun, 'zona': z, 'secao': s, 'tipo': tipo, 'fonte': fonte,
                   'candidatas': cand, 'candidatas_mesmo_municipio': cand_mun}
            if len(cand_mun) == 1:
                k = cand_mun[0]; reg['chave'] = k; reg['casamento'] = 'zona, seção e município' if z is not None else 'município e seção, único'
            elif len(cand) == 1 and z is not None:
                k = cand[0]; reg['chave'] = k; reg['casamento'] = 'zona e seção (município do bweb diferente do publicado)'
            else:
                k = None; reg['chave'] = None; reg['casamento'] = 'ambíguo ou não achado'
            if k:
                b1 = base.get(k, {}).get('1', {}); v = bw[k]
                reg.update({'mun_bweb': v['mun_nome'], 'urna1': b1.get('urna'), 'urna2': v['urna2'], 'carga2': v['carga2'],
                            'em_S': k in S, 'modelo_urna1': modelo(b1['urna'], 2026) if b1.get('urna') else None,
                            'urna1_efetivada_no_2t_em': urnas2.get(b1.get('urna'), [])})
            listadas.append(reg)
    # trocas de urna entre os turnos, em todo o país (D5, descritivo): por data da carga da urna do 2º turno e por a urna
    # do 1º turno ter ou não votado em alguma seção no 2º turno
    trocas = collections.Counter(); fora_S_sem_voto = collections.Counter()
    for k, v in bw.items():
        b1 = base.get(k, {}).get('1')
        if not b1 or b1.get('urna') is None or v['urna2'] == b1['urna']:
            continue
        vesp = v['carga2'][:10] == VESPERA_2T
        sumiu = not urnas2.get(b1['urna'])
        trocas[('carga 24/10' if vesp else 'outra carga', 'urna do 1º turno não votou no 2º' if sumiu else 'urna do 1º turno votou em outra seção no 2º')] += 1
        if not vesp and sumiu:
            fora_S_sem_voto[k.split('|')[0]] += 1
    T = [r['chave'] for r in listadas if r.get('chave') and r['tipo'] in ('I', 'B') and r.get('em_S')]
    controles = [r['chave'] for r in listadas if r.get('chave') and r['tipo'] in ('A', 'R')]
    sel = {'S': S, 'listadas': listadas, 'T': T, 'controles': controles,
           'n_secoes_bweb_2t': len(bw), 'trocas_de_urna': {' | '.join(k): v for k, v in trocas.items()},
           'troca_fora_de_S_urna1_sem_voto_no_2t_por_uf': dict(sorted(fora_S_sem_voto.items()))}
    json.dump(sel, open(os.path.join(trab, 'selecao.json'), 'w'), ensure_ascii=False, indent=1)
    # listas de download: T, controles e as seções de lista fora de T (fora de S, ou candidatas em S de casamento
    # ambíguo) primeiro, depois o resto de S
    extras = [r['chave'] for r in listadas if r.get('chave') and r['tipo'] in ('I', 'B') and not r.get('em_S')]
    extras += [c for r in listadas if not r.get('chave') for c in r['candidatas'] if c in S]
    sel['extras_de_lista'] = extras
    json.dump(sel, open(os.path.join(trab, 'selecao.json'), 'w'), ensure_ascii=False, indent=1)
    prim = list(dict.fromkeys(T + controles + extras))
    resto = [k for k in sorted(S) if k not in prim]
    open(os.path.join(trab, 'lista_prioritaria.txt'), 'w').write('\n'.join(prim) + '\n')
    open(os.path.join(trab, 'lista_S_resto.txt'), 'w').write('\n'.join(resto) + '\n')
    print('S', len(S), 'listadas', len(listadas), 'T', len(T), 'controles', len(controles), 'resto de S', len(resto))


# ---------------------------------------------------------------------------------------------------------------
# Análise dos arquivos baixados
# ---------------------------------------------------------------------------------------------------------------
RX_VER = re.compile(r'^Verificação de assinatura(?: - Etapa| de (?:aplicação|dado) por etapa) \[(\d+)\] - \[(?:Pacote: )?([^\]]+)\](?: - \[Arquivo: [^\]]*\])? - \[([^\]]+)\]')
NORMS = [(re.compile(r'\d{13}-'), 'SECAO-'), (re.compile(r'o0\d{4}[a-z]{2}-'), 'oPLEITOUF-'), (re.compile(r'o0\d{4}-'), 'oPLEITO-')]


def norm_comp(c):
    for rx, sub in NORMS:
        c = rx.sub(sub, c)
    return c


def ler_log_f11(caminho):
    """Por dia: versões, modelo, componentes verificados (normalizados) e resultado, habilitações e biométricas,
    fase e modo de carga, urnas no log, primeira e última linha. Soma todos os logs do pacote (inclusive aninhados)."""
    from decodificar import _linhas_log
    d = collections.defaultdict(lambda: {'versoes': set(), 'modelos': set(), 'comp': set(), 'verif': 0, 'verif_sem_sucesso': [],
                                         'hab': 0, 'bio': 0, 'fase': set(), 'modo_carga': set(), 'urnas': set(),
                                         'primeira': None, 'ultima': None, 'aplicacoes': set(), 'midia_votacao': set(),
                                         'iniciando': set(), 'verif_outras_apps': collections.Counter()})
    for bloco in _linhas_log(caminho):
        for l in bloco:
            p = l.split('\t')
            if len(p) < 5 or len(p[0]) < 19:
                continue
            dia, hora, urna, app, msg = p[0][:10], p[0][11:19], p[2], p[3], p[4]
            r = d[dia]
            r['urnas'].add(urna); r['aplicacoes'].add(app)
            if r['primeira'] is None or hora < r['primeira']: r['primeira'] = hora
            if r['ultima'] is None or hora > r['ultima']: r['ultima'] = hora
            if msg.startswith('Versão da aplicação: '): r['versoes'].add(msg.split(': ', 1)[1])
            elif msg.startswith('Identificação do Modelo de Urna: '): r['modelos'].add(msg.split(': ', 1)[1])
            elif msg.startswith('Verificação de assinatura'):
                # componentes: só as verificações do aplicativo de votação na inicialização (GAP); as da carga (SCUE)
                # e de outros aplicativos ficam à parte; resultado sem SUCESSO é contado em qualquer aplicativo
                m = RX_VER.match(msg)
                if app == 'GAP':
                    r['verif'] += 1
                    if m: r['comp'].add(norm_comp(m.group(2)))
                else:
                    r['verif_outras_apps'][app] += 1
                if m:
                    if m.group(3) != 'SUCESSO': r['verif_sem_sucesso'].append(p[0] + ' ' + app + ' ' + msg)
                else:
                    r['verif_sem_sucesso'].append(p[0] + ' ' + app + ' (linha fora do padrão) ' + msg)
            elif msg == 'Eleitor foi habilitado': r['hab'] += 1
            elif msg == 'Tipo de habilitação do eleitor [biométrica]': r['bio'] += 1
            elif msg.startswith('Fase da UE: '): r['fase'].add(msg.split(': ', 1)[1])
            elif msg.startswith('Modo de carga da UE - '): r['modo_carga'].add(msg.split(' - ', 1)[1])
            elif msg.startswith('Data e hora da geração da mídia de votação: '): r['midia_votacao'].add(msg.split(': ', 1)[1])
            elif msg.startswith('Iniciando aplicação - '): r['iniciando'].add(msg.split(' - ', 1)[1])
    return d


def _secoes_pasta(pasta):
    for uf in sorted(os.listdir(pasta)):
        if not os.path.isdir(os.path.join(pasta, uf)): continue
        for m in sorted(os.listdir(os.path.join(pasta, uf))):
            for z in sorted(os.listdir(os.path.join(pasta, uf, m))):
                for s in sorted(os.listdir(os.path.join(pasta, uf, m, z))):
                    yield f'{uf.upper()}|{int(m)}|{int(z)}|{int(s)}', os.path.join(pasta, uf, m, z, s)


def _ultimo(arqs, suf):
    """Arquivo do último hash listado (prefixo numérico maior)."""
    c = [a for a in arqs if a.endswith(suf)]
    return sorted(c, key=lambda a: int(a.split('-', 1)[0]) if a.split('-', 1)[0].isdigit() else -1)[-1] if c else None


def _uma_secao(args):
    k, p, dia = args
    from decodificar import ler_bu
    arqs = os.listdir(p)
    out = {'k': k, 'sem_aux': 'SEM_AUX' in arqs}
    try:
        aux = json.load(open(os.path.join(p, 'aux.json')))
        out['aux_hashes'] = len(aux.get('hashes', [])); out['aux_st'] = aux.get('st')
    except Exception:
        out['aux_hashes'] = None
    bu = _ultimo(arqs, '-bu.dat'); lg = _ultimo(arqs, '-log.jez')
    if bu:
        try:
            b = ler_bu(os.path.join(p, bu))
            out.update({'bu_versao': b.get('versao'), 'bu_urna': b.get('urna'), 'bu_ab': b.get('ab'), 'bu_enc': b.get('enc'),
                        'bu_id': (b.get('mun'), b.get('zona'), b.get('secao'))})
        except Exception as e:
            out['bu_erro'] = str(e)
    if lg:
        try:
            d = ler_log_f11(os.path.join(p, lg))
            out['log'] = {di: {kk: (sorted(v) if isinstance(v, set) else dict(v) if isinstance(v, collections.Counter) else v)
                               for kk, v in r.items()} for di, r in d.items()}
        except Exception as e:
            out['log_erro'] = str(e)
    return out


def ler_pasta(pasta, dia, procs=4):
    from multiprocessing import Pool
    itens = [(k, p, dia) for k, p in _secoes_pasta(pasta)]
    with Pool(procs) as pool:
        res = pool.map(_uma_secao, itens, chunksize=8)
    return {r['k']: r for r in res}


def referencia_amostra(pasta_amostra, procs=4):
    """Urnas reais (amostra do 2º turno, logs com os dois turnos): versões, componentes por modelo e dia, falhas."""
    from multiprocessing import Pool
    itens = [(k, p, None) for k, p in _secoes_pasta(pasta_amostra)]
    with Pool(procs) as pool:
        res = pool.map(_uma_secao, itens, chunksize=16)
    ref = {}
    for dia in (D1T, D2T):
        versoes = collections.Counter(); comp = collections.defaultdict(collections.Counter); urnas = collections.Counter()
        falhas = []; bu_versoes = collections.Counter()
        for r in res:
            lg = (r.get('log') or {}).get(dia)
            if not lg or not lg['verif']:
                continue
            mod = (lg['modelos'] or ['?'])[0] if len(lg['modelos']) <= 1 else '+'.join(lg['modelos'])
            urnas[mod] += 1
            for v in lg['versoes']: versoes[v] += 1
            for c in lg['comp']: comp[mod][c] += 1
            if lg['verif_sem_sucesso']: falhas.append((r['k'], lg['verif_sem_sucesso'][:3]))
            if dia == D2T and r.get('bu_versao'): bu_versoes[r['bu_versao']] += 1
        ref[dia] = {'urnas_com_verificacao_no_dia': dict(urnas), 'versoes_no_log': dict(versoes),
                    'componentes_por_modelo': {m: dict(c) for m, c in comp.items()}, 'falhas': falhas,
                    'versoes_no_boletim_2t': dict(bu_versoes)}
    ref['secoes_lidas'] = len(res)
    return ref


def conferir(r, dia, urna_bweb, ref_dia, versao_ref):
    """Conferências (a) a (c) de D3 para uma seção baixada, num dia; (d) vem do verificar_assinaturas."""
    o = {'tem_bu': 'bu_versao' in r, 'tem_log': 'log' in r and dia in r['log']}
    lg = (r.get('log') or {}).get(dia, {})
    o['versao_bu'] = r.get('bu_versao'); o['versoes_log_no_dia'] = lg.get('versoes', [])
    o['modelo'] = lg.get('modelos', [])
    o['urna_bu'] = r.get('bu_urna'); o['urna_bweb'] = urna_bweb
    o['urna_bu_igual_bweb'] = (r.get('bu_urna') == urna_bweb) if r.get('bu_urna') is not None else None
    o['urnas_no_log_no_dia'] = lg.get('urnas', [])
    o['verificacoes_no_dia'] = lg.get('verif', 0)
    o['verificacoes_sem_sucesso_no_dia'] = lg.get('verif_sem_sucesso', [])
    # urna com log de contingência aninhado tem dois modelos: vale a união dos componentes de cada um e do par
    mods = lg.get('modelos') or ['?']
    conhecidos = set()
    for m in list(mods) + ['+'.join(mods)]:
        conhecidos |= set(ref_dia['componentes_por_modelo'].get(m, {}))
    o['componentes_fora_das_urnas_reais_do_modelo'] = sorted(set(lg.get('comp', [])) - conhecidos) if conhecidos else 'modelo sem referência'
    o['hab_no_dia'] = lg.get('hab', 0); o['bio_no_dia'] = lg.get('bio', 0)
    o['fase'] = lg.get('fase', []); o['modo_carga'] = lg.get('modo_carga', []); o['iniciando'] = lg.get('iniciando', [])
    o['midia_votacao'] = lg.get('midia_votacao', [])
    vers = set(o['versoes_log_no_dia']) | ({o['versao_bu']} if o['versao_bu'] else set())
    o['a_versao_diferente'] = sorted(v for v in vers if not v.startswith(versao_ref)) if vers else 'sem versão lida'
    o['b_componente_novo'] = o['componentes_fora_das_urnas_reais_do_modelo'] if isinstance(o['componentes_fora_das_urnas_reais_do_modelo'], list) else []
    o['c_sem_sucesso'] = o['verificacoes_sem_sucesso_no_dia']
    return o


def verificar_vsc(pasta):
    script = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'verificar_assinaturas.py')
    r = subprocess.run([sys.executable, '-I', script, pasta], capture_output=True, text=True, cwd=os.path.dirname(script))
    if r.returncode != 0:
        raise RuntimeError('verificar_assinaturas.py falhou em ' + pasta + ': ' + r.stderr[-2000:])
    return json.loads(r.stdout)


def gedai_correspondencias(zip_gedai, chaves):
    """Correspondências seção-urna transmitidas pelo Gedai (log público do 2º turno) para as seções dadas."""
    import io
    rx = re.compile(r'(Transmitida|Recebida|Cadastrada) a correspondência de seção: município (\d+), zona (\d+), seção (\d+), carga (\d+), id urna (\d+), mc (\S+?)\.?$')
    alvo = set(chaves); out = collections.defaultdict(set)
    z = zipfile.ZipFile(zip_gedai)
    for i in z.infolist():
        if not i.filename.endswith('.jez'): continue
        comp = i.filename.split('-')[5] if i.filename.count('-') > 5 else i.filename
        z1 = zipfile.ZipFile(io.BytesIO(z.read(i.filename)))
        for n1 in z1.namelist():
            if not n1.endswith('.jez'): continue
            z2 = zipfile.ZipFile(io.BytesIO(z1.read(n1)))
            for n2 in z2.namelist():
                for l in z2.read(n2).decode('latin1', errors='replace').splitlines():
                    p = l.split('\t')
                    if len(p) < 3: continue
                    m = rx.search(p[2])
                    if not m: continue
                    uf = os.path.basename(zip_gedai).split('_')[3]
                    k = f'{uf}|{int(m.group(2))}|{int(m.group(3))}|{int(m.group(4))}'
                    if k in alvo:
                        out[k].add((p[0], comp, m.group(1), int(m.group(6))))
    return {k: sorted(v, key=lambda x: x[0][6:10] + x[0][3:5] + x[0][:2] + x[0][11:]) for k, v in out.items()}


# ---------------------------------------------------------------------------------------------------------------
# Inventário do que foi publicado (pesquisa de 31/10/2026). Páginas jus.br (www.tse, TREs, sintse) deram HTTP 403 ao
# leitor e ao curl; o que vem delas saiu do resumo do buscador (confiança média ou baixa). Não houve contorno.
# ---------------------------------------------------------------------------------------------------------------
INVENTARIO = [
    {'categoria': 'lista de urnas', 'item': 'SP, lista completa', 'status': 'achado',
     'achado': '51 seções: 30 de integridade (Centro Cultural São Paulo), 3 com biometria (Unip Paraíso, 6ª zona), 10 de autenticidade e 8 de gestão de riscos (reserva para problemas no transporte). 34 das 51 escolhidas pelas entidades, sem dizer quais.',
     'fonte': FONTE_SP, 'data': '24/10/2026', 'confianca': 'alta para os números (as 51 casam com o bweb por zona, seção e município); reprodução secundária, a página do TRE-SP deu 403'},
    {'categoria': 'lista de urnas', 'item': 'AL, lista completa', 'status': 'achado',
     'achado': '23 seções: 18 de integridade (auditório da OAB, Maceió), 2 com biometria (Unima/Afya, 2ª zona, seções 355 e 365) e 3 de autenticidade.',
     'fonte': FONTE_AL, 'data': '24/10/2026', 'confianca': 'alta (as 23 casam com o bweb)'},
    {'categoria': 'lista de urnas', 'item': 'PB, lista parcial', 'status': 'achado em parte',
     'achado': 'Texto diz 23 urnas (20 de integridade, 1 com biometria, e 3 de autenticidade), mas lista 22 e só dá número de seção para 4 das de integridade (João Pessoa 1ª zona 297 com biometria; Cabedelo 181; Campina Grande 171 e 254, sem zona) e para as 3 de autenticidade. 4 indicadas pelas instituições, sem dizer quais.',
     'fonte': FONTE_PB, 'data': '24/10/2026', 'confianca': 'média'},
    {'categoria': 'lista de urnas', 'item': 'SC, GO, MG, PA, MS, RS, RJ, DF, MT, ES, PR e demais', 'status': 'lista existe ou foi anunciada, não lida',
     'achado': 'SC: página do TRE-SC com o resultado do sorteio (25 seções de integridade, mais biometria e autenticidade, pelo resumo do buscador). GO: 35 seções, 25 de integridade (2 com biometria) e 8 de autenticidade (soma 33, o texto diz 35). PA: 35 urnas, 25 de integridade e 8 de autenticidade (mesma conta que não fecha). MG: 33 de integridade e 10 de autenticidade, lista por região. MS: 20 e 3, em PDF. RS: 35 sorteadas. RJ: 31 de integridade, 2 com biometria (FGV) e 10 de autenticidade. DF: 20 (16 na CLDF, 2 no TSE, 2 com biometria na Escola Canadense). MT: 20 (1 com biometria). ES: 18 em ambiente controlado. PR: 27 (2 com biometria). RN: repete o 1º turno, 18 mais 2 com biometria e 3 de autenticidade. RR: 20 e 3. SP, MG, RJ e BA: 33 cada (Agência Brasil).',
     'fonte': 'https://www.tre-sc.jus.br/eleicoes/eleicoes-2026/resultado-do-sorteio-da-auditoria-no-2o-turno-das-eleicoes ; https://www.tre-go.jus.br/comunicacao/noticias/2026/Outubro/tre-go-sorteia-urnas-que-serao-auditadas-no-2o-turno ; https://www.tre-mg.jus.br/comunicacao/noticias/2026/Outubro/definidas-as-urnas-eletronicas-que-serao-auditadas-no-2o-turno ; https://www.tre-pa.jus.br/comunicacao/noticias/2026/Outubro/cerimonia-publica-sorteia-as-urnas-que-serao-auditadas-no-segundo-turno ; https://midiamax.com.br/politica/2026/tre-ms-sorteia-urnas-eletronicas-passarao-auditoria-2-turno-eleicoes-2026/ ; https://www.jornaldocomercio.com/politica/2026/10/1268088-tre-rs-realiza-auditoria-em-urnas-eletronicas-para-o-segundo-turno.html ; https://www.acessa.com/noticias/2026/10/342672-tre-rj-define-urnas-que-serao-auditadas-no-segundo-turno.html ; https://portaln10.com.br/politica/eleicoes/auditoria-urnas-eletronicas-rn-eleicoes-2026-352796/ ; https://bombabomba.com.br/urnas-eletronicas-sao-aprovadas-em-teste-de-integridade-realizado-na-cldf-no-2o-turno/ ; https://agenciabrasil.ebc.com.br/justica/noticia/2026-10/tribunais-eleitorais-definem-urnas-que-serao-auditadas-no-2o-turno',
     'data': '21 a 25/10/2026', 'confianca': 'média para os números (jus.br pelo resumo do buscador; RS atrás de assinatura); baixa para SC'},
    {'categoria': 'lista de urnas', 'item': 'Total nacional', 'status': 'não publicado', 'achado': 'Nenhuma fonte dá o total de urnas do teste no 2º turno.', 'fonte': '', 'data': '', 'confianca': ''},
    {'categoria': 'arquivos de urna do teste (boletim, RDV, log)', 'item': 'Publicação', 'status': 'não publicados',
     'achado': 'Nenhum arquivo de urna do teste foi achado em TSE, TREs, dados abertos ou imprensa. A Portaria TSE 765/2024, que regulou o teste com biometria em 2024, diz no art. 19: "É vedado o fornecimento dos arquivos de imagem do Boletim de Urna (BU), do Registro Digital do Voto (RDV) e dos logs das urnas objetos do teste de integridade." O buscador atribuiu o mesmo texto à Res. TSE 23.758/2026 numa busca e não o achou nela em outra; não confirmei se a vedação vale em 2026 nem se cobre a modalidade em ambiente controlado. No site de resultados, o pacote das seções do teste é o da urna reserva (ver a conferência).',
     'fonte': 'https://www.tse.jus.br/legislacao/compilada/prt/2024/portaria-no-765-de-21-de-setembro-de-2024 ; https://www.tse.jus.br/legislacao/compilada/res/2026/resolucao-no-23-758-de-2-de-marco-de-2026',
     'data': '21/09/2024 e 02/03/2026', 'confianca': 'média para a regra de 2024; baixa para a mesma regra em 2026 (páginas 403)'},
    {'categoria': 'contagem das cédulas', 'item': 'Quantidade e composição', 'status': 'só totais parciais',
     'achado': 'TSE (Museu do Voto): 389 votos em 2 urnas. SP: "mais de 16 mil cédulas" preenchidas para o 2º turno (no 1º, 16.400 = 400 por urna x 41 urnas). Demais UFs: não publicado. Composição das cédulas (quantos votos em cada candidato, brancos e nulos): não publicada em nenhuma UF.',
     'fonte': 'https://www.tse.jus.br/comunicacao/noticias/2026/Outubro/teste-de-integridade-do-2o-turno-no-tse-confirma-correspondencia-entre-cedulas-e-votos-nas-urnas ; https://www.tre-sp.jus.br/comunicacao/noticias/2026/Outubro/eleicoes-2026-urnas-eletronicas-serao-submetidas-a-novas-auditorias-para-o-2o-turno-em-sp',
     'data': '25/10/2026', 'confianca': 'média (resumo do buscador)'},
    {'categoria': 'relatórios', 'item': 'TCU', 'status': 'fiscalização autorizada; relatório ainda não publicado',
     'achado': 'Acórdão 2.558/2026-TCU-Plenário (TC 019.754/2026-4, 16/09/2026, relator Odair Cunha), lido no PDF: autoriza a fiscalização dos testes de integridade com e sem biometria nos 27 TREs, custo previsto de R$ 1.000.010,00 (404 HDs), com base no Acordo de Cooperação Técnica 51/2026 (vigência até 31/12/2031). Relatório consolidado ao TSE em até 30 dias corridos depois do 2º turno (até 24/11/2026): não saiu.',
     'fonte': 'https://static.poder360.com.br/uploads/2026/09/019.754-2026-4-OJC-Proposta-de-Fiscalizacao-Integridade-das-Urnas.pdf ; https://www.tse.jus.br/comunicacao/noticias/2026/Outubro/eleicoes-de-2026-terao-acompanhamento-do-tcu-nos-testes-de-integridade-das-urnas-eletronicas',
     'data': '16/09/2026', 'confianca': 'alta (documento primário lido)'},
    {'categoria': 'relatórios', 'item': 'Empresas de auditoria externa dos TREs', 'status': 'não localizados (2026)',
     'achado': 'Relatórios de 2026 não localizados (em 2024 saíram no site do TSE, um por UF e turno). Pelo atestado do TRE-AL sobre o contrato de 2022 (Maciel Consultores), o relatório conclusivo traz o relatório de resultados divergentes do sistema de apoio (comparação entre o RDV da urna e as cédulas digitadas), a contagem manual independente de pelo menos uma urna e cópias digitalizadas da zerésima e do boletim da urna e do sistema de apoio (art. 66, § 1º, da Res. 23.673/2021). São os únicos documentos por urna previstos.',
     'fonte': 'https://static.tre-al.jus.br/portal/transparencia/contratacoes/solicitacoes-de-contratacao/2026/act13.pdf ; https://www.tse.jus.br/eleicoes/eleicoes-2024-content/arquivos-teste-de-integridade/arquivos-segundo-turno/rs-relatorio-auditoria-externa-2024-2o-turno-ass',
     'data': '30/06/2026 (atestado)', 'confianca': 'alta para o escopo (documento primário lido); não localizado para 2026'},
    {'categoria': 'relatórios', 'item': 'Atas do 2º turno', 'status': 'existem em SP, não lidas',
     'achado': 'O TRE-SP publicou as atas do teste de integridade e do teste com biometria do 2º turno e a lista de urnas (resumo do buscador da página "Dados, arquivos e relatórios"). Atas de outros TREs: não localizadas.',
     'fonte': 'https://www.tre-sp.jus.br/eleicoes/eleicoes-2026/dados-arquivos-e-relatorios', 'data': '10/2026', 'confianca': 'baixa (página 403)'},
    {'categoria': 'divergência do DF', 'item': 'Relatório ou ata', 'status': 'não localizado',
     'achado': 'Só a nota: das 16 urnas da CLDF, "a única divergência verificada foi um erro humano de digitação" (juiz João Marcos Guimarães Silva). Urna, seção, cargo, número de votos, direção e trecho do vídeo: não divulgados.',
     'fonte': 'Agência CLDF, 25/10/2026 18h45, reproduzida em https://bombabomba.com.br/urnas-eletronicas-sao-aprovadas-em-teste-de-integridade-realizado-na-cldf-no-2o-turno/', 'data': '25/10/2026', 'confianca': 'média (reprodução de agência oficial)'},
    {'categoria': 'vídeos', 'item': 'Transmissões', 'status': 'existem, não assistidas',
     'achado': 'Transmissão ao vivo no YouTube: TSE (Museu do Voto, câmeras 24 horas), TV Câmara Distrital (CLDF), canais dos TREs (AL, PA e outros), Alesc (SC). Pelo estudo técnico preliminar do TRE-AL (10/07/2026): uma câmera por urna focada no terminal do eleitor, mais 4 de ambiente, microfone para quem canta o voto, gravação em 2 vias mais 2 de reserva, e gravação além das 17h "caso haja incongruência nos resultados". O trecho da divergência do DF não foi localizado.',
     'fonte': 'https://static.tre-al.jus.br/portal/transparencia/contratacoes/solicitacoes-de-contratacao/2026/497757-etp.pdf ; https://www.tse.jus.br/comunicacao/noticias/2026/Outubro/tse-realiza-teste-de-integridade-das-urnas-eletronicas-no-museu-do-voto',
     'data': '10/07/2026 e 25/10/2026', 'confianca': 'alta para o contrato de AL (documento primário lido); média para o resto'},
    {'categoria': 'dados abertos', 'item': 'Logs do Gedai do 2º turno', 'status': 'achado e lido (AL, SP e PB)',
     'achado': 'Conjunto "Resultados - 2026 - Logs do sistema de preparação das urnas eletrônicas (Gedai) - 2º turno", 27 UFs e exterior, carregados em 24/10 (13h29) e 25/10 (13h27). Formato zip > jez > jez > gedai-ue.log. Registra a correspondência seção-urna transmitida por computador. Não há registro do teste de integridade como tal.',
     'fonte': 'https://dadosabertos.tse.jus.br/dataset/resultados-2026-logs-do-sistema-de-preparacao-das-urnas-eletronicas-gedai-2-turno', 'data': '24 e 25/10/2026', 'confianca': 'alta (arquivo baixado, SHA-512 igual ao publicado)'},
    {'categoria': 'norma', 'item': 'Res. TSE 23.758/2026', 'status': 'achado (texto citado em documento primário)',
     'achado': 'O estudo técnico preliminar do TRE-AL transcreve a redação dada pela Res. 23.758/2026 à Res. 23.673/2021: duas modalidades (ambiente controlado, com servidores, e com biometria de voluntários perto das seções); art. 53-A; art. 59-A: de 5% a 10% das urnas do teste com biometria. A cartilha do TRE-SP de 2026 cita "Res. 23.769/2026" para o mesmo assunto (numeração diferente).',
     'fonte': 'https://static.tre-al.jus.br/portal/transparencia/contratacoes/solicitacoes-de-contratacao/2026/497757-etp.pdf ; https://www.tre-sp.jus.br/eleicoes/eleicoes-2026/arquivos/cartilha-auditorias-da-urna-eletronica-e-dos-sistemas-eleitorais-no-dia-da-eleicao/@@display-file/file/auditorias-2026.pdf',
     'data': '10/07/2026', 'confianca': 'alta (AL); baixa (número 23.769, só pelo buscador)'},
]

# Boletim contra cédulas no 2º turno, pelo que foi publicado (D8). Classificação de cada divergência por D2.
RESULTADOS = [
    {'uf': 'DF (TSE, Museu do Voto)', 'urnas': 2, 'votos': 389, 'divergencias': 0, 'texto': 'auditoria terminou sem divergências', 'fonte': 'https://www.tse.jus.br/comunicacao/noticias/2026/Outubro/teste-de-integridade-do-2o-turno-no-tse-confirma-correspondencia-entre-cedulas-e-votos-nas-urnas', 'confianca': 'média (resumo do buscador)'},
    {'uf': 'DF (CLDF)', 'urnas': 16, 'votos': None, 'divergencias': 1, 'texto': '"a única divergência verificada foi um erro humano de digitação" (juiz João Marcos Guimarães Silva)',
     'explicacao': 'documentada incompleta: causa dada pela autoridade do teste em nota oficial; urna, cargo, votos, direção e vídeo não publicados',
     'leitura_estrita': 'não há ata nem relatório publicado com o voto identificado; aciona o sinal por falta de documento',
     'fonte': 'https://bombabomba.com.br/urnas-eletronicas-sao-aprovadas-em-teste-de-integridade-realizado-na-cldf-no-2o-turno/', 'confianca': 'média'},
    {'uf': 'DF (biometria, Escola Canadense)', 'urnas': 2, 'votos': None, 'divergencias': None, 'texto': 'resultado não publicado à parte', 'fonte': '', 'confianca': ''},
    {'uf': 'SP', 'urnas': 33, 'votos': None, 'divergencias': 0, 'texto': 'concluído sem divergências (30 no CCSP e 3 com biometria na Unip)', 'fonte': 'https://www.tre-sp.jus.br/comunicacao/noticias/2026/Outubro/teste-de-integridade-das-urnas-no-2o-turno-e-concluido-sem-divergencias-em-sao-paulo', 'confianca': 'média (resumo do buscador)'},
    {'uf': 'SC', 'urnas': 27, 'votos': None, 'divergencias': 0, 'texto': '27 urnas, 2 com biometria; "sem intercorrências"', 'fonte': 'https://www.tre-sc.jus.br/comunicacao/noticias/2026/Outubro/teste-de-integridade-confirma-seguranca-da-urna-e-reforca-a-transparencia-das-eleicoes-2026', 'confianca': 'média (resumo do buscador)'},
    {'uf': 'AL', 'urnas': 20, 'votos': None, 'divergencias': None, 'texto': 'notícia do resultado (23 urnas auditadas) não fala em divergência', 'fonte': 'https://www.cadaminuto.com.br/noticia/2026/10/27/eleicoes-2026-23-urnas-eletronicas-foram-auditadas-durante-o-2-turno-em-al', 'confianca': 'média'},
    {'uf': 'MT', 'urnas': 20, 'votos': None, 'divergencias': None, 'texto': 'notícia do TRE-MT sem frase explícita de resultado no resumo; nota interna anterior dizia "sem divergência", não confirmada', 'fonte': 'https://www.tre-mt.jus.br/comunicacao/noticias/2026/Outubro/teste-de-integridade-reforca-seguranca-e-confiabilidade-da-urna-eletronica-no-2o-turno', 'confianca': 'baixa'},
    {'uf': 'demais UFs', 'urnas': None, 'votos': None, 'divergencias': None, 'texto': 'só anúncio do sorteio ou notícia sem resultado; nenhuma outra divergência relatada', 'fonte': '', 'confianca': ''},
]


def _resumo_conf(confs):
    """Agrega conferências (a) a (c) e de identificação de várias seções."""
    c = collections.Counter()
    for k, o in confs.items():
        c['secoes'] += 1
        c['com_boletim'] += bool(o['tem_bu']); c['com_log_no_dia'] += bool(o['tem_log'])
        c['a_versao_diferente'] += isinstance(o['a_versao_diferente'], list) and bool(o['a_versao_diferente'])
        c['sem_versao_lida'] += not isinstance(o['a_versao_diferente'], list)
        c['b_componente_novo'] += bool(o['b_componente_novo'])
        c['c_verificacao_sem_sucesso'] += bool(o['c_sem_sucesso'])
        c['urna_do_boletim_diferente_do_bweb'] += (o['urna_bu_igual_bweb'] is False)
        c['urna_do_boletim_nao_lida'] += (o['urna_bu_igual_bweb'] is None)
        c['habilitacoes'] += o['hab_no_dia']; c['biometricas'] += o['bio_no_dia']
    return dict(c)


def _falhas_vsc(v, chaves):
    al = set(chaves)
    return [f for f in v.get('falhas', []) if f[0] in al]


def analisar(trab, dl1p, dl2p, dl1s, dl2s, amostra, gedai_al, secoes_gz, saida_json, saida_txt):
    import gzip
    from modelos import modelo
    sel = json.load(open(os.path.join(trab, 'selecao.json')))
    base = json.load(gzip.open(secoes_gz))
    ref_path = os.path.join(trab, 'ref_amostra.json')
    ref = json.load(open(ref_path)) if os.path.exists(ref_path) else referencia_amostra(amostra)
    if not os.path.exists(ref_path):
        json.dump(ref, open(ref_path, 'w'), ensure_ascii=False)
    v1 = list(ref[D1T]['versoes_no_log']); v2 = list(ref[D2T]['versoes_no_log'])
    versao_ref = v1[0] if len(v1) == 1 else None
    S = sel['S']; T = sel['T']; lis = {r['chave']: r for r in sel['listadas'] if r.get('chave')}
    extras = sel.get('extras_de_lista', []); controles = sel['controles']
    d1 = ler_pasta(dl1p, None); d1.update(ler_pasta(dl1s, None))
    d2 = ler_pasta(dl2p, None)
    tem_2t_S = dl2s not in ('-', '') and os.path.isdir(dl2s)
    if tem_2t_S:
        d2.update(ler_pasta(dl2s, None))
    vsc = {'1t_prior': verificar_vsc(dl1p), '2t_prior': verificar_vsc(dl2p), '1t_S': verificar_vsc(dl1s),
           '2t_S': verificar_vsc(dl2s) if tem_2t_S else {'contagem': 'não baixado (D6 pede só o 1º turno de S)'}}
    for nome, v in vsc.items():
        json.dump(v, open(os.path.join(trab, f'vsc_{nome}.json'), 'w'), ensure_ascii=False, indent=1, default=str)
    vsc = {n: (v if isinstance(v.get('contagem'), dict) else {**v, 'falhas': []}) for n, v in vsc.items()}
    falhas_vsc1 = vsc['1t_prior'].get('falhas', []) + vsc['1t_S'].get('falhas', [])
    falhas_vsc2 = vsc['2t_prior'].get('falhas', []) + vsc['2t_S'].get('falhas', [])

    def urna1(k): return base[k]['1']['urna']
    def urna2(k): return lis[k]['urna2'] if k in lis else S[k]['urna2']
    vref = versao_ref.split(' - ')[0] if versao_ref else '10.23.0.0'
    conf_T1 = {k: conferir(d1.get(k, {}), D1T, urna1(k), ref[D1T], vref) for k in T}
    conf_T2 = {k: conferir(d2.get(k, {}), D2T, urna2(k), ref[D2T], vref) for k in T}
    conf_X1 = {k: conferir(d1.get(k, {}), D1T, urna1(k), ref[D1T], vref) for k in extras}
    conf_X2 = {k: conferir(d2.get(k, {}), D2T, urna2(k), ref[D2T], vref) for k in extras}
    conf_C1 = {k: conferir(d1.get(k, {}), D1T, urna1(k), ref[D1T], vref) for k in controles}
    conf_C2 = {k: conferir(d2.get(k, {}), D2T, urna2(k), ref[D2T], vref) for k in controles}
    conf_S1 = {k: conferir(d1.get(k, {}), D1T, urna1(k), ref[D1T], vref) for k in S}
    conf_S2 = {k: conferir(d2.get(k, {}), D2T, urna2(k), ref[D2T], vref) for k in S if k in d2}
    # (d) assinatura do pacote, por seção
    fv1 = collections.defaultdict(list); fv2 = collections.defaultdict(list)
    for f in falhas_vsc1: fv1[f[0]].append(f[1:])
    for f in falhas_vsc2: fv2[f[0]].append(f[1:])
    # carga das reservas no 24/10 (log e bweb) e verificações da carga
    carga = {}
    for k in list(T) + extras + [c for c in controles if c in S] + [k for k in S]:
        lg = (d2.get(k, {}).get('log') or {}).get('24/10/2026', {})
        carga[k] = {'bweb': lis[k]['carga2'] if k in lis else S[k]['carga2'], 'log_primeira': lg.get('primeira'), 'log_ultima': lg.get('ultima'),
                    'versoes_24_10': lg.get('versoes', []), 'verificacoes_carga': lg.get('verif_outras_apps', {}),
                    'sem_sucesso_24_10': lg.get('verif_sem_sucesso', [])}
    # tabela por urna de T
    tabela_T = []
    for k in T:
        r = lis[k]; a, b = conf_T1[k], conf_T2[k]
        tabela_T.append({'secao': k, 'municipio': r.get('mun_bweb'), 'tipo_no_teste': {'I': 'ambiente controlado', 'B': 'com biometria'}[r['tipo']],
                         'urna_testada': r['urna1'], 'modelo_urna_testada': (a['modelo'] or [modelo(r['urna1'], 2026)])[0],
                         'versao_boletim_1t': a['versao_bu'], 'versao_log_04_10': a['versoes_log_no_dia'],
                         'verificacoes_04_10': a['verificacoes_no_dia'], 'sem_sucesso_04_10': len(a['c_sem_sucesso']),
                         'componente_fora_das_reais': a['b_componente_novo'], 'vsc_1t_falhas': fv1.get(k, []),
                         'urna_boletim_igual_bweb_1t': a['urna_bu_igual_bweb'],
                         'parte_biometrica_1t': round(a['bio_no_dia'] / a['hab_no_dia'], 3) if a['hab_no_dia'] else None,
                         'urna_testada_votou_no_2t': r.get('urna1_efetivada_no_2t_em', []),
                         'urna_reserva': r['urna2'], 'modelo_reserva': (b['modelo'] or [modelo(r['urna2'], 2026)])[0],
                         'carga_reserva_bweb': r['carga2'], 'carga_reserva_log': [carga[k]['log_primeira'], carga[k]['log_ultima']],
                         'versao_reserva_25_10': b['versoes_log_no_dia'], 'sem_sucesso_reserva_25_10': len(b['c_sem_sucesso']),
                         'componente_fora_reserva': b['b_componente_novo'], 'vsc_2t_falhas': fv2.get(k, []),
                         'urna_boletim_igual_bweb_2t': b['urna_bu_igual_bweb'],
                         'parte_biometrica_2t': round(b['bio_no_dia'] / b['hab_no_dia'], 3) if b['hab_no_dia'] else None,
                         'pacotes_no_aux_2t': d2.get(k, {}).get('aux_hashes')})
    difv = lambda o: isinstance(o['a_versao_diferente'], list) and bool(o['a_versao_diferente'])
    sinal_T = [t['secao'] for t in tabela_T if (difv(conf_T1[t['secao']]) or conf_T1[t['secao']]['b_componente_novo']
                                                 or conf_T1[t['secao']]['c_sem_sucesso'] or fv1.get(t['secao'])
                                                 or conf_T1[t['secao']]['urna_bu_igual_bweb'] is False)]
    sem_arquivo_T = [k for k in T if not conf_T1[k]['tem_log'] or not conf_T1[k]['tem_bu'] or k not in {x for x in d1}]
    # superconjunto S
    resumo = {'T_1t': _resumo_conf(conf_T1), 'T_2t_reservas': _resumo_conf(conf_T2), 'extras_1t': _resumo_conf(conf_X1),
              'extras_2t': _resumo_conf(conf_X2), 'controles_1t': _resumo_conf(conf_C1), 'controles_2t': _resumo_conf(conf_C2),
              'S_1t': _resumo_conf(conf_S1), 'S_2t_reservas': _resumo_conf(conf_S2)}
    for nome, chaves, fv in (('T_1t', T, fv1), ('T_2t_reservas', T, fv2), ('S_1t', S, fv1), ('S_2t_reservas', S, fv2),
                             ('controles_1t', controles, fv1), ('controles_2t', controles, fv2), ('extras_1t', extras, fv1), ('extras_2t', extras, fv2)):
        resumo[nome]['d_secoes_com_falha_no_vsc'] = sum(1 for k in chaves if fv.get(k))
    det_S = {'S_1t_problemas': {k: {'a': o['a_versao_diferente'], 'b': o['b_componente_novo'], 'c': o['c_sem_sucesso'][:3], 'd': fv1.get(k, []),
                                    'urna_bu_igual_bweb': o['urna_bu_igual_bweb'], 'tem_log': o['tem_log'], 'tem_bu': o['tem_bu']}
                                for k, o in conf_S1.items() if o['a_versao_diferente'] or o['b_componente_novo'] or o['c_sem_sucesso'] or fv1.get(k) or o['urna_bu_igual_bweb'] is not True or not o['tem_log']},
             'S_2t_problemas': {k: {'a': o['a_versao_diferente'], 'b': o['b_componente_novo'], 'c': o['c_sem_sucesso'][:3], 'd': fv2.get(k, []),
                                    'urna_bu_igual_bweb': o['urna_bu_igual_bweb'], 'tem_log': o['tem_log'], 'tem_bu': o['tem_bu']}
                                for k, o in conf_S2.items() if o['a_versao_diferente'] or o['b_componente_novo'] or o['c_sem_sucesso'] or fv2.get(k) or o['urna_bu_igual_bweb'] is not True or not o['tem_log']}}
    modelos_T = collections.Counter(t['modelo_urna_testada'] for t in tabela_T)
    modelos_S = collections.Counter((conf_S1[k]['modelo'] or [S[k]['modelo_urna1']])[0] for k in S)
    carga_S = collections.Counter((S[k]['carga2'][11:13] + 'h') for k in S)
    d5 = {'T_urna_testada_votou_no_2t': sum(1 for t in tabela_T if t['urna_testada_votou_no_2t']),
          'S_urna1_votou_no_2t': sum(1 for k in S if S[k]['urna1_efetivada_no_2t_em']),
          'trocas_de_urna_no_pais': sel.get('trocas_de_urna'), 'troca_fora_de_S_por_uf': sel.get('troca_fora_de_S_urna1_sem_voto_no_2t_por_uf')}
    gedai = {}
    for zg in [z for z in (gedai_al or '').split(',') if z and os.path.exists(z)]:
        uf = os.path.basename(zg).split('_')[3]
        alvo = [k for k in list(lis) + extras if k.startswith(uf + '|')]
        g = gedai_correspondencias(zg, alvo)
        for k in alvo:
            gedai.setdefault(k, g.get(k, []))
    gedai_res = {}
    for k, ev in gedai.items():
        r = lis.get(k) or {'tipo': 'candidata (lista ambígua)', 'urna1': S[k]['urna1'], 'urna2': S[k]['urna2']}
        gedai_res[k] = {'tipo': r['tipo'], 'urna1': r['urna1'], 'urna2': r['urna2'],
                        'urna1_transmitida': [e[0] for e in ev if e[3] == r['urna1']],
                        'urna2_transmitida': [e[0] for e in ev if e[3] == r['urna2']],
                        'computadores': sorted({e[1] for e in ev}),
                        'outras_urnas': sorted({(e[3], e[0]) for e in ev if e[3] not in (r['urna1'], r['urna2'])})}
    divergencias = [x for x in RESULTADOS if x.get('divergencias')]
    sinal_boletim_D2 = [x['uf'] for x in divergencias if not x.get('explicacao', '').startswith('documentada')]
    sinal_boletim_estrito = [x['uf'] for x in divergencias]
    sinal = bool(sinal_T or sinal_boletim_D2)
    veredito = ('SINAL' if sinal else 'SEM SINAL') + (' (por extensão, D3: programa da urna de teste diferente)' if sinal_T else '')
    out = {'teste': 'F11', 'registro': 'PRE-REGISTRO-2026-10-26.md, Adendo 21, F11 (commit 913af7a)', 'veredito': veredito,
           'veredito_detalhe': {'arquivos_do_teste_publicados': False,
                                'boletim_contra_cedulas': {'divergencias_publicadas': divergencias, 'sinal_por_D2': sinal_boletim_D2,
                                                           'sinal_na_leitura_estrita': sinal_boletim_estrito},
                                'programa_por_extensao_D3': {'urnas_de_teste_identificadas': len(T), 'com_problema': sinal_T,
                                                             'sem_arquivo': sem_arquivo_T}},
           'referencia_urnas_reais': {'versao': versao_ref, 'versoes_04_10': ref[D1T]['versoes_no_log'], 'versoes_25_10': ref[D2T]['versoes_no_log'],
                                      'urnas_com_verificacao_04_10': ref[D1T]['urnas_com_verificacao_no_dia'],
                                      'componentes_por_modelo_04_10': {m: len(c) for m, c in ref[D1T]['componentes_por_modelo'].items()},
                                      'falhas_04_10': ref[D1T]['falhas'], 'falhas_25_10': ref[D2T]['falhas']},
           'inventario': INVENTARIO, 'resultados_publicados': RESULTADOS,
           'listas_contra_bweb': sel['listadas'], 'S_total': len(S), 'T': T, 'extras_de_lista': extras, 'controles': controles,
           'tabela_T': tabela_T, 'extras': {k: {'1t': conf_X1[k], '2t': conf_X2[k], 'vsc1': fv1.get(k, []), 'vsc2': fv2.get(k, [])} for k in extras},
           'controles_detalhe': {k: {'tipo': lis[k]['tipo'], 'em_S': lis[k].get('em_S'), 'urna1': lis[k]['urna1'], 'urna2': lis[k]['urna2'],
                                     'carga2': lis[k]['carga2'], 'versao_1t': conf_C1[k]['versoes_log_no_dia'], 'versao_2t': conf_C2[k]['versoes_log_no_dia'],
                                     'sem_sucesso': len(conf_C1[k]['c_sem_sucesso']) + len(conf_C2[k]['c_sem_sucesso'])} for k in controles},
           'resumos': resumo, 'S_detalhe_problemas': det_S, 'vsc_contagens': {n: v.get('contagem') for n, v in vsc.items()},
           'vsc_emissores': {n: v.get('emissores') for n, v in vsc.items()}, 'vsc_chaves_software': {n: v.get('chaves_software') for n, v in vsc.items()},
           'modelos_T': dict(modelos_T), 'modelos_S_urna1': dict(modelos_S), 'carga_S_por_hora': dict(sorted(carga_S.items())),
           'D5': d5, 'gedai_AL': gedai_res, 'carga_reservas': {k: carga[k] for k in list(T) + extras},
           'S_por_uf': dict(sorted(collections.Counter(k.split('|')[0] for k in S).items())), 'S_dict_keys': sorted(S)}
    out['pistas'] = montar_pistas(out, ref)
    out['significado'] = SIGNIFICADO; out['desvios'] = DESVIOS
    json.dump(out, open(saida_json, 'w'), ensure_ascii=False, indent=1, default=str)
    escrever_txt(out, saida_txt)
    print('veredito', veredito)


def escrever_txt(o, caminho):
    open(caminho, 'w').write(texto_resultado(o))


# Urnas de integridade anunciadas para o 2º turno (com e sem biometria), por UF, com a fonte no inventário e no L7.
ANUNCIADO = {'SP': 33, 'MG': 33, 'RJ': 33, 'BA': 33, 'PR': 27, 'RS': 27, 'PE': 27, 'CE': 27, 'SC': 27, 'RR': 20, 'DF': 20,
             'AL': 20, 'MT': 20, 'PB': 20, 'MS': 20, 'ES': 18, 'GO': 25, 'PA': 25, 'RN': 20}

SIGNIFICADO = [
    'Quem está de fora não consegue conferir o teste de integridade do 2º turno arquivo por arquivo: não foi publicado o boletim, o RDV '
    'nem o log de nenhuma urna testada, e uma portaria de 2024 veda fornecê-los. O que existe é a palavra dos TREs (sem divergência no TSE, '
    'em SP e em SC; uma no DF, atribuída a digitação), atas e vídeos que não deu para ler, e, mais tarde, os relatórios das empresas de '
    'auditoria (com cópia digitalizada do boletim e da zerésima de cada urna) e o do TCU, previsto até 24/11/2026.',
    'O que dá para conferir de fora é a identidade e o programa das urnas testadas, por um caminho indireto: a urna testada é a que votou '
    'na seção no 1º turno, com a mesma carga, e os arquivos públicos dela no 1º turno mostram a mesma versão, os mesmos componentes '
    'verificados com sucesso e o certificado da própria urna validando as assinaturas, como nas urnas reais. Isso afasta a hipótese de '
    'terem ido para o teste aparelhos com outro programa instalado: nas urnas das listas de SP, AL e PB, nome por nome, e, sem lista, '
    'no grupo S inteiro, que contém as urnas de teste das outras UFs.',
    'O que isso não afasta: um programa igual em todas as urnas que se comportasse de outro jeito ao perceber que está em teste (L7). Esse '
    'cenário não deixa marca nos arquivos do 1º turno nem nas reservas; só o log do próprio teste mostraria o que a urna viu (habilitação, '
    'volume, ritmo). Também não afasta uma troca do programa da urna testada entre o 1º turno e o dia do teste, que só o log do teste '
    'mostraria. Essas duas portas continuam fechadas só pela inspeção do código e pela cadeia de compilação e assinatura do TSE.',
    'A única discordância entre urna e papel em 2026 (DF, 2º turno) segue sem urna, cargo, tamanho, direção e trecho de vídeo publicados. '
    'Um erro de digitação conferido pelo vídeo não tem a cara de fraude (seria um voto isolado, sem direção sistemática), mas hoje isso é '
    'afirmação da autoridade do teste, não dado público.',
    'Os registros públicos mostram que o procedimento deixou a marca prevista: nas listas de SP e AL, todas as seções de integridade '
    'votaram numa reserva carregada no sábado, a urna original não votou em lugar nenhum no 2º turno, as de autenticidade ficaram com a '
    'urna e a carga de setembro, e o Gedai registrou a correspondência da reserva no sábado (menos numa seção de SP, sem registro). Não há sinal de que o teste tenha usado '
    'urnas diferentes das sorteadas, mas a conferência do papel continua dependendo do que os TREs publicarem.',
]

DESVIOS = [
    'O registro pede a conferência nos arquivos do teste. Como nenhum foi publicado, a parte do programa foi feita por extensão (D3), com '
    'os arquivos do 1º turno das mesmas urnas, e a parte do boletim contra cédulas ficou no que foi publicado (D8). Decisões D1 a D8 '
    'escritas no docstring antes de baixar ou ler arquivo de urna das seções do teste.',
    '"Explicação documentada" (D2): adotei a leitura em que a causa dada em nota oficial basta, e relato também a leitura estrita, em que '
    'o caso do DF acionaria o sinal por falta de ata ou relatório publicado.',
    'T só com seções de lista que estão em S. Ficou de fora a seção com biometria de João Pessoa (PB|20516|1|297): a reserva carregada no '
    'sábado (urna 01797582) foi trocada por uma urna de contingência carregada em setembro (01659991) às 13h35 do domingo, e por isso a '
    'seção não entra em S. Ficaram de fora também as duas seções de Campina Grande, de lista ambígua (sem zona); a única candidata de '
    'cada uma em S foi conferida. As três passam em todas as conferências; incluí-las não muda nada.',
    'Componentes comparados só nas verificações do aplicativo de votação na inicialização (GAP). As da carga (SCUE) ficaram à parte porque, '
    'ao montar a referência e antes de ler qualquer urna de teste, apareceu na amostra uma urna de SP com a carga gravada com o relógio um '
    'mês adiantado e outro formato de linha. Resultado sem SUCESSO é contado em qualquer aplicativo.',
    'Correção feita depois de ver os dados das reservas: a comparação de componentes de log com duas urnas (contingência) usava só o '
    'primeiro modelo e marcou por engano um componente da UE2015 na seção de João Pessoa; passou a usar a união dos modelos presentes. '
    'Não afeta nenhuma urna de T no 1º turno (nenhuma tem dois modelos no log).',
    'A lista de SP veio de reprodução da imprensa (a página do TRE-SP deu 403), lida por leitor automático; foi conferida contra o bweb: '
    'as 51 seções casam por zona, seção e município. A de AL também casa nas 23.',
    'RDV não baixado: o do teste não existe publicado, e o das urnas reais não entra na conferência do registro.',
    'Reservas de S no 2º turno: só as de T, dos controles e das extras foram baixadas. A D6 pede o 1º turno de S; o download das '
    'demais reservas foi parado de propósito antes de começar.',
    'S é a definição do L7 (urna do 2º turno diferente e carga em 24/10). Ela deixa de fora seções do teste cuja reserva foi trocada no '
    'domingo (como a de João Pessoa) e inclui trocas de sábado que não são teste (em SP, 7 das 8 seções de gestão de riscos e mais 32).',
]


def montar_pistas(o, ref):
    P = []
    div = [x for x in o['resultados_publicados'] if x.get('divergencias')]
    P.append('Divergência do DF (CLDF, 2º turno): pedir ao TRE-DF (Lei de Acesso à Informação) urna, seção, cargo, voto digitado e voto '
             'da cédula, horário e trecho do vídeo. No TRE-AL, pelo estudo técnico da contratação, cada urna do teste tem câmera própria e '
             'gravação em 4 vias; se o DF seguiu o mesmo padrão (a CLDF transmitiu ao vivo), o trecho existe. Depende de pedir; fica '
             'para quem puder.')
    P.append('Relatórios das empresas de auditoria externa de 2026 e relatório consolidado do TCU (até 24/11/2026): pelo art. 66, § 1º, '
             'da Res. 23.673, cada relatório traz a contagem manual independente de pelo menos uma urna e cópia digitalizada da zerésima e '
             'do boletim da urna e do sistema de apoio. Serão os únicos documentos por urna do teste. Acompanhar o site do TSE '
             '(arquivos-teste-de-integridade) e o do TCU (TC 019.754/2026-4).')
    for k, f in [x for x in ref[D1T]['falhas'] if x[0] == 'BA|33553|169|132']:
        P.append(f'Urna real com verificação de assinatura sem SUCESSO no dia do 1º turno: {k}, {f[0]}. Na amostra, é a única entre '
                 f'{_n(sum(ref[D1T]["urnas_com_verificacao_no_dia"].values()))} urnas com log do 04/10. A urna recusou iniciar ("Erro na '
                 f'verificação de integridade do sistema", "Validação de árvore genérica mal sucedida"), foi desligada e substituída por '
                 f'contingência (urna 02277331, 08h36). É o comportamento previsto, mas a causa (mídia ou aparelho) não é pública.')
    outras = [x for x in ref[D1T]['falhas'] + ref[D2T]['falhas'] if x[0] != 'BA|33553|169|132']
    if outras:
        P.append('Outras urnas reais com verificação sem SUCESSO na amostra: ' + json.dumps(outras, ensure_ascii=False)[:600])
    sp = collections.Counter(k.split('|')[0] for k in o['S_dict_keys'])
    exc = {uf: (sp.get(uf, 0), ANUNCIADO[uf]) for uf in ANUNCIADO if sp.get(uf, 0) != ANUNCIADO[uf]}
    P.append('Grupo S diferente do número anunciado (seções em S contra urnas de integridade anunciadas): '
             + '; '.join(f'{uf} {a} contra {b}' for uf, (a, b) in sorted(exc.items())) + '. Em SP, 7 das 8 seções de "gestão de '
             'riscos" (reserva para problemas no transporte) também tiveram a urna retirada no sábado (a urna original não votou no 2º '
             'turno); sobram 32 trocas de sábado em SP sem explicação na lista. Podem ser trocas comuns de véspera; não dá para saber.')
    g = o['gedai_AL']
    for k, v in sorted(g.items()):
        if v['tipo'] in ('I', 'B') and not [d for d in v['urna2_transmitida'] if d.startswith('24/10')] and not [d for (u, d) in v['outras_urnas'] if d.startswith('24/10')]:
            P.append(f'Gedai: na seção de integridade {k} não aparece, no log público do 2º turno, a correspondência da urna reserva '
                     f'{v["urna2"]} no sábado (só a da urna original, em {", ".join(v["urna1_transmitida"])}), embora o bweb dê a carga '
                     f'da reserva em 24/10. Pode ser log de computador que não entrou no arquivo publicado.')
        if v['outras_urnas'] and k != 'PB|20516|1|297':  # João Pessoa tem pista própria
            P.append(f'Gedai: na seção {k} ({v["tipo"]}) o sábado registrou outra urna além da que votou: '
                     + ', '.join(f'{u} em {d}' for u, d in v['outras_urnas']) + f'; votou a {v["urna2"]}. Saber qual urna foi '
                     f'para a seção e o destino da outra.')
    P.append('João Pessoa, seção 297 da 1ª zona (teste com biometria, PB): a reserva carregada no sábado (01797582, UE2015) reiniciou às '
             '11h31 e às 13h16 do domingo e foi trocada às 13h35 por uma urna de contingência carregada em setembro (01659991, UE2013), '
             'que é a que aparece no boletim. Por que a reserva falhou não está publicado.')
    P.append('Números que não fecham nas fontes: PB anuncia 20 urnas de integridade e lista 19 (só 4 com número de seção); GO e PA '
             'anunciam 35 urnas e dizem 25 de integridade e 8 de autenticidade (33). Processo do TCU citado com três números: '
             'TC 019.754/2026-4 (Acórdão 2.558/2026, a proposta de fiscalização, lida), TC 020.282/2026-5 (L7) e TC 018.879/2026-8 (o '
             'acordo). A norma de 2026 aparece como Res. 23.758 e como Res. 23.769.')
    P.append('Relatórios "ocorreje" do TSE de 25/10 (12h45 e 18h00): o buscador ora os descreve como ocorrências de urnas, ora como '
             'contagem de participantes do teste com biometria (SP 254 de 3.280 às 18h). Não deu para ler (403). Se for a segunda leitura, '
             'é o único número público do volume do teste com biometria.')
    P.append('Portaria TSE 765/2024, art. 15: os boletins do teste com biometria levam a expressão "Teste de Integridade com Biometria", '
             '"poderá" ser por carimbo. Se em 2026 a expressão sai impressa pela urna, o programa sabe que está em teste; se é carimbo, '
             'não. Vale confirmar no relatório de auditoria ou numa ata com foto do boletim.')
    P.append('Urna real SP|66079|63|214 (02290625, amostra): a carga de setembro ficou gravada no log com data de 25/10/2026, 13h07, até a '
             'linha "Data e hora atualizada" mudar para 25/09/2026, 13h08. Relógio um mês adiantado na carga. Sem efeito nos votos, mas '
             'confunde qualquer conferência por data no log.')
    return P


def _n(x, d=0):
    """Número no formato brasileiro."""
    if x is None:
        return 'n/d'
    t = f'{x:,.{d}f}'
    return t.replace(',', 'X').replace('.', ',').replace('X', '.')


def _quebra(t, larg=118, rec='  '):
    import textwrap
    return '\n'.join(textwrap.fill(par, larg, subsequent_indent=rec) for par in t.split('\n'))


def texto_resultado(o):
    R = o['resumos']; vd = o['veredito_detalhe']; T = o['tabela_T']
    L = []
    a = L.append
    a('F11. Arquivos públicos do teste de integridade do 2º turno (Adendo 21)')
    a('Registro: PRE-REGISTRO-2026-10-26.md, Adendo 21 (commit 913af7a, 31/10/2026 10:36:29 UTC). Script: scripts/analisar_F11.py.')
    a('Pesquisa e downloads em 31/10/2026. As páginas jus.br (www.tse.jus.br, sites dos TREs, sintse) deram HTTP 403 ao curl e ao leitor')
    a('de páginas; não houve contorno. O que vem delas saiu do resumo do buscador e está marcado com a confiança no JSON.')
    a('')
    a('Critério registrado (antes de rodar):')
    a(_quebra('  "Achar o que o TSE e os TREs publicaram (lista de urnas, relatórios, boletins, logs, RDV, vídeos, contagem das cédulas). '
              'Se houver arquivos de urna: conferir boletim contra a contagem das cédulas, versão do programa e verificação de assinatura '
              'no log contra as urnas reais, e o modo de habilitação usado. Sinal: alguma urna de teste com boletim diferente das cédulas '
              'sem explicação documentada, ou com programa diferente das urnas reais. Sem critério para o resto."', rec='  '))
    a('')
    a(f'VEREDITO PELA LETRA: {o["veredito"]}, com alcance limitado')
    t1 = R['T_1t']; t2 = R['T_2t_reservas']
    ufs_T = collections.Counter(t['secao'].split('|')[0] for t in T)
    div = vd['boletim_contra_cedulas']['divergencias_publicadas']
    a(_quebra(f'  1) Arquivos do teste: nenhum boletim, RDV ou log de urna testada foi publicado; uma portaria de 2024 (teste com '
              f'biometria) veda fornecê-los, e não confirmei a regra de 2026. A conferência arquivo por arquivo que o registro pede não '
              f'pôde ser feita no arquivo do próprio teste.', rec='     '))
    a(_quebra(f'  2) Boletim contra cédulas, pelo que foi publicado: {len(div)} divergência (DF, CLDF), com causa dada pela autoridade do '
              f'teste ("erro humano de digitação"). Pela decisão D2 é explicação documentada incompleta e não aciona o sinal. Na leitura '
              f'estrita (ata ou relatório publicado com o voto identificado) acionaria, por falta de documento, não por indício de '
              f'adulteração. Nas demais UFs com resultado publicado (TSE, SP, SC), sem divergência.', rec='     '))
    a(_quebra(f'  3) Programa, por extensão (D3): {len(T)} urnas de teste identificadas pelo número de série '
              f'({", ".join(f"{u} {c}" for u, c in sorted(ufs_T.items()))}). Nos arquivos públicos do 1º turno dessas mesmas urnas, com a '
              f'mesma carga: versão diferente da das urnas reais em {t1["a_versao_diferente"]} (sem versão lida: {t1["sem_versao_lida"]}); componente verificado que '
              f'nenhuma urna real do mesmo modelo verificou em {t1["b_componente_novo"]}; verificação de assinatura sem SUCESSO em '
              f'{t1["c_verificacao_sem_sucesso"]}; falha no arquivo de assinatura (.vsc) em {t1["d_secoes_com_falha_no_vsc"]}; número '
              f'da urna no boletim diferente do bweb em {t1["urna_do_boletim_diferente_do_bweb"]}. Nenhuma urna de teste com programa '
              f'diferente das reais.', rec='     '))
    a('')
    # 1. inventário
    a('1. O que foi publicado (inventário completo, com fonte e confiança, no JSON)')
    for it in o['inventario']:
        a(_quebra(f'- {it["categoria"]}, {it["item"]}: {it["status"]}. {it["achado"]}', rec='  '))
    a('')
    a('2. Boletim contra cédulas no 2º turno, pelo publicado')
    for r in o['resultados_publicados']:
        x = f'- {r["uf"]}: urnas {r["urnas"] if r["urnas"] is not None else "n/d"}'
        if r.get('votos'): x += f', {_n(r["votos"])} votos'
        x += f'; divergências {r["divergencias"] if r["divergencias"] is not None else "n/d"}; {r["texto"]}.'
        if r.get('explicacao'): x += f' Classificação (D2): {r["explicacao"]}. Leitura estrita: {r["leitura_estrita"]}.'
        a(_quebra(x, rec='  '))
    a('')
    # 3. identificação
    lst = o['listas_contra_bweb']
    def cont(uf, tipos):
        rr = [r for r in lst if r['uf'] == uf and r['tipo'] in tipos]
        return len(rr), sum(1 for r in rr if r.get('chave')), sum(1 for r in rr if r.get('em_S'))
    a('3. As urnas de teste nos registros públicos (listas publicadas contra o bweb do 2º turno)')
    a(_quebra('  Grupo S (do L7): seções cuja urna do 2º turno é outra e foi carregada no sábado 24/10. Pela regra, a urna da seção escolhida '
              'vai para o teste e a seção vota numa reserva carregada no sábado; a urna testada é a do 1º turno.', rec='  '))
    for uf in ('SP', 'AL', 'PB'):
        for nome, tp in (('integridade (com e sem biometria)', ('I', 'B')), ('autenticidade', ('A',)), ('gestão de riscos', ('R',))):
            n, c, e = cont(uf, tp)
            if n: a(f'  {uf}, {nome}: {n} na lista, {c} achadas no bweb, {e} em S.')
    a(_quebra(f'  Urna testada que votou em alguma seção no 2º turno: {o["D5"]["T_urna_testada_votou_no_2t"]} de {len(T)}; em todo S, urna do '
              f'1º turno que votou no 2º: {o["D5"]["S_urna1_votou_no_2t"]} de {o["S_total"]}. As seções de autenticidade mantiveram a urna e '
              f'a carga de setembro, como a regra prevê.', rec='  '))
    ext = o['extras']
    for k, v in ext.items():
        a(_quebra(f'  Fora de T: {k}: 1º turno versão {v["1t"]["versoes_log_no_dia"]}, sem SUCESSO {len(v["1t"]["c_sem_sucesso"])}, '
                  f'.vsc {len(v["vsc1"])} falhas; 2º turno versão {v["2t"]["versoes_log_no_dia"]}, modelos no log {v["2t"]["modelo"]}.', rec='    '))
    tr = o['D5']['trocas_de_urna_no_pais'] or {}
    a(_quebra('  Trocas de urna entre os turnos no país: ' + '; '.join(f'{k}: {_n(v)}' for k, v in tr.items()) + '.', rec='  '))
    g = o['gedai_AL']
    if g:
        por_uf = collections.defaultdict(lambda: [0, 0, 0])
        for k, v in g.items():
            if v['tipo'] in ('I', 'B') or v['tipo'].startswith('candidata'):
                uf = k.split('|')[0]; por_uf[uf][0] += 1
                por_uf[uf][1] += bool([d for d in v['urna2_transmitida'] if d.startswith('24/10/2026')] or [d for (u, d) in v['outras_urnas'] if d.startswith('24/10/2026')])
                por_uf[uf][2] += bool(v['urna1_transmitida'])
        a(_quebra('  Logs do Gedai (dados abertos): seções de integridade das listas com correspondência de outra urna transmitida em 24/10 '
                  '(a reserva): ' + '; '.join(f'{uf} {x[1]} de {x[0]} (urna original transmitida em setembro em {x[2]})' for uf, x in sorted(por_uf.items())) + '.', rec='  '))
    a('')
    a('4. Programa das urnas de teste (arquivos públicos do 1º turno das mesmas urnas)')
    rf = o['referencia_urnas_reais']
    a(_quebra(f'  Referência, urnas reais da amostra: versão {rf["versao"]} em todas as {_n(sum(rf["versoes_04_10"].values()))} com log do '
              f'dia 04/10 e em todas as {_n(sum(rf["versoes_25_10"].values()))} do dia 25/10; {next(iter(rf["componentes_por_modelo_04_10"].values()))} '
              f'componentes verificados por modelo na inicialização; verificação sem SUCESSO no 04/10: {len(rf["falhas_04_10"])} urna; no 25/10: '
              f'{len(rf["falhas_25_10"])}.', rec='  '))
    a(_quebra(f'  {len(T)} urnas de teste: boletim lido em {t1["com_boletim"]}, log do dia em {t1["com_log_no_dia"]}; resultado acima. '
              f'Modelos: ' + ', '.join(f'{m} {c}' for m, c in sorted(o['modelos_T'].items())) + '. Emissor do certificado da urna (no .vsc) '
              'e chave de software iguais às das urnas reais (AC URNA para UE2013 e UE2015, AC UE2020, AC UE2022; SEVIN 20260708).', rec='  '))
    a(_quebra('  Para comparar, nas urnas do 1º turno de SP, AL e PB (faixas de modelos.py): UE2013 2,1%, UE2015 19,2%, UE2020 39,7% e '
              'UE2022 39,0%. Nenhuma UE2013 entre as 54 de teste; ao acaso, com 33 de SP, 20 de AL e 1 da PB, o esperado seria 1,5 e a '
              'chance de nenhuma, 22%. Não é desvio que mereça peso.', rec='  '))
    a('  Por urna (seção, tipo no teste, urna testada, modelo, versão no boletim, verificações no 04/10 sem SUCESSO, parte biométrica no 1º turno):')
    for t in T:
        a(f'    {t["secao"]} {t["municipio"]}, {t["tipo_no_teste"]}: urna {t["urna_testada"]} {t["modelo_urna_testada"]}, '
          f'{(t["versao_boletim_1t"] or "")[:9]}, {t["verificacoes_04_10"]} verificações, {t["sem_sucesso_04_10"]} sem SUCESSO, '
          f'biometria {_n(100 * t["parte_biometrica_1t"], 1) if t["parte_biometrica_1t"] is not None else "n/d"}%')
    a('')
    a('5. Urnas reserva que votaram nas seções do teste no 25/10 (arquivos públicos do 2º turno)')
    a(_quebra(f'  {t2["secoes"]} seções: versão diferente {t2["a_versao_diferente"]} (sem versão lida {t2["sem_versao_lida"]}); componente novo {t2["b_componente_novo"]}; '
              f'verificação sem SUCESSO {t2["c_verificacao_sem_sucesso"]}; falha no .vsc {t2["d_secoes_com_falha_no_vsc"]}; urna do boletim '
              f'diferente do bweb {t2["urna_do_boletim_diferente_do_bweb"]}. O aux.json do 2º turno lista um só pacote em '
              f'{sum(1 for t in T if t["pacotes_no_aux_2t"] == 1)} das {len(T)} seções, e o boletim desse pacote é o da reserva em '
              f'{sum(1 for t in T if t["urna_boletim_igual_bweb_2t"])}: o boletim do teste não está no site de resultados.', rec='  '))
    cr = [t['carga_reserva_log'][0] for t in T if t['carga_reserva_log'][0]]
    a(_quebra(f'  Carga das reservas no sábado 24/10, pelo log: primeira linha entre {min(cr) if cr else "n/d"} e {max(cr) if cr else "n/d"}; '
              f'verificações da carga sem SUCESSO: {sum(len(o["carga_reservas"][t["secao"]]["sem_sucesso_24_10"]) for t in T)}.', rec='  '))
    a('')
    s1 = R['S_1t']; s2 = R['S_2t_reservas']
    a(f'6. Superconjunto S ({o["S_total"]} seções, todas as UFs; contém as urnas de teste das UFs sem lista)')
    a(_quebra(f'  Urnas do 1º turno (as que saíram da seção no sábado): {s1["secoes"]} seções, boletim {s1["com_boletim"]}, log do dia {s1["com_log_no_dia"]}; '
              f'versão diferente {s1["a_versao_diferente"]} (sem versão lida {s1["sem_versao_lida"]}); componente novo {s1["b_componente_novo"]}; sem SUCESSO {s1["c_verificacao_sem_sucesso"]}; '
              f'falha no .vsc {s1["d_secoes_com_falha_no_vsc"]}; urna do boletim diferente do bweb {s1["urna_do_boletim_diferente_do_bweb"]}.', rec='  '))
    a(_quebra(f'  Reservas (2º turno), só as baixadas (as de T, controles e extras em S; D6 não pede as demais): {s2["secoes"]} seções, boletim {s2["com_boletim"]}, log do dia {s2["com_log_no_dia"]}; versão diferente '
              f'{s2["a_versao_diferente"]} (sem versão lida {s2["sem_versao_lida"]}); componente novo {s2["b_componente_novo"]}; sem SUCESSO {s2["c_verificacao_sem_sucesso"]}; '
              f'falha no .vsc {s2["d_secoes_com_falha_no_vsc"]}; urna do boletim diferente do bweb {s2["urna_do_boletim_diferente_do_bweb"]}.', rec='  '))
    for nome in ('S_1t_problemas', 'S_2t_problemas'):
        pr = o['S_detalhe_problemas'][nome]
        if pr:
            a(_quebra(f'  {nome}: ' + '; '.join(f'{k}: ' + json.dumps(v, ensure_ascii=False, default=str)[:300] for k, v in list(pr.items())[:12]), rec='    '))
    a(_quebra('  Modelos das urnas do 1º turno em S: ' + ', '.join(f'{m} {c}' for m, c in sorted(o['modelos_S_urna1'].items(), key=lambda x: str(x[0]))) + '.', rec='  '))
    a('')
    a('7. Modo de habilitação')
    hb = lambda r: _n(100 * r['biometricas'] / r['habilitacoes'], 1) if r.get('habilitacoes') else 'n/d'
    a(_quebra(f'  No teste, só pelas listas: ambiente controlado (habilitação pelo caderno de votação, sem digital) e com biometria '
              f'(voluntários). SP 30 e 3; AL 18 e 2; PB pelo menos 1 com biometria; DF 2 com biometria; RJ 2; SC 2; PR 2; MT 1. '
              f'Na votação real, as mesmas urnas de teste no 1º turno tiveram {hb(t1)}% das habilitações por biometria '
              f'({_n(t1["habilitacoes"])} habilitações); as reservas no 2º turno, {hb(t2)}%; as urnas do 1º turno de S, {hb(s1)}%. '
              f'Nada nos arquivos públicos mostra o modo usado no teste em si.', rec='  '))
    a('')
    a('8. O que isso significa')
    for x in SIGNIFICADO:
        a(_quebra('- ' + x, rec='  '))
    a('')
    a('9. Pistas (para investigar, inclusive fora do critério)')
    for x in o.get('pistas', []):
        a(_quebra('- ' + x, rec='  '))
    a('')
    a('10. Desvios e decisões')
    for x in DESVIOS:
        a(_quebra('- ' + x, rec='  '))
    a('')
    a('Arquivos: resultados/F11_teste_integridade_arquivos.json (tudo, inclusive a tabela por urna, as listas casadas com o bweb e o inventário com')
    a('links); downloads em /home/user/trabalho-eleicao/adendo21/F11_dl_* (fora do repositório).')
    return '\n'.join(L) + '\n'


if __name__ == '__main__':
    if sys.argv[1] == 'selecionar':
        selecionar(*sys.argv[2:5])
    elif sys.argv[1] == 'analisar':
        analisar(*sys.argv[2:12])
