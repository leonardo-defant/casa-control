"""Conferência PAINEL, passo 9: sensibilidade da reconstrução do +15,6 (M1 do passo 5) a escolhas que o painel não
publica: sem f_S; sem peso; e as mesmas com o 1º turno como controle. Decisão fixada antes de rodar: só estas quatro
variantes, efeito fixo de município, erro agrupado por município.
Uso: python3 -I p9_variantes_M1.py <tabela.html.gz> <secoes2026.json.gz>
"""
import json, sys
sys.path.insert(0, '/home/user/trabalho-eleicao/conferencia_adendo24/PAINEL/scripts')
import numpy as np
from p5_regressoes import ler, fe_wls
a = np.array([[np.nan if x is None else x for x in r] for r in ler(sys.argv[1], sys.argv[2])], dtype=float)
uf, mun, loc, c2, b2, cm2, sm2, na2, dn2, L2, R2, L1, R1, p13_1 = [a[:, j] for j in range(14)]
y2 = L2 / (L2 + R2); y1 = L1 / (L1 + R1); w = L2 + R2; gm = uf * 100000 + mun
X3 = np.column_stack([cm2 / c2, na2 / c2, dn2 / c2])
out = {}
for nome, XX, ww in (('sem_fS_peso', X3, w), ('sem_fS_sem_peso', X3, np.ones_like(w)),
                     ('sem_fS_peso_com1T', np.column_stack([X3, y1]), w),
                     ('sem_fS_sem_peso_com1T', np.column_stack([X3, y1]), np.ones_like(w))):
    b, ep = fe_wls(y2, XX, ww, gm, gm)
    out[nome] = {'f_cm': [round(float(b[0]), 4), round(float(ep[0]), 4)], 'f_na': [round(float(b[1]), 4), round(float(ep[1]), 4)],
                 'f_dn': [round(float(b[2]), 4), round(float(ep[2]), 4)]}
print(json.dumps(out, indent=1))
