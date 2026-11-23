#!/usr/bin/env bash
# Menyalakan Fuseki + dashboard sekaligus (macOS / Linux).
# Pemakaian:  ./dashboard/start_demo.sh ~/Downloads/apache-jena-fuseki-6.3.0
# Berhenti :  tekan Ctrl+C (Fuseki ikut dimatikan).
set -e
DIR="$(cd "$(dirname "$0")" && pwd)"
ROOT="$(cd "$DIR/.." && pwd)"
FUSEKI_HOME="${1:-$HOME/Downloads/apache-jena-fuseki-6.3.0}"
LOG="$ROOT/output/fuseki/fuseki.log"

echo "1/3  Menyalakan Fuseki dari $FUSEKI_HOME (log: output/fuseki/fuseki.log) ..."
bash "$ROOT/output/fuseki/start_fuseki.sh" "$FUSEKI_HOME" > "$LOG" 2>&1 &
FPID=$!
trap 'echo; echo "Mematikan Fuseki ..."; kill $FPID 2>/dev/null; pkill -P $FPID 2>/dev/null; exit 0' INT TERM

echo "2/3  Menunggu Fuseki siap (penalaran 303 aturan butuh beberapa detik) ..."
for i in $(seq 1 90); do
  if curl -s -o /dev/null -w "%{http_code}" "http://localhost:3030/\$/ping" 2>/dev/null | grep -q 200; then
    echo "     Fuseki siap di http://localhost:3030"; break
  fi
  if ! kill -0 $FPID 2>/dev/null; then echo "Fuseki berhenti. Isi log:"; tail -20 "$LOG"; exit 1; fi
  sleep 1
done

echo "3/3  Menyalakan dashboard ..."
python3 "$DIR/server.py"
