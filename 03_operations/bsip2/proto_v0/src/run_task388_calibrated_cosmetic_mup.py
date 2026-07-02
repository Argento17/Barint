#!/usr/bin/env python3
"""
TASK-388 — Calibrated Cosmetic-MUP Impact Measurement (EXPLORE; no score change).

Measures the grade-move delta of adding a CALIBRATED, tier-graded cosmetic-MUP
penalty ON TOP of the current published baseline (which already includes
BARI_D4_SCORE_V1 contested-only scoring — 102/483 penalized, 6 grade moves).

Design under test (tier-graded cosmetic-MUP):
  - functional tier additives (xanthan/guar/locust-bean, lecithin, natural
    colorants): ZERO weight. They are cosmetic_mup but have no concern basis.
  - likely-neutral tier additives (SSL/DATEM/PGPR/modified starch): ZERO weight.
    These are industrial-UPF markers but the broad cosmetic_mup rejection ruling
    (owner 2026-06-21) was specifically about them.
  - dose-dependent sweeteners (E955/E950/E960): ZERO weight — already handled by
    SWEETENER_CAP tiers.
  - disclosure-gap (E150/caramel color): ZERO weight — ambiguous type, no penalty.
  - unclassified (E141): ZERO weight.
  - dose-dependent PHOSPHATE (E450/E451/E452, key: "E450" in library):
      weight = 1 point per binary detection (not additive per form). THIS IS
      the ONLY new signal under the calibrated design.
  - contested score_eligible: weight = 2 (UNCHANGED — already live in published
      scores; included here only to confirm no new stacking introduced).

Key constraint (anti-double-count):
  The PUBLISHED baseline already has D4 contested deducted. So we are measuring
  ONLY the INCREMENTAL impact of adding phosphate weight=1 on top.

Usage:
  cd 03_operations/bsip2/proto_v0/src
  python run_task388_calibrated_cosmetic_mup.py

Exit: 0 = all checks pass; 1 = a check failed.
"""
from __future__ import annotations

import json
import os
import re
import sys
import statistics
from collections import Counter, defaultdict
from pathlib import Path

REPO = Path(__file__).resolve().parents[4]   # C:\Bari
SRC  = Path(__file__).resolve().parent

os.chdir(SRC)
sys.path.insert(0, str(SRC))

# Force UTF-8 output
sys.stdout.reconfigure(encoding="utf-8", errors="replace")

# ─────────────────────────────────────────────────────────────────────────────
# Import constants (flag state irrelevant — we compute penalties manually here)
# ─────────────────────────────────────────────────────────────────────────────
from constants import (
    GLASSBOX_W2_ADDITIVES,
    D4_SCORE_CAP,
    D4_COMBINED_ADDITIVE_PROCESSING_CAP,
    D4_SCORE_CONTESTED_WEIGHT,
)

LIVE_MANIFEST = REPO / "03_operations" / "spine" / "live_manifest.json"

# ── BSIP1 corpus source map (same as run_task371_d4_score.py) ────────────────
BSIP1_SOURCES: dict[str, list[tuple[str, str]]] = {
    "brined_cheeses":    [("03_operations/bsip1/run_brined_cheeses_002/output", "bsip1_brinedcheese_*.json")],
    "cakes":             [("03_operations/bsip1/run_cakes_001/output", "bsip1_cakes_*.json")],
    "breakfast-cereals": [("03_operations/bsip1/run_cereals_008/output", "*.json")],
    "cheese-spreads":    [("03_operations/bsip1/run_cheese_003/output", "*.json")],
    "cookies_coffee":    [
        ("03_operations/bsip1/run_cookies_001/output", "*.json"),
        ("03_operations/bsip1/run_cakes_001/output",   "*.json"),
    ],
    "granola":           [("03_operations/bsip1/run_cereals_005/output", "*.json")],
    "hard_cheeses":      [("02_products/hard_cheeses/bsip1_outputs",     "*.json")],
    "hummus":            [("02_products/hummus/canonical_bsip1",          "*.json")],
    "juices":            [("02_products/juices/bsip1_outputs",            "*.json")],
    "milk":              [("03_operations/bsip1/run_milk_002/output",     "*.json")],
    "snacks":            [("03_operations/bsip1/run_001/output",          "*.json")],
    "bread":             [("03_operations/bsip1/run_bread_conform_001/output", "*.json")],
}

# ─────────────────────────────────────────────────────────────────────────────
# Grade boundary (matches score_engine.py _grade())
# ─────────────────────────────────────────────────────────────────────────────
def _grade(score) -> str:
    if score is None:
        return "?"
    s = float(score)
    if s >= 90: return "S"
    if s >= 80: return "A"
    if s >= 65: return "B"
    if s >= 50: return "C"
    if s >= 35: return "D"
    return "E"


# ─────────────────────────────────────────────────────────────────────────────
# CALIBRATED penalty (EXPLORE design — tier-graded cosmetic-MUP)
# This function intentionally does NOT use compute_d4_score_penalty() so we
# can measure the INCREMENTAL phosphate component only, separate from the
# contested component already embedded in published scores.
# ─────────────────────────────────────────────────────────────────────────────

# Phosphate match patterns from GLASSBOX_W2_ADDITIVES["E450"]["match_patterns_he"]
_PHOSPHATE_PATTERNS = list(GLASSBOX_W2_ADDITIVES.get("E450", {}).get("match_patterns_he", []))
_PHOSPHATE_RE = re.compile(
    "|".join(re.escape(p) for p in _PHOSPHATE_PATTERNS),
    re.IGNORECASE | re.UNICODE,
)

# Score-eligible contested set (same as BARI_D4_SCORE_V1 baseline — for reference only)
_CONTESTED_ELIGIBLE = sorted([
    k for k, v in GLASSBOX_W2_ADDITIVES.items()
    if v.get("tier") == "contested" and v.get("score_eligible", False)
])

# Functional + likely-neutral cosmetic_mup additives that must score 0
# (the 2026-06-21 rejection cases)
_ZERO_WEIGHT_COSMETIC_MUP = {
    k: v for k, v in GLASSBOX_W2_ADDITIVES.items()
    if v.get("cosmetic_mup") and v.get("tier") in ("functional", "likely-neutral")
}

# Weight constants for calibrated design
PHOSPHATE_MUP_WEIGHT = 1    # NEW: binary detection; weight per product (not per E-form)
CONTESTED_WEIGHT = 2        # UNCHANGED (already live — included for cap accounting only)
COSMETIC_BROAD_WEIGHT = 0   # UNCHANGED (0 — rejected 2026-06-21)

def _detect_phosphate(text: str) -> bool:
    """Returns True if any phosphate form (E450/E451/E452) is detected in ingredient text."""
    if not text:
        return False
    return bool(_PHOSPHATE_RE.search(text))


def _compute_incremental_phosphate_penalty(
    ingredient_text: str,
    ecs_spent: int = 0,
    already_contested_penalty: int = 0,
) -> tuple[int, str]:
    """
    Computes ONLY the incremental phosphate MUP penalty — what is ADDED on top
    of the contested penalty already embedded in published scores.

    The combined cap (12) must account for:
      - already_contested_penalty: D4 contested already in published score
      - ecs_spent: ECS-v1 budget (stub=0 here, conservative upper bound)
      - new phosphate penalty

    Returns (incremental_penalty, trace_note).
    """
    if not ingredient_text:
        return 0, "PHOSPHATE_MUP: no ingredient text"

    phosphate_detected = _detect_phosphate(ingredient_text)
    if not phosphate_detected:
        return 0, "PHOSPHATE_MUP: not detected"

    phosphate_raw = PHOSPHATE_MUP_WEIGHT  # = 1 (binary)

    # Combined cap: ECS + already_contested_penalty + new_phosphate must not exceed 12
    # (In the standalone runner ECS=0 and already_contested is also 0 since we're
    #  measuring incremental only on top of published scores — conservative.)
    total_already_spent = ecs_spent + already_contested_penalty
    remaining_budget = max(0, D4_COMBINED_ADDITIVE_PROCESSING_CAP - total_already_spent)
    incremental = max(0, min(phosphate_raw, remaining_budget))

    note = (
        f"PHOSPHATE_MUP: detected=True weight=1 "
        f"ecs_spent={ecs_spent} already_contested={already_contested_penalty} "
        f"remaining_budget={remaining_budget} incremental={incremental}"
    )
    return incremental, note


# ─────────────────────────────────────────────────────────────────────────────
# Load corpus
# ─────────────────────────────────────────────────────────────────────────────
def _build_barcode_index() -> dict[str, str]:
    index: dict[str, str] = {}
    for _cat, sources in BSIP1_SOURCES.items():
        for rel_dir, glob in sources:
            d = REPO / rel_dir
            if not d.exists():
                continue
            for f in d.glob(glob):
                try:
                    prod = json.loads(f.read_text(encoding="utf-8"))
                    bc = str(prod.get("barcode", "") or "").strip()
                    ing = (prod.get("ingredients_text_he")
                           or prod.get("ingredients_raw")
                           or "")
                    if bc and ing and len(ing) > 3 and bc not in index:
                        index[bc] = ing
                except Exception:
                    pass
    return index


def _load_live_products() -> list[dict]:
    manifest = json.loads(LIVE_MANIFEST.read_text(encoding="utf-8"))
    files = manifest.get("files", [])
    seen_cats: dict[str, dict] = {}
    for f in files:
        cat = f["category"]
        path = Path(f["path"])
        if path.exists():
            seen_cats[cat] = {"path": path, "category": cat}
    all_products: list[dict] = []
    for cat in sorted(seen_cats.keys()):
        info = seen_cats[cat]
        data = json.loads(info["path"].read_text(encoding="utf-8"))
        prods = data.get("products", data if isinstance(data, list) else [])
        for p in prods:
            if not isinstance(p, dict):
                continue
            bc = str(p.get("barcode") or p.get("id") or "").strip()
            score = p.get("score") or p.get("bariScore")
            grade = p.get("grade") or p.get("bariGrade")
            name  = (p.get("name") or p.get("productName") or bc or "?")
            all_products.append({
                "barcode":   bc,
                "name":      name,
                "category":  cat,
                "score_off": score,   # published baseline (includes D4 contested if it fired)
                "grade_off": grade or (_grade(score) if score is not None else "?"),
            })
    return all_products


# ─────────────────────────────────────────────────────────────────────────────
# Main
# ─────────────────────────────────────────────────────────────────────────────
def main() -> int:
    print("=" * 72)
    print("TASK-388: Calibrated Cosmetic-MUP Impact (phosphate only, weight=1)")
    print("EXPLORE phase — NO published score changed, NO flag flipped")
    print("=" * 72)

    # ── Design summary ────────────────────────────────────────────────────────
    print("\n[DESIGN UNDER TEST]")
    print("  Tier-graded cosmetic-MUP penalty:")
    print("    functional cosmetic_mup (xanthan, guar, lecithin, natural colorants): weight=0")
    print("    likely-neutral cosmetic_mup (SSL, DATEM, PGPR, modified starch):     weight=0")
    print("    dose-dependent sweeteners (E955/E950/E960):                           weight=0 (SWEETENER_CAP)")
    print("    disclosure-gap (E150, caramel color):                                 weight=0")
    print("    unclassified (E141):                                                  weight=0")
    print("    dose-dependent PHOSPHATE (E450/E451/E452, binary):                   weight=1 [NEW]")
    print("    contested score_eligible (already in published scores):               weight=2 [UNCHANGED]")
    print()

    # ── Zero-weight clean-product roster ─────────────────────────────────────
    print("[CLEAN-PRODUCT PROTECTION — zero weight under calibrated design]")
    for e_num, entry in sorted(_ZERO_WEIGHT_COSMETIC_MUP.items()):
        print(f"  {e_num:6s} [{entry['tier']:15s}] cosmetic_mup=True  {entry['name_en']}")
    print()

    # ── Score-eligible contested set (for reference) ──────────────────────────
    print(f"[CONTESTED ELIGIBLE (already in published scores, weight=2): {len(_CONTESTED_ELIGIBLE)}]")
    print(f"  {_CONTESTED_ELIGIBLE}")
    print()

    # ── Build barcode index ───────────────────────────────────────────────────
    print("Building barcode -> ingredients index from BSIP1 corpus...")
    bc_index = _build_barcode_index()
    print(f"  Indexed barcodes with ingredient text: {len(bc_index)}")

    # ── Load products ─────────────────────────────────────────────────────────
    print("\nLoading live frontend products (BARI_D4_SCORE_V1 published baseline)...")
    products = _load_live_products()
    total = len(products)
    print(f"  Total products: {total}")

    matched = 0
    for p in products:
        ing = bc_index.get(p["barcode"], "")
        p["ingredients"] = ing
        if ing:
            matched += 1
    print(f"  Matched to ingredient text: {matched}/{total}")
    print(f"  No ingredient text (penalty=0): {total - matched}/{total}")

    # ─────────────────────────────────────────────────────────────────────────
    # Compute incremental phosphate penalty per product
    # ─────────────────────────────────────────────────────────────────────────
    print("\n" + "-" * 72)
    print("Computing incremental phosphate MUP penalty per product")
    print("-" * 72)

    phosphate_movers: list[dict] = []
    phosphate_grade_changers: list[dict] = []
    phosphate_detected_products: list[dict] = []

    for p in products:
        if not p["ingredients"] or p["score_off"] is None:
            p["phosphate_penalty"] = 0
            p["phosphate_note"]    = "no ingredients or no score"
            p["score_v2"] = p["score_off"]
            p["grade_v2"] = p["grade_off"]
            continue

        penalty, note = _compute_incremental_phosphate_penalty(
            p["ingredients"],
            ecs_spent=0,                     # conservative: ECS stub=0
            already_contested_penalty=0,     # published score already includes contested;
                                             # measuring INCREMENTAL only
        )

        p["phosphate_penalty"] = penalty
        p["phosphate_note"]    = note

        if penalty > 0:
            phosphate_detected_products.append(p)
            score_v2 = round(max(0.0, float(p["score_off"]) - penalty), 1)
            grade_v2 = _grade(score_v2)
        else:
            score_v2 = p["score_off"]
            grade_v2 = p["grade_off"]

        p["score_v2"] = score_v2
        p["grade_v2"] = grade_v2

        if penalty > 0:
            phosphate_movers.append(p)
            if p["grade_off"] != grade_v2:
                phosphate_grade_changers.append(p)

    print(f"\n  Products with phosphate detected (incremental penalty=1): {len(phosphate_detected_products)}/{total}")
    print(f"  Grade changes from incremental phosphate (+1 on top of baseline):    {len(phosphate_grade_changers)}")

    # ─────────────────────────────────────────────────────────────────────────
    # By-category distributions
    # ─────────────────────────────────────────────────────────────────────────
    print("\n" + "-" * 72)
    print("Before/After grade distributions by category")
    print("  (baseline = published BARI_D4_SCORE_V1 scores; ON = +phosphate weight=1)")
    print("-" * 72)

    cat_off:  defaultdict[str, list] = defaultdict(list)
    cat_on:   defaultdict[str, list] = defaultdict(list)
    s_off:    defaultdict[str, list] = defaultdict(list)
    s_on:     defaultdict[str, list] = defaultdict(list)

    for p in products:
        c = p["category"]
        cat_off[c].append(p["grade_off"])
        cat_on[c].append(p["grade_v2"])
        if p["score_off"] is not None:
            s_off[c].append(float(p["score_off"]))
        if p["score_v2"] is not None:
            s_on[c].append(float(p["score_v2"]))

    for cat in sorted(cat_off.keys()):
        n    = len(cat_off[cat])
        off_c = dict(sorted(Counter(cat_off[cat]).items()))
        on_c  = dict(sorted(Counter(cat_on[cat]).items()))
        chgs = sum(1 for a, b in zip(cat_off[cat], cat_on[cat]) if a != b)
        m_off = f"{statistics.mean(s_off[cat]):.1f}" if s_off[cat] else "N/A"
        m_on  = f"{statistics.mean(s_on[cat]):.1f}"  if s_on[cat]  else "N/A"
        chg_mark = f"  *** {chgs} grade change(s) ***" if chgs else ""
        print(f"\n  {cat} (n={n}):{chg_mark}")
        print(f"    BASELINE: {off_c}  mean={m_off}")
        print(f"    +PHOSPH:  {on_c}   mean={m_on}")

    # ─────────────────────────────────────────────────────────────────────────
    # Grade-change detail table
    # ─────────────────────────────────────────────────────────────────────────
    print("\n" + "-" * 72)
    print(f"Grade-change detail ({len(phosphate_grade_changers)} products)")
    print("-" * 72)

    if not phosphate_grade_changers:
        print("  No grade changes from incremental phosphate penalty.")
    else:
        hdr = f"  {'Barcode':16s} {'Name':30s} {'Cat':22s} {'Pen':>4} {'ScBSL':>6} {'GrBSL':>6} {'ScV2':>6} {'GrV2':>5}"
        print(hdr)
        print("  " + "-" * 100)
        for p in sorted(phosphate_grade_changers, key=lambda x: (x["category"], -(x["phosphate_penalty"]))):
            print(
                f"  {p['barcode']:16s}"
                f" {str(p['name'])[:28]:30s}"
                f" {p['category']:22s}"
                f" {p['phosphate_penalty']:>4}"
                f" {str(p['score_off']):>6}"
                f" {p['grade_off']:>6}"
                f" {str(p['score_v2']):>6}"
                f" {p['grade_v2']:>5}"
            )

    # ─────────────────────────────────────────────────────────────────────────
    # All phosphate detections (penalty=1 products)
    # ─────────────────────────────────────────────────────────────────────────
    print("\n" + "-" * 72)
    print(f"All phosphate-detected products (penalty=1) — {len(phosphate_movers)} products")
    print("-" * 72)

    for p in sorted(phosphate_movers, key=lambda x: (x["category"], x["name"])):
        gc = " *** GRADE CHANGE ***" if p["grade_off"] != p["grade_v2"] else ""
        print(
            f"  [{p['category']:20s}]"
            f"  {str(p['score_off']):>6} {p['grade_off']} ->"
            f"  {str(p['score_v2']):>6} {p['grade_v2']}"
            f"  bc={p['barcode']}{gc}"
        )

    # ─────────────────────────────────────────────────────────────────────────
    # CLEAN-PRODUCT TEST — 2026-06-21 failure cases
    # Must show ZERO penalty under calibrated design
    # ─────────────────────────────────────────────────────────────────────────
    print("\n" + "-" * 72)
    print("CLEAN-PRODUCT TEST (2026-06-21 failure cases under broad design)")
    print("  These must score 0 under the calibrated tier-graded design")
    print("-" * 72)

    # Identify clean products by ingredient-text pattern
    # We search for the failure cases: xanthan gum (E415) and SSL (E481)
    _XANTHAN_RE  = re.compile(r"קסנטן|קסנטאן|קסנתן", re.IGNORECASE | re.UNICODE)
    _SSL_RE      = re.compile(r"נתרן סטארויל לקטילט|SSL|נתרן סטיארויל", re.IGNORECASE | re.UNICODE)
    _LECITHIN_RE = re.compile(r"לציטין", re.IGNORECASE | re.UNICODE)
    _PECTIN_RE   = re.compile(r"פקטין", re.IGNORECASE | re.UNICODE)
    _BETACAR_RE  = re.compile(r"בטא.?קרוטן|ביתא.?קרוטן", re.IGNORECASE | re.UNICODE)
    _GUAR_RE     = re.compile(r"גואר", re.IGNORECASE | re.UNICODE)
    _LBG_RE      = re.compile(r"לוקוסט.בין גאם|קרוב.בין גאם", re.IGNORECASE | re.UNICODE)

    clean_patterns = [
        ("xanthan (E415, functional)", _XANTHAN_RE),
        ("SSL (E481, likely-neutral)", _SSL_RE),
        ("lecithin (E322, functional)", _LECITHIN_RE),
        ("pectin (E440, functional)", _PECTIN_RE),
        ("beta-carotene (E160a, functional)", _BETACAR_RE),
        ("guar gum (E412, functional)", _GUAR_RE),
        ("locust bean gum (E410, functional)", _LBG_RE),
    ]

    total_clean_hits = 0
    for label, pat in clean_patterns:
        matches = [p for p in products if p.get("ingredients") and pat.search(p["ingredients"])]
        penalized = [p for p in matches if p["phosphate_penalty"] > 0]
        n_match = len(matches)
        n_pen = len(penalized)
        status = "PASS (zero penalty)" if n_pen == 0 else f"FAIL ({n_pen} penalized)"
        print(f"  {label:45s} n={n_match:3d}  penalty>0={n_pen:3d}  [{status}]")
        if n_pen > 0:
            total_clean_hits += n_pen
            for p in penalized:
                print(f"    !! PENALIZED: {p['barcode']} {p['name'][:30]} [{p['category']}]")

    if total_clean_hits == 0:
        print("\n  CLEAN-PRODUCT TEST: PASS — zero penalty on all 7 functional/likely-neutral categories")
    else:
        print(f"\n  CLEAN-PRODUCT TEST: FAIL — {total_clean_hits} clean products incorrectly penalized")

    # ─────────────────────────────────────────────────────────────────────────
    # Aggregate statistics
    # ─────────────────────────────────────────────────────────────────────────
    print("\n" + "-" * 72)
    print("Aggregate statistics")
    print("-" * 72)

    all_off = dict(sorted(Counter(p["grade_off"] for p in products).items()))
    all_on  = dict(sorted(Counter(p["grade_v2"]  for p in products).items()))
    print(f"  BASELINE grade distribution (BARI_D4_SCORE_V1):  {all_off}")
    print(f"  V2 grade distribution (+phosphate weight=1):      {all_on}")
    print(f"  Total products: {total}")
    print(f"  Matched with ingredient text: {matched}")
    print(f"  Products with phosphate detected: {len(phosphate_movers)}")
    print(f"  Products with grade change: {len(phosphate_grade_changers)}")
    print(f"  Phosphate detection rate: {len(phosphate_movers)/total*100:.1f}% of scored corpus")

    # Per-category phosphate detection
    cat_phosphate: defaultdict[str, int] = defaultdict(int)
    cat_total: defaultdict[str, int] = defaultdict(int)
    for p in products:
        cat_total[p["category"]] += 1
        if p["phosphate_penalty"] > 0:
            cat_phosphate[p["category"]] += 1
    print("\n  Phosphate detection by category:")
    for cat in sorted(cat_total.keys()):
        n_p = cat_phosphate[cat]
        n_t = cat_total[cat]
        if n_p > 0:
            print(f"    {cat:30s}  {n_p}/{n_t} ({n_p/n_t*100:.0f}%)")
        else:
            print(f"    {cat:30s}  0/{n_t} (0%)   [not affected]")

    # ─────────────────────────────────────────────────────────────────────────
    # Integrity checks
    # ─────────────────────────────────────────────────────────────────────────
    print("\n" + "-" * 72)
    print("Integrity checks")
    print("-" * 72)

    fails: list[str] = []

    # Check: no penalty exceeds weight=1 (binary)
    over_weight = [p for p in products if p["phosphate_penalty"] > 1]
    if over_weight:
        fails.append(f"WEIGHT VIOLATION: {len(over_weight)} products with phosphate_penalty > 1")
    else:
        print("  WEIGHT CHECK PASS: no phosphate_penalty > 1 (binary detection confirmed)")

    # Check: no score increase
    upward = [p for p in products
              if p["score_off"] is not None and p["score_v2"] is not None
              and float(p["score_v2"]) > float(p["score_off"])]
    if upward:
        fails.append(f"MONOTONE VIOLATION: {len(upward)} products with score increase")
    else:
        print("  MONOTONE CHECK PASS: no product received a score increase")

    # Check: clean-product test
    if total_clean_hits > 0:
        fails.append(f"CLEAN-PRODUCT TEST FAIL: {total_clean_hits} functional/likely-neutral MUP products penalized")
    else:
        print("  CLEAN-PRODUCT TEST PASS: functional + likely-neutral cosmetic_mup = zero penalty")

    # Check: combined cap not exceeded
    cap_viol = [p for p in products if p["phosphate_penalty"] > D4_COMBINED_ADDITIVE_PROCESSING_CAP]
    if cap_viol:
        fails.append(f"COMBINED CAP VIOLATION: {len(cap_viol)} products exceed {D4_COMBINED_ADDITIVE_PROCESSING_CAP}")
    else:
        print(f"  COMBINED CAP PASS: no product exceeds D4_COMBINED_ADDITIVE_PROCESSING_CAP={D4_COMBINED_ADDITIVE_PROCESSING_CAP}")

    if fails:
        for msg in fails:
            print(f"  FAIL: {msg}")

    # ─────────────────────────────────────────────────────────────────────────
    # BROAD vs CALIBRATED comparison
    # (Count how many products would be hit by the broad design for comparison)
    # ─────────────────────────────────────────────────────────────────────────
    print("\n" + "-" * 72)
    print("BROAD vs CALIBRATED design comparison")
    print("-" * 72)

    # Under the broad design (weight=1 for ALL cosmetic_mup=True), how many would fire?
    all_cosmetic_mup_patterns = []
    for e_num, entry in GLASSBOX_W2_ADDITIVES.items():
        if entry.get("cosmetic_mup"):
            all_cosmetic_mup_patterns.extend(entry.get("match_patterns_he", []))

    _BROAD_MUP_RE = re.compile(
        "|".join(re.escape(p) for p in set(all_cosmetic_mup_patterns)),
        re.IGNORECASE | re.UNICODE,
    )

    broad_hit_count = 0
    for p in products:
        if p.get("ingredients") and _BROAD_MUP_RE.search(p["ingredients"]):
            broad_hit_count += 1

    print(f"  Broad cosmetic_mup design (ALL cosmetic_mup=True, weight=1): ~{broad_hit_count}/{total} products hit")
    print(f"  Calibrated design (phosphate only, weight=1):                  {len(phosphate_movers)}/{total} products hit")
    print(f"  Reduction factor: {broad_hit_count - len(phosphate_movers)} fewer products penalized")
    print(f"  Percentage of broad hit that is calibrated hit: {len(phosphate_movers)/max(broad_hit_count,1)*100:.1f}%")

    # ─────────────────────────────────────────────────────────────────────────
    # Final result
    # ─────────────────────────────────────────────────────────────────────────
    print("\n" + "=" * 72)
    overall = "PASS" if not fails else "FAIL"
    print(f"TASK-388 EXPLORE RESULT: {overall}")
    print(f"  Total products in corpus:                 {total}")
    print(f"  Matched with ingredient text:             {matched}")
    print(f"  Phosphate detected (new penalty):         {len(phosphate_movers)}")
    print(f"  Grade changes from phosphate weight=1:    {len(phosphate_grade_changers)}")
    print(f"  Integrity check failures:                 {len(fails)}")
    print("=" * 72)
    return 0 if not fails else 1


if __name__ == "__main__":
    sys.exit(main())
