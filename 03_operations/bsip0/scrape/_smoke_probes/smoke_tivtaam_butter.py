"""
TASK-518 smoke probe -- Tiv Taam, butter shelf (query "חמאה"). Proves discovery
(paginated v2 API, `total` field gives the real discoverable count), fetch+parse
in ONE call (nutritionValues inline on every search row), and plausibility gate.
"""
from __future__ import annotations
import json
import sys
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8", errors="replace")
sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "tiv_taam"))
sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "_shared"))

from acquire_tivtaam import acquire  # noqa: E402
from plausibility_gate import check_panel, FoodClass  # noqa: E402
from bsip0_nutrition import parse_nutrition_numeric  # noqa: E402

OUT_DIR = Path(__file__).resolve().parent / "outputs" / "tivtaam_butter"


def main():
    records, out_path = acquire("חמאה", "butter", OUT_DIR, max_products=30)

    scraped_ok = [r for r in records if r.get("status") == "scraped"]
    parse_ok = 0
    gate_pass = 0
    gate_fail_detail = []
    for r in scraped_ok:
        nutr_numeric = parse_nutrition_numeric(r["nutrition"])
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
        verdict = check_panel(gate_input, FoodClass.SPREAD, r.get("ingredients_raw", ""))
        if verdict.ok:
            gate_pass += 1
        else:
            gate_fail_detail.append({"barcode": r.get("barcode"), "name": r.get("name_he"), "reasons": verdict.reasons})

    summary = {
        "discovered_candidates": len(records),
        "scraped_ok": len(scraped_ok),
        "empty_panel": sum(1 for r in records if r.get("status") == "empty_panel"),
        "no_barcode": sum(1 for r in records if r.get("status") == "no_barcode"),
        "parse_rate_core4_of_scraped": f"{parse_ok}/{len(scraped_ok)}" if scraped_ok else "0/0",
        "gate_pass_of_scraped": f"{gate_pass}/{len(scraped_ok)}" if scraped_ok else "0/0",
        "gate_fail_detail": gate_fail_detail,
        "raw_output_path": str(out_path),
        "sample_names": [r.get("name_he") for r in records[:10]],
    }
    print("\n=== SMOKE PROBE SUMMARY (Tiv Taam / butter) ===")
    print(json.dumps(summary, ensure_ascii=False, indent=2))
    (OUT_DIR / "smoke_summary.json").write_text(json.dumps(summary, ensure_ascii=False, indent=2), encoding="utf-8")


if __name__ == "__main__":
    main()
