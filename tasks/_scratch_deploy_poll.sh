#!/usr/bin/env bash
needle1="וגם המטעה ביותר"      # new Nutricare-oxide insightLine
needle2="המינון היומי"          # new Full-Mag fixed line
url="https://bari.digital/hashvaot/magnesium"
for i in $(seq 1 20); do
  html=$(curl -fsSL --max-time 25 "$url?cb=$i" 2>/dev/null)
  if echo "$html" | grep -q "$needle1" && echo "$html" | grep -q "$needle2"; then
    echo "LIVE: new magnesium copy detected on attempt $i (~$((i*30))s)"
    exit 0
  fi
  sleep 30
done
echo "TIMEOUT: new copy not detected after ~10min — check Vercel build"
exit 1
