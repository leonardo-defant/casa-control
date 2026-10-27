"""Transcreve o áudio que toca durante cada legenda e compara a 1ª e a última palavra com o trecho esperado."""
import json, subprocess, sys, unicodedata, re
import numpy as np
from faster_whisper import WhisperModel
sys.path.insert(0, '/home/user/casa-control/eleicao-2026/video/motor')
from alinhar_legendas import numeros, limpa
modelo, plano_arq, nar_arq, video = sys.argv[1:5]
m = WhisperModel('small', device='cpu', compute_type='int8', download_root=modelo)
p = json.load(open(plano_arq)); nar = json.load(open(nar_arq))['cenas']
raw = subprocess.run(['ffmpeg', '-loglevel', 'error', '-i', video, '-vn', '-ac', '1', '-ar', '16000', '-f', 's16le', '-'], capture_output=True).stdout
audio = np.frombuffer(raw, np.int16).astype(np.float32) / 32768
t0 = 0.0; ruins = 0; total = 0
for i, c in enumerate(p['cenas']):
    for k, (a, b, txt) in enumerate(c['legenda']):
        falado = nar[i]['legendas'][k][0]
        esp = numeros([limpa(w) for w in falado.split() if limpa(w)])
        seg = audio[int((t0 + a) * 16000):int((t0 + b) * 16000)]
        segs, _ = m.transcribe(seg, language='pt', beam_size=5, condition_on_previous_text=False)
        ouv = ' '.join(s.text for s in segs).strip()
        oth = [re.sub(r'\D', '', w) if re.search(r'\d', w) else limpa(w) for w in ouv.replace('%', ' ').split()]
        oth = [w for w in oth if w]
        ok_ini = bool(oth) and (oth[0] == esp[0] or oth[0][:3] == esp[0][:3])
        ok_fim = bool(oth) and (oth[-1] == esp[-1] or oth[-1][:3] == esp[-1][:3] or esp[-1].replace(',', '') == oth[-1])
        total += 1
        if not (ok_ini and ok_fim):
            ruins += 1
            print(f'cena{i:02d} leg{k:02d} [{t0 + a:7.2f}-{t0 + b:7.2f}] esperado: "{falado}"\n                       ouvido:   "{ouv}"', flush=True)
    t0 += c['duracao']
print(f'{total} legendas, {ruins} com início ou fim diferente do esperado')
