#!/bin/bash
# uso: baixar_bweb.sh <urls.txt> <pasta_destino>
# baixa zips e .sha512, confere hash e integridade, com até 5 tentativas por arquivo
URLS="$1"; DEST="$2"; mkdir -p "$DEST"
baixa() {
  u="$1"; d="$2"; f="$d/$(basename "$u")"
  for t in 1 2 3 4 5; do
    curl -sS -L --max-time 3600 --retry 3 -o "$f.part" "$u" && \
    if [[ "$f" == *.zip ]]; then head -c 4 "$f.part" | grep -q "PK" ; else ! grep -qi "<html" "$f.part"; fi && \
    mv "$f.part" "$f" && echo "ok $f" && return 0
    echo "falha $t $u"; sleep $((t*10))
  done
  echo "DESISTIU $u"; return 1
}
export -f baixa
grep -v '^$' "$URLS" | xargs -P 4 -I{} bash -c 'baixa "$@"' _ {} "$DEST"
cd "$DEST"
for z in *.zip; do
  esperado=$(awk '{print $1}' "$z.sha512" 2>/dev/null | head -1)
  obtido=$(sha512sum "$z" | awk '{print $1}')
  if [ "$esperado" == "$obtido" ]; then echo "sha ok $z"; else echo "SHA DIFERENTE $z esperado=$esperado"; fi
done
