"""
TASK-180B reship: apply run_snackbars_007_headpin scores to snacks_frontend_v2.json
CC-verified mapping by imageUrl barcode extraction.
"""
import json
import re
from pathlib import Path

FRONTEND_JSON = Path(r"C:\Bari\bari-web\src\data\comparisons\snacks_frontend_v2.json")

# Correct mapping: snk_id -> (bsip1_pid, off_json_score, new_rounded_score)
CORRECT_MAP = {
    "snk-001": ("bsip1_7290011498870", 70.0,  70),
    "snk-015": ("bsip1_7290011498894", 63.0,  63),
    "snk-004": ("bsip1_8423207206495", 60.4,  60),
    "snk-002": ("bsip1_7290011498948", 56.7,  57),
    "snk-003": ("bsip1_16000548404",   55.1,  55),
    "snk-016": ("bsip1_8423207210928", 52.5,  53),
    "snk-009": ("bsip1_8410076610379", 47.7,  48),
    "snk-005": ("bsip1_5900020039590", 47.6,  48),
    "snk-010": ("bsip1_8410076610386", 46.2,  46),
    "snk-018": ("bsip1_8410076602251", 45.9,  46),
    "snk-011": ("bsip1_7290111936784", 43.8,  44),
    "snk-012": ("bsip1_7290111937262", 42.0,  42),
    "snk-017": ("bsip1_8410076610508", 40.5,  41),
    "snk-019": ("bsip1_7290118427896", 39.8,  40),
    "snk-020": ("bsip1_7290014525306", 31.8,  32),
    "snk-007": ("bsip1_5900020015174", 26.7,  27),
    "snk-006": ("bsip1_7290118427858", 17.7,  18),
    "snk-013": ("bsip1_4011800633516", 16.3,  16),
}

GRADE_THRESHOLDS = [(80,"A"),(70,"B"),(50,"C"),(35,"D")]

def score_to_grade(s):
    for t, g in GRADE_THRESHOLDS:
        if s >= t:
            return g
    return "E"

data = json.loads(FRONTEND_JSON.read_text(encoding="utf-8"))

changes = []
for p in data["products"]:
    sid = p["id"]
    if sid not in CORRECT_MAP:
        print(f"WARNING: {sid} not in map")
        continue
    _, raw, new_score = CORRECT_MAP[sid]
    old_score = p["score"]
    old_grade = p["grade"]
    new_grade = score_to_grade(new_score)
    if old_score != new_score:
        changes.append(f"  {sid}: {old_score}/{old_grade} -> {new_score}/{new_grade}")
    p["score"] = new_score
    p["grade"] = new_grade

# Re-sort by score descending (stable to preserve tie order)
data["products"].sort(key=lambda p: -p["score"])

# Update meta
data["_meta"]["production_pass"] += (
    " TASK-180B re-baseline pass 2026-06-05: run_snackbars_007_headpin (engine-baseline-2026-06-04, "
    "config d6f0b99fc5c49e0e); 11 cosmetic score updates (all ≤2pt, zero grade changes); "
    "crosswalk corrected by imageUrl-barcode extraction; 69.5/B note voided (product not displayed). "
    "Note: comparisonContext/insightLine quoted scores may be ±2pt stale — Content Agent editorial pass pending."
)

FRONTEND_JSON.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")

print("Score changes applied:")
for c in changes:
    print(c)
print(f"\nTotal changes: {len(changes)}/18")
print("Done — snacks_frontend_v2.json reshippped.")
