# Auditoria do 2º turno presidencial de 2026: passagem para o revisor cético

Este documento entrega a pesquisa feita em 26/10/2026 a um revisor independente (Codex). O papel do revisor é tentar derrubar cada conclusão, nos dois sentidos: achar fraude que eu deixei passar e achar erro meu que fabrique ou esconda um sinal. Tudo o que está aqui pode e deve ser refeito a partir do código e dos dados.

Estado em 26/10/2026, fim da tarde (UTC): os boletins de urna do 2º turno em formato aberto (bweb) ainda não estavam publicados no portal de dados abertos do TSE. Os testes rodaram numa amostra de arquivos de urna baixados um a um do site de resultados.

## 1. A pergunta

O Léo (dono da pesquisa) acredita que a eleição foi fraudada. A tese principal dele: o programa da urna estaria corrompido, com um desvio programado antes, e teria "errado a mão" no 2º turno (Lula ganhou cerca de 10,4 milhões de votos entre os turnos; Flávio, cerca de 3,7 milhões). Variante inicial: votos brancos e nulos de presidente registrados como votos em Lula. Ele parte do pressuposto de que a urna não é confiável e pediu uma "caçadora cética da verdade", sem suavizar resultados em nenhuma direção.

Resultado oficial do 2º turno (soma dos 28 arquivos por UF e exterior do TSE): Lula 64.256.232, Flávio 59.826.041, brancos 1.430.496, nulos 2.723.305, comparecimento 128.236.074. Margem de 4,43 milhões de votos.

Regras que segui:
1. Critério antes do dado. Todo teste tem critério registrado num commit com horário antes de olhar o dado correspondente (`PRE-REGISTRO-2026-10-26.md`, adendos 1 a 13). Quando o registro estava errado, corrigi num adendo novo, dizendo o que já tinha sido visto.
2. Fato, indício, evidência e prova são coisas diferentes. "Sinal" é indício e pede cruzamento com outro teste independente.
3. Para cada teste: o que foi testado, o critério, o número, se apoia ou contraria a tese e o que fica sem teste.
4. Script reescrito só vale depois de reproduzir as referências de 2018 e 2022 do documento original.
5. Resultado da amostra é provisório; com o bweb completo, refaz-se com o mesmo critério.

## 2. Dados e como foram obtidos

| Dado | Fonte | Observação |
|---|---|---|
| bweb do 1º turno de 2026, de 2022 e de 2018 | portal de dados abertos do TSE (CKAN), arquivos por UF | base por seção: `secoes2026_1t.json.gz`, `secoes2022.json.gz`, `secoes2018.json.gz` (fora do repositório, no scratchpad da sessão) |
| votos por candidato no 1º turno de 2026 | mesmo bweb, `extrair_candidatos.py` | `candidatos2026_1t.json.gz` |
| arquivos de urna do 2º turno (boletim, RDV, log, assinatura) | `resultados.tse.jus.br/oficial/ele2026/arquivo-urna/3221/dados/{uf}/{mun}/{zona}/{secao}/` | o `-aux.json` de cada seção lista o hash e os arquivos; só arquivos listados foram pedidos |
| total oficial por UF e por município | `resultados.tse.jus.br/oficial/ele2026/6258/dados/...` | usado no T1 e na soma nacional |
| pesquisas | imprensa, com conferência em segunda fonte quando possível | `resultados/*_pesquisas_verificadas.txt` |

Cuidados:
- Todo dado baixado foi tratado como não confiável: pastas próprias, Python sempre com `-I`.
- O site de resultados limita a taxa (HTTP 429 da Akamai). O baixador (`baixar_arquivos_urna.py`) tem limitador global (cerca de 1,3 requisição por segundo) e recuo após 429.
- Nenhum caminho do TSE foi adivinhado. O caminho de 2022 no mesmo padrão (`ele2022/arquivo-urna/407/...`) respondeu 404 e não foi tentado outro.
- Os endereços de lista de revogação e de política das AC do TSE, citados nos próprios certificados, responderam 403 a partir deste ambiente.

Amostra do 2º turno (`sortear_amostra.py`, semente 20261026), em três estratos:
- **M:** 120 municípios inteiros.
- **L:** 1.500 locais de votação.
- **G:** metade dos locais das 6 UFs com 2º turno de governador.

O download parou no limite de 2 horas da tarefa em segundo plano. Ficaram 3.897 seções com boletim, em 625 locais. Delas, 835 têm também RDV, log e arquivo de assinatura. Depois vieram mais duas levas:
- **Logs das outras 3.062 seções** (Adendo 12).
- **Extensão dirigida do T17** (Adendos 10 e 11):
  - 264 seções sorteadas entre os locais com modelos misturados;
  - todas as 1.335 seções dos 119 locais do país que têm urnas antigas e novas juntas.

## 3. Mapa do código (`scripts/`)

| Script | Função |
|---|---|
| `lib.py` | leitura das bases; `fe_ols` (efeito fixo por desvio da média do grupo, peso, erro agrupado CR1) |
| `ber.py`, `decodificar.py` | leitura genérica de BER; boletim (`ler_bu`), RDV (`ler_rdv`), log (`_linhas_log`, inclusive os .jez internos de contingência) |
| `extrair_bweb.py`, `extrair_candidatos.py`, `juntar.py`, `somar_oficial.py` | montam as bases por seção a partir do bweb |
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
| `rodar_2026.sh` | rotina completa para quando o bweb do 2º turno sair (sai com código 2 enquanto não sai) |

## 4. Resultados por teste

Veredito pelo critério pré-registrado. "Amostra" quer dizer provisório.

| Teste | O que pegaria | Resultado | Veredito |
|---|---|---|---|
| T1 soma dos boletins contra o total oficial | alteração na totalização | 10 municípios inteiros (734 seções): diferença zero em todos os campos | sem sinal |
| T2 RDV contra boletim | registro interno incoerente | 835 seções, candidato a candidato: zero diferença | sem sinal |
| T3 log: horários e ritmo | voto fora de hora, sem habilitação, rajadas | 3.897 seções: zero em A1 a A5 | sem sinal |
| T4 zeros de branco+nulo | conversão total em parte das urnas | só referências calibradas; 2026 2º turno depende do bweb | pendente |
| T5 presidente contra governador (1º turno) | conversão de branco/nulo recorrente | beta 2026 0,348; 2018 0,429; 2022 0,293 (2026 é 1,19 vez o menor) | sem sinal |
| T6 branco/nulo declarado contra registrado | branco/nulo "sumido" | Datafolha: registrado menos declarado +1,57 (2018), +0,59 (2022), +0,24 (2026) | sem sinal |
| T7 ganho além do bolo da seção | troca de voto ou de eleitor | 10,57% das seções e 1,71% do ganho (2022: 5,27% e 1,09%; troca simulada de 2%: 12,43% e 2,09%) | inconclusivo: (a) passou 5,3 pontos da referência, (b) só 0,6 |
| T8 fluxo por seção | coeficiente fora de 0 a 1 | Lula recebeu 0,53 dos outros, 0,667 da queda de branco/nulo, 0,605 do aumento do comparecimento; todos dentro de 0 a 1 | sem sinal |
| T9 biometria dos eleitores a mais | votos em nome de faltosos | 3.873 seções: 0,139 (0,016) dos eleitores a mais sem biometria, como a base de 12,2%; ganho de Lula por habilitação a mais 0,56 sem biometria e 0,51 com | sem sinal |
| T10 programa e mídia entre os turnos | programa trocado | 3.897 urnas: mesma versão 10.23.0.0, nenhum componente novo; 1 verificação de assinatura com ERRO, em 22/09, na preparação (urna recusou a mídia, religada e verificada com sucesso; tudo SUCESSO nos dois dias de votação) | bandeira literal em 1 urna, explicada pelo log |
| T11 pesquisa: presidente contra governador na mesma amostra | fraude só no presidente | AtlasIntel, 6 UFs: D médio -1,47 | sem sinal |
| T12 mudança do erro de cada instituto entre turnos | erro anômalo em 2026 | -1,32 em média | sem sinal |
| T13 teto de Lula pela rejeição | voto acima do possível | Lula abaixo do próprio teto nos 8 institutos | sem sinal |
| T14 marca de troca de votos | troca proporcional dos votos de Flávio | 0,051 (0,007); limite de "sem sinal" era 0,051 | sem sinal no limite; base de referência ambígua (ver seção 7) |
| T17 modelo da urna no mesmo prédio | troca restrita a um modelo ou às urnas novas | antigas menos novas nos 119 locais: -0,016 (0,140); seria preciso cerca de 2,2 | sem sinal |
| T18 assinatura digital | arquivo trocado depois da urna | 835 seções, 9.185 arquivos e 835 blocos válidos; SHA-256 do vsc igual ao hash do aux em 835 | sem sinal (refazer com as 3.897) |
| T19 conteúdo dos nulos | candidato contado como nulo | zero nulos de presidente digitados 13 ou 22 em 5.087 | sem sinal no item forte; (b) sem referência |
| T20 pendências do T10 | carga ou programa fora do oficial | 3.897 urnas: 426 pendências, 426 explicadas no próprio log (2 regras definidas depois de ver os dados: sessão de geração da zona e computador da própria zona); votáveis 13 e 22 em 3.897 boletins | sem sinal (faltam as atas de carga) |
| T30 gatilho por horário | troca depois de certa hora | 3.874 seções: +5,0 (1,4) às 14h e +11,3 (2,7) às 16h passam valor e z, mas o placebo falha (+16); com local e fatia do 1º turno: +1,1, +1,1 e +4,1 (2,1), z 1,95 às 16h | sem poder pelo critério; leitura de composição, às 16h no limite (ver seção 7) |
| T21(c) biometria no fim do dia | inserção tardia | das 15h30 em diante, sem biometria 12,1% no 1º turno e 12,6% no 2º (+0,49 na mesma urna); ganho de Lula igual por habilitação tardia com e sem biometria (0,47) | descritivo |
| T30 gatilho por contagem | troca depois de N votos | -1,4 a -2,5 | sem sinal |
| T33 pesquisas em votos totais | separar conversão de troca | Flávio abaixo do que as pesquisas davam em 8 de 9 institutos, 1,6 ponto em média além do histórico; só 1 passou de 3 | inconclusivo; pesa contra a tese "só conversão de branco/nulo" |

Detalhes e números completos: `resultados/ADENDO9_resultados_amostra.txt` (T17 a T33) e os arquivos citados em cada linha.

## 5. Leitura de conjunto

O que os testes já excluem ou enfraquecem muito, cada um pela sua via:
- **Alteração depois da urna:** totalização (T1), arquivo trocado (T18) ou programa diferente do lacrado (T10, T20).
- **Troca concentrada em parte das urnas:** um modelo (T17, dentro do limite de SP para antigas contra novas), um lote ou urnas de contingência. Esse cenário criaria saltos locais (T7) e precisaria escapar de todas as urnas sorteadas para o teste de integridade.
- **Conversão de branco/nulo como explicação única:**
  - O branco+nulo do 2º turno foi de 4,15 milhões, menos que a margem.
  - A queda entre turnos (32%) está dentro da faixa histórica de 2002 a 2014, quedas de 22% a 42% (`historico_comparecimento_bn.txt`).
  - T5, T6 e T8 sem sinal.
  - T33 indica que parte do erro das pesquisas está nos votos de Flávio, não no branco/nulo.
- **Votos em nome de faltosos em grande escala:** T9 e T3, ambos com as 3.897 seções.
- **Programa ou carga fora do oficial:** T10 e T20 nas 3.897 urnas, com todas as pendências explicadas no log.

O que continua aberto:
- **Troca uniforme pequena e espalhada,** do tamanho do erro das pesquisas.
  - T7 (inconclusivo) e T14 (no limite) são compatíveis com algo entre 1% e 2% de "troca" quando a base é 2022, e com cerca de 4,5% quando a base é 2018.
  - Isso inclui eleitores reais que votaram em Flávio no 1º turno e em Lula no 2º, e a troca de eleitores entre os turnos.
  - Esses dois testes não separam isso de fraude.
  - O T16 (cauda inferior por UF, com o bweb) é o teste desenhado para isso.
- **Testes que dependem do bweb:** T4 no 2º turno, T5 no 2º turno, T15, T16, T21 a T23, T27 a T29, T31 e T32, e os testes da seção 7 do documento original (modelo, bn_secao, governador).
- **Testes que dependem de dado externo:**
  - T24: QR dos boletins impressos coletados por fiscais.
  - T25: caderno de votação físico e óbitos.
  - T26: seções sorteadas para o teste de integridade e relatórios oficiais.

O que não tem teste com dado público:
- **Lógica maliciosa dentro do programa oficial assinado, agindo por igual em todas as urnas.** Nos resultados ela se confunde com troca real de eleitores. As barreiras são a inspeção de código e o desenho do teste de integridade, que não deixam rastro em dado público.
- **Linhas de base contaminadas:** uma alteração constante em todos os anos não aparece em nenhuma comparação relativa.
- **Se cada voto gravado é o que o eleitor digitou:** o voto é secreto e não há comprovante individual.
- **Compra de votos e coação** de eleitores reais.

Fatos de contexto já checados:
- **Prorrogação do horário:** na prática, as seções fecharam às 17h e o último voto foi às 17h03. O TSE pausou a totalização às 17h20 e uma segunda decisão estreitou o alcance da prorrogação. Isso corrige o "99,8% fecharam às 19h" do documento original.
- **Erro médio das pesquisas no 2º turno:**
  - 2026: +2,63 pontos a favor de Lula.
  - 2022: -1,18.
  - 2018: -0,20.
  - Veritá e Gerp, as que mais acertaram o 1º turno, foram as que mais erraram o 2º (+3,35 e +3,79).
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
  - Nenhum veredito mudou. Tudo está corrigido e listado no fim de `ADENDO9_resultados_amostra.txt`.

## 7. Onde eu posso estar errado (comece por aqui)

1. **Linha de base do T14 e do T7.**
   - O coeficiente de 2026 (0,051) equivale a cerca de 1,4% de troca sobre a base de 2022 e a cerca de 4,5% sobre a de 2018. Eu li isso como "no limite".
   - Um revisor pode argumentar que a base certa é a de 2018, quando quem ganhou terreno também era o PT. Nesse caso, a troca equivalente se aproxima dos 3,6% que decidiriam a eleição.
   - Meu contra-argumento: em 2026 os eliminados (Cury, Renan Santos, Caiado) são outros, e a composição muda o coeficiente. Mas isso não está provado.
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
6. **Amostra:** são 625 locais. Os estratos M e G pesam municípios específicos (por exemplo, MG 46337 e BA 34193 têm muitas seções). Os testes por seção usam efeito fixo de local, mas a generalização para o país é de amostra.
7. **Pesquisas:**
   - Os números vêm da imprensa, não dos PDFs registrados no TSE.
   - Vários totais são ambíguos (indecisos somados a branco/nulo).
8. **Modelo da urna pela faixa de série:** conferido contra o arquivo de assinatura nas 835. Nas demais seções é inferido.

## 8. Como reproduzir

```
# bases do 1º turno e de 2018/2022 a partir do bweb (ver cabeçalho de cada script)
python3 -I scripts/extrair_bweb.py 1 secoes2026_1t.json.gz <zips do bweb do 1º turno>
python3 -I scripts/extrair_candidatos.py ...
# amostra do 2º turno
python3 -I scripts/sortear_amostra.py ...
TAXA=1.3 python3 -I scripts/baixar_arquivos_urna.py 3221 <lista> <pasta> bu,rdv,log,vota 3
python3 -I scripts/analisar_amostra.py <pasta_2t> <pasta_1t> secoes2026_1t.json.gz <lista_municipios> <saida>
# testes do adendo 9
python3 -I scripts/verificar_assinaturas.py <pasta_2t>
python3 -I scripts/verificar_ac_ecdsa.py <pasta_2t>
python3 -I scripts/analisar_nulos_rdv.py <pasta_2t> secoes2026_1t.json.gz candidatos2026_1t.json.gz <amostra_2t>
python3 -I scripts/analisar_pendencias.py <pasta_2t> <T10_software.json> secoes2026_1t.json.gz <amostra_2t>
python3 -I scripts/analisar_maquina.py secoes2026_1t.json.gz <amostra_2t> <T3_logs.json> --extensao_pares <pasta_t17> --extensao_contraste <pasta_t17b>
python3 -I scripts/analisar_gatilhos.py <pasta_2t> secoes2026_1t.json.gz <amostra_2t> secoes2022.json.gz [--chaves lista]
python3 -I scripts/analisar_pesquisas_totais.py
# quando o bweb do 2º turno sair
DADOS=<pasta das bases> TRAB=<pasta de trabalho> ./rodar_2026.sh
```

As bases e os arquivos de urna não estão no repositório, por tamanho (cerca de 600 MB). Todos vêm de fontes públicas do TSE pelos caminhos acima.

## 9. Pendências

1. Quando o bweb do 2º turno sair, rodar `rodar_2026.sh` e os testes que dependem dele, com os critérios já registrados.
2. Comparar a impressão digital da chave da AC URNA com o certificado publicado pelo TSE.
3. Obter as atas de carga (T20), as coletas de QR dos fiscais (T24), o caderno de votação e os óbitos (T25) e os relatórios do teste de integridade (T26).
