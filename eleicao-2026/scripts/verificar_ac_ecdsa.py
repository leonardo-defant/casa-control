"""Robustez do T18, fora do pré-registro: os certificados das urnas UE2013 e UE2015 foram assinados pela mesma chave de AC?

O certificado da AC URNA não vem no pacote, e os endereços de lista de revogação e de política citados nos próprios
certificados devolvem 403 a partir deste ambiente. Como a assinatura dos certificados é ECDSA P-521 com SHA-512, a
chave pública de quem assinou pode ser recuperada de cada assinatura (dois ou quatro candidatos por certificado):
Q = r^-1 (s R - e G), com R um dos pontos de abscissa r. A chave comum a dois certificados é a da AC; depois, todos
os certificados são verificados com ela pela biblioteca cryptography.
Isso mostra que um único detentor de chave assinou todos os certificados do pacote. Não liga essa chave ao TSE:
só o certificado da AC publicado pelo TSE faz isso.
Uso: python3 -I verificar_ac_ecdsa.py <pasta_arq_2t>
"""
import os as _os, sys as _sys
_sys.path.insert(0, _os.path.dirname(_os.path.abspath(__file__)))
import collections, glob, hashlib, json, sys
from cryptography import x509
from cryptography.exceptions import InvalidSignature
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.asymmetric import ec
from cryptography.hazmat.primitives.asymmetric.utils import decode_dss_signature
from ber import read_tlv
from verificar_assinaturas import ler_vsc

P = 2 ** 521 - 1
A = P - 3
B = 0x0051953eb9618e1c9a1f929a21a0b68540eea2da725b99b315f3b8b489918ef109e156193951ec7e937b1652c0bd3bb1bf073573df883d2c34f1ef451fd46b503f00
N = 0x01fffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffa51868783bf2f966b7fcc0148f709a5d03bb5c9b8899c47aebb6fb71e91386409
G = (0x00c6858e06b70404e9cd9e3ecb662395b4429c648139053fb521f828af606b4d3dbaa14b5e77efe75928fe1dc127a2ffa8de3348b3c1856a429bf97e7e31c2e5bd66,
     0x011839296a789a3bc0045c8a5fb42c7d1bd998f54449579b446817afbd17273e662c97ee72995ef42640c550b9013fad0761353c7086a272c24088be94769fd16650)


def soma(p1, p2):
    if p1 is None: return p2
    if p2 is None: return p1
    (x1, y1), (x2, y2) = p1, p2
    if x1 == x2 and (y1 + y2) % P == 0:
        return None
    if p1 == p2:
        l = (3 * x1 * x1 + A) * pow(2 * y1, P - 2, P) % P
    else:
        l = (y2 - y1) * pow(x2 - x1, P - 2, P) % P
    x3 = (l * l - x1 - x2) % P
    return x3, (l * (x1 - x3) - y1) % P


def mult(k, pt):
    r = None
    while k:
        if k & 1: r = soma(r, pt)
        pt = soma(pt, pt); k >>= 1
    return r


def candidatos(cert):
    r, s = decode_dss_signature(cert.signature)
    e = int.from_bytes(hashlib.sha512(cert.tbs_certificate_bytes).digest(), 'big')  # 512 bits < 521: sem truncar
    out = []
    for x in (r, r + N):
        if x >= P: continue
        y2 = (pow(x, 3, P) + A * x + B) % P
        y = pow(y2, (P + 1) // 4, P)
        if y * y % P != y2: continue
        for yy in (y, P - y):
            Rp = (x, yy)
            Q = mult(pow(r, -1, N), soma(mult(s, Rp), mult((-e) % N, G)))
            if Q: out.append(Q)
    return out


def main():
    pasta = sys.argv[1]
    # parâmetros da curva conferidos contra a biblioteca
    gpub = ec.derive_private_key(1, ec.SECP521R1()).public_key().public_numbers()
    assert (gpub.x, gpub.y) == G, 'ponto base diferente do da biblioteca'
    certs = []
    for f in sorted(glob.glob(os.path.join(pasta, '*/*/*/*/*-vota.vsc'))):
        cb = ler_vsc(f)['hw_cert']
        if cb.startswith(b'-----'):
            continue
        c = x509.load_der_x509_certificate(cb[:read_tlv(cb, 0)[4]])
        certs.append((f, c))
    algs = collections.Counter(c.signature_algorithm_oid.dotted_string for _, c in certs)
    c0 = set(candidatos(certs[0][1])); c1 = set(candidatos(certs[1][1]))
    comum = c0 & c1
    out = {'certificados_ecdsa': len(certs), 'algoritmo_da_assinatura': dict(algs), 'candidatos_comuns': len(comum)}
    if len(comum) == 1:
        Q = comum.pop()
        pub = ec.EllipticCurvePublicNumbers(Q[0], Q[1], ec.SECP521R1()).public_key()
        ok = 0; ruins = []
        for f, c in certs:
            try:
                pub.verify(c.signature, c.tbs_certificate_bytes, ec.ECDSA(hashes.SHA512())); ok += 1
            except InvalidSignature:
                ruins.append(f)
        from cryptography.hazmat.primitives.serialization import Encoding, PublicFormat
        spki = pub.public_bytes(Encoding.DER, PublicFormat.SubjectPublicKeyInfo)
        ski_sha1 = hashlib.sha1(pub.public_bytes(Encoding.X962, PublicFormat.UncompressedPoint)).hexdigest()
        akis = collections.Counter(c.extensions.get_extension_for_class(x509.AuthorityKeyIdentifier).value.key_identifier.hex() for _, c in certs)
        out.update({'certificados_verificados_com_a_chave_recuperada': ok, 'falhas': ruins,
                    'sha256_da_chave_da_ac': hashlib.sha256(spki).hexdigest(),
                    'sha1_do_ponto_da_chave (convencao usual do identificador de chave)': ski_sha1,
                    'identificador_da_ac_nos_certificados': dict(akis),
                    'identificador_bate_com_a_chave': ski_sha1 in akis})
    print(json.dumps(out, ensure_ascii=False, indent=1))


if __name__ == '__main__':
    import os
    main()
