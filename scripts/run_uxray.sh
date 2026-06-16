#!/usr/bin/env bash
set -e

if [ -z "$1" ]; then
  echo "Usage: ./run_uxray.sh <url>"
  echo "Example: ./run_uxray.sh https://example.com"
  exit 1
fi

URL="$1"

echo "[+] Running crawler for: $URL"
python crawler.py "$URL"

LATEST=$(find evidence -mindepth 1 -maxdepth 1 -type d -printf '%T@ %p\n' | sort -nr | head -1 | cut -d' ' -f2-)

echo "[+] Latest evidence folder:"
echo "$LATEST"

echo "[+] Running analyzer..."
python analyzer.py "$LATEST"

echo ""
echo "[+] Report:"
echo "$LATEST/report.md"
echo ""

cat "$LATEST/report.md"
