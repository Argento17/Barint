"""
BSIP1 Enrichment Runner
Applies ingredient_enricher.enrich() to all product JSON files across
all BSIP1 runs, updates them in-place, and produces a validation report.

Usage:
  python enrich_runner.py                   # enrich all runs, write report
  python enrich_runner.py --dry-run         # enrich but do not write files
  python enrich_runner.py --run run_001     # enrich one run only
"""
import sys
import json
import pathlib
import argparse
import datetime

sys.path.insert(0, str(pathlib.Path(__file__).parent))
from ingredient_enricher import enrich, ENRICHMENT_VERSION

BSIP1_ROOT = pathlib.Path(r"C:\Bari\03_operations\bsip1")
REPORT_ROOT = BSIP1_ROOT / "reports"

RUNS = {
    "run_001":         BSIP1_ROOT / "run_001"          / "output",
    "run_cereals_001": BSIP1_ROOT / "run_cereals_001"  / "output",
    "run_yogurt_001":  BSIP1_ROOT / "run_yogurt_001"   / "output",
    "run_milk_001":    BSIP1_ROOT / "run_milk_001"     / "output",
    "run_milk_002":    BSIP1_ROOT / "run_milk_002"     / "output",
    "run_hummus_001":  BSIP1_ROOT / "run_hummus_001"   / "output",
    "run_yogurt_003":  BSIP1_ROOT / "run_yogurt_003"   / "output",
}


def load_product(path: pathlib.Path) -> dict:
    with open(path, encoding="utf-8") as f:
        return json.load(f)


def write_product(path: pathlib.Path, record: dict):
    with open(path, "w", encoding="utf-8") as f:
        json.dump(record, f, ensure_ascii=False, indent=2)


def enrich_run(run_id: str, run_dir: pathlib.Path, dry_run: bool) -> list[dict]:
    """
    Enrich all product (non-audit) JSON files in run_dir.
    Returns list of per-product result dicts for the validation report.
    """
    if not run_dir.exists():
        print(f"  [SKIP] {run_id}: directory not found ({run_dir})")
        return []

    files = sorted(f for f in run_dir.glob("bsip1_*.json") if "audit" not in f.name)
    if not files:
        print(f"  [SKIP] {run_id}: no product files found")
        return []

    print(f"  [{run_id}] {len(files)} products")
    results = []

    for path in files:
        try:
            record = load_product(path)
            enriched = enrich(record)

            if not dry_run:
                write_product(path, enriched)

            es = enriched.get("enrichment_summary", {})
            results.append({
                "run_id":           run_id,
                "pid":              record.get("canonical_product_id", path.stem),
                "name":             record.get("canonical_name_he", "?"),
                "raw_source":       enriched.get("ingredients_raw_provenance", {}).get("source", "?"),
                "raw_missing":      enriched.get("ingredients_raw_provenance", {}).get("missing", True),
                "ingredient_count": es.get("ingredient_count_parsed", 0),
                "additive_count":   es.get("additive_count", 0),
                "flavor_count":     es.get("flavor_marker_count", 0),
                "sweetener_count":  es.get("sweetener_count", 0),
                "protein_count":    es.get("protein_marker_count", 0),
                "matrix_count":     es.get("matrix_marker_count", 0),
                "ferment_count":    es.get("fermentation_marker_count", 0),
                "roast_count":      es.get("roasting_marker_count", 0),
                "has_flavor_desc":  es.get("has_flavor_descriptor", False),
                "has_live_cult":    es.get("has_live_cultures", False),
                "has_isolate":      es.get("has_protein_isolate_or_concentrate", False),
                "warnings":         enriched.get("enrichment_warnings", []),
                # Examples for validation report
                "additives_ex":     [e["term"] for e in enriched.get("extracted_additives", [])[:5]],
                "flavors_ex":       [e["term"] for e in enriched.get("extracted_flavors", [])[:3]],
                "sweeteners_ex":    [e["term"] for e in enriched.get("extracted_sweeteners", [])[:5]],
                "proteins_ex":      [e["term"] for e in enriched.get("extracted_protein_markers", [])[:4]],
                "matrix_ex":        [e["term"] for e in enriched.get("extracted_matrix_markers", [])[:4]],
                "ferment_ex":       [e["term"] for e in enriched.get("extracted_fermentation_markers", [])[:3]],
                "roast_ex":         [e["term"] for e in enriched.get("extracted_roasting_markers", [])[:3]],
                "order_sample":     [i["text"][:50] for i in enriched.get("ingredient_order", [])[:3]],
            })
        except Exception as e:
            print(f"    ERROR {path.name}: {e}")
            results.append({
                "run_id": run_id, "pid": path.stem, "name": "?",
                "raw_source": "error", "raw_missing": True,
                "ingredient_count": 0, "additive_count": 0,
                "flavor_count": 0, "sweetener_count": 0,
                "protein_count": 0, "matrix_count": 0,
                "ferment_count": 0, "roast_count": 0,
                "has_flavor_desc": False, "has_live_cult": False, "has_isolate": False,
                "warnings": [str(e)],
                "additives_ex": [], "flavors_ex": [], "sweeteners_ex": [],
                "proteins_ex": [], "matrix_ex": [], "ferment_ex": [],
                "roast_ex": [], "order_sample": [],
            })
    return results


def _pct(n, total):
    return f"{n}/{total} ({int(n/total*100)}%)" if total else "0/0"


def generate_report(all_results: list[dict], dry_run: bool) -> str:
    ts = datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%d %H:%M UTC")
    total = len(all_results)
    lines = [
        "# BSIP1 Ingredient Enrichment — Validation Report",
        f"\n**Generated:** {ts}",
        f"**Enrichment version:** {ENRICHMENT_VERSION}",
        f"**Mode:** {'DRY RUN (files not modified)' if dry_run else 'APPLIED (files updated in-place)'}",
        f"**Total products enriched:** {total}",
        "",
    ]

    # ── Coverage ──
    lines += ["## 1. Coverage Summary", ""]
    by_run: dict[str, list[dict]] = {}
    for r in all_results:
        by_run.setdefault(r["run_id"], []).append(r)

    lines += ["| Run | Products | Raw Available | Avg Ingredients | Avg Additives |",
              "|---|---|---|---|---|"]
    for run_id, recs in sorted(by_run.items()):
        n = len(recs)
        raw_ok = sum(1 for r in recs if not r["raw_missing"])
        avg_ing = sum(r["ingredient_count"] for r in recs) / n if n else 0
        avg_add = sum(r["additive_count"] for r in recs) / n if n else 0
        lines.append(f"| {run_id} | {n} | {_pct(raw_ok, n)} | {avg_ing:.1f} | {avg_add:.1f} |")

    lines += [
        "",
        f"**Raw ingredient text available:** {_pct(sum(1 for r in all_results if not r['raw_missing']), total)}",
        f"**From BSIP0 scrape:** {_pct(sum(1 for r in all_results if r['raw_source'] == 'bsip0_scrape'), total)}",
        f"**BSIP1 text fallback:** {_pct(sum(1 for r in all_results if r['raw_source'] == 'bsip1_text_fallback'), total)}",
        f"**Missing (no source):** {_pct(sum(1 for r in all_results if r['raw_missing']), total)}",
        "",
    ]

    # ── Ordered parsing ──
    lines += ["## 2. Ordered Ingredient Parsing", ""]
    parsed_ok = sum(1 for r in all_results if r["ingredient_count"] > 0)
    lines += [
        f"**Parse success rate:** {_pct(parsed_ok, total)}",
        f"**Average ingredient count:** {sum(r['ingredient_count'] for r in all_results)/total:.1f}",
        f"**Max ingredient count:** {max(r['ingredient_count'] for r in all_results)}",
        "",
        "**Sample parsed ingredient lists:**",
        "",
    ]
    for r in all_results[:3]:
        if r["order_sample"]:
            sample = " → ".join(f"[{i+1}]{t}" for i, t in enumerate(r["order_sample"]))
            lines.append(f"- {r['name'][:40]}: {sample}")
    lines.append("")

    # ── Additive extraction ──
    lines += ["## 3. Additive Extraction", ""]
    with_add = sum(1 for r in all_results if r["additive_count"] > 0)
    lines += [
        f"**Products with ≥1 additive:** {_pct(with_add, total)}",
        "",
        "**Examples:**",
        "",
    ]
    for r in sorted(all_results, key=lambda x: -x["additive_count"])[:5]:
        if r["additives_ex"]:
            lines.append(f"- {r['name'][:45]}: {', '.join(r['additives_ex'])}")
    lines.append("")

    # ── Flavor extraction ──
    lines += ["## 4. Flavor Extraction", ""]
    with_flav = sum(1 for r in all_results if r["flavor_count"] > 0)
    with_desc = sum(1 for r in all_results if r["has_flavor_desc"])
    lines += [
        f"**Products with flavor markers:** {_pct(with_flav, total)}",
        f"**Products with flavor descriptor (בטעם):** {_pct(with_desc, total)}",
        "",
        "**Examples:**",
        "",
    ]
    for r in all_results:
        if r["flavors_ex"]:
            lines.append(f"- {r['name'][:45]}: {', '.join(r['flavors_ex'])}")
        if len([x for x in lines if x.startswith("- ")]) >= 6:
            break
    lines.append("")

    # ── Sweetener extraction ──
    lines += ["## 5. Sweetener Extraction", ""]
    with_sweet = sum(1 for r in all_results if r["sweetener_count"] > 0)
    lines += [
        f"**Products with sweetener markers:** {_pct(with_sweet, total)}",
        "",
        "**Examples:**",
        "",
    ]
    for r in sorted(all_results, key=lambda x: -x["sweetener_count"])[:5]:
        if r["sweeteners_ex"]:
            lines.append(f"- {r['name'][:45]}: {', '.join(r['sweeteners_ex'])}")
    lines.append("")

    # ── Protein markers ──
    lines += ["## 6. Protein / Isolate Extraction", ""]
    with_prot = sum(1 for r in all_results if r["protein_count"] > 0)
    with_iso = sum(1 for r in all_results if r["has_isolate"])
    lines += [
        f"**Products with protein markers:** {_pct(with_prot, total)}",
        f"**Products with isolate or concentrate:** {_pct(with_iso, total)}",
        "",
        "**Examples:**",
        "",
    ]
    for r in sorted(all_results, key=lambda x: -x["protein_count"])[:5]:
        if r["proteins_ex"]:
            lines.append(f"- {r['name'][:45]}: {', '.join(r['proteins_ex'])}")
    lines.append("")

    # ── Matrix markers ──
    lines += ["## 7. Matrix Degradation Markers", ""]
    with_mat = sum(1 for r in all_results if r["matrix_count"] > 0)
    lines += [
        f"**Products with matrix markers:** {_pct(with_mat, total)}",
        "",
        "**Examples:**",
        "",
    ]
    for r in sorted(all_results, key=lambda x: -x["matrix_count"])[:5]:
        if r["matrix_ex"]:
            lines.append(f"- {r['name'][:45]}: {', '.join(r['matrix_ex'])}")
    lines.append("")

    # ── Fermentation markers ──
    lines += ["## 8. Fermentation Markers", ""]
    with_ferm = sum(1 for r in all_results if r["ferment_count"] > 0)
    with_cult = sum(1 for r in all_results if r["has_live_cult"])
    lines += [
        f"**Products with fermentation markers:** {_pct(with_ferm, total)}",
        f"**Products with live cultures:** {_pct(with_cult, total)}",
        "",
        "**Examples:**",
        "",
    ]
    ferm_shown = 0
    for r in all_results:
        if r["ferment_ex"]:
            lines.append(f"- {r['name'][:45]}: {', '.join(r['ferment_ex'])}")
            ferm_shown += 1
        if ferm_shown >= 6:
            break
    lines.append("")

    # ── Roasting markers ──
    lines += ["## 9. Roasting / Baking Markers", ""]
    with_roast = sum(1 for r in all_results if r["roast_count"] > 0)
    lines += [
        f"**Products with roasting/baking markers:** {_pct(with_roast, total)}",
        "",
        "**Examples:**",
        "",
    ]
    roast_shown = 0
    for r in all_results:
        if r["roast_ex"]:
            lines.append(f"- {r['name'][:45]}: {', '.join(r['roast_ex'])}")
            roast_shown += 1
        if roast_shown >= 6:
            break
    lines.append("")

    # ── Products with missing ingredients ──
    missing = [r for r in all_results if r["raw_missing"]]
    if missing:
        lines += ["## 10. Products with Missing Ingredient Data", ""]
        for r in missing:
            lines.append(f"- `{r['pid']}` ({r['run_id']}): {r['name'][:50]}")
        lines.append("")

    # ── Warnings ──
    all_warnings = [(r["pid"], w) for r in all_results for w in r["warnings"]]
    if all_warnings:
        lines += ["## 11. Enrichment Warnings", ""]
        for pid, w in all_warnings[:20]:
            lines.append(f"- `{pid}`: {w}")
        lines.append("")

    # ── Limitations ──
    lines += [
        "## 12. Known Limitations",
        "",
        "1. **Nested sub-ingredient parsing:** Nested groups (e.g., `שבבי שוקולד (סוכר, שמן, לציטין)`) "
        "are included in full-text extraction but position is attributed to the parent ingredient position.",
        "2. **Homonym terms:** Single-word terms like `קרמל` (caramel) may be a color additive OR a flavor "
        "depending on context. The extraction reports the match without resolving ambiguity — BSIP2 must "
        "apply context logic.",
        "3. **BSIP0 coverage:** Only Yohananof scrape data is currently indexed. Products from other "
        "retailers will use the `bsip1_text_fallback` provenance.",
        "4. **Synthetic BSIP1 records** (cereals_001, yogurt_001): These were generated programmatically, "
        "not canonicalized from BSIP0. The `ingredients_text_he` field is the authoritative source; "
        "provenance is `bsip1_text_fallback`.",
        "5. **E-number detection:** E-number matching uses exact string match. E-numbers with dashes "
        "(E-322 vs E322) both patterns are covered but formatting variants may be missed.",
        "6. **Fiber laundering proxy:** `inulin`, `שורש עולש`, `שורש ציקוריה` are flagged as "
        "`prebiotic_fiber` in the additive list. Whether this constitutes fiber laundering requires "
        "nutritional context (fiber %/100g) which is available in the nutrition fields.",
        "7. **Percentage extraction:** Only explicitly declared percentages in parentheses are captured. "
        "Ranges (e.g., 3-5%) are not parsed.",
        "",
        "*Report generated by `enrich_runner.py` — BSIP1 enrichment pipeline*",
    ]

    return "\n".join(lines)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--dry-run", action="store_true")
    parser.add_argument("--run", help="Enrich only this run ID")
    args = parser.parse_args()

    REPORT_ROOT.mkdir(parents=True, exist_ok=True)

    runs_to_process = {args.run: RUNS[args.run]} if args.run and args.run in RUNS else RUNS
    if args.run and args.run not in RUNS:
        print(f"Unknown run ID: {args.run}. Available: {list(RUNS.keys())}")
        sys.exit(1)

    print(f"BSIP1 Enrichment Runner — {ENRICHMENT_VERSION}")
    print(f"Mode: {'DRY RUN' if args.dry_run else 'WRITE'}")
    print()

    all_results: list[dict] = []
    for run_id, run_dir in sorted(runs_to_process.items()):
        results = enrich_run(run_id, run_dir, args.dry_run)
        all_results.extend(results)

    print(f"\nTotal: {len(all_results)} products processed")

    report_text = generate_report(all_results, args.dry_run)
    report_path = REPORT_ROOT / "enrichment_validation_001.md"
    report_path.write_text(report_text, encoding="utf-8")
    print(f"Report written: {report_path}")


if __name__ == "__main__":
    main()
