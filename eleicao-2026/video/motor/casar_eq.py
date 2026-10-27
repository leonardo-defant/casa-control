"""Equalização por casamento de curva ("match EQ"): calcula o ganho por banda de 1/3 de oitava que leva o espectro
médio da voz (medido com espectro.py) até uma curva alvo, e grava a cadeia de filtros do ffmpeg (firequalizer, de fase
linear) num arquivo de texto que montar_plano.py usa com --eq.
O ganho é limitado (padrão ±9 dB) e suavizado entre bandas vizinhas; acima do limite de banda da voz (onde não há
sinal para realçar) não há reforço: o brilho ali vem do excitador, que gera harmônicos a partir do que existe.
Uso: python3 -I casar_eq.py <espectro_voz.json> <chave_voz> <alvo.json> <saida_filtro.txt> [--limite 9] [--ar -6] [--anterior filtro.txt]
alvo.json: {"centros_hz": [...], "alvo_db": [...]} na mesma normalização de espectro.py (0 dB = fala de 100 Hz a 8 kHz).
--anterior: soma os ganhos de uma rodada anterior (para refinar medindo a voz já equalizada).
"""
import json, re, sys
import numpy as np

PRE = 'highpass=f=60:p=2'
# "ar": copia a banda de 5,4 a 10,8 kHz uma oitava acima (replicação de banda, como no HE-AAC), porque a voz gerada
# não tem nada acima de ~11 kHz; o nível sai de --ar (dB)
AR = ('asplit=2[seco][ar];[ar]highpass=f=5500:p=2,highpass=f=5500:p=2,lowpass=f=10800:p=2,lowpass=f=10800:p=2,'
      'afreqshift=shift=5400,highpass=f=11000:p=2,highpass=f=11000:p=2,lowpass=f=12500:p=2,lowpass=f=12500:p=2,'
      'volume={db}dB[ar2];[seco][ar2]amix=inputs=2:normalize=0')  # o passa-baixas imita a queda natural acima de 12 kHz
POS = ('acompressor=threshold=-22dB:ratio=2.5:attack=10:release=160:makeup=2,'
       'deesser=i=0.3')


def main():
    voz_arq, chave, alvo_arq, saida = sys.argv[1:5]
    lim = float(sys.argv[sys.argv.index('--limite') + 1]) if '--limite' in sys.argv else 9.0
    voz = json.load(open(voz_arq)); alvo = json.load(open(alvo_arq))
    c = np.array(voz['centros_hz'], float); v = np.array(voz['curvas'][chave]['bandas_db'])
    a = np.interp(np.log(c), np.log(np.array(alvo['centros_hz'], float)), np.array(alvo['alvo_db']))
    g = a - v
    usa = (c >= 63) & (c <= 10000)  # fora disso: abaixo é o passa-altas; acima não há voz para realçar
    g[~usa] = 0.0
    g = np.clip(g, -lim, lim)
    gs = g.copy()
    for k in range(1, len(g) - 1):  # suaviza (1/4, 1/2, 1/4) para não criar picos estreitos
        gs[k] = 0.25 * g[k - 1] + 0.5 * g[k] + 0.25 * g[k + 1]
    gs[~usa] = 0.0
    if '--anterior' in sys.argv:
        ant = open(sys.argv[sys.argv.index('--anterior') + 1]).read()
        prev = dict((float(f), float(d)) for f, d in re.findall(r'entry\(([\d.]+),([-\d.]+)\)', ant))
        gs = np.clip(np.array([prev.get(float(f), 0.0) for f in c]) + gs, -lim - 3, lim + 3)
    entradas = ';'.join(f'entry({int(f)},{x:.2f})' for f, x in zip(c, gs))
    # FIR de fase linear com 50 ms de atraso: o atrim tira esse atraso para a fala não sair do lugar (o áudio é 48 kHz)
    fir = (f"firequalizer=gain_entry='entry(20,0);{entradas};entry(20000,{gs[-1]:.2f})':delay=0.05:wfunc=hann,"
           "atrim=start_sample=2400,asetpts=N/SR/TB")
    ar = float(sys.argv[sys.argv.index('--ar') + 1]) if '--ar' in sys.argv else -6.0
    open(saida, 'w').write(f'{PRE},{fir},{AR.format(db=ar)},{POS}\n')
    print('ganho por banda (dB):')
    for f, x, vv, aa in zip(c, gs, v, a):
        print(f'{int(f):>6} Hz  voz {vv:6.1f}  alvo {aa:6.1f}  ganho {x:+5.1f}')


if __name__ == '__main__':
    main()
