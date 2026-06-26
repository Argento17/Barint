# -*- coding: utf-8 -*-
"""
TASK-413 deploy merge: start from LIVE snacks_frontend_v5 (preserves copy, array order,
all display fields, no PENDING), apply ONLY the staged re-score (score+grade).

Copy-preserving rule: only score+grade are overwritten from staged.
PENDING_COPY fields in staged are never written over live values.
No copy rewriting in this script — copy is unchanged from v5.

Drill-down standard (TASK-411): snacks already renders golden standard.
Do NOT add consumerExplanation/bestUseCases/consumerTakeaway/bariInterpretation/bottomLine.
Keep positiveSignals/limitingFactors/rowVerdict only.

Score-movers (both E grade, both CLEAN/_task405_clean, 0 grade moves):
  6009684861000: 26.0 -> 30.0 (delta=+4.0) — copy claim check: CLEAN
    (comparisonContext "יותר" = ingredient-character claim, not score-rank)
  8423207208703: 24.4 -> 24.6 (delta=+0.2) — copy claim check: CLEAN
    (rowVerdict "ראשון" = ingredient position, not score rank)
Both copy-clean: carry as-is.
"""
import json, io, sys

sys.stdout.reconfigure(encoding="utf-8", errors="replace")

LIVE_PATH   = r"C:\Bari\bari-web\src\data\comparisons\snacks_frontend_v5.json"
STAGED_PATH = r"C:\bari_snacks\03_operations\page_generator\outputs\snacks_task413_staged.json"
OUT_PATH    = r"C:\bari_snacks\03_operations\page_generator\outputs\snacks_task413_DEPLOY.json"

with io.open(LIVE_PATH, encoding="utf-8") as f:
    live = json.load(f)
with io.open(STAGED_PATH, encoding="utf-8") as f:
    staged = json.load(f)

staged_map = {p["barcode"]: p for p in staged["products"]}

score_updates = 0
grade_updates = 0
audit = {"score_moved": [], "grade_moved": []}

for p in live["products"]:
    bc = p.get("barcode")
    s = staged_map.get(bc)
    if not s:
        print(f"  WARNING: {bc} not found in staged — keeping live values")
        continue

    # Apply score from staged
    if s.get("score") is not None and s.get("score") != p.get("score"):
        audit["score_moved"].append({"bc": bc, "old": p.get("score"), "new": s["score"]})
        p["score"] = s["score"]
        score_updates += 1

    # Apply grade from staged
    if s.get("grade") and s.get("grade") != p.get("grade"):
        audit["grade_moved"].append({"bc": bc, "old": p.get("grade"), "new": s["grade"]})
        p["grade"] = s["grade"]
        grade_updates += 1

# Update _meta provenance
live.setdefault("_meta", {})
live["_meta"]["task413_rederive"] = {
    "run_id": "task413_rederive",
    "corpus_dir": r"C:\Bari\03_operations\bsip1\score_bars_task362_20260620_143230\output",
    "corpus_n": 51,
    "live_display_n": len(live["products"]),
    "flags": {
        "BARI_FAT_TECH_V1": "on",
        "BARI_D4_SCORE_V1": "on",
        "BARI_SHELF_RELATIVE_V1": "off",
        "BARI_RECAL_P0": "off",
        "BARI_GRAD_SODIUM_V1": "off",
        "BARI_REDLABEL_V1": "off",
    },
    "reproduce_count": "19/21",
    "grade_moves": 0,
    "score_updates_applied": score_updates,
    "grade_updates_applied": grade_updates,
    "score_moved_detail": audit["score_moved"],
    "copy_policy": "copy-preserving: live v5 copy carried unchanged; 2 score-movers copy verified clean",
    "copy_claim_check": {
        "6009684861000": "CLEAN — 'יותר' in comparisonContext is ingredient-character claim, not score-rank",
        "8423207208703": "CLEAN — 'ראשון' in rowVerdict refers to ingredient position, not score rank",
    },
}

with open(OUT_PATH, "w", encoding="utf-8") as f:
    json.dump(live, f, ensure_ascii=False, indent=2)

print(f"score_updates={score_updates} | grade_updates={grade_updates}")
print(f"Grade moves: {audit['grade_moved']}")
print(f"Score moved: {audit['score_moved']}")
print(f"OUT: {OUT_PATH}")
