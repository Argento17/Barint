"""
Bari Category Factory — Traceability Validator
Implements: TRC-002 (BSIP0 backlink) + CAN-004 (exclusion leak)

TRC-002: Every canonical bsip1_{barcode}.json must have a matching BSIP0
         source file. Shufersal: P_{barcode}.json. Yohananof: {barcode}/ dir.

CAN-004: Products rejected in candidate_review.csv (approved_for_scrape=NO)
         must not appear inside canonical_bsip1/.

Usage:
    python traceability_validator.py --category hummus

Exit codes:
    0 = both checks PASS
    1 = one or both checks FAIL
"""

from __future__ import annotations

import argparse
import csv
import json
import pathlib
import sys
import datetime

sys.stdout.reconfigure(encoding="utf-8", errors="replace")

# ---------------------------------------------------------------------------
# Path resolution — derived from script location, no hardcoded roots
# ---------------------------------------------------------------------------

SCRIPT_DIR  = pathlib.Path(__file__).resolve().parent   # validators/
QA_DIR      = SCRIPT_DIR.parent                         # qa/
OPS_DIR     = QA_DIR.parent                             # 03_operations/
BARI_ROOT   = OPS_DIR.parent                            # C:\Bari\


def build_paths(category: str) -> dict[str, pathlib.Path]:
    products_dir  = BARI_ROOT / "02_products" / category
    bsip0_dir     = products_dir / "observations_bsip0"
    canonical_dir = products_dir / "canonical_bsip1"
    reports_dir   = QA_DIR / "reports"
    return {
        "products_dir":  products_dir,
        "bsip0_dir":     bsip0_dir,
        "canonical_dir": canonical_dir,
        "reports_dir":   reports_dir,
    }


# ---------------------------------------------------------------------------
# BSIP0 source lookup — supports Shufersal, Yohananof, and legacy layouts
# ---------------------------------------------------------------------------

def find_bsip0_source(barcode: str, bsip0_dir: pathlib.Path) -> tuple[bool, str | None]:
    """
    Return (found, location_label) for a barcode in any known BSIP0 layout.

    Checked in order:
      1. Shufersal retailer subdir  — observations_bsip0/shufersal/P_{barcode}.json
      2. Yohananof retailer subdir  — observations_bsip0/yohananof/{barcode}/
      3. Legacy flat Yohananof      — observations_bsip0/{barcode}/
      4. Legacy flat Shufersal      — observations_bsip0/P_{barcode}.json
    """
    # 1 — Shufersal (new factory layout)
    shufersal_file = bsip0_dir / "shufersal" / f"P_{barcode}.json"
    if shufersal_file.exists():
        return True, f"shufersal/P_{barcode}.json"

    # 2 — Yohananof (new factory layout)
    yohananof_dir = bsip0_dir / "yohananof" / barcode
    if yohananof_dir.is_dir():
        return True, f"yohananof/{barcode}/"

    # 3 — Legacy: barcode directory directly in observations_bsip0/
    legacy_dir = bsip0_dir / barcode
    if legacy_dir.is_dir():
        return True, f"(legacy){barcode}/"

    # 4 — Legacy: P_{barcode}.json directly in observations_bsip0/
    legacy_file = bsip0_dir / f"P_{barcode}.json"
    if legacy_file.exists():
        return True, f"(legacy)P_{barcode}.json"

    return False, None


# ---------------------------------------------------------------------------
# TRC-002
# ---------------------------------------------------------------------------

def check_trc002(canonical_dir: pathlib.Path, bsip0_dir: pathlib.Path) -> dict:
    """
    For every bsip1_{barcode}.json in canonical_bsip1/,
    confirm a matching BSIP0 observation exists.
    """
    result: dict = {
        "check_id": "TRC-002",
        "description": "Every canonical BSIP1 file traces back to a BSIP0 source",
        "total_checked": 0,
        "matched": 0,
        "unmatched": 0,
        "unmatched_detail": [],  # list of {barcode, canonical_file}
        "pass": False,
    }

    bsip1_files = sorted(canonical_dir.glob("bsip1_*.json"))
    result["total_checked"] = len(bsip1_files)

    if result["total_checked"] == 0:
        result["error"] = f"No bsip1_*.json files found in {canonical_dir}"
        return result

    for f in bsip1_files:
        # Filename pattern: bsip1_{barcode}.json
        barcode = f.stem[len("bsip1_"):]
        found, location = find_bsip0_source(barcode, bsip0_dir)
        if found:
            result["matched"] += 1
        else:
            result["unmatched"] += 1
            result["unmatched_detail"].append({
                "barcode":        barcode,
                "canonical_file": f.name,
            })

    result["pass"] = result["unmatched"] == 0
    return result


# ---------------------------------------------------------------------------
# CAN-004
# ---------------------------------------------------------------------------

def _collect_rejected_codes(bsip0_dir: pathlib.Path) -> list[dict]:
    """
    Walk all candidate_review.csv files under bsip0_dir and collect rows
    where approved_for_scrape == 'NO'.
    Returns list of dicts with keys: code, barcode, name, retailer, csv_path.
    """
    rejected: list[dict] = []

    csv_files = list(bsip0_dir.rglob("candidate_review.csv"))
    if not csv_files:
        return rejected

    for csv_path in csv_files:
        # Retailer label: parent dir name if it's a known retailer subdir
        parent = csv_path.parent
        retailer = parent.name if parent != bsip0_dir else "unknown"

        try:
            with csv_path.open(encoding="utf-8-sig", newline="") as fh:
                reader = csv.DictReader(fh)
                for row in reader:
                    if row.get("approved_for_scrape", "").strip().upper() != "NO":
                        continue
                    code = (row.get("code") or "").strip()
                    if not code:
                        continue
                    # Shufersal codes are P_{barcode}; strip the prefix
                    barcode = code[2:] if code.startswith("P_") else code
                    rejected.append({
                        "code":     code,
                        "barcode":  barcode,
                        "name":     (row.get("name") or "").strip(),
                        "retailer": retailer,
                        "csv_path": str(csv_path),
                    })
        except Exception as exc:
            print(f"  [WARN] Could not read {csv_path}: {exc}", file=sys.stderr)

    return rejected


def check_can004(canonical_dir: pathlib.Path, bsip0_dir: pathlib.Path) -> dict:
    """
    Load all candidate_review.csv files and confirm no rejected product
    (approved_for_scrape=NO) has a bsip1_{barcode}.json in canonical_bsip1/.
    """
    result: dict = {
        "check_id": "CAN-004",
        "description": "No excluded products appear inside canonical_bsip1/",
        "csv_files_scanned": 0,
        "rejected_checked": 0,
        "leaked": 0,
        "leaked_detail": [],  # list of {barcode, name, retailer, canonical_file}
        "pass": False,
    }

    csv_files = list(bsip0_dir.rglob("candidate_review.csv"))
    result["csv_files_scanned"] = len(csv_files)

    if not csv_files:
        # No candidate_review.csv at all — cannot perform check
        result["error"] = (
            f"No candidate_review.csv found under {bsip0_dir}. "
            "Cannot verify exclusion integrity."
        )
        result["pass"] = False
        return result

    rejected = _collect_rejected_codes(bsip0_dir)
    result["rejected_checked"] = len(rejected)

    for item in rejected:
        barcode          = item["barcode"]
        canonical_file   = canonical_dir / f"bsip1_{barcode}.json"
        if canonical_file.exists():
            result["leaked"] += 1
            result["leaked_detail"].append({
                "barcode":        barcode,
                "name":           item["name"],
                "retailer":       item["retailer"],
                "canonical_file": canonical_file.name,
            })

    result["pass"] = result["leaked"] == 0
    return result


# ---------------------------------------------------------------------------
# Report writer
# ---------------------------------------------------------------------------

def _verdict(passed: bool) -> str:
    return "PASS ✅" if passed else "FAIL ❌"


def write_report(
    category:    str,
    trc002:      dict,
    can004:      dict,
    overall:     bool,
    reports_dir: pathlib.Path,
) -> pathlib.Path:
    reports_dir.mkdir(parents=True, exist_ok=True)
    report_path = reports_dir / f"traceability_report_{category}.md"

    ts    = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    lines = [
        f"# Bari Traceability Validation Report — {category}",
        f"",
        f"**Generated:** {ts}  ",
        f"**Category:** {category}  ",
        f"**Overall verdict:** {_verdict(overall)}",
        f"",
        f"---",
        f"",
        f"## TRC-002 — BSIP0 Backlink Check",
        f"",
        f"> Every canonical `bsip1_{{barcode}}.json` must have a matching BSIP0 source.",
        f"",
        f"| Metric | Value |",
        f"|--------|-------|",
        f"| Verdict | **{_verdict(trc002['pass'])}** |",
        f"| Total BSIP1 files checked | {trc002['total_checked']} |",
        f"| Matched to BSIP0 source | {trc002['matched']} |",
        f"| Unmatched (no BSIP0 found) | {trc002['unmatched']} |",
    ]

    if trc002.get("error"):
        lines += [
            f"",
            f"**Error:** {trc002['error']}",
        ]
    elif trc002["unmatched"] > 0:
        lines += [
            f"",
            f"### Unmatched products — no BSIP0 source found",
            f"",
            f"| Barcode | Canonical file |",
            f"|---------|----------------|",
        ]
        for item in trc002["unmatched_detail"]:
            lines.append(f"| `{item['barcode']}` | `{item['canonical_file']}` |")
        lines += [
            f"",
            f"**Action required:** Investigate each unmatched barcode.",
            f"- If the product was scraped, the BSIP0 source file may have been moved or renamed.",
            f"- If the product was not scraped, the BSIP1 file was introduced without a BSIP0 source — remove it from `canonical_bsip1/` and re-run.",
        ]
    else:
        lines += [
            f"",
            f"All {trc002['matched']} BSIP1 files have a confirmed BSIP0 source.",
        ]

    lines += [
        f"",
        f"---",
        f"",
        f"## CAN-004 — Exclusion Leak Check",
        f"",
        f"> Products rejected in `candidate_review.csv` must not appear in `canonical_bsip1/`.",
        f"",
        f"| Metric | Value |",
        f"|--------|-------|",
        f"| Verdict | **{_verdict(can004['pass'])}** |",
        f"| CSV files scanned | {can004['csv_files_scanned']} |",
        f"| Rejected products checked | {can004['rejected_checked']} |",
        f"| Leaked into canonical | {can004['leaked']} |",
    ]

    if can004.get("error"):
        lines += [
            f"",
            f"**Error:** {can004['error']}",
        ]
    elif can004["leaked"] > 0:
        lines += [
            f"",
            f"### Leaked products — rejected but found in canonical_bsip1/",
            f"",
            f"| Barcode | Product name | Source retailer | Canonical file |",
            f"|---------|-------------|-----------------|----------------|",
        ]
        for item in can004["leaked_detail"]:
            lines.append(
                f"| `{item['barcode']}` | {item['name']} "
                f"| {item['retailer']} | `{item['canonical_file']}` |"
            )
        lines += [
            f"",
            f"**Action required:** Remove each leaked file from `canonical_bsip1/`.",
            f"These products were explicitly excluded in `candidate_review.csv`.",
            f"Investigate how they entered the canonical corpus before removing.",
        ]
    else:
        lines += [
            f"",
            f"All {can004['rejected_checked']} rejected products are absent from `canonical_bsip1/`.",
        ]

    lines += [
        f"",
        f"---",
        f"",
        f"## Summary",
        f"",
        f"| Check | Verdict | Key metric |",
        f"|-------|---------|------------|",
        f"| TRC-002 — BSIP0 backlink | {_verdict(trc002['pass'])} "
        f"| {trc002['matched']}/{trc002['total_checked']} matched |",
        f"| CAN-004 — Exclusion leak | {_verdict(can004['pass'])} "
        f"| {can004['leaked']} leaked / {can004['rejected_checked']} rejected |",
        f"",
        f"**Overall: {_verdict(overall)}**",
        f"",
    ]

    if overall:
        lines.append(
            f"Category `{category}` passed both traceability checks. "
            f"Clear to proceed to BSIP2."
        )
    else:
        lines += [
            f"Category `{category}` has open traceability failures.",
            f"**Do not proceed to BSIP2 until all FAIL checks are resolved.**",
        ]

    lines += [
        f"",
        f"---",
        f"",
        f"*Bari Traceability Validator v1 — "
        f"[TRC-002 + CAN-004 per category_factory_qa_v1.md]*",
    ]

    report_path.write_text("\n".join(lines), encoding="utf-8")
    return report_path


# ---------------------------------------------------------------------------
# Setup validation
# ---------------------------------------------------------------------------

def validate_setup(paths: dict, category: str) -> list[str]:
    """Return a list of fatal setup errors. Empty list = safe to proceed."""
    errors: list[str] = []

    if not paths["products_dir"].exists():
        errors.append(
            f"Product directory not found: {paths['products_dir']}\n"
            f"  Available categories: "
            + ", ".join(
                d.name for d in (BARI_ROOT / "02_products").iterdir()
                if d.is_dir() and not d.name.startswith(".")
            )
        )

    if not paths["canonical_dir"].exists():
        errors.append(
            f"canonical_bsip1/ not found: {paths['canonical_dir']}\n"
            f"  BSIP1 enrichment may not have run yet for this category."
        )

    if not paths["bsip0_dir"].exists():
        errors.append(
            f"observations_bsip0/ not found: {paths['bsip0_dir']}\n"
            f"  BSIP0 scrape may not have run yet for this category."
        )

    return errors


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def main() -> int:
    parser = argparse.ArgumentParser(
        description=(
            "Bari Category Factory — Traceability Validator\n"
            "Checks TRC-002 (BSIP0 backlink) and CAN-004 (exclusion leak)."
        ),
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    parser.add_argument(
        "--category",
        required=True,
        metavar="CATEGORY",
        help=(
            "Category name matching the directory under 02_products/. "
            "Example: hummus"
        ),
    )
    parser.add_argument(
        "--report-only",
        action="store_true",
        help="Write report but always exit 0 (useful for CI observation runs).",
    )
    args = parser.parse_args()

    category = args.category.strip().lower()
    paths    = build_paths(category)

    # --- Setup checks (before any banner so output order is clean) ---
    setup_errors = validate_setup(paths, category)

    print(f"\n=== Bari Traceability Validator ===")
    print(f"Category : {category}")
    print(f"BARI_ROOT: {BARI_ROOT}")
    print()

    if setup_errors:
        for err in setup_errors:
            print(f"[SETUP ERROR] {err}")
        return 1

    print(f"Paths resolved:")
    print(f"  canonical_bsip1 : {paths['canonical_dir']}")
    print(f"  observations_bsip0: {paths['bsip0_dir']}")
    print(f"  report output   : {paths['reports_dir']}")
    print()

    # --- TRC-002 ---
    print("Running TRC-002 — BSIP0 backlink check...")
    trc002 = check_trc002(paths["canonical_dir"], paths["bsip0_dir"])

    print(f"  Total BSIP1 files : {trc002['total_checked']}")
    print(f"  Matched to BSIP0  : {trc002['matched']}")
    print(f"  Unmatched         : {trc002['unmatched']}")

    if trc002.get("error"):
        print(f"  [ERROR] {trc002['error']}", file=sys.stderr)
    elif trc002["unmatched_detail"]:
        print("  Unmatched barcodes:")
        for item in trc002["unmatched_detail"]:
            print(f"    ✗ {item['barcode']}  ({item['canonical_file']})")

    trc002_label = "PASS ✅" if trc002["pass"] else "FAIL ❌"
    print(f"  TRC-002: {trc002_label}")
    print()

    # --- CAN-004 ---
    print("Running CAN-004 — exclusion leak check...")
    can004 = check_can004(paths["canonical_dir"], paths["bsip0_dir"])

    print(f"  CSV files scanned        : {can004['csv_files_scanned']}")
    print(f"  Rejected products checked: {can004['rejected_checked']}")
    print(f"  Leaked into canonical    : {can004['leaked']}")

    if can004.get("error"):
        print(f"  [ERROR] {can004['error']}", file=sys.stderr)
    elif can004["leaked_detail"]:
        print("  Leaked products:")
        for item in can004["leaked_detail"]:
            print(f"    ✗ {item['barcode']}  {item['name']}  ({item['retailer']})")

    can004_label = "PASS ✅" if can004["pass"] else "FAIL ❌"
    print(f"  CAN-004: {can004_label}")
    print()

    # --- Overall verdict ---
    overall = trc002["pass"] and can004["pass"]
    overall_label = "PASS ✅" if overall else "FAIL ❌"
    print(f"Overall verdict: {overall_label}")
    print()

    # --- Write report ---
    report_path = write_report(
        category    = category,
        trc002      = trc002,
        can004      = can004,
        overall     = overall,
        reports_dir = paths["reports_dir"],
    )
    print(f"Report written: {report_path}")

    if args.report_only:
        return 0
    return 0 if overall else 1


if __name__ == "__main__":
    sys.exit(main())
