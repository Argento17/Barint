"""
TASK-518 smoke probe -- Yohananof, butter (חמאה) shelf. Small, well-understood
category per the task's acceptance bar. Proves: discovery (full shelf, not
partial), fetch (product modal), parse (ingredients + nutrition via shared
parser), plausibility gate pass rate.
"""
from __future__ import annotations
import json
import sys
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8", errors="replace")
sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "yohananof"))
sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "_shared"))

from acquire_yohananof import acquire  # noqa: E402
from plausibility_gate import check_panel, FoodClass  # noqa: E402
from bsip0_nutrition import parse_nutrition_numeric  # noqa: E402

OUT_DIR = Path(__file__).resolve().parent / "outputs" / "yohananof_butter"

BUTTER_INCLUDE = ["חמאה", "butter", "kerrygold", "lurpak", "גהי"]
BUTTER_DROP = [
    "מרגרינה", "חמאת בוטנים", "חמאת שקדים", "תרסיס", "בוטנים", "שקדים",
    "פופקורן", "עוגי", "עוגה", "ביסקוויט", "קרם", "שמפו", "סבון",
]


def main():
    records, out_path = acquire(BUTTER_INCLUDE, BUTTER_DROP, "butter", OUT_DIR, max_products=30, headless=True)

    total = len(records)
    scraped_ok = [r for r in records if r.get("status") == "scraped"]
    parse_ok = 0
    gate_pass = 0
    gate_fail_reasons = []
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
        verdict = check_panel(gate_input, FoodClass.DAIRY_SOLID, r.get("ingredients_raw", ""))
        if verdict.ok:
            gate_pass += 1
        else:
            gate_fail_reasons.append({"barcode": r.get("barcode"), "name": r.get("name_he"), "reasons": verdict.reasons})

    summary = {
        "discovered_candidates": total,
        "scraped_ok": len(scraped_ok),
        "empty_panel": sum(1 for r in records if r.get("status") == "empty_panel"),
        "not_found": sum(1 for r in records if r.get("status") == "not_found"),
        "failed": sum(1 for r in records if r.get("status") == "failed"),
        "parse_rate_of_scraped": f"{parse_ok}/{len(scraped_ok)}" if scraped_ok else "0/0",
        "gate_pass_of_scraped": f"{gate_pass}/{len(scraped_ok)}" if scraped_ok else "0/0",
        "gate_fail_detail": gate_fail_reasons,
        "raw_output_path": str(out_path),
    }
    print("\n=== SMOKE PROBE SUMMARY (Yohananof / butter) ===")
    print(json.dumps(summary, ensure_ascii=False, indent=2))
    (OUT_DIR / "smoke_summary.json").write_text(json.dumps(summary, ensure_ascii=False, indent=2), encoding="utf-8")
    return summary


if __name__ == "__main__":
    main()
