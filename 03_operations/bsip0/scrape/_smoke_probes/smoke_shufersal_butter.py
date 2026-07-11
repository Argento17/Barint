"""
TASK-518 smoke probe -- Shufersal, butter shelf. Re-verifies the ALREADY-WORKING
retailer (per the task brief: "the one solid retailer") with a fresh live run
rather than trusting memory of past runs. Reuses the proven 3-phase engine
(shufersal_butter/01_scrape_butter.py) unmodified via import; only caps
MAX_PRODUCTS lower and redirects output into the scrape tree (never touches
02_products/, per TASK-518 scope -- infra proof only, not a category build).
"""
from __future__ import annotations
import importlib.util
import json
import sys
from datetime import datetime
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8", errors="replace")

HERE = Path(__file__).resolve().parent
OUT_DIR = HERE / "outputs" / "shufersal_butter"
OUT_DIR.mkdir(parents=True, exist_ok=True)

BUTTER_SCRIPT = Path(r"C:\Bari\03_operations\bsip0\scrape\shufersal_butter\01_scrape_butter.py")
spec = importlib.util.spec_from_file_location("shufersal_butter_core", BUTTER_SCRIPT)
core = importlib.util.module_from_spec(spec)
spec.loader.exec_module(core)

# Cap for a smoke probe (task asks for ~15-30 SKUs), don't run the full-size category build.
core.MAX_PRODUCTS = 25

sys.path.insert(0, str(HERE.parent / "_shared"))
from plausibility_gate import check_panel, FoodClass  # noqa: E402
from bsip0_nutrition import parse_nutrition_numeric  # noqa: E402


def main():
    products, notes = core.run_acquisition(verbose=True)

    parse_ok = 0
    gate_pass = 0
    gate_fail_detail = []
    for p in products:
        nutr_numeric = parse_nutrition_numeric(p["nutrition"])
        has_core = sum(1 for k in ("energy_kcal", "fat_g", "carbohydrates_g", "protein_g") if nutr_numeric.get(k) is not None)
        if has_core >= 3:
            parse_ok += 1
        gate_input = {
            "energy_kcal": nutr_numeric.get("energy_kcal"),
            "carbs": nutr_numeric.get("carbohydrates_g"),
            "fat": nutr_numeric.get("fat_g"),
            "protein": nutr_numeric.get("protein_g"),
            "sugar": nutr_numeric.get("sugars_g"),
        }
        # Butter is a near-pure-fat product (~700-750 kcal/100g) -- FoodClass.SPREAD
        # (40-750 kcal bound) is the correct calibration, not DAIRY_SOLID (cheese-
        # calibrated, 40-450) or DRY_BAR. See TASK-518 return notes.
        verdict = check_panel(gate_input, FoodClass.SPREAD, p.get("ingredients_raw", ""))
        if verdict.ok:
            gate_pass += 1
        else:
            gate_fail_detail.append({"barcode": p.get("barcode"), "name": p.get("name_he"), "reasons": verdict.reasons})

    ts = datetime.utcnow().strftime("%Y%m%dT%H%M%S")
    out_path = OUT_DIR / f"shufersal_butter_smoke_raw_{ts}.json"
    out_path.write_text(json.dumps(products, ensure_ascii=False, indent=2), encoding="utf-8")

    summary = {
        "candidates_total_seen_before_cap": None,  # run_acquisition doesn't expose pre-cap discovery count directly
        "products_fetched": len(products),
        "parse_rate_core4_of_fetched": f"{parse_ok}/{len(products)}",
        "gate_pass_of_fetched": f"{gate_pass}/{len(products)}",
        "gate_fail_detail": gate_fail_detail,
        "raw_output_path": str(out_path),
    }
    print("\n=== SMOKE PROBE SUMMARY (Shufersal / butter) ===")
    print(json.dumps(summary, ensure_ascii=False, indent=2))
    (OUT_DIR / "smoke_summary.json").write_text(json.dumps(summary, ensure_ascii=False, indent=2), encoding="utf-8")


if __name__ == "__main__":
    main()
