"""Conferência PAINEL, passo 2: extrair as cadeias de texto de um arquivo JavaScript baixado, como TEXTO.

Uso: python3 -I p2_strings_js.py <arquivo> <saida.txt>
Nada é executado: o arquivo é lido como bytes UTF-8 e percorrido caractere a caractere por um leitor simples de
literais (aspas duplas, simples e crases, com escapes), que pula comentários. Também lista URLs e trechos com
fetch(, /api/, .json, firebase, supabase.
Decisões (antes de rodar): só leitura; travessões (U+2014, U+2013) trocados por hífen na saída; literais com menos de
2 caracteres descartados; ordem de aparição preservada; escapes \\xNN e \\uNNNN decodificados.
"""
import re
import sys


def decod(s):
    def rep(m):
        t = m.group(0)
        if t.startswith('\\x'):
            return chr(int(t[2:], 16))
        if t.startswith('\\u{'):
            return chr(int(t[3:-1], 16))
        if t.startswith('\\u'):
            return chr(int(t[2:], 16))
        return {'\\n': '\n', '\\t': '\t', '\\"': '"', "\\'": "'", '\\\\': '\\', '\\`': '`'}.get(t, t[1:])
    return re.sub(r'\\x[0-9a-fA-F]{2}|\\u\{[0-9a-fA-F]+\}|\\u[0-9a-fA-F]{4}|\\.', rep, s)


def literais(src):
    i, n = 0, len(src)
    while i < n:
        c = src[i]
        if c == '/' and i + 1 < n and src[i + 1] == '/':
            j = src.find('\n', i)
            i = n if j < 0 else j
            continue
        if c == '/' and i + 1 < n and src[i + 1] == '*':
            j = src.find('*/', i + 2)
            i = n if j < 0 else j + 2
            continue
        if c in '"\'`':
            j = i + 1
            while j < n and src[j] != c:
                if src[j] == '\\':
                    j += 2
                    continue
                j += 1
            yield i, c, src[i + 1:j]
            i = j + 1
            continue
        i += 1


def main():
    src = open(sys.argv[1], 'rb').read().decode('utf-8', errors='replace')
    out = open(sys.argv[2], 'w', encoding='utf-8')
    print('chars', len(src), file=out)
    k = 0
    for pos, q, s in literais(src):
        if len(s) < 2:
            continue
        t = decod(s).replace('\u2014', '-').replace('\u2013', '-').replace('\n', ' / ')
        k += 1
        print('%06d%s|%s' % (pos, q, t), file=out)
    print('literais', k, file=out)
    print('== urls ==', file=out)
    for u in sorted(set(re.findall(r'https?://[^\s"\'`\\)]+', src))):
        print(u, file=out)
    print('== fetch/api ==', file=out)
    for m in re.finditer(r'fetch\(|/api/|\.json|firestore|firebase|supabase|axios|\.csv|\.pdf|download', src):
        print(m.start(), decod(src[max(0, m.start() - 100):m.start() + 160]).replace('\u2014', '-').replace('\u2013', '-'), file=out)
    out.close()


if __name__ == '__main__':
    main()
