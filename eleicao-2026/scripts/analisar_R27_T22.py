"""R27_T22 (Adendo 27, Onda D-c, e Adendo 30, última onda): GOVERNADOR NA MESMA URNA COM RÉGUA.

Fragilidade "T22b e F20 (governador na mesma urna)" de registro/adendo27/equipe_vermelha_relatorio.json.
Registro: PRE-REGISTRO-2026-10-26.md, Adendo 27 (commit 2748895, 10/11/2026 00:16:42 UTC) e Adendo 30 (commit a7218fb).

LETRA DO REGISTRO (copiada)
  reteste_proposto: "Calibrar o D natural com o voto por candidato a governador do 2º turno de 2018 e 2022 (bweb
    público, cargo 3; baixar uma UF por vez, filtrar por bytes e apagar o zip), com o alinhamento fixado antes por
    agente que não vê o D. São 26 pares UF e ano. Repetir o contraste C = D menos espelho."
  criterio_proposto: "SINAL: D de 2026 (empilhado em AM, DF e ES e também só AM) abaixo do percentil 5 dos 26 D
    naturais e de -0,03 ou menos. EXCLUSÃO de troca de 3,6% só no presidente: D de 2026 mais 0,0345 acima do percentil
    95 dos naturais. Entre os dois: inconclusivo. Se a dispersão natural (desvio-padrão) passar de 0,03, declarar o
    desenho SEM PODER e parar de citá-lo como contrapeso."
  Aviso do Adendo 27: este reteste foi escrito por quem já conhecia os resultados antigos de 2026 (T22b: D +0,0130,
    ep 0,0047, em AM, DF e ES; por UF AM -0,0104, DF +0,0103, ES +0,0489, AC +0,0462, TO +0,2979; espelho AM e DF
    +0,0017; C em AM -0,0225). O critério é novo; a escolha do que retestar é posterior ao dado. O que NÃO se conhecia
    ao escrever este docstring: nenhum D de 2018 ou de 2022 (o voto por candidato a governador desses anos nunca tinha
    sido baixado).
  Definição de D (Adendo 14, T22b; função t22b de scripts/analisar_pres_gov.py): por seção, duas regressões empilhadas
    com coeficientes próprios de cada cargo, efeito fixo de local por cargo, erro agrupado por local (CR1), sem peso:
      presidente: (votos do candidato no 2º turno menos no 1º) contra [demais candidatos a presidente no 1º turno,
        queda do branco mais nulo de presidente, variação do comparecimento, votos do adversário no 1º turno,
        votos próprios no 1º turno];
      governador: a mesma coisa para o finalista a governador do mesmo campo.
    D = coeficiente dos votos próprios do presidenciável menos o do aliado a governador.
  Espelho (F20, decisão D7): a mesma conta do outro lado (presidenciável do PT menos o governador do campo do PT).
  C (F20, pós-resultado P1): C = D menos espelho, nas UFs com um finalista de cada campo, tirado da mesma regressão
    pela identidade espelho = adversário_1T do aliado menos adversário_1T do presidenciável, com EP agrupado.

DECISÕES QUE O REGISTRO NÃO FIXA, ESCRITAS ANTES DE CALCULAR QUALQUER D DE 2018 OU 2022 (todas relatadas como desvio)

Dados
X1. Fonte do voto por candidato a governador de 2018 e 2022: arquivo "votação por seção" do portal de dados abertos
    do TSE (cdn.tse.jus.br/estatistica/sead/odsele/votacao_secao/votacao_secao_<ano>_<UF>.zip), que traz os DOIS turnos
    por seção e por candidato. O registro fala em "bweb do 2º turno", mas o D precisa também do voto por candidato do
    1º turno (variável "votos próprios no 1º turno"), que no bweb só existe no arquivo do 1º turno, várias vezes maior.
    O conteúdo é o mesmo (voto oficial por seção). Conferência obrigatória: branco, nulo, válidos e comparecimento de
    governador de cada seção e turno contra as bases dados/secoes2018.json.gz e secoes2022.json.gz (campos 1g e 2g,
    que vieram do bweb). Seção que não confere em algum dos dois turnos sai, e a contagem é relatada.
X2. Download: uma UF por vez, tamanho conferido antes (HEAD), leitura por faixas de bytes (Range) com no máximo 1
    requisição por segundo, descompressão em fluxo e filtro por bytes das linhas de governador (;3;"Governador";).
    O zip nunca é gravado em disco; só fica o agregado por seção (gov_<ano>_<UF>.json.gz). Para em 429, 403 ou 407.
X3. 2026: governador do 2º turno por candidato lido por código próprio dos zips do bweb do 2º turno das 6 UFs
    (cargo 3, filtro por bytes), conferido contra a base secoes2026 (campo 2g) e contra a extração da onda A
    (adendo27/A2/gov2t_6ufs.json.gz). Governador do 1º turno por candidato: dados/candidatos_gov_2026_1t_6ufs.json.gz.
X4. Universo de cada par UF e ano: seções da base com presidente e governador nos dois turnos e com o voto por
    candidato a governador nos dois turnos. Finalistas = os dois números com voto nominal no 2º turno do arquivo.
    Presidente: L = candidato do PT (Haddad 13 em 2018, Lula 13 em 2022 e 2026); R = Bolsonaro (17 em 2018, 22 em
    2022) ou Flávio (22 em 2026), como nas bases. Local = chave_local com o local do 2º turno (como no t22b).
    Branco e nulo de governador de cada turno: os das bases (1g e 2g), como em 2026.

Alinhamento (gravado em resultados/R27_T22_alinhamento_2018_2022.json antes de calcular qualquer D)
A1. Papel de Flávio em 2018 e 2022 = Jair Bolsonaro (mesmo campo político e o candidato contra quem a troca só no
    presidente teria sido feita, se a suspeita do Léo sobre esses anos estiver certa). Em 2018 ele venceu e em 2022
    perdeu; os dois anos entram juntos nos naturais, e o D por ano é relatado à parte.
A2. Campo de Bolsonaro (regra do F20, Adendo 23, transposta): o finalista (a) declarou apoio ou voto em Bolsonaro no
    2º turno presidencial daquele ano, ou recebeu apoio declarado do próprio Bolsonaro; ou (b) é filiado ao partido de
    Bolsonaro (PSL em 2018, PL em 2022) ou tem esse partido na coligação registrada para governador. Basta uma.
A3. Campo do PT: o finalista declarou apoio ou voto no candidato do PT no 2º turno, ou recebeu apoio declarado dele,
    ou é do PT ou tem o PT na coligação registrada, e não está no campo de Bolsonaro.
A4. Classes de cada par UF e ano:
    "limpo": exatamente um finalista no campo de Bolsonaro (o outro no campo do PT ou neutro). São os naturais
      PRINCIPAIS, porque é a situação de AM, DF e ES em 2026, as UFs do critério.
    "duplo": os dois finalistas no campo de Bolsonaro (situação de AC e TO em 2026). Fora dos principais. Entram só no
      conjunto SECUNDÁRIO, com o desempate D2 do F20 (o único que atende a (a) e (b) ao mesmo tempo); sem desempate, sai.
    "sem campo de Bolsonaro": nenhum finalista no campo de Bolsonaro. Fora do D. Se exatamente um for do campo do PT,
      entra nos naturais do ESPELHO.
    "fora": fonte contraditória ou sem fonte clara de apoio declarado ou de coligação.
A5. Naturais do espelho: pares com exatamente um finalista no campo do PT. Naturais de C: pares com um finalista de
    cada campo ("polarizado").
A6. O registro diz "26 D naturais". Só entram os pares com fonte clara; o número efetivo é relatado. Se os principais
    forem menos de 8, a régua é declarada insuficiente (SEM PODER por falta de naturais), seja qual for a dispersão.

Estatística
E1. D por par UF e ano: a regressão do t22b escrita de novo neste arquivo (função reg_par), só com as seções da UF,
    locais com 2 seções ou mais, mínimo de 30 seções. Conferência do código: reproduzir os D de 2026 já publicados
    (AM, DF, ES empilhado +0,0130; por UF) antes de olhar 2018 e 2022.
E2. Percentis 5 e 95: interpolação linear (numpy.percentile padrão) sobre os D naturais PRINCIPAIS, um por par UF e
    ano, sem peso. Ao lado: mínimo, máximo, mediana, média, e os percentis no conjunto secundário (principais mais
    duplos com desempate) e por ano.
E3. Dispersão natural = desvio-padrão amostral (ddof = 1) dos D naturais principais. Ao lado: ddof = 0, a dispersão
    descontado o erro de estimação de cada D (raiz de variância menos média dos EP ao quadrado), por ano e no
    conjunto secundário. A letra usa a dispersão bruta.
E4. Partes do veredito e precedência (a letra tem quatro cláusulas e não diz a ordem):
    Parte 1 (régua): SEM PODER se a dispersão passar de 0,03 (ou se houver menos de 8 naturais, A6); senão COM PODER.
    Parte 2 (sinal), para o D empilhado em AM, DF e ES e, separado, para o D só de AM: SINAL se D < percentil 5 dos
      naturais E D <= -0,03; senão, ver parte 3.
    Parte 3 (exclusão), para os mesmos dois D: EXCLUSÃO da troca de 3,6% só no presidente se D + 0,0345 > percentil 95
      dos naturais. Nem sinal nem exclusão: INCONCLUSIVO.
    Se a parte 1 der SEM PODER, as partes 2 e 3 são relatadas pela letra mas não contam nem como indício nem como
      contrapeso (é o que a letra manda: "parar de citá-lo como contrapeso"). Regra geral da onda, acima disso: se a
      troca plantada em 2026 não for vista pelo critério, o veredito do teste é SEM PODER.
    "Empilhado e também só AM": cada um tem veredito próprio; o veredito do teste segue o empilhado (estatística do
      T22b) e o de AM vai ao lado.
E5. Complemento fixado antes (descritivo): o D empilhado de 2026 é uma média de 3 UFs e os naturais são de uma UF só.
    Ao lado dos percentis da letra, a distribuição do D empilhado de todos os trios de pares principais do mesmo ano
    (regressão empilhada de verdade), com os mesmos percentis.
E6. Calibração por efeito plantado:
    (i) irregularidade, em 2026: troca só no presidente de s = 3,6% dos votos de Flávio do 2º turno para Lula (valor
        esperado, como no t22b_com_troca; ao lado, sorteio binomial com semente 20261110), em AM, DF e ES e só em AM.
        O teste "enxerga" se o D com a troca plantada cai na cláusula SINAL. Também s de 0,5% a 10% para achar a menor
        troca que o critério veria.
    (ii) irregularidade, nos naturais: a mesma troca plantada em cada par principal de 2018 e 2022 (de Bolsonaro para
        o candidato do PT), com percentil 5 calculado sem o próprio par. Taxa de detecção (poder) e taxa de falso
        alarme sem a troca.
    (iii) explicação inocente, em 2026: abstenção de 3,6% dos eleitores de Flávio do 2º turno (saem dos dois cargos na
        mesma urna). No presidente: R2 menos s x R2 e comparecimento menos s x R2. No governador: os mesmos eleitores
        saem (iii-a) na proporção do voto de governador da seção no 2º turno (aliado, adversário, branco e nulo) ou
        (iii-b) todos do aliado, até o limite dos votos dele, o resto na proporção. O critério não deve dar SINAL.
    (iv) limite do desenho: troca de 3,6% nos dois cargos ao mesmo tempo (de Flávio para Lula e do aliado para o
        adversário). O D não deve se mover: o teste é cego a desvio que mexa também no governador (dito no registro).
E7. Espelho: em 2026, próprio(Lula) menos próprio(governador do campo de Lula) em AM e DF empilhados, em cada uma, e
    em RN (Cadu 13 contra neutro; entra aqui porque os naturais do espelho também incluem PT contra neutro). Régua:
    os espelhos naturais de 2018 e 2022 (A5). Mesmo critério da letra, espelhado. A troca só no presidente quase não
    move o espelho (cerca de +0,001), então ele serve de placebo na mesma urna.
E8. Contraste C = D menos espelho: 2026 em AM e DF (empilhado e cada uma); naturais nos pares polarizados. O registro
    manda "repetir" e não dá critério: aplico o mesmo critério da letra a C (percentis dos C naturais, -0,03, e
    exclusão com o deslocamento de C sob a troca plantada medido em 2026), como decisão minha, relatada à parte.
E9. Tradução em votos: o deslocamento de D por ponto de troca sai da troca plantada em 2026 (E6 i). Relato (a) a
    largura da faixa natural (percentil 5 a 95) em fração de troca e em votos de margem no país (3,6% de troca só no
    presidente = 4.430.191 votos de margem, por regra de três); (b) a menor troca que o critério veria; (c) a maior
    troca que o critério não consegue excluir; (d) os votos de Flávio nas UFs do teste.
E10. Outros anos como régua: o Léo suspeita também de 2018 e 2022. Se nesses anos houve a mesma troca só no
    presidente contra Bolsonaro, os D naturais já viriam deslocados para baixo e 2026 pareceria normal. O veredito diz
    que depende só dessa comparação. O valor bruto de 2026 (D por UF, espelho, C) vai sempre ao lado.
E11. Depois de ver qualquer D de 2018 ou 2022, tudo o que for acrescentado vai marcado como EXPLORATÓRIO.

Uso:
  python3 -I analisar_R27_T22.py extrair <ano> <UF> <pasta_saida>
  python3 -I analisar_R27_T22.py extrair2026 <pasta_zips2t> <saida.json.gz>
  python3 -I analisar_R27_T22.py rodar <pasta_trabalho> <alinhamento.json> <saida.json> <saida.txt>
"""
import os as _os, sys as _sys
_sys.path.insert(0, _os.path.dirname(_os.path.abspath(__file__)))
import collections, csv, gzip, io, json, os, re, ssl, sys, time, zlib, struct
import urllib.request, urllib.error

RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
URL_VS = 'https://cdn.tse.jus.br/estatistica/sead/odsele/votacao_secao/votacao_secao_{ano}_{uf}.zip'
PARES = {'2018': ['AP', 'AM', 'DF', 'MG', 'MS', 'PA', 'RJ', 'RN', 'RO', 'RR', 'RS', 'SC', 'SE', 'SP'],
         '2022': ['AL', 'AM', 'BA', 'ES', 'MS', 'PB', 'PE', 'RO', 'RS', 'SC', 'SE', 'SP']}
MARCA = re.compile(rb';3;"(?:Governador|GOVERNADOR)";')


# ================================================================ extração em fluxo (X1, X2)
def _abridor():
    ca = '/root/.ccr/ca-bundle.crt'
    ctx = ssl.create_default_context(cafile=ca if os.path.exists(ca) else None)
    return urllib.request.build_opener(urllib.request.ProxyHandler(), urllib.request.HTTPSHandler(context=ctx))


def _blocos(url, bloco=8 << 20):
    """Gera o arquivo em faixas de bytes, 1 requisição por segundo, com repetição limitada. Para em 429/403/407."""
    op = _abridor()
    req = urllib.request.Request(url, method='HEAD')
    r = op.open(req, timeout=60)
    tam = int(r.headers['Content-Length'])
    info = {'url': url, 'tamanho': tam, 'last_modified': r.headers.get('Last-Modified'), 'etag': r.headers.get('ETag')}
    yield info
    pos = 0
    while pos < tam:
        fim = min(pos + bloco, tam) - 1
        dados = None
        for tent in range(4):
            time.sleep(1.0)
            try:
                r = op.open(urllib.request.Request(url, headers={'Range': f'bytes={pos}-{fim}'}), timeout=180)
                b = r.read()
                if r.status == 206 and len(b) == fim - pos + 1:
                    dados = b
                    break
            except urllib.error.HTTPError as e:
                if e.code in (429, 403, 407):
                    raise SystemExit(f'parado: HTTP {e.code} em {url}')
            except Exception as e:  # rede: tenta de novo com espera
                sys.stderr.write(f'  falha de rede ({type(e).__name__}), tentativa {tent + 1}\n')
            time.sleep(5 * (tent + 1))
        if dados is None:
            raise SystemExit(f'parado: faixa {pos}-{fim} não veio em {url}')
        yield dados
        pos = fim + 1


class _Fluxo:
    def __init__(self, it):
        self.it = it; self.buf = b''; self.fim = False

    def mais(self):
        try:
            self.buf += next(self.it)
            return True
        except StopIteration:
            self.fim = True
            return False

    def ler(self, n):
        while len(self.buf) < n:
            if not self.mais():
                break
        out, self.buf = self.buf[:n], self.buf[n:]
        return out


def _csv_do_zip(fl):
    """Percorre os cabeçalhos locais do zip em fluxo e gera os pedaços descomprimidos do primeiro .csv."""
    while True:
        sig = fl.ler(4)
        if sig != b'PK\x03\x04':
            return
        h = fl.ler(26)
        ver, flag, met, _t, _d, _crc, csz, usz, nlen, xlen = struct.unpack('<HHHHHIIIHH', h)
        nome = fl.ler(nlen).decode('cp437'); fl.ler(xlen)
        if met == 8:
            d = zlib.decompressobj(-15)
            eh_csv = nome.lower().endswith('.csv')
            while not d.eof:
                if not fl.buf and not fl.mais():
                    raise SystemExit('zip truncado')
                dados, fl.buf = fl.buf, b''
                out = d.decompress(dados)
                if eh_csv and out:
                    yield out
            fl.buf = d.unused_data + fl.buf
            if eh_csv:
                return
            if flag & 8:
                raise SystemExit('zip com descritor de dados antes do csv: não tratado')
        elif met == 0:
            if flag & 8 or csz == 0xFFFFFFFF:
                raise SystemExit('entrada sem compressão de tamanho desconhecido: não tratado')
            fl.ler(csz)
        else:
            raise SystemExit(f'método de compressão {met} não tratado')


def extrair(ano, uf, pasta):
    saida = os.path.join(pasta, f'gov_{ano}_{uf}.json.gz')
    if os.path.exists(saida):
        print('já existe', saida); return
    it = _blocos(URL_VS.format(ano=ano, uf=uf))
    info = next(it)
    fl = _Fluxo(it)
    sec = {}; nomes = {'1': {}, '2': {}}; n_lin = 0; n_gov = 0; cab = None; resto = b''; ix = None; t0 = time.time()
    geracao = set()

    def trata(linhas):
        nonlocal n_gov
        rd = csv.reader(io.StringIO(b'\n'.join(linhas).decode('latin1'), newline=''), delimiter=';')
        for r in rd:
            if len(r) <= ix['QT_VOTOS'] or r[ix['CD_CARGO']] != '3':
                continue
            assert r[ix['SG_UF']] == uf and r[ix['ANO_ELEICAO']] == ano, r[:12]
            t = r[ix['NR_TURNO']]
            k = f"{uf}|{int(r[ix['CD_MUNICIPIO']])}|{int(r[ix['NR_ZONA']])}|{int(r[ix['NR_SECAO']])}"
            nv = str(int(r[ix['NR_VOTAVEL']])); q = int(r[ix['QT_VOTOS']])
            s = sec.get(k)
            if s is None:
                s = sec[k] = {'1': {}, '2': {}}
            s[t][nv] = s[t].get(nv, 0) + q
            if nv not in nomes[t]:
                nomes[t][nv] = r[ix['NM_VOTAVEL']]
            geracao.add(r[ix['DT_GERACAO']])
            n_gov += 1

    for bloco in _csv_do_zip(fl):
        dados = resto + bloco
        if cab is None:
            p = dados.find(b'\n')
            if p < 0:
                resto = dados; continue
            cab = next(csv.reader([dados[:p].decode('latin1').strip()], delimiter=';'))
            ix = {c.strip(): i for i, c in enumerate(cab)}
            dados = dados[p + 1:]
        u = dados.rfind(b'\n')
        if u < 0:
            resto = dados; continue
        resto = dados[u + 1:]; corpo = dados[:u]
        n_lin += corpo.count(b'\n') + 1
        linhas = []
        pos = 0
        for m in MARCA.finditer(corpo):
            if m.start() < pos:
                continue
            a = corpo.rfind(b'\n', 0, m.start()) + 1
            b = corpo.find(b'\n', m.end())
            if b < 0:
                b = len(corpo)
            linhas.append(corpo[a:b].rstrip(b'\r')); pos = b
        if linhas:
            trata(linhas)
    if resto.strip():
        n_lin += 1
        if MARCA.search(resto):
            trata([resto.rstrip(b'\r\n')])
    out = {'ano': ano, 'uf': uf, 'fonte': info, 'cabecalho': cab, 'linhas_csv': n_lin, 'linhas_governador': n_gov,
           'dt_geracao': sorted(geracao), 'nomes': nomes, 'secoes': sec, 'segundos': round(time.time() - t0, 1)}
    with gzip.open(saida + '.tmp', 'wt', encoding='utf-8') as f:
        json.dump(out, f, ensure_ascii=False, separators=(',', ':'))
    os.replace(saida + '.tmp', saida)
    tot = {t: collections.Counter() for t in ('1', '2')}
    for s in sec.values():
        for t in ('1', '2'):
            tot[t].update(s[t])
    print(json.dumps({'ano': ano, 'uf': uf, 'tamanho_zip': info['tamanho'], 'linhas_csv': n_lin, 'linhas_governador': n_gov,
                      'secoes': len(sec), 'segundos': out['segundos'],
                      'total_2t': {f"{n} {nomes['2'].get(n, '')}": q for n, q in tot['2'].most_common()}},
                     ensure_ascii=False))


# ================================================================ 2026: governador do 2º turno por candidato (X3)
def extrair2026(pzips, saida):
    import glob, zipfile
    out = {}; tipos = {}
    marca = re.compile(rb'\n[^\n]*;3;"?Governador"?;[^\n]*', re.I)
    for uf in ('AC', 'AM', 'DF', 'ES', 'RN', 'TO'):
        zs = sorted(glob.glob(os.path.join(pzips, f'bweb_2t_{uf}_*.zip')))
        assert len(zs) == 1, zs
        z = zipfile.ZipFile(zs[0])
        nome = [n for n in z.namelist() if n.lower().endswith('.csv')][0]
        bruto = z.read(nome)
        p = bruto.find(b'\n')
        cab = next(csv.reader([bruto[:p].decode('latin1').strip()], delimiter=';'))
        ix = {c.strip().replace('SG_ UF', 'SG_UF'): i for i, c in enumerate(cab)}
        linhas = [m.group(0)[1:].rstrip(b'\r') for m in marca.finditer(bruto)]
        tp = collections.Counter()
        for r in csv.reader(io.StringIO(b'\n'.join(linhas).decode('latin1'), newline=''), delimiter=';'):
            if r[ix['CD_CARGO_PERGUNTA']] != '3':
                continue
            k = f"{r[ix['SG_UF']]}|{int(r[ix['CD_MUNICIPIO']])}|{int(r[ix['NR_ZONA']])}|{int(r[ix['NR_SECAO']])}"
            s = out.get(k)
            if s is None:
                s = out[k] = {'B': 0, 'N': 0, 'V': 0, 'comp': int(r[ix['QT_COMPARECIMENTO']]), 'cand': {}}
            tv, q = int(r[ix['CD_TIPO_VOTAVEL']]), int(r[ix['QT_VOTOS']])
            tp[tv] += q
            if tv == 2:
                s['B'] += q
            elif tv == 3:
                s['N'] += q
            else:
                s['V'] += q
                if tv == 1:
                    n = str(int(r[ix['NR_VOTAVEL']])); s['cand'][n] = s['cand'].get(n, 0) + q
        tipos[uf] = dict(tp)
        del bruto
    with gzip.open(saida, 'wt', encoding='utf-8') as f:
        json.dump({'tipos_votavel': tipos, 'secoes': out}, f, separators=(',', ':'))
    print('ok', saida, len(out), tipos)


# ================================================================ análise
NOTA_POS_RESULTADO = """ACRESCENTADO DEPOIS DE VER O RESULTADO (o docstring acima fica igual ao gravado antes de calcular):
o bloco 8 da função rodar (posição em desvios, decomposição por ano, mesma UF em dois anos, régua interna de 2026,
aliado do partido do presidenciável, coeficiente próprio do presidenciável em todos os pares) e a função leitura.
São descritivos, marcados como exploratórios nas saídas, e não entram em nenhum veredito.
O subcomando conferir_bweb2t (comparação com o bweb do 2º turno, a fonte citada no registro) foi escrito depois do
docstring e antes de calcular qualquer D; ele só compara votos por candidato entre duas fontes."""
import hashlib, itertools
import numpy as np

NOMES = ['outros_1T', 'queda_branco_nulo', 'var_comparecimento', 'adversario_1T', 'proprio_1T']
S_TROCA = 0.036
DESLOC_LETRA = 0.0345
LIM_SINAL = -0.03
LIM_DISP = 0.03
MIN_NATURAIS = 8
SEMENTE = 20261110
CAMPOS_P = ('L1', 'R1', 'O1', 'bn1', 'c1', 'L2', 'R2', 'bn2', 'c2')
CAMPOS_G = ('fa1', 'fa2', 'fb1', 'fb2', 'out1', 'gbn1', 'gbn2', 'gc1', 'gc2')
ALIADOS_2026 = {'AC': '11', 'AM': '22', 'DF': '11', 'ES': '10', 'TO': '44'}       # F20 (Adendo 23)
CAMPO_LULA_2026 = {'AM': '55', 'DF': '13', 'RN': '13'}                            # F20, D3 e D7
VOTOS_FLAVIO_2T_BR = 59826041
MARGEM_BR = 4430191


def chave_local(k, s):
    uf, mun, zona, _ = k.split('|')
    return f"{uf}|{mun}|{zona}|{s['loc']}"


def carregar(p):
    with gzip.open(p, 'rt') as f:
        return json.load(f)


def montar(base, uf, nom1, nom2):
    """Matrizes por seção de uma UF. nom1 e nom2: {chave: {numero: votos nominais}} de governador no 1º e 2º turno.
    Só seções com presidente e governador nos dois turnos na base e nos dois dicionários."""
    tot2 = collections.Counter()
    ks = []
    for k, v in base.items():
        if k.split('|')[0] != uf or not all(t in v for t in ('1', '2', '1g', '2g')):
            continue
        if k not in nom1 or k not in nom2:
            continue
        ks.append(k); tot2.update(nom2[k])
    fin = [n for n, q in tot2.most_common() if q > 0]
    assert len(fin) == 2, (uf, tot2.most_common(5))
    fa, fb = fin
    M = {c: np.zeros(len(ks)) for c in CAMPOS_P + CAMPOS_G}
    loc = []
    for i, k in enumerate(ks):
        v = base[k]; a, b, ag, bg = v['1'], v['2'], v['1g'], v['2g']; c1, c2 = nom1[k], nom2[k]
        loc.append(chave_local(k, b))
        M['L1'][i] = a['L']; M['R1'][i] = a['R']; M['O1'][i] = a['O']; M['bn1'][i] = a['B'] + a['N']; M['c1'][i] = a['comp']
        M['L2'][i] = b['L']; M['R2'][i] = b['R']; M['bn2'][i] = b['B'] + b['N']; M['c2'][i] = b['comp']
        M['fa1'][i] = c1.get(fa, 0); M['fb1'][i] = c1.get(fb, 0)
        M['out1'][i] = sum(q for n, q in c1.items() if n not in (fa, fb))
        M['fa2'][i] = c2.get(fa, 0); M['fb2'][i] = c2.get(fb, 0)
        M['gbn1'][i] = ag['B'] + ag['N']; M['gbn2'][i] = bg['B'] + bg['N']; M['gc1'][i] = ag['comp']; M['gc2'][i] = bg['comp']
    M['loc'] = np.array(loc); M['fin'] = (fa, fb); M['uf'] = uf
    return M


def orienta(M, aliado):
    fa, fb = M['fin']
    assert aliado in (fa, fb), (M['uf'], aliado, M['fin'])
    return ('fa', 'fb') if aliado == fa else ('fb', 'fa')


def bloco(M, aliado, lado='R'):
    """Linhas do t22b para um lado. lado R: Bolsonaro ou Flávio e o aliado. lado L: candidato do PT e o aliado dele."""
    a, o = orienta(M, aliado)
    if lado == 'R':
        yP = M['R2'] - M['R1']; XP = np.column_stack([M['O1'], M['bn1'] - M['bn2'], M['c2'] - M['c1'], M['L1'], M['R1']])
    else:
        yP = M['L2'] - M['L1']; XP = np.column_stack([M['O1'], M['bn1'] - M['bn2'], M['c2'] - M['c1'], M['R1'], M['L1']])
    yG = M[a + '2'] - M[a + '1']
    XG = np.column_stack([M['out1'], M['gbn1'] - M['gbn2'], M['gc2'] - M['gc1'], M[o + '1'], M[a + '1']])
    return M['loc'], yP, XP, yG, XG


def reg(blocos):
    """Regressão empilhada do t22b (escrita de novo): dois cargos, coeficientes próprios, efeito fixo de local por
    cargo, erro CR1 agrupado por local. Devolve b (10), V (10x10), seções usadas, linhas, locais."""
    loc = np.concatenate([b[0] for b in blocos])
    yP = np.concatenate([b[1] for b in blocos]); XP = np.vstack([b[2] for b in blocos])
    yG = np.concatenate([b[3] for b in blocos]); XG = np.vstack([b[4] for b in blocos])
    _, li = np.unique(loc, return_inverse=True)
    keep = np.bincount(li)[li] >= 2
    if keep.sum() < 30:
        return None
    _, li = np.unique(li[keep], return_inverse=True); G = int(li.max()) + 1; cnt = np.bincount(li)

    def dm(A):
        A = A[keep].astype(float)
        if A.ndim == 1:
            return A - (np.bincount(li, weights=A) / cnt)[li]
        out = np.empty_like(A)
        for j in range(A.shape[1]):
            out[:, j] = A[:, j] - (np.bincount(li, weights=A[:, j]) / cnt)[li]
        return out
    yPd, XPd, yGd, XGd = dm(yP), dm(XP), dm(yG), dm(XG)
    iP = np.linalg.inv(XPd.T @ XPd); iG = np.linalg.inv(XGd.T @ XGd)
    bP = iP @ (XPd.T @ yPd); bG = iG @ (XGd.T @ yGd)
    eP = yPd - XPd @ bP; eG = yGd - XGd @ bG
    S = np.zeros((G, 10))
    for j in range(5):
        S[:, j] = np.bincount(li, weights=XPd[:, j] * eP, minlength=G)
        S[:, 5 + j] = np.bincount(li, weights=XGd[:, j] * eG, minlength=G)
    inv = np.zeros((10, 10)); inv[:5, :5] = iP; inv[5:, 5:] = iG
    n = int(keep.sum()); N = 2 * n; k = 10
    V = G / (G - 1) * (N - 1) / (N - k) * inv @ (S.T @ S) @ inv
    return np.concatenate([bP, bG]), V, n, N, G


cD = np.zeros(10); cD[4], cD[9] = 1, -1          # D = próprio(presidenciável) - próprio(aliado)
cE = np.zeros(10); cE[8], cE[3] = 1, -1          # espelho pela identidade = adversário(aliado) - adversário(presid.)
cC = cD - cE


def est(r, c):
    b, V = r[0], r[1]
    return [float(c @ b), float(np.sqrt(c @ V @ c))]


def resumo_reg(r, com_C=False):
    if r is None:
        return None
    b, V, n, N, G = r
    o = {'secoes': n, 'linhas': N, 'locais': G, 'D': est(r, cD),
         'proprio_presidenciavel': [float(b[4]), float(np.sqrt(V[4, 4]))],
         'proprio_governador': [float(b[9]), float(np.sqrt(V[9, 9]))],
         'coef_presidente': {nm: [float(b[i]), float(np.sqrt(V[i, i]))] for i, nm in enumerate(NOMES)},
         'coef_governador': {nm: [float(b[5 + i]), float(np.sqrt(V[5 + i, 5 + i]))] for i, nm in enumerate(NOMES)}}
    if com_C:
        o['espelho_pela_identidade'] = est(r, cE); o['C'] = est(r, cC)
    return o


# ---------------------------------------------------------------- efeitos plantados (E6)
def copia(M):
    return {k: (v.copy() if isinstance(v, np.ndarray) else v) for k, v in M.items()}


def planta_troca_pres(M, s, rng=None):
    """Troca só no presidente: fração s dos votos de R no 2º turno vira voto de L."""
    W = copia(M)
    x = rng.binomial(M['R2'].astype(np.int64), s).astype(float) if rng is not None else s * M['R2']
    W['R2'] = M['R2'] - x; W['L2'] = M['L2'] + x
    return W


def planta_abstencao(M, s, aliado, modo):
    """Explicação inocente: fração s dos eleitores de R no 2º turno não comparece (sai dos dois cargos)."""
    W = copia(M); a, o = orienta(M, aliado)
    n = s * M['R2']
    W['R2'] = M['R2'] - n; W['c2'] = M['c2'] - n
    gc = np.where(M['gc2'] > 0, M['gc2'], 1.0)
    if modo == 'proporcional':
        for c in (a + '2', o + '2', 'gbn2'):
            W[c] = M[c] - n * M[c] / gc
    else:  # todos do aliado, até o limite; o resto na proporção de adversário e branco mais nulo
        m = np.minimum(n, M[a + '2']); r = n - m
        den = M[o + '2'] + M['gbn2']; den = np.where(den > 0, den, 1.0)
        W[a + '2'] = M[a + '2'] - m
        W[o + '2'] = M[o + '2'] - r * M[o + '2'] / den
        W['gbn2'] = M['gbn2'] - r * M['gbn2'] / den
    W['gc2'] = M['gc2'] - n
    return W


def planta_troca_dois_cargos(M, s, aliado):
    W = planta_troca_pres(M, s); a, o = orienta(M, aliado)
    x = s * M[a + '2']
    W[a + '2'] = M[a + '2'] - x; W[o + '2'] = M[o + '2'] + x
    return W


# ---------------------------------------------------------------- critério da letra (E2 a E4)
def pct(v):
    v = np.asarray(v, float)
    return {'n': int(len(v)), 'p5': float(np.percentile(v, 5)), 'p95': float(np.percentile(v, 95)),
            'min': float(v.min()), 'max': float(v.max()), 'mediana': float(np.median(v)), 'media': float(v.mean()),
            'dp_ddof1': float(v.std(ddof=1)) if len(v) > 1 else None, 'dp_ddof0': float(v.std(ddof=0))}


def letra(D, p5, p95, desloc=DESLOC_LETRA):
    if D < p5 and D <= LIM_SINAL:
        return 'SINAL'
    if D + desloc > p95:
        return 'EXCLUSÃO'
    return 'INCONCLUSIVO'


def dispersao(lista):
    """lista de (D, ep). Dispersão bruta e descontado o erro de estimação."""
    d = np.array([x[0] for x in lista]); e = np.array([x[1] for x in lista])
    o = pct(d)
    o['media_ep2'] = float((e ** 2).mean())
    o['dp_descontado_erro'] = float(np.sqrt(max(0.0, d.var(ddof=1) - (e ** 2).mean()))) if len(d) > 1 else None
    return o


# ---------------------------------------------------------------- dados
def conferir_e_separar(base, uf, secoes_gov):
    """2018 e 2022: separa nominais de branco (95) e nulo (96) e confere contra 1g e 2g da base (X1)."""
    nom1, nom2 = {}, {}; conf = collections.Counter()
    for k, v in base.items():
        if k.split('|')[0] != uf:
            continue
        conf['secoes_na_base'] += 1
        if not all(t in v for t in ('1', '2', '1g', '2g')):
            conf['base_sem_os_4_blocos'] += 1; continue
        s = secoes_gov.get(k)
        if s is None or not s['1'] or not s['2']:
            conf['sem_governador_por_candidato'] += 1; continue
        ok = True
        for t, tg in (('1', '1g'), ('2', '2g')):
            B = s[t].get('95', 0); Nn = s[t].get('96', 0); V = sum(q for n, q in s[t].items() if n not in ('95', '96'))
            g = v[tg]
            if (B, Nn, V, B + Nn + V) != (g['B'], g['N'], g['V'], g['comp']):
                ok = False; conf[f'difere_turno_{t}'] += 1
        if not ok:
            conf['fora_por_conferencia'] += 1; continue
        conf['confere'] += 1
        nom1[k] = {n: q for n, q in s['1'].items() if n not in ('95', '96')}
        nom2[k] = {n: q for n, q in s['2'].items() if n not in ('95', '96')}
    conf['secoes_do_arquivo_fora_da_base'] = sum(1 for k in secoes_gov if k not in base)
    return nom1, nom2, dict(conf)


def salvar_M(M, p):
    np.savez_compressed(p, fin=np.array(M['fin']), uf=np.array(M['uf']), **{k: M[k] for k in CAMPOS_P + CAMPOS_G + ('loc',)})


def ler_M(p):
    z = np.load(p)
    M = {k: z[k] for k in CAMPOS_P + CAMPOS_G + ('loc',)}
    M['fin'] = tuple(str(x) for x in z['fin']); M['uf'] = str(z['uf'])
    return M


def preparar(trab, alin):
    """Monta e guarda as matrizes de cada par (2018, 2022) e das 6 UFs de 2026. Não calcula nenhum D."""
    pm = os.path.join(trab, 'M'); os.makedirs(pm, exist_ok=True)
    pc = os.path.join(trab, 'conferencia_dados.json')
    conf = json.load(open(pc)) if os.path.exists(pc) else {}
    for ano in ('2018', '2022'):
        falta = [uf for uf in PARES[ano] if not os.path.exists(os.path.join(pm, f'M_{ano}_{uf}.npz'))]
        if not falta:
            continue
        base = carregar(os.path.join(RAIZ, 'dados', f'secoes{ano}.json.gz'))
        for uf in falta:
            g = carregar(os.path.join(trab, 'gov', f'gov_{ano}_{uf}.json.gz'))
            nom1, nom2, c = conferir_e_separar(base, uf, g['secoes'])
            M = montar(base, uf, nom1, nom2)
            par = [p for p in alin['pares'] if p['ano'] == ano and p['uf'] == uf][0]
            assert set(M['fin']) == {f['numero'] for f in par['finalistas']}, (ano, uf, M['fin'])
            tot1 = collections.Counter(); tot2 = collections.Counter()
            for k in nom1:
                tot1.update(nom1[k]); tot2.update(nom2[k])
            c.update({'fonte': g['fonte'], 'dt_geracao': g['dt_geracao'], 'finalistas': list(M['fin']),
                      'nomes_2t': {n: g['nomes']['2'].get(n) for n in M['fin']},
                      'votos_1t_nas_secoes_usadas': {n: tot1[n] for n in M['fin']},
                      'votos_2t_nas_secoes_usadas': {n: tot2[n] for n in M['fin']},
                      'secoes_usadas': int(len(M['loc']))})
            conf[f'{ano}_{uf}'] = c
            salvar_M(M, os.path.join(pm, f'M_{ano}_{uf}.npz'))
            json.dump(conf, open(pc, 'w'), ensure_ascii=False, indent=1)
            print('montado', ano, uf, c.get('confere'), c.get('fora_por_conferencia', 0), flush=True)
        del base
    if not all(os.path.exists(os.path.join(pm, f'M_2026_{uf}.npz')) for uf in ('AC', 'AM', 'DF', 'ES', 'RN', 'TO')):
        base = carregar(os.path.join(RAIZ, 'dados', 'secoes2026.json.gz'))
        base = {k: v for k, v in base.items() if k.split('|')[0] in ('AC', 'AM', 'DF', 'ES', 'RN', 'TO')}
        g1 = carregar(os.path.join(RAIZ, 'dados', 'candidatos_gov_2026_1t_6ufs.json.gz'))['secoes']
        g2 = carregar(os.path.join(trab, 'gov2t_2026_6ufs.json.gz'))['secoes']
        pA2 = os.path.join(os.path.dirname(trab), 'A2', 'gov2t_6ufs.json.gz')
        gA2 = carregar(pA2) if os.path.exists(pA2) else None
        c = collections.Counter()
        nom2 = {}
        for k, v in base.items():
            if '2g' not in v:
                c['base_sem_2g'] += 1; continue
            s = g2.get(k)
            if s is None:
                c['zip_sem_secao'] += 1; continue
            igual = all(v['2g'][x] == s[x] for x in ('B', 'N', 'V', 'comp')) and sum(s['cand'].values()) == s['V']
            c['confere_com_a_base' if igual else 'difere_da_base'] += 1
            if gA2 is not None:
                a2 = gA2.get(k)
                c['igual_a_extracao_da_onda_A' if (a2 is not None and a2['nom'] == s['cand'] and a2['B'] == s['B'] and a2['N'] == s['N']) else 'difere_da_onda_A'] += 1
            if igual:
                nom2[k] = s['cand']
        c['secoes_sem_governador_1t_por_candidato'] = sum(1 for k in base if k not in g1)
        for uf in ('AC', 'AM', 'DF', 'ES', 'RN', 'TO'):
            M = montar(base, uf, g1, nom2)
            salvar_M(M, os.path.join(pm, f'M_2026_{uf}.npz'))
            c[f'secoes_usadas_{uf}'] = int(len(M['loc']))
        conf['2026'] = dict(c)
        json.dump(conf, open(pc, 'w'), ensure_ascii=False, indent=1)
        print('montado 2026', dict(c), flush=True)
    return conf


# ---------------------------------------------------------------- cálculo
def D_de(M, aliado, lado='R'):
    return resumo_reg(reg([bloco(M, aliado, lado)]), com_C=True)


def rodar(trab, palin, saida, saida_txt):
    alin = json.load(open(palin, encoding='utf-8'))
    sha = hashlib.sha256(open(palin, 'rb').read()).hexdigest()
    reg_sha = open(os.path.join(trab, 'alinhamento.sha256')).read().split()[0]
    assert sha == reg_sha, 'o alinhamento mudou depois de gravado'
    conf = preparar(trab, alin)
    pm = os.path.join(trab, 'M')
    out = {'teste': 'R27_T22: governador na mesma urna com régua (fragilidade "T22b e F20" da equipe vermelha)',
           'registro': 'PRE-REGISTRO-2026-10-26.md, Adendo 27 (commit 2748895) e Adendo 30 (commit a7218fb); '
                       'registro/adendo27/equipe_vermelha_relatorio.json, fragilidade "T22b e F20 (governador na mesma urna)"',
           'alinhamento': {'arquivo': os.path.relpath(palin, RAIZ), 'sha256': sha, 'gravado_em_utc': alin['gravado_em_utc'],
                           'resumo': alin['resumo']},
           'conferencia_dados': conf}
    parcial = os.path.join(trab, 'parcial_resultado.json')

    def grava():
        json.dump(out, open(parcial, 'w', encoding='utf-8'), ensure_ascii=False, indent=1)

    # ------------------------------------------------ 1) 2026 (conferência do código contra o publicado)
    M26 = {uf: ler_M(os.path.join(pm, f'M_2026_{uf}.npz')) for uf in ('AC', 'AM', 'DF', 'ES', 'RN', 'TO')}

    def emp26(ufs, lado='R', mapa=None, transf=None):
        mapa = mapa or ALIADOS_2026
        bl = []
        for u in ufs:
            M = M26[u] if transf is None else transf(M26[u], mapa[u] if lado == 'R' else ALIADOS_2026.get(u))
            bl.append(bloco(M, mapa[u], lado))
        return reg(bl)

    r3 = emp26(('AM', 'DF', 'ES')); rAM = emp26(('AM',)); r5 = emp26(('AC', 'AM', 'DF', 'ES', 'TO'))
    o26 = {'empilhado_AM_DF_ES': resumo_reg(r3), 'so_AM': resumo_reg(rAM, True), 'empilhado_5_UFs_F20': resumo_reg(r5),
           'por_uf': {u: D_de(M26[u], ALIADOS_2026[u]) for u in ALIADOS_2026},
           'publicado_para_conferir': {'T22b_AM_DF_ES': [0.0130, 0.0047], 'AM': [-0.0104, 0.0115], 'DF': [0.0103, 0.0067],
                                       'ES': [0.0489, 0.0060], 'AC': [0.0462, 0.0159], 'TO': [0.2979, 0.0153],
                                       'F20_5_UFs': [0.0466, 0.0049], 'espelho_AM_DF': [0.0017, 0.0062], 'C_AM': [-0.0225, 0.0142]}}
    # espelho e C de 2026
    esp = {'AM_DF': resumo_reg(emp26(('AM', 'DF'), 'L', CAMPO_LULA_2026))}
    for u in ('AM', 'DF', 'RN'):
        esp[u] = resumo_reg(emp26((u,), 'L', CAMPO_LULA_2026))
    o26['espelho'] = {k: {'espelho': v['D'], 'proprio_Lula': v['proprio_presidenciavel'],
                          'proprio_gov_campo_Lula': v['proprio_governador'], 'secoes': v['secoes']} for k, v in esp.items()}
    rC = emp26(('AM', 'DF'))
    o26['C'] = {'AM_DF': resumo_reg(rC, True), 'AM': resumo_reg(emp26(('AM',)), True), 'DF': resumo_reg(emp26(('DF',)), True)}
    pub = o26['publicado_para_conferir']
    difs = {'T22b_AM_DF_ES': o26['empilhado_AM_DF_ES']['D'][0] - pub['T22b_AM_DF_ES'][0],
            'F20_5_UFs': o26['empilhado_5_UFs_F20']['D'][0] - pub['F20_5_UFs'][0],
            'espelho_AM_DF': o26['espelho']['AM_DF']['espelho'][0] - pub['espelho_AM_DF'][0],
            'C_AM': o26['C']['AM']['C'][0] - pub['C_AM'][0]}
    for u in ALIADOS_2026:
        difs[u] = o26['por_uf'][u]['D'][0] - pub[u][0]
    o26['diferenca_para_o_publicado'] = difs
    o26['codigo_reproduz_o_publicado'] = bool(max(abs(x) for x in difs.values()) < 6e-5)
    o26['votos_Flavio_2t'] = {u: float(M26[u]['R2'].sum()) for u in M26}
    o26['votos_Lula_2t'] = {u: float(M26[u]['L2'].sum()) for u in M26}
    out['2026'] = o26; grava()
    print('2026 reproduz o publicado:', o26['codigo_reproduz_o_publicado'], difs, flush=True)
    if not o26['codigo_reproduz_o_publicado']:
        raise SystemExit('o código novo não reproduz os D publicados de 2026: parar e investigar antes de abrir 2018 e 2022')

    # ------------------------------------------------ 2) D naturais de 2018 e 2022
    Mn = {}
    def M_de(ano, uf):
        if (ano, uf) not in Mn:
            Mn[(ano, uf)] = ler_M(os.path.join(pm, f'M_{ano}_{uf}.npz'))
        return Mn[(ano, uf)]

    nat = {'principais': {}, 'secundario_duplos': {}, 'pela_coligacao_descritivo': {}, 'sensibilidade_outro_finalista': {},
           'espelho': {}, 'C_polarizados': {}}
    for p in alin['pares']:
        ano, uf = p['ano'], p['uf']; rot = f'{ano}_{uf}'
        M = M_de(ano, uf)
        decl = [f['numero'] for f in p['finalistas'] if f['atende_a_apoio_declarado_a_Bolsonaro']]
        if p['classe'] == 'limpo':
            r = D_de(M, p['aliado_de_Bolsonaro_principal']); r['aliado'] = p['aliado_de_Bolsonaro_principal']
            nat['principais'][rot] = r
            if p['polarizado_para_C']:
                nat['C_polarizados'][rot] = {'C': r['C'], 'D': r['D'], 'espelho_pela_identidade': r['espelho_pela_identidade']}
        if p['classe'] == 'duplo':
            al = p['aliado_de_Bolsonaro_secundario_desempate_D2']
            if al:
                r = D_de(M, al); r['aliado'] = al; nat['secundario_duplos'][rot] = r
            for n in decl:
                if n != al:
                    r = D_de(M, n); r['aliado'] = n; nat['sensibilidade_outro_finalista'][f'{rot}_{n}'] = r
        if p['aliado_so_pela_coligacao_robustez']:
            al = p['aliado_so_pela_coligacao_robustez']
            r = D_de(M, al); r['aliado'] = al; nat['pela_coligacao_descritivo'][rot] = r
        if p['finalista_do_campo_do_PT_para_o_espelho']:
            al = p['finalista_do_campo_do_PT_para_o_espelho']
            r = D_de(M, al, 'L')
            nat['espelho'][rot] = {'espelho': r['D'], 'proprio_PT': r['proprio_presidenciavel'],
                                   'proprio_gov_campo_PT': r['proprio_governador'], 'secoes': r['secoes'], 'aliado_PT': al}
    out['naturais'] = nat; grava()

    princ = [(k, v['D'][0], v['D'][1]) for k, v in nat['principais'].items()]
    sec = princ + [(k, v['D'][0], v['D'][1]) for k, v in nat['secundario_duplos'].items()]
    reguas = {'principais': dispersao([(d, e) for _, d, e in princ]),
              'principais_2018': dispersao([(d, e) for k, d, e in princ if k.startswith('2018')]),
              'principais_2022': dispersao([(d, e) for k, d, e in princ if k.startswith('2022')]),
              'secundario_principais_mais_duplos': dispersao([(d, e) for _, d, e in sec]),
              'mais_pela_coligacao': dispersao([(d, e) for _, d, e in sec] + [tuple(v['D']) for v in nat['pela_coligacao_descritivo'].values()]),
              'todos_com_sensibilidade': dispersao([(d, e) for _, d, e in sec] + [tuple(v['D']) for v in nat['pela_coligacao_descritivo'].values()]
                                                   + [tuple(v['D']) for v in nat['sensibilidade_outro_finalista'].values()]),
              'espelho': dispersao([tuple(v['espelho']) for v in nat['espelho'].values()]),
              'C_polarizados': dispersao([tuple(v['C']) for v in nat['C_polarizados'].values()])}
    out['reguas'] = reguas; grava()

    # ------------------------------------------------ 3) calibração em 2026 (E6 i, iii, iv)
    R = reguas['principais']; p5, p95 = R['p5'], R['p95']
    cal = {}
    def linha26(ufs, transf=None):
        r = emp26(ufs, transf=transf)
        return est(r, cD)
    for nome, ufs in (('empilhado_AM_DF_ES', ('AM', 'DF', 'ES')), ('so_AM', ('AM',))):
        D0 = linha26(ufs)
        c = {'D_observado': D0, 'grade_troca_so_presidente': {}}
        for s in (0.005, 0.01, 0.015, 0.02, 0.025, 0.03, 0.036, 0.04, 0.05, 0.06, 0.08, 0.10):
            Ds = linha26(ufs, lambda M, al, s=s: planta_troca_pres(M, s))
            c['grade_troca_so_presidente'][f'{s:.3f}'] = {'D': Ds, 'deslocamento': Ds[0] - D0[0], 'letra': letra(Ds[0], p5, p95)}
        g36 = c['grade_troca_so_presidente']['0.036']
        c['troca_3_6_valor_esperado'] = g36
        rng = np.random.default_rng(SEMENTE)
        Db = linha26(ufs, lambda M, al: planta_troca_pres(M, S_TROCA, rng))
        c['troca_3_6_binomial'] = {'D': Db, 'deslocamento': Db[0] - D0[0], 'letra': letra(Db[0], p5, p95), 'semente': SEMENTE}
        c['deslocamento_por_ponto_de_troca'] = (g36['D'][0] - D0[0]) / S_TROCA
        vistos = [float(s) for s, v in c['grade_troca_so_presidente'].items() if v['letra'] == 'SINAL']
        c['menor_troca_da_grade_que_o_criterio_ve'] = min(vistos) if vistos else None
        c['enxerga_a_troca_de_3_6'] = bool(g36['letra'] == 'SINAL')
        for modo in ('proporcional', 'todos_do_aliado'):
            Da = linha26(ufs, lambda M, al, modo=modo: planta_abstencao(M, S_TROCA, al, modo))
            c[f'inocente_abstencao_3_6_{modo}'] = {'D': Da, 'deslocamento': Da[0] - D0[0], 'letra': letra(Da[0], p5, p95)}
        Dd = linha26(ufs, lambda M, al: planta_troca_dois_cargos(M, S_TROCA, al))
        c['limite_troca_3_6_nos_dois_cargos'] = {'D': Dd, 'deslocamento': Dd[0] - D0[0], 'letra': letra(Dd[0], p5, p95)}
        cal[nome] = c
    # espelho e C de 2026 com a troca plantada (o espelho quase não deve se mover)
    rE = emp26(('AM', 'DF'), 'L', CAMPO_LULA_2026, transf=lambda M, al: planta_troca_pres(M, S_TROCA))
    rCt = emp26(('AM', 'DF'), transf=lambda M, al: planta_troca_pres(M, S_TROCA))
    rCtAM = emp26(('AM',), transf=lambda M, al: planta_troca_pres(M, S_TROCA))
    cal['espelho_AM_DF_com_troca_3_6'] = est(rE, cD)
    cal['C_AM_DF_com_troca_3_6'] = est(rCt, cC); cal['C_AM_com_troca_3_6'] = est(rCtAM, cC)
    cal['deslocamento_de_C_AM_DF'] = cal['C_AM_DF_com_troca_3_6'][0] - o26['C']['AM_DF']['C'][0]
    cal['deslocamento_de_C_AM'] = cal['C_AM_com_troca_3_6'][0] - o26['C']['AM']['C'][0]
    out['calibracao_2026'] = cal; grava()

    # ------------------------------------------------ 4) calibração nos naturais (E6 ii), deixando um de fora
    loo = {}
    for p in alin['pares']:
        if p['classe'] != 'limpo':
            continue
        rot = f"{p['ano']}_{p['uf']}"; al = p['aliado_de_Bolsonaro_principal']; M = M_de(p['ano'], p['uf'])
        outros = [d for k, d, e in princ if k != rot]
        q5 = float(np.percentile(outros, 5)); q95 = float(np.percentile(outros, 95))
        D0 = nat['principais'][rot]['D'][0]
        Dt = est(reg([bloco(planta_troca_pres(M, S_TROCA), al)]), cD)
        loo[rot] = {'D': D0, 'D_com_troca_3_6': Dt[0], 'deslocamento': Dt[0] - D0, 'p5_sem_o_proprio': q5, 'p95_sem_o_proprio': q95,
                    'letra_sem_troca': letra(D0, q5, q95), 'letra_com_troca': letra(Dt[0], q5, q95)}
    n = len(loo)
    out['calibracao_naturais'] = {
        'por_par': loo,
        'deteccao_da_troca_3_6': [sum(v['letra_com_troca'] == 'SINAL' for v in loo.values()), n],
        'falso_alarme_sem_troca': [sum(v['letra_sem_troca'] == 'SINAL' for v in loo.values()), n],
        'exclusao_indevida_com_troca': [sum(v['letra_com_troca'] == 'EXCLUSÃO' for v in loo.values()), n],
        'exclusao_sem_troca': [sum(v['letra_sem_troca'] == 'EXCLUSÃO' for v in loo.values()), n],
        'deslocamento_medio': float(np.mean([v['deslocamento'] for v in loo.values()]))}
    grava()

    # ------------------------------------------------ 5) trios empilhados do mesmo ano (E5)
    trios = {}
    for ano in ('2018', '2022'):
        ps = [p for p in alin['pares'] if p['classe'] == 'limpo' and p['ano'] == ano]
        for t in itertools.combinations(ps, 3):
            r = reg([bloco(M_de(ano, p['uf']), p['aliado_de_Bolsonaro_principal']) for p in t])
            trios[f"{ano}_" + '_'.join(p['uf'] for p in t)] = est(r, cD)
    reguas['trios_empilhados_mesmo_ano'] = dispersao([tuple(v) for v in trios.values()])
    out['trios'] = trios
    emp = {}
    for ano in ('2018', '2022', 'todos'):
        ps = [p for p in alin['pares'] if p['classe'] == 'limpo' and (ano == 'todos' or p['ano'] == ano)]
        emp[ano] = resumo_reg(reg([bloco(M_de(p['ano'], p['uf']), p['aliado_de_Bolsonaro_principal']) for p in ps]))
    out['naturais_empilhados_descritivo'] = {k: {'D': v['D'], 'secoes': v['secoes'], 'locais': v['locais']} for k, v in emp.items()}
    grava()

    # ------------------------------------------------ 6) vereditos pela letra (E4)
    D3 = o26['empilhado_AM_DF_ES']['D']; DAM = o26['so_AM']['D']
    n_nat = R['n']; disp = R['dp_ddof1']
    v = {'parte1_regua': {'n_naturais_principais': n_nat, 'dispersao_dp_ddof1': disp, 'limite': LIM_DISP,
                          'veredito': 'SEM PODER' if (disp > LIM_DISP or n_nat < MIN_NATURAIS) else 'COM PODER',
                          'motivo': ('dispersão natural acima de 0,03' if disp > LIM_DISP else '') +
                                    (' menos de 8 naturais' if n_nat < MIN_NATURAIS else '')},
         'percentis_principais': {'p5': p5, 'p95': p95}}
    for nome, D in (('empilhado_AM_DF_ES', D3), ('so_AM', DAM)):
        v[nome] = {'D': D, 'abaixo_do_p5': bool(D[0] < p5), 'menor_ou_igual_a_menos_0_03': bool(D[0] <= LIM_SINAL),
                   'D_mais_0_0345': D[0] + DESLOC_LETRA, 'acima_do_p95': bool(D[0] + DESLOC_LETRA > p95),
                   'letra': letra(D[0], p5, p95),
                   'posto_entre_os_naturais': int(sum(d < D[0] for _, d, _ in princ)),
                   'letra_no_conjunto_secundario': letra(D[0], reguas['secundario_principais_mais_duplos']['p5'], reguas['secundario_principais_mais_duplos']['p95']),
                   'letra_so_com_2018': letra(D[0], reguas['principais_2018']['p5'], reguas['principais_2018']['p95']),
                   'letra_so_com_2022': letra(D[0], reguas['principais_2022']['p5'], reguas['principais_2022']['p95'])}
    T = reguas['trios_empilhados_mesmo_ano']
    v['empilhado_AM_DF_ES']['letra_contra_trios_empilhados'] = letra(D3[0], T['p5'], T['p95'])
    v['empilhado_AM_DF_ES']['posto_entre_os_trios'] = [int(sum(x[0] < D3[0] for x in trios.values())), len(trios)]
    v['plantado_visto'] = {k: cal[k]['enxerga_a_troca_de_3_6'] for k in ('empilhado_AM_DF_ES', 'so_AM')}
    # espelho (E7)
    Re = reguas['espelho']
    v['espelho'] = {'regua': {'n': Re['n'], 'p5': Re['p5'], 'p95': Re['p95'], 'dp_ddof1': Re['dp_ddof1']}}
    for k in ('AM_DF', 'AM', 'DF', 'RN'):
        e = o26['espelho'][k]['espelho']
        v['espelho'][k] = {'espelho': e, 'letra_espelhada': letra(e[0], Re['p5'], Re['p95']),
                           'posto': [int(sum(x['espelho'][0] < e[0] for x in nat['espelho'].values())), Re['n']]}
    # C (E8)
    Rc = reguas['C_polarizados']
    v['C'] = {'regua': {'n': Rc['n'], 'p5': Rc['p5'], 'p95': Rc['p95'], 'dp_ddof1': Rc['dp_ddof1']}}
    for k, dk in (('AM_DF', -cal['deslocamento_de_C_AM_DF']), ('AM', -cal['deslocamento_de_C_AM']), ('DF', -cal['deslocamento_de_C_AM_DF'])):
        c = o26['C'][k]['C']
        v['C'][k] = {'C': c, 'deslocamento_usado': dk, 'letra_aplicada_a_C': letra(c[0], Rc['p5'], Rc['p95'], dk),
                     'posto': [int(sum(x['C'][0] < c[0] for x in nat['C_polarizados'].values())), Rc['n']]}
    final = 'SEM PODER' if (v['parte1_regua']['veredito'] == 'SEM PODER' or not v['plantado_visto']['empilhado_AM_DF_ES']) else v['empilhado_AM_DF_ES']['letra']
    v['veredito_do_teste'] = final
    out['vereditos'] = v; grava()

    # ------------------------------------------------ 7) tradução em votos (E9)
    k3 = cal['empilhado_AM_DF_ES']['deslocamento_por_ponto_de_troca']
    def votos(gap):
        s = abs(gap / k3)
        return {'fracao_dos_votos_de_Flavio': s, 'votos_trocados_no_pais': s * VOTOS_FLAVIO_2T_BR,
                'margem_equivalente_no_pais': 2 * s * VOTOS_FLAVIO_2T_BR, 'fracao_da_margem': 2 * s * VOTOS_FLAVIO_2T_BR / MARGEM_BR}
    R2_3 = sum(o26['votos_Flavio_2t'][u] for u in ('AM', 'DF', 'ES'))
    tr = {'deslocamento_de_D_por_ponto_de_troca': k3,
          'troca_3_6_no_pais': {'votos_trocados': S_TROCA * VOTOS_FLAVIO_2T_BR, 'margem': 2 * S_TROCA * VOTOS_FLAVIO_2T_BR},
          'votos_Flavio_2t_AM_DF_ES': R2_3, 'troca_3_6_em_AM_DF_ES_votos': S_TROCA * R2_3,
          'largura_faixa_natural_p5_p95': dict(votos(p95 - p5), largura=p95 - p5),
          'um_desvio_padrao_natural': dict(votos(disp), dp=disp),
          'maior_troca_que_nao_da_para_excluir_empilhado': dict(votos(max(0.0, p95 - D3[0])), folga_ate_p95=p95 - D3[0]),
          'troca_necessaria_para_o_criterio_ver_empilhado': dict(votos(max(0.0, D3[0] - min(p5, LIM_SINAL))), distancia=D3[0] - min(p5, LIM_SINAL)),
          'D_2026_menos_mediana_natural': dict(votos(D3[0] - R['mediana']), diferenca=D3[0] - R['mediana'],
                                               sentido='D de 2026 acima da mediana natural: contrário ao da troca' if D3[0] > R['mediana'] else 'D de 2026 abaixo da mediana natural: no sentido da troca')}
    out['traducao_em_votos'] = tr; grava()
    # ------------------------------------------------ 8) EXPLORATÓRIO: tudo abaixo foi acrescentado DEPOIS de ver o resultado
    from scipy import stats as _st
    ex = {'aviso': 'Acrescentado depois de ver os D de 2018 e 2022. Descritivo, fora do registro, não entra em veredito.'}

    def tpos(x, vals):
        vals = np.asarray(vals, float); n = len(vals); m = vals.mean(); sd = vals.std(ddof=1)
        t = (x - m) / (sd * np.sqrt(1 + 1 / n))
        return {'valor': float(x), 'n': int(n), 'media': float(m), 'dp': float(sd), 't_preditivo': float(t),
                'p_unicaudal_abaixo': float(_st.t.cdf(t, n - 1)), 'naturais_abaixo': int((vals < x).sum())}
    dn = [d for _, d, _ in princ]
    ex['posicao_t'] = {'empilhado_AM_DF_ES_contra_naturais': tpos(D3[0], dn), 'so_AM_contra_naturais': tpos(DAM[0], dn),
                       'empilhado_contra_trios': tpos(D3[0], [x[0] for x in trios.values()]),
                       'C_AM_DF_contra_C_naturais': tpos(o26['C']['AM_DF']['C'][0], [x['C'][0] for x in nat['C_polarizados'].values()]),
                       'C_AM_contra_C_naturais': tpos(o26['C']['AM']['C'][0], [x['C'][0] for x in nat['C_polarizados'].values()]),
                       'espelho_AM_DF_contra_espelhos_naturais': tpos(o26['espelho']['AM_DF']['espelho'][0], [x['espelho'][0] for x in nat['espelho'].values()])}
    def lado(rs):
        a = np.array([[r['proprio_presidenciavel'][0], r['proprio_governador'][0], r['D'][0]] for r in rs])
        return {'n': len(rs), 'proprio_presidenciavel_media': float(a[:, 0].mean()), 'proprio_presidenciavel_dp': float(a[:, 0].std(ddof=1)),
                'proprio_aliado_media': float(a[:, 1].mean()), 'proprio_aliado_dp': float(a[:, 1].std(ddof=1)),
                'D_media': float(a[:, 2].mean()), 'D_dp': float(a[:, 2].std(ddof=1)), 'D_mediana': float(np.median(a[:, 2]))}
    ex['decomposicao_por_ano'] = {
        '2018_principais': lado([v_ for k_, v_ in nat['principais'].items() if k_.startswith('2018')]),
        '2022_principais': lado([v_ for k_, v_ in nat['principais'].items() if k_.startswith('2022')]),
        '2026_AM_DF_ES': lado([o26['por_uf'][u] for u in ('AM', 'DF', 'ES')]),
        '2026_5_UFs': lado([o26['por_uf'][u] for u in ALIADOS_2026])}
    ex['regua_interna_2026'] = {'dp_D_entre_AM_DF_ES': ex['decomposicao_por_ano']['2026_AM_DF_ES']['D_dp'],
                                'dp_D_entre_as_5_UFs': ex['decomposicao_por_ano']['2026_5_UFs']['D_dp'],
                                'D_por_uf': {u: o26['por_uf'][u]['D'] for u in ALIADOS_2026}}
    ex['posto_por_ano'] = {nome: {'abaixo_em_2018': int(sum(d < D[0] for k_, d, _ in princ if k_.startswith('2018'))),
                                  'abaixo_em_2022': int(sum(d < D[0] for k_, d, _ in princ if k_.startswith('2022'))), 'de': 5}
                           for nome, D in (('empilhado_AM_DF_ES', D3), ('so_AM', DAM))}
    todos_D = dict(nat['principais']); todos_D.update(nat['secundario_duplos']); todos_D.update(nat['pela_coligacao_descritivo'])
    def mesma(uf, a, b, obs=''):
        ra = todos_D.get(f'{a}_{uf}') if a != '2026' else o26['por_uf'][uf]
        rb = todos_D.get(f'{b}_{uf}') if b != '2026' else o26['por_uf'][uf]
        return {'uf': uf, 'anos': [a, b], 'D': [ra['D'][0], rb['D'][0]], 'variacao_D': rb['D'][0] - ra['D'][0],
                'variacao_proprio_presidenciavel': rb['proprio_presidenciavel'][0] - ra['proprio_presidenciavel'][0],
                'variacao_proprio_aliado': rb['proprio_governador'][0] - ra['proprio_governador'][0], 'obs': obs}
    ex['mesma_UF_em_dois_anos'] = [
        mesma('SP', '2018', '2022', 'principais nos dois anos (Doria; Tarcísio)'),
        mesma('SC', '2018', '2022', '2018 pelo desempate (Moisés); 2022 principal (Jorginho)'),
        mesma('RO', '2018', '2022', 'os dois pelo desempate (Marcos Rocha; Marcos Rogério)'),
        mesma('AM', '2018', '2022', '2018 pelo desempate (Amazonino); 2022 principal (Wilson Lima)'),
        mesma('AM', '2022', '2026', 'Wilson Lima; Maria do Carmo'),
        mesma('ES', '2022', '2026', 'Manato; Pazolini'),
        mesma('DF', '2018', '2026', '2018 só pela coligação (Ibaneis, neutro); Celina Leão')]
    ex['mesma_UF_dp_das_variacoes_2018_2022'] = float(np.std([x['variacao_D'] for x in ex['mesma_UF_em_dois_anos'][:4]], ddof=1))
    partido_do_presid = {'2018_RR', '2022_ES', '2022_RS', '2022_SC', '2018_RO', '2018_SC', '2022_RO'}   # aliado do PSL (2018) ou do PL (2022)
    quinze = dict(nat['principais']); quinze.update(nat['secundario_duplos'])
    a_ = [v_['D'][0] for k_, v_ in quinze.items() if k_ in partido_do_presid]; b_ = [v_['D'][0] for k_, v_ in quinze.items() if k_ not in partido_do_presid]
    ex['aliado_do_partido_do_presidenciavel'] = {'do_partido': pct(a_), 'de_outro_partido': pct(b_),
                                                 'AM_2026_PL_naturais_do_partido_abaixo': int(sum(x < DAM[0] for x in a_))}
    pp = {}
    for ano in ('2018', '2022'):
        for uf in PARES[ano]:
            M = M_de(ano, uf); r_ = reg([bloco(M, M['fin'][0], 'R')])
            pp[f'{ano}_{uf}'] = [float(r_[0][4]), float(np.sqrt(r_[1][4, 4]))]
    for uf in M26:
        r_ = reg([bloco(M26[uf], M26[uf]['fin'][0], 'R')])
        pp[f'2026_{uf}'] = [float(r_[0][4]), float(np.sqrt(r_[1][4, 4]))]
    ex['proprio_do_presidenciavel_da_direita_em_todos_os_pares'] = dict(sorted(pp.items(), key=lambda kv: kv[1][0]))
    ex['proprio_do_presidenciavel_2026_menos_eleicao_anterior_na_mesma_UF'] = {
        'AM_contra_2022': pp['2026_AM'][0] - pp['2022_AM'][0], 'ES_contra_2022': pp['2026_ES'][0] - pp['2022_ES'][0],
        'RN_contra_2018': pp['2026_RN'][0] - pp['2018_RN'][0], 'DF_contra_2018': pp['2026_DF'][0] - pp['2018_DF'][0]}
    out['exploratorio_depois_de_ver_o_resultado'] = ex; grava()

    out['docstring_sha256_antes_de_rodar'] = open(os.path.join(trab, 'docstring_antes_de_rodar.sha256')).read().strip()
    out['nota_pos_resultado'] = NOTA_POS_RESULTADO
    out['veredito_por_parte'] = {
        'parte1_regua': v['parte1_regua']['veredito'], 'empilhado_AM_DF_ES': v['empilhado_AM_DF_ES']['letra'], 'so_AM': v['so_AM']['letra'],
        'espelho': v['espelho']['AM_DF']['letra_espelhada'], 'C': v['C']['AM_DF']['letra_aplicada_a_C'],
        'troca_3_6_plantada_vista': v['plantado_visto'], 'teste': v['veredito_do_teste'],
        'depende_so_de_comparacao_com_outros_anos': True}
    pcb = os.path.join(trab, 'conferencia_bweb2t.json')
    if os.path.exists(pcb):
        out['conferencia_bweb2t'] = json.load(open(pcb))
    LE = leitura(out)
    out['leitura_escrita_depois_de_ver_o_resultado'] = LE
    with open(saida, 'w', encoding='utf-8') as f:
        json.dump(out, f, ensure_ascii=False, indent=1)
    with open(saida_txt, 'w', encoding='utf-8') as f:
        f.write(texto(out, LE))
    print('ok', saida, saida_txt, 'veredito', final)


# ================================================================ texto
def leitura(out):
    """Tudo aqui foi ESCRITO DEPOIS DE VER O RESULTADO. Os números saem do próprio resultado; as frases são leitura."""
    v = out['vereditos']; R = out['reguas']; o26 = out['2026']; nat = out['naturais']; cal = out['calibracao_2026']
    cn = out['calibracao_naturais']; tr = out['traducao_em_votos']; ex = out['exploratorio_depois_de_ver_o_resultado']
    P = R['principais']; D3 = v['empilhado_AM_DF_ES']['D']; DAM = v['so_AM']['D']
    pt = ex['posicao_t']; dc = ex['decomposicao_por_ano']; mu = {(x['uf'], x['anos'][0], x['anos'][1]): x for x in ex['mesma_UF_em_dois_anos']}
    pos = sum(1 for x in nat['principais'].values() if x['D'][0] > 0)
    c3 = cal['empilhado_AM_DF_ES']; cA = cal['so_AM']
    L = []; A = L.append
    A('EXPLORATÓRIO (acrescentado depois de ver o resultado; fora do registro; não entra em veredito)')
    A('  Posição de 2026 na régua em desvios (t preditivo, uma cauda, supondo naturais normais):')
    A(f"    D empilhado contra os {P['n']} naturais: t {f(pt['empilhado_AM_DF_ES_contra_naturais']['t_preditivo'], 2)}, p {g(pt['empilhado_AM_DF_ES_contra_naturais']['p_unicaudal_abaixo'], 2)}; "
      f"D de AM: t {f(pt['so_AM_contra_naturais']['t_preditivo'], 2)}, p {g(pt['so_AM_contra_naturais']['p_unicaudal_abaixo'], 2)}; "
      f"D empilhado contra os {pt['empilhado_contra_trios']['n']} trios: t {f(pt['empilhado_contra_trios']['t_preditivo'], 2)}, p {g(pt['empilhado_contra_trios']['p_unicaudal_abaixo'], 2)}.")
    A(f"    C de AM e DF contra os {pt['C_AM_DF_contra_C_naturais']['n']} C naturais: t {f(pt['C_AM_DF_contra_C_naturais']['t_preditivo'], 2)}, p {g(pt['C_AM_DF_contra_C_naturais']['p_unicaudal_abaixo'], 2)}; "
      f"C de AM: t {f(pt['C_AM_contra_C_naturais']['t_preditivo'], 2)}, p {g(pt['C_AM_contra_C_naturais']['p_unicaudal_abaixo'], 2)}; "
      f"espelho de AM e DF contra os {pt['espelho_AM_DF_contra_espelhos_naturais']['n']} espelhos: t {f(pt['espelho_AM_DF_contra_espelhos_naturais']['t_preditivo'], 2)}, p {g(pt['espelho_AM_DF_contra_espelhos_naturais']['p_unicaudal_abaixo'], 2)}.")
    pa = ex['posto_por_ano']
    A(f"  Por ano: abaixo do D empilhado de 2026 ficam {pa['empilhado_AM_DF_ES']['abaixo_em_2018']} dos 5 naturais de 2018 e {pa['empilhado_AM_DF_ES']['abaixo_em_2022']} dos 5 de 2022; "
      f"abaixo do D de AM, {pa['so_AM']['abaixo_em_2018']} e {pa['so_AM']['abaixo_em_2022']}.")
    A('  De onde vem a diferença entre os anos (média simples dos coeficientes próprios; dp entre UFs entre parênteses):')
    for k, rot in (('2018_principais', '2018, 5 pares      '), ('2022_principais', '2022, 5 pares      '), ('2026_AM_DF_ES', '2026, AM, DF e ES  ')):
        x = dc[k]
        A(f"    {rot} presidenciável {f(x['proprio_presidenciavel_media'], 3)} ({g(x['proprio_presidenciavel_dp'], 3)}); aliado {f(x['proprio_aliado_media'], 3)} ({g(x['proprio_aliado_dp'], 3)}); D {f(x['D_media'], 3)} ({g(x['D_dp'], 3)})")
    d1 = dc['2022_principais']['D_media'] - dc['2018_principais']['D_media']; d2 = dc['2026_AM_DF_ES']['D_media'] - dc['2022_principais']['D_media']
    A(f"    De 2018 para 2022 o D médio cai {g(-d1, 3)}: o coeficiente do presidenciável SOBE {g(dc['2022_principais']['proprio_presidenciavel_media'] - dc['2018_principais']['proprio_presidenciavel_media'], 3)} "
      f"e o do aliado sobe {g(dc['2022_principais']['proprio_aliado_media'] - dc['2018_principais']['proprio_aliado_media'], 3)}. A queda vem do lado do governador.")
    A(f"    De 2022 para 2026 o D médio cai {g(-d2, 3)}: o coeficiente do presidenciável cai {g(dc['2022_principais']['proprio_presidenciavel_media'] - dc['2026_AM_DF_ES']['proprio_presidenciavel_media'], 3)} "
      f"e o do aliado cai {g(dc['2022_principais']['proprio_aliado_media'] - dc['2026_AM_DF_ES']['proprio_aliado_media'], 3)}. A queda vem do lado do presidente, com 5 e 3 UFs diferentes.")
    A('  Mesma UF em duas eleições, variação de D: ' + '; '.join(f"{x['uf']} {x['anos'][0]} a {x['anos'][1]} {f(x['variacao_D'], 3)}" for x in ex['mesma_UF_em_dois_anos']) + '.')
    ri = ex['regua_interna_2026']
    A(f"  Régua interna de 2026, sem outro ano: desvio-padrão do D entre AM, DF e ES {g(ri['dp_D_entre_AM_DF_ES'], 3)}; entre as 5 UFs do F20 {g(ri['dp_D_entre_as_5_UFs'], 3)}.")
    ap = ex['aliado_do_partido_do_presidenciavel']
    A(f"  Aliado do próprio partido do presidenciável (PSL em 2018, PL em 2022; {ap['do_partido']['n']} pares): D mediano {f(ap['do_partido']['mediana'], 3)}, dp {g(ap['do_partido']['dp_ddof1'], 3)}; "
      f"de outro partido ({ap['de_outro_partido']['n']} pares): mediano {f(ap['de_outro_partido']['mediana'], 3)}, dp {g(ap['de_outro_partido']['dp_ddof1'], 3)}. "
      f"AM em 2026 (aliada do PL): {ap['AM_2026_PL_naturais_do_partido_abaixo']} de {ap['do_partido']['n']} abaixo.")
    A('')
    A('LEITURA (escrita depois de ver o resultado)')
    A('O que a régua mostrou')
    A(f"  1. D não tem zero natural. Em {pos} dos {P['n']} pares de 2018 e 2022 o presidenciável da direita perdeu uma fração MENOR dos próprios")
    A(f"     eleitores que o aliado a governador (D de {f(P['min'], 3)} a {f(P['max'], 3)}, mediana {f(P['mediana'], 3)}). A variação natural entre estados")
    A(f"     (desvio-padrão {g(P['dp_ddof1'], 3)}) é maior que o deslocamento que a troca de 3,6% produz (0,0345).")
    A('  2. Por isso o desenho não separa "troca só no presidente do tamanho que vira a eleição" de "diferença normal entre estados".')
    A('     Pela letra fica SEM PODER. O "SEM SINAL" do T22b (Adendo 14), que supunha D natural igual a zero, e a "EXCLUSÃO" do F20')
    A('     (Adendo 23) não valem mais como contrapeso à tese. O teste também não acusa nada.')
    A('A favor da tese, com o mesmo rigor')
    A(f"  a. Contra a régua, o D de 2026 fica na parte de baixo: só {v['empilhado_AM_DF_ES']['posto_entre_os_naturais']} dos {P['n']} naturais ficam abaixo do empilhado ({f(D3[0], 3)}) e "
      f"{v['so_AM']['posto_entre_os_naturais']} abaixo do de AM ({f(DAM[0], 3)},")
    A(f"     a {g(DAM[0] - P['p5'], 4)} do percentil 5). A distância do empilhado até a mediana natural ({g(-tr['D_2026_menos_mediana_natural']['diferenca'], 3)}) equivale a uma troca de "
      f"{g(100 * tr['D_2026_menos_mediana_natural']['fracao_dos_votos_de_Flavio'], 1)}% dos votos de Flávio,")
    A('     mais do que os 3,6% que viram o resultado. Não passa de nenhum limiar: pela conta exploratória, um valor assim ou mais baixo')
    A(f"     sai por acaso em cerca de {g(100 * pt['empilhado_AM_DF_ES_contra_naturais']['p_unicaudal_abaixo'], 0)}% das vezes (AM: {g(100 * pt['so_AM_contra_naturais']['p_unicaudal_abaixo'], 0)}%).")
    cnat = sorted(x['C'][0] for x in nat['C_polarizados'].values())
    A(f"  b. O contraste C de 2026 (AM e DF {f(o26['C']['AM_DF']['C'][0])}; AM {f(o26['C']['AM']['C'][0])}; DF {f(o26['C']['DF']['C'][0])}) fica abaixo dos {len(cnat)} C naturais ({f(cnat[0])} a {f(cnat[-1])}).")
    A(f"     São só {len(cnat)} naturais, 4 deles de 2022, e nenhum C de 2026 chega a -0,03. Pela conta exploratória: p {g(pt['C_AM_DF_contra_C_naturais']['p_unicaudal_abaixo'], 2)} (AM e DF) e {g(pt['C_AM_contra_C_naturais']['p_unicaudal_abaixo'], 2)} (AM).")
    A(f"  c. Os 5 naturais de 2018, ano em que a direita venceu, são todos mais altos ({f(R['principais_2018']['min'], 3)} a {f(R['principais_2018']['max'], 3)}) que qualquer D de AM, DF e ES em 2026.")
    A(f"  d. O coeficiente próprio de Flávio em AM, DF e ES (média {f(dc['2026_AM_DF_ES']['proprio_presidenciavel_media'], 3)}) é mais negativo que o de Bolsonaro nos naturais de 2022 ({f(dc['2022_principais']['proprio_presidenciavel_media'], 3)}),")
    A(f"     e o do aliado a governador ficou quase igual ({f(dc['2026_AM_DF_ES']['proprio_aliado_media'], 3)} contra {f(dc['2022_principais']['proprio_aliado_media'], 3)}). Diferença de {g(dc['2022_principais']['proprio_presidenciavel_media'] - dc['2026_AM_DF_ES']['proprio_presidenciavel_media'], 3)}, perto do que a troca de 3,6% daria,")
    A('     mas com UFs diferentes nos dois anos e desvio entre UFs de 0,02 a 0,03 (cerca de 1,3 erro-padrão). Item visto depois do dado.')
    A('Contra a tese, com o mesmo rigor')
    A(f"  a. Pela letra não há sinal: nem o empilhado nem AM ficam abaixo do percentil 5 ({f(P['p5'], 4)}), e nenhum chega a -0,03.")
    A(f"  b. 2026 está dentro da faixa natural. Na comparação de igual para igual (D empilhado contra trios empilhados do mesmo ano),")
    A(f"     {v['empilhado_AM_DF_ES']['posto_entre_os_trios'][0]} dos {v['empilhado_AM_DF_ES']['posto_entre_os_trios'][1]} trios ficam abaixo de 2026. Com todos os principais de 2022 empilhados o D é {f(out['naturais_empilhados_descritivo']['2022']['D'][0], 4)}, abaixo do de 2026.")
    e_ = v['espelho']
    A(f"  c. O espelho, que a troca não move, também fica abaixo da mediana da régua dele ({f(e_['AM_DF']['espelho'][0], 3)} contra {f(R['espelho']['mediana'], 3)}; {e_['AM_DF']['posto'][0]} de {e_['AM_DF']['posto'][1]} abaixo;")
    A(f"     RN {e_['RN']['posto'][0]} de {e_['RN']['posto'][1]}). Em 2026 D e espelho estão os dois perto de zero: parte do \"D baixo\" aparece também do lado de Lula.")
    A(f"     A distância do espelho à mediana dele ({g(R['espelho']['mediana'] - e_['AM_DF']['espelho'][0], 3)}) é menor que a do D ({g(-tr['D_2026_menos_mediana_natural']['diferenca'], 3)}); a diferença é o que o C mede (item b a favor).")
    es = mu[('ES', '2022', '2026')]
    A(f"  d. ES, a única UF com a mesma estrutura (aliado da direita contra não alinhado ou do outro campo) em 2022 e 2026, tem o mesmo D: {f(es['D'][0], 3)} e {f(es['D'][1], 3)}.")
    A('     (Se as duas eleições tiverem a mesma troca, isso não distingue nada; pesa só contra "troca nova em 2026".)')
    A('  e. A diferença entre 2018 e os anos seguintes vem do lado do governador (aliados de 2018 perderam muito mais dos próprios')
    A('     eleitores), e o coeficiente de Bolsonaro até subiu de 2018 para 2022. Troca só no presidente agiria no coeficiente do presidente.')
    A(f"  f. O D de uma mesma UF muda de uma eleição para outra tanto ou mais do que a troca moveria, nos dois sentidos: de 2018 a 2022,")
    A(f"     SP {f(mu[('SP', '2018', '2022')]['variacao_D'], 3)}, SC {f(mu[('SC', '2018', '2022')]['variacao_D'], 3)}, AM {f(mu[('AM', '2018', '2022')]['variacao_D'], 3)}, RO {f(mu[('RO', '2018', '2022')]['variacao_D'], 3)}. Em AM, de 2022 a 2026, {f(mu[('AM', '2022', '2026')]['variacao_D'], 3)}, dos quais {f(-mu[('AM', '2022', '2026')]['variacao_proprio_aliado'], 3)}")
    A(f"     vêm do lado do governador (troca de candidato aliado) e {f(mu[('AM', '2022', '2026')]['variacao_proprio_presidenciavel'], 3)} do lado do presidente.")
    A('  g. O fato bruto que o T22b relatou continua de pé: em AM e DF o aliado a governador perdeu os próprios eleitores na mesma')
    A('     proporção que Flávio, na mesma urna. O que mudou é a leitura: nos anos de referência o aliado costumava perder MAIS.')
    A('O que isso significa em votos')
    A(f"  A faixa natural de D (percentil 5 a 95) tem a largura de uma troca de {g(100 * tr['largura_faixa_natural_p5_p95']['fracao_dos_votos_de_Flavio'], 1)}% dos votos de Flávio ({mil(tr['largura_faixa_natural_p5_p95']['margem_equivalente_no_pais'])} votos de margem")
    A(f"  se fosse no país inteiro, {g(tr['largura_faixa_natural_p5_p95']['fracao_da_margem'], 1)} vezes a margem). Um desvio-padrão natural vale {g(100 * tr['um_desvio_padrao_natural']['fracao_dos_votos_de_Flavio'], 1)}% ({mil(tr['um_desvio_padrao_natural']['margem_equivalente_no_pais'])} votos, {g(100 * tr['um_desvio_padrao_natural']['fracao_da_margem'], 0)}% da margem).")
    A(f"  A cláusula de sinal só dispararia no empilhado com troca de {g(100 * tr['troca_necessaria_para_o_criterio_ver_empilhado']['fracao_dos_votos_de_Flavio'], 1)}% ou mais; a de exclusão não exclui nada abaixo de {g(100 * tr['maior_troca_que_nao_da_para_excluir_empilhado']['fracao_dos_votos_de_Flavio'], 1)}%.")
    A(f"  O teste cobre {mil(tr['votos_Flavio_2t_AM_DF_ES'])} votos de Flávio (AM, DF e ES), {g(100 * tr['votos_Flavio_2t_AM_DF_ES'] / VOTOS_FLAVIO_2T_BR, 1)}% dos dele no país.")
    A('Limites')
    A('  1. O veredito depende só da comparação com 2018 e 2022. Se nesses anos houve a mesma troca só no presidente, os naturais já')
    A(f"     vêm deslocados e a comparação é cega. Sem outro ano, a régua interna de 2026 dá o mesmo recado: o D varia {g(ri['dp_D_entre_AM_DF_ES'], 3)} entre AM, DF e ES")
    A(f"     e {g(ri['dp_D_entre_as_5_UFs'], 3)} entre as 5 UFs.")
    A(f"  2. Cego, por desenho, a desvio que mexa também no governador (troca plantada nos dois cargos move D em {f(c3['limite_troca_3_6_nos_dois_cargos']['deslocamento'], 4)}) ou que poupe as 6 UFs.")
    A(f"  3. Só {P['n']} naturais com fonte clara (o registro previa 26); percentis 5 e 95 de {P['n']} valores são quase o mínimo e o máximo.")
    A(f"  4. Calibração: a troca de 3,6% plantada em 2026 não é vista no empilhado; nos naturais é vista em {cn['deteccao_da_troca_3_6'][0]} de {cn['deteccao_da_troca_3_6'][1]}; a cláusula de")
    A(f"     exclusão erra para os dois lados (\"exclui\" {cn['exclusao_sem_troca'][0]} de {cn['exclusao_sem_troca'][1]} pares sem troca e {cn['exclusao_indevida_com_troca'][0]} de {cn['exclusao_indevida_com_troca'][1]} com a troca plantada).")
    A(f"     A explicação inocente plantada (abstenção de eleitores de Flávio nos dois cargos) move D em {f(c3['inocente_abstencao_3_6_proporcional']['deslocamento'], 4)} e {f(c3['inocente_abstencao_3_6_todos_do_aliado']['deslocamento'], 4)}: não imita a troca.")
    A('  5. Rodado por um agente só. Falta o conferente independente (regra do Adendo 27).')
    A('Desvios do registro (todos decididos antes de calcular qualquer D de 2018 ou 2022; detalhes no docstring e no arquivo de alinhamento)')
    A('  1. Fonte: arquivo de votação por seção do TSE (traz os dois turnos por candidato) em vez do bweb, porque o D precisa do voto por')
    A('     candidato a governador também no 1º turno. Conferido contra as bases e, no 2º turno, contra o bweb que o registro cita.')
    A('  2. Zip lido em fluxo por faixas de bytes, sem gravar em disco, em vez de baixar e apagar.')
    A(f"  3. Naturais: {P['n']} principais em vez de 26 (regra de um só finalista no campo de Bolsonaro, com fonte); duplos e casos só pela coligação ao lado.")
    A('  4. Refinamento gravado no arquivo de alinhamento, depois do docstring e antes de qualquer D: candidato com o partido de Bolsonaro')
    A('     na coligação que declarou neutralidade (DF e PA em 2018) conta como fonte contraditória e sai.')
    A('  5. O alinhamento foi fixado pelo mesmo agente que depois calculou o D (o registro pedia outro agente), antes de qualquer D, com')
    A('     hash e hora gravados.')
    A('  6. Percentis por interpolação linear; desvio-padrão amostral; precedência das cláusulas; trios empilhados; critério aplicado a C;')
    A('     RN no espelho: decisões do docstring.')
    A('Contagem: 2 estatísticas registradas (empilhado e AM) em 2 cláusulas, mais espelho e C: 0 sinal, 0 exclusão.')
    A('Pistas (o que daria poder a este desenho, ou onde olhar)')
    A(f"  1. O contraste C varia menos que o D (desvio-padrão {g(R['C_polarizados']['dp_ddof1'], 3)} contra {g(P['dp_ddof1'], 3)}) e em 2026 ficou abaixo dos {R['C_polarizados']['n']} naturais. Uma régua de C com mais")
    A('     pares polarizados (2º turno de governador de 2014, 2010 e 2006, PT contra PSDB, pelo mesmo arquivo do TSE) diria se isso é acaso.')
    pp = ex['proprio_do_presidenciavel_da_direita_em_todos_os_pares']; ordem = list(pp); dq = ex['proprio_do_presidenciavel_2026_menos_eleicao_anterior_na_mesma_UF']
    A(f"  2. Só o lado do presidente (não depende de alinhamento): o coeficiente próprio de Flávio em AM ({f(pp['2026_AM'][0], 3)}) é o {ordem.index('2026_AM') + 1}º mais negativo")
    A(f"     dos {len(pp)} calculados (26 pares de 2018 e 2022 e 6 UFs de 2026; o mais baixo é {ordem[0].replace('_', ' ')}, {f(pp[ordem[0]][0], 3)}); RN, TO e AC de 2026 estão em {ordem.index('2026_RN') + 1}º, {ordem.index('2026_TO') + 1}º e {ordem.index('2026_AC') + 1}º.")
    A(f"     Nas quatro UFs que se repetem, o de 2026 é mais negativo que o da eleição anterior: AM {f(dq['AM_contra_2022'], 3)} e ES {f(dq['ES_contra_2022'], 3)} contra 2022;")
    A(f"     RN {f(dq['RN_contra_2018'], 3)} e DF {f(dq['DF_contra_2018'], 3)} contra 2018 (a troca de 3,6% daria -0,035). Em AM a aliada perdeu o mesmo ({f(o26['por_uf']['AM']['proprio_governador'][0], 3)}), o que casa com")
    A('     eleitor que não voltou (os dois cargos caem juntos) e não com troca só no presidente. É o canal do comparecimento das ondas')
    A('     A e B, que se decide em caderno de votação, não em boletim.')
    A('  3. Este desenho só alcança troca que poupe o governador. As testemunhas (D4-3 e D4-4) seguem sendo os únicos desenhos')
    A('     registrados que enxergam troca uniforme e coerente dentro da urna.')
    return L


def f(x, d=4):
    return f'{x:+.{d}f}'.replace('.', ',')


def g(x, d=4):
    return f'{x:.{d}f}'.replace('.', ',')


def mil(x):
    return f'{int(round(x)):,}'.replace(',', '.')


def de(v, d=4):
    return f'{f(v[0], d)} (ep {g(v[1], d)})'


def texto(out, leitura=None):
    L = []; A = L.append
    v = out['vereditos']; R = out['reguas']; o26 = out['2026']; nat = out['naturais']; cal = out['calibracao_2026']
    cn = out['calibracao_naturais']; tr = out['traducao_em_votos']; al = out['alinhamento']
    P = R['principais']
    A('R27_T22 (Adendo 27, onda D-c; Adendo 30, última onda): GOVERNADOR NA MESMA URNA COM RÉGUA')
    A('Fragilidade "T22b e F20 (governador na mesma urna)" da equipe vermelha. Rodado em 10/11/2026.')
    A('Script: scripts/analisar_R27_T22.py (decisões no docstring, gravado antes de calcular: ' + out['docstring_sha256_antes_de_rodar'].split()[0][:16] + '...).')
    A(f"Alinhamento gravado antes de qualquer D de 2018 ou 2022: {al['arquivo']} ({al['gravado_em_utc']}, sha256 {al['sha256'][:16]}...).")
    A('Aviso do registro: este reteste foi escolhido por quem já conhecia os D de 2026. O critério é novo. Os D de 2018 e 2022')
    A('não eram conhecidos de ninguém antes desta rodada.')
    A('')
    A('O QUE O TESTE MEDE')
    A('  Na mesma urna, quanto dos próprios eleitores do 1º turno o presidenciável da direita perde até o 2º turno, menos')
    A('  quanto perde o candidato a governador do campo dele (D). Troca feita só no voto de presidente puxa D para baixo')
    A('  (troca de 3,6% dos votos: cerca de -0,0345). A pergunta desta rodada: quanto D varia sozinho, sem troca nenhuma?')
    A('  A régua são os pares UF e ano de 2018 e 2022 com 2º turno de governador e um finalista claramente do campo de Bolsonaro.')
    A('')
    A('VEREDITO PELA LETRA, POR PARTE')
    p1 = v['parte1_regua']
    A(f"  Parte 1, régua: {p1['veredito']}. Dispersão natural de D (desvio-padrão dos {p1['n_naturais_principais']} naturais principais): "
      f"{g(p1['dispersao_dp_ddof1'])}; limite da letra: 0,03.")
    for nome, rot in (('empilhado_AM_DF_ES', 'D de 2026 empilhado em AM, DF e ES'), ('so_AM', 'D de 2026 só em AM')):
        x = v[nome]
        A(f"  Partes 2 e 3, {rot}: {x['letra']}. D = {de(x['D'])}; percentil 5 dos naturais {f(P['p5'])}, percentil 95 {f(P['p95'])}; "
          f"D + 0,0345 = {f(x['D_mais_0_0345'])}.")
        A(f"      abaixo do percentil 5: {'sim' if x['abaixo_do_p5'] else 'não'}; de -0,03 ou menos: {'sim' if x['menor_ou_igual_a_menos_0_03'] else 'não'}; "
          f"D + 0,0345 acima do percentil 95: {'sim' if x['acima_do_p95'] else 'não'}; naturais abaixo do D de 2026: {x['posto_entre_os_naturais']} de {P['n']}.")
    pv = v['plantado_visto']
    A(f"  Troca de 3,6% plantada em 2026: o critério {'ENXERGA' if pv['empilhado_AM_DF_ES'] else 'NÃO ENXERGA'} no empilhado "
      f"(D plantado {f(cal['empilhado_AM_DF_ES']['troca_3_6_valor_esperado']['D'][0])}, letra {cal['empilhado_AM_DF_ES']['troca_3_6_valor_esperado']['letra']}) e "
      f"{'ENXERGA' if pv['so_AM'] else 'NÃO ENXERGA'} em AM (D plantado {f(cal['so_AM']['troca_3_6_valor_esperado']['D'][0])}, letra {cal['so_AM']['troca_3_6_valor_esperado']['letra']}).")
    e_ = v['espelho']; c_ = v['C']
    A(f"  Espelho (lado de Lula, que a troca não move): {e_['AM_DF']['letra_espelhada']} pela letra espelhada. AM e DF {de(e_['AM_DF']['espelho'])}; régua de {e_['regua']['n']} pares, "
      f"percentil 5 {f(e_['regua']['p5'])}, percentil 95 {f(e_['regua']['p95'])}, desvio-padrão {g(e_['regua']['dp_ddof1'])}.")
    A(f"  Contraste C = D menos espelho: {c_['AM_DF']['letra_aplicada_a_C']} pela letra aplicada a C. AM e DF {de(c_['AM_DF']['C'])}; AM {de(c_['AM']['C'])}; régua de {c_['regua']['n']} pares, "
      f"percentil 5 {f(c_['regua']['p5'])}, desvio-padrão {g(c_['regua']['dp_ddof1'])}. Os C de 2026 ficam abaixo dos {c_['regua']['n']} naturais, sem chegar a -0,03.")
    A(f"  VEREDITO DO TESTE: {v['veredito_do_teste']}. O desenho deixa de ser citado como contrapeso (T22b \"sem sinal\", F20 \"exclusão\") e também não é indício.")
    A('  O veredito depende só da comparação com 2018 e 2022 (anos de que o Léo também suspeita). Ver "limites".')
    A('')
    A('DADOS')
    c = out['conferencia_dados']
    tot = sum(x.get('confere', 0) for k, x in c.items() if k != '2026'); fora = sum(x.get('fora_por_conferencia', 0) for k, x in c.items() if k != '2026')
    A(f"  2018 e 2022: voto por candidato a governador nos dois turnos, por seção, do arquivo de votação por seção do TSE (26 pares")
    A(f"  UF e ano, lidos em fluxo, sem gravar zip). Conferência contra as bases (branco, nulo, válidos e comparecimento de governador,")
    A(f"  1º e 2º turno): {mil(tot)} seções conferem, {mil(fora)} não conferem.")
    cb = out.get('conferencia_bweb2t')
    if cb:
        ig = sum(x.get('igual', 0) for x in cb.values()); di = sum(x.get('diferente', 0) for x in cb.values())
        so = sum(x.get('so_no_bweb', 0) + x.get('so_na_votacao_por_secao', 0) for x in cb.values()); er = [k for k, x in cb.items() if 'erro' in x]
        A(f"  Contra o bweb do 2º turno (a fonte que o registro cita), voto por candidato a governador seção a seção: {mil(ig)} seções iguais,")
        A(f"  {mil(di)} diferentes, {mil(so)} só em uma das fontes" + (f"; não conferidos: {', '.join(er)}." if er else '.'))
    c26 = c['2026']
    A(f"  2026: governador do 2º turno por candidato lido de novo dos zips do bweb: {mil(c26.get('confere_com_a_base', 0))} seções iguais à base, "
      f"{mil(c26.get('difere_da_base', 0))} diferentes; iguais à extração da onda A em {mil(c26.get('igual_a_extracao_da_onda_A', 0))}.")
    A(f"  O código novo reproduz os D publicados de 2026 (T22b, F20, espelho, C): {'sim' if o26['codigo_reproduz_o_publicado'] else 'NÃO'}"
      f" (maior diferença {g(max(abs(x) for x in o26['diferenca_para_o_publicado'].values()), 5)}, arredondamento).")
    A('')
    A('ALINHAMENTO (regra do F20 transposta; fontes no arquivo de alinhamento)')
    rs = al['resumo']
    A(f"  Naturais principais (um só finalista no campo de Bolsonaro), {len(rs['principais_limpos'])}: " + ', '.join(f'{a} {u} {n}' for a, u, n in rs['principais_limpos']) + '.')
    A(f"  Secundário (os dois no campo; desempate pelo partido de Bolsonaro), {len(rs['secundario_duplos_com_desempate'])}: " + ', '.join(f'{a} {u} {n}' for a, u, n in rs['secundario_duplos_com_desempate']) + '.')
    A(f"  Fora do D: " + ', '.join(f'{a} {u} ({cl})' for a, u, cl in rs['fora_do_D']) + '; duplos sem desempate: ' + ', '.join(f'{a} {u}' for a, u in rs['duplos_sem_desempate_fora']) + '.')
    A(f"  Espelho (um só finalista no campo do PT), {len(rs['espelho'])}: " + ', '.join(f'{a} {u} {n}' for a, u, n in rs['espelho']) + '.')
    A(f"  Polarizados, para C, {len(rs['polarizados_para_C'])}: " + ', '.join(f'{a} {u}' for a, u in rs['polarizados_para_C']) + '.')
    A('  O registro falava em 26 D naturais. Com fonte clara e um só aliado, sobram ' + str(P['n']) + '.')
    A('')
    A('VALOR BRUTO DE 2026 (sem comparação com outro ano)')
    A(f"  Empilhado AM, DF, ES: D = {de(o26['empilhado_AM_DF_ES']['D'])}; {mil(o26['empilhado_AM_DF_ES']['secoes'])} seções, {mil(o26['empilhado_AM_DF_ES']['locais'])} locais.")
    for u, r in o26['por_uf'].items():
        A(f"  {u} (aliado {ALIADOS_2026[u]}): próprio de Flávio {de(r['proprio_presidenciavel'])}; do aliado {de(r['proprio_governador'])}; D = {de(r['D'])}")
    A(f"  Empilhado nas 5 UFs do F20: D = {de(o26['empilhado_5_UFs_F20']['D'])}.")
    A('')
    A('D NATURAIS (próprio de Bolsonaro menos próprio do aliado a governador, mesma regressão, por UF)')
    A('  par       aliado  seções   próprio Bolsonaro    próprio aliado       D')
    def lin(k, r):
        return f"  {k.replace('_', ' '):<9} {r['aliado']:>4}  {r['secoes']:>7}   {de(r['proprio_presidenciavel']):<20} {de(r['proprio_governador']):<20} {de(r['D'])}"
    A('  principais:')
    for k, r in sorted(nat['principais'].items(), key=lambda kv: kv[1]['D'][0]):
        A(lin(k, r))
    A('  secundário (duplos com desempate):')
    for k, r in sorted(nat['secundario_duplos'].items(), key=lambda kv: kv[1]['D'][0]):
        A(lin(k, r))
    A('  descritivo, o outro finalista dos duplos como aliado:')
    for k, r in sorted(nat['sensibilidade_outro_finalista'].items(), key=lambda kv: kv[1]['D'][0]):
        A(lin(k[:7], r))
    A('  descritivo, só pela coligação (candidato declarou neutralidade):')
    for k, r in sorted(nat['pela_coligacao_descritivo'].items(), key=lambda kv: kv[1]['D'][0]):
        A(lin(k, r))
    A('')
    A('RÉGUA')
    def reg_l(nome, x):
        return (f"  {nome:<44} n {x['n']:>2}  p5 {f(x['p5'])}  mediana {f(x['mediana'])}  p95 {f(x['p95'])}  mín {f(x['min'])}  máx {f(x['max'])}  "
                f"dp {g(x['dp_ddof1']) if x['dp_ddof1'] is not None else 'nd'}  dp sem erro de estimação {g(x['dp_descontado_erro']) if x['dp_descontado_erro'] is not None else 'nd'}")
    for nome, k in (('principais (a régua da letra)', 'principais'), ('principais de 2018', 'principais_2018'), ('principais de 2022', 'principais_2022'),
                    ('principais mais duplos com desempate', 'secundario_principais_mais_duplos'), ('mais os dois só pela coligação', 'mais_pela_coligacao'),
                    ('todos, com o outro finalista dos duplos', 'todos_com_sensibilidade'), ('trios empilhados do mesmo ano', 'trios_empilhados_mesmo_ano'),
                    ('espelho (lado do PT)', 'espelho'), ('C nos polarizados', 'C_polarizados')):
        A(reg_l(nome, R[k]))
    ne = out['naturais_empilhados_descritivo']
    A(f"  D com todos os principais empilhados: 2018 {de(ne['2018']['D'])}; 2022 {de(ne['2022']['D'])}; os dois anos {de(ne['todos']['D'])}.")
    x = v['empilhado_AM_DF_ES']
    A(f"  O D empilhado de 2026 contra os trios empilhados: letra {x['letra_contra_trios_empilhados']}; trios abaixo dele: {x['posto_entre_os_trios'][0]} de {x['posto_entre_os_trios'][1]}.")
    A(f"  Letra com outras réguas (empilhado / só AM): secundário {x['letra_no_conjunto_secundario']} / {v['so_AM']['letra_no_conjunto_secundario']}; "
      f"só 2018 {x['letra_so_com_2018']} / {v['so_AM']['letra_so_com_2018']}; só 2022 {x['letra_so_com_2022']} / {v['so_AM']['letra_so_com_2022']}.")
    A('')
    A('CALIBRAÇÃO POR EFEITO PLANTADO')
    for nome, rot in (('empilhado_AM_DF_ES', 'AM, DF e ES empilhados'), ('so_AM', 'só AM')):
        c_ = cal[nome]
        A(f"  2026, {rot}: D observado {de(c_['D_observado'])}")
        A('    troca só no presidente (valor esperado): ' + '; '.join(f"{g(100 * float(s), 1)}% D {f(x_['D'][0])} {x_['letra']}" for s, x_ in c_['grade_troca_so_presidente'].items()))
        b_ = c_['troca_3_6_binomial']
        A(f"    troca de 3,6% por sorteio binomial: D {f(b_['D'][0])}, {b_['letra']}. Deslocamento de D por ponto de troca: {g(c_['deslocamento_por_ponto_de_troca'], 3)}.")
        m = c_['menor_troca_da_grade_que_o_criterio_ve']
        A(f"    menor troca da grade que a cláusula de sinal vê: {g(100 * m, 1) + '% dos votos de Flávio' if m else 'nenhuma até 10%'}.")
        a1, a2 = c_['inocente_abstencao_3_6_proporcional'], c_['inocente_abstencao_3_6_todos_do_aliado']
        A(f"    explicação inocente plantada (3,6% dos eleitores de Flávio faltam ao 2º turno nos dois cargos): proporcional D {f(a1['D'][0])} ({a1['letra']}); "
          f"todos do aliado D {f(a2['D'][0])} ({a2['letra']}).")
        d2 = c_['limite_troca_3_6_nos_dois_cargos']
        A(f"    limite do desenho, troca de 3,6% nos dois cargos: D {f(d2['D'][0])} (deslocamento {f(d2['deslocamento'])}): {d2['letra']}.")
    A(f"  Nos naturais, um de fora por vez: a troca de 3,6% plantada é vista em {cn['deteccao_da_troca_3_6'][0]} de {cn['deteccao_da_troca_3_6'][1]} pares; "
      f"falso alarme sem troca em {cn['falso_alarme_sem_troca'][0]} de {cn['falso_alarme_sem_troca'][1]}; "
      f"'exclusão' com a troca plantada (erro) em {cn['exclusao_indevida_com_troca'][0]} de {cn['exclusao_indevida_com_troca'][1]}; "
      f"'exclusão' sem troca em {cn['exclusao_sem_troca'][0]} de {cn['exclusao_sem_troca'][1]}.")
    A('')
    A('ESPELHO (próprio do candidato do PT menos próprio do governador do campo do PT; a troca só no presidente quase não o move)')
    e = v['espelho']
    A(f"  régua: {e['regua']['n']} pares, p5 {f(e['regua']['p5'])}, p95 {f(e['regua']['p95'])}, dp {g(e['regua']['dp_ddof1'])}")
    for k, rot in (('AM_DF', 'AM e DF empilhados'), ('AM', 'AM'), ('DF', 'DF'), ('RN', 'RN')):
        A(f"  2026 {rot}: espelho {de(e[k]['espelho'])}; letra espelhada {e[k]['letra_espelhada']}; naturais abaixo: {e[k]['posto'][0]} de {e[k]['posto'][1]}")
    A(f"  com a troca de 3,6% plantada, o espelho de AM e DF fica em {de(cal['espelho_AM_DF_com_troca_3_6'])}.")
    A('  espelhos naturais: ' + '; '.join(f"{k.replace('_', ' ')} {f(x_['espelho'][0])}" for k, x_ in sorted(nat['espelho'].items(), key=lambda kv: kv[1]['espelho'][0])))
    A('')
    A('CONTRASTE C = D MENOS ESPELHO (pares com um finalista de cada campo; critério aplicado a C é decisão desta rodada)')
    c_ = v['C']
    A(f"  régua: {c_['regua']['n']} pares, p5 {f(c_['regua']['p5'])}, p95 {f(c_['regua']['p95'])}, dp {g(c_['regua']['dp_ddof1'])}")
    A('  C naturais: ' + '; '.join(f"{k.replace('_', ' ')} {de(x_['C'])}" for k, x_ in sorted(nat['C_polarizados'].items(), key=lambda kv: kv[1]['C'][0])))
    for k, rot in (('AM_DF', 'AM e DF empilhados'), ('AM', 'AM'), ('DF', 'DF')):
        A(f"  2026 {rot}: C = {de(c_[k]['C'])}; letra aplicada a C: {c_[k]['letra_aplicada_a_C']}; naturais abaixo: {c_[k]['posto'][0]} de {c_[k]['posto'][1]}")
    A(f"  com a troca de 3,6% plantada: C de AM e DF {de(cal['C_AM_DF_com_troca_3_6'])}; C de AM {de(cal['C_AM_com_troca_3_6'])}.")
    A('')
    A('TRADUÇÃO EM VOTOS DE MARGEM (regra de três com a troca plantada; 3,6% dos votos de Flávio no país = '
      + mil(tr['troca_3_6_no_pais']['votos_trocados']) + ' votos trocados = ' + mil(tr['troca_3_6_no_pais']['margem']) + ' de margem)')
    def vt(x):
        return f"{g(100 * x['fracao_dos_votos_de_Flavio'], 2)}% dos votos de Flávio, {mil(x['margem_equivalente_no_pais'])} votos de margem no país ({g(100 * x['fracao_da_margem'], 0)}% da margem)"
    A(f"  Largura da faixa natural (percentil 5 a 95, {g(tr['largura_faixa_natural_p5_p95']['largura'])}): {vt(tr['largura_faixa_natural_p5_p95'])}.")
    A(f"  Um desvio-padrão natural ({g(tr['um_desvio_padrao_natural']['dp'])}): {vt(tr['um_desvio_padrao_natural'])}.")
    A(f"  Maior troca que a régua não deixa excluir no empilhado (folga até o percentil 95, {f(tr['maior_troca_que_nao_da_para_excluir_empilhado']['folga_ate_p95'])}): {vt(tr['maior_troca_que_nao_da_para_excluir_empilhado'])}.")
    A(f"  Troca que seria preciso para a cláusula de sinal disparar no empilhado (distância {g(tr['troca_necessaria_para_o_criterio_ver_empilhado']['distancia'])}): {vt(tr['troca_necessaria_para_o_criterio_ver_empilhado'])}.")
    dm_ = tr['D_2026_menos_mediana_natural']
    A(f"  D de 2026 menos a mediana natural: {f(dm_['diferenca'])} ({dm_['sentido']}); em troca equivalente: {vt(dm_)}.")
    A(f"  Votos de Flávio no 2º turno em AM, DF e ES: {mil(tr['votos_Flavio_2t_AM_DF_ES'])}; 3,6% deles: {mil(tr['troca_3_6_em_AM_DF_ES_votos'])} votos.")
    if leitura:
        A('')
        L.extend(leitura)
    return '\n'.join(L) + '\n'


# ================================================================ conferência com o bweb do 2º turno (X1)
URL_BWEB2T = {'2018': 'https://cdn.tse.jus.br/estatistica/sead/eleicoes/eleicoes2018/buweb/BWEB_2t_{uf}_301020181744.zip',
              '2022': 'https://cdn.tse.jus.br/estatistica/sead/eleicoes/eleicoes2022/buweb/bweb_2t_{uf}_311020221535.zip'}


def conferir_bweb2t(trab):
    """O registro fala no bweb do 2º turno. Baixa o bweb do 2º turno de cada par (pequeno), uma UF por vez, em pasta
    nova e vazia, lê o governador por candidato (filtro por bytes) e compara, seção a seção, com o que veio do
    arquivo de votação por seção. Apaga o zip. Não calcula nenhum D."""
    import shutil, zipfile
    psai = os.path.join(trab, 'conferencia_bweb2t.json')
    res = json.load(open(psai)) if os.path.exists(psai) else {}
    op = _abridor()
    for ano in ('2018', '2022'):
        for uf in PARES[ano]:
            rot = f'{ano}_{uf}'
            if rot in res:
                continue
            url = URL_BWEB2T[ano].format(uf=uf)
            time.sleep(1.0)
            try:
                r = op.open(urllib.request.Request(url, method='HEAD'), timeout=60)
            except urllib.error.HTTPError as e:
                if e.code in (429, 403, 407):
                    raise SystemExit(f'parado: HTTP {e.code}')
                res[rot] = {'erro': f'HTTP {e.code}', 'url': url}; continue
            tam = int(r.headers['Content-Length'])
            if tam > 80 << 20:
                res[rot] = {'erro': 'maior que 80 MB, não baixado', 'tamanho': tam, 'url': url}; continue
            pasta = os.path.join(trab, 'bweb2t_tmp', rot)
            if os.path.exists(pasta):
                shutil.rmtree(pasta)
            os.makedirs(pasta)
            pz = os.path.join(pasta, 'b.zip')
            time.sleep(1.0)
            with op.open(urllib.request.Request(url), timeout=300) as r, open(pz, 'wb') as f:
                shutil.copyfileobj(r, f)
            assert os.path.getsize(pz) == tam
            z = zipfile.ZipFile(pz)
            nome = [n for n in z.namelist() if n.lower().endswith(('.csv', '.txt'))][0]
            bruto = z.read(nome)
            pnl = bruto.find(b'\n')
            cab = next(csv.reader([bruto[:pnl].decode('latin1').strip()], delimiter=';'))
            ix = {c.strip().replace('SG_ UF', 'SG_UF'): i for i, c in enumerate(cab)}
            marca = re.compile(rb'\n[^\n]*;"?3"?;"?Governador"?;[^\n]*', re.I)
            linhas = [m.group(0)[1:].rstrip(b'\r') for m in marca.finditer(bruto)]
            sec = {}
            for r_ in csv.reader(io.StringIO(b'\n'.join(linhas).decode('latin1'), newline=''), delimiter=';'):
                if r_[ix['CD_CARGO_PERGUNTA']] != '3':
                    continue
                k = f"{uf}|{int(r_[ix['CD_MUNICIPIO']])}|{int(r_[ix['NR_ZONA']])}|{int(r_[ix['NR_SECAO']])}"
                tv = int(r_[ix['CD_TIPO_VOTAVEL']]); q = int(r_[ix['QT_VOTOS']])
                n = '95' if tv == 2 else '96' if tv == 3 else str(int(r_[ix['NR_VOTAVEL']]))
                d = sec.setdefault(k, {}); d[n] = d.get(n, 0) + q
            g = carregar(os.path.join(trab, 'gov', f'gov_{ano}_{uf}.json.gz'))['secoes']
            c = collections.Counter()
            for k, d in sec.items():
                a = g.get(k)
                if a is None:
                    c['so_no_bweb'] += 1
                elif {n: q for n, q in a['2'].items() if q} == {n: q for n, q in d.items() if q}:
                    c['igual'] += 1
                else:
                    c['diferente'] += 1
            c['so_na_votacao_por_secao'] = sum(1 for k in g if k not in sec)
            res[rot] = dict(c, url=url, tamanho=tam, cabecalho_tem=sorted(ix)[:0])
            shutil.rmtree(pasta)
            json.dump(res, open(psai, 'w'), ensure_ascii=False, indent=1)
            print(rot, dict(c), flush=True)
    json.dump(res, open(psai, 'w'), ensure_ascii=False, indent=1)
    return res


if __name__ == '__main__':
    if sys.argv[1] == 'extrair':
        extrair(sys.argv[2], sys.argv[3], sys.argv[4])
    elif sys.argv[1] == 'extrair2026':
        extrair2026(sys.argv[2], sys.argv[3])
    elif sys.argv[1] == 'conferir_bweb2t':
        conferir_bweb2t(sys.argv[2])
    elif sys.argv[1] == 'preparar':
        preparar(sys.argv[2], json.load(open(sys.argv[3], encoding='utf-8')))
    elif sys.argv[1] == 'rodar':
        rodar(*sys.argv[2:6])
