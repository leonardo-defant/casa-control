"""Junta as cenas renderizadas e a narração num MP4 final 1080x1920.
Cada fala é completada com silêncio até a duração exata da sua tela (em amostras), as falas viram uma trilha única em PCM
e o AAC é codificado uma vez só, para o áudio não ir atrasando a cada emenda.
Uso: python3 -I montar_video.py <plano.json> <pasta_cenas> <saida.mp4>
"""
import json, os, subprocess, sys, tempfile

TAXA = 48000


def main():
    plano_arq, pasta, saida = sys.argv[1:4]
    plano = json.load(open(plano_arq))
    tmp = tempfile.mkdtemp(prefix='montagem_', dir=os.path.dirname(os.path.abspath(saida)))
    falas, telas = [], []
    for i, c in enumerate(plano['cenas']):
        n = round(c['duracao'] * TAXA)
        w = os.path.join(tmp, f'fala{i:02d}.wav')
        subprocess.run(['ffmpeg', '-y', '-loglevel', 'error', '-i', c['audio'], '-af', f'aresample={TAXA},apad=whole_len={n},atrim=end_sample={n}',
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
    # fade curto no fim do vídeo; o resto da trilha vai como está
    total = sum(c['duracao'] for c in plano['cenas'])
    subprocess.run(['ffmpeg', '-y', '-loglevel', 'error', '-i', video, '-i', trilha, '-map', '0:v', '-map', '1:a', '-c:v', 'copy',
                    '-af', f'afade=t=out:st={total - 0.4:.3f}:d=0.4', '-c:a', 'aac', '-b:a', '192k', '-ar', str(TAXA), '-shortest',
                    '-movflags', '+faststart', saida], check=True)
    d = subprocess.run(['ffprobe', '-v', 'error', '-show_entries', 'format=duration', '-of', 'csv=p=0', saida], capture_output=True, text=True).stdout
    print('pronto:', saida, round(float(d), 1), 's')


if __name__ == '__main__':
    main()
