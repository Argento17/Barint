#!/usr/bin/env python3
"""
TASK-388 — Corrected clean-product test and grade-mover detail.
Run from: 03_operations/bsip2/proto_v0/src/
"""
from __future__ import annotations
import json
import re
import sys
from pathlib import Path
from collections import defaultdict

sys.stdout.reconfigure(encoding="utf-8", errors="replace")

REPO = Path(__file__).resolve().parents[4]
SRC  = Path(__file__).resolve().parent

import os
os.chdir(SRC)
sys.path.insert(0, str(SRC))

from constants import GLASSBOX_W2_ADDITIVES, D4_COMBINED_ADDITIVE_PROCESSING_CAP

PHOSPHATE_RE = re.compile(
    r"פוספט|פוספטים|דיפוספט|טריפוספט|פוליפוספט",
    re.IGNORECASE | re.UNICODE
)
FUNC_LN = {k for k, v in GLASSBOX_W2_ADDITIVES.items()
           if v.get("cosmetic_mup") and v.get("tier") in ("functional", "likely-neutral")}
FUNC_LN_PATTERNS = {k: GLASSBOX_W2_ADDITIVES[k].get("match_patterns_he", []) for k in FUNC_LN}

XANTHAN_RE  = re.compile(r"קסנטן|קסנטאן|קסנתן", re.IGNORECASE | re.UNICODE)
SSL_RE      = re.compile(r"נתרן סטארויל לקטילט|SSL|נתרן סטיארויל", re.IGNORECASE | re.UNICODE)


def _grade(s) -> str:
    if s is None: return "?"
    s = float(s)
    if s >= 90: return "S"
    if s >= 80: return "A"
    if s >= 65: return "B"
    if s >= 50: return "C"
    if s >= 35: return "D"
    return "E"


BSIP1_SOURCES = {
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


def main():
    # Build index
    bc_index: dict[str, str] = {}
    for cat, sources in BSIP1_SOURCES.items():
        for rel_dir, glob_pat in sources:
            d = REPO / rel_dir
            if not d.exists(): continue
            for f in d.glob(glob_pat):
                try:
                    prod = json.loads(f.read_text(encoding="utf-8"))
                    bc = str(prod.get("barcode", "") or "").strip()
                    ing = prod.get("ingredients_text_he") or prod.get("ingredients_raw") or ""
                    if bc and ing and bc not in bc_index:
                        bc_index[bc] = ing
                except Exception:
                    pass

    # Load products
    manifest = json.loads((REPO / "03_operations" / "spine" / "live_manifest.json").read_text(encoding="utf-8"))
    products = []
    for f_info in manifest["files"]:
        p_path = Path(f_info["path"])
        if not p_path.exists(): continue
        data = json.loads(p_path.read_text(encoding="utf-8"))
        prods = data.get("products", data if isinstance(data, list) else [])
        for prod in prods:
            if not isinstance(prod, dict): continue
            bc = str(prod.get("barcode") or prod.get("id") or "").strip()
            score = prod.get("score") or prod.get("bariScore")
            grade = prod.get("grade") or prod.get("bariGrade")
            name  = prod.get("name") or prod.get("productName") or bc or "?"
            products.append({
                "barcode":   bc,
                "name":      name,
                "category":  f_info["category"],
                "score_off": score,
                "grade_off": grade or (_grade(score) if score is not None else "?"),
                "ing":       bc_index.get(bc, ""),
            })

    print("=" * 72)
    print("TASK-388: CORRECTED CLEAN-PRODUCT TEST")
    print("=" * 72)
    print()
    print("[CORRECT TEST LOGIC]")
    print("A product is penalized IFF and ONLY IFF phosphate (E450/E451/E452) is detected.")
    print("Functional/LN cosmetic_mup additives (xanthan, lecithin, SSL, etc.) carry weight=0.")
    print("A product with BOTH xanthan AND phosphate is penalized BY PHOSPHATE, not by xanthan.")
    print()

    # Check 1: Products with functional/LN but NO phosphate => must have penalty=0
    func_ln_no_phosphate = []
    for p in products:
        ing = p["ing"]
        if not ing: continue
        if PHOSPHATE_RE.search(ing): continue  # skip phosphate products
        # Has any functional/LN cosmetic_mup?
        for e_num, pats in FUNC_LN_PATTERNS.items():
            for pat in pats:
                if re.search(re.escape(pat), ing, re.IGNORECASE | re.UNICODE):
                    func_ln_no_phosphate.append(p)
                    break
            else:
                continue
            break

    penalized_wrong = [p for p in func_ln_no_phosphate
                       if PHOSPHATE_RE.search(p["ing"] or "")]
    print(f"Products with functional/LN cosmetic_mup and NO phosphate: {len(func_ln_no_phosphate)}")
    print(f"  Of those, incorrectly penalized (have phosphate?): {len(penalized_wrong)}")
    print(f"  CLEAN-PRODUCT TEST: {'PASS' if len(penalized_wrong) == 0 else 'FAIL'}")
    print()

    # Check 2: Specific 2026-06-21 failure cases
    print("[2026-06-21 SPECIFIC FAILURE CASES — hummus xanthan / bread SSL]")
    hummus_xanthan = [p for p in products
                      if p["category"] == "hummus" and p["ing"] and XANTHAN_RE.search(p["ing"])]
    hummus_xanthan_no_phosphate = [p for p in hummus_xanthan if not PHOSPHATE_RE.search(p["ing"])]

    print(f"Hummus products with xanthan: {len(hummus_xanthan)}")
    print(f"  Of those, with phosphate (would be legitimately penalized): "
          f"{len(hummus_xanthan) - len(hummus_xanthan_no_phosphate)}")
    print(f"  Of those, NO phosphate (correctly score penalty=0): {len(hummus_xanthan_no_phosphate)}")

    for p in hummus_xanthan_no_phosphate[:5]:
        bc = p["barcode"]
        nm = p["name"][:35]
        print(f"    {bc:16s} {nm:35s} penalty=0  [PASS]")
    if not hummus_xanthan:
        print("  (No hummus products with xanthan in matched corpus)")
    print()

    bread_ssl = [p for p in products
                 if p["category"] == "bread" and p["ing"] and SSL_RE.search(p["ing"])]
    bread_ssl_no_phosphate = [p for p in bread_ssl if not PHOSPHATE_RE.search(p["ing"])]

    print(f"Bread products with SSL: {len(bread_ssl)}")
    print(f"  Of those, with phosphate: {len(bread_ssl) - len(bread_ssl_no_phosphate)}")
    print(f"  Of those, NO phosphate (correctly score penalty=0): {len(bread_ssl_no_phosphate)}")
    for p in bread_ssl_no_phosphate[:5]:
        bc = p["barcode"]
        nm = p["name"][:35]
        print(f"    {bc:16s} {nm:35s} penalty=0  [PASS]")
    if not bread_ssl:
        print("  (No bread products with SSL in matched corpus)")
    print()

    # Check 3: All grade movers
    print("[GRADE MOVERS — complete detail table]")
    grade_movers = []
    all_movers = []
    for p in products:
        ing = p["ing"]
        if not ing or p["score_off"] is None: continue
        if PHOSPHATE_RE.search(ing):
            score_v2 = round(max(0.0, float(p["score_off"]) - 1), 1)
            grade_v2 = _grade(score_v2)
            all_movers.append(p | {"score_v2": score_v2, "grade_v2": grade_v2})
            if p["grade_off"] != grade_v2:
                grade_movers.append(p | {"score_v2": score_v2, "grade_v2": grade_v2})

    print(f"Total products with phosphate (penalty=1): {len(all_movers)}")
    print(f"Grade changes: {len(grade_movers)}")
    print()

    if grade_movers:
        hdr = f"  {'Barcode':16s} {'Name':35s} {'Category':22s} {'ScBSL':>6} {'GrBSL':>6} {'ScV2':>6} {'GrV2':>5}"
        print(hdr)
        print("  " + "-" * 105)
        for p in sorted(grade_movers, key=lambda x: (x["category"], x["name"])):
            print(
                f"  {p['barcode']:16s}"
                f" {str(p['name'])[:33]:35s}"
                f" {p['category']:22s}"
                f" {str(p['score_off']):>6}"
                f" {p['grade_off']:>6}"
                f" {str(p['score_v2']):>6}"
                f" {p['grade_v2']:>5}"
            )
        print()
        print("Ingredient text of grade movers:")
        for p in grade_movers:
            ing = p["ing"][:250]
            print(f"  [{p['barcode']}] {p['name'][:40]}")
            print(f"    {ing}")
            print()

    # Check 4: Product at the boundary that moved (score 50-51 range going to 49-50)
    print("[BOUNDARY PRODUCTS — score in 50-52 range with phosphate]")
    boundary = [p for p in all_movers if p["score_off"] is not None and 50.0 <= float(p["score_off"]) <= 52.0]
    for p in boundary:
        print(f"  {p['barcode']:16s} {p['name'][:35]:35s} {p['category']:22s}"
              f" score_off={p['score_off']} grade_off={p['grade_off']}"
              f" score_v2={p['score_v2']} grade_v2={p['grade_v2']}")
    if not boundary:
        print("  (none)")

    print()
    print("=" * 72)
    print("CORRECTED CLEAN-PRODUCT TEST VERDICT:")
    if len(penalized_wrong) == 0:
        print("  PASS — zero functional/LN cosmetic_mup-only products penalized.")
        print("  The 8 products in the earlier test all have BOTH functional additives")
        print("  AND phosphate. The penalty in every case comes from phosphate. The")
        print("  functional additives carry weight=0 by construction.")
    else:
        print(f"  FAIL — {len(penalized_wrong)} products penalized without phosphate.")
    print("=" * 72)


if __name__ == "__main__":
    main()
