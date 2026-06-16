#!/usr/bin/env bash
set -u -o pipefail
export PATH="/home/ubuntu/uxray-ai/venv/bin:$PATH"
SITES=(
  "https://www.worten.pt"
  "https://www.auchan.pt"
  "https://www.booking.com"
  "https://www.continente.pt"
  "https://www.flytap.com"
  "https://www.meo.pt"
  "https://www.radiopopular.pt"
  "https://www.nos.pt"
  "https://www.publico.pt"
  "https://expresso.pt"
  "https://www.fnac.pt"
  "https://www.cgd.pt"
  "https://www.millenniumbcp.pt"
  "https://www.fidelidade.pt"
  "https://www.rtp.pt"
  "https://www.sapo.pt"
  "https://www.pingodoce.pt"
  "https://www.lidl.pt"
  "https://www.ageas.pt"
  "https://www.vodafone.pt"
  "https://www.edp.pt"
)
mkdir -p log_gpt55
LOG="log_gpt55/batch_$(date +%Y%m%d_%H%M%S).log"
CSV="log_gpt55/batch_$(date +%Y%m%d_%H%M%S)_folders.tsv"
echo -e "url\tstatus\tfolder" > "$CSV"
echo "GPT-5.5 / current environment UX-Ray batch" | tee "$LOG"
echo "Started: $(date -Iseconds)" | tee -a "$LOG"
echo "Sites: ${#SITES[@]}" | tee -a "$LOG"
OK=0
FAIL=0
for URL in "${SITES[@]}"; do
  echo "" | tee -a "$LOG"
  echo "===== $URL =====" | tee -a "$LOG"
  START_TS=$(date +%s)
  if timeout 120 ./run_uxray.sh "$URL" 2>&1 | tee -a "$LOG"; then
    LATEST=$(find evidence -mindepth 1 -maxdepth 1 -type d -newermt "@$START_TS" -printf '%T@ %p\n' 2>/dev/null | sort -nr | head -1 | cut -d' ' -f2- || true)
    if [ -n "$LATEST" ] && [ -f "$LATEST/report.md" ]; then
      OK=$((OK+1))
      echo -e "$URL\tok\t$LATEST" >> "$CSV"
      echo "RESULT: ok latest=$LATEST" | tee -a "$LOG"
    else
      FAIL=$((FAIL+1))
      echo -e "$URL\tno_report\t$LATEST" >> "$CSV"
      echo "RESULT: no_report latest=$LATEST" | tee -a "$LOG"
    fi
  else
    FAIL=$((FAIL+1))
    LATEST=$(find evidence -mindepth 1 -maxdepth 1 -type d -newermt "@$START_TS" -printf '%T@ %p\n' 2>/dev/null | sort -nr | head -1 | cut -d' ' -f2- || true)
    echo -e "$URL\tfailed_or_timeout\t$LATEST" >> "$CSV"
    echo "RESULT: failed_or_timeout latest=$LATEST" | tee -a "$LOG"
  fi
done
echo "" | tee -a "$LOG"
echo "Finished: $(date -Iseconds)" | tee -a "$LOG"
echo "OK=$OK FAIL=$FAIL" | tee -a "$LOG"
echo "folders=$CSV" | tee -a "$LOG"
echo "$LOG"
