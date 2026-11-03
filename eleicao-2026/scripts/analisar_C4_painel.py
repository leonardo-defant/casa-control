"""C4 (tarefa PAINEL) do Adendo 24: leitura do painel que o reel @assis.salvioli (DfHTWubBajq) cita, essencia-ai.com.

Registro: PRE-REGISTRO-2026-10-26.md, Adendo 24 (commit ca110bb, 03/11/2026 04:24:10 UTC). O Adendo fixa C1, C2 e C3;
a leitura do painel não está nele e não tem critério de sinal. Este script só organiza o que foi baixado (páginas HTML,
nunca código do site) e faz contas aritméticas com os números do reel e com os resultados já gravados de C1 e C2.

Decisões (o registro não fixa; escritas aqui antes de calcular e declaradas como desvio no resultado)
  D1. Leitura só do HTML servido pelas páginas do site. Nenhum arquivo .js, .css, fonte ou imagem do site é baixado ou
      executado (regra da tarefa). Downloads numa pasta nova e vazia: /home/user/trabalho-eleicao/adendo24/C4_painel_dl.
  D2. curl com o user agent padrão, sem cookies e sem cabeçalhos especiais (nem "RSC: 1" nem nada que imite navegador).
      Login, 403, 429 ou desafio: parar e registrar, sem contorno.
  D3. Fontes alternativas permitidas: outras páginas HTML do mesmo site, robots.txt e sitemap.xml, a API pública de
      disponibilidade do Wayback Machine, archive.ph, a página do autor no Instagram e busca na web. Feitas à mão antes
      deste script; o script relê os arquivos gravados e o log de tentativas abaixo (TENTATIVAS).
  D4. Para cada pergunta da tarefa, quatro camadas separadas: (i) o que o painel diz; (ii) o que o reel diz, pela
      degravação, em trecho literal; (iii) o que a aritmética dos números do reel permite inferir (inferência nossa,
      marcada como tal); (iv) o que C1 e C2 já mediram (lidos dos JSON, nada recalculado sobre a base).
  D5. Sem veredito de sinal: o Adendo 24 não fixa critério para o painel. O resultado diz só se foi possível ler.
  D6. "Margem do reel" = 4.357.147 e "universo do reel" = 492.988 urnas, os implícitos da cena 2 (C1, P1_reel); a margem
      das 27 UFs (4.401.534) vai ao lado.
  D7. Projeção nacional das órfãs pela fração da amostra, sem peso amostral (C2, D13): só ordem de grandeza.
  D8. "Score zero" lido como o maior score de comparação da janela igual a zero (C2, D12), que é a leitura literal.
"""
import hashlib
import json
import os
import re
import sys

REPO = '/home/user/casa-control/eleicao-2026'
DL = '/home/user/trabalho-eleicao/adendo24/C4_painel_dl'
SAIDA = os.path.join(REPO, 'resultados', 'C4_painel_reel.txt')

# Log das tentativas feitas à mão (D3), 03/11/2026, depois do commit do Adendo. Códigos HTTP e respostas observados.
TENTATIVAS = [
    ('https://essencia-ai.com/', 'home.html', '200; agência de IA (produto Dashfy, consultoria); o único link ao tema é "Auditoria 2026" no rodapé'),
    ('https://essencia-ai.com/auditoria-2026', 'auditoria-2026.html', '200, sem login e sem 403; texto visível só menu e rodapé'),
    ('https://essencia-ai.com/sobre-nos', 'sobre-nos.html', '200; institucional'),
    ('https://essencia-ai.com/solucoes', 'solucoes.html', '200; institucional'),
    ('https://essencia-ai.com/produtos', 'produtos.html', '200; produto Dashfy'),
    ('https://essencia-ai.com/termos-de-servico', 'termos-de-servico.html', '200'),
    ('https://essencia-ai.com/politica-de-privacidade', 'politica-de-privacidade.html', '200'),
    ('https://essencia-ai.com/robots.txt', 'robots.txt', '404'),
    ('https://essencia-ai.com/sitemap.xml', 'sitemap.xml', '404'),
    ('WebFetch de https://essencia-ai.com/auditoria-2026 (leitor sem JavaScript)', None,
     'resposta: "apenas menu de navegação, dados de contato, redes sociais e rodapé"'),
    ('https://archive.org/wayback/available?url=essencia-ai.com/auditoria-2026', 'wayback_avail.json',
     '200; "archived_snapshots": {} (nenhuma cópia arquivada)'),
    ('https://web.archive.org/cdx/search/cdx?url=essencia-ai.com*', None,
     'conexão reiniciada no proxy, duas tentativas; sem resposta'),
    ('https://archive.ph/newest/https://essencia-ai.com/auditoria-2026', 'archiveph.html',
     '429 com desafio; não contornado'),
    ('https://www.instagram.com/assis.salvioli/ (link da bio)', None,
     '302 para https://www.instagram.com/accounts/login/; não contornado'),
    ('Busca na web, 6 consultas (domínio essencia-ai.com; "digitais órfãs"; nome do autor; EssencIA "Auditoria 2026"; '
     'números exatos 1.280.132, 2.514.969 e 15.709.293)', None, 'nada indexado do painel nem dos números'),
]

TERMOS = ['urna', 'biometr', 'eleiç', 'eleic', 'TSE', 'Lula', 'Flávio', 'órfã', 'orfa', 'score']


def n_(x, casas=0):
    if casas == 0:
        s = f'{round(x):,}'
    else:
        s = f'{x:,.{casas}f}'
    return s.replace(',', 'X').replace('.', ',').replace('X', '.')


def p_(x, casas=2):
    return n_(x, casas)


def s_(x, casas=3):
    return ('+' if x > 0 else '') + n_(x, casas)


def sha(caminho):
    h = hashlib.sha256()
    with open(caminho, 'rb') as f:
        h.update(f.read())
    return h.hexdigest()


def texto_visivel(html):
    sem = re.sub(r'<script[^>]*>.*?</script>', ' ', html, flags=re.S)
    sem = re.sub(r'<style[^>]*>.*?</style>', ' ', sem, flags=re.S)
    sem = re.sub(r'<svg[^>]*>.*?</svg>', ' ', sem, flags=re.S)
    sem = re.sub(r'<[^>]+>', ' ', sem)
    return re.sub(r'\s+', ' ', sem).strip()


def main():
    linhas = []
    w = linhas.append

    c1 = json.load(open(os.path.join(REPO, 'resultados', 'C1_nivel_mudanca_biometria.json')))
    c2 = json.load(open(os.path.join(REPO, 'resultados', 'C2_digitais_orfas.json')))

    # ---------- páginas baixadas ----------
    pag = {}
    for url, arq, nota in TENTATIVAS:
        if arq and os.path.exists(os.path.join(DL, arq)):
            cam = os.path.join(DL, arq)
            with open(cam, encoding='utf-8', errors='replace') as f:
                h = f.read()
            pag[arq] = {'bytes': os.path.getsize(cam), 'sha256': sha(cam), 'html': h}

    aud = pag['auditoria-2026.html']['html']
    vis_aud = texto_visivel(aud).replace('\u2014', '-').replace('\u2013', '-')  # travessão do original vira hífen
    tem_client_root = 'ClientPageRoot' in aud
    m_chunk = re.search(r'static/chunks/app/auditoria-2026/page-[0-9a-f]+\.js', aud)
    chunk = m_chunk.group(0) if m_chunk else None
    m_title = re.search(r'<title>(.*?)</title>', aud)
    m_desc = re.search(r'<meta name="description" content="([^"]*)"', aud)
    termos_achados = {}
    for arq, d in pag.items():
        if not arq.endswith('.html') or arq == 'archiveph.html':
            continue
        v = texto_visivel(d['html'])
        termos_achados[arq] = sorted({t for t in TERMOS if t.lower() in v.lower()})
    datas = {}
    for nome in ('home_headers.txt', 'auditoria_headers.txt'):
        cam = os.path.join(DL, nome)
        if os.path.exists(cam):
            for ln in open(cam, encoding='utf-8', errors='replace'):
                if ln.lower().startswith('date:'):
                    datas[nome] = ln.split(':', 1)[1].strip()
                if ln.lower().startswith('x-fah-adapter') or ln.lower().startswith('x-nextjs-prerender'):
                    datas.setdefault(nome + '_srv', []).append(ln.strip())

    # ---------- números do reel (degravação) ----------
    reel = c1['P1_reel']
    orfas_reel = 1280132
    margem_reel = 4357147  # implícita (D6)
    assert abs(reel['margem_mais_10_Lula'] / (reel['parte_margem_mais_10'] / 100) - margem_reel) < 1000
    univ_reel = reel['secoes_total']
    saldo = 2514969
    impacto = 858727
    suspeitos, urnas_anom = 5677789, 114095
    sem_bio = reel['sem_biometria_total']
    sem_bio_outro = reel['sem_biometria_total_outro_painel']
    MI_r, DG_r, com_bio_r = 5.78e6, 1.47e6, 110.9e6
    fat_bio, fat_MI, fat_DG, salto = 51.43, 51.36, 51.40, 15.6

    U = c1['universo']
    NH2, C2n = U['NH_2T'], U['comparecimento_2T']
    margem_27 = U['L2'] - U['R2']
    est = c1['P3_estimativa_nacional']

    # faixas do reel em proporção de urnas
    r_05 = reel['secoes_0_5'] / univ_reel * 100
    r_510 = (reel['secoes_ate_10'] - reel['secoes_0_5']) / univ_reel * 100
    r_10 = reel['secoes_mais_10'] / univ_reel * 100
    cal = c1['P4_placar_perfil']['def_NH_mais_S_hat_calibrado']
    bweb = c1['P1_placar_campo_bweb']
    p6 = c1['P6_exploratorio_pos_resultado']
    reg_cal = p6['a_regressao_faixas_reel_calibrado_pais']
    plc_cal = p6['a_placebo_faixas_reel_calibrado_pais']
    tab = c1['C1_tabela']
    reg = c1['C1_regressao']

    # órfãs
    tot2 = c2['totais']['2T_todas']
    man2 = tot2['votos_manuais']
    or2 = tot2['votos']['OR']
    og = c2['ordem_de_grandeza']
    sc2 = c2['score']['2']
    sc_zero = sc2['OR_maior_score']['0']
    sc_19 = sc2['OR_maior_score']['1-9']
    sc_1019 = sc2['OR_maior_score']['10-19']
    sc_20 = sc2['OR_maior_score']['20-49'] + sc2['OR_maior_score']['50+']
    sc_sem = sc2['OR_sem_linha_de_score']
    hora2 = {int(k): v for k, v in c2['orfas_por_hora']['2'].items()}
    hora1 = {int(k): v for k, v in c2['orfas_por_hora']['1'].items()}
    tarde2 = sum(v for k, v in hora2.items() if k >= 17)
    tarde1 = sum(v for k, v in hora1.items() if k >= 17)
    rob = c2['robustez']
    e3 = c2['exploratorio_depois_do_resultado']['E3_conta_ingenua']['2T']
    b, ep = c2['b'], c2['ep']
    mod = c2['por_modelo']

    # ---------- texto ----------
    w('C4 do Adendo 24 (tarefa PAINEL): o painel citado pelo reel @assis.salvioli (DfHTWubBajq), essencia-ai.com')
    w('Registro: PRE-REGISTRO-2026-10-26.md, Adendo 24 (commit ca110bb, 03/11/2026 04:24:10 UTC). O Adendo fixa C1 a C3; a')
    w('leitura do painel não tem critério registrado nem veredito de sinal. Script: scripts/analisar_C4_painel.py.')
    w('')
    w('RESULTADO: O PAINEL NÃO PÔDE SER LIDO SEM BAIXAR E RODAR CÓDIGO DO SITE.')
    w('  A página https://essencia-ai.com/auditoria-2026 (link "Auditoria 2026" no rodapé de essencia-ai.com) responde')
    w('  HTTP 200, sem login e sem 403. O HTML servido só tem cabeçalho, menu e rodapé: a rota é um componente de cliente')
    w(f'  do Next.js ("ClientPageRoot" no payload: {"sim" if tem_client_root else "não"}) e o conteúdo é montado no navegador')
    w(f'  pelo arquivo /_next/{chunk}.')
    w('  A regra da tarefa proíbe baixar ou rodar código do site; esse arquivo não foi baixado. Logo nenhuma das perguntas')
    w('  tem resposta com trecho do painel: fonte de dados, definições, método do +15,6 e dos 2,51 milhões ficam sem leitura.')
    w('  Abaixo, para cada pergunta: (i) painel; (ii) o que o próprio reel diz (degravação, trecho literal); (iii) o que a')
    w('  aritmética dos números do reel permite inferir (inferência nossa, não do painel); (iv) o que C1 e C2 já mediram.')
    w('')

    w('1. Tentativas (03/11/2026, depois do commit do Adendo; curl com user agent padrão, sem cookies; D1 a D3)')
    for url, arq, nota in TENTATIVAS:
        extra = ''
        if arq in pag:
            extra = f' [{n_(pag[arq]["bytes"])} bytes, sha256 {pag[arq]["sha256"][:16]}...]'
        w(f'  {url}: {nota}{extra}')
    w(f'  Data do servidor: home {datas.get("home_headers.txt")}; auditoria-2026 {datas.get("auditoria_headers.txt")}.')
    w(f'  Servidor da auditoria-2026: {"; ".join(datas.get("auditoria_headers.txt_srv", [])) or "n/d"} (a home traz')
    w(f'  {"; ".join(datas.get("home_headers.txt_srv", []))}).')
    w('  Termos da eleição no texto visível de cada página (urna, biometr, eleiç, TSE, Lula, Flávio, órfã, score):')
    for arq, t in termos_achados.items():
        w(f'    {arq}: {", ".join(t) if t else "nenhum"}')
    w('')

    w('2. O que o HTML da auditoria-2026 entrega (trechos)')
    w(f'  <title>: "{m_title.group(1) if m_title else "n/d"}"')
    w(f'  <meta name="description">: "{m_desc.group(1) if m_desc else "n/d"}"')
    w('  Payload do servidor (React Server Components): a:I[894,[],"ClientPageRoot"] e')
    w(f'  b:I[705,[..., "26","{chunk}"],"default"]; a página é {{"Component":"$b","searchParams":{{}},"params":{{}}}}.')
    w('  Ou seja, o servidor não manda nenhum dado do painel; tudo vem do arquivo da página (estático) ou de chamadas que ele')
    w('  faz no navegador. Qual dos dois, não dá para saber sem ler o código.')
    w(f'  Texto visível, inteiro ({len(vis_aud)} caracteres; travessão do original trocado por hífen): "{vis_aud}"')
    w('  Quem publica: "Essência Soluções em Inteligência Artificial, agência brasileira sediada no Rio de Janeiro" (rodapé).')
    w('  Nenhum autor, metodologia ou base para baixar no HTML de nenhuma página; o único contato é o geral, contato@essencia-ai.com.')
    w('')

    w('3. As perguntas, uma a uma')
    w('')
    w('3a. Qual a fonte de dados')
    w('  (i) Painel: não lido.')
    w('  (ii) Reel: "Abrimos a caixa-preta das 497 mil urnas do TSE com Inteligência Artificial"; "Nós auditamos com')
    w('  inteligência artificial as 497 mil urnas, lemos os logs segundo a segundo e cruzamos com 2022"; "Gravado no arquivo')
    w('  .jez de 51 mil urnas"; "Não é boato, é dado oficial". Telas: 497.897 urnas; 455.785 seções pareadas 2022/2026;')
    w('  99,71% de match exato log x boletim.')
    w(f'  (iii) Inferência: logs de urna (.logjez) e boletins do TSE de 2022 e 2026. 497.897 é exatamente o nosso universo')
    w(f'  de seções das 27 UFs no 2º turno, sem exterior (C1). Mas as faixas da cena 2 somam {n_(univ_reel)} urnas')
    w(f'  ({n_(U["secoes"] - univ_reel)} a menos) e a margem implícita é {n_(margem_reel)} ({n_(margem_27 - margem_reel)} a menos que')
    w(f'  os {n_(margem_27)} das 27 UFs): o painel usa pelo menos dois universos, e o reel não diz qual filtro dá {n_(univ_reel)}.')
    w(f'  O "sem agregação" do C1 dá {n_(c1["universos_candidatos"]["sem_agregacao_no_2T"])}, não {n_(univ_reel)}.')
    w(f'  (iv) Na amostra de 3.897 logs, votos no log = comparecimento do bweb em 3.897 de 3.897 seções no 2º turno (C2).')
    w(f'  Os 0,29% sem "match exato" do reel seriam cerca de {n_(U["secoes"] * 0.0029)} urnas; o reel não diz o que é match.')
    w('')

    w('3b. Como definem "sem biometria"')
    w('  (i) Painel: não lido.')
    w('  (ii) Reel: "Onde está a anomalia real? Nos 15,7 milhões de votos sem biometria habilitados na mesa" (cena 1);')
    w(f'  telas: {n_(sem_bio)} e, em outro painel, {n_(sem_bio_outro)} (o próprio reel difere em {n_(sem_bio - sem_bio_outro)});')
    w('  cena 2: "urnas com biometria degradada"; cena 4: "com biometria 110,9 milhões (51,43% Lula)".')
    w(f'  (iii) Inferência: 15,7 milhões não é o campo do bweb QT_ELEI_BIOM_SEM_HABILITACAO ({n_(NH2)} no 2º turno, C1).')
    w('  Bate com S + M: eleitor sem biometria cadastrada (S, habilitado pelo ano de nascimento, nunca passa pelo leitor)')
    w(f'  mais eleitor com biometria liberado sem ela (M). Nossa estimativa de NH + S: {n_(est["NH_mais_S_i"])} (razão por UF)')
    w(f'  a {n_(est["NH_mais_S_ii_nas_UFs_com_perfil"])} (perfil); {n_(sem_bio)} cai entre as duas. As faixas da cena 2, em')
    w(f'  proporção de urnas (0 a 5% {p_(r_05)}%, 5 a 10% {p_(r_510)}%, mais de 10% {p_(r_10)}%), reproduzem as do proxy')
    w(f'  NH + S calibrado ({p_(cal["0_a_5"]["pct_secoes"])}%, {p_(cal["5_a_10"]["pct_secoes"])}%, {p_(cal["mais_de_10"]["pct_secoes"])}%)'
      f' e não as do campo do bweb ({p_(bweb["0_a_5"]["pct_secoes"])}%, {p_(bweb["5_a_10"]["pct_secoes"])}%, {p_(bweb["mais_de_10"]["pct_secoes"])}%).')
    w(f'  Se for isso, "habilitados na mesa" está errado para cerca de {n_(sem_bio - NH2)} deles ({n_(sem_bio)} menos {n_(NH2)}):')
    w('  S é atributo do cadastro (o eleitor nunca coletou digital), não decisão do mesário, e se concentra por região e idade.')
    soma4 = com_bio_r + MI_r + DG_r + orfas_reel
    comp_reel = C2n * univ_reel / U['secoes']
    w(f'  Conta da cena 4: 110,9 + 5,78 + 1,47 + 1,28 = {p_(soma4 / 1e6)} milhões. Comparecimento das 27 UFs menos {n_(sem_bio)}')
    w(f'  = {n_(C2n - sem_bio)}, não 110,9 milhões. Duas leituras dão 110,9 e não se separam sem o painel: (a) universo de')
    w(f'  {n_(univ_reel)} urnas, comparecimento cerca de {n_(comp_reel)} (proporcional), menos {n_(sem_bio)} = {n_(comp_reel - sem_bio)};')
    w(f'  (b) {n_(C2n - sem_bio)} menos as {n_(orfas_reel)} órfãs = {n_(C2n - sem_bio - orfas_reel)} (órfãs tiradas duas vezes).')
    w('')

    w('3c. Como definem "digital órfã"')
    w('  (i) Painel: não lido.')
    w('  (ii) Reel: "Todo o salto na mesma cidade vem de 1 milhão e 280 mil liberações onde a digital usada não existia em')
    w('  nenhum arquivo da urna" (cena 4); "destrava a urna com digitais de score zero que não existiam em nenhum arquivo"')
    w('  (cena 5); tela de abertura: "1.280.132 digitais órfãs (score zero)".')
    w('  (iv) O log (C2, D2): na liberação manual a urna pede a digital do mesário, compara com cada mesário registrado')
    w('  ("Batimento de digitais retornou o score N") e termina numa de três mensagens. A órfã é "Capturada a digital do')
    w('  mesário" seguida de "Não encontrou digital coletada em nenhum dos arquivos, vai salvar a digital em novo arquivo."')
    w('  A digital não existia antes, mas a urna a grava; as liberações seguintes com o mesmo dedo saem como "Digital')
    w('  coletada bate com uma digital gravada após o registro inicial de mesário" (DG, o "mesário substituto" do reel).')
    w(f'  Contagem: amostra {n_(or2)} órfãs em {n_(man2)} liberações manuais ({p_(or2 / man2 * 100)}%), 3.897 seções; aplicada ao')
    w(f'  NH nacional, {n_(og["estimativa_por_manuais"])}; o reel diz {n_(orfas_reel)} ({p_((orfas_reel / og["estimativa_por_manuais"] - 1) * 100, 1)}%).')
    fr = og['reel']['fracoes_do_reel']
    fa = og['fracoes_da_amostra']
    w(f'  Repartição das manuais: reel MI {p_(fr["MI"] * 100, 1)}%, DG {p_(fr["DG"] * 100, 1)}%, OR {p_(fr["OR"] * 100, 1)}%; amostra'
      f' {p_(fa["MI"] * 100, 1)}%, {p_(fa["DG"] * 100, 1)}%, {p_(fa["OR"] * 100, 1)}%.')
    w('  Como contagem, o 1,28 milhão do reel é plausível; o que muda é o que ele quer dizer (3d e 3e).')
    w('')

    w('3d. Como definem "score zero"')
    w('  (i) Painel: não lido.')
    w('  (ii) Reel: "digitais de score zero" e "1.280.132 digitais órfãs (score zero)": trata toda órfã como score zero.')
    w(f'  (iv) Log (C2, seção 8), maior score de comparação em cada órfã do 2º turno: 0 em {n_(sc_zero)} ({p_(sc_zero / or2 * 100)}%),')
    w(f'  1 a 9 em {n_(sc_19)} ({p_(sc_19 / or2 * 100, 1)}%), 10 a 19 em {n_(sc_1019)} ({p_(sc_1019 / or2 * 100, 1)}%), 20 ou mais em {n_(sc_20)},')
    w(f'  sem linha de score em {n_(sc_sem)}; mediana {p_(sc2["OR_maior_score_mediana"], 0)}. Os batimentos aceitos têm score 20 ou mais')
    w(f'  em todos os casos (mediana DG {p_(sc2["DG_mediana"], 0)}, MI {p_(sc2["MI_mediana"], 0)}). Órfã é score abaixo do corte, não zero.')
    w(f'  Se "score zero" fosse literal, seriam cerca de {n_(sc_zero / or2 * orfas_reel)} no país ({n_(sc_zero)}/{n_(or2)} de {n_(orfas_reel)}).')
    w('')

    w('3e. Como calcularam os +15,6 pontos de Lula nos votos liberados por digital órfã')
    w('  (i) Painel: não lido. O reel não diz se é comparação entre seções ou regressão, nem quais controles.')
    w('  (ii) Reel: "E olha a prova definitiva dentro da mesma cidade, nas 5.570 cidades: quando a digital do eleitor falha')
    w('  mas o mesário oficial assina com o dedo, em 5,8 milhões de votos, o voto em Lula é 51,36%, idêntico à biometria.')
    w('  E se for um mesário substituto usando o mesmo dedo o dia todo? Testamos: desvio zero. Todo o salto na mesma cidade')
    w('  vem de 1 milhão e 280 mil liberações onde a digital usada não existia em nenhum arquivo da urna." Telas: com')
    w('  biometria 110,9 mi (51,43%); mesário oficial 5,78 mi (51,36%); substituto cerca de 1,47 mi (51,40%); órfãs 1,28 mi,')
    w('  "salto de +15,6 pp". Cena 3, prova 3: "+4,2 pp no mesmo prédio, +8,8 pp digitais órfãs".')
    w('  (iii) Inferência: o RDV não liga eleitor a voto; dar uma fatia de Lula a cada tipo de liberação só se faz comparando')
    w('  seções (inferência ecológica), por exemplo fatia da seção contra as frações de cada tipo, com efeito fixo de')
    w('  município ("dentro da mesma cidade, nas 5.570 cidades"). Nada no reel fala de controle pelo voto da mesma seção no')
    w('  1º turno. A mesma grandeza cai de +15,6 (cidade) para +8,8 (prédio): quanto mais fina a comparação, menor o efeito,')
    w('  que é o desenho de composição. "Desvio zero" do substituto e 51,36 contra 51,43 são diferenças de 0,07 ponto, o que')
    w('  pede um erro-padrão que o reel não mostra.')
    w(f'  (iv) C2 (amostra, 3.781 seções em 625 locais): especificação registrada (dentro do local, controle do 1º turno)')
    w(f'  b = {p_(b, 3)} (ep {p_(ep, 3)}), SEM SINAL; +0,156 fica a {p_((0.156 - b) / ep, 1)} ep. Dentro do município com controle:')
    d_ = rob['d_efeito_fixo_municipio']
    e_ = rob['e_efeito_fixo_municipio_sem_controle']
    w(f'  {p_(d_["coef"]["f_OR"], 3)} (ep {p_(d_["ep"]["f_OR"], 3)}). Dentro do município sem controle, a mais parecida com a frase do reel:')
    w(f'  {s_(e_["coef"]["f_OR"], 3)} (ep {p_(e_["ep"]["f_OR"], 3)}), que nesta amostra não exclui +0,156 ({p_((0.156 - e_["coef"]["f_OR"]) / e_["ep"]["f_OR"], 1)} ep).')
    w(f'  Conta ingênua (fatia ponderada pelos votos órfãos contra pelos biométricos): {p_(e3["fatia_ponderada_pelas_orfas"] * 100)}% contra')
    w(f'  {p_(e3["fatia_ponderada_pela_biometria"] * 100)}% = {s_(e3["diferenca"] * 100, 2)} pontos; dentro do município {s_(e3["diferenca_dentro_do_municipio"] * 100, 2)} ponto.')
    m2 = mod['2T_todas']
    txt_mod = '; '.join(f'{k} {p_(v["pct_OR_dos_votos"])}%' for k, v in m2.items())
    w(f'  Fração de órfãs nos votos por modelo de urna: {txt_mod}. A fração acompanha o equipamento e o local.')
    w('')

    w('3f. O que dizem dos 2,51 milhões "descontando estado e porte"')
    w('  (i) Painel: não lido.')
    w('  (ii) Reel: "São 858 mil votos de impacto na margem dentro da mesma cidade, 5,67 milhões de votos suspeitos em 114 mil')
    w('  urnas anômalas e um saldo líquido nacional, descontando estado e porte, de 2 milhões e 514 mil votos de vantagem')
    w('  para o 13 no bloco sem biometria." Tela: "+2.514.969 votos líquidos pró-13 (57,7% da margem nacional)".')
    w(f'  (iii) Aritmética: {n_(saldo)} / {n_(margem_reel)} = {p_(saldo / margem_reel * 100)}% (bate com 57,7%); / {n_(margem_27)} ='
      f' {p_(saldo / margem_27 * 100)}% (não bate).')
    w(f'  O denominador é a margem do universo de {n_(univ_reel)} urnas. {n_(saldo)} / {n_(sem_bio)} = {p_(saldo / sem_bio, 3)}: {p_(saldo / sem_bio * 100, 1)} pontos')
    w(f'  de margem por voto do bloco, ou fatia de Lula cerca de {p_(saldo / sem_bio * 50, 1)} pontos acima do esperado, se a conta for essa.')
    w('  "Descontando estado e porte" sugere ajuste por UF e tamanho da seção; o reel não fala de controle pelo 1º turno nem')
    w('  por município ou local.')
    w(f'  (iv) C1, campo do bweb: a faixa de mais de 10% já dava a Lula {n_(tab["C"]["margem_Lula_1T"])} no 1º turno, quando as outras')
    w(f'  duas davam a Flávio {n_(tab["A"]["margem_Lula_1T"] + tab["B"]["margem_Lula_1T"])}; dentro do local, a virada da faixa de mais de 10% foi')
    w(f'  {p_(-reg["coef"]["C"], 3)} ponto MENOR que a de 0 a 5% (ep {p_(reg["ep"]["C"], 3)}). Com a definição do reel (NH + S calibrado),')
    w(f'  dentro do local: virada C - A = {s_(reg_cal["coef"]["C"], 3)} (ep {p_(reg_cal["ep"]["C"], 3)}) e nível do 1º turno C - A ='
      f' {s_(plc_cal["coef"]["C"], 3)} (ep {p_(plc_cal["ep"]["C"], 3)}, z {p_(plc_cal["z"]["C"], 1)}),')
    w('  em pontos: dentro do mesmo local, as faixas diferem pouco no nível e nada na mudança; a distância do placar')
    w('  nacional vem de comparar locais diferentes. Ajustar só por UF e porte deixa de fora a geografia dentro da UF.')
    w(f'  Com a mesma definição, o placar do reel não se reproduz: faixa de mais de 10% com {p_(cal["mais_de_10"]["parte_da_margem_pct"])}% da margem')
    w(f'  ({n_(cal["mais_de_10"]["margem_Lula"])}), não 97,65% ({n_(reel["margem_mais_10_Lula"])}); faixa de 0 a 5% com Lula {p_(cal["0_a_5"]["fatia_Lula"])}%,')
    w('  não Flávio 52 x 48.')
    w(f'  858.727: {n_(impacto)} / {n_(orfas_reel)} = {p_(impacto / orfas_reel, 4)}, e 51,43% + 15,6 = {p_(fat_bio + salto)}%. Coincide com o total de')
    w('  votos de Lula estimado entre as órfãs, não com impacto na margem. O excesso de margem dessas órfãs sobre a biometria')
    w(f'  seria {n_(orfas_reel)} x 2 x 0,156 = {n_(orfas_reel * 2 * 0.156)}. Hipótese a conferir no painel.')
    w(f'  5.677.789 votos em 114.095 urnas: {p_(suspeitos / urnas_anom, 1)} votos por urna, {p_(urnas_anom / univ_reel * 100, 1)}% das {n_(univ_reel)} urnas;')
    w('  o reel não define "anômala".')
    w('')

    w('4. Contagem contra conclusão')
    w(f'  Se sustentam como contagem: 1,28 milhão de órfãs (projeção da amostra {n_(og["estimativa_por_manuais"])}); repartição MI, DG, OR;')
    w(f'  15,7 milhões como S + M ({n_(est["NH_mais_S_i"])} a {n_(est["NH_mais_S_ii_nas_UFs_com_perfil"])}); 497.897 seções.')
    w(f'  Rótulos errados: "score zero" ({n_(sc_zero)} de {n_(or2)} na amostra); "habilitados na mesa" para os 15,7 milhões (cerca de')
    w('  7,1 milhões são eleitores sem biometria cadastrada); "não existia em nenhum arquivo" (a urna cria o arquivo na hora).')
    w(f'  Conclusões sem apoio: +15,6 (b = {p_(b, 3)}, ep {p_(ep, 3)}, na especificação registrada); 97,65% da margem (composição; com')
    w(f'  a definição do reel, {p_(cal["mais_de_10"]["parte_da_margem_pct"])}%); 2,51 milhões (sem controle do 1º turno).')
    w(f'  Cena 5 (liberações depois das 17h): das {n_(or2)} órfãs do 2º turno na amostra, {n_(tarde2)} às 17h ou depois; no 1º turno,')
    w(f'  {n_(tarde1)}. O pico é às 8h ({n_(hora2.get(8, 0))} no 2º turno, {p_(hora2.get(8, 0) / or2 * 100, 1)}%), na abertura.')
    w('')

    ep_e = e_['ep']['f_OR']
    ep_sec = ep_e / (497897 / 3897) ** 0.5
    ep_mun = ep_e / (5570 / e_['grupos']) ** 0.5
    w('5. Pistas (o que merece investigação, com números)')
    w('  P1. Ler o painel: alguém abre https://essencia-ai.com/auditoria-2026 num navegador comum e salva texto e capturas, ou')
    w(f'      a coordenação autoriza ler /_next/{chunk} como texto, sem rodar (a rota é')
    w('      pré-renderizada, x-nextjs-prerender: 1; o conteúdo pode estar todo nesse arquivo ou vir de chamadas dele).')
    w(f'  P2. Universo de {n_(univ_reel)} urnas e margem {n_(margem_reel)}: {n_(U["secoes"] - univ_reel)} urnas e {n_(margem_27 - margem_reel)} votos de margem a menos')
    w(f'      que as 27 UFs; o filtro não é "sem agregação" ({n_(c1["universos_candidatos"]["sem_agregacao_no_2T"])}).')
    w(f'  P3. {n_(impacto)} = {p_(impacto / orfas_reel, 4)} x {n_(orfas_reel)}, que é 51,43% + 15,6 pontos: se confirmado, o "impacto na margem"')
    w(f'      é o total de votos de Lula estimado entre as órfãs; o excesso seria cerca de {n_(orfas_reel * 2 * 0.156)}, e só se o +15,6 valesse.')
    w(f'  P4. Gradiente: +15,6 (cidade), +8,8 (prédio), {p_(b * 100, 1)} (local com controle do 1º turno, C2). Pedir o método da prova 3')
    w(f'      ("+4,2 pp no mesmo prédio") e comparar com a nossa diferença de nível dentro do local, {s_(plc_cal["coef"]["C"], 3)} ponto no 1º turno.')
    w(f'  P5. A especificação mais parecida com a do reel (município, sem 1º turno) dá {s_(e_["coef"]["f_OR"], 3)} (ep {p_(ep_e, 3)}) e não exclui +0,156.')
    w(f'      Com todos os logs o erro cairia para algo entre {p_(ep_sec, 3)} e {p_(ep_mun, 3)} (conta grosseira pela raiz do número de seções ou')
    w('      de municípios). Mesmo replicado, seria nível sem controle do 1º turno; a especificação registrada já deu SEM SINAL.')
    w(f'  P6. Score zero: {n_(sc_zero)} de {n_(or2)} órfãs (0,12%). Ver se o painel chama de "score zero" outra coisa (por exemplo o score de')
    w('      uma das comparações, não o maior; ou a ausência de linha de score, 76 casos).')
    w(f'  P7. Órfãs depois das 17h: {n_(tarde2)} no 2º turno e {n_(tarde1)} no 1º, na amostra. A cena 5 junta "sala vazia pós-17h" (1.635 seções)')
    w('      com órfãs: cruzar, nessas seções, se há órfã depois da resposta "SIM" (o C3 faz isso em Xique-Xique e Coronel José Dias).')
    w(f'  P8. {n_(sem_bio)} contra {n_(sem_bio_outro)} nas telas do próprio reel: digitação ou duas versões da base.')
    w('  P9. 99,71% de match log x boletim (cerca de 1.444 urnas fora); na amostra, 3.897 de 3.897, inclusive as 13 seções com')
    w('      contingência quando o log aninhado é lido. Perguntar o que o painel chama de match.')
    w(f'  P10. 2,51 milhões = {p_(saldo / sem_bio * 100, 1)} pontos de margem por voto do bloco. Refazer "descontando estado e porte" no bweb com S + M')
    w(f'      estimado, com e sem controle do 1º turno; o C1 já dá virada C - A = {s_(reg_cal["coef"]["C"], 3)} (ep {p_(reg_cal["ep"]["C"], 3)}) dentro do local.')
    w('')

    w('6. Desvios declarados (D1 a D8 no docstring, escritos antes de calcular)')
    w('  Escopo: a tarefa PAINEL não está no Adendo 24; é descritiva e não muda nenhum veredito de C1 a C3.')
    w('  D1: só HTML; o arquivo da página e todos os .js, .css e fontes do site ficaram de fora (regra da tarefa).')
    w('  D2: sem contorno; archive.ph (429) e Instagram (login) pararam onde bloquearam.')
    w('  D4: trechos do reel vêm da degravação (legendas), não de áudio; inferências marcadas como "Inferência".')
    w('  D6: margem do reel 4.357.147 e universo 492.988 (implícitos, C1); D7: projeção sem peso; D8: score zero literal.')
    w('  WebFetch foi usado como segundo leitor da página (não executa JavaScript; só confirmou o vazio).')
    w('')
    w('7. Arquivos')
    w(f'  Downloads: {DL}/ (HTML, cabeçalhos, resposta do Wayback e do archive.ph).')
    w('  Extrator de texto usado à mão: /home/user/trabalho-eleicao/adendo24/C4_scripts/texto_html.py.')
    w('  Resultados lidos: resultados/C1_nivel_mudanca_biometria.json, resultados/C2_digitais_orfas.json.')
    w('  Degravação: /root/.claude/uploads/ce2a8c88-e5ad-504f-8950-6f5ee14ae721/a50a6d9b-degravacao_DfHTWubBajq.md.')

    txt = '\n'.join(linhas) + '\n'
    for ch in ('\u2014', '\u2013'):
        assert ch not in txt, 'travessão no texto'
    with open(SAIDA, 'w', encoding='utf-8') as f:
        f.write(txt)
    print(txt)


if __name__ == '__main__':
    sys.exit(main())
