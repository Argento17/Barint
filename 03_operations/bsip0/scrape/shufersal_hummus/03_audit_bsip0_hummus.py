"""
BSIP0 audit gate — Hummus and Savory Dips (Shufersal).

Reads all scraped product JSONs and verifies the BSIP0 gate criteria
from corpus_filter.md. Produces a gate report in the reports directory.

Usage:
    python 03_audit_bsip0_hummus.py

Pass criteria (from corpus_filter.md):
    Total products      ≥ 30
    Nutrition coverage  ≥ 80%  (calories + protein + carbs + fat)
    Ingredient coverage ≥ 70%
    Image availability  ≥ 90%
    Traceability        100%   (all products have a Shufersal source URL)
    Corpus filter filed Yes    (corpus_filter.md exists)
"""

from __future__ import annotations

import json
import sys
import datetime
import pathlib

sys.stdout.reconfigure(encoding="utf-8", errors="replace")

OBSERVATIONS_DIR  = pathlib.Path(r"C:\Bari\02_products\hummus\observations_bsip0\shufersal")
REPORT_DIR        = pathlib.Path(r"C:\Bari\02_products\hummus\reports")
CORPUS_FILTER_MD  = pathlib.Path(r"C:\Bari\02_products\hummus\corpus_filter.md")
REPORT_DIR.mkdir(parents=True, exist_ok=True)

# Gate thresholds (from corpus_filter.md)
MIN_PRODUCTS    = 30
MIN_NUTRITION   = 0.80
MIN_INGREDIENTS = 0.70
MIN_IMAGES      = 0.90


def load_products() -> list[dict]:
    products = []
    for f in OBSERVATIONS_DIR.glob("*.json"):
        if f.name.startswith("all_discovered"):
            continue
        try:
            p = json.loads(f.read_text(encoding="utf-8"))
            products.append(p)
        except Exception as e:
            print(f"  [WARN] Could not load {f.name}: {e}")
    return products


def check_nutrition(p: dict) -> bool:
    n = p.get("nutrition", {})
    return bool(n.get("energy_kcal_raw") and n.get("protein_raw") and
                n.get("carbs_raw") and n.get("fat_raw"))


def check_ingredients(p: dict) -> bool:
    return bool((p.get("ingredients_raw") or "").strip())


def check_image(p: dict) -> bool:
    return bool(p.get("image_urls"))


def check_traceable(p: dict) -> bool:
    url = p.get("source_url", "")
    return "shufersal" in url.lower()


def run_gate(products: list[dict]) -> tuple[bool, list[str], dict]:
    total = len(products)
    results: dict[str, int | float | bool] = {"total": total}
    notes: list[str] = []
    passed = True

    # Product count
    if total < MIN_PRODUCTS:
        notes.append(f"FAIL: {total} products < {MIN_PRODUCTS}")
        passed = False
    else:
        notes.append(f"OK: {total} products ≥ {MIN_PRODUCTS}")
    results["product_count_pass"] = total >= MIN_PRODUCTS

    # Nutrition coverage
    n_nutr = sum(1 for p in products if check_nutrition(p))
    nutr_pct = n_nutr / total if total else 0
    results["nutrition_coverage_pct"] = round(nutr_pct * 100, 1)
    results["n_nutrition"] = n_nutr
    if nutr_pct < MIN_NUTRITION:
        notes.append(f"FAIL: nutrition coverage {nutr_pct:.0%} < {MIN_NUTRITION:.0%}")
        passed = False
    else:
        notes.append(f"OK: nutrition coverage {nutr_pct:.0%}")
    results["nutrition_pass"] = nutr_pct >= MIN_NUTRITION

    # Ingredient coverage
    n_ingr = sum(1 for p in products if check_ingredients(p))
    ingr_pct = n_ingr / total if total else 0
    results["ingredient_coverage_pct"] = round(ingr_pct * 100, 1)
    results["n_ingredients"] = n_ingr
    if ingr_pct < MIN_INGREDIENTS:
        notes.append(f"FAIL: ingredient coverage {ingr_pct:.0%} < {MIN_INGREDIENTS:.0%}")
        passed = False
    else:
        notes.append(f"OK: ingredient coverage {ingr_pct:.0%}")
    results["ingredients_pass"] = ingr_pct >= MIN_INGREDIENTS

    # Image coverage
    n_img = sum(1 for p in products if check_image(p))
    img_pct = n_img / total if total else 0
    results["image_coverage_pct"] = round(img_pct * 100, 1)
    results["n_images"] = n_img
    if img_pct < MIN_IMAGES:
        notes.append(f"FAIL: image coverage {img_pct:.0%} < {MIN_IMAGES:.0%}")
        passed = False
    else:
        notes.append(f"OK: image coverage {img_pct:.0%}")
    results["images_pass"] = img_pct >= MIN_IMAGES

    # Traceability
    n_trace = sum(1 for p in products if check_traceable(p))
    results["n_traceable"] = n_trace
    if n_trace < total:
        notes.append(f"FAIL: {total - n_trace} products missing valid Shufersal URL")
        passed = False
    else:
        notes.append(f"OK: all {total} products have Shufersal URLs")
    results["traceability_pass"] = n_trace == total

    # Corpus filter filed
    filter_exists = CORPUS_FILTER_MD.exists()
    results["corpus_filter_filed"] = filter_exists
    if not filter_exists:
        notes.append(f"FAIL: corpus_filter.md not found at {CORPUS_FILTER_MD}")
        passed = False
    else:
        notes.append(f"OK: corpus_filter.md exists")

    results["gate_pass"] = passed
    return passed, notes, results


def write_report(passed: bool, notes: list[str], results: dict, products: list[dict]) -> pathlib.Path:
    ts = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    report_path = REPORT_DIR / f"bsip0_gate_result_{ts}.md"

    lines = [
        f"# BSIP0 Gate Report — Hummus",
        f"",
        f"**Date:** {datetime.date.today().isoformat()}",
        f"**Verdict:** {'PASS' if passed else 'FAIL'}",
        f"",
        f"## Gate criteria",
        f"",
    ]
    for note in notes:
        status = "✅" if note.startswith("OK") else "❌"
        lines.append(f"- {status} {note}")

    lines += [
        f"",
        f"## Summary",
        f"",
        f"| Metric | Value |",
        f"|---|---|",
        f"| Total products | {results['total']} |",
        f"| Nutrition coverage | {results['nutrition_coverage_pct']}% ({results['n_nutrition']}/{results['total']}) |",
        f"| Ingredient coverage | {results['ingredient_coverage_pct']}% ({results['n_ingredients']}/{results['total']}) |",
        f"| Image coverage | {results['image_coverage_pct']}% ({results['n_images']}/{results['total']}) |",
        f"| Traceable | {results['n_traceable']}/{results['total']} |",
        f"| Corpus filter filed | {'Yes' if results['corpus_filter_filed'] else 'No'} |",
        f"",
    ]

    if not passed:
        lines += [
            f"## Next steps on FAIL",
            f"",
            f"- If product count < 30: add optional A162405 category traversal in 01_discover_hummus_shufersal.py",
            f"- If nutrition coverage < 80%: add Yohananof supplementary run for brands with missing data",
            f"- If ingredient coverage < 70%: check scraper ingredient extraction on failing products",
            f"- If image coverage < 90%: check image URL format for missing products",
            f"",
        ]
    else:
        lines += [
            f"## Next step",
            f"",
            f"Gate PASSED. Proceed to BSIP1 enrichment:",
            f"",
            f"```",
            f"cd C:\\Bari\\03_operations\\bsip1\\core",
            f"python enrich_runner.py --input C:\\Bari\\02_products\\hummus\\observations_bsip0\\shufersal --output C:\\Bari\\03_operations\\bsip1\\run_hummus_001\\output",
            f"```",
            f"",
        ]

    report_path.write_text("\n".join(lines), encoding="utf-8")
    return report_path


def main() -> None:
    print("=== BSIP0 Gate Audit — Hummus ===\n")
    products = load_products()
    print(f"Loaded {len(products)} scraped product files from {OBSERVATIONS_DIR}\n")

    if not products:
        print("ERROR: No scraped products found.")
        print(f"Run 02_scrape_hummus_shufersal.py first.")
        sys.exit(1)

    passed, notes, results = run_gate(products)

    for note in notes:
        prefix = "✅" if note.startswith("OK") else "❌"
        print(f"  {prefix} {note}")

    report_path = write_report(passed, notes, results, products)
    print(f"\nReport saved: {report_path}")
    print(f"\nVERDICT: {'PASS' if passed else 'FAIL'}")

    if not passed:
        sys.exit(1)


if __name__ == "__main__":
    main()
