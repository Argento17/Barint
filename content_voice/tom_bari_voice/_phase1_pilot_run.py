"""Phase 1 pilot: run the Layer-1 naturalness pre-filter across the live
protein-bars consumer copy, write a UTF-8 report (console can't print Hebrew)."""
import json, io, sys
sys.path.insert(0, "C:/Bari")
from integrations.clients.naturalness_gate import analyze

import sys as _sys
SRC = _sys.argv[1] if len(_sys.argv) > 1 else "bari-web/src/data/comparisons/protein_bars_frontend_v1.json"
CONSUMER_KEYS = {
    "insightLine", "rowVerdict", "comparisonContext", "hero", "heroTitle",
    "prologue", "prologueText", "title", "subtitle", "takeaway", "verdict",
    "whatMatters", "categoryNote", "note", "summary", "text", "body",
    "headline", "tagline", "description",
}

def is_hebrew(s):
    return isinstance(s, str) and any("֐" <= c <= "ת" for c in s) and len(s) > 12

rows = []  # (path, key, text)
def walk(o, p=""):
    if isinstance(o, dict):
        for k, v in o.items():
            if k in CONSUMER_KEYS and is_hebrew(v):
                rows.append((p + "/" + k, k, v))
            walk(v, p + "/" + k)
    elif isinstance(o, list):
        for i, v in enumerate(o):
            walk(v, p + f"[{i}]")

d = json.load(open(SRC, encoding="utf-8"))
walk(d)

out = io.StringIO()
out.write(f"# Phase 1 pilot — Layer-1 naturalness pre-filter on {SRC}\n\n")
out.write(f"Consumer Hebrew strings scanned: {len(rows)}\n\n")
high = med = clean = 0
for path, key, text in rows:
    r = analyze(text)
    hi = [f for f in r.flags if f.severity == "HIGH"]
    me = [f for f in r.flags if f.severity == "MEDIUM"]
    if hi: high += 1
    elif me: med += 1
    else: clean += 1
    status = "HIGH-BLOCK" if hi else ("medium" if me else "clean")
    out.write(f"## [{status}] {path}\n")
    out.write(f"> {text}\n\n")
    for f in r.flags:
        out.write(f"  - {f.severity} {f.tell}: «{f.match}» — {f.note}\n")
    fs = r.f2_signal
    out.write(f"  - F2-signal: hedges={fs['hedge_count']} verdict_marker={fs['has_verdict_marker']} risk={fs['f2_risk']}\n\n")

out.write("---\n")
out.write(f"SUMMARY: {high} HIGH-block · {med} medium-only · {clean} clean "
          f"(of {len(rows)} strings)\n")

import os as _os
_rep = "content_voice/tom_bari_voice/_phase1_pilot_report" + (
    "" if "v1" in _os.path.basename(SRC) else "_" + _os.path.basename(SRC).replace(".json", "")) + ".md"
open(_rep, "w", encoding="utf-8").write(out.getvalue())
print(f"done: {len(rows)} strings, {high} HIGH, {med} medium, {clean} clean")
