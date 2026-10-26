"""Totais do 2º turno de 2026 (presidente) por município, do site de resultados do TSE (mesmo arquivo do T1).
Retoma de onde parou: pula o município que já tem arquivo salvo. Pausa crescente depois de um 429.
Uso: TAXA=0.9 python3 -I baixar_municipios.py <secoes2026_1t.json.gz> <pasta_saida>
"""
import os as _os, sys as _sys
_sys.path.insert(0, _os.path.dirname(_os.path.abspath(__file__)))
import json, os, ssl, sys, time, urllib.error, urllib.request
from lib import carregar

TAXA = float(os.environ.get('TAXA', '0.9'))
CTX = ssl.create_default_context(cafile=os.environ.get('SSL_CERT_FILE', '/root/.ccr/ca-bundle.crt'))


def main():
    base, saida = sys.argv[1:3]
    muns = sorted({tuple(k.split('|')[:2]) for k in carregar(base) if not k.startswith('ZZ|')})
    os.makedirs(saida, exist_ok=True)
    st = {'ok': 0, 'pulado': 0, 'erro': 0, '429': 0}; t0 = time.time(); pausa = 30
    for i, (uf, m) in enumerate(muns):
        arq = os.path.join(saida, f'{uf.lower()}{int(m):05d}.json')
        if os.path.exists(arq):
            st['pulado'] += 1; continue
        u = f'https://resultados.tse.jus.br/oficial/ele2026/6258/dados/{uf.lower()}/{uf.lower()}{int(m):05d}-c0001-e006258-u.json'
        for tent in range(8):
            time.sleep(1.0 / TAXA)
            try:
                with urllib.request.urlopen(u, timeout=60, context=CTX) as r:
                    o = json.load(r)
                json.dump(o, open(arq + '.tmp', 'w')); os.replace(arq + '.tmp', arq)
                st['ok'] += 1; pausa = 30; break
            except urllib.error.HTTPError as e:
                if e.code == 429:
                    st['429'] += 1; time.sleep(pausa); pausa = min(pausa * 2, 600); continue
                st['erro'] += 1; print('erro', uf, m, e.code, flush=True); break
            except Exception as e:
                st['erro'] += 1; print('erro', uf, m, repr(e)[:120], flush=True); time.sleep(5)
        if (i + 1) % 100 == 0:
            print(f'{i + 1}/{len(muns)} municipios, {st}, {time.time() - t0:.0f}s', flush=True)
    print('fim', st, flush=True)


if __name__ == '__main__':
    main()
