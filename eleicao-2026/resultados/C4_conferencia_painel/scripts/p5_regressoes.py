"""Conferência PAINEL, passo 5: refazer, com a base nacional do próprio painel (Tabela Mestra v21, 497.885 seções,
campos de log conferidos contra os logs da amostra no passo 6), as contas por trás de "+15,6 pp dentro da mesma cidade",
"+8,8 pp dentro da mesma escola" e "+2.514.969 votos, controlado UF/porte".

Uso: python3 -I p5_regressoes.py <Painel_Tabela_Mestra_Auditoria_v21.html.gz> <secoes2026.json.gz> <saida.json>

Decisões fixadas antes de rodar (o painel não publica método; nada disto está no Adendo 24, tudo é desvio declarado):
  H1. y2 = L2/(L2+R2) da seção (base oficial, idêntica à tabela); y1 = L1/(L1+R1) do 1º turno na mesma seção (base
      oficial). Peso = L2+R2. Erro-padrão agrupado por município (UF + nome).
  H2. Composição do comparecimento do 2º turno pelos campos do painel: f_cm = cm2/c2 (mesário identificado),
      f_na = na2/c2 (digital gravada após o registro, "mesário substituto"), f_dn = dn2/c2 (órfã, "DigNova"),
      f_S = (c2 - b2 - cm2 - sm2)/c2 (sem digital cadastrada e resto); base omitida = biometria do eleitor (b2/c2).
      O coeficiente de f_dn é a diferença ecológica de fatia de Lula entre o voto liberado por órfã e o biométrico.
  H3. Modelos: M1 efeito fixo de município, sem 1º turno (a leitura mais próxima de "dentro da mesma cidade");
      M2 = M1 + y1; M3 efeito fixo de local de votação (UF, município, nr_local), sem y1 ("mesma escola");
      M4 = M3 + y1; M5 placebo: y1 contra as frações do 2º turno, efeito fixo de município.
  H4. "Controlado UF/porte": f_sb = (c2 - b2)/c2 (a definição de "sem biometria" que reproduz as faixas do painel),
      efeito fixo de UF x porte. Porte em duas leituras: (a) classe do município pelo comparecimento do 2º turno
      (até 10 mil, 10 a 50 mil, 50 a 200 mil, 200 mil a 1 milhão, mais de 1 milhão); (b) quintil nacional do
      comparecimento da seção. Saldo implícito = 2 x beta x soma de (c2 - b2) x (L2+R2)/c2 (votos válidos do bloco).
      M6a, M6b sem y1; M7a, M7b com y1.
  H5. Nenhum limiar: é reconstrução descritiva, sem veredito (o Adendo 24 não fixa critério para o painel).
"""
import gzip
import json
import re
import sys

import numpy as np


def ler(cam_tab, cam_base):
    src = gzip.open(cam_tab, 'rb').read().decode('utf-8', errors='replace')
    m = re.search(r'<script id="raw-data" type="text/plain">', src)
    corpo = src[m.end():src.find('</script>', m.end())].strip('\n')
    i = src.find('const DICT = ') + len('const DICT = ')
    D, _ = json.JSONDecoder().raw_decode(src, i)
    base = json.load(gzip.open(cam_base))
    idx = {}
    for k, v in base.items():
        uf, mun, z, s = k.split('|')
        idx[(uf, int(z), int(s))] = v
    rows = []
    for ln in corpo.split('\n'):
        p = ln.strip().split(',')
        if len(p) != 40:
            continue
        uf = D['ufs'][int(p[0])]
        v = idx[(uf, int(p[2]), int(p[3]))]
        s1, s2 = v.get('1'), v['2']
        L1 = s1['L'] if s1 else None
        R1 = s1['R'] if s1 else None
        rows.append((int(p[0]), int(p[1]), int(p[4]), int(p[9]), int(p[18]), int(p[22]), int(p[24]), int(p[25]),
                     int(p[26]), s2['L'], s2['R'], L1, R1, float(p[12])))
    return rows


def fe_wls(y, X, w, g, cl):
    """WLS com um efeito fixo (grupo g), erro agrupado por cl. Devolve beta, ep."""
    _, gi = np.unique(g, return_inverse=True)
    sw = np.bincount(gi, weights=w)
    def dm(v):
        mu = np.bincount(gi, weights=w * v) / sw
        return v - mu[gi]
    yd = dm(y)
    Xd = np.column_stack([dm(X[:, j]) for j in range(X.shape[1])])
    XtWX = Xd.T @ (Xd * w[:, None])
    b = np.linalg.solve(XtWX, Xd.T @ (w * yd))
    e = yd - Xd @ b
    _, ci = np.unique(cl, return_inverse=True)
    G = ci.max() + 1
    S = np.zeros((G, X.shape[1]))
    for j in range(X.shape[1]):
        S[:, j] = np.bincount(ci, weights=w * e * Xd[:, j], minlength=G)
    meat = S.T @ S
    inv = np.linalg.inv(XtWX)
    n, k = len(y), X.shape[1]
    corr = G / (G - 1) * (n - 1) / (n - k)
    V = corr * inv @ meat @ inv
    return b, np.sqrt(np.diag(V))


def main():
    rows = ler(sys.argv[1], sys.argv[2])
    a = np.array([[np.nan if x is None else x for x in r] for r in rows], dtype=float)
    uf, mun, loc, c2, b2, cm2, sm2, na2, dn2, L2, R2, L1, R1, p13_1 = [a[:, j] for j in range(14)]
    ok = (c2 > 0) & (L2 + R2 > 0) & ~np.isnan(L1) & (L1 + R1 > 0)
    R = {'n_total': int(len(a)), 'n_usadas': int(ok.sum())}
    y1_chk = 100 * L1 / (L1 + R1)
    R['p13_1_igual_H2H_1T_ate_0,01'] = int(np.sum(np.abs(y1_chk[ok] - p13_1[ok]) < 0.006))
    a = a[ok]
    uf, mun, loc, c2, b2, cm2, sm2, na2, dn2, L2, R2, L1, R1, p13_1 = [a[:, j] for j in range(14)]
    y2 = L2 / (L2 + R2)
    y1 = L1 / (L1 + R1)
    w = L2 + R2
    f_cm, f_na, f_dn = cm2 / c2, na2 / c2, dn2 / c2
    f_S = (c2 - b2 - cm2 - sm2) / c2
    gm = uf * 100000 + mun
    gl = gm * 100000 + loc
    X = np.column_stack([f_cm, f_na, f_dn, f_S])
    nomes = ['f_cm', 'f_na', 'f_dn', 'f_S']
    mods = {}
    for nome, yy, XX, g, nm in (
            ('M1_mun_sem_1T', y2, X, gm, nomes),
            ('M2_mun_com_1T', y2, np.column_stack([X, y1]), gm, nomes + ['y1']),
            ('M3_local_sem_1T', y2, X, gl, nomes),
            ('M4_local_com_1T', y2, np.column_stack([X, y1]), gl, nomes + ['y1']),
            ('M5_placebo_y1_mun', y1, X, gm, nomes),
            ('M5b_placebo_y1_local', y1, X, gl, nomes)):
        b, ep = fe_wls(yy, XX, w, g, gm)
        mods[nome] = {n_: [round(float(b[j]), 4), round(float(ep[j]), 4)] for j, n_ in enumerate(nm)}
    # H4: UF x porte
    f_sb = (c2 - b2) / c2
    comp_mun = {}
    for gg, cc in zip(gm, c2):
        comp_mun[gg] = comp_mun.get(gg, 0) + cc
    cm_arr = np.array([comp_mun[gg] for gg in gm])
    porte_a = np.digitize(cm_arr, [10000, 50000, 200000, 1000000])
    q = np.quantile(c2, [0.2, 0.4, 0.6, 0.8])
    porte_b = np.digitize(c2, q)
    validos_bloco = float(np.sum((c2 - b2) * (L2 + R2) / c2))
    R['soma_c2_menos_b2'] = float(np.sum(c2 - b2))
    R['validos_do_bloco'] = round(validos_bloco)
    for nome, porte, com in (('M6a_UFxporte_mun_sem_1T', porte_a, False), ('M6b_UFxquintil_secao_sem_1T', porte_b, False),
                             ('M7a_UFxporte_mun_com_1T', porte_a, True), ('M7b_UFxquintil_secao_com_1T', porte_b, True),
                             ('M8_mun_sem_1T', None, False), ('M9_local_com_1T', None, True)):
        if nome.startswith('M8'):
            g = gm
        elif nome.startswith('M9'):
            g = gl
        else:
            g = uf * 10 + porte
        XX = np.column_stack([f_sb, y1]) if com else f_sb[:, None]
        b, ep = fe_wls(y2, XX, w, g, gm)
        mods[nome] = {'f_sb': [round(float(b[0]), 4), round(float(ep[0]), 4)],
                      'saldo_implicito': round(2 * float(b[0]) * validos_bloco),
                      'saldo_ic95': [round(2 * float(b[0] - 1.96 * ep[0]) * validos_bloco),
                                     round(2 * float(b[0] + 1.96 * ep[0]) * validos_bloco)]}
        if com:
            mods[nome]['y1'] = [round(float(b[1]), 4), round(float(ep[1]), 4)]
    R['modelos'] = mods
    # contas ingênuas de nível: fatia de Lula ponderada pelos votos de cada tipo (sem efeito fixo)
    R['ingenua_fatia_ponderada'] = {k: round(float(np.sum(v * y2) / np.sum(v)), 4) for k, v in
                                    (('bio', b2), ('cm', cm2), ('na', na2), ('dn', dn2), ('S', c2 - b2 - cm2 - sm2))}
    R['ingenua_fatia_ponderada_1T'] = {k: round(float(np.sum(v * y1) / np.sum(v)), 4) for k, v in
                                       (('bio', b2), ('cm', cm2), ('na', na2), ('dn', dn2), ('S', c2 - b2 - cm2 - sm2))}
    json.dump(R, open(sys.argv[3], 'w'), ensure_ascii=False, indent=1)
    print(json.dumps(R, ensure_ascii=False, indent=1))


if __name__ == '__main__':
    main()
