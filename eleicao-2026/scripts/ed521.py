"""Verificação de assinatura EdDSA sobre a curva E-521 (Ed521), usada pelas urnas UE2020 e UE2022.

Curva: x^2 + y^2 = 1 - 376014 x^2 y^2 sobre p = 2^521 - 1 (Aranha, Barreto, Pereira e Ricardini, 2013); ponto base
com y = 12 e x par; ordem L = 2^519 - 337554763258501705789107630418782636071904961214051226618635150085779108655765.
Codificação: 66 bytes little-endian de y, com o bit 527 igual à paridade de x. Assinatura: R (66 bytes) || S (66 bytes).
k = SHAKE256("SigEd521" || 0x00 || 0x00 || R || A || M, 132 bytes) mod L, como o Ed448 com contexto vazio.
Variante identificada por tentativa sobre os arquivos da urna (o identificador do certificado é 1.3.6.1.4.1.44588.2.1):
a mensagem assinada é o SHA-512 do resumo SHA-512 listado. Uma variante errada não verifica nenhuma assinatura.
Implementação simples, sem cuidado com tempo constante: serve só para verificar, nunca para assinar.
"""
import hashlib

P = 2 ** 521 - 1
D = (-376014) % P
L = 2 ** 519 - 337554763258501705789107630418782636071904961214051226618635150085779108655765
DOM = b'SigEd521\x00\x00'


def _sqrt(u):
    r = pow(u, (P + 1) // 4, P)
    return r if r * r % P == u % P else None


def _recx(y, sinal):
    x = _sqrt((y * y - 1) * pow(D * y * y - 1, P - 2, P) % P)
    if x is None:
        return None
    return P - x if x & 1 != sinal else x


def _soma(a, b):
    (x1, y1, z1, t1), (x2, y2, z2, t2) = a, b
    A = x1 * x2 % P; B = y1 * y2 % P; C = D * t1 * t2 % P; DD = z1 * z2 % P
    E = ((x1 + y1) * (x2 + y2) - A - B) % P; F = (DD - C) % P; G = (DD + C) % P; H = (B - A) % P
    return (E * F % P, G * H % P, F * G % P, E * H % P)


def _mult(k, pt):
    r = (0, 1, 1, 0)
    while k:
        if k & 1:
            r = _soma(r, pt)
        pt = _soma(pt, pt); k >>= 1
    return r


def _afim(pt):
    x, y, z, _ = pt
    zi = pow(z, P - 2, P)
    return x * zi % P, y * zi % P


def _decod(b):
    if len(b) != 66:
        return None
    v = int.from_bytes(b, 'little'); y = v & ((1 << 521) - 1)
    if y >= P:
        return None
    x = _recx(y, (v >> 527) & 1)
    return None if x is None else (x, y, 1, x * y % P)


_GX = _recx(12, 0)
BASE = (_GX, 12, 1, _GX * 12 % P)


def verificar(chave, assinatura, mensagem):
    A = _decod(chave); R = _decod(assinatura[:66]); S = int.from_bytes(assinatura[66:], 'little')
    if len(assinatura) != 132 or A is None or R is None or S >= L:
        return False
    k = int.from_bytes(hashlib.shake_256(DOM + assinatura[:66] + chave + mensagem).digest(132), 'little') % L
    return _afim(_mult(4 * S, BASE)) == _afim(_soma(_mult(4, R), _mult(4 * k, A)))


def verificar_resumo(chave, assinatura, resumo_sha512):
    """Forma usada nos arquivos da urna: a mensagem é o SHA-512 do resumo SHA-512 do arquivo."""
    return verificar(chave, assinatura, hashlib.sha512(resumo_sha512).digest())
