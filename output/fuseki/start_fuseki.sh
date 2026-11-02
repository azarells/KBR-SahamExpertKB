#!/usr/bin/env bash
# Menjalankan Apache Jena Fuseki 6.x dengan SahamExpertKB v2 (macOS / Linux)
# Pemakaian:  ./start_fuseki.sh /path/ke/apache-jena-fuseki-6.2.0
set -e
DIR="$(cd "$(dirname "$0")" && pwd)"
FUSEKI_HOME="${1:-$HOME/Downloads/apache-jena-fuseki-6.2.0}"
if [ ! -x "$FUSEKI_HOME/fuseki-server" ]; then
  echo "fuseki-server tidak ditemukan / tidak executable di: $FUSEKI_HOME"
  echo "Jalankan: chmod +x \"$FUSEKI_HOME\"/fuseki-*  dan  xattr -dr com.apple.quarantine \"$FUSEKI_HOME\""
  exit 1
fi
# Jena 6 butuh Java 21+. Pakai JDK 25 bila terpasang (macOS).
if [ -x /usr/libexec/java_home ]; then
  JH=$(/usr/libexec/java_home -v 25 2>/dev/null || /usr/libexec/java_home -v 21+ 2>/dev/null || true)
  [ -n "$JH" ] && export JAVA_HOME="$JH" && export PATH="$JAVA_HOME/bin:$PATH"
fi
java -version 2>&1 | head -1
DIR_URI=$(printf '%s' "$DIR" | sed 's/ /%20/g')
sed "s#__DIR__#${DIR_URI}#g" "$DIR/config_saham.template.ttl" > "$DIR/config_saham.ttl"
echo "Config: $DIR/config_saham.ttl"
echo "Buka UI: http://localhost:3030   (dataset: /saham dan /saham-pellet)"
cd "$FUSEKI_HOME"
exec ./fuseki-server --config="$DIR/config_saham.ttl"
