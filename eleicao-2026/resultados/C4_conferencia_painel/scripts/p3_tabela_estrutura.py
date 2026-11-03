"""Conferência PAINEL, passo 3: separar a Tabela Mestra v21 (HTML de 74 MB, guardado em gzip) em partes, como TEXTO.

Uso: python3 -I p3_tabela_estrutura.py <arquivo.html.gz> <pasta_saida_das_partes>
Nada é executado. Lê o gzip, acha os blocos <script ...> e grava cada um (exceto o de dados) como .txt na pasta de
saída (que é pasta de download, dado não confiável). Do bloco de dados (script id="raw-data") grava só as 30 primeiras
e as 5 últimas linhas e conta linhas e campos por linha.
Decisões (antes de rodar): nenhuma; é só separação.
"""
import gzip
import os
import re
import sys
from collections import Counter


def main():
    src = gzip.open(sys.argv[1], 'rb').read().decode('utf-8', errors='replace')
    out = sys.argv[2]
    print('chars', len(src))
    blocos = [(m.start(), m.end(), m.group(1)) for m in re.finditer(r'<script([^>]*)>', src)]
    print('scripts', len(blocos))
    for k, (ini, fim_tag, attrs) in enumerate(blocos):
        fim = src.find('</script>', fim_tag)
        corpo = src[fim_tag:fim]
        print(k, ini, attrs.strip(), 'len', len(corpo))
        if 'raw-data' in attrs:
            linhas = corpo.strip('\n').split('\n')
            print('  linhas de dados', len(linhas))
            print('  campos por linha', Counter(len(l.split(',')) for l in linhas).most_common(5))
            with open(os.path.join(out, 'raw_data_amostra.txt'), 'w', encoding='utf-8') as f:
                f.write('\n'.join(linhas[:30]) + '\n...\n' + '\n'.join(linhas[-5:]) + '\n')
        else:
            with open(os.path.join(out, 'script_%02d.txt' % k), 'w', encoding='utf-8') as f:
                f.write(corpo)
    depois = src[src.rfind('</script>') + 9:]
    print('depois do último script', len(depois), repr(depois[:300]))


if __name__ == '__main__':
    main()
