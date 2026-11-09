# Bases por seção usadas na investigação

Guardadas no repositório em 09/11/2026 para que uma sessão nova comece sem baixar e extrair gigabytes. Os hashes estão em `SHA256SUMS.txt`. Confira antes de usar: `cd dados && sha256sum -c SHA256SUMS.txt`.

## Estrutura

`secoesAAAA.json.gz` é um dicionário com chave `"UF|municipio|zona|secao"` (exterior com UF `ZZ`). O valor tem `"1"` (1º turno) e `"2"` (2º turno), cada um com:

- `loc`: local de votação
- `urna`: número da urna efetivada
- `tipo`: tipo da seção (Apurada etc.)
- `apt`: aptos
- `comp`: comparecimento
- `ab` e `enc`: abertura e encerramento (só em 2026)
- `L`: candidato do PT
- `R`: adversário
- `O`: outros candidatos
- `B`: brancos
- `N`: nulos

A base de 2026 tem ainda `"1g"`, o governador do 1º turno.

| Arquivo | L | R | Origem e conferência |
|---|---|---|---|
| `secoes2026.json.gz` | Lula 13 | Flávio 22 | bweb do 1º e do 2º turno (dadosabertos.tse.jus.br), `scripts/extrair_bweb.py` e `juntar.py`. Conferida campo a campo contra os zips do bweb no Adendo 25: 499.206 seções no 1º turno e 499.205 no 2º, 0 discordâncias. Soma igual ao oficial. Os votos do 28 (candidato anulado) estão em `O`. |
| `secoes2022.json.gz` | Lula 13 | Bolsonaro 22 | Veio pronta, em zip enviado pelo Léo antes da sessão; código de extração não documentado. O 2º turno bate voto a voto com o oficial. |
| `secoes2018.json.gz` | Haddad 13 | Bolsonaro 17 | Mesma origem da de 2022. O 2º turno bate com o oficial. O 1º turno difere muito pouco (Haddad -46, Bolsonaro -20, válidos +670). Cinco seções com turno anulado. |
| `secoes2014.json.gz` | Dilma 13 | Aécio 45 | bweb de 2014 do TSE (cdn.tse.jus.br/estatistica/sead/eleicoes/eleicoes2014/buweb/), extraída no F21 (Adendo 23). Conferida contra o oficial, diferença 0 nos dois turnos. O bweb de 2014 não tem a hora de recebimento do boletim. |
| `candidatos2026_1t.json.gz` | | | `{"secoes": {chave: {numero: votos}}, "nomes": {numero: nome}, ...}`: votos por candidato a presidente no 1º turno de 2026, por seção (`scripts/extrair_candidatos.py`). |
| `candidatos_gov_2026_1t_6ufs.json.gz` | | | Mesmo formato, para governador no 1º turno, nas 6 UFs com 2º turno de governador. |

Funções de leitura e regressão em `scripts/lib.py` (`carregar`, `chave_local`, `fe_ols`).
