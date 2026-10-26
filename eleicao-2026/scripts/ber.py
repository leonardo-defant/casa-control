"""Decodificador BER genérico (sem esquema) para os arquivos de urna do TSE."""
import sys

def read_tlv(b, i):
    t0 = b[i]; i += 1
    cls = t0 >> 6; cons = (t0 >> 5) & 1; tag = t0 & 0x1f
    if tag == 0x1f:
        tag = 0
        while True:
            x = b[i]; i += 1
            tag = (tag << 7) | (x & 0x7f)
            if not x & 0x80: break
    l0 = b[i]; i += 1
    if l0 & 0x80:
        n = l0 & 0x7f
        if n == 0:
            raise ValueError('comprimento indefinido nao suportado')
        ln = int.from_bytes(b[i:i+n], 'big'); i += n
    else:
        ln = l0
    return cls, cons, tag, i, i + ln

def parse(b, i=0, end=None):
    end = len(b) if end is None else end
    out = []
    while i < end:
        cls, cons, tag, s, e = read_tlv(b, i)
        if cons:
            out.append((cls, tag, parse(b, s, e)))
        else:
            out.append((cls, tag, b[s:e]))
        i = e
    return out

def try_inner(v):
    """OCTET STRING que contém BER aninhado (envelope)."""
    try:
        p = parse(v)
        if p and sum(1 for _ in p) >= 1:
            return p
    except Exception:
        return None
    return None

def show(node, depth=0, maxbytes=40):
    for cls, tag, v in node:
        pre = '  ' * depth + f'[{cls}:{tag}]'
        if isinstance(v, list):
            print(pre); show(v, depth + 1)
        else:
            if cls == 0 and tag == 2:
                print(pre, 'INT', int.from_bytes(v, 'big', signed=True))
            elif cls == 0 and tag == 10:
                print(pre, 'ENUM', int.from_bytes(v, 'big', signed=True))
            elif cls == 0 and tag in (12, 19, 22, 26, 27):
                print(pre, 'STR', v.decode('latin1'))
            elif cls == 0 and tag == 4 and len(v) > 8:
                inner = try_inner(v)
                if inner is not None and len(v) > 50:
                    print(pre, f'OCTET({len(v)}) -> BER'); show(inner, depth + 1)
                else:
                    print(pre, 'OCTET', v[:maxbytes].hex())
            else:
                print(pre, 'RAW', v[:maxbytes].hex() if any(c < 32 or c > 126 for c in v) else v.decode('latin1'))

if __name__ == '__main__':
    show(parse(open(sys.argv[1], 'rb').read()))
