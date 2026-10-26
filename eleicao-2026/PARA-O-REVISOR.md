# Auditoria do 2º turno presidencial de 2026: passagem para o revisor cético

Este documento entrega a pesquisa feita em 26/10/2026 a um revisor independente (Codex). O papel do revisor é tentar derrubar cada conclusão, nos dois sentidos: achar fraude que eu deixei passar e achar erro meu que fabrique ou esconda um sinal. Tudo o que está aqui pode e deve ser refeito a partir do código e dos dados.

Estado na última consulta ao portal de dados abertos do TSE (26/10/2026, 15h47 UTC): os boletins de urna do 2º turno em formato aberto (bweb) ainda não estavam publicados; o pacote tinha só os 56 arquivos do 1º turno, atualizados em 06/10. Os testes rodaram numa amostra de arquivos de urna baixados um a um do site de resultados.

## 1. A pergunta

O Léo (dono da pesquisa) acredita que a eleição foi fraudada. A tese principal dele: o programa da urna estaria corrompido, com um desvio programado antes, e teria "errado a mão" no 2º turno (Lula ganhou cerca de 10,4 milhões de votos entre os turnos; Flávio, cerca de 3,7 milhões). Variante inicial: votos brancos e nulos de presidente registrados como votos em Lula. Ele parte do pressuposto de que a urna não é confiável e pediu uma "caçadora cética da verdade", sem suavizar resultados em nenhuma direção.

Resultado oficial do 2º turno (soma dos 28 arquivos por UF e exterior do TSE): Lula 64.256.232, Flávio 59.826.041, brancos 1.430.496, nulos 2.723.305, comparecimento 128.236.074. Margem de 4,43 milhões de votos.

Regras que segui:
1. Critério antes do dado, com exceções declaradas. Os critérios estão em commits com horário (`PRE-REGISTRO-2026-10-26.md`, adendos 1 a 13). Quatro testes viram parte do dado antes do registro:
   - T14: o Adendo 8 (12h57 UTC) veio depois de o coeficiente 0,056 (0,012) das 1.709 primeiras seções ter sido versionado (12h10), e o adendo diz isso. O limite de "sem sinal" (0,051) é o valor depois obtido com as 3.897.
   - T12: o Adendo 7 (12h20) veio depois de o erro de cada instituto no 2º turno de 2026 estar versionado em `erro_pesquisas_2t.txt` (11h53).
   - T20: a janela de 10 a 15/10 e duas regras de explicação saíram dos dados.
   - T30: a especificação R2 foi fixada depois de ver as 835 primeiras seções.
   Quando o registro estava errado, corrigi num adendo novo, dizendo o que já tinha sido visto.
2. Fato, indício, evidência e prova são coisas diferentes. "Sinal" é indício e pede cruzamento com outro teste independente.
3. Para cada teste: o que foi testado, o critério, o número, se apoia ou contraria a tese e o que fica sem teste.
4. Script reescrito só vale depois de reproduzir as referências de 2018 e 2022 do documento original.
5. Resultado da amostra é provisório; com o bweb completo, refaz-se com o mesmo critério.

## 2. Dados e como foram obtidos

| Dado | Fonte | Observação |
|---|---|---|
| bweb do 1º turno de 2026 | portal de dados abertos do TSE (CKAN), arquivos por UF | base por seção `secoes2026_1t.json.gz`, montada nesta sessão com `extrair_bweb.py` (fora do repositório, no scratchpad da sessão) |
| bases de referência de 2018 e 2022 | recebidas prontas, de um pacote anterior à sessão (`secoes2022.json.gz` com data 01h47 UTC e `secoes2018.json.gz` com data 10h34 UTC, antes do primeiro commit dos scripts) | origem e código de extração não documentados; `extrair_bweb.py` fixa a direita no 22 e não refaz a base de 2018, em que Bolsonaro é o 17 (a base existente tem os votos dele corretos) |
| votos por candidato no 1º turno de 2026 | mesmo bweb, `extrair_candidatos.py` | `candidatos2026_1t.json.gz` |
| arquivos de urna do 2º turno (boletim, RDV, log, assinatura) | `resultados.tse.jus.br/oficial/ele2026/arquivo-urna/3221/dados/{uf}/{mun}/{zona}/{secao}/` | o `-aux.json` de cada seção lista o hash e os arquivos; só arquivos listados foram pedidos |
| total oficial por UF e por município | `resultados.tse.jus.br/oficial/ele2026/6258/dados/...` | usado no T1 e na soma nacional |
| pesquisas | imprensa, com conferência em segunda fonte quando possível | `resultados/*_pesquisas_verificadas.txt` |

Cuidados:
- Todo dado baixado foi tratado como não confiável: pastas próprias, Python sempre com `-I`.
- O site de resultados limita a taxa (HTTP 429 da Akamai). O baixador (`baixar_arquivos_urna.py`) tem limitador global e recuo após 429. O padrão do código é 3 requisições por segundo; as levas registradas rodaram com TAXA de 0,9 a 1,5, mas a primeira tentativa do estrato M, numa versão anterior do baixador, rodou a 8,3 por segundo, com 33 erros.
- Nenhum caminho do TSE foi adivinhado. O caminho de 2022 no mesmo padrão (`ele2022/arquivo-urna/407/...`) respondeu 404 e não foi tentado outro.
- Os endereços de lista de revogação e de política das AC do TSE, citados nos próprios certificados, responderam 403 a partir deste ambiente.

Amostra do 2º turno (`sortear_amostra.py`, semente 20261026), desenhada em três estratos:
- **M:** 120 municípios inteiros.
- **L:** 1.500 locais de votação.
- **G:** metade dos locais das 6 UFs com 2º turno de governador (2.881 locais).

O download parou no limite de 2 horas da tarefa em segundo plano e não chegou ao estrato G. Ficaram 3.897 seções com boletim, em 741 locais (625 com 2 ou mais seções, os que entram nas regressões com efeito fixo de local):
- 823 seções de M: 14 dos 120 municípios, 13 completos.
- 3.062 seções de L: 476 dos 1.500 locais, todos completos, na ordem aleatória do sorteio.
- 12 seções de teste do AC.

As 835 seções com RDV, log e arquivo de assinatura são as 823 de M mais as 12 de teste. Os arquivos de assinatura dessas 835 vieram numa leva própria (Adendo 9). Depois vieram mais três levas:
- **Logs das outras 3.062 seções** (Adendo 12).
- **Arquivos de assinatura das outras 3.062** (Adendo 13), em andamento.
- **Extensão dirigida do T17** (Adendos 10 e 11):
  - 264 seções sorteadas entre os locais com modelos misturados;
  - todas as 1.335 seções dos 119 locais do país que têm urnas antigas e novas juntas.

## 3. Mapa do código (`scripts/`)

| Script | Função |
|---|---|
| `lib.py` | leitura das bases; `fe_ols` (efeito fixo por desvio da média do grupo, peso, erro agrupado CR1) |
| `ber.py`, `decodificar.py` | leitura genérica de BER; boletim (`ler_bu`), RDV (`ler_rdv`), log (`_linhas_log`, inclusive os .jez internos de contingência) |
| `extrair_bweb.py`, `extrair_candidatos.py`, `juntar.py` | montam as bases de 2026 a partir do bweb (as de 2018 e 2022 não saíram deles) |
| `somar_oficial.py` | soma uma base pronta por UF e Brasil e compara com o total oficial |
| `baixar_arquivos_urna.py`, `sortear_amostra.py`, `analisar_amostra.py` | download, sorteio e decodificação da amostra; T1, T2, T3 e validação do decodificador |
| `modelos.py` | modelo da urna pela faixa do número de série (conferido contra o enumerado do arquivo de assinatura em 835 de 835) |
| `analisar_modelos.py`, `analisar_bn_secao.py`, `analisar_gov.py`, `analisar_zeros.py`, `analisar_pres_gov_nivel.py` | testes da seção 7 do documento original, T4 e T5 |
| `analisar_fluxos.py`, `analisar_fluxo_regressao.py` | T7, T8 e T14 |
| `analisar_biometria.py`, `analisar_biometria_tarde.py` | T9 e T21(c) |
| `analisar_software.py`, `analisar_pendencias.py` | T10 e T20 |
| `verificar_assinaturas.py`, `ed521.py`, `verificar_ac_ecdsa.py` | T18 |
| `analisar_nulos_rdv.py` | T19 |
| `analisar_maquina.py` | T17 |
| `analisar_gatilhos.py` | T30 |
| `analisar_pesquisas_totais.py` | T33 |
| `rodar_2026.sh` | rotina parcial para quando o bweb do 2º turno sair (sai com código 2 enquanto não sai). Ela baixa o bweb, monta a base, compara a soma do Brasil e de cada UF com o total oficial e roda T4, T5 do 2º turno e os testes da seção 7 do documento original. T7, T8 e T14 com o bweb rodam à parte. O T15 completo, T16, T21 a T23 (exceto o T21(c)), T27 a T29, T31 e T32 ainda não têm script. |

## 4. Resultados por teste

Veredito pelo critério pré-registrado. "Amostra" quer dizer provisório.

| Teste | O que pegaria | Resultado | Veredito |
|---|---|---|---|
| T1 soma dos boletins contra o total oficial | alteração na totalização | 13 municípios inteiros (797 seções; 10 no T1 original e 3 de AL acrescentados depois): diferença zero em todos os campos | sem sinal (0,16% das seções do país) |
| T2 RDV contra boletim | registro interno incoerente | 835 seções, candidato a candidato: zero diferença | sem sinal |
| T3 log: horários e ritmo | voto fora de hora, sem habilitação, rajadas | 3.897 seções: zero em A1 a A5 | sem sinal |
| T4 zeros de branco+nulo | conversão total em parte das urnas | só referências calibradas; 2026 2º turno depende do bweb | pendente |
| T5 presidente contra governador (1º turno) | conversão de branco/nulo recorrente, que já agiria no 1º turno | beta 2026 0,348; 2018 0,429; 2022 0,293 (2026 é 1,19 vez o menor) | sem sinal para conversão no 1º turno; não testa conversão só no 2º (T5 do 2º turno depende do bweb) |
| T6 branco/nulo declarado contra registrado | branco/nulo "sumido" | declarado menos registrado, 2026 menos o maior de 2018 e 2022: Datafolha +0,35, CNT/MDA +1,55, Quaest +3,35, AtlasIntel +1,15 (Quaest e AtlasIntel só com 2022); média +1,60 (com o "não sabe" redistribuído, +1,54); só Datafolha e MDA, que têm os três anos, +0,95 | inconclusivo; sem sinal só com Datafolha e MDA, a 0,05 do limite |
| T7 ganho além do bolo da seção | troca de voto ou de eleitor | 10,57% das seções e 1,71% do ganho (2022 no país: 5,27% e 1,09%; troca simulada de 2%: 12,43% e 2,09%). Robustez posterior, 2022 nas mesmas seções da amostra: 7,06% e 1,69% | inconclusivo: (a) passou 5,3 pontos da referência nacional (3,5 da referência nas mesmas seções), (b) só 0,6 (0,02 nas mesmas seções) |
| T8 fluxo por seção | coeficiente fora de 0 a 1 | Lula recebeu 0,53 dos outros, 0,667 da queda de branco/nulo, 0,605 do aumento do comparecimento; todos dentro de 0 a 1 | sem sinal |
| T9 biometria dos eleitores a mais | votos em nome de faltosos | 3.873 seções. Dentro do local, 0,139 (0,016) dos eleitores a mais foram sem biometria, perto da base de 12,2%. Em números brutos, 22% das habilitações a mais (4.583 de 20.651) foram sem biometria. Ganho de Lula por habilitação a mais: 0,56 sem biometria e 0,51 com | sem sinal pelo critério; o excesso bruto de habilitações sem biometria fica para o T21 (ver seção 7) |
| T10 programa e mídia entre os turnos | programa trocado | 3.897 urnas: mesma versão 10.23.0.0, nenhum componente novo; 1 verificação de assinatura com ERRO, em 22/09, na preparação (urna recusou a mídia, religada e verificada com sucesso; tudo SUCESSO nos dois dias de votação) | bandeira vermelha pelo critério registrado em 1 urna (pb/21873/0033/0098); o log mostra a causa, mas aceitar isso como explicação é leitura posterior, não estava no registro |
| T11 pesquisa: presidente contra governador na mesma amostra | fraude só no presidente | AtlasIntel, 6 UFs: D médio -1,47 | sem sinal |
| T12 mudança do erro de cada instituto entre turnos | erro anômalo em 2026 | -1,32 em média (Datafolha, MDA, PoderData, AtlasIntel); sem o PoderData, cuja pesquisa "final" de 2018 foi de 10 dias antes: -3,65 (3 institutos); com os 6 sem o PoderData: -2,36. A mudança média de 2026 (-5,70) é a mesma de todas as históricas (-5,39) | sem sinal no conjunto registrado; sinal sem o PoderData; frágil |
| T13 teto de Lula pela rejeição | voto acima do possível | Lula abaixo do próprio teto nos 8 institutos | sem sinal |
| T14 marca de troca de votos | troca proporcional dos votos de Flávio | 0,0507 (0,0070), intervalo de 0,037 a 0,064; limite de "sem sinal" era 0,051. Referências sem troca: país 0,006 a 0,041; mesmas seções da amostra (robustez posterior) 2022 Bolsonaro 0,048 (0,007), 2018 Haddad 0,010 (0,009) | sem sinal no limite; a leitura depende da referência (ver seções 5 e 7) |
| T17 modelo da urna no mesmo prédio | troca restrita às urnas novas ou a um modelo | antigas menos novas nos 119 locais: -0,016 (0,140); seria preciso cerca de 2,2. Um modelo só: UE2020 contra UE2022 -0,04 (0,22) e UE2013 contra UE2015 +0,34 (0,24), efeito mínimo detectável 0,61 e 0,67 | sem sinal para antigas contra novas (vale para SP); sem poder para um modelo só |
| T18 assinatura digital | arquivo trocado depois da urna | 835 seções, 9.185 arquivos e 835 blocos válidos; SHA-256 do vsc igual ao hash do aux em 835 (o aux e o vsc vêm do mesmo servidor, então isso é coerência, não verificação independente) | sem sinal (as 3.062 restantes em download) |
| T19 conteúdo dos nulos | candidato contado como nulo | zero nulos de presidente digitados 13 ou 22 em 5.087 | sem sinal no item forte; (b) sem referência |
| T20 pendências do T10 | carga ou programa fora do oficial | 3.897 urnas: 426 com pendência (438 itens). 103 fecham com as regras já usadas nas 835 primeiras. 323 só fecham com 2 regras definidas depois de ver os dados (sessão de geração da zona e computador da própria zona), que não são o evento de substituição, contingência ou recarga exigido. A janela de 10 a 15/10 também saiu das 835 primeiras. Votáveis 13 e 22 em 3.897 boletins | em aberto pelo critério literal; não é sinal, porque não há calendário oficial que torne as datas "fora do oficial"; faltam as atas de carga |
| T30 gatilho por horário | troca depois de certa hora | 3.874 seções: +5,0 (1,4) às 14h e +11,3 (2,7) às 16h passam valor e z, mas o placebo falha (+16); com local e fatia do 1º turno: +1,1, +1,1 e +4,1 (2,1), z 1,95 às 16h | sem poder pelo critério; leitura de composição, às 16h no limite (ver seção 7) |
| T21(c) biometria no fim do dia | inserção tardia | das 15h30 em diante, sem biometria 12,1% no 1º turno e 12,6% no 2º (+0,49 na mesma urna); ganho de Lula igual por habilitação tardia com e sem biometria (0,47) | descritivo |
| T30 gatilho por contagem | troca depois de N votos | -1,4 a -2,5 (negativos) | sem sinal para N de 100 a 200; para N = 50, inconclusivo pelo tamanho (-2,5, negativo) |
| T33 pesquisas em votos totais | separar conversão de troca | Flávio abaixo do que as pesquisas davam em 8 de 9 institutos, 1,6 ponto em média além do histórico; só 1 passou de 3 (a AtlasIntel, ambígua), e o critério pedia 5 | inconclusivo; a direção contra a tese "só conversão de branco/nulo" é só descritiva |

Detalhes e números completos: `resultados/ADENDO9_resultados_amostra.txt` (T17 a T33) e os arquivos citados em cada linha.

## 5. Leitura de conjunto

O que os testes já excluem ou enfraquecem muito, cada um pela sua via:
- **Alteração depois da urna:** totalização (T1) e arquivo trocado (T18).
- **Troca concentrada num modelo de urna:** T17, antigas contra novas sem sinal nos 119 locais (113 em SP).
- **Conversão de branco/nulo como explicação única:**
  - Para a conversão decidir sozinha, o branco+nulo verdadeiro teria de ser de cerca de 6,7% do comparecimento, contra 3,24% registrados. (Os 4,15 milhões registrados serem menos que a margem não contraria a conversão, porque o voto convertido sai do branco/nulo.)
  - A queda entre turnos (32%) está dentro da faixa de 2002 a 2014, quedas de 22% a 42% (`historico_comparecimento_bn.txt`). Mas o branco/nulo subiu entre os turnos em 2018 (+9%) e em 2022 (+4%), e 2026 teve o maior aumento de comparecimento (+1,86 ponto) e de válidos sobre o eleitorado (+3,01) da série.
  - T5 e T8 sem sinal. T6 inconclusivo: média dos institutos 1,60; sem sinal só com Datafolha e MDA (0,95).
  - T33 é inconclusivo: só 1 de 9 institutos teve Flávio 3 pontos ou mais abaixo, e o critério pedia 5. A direção, em 8 de 9, sugere que parte do erro das pesquisas está nos votos de Flávio, não só no branco/nulo, mas isso não basta para excluir a conversão.
- **Votos em nome de faltosos em grande escala:** T9 e T3, ambos com as 3.897 seções.
- **Programa ou carga fora do oficial:** T10 e T20 nas 3.897 urnas enfraquecem esse cenário, com ressalvas.
  - O T10 tem 1 bandeira vermelha pelo critério registrado, com a causa no log.
  - Das 426 urnas com pendência, 323 só fecham com duas regras definidas depois de ver os dados.
  - Até as atas de carga, é leitura provisória, não exclusão.

O que continua aberto:
- **Troca uniforme pequena e espalhada,** do tamanho do erro das pesquisas. É o ponto aberto mais importante.
  - T7 é inconclusivo, e o T14 ficou no limite.
  - Pela base de 2022, o T14 equivale a cerca de 1,4% de "troca", com intervalo de 0% a 2,8%, que exclui os 3,6% que decidiriam a eleição.
  - Pela base de 2018 (Haddad), equivale a cerca de 4,5%, com intervalo de 3,1% a 5,9%: o ponto passa dos 3,6% e o intervalo os inclui.
  - O coeficiente de 2026 (0,051) fica acima de todos os valores sem troca das referências nacionais (0,006 a 0,041).
  - Nas mesmas seções da amostra (robustez escolhida depois de ver os dados), o de quem ganhou terreno em 2022 (Bolsonaro, sem troca suposta) é 0,048 (0,007), quase igual ao de Lula em 2026. O de Haddad em 2018 nessas seções é 0,010 (0,009).
  - Se a base certa for 2022, a marca de troca some. Se for 2018, ela fica em cerca de 4%. A pergunta, em termos simples: o padrão de ganho de Lula em 2026 parece o de Bolsonaro em 2022 (que, pela tese, não teria fraude a favor dele) ou o de Haddad em 2018?
  - Isso inclui eleitores reais que votaram em Flávio no 1º turno e em Lula no 2º, e a troca de eleitores entre os turnos.
  - Esses dois testes não separam isso de fraude.
  - O T16 (cauda inferior por UF, com o bweb) é o teste desenhado para isso.
- **Troca concentrada num lote ou em urnas de contingência:**
  - Nenhum teste trata de lote.
  - No T17, a contingência no 2º turno (2 locais) e a urna trocada entre os turnos (37 locais) estão sem poder.
  - O T7, que pegaria saltos locais, é inconclusivo.
  - O T26 (teste de integridade) depende de dado externo.
- **Testes que dependem do bweb:** T4 no 2º turno, T5 no 2º turno, T15, T16, T21 a T23, T27 a T29, T31 e T32, e os testes da seção 7 do documento original (modelo, bn_secao, governador).
- **Testes que dependem de dado externo:**
  - T24: QR dos boletins impressos coletados por fiscais.
  - T25: caderno de votação físico e óbitos.
  - T26: seções sorteadas para o teste de integridade e relatórios oficiais.

O que aponta na direção da tese, lido junto (nenhum é sinal pelo critério registrado; juntos pedem atenção):
- **T7(a):** 10,6% das seções com ganho de Lula acima do bolo, 5,3 pontos acima da referência nacional (3,5 acima da referência nas mesmas seções).
- **T14:** no limite, e acima de todas as referências nacionais sem troca.
- **T12 sem o PoderData:** -3,65, sinal pelo critério.
- **T6 com os institutos além do Datafolha:** média de 1,60, inconclusivo.
- **T30 sem controles:** positivo em todos os cortes e especificações.
- **Biometria:**
  - T9 bruto: 22% das habilitações a mais sem biometria, contra a base de 12,2%. No país, o excesso seria da ordem de 265 mil, numa extrapolação grosseira da amostra.
  - T21(c): +0,49 ponto (0,13) de habilitações sem biometria no fim do dia.
- **Leitura:**
  - São muitos testes; olhando só os que ficaram perto do limite, alguns cairiam do lado da tese por acaso.
  - Contra isso, as explicações inocentes de cada um estão listadas nas linhas da tabela, e os testes desenhados para separar as duas leituras ainda dependem do bweb: T16, T21 e o T14 com todas as seções.
  - Em escala, nenhum desses números chega sozinho aos 2,2 milhões de votos trocados ou aos 4,43 milhões acrescentados que decidiriam a eleição.
  - A exceção é o T14 lido pela base de 2018.

O que não tem teste com dado público:
- **Lógica maliciosa dentro do programa oficial assinado, agindo por igual em todas as urnas.** Nos resultados ela se confunde com troca real de eleitores. As barreiras são a inspeção de código e o desenho do teste de integridade, que não deixam rastro em dado público.
- **Linhas de base contaminadas:** uma alteração constante em todos os anos não aparece em nenhuma comparação relativa.
- **Se cada voto gravado é o que o eleitor digitou:** o voto é secreto e não há comprovante individual.
- **Compra de votos e coação** de eleitores reais.

Fatos de contexto já checados:
- **Prorrogação do horário:** a decisão de Zanin foi divulgada às 17h03 e só valeu para as seções ainda abertas. O TSE suspendeu a totalização às 17h06 (Agência Brasil), com 1.225 seções apuradas, e a retomou às 19h. Nos logs da amostra (3.897 seções, em hora de Brasília):
  - 236 seções tiveram voto depois das 17h e só 16 depois das 17h05.
  - 38 encerraram depois das 17h30 e 7 depois das 18h.
  - O último voto foi às 18h37 (RJ 60011, zona 7, seção 132), e 4 seções encerraram por volta das 19h (3 no RJ 60011 e 1 em SP 71072).
  - O "99,8% fecharam às 19h" do documento original é a hora de envio dos boletins, não de encerramento.
- **Erro médio das pesquisas no 2º turno:**
  - 2026: +2,63 pontos a favor de Lula.
  - 2022: -1,18.
  - 2018: -0,20.
  - Veritá e Gerp, as que mais acertaram o 1º turno, foram as que mais erraram o 2º (+3,34 e +3,79).
- **A conta "Lula precisaria de 99% de quem entrou":** com o mesmo método, Bolsonaro precisaria de 237% em 2022. A conta falha nos dois anos (`historico_comparecimento_bn.txt`, `transferencia_2022_x_2026.txt`).

## 6. Erros meus que foram corrigidos (para o revisor ver onde eu já errei)

- **Decodificador:**
  - Lia mal o voto nulo sem dígitos (tipo 6 do RDV).
  - Não lia o log interno das urnas de contingência.
  - Não filtrava o cargo.
  - Corrigido e validado contra o bweb do 1º turno: 80 de 80 seções idênticas.
- **Alarme falso de "voto antes da abertura":** a palavra "computado" casava com "computador". Corrigido.
- **T4:** o estimador original era viesado. Passou a ser calibrado por simulação nula (Adendo 6).
- **T17:** a leitura preliminar de -3,3 pontos vinha de um único prédio. Só 119 locais no país têm urnas antigas e novas juntas (Adendo 11).
- **Revisão adversarial independente (19 agentes):**
  - T20 tinha 21 pendências, não 20, e as regras de explicação estavam frouxas.
  - O placebo do T30 tinha uma covariável fora do registro.
  - Os pares do T17 eram "sem poder", não "sem sinal".
  - O verificador do T18 podia pular arquivos em silêncio.
  - Nenhum teste passou a sinal. Os pares de um modelo só do T17 mudaram de rótulo, de "sem sinal" para "sem poder". Tudo está corrigido e listado no fim de `ADENDO9_resultados_amostra.txt`.
- **Conferência independente deste documento (25 agentes, cerca de 575 itens):**
  - Os erros foram corrigidos nesta versão:
    - o T6 era inconclusivo, não "sem sinal";
    - a amostra tem 741 locais, não 625, e não chegou ao estrato G;
    - o "último voto às 17h03" e a "pausa às 17h20" estavam errados;
    - as bases de 2018 e 2022 vieram prontas;
    - o T14 pela base de 2018 passa dos 3,6%, não "se aproxima";
    - o T12 é frágil;
    - as exceções à regra do pré-registro não tinham sido declaradas;
    - "lote ou contingência" estava dado como excluído sem teste.
  - Os relatórios completos das duas revisões estão em `reproducao/revisoes/` (JSON; os caminhos citados são do ambiente desta sessão).

## 7. Onde eu posso estar errado (comece por aqui)

1. **Linha de base do T14 e do T7.** É o ponto mais importante.
   - Sem arredondar, o coeficiente de 2026 é 0,0507 (0,0070), com intervalo de 0,037 a 0,064.
   - Equivale a cerca de 1,4% de troca sobre a base nacional de 2022 (topo do intervalo, 2,6%) e a cerca de 4,5% sobre a de 2018 (topo, 5,8%).
   - Pela base de 2018, o ponto passa dos 3,6% que decidiriam a eleição.
   - Um revisor pode argumentar que a base certa é a de 2018, quando quem ganhou terreno também era o PT.
   - Contra-argumentos:
     - nas mesmas seções da amostra, Bolsonaro em 2022 dá 0,048, igual a 2026;
     - em 2026 os eliminados (Cury, Renan Santos, Caiado) são outros, e a composição muda o coeficiente.
   - O primeiro contra-argumento é uma robustez escolhida depois de ver os dados. O segundo não está provado.
   - As calibrações por troca simulada (Adendos 4 e 8) foram rodadas na sessão, mas o código delas não está versionado. Ele precisa ser reescrito para conferir.
2. **T7 é formalmente inconclusivo,** não "sem sinal". A parte (a), 10,6% das seções com excesso, passou 5 pontos da referência.
3. **T17 vale para SP:** 113 dos 119 locais estão lá. Uma alteração restrita a outra UF não aparece.
4. **T30 por horário:**
   - A leitura de composição (quem vota mais tarde já era mais Lula) usa a especificação R2.
     - Ela foi fixada depois de ver as 835 primeiras seções.
     - Foi fixada antes da rodada com as 3.874.
   - Na rodada com todas as seções:
     - Às 14h e às 16h, a inclinação sem controles passa o valor e o z do critério de sinal. Só o placebo em nível barra o sinal.
     - Às 16h, R2 dá +4,1 (2,1), com z de 1,95, a 0,01 do limite da regra de composição.
   - O efeito máximo plausível às 16h é de cerca de 0,2 ponto, pequeno demais para decidir.
   - Um revisor deve propor um placebo melhor que o nível do 1º turno.
5. **T18:**
   - A cadeia até a raiz do TSE não foi verificada.
   - Para as urnas antigas, mostrei que os 392 certificados conferem com uma única chave de AC.
   - A impressão digital SHA-256 da chave é 5d4c7e3a00234e6ee1400c07730f16402b775e7a326a660dba71c3556722260e. Alguém no Brasil deve compará-la com o certificado da AC URNA publicado pelo TSE.
   - Para as urnas novas (Ed521), a chave da AC não pode ser recuperada.
   - A variante Ed521 foi identificada por tentativa. Ela verifica tudo e o controle negativo rejeita tudo, mas não há especificação publicada à mão.
6. **Amostra:**
   - São 741 locais (625 com 2 ou mais seções).
   - Vêm 823 seções de 14 municípios do estrato M, 3.062 de 476 locais do estrato L e 12 seções de teste do AC. O estrato G não entrou.
   - Alguns municípios pesam muito: SP 71072 tem 262 seções, MG 46337 tem 277 e BA 34193 tem 208.
   - As 835 seções com RDV, log e assinatura não são aleatórias: são os municípios do M baixados primeiro, mais as 12 de teste.
   - Os testes por seção usam efeito fixo de local. Mesmo assim, comparar 2026 (amostra) com 2018 e 2022 (país) mistura bases diferentes. Por isso as referências nas mesmas seções importam (`resultados/T7_T14_referencias_mesmas_secoes.txt`).
   - 6 seções da lista ficaram só com o índice, sem boletim.
7. **Pesquisas:**
   - Os números vêm da imprensa, não dos PDFs registrados no TSE.
   - Vários totais são ambíguos (indecisos somados a branco/nulo).
8. **Modelo da urna pela faixa de série:** conferido contra o arquivo de assinatura nas 835. Nas demais seções é inferido.
9. **T20:**
   - 323 das 426 urnas com pendência só fecham com duas regras criadas depois de ver os dados.
   - A própria janela de 10 a 15/10 saiu das 835 primeiras urnas.
   - Sem as atas de carga, não dá para dizer se as mídias geradas entre 16 e 24/10 seguiram o calendário oficial de cada zona.
10. **T10:** a falha de verificação de assinatura de 22/09 é bandeira vermelha pelo critério registrado. Aceitar a explicação do log é leitura posterior.
11. **T6 e T12:** os dois dependem de quais institutos entram.
    - T6 só dá "sem sinal" com o Datafolha.
    - T12 só dá "sem sinal" com o PoderData, cuja pesquisa de 2018 foi feita 10 dias antes da eleição.
    - Os números das pesquisas vêm da imprensa. T6, T11, T12 e T13 não têm script próprio: as contas estão em `resultados/T11_T12_T13.txt` e `pesquisa_externa_verificada.txt`.
12. **Biometria (T9 e T21c):**
    - Em números brutos, houve mais habilitação sem biometria no 2º turno.
    - Uma explicação inocente possível: quem costuma faltar tem menos cadastro biométrico. Ela não foi testada.
    - O teste nacional (T21, com o bweb e a referência de 2022) é o que decide.
13. **T4:** o limite calibrado fica alto por causa do Rc0 de 2018 (1,879); o sinal exige Rc0 acima de 2,03, contra 1,21 a 1,22 nas outras referências. Um Rc0 de 1,9 em 2026 sairia "sem sinal". Além disso, `T4_referencias.txt` começa com um erro de execução de uma versão anterior; vale `T4_referencias_calibradas.txt`.
14. **T30:**
    - O fuso por UF erra o oeste do AM (UTC-5) e Fernando de Noronha.
    - O placebo também falha em R1, e R2 não tem placebo.
    - O limite de 1,96 para "perder significância" foi fixado depois.
15. **A conta dos 237%:** usa a transferência declarada no PoderData em 2022 e na Quaest em 2026, institutos diferentes.
16. **Ordem entre dado e critério:**
    - O registro inicial diz que uma seção do AC já tinha sido decodificada.
    - A base parcial unida (11h23 UTC) é anterior ao Adendo 4 (11h34 UTC).
    - As datas dos arquivos estão em `reproducao/datas_dos_arquivos.txt`, e os commits estão no ramo `claude/new-session-5cnflo` do repositório `leonardo-defant/casa-control`.

## 8. Como reproduzir

Arquivos de apoio:
- `reproducao/`:
  - listas de seções (a amostra de 3.897, as 835 com RDV e log, e as duas extensões do T17);
  - estratos e ordens de sorteio;
  - logs de download;
  - datas dos arquivos;
  - versões do ambiente (`ambiente.txt`: Python 3.13, numpy 2.5, scipy 1.18, cryptography 50).
- `CONTEXTO-ELEICAO-2026-original.md`: o documento original da conversa de 25/10, com os critérios da seção 7 e as referências que a regra 4 manda reproduzir.

Passos:
1. **Bases.**
   - A do 1º turno de 2026 sai de `python3 -I scripts/extrair_bweb.py 1 secoes2026_1t.json.gz <zips bweb_1t_*>`.
   - Os votos por candidato saem de `python3 -I scripts/extrair_candidatos.py candidatos2026_1t.json.gz <zips>`.
   - As de 2018 e 2022 vieram prontas e não se refazem com estes scripts.
2. **Amostra do 2º turno.** Use as listas de `reproducao/` (a ordem real de download foi o prefixo dessas listas). Para cada lista, rode `TAXA=1.0 python3 -I scripts/baixar_arquivos_urna.py 3221 <lista> <pasta> <tipos> 2`, onde os tipos são bu, rdv, log ou vota. As levas foram:
   - M10 com bu, rdv e log;
   - L só com bu;
   - os logs das 3.062 por `amostra_2t_3897_secoes.txt` menos as 835;
   - os vsc das 835 e depois os das 3.062.
3. **Decodificação, T1, T2 e T3.** Rode `python3 -I scripts/analisar_amostra.py <pasta_2t> <pasta_1t> secoes2026_1t.json.gz <lista_municipios|-> <saida>`. Ela gera:
   - `secoes2026_2t_amostra.json.gz`, só o 2º turno;
   - `T3_logs.json`.
   - Já `secoes2026_amostra.json.gz`, com os dois turnos unidos, sai de `scripts/juntar.py`.
   - Atenção: `analisar_amostra.py` e `somar_oficial.py` fixam o arquivo de certificados do ambiente (`/root/.ccr/ca-bundle.crt`); fora dele, troque pelo padrão do sistema.
4. **T7, T8 e T14.** Rode `python3 -I scripts/analisar_fluxos.py <secoes_dois_turnos> L --chaves <lista>` e `python3 -I scripts/analisar_fluxo_regressao.py <secoes_dois_turnos> L --chaves <lista> --candidatos candidatos2026_1t.json.gz --grupos 'Cury:70;Renan:14;Caiado:55;Zema:30'`. (O exemplo no cabeçalho do script foi corrigido: Renan Santos é o 14 e Zema o 30.)
5. **T9 e T21(c):** `scripts/analisar_biometria.py` e `scripts/analisar_biometria_tarde.py`.
6. **T10 e T20.** Primeiro `python3 -I scripts/analisar_software.py <pasta_2t> T10_software.json`, depois `python3 -I scripts/analisar_pendencias.py <pasta_2t> T10_software.json secoes2026_1t.json.gz secoes2026_2t_amostra.json.gz`.
7. **T18:** `python3 -I scripts/verificar_assinaturas.py <pasta_2t>` e `python3 -I scripts/verificar_ac_ecdsa.py <pasta_2t>`.
8. **T19:** `python3 -I scripts/analisar_nulos_rdv.py <pasta_2t> secoes2026_1t.json.gz candidatos2026_1t.json.gz secoes2026_2t_amostra.json.gz`.
9. **T17:** `python3 -I scripts/analisar_maquina.py secoes2026_1t.json.gz secoes2026_2t_amostra.json.gz <T3_logs.json das 835> --extensao_pares <pasta das 264> --extensao_contraste <pasta das 1.335>`.
10. **T30:** `python3 -I scripts/analisar_gatilhos.py <pasta_2t> secoes2026_1t.json.gz secoes2026_2t_amostra.json.gz secoes2022.json.gz [--chaves amostra_835_com_rdv_log.txt]`.
11. **T33:** `python3 -I scripts/analisar_pesquisas_totais.py`.
12. **Quando o bweb do 2º turno sair:** `DADOS=<pasta das bases> TRAB=<pasta de trabalho> ./rodar_2026.sh` (rotina parcial; ver a seção 3).

Sem script versionado:
- T6, T11, T12 e T13 (contas sobre os arquivos de pesquisas);
- as calibrações por troca simulada do T7 e do T14;
- os controles negativos do T18 e a busca da variante Ed521;
- a conferência do modelo pela faixa contra o arquivo de assinatura;
- a frota do 1º turno, que é calculada dentro de `analisar_maquina.py`.

As bases e os arquivos de urna não estão no repositório, por tamanho (cerca de 1 GB). Todos vêm de fontes públicas do TSE pelos caminhos acima.

## 9. Pendências

1. Quando o bweb do 2º turno sair, rodar `rodar_2026.sh` e os testes que dependem dele, com os critérios já registrados.
2. Comparar a impressão digital da chave da AC URNA com o certificado publicado pelo TSE.
3. Obter as atas de carga (T20), as coletas de QR dos fiscais (T24), o caderno de votação e os óbitos (T25) e os relatórios do teste de integridade (T26).
