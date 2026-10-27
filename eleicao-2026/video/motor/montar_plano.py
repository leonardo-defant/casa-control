"""Monta o plano do vídeo a partir da narração: acelera as cenas lentas (sem mudar o tom), mede a duração de cada uma,
quebra o texto em legendas sincronizadas pelo tamanho de cada trecho e escreve plano.json para o render.js.
Uso: python3 -I montar_plano.py <narracao.json> <pasta_audio_original> <pasta_saida> [--alvo 2.6] [--max-vel 1.2]
Depois, alinhar_legendas.py troca os tempos estimados das legendas pelos tempos reais das palavras.
"""
import array, json, os, re, subprocess, sys

ALVO = 2.6        # palavras por segundo
MAX_VEL = 1.2     # aceleração máxima
CAUDA = 0.3       # segundos de tela depois da fala (somado às margens abaixo, dá ~0,65 s entre uma fala e outra)
MARGEM_INI = 0.12 # silêncio mantido antes da fala
MARGEM_FIM = 0.25 # mantido depois da fala (preserva o decaimento da última sílaba)
CAUDA_FINAL = 2.0 # respiro depois da última fala do vídeo
FPS = 30
LUFS = -16.0      # loudness de cada fala, perto do que as redes usam; o limitador segura os picos em -1,5 dBFS


def loudness(arq):
    err = subprocess.run(['ffmpeg', '-i', arq, '-af', 'ebur128', '-f', 'null', '-'], capture_output=True, text=True).stderr
    return float(re.findall(r'I:\s+(-?[\d.]+) LUFS', err)[-1])


def duracao(arq):
    return float(subprocess.run(['ffprobe', '-v', 'error', '-show_entries', 'format=duration', '-of', 'csv=p=0', arq],
                                capture_output=True, text=True).stdout)


def limites_fala(arq):
    """Início e fim da fala (s), pelo envelope em janelas de 20 ms com limiar de 3% do pico.
    Estalos isolados nas pontas (até 60 ms, a 0,12 s ou mais da fala) não contam como fala."""
    raw = subprocess.run(['ffmpeg', '-loglevel', 'error', '-i', arq, '-ac', '1', '-ar', '16000', '-f', 's16le', '-'], capture_output=True).stdout
    a = array.array('h', raw); jan = 320
    env = [(sum(x * x for x in a[k:k + jan]) / jan) ** 0.5 for k in range(0, len(a) - jan, jan)]
    lim = max(env) * 0.03
    blocos, ini = [], None  # trechos contínuos acima do limiar, em janelas
    for k, e in enumerate(env + [0]):
        if e > lim and ini is None: ini = k
        elif e <= lim and ini is not None: blocos.append([ini, k]); ini = None
    while len(blocos) > 1 and blocos[0][1] - blocos[0][0] <= 3 and blocos[1][0] - blocos[0][1] >= 6: blocos.pop(0)
    while len(blocos) > 1 and blocos[-1][1] - blocos[-1][0] <= 3 and blocos[-1][0] - blocos[-2][1] >= 6: blocos.pop()
    return blocos[0][0] * 0.02, blocos[-1][1] * 0.02


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
    global ALVO, MAX_VEL
    nar, pasta, saida = sys.argv[1:4]
    if '--alvo' in sys.argv: ALVO = float(sys.argv[sys.argv.index('--alvo') + 1])
    if '--max-vel' in sys.argv: MAX_VEL = float(sys.argv[sys.argv.index('--max-vel') + 1])
    os.makedirs(saida, exist_ok=True)
    cenas = json.load(open(nar))['cenas']
    plano = {'fps': FPS, 'cenas': []}
    for i, c in enumerate(cenas):
        orig = os.path.join(pasta, f'cena{i:02d}.wav'); d0 = duracao(orig)
        pal = len(c['texto'].split())
        vel = min(c.get('vel_max', MAX_VEL), max(1.0, ALVO / (pal / d0)))  # 'vel_max' segura cenas densas de números
        arq = os.path.join(saida, f'cena{i:02d}.wav')
        bruto = arq + '.bruto.wav'
        subprocess.run(['ffmpeg', '-y', '-loglevel', 'error', '-i', orig, '-af', f'atempo={vel:.4f}', '-ar', '48000', '-ac', '2', bruto], check=True)
        # corta o silêncio das pontas (sobra MARGEM), com fade curto para não estalar
        f0, f1 = limites_fala(bruto); a0 = max(0.0, f0 - MARGEM_INI); a1 = min(duracao(bruto), f1 + MARGEM_FIM)
        cortado = arq + '.cortado.wav'
        subprocess.run(['ffmpeg', '-y', '-loglevel', 'error', '-i', bruto, '-af',
                        f'atrim={a0:.3f}:{a1:.3f},asetpts=PTS-STARTPTS,afade=t=in:d=0.02,afade=t=out:st={a1 - a0 - 0.04:.3f}:d=0.04', cortado], check=True)
        ganho = LUFS - loudness(cortado)  # todas as falas no mesmo nível
        subprocess.run(['ffmpeg', '-y', '-loglevel', 'error', '-i', cortado, '-af', f'volume={ganho:.2f}dB,alimiter=limit=0.84:attack=5:release=60:level=disabled',
                        '-ar', '48000', '-ac', '2', arq], check=True)
        os.remove(bruto); os.remove(cortado)
        d = duracao(arq); t0 = limites_fala(arq)[0]
        dur_cena = round((d + (CAUDA_FINAL if i == len(cenas) - 1 else CAUDA)) * FPS) / FPS
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
