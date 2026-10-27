# Eleição presidencial de 2026, 2º turno: investigação de fraude

Ponto de entrada da pesquisa. Reúne a situação, a tese e os argumentos do Léo (dono da pesquisa), os fatos levantados e conferidos, cada teste feito com o resultado, e o que falta. Atualizado em 27/10/2026, madrugada (UTC).

Leitura sugerida:
1. Este arquivo, inteiro.
2. `PRE-REGISTRO-2026-10-26.md`: os critérios de cada teste, registrados em commits com horário antes de ver os dados (adendos 1 a 16).
3. `PARA-O-REVISOR.md`: passagem para o revisor cético (Codex), com a lista de "onde eu posso estar errado" e como reproduzir.
4. `CONTEXTO-ELEICAO-2026-original.md`: o documento que abriu a sessão (robô de apuração, primeiras análises, critérios da seção 7).
5. `resultados/`: um arquivo por teste ou levantamento. Os citados aqui estão entre crases.

---

## 1. A situação e a pergunta

O 2º turno foi em 25/10/2026, entre Lula (PT, 13) e Flávio Bolsonaro (PL, 22). Flávio venceu o 1º turno por 2,22 milhões de votos e chegou ao 2º com o apoio da maior parte da direita e do centro. Lula venceu o 2º turno por 4,43 milhões.

O Léo acredita que a eleição foi fraudada e pediu uma investigação que parta desse pressuposto: pensar como quem fraudaria, procurar onde a fraude deixaria marca e testar cada ponto com dado público e critério definido antes. Ele pediu também que a análise olhe o contexto de 2026, e não outras eleições, e que não fique refutando os argumentos dele, e sim tentando entender o que aconteceu. O combinado desde o início: ceticismo nos dois sentidos, resultados relatados sem suavizar para nenhum lado.

Repositório futuro: o Léo criou o repo `eleicoes-2026` para receber todo o contexto desta pesquisa e trabalhar com o Codex como revisor cético. Esta pasta será movida para lá quando ele pedir.

## 2. Números oficiais

| | 1º turno (04/10) | 2º turno (25/10) | Variação |
|---|---|---|---|
| Flávio Bolsonaro (22) | 56.104.503 (47,03% dos válidos) | 59.826.041 (48,21%) | +3.721.538 |
| Lula (13) | 53.879.538 (45,16%) | 64.256.232 (51,79%) | +10.376.694 |
| Augusto Cury (70) | 3.448.569 | | |
| Renan Santos (14) | 2.675.887 | | |
| Ronaldo Caiado (55) | 2.605.148 | | |
| Romeu Zema (30) | 326.488 | | |
| Demais candidatos | cerca de 0,26 milhão | | |
| Brancos + nulos | 4,77% do comparecimento (cerca de 5,98 milhões) | 3,24% (4.153.801: brancos 1.430.496, nulos 2.723.305) | cerca de -1,82 milhão |
| Abstenção | 21,08% | 19,21% | comparecimento +2,96 milhões (128.236.074 no 2º turno) |

A conta que fecha por identidade: o que os dois finalistas ganharam juntos (+14,10 milhões) é igual aos votos dos eliminados (9,32 milhões) mais o aumento do comparecimento (+2,96 milhões) mais a queda do branco e nulo (+1,82 milhão). O que está em discussão não é se a soma fecha, e sim como esse total se dividiu.

Para referência (base de 2022 por seção): Bolsonaro teve 51.072.345 votos no 1º turno de 2022 e 58.206.354 no 2º. Flávio teve mais que ele no 1º turno (56,10 contra 51,07 milhões) e no 2º (59,83 contra 58,21 milhões).

## 3. A tese e os argumentos do Léo, nas palavras dele

As frases abaixo são trechos das mensagens do Léo na sessão, com ajustes mínimos de digitação.

**A tese.**
- Variante inicial (documento original): "de alguma forma eles alteram os votos brancos e nulos, por isso o roubo deles é limitado". O branco e nulo verdadeiro seria um valor desconhecido, porque o único registro é o da própria urna.
- Variante desta sessão: "Minha suspeita é que o sistema da urna é corrompido. Minha tese é que eles programaram o desvio previamente e erraram a mão, pq o resultado do Lula não é explicável estatisticamente."
- "Não acredito que haja fraude no número de eleitores. Isso é mais fácil de pegar."
- "Vc não pode afirmar que o programa da urna é seguro! Olhe as falhas que foram descobertas no php nessa semana! Enfim nenhum sistema é seguro hoje! Imagina um que nem teve escrutínio público amplo pra avaliação."
- "A gente não vai conseguir identificar se existe um malware no sistema ou não. Porque isso só se a gente auditasse o código, e isso é impossível." O que dá para fazer é medir a discrepância entre os dados da urna (que, pela tese, já podem estar corrompidos) e a lógica do mundo real: pesquisas, transferência de votos, esquerda e direita, rejeição de Lula, histórico de abstenção, branco e nulo.
- "Lembrando que não houve carga nova de sistema nas urnas. Pode ter havido, sim, um malware quando colocaram os candidatos novos." "A gente parte do pressuposto de que a urna não é confiável, porque não é."
- "E os brancos e nulos, no caso de fraude, não são convertidos porque eles são intocados. Esse é o dado que você está vendo, né? Mas e se esse dado já foi fraudado? E não tem como saber quem votou branco e nulo, como o voto é secreto. Imagina se o malware converte esses dados automaticamente de branco e nulo."

**A conta.**
- "Tinha aprox 9 milhões de votos de outros candidatos pra migrar (quase todos apoiaram Flávio e nenhum Lula). Tiveram 3 milhões a mais de votantes (que já não é normal). E tinham mais 5 milhões de brancos e nulos tomando lado. Flávio fez 3,6 mi de votos a mais, que é menos de 50% dos votos de outros candidatos, Lula teria que ter feito 100% do resto, o que é praticamente impossível."
- "Flávio teria que converter apenas 40% (no máximo) dos votos de outros candidatos, Lula 100% do restante de 60%, 100% dos votos brancos e nulos convertidos e 100% da abstenção negativa."
- "Dos 9,2 milhões de votos dos outros candidatos é natural que houvesse boa parte de abstenção, de eleitores deles que não iriam votar ou votar branco e nulo; então se a abstenção caiu e branco e nulo também, quer dizer que ainda mais eleitores novos apareceram pra compensar. E esses seriam massivamente do Lula, quase 100%. O que não faz sentido."
- "Vc está dizendo que entre todo mundo que saiu e entrou o saldo é 100% pro Lula; se for por esse lado a conta fica ainda pior, pq do lado do Lula não saiu ninguém."
- "Lula ganhar estaria dentro da margem de erro de algumas pesquisas, mas ganhar 11 milhões de votos dentro desse universo foi escrachado."

**A lógica política.**
- "Não existiam candidatos de esquerda pra uma transferência expressiva de votos. Flávio fez 47% no primeiro turno tendo vários candidatos com o mesmo apelo anti PT como concorrentes; o natural seria a transferência de votos ser dele, e não de Lula."
- "Não existe transferência de votos de PL pra PT, existe de qualquer outro pra contra PT."
- "Flávio não cresceu em nenhum estado entre primeiro e segundo turno [em %], levando em consideração o apoio dos outros candidatos, não faz sentido."
- "94% dos municípios do Brasil tiveram uníssonos Lula à frente, levando em consideração todo o contexto. É praticamente impossível."

**O contexto que ele apontou** (conferido na seção 4): maior bancada da história do PL na Câmara (mais de 120 deputados), direita com mais de 50% do Senado, maioria dos governadores eleitos com Flávio, Temer e outros nomes do centro com Flávio, os derrotados do 1º turno com Flávio, pesquisas com Flávio na frente, trackings internos do PT e do PL com Flávio 4 a 6 pontos à frente, Flávio melhor nos debates, votação recorde de Flávio no 1º turno, e "o ex-advogado dele [de Lula] paralisar a apuração da eleição depois das 17 horas". Depois acrescentou: Trump e Musk acusam a eleição de fraude.

**Sobre pesquisas.** Priorizar as que mais acertaram o 1º turno (Veritá e Gerp). Desconfiar das que têm viés de esquerda e se envolveram em escândalos recentes (patrocínios e palestras pagas pelo Banco Master).

**Como investigar.** "Pensarmos pela cabeça de quem tentaria fraudar a eleição. Ele saberia que isso seria averiguado pelo mundo todo. Como essa pessoa agiria? Aonde esses números seriam refletidos na apuração? Aonde pode haver pistas da fraude e onde a lógica não faz sentido?" "Estamos atrás de uma conspiração e vc tem que tentar enxergar o que ninguém vê. Como roubar uma eleição com urnas opacas sem deixar evidências estatísticas... acho que eles falharam pq a lógica não vai fechar essa conta."

Ele trouxe também a análise de um reel do Instagram (Alex Ribeiro, @lex.rill, 26/10): "0 em 7" viradas desde 1989 e "3 em 1000" pela margem de erro das pesquisas da véspera. A conta do vídeo bate com os números oficiais. O "3 em 1000" depende de tratar a margem de erro como desvio-padrão e supor que ninguém mudou o voto depois da pesquisa.

## 4. O contexto, conferido

Pesquisa em várias frentes, cada uma com verificador independente que reabriu as fontes. Detalhes e links em `resultados/contexto_2t_2026_e_onde_estaria_a_fraude.txt`, `resultados/contexto_2t_2026_pesquisa_verificada.json` e `resultados/trump_musk_2t_2026_verificado.json`.

| O que foi dito | O que as fontes mostram |
|---|---|
| PL com mais de 120 deputados, maior bancada da história | 121 deputados. É a maior de um partido desde 1988; na história, o PMDB fez 260 em 1986 |
| Direita com mais de 50% do Senado | Sim. PL 29 de 81 (maior bancada em início de legislatura desde 1988); PL, PP, União, Republicanos, Novo e Podemos somam 50 de 81 |
| A maioria dos governadores apoiou Flávio | 12 dos 21 eleitos no 1º turno (GO, MT, MS, MG, PA, PR, RJ, RS, RO, RR, SC, SP). 5 apoiaram Lula (BA, CE, PB, PI, SE) e 4 ficaram neutros (AL, AP, MA, PE) |
| Os derrotados apoiaram Flávio | Zema, Caiado, Clariana, Cury (com 8 compromissos) e Grassi, sim. Renan Santos liberou os eleitores. Samara, Hertz e Edmilson foram de Lula; o PCO pediu voto nulo |
| Temer e o centro com Flávio | Temer apoiou em 05/10. União, PP, Novo, Republicanos e Podemos também. O MDB se dividiu (17 de 27 diretórios com Flávio) |
| Pesquisas com Flávio na frente | 11 de 12 institutos na véspera, com 50,1% a 52% dos válidos. Só o Vox Brasil tinha Lula à frente |
| Trackings do PT e do PL com Flávio 4 a 6 pontos à frente | Os "4 a 6 pontos" vêm de um interlocutor anônimo (Metrópoles, 21/10). No dia seguinte, o tracking principal do PL foi descrito com Flávio +3. Os do PT davam 50 x 50 e Lula +1 |
| Flávio melhor nos debates | Houve 2 debates entre os dois, ambos no 2º turno (Band em 18/10 e Globo em 23/10). Nenhuma pesquisa representativa mediu quem foi melhor |
| Votação recorde de Flávio | Mais que Bolsonaro em 2022 no 1º turno (56,10 contra 51,07 milhões) e no 2º (59,83 contra 58,21) |
| O ex-advogado de Lula paralisou a apuração depois das 17h | Cristiano Zanin (STF, ex-advogado de Lula na Lava Jato) prorrogou a votação até as 19h nas seções ainda abertas, em liminar às 17h03, a pedido da coligação de Lula (falta de ônibus em Salvador, Feira e Lauro de Freitas). Quem suspendeu a divulgação foi o TSE (presidente Nunes Marques, indicado por Bolsonaro), das 17h06 às 19h, com 1.225 de 499.248 seções apuradas. A campanha de Flávio também tinha pedido prorrogação em 19 cidades de SP, PR e SC |
| Votos depois das 17h | Cerca de 34 a 35,5 mil no país (0,027%). Nos logs da amostra: cerca de 33 mil a partir das 17h e cerca de 6 mil depois da liminar das 17h03. No 1º turno, sem prorrogação, 3,72 milhões votaram depois das 17h (filas) |
| Trump acusa fraude | Sim, com palavras próprias, a repórteres em 26/10: "It looked like another rigged election, frankly"; "The extension given was very strange". Sem prova; o único fato citado foi a prorrogação. Na mesma fala: "I like Lula", "I'm not running Brazil". A Casa Branca segurou a nota de felicitação do Departamento de Estado (Folha) |
| Musk acusa fraude | Não com palavras próprias. Em 7 posts de 26/10 (cerca de 14 milhões de visualizações), endossou posts de terceiros que falam em "rigging": "Math doesn't add up", "Wow", "True", "Interesting question". As alegações desses posts estão testadas na seção 5 |
| Flávio pediu a anulação | Anunciou em 25/10, citando a prorrogação e fiscais "retirados da sala-cofre", sem estado, seção ou número. O jurídico descartou em 26/10. O TSE diz que dois fiscais do PL acompanharam o teste de integridade e a totalização |
| Teste de integridade | No DF houve 1 divergência no 2º turno (e 2 no 1º), atribuída a "erro humano de digitação". Urna, cargo e direção do voto não divulgados. SP (33 urnas) e TSE (2 urnas) sem divergência. Relatório do TCU até 24/11 (`resultados/teste_integridade_df_2026.txt`) |

## 5. O que os dados mostram

### 5.1 As faltas de lógica que se sustentam dentro de 2026

1. **Lula ganhou mais votos e mais pontos que Flávio entre os turnos em todas as 27 UFs** (`resultados/T38_pontos_por_uf.txt`). Flávio perdeu votos absolutos em 6 UFs (AC, AP, RR, MA, AM, TO). Em Goiás, terra de Caiado: Lula +9,3 pontos, Flávio +6,1. No Rio, estado de Flávio: Lula +872 mil, Flávio +202 mil.
2. **Por município** (`resultados/T38_municipios.txt`, 5.571 cidades, soma igual ao total oficial): Lula ganhou mais votos que Flávio em 5.228 (93,8%). Flávio ganhou mais votos em 339 e mais pontos em 182, quase todas cidades pequenas do RS, de SC e de GO, com saldo de só +25.300 votos para ele. 211 cidades viraram de Flávio para Lula e 1 (Uirapuru, GO) de Lula para Flávio.
3. **As pesquisas acertaram Lula no 1º turno e erraram para baixo no 2º**, os 12 institutos na mesma direção (`resultados/ADENDO16_resultados.txt`). Erro mediano em Lula: +0,2 ponto no 1º turno, +2,7 no 2º (de +1,2 a +3,8). A última semana não mostrava Lula subindo. Levar Flávio de 51% para 48,21% dos válidos são 3,46 milhões de votos; para virar o resultado bastariam 2,22 milhões.
4. **A troca dentro das bases dos finalistas inverteu.** Pela regressão por seção da amostra, 5,0% dos eleitores de Flávio no 1º turno passaram para Lula e só 1,1% dos de Lula passaram para Flávio: um saldo de cerca de 2,2 milhões para Lula. As pesquisas declaravam vazamento parecido dos dois lados (PoderData 23-24/10: 5% e 5%; Ipespe: 2% e 1%; Nexus: 98% de fidelidade dos dois), com saldo de 0 a 0,6 milhão.
5. **Eleitores dos eliminados.** Entre os que escolheram um finalista, a urna dá a Lula 52,2%; os institutos declaravam de 32% a 44%.
6. **Onde urna e pesquisa concordam:** no branco e nulo do 1º turno (urna 67% para Lula, PoderData 66%) e em quem não votou no 1º turno (60% contra 59%). A diferença entre o resultado e as pesquisas, cerca de 3 milhões, está toda no eleitorado de direita do 1º turno.
7. **Sobre os 94% das cidades.** É a virada nacional vista cidade por cidade: com a margem de Flávio caindo em média 4,4 pontos por cidade e variação típica de 2,2 pontos entre cidades, a conta prevê 2,6% das cidades andando para Flávio; foram 3,3%. Uma virada desse tamanho, real ou fabricada, sai quase unânime de qualquer jeito. A pergunta que fica é de onde veio o movimento nacional.

### 5.2 Onde a fraude deixaria marca e o que apareceu

| Onde estaria a fraude | Marca que deixaria | O que apareceu | Arquivo |
|---|---|---|---|
| Na totalização, durante a pausa | Boletim assinado diferente do total, ou assinatura inválida | 13 municípios inteiros: soma igual ao oficial, diferença zero (T1). 3.897 seções: todas as assinaturas válidas (T18). Por município, a soma das 5.571 cidades bate com o total oficial | `T1_extensao_municipios.json`, `T18_assinaturas_amostra_inteira.json`, `T38_municipios.txt` |
| Na prorrogação | Muitos votos fora de hora; urna reaberta | Cerca de 6 mil votos depois da liminar; nenhuma seção com voto depois do encerramento; 5,8% das seções tiveram voto depois das 17h; às 17h03 locais só 31% tinham iniciado o encerramento (o "80% fechadas" é número de SP) | `contexto_2t_2026_e_onde_estaria_a_fraude.txt`, item 4 |
| Votos em nome de quem faltou | Voto sem habilitação, rajada, biometria | Zero em 3.897 logs (T3); biometria dos eleitores a mais perto da base (T9) | `T9_*`, `T21c_*` |
| Programa trocado entre os turnos | Versão ou componente novo | Mesma versão 10.23.0.0 nas 3.897 urnas (T10); 1 erro de verificação na preparação, resolvido no próprio log; pendências de carga em aberto até as atas (T20) | `T20_pendencias_amostra_inteira.json` |
| Troca num modelo ou lote de urna | Diferença entre modelos no mesmo prédio | Sem sinal para antigas contra novas nos 119 locais; sem poder para um modelo só (T17) | `T17_119_locais_antigas_e_novas.txt` |
| Gatilho por horário ou por contagem | Mudança depois de certa hora ou de N votos | Sem sinal depois de controlar a composição (T30) | `T30_gatilhos_amostra_inteira.json` |
| Branco e nulo convertido em 13 (forma A) | Branco/nulo de presidente encolhe frente ao de governador na mesma urna; urna abaixo do declarado | Nas 6 UFs com governador no 2º turno, a inclinação passou de 0,305 no 1º turno para 0,328 no 2º (com a conversão de 52% necessária para virar, cairia para cerca de 0,15). A razão presidente/governador subiu nas 6 UFs (T5 e T39). Datafolha declarava 3% de branco e nulo; foram 3,24%. Nenhum nulo digitado 13 ou 22 (T19). O nulo por suspensão do log não tem poder no 2º turno (T36) | `ADENDO14_e_T39_resultados.txt`, `T19_nulos_rdv_amostra.json`, `T36_nulo_suspensao_amostra.json` |
| Troca de votos de Flávio para Lula (forma B) | Só no voto de presidente; maior onde Flávio é forte | Na mesma urna de AM, DF e ES, o candidato a governador do campo de Flávio perdeu tantos eleitores do 1º turno quanto ele (5,9% contra 4,8%; T22b, sem sinal pela letra, intervalo de -0,032 a +0,054). Entre UFs e entre cidades, a virada foi MENOR onde Flávio é mais forte (nas cidades com Flávio acima de 65%, a margem andou -2,5 pontos; abaixo de 30%, -4,7) | `ADENDO14_e_T39_resultados.txt`, `T38_municipios.txt`, `ADENDO16_resultados.txt` |
| Troca pequena e espalhada, do tamanho do erro das pesquisas | Perda dos próprios eleitores acima de qualquer referência | Coeficiente de Flávio -0,050, no limite do critério (T14); a leitura depende da base (2022 dá 0,048, quase igual; 2018 dá 0,010). Comparando os dois finalistas na mesma força local do adversário, a direita, que era mais fiel em 2018 e 2022, ficou 2,5 pontos menos fiel em 2026 (T35 preliminar, inconclusivo, a 0,05 erro-padrão do limiar) | `T35_e_inversao_do_vazamento_amostra.txt`, `T7_T8_T14_amostra.txt` |

Também testado: as alegações dos posts endossados por Musk. "A conta não fecha" (a soma fecha; ver seção 2). "Prorrogou 3 minutos antes do fechamento": a liminar saiu às 17h03. "Só nos condados amigos": valeu para o país todo. "Um código trava as urnas às 17h": 225 seções da amostra receberam voto depois das 17h. "213 cidades viraram": são 211.

### 5.3 Leitura atual

- A anomalia real: um movimento nacional de cerca de 5 pontos para Lula contra o contexto inteiro, que nenhuma medição prévia captou, concentrado no eleitorado de direita do 1º turno (base de Flávio e eleitores dos eliminados).
- Nos lugares onde as formas de fraude testadas deixariam marca, até agora não apareceu marca: totalização, prorrogação, inserção de votos, programa trocado, modelo de urna, gatilho, conversão de branco e nulo nas 6 UFs com referência na mesma urna, troca só no presidente.
- O que sobra para a tese: uma lógica no programa oficial que poupe os 6 estados com governador no 2º turno (onde a mesma urna dá referência), ou que mexa também no voto de governador; ou algo que aja por igual em todas as urnas e se confunda com eleitor real. O T16, o T34 e a soma completa dos boletins olham parte disso.
- A explicação sem fraude que precisa ser descartada: troca de eleitores entre os turnos. Cerca de 11% dos votantes do 2º turno não tinham votado no 1º (PoderData), o que dá cerca de 14 milhões entrando e 11 milhões saindo. Se quem saiu era mais de direita e quem entrou mais de Lula (PoderData: 50 a 35 entre quem não votou no 1º turno), a urna mostra isso como "eleitor de Flávio que virou Lula", e a pergunta de fidelidade das pesquisas não vê. A ponderação pelo resultado do 1º turno, que o PoderData passou a usar em 13/10, puxaria as pesquisas para Flávio nesse caso. Isso também explica o T22b (quem falta não vota para governador). Indício na amostra, exploratório: dentro do mesmo local de votação, o comparecimento subiu menos onde Flávio era mais forte.

## 6. Pendências

- **Boletins completos do 2º turno (bweb):** o TSE ainda não publicou (última consulta em 27/10, 00h08 UTC; o portal só tem o 1º turno, de 06/10). Previsão: 27 ou 28/10. Quando sair: `rodar_2026.sh` faz a soma de todas as seções contra o total oficial, e roda T4 (seções com branco e nulo zerado), T5, T8, T34 (salto na divisa Sul/não Sul; referência de 2022 pronta: +0,005) e T35 com todas as seções. Faltam scripts para o T16 (piso por UF) e o T14 completo.
- **Teste de integridade:** a urna, o cargo e a direção da divergência do DF no 2º turno; a composição das cédulas (quantos brancos e nulos para presidente). Atas do TRE-DF e relatório do TCU até 24/11. O PL tinha fiscais no teste e pode pedir o vídeo.
- **Troca de eleitores:** o perfil do comparecimento por idade e zona nos dois turnos (dado do TSE) mostra quem deixou de votar.
- **Atas de carga das urnas:** fecham as pendências do T20.
- **Revisão cética:** mover a pasta para o repo `eleicoes-2026` e passar ao Codex (`PARA-O-REVISOR.md` está pronto, mas é anterior aos adendos 14 a 16; atualizar).

## 7. Mapa dos arquivos

| Pasta ou arquivo | O que tem |
|---|---|
| `PRE-REGISTRO-2026-10-26.md` | critérios dos testes T1 a T39, em adendos com horário; cada adendo diz o que já tinha sido visto |
| `PARA-O-REVISOR.md` | passagem para o revisor, erros corrigidos, onde posso estar errado, como reproduzir |
| `CONTEXTO-ELEICAO-2026-original.md` | documento que abriu a sessão |
| `resultados/ADENDO9_resultados_amostra.txt` | T17 a T33 na amostra |
| `resultados/ADENDO14_e_T39_resultados.txt` | governador na mesma urna (T22b, T5 do 2º turno, T22, T39) |
| `resultados/ADENDO16_resultados.txt` | T36, T37, T38 por UF, erro das pesquisas por turno, desenho entre UFs |
| `resultados/T38_municipios.txt` e `.json` | as 5.571 cidades |
| `resultados/T35_e_inversao_do_vazamento_amostra.txt` | a inversão do vazamento e a curva por força do adversário |
| `resultados/contexto_2t_2026_e_onde_estaria_a_fraude.txt` | contexto conferido, anomalias, mapa da fraude, Trump e Musk |
| `resultados/teste_integridade_df_2026.txt` | as divergências do DF |
| `resultados/*_pesquisas_verificadas.txt` | pesquisas levantadas e conferidas |
| `scripts/` | todo o código (mapa em `PARA-O-REVISOR.md`, seção 3); novos nesta etapa: `analisar_pres_gov.py`, `analisar_curva_forca.py`, `analisar_divisa.py`, `analisar_nulo_suspensao.py`, `analisar_eliminados.py`, `baixar_municipios.py`, `analisar_municipios.py` |
| `rodar_2026.sh` | rotina para quando o bweb do 2º turno sair |
| `reproducao/` | listas da amostra, logs de download, ambiente, revisões |

**Dados que não estão no repositório** (ficaram no scratchpad da sessão, que é apagado quando o container é reciclado):
- Bases por seção de 2018 e 2022 (`secoes2018.json.gz`, `secoes2022.json.gz`): vieram nos zips enviados pelo Léo (`eleicao-2026-parte2-secoes2022.zip`, `eleicao-2026-parte3-secoes2018.zip`).
- Base do 1º turno de 2026 (`secoes2026_1t.json.gz`, `candidatos2026_1t.json.gz`, `candidatos_gov_2026_1t_6ufs.json.gz`): refazer a partir do bweb do 1º turno no portal do TSE com `extrair_bweb.py` e `extrair_candidatos.py`.
- Arquivos de urna da amostra (3.897 seções e o estrato G de 2.400 seções): refazer com `sortear_amostra.py` (semente 20261026) e `baixar_arquivos_urna.py`, usando as listas em `reproducao/`.
- Totais do 2º turno por município: refazer com `baixar_municipios.py`.
- Locais de votação com coordenadas: "Eleitorado por local de votação - 2026" no portal do TSE.

## 8. Regras de trabalho

- Critério antes do dado, em commit com horário. Quando o registro estava errado ou o dado já tinha sido visto, isso está declarado no adendo seguinte.
- Fato, indício, evidência e prova são coisas diferentes. "Sinal" é indício e pede cruzamento com outro teste independente.
- Resultado da amostra é provisório; com o bweb completo, refaz-se com o mesmo critério.
- Todo dado baixado é tratado como não confiável: pasta própria, Python com `-I`. Só são pedidos ao TSE arquivos listados pelo próprio TSE; nenhum caminho é adivinhado.
- Ceticismo nos dois sentidos: nem confirmar por simpatia, nem descartar por princípio. Partir do pressuposto de fraude para procurar onde estaria a marca, e relatar o que aparecer.
- Textos sem travessões.
