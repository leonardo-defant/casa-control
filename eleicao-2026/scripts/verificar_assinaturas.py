"""T18 do pré-registro (adendo 9): assinatura digital dos arquivos de cada seção (-vota.vsc).

Estrutura lida do BER (sem esquema publicado à mão): três blocos.
  Bloco 0: assinatura de software. Cabeçalho com identificador de chave (ex.: SEVIN 20260708) e, para cada arquivo,
           tamanho, SHA-512 e uma assinatura de 4.765 bytes em formato próprio. A chave pública não vem no pacote:
           aqui só se confere o resumo.
  Bloco 1: assinatura de hardware da urna. Para cada arquivo, tamanho, SHA-512 e assinatura ECDSA (DER); o bloco
           inteiro também é assinado. O certificado X.509 da urna (emissor AC URNA, TSE) vem no pacote.
  Bloco 2: dois enumerados de significado não documentado.
Bloco 1 das urnas UE2013 e UE2015: ECDSA P-521; das UE2020 e UE2022: Ed521 (ver ed521.py). Nos dois casos o valor
assinado é o SHA-512 do resumo SHA-512 listado.
Para cada seção: resumo e tamanho de cada arquivo baixado contra os dois blocos; assinatura de cada arquivo e do
bloco com a chave do certificado; número da urna no certificado contra o do boletim; emissor e identificador da AC.
Uso: python3 -I verificar_assinaturas.py <pasta_arq_2t>
"""
import os as _os, sys as _sys
_sys.path.insert(0, _os.path.dirname(_os.path.abspath(__file__)))
import collections, hashlib, json, os, sys
from cryptography import x509
from cryptography.exceptions import InvalidSignature, UnsupportedAlgorithm
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.asymmetric import ec, utils
from ber import parse, read_tlv
from decodificar import ler_bu
import ed521

ALG = {256: hashes.SHA256, 384: hashes.SHA384, 512: hashes.SHA512}


def entradas(octet):
    out = {}
    for e in parse(octet)[0][2][0][2]:  # SEQ { SEQ OF entrada }
        nm = e[2][0][2].decode('latin1'); s = e[2][1][2]
        out[nm] = {'tam': int.from_bytes(s[0][2], 'big'), 'sha512': s[1][2], 'ass': s[2][2]}
    return out


def ler_vsc(caminho):
    top = parse(open(caminho, 'rb').read())[0][2]
    b0, b1 = top[0][2], top[1][2]
    cab0 = b0[2][2]; cab1 = b1[2][2]
    return {'sw_chave': (cab0[0][2][0][2].decode('latin1'), int.from_bytes(cab0[0][2][1][2], 'big')),
            'sw_entradas': entradas(b0[3][2]), 'sw_conteudo': b0[3][2],
            'sw_cab': {'tam': int.from_bytes(cab0[3][2][0][2], 'big'), 'sha512': cab0[3][2][1][2]},
            'hw_titular': cab1[0][2][0][2].decode('latin1'), 'hw_entradas': entradas(b1[3][2]), 'hw_conteudo': b1[3][2],
            'hw_cab': {'tam': int.from_bytes(cab1[3][2][0][2], 'big'), 'sha512': cab1[3][2][1][2], 'ass': cab1[3][2][2][2]},
            'hw_cert': b1[4][2], 'bloco2': [x[2].hex() for x in top[2][2]] if len(top) > 2 else None}


def verifica_ecdsa(pub, ass, resumo):
    """ECDSA com SHA-512 sobre o arquivo equivale a verificar o resumo SHA-512 já calculado (modo 'resumo').
    Se falhar, tenta a assinatura sobre o próprio resumo tratado como dado ('resumo_como_dado')."""
    try:
        pub.verify(ass, resumo, ec.ECDSA(utils.Prehashed(hashes.SHA512()))); return 'resumo'
    except InvalidSignature:
        pass
    try:
        pub.verify(ass, resumo, ec.ECDSA(hashes.SHA512())); return 'resumo_como_dado'
    except InvalidSignature:
        return None


def chave_bruta(cert):
    """Bytes da chave pública (BIT STRING do SubjectPublicKeyInfo), para algoritmos que a biblioteca não conhece."""
    from cryptography.hazmat.primitives.serialization import Encoding
    tbs = parse(cert.public_bytes(Encoding.DER))[0][2][0][2]
    for n in tbs:
        f = n[2] if isinstance(n[2], list) else []
        if len(f) == 2 and (f[0][0], f[0][1]) == (0, 16) and (f[1][0], f[1][1]) == (0, 3):
            return f[1][2][1:]
    return None


def verifica_ass(pub, chave_ed, ass, resumo):
    if pub is not None:
        return verifica_ecdsa(pub, ass, resumo)
    if chave_ed is not None and ed521.verificar_resumo(chave_ed, ass, resumo):
        return 'ed521_resumo'
    return None


def secoes(pasta):
    for uf in sorted(os.listdir(pasta)):
        for m in sorted(os.listdir(os.path.join(pasta, uf))):
            for z in sorted(os.listdir(os.path.join(pasta, uf, m))):
                for s in sorted(os.listdir(os.path.join(pasta, uf, m, z))):
                    yield f'{uf.upper()}|{int(m)}|{int(z)}|{int(s)}', os.path.join(pasta, uf, m, z, s)


def main():
    pasta = sys.argv[1]
    cont = collections.Counter(); falhas = []; emissores = collections.Counter(); akis = collections.Counter()
    chaves_sw = collections.Counter(); extras = collections.Counter(); tipos_chave = collections.Counter(); modo = collections.Counter(); bloco2 = collections.Counter(); validade = []
    for k, p in secoes(pasta):
        fs = os.listdir(p)
        vs = sorted(f for f in fs if f.endswith('-vota.vsc'))
        if not vs:
            continue
        cont['secoes_com_vsc'] += 1
        pre = vs[-1].split('-o')[0] + '-'  # índice do hash no aux, para casar os arquivos do mesmo pacote
        try:
            v = ler_vsc(os.path.join(p, vs[-1]))
        except Exception as e:
            falhas.append((k, 'vsc ilegivel', str(e))); continue
        cb = v['hw_cert']  # em parte das urnas o certificado vem em PEM, nas outras em DER
        if cb.startswith(b'-----'):
            cert = x509.load_pem_x509_certificate(cb)
        else:
            fim = read_tlv(cb, 0)[4]  # alguns DER vêm com bytes a mais depois do certificado
            if fim < len(cb):
                cont['cert_der_com_bytes_extras'] += 1; extras[cb[fim:].hex()[:16]] += 1
            cert = x509.load_der_x509_certificate(cb[:fim])
        cont['cert_pem' if cb.startswith(b'-----') else 'cert_der'] += 1
        chave_ed = None
        try:
            pub = cert.public_key()
        except UnsupportedAlgorithm:
            # urnas UE2020 e UE2022: identificador 1.3.6.1.4.1.44588.2.1 (Ed521), chave de 66 bytes
            pub = None; chave_ed = chave_bruta(cert)
        tipos_chave[cert.signature_algorithm_oid.dotted_string if pub is None else type(pub).__name__] += 1
        emissores[cert.issuer.rfc4514_string()] += 1
        try:
            akis[cert.extensions.get_extension_for_class(x509.AuthorityKeyIdentifier).value.key_identifier.hex()] += 1
        except Exception:
            akis['sem'] += 1
        validade.append((cert.not_valid_before_utc.isoformat()[:10], cert.not_valid_after_utc.isoformat()[:10]))
        chaves_sw[v['sw_chave']] += 1; bloco2[str(v['bloco2'])] += 1
        cn = cert.subject.get_attributes_for_oid(x509.NameOID.COMMON_NAME)[0].value
        if cn.lower() != v['hw_titular'].lower():
            if v['hw_titular'].upper() == 'UEAO':  # urnas novas gravam só o prefixo no cabeçalho
                cont['titular_so_prefixo'] += 1
            else:
                falhas.append((k, 'titular do bloco diferente do certificado', cn, v['hw_titular']))
        # bloco inteiro
        if hashlib.sha512(v['hw_conteudo']).digest() != v['hw_cab']['sha512'] or len(v['hw_conteudo']) != v['hw_cab']['tam']:
            falhas.append((k, 'resumo do bloco de hardware'))
        mb = verifica_ass(pub, chave_ed, v['hw_cab']['ass'], hashlib.sha512(v['hw_conteudo']).digest())
        cont['bloco_hw_assinatura_ok' if mb else 'bloco_hw_assinatura_FALHA'] += 1
        if not mb: falhas.append((k, 'assinatura do bloco de hardware'))
        else: modo['bloco:' + mb] += 1
        if hashlib.sha512(v['sw_conteudo']).digest() != v['sw_cab']['sha512'] or len(v['sw_conteudo']) != v['sw_cab']['tam']:
            falhas.append((k, 'resumo do bloco de software'))
        # cada arquivo assinado: ECDSA de todos; resumo dos que foram baixados
        for nm, e in v['hw_entradas'].items():
            cont['arquivos_listados'] += 1
            s0 = v['sw_entradas'].get(nm)
            if s0 is None or s0['sha512'] != e['sha512'] or s0['tam'] != e['tam']:
                falhas.append((k, 'blocos 0 e 1 discordam', nm))
            local = os.path.join(p, pre + nm)
            if os.path.exists(local):
                dados = open(local, 'rb').read()
                cont['arquivos_baixados_conferidos'] += 1
                if hashlib.sha512(dados).digest() != e['sha512'] or len(dados) != e['tam']:
                    falhas.append((k, 'resumo do arquivo baixado diferente', nm)); cont['resumo_FALHA'] += 1
                else:
                    cont['resumo_ok'] += 1
            # a assinatura é conferida contra o resumo listado; o resumo, contra o arquivo baixado (acima)
            m = verifica_ass(pub, chave_ed, e['ass'], e['sha512'])
            if m: cont['assinatura_arquivo_ok'] += 1; modo['arquivo:' + m] += 1
            else: cont['assinatura_arquivo_FALHA'] += 1; falhas.append((k, 'assinatura do arquivo', nm, os.path.exists(local)))
        # número da urna
        bus = sorted(f for f in fs if f.endswith('-bu.dat') and f.startswith(pre))
        if bus:
            serie = ler_bu(os.path.join(p, bus[-1]))['urna']
            n_cert = int(cn[4:]) if cn.lower().startswith('ueao') and cn[4:].isdigit() else None
            if n_cert != serie:
                falhas.append((k, 'numero da urna no certificado diferente do boletim', cn, serie))
                cont['urna_cert_diferente_bu'] += 1
            else:
                cont['urna_cert_igual_bu'] += 1
    out = {'contagem': dict(cont), 'falhas': falhas, 'emissores': dict(emissores), 'identificador_da_ac': dict(akis),
           'chaves_software': {f'{a} {b}': c for (a, b), c in chaves_sw.items()}, 'modo_da_assinatura': dict(modo), 'tipos_de_chave': dict(tipos_chave), 'bytes_extras_no_der': dict(extras),
           'bloco2': dict(bloco2), 'validade_certificados': {f'{a} a {b}': c for (a, b), c in collections.Counter(validade).most_common(10)},
           'cadeia_ate_a_raiz': 'nao verificada: os certificados das AC (AC URNA, AC UE2020, AC UE2022) nao vem no pacote',
           'assinatura_de_software': 'nao verificada: formato proprio (4.765 bytes, cabecalho 24.01.03) e chave SEVIN fora do pacote; so o resumo foi conferido'}
    print(json.dumps(out, ensure_ascii=False, indent=1, default=str))


if __name__ == '__main__':
    main()
