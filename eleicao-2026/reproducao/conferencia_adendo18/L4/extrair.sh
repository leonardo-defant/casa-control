#!/bin/bash
# extrai linhas de Presidente (CD_CARGO_PERGUNTA=1) do bweb: UF;MUN;ZONA;SECAO;LOCAL;APTOS;COMP;TIPO_URNA;TIPO_VOTAVEL;NR_VOTAVEL;VOTOS;NR_URNA;AGREG
zip="$1"; out="$2"
unzip -p "$zip" '*.csv' | LC_ALL=C awk -F';' 'NR>1 && $17==1 {print $11";"$12";"$14";"$15";"$16";"$23";"$24";"$26";"$28";"$30";"$32";"$33";"$39}' | tr -d '"' | gzip -1 > "$out"
