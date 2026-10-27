"""Acerta o tempo das legendas pela fala real: transcreve a fala de cada cena com tempo por palavra (faster-whisper),
alinha as palavras ao texto narrado e faz cada legenda entrar até 0,25 s antes da primeira palavra do seu trecho,
nunca antes de a fala anterior acabar. Reescreve plano.json no lugar.
Requer faster-whisper (modelo small). Uso: alinhar_legendas.py <modelo_dir> <narracao.json> <plano.json>
"""
import difflib, json, re, subprocess, sys, unicodedata
import numpy as np
from faster_whisper import WhisperModel

ANTES = 0.25  # quanto a legenda pode entrar antes da primeira palavra
# palavras curtas que o reconhecimento costuma pôr no lugar errado; o trecho se ancora na primeira palavra de conteúdo
CURTAS = {'e', 'o', 'a', 'os', 'as', 'de', 'do', 'da', 'dos', 'das', 'em', 'no', 'na', 'um', 'uma', 'que', 'é', 'se', 'por', 'para', 'com', 'mas'}

UNID = {'zero': 0, 'um': 1, 'uma': 1, 'dois': 2, 'duas': 2, 'três': 3, 'quatro': 4, 'cinco': 5, 'seis': 6, 'sete': 7, 'oito': 8,
        'nove': 9, 'dez': 10, 'onze': 11, 'doze': 12, 'treze': 13, 'catorze': 14, 'quatorze': 14, 'quinze': 15, 'dezesseis': 16,
        'dezessete': 17, 'dezoito': 18, 'dezenove': 19, 'vinte': 20, 'trinta': 30, 'quarenta': 40, 'cinquenta': 50,
        'sessenta': 60, 'setenta': 70, 'oitenta': 80, 'noventa': 90, 'cem': 100, 'cento': 100, 'duzentos': 200,
        'duzentas': 200, 'trezentos': 300, 'trezentas': 300, 'quatrocentos': 400, 'quatrocentas': 400, 'quinhentos': 500,
        'quinhentas': 500, 'seiscentos': 600, 'seiscentas': 600, 'setecentos': 700, 'setecentas': 700, 'oitocentos': 800,
        'oitocentas': 800, 'novecentos': 900, 'novecentas': 900}


def limpa(w):
    w = unicodedata.normalize('NFC', w.lower())
    return re.sub(r"[^\w,]", '', w).strip(',')


def numeros(pal):
    """Troca sequências de números por extenso por algarismos ('cinco mil duzentas e vinte e oito' -> '5228',
    'dois vírgula sete' -> '2,7', 'noventa e quatro por cento' -> '94'). 'um'/'uma' sozinhos ficam como palavra."""
    out, i = [], 0
    while i < len(pal):
        if pal[i] not in UNID and pal[i] != 'mil':
            out.append(pal[i]); i += 1; continue
        j, total, grupo, n = i, 0, 0, 0
        while j < len(pal):
            w = pal[j]
            if w in UNID: grupo += UNID[w]; n += 1; j += 1
            elif w == 'mil': total += max(grupo, 1) * 1000; grupo = 0; n += 1; j += 1
            elif w == 'e' and j + 1 < len(pal) and pal[j + 1] in UNID and n: j += 1
            else: break
        valor = str(total + grupo)
        if j + 1 < len(pal) and pal[j] == 'vírgula' and pal[j + 1] in UNID:
            valor += ',' + str(UNID[pal[j + 1]]); n += 1; j += 2
        if n == 1 and pal[i] in ('um', 'uma') and ',' not in valor:
            out.append(pal[i]); i += 1; continue
        out.append(valor)
        if j + 1 < len(pal) and pal[j] == 'por' and pal[j + 1] == 'cento': j += 2
        i = j
    return out


def palavras_asr(m, arq):
    raw = subprocess.run(['ffmpeg', '-loglevel', 'error', '-i', arq, '-ac', '1', '-ar', '16000', '-f', 's16le', '-'], capture_output=True).stdout
    audio = np.frombuffer(raw, np.int16).astype(np.float32) / 32768
    segs, _ = m.transcribe(audio, language='pt', word_timestamps=True, beam_size=5)
    out = []
    for s in segs:
        for w in s.words:
            t = w.word.strip().lower().replace('%', '')
            t = re.sub(r'(?<=\d)\.(?=\d{3})', '', t)
            if re.fullmatch(r',\d+[.,!?]?', t) and out:  # '2' + ',7' -> '2,7'
                out[-1][0] += ',' + re.sub(r'\D', '', t); out[-1][2] = w.end; continue
            out.append([limpa(t), w.start, w.end])
    return [x for x in out if x[0]]


def pausas(arq, minimo=0.08):
    """Trechos de silêncio (início, fim) em segundos, por janelas de 10 ms abaixo de 3% do pico."""
    raw = subprocess.run(['ffmpeg', '-loglevel', 'error', '-i', arq, '-ac', '1', '-ar', '16000', '-f', 's16le', '-'], capture_output=True).stdout
    a = np.frombuffer(raw, np.int16).astype(np.float32)
    n = len(a) // 160; env = np.sqrt((a[:n * 160].reshape(n, 160) ** 2).mean(axis=1)); lim = env.max() * 0.03
    out, ini = [], None
    for k, e in enumerate(env):
        if e <= lim and ini is None: ini = k
        elif e > lim and ini is not None:
            if (k - ini) * 0.01 >= minimo: out.append((ini * 0.01, k * 0.01))
            ini = None
    return out


def main():
    modelo_dir, nar_arq, plano_arq = sys.argv[1:4]
    m = WhisperModel('small', device='cpu', compute_type='int8', download_root=modelo_dir)
    nar = json.load(open(nar_arq))['cenas']; plano = json.load(open(plano_arq))
    for i, (c, n) in enumerate(zip(plano['cenas'], nar)):
        falado = [p[0] for p in n['legendas']]
        assert len(falado) == len(c['legenda']), f'cena {i}: legendas do plano e da narração não batem'
        tok, dono = [], []
        for k, frag in enumerate(falado):
            ts = numeros([limpa(w) for w in frag.split() if limpa(w)])
            tok += ts; dono += [k] * len(ts)
        asr = palavras_asr(m, c['audio']); silencios = pausas(c['audio'])
        mapa = {}
        for a, b, size in difflib.SequenceMatcher(None, tok, [x[0] for x in asr], autojunk=False).get_matching_blocks():
            for d in range(size): mapa[a + d] = b + d
        inicios = []
        for k in range(len(falado)):
            idx = [j for j in range(len(tok)) if dono[j] == k]
            casados = [j for j in idx if j in mapa]
            if not casados:
                inicios.append(None); continue
            j1 = casados[0]; t1 = asr[mapa[j1]][1] - 0.2 * (j1 - idx[0])
            j2 = next((x for x in casados[:4] if tok[x] not in CURTAS), j1); t2 = asr[mapa[j2]][1] - 0.2 * (j2 - idx[0])
            fim_antes = asr[mapa[j1] - 1][2] if mapa[j1] > 0 and j1 == idx[0] else 0.0
            # o reconhecimento erra o tempo das palavras curtas; a fronteira real do trecho é a maior pausa por perto
            perto = [p for p in silencios if min(t1, t2) - 0.5 <= p[1] <= max(t1, t2) + 0.3]
            if perto:
                p = max(perto, key=lambda p: p[1] - p[0]); t, fim_antes = p[1], p[0]
            else:
                t = t1 if j1 == idx[0] else t2
            inicios.append(max(fim_antes, t - ANTES, 0.0))
        # trechos sem nenhuma palavra casada: meio caminho entre os vizinhos
        for k, v in enumerate(inicios):
            if v is None:
                ant = next((inicios[x] for x in range(k - 1, -1, -1) if inicios[x] is not None), 0.0)
                pos = next((inicios[x] for x in range(k + 1, len(inicios)) if inicios[x] is not None), c['duracao'] - 0.5)
                inicios[k] = (ant + pos) / 2
        inicios[0] = min(inicios[0], 0.3)
        for k in range(1, len(inicios)):
            inicios[k] = max(inicios[k], inicios[k - 1] + 0.4)
        velho = [x[0] for x in c['legenda']]
        for k, x in enumerate(c['legenda']):
            x[0] = round(float(inicios[k]), 3); x[1] = round(float(inicios[k + 1]), 3) if k + 1 < len(inicios) else round(c['duracao'], 3)
        casou = sum(1 for j in range(len(tok)) if j in mapa)
        desvio = max(abs(a - b) for a, b in zip(velho, inicios))
        print(f'cena{i:02d} {c["tipo"]:<12} palavras casadas {casou}/{len(tok)}  maior mudança {desvio:.2f}s  inícios {[round(float(x), 2) for x in inicios]}', flush=True)
    json.dump(plano, open(plano_arq, 'w'), ensure_ascii=False, indent=1)


if __name__ == '__main__':
    main()
