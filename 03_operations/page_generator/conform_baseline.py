#!/usr/bin/env python3
"""
conform_baseline.py — read-only per-product DATA contract validator (P268).

Loads each live comparison shelf JSON (the file the page-data layer imports),
checks owner-locked baseline contract rules, and reports violations. Never writes
or mutates shelf data.

Usage:
  python 03_operations/page_generator/conform_baseline.py --all
  python 03_operations/page_generator/conform_baseline.py --shelf snacks

Exit code: 0 = all checked shelves conform; 1 = at least one violation; 3 = usage error.
ASCII-only stdout (Windows cp1252 safe).
"""
from __future__ import annotations

import argparse
import json
import re
import sys
from collections import defaultdict
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

THIS_DIR = Path(__file__).resolve().parent
REPO = THIS_DIR.parents[1]
WEB_DATA = REPO / "bari-web" / "src" / "data" / "comparisons"

# Served JSON per shelf (matches *-page-data.ts imports).
SHELF_FILES: dict[str, str] = {
    "bread": "bread_frontend_v3.json",
    "brined_cheeses": "brined_cheeses_frontend_v2.json",
    "cakes": "cakes_hard_cookies_frontend_v1.json",
    "cereals": "cereals_frontend_v2.json",
    "cheese": "cheese_frontend_v4.json",
    "cookies_coffee": "cookies_coffee_frontend_v2.json",
    "granola": "granola_frontend_v1.json",
    "hard_cheeses": "hard_cheeses_frontend_v2.json",
    "hummus": "hummus_frontend_v5.json",
    "juices": "juices_frontend_v3.json",
    "milk": "milk_frontend_v1.json",
    "snacks": "snacks_frontend_v4.json",
}

REQUIRED_PRODUCT_KEYS = (
    "id",
    "barcode",
    "name",
    "imageUrl",
    "score",
    "grade",
    "rank",
    "categoryTotal",
    "confidence",
    "confidence_label_he",
    "confidence_sub_reason",
    "confidence_tooltip_he",
    "insightLine",
    "rowVerdict",
    "d4_additives",
    "expansion",
)

REQUIRED_EXPANSION_KEYS = (
    "positiveSignals",
    "limitingFactors",
    "nutrition",
    "ingredients",
    "comparisonContext",
    "servingNote",
    "confidenceLabel",
)

FORBIDDEN_PRODUCT_KEYS = frozenset(
    {"bariInterpretation", "consumerTakeaway", "bestUseCases", "caps_applied"}
)

FORBIDDEN_EXPANSION_KEYS = frozenset(
    {"consumerExplanation", "bottomLine", "unknowns", "rowVerdict"}
)

RE_ID_PREFIX = re.compile(r"\b(?:jc|snk|hc)-\d+", re.I)
RE_BSIP1 = re.compile(r"\bbsip1[_-]", re.I)
RE_E_CODE = re.compile(r"\bE\d{3}\b", re.I)
RE_SCORE_GRADE_PREFIX = re.compile(r"\d+\s*/\s*grade\s*:", re.I)

RE_SIZE_TOKENS = re.compile(
    r"(?<!\d)\d+(?:\.\d+)?\s*(?:"
    r"גרם|ג'|ג\"|מ\"ל|מ״ל|ml|ML|ליטר|ל'|ל׳|liter|L\b|×\s*\d+\s*(?:יח|יח')?"
    r")",
    re.I,
)


@dataclass
class ShelfReport:
    shelf_id: str
    path: Path
    product_count: int = 0
    missing_required: list[str] = field(default_factory=list)
    forbidden_present: dict[str, int] = field(default_factory=dict)
    no_image: list[str] = field(default_factory=list)
    size_dup_sets: list[list[str]] = field(default_factory=list)
    rank_total_mismatch: list[str] = field(default_factory=list)
    copy_hygiene: list[str] = field(default_factory=list)

    @property
    def violation_count(self) -> int:
        return (
            len(self.missing_required)
            + sum(self.forbidden_present.values())
            + len(self.no_image)
            + len(self.size_dup_sets)
            + len(self.rank_total_mismatch)
            + len(self.copy_hygiene)
        )

    @property
    def conforms(self) -> bool:
        return self.violation_count == 0


def load_json(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def extract_products(raw: Any) -> list[dict[str, Any]]:
    if not isinstance(raw, dict):
        raise ValueError("root must be a JSON object")
    products = raw.get("products")
    if not isinstance(products, list):
        raise ValueError("missing products[] array")
    return [p for p in products if isinstance(p, dict)]


def normalize_size_name(name: str) -> str:
    s = RE_SIZE_TOKENS.sub("", name or "")
    s = re.sub(r"\s+", " ", s).strip().lower()
    return s


def limiting_texts(raw: Any) -> list[str]:
    if not isinstance(raw, list):
        return []
    out: list[str] = []
    for item in raw:
        if isinstance(item, str):
            out.append(item)
        elif isinstance(item, dict) and isinstance(item.get("text"), str):
            out.append(item["text"])
    return out


def consumer_copy_fields(product: dict[str, Any]) -> list[tuple[str, str]]:
    fields: list[tuple[str, str]] = []
    for key in ("insightLine", "rowVerdict"):
        val = product.get(key)
        if isinstance(val, str) and val.strip():
            fields.append((key, val))
    expansion = product.get("expansion")
    if isinstance(expansion, dict):
        ctx = expansion.get("comparisonContext")
        if isinstance(ctx, str) and ctx.strip():
            fields.append(("expansion.comparisonContext", ctx))
        for i, sig in enumerate(expansion.get("positiveSignals") or []):
            if isinstance(sig, str) and sig.strip():
                fields.append((f"expansion.positiveSignals[{i}]", sig))
        for i, txt in enumerate(limiting_texts(expansion.get("limitingFactors"))):
            if txt.strip():
                fields.append((f"expansion.limitingFactors[{i}]", txt))
    return fields


def check_copy_hygiene(product: dict[str, Any]) -> list[str]:
    pid = str(product.get("id", "?"))
    barcode = str(product.get("barcode") or "")
    hits: list[str] = []
    for field_path, text in consumer_copy_fields(product):
        reasons: list[str] = []
        if RE_ID_PREFIX.search(text):
            reasons.append("internal-id-prefix")
        if RE_BSIP1.search(text):
            reasons.append("bsip1-token")
        if barcode and barcode in text:
            reasons.append("raw-barcode")
        if isinstance(product.get("id"), str) and product["id"] in text:
            reasons.append("product-id")
        if RE_E_CODE.search(text):
            reasons.append("E-code")
        if RE_SCORE_GRADE_PREFIX.search(text):
            reasons.append("score/grade-prefix")
        if reasons:
            hits.append(f"{pid} {field_path}: {','.join(reasons)}")
    return hits


def check_product(
    product: dict[str, Any],
    *,
    product_count: int,
    score_rank: dict[str, int],
) -> tuple[list[str], dict[str, int], bool, list[str], list[str]]:
    pid = str(product.get("id", "?"))
    missing: list[str] = []
    forbidden: dict[str, int] = defaultdict(int)
    rank_issues: list[str] = []
    copy_issues: list[str] = []

    for key in REQUIRED_PRODUCT_KEYS:
        if key not in product:
            missing.append(f"{pid} missing-required:{key}")

    for key in FORBIDDEN_PRODUCT_KEYS:
        if key in product:
            forbidden[key] += 1

    expansion = product.get("expansion")
    if isinstance(expansion, dict):
        for key in FORBIDDEN_EXPANSION_KEYS:
            if key in expansion:
                forbidden[f"expansion.{key}"] += 1
        for key in REQUIRED_EXPANSION_KEYS:
            if key not in expansion:
                missing.append(f"{pid} missing-required:expansion.{key}")
        if "positiveSignals" in expansion and not isinstance(
            expansion["positiveSignals"], list
        ):
            missing.append(f"{pid} missing-required:expansion.positiveSignals (not array)")
        if "limitingFactors" in expansion and not isinstance(
            expansion["limitingFactors"], list
        ):
            missing.append(f"{pid} missing-required:expansion.limitingFactors (not array)")
        if "nutrition" in expansion and not isinstance(expansion["nutrition"], dict):
            missing.append(f"{pid} missing-required:expansion.nutrition (not object)")
    elif "expansion" in product:
        missing.append(f"{pid} missing-required:expansion (not object)")

    if "d4_additives" in product and not isinstance(product["d4_additives"], list):
        missing.append(f"{pid} missing-required:d4_additives (not array)")

    image = product.get("imageUrl")
    no_image = not (isinstance(image, str) and image.strip())

    rank_val = product.get("rank")
    if rank_val is not None and pid in score_rank:
        expected = score_rank[pid]
        try:
            if int(rank_val) != expected:
                rank_issues.append(
                    f"{pid} rank={rank_val} expected={expected} (score-order)"
                )
        except (TypeError, ValueError):
            rank_issues.append(f"{pid} rank={rank_val!r} not an integer")

    ct = product.get("categoryTotal")
    if ct is not None:
        try:
            if int(ct) != product_count:
                rank_issues.append(
                    f"{pid} categoryTotal={ct} expected={product_count}"
                )
        except (TypeError, ValueError):
            rank_issues.append(f"{pid} categoryTotal={ct!r} not an integer")

    copy_issues.extend(check_copy_hygiene(product))

    return missing, dict(forbidden), no_image, rank_issues, copy_issues

def build_score_rank(products: list[dict[str, Any]]) -> dict[str, int]:
    """Map product id -> expected rank (1 = highest score). Competition ranking."""
    scores: dict[str, float] = {}
    for p in products:
        pid = str(p.get("id", "?"))
        score = p.get("score")
        if isinstance(score, (int, float)):
            scores[pid] = float(score)
        else:
            scores[pid] = float("-inf")
    all_scores = list(scores.values())
    return {
        pid: 1 + sum(1 for s in all_scores if s > score)
        for pid, score in scores.items()
    }


def find_size_dup_sets(products: list[dict[str, Any]]) -> list[list[str]]:
    buckets: dict[str, list[str]] = defaultdict(list)
    for p in products:
        pid = str(p.get("id", "?"))
        name = p.get("name")
        if not isinstance(name, str) or not name.strip():
            continue
        key = normalize_size_name(name)
        if not key:
            continue
        buckets[key].append(pid)
    return [ids for ids in buckets.values() if len(ids) > 1]


def check_shelf(shelf_id: str, path: Path) -> ShelfReport:
    report = ShelfReport(shelf_id=shelf_id, path=path)
    try:
        raw = load_json(path)
        products = extract_products(raw)
    except Exception as exc:  # noqa: BLE001
        report.missing_required.append(f"LOAD-ERROR: {exc}")
        return report

    report.product_count = len(products)
    score_rank = build_score_rank(products)

    forbidden_totals: dict[str, int] = defaultdict(int)
    for product in products:
        missing, forbidden, no_img, rank_issues, copy_issues = check_product(
            product,
            product_count=report.product_count,
            score_rank=score_rank,
        )
        report.missing_required.extend(missing)
        for key, count in forbidden.items():
            forbidden_totals[key] += count
        if no_img:
            report.no_image.append(str(product.get("id", "?")))
        report.rank_total_mismatch.extend(rank_issues)
        report.copy_hygiene.extend(copy_issues)

    report.forbidden_present = dict(forbidden_totals)
    report.size_dup_sets = find_size_dup_sets(products)
    return report

def summarize_shelf(report: ShelfReport) -> str:
    parts: list[str] = []
    if report.missing_required:
        parts.append(f"missing-required x{len(report.missing_required)}")
    if report.forbidden_present:
        fb = ", ".join(f"{k} x{v}" for k, v in sorted(report.forbidden_present.items()))
        parts.append(f"forbidden-present ({fb})")
    if report.no_image:
        parts.append(f"no-image x{len(report.no_image)}")
    if report.size_dup_sets:
        parts.append(f"size-duplicate-sets x{len(report.size_dup_sets)}")
    if report.rank_total_mismatch:
        parts.append(f"rank/total-mismatch x{len(report.rank_total_mismatch)}")
    if report.copy_hygiene:
        parts.append(f"copy-hygiene x{len(report.copy_hygiene)}")
    if not parts:
        return "CONFORMS (0 violations)"
    return "; ".join(parts)


def format_report_lines(reports: list[ShelfReport]) -> list[str]:
    lines: list[str] = []
    lines.append("P268 baseline contract drift report")
    lines.append("=" * 72)
    conforming = [r for r in reports if r.conforms]
    violating = [r for r in reports if not r.conforms]
    lines.append(
        f"SUMMARY: {len(conforming)} conform, {len(violating)} non-conforming "
        f"(of {len(reports)} shelves checked)."
    )
    lines.append("")
    for report in reports:
        status = "CONFORMS" if report.conforms else "NON-CONFORMING"
        lines.append(
            f"[{status}] {report.shelf_id}  "
            f"({report.path.name}, {report.product_count} products)"
        )
        lines.append(f"  {summarize_shelf(report)}")
        if report.missing_required:
            lines.append("  missing-required:")
            for item in report.missing_required[:20]:
                lines.append(f"    - {item}")
            if len(report.missing_required) > 20:
                lines.append(f"    ... +{len(report.missing_required) - 20} more")
        if report.forbidden_present:
            lines.append("  forbidden-present:")
            for key, count in sorted(report.forbidden_present.items()):
                lines.append(f"    - {key} x{count}")
        if report.no_image:
            lines.append(f"  no-image ({len(report.no_image)}):")
            for pid in report.no_image[:10]:
                lines.append(f"    - {pid}")
            if len(report.no_image) > 10:
                lines.append(f"    ... +{len(report.no_image) - 10} more")
        if report.size_dup_sets:
            lines.append(f"  size-duplicate-sets ({len(report.size_dup_sets)}):")
            for dup_set in report.size_dup_sets[:10]:
                lines.append(f"    - {', '.join(dup_set)}")
            if len(report.size_dup_sets) > 10:
                lines.append(f"    ... +{len(report.size_dup_sets) - 10} more")
        if report.rank_total_mismatch:
            lines.append(f"  rank/total-mismatch ({len(report.rank_total_mismatch)}):")
            for item in report.rank_total_mismatch[:10]:
                lines.append(f"    - {item}")
            if len(report.rank_total_mismatch) > 10:
                lines.append(f"    ... +{len(report.rank_total_mismatch) - 10} more")
        if report.copy_hygiene:
            lines.append(f"  copy-hygiene ({len(report.copy_hygiene)}):")
            for item in report.copy_hygiene[:10]:
                lines.append(f"    - {item}")
            if len(report.copy_hygiene) > 10:
                lines.append(f"    ... +{len(report.copy_hygiene) - 10} more")
        lines.append("")
    if violating:
        lines.append("NON-CONFORMING SHELVES:")
        for report in violating:
            lines.append(f"  - {report.shelf_id}: {summarize_shelf(report)}")
    else:
        lines.append("All checked shelves conform to the baseline contract.")
    return lines


def print_report(reports: list[ShelfReport]) -> None:
    for line in format_report_lines(reports):
        print(line)


def write_drift_report(reports: list[ShelfReport], out_path: Path) -> None:
    out_path.parent.mkdir(parents=True, exist_ok=True)
    text = "\n".join(format_report_lines(reports)) + "\n"
    out_path.write_text(text, encoding="utf-8")


def resolve_shelf(shelf_arg: str) -> str | None:
    target = shelf_arg.strip().lower().replace("-", "_")
    if target in SHELF_FILES:
        return target
    for shelf_id in SHELF_FILES:
        if shelf_id.replace("_", "-") == target:
            return shelf_id
    return None


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Read-only per-product baseline contract validator (P268)."
    )
    g = parser.add_mutually_exclusive_group(required=True)
    g.add_argument("--all", action="store_true", help="check every live shelf")
    g.add_argument("--shelf", help="check one shelf id (e.g. snacks, bread)")
    args = parser.parse_args()

    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")  # type: ignore[attr-defined]

    if args.all:
        shelf_ids = sorted(SHELF_FILES)
    else:
        shelf_id = resolve_shelf(args.shelf)
        if shelf_id is None:
            known = ", ".join(sorted(SHELF_FILES))
            print(f"ERROR: unknown shelf '{args.shelf}'. Known: {known}", file=sys.stderr)
            return 3
        shelf_ids = [shelf_id]

    reports: list[ShelfReport] = []
    for shelf_id in shelf_ids:
        filename = SHELF_FILES[shelf_id]
        path = WEB_DATA / filename
        if not path.is_file():
            report = ShelfReport(shelf_id=shelf_id, path=path)
            report.missing_required.append(f"FILE-MISSING: {path}")
            reports.append(report)
            continue
        reports.append(check_shelf(shelf_id, path))

    print_report(reports)

    if args.all:
        drift_path = REPO / "tasks" / "returns" / "P268_drift_report.md"
        write_drift_report(reports, drift_path)
        print(f"\nDrift report written: {drift_path}")

    return 0 if all(r.conforms for r in reports) else 1


if __name__ == "__main__":
    sys.exit(main())
