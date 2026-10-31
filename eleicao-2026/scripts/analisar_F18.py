"""F18 do pré-registro (Adendo 22): certificados de urna emitidos depois do vencimento da AC URNA.

Registro (PRE-REGISTRO-2026-10-26.md, Adendo 22, commit f12121e, 31/10/2026 14:52:48 UTC, antes de rodar):
  - Amostra estratificada por UF de 1.500 seções do 2º turno com urna antiga (UE2013 ou UE2015, pelas faixas do F4),
    semente 20261031. Baixar o .vsc e conferir a assinatura de cada certificado de urna com a AC URNA publicada e a
    data de emissão.
  - Descritivo, sem critério de sinal: fração e estimativa nacional (com intervalo de 95%) de certificados emitidos
    depois de 18/07/2026, e se algum certificado não confere com a AC publicada (isso seria sinal).

O que já se sabia antes de escrever este arquivo (transparência): o F12 (Adendo 21) achou, na amostra antiga do 2º
turno (amostra2t, 3.897 seções), 1.059 certificados da AC URNA, todos com assinatura conferindo, o mais recente emitido
em 2026-07-17, e nenhum emitido depois do fim da AC (2026-07-18 21:59:57 UTC); fora da amostra, a urna de Marília
(SP|66818|400|141) tem certificado emitido em 2026-08-03 pela chave da AC URNA. Nenhum arquivo da amostra do F18 foi
baixado nem olhado antes de fixar as decisões abaixo.

Decisões que o registro não fixa (tomadas antes de sortear, baixar e calcular; cada uma é declarada como desvio):
  D1. Quadro: todas as seções com registro do 2º turno em trab2t/secoes2026.json.gz (bweb do 2º turno; 499.205 seções,
      todas "Apurada"), Brasil e exterior. Urna = campo 'urna' do turno '2' (NR_URNA_EFETIVADA do bweb do 2º turno).
  D2. Modelo pelas faixas do F4 (resultados/F4_modelo_urna.json, faixas.limites_usados), com o classificador do F4 e
      do F10: número abaixo do menor ou acima do maior da amostra de logs fica sem modelo e sai; número na zona de corte
      recebe o modelo do corte (contado à parte). Urna antiga = UE2013 ou UE2015.
  D3. Estrato = UF do bweb, com o exterior (ZZ) como estrato próprio, porque é assim que o TSE codifica a UF no bweb
      e no endereço dos arquivos de urna. Leitura sem o exterior relatada ao lado.
  D4. Alocação proporcional: cota n_h = 1.500 x N_h / N; cada estrato recebe a parte inteira e as vagas que sobram vão
      para os maiores restos (método de Hamilton; empate pela ordem alfabética da UF). Estrato com n_h = 0 não é
      sorteado (o registro diz proporcional; não há mínimo por estrato) e entra na estimativa nacional com a fração
      estimada nos outros estratos (ver D11).
  D5. Sorteio: dentro do estrato, seções ordenadas por (município, zona, seção) como inteiros; um gerador
      numpy.random.default_rng(20261031) para todos os estratos, em ordem alfabética de UF; em cada estrato com
      n_h > 0, rng.choice(N_h, n_h, replace=False) (estratos com n_h = 0 não chamam o gerador). Amostra sem reposição e
      sem substituição: seção sem arquivo fica como não resposta (D12).
  D6. Download: scripts/baixar_arquivos_urna.py, pleito 3221 (2º turno), tipo 'vota' (só aux.json e o -vota.vsc que o
      aux lista), TAXA=1.0, 4 conexões, para a pasta nova e vazia adendo22/F18_arq; a lista fica em adendo22/F18_scripts.
      Uma passada e, se houver falha de rede, uma segunda (o script retoma e não pede de novo o que já tem).
  D7. vsc usado: o -vota.vsc do último índice de hash listado no aux.json e presente no disco, como no F12 e no T18. Se
      o aux listar mais de um vsc, os outros entram só como descritivo (mesmo certificado ou não).
  D8. Certificado: o do bloco 1 do vsc (assinatura de hardware), em PEM ou DER (bytes depois do DER são ignorados e
      contados), lido com o código do F12 (analisar_F12.trabalho_cert). Data de emissão = notBefore (UTC), a única data
      de emissão que o certificado traz; serial = serialNumber. Registrados também notAfter, emissor, AKI, titular e o
      número da urna no titular.
  D9. "Confere com a AC publicada", como no D2 do F12: (a) a assinatura do certificado confere com a chave da AC
      publicada que ele aponta (AKI igual ao SKI da AC), (b) aponta para uma AC publicada, (c) o emissor (DN) é o titular
      dessa AC. ECDSA P-521 com SHA-512 sobre o TBSCertificate (AC URNA); Ed521 puro (AC UE2020 e AC UE2022, se alguma
      seção da amostra tiver urna nova no vsc). AC publicada = constante _AC_RAIZ_UE_PEMS do pacote de documentação do
      TSE formato-arquivos-bu-rdv-ass-digital-v2.zip, a mesma cópia baixada no F12 (adendo21/F12_dl_doccaz, lida como
      texto, nada executado); o SHA-256 do zip e de cada AC é conferido com o JSON do F12. Controles negativos do F12:
      TBS com um bit trocado e assinatura com um byte trocado não podem ser aceitos. Sinal = algum certificado da
      amostra que falhe (a), (b) ou (c).
  D10. "Emitido depois de 18/07/2026" (principal) = notBefore com data UTC (a data escrita no certificado) de
      19/07/2026 ou depois. Leituras ao lado: notBefore depois do instante do fim da AC URNA publicada
      (2026-07-18 21:59:57 UTC); data de Brasília (UTC-3) de 19/07/2026 ou depois. Denominador: seções da amostra com
      certificado lido no vsc, qualquer que seja a AC; a fração só entre os certificados da AC URNA sai ao lado.
  D11. Estimativa: estimador estratificado p = soma de W_h p_h nos estratos com resposta, W_h = N_h / (soma dos N_h
      desses estratos); estimativa nacional = N x p, com N = todas as seções do quadro (os estratos sem amostra recebem
      a fração dos outros). Variância: soma de W_h^2 (1 - n_h/N_h) s_h^2 / n_h, s_h^2 = n_h/(n_h - 1) p_h (1 - p_h).
      Intervalo de 95% principal: Korn e Graubard (Clopper-Pearson com tamanho efetivo n_ef = p(1-p)/v, limitado ao
      número de respondentes; n_ef = respondentes se p = 0, p = 1 ou v = 0; ajuste de graus de liberdade
      (t_{n-1}/t_{gl})^2 com gl = respondentes - estratos com resposta), x_ef = p x n_ef. Intervalo de Wald ao lado. O
      intervalo da contagem é N vezes o da fração. Unidade: seção (cada seção tem uma urna; urnas distintas relatadas).
  D12. Não resposta (sem aux.json, sem vsc, vsc ilegível): contada por estrato; a estimativa supõe ausência ao acaso
      dentro do estrato; limites extremos (todas as ausentes depois de 18/07 ou nenhuma) relatados ao lado.
  D13. Conferências descritivas (fora do critério): SHA-256 do vsc contra o hash do aux.json; resumo e assinatura do
      bloco de hardware com a chave do próprio certificado (liga o certificado aos arquivos da seção); número da urna
      no certificado contra o do bweb; modelo do bloco 2 do vsc contra a faixa e contra a AC; serial ou chave repetidos
      em urnas diferentes; meses de emissão e fim de validade; ordem dos seriais contra a data; seções que também estão
      na amostra antiga do 2º turno (amostra2t, a do F12): mesmo certificado ou não.
  D14. Veredito pela letra: SINAL se algum certificado não confere com a AC publicada (D9); senão SEM SINAL. A fração
      e a estimativa são descritivas, sem critério.

Acrescentado DEPOIS de ver resultado parcial (exploração, fora do registro e do veredito): nos primeiros 42 certificados
baixados, o serial da AC URNA cresceu com a data de emissão sem nenhuma inversão. Por isso, como pista: E1. seriais e
datas de todos os certificados da AC URNA da amostra antiga do 2º turno (amostra2t, a do F12) e da urna de Marília
(adendo21/F12_dl_marilia_1t e _2t, já baixados no F12), lidos sem verificação, para ver se o serial é um contador da AC e,
se for, quantos seriais a AC URNA gastou entre duas datas (em particular entre o último emitido antes de 18/07/2026 e o
de Marília, de 03/08/2026).

Uso:
  python3 -I -B analisar_F18.py amostra [--base ...] [--f4 ...] [--lista ...] [--amostra_json ...]
  python3 -I -B analisar_F18.py analisar [--base ...] [--f4 ...] [--arq ...] [--zip_ac ...] [--f12 ...] [--amostra2t ...]
                                         [--saida_json ...] [--saida_txt ...] [--proc 4]
"""
import os as _os, sys as _sys
_sys.path.insert(0, _os.path.dirname(_os.path.abspath(__file__)))
import argparse, base64, collections, datetime as dt, glob, hashlib, json, math, os, sys, zipfile
from multiprocessing import Pool
import numpy as np
from scipy import stats
from cryptography import x509
from cryptography.hazmat.primitives.serialization import Encoding
from lib import carregar

SEMENTE = 20261031
N_AMOSTRA = 1500
ANTIGAS = ('UE2013', 'UE2015')
UTC = dt.timezone.utc
CORTE_DATA = dt.date(2026, 7, 19)          # D10: data UTC de 19/07/2026 ou depois
AQUI = os.path.dirname(os.path.abspath(__file__))
RES = os.path.join(AQUI, '..', 'resultados')
T = '/home/user/trabalho-eleicao'
MODELO_B2 = {13: 'UE2013', 15: 'UE2015', 20: 'UE2020', 22: 'UE2022'}
AC_DO_MODELO = {'UE2013': 'AC URNA', 'UE2015': 'AC URNA', 'UE2020': 'AC UE2020', 'UE2022': 'AC UE2022'}


def limpa(s):
    """Sem travessões no que vai para a saída."""
    return s.replace('\u2014', '-').replace('\u2013', '-') if isinstance(s, str) else s


# ------------------------------------------------------------------------------------------------ quadro e amostra
def faixas_F4(f4json):
    """Classificador do F4 e do F10 (D2)."""
    with open(f4json) as f:
        F = json.load(f)['faixas']
    lim = F['limites_usados']; fx = F['faixas']
    minimo, maximo = lim[0][0], lim[-1][1]
    zonas = [(fx[j]['ultimo_da_amostra'], fx[j + 1]['primeiro_da_amostra']) for j in range(len(fx) - 1)]

    def mod(u):
        if u is None or u < minimo or u > maximo:
            return None
        for f_ in fx:
            if f_['corte_superior'] is None or u < f_['corte_superior']:
                return f_['modelo']
        return None

    def na_zona(u):
        return u is not None and any(a < u < b for a, b in zonas)
    return mod, na_zona, {'limites_usados': lim, 'zonas_de_corte': zonas}


def ordem_secao(k):
    uf, m, z, s = k.split('|')
    return (int(m), int(z), int(s))


def montar_amostra(base, f4json):
    d = carregar(base)
    mod, na_zona, info = faixas_F4(f4json)
    quadro = collections.defaultdict(list); urna_de = {}
    cont = collections.Counter(); modelos = collections.Counter()
    for k, v in d.items():
        b = v.get('2')
        if not b:
            cont['sem_2t'] += 1; continue
        cont['secoes_2t'] += 1; cont['tipo_' + str(b.get('tipo'))] += 1
        m = mod(b.get('urna')); modelos[str(m)] += 1
        if m in ANTIGAS:
            quadro[k.split('|')[0]].append(k); urna_de[k] = b['urna']
            cont['antigas_na_zona_de_corte'] += na_zona(b['urna'])
    for uf in quadro:
        quadro[uf].sort(key=ordem_secao)
    N = sum(len(v) for v in quadro.values())
    ufs = sorted(quadro)
    cota = {uf: N_AMOSTRA * len(quadro[uf]) / N for uf in ufs}
    n_h = {uf: int(math.floor(cota[uf])) for uf in ufs}
    sobra = N_AMOSTRA - sum(n_h.values())
    for uf in sorted(ufs, key=lambda u: (-(cota[u] - n_h[u]), u))[:sobra]:
        n_h[uf] += 1
    rng = np.random.default_rng(SEMENTE)
    amostra = {}
    for uf in ufs:
        if n_h[uf] == 0:
            amostra[uf] = []; continue
        idx = rng.choice(len(quadro[uf]), size=n_h[uf], replace=False)
        amostra[uf] = [quadro[uf][i] for i in sorted(int(x) for x in idx)]
    urnas_quadro = collections.Counter(urna_de.values())
    desc = {'secoes_2t_na_base': cont['secoes_2t'], 'tipos_2t': {k[5:]: v for k, v in cont.items() if k.startswith('tipo_')},
            'modelos_2t_pelas_faixas_F4': dict(modelos), 'quadro_secoes_antigas': N,
            'quadro_urnas_distintas': len(urnas_quadro),
            'quadro_urnas_em_mais_de_uma_secao': {str(u): c for u, c in urnas_quadro.items() if c > 1},
            'quadro_na_zona_de_corte': cont['antigas_na_zona_de_corte'],
            'quadro_por_modelo': dict(collections.Counter(mod(u) for u in urna_de.values())),
            'faixas_F4': info,
            'estratos': {uf: {'N_h': len(quadro[uf]), 'cota': cota[uf], 'n_h': n_h[uf]} for uf in ufs},
            'estratos_sem_amostra': [uf for uf in ufs if n_h[uf] == 0], 'semente': SEMENTE, 'n': sum(n_h.values())}
    return amostra, quadro, urna_de, desc, d, mod, na_zona


def cmd_amostra(a):
    amostra, quadro, urna_de, desc, *_ = montar_amostra(a.base, a.f4)
    linhas = [k for uf in sorted(amostra) for k in amostra[uf]]
    os.makedirs(os.path.dirname(os.path.abspath(a.lista)), exist_ok=True)
    open(a.lista, 'w').write('\n'.join(linhas) + '\n')
    sha = hashlib.sha256(open(a.lista, 'rb').read()).hexdigest()
    desc['lista'] = os.path.abspath(a.lista); desc['sha256_lista'] = sha
    json.dump(desc, open(a.amostra_json, 'w'), ensure_ascii=False, indent=1)
    print(f"quadro {desc['quadro_secoes_antigas']} secoes antigas em {len(desc['estratos'])} estratos; amostra {len(linhas)}; "
          f"sem amostra: {desc['estratos_sem_amostra']}; sha256 da lista {sha}")


# ------------------------------------------------------------------------------------------------ AC publicada
def acs_publicadas(zip_ac, f12json):
    import analisar_F12 as F12
    zb = open(zip_ac, 'rb').read()
    zf = zipfile.ZipFile(zip_ac)
    txt = zf.read('python/lib/mr_util.py').decode('utf-8')
    blocos, comentario = F12.pems_do_texto_mr_util(txt)
    acs_der = {}
    for _, der in blocos:
        c = x509.load_der_x509_certificate(der)
        acs_der[F12.cn(c.subject)] = der
    fichas = {n: F12.ficha_ac(x509.load_der_x509_certificate(d)) for n, d in acs_der.items()}
    f12 = json.load(open(f12json))
    conf = {'sha256_zip': hashlib.sha256(zb).hexdigest(),
            'sha256_zip_no_F12': f12['fontes_das_ac']['pacote_TSE_v2']['sha256_zip'],
            'por_ac': {n: {'sha256_der': fichas[n]['sha256_der'], 'sha256_der_no_F12': f12['acs_publicadas'].get(n, {}).get('sha256_der'),
                           'igual': fichas[n]['sha256_der'] == f12['acs_publicadas'].get(n, {}).get('sha256_der')} for n in fichas},
            'comentario_do_TSE': comentario, 'origem': os.path.abspath(zip_ac)}
    conf['zip_igual_ao_F12'] = conf['sha256_zip'] == conf['sha256_zip_no_F12']
    conf['todas_iguais_ao_F12'] = conf['zip_igual_ao_F12'] and all(x['igual'] for x in conf['por_ac'].values())
    return acs_der, fichas, conf


# ------------------------------------------------------------------------------------------------ trabalho por seção
def _init(acs_der):
    import analisar_F12 as F12
    F12._init(acs_der)


def pasta_da(arq, k):
    uf, m, z, s = k.split('|')
    return os.path.join(arq, uf.lower(), f'{int(m):05d}', f'{int(z):04d}', f'{int(s):04d}')


def vscs_listados(p):
    """[(índice, nome no disco, hash do aux)] dos -vota.vsc listados no aux.json, na ordem do aux."""
    try:
        aux = json.load(open(os.path.join(p, 'aux.json')))
    except Exception:  # noqa: BLE001
        return None, None
    out = []
    for i, h in enumerate(aux.get('hashes', [])):
        for x in h.get('arq', []):
            if x.get('tp') == 'vota':
                out.append((i, f'{i}-' + x['nm'], h.get('hash', '')))
    return out, aux


def trabalho(item):
    import analisar_F12 as F12
    from verificar_assinaturas import ler_vsc, verifica_ass, chave_bruta
    from cryptography.exceptions import UnsupportedAlgorithm
    k, p, origem = item
    r = {'secao': k, 'origem': origem, 'estado': None}
    if not os.path.isdir(p):
        r['estado'] = 'pasta ausente'; return r
    if os.path.exists(os.path.join(p, 'SEM_AUX')):
        r['estado'] = 'sem aux.json (404)'; return r
    listados, aux = vscs_listados(p)
    if listados is None:
        r['estado'] = 'aux.json ausente ou ilegível'; return r
    r['aux_st'] = aux.get('st'); r['n_hashes_aux'] = len(aux.get('hashes', []))
    r['vsc_listados'] = len(listados)
    r['tipos_no_aux'] = sorted({str(x.get('tp')) for h in aux.get('hashes', []) for x in h.get('arq', [])})
    presentes = [x for x in listados if os.path.exists(os.path.join(p, x[1]))]
    r['vsc_presentes'] = len(presentes)
    if not presentes:
        r['estado'] = 'vsc listado não baixado' if listados else 'aux sem vsc'; return r
    i_hash, nome, hash_aux = presentes[-1]
    cam = os.path.join(p, nome)
    bruto = open(cam, 'rb').read()
    try:
        esperado = bytes.fromhex(hash_aux).decode()
        r['vsc_sha256_igual_aux'] = base64.b64encode(hashlib.sha256(bruto).digest()).decode().replace('/', '-') == esperado
    except ValueError:
        r['vsc_sha256_igual_aux'] = None
    try:
        c = F12.trabalho_cert((k, cam, '2t'))
    except Exception as e:  # noqa: BLE001
        r['estado'] = 'vsc ou certificado ilegível'; r['erro'] = repr(e)[:200]; return r
    c.pop('resumos_vsc', None)
    r.update(c); r['estado'] = 'ok'; r['vsc'] = nome
    # bloco de hardware assinado pela chave do próprio certificado (D13)
    try:
        v = ler_vsc(cam)
        cert, _, _ = F12.carregar_cert(v['hw_cert'])
        try:
            pub, ched = cert.public_key(), None
        except UnsupportedAlgorithm:
            pub, ched = None, chave_bruta(cert)
        h = hashlib.sha512(v['hw_conteudo']).digest()
        r['bloco_hw_resumo_ok'] = h == v['hw_cab']['sha512'] and len(v['hw_conteudo']) == v['hw_cab']['tam']
        r['bloco_hw_assinatura_ok'] = bool(verifica_ass(pub, ched, v['hw_cab']['ass'], h))
        ident = k.split('|')
        ident = f'{ident[0].lower()}{int(ident[1]):05d}{int(ident[2]):04d}{int(ident[3]):04d}'
        r['vsc_de_outra_secao'] = [nm for nm in v['hw_entradas'] if ident not in nm][:3]
        r['arquivos_no_vsc'] = len(v['hw_entradas'])
    except Exception as e:  # noqa: BLE001
        r['bloco_hw_assinatura_ok'] = None; r['erro_bloco'] = repr(e)[:200]
    # outros vsc listados (D7)
    outros = []
    for i2, n2, _ in presentes[:-1]:
        try:
            c2 = F12.trabalho_cert((k, os.path.join(p, n2), '2t'))
            outros.append({'vsc': n2, 'sha256_cert': c2['sha256_cert'], 'mesmo_certificado': c2['sha256_cert'] == r['sha256_cert'],
                           'assinatura_ok': c2['assinatura_ok'], 'inicio': c2['inicio']})
        except Exception as e:  # noqa: BLE001
            outros.append({'vsc': n2, 'erro': repr(e)[:120]})
    r['outros_vsc'] = outros
    return r


def serial_e_data(item):
    """E1: serial, notBefore e AC (pelo AKI) do certificado do vsc, sem verificar nada."""
    import analisar_F12 as F12
    from verificar_assinaturas import ler_vsc
    k, cam, origem = item
    try:
        cert, _, _ = F12.carregar_cert(ler_vsc(cam)['hw_cert'])
        aki = F12.ext(cert, x509.AuthorityKeyIdentifier)
        return {'secao': k, 'origem': origem, 'serial': cert.serial_number, 'inicio': cert.not_valid_before_utc.isoformat(),
                'fim': cert.not_valid_after_utc.isoformat(), 'aki': aki.key_identifier.hex() if aki and aki.key_identifier else None,
                'titular': F12.cn(cert.subject)}
    except Exception as e:  # noqa: BLE001
        return {'secao': k, 'origem': origem, 'erro': repr(e)[:120]}


def explorar_seriais(ok, pool, a, ski_acurna, fim_acurna, nomes_aki):
    """E1 (fora do registro): seriais da AC URNA contra a data, juntando F18, amostra2t e Marília."""
    import analisar_F12 as F12
    itens = []
    for uf in sorted(os.listdir(a.amostra2t)):
        for pasta in sorted(glob.glob(os.path.join(a.amostra2t, uf, '*', '*', '*'))):
            u, m, z, s_ = pasta.rstrip('/').split('/')[-4:]
            f = F12.vsc_da_secao(pasta)
            if f:
                itens.append((f'{u.upper()}|{int(m)}|{int(z)}|{int(s_)}', f, 'amostra2t'))
    for t, pasta in (('marilia_1t', a.marilia1t), ('marilia_2t', a.marilia2t)):
        for f in sorted(glob.glob(os.path.join(pasta, '*', '*', '*', '*', '*-vota.vsc'))):
            itens.append(('SP|66818|400|141', f, t))
    outros = pool.map(serial_e_data, itens, chunksize=32)
    todos = [{'secao': r['secao'], 'origem': 'F18', 'serial': r['serial'], 'inicio': r['inicio'], 'aki': r['aki']} for r in ok]
    todos += [r for r in outros if 'erro' not in r]
    faixa = collections.defaultdict(list)
    for r in todos:
        faixa[nomes_aki.get(r['aki'], str(r['aki']))].append((r['serial'], r['inicio']))
    faixa_por_ac = {n: {'certificados': len(v), 'serial_min': min(v)[0], 'serial_max': max(v)[0],
                        'emissao_do_serial_max': max(v)[1]} for n, v in faixa.items()}
    acu = {}
    for r in todos:
        if r['aki'] != ski_acurna:
            continue
        acu.setdefault((r['serial'], r['inicio']), r)
    lst = sorted(acu.values(), key=lambda r: (r['inicio'], r['serial']))
    inv = [(lst[i - 1]['secao'], lst[i - 1]['serial'], lst[i - 1]['inicio'], lst[i]['secao'], lst[i]['serial'], lst[i]['inicio'])
           for i in range(1, len(lst)) if lst[i]['serial'] < lst[i - 1]['serial']]
    ts = [dt.datetime.fromisoformat(r['inicio']).timestamp() for r in lst]
    rho = float(stats.spearmanr(ts, [r['serial'] for r in lst]).correlation) if len(lst) > 2 else None
    ser_iguais = collections.Counter(r['serial'] for r in lst)
    antes = [r for r in lst if dt.datetime.fromisoformat(r['inicio']) <= fim_acurna]
    depois = [r for r in lst if dt.datetime.fromisoformat(r['inicio']) > fim_acurna]
    ult_antes = antes[-1] if antes else None
    recentes = lst[-12:]
    gaps = []
    for i in range(max(1, len(lst) - 12), len(lst)):
        gaps.append({'de': [lst[i - 1]['secao'], lst[i - 1]['serial'], lst[i - 1]['inicio']], 'para': [lst[i]['secao'], lst[i]['serial'], lst[i]['inicio']],
                     'seriais_entre': lst[i]['serial'] - lst[i - 1]['serial'],
                     'dias_entre': (dt.datetime.fromisoformat(lst[i]['inicio']) - dt.datetime.fromisoformat(lst[i - 1]['inicio'])).total_seconds() / 86400})
    return {'faixa_de_serial_por_ac': faixa_por_ac, 'certificados_ac_urna_distintos': len(lst), 'por_origem': dict(collections.Counter(r['origem'] for r in acu.values())),
            'lidos_fora_do_F18': len(outros), 'erros_de_leitura': sum(1 for r in outros if 'erro' in r),
            'spearman_data_serial': rho, 'inversoes': len(inv), 'inversoes_lista': inv[:10],
            'serial_com_duas_datas': [s_ for s_, c in ser_iguais.items() if c > 1],
            'ultimo_antes_do_fim_da_ac': ult_antes, 'depois_do_fim_da_ac': depois,
            'seriais_gastos_do_ultimo_antes_ao_primeiro_depois': (depois[0]['serial'] - ult_antes['serial']) if (depois and ult_antes) else None,
            'mais_recentes': recentes, 'saltos_entre_os_mais_recentes': gaps}


# ------------------------------------------------------------------------------------------------ estimativa
def estimar(por_estrato, N_quadro, Nh):
    """por_estrato: {uf: (n_respondentes, x_eventos)}. D11."""
    cobertos = {h: v for h, v in por_estrato.items() if v[0] > 0}
    Ncob = sum(Nh[h] for h in cobertos)
    p = 0.0; var = 0.0; n = 0; x = 0
    for h, (nh, xh) in cobertos.items():
        W = Nh[h] / Ncob; ph = xh / nh
        p += W * ph; n += nh; x += xh
        if nh > 1:
            s2 = nh / (nh - 1) * ph * (1 - ph)
            var += W * W * (1 - nh / Nh[h]) * s2 / nh
    H = len(cobertos)
    if 0 < p < 1 and var > 0:
        n_ef = min(n, p * (1 - p) / var)
    else:
        n_ef = n
    gl = max(n - H, 1)
    aj = (stats.t.ppf(0.975, n - 1) / stats.t.ppf(0.975, gl)) ** 2 if n > 1 else 1.0
    n_ef *= aj
    x_ef = p * n_ef
    lo = 0.0 if x_ef <= 0 else float(stats.beta.ppf(0.025, x_ef, n_ef - x_ef + 1))
    hi = 1.0 if x_ef >= n_ef else float(stats.beta.ppf(0.975, x_ef + 1, n_ef - x_ef))
    ep = math.sqrt(var)
    return {'respondentes': n, 'eventos': x, 'estratos_com_resposta': H, 'secoes_do_quadro_nesses_estratos': Ncob,
            'fracao': p, 'ep': ep, 'n_efetivo': n_ef, 'ajuste_gl': aj,
            'ic95_korn_graubard': [lo, hi], 'ic95_wald': [max(0.0, p - 1.96 * ep), min(1.0, p + 1.96 * ep)],
            'estimativa_nacional_secoes': p * N_quadro, 'ic95_nacional_secoes': [lo * N_quadro, hi * N_quadro],
            'N_quadro': N_quadro}


# ------------------------------------------------------------------------------------------------ principal
def cmd_analisar(a):
    import analisar_F12 as F12
    amostra, quadro, urna_de, desc, d, mod, na_zona = montar_amostra(a.base, a.f4)
    lista_disco = [l.strip() for l in open(a.lista) if l.strip()] if os.path.exists(a.lista) else None
    linhas = [k for uf in sorted(amostra) for k in amostra[uf]]
    R = {'teste': 'F18', 'registro': 'Adendo 22 do PRE-REGISTRO-2026-10-26.md (commit f12121e, 31/10/2026 14:52:48 UTC)',
         'quadro_e_amostra': desc, 'lista_baixada_igual_a_amostra': lista_disco == linhas}
    acs_der, fichas, conf = acs_publicadas(a.zip_ac, a.f12)
    R['acs_publicadas'] = fichas; R['conferencia_das_ac_com_o_F12'] = conf
    fim_acurna = dt.datetime.fromisoformat(fichas['AC URNA']['validade_fim_utc'])
    itens = [(k, pasta_da(a.arq, k), 'F18') for k in linhas]
    # seções da amostra que também estão na amostra antiga do 2º turno (F12)
    sobrep = [(k, pasta_da(a.amostra2t, k), 'amostra2t') for k in linhas if os.path.isdir(pasta_da(a.amostra2t, k))]
    with Pool(a.proc, initializer=_init, initargs=(acs_der,)) as pool:
        res = pool.map(trabalho, itens, chunksize=8)
        res_s = pool.map(trabalho, sobrep, chunksize=4) if sobrep else []
        ok_ = [r for r in res if r['estado'] == 'ok']
        R['exploracao_E1_seriais'] = explorar_seriais(ok_, pool, a, fichas['AC URNA']['ski'], fim_acurna,
                                                         {f['ski']: n for n, f in fichas.items()})
    por_k = {r['secao']: r for r in res}
    # E1, continuação: densidade de seriais por certificado do quadro (só com a amostra F18, que é probabilística)
    X = R['exploracao_E1_seriais']
    ok_ac = [r for r in res if r['estado'] == 'ok' and r['ac_pelo_aki'] == 'AC URNA']
    n_ok = len([r for r in res if r['estado'] == 'ok'])
    N_q = desc['quadro_secoes_antigas']
    antes_2017 = max((s_ for i_, s_ in [(r['inicio'], r['serial']) for r in ok_ac] if i_ < '2017-01-01'), default=None)
    ult = X['ultimo_antes_do_fim_da_ac']
    jan = [r for r in ok_ac if '2017-01-01' <= r['inicio'] and dt.datetime.fromisoformat(r['inicio']) <= fim_acurna]
    dens = {'janela': 'emitidos de 01/01/2017 até o fim da AC URNA', 'certificados_F18_na_janela': len(jan),
            'serial_inicial (maior serial de 2016 na amostra F18)': antes_2017, 'serial_final (último antes do fim da AC)': ult['serial'] if ult else None}
    if jan and antes_2017 and ult:
        est_q = len(jan) / n_ok * N_q
        span = ult['serial'] - antes_2017
        razao = span / est_q
        g = X['seriais_gastos_do_ultimo_antes_ao_primeiro_depois']
        dens.update({'seriais_na_janela': span, 'certificados_do_quadro_estimados_na_janela': est_q, 'seriais_por_certificado_do_quadro': razao,
                     'seriais_depois_do_fim_ate_marilia': g,
                     'certificados_do_quadro_projetados_nesses_seriais': (g / razao) if g else None,
                     'esperado_na_amostra_F18': (g / razao * n_ok / N_q) if g else None})
    X['densidade'] = dens
    X['marilia_no_quadro'] = 'SP|66818|400|141' in urna_de
    X['marilia_urna_no_bweb'] = urna_de.get('SP|66818|400|141')

    # ---- classificação de cada certificado
    estado = collections.Counter(r['estado'] for r in res)
    ok = [r for r in res if r['estado'] == 'ok']
    falhas = []
    for r in ok:
        r['urna_bweb'] = urna_de[r['secao']]
        r['modelo_faixa_bweb'] = mod(r['urna_bweb'])
        r['na_zona_de_corte'] = na_zona(r['urna_bweb'])
        ini = dt.datetime.fromisoformat(r['inicio'])
        r['depois_data_utc'] = ini.date() >= CORTE_DATA
        r['depois_do_instante_fim_ac_urna'] = ini > fim_acurna
        r['depois_data_brasilia'] = (ini - dt.timedelta(hours=3)).date() >= CORTE_DATA
        b2 = r.get('bloco2') or []
        r['modelo_bloco2'] = MODELO_B2.get(b2[0]) if b2 else None
        motivos = []
        if r['ac_pelo_aki'] is None:
            motivos.append('AKI não corresponde a nenhuma AC publicada')
        else:
            if not r['emissor_dn_igual_texto']:
                motivos.append('emissor diferente do titular da AC')
            if not r['assinatura_ok']:
                motivos.append('assinatura não confere com a AC')
        r['falha_pelo_criterio'] = motivos
        if motivos:
            falhas.append({'secao': r['secao'], 'motivos': motivos, 'urna': r['urna'], 'ac': r['ac_pelo_aki'], 'aki': r['aki'], 'emissor': r['emissor']})
    R['sem_certificado'] = [{'secao': r['secao'], 'estado': r['estado'], 'tipos_no_aux': r.get('tipos_no_aux'), 'urna_bweb': urna_de[r['secao']]}
                            for r in res if r['estado'] != 'ok']
    controles = {'tbs_adulterado_aceito': sum(bool(r['controle_adulterado_ok']) for r in ok),
                 'assinatura_trocada_aceita': sum(bool(r['controle_assinatura_trocada_ok']) for r in ok),
                 'verifica_tambem_com_outra_ac': sum(bool(r['outras_acs_ok']) for r in ok),
                 'controles_rodados': 2 * sum(1 for r in ok if r['ac_pelo_aki'])}
    por_ac = collections.Counter(str(r['ac_pelo_aki']) for r in ok)
    R['certificados'] = {
        'estado_por_secao': dict(estado), 'lidos': len(ok), 'por_ac': dict(por_ac),
        'assinatura_ok': sum(bool(r['assinatura_ok']) for r in ok),
        'emissor_dn_igual_byte_a_byte': sum(bool(r['emissor_dn_igual_bytes']) for r in ok),
        'formato': dict(collections.Counter(r['formato'] for r in ok)),
        'der_com_bytes_extras': sum(1 for r in ok if r['bytes_extras']),
        'algoritmo': dict(collections.Counter(r['alg'] for r in ok)),
        'falhas_pelo_criterio': falhas, 'controles_negativos': controles}

    # ---- emissão depois de 18/07/2026
    Nh = {uf: v['N_h'] for uf, v in desc['estratos'].items()}
    N = desc['quadro_secoes_antigas']

    def por_estrato(chave, filtro=lambda r: True, ufs=None):
        o = {}
        for uf in Nh:
            if ufs is not None and uf not in ufs:
                continue
            rs = [r for r in ok if r['secao'].split('|')[0] == uf and filtro(r)]
            o[uf] = (len(rs), sum(bool(r[chave]) for r in rs))
        return o
    est = {}
    est['principal_data_utc'] = estimar(por_estrato('depois_data_utc'), N, Nh)
    est['instante_do_fim_da_ac_urna'] = estimar(por_estrato('depois_do_instante_fim_ac_urna'), N, Nh)
    est['data_de_brasilia'] = estimar(por_estrato('depois_data_brasilia'), N, Nh)
    Nh_br = {u: v for u, v in Nh.items() if u != 'ZZ'}
    est['sem_exterior'] = estimar(por_estrato('depois_data_utc', ufs=set(Nh_br)), sum(Nh_br.values()), Nh_br)
    # descritivo: emitidos em 2026 (qualquer data do ano), com o mesmo estimador
    for r in ok:
        r['emitido_em_2026'] = r['inicio'][:4] == '2026'
    est['descritivo_emitidos_em_2026'] = estimar(por_estrato('emitido_em_2026'), N, Nh)
    # só certificados da AC URNA (descritivo; N do quadro inteiro como referência)
    est['so_ac_urna'] = estimar(por_estrato('depois_data_utc', lambda r: r['ac_pelo_aki'] == 'AC URNA'), N, Nh)
    # limites extremos de não resposta (D12), em contagem bruta e com o mesmo estimador
    nao_resp = {uf: v['n_h'] - por_estrato('depois_data_utc')[uf][0] for uf, v in desc['estratos'].items()}
    pe = por_estrato('depois_data_utc')
    pior = {uf: (desc['estratos'][uf]['n_h'], pe[uf][1] + nao_resp[uf]) for uf in Nh}
    melhor = {uf: (desc['estratos'][uf]['n_h'], pe[uf][1]) for uf in Nh}
    est['nao_resposta'] = {'por_estrato': {u: n for u, n in nao_resp.items() if n}, 'total': sum(nao_resp.values()),
                           'todas_ausentes_depois': estimar(pior, N, Nh)['fracao'], 'nenhuma_ausente_depois': estimar(melhor, N, Nh)['fracao']}
    R['emitidos_depois_de_18_07_2026'] = est
    depois = sorted([r for r in ok if r['depois_data_utc'] or r['depois_do_instante_fim_ac_urna'] or r['depois_data_brasilia']],
                    key=lambda r: r['inicio'])
    R['lista_emitidos_depois'] = [{k_: r.get(k_) for k_ in ('secao', 'urna', 'urna_bweb', 'ac_pelo_aki', 'serial', 'inicio', 'fim',
                                                             'assinatura_ok', 'depois_data_utc', 'depois_do_instante_fim_ac_urna',
                                                             'depois_data_brasilia', 'modelo_bloco2', 'hw_quando', 'bloco_hw_assinatura_ok')}
                                  for r in depois]

    # ---- descritivos de datas e seriais
    meses = collections.Counter(r['inicio'][:7] for r in ok)
    anos = collections.Counter(f"{r['ac_pelo_aki']} {r['inicio'][:4]}" for r in ok)
    fins = collections.Counter(r['fim'][:10] for r in ok)
    em2026 = sorted([r for r in ok if r['inicio'][:4] == '2026'], key=lambda r: r['inicio'])
    ac_urna = sorted([r for r in ok if r['ac_pelo_aki'] == 'AC URNA'], key=lambda r: r['inicio'])
    seriais = [r['serial'] for r in ac_urna]
    # ordem: serial cresce com a data?
    inv = sum(1 for i in range(1, len(ac_urna)) if ac_urna[i]['serial'] < ac_urna[i - 1]['serial'])
    rho = float(stats.spearmanr([dt.datetime.fromisoformat(r['inicio']).timestamp() for r in ac_urna], seriais).correlation) if len(ac_urna) > 2 else None
    ser_rep = collections.defaultdict(set); ch_rep = collections.defaultdict(set)
    for r in ok:
        ser_rep[(r['ac_pelo_aki'], r['serial'])].add(r['urna']); ch_rep[r['sha256_chave_urna']].add(r['urna'])
    R['descritivo'] = {
        'emissao_por_ano_e_ac': dict(sorted(anos.items())), 'emissao_por_mes': dict(sorted(meses.items())),
        'fim_de_validade_mais_comum': fins.most_common(8),
        'emissao_mais_recente': max((r['inicio'] for r in ok), default=None),
        'emissao_mais_recente_ac_urna': ac_urna[-1]['inicio'] if ac_urna else None,
        'emitidos_em_2026': [{k_: r.get(k_) for k_ in ('secao', 'urna', 'ac_pelo_aki', 'serial', 'inicio', 'fim', 'assinatura_ok', 'modelo_bloco2')} for r in em2026],
        'fim_31_12_2037_23h': sum(1 for r in ok if r['fim'].startswith('2037-12-31T23:00')),
        'seriais_ac_urna': {'min': min(seriais) if seriais else None, 'max': max(seriais) if seriais else None,
                            'bits_max': max(s.bit_length() for s in seriais) if seriais else None,
                            'inversoes_na_ordem_da_data': inv, 'spearman_data_serial': rho},
        'serial_repetido_em_urnas_diferentes': [[str(k_[0]), str(k_[1]), sorted(v)] for k_, v in ser_rep.items() if len(v) > 1],
        'chave_repetida_em_urnas_diferentes': sum(1 for v in ch_rep.values() if len(v) > 1),
        'urna_no_certificado_diferente_do_bweb': [(r['secao'], r['urna'], r['urna_bweb']) for r in ok if r['urna'] != r['urna_bweb']],
        'modelo_bloco2': dict(collections.Counter(str(r['modelo_bloco2']) for r in ok)),
        'modelo_bloco2_diferente_da_faixa': [(r['secao'], r['urna'], r['modelo_bloco2'], r['modelo_faixa_bweb']) for r in ok if r['modelo_bloco2'] != r['modelo_faixa_bweb']],
        'ac_diferente_da_do_modelo': [(r['secao'], r['modelo_bloco2'], r['ac_pelo_aki']) for r in ok if AC_DO_MODELO.get(r['modelo_bloco2']) != r['ac_pelo_aki']],
        'na_zona_de_corte': sum(1 for r in ok if r['na_zona_de_corte']),
        'vsc_sha256_igual_aux': dict(collections.Counter(str(r.get('vsc_sha256_igual_aux')) for r in ok)),
        'bloco_hw_resumo_ok': dict(collections.Counter(str(r.get('bloco_hw_resumo_ok')) for r in ok)),
        'bloco_hw_assinatura_ok': dict(collections.Counter(str(r.get('bloco_hw_assinatura_ok')) for r in ok)),
        'vsc_com_arquivo_de_outra_secao': [(r['secao'], r['vsc_de_outra_secao']) for r in ok if r.get('vsc_de_outra_secao')],
        'secoes_com_mais_de_um_vsc': [(r['secao'], r['outros_vsc']) for r in ok if r.get('outros_vsc')],
        'aux_status': dict(collections.Counter(str(r.get('aux_st')) for r in res)),
        'hw_quando_min_max': [min((r['hw_quando'] for r in ok), default=None), max((r['hw_quando'] for r in ok), default=None)],
        'usuario_e_conjunto_sw': dict(collections.Counter(f"{r['sw_usuario']} / {r['sw_conjunto']}" for r in ok)),
    }
    # por UF: certificados lidos, da AC URNA, emitidos em 2026 e depois de 18/07
    R['por_uf'] = {uf: {'N_h': Nh[uf], 'n_h': desc['estratos'][uf]['n_h'],
                        'lidos': sum(1 for r in ok if r['secao'].split('|')[0] == uf),
                        'em_2026': sum(1 for r in ok if r['secao'].split('|')[0] == uf and r['inicio'][:4] == '2026'),
                        'depois_de_18_07': sum(1 for r in ok if r['secao'].split('|')[0] == uf and r['depois_data_utc'])} for uf in sorted(Nh)}
    # sobreposição com a amostra2t
    comp = []
    for r2 in res_s:
        r1 = por_k.get(r2['secao'])
        if r2.get('estado') != 'ok' or not r1 or r1.get('estado') != 'ok':
            comp.append({'secao': r2['secao'], 'comparavel': False}); continue
        comp.append({'secao': r2['secao'], 'comparavel': True, 'mesmo_certificado': r1['sha256_cert'] == r2['sha256_cert'],
                     'serial_F18': r1['serial'], 'serial_amostra2t': r2['serial'], 'inicio': r1['inicio']})
    R['sobreposicao_amostra2t'] = {'secoes': len(sobrep), 'comparaveis': sum(1 for c in comp if c['comparavel']),
                                   'mesmo_certificado': sum(1 for c in comp if c.get('mesmo_certificado')), 'lista': comp}
    R['registros'] = [{k_: v for k_, v in r.items() if k_ not in ('outros_vsc',)} for r in res]

    # ---- veredito
    R['veredito'] = {'pela_letra': 'SINAL' if falhas else 'SEM SINAL',
                     'motivo': (f'{len(falhas)} certificado(s) não confere(m) com a AC publicada' if falhas else
                                f"nenhum dos {len(ok)} certificados lidos deixa de conferir com a AC publicada"),
                     'fracao_e_estimativa': 'descritivas, sem critério de sinal'}
    json.dump(R, open(a.saida_json, 'w'), ensure_ascii=False, indent=1, default=str)
    escrever_txt(R, a.saida_txt)
    print(open(a.saida_txt).read())


# ------------------------------------------------------------------------------------------------ texto
def fi(x):
    return f'{int(round(x)):,}'.replace(',', '.')


def fz(x, c=2):
    return f'{x:.{c}f}'.replace('.', ',')


def fp(x, c=2):
    return fz(100 * x, c) + '%'


def escrever_txt(R, caminho):
    L = []; w = L.append
    Q = R['quadro_e_amostra']; C = R['certificados']; E = R['emitidos_depois_de_18_07_2026']; D = R['descritivo']
    P = E['principal_data_utc']; V = R['veredito']
    w('F18. Certificados de urna emitidos depois do vencimento da AC URNA (Adendo 22)')
    w('')
    w('VEREDITO PELA LETRA DO ADENDO 22')
    w(f"  {V['pela_letra']}. {V['motivo'][0].upper() + V['motivo'][1:]}.")
    w(f"  Emitidos depois de 18/07/2026 (descritivo): {fi(P['eventos'])} de {fi(P['respondentes'])} na amostra; fração estimada "
      f"{fp(P['fracao'], 3)} (IC 95% {fp(P['ic95_korn_graubard'][0], 3)} a {fp(P['ic95_korn_graubard'][1], 3)}); "
      f"estimativa nacional {fi(P['estimativa_nacional_secoes'])} seções (IC 95% {fi(P['ic95_nacional_secoes'][0])} a {fi(P['ic95_nacional_secoes'][1])}) "
      f"de {fi(Q['quadro_secoes_antigas'])} com urna antiga.")
    w('')
    w('NÚMEROS')
    w(f"  Quadro: {fi(Q['quadro_secoes_antigas'])} seções do 2º turno com urna UE2013 ou UE2015 pelas faixas do F4 "
      f"({', '.join(f'{k} {fi(v)}' for k, v in sorted(Q['quadro_por_modelo'].items()))}), {fi(Q['quadro_urnas_distintas'])} urnas distintas, "
      f"{len(Q['estratos'])} estratos (UF, com ZZ = exterior). Estratos sem amostra pela alocação proporcional: {', '.join(Q['estratos_sem_amostra']) or 'nenhum'}.")
    w(f"  Amostra: {fi(Q['n'])} seções, semente {Q['semente']}; lista baixada igual à sorteada: {'sim' if R['lista_baixada_igual_a_amostra'] else 'NÃO'}.")
    w(f"  Situação das seções: " + '; '.join(f'{k} {fi(v)}' for k, v in sorted(C['estado_por_secao'].items(), key=lambda x: -x[1])) + '.')
    for x in R['sem_certificado']:
        w(f"    sem certificado: {x['secao']} ({x['estado']}; tipos no aux: {', '.join(x.get('tipos_no_aux') or [])}; urna no bweb {x.get('urna_bweb')})")
    cf = R['conferencia_das_ac_com_o_F12']
    w(f"  AC publicada: a mesma cópia do pacote do TSE usada no F12 (zip e certificados com o mesmo SHA-256 do F12: {'sim' if cf['todas_iguais_ao_F12'] else 'NÃO'}). "
      f"AC URNA: serial {R['acs_publicadas']['AC URNA']['serial']}, de {R['acs_publicadas']['AC URNA']['validade_inicio_utc'][:19]} a {R['acs_publicadas']['AC URNA']['validade_fim_utc'][:19]} UTC.")
    w(f"  Certificados lidos: {fi(C['lidos'])} (" + ', '.join(f'{k} {fi(v)}' for k, v in sorted(C['por_ac'].items())) + f"); "
      f"assinatura confere com a AC apontada: {fi(C['assinatura_ok'])} de {fi(C['lidos'])}; emissor igual ao titular da AC byte a byte: {fi(C['emissor_dn_igual_byte_a_byte'])}.")
    cn_ = C['controles_negativos']
    w(f"  Controles: TBS com 1 bit trocado ou assinatura com 1 byte trocado aceitos {cn_['tbs_adulterado_aceito'] + cn_['assinatura_trocada_aceita']} vezes em {fi(cn_['controles_rodados'])}; "
      f"certificado que confere também com outra AC: {cn_['verifica_tambem_com_outra_ac']}.")
    w(f"  Falhas pelo critério: {len(C['falhas_pelo_criterio'])}" + (f" {C['falhas_pelo_criterio'][:5]}" if C['falhas_pelo_criterio'] else '') + '.')
    for nome, rot in (('principal_data_utc', 'Principal (data UTC do notBefore de 19/07/2026 em diante)'),
                      ('instante_do_fim_da_ac_urna', 'Depois do instante do fim da AC URNA (2026-07-18 21:59:57 UTC)'),
                      ('data_de_brasilia', 'Data de Brasília (UTC-3) de 19/07/2026 em diante'),
                      ('sem_exterior', 'Sem o exterior (data UTC)'),
                      ('so_ac_urna', 'Só certificados da AC URNA (data UTC)'),
                      ('descritivo_emitidos_em_2026', 'Descritivo: emitidos em qualquer data de 2026')):
        e = E[nome]
        w(f"  {rot}: {fi(e['eventos'])} de {fi(e['respondentes'])}; fração {fp(e['fracao'], 3)}, IC 95% {fp(e['ic95_korn_graubard'][0], 3)} a {fp(e['ic95_korn_graubard'][1], 3)} "
          f"(Wald {fp(e['ic95_wald'][0], 3)} a {fp(e['ic95_wald'][1], 3)}); nacional {fi(e['estimativa_nacional_secoes'])} de {fi(e['N_quadro'])} "
          f"(IC {fi(e['ic95_nacional_secoes'][0])} a {fi(e['ic95_nacional_secoes'][1])}).")
    nr = E['nao_resposta']
    w(f"  Não resposta: {nr['total']} {'seção' if nr['total'] == 1 else 'seções'}" + (f" ({nr['por_estrato']})" if nr['total'] else '') +
      f"; limites extremos da fração: {fp(nr['nenhuma_ausente_depois'], 3)} a {fp(nr['todas_ausentes_depois'], 3)}.")
    w(f"  Emissão mais recente: {D['emissao_mais_recente']}; da AC URNA: {D['emissao_mais_recente_ac_urna']}.")
    w(f"  Emissão por ano e AC: " + ', '.join(f'{k} {v}' for k, v in D['emissao_por_ano_e_ac'].items()) + '.')
    w(f"  Emitidos em 2026: {len(D['emitidos_em_2026'])}; com fim em 31/12/2037 23:00 UTC: {D['fim_31_12_2037_23h']} {'certificado' if D['fim_31_12_2037_23h'] == 1 else 'certificados'} no total.")
    for x in D['emitidos_em_2026']:
        w(f"    {x['secao']}: urna {x['urna']}, {x['ac_pelo_aki']}, serial {x['serial']}, emitido {x['inicio'][:19]} UTC, fim {x['fim'][:19]}, assinatura {'confere' if x['assinatura_ok'] else 'NÃO confere'}, bloco 2 {x['modelo_bloco2']}.")
    if R['lista_emitidos_depois']:
        w('  Emitidos depois de 18/07/2026 (qualquer das três leituras):')
        for x in R['lista_emitidos_depois']:
            w(f"    {x['secao']}: urna {x['urna']} (bweb {x['urna_bweb']}), {x['ac_pelo_aki']}, serial {x['serial']}, emitido {x['inicio'][:19]} UTC, "
              f"assinatura {'confere' if x['assinatura_ok'] else 'NÃO confere'}, bloco de hardware assinado pela urna: {x['bloco_hw_assinatura_ok']}, assinatura de hardware em {x['hw_quando']} (local).")
    w('')
    w('CONFERÊNCIAS DESCRITIVAS')
    w(f"  SHA-256 do vsc igual ao do aux.json: {D['vsc_sha256_igual_aux']}; resumo do bloco de hardware: {D['bloco_hw_resumo_ok']}; "
      f"assinatura do bloco de hardware pela chave do certificado: {D['bloco_hw_assinatura_ok']}.")
    w(f"  Urna do certificado diferente da do bweb: {len(D['urna_no_certificado_diferente_do_bweb'])} {D['urna_no_certificado_diferente_do_bweb'][:5]}.")
    w(f"  Modelo do bloco 2: {D['modelo_bloco2']}; diferente da faixa: {len(D['modelo_bloco2_diferente_da_faixa'])} {D['modelo_bloco2_diferente_da_faixa'][:5]}; "
      f"AC diferente da do modelo: {len(D['ac_diferente_da_do_modelo'])} {D['ac_diferente_da_do_modelo'][:5]}; seções na zona de corte: {D['na_zona_de_corte']}.")
    s = D['seriais_ac_urna']
    w(f"  Seriais da AC URNA: de {s['min']} a {s['max']} ({s['bits_max']} bits no máximo); Spearman data x serial {fz(s['spearman_data_serial'], 3) if s['spearman_data_serial'] is not None else 'n/d'}; "
      f"inversões na ordem da data {s['inversoes_na_ordem_da_data']}.")
    w(f"  Serial repetido em urnas diferentes: {len(D['serial_repetido_em_urnas_diferentes'])}; chave repetida: {D['chave_repetida_em_urnas_diferentes']}; "
      f"vsc com arquivo de outra seção: {len(D['vsc_com_arquivo_de_outra_secao'])}; seções com mais de um vsc: {len(D['secoes_com_mais_de_um_vsc'])}.")
    w(f"  Fim de validade mais comum: {D['fim_de_validade_mais_comum'][:5]}.")
    w(f"  Assinatura de hardware (horário local): de {D['hw_quando_min_max'][0]} a {D['hw_quando_min_max'][1]}; assinatura de software: {D['usuario_e_conjunto_sw']}.")
    S = R['sobreposicao_amostra2t']
    w(f"  Seções também na amostra antiga do 2º turno (F12): {S['secoes']}; comparáveis {S['comparaveis']}; mesmo certificado {S['mesmo_certificado']}.")
    X = R.get('exploracao_E1_seriais')
    if X:
        w('')
        w('EXPLORAÇÃO E1 (fora do registro, escolhida depois de ver resultado parcial; não vale como teste)')
        w(f"  Certificados distintos da AC URNA (F18 + amostra2t + Marília): {fi(X['certificados_ac_urna_distintos'])} {X['por_origem']}; "
          f"Spearman data x serial {fz(X['spearman_data_serial'], 4) if X['spearman_data_serial'] is not None else 'n/d'}; inversões {X['inversoes']}"
          + (f" {X['inversoes_lista'][:3]}" if X['inversoes'] else '') + f"; serial com duas datas: {len(X['serial_com_duas_datas'])}.")
        w('  Faixa de serial por AC (todas as origens): ' + '; '.join(f"{n} {fi(v['certificados'])} certificados, de {v['serial_min']} a {v['serial_max']}" for n, v in sorted(X['faixa_de_serial_por_ac'].items())) + '.')
        u = X['ultimo_antes_do_fim_da_ac']
        if u:
            w(f"  Último emitido antes do fim da AC: {u['secao']} ({u['origem']}), serial {u['serial']}, {u['inicio'][:19]} UTC.")
        for x in X['depois_do_fim_da_ac']:
            w(f"  Depois do fim da AC: {x['secao']} ({x['origem']}), serial {x['serial']}, {x['inicio'][:19]} UTC.")
        if X['seriais_gastos_do_ultimo_antes_ao_primeiro_depois'] is not None:
            w(f"  Seriais entre o último antes e o primeiro depois: {fi(X['seriais_gastos_do_ultimo_antes_ao_primeiro_depois'])}.")
        dn = X.get('densidade', {})
        if dn.get('seriais_por_certificado_do_quadro'):
            w(f"  Densidade (só a amostra F18): {dn['certificados_F18_na_janela']} certificados emitidos de 2017 até o fim da AC, "
              f"cerca de {fi(dn['certificados_do_quadro_estimados_na_janela'])} no quadro, para {fi(dn['seriais_na_janela'])} seriais: "
              f"{fz(dn['seriais_por_certificado_do_quadro'], 1)} seriais por certificado do quadro. Nessa razão, os {fi(dn['seriais_depois_do_fim_ate_marilia'])} seriais "
              f"de 17/07 a 03/08/2026 dariam cerca de {fz(dn['certificados_do_quadro_projetados_nesses_seriais'], 1)} certificados do quadro "
              f"e {fz(dn['esperado_na_amostra_F18'], 2)} esperados na amostra F18.")
        w(f"  A seção de Marília está no quadro do F18: {'sim' if X.get('marilia_no_quadro') else 'não'} (urna no bweb {X.get('marilia_urna_no_bweb')}); "
          f"o total nacional verdadeiro é então de pelo menos 1.")
        w('  Saltos entre os mais recentes (seriais, dias):')
        for g in X['saltos_entre_os_mais_recentes']:
            w(f"    {g['de'][0]} {g['de'][1]} {g['de'][2][:10]} -> {g['para'][0]} {g['para'][1]} {g['para'][2][:10]}: {fi(g['seriais_entre'])} seriais em {fz(g['dias_entre'], 1)} dias")
        w('')
    w('  Por UF (N do quadro, n sorteado, lidos, emitidos em 2026, depois de 18/07):')
    w('    ' + '; '.join(f"{uf} {fi(v['N_h'])}/{v['n_h']}/{v['lidos']}/{v['em_2026']}/{v['depois_de_18_07']}" for uf, v in R['por_uf'].items()))
    w('')
    w('DESVIOS (decisões não fixadas pelo registro, tomadas antes de sortear, baixar e calcular; texto completo no docstring)')
    for t in DESVIOS:
        w('  ' + t)
    open(caminho, 'w').write(limpa('\n'.join(L)) + '\n')


DESVIOS = [
    'D1. Quadro = seções do bweb do 2º turno (base trab2t/secoes2026.json.gz), Brasil e exterior; urna = NR_URNA_EFETIVADA do 2º turno.',
    'D2. Modelo pelas faixas do F4 com o classificador do F4/F10; fora da faixa sai; zona de corte recebe o modelo do corte.',
    'D3. Estrato = UF do bweb, exterior (ZZ) como estrato próprio; leitura sem o exterior ao lado.',
    'D4. Alocação proporcional por maiores restos (Hamilton), sem mínimo por estrato; estrato com zero sorteadas recebe a fração dos outros.',
    'D5. Ordem (município, zona, seção); numpy default_rng(20261031), estratos em ordem alfabética, choice sem reposição; sem substituição.',
    'D6. Download com baixar_arquivos_urna.py, pleito 3221, tipo vota (aux.json e -vota.vsc), TAXA=1.0, pasta nova adendo22/F18_arq.',
    'D7. vsc do último índice de hash do aux presente no disco (como F12 e T18); outros vsc só descritivos.',
    'D8. Certificado do bloco 1 do vsc lido com o código do F12; data de emissão = notBefore (UTC); serial = serialNumber.',
    'D9. Confere = AKI aponta AC publicada, emissor = titular da AC e assinatura confere (ECDSA P-521/SHA-512 ou Ed521), AC do pacote do TSE na cópia do F12.',
    'D10. Depois de 18/07/2026 = data UTC do notBefore de 19/07 em diante; ao lado, depois do instante do fim da AC e pela data de Brasília.',
    'D11. Estimador estratificado; IC 95% de Korn e Graubard (Clopper-Pearson com tamanho efetivo e ajuste de graus de liberdade); Wald ao lado; unidade = seção.',
    'D12. Não resposta suposta ao acaso dentro do estrato; limites extremos relatados.',
    'D13. Conferências descritivas: hash do aux, bloco de hardware assinado pela urna, urna do certificado x bweb, bloco 2, repetições, seriais, sobreposição com a amostra2t.',
    'D14. Veredito: SINAL se algum certificado não confere com a AC publicada; senão SEM SINAL; fração e estimativa sem critério.',
]


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('modo', choices=['amostra', 'analisar'])
    ap.add_argument('--base', default=f'{T}/trab2t/secoes2026.json.gz')
    ap.add_argument('--f4', default=os.path.join(RES, 'F4_modelo_urna.json'))
    ap.add_argument('--lista', default=f'{T}/adendo22/F18_scripts/lista_F18.txt')
    ap.add_argument('--amostra_json', default=f'{T}/adendo22/F18_scripts/amostra_F18.json')
    ap.add_argument('--arq', default=f'{T}/adendo22/F18_arq')
    ap.add_argument('--amostra2t', default=f'{T}/amostra2t/arq')
    ap.add_argument('--zip_ac', default=f'{T}/adendo21/F12_dl_doccaz/docv2/formato-arquivos-bu-rdv-ass-digital-v2.zip')
    ap.add_argument('--f12', default=os.path.join(RES, 'F12_certificados_resumos.json'))
    ap.add_argument('--saida_json', default=os.path.join(RES, 'F18_certificados_pos_vencimento.json'))
    ap.add_argument('--saida_txt', default=os.path.join(RES, 'F18_certificados_pos_vencimento.txt'))
    ap.add_argument('--marilia1t', default=f'{T}/adendo21/F12_dl_marilia_1t')
    ap.add_argument('--marilia2t', default=f'{T}/adendo21/F12_dl_marilia_2t')
    ap.add_argument('--proc', type=int, default=4)
    a = ap.parse_args()
    (cmd_amostra if a.modo == 'amostra' else cmd_analisar)(a)


if __name__ == '__main__':
    main()
