#!/bin/bash
# Rotina para quando o TSE publicar os boletins (bweb) do 2º turno de 2026.
# Código 2 = ainda não publicado. Requer: python3 com numpy, curl, unzip; ~6 GB livres.
# Uso: DADOS=<pasta com secoes2018/2022/2026_1t.json.gz> TRAB=<pasta de trabalho> [LOCAIS=<pasta CSV locais 2026>] ./rodar_2026.sh
set -euo pipefail
AQUI="$(cd "$(dirname "$0")" && pwd)"; SC="$AQUI/scripts"; RES="$AQUI/resultados"
DADOS="${DADOS:?defina DADOS}"; TRAB="${TRAB:?defina TRAB}"; mkdir -p "$TRAB/zips2t" "$RES"
# o parâmetro _ evita resposta velha guardada em cache no caminho (aconteceu em 28/10: o cache ainda mostrava o pacote sem o 2º turno)
curl -sS --max-time 60 "https://dadosabertos.tse.jus.br/api/3/action/package_show?id=resultados-2026-boletim-de-urna&_=$(date +%s)" -o "$TRAB/ckan.json" || exit 1
python3 -I -c "
import json,sys
r=json.load(open('$TRAB/ckan.json'))['result']['resources']
u=[x['url'] for x in r if '/bweb_2t_' in x['url']]
# o catálogo pode listar o .sha512 no lugar do .zip (aconteceu com RR em 27/10/2026): o zip sai do nome do .sha512
zips={x for x in u if x.endswith('.zip')}
zips|={x[:-7] for x in u if x.endswith('.zip.sha512')}
u=sorted(set(u)|zips)
open('$TRAB/urls2t.txt','w').write('\n'.join(u)+'\n')
print(len({x.split('/bweb_2t_')[1][:2] for x in zips}))" > "$TRAB/n2t.txt"
N=$(cat "$TRAB/n2t.txt")
echo "UFs (mais exterior) com boletim do 2º turno no portal: $N de 28"
if [ "$N" -lt 28 ]; then echo "boletins do 2º turno ainda não publicados (ou incompletos)"; exit 2; fi
bash "$AQUI/scripts/baixar_bweb.sh" "$TRAB/urls2t.txt" "$TRAB/zips2t" > "$TRAB/download2t.log" 2>&1
tail -30 "$TRAB/download2t.log"
if grep -q "SHA DIFERENTE\|DESISTIU" "$TRAB/download2t.log"; then echo "download com problema; veja $TRAB/download2t.log"; exit 3; fi
cd "$SC"
python3 -I extrair_bweb.py 2 "$TRAB/secoes2026_2t.json.gz" "$TRAB"/zips2t/*.zip
python3 -I juntar.py "$TRAB/secoes2026.json.gz" "$DADOS/secoes2026_1t.json.gz" "$TRAB/secoes2026_2t.json.gz"
SAIDA="$RES/soma_oficial_2t.json" python3 -I somar_oficial.py "$TRAB/secoes2026.json.gz" 2 > "$RES/soma_oficial_2t.txt"
python3 -I analisar_modelos.py "$TRAB/secoes2026.json.gz" 2026 > "$RES/modelos_2026.json"
python3 -I analisar_bn_secao.py "$TRAB/secoes2026.json.gz" 2026 > "$RES/bn_secao_2026.json"
python3 -I analisar_gov.py "$TRAB/secoes2026.json.gz" 2026 > "$RES/gov_2026.json"
python3 -I analisar_zeros.py "$TRAB/secoes2026.json.gz" 2 > "$RES/zeros_2026_2t.json"
python3 -I analisar_pres_gov_nivel.py "$TRAB/secoes2026.json.gz" 2 > "$RES/T5_2026_2t.json"
python3 -I analisar_fluxo_regressao.py "$TRAB/secoes2026.json.gz" L > "$RES/T8_2026_bweb_L.json"
python3 -I analisar_fluxo_regressao.py "$TRAB/secoes2026.json.gz" R > "$RES/T8_2026_bweb_R.json"
# T35 (Adendo 15): perda própria por força local do adversário, todas as seções
python3 -I analisar_curva_forca.py "$TRAB/secoes2026.json.gz" "$DADOS/secoes2022.json.gz" "$DADOS/secoes2018.json.gz" > "$RES/T35_curva_forca_bweb.json"
# T34 (Adendo 15): divisa Sul/não Sul; LOCAIS = pasta com os CSV de eleitorado_local_votacao_2026 (PR SC RS SP MS MG GO MT RJ)
if [ -n "${LOCAIS:-}" ]; then python3 -I analisar_divisa.py "$TRAB/secoes2026.json.gz" "$LOCAIS" "$RES/T34_divisa_2026.json" > "$RES/T34_divisa_2026.txt"; fi
echo "pronto: resultados em $RES"
