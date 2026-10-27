"""Monta o plano do vídeo a partir da narração: acelera as cenas lentas (sem mudar o tom), mede a duração de cada uma,
quebra o texto em legendas sincronizadas pelo tamanho de cada trecho e escreve plano.json para o render.js.
Uso: python3 -I montar_plano.py <narracao.json> <pasta_audio_original> <pasta_saida>
"""
import json, os, re, subprocess, sys

ALVO = 2.6        # palavras por segundo
MAX_VEL = 1.2     # aceleração máxima
CAUDA = 0.7       # segundos de tela depois da fala
FPS = 30


def duracao(arq):
    return float(subprocess.run(['ffprobe', '-v', 'error', '-show_entries', 'format=duration', '-of', 'csv=p=0', arq],
                                capture_output=True, text=True).stdout)


def inicio_fala(arq):
    err = subprocess.run(['ffmpeg', '-i', arq, '-af', 'silencedetect=noise=-40dB:d=0.2', '-f', 'null', '-'], capture_output=True, text=True).stderr
    ini = re.findall(r'silence_start: ([\d.]+)', err); fim = re.findall(r'silence_end: ([\d.]+)', err)
    return float(fim[0]) if ini and float(ini[0]) < 0.05 and fim else 0.0


def trechos(texto, max_pal=8):
    """Quebra em trechos de até max_pal palavras, preferindo pontuação."""
    partes = re.split(r'(?<=[.,:;?!])\s+', texto)
    out = []
    for p in partes:
        pal = p.split()
        while len(pal) > max_pal:
            corte = max_pal if len(pal) - max_pal >= 3 else len(pal) // 2
            out.append(' '.join(pal[:corte])); pal = pal[corte:]
        if pal:
            if out and len(pal) <= 2 and len(out[-1].split()) + len(pal) <= max_pal + 2:
                out[-1] += ' ' + ' '.join(pal)
            else:
                out.append(' '.join(pal))
    return out


def main():
    nar, pasta, saida = sys.argv[1:4]
    os.makedirs(saida, exist_ok=True)
    cenas = json.load(open(nar))['cenas']
    plano = {'fps': FPS, 'cenas': []}
    for i, c in enumerate(cenas):
        orig = os.path.join(pasta, f'cena{i:02d}.wav'); d0 = duracao(orig)
        pal = len(c['texto'].split())
        vel = min(MAX_VEL, max(1.0, ALVO / (pal / d0)))
        arq = os.path.join(saida, f'cena{i:02d}.wav')
        subprocess.run(['ffmpeg', '-y', '-loglevel', 'error', '-i', orig, '-af', f'atempo={vel:.4f}', '-ar', '48000', '-ac', '2', arq], check=True)
        d = duracao(arq); t0 = inicio_fala(arq)
        dur_cena = round((d + CAUDA) * FPS) / FPS
        # legenda: tempo de cada trecho proporcional ao número de caracteres (inclui pausas da pontuação)
        if 'legendas' in c:  # pares [trecho falado, legenda com algarismos]: o tempo sai do trecho falado
            falado = [p[0] for p in c['legendas']]; tr = [p[1] for p in c['legendas']]
        else:
            falado = tr = trechos(c['texto'])
        pesos = [len(x) + 6 * len(re.findall(r'[.,:;?!]', x)) for x in falado]; tot = sum(pesos)
        leg, t = [], t0
        for x, p in zip(tr, pesos):
            dt = (d - t0) * p / tot
            leg.append([round(t, 3), round(t + dt, 3), x]); t += dt
        leg[-1][1] = round(dur_cena, 3)
        plano['cenas'].append({'tipo': c['tipo'], 'duracao': dur_cena, 'audio': arq, 'velocidade': round(vel, 3), 'legenda': leg})
        print(f'cena{i:02d} {c["tipo"]:<12} original {d0:5.2f}s  x{vel:.2f} -> {d:5.2f}s  tela {dur_cena:5.2f}s  legendas {len(leg)}')
    json.dump(plano, open(os.path.join(saida, 'plano.json'), 'w'), ensure_ascii=False, indent=1)
    print('total', round(sum(c['duracao'] for c in plano['cenas']), 1), 's')


if __name__ == '__main__':
    main()
