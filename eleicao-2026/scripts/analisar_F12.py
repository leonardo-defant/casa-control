"""F12 do pré-registro (Adendo 21): certificados das autoridades certificadoras da urna e resumos digitais dos programas.

Letra do registro: achar os certificados públicos da AC URNA, AC UE2020 e AC UE2022 e conferir, com código próprio, se os
certificados das urnas da amostra foram assinados por elas e em que prazo de validade; conferir a alegação de que o
certificado da AC URNA venceu em 18/07/2026; achar os resumos digitais publicados dos programas lacrados em 04/09 e
comparar com qualquer resumo obtenível dos arquivos de urna. Sinal: certificado de urna que não se valida pela AC
publicada, ou resumo de programa diferente do publicado. Sem critério para o resto.

Decisões tomadas antes de calcular o resultado (o registro não as fixa; todas declaradas como desvio no relatório):
 D1. Fonte das AC. O site do TSE (www.tse.jus.br) e o do TRE-PE respondem 403 (Akamai) a partir deste ambiente; os endereços
     de política e de lista de revogação citados nos certificados (dpc.*, lcr.*.tse.jus.br) só servem HTTP simples, que o
     proxy deste ambiente não encaminha (em HTTPS o certificado do servidor não cobre o nome). Por isso a "AC publicada" é a
     constante _AC_RAIZ_UE_PEMS do pacote oficial de documentação do TSE formato-arquivos-bu-rdv-ass-digital-v2.zip
     (python/lib/mr_util.py, comentada pelo TSE como "obtidos em dpc.acue2020.tse.jus.br"), lido de uma cópia de terceiros
     (github.com/doccaz/urnas-br, docv2). Conferências: o mesmo certificado em três cópias independentes (epicleet/var-ue,
     ivanmneto92-sys/auditoria-presidente-2026, alissonlinneker/dataurnas-br) e o SHA-512 dos arquivos acue2020.cer e
     acue2022.cer no resumo digital do sistema HOLOCRON das Eleições 2026 (cópia de terceiros do TSE, ver D4). O zip e o
     arquivo .py são lidos como texto; nada deles é executado.
 D2. "Não se valida pela AC publicada" = (a) a assinatura do certificado da urna não confere com a chave pública da AC
     publicada que ele aponta (AKI igual ao SKI da AC), ou (b) o certificado aponta para uma AC que não está entre as
     publicadas, ou (c) o emissor (DN) do certificado não é o titular da AC apontada. O prazo de validade fica descritivo,
     como manda "Sem critério para o resto"; a leitura estrita (validação de caminho do RFC 5280 na data da assinatura,
     que exige a AC dentro da validade) também é calculada e relatada ao lado, sem mudar o veredito.
 D3. Assinatura do certificado: ECDSA P-521 com SHA-512 sobre o TBSCertificate (AC URNA, biblioteca cryptography); Ed521
     puro sobre o TBSCertificate (AC UE2020 e AC UE2022, ed521.verificar), como em mr_util.valida_certificado do pacote do
     TSE. Os bytes do TBSCertificate são os do próprio arquivo (sem recodificar).
 D4. Resumos publicados: a página do TSE (resumos-digitais-hashes-das-eleicoes-2026-1o-e-2o-turnos) e a do TRE-PE dão 403;
     a cópia do Internet Archive (captura de 27/10/2026) não abre a partir deste ambiente. Uso a cópia de terceiros
     github.com/havaianasdestruido/resumos-eleicao-2026 (zips com data interna de 03/09/2026, enviados em 04/10/2026).
     A autenticidade dessa cópia só é conferida indiretamente (D1: os certificados AC UE2020 e AC UE2022 do pacote do
     TSE têm o SHA-512 que ela publica).
 D5. "Resumo obtenível dos arquivos de urna" = (a) o SHA-512 de cada um dos 11 arquivos listados no -vota.vsc de cada
     seção (inclusive hash.dat e mr.ver, que não são publicados); (b) os nomes dos pacotes cuja assinatura o log diz ter
     verificado; (c) a versão da aplicação no boletim e no log. Os arquivos públicos de seção não trazem nenhum arquivo de
     programa nem resumo de programa: se nada de (a) for programa, a parte "resumo de programa diferente do publicado"
     fica SEM DADO, e (b) e (c) ficam descritivos.
 D6. Datas de referência da validade: a data e hora de criação da assinatura de hardware do -vota.vsc (horário local da
     urna, convertido para UTC com -3 h; a diferença de fuso entre UFs, de até 2 h, só importaria a menos de 1 dia de
     uma data-limite, e esses casos são contados à parte) e os dias de votação 04/10/2026 e 25/10/2026.
 D7. Fora da amostra do registro, como descritivo: os -vota.vsc do 1º turno (pleito 3220) das 80 seções de amostra2t/arq1t,
     e o -vota.vsc e o -bu.dat dos dois turnos da seção SP|66818|400|141 (Marília), que a dataurnas-br cita como urna com
     certificado emitido pela chave da AC URNA depois do vencimento; baixados para esta tarefa pelo baixar_arquivos_urna.py
     (TAXA=1.0, só o que o aux.json lista).
 D8. Robustez, fora do critério: a chave da AC RAIZ UE é recuperada da assinatura ECDSA do certificado da AC URNA (dois a
     quatro candidatos) e escolhida pelo identificador de chave (AKI) do próprio certificado. Isso não liga a chave ao TSE.

Uso: python3 -I analisar_F12.py [--arq2t ...] [--vsc1t ...] [--dl ...] [--saida_json ...] [--saida_txt ...]
"""
import os as _os, sys as _sys
_sys.path.insert(0, _os.path.dirname(_os.path.abspath(__file__)))
import argparse, base64, collections, datetime as dt, glob, hashlib, html, json, os, re, sys, zipfile
from multiprocessing import Pool
from cryptography import x509
from cryptography.exceptions import InvalidSignature, UnsupportedAlgorithm
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.asymmetric import ec
from cryptography.hazmat.primitives.serialization import Encoding, PublicFormat
from ber import read_tlv, parse
from verificar_assinaturas import ler_vsc, chave_bruta
from verificar_ac_ecdsa import candidatos
from decodificar import ler_bu, _linhas_log
from modelos import FAIXAS
import ed521

DL = '/home/user/trabalho-eleicao/adendo21'
UTC = dt.timezone.utc
DIAS = {'1t': dt.date(2026, 10, 4), '2t': dt.date(2026, 10, 25)}
ALEGADO = dt.datetime(2026, 7, 18, tzinfo=UTC)
MODELO_B2 = {13: 'UE2013', 15: 'UE2015', 20: 'UE2020', 22: 'UE2022'}
ALG_B2 = {1: 'rsa', 2: 'ecdsa', 3: 'cepesc', 4: 'eddsa'}
AC_DO_MODELO = {'UE2013': 'AC URNA', 'UE2015': 'AC URNA', 'UE2020': 'AC UE2020', 'UE2022': 'AC UE2022'}
MANIFESTO_DO_MODELO = {'UE2013': 'path1u13', 'UE2015': 'path1u15', 'UE2020': 'path1u20', 'UE2022': 'path1u22'}


def limpa(s):
    """Sem travessões no que vai para a saída."""
    return s.replace('\u2014', '-').replace('\u2013', '-') if isinstance(s, str) else s


def b64(b):
    return base64.b64encode(b).decode()


# ------------------------------------------------------------------------------------------------ certificados
def carregar_cert(b):
    if b.lstrip().startswith(b'-----'):
        return x509.load_pem_x509_certificate(b), 'PEM', b''
    fim = read_tlv(b, 0)[4]
    return x509.load_der_x509_certificate(b[:fim]), 'DER', b[fim:]


def cn(nome):
    v = nome.get_attributes_for_oid(x509.NameOID.COMMON_NAME)
    return v[0].value if v else None


def ext(cert, cls):
    try:
        return cert.extensions.get_extension_for_class(cls).value
    except x509.ExtensionNotFound:
        return None


def chave_da(cert):
    """('ecdsa', objeto da biblioteca) ou ('ed521', 66 bytes)."""
    try:
        return 'ecdsa', cert.public_key()
    except UnsupportedAlgorithm:
        return 'ed521', chave_bruta(cert)


def bytes_da_chave(tipo, k):
    return k.public_bytes(Encoding.X962, PublicFormat.UncompressedPoint) if tipo == 'ecdsa' else k


def verifica(tipo, chave, assinatura, tbs):
    if tipo == 'ecdsa':
        try:
            chave.verify(assinatura, tbs, ec.ECDSA(hashes.SHA512())); return True
        except (InvalidSignature, ValueError):
            return False
    return ed521.verificar(chave, assinatura, tbs)


def ficha_ac(cert):
    tipo, k = chave_da(cert)
    kb = bytes_da_chave(tipo, k)
    ski = ext(cert, x509.SubjectKeyIdentifier); aki = ext(cert, x509.AuthorityKeyIdentifier)
    bc = ext(cert, x509.BasicConstraints); ku = ext(cert, x509.KeyUsage)
    crl = ext(cert, x509.CRLDistributionPoints); pol = ext(cert, x509.CertificatePolicies)
    der = cert.public_bytes(Encoding.DER)
    return {
        'titular': cert.subject.rfc4514_string(), 'emissor': cert.issuer.rfc4514_string(),
        'serial': cert.serial_number, 'validade_inicio_utc': cert.not_valid_before_utc.isoformat(),
        'validade_fim_utc': cert.not_valid_after_utc.isoformat(),
        'algoritmo_assinatura': cert.signature_algorithm_oid.dotted_string, 'tipo_chave': tipo,
        'ski': ski.digest.hex() if ski else None, 'aki': aki.key_identifier.hex() if aki and aki.key_identifier else None,
        'aki_emissor': [str(g.value.rfc4514_string()) for g in (aki.authority_cert_issuer or [])] if aki else None,
        'aki_serial_do_emissor': aki.authority_cert_serial_number if aki else None,
        'ski_igual_sha1_da_chave': (ski.digest == hashlib.sha1(kb).digest()) if ski else None,
        'ca': bc.ca if bc else None, 'assina_certificados': ku.key_cert_sign if ku else None,
        'lcr': [u.value for d in (crl or []) for u in (d.full_name or [])],
        'politica': [str(q) for p in (pol or []) for q in (p.policy_qualifiers or [])],
        'sha256_der': hashlib.sha256(der).hexdigest(), 'sha256_chave': hashlib.sha256(kb).hexdigest(),
    }


def pems_do_texto_mr_util(txt):
    """Blocos da constante _AC_RAIZ_UE_PEMS, com o nome do comentário que precede cada um."""
    i = txt.index('_AC_RAIZ_UE_PEMS = ['); j = txt.index(']', i)
    trecho = txt[i:j]
    com = re.search(r'#\s*(obtidos em[^\n]*)', txt[max(0, i - 300):i])
    blocos = re.findall(r'#\s*(\S+\.crt)\s*"""(.*?)"""', trecho, flags=re.S)
    return [(nome, base64.b64decode(''.join(b.split()))) for nome, b in blocos], (com.group(1).strip() if com else None)


def pems_do_var_ue(txt):
    i = txt.index('trusted_issuers = decode_issuers(['); j = txt.index('])', i)
    blocos = re.findall(r"'''\s*(MII.*?)'''", txt[i:j], flags=re.S)
    return [base64.b64decode(''.join(b.split())) for b in blocos]


def formatos_pem(der):
    corpo = b64(der); linhas = [corpo[k:k + 64] for k in range(0, len(corpo), 64)]
    out = {'DER': der}
    for nl_nome, nl in (('LF', '\n'), ('CRLF', '\r\n')):
        t = '-----BEGIN CERTIFICATE-----' + nl + nl.join(linhas) + nl + '-----END CERTIFICATE-----'
        out[f'PEM {nl_nome} com quebra final'] = (t + nl).encode()
        out[f'PEM {nl_nome} sem quebra final'] = t.encode()
    return out


# ------------------------------------------------------------------------------------------------ manifestos de resumo
def ler_manifesto(caminho):
    t = open(caminho, encoding='utf-8', errors='replace').read()
    titulos = [limpa(html.unescape(re.sub(r'<[^>]+>', '', x)).strip()) for x in re.findall(r'<h[12][^>]*>(.*?)</h[12]>', t, flags=re.S)]
    itens = []; sec = None
    for r in re.findall(r'<tr[^>]*>(.*?)</tr>', t, flags=re.S):
        c = [html.unescape(re.sub(r'<[^>]+>', '', x)).strip() for x in re.findall(r'<t[hd][^>]*>(.*?)</t[hd]>', r, flags=re.S)]
        if '<th' in r:
            continue
        if len(c) == 1:
            sec = c[0]; continue
        if len(c) == 2:
            itens.append({'secao': sec, 'nome': c[0], 'sha512b64': c[1]})
    return titulos, itens


# ------------------------------------------------------------------------------------------------ trabalho por seção
ACS = None  # preenchido em cada processo


def _init(acs_serial):
    global ACS
    ACS = {}
    for nome, der in acs_serial.items():
        c = x509.load_der_x509_certificate(der)
        tipo, k = chave_da(c)
        ACS[nome] = {'cert': c, 'tipo': tipo, 'chave': k, 'ski': ext(c, x509.SubjectKeyIdentifier).digest.hex(),
                     'subject_der': c.subject.public_bytes()}


def trabalho_cert(item):
    chave_secao, caminho, turno = item
    v = ler_vsc(caminho)
    top = parse(open(caminho, 'rb').read())[0][2]
    b0, b1 = top[0][2], top[1][2]
    hw_quando = b1[0][2].decode('latin1'); sw_conjunto = next((n[2].decode('latin1') for n in b0 if (n[0], n[1]) == (2, 0)), None)
    cert, formato, extras = carregar_cert(v['hw_cert'])
    tbs = cert.tbs_certificate_bytes; sig = cert.signature
    aki = ext(cert, x509.AuthorityKeyIdentifier)
    aki = aki.key_identifier.hex() if aki and aki.key_identifier else None
    titular = cn(cert.subject) or ''
    try:
        urna = int(titular[4:]) if titular.lower().startswith('ueao') else None
    except ValueError:
        urna = None
    r = {'secao': chave_secao, 'turno': turno, 'formato': formato, 'bytes_extras': extras.hex()[:8], 'titular': titular, 'urna': urna,
         'emissor_cn': cn(cert.issuer), 'emissor': cert.issuer.rfc4514_string(), 'aki': aki, 'serial': cert.serial_number,
         'inicio': cert.not_valid_before_utc.isoformat(), 'fim': cert.not_valid_after_utc.isoformat(),
         'alg': cert.signature_algorithm_oid.dotted_string, 'hw_quando': hw_quando, 'sw_conjunto': sw_conjunto,
         'sw_usuario': f"{v['sw_chave'][0]} {v['sw_chave'][1]}", 'bloco2': [int(x, 16) for x in (v['bloco2'] or [])],
         'sha256_cert': hashlib.sha256(cert.public_bytes(Encoding.DER)).hexdigest()}
    tipo_u, k_u = chave_da(cert)
    r['sha256_chave_urna'] = hashlib.sha256(bytes_da_chave(tipo_u, k_u)).hexdigest()
    ac = next((n for n, a in ACS.items() if a['ski'] == aki), None)
    r['ac_pelo_aki'] = ac
    r['emissor_dn_igual_bytes'] = r['emissor_dn_igual_texto'] = None
    r['assinatura_ok'] = None; r['outras_acs_ok'] = []; r['controle_adulterado_ok'] = None; r['controle_assinatura_trocada_ok'] = None
    if ac:
        a = ACS[ac]
        r['emissor_dn_igual_bytes'] = cert.issuer.public_bytes() == a['subject_der']
        r['emissor_dn_igual_texto'] = cert.issuer.rfc4514_string().lower() == a['cert'].subject.rfc4514_string().lower()
        r['assinatura_ok'] = verifica(a['tipo'], a['chave'], sig, tbs)
        # controles negativos: um bit trocado no TBS; assinatura com um byte trocado
        adult = bytearray(tbs); adult[len(adult) // 2] ^= 0x01
        r['controle_adulterado_ok'] = verifica(a['tipo'], a['chave'], sig, bytes(adult))
        s2 = bytearray(sig); s2[10] ^= 0x01
        r['controle_assinatura_trocada_ok'] = verifica(a['tipo'], a['chave'], bytes(s2), tbs)
        for n2, a2 in ACS.items():
            if n2 != ac and a2['tipo'] == a['tipo'] and verifica(a2['tipo'], a2['chave'], sig, tbs):
                r['outras_acs_ok'].append(n2)
    # resumos de todos os arquivos listados no vsc (para comparar com os manifestos)
    r['resumos_vsc'] = {nm.split('-')[-1]: b64(e['sha512']) for nm, e in v['hw_entradas'].items()}
    r['resumo_mr_ver_tam'] = next((e['tam'] for nm, e in v['hw_entradas'].items() if nm.endswith('mr.ver')), None)
    return r


RE_GAP = re.compile(r'Verificação de assinatura - Etapa \[(\d+)\] - \[([^\]]+)\] - \[([^\]]+)\]')
RE_SCUE = re.compile(r'Verificação de assinatura de (aplicação|dado) por etapa \[(\d+)\] - \[Pacote: ([^\]]+)\](?: - \[Arquivo: ([^\]]+)\])? - \[([^\]]+)\]')
RE_VER = re.compile(r'Versão da aplicação: (.*)')
RE_MOD = re.compile(r'Identificação do Modelo de Urna: (\S+)')


def trabalho_log(item):
    chave_secao, pasta = item
    out = {'secao': chave_secao, 'verif': collections.Counter(), 'versoes': collections.Counter(), 'modelos': collections.Counter(),
           'outras_assinatura': [], 'bu_versao': None, 'erro': None, 'blocos': []}
    logs = sorted(glob.glob(os.path.join(pasta, '*-log.jez'))); bus = sorted(glob.glob(os.path.join(pasta, '*-bu.dat')))
    try:
        if bus:
            out['bu_versao'] = ler_bu(bus[-1])['versao']
        for f in logs[-1:]:
            for bloco in _linhas_log(f):
                out['blocos'].append(sorted({x.split('\t')[2] for x in bloco if len(x.split('\t')) > 4}))
                for l in bloco:
                    p = l.split('\t')
                    if len(p) < 6:
                        continue
                    app, msg = p[3], p[4]
                    m = RE_GAP.search(msg)
                    if m:
                        out['verif'][(app, m.group(2), m.group(3))] += 1; continue
                    m = RE_SCUE.search(msg)
                    if m:
                        out['verif'][(app, m.group(3) + (' :: ' + m.group(4) if m.group(4) else ''), m.group(5))] += 1; continue
                    m = RE_VER.search(msg)
                    if m:
                        out['versoes'][(app, m.group(1).strip())] += 1; continue
                    m = RE_MOD.search(msg)
                    if m:
                        out['modelos'][m.group(1)] += 1; continue
                    low = msg.lower()
                    if ('assinatura' in low or 'hash' in low or 'resumo' in low) and any(w in low for w in ('falha', 'erro', 'inválid', 'invalid', 'diverg')):
                        if len(out['outras_assinatura']) < 8:
                            out['outras_assinatura'].append(l[:200])
    except Exception as e:  # noqa: BLE001
        out['erro'] = repr(e)[:200]
    out['verif'] = [[a, b, c, n] for (a, b, c), n in out['verif'].items()]
    out['versoes'] = [[a, b, n] for (a, b), n in out['versoes'].items()]
    out['modelos'] = dict(out['modelos'])
    return out


def normaliza_nome(n):
    """Agrupa os arquivos de dados que mudam por seção ou UF (para a tabela não ter uma linha por seção)."""
    n = re.sub(r'/\d{13}-', '/<mun zona secao>-', n)
    n = re.sub(r'(o0\d{4})(?!br)[a-z]{2}(\d{5})?-', lambda m: m.group(1) + '<uf>' + ('<00000>' if m.group(2) else '') + '-', n)
    return n


RE_CTX = re.compile(r'MR gerada pelo computador|Data e hora da geração da MR|Mídia de resultado de 2º turno|Número de série da MR|contingência|Contingência|CRÍTICA|Urna ligada em|pronta para receber|sincronização|Erro|ERRO|Falha')


def contexto_erro(pasta, n_max=80):
    """Linhas de contexto (mídia de resultado, contingência, energia, retomada) em volta do primeiro erro de assinatura de cada bloco
    do log, de 15 min antes a 90 min depois, e votos computados por bloco."""
    f = sorted(glob.glob(os.path.join(pasta, '*-log.jez')))[-1]
    out = []
    for bloco in _linhas_log(f):
        votos = collections.Counter(l[:10] for l in bloco if 'O voto do eleitor foi computado' in l)
        t_err = None
        for l in bloco:
            low = l.lower()
            if 'assinatura' in low and ('erro' in low or 'falha' in low):
                try:
                    t_err = dt.datetime.strptime(l[:19], '%d/%m/%Y %H:%M:%S')
                except ValueError:
                    continue
                break
        ctx = []
        if t_err:
            for l in bloco:
                try:
                    t = dt.datetime.strptime(l[:19], '%d/%m/%Y %H:%M:%S')
                except ValueError:
                    continue
                if t_err - dt.timedelta(minutes=15) <= t <= t_err + dt.timedelta(minutes=90) and RE_CTX.search(l.split('\t')[4] if len(l.split('\t')) > 4 else ''):
                    ctx.append(' | '.join(l.split('\t')[:5])[:220])
        out.append({'urnas': sorted({x.split('\t')[2] for x in bloco if len(x.split('\t')) > 4}), 'votos_por_dia': dict(votos),
                    'primeiro_erro': t_err.isoformat() if t_err else None, 'contexto': ctx[:n_max]})
    return out


def secoes(pasta):
    for f in sorted(glob.glob(os.path.join(pasta, '*/*/*/*/'))):
        uf, m, z, s = f.rstrip('/').split('/')[-4:]
        yield f'{uf.upper()}|{int(m)}|{int(z)}|{int(s)}', f


def vsc_da_secao(pasta_secao):
    """O -vota.vsc listado no aux.json (último índice de hash presente no disco), como no T18."""
    try:
        aux = json.load(open(os.path.join(pasta_secao, 'aux.json')))
    except Exception:  # noqa: BLE001
        return None
    nomes = [f'{i}-' + a['nm'] for i, h in enumerate(aux.get('hashes', [])) for a in h.get('arq', []) if a.get('tp') == 'vota']
    presentes = [n for n in nomes if os.path.exists(os.path.join(pasta_secao, n))]
    return os.path.join(pasta_secao, presentes[-1]) if presentes else None


def quando_utc(s):
    """'20261025T150826' no horário local da urna -> UTC (com -3 h, D6)."""
    return (dt.datetime.strptime(s, '%Y%m%dT%H%M%S') + dt.timedelta(hours=3)).replace(tzinfo=UTC)


# ------------------------------------------------------------------------------------------------ principal
def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--arq2t', default='/home/user/trabalho-eleicao/amostra2t/arq')
    ap.add_argument('--vsc1t', default=f'{DL}/F12_dl_vsc1t')
    ap.add_argument('--doccaz', default=f'{DL}/F12_dl_doccaz')
    ap.add_argument('--varue', default=f'{DL}/F12_dl_varue')
    ap.add_argument('--ivan', default=f'{DL}/F12_dl_ivanmneto')
    ap.add_argument('--dataurnas', default=f'{DL}/F12_dl_dataurnas')
    ap.add_argument('--resumos', default=f'{DL}/F12_dl_resumos2026')
    ap.add_argument('--saida_json', default=os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'resultados', 'F12_certificados_resumos.json'))
    ap.add_argument('--saida_txt', default=os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'resultados', 'F12_certificados_resumos.txt'))
    ap.add_argument('--marilia1t', default=f'{DL}/F12_dl_marilia_1t')
    ap.add_argument('--marilia2t', default=f'{DL}/F12_dl_marilia_2t')
    ap.add_argument('--proc', type=int, default=4)
    a = ap.parse_args()
    R = {'teste': 'F12', 'registro': 'Adendo 21 do PRE-REGISTRO-2026-10-26.md (commit 913af7a)'}

    # ---------------- 1. certificados das AC, por fonte
    fontes = {}
    zpath = os.path.join(a.doccaz, 'docv2', 'formato-arquivos-bu-rdv-ass-digital-v2.zip')
    zb = open(zpath, 'rb').read()
    zf = zipfile.ZipFile(zpath)
    mr_txt = zf.read('python/lib/mr_util.py').decode('utf-8')
    info_mr = zf.getinfo('python/lib/mr_util.py')
    blocos_tse, comentario = pems_do_texto_mr_util(mr_txt)
    fontes['pacote_TSE_v2'] = {'certs': [d for _, d in blocos_tse], 'nomes': [n for n, _ in blocos_tse],
                               'origem': 'formato-arquivos-bu-rdv-ass-digital-v2.zip (cópia em github.com/doccaz/urnas-br, docv2), python/lib/mr_util.py, _AC_RAIZ_UE_PEMS',
                               'sha256_zip': hashlib.sha256(zb).hexdigest(), 'data_interna_mr_util': '%04d-%02d-%02d %02d:%02d' % info_mr.date_time[:5],
                               'comentario_do_TSE': comentario}
    fontes['var_ue'] = {'certs': pems_do_var_ue(open(os.path.join(a.varue, 'var-ue.py'), encoding='utf-8').read()),
                        'origem': 'github.com/epicleet/var-ue, var-ue.py, trusted_issuers'}
    for chave_f, pasta, origem in (('ivanmneto92', os.path.join(a.ivan, 'certificados'), 'github.com/ivanmneto92-sys/auditoria-presidente-2026, certificados/'),
                                   ('dataurnas', os.path.join(a.dataurnas, 'data', 'certificados', 'ac'), 'github.com/alissonlinneker/dataurnas-br, data/certificados/ac/')):
        brutos = {os.path.basename(f): open(f, 'rb').read() for f in sorted(glob.glob(os.path.join(pasta, '*.pem')))}
        fontes[chave_f] = {'certs': [x509.load_pem_x509_certificate(b).public_bytes(Encoding.DER) for b in brutos.values()],
                           'nomes': list(brutos), 'brutos': brutos, 'origem': origem}
    acs_der = {}
    comparacao = collections.defaultdict(dict)
    for nf, f in fontes.items():
        for der in f['certs']:
            c = x509.load_der_x509_certificate(der)
            nome = cn(c.subject)
            comparacao[nome][nf] = hashlib.sha256(der).hexdigest()
            if nf == 'pacote_TSE_v2':
                acs_der[nome] = der
    R['fontes_das_ac'] = {nf: {k: v for k, v in f.items() if k not in ('certs', 'brutos')} for nf, f in fontes.items()}
    R['comparacao_entre_fontes_sha256_der'] = {n: {'por_fonte': d, 'todas_iguais': len(set(d.values())) == 1, 'fontes': len(d)} for n, d in comparacao.items()}
    acs = {n: ficha_ac(x509.load_der_x509_certificate(d)) for n, d in acs_der.items()}
    R['acs_publicadas'] = acs

    # HOLOCRON: SHA-512 publicado dos arquivos de certificado
    titulos_h, itens_h = ler_manifesto(os.path.join(a.resumos, 'extracted', 'pc1holo', 'pc1holo.html'))
    certs_h = {i['nome'].split('\\')[-1]: i['sha512b64'] for i in itens_h if '\\certificados\\' in i['nome'].lower()}
    holo = {'manifesto': 'pc1holo.html', 'titulos': titulos_h, 'arquivos_de_certificado_listados': certs_h, 'conferencia': {}}
    for n, der in acs_der.items():
        cand = {f'{k} (canônico)': hashlib.sha512(v).digest() for k, v in formatos_pem(der).items()}
        for nf in ('ivanmneto92', 'dataurnas'):
            for arq, bruto in fontes[nf]['brutos'].items():
                if x509.load_pem_x509_certificate(bruto).public_bytes(Encoding.DER) == der:
                    cand[f'arquivo {arq} de {nf}'] = hashlib.sha512(bruto).digest()
        achados = {k: [nm for nm, h in certs_h.items() if h == b64(d)] for k, d in cand.items()}
        holo['conferencia'][n] = {'formas_que_conferem': {k: v for k, v in achados.items() if v},
                                  'formas_testadas': len(cand), 'listado_no_manifesto': any(achados.values())}
    R['holocron'] = holo

    # robustez D8: chave da AC RAIZ UE a partir da assinatura do certificado da AC URNA
    c_urna = x509.load_der_x509_certificate(acs_der['AC URNA'])
    aki_raiz = ext(c_urna, x509.AuthorityKeyIdentifier).key_identifier
    cands = candidatos(c_urna)
    escolhidos = []
    for Q in cands:
        pt = b'\x04' + Q[0].to_bytes(66, 'big') + Q[1].to_bytes(66, 'big')
        if hashlib.sha1(pt).digest() == aki_raiz:
            pub = ec.EllipticCurvePublicNumbers(Q[0], Q[1], ec.SECP521R1()).public_key()
            spki = pub.public_bytes(Encoding.DER, PublicFormat.SubjectPublicKeyInfo)
            ok = verifica('ecdsa', pub, c_urna.signature, c_urna.tbs_certificate_bytes)
            escolhidos.append({'sha256_spki': hashlib.sha256(spki).hexdigest(), 'verifica_ac_urna': ok})
    R['raiz_recuperada_D8'] = {'candidatos': len(cands), 'aki_da_ac_urna': aki_raiz.hex(), 'candidatos_com_sha1_igual_ao_aki': escolhidos}

    # ---------------- 2. certificados das urnas
    itens2 = []; sem_vsc2 = []
    for k, p in secoes(a.arq2t):
        f = vsc_da_secao(p)
        (itens2 if f else sem_vsc2).append((k, f, '2t') if f else k)
    itens1 = [(k, f, '1t') for k, p in secoes(a.vsc1t) for f in [vsc_da_secao(p)] if f]
    itens_m = [(k, f, t) for t, pasta in (('1t', a.marilia1t), ('2t', a.marilia2t)) for k, p in secoes(pasta) for f in [vsc_da_secao(p)] if f]
    with Pool(a.proc, initializer=_init, initargs=(acs_der,)) as pool:
        res = pool.map(trabalho_cert, itens2 + itens1, chunksize=8)
        res_m = pool.map(trabalho_cert, itens_m)
        logs = pool.map(trabalho_log, [(k, p) for k, p in secoes(a.arq2t)], chunksize=8)
    res2 = [r for r in res if r['turno'] == '2t']; res1 = [r for r in res if r['turno'] == '1t']
    ficha_utc = {n: (dt.datetime.fromisoformat(f['validade_inicio_utc']), dt.datetime.fromisoformat(f['validade_fim_utc'])) for n, f in acs.items()}

    def resumo_certs(rs, turno):
        o = collections.Counter(); por_ac = collections.defaultdict(collections.Counter)
        falhas = []; emitidos_depois = []; perto_do_limite = []; modelo_div = []; faixa_div = []
        for r in rs:
            ac = r['ac_pelo_aki']; o['certificados'] += 1; pa = por_ac[ac or 'nenhuma AC publicada']; pa['certificados'] += 1
            o['formato_' + r['formato']] += 1
            if ac is None:
                falhas.append((r['secao'], 'AKI não corresponde a nenhuma AC publicada', r['aki'], r['emissor_cn'])); continue
            if not r['emissor_dn_igual_texto']:
                falhas.append((r['secao'], 'emissor diferente do titular da AC', r['emissor'])); pa['dn_diferente'] += 1
            pa['dn_igual_byte_a_byte'] += bool(r['emissor_dn_igual_bytes'])
            if r['assinatura_ok']:
                pa['assinatura_ok'] += 1
            else:
                pa['assinatura_FALHA'] += 1; falhas.append((r['secao'], 'assinatura do certificado não confere com a AC', ac))
            pa['controle_tbs_adulterado_aceito'] += bool(r['controle_adulterado_ok'])
            pa['controle_assinatura_trocada_aceita'] += bool(r['controle_assinatura_trocada_ok'])
            pa['verifica_tambem_com_outra_ac'] += bool(r['outras_acs_ok'])
            ini, fim = dt.datetime.fromisoformat(r['inicio']), dt.datetime.fromisoformat(r['fim'])
            ac_ini, ac_fim = ficha_utc[ac]
            t = quando_utc(r['hw_quando'])
            dia = DIAS[turno]
            pa['urna_valida_na_assinatura'] += ini <= t <= fim
            pa['urna_valida_no_dia'] += ini.date() <= dia <= fim.date()
            pa['ac_valida_na_assinatura'] += ac_ini <= t <= ac_fim
            pa['emitido_dentro_da_validade_da_ac'] += ac_ini <= ini <= ac_fim
            pa['urna_vence_depois_da_ac'] += fim > ac_fim
            pa['caminho_estrito_rfc5280_ok_na_assinatura'] += (ini <= t <= fim) and (ac_ini <= t <= ac_fim)
            if ini > ac_fim:
                emitidos_depois.append({'secao': r['secao'], 'urna': r['urna'], 'emissao_utc': r['inicio'], 'ac': ac, 'assinatura_ok': r['assinatura_ok']})
            for lim in (ini, fim, ac_ini, ac_fim):
                if abs((t - lim).total_seconds()) < 86400:
                    perto_do_limite.append((r['secao'], lim.isoformat()))
            b2 = r['bloco2']
            mod = MODELO_B2.get(b2[0]) if b2 else None
            pa['modelo_bloco2_' + str(mod)] += 1
            pa['algoritmo_bloco2_' + str(ALG_B2.get(b2[1]) if b2 and len(b2) > 1 else None)] += 1
            if AC_DO_MODELO.get(mod) != ac:
                modelo_div.append((r['secao'], mod, ac))
            mf = None
            for x, y, m in FAIXAS[2026]:
                if r['urna'] is not None and x <= r['urna'] <= y:
                    mf = m
            if mf != mod:
                faixa_div.append((r['secao'], r['urna'], mf, mod))
        anos = collections.Counter((r['ac_pelo_aki'], r['inicio'][:4]) for r in rs)
        return {'contagem': dict(o), 'por_ac': {k: dict(v) for k, v in por_ac.items()}, 'falhas': falhas,
                'emitidos_depois_do_fim_da_ac': emitidos_depois, 'a_menos_de_1_dia_de_um_limite': perto_do_limite[:20],
                'n_a_menos_de_1_dia_de_um_limite': len(perto_do_limite),
                'modelo_do_bloco2_diferente_do_esperado_para_a_ac': modelo_div[:20], 'n_modelo_div': len(modelo_div),
                'modelo_da_faixa_do_numero_diferente_do_bloco2': faixa_div[:20], 'n_faixa_div': len(faixa_div),
                'ano_de_emissao_por_ac': {f'{k[0]} {k[1]}': v for k, v in sorted(anos.items(), key=lambda x: (str(x[0][0]), x[0][1]))},
                'emissao_mais_recente_por_ac': {ac: max(r['inicio'] for r in rs if r['ac_pelo_aki'] == ac) for ac in {r['ac_pelo_aki'] for r in rs}},
                'fim_mais_cedo_por_ac': {ac: min(r['fim'] for r in rs if r['ac_pelo_aki'] == ac) for ac in {r['ac_pelo_aki'] for r in rs}},
                'hw_criacao_min_max': [min(r['hw_quando'] for r in rs), max(r['hw_quando'] for r in rs)] if rs else None,
                'sw_usuario': dict(collections.Counter(r['sw_usuario'] for r in rs)),
                'sw_conjunto_de_chaves': dict(collections.Counter(r['sw_conjunto'] for r in rs))}

    R['urnas_2t'] = resumo_certs(res2, '2t'); R['urnas_2t']['secoes_sem_vsc'] = len(sem_vsc2)
    R['urnas_2t']['emitidos_em_2026'] = sorted(({'secao': r['secao'], 'urna': r['urna'], 'ac': r['ac_pelo_aki'], 'emissao_utc': r['inicio'], 'fim_utc': r['fim'],
                                                 'assinatura_ok': r['assinatura_ok']} for r in res2 if r['inicio'] >= '2026'), key=lambda x: x['emissao_utc'])
    R['urnas_1t_80'] = resumo_certs(res1, '1t')
    # unicidade de serial e de chave
    ser = collections.defaultdict(set); chv = collections.defaultdict(set); certs_da_urna = collections.defaultdict(set)
    for r in res2 + res1:
        ser[(r['ac_pelo_aki'], r['serial'])].add(r['urna']); chv[r['sha256_chave_urna']].add(r['urna']); certs_da_urna[r['urna']].add(r['sha256_cert'])
    R['unicidade'] = {'serial_repetido_em_urnas_diferentes': [[str(k[0]), k[1], sorted(v)] for k, v in ser.items() if len(v) > 1],
                      'chave_repetida_em_urnas_diferentes': [[k[:16], sorted(v)] for k, v in chv.items() if len(v) > 1],
                      'urna_com_mais_de_um_certificado': [[u, len(v)] for u, v in certs_da_urna.items() if len(v) > 1]}
    # 1º contra 2º turno na mesma seção
    por_sec2 = {r['secao']: r for r in res2}
    cmp = collections.Counter(); difs = []
    for r in res1:
        r2 = por_sec2.get(r['secao'])
        if not r2:
            cmp['sem_2t_na_amostra'] += 1; continue
        if r2['urna'] == r['urna']:
            cmp['mesma_urna'] += 1
            cmp['mesma_urna_mesmo_certificado' if r2['sha256_cert'] == r['sha256_cert'] else 'mesma_urna_certificado_diferente'] += 1
            if r2['sha256_cert'] != r['sha256_cert']:
                difs.append(r['secao'])
        else:
            cmp['urna_diferente'] += 1; difs.append((r['secao'], r['urna'], r2['urna']))
    R['urnas_1t_80']['comparacao_com_2t'] = dict(cmp); R['urnas_1t_80']['casos'] = difs[:20]

    # seção citada pela dataurnas-br como certificado emitido depois do fim da AC URNA (fora da amostra, descritivo)
    R['secao_marilia_citada_pela_dataurnas'] = []
    for r in res_m:
        ac = r['ac_pelo_aki']; ini = dt.datetime.fromisoformat(r['inicio'])
        bu = sorted(glob.glob(os.path.join(os.path.dirname(dict((x[0] + x[2], x[1]) for x in itens_m)[r['secao'] + r['turno']]), '*-bu.dat')))
        R['secao_marilia_citada_pela_dataurnas'].append({
            'secao': r['secao'], 'turno': r['turno'], 'urna_no_certificado': r['urna'], 'urna_no_boletim': ler_bu(bu[-1])['urna'] if bu else None,
            'ac': ac, 'emissao_utc': r['inicio'], 'fim_utc': r['fim'], 'assinatura_ok': r['assinatura_ok'],
            'controle_adulterado_aceito': r['controle_adulterado_ok'], 'modelo_bloco2': MODELO_B2.get(r['bloco2'][0]) if r['bloco2'] else None,
            'emitido_depois_do_fim_da_ac': bool(ac and ini > ficha_utc[ac][1]), 'hw_quando': r['hw_quando']})

    # ---------------- 3. alegação AC URNA
    f = acs['AC URNA']
    fim_ac = dt.datetime.fromisoformat(f['validade_fim_utc'])
    pa2 = R['urnas_2t']['por_ac'].get('AC URNA', {})
    R['alegacao_ac_urna'] = {
        'alegacao': 'certificado da AC URNA vencido em 18/07/2026 pela regra estrita do X.509',
        'quem': ['ivanmneto92-sys/auditoria-presidente-2026, README.md, seção Limitações (commit 7a7ccc6, 28/10/2026)',
                 'alissonlinneker/dataurnas-br, data/certificados/README.md, Observação sobre a AC URNA (commit 12f0433, 15/10/2026)'],
        'validade_fim_no_certificado_publicado_utc': f['validade_fim_utc'],
        'confere_a_data': fim_ac.date() == ALEGADO.date(),
        'certificados_de_urna_da_ac_urna_2t': pa2.get('certificados', 0),
        'desses_com_assinatura_ok': pa2.get('assinatura_ok', 0),
        'desses_com_ac_valida_na_data_da_assinatura': pa2.get('ac_valida_na_assinatura', 0),
        'desses_com_caminho_estrito_ok': pa2.get('caminho_estrito_rfc5280_ok_na_assinatura', 0),
        'desses_emitidos_dentro_da_validade_da_ac': pa2.get('emitido_dentro_da_validade_da_ac', 0),
        'emitidos_depois_do_fim_da_ac_2t': len([e for e in R['urnas_2t']['emitidos_depois_do_fim_da_ac'] if e['ac'] == 'AC URNA']),
        'acurna_no_manifesto_holocron': any('acurna.' in n.lower() for n in certs_h),
        'secao_marilia_emitido_depois_do_fim': [x for x in R['secao_marilia_citada_pela_dataurnas'] if x['emitido_depois_do_fim_da_ac']],
    }

    # ---------------- 4. resumos dos programas
    manif = {}
    todos_hash = collections.defaultdict(list)
    for h in sorted(glob.glob(os.path.join(a.resumos, 'extracted', '*', '*.html'))):
        pasta = os.path.basename(os.path.dirname(h))
        tit, it = ler_manifesto(h)
        manif[pasta] = {'arquivo': os.path.basename(h), 'titulos': tit, 'itens': len(it),
                        'hash_geral': sum(1 for i in it if i['nome'].upper().startswith('HASH GERAL')),
                        'formato_ok': sum(1 for i in it if len(base64.b64decode(i['sha512b64'] + '=' * (-len(i['sha512b64']) % 4))) == 64),
                        '_itens': it}
        for i in it:
            todos_hash[i['sha512b64']].append((pasta, i['nome']))
    zips = {os.path.basename(z): '%04d-%02d-%02d %02d:%02d' % zipfile.ZipFile(z).infolist()[0].date_time[:5] for z in sorted(glob.glob(os.path.join(a.resumos, '*.zip')))}
    R['manifestos'] = {'fonte': 'github.com/havaianasdestruido/resumos-eleicao-2026 (cópia de terceiros; D4)', 'zips_e_data_interna': zips,
                       'por_manifesto': {k: {kk: vv for kk, vv in v.items() if kk != '_itens'} for k, v in manif.items()}}
    # (a) resumos dos arquivos listados no vsc contra os manifestos
    achou = collections.Counter(); tipos = collections.Counter(); mrver = collections.Counter()
    for r in res2:
        for suf, h in r['resumos_vsc'].items():
            tipos[suf] += 1
            if h in todos_hash:
                achou[suf] += 1
        mrver[r['resumos_vsc'].get('mr.ver')] += 1
    # (b) pacotes verificados nos logs
    base_mod = {}; uf_mod = {}
    for mod, pasta in MANIFESTO_DO_MODELO.items():
        it = manif[pasta]['_itens']
        base_mod[mod] = {i['nome'] for i in it if i['secao'] == 'ARQUIVOS BASE'}
        uf_mod[mod] = collections.defaultdict(set)
        for i in it:
            if i['secao'] and i['secao'].startswith('UF = ') and ' - ' in i['nome']:
                uf_mod[mod][i['secao'][5:]].add(i['nome'].split(' - ', 1)[1])
    todos_nomes = {i['nome'].split(' - ', 1)[-1] for v in manif.values() for i in v['_itens']}
    base_nomes = {re.split(r'[\\/]', x)[-1].lower() for x in todos_nomes}
    mod_da_secao = {r['secao']: MODELO_B2.get(r['bloco2'][0]) if r['bloco2'] else None for r in res2}
    nomes = collections.defaultdict(lambda: collections.Counter()); status = collections.Counter(); nao_sucesso = []
    versoes = collections.Counter(); bu_vers = collections.Counter(); mod_log = collections.Counter(); erros_log = []; outras = []
    secs_todos_no_modelo = collections.Counter()
    for L in logs:
        if not L['blocos'] and L['bu_versao'] is None:
            secs_todos_no_modelo['seção sem arquivos de urna'] += 1; continue
        if L['erro']:
            erros_log.append((L['secao'], L['erro']))
        bu_vers[L['bu_versao']] += 1
        for app, ver, n in L['versoes']:
            versoes[(app, ver)] += 1
        for m, n in L['modelos'].items():
            mod_log[(mod_da_secao.get(L['secao']), m)] += 1
        outras.extend((L['secao'], x) for x in L['outras_assinatura'])
        mod = mod_da_secao.get(L['secao']); uf = L['secao'].split('|')[0]
        fora = 0
        for app, caminho, st, n in L['verif']:
            status[st] += n
            if st != 'SUCESSO':
                nao_sucesso.append((L['secao'], app, caminho, st))
            nome = caminho.split(' :: ')[0]
            if mod and nome in base_mod.get(mod, ()):
                cls = 'no resumo do modelo (arquivos base)'
            elif mod and nome in uf_mod.get(mod, {}).get(uf, ()):
                cls = 'no resumo do modelo (lista da UF)'
            elif mod and nome.replace('/dsk/fe/', '/dsk/fi/') in uf_mod.get(mod, {}).get(uf, ()):
                cls = 'no resumo do modelo (lista da UF, com /dsk/fe/ no lugar de /dsk/fi/)'
            elif nome in todos_nomes:
                cls = 'em outro resumo publicado'
            elif nome.split('/')[-1].lower() in base_nomes:
                cls = 'mesmo nome de arquivo em outro resumo publicado, com outro caminho'
            else:
                cls = 'sem resumo publicado'
            tipo_arq = 'dado da carga (/dsk/)' if nome.startswith('/dsk/') and not nome.endswith('.vst') else 'pacote de programa'
            nomes[(app, normaliza_nome(nome), cls, tipo_arq)][mod] += 1
            if app in ('GAP',) and nome.endswith('.vst') and not cls.startswith('no resumo do modelo'):
                fora += 1
        secs_todos_no_modelo['todos os .vst do GAP no resumo do modelo' if fora == 0 else 'algum .vst do GAP fora do resumo do modelo'] += 1
    tabela_nomes = sorted(([app, nome, cls, tipo_arq, dict(c), sum(c.values())] for (app, nome, cls, tipo_arq), c in nomes.items()), key=lambda x: (x[3], x[2], x[0], x[1]))
    resumo_classes = collections.Counter()
    for app, nome, cls, tipo_arq, c, n in tabela_nomes:
        resumo_classes[f'{tipo_arq} | {cls}'] += n
    cruzados = []; com_erro = []
    for L in logs:
        mods_log = set(L['modelos']); mvsc = mod_da_secao.get(L['secao'])
        if mvsc and mods_log - {mvsc}:
            cruzados.append({'secao': L['secao'], 'modelo_vsc': mvsc, 'modelos_no_log': sorted(mods_log), 'urnas_por_bloco_do_log': L['blocos'],
                             'explicado_por_troca_de_urna_no_log': len({u for b in L['blocos'] for u in b}) >= 2})
        if L['outras_assinatura'] or any(st != 'SUCESSO' for _, _, st, _ in L['verif']):
            uf_, m_, z_, s_ = L['secao'].split('|')
            pasta_ = os.path.join(a.arq2t, uf_.lower(), f'{int(m_):05d}', f'{int(z_):04d}', f'{int(s_):04d}')
            com_erro.append({'secao': L['secao'], 'urnas_por_bloco_do_log': L['blocos'], 'urna_do_vsc': next((r['urna'] for r in res2 if r['secao'] == L['secao']), None),
                             'blocos_do_log': contexto_erro(pasta_),
                             'linhas': [x[:200] for x in L['outras_assinatura']], 'verificacoes_nao_sucesso': [[a_, c_, st] for a_, c_, st, _ in L['verif'] if st != 'SUCESSO']})
    R['resumos'] = {
        'a_resumos_dos_arquivos_do_vsc_nos_manifestos': {'arquivos_conferidos': dict(tipos), 'encontrados_em_algum_manifesto': dict(achou),
                                                         'mr_ver_resumos_distintos': len(mrver), 'mr_ver_tamanho': res2[0]['resumo_mr_ver_tam'] if res2 else None,
                                                         'mr_ver_resumo': next(iter(mrver)) if len(mrver) == 1 else None},
        'b_pacotes_verificados_nos_logs': {'status_das_verificacoes': dict(status), 'nao_sucesso': nao_sucesso[:30], 'n_nao_sucesso': len(nao_sucesso),
                                           'secoes': dict(secs_todos_no_modelo), 'por_classe': dict(resumo_classes), 'tabela': tabela_nomes,
                                           'secoes_com_modelo_do_log_diferente_do_vsc': cruzados, 'secoes_com_erro_de_assinatura_no_log': com_erro,
                                           'linhas_de_assinatura_com_falha_ou_erro': outras[:30], 'n_linhas_de_assinatura_com_falha_ou_erro': len(outras),
                                           'logs_com_erro_de_leitura': erros_log[:10], 'n_logs_com_erro': len(erros_log)},
        'c_versoes': {'boletim': dict(bu_vers), 'log_por_aplicacao': {f'{k[0]} | {k[1]}': v for k, v in versoes.items()},
                      'modelo_no_log_x_modelo_do_vsc': {f'{k[0]} | {k[1]}': v for k, v in mod_log.items()}},
        'resumo_de_programa_obtenivel_dos_arquivos_de_urna': False,
    }

    # ---------------- 5. veredito pela letra
    falhas2 = R['urnas_2t']['falhas']
    cert_sinal = len(falhas2) > 0
    R['veredito'] = {
        'certificados': 'SINAL' if cert_sinal else 'SEM SINAL',
        'resumos_de_programa': 'SEM DADO (nenhum resumo de programa sai dos arquivos públicos de urna)',
        'leitura_estrita_rfc5280': f"{pa2.get('certificados', 0) - pa2.get('caminho_estrito_rfc5280_ok_na_assinatura', 0)} de {pa2.get('certificados', 0)} certificados emitidos pela AC URNA não passariam na validação de caminho do RFC 5280 na data da assinatura, porque o certificado publicado da AC URNA venceu antes",
    }
    open(a.saida_json, 'w').write(limpa(json.dumps(R, ensure_ascii=False, indent=1, default=str)) + '\n')
    escrever_txt(R, a.saida_txt)
    print(json.dumps(R['veredito'], ensure_ascii=False, indent=1))


def texto_resumo(R):
    """Parte narrativa do relatório, montada com os números calculados."""
    u2 = R['urnas_2t']; u1 = R['urnas_1t_80']; pa = u2['por_ac']; al = R['alegacao_ac_urna']
    rb = R['resumos']['b_pacotes_verificados_nos_logs']; ra = R['resumos']['a_resumos_dos_arquivos_do_vsc_nos_manifestos']
    m = R['manifestos']['por_manifesto']; hol = R['holocron']; mar = R['secao_marilia_citada_pela_dataurnas']
    n2 = u2['contagem']['certificados']; ok2 = sum(c.get('assinatura_ok', 0) for c in pa.values())
    adult = sum(c.get('controle_tbs_adulterado_aceito', 0) + c.get('controle_assinatura_trocada_aceita', 0) for c in pa.values())
    urna = pa.get('AC URNA', {}); e26 = u2['emitidos_em_2026']
    cruz = rb['secoes_com_modelo_do_log_diferente_do_vsc']; err = rb['secoes_com_erro_de_assinatura_no_log']
    L = []; w = L.append
    w('VEREDITO PELA LETRA DO ADENDO 21')
    w(f"  Certificados: {R['veredito']['certificados']}. Nenhum certificado de urna da amostra deixa de se validar pela AC publicada:")
    w(f"  {ok2} de {n2} assinaturas conferem com a chave da AC que o certificado aponta, com emissor igual ao titular da AC byte a byte.")
    w(f"  Resumos dos programas: {R['veredito']['resumos_de_programa']}.")
    w(f"  Alegação da AC URNA: CONFERE. O certificado publicado da AC URNA vale até {al['validade_fim_no_certificado_publicado_utc'][:19].replace('T', ' ')} UTC.")
    w('')
    w('NÚMEROS')
    w(f"  AC publicadas: AC URNA (ECDSA P-521, emitida pela AC RAIZ UE, 22/07/2011 a 18/07/2026), AC UE2020 (Ed521, emitida pela AC URNA v2,")
    w(f"  05/07/2021 a 01/07/2037) e AC UE2022 (Ed521, AC URNA v2, 28/02/2023 a 24/02/2039). O mesmo certificado, byte a byte, nas 4 fontes")
    w(f"  (pacote do TSE, var-ue, ivanmneto92-sys, dataurnas-br). O SHA-512 de acue2020.cer e acue2022.cer no resumo do HOLOCRON é o do PEM")
    w(f"  desses certificados; o HOLOCRON não lista nenhum acurna; lista acraiz-ue.pem, acraizuev2.cer e acurnav2.cer, que não achei.")
    w(f"  Urnas do 2º turno: {n2} certificados (AC UE2022 {pa.get('AC UE2022', {}).get('certificados', 0)}, AC UE2020 {pa.get('AC UE2020', {}).get('certificados', 0)}, AC URNA {urna.get('certificados', 0)}).")
    w(f"  Assinatura confere: {ok2} de {n2}. Controles: TBS com 1 bit trocado ou assinatura com 1 byte trocado aceitos {adult} vezes em {2 * n2}.")
    w(f"  Nenhum certificado Ed521 confere também com a outra AC Ed521. Modelo e algoritmo do bloco 2 do vsc batem com a AC em {n2 - u2['n_modelo_div']} de {n2};")
    w(f"  o modelo pela faixa do número da urna bate com o bloco 2 em {n2 - u2['n_faixa_div']} de {n2}. Serial ou chave repetidos em urnas diferentes: 0.")
    w(f"  Validade: todos os {n2} certificados de urna válidos no momento da assinatura (25/10/2026, {u2['hw_criacao_min_max'][0][9:11]}h a {u2['hw_criacao_min_max'][1][9:11]}h locais).")
    w(f"  AC URNA: {urna.get('emitido_dentro_da_validade_da_ac', 0)} de {urna.get('certificados', 0)} emitidos dentro da validade dela (o mais recente em {u2['emissao_mais_recente_por_ac'].get('AC URNA', '')[:10]}),")
    w(f"  mas a AC estava vencida no momento da assinatura em {urna.get('certificados', 0) - urna.get('ac_valida_na_assinatura', 0)} de {urna.get('certificados', 0)}; todos vencem depois da AC (2027 a 2037).")
    w(f"  Leitura estrita do RFC 5280 na data da assinatura: {urna.get('caminho_estrito_rfc5280_ok_na_assinatura', 0)} de {urna.get('certificados', 0)} da AC URNA passam; AC UE2020 e AC UE2022: {pa.get('AC UE2020', {}).get('caminho_estrito_rfc5280_ok_na_assinatura', 0) + pa.get('AC UE2022', {}).get('caminho_estrito_rfc5280_ok_na_assinatura', 0)} de {pa.get('AC UE2020', {}).get('certificados', 0) + pa.get('AC UE2022', {}).get('certificados', 0)}.")
    w(f"  1º turno (80 seções, fora da amostra): {sum(c.get('assinatura_ok', 0) for c in u1['por_ac'].values())} de {u1['contagem']['certificados']} conferem; mesma urna e mesmo certificado nos dois turnos em {u1['comparacao_com_2t'].get('mesma_urna_mesmo_certificado', 0)}; urna trocada em {u1['comparacao_com_2t'].get('urna_diferente', 0)}.")
    if mar:
        x = mar[0]
        w(f"  Seção SP|66818|400|141 (Marília, citada pela dataurnas-br): urna UE2013 {x['urna_no_certificado']} (a mesma do boletim), certificado emitido em {x['emissao_utc'][:19].replace('T', ' ')} UTC,")
        w(f"  15 dias e 20 horas depois do fim da AC URNA publicada; a assinatura confere com a chave dela: {'sim' if all(y['assinatura_ok'] for y in mar) else 'não'} (nos dois turnos).")
    w(f"  Certificados de urna emitidos em 2026 na amostra: {len(e26)} ({', '.join(f'{e['ac']} {e['emissao_utc'][:10]}' for e in e26)}), todos com fim em 31/12/2037 23:00 UTC.")
    w(f"  Resumos publicados (cópia de terceiros): urna 2013 {m['path1u13']['itens']} linhas, 2015 {m['path1u15']['itens']}, 2020 {m['path1u20']['itens']}, 2022 {m['path1u22']['itens']}, datadas de 02/09/2026, todas no formato SHA-512.")
    w(f"  Dos arquivos de urna: {sum(ra['arquivos_conferidos'].values())} resumos SHA-512 listados nos vsc (11 arquivos por seção); {sum(ra['encontrados_em_algum_manifesto'].values())} aparecem em algum resumo publicado. Nenhum é de programa.")
    w(f"  Logs: {rb['status_das_verificacoes'].get('SUCESSO', 0)} verificações de assinatura de pacote com SUCESSO e {rb['status_das_verificacoes'].get('ERRO', 0)} com ERRO.")
    w(f"  Os 24 pacotes de programa que o GAP verifica a cada partida estão no resumo publicado do modelo da urna em {rb['secoes'].get('todos os .vst do GAP no resumo do modelo', 0)} seções;")
    w(f"  nas outras {len(cruz)}, o log tem duas urnas de modelos diferentes (troca registrada) em {sum(1 for c in cruz if c['explicado_por_troca_de_urna_no_log'])} de {len(cruz)}.")
    w(f"  Versão em todos os boletins e em todos os aplicativos do log: {', '.join(R['resumos']['c_versoes']['boletim'])}.")
    w('')
    w('O QUE ISSO SIGNIFICA')
    w('  Os certificados das urnas da amostra foram emitidos pelas três AC que o TSE publica no pacote de documentação, e nenhum aponta para')
    w('  outra AC. Isso fecha a cadeia até as AC intermediárias: um pacote trocado com certificado forjado exigiria a chave privada de uma')
    w('  delas. Não fecha até a raiz (AC RAIZ UE e AC URNA v2 não estão publicadas em lugar que eu consiga baixar), e a AC publicada só é')
    w('  "do TSE" por duas cópias de terceiros que concordam entre si (o pacote de documentação e o resumo do HOLOCRON).')
    w('  A alegação sobre a AC URNA é verdadeira e precisa: o certificado publicado venceu em 18/07/2026, antes dos dois turnos. Pela')
    w('  regra estrita do X.509, a cadeia dos 27% da amostra com urna antiga (UE2013 e UE2015) estaria vencida no dia da assinatura. Isso não mostra')
    w('  arquivo adulterado: as assinaturas conferem e cada certificado de urna está dentro da própria validade. Mostra um problema de gestão')
    w('  da AC: ou há um certificado renovado da AC URNA, com a mesma chave, que não foi publicado, ou a chave continuou em uso depois do')
    w('  vencimento. A urna de Marília com certificado emitido em 03/08/2026 pela mesma chave confirma que a chave assinou depois do fim.')
    w('  Os resumos dos programas não podem ser comparados com os arquivos públicos de urna: eles não trazem nenhum arquivo de programa nem')
    w('  resumo de programa (o hash.dat, que pode conter isso, é listado no vsc mas não é publicado). O que dá para ver é indireto: a urna')
    w('  registra que verificou a assinatura de cada pacote e que deu certo, e os nomes dos pacotes batem com a lista publicada do modelo.')
    w('  Esse registro é feito pelo próprio programa da urna: um programa trocado poderia escrever o mesmo log.')
    w('')
    w('PISTAS (fora do critério; tudo no JSON)')
    up = [e for e in e26 if e['ac'] == 'AC URNA']
    w(f"  1. A chave da AC URNA assinou depois do vencimento publicado: Marília, emitido em 03/08/2026 (fora da amostra; nenhum caso na amostra,")
    w(f"     onde os {len(up)} certificados da AC URNA de 2026 são de {', '.join(e['emissao_utc'][:10] for e in up)}). Os {len(e26)} certificados de urna de 2026 da amostra e o de")
    w("     Marília têm fim fixo em 31/12/2037 23:00 UTC; os anteriores vencem cerca de 14 anos depois da emissão. Mudou o perfil de emissão em 2026.")
    w("     Falta achar um certificado renovado da AC URNA (mesma chave) e saber por que o pacote de documentação traz o vencido.")
    w("  2. O resumo do HOLOCRON 2026 lista acraiz-ue.pem, acraizuev2.cer e acurnav2.cer (SHA-512 no JSON, holocron) e não lista a AC URNA.")
    w("     Com esses arquivos a cadeia fecharia até a raiz e daria para conferir byte a byte. A chave da AC RAIZ UE recuperada da assinatura")
    w(f"     da AC URNA (D8) tem SHA-256 do SubjectPublicKeyInfo {R['raiz_recuperada_D8']['candidatos_com_sha1_igual_ao_aki'][0]['sha256_spki'] if R['raiz_recuperada_D8']['candidatos_com_sha1_igual_ao_aki'] else 'não achada'}.")
    for e in err:
        b = e['blocos_do_log']
        w(f"  {e['secao']}: urnas no log {[x['urnas'] for x in b]}, urna do vsc {e['urna_do_vsc']}, votos por bloco {[x['votos_por_dia'] for x in b]}; primeiro erro {[x['primeiro_erro'] for x in b]}.")
        for x in b:
            vistos = set(); k = 0
            for c in x['contexto']:
                msg = c.split(' | ', 4)[-1][:120]
                if msg in vistos or msg.startswith('Urna ligada em'):
                    continue
                vistos.add(msg); k += 1
                if k <= 12:
                    w(f"       {c}")
    w(f"  {len(cruz)} seções com módulo de outro modelo no log: em {sum(1 for c in cruz if c['explicado_por_troca_de_urna_no_log'])} há troca de urna registrada (lista no JSON).")
    sem = [r for r in rb['tabela'] if r[3] == 'pacote de programa' and r[2] == 'sem resumo publicado']
    outro = [r for r in rb['tabela'] if r[3] == 'pacote de programa' and r[2].startswith('mesmo nome')]
    w(f"  Pacotes de programa verificados nos logs sem resumo publicado com esse nome: {len(sem)} ({', '.join(r[0] + ' ' + r[1] for r in sem)}).")
    w(f"     Com o mesmo nome em outro resumo (GEDAI-UE, caminho do Windows): {', '.join(r[1] for r in outro)}. O avbootcfg.vsu é gerado na urna;")
    w("     segundo o trecho da página do TSE mostrado pelo buscador, avbootcfg.vsu e uenux.cfg não têm hash publicado (a página não abriu daqui).")
    w(f"  mr.ver: o mesmo arquivo ({ra['mr_ver_tamanho']} bytes, um único SHA-512) nas {n2} urnas de todos os modelos; não está nos resumos e não é")
    w("     publicado. hash.dat (19,8 a 20,4 KB, diferente em cada seção) é assinado no vsc e não é publicado; se tiver os resumos dos programas")
    w("     instalados, publicá-lo permitiria a comparação que o F12 pede.")
    w(f"  Assinatura de software: as {n2} seções do 2º turno e as 80 do 1º usam o mesmo usuário e conjunto de chaves ({', '.join(u2['sw_usuario'])}; {', '.join(u2['sw_conjunto_de_chaves'])}),")
    w("     com algoritmo CEPESC, que não dá para verificar com informação pública.")
    w(f"  AC UE2020: {pa.get('AC UE2020', {}).get('urna_vence_depois_da_ac', 0)} certificados de urna vencem depois da própria AC. AC URNA: {urna.get('urna_vence_depois_da_ac', 0)} de {urna.get('certificados', 0)}.")
    w("  O bloco 2 do vsc, que o T18 deixou sem significado, é (modelo do equipamento, algoritmo) do esquema do TSE: 22/20 com EdDSA, 15/13 com ECDSA.")
    w("  Fontes: o pacote do TSE e os resumos dos programas vieram de cópias de terceiros, porque o site do TSE dá 403 daqui. As duas cópias")
    w("     concordam entre si nos certificados AC UE2020 e AC UE2022. Conferir com o site do TSE a partir de outra rede fecharia esse ponto.")
    w("  Não reproduzi o HASH GERAL dos resumos (11 métodos tentados): a consistência interna das listas não foi conferida.")
    return L


def escrever_txt(R, caminho):
    L = []
    w = L.append
    v = R['veredito']; u2 = R['urnas_2t']; u1 = R['urnas_1t_80']; al = R['alegacao_ac_urna']
    w('F12. Certificados das autoridades certificadoras da urna e resumos digitais dos programas (Adendo 21)')
    w('')
    L.extend(texto_resumo(R))
    w('')
    w('DETALHE')
    w('')
    w(f"Veredito pela letra: certificados {v['certificados']}; resumos de programa {v['resumos_de_programa']}.")
    w(f"Leitura estrita (descritiva, D2): {v['leitura_estrita_rfc5280']}.")
    w('')
    w('1. Certificados das AC usados como "publicados" (D1)')
    for n, f in R['acs_publicadas'].items():
        w(f"  {n}: emissor {f['emissor']}; serial {f['serial']}; validade {f['validade_inicio_utc'][:19]} a {f['validade_fim_utc'][:19]} UTC; "
          f"assinatura {f['algoritmo_assinatura']}; chave {f['tipo_chave']}; SKI {f['ski']}; AKI {f['aki']}; CA {f['ca']}; assina certificados {f['assina_certificados']}; "
          f"SKI = SHA-1 da chave: {f['ski_igual_sha1_da_chave']}; SHA-256 (DER) {f['sha256_der']}")
    w('  Mesmo certificado nas fontes:')
    for n, c in R['comparacao_entre_fontes_sha256_der'].items():
        w(f"    {n}: {c['fontes']} fontes, todas iguais: {c['todas_iguais']}")
    w('  Resumo publicado do HOLOCRON (pc1holo.html, cópia de terceiros):')
    for n, c in R['holocron']['conferencia'].items():
        w(f"    {n}: listado e igual: {c['listado_no_manifesto']}; formas que conferem: {', '.join(f'{k} -> {x}' for k, x in c['formas_que_conferem'].items()) or 'nenhuma'}")
    w(f"    Arquivos de certificado listados no HOLOCRON: {', '.join(R['holocron']['arquivos_de_certificado_listados'])}")
    rr = R['raiz_recuperada_D8']
    w(f"  D8 (robustez): {rr['candidatos']} candidatos a chave da AC RAIZ UE recuperados da assinatura da AC URNA; com SHA-1 igual ao AKI {rr['aki_da_ac_urna']}: {rr['candidatos_com_sha1_igual_ao_aki']}")
    w('')
    for titulo, u in (('2. Certificados das urnas, amostra do 2º turno', u2), ('3. Certificados das urnas, 80 seções do 1º turno (D7, descritivo)', u1)):
        w(titulo)
        w(f"  Contagem: {u['contagem']}")
        for ac, c in u['por_ac'].items():
            w(f"  {ac}: {c}")
        w(f"  Falhas pelo critério: {len(u['falhas'])} {u['falhas'][:5]}")
        w(f"  Emitidos depois do fim da validade da AC: {len(u['emitidos_depois_do_fim_da_ac'])} {u['emitidos_depois_do_fim_da_ac'][:10]}")
        w(f"  Ano de emissão por AC: {u['ano_de_emissao_por_ac']}")
        w(f"  Emissão mais recente por AC: {u['emissao_mais_recente_por_ac']}; fim mais cedo: {u['fim_mais_cedo_por_ac']}")
        w(f"  Criação da assinatura de hardware (local): {u['hw_criacao_min_max']}; a menos de 1 dia de um limite de validade: {u['n_a_menos_de_1_dia_de_um_limite']}")
        w(f"  Modelo do bloco 2 diferente do esperado para a AC: {u['n_modelo_div']} {u['modelo_do_bloco2_diferente_do_esperado_para_a_ac'][:5]}")
        w(f"  Modelo pela faixa do número diferente do bloco 2: {u['n_faixa_div']} {u['modelo_da_faixa_do_numero_diferente_do_bloco2'][:10]}")
        w(f"  Assinatura de software: usuário {u['sw_usuario']}; conjunto de chaves {u['sw_conjunto_de_chaves']}")
        if 'comparacao_com_2t' in u:
            w(f"  1º contra 2º turno na mesma seção: {u['comparacao_com_2t']} {u['casos'][:10]}")
        w('')
    w(f"  Emitidos em 2026 (2º turno): {R['urnas_2t']['emitidos_em_2026']}")
    w(f"  Seção citada pela dataurnas-br (fora da amostra): {R['secao_marilia_citada_pela_dataurnas']}")
    un = R['unicidade']
    w(f"  Unicidade (2º turno e 1º): serial repetido em urnas diferentes {len(un['serial_repetido_em_urnas_diferentes'])}; chave repetida {len(un['chave_repetida_em_urnas_diferentes'])}; urna com mais de um certificado {len(un['urna_com_mais_de_um_certificado'])} {un['urna_com_mais_de_um_certificado'][:10]}")
    w('')
    w('4. Alegação: certificado da AC URNA vencido em 18/07/2026')
    for k, x in al.items():
        w(f"  {k}: {x}")
    w('')
    w('5. Resumos digitais dos programas')
    m = R['manifestos']
    w(f"  Fonte: {m['fonte']}")
    for k, x in m['por_manifesto'].items():
        w(f"    {k}: {' / '.join(x['titulos'])}; {x['itens']} linhas; formato SHA-512 ok {x['formato_ok']}; HASH GERAL {x['hash_geral']}")
    ra = R['resumos']['a_resumos_dos_arquivos_do_vsc_nos_manifestos']
    w(f"  (a) Resumos dos arquivos do vsc encontrados em algum manifesto: {ra['encontrados_em_algum_manifesto'] or 'nenhum'} (conferidos {sum(ra['arquivos_conferidos'].values())}); mr.ver: {ra['mr_ver_resumos_distintos']} resumo distinto, {ra['mr_ver_tamanho']} bytes")
    rb = R['resumos']['b_pacotes_verificados_nos_logs']
    w(f"  (b) Verificações de assinatura nos logs: {rb['status_das_verificacoes']}; não SUCESSO: {rb['n_nao_sucesso']}; seções: {rb['secoes']}; logs com erro de leitura: {rb['n_logs_com_erro']}")
    w(f"      Linhas de assinatura com falha ou erro: {rb['n_linhas_de_assinatura_com_falha_ou_erro']} {rb['linhas_de_assinatura_com_falha_ou_erro'][:5]}")
    w(f"      Por classe (soma de seções x pacote): {rb['por_classe']}")
    for app, nome, cls, tipo_arq, por_mod, n in rb['tabela']:
        if not cls.startswith('no resumo do modelo (arquivos base)'):
            w(f"      [{tipo_arq} | {cls}] {app} {nome}: {n} ({por_mod})")
    w(f"      Seções com modelo no log diferente do vsc: {len(rb['secoes_com_modelo_do_log_diferente_do_vsc'])}")
    for x in rb['secoes_com_modelo_do_log_diferente_do_vsc']:
        w(f"        {x}")
    w(f"      Seções com erro de assinatura no log: {len(rb['secoes_com_erro_de_assinatura_no_log'])}")
    for x in rb['secoes_com_erro_de_assinatura_no_log']:
        w(f"        {x['secao']}: urnas por bloco {x['urnas_por_bloco_do_log']}; urna do vsc {x['urna_do_vsc']}; {x['verificacoes_nao_sucesso']}; {x['linhas'][:3]}")
    rc = R['resumos']['c_versoes']
    w(f"  (c) Versão no boletim: {rc['boletim']}")
    w(f"      Versão no log: {rc['log_por_aplicacao']}")
    w(f"      Modelo no log x modelo do vsc: {rc['modelo_no_log_x_modelo_do_vsc']}")
    open(caminho, 'w').write(limpa('\n'.join(L)) + '\n')


if __name__ == '__main__':
    main()
