#!/usr/bin/env python3
"""
TASK-129D — Hummus confidence-label hardening (P0 #1 from confidence_reaudit_launch_v1.md).

PROBLEM (re-audit §3 P0 #1): the Launch-Definition §5 `verified` gate is
presence-based — `verified` iff (>=3/6 nutrition fields present AND ingredients
present). It does NOT validate that the ingredients field is a real ingredient
list, so an OCR'd nutrition-panel dump or a bare allergen line can pass as
`verified`.

THIS FIX: a deterministic ingredient-quality detector run as the FINAL pass over
the displayed corpus. Any row currently `verified` whose ingredients field is NOT
a real ingredient list is downgraded `verified -> partial`.

HARD CONSTRAINTS (TASK-129D):
  - NO score / grade changes. run_hummus_002 stays frozen. Asserted below.
  - Confidence LABELS only. positiveSignals / limitingFactors / nutrition / order
    are untouched.
  - Idempotent: re-running on its own output is a no-op.

BUILD ORDER: run AFTER build_hummus_explanation_v1.py (which regenerates v3 and
copies `confidence` verbatim from v2). This script is the authoritative final
confidence pass for the hummus corpus; it must run last.

Operates on (writes both):
  - workspace : ./hummus_frontend_v3.json
  - deployed  : C:\\bari\\bari-web\\src\\data\\comparisons\\hummus_frontend_v3.json
"""
import json, os, io, sys, copy, collections, datetime

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")

HERE    = os.path.dirname(os.path.abspath(__file__))
OUT_WS  = os.path.join(HERE, "hummus_frontend_v3.json")
OUT_WEB = r"C:\bari\bari-web\src\data\comparisons\hummus_frontend_v3.json"

# ── Deterministic ingredient-quality detector ────────────────────────────────
# A real Hebrew food-label ingredient list carries at least one of: a named
# additive class, structured comma-separated tokens, parenthetical sub-ingredients,
# or ingredient percentages. A row FAILS quality (-> not a real list) when it shows
# none of those, or when it is a nutrition-panel dump masquerading as ingredients.
ADDITIVE_TERMS = [
    "חומר משמר", "מווסת חומציות", "מייצב", "מתחלב", "חומצת", "נתרן בנזואט",
    "גואר", "קסנטן", "עמילן", "צבע מאכל", "מתחמצן", "סודיום ביקרבונט",
]
NUTRITION_PANEL_TERMS = [
    "ערכים תזונתיים", "אנרגיה", "מתוך פחמימות", "מתוכם שומן רווי", "סיבים תזונתיים",
]


def is_real_ingredient_list(ingredients):
    """True iff the text reads as a genuine ingredient list (deterministic)."""
    if not ingredients:
        return False
    t = " ".join(ingredients.split())
    has_additive = any(term in t for term in ADDITIVE_TERMS)
    # Nutrition-panel dump (>=2 panel markers and no additive vocabulary) is not a list.
    panel_hits = sum(1 for k in NUTRITION_PANEL_TERMS if k in t)
    if panel_hits >= 2 and not has_additive:
        return False
    structured = (
        t.count(",") >= 3
        or ("%" in t and t.count(",") >= 1)
        or ("(" in t and t.count(",") >= 2)
    )
    return has_additive or structured


def harden(doc):
    """Downgrade verified rows that fail the ingredient-quality gate. Returns
    (relabeled_records). Mutates doc in place. No score/grade/content changes."""
    relabeled = []
    for p in doc["products"]:
        if p.get("confidence") != "verified":
            continue
        ing = (p.get("expansion") or {}).get("ingredients")
        if not is_real_ingredient_list(ing):
            relabeled.append((p["id"], p.get("name"), p.get("score"), p.get("grade")))
            p["confidence"] = "partial"
    # refresh file-level distribution
    dist = collections.Counter(p["confidence"] for p in doc["products"])
    doc["_meta"]["confidence_distribution"] = dict(dist)
    doc["_meta"]["confidence_hardening"] = {
        "task": "TASK-129D",
        "rule": "verified requires a real ingredient list (additive-class / structured / "
                "percentage markers); nutrition-panel dumps and bare allergen lines fail",
        "applied": datetime.datetime.now(datetime.timezone.utc).isoformat(),
        "relabeled_verified_to_partial": [r[0] for r in relabeled],
        "score_changes": 0,
        "source_audit": "confidence_reaudit_launch_v1.md §3 P0 #1",
    }
    return relabeled


def main():
    src = OUT_WEB if os.path.exists(OUT_WEB) else OUT_WS
    doc = json.load(open(src, encoding="utf-8"))

    before_dist = collections.Counter(p["confidence"] for p in doc["products"])
    before_scores = {p["id"]: (p.get("score"), p.get("grade")) for p in doc["products"]}

    relabeled = harden(doc)

    # HARD GUARANTEE: zero score / grade movement.
    after_scores = {p["id"]: (p.get("score"), p.get("grade")) for p in doc["products"]}
    assert before_scores == after_scores, "SCORE/GRADE MOVED — aborting (constraint violation)"

    after_dist = collections.Counter(p["confidence"] for p in doc["products"])

    for path in (OUT_WS, OUT_WEB):
        with open(path, "w", encoding="utf-8") as f:
            json.dump(doc, f, ensure_ascii=False, indent=2)

    print("TASK-129D — hummus confidence hardening")
    print("  before:", dict(before_dist))
    print("  after :", dict(after_dist))
    print(f"  relabeled verified -> partial: {len(relabeled)}")
    for pid, name, score, grade in relabeled:
        print(f"    [{pid}] {name} | {score}/{grade}")
    print("  score/grade changes: 0 (asserted)")


if __name__ == "__main__":
    main()
