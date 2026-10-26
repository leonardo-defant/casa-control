"""Baixa arquivos de urna por seção do site de resultados do TSE (2026).

Caminhos usados (padrão documentado em 2022 e conferido em 2026):
  aux:     /oficial/ele2026/arquivo-urna/{pleito}/dados/{uf}/{mun5}/{zona4}/{secao4}/p00{pleito}-{uf}-m{mun5}-z{zona4}-s{secao4}-aux.json
  arquivo: /oficial/ele2026/arquivo-urna/{pleito}/dados/{uf}/{mun5}/{zona4}/{secao4}/{hash}/{nome listado no aux}
Só pede arquivos que o aux lista. Retoma: arquivos já salvos não são pedidos de novo.

Uso: python3 -I baixar_arquivos_urna.py <pleito> <lista.txt> <pasta_saida> <tipos: bu,rdv,log> [conc]
lista.txt: uma seção por linha no formato UF|mun|zona|secao (números sem zeros à esquerda).
"""
import json, os, ssl, sys, threading, time, urllib.request, urllib.error
from concurrent.futures import ThreadPoolExecutor

BASE = 'https://resultados.tse.jus.br/oficial/ele2026/arquivo-urna'
CTX = ssl.create_default_context(cafile=os.environ.get('SSL_CERT_FILE', '/root/.ccr/ca-bundle.crt'))
lock = threading.Lock()
stats = {'req': 0, 'erro': 0, 'bloqueio': 0, 'r429': 0, 'secoes': 0, 'bytes': 0, 'falhou': 0}
TAXA = float(os.environ.get('TAXA', '3'))  # requisições por segundo, no total
_prox = [0.0]
pausa_ate = [0.0]


def espera_vez():
    """Limitador global: espaça as requisições e respeita a pausa após um 429."""
    while True:
        with lock:
            agora = time.time()
            alvo = max(_prox[0], pausa_ate[0])
            if agora >= alvo:
                _prox[0] = agora + 1.0 / TAXA
                return
        time.sleep(min(alvo - agora, 1.0))


def get(url, tent=12):
    for t in range(tent):
        espera_vez()
        try:
            req = urllib.request.Request(url, headers={'User-Agent': 'auditoria-eleicao-2026 (pesquisa)'})
            with urllib.request.urlopen(req, timeout=60, context=CTX) as r:
                b = r.read()
            with lock:
                stats['req'] += 1; stats['bytes'] += len(b)
            if b[:200].lower().lstrip().startswith(b'<!doctype html') or b[:200].lower().lstrip().startswith(b'<html'):
                with lock: stats['bloqueio'] += 1
                time.sleep(30 * (t + 1)); continue
            return b
        except urllib.error.HTTPError as e:
            if e.code == 404:
                with lock: stats['erro'] += 1
                return None
            if e.code == 429:
                with lock:
                    stats['r429'] += 1
                    pausa_ate[0] = max(pausa_ate[0], time.time() + 20 * min(t + 1, 6))
                continue
            with lock: stats['erro'] += 1
            time.sleep(5 * (t + 1))
        except Exception:
            with lock: stats['erro'] += 1
            time.sleep(5 * (t + 1))
    with lock: stats['falhou'] += 1
    return None


def secao(pleito, linha, saida, tipos):
    uf, mun, zona, sec = linha.split('|')
    uf = uf.lower(); m5 = f'{int(mun):05d}'; z4 = f'{int(zona):04d}'; s4 = f'{int(sec):04d}'
    d = os.path.join(saida, uf, m5, z4, s4); os.makedirs(d, exist_ok=True)
    pa = os.path.join(d, 'aux.json')
    base = f'{BASE}/{pleito}/dados/{uf}/{m5}/{z4}/{s4}'
    if os.path.exists(pa):
        aux = json.load(open(pa))
    else:
        b = get(f'{base}/p00{pleito}-{uf}-m{m5}-z{z4}-s{s4}-aux.json')
        if b is None:
            open(os.path.join(d, 'SEM_AUX'), 'w').close(); return
        aux = json.loads(b.decode('utf-8'))
        open(pa, 'wb').write(b)
    for i, h in enumerate(aux.get('hashes', [])):
        for a in h.get('arq', []):
            if a.get('tp') not in tipos:
                continue
            nome = a['nm']; dest = os.path.join(d, f'{i}-{nome}')
            if os.path.exists(dest):
                continue
            b = get(f"{base}/{h['hash']}/{nome}")
            if b is not None:
                open(dest + '.part', 'wb').write(b); os.replace(dest + '.part', dest)
    with lock:
        stats['secoes'] += 1


if __name__ == '__main__':
    pleito, lista, saida, tipos = sys.argv[1], sys.argv[2], sys.argv[3], set(sys.argv[4].split(','))
    conc = int(sys.argv[5]) if len(sys.argv) > 5 else 4
    linhas = [l.strip() for l in open(lista) if l.strip()]
    t0 = time.time()
    with ThreadPoolExecutor(conc) as ex:
        futs = [ex.submit(secao, pleito, l, saida, tipos) for l in linhas]
        ult = [time.time()]
        for i, f in enumerate(futs):
            f.result()
            if time.time() - ult[0] > 60 or i + 1 == len(futs):
                ult[0] = time.time()
                dt = time.time() - t0
                print(f"{i+1}/{len(futs)} secoes, {stats['req']} req, {stats['req']/dt:.1f} req/s, erros {stats['erro']}, 429 {stats['r429']}, falhas {stats['falhou']}, bloqueios {stats['bloqueio']}, {stats['bytes']/1e6:.0f} MB", flush=True)
