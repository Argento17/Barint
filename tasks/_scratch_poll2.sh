#!/usr/bin/env bash
needle="מבוססים על נתונים חלקיים"   # page-level partial-data banner (forcePartialDisclosure)
url="https://bari.digital/hashvaot/magnesium"
for i in $(seq 1 20); do
  html=$(curl -fsSL --max-time 25 "$url?cb2=$i" 2>/dev/null)
  if echo "$html" | grep -q "$needle"; then
    echo "LIVE: partial-data banner present on attempt $i (~$((i*30))s) — table-polish deploy landed"
    exit 0
  fi
  sleep 30
done
echo "TIMEOUT: banner not detected after ~10min — check Vercel build"
exit 1
