"""
BSIP0 Acquisition Audit v2 — Browser Automation Orchestrator

Runs all retailer probes, applies acceptance gate, generates reports.
All output -> C:/Bari/02_products/bread_retail_002/

Usage:
    python acquisition_audit_v2.py
    python acquisition_audit_v2.py --retailers shufersal,victory
    python acquisition_audit_v2.py --skip-browser  # static-only probes
"""

from __future__ import annotations

import argparse
import json
import sys
from datetime import datetime

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
from pathlib import Path

from retailer_base import RetailProbeResult, RawProduct

OUTPUT_DIR = Path(r"C:\Bari\02_products\bread_retail_002")
SRC_DIR = Path(__file__).parent

# Acceptance gate thresholds
GATE_MIN_PRODUCTS = 20
GATE_NUTRITION_PCT = 0.70
GATE_INGREDIENT_PCT = 0.40
GATE_MIN_RETAILERS = 1   # at least one real retailer (not OFF)

RUN_ID = f"real_bread_retail_002_v2_{datetime.utcnow().strftime('%Y%m%dT%H%M%S')}"
RUN_DATE = datetime.utcnow().isoformat()


# ---------------------------------------------------------------------------
# Probe runner

def run_probes(retailer_ids: list[str] | None = None, skip_browser: bool = False) -> list[RetailProbeResult]:
    sys.path.insert(0, str(SRC_DIR))

    probe_modules = [
        ("shufersal", "shufersal_probe", "ShufersalProbe"),
        ("victory",   "victory_probe",   "VictoryProbe"),
        ("carrefour", "carrefour_probe", "CarrefourProbe"),
        ("wolt_market", "wolt_probe",    "WoltProbe"),
    ]

    results: list[RetailProbeResult] = []
    for rid, module_name, class_name in probe_modules:
        if retailer_ids and rid not in retailer_ids:
            print(f"[skip] {rid}")
            continue

        try:
            mod = __import__(module_name)
            cls = getattr(mod, class_name)
            probe = cls()
            if skip_browser and probe.requires_browser:
                print(f"[skip-browser] {rid}")
                continue
            print(f"[run] {rid}...")
            result = probe.probe()
            print(
                f"  → {result.access_status} | {result.n_products()} products"
                + (f" | BLOCKER: {result.blocker_type}" if result.blocker_type else "")
            )
            results.append(result)
        except Exception as exc:
            print(f"[ERROR] {rid}: {exc}")
            from retailer_base import RetailProbeResult
            err = RetailProbeResult(
                retailer_id=rid,
                retailer_name=rid,
                access_status="failed",
                blocker_type="probe_exception",
                blocker_detail=str(exc),
            )
            err.probe_notes.append(f"Probe module failed to load or run: {exc}")
            results.append(err)
    return results


# ---------------------------------------------------------------------------
# Acceptance gate

def apply_gate(products: list[RawProduct]) -> dict:
    n = len(products)
    if n == 0:
        return {
            "passed": False,
            "reason": "zero_products — no real retailer bread/cracker products extracted",
            "n_products": 0,
            "nutrition_pct": 0.0,
            "ingredient_pct": 0.0,
            "retailers_with_products": [],
        }

    n_nutrition = sum(1 for p in products if p.has_nutrition())
    n_ingredients = sum(1 for p in products if p.has_ingredients())
    retailers_with_products = list({p.retailer_id for p in products})

    nutrition_pct = n_nutrition / n
    ingredient_pct = n_ingredients / n

    failures = []
    if n < GATE_MIN_PRODUCTS:
        failures.append(
            f"too_few_products: {n} < {GATE_MIN_PRODUCTS} required"
        )
    if nutrition_pct < GATE_NUTRITION_PCT:
        failures.append(
            f"low_nutrition_coverage: {nutrition_pct:.0%} < {GATE_NUTRITION_PCT:.0%} required"
        )
    if ingredient_pct < GATE_INGREDIENT_PCT:
        failures.append(
            f"low_ingredient_coverage: {ingredient_pct:.0%} < {GATE_INGREDIENT_PCT:.0%} required"
        )
    if len(retailers_with_products) < GATE_MIN_RETAILERS:
        failures.append(
            f"insufficient_retailers: {len(retailers_with_products)} < {GATE_MIN_RETAILERS} required"
        )

    return {
        "passed": len(failures) == 0,
        "reason": "; ".join(failures) if failures else "all criteria met",
        "n_products": n,
        "n_nutrition": n_nutrition,
        "n_ingredients": n_ingredients,
        "nutrition_pct": round(nutrition_pct, 3),
        "ingredient_pct": round(ingredient_pct, 3),
        "retailers_with_products": retailers_with_products,
        "failures": failures,
    }


# ---------------------------------------------------------------------------
# Report generators

def _blocker_label(result: RetailProbeResult) -> str:
    labels = {
        "maintenance_mode":  "IN MAINTENANCE — HTTP 200 with maintenance placeholder",
        "http_403":          "BLOCKED — HTTP 403 / browser also blocked",
        "angularjs_spa":     "BLOCKED (JS) — AngularJS SPA, browser rendered but no products",
        "auth_required":     "PARTIAL — requires authentication/session cookie",
        "timeout":           "FAILED — connection timeout",
        "browser_crash":     "FAILED — browser session crashed",
        "probe_exception":   "FAILED — probe module error",
        "api_no_products":   "API accessible but returned no products",
        "":                  "OK",
    }
    return labels.get(result.blocker_type, result.blocker_type)


def generate_main_audit(results: list[RetailProbeResult], gate: dict, all_products: list[RawProduct]) -> str:
    gate_status = "PASSED ✓" if gate["passed"] else "FAILED ✗"
    lines = [
        "# BSIP0 Acquisition Audit v2",
        f"",
        f"**Run:** `{RUN_ID}` | **Date:** {RUN_DATE[:10]} | **Method:** Playwright browser automation",
        f"",
        "This audit documents all browser-based retailer access attempts and the BSIP0 acceptance gate result.",
        "No products are added to the corpus until the gate passes.",
        "",
        "---",
        "",
        "## 1. Gate Result",
        "",
        f"**Status: {gate_status}**",
        "",
    ]
    if gate["passed"]:
        lines.append(f"Products collected: {gate['n_products']} (gate: ≥{GATE_MIN_PRODUCTS})")
        lines.append(f"Nutrition coverage: {gate['nutrition_pct']:.0%} (gate: ≥{GATE_NUTRITION_PCT:.0%})")
        lines.append(f"Ingredient coverage: {gate['ingredient_pct']:.0%} (gate: ≥{GATE_INGREDIENT_PCT:.0%})")
        lines.append(f"Retailers: {', '.join(gate['retailers_with_products'])}")
        lines.append("")
        lines.append("**Proceed to BSIP1/BSIP2 pipeline.**")
    else:
        lines.append(f"Reason: {gate['reason']}")
        lines.append("")
        lines.append("**Do NOT proceed to BSIP1/BSIP2 pipeline.**")
        lines.append("The corpus does not meet minimum acceptance criteria.")
        lines.append(f"Products collected: {gate['n_products']} (need {GATE_MIN_PRODUCTS})")

    lines += [
        "",
        "---",
        "",
        "## 2. Retailer Access Summary (v2 — Browser Automation)",
        "",
        "| Retailer | Access Method | Status | Blocker | Products | Manual Action? |",
        "|:---------|:-------------|:-------|:--------|:---------|:--------------|",
    ]
    for r in results:
        manual = "YES — see report" if r.requires_manual_action else "No"
        lines.append(
            f"| {r.retailer_name} | {r.access_method} | {r.access_status} "
            f"| {_blocker_label(r)} | {r.n_products()} | {manual} |"
        )

    lines += [
        "",
        "---",
        "",
        "## 3. Retailer-by-Retailer Findings",
        "",
    ]
    for r in results:
        lines.append(f"### {r.retailer_name}")
        lines.append("")
        lines.append(f"**Status:** {_blocker_label(r)}")
        lines.append(f"**Products extracted:** {r.n_products()}")
        if r.blocker_detail:
            lines.append(f"**Blocker detail:** {r.blocker_detail}")
        if r.requires_manual_action:
            lines.append(f"**MANUAL ACTION REQUIRED:** {r.manual_action_description}")
        if r.probe_notes:
            lines.append("")
            lines.append("**Probe log:**")
            for note in r.probe_notes:
                lines.append(f"- {note}")
        if r.screenshots:
            lines.append("")
            lines.append("**Screenshots:**")
            for ss in r.screenshots:
                lines.append(f"- `{ss}`")
        lines.append("")

    lines += [
        "---",
        "",
        "## 4. Products Extracted",
        "",
        f"Total: {len(all_products)}",
        "",
    ]
    if all_products:
        lines.append("| # | Name | Retailer | Nutrition | Ingredients | Source URL |")
        lines.append("|:--|:-----|:---------|:----------|:------------|:-----------|")
        for i, p in enumerate(all_products, 1):
            nutr = "✓" if p.has_nutrition() else "✗"
            ingr = "✓" if p.has_ingredients() else "✗"
            url_short = p.source_url[:60] + "…" if len(p.source_url) > 60 else p.source_url
            lines.append(f"| {i} | {p.name_he} | {p.retailer_name} | {nutr} | {ingr} | {url_short} |")
    else:
        lines.append("**No products extracted.**")

    lines += [
        "",
        "---",
        "",
        "## 5. API Endpoints Discovered",
        "",
    ]
    all_api_calls: list[dict] = []
    for r in results:
        all_api_calls.extend(r.captured_api_calls)
    if all_api_calls:
        lines.append(f"{len(all_api_calls)} API calls captured across all retailers.")
        lines.append("See `discovered_api_endpoints.json` for full details.")
    else:
        lines.append("No XHR/API calls captured.")

    lines += [
        "",
        "---",
        "",
        "## 6. Manual Actions Required",
        "",
    ]
    manual_retailers = [r for r in results if r.requires_manual_action]
    if manual_retailers:
        for r in manual_retailers:
            lines.append(f"### {r.retailer_name}")
            lines.append(f"{r.manual_action_description}")
            lines.append("")
    else:
        lines.append("No manual actions required.")

    lines += [
        "",
        "---",
        "",
        "## 7. Recommended Next Steps",
        "",
    ]
    blocked = [r for r in results if r.access_status in ("blocked", "failed")]
    partial = [r for r in results if r.access_status == "partial"]
    accessible = [r for r in results if r.access_status == "accessible"]

    if accessible:
        lines.append(f"**Accessible ({len(accessible)}):** {', '.join(r.retailer_name for r in accessible)}")
        lines.append("→ Proceed with these retailers to BSIP1.")
    if partial:
        lines.append(f"**Partial ({len(partial)}):** {', '.join(r.retailer_name for r in partial)}")
        lines.append("→ Requires session cookies or manual login to unlock product catalog.")
    if blocked:
        lines.append(f"**Blocked ({len(blocked)}):** {', '.join(r.retailer_name for r in blocked)}")
        lines.append("→ Need direct API credentials, proxy rotation, or partnership.")

    lines.append("")
    lines.append(f"*Generated by acquisition_audit_v2.py — {RUN_DATE}*")
    return "\n".join(lines)


def generate_access_matrix(results: list[RetailProbeResult]) -> str:
    lines = [
        "# Retailer Access Matrix v2",
        "",
        f"**Generated:** {RUN_DATE[:10]} | **Method:** Playwright browser automation",
        "",
        "| Retailer | Static HTTP | Browser | Products | Blocker | Manual? |",
        "|:---------|:-----------|:--------|:---------|:--------|:--------|",
    ]
    for r in results:
        static = "✗ blocked" if r.blocker_type in ("http_403", "maintenance_mode") else "?"
        browser = "✓" if r.access_status == "accessible" else ("~" if r.access_status == "partial" else "✗")
        manual = "YES" if r.requires_manual_action else "No"
        lines.append(
            f"| {r.retailer_name} | {static} | {browser} | {r.n_products()} | {r.blocker_type or 'none'} | {manual} |"
        )
    return "\n".join(lines)


def generate_session_inventory(results: list[RetailProbeResult]) -> str:
    lines = [
        "# Session State Inventory",
        "",
        f"**Generated:** {RUN_DATE}",
        "",
        "Documents cookie/session state for each retailer after browser probe.",
        "",
    ]
    for r in results:
        lines.append(f"## {r.retailer_name}")
        lines.append(f"- Access status: {r.access_status}")
        lines.append(f"- Session dir: `acquisition_v2/sessions/{r.retailer_id}/`")
        lines.append(f"- Screenshots: {len(r.screenshots)} saved")
        if r.requires_manual_action:
            lines.append(f"- **Manual action needed:** {r.manual_action_description}")
        lines.append("")
    return "\n".join(lines)


def generate_retailer_report(result: RetailProbeResult) -> str:
    lines = [
        f"# {result.retailer_name} — Probe Report",
        "",
        f"**Generated:** {RUN_DATE}",
        f"**Access method:** {result.access_method}",
        f"**Status:** {result.access_status}",
        f"**Blocker:** {result.blocker_type or 'none'}",
        "",
    ]
    if result.blocker_detail:
        lines += ["**Detail:**", result.blocker_detail, ""]
    if result.requires_manual_action:
        lines += [
            "## Manual Action Required",
            result.manual_action_description,
            "",
        ]
    lines.append("## Probe Log")
    for note in result.probe_notes:
        lines.append(f"- {note}")
    lines.append("")
    lines.append(f"## Products ({result.n_products()})")
    if result.products:
        for p in result.products:
            lines.append(
                f"- {p.name_he} | {p.barcode} | nutrition={p.has_nutrition()} | ingredients={p.has_ingredients()}"
            )
    else:
        lines.append("No products extracted.")
    lines.append("")
    lines.append("## Screenshots")
    for ss in result.screenshots:
        lines.append(f"- `{ss}`")
    return "\n".join(lines)


def generate_source_manifest(results: list[RetailProbeResult], gate: dict, all_products: list[RawProduct]) -> dict:
    return {
        "run_id": RUN_ID,
        "run_date": RUN_DATE,
        "gate_passed": gate["passed"],
        "gate_reason": gate["reason"],
        "n_products": len(all_products),
        "acquisition_method": "playwright_browser_v2",
        "retailer_summary": [
            {
                "retailer_id": r.retailer_id,
                "retailer_name": r.retailer_name,
                "access_status": r.access_status,
                "blocker_type": r.blocker_type,
                "n_products": r.n_products(),
                "requires_manual_action": r.requires_manual_action,
            }
            for r in results
        ],
        "products": [p.to_dict() for p in all_products],
    }


# ---------------------------------------------------------------------------
# Main

def main():
    parser = argparse.ArgumentParser(description="BSIP0 Acquisition Audit v2")
    parser.add_argument("--retailers", help="Comma-separated retailer IDs to run")
    parser.add_argument("--skip-browser", action="store_true", help="Skip browser-based probes")
    args = parser.parse_args()

    retailer_ids = [r.strip() for r in args.retailers.split(",")] if args.retailers else None

    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    screenshots_dir = SRC_DIR / "screenshots" / "failure_states"
    screenshots_dir.mkdir(parents=True, exist_ok=True)

    print(f"\n=== BSIP0 Acquisition Audit v2 ===")
    print(f"Run: {RUN_ID}")
    print(f"Output: {OUTPUT_DIR}")
    print()

    # Run probes
    results = run_probes(retailer_ids=retailer_ids, skip_browser=args.skip_browser)

    # Collect all products
    all_products: list[RawProduct] = []
    for r in results:
        all_products.extend(r.products)

    # Gate
    gate = apply_gate(all_products)
    print(f"\nGate: {'PASSED' if gate['passed'] else 'FAILED'} — {gate['reason']}")

    # Write reports
    reports = {
        "bsip0_acquisition_v2_audit.md": generate_main_audit(results, gate, all_products),
        "retailer_access_matrix_v2.md": generate_access_matrix(results),
        "session_state_inventory.md": generate_session_inventory(results),
    }
    for name, content in reports.items():
        path = OUTPUT_DIR / name
        path.write_text(content, encoding="utf-8")
        print(f"[wrote] {path}")

    # Per-retailer reports
    retailer_report_map = {
        "shufersal":   "shufersal_probe_report.md",
        "victory":     "victory_probe_report.md",
        "carrefour":   "carrefour_probe_report.md",
        "wolt_market": "wolt_probe_report.md",
    }
    for r in results:
        fname = retailer_report_map.get(r.retailer_id, f"{r.retailer_id}_probe_report.md")
        path = OUTPUT_DIR / fname
        path.write_text(generate_retailer_report(r), encoding="utf-8")
        print(f"[wrote] {path}")

    # API endpoints JSON
    all_api_calls = []
    for r in results:
        for call in r.captured_api_calls:
            call["retailer_id"] = r.retailer_id
            all_api_calls.append(call)
    api_path = OUTPUT_DIR / "discovered_api_endpoints.json"
    api_path.write_text(
        json.dumps(all_api_calls, ensure_ascii=False, indent=2), encoding="utf-8"
    )
    print(f"[wrote] {api_path}")

    # Source manifest
    manifest = generate_source_manifest(results, gate, all_products)
    manifest_path = OUTPUT_DIR / "bsip0_source_manifest_v2.json"
    manifest_path.write_text(
        json.dumps(manifest, ensure_ascii=False, indent=2), encoding="utf-8"
    )
    print(f"[wrote] {manifest_path}")

    # Raw product JSON (only if gate passed)
    if gate["passed"] and all_products:
        raw_path = OUTPUT_DIR / f"{RUN_ID}_bsip0_raw.json"
        raw_path.write_text(
            json.dumps([p.to_dict() for p in all_products], ensure_ascii=False, indent=2),
            encoding="utf-8",
        )
        print(f"[wrote] {raw_path}")
        print(f"\nGate PASSED — {len(all_products)} products ready for BSIP1/BSIP2")
    else:
        print(f"\nGate FAILED — do NOT proceed to BSIP1/BSIP2")
        print(f"  {gate['reason']}")

    print("\nDone.")


if __name__ == "__main__":
    main()
