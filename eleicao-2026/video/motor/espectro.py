"""Espectro médio de longo prazo (LTAS) da fala, em bandas de 1/3 de oitava, só nos trechos com voz.
Cada curva sai normalizada pela energia total entre 100 Hz e 8 kHz (0 dB = toda a fala), para comparar a forma
(o equilíbrio grave x agudo) e não o volume.
Uso: python3 -I espectro.py [--json saida.json] <audio1> [<audio2> ...]
"""
import json, subprocess, sys
import numpy as np

TAXA = 48000
CENTROS = [50, 63, 80, 100, 125, 160, 200, 250, 315, 400, 500, 630, 800, 1000, 1250, 1600, 2000, 2500, 3150, 4000,
           5000, 6300, 8000, 10000, 12500, 16000]


def ler(arq):
    raw = subprocess.run(['ffmpeg', '-nostdin', '-loglevel', 'error', '-i', arq, '-ac', '1', '-ar', str(TAXA), '-f', 'f32le', '-'],
                         capture_output=True, check=True).stdout
    return np.frombuffer(raw, np.float32).astype(np.float64)


def ltas(a, n=8192):
    passo = n // 2; jan = np.hanning(n)
    quadros = np.lib.stride_tricks.sliding_window_view(a, n)[::passo] * jan
    pot = np.abs(np.fft.rfft(quadros, axis=1)) ** 2
    e = pot.sum(axis=1); edb = 10 * np.log10(e + 1e-20)
    ativo = edb > np.percentile(edb, 95) - 30  # só quadros com fala (tira silêncio e respiro fraco)
    return pot[ativo].mean(axis=0), np.fft.rfftfreq(n, 1 / TAXA), ativo.mean()


def bandas(p, f):
    out = []
    for c in CENTROS:
        lo, hi = c / 2 ** (1 / 6), c * 2 ** (1 / 6)
        out.append(p[(f >= lo) & (f < hi)].sum())
    out = np.array(out); ref = out[(np.array(CENTROS) >= 100) & (np.array(CENTROS) <= 8000)].sum()
    return 10 * np.log10(out / ref + 1e-20)


def medidas(p, f):
    def e(lo, hi): return p[(f >= lo) & (f < hi)].sum()
    sel = (f >= 80) & (f <= 12000)
    return {'centroide_hz': round(float((p[sel] * f[sel]).sum() / p[sel].sum())),
            'grave_100_500_db': round(10 * np.log10(e(100, 500) / e(100, 8000)), 1),
            'presenca_2k_5k_db': round(10 * np.log10(e(2000, 5000) / e(100, 8000)), 1),
            'ar_5k_10k_db': round(10 * np.log10(e(5000, 10000) / e(100, 8000)), 1)}


def main():
    args = sys.argv[1:]; saida = None
    if '--json' in args:
        i = args.index('--json'); saida = args[i + 1]; del args[i:i + 2]
    res = {}
    for arq in args:
        p, f, frac = ltas(ler(arq))
        res[arq] = {'bandas_db': [round(float(x), 2) for x in bandas(p, f)], 'fala_frac': round(float(frac), 2), **medidas(p, f)}
    nomes = [a.split('/')[-1][:18] for a in args]
    print('Hz     ' + ''.join(f'{n:>19}' for n in nomes))
    for k, c in enumerate(CENTROS):
        print(f'{c:>6} ' + ''.join(f'{res[a]["bandas_db"][k]:>19.1f}' for a in args))
    for m in ('centroide_hz', 'grave_100_500_db', 'presenca_2k_5k_db', 'ar_5k_10k_db'):
        print(f'{m:<18}' + ''.join(f'{res[a][m]:>14}' for a in args))
    if saida:
        json.dump({'centros_hz': CENTROS, 'curvas': res}, open(saida, 'w'), ensure_ascii=False, indent=1)


if __name__ == '__main__':
    main()
