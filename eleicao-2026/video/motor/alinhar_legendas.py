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


def envelopes(arq):
    """Envelopes de 10 ms: banda cheia e banda de voz (abaixo de 1 kHz, onde respiração e fricativas quase não aparecem)."""
    def env(filtro):
        raw = subprocess.run(['ffmpeg', '-loglevel', 'error', '-i', arq, '-af', filtro, '-ac', '1', '-ar', '16000', '-f', 's16le', '-'],
                             capture_output=True).stdout
        a = np.frombuffer(raw, np.int16).astype(np.float32); n = len(a) // 160
        return np.sqrt((a[:n * 160].reshape(n, 160) ** 2).mean(axis=1))
    return env('anull'), env('lowpass=f=1000,lowpass=f=1000')


def pausas(env, minimo=0.12):
    """Trechos de silêncio (início, fim) em segundos: janelas abaixo de 1,5% do pico da banda cheia
    (fricativas surdas e oclusões curtas não contam como pausa)."""
    lim = env.max() * 0.015; out, ini = [], None
    for k, e in enumerate(env):
        if e <= lim and ini is None: ini = k
        elif e > lim and ini is not None:
            if (k - ini) * 0.01 >= minimo: out.append((ini * 0.01, k * 0.01))
            ini = None
    return out


def ler16k(arq):
    raw = subprocess.run(['ffmpeg', '-loglevel', 'error', '-i', arq, '-ac', '1', '-ar', '16000', '-f', 's16le', '-'], capture_output=True).stdout
    return np.frombuffer(raw, np.int16).astype(np.float32) / 32768


def ouvir(m, trecho):
    """Palavras reconhecidas num trecho curto, normalizadas como o texto narrado."""
    if len(trecho) < 1600:
        return []
    segs, _ = m.transcribe(trecho, language='pt', beam_size=5, condition_on_previous_text=False)
    out = []
    for w in ' '.join(x.text for x in segs).lower().replace('%', ' ').split():
        w = re.sub(r'(?<=\d)\.(?=\d{3})', '', w); w = limpa(w)
        if w: out.append(w)
    return out


def igual(a, b):
    return a == b or (len(a) >= 3 and len(b) >= 3 and a[:3] == b[:3])


def nota_corte(antes, depois, ult, pri, seg):
    """Quanto o que se ouve dos dois lados do corte confirma a fronteira: palavra exata vale mais que só o começo dela,
    a segunda palavra do trecho novo vale pouco (o reconhecimento às vezes engole a primeira, se for curta),
    e palavra que vazou para o lado errado tira ponto."""
    n = 0
    if antes:
        n += 3 if antes[-1] == ult else (1 if igual(antes[-1], ult) else 0)
        n -= 2 if igual(antes[-1], pri) and not igual(pri, ult) else 0
    if depois:
        n += 3 if depois[0] == pri else (1 if igual(depois[0], pri) or (seg and depois[0] == seg) else 0)
        n -= 2 if igual(depois[0], ult) and not igual(pri, ult) else 0
    return n


def corte_conferido(m, audio, voz, t1, ult, pri, seg=None):
    """Fala corrida: entre os vales de voz perto de t1, o corte em que o reconhecimento ouve a última palavra do trecho
    anterior antes do corte e a primeira do trecho novo depois dele. Sem confirmação, vale o vale mais fundo."""
    a0, a1 = int(max(1, (t1 - 0.4) / 0.01)), min(len(voz) - 2, int((t1 + 0.4) / 0.01))
    vales = sorted((k for k in range(a0, a1 + 1) if voz[k] <= voz[k - 1] and voz[k] <= voz[k + 1]), key=lambda k: voz[k])[:6]
    melhor = None
    for k in vales:
        c = k * 0.01
        antes, depois = ouvir(m, audio[max(0, int((c - 1.6) * 16000)):int(c * 16000)]), ouvir(m, audio[int(c * 16000):int((c + 1.6) * 16000)])
        nota = nota_corte(antes, depois, ult, pri, seg)
        if melhor is None or nota > melhor[0]:
            melhor = (nota, c)
        if nota == 6:
            break
    if melhor and melhor[0] > 0:
        return melhor[1]
    b0, b1 = int(max(0.0, t1 - 0.05) / 0.01), int((t1 + 0.30) / 0.01)
    return (b0 + int(np.argmin(voz[b0:b1 + 1]))) * 0.01 if b1 > b0 else t1


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
        asr = palavras_asr(m, c['audio']); cheia, voz = envelopes(c['audio']); silencios = pausas(cheia); lim_voz = voz.max() * 0.03
        audio = ler16k(c['audio'])
        mapa = {}
        for a, b, size in difflib.SequenceMatcher(None, tok, [x[0] for x in asr], autojunk=False).get_matching_blocks():
            for d in range(size): mapa[a + d] = b + d
        inicios, fim_trecho = [], 0.0  # fim da última palavra reconhecida do trecho anterior
        for k in range(len(falado)):
            idx = [j for j in range(len(tok)) if dono[j] == k]
            casados = [j for j in idx if j in mapa]
            if not casados:
                inicios.append(None); continue
            fim_ant, fim_trecho = fim_trecho, asr[mapa[casados[-1]]][2]
            j1 = casados[0]; t1 = asr[mapa[j1]][1] - 0.2 * (j1 - idx[0])
            j2 = next((x for x in casados[:4] if tok[x] not in CURTAS), j1); t2 = asr[mapa[j2]][1] - 0.2 * (j2 - idx[0])
            # o reconhecimento erra o tempo das palavras curtas; a fronteira real do trecho é a pausa real mais perto,
            # desde que ela venha depois do fim do trecho anterior
            perto = [p for p in silencios if min(t1, t2) - 0.5 <= p[1] <= max(t1, t2) + 0.3 and p[0] >= fim_ant - 0.15]
            if perto:  # depois da pausa, a fala começa na primeira voz (uma respiração no meio não conta)
                p = min(perto, key=lambda p: abs(p[1] - t1)); a0 = int(p[1] / 0.01)
                v = next((k for k in range(a0, min(len(voz), a0 + 100)) if voz[k] > lim_voz), a0)
                inicios.append(max(p[0], v * 0.01 - ANTES, 0.0))
            elif k == 0:
                inicios.append(t1)
            else:  # fala corrida: a troca vai para o vale de voz entre as palavras, conferido pelo reconhecimento
                ult = tok[max(j for j in range(len(tok)) if dono[j] == k - 1)] if k - 1 in dono else tok[idx[0]]
                inicios.append(corte_conferido(m, audio, voz, t1, ult, tok[idx[0]], tok[idx[1]] if len(idx) > 1 else None))
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
