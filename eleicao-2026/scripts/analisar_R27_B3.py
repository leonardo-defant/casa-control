"""R27_B3: RESERVATÓRIO E ELEITOR MARGINAL (Adendo 27, Onda B, com o contexto do Adendo 28).

Três partes, com critério já registrado antes de rodar:
  I.   D2-4 INCREMENTO (desenho cego D2): para quem foi o comparecimento a mais, dentro do mesmo prédio, em 2014, 2018,
       2022 e 2026.
  II.  D2-3 RESERVA (desenho cego D2): eleitores sem biometria e muito idosos como reservatório. R1 (censo, perfil do
       eleitorado por seção), R2 (amostra de logs, conta exata), R3 (faixas etárias do perfil de comparecimento).
  III. T32 por seção (reteste da equipe vermelha, fragilidade "Comparecimento: T3, T9, T21, T28, F6, F15, T25 e T32"):
       variação do comparecimento contra as fatias por idade e ganho de Lula por eleitor a mais por terço da fatia de
       70 anos ou mais. A escolha deste reteste é posterior ao dado antigo (aviso do Adendo 27); o critério é novo.

Uso:
  python3 -I scripts/analisar_R27_B3.py parte1     D2-4 nos quatro anos, plantios, placebos, secundárias
  python3 -I scripts/analisar_R27_B3.py parte2     D2-3 R1 e R2 (2026 e placebo de 2022), plantios
  python3 -I scripts/analisar_R27_B3.py parte2r3   D2-3 R3 (perfil de comparecimento, 2026 só 1º turno, 2022 dois turnos)
  python3 -I scripts/analisar_R27_B3.py parte3     T32 por seção
  python3 -I scripts/analisar_R27_B3.py relatorio  junta os parciais e grava resultados/R27_B3_reservatorio_e_marginal.json e .txt
Extrações sem voto (perfil, locais, logs) ficam em /home/user/trabalho-eleicao/adendo27/R27_B3 (scripts extrair_perfil.py,
baixar_perfil2022.py, montar_bases.py, copiados para dentro deste arquivo nas funções de mesmo nome).

O QUE EU JÁ SABIA AO ESCREVER ESTAS DECISÕES (contaminação declarada)
  Li o resumo da Onda A (resultados/ADENDO27_ondaA_resultados.txt): a virada passa pelo comparecimento, concentrada em
  PI, MA, TO, PB e CE; os faltosos do 1º turno aparecem como voto de Lula no dobro da taxa. Ao abrir o script da A6 para
  copiar a leitura do perfil, li no docstring que o coeficiente da fração sem biometria no ganho de Lula "saiu negativo e
  forte" (isso antecipa o sinal de γ_sb do R1; não vi o número). Vi contagens de estrutura (sem voto): 16.747.631
  eleitores sem biometria no perfil de 2026 (Brasil, sem exterior), 17.931 seções agregadas, tipos de seção das bases.
  Não calculei nenhuma estatística com voto antes de gravar este docstring (cópia com SHA-256 e hora em
  /home/user/trabalho-eleicao/adendo27/R27_B3/docstring_antes_de_rodar.txt).

DECISÕES QUE O REGISTRO NÃO FIXA (escritas antes de qualquer conta com voto; relatar como desvios)

Gerais
  G1. Aptos de referência = aptos do 1º turno da seção. "Tipo Apurada" = tipo igual a "apurada" (sem diferenciar
      maiúsculas) nos dois turnos. Local = UF, município, zona e local do 1º turno (lib.chave_local). Exterior (ZZ) fora
      de tudo.
  G2. Regressão com efeito fixo por transformação dentro do grupo, peso aptos, erro agrupado por município (CR1, a
      mesma correção de lib.fe_ols, mas com o município como grupo do erro mesmo quando o efeito fixo é o local).
      Função própria (fe_reg) conferida contra lib.fe_ols quando o efeito fixo e o grupo do erro coincidem.
  G3. Votos plantados são fracionários (sem arredondar) e a semente é 20261110.
  G4. Nível: como o desenho D2 pede 1% na estatística primária de cada teste, intervalos de 95% são os do critério
      escrito e o de 99% vai ao lado. Total nacional de aptos (Brasil sem exterior) e de eleitores sem biometria saem
      das bases e do perfil.

Parte I (D2-4)
  I1. Universo pela letra: seções com os dois turnos, tipo Apurada, aptos >= 50, variação de aptos de no máximo 2, fora
      de ZZ, em locais com 3 ou mais seções assim. Não exijo o mesmo local nos dois turnos (o desenhista não exigiu na
      calibração dele).
  I2. θ0 pela letra: s_j = Σ(L2 - R2)/ΣC2 das seções do universo no local; peso W_j = Σ apt_i (a_i - ā_j)², com ā_j a
      média do local ponderada por aptos. Θ = θ - θ0.
  I3. Erro-padrão de Θ: principal = erro de θ na regressão (θ0 tratado como fixo). Ao lado: reamostragem de municípios
      (500 repetições) de Θ inteiro (θ e θ0 juntos), feita com as somas por município depois da transformação dentro do
      local. "IC de 95% de Θ_2026 excluindo esse máximo" = Θ_2026 - 1,96 ep acima do maior Θ histórico. Erro de
      Θ_2026 - Θ_ref = raiz(ep26² + (ep14² + ep18² + ep22²)/9).
  I4. Ordem do veredito: (1) SINAL se as três condições do critério valem; (2) senão, INCONCLUSIVO se a amplitude de Θ
      entre 2014, 2018 e 2022 passa de 0,10 (histórico instável) ou se |Θ_2026 - Θ_ref| fica entre 0,05 e 0,15 ou acima
      de 0,15 sem cumprir o resto; (3) SEM SINAL se |Θ_2026 - Θ_ref| < 0,05 e a assimetria de cauda fica abaixo de
      443.019 votos. Se os plantios mostrarem que o limiar de 0,15 não é atingido pelo efeito que o registro diz que ele
      representa, o veredito é SEM PODER para absolver.
  I5. Plantio (poder): sorteio de cada seção com probabilidade f (5%, 20%, 50%, 80%) entre todas as seções do Brasil
      com os dois turnos; cada sorteada recebe φ·apt_i votos em C2 e L2, com φ = K/(f·Σapt nacional), K = 1.107.548 e
      depois 4.430.191 (o total efetivamente plantado é relatado; o universo do teste recebe a sua parte). Sem teto de
      faltosos na versão principal, para comparar com a fórmula do registro; marco os cenários em que φ passa da
      abstenção média do 2º turno (fisicamente impossíveis como voto em nome de faltoso). Prédios inteiros: sorteio de
      locais com probabilidade f, todas as seções do local recebem φ·apt_i.
  I6. Explicação inocente plantada (o registro pede no texto da tarefa, não no desenho): (a) ENTRADA DE ELEITORES
      REAIS: as mesmas seções e os mesmos φ·apt_i somados a C2, repartidos entre L2, R2, B2 e N2 na proporção do voto
      observado da própria seção no 2º turno; (b) ABSTENÇÃO PURA: nas mesmas seções, φ·apt_i tirados de C2 e de R2
      (eleitor de Flávio que não volta; limitado a R2), sem voto para Lula. Espera-se Θ para zero em (a) e Θ negativo em
      (b). Para separar inserção de abstenção na mesma conta, rodo também as duas metades da regressão, declaradas aqui
      como secundárias fora do registro: θ_L (variação de L sobre aptos contra a) e θ_R (variação de R sobre aptos
      contra a), com referências L2/C2 e R2/C2 do local. Inserção para Lula puxa Θ_L para cima e Θ_R para baixo;
      abstenção de eleitor de Flávio puxa Θ_R para cima e Θ_L para baixo.
  I7. Espelho: a mesma conta a favor de Flávio é a mesma estatística com o sinal trocado (m' = -m); relato o que uma
      inserção para Flávio do mesmo tamanho daria (plantio em R2) e leio o critério nos dois sentidos. Placebos do
      registro: desfecho branco e nulo ((B2 + N2) - (B1 + N1))/apt contra a, com referência (B2 + N2)/C2 do local; e
      sentido inverso, 1º turno como suspeito: a' = (C1 - C2)/apt, m' = [(L1 - R1) - (L2 - R2)]/apt, controles do 2º
      turno ((B2 + N2)/apt, L2/apt, R2/apt), referência (L1 - R1)/C1 do local.
  I8. Secundárias pela letra, com estas definições: (i) dispersão = desvio-padrão ponderado por aptos do resíduo de a
      dentro do local, e o desvio robusto (1,4826 × desvio absoluto mediano), como o desenhista mediu; (ii) cauda:
      resíduo r_i = a_i - ā_j; limite = 4 desvios robustos do ano; votos = Σ r_i·apt_i acima de +4 menos Σ |r_i|·apt_i
      abaixo de -4; margem dessas seções contra as vizinhas = média ponderada de m_i menos a média do local; (iii)
      locais do mesmo universo somados, efeito fixo de município, referência s do município com peso
      Σ apt_j (a_j - ā_mun)²; (iv) seções fora de ZZ, Apuradas, com aptos >= 50 e comparecimento >= 95% dos aptos, por
      turno e ano.
  I9. Leitura em votos pela fórmula do registro: K(f) = Σapt · σn · raiz(Θ/(1 - Θ)) · raiz(f/(1 - f)), com σn = 0,016 e
      Θ = Θ_2026 - Θ_ref (e o limite superior de 95%), para f = 5%, 20%, 50% e 80%; e o K lido na curva dos plantios.
  I10. Secundária declarada antes, escolhida já conhecendo a Onda A (não cega): Θ de 2026 e dos outros anos só nas
      seções de PI, MA, TO, PB e CE e só nas demais UFs, e por UF. Não entra no veredito.

Parte II (D2-3)
  II1. Perfil do eleitorado: cadastro de 14/07/2026 (perfil_eleitor_secao_2026), seções agregadas somadas na principal
      pelo arquivo de locais (mapa do 2º turno). N_sb = QT_ELEITORES - QT_ELEITORES_BIOMETRIA. p_sb = N_sb/aptos (aptos
      do 1º turno do boletim). As frações de idade, instrução e sexo usam como denominador o total do perfil da seção.
      "16 a 24" = códigos 1600 a 2124; "60 a 69" = 6064 e 6569; "70 ou mais" = 7074 em diante; "fundamental incompleto
      ou menos" = instrução 1, 2 e 3. Seções com |total do perfil - aptos| > 10 ficam fora (o perfil é de julho).
  II2. R1, universo: Brasil, dois turnos, Apurada nos dois, variação de aptos de no máximo 2, perfil ligado. Efeito
      fixo de local (locais de uma seção só saem sozinhos), peso aptos, erro por município. ΣN_sb nacional = perfil do
      Brasil sem exterior (o exterior não tem biometria e não entra no universo). V1 = δ × ΣN_sb nacional; limites de
      95% = (δ ± 1,96 ep) × ΣN_sb.
  II3. R2: contagem por seção e dia com o extrator do desenhista D2 (extrair_eventos_log.py): ANO, BIO e MAN de
      habilitações com voto computado. Amostra = todas as seções da amostra antiga com os dois dias no mesmo log e
      perfil ligado (principal); ao lado, só o prefixo autoponderado de L_ordem.txt. Erro de Δτ por linearização do
      estimador de razão, agrupado por local. A amostra não é aleatória simples: V2 vale como ordem de grandeza.
      V = max(V1, V2); limite inferior de V = o limite inferior da parcela que deu o máximo.
  II4. Veredito de volume (R1 e R2) e sentinela R3 são relatados separados. Pela letra o R3 fica INCONCLUSIVO enquanto
      o TSE não publicar o 2º turno no perfil de comparecimento (conferido em 10/11/2026: o arquivo no ar é o mesmo de
      21/10/2026, mesmo etag). SEM SINAL do teste inteiro exige R3 dentro da faixa, logo o teste inteiro não pode sair
      SEM SINAL hoje; relato o veredito do volume e digo isso.
  II5. "Placebo de 2022 com δ menor que um terço do de 2026": δ_2022 < δ_2026/3 com δ_2026 > 0. "δ parecido" (leva a
      inconclusivo): δ_2022 >= δ_2026/3 quando o resto do critério de sinal passa. Perfil de 2022 = perfil_eleitor_secao
      de 2022 (cadastro de 26/08/2022), agregadas somadas pelo arquivo de locais de 2022.
  II6. Plantio pela letra: φ·N_sb somados a C2 e L2 de cada seção com perfil, φ = K/ΣN_sb nacional, K = 1.107.548 e
      443.019; o mesmo em ANO2 na amostra. Inocente (entrada de eleitores reais sem biometria): os mesmos φ·N_sb
      somados a C2 e repartidos como o voto da seção no 2º turno; mede se γ_sb/δ >= 0,5 separa as duas. Abstenção pura
      não tem versão neste teste (o reservatório é de quem entra).
  II7. Espelho e desfechos ao lado (declarados antes): γ_sb com o sinal trocado é o ganho de Flávio; as duas metades
      (variação de L e de R sobre aptos contra p_sb); desfecho branco e nulo; e o mesmo R1 com efeito fixo de município
      no lugar do local (enxerga prédios inteiros, mais sujeito a comportamento). Valor bruto de 2026: médias de a e de
      m por quinto de p_sb.
  II8. R3: perfil de comparecimento por UF (arquivos por UF, exterior fora), T(b, t) = Σcomparecimento/Σaptos. 2026 só
      tem o 1º turno. Relato os níveis de 2026 no 1º turno contra 2022, as razões de 2022 e o plantio de 3 pontos na
      faixa de 100 anos ou mais.

Parte III (T32 por seção)
  III1. Universo = o do R1. y = 100·(C2 - C1)/apt contra as fatias (sobre o total do perfil) de 16 e 17, 18 a 24, 60 a
      69 e 70 ou mais (referência 25 a 59), efeito fixo de município, peso aptos, erro por município.
  III2. "Ganho de Lula por eleitor a mais" = coeficiente de a = (C2 - C1)/apt na regressão de (L2 - L1)/apt, efeito
      fixo de município, com os controles do 1º turno do D2-4 (O1, B1 + N1, L1 e R1 sobre aptos), estimado dentro de
      cada terço da fatia de 70 ou mais (cortes nacionais, seções sem peso). Ao lado: sem controles, a razão bruta
      Σ(L2 - L1)/Σ(C2 - C1), o mesmo para Flávio (espelho) e para a margem.
  III3. Decil de maior fatia de 70 ou mais (corte nacional, seções sem peso). "Alta do comparecimento contra as demais
      seções do município": taxa ΣΔC/Σapt do decil contra a taxa das demais seções dos mesmos municípios, ponderada
      pelos aptos do decil em cada município (padronização direta). Condição "2 vezes": razão >= 2 se a taxa das demais
      for positiva; se for zero ou negativa, vale se a do decil for positiva. Ganho no decil >= 0,9 e no resto <= 0,6,
      com a diferença a mais de 4 erros-padrão num modelo único com efeito fixo de município vezes grupo e todos os
      regressores abertos por grupo.
  III4. SEM SINAL: maior menos menor ganho entre os terços <= 0,1 E alta proporcional aos faltosos, que defino como: a
      taxa de entrada por faltoso do 1º turno, ΣΔC/Σ(apt - C1), no terço de cima entre 0,8 e 1,25 vezes a do terço de
      baixo. Fora de SINAL e de SEM SINAL: INCONCLUSIVO.
  III5. Plantio: φ·N70_i votos somados a C2 e L2 (N70 = eleitores de 70 anos ou mais da seção), φ = K/ΣN70 nacional,
      K = 1.107.548 e 4.430.191. Inocente: os mesmos votos repartidos como o voto da seção. Se o critério de SINAL não
      disparar com a margem inteira plantada, a parte é SEM PODER para acusar por esse critério e isso é dito.
  III6. Espelho: a mesma conta com o ganho de Flávio, e com a fatia de 16 a 24 anos no lugar da de 70 ou mais.

Tradução em votos: cada voto inserido vale 1 de margem (margem 4.430.191; 25% = 1.107.548; 10% = 443.019).
"""
# ADIÇÕES DEPOIS DE GRAVAR O DOCSTRING (o texto acima é o gravado às 04:49:16 UTC de 10/11/2026 e não foi alterado):
#   modos idosos_uf, expl2018 e acap (exploratórios E2, E1/E3 do relatório); filtro de mesma urna no R2; erro agrupado por local quando a
#   UF tem um município só (DF); T32 de 2022 como placebo; metades por UF; E4 (grupo sem biometria como controle). Tudo marcado no relatório.
import os, sys, json, gzip, math, hashlib, time
import numpy as np

RAIZ = '/home/user/casa-control/eleicao-2026'
TRAB = '/home/user/trabalho-eleicao/adendo27/R27_B3'
D = '/home/user/trabalho-eleicao'
MARGEM = 4430191; K25 = 1107548; K10 = 443019
SEMENTE = 20261110
ANOS = (2014, 2018, 2022, 2026)
UFS5 = ('PI', 'MA', 'TO', 'PB', 'CE')
SIGMA_N = 0.016
CAMPOS = ['apt', 'comp', 'L', 'R', 'O', 'B', 'N']


def grava(nome, obj):
    with open(f'{TRAB}/{nome}', 'w') as f:
        json.dump(obj, f, ensure_ascii=False, indent=1)


# ---------------------------------------------------------------------------------------------- leitura das bases
def montar_base(ano):
    """Converte dados/secoesAAAA.json.gz em vetores (só leitura e empacotamento)."""
    with gzip.open(f'{RAIZ}/dados/secoes{ano}.json.gz', 'rt') as f:
        d = json.load(f)
    ks = sorted(d); n = len(ks)
    out = {'chave': np.array(ks)}
    for t in ('1', '2'):
        for c in CAMPOS: out[c + t] = np.full(n, -1, dtype=np.int32)
        out['loc' + t] = np.full(n, -1, dtype=np.int64); out['tipo' + t] = np.zeros(n, dtype='U24')
        out['urna' + t] = np.full(n, -1, dtype=np.int64)
    for i, k in enumerate(ks):
        v = d[k]
        for t in ('1', '2'):
            if t not in v: continue
            s = v[t]
            for c in CAMPOS:
                x = s.get(c)
                if x is not None: out[c + t][i] = int(x)
            try: out['loc' + t][i] = int(s.get('loc'))
            except (TypeError, ValueError): pass
            try: out['urna' + t][i] = int(s.get('urna'))
            except (TypeError, ValueError): pass
            out['tipo' + t][i] = str(s.get('tipo'))[:24]
    np.savez_compressed(f'{TRAB}/base{ano}.npz', **out)


def carregar_base(ano):
    p = f'{TRAB}/base{ano}.npz'
    if not os.path.exists(p): montar_base(ano)
    z = np.load(p)
    B = {k: z[k] for k in z.files}
    partes = [c.split('|') for c in B['chave'].tolist()]
    B['uf'] = np.array([p_[0] for p_ in partes])
    B['mun'] = np.array([int(p_[1]) for p_ in partes], dtype=np.int64)
    B['zona'] = np.array([int(p_[2]) for p_ in partes], dtype=np.int64)
    B['secao'] = np.array([int(p_[3]) for p_ in partes], dtype=np.int64)
    B['brasil'] = B['uf'] != 'ZZ'
    B['dois'] = (B['apt1'] > 0) & (B['apt2'] > 0) & (B['comp1'] > 0) & (B['comp2'] > 0)
    B['apurada'] = (np.char.lower(B['tipo1']) == 'apurada') & (np.char.lower(B['tipo2']) == 'apurada')
    _, B['ufid'] = np.unique(B['uf'], return_inverse=True)
    B['munid'] = np.unique(B['ufid'].astype(np.int64) * 10 ** 6 + B['mun'], return_inverse=True)[1]
    B['locid'] = np.unique(np.char.add(np.char.add(np.char.add(B['uf'], '|'), B['mun'].astype(str)),
                                       np.char.add(np.char.add('|', B['zona'].astype(str)), np.char.add('|', B['loc1'].astype(str)))),
                           return_inverse=True)[1]
    return B


# ---------------------------------------------------------------------------------------------- regressão
def demean(M, g, w):
    ng = g.max() + 1
    sw = np.bincount(g, weights=w, minlength=ng)
    out = np.empty_like(M, dtype=float)
    for j in range(M.shape[1]):
        out[:, j] = M[:, j] - (np.bincount(g, weights=w * M[:, j], minlength=ng) / np.where(sw > 0, sw, 1))[g]
    return out


def fe_reg(y, X, fe, cl, w, nomes, extra=False):
    """MQO com efeito fixo (within), peso w, erro agrupado por cl (CR1 como em lib.fe_ols)."""
    y = np.asarray(y, float); X = np.asarray(X, float)
    if X.ndim == 1: X = X[:, None]
    w = np.asarray(w, float)
    _, g = np.unique(fe, return_inverse=True)
    ok = np.bincount(g)[g] >= 2
    y, X, w, g, cl = y[ok], X[ok], w[ok], g[ok], np.asarray(cl)[ok]
    _, g = np.unique(g, return_inverse=True)
    _, c = np.unique(cl, return_inverse=True)
    k = X.shape[1]
    Z = demean(np.column_stack([y, X]), g, w)
    yd, Xd = Z[:, 0], Z[:, 1:]
    XtX = (Xd * w[:, None]).T @ Xd
    b = np.linalg.solve(XtX, (Xd * w[:, None]).T @ yd)
    e = yd - Xd @ b
    G = int(c.max()) + 1
    S = np.zeros((G, k))
    for j in range(k): S[:, j] = np.bincount(c, weights=w * Xd[:, j] * e, minlength=G)
    inv = np.linalg.inv(XtX)
    N = len(y)
    V = G / (G - 1) * (N - 1) / (N - k) * inv @ (S.T @ S) @ inv
    se = np.sqrt(np.diag(V))
    r = {'n': int(N), 'grupos_ef': int(g.max() + 1), 'grupos_erro': G, 'coef': dict(zip(nomes, b.tolist())), 'ep': dict(zip(nomes, se.tolist()))}
    if extra:
        r['_'] = {'ok': ok, 'Xd': Xd, 'yd': yd, 'w': w, 'c': c, 'G': G, 'V': V, 'b': b}
    return r


def ce(r, nome):
    return {'coef': r['coef'][nome], 'ep': r['ep'][nome]}


# ---------------------------------------------------------------------------------------------- PARTE I: D2-4
def universo4(B):
    u = B['brasil'] & B['dois'] & B['apurada'] & (B['apt1'] >= 50) & (np.abs(B['apt2'] - B['apt1']) <= 2)
    cnt = np.bincount(B['locid'][u], minlength=B['locid'].max() + 1)
    return u & (cnt[B['locid']] >= 3)


def conta_theta(apt, a, y, ctrl, s_num, s_den, loc, mun, nomes_ctrl, boot=0, rng=None):
    """θ = coeficiente de a em y ~ a + controles com efeito fixo de local; θ0 = média de s_j com peso W_j; Θ = θ - θ0."""
    _, lj = np.unique(loc, return_inverse=True)
    nl = lj.max() + 1
    sa = np.bincount(lj, weights=apt, minlength=nl)
    abar = np.bincount(lj, weights=apt * a, minlength=nl) / sa
    W = np.bincount(lj, weights=apt * (a - abar[lj]) ** 2, minlength=nl)
    den = np.bincount(lj, weights=s_den, minlength=nl)
    s = np.bincount(lj, weights=s_num, minlength=nl) / np.where(den > 0, den, 1)
    th0 = float((W * s).sum() / W.sum())
    if len(np.unique(mun)) < 2: mun = lj   # um município só (DF): erro agrupado por local
    r = fe_reg(y, np.column_stack([a] + ctrl), lj, mun, apt, ['a'] + nomes_ctrl, extra=boot > 0)
    th = r['coef']['a']; ep = r['ep']['a']
    o = {'theta': th, 'ep_theta': ep, 'theta0': th0, 'Theta': th - th0, 'n': r['n'], 'locais': r['grupos_ef'], 'municipios': r['grupos_erro'],
         'controles': {k: r['coef'][k] for k in nomes_ctrl}}
    if boot > 0:
        x = r.pop('_'); Xd, yd, w, c, G = x['Xd'], x['yd'], x['w'], x['c'], x['G']
        k = Xd.shape[1]
        A = np.zeros((G, k, k)); bb = np.zeros((G, k))
        for i in range(k):
            bb[:, i] = np.bincount(c, weights=w * Xd[:, i] * yd, minlength=G)
            for j in range(i, k):
                A[:, i, j] = A[:, j, i] = np.bincount(c, weights=w * Xd[:, i] * Xd[:, j], minlength=G)
        # município de cada local (o local está contido no município)
        _, cm = np.unique(mun, return_inverse=True)
        mun_do_local = np.zeros(nl, dtype=np.int64); mun_do_local[lj] = cm
        num_g = np.bincount(mun_do_local, weights=W * s, minlength=G); den_g = np.bincount(mun_do_local, weights=W, minlength=G)
        tb = np.empty(boot)
        for it in range(boot):
            q = rng.multinomial(G, np.full(G, 1.0 / G)).astype(float)
            tb[it] = np.linalg.solve(np.tensordot(q, A, 1), q @ bb)[0] - (q @ num_g) / (q @ den_g)
        o['ep_Theta_reamostragem'] = float(tb.std(ddof=1))
    return o


def monta_u(B, u):
    U = {k: B[k][u].astype(float) for k in ('apt1', 'comp1', 'comp2', 'L1', 'R1', 'O1', 'B1', 'N1', 'L2', 'R2', 'O2', 'B2', 'N2')}
    U['loc'] = B['locid'][u]; U['mun'] = B['munid'][u]; U['uf'] = B['uf'][u]
    return U


def estat4(U, C2=None, L2=None, R2=None, B2=None, N2=None, boot=0, rng=None, sel=None, quais=('m',)):
    """Estatísticas do D2-4 no universo U (dicionário de vetores); os vetores do 2º turno podem ser trocados (plantio)."""
    C2 = U['comp2'] if C2 is None else C2; L2 = U['L2'] if L2 is None else L2; R2 = U['R2'] if R2 is None else R2
    B2 = U['B2'] if B2 is None else B2; N2 = U['N2'] if N2 is None else N2
    apt = U['apt1']
    if sel is None: sel = np.ones(len(apt), bool)
    a = (C2 - U['comp1']) / apt
    ctrl = [U['O1'] / apt, (U['B1'] + U['N1']) / apt, U['L1'] / apt, U['R1'] / apt]
    nc = ['O1', 'BN1', 'L1', 'R1']
    out = {}
    f = lambda v: v[sel]
    cs = [f(c) for c in ctrl]
    if 'm' in quais:
        m = ((L2 - R2) - (U['L1'] - U['R1'])) / apt
        out['m'] = conta_theta(f(apt), f(a), f(m), cs, f(L2 - R2), f(C2), f(U['loc']), f(U['mun']), nc, boot, rng)
    if 'L' in quais:
        out['L'] = conta_theta(f(apt), f(a), f((L2 - U['L1']) / apt), cs, f(L2), f(C2), f(U['loc']), f(U['mun']), nc)
    if 'R' in quais:
        out['R'] = conta_theta(f(apt), f(a), f((R2 - U['R1']) / apt), cs, f(R2), f(C2), f(U['loc']), f(U['mun']), nc)
    if 'BN' in quais:
        out['BN'] = conta_theta(f(apt), f(a), f(((B2 + N2) - (U['B1'] + U['N1'])) / apt), cs, f(B2 + N2), f(C2), f(U['loc']), f(U['mun']), nc)
    if 'inv' in quais:  # 1º turno como suspeito
        ai = (U['comp1'] - C2) / apt
        mi = ((U['L1'] - U['R1']) - (L2 - R2)) / apt
        ci = [f((B2 + N2) / apt), f(L2 / apt), f(R2 / apt)]
        out['inv'] = conta_theta(f(apt), f(ai), f(mi), ci, f(U['L1'] - U['R1']), f(U['comp1']), f(U['loc']), f(U['mun']), ['BN2', 'L2', 'R2'])
    return out


def residuo_local(v, apt, loc):
    _, lj = np.unique(loc, return_inverse=True)
    return v - (np.bincount(lj, weights=apt * v) / np.bincount(lj, weights=apt))[lj]


def secundarias4(B, u, U):
    apt = U['apt1']; a = (U['comp2'] - U['comp1']) / apt
    m = ((U['L2'] - U['R2']) - (U['L1'] - U['R1'])) / apt
    r = residuo_local(a, apt, U['loc']); rm = residuo_local(m, apt, U['loc'])
    dp = math.sqrt((apt * r ** 2).sum() / apt.sum())
    rob = 1.4826 * float(np.median(np.abs(r - np.median(r))))
    up = r > 4 * rob; dn = r < -4 * rob
    vu = float((r[up] * apt[up]).sum()); vd = float((-r[dn] * apt[dn]).sum())
    def med(msk):
        return float((rm[msk] * apt[msk]).sum() / apt[msk].sum()) if msk.any() else None
    o = {'i_dispersao': {'dp_ponderado': dp, 'dp_robusto': rob, 'referencia_registro': SIGMA_N},
         'ii_cauda': {'limite_4_desvios_robustos': 4 * rob, 'secoes_acima': int(up.sum()), 'secoes_abaixo': int(dn.sum()),
                      'votos_acima': vu, 'votos_abaixo': vd, 'assimetria_votos': vu - vd,
                      'margem_residual_media_acima': med(up), 'margem_residual_media_abaixo': med(dn),
                      'votos_de_margem_residual_acima': float((rm[up] * apt[up]).sum()), 'votos_de_margem_residual_abaixo': float((rm[dn] * apt[dn]).sum()),
                      'inclinacao_margem_por_voto_acima': (float((rm[up] * apt[up]).sum()) / vu) if vu > 0 else None,
                      'inclinacao_margem_por_voto_abaixo': (float((rm[dn] * apt[dn]).sum()) / -vd) if vd > 0 else None}}
    # (iii) entre locais, efeito fixo de município
    o['iii_entre_locais'] = entre_locais(U)
    # (iv) comparecimento >= 95%
    b = B['brasil'] & B['apurada'] & (B['apt1'] >= 50)
    o['iv_comparecimento_95'] = {'secoes_base': int(b.sum()),
                                 '1t': int((b & (B['comp1'] >= 0.95 * B['apt1'])).sum()),
                                 '2t': int((b & (B['apt2'] > 0) & (B['comp2'] >= 0.95 * B['apt2'])).sum())}
    return o


def entre_locais(U, C2=None, L2=None, R2=None):
    C2 = U['comp2'] if C2 is None else C2; L2 = U['L2'] if L2 is None else L2; R2 = U['R2'] if R2 is None else R2
    _, lj = np.unique(U['loc'], return_inverse=True)
    nl = lj.max() + 1
    S = lambda v: np.bincount(lj, weights=v, minlength=nl)
    apt = S(U['apt1']); mun = np.zeros(nl, dtype=np.int64); mun[lj] = U['mun']
    a = (S(C2) - S(U['comp1'])) / apt
    m = ((S(L2) - S(R2)) - (S(U['L1']) - S(U['R1']))) / apt
    ctrl = [S(U['O1']) / apt, (S(U['B1']) + S(U['N1'])) / apt, S(U['L1']) / apt, S(U['R1']) / apt]
    cnt = np.bincount(mun); ok = cnt[mun] >= 2
    r = conta_theta(apt[ok], a[ok], m[ok], [c[ok] for c in ctrl], (S(L2) - S(R2))[ok], S(C2)[ok], mun[ok], mun[ok], ['O1', 'BN1', 'L1', 'R1'])
    return r


def plantar_secoes(Bn, rng, f, K, alvo='L', modo='insercao', por_local=False):
    """Devolve vetores do 2º turno com plantio. Bn: vetores nacionais (Brasil, dois turnos). modo: insercao (C2 e alvo),
    entrada (C2, repartido como o voto da seção), abstencao (tira de C2 e de R2)."""
    n = len(Bn['apt1'])
    if por_local:
        _, lj = np.unique(Bn['loc'], return_inverse=True)
        esc = (rng.random(lj.max() + 1) < f)[lj]
    else:
        esc = rng.random(n) < f
    phi = K / (f * Bn['apt1'].sum())
    k = np.where(esc, phi * Bn['apt1'], 0.0)
    C2 = Bn['comp2'].copy(); L2 = Bn['L2'].copy(); R2 = Bn['R2'].copy(); B2 = Bn['B2'].copy(); N2 = Bn['N2'].copy()
    if modo == 'insercao':
        C2 += k
        if alvo == 'L': L2 += k
        else: R2 += k
    elif modo == 'entrada':
        c = Bn['comp2']
        C2 += k; L2 += k * Bn['L2'] / c; R2 += k * Bn['R2'] / c; B2 += k * Bn['B2'] / c; N2 += k * Bn['N2'] / c
    elif modo == 'abstencao':
        k = np.minimum(k, Bn['R2'])
        C2 -= k; R2 -= k
    return {'C2': C2, 'L2': L2, 'R2': R2, 'B2': B2, 'N2': N2, 'phi': float(phi), 'plantado': float(k.sum()), 'secoes': int(esc.sum())}


def formula_registro(K, f, aptos, sn=SIGMA_N):
    sk2 = (K / aptos) ** 2 * (1 - f) / f
    return sk2 / (sn ** 2 + sk2)


def parte1():
    t0 = time.time()
    res = {'por_ano': {}}
    guard = {}
    for ano in ANOS:
        B = carregar_base(ano)
        u = universo4(B)
        U = monta_u(B, u)
        rng = np.random.default_rng(SEMENTE + ano)
        e = estat4(U, boot=500, rng=rng, quais=('m', 'L', 'R', 'BN', 'inv'))
        nb = B['brasil'] & B['dois']
        info = {'secoes_na_base': int(len(B['chave'])), 'secoes_brasil_dois_turnos': int(nb.sum()),
                'universo_secoes': int(u.sum()), 'universo_aptos': float(U['apt1'].sum()),
                'aptos_brasil_dois_turnos': float(B['apt1'][nb].sum()),
                'excluidas_por_variacao_de_aptos_maior_que_2': int((B['brasil'] & B['dois'] & B['apurada'] & (B['apt1'] >= 50) & (np.abs(B['apt2'] - B['apt1']) > 2)).sum()),
                'bruto': {'comparecimento_1t': float(U['comp1'].sum()), 'comparecimento_2t': float(U['comp2'].sum()),
                          'margem_1t_L_menos_R': float((U['L1'] - U['R1']).sum()), 'margem_2t_L_menos_R': float((U['L2'] - U['R2']).sum()),
                          's_nacional_no_universo': float((U['L2'] - U['R2']).sum() / U['comp2'].sum())}}
        sec = secundarias4(B, u, U)
        grupos = {}
        for nome, msk in (('PI_MA_TO_PB_CE', np.isin(U['uf'], UFS5)), ('demais_UFs', ~np.isin(U['uf'], UFS5))):
            grupos[nome] = estat4(U, sel=msk, quais=('m', 'L', 'R'))
        por_uf = {}
        for uf in sorted(set(U['uf'].tolist())):
            msk = U['uf'] == uf
            try:
                eu = estat4(U, sel=msk, quais=('m', 'L', 'R'))
                por_uf[uf] = {k: v for k, v in eu['m'].items() if k != 'controles'}
                por_uf[uf].update({'Theta_L': eu['L']['Theta'], 'Theta_R': eu['R']['Theta'], 'ep_theta_L': eu['L']['ep_theta'], 'ep_theta_R': eu['R']['ep_theta'],
                                   'aptos': float(U['apt1'][msk].sum()), 'variacao_media_do_comparecimento': float((U['comp2'][msk] - U['comp1'][msk]).sum() / U['apt1'][msk].sum())})
            except Exception as ex: por_uf[uf] = {'erro': str(ex)}
        res['por_ano'][str(ano)] = {'info': info, 'principal': e, 'secundarias': sec, 'grupos_de_uf': grupos, 'por_uf': por_uf}
        print(ano, 'n', info['universo_secoes'], 'theta %.4f ep %.4f theta0 %.4f Theta %.4f (ep reamostragem %.4f)' % (
            e['m']['theta'], e['m']['ep_theta'], e['m']['theta0'], e['m']['Theta'], e['m']['ep_Theta_reamostragem']), 'tempo %.0f s' % (time.time() - t0), flush=True)
        grava('parcial_parte1_anos.json', res)
        if ano == 2026: guard = {'B': B, 'u': u, 'U': U}
    # ------------------------------------------------ plantios em 2026
    B, u, U = guard['B'], guard['u'], guard['U']
    nb = B['brasil'] & B['dois']
    Bn = {k: B[k][nb].astype(float) for k in ('apt1', 'comp1', 'comp2', 'L1', 'R1', 'O1', 'B1', 'N1', 'L2', 'R2', 'B2', 'N2')}
    Bn['loc'] = B['locid'][nb]
    pos = np.cumsum(nb) - 1; iu = pos[u]            # posição das seções do universo dentro do vetor nacional
    aptos_nac = float(Bn['apt1'].sum())
    abst2 = float(1 - Bn['comp2'].sum() / Bn['apt1'].sum())
    obs = res['por_ano']['2026']['principal']
    plant = {'aptos_nacionais': aptos_nac, 'abstencao_media_2t': abst2, 'cenarios': []}
    rng = np.random.default_rng(SEMENTE)
    for K in (K25, MARGEM):
        for f in (0.05, 0.20, 0.50, 0.80):
            semente_c = int(rng.integers(1, 2 ** 31))
            linha = {'K': K, 'f': f, 'phi': K / (f * aptos_nac), 'fisicamente_possivel_em_media': bool(K / (f * aptos_nac) < abst2),
                     'formula_registro': formula_registro(K, f, aptos_nac),
                     'formula_com_dp_de_2026': formula_registro(K, f, aptos_nac, res['por_ano']['2026']['secundarias']['i_dispersao']['dp_ponderado'])}
            for nome, kw in (('insercao_L', dict(alvo='L', modo='insercao')), ('entrada_real', dict(modo='entrada')),
                             ('abstencao_R', dict(modo='abstencao')), ('insercao_R_espelho', dict(alvo='R', modo='insercao'))):
                p = plantar_secoes(Bn, np.random.default_rng(semente_c), f, K, **kw)
                e = estat4(U, C2=p['C2'][iu], L2=p['L2'][iu], R2=p['R2'][iu], B2=p['B2'][iu], N2=p['N2'][iu], quais=('m', 'L', 'R'))
                linha[nome] = {'plantado_nacional': p['plantado'], 'plantado_no_universo': float(np.abs(p['C2'][iu] - U['comp2']).sum()),
                               'Theta': e['m']['Theta'], 'theta': e['m']['theta'], 'theta0': e['m']['theta0'], 'ep_theta': e['m']['ep_theta'],
                               'deslocamento_de_Theta': e['m']['Theta'] - obs['m']['Theta'],
                               'Theta_L': e['L']['Theta'], 'Theta_R': e['R']['Theta'],
                               'deslocamento_Theta_L': e['L']['Theta'] - obs['L']['Theta'], 'deslocamento_Theta_R': e['R']['Theta'] - obs['R']['Theta']}
            # prédios inteiros
            p = plantar_secoes(Bn, np.random.default_rng(semente_c + 1), f, K, alvo='L', modo='insercao', por_local=True)
            e = estat4(U, C2=p['C2'][iu], L2=p['L2'][iu], R2=p['R2'][iu], quais=('m',))
            el = entre_locais(U, C2=p['C2'][iu], L2=p['L2'][iu], R2=p['R2'][iu])
            base_l = res['por_ano']['2026']['secundarias']['iii_entre_locais']
            linha['predios_inteiros_insercao_L'] = {'plantado_nacional': p['plantado'], 'Theta_principal': e['m']['Theta'],
                                                    'deslocamento_principal': e['m']['Theta'] - obs['m']['Theta'],
                                                    'Theta_iii': el['Theta'], 'deslocamento_iii': el['Theta'] - base_l['Theta'], 'ep_theta_iii': el['ep_theta']}
            # (iii) com plantio por seção
            p = plantar_secoes(Bn, np.random.default_rng(semente_c), f, K, alvo='L', modo='insercao')
            el = entre_locais(U, C2=p['C2'][iu], L2=p['L2'][iu], R2=p['R2'][iu])
            linha['insercao_L']['Theta_iii'] = el['Theta']; linha['insercao_L']['deslocamento_iii'] = el['Theta'] - base_l['Theta']
            plant['cenarios'].append(linha)
            print('plantio K %d f %.2f formula %.3f insercao dTheta %.3f entrada %.3f abstencao %.3f espelho %.3f predios %.3f iii %.3f' % (
                K, f, linha['formula_registro'], linha['insercao_L']['deslocamento_de_Theta'], linha['entrada_real']['deslocamento_de_Theta'],
                linha['abstencao_R']['deslocamento_de_Theta'], linha['insercao_R_espelho']['deslocamento_de_Theta'],
                linha['predios_inteiros_insercao_L']['deslocamento_principal'], linha['predios_inteiros_insercao_L']['deslocamento_iii']), flush=True)
            grava('parcial_parte1_plantios.json', plant)
    # inserção igual em todas as seções (f = 1): cegueira declarada
    k = K25 / aptos_nac * Bn['apt1']
    e = estat4(U, C2=(Bn['comp2'] + k)[iu], L2=(Bn['L2'] + k)[iu], quais=('m',))
    plant['insercao_igual_em_todas_as_secoes_K25'] = {'Theta': e['m']['Theta'], 'deslocamento': e['m']['Theta'] - obs['m']['Theta']}
    k = MARGEM / aptos_nac * Bn['apt1']
    e = estat4(U, C2=(Bn['comp2'] + k)[iu], L2=(Bn['L2'] + k)[iu], quais=('m',))
    plant['insercao_igual_em_todas_as_secoes_margem'] = {'Theta': e['m']['Theta'], 'deslocamento': e['m']['Theta'] - obs['m']['Theta']}
    grava('parcial_parte1_plantios.json', plant)
    res['plantios_2026'] = plant
    grava('parcial_parte1.json', res)
    print('parte1 ok %.0f s' % (time.time() - t0), flush=True)


# ---------------------------------------------------------------------------------------------- perfil do eleitorado
FAIXAS = [1600, 1700, 1800, 1900, 2000, 2124, 2529, 3034, 3539, 4044, 4549, 5054, 5559, 6064, 6569, 7074, 7579, 8084, 8589,
          9094, 9599, 9999, -3]
NF = len(FAIXAS)
ZIP_LOCAIS = {2026: D + '/adendo21/F14_dl_locais/eleitorado_local_votacao_2026.zip', 2022: TRAB + '/dl_locais2022/eleitorado_local_votacao_2022.zip'}


def perfil_ligado(ano, B):
    """Perfil por seção (extrair_perfil.py), agregadas somadas na principal (mapa do 2º turno), alinhado à ordem da base."""
    cache = f'{TRAB}/perfil_ligado_{ano}.npz'
    if os.path.exists(cache):
        z = np.load(cache); return z['M'], z['tem'], json.loads(str(z['info']))
    import pandas as pd, zipfile
    z = np.load(f'{TRAB}/perfil{ano}.npz')
    P = pd.DataFrame({'uf': z['uf'], 'k': z['chave']})
    M = z['M'].astype(np.int64)
    zf = zipfile.ZipFile(ZIP_LOCAIS[ano])
    nomes = [i.filename for i in zf.infolist() if i.filename.lower().endswith('.csv')]
    nome = [n for n in nomes if 'BRASIL' in n.upper()] or nomes
    loc = pd.read_csv(zf.open(nome[0]), sep=';', encoding='latin-1', usecols=['NR_TURNO', 'SG_UF', 'CD_MUNICIPIO', 'NR_ZONA', 'NR_SECAO', 'NR_SECAO_PRINCIPAL'])
    loc = loc[(loc.NR_TURNO == 2) & (loc.NR_SECAO_PRINCIPAL > 0) & (loc.SG_UF != 'ZZ')]
    kag = (loc.CD_MUNICIPIO.astype(np.int64) * 10 ** 8 + loc.NR_ZONA.astype(np.int64) * 10 ** 4 + loc.NR_SECAO.astype(np.int64)).to_numpy()
    kpr = (loc.CD_MUNICIPIO.astype(np.int64) * 10 ** 8 + loc.NR_ZONA.astype(np.int64) * 10 ** 4 + loc.NR_SECAO_PRINCIPAL.astype(np.int64)).to_numpy()
    mapa = dict(zip(zip(loc.SG_UF.tolist(), kag.tolist()), kpr.tolist()))
    kk = np.array([mapa.get((u, k), k) for u, k in zip(P.uf.tolist(), P.k.tolist())], dtype=np.int64)
    n_ag = int((kk != P.k.to_numpy()).sum())
    kb = B['mun'] * 10 ** 8 + B['zona'] * 10 ** 4 + B['secao']
    idx = {(u, int(k)): i for i, (u, k) in enumerate(zip(B['uf'].tolist(), kb.tolist()))}
    lin = np.array([idx.get((u, int(k)), -1) for u, k in zip(P.uf.tolist(), kk.tolist())], dtype=np.int64)
    out = np.zeros((len(B['chave']), M.shape[1]), dtype=np.int64)
    okl = lin >= 0
    np.add.at(out, lin[okl], M[okl])
    tem = np.zeros(len(B['chave']), bool); tem[lin[okl]] = True
    info = {'secoes_no_perfil': int(len(M)), 'agregadas_somadas_na_principal': n_ag, 'linhas_do_perfil_sem_secao_na_base': int((~okl).sum()),
            'eleitores_do_perfil_sem_secao_na_base': int(M[~okl, 0].sum()), 'secoes_da_base_com_perfil': int(tem.sum()),
            'eleitores_perfil_brasil': int(M[:, 0].sum()), 'sem_biometria_perfil_brasil': int((M[:, 0] - M[:, 1]).sum())}
    np.savez_compressed(cache, M=out.astype(np.int32), tem=tem, info=json.dumps(info))
    return out, tem, info


def variaveis_perfil(M):
    tot = M[:, 0].astype(float); t = np.where(tot > 0, tot, 1)
    F = M[:, 12:12 + NF].astype(float); Fb = M[:, 12 + NF:12 + 2 * NF].astype(float)
    ix = {c: i for i, c in enumerate(FAIXAS)}
    som = lambda cods, A=F: A[:, [ix[c] for c in cods]].sum(1)
    v = {'tot': tot, 'N_sb': tot - M[:, 1], 'fem': M[:, 2] / t, 'fund': M[:, 3:6].sum(1) / t,
         'N1617': som([1600, 1700]), 'N1824': som([1800, 1900, 2000, 2124]), 'N6069': som([6064, 6569]),
         'N70': som([7074, 7579, 8084, 8589, 9094, 9599, 9999]), 'N80': som([8084, 8589, 9094, 9599, 9999]),
         'N90': som([9094, 9599, 9999])}
    v['f1617'] = v['N1617'] / t; v['f1824'] = v['N1824'] / t; v['f1624'] = v['f1617'] + v['f1824']
    v['f6069'] = v['N6069'] / t; v['f70'] = v['N70'] / t
    v['Nsb70'] = v['N70'] - som([7074, 7579, 8084, 8589, 9094, 9599, 9999], Fb)
    v['Nsb1624'] = v['N1617'] + v['N1824'] - som([1600, 1700, 1800, 1900, 2000, 2124], Fb)
    return v


def universo_r1(B, M, tem):
    return (B['brasil'] & B['dois'] & B['apurada'] & (np.abs(B['apt2'] - B['apt1']) <= 2) & tem & (np.abs(M[:, 0] - B['apt1']) <= 10))


# ---------------------------------------------------------------------------------------------- PARTE II: D2-3
def r1(B, u, V, C2=None, L2=None, R2=None, B2=None, N2=None, ef='loc', quais=('a', 'm')):
    f = lambda k: B[k][u].astype(float)
    apt = f('apt1')
    C2 = f('comp2') if C2 is None else C2; L2 = f('L2') if L2 is None else L2; R2 = f('R2') if R2 is None else R2
    B2 = f('B2') if B2 is None else B2; N2 = f('N2') if N2 is None else N2
    X = np.column_stack([V['N_sb'][u] / apt, V['f1624'][u], V['f6069'][u], V['f70'][u], V['fund'][u], V['fem'][u], f('comp1') / apt])
    nomes = ['p_sb', 'f1624', 'f6069', 'f70', 'fund', 'fem', 'C1']
    ys = {'a': (C2 - f('comp1')) / apt, 'm': ((L2 - R2) - (f('L1') - f('R1'))) / apt, 'L': (L2 - f('L1')) / apt, 'R': (R2 - f('R1')) / apt,
          'BN': ((B2 + N2) - (f('B1') + f('N1'))) / apt}
    g = B['locid'][u] if ef == 'loc' else B['munid'][u]
    out = {}
    for q in quais:
        r = fe_reg(ys[q], X, g, B['munid'][u], apt, nomes)
        out[q] = {'n': r['n'], 'grupos_ef': r['grupos_ef'], 'municipios': r['grupos_erro'], 'coef': r['coef'], 'ep': r['ep']}
    return out


def resumo_r1(o, nsb_nac):
    d = o['a']['coef']['p_sb']; ed = o['a']['ep']['p_sb']; g = o['m']['coef']['p_sb']; eg = o['m']['ep']['p_sb']
    return {'delta': d, 'ep_delta': ed, 'gamma_sb': g, 'ep_gamma_sb': eg, 'gamma_sobre_delta': (g / d) if d != 0 else None,
            'V1': d * nsb_nac, 'V1_inf95': (d - 1.96 * ed) * nsb_nac, 'V1_sup95': (d + 1.96 * ed) * nsb_nac,
            'V1_inf99': (d - 2.576 * ed) * nsb_nac, 'V1_sup99': (d + 2.576 * ed) * nsb_nac,
            'gamma_ic95': [g - 1.96 * eg, g + 1.96 * eg], 'n': o['a']['n'], 'locais_ou_municipios_ef': o['a']['grupos_ef'], 'municipios': o['a']['municipios']}


def r1_ano(ano, plantar=False):
    B = carregar_base(ano)
    M, tem, info = perfil_ligado(ano, B)
    V = variaveis_perfil(M)
    u = universo_r1(B, M, tem)
    nsb_nac = float(info['sem_biometria_perfil_brasil'])
    apt = B['apt1'][u].astype(float)
    base_ok = B['brasil'] & B['dois'] & B['apurada'] & (np.abs(B['apt2'] - B['apt1']) <= 2)
    dif = (M[:, 0] - B['apt1'])[base_ok & tem]
    res = {'perfil': info, 'universo': {'secoes': int(u.sum()), 'aptos': float(apt.sum()), 'N_sb_no_universo': float(V['N_sb'][u].sum()),
                                        'p_sb_medio_ponderado': float(V['N_sb'][u].sum() / apt.sum()),
                                        'sem_perfil': int((base_ok & ~tem).sum()), 'fora_por_diferenca_maior_que_10': int((np.abs(dif) > 10).sum()),
                                        'perfil_igual_aos_aptos': int((dif == 0).sum()), 'perfil_a_ate_2_dos_aptos': int((np.abs(dif) <= 2).sum())},
           'N_sb_nacional': nsb_nac}
    o = r1(B, u, V, quais=('a', 'm', 'L', 'R', 'BN'))
    res['regressoes_ef_local'] = o; res['resumo'] = resumo_r1(o, nsb_nac)
    om = r1(B, u, V, ef='mun', quais=('a', 'm', 'L', 'R'))
    res['regressoes_ef_municipio'] = om; res['resumo_ef_municipio'] = resumo_r1(om, nsb_nac)
    # sem controles de perfil (só C1), para mostrar o peso dos controles
    f = lambda k: B[k][u].astype(float)
    Xs = np.column_stack([V['N_sb'][u] / apt, f('comp1') / apt])
    ra = fe_reg((f('comp2') - f('comp1')) / apt, Xs, B['locid'][u], B['munid'][u], apt, ['p_sb', 'C1'])
    rm = fe_reg(((f('L2') - f('R2')) - (f('L1') - f('R1'))) / apt, Xs, B['locid'][u], B['munid'][u], apt, ['p_sb', 'C1'])
    res['sem_controles_de_perfil'] = {'delta': ce(ra, 'p_sb'), 'gamma_sb': ce(rm, 'p_sb')}
    # bruto por quinto de p_sb
    p = V['N_sb'][u] / apt
    q = np.quantile(p, [0.2, 0.4, 0.6, 0.8]); fx = np.searchsorted(q, p, side='right')
    a = f('comp2') - f('comp1'); m = (f('L2') - f('R2')) - (f('L1') - f('R1'))
    res['bruto_por_quinto_de_p_sb'] = [{'quinto': int(i + 1), 'secoes': int((fx == i).sum()), 'p_sb_medio': float(V['N_sb'][u][fx == i].sum() / apt[fx == i].sum()),
                                        'comparecimento_1t_sobre_aptos': float(f('comp1')[fx == i].sum() / apt[fx == i].sum()),
                                        'alta_comparecimento_pp': float(100 * a[fx == i].sum() / apt[fx == i].sum()),
                                        'ganho_de_margem_L_pp': float(100 * m[fx == i].sum() / apt[fx == i].sum()),
                                        'lula_2t_sobre_validos': float(f('L2')[fx == i].sum() / (f('L2')[fx == i].sum() + f('R2')[fx == i].sum()))} for i in range(5)]
    for nome, msk in (('PI_MA_TO_PB_CE', np.isin(B['uf'], UFS5)), ('demais_UFs', ~np.isin(B['uf'], UFS5))):
        oo = r1(B, u & msk, V); res['grupo_' + nome] = resumo_r1(oo, float(V['N_sb'][B['brasil'] & msk].sum()))
        res['grupo_' + nome]['N_sb_do_grupo'] = float(V['N_sb'][B['brasil'] & msk].sum())
    if plantar:
        pl = []
        nsb = V['N_sb'][u]; c2 = f('comp2')
        for K in (K25, K10, MARGEM):
            phi = K / nsb_nac; k = phi * nsb
            oi = r1(B, u, V, C2=c2 + k, L2=f('L2') + k)
            oe = r1(B, u, V, C2=c2 + k, L2=f('L2') + k * f('L2') / c2, R2=f('R2') + k * f('R2') / c2, B2=f('B2') + k * f('B2') / c2, N2=f('N2') + k * f('N2') / c2)
            oesp = r1(B, u, V, C2=c2 + k, R2=f('R2') + k)
            pl.append({'K': K, 'phi': phi, 'plantado_no_universo': float(k.sum()), 'insercao_L': resumo_r1(oi, nsb_nac),
                       'entrada_real_repartida_como_a_secao': resumo_r1(oe, nsb_nac), 'insercao_R_espelho': resumo_r1(oesp, nsb_nac)})
        res['plantios'] = pl
    return res


def contar_log(arq):
    sys.path.insert(0, D + '/adendo27/desenho_D2/scripts')
    import extrair_eventos_log as E
    p = arq.split('/')
    chave = f"{p[-5].upper()}|{int(p[-4])}|{int(p[-3])}|{int(p[-2])}"
    try: r = E.ler(arq)
    except Exception as ex: return chave, {'erro': str(ex)[:100]}
    o = {}
    for dia, t in (('04/10/2026', '1'), ('25/10/2026', '2')):
        x = r.get(dia)
        if not x or not x['votos']: continue
        c = {'ANO': 0, 'BIO': 0, 'MAN': 0, 'OUTRO': 0, 'hab': len(x['votos'])}
        for v in x['votos']:
            if v['t_comp'] is None: continue
            cl = v['classe']
            c['MAN' if cl.startswith('MAN') else cl if cl in ('ANO', 'BIO') else 'OUTRO'] += 1
        c['ANO_hab'] = sum(1 for v in x['votos'] if v['classe'] == 'ANO')
        o[t] = c
    return chave, o


def extrair_logs():
    import glob
    from multiprocessing import Pool
    fs = sorted(glob.glob(D + '/amostra2t/arq/*/*/*/*/*-log.jez'))
    with Pool(4) as p: out = dict(p.imap_unordered(contar_log, fs, chunksize=50))
    grava('logs_contagem.json', out)
    return out


def r2(B, V, info):
    cam = f'{TRAB}/logs_contagem.json'
    lg = json.load(open(cam)) if os.path.exists(cam) else extrair_logs()
    pos = {k: i for i, k in enumerate(B['chave'].tolist())}
    ordemL = [l.strip() for l in open(D + '/amostra2t/L_ordem.txt') if l.strip()]
    naL = set(k for k in lg if k in set(ordemL))
    nsb_nac = float(info['sem_biometria_perfil_brasil'])
    def conta(chaves, rot):
        ii = []; d = {k: [] for k in ('ANO1', 'ANO2', 'BM1', 'BM2', 'MAN1', 'MAN2', 'OUT1', 'OUT2')}
        for k in chaves:
            x = lg[k]
            if '1' not in x or '2' not in x or k not in pos: continue
            if B['urna1'][pos[k]] != B['urna2'][pos[k]]: continue   # urna trocada: o dia 04/10 do log pode ser de outra seção
            ii.append(pos[k])
            for t in ('1', '2'):
                d['ANO' + t].append(x[t]['ANO']); d['BM' + t].append(x[t]['BIO'] + x[t]['MAN']); d['MAN' + t].append(x[t]['MAN']); d['OUT' + t].append(x[t]['OUTRO'])
        ii = np.array(ii); d = {k: np.array(v, float) for k, v in d.items()}
        nsb = V['N_sb'][ii]; nbio = V['tot'][ii] - nsb
        S = nsb.sum(); tau1 = d['ANO1'].sum() / S; tau2 = d['ANO2'].sum() / S; dt = tau2 - tau1
        # linearização do estimador de razão, agrupado por local
        _, c = np.unique(B['locid'][ii], return_inverse=True); G = c.max() + 1
        e = (d['ANO2'] - d['ANO1'] - dt * nsb) / S
        ep = math.sqrt(G / (G - 1) * (np.bincount(c, weights=e) ** 2).sum())
        cb = d['BM2'].sum() / d['BM1'].sum(); ca = d['ANO2'].sum() / d['ANO1'].sum()
        # diferença de crescimento (ANO menos biométrico), com erro por local
        e2 = (d['ANO2'] - ca * d['ANO1']) / d['ANO1'].sum() - (d['BM2'] - cb * d['BM1']) / d['BM1'].sum()
        ep2 = math.sqrt(G / (G - 1) * (np.bincount(c, weights=e2) ** 2).sum())
        comp1 = B['comp1'][ii].astype(float); comp2 = B['comp2'][ii].astype(float)
        # EXPLORATÓRIO (depois de ver o resultado): variação do comparecimento em pontos do próprio grupo, biométrico menos sem biometria
        db_ = (d['BM2'] - d['BM1']).sum() / nbio.sum(); ds_ = (d['ANO2'] - d['ANO1']).sum() / S
        e3 = (d['BM2'] - d['BM1'] - db_ * nbio) / nbio.sum() - (d['ANO2'] - d['ANO1'] - ds_ * nsb) / S
        ep3 = math.sqrt(G / (G - 1) * (np.bincount(c, weights=e3) ** 2).sum())
        nbio_nac = float(info['eleitores_perfil_brasil'] - info['sem_biometria_perfil_brasil'])
        o = {'rotulo': rot, 'secoes': int(len(ii)), 'locais': int(G), 'N_sb_na_amostra': float(S), 'eleitores_com_biometria_na_amostra': float(nbio.sum()),
             'ANO_1t': float(d['ANO1'].sum()), 'ANO_2t': float(d['ANO2'].sum()), 'BIO_mais_MAN_1t': float(d['BM1'].sum()), 'BIO_mais_MAN_2t': float(d['BM2'].sum()),
             'MAN_1t': float(d['MAN1'].sum()), 'MAN_2t': float(d['MAN2'].sum()), 'OUTRO_1t': float(d['OUT1'].sum()), 'OUTRO_2t': float(d['OUT2'].sum()),
             'tau_1': float(tau1), 'tau_2': float(tau2), 'delta_tau': float(dt), 'ep_delta_tau': float(ep),
             'V2': float(dt * nsb_nac), 'V2_inf95': float((dt - 1.96 * ep) * nsb_nac), 'V2_sup95': float((dt + 1.96 * ep) * nsb_nac),
             'V2_inf99': float((dt - 2.576 * ep) * nsb_nac), 'V2_sup99': float((dt + 2.576 * ep) * nsb_nac),
             'crescimento_ANO': float(ca), 'crescimento_BIO_mais_MAN': float(cb), 'diferenca_de_crescimento': float(ca - cb), 'ep_diferenca_de_crescimento': float(ep2),
             'comparecimento_biometricos_1t': float(d['BM1'].sum() / nbio.sum()), 'comparecimento_biometricos_2t': float(d['BM2'].sum() / nbio.sum()),
             'excesso_ANO_sobre_crescimento_biometrico_na_amostra': float(d['ANO2'].sum() - cb * d['ANO1'].sum()),
             'excesso_ANO_nacional': float((d['ANO2'].sum() - cb * d['ANO1'].sum()) / S * nsb_nac),
             'exploratorio_did': {'variacao_biometricos_pp_do_grupo': float(100 * db_), 'variacao_sem_biometria_pp_do_grupo': float(100 * ds_),
                                  'diferenca_pp': float(100 * (db_ - ds_)), 'ep_pp': float(100 * ep3),
                                  'previsto_se_a_margem_inteira_entrasse_como_biometria_falsa_pp': float(100 * MARGEM / nbio_nac),
                                  'previsto_com_25_por_cento_da_margem_pp': float(100 * K25 / nbio_nac), 'previsto_com_10_por_cento_pp': float(100 * K10 / nbio_nac),
                                  'limite_superior_95_em_votos': float((db_ - ds_ + 1.96 * ep3) * nbio_nac),
                                  'faltosos_do_1t_que_voltaram_liquido_biometricos': float((d['BM2'] - d['BM1']).sum() / (nbio.sum() - d['BM1'].sum())),
                                  'faltosos_do_1t_que_voltaram_liquido_sem_biometria': float((d['ANO2'] - d['ANO1']).sum() / (S - d['ANO1'].sum())),
                                  'na_escala_por_faltoso_excesso_do_grupo_biometrico_em_votos': float(((d['BM2'] - d['BM1']).sum() / (nbio.sum() - d['BM1'].sum()) - (d['ANO2'] - d['ANO1']).sum() / (S - d['ANO1'].sum()))
                                                                                                     * (nbio.sum() - d['BM1'].sum()) / nbio.sum() * nbio_nac)},
             'conferencia_log_contra_bweb': {'soma_log_1t': float((d['ANO1'] + d['BM1'] + d['OUT1']).sum()), 'comp_bweb_1t': float(comp1.sum()),
                                             'soma_log_2t': float((d['ANO2'] + d['BM2'] + d['OUT2']).sum()), 'comp_bweb_2t': float(comp2.sum()),
                                             'secoes_com_diferenca_2t': int(((d['ANO2'] + d['BM2'] + d['OUT2']) != comp2).sum())}}
        pl = []
        for K in (K25, K10):
            phi = K / nsb_nac
            dt_p = (d['ANO2'].sum() + phi * S - d['ANO1'].sum()) / S
            pl.append({'K': K, 'phi': phi, 'V2_plantado': float(dt_p * nsb_nac), 'aumento_de_V2': float((dt_p - dt) * nsb_nac),
                       'aumento_em_erros_padrao': float(phi / ep)})
        o['plantios'] = pl
        return o
    todas = [k for k in sorted(lg)]
    res = {'logs_lidos': len(lg), 'logs_com_erro': sum(1 for v in lg.values() if 'erro' in v),
           'logs_com_os_dois_dias': sum(1 for v in lg.values() if '1' in v and '2' in v),
           'principal_todas_as_secoes_com_dois_dias': conta(todas, 'todas'),
           'prefixo_autoponderado_L': conta([k for k in ordemL if k in naL], 'L'),
           'fora_do_prefixo_L_M10_e_avulsas': conta([k for k in todas if k not in naL], 'M10 e avulsas')}
    return res


def parte2():
    t0 = time.time()
    res = {}
    res['R1_2026'] = r1_ano(2026, plantar=True)
    grava('parcial_parte2_r1_2026.json', res['R1_2026'])
    print('R1 2026', json.dumps(res['R1_2026']['resumo']), 'tempo %.0f' % (time.time() - t0), flush=True)
    B = carregar_base(2026); M, tem, info = perfil_ligado(2026, B); V = variaveis_perfil(M)
    res['R2_2026'] = r2(B, V, info)
    grava('parcial_parte2_r2.json', res['R2_2026'])
    print('R2', json.dumps({k: v for k, v in res['R2_2026']['principal_todas_as_secoes_com_dois_dias'].items() if k != 'plantios'}), flush=True)
    del B
    if os.path.exists(f'{TRAB}/perfil2022.npz'):
        res['R1_2022_placebo'] = r1_ano(2022)
        grava('parcial_parte2_r1_2022.json', res['R1_2022_placebo'])
        print('R1 2022', json.dumps(res['R1_2022_placebo']['resumo']), flush=True)
    else:
        print('perfil de 2022 ainda nao esta pronto', flush=True)
    grava('parcial_parte2.json', res)
    print('parte2 ok %.0f s' % (time.time() - t0), flush=True)


# ---------------------------------------------------------------------------------------------- R3: perfil de comparecimento
ZIP_COMPAR = {2026: D + '/adendo21/F15_dl_perfil2026/perfil_comparecimento_abstencao_2026.zip',
              2022: TRAB + '/dl_compar2022/perfil_comparecimento_abstencao_2022.zip',
              2018: TRAB + '/dl_compar2018/perfil_comparecimento_abstencao_2018.zip'}


def _compar_uf(arg):
    import pandas as pd, zipfile
    zp, nome = arg
    acc = None
    with zipfile.ZipFile(zp) as zf:
        with zf.open(nome) as f:
            for ch in pd.read_csv(f, sep=';', encoding='latin-1', chunksize=2000000, usecols=['NR_TURNO', 'CD_FAIXA_ETARIA', 'QT_APTOS', 'QT_COMPARECIMENTO', 'QT_ABSTENCAO']):
                g = ch.groupby(['NR_TURNO', 'CD_FAIXA_ETARIA'])[['QT_APTOS', 'QT_COMPARECIMENTO', 'QT_ABSTENCAO']].sum()
                acc = g if acc is None else acc.add(g, fill_value=0)
    return nome, {f'{int(t)}|{int(fx)}': [int(v) for v in row] for (t, fx), row in zip(acc.index, acc.values)}


def ler_compar(ano):
    cache = f'{TRAB}/compar_{ano}.json'
    if os.path.exists(cache): return json.load(open(cache))
    import zipfile
    from multiprocessing import Pool
    zp = ZIP_COMPAR[ano]
    nomes = [i.filename for i in zipfile.ZipFile(zp).infolist() if i.filename.lower().endswith('.csv') and 'BRASIL' not in i.filename.upper() and '_ZZ' not in i.filename.upper()]
    tot = {}
    with Pool(4) as p:
        for nome, d in p.imap_unordered(_compar_uf, [(zp, n) for n in nomes]):
            for k, v in d.items():
                t = tot.setdefault(k, [0, 0, 0])
                for j in range(3): t[j] += v[j]
    o = {'arquivos_por_uf': len(nomes), 'celulas': tot}
    json.dump(o, open(cache, 'w'))
    return o


GRUPOS_R3 = {'16 e 17': [1600, 1700], '18 a 24': [1800, 1900, 2000, 2124], '25 a 59': [2529, 3034, 3539, 4044, 4549, 5054, 5559],
             '60 a 69': [6064, 6569], '70 a 79': [7074, 7579], '80 a 89': [8084, 8589], '90 a 94': [9094], '95 a 99': [9599],
             '100 ou mais': [9999], '80 ou mais': [8084, 8589, 9094, 9599, 9999], '90 ou mais': [9094, 9599, 9999]}


def parte2r3():
    res = {'arquivo_2026': {'last_modified': 'Wed, 21 Oct 2026 16:40:26 GMT', 'etag': 'da985e4-65e5c6781db46', 'bytes': 229213668,
                            'conferido_em': '10/11/2026 04:40 UTC (pedido de cabeçalho ao CDN do TSE)', 'gerado_em': '13/10/2026'}}
    T = {}
    for ano in (2026, 2022):
        d = ler_compar(ano)
        turnos = sorted({k.split('|')[0] for k in d['celulas']})
        res[f'turnos_no_arquivo_{ano}'] = turnos
        for t in turnos:
            lin = {}
            for nome, cods in GRUPOS_R3.items():
                ap = sum(d['celulas'].get(f'{t}|{c}', [0, 0, 0])[0] for c in cods); co = sum(d['celulas'].get(f'{t}|{c}', [0, 0, 0])[1] for c in cods)
                lin[nome] = {'aptos': ap, 'comparecimento': co, 'T': co / ap if ap else None}
            ap = sum(v[0] for k, v in d['celulas'].items() if k.startswith(t + '|')); co = sum(v[1] for k, v in d['celulas'].items() if k.startswith(t + '|'))
            lin['total'] = {'aptos': ap, 'comparecimento': co, 'T': co / ap}
            T[f'{ano}_{t}t'] = lin
    res['T'] = T
    ref = lambda a: T[f'{a}_2t']['60 a 69']['T'] / T[f'{a}_1t']['60 a 69']['T']
    if '2022_2t' in T:
        res['sentinela_2022'] = {b: {'razao_2t_sobre_1t': T['2022_2t'][b]['T'] / T['2022_1t'][b]['T'], 'razao_60a69': ref(2022),
                                     'razao_relativa': T['2022_2t'][b]['T'] / T['2022_1t'][b]['T'] / ref(2022)} for b in ('90 a 94', '95 a 99', '100 ou mais', '90 ou mais', '80 ou mais', '70 a 79', '18 a 24', '16 e 17')}
        mx = max(T['2022_1t']['100 ou mais']['T'], T['2022_2t']['100 ou mais']['T'])
        res['nivel_100_ou_mais'] = {'2022_1t': T['2022_1t']['100 ou mais']['T'], '2022_2t': T['2022_2t']['100 ou mais']['T'], 'maior_de_2022': mx,
                                    '2026_1t': T['2026_1t']['100 ou mais']['T'], '2026_1t_menos_maior_de_2022_pp': 100 * (T['2026_1t']['100 ou mais']['T'] - mx),
                                    'limiar_do_registro_para_o_2t_de_2026': mx + 0.03}
        # plantio: 3 pontos na faixa de 100 ou mais sobre o maior de 2022, e razão relativa plantada de 1,15
        c = T['2026_1t']['100 ou mais']
        res['plantio_R3'] = {'T_2t_plantado_100_ou_mais': mx + 0.03, 'votos_que_isso_representa_na_faixa': (mx + 0.03 - c['T']) * c['aptos'],
                             'criterio_de_nivel_dispara': True,
                             'razao_relativa_plantada_se_60a69_repetir_2022': ((mx + 0.03) / c['T']) / ref(2022),
                             'criterio_de_razao_dispara': bool(((mx + 0.03) / c['T']) / ref(2022) > 1.15),
                             'aptos_90_ou_mais_2026': T['2026_1t']['90 ou mais']['aptos'], 'comparecimento_90_ou_mais_2026_1t': T['2026_1t']['90 ou mais']['comparecimento'],
                             'votos_para_razao_1.15_em_90_ou_mais': 0.15 * ref(2022) * T['2026_1t']['90 ou mais']['comparecimento']}
    res['tem_2t_de_2026'] = '2026_2t' in T
    grava('parcial_parte2_r3.json', res)
    print(json.dumps({k: v for k, v in res.items() if k != 'T'}, ensure_ascii=False)[:3000], flush=True)
    for k, lin in T.items(): print(k, {b: round(v['T'], 4) for b, v in lin.items()}, flush=True)


def _compar_uf2(arg):
    import pandas as pd, zipfile
    zp, nome = arg
    acc = None
    with zipfile.ZipFile(zp) as zf:
        with zf.open(nome) as f:
            for ch in pd.read_csv(f, sep=';', encoding='latin-1', chunksize=2000000, usecols=['NR_TURNO', 'SG_UF', 'CD_FAIXA_ETARIA', 'QT_APTOS', 'QT_COMPARECIMENTO']):
                g = ch.groupby(['NR_TURNO', 'SG_UF', 'CD_FAIXA_ETARIA'])[['QT_APTOS', 'QT_COMPARECIMENTO']].sum()
                acc = g if acc is None else acc.add(g, fill_value=0)
    return {f'{int(t)}|{uf}|{int(fx)}': [int(v) for v in row] for (t, uf, fx), row in zip(acc.index, acc.values)}


def exploratorio_idosos_por_uf():
    """EXPLORATÓRIO (decidido depois de ver o R3): comparecimento oficial por UF das faixas de 70 anos ou mais, 1º turno de 2026
    contra os dois turnos de 2022. Sem voto por candidato."""
    import zipfile
    from multiprocessing import Pool
    out = {}
    for ano in (2026, 2022):
        zp = ZIP_COMPAR[ano]
        nomes = [i.filename for i in zipfile.ZipFile(zp).infolist() if i.filename.lower().endswith('.csv') and 'BRASIL' not in i.filename.upper() and '_ZZ' not in i.filename.upper()]
        tot = {}
        with Pool(4) as p:
            for d in p.imap_unordered(_compar_uf2, [(zp, n) for n in nomes]):
                for k, v in d.items():
                    t = tot.setdefault(k, [0, 0]); t[0] += v[0]; t[1] += v[1]
        out[str(ano)] = tot
    grupos = {'70 a 79': [7074, 7579], '80 ou mais': [8084, 8589, 9094, 9599, 9999], '90 ou mais': [9094, 9599, 9999], '60 a 69': [6064, 6569], '18 a 24': [1800, 1900, 2000, 2124]}
    ufs = sorted({k.split('|')[1] for k in out['2026']})
    tab = {}
    for uf in ufs:
        lin = {}
        for g, cods in grupos.items():
            for rot, ano, t in (('2026_1t', '2026', '1'), ('2022_1t', '2022', '1'), ('2022_2t', '2022', '2')):
                ap = sum(out[ano].get(f'{t}|{uf}|{c}', [0, 0])[0] for c in cods); co = sum(out[ano].get(f'{t}|{uf}|{c}', [0, 0])[1] for c in cods)
                lin[f'{g}|{rot}'] = {'aptos': ap, 'comparecimento': co, 'T': co / ap if ap else None}
        tab[uf] = lin
    grava('exploratorio_idosos_por_uf.json', tab)
    for uf in ufs:
        l = tab[uf]
        print(uf, ' '.join('%s: %.3f/%.3f/%.3f' % (g, l[g + '|2022_1t']['T'], l[g + '|2022_2t']['T'], l[g + '|2026_1t']['T']) for g in ('70 a 79', '80 ou mais', '90 ou mais')), flush=True)
    return tab


# ---------------------------------------------------------------------------------------------- PARTE III: T32 por seção
def t32(B, u, V, C2=None, L2=None, R2=None, fatia='f70', boot=300, completo=True):
    f = lambda k: B[k][u].astype(float)
    apt = f('apt1'); mun = B['munid'][u]
    C2 = f('comp2') if C2 is None else C2; L2 = f('L2') if L2 is None else L2; R2 = f('R2') if R2 is None else R2
    dC = C2 - f('comp1'); a = dC / apt
    dL = (L2 - f('L1')) / apt; dR = (R2 - f('R1')) / apt
    ctrl = [f('O1') / apt, (f('B1') + f('N1')) / apt, f('L1') / apt, f('R1') / apt]; nc = ['O1', 'BN1', 'L1', 'R1']
    out = {}
    if completo:
        Xa = np.column_stack([V['f1617'][u], V['f1824'][u], V['f6069'][u], V['f70'][u]])
        r = fe_reg(100 * a, Xa, mun, mun, apt, ['f1617', 'f1824', 'f6069', 'f70'])
        out['a_regressao_idade'] = {'n': r['n'], 'municipios': r['grupos_erro'], 'coef': r['coef'], 'ep': r['ep']}
        r = fe_reg(100 * a, np.column_stack([Xa, f('comp1') / apt]), mun, mun, apt, ['f1617', 'f1824', 'f6069', 'f70', 'C1'])
        out['a_regressao_idade_com_C1'] = {'coef': r['coef'], 'ep': r['ep']}
        r = fe_reg(100 * a, np.column_stack([Xa, f('comp1') / apt]), B['locid'][u], mun, apt, ['f1617', 'f1824', 'f6069', 'f70', 'C1'])
        out['a_regressao_idade_com_C1_ef_local'] = {'coef': r['coef'], 'ep': r['ep']}
    x = V[fatia][u]
    q3 = np.quantile(x, [1 / 3, 2 / 3]); t3 = np.searchsorted(q3, x, side='right')
    q10 = float(np.quantile(x, 0.9)); top = x >= q10
    def inclin(msk, y, com_ctrl=True):
        X = np.column_stack([a[msk]] + ([c[msk] for c in ctrl] if com_ctrl else []))
        r = fe_reg(y[msk], X, mun[msk], mun[msk], apt[msk], ['a'] + (nc if com_ctrl else []))
        return {'coef': r['coef']['a'], 'ep': r['ep']['a'], 'n': r['n']}
    def bloco(msk):
        o = {'secoes': int(msk.sum()), 'aptos': float(apt[msk].sum()), 'fatia_media': float((x[msk] * apt[msk]).sum() / apt[msk].sum()),
             'alta_comparecimento_pp': float(100 * dC[msk].sum() / apt[msk].sum()), 'abstencao_1t': float(1 - f('comp1')[msk].sum() / apt[msk].sum()),
             'entrada_por_faltoso_do_1t': float(dC[msk].sum() / (apt[msk] - f('comp1')[msk]).sum()),
             'ganho_L_por_eleitor_a_mais': inclin(msk, dL), 'ganho_R_por_eleitor_a_mais': inclin(msk, dR), 'ganho_de_margem_por_eleitor_a_mais': inclin(msk, dL - dR)}
        if completo:
            o['ganho_L_sem_controles'] = inclin(msk, dL, False); o['ganho_R_sem_controles'] = inclin(msk, dR, False)
            o['razao_bruta_dL_sobre_dC'] = float((dL[msk] * apt[msk]).sum() / dC[msk].sum()); o['razao_bruta_dR_sobre_dC'] = float((dR[msk] * apt[msk]).sum() / dC[msk].sum())
        return o
    out['cortes'] = {'tercos': q3.tolist(), 'decil_superior': q10}
    out['tercos'] = [bloco(t3 == i) for i in range(3)]
    out['decil_superior'] = bloco(top); out['resto'] = bloco(~top)
    # alta do decil contra as demais seções dos mesmos municípios (padronização direta)
    G = mun.max() + 1
    at = np.bincount(mun[top], weights=apt[top], minlength=G); ct = np.bincount(mun[top], weights=dC[top], minlength=G)
    ar = np.bincount(mun[~top], weights=apt[~top], minlength=G); cr = np.bincount(mun[~top], weights=dC[~top], minlength=G)
    amb = (at > 0) & (ar > 0)
    tr = np.where(amb, cr / np.where(ar > 0, ar, 1), 0)
    taxa_top = ct[amb].sum() / at[amb].sum(); taxa_resto = (at[amb] * tr[amb]).sum() / at[amb].sum()
    rng = np.random.default_rng(SEMENTE + 3)
    idx = np.where(amb)[0]; rb = []; db = []
    for _ in range(boot):
        qq = rng.multinomial(len(idx), np.full(len(idx), 1.0 / len(idx))).astype(float)
        num = (qq * ct[idx]).sum() / (qq * at[idx]).sum(); den = (qq * at[idx] * tr[idx]).sum() / (qq * at[idx]).sum()
        rb.append(num / den if den != 0 else np.nan); db.append(num - den)
    out['alta_decil_contra_demais_do_municipio'] = {'municipios_com_os_dois_grupos': int(amb.sum()), 'aptos_do_decil_nesses_municipios': float(at[amb].sum()),
                                                    'taxa_decil_pp': float(100 * taxa_top), 'taxa_demais_padronizada_pp': float(100 * taxa_resto),
                                                    'razao': float(taxa_top / taxa_resto) if taxa_resto != 0 else None,
                                                    'ep_razao_reamostragem': float(np.nanstd(rb, ddof=1)) if boot else None,
                                                    'diferenca_pp': float(100 * (taxa_top - taxa_resto)), 'ep_diferenca_pp': float(100 * np.std(db, ddof=1)) if boot else None,
                                                    'eleitores_a_mais_no_decil_alem_da_taxa_das_demais': float((taxa_top - taxa_resto) * at[amb].sum())}
    # diferença de ganho de Lula entre decil e resto num modelo único (efeito fixo de município x grupo, regressores abertos por grupo)
    def difer(y):
        cols = []; nomes = []
        for gnome, msk in (('top', top), ('resto', ~top)):
            for v, nm in zip([a] + ctrl, ['a'] + nc):
                cols.append(np.where(msk, v, 0.0)); nomes.append(f'{nm}_{gnome}')
        r = fe_reg(y, np.column_stack(cols), mun.astype(np.int64) * 2 + top, mun, apt, nomes, extra=True)
        Vm = r['_']['V']; i1 = nomes.index('a_top'); i2 = nomes.index('a_resto')
        d = r['coef']['a_top'] - r['coef']['a_resto']; ep = math.sqrt(Vm[i1, i1] + Vm[i2, i2] - 2 * Vm[i1, i2])
        return {'decil': r['coef']['a_top'], 'ep_decil': r['ep']['a_top'], 'resto': r['coef']['a_resto'], 'ep_resto': r['ep']['a_resto'], 'diferenca': d, 'ep_diferenca': ep, 'z': d / ep}
    out['ganho_L_decil_contra_resto'] = difer(dL)
    out['ganho_R_decil_contra_resto'] = difer(dR)
    g = out['ganho_L_decil_contra_resto']; al = out['alta_decil_contra_demais_do_municipio']
    cond_alta = (al['razao'] is not None and al['taxa_demais_padronizada_pp'] > 0 and al['razao'] >= 2) or (al['taxa_demais_padronizada_pp'] <= 0 and al['taxa_decil_pp'] > 0)
    sinal = bool(cond_alta and g['decil'] >= 0.9 and g['resto'] <= 0.6 and g['z'] > 4)
    gs = [b['ganho_L_por_eleitor_a_mais']['coef'] for b in out['tercos']]
    e3 = out['tercos'][2]['entrada_por_faltoso_do_1t'] / out['tercos'][0]['entrada_por_faltoso_do_1t']
    sem = bool((max(gs) - min(gs)) <= 0.1 and 0.8 <= e3 <= 1.25)
    out['criterio'] = {'alta_2_vezes': bool(cond_alta), 'ganho_decil_>=_0.9': bool(g['decil'] >= 0.9), 'ganho_resto_<=_0.6': bool(g['resto'] <= 0.6), 'diferenca_a_mais_de_4_ep': bool(g['z'] > 4),
                       'amplitude_do_ganho_L_entre_tercos': float(max(gs) - min(gs)), 'entrada_por_faltoso_terco_de_cima_sobre_o_de_baixo': float(e3),
                       'SINAL': sinal, 'SEM_SINAL': sem, 'veredito': 'SINAL' if sinal else ('SEM SINAL' if sem else 'INCONCLUSIVO')}
    return out


def parte3():
    t0 = time.time()
    res = {}
    for ano in (2026, 2022):
        if not os.path.exists(f'{TRAB}/perfil{ano}.npz'):
            print('perfil de', ano, 'ainda nao esta pronto', flush=True); continue
        B = carregar_base(ano); M, tem, info = perfil_ligado(ano, B); V = variaveis_perfil(M); u = universo_r1(B, M, tem)
        f = lambda k: B[k][u].astype(float)
        r = {'universo': {'secoes': int(u.sum()), 'aptos': float(f('apt1').sum()), 'N70_no_universo': float(V['N70'][u].sum()), 'N70_nacional': float(V['N70'][B['brasil']].sum()),
                          'N80_nacional': float(V['N80'][B['brasil']].sum()), 'N90_nacional': float(V['N90'][B['brasil']].sum()),
                          'N1624_nacional': float((V['N1617'] + V['N1824'])[B['brasil']].sum()), 'eleitores_perfil': float(V['tot'][B['brasil']].sum())}}
        r['principal_fatia_70_ou_mais'] = t32(B, u, V)
        r['espelho_fatia_16_a_24'] = t32(B, u, V, fatia='f1624', completo=False)
        for nome, msk in (('PI_MA_TO_PB_CE', np.isin(B['uf'], UFS5)), ('demais_UFs', ~np.isin(B['uf'], UFS5))):
            r['grupo_' + nome] = t32(B, u & msk, V, completo=False, boot=100)
        coef = r['principal_fatia_70_ou_mais']['a_regressao_idade']
        r['leitura_em_votos'] = {'coef_f70_pp_por_unidade_de_fatia': coef['coef']['f70'],
                                 'comparecimento_a_mais_atribuivel_a_fatia_de_70_ou_mais': coef['coef']['f70'] / 100 * r['universo']['N70_nacional'],
                                 'limite_superior_95': (coef['coef']['f70'] + 1.96 * coef['ep']['f70']) / 100 * r['universo']['N70_nacional'],
                                 'limite_inferior_95': (coef['coef']['f70'] - 1.96 * coef['ep']['f70']) / 100 * r['universo']['N70_nacional']}
        if ano == 2026:
            pl = []
            n70 = V['N70'][u]; n70nac = r['universo']['N70_nacional']; c2 = f('comp2')
            for K in (K25, MARGEM):
                k = K / n70nac * n70
                ti = t32(B, u, V, C2=c2 + k, L2=f('L2') + k, completo=True, boot=100)
                te = t32(B, u, V, C2=c2 + k, L2=f('L2') + k * f('L2') / c2, R2=f('R2') + k * f('R2') / c2, completo=False, boot=100)
                tm = t32(B, u, V, C2=c2 + k, R2=f('R2') + k, completo=False, boot=100)
                def res_(t):
                    return {'criterio': t['criterio'], 'alta': {kk: t['alta_decil_contra_demais_do_municipio'][kk] for kk in ('taxa_decil_pp', 'taxa_demais_padronizada_pp', 'razao')},
                            'ganho_L_decil_contra_resto': t['ganho_L_decil_contra_resto'], 'ganho_R_decil_contra_resto': t['ganho_R_decil_contra_resto'],
                            'ganho_L_por_terco': [b['ganho_L_por_eleitor_a_mais']['coef'] for b in t['tercos']]}
                pl.append({'K': K, 'phi': K / n70nac, 'plantado_no_universo': float(k.sum()), 'insercao_L': res_(ti),
                           'coef_f70_plantado': ti['a_regressao_idade']['coef']['f70'], 'entrada_real': res_(te), 'insercao_R_espelho': res_(tm)})
                print('plantio T32 K', K, json.dumps(pl[-1]['insercao_L']['criterio']), flush=True)
            r['plantios'] = pl
        res[str(ano)] = r
        grava(f'parcial_parte3_{ano}.json', r)
        p = r['principal_fatia_70_ou_mais']
        print(ano, json.dumps(p['criterio']), json.dumps(p['alta_decil_contra_demais_do_municipio']), json.dumps(p['ganho_L_decil_contra_resto']), 'tempo %.0f' % (time.time() - t0), flush=True)
        del B
    grava('parcial_parte3.json', res)
    print('parte3 ok %.0f s' % (time.time() - t0), flush=True)


# ---------------------------------------------------------------------------------------------- exploratórios depois do resultado
def exploratorio_2018():
    """EXPLORATÓRIO (decidido depois de ver o R3): faixas etárias do perfil de comparecimento de 2018, para ver a tendência."""
    d = ler_compar(2018)
    T = {}
    for t in sorted({k.split('|')[0] for k in d['celulas']}):
        lin = {}
        for nome, cods in GRUPOS_R3.items():
            ap = sum(d['celulas'].get(f'{t}|{c}', [0, 0, 0])[0] for c in cods); co = sum(d['celulas'].get(f'{t}|{c}', [0, 0, 0])[1] for c in cods)
            lin[nome] = {'aptos': ap, 'comparecimento': co, 'T': co / ap if ap else None}
        ap = sum(v[0] for k, v in d['celulas'].items() if k.startswith(t + '|')); co = sum(v[1] for k, v in d['celulas'].items() if k.startswith(t + '|'))
        lin['total'] = {'aptos': ap, 'comparecimento': co, 'T': co / ap}
        T[f'2018_{t}t'] = lin
    grava('exploratorio_compar_2018.json', {'arquivos_por_uf': d['arquivos_por_uf'], 'T': T})
    for k, lin in T.items(): print(k, {b: (round(v['T'], 4) if v['T'] is not None else None) for b, v in lin.items()}, flush=True)


def exploratorio_ac_ap():
    """EXPLORATÓRIO (depois de ver a Parte I por UF): seções de AC, AP e RR com a maior queda de comparecimento em relação às
    vizinhas do mesmo prédio, para pedido de cadernos. Lista de estrutura mais a variação de L e R."""
    B = carregar_base(2026); u = universo4(B); U = monta_u(B, u)
    apt = U['apt1']; a = (U['comp2'] - U['comp1']) / apt
    r = residuo_local(a, apt, U['loc'])
    ch = B['chave'][u]
    out = {}
    for uf in ('AC', 'AP', 'RR'):
        m = np.where(U['uf'] == uf)[0]
        o = m[np.argsort(r[m])][:15]
        out[uf] = [{'secao': str(ch[i]), 'aptos': int(apt[i]), 'comparecimento_1t': int(U['comp1'][i]), 'comparecimento_2t': int(U['comp2'][i]),
                    'residuo_no_predio_pp': float(100 * r[i]), 'variacao_L': int(U['L2'][i] - U['L1'][i]), 'variacao_R': int(U['R2'][i] - U['R1'][i])} for i in o]
    grava('exploratorio_ac_ap_rr_secoes.json', out)
    return out


# ---------------------------------------------------------------------------------------------- relatório
def n_(x, c=4, s=False):
    if x is None: return 'n/d'
    t = f'{x:+.{c}f}' if s else f'{x:.{c}f}'
    return t.replace('.', ',')


def i_(x):
    return f'{int(round(x)):,}'.replace(',', '.')


def texto(res):
    P = []; W = P.append
    p1 = res['parte_I_D2-4']; p2 = res['parte_II_D2-3']; p3 = res['parte_III_T32']; v = res['veredito']
    AN = ('2014', '2018', '2022', '2026')
    pc = lambda x, c=1: n_(100 * x, c)
    W('R27_B3: RESERVATÓRIO E ELEITOR MARGINAL (Adendo 27, Onda B; contexto do Adendo 28)')
    W('')
    W('Registro: Adendo 27 (commit 2748895, 10/11/2026 00:16:42 UTC) e Adendo 28 (commit 938be19, 10/11/2026 04:36:33 UTC).')
    W(f"Decisões que o registro não fixa: gravadas no docstring de scripts/analisar_R27_B3.py antes de qualquer conta com voto (SHA-256 {res['registro']['docstring_gravado_antes_de_qualquer_conta_com_voto']['sha256'][:16]}..., 10/11/2026 04:49:16 UTC).")
    W('D2-3 e D2-4 são desenho cego. O T32 por seção é reteste da equipe vermelha: a escolha do que retestar é posterior ao dado antigo, o critério é novo.')
    W('Pergunta desta onda: a virada pelo comparecimento é mobilização desigual ou irregularidade no registro de quem votou? Este teste olha três')
    W('lugares onde "voto lançado em nome de quem faltou" deixaria marca: seções que sobem mais que as vizinhas de prédio, eleitores sem biometria e')
    W('eleitores muito idosos.')
    W('')
    W('VEREDITOS PELA LETRA')
    W(f"  D2-4 INCREMENTO (eleitor marginal dentro do prédio): {v['D2-4_INCREMENTO']}, com poder medido por plantio.")
    W(f"  D2-3 RESERVA: volume (R1 e R2) {v['D2-3_RESERVA_volume']}; sentinela R3 {v['D2-3_RESERVA_sentinela_R3']} (o TSE não publicou o 2º turno no perfil de")
    W(f"    comparecimento); teste inteiro pela letra {v['D2-3_teste_inteiro_pela_letra']}, porque o registro exige o R3 para dizer sem sinal.")
    W(f"  T32 por seção (equipe vermelha): {v['T32_por_secao']}. Pela letra cai em {p3['veredito_pela_letra_sem_olhar_o_poder']}; o critério de sinal não dispara nem com a margem")
    W('    inteira plantada em nome de eleitores de 70 anos ou mais, então não serve para acusar. O que ele mede é relatado.')
    W('  Resumo em uma frase: nas formas que este teste enxerga (inserção desigual entre seções do mesmo prédio, uso de eleitores sem biometria, uso de')
    W('  seções de eleitorado muito idoso) não há marca de voto lançado em nome de faltosos; a forma espalhada por igual e registrada como biometria')
    W('  continua fora do alcance.')
    W('')
    W('PARTE I. D2-4 INCREMENTO: PARA QUEM FOI O COMPARECIMENTO A MAIS, DENTRO DO MESMO PRÉDIO')
    W('  Conta: dentro de cada local, regressão do ganho de margem de Lula (em aptos) contra a variação do comparecimento (em aptos), com controles do')
    W('  1º turno, efeito fixo de local, erro por município. θ = margem ganha por eleitor a mais. θ0 = o que daria se o eleitor a mais votasse como o')
    W('  prédio. Θ = θ - θ0. Voto inserido para um candidato só puxa Θ para +1.')
    W('  ano    seções    locais   θ (ep)             θ0        Θ         ep de Θ por reamostragem')
    for a in AN:
        W(f"  {a}  {i_(p1['n'][a]):>8}  {i_(p1['locais'][a]):>7}  {n_(p1['theta'][a], 4, True)} ({n_(p1['ep_theta'][a])})  {n_(p1['theta0'][a], 4, True)}  {n_(p1['Theta'][a], 4, True)}   {n_(p1['ep_Theta_reamostragem'][a])}")
    W(f"  Valor bruto de 2026: Θ = {n_(p1['Theta']['2026'], 4, True)} (IC de 95% de {n_(p1['ic95_Theta_2026'][0], 4, True)} a {n_(p1['ic95_Theta_2026'][1], 4, True)}). Por eleitor a mais dentro do prédio, Lula ganha")
    W(f"  {n_(p1['metades']['theta_L']['2026'], 3)} e Flávio {n_(p1['metades']['theta_R']['2026'], 3)} (em 2022: {n_(p1['metades']['theta_L']['2022'], 3)} e {n_(p1['metades']['theta_R']['2022'], 3)}; em 2018: {n_(p1['metades']['theta_L']['2018'], 3)} e {n_(p1['metades']['theta_R']['2018'], 3)}; em 2014: {n_(p1['metades']['theta_L']['2014'], 3)} e {n_(p1['metades']['theta_R']['2014'], 3)}).")
    W('  O eleitor a mais se reparte quase meio a meio. Não vai inteiro para um candidato.')
    W(f"  Estatística primária: Θ_2026 - Θ_ref = {n_(p1['Theta_2026_menos_ref'], 4, True)} (ep {n_(p1['ep'])}; por reamostragem {n_(p1['ep_por_reamostragem'])}). Θ_ref = {n_(p1['Theta_ref'], 4, True)}. Maior Θ histórico")
    W(f"  {n_(p1['maior_Theta_historico'], 4, True)} (2022). Amplitude histórica {n_(p1['amplitude_historica'], 4)} (o limite que levaria a inconclusivo é 0,10; passou perto).")
    W(f"  Critério: sinal pede 0,15 ou mais e 0,10 acima do maior histórico; sem sinal pede módulo abaixo de 0,05 e cauda abaixo de 443.019 votos.")
    W(f"  Cauda (ii): {i_(res['detalhe']['parte1']['por_ano']['2026']['secundarias']['ii_cauda']['secoes_acima'])} seções com alta acima de 4 desvios robustos e {i_(res['detalhe']['parte1']['por_ano']['2026']['secundarias']['ii_cauda']['secoes_abaixo'])} com queda; assimetria de {i_(p1['assimetria_de_cauda_votos'])} votos. Veredito: {p1['veredito']}.")
    W('  Secundárias e placebos (sem limiar no registro):')
    d = res['detalhe']['parte1']['por_ano']
    W('   (i) dispersão da variação do comparecimento dentro do prédio: ' + '; '.join(f"{a} {n_(d[a]['secundarias']['i_dispersao']['dp_ponderado'])}" for a in AN) + '. A de 2026 é a maior dos quatro anos')
    W('       (de 4% a 10% acima). O registro não fixou limiar; é o único item desta parte que pende para a marca.')
    W('   (iii) entre locais do mesmo município: Θ ' + '; '.join(f"{a} {n_(p1['iii_entre_locais']['Theta'][a], 3, True)}" for a in AN) + f". 2026 menos a referência: {n_(p1['iii_entre_locais']['Theta_2026_menos_ref'], 3, True)} (ep {n_(p1['iii_entre_locais']['ep'], 3)}).")
    W('   (iv) seções com comparecimento de 95% ou mais: ' + '; '.join(f"{a} {i_(d[a]['secundarias']['iv_comparecimento_95']['1t'])} no 1º turno e {i_(d[a]['secundarias']['iv_comparecimento_95']['2t'])} no 2º" for a in AN) + '.')
    W(f"       Valor bruto de 2026 na (iii), sem usar outros anos: se todo o +{n_(p1['iii_entre_locais']['Theta']['2026'], 3)} fosse inserção em prédios inteiros, seriam cerca de {i_(p1['iii_entre_locais']['K_bruto_se_metade_dos_predios'])} votos em metade dos prédios.")
    W(f"   Placebo branco e nulo: 2026 menos referência {n_(p1['placebo_branco_e_nulo']['Theta_2026_menos_ref'], 3, True)}. Sentido inverso (1º turno como suspeito): {n_(p1['placebo_sentido_inverso']['Theta_2026_menos_ref'], 3, True)}.")
    W(f"   Só PI, MA, TO, PB e CE (escolha não cega, feita conhecendo a Onda A): Θ " + '; '.join(f"{a} {n_(p1['grupo_PI_MA_TO_PB_CE']['Theta'][a], 3, True)}" for a in AN) + f"; 2026 menos referência {n_(p1['grupo_PI_MA_TO_PB_CE']['D'], 3, True)} (ep {n_(p1['grupo_PI_MA_TO_PB_CE']['ep'], 3)}).")
    W('  Calibração por plantio em 2026 (deslocamento de Θ; a fórmula do registro ao lado):')
    W('   K            fração   fórmula  inserção p/ Lula  entrada real  abstenção de Flávio  inserção p/ Flávio  prédios inteiros  (iii) prédios inteiros')
    for c in res['detalhe']['parte1']['plantios_2026']['cenarios']:
        W(f"   {i_(c['K']):>9}   {pc(c['f'], 0):>4}%   {n_(c['formula_registro'], 3)}    {n_(c['insercao_L']['deslocamento_de_Theta'], 3, True)}            {n_(c['entrada_real']['deslocamento_de_Theta'], 3, True)}        {n_(c['abstencao_R']['deslocamento_de_Theta'], 3, True)}               {n_(c['insercao_R_espelho']['deslocamento_de_Theta'], 3, True)}              {n_(c['predios_inteiros_insercao_L']['deslocamento_principal'], 3, True)}            {n_(c['predios_inteiros_insercao_L']['deslocamento_iii'], 3, True)}" + ('' if c['fisicamente_possivel_em_media'] else '   (passa da abstenção média)'))
    lv = p1['leitura_em_votos']
    W(f"   O teste enxerga a inserção desigual (o deslocamento fica de 10% a 35% abaixo da fórmula, porque a dispersão natural de 2026 é {n_(lv['dp_natural_calibrado_pelos_plantios'])} e não 0,016).")
    W('   Distingue as explicações: eleitor real que entra e vota como a seção não mexe em Θ; eleitor de Flávio que falta (abstenção pura) puxa Θ para')
    W('   baixo; inserção para Flávio (espelho) puxa para baixo. Só inserção para Lula puxa para cima. É cego para inserção igual em todas as seções do')
    W(f"   prédio (deslocamento {n_(res['detalhe']['parte1']['plantios_2026']['insercao_igual_em_todas_as_secoes_margem']['deslocamento'], 3, True)} com a margem inteira) e para prédios inteiros; a variante (iii) enxerga prédios inteiros.")
    W(f"   Limiar do sinal (0,15): 25% da margem só o atinge se couber em até {pc(lv['fracao_maxima_de_secoes_para_K25_dar_0.15'], 0)}% das seções (o registro dizia metade); a margem inteira, em até {pc(lv['fracao_maxima_de_secoes_para_a_margem_dar_0.15'], 0)}%.")
    W(f"   O sem sinal (0,05) exclui 25% da margem inserida em menos de {pc(lv['fracao_maxima_de_secoes_para_K25_dar_0.05'], 0)}% das seções e a margem inteira em menos de {pc(lv['fracao_maxima_de_secoes_para_a_margem_dar_0.05'], 0)}% (o registro dizia 78% e 98%).")
    k5 = lv['K_que_desloca_0.05_(limiar_do_sem_sinal)']; kb = lv['K_se_o_Theta_bruto_de_2026_fosse_todo_insercao_(sem_usar_outros_anos)']; ks = lv['idem_no_limite_superior_95']; kr = lv['K_no_limite_superior_95_de_Theta2026_menos_ref']
    W('  Tradução em votos de margem (cada voto inserido vale 1):')
    W(f"   Excluído pelo sem sinal: inserção desigual acima de {i_(k5['0.05'])} votos se concentrada em 5% das seções; {i_(k5['0.2'])} em 20%; {i_(k5['0.5'])} em 50%; {i_(k5['0.8'])} em 80%.")
    W(f"   Limite superior de 95% do excesso de 2026 sobre a referência: {i_(kr['0.05'])}; {i_(kr['0.2'])}; {i_(kr['0.5'])}; {i_(kr['0.8'])} (mesmas frações).")
    W(f"   Sem usar outros anos (o Léo suspeita deles): se TODO o Θ bruto de 2026 fosse inserção, seriam {i_(kb['0.05'])}; {i_(kb['0.2'])}; {i_(kb['0.5'])}; {i_(kb['0.8'])} votos")
    W(f"   (no limite superior de 95%: {i_(ks['0.05'])}; {i_(ks['0.2'])}; {i_(ks['0.5'])}; {i_(ks['0.8'])}), de 3% a 31% da margem conforme o espalhamento. O veredito sem sinal depende")
    W('   da comparação com 2014, 2018 e 2022; o teto sem essa comparação é o desta linha.')
    W('')
    W('PARTE II. D2-3 RESERVA: ELEITORES SEM BIOMETRIA E MUITO IDOSOS')
    r26 = p2['R1_2026']; r22 = p2['R1_2022_placebo']; q = p2['R2']; u1 = res['detalhe']['R1_2026']['universo']; pf = res['detalhe']['R1_2026']['perfil']
    W(f"  Perfil do eleitorado (cadastro de 14/07/2026): {i_(pf['eleitores_perfil_brasil'])} eleitores no Brasil, {i_(pf['sem_biometria_perfil_brasil'])} sem biometria ({pc(p2['parcela_dos_sem_biometria_no_eleitorado'])}%).")
    W(f"  {i_(pf['agregadas_somadas_na_principal'])} seções agregadas somadas na principal. Universo do R1: {i_(u1['secoes'])} seções ({i_(u1['fora_por_diferenca_maior_que_10'])} fora por diferença de mais de 10 entre perfil e aptos).")
    W('  R1 (censo, efeito fixo de local, controles de idade, instrução, sexo e comparecimento do 1º turno):')
    W(f"   2026: δ = {n_(r26['delta'], 4, True)} (ep {n_(r26['ep_delta'])}); γ_sb = {n_(r26['gamma_sb'], 4, True)} (ep {n_(r26['ep_gamma_sb'])}); n = {i_(r26['n'])} seções, {i_(r26['locais_ou_municipios_ef'])} locais, {i_(r26['municipios'])} municípios.")
    W(f"         V1 = δ × ΣN_sb = {i_(r26['V1'])} votos (IC de 95% de {i_(r26['V1_inf95'])} a {i_(r26['V1_sup95'])}). O sinal é o contrário do previsto pela hipótese:")
    W('         seção com mais eleitores sem biometria teve MENOS alta de comparecimento e MENOS ganho de margem para Lula que as vizinhas de prédio.')
    W(f"   2022 (placebo): δ = {n_(r22['delta'], 4, True)} (ep {n_(r22['ep_delta'])}); γ_sb = {n_(r22['gamma_sb'], 4, True)} (ep {n_(r22['ep_gamma_sb'])}); V1 = {i_(r22['V1'])}. Mesmo sinal, cinco vezes menor.")
    W(f"   Com efeito fixo de município (enxerga prédios inteiros): 2026 δ = {n_(p2['R1_2026_ef_municipio']['delta'], 4, True)}, γ_sb = {n_(p2['R1_2026_ef_municipio']['gamma_sb'], 4, True)}; 2022 δ = {n_(p2['R1_2022_ef_municipio']['delta'], 4, True)}, γ_sb = {n_(p2['R1_2022_ef_municipio']['gamma_sb'], 4, True)}.")
    W(f"   Metades em 2026: variação de Lula {n_(p2['R1_metades_2026']['L']['coef'], 4, True)} (ep {n_(p2['R1_metades_2026']['L']['ep'])}), de Flávio {n_(p2['R1_metades_2026']['R']['coef'], 4, True)} (ep {n_(p2['R1_metades_2026']['R']['ep'])}), de branco e nulo {n_(p2['R1_metades_2026']['BN']['coef'], 4, True)} (ep {n_(p2['R1_metades_2026']['BN']['ep'])}).")
    g5 = p2['R1_grupo_PI_MA_TO_PB_CE']
    W(f"   Só PI, MA, TO, PB e CE: δ = {n_(g5['delta'], 4, True)} (ep {n_(g5['ep_delta'])}), γ_sb = {n_(g5['gamma_sb'], 4, True)} (ep {n_(g5['ep_gamma_sb'])}). Nesses cinco estados há só {i_(g5['N_sb_do_grupo'])} eleitores sem")
    W('   biometria no total: o reservatório quase não existe justamente onde a Onda A achou o desvio do comparecimento.')
    W('   Valor bruto de 2026 por quinto da fração sem biometria (sem controles): alta do comparecimento de ' + ', '.join(n_(x['alta_comparecimento_pp'], 2) for x in p2['bruto_por_quinto_de_p_sb_2026']) + ' pontos')
    W('   e ganho de margem de Lula de ' + ', '.join(n_(x['ganho_de_margem_L_pp'], 2) for x in p2['bruto_por_quinto_de_p_sb_2026']) + ' pontos. No bruto a alta cresce com a fração sem biometria')
    W('   (essas seções tinham mais faltosos no 1º turno); com o comparecimento do 1º turno no modelo, como o registro manda, o sinal inverte.')
    W(f"  R2 (conta exata nos logs; {i_(q['secoes'])} seções da amostra antiga com a mesma urna nos dois turnos, {i_(q['locais'])} locais; soma das habilitações do log igual ao")
    W(f"   comparecimento do bweb nos dois turnos, {i_(q['conferencia_log_contra_bweb']['soma_log_1t'])} e {i_(q['conferencia_log_contra_bweb']['soma_log_2t'])}):")
    W(f"   comparecimento dos eleitores sem biometria: {pc(q['tau_1'], 2)}% no 1º turno e {pc(q['tau_2'], 2)}% no 2º (habilitações ANO {i_(q['ANO_1t'])} e {i_(q['ANO_2t'])} sobre {i_(q['N_sb_na_amostra'])} eleitores).")
    W(f"   Δτ = {n_(q['delta_tau'], 4, True)} (ep {n_(q['ep_delta_tau'])}). V2 = {i_(q['V2'])} votos no país (IC de 95% de {i_(q['V2_inf95'])} a {i_(q['V2_sup95'])}; de 99% até {i_(q['V2_sup99'])}).")
    W(f"   Grupo com biometria na mesma seção (placebo): cresceu {pc(q['crescimento_BIO_mais_MAN'] - 1, 2)}%; o sem biometria cresceu {pc(q['crescimento_ANO'] - 1, 2)}%. Diferença {n_(100 * q['diferenca_de_crescimento'], 2, True)} pontos (ep {n_(100 * q['ep_diferenca_de_crescimento'], 2)}).")
    W(f"   A marca (a) do desenho apareceu na direção (o sem biometria subiu mais), mas o volume é pequeno: acima do crescimento do grupo biométrico")
    W(f"   são {i_(q['excesso_ANO_nacional'])} votos no país ({pc(q['excesso_ANO_nacional'] / MARGEM)}% da margem). Do aumento de 2.960.239 no comparecimento, {pc(p2['parcela_do_aumento_do_comparecimento_que_veio_dos_sem_biometria'])}% veio de eleitores")
    W(f"   sem biometria, que são {pc(p2['parcela_dos_sem_biometria_no_eleitorado'])}% do eleitorado. Só no prefixo autoponderado da amostra: V2 = {i_(p2['R2_prefixo_L']['V2'])} (de {i_(p2['R2_prefixo_L']['V2_inf95'])} a {i_(p2['R2_prefixo_L']['V2_sup95'])}).")
    W('   A amostra de logs não é aleatória simples; o N1 refaz essa conta na amostra aleatória nova.')
    W(f"  V = max(V1, V2) = {i_(p2['V'])} (de {i_(p2['V_inf95'])} a {i_(p2['V_sup95'])}), {pc(p2['V'] / MARGEM)}% da margem. Limites superiores de V1 e de V2 abaixo de 443.019: volume {p2['veredito_volume_R1_R2']}.")
    a = p2['plantio_K25']; b = p2['plantio_K10']
    W(f"  Calibração: plantados 1.107.548 votos (φ = {pc(a['phi'], 2)}% dos sem biometria) em C2 e L2, o R1 devolve δ = {n_(a['insercao_L']['delta'], 4, True)} (subiu exatamente φ), γ_sb = {n_(a['insercao_L']['gamma_sb'], 4, True)},")
    W(f"   γ_sb/δ = {n_(a['insercao_L']['gamma_sobre_delta'], 2)}, e o R2 devolve V = {i_(a['insercao_L']['V'])}: o critério de sinal dispara. O R1 sozinho não dispararia (V1 plantado = {i_([x for x in res['detalhe']['R1_2026']['plantios'] if x['K'] == K25][0]['insercao_L']['V1'])},")
    W(f"   porque parte de δ negativo); quem enxerga o volume é a conta exata do R2. Com 443.019 plantados, V = {i_(b['insercao_L']['V'])}: entre os limiares, inconclusivo, como devia.")
    W(f"   Explicação inocente plantada (os mesmos eleitores entram e votam como a seção): δ igual, γ_sb = {n_(a['entrada_real']['gamma_sb'], 4, True)}, critério não dispara. O teste separa as")
    W(f"   duas pelo γ_sb. Espelho (inserção para Flávio): γ_sb = {n_(a['insercao_R_espelho']['gamma_sb'], 4, True)}, não dispara.")
    R3 = p2['R3']; T = R3['T']
    W('  R3 (faixas etárias, dado oficial): o arquivo de 2026 no ar em 10/11/2026 é o mesmo de 21/10 (gerado em 13/10) e só tem o 1º turno. INCONCLUSIVO pela letra.')
    W('   O que dá para ver (Brasil sem exterior; os arquivos de 2022 e 2018 não trazem o DF):')
    W('   faixa         2022 1º turno   2022 2º turno   razão   2026 1º turno')
    for fx in ('60 a 69', '70 a 79', '80 a 89', '90 a 94', '95 a 99', '100 ou mais'):
        W(f"   {fx:<12}  {pc(T['2022_1t'][fx]['T'], 2):>6}%         {pc(T['2022_2t'][fx]['T'], 2):>6}%         {n_(T['2022_2t'][fx]['T'] / T['2022_1t'][fx]['T'], 3)}   {pc(T['2026_1t'][fx]['T'], 2):>6}%")
    s22 = R3['sentinela_2022']
    W(f"   Sentinela em 2022 (placebo): razão relativa à faixa de 60 a 69 de {n_(s22['90 a 94']['razao_relativa'], 3)} (90 a 94), {n_(s22['95 a 99']['razao_relativa'], 3)} (95 a 99) e {n_(s22['100 ou mais']['razao_relativa'], 3)} (100 ou mais).")
    W('   O desenho supunha que 2022 ficaria abaixo de 1,05. Não ficou: o próprio 2022 passa do limiar de 1,15 que acusaria 2026. Pela letra, a cláusula')
    W('   de razão nunca daria sinal em 2026, e a sentinela em 2022 fica ela mesma acesa (o Léo suspeita de 2022).')
    W(f"   Plantio: 3 pontos a mais na faixa de 100 anos ou mais são {i_(R3['plantio_R3']['votos_que_isso_representa_na_faixa'])} votos e disparam a cláusula de nível (limiar de {pc(R3['nivel_100_ou_mais']['limiar_do_registro_para_o_2t_de_2026'], 2)}%);")
    W(f"   a razão de 1,15 nas faixas de 90 ou mais seriam cerca de {i_(R3['plantio_R3']['votos_para_razao_1.15_em_90_ou_mais'])} votos. A sentinela mede uso de nome de morto, não volume.")
    W('')
    W('PARTE III. T32 POR SEÇÃO (reteste da equipe vermelha)')
    c = p3
    r6 = c['regressao_idade_2026']; r2_ = c['regressao_idade_2022']
    W('  (a) Variação do comparecimento (pontos dos aptos) contra as fatias de idade, efeito fixo de município:')
    W(f"   2026: 16 e 17 {n_(r6['coef']['f1617'], 2, True)} (ep {n_(r6['ep']['f1617'], 2)}); 18 a 24 {n_(r6['coef']['f1824'], 2, True)} ({n_(r6['ep']['f1824'], 2)}); 60 a 69 {n_(r6['coef']['f6069'], 2, True)} ({n_(r6['ep']['f6069'], 2)}); 70 ou mais {n_(r6['coef']['f70'], 2, True)} ({n_(r6['ep']['f70'], 2)}).")
    W(f"   2022: 16 e 17 {n_(r2_['coef']['f1617'], 2, True)} (ep {n_(r2_['ep']['f1617'], 2)}); 18 a 24 {n_(r2_['coef']['f1824'], 2, True)} ({n_(r2_['ep']['f1824'], 2)}); 60 a 69 {n_(r2_['coef']['f6069'], 2, True)} ({n_(r2_['ep']['f6069'], 2)}); 70 ou mais {n_(r2_['coef']['f70'], 2, True)} ({n_(r2_['ep']['f70'], 2)}).")
    W(f"   Em 2026 a seção com mais eleitores de 70 anos ou mais subiu mais: lido como votos, {i_(c['leitura_em_votos_2026']['comparecimento_a_mais_atribuivel_a_fatia_de_70_ou_mais'])} de comparecimento a mais ligados a essa fatia")
    W(f"   (de {i_(c['leitura_em_votos_2026']['limite_inferior_95'])} a {i_(c['leitura_em_votos_2026']['limite_superior_95'])}); em 2022, {i_(c['leitura_em_votos_2022']['comparecimento_a_mais_atribuivel_a_fatia_de_70_ou_mais'])}. Isso some quando se controla o comparecimento do 1º turno")
    W(f"   (coeficiente de 70 ou mais {n_(c['regressao_idade_com_C1_2026']['coef']['f70'], 2, True)} em 2026 e {n_(c['regressao_idade_com_C1_2022']['coef']['f70'], 2, True)} em 2022): seção de idosos tem mais faltosos para voltar. Dentro do prédio, com esse")
    W(f"   controle: {n_(c['regressao_idade_com_C1_ef_local_2026']['coef']['f70'], 2, True)} (ep {n_(c['regressao_idade_com_C1_ef_local_2026']['ep']['f70'], 2)}) em 2026 contra {n_(c['regressao_idade_com_C1_ef_local_2022']['coef']['f70'], 2, True)} (ep {n_(c['regressao_idade_com_C1_ef_local_2022']['ep']['f70'], 2)}) em 2022. A regressão depende da especificação e não decide.")
    W('  (b) Por terço da fatia de 70 ou mais (alta do comparecimento; ganho por eleitor a mais de Lula e de Flávio, efeito fixo de município):')
    for rot, tt in (('2026', c['tercos_2026']), ('2022', c['tercos_2022'])):
        W(f"   {rot}: " + '; '.join(f"terço {k + 1}: alta {n_(t['alta_comparecimento_pp'], 2, True)} p.p., Lula {n_(t['ganho_L_por_eleitor_a_mais']['coef'], 3)}, Flávio {n_(t['ganho_R_por_eleitor_a_mais']['coef'], 3)}" for k, t in enumerate(tt)) + '.')
    al = c['alta_decil_2026']; a2 = c['alta_decil_2022']; gl = c['ganho_L_2026']; g2 = c['ganho_L_2022']; gr = c['ganho_R_2026']
    W('  (c) Decil de maior fatia de 70 ou mais contra as demais seções dos mesmos municípios:')
    W(f"   2026: alta de {n_(al['taxa_decil_pp'], 2)} p.p. contra {n_(al['taxa_demais_padronizada_pp'], 2)} (razão {n_(al['razao'], 2)}, ep {n_(al['ep_razao_reamostragem'], 2)}; diferença {n_(al['diferenca_pp'], 2, True)} p.p., ep {n_(al['ep_diferenca_pp'], 2)}); ganho de Lula por eleitor a mais")
    W(f"         {n_(gl['decil'], 3)} no decil e {n_(gl['resto'], 3)} no resto (diferença {n_(gl['diferenca'], 3, True)}, {n_(gl['z'], 1, True)} ep); o de Flávio, {n_(gr['decil'], 3)} e {n_(gr['resto'], 3)} ({n_(gr['z'], 1, True)} ep).")
    W(f"   2022: alta de {n_(a2['taxa_decil_pp'], 2)} p.p. contra {n_(a2['taxa_demais_padronizada_pp'], 2)} (razão {n_(a2['razao'], 2)}; diferença {n_(a2['diferenca_pp'], 2, True)} p.p., ep {n_(a2['ep_diferenca_pp'], 2)}); ganho de Lula {n_(g2['decil'], 3)} e {n_(g2['resto'], 3)} ({n_(g2['z'], 1, True)} ep).")
    W(f"   Critério de sinal: alta de 2 vezes ou mais (2026: {n_(al['razao'], 2)}, não) E ganho de Lula de 0,9 ou mais no decil (2026: {n_(gl['decil'], 2)}, não). Critério de sem sinal:")
    W(f"   ganho de Lula a até 0,1 entre os terços (amplitude {n_(c['criterio_2026']['amplitude_do_ganho_L_entre_tercos'], 3)}, sim) E alta proporcional aos faltosos do 1º turno (entrada por faltoso no terço de")
    W(f"   cima {n_(c['criterio_2026']['entrada_por_faltoso_terco_de_cima_sobre_o_de_baixo'], 2)} vezes a do terço de baixo; minha faixa era de 0,8 a 1,25; não). Pela letra: {c['veredito_pela_letra_sem_olhar_o_poder']}.")
    pm = c['plantio_margem']['insercao_L']; p25 = c['plantio_K25']['insercao_L']
    W(f"  Calibração: com 1.107.548 votos plantados em nome de eleitores de 70 ou mais (φ = {pc(c['plantio_K25']['phi'], 2)}% deles) a razão do decil vai a {n_(p25['alta']['razao'], 2)} e o ganho de Lula")
    W(f"   no decil a {n_(p25['ganho_L_decil_contra_resto']['decil'], 3)}; com a margem inteira (φ = {pc(c['plantio_margem']['phi'], 1)}%), razão {n_(pm['alta']['razao'], 2)} e ganho {n_(pm['ganho_L_decil_contra_resto']['decil'], 3)}. O limiar de 0,9 não é atingido nem assim: o critério de")
    W(f"   sinal da equipe vermelha é SEM PODER. O que responde ao plantio é o coeficiente de 70 ou mais em (a): de {n_(r6['coef']['f70'], 2)} para {n_(c['plantio_K25']['coef_f70_plantado'], 2)} com 25% da margem")
    W(f"   e {n_(c['plantio_margem']['coef_f70_plantado'], 2)} com a margem inteira. O observado ({n_(r6['coef']['f70'], 2)}) está {n_(r6['coef']['f70'] - r2_['coef']['f70'], 2)} acima de 2022 ({n_(r2_['coef']['f70'], 2)}); a entrada real plantada dá o mesmo coeficiente, então só o")
    W('   ganho por eleitor a mais separa as duas, e ele é igual dentro e fora do decil.')
    W(f"  Tradução em votos: eleitores a mais no decil, além da taxa das vizinhas de município: {i_(al['eleitores_a_mais_no_decil_alem_da_taxa_das_demais'])} em 2026 ({i_(a2['eleitores_a_mais_no_decil_alem_da_taxa_das_demais'])} em 2022). Pela repartição")
    W(f"   medida ({n_(gl['decil'], 3)} para Lula e {n_(gr['decil'], 3)} para Flávio), isso vale cerca de {i_(c['margem_no_decil_se_os_eleitores_a_mais_votaram_como_a_inclinacao'])} votos de margem. Se todos fossem votos inseridos para Lula, {pc(al['eleitores_a_mais_no_decil_alem_da_taxa_das_demais'] / MARGEM)}% da margem.")
    g5a = c['grupo_PI_MA_TO_PB_CE_2026']['alta_decil_contra_demais_do_municipio']; g5b = c['grupo_PI_MA_TO_PB_CE_2022']['alta_decil_contra_demais_do_municipio']; g5g = c['grupo_PI_MA_TO_PB_CE_2026']['ganho_L_decil_contra_resto']
    W(f"  Só PI, MA, TO, PB e CE: alta de {n_(g5a['taxa_decil_pp'], 2)} p.p. no decil contra {n_(g5a['taxa_demais_padronizada_pp'], 2)} nas demais (razão {n_(g5a['razao'], 1)}, ep {n_(g5a['ep_razao_reamostragem'], 1)}; diferença {n_(g5a['diferenca_pp'], 2, True)} p.p., ep {n_(g5a['ep_diferenca_pp'], 2)});")
    W(f"   em 2022 a diferença era {n_(g5b['diferenca_pp'], 2, True)} p.p. (ep {n_(g5b['ep_diferenca_pp'], 2)}). Ganho de Lula por eleitor a mais {n_(g5g['decil'], 3)} no decil e {n_(g5g['resto'], 3)} no resto. São {i_(g5a['eleitores_a_mais_no_decil_alem_da_taxa_das_demais'])} eleitores")
    W('   a mais no decil. A condição de "2 vezes" vale nesses cinco estados, a do ganho de 0,9 não.')
    e6 = c['espelho_16_a_24_2026']['alta_decil_contra_demais_do_municipio']
    W(f"  Espelho (fatia de 16 a 24 anos): o decil mais jovem subiu {n_(e6['taxa_decil_pp'], 2)} p.p. contra {n_(e6['taxa_demais_padronizada_pp'], 2)} das demais (diferença {n_(e6['diferenca_pp'], 2, True)}); em 2022 a diferença foi {n_(c['espelho_16_a_24_2022']['alta_decil_contra_demais_do_municipio']['diferenca_pp'], 2, True)}.")
    W('')
    W('EXPLORATÓRIOS (feitos depois de ver resultados; não entram em veredito)')
    pu = p1['por_uf_exploratorio']
    W('  E1. Θ por UF (27 contas; o acaso daria 1 ou 2 além de 2 ep). Além de 3,11 ep (corte para 27 comparações): AC e AP, com sinal NEGATIVO, e MG')
    W('   bem no limite (3,11), com sinal positivo.')
    for uf in ('AC', 'AP', 'RR', 'MG', 'SC', 'MS'):
        x = pu[uf]
        W(f"   {uf}: Θ {n_(x['Theta_2014'], 3, True)}; {n_(x['Theta_2018'], 3, True)}; {n_(x['Theta_2022'], 3, True)}; 2026 {n_(x['Theta_2026'], 3, True)} (ep {n_(x['ep_2026'], 3)}). 2026 menos referência {n_(x['D'], 3, True)} ({n_(x['z'], 1, True)} ep). Metades em 2026: Lula {n_(x['Theta_L_2026'], 3, True)}, Flávio {n_(x['Theta_R_2026'], 3, True)}. Equivale a {i_(x['votos_equivalentes_se_metade_das_secoes'])} votos se em metade das seções.")
    W('   Em AC, AP e RR o comparecimento caiu 5 a 7,5 pontos entre os turnos (como nos outros anos). Em 2026, dentro do prédio, a seção que caiu mais')
    W('   perdeu votos de Flávio além da proporção (Θ de Flávio positivo, de Lula negativo); em 2014, 2018 e 2022 era o contrário. É a assinatura da')
    W('   "abstenção pura" do plantio (eleitor de Flávio que não volta), desigual entre seções, e não de inserção para Lula. Em votos é pequeno (cerca de')
    W('   5 a 6 mil em cada estado), mas é o lugar onde caderno de votação separaria as duas leituras com menos seções.')
    W('   MG, SC e MS têm excesso positivo só por causa de 2014; contra 2022 sozinho dão ' + ', '.join(n_(pu[u]['Theta_2026'] - pu[u]['Theta_2022'], 3, True) for u in ('MG', 'SC', 'MS')) + '.')
    if res['exploratorios'].get('faixas_etarias_2018'):
        T18 = res['exploratorios']['faixas_etarias_2018']['T']
        W('  E2. Comparecimento oficial dos muito idosos, série (Brasil sem DF e sem exterior):')
        W(f"   80 anos ou mais: {pc(T18['2018_1t']['80 ou mais']['T'])}% e {pc(T18['2018_2t']['80 ou mais']['T'])}% (2018, 1º e 2º turno); {pc(T['2022_1t']['80 ou mais']['T'])}% e {pc(T['2022_2t']['80 ou mais']['T'])}% (2022); {pc(T['2026_1t']['80 ou mais']['T'])}% (2026, 1º turno, com o DF).")
        W(f"   70 a 79: {pc(T18['2018_1t']['70 a 79']['T'])}% e {pc(T18['2018_2t']['70 a 79']['T'])}%; {pc(T['2022_1t']['70 a 79']['T'])}% e {pc(T['2022_2t']['70 a 79']['T'])}%; {pc(T['2026_1t']['70 a 79']['T'])}%. 90 ou mais: {pc(T18['2018_1t']['90 ou mais']['T'], 2)}% e {pc(T18['2018_2t']['90 ou mais']['T'], 2)}%; {pc(T['2022_1t']['90 ou mais']['T'], 2)}% e {pc(T['2022_2t']['90 ou mais']['T'], 2)}%; {pc(T['2026_1t']['90 ou mais']['T'], 2)}%.")
        W(f"   Em votos: de 80 anos ou mais votaram {i_(T['2022_1t']['80 ou mais']['comparecimento'])} no 1º turno de 2022, {i_(T['2022_2t']['80 ou mais']['comparecimento'])} no 2º, e {i_(T['2026_1t']['80 ou mais']['comparecimento'])} no 1º turno de 2026.")
        W('   Em 2018 os muito idosos votaram igual nos dois turnos (razão de 1,03 a 1,04). O salto começa no 2º turno de 2022 (mais 19% nos de 80 ou mais,')
        W('   mais 29% nos de 90 ou mais) e o 1º turno de 2026 já está muito acima. Não é dado do 2º turno de 2026 nem aponta candidato: o salto de 2026')
        W('   é no turno que Flávio venceu e aparece em todas as UFs, inclusive nas dele. Explicações inocentes a testar (não testadas aqui): transporte gratuito')
        W('   no dia da eleição e depuração do cadastro (em BA, CE, MA, AM e PA os aptos de 90 ou mais caíram 40% a 57%, o que sobe a taxa sem')
        W('   subir os votos). O número de votantes, porém, subiu em toda parte. É a faixa onde "nome que ninguém reclama" mais cresceu na série, nos')
        W('   dois sentidos de leitura.')
    dd = q['exploratorio_did']
    W('  E4. O grupo sem biometria como controle da hipótese de "biometria falsa" (amostra de logs). Um programa que registrasse votos falsos como')
    W('   habilitação biométrica só poderia usar nomes de quem tem biometria no cadastro. Variação do comparecimento em pontos do próprio grupo:')
    W(f"   com biometria {n_(dd['variacao_biometricos_pp_do_grupo'], 2, True)}; sem biometria {n_(dd['variacao_sem_biometria_pp_do_grupo'], 2, True)}; diferença {n_(dd['diferenca_pp'], 2, True)} (ep {n_(dd['ep_pp'], 2)}). A margem inteira entrando como biometria falsa pediria")
    W(f"   {n_(dd['previsto_se_a_margem_inteira_entrasse_como_biometria_falsa_pp'], 2, True)} pontos a mais no grupo com biometria; 25% da margem, {n_(dd['previsto_com_25_por_cento_da_margem_pp'], 2, True)}. SE os dois grupos variassem igual sem fraude, o limite superior de 95% seria")
    W(f"   de {i_(dd['limite_superior_95_em_votos'])} votos. Mas essa hipótese NÃO foi testada, e a escala decide a conta: medido por faltoso do 1º turno, voltaram em saldo")
    W(f"   {pc(dd['faltosos_do_1t_que_voltaram_liquido_biometricos'])}% dos faltosos com biometria e {pc(dd['faltosos_do_1t_que_voltaram_liquido_sem_biometria'])}% dos sem biometria; se a régua fosse essa, sobrariam {i_(dd['na_escala_por_faltoso_excesso_do_grupo_biometrico_em_votos'])} votos no grupo com")
    W('   biometria. O faltoso sem biometria é em boa parte cadastro parado (quem nunca volta), então essa segunda régua exagera. Sem o mesmo dado de')
    W('   2022 (tipo de habilitação por turno) não há como escolher a régua: o E4 não é teto nem indício, é a conta que falta fazer com dado do TSE.')
    W('  E3. Lista para cadernos: resultados JSON, campo exploratorios.secoes_AC_AP_RR_para_cadernos (15 seções por UF com a maior queda de comparecimento')
    W('   em relação às vizinhas de prédio, com a variação de Lula e de Flávio). A marca do E1 é da média do estado: em parte dessas seções quem caiu')
    W('   foi Lula. A lista serve para conferir assinaturas contra o comparecimento, não aponta seção fraudada.')
    W('')
    W('A FAVOR DA TESE (ou que a mantém aberta)')
    W(f"  1. O comparecimento dos eleitores sem biometria cresceu mais que o dos demais na mesma seção ({pc(q['crescimento_ANO'] - 1, 2)}% contra {pc(q['crescimento_BIO_mais_MAN'] - 1, 2)}%, diferença a {n_(q['diferenca_de_crescimento'] / q['ep_diferenca_de_crescimento'], 0)} ep).")
    W(f"     É a marca (a) do desenho, na direção prevista. O excesso vale {i_(q['excesso_ANO_nacional'])} votos ({pc(q['excesso_ANO_nacional'] / MARGEM)}% da margem).")
    W(f"  2. Seções com mais idosos subiram mais (decil de 70 ou mais: {n_(al['diferenca_pp'], 2, True)} p.p. sobre as vizinhas; nos cinco estados da Onda A, {n_(g5a['diferenca_pp'], 2, True)} p.p., acima dos {n_(g5b['diferenca_pp'], 2, True)} de 2022).")
    W('  3. A dispersão da variação do comparecimento dentro do prédio é a maior dos quatro anos (0,0172 contra 0,0157 a 0,0165).')
    W('  4. O R3 não pôde rodar: o TSE ainda não publicou o perfil de comparecimento do 2º turno. Não há atraso anormal até aqui: o do 1º turno foi')
    W('     gerado 9 dias depois da votação e só subiu ao ar 17 dias depois; o 2º turno está no dia 16. E a série mostra salto do comparecimento dos')
    W('     muito idosos a partir do 2º turno de 2022 (E2), que ninguém explicou com dado.')
    W('  5. O teste é cego, por desenho, para comparecimento a mais espalhado por igual nas seções do prédio e registrado como biometria. É a forma que')
    W('     a Onda A deixou de pé. Ausência de marca aqui não a alcança.')
    W('CONTRA A TESE')
    W(f"  1. Dentro do prédio, o eleitor a mais de 2026 se repartiu como em 2022 ({n_(p1['metades']['theta_L']['2026'], 3)} para Lula e {n_(p1['metades']['theta_R']['2026'], 3)} para Flávio), e o excesso sobre o padrão é {n_(p1['Theta_2026_menos_ref'], 3, True)}")
    W(f"     (ep {n_(p1['ep'], 3)}). Voto inserido só para Lula em parte das seções daria de +0,13 a +0,84 nos plantios. Fica excluída inserção desigual acima de")
    W(f"     {i_(k5['0.05'])} a {i_(k5['0.8'])} votos, conforme o espalhamento.")
    W(f"  2. O reservatório sem biometria não prevê alta de comparecimento nem ganho de Lula (δ e γ_sb negativos), e a conta exata dos logs limita o canal")
    W(f"     a {i_(q['V2_sup95'])} votos (7,8% da margem) mesmo contando TODO o aumento desses eleitores como suspeito. Nos cinco estados da Onda A quase não")
    W(f"     há eleitor sem biometria ({i_(g5['N_sb_do_grupo'])}).")
    W(f"  3. Nas seções de eleitorado idoso o eleitor a mais não foi mais para Lula ({n_(gl['decil'], 3)} contra {n_(gl['resto'], 3)} no resto; para Flávio {n_(gr['decil'], 3)} contra {n_(gr['resto'], 3)}), e o")
    W('     padrão de subir mais onde há mais idosos existia igual em 2022.')
    W(f"  4. Saltos isolados de comparecimento quase não existem: {i_(res['detalhe']['parte1']['por_ano']['2026']['secundarias']['ii_cauda']['secoes_acima'])} seções acima de 4 desvios, {i_(res['detalhe']['parte1']['por_ano']['2026']['secundarias']['ii_cauda']['secoes_abaixo'])} abaixo, saldo de {i_(p1['assimetria_de_cauda_votos'])} votos.")
    W('  5. Onde há marca por UF (AC e AP), ela é de eleitor de Flávio que falta, não de voto a mais para Lula, e vale poucos milhares de votos.')
    W('')
    W('O QUE ISSO SIGNIFICA')
    W('  Para o Léo, em português direto: se alguém lançou votos em nome de quem faltou, não foi (a) em algumas seções mais que em outras do mesmo')
    W('  prédio, (b) usando eleitores sem biometria, nem (c) concentrando em seções de idosos com voto de um lado só. Essas três portas ficam fechadas')
    W(f"  até estes tetos: {pc(q['V2_sup95'] / MARGEM)}% da margem pelo eleitor sem biometria; {pc(al['eleitores_a_mais_no_decil_alem_da_taxa_das_demais'] / MARGEM)}% pelas seções de idosos; e, para inserção desigual entre seções, de {pc(k5['0.05'] / MARGEM, 0)}% da margem")
    W(f"  (se concentrada em 5% das seções) a {pc(k5['0.8'] / MARGEM, 0)}% (se espalhada por 80% delas). Quanto mais espalhada, menos este teste limita. A virada pelo comparecimento")
    W('  que a Onda A achou é, portanto, um fenômeno espalhado por igual dentro dos prédios: isso é o que mobilização (ou desmobilização) de verdade produz, e é')
    W('  também o que produziria um desvio feito no programa e registrado como biometria. Este teste não separa essas duas; quem separa é o N1 (por')
    W('  onde entraram os votos a mais), o perfil de comparecimento do 2º turno e, de vez, os cadernos de votação.')
    W('')
    W('PISTAS')
    W('  1. Cobrar do TSE o perfil de comparecimento do 2º turno de 2026. Com ele o R3 roda em minutos (modo parte2r3). Números que acusariam: faixa de')
    W(f"     100 anos ou mais acima de {pc(R3['nivel_100_ou_mais']['limiar_do_registro_para_o_2t_de_2026'], 2)}%, ou razão 2º sobre 1º turno das faixas de 90 ou mais acima de 1,15 vez a da faixa de 60 a 69.")
    W('  2. Cadernos de votação em AC e AP (lista do E3): é onde a saída de eleitores de Flávio foi desigual entre salas do mesmo prédio.')
    W('  3. Pedir ao TSE o comparecimento por seção, turno e faixa etária COM o tipo de habilitação (biometria, mesário, sem biometria), 2018 a 2026:')
    W('     responde de uma vez o salto dos muito idosos (E2) e a marca (a) do R2.')
    W('  4. Cruzar com o N1: se a variação de S na amostra aleatória ficar perto de 308 mil, as duas contas se confirmam.')
    W('')
    W('DESVIOS E DECISÕES')
    W('  Antes de rodar (no docstring): aptos do 1º turno como base; local do 1º turno; erro de Θ pela regressão (reamostragem ao lado); ordem do')
    W('  veredito; plantios sem teto de faltosos; explicações inocentes plantadas; metades θ_L e θ_R; faixa de 0,8 a 1,25 para "proporcional aos')
    W('  faltosos"; ganho por eleitor a mais definido como inclinação com controles; seções com diferença de mais de 10 entre perfil e aptos fora.')
    W('  Depois de ver resultado (marcados): (1) filtro de mesma urna no R2, posto depois de ver que 20 seções com urna trocada traziam no log do 1º')
    W(f"  turno votos de outra seção (sem o filtro V2 = 304.319; com ele {i_(q['V2'])}); (2) erro agrupado por local no DF, que tem um município só; (3) os")
    W('  arquivos de 2022 e 2018 do perfil de comparecimento não trazem o DF, descoberto depois; (4) T32 de 2022 como placebo (escrito no código antes')
    W('  de ver qualquer resultado da Parte III, mas fora do docstring); (5) veredito SEM PODER do T32 pela regra geral da tarefa; (6) E1, E2, E3 e E4.')
    W('  O R2 pede a "amostra L"; usei todas as seções com log dos dois dias e dei o prefixo autoponderado ao lado. Não usei a amostra aleatória nova')
    W('  (é do N1).')
    ct = res['contagem_de_testes']
    W(f"  Contagem: {ct['vereditos_com_criterio_registrado']} vereditos com critério registrado, {ct['sinais_pela_letra']} sinal; o acaso daria {n_(ct['sinais_esperados_por_acaso_a_5_por_cento'], 1)}. No exploratório por UF, {len(ct['exploratorio_por_uf']['alem_de_2_ep'])} de 27 além de 2 ep")
    W(f"  ({', '.join(ct['exploratorio_por_uf']['alem_de_2_ep'])}); o acaso daria {n_(ct['exploratorio_por_uf']['esperado_por_acaso_alem_de_2_ep'], 1)}.")
    W('  Conferências: fe_reg igual a lib.fe_ols quando o grupo do erro é o local (θ = 0,0710, ep 0,0030); contagem ANO do extrator D2 igual ao tipo S do')
    W('  extrator D1 em 7.733 de 7.772 pares seção e turno (99.519 contra 99.480); perfil de comparecimento do 1º turno de 2026 igual ao perfil por seção')
    W('  em todas as faixas etárias. Falta a conferência independente por outro agente.')
    W('')
    W('Arquivos: scripts/analisar_R27_B3.py; resultados/R27_B3_reservatorio_e_marginal.json; trabalho em /home/user/trabalho-eleicao/adendo27/R27_B3.')
    return '\n'.join(P) + '\n'


def relatorio():
    L = lambda nome: json.load(open(f'{TRAB}/{nome}'))
    P1 = L('parcial_parte1.json'); A1 = L('parcial_parte2_r1_2026.json'); A2 = L('parcial_parte2_r1_2022.json'); R2 = L('parcial_parte2_r2.json')
    R3 = L('parcial_parte2_r3.json'); T26 = L('parcial_parte3_2026.json'); T22 = L('parcial_parte3_2022.json')
    opc = lambda nome: json.load(open(f'{TRAB}/{nome}')) if os.path.exists(f'{TRAB}/{nome}') else None
    IDU = opc('exploratorio_idosos_por_uf.json'); C18 = opc('exploratorio_compar_2018.json'); ACAP = opc('exploratorio_ac_ap_rr_secoes.json')
    # ------------------------------------------------------------ Parte I
    Th = {a: P1['por_ano'][a]['principal']['m'] for a in ('2014', '2018', '2022', '2026')}
    hist = [Th[a]['Theta'] for a in ('2014', '2018', '2022')]
    ref = sum(hist) / 3; Dp = Th['2026']['Theta'] - ref
    epD = math.sqrt(Th['2026']['ep_theta'] ** 2 + sum(Th[a]['ep_theta'] ** 2 for a in ('2014', '2018', '2022')) / 9)
    epDb = math.sqrt(Th['2026']['ep_Theta_reamostragem'] ** 2 + sum(Th[a]['ep_Theta_reamostragem'] ** 2 for a in ('2014', '2018', '2022')) / 9)
    mx = max(hist); amp = max(hist) - min(hist)
    sec26 = P1['por_ano']['2026']['secundarias']
    cauda = sec26['ii_cauda']['assimetria_votos']
    sinal1 = bool(Dp >= 0.15 and Th['2026']['Theta'] >= mx + 0.10 and Th['2026']['Theta'] - 1.96 * Th['2026']['ep_theta'] > mx)
    sem1 = bool(abs(Dp) < 0.05 and abs(cauda) < K10 and amp <= 0.10)
    ver1 = 'SINAL' if sinal1 else ('SEM SINAL' if sem1 else 'INCONCLUSIVO')
    pl = P1['plantios_2026']; Anac = pl['aptos_nacionais']; th_obs = Th['2026']['theta']
    sn2 = []
    for c in pl['cenarios']:
        if c['K'] != K25: continue
        x = c['insercao_L']['deslocamento_de_Theta'] / (1 - th_obs); sk2 = (c['K'] / Anac) ** 2 * (1 - c['f']) / c['f']
        sn2.append(sk2 * (1 - x) / x)
    sn_ef = math.sqrt(sorted(sn2)[len(sn2) // 2 - 1] / 2 + sorted(sn2)[len(sn2) // 2] / 2)
    def K_de(desl, f):
        if desl <= 0: return 0.0
        x = min(desl / (1 - th_obs), 0.999)
        return Anac * math.sqrt(sn_ef ** 2 * x / (1 - x) * f / (1 - f))
    def f_lim(K, desl):
        x = desl / (1 - th_obs); r = K ** 2 / (Anac ** 2 * sn_ef ** 2 * x / (1 - x))
        return r / (1 + r)
    FS = (0.05, 0.20, 0.50, 0.80)
    def K_iii(desl):   # calibrado no plantio de prédios inteiros com 25% da margem em metade dos locais
        c5 = [c for c in pl['cenarios'] if c['K'] == K25 and c['f'] == 0.5][0]
        thi = P1['por_ano']['2026']['secundarias']['iii_entre_locais']['theta']
        x = c5['predios_inteiros_insercao_L']['deslocamento_iii'] / (1 - thi); sn2i = (K25 / Anac) ** 2 * (1 - x) / x
        xx = min(desl / (1 - thi), 0.999)
        return Anac * math.sqrt(sn2i * xx / (1 - xx)) if desl > 0 else 0.0
    leit = {'dp_natural_calibrado_pelos_plantios': sn_ef,
            'K_que_desloca_0.05_(limiar_do_sem_sinal)': {str(f): K_de(0.05, f) for f in FS},
            'K_que_desloca_0.15_(limiar_do_sinal)': {str(f): K_de(0.15, f) for f in FS},
            'K_no_limite_superior_95_de_Theta2026_menos_ref': {str(f): K_de(Dp + 1.96 * epD, f) for f in FS},
            'K_se_o_Theta_bruto_de_2026_fosse_todo_insercao_(sem_usar_outros_anos)': {str(f): K_de(Th['2026']['Theta'], f) for f in FS},
            'idem_no_limite_superior_95': {str(f): K_de(Th['2026']['Theta'] + 1.96 * Th['2026']['ep_theta'], f) for f in FS},
            'fracao_maxima_de_secoes_para_K25_dar_0.15': f_lim(K25, 0.15), 'fracao_maxima_de_secoes_para_K25_dar_0.05': f_lim(K25, 0.05),
            'fracao_maxima_de_secoes_para_a_margem_dar_0.15': f_lim(MARGEM, 0.15), 'fracao_maxima_de_secoes_para_a_margem_dar_0.05': f_lim(MARGEM, 0.05)}
    def serie(q, campo='Theta'):
        return {a: P1['por_ano'][a]['principal'][q][campo] for a in ('2014', '2018', '2022', '2026')}
    def dif_ref(q):
        v = serie(q); return v['2026'] - (v['2014'] + v['2018'] + v['2022']) / 3
    iii = {a: P1['por_ano'][a]['secundarias']['iii_entre_locais'] for a in ('2014', '2018', '2022', '2026')}
    Diii = iii['2026']['Theta'] - (iii['2014']['Theta'] + iii['2018']['Theta'] + iii['2022']['Theta']) / 3
    epDiii = math.sqrt(iii['2026']['ep_theta'] ** 2 + sum(iii[a]['ep_theta'] ** 2 for a in ('2014', '2018', '2022')) / 9)
    por_uf = {}
    for uf in sorted(P1['por_ano']['2026']['por_uf']):
        x = [P1['por_ano'][a]['por_uf'].get(uf, {}) for a in ('2014', '2018', '2022', '2026')]
        if any('Theta' not in v for v in x): continue
        d = x[3]['Theta'] - sum(v['Theta'] for v in x[:3]) / 3
        e = math.sqrt(x[3]['ep_theta'] ** 2 + sum(v['ep_theta'] ** 2 for v in x[:3]) / 9)
        por_uf[uf] = {'Theta_2014': x[0]['Theta'], 'Theta_2018': x[1]['Theta'], 'Theta_2022': x[2]['Theta'], 'Theta_2026': x[3]['Theta'], 'ep_2026': x[3]['ep_theta'],
                      'D': d, 'ep_D': e, 'z': d / e, 'Theta_L_2026': x[3]['Theta_L'], 'Theta_R_2026': x[3]['Theta_R'],
                      'Theta_R_historico': [v['Theta_R'] for v in x[:3]], 'Theta_L_historico': [v['Theta_L'] for v in x[:3]],
                      'aptos_2026': x[3]['aptos'], 'variacao_media_do_comparecimento_2026': x[3]['variacao_media_do_comparecimento'],
                      'votos_equivalentes_se_metade_das_secoes': x[3]['aptos'] * math.sqrt(sn_ef ** 2 * min(abs(d) / (1 - th_obs), 0.999) / (1 - min(abs(d) / (1 - th_obs), 0.999)))}
    g5 = {a: P1['por_ano'][a]['grupos_de_uf']['PI_MA_TO_PB_CE'] for a in ('2014', '2018', '2022', '2026')}
    gd = {a: P1['por_ano'][a]['grupos_de_uf']['demais_UFs'] for a in ('2014', '2018', '2022', '2026')}
    def Dg(g, q='m'):
        d = g['2026'][q]['Theta'] - sum(g[a][q]['Theta'] for a in ('2014', '2018', '2022')) / 3
        e = math.sqrt(g['2026'][q]['ep_theta'] ** 2 + sum(g[a][q]['ep_theta'] ** 2 for a in ('2014', '2018', '2022')) / 9)
        return {'D': d, 'ep': e}
    parte1 = {'veredito': ver1, 'Theta': {a: Th[a]['Theta'] for a in Th}, 'theta': {a: Th[a]['theta'] for a in Th}, 'theta0': {a: Th[a]['theta0'] for a in Th},
              'ep_theta': {a: Th[a]['ep_theta'] for a in Th}, 'ep_Theta_reamostragem': {a: Th[a]['ep_Theta_reamostragem'] for a in Th},
              'n': {a: Th[a]['n'] for a in Th}, 'locais': {a: Th[a]['locais'] for a in Th}, 'municipios': {a: Th[a]['municipios'] for a in Th},
              'Theta_ref': ref, 'Theta_2026_menos_ref': Dp, 'ep': epD, 'ep_por_reamostragem': epDb, 'maior_Theta_historico': mx, 'amplitude_historica': amp,
              'ic95_Theta_2026': [Th['2026']['Theta'] - 1.96 * Th['2026']['ep_theta'], Th['2026']['Theta'] + 1.96 * Th['2026']['ep_theta']],
              'criterios': {'D>=0.15': bool(Dp >= 0.15), 'Theta26>=max+0.10': bool(Th['2026']['Theta'] >= mx + 0.10), '|D|<0.05': bool(abs(Dp) < 0.05),
                            'cauda<443019': bool(abs(cauda) < K10), 'amplitude_historica<=0.10': bool(amp <= 0.10)},
              'assimetria_de_cauda_votos': cauda, 'leitura_em_votos': leit,
              'metades': {'Theta_L': serie('L'), 'Theta_R': serie('R'), 'theta_L': serie('L', 'theta'), 'theta_R': serie('R', 'theta'),
                          'Theta_L_2026_menos_ref': dif_ref('L'), 'Theta_R_2026_menos_ref': dif_ref('R')},
              'placebo_branco_e_nulo': {'Theta': serie('BN'), 'Theta_2026_menos_ref': dif_ref('BN')},
              'placebo_sentido_inverso': {'Theta': serie('inv'), 'Theta_2026_menos_ref': dif_ref('inv')},
              'iii_entre_locais': {'Theta': {a: iii[a]['Theta'] for a in iii}, 'ep_theta': {a: iii[a]['ep_theta'] for a in iii}, 'Theta_2026_menos_ref': Diii, 'ep': epDiii,
                                   'K_bruto_se_metade_dos_predios': K_iii(iii['2026']['Theta'])},
              'grupo_PI_MA_TO_PB_CE': {'Theta': {a: g5[a]['m']['Theta'] for a in g5}, **Dg(g5), 'Theta_L': {a: g5[a]['L']['Theta'] for a in g5}, 'Theta_R': {a: g5[a]['R']['Theta'] for a in g5}},
              'grupo_demais_UFs': {'Theta': {a: gd[a]['m']['Theta'] for a in gd}, **Dg(gd)},
              'por_uf_exploratorio': por_uf}
    # ------------------------------------------------------------ Parte II
    r26 = A1['resumo']; r22 = A2['resumo']; p2 = R2['principal_todas_as_secoes_com_dois_dias']; pL = R2['prefixo_autoponderado_L']
    V1, V2 = r26['V1'], p2['V2']
    V = max(V1, V2); Vinf = r26['V1_inf95'] if V1 >= V2 else p2['V2_inf95']; Vsup = r26['V1_sup95'] if V1 >= V2 else p2['V2_sup95']
    sinal_vol = bool(V >= K25 and Vinf >= K10 and r26['gamma_ic95'][0] > 0 and r26['gamma_sobre_delta'] is not None and r26['delta'] > 0 and r26['gamma_sobre_delta'] >= 0.5
                     and r22['delta'] < r26['delta'] / 3)
    sem_vol = bool(r26['V1_sup95'] < K10 and p2['V2_sup95'] < K10)
    ver_vol = 'SINAL' if sinal_vol else ('SEM SINAL' if sem_vol else 'INCONCLUSIVO')
    plK25 = [x for x in A1['plantios'] if x['K'] == K25][0]; plK10 = [x for x in A1['plantios'] if x['K'] == K10][0]
    v2p25 = [x for x in p2['plantios'] if x['K'] == K25][0]; v2p10 = [x for x in p2['plantios'] if x['K'] == K10][0]
    def veria(pr1, pv2):
        Vp = max(pr1['V1'], pv2['V2_plantado']); infp = pr1['V1_inf95'] if pr1['V1'] >= pv2['V2_plantado'] else pv2['V2_plantado'] - 1.96 * p2['ep_delta_tau'] * A1['N_sb_nacional']
        return {'V': Vp, 'V_inf95': infp, 'gamma_sb': pr1['gamma_sb'], 'gamma_ic95': pr1['gamma_ic95'], 'gamma_sobre_delta': pr1['gamma_sobre_delta'], 'delta': pr1['delta'],
                'criterio_de_sinal_dispara': bool(Vp >= K25 and infp >= K10 and pr1['gamma_ic95'][0] > 0 and pr1['delta'] > 0 and pr1['gamma_sobre_delta'] >= 0.5 and r22['delta'] < pr1['delta'] / 3)}
    parte2 = {'veredito_volume_R1_R2': ver_vol, 'veredito_sentinela_R3': 'INCONCLUSIVO (o TSE não publicou o 2º turno de 2026 no perfil de comparecimento)',
              'veredito_do_teste_inteiro_pela_letra': 'INCONCLUSIVO' if ver_vol != 'SINAL' else 'SINAL',
              'R1_2026': r26, 'R1_2022_placebo': r22, 'R1_2026_ef_municipio': A1['resumo_ef_municipio'], 'R1_2022_ef_municipio': A2['resumo_ef_municipio'],
              'R1_metades_2026': {q: {'coef': A1['regressoes_ef_local'][q]['coef']['p_sb'], 'ep': A1['regressoes_ef_local'][q]['ep']['p_sb']} for q in ('L', 'R', 'BN')},
              'R1_metades_2022': {q: {'coef': A2['regressoes_ef_local'][q]['coef']['p_sb'], 'ep': A2['regressoes_ef_local'][q]['ep']['p_sb']} for q in ('L', 'R', 'BN')},
              'R1_grupo_PI_MA_TO_PB_CE': A1['grupo_PI_MA_TO_PB_CE'], 'R1_grupo_demais_UFs': A1['grupo_demais_UFs'],
              'R2': p2, 'R2_prefixo_L': pL, 'V': V, 'V_inf95': Vinf, 'V_sup95': Vsup,
              'plantio_K25': {'insercao_L': veria(plK25['insercao_L'], v2p25), 'entrada_real': veria(plK25['entrada_real_repartida_como_a_secao'], v2p25),
                              'insercao_R_espelho': veria(plK25['insercao_R_espelho'], v2p25), 'phi': plK25['phi']},
              'plantio_K10': {'insercao_L': veria(plK10['insercao_L'], v2p10), 'entrada_real': veria(plK10['entrada_real_repartida_como_a_secao'], v2p10), 'phi': plK10['phi']},
              'bruto_por_quinto_de_p_sb_2026': A1['bruto_por_quinto_de_p_sb'], 'bruto_por_quinto_de_p_sb_2022': A2['bruto_por_quinto_de_p_sb'],
              'parcela_do_aumento_do_comparecimento_que_veio_dos_sem_biometria': V2 / 2960239, 'parcela_dos_sem_biometria_no_eleitorado': A1['N_sb_nacional'] / A1['perfil']['eleitores_perfil_brasil'],
              'R3': R3}
    # ------------------------------------------------------------ Parte III
    c26 = T26['principal_fatia_70_ou_mais']; c22 = T22['principal_fatia_70_ou_mais']
    plm = [x for x in T26['plantios'] if x['K'] == MARGEM][0]; pl25 = [x for x in T26['plantios'] if x['K'] == K25][0]
    sem_poder3 = not plm['insercao_L']['criterio']['SINAL']
    ver3_letra = c26['criterio']['veredito']
    ver3 = 'SEM PODER' if (sem_poder3 and ver3_letra != 'SEM SINAL') else ver3_letra
    al = c26['alta_decil_contra_demais_do_municipio']; gl = c26['ganho_L_decil_contra_resto']; gr = c26['ganho_R_decil_contra_resto']
    parte3 = {'veredito': ver3, 'veredito_pela_letra_sem_olhar_o_poder': ver3_letra, 'criterio_2026': c26['criterio'], 'criterio_2022': c22['criterio'],
              'alta_decil_2026': al, 'alta_decil_2022': c22['alta_decil_contra_demais_do_municipio'],
              'ganho_L_2026': gl, 'ganho_R_2026': gr, 'ganho_L_2022': c22['ganho_L_decil_contra_resto'], 'ganho_R_2022': c22['ganho_R_decil_contra_resto'],
              'tercos_2026': c26['tercos'], 'tercos_2022': c22['tercos'],
              'regressao_idade_2026': c26['a_regressao_idade'], 'regressao_idade_2022': c22['a_regressao_idade'],
              'regressao_idade_com_C1_2026': c26['a_regressao_idade_com_C1'], 'regressao_idade_com_C1_2022': c22['a_regressao_idade_com_C1'],
              'regressao_idade_com_C1_ef_local_2026': c26['a_regressao_idade_com_C1_ef_local'], 'regressao_idade_com_C1_ef_local_2022': c22['a_regressao_idade_com_C1_ef_local'],
              'leitura_em_votos_2026': T26['leitura_em_votos'], 'leitura_em_votos_2022': T22['leitura_em_votos'],
              'margem_no_decil_se_os_eleitores_a_mais_votaram_como_a_inclinacao': al['eleitores_a_mais_no_decil_alem_da_taxa_das_demais'] * (gl['decil'] - gr['decil']),
              'plantio_K25': pl25, 'plantio_margem': plm, 'espelho_16_a_24_2026': T26['espelho_fatia_16_a_24'], 'espelho_16_a_24_2022': T22['espelho_fatia_16_a_24'],
              'grupo_PI_MA_TO_PB_CE_2026': T26['grupo_PI_MA_TO_PB_CE'], 'grupo_PI_MA_TO_PB_CE_2022': T22['grupo_PI_MA_TO_PB_CE'],
              'grupo_demais_UFs_2026': T26['grupo_demais_UFs'], 'universo_2026': T26['universo'], 'universo_2022': T22['universo']}
    sha_doc = open(f'{TRAB}/docstring_antes_de_rodar.sha256').read().split()
    res = {'teste': 'R27_B3: reservatório e eleitor marginal (D2-3, D2-4 e fragilidade "Comparecimento" com o T32 por seção)',
           'registro': {'adendo_27': 'commit 2748895, 10/11/2026 00:16:42 UTC', 'adendo_28': 'commit 938be19, 10/11/2026 04:36:33 UTC',
                        'docstring_gravado_antes_de_qualquer_conta_com_voto': {'sha256': sha_doc[0], 'hora': ' '.join(sha_doc[2:])},
                        'cego': 'D2-3 e D2-4 são desenho cego; o T32 por seção é reteste da equipe vermelha (escolha posterior ao dado antigo, critério novo)'},
           'veredito': {'D2-4_INCREMENTO': ver1, 'D2-3_RESERVA_volume': ver_vol, 'D2-3_RESERVA_sentinela_R3': 'INCONCLUSIVO', 'D2-3_teste_inteiro_pela_letra': parte2['veredito_do_teste_inteiro_pela_letra'],
                        'T32_por_secao': ver3},
           'parte_I_D2-4': parte1, 'parte_II_D2-3': parte2, 'parte_III_T32': parte3,
           'exploratorios': {'idosos_por_uf_1t_2026_contra_2022': IDU, 'faixas_etarias_2018': C18, 'secoes_AC_AP_RR_para_cadernos': ACAP},
           'detalhe': {'parte1': P1, 'R1_2026': A1, 'R1_2022': A2, 'R2': R2, 'T32_2026': T26, 'T32_2022': T22}}
    with open(f'{TRAB}/resumo_para_o_texto.json', 'w') as f:
        json.dump({k: v for k, v in res.items() if k != 'detalhe'}, f, ensure_ascii=False, indent=1)
    res['contagem_de_testes'] = {'vereditos_com_criterio_registrado': 4, 'sinais_pela_letra': 0, 'sinais_esperados_por_acaso_a_5_por_cento': 0.2,
                                 'exploratorio_por_uf': {'ufs': len(por_uf), 'alem_de_2_ep': sorted([u for u, v in por_uf.items() if abs(v['z']) > 2]),
                                                         'esperado_por_acaso_alem_de_2_ep': 0.0455 * len(por_uf),
                                                         'alem_do_limite_de_bonferroni_3.11': sorted([u for u, v in por_uf.items() if abs(v['z']) > 3.11])}}
    txt = texto(res)
    res['texto_sha256'] = hashlib.sha256(txt.encode()).hexdigest()
    with open(RAIZ + '/resultados/R27_B3_reservatorio_e_marginal.json', 'w') as f:
        json.dump(res, f, ensure_ascii=False, indent=1)
    with open(RAIZ + '/resultados/R27_B3_reservatorio_e_marginal.txt', 'w') as f:
        f.write(txt)
    print(txt)
    return res


# ---------------------------------------------------------------------------------------------- extrações sem voto (cópia dos scripts de trabalho)
NCOL_PERFIL = 12 + 2 * NF   # 0 total, 1 biometria, 2 mulheres, 3..10 instrução 1..8, 11 instrução outra, 12.. total por faixa, depois biometria por faixa


def _perfil_uf(z):
    """Perfil do eleitorado de um zip de UF, lido em fluxo (cópia de R27_B3/extrair_perfil.py, função um). SEM VOTOS."""
    import pandas as pd, zipfile
    ixf = {c: i for i, c in enumerate(FAIXAS)}
    uf = os.path.basename(z).split('_')[-1][:2].upper()
    acc = {}
    with zipfile.ZipFile(z) as zf:
        nome = [i.filename for i in zf.infolist() if i.filename.lower().endswith('.csv')][0]
        with zf.open(nome) as f:
            cab = pd.read_csv(f, sep=';', encoding='latin-1', nrows=0).columns.tolist()
        qcol = 'QT_ELEITORES' if 'QT_ELEITORES' in cab else 'QT_ELEITORES_PERFIL'
        ecol = 'CD_GRAU_ESCOLARIDADE' if 'CD_GRAU_ESCOLARIDADE' in cab else 'CD_GRAU_INSTRUCAO'
        with zf.open(nome) as f:
            for ch in pd.read_csv(f, sep=';', encoding='latin-1', chunksize=2000000,
                                  usecols=['CD_MUNICIPIO', 'NR_ZONA', 'NR_SECAO', 'CD_GENERO', 'CD_FAIXA_ETARIA', ecol, qcol, 'QT_ELEITORES_BIOMETRIA']):
                chave = ch['CD_MUNICIPIO'].to_numpy(np.int64) * 10 ** 8 + ch['NR_ZONA'].to_numpy(np.int64) * 10 ** 4 + ch['NR_SECAO'].to_numpy(np.int64)
                q = ch[qcol].to_numpy(np.int64); b = ch['QT_ELEITORES_BIOMETRIA'].to_numpy(np.int64)
                un, inv = np.unique(ch['CD_FAIXA_ETARIA'].to_numpy(np.int64), return_inverse=True)
                fidx = np.array([ixf.get(int(x), NF - 1) for x in un])[inv]
                es = ch[ecol].to_numpy(np.int64); eidx = np.where((es >= 1) & (es <= 8), es + 2, 11)
                uk, kinv = np.unique(chave, return_inverse=True)
                M = np.zeros((len(uk), NCOL_PERFIL), dtype=np.int64)
                M[:, 0] = np.bincount(kinv, weights=q, minlength=len(uk)); M[:, 1] = np.bincount(kinv, weights=b, minlength=len(uk))
                M[:, 2] = np.bincount(kinv, weights=q * (ch['CD_GENERO'].to_numpy() == 4), minlength=len(uk))
                np.add.at(M, (kinv, eidx), q); np.add.at(M, (kinv, 12 + fidx), q); np.add.at(M, (kinv, 12 + NF + fidx), b)
                for k, row in zip(uk.tolist(), M):
                    if k in acc: acc[k] += row
                    else: acc[k] = row.copy()
    ks = sorted(acc)
    return uf, np.array(ks, dtype=np.int64), np.array([acc[k] for k in ks], dtype=np.int32).reshape(len(ks), NCOL_PERFIL)


def extrair_perfil_2026():
    """Gera R27_B3/perfil2026.npz a partir dos zips do F15 (exterior fora)."""
    import glob
    from multiprocessing import Pool
    zips = [z for z in sorted(glob.glob(D + '/adendo21/F15_dl_perfil_secao/perfil_eleitor_secao_2026_*.zip')) if not z.upper().endswith('_ZZ.ZIP')]
    zips.sort(key=os.path.getsize, reverse=True)
    ufs = []; chaves = []; mats = []
    with Pool(3) as p:
        for uf, ks, M in p.imap_unordered(_perfil_uf, zips):
            ufs.append(np.array([uf] * len(ks))); chaves.append(ks); mats.append(M)
    np.savez_compressed(TRAB + '/perfil2026.npz', uf=np.concatenate(ufs), chave=np.concatenate(chaves), M=np.concatenate(mats), faixas=np.array(FAIXAS))


def baixar_perfil_2022():
    """Baixa o perfil por seção de 2022 (cdn.tse.jus.br), um zip por vez, agrega e apaga o zip (cópia de R27_B3/baixar_perfil2022.py).
    Intervalo de 1,2 s entre pedidos, para em qualquer 429, confere o tamanho com o content-length medido antes (dl_heads/heads_2022.txt)."""
    import subprocess
    esper = {}
    for l in open(TRAB + '/dl_heads/heads_2022.txt'):
        p = l.split()
        if len(p) > 3 and len(p[0]) == 2 and 'content-length:' in p: esper[p[0]] = int(p[p.index('content-length:') + 1])
    os.makedirs(TRAB + '/dl_perfil2022', exist_ok=True); os.makedirs(TRAB + '/perfil2022_partes', exist_ok=True)
    reg = {}
    for uf in sorted(esper, key=lambda u: esper[u]):
        arq = f'{TRAB}/dl_perfil2022/perfil_eleitor_secao_2022_{uf}.zip'; par = f'{TRAB}/perfil2022_partes/{uf}.npz'
        if os.path.exists(par): continue
        url = f'https://cdn.tse.jus.br/estatistica/sead/odsele/perfil_eleitor_secao/perfil_eleitor_secao_2022_{uf}.zip'
        for tentativa in range(3):
            r = subprocess.run(['curl', '-sS', '-o', arq, '-w', '%{http_code}', '--max-time', '1200', url], capture_output=True, text=True)
            cod = r.stdout.strip(); time.sleep(1.2)
            if cod == '429': print(uf, 'HTTP 429: PARADO', flush=True); sys.exit(2)
            if cod == '200' and os.path.getsize(arq) == esper[uf]: break
            if cod not in ('200', '000'): break
            time.sleep(10)
        if cod != '200' or os.path.getsize(arq) != esper[uf]: print(uf, 'falha', cod, flush=True); sys.exit(3)
        h = hashlib.sha256(open(arq, 'rb').read()).hexdigest()
        u_, ks, M = _perfil_uf(arq)
        np.savez_compressed(par, chave=ks, M=M)
        reg[uf] = {'bytes': esper[uf], 'sha256': h, 'secoes': int(len(ks)), 'eleitores': int(M[:, 0].sum()), 'biometria': int(M[:, 1].sum())}
        os.remove(arq)
    ufl = []; chl = []; ml = []
    for uf in sorted(esper):
        z = np.load(f'{TRAB}/perfil2022_partes/{uf}.npz')
        ufl.append(np.array([uf] * len(z['chave']))); chl.append(z['chave']); ml.append(z['M'])
    np.savez_compressed(TRAB + '/perfil2022.npz', uf=np.concatenate(ufl), chave=np.concatenate(chl), M=np.concatenate(ml), faixas=np.array(FAIXAS))
    return reg


if __name__ == '__main__':
    modo = sys.argv[1] if len(sys.argv) > 1 else ''
    if modo == 'parte1': parte1()
    elif modo == 'parte2': parte2()
    elif modo == 'parte2r3': parte2r3()
    elif modo == 'parte3': parte3()
    elif modo == 'relatorio': relatorio()
    elif modo == 'idosos_uf': exploratorio_idosos_por_uf()
    elif modo == 'expl2018': exploratorio_2018()
    elif modo == 'perfil2026': extrair_perfil_2026()
    elif modo == 'perfil2022': baixar_perfil_2022()
    elif modo == 'logs': extrair_logs()
    elif modo == 'acap': print(json.dumps(exploratorio_ac_ap(), indent=1))
    else: print(__doc__)
