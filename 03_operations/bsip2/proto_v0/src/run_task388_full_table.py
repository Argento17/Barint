#!/usr/bin/env python3
"""
TASK-388 — Full phosphate impact table (all 35 products, stable).
Run: python run_task388_full_table.py
"""
from __future__ import annotations
import json
import re
import sys
import os
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8", errors="replace")
REPO = Path(__file__).resolve().parents[4]
SRC  = Path(__file__).resolve().parent
os.chdir(SRC)
sys.path.insert(0, str(SRC))

from constants import GLASSBOX_W2_ADDITIVES

PHOSPHATE_RE = re.compile(
    r"פוספט|פוספטים|דיפוספט|טריפוספט|פוליפוספט",
    re.IGNORECASE | re.UNICODE
)


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
            if not d.exists():
                continue
            for f in d.glob(glob_pat):
                try:
                    prod = json.loads(f.read_text(encoding="utf-8"))
                    bc = str(prod.get("barcode", "") or "").strip()
                    ing = prod.get("ingredients_text_he") or prod.get("ingredients_raw") or ""
                    if bc and ing and bc not in bc_index:
                        bc_index[bc] = ing
                except Exception:
                    pass

    # Load live products
    manifest = json.loads(
        (REPO / "03_operations" / "spine" / "live_manifest.json").read_text(encoding="utf-8")
    )
    products = []
    for f_info in manifest["files"]:
        p_path = Path(f_info["path"])
        if not p_path.exists():
            continue
        data = json.loads(p_path.read_text(encoding="utf-8"))
        prods = data.get("products", data if isinstance(data, list) else [])
        for prod in prods:
            if not isinstance(prod, dict):
                continue
            bc = str(prod.get("barcode") or prod.get("id") or "").strip()
            score = prod.get("score") or prod.get("bariScore")
            grade = prod.get("grade") or prod.get("bariGrade")
            name = prod.get("name") or prod.get("productName") or bc or "?"
            products.append({
                "barcode":   bc,
                "name":      name,
                "category":  f_info["category"],
                "score_off": score,
                "grade_off": grade or (_grade(score) if score is not None else "?"),
                "ing":       bc_index.get(bc, ""),
            })

    print("FULL TABLE: ALL 35 PHOSPHATE-DETECTED PRODUCTS (penalty=+1 on published baseline)")
    print("Baseline = BARI_D4_SCORE_V1 published scores (contested already included)")
    print("=" * 115)
    row_fmt = "{:>3} {:17s} {:22s} {:>7} {:>6} {:>7} {:>6}  {}"
    print(row_fmt.format("#", "Barcode", "Category", "ScBSL", "GrBSL", "ScV2", "GrV2", "Name"))
    print("    " + "-" * 111)

    n = 0
    grade_changes = 0
    rows = []
    for p in sorted(products, key=lambda x: (x["category"], str(x["name"]))):
        ing = p["ing"]
        if not ing or p["score_off"] is None:
            continue
        if not PHOSPHATE_RE.search(ing):
            continue
        n += 1
        score_v2 = round(max(0.0, float(p["score_off"]) - 1), 1)
        grade_v2 = _grade(score_v2)
        gc = "***" if p["grade_off"] != grade_v2 else "   "
        if p["grade_off"] != grade_v2:
            grade_changes += 1
        rows.append((n, p["barcode"], p["category"], p["score_off"], p["grade_off"],
                     score_v2, grade_v2, gc, str(p["name"])[:45]))
        print(row_fmt.format(
            n,
            p["barcode"],
            p["category"],
            str(p["score_off"]),
            p["grade_off"],
            str(score_v2),
            grade_v2,
            gc + " " + str(p["name"])[:45],
        ))

    print("    " + "-" * 111)
    print(f"Total: {n} products penalized | Grade changes: {grade_changes}")
    print()
    print("NOTE: 'ScBSL/GrBSL' = published BARI_D4_SCORE_V1 baseline (already includes")
    print("      contested penalty where applicable). 'ScV2/GrV2' = score with +1 phosphate")
    print("      incremental on top. Penalty = -1 point on composite (binary per product).")
    print()
    print("GRADE CHANGE SUMMARY:")
    for row in rows:
        n_i, bc, cat, s_off, g_off, s_v2, g_v2, gc, name = row
        if gc.strip() == "***":
            print(f"  {bc:17s} {cat:22s} {str(s_off):>7} {g_off} -> {str(s_v2):>7} {g_v2}")
            print(f"  Name: {name}")


if __name__ == "__main__":
    main()
