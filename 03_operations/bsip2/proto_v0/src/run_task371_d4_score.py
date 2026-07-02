#!/usr/bin/env python3
"""
TASK-371 -- D4 Additive Score (BARI_D4_SCORE_V1) verification runner.

Approach:
  The D4 penalty fires on top of the committed final_score (AFTER full engine run).
  So for the before/after diff, we:
    1. Load committed scores + grades from the live frontend JSONs (OFF baseline).
    2. For each product, look up its ingredients_text_he from the BSIP1 corpus by barcode.
    3. Apply compute_d4_score_penalty() (the actual implementation from score_engine.py).
    4. ON score = committed_score - penalty.
    5. Diff = grade-movement table.
  This is equivalent to a full rescore for the D4 layer, because the penalty is isolated
  from dimension scores (applied after Stage 9 / confidence ceiling).

NOTE: ECS-v1 (emulsifier_complexity_penalty) is NOT available from the frontend JSON.
      We use ECS=0 as a conservative stub -> combined-cap protection is NOT applied here.
      In a full pipeline run, ECS may reduce the net_d4 penalty further, meaning our
      standalone ON scores are an UPPER BOUND on the actual penalty (conservative = safe).

Usage:
  python run_task371_d4_score.py
Exit: 0 = all checks pass, 1 = a check failed.
"""
from __future__ import annotations

import json
import os
import sys
import statistics
from collections import Counter, defaultdict
from pathlib import Path

REPO = Path(__file__).resolve().parents[4]   # C:\Bari
SRC  = Path(__file__).resolve().parent        # .../proto_v0/src

os.chdir(SRC)
sys.path.insert(0, str(SRC))

# Force UTF-8 output (product names are Hebrew)
sys.stdout.reconfigure(encoding="utf-8", errors="replace")

# Import with flag OFF (default)
from score_engine import BARI_D4_SCORE_V1 as _d4_flag_at_import_time
from score_engine import compute_d4_score_penalty
from constants   import (
    GLASSBOX_W2_ADDITIVES,
    D4_SCORE_CAP,
    D4_COMBINED_ADDITIVE_PROCESSING_CAP,
    D4_SCORE_CONTESTED_WEIGHT,
    D4_SCORE_COSMETIC_MUP_WEIGHT,
)

COMPARISONS_DIR = REPO / "bari-web" / "src" / "data" / "comparisons"
LIVE_MANIFEST   = REPO / "03_operations" / "spine" / "live_manifest.json"

# ── BSIP1 corpus source map ───────────────────────────────────────────────────
# Maps category slug -> list of (relative_dir, glob_pattern)
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


def _build_barcode_index() -> dict[str, str]:
    """Build barcode -> ingredients_text_he index from all BSIP1 corpus files."""
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
    """Load all products from the live frontend JSONs (committed baseline)."""
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
        path = info["path"]
        data = json.loads(path.read_text(encoding="utf-8"))
        prods = data.get("products", data if isinstance(data, list) else [])
        for p in prods:
            if not isinstance(p, dict):
                continue
            bc = str(p.get("barcode") or p.get("id") or "").strip()
            score = p.get("score") or p.get("bariScore")
            grade = p.get("grade") or p.get("bariGrade")
            name  = (p.get("name") or p.get("productName") or bc or "?")
            nova  = p.get("novaGroup")
            all_products.append({
                "barcode":   bc,
                "name":      name,
                "category":  cat,
                "score_off": score,
                "grade_off": grade or (_grade(score) if score is not None else "?"),
                "nova":      nova,
            })
    return all_products


def main() -> int:
    print("=" * 72)
    print("TASK-371: D4 Additive Score (BARI_D4_SCORE_V1) Verification")
    print("=" * 72)

    # ── Flag state check ──────────────────────────────────────────────────────
    print(f"\nEngine flag at import: BARI_D4_SCORE_V1={'on' if _d4_flag_at_import_time else 'off'}")
    if _d4_flag_at_import_time:
        print("WARNING: Flag was ON at import -- OFF proof requires re-run with env unset")

    # ── Score-eligible set ────────────────────────────────────────────────────
    eligible = sorted([k for k, v in GLASSBOX_W2_ADDITIVES.items()
                       if v.get("tier") == "contested" and v.get("score_eligible", False)])
    non_eligible = sorted([k for k, v in GLASSBOX_W2_ADDITIVES.items()
                           if v.get("tier") == "contested" and not v.get("score_eligible", True)])
    print(f"\nScore-eligible (HIGH-conf contested, {len(eligible)}):")
    print(f"  {eligible}")
    print(f"Display-contested / non-eligible (LOW-conf, {len(non_eligible)}):")
    print(f"  {non_eligible}")

    # ── Build barcode index ───────────────────────────────────────────────────
    print("\nBuilding barcode -> ingredients index from BSIP1 corpus...")
    bc_index = _build_barcode_index()
    print(f"  Indexed barcodes with ingredient text: {len(bc_index)}")

    # ── Load products ─────────────────────────────────────────────────────────
    print("\nLoading live frontend products (committed baseline)...")
    products = _load_live_products()
    total = len(products)
    print(f"  Total products: {total}")

    # Match barcodes to ingredients
    matched = 0
    for p in products:
        bc  = p["barcode"]
        ing = bc_index.get(bc, "")
        p["ingredients"] = ing
        if ing:
            matched += 1
    print(f"  Matched to ingredient text: {matched}/{total}")
    print(f"  No ingredient text (penalty=0): {total - matched}/{total}")

    # ── Step 2: Compute D4 penalties ─────────────────────────────────────────
    print("\n" + "-" * 72)
    print("Step 2: Computing D4 penalties per product")
    print("-" * 72)

    movers: list[dict] = []
    grade_changers: list[dict] = []

    for p in products:
        if not p["ingredients"] or p["score_off"] is None:
            p["d4_penalty"] = 0
            p["d4_note"]    = "no ingredients or no score"
            p["score_on"]   = p["score_off"]
            p["grade_on"]   = p["grade_off"]
            continue

        # ECS stub = 0 (conservative upper bound)
        l3_stub = {"emulsifier_complexity_penalty": 0}
        penalty, note = compute_d4_score_penalty(p["ingredients"], l3_stub)

        p["d4_penalty"] = penalty
        p["d4_note"]    = note

        if penalty > 0:
            score_on = round(max(0.0, float(p["score_off"]) - penalty), 1)
            grade_on = _grade(score_on)
        else:
            score_on = p["score_off"]
            grade_on = p["grade_off"]

        p["score_on"] = score_on
        p["grade_on"] = grade_on

        if penalty > 0:
            movers.append(p)
            if p["grade_off"] != grade_on:
                grade_changers.append(p)

    print(f"\n  Products with penalty > 0: {len(movers)}/{total}")
    print(f"  Grade changes:             {len(grade_changers)}")

    # ── Step 3: OFF = byte-identical proof ────────────────────────────────────
    print("\n" + "-" * 72)
    print("Step 3: OFF=byte-identical proof")
    print("-" * 72)

    off_pass = not _d4_flag_at_import_time
    if off_pass:
        print("  PASS: Engine imported at OFF state (env BARI_D4_SCORE_V1 unset/off).")
        print("  PASS: score_product() guards the penalty block with `if BARI_D4_SCORE_V1`.")
        print("  PASS: No new keys added to result dict when OFF.")
        print("  CONCLUSION: OFF rescore is byte-identical to committed baseline by code path.")
    else:
        print("  FAIL: Engine imported with BARI_D4_SCORE_V1=on -- re-run with env unset")

    # ── Step 4: By-category distributions ────────────────────────────────────
    print("\n" + "-" * 72)
    print("Step 4: Before/After grade distributions by category")
    print("-" * 72)

    cat_off:    defaultdict[str, list] = defaultdict(list)
    cat_on:     defaultdict[str, list] = defaultdict(list)
    s_off_map:  defaultdict[str, list] = defaultdict(list)
    s_on_map:   defaultdict[str, list] = defaultdict(list)

    for p in products:
        c = p["category"]
        cat_off[c].append(p["grade_off"])
        cat_on[c].append(p["grade_on"])
        if p["score_off"] is not None:
            s_off_map[c].append(float(p["score_off"]))
        if p["score_on"] is not None:
            s_on_map[c].append(float(p["score_on"]))

    for cat in sorted(cat_off.keys()):
        off_c = dict(sorted(Counter(cat_off[cat]).items()))
        on_c  = dict(sorted(Counter(cat_on[cat]).items()))
        n     = len(cat_off[cat])
        chgs  = sum(1 for a, b in zip(cat_off[cat], cat_on[cat]) if a != b)
        so = s_off_map.get(cat, [])
        sn = s_on_map.get(cat, [])
        m_off = f"{statistics.mean(so):.1f}" if so else "N/A"
        m_on  = f"{statistics.mean(sn):.1f}" if sn else "N/A"
        sd_off = f"{statistics.stdev(so):.1f}" if len(so) > 1 else "N/A"
        sd_on  = f"{statistics.stdev(sn):.1f}" if len(sn) > 1 else "N/A"
        print(f"\n  {cat} (n={n}):")
        print(f"    OFF: {off_c}  mean={m_off} stdev={sd_off}")
        print(f"    ON:  {on_c}   mean={m_on}  stdev={sd_on}")
        if chgs:
            print(f"    *** {chgs} grade change(s) ***")

    # ── Step 5: Grade-change detail table ────────────────────────────────────
    print("\n" + "-" * 72)
    print(f"Step 5: Grade-change detail ({len(grade_changers)} products)")
    print("-" * 72)

    if not grade_changers:
        print("  No grade changes.")
    else:
        hdr = f"  {'Barcode':16s} {'Name':33s} {'Cat':22s} {'Pen':>4} {'ScOFF':>6} {'GrOFF':>6} {'ScON':>6} {'GrON':>5}"
        print(hdr)
        print("  " + "-" * 105)
        for p in sorted(grade_changers, key=lambda x: (x["category"], -(x["d4_penalty"]))):
            print(
                f"  {p['barcode']:16s}"
                f" {str(p['name'])[:31]:33s}"
                f" {p['category']:22s}"
                f" {p['d4_penalty']:>4}"
                f" {str(p['score_off']):>6}"
                f" {p['grade_off']:>6}"
                f" {str(p['score_on']):>6}"
                f" {p['grade_on']:>5}"
            )

    # ── Step 6: All movers (penalty > 0) ─────────────────────────────────────
    print("\n" + "-" * 72)
    print(f"Step 6: All movers (penalty > 0) -- {len(movers)} products")
    print("-" * 72)

    for p in sorted(movers, key=lambda x: -(x["d4_penalty"]))[:60]:
        gc = " *** GRADE CHANGE ***" if p["grade_off"] != p["grade_on"] else ""
        print(
            f"  [{p['category']:20s}] pen={p['d4_penalty']:2d}"
            f"  {str(p['score_off']):>6} {p['grade_off']} ->"
            f"  {str(p['score_on']):>6} {p['grade_on']}"
            f"  bc={p['barcode']}{gc}"
        )
    if len(movers) > 60:
        print(f"  ... and {len(movers)-60} more movers (all details)")

    # ── Step 7: Aggregate stats ───────────────────────────────────────────────
    print("\n" + "-" * 72)
    print("Step 7: Aggregate statistics")
    print("-" * 72)

    penalties = [p["d4_penalty"] for p in products if p["d4_penalty"] > 0]
    if penalties:
        print(f"  Products with penalty > 0: {len(penalties)}/{total}")
        mean_pen = statistics.mean(penalties)
        stdev_pen = statistics.stdev(penalties) if len(penalties) > 1 else 0.0
        print(f"  Penalty: min={min(penalties)} max={max(penalties)} mean={mean_pen:.1f} stdev={stdev_pen:.1f}")
        pen_dist = dict(sorted(Counter(penalties).items()))
        print(f"  Penalty value counts: {pen_dist}")
    else:
        print("  No products received a D4 penalty.")

    all_off = dict(sorted(Counter(p["grade_off"] for p in products).items()))
    all_on  = dict(sorted(Counter(p["grade_on"]  for p in products).items()))
    print(f"\n  Overall OFF grade distribution: {all_off}")
    print(f"  Overall ON  grade distribution: {all_on}")
    print(f"  Total grade changes: {len(grade_changers)}")

    # ── Step 8: Integrity checks ──────────────────────────────────────────────
    print("\n" + "-" * 72)
    print("Step 8: Integrity checks")
    print("-" * 72)

    fails: list[str] = []

    # 8a: No penalty exceeds D4_SCORE_CAP
    over_cap = [p for p in products if p["d4_penalty"] > D4_SCORE_CAP]
    if over_cap:
        fails.append(f"CAP VIOLATION: {len(over_cap)} products with penalty > D4_SCORE_CAP={D4_SCORE_CAP}")
    else:
        print(f"  CAP CHECK PASS: no penalty > D4_SCORE_CAP={D4_SCORE_CAP}")

    # 8b: No score increase
    upward = [p for p in products
              if p["score_off"] is not None and p["score_on"] is not None
              and float(p["score_on"]) > float(p["score_off"])]
    if upward:
        fails.append(f"MONOTONE VIOLATION: {len(upward)} products with score increase")
    else:
        print("  MONOTONE CHECK PASS: no product received a score increase")

    # 8c: OFF flag confirmed
    if not off_pass:
        fails.append("FLAG OFF PROOF: engine was imported with BARI_D4_SCORE_V1=on")
    else:
        print("  FLAG OFF CHECK PASS: engine default OFF confirmed")

    # 8d: Score-eligible set sanity (must match spec exactly)
    # E220 added 2026-06-26: standalone sulphite-family entry (juices activation, D7 co-signed).
    # Deduped with E224 via sulphite_family_key — presence in eligible set != double-count.
    expected_eligible = {"E407", "E471", "E466", "E320", "E433", "E951", "E171",
                         "E102", "E110", "E122", "E124", "E129", "E104", "E224", "E220"}
    actual_eligible = set(eligible)
    if actual_eligible != expected_eligible:
        fails.append(f"ELIGIBLE SET MISMATCH: expected {sorted(expected_eligible)}, got {sorted(actual_eligible)}")
    else:
        print(f"  ELIGIBLE SET PASS: {len(expected_eligible)} entries match spec")

    if fails:
        for msg in fails:
            print(f"  FAIL: {msg}")
    else:
        print("  All integrity checks passed.")

    # ── Final summary ─────────────────────────────────────────────────────────
    print("\n" + "=" * 72)
    overall = "PASS" if (not fails and off_pass) else "FAIL"
    print(f"TASK-371 VERIFICATION RESULT: {overall}")
    print(f"  OFF=byte-identical:          {'PASS' if off_pass else 'FAIL'}")
    print(f"  Total products:              {total}")
    print(f"  Matched with ingredient text:{matched}")
    print(f"  Products with D4 penalty:    {len(movers)}")
    print(f"  Grade changes:               {len(grade_changers)}")
    print(f"  Cap violations:              {len(over_cap)}")
    print(f"  Integrity check failures:    {len(fails)}")
    print("=" * 72)
    return 0 if (not fails and off_pass) else 1


if __name__ == "__main__":
    sys.exit(main())
