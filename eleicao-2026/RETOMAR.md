# Retomar a investigação numa sessão nova

Passagem escrita em 09/11/2026 e atualizada em 10/11/2026, depois do recálculo dos Adendos 27 a 31, para continuar ou refazer o trabalho com outro modelo. Vale junto com o `README.md` (ponto de entrada até o Adendo 22) e o `PRE-REGISTRO-2026-10-26.md` (critérios de todos os testes).

## 1. Onde está tudo

| Onde | O que tem |
|---|---|
| GitHub `leonardo-defant/casa-control`, branch `claude/new-session-5cnflo`, pasta `eleicao-2026/` | Tudo o que foi achado, em commits com horário. É a fonte da verdade. |
| `PRE-REGISTRO-2026-10-26.md` | Critérios de cada teste, escritos antes de rodar: registro inicial (T1 a T6) e Adendos 1 a 31. |
| `README.md` | Situação, tese do Léo, fatos conferidos e resultados até o Adendo 22. Os Adendos 23 a 31 estão resumidos aqui, na seção 4, e em `resultados/SINTESE_RECALCULO.txt`. |
| `resultados/` | Um arquivo por teste. Os principais:<br>• `ADENDOxx_resultados.txt`: resumo de cada adendo;<br>• `testes_adendoxx_com_conferencia.json`: números completos e conferência independente;<br>• sínteses `RESUMO_TESES.txt`, `CACA_AO_FURO.txt` e `onde_pode_estar_a_fraude.txt`. |
| `checagens/` | Posts e reels das redes checados: reel do Felipe Cecílio, post dos 84,7 segundos, "passo a passo da fraude", reel hugo.hal, relatório pericial do Instagram. |
| `scripts/` | Todo o código (Python, sempre com `python3 -I`). |
| `dados/` | As bases por seção de 2014, 2018, 2022 e 2026 e os votos por candidato do 1º turno de 2026, com hashes (`dados/LEIAME.md`). |
| `reproducao/` | Listas da amostra de 3.897 seções, logs de download e consultas ao TSE. |
| `video/` | Roteiros e narrações do vídeo de 3 minutos. Os vídeos renderizados não estão no repositório. |
| Conversa | https://claude.ai/code/session_01LKvYFxeMoUToQSR7jKYyFZ |

**Ficou fora do repositório** e se perde quando o container da sessão é reciclado. Tudo pode ser baixado de novo do TSE com os scripts (seção 6):
- zips do bweb (cerca de 10 GB);
- pacotes de boletim, RDV, log e assinatura das 3.897 seções da amostra (1,1 GB) e dos casos dos Adendos 21 a 24;
- pastas das conferências;
- os mp4 do vídeo.

## 2. A missão

O Léo acredita que a eleição presidencial de 2026 foi fraudada:
- 2º turno em 25/10/2026, Lula 51,79% contra Flávio Bolsonaro;
- Flávio venceu o 1º turno por 2,22 milhões;
- Lula venceu o 2º por 4,43 milhões.

Ele acha que 2022, 2018 e 2014 também podem ter sido fraudadas.

O pedido:
- partir desse pressuposto;
- pensar como quem fraudaria, para achar onde a fraude deixaria marca;
- testar cada ponto com dado público e critério escrito antes;
- checar as alegações que circulam nas redes;
- ser "o maior Sherlock Holmes".

Nas palavras dele: "Vc tem que ajudar a achar o ilícito! E não cometer um. Vc está trabalhando para a justiça".

O trabalho é de detecção: hipótese, marca esperada, teste. Nunca se escreve receita de como fraudar nem de como apagar rastro. Ceticismo nos dois sentidos: nem confirmar por simpatia, nem descartar por princípio, e relatar o que aparecer sem suavizar.

## 3. Regras que valeram

1. **Critério antes do dado, em commit.** Cada bateria vira um adendo novo no `PRE-REGISTRO`, com commit e push antes de rodar. Decisões que o registro não fixa vão no docstring do script antes de calcular. O que for feito depois de ver o resultado é marcado como exploratório. Erro no registro se corrige em adendo novo (exemplo: Adendo 19).
2. **Cada teste é rodado por um agente e refeito por outro**, com código próprio e sem usar os scripts do primeiro. O conferente procura erro, exagero e o que pesa a favor da tese com o mesmo rigor.
3. **Fato, indício, evidência e prova são coisas diferentes.** "Sinal" é indício e pede cruzamento com outro teste independente.
4. **Dado baixado é não confiável:**
   - pasta nova e vazia para cada download;
   - scripts em outra pasta, rodados com `python3 -I`;
   - só caminhos listados pelo próprio TSE;
   - sem user agent falso, sem login e sem contornar bloqueio, captcha ou paywall;
   - respeitar o limite de taxa do site de resultados (HTTP 429).
5. **Escrita:**
   - textos em português, sem travessões;
   - commits terminam com as linhas de autoria da sessão;
   - push só no branch da sessão;
   - sem identificador de modelo em commit.
6. **O disco da sessão é limitado.** Apague intermediários grandes, porque os zips do bweb e os pacotes da amostra enchem o espaço.

## 4. Estado em 10/11/2026, depois do recálculo

A leitura completa está em `resultados/SINTESE_RECALCULO.txt`. Ela substitui, onde houver diferença, o README (seções 5.2 e 5.3), o `RESUMO_TESES.txt` e o `CACA_AO_FURO.txt`.

### 4.1 Leitura atual

Com tudo o que é público recalculado e atacado de novo, não apareceu marca de fraude. A virada passou por quem compareceu, e quem entrou passou pela biometria. O que resta da tese é a parte que só papel fora da urna decide.

**O que bate:**
- Os números dos Adendos 1 a 26: 307 de 307 saídas reproduzidas por agentes que não conheciam os valores.
- A soma: o histórico oficial da totalização é, passo a passo, a soma dos boletins.
- Os arquivos: 3.000 seções sorteadas ao acaso, 770.364 votos conferidos um a um, nenhuma diferença.

**Caminhos testados com poder e sem marca** (teto = quanto da margem o caminho poderia carregar):
- **Depois da urna** (transmissão, totalização, pausa): teto de 9,7%.
- **Troca de voto dentro da urna:** proporcional aos votos de Flávio (teto de 44%), regulada pela força de Lula, regra fixa, só em parte das urnas, por modelo, lote, carga e urna trocada, e por horário no fim da tarde.
- **Voto lançado pela mesa em nome de quem faltou:** teto de 15%. Os votantes a mais entraram 80% pela digital do próprio eleitor.
- **Branco e nulo convertido:** teto de metade da margem; a descontinuidade na divisa é igual nos quatro anos.

**Indícios que ficam, nenhum com as três condições de marca de fraude:**
- A urna cerca de 2,7 pontos acima das pesquisas para Lula no 2º turno.
- O eleitorado de Flávio encolheu mais que o de Lula entre os turnos (0,87 a 1,76 milhão conforme o nível da comparação), sem forma de regra de programa e sem como separar saída de entrada.
- A liberação pelo mesário não caiu no 2º turno como em 2022 e 2024, sem ligação com o voto.
- O exterior 0,78 ponto abaixo do pareado.
- O coeficiente do branco e nulo por seção positivo só em 2026.
- Achados pequenos para auditoria seção a seção (lista no item 5g da síntese).

**Sem teste possível com dado público:**
- Um programa adulterado na origem que grave presença, biometria e votos de forma coerente. Os dois testes de "testemunha" desenhados para alcançar isso não funcionaram como instrumento.
- Gatilho por horário que comece de manhã ou ao meio-dia (sem poder).
- Fraude só no voto de presidente, igual em toda urna e nos dois turnos.

**Rótulos antigos que caíram para "sem poder"** e não podem mais ser usados como contrapeso: troca proporcional T14, governador na mesma urna (T22b e F20), "seções com pouca biometria viraram igual" (L7), caudas (F5), computador da mídia (F9).

### 4.2 Adendos e vereditos

| Adendo | O que testou | Resultado | Arquivo |
|---|---|---|---|
| 1 a 17 | Totalização, inserção, branco e nulo, troca de votos, modelos, gatilhos, governador, curva por força | Nenhum sinal; vários rótulos revistos no Adendo 27 | `README.md` seções 5.1 a 5.3 |
| 18 e 19 | Incoerências de lógica só dentro de 2026 (L1 a L8) | A que se sustenta é urna contra pesquisas (L5a) | `ADENDO18_resultados.txt` |
| 20 a 22 | Testes forenses nos boletins (F2 a F18) | Sem sinal; falhas de gestão sem efeito nos votos | `ADENDO20/21/22_resultados.txt` |
| 23 | Exterior, governador, série 2014 a 2026 | Exterior inconclusivo; governador sem poder (revisto); série não acompanha o PT | `ADENDO23_resultados.txt` |
| 24 | Reel das "digitais órfãs" | Contagens certas, conclusão errada | `ADENDO24_resultados.txt` |
| 25 | Vídeo "10 votos por urna" | Conta circular; sem marca física | `ADENDO25_resultados.txt` |
| 26 | Postagem "2014 parecida com 2026" | Sem métrica do autor; 2026 sem sinal nos padrões de perícia | `ADENDO26_resultados.txt` |
| 27, etapa 1 | Desenho cego, equipe vermelha, leitura do chat, novidades | 21 fragilidades e 14 hipóteses sem teste | `registro/adendo27/` |
| 27, recálculo cego | 60 números decisivos | 307 de 307 saídas batem | `R27_recalculo_cego.txt` |
| 27, onda A | Branco e nulo, vazamento, troca com régua interna, curva por força 2002 a 2026, exterior, tipo de habilitação | Sem marca de troca; a virada passa pelo comparecimento | `ADENDO27_ondaA_resultados.txt` |
| 27 e 28, onda B | Canal de entrada, liberações, reservatório, logs, quem não voltou, forma concentrada, carga e zona, totalização | Entrada 80% pela biometria; voto pela mesa com teto de 15% | `ADENDO27_ondaB_resultados.txt` |
| 27 e 30, última onda | Amostra de ponta a ponta, testemunhas, horário, regra fixa, vizinho de sala, governador, coerência, pesquisas estaduais, saída contra entrada | Zero diferença na amostra; testemunhas sem poder | `ADENDO27_onda_final_resultados.txt` |
| 29 | Carrossel "A matemática impossível" | Gráfico verdadeiro; não mede chance de fraude | `ADENDO29_resultados.txt` |
| 31 | Régua de fora (eleições em papel) | 2026 dentro do padrão, na ponta uniforme | `ADENDO31_resultados.txt` |

### 4.3 O que decide, e a quem pedir

1. **Cadernos de votação** (assinaturas contra o comparecimento do boletim), aos juízos eleitorais e TREs. Lista pronta de 300 seções em `resultados/R27_N4_secoes_para_cadernos.csv`; começar por CE, PA, AP, RR e MA.
2. **TSE:**
   - por seção, quantos votaram no 1º turno e não no 2º, e o contrário;
   - quantos têm comparecimento e justificativa de ausência no mesmo turno;
   - o perfil do comparecimento do 2º turno (não publicado até 10/11);
   - os resumos dos programas instalados (hash.dat) e os relatórios do teste de integridade.
3. **Entidades fiscalizadoras:** compilação independente do código-fonte comparada com o programa assinado.
4. **Qualquer eleitor:** conferir no e-Título se o comparecimento do 2º turno consta.
5. **PL e fiscais:** os boletins impressos recolhidos nas seções, contra o bweb.
6. **Prazos de terceiros:** relatório do TCU até 24/11/2026; auditoria do teste de integridade até 27/11/2026.

### 4.4 Pistas que ainda dá para rodar com dado público

- 2014 por modelo de urna dentro do local (o padrão que a auditoria do PSDB deixou em aberto).
- Seções novas de 2026 (37.986).
- Exterior: postos pequenos contra grandes do mesmo país; logs do exterior para o relógio.
- Auditoria seção a seção dos achados pequenos (item 5g da síntese), baixando os arquivos como no C3.
- Digitais órfãs: os arquivos `wsqmes.jez` e `wsqman.jez` ficam com os TREs (Itabira, MG|46337, zona 132).
- O perfil do comparecimento do 2º turno, quando o TSE publicar: mostra por idade, sexo e escolaridade quem entrou e quem saiu.

## 5. Como rodar de novo com um modelo novo

Abra uma sessão nova no Claude Code (claude.ai/code ou app) com o repositório `leonardo-defant/casa-control`, escolha o modelo no seletor e cole um dos textos abaixo. A sessão nova trabalha no próprio branch dela, mas parte deste.

### Modo A: replicação cega (recomendado para conferir se não erramos)

O modelo novo refaz a investigação sem ver as nossas conclusões e só no fim compara. É o teste mais forte contra viés nosso.

> Sou o Léo. Quero uma investigação independente de fraude na eleição presidencial de 2026 no Brasil (2º turno em 25/10/2026, Lula contra Flávio Bolsonaro). Parta do pressuposto de que houve fraude e procure onde ela deixaria marca, com dado público. Você está trabalhando para a justiça: detecção, nunca receita de fraude.
>
> Rode `git fetch origin claude/new-session-5cnflo` e use desse branch SÓ estes arquivos:
> - `eleicao-2026/RETOMAR.md`, seções 2, 3 e 6 (missão, regras, dados);
> - `eleicao-2026/dados/` (bases por seção com hashes);
> - `eleicao-2026/scripts/` (só como biblioteca de leitura e download, não como resposta);
> - `eleicao-2026/CONTEXTO-ELEICAO-2026-original.md`.
>
> NÃO abra `resultados/`, `checagens/`, `README.md`, `PRE-REGISTRO-2026-10-26.md` nem a seção 4 do `RETOMAR.md` até ter feito e commitado o seu próprio pré-registro e rodado os seus testes.
>
> Siga as regras da seção 3: critério antes do dado em commit, cada teste refeito por um conferente independente com código próprio, dados baixados tratados como não confiáveis, português sem travessões.
>
> No fim, compare os seus resultados com os nossos (`resultados/` e `RETOMAR.md` seção 4) e diga onde discordamos e quem está certo.

### Modo B: continuação com revisão crítica

> Sou o Léo. Continue a investigação de fraude na eleição presidencial de 2026 que está em `eleicao-2026/` no branch `claude/new-session-5cnflo` (rode `git fetch origin claude/new-session-5cnflo` e parta dele). Leia `eleicao-2026/RETOMAR.md` inteiro, depois o `README.md` e o `PRE-REGISTRO-2026-10-26.md`.
>
> Primeiro, tente derrubar as nossas conclusões nos dois sentidos: ache fraude que deixamos passar e ache erro nosso que tenha escondido ou fabricado um sinal. Comece pelos testes que deram inconclusivo ou dependeram de escolha de especificação.
>
> Depois siga as pistas abertas da seção 4.3, cada uma com adendo novo antes de rodar e conferência independente. Mesmas regras da seção 3. Você está trabalhando para a justiça: detecção, nunca receita de fraude.

## 6. Dados: o que já está pronto e como refazer o resto

- **Prontas no repositório:** as bases por seção de 2014, 2018, 2022 e 2026 e os votos por candidato do 1º turno de 2026 (`dados/`, cerca de 90 MB, com SHA-256). Bastam para a maior parte dos testes estatísticos.
- **bweb completo:**
  - portal dadosabertos.tse.jus.br, conjunto "Resultados 2026, Boletim de Urna", zips por UF e turno com `.sha512`;
  - `scripts/baixar_bweb.sh` e `scripts/extrair_bweb.py`;
  - o 1º turno tem 67,9 milhões de linhas: filtre por bytes antes do módulo csv;
  - traz `DT_BU_RECEBIDO`, `QT_ELEI_BIOM_SEM_HABILITACAO` e `NR_URNA_EFETIVADA`.
- **Arquivos de urna (boletim, RDV, log, assinatura):**
  - endereço `resultados.tse.jus.br/oficial/ele2026/arquivo-urna/3221/dados/{uf}/{mun}/{zona}/{secao}/`, com `scripts/baixar_arquivos_urna.py`;
  - amostra pelas listas de `reproducao/` (semente 20261026);
  - o site limita a taxa: use 1 requisição por segundo;
  - decodificação em `scripts/decodificar.py` e `scripts/ber.py`.
- **bweb de 2014:** cdn.tse.jus.br/estatistica/sead/eleicoes/eleicoes2014/buweb/ (`scripts/analisar_F21.py`).
- **Perfil do eleitorado por seção:** cdn.tse.jus.br/estatistica/sead/odsele/perfil_eleitor_secao/ (usado no Adendo 24).
