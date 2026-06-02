#!/usr/bin/env python3
"""
TASK-128C / TASK-129-style — Maadanim confidence blocker audit (displayed-set method).

Purpose: validate whether the maadanim confidence blocker (re-audit claimed ~63
marketing-prose `verified` rows) is REAL or INFLATED by the same heuristic issue
found in Hummus (file-view + substring false positives), per
confidence_reaudit_launch_v1.md §3 P0 #1.

READ-ONLY AUDIT. Does NOT write the corpus. No score / label changes here.

Two detectors are run against the DISPLAYED 90:
  1. ORIGINAL re-audit marketing-prose heuristic (promo tokens) — reproduces the
     count the re-audit reported, to expose any inflation.
  2. CANONICAL ingredient-quality detector (same logic shipped for hummus in
     harden_hummus_confidence_v1.py) — the defensible gate.
"""
import json, os, io, sys, collections

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")

WEB = r"C:\bari\bari-web\src\data\comparisons\maadanim_frontend_v2.json"

# ── Detector 1: ORIGINAL re-audit marketing-prose heuristic ──────────────────
# Per confidence_reaudit_launch_v1.md §3 P0 #1: "long prose, promo tokens such as
# מסייע, האריזה, מיחזור, עשיר בחלבון". Presence of any promo token => flagged.
PROMO_TOKENS = ["מסייע", "האריזה", "מיחזור", "עשיר בחלבון", "עשיר ב"]

def fails_marketing_prose(ing):
    if not ing:
        return False  # null ingredients handled by presence gate, not this heuristic
    t = " ".join(ing.split())
    return any(tok in t for tok in PROMO_TOKENS)

# ── Detector 2: CANONICAL ingredient-quality detector (hummus-shipped) ────────
ADDITIVE_TERMS = [
    "חומר משמר", "מווסת חומציות", "מייצב", "מתחלב", "חומצת", "נתרן בנזואט",
    "גואר", "קסנטן", "עמילן", "צבע מאכל", "מתחמצן", "סודיום ביקרבונט",
]
NUTRITION_PANEL_TERMS = [
    "ערכים תזונתיים", "אנרגיה", "מתוך פחמימות", "מתוכם שומן רווי", "סיבים תזונתיים",
]

def is_real_ingredient_list(ingredients):
    if not ingredients:
        return False
    t = " ".join(ingredients.split())
    has_additive = any(term in t for term in ADDITIVE_TERMS)
    panel_hits = sum(1 for k in NUTRITION_PANEL_TERMS if k in t)
    if panel_hits >= 2 and not has_additive:
        return False
    structured = (
        t.count(",") >= 3
        or ("%" in t and t.count(",") >= 1)
        or ("(" in t and t.count(",") >= 2)
    )
    return has_additive or structured


def main():
    doc = json.load(open(WEB, encoding="utf-8"))
    prods = doc["products"]

    before = collections.Counter(p.get("confidence") for p in prods)

    verified = [p for p in prods if p.get("confidence") == "verified"]

    # Detector 1: marketing-prose heuristic over displayed verified rows
    mp_fail = [p for p in verified if fails_marketing_prose((p.get("expansion") or {}).get("ingredients"))]

    # Detector 2: canonical ingredient-quality gate over displayed verified rows
    iq_fail = [p for p in verified if not is_real_ingredient_list((p.get("expansion") or {}).get("ingredients"))]

    # Breakdown of detector-2 failures by reason
    null_ing, panel_dump, unstructured = [], [], []
    for p in iq_fail:
        ing = (p.get("expansion") or {}).get("ingredients")
        if not ing:
            null_ing.append(p)
            continue
        t = " ".join(ing.split())
        panel_hits = sum(1 for k in NUTRITION_PANEL_TERMS if k in t)
        has_add = any(term in t for term in ADDITIVE_TERMS)
        if panel_hits >= 2 and not has_add:
            panel_dump.append(p)
        else:
            unstructured.append(p)

    print("=" * 72)
    print("MAADANIM CONFIDENCE BLOCKER — DISPLAYED-SET AUDIT")
    print("=" * 72)
    print(f"Displayed products            : {len(prods)}")
    print(f"Confidence distribution       : {dict(before)}")
    print(f"Displayed 'verified' rows      : {len(verified)}")
    print()
    print("DETECTOR 1 — original re-audit marketing-prose heuristic (promo tokens)")
    print(f"  flagged verified rows        : {len(mp_fail)}  (re-audit claimed ~63 over FILE view)")
    print()
    print("DETECTOR 2 — canonical ingredient-quality gate (hummus-shipped)")
    print(f"  FAIL (genuine relabel cand.) : {len(iq_fail)}")
    print(f"    - null/empty ingredients   : {len(null_ing)}")
    print(f"    - nutrition-panel dump      : {len(panel_dump)}")
    print(f"    - unstructured / prose      : {len(unstructured)}")
    print()
    if iq_fail:
        print("GENUINE verified->partial CANDIDATES (canonical gate):")
        for p in iq_fail:
            ing = (p.get("expansion") or {}).get("ingredients")
            print(f"  [{p['id']}] {p['name']} | {p.get('score')}/{p.get('grade')}")
            print(f"      ING: {repr(ing)[:160]}")
    print()
    # what marketing-prose flags but canonical PASSES (i.e. inflation / false positives)
    iq_fail_ids = {p["id"] for p in iq_fail}
    inflated = [p for p in mp_fail if p["id"] not in iq_fail_ids]
    print(f"INFLATION CHECK — flagged by Detector 1 but PASS canonical gate: {len(inflated)}")
    for p in inflated[:20]:
        ing = (p.get("expansion") or {}).get("ingredients")
        # which promo token tripped it
        t = " ".join((ing or "").split())
        trip = [tok for tok in PROMO_TOKENS if tok in t]
        print(f"  [{p['id']}] {p['name']} | tripped: {trip}")
        print(f"      ING: {repr(ing)[:140]}")


if __name__ == "__main__":
    main()
