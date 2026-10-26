#!/bin/bash
# Rotina para quando o TSE publicar os boletins (bweb) do 2º turno de 2026.
# Código 2 = ainda não publicado. Requer: python3 com numpy, curl, unzip; ~6 GB livres.
# Uso: DADOS=<pasta com secoes2018/2022/2026_1t.json.gz> TRAB=<pasta de trabalho> ./rodar_2026.sh
set -u
AQUI="$(cd "$(dirname "$0")" && pwd)"; SC="$AQUI/scripts"; RES="$AQUI/resultados"
DADOS="${DADOS:?defina DADOS}"; TRAB="${TRAB:?defina TRAB}"; mkdir -p "$TRAB/zips2t" "$RES"
curl -sS --max-time 60 "https://dadosabertos.tse.jus.br/api/3/action/package_show?id=resultados-2026-boletim-de-urna" -o "$TRAB/ckan.json" || exit 1
python3 -I -c "
import json,sys
r=json.load(open('$TRAB/ckan.json'))['result']['resources']
u=[x['url'] for x in r if '/bweb_2t_' in x['url']]
open('$TRAB/urls2t.txt','w').write('\n'.join(u)+'\n')
print(len(u))" > "$TRAB/n2t.txt"
N=$(cat "$TRAB/n2t.txt")
echo "arquivos do 2º turno no portal: $N"
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
echo "pronto: resultados em $RES"
