# Eleição presidencial de 2026, 2º turno: investigação de fraude

Ponto de entrada da pesquisa. Reúne a situação, a tese e os argumentos do Léo (dono da pesquisa), os fatos levantados e conferidos, cada teste feito com o resultado, e o que falta. Atualizado em 27/10/2026, madrugada (UTC). Os números deste arquivo foram conferidos contra os arquivos de `resultados/` por verificadores independentes; onde a fonte é fraca ou o veredito é só descritivo, isso está dito.

Leitura sugerida:
1. Este arquivo, inteiro.
2. `PRE-REGISTRO-2026-10-26.md`: os critérios de cada teste (T1 a T6 no registro inicial, os demais nos adendos 1 a 17), escritos antes de ver os dados. Vale o horário do commit (o Adendo 17 corrige horários escritos à mão nos cabeçalhos).
3. `PARA-O-REVISOR.md`: passagem para o revisor cético (Codex), com "onde eu posso estar errado" e como reproduzir. É anterior aos adendos 14 a 17.
4. `CONTEXTO-ELEICAO-2026-original.md`: o documento que abriu a sessão (robô de apuração, primeiras análises, critérios da seção 7).
5. `resultados/`: um arquivo por teste ou levantamento. Os citados aqui estão entre crases.

---

## 1. A situação e a pergunta

O 2º turno foi em 25/10/2026, entre Lula (PT, 13) e Flávio Bolsonaro (PL, 22). Flávio venceu o 1º turno por 2,22 milhões de votos e chegou ao 2º com o apoio da maior parte da direita e de parte do centro. Lula venceu o 2º turno por 4,43 milhões.

O Léo acredita que a eleição foi fraudada. Ele pediu uma investigação que parta desse pressuposto: pensar como quem fraudaria, procurar onde a fraude deixaria marca e testar cada ponto com dado público e critério definido antes. Pediu também que a análise olhe o contexto de 2026, e não outras eleições, e disse, quando achou que a análise estava contestando os argumentos dele em vez de investigar: "acho que vc perdeu o contexto do que precisamos fazer nessa sessão, e vc está me refutando ao invés de tentar entender o que aconteceu". Isso convive com o combinado do início (documento original, seção 0): ceticismo nos dois sentidos, contrapontos com dados, resultados relatados sem suavizar para nenhum lado.

Repositório futuro: o Léo informou na conversa (26/10, 14h10 UTC) que criou o repo `eleicoes-2026` para receber todo o contexto desta pesquisa e trabalhar com o Codex como revisor cético. Esta pasta será movida para lá quando ele pedir.

## 2. Números oficiais

| | 1º turno (04/10) | 2º turno (25/10) | Variação |
|---|---|---|---|
| Flávio Bolsonaro (22) | 56.104.503 (47,03% dos válidos) | 59.826.041 (48,21%) | +3.721.538 |
| Lula (13) | 53.879.538 (45,16%) | 64.256.232 (51,79%) | +10.376.694 |
| Augusto Cury (70) | 3.448.569 | | |
| Renan Santos (14) | 2.675.887 | | |
| Ronaldo Caiado (55) | 2.605.148 | | |
| Romeu Zema (30) | 326.488 | | |
| Demais candidatos | 260.655 | | |
| Brancos + nulos | 4,77% do comparecimento (5.975.047) | 3,24% (4.153.801: brancos 1.430.496, nulos 2.723.305) | -1.821.246 |
| Abstenção | 21,08% | 19,22% | comparecimento +2.960.239 (128.236.074 no 2º turno) |

Fontes: 1º turno, votos por candidato pela soma das seções do bweb (`resultados/candidatos_1t_2026_totais.txt`; o 28, candidatura anulada, conta como nulo); brancos (2.300.798), nulos (3.674.249, com os 5.246 do 28), comparecimento (125.275.835) e abstenção (21,08%) do arquivo oficial do TSE (`CONTEXTO-ELEICAO-2026-original.md`, seção 1), iguais à soma do bweb. 2º turno, soma dos 28 arquivos por UF e exterior do TSE (`PARA-O-REVISOR.md`, seção 1); o arquivo nacional do TSE (gerado em 25/10 às 23h27min02s) dá os mesmos 1.430.496 brancos e 2.723.305 nulos da soma dos boletins completos (bweb); os números 10 votos menores (1.430.493 e 2.723.298) aparecem só em parte da imprensa (correção de 29/10, conferida no T15). Parte da imprensa deu 19,21% de abstenção com 99,91% das seções.

A conta que fecha por identidade: o que os dois finalistas ganharam juntos (+14.098.232) é igual aos votos dos eliminados (9.316.747) mais o aumento do comparecimento (+2.960.239) mais a queda do branco e nulo (+1.821.246). O que está em discussão não é se a soma fecha, e sim como esse total se dividiu.

Para referência (base de 2022 por seção): Bolsonaro teve 51.072.345 votos no 1º turno de 2022 e 58.206.354 no 2º; Lula teve 57.259.504 e 60.345.999.

## 3. A tese e os argumentos do Léo, nas palavras dele

Trechos das mensagens do Léo (documento original, seção 0.1, e mensagens desta sessão), com ajustes mínimos de digitação.

**A tese.**
- Variante inicial: "Eu tenho uma teoria, eleição é fraudada, e o que me leva a crer é que Barroso exerceu sua força pra barrar o voto impresso! O que eu acho é que de alguma forma eles alteram os votos brancos e nulos, por isso o roubo deles é limitado e eles não conseguem roubar sempre, nem vencer eleições regionais, deputados e senadores."
- "Minha tese sobre os brancos e nulos é sobre um valor não sabido, e não sobre a comparação do primeiro com o segundo turno. Afinal, a gente não tem a fotografia real, só a visão da urna."
- "Se alguém fosse roubar, não ia fazer isso de forma perceptível."
- "Como pode acontecer um erro generalizado das instituições de pesquisa, juntamente com a situação do Barroso, do Zanin e com os relatos de fraudes da Venezuela? Somando aos fatos inéditos de brancos, nulos e abstenções."
- Variante desta sessão: "Não acredito que haja fraude no número de eleitores. Isso é mais fácil de pegar, mas vamos verificar. Minha suspeita é que o sistema da urna é corrompido. Minha tese é que eles programaram o desvio previamente e erraram a mão, pq o resultado do Lula não é explicável estatisticamente."
- "Vc não pode afirmar que o programa da urna é seguro! Olhe as falhas que foram descobertas no php nessa semana! Enfim nenhum sistema é seguro hoje! Imagina um que nem teve escrutínio público amplo pra avaliação."
- "A gente não vai conseguir identificar se existe um malware no sistema ou não. Porque isso só se a gente auditasse o código, e isso é impossível. O que que a gente tem que tentar entender? É a discrepância que possa existir entre os dados reais das urnas, que já pode ser, e na tese seria o dado já corrompido, e a lógica do mundo real, onde as pesquisas e a lógica sobre transferência de votos, sobre esquerda, direita, rejeição do Lula, dados históricos de abstenção, brancos e nulos (...) mostrariam uma falta de lógica nos resultados."
- "Lembrando que não houve carga nova de sistema nas urnas. Pode ter havido, sim, um malware quando colocaram os candidatos novos. Mesmo não sendo o mesmo sistema, eu sei. Pode ter havido também que esse sistema é corrompido desde o começo. Pode ter havido inúmeras outras situações que a gente não tem ideia e não tem como afirmar. Então a gente parte do pressuposto de que a urna não é confiável, porque não é."
- Contestando a leitura de que o branco e nulo estava limpo: "Os brancos e nulos, no caso de fraude, não são convertidos porque eles são intocados. Esse é o dado que você está vendo, né? Mas e se esse dado já foi fraudado? E não tem como saber quem votou branco e nulo, como o voto é secreto. Mas imagina se o malware converte esses dados automaticamente de branco e nulo."

**A conta.**
- "Tinha aprox 9 milhões de votos de outros candidatos pra migrar (quase todos apoiaram Flávio e nenhum Lula). Tiveram 3 milhões a mais de votantes (que já não é normal). E tinham mais 5 milhões de brancos e nulos tomando lado (que já não é normal tbm). Flávio fez 3,6 mi de votos a mais, que é menos de 50% dos votos de outros candidatos, Lula teria que ter feito 100% do resto, o que é praticamente impossível. Mas essa é uma análise macro. Os votos não são os mesmos, votantes podem ter saído e entrado e a gente só vê a soma estatística, mas tbm não é fácil comprovar que houve tanta mudança. Como averiguar?"
- "Flávio teria que converter apenas 40% (no máximo) dos votos de outros candidatos, Lula 100% do restante de 60% dos votos que sobraram, 100% dos votos brancos e nulos convertidos e 100% da abstenção negativa. Correto?"
- "Dos 9,2 milhões de votos dos outros candidatos é natural que houvesse boa parte de abstenção já, de eleitores deles que não iriam votar ou votar brancos e nulos, então se a abstenção caiu e brancos e nulos também, quer dizer que ainda mais eleitores novos apareceram pra compensar esse que naturalmente não iriam. Segundo ponto é sobre esses seriam massivamente do Lula, quase 100%. O que não faz sentido." "E também pesquisar sobre a quantidade total de votos do primeiro e do segundo turno das eleições anteriores em %, pq me parece que nesse o % de votos cresceu consideravelmente sobre o que 'deveria' ter sido estatisticamente."
- "Vc está dizendo que entre todo mundo que saiu e entrou o saldo é 100% pro Lula, como vc disse, é saldo, e se for por esse lado a conta fica ainda pior, pq do lado do Lula não saiu ninguém." "Isso prova uma anomalia ABSURDA e inédita, vc não tem que se preocupar com a matemática, ela vai fechar, invariavelmente."
- "Lula ganhar estaria dentro da margem de erro de algumas pesquisas, mas ganhar 11 milhões de votos dentro desse universo foi escrachado."

**A lógica política.**
- "Não se esqueça, ao comparar com outras eleições, não existiam candidatos de esquerda pra uma transferência expressiva de votos de candidato pra candidato. Flávio fez 47% no primeiro turno tendo outros vários candidatos com o mesmo apelo anti PT como concorrentes; o natural seria a transferência de votos, como nos outros anos, ser dele, e não de Lula! A ideia da lógica, ao meu ver, seria Flávio fez uma votação X no primeiro turno e teria um crescimento de votos e % no segundo, tal como Bolsonaro em 2022."
- "São todos contra o PT no Brasil, e a conta não fecha. Não existe transferência de votos de PL pra PT, existe de qualquer outro pra contra PT."
- A falta de lógica "desse candidato ter ganho 11 milhões de votos em cima daquilo que parecia já ser o teto de votos, ou muito próximo do teto que ele já havia", e o "aumento da participação da fatia final do Lula em estados que são predominantemente de direita", que "mostrariam uma falta de lógica nos resultados, não estatística".
- "Flávio não cresceu em nenhum estado entre primeiro e segundo turno, levando em consideração o apoio dos outros candidatos, não faz sentido estatisticamente." "Sobre Flávio não crescer estou falando crescer em %." Depois: "ele não conseguiu em nem um estado ter um saldo positivo em percentual de votos em relação ao Lula? Nenhum estado ele ganhou mais pontos do que o Lula de um turno para o outro? E por município também?"
- "E se existiu aumento da abstenção onde Flávio prioritariamente ganhou, a queda de abstenção, que já é questionável, pode ser ainda maior se levarmos em consideração estados que Lula estava à frente e fez ainda mais % de votos."
- "94% dos municípios do Brasil tiveram uníssonos Lula à frente [no ganho de votos entre os turnos; ver seção 5.1], levando em consideração todo o contexto que te passei! É praticamente impossível!"

**O contexto que ele apontou** (mensagem de 26/10, 21h14 UTC; conferido na seção 4): "a direita, o Flávio, elegeu a maior bancada da história do Congresso Nacional", "mais de 120 pessoas só do PL, fora o resto de direita"; "mais de 50% já do Senado"; "a maioria dos governadores apoiaram o Flávio" e "o apoio massivo de todos os governadores eleitos de direita"; Michel Temer e outros políticos do centro com Flávio; os derrotados do 1º turno com Flávio; "as pesquisas colocando ele na frente"; "os trackings internos, tanto do PT quanto do Flávio, apontando que ele tinha 4 a 6 pontos de vantagem"; "ele foi melhor em todos os debates"; "o Flávio ter feito uma votação recorde, mais do que o Bolsonaro no segundo turno da eleição anterior, no primeiro turno"; "o fato do ex-advogado dele [de Lula] paralisar a apuração da eleição depois das 17 horas"; "a maior conversão de brancos e nulos, 60% e poucos% negativo, a menor abstenção do primeiro para o segundo turno, com 3 milhões de eleitores a mais". Depois acrescentou: "Trump e Musk acusam a eleição de fraude."

**Sobre pesquisas.** "Leve em consideração prioritariamente as pesquisas que mais acertaram, Veritá e Gerp." "Existem também pesquisas que têm claramente um viés de esquerda e que estiveram envolvidas em escândalos ali recentemente, por exemplo, do Banco Master, recebendo patrocínios e sendo contratadas para palestras. Então a gente tem que buscar também as pesquisas que são mais isentas e que tiveram a melhor assertividade aí nos últimos anos."

**Como investigar.** "Pensarmos pela cabeça de quem tentaria fraudar a eleição. Ele saberia que isso seria averiguado pelo mundo todo posteriormente, a pergunta é: como essa pessoa agiria e como ela tentaria fraudar a eleição? Difícil saber, mas aonde esses números seriam refletidos na apuração? Aonde pode haver pistas da fraude e onde a lógica não faz sentido?" "Estamos atrás de uma conspiração e vc tem que tentar enxergar o que ninguém vê! Como roubar uma eleição com urnas opacas sem deixar evidências estatísticas... acho que eles falharam pq a lógica não vai fechar essa conta." "Eu não quero que você fique analisando outras eleições, compare o contexto do agora. E veja se existe lógica nisso. Porque não existe. E a gente tem que pensar pelo lado de que alguém fraudou essa eleição e tentar descobrir como e onde."

**O reel que ele trouxe** (Alex Ribeiro, @lex.rill, 26/10). Afirmações centrais do vídeo: (1) "0 em 7": desde 1989, quem venceu o 1º turno sempre venceu o 2º; (2) "3 em 1000": pela margem de erro das pesquisas da véspera (Datafolha e Quaest, Flávio 51 x 49), essa seria a chance de Lula chegar a 51,8%; (3) Lula ficou com 3 em cada 4 dos 14,1 milhões de votos em jogo, e mesmo com todos os novos eleitores e todo o branco e nulo "faltam 5,6 milhões", o que exigiria que 6 em cada 10 eleitores de Cury, Santos, Caiado e Zema migrassem para Lula. A conferência está na seção 4.

## 4. O contexto, conferido

Pesquisa em várias frentes, cada uma com verificador independente que reabriu as fontes. Detalhes e links em `resultados/contexto_2t_2026_e_onde_estaria_a_fraude.txt`, `resultados/contexto_2t_2026_pesquisa_verificada.json` e `resultados/trump_musk_2t_2026_verificado.json`.

| O que foi dito | O que as fontes mostram |
|---|---|
| Maior bancada da história do Congresso; mais de 120 deputados só do PL | 121 deputados do PL: a maior bancada de um partido desde 1988. Não é a maior da história: o PMDB fez 260 em 1986 |
| Direita com mais de 50% do Senado | Sim, pelos dois critérios encontrados: PL 29 de 81 (maior bancada em início de legislatura desde 1988); PL, PP, União, Republicanos, Novo e Podemos somam 50 de 81 (classificação nossa, por partido); o Poder360 conta 49 de 81 "mais à direita". Ainda depende do caso Dallagnol no TSE |
| A maioria dos governadores apoiou Flávio; todos os eleitos de direita | 12 dos 21 eleitos no 1º turno (GO, MT, MS, MG, PA, PR, RJ, RS, RO, RR, SC, SP). 5 apoiaram Lula, todos no Nordeste (BA, CE, PB, PI, SE), e 4 ficaram neutros (AL, AP, MA, PE) |
| Os derrotados apoiaram Flávio | Zema; Caiado (pessoalmente; o PSD ficou neutro); Clariana e Grassi (com condições); Cury (com uma carta de 8 compromissos, depois de anunciar neutralidade em 05/10). Renan Santos liberou os eleitores. Samara, Hertz e Edmilson foram de Lula (voto crítico); o PCO pediu voto nulo |
| Temer e o centro com Flávio | Temer apoiou em 05/10. União, PP, Novo, Republicanos (com exceção dos diretórios da PB e de PE) e Podemos (sem punir quem fizesse campanha para Lula) também. O MDB se dividiu (17 de 27 diretórios com Flávio). O PSD ficou oficialmente neutro e o PSDB liberou os filiados |
| Pesquisas com Flávio na frente | 11 dos 12 institutos, na última pesquisa de cada um antes do 2º turno (campos entre 18 e 24/10), com 50,1% a 52% dos válidos. Só o Vox Brasil tinha Lula à frente |
| Trackings do PT e da campanha de Flávio com Flávio 4 a 6 pontos à frente | Os "4 a 6 pontos" vêm de um interlocutor anônimo (Metrópoles, 21/10). No dia seguinte, o tracking principal do PL foi descrito com Flávio +3. Os do PT davam 50 x 50, Lula +1 (Edinho Silva) e Lula 50,6 x 49,4 (Rafael Fonteles) |
| Flávio melhor em todos os debates | Lula e Flávio se enfrentaram em 2 debates, ambos no 2º turno (Band em 18/10 e Globo em 23/10). Nenhuma pesquisa representativa mediu quem foi melhor: só um estudo qualitativo com 12 eleitores e opiniões de comentaristas |
| Votação recorde de Flávio, mais que Bolsonaro no 2º turno anterior | Não é recorde. Flávio teve mais votos que Bolsonaro em 2022 no 1º turno (56,10 contra 51,07 milhões) e no 2º (59,83 contra 58,21), mas no 1º turno de 2026 teve menos que Bolsonaro no 2º turno de 2022 (56,10 contra 58,21) e menos que Lula no 1º turno de 2022 (57,26) |
| Maior conversão de branco e nulo, menor abstenção, 3 milhões a mais | O aumento do comparecimento entre turnos (+1,86 ponto) e dos válidos sobre o eleitorado (+3,01) é o maior da série 2002 a 2026; pela tendência de 2010 a 2022 seria +1,57. A abstenção de 19,22% é a menor em 2º turno em 20 anos (TVT, Agência Brasil). A queda do branco e nulo (-32%) fica dentro da faixa de 2002 a 2014 (-22% a -42%), mas em 2018 e 2022 ele tinha subido entre turnos (`resultados/historico_comparecimento_bn.txt`) |
| O ex-advogado de Lula paralisou a apuração depois das 17h | Cristiano Zanin (STF, ex-advogado de Lula na Lava Jato, indicado por ele), sorteado relator às 16h33 de uma reclamação da coligação de Lula (falta de ônibus em Salvador, Feira de Santana e Lauro de Freitas), prorrogou a votação até as 19h "em todas as seções de todo o Brasil" em liminar divulgada às 17h03; em seguida, numa nota de esclarecimento, restringiu a prorrogação às seções ainda abertas. Quem suspendeu o recebimento dos boletins e a totalização (e, com ela, a divulgação) foi o TSE, presidido por Nunes Marques (indicado ao STF por Bolsonaro): às 17h06 segundo a Agência Brasil (os ao vivo registram a pausa às 17h23 a 17h27), com 1.225 de 499.248 seções apuradas, e retomou às 19h. A campanha de Flávio também tinha pedido prorrogação em 17 a 19 cidades de SP, PR e SC (conforme o veículo) e depois em MG e no RS |
| Votos depois das 17h | Cerca de 34 a 35,5 mil no país (0,027%; Setup News/CNN e g1, pelos logs). Nos logs das 3.897 urnas da amostra, em hora local da urna: 0,026% dos votos a partir das 17h e 0,0047% a partir das 17h03, o que projeta cerca de 33 mil e 6 mil votos no país; em hora de Brasília, 236 seções da amostra tiveram voto depois das 17h e 16 depois das 17h05 (`PARA-O-REVISOR.md`, seção 5). No 1º turno, sem prorrogação, 3,72 milhões votaram depois das 17h (filas) |
| Trump acusa a eleição de fraude | Sim, com palavras próprias, a repórteres em 26/10: "It looked like another rigged election, frankly"; "it looked so corrupt, so terrible"; "The extension given was very strange". Sem prova; o único fato concreto citado foi a prorrogação. Na mesma fala: "I like Lula", "I'm not running Brazil". Segundo a Folha, a Casa Branca segurou a nota de felicitação do Departamento de Estado. Nenhuma sanção ou não reconhecimento formal encontrado |
| Musk acusa a eleição de fraude | Não com palavras próprias. Em 7 posts de 26/10 (cerca de 14 milhões de visualizações somadas), endossou posts de terceiros: "Wow" a Martin De Luca, que fala em "blatant rigging"; "Yeah, that was shady" a Robby Starbuck, que fala em "steal this election"; "Math doesn't add up" à conta dos totais do perfil End Wokeness; "True" a Rothmus, sobre Zanin; "Interesting question" a Geiger Capital, sobre urnas que travariam às 17h; um repost de Jack Posobiec; e um emoji de olhos revirados à felicitação de Ursula von der Leyen a Lula. As alegações desses posts estão testadas na seção 5.2 |
| Flávio pediu a anulação | Anunciou em 25/10, citando a prorrogação e fiscais "retirados da sala-cofre", sem estado, seção ou número. O jurídico descartou a anulação em 26/10. O TSE diz que dois fiscais do PL acompanharam o teste de integridade e a totalização |
| Teste de integridade | No DF houve 1 divergência no 2º turno (e 2 no 1º), atribuída a "erro humano de digitação"; a do 2º turno vem de reprodução do texto da Agência CLDF. Urna, cargo e direção do voto não divulgados. SP (33 urnas) e TSE (2 urnas, 389 votos) sem divergência, segundo trechos de busca das páginas oficiais, que deram 403 ao verificador. Composição das cédulas não divulgada. Relatório do TCU até 24/11 (`resultados/teste_integridade_df_2026.txt`) |
| O reel: "0 em 7" | Verdadeiro: nunca houve virada entre turnos desde 1989. Mas a margem do 1º turno de 2026 (1,9 ponto dos válidos) foi a menor das 8 eleições com 2º turno, menor que a de todas as 7 anteriores; a seguinte foi a de 2022 (5,2) (`resultados/analise_reel_lexrill.txt`) |
| O reel: "3 em 1000" | A conta sai de ler a margem de ±2 pontos como intervalo de 95% e contar só o erro amostral (3,1 em 1000). Lida como desvio-padrão, seria cerca de 8%. Com o erro real das pesquisas brasileiras (Datafolha, raiz do erro quadrático médio de 4,8 pontos), fica perto de 28%. Pelo mesmo método só amostral, o 1º turno de 2026 (Datafolha com Flávio em 42% dos válidos, ele teve 47,03%) daria cerca de 4 em 10 milhões (`resultados/analise_reel_lexrill.txt`, item 7) |
| O reel: "faltam 5,6 milhões", "6 em cada 10" dos eliminados | A conta bate com os números oficiais. O mesmo método aplicado a Bolsonaro em 2022 dá que 66% dos eleitores de Tebet, Ciro e demais (que apoiaram Lula) teriam ido para Bolsonaro |

## 5. O que os dados mostram

### 5.1 As faltas de lógica que se sustentam dentro de 2026

1. **Lula ganhou mais votos e mais pontos que Flávio entre os turnos em todas as 27 UFs** (`resultados/T38_pontos_por_uf.txt`). Flávio perdeu votos absolutos em 6 UFs (AC, AP, RR, MA, AM, TO). Em Goiás, terra de Caiado: Lula +9,3 pontos, Flávio +6,1. No Rio, estado de Flávio: Lula +872 mil, Flávio +202 mil.
2. **Por município** (`resultados/T38_municipios.txt`; os totais por município publicados pelo TSE somam o total nacional menos o exterior): Lula ganhou mais votos que Flávio em 5.228 das 5.571 cidades (93,8%), Flávio em 339 (6,1%), e houve 4 empates. Flávio ganhou mais pontos em 182. Cerca de três quartos dessas cidades estão no RS, em SC e em GO (e 27 das 339 no PR), quase todas pequenas, com saldo de só +25.300 votos para Flávio somando as 339 (média de cerca de 75 votos de saldo por cidade). 211 cidades viraram de Flávio para Lula e 1 (Uirapuru, GO) de Lula para Flávio.
3. **As pesquisas acertaram Lula no 1º turno e erraram para baixo no 2º, os 12 institutos na mesma direção** (`resultados/ADENDO16_resultados.txt`). Erro mediano em Lula: +0,2 ponto no 1º turno (de -2,6 a +2,6), +2,7 no 2º (de +1,2 a +3,8). No 1º turno, o erro em Flávio foi para baixo porque as pesquisas davam 8% a 17% aos demais, que tiveram 7,8% (voto útil de última hora). A última semana não mostrava Lula subindo (Datafolha 50 x 50 em 20 a 22/10 e 51 x 49 Flávio em 23 e 24/10). Levar Flávio de 51% para 48,21% dos válidos são 3,46 milhões de votos; para virar o resultado bastariam 2,22 milhões.
4. **A troca dentro das bases dos finalistas inverteu** (`resultados/T35_e_inversao_do_vazamento_amostra.txt`). Pela regressão por seção da amostra, 5,0% dos eleitores de Flávio no 1º turno passaram para Lula e 1,1% dos de Lula passaram para Flávio: um saldo de cerca de 2,2 milhões para Lula. Nas mesmas seções, em 2018 e 2022, quem vazava era o eleitor do PT (Haddad 3,6%, Lula 4,8%) e o da direita era fiel (Bolsonaro 1,0% e 2,1%). As pesquisas de 2026 declaravam vazamento parecido dos dois lados (PoderData 23-24/10: 5% e 5%; Ipespe: 2% e 1%; Nexus: 98% de fidelidade dos dois), com saldo de 0 a 0,6 milhão (`resultados/contexto_2t_2026_e_onde_estaria_a_fraude.txt`).
5. **Eleitores dos eliminados.** Entre os que escolheram um finalista, a urna dá a Lula 52,2% (EP 1,7); os institutos declaravam de 32% a 44%. É comparação post hoc: o T37 como registrado ficou inconclusivo por erro de desenho (`resultados/ADENDO16_resultados.txt`, `resultados/T37_eliminados_urna_amostra.json`).
6. **Onde urna e pesquisa concordam:** no branco e nulo do 1º turno (urna 67% para Lula, PoderData 66%) e em quem não votou no 1º turno (60% contra 59%) (`resultados/contexto_2t_2026_e_onde_estaria_a_fraude.txt`). A diferença entre o resultado e as pesquisas, cerca de 3 milhões, está toda no eleitorado de direita do 1º turno.
7. **Sobre os 94% das cidades.** Os 94% são as cidades em que Lula ganhou mais votos (não as em que venceu: Lula venceu em 2.875 das 5.571 no 2º turno, contra 2.663 no 1º, que teve 2 empates; chave 'vitorias' do `resultados/T38_municipios.json`). É a virada nacional vista cidade por cidade. Em pontos: a margem de Flávio caiu em média 4,4 pontos por cidade, com variação típica de 2,2 pontos entre cidades; com essa média e essa variação, a conta prevê 2,6% das cidades andando para Flávio, e foram 3,3%. O mesmo vale estado por estado (RS previsto 14,5%, observado 15,9%; SC 10,7% e 9,8%; GO 12,1% e 10,2%; chave 'uniformidade' do `resultados/T38_municipios.json`). Uma virada desse tamanho, real ou fabricada, sai quase unânime de qualquer jeito. A pergunta que fica é de onde veio o movimento nacional.

### 5.2 Onde a fraude deixaria marca e o que apareceu

| Onde estaria a fraude | Marca que deixaria | O que apareceu | Arquivo em `resultados/` |
|---|---|---|---|
| Na totalização, durante a pausa | Boletim assinado diferente do total; arquivo trocado | T1: 13 municípios inteiros, soma dos boletins igual ao oficial, diferença zero. T18: 3.897 seções, assinatura de hardware válida em todos os 42.867 arquivos e nos 3.897 blocos; cadeia até a raiz do TSE e assinatura de software não verificadas. Sem sinal | `T1_soma_municipios.json`, `T1_extensao_municipios.json`, `T18_assinaturas_amostra_inteira.json` |
| Na prorrogação | Muitos votos fora de hora; urna reaberta | Cerca de 6 mil votos depois da liminar. Nenhuma seção com voto depois do encerramento. 5,8% das seções da amostra tiveram voto a partir das 17h (hora local; 236 seções em hora de Brasília); às 17h03 locais, só 31% tinham iniciado o encerramento (o "80% fechadas" é número de SP). Descritivo: não havia critério registrado | `contexto_2t_2026_e_onde_estaria_a_fraude.txt`, item 4 |
| Votos em nome de quem faltou | Voto sem habilitação, rajada, biometria fora da base | T3: zero anomalias em 3.897 logs. T9: dentro do local, a fração sem biometria entre os eleitores a mais fica na base (0,139 contra 12,2%), sem sinal; no bruto, 22% das habilitações a mais foram sem biometria, o que fica para o T21 com o bweb | `T2_T3_amostra_inteira.txt`, `T9_biometria_amostra_inteira.json`, `T21c_biometria_tarde_amostra_inteira.json` |
| Programa trocado entre os turnos | Versão ou componente novo; carga fora do oficial | T10: mesma versão 10.23.0.0 nas 3.897 urnas; 1 urna com bandeira vermelha pelo critério registrado (erro de verificação de assinatura em 22/09, na preparação), com a causa no log, mas aceitar essa explicação é leitura posterior. T20: pendências de carga em aberto pelo critério literal até as atas de carga | `T10_software_amostra_inteira.txt`, `T20_pendencias_amostra_inteira.json` |
| Troca num modelo de urna | Diferença entre modelos no mesmo prédio | T17: sem sinal para antigas contra novas nos 119 locais (113 em SP; não vale para outras UFs); sem poder para um modelo só, para contingência e para urna trocada. Lote: não testado | `ADENDO9_resultados_amostra.txt`, `T17_maquina.json` |
| Gatilho por horário ou por contagem | Mudança depois de certa hora ou de N votos | T30, horário: sem poder pelo critério (erro-padrão acima de 0,6); às 14h e às 16h a inclinação passa valor e z do sinal, mas o placebo falha; com local e fatia do 1º turno, a associação cai, e às 16h o z fica em 1,95 contra o limite de 1,96. Contagem: sem sinal de N = 100 a 200; N = 50 inconclusivo, com coeficiente negativo | `T30_gatilhos_amostra_inteira.json`, `ADENDO9_resultados_amostra.txt` |
| Branco e nulo convertido em 13 (forma A) | Branco e nulo de presidente encolhe frente ao de governador na mesma urna; urna abaixo do declarado | Nas 6 UFs com governador no 2º turno: T5 do 2º turno inconclusivo pela letra (0,328 entre 0,241 e 0,341). Comparação descritiva com o 1º turno das mesmas seções: 0,305 no 1º, 0,328 no 2º; com a conversão de 52% necessária para virar, cairia para cerca de 0,15. A razão branco e nulo de presidente / de governador subiu nas 6 UFs (T39). Datafolha declarava 3% de branco e nulo; foram 3,24%. T19: nenhum nulo digitado 13 ou 22. T36: sem poder no 2º turno | `ADENDO14_e_T39_resultados.txt`, `T19_nulos_rdv_amostra.json`, `T36_nulo_suspensao_amostra.json` |
| Troca de votos de Flávio para Lula (forma B) | Só no voto de presidente; maior onde Flávio é forte | T22b, sem sinal pela letra: na mesma urna de AM, DF e ES, o candidato a governador do campo de Flávio perdeu tantos eleitores do 1º turno quanto ele (5,9% contra 4,8%; D = +0,011, intervalo de -0,032 a +0,054, que não exclui por completo os -0,03 de uma troca). Entre UFs e entre cidades, a virada foi menor onde Flávio é mais forte (nas cidades com Flávio acima de 65%, a margem andou -2,5 pontos; abaixo de 30%, -4,7) | `ADENDO14_e_T39_resultados.txt`, `T38_municipios.txt`, `ADENDO16_resultados.txt` |
| Troca pequena e espalhada, do tamanho do erro das pesquisas | Perda dos próprios eleitores acima de qualquer referência; ganho além do bolo da seção | É o ponto aberto mais importante. T14: coeficiente 0,0507 (EP 0,0070; intervalo de 0,037 a 0,064) contra limite de "sem sinal" de 0,051, sem sinal no limite; a leitura depende da base (nas mesmas seções, robustez escolhida depois: 2022 dá 0,048, 2018 dá 0,010). T7 inconclusivo: 10,6% das seções com ganho além do bolo, contra 5,3% em 2022 no país e 7,1% nas mesmas seções. T35 preliminar, inconclusivo: a vantagem de fidelidade da direita sobre a esquerda na mesma força local do adversário (+1,2 ponto em 2018, dentro do erro; +3,4 em 2022) virou desvantagem de 2,5 pontos em 2026; a diferença para 2018 fica a 0,05 erro-padrão do limiar | `T7_T8_T14_amostra.txt`, `T7_T14_referencias_mesmas_secoes.txt`, `T35_e_inversao_do_vazamento_amostra.txt`, `PARA-O-REVISOR.md` (seção 7) |

As alegações dos posts endossados por Musk, testadas: "a conta não fecha" (a soma fecha; ver seção 2). "Zanin prorrogou 3 minutos antes do fechamento": a liminar saiu às 17h03. "Só nos condados amigos": a liminar valia para o país todo. "Um código trava as urnas às 17h": 236 seções da amostra receberam voto depois das 17h de Brasília (225 a partir das 17h locais). "213 cidades viraram" (número da CNN Brasil; o Jornal Razão diz que Musk repostou Tommy Robinson com ele, mas o post primário não foi localizado): são 211.

### 5.3 Leitura atual

- A anomalia real: um movimento de cerca de 2,7 pontos na fatia de Lula além do que as pesquisas mediam (cerca de 5,5 pontos na margem), contra o contexto inteiro; a margem de Flávio nos válidos foi de +1,87 no 1º turno a -3,58 no 2º. Só o Vox Brasil e trackings do PT tinham Lula à frente, e por pouco. O movimento está concentrado no eleitorado de direita do 1º turno (base de Flávio e eleitores dos eliminados).
- Nenhum teste deu sinal. Sem sinal: totalização (T1, T18), inserção de votos (T3, T9), troca só no presidente (T22b, com intervalo largo), troca proporcional pelo T14 (no limite, na amostra), urnas antigas contra novas (T17, vale para SP). T19: o sinal forte (nulo digitado 13 ou 22) está ausente, e o item (b) ficou sem referência. T10: bandeira vermelha pela letra em 1 urna, com a causa no log aceita só como leitura posterior. Sem poder, inconclusivo ou em aberto pela letra: T20 (em aberto), um modelo de urna só (T17), gatilho por horário (T30), T5 do 2º turno, T7 e T35. A prorrogação foi analisada de forma descritiva (cerca de 6 mil votos depois da liminar, nenhuma urna reaberta).
- O que sobra para a tese: uma lógica no programa oficial que poupe os 6 estados com governador no 2º turno (onde a mesma urna dá referência), ou que mexa também no voto de governador; ou algo que aja por igual em todas as urnas e se confunda com eleitor real. O T16, o T34 e a soma completa dos boletins olham parte disso.
- A explicação sem fraude que precisa ser descartada: troca de eleitores entre os turnos. Cerca de 11% dos votantes do 2º turno não tinham votado no 1º (PoderData), o que dá cerca de 14 milhões entrando e 11 milhões saindo. Se quem saiu era mais de direita e quem entrou mais de Lula (PoderData: 50 a 35 entre quem não votou no 1º turno), a urna mostra isso como "eleitor de Flávio que virou Lula", e a pergunta de fidelidade das pesquisas não vê. A ponderação pelo resultado do 1º turno, que o PoderData passou a usar em 13/10, puxaria as pesquisas para Flávio nesse caso. Isso também explicaria o T22b (quem falta não vota para governador). Indício na amostra, exploratório: dentro do mesmo local de votação, o comparecimento subiu menos onde Flávio era mais forte.

### 5.4 Adendo 18: incoerências de lógica dentro de 2026, sem outras eleições como régua

Critérios escritos antes de rodar (commit bc7decb); cada teste conferido por outro agente com código próprio (`resultados/ADENDO18_resultados.txt`, `resultados/testes_adendo18_com_conferencia.json`).

| Teste | Pela letra | Leitura |
|---|---|---|
| L1, horários impossíveis | INCOERÊNCIA seção a seção (1 seção de 18 votos), INCONCLUSIVO em grupo | 18 seções sem explicação, contra o limite de 100; virada média -0,43. Os arquivos das 18 (boletim, log, assinatura) fecham com o bweb; as aberturas tardias têm causa no log |
| L2, urna trocada ou carga fora do padrão | COERENTE | -0,02 e -0,01 ponto |
| L3, núcleo do PL | COERENTE | Flávio perdeu 8,1% onde o PL é fraco e 2,9% no núcleo; não descarta desvio somado ao comportamento |
| L4, aliados em casa | INCONCLUSIVO | Caiado e Zema mandaram a maioria para Flávio; a urna fica 11 a 22 pontos acima das pesquisas, como no neutro Renan |
| L5(a), erro das pesquisas entre turnos | INCOERÊNCIA | 11 de 11 institutos; virada -6,10. É a incoerência que se sustenta, e não se separa entre transferência, comparecimento e contagem |
| L5(b), saldo | DESCRITIVO | Mesmo erro de L5(a), visto como fluxo |
| L6, governadores | INCOERÊNCIA | +1,48 ponto, mas invertido do lado de Lula e explicado em boa parte por nível e composição |
| L7, teste de integridade | DESCRITIVO | Fraude pega por azar não cola; o furo de desenho é um programa que reconheça o teste (modalidade principal sem digital), que só a leitura e a compilação do código excluem |
| L8, "dossiê" dos EUA | DESCRITIVO | Não há documento; a prorrogação não muda o resultado; o 1º turno também teve paradas no recebimento |

### 5.5 Adendos 20 a 22: testes forenses nos boletins e o que não depende de ninguém

Critérios antes de rodar (commits d976d4d, 913af7a e f12121e); cada teste conferido por outro agente com código próprio (`resultados/ADENDO20_resultados.txt`, `ADENDO21_resultados.txt`, `ADENDO22_resultados.txt` e os `testes_adendo2x_com_conferencia.json`).

- Sem sinal: dígitos, porcentagens redondas e boletins repetidos (F2); caudas e as 40 seções extremas (F5); eleitor a mais sem biometria (F6); mídia do 2º turno por computador (F9, com pouco poder); teste de integridade (F11); assinaturas e certificados (F12, F18); 64 casos pendentes arquivo por arquivo (F14).
- Urnas antigas (F4, F10, F16): a vantagem de Lula nelas vem de locais em que as seções novas votaram em outro prédio; com o local de fato usado, some.
- Pesquisas (F13, F17): a diferença urna contra pesquisa nos eleitores dos eliminados depende do método; os painéis online calibrados mediram perto da urna.
- Falhas de gestão e de procedimento: certificado da AC URNA vencido em 18/07/2026 (cadeia vencida pela regra estrita nas urnas antigas; ao menos um certificado emitido depois); Volta Redonda (urnas de duas escolas suspensas às 17h e encerradas às 19h por um título que não é de mesário); mesma mídia do 2º turno em duas urnas do RJ; divergências do teste de integridade sempre na CLDF. Nenhuma muda votos.
- Fica sem resposta com dado público: um programa da urna que reconheça o teste de integridade (só a compilação independente do código exclui). Pendente: perfil do comparecimento do 2º turno (não publicado), relatórios do TCU e da UE.

## 6. Pendências

- **Boletins completos do 2º turno (bweb):** publicados em 28/10 (`reproducao/consultas_bweb_2t.txt`); os testes da seção 7 e os testes estendidos rodaram (`resultados/testes_bweb_2t_com_conferencia.json`). Registro anterior: o TSE ainda não publicou (consulta registrada em `reproducao/consultas_bweb_2t.txt`: em 27/10 às 02h01 UTC, o pacote só tinha os 56 arquivos do 1º turno, de 06/10). O do 1º turno saiu dois dias depois da votação. Quando o do 2º sair, `rodar_2026.sh` (que exige DADOS com as bases de 2018, 2022 e do 1º turno de 2026, fora do repositório) baixa o bweb, compara a soma de cada UF e do Brasil com o total oficial e roda T4 (seções com branco e nulo zerado), T5 do 2º turno, os testes da seção 7 do documento original (modelo, branco e nulo por seção, governador), T8, T35 com todas as seções e, se LOCAIS apontar para os CSV de locais de votação de 2026, o T34 (salto na divisa Sul/não Sul; referência de 2022 pronta: +0,005). Falta script para o T15 completo, T16 (piso por UF), T21 a T23 com o bweb, T27 a T29, T31, T32 e as calibrações do T7 e do T14; para o T7 (`analisar_fluxos.py`) e para o T14 com os grupos dos eliminados (com `candidatos2026_1t.json.gz`), falta só a chamada no `rodar_2026.sh`.
- **Teste de integridade:** a urna, o cargo e a direção da divergência do DF no 2º turno; a composição das cédulas (quantos brancos e nulos para presidente). Atas do TRE-DF e relatório do TCU até 24/11. Um pedido de acesso à informação, ou o PL (que, segundo o TSE, teve dois fiscais no teste de integridade do TSE), pode pedir ao TRE-DF a urna, o cargo, a direção e o trecho do vídeo.
- **Troca de eleitores:** o perfil do comparecimento por idade e zona nos dois turnos (dado do TSE) mostra quem deixou de votar.
- **Atas de carga das urnas:** fecham as pendências do T20.
- **Revisão cética:** mover a pasta para o repo `eleicoes-2026` e passar ao Codex; atualizar `PARA-O-REVISOR.md` com os adendos 14 a 17.

## 7. Mapa dos arquivos

| Pasta ou arquivo | O que tem |
|---|---|
| `PRE-REGISTRO-2026-10-26.md` | critérios de T1 a T6 no registro inicial e de T7 a T39 em adendos; vale o horário do commit |
| `PARA-O-REVISOR.md` | passagem para o revisor, erros corrigidos, onde posso estar errado, como reproduzir (anterior aos adendos 14 a 17) |
| `CONTEXTO-ELEICAO-2026-original.md` | documento que abriu a sessão |
| `resultados/ADENDO9_resultados_amostra.txt` | T17, T18, T19, T20, T30 e T33 na amostra, e T3, T9, T10, T18, T20, T30 e T21(c) com os logs das 3.897 seções |
| `resultados/ADENDO14_e_T39_resultados.txt` | governador na mesma urna (T22b, T5 do 2º turno, T22, T39) |
| `resultados/ADENDO16_resultados.txt` | T36, T37, T38 por UF, erro das pesquisas por turno, desenho entre UFs |
| `resultados/T38_municipios.txt` e `.json` | contagens e somas das 5.571 cidades, tabela por UF e lista das 182 em que Flávio ganhou mais pontos (os dados por cidade ficam fora do repositório) |
| `resultados/T35_e_inversao_do_vazamento_amostra.txt` | a inversão do vazamento e a curva por força do adversário |
| `resultados/contexto_2t_2026_e_onde_estaria_a_fraude.txt` | contexto conferido, anomalias, mapa da fraude, Trump e Musk |
| `resultados/teste_integridade_df_2026.txt` | as divergências do DF |
| `resultados/candidatos_1t_2026_totais.txt` | votos por candidato no 1º turno |
| `resultados/analise_reel_lexrill.txt` | conferência do reel |
| `resultados/historico_comparecimento_bn.txt` | comparecimento e branco e nulo entre turnos, 2002 a 2026 |
| `resultados/*_pesquisas_verificadas.txt` | pesquisas levantadas e conferidas |
| `scripts/` | o código versionado (mapa em `PARA-O-REVISOR.md`, seção 3; o que não tem script está listado na seção 8 de lá). Novos nesta etapa: `analisar_pres_gov.py`, `analisar_curva_forca.py`, `analisar_divisa.py`, `analisar_nulo_suspensao.py`, `analisar_eliminados.py`, `baixar_municipios.py`, `analisar_municipios.py` |
| `rodar_2026.sh` | rotina para quando o bweb do 2º turno sair |
| `reproducao/` | listas da amostra, logs de download, ambiente, revisões, consultas ao bweb |

**Dados que não estão no repositório** (ficaram no scratchpad da sessão, que é apagado quando o container é reciclado):
- Bases por seção de 2018 e 2022 (`secoes2018.json.gz`, `secoes2022.json.gz`): vieram nos zips enviados pelo Léo (`eleicao-2026-parte2-secoes2022.zip`, `eleicao-2026-parte3-secoes2018.zip`).
- Base do 1º turno de 2026 (`secoes2026_1t.json.gz`, `candidatos2026_1t.json.gz` e `candidatos_gov_2026_1t_6ufs.json.gz`, este com os candidatos a governador das 6 UFs, por `extrair_candidatos.py --cargo 3`): refazer a partir do bweb do 1º turno no portal do TSE com `extrair_bweb.py` e `extrair_candidatos.py`.
- Arquivos de urna da amostra (3.897 seções, mais o estrato G de 2.400 seções): refazer com `sortear_amostra.py` (semente 20261026) e `baixar_arquivos_urna.py`, usando as listas em `reproducao/`.
- Totais do 2º turno por município: refazer com `baixar_municipios.py`.
- Locais de votação com coordenadas: "Eleitorado por local de votação - 2026" no portal do TSE.

## 8. Regras de trabalho

- Critério antes do dado, em commit. Quando o registro estava errado ou o dado já tinha sido visto, isso está declarado no próprio adendo, num adendo seguinte ou no arquivo de resultados do teste.
- Fato, indício, evidência e prova são coisas diferentes. "Sinal" é indício e pede cruzamento com outro teste independente.
- Resultado da amostra é provisório; com o bweb completo, refaz-se com o mesmo critério.
- Todo dado baixado é tratado como não confiável: pasta própria, Python com `-I`. Só são pedidos ao TSE arquivos listados pelo próprio TSE, ou caminhos já usados no T1; nenhum caminho é adivinhado.
- Ceticismo nos dois sentidos: nem confirmar por simpatia, nem descartar por princípio. Partir do pressuposto de fraude para procurar onde estaria a marca, e relatar o que aparecer.
- Textos sem travessões.
