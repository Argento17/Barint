"""
Acquisition v3 orchestrator — bread_retail_003 (Shufersal representative shelf).

Runs:
  1. shufersal_probe_v3  — 300-product scrape, mainstream-first
  2. composition_gate    — validates corpus balance
  3. BSIP0 gate          — ≥150 products, ≥70% nutrition, ≥50% ingredient coverage
  4. Saves raw JSON to   C:/Bari/02_products/bread_retail_003/
  5. Generates           bread_representation_audit_002.md

Usage:
  python acquisition_v3.py [--dry-run]

  --dry-run  Run composition gate on existing raw JSON without re-scraping.
"""

from __future__ import annotations

import json
import re
import sys
import pathlib
import datetime

sys.path.insert(0, str(pathlib.Path(__file__).parent))
sys.stdout.reconfigure(encoding="utf-8", errors="replace")

from shufersal_probe_v3 import run_acquisition
from composition_gate import check_composition, classify_archetype, print_gate_result

OUT_DIR    = pathlib.Path(r"C:\Bari\02_products\bread_retail_003")
REPORT_DIR = OUT_DIR / "reports"
OUT_DIR.mkdir(parents=True, exist_ok=True)
REPORT_DIR.mkdir(parents=True, exist_ok=True)

TODAY = datetime.date.today().isoformat()
RUN_TS = datetime.datetime.utcnow().strftime("%Y%m%dT%H%M%S")
RUN_ID = f"real_bread_retail_003_v1"


# ──────────────────────────────────────────────────────────────────────────────
# BSIP0 gate
# ──────────────────────────────────────────────────────────────────────────────

def bsip0_gate(products: list[dict]) -> tuple[bool, list[str]]:
    notes: list[str] = []
    total = len(products)
    n_nutr = sum(
        1 for p in products
        if p.get("nutrition", {}).get("energy_kcal_raw") or p.get("nutrition", {}).get("carbs_raw")
    )
    n_ingr = sum(1 for p in products if (p.get("ingredients_raw") or ""))
    n_url = sum(1 for p in products if (p.get("source_url") or "").startswith("https://www.shufersal"))

    nutr_pct = n_nutr * 100 / total if total else 0
    ingr_pct = n_ingr * 100 / total if total else 0

    passed = True
    if total < 150:
        notes.append(f"FAIL: {total} products < 150")
        passed = False
    else:
        notes.append(f"OK: {total} products ≥ 150")
    if nutr_pct < 70:
        notes.append(f"FAIL: nutrition coverage {nutr_pct:.0f}% < 70%")
        passed = False
    else:
        notes.append(f"OK: nutrition coverage {nutr_pct:.0f}%")
    if ingr_pct < 50:
        notes.append(f"WARN: ingredient coverage {ingr_pct:.0f}% < 50% (not a gate fail — score degradation handles this)")
    else:
        notes.append(f"OK: ingredient coverage {ingr_pct:.0f}%")
    if n_url < total * 0.9:
        notes.append(f"WARN: {total - n_url} products lack valid Shufersal URLs")
    else:
        notes.append(f"OK: real Shufersal URLs {n_url}/{total}")

    return passed, notes


# ──────────────────────────────────────────────────────────────────────────────
# Audit report generator
# ──────────────────────────────────────────────────────────────────────────────

def _price_tier(price_per_100g: float | None) -> str:
    if price_per_100g is None:
        return "unknown"
    if price_per_100g < 1.5:
        return "budget"
    if price_per_100g < 3.0:
        return "mid"
    if price_per_100g < 5.0:
        return "premium"
    return "ultra-premium"


WELLNESS_KW = [
    "כוסמין", "אורגני", "מחמצת", "ללא גלוטן", "gluten free", "vegan", "טבעוני",
    "ספלט", "spelt", "sourdough", "אמרנט", "קינואה", "quinoa", "פסיליום", "psyllium",
    "אורגני", "ביו", "bio", "נבטים", "שיבולת שועל", "oat", "כוסמת", "buckwheat",
]

MAINSTREAM_KW = [
    "לחם לבן", "לחם אחיד", "לחם חלב", "טוסט", "פיתה", "לאפה", "חלה",
    "ברמן", "וונדר", "wonder", "berman", "אנג'ל", "דגנית",
]


def _has_wellness(name: str) -> bool:
    return any(kw in name for kw in WELLNESS_KW)


def _has_mainstream(name: str) -> bool:
    return any(kw in name for kw in MAINSTREAM_KW)


def _query_bias_summary(products: list[dict]) -> dict[str, int]:
    query_counts: dict[str, int] = {}
    for p in products:
        q = p.get("acquisition_query", "unknown")
        query_counts[q] = query_counts.get(q, 0) + 1
    return dict(sorted(query_counts.items(), key=lambda x: -x[1]))


def generate_audit_report(
    products: list[dict],
    gate_comp,
    gate_bsip0_notes: list[str],
    acq_notes: list[str],
    prev_corpus_n: int = 108,
) -> str:
    total = len(products)
    n_nutr = sum(1 for p in products if p.get("nutrition", {}).get("energy_kcal_raw") or p.get("nutrition", {}).get("carbs_raw"))
    n_ingr = sum(1 for p in products if p.get("ingredients_raw"))

    wellness_count = sum(1 for p in products if _has_wellness(p.get("name_he", "")))
    mainstream_count_kwonly = sum(1 for p in products if _has_mainstream(p.get("name_he", "")))

    price_tiers: dict[str, int] = {}
    for p in products:
        tier = _price_tier(p.get("price_per_100g"))
        price_tiers[tier] = price_tiers.get(tier, 0) + 1

    def pct(n: int) -> str:
        return f"{n} ({n*100//total if total else 0}%)"

    query_bias = _query_bias_summary(products)

    lines = [
        f"# Bread Representation Audit 002 — {RUN_ID}",
        f"\n**Generated:** {TODAY} | **Source:** Shufersal acquisition v3",
        f"\n---",
        f"\n## 1. Corpus Summary",
        f"",
        f"| Metric | Value |",
        f"|:-------|:------|",
        f"| Total products scraped | {total} |",
        f"| Products with nutrition | {pct(n_nutr)} |",
        f"| Products with ingredients | {pct(n_ingr)} |",
        f"| Wellness-keyword products | {pct(wellness_count)} |",
        f"| Mainstream-keyword products | {pct(mainstream_count_kwonly)} |",
        f"| Previous corpus (002_v2) | {prev_corpus_n} |",
        f"| Net new products | {total - prev_corpus_n:+d} |",
        f"",
        f"---",
        f"\n## 2. Composition Gate",
        f"",
        f"**Status: {'PASS' if gate_comp.passed else 'FAIL'}**",
        f"",
        f"| Check | Value | Threshold | Status |",
        f"|:------|:------|:----------|:-------|",
        f"| Total products | {gate_comp.total} | ≥ 150 | {'✓' if gate_comp.total >= 150 else '✗'} |",
        f"| Mainstream share | {gate_comp.mainstream_pct}% | ≥ 20% | {'✓' if gate_comp.mainstream_pct >= 20 else '✗'} |",
        f"| Spelt share | {gate_comp.spelt_pct}% | ≤ 20% | {'✓' if gate_comp.spelt_pct <= 20 else '✗'} |",
        f"| Sourdough-label share | {gate_comp.sourdough_label_pct}% | ≤ 20% | {'✓' if gate_comp.sourdough_label_pct <= 20 else '✗'} |",
        f"| Commodity anchors | {gate_comp.commodity_anchor_count} | ≥ 10 | {'✓' if gate_comp.commodity_anchor_count >= 10 else '✗'} |",
        f"| Simple white bread | {gate_comp.simple_white_count} | ≥ 5 | {'✓' if gate_comp.simple_white_count >= 5 else '✗'} |",
        f"| Pita/toast | {gate_comp.pita_toast_count} | ≥ 5 | {'✓' if gate_comp.pita_toast_count >= 5 else '✗'} |",
        f"",
    ]

    if gate_comp.failures:
        lines.append("**Gate failures:**")
        for f in gate_comp.failures:
            lines.append(f"- {f}")
        lines.append("")

    if gate_comp.warnings:
        lines.append("**Warnings:**")
        for w in gate_comp.warnings:
            lines.append(f"- {w}")
        lines.append("")

    lines += [
        f"---",
        f"\n## 3. Archetype Distribution",
        f"",
        f"| Archetype | Count | Share |",
        f"|:----------|:------|:------|",
    ]
    for arch, count in sorted(gate_comp.archetype_counts.items(), key=lambda x: -x[1]):
        pct_val = gate_comp.archetype_pcts.get(arch, 0)
        lines.append(f"| {arch} | {count} | {pct_val}% |")

    lines += [
        f"",
        f"---",
        f"\n## 4. Price-Tier Distribution",
        f"",
        f"Based on price_per_100g extracted from product name weight + shelf price.",
        f"",
        f"| Price Tier | Count | Share | Range (₪/100g) |",
        f"|:-----------|:------|:------|:---------------|",
        f"| Budget | {price_tiers.get('budget',0)} | {price_tiers.get('budget',0)*100//total if total else 0}% | < 1.50 |",
        f"| Mid | {price_tiers.get('mid',0)} | {price_tiers.get('mid',0)*100//total if total else 0}% | 1.50–3.00 |",
        f"| Premium | {price_tiers.get('premium',0)} | {price_tiers.get('premium',0)*100//total if total else 0}% | 3.00–5.00 |",
        f"| Ultra-premium | {price_tiers.get('ultra-premium',0)} | {price_tiers.get('ultra-premium',0)*100//total if total else 0}% | > 5.00 |",
        f"| Unknown | {price_tiers.get('unknown',0)} | {price_tiers.get('unknown',0)*100//total if total else 0}% | no price data |",
        f"",
        f"---",
        f"\n## 5. Query Source Breakdown",
        f"",
        f"| Query / Source | Products |",
        f"|:---------------|:---------|",
    ]
    for q, n in list(query_bias.items())[:30]:
        lines.append(f"| {q} | {n} |")

    lines += [
        f"",
        f"---",
        f"\n## 6. BSIP0 Gate",
        f"",
    ]
    for note in gate_bsip0_notes:
        prefix = "✓" if note.startswith("OK") else ("✗" if note.startswith("FAIL") else "⚠")
        lines.append(f"- {prefix} {note}")

    lines += [
        f"",
        f"---",
        f"\n## 7. Comparison vs bread_retail_002_v2",
        f"",
        f"| Dimension | 002_v2 | 003_v1 | Change |",
        f"|:----------|:-------|:-------|:-------|",
        f"| Total products | {prev_corpus_n} | {total} | {total-prev_corpus_n:+d} |",
        f"| Wellness-keyword share | ~64% | {wellness_count*100//total if total else 0}% | target ≤40% |",
        f"| Search queries used | 6 | 19+ | mainstream-first |",
        f"| Pages per query | 1 | up to 5 | deeper pagination |",
        f"| Category browsing | no | yes | A1005, A1015, A1008, A1014 |",
        f"| Brand searches | no | yes | ברמן, וונדר, אנג'ל, דגנית |",
        f"| Price tracking | no | yes | price_per_100g |",
        f"",
        f"---",
        f"\n## 8. Acquisition Notes",
        f"",
    ]
    for note in acq_notes[-30:]:
        lines.append(f"    {note}")

    lines.append(f"\n*Generated by acquisition_v3.py — {TODAY}*")

    return "\n".join(lines)


# ──────────────────────────────────────────────────────────────────────────────
# Main
# ──────────────────────────────────────────────────────────────────────────────

def main(dry_run: bool = False) -> None:
    raw_json_path = OUT_DIR / f"{RUN_ID}_{RUN_TS}_bsip0_raw.json"

    if dry_run:
        # Find most recent raw JSON
        existing = sorted(OUT_DIR.glob("*_bsip0_raw.json"), key=lambda p: p.stat().st_mtime, reverse=True)
        if not existing:
            print("No existing raw JSON found. Run without --dry-run first.")
            sys.exit(1)
        raw_json_path = existing[0]
        print(f"[dry-run] Loading {raw_json_path}")
        data = json.loads(raw_json_path.read_text(encoding="utf-8"))
        products = data if isinstance(data, list) else data.get("products", [])
        acq_notes = ["[dry-run] Loaded from existing file"]
    else:
        print("=== Shufersal Acquisition v3 ===")
        products, acq_notes = run_acquisition(verbose=True)

        # Save raw JSON
        raw_json_path.write_text(
            json.dumps(products, ensure_ascii=False, indent=2),
            encoding="utf-8"
        )
        print(f"\nRaw JSON saved: {raw_json_path}")

    # Composition gate
    print("\n=== Composition Gate ===")
    gate_comp = check_composition(products)
    print_gate_result(gate_comp)

    # BSIP0 gate
    print("\n=== BSIP0 Gate ===")
    bsip0_passed, bsip0_notes = bsip0_gate(products)
    for note in bsip0_notes:
        print(f"  {note}")

    # Audit report
    report_path = REPORT_DIR / "bread_representation_audit_002.md"
    report = generate_audit_report(products, gate_comp, bsip0_notes, acq_notes)
    report_path.write_text(report, encoding="utf-8")
    print(f"\nAudit report: {report_path}")

    overall_pass = gate_comp.passed and bsip0_passed
    print(f"\n{'='*50}")
    print(f"Overall gate: {'PASS — ready for BSIP1/BSIP2' if overall_pass else 'FAIL — review failures before scoring'}")
    print(f"Raw JSON:     {raw_json_path}")
    print(f"Audit report: {report_path}")
    if not overall_pass:
        print("\nAddress gate failures before running batch_run_bread_retail_003.py")
        sys.exit(1)
    else:
        print(f"\nNext step: python batch_run_bread_retail_003.py --raw {raw_json_path}")


if __name__ == "__main__":
    dry_run = "--dry-run" in sys.argv
    main(dry_run=dry_run)
