#!/usr/bin/env python3
"""
P173 / TASK-322 — Standalone detection method for the Fazzino HP carb+sodium cluster.

Fazzino definition (measurement only — NOT wired to score_engine):
  - > 40% kcal from carbohydrate
  - >= 200 mg sodium / 100 g (>= 0.20% sodium by weight)

Run by path: python method_hp_carb_sodium.py --calibrate
OFF-ban: nutrition from in-house BSIP1 panel only; missing → insufficient_data.
"""

from __future__ import annotations

import argparse
import json
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

# ---------------------------------------------------------------------------
# Inert thresholds (NOT referenced by score_engine.py)
# ---------------------------------------------------------------------------
HP_CARB_SODIUM_CARB_PCT_KCAL = 40.0   # strictly greater than this value fires
HP_CARB_SODIUM_SODIUM_MG_100G = 200.0  # >= this value fires

REPO = Path(__file__).resolve().parents[4]
CONFIGS_DIR = REPO / "03_operations" / "page_generator" / "configs"
REPORT_DIR = (
    REPO / "03_operations" / "bsip2" / "proto_v0" / "reports" / "methods" / "hp_carb_sodium"
)


def _atwater_kcal(protein_g: float | None, carbs_g: float | None, fat_g: float | None) -> float | None:
    """Atwater general factors: 4/4/9 kcal per g protein/carbs/fat."""
    if protein_g is None and carbs_g is None and fat_g is None:
        return None
    return (protein_g or 0) * 4 + (carbs_g or 0) * 4 + (fat_g or 0) * 9


def evaluate_hp_carb_sodium(nutrition: dict[str, Any]) -> dict[str, Any]:
    """
    Evaluate carb+sodium HP cluster on normalized per-100g nutrition.

    Returns:
        fires: true | false | "insufficient_data"
        carb_pct_kcal: float | None
        sodium_mg_100g: float | None
        reason: str
    """
    carbs = nutrition.get("carbohydrates_g")
    sodium = nutrition.get("sodium_mg")
    kcal = nutrition.get("energy_kcal")
    protein = nutrition.get("protein_g")
    fat = nutrition.get("fat_g")

    if carbs is None:
        return {
            "fires": "insufficient_data",
            "carb_pct_kcal": None,
            "sodium_mg_100g": sodium,
            "reason": "carbohydrates_g missing",
        }
    if sodium is None:
        return {
            "fires": "insufficient_data",
            "carb_pct_kcal": None,
            "sodium_mg_100g": None,
            "reason": "sodium_mg missing",
        }

    energy_source = "declared"
    if kcal is None or kcal <= 0:
        derived = _atwater_kcal(protein, carbs, fat)
        if derived is None or derived <= 0:
            return {
                "fires": "insufficient_data",
                "carb_pct_kcal": None,
                "sodium_mg_100g": sodium,
                "reason": "energy_kcal missing and macros insufficient for Atwater fallback",
            }
        kcal = derived
        energy_source = "atwater_macros"

    carb_pct = round((carbs * 4 / kcal) * 100, 2)
    carb_ok = carb_pct > HP_CARB_SODIUM_CARB_PCT_KCAL
    sodium_ok = sodium >= HP_CARB_SODIUM_SODIUM_MG_100G
    fires = carb_ok and sodium_ok

    parts = [
        f"carb_pct_kcal={carb_pct}% (>{HP_CARB_SODIUM_CARB_PCT_KCAL}%: {carb_ok})",
        f"sodium_mg={sodium} (>={HP_CARB_SODIUM_SODIUM_MG_100G}: {sodium_ok})",
        f"energy_source={energy_source}",
    ]
    if fires:
        parts.insert(0, "HP_CARB_SODIUM fires")
    else:
        parts.insert(0, "HP_CARB_SODIUM does not fire")

    return {
        "fires": fires,
        "carb_pct_kcal": carb_pct,
        "sodium_mg_100g": sodium,
        "reason": "; ".join(parts),
    }


def discover_shelf_configs() -> list[Path]:
    return sorted(
        p for p in CONFIGS_DIR.glob("*.json") if not p.name.startswith("_generated_")
    )


def normalize_corpus_dirs(config: dict, scoring: dict) -> list[str]:
    bsip1_dir = scoring.get("bsip1_dir")
    if bsip1_dir:
        return [bsip1_dir]
    corpus_dirs = config.get("corpus_dirs", [])
    if isinstance(corpus_dirs, str):
        corpus_dirs = [corpus_dirs]
    return [d for d in corpus_dirs if d]


def collect_bsip1_products(corpus_dirs: list[str]) -> list[tuple[Path, dict]]:
    seen: set[str] = set()
    out: list[tuple[Path, dict]] = []
    for corpus_dir in corpus_dirs:
        cdir = Path(corpus_dir)
        if not cdir.is_dir():
            continue
        for path in sorted(cdir.glob("bsip1_*.json")):
            if "audit" in path.name:
                continue
            try:
                doc = json.loads(path.read_text(encoding="utf-8"))
            except (json.JSONDecodeError, OSError):
                continue
            barcode = str(doc.get("barcode") or "").strip()
            if not barcode or barcode in seen:
                continue
            seen.add(barcode)
            out.append((path, doc))
    return out


def _product_name(doc: dict) -> str:
    return (
        doc.get("canonical_name_he")
        or doc.get("product_name_he")
        or doc.get("canonical_product_id")
        or ""
    )


def _fp_review_hint(doc: dict, shelf: str) -> str:
    """Heuristic false-positive flag for manual review (EV-013 risk_of_misuse)."""
    name = _product_name(doc).lower()
    ingredients = (doc.get("ingredients_text_he") or doc.get("ingredients_raw") or "").lower()
    nn = doc.get("normalized_nutrition_per_100g") or {}
    sugars = nn.get("sugars_g")
    additive_heavy = len(doc.get("ingredients_list") or []) > 8

    endemic_markers = (
        "לחם", "bread", "פיתה", "חלה", "בגט", "לחמנייה",
        "גבינ", "cheese", "צפתית", "בולגרית", "פטה", "מוצרלה",
        "יוגורט", "חמאה", "שמנת",
    )
    snack_markers = (
        "חטיף", "ביסקוויט", "קרקר", "צ'יפס", "ציפס", "פופקורן",
        "דגנים", "קורנפלקס", "גרנולה", "וופל", "עוגי", "במבה", "ביסלי",
    )

    if any(m in name or m in ingredients for m in endemic_markers):
        return "candidate_false_positive — endemic/natural carb+salt matrix (bread/cheese/dairy class)"
    if shelf in ("brined_cheeses", "hard_cheeses", "cheese") and nn.get("sodium_mg", 0) >= 200:
        return "candidate_false_positive — structural dairy sodium + moderate carbs, not refined snack"
    if any(m in name for m in snack_markers) or (sugars is not None and sugars >= 15):
        return "likely_true_positive — refined-carb+salt snack profile"
    if additive_heavy:
        return "likely_true_positive — long ingredient list suggests industrial formulation"
    return "review_needed — carb+salt threshold met; classify manually"


def run_calibration() -> dict[str, Any]:
    products: list[dict[str, Any]] = []
    shelf_totals: dict[str, dict[str, int]] = {}

    for config_path in discover_shelf_configs():
        shelf = config_path.stem
        config = json.loads(config_path.read_text(encoding="utf-8"))
        scoring = config.get("scoring") or {}
        corpus_dirs = normalize_corpus_dirs(config, scoring)
        if not corpus_dirs:
            continue

        shelf_totals.setdefault(shelf, {"evaluated": 0, "fired": 0, "insufficient_data": 0})

        for _path, doc in collect_bsip1_products(corpus_dirs):
            nn = doc.get("normalized_nutrition_per_100g") or {}
            result = evaluate_hp_carb_sodium(nn)
            fires_val = result["fires"]

            shelf_totals[shelf]["evaluated"] += 1
            if fires_val == "insufficient_data":
                shelf_totals[shelf]["insufficient_data"] += 1
            elif fires_val is True:
                shelf_totals[shelf]["fired"] += 1

            products.append({
                "barcode": str(doc.get("barcode") or ""),
                "shelf": shelf,
                "product_name": _product_name(doc),
                "carb_pct_kcal": result["carb_pct_kcal"],
                "sodium_mg_100g": result["sodium_mg_100g"],
                "fires": fires_val,
                "reason": result["reason"],
                "bsip1_source": str(_path),
            })

    products.sort(key=lambda r: (r["shelf"], r["barcode"]))
    fired = [p for p in products if p["fires"] is True]

    summary = {
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "method": "hp_carb_sodium",
        "thresholds": {
            "carb_pct_kcal_gt": HP_CARB_SODIUM_CARB_PCT_KCAL,
            "sodium_mg_100g_gte": HP_CARB_SODIUM_SODIUM_MG_100G,
        },
        "products_evaluated": len(products),
        "fired": len(fired),
        "insufficient_data": sum(1 for p in products if p["fires"] == "insufficient_data"),
        "not_fired": sum(1 for p in products if p["fires"] is False),
        "fire_rate_per_shelf": {
            s: {
                "evaluated": t["evaluated"],
                "fired": t["fired"],
                "insufficient_data": t["insufficient_data"],
                "fire_rate": round(t["fired"] / t["evaluated"], 4) if t["evaluated"] else 0.0,
            }
            for s, t in sorted(shelf_totals.items())
        },
        "products": products,
    }
    return summary, fired, shelf_totals


def write_reports(summary: dict, fired: list[dict], shelf_totals: dict) -> None:
    REPORT_DIR.mkdir(parents=True, exist_ok=True)
    cal_json = REPORT_DIR / "calibration.json"
    cal_md = REPORT_DIR / "calibration.md"

    cal_json.write_text(json.dumps(summary, ensure_ascii=False, indent=2), encoding="utf-8")

    lines = [
        "# HP carb+sodium cluster — calibration dataset (P173)",
        "",
        f"Generated: {summary['generated_at']}",
        "",
        "## Summary",
        "",
        f"| Metric | Count |",
        f"|--------|------:|",
        f"| Products evaluated (denominator) | {summary['products_evaluated']} |",
        f"| Fired (carb>40% kcal AND sodium>=200mg/100g) | {summary['fired']} |",
        f"| Insufficient data | {summary['insufficient_data']} |",
        f"| Did not fire | {summary['not_fired']} |",
        "",
        "## Fire rate per shelf",
        "",
        "| Shelf | Evaluated | Fired | Insufficient | Fire rate |",
        "|-------|----------:|------:|-------------:|----------:|",
    ]
    for shelf, t in sorted(shelf_totals.items()):
        rate = t["fired"] / t["evaluated"] if t["evaluated"] else 0.0
        lines.append(
            f"| {shelf} | {t['evaluated']} | {t['fired']} | {t['insufficient_data']} | {rate:.1%} |"
        )

    lines.extend([
        "",
        "## Manual false-positive review (fired products)",
        "",
        "Per EV-013 `risk_of_misuse`: without calibrated thresholds, HP-style carb+salt",
        "signals can falsely flag naturally salty+carbohydrate foods (bread, cheese, dates).",
        "Review each fired product: refined-carb+salt snack vs defensible endemic food.",
        "",
        "| Shelf | Barcode | Product | carb%kcal | sodium mg/100g | FP review |",
        "|-------|---------|---------|----------:|---------------:|-----------|",
    ])

    for p in fired:
        doc_hint_path = Path(p["bsip1_source"])
        try:
            doc = json.loads(doc_hint_path.read_text(encoding="utf-8"))
            fp = _fp_review_hint(doc, p["shelf"])
        except (OSError, json.JSONDecodeError):
            fp = "review_needed"
        name = p["product_name"].replace("|", "/")
        lines.append(
            f"| {p['shelf']} | {p['barcode']} | {name} | "
            f"{p['carb_pct_kcal']} | {p['sodium_mg_100g']} | {fp} |"
        )

    cal_md.write_text("\n".join(lines) + "\n", encoding="utf-8")


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="HP carb+sodium detection method (P173)")
    parser.add_argument(
        "--calibrate",
        action="store_true",
        help="Run calibration over live BSIP1 corpora from page_generator configs",
    )
    parser.add_argument(
        "--nutrition-json",
        help="Single-product test: path to JSON with normalized_nutrition_per_100g or flat nutrition dict",
    )
    args = parser.parse_args(argv)

    if args.nutrition_json:
        raw = json.loads(Path(args.nutrition_json).read_text(encoding="utf-8"))
        nn = raw.get("normalized_nutrition_per_100g") or raw
        result = evaluate_hp_carb_sodium(nn)
        print(json.dumps(result, ensure_ascii=False, indent=2))
        return 0

    if args.calibrate:
        summary, fired, shelf_totals = run_calibration()
        write_reports(summary, fired, shelf_totals)
        print(json.dumps({
            "products_evaluated": summary["products_evaluated"],
            "fired": summary["fired"],
            "insufficient_data": summary["insufficient_data"],
            "report_dir": str(REPORT_DIR),
        }, indent=2))
        return 0

    parser.print_help()
    return 1


if __name__ == "__main__":
    sys.exit(main())