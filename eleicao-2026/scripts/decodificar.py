"""Leitura dos arquivos de urna de 2026: boletim (-bu.dat), registro digital do voto (-rdv.dat) e log (-log.jez).

Estrutura inferida do BER e validada contra o bweb do 1º turno (mesmas seções).
BU, tipo de voto: 1 nominal, 2 branco, 3 nulo. RDV, tipo de voto: 2 nominal, 3 branco, 4 nulo (com os dígitos digitados).
"""
import collections, re, zipfile
from ber import parse

ELEICOES_PRES = {6257, 6258}
ESQ, DIR = 13, 22


def _int(v):
    return int.from_bytes(v, 'big', signed=False)


def _filhos(no):
    return no[2] if isinstance(no[2], list) else []


def ler_bu(caminho):
    env = parse(open(caminho, 'rb').read())[0][2]
    octet = [n for n in env if (n[0], n[1]) == (0, 4)][-1][2]
    bu = parse(octet)[0][2]
    out = {'eleicoes': {}}
    # identificação da seção: SEQ { SEQ{mun, zona}, INT local, INT secao }
    for n in bu:
        if (n[0], n[1]) == (0, 16) and len(_filhos(n)) == 3 and (_filhos(n)[0][0], _filhos(n)[0][1]) == (0, 16) \
                and all((c[0], c[1]) == (0, 2) for c in _filhos(n)[1:]):
            mz = _filhos(_filhos(n)[0])
            out['mun'], out['zona'] = _int(mz[0][2]), _int(mz[1][2])
            out['loc'], out['secao'] = _int(_filhos(n)[1][2]), _int(_filhos(n)[2][2])
    # urna: SEQ{ ENUM, STR versao, SEQ correspondencia{ [2:0], SEQ carga{ INT numeroInterno, ...}}, ...}
    urna = bu[2][2]
    out['versao'] = urna[1][2].decode('latin1')
    corr = urna[2][2]
    out['urna'] = _int(corr[1][2][0][2])
    # abertura e encerramento: [2:0]{STR, STR}
    for n in bu:
        if (n[0], n[1]) == (2, 0) and len(_filhos(n)) == 2 and all(c[1] == 27 for c in _filhos(n)):
            out['ab'], out['enc'] = (c[2].decode() for c in _filhos(n))
    # resultados por eleição
    for n in bu:
        if (n[0], n[1]) != (0, 16):
            continue
        for el in _filhos(n):
            f = _filhos(el) if isinstance(el[2], list) else []
            if len(f) < 5 or (f[0][0], f[0][1]) != (0, 2):
                continue
            ide = _int(f[0][2])
            if ide < 6000 or ide > 7000:
                continue
            rec = {'apt': _int(f[1][2]), 'cargos': {}}
            for rv in _filhos(f[4]):  # resultadosVotacao
                g = _filhos(rv)
                comp = _int(g[1][2])
                for tc in _filhos(g[2]):  # totaisVotosCargo
                    h = _filhos(tc)
                    cargo = _int(h[0][2])
                    votos = collections.Counter()
                    for vv in _filhos(h[2]):
                        e = _filhos(vv)
                        tipo = _int(e[0][2]); q = _int(e[1][2])
                        cand = None
                        for x in e[2:]:
                            if (x[0], x[1]) == (2, 3):
                                cand = _int(_filhos(x)[1][2])
                        votos[(tipo, cand)] += q
                    rec['cargos'][cargo] = {'comp': comp, 'votos': votos}
            out['eleicoes'][ide] = rec
    return out


def bu_para_secao(b):
    """Converte para o formato das bases (L, R, O, B, N, comp, apt; e governador B, N, V, comp)."""
    s = g = None
    for ide, rec in b['eleicoes'].items():
        for cargo, c in rec['cargos'].items():
            v = c['votos']
            if cargo == 1:
                s = {'loc': b.get('loc'), 'urna': b['urna'], 'apt': rec['apt'], 'comp': c['comp'],
                     'ab': b.get('ab', '')[-6:], 'enc': b.get('enc', '')[-6:],
                     'L': sum(q for (t, n), q in v.items() if t == 1 and n == ESQ),
                     'R': sum(q for (t, n), q in v.items() if t == 1 and n == DIR),
                     'O': sum(q for (t, n), q in v.items() if t == 1 and n not in (ESQ, DIR)),
                     'B': sum(q for (t, n), q in v.items() if t == 2),
                     'N': sum(q for (t, n), q in v.items() if t == 3),
                     'tipos_extra': sorted({t for (t, n) in v if t not in (1, 2, 3)})}
            elif cargo == 3:
                g = {'B': sum(q for (t, n), q in v.items() if t == 2), 'N': sum(q for (t, n), q in v.items() if t == 3),
                     'V': sum(q for (t, n), q in v.items() if t not in (2, 3)), 'comp': c['comp']}
    return s, g


def ler_rdv(caminho):
    """Contagem por (eleição, cargo, tipo, dígitos) no RDV."""
    top = parse(open(caminho, 'rb').read())[0][2]
    rdv = top[2][2]
    els = [n for n in rdv if (n[0], n[1]) == (2, 1)][0][2]
    out = collections.Counter()
    for el in els:
        f = _filhos(el)
        ide = _int(f[0][2])
        for cargo in _filhos(f[1]):
            h = _filhos(cargo)
            cod = _int(h[0][2])
            for voto in _filhos(h[2]):
                e = _filhos(voto)
                tipo = _int(e[0][2]); dig = e[1][2].decode() if len(e) > 1 else ''
                out[(ide, cod, tipo, dig)] += 1
    return out


def rdv_para_bu(c):
    """Converte a contagem do RDV para o mesmo formato de bu_para_secao (presidente e governador)."""
    res = {}
    for (ide, cod, tipo, dig), q in c.items():
        r = res.setdefault(cod, collections.Counter())
        if tipo == 2:
            n = int(dig)
            r['L' if (cod == 1 and n == ESQ) else 'R' if (cod == 1 and n == DIR) else 'O' if cod == 1 else 'V'] += q
        elif tipo == 3: r['B'] += q
        elif tipo == 4: r['N'] += q
        else: r[f'tipo{tipo}'] += q
        r['total'] += q
    return res


RX = re.compile(r'^(\d\d/\d\d/\d{4}) (\d\d):(\d\d):(\d\d)$')


def ler_log(caminho, data):
    """Métricas do pré-registro (T3) para o dia da eleição `data` (dd/mm/aaaa)."""
    z = zipfile.ZipFile(caminho)
    nome = [n for n in z.namelist() if n.startswith('logd')][0]
    linhas = z.read(nome).decode('latin1').splitlines()
    ev = []
    for l in linhas:
        p = l.split('\t')
        if len(p) < 5 or not p[0].startswith(data):
            continue
        m = RX.match(p[0])
        if not m:
            continue
        t = int(m.group(2)) * 3600 + int(m.group(3)) * 60 + int(m.group(4))
        ev.append((t, p[3], p[4]))
    out = {'n_eventos': len(ev), 'urnas_no_log': len({l.split('\t')[2] for l in linhas if l.count('\t') >= 4 and l.startswith(data)})}
    pronta = [t for t, a, m in ev if m == 'Urna pronta para receber votos']
    enc = [t for t, a, m in ev if m.startswith('Inicio do Encerramento') or m.startswith('Início do Encerramento')]
    comp = [t for t, a, m in ev if m == 'O voto do eleitor foi computado']
    out['computados'] = len(comp)
    out['habilitados'] = sum(1 for t, a, m in ev if m == 'Eleitor foi habilitado')
    out['pronta'] = pronta[0] if pronta else None
    out['encerramento'] = enc[-1] if enc else None
    out['A2_antes'] = sum(1 for t in comp if pronta and t < pronta[0])
    out['A2_depois'] = sum(1 for t in comp if enc and t > enc[-1])
    # A3 e A4: percorre a sequência
    hab_pend = None; a3 = 0; a4 = 0; dur = []
    for t, a, m in ev:
        if m == 'Eleitor foi habilitado':
            hab_pend = t
        elif m == 'O voto do eleitor foi computado':
            if hab_pend is None:
                a3 += 1
            else:
                dur.append(t - hab_pend)
                if t - hab_pend < 2:
                    a4 += 1
            hab_pend = None
    out['A3_sem_habilitacao'] = a3
    out['A4_menos_2s'] = a4
    # A5: rajadas de 10+ votos com menos de 15 s entre votos computados
    run = 1; a5 = 0; maior = 1
    for i in range(1, len(comp)):
        if comp[i] - comp[i - 1] < 15:
            run += 1
        else:
            if run >= 10: a5 += 1
            run = 1
        maior = max(maior, run)
    if run >= 10: a5 += 1
    out['A5_rajadas'] = a5
    out['maior_sequencia_rapida'] = maior
    dur.sort()
    out['dur_mediana'] = dur[len(dur) // 2] if dur else None
    out['dur_min'] = dur[0] if dur else None
    out['primeiro_voto'] = comp[0] if comp else None
    out['ultimo_voto'] = comp[-1] if comp else None
    out['msgs_contingencia'] = sum(1 for t, a, m in ev if 'conting' in m.lower() or 'substitu' in m.lower() or 'cédula' in m.lower())
    out['erros'] = sum(1 for l in linhas if l.startswith(data) and '\tERRO\t' in l)
    return out
