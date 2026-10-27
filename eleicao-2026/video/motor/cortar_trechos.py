"""Monta uma versão curta da narração a partir da completa: escolhe as cenas, tira legendas inteiras (e o trecho de fala
delas) e renumera tudo. O corte é feito na fala original de cada cena, nas fronteiras de legenda do plano já alinhado,
que caem em pausas ou nos vales conferidos entre palavras.
Uso: python3 -I cortar_trechos.py <narracao.json> <plano_alinhado.json> <pasta_audio> <corte.json> <pasta_saida>
corte.json: {"cenas": [{"de": 1, "tipo": "contexto3", "tirar": [6, 10, 11, 12]}, {"arquivo": "fechamento.wav", "texto": ..., "legendas": ..., "tipo": ...}]}
Grava <pasta_saida>/cenaNN.wav e <pasta_saida>/narracao.json.
"""
import json, os, subprocess, sys
import numpy as np

MARGEM_INI = 0.12  # o mesmo de montar_plano.py
SUAVE = 0.008      # fade em cada emenda (s)


def ler(arq):
    taxa = int(subprocess.run(['ffprobe', '-v', 'error', '-select_streams', 'a:0', '-show_entries', 'stream=sample_rate', '-of', 'csv=p=0', arq],
                              capture_output=True, text=True).stdout)
    raw = subprocess.run(['ffmpeg', '-loglevel', 'error', '-i', arq, '-ac', '1', '-f', 's16le', '-'], capture_output=True).stdout
    return np.frombuffer(raw, np.int16).astype(np.float32), taxa


def inicio_corte(orig, vel):
    """Onde montar_plano.py começou a fala desta cena, no tempo acelerado (refaz o mesmo cálculo)."""
    sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
    from montar_plano import limites_fala
    tmp = orig + '.tmp_vel.wav'
    subprocess.run(['ffmpeg', '-y', '-loglevel', 'error', '-i', orig, '-af', f'atempo={vel:.4f}', '-ar', '48000', '-ac', '2', tmp], check=True)
    f0 = limites_fala(tmp)[0]; os.remove(tmp)
    return max(0.0, f0 - MARGEM_INI)


def main():
    nar_arq, plano_arq, pasta, corte_arq, saida = sys.argv[1:6]
    nar = json.load(open(nar_arq))['cenas']; plano = json.load(open(plano_arq))['cenas']; corte = json.load(open(corte_arq))
    os.makedirs(saida, exist_ok=True)
    novas = []
    for j, cena in enumerate(corte['cenas']):
        dest = os.path.join(saida, f'cena{j:02d}.wav')
        if 'arquivo' in cena:  # fala nova, já pronta
            subprocess.run(['ffmpeg', '-y', '-loglevel', 'error', '-i', cena['arquivo'], dest], check=True)
            novas.append({'tipo': cena['tipo'], 'texto': cena['texto'], 'legendas': cena['legendas']})
            continue
        i = cena['de']; orig = os.path.join(pasta, f'cena{i:02d}.wav'); c = plano[i]; tirar = set(cena.get('tirar', []))
        a, taxa = ler(orig)
        if tirar:
            vel = c['velocidade']; a0 = inicio_corte(orig, vel)
            orig_t = lambda tf: (a0 + tf) * vel  # tempo do plano -> tempo da fala original
            leg = c['legenda']; manter = np.ones(len(a), bool)
            for k in tirar:
                ini = 0.0 if k == 0 else orig_t(leg[k][0])
                fim = orig_t(leg[k + 1][0]) if k + 1 < len(leg) else len(a) / taxa
                manter[int(ini * taxa):int(fim * taxa)] = False
            # junta os pedaços que ficam, com fade curto em cada emenda
            pedacos, k0 = [], None
            for k in range(len(a) + 1):
                dentro = k < len(a) and manter[k]
                if dentro and k0 is None: k0 = k
                elif not dentro and k0 is not None: pedacos.append(a[k0:k].copy()); k0 = None
            n = int(SUAVE * taxa)
            for p in pedacos:
                if len(p) > 2 * n:
                    p[:n] *= np.linspace(0, 1, n); p[-n:] *= np.linspace(1, 0, n)
            a = np.concatenate(pedacos)
        subprocess.run(['ffmpeg', '-y', '-loglevel', 'error', '-f', 's16le', '-ar', str(taxa), '-ac', '1', '-i', '-', dest],
                       input=np.clip(a, -32768, 32767).astype(np.int16).tobytes(), check=True)
        legs = [p for k, p in enumerate(nar[i]['legendas']) if k not in tirar]
        novas.append({'tipo': cena.get('tipo', nar[i]['tipo']), 'texto': ' '.join(p[0] for p in legs), 'legendas': legs})
        print(f'cena{j:02d} <- cena{i:02d} {nar[i]["tipo"]:<12} tirou {sorted(tirar)}  {len(a) / taxa:5.2f}s', flush=True)
    json.dump({'versao': corte.get('versao', 'corte'), 'cenas': novas}, open(os.path.join(saida, 'narracao.json'), 'w'), ensure_ascii=False, indent=1)


if __name__ == '__main__':
    main()
