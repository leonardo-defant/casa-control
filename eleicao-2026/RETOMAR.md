# Retomar a investigação numa sessão nova

Passagem escrita em 09/11/2026 para continuar ou refazer o trabalho com outro modelo. Vale junto com o `README.md` (ponto de entrada até o Adendo 22) e o `PRE-REGISTRO-2026-10-26.md` (critérios de todos os testes).

## 1. Onde está tudo

| Onde | O que tem |
|---|---|
| GitHub `leonardo-defant/casa-control`, branch `claude/new-session-5cnflo`, pasta `eleicao-2026/` | Tudo o que foi achado, em commits com horário. É a fonte da verdade. |
| `PRE-REGISTRO-2026-10-26.md` | Critérios de cada teste, escritos antes de rodar: registro inicial (T1 a T6) e Adendos 1 a 26. |
| `README.md` | Situação, tese do Léo, fatos conferidos e resultados até o Adendo 22. Os Adendos 23 a 26 estão resumidos aqui, na seção 4. |
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

## 4. Estado em 09/11/2026

### 4.1 Leitura atual

Nenhum teste com dado público mostrou marca de fraude.

**Portas fechadas pelos dados:**
- **Totalização e transmissão:** a soma dos boletins é igual ao oficial e as assinaturas conferem.
- **Prorrogação:** não muda o resultado.
- **Inserção de votos pelo mesário:** voto sem habilitação é zero.
- **Dígitos e números redondos.**
- **Modelo de urna:** a vantagem nas urnas antigas some quando se usa o prédio em que a seção de fato votou.
- **Carga das urnas, horários e certificados:** as 18 seções com horário fora do padrão (L1) fecham nos próprios arquivos; nos certificados houve falha de gestão, mas as assinaturas valem.
- **Alegações das redes checadas:** 84,7 segundos, digitais órfãs e 10 votos por urna.

**O que fica de pé:**
- **Urna contra pesquisas no 2º turno** (L5a, Adendo 18): cerca de 2,7 pontos a mais para Lula do que as pesquisas mediam, concentrados no eleitorado de direita do 1º turno. Depende do método: os painéis online calibrados (AtlasIntel, Palver) mediram perto da urna. Não se separa, com dado público, entre transferência, comparecimento e contagem.
- **Comparecimento:** subiu 2,92 milhões do 1º para o 2º turno, a maior alta da série. Os votantes a mais se dividiram como os demais.
- **Exterior:** ficou 0,65 ponto abaixo de seções do Brasil de composição igual, concentrado em alguns países (Japão, Paraguai, Líbano, Espanha). Nos EUA, zero.
- **Seções novas de 2026:** as 37.986 que não existiam em 2022 têm assimetria maior (-0,058 contra -0,011), com virada igual.
- **A única porta aberta:** um programa adulterado na origem que reconheça o teste de integridade. Só a compilação independente do código-fonte e a publicação dos resumos (hash.dat) fecham.

### 4.2 Adendos e vereditos

| Adendo | O que testou | Resultado | Arquivo |
|---|---|---|---|
| 1 a 17 | Totalização, inserção, branco e nulo, troca de votos, modelos, gatilhos, governador na mesma urna, curva por força | Nenhum sinal. Pontos inconclusivos listados no README, seção 5.2 | `README.md` seções 5.1 a 5.3; `ADENDO9`, `ADENDO14`, `ADENDO16` |
| 18 e 19 | Incoerências de lógica só dentro de 2026 (L1 a L8) e errata | A incoerência que se sustenta é urna contra pesquisas (L5a); nenhuma marca física | `ADENDO18_resultados.txt` |
| 20 a 22 | Testes forenses nos boletins e o que não depende de ninguém (F2 a F18) | Sem sinal. Urnas antigas explicadas pelo prédio. Falhas de gestão sem efeito nos votos | `ADENDO20/21/22_resultados.txt` |
| 23 | Exterior pareado (F19), governador nas UFs (F20), série 2014 a 2026 (F21) | F19 inconclusivo (-0,65, menos da metade do que viraria); F20 inconclusivo pela letra, sem sinal tirando AC e TO; F21 inconsistente com mecanismo repetido a favor do PT | `ADENDO23_resultados.txt`, `CACA_AO_FURO.txt` |
| 24 | Reel @assis.salvioli, "digitais órfãs" | Contagens certas, conclusão errada. O +15,6 é nível sem o 1º turno; com controle, -0,13 ponto (ep 0,38). O 139 e o 79 são erros de digitação na mesa | `ADENDO24_resultados.txt` |
| 25 | Vídeo "10 votos extras para Lula por urna" | Conta circular: o 5.354.957 é o ganho menos 10 vezes as urnas. Sem marca física (b = 0,951 contra 4,8 a 10 previstos) | `ADENDO25_resultados.txt` |
| 26 | Postagem "2014 parecida com 2026" (Felipe Cecílio) | O autor não diz as métricas. 2014 é o ano mais perto de 2026 em só 3 de 10. 2026 sem sinal nos padrões de perícia. A auditoria do PSDB de 2014 não achou fraude na totalização | `ADENDO26_resultados.txt` |

### 4.3 Pistas abertas, em ordem de valor

1. **2014 por modelo de urna dentro do local.**
   - O relatório da auditoria do PSDB (pp. 135 e 136) deixou em aberto um padrão bruto: margem de Dilma maior nas urnas com biometria e nas com circuito MSD.
   - Em 2026, o padrão parecido sumiu dentro do local.
   - Dá para testar com a base de 2014, se o modelo sair do número da urna. Precisa de adendo novo.
2. **Seções novas de 2026 e exterior país a país** (2022 contra 2026). Oferecidos ao Léo, ainda não registrados.
3. **Digitais órfãs** (falta de auditoria real, sem marca no voto):
   - pedir ao TRE-MG os arquivos `wsqmes.jez` e `wsqman.jez` de Itabira (MG|46337, zona 132);
   - pedir os cadernos de votação de BA|39713|68|82 e PI|10243|13|199.
4. **Pedidos a terceiros:**
   - compilação independente do código-fonte;
   - publicação do hash.dat;
   - detalhe da divergência do teste de integridade na CLDF;
   - relatório do TCU (até 24/11/2026) e da missão da UE;
   - perfil do comparecimento por idade e zona nos dois turnos.
5. **Painel essencia-ai.com:**
   - conferir a seção real do "Caso 1" (MA, zona 106, seção 163) como no C3;
   - descobrir o filtro do universo de 492.988 seções.
6. **Picos de comparecimento por município**, ligados a revisões biométricas do cadastro (P3 do Adendo 26).

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
