"""Energia do fim de cada wav: dBFS das últimas janelas de 20 ms e silêncio final. Cortado = fim ainda com som."""
import array, math, subprocess, sys
for arq in sys.argv[1:]:
    raw = subprocess.run(['ffmpeg', '-loglevel', 'error', '-i', arq, '-ac', '1', '-ar', '16000', '-f', 's16le', '-'], capture_output=True).stdout
    a = array.array('h', raw); jan = 320
    env = [(sum(x * x for x in a[k:k + jan]) / jan) ** 0.5 for k in range(0, len(a) - jan, jan)]
    lim = max(env) * 0.03
    fim = len(env) - 1 - next(k for k, e in enumerate(reversed(env)) if e > lim)
    ult = [round(20 * math.log10(max(e, 1) / 32768)) for e in env[-4:]]
    sil = len(a) / 16000 - (fim + 1) * 0.02
    print(f'{arq.split("/")[-1]:<10} dur {len(a)/16000:6.2f}  silencio_final {sil:5.2f}  ultimos80ms {ult}  {"CORTADO" if max(ult) > -50 else "ok"}')
