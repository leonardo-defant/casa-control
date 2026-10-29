"""Conferência independente do D2 do L7: biometria por urna nos logs da amostra do 2º turno.
Leitura própria dos .jez (zip com logd.dat, e .jez aninhado em contingência). Conta por urna, no dia 25/10/2026:
habilitações, tipo de habilitação (todas as variantes), habilitação manual pelo mesário e votos computados."""
import collections, io, json, os, re, sys, zipfile
from multiprocessing import Pool

RAIZ = sys.argv[1]
SAIDA = sys.argv[2]
RX_MES = re.compile(r'^Mesário \S+ habilitou o eleitor')


def linhas(caminho):
    out = []
    z = zipfile.ZipFile(caminho)
    for n in z.namelist():
        if n.startswith('logd'):
            out.append(z.read(n).decode('latin1').splitlines())
        elif n.endswith('.jez'):
            try:
                zz = zipfile.ZipFile(io.BytesIO(z.read(n)))
                for m in zz.namelist():
                    if m.startswith('logd'):
                        out.append(zz.read(m).decode('latin1').splitlines())
            except zipfile.BadZipFile:
                out.append(['__BADZIP__'])
    return out


def um(args):
    raiz, logs = args
    uf, m, z, s = raiz.split('/arq/')[-1].split('/')
    k = f'{uf.upper()}|{int(m)}|{int(z)}|{int(s)}'
    c = collections.Counter()
    tipos = collections.Counter()
    for lg in sorted(logs):
        for bloco in linhas(os.path.join(raiz, lg)):
            for l in bloco:
                p = l.split('\t')
                if len(p) < 5 or not p[0].startswith('25/10/2026'):
                    continue
                msg = p[4]
                if msg == 'Eleitor foi habilitado':
                    c['hab'] += 1
                elif msg.startswith('Tipo de habilitação do eleitor'):
                    tipos[msg] += 1
                elif RX_MES.match(msg):
                    c['mesario_habilitou'] += 1
                elif msg == 'O voto do eleitor foi computado':
                    c['comp'] += 1
                elif msg.startswith('Solicita digital. Tentativa [1]'):
                    c['solicita_digital_1'] += 1
    c['n_arquivos_log'] = len(logs)
    return k, dict(c), dict(tipos)


def main():
    tarefas = []
    for raiz, dirs, arqs in os.walk(RAIZ):
        logs = [a for a in arqs if a.endswith('-log.jez')]
        if logs:
            tarefas.append((raiz, logs))
    with Pool(4) as P:
        res = P.map(um, tarefas, chunksize=20)
    out = {k: {'c': c, 'tipos': t} for k, c, t in res}
    json.dump(out, open(SAIDA, 'w'), ensure_ascii=False)
    print(len(out), 'urnas;', sum(1 for v in out.values() if v['c'].get('n_arquivos_log', 0) > 1), 'pastas com mais de 1 log')
    tt = collections.Counter()
    for v in out.values():
        tt.update(v['tipos'])
    print(tt.most_common())


if __name__ == '__main__':
    main()
