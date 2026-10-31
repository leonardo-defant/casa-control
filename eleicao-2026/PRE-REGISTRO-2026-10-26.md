# Pré-registro dos testes novos (26/10/2026, manhã, horário de Cuiabá)

Este arquivo foi escrito e versionado no git **antes** de rodar os testes abaixo nos dados de 2026. O horário do commit é a prova. Os critérios da seção 7 do CONTEXTO-ELEICAO-2026.md continuam valendo como estão; aqui só entram os testes que ainda não tinham critério.

Situação no momento do registro:
- Boletins (bweb) do 2º turno de 2026 ainda não publicados no portal de dados abertos (só os 28 do 1º turno, de 06/10).
- Os arquivos por seção do 2º turno (`-bu.dat`, `-rdv.dat`, `-log.jez`) estão acessíveis no site de resultados pelo caminho `/arquivo-urna/3221/dados/{uf}/{mun}/{zona}/{secao}/{hash}/{arquivo}`, com o hash lido do `-aux.json` da seção (mesmo padrão de 2022). Uma seção do Acre (01074, zona 4, seção 1) foi baixada e decodificada para validar o formato. Nenhum outro dado do 2º turno por seção foi olhado.
- A parte 1 do pacote (código e base do 1º turno de 2026) não chegou nesta sessão. Os scripts estão sendo reescritos e só serão usados depois de reproduzirem os números de referência de 2018 e 2022 do documento.

## Regras gerais

1. Fato confirmado, indício, evidência e prova são coisas diferentes. Um "sinal" abaixo é indício e pede cruzamento com outro teste independente.
2. Para cada teste: o que foi testado, o critério, o número, se apoia ou contraria a tese e o que fica sem teste.
3. Se um script reescrito não reproduzir a referência do documento, o teste correspondente não é relatado como resultado até a diferença ser explicada.
4. Resultados da amostra do 2º turno são provisórios. Quando o bweb completo sair, o teste é refeito com todas as seções e vale o resultado completo, com o mesmo critério.

## T1. Soma dos boletins da amostra contra o total oficial por município (critério 1 da seção 7)

- Para os municípios baixados por inteiro: soma, seção por seção, de votos no 13, no 22, brancos, nulos e comparecimento nos `-bu.dat`, contra o arquivo oficial do município no site de resultados (`{uf}{mun}-c0001-e006258-u.json`).
- **Evidência forte de fraude na totalização:** qualquer diferença que não seja explicada por seção não instalada, seção anulada ou voto anulado registrado pelo TSE.
- **Limite:** não pega uma urna que já registre errado (o boletim sai do mesmo software).

## T2. RDV contra boletim (critério 4 da seção 7)

- Para cada seção da amostra com `-rdv.dat`: contagem de votos por cargo e tipo (nominal por número, branco, nulo) no RDV contra o `-bu.dat`.
- **Evidência forte:** qualquer diferença em qualquer seção.
- **Limite:** os dois arquivos saem do mesmo software; igualdade não descarta software que grave errado nos dois.

## T3. Logs da urna: horários impossíveis e ritmo não humano (critério 3 da seção 7)

Medidas por seção, contando só o dia da eleição e só a aplicação de votação:
- A1: número de mensagens "O voto do eleitor foi computado" diferente do comparecimento do boletim.
- A2: voto computado antes de "Urna pronta para receber votos" ou depois de "Inicio do Encerramento".
- A3: voto computado sem "Eleitor foi habilitado" desde o voto anterior.
- A4: intervalo entre "Eleitor foi habilitado" e "O voto do eleitor foi computado" menor que 2 segundos.
- A5: rajada de 10 ou mais votos seguidos com menos de 15 segundos entre um voto computado e o seguinte.

Referência: as mesmas medidas nos logs do 1º turno de 2026 (pleito 3220) das mesmas seções.
- **Bandeira vermelha:** qualquer A1, A2 ou A3 sem explicação documentada no próprio log (urna substituída, votação por cédula, reinício), ou taxa de A4 ou A5 no 2º turno acima de 3 vezes a do 1º turno nas mesmas seções e em mais de 0,5% das seções.
- **Limite:** um software malicioso poderia gravar log falso; o log não registra o conteúdo do voto.

## T4. Excesso de seções com branco+nulo de presidente zerado (pendência 8.2, item 8)

- Para cada seção com comparecimento de 50 ou mais: indicador de branco+nulo de presidente igual a zero (Z0) e menor ou igual a 1 (Z1).
- Esperado de cada seção: probabilidade de zero (ou de no máximo 1) numa beta-binomial com média igual à taxa de branco+nulo das outras seções do mesmo local de votação no mesmo turno (se o local só tiver uma seção, as outras seções do município) e superdispersão estimada pelo método dos momentos dentro de cada eleição e turno.
- Estatística: R = observados / esperados, para Z0 e Z1.
- Referências: 2018 (1º e 2º turnos), 2022 (1º e 2º turnos) e 2026 (1º turno).
- **Sinal a favor da tese (2º turno de 2026):** R acima do maior R das referências mais 0,15 **e** excesso (observados menos esperados vezes o maior R das referências) acima de 3 vezes a raiz desse esperado.
- **Sem sinal:** R até o maior R das referências mais 0,05.
- Entre os dois: inconclusivo.
- Escala: quando houver excesso, somar o branco+nulo esperado dessas seções para ver quantos votos uma conversão total nelas renderia, contra os 4,43 milhões necessários para inverter o resultado.
- **Limite:** só pega conversão total em parte das urnas. Conversão parcial e uniforme não gera zeros em excesso.

## T5. Versão "valor desconhecido", nos dois turnos: presidente contra governador no 1º turno (todas as 27 UFs tiveram governador no 1º turno)

Ideia: se a urna converte uma fração X do branco+nulo verdadeiro de presidente em voto no 13 em todas as eleições, a comparação entre turnos não vê nada, mas a relação, dentro do mesmo local de votação, entre o branco+nulo de presidente e o de governador na mesma urna encolhe pelo fator (1 menos X), e a relação entre a fatia do 13 e o branco+nulo de governador sobe.

- (a) Inclinação beta: branco+nulo de presidente (% do comparecimento) contra branco+nulo de governador (% do comparecimento), com efeito fixo do local de votação, peso pelo comparecimento, erro-padrão agrupado por local. 1º turno de 2018, 2022 e 2026.
- (b) Inclinação gama: fatia do 13 (% do comparecimento) contra branco+nulo de governador, mesma especificação.
- Conta da tese: para inverter o resultado do 2º turno, X teria de ser de pelo menos cerca de 52% (4,43 milhões contra 4,15 milhões registrados mais 4,43 milhões convertidos).
- **Sinal a favor da tese:** beta de 2026 abaixo de 0,6 vez o menor beta das referências e a mais de 3 erros-padrão abaixo dele.
- **Sem sinal:** beta de 2026 de pelo menos 0,85 vez o menor beta das referências.
- Entre os dois: inconclusivo.
- Gama é lido junto, como confirmação de direção, sem critério próprio.
- **Limites:** se X for igual nos três anos, este teste não vê nada (a tese diz que a fraude é recorrente). O comportamento muda de um ano para outro (2018 teve branco+nulo de 8,8%). Por isso só uma queda grande de beta conta.
- O mesmo teste é repetido no 2º turno nos estados com 2º turno de governador (2026: AC, AM, DF, ES, RN, TO; referências 2018 e 2022 com os estados que tiveram 2º turno de governador em cada ano), com o mesmo critério.

## T6. Branco/nulo declarado nas pesquisas contra o registrado (pendência 8.2, item 9)

- Para cada instituto com votos totais publicados na última pesquisa antes do 2º turno (Datafolha, Quaest, AtlasIntel e outros com série em 2018, 2022 e 2026): diferença entre o branco/nulo declarado e o registrado (% do comparecimento).
- Conta da tese: para inverter o resultado, o branco/nulo verdadeiro do 2º turno teria de ser de pelo menos 6,7% do comparecimento, contra 3,24% registrados, uma diferença de cerca de 3,5 pontos que não existiria em 2018 e 2022 se a fraude fosse nova, ou seria menor nesses anos.
- **Sinal a favor da tese:** diferença média de 2026 maior que a maior diferença média de 2018 e 2022 em 2,0 pontos ou mais, com o mesmo instituto e o mesmo tratamento de "não sabe".
- **Sem sinal:** até 1,0 ponto acima.
- **Limites:** pesquisa mede intenção, inclui quem não vai votar e tem erro próprio (em 2026 o erro de candidato foi de cerca de 2,7 pontos). Se a fraude também existisse em 2018 e 2022, a comparação entre anos perde força; nesse caso vale olhar o nível da diferença em cada ano.

## Adendo 1 (antes de ver qualquer dado do 2º turno por seção): calibração da pista do branco/nulo por seção

O script reescrito (`scripts/analisar_bn_secao.py`) reproduz exatamente as referências do documento: 2018 -0,060 (0,002), 2022 -0,071 (0,002), com 427.541 e 448.165 seções em 66.849 e 68.662 locais, e os outros dois coeficientes também batem (2018 +0,231 e -0,399; 2022 -0,075 e -0,177).

A calibração da seção 6.10 do documento (+0,15 para 1,82 milhão; +0,35 a +0,40 para 4,43 milhões) só se reproduz quando a conversão simulada é proporcional ao branco/nulo do **1º turno** da seção, que é a própria variável da regressão. A tese diz que a urna converte o branco/nulo digitado no **2º turno**. Simulando em 2022 uma conversão proporcional ao branco/nulo do 2º turno de cada seção, na mesma fração do comparecimento de 2026:

| Conversão (escala de 2026) | Proporcional ao BN do 2º turno (o que a tese descreve) | Proporcional ao BN do 1º turno (calibração do documento) | Mesma taxa por eleitor |
|---|---|---|---|
| 1,82 milhão | +0,061 (coeficiente vai a -0,009) | +0,153 | -0,005 |
| 4,43 milhões | +0,142 (coeficiente vai a +0,071) | +0,353 | -0,011 |

Consequências, registradas antes dos dados:
- O critério da seção 7 fica como está (sinal acima de +0,04 e a mais de 3 erros-padrão disso; sem sinal entre -0,07 e +0,04).
- Mas o patamar "compatível com inversão, +0,29 ou mais" está mal calibrado: na versão realista, uma conversão que inverte o resultado leva o coeficiente para cerca de +0,07, não +0,29.
- Um resultado "sem sinal" (entre -0,07 e +0,04) não descarta conversões de até cerca de 2,5 milhões de votos. Este teste tem pouco poder contra a tese e precisa ser lido junto com os outros.

## Adendo 2 (antes de abrir qualquer boletim do 2º turno dos 6 estados): calibração do teste presidente contra governador por seção

O script reescrito (`scripts/analisar_gov.py`) reproduz a referência de 2022 do documento (+0,04) com efeito fixo de **município**: +0,044 (0,005), 249.040 seções em 2.710 municípios dos 12 estados com 2º turno de governador. Com efeito fixo de **local de votação** (mais rigoroso), o mesmo teste dá -0,005 (0,002). Os dois serão relatados.

Simulação em 2022 de uma conversão uniforme (mesma fração f do branco+nulo de presidente do 2º turno em todas as seções):

| f | Votos convertidos (12 estados) | Efeito fixo de município | Efeito fixo de local |
|---|---|---|---|
| 0 | 0 | +0,044 | -0,005 |
| 0,309 | 1,13 milhão | +0,029 | -0,011 |
| 0,753 | 2,75 milhões | +0,076 | +0,052 |

Consequências, registradas antes dos dados:
- O "perto de +0,5" do documento só vale se a conversão variar muito de urna para urna (por exemplo, concentrada em parte delas). Uma conversão uniforme quase não mexe neste coeficiente, porque a variação natural da queda do branco/nulo de governador domina.
- Critério mantido para conversão concentrada: coeficiente acima de +0,25 e a mais de 3 erros-padrão da referência de 2022 é sinal a favor da tese.
- Para conversão uniforme, este teste é fraco. Um coeficiente de 2026 até +0,10 (município) ou +0,06 (local) não distingue conversão uniforme grande de ausência de conversão.

## Adendo 3 (26/10, a pedido do Léo, antes de olhar fluxos do 2º turno de 2026 por seção): de onde vieram os votos, seção por seção

Pergunta: a soma nacional não diz quem entrou e quem saiu. Dentro de cada seção, os eleitores são os mesmos inscritos, na mesma urna, nos dois turnos. Isso permite medir se o ganho de um candidato cabe no "bolo" disponível naquela seção.

### T7. Ganho além do bolo da seção

- Para cada seção com os dois turnos: bolo = votos dos outros candidatos no 1º turno + queda do branco+nulo (se houver) + aumento do comparecimento (se houver).
- Excesso do candidato que mais ganhou = ganho dele na seção menos o bolo. Excesso positivo só é possível se eleitores do adversário no 1º turno mudaram de lado, ou se houve troca de eleitores (gente que votou no 1º e faltou no 2º, substituída por gente que faltou no 1º e votou no 2º).
- Estatísticas: (a) % das seções com excesso positivo; (b) soma dos excessos positivos como % do ganho total do candidato.
- Referências: 2018 (Haddad, que mais ganhou) e 2022 (Bolsonaro, que mais ganhou). 2026: Lula.
- **Sinal:** (a) e (b) de 2026 acima do maior valor das referências em mais de 5 pontos.
- **Sem sinal:** (a) e (b) até 2 pontos acima do maior valor das referências.
- Entre os dois: inconclusivo.
- **Limite:** não testa a tese do branco/nulo (voto convertido aparece como queda do branco/nulo, que está dentro do bolo). Testa a pergunta "Lula precisaria de mais do que havia para ganhar".

### T8. Regressão de fluxo por seção, dentro do mesmo local

- Ganho de votos do candidato na seção contra: votos de cada outro candidato no 1º turno (2026: Renan Santos, Caiado, Zema, Cury e demais, separados), queda do branco+nulo, variação do comparecimento e votos do próprio adversário no 1º turno; efeito fixo de local, erro agrupado por local.
- Leitura: cada coeficiente estima a fração daquele grupo que foi para o candidato (inferência ecológica, não comportamento individual). Coeficientes fora de 0 a 1 por mais de 3 erros-padrão indicam que o modelo não descreve os dados.
- **Sinal:** ganho de Lula que só se explica com coeficiente de queda do branco+nulo acima de 1 ou com coeficiente acima de 1 para algum grupo, ou um ganho grande em seções sem bolo (constante).
- **Limite:** inferência ecológica; dois grupos que moram nas mesmas seções não se separam bem.

### T9. Os eleitores a mais do 2º turno (comparecimento)

- Nas seções da amostra com log e boletim dos dois turnos: habilitações biométricas e não biométricas no 1º e no 2º turno.
- Se o comparecimento extra viesse de votos inseridos sem o eleitor, ele apareceria como habilitação não biométrica a mais no 2º turno.
- **Sinal:** aumento da habilitação não biométrica do 1º para o 2º turno que acompanhe, dentro do mesmo local, o aumento do comparecimento e o ganho de Lula.
- **Limite:** a amostra de logs é pequena (10 municípios); o bweb completo traz só parte desses campos.

## Adendo 4 (26/10, antes da amostra nacional de locais): calibração do T7 para troca de votos

Se as pesquisas Veritá (Flávio 51,56% dos válidos) ou Gerp (52%) estivessem certas, a fraude teria de ser troca de voto de Flávio para Lula (4,15 a 4,70 milhões, cerca de 6,5% dos votos de Flávio), porque a versão por branco/nulo exigiria um branco/nulo verdadeiro de 9,5% a 10,3%, contra 1,43% declarado na própria Veritá. O T7 é o teste por seção que reage a troca.

Simulação em 2022 (troca uniforme de uma fração dos votos do adversário para quem mais ganhou):

| Troca | Seções com excesso | Ganho em excesso |
|---|---|---|
| 0 | 5,27% | 1,09% |
| 1% | 8,83% | 1,51% |
| 2% | 12,43% | 2,09% |
| 3,5% | 19,81% | 3,40% |
| 6% | 35,76% | 6,92% |

Leitura registrada antes dos dados: na amostra nacional de 2026, um resultado perto de 35% das seções e 7% do ganho seria compatível com a troca que a Veritá implica; perto de 5% a 9% das seções e 1% a 1,5% do ganho, incompatível. O critério do adendo 3 continua valendo.

## Adendo 5 (26/10, antes de rodar): T10, o programa da urna mudou entre os turnos?

Tese do Léo nesta etapa: o sistema da urna foi corrompido com um desvio programado previamente, que aparece como alteração entre o 1º e o 2º turno.

O log de cada urna do 2º turno traz o histórico dela desde a carga (verificado numa seção do Acre): carga em setembro, votação do 1º turno, transição para o 2º turno e votação do 2º turno. Em cada inicialização, o log registra a versão do aplicativo, a data de geração da mídia de votação, a verificação de assinatura de cada componente e, na transição, a data de geração da mídia de resultado com a informação de candidatura do 2º turno.

Medidas por urna da amostra:
- V1: versões do aplicativo registradas (todas as inicializações).
- V2: data de geração da mídia de votação usada no dia do 1º turno e no dia do 2º turno.
- V3: alguma etapa de verificação de assinatura sem SUCESSO, em qualquer data.
- V4: componentes verificados no dia do 2º turno que não foram verificados no dia do 1º turno (arquivo novo).
- V5: data de geração da mídia de resultado do 2º turno.

**Bandeira vermelha:** versão diferente entre urnas ou entre turnos sem explicação (urna de contingência ou recarga registrada); mídia de votação regerada depois do 1º turno sem explicação; qualquer verificação de assinatura sem SUCESSO; componente de programa novo no 2º turno.

**Limite:** o log é escrito pelo próprio programa; um programa malicioso assinado com a chave oficial passaria neste teste. O teste só pega troca de programa, não código malicioso já embutido na versão oficial. Isso só se testa com inspeção de código, teste de integridade e teste de autenticidade.

## Adendo 6 (26/10, antes de rodar o T4 no 2º turno de 2026): correções da revisão independente

Uma revisão adversarial independente do código encontrou defeitos, corrigidos antes de relatar qualquer resultado final:
- `rodar_2026.sh` falharia em silêncio (módulo `lib` não achado com `python3 -I` e sem `set -e`). Corrigido: caminho de importação em cada script e `set -euo pipefail`.
- T3: o leitor de log ignorava o log da urna original quando há urna de contingência (fica num pacote interno). Corrigido; com isso os casos de contingência fecham exatamente.
- T2: comparava totais agrupados; agora compara candidato por candidato, como este pré-registro manda.
- T1: município com seção ainda não baixada aparecia como "diferença". Agora só municípios completos entram.
- Decodificador: agora filtra só cargo constitucional majoritário. Foi validado contra o bweb do 1º turno em 80 seções sorteadas: 80 de 80 idênticas em todos os campos, inclusive voto por candidato.

T4 (branco+nulo zerado): a revisão mostrou que o estimador do esperado usa a taxa estimada como se fosse a verdadeira e superestima a superdispersão. Por isso R fica abaixo de 1 mesmo sem fraude e depende do nível de branco+nulo. Correção registrada antes dos dados:
- O critério original (R bruto contra o maior R das referências) continua sendo relatado como foi registrado.
- Leitura calibrada, que passa a ser a principal: para cada eleição e turno, simular branco+nulo sob a hipótese nula (beta-binomial em torno da taxa do local, ou do município para local de seção única, com a superdispersão ajustada para que o estimador aplicado aos dados simulados reproduza a superdispersão observada), aplicar exatamente o mesmo estimador e obter R_nulo (média de 5 simulações). Estatística calibrada: Rc = R / R_nulo.
- Sinal: Rc do 2º turno de 2026 acima do maior Rc das referências mais 0,15, com excesso acima de 3 vezes a raiz do esperado. Sem sinal: até o maior Rc das referências mais 0,05.
- Votos do candidato 28 (candidatura anulada) entram como nulos, como no total oficial.

## Adendo 7 (26/10, antes de coletar os dados): a "lógica do mundo real" como teste

Proposta do Léo: tratar o dado da urna como não confiável e procurar falta de lógica contra referências externas (pesquisas mais isentas e assertivas, transferência por espectro político, rejeição de Lula, histórico). Para que "falta de lógica" possa ser verificada e não seja só impressão, cada expectativa vira uma previsão numérica com critério definido aqui, antes dos números.

Regra para escolher pesquisas "isentas e assertivas": pelo histórico de acerto medido antes do 2º turno de 2026 (2º turnos de 2018 e 2022 e 1º turno de 2026), nunca pelo resultado do 2º turno de 2026. Alegações de conflito de interesse só entram se verificadas em fonte.

### T11. Mesma pesquisa, dois cargos, mesma urna

Se a urna altera só o voto para presidente, nas pesquisas estaduais que perguntaram presidente e governador à mesma amostra o erro para presidente (a favor de Lula) deve ser bem maior que o erro para governador.
- Estados: os 6 com 2º turno de governador em 2026 (AC, AM, DF, ES, RN, TO), última pesquisa antes do 2º turno com as duas perguntas. Se houver, também 1º turno nos 27 estados.
- Erro de presidente: fatia de Lula nos válidos do estado (resultado menos pesquisa). Erro de governador: valor absoluto do erro na fatia do candidato que venceu (resultado menos pesquisa).
- **Sinal:** média de (erro de presidente menos erro absoluto de governador) de 2,0 pontos ou mais, com pelo menos 4 estados.
- **Sem sinal:** média de até 0,5 ponto.
- Entre os dois: inconclusivo.

### T12. Como cada instituto erra do 1º para o 2º turno

Se o erro das pesquisas no 2º turno de 2026 for anômalo, a mudança do erro entre o 1º e o 2º turno deve ser diferente da mudança histórica do mesmo instituto.
- Para cada instituto com pesquisa final nos dois turnos em 2018, 2022 e 2026: erro do candidato de direita nos válidos (resultado menos pesquisa) no 1º e no 2º turno; Δ = erro do 2º turno menos erro do 1º turno.
- **Sinal:** Δ de 2026 mais negativo que a média histórica do mesmo instituto em 3 pontos ou mais, na média dos institutos com histórico.
- **Sem sinal:** diferença de até 1,5 ponto.

### T13. O "teto" de Lula pela rejeição

- Rejeição ("não votaria de jeito nenhum") de cada finalista na última pesquisa antes do 2º turno, em 2018, 2022 e 2026, pelos mesmos institutos.
- Teto = 100 menos a rejeição (em % dos entrevistados). Comparar com o voto do candidato em % do comparecimento.
- **Sinal:** Lula acima do próprio teto em mais de 3 pontos, quando nenhum vencedor de 2018 e 2022 ultrapassou o teto pelos mesmos institutos.
- **Sem sinal:** Lula abaixo do teto ou acima dele no mesmo tamanho dos vencedores anteriores.

## Adendo 8 (26/10, antes do bweb do 2º turno): T14, marca de troca de votos por seção

Se a urna trocasse uma fração s dos votos de Flávio por votos de Lula, o ganho de Lula em cada seção ficaria proporcional aos votos de Flávio daquela seção. Na regressão do T8 (dentro do mesmo local), o coeficiente dos votos do adversário no 1º turno sobe em cerca de s.

Calibração (troca uniforme simulada sobre os dados reais):
- 2018, Haddad como ganhador: 0,006 sem troca; 0,026 com 2%; 0,046 com 4%; 0,071 com 6,5%.
- 2022, Bolsonaro como ganhador: 0,038 sem troca; 0,057 com 2%; 0,076 com 4%; 0,100 com 6,5%.
- Sem troca, o coeficiente variou de 0,006 a 0,041 entre os candidatos de 2018 e 2022 (comportamento real: eleitores que mudam de lado e troca de eleitores).

Critério para o 2º turno de 2026, com todas as seções do bweb:
- **Sinal:** coeficiente acima de 0,071 (o maior valor sem troca, 0,041, mais 0,03, o equivalente a cerca de 3% de troca) e a mais de 3 erros-padrão disso.
- **Compatível com a troca que a pesquisa Veritá implicaria (cerca de 6,5%):** 0,10 ou mais.
- **Sem sinal:** até 0,051.
- Entre os dois: inconclusivo.

Transparência: na amostra parcial (1.709 seções) este coeficiente já foi visto: 0,056 (erro-padrão 0,012). O critério acima vale para os dados completos, que ainda não existem.

## Adendo 9 (26/10, tarde, antes de rodar qualquer um destes testes): a fraude vista pela cabeça de quem frauda

Pedido do Léo: pensar como agiria quem quisesse fraudar e onde os números apareceriam. Uma modelagem de ameaça independente (quatro frentes: código oficial, preparação regional, gatilhos seletivos e ações fora da urna, mais o que exigiria um resultado plausível) chegou a este princípio, registrado antes dos testes:

- Quem frauda sabendo que todos vão refazer as contas evita contradição exata (soma, assinatura, QR, programa diferente do lacrado, voto sem habilitação) e deixa o 1º turno intacto. Agiria só no 2º turno e só para presidente, com um deslocamento pequeno e espalhado.
- A aritmética não deixa escolha: virar 4,43 milhões de margem exige trocar cerca de 2,2 milhões de votos de Flávio (3,6% deles, uns 4,4 por seção) ou acrescentar cerca de 4,43 milhões (uns 9 por seção).
- O rastro aparece em quatro pontos: (1) ganho de Lula contra a fonte possível do voto, seção por seção; (2) presidente contra governador e o conteúdo dos nulos; (3) comparecimento contra o que a urna não escreve (caderno, óbitos, idade); (4) a cadeia urna, papel, arquivo assinado, total.
- O único espaço sem rastro estatístico próprio é a troca uniforme feita pelo próprio programa assinado. Mesmo ela tem teto pela cauda inferior da troca por estrato (T16) e pela contagem física (T25, T31).

Transparência sobre o que já foi visto: os resultados de T1 a T14 já relatados. Não foram olhados: o modelo e o número da urna por seção do 2º turno contra o 1º (T17), os dígitos dos votos nulos no RDV (T19), os horários de cada voto no log (T30), os arquivos de assinatura `-vota.vsc` (T18, ainda não baixados), Flávio em votos totais nas pesquisas (T33).

Os testes marcados "agora" rodam na amostra (3.897 seções com boletim, 835 com RDV e log). Valem como preliminares e são refeitos com o bweb completo quando houver, com o mesmo critério. Nos demais, o critério fica registrado para quando o dado existir.

### T15. Soma nacional completa e cadastro de seções (com o bweb)
- Somar, sem deduplicar votos e deduplicando aptos e comparecimento por seção, todos os números votáveis, brancos, nulos, aptos e comparecimento de todas as seções e tipos de urna; comparar com tolerância zero com o total oficial de cada município, UF, exterior e Brasil.
- No mesmo passo: conjunto de seções igual ao do 1º turno (499.206) salvo agregação documentada; aptos iguais seção a seção; nenhuma seção com comparecimento acima dos aptos; seções em situação especial por UF e o saldo líquido que tiraram, medido pela margem de Flávio sobre Lula de cada uma no 1º turno.
- **Sinal:** qualquer diferença não atribuível a uma seção nomeada com ato documentado; soma dos municípios diferente do total da UF; ou saldo tirado pelas seções especiais acima de 3 vezes o do 2º turno de 2022 e acima de 100 mil votos.
- **Sem sinal:** diferença zero em todos os níveis depois da reconciliação documentada e saldo das seções especiais até 1,5 vez o de 2022.

### T16. Piso da troca uniforme: cauda inferior do coeficiente de troca por estrato (com o bweb)
- A regressão do T8/T14 (ganho de Lula na seção nos votos de cada eliminado, na queda do branco+nulo, na variação do comparecimento e nos votos de Flávio e de Lula no 1º turno; efeito fixo de local; erro agrupado por local) rodada em cada uma das 27 UFs e, no país, capital contra interior.
- Estatística principal: Q10, o 10º percentil ponderado por seções do coeficiente dos votos de Flávio no 1º turno entre as 27 UFs. Secundária: o menor coeficiente entre as UFs com 5.000 seções ou mais.
- Antes de abrir 2026: o mesmo cálculo em 2018 (Haddad) e 2022 (Bolsonaro), sem troca e com troca uniforme simulada de 1%, 2% e 3,6%.
- **Sem sinal (exclui troca uniforme de 2% ou mais):** Q10 de 2026 abaixo do menor Q10 simulado com 2% entre as duas referências, por mais de 2 erros-padrão.
- **Sinal:** Q10 de 2026 acima do maior Q10 simulado com 3%, a mais de 2 erros-padrão.
- Entre os dois: inconclusivo. Suposição registrada: a troca real no estrato mais baixo de 2026 não fica abaixo da do estrato mais baixo das referências. Um sinal aqui só pesa se coincidir com T17, T22 ou T25.

### T17. Atributo da máquina dentro do mesmo prédio (agora, preliminar)
- y = variação da fatia de Lula entre os dois candidatos (2º menos 1º turno), peso votos de Lula mais Flávio no 2º turno, efeito fixo de local, erro agrupado por local.
- Indicadores: modelo da urna do 2º turno pela faixa do número de série (referência UE2022); urna diferente entre os turnos (número da urna do bweb do 1º turno contra o do boletim do 2º turno); na subamostra com log, contingência no 2º turno. Covariáveis: logaritmo dos aptos, variação do comparecimento, fatia de Lula no 1º turno.
- Repetir com y igual à variação do branco+nulo e à variação do comparecimento. Placebo: o mesmo modelo com y = fatia de Lula no 1º turno (nível).
- Contribuição nacional de um grupo = coeficiente vezes a fração de seções do grupo. Magnitude exigida pela aritmética: 1,79 ponto dividido por essa fração.
- **Sinal:** algum grupo com contribuição acima de 0,3 ponto, a mais de 4 erros-padrão, sem efeito no placebo (abaixo de 0,1 em valor absoluto) e sem efeito no comparecimento.
- **Sem sinal:** todos os coeficientes abaixo de 0,5 ponto em valor absoluto e contribuição somada abaixo de 0,15 ponto (cerca de 190 mil votos).
- Na amostra, relatar também o efeito mínimo detectável (2,8 erros-padrão). Se ele passar de 0,5 ponto num grupo, aquele grupo fica sem poder na amostra.

### T18. Assinatura digital de cada arquivo de seção (agora)
- Baixar o `-vota.vsc` listado no `-aux.json` das 835 seções que têm boletim, RDV e log, pelo mesmo limitador de taxa, sem montar nenhum caminho que não esteja listado.
- Para cada seção: decodificar o arquivo de assinatura; conferir o resumo de cada arquivo assinado contra o arquivo baixado; verificar cada assinatura com a chave pública do certificado que vem no próprio pacote; conferir emissor e titular dos certificados e se o número da urna no certificado (se houver) bate com o do boletim.
- Cadeia até a raiz oficial do TSE: só se o certificado da autoridade estiver no pacote ou publicado pelo TSE. Se não estiver, o item fica relatado como "cadeia não verificada", sem inferência.
- **Sinal:** qualquer arquivo com resumo diferente ou assinatura inválida, confirmado depois de baixar de novo; certificado de emissor diferente dos demais sem explicação; número de urna divergente sem contingência registrada.
- **Sem sinal:** 100% dos resumos e assinaturas válidos e campos coerentes.
- Limite: a assinatura prova que o arquivo saiu da urna sem alteração depois. Não diz nada sobre o que a urna gravou.

### T19. Conteúdo dos votos nulos no RDV (agora, parcial)
- (a) Contar no RDV do 2º turno os nulos de presidente digitados 13 ou 22 e, nas UFs com 2º turno de governador, os nulos de governador com o número de um dos dois candidatos.
- (b) Por seção, nulos de presidente digitados com o número de um eliminado (70, 14, 55, 30) contra os votos dele no 1º turno na mesma seção; inclinação com efeito fixo de município. Referência: a mesma relação no 2º turno de 2022 (12 e 15 digitados como nulo contra os votos de Ciro e Tebet no 1º turno), numa amostra de 2022 baixada pelo mesmo procedimento, só se o `-aux.json` de 2022 responder no padrão já documentado; sem isso, (b) fica sem referência e é só descritivo.
- (c) Razão entre brancos e nulos por seção, contra o 1º turno: descritivo.
- (d) Seções com um mesmo número nulo raro repetido 5 vezes ou mais, fora dos números de candidatos de 2022 a 2026 e de 00 e 99: só lista para conferência.
- **Sinal forte:** qualquer nulo de presidente com 13 ou 22 (ou de governador com o número de um finalista) confirmado numa segunda decodificação.
- **Sinal de conversão seletiva:** inclinação de (b) abaixo de 0,5 vez a de 2022, a mais de 3 erros-padrão.
- **Sem sinal:** zero nulos com 13 ou 22 e inclinação de (b) entre 0,75 e 1,33 vez a de 2022.

### T20. Fechamento das pendências do T10 e identidade dos dados de candidatos (agora, parcial)
- Casar cada urna que o T10 deixou em aberto (2 com mídia diferente, 13 sem o 1º turno no log, 1 com mídia igual e sem o 1º turno, 8 mídias de resultado geradas fora de 10 a 15/10) com o evento de substituição, contingência ou recarga no próprio log. A ata de carga do TRE fica para quando for obtida.
- Na amostra inteira: a lista de números votáveis de presidente em cada boletim tem de ser {13, 22} e a de governador, nas 6 UFs, os dois finalistas da UF.
- **Sinal:** urna com mídia, programa ou candidatos fora do oficial sem evento que explique; lista de votáveis diferente dentro de uma UF.
- **Sem sinal:** todas as pendências casadas com eventos registrados e listas idênticas por UF.

### T21. Liberação sem biometria em todo o país (com o bweb)
- Por seção, nos dois turnos de 2026 e de 2022: variação das habilitações sem biometria de quem tem biometria cadastrada, dividida pelo comparecimento. (a) Total nacional contra a variação do comparecimento e contra 2022. (b) Regressão do ganho de Lula nas duas variações (com e sem biometria), efeito fixo de local. (c) Nos logs da amostra: fração das liberações sem biometria nos últimos 90 minutos, 2º contra 1º turno na mesma urna.
- **Sinal:** coeficiente de Lula nas liberações sem biometria acima de 0,9 e a mais de 3 erros-padrão acima do coeficiente das biométricas, com variação nacional das liberações mais de 400 mil acima do esperado pela proporção de 2022.
- **Sem sinal:** coeficientes a até 0,15 um do outro e liberações proporcionais ao aumento do comparecimento, como em 2022.

### T22. Governador da mesma urna como controle da virada (com o bweb)
- Nas UFs com 2º turno de governador, campo de cada candidato fixado pelo apoio declarado no 2º turno; UF sem alinhamento claro sai. Regressão, com efeito fixo de local, da variação da fatia de Lula na variação da fatia do governador do campo de Lula e na composição do 1º turno. Comparar com os estados de 2018 e 2022 com 2º turno de governador alinhado. Ler junto com o T5 do 2º turno.
- **Sinal:** em pelo menos 4 UFs alinhadas, inclinação abaixo do menor valor de 2022 por mais de 3 erros-padrão e virada de Lula não acompanhada de 1,5 ponto ou mais, no mesmo sentido em todas.
- **Sem sinal:** inclinação e resíduo dentro da faixa entre estados de 2018 e 2022.

### T23. Componente de zona e degrau na fronteira de zona (com o bweb)
- Resíduo r da variação da fatia de Lula por seção, de um modelo dentro da UF com a composição completa do 1º turno e a variação do comparecimento. (a) Decompor a variância de r em município, zona dentro do município, local dentro da zona e seção, descontando a variância binomial. (b) Nos municípios com 2 zonas ou mais, pares de locais a até 1 km em zonas diferentes contra pares à mesma distância na mesma zona (coordenadas do cadastro de locais do TSE).
- **Sinal:** componente de zona de pelo menos 2 vezes o maior de 2018 e 2022, degrau médio na fronteira de 1 ponto ou mais e mais de 200 mil votos somados nas zonas extremas.
- **Sem sinal:** componente até 1,3 vez o das referências e degrau abaixo de 0,3 ponto.

### T24. Boletim impresso (QR code) contra arquivo publicado (dado externo)
- Leituras de QR dos fiscais do PL e do PT e de cidadãos, validadas pelo resumo e pela assinatura do próprio QR; foto sem QR verificável vale só como pista. Comparar campo a campo com o boletim publicado. Medir a cobertura por UF e por decil da fatia de Lula no 1º turno.
- **Sinal:** uma única divergência com QR autêntico, não explicada por cédula ou junta.
- **Sem sinal:** zero divergência com cobertura de pelo menos 20 mil seções, incluindo pelo menos 20% das seções dos dois decis mais favoráveis a Lula, e com a base do PL entregue.

### T25. Contraprova física do comparecimento (dado externo)
- Sorteio público de cerca de 400 seções, estratificado por UF e com sobreamostra nas de maior aumento de comparecimento: assinaturas no caderno contra o comparecimento do boletim. Cruzamento dos votantes do 2º turno com óbitos anteriores a 25/10, por zona, contra o 1º turno e 2022.
- **Sinal:** diferença média acima de 2 por seção, ou qualquer seção com diferença de 10 ou mais sem ata; ou taxa de mortos dados como votantes acima de 3 vezes a do 1º turno e a de 2022.
- **Sem sinal:** diferença zero (até 1, com ata) em pelo menos 98% das seções e taxa de óbitos dentro da histórica.

### T26. Seções sorteadas para o teste de integridade (dado externo)
- Seções cuja urna foi sorteada para o teste de integridade em 2022 e nos dois turnos de 2026 (atas dos TREs). Diferença em diferenças da variação da fatia de Lula nas sorteadas só no 2º turno contra as demais do mesmo local, com placebo em 2022. Conferência de todos os relatórios de integridade e autenticidade e da cobertura por UF e modelo contra a frota.
- **Sinal:** diferença em diferenças de -1,0 ponto ou menos a mais de 3 erros-padrão e ausente em 2022; divergência não explicada nos relatórios; ou modelo com mais de 15% da frota sem urna testada.
- **Sem sinal:** efeito até 0,4 ponto em valor absoluto, com erro-padrão até 0,2, e relatórios 100% conformes.

### T27. Teto somado dos vetores medidos (com o bweb)
- Por seção, o excesso de cada vetor sobre a maior taxa de 2018, 2022 e do 1º turno de 2026, em votos (T21, votos depois das 17h, T15, T7, T28, T17, T23). Cada voto entra uma vez, no vetor de maior valor da seção. Somar e comparar com 2,22 milhões (troca) e 4,43 milhões (acréscimo).
- **Sem sinal:** soma até 0,5 milhão. **Sinal:** 2,2 milhões ou mais. Entre os dois: inconclusivo. Chegar perto não prova fraude.

### T28. Cauda de comparecimento extremo com voto concentrado (com o bweb)
- Seções com 100 aptos ou mais, sem as especiais. Esperado por beta-binomial em torno da média do local, calibrado por simulação nula como no T4. Contar observados e esperados de comparecimento de 95% ou mais com fatia de Lula de 80% ou mais, o mesmo para Flávio, e aumento de comparecimento de 15 pontos ou mais.
- **Sinal:** O/E calibrado de Lula de pelo menos 1,5 vez o maior das referências (2º turno de 2022 e 1º de 2026), com excesso acima de 3 vezes a raiz do esperado e O/E de Flávio normal.
- **Sem sinal:** O/E até 1,1 vez o das referências.

### T29. Matriz de transferência com inferência ecológica calibrada (com o bweb)
- Por UF, matriz de transição do 1º para o 2º turno (multinomial-Dirichlet ou King). Validação antes: plantar em 2022 uma troca conhecida de 2% e exigir recuperação com erro de até 1 ponto; se não passar, o teste é declarado sem poder.
- **Sinal:** célula Flávio para Lula de 3% ou mais no país e em pelo menos 20 UFs, com intervalo acima de 1%, fora da faixa de 2018 e 2022 para quem ganhou terreno.
- **Sem sinal:** célula até 2% no país e dentro da faixa das referências.

### T30. Gatilho por horário ou por contagem (agora)
- Horário: nos logs da amostra com os dois turnos na mesma urna, por seção, fração f2 das confirmações de voto do 2º turno depois das 12h, 14h e 16h em hora de Brasília (o deslocamento de fuso de cada urna é tirado do horário em que ela ficou pronta para votos, arredondado para a hora cheia em relação às 8h), e f1 no 1º turno. Regressão da variação da fatia de Lula em f2, controlando f1 e a variação do comparecimento, efeito fixo de município.
- **Sinal:** em algum corte, inclinação de 4 pontos ou mais por unidade de fração, a mais de 3 erros-padrão com correção de Bonferroni para 3 cortes (z de 2,93), e ausente no 1º turno (mesma regressão com y = fatia no 1º turno e f1).
- **Sem sinal:** inclinação até 1,5 ponto em valor absoluto, com erro-padrão até 0,6. Se o erro-padrão passar de 0,6, o corte fica sem poder na amostra.
- Contagem: em todas as seções da amostra, variação da fatia de Lula na fração max(0, votantes menos N) dividida pelos votantes, para N em 50, 100, 150 e 200, efeito fixo de local, controlando a variação do comparecimento. Placebo: a mesma regressão com os dois turnos de 2022 completos. **Sinal:** coeficiente de 4 pontos ou mais a mais de 3 erros-padrão com Bonferroni para 4 cortes (z de 3,02), ausente em 2022. **Sem sinal:** até 1,5 ponto em valor absoluto.

### T31. Seções votadas em cédula (com o bweb)
- Seções do 2º turno de 2026 e de 2022 apuradas pela junta por cédula. Para cada uma, variação da fatia de Lula menos a média das outras seções do local (ou município). Estimativa conjunta com intervalo e efeito mínimo detectável calculado antes.
- **Sinal:** efeito de -1,8 ponto ou menos a mais de 2,5 erros-padrão, com 30 seções ou mais. **Sem sinal:** entre -0,7 e +0,7 com efeito mínimo detectável até 1,8. Acima de 1,8, sem poder.

### T32. Idade de quem passou a comparecer (com o perfil de comparecimento do TSE)
- Variação do comparecimento entre turnos nas faixas de 80 anos ou mais; parcela do aumento vinda dessas faixas; correlação entre zonas dessa variação com o ganho de Lula e com o encerramento tardio da zona no 1º turno.
- **Sinal:** parcela de 80 anos ou mais acima de 2 vezes a maior das referências (2018, 2022) e correlação com o ganho de Lula pelo menos 0,3 acima da de 2022, sem relação com a fila. **Sem sinal:** parcela até 1,3 vez a das referências e correlação a até 0,1 da de 2022.

### T33. Pesquisas: Flávio em votos totais e T11 com todos os institutos (agora)
- (a) Para cada instituto com votos totais na última pesquisa do 2º turno: Flávio em votos totais mais sua parte proporcional dos indecisos, contra o voto dele em % do comparecimento. A mesma conta para o candidato de direita no 2º turno de 2018 e 2022 (distância histórica).
- (b) T11 com todos os institutos que perguntaram presidente e governador à mesma amostra nas 6 UFs, e não só a AtlasIntel.
- **(a):** se Flávio ficou 3 pontos ou mais abaixo do que as pesquisas davam, além da distância histórica, em pelo menos 5 institutos, a conversão pura de branco/nulo não explica o resultado (isso pesa contra essa tese específica, não a favor de fraude). Sem sinal para (a): distância até 1 ponto acima da histórica.
- **(b):** mesmo critério do T11 (sinal com média de 2,0 ou mais em pelo menos 4 UFs; sem sinal até 0,5).

## Adendo 10 (26/10, tarde, antes de baixar os boletins da extensão): T17 com amostra dirigida de locais com modelos misturados

Transparência: o T17 preliminar já foi visto. Na amostra (3.897 seções), só 67 locais tinham urnas de modelos diferentes, e o placebo falhou: as seções com UE2013 e UE2015 já eram cerca de 4,5 pontos mais Lula no 1º turno, com comparecimento cerca de 2 pontos menor e encerramento mais tarde que as UE2022 do mesmo local. Na virada, essas seções ficaram cerca de 3,3 pontos abaixo. Na base completa do 1º turno (7.896 locais mistos), a diferença de partida das urnas antigas é bem menor (+0,74 e +0,95 ponto na fatia de Lula). A amostra preliminar não tem poder para separar composição de efeito da máquina. A leitura possível nos dois sentidos: urnas novas alteradas a favor de Lula, ou eleitores de Flávio que desistiram da fila nas urnas antigas no 1º turno e voltaram no 2º.

Frota do 1º turno de 2026 (seções): UE2020 40,2%, UE2022 39,8%, UE2015 17,6%, UE2013 2,4%. O número da urna foi o mesmo nos dois turnos em 98,9% das seções da amostra.

Extensão, fixada antes de baixar:
- Universo: locais do bweb do 1º turno com pelo menos 2 modelos entre seções de 20 ou mais votantes, fora da amostra atual (7.828 locais).
- Sorteio: permutação com semente 20261026; os 450 primeiros locais, todas as seções de cada um (3.758 seções). Baixar só o `-aux.json` e o `-bu.dat`, na ordem do sorteio, pelo mesmo limitador de taxa. Se o download parar antes, entra o prefixo completo de locais baixados, que continua aleatório.
- Análise: a mesma do T17 (adendo 9) na união da amostra atual com a extensão, mais o contraste pré-especificado urnas antigas (UE2013 e UE2015) contra novas (UE2020 e UE2022), com as covariáveis do T17 e, numa segunda versão, também o horário de encerramento do 1º turno e se a seção encerrou depois das 18h no 1º turno (fila).
- Contribuição, se o grupo alterado fossem as urnas novas: coeficiente vezes 0,80 (fração das novas na frota). Se fossem as antigas: coeficiente vezes 0,20.

Critério para o contraste antigas contra novas (y = virada de Lula):
- **Sinal:** novas acima das antigas em 1,0 ponto ou mais, a mais de 4 erros-padrão, nas duas versões (com e sem as variáveis de fila), com placebo (fatia de Lula no 1º turno) abaixo de 1,5 ponto em valor absoluto e diferença no comparecimento que não explique o efeito (efeito na variação do comparecimento abaixo de 1 ponto).
- **Sem sinal:** diferença abaixo de 0,5 ponto em valor absoluto, com erro-padrão até 0,2.
- Entre os dois: inconclusivo. Referência: em 2022 o mesmo teste por modelo deu virada de -0,16 a -0,18 (erro-padrão 0,12).
- Leitura de fila: se o efeito cair para menos da metade ao entrar o encerramento do 1º turno, e as seções antigas tiverem encerrado mais tarde no 1º turno, a explicação de fila fica favorecida.

## Adendo 11 (26/10, tarde, antes de baixar os locais com urnas antigas e novas juntas): correção do desenho do Adendo 10

Erro de desenho encontrado ao preparar a análise: o efeito de cerca de -3,3 pontos das urnas antigas no T17 preliminar vinha de um único local. No país inteiro, só 119 locais têm, entre seções de 20 ou mais votantes, urnas antigas (UE2013 ou UE2015) e novas (UE2020 ou UE2022) ao mesmo tempo: 113 em SP, 3 no AM e 3 no MT, com 1.335 seções. Os outros 7.777 locais mistos misturam só novas (5.165) ou só antigas (2.612). Dos 450 locais sorteados no Adendo 10, só 9 são de antigas com novas. O efeito fixo de local identifica o contraste antigas contra novas apenas nesses locais.

O que já foi visto: o T17 preliminar (1 local de antigas com novas) e uma rodada parcial com 225 seções da extensão, ainda com 1 único local de antigas com novas, portanto sem informação nova sobre o contraste.

Mudança, registrada antes de baixar:
- O download do Adendo 10 foi parado em 264 seções (prefixo do sorteio, que continua aleatório).
- Baixar o `-aux.json` e o `-bu.dat` de todas as 1.335 seções dos 119 locais, pelo mesmo limitador de taxa.
- Contraste antigas contra novas: o mesmo do Adendo 10, nesses 119 locais (é o universo inteiro, não uma amostra). Critérios iguais. Se o erro-padrão passar de 0,3, o teste fica com poder limitado e o resultado sai junto com o efeito mínimo detectável (2,8 erros-padrão).
- Contrastes de um modelo só (UE2020 contra UE2022; UE2013 contra UE2015): com a amostra atual mais o prefixo de 264 seções, como no T17 do Adendo 9.
- Limite de generalização: 113 dos 119 locais estão em SP. Um efeito encontrado vale para SP; ausência de efeito não exclui alteração restrita a outra UF.

## Adendo 12 (26/10, tarde, antes de baixar os logs das demais seções da amostra): T30 com todos os logs da amostra

Transparência: o T30 por horário já foi visto nas 835 seções com log (16 municípios; 2 deles com 481 seções). Inclinação da virada na fração de votos depois de 12h, 14h e 16h: +6,6 (2,6), +7,4 (1,6) e +14,9 (4,9), com efeito fixo de município. A revisão independente mostrou que o placebo rodado tinha uma covariável fora do registro (log dos aptos); o placebo como registrado (y = fatia de Lula no 1º turno, x = f1, efeito fixo de município) dá +13,0 (3,2), +16,0 (3,3) e +16,2 (3,6) e continua falhando. Com correções para poucos grupos (jackknife CV3), os z caem para 1,7, 3,1 e 2,2. O placebo em nível falha por composição: dentro do município, quem vota mais tarde já votava mais em Lula no 1º turno.

Extensão: baixar o `-log.jez` listado no `-aux.json` das outras 3.062 seções da amostra (todas já têm o `-aux.json`), pelo mesmo limitador. O T30 é refeito com todas as seções com log dos dois turnos, com o critério do Adendo 9 sem mudança.

Leituras de robustez fixadas agora, relatadas ao lado do critério e sem substituí-lo:
- R1: efeito fixo de local no lugar de município.
- R2: R1 mais a fatia de Lula no 1º turno como controle, que trata a composição que fez o placebo falhar.
- R3: erro-padrão CV3 (jackknife por grupo) ao lado do CR1.
- Leitura: se, em algum corte, a inclinação ficar em 4 pontos ou mais com z acima de 2,93 em R2 com CR1 e CV3, o horário passa a ser indício a cruzar com T21 e T25, mesmo com o placebo em nível falhando. Se em R2 a inclinação cair abaixo de 1,5 ou perder significância, a associação é lida como composição.
- Escala: uma troca de uma fração q dos votos de Flávio dados depois do corte daria inclinação de cerca de 50 vezes q, em pontos. Uma inclinação de 7,4 equivaleria a q de cerca de 15% e a cerca de 1,6 ponto na média nacional. Por isso a leitura de composição contra gatilho importa.

Com os mesmos logs: T21(c), fração das habilitações sem biometria nos últimos 90 minutos, 2º contra 1º turno na mesma urna, só descritivo.

## Adendo 13 (26/10, tarde, antes de baixar os arquivos de assinatura das demais seções): T18, T10, T3 e T9 em toda a amostra

Com os logs das 3.897 seções da amostra (Adendo 12), refazer pelo mesmo código e com os mesmos critérios: T10 (versão, mídia, assinaturas no log, componentes novos), T3 (horários e ritmo) e T9 (biometria). Depois, baixar o `-vota.vsc` listado no `-aux.json` das outras 3.062 seções e refazer o T18 em todas (boletim e log de cada uma conferidos contra a assinatura da urna). Critérios sem mudança. Resultados das 835 já relatados; os das 3.062 ainda não foram olhados.

T21(c), descritivo: fração das habilitações sem biometria das 15h30 de Brasília em diante, 2º contra 1º turno na mesma urna (analisar_biometria_tarde.py, escrito antes de rodar).

## Adendo 14 (26/10, noite, antes de abrir qualquer boletim do estrato G): presidente contra governador na mesma urna

Contexto: o T8 e o T14 mostram que, dentro de cada seção, Flávio perdeu em termos líquidos cerca de 5% dos próprios eleitores do 1º turno (coeficiente -0,050, erro-padrão 0,007), e esse é o termo que fecha a conta do ganho de Lula. Duas leituras: (a) eleitores de Flávio do 1º turno que faltaram ou anularam no 2º, substituídos por outros; (b) troca só no voto de presidente, feita pelo eleitor ou pelo programa. Quem falta não vota em nenhum cargo; a troca só no presidente não mexe no governador.

Dados: prefixo de 2.400 seções do estrato G (ordem aleatória do sorteio original), só o `-bu.dat`, em download desde as 20h33 UTC (corrigido; a primeira versão deste adendo dizia 18h40 por engano); nenhum boletim aberto até este registro. Votos por candidato a governador no 1º turno extraídos do bweb do 1º turno das mesmas UFs.

Campos fixados antes, com fontes conferidas por dois agentes independentes (arquivo `resultados/alinhamento_governadores_2t_2026.json`):
- AM: campo de Flávio 22 (Professora Maria do Carmo, PL); campo de Lula 55 (Omar Aziz, PSD). Claro.
- DF: campo de Flávio 11 (Celina Leão, PP); campo de Lula 13 (Leandro Grass, PT). Claro.
- ES: campo de Flávio 10 (Pazolini, Republicanos); campo de Lula sem candidato claro.
- RN: campo de Lula 13 (Cadu de Lula, PT); campo de Flávio sem candidato claro (Allyson neutro).
- AC e TO: os dois finalistas no campo de Flávio; saem.

Testes:
- T22 como registrado no Adendo 9, com AM e DF (as UFs claras). O critério de sinal pede pelo menos 4 UFs: com 2, o T22 fica sem poder pelo registro e é relatado como descritivo.
- T5 no 2º turno, como registrado no pré-registro original, nas 6 UFs (beta do branco+nulo de presidente contra o de governador; referências 0,468 em 2018 e 0,401 em 2022).
- T22b (novo). Nas seções de AM, DF e ES, a mesma regressão do T8 para os dois cargos: ganho do candidato entre turnos contra os próprios votos no 1º turno, os votos dos demais candidatos do mesmo cargo no 1º turno, a queda do branco+nulo do cargo e a variação do comparecimento, com efeito fixo de local e erro agrupado por local. D = coeficiente dos próprios votos de Flávio menos o do candidato a governador do campo dele, nas mesmas seções (empilhado nas 3 UFs, com efeito fixo de local por cargo).
  - Sinal de troca só no voto de presidente: D de -0,03 ou menos, a mais de 2,5 erros-padrão de zero.
  - Sem sinal (a perda de Flávio acompanha a do aliado, como faria a falta ao 2º turno): D entre -0,015 e +0,015.
  - Entre os dois: inconclusivo.
  - Limites: não separa troca feita pelo eleitor (voto dividido) de troca feita pelo programa; a dinâmica do 2º turno de governador é própria (o aliado recebe votos dos eliminados do 1º turno estadual); não há referência de outro ano com os votos por candidato a governador.

## Adendo 15 (26/10, noite, ~21h15 UTC, antes de rodar qualquer um dos dois testes abaixo): onde estaria a condição do desvio

Contexto e o que já vi: o recorte exploratório por região (commit 252b98c) mostrou Flávio perdendo cerca de 5% dos próprios eleitores do 1º turno em todas as regiões, menos no Sul (cerca de 0). Por UF do Sul, também exploratório (26/10, ~20h50 UTC, amostra de 3.897 seções): PR +0,008 (EP 0,031, 25 locais), SC +0,045 (EP 0,022, 22 locais), RS -0,033 (EP 0,017, 56 locais); em 2022, nas mesmas seções, Lula perdeu cerca de 8% nas três. Não vi a curva de perda própria por força local do adversário em nenhum ano, nem nenhum dado da divisa.

Se houve desvio pelo programa e ele poupou o Sul, a condição tem de estar escrita em algum lugar. As duas condições mais simples deixam marcas diferentes:
- Condição pela UF (o programa sabe em que estado está): a perda muda de uma vez na divisa entre o Sul e os vizinhos, mesmo com eleitores parecidos dos dois lados.
- Condição pela força local de Lula (desvia mais onde Lula já é forte, para disfarçar): não há salto na divisa, e Flávio fica abaixo de qualquer referência na mesma faixa de força do adversário.
Já a leitura natural ("o eleitor se aproxima da maioria do lugar", vista com Lula em 2022, que perdeu mais no Sul, onde era minoria) prevê que Flávio 2026 caia na mesma curva que os outros candidatos de 2018, 2022 e 2026.

### T34. Salto na divisa Sul / não Sul (com o bweb do 2º turno)
- Dados: bweb do 1º e do 2º turno de 2026 por seção; coordenadas dos locais de votação do arquivo "Eleitorado por local de votação - 2026" do portal do TSE (gerado em 25/10, baixado em 26/10 às 21h00 UTC). Unidade: local de votação (soma das seções), com coordenadas válidas e pelo menos 100 votos nominais no 2º turno.
- Medida: resíduo r da fatia de Lula no 2º turno, L2/(L2+F2), num modelo linear ponderado pelos votos nominais do 2º turno, ajustado com todos os locais a até 100 km de um local da outra UF, contra as fatias do comparecimento do 1º turno de Lula, Flávio, demais candidatos e branco+nulo, e o log do eleitorado. Sem nenhuma variável de UF.
- Pares: cada local do lado Sul (PR) com o local mais próximo do outro lado (SP ou MS) a até 20 km, e vice-versa (pares repetidos contam uma vez). J = média ponderada de r(não Sul) - r(Sul). Erro-padrão por bootstrap de municípios do lado Sul, com seus pares (2.000 reamostras).
- Divisas placebo, mesmo método: dentro do Sul (PR-SC, SC-RS) e entre UFs fora do Sul sem 2º turno de governador (SP-MS, SP-MG, SP-RJ, MS-MT, MS-GO, MS-MG, MG-GO, GO-MT, MG-RJ). Só entram divisas com pelo menos 50 pares.
- Referência: o mesmo J em 2022 (Lula contra Bolsonaro), com as seções de 2022 ligadas às coordenadas de 2026 pela chave UF|município|zona|seção.
- Esperado sob desvio de cerca de 4,5% fora do Sul e zero no Sul: J perto de +0,03 (o desvio soma s(1 - m) à fatia m de Lula).
- Sinal de condição pela UF: J de 2026 de 0,015 ou mais, a mais de 2,5 erros-padrão, e J(2026) - J(2022) de 0,015 ou mais, a mais de 2,5 erros-padrão (erro da diferença somando as variâncias). Se a mediana do |J| das divisas placebo de 2026 passar de 0,01, o sinal vira inconclusivo (divisa de estado em geral salta).
- Sem sinal: J de 2026 de 0,008 ou menos, com erro-padrão de até 0,005.
- Entre os dois: inconclusivo.

### T35. Curva de perda própria por força local do adversário (amostra agora, preliminar; bweb depois, decisivo)
- Seis candidaturas: Haddad e Bolsonaro (2018), Lula e Bolsonaro (2022), Lula e Flávio (2026), sempre nas mesmas seções.
- Faixas pela fatia do adversário no 1º turno, entre os votos válidos do local de votação (soma das seções do local): menos de 35%, 35% a 50%, 50% a 65%, 65% ou mais.
- Em cada faixa, a regressão do T8 sem grupos (outros, queda do branco+nulo, variação do comparecimento, adversário, próprio), efeito fixo de local, erro agrupado por local; guarda o coeficiente dos próprios votos.
- A(ano) = média, ponderada pelo inverso da variância, sobre as faixas em que as duas candidaturas do ano têm pelo menos 30 locais, de [coeficiente próprio do candidato da direita - coeficiente próprio do candidato da esquerda]. É a comparação entre os dois finalistas do mesmo ano na mesma força local do adversário.
- Sinal de desvio contra Flávio que a força local não explica: A(2026) de -0,03 ou menos, a mais de 2,5 erros-padrão, e A(2026) - A(2018) de -0,03 ou menos, a mais de 2,5 erros-padrão. A(2022) é relatado: se também ficar em -0,03 ou menos, aponta para o mesmo mecanismo em 2022 ou para uma assimetria natural entre os campos, e o texto diz isso.
- Sem sinal: |A(2026)| até 0,015 e |A(2026) - A(2018)| até 0,015.
- Entre os dois: inconclusivo.
- Descritivo: os seis coeficientes por faixa, lado a lado, para ver se Flávio 2026 cai na curva comum.
- Limites: a ideia nasceu de um recorte já visto (regional); a amostra tem poucas seções por faixa e ano, então o veredito da amostra é preliminar e o do bweb é o que vale.

## Adendo 16 (26/10, noite, ~22h UTC, antes de rodar os testes abaixo): a fraude pelo lado do branco e nulo, no contexto de 2026

Pedido do Léo: partir da hipótese de que houve fraude e procurar onde ela deixaria marca, olhando o contexto de 2026 (apoios a Flávio depois do 1º turno, pesquisas, pausa da totalização) e não outras eleições. Duas formas de desvio pelo programa, com marcas diferentes:
- (A) conversão de branco e nulo em 13: o eleitor anula ou vota em branco e a urna grava 13 no boletim e no RDV. A contagem de Flávio fica intocada; Lula ganha o que seria branco e nulo.
- (B) troca de uma fração s dos votos de Flávio para Lula (Adendos 9 e 14).

O que já vi antes deste registro: a transferência declarada na Quaest por candidato eliminado (resultados/decomposicao_fluxos_2026.txt) e os coeficientes de Lula por candidato eliminado na amostra (T8 com grupos: Cury 0,54, Renan 0,49, Caiado 0,54, Zema 0,42). NÃO vi: os coeficientes de Flávio por candidato eliminado, os cruzamentos (voto no 1º turno contra voto no 2º) dos demais institutos, a comparação dos nulos por suspensão no log com os boletins, a tabela por UF de pontos ganhos entre turnos, nem nada por município do 2º turno.

### T36. Nulo atribuído por suspensão no log contra os nulos do boletim (amostra, já baixada)
- O log da urna registra "Atribuido voto nulo por suspensão [Presidente]" quando o eleitor sai sem concluir. É o único registro do log que diz o tipo do voto. Esse nulo tem de estar no boletim.
- Por seção, no dia 25/10, somando todos os logs do pacote: S = número desses eventos para Presidente; N = nulos de presidente no boletim do 2º turno. O mesmo no 1º turno (04/10), com N do bweb do 1º turno.
- Sinal de conversão de nulos (forma A ingênua, que converte todo nulo ou converte depois de gravar o log): pelo menos uma seção com N menor que S, sem explicação por contingência (pacote com mais de uma urna), conferida à mão.
- Sem sinal: nenhuma seção com N menor que S entre pelo menos 100 seções com S de 1 ou mais.
- Limite: uma conversão de só uma fração dos nulos, ou que poupe os nulos por suspensão, não deixa essa marca. É o teste da forma ingênua.

### T37. O que a urna diz que os eleitores dos eliminados fizeram, contra o que eles declararam (amostra agora; bweb depois)
- Urna: regressão do T8 com os grupos Cury (70), Renan (14), Caiado (55), Zema (30) e demais, para Lula e para Flávio, empilhada (efeito fixo de local por candidato, erro agrupado por local). b_L e b_F = fração dos eleitores de cada grupo no 1º turno que a urna põe em Lula e em Flávio no 2º; o resto (1 - b_L - b_F) é quem não votou num finalista.
- Declarado: cruzamento voto no 1º turno contra intenção no 2º turno na última pesquisa de cada instituto que publicar esse cruzamento (Quaest já conhecida; os demais buscados depois deste registro). Referência = mediana dos institutos para l (Lula), f (Flávio) e n (nenhum) de cada grupo.
- Medidas, com os quatro grupos somados pelo voto do 1º turno: dF = b_F - f; dL = b_L - l.
- Padrão da forma A (conversão de branco e nulo): |dF| até 0,07 e dL de 0,15 ou mais, a mais de 2,5 erros-padrão (erro da urna; a pesquisa entra como fixa e o texto diz isso).
- Padrão da forma B (troca de Flávio para Lula): dF de -0,07 ou menos e dL de +0,07 ou mais, os dois a mais de 2,5 erros-padrão.
- Sem padrão de fraude: |dF| e |dL| até 0,07.
- Qualquer outro resultado: inconclusivo.
- Limites: o lado de Lula (dL) já foi visto; o que separa A de B é dF, que não foi visto. Regressão ecológica entre seções e declaração em pesquisa erram, cada uma do seu jeito. Um padrão A também aparece se quem disse "nenhum" na pesquisa votou em Lula de fato (voto escondido ou decisão de última hora).

### T38. Pontos ganhos entre turnos, por UF e por município (descritivo)
- Para cada UF e cada município: ganho de Flávio e de Lula entre turnos em votos e em pontos da fatia dos válidos. Conta em quantos Flávio ganhou mais votos e mais pontos que Lula.
- Corte por força dos eliminados: o mesmo ganho relativo (Flávio menos Lula, em pontos) contra a fatia de Caiado, Renan, Cury e Zema no 1º turno do município. Descritivo.

### T39. Branco e nulo de presidente contra o de governador, 1º contra 2º turno, nas 6 UFs (estrato G, descritivo)
- R(t) = branco+nulo de presidente / branco+nulo de governador nas mesmas seções, no turno t. A forma A só no presidente baixa R(2) em relação a R(1). Sem referência de 2026 fora destas UFs; relatado com o T5 (beta de 0,468 em 2018 e 0,401 em 2022) e com R de 2018 e 2022 se as bases tiverem governador no 2º turno.

## Adendo 17 (27/10, ~02h UTC): correção de horários escritos à mão e de um desenho

Na conferência do README, um verificador comparou os horários escritos nos cabeçalhos com os dos commits. Os horários dos cabeçalhos foram estimados à mão e estão errados; vale o horário do commit (git log, UTC):
- Adendo 15: o cabeçalho diz "~21h15 UTC"; o commit f793d16 é de 21h04min07s. O resultado preliminar do T35 foi commitado às 21h08min31s (79c7d67), e o arquivo do resultado diz "~21h25 UTC" por engano.
- Adendo 16: o cabeçalho diz "~22h UTC"; o commit 618ebec é de 21h20min01s. Os primeiros resultados foram commitados às 21h25min57s (dec884c).
A ordem critério antes de resultado se mantém nos dois casos.

O T37 (Adendo 16) foi registrado com uma medida que não se interpreta: na especificação do T8, b_L + b_F = 1 por identidade, e a urna não identifica o "nenhum" dos eleitores dos eliminados. O veredito pela letra é inconclusivo, e a comparação corrigida (divisão entre os que escolheram um finalista) é post hoc. Isso já estava declarado em resultados/ADENDO16_resultados.txt; fica registrado aqui também.

## Adendo 18 (29/10/2026, antes de rodar qualquer teste abaixo): incoerências de lógica, sem usar outras eleições como referência

Pedido do Léo: partir da hipótese de que 2026 foi fraudada e de que 2018 e 2022 também podem ter sido, então nenhuma eleição anterior serve de régua. Procurar o que não faz sentido pela lógica dos fatos de 2026: dentro dos próprios dados de 2026 (mesma eleição, mesmas urnas, mesmos eleitores, outros cargos e outros registros da urna) e em fontes que não passam pela urna (pesquisas, apoios declarados, testes físicos, documentos públicos). A regra continua: o critério de cada teste fica escrito aqui antes de rodar, porque sem isso qualquer busca acha coincidências.

O que já vi e que toca estes testes (transparência): o T8 e o T35 (Flávio perde em termos líquidos uns 3,9% dos próprios eleitores; Lula, 1,3%), o T22b (o governador aliado de Flávio perde junto em AM, DF e ES), o T37 (eleitores dos eliminados mais para Lula na urna que nas pesquisas), o T11 e o T12 (erros das pesquisas), a variação por UF (flavio_por_uf.txt e T38) e os horários de encerramento (checagem do relatório do Instagram). Não vi: nada por faixa de voto do PL para deputado, a troca de urna e a data de carga em todas as seções, a ordem dos horários de cada boletim, os eleitores dos eliminados no estado de origem de cada um, nem o efeito do apoio dos governadores.

### L1. Horários impossíveis em todas as seções (bweb dos dois turnos)
- Por seção: abertura, encerramento, emissão do boletim, recebimento pelo TSE e data de carga da urna, com o fuso de cada município (deslocamento pela hora de abertura mais comum do município).
- Impossível: encerramento antes das 17h00 de Brasília com comparecimento acima de zero; emissão do boletim antes do encerramento; recebimento antes da emissão; abertura antes das 7h ou depois das 10h de Brasília sem urna de contingência; carga fora da janela de carga do turno na UF.
- **Sinal:** 100 ou mais seções impossíveis no 2º turno sem explicação por fuso, contingência ou junta, ou qualquer número delas em que a virada de Lula supere a das outras seções do mesmo local em 3 pontos ou mais. **Sem sinal:** nenhuma seção impossível sem explicação. Entre os dois: inconclusivo, com a lista das seções para conferência.

### L2. Urna trocada entre os turnos e carga fora do padrão (bweb completo)
- Grupos: seções cujo número de urna mudou entre o 1º e o 2º turno; seções cuja data de carga do 2º turno fica fora da faixa entre os percentis 1 e 99 da sua UF.
- y = virada de Lula (fatia entre os dois finalistas, 2º menos 1º turno), efeito fixo de local, erro agrupado por local, peso pelos votos dos finalistas.
- **Sinal:** algum grupo com 500 seções ou mais e diferença de 1,0 ponto ou mais a favor de Lula, a mais de 4 erros-padrão. **Sem sinal:** diferença abaixo de 0,3 ponto em valor absoluto, com erro-padrão até 0,15. Entre os dois: inconclusivo.

### L3. O núcleo do PL: quem é do PL perde eleitor para Lula?
- Lógica: o eleitor mais partidário é o que menos troca de lado. Se Flávio perdeu eleitores por comportamento, a perda tem de ser pequena onde o PL é muito forte. Se uma fração fixa dos votos dele foi desviada, a perda fica parecida em todo lugar.
- Força do PL na seção: fatia do PL (nominal mais legenda, número 22) nos votos válidos para deputado federal no 1º turno de 2026, na mesma urna. Quintis de seções por essa fatia.
- Em cada quintil, a regressão do T8 (ganho de Flávio contra os votos de cada grupo no 1º turno, a queda do branco+nulo e a variação do comparecimento; efeito fixo de local; erro agrupado por local); guarda o coeficiente dos próprios votos de Flávio (P1 a P5). O mesmo para Lula com a fatia do PT para deputado federal.
- **Incoerência a favor da tese:** P5 (núcleo do PL) de -0,03 ou menos, a mais de 3 erros-padrão, e P5 não menor que P1 em valor absoluto por mais de 0,01. **Coerente com comportamento:** |P5| até metade de |P1|. Entre os dois: inconclusivo.

### L4. Os eleitores dos candidatos que apoiaram Flávio, no estado de cada um
- Lógica: Caiado (GO) e Zema (MG) apoiaram Flávio e governam esses estados; Cury (SP) também apoiou. Os eleitores deles no 1º turno deveriam ir mais para Flávio que para Lula, principalmente em casa.
- Em GO (Caiado), MG (Zema) e SP (Cury): regressão do T8 com os grupos dos eliminados, dentro da UF, efeito fixo de local. s = b_L / (b_L + b_F) para o grupo do candidato da casa: fatia de Lula entre os eleitores dele que a urna põe num finalista.
- Referência externa (não passa pela urna): a mesma fatia declarada nas pesquisas do 2º turno com cruzamento por voto no 1º turno (mediana dos institutos; Quaest já conhecida: Caiado 36%, Cury 47%, Zema 36%).
- **Incoerência:** s acima de 50% e acima da referência das pesquisas em 15 pontos ou mais, a mais de 3 erros-padrão, em pelo menos 2 das 3 UFs. **Coerente:** s até a referência mais 5 pontos nas 3. Entre os dois: inconclusivo. Limite: a regressão entre seções erra quando o eleitor de um candidato mora junto com outro tipo de eleitor; o resultado é indício, não prova.

### L5. Pesquisas, que não passam pela urna
- (a) Para cada instituto com pesquisa final nos dois turnos: erro de Flávio (urna menos pesquisa, nos válidos) no 1º e no 2º turno. **Incoerência:** em pelo menos 6 dos institutos, Flávio acima da pesquisa no 1º turno e abaixo dela no 2º, com virada média de 4 pontos ou mais. **Coerente:** sinais iguais nos dois turnos na maioria.
- (b) O "saldo" de quem não votou num finalista no 1º turno (branco, nulo, abstenção e eleitor de eliminado que as pesquisas davam como "nenhum"): pela urna e pelas transferências declaradas, a fatia desse saldo que foi para Lula. Comparar com a divisão entre Lula e Flávio dos indecisos, brancos, nulos e "não vai votar" nas pesquisas finais do 2º turno, quando o instituto publicar. **Incoerência:** fatia de Lula pela urna acima da maior fatia das pesquisas em 30 pontos ou mais. Sem a divisão publicada, só descritivo.

### L6. O apoio dos governadores
- Lógica: governador eleito no 1º turno que fez campanha para um candidato puxa voto para ele no estado.
- Lista fixada antes de cruzar com o resultado (fontes de imprensa, por um agente que não vê a virada): para cada UF com governador eleito no 1º turno, o apoio declarado no 2º turno (Flávio, Lula ou neutro) e a votação do governador no 1º turno.
- Medida: virada de Lula por UF (pontos entre os dois finalistas) contra o apoio, ponderada pelos votos, e contra a votação do governador.
- **Incoerência:** a virada de Lula nos estados com governador pró-Flávio não é menor que nos demais (diferença de zero ou mais). **Coerente:** menor em 1 ponto ou mais. Entre os dois: inconclusivo. Limite: são poucos estados e o apoio não é aleatório.

### L7. O que uma fraude no programa teria de driblar (pesquisa, sem critério numérico)
- Como funcionou o teste de integridade do 2º turno de 2026 (quantas urnas, se usa eleitores reais e biometria, se a urna consegue saber que está em teste), o que dizem os relatórios e as auditorias de partidos, inclusive do PL. Lista do que uma fraude no programa precisaria fazer para passar por cada controle. Relatado como argumento, sem veredito.

### L8. O "dossiê" dos EUA citado na imprensa (pesquisa)
- Achar o documento ou a reportagem, separar o que é afirmação técnica conferível nos dados públicos e conferir cada uma; o que não for conferível é relatado como tal.

## Adendo 19 (29/10/2026, 08h08 UTC, depois de rodar o Adendo 18): errata

1. L4: os valores de referência escritos no Adendo 18 como "Quaest já conhecida: Caiado 36%, Cury 47%, Zema 36%" não são da Quaest publicada. Saíram de `resultados/decomposicao_fluxos_2026.txt`, montado com números ainda não conferidos, e o 47% de Cury era a fatia de Flávio (a de Lula seria 53%). O critério manda usar a mediana dos institutos, e foi o que o teste usou, com os valores conferidos em `resultados/contexto_2t_2026_pesquisa_verificada.json`. Com os números do registro, com os conferidos ou com qualquer outra leitura testada, o veredito é o mesmo (INCONCLUSIVO).
2. Nada mais do Adendo 18 foi alterado. Os resultados estão em `resultados/ADENDO18_resultados.txt` e em `resultados/testes_adendo18_com_conferencia.json`, com as correções apontadas pelas conferências.

## Adendo 20 (30/10/2026, antes de rodar qualquer teste abaixo): testes forenses nos boletins que ainda não foram feitos

Pedido do Léo: com todos os dados, principalmente os boletins de urna, apontar onde há possibilidade de fraude e trazer os dados que possam dar pistas, com testes estatísticos. Regra do Adendo 18 mantida: nenhuma eleição anterior como régua. Os controles são o 1º turno de 2026 nas mesmas seções, simulações de contagem limpa (sorteio binomial a partir da fatia da própria seção ou do local) e o lado de Flávio como espelho. Ficam de fora o que já rodou com o bweb completo: canto de comparecimento extremo (T28), componente de zona e degrau na fronteira (T23), liberação sem biometria em média (T21), troca uniforme e governador (T14, T16, T22b).

### F2. Dígitos, porcentagens redondas e boletins repetidos (todas as seções do Brasil; exterior fora)
- (a) Último dígito dos votos de Lula e de Flávio por seção, só contagens de 50 ou mais. Estatística: qui-quadrado contra uniforme. Referência: 200 simulações em que cada contagem é sorteada de uma binomial com a fatia do local de votação da seção, mesmo total de válidos. Sinal: o qui-quadrado observado de Lula ou de Flávio no 2º turno passa do percentil 99,9 das simulações e o do mesmo candidato no 1º turno fica abaixo do percentil 99. Sem sinal: abaixo do percentil 95 nos dois candidatos no 2º turno. Entre os dois: inconclusivo.
- (b) Porcentagens redondas: fração de seções em que 100 x Lula / válidos, ou 100 x comparecimento / aptos, cai a 0,1 ponto ou menos de um múltiplo de 5. Mesma referência simulada. Sinal: excesso do observado sobre a média simulada acima de 4 desvios-padrão da simulação no 2º turno, para Lula ou para o comparecimento, e pelo menos o dobro do excesso padronizado do 1º turno. Sem sinal: dentro de 2 desvios-padrão. Entre os dois: inconclusivo.
- (c) Boletins repetidos: pares de seções da mesma zona com Lula, Flávio, branco e nulo idênticos no 2º turno, comparecimento de 100 ou mais. Esperado pela mesma simulação. Sinal: observado de pelo menos 3 vezes o esperado e 20 pares ou mais. Sem sinal: até 1,5 vez o esperado.

### F4. Modelo de urna no bweb inteiro
- Mapa do número da urna para o modelo pelos logs da amostra (o log informa o modelo; o boletim, o número). Só se aplica ao bweb se as faixas forem limpas: cada faixa com um modelo só em 99% ou mais das urnas da amostra. Se não forem, o teste fica SEM PODER.
- Virada de Lula (fatia entre os dois finalistas, 2º turno menos 1º) com efeito fixo de local, erro agrupado por local, peso pelos votos dos finalistas no 2º turno, um indicador por modelo (referência: o mais comum). Placebo: a fatia do 1º turno como variável.
- Sinal: algum modelo com 5.000 seções ou mais e diferença de 1,0 ponto ou mais a favor de Lula, a mais de 4 erros-padrão. Sem sinal: todos com diferença abaixo de 0,3 em valor absoluto e erro-padrão até 0,15. Entre os dois: inconclusivo.

### F5. Caudas: seções que destoam do previsto pelo próprio 1º turno
- Previsão: a regressão do T8 com efeito fixo de local (ganho de Lula e de Flávio contra os votos do 1º turno da seção) dá L2 e R2 previstos e a fatia prevista p. Para cada seção, z = (fatia observada - p) / raiz(p(1-p)/n), n = votos dos finalistas no 2º turno.
- Sinal: o número de seções com z acima de +4 é pelo menos 1,3 vez o de seções com z abaixo de -4, com 200 ou mais acima de +4, e pelo menos 30% das seções acima de +4 ficam em até 10 zonas. Sem sinal: razão entre 0,8 e 1,25. Entre os dois: inconclusivo. Relatar também a margem líquida movida pelas duas caudas.
- Arquivos de urna: boletim, RDV, log e assinatura das 30 seções com maior z e das 10 com menor z. Sinal no arquivo: assinatura inválida, boletim diferente do bweb, RDV diferente do boletim, votos no log diferentes do comparecimento, ou anomalia A2 a A5 do T3, em qualquer uma delas.

### F6. Eleitor a mais sem biometria, nas pontas
- Do bweb dos dois turnos: variação das liberações sem biometria (QT_ELEI_BIOM_SEM_HABILITACAO, 2º turno menos 1º) sobre os aptos. Grupo: o 1% de seções com a maior variação, desde que a variação seja de 10 ou mais.
- Virada de Lula do grupo contra as outras seções do mesmo local (efeito fixo de local, erro agrupado por local, peso pelos votos dos finalistas no 2º turno). Sinal: diferença de 2,0 pontos ou mais a favor de Lula, a mais de 4 erros-padrão, com 1.000 seções ou mais no grupo. Sem sinal: diferença abaixo de 0,5 em valor absoluto com erro-padrão até 0,25. Entre os dois: inconclusivo.
- Logs: 40 seções do grupo e 40 de controle sorteadas nos mesmos locais (semente 20261030). Rajada de fim de dia = 10 ou mais habilitações sem biometria depois das 16h locais. Sinal no log: a fração de seções do grupo com rajada é pelo menos 3 vezes a dos controles e são 5 seções ou mais.

### F8. O que os EUA e os observadores disseram (pesquisa, sem critério numérico)
- Texto, data e órgão de cada declaração do governo dos EUA sobre o 2º turno de 2026, se fala em indícios de fraude e quais; relatórios de observação internacional (OEA, UE, Centro Carter, Parlasul e outros); posição e auditoria do PL. Cada indício concreto que der para conferir nos dados públicos é conferido; o que não der é relatado como tal.

## Adendo 21 (31/10/2026, antes de rodar qualquer teste abaixo): o que dá para fazer sem pedir nada a ninguém

Pedido do Léo: fazer tudo o que não depende de pedir algo a alguém. Regra do Adendo 18 mantida (nenhuma eleição anterior como régua). Os dados de trabalho foram movidos para /home/user/trabalho-eleicao (fora do repositório), com os mesmos arquivos.

### F9. Computador que gerou a mídia de resultado do 2º turno
- No 2º turno a urna fica com a carga do 1º e recebe uma mídia nova, gerada nos computadores das zonas. O log registra "MR gerada pelo computador", a data e o usuário. Uma mídia adulterada num computador apareceria nas urnas dele.
- Para cada seção da amostra de logs: resíduo da virada de Lula (fatia entre os finalistas, 2º turno menos 1º) contra as outras seções do mesmo local no bweb, ponderado pelos votos dos finalistas. Média do resíduo por computador. Estatística: variância ponderada entre computadores; referência: 2.000 permutações dos computadores entre as seções da mesma UF.
- Sinal: p da permutação abaixo de 0,001 e pelo menos um computador com 10 ou mais seções da amostra e resíduo médio de +2,0 pontos ou mais a favor de Lula a mais de 4 erros-padrão. Sem sinal: p acima de 0,05. Entre os dois: inconclusivo.
- Descritivo: datas de geração da mídia fora da janela de 05 a 23/10, usuário e computador fora da zona da seção.

### F10. Urnas antigas: o mesmo desvio aparece nos outros cargos?
- Nos locais com urna antiga (UE2013 ou UE2015) e nova (UE2020 ou UE2022) no 1º turno: diferença antiga menos nova, dentro do local, na fatia de Lula entre os finalistas (presidente) e num índice de perfil feito só com os outros cargos do 1º turno (fatia da federação PT/PCdoB/PV nos válidos para deputado federal e para deputado estadual, e fatia do candidato a senador do campo de Lula, quando houver).
- Escala: inclinação b da fatia de Lula sobre o índice, entre seções, dentro do local, nas seções desses locais. Estatística: D = (diferença no presidente) - b x (diferença no índice), erro por bootstrap de locais (2.000).
- Sinal de máquina: D de +0,5 ponto ou mais a mais de 3 erros-padrão. Sem sinal: |D| abaixo de 0,3 com erro-padrão até 0,2. Entre os dois: inconclusivo.

### F11. Arquivos públicos do teste de integridade do 2º turno
- Achar o que o TSE e os TREs publicaram (lista de urnas, relatórios, boletins, logs, RDV, vídeos, contagem das cédulas). Se houver arquivos de urna: conferir boletim contra a contagem das cédulas, versão do programa e verificação de assinatura no log contra as urnas reais, e o modo de habilitação usado. Sinal: alguma urna de teste com boletim diferente das cédulas sem explicação documentada, ou com programa diferente das urnas reais. Sem critério para o resto.

### F12. Certificados e resumos dos programas
- Achar os certificados públicos da AC URNA, AC UE2020 e AC UE2022 e conferir, com código próprio, se os certificados das urnas da amostra foram assinados por elas e em que prazo de validade. Conferir a alegação de que o certificado da AC URNA venceu em 18/07/2026. Achar os resumos digitais publicados dos programas lacrados em 04/09 e comparar com qualquer resumo obtenível dos arquivos de urna. Sinal: certificado de urna que não se valida pela AC publicada, ou resumo de programa diferente do publicado. Sem critério para o resto.

### F13. Pesquisas independentes da urna
- Pesquisas feitas depois da eleição com a lembrança do voto nos dois turnos, boca de urna do dia 25/10 e os relatórios finais completos (com tabelas cruzadas) dos institutos. Para cada uma: fatia de Lula entre os eleitores dos eliminados que escolheram um finalista. Descritivo, com a régua: "confere com a urna" se ficar a 5 pontos ou menos de 52% a 54%; "confere com as pesquisas de antes" se ficar entre 32% e 44%; entre os dois, intermediário.

### F14. Casos pendentes, arquivo por arquivo
- Boletim, RDV, log e assinatura de: as 37 seções com mais de 80% de liberação sem biometria nos dois turnos (F6), ES|56995|53|978 e as outras seções do local, as 17 seções da zona 90 de Volta Redonda mantidas abertas, AC|1554|3|160, AC|1040|4|160, AC|1066|4|313, RR|3026|6|97 e AM|2097|18|37 e 39; e o 1º turno de AM|2399|45|63 se o arquivo existir. Sinal: assinatura inválida, boletim diferente do bweb, RDV diferente do boletim, votos no log diferentes do comparecimento, ou anomalia A2 a A5. Descritivo: quem liberou (mesário identificado ou não), horário das liberações e contingências.

### F15. Quem foi votar a mais: perfil do comparecimento
- Dado aberto do TSE de comparecimento e abstenção por zona, faixa etária, gênero e escolaridade, nos dois turnos de 2026.
- (a) Conferência: comparecimento por zona no perfil contra a soma do bweb. Sinal: alguma zona com diferença acima de 0,5% sem explicação.
- (b) Entre as zonas da mesma UF, relação entre a variação do comparecimento de 16 a 34 anos (em pontos) e a virada de Lula na zona, ponderada pelos votos dos finalistas. Incoerência: inclinação negativa a mais de 3 erros-padrão. Coerente: positiva a mais de 3 erros-padrão. Entre os dois: inconclusivo.
- (c) Descritivo: variação do comparecimento por faixa etária, gênero e escolaridade no país.
