"""Requer faster-whisper (modelo small). Gerar cada fala com "\n\nObrigado." no fim do texto: o seed_audio corta o
final do áudio, e assim o corte cai na palavra de reserva, que este script remove.
Corta a palavra de reserva ("Obrigado.") do fim de uma tomada: acha a palavra pelo reconhecimento de fala,
corta no meio do silêncio que a antecede e confere o que sobrou.
Uso: cortar_reserva.py <modelo_dir> <entrada.wav> <saida.wav>"""
import array, subprocess, sys
import numpy as np
from faster_whisper import WhisperModel

modelo_dir, ent, sai = sys.argv[1:4]
m = WhisperModel('small', device='cpu', compute_type='int8', download_root=modelo_dir)


def ler(arq):
    raw = subprocess.run(['ffmpeg', '-loglevel', 'error', '-i', arq, '-ac', '1', '-ar', '16000', '-f', 's16le', '-'], capture_output=True).stdout
    return np.frombuffer(raw, np.int16).astype(np.float32) / 32768


def palavras(audio):
    segs, _ = m.transcribe(audio, language='pt', word_timestamps=True, beam_size=5)
    return [w for s in segs for w in s.words]


a = ler(ent); pal = palavras(a)
res = [w for w in pal if 'obrigad' in w.word.lower() or 'assistir' in w.word.lower()]
if not res:
    sys.exit(f'ERRO: palavra de reserva não encontrada em {ent}')
t_res = res[-1].start
env = np.sqrt(np.convolve(a ** 2, np.ones(320) / 320, 'same'))[::320]  # janelas de 20 ms
lim = env.max() * 0.03
i0, i1 = int(max(0, t_res - 2.5) / 0.02), int((t_res + 0.1) / 0.02)
melhor, ini, k = (0, None), None, i0
for k in range(i0, min(i1, len(env))):
    if env[k] <= lim:
        ini = k if ini is None else ini
        if k - ini + 1 > melhor[0]: melhor = (k - ini + 1, ini)
    else:
        ini = None
if melhor[0] * 0.02 < 0.15:
    sys.exit(f'ERRO: sem pausa clara antes da reserva em {ent} (maior pausa {melhor[0]*0.02:.2f}s)')
fim_fala = melhor[1] * 0.02; corte = fim_fala + min(0.25, melhor[0] * 0.02 / 2)
subprocess.run(['ffmpeg', '-y', '-loglevel', 'error', '-i', ent, '-af', f'atrim=0:{corte:.3f}', sai], check=True)
ult = palavras(ler(sai))[-6:]
print(f'{ent.split("/")[-1]}: reserva em {t_res:.2f}s, pausa {melhor[0]*0.02:.2f}s, corte em {corte:.2f}s :: ' + ' '.join(w.word.strip() for w in ult))
