"""Leitura única de cada base; grava arrays próprios (independente do npz do outro agente) e diagnósticos de tipo/None."""
import gzip, json, sys, collections, pickle
import numpy as np
base, rot, out = sys.argv[1:4]
with gzip.open(base, 'rt') as f:
    d = json.load(f)
diag = {'chaves': len(d)}
res = {}
for t in ('1', '2'):
    ks, cols = [], collections.defaultdict(list)
    tipos = collections.Counter(); nones = collections.Counter(); faltam = collections.Counter()
    for k, v in d.items():
        s = v.get(t)
        if s is None:
            faltam['sem_turno'] += 1; continue
        ks.append(k); tipos[str(s.get('tipo'))] += 1
        for c in ('apt', 'comp', 'L', 'R', 'O', 'B', 'N'):
            x = s.get(c)
            if x is None:
                nones[c] += 1; x = 0
            cols[c].append(int(x))
        cols['enc'].append(str(s.get('enc'))); cols['tipo'].append(str(s.get('tipo')))
    diag[t] = {'n': len(ks), 'tipos': dict(tipos), 'None_por_campo': dict(nones), 'faltam': dict(faltam)}
    res[t] = {'k': np.array(ks), **{c: np.array(v) for c, v in cols.items()}}
with open(out + f'/{rot}.pkl', 'wb') as f:
    pickle.dump(res, f, protocol=4)
print(rot, json.dumps(diag, ensure_ascii=False))
