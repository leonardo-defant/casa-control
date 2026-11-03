"""C2 do pré-registro (Adendo 24, commit ca110bb, 03/11/2026 04:24:10 UTC): digitais órfãs e o voto da seção.

Letra do registro
  - Por seção e por dia (25/10 e, quando a mesma urna, 04/10): votos liberados por digital que não estava em nenhum
    arquivo ("Não encontrou digital coletada em nenhum dos arquivos"), por digital gravada no dia, por mesário
    identificado e por biometria do eleitor.
  - Regressão dentro do local: fatia de Lula entre os finalistas no 2º turno contra a fração de votos liberados por
    digital órfã, com a fatia de Lula no 1º turno como controle; o coeficiente b estima quanto mais de Lula têm esses
    votos (o reel diz +0,156). Placebo: a mesma regressão com a fatia do 1º turno como variável e a fração de órfãs do
    2º turno como explicativa.
  - Sinal: b de 0,10 ou mais a mais de 4 erros-padrão. Sem sinal: |b| abaixo de 0,05 com erro-padrão até 0,025. Entre
    os dois: inconclusivo.

Decisões que o registro não fixa (escritas aqui antes de rodar a regressão e antes de olhar qualquer voto ao lado de
uma contagem de órfãs; declaradas como desvio no resultado)
  D1. Pacotes: os logs da pasta amostra2t/arq (um pacote por seção; as pastas sem log ficam fora e são contadas; com
      mais de um log no pacote, o de maior índice, o que não ocorre nesta amostra). Todos os blocos de log do pacote
      (decodificar._linhas_log, que inclui o log da urna original aninhado quando há contingência), aplicativo VOTA,
      linhas do dia 25/10/2026 (2º turno) e 04/10/2026 (1º turno).
  D2. Classe de cada "Eleitor foi habilitado", pela janela de mensagens desde o último "Identificador do eleitor
      digitado pelo mesário" (ou desde a habilitação anterior). Inspeção feita antes, nos 3.897 logs, só de combinações
      de mensagens (sem nenhum voto ao lado):
        B   biometria do eleitor: "Tipo de habilitação do eleitor [biométrica]" na janela. Também B, contada à parte
            (B_sem_linha): sem linha de tipo, sem pedido de dado pessoal e sem ano de nascimento, mas com "Capturada a
            digital" (47 no 2º turno e 24 no 1º na inspeção; as linhas de memória do sistema aparecem no lugar da
            linha de tipo).
        Liberação manual (eleitor com biometria cadastrada liberado sem ela, o que o bweb conta em
        QT_ELEI_BIOM_SEM_HABILITACAO): "Solicitação de dado pessoal do eleitor para habilitação manual" na janela, sem
        a linha biométrica. Depois de "Dado digitado confere", "Solicita digital do mesário"; a urna compara a digital
        com cada mesário registrado ("Batimento de digitais retornou o score N" e "Biometria coletada não é do mesário
        ...") e termina em uma de três mensagens:
          MI  mesário identificado: "Mesário N habilitou o eleitor" (subtipos: digital achada nos arquivos dos
              mesários registrados, "encontrada nos arquivos coletados", ou no cadastro de eleitores da seção,
              "encontrada em eleitores").
          DG  digital gravada no dia: "Digital coletada bate com uma digital gravada após o registro inicial de
              mesário. Não é possível associar a habilitação a um mesário." (bate com uma digital salva em arquivo novo
              antes; é o "mesário substituto com o mesmo dedo" do reel).
          OR  digital órfã: "Capturada a digital do mesário" e "Não encontrou digital coletada em nenhum dos arquivos,
              vai salvar a digital em novo arquivo." (a do reel e do Adendo 24).
          MX  liberação manual sem nenhuma das três (contada; não houve na inspeção).
        S   sem biometria cadastrada: "Ano de nascimento digitado é igual ao do cadastro", sem pedido de digital. Não é
            uma das quatro categorias do registro; é contada à parte e entra no denominador.
        X   nenhuma das anteriores (contada).
      Na inspeção, nenhuma janela teve mais de uma das três mensagens de autorização, e toda mensagem de digital órfã
      ou gravada foi seguida de habilitação.
  D3. "Votos liberados por": cada "O voto do eleitor foi computado" recebe a classe da última habilitação depois do voto
      anterior; voto sem habilitação antes (A3 do T3) e habilitação que não chega a voto são contados à parte. Fração
      da seção = votos da classe / votos computados no log do dia.
  D4. Amostra da regressão: seções com log lido, chave na base com os dois turnos, votos computados no log de 25/10
      acima de zero e L+R acima de zero nos dois turnos. Unidades em fração (0 a 1), não em pontos: y = L2/(L2+R2),
      x = votos OR / votos computados no log de 25/10, controle = L1/(L1+R1). Assim b se compara direto ao +0,156 do
      reel e aos limiares 0,10, 0,05 e 0,025 do registro.
  D5. Regressão: lib.fe_ols, efeito fixo de local (lib.chave_local com o local do 2º turno), peso L2+R2 (o registro não
      fixa o peso; é o de todos os testes do programa), erro agrupado por local (CR1). Locais com uma seção só na
      amostra não informam (fe_ols descarta).
  D6. Placebo: y = L1/(L1+R1), x = a mesma fração de órfãs do 2º turno, sem controle (o controle seria a própria
      variável), mesmo efeito fixo, peso e erro.
  D7. Veredito pela letra: SINAL se b >= 0,10 e b/ep > 4. SEM SINAL se |b| < 0,05 e ep <= 0,025. Senão INCONCLUSIVO.
      O placebo não muda o veredito; é lido ao lado.
  D8. Robustez fixada antes, fora do critério: (a) só logs completos (votos no log = comparecimento do bweb no 2º
      turno), com o comparecimento do bweb no denominador; (b) sem peso; (c) sem o controle do 1º turno; (d) efeito
      fixo de município, com controle; (e) efeito fixo de município sem controle (o mais perto do "dentro da mesma
      cidade" do reel); (f) as frações OR, DG, MI e S juntas (referência B), com controle; (g) mudança: virada
      s2 - s1 contra a variação da fração de órfãs (2º menos 1º turno), só seções com a mesma urna e log completo nos
      dois dias; (h) o 1º turno sozinho: s1 contra a fração de órfãs do 1º turno na mesma urna, sem controle (se a
      relação já aparece no turno que Flávio venceu, é composição do eleitorado e não desvio do 2º turno).
  D9. Modelo de urna pelas faixas do F4 (resultados/F4_modelo_urna.json, limites_usados, mesma regra de
      analisar_F4.classificar) sobre o número da urna da base em cada turno. "1º turno da mesma urna": urna do 1º turno
      igual à do 2º na base e votos no log de 04/10 iguais ao comparecimento do bweb no 1º turno.
  D10. Concentração (descritivo): seções com zero órfãs; fração das órfãs no 1%, 5% e 10% de seções com mais órfãs;
      Gini por seção, por local e por município; as 15 seções com mais órfãs; órfãs pelo número de mesários com digital
      comparada na seção (títulos distintos nas mensagens de comparação do dia).
  D11. Conferências: MI + DG + OR + MX por seção contra QT_ELEI_BIOM_SEM_HABILITACAO do bweb (cargo 1, lido com
      analisar_F6.ler_zip), entre os logs completos, nos dois turnos; linhas brutas da mensagem de órfã contra a classe
      OR; votos computados contra o comparecimento do bweb.
  D12. Score (descritivo): para cada liberação manual, as linhas "Batimento de digitais retornou o score N" da janela;
      para as órfãs, o maior score e se todos são zero (o "score zero" do reel).
  D13. Ordem de grandeza nacional (descritivo, sem peso amostral; a amostra é de municípios pequenos inteiros, locais
      sorteados e metade dos locais de 6 UFs): OR / (MI + DG + OR + MX) da amostra vezes o NH nacional do 2º turno no
      F6 (resultados/F6_sem_biometria.json, descritivo.universo.NH_2T), ao lado do 1,28 milhão do reel.

Acrescentado depois de ver o resultado pela letra (não muda o veredito; marcado como exploratório no resultado):
  E1. Conferência da regressão principal com dummies explícitas de local (numpy.linalg.lstsq) e erro agrupado contando
      as dummies na correção de amostra pequena (a convenção de lib.fe_ols conta só os regressores).
  E2. Placebo com efeito fixo de município (fatia do 1º turno contra a fração de órfãs do 2º, sem controle), para ler
      a robustez (e).
  E3. A conta ingênua: fatia de Lula das seções ponderada pelos votos órfãos contra a ponderada pelos votos
      biométricos, sem efeito fixo e dentro do município, no 2º turno e no 1º (mesma urna). É uma conta ecológica do tipo
      que pode produzir um "salto" sem que nenhum eleitor órfão vote diferente.
  E4. Os 10 municípios com mais órfãs: seções, órfãs e manuais nos dois turnos, virada da cidade e das seções com 10
      ou mais órfãs contra as outras da cidade (médias ponderadas por L2+R2).
  Correção de descritivo: o "score que bateu" do MI passa a ser lido só no subtipo "encontrada nos arquivos coletados"
  (no subtipo do cadastro de eleitores não há linha de score da comparação que bateu).

Uso:
  python3 -I analisar_C2_reel.py <pasta_arq> <secoes2026.json.gz> <zips_bweb_1T> <zips_bweb_2T> <F4.json> <F6.json> \
      <saida.json> <saida.txt>
"""
import os as _os, sys as _sys
_sys.path.insert(0, _os.path.dirname(_os.path.abspath(__file__)))
import collections, glob, json, math, os, re, sys, time
from multiprocessing import Pool
import numpy as np
from lib import carregar, chave_local, fe_ols

D1, D2 = '04/10/2026', '25/10/2026'
TURNO = {D1: '1', D2: '2'}
B_SINAL, Z_SINAL, B_SEM, EP_SEM = 0.10, 4.0, 0.05, 0.025
B_REEL = 0.156
RX = re.compile(r'^(\d\d/\d\d/\d{4}) (\d\d):(\d\d):(\d\d)$')
RX_MESOK = re.compile(r'^Mesário \d+ habilitou o eleitor')
RX_SCORE = re.compile(r'^Batimento de digitais retornou o score (-?\d+)')
RX_TIT = re.compile(r'[Mm]esário (\d+)')
MSG_ID = 'Identificador do eleitor digitado pelo mesário'
MSG_HAB = 'Eleitor foi habilitado'
MSG_VOTO = 'O voto do eleitor foi computado'
MSG_BIO = 'Tipo de habilitação do eleitor [biométrica]'
MSG_MAN = 'Solicitação de dado pessoal do eleitor para habilitação manual'
MSG_ANO = 'Ano de nascimento digitado é igual ao do cadastro'
MSG_NOVA = 'Não encontrou digital coletada em nenhum dos arquivos'
MSG_GRAV = 'Digital coletada bate com uma digital gravada após o registro inicial'
MSG_NAOCONF = 'Dado digitado não confere'
CLASSES = ('B', 'MI', 'DG', 'OR', 'MX', 'S', 'X')


def log(*a):
    print('#', time.strftime('%H:%M:%S'), *a, file=sys.stderr, flush=True)


# ------------------------------------------------------------------ leitura do log

def novo_dia():
    return {'hab': collections.Counter(), 'votos': collections.Counter(), 'computados': 0,
            'voto_sem_hab': 0, 'hab_sem_voto': 0, 'sub_MI': collections.Counter(), 'B_sem_linha': 0,
            'linhas_OR': 0, 'linhas_DG': 0, 'linhas_MI': 0, 'janelas_com_2_autorizacoes': 0,
            'nao_confere': 0, 'mesarios': set(), 'urnas': set(), 'blocos_com_voto': 0,
            'OR_max_score': [], 'OR_todos_zero': 0, 'OR_sem_score': 0, 'DG_score': [], 'MI_score': [],
            'DG_antes_da_primeira_OR_do_bloco': 0, 'OR_por_hora': collections.Counter(),
            'contingencia': False}


def classe_da_janela(win):
    """win: lista de mensagens desde o identificador. Devolve (classe, subtipo MI, B_sem_linha, n autorizações)."""
    tem = lambda p: any(w.startswith(p) for w in win)
    mi = any(RX_MESOK.match(w) for w in win)
    orf = tem(MSG_NOVA); dg = tem(MSG_GRAV)
    n_aut = int(mi) + int(orf) + int(dg)
    if MSG_BIO in win:
        return 'B', None, False, n_aut
    if MSG_MAN in win or any(w.startswith('Tipo de habilitação do eleitor [') for w in win):
        if mi:
            sub = 'arquivos_coletados' if any('encontrada nos arquivos coletados' in w for w in win) else \
                ('cadastro_de_eleitores' if any('encontrada em eleitores' in w for w in win) else 'outro')
            return 'MI', sub, False, n_aut
        if orf:
            return 'OR', None, False, n_aut
        if dg:
            return 'DG', None, False, n_aut
        return 'MX', None, False, n_aut
    if MSG_ANO in win:
        return 'S', None, False, n_aut
    if tem('Capturada a digital. Tentativa'):
        return 'B', None, True, n_aut
    return 'X', None, False, n_aut


def contar(caminho):
    from decodificar import _linhas_log
    blocos = _linhas_log(caminho)
    R = {D1: novo_dia(), D2: novo_dia()}
    for bl in blocos:
        win = []; pend = {D1: None, D2: None}; teve_or = {D1: False, D2: False}; votos_bloco = collections.Counter()
        for l in bl:
            x = l.split('\t')
            if len(x) < 5:
                continue
            dia = x[0][:10]
            if dia not in R:
                continue
            m = RX.match(x[0])
            if not m:
                continue
            msg = x[4]; r = R[dia]
            if msg.startswith('Modo de carga da UE - Urna de contingência') or msg.startswith('Contingência executada'):
                r['contingencia'] = True
            if x[3] != 'VOTA':
                continue
            r['urnas'].add(x[2])
            if msg.startswith(MSG_NOVA):
                r['linhas_OR'] += 1
            elif msg.startswith(MSG_GRAV):
                r['linhas_DG'] += 1
            elif RX_MESOK.match(msg):
                r['linhas_MI'] += 1
            elif msg == MSG_NAOCONF:
                r['nao_confere'] += 1
            if 'esário' in msg and ('Biometria' in msg or 'habilitou' in msg):
                t = RX_TIT.search(msg)
                if t:
                    r['mesarios'].add(t.group(1))
            if msg == MSG_ID:
                win = []
            win.append(msg)
            if msg == MSG_HAB:
                cl, sub, bsl, n_aut = classe_da_janela(win)
                r['hab'][cl] += 1
                if sub:
                    r['sub_MI'][sub] += 1
                if bsl:
                    r['B_sem_linha'] += 1
                if n_aut > 1:
                    r['janelas_com_2_autorizacoes'] += 1
                if cl in ('MI', 'DG', 'OR', 'MX'):
                    sc = [int(RX_SCORE.match(w).group(1)) for w in win if RX_SCORE.match(w)]
                    if cl == 'OR':
                        if sc:
                            r['OR_max_score'].append(max(sc))
                            if max(sc) == 0:
                                r['OR_todos_zero'] += 1
                        else:
                            r['OR_sem_score'] += 1
                        r['OR_por_hora'][int(m.group(2))] += 1
                        teve_or[dia] = True
                    elif cl == 'DG':
                        if sc:
                            r['DG_score'].append(sc[-1])
                        if not teve_or[dia]:
                            r['DG_antes_da_primeira_OR_do_bloco'] += 1
                    elif cl == 'MI' and sc and sub == 'arquivos_coletados':
                        r['MI_score'].append(sc[-1])
                if pend[dia] is not None:
                    r['hab_sem_voto'] += 1
                pend[dia] = cl
                win = []
            elif msg == MSG_VOTO:
                r['computados'] += 1; votos_bloco[dia] += 1
                if pend[dia] is None:
                    r['voto_sem_hab'] += 1
                else:
                    r['votos'][pend[dia]] += 1
                pend[dia] = None
        for dia in R:
            if votos_bloco[dia]:
                R[dia]['blocos_com_voto'] += 1
    out = {}
    for dia, r in R.items():
        o = dict(r)
        o['hab'] = {c: r['hab'].get(c, 0) for c in CLASSES}
        o['votos'] = {c: r['votos'].get(c, 0) for c in CLASSES}
        o['sub_MI'] = dict(r['sub_MI']); o['OR_por_hora'] = {str(h): v for h, v in sorted(r['OR_por_hora'].items())}
        o['n_mesarios'] = len(r['mesarios']); o['urnas'] = sorted(r['urnas']); del o['mesarios']
        out[TURNO[dia]] = o
    out['blocos'] = len(blocos)
    return caminho, out


# ------------------------------------------------------------------ apoio

def modelo_f4(u, F4):
    fx = F4['faixas']['faixas']
    lim = F4['faixas']['limites_usados']
    mn, mx = lim[0][0], lim[-1][1]
    if u is None or not isinstance(u, int) or u < mn or u > mx:
        return None
    for f in fx:
        if f['corte_superior'] is None or u < f['corte_superior']:
            return f['modelo']
    return None


def gini(v):
    v = np.sort(np.asarray(v, float))
    n = len(v)
    if n == 0 or v.sum() == 0:
        return None
    i = np.arange(1, n + 1)
    return float((2 * (i * v).sum()) / (n * v.sum()) - (n + 1) / n)


def topo(v, p):
    v = np.sort(np.asarray(v, float))[::-1]
    n = max(1, int(round(p * len(v))))
    return float(v[:n].sum() / v.sum()) if v.sum() else None


def reg(rows, y, xs, nomes, grupo='loc', peso='w'):
    Y = np.array([y(r) for r in rows], float)
    X = np.array([[f(r) for f in xs] for r in rows], float)
    g = np.array([r[grupo] for r in rows])
    w = np.array([r[peso] for r in rows], float) if peso else None
    o = fe_ols(Y, X, g, w, nomes)
    return o


def veredito(b, ep):
    if b >= B_SINAL and ep > 0 and b / ep > Z_SINAL:
        return 'SINAL'
    if abs(b) < B_SEM and ep <= EP_SEM:
        return 'SEM SINAL'
    return 'INCONCLUSIVO'


def dp_dentro(rows, f, grupo='loc'):
    """Desvio-padrão ponderado (peso w) de f dentro do grupo: a variação que identifica o coeficiente."""
    gs = collections.defaultdict(list)
    for r in rows:
        gs[r[grupo]].append(r)
    num = den = 0.0
    for g, rr in gs.items():
        if len(rr) < 2:
            continue
        ww = np.array([r['w'] for r in rr], float); vv = np.array([f(r) for r in rr], float)
        mu = (ww * vv).sum() / ww.sum()
        num += (ww * (vv - mu) ** 2).sum(); den += ww.sum()
    return math.sqrt(num / den) if den else None


# ------------------------------------------------------------------ principal

def main():
    pasta, basef, zips1, zips2, f4f, f6f, saida_json, saida_txt = sys.argv[1:9]
    t0 = time.time()
    base = carregar(basef); F4 = json.load(open(f4f)); F6 = json.load(open(f6f))
    dirs = sorted(glob.glob(os.path.join(pasta, '*', '*', '*', '*')))
    pacotes = []; sem_log = []
    for d in dirs:
        uf, m5, z4, s4 = d.split('/')[-4:]
        k = f'{uf.upper()}|{int(m5)}|{int(z4)}|{int(s4)}'
        lg = sorted((g for g in os.listdir(d) if g.endswith('-log.jez')), key=lambda s: int(s.split('-')[0]))
        if not lg:
            sem_log.append(k); continue
        pacotes.append((k, os.path.join(d, lg[-1]), len(lg)))
    log('pastas', len(dirs), 'com log', len(pacotes), 'sem log', len(sem_log))
    por_caminho = {p: k for k, p, _ in pacotes}
    S = {}
    with Pool(4) as pool:
        for i, (cam, o) in enumerate(pool.imap_unordered(contar, [p for _, p, _ in pacotes], chunksize=8)):
            S[por_caminho[cam]] = o
            if i % 500 == 0:
                log('logs lidos', i)
    log('logs lidos', len(S), f'{time.time() - t0:.0f}s')

    # NH do bweb (conferência), só as UFs da amostra
    import analisar_F6
    ufs = sorted({k.split('|')[0] for k in S})
    NH = {}
    with Pool(4) as pool:
        for t, pz in (('1', zips1), ('2', zips2)):
            zs = [z for z in glob.glob(os.path.join(pz, '*.zip')) if re.search(r'_(%s)_' % '|'.join(ufs), os.path.basename(z))]
            NH[t] = {}
            for nome, out, inc, inv, linhas in pool.imap_unordered(analisar_F6.ler_zip, zs):
                NH[t].update({k: v for k, v in out.items() if k in S})
            log('bweb', t, len(NH[t]))

    # tabela por seção
    secs = []
    for k, o in sorted(S.items()):
        b = base.get(k)
        r = {'k': k, 'logs_no_pacote': [n for kk, _, n in pacotes if kk == k][0], 'blocos': o['blocos']}
        r['na_base_dois_turnos'] = bool(b and '1' in b and '2' in b)
        if b and '2' in b:
            s2 = b['2']
            r.update({'loc': chave_local(k, s2), 'mun': '|'.join(k.split('|')[:2]), 'apt2': s2['apt'], 'comp2': s2['comp'],
                      'L2': s2['L'], 'R2': s2['R'], 'urna2': s2['urna'], 'tipo2': s2.get('tipo'),
                      'modelo2': modelo_f4(s2['urna'], F4)})
        if b and '1' in b:
            s1 = b['1']
            r.update({'comp1': s1['comp'], 'L1': s1['L'], 'R1': s1['R'], 'urna1': s1['urna'], 'modelo1': modelo_f4(s1['urna'], F4)})
        for t in '12':
            d = o[t]
            r['t' + t] = {kk: d[kk] for kk in ('hab', 'votos', 'computados', 'voto_sem_hab', 'hab_sem_voto', 'sub_MI',
                                               'B_sem_linha', 'linhas_OR', 'linhas_DG', 'linhas_MI', 'janelas_com_2_autorizacoes',
                                               'nao_confere', 'n_mesarios', 'urnas', 'blocos_com_voto', 'OR_todos_zero',
                                               'OR_sem_score', 'DG_antes_da_primeira_OR_do_bloco', 'OR_por_hora', 'contingencia')}
            r['t' + t]['OR_max_score'] = d['OR_max_score']; r['t' + t]['DG_score'] = d['DG_score']; r['t' + t]['MI_score'] = d['MI_score']
            nh = NH[t].get(k)
            r['t' + t]['NH_bweb'] = nh[3] if nh else None
            cbw = r.get('comp' + t)
            r['t' + t]['log_completo'] = cbw is not None and d['computados'] == cbw and cbw > 0
            v = d['votos']
            r['t' + t]['manual'] = sum(d['hab'][c] for c in ('MI', 'DG', 'OR', 'MX'))
        r['mesma_urna'] = r.get('urna1') is not None and r.get('urna1') == r.get('urna2')
        r['t1_mesma_urna_completo'] = r['mesma_urna'] and r['t1']['log_completo']
        secs.append(r)

    # conferências
    conf = {}
    for t in '12':
        comp_ok = [r for r in secs if r['t' + t]['log_completo'] and r['t' + t]['NH_bweb'] is not None]
        dif = collections.Counter(max(-3, min(3, r['t' + t]['manual'] - r['t' + t]['NH_bweb'])) for r in comp_ok)
        conf[t] = {'secoes_com_log': len(secs),
                   'log_completo': sum(1 for r in secs if r['t' + t]['log_completo']),
                   'com_votos_no_log': sum(1 for r in secs if r['t' + t]['computados'] > 0),
                   'manual_igual_NH_entre_completos': dif.get(0, 0), 'completos_com_NH': len(comp_ok),
                   'manual_menos_NH_distribuicao': {str(a): b for a, b in sorted(dif.items())},
                   'linhas_OR': sum(r['t' + t]['linhas_OR'] for r in secs), 'hab_OR': sum(r['t' + t]['hab']['OR'] for r in secs),
                   'linhas_DG': sum(r['t' + t]['linhas_DG'] for r in secs), 'hab_DG': sum(r['t' + t]['hab']['DG'] for r in secs),
                   'linhas_MI': sum(r['t' + t]['linhas_MI'] for r in secs), 'hab_MI': sum(r['t' + t]['hab']['MI'] for r in secs),
                   'janelas_com_2_autorizacoes': sum(r['t' + t]['janelas_com_2_autorizacoes'] for r in secs),
                   'voto_sem_hab': sum(r['t' + t]['voto_sem_hab'] for r in secs),
                   'hab_sem_voto': sum(r['t' + t]['hab_sem_voto'] for r in secs),
                   'contingencia': sum(1 for r in secs if r['t' + t]['contingencia'])}
    conf['1']['mesma_urna_na_base'] = sum(1 for r in secs if r['mesma_urna'])
    conf['1']['mesma_urna_e_log_1T_completo'] = sum(1 for r in secs if r['t1_mesma_urna_completo'])

    # totais por classe
    def totais(rr, t):
        h = collections.Counter(); v = collections.Counter(); sub = collections.Counter()
        for r in rr:
            h.update(r['t' + t]['hab']); v.update(r['t' + t]['votos']); sub.update(r['t' + t]['sub_MI'])
        comp = sum(r['t' + t]['computados'] for r in rr)
        man = sum(v[c] for c in ('MI', 'DG', 'OR', 'MX'))
        return {'secoes': len(rr), 'votos_computados': comp, 'habilitacoes': dict(h), 'votos': dict(v), 'subtipos_MI': dict(sub),
                'B_sem_linha': sum(r['t' + t]['B_sem_linha'] for r in rr),
                'pct_votos': {c: 100 * v[c] / comp if comp else None for c in CLASSES},
                'votos_manuais': man,
                'pct_das_manuais': {c: 100 * v[c] / man if man else None for c in ('MI', 'DG', 'OR', 'MX')}}
    tot = {'2T_todas': totais([r for r in secs if r['t2']['computados'] > 0], '2'),
           '1T_mesma_urna_completo': totais([r for r in secs if r['t1_mesma_urna_completo']], '1'),
           '2T_mesmas_secoes_do_1T': totais([r for r in secs if r['t1_mesma_urna_completo']], '2')}

    # amostra da regressão
    rows = []
    for r in secs:
        if not r['na_base_dois_turnos'] or r['t2']['computados'] <= 0:
            continue
        if r['L2'] + r['R2'] <= 0 or r['L1'] + r['R1'] <= 0:
            continue
        c2 = r['t2']['computados']; v2 = r['t2']['votos']
        q = {'k': r['k'], 'loc': r['loc'], 'mun': r['mun'], 'w': r['L2'] + r['R2'], 'w1': r['L1'] + r['R1'],
             's2': r['L2'] / (r['L2'] + r['R2']), 's1': r['L1'] / (r['L1'] + r['R1']),
             'f_OR': v2['OR'] / c2, 'f_DG': v2['DG'] / c2, 'f_MI': v2['MI'] / c2, 'f_S': v2['S'] / c2,
             'f_OR_bweb': v2['OR'] / r['comp2'] if r['comp2'] else None,
             'completo2': r['t2']['log_completo'], 'mesma_urna': r['mesma_urna'], 'completo1': r['t1_mesma_urna_completo'],
             'OR2': v2['OR'], 'c2': c2, 'B2': v2['B'], 'MI2': v2['MI'], 'DG2': v2['DG'], 'man2': r['t2']['manual'], 'man1': 0}
        if r['t1_mesma_urna_completo'] and r['t1']['computados'] > 0:
            q['f_OR1'] = r['t1']['votos']['OR'] / r['t1']['computados']; q['OR1'] = r['t1']['votos']['OR']
            q['B1'] = r['t1']['votos']['B']; q['man1'] = r['t1']['manual']
        rows.append(q)
    log('amostra da regressão', len(rows))

    principal = reg(rows, lambda r: r['s2'], [lambda r: r['f_OR'], lambda r: r['s1']], ['f_OR', 's1'])
    b = principal['coef']['f_OR']; ep = principal['ep']['f_OR']
    ver = veredito(b, ep)
    placebo = reg(rows, lambda r: r['s1'], [lambda r: r['f_OR']], ['f_OR'])
    log('principal', b, ep, ver)

    rob = {}
    cpl = [r for r in rows if r['completo2']]
    rob['a_so_logs_completos_denominador_bweb'] = reg(cpl, lambda r: r['s2'], [lambda r: r['f_OR_bweb'], lambda r: r['s1']], ['f_OR', 's1'])
    rob['b_sem_peso'] = reg(rows, lambda r: r['s2'], [lambda r: r['f_OR'], lambda r: r['s1']], ['f_OR', 's1'], peso=None)
    rob['c_sem_controle_1T'] = reg(rows, lambda r: r['s2'], [lambda r: r['f_OR']], ['f_OR'])
    rob['d_efeito_fixo_municipio'] = reg(rows, lambda r: r['s2'], [lambda r: r['f_OR'], lambda r: r['s1']], ['f_OR', 's1'], grupo='mun')
    rob['e_efeito_fixo_municipio_sem_controle'] = reg(rows, lambda r: r['s2'], [lambda r: r['f_OR']], ['f_OR'], grupo='mun')
    rob['f_todas_as_fracoes'] = reg(rows, lambda r: r['s2'], [lambda r: r['f_OR'], lambda r: r['f_DG'], lambda r: r['f_MI'],
                                                              lambda r: r['f_S'], lambda r: r['s1']], ['f_OR', 'f_DG', 'f_MI', 'f_S', 's1'])
    mud = [r for r in rows if r['completo2'] and r.get('f_OR1') is not None]
    rob['g_mudanca_virada_contra_var_orfas'] = reg(mud, lambda r: r['s2'] - r['s1'], [lambda r: r['f_OR'] - r['f_OR1']], ['var_f_OR'])
    rob['h_1T_sozinho_s1_contra_orfas_1T'] = reg(mud, lambda r: r['s1'], [lambda r: r['f_OR1']], ['f_OR1'], peso='w1')
    rob['h2_2T_mesmas_secoes_s2_contra_orfas_2T_sem_controle'] = reg(mud, lambda r: r['s2'], [lambda r: r['f_OR']], ['f_OR'])
    for nm, o in rob.items():
        o['z'] = {kk: (o['coef'][kk] / o['ep'][kk] if o['ep'][kk] else None) for kk in o['coef']}

    # ---------------- exploratório (escrito depois de ver o resultado pela letra)
    exp = {}
    # E1: dummies explícitas
    cnt = collections.Counter(r['loc'] for r in rows)
    rr = [r for r in rows if cnt[r['loc']] >= 2]
    locs = sorted({r['loc'] for r in rr}); ixl = {l: i for i, l in enumerate(locs)}
    nX, G = len(rr), len(locs)
    X = np.zeros((nX, 2 + G)); Y = np.zeros(nX); W = np.zeros(nX); gg = np.zeros(nX, int)
    for i, r in enumerate(rr):
        X[i, 0] = r['f_OR']; X[i, 1] = r['s1']; X[i, 2 + ixl[r['loc']]] = 1; Y[i] = r['s2']; W[i] = r['w']; gg[i] = ixl[r['loc']]
    sw = np.sqrt(W)
    bb = np.linalg.lstsq(X * sw[:, None], Y * sw, rcond=None)[0]
    ee = Y - X @ bb
    inv = np.linalg.pinv((X * W[:, None]).T @ X)
    Sg = np.zeros((G, X.shape[1]))
    for j in range(X.shape[1]):
        Sg[:, j] = np.bincount(gg, weights=W * X[:, j] * ee, minlength=G)
    Vv = inv @ (Sg.T @ Sg) @ inv
    exp['E1_dummies_explicitas'] = {'n': nX, 'locais': G, 'b': float(bb[0]),
                                    'ep_contando_dummies': float(math.sqrt(G / (G - 1) * (nX - 1) / (nX - 2 - G) * Vv[0, 0])),
                                    'ep_convencao_fe_ols': float(math.sqrt(G / (G - 1) * (nX - 1) / (nX - 2) * Vv[0, 0]))}
    # E2: placebo com efeito fixo de município
    e2 = reg(rows, lambda r: r['s1'], [lambda r: r['f_OR']], ['f_OR'], grupo='mun')
    e2['z'] = {kk: e2['coef'][kk] / e2['ep'][kk] for kk in e2['coef']}
    exp['E2_placebo_efeito_fixo_municipio'] = e2
    # E3: conta ingênua
    def pond(rr, peso, val):
        sw_ = sum(peso(r) for r in rr)
        return sum(peso(r) * val(r) for r in rr) / sw_ if sw_ else None
    def dentro_mun(rr, val):
        gm = collections.defaultdict(list)
        for r in rr:
            gm[r['mun']].append(r)
        mu = {m: sum(r['w'] * val(r) for r in x) / sum(r['w'] for r in x) for m, x in gm.items()}
        return lambda r: val(r) - mu[r['mun']]
    e3 = {}
    for nome, rr_, por, fa, fb in (('2T', rows, 'OR2', 's2', 'B2'), ('2T_fatia_do_1T_mesmas_secoes', rows, 'OR2', 's1', 'B2'),
                                   ('1T_mesma_urna', mud, 'OR1', 's1', 'B1')):
        v = lambda r, fa=fa: r[fa]
        a = pond(rr_, lambda r: r[por], v); bq = pond(rr_, lambda r: r[fb], v)
        dv = dentro_mun(rr_, v)
        a2 = pond(rr_, lambda r: r[por], dv); b2 = pond(rr_, lambda r: r[fb], dv)
        e3[nome] = {'fatia_ponderada_pelas_orfas': a, 'fatia_ponderada_pela_biometria': bq, 'diferenca': a - bq,
                    'dentro_do_municipio_orfas': a2, 'dentro_do_municipio_biometria': b2, 'diferenca_dentro_do_municipio': a2 - b2}
    exp['E3_conta_ingenua'] = e3
    # E4: municípios com mais órfãs
    gm = collections.defaultdict(list)
    for r in rows:
        gm[r['mun']].append(r)
    top = sorted(gm, key=lambda m: -sum(r['OR2'] for r in gm[m]))[:10]
    e4 = []
    for m in top:
        x = gm[m]
        alto = [r for r in x if r['OR2'] >= 10]; resto = [r for r in x if r['OR2'] < 10]
        vir = lambda rr_: pond(rr_, lambda r: r['w'], lambda r: 100 * (r['s2'] - r['s1'])) if rr_ else None
        e4.append({'mun': m, 'secoes': len(x), 'OR_2T': sum(r['OR2'] for r in x), 'OR_1T_mesma_urna': sum(r.get('OR1', 0) for r in x),
                   'manuais_2T': sum(r['man2'] for r in x), 'manuais_1T': sum(r['man1'] for r in x),
                   'MI_2T': sum(r['MI2'] for r in x), 'DG_2T': sum(r['DG2'] for r in x), 'votos_2T': sum(r['c2'] for r in x),
                   'virada_cidade_pts': vir(x), 'secoes_com_10_ou_mais_OR': len(alto), 'virada_secoes_10_ou_mais_pts': vir(alto),
                   'virada_outras_pts': vir(resto), 'fatia_Lula_2T_cidade': pond(x, lambda r: r['w'], lambda r: 100 * r['s2'])})
    exp['E4_municipios_com_mais_orfas'] = e4

    # poder e variação que identifica
    ident = {'dp_f_OR_dentro_do_local': dp_dentro(rows, lambda r: r['f_OR']),
             'dp_f_OR_dentro_do_municipio': dp_dentro(rows, lambda r: r['f_OR'], 'mun'),
             'media_ponderada_f_OR': float(np.average([r['f_OR'] for r in rows], weights=[r['w'] for r in rows])),
             'secoes_com_OR': sum(1 for r in rows if r['OR2'] > 0),
             'efeito_minimo_detectavel_80pc': 2.8 * ep}
    gl = collections.defaultdict(set)
    for r in rows:
        gl[r['loc']].add(round(r['f_OR'], 9))
    ident['locais'] = len(gl); ident['locais_onde_f_OR_varia'] = sum(1 for v in gl.values() if len(v) > 1)

    # por modelo (faixas do F4)
    def por_modelo(rr, t, chave_mod):
        g = collections.defaultdict(lambda: collections.Counter())
        for r in rr:
            mo = r.get(chave_mod) or 'sem_modelo'
            c = g[mo]
            c['secoes'] += 1; c['votos'] += r['t' + t]['computados']
            for cl in CLASSES:
                c[cl] += r['t' + t]['votos'][cl]
            c['secoes_com_OR'] += r['t' + t]['votos']['OR'] > 0
        out = {}
        for mo, c in sorted(g.items()):
            man = c['MI'] + c['DG'] + c['OR'] + c['MX']
            out[mo] = {'secoes': c['secoes'], 'votos': c['votos'], 'OR': c['OR'], 'DG': c['DG'], 'MI': c['MI'], 'S': c['S'], 'B': c['B'],
                       'manuais': man, 'pct_OR_dos_votos': 100 * c['OR'] / c['votos'] if c['votos'] else None,
                       'pct_OR_das_manuais': 100 * c['OR'] / man if man else None,
                       'pct_manuais_dos_votos': 100 * man / c['votos'] if c['votos'] else None,
                       'pct_secoes_com_OR': 100 * c['secoes_com_OR'] / c['secoes']}
        return out
    s2v = [r for r in secs if r['t2']['computados'] > 0 and r.get('modelo2', 'x') != 'x']
    s1v = [r for r in secs if r['t1_mesma_urna_completo']]
    modelos = {'2T_todas': por_modelo(s2v, '2', 'modelo2'), '1T_mesma_urna': por_modelo(s1v, '1', 'modelo1'),
               '2T_mesmas_secoes_do_1T': por_modelo(s1v, '2', 'modelo2')}

    # 1º turno da mesma urna, seção a seção
    par = [r for r in secs if r['t1_mesma_urna_completo'] and r['t2']['log_completo']]
    a1 = np.array([r['t1']['votos']['OR'] for r in par], float); a2 = np.array([r['t2']['votos']['OR'] for r in par], float)
    c1 = np.array([r['t1']['computados'] for r in par], float); c2 = np.array([r['t2']['computados'] for r in par], float)
    mesma = {'secoes': len(par), 'OR_1T': int(a1.sum()), 'OR_2T': int(a2.sum()), 'votos_1T': int(c1.sum()), 'votos_2T': int(c2.sum()),
             'pct_OR_1T': 100 * a1.sum() / c1.sum(), 'pct_OR_2T': 100 * a2.sum() / c2.sum(),
             'correlacao_fracao_OR_1T_2T': float(np.corrcoef(a1 / c1, a2 / c2)[0, 1]),
             'correlacao_contagem_OR_1T_2T': float(np.corrcoef(a1, a2)[0, 1]),
             'secoes_OR_2T_maior': int((a2 > a1).sum()), 'secoes_OR_2T_menor': int((a2 < a1).sum()), 'secoes_iguais': int((a2 == a1).sum()),
             'secoes_zero_nos_dois': int(((a1 == 0) & (a2 == 0)).sum())}
    top2 = np.argsort(-a2)[:max(1, int(round(0.05 * len(par))))]
    mesma['5pct_com_mais_OR_no_2T'] = {'secoes': len(top2), 'OR_2T': int(a2[top2].sum()), 'OR_1T_mesmas_secoes': int(a1[top2].sum()),
                                       'votos_2T': int(c2[top2].sum()), 'votos_1T': int(c1[top2].sum())}
    pmod = collections.defaultdict(lambda: [0, 0, 0, 0])
    for r in par:
        x = pmod[r.get('modelo2') or 'sem_modelo']; x[0] += r['t1']['votos']['OR']; x[1] += r['t1']['computados']; x[2] += r['t2']['votos']['OR']; x[3] += r['t2']['computados']
    mesma['por_modelo'] = {mo: {'pct_OR_1T': 100 * v[0] / v[1], 'pct_OR_2T': 100 * v[2] / v[3], 'OR_1T': v[0], 'OR_2T': v[2]} for mo, v in sorted(pmod.items())}

    # concentração (2º turno, seções com votos no log)
    cs = [r for r in secs if r['t2']['computados'] > 0]
    v_or = np.array([r['t2']['votos']['OR'] for r in cs], float)
    porloc = collections.Counter(); pormun = collections.Counter()
    for r in cs:
        porloc[r.get('loc')] += r['t2']['votos']['OR']; pormun[r.get('mun')] += r['t2']['votos']['OR']
    conc = {'secoes': len(cs), 'OR_total': int(v_or.sum()), 'secoes_com_zero': int((v_or == 0).sum()),
            'pct_secoes_com_zero': 100 * float((v_or == 0).mean()),
            'secoes_com_1_ou_mais': int((v_or >= 1).sum()), 'secoes_com_10_ou_mais': int((v_or >= 10).sum()),
            'secoes_com_30_ou_mais': int((v_or >= 30).sum()),
            'fracao_no_1pct': topo(v_or, 0.01), 'fracao_no_5pct': topo(v_or, 0.05), 'fracao_no_10pct': topo(v_or, 0.10),
            'gini_secoes': gini(v_or), 'locais': len(porloc), 'gini_locais': gini(list(porloc.values())),
            'municipios': len(pormun), 'gini_municipios': gini(list(pormun.values())),
            'fracao_nos_10_municipios_com_mais': sum(v for _, v in pormun.most_common(10)) / v_or.sum() if v_or.sum() else None,
            'municipios_com_mais': [[m, v] for m, v in pormun.most_common(10)],
            'media_por_secao': float(v_or.mean()), 'variancia_sobre_media': float(v_or.var() / v_or.mean()) if v_or.mean() else None}
    # comparação: manuais (M) concentradas como? (régua para ler a concentração das órfãs)
    v_m = np.array([r['t2']['manual'] for r in cs], float)
    conc['manuais_fracao_no_5pct'] = topo(v_m, 0.05); conc['manuais_gini_secoes'] = gini(v_m)
    # órfãs entre as manuais, nas seções com muitas manuais
    conc['OR_das_manuais_por_faixa_de_manuais'] = {}
    for lo, hi in ((1, 10), (10, 30), (30, 60), (60, 100000)):
        rr = [r for r in cs if lo <= r['t2']['manual'] < hi]
        man = sum(r['t2']['manual'] for r in rr); orr = sum(r['t2']['hab']['OR'] for r in rr)
        conc['OR_das_manuais_por_faixa_de_manuais'][f'{lo}-{hi - 1}'] = {'secoes': len(rr), 'manuais': man, 'OR': orr,
                                                                         'pct_OR': 100 * orr / man if man else None}
    # pelo número de mesários com digital comparada
    pm = collections.defaultdict(lambda: [0, 0, 0])
    for r in cs:
        n = min(r['t2']['n_mesarios'], 6)
        pm[n][0] += 1; pm[n][1] += r['t2']['manual']; pm[n][2] += r['t2']['hab']['OR']
    conc['por_numero_de_mesarios_comparados'] = {str(n): {'secoes': v[0], 'manuais': v[1], 'OR': v[2],
                                                          'pct_OR_das_manuais': 100 * v[2] / v[1] if v[1] else None}
                                                 for n, v in sorted(pm.items())}
    ordem = sorted(cs, key=lambda r: -r['t2']['votos']['OR'])[:15]
    conc['15_secoes_com_mais'] = [{'k': r['k'], 'modelo': r.get('modelo2'), 'votos': r['t2']['computados'], 'manuais': r['t2']['manual'],
                                   'OR': r['t2']['votos']['OR'], 'DG': r['t2']['votos']['DG'], 'MI': r['t2']['votos']['MI'],
                                   'mesarios_comparados': r['t2']['n_mesarios'],
                                   'OR_1T_mesma_urna': r['t1']['votos']['OR'] if r['t1_mesma_urna_completo'] else None,
                                   'manuais_1T_mesma_urna': r['t1']['manual'] if r['t1_mesma_urna_completo'] else None,
                                   'virada_pts': (100 * (r['L2'] / (r['L2'] + r['R2']) - r['L1'] / (r['L1'] + r['R1'])))
                                   if r.get('L1') is not None and r['L1'] + r['R1'] > 0 and r['L2'] + r['R2'] > 0 else None,
                                   'fatia_Lula_2T': 100 * r['L2'] / (r['L2'] + r['R2']) if r['L2'] + r['R2'] > 0 else None}
                                  for r in ordem]
    # score
    sc = {}
    for t in '12':
        mx = [x for r in secs for x in r['t' + t]['OR_max_score']]
        dg = [x for r in secs for x in r['t' + t]['DG_score']]
        mi = [x for r in secs for x in r['t' + t]['MI_score']]
        def hist(v):
            c = collections.Counter('0' if x == 0 else '1-9' if x < 10 else '10-19' if x < 20 else '20-49' if x < 50 else '50+' for x in v)
            return {kk: c.get(kk, 0) for kk in ('0', '1-9', '10-19', '20-49', '50+')}
        sc[t] = {'OR_maior_score': hist(mx), 'OR_todos_os_scores_zero': sum(r['t' + t]['OR_todos_zero'] for r in secs),
                 'OR_sem_linha_de_score': sum(r['t' + t]['OR_sem_score'] for r in secs),
                 'OR_maior_score_mediana': float(np.median(mx)) if mx else None,
                 'DG_score_que_bateu': hist(dg), 'DG_mediana': float(np.median(dg)) if dg else None,
                 'MI_score_que_bateu': hist(mi), 'MI_mediana': float(np.median(mi)) if mi else None,
                 'DG_antes_da_primeira_OR_do_bloco': sum(r['t' + t]['DG_antes_da_primeira_OR_do_bloco'] for r in secs)}
    hora = {}
    for t in '12':
        c = collections.Counter()
        for r in secs:
            c.update({int(h): v for h, v in r['t' + t]['OR_por_hora'].items()})
        hora[t] = {str(h): c.get(h, 0) for h in range(7, 20)}

    # ordem de grandeza nacional
    tt = tot['2T_todas']
    nh_nac = F6['descritivo']['universo']['NH_2T']; comp_nac = F6['descritivo']['universo']['comp_2T']
    og = {'NH_nacional_2T_F6': nh_nac, 'comparecimento_nacional_2T_F6': comp_nac,
          'OR_sobre_manuais_amostra': tt['votos']['OR'] / tt['votos_manuais'],
          'OR_sobre_votos_amostra': tt['votos']['OR'] / tt['votos_computados'],
          'estimativa_por_manuais': nh_nac * tt['votos']['OR'] / tt['votos_manuais'],
          'estimativa_por_votos': comp_nac * tt['votos']['OR'] / tt['votos_computados'],
          'reel': {'orfas': 1280132, 'mesario_oficial': 5780000, 'mesario_substituto': 1470000,
                   'soma_tres': 1280132 + 5780000 + 1470000,
                   'fracoes_do_reel': {'MI': 5780000 / 8530132, 'DG': 1470000 / 8530132, 'OR': 1280132 / 8530132}},
          'fracoes_da_amostra': {c: tt['votos'][c] / tt['votos_manuais'] for c in ('MI', 'DG', 'OR')}}

    out = {'teste': 'C2 do Adendo 24 (digitais órfãs e o voto da seção)', 'registro': 'PRE-REGISTRO-2026-10-26.md, Adendo 24, commit ca110bb',
           'pastas': len(dirs), 'pacotes_com_log': len(pacotes), 'sem_log': sem_log,
           'pacotes_com_mais_de_um_log': sum(1 for _, _, n in pacotes if n > 1),
           'conferencia': conf, 'totais': tot,
           'regressao_principal': principal, 'veredito': ver, 'b': b, 'ep': ep, 'z': b / ep if ep else None,
           'placebo': placebo, 'robustez': rob, 'exploratorio_depois_do_resultado': exp, 'identificacao': ident, 'por_modelo': modelos,
           'mesma_urna_1T_2T': mesma, 'concentracao': conc, 'score': sc, 'orfas_por_hora': hora, 'ordem_de_grandeza': og,
           'secoes': secs}
    json.dump(out, open(saida_json, 'w'), ensure_ascii=False, indent=0)
    texto(out, saida_txt)
    log(f'feito em {time.time() - t0:.0f}s')


# ------------------------------------------------------------------ texto

def n_(x):
    return f'{x:,.0f}'.replace(',', '.')


def f_(x, nd=3):
    return 'sem dado' if x is None else f'{x:+.{nd}f}'.replace('.', ',')


def p_(x, nd=1):
    return 'sem dado' if x is None else f'{x:.{nd}f}'.replace('.', ',')


def texto(o, saida):
    L = []; w = L.append
    w('C2 do Adendo 24: digitais órfãs e o voto da seção (amostra de logs do 2º turno, locais quase inteiros)')
    w('Registro: PRE-REGISTRO-2026-10-26.md, Adendo 24, commit ca110bb (03/11/2026 04:24:10 UTC). Script: scripts/analisar_C2_reel.py.')
    w('Reel checado: @assis.salvioli (DfHTWubBajq), cena 4: "1 milhão e 280 mil liberações onde a digital usada não existia em')
    w('nenhum arquivo da urna", "salto de +15,6 pp" para Lula; mesário oficial 5,78 milhões (51,36%), substituto 1,47 milhão (51,40%).')
    w('')
    w(f'VEREDITO PELA LETRA: {o["veredito"]}')
    w(f'  b = {f_(o["b"])} (erro-padrão {p_(o["ep"], 3)}, z {f_(o["z"], 1)}); o reel diz +0,156. Sinal pede b >= 0,10 a mais de 4')
    w('  erros-padrão; sem sinal pede |b| < 0,05 com erro-padrão até 0,025.')
    w('')
    c = o['conferencia']
    w('1. Leitura e conferência')
    w(f'  Pastas: {o["pastas"]}; com log: {o["pacotes_com_log"]}; sem log: {len(o["sem_log"])} ({", ".join(o["sem_log"])}); pacotes com mais de um log: {o["pacotes_com_mais_de_um_log"]}.')
    for t, nm in (('2', '2º turno (25/10)'), ('1', '1º turno (04/10, no mesmo log)')):
        x = c[t]
        w(f'  {nm}: seções com votos no log {n_(x["com_votos_no_log"])}; log completo (votos no log = comparecimento do bweb) {n_(x["log_completo"])};')
        w(f'    liberações manuais (MI+DG+OR+MX) = NH do bweb em {n_(x["manual_igual_NH_entre_completos"])} de {n_(x["completos_com_NH"])} logs completos; '
          f'diferenças {json.dumps(x["manual_menos_NH_distribuicao"])}.')
        w(f'    linhas "Não encontrou digital..." {n_(x["linhas_OR"])}, habilitações OR {n_(x["hab_OR"])}; linhas "bate com uma digital gravada" {n_(x["linhas_DG"])}, '
          f'habilitações DG {n_(x["hab_DG"])}; linhas "Mesário N habilitou" {n_(x["linhas_MI"])}, habilitações MI {n_(x["hab_MI"])};')
        w(f'    janelas com duas autorizações {x["janelas_com_2_autorizacoes"]}; votos sem habilitação antes {x["voto_sem_hab"]}; habilitações sem voto {x["hab_sem_voto"]}; '
          f'seções com contingência {x["contingencia"]}.')
    w(f'  1º turno na mesma urna (urna igual na base): {n_(c["1"]["mesma_urna_na_base"])}; com log de 04/10 completo: {n_(c["1"]["mesma_urna_e_log_1T_completo"])}.')
    w('')
    w('2. Como os votos foram liberados (votos computados, pela classe da habilitação anterior)')
    w('  classe                                   2º turno (todas)        1º turno (mesma urna)   2º turno (mesmas seções)')
    T = o['totais']
    nomes = {'B': 'B   biometria do eleitor', 'MI': 'MI  mesário identificado', 'DG': 'DG  digital gravada no dia',
             'OR': 'OR  digital órfã (arquivo novo)', 'MX': 'MX  manual sem autorização vista', 'S': 'S   sem biometria cadastrada',
             'X': 'X   indeterminada'}
    for cl in CLASSES:
        cols = []
        for kk in ('2T_todas', '1T_mesma_urna_completo', '2T_mesmas_secoes_do_1T'):
            v = T[kk]['votos'].get(cl, 0)
            cols.append(f'{n_(v):>10} ({p_(T[kk]["pct_votos"][cl], 2):>5}%)')
        w(f'  {nomes[cl]:<38} ' + '   '.join(cols))
    for kk, nm in (('2T_todas', '2º turno'), ('1T_mesma_urna_completo', '1º turno'), ('2T_mesmas_secoes_do_1T', '2º turno, mesmas seções')):
        x = T[kk]
        w(f'  {nm}: {n_(x["secoes"])} seções, {n_(x["votos_computados"])} votos; manuais {n_(x["votos_manuais"])}; entre as manuais: MI {p_(x["pct_das_manuais"]["MI"])}%, '
          f'DG {p_(x["pct_das_manuais"]["DG"])}%, OR {p_(x["pct_das_manuais"]["OR"])}%; subtipos de MI {json.dumps(x["subtipos_MI"], ensure_ascii=False)}; B sem linha de tipo {x["B_sem_linha"]}.')
    og = o['ordem_de_grandeza']
    w(f'  Reel: MI 5,78 mi, DG 1,47 mi, OR 1,28 mi (soma 8,53 mi; frações {p_(100 * og["reel"]["fracoes_do_reel"]["MI"])}%, {p_(100 * og["reel"]["fracoes_do_reel"]["DG"])}%, '
          f'{p_(100 * og["reel"]["fracoes_do_reel"]["OR"])}%); NH nacional do 2º turno no F6: {n_(og["NH_nacional_2T_F6"])}.')
    w(f'  Ordem de grandeza, sem peso amostral: OR / manuais na amostra = {p_(100 * og["OR_sobre_manuais_amostra"], 2)}% -> {n_(og["estimativa_por_manuais"])} no país; '
      f'OR / votos = {p_(100 * og["OR_sobre_votos_amostra"], 3)}% -> {n_(og["estimativa_por_votos"])}.')
    w('')
    pr = o['regressao_principal']; pl = o['placebo']; idt = o['identificacao']
    w('3. Regressão registrada (fatia de Lula no 2º turno contra a fração de votos OR, controle fatia do 1º turno; efeito fixo de local,')
    w('   peso L2+R2, erro agrupado por local; frações de 0 a 1)')
    w(f'  b(f_OR) = {f_(pr["coef"]["f_OR"])} (ep {p_(pr["ep"]["f_OR"], 3)}); controle s1 {f_(pr["coef"]["s1"])} (ep {p_(pr["ep"]["s1"], 3)}); '
      f'{n_(pr["n"])} seções em {n_(pr["grupos"])} locais.')
    w(f'  Placebo (fatia do 1º turno contra a fração OR do 2º turno, sem controle): {f_(pl["coef"]["f_OR"])} (ep {p_(pl["ep"]["f_OR"], 3)}).')
    w(f'  Variação que identifica: fração OR média ponderada {p_(100 * idt["media_ponderada_f_OR"], 2)}%; desvio-padrão dentro do local {p_(100 * idt["dp_f_OR_dentro_do_local"], 2)} pontos '
      f'(dentro do município {p_(100 * idt["dp_f_OR_dentro_do_municipio"], 2)}); seções com OR {n_(idt["secoes_com_OR"])}; locais onde a fração varia {n_(idt["locais_onde_f_OR_varia"])} de {n_(idt["locais"])}.')
    w(f'  Efeito mínimo detectável (80%, 2,8 ep): {p_(idt["efeito_minimo_detectavel_80pc"], 3)}.')
    w(f'  VEREDITO: {o["veredito"]}.')
    w('')
    w('4. Robustez (fixada antes, fora do critério)')
    for nm, x in o['robustez'].items():
        cc = '  '.join(f'{kk} {f_(x["coef"][kk])} (ep {p_(x["ep"][kk], 3)}, z {f_(x["z"][kk], 1)})' for kk in x['coef'])
        w(f'  {nm}: {cc}; n {n_(x["n"])}, grupos {n_(x["grupos"])}')
    w('')
    w('5. Fração de órfãs por modelo de urna (faixas do F4)')
    for kk, nm in (('2T_todas', '2º turno, todas as seções'), ('1T_mesma_urna', '1º turno, mesma urna, log completo'),
                   ('2T_mesmas_secoes_do_1T', '2º turno, as mesmas seções')):
        w(f'  {nm}:')
        for mo, x in o['por_modelo'][kk].items():
            w(f'    {mo:<10} {n_(x["secoes"]):>6} seções {n_(x["votos"]):>9} votos; OR {n_(x["OR"]):>6} ({p_(x["pct_OR_dos_votos"], 2)}% dos votos, '
              f'{p_(x["pct_OR_das_manuais"])}% das manuais); manuais {p_(x["pct_manuais_dos_votos"])}% dos votos; seções com OR {p_(x["pct_secoes_com_OR"])}%')
    w('')
    m = o['mesma_urna_1T_2T']
    w('6. Mesma urna nos dois turnos (log completo nos dois dias)')
    w(f'  {n_(m["secoes"])} seções: OR {n_(m["OR_1T"])} no 1º turno ({p_(m["pct_OR_1T"], 2)}% dos votos) e {n_(m["OR_2T"])} no 2º ({p_(m["pct_OR_2T"], 2)}%).')
    w(f'  Correlação entre seções da fração OR nos dois turnos {p_(m["correlacao_fracao_OR_1T_2T"], 2)} (contagem {p_(m["correlacao_contagem_OR_1T_2T"], 2)}); '
      f'mais OR no 2º {n_(m["secoes_OR_2T_maior"])}, menos {n_(m["secoes_OR_2T_menor"])}, igual {n_(m["secoes_iguais"])} (zero nos dois {n_(m["secoes_zero_nos_dois"])}).')
    t5 = m['5pct_com_mais_OR_no_2T']
    w(f'  As {t5["secoes"]} seções (5%) com mais OR no 2º turno: {n_(t5["OR_2T"])} OR no 2º e {n_(t5["OR_1T_mesmas_secoes"])} no 1º na mesma urna.')
    w('  Por modelo: ' + '; '.join(f'{mo} {p_(v["pct_OR_1T"], 2)}% no 1º e {p_(v["pct_OR_2T"], 2)}% no 2º' for mo, v in m['por_modelo'].items()))
    w('')
    cc = o['concentracao']
    w('7. Concentração das órfãs (2º turno)')
    w(f'  {n_(cc["OR_total"])} órfãs em {n_(cc["secoes"])} seções: zero em {n_(cc["secoes_com_zero"])} ({p_(cc["pct_secoes_com_zero"])}%); 10 ou mais em {cc["secoes_com_10_ou_mais"]}; 30 ou mais em {cc["secoes_com_30_ou_mais"]}.')
    w(f'  Fração das órfãs no 1% de seções com mais: {p_(100 * cc["fracao_no_1pct"])}%; no 5%: {p_(100 * cc["fracao_no_5pct"])}%; no 10%: {p_(100 * cc["fracao_no_10pct"])}%. '
      f'Gini por seção {p_(cc["gini_secoes"], 2)}, por local {p_(cc["gini_locais"], 2)}, por município {p_(cc["gini_municipios"], 2)}.')
    w(f'  Régua: todas as liberações manuais têm {p_(100 * cc["manuais_fracao_no_5pct"])}% no 5% de seções com mais e Gini {p_(cc["manuais_gini_secoes"], 2)}. '
      f'Variância sobre média das órfãs por seção {p_(cc["variancia_sobre_media"], 1)} (Poisson daria 1).')
    w(f'  10 municípios com mais órfãs: {p_(100 * cc["fracao_nos_10_municipios_com_mais"])}% do total; ' + ', '.join(f'{mm} ({v})' for mm, v in cc['municipios_com_mais']))
    w('  Órfãs entre as manuais, pelo número de manuais da seção: ' + '; '.join(f'{kk}: {p_(v["pct_OR"])}% de {n_(v["manuais"])} ({v["secoes"]} seções)'
                                                                       for kk, v in cc['OR_das_manuais_por_faixa_de_manuais'].items()))
    w('  Órfãs entre as manuais, pelo número de mesários com digital comparada: ' + '; '.join(f'{kk}: {p_(v["pct_OR_das_manuais"])}% de {n_(v["manuais"])} ({v["secoes"]} seções)'
                                                                                 for kk, v in cc['por_numero_de_mesarios_comparados'].items()))
    w('  As 15 seções com mais órfãs no 2º turno:')
    w('    seção                  modelo   votos manuais   OR   DG   MI mes.comp  OR 1T  man 1T  virada  Lula 2T')
    for r in cc['15_secoes_com_mais']:
        w(f'    {r["k"]:<22} {str(r["modelo"]):<7} {r["votos"]:>5} {r["manuais"]:>7} {r["OR"]:>4} {r["DG"]:>4} {r["MI"]:>4} {r["mesarios_comparados"]:>8} '
          f'{str(r["OR_1T_mesma_urna"]):>6} {str(r["manuais_1T_mesma_urna"]):>7} {f_(r["virada_pts"], 1):>7} {p_(r["fatia_Lula_2T"]):>7}')
    w('')
    w('8. Score das digitais (linhas "Batimento de digitais retornou o score N")')
    for t, nm in (('2', '2º turno'), ('1', '1º turno')):
        s = o['score'][t]
        w(f'  {nm}: maior score das órfãs {json.dumps(s["OR_maior_score"])} (mediana {p_(s["OR_maior_score_mediana"], 0)}); órfãs com todos os scores zero {s["OR_todos_os_scores_zero"]}; '
          f'sem linha de score {s["OR_sem_linha_de_score"]}.')
        w(f'    score que bateu: DG {json.dumps(s["DG_score_que_bateu"])} (mediana {p_(s["DG_mediana"], 0)}); MI {json.dumps(s["MI_score_que_bateu"])} (mediana {p_(s["MI_mediana"], 0)}); '
          f'DG antes da primeira OR do bloco {s["DG_antes_da_primeira_OR_do_bloco"]}.')
    w('  Órfãs por hora do relógio da urna, 2º turno (1º): ' + ', '.join(f'{h}h {o["orfas_por_hora"]["2"][h]} ({o["orfas_por_hora"]["1"][h]})' for h in o['orfas_por_hora']['2']))
    w('')
    ex = o['exploratorio_depois_do_resultado']
    NOMES_MUN = {'MG|46337': 'Itabira', 'SP|71072': 'São Paulo', 'BA|34193': 'Campo Formoso', 'RJ|60011': 'Rio de Janeiro',
                 'CE|13382': 'Banabuiú', 'MG|46078': 'Ijaci', 'AL|28436': 'Poço das Trincheiras', 'RS|89575': 'Vera Cruz',
                 'BA|38490': 'Salvador', 'AL|27910': 'Maravilha', 'PE|23817': 'Caruaru', 'GO|94790': 'Mutunópolis',
                 'MG|44458': 'Divinópolis'}
    w('9. Exploratório (escrito depois de ver o resultado pela letra; pistas, sem veredito)')
    e1 = ex['E1_dummies_explicitas']
    w(f'  E1. Dummies explícitas de local: b {f_(e1["b"])}; erro-padrão {p_(e1["ep_convencao_fe_ols"], 4)} na convenção de lib.fe_ols e '
      f'{p_(e1["ep_contando_dummies"], 4)} contando as {e1["locais"]} dummies (as duas abaixo de 0,025).')
    e2 = ex['E2_placebo_efeito_fixo_municipio']
    w(f'  E2. Placebo com efeito fixo de município: {f_(e2["coef"]["f_OR"])} (ep {p_(e2["ep"]["f_OR"], 3)}); compare com a robustez (e), '
      f'{f_(o["robustez"]["e_efeito_fixo_municipio_sem_controle"]["coef"]["f_OR"])}.')
    w('  E3. Conta ingênua (fatia de Lula entre os finalistas das seções, ponderada pelos votos órfãos contra a ponderada pelos votos biométricos):')
    for kk, x in ex['E3_conta_ingenua'].items():
        w(f'    {kk}: órfãs {p_(100 * x["fatia_ponderada_pelas_orfas"], 2)}%, biometria {p_(100 * x["fatia_ponderada_pela_biometria"], 2)}%, '
          f'diferença {f_(100 * x["diferenca"], 2)} pontos; dentro do município {f_(100 * x["diferenca_dentro_do_municipio"], 2)} pontos.')
    w('  E4. Municípios com mais órfãs (virada ponderada, pontos; "10+" = seções com 10 ou mais órfãs no 2º turno):')
    for x in ex['E4_municipios_com_mais_orfas']:
        w(f'    {x["mun"]} {NOMES_MUN.get(x["mun"], ""):<20} {x["secoes"]:>4} seções; OR {x["OR_2T"]:>5} no 2º e {x["OR_1T_mesma_urna"]:>5} no 1º; '
          f'manuais {x["manuais_2T"]} e {x["manuais_1T"]}; MI {x["MI_2T"]}, DG {x["DG_2T"]} no 2º; Lula 2º {p_(x["fatia_Lula_2T_cidade"])}%; '
          f'virada da cidade {f_(x["virada_cidade_pts"], 2)}, 10+ ({x["secoes_com_10_ou_mais_OR"]}) {f_(x["virada_secoes_10_ou_mais_pts"], 2)}, outras {f_(x["virada_outras_pts"], 2)}')
    w('')
    w('10. Desvios declarados (decisões que o registro não fixa; docstring do script, escritas antes de rodar)')
    for d in ('D2: além das quatro categorias do registro, S (eleitor sem biometria cadastrada, por ano de nascimento) e B sem linha de tipo; S entra no denominador.',
              'D3: votos atribuídos à classe da última habilitação antes de cada voto computado; denominador = votos computados no log do dia.',
              'D4: frações de 0 a 1 (y, x e controle), para b ser comparável ao +0,156 do reel.',
              'D5: peso L2+R2 e efeito fixo do local do 2º turno (o registro não fixa o peso).',
              'D6: placebo sem controle, mesmo peso e efeito fixo.',
              'D8: robustez (a) a (h), fora do critério.',
              'D13: ordem de grandeza nacional sem peso amostral (a amostra não é aleatória simples do país).'):
        w('  ' + d)
    open(saida, 'w').write('\n'.join(L) + '\n')


if __name__ == '__main__':
    main()
