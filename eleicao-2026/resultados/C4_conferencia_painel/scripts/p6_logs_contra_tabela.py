"""Conferência PAINEL, passo 6: contar, nos logs da amostra (3.897 pacotes do 2º turno), os tipos de habilitação do dia
25/10/2026 e comparar seção a seção com os campos da Tabela Mestra v21 do painel (b2, cm2, na2, dn2, c2).

Uso: python3 -I p6_logs_contra_tabela.py <pasta amostra2t/arq> <Painel_Tabela_Mestra_Auditoria_v21.html.gz> <saida.json>

Leitor próprio (zipfile da biblioteca padrão), sem decodificar.py nem resultados de outros agentes.
Decisões fixadas antes de rodar:
  G1. Só linhas datadas de 25/10/2026, aplicação VOTA. Se o .jez trouxer mais de um logd (ou um zip aninhado), somo
      todos os logd.dat do pacote para o dia 25/10 (contingência).
  G2. Contagens por seção: VOT = "O voto do eleitor foi computado"; BIO = "Tipo de habilitação do eleitor [biométrica]";
      MI = "Mesário N habilitou o eleitor"; DG = "Digital coletada bate com uma digital gravada após o registro inicial
      de mesário..."; OR = "Não encontrou digital coletada em nenhum dos arquivos, vai salvar a digital em novo arquivo.";
      HAB = "Eleitor foi habilitado".
  G3. Hipótese a testar (não suposta): b2 = BIO, cm2 = MI, na2 = DG, dn2 = OR, c2 = VOT. Conto igualdade exata e somas.
  G4. Para cada OR, guardo o maior "Batimento de digitais retornou o score N" entre o "Solicita digital do mesário"
      anterior e o OR (score do 5º toque), para ver o que o painel chama de "score zero".
"""
import glob
import gzip
import io
import json
import os
import re
import sys
import zipfile
from collections import Counter


def logs_do_pacote(cam):
    out = []
    z = zipfile.ZipFile(cam)
    for nm in z.namelist():
        dado = z.read(nm)
        if nm.lower().endswith('.dat'):
            out.append(dado)
        elif dado[:2] == b'PK':
            z2 = zipfile.ZipFile(io.BytesIO(dado))
            for nm2 in z2.namelist():
                if nm2.lower().endswith('.dat'):
                    out.append(z2.read(nm2))
    return out


def contar(cam):
    c = Counter()
    scores_or = []
    for dado in logs_do_pacote(cam):
        t = dado.decode('latin-1')
        ultimo_score = None
        em_mesario = False
        for ln in t.split('\n'):
            p = ln.split('\t')
            if len(p) < 5 or not p[0].startswith('25/10/2026') or p[3] != 'VOTA':
                continue
            m = p[4]
            if m.startswith('O voto do eleitor foi computado'):
                c['VOT'] += 1
            elif m.startswith('Tipo de habilitação do eleitor [biométrica]'):
                c['BIO'] += 1
            elif re.match(r'Mesário \d+ habilitou o eleitor', m):
                c['MI'] += 1
            elif m.startswith('Digital coletada bate com uma digital gravada após o registro inicial'):
                c['DG'] += 1
            elif m.startswith('Não encontrou digital coletada em nenhum dos arquivos'):
                c['OR'] += 1
                scores_or.append(ultimo_score)
            elif m.startswith('Eleitor foi habilitado'):
                c['HAB'] += 1
            if m.startswith('Solicita digital do mesário'):
                em_mesario = True
                ultimo_score = None
            elif em_mesario and m.startswith('Batimento de digitais retornou o score'):
                v = int(re.search(r'score (\d+)', m).group(1))
                ultimo_score = v if ultimo_score is None else max(ultimo_score, v)
            elif m.startswith('O voto do eleitor foi computado'):
                em_mesario = False
    return c, scores_or


def ler_tabela(cam):
    src = gzip.open(cam, 'rb').read().decode('utf-8', errors='replace')
    m = re.search(r'<script id="raw-data" type="text/plain">', src)
    corpo = src[m.end():src.find('</script>', m.end())].strip('\n')
    i = src.find('const DICT = ') + len('const DICT = ')
    dicio, _ = json.JSONDecoder().raw_decode(src, i)
    tab = {}
    for ln in corpo.split('\n'):
        p = ln.strip().split(',')
        if len(p) != 40:
            continue
        uf = dicio['ufs'][int(p[0])].lower()
        tab[(uf, int(p[2]), int(p[3]))] = {'c2': int(p[9]), 'b2': int(p[18]), 'cm2': int(p[22]), 'sm2': int(p[24]),
                                          'na2': int(p[25]), 'dn2': int(p[26]), 't4_2': int(p[21])}
    return tab


def main():
    tab = ler_tabela(sys.argv[2])
    fs = sorted(glob.glob(os.path.join(sys.argv[1], '*', '*', '*', '*', '*-log.jez')))
    pares = {'b2': 'BIO', 'cm2': 'MI', 'na2': 'DG', 'dn2': 'OR', 'c2': 'VOT'}
    igual = Counter()
    soma_tab = Counter()
    soma_log = Counter()
    dif_ex = {k: [] for k in pares}
    sem_tab = []
    n = 0
    sc = Counter()
    for f in fs:
        nome = os.path.basename(f)
        mm = re.search(r'o03221([a-z]{2})(\d{5})(\d{4})(\d{4})-log', nome)
        uf, mun, zona, secao = mm.group(1), mm.group(2), int(mm.group(3)), int(mm.group(4))
        c, scores = contar(f)
        for s in scores:
            sc['sem_linha' if s is None else ('0' if s == 0 else ('1-9' if s < 10 else ('10-19' if s < 20 else '20+')))] += 1
        t = tab.get((uf, zona, secao))
        if t is None:
            sem_tab.append(nome)
            continue
        n += 1
        for kt, kl in pares.items():
            soma_tab[kt] += t[kt]
            soma_log[kl] += c[kl]
            if t[kt] == c[kl]:
                igual[kt] += 1
            elif len(dif_ex[kt]) < 6:
                dif_ex[kt].append([nome, t[kt], c[kl]])
        soma_tab['sm2'] += t['sm2']
        soma_tab['t4_2'] += t['t4_2']
        soma_log['HAB'] += c['HAB']
    R = {'pacotes': len(fs), 'na_tabela': n, 'sem_tabela': sem_tab[:20], 'n_sem_tabela': len(sem_tab),
         'iguais_por_campo': dict(igual), 'soma_tabela': dict(soma_tab), 'soma_log': dict(soma_log),
         'exemplos_diferenca': dif_ex, 'score_maximo_antes_do_OR': dict(sc)}
    json.dump(R, open(sys.argv[3], 'w'), ensure_ascii=False, indent=1)
    print(json.dumps(R, ensure_ascii=False, indent=1))


if __name__ == '__main__':
    main()
