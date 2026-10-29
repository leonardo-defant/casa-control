"""Seções com zero voto para um finalista: 2026 (1º e 2º turno), 2022 e 2018 (2º turno), e quantas ficam em
aldeia/escola indígena (nome do local de votação no cadastro de 2026)."""
import csv, glob, re, sys, collections
sys.path.insert(0, '/home/user/casa-control/eleicao-2026/scripts')
from lib import carregar
S = sys.argv[1]
nome = {}
for f in glob.glob(f'{S}/locais_votacao/eleitorado_local_votacao_2026_*.csv'):
    for r in csv.DictReader(open(f, encoding='latin1'), delimiter=';'):
        nome[f"{r['SG_UF']}|{int(r['CD_MUNICIPIO'])}|{int(r['NR_ZONA'])}|{int(r['NR_SECAO'])}"] = r['NM_LOCAL_VOTACAO']
ind = re.compile(r'ALDEIA|IND[IÍ]GENA|INDIGENA|TERRA IND|POVO ', re.I)
def norm(k):
    uf, m, z, s = k.split('|'); return f'{uf}|{int(m)}|{int(z)}|{int(s)}'
def contar(base, turno, rot):
    d = carregar(base); z = {'R0': [], 'L0': []}
    for k, v in d.items():
        t = v.get(turno)
        if not t or t.get('comp', 0) < 1: continue
        if t['R'] == 0 and t['L'] > 0: z['R0'].append((k, t))
        if t['L'] == 0 and t['R'] > 0: z['L0'].append((k, t))
    for lado in ('R0', 'L0'):
        xs = z[lado]; n_ind = sum(1 for k, _ in xs if ind.search(nome.get(norm(k), '')))
        votos = sum(t['L'] if lado == 'R0' else t['R'] for _, t in xs)
        ufs = collections.Counter(k.split('|')[0] for k, _ in xs).most_common(6)
        print(f'{rot}: seções com {"direita" if lado=="R0" else "esquerda"} zerada: {len(xs)} | votos do outro nelas: {votos} | em local indígena (cadastro 2026): {n_ind} | UFs: {ufs}')
    return d, z
d26, z2 = contar(f'{S}/trab2t/secoes2026.json.gz', '2', '2026 2º turno (Lula x Flávio)')
_, z1 = contar(f'{S}/trab2t/secoes2026.json.gz', '1', '2026 1º turno (Lula x Flávio)')
contar(f'{S}/dados2t/secoes2022.json.gz', '2', '2022 2º turno (Lula x Bolsonaro)')
contar(f'{S}/dados2t/secoes2018.json.gz', '2', '2018 2º turno (Haddad x Bolsonaro)')
# as 2º turno 2026 com Flávio zerado: quanto ele tinha no 1º turno nessas mesmas seções
r1 = [d26[k]['1']['R'] for k, _ in z2['R0'] if '1' in d26[k]]
print('Flávio no 1º turno nas seções em que zerou no 2º: soma', sum(r1), '| seções onde já tinha 0 no 1º:', sum(1 for x in r1 if x == 0), 'de', len(r1), '| máximo', max(r1) if r1 else None)
