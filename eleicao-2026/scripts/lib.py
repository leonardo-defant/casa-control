"""Funções comuns: leitura das seções e regressão com efeito fixo e erro agrupado."""
import gzip, json
import numpy as np


def carregar(caminho):
    with gzip.open(caminho, 'rt') as f:
        return json.load(f)


def chave_local(k, s):
    uf, mun, zona, _ = k.split('|')
    return f"{uf}|{mun}|{zona}|{s['loc']}"


def demean(M, g, w):
    """Subtrai a média ponderada do grupo de cada coluna de M."""
    ng = g.max() + 1
    sw = np.bincount(g, weights=w, minlength=ng)
    out = np.empty_like(M, dtype=float)
    for j in range(M.shape[1]):
        m = np.bincount(g, weights=w * M[:, j], minlength=ng) / np.where(sw > 0, sw, 1)
        out[:, j] = M[:, j] - m[g]
    return out


def fe_ols(y, X, grupos, w=None, nomes=None):
    """MQO com efeito fixo de grupo (transformação within), pesos e erro-padrão agrupado (CR1)."""
    y = np.asarray(y, float); X = np.asarray(X, float)
    if X.ndim == 1: X = X[:, None]
    n, k = X.shape
    w = np.ones(n) if w is None else np.asarray(w, float)
    _, g = np.unique(grupos, return_inverse=True)
    # só grupos com 2 ou mais observações informam
    cnt = np.bincount(g)
    ok = cnt[g] >= 2
    y, X, w, g = y[ok], X[ok], w[ok], g[ok]
    _, g = np.unique(g, return_inverse=True)
    Z = demean(np.column_stack([y, X]), g, w)
    yd, Xd = Z[:, 0], Z[:, 1:]
    sw = np.sqrt(w)
    Xw, yw = Xd * sw[:, None], yd * sw
    XtX = Xw.T @ Xw
    b = np.linalg.solve(XtX, Xw.T @ yw)
    e = yd - Xd @ b
    G = g.max() + 1
    S = np.zeros((G, k))
    for j in range(k):
        S[:, j] = np.bincount(g, weights=w * Xd[:, j] * e, minlength=G)
    meat = S.T @ S
    inv = np.linalg.inv(XtX)
    N = len(y)
    c = G / (G - 1) * (N - 1) / (N - k)
    V = c * inv @ meat @ inv
    se = np.sqrt(np.diag(V))
    nomes = nomes or [f'x{j}' for j in range(k)]
    return {'n': int(N), 'grupos': int(G), 'coef': dict(zip(nomes, b.tolist())), 'ep': dict(zip(nomes, se.tolist()))}
