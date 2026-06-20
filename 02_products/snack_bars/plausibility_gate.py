"""
Snack-bar per-100g plausibility gate — TASK-360 reusable validator.

Usage (standalone verification):
    python plausibility_gate.py <bsip1_file_or_dir>

Or import and call:
    from plausibility_gate import run_gate, batch_gate_report
"""
from __future__ import annotations

import json
import pathlib
import sys
from typing import Any

# ── Gate thresholds (TASK-360 spec) ──────────────────────────────────────────
GATE_MIN_ACCOUNTED_G = 70.0   # carbs+fat+protein+fiber per 100g
GATE_MIN_KCAL_DRY    = 150.0  # kcal/100g minimum for a dry snack format

SUGAR_BEARING_TOKENS = [
    "סוכר", "שוקולד", "דבש", "סירופ", "תמרים", "גלוקוז", "פרוקטוז",
    "מולסה", "מחית תמרים", "ממתיק", "גלוקוז-פרוקטוז",
]


def run_gate(
    nutrition_per_100g: dict,
    ingredients: str = "",
    barcode: str = "",
    serving_g: float | None = None,
) -> dict:
    """
    Apply the TASK-360 per-100g plausibility gate to a single product.

    Args:
        nutrition_per_100g: dict with keys like energy_kcal, carbohydrates_g,
                            fat_g, protein_g, dietary_fiber_g, sugars_g.
                            Accepts BOTH canonical keys (energy_kcal, carbohydrates_g …)
                            AND _100g suffixed keys (energy_kcal_100g, carbohydrates_g_100g …).
        ingredients: raw Hebrew ingredient text (for sugar-token check).
        barcode: for logging only.
        serving_g: if provided and the product fails the direct gate, the gate
                   will attempt to convert values ×(100/serving_g) and re-check.

    Returns dict:
        {
          "verdict": "pass" | "converted_pass" | "quarantine",
          "accounted_mass": float,   # carbs+fat+protein+fiber
          "kcal": float,
          "fail_reasons": list[str],
          "basis": "per_100g" | "converted_from_serving" | None,
          "conversion_factor": float,
          "serving_g_used": float | None,
          "final_nutrition": dict | None,  # per-100g values to use (or None if quarantine)
        }
    """
    def _get(key, alt_key=None):
        v = nutrition_per_100g.get(key)
        if v is None and alt_key:
            v = nutrition_per_100g.get(alt_key)
        return float(v) if v is not None else None

    kcal   = _get("energy_kcal",     "energy_kcal_100g") or 0.0
    carbs  = _get("carbohydrates_g", "carbohydrates_g_100g") or 0.0
    fat    = _get("fat_g",           "fat_g_100g") or 0.0
    prot   = _get("protein_g",       "protein_g_100g") or 0.0
    fiber  = _get("dietary_fiber_g", "fiber_g_100g") or 0.0
    sugars = _get("sugars_g",        "sugars_g_100g")

    accounted = carbs + fat + prot + fiber

    def _check(n_kcal, n_acc, n_sug, ingr):
        fails = []
        if n_acc < GATE_MIN_ACCOUNTED_G:
            fails.append(
                f"accounted_mass={n_acc:.1f}g < {GATE_MIN_ACCOUNTED_G}g per 100g "
                f"(carbs={carbs:.1f}+fat={fat:.1f}+protein={prot:.1f}+fiber={fiber:.1f})"
            )
        if n_sug is not None and n_sug == 0:
            if any(tok in (ingr or "") for tok in SUGAR_BEARING_TOKENS):
                fails.append("sugars_g=0 but ingredients contain sugar-bearing token(s)")
        if n_kcal is not None and n_kcal < GATE_MIN_KCAL_DRY:
            fails.append(f"kcal={n_kcal:.0f} < {GATE_MIN_KCAL_DRY:.0f} (minimum for dry snack)")
        return fails

    fails = _check(kcal, accounted, sugars, ingredients)

    if not fails:
        return {
            "verdict": "pass",
            "accounted_mass": round(accounted, 1),
            "kcal": kcal,
            "fail_reasons": [],
            "basis": "per_100g",
            "conversion_factor": 1.0,
            "serving_g_used": None,
            "final_nutrition": {k: v for k, v in nutrition_per_100g.items()
                                if not k.startswith("_")},
        }

    # Attempt per-serving conversion
    if serving_g and 5.0 < serving_g < 90.0:
        f = 100.0 / serving_g

        def _c(v):
            return round(v * f, 1) if v is not None else None

        conv = {
            "energy_kcal":     _c(kcal),
            "carbohydrates_g": _c(carbs),
            "fat_g":           _c(fat),
            "protein_g":       _c(prot),
            "dietary_fiber_g": _c(fiber),
            "sugars_g":        _c(sugars),
        }
        conv_acc = (conv["carbohydrates_g"] or 0) + (conv["fat_g"] or 0) + \
                   (conv["protein_g"] or 0) + (conv["dietary_fiber_g"] or 0)
        conv_fails = _check(conv.get("energy_kcal") or 0, conv_acc, conv.get("sugars_g"), ingredients)

        if not conv_fails:
            return {
                "verdict": "converted_pass",
                "accounted_mass": round(conv_acc, 1),
                "kcal": conv.get("energy_kcal") or 0.0,
                "fail_reasons": fails,
                "original_fail_reasons": fails,
                "basis": "converted_from_serving",
                "conversion_factor": round(f, 3),
                "serving_g_used": serving_g,
                "final_nutrition": conv,
            }

        return {
            "verdict": "quarantine",
            "accounted_mass": round(accounted, 1),
            "kcal": kcal,
            "fail_reasons": fails,
            "post_conversion_fails": conv_fails,
            "basis": None,
            "conversion_factor": f,
            "serving_g_used": serving_g,
            "final_nutrition": None,
        }

    return {
        "verdict": "quarantine",
        "accounted_mass": round(accounted, 1),
        "kcal": kcal,
        "fail_reasons": fails,
        "no_serving_size": True,
        "basis": None,
        "conversion_factor": 1.0,
        "serving_g_used": None,
        "final_nutrition": None,
    }


def batch_gate_report(bsip1_paths: list[pathlib.Path]) -> dict:
    """
    Run the gate against a list of BSIP1 JSON files and return a summary report.
    Reads normalized_nutrition_per_100g, ingredients_text_he, barcode, serving_size_g.
    """
    results = []
    for path in bsip1_paths:
        try:
            rec = json.loads(path.read_text(encoding="utf-8"))
        except Exception as e:
            results.append({"path": str(path), "error": str(e)})
            continue

        barcode = str(rec.get("barcode", path.stem))
        nn = rec.get("normalized_nutrition_per_100g") or {}
        ingr = rec.get("ingredients_text_he") or rec.get("ingredients_raw") or ""
        serving_g = rec.get("serving_size_g") or rec.get("unit_size_g")

        gate = run_gate(nn, ingr, barcode, serving_g)

        results.append({
            "barcode":       barcode,
            "name":          rec.get("canonical_name_he", "")[:60],
            "verdict":       gate["verdict"],
            "accounted_mass": gate["accounted_mass"],
            "kcal":          gate["kcal"],
            "basis":         gate["basis"],
            "fail_reasons":  gate["fail_reasons"],
        })

    total    = len(results)
    passed   = sum(1 for r in results if r.get("verdict") == "pass")
    conv     = sum(1 for r in results if r.get("verdict") == "converted_pass")
    quarant  = sum(1 for r in results if r.get("verdict") == "quarantine")
    errors   = sum(1 for r in results if "error" in r)

    return {
        "total":                total,
        "passed_direct":        passed,
        "passed_converted":     conv,
        "quarantined":          quarant,
        "errors":               errors,
        "pass_rate_pct":        round((passed + conv) * 100 / total, 1) if total else 0,
        "rows":                 results,
    }


# ── Standalone CLI ────────────────────────────────────────────────────────────

def _print_table(report: dict) -> None:
    rows = report["rows"]
    header = f"{'barcode':<16} {'verdict':<16} {'acc_g':>6} {'kcal':>6}  {'name':<50}"
    print(header)
    print("-" * len(header))
    for r in rows:
        if "error" in r:
            print(f"  ERROR: {r['path']}: {r['error']}")
            continue
        line = (
            f"{r['barcode']:<16} "
            f"{r['verdict']:<16} "
            f"{r['accounted_mass']:>6.1f} "
            f"{r['kcal']:>6.0f}  "
            f"{r['name']:<50}"
        )
        if r["fail_reasons"]:
            line += f"\n    FAILS: {'; '.join(r['fail_reasons'])}"
        print(line)

    print()
    print(f"Total: {report['total']}  "
          f"Pass: {report['passed_direct']}  "
          f"Converted: {report['passed_converted']}  "
          f"Quarantine: {report['quarantined']}  "
          f"Errors: {report['errors']}  "
          f"PassRate: {report['pass_rate_pct']}%")


if __name__ == "__main__":
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")

    args = sys.argv[1:]
    if not args:
        print("Usage: python plausibility_gate.py <bsip1_file.json | bsip1_dir/>")
        sys.exit(1)

    target = pathlib.Path(args[0])
    if target.is_dir():
        paths = sorted(target.glob("bsip1_*.json"))
    elif target.is_file():
        paths = [target]
    else:
        print(f"Not found: {target}", file=sys.stderr)
        sys.exit(1)

    if not paths:
        print(f"No bsip1_*.json files found in {target}", file=sys.stderr)
        sys.exit(1)

    report = batch_gate_report(paths)
    _print_table(report)

    # Exit non-zero if any quarantine
    if report["quarantined"] > 0:
        sys.exit(1)
