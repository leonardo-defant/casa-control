"""Junta as cenas renderizadas e a narração num MP4 final 1080x1920.
Cada cena leva o seu áudio, completado com silêncio até a duração da tela; as cenas são concatenadas em ordem.
Uso: python3 -I montar_video.py <plano.json> <pasta_cenas> <saida.mp4>
"""
import json, os, subprocess, sys, tempfile


def main():
    plano_arq, pasta, saida = sys.argv[1:4]
    plano = json.load(open(plano_arq))
    tmp = tempfile.mkdtemp(prefix='montagem_', dir=os.path.dirname(os.path.abspath(saida)))
    partes = []
    for i, c in enumerate(plano['cenas']):
        v = os.path.join(pasta, f'cena{i:02d}_{c["tipo"]}.mp4')
        out = os.path.join(tmp, f'parte{i:02d}.mp4')
        # áudio: narração + silêncio até o fim da tela, com fade curto no fim
        subprocess.run(['ffmpeg', '-y', '-loglevel', 'error', '-i', v, '-i', c['audio'],
                        '-filter_complex', f"[1:a]apad,atrim=0:{c['duracao']},afade=t=out:st={max(0, c['duracao'] - 0.25)}:d=0.25[a]",
                        '-map', '0:v', '-map', '[a]', '-c:v', 'copy', '-c:a', 'aac', '-b:a', '192k', '-ar', '48000', '-shortest', out], check=True)
        partes.append(out)
    lista = os.path.join(tmp, 'lista.txt')
    with open(lista, 'w') as f:
        for p in partes:
            f.write(f"file '{p}'\n")
    subprocess.run(['ffmpeg', '-y', '-loglevel', 'error', '-f', 'concat', '-safe', '0', '-i', lista,
                    '-c:v', 'copy', '-c:a', 'aac', '-b:a', '192k', '-movflags', '+faststart', saida], check=True)
    d = subprocess.run(['ffprobe', '-v', 'error', '-show_entries', 'format=duration', '-of', 'csv=p=0', saida], capture_output=True, text=True).stdout
    print('pronto:', saida, round(float(d), 1), 's')


if __name__ == '__main__':
    main()
