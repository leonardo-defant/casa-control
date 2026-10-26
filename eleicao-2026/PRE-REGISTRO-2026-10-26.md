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
