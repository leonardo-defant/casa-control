# Eleição presidencial 2026, 2º turno: robô do TSE, projeção e auditoria

Documento de passagem de contexto para uma sessão no Claude Code. Reúne tudo o que foi feito na conversa de 25/10/2026 (das 19h12 às 22h20, horário de Cuiabá): o robô de apuração, o painel, o modelo de projeção, as análises de auditoria, os fatos checados com fontes, as hipóteses discutidas, os critérios definidos antes dos dados e as pendências.

Horários: quando não indicado, horário de Cuiabá (UTC-4). Os arquivos do TSE usam horário de Brasília (UTC-3).

---

## 0. Como usar este documento

1. Leia as seções 1 a 3 para entender o que existe e como os dados do TSE funcionam.
2. As seções 5 e 6 trazem cada hipótese testada e os números de cada teste.
3. A seção 7 tem os critérios definidos antes dos dados. Não mude esses critérios depois de ver os resultados.
4. A seção 8 lista o que está pendente. A tarefa principal é rodar `auditoria/rodar_2026.sh` quando o TSE publicar os boletins de urna do 2º turno.

**Para começar a sessão:** o pacote veio em 3 partes de até 30 MB (`eleicao-2026-parte1.zip`, `eleicao-2026-parte2-secoes2022.zip`, `eleicao-2026-parte3-secoes2018.zip`). Descompacte as três no mesmo lugar: todas criam a mesma pasta `eleicao-2026`. A parte 1 tem o código, este documento, os dados menores e os boletins do 1º turno de 2026; as partes 2 e 3 trazem os boletins de 2022 e 2018 já extraídos, que ficam em `eleicao-2026/auditoria/`. Abra o Claude Code dentro da pasta `eleicao-2026` e mande, por exemplo:

> Leia CONTEXTO-ELEICAO-2026.md inteiro, com atenção à seção 0.1 (o que queremos sobre fraude). Depois rode auditoria/rodar_2026.sh e me diga se os boletins de urna do 2º turno já saíram. Se saíram, aplique os critérios da seção 7 e me mostre os resultados sem suavizar para nenhum lado. Se não saíram, avance nos testes da seção 0.1 que não dependem deles.

**Preferências do usuário (Léo) para esta sessão:**
- Nunca usar travessões nos textos.
- Atuar como parceiro de debate rigoroso: testar premissas, apresentar contrapontos, apontar viés de confirmação e premissas não verificadas, priorizar a verdade sobre a concordância.
- Ele pediu uma "caçadora cética da verdade". Combinado: ceticismo nos dois sentidos, inclusive sobre a hipótese de fraude. Critérios definidos antes de ver os dados e resultados relatados sem suavizar para nenhum lado.
- Ele acredita que a eleição foi fraudada e propôs teses específicas (seção 5). Testar cada uma de verdade, reconhecer quando ele tem um ponto e mostrar com dados quando a tese falha.

### 0.1 O que queremos sobre fraude (ler antes de tudo)

**Objetivo.** Investigar a fundo se houve fraude no 2º turno de 2026, com prioridade para a tese do Léo de que votos em branco e nulos para presidente foram registrados pela urna como votos para Lula. Procurar ativamente as incoerências que uma fraude desse tipo deixaria, testar cada uma com dados públicos e critério definido antes de ver o resultado, e relatar o que sair: se aparecer evidência, dizer com clareza; se não aparecer, dizer também, junto com o que continua sem teste.

**A posição do Léo, nas palavras dele** (trechos das mensagens, com ajustes mínimos de digitação):
- "Essa sessão de agora em diante será uma caçadora cética da verdade!"
- "Precisamos buscar incoerências fortes e coisas pouco prováveis que expliquem a virada de Lula como fraude!"
- "Eu tenho uma teoria, eleição é fraudada, e o que me leva a crer é que Barroso exerceu sua força pra barrar o voto impresso! O que eu acho é que de alguma forma eles alteram os votos brancos e nulos, por isso o roubo deles é limitado e eles não conseguem roubar sempre, nem vencer eleições regionais, deputados e senadores."
- "Minha tese sobre os brancos e nulos é sobre um valor não sabido, e não sobre a comparação do primeiro com o segundo turno. Afinal, a gente não tem a fotografia real, só a visão da urna."
- "Se alguém fosse roubar, não ia fazer isso de forma perceptível."
- "Como pode acontecer um erro generalizado das instituições de pesquisa, juntamente com a situação do Barroso, do Zanin e com os relatos de fraudes da Venezuela? Somando aos fatos inéditos de brancos, nulos e abstenções."
- "Teste a minha tese, mas faça a análise cética também."

**A tese, formulada para teste.** O software da urna registraria parte dos votos em branco e nulos para presidente como voto no 13. O branco/nulo verdadeiro seria desconhecido, porque o único registro é o da própria urna. O ganho fica limitado ao bolo de branco e nulo, o que explicaria um "roubo limitado". Ordem de grandeza: para inverter o resultado, a conversão teria de passar de 4,43 milhões de votos, mais que todo o branco e nulo registrado no 2º turno (4,15 milhões). Mesmo que toda a queda do branco/nulo entre turnos (1,82 milhão) tivesse virado voto de Lula, o vencedor não mudaria; para mudar, a tese precisa do "valor desconhecido".

Ponto metodológico em que o Léo tem razão: uma conversão presente nos dois turnos não aparece em nenhuma comparação entre o 1º e o 2º turno. Esses testes só alcançam a parte da conversão que mudou de um turno para o outro.

**O que essa fraude deixaria, e o que não deixaria:**

| Teste | Pega a conversão? | Situação |
|---|---|---|
| Soma dos boletins x total oficial | Não. A urna já imprimiria o boletim convertido; isso só pega fraude na totalização | 1º turno bateu; 2º turno pendente |
| Registro digital do voto x boletim | Não. Os dois saem do mesmo software | Pendente (precisa da especificação EA18) |
| Modelo de urna no mesmo prédio | Só se a fraude estiver em um modelo ou lote de hardware. Não pega software igual em todas | 2022 e 1º turno de 2026 sem sinal; virada do 2º turno pendente |
| Presidente x governador na mesma urna (AC, AM, DF, ES, RN, TO) | Sim, se a conversão for só para presidente | Por estado: inconclusivo (seção 6.8). Por seção: pendente, com critério na seção 7 |
| Virada de Lula x branco/nulo do 1º turno da própria seção, dentro do mesmo local, em 2018, 2022 e 2026 (`analisar_bn_secao.py`) | Indiretamente: com conversão nova em 2026, proporcional ao branco/nulo, seções com mais branco/nulo teriam virada maior só em 2026 | Referências de 2018 e 2022 prontas (seção 6.10); 2026 pendente, com critério na seção 7 |
| Excesso de seções com branco/nulo de presidente zerado ou quase zerado | Sim, se a conversão for total em parte das urnas | Não feito |
| Branco/nulo declarado nas pesquisas finais x registrado | Indiretamente: é a principal medida independente do "valor desconhecido" | Não feito. Comparar com a mesma diferença em 2018 e 2022, nas mesmas pesquisas |
| Teste de integridade com cédulas conhecidas | Sim, se as cédulas tiverem branco e nulo para presidente e o software não perceber o teste (a versão com biometria existe para isso) | Relatório do 2º turno pendente; composição das cédulas não confirmada |
| Logs da urna | Talvez. Depende do que o log registra sem quebrar o sigilo do voto | Não feito; verificar na especificação |

**Pista aberta mais forte a favor da tese.** Na regressão por município, o branco/nulo do 1º turno "explica" muito mais a virada em 2026 do que em 2018 e 2022 (dentro das UFs, para o candidato de esquerda: 14%, 14% e 67%; para o da direita: 16%, 38% e 3%; UFs acima de 70% para a esquerda: 2, 4 e 10 de 24; seção 6.2). A leitura até aqui foi de artefato de regressão com dados agregados (outra especificação dá 118%, o que é impossível), mas a diferença entre os anos é real e não está explicada. O teste por seção dentro do mesmo local de votação (`analisar_bn_secao.py`) é o que separa as duas explicações.

**Como conduzir:**
- Não partir da conclusão em nenhum sentido. O Léo acredita em fraude e pediu teste sério com análise cética: nem confirmar por simpatia, nem descartar por princípio.
- Para cada indício, perguntar quanto mais provável ele é com fraude do que sem fraude. Um fato igualmente provável nos dois cenários (por exemplo, a posição de Barroso contra o voto impresso em 2021) não soma nada, por mais suspeito que pareça. A soma de coincidências só pesa com itens independentes e bem mais prováveis com fraude.
- Levar a sério o argumento de que uma fraude bem-feita não seria perceptível, mas apontar quando ele torna a tese impossível de testar. Sempre dizer qual observação mudaria a conclusão.
- Separar fato confirmado, indício, evidência e prova.
- Reconhecer os pontos válidos, já reconhecidos na conversa: o erro das pesquisas foi real e grande; a prorrogação nacional por decisão individual é contestável; a falta de comprovante conferido pelo eleitor é uma fraqueza real de auditabilidade; a anomalia do branco/nulo segue aberta.
- Corrigir os próprios erros na hora. Exemplo: o teste por estado presidente x governador estava registrado como "falhou"; revisando, um sinal estava lido ao contrário e o resultado é inconclusivo (seção 6.8).
- Entregar cada resultado com: o que foi testado, o critério definido antes, o número, se apoia ou contraria a tese e o que fica sem teste.

---

## 1. Resultado final oficial

Fonte: arquivo nacional do TSE (`br-c0001-e006258-u.json`, cópia em `auditoria/oficial2026_2t.json`), gerado em 25/10/2026 às 23h09 de Brasília, com 99,99% das seções (499.247 de 499.248). Falta 1 seção, então os totais ainda podem variar em algumas centenas de votos.

| | 2º turno | 1º turno |
|---|---|---|
| Lula (13) | 64.255.969 votos, 51,79% | 53.879.538 votos, 45,16% |
| Flávio Bolsonaro (22) | 59.826.002 votos, 48,21% | 56.104.503 votos, 47,03% |
| Diferença | 4.429.967 a favor de Lula | 2.224.965 a favor de Flávio |
| Votos válidos | 124.081.971 | 119.300.788 |
| Brancos | 1.430.493 (1,12% do comparecimento) | 2.300.798 (1,84%) |
| Nulos | 2.723.298 (2,12%) | 3.674.249 (2,93%) |
| Comparecimento | 128.235.762 (80,78%) | 125.275.835 (78,92%) |
| Abstenção | 30.508.978 (19,22%) | 33.469.244 (21,08%) |
| Eleitorado | 158.745.502 | 158.745.502 |

De onde vieram os 14,1 milhões de votos a mais somados pelos dois (Lula +10,38 mi, Flávio +3,72 mi): 9,32 mi dos candidatos eliminados, 2,96 mi de comparecimento maior e 1,82 mi de branco e nulo a menos. A conta fecha exatamente.

Até a geração deste documento o TSE ainda não tinha marcado o candidato como eleito no arquivo (campo `e` = "n"). O robô marcou "matematicamente eleito" quando a vantagem passou a superar todo o eleitorado ainda não apurado.

---

## 2. O que foi construído

### 2.1 Robô de apuração e projeção (`robo-tse/robo-tse.js`)

- Node 18 ou superior, sem dependências. Rodar com `node robo-tse.js` dentro da pasta `robo-tse`. Painel em `http://localhost:8787`.
- Opções: `--intervalo 60`, `--porta 8787`, `--conc 6` (requisições simultâneas), `--sims 2000`, `--max-mun 1500`, `--uma-vez`.
- Gera `estado.json` (última leitura completa, lida pelo painel) e `historico.csv` (uma linha por atualização).
- Precisa de `baseline-1t.json.gz` na mesma pasta: 1º turno por seção (499.206 seções), gerado de `votacao_secao_2026_BR.zip` dos dados abertos (script `analises/tse/build_baseline.py`; uso: `python3 build_baseline.py votacao_secao_2026_BR.zip baseline-1t.json.gz`). Formato: `uf -> municipio -> zona -> secao -> [Lula, Flávio, outros válidos, branco+nulo]`.

**Ciclo de captura (a cada 60 s):**
1. Resultado nacional e das 27 UFs mais exterior (`-u.json`).
2. Arquivo de acompanhamento por UF (`-ab.json`): seções totalizadas, eleitorado apurado e não apurado e comparecimento por município. Mudanças disparam as próximas etapas.
3. Lista de seções por UF (`-cs.json`): quais seções já têm boletim publicado.
4. Resultado de cada município que mudou (`{uf}{mun}-c0001-...-u.json`), com prioridade para os parcialmente apurados.
5. Projeção, simulação, gravação e impressão.

**Modelo de projeção (versão final, validada):**
1. Para cada município, soma o 1º turno só das seções que já entraram no 2º turno e compara com o 2º turno delas (as mesmas seções nos dois turnos).
2. A lista de seções do TSE anda atrás dos votos totalizados (seção 3.4). As seções já contadas mas ainda fora da lista são estimadas pela média das seções não listadas daquele município, e o volume restante é reduzido na mesma proporção (`fracRem`).
3. Regressão ecológica linear (matriz de transferência tipo Goodman), com efeito fixo por UF e pesos pelos votos válidos: `fatia 2T de Lula = a_UF + bL*l + bO*o + bZ*z`, onde `l` é a fatia de Lula no 1º turno, `o` a fatia dos demais candidatos (o voto que migra) e `z` o log do eleitorado do município. Linear em fatias, então somar seção por seção não distorce o total.
4. Cada seção ainda não apurada recebe a fatia prevista a partir do seu próprio 1º turno, mais o desvio do município (encolhido por `n/(n+1500)` votos apurados).
5. Volume de votos restante: seção por seção, pelo total de votos do 1º turno vezes a razão observada (válidos 2T / votos 1T nas seções comparadas, encolhida para a UF), multiplicado por `fracRem`. Sem seções mapeadas, usa eleitorado não totalizado vezes válidos por eleitor.
6. Monte Carlo com 2.000 simulações: erro do município, erro da UF (inflado por baixa cobertura) e choque nacional `TAU = 0,0025 + 0,015 * fração não apurada`. Gera intervalo de 95% e chance de vitória.
7. Veredito: "oficial" (TSE declara eleito), "matematicamente eleito" (vantagem maior que todo o eleitorado não apurado), "veredito" (chance de 99% ou mais), "tendência" (90% a 99%), "indefinido" (abaixo de 90%).

**Validação (backtest, `analises/teste.js` com o retrato das 19h30):** esconder municípios já 100% apurados e prever o resultado deles. Fatia de Lula prevista contra a real no grupo escondido, com a versão final do robô: aleatório 30% (611 municípios): 49,38% contra 49,36%; cidades pequenas (1.998): 51,92% contra 51,79%; Nordeste inteiro (545): 72,65% contra 72,33%; Sul inteiro (617): 35,62% contra 35,69%. Volume de votos previsto dentro de 0,7% em todos. Limite: quase nenhuma cidade grande estava completa na hora do teste (só 2 acima de 100 mil eleitores). Bug menor conhecido: o erro municipal RMS sai `NaN` em dois dos testes; não afeta os totais.

**Erros encontrados e corrigidos durante a noite (registrar para não repetir):**
1. Modelo em logit com pesos limitados (`min(votos, 20000)`) superestimava Lula em cerca de 0,5 ponto nas capitais. Corrigido com modelo linear e pesos pelos votos totais.
2. Volume restante pelo comparecimento médio da UF dava peso demais a municípios de comparecimento baixo. Corrigido com volume seção por seção.
3. **Dupla contagem:** seções contadas nos votos mas ainda fora da lista do TSE entravam também como restantes. Às 20h56 de Brasília o robô estimava 27,5 milhões de votos restantes contra 21,0 milhões numa conta independente (excesso de 30,6%). Corrigido com `fracRem` e ajuste das seções comparadas. Depois da correção, diferença de 0,9%.
4. Tentativa errada de alinhar a lista de seções pelo horário: o campo `ha` é o horário de publicação do boletim, não da totalização. Desfeito.
5. O backtest inicial também tinha um artefato: escondia o município mas deixava as seções marcadas como totalizadas na lista. Corrigido no teste.
6. Um monitor de log com `awk` no pipeline ficou com saída em buffer e o painel passou cerca de 30 minutos sem atualizar. Usar só `grep --line-buffered`.

**Evolução da projeção durante a noite:**

| Hora TSE (Brasília) | Seções | Apurado Lula | Projeção Lula | Observação |
|---|---|---|---|---|
| 20h23 | 46,0% | 49,97% | 51,5% | versão inicial em logit |
| 20h36 | 60,9% | 50,55% | 51,8% (50,9 a 52,6) | com o erro de dupla contagem |
| 20h56 | 84,2% | 51,40% | 51,8% (51,6 a 52,0) | depois da correção |
| 21h01 | 89,7% | 51,5% | 51,8% | previsão em votos: Lula 64,2 mi, Flávio 59,8 mi |
| 22h46 | 99,99% | 51,79% | 51,79% | final: Lula 64,26 mi, Flávio 59,83 mi |

O histórico completo está em `robo-tse/historico-2026-10-25.csv` e o log da noite em `robo-tse/robo-2026-10-25.log`.

### 2.2 Painel publicado

- Artefato do claude.ai, compartilhado por link: https://claude.ai/artifact/Fs49Hd7V8rTz2WRqhziNmy
- Fonte: `robo-tse/painel.html`. Lê `estado.json` publicado junto. O artefato não consegue buscar o TSE sozinho (a política de segurança bloqueia acesso externo), então só muda quando o painel é republicado com um `estado.json` novo.
- Mostra: veredito, os dois candidatos (projeção, intervalo, chance, apurado), barra de projeção, comparação seção a seção, quadro de abstenção nas mesmas seções (por inclinação e porte do município), gráfico de evolução e tabela por UF.
- Última versão publicada com a leitura final do robô (22h46 de Brasília, 99,99% das seções). O mesmo estado está em `robo-tse/estado-final.json`.

### 2.3 Auditoria por boletim de urna (`auditoria/`)

| Arquivo | O que faz |
|---|---|
| `extrair_bu.py` | Lê os zips `bweb_*` (boletins de urna dos dados abertos), filtra Presidente e Governador e grava por seção e turno: local de votação, número de série da urna, tipo, aptos, comparecimento, votos (13, 22, outros, branco, nulo), abertura, encerramento e branco/nulo de governador. Uso: `python3 extrair_bu.py <pasta_zips> <saida.json.gz>` |
| `faixas.json` | Faixas de número de série por modelo de urna (2022 e 2026), inferidas dos agrupamentos nos próprios dados |
| `analisar_modelos.py` | Teste por modelo de urna: comparação bruta e dentro do mesmo local de votação (efeito fixo do local, erro-padrão agrupado), para fatia de Lula, virada entre turnos, branco+nulo e comparecimento |
| `analisar_1turno.py` | Mesmo teste com um turno só (níveis) |
| `analisar_gov.py` | Teste da tese do branco/nulo: presidente contra governador na mesma urna, seção por seção |
| `analisar_bn_secao.py` | Pista do branco/nulo por seção: virada do 13 contra o branco/nulo do 1º turno da própria seção, dentro do mesmo local, com controles. Uso: `python3 analisar_bn_secao.py <secoes.json.gz> <ano>` |
| `preparar_2018.sh` | Baixa e extrai os boletins de 2018 (referência para o teste acima); gera `secoes2018.json.gz` |
| `secoes2018.json.gz` | 2018 extraído (dois turnos, com governador; Haddad no campo `L`, Bolsonaro no campo `R`) |
| `gov_vs_pres.py` | Presidente contra governador por estado, 2022 e 2026 (consulta o TSE e usa `analises/d2022/detalhe_votacao_munzona_2022.zip`) |
| `uf_swing.py` | Virada de Lula e variação do branco/nulo por estado (consulta o TSE) |
| `oficial2026_1t.json`, `oficial2026_2t.json` | Cópias dos arquivos nacionais oficiais do TSE (1º turno final; 2º turno das 23h09) |
| `rodar_2026.sh` | Rotina completa: consulta a API, baixa os boletins de 2026 (1º e 2º turnos), extrai, roda todos os testes e compara a soma dos boletins com o total oficial. Código 2 = ainda não publicado |
| `secoes2022.json.gz` | 2022 extraído (472.028 seções, dois turnos, com governador) |
| `secoes2026_1t.json.gz` | 1º turno de 2026 extraído (499.206 seções). Atenção: extraído antes de incluir governador; a rotina refaz a extração completa |
| `resultado2022.json` | Resultado do teste por modelo de urna em 2022 |

Dependências: Python 3.10 ou superior com `numpy` e `scipy`; `curl`, `unzip`, `grep`. Espaço: cerca de 6 GB para os zips de 2026 e 6 GB para os de 2022.

---

## 3. Fontes de dados e endpoints

### 3.1 Resultados ao vivo (`https://resultados.tse.jus.br/oficial/ele2026`)

| Código | O que é |
|---|---|
| Eleição 6257 | Federal, 1º turno (04/10/2026) |
| Eleição 6258 | Federal, 2º turno (25/10/2026) |
| Eleição 6259 / 6260 | Estadual, 1º / 2º turno (governador no 2º turno: AM, RN, DF, ES, AC e TO) |
| Pleito 3220 / 3221 | Arquivos de seção e boletins do 1º / 2º turno |
| Cargo c0001 / c0003 | Presidente / Governador |

- Resultado unificado: `/{ele}/dados/{uf}/{uf}-c0001-e{ele6}-u.json`, por exemplo `/6258/dados/br/br-c0001-e006258-u.json`. A pasta `dados-simplificados` não existe mais em 2026 (responde 404).
- Por município: `/{ele}/dados/{uf}/{uf}{mun5}-c0001-e{ele6}-u.json`.
- Acompanhamento por município: `/{ele}/dados/{uf}/{uf}-e{ele6}-ab.json`.
- Configuração de municípios: `/{ele}/config/mun-e{ele6}-cm.json`.
- Lista de seções: `/arquivo-urna/{pleito}/config/{uf}/{uf}-p{pleito6}-cs.json`. Campos por seção: `ns` (número), `da`/`ha` (data e hora em que o arquivo de urna da seção foi publicado), `nsp` (seção agregada, aponta para a principal; não tem urna própria), `nsa` (lista de agregadas da principal).
- Arquivo auxiliar por seção: `/arquivo-urna/{pleito}/dados/{uf}/{mun}/{zona}/{secao}/p00{pleito}-{uf}-m{mun}-z{zona}-s{secao}-aux.json`. Lista os arquivos `-bu.dat`, `-imgbu.dat`, `-rdv.dat`, `-log.jez`, `-vota.vsc` com um hash. O caminho de download desses arquivos não foi descoberto (precisa da especificação EA18 / instruções de download do TSE). O TSE avisa que muitas requisições a caminhos inexistentes podem bloquear o IP: não chutar caminhos.
- Configuração de eleições: `https://resultados.tse.jus.br/oficial/comum/config/ele-c.json`.
- Campos do `-u.json`: candidatos em `carg[].agr[].par[].cand[]` (`n`, `nmu`, `vap`, `pvap`, `e`, `st`); seções em `s` (`ts`, `st`, `pst`, `pstn`); eleitorado em `e` (`te`, `est`, `esnt`, `c`, `a`, `pa`); votos em `v` (`vv`, `vb`, `tvn`). Números vêm como texto com vírgula decimal.
- CORS: o host devolve `Access-Control-Allow-Origin` com a origem do pedido, então uma página web comum consegue ler os JSON direto do navegador (artefatos do claude.ai não, por bloqueio próprio).

### 3.2 Dados abertos (`dadosabertos.tse.jus.br` e `cdn.tse.jus.br`)

- API CKAN: `https://dadosabertos.tse.jus.br/api/3/action/package_show?id=resultados-2026-boletim-de-urna` (mesmo padrão para `resultados-2022-boletim-de-urna`).
- Boletins de urna 2026, 1º turno: `https://cdn.tse.jus.br/estatistica/sead/eleicoes/eleicoes2026/buweb/bweb_1t_{UF}_051020261403.zip` (28 arquivos, cerca de 5 GB; o CSV de SP tem 8,3 GB descompactado). O 2º turno ainda não estava publicado às 22h de 25/10.
- Boletins de urna 2022: `.../eleicoes2022/buweb/bweb_1t_{UF}_051020221321.zip` e `bweb_2t_{UF}_311020221535.zip`. Os de 2022 do 2º turno saíram no dia seguinte à eleição.
- Votação por seção, Presidente: `https://cdn.tse.jus.br/estatistica/sead/odsele/votacao_secao/votacao_secao_2026_BR.zip` (1º turno; atualizado ao fim de cada turno).
- Por município e zona: `https://cdn.tse.jus.br/estatistica/sead/odsele/detalhe_votacao_munzona/detalhe_votacao_munzona_{ano}.zip` e `https://cdn.tse.jus.br/estatistica/sead/odsele/votacao_candidato_munzona/votacao_candidato_munzona_{ano}.zip`. Os arquivos `_BR.csv` dentro deles trazem Presidente. Usados para 2018 e 2022. Os de candidato são grandes (395 MB em 2018, 643 MB em 2022) e não estão no pacote; os resultados já processados estão (`analises/d2018/mun2018.json`, `analises/d2022/mun2022.json`).
- Colunas do boletim (`bweb`): `SG_UF, CD_MUNICIPIO, NR_ZONA, NR_SECAO, NR_LOCAL_VOTACAO, CD_CARGO_PERGUNTA, QT_APTOS, QT_COMPARECIMENTO, DS_TIPO_URNA, CD_TIPO_VOTAVEL (2 branco, 3 nulo), NR_VOTAVEL, QT_VOTOS, NR_URNA_EFETIVADA, DT_ABERTURA, DT_ENCERRAMENTO`, entre outras.

### 3.3 Faixas de número de série por modelo de urna (inferidas)

- 2022: UE2009 999.000 a 1.220.500; UE2010 1.220.501 a 1.345.500; UE2011 1.345.501 a 1.649.999; UE2013 1.650.000 a 1.749.999; UE2015 1.750.000 a 1.999.999; UE2020 2.000.000 a 2.299.999.
- 2026: UE2013 1.650.000 a 1.749.999; UE2015 1.750.000 a 1.999.999; UE2020 2.000.000 a 2.249.999; UE2022 2.250.000 a 2.599.999.
- Quantidades usadas em 2026 (TSE/O Povo): UE2022 217.145; UE2020 222.323; UE2015 95.065; UE2013 29.377.

### 3.4 Pegadinhas

- O CDN do TSE às vezes devolve uma página HTML de bloqueio para rajadas vindas de IP de datacenter. Tentar de novo com espera e usar concorrência 4.
- A lista de seções (`-cs.json`) anda atrás dos votos: em metade dos municípios parciais testados em MG e BA, os votos já incluíam seções que a lista ainda não marcava (um caso: 45 seções nos votos contra 10 na lista). Nunca tratar seção fora da lista como "não apurada" sem ajuste.
- Em 2026 os campos numéricos dos CSV de boletim vêm sem aspas; em 2022, com aspas. Ler sempre pelo cabeçalho.
- 2018 tem diferenças: os zips começam com `BWEB_` (maiúsculas), a coluna de UF vem como `SG_ UF` (com espaço), `DS_TIPO_URNA` traz "Apurada" em vez do modelo e o candidato da direita no 2º turno era o 17. `extrair_bu.py` já trata tudo isso (conferido: AC 2018, 2º turno, Bolsonaro 294.899 votos, 77,2% dos válidos; e 2022 sem nenhuma diferença em relação à extração anterior).
- O nulo oficial inclui votos anulados de candidatura cassada: no 1º turno de 2026, 5.246 votos do candidato 28 aparecem como nominais no boletim e como nulos no total oficial.
- Zips baixados em paralelo às vezes chegam corrompidos. Verificar com `unzip -tq`.
- 99,8% das seções enviaram o boletim depois das 19h por causa da prorrogação (seção 4.2). Histograma de chegada por hora de Brasília: 16h 1; 17h 1.172; 19h 72.913; 20h 304.805; 21h 118.532.

---

## 4. Fatos checados (com fontes)

### 4.1 Pesquisas
- Radar do Voto listou 38 pesquisas de 2º turno coletadas em outubro: 34 com Flávio na frente, 3 com Lula, 1 empate. https://radardovoto.com/pesquisas/segundo-turno
- As 7 divulgadas na véspera (coleta de 21 a 24/10), votos válidos, Lula x Flávio: AtlasIntel 49,2 x 50,8; CNT/MDA 49,3 x 50,7; Datafolha 49 x 51; Futura 49,9 x 50,1; Gerp 48 x 52; Nexus/BTG 49,5 x 50,5; Quaest 49 x 51. Média de Flávio: cerca de 50,9%. Todas dentro da margem (empate técnico). Resultado: Flávio 48,21%. Erro de cerca de 2,7 pontos, todas para o mesmo lado. https://www.gazetadopovo.com.br/eleicoes/2026/pesquisa-eleitoral-2026/o-que-dizem-as-pesquisas-para-presidente-na-vespera-do-segundo-turno/
- Datafolha anteriores: 6 e 7/10, Flávio 52 x 48; 13 a 15/10, Flávio 51 x 49.
- Precedente: na véspera do 1º turno de 2022, o Datafolha dava Bolsonaro com 36% dos válidos; ele teve 43,2%. https://www.poder360.com.br/pesquisas/datafolha-lula-tem-50-dos-votos-validos-e-bolsonaro-36/

### 4.2 Prorrogação da votação (Zanin)
- A coligação de Lula pediu mais tempo alegando corte de ônibus em Salvador e São Paulo (em Salvador, inspeção judicial encontrou mais da metade da frota na garagem; o secretário de mobilidade foi preso por ordem da Justiça Eleitoral). O pedido chegou ao STF às 16h32 (Brasília).
- O ministro Cristiano Zanin, do STF, prorrogou até as 19h em todas as seções do país e atribuiu ao TSE a execução. A campanha de Flávio também tinha pedido prorrogação, mas só em municípios de SP, PR, SC, MG e RS, por chuva e bloqueios.
- Leitura combinada: é legítimo questionar uma decisão individual, a pedido de um lado, com alcance nacional. Mas ela mexe em quem vota, não em como o voto é contado. Todo o aumento de comparecimento foi de 2,96 milhões; mesmo com dois terços para Lula, daria cerca de 1 milhão de saldo, contra uma vantagem de 4,4 milhões.
- https://www.cnnbrasil.com.br/eleicoes/zanin-prorroga-eleicao-ate-as-19h-deste-domingo-em-todo-o-pais/ e https://exame.com/brasil/por-que-o-tse-decidiu-prorrogar-o-horario-de-votacao-ate-as-19h/

### 4.3 Fiscais do PL
- Até dois fiscais por seção, orientados a escanear o QR code dos boletins. A contagem paralela do partido já indicava o resultado e mostrava Lula subindo 2 a 4 pontos por local de votação em relação ao 1º turno. A reportagem não menciona nenhuma divergência alegada entre boletins e números do TSE. https://www.metropoles.com/colunas/demetrio-vecchioli/com-exercito-de-fiscais-pl-tinha-nocao-da-derrota-desde-as-17h

### 4.4 Comando do TSE
- Presidente: Nunes Marques; vice: André Mendonça. Ambos indicados ao STF por Bolsonaro. https://www.migalhas.com.br/quentes/453930/nunes-marques-e-eleito-presidente-do-tse-andre-mendonca-sera-vice

### 4.5 Barroso e o voto impresso
- Em junho de 2021, presidentes de 11 partidos fecharam posição contra o voto impresso; Barroso, então presidente do TSE, atuou publicamente contra. https://www.poder360.com.br/brasil/presidentes-de-11-partidos-fecham-posicao-contra-voto-impresso/
- A PEC caiu na Câmara em 10/08/2021: 229 a favor, 218 contra, 1 abstenção; eram necessários 308. https://www.cnnbrasil.com.br/politica/pec-do-voto-impresso-e-rejeitada-em-1-turno-na-camara/
- Leitura: oposição ao voto impresso não é evidência de fraude, mas a falta de comprovante conferido pelo eleitor é uma fraqueza real de auditabilidade.

### 4.6 Venezuela, Carvajal e Smartmatic
- Hugo Carvajal, ex-chefe de inteligência venezuelano, declarou-se culpado nos EUA em junho de 2025. Em carta a Trump (divulgada em dezembro de 2025), acusou a Smartmatic de manipular eleições, sem documentos ou detalhe técnico; a carta não cita o Brasil, urna brasileira, malware nem transistores. https://claudiodantas.com.br/carta-trump-carvajal-smartmatic-manipulacao/ e https://en.wikipedia.org/wiki/Hugo_Carvajal
- A Smartmatic não desenvolveu as urnas brasileiras: teve com o TSE só serviços de conexão de dados e voz e perdeu para a Positivo a licitação de urnas de 2020. Documentos da CIA divulgados em 16/07/2026 dizem que Venezuela e Smartmatic planejaram alterar votos em 2012, concluem que não houve fraude eletrônica em larga escala e que eles não conseguiriam manipular de forma previsível uma eleição fora da Venezuela. https://www.agencialupa.org/noticias/2026/07/17/smartmatic-citada-em-relatorio-da-cia-sobre-eleicoes-venezuelanas-nao-desenvolveu-urnas-do-brasil/
- Na Venezuela (2024), a fraude foi demonstrada comparando as atas impressas pelas máquinas com o resultado oficial, que o órgão eleitoral não publicou por mesa. No Brasil a comparação equivalente (boletins contra total) bate voto a voto (seção 6.7).

### 4.7 Fernando Cerimedo (o "argentino" de 2022)
- Consultor argentino (canal La Derecha Diario; depois estrategista digital de Milei). Em novembro de 2022, live alegando que modelos antigos de urna deram mais votos a Lula que a UE2020 e que haveria uma "trava" no total de votos das urnas antigas.
- O TSE respondeu que todos os modelos foram testados. Pesquisadores da USP e da UFSCar mostraram que a "trava" é o limite de eleitores por seção (cerca de 400; as UE2020 iam para seções maiores) e que os modelos estavam distribuídos de forma desigual pelo território. https://jornal.usp.br/wp-content/uploads/2022/11/Analise-USPUFSCar-Alegacoes-Fraude-Urnas-v5.2-2.pdf
- O PL usou os argumentos para pedir a anulação de votos das urnas antigas; o TSE rejeitou e multou a coligação em R$ 22,9 milhões por má-fé. https://diariodonordeste.verdesmares.com.br/pontopoder/alexandre-de-moraes-indefere-pedido-de-pl-e-multa-partido-de-bolsonaro-em-r-229-milhoes-1.3304459
- A PF o indiciou em novembro de 2024 no inquérito do golpe; a PGR não o denunciou porque não ficou demonstrado que ele sabia que o relatório era falso. https://apublica.org/2025/09/julgamento-stf-quem-foi-indiciado-mas-nao-deve-ser-julgado/
- O teste dele foi refeito do jeito certo nesta sessão (seção 6.6).

### 4.8 Felipe Gimenez
- Procurador do Estado de MS. Em maio de 2021 (Pânico, Jovem Pan) defendeu voto impresso com contagem pública, disse que há indícios de que as urnas são seguras mas não evidências, e que fraude seria impossível de provar porque a contagem ocorre dentro da máquina; citou documentos estatísticos não publicados, sem apresentar prova. https://jovempan.com.br/programas/panico/e-impossivel-provar-fraudes-do-sistema-eleitoral-eletronico-afirma-procurador.html
- Em 10/01/2023, Bolsonaro postou e apagou cerca de três horas depois um trecho em que Gimenez diz que Lula não foi eleito pelo povo; o post levou Bolsonaro ao inquérito do 8 de janeiro, e ele disse à PF (26/04/2023) que publicou por engano, sob efeito de remédios. https://exame.com/brasil/bolsonaro-divulga-video-que-questiona-vitoria-de-lula-mas-apaga-publicacao/ e https://www.poder360.com.br/brasil/bolsonaro-diz-a-pf-que-fez-publicacao-sob-efeito-de-remedios/
- Segundo reportagem, a PGE de MS arquivou uma investigação contra ele. https://semanaon.com.br/judiciario/pge-arquiva-investigacao-contra-procurador-que-mentiu-sobre-eleicoes-em-video-divulgado-sem-querer-por-bolsonaro/

### 4.9 Teste de integridade (votação paralela)
- Na véspera, urnas de seções reais são sorteadas (ou indicadas por OAB, MP e partidos) e trocadas por reservas. No dia, voluntários digitam votos que entidades externas anotaram antes em cédulas de papel; tudo é filmado tecla por tecla; o boletim é comparado com o papel. Há uma versão com biometria de eleitores reais, criada para impedir que um software malicioso perceba o teste. https://www.correio24horas.com.br/economia/justica-eleitoral-detalha-auditoria-das-urnas-para-2026-saiba-como-funciona-a-votacao-paralela-0226
- 1º turno de 2026: o TSE informou que papel e urna bateram (DF: 20 urnas, com MP, Defensoria, TCU, PF, CGU e OAB acompanhando). https://www.tse.jus.br/comunicacao/noticias/2026/Outubro/teste-de-integridade-no-tse-confirma-correspondencia-entre-cedulas-e-votos-registrados-nas-urnas
- **Ponto em aberto importante:** não foi confirmado se as cédulas do teste incluem votos em branco e nulos para presidente. Se não incluírem, o teste não cobre a tese de conversão de branco e nulo (seção 5).

---

## 5. Hipóteses do usuário e o que os testes mostraram

| Hipótese | Teste | Resultado | Situação |
|---|---|---|---|
| "Ninguém ganha 10 milhões de votos em 30 dias" | Aritmética do 2º turno e precedentes | São 21 dias e é redistribuição: 9,3 mi dos eliminados, cerca de 3,0 mi a mais de comparecimento, cerca de 1,8 mi a menos de branco e nulo. Lula +10,4 mi, Flávio +3,7 mi. Em 2018, Haddad ganhou 15,7 mi entre turnos. Ressalva válida do usuário: em 2018 o bolo de eliminados era bem maior (cerca de 26 mi) | Premissa não se sustenta |
| Pesquisas erraram todas | Levantamento de 38 pesquisas | Fato confirmado: erro de cerca de 2,7 pontos para o mesmo lado. Erros sistemáticos maiores já ocorreram (2022, contra Bolsonaro) | Indício fraco de fraude; erro de pesquisa real |
| Prorrogação de Zanin | Escala do efeito; horários de boletim | Fato confirmado e contestável. Efeito máximo estimado de cerca de 1 mi de saldo contra 4,4 mi de vantagem. 99,8% das seções fecharam às 19h, então não há grupo de controle | Questão de justiça do pleito, não de contagem |
| Branco e nulo convertidos em voto de Lula (versão 1º x 2º turno) | Teste natural nos 6 estados com 2º turno de governador; correlação entre estados | Nesses 6 estados o branco/nulo de presidente não caiu (subiu em 5), e Lula cresceu 2,64 pontos contra 3,00 nos demais: diferença na direção da conversão, mas menor que a esperada. Correlação entre queda do branco/nulo e virada de Lula: -0,11. A soma dos boletins não testa esta tese | Inconclusivo por estado; testes por seção pendentes (seção 7). Antes registrado como "falhou"; ver a correção na seção 6.8 |
| Branco e nulo convertidos como "valor desconhecido" (só a urna sabe) | Escala e teste de integridade | Para Flávio ter vencido, seria preciso converter mais de 4,4 mi de votos, mais que todo o branco e nulo restante (4,15 mi), ou seja, mais da metade de todos os brancos e nulos; supondo o 1º turno limpo, o branco/nulo real teria de subir de 4,8% para pelo menos 6,7%. Uma conversão desse tamanho apareceria em teste com cédulas conhecidas, a menos que o software reconhecesse o teste | Depende do relatório do teste de integridade e de saber se as cédulas têm branco e nulo |
| "Roubo limitado, por isso perdem governos e Congresso" | Lógica | Cada limite acrescentado para a tese caber nos fatos a torna menos testável. Registrado como alerta | Não testável como está |
| Malware de hardware nas urnas (atribuído a Carvajal) | Teste por modelo de urna | Carvajal não fala do Brasil nas fontes encontradas. 2022: nenhum efeito de modelo no mesmo prédio. 2026, 1º turno: urnas antigas um pouco mais de Lula, como em 2022 e dentro da margem da diferença entre anos | Teste decisivo (virada por modelo) pendente |
| Lula subiu em todos os estados, improvável | 2018, 2022, 2026 | Em 2022 Bolsonaro subiu nos 27 estados e em 98% dos municípios; em 2018 Haddad subiu em 25. Padrão normal de 2º turno | Premissa não se sustenta |
| Lula já era muito alto, difícil subir em todos | Redutos dos dois lados | Lula teve 45,2% no 1º turno (segundo lugar). Nos redutos (63% a 75%), Lula subiu 1,2 a 2,5 pontos; Bolsonaro, em 2022, subiu 1,0 a 2,2 nos dele. Menor ganho no reduto mais forte nos dois casos | Efeito teto confirmado e igual nos dois lados |
| Cerimedo: urnas antigas favoreceram Lula em 2022 | Teste refeito controlando o local de votação | Diferença bruta de até 5 pontos cai para 0,2 a 0,4 (margem de 0,3) no mesmo prédio; virada entre turnos 0,17 menor nas antigas | Não se sustenta |

---

## 6. Resultados detalhados

### 6.1 Comparação seção a seção (final)
- 499.177 seções em 5.714 municípios comparadas com o 1º turno das mesmas seções. Migração média para Lula: +2,97 pontos.
- Com 2.014 municípios 100% apurados (por volta das 19h30): mediana da virada +2,37; percentis 1, 5, 25, 50, 75, 95 e 99: -1,70; 0,24; 1,57; 2,37; 3,12; 4,21; 4,84. 79 municípios com virada negativa, 3 acima de +8.

### 6.2 Matriz de transferência (regressão ecológica por município)
Atenção: resultado frágil. Muda com a especificação e não pode ser lido como comportamento individual.
- Níveis, com restrição (5.533 municípios completos): eleitores de Lula e Flávio no 1º turno ficaram com eles; demais candidatos: 37% Lula, 43% Flávio, 20% não votaram validamente; abstenção do 1º turno: 2% para Lula.
- Separando: Renan Santos, Caiado e Zema: 37% Lula, 63% Flávio. Cury: 40% Lula, 3% Flávio.
- Branco/nulo do 1º turno aparece com 77% a 100% para Lula nos agrupamentos de `transfer2.py` (Brasil 100%, Norte e Nordeste 96%, Sul e Sudeste 77%); por região em `transfer.py`, vai de 62% (Sudeste) a 100% (Norte). Isso **não** significa que esses eleitores votaram em Lula: em outra especificação (fluxos com efeito fixo por UF) o coeficiente passa de 100% (118%), o que é impossível e mostra que a variável funciona como proxy de outra coisa. Isso foi corrigido explicitamente com o usuário durante a conversa.
- Mesma conta em três eleições (coeficiente branco/nulo do 1º turno para o candidato de esquerda): níveis 8% (2018), 21% (2022), 100% (2026); dentro de cada UF 14%, 14% e 67%; UFs acima de 70%: 2, 4 e 10 de 24. Para o candidato da direita: níveis 13%, 13% e 0%; dentro de cada UF 16%, 38% e 3%.

### 6.3 Branco, nulo e abstenção
- Branco+nulo de presidente (% do comparecimento): 2018: 8,79% para 9,57%; 2022: 4,41% para 4,59%; 2026: 4,77% para 3,24%. Primeira queda entre turnos das três eleições.
- Abstenção nas mesmas seções: 21,08% para 19,22% (-1,86 ponto), base de 158,7 milhões de eleitores.
- Com 71,7% apurado, a queda da abstenção foi maior onde Flávio era forte no 1º turno (-1,84 ponto) do que onde Lula era forte (-1,26).
- Por estado: o branco/nulo de presidente caiu 1,69 ponto nos 21 estados sem 2º turno de governador e subiu 0,14 nos 6 com governador.

### 6.4 Testes forenses clássicos (2º turno, municípios)

| | 2018 | 2022 | 2026 |
|---|---|---|---|
| Último dígito, p-valor esquerda / direita | 0,63 / 0,34 | 0,62 / 0,76 | 0,60 / 0,57 |
| Municípios com comparecimento acima de 95% e voto acima de 90% num lado | 0 | 0 | 0 |
| Maior comparecimento municipal | 93,8% | 94,1% | 93,1% |
| Correlação comparecimento x voto na esquerda, dentro da UF | -0,356 | -0,338 | -0,290 |
| 5% de maior comparecimento de cada UF contra o resto da UF (fatia da esquerda) | -4,0 | -4,1 | -2,1 |

Nenhum sinal de enchimento de urna ou de números inventados.

### 6.5 Uniformidade da virada
- 2018: Haddad subiu em 25 de 27 estados e em 73% dos municípios (de -0,2 a +13,1 pontos).
- 2022: Lula caiu nos 27 estados (Bolsonaro subiu em todos) e subiu em só 2% dos municípios.
- 2026: Lula subiu em todos os estados e em 97% dos municípios (de +1,2 a +4,4 pontos).
- Correlação entre a virada de Lula e o voto dos outros candidatos no 1º turno, por estado: +0,61. Maiores viradas: RJ +4,4, SP +4,0, GO +3,8 (onde Lula era fraco). Menores: BA e PI +1,2, CE +1,9 (onde já tinha 70% ou mais).

Virada por estado (arquivos oficiais por UF), em pontos, e queda do branco/nulo de presidente (* = 2º turno de governador):
AC* +2,64 / -0,78; AL +3,27 / +3,36; AM* +2,28 / -0,39; AP +2,85 / +0,52; BA +1,44 / +1,97; CE +2,00 / +2,14; DF* +3,10 / -0,20; ES* +2,83 / -0,38; GO +3,65 / +0,74; MA +2,10 / +1,43; MG +3,12 / +1,77; MS +3,22 / +0,95; MT +3,00 / +0,95; PA +2,15 / +2,03; PB +2,51 / +3,27; PE +2,04 / +2,37; PI +1,21 / +1,54; PR +3,18 / +0,89; RJ +4,25 / +1,57; RN* +2,51 / +0,90; RO +2,65 / +0,33; RR +3,20 / +0,42; RS +3,06 / +1,41; SC +3,27 / +0,57; SE +2,33 / +2,19; SP +3,77 / +1,82; TO* +2,37 / -1,00.

### 6.6 Teste por modelo de urna

**2022, 2º turno (472.024 seções). Bruto:** Lula com UE2009 51,03%; UE2010 53,77%; UE2011 53,84%; UE2013 51,23%; UE2015 51,56%; UE2020 48,95%.

**2022, mesmo local de votação** (10.748 locais com modelos diferentes, 82.758 seções), diferença em relação à UE2020 vizinha:
- Fatia de Lula no 2º turno: +0,24 a +0,37 (erro-padrão 0,30).
- Virada do 1º para o 2º turno (mesma seção, mesmo modelo): -0,16 a -0,18 (erro-padrão 0,12).
- Branco+nulo no 2º turno: -0,15 a -0,17 (0,10). Variação do branco+nulo: -0,04 a -0,06 (0,10 a 0,11).
- 1º turno de 2022, nível: +0,43 a +0,60 (0,33).

**2026, 1º turno (499.206 seções). Bruto:** UE2013 51,15%; UE2015 49,16%; UE2020 48,73%; UE2022 49,04% (Lula contra Flávio).
**Mesmo local** (7.896 locais, 65.839 seções), contra a UE2022 vizinha: UE2013 +0,95 (0,31); UE2015 +0,74 (0,30); UE2020 +0,05 (0,05). Branco+nulo: +0,02 a +0,03.
- Votos (Lula+Flávio) por modelo: UE2022 43,88 mi; UE2020 43,93 mi; UE2015 19,57 mi; UE2013 2,60 mi. Mesmo que toda a diferença fosse manipulação, seriam cerca de 170 mil votos trocados no 1º turno.
- Leitura: mesma direção de 2022, um pouco maior, diferença entre anos dentro do ruído. Mais compatível com o modo de distribuir urnas dentro dos prédios (as novas vão para seções maiores) do que com a máquina. O teste decisivo é a virada entre turnos na mesma seção e mesma urna, que depende dos boletins do 2º turno.

### 6.7 Soma dos boletins de urna contra o total oficial
- 2022, 1º turno: Lula 57.259.504 e Bolsonaro 51.072.345 nos dois. Diferença zero.
- 2022, 2º turno: Lula 60.345.999 e Bolsonaro 58.206.354 nos dois. Diferença zero.
- 2026, 1º turno: Lula 53.879.538, Flávio 56.104.503, branco 2.300.798, comparecimento 125.275.835, idênticos. Nulos: 3.669.003 nos boletins contra 3.674.249 no oficial; a diferença de 5.246 é exatamente o total do candidato 28, cuja candidatura foi anulada e cujos votos o TSE conta como nulos.
- Conclusão: não há alteração entre o boletim impresso na seção e o total nacional nesses turnos. Isso descarta fraude na totalização, mas não uma urna que já registre errado. 2º turno de 2026: pendente.

### 6.8 Presidente contra governador (mesmos eleitores, mesma urna)
Estados com 2º turno de governador em 2026, branco+nulo em % do comparecimento (presidente 1T, presidente 2T, governador 1T, governador 2T):
AM 2,85 / 3,24 / 7,18 / 5,28; RN 4,57 / 3,66 / 8,36 / 5,21; DF 3,20 / 3,40 / 9,06 / 6,91; ES 4,30 / 4,68 / 10,07 / 8,22; AC 3,94 / 4,72 / 9,90 / 9,17; TO 3,60 / 4,60 / 11,95 / 8,62.
- Queda do branco/nulo de presidente menos queda do de governador: 2026 -2,49 pontos; 2022 -6,20 (-3,67 sem SE, que tem um valor atípico no 1º turno).
- **Correção em 26/10:** a versão anterior deste documento lia esse sinal ao contrário. Conversão de branco/nulo de presidente aumentaria a queda do de presidente e deixaria esse número menos negativo. Em 2026 ele é menos negativo que em 2022, ou seja, na direção que a conversão produziria. Mas a comparação entre os anos é fraca: os estados e as disputas de governador são outros, e o tamanho da queda do branco/nulo de governador depende da disputa local. Esse número sozinho não serve nem a favor nem contra.
- Os outros números por estado: o branco/nulo de presidente subiu em 5 dos 6 estados com governador e caiu 1,69 ponto nos demais. A explicação sem fraude proposta na conversa: onde só há a disputa de presidente, quem votaria em branco tende a nem ir votar. Lula cresceu 2,64 pontos nesses 6 estados e 3,00 nos demais; a diferença de 0,36 vai na direção da conversão, mas é menos da metade dos cerca de 0,9 ponto esperados se toda a diferença de branco/nulo entre os dois grupos tivesse virado voto de Lula, e não controla as outras diferenças entre esses estados. Correlação entre queda do branco/nulo e virada de Lula entre os 27 estados: -0,11.
- Conclusão por estado: inconclusivo. Uma fraude que evitasse justamente esses 6 estados também escaparia deste teste. Os testes por seção (seção 7) decidem melhor.
- Referência por seção em 2022 (`analisar_gov.py`): cada ponto a mais de queda do branco/nulo de presidente, relativa ao de governador, vem com +0,04 ponto de virada para Lula. Conversão daria perto de +0,5.

### 6.9 Comparecimento e prorrogação
- Por inclinação do município no 1º turno (com 71,7% apurado), variação da abstenção: Flávio forte -1,84; Flávio à frente -1,67; equilibrado -1,64; Lula à frente -1,48; Lula forte -1,26 pontos.
- Por porte (parcial): queda entre -1,26 e -1,73 em todos os portes.

### 6.10 Pista do branco/nulo por seção: referências de 2018 e 2022
`analisar_bn_secao.py`: virada do 13 entre turnos contra o branco/nulo do 1º turno da própria seção, comparando seções do mesmo local de votação, com controles para a fatia do 13 e dos demais candidatos no 1º turno. Coeficiente em pontos de virada por ponto de branco/nulo (erro-padrão agrupado por local):

| | 2018 | 2022 | 2026 |
|---|---|---|---|
| Seções / locais | 427.541 / 66.849 | 448.165 / 68.662 | pendente |
| Branco/nulo médio no 1º turno | 8,76% | 4,41% | 4,77% |
| Coeficiente do branco/nulo do 1º turno | -0,060 (0,002) | -0,071 (0,002) | pendente |
| Coeficiente dos outros candidatos | +0,231 (0,003) | -0,075 (0,002) | pendente |
| Coeficiente da fatia do 13 | -0,399 (0,002) | -0,177 (0,001) | pendente |

- Nos dois anos de referência, seção com mais branco/nulo no 1º turno teve virada um pouco **menor** para o 13 dentro do mesmo prédio, e o número quase não mudou entre os anos (diferença de 0,011).
- Os outros coeficientes mudaram muito entre 2018 e 2022 (o dos outros candidatos foi de +0,23 para -0,08). Ou seja, coeficientes de comportamento variam bastante de uma eleição para outra; um valor diferente em 2026 também pode ter causa comportamental.
- Calibração: uma conversão nova em 2026, proporcional ao branco/nulo de cada seção, do tamanho da queda do branco/nulo entre turnos (1,82 milhão) subiria o coeficiente em cerca de +0,15; uma capaz de inverter o resultado (4,43 milhões), em cerca de +0,35 a +0,40. Uma conversão de número fixo por urna não aparece neste teste.

---

## 7. Critérios definidos antes dos dados

Combinados com o usuário antes de ver os resultados. Relatar o que der, sem suavizar.

**Evidência forte de fraude seria qualquer um destes:**
1. Boletim (papel escaneado pelos fiscais ou arquivo publicado) diferente do total do TSE.
2. Anomalias concentradas em urnas ou zonas específicas em 2026 e ausentes em 2022.
3. Logs de urna com horários impossíveis (votos depois do fechamento, ritmo não humano).
4. Registro digital dos votos diferente do boletim.

**Teste por modelo de urna (2º turno de 2026):** bandeira vermelha se algum modelo, comparado com as UE2022 vizinhas no mesmo local de votação e usando a mesma seção nos dois turnos, mostrar virada para Lula maior que 0,5 ponto e acima de 3 erros-padrão, ou queda de branco+nulo maior que 0,5 ponto e acima de 3 erros-padrão. Referência de 2022: virada das urnas antigas -0,17 (erro-padrão 0,12).

**Teste presidente contra governador (seção):** conversão de branco/nulo de presidente levaria o coeficiente para perto de +0,5. Referência de 2022: +0,04.

**Pista do branco/nulo por seção (`analisar_bn_secao.py`), definido em 26/10/2026, antes da publicação dos boletins do 2º turno de 2026:** referências 2018 -0,060 e 2022 -0,071 (erro-padrão 0,002). Sinal a favor da tese: coeficiente de 2026 acima de +0,04 (o maior das referências mais 0,10) e a mais de 3 erros-padrão disso. Compatível com uma conversão capaz de inverter o resultado: coeficiente de +0,29 ou mais. Entre -0,07 e +0,04: sem sinal. Um sinal aqui é indício, não prova, porque também pode ter causa comportamental (seção 6.10); se aparecer, cruzar com o teste presidente x governador por seção e com o teste de integridade.

---

## 8. Pendências

### 8.1 Tarefas agendadas na conversa original (não na nova sessão)
- 26/10/2026 às 13h (Cuiabá), identificador `trig_01QWfzZEdPBKpkfVgntJZssD`: rodar `rodar_2026.sh`; se os boletins do 2º turno não estiverem publicados, repetir a cada 6 horas até 01/11.
- 26/10/2026 às 13h10, identificador `trig_01RefwLZMaHLA4F1LJkQtiZA`: ler o relatório do teste de integridade do 2º turno (quantas urnas, divergências e se as cédulas incluem branco e nulo para presidente); repetir a cada 12 horas até 31/10.

Essas tarefas voltam para a conversa original e usam os arquivos daquele ambiente. Se aquele ambiente for reciclado por inatividade, os arquivos de lá podem se perder; este pacote é a cópia de segurança. Na nova sessão, reproduzir com os comandos da seção 9.

### 8.2 Para fazer no Claude Code
1. Verificar a publicação dos boletins do 2º turno (`./auditoria/rodar_2026.sh`; código 2 = ainda não saiu). Quando sair, rodar e aplicar os critérios da seção 7.
2. Confirmar a soma dos boletins do 2º turno contra o total oficial (está na rotina).
3. Descobrir a especificação de download dos arquivos de urna (EA18, "Instruções para download dos arquivos da divulgação", em https://www.tse.jus.br/eleicoes/arquivos) para baixar `-bu.dat`, `-rdv.dat` e `-log.jez` de amostras e testar: ritmo de votação nos logs, registro digital contra boletim. Não chutar caminhos (risco de bloqueio de IP).
4. Ler o relatório do teste de integridade do 2º turno e a resolução do TSE de 2026 sobre auditoria: as cédulas incluem branco e nulo para presidente?
5. Quando `votacao_secao_2026_BR.zip` for atualizado com o 2º turno, repetir as análises por seção sem depender dos boletins.
6. Opcional: transformar o robô em uma página web estática que lê o TSE direto do navegador (o host aceita CORS) e publicar no Vercel, se o usuário pedir.
7. Pista do branco/nulo por seção em 2026 (`analisar_bn_secao.py`, já incluído em `rodar_2026.sh`), contra as referências de 2018 e 2022 e o critério da seção 7.
8. Excesso de seções com branco/nulo de presidente zerado ou quase zerado no 2º turno: comparar com o esperado pelo tamanho da seção e pelo 1º turno, com 2022 como referência e, nos 6 estados, com o branco/nulo de governador na mesma urna. Definir o critério antes de rodar.
9. Branco/nulo declarado nas pesquisas finais (Datafolha, Quaest, AtlasIntel) contra o registrado, em 2018, 2022 e 2026, tratando "não sabe" do mesmo jeito nos três anos. É a principal medida independente do "valor desconhecido".
10. Relatórios de fiscalização de 2026: inspeção do código-fonte, verificação de assinaturas e resumos digitais dos sistemas nas urnas, auditorias de partidos e entidades. Procurar qualquer divergência relatada.
11. Boletins escaneados pelos fiscais do PL: se forem publicados, comparar uma amostra com os boletins do TSE.

---

## 9. Como rodar

Requisitos: Node 18 ou superior; Python 3.10 ou superior com `numpy` e `scipy` (`pip install numpy scipy`); `curl`, `unzip` e `grep`. Espaço em disco: cerca de 12 GB se for baixar os boletins de 2026 (1º e 2º turnos).

```bash
# robô (de dentro de robo-tse/)
node robo-tse.js                            # painel em http://localhost:8787
node robo-tse.js --uma-vez --conc 4         # uma leitura e sai

# auditoria (de dentro de auditoria/)
./rodar_2026.sh                             # código 2 = boletins do 2º turno ainda não publicados
python3 analisar_modelos.py secoes2022.json.gz 2022
python3 analisar_1turno.py secoes2026_1t.json.gz 2026 1
python3 analisar_gov.py secoes2022.json.gz 2022
python3 analisar_bn_secao.py secoes2022.json.gz 2022   # pista do branco/nulo por seção (também 2018)
./preparar_2018.sh                          # só se for refazer 2018 do zero (baixa cerca de 1,4 GB)
python3 uf_swing.py                         # virada e branco/nulo por estado (consulta o TSE)
python3 gov_vs_pres.py                      # presidente x governador por estado (consulta o TSE)

# análises gerais (de dentro de analises/)
python3 compara.py                          # matriz de transferência 2018, 2022 e 2026 + forense
python3 transfer.py                         # matriz de transferência de 2026 por grupo de candidatos
python3 forense2.py                         # testes forenses clássicos 2018, 2022 e 2026
node forense.js                             # distribuição da virada e do comparecimento (retrato das 19h30)
node teste.js                               # backtest do modelo de projeção (usa cache.json)
node mun2t.js                               # baixa de novo o 2º turno por município (atualiza mun2t.json)
```

Conferência feita depois de montar o pacote: os caminhos absolutos do ambiente original foram trocados por caminhos relativos ao próprio script; todos os scripts passaram na checagem de sintaxe; `rodar_2026.sh` (código 2), `compara.py`, `transfer.py`, `transfer2.py`, `porUF.py`, `forense2.py`, `forense.js`, `teste.js`, `analisar_1turno.py`, `analisar_gov.py` e `gov_vs_pres.py` foram rodados a partir do pacote e reproduziram os números deste documento.

Arquivos grandes que ficaram de fora (baixar só se for refazer do zero):
- `votacao_secao_2026_BR.zip` (162 MB), para `analises/tse/build_baseline.py` e `analises/tse/por_candidato.py` (este espera o arquivo com o nome `secao1t.zip` na mesma pasta): https://cdn.tse.jus.br/estatistica/sead/odsele/votacao_secao/votacao_secao_2026_BR.zip
- `votacao_candidato_munzona_2018.zip` e `_2022.zip`, para `analises/d2018/build2018.py` e `analises/d2022/build2022.py` (endereços na seção 3.2).
- Os zips de boletim de urna (`bweb`), que `rodar_2026.sh` baixa sozinho; os de 2022 estão listados em `auditoria/urls2022.txt`.

---

## 10. Estrutura do pacote

```
eleicao-2026/
  CONTEXTO-ELEICAO-2026.md            este documento
  robo-tse/
    robo-tse.js                       robô de captura e projeção
    painel.html                       painel (servido pelo robô e publicado como artefato)
    baseline-1t.json.gz               1º turno por seção (base do modelo)
    LEIA-ME.txt                       instruções curtas de uso no Mac
    estado-final.json                 última leitura do robô (22h46, 99,99% das seções)
    historico-2026-10-25.csv          projeção a cada atualização durante a noite
    robo-2026-10-25.log               log completo da noite
  auditoria/
    extrair_bu.py                     extrai Presidente e Governador dos zips de boletim
    analisar_modelos.py               teste por modelo de urna (bruto e dentro do mesmo local)
    analisar_1turno.py                mesmo teste com um turno só
    analisar_gov.py                   presidente x governador por seção
    analisar_bn_secao.py              pista do branco/nulo por seção, dentro do mesmo local
    gov_vs_pres.py, uf_swing.py       comparações por estado (consultam o TSE)
    rodar_2026.sh                     rotina completa para quando o 2º turno sair
    preparar_2018.sh                  baixa e extrai os boletins de 2018
    faixas.json                       faixas de número de série por modelo
    resultado2022.json                resultado do teste por modelo em 2022
    secoes2018.json.gz                boletins de 2018 extraídos (dois turnos, com governador)
    secoes2022.json.gz                boletins de 2022 extraídos (dois turnos, com governador)
    secoes2026_1t.json.gz             boletins do 1º turno de 2026 extraídos (sem governador)
    oficial2026_1t.json, oficial2026_2t.json   totais oficiais do TSE
    urls2018.txt, urls2022.txt, urls2026_1t.txt   endereços dos zips de boletim
  analises/
    tse/build_baseline.py             gera a base do 1º turno por seção
    tse/por_candidato.py              1º turno por candidato e município
    tse/por_candidato_1t.json         resultado (nacional e por município)
    mun2t.js, mun2t.json              2º turno de 2026 por município (retrato com 5.533 completos)
    d2018/, d2022/                    detalhe por município e zona (zips) e resultados processados
    compara.py, porUF.py              transferência 2018, 2022 e 2026 (porUF: por estado)
    transfer.py, transfer2.py         matriz de transferência de 2026
    forense2.py, forense.js           testes forenses e distribuição da virada
    abst.js, abst.json                abstenção nas mesmas seções por inclinação e porte
    prorrog.js, prorrog.json          horário de publicação dos boletins (efeito da prorrogação)
    teste.js, diag.js, diag2.js       backtest e diagnósticos do modelo
    cache.json                        retrato dos dados do TSE às 19h30 (para o backtest)
```

---

## 11. Avaliação atual

Até aqui, os dados apontam para uma vitória real de Lula, com um erro grande e na mesma direção de todas as pesquisas e uma mudança de regra contestável no dia (a prorrogação nacional até as 19h). Os testes de totalização (boletins contra total) e de padrão (virada uniforme, comparação com 2018 e 2022, testes forenses) não mostraram sinal de fraude.

A tese de conversão de branco e nulo não foi derrubada. O teste por estado com governador ficou inconclusivo (seção 6.8); os testes que já bateram (soma dos boletins, modelo de urna) não alcançam uma conversão feita pelo software em todas as urnas; e a versão "valor desconhecido" só pode ser testada pelo teste de integridade com branco e nulo e por medidas indiretas (seção 0.1). O que pesa contra ela hoje é um argumento de plausibilidade, não um teste: para inverter o resultado, o branco/nulo verdadeiro do 2º turno teria de ser de pelo menos 6,7% do comparecimento, contra 4,8% registrados no 1º turno, quando entre turnos o branco/nulo variou +0,8 ponto em 2018 e +0,2 em 2022; e a conversão teria de ser maior que todo o branco e nulo registrado. Esse argumento supõe o 1º turno limpo. Se a conversão também tivesse ocorrido no 1º turno, ele enfraquece, porque os 4,8% também estariam subestimados.

O que pode mudar essa avaliação: divergência na soma dos boletins do 2º turno; virada diferente por modelo de urna dentro do mesmo prédio; coeficiente presidente contra governador perto de +0,5; coeficiente do branco/nulo por seção em 2026 muito acima de 2018 e 2022; excesso de seções com branco/nulo zerado; branco/nulo declarado nas pesquisas muito acima do registrado, fora do padrão de 2018 e 2022; divergência no teste de integridade; ou cédulas de teste sem branco e nulo, o que deixaria a tese do usuário sem cobertura nesse teste específico. Se qualquer um desses aparecer, dizer com clareza.
