"""
TASK-362 — Score the BROADENED, GATED bar set through the BSIP2 engine with
REQ-362-R1 routing fixes (protein-marker overrides cracker, engineered-bar
overrides whole_food_fat, negation-aware sweetener detection).

Input : the bar-shelf scrape (bars_bsip0_raw_*.json, 120 products).
Gates : hebrew_scope_test (membership) + plausibility_gate (per-100g sanity).
Engine: reuses build_bsip1() + run_bsip2() from run_task360_phase3.py — the SAME
        proven path that scored v5. classify_bar() splits snack_bars vs protein_bars.

Exclusions (missing-data-discard rule — TASK-362 co-sign):
  5900020039590 (Fitness "חטיף דגנים קלאסי") — scraped ingredient list is
  marketing copy, not real ingredients; discarded before scoring.

Outputs (data only — no frontend write, no copy): BSIP1 files + BSIP2 traces +
a scored manifest with grade distributions, split by category.
"""
from __future__ import annotations
import glob, json, pathlib, sys, datetime

ROOT = pathlib.Path(r"C:\Bari")
sys.stdout.reconfigure(encoding="utf-8", errors="replace")
# snack_bars first so run_task360_phase3 resolves; _shared LAST so its (newer)
# plausibility_gate.py with classify_bar wins over the legacy one in snack_bars/.
sys.path.insert(0, str(ROOT / "02_products" / "snack_bars"))
sys.path.insert(0, str(ROOT / "03_operations" / "bsip0" / "scrape" / "_shared"))

from hebrew_scope_test import scope_test, BAR_SHELF, Scope
from plausibility_gate import classify_bar
from bsip0_nutrition import parse_nutrition_numeric
# reuse the proven builder + engine bridge + serving-aware gate
import run_task360_phase3 as P3

RUN_ID = "score_bars_task362_" + datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
BSIP1_DIR = ROOT / "03_operations" / "bsip1" / RUN_ID / "output"
BSIP2_DIR = ROOT / "02_products" / "snack_bars" / "bsip2_outputs" / RUN_ID / "products"
for d in (BSIP1_DIR, BSIP2_DIR):
    d.mkdir(parents=True, exist_ok=True)

raw_path = sorted(glob.glob(str(ROOT / "02_products/snack_bars/bsip0_outputs/bars_bsip0_raw_*.json")))[-1]
raw = json.load(open(raw_path, encoding="utf-8"))
print(f"loaded {len(raw)} scraped bars from {pathlib.Path(raw_path).name}")

# ── Missing-data-discard exclusions (TASK-362 co-sign, both Nutrition and Product) ──
# Barcodes excluded before scoring due to marketing copy masquerading as ingredients.
EXCLUDED_BARCODES: frozenset[str] = frozenset({
    "5900020039590",  # Fitness "חטיף דגנים קלאסי" — ingredient list is marketing prose
})
excluded_count = sum(1 for p in raw if p["barcode"] in EXCLUDED_BARCODES)
raw = [p for p in raw if p["barcode"] not in EXCLUDED_BARCODES]
print(f"excluded {excluded_count} barcodes (missing-data-discard): {sorted(EXCLUDED_BARCODES)}")

# ── gate: scope + plausibility, then score ──
scored = []
counts = {"excluded_discard": excluded_count, "out_of_scope": 0, "ambiguous": 0, "no_nutrition": 0, "quarantine": 0, "scored": 0}
for p in raw:
    sc = scope_test(p["name_he"], p.get("ingredients_raw", ""), BAR_SHELF)
    if sc.verdict == Scope.OUT_OF_SCOPE:
        counts["out_of_scope"] += 1; continue
    if sc.verdict == Scope.AMBIGUOUS:
        counts["ambiguous"] += 1; continue

    nutr_num = parse_nutrition_numeric(p["nutrition"])
    if nutr_num.get("energy_kcal") is None and nutr_num.get("carbohydrates_g") is None:
        counts["no_nutrition"] += 1; continue

    barcode = p["barcode"]
    code = "P_" + barcode
    gate = P3.run_plausibility_gate(nutr_num, p.get("ingredients_raw", ""), barcode,
                                    p.get("serving_size_g_hint"))
    if gate["verdict"] not in ("pass", "converted_pass"):
        counts["quarantine"] += 1; continue

    meta = {"description": p["name_he"], "name_truncated": p["name_he"], "brand": p.get("brand", ""),
            "code": code, "sku": barcode, "image_url": (p.get("image_urls") or [""])[0],
            "unit_description": "", "health_attrs": [], "all_cat_codes": []}
    scraped = {"plausibility_gate": gate, "ingredients_raw": p.get("ingredients_raw", ""),
               "weight_g": p.get("weight_g"), "serving_g": p.get("serving_size_g_hint"),
               "nutrition_numeric_per_100g": nutr_num}
    bsip1 = P3.build_bsip1(meta, scraped, barcode, RUN_ID)
    bsip1_path = BSIP1_DIR / f"bsip1_{barcode}.json"
    bsip1_path.write_text(json.dumps(bsip1, ensure_ascii=False, indent=2), encoding="utf-8")

    res = P3.run_bsip2(bsip1_path, BSIP2_DIR)
    if res["status"] != "ok":
        print("  BSIP2 ERROR", barcode, res.get("error")); continue
    tr = res["trace"]
    prot = nutr_num.get("protein_g")
    sc_val = tr.get("final_score_estimate", tr.get("score"))
    scored.append({"barcode": barcode, "name": p["name_he"], "brand": p.get("brand", ""),
                   "score": round(sc_val, 1) if sc_val is not None else None,
                   "grade": tr.get("grade_estimate", tr.get("grade")),
                   "category": classify_bar(p["name_he"], prot),
                   "engine_category": tr.get("category"), "protein_g": prot})
    counts["scored"] += 1

# ── split + report ──
snack = sorted([s for s in scored if s["category"] == "snack_bar"], key=lambda x: -(x["score"] or 0))
prot = sorted([s for s in scored if s["category"] == "protein_bar"], key=lambda x: -(x["score"] or 0))

def dist(items):
    from collections import Counter
    return dict(Counter(s["grade"] for s in items))

print("\n=== FUNNEL ===", counts)
print(f"\n=== SNACK BARS ({len(snack)}) grades={dist(snack)} ===")
for s in snack:
    print(f"   {str(s['score']):>5} {s['grade']}  {s['barcode']:14} {s['name'][:34]}")
print(f"\n=== PROTEIN BARS ({len(prot)}) grades={dist(prot)} ===")
for s in prot:
    print(f"   {str(s['score']):>5} {s['grade']}  {s['barcode']:14} {s['name'][:34]}")

manifest = {"run_id": RUN_ID, "scored": len(scored), "funnel": counts,
            "snack_bars": snack, "protein_bars": prot, "source_scrape": pathlib.Path(raw_path).name}
out = ROOT / "02_products" / "snack_bars" / f"{RUN_ID}_manifest.json"
out.write_text(json.dumps(manifest, ensure_ascii=False, indent=2), encoding="utf-8")
print("\nmanifest:", out)
