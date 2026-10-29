#!/bin/bash
# $1 = turno, $2 = zip, $3 = saida
unzip -p "$2" '*.csv' | grep -a ';1;"Presidente";' | python3 -I /tmp/claude-0/-home-user-casa-control/ce2a8c88-e5ad-504f-8950-6f5ee14ae721/scratchpad/conferencia_adendo18/L8/extrair.py "$1" "$3"
