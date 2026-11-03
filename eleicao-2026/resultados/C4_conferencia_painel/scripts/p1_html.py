"""Conferência PAINEL, passo 1: ler o HTML baixado como texto (nunca executar nada).

Uso: python3 -I p1_html.py <arquivo.html>
Imprime: título, texto visível, todos os caminhos /_next/static citados, o payload RSC (self.__next_f.push) resumido,
e qualquer URL externa (http/https) citada.
Decisões (antes de rodar): só leitura de texto; travessões do original trocados por hífen na impressão.
"""
import re
import sys


def visivel(h):
    s = re.sub(r'<script[^>]*>.*?</script>', ' ', h, flags=re.S | re.I)
    s = re.sub(r'<style[^>]*>.*?</style>', ' ', s, flags=re.S | re.I)
    s = re.sub(r'<[^>]+>', ' ', s)
    s = s.replace('\u2014', '-').replace('\u2013', '-')
    return re.sub(r'\s+', ' ', s).strip()


def main():
    h = open(sys.argv[1], encoding='utf-8', errors='replace').read()
    print('bytes', len(h.encode('utf-8')))
    t = re.search(r'<title>(.*?)</title>', h, flags=re.S)
    print('title:', t.group(1) if t else None)
    v = visivel(h)
    print('visivel (%d chars):' % len(v), v)
    caminhos = sorted(set(re.findall(r'(?:/_next/)?static/(?:chunks|css|media)/[A-Za-z0-9_./\-\[\]]+', h)))
    print('caminhos static (%d):' % len(caminhos))
    for c in caminhos:
        print('  ', c)
    urls = sorted(set(re.findall(r'https?://[A-Za-z0-9_.\-]+(?:/[^\s"\'<>\\]*)?', h)))
    print('urls (%d):' % len(urls))
    for u in urls:
        print('  ', u)
    pushes = re.findall(r'self\.__next_f\.push\((.*?)\)</script>', h, flags=re.S)
    print('pushes RSC:', len(pushes))
    for p in pushes:
        q = p.replace('\u2014', '-').replace('\u2013', '-')
        print('  ---', len(q), 'chars:', q[:1500])


if __name__ == '__main__':
    main()
