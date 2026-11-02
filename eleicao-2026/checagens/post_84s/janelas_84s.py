"""Checagem do post de Felipe Cecílio: "crescimento sistemático dos votos de Lula ... matematicamente impossível
durante um intervalo de 84,7 segundos da apuração".

Método fixado antes de olhar os resultados das janelas:
- Fila da apuração: cada seção entra na hora em que o TSE recebeu o boletim (DT_BU_RECEBIDO, hora de Brasília),
  com os votos de presidente de Lula (13) e Flávio (22). Exterior incluído.
- Janelas de 84,7 s começando em cada segundo com boletim recebido. Em cada janela: boletins, votos, fatia de Lula
  entre os dois, fatia acumulada antes da janela e depois dela (o "crescimento" visto no placar), e a fatia das MESMAS
  seções no 1º turno.
- z ingênuo: (fatia da janela - fatia acumulada antes) / raiz(p(1-p)/votos da janela), tratando cada voto como
  sorteio independente (é a conta que gera o "impossível").
- z pela virada: (virada da janela - virada nacional) / (desvio-padrão da virada por seção / raiz(seções)), com a
  virada = fatia no 2º turno - fatia no 1º turno das mesmas seções. Mede se as seções da janela mudaram mais que as
  outras, que é o que uma fraude no fluxo deixaria.
- Controle: as mesmas janelas no 1º turno (só z ingênuo, para Lula e para Flávio), sem prorrogação e com Flávio
  vencendo.
Uso: python3 -I janelas_84s.py <zips2t> <zips1t> <secoes2026.json.gz> <saida.json>
"""
import csv, glob, gzip, io, json, math, statistics, sys, zipfile
from datetime import datetime

JAN = 84.7


def ler(pasta, turno):
    """Seção -> (segundos desde 00:00 do dia da votação, L, R) para presidente. Filtra as linhas de presidente em bytes."""
    sec = {}
    for zp in sorted(glob.glob(f'{pasta}/*.zip')):
        z = zipfile.ZipFile(zp)
        nome = [n for n in z.namelist() if n.endswith('.csv')][0]
        f = z.open(nome)
        h = next(csv.reader([f.readline().decode('latin1')], delimiter=';')); ix = {c: i for i, c in enumerate(h)}
        for linha in f:
            if b';"Presidente";' not in linha:
                continue
            r = next(csv.reader([linha.decode('latin1')], delimiter=';'))
            if r[ix['CD_CARGO_PERGUNTA']] != '1':
                continue
            k = f"{r[ix['SG_UF']]}|{int(r[ix['CD_MUNICIPIO']])}|{int(r[ix['NR_ZONA']])}|{int(r[ix['NR_SECAO']])}"
            if k not in sec:
                t = datetime.strptime(r[ix['DT_BU_RECEBIDO']], '%Y-%m-%d %H:%M:%S')
                dia = 4 if turno == 1 else 25
                sec[k] = [(t.day - dia) * 86400 + t.hour * 3600 + t.minute * 60 + t.second, 0, 0]
            v = r[ix['NR_VOTAVEL']]; q = int(r[ix['QT_VOTOS']])
            if v == '13':
                sec[k][1] += q
            elif v == '22':
                sec[k][2] += q
    return sec


def hms(s):
    s = int(s)
    return f'{s // 3600:02d}:{s % 3600 // 60:02d}:{s % 60:02d}'


def janelas(fila, alvo_idx, sw=None, sw_nat=None, sd_sw=None):
    """fila ordenada por tempo: (t, L, R, virada?). Devolve a lista de janelas com métricas."""
    n = len(fila); j = 0; out = []
    cumL = [0] * (n + 1); cumR = [0] * (n + 1); cumV = [0.0] * (n + 1); cumN = [0] * (n + 1)
    for i, x in enumerate(fila):
        cumL[i + 1] = cumL[i] + x[1]; cumR[i + 1] = cumR[i] + x[2]
        cumV[i + 1] = cumV[i] + (x[3] if x[3] is not None else 0.0); cumN[i + 1] = cumN[i] + (x[3] is not None)
    i = 0
    while i < n:
        t0 = fila[i][0]
        while j < n and fila[j][0] < t0 + JAN:
            j += 1
        wl = cumL[j] - cumL[i]; wr = cumR[j] - cumR[i]
        al, ar = cumL[i], cumR[i]
        if wl + wr > 0 and al + ar > 0:
            p = al / (al + ar); fw = wl / (wl + wr)
            z = (fw - p) / math.sqrt(p * (1 - p) / (wl + wr))
            depois = (al + wl) / (al + ar + wl + wr)
            o = {'inicio': hms(t0), 'boletins': j - i, 'votos': wl + wr, 'fatia_janela': round(100 * fw, 2),
                 'acumulado_antes': round(100 * p, 3), 'acumulado_depois': round(100 * depois, 3),
                 'crescimento_placar_pts': round(100 * (depois - p), 3), 'z_ingenuo': round(z, 1)}
            if sw is not None:
                nv = cumN[j] - cumN[i]
                if nv:
                    mv = (cumV[j] - cumV[i]) / nv
                    o['virada_media'] = round(mv, 2)
                    o['z_virada'] = round((mv - sw_nat) / (sd_sw / math.sqrt(nv)), 2)
            out.append(o)
        # próxima janela começa no próximo segundo com boletim
        t = fila[i][0]
        while i < n and fila[i][0] == t:
            i += 1
    return out


def main():
    z2, z1, basef, saida = sys.argv[1:5]
    s2 = ler(z2, 2); s1 = ler(z1, 1)
    base = json.load(gzip.open(basef))
    viradas = []
    fila2 = []
    for k, (t, l, r) in s2.items():
        v = None
        b = base.get(k, {}).get('1')
        if b and b['L'] + b['R'] > 0 and l + r > 0:
            v = 100 * l / (l + r) - 100 * b['L'] / (b['L'] + b['R']); viradas.append(v)
        fila2.append((t, l, r, v))
    fila2.sort()
    sw_nat = statistics.mean(viradas); sd_sw = statistics.pstdev(viradas)
    w2 = janelas(fila2, 1, True, sw_nat, sd_sw)
    fila1 = sorted((t, l, r, None) for k, (t, l, r) in s1.items())
    w1 = janelas(fila1, 1)
    def top(ws, chave, n=5, rev=True):
        return sorted(ws, key=lambda o: o[chave], reverse=rev)[:n]
    tot2 = sum(x[1] for x in fila2), sum(x[2] for x in fila2)
    out = {
        'boletins_2t': len(fila2), 'boletins_1t': len(fila1),
        'lula_flavio_2t': tot2, 'primeiro_e_ultimo_2t': [hms(fila2[0][0]), hms(fila2[-1][0])],
        'virada_nacional_media_por_secao': round(sw_nat, 3), 'dp_virada_por_secao': round(sd_sw, 3),
        'janelas_2t': len(w2),
        'janelas_2t_com_z_ingenuo_acima_de_5': sum(1 for o in w2 if o['z_ingenuo'] > 5),
        'janelas_2t_com_z_ingenuo_abaixo_de_menos_5': sum(1 for o in w2 if o['z_ingenuo'] < -5),
        'janelas_1t_com_z_ingenuo_acima_de_5': sum(1 for o in w1 if o['z_ingenuo'] > 5),
        'janelas_1t_com_z_ingenuo_abaixo_de_menos_5': sum(1 for o in w1 if o['z_ingenuo'] < -5),
        'janelas_2t_com_z_virada_acima_de_4': sum(1 for o in w2 if o.get('z_virada', 0) > 4 and o['boletins'] >= 30),
        'janelas_2t_com_z_virada_abaixo_de_menos_4': sum(1 for o in w2 if o.get('z_virada', 0) < -4 and o['boletins'] >= 30),
        'top_crescimento_placar_2t': top([o for o in w2 if o['inicio'] >= '17:30:00'], 'crescimento_placar_pts'),
        'top_z_ingenuo_2t_depois_das_19h': top([o for o in w2 if o['inicio'] >= '19:00:00'], 'z_ingenuo'),
        'top_z_ingenuo_1t_lula': top([o for o in w1 if o['acumulado_antes'] > 0], 'z_ingenuo'),
        'top_z_ingenuo_1t_flavio': top([o for o in w1 if o['acumulado_antes'] > 0], 'z_ingenuo', rev=False),
        'top_z_virada_2t': top([o for o in w2 if o['boletins'] >= 30 and 'z_virada' in o], 'z_virada'),
        'primeira_janela_apos_retomada_19h': next((o for o in w2 if o['inicio'] >= '19:03:00'), None),
    }
    json.dump(out, open(saida, 'w'), ensure_ascii=False, indent=1)
    print(json.dumps(out, ensure_ascii=False, indent=1))


if __name__ == '__main__':
    main()
