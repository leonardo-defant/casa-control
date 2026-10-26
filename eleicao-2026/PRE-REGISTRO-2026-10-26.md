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
