"""Junta as cenas renderizadas e a narração num MP4 final 1080x1920.
Cada fala é completada com silêncio até a duração exata da sua tela (em amostras), as falas viram uma trilha única em PCM
e o AAC é codificado uma vez só, para o áudio não ir atrasando a cada emenda.
Com --musica, a trilha entra por baixo da voz: em loop até o fim, no nível --musica-lufs (padrão -20, a voz fica em -16),
abaixando uns 7 dB enquanto a voz fala (sidechain; sob a fala fica perto de -27) e com fade de entrada e de saída.
--musica-inicio pula o começo do arquivo (silêncio ou introdução).
Uso: python3 -I montar_video.py <plano.json> <pasta_cenas> <saida.mp4> [--musica <arq>] [--musica-lufs -20] [--musica-inicio 0] [--velocidade 1.06]
--velocidade: acelera a voz (atempo) e encurta cada cena na mesma proporção; as telas precisam ter sido renderizadas
com o mesmo valor (render.js --velocidade). A música não acelera.
"""
import json, os, re, subprocess, sys, tempfile

TAXA = 48000


def loudness(arq):
    err = subprocess.run(['ffmpeg', '-nostdin', '-i', arq, '-af', 'ebur128', '-f', 'null', '-'], capture_output=True, text=True).stderr
    return float(re.findall(r'I:\s+(-?[\d.]+) LUFS', err)[-1])


def main():
    plano_arq, pasta, saida = sys.argv[1:4]
    plano = json.load(open(plano_arq))
    vel = float(sys.argv[sys.argv.index('--velocidade') + 1]) if '--velocidade' in sys.argv else 1.0
    fps = plano.get('fps', 30)
    durs = [round(c['duracao'] / vel * fps) / fps for c in plano['cenas']]  # o mesmo número de quadros do render.js
    tmp = tempfile.mkdtemp(prefix='montagem_', dir=os.path.dirname(os.path.abspath(saida)))
    falas, telas = [], []
    for i, c in enumerate(plano['cenas']):
        n = round(durs[i] * TAXA)
        w = os.path.join(tmp, f'fala{i:02d}.wav')
        subprocess.run(['ffmpeg', '-y', '-loglevel', 'error', '-i', c['audio'], '-af', (f'atempo={vel:.5f},' if vel != 1 else '') + f'aresample={TAXA},apad=whole_len={n},atrim=end_sample={n}',
                        '-ac', '2', '-c:a', 'pcm_s16le', w], check=True)
        falas.append(w); telas.append(os.path.join(pasta, f'cena{i:02d}_{c["tipo"]}.mp4'))
    def lista(nome, arqs):
        arq = os.path.join(tmp, nome)
        with open(arq, 'w') as f:
            f.writelines(f"file '{a}'\n" for a in arqs)
        return arq
    trilha = os.path.join(tmp, 'trilha.wav'); video = os.path.join(tmp, 'video.mp4')
    subprocess.run(['ffmpeg', '-y', '-loglevel', 'error', '-f', 'concat', '-safe', '0', '-i', lista('falas.txt', falas), '-c', 'copy', trilha], check=True)
    subprocess.run(['ffmpeg', '-y', '-loglevel', 'error', '-f', 'concat', '-safe', '0', '-i', lista('telas.txt', telas), '-an', '-c', 'copy', video], check=True)
    total = sum(durs)
    if '--musica' in sys.argv:
        musica = sys.argv[sys.argv.index('--musica') + 1]
        alvo = float(sys.argv[sys.argv.index('--musica-lufs') + 1]) if '--musica-lufs' in sys.argv else -20.0
        ini = float(sys.argv[sys.argv.index('--musica-inicio') + 1]) if '--musica-inicio' in sys.argv else 0.0
        ganho = alvo - loudness(musica)
        mix = os.path.join(tmp, 'mix.wav')
        subprocess.run(['ffmpeg', '-nostdin', '-y', '-loglevel', 'error', '-i', trilha, '-stream_loop', '-1', '-ss', f'{ini:.2f}', '-i', musica, '-filter_complex',
                        f'[1:a]aresample={TAXA},aformat=channel_layouts=stereo,volume={ganho:.2f}dB,atrim=0:{total:.3f},'
                        f'afade=t=in:d=1.5,afade=t=out:st={total - 3:.3f}:d=3[m];[0:a]asplit=2[v][sc];'
                        '[m][sc]sidechaincompress=threshold=0.06:ratio=2:attack=30:release=600[md];'  # abaixa uns 7 dB sob a voz
                        '[v][md]amix=inputs=2:duration=first:normalize=0,alimiter=limit=0.84:level=disabled[a]',
                        '-map', '[a]', '-c:a', 'pcm_s16le', mix], check=True)
        trilha = mix
        print(f'música: {os.path.basename(musica)} em {alvo} LUFS (ganho {ganho:+.1f} dB) com sidechain da voz')
    # fade curto no fim do vídeo; o resto da trilha vai como está
    subprocess.run(['ffmpeg', '-y', '-loglevel', 'error', '-i', video, '-i', trilha, '-map', '0:v', '-map', '1:a', '-c:v', 'copy',
                    '-af', f'afade=t=out:st={total - 0.4:.3f}:d=0.4', '-c:a', 'aac', '-b:a', '192k', '-ar', str(TAXA), '-shortest',
                    '-movflags', '+faststart', saida], check=True)
    d = subprocess.run(['ffprobe', '-v', 'error', '-show_entries', 'format=duration', '-of', 'csv=p=0', saida], capture_output=True, text=True).stdout
    print('pronto:', saida, round(float(d), 1), 's')


if __name__ == '__main__':
    main()
