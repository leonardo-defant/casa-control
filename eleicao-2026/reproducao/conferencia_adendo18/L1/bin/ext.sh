#!/bin/bash
# uso: ext.sh <zip> <dir_saida>   (uma linha por combinação distinta dos campos de seção; conta linhas com NF != 45)
z="$1"; out="$2/$(basename "$z" .zip).txt"
unzip -p "$z" '*.csv' | mawk -F';' 'NR>1{ if (NF!=45) {bad++; next}; l=$11";"$12";"$13";"$14";"$15";"$16";"$22";"$23";"$24";"$26";"$33";"$34";"$35";"$36";"$37";"$39";"$40";"$41";"$43";"$44";"$45";"$7";"$8; if (!(l in s)) {s[l]=1; print l} } END{print "bad="bad+0" linhas="NR > "/dev/stderr"}' > "$out.tmp" && mv "$out.tmp" "$out"
echo "ok $(basename $z) $(wc -l < $out)"
