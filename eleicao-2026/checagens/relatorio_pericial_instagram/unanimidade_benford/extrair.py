"""Lê cada base por seção uma única vez e grava arrays compactos (npz) por ano e turno.
Uso: python3 -I extrair.py <base.json.gz> <rotulo> <pasta_saida>"""
import gzip, json, sys, os
import numpy as np

base, rot, out = sys.argv[1:4]
with gzip.open(base, 'rt') as f:
    d = json.load(f)
for t in ('1', '2'):
    ks = []; cols = {c: [] for c in ('apt', 'comp', 'L', 'R', 'O', 'B', 'N', 'loc')}; tipo = []; enc = []
    for k, v in d.items():
        s = v.get(t)
        if s is None:
            continue
        ks.append(k)
        for c in cols:
            x = s.get(c, 0)
            cols[c].append(-1 if x is None else int(x))
        tipo.append(str(s.get('tipo')))
        enc.append(str(s.get('enc')))
    np.savez_compressed(os.path.join(out, f'{rot}_t{t}.npz'), chave=np.array(ks), tipo=np.array(tipo), enc=np.array(enc),
                        **{c: np.array(cols[c], dtype=np.int64) for c in cols})
    print(rot, t, len(ks), {c: int(np.sum(cols[c])) for c in ('comp', 'L', 'R', 'O', 'B', 'N')}, flush=True)
