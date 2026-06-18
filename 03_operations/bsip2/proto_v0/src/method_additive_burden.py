#!/usr/bin/env python3
"""
P176 / TASK-325 — Additive burden aggregate index (representation only).

Rolls existing per-signal additive findings from BSIP2 traces into a single
displayable burden index. NO scoring change — consumes EV-002/003/019 outputs
already present in L3_inferred_classifications.

Run: python method_additive_burden.py --calibrate
OFF-ban: trace data only; never read Open Food Facts.
"""

from __future__ import annotations

import argparse
import json
import re
import statistics
import sys
from collections import Counter
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

# ---------------------------------------------------------------------------
# Inert weights / bands (NOT referenced by score_engine.py)
# ---------------------------------------------------------------------------
ADDITIVE_BURDEN_METHOD_VERSION = "additive_burden_v1"

# Transparent rollup weights — mirror engine signal severity, display-only.
ADDITIVE_BURDEN_WEIGHT_AT_RISK = 3.0          # EV-002: tax_named_concern_additives
ADDITIVE_BURDEN_WEIGHT_HIGH_RISK_EMULS = 2.0  # EV-003: sprint1_high_risk_emulsifier_found
ADDITIVE_BURDEN_WEIGHT_NEUTRAL_EMULS = 0.0    # EV-003: neutral tier — informational, zero weight
ADDITIVE_BURDEN_WEIGHT_PREBIOTIC_EXEMPT = -1.0  # EV-019: prebiotic gum exemption reduces display burden

ADDITIVE_BURDEN_BAND_LOW_MAX = 2.99
ADDITIVE_BURDEN_BAND_MED_MAX = 5.99

# Trace keys consumed (must all be present or index=null)
EV002_TRACE_KEY = "tax_named_concern_additives"
EV003_HIGH_TRACE_KEY = "sprint1_high_risk_emulsifier_found"
EV003_NEUTRAL_TRACE_KEY = "sprint1_neutral_emulsifier_found"
EV019_TRACE_KEY = "sprint1_prebiotic_gum_found"
REQUIRED_L3_KEYS = (
    EV002_TRACE_KEY,
    EV003_HIGH_TRACE_KEY,
    EV003_NEUTRAL_TRACE_KEY,
    EV019_TRACE_KEY,
)

OFF_REGEX = re.compile(
    r"open_food_facts|openfoodfacts\.org|images\.openfoodfacts|off_candidate_panel",
    re.IGNORECASE,
)

REPO = Path(__file__).resolve().parents[4]
CONFIGS_DIR = REPO / "03_operations" / "page_generator" / "configs"
REPORT_DIR = (
    REPO / "03_operations" / "bsip2" / "proto_v0" / "reports" / "methods" / "additive_burden"
)


def _trace_off_sourced(trace: dict[str, Any]) -> bool:
    """True when trace provenance references Open Food Facts (TASK-238 ban)."""
    blob = json.dumps(trace, ensure_ascii=False)
    return bool(OFF_REGEX.search(blob))


def _burden_band(index: float) -> str:
    if index <= 0:
        return "NONE"
    if index <= ADDITIVE_BURDEN_BAND_LOW_MAX:
        return "LOW"
    if index <= ADDITIVE_BURDEN_BAND_MED_MAX:
        return "MED"
    return "HIGH"


def evaluate_additive_burden(trace: dict[str, Any]) -> dict[str, Any]:
    """
    Roll up EV-002/003/019 additive signals from a BSIP2 trace.

    Returns index payload or index:null with reason when signals are absent.
    """
    if _trace_off_sourced(trace):
        return {
            "index": None,
            "reason": "trace references Open Food Facts (OFF-ban)",
        }

    l3 = trace.get("L3_inferred_classifications")
    if not isinstance(l3, dict):
        return {
            "index": None,
            "reason": "L3_inferred_classifications missing",
        }

    missing = [k for k in REQUIRED_L3_KEYS if k not in l3]
    if missing:
        return {
            "index": None,
            "reason": f"additive signals absent in trace: {', '.join(missing)}",
        }

    at_risk_list = list(l3.get(EV002_TRACE_KEY) or [])
    high_risk_emulsifiers = list(l3.get(EV003_HIGH_TRACE_KEY) or [])
    neutral_emulsifiers = list(l3.get(EV003_NEUTRAL_TRACE_KEY) or [])
    prebiotic_exempt = list(l3.get(EV019_TRACE_KEY) or [])

    at_risk_count = len(at_risk_list)

    components = {
        "ev002_at_risk": {
            "signal": "EV-002",
            "trace_field": EV002_TRACE_KEY,
            "additives": at_risk_list,
            "count": at_risk_count,
            "weight": ADDITIVE_BURDEN_WEIGHT_AT_RISK,
            "weighted": round(at_risk_count * ADDITIVE_BURDEN_WEIGHT_AT_RISK, 2),
        },
        "ev003_emulsifier_tiers": {
            "signal": "EV-003",
            "high_risk": {
                "trace_field": EV003_HIGH_TRACE_KEY,
                "emulsifiers": high_risk_emulsifiers,
                "count": len(high_risk_emulsifiers),
                "weight": ADDITIVE_BURDEN_WEIGHT_HIGH_RISK_EMULS,
                "weighted": round(
                    len(high_risk_emulsifiers) * ADDITIVE_BURDEN_WEIGHT_HIGH_RISK_EMULS, 2
                ),
            },
            "neutral": {
                "trace_field": EV003_NEUTRAL_TRACE_KEY,
                "emulsifiers": neutral_emulsifiers,
                "count": len(neutral_emulsifiers),
                "weight": ADDITIVE_BURDEN_WEIGHT_NEUTRAL_EMULS,
                "weighted": round(
                    len(neutral_emulsifiers) * ADDITIVE_BURDEN_WEIGHT_NEUTRAL_EMULS, 2
                ),
            },
        },
        "ev019_prebiotic_exemption": {
            "signal": "EV-019",
            "trace_field": EV019_TRACE_KEY,
            "exempt_gums": prebiotic_exempt,
            "count": len(prebiotic_exempt),
            "weight": ADDITIVE_BURDEN_WEIGHT_PREBIOTIC_EXEMPT,
            "weighted": round(
                len(prebiotic_exempt) * ADDITIVE_BURDEN_WEIGHT_PREBIOTIC_EXEMPT, 2
            ),
        },
    }

    additive_burden_index = round(
        components["ev002_at_risk"]["weighted"]
        + components["ev003_emulsifier_tiers"]["high_risk"]["weighted"]
        + components["ev003_emulsifier_tiers"]["neutral"]["weighted"]
        + components["ev019_prebiotic_exemption"]["weighted"],
        2,
    )

    return {
        "index": {
            "at_risk_count": at_risk_count,
            "high_risk_emulsifiers": high_risk_emulsifiers,
            "neutral_emulsifiers": neutral_emulsifiers,
            "prebiotic_exempt": prebiotic_exempt,
            "additive_burden_index": additive_burden_index,
            "burden_band": _burden_band(additive_burden_index),
            "components": components,
        },
        "reason": None,
    }


def discover_shelf_configs() -> list[Path]:
    return sorted(
        p for p in CONFIGS_DIR.glob("*.json") if not p.name.startswith("_generated_")
    )


def normalize_run_dirs(config: dict[str, Any]) -> list[Path]:
    run_dir = config.get("run_products_dir")
    if not run_dir:
        return []
    if isinstance(run_dir, str):
        return [Path(run_dir)]
    return [Path(d) for d in run_dir]


def _product_name(trace: dict[str, Any]) -> str:
    ref = trace.get("input_reference") or {}
    return (
        ref.get("product_name_he")
        or ref.get("canonical_name_he")
        or ref.get("canonical_product_id")
        or ""
    )


def collect_traces_from_dir(trace_dir: Path) -> list[tuple[Path, dict[str, Any]]]:
    out: list[tuple[Path, dict[str, Any]]] = []
    if not trace_dir.is_dir():
        return out
    for product_dir in sorted(trace_dir.iterdir()):
        if not product_dir.is_dir():
            continue
        trace_path = product_dir / "bsip2_trace.json"
        if not trace_path.is_file():
            continue
        try:
            trace = json.loads(trace_path.read_text(encoding="utf-8"))
        except (json.JSONDecodeError, OSError):
            continue
        out.append((trace_path, trace))
    return out


def run_calibration() -> tuple[dict[str, Any], dict[str, dict[str, int]]]:
    products: list[dict[str, Any]] = []
    shelf_totals: dict[str, dict[str, int]] = {}

    for config_path in discover_shelf_configs():
        shelf = config_path.stem
        config = json.loads(config_path.read_text(encoding="utf-8"))
        run_dirs = normalize_run_dirs(config)
        if not run_dirs:
            continue

        shelf_totals.setdefault(
            shelf,
            {
                "evaluated": 0,
                "index_null": 0,
                "with_at_risk": 0,
                "band_NONE": 0,
                "band_LOW": 0,
                "band_MED": 0,
                "band_HIGH": 0,
            },
        )

        seen_on_shelf: set[str] = set()
        for run_dir in run_dirs:
            for trace_path, trace in collect_traces_from_dir(run_dir):
                ref = trace.get("input_reference") or {}
                barcode = str(ref.get("barcode") or "").strip()
                shelf_key = f"{shelf}:{barcode}" if barcode else f"{shelf}:{trace_path}"
                if shelf_key in seen_on_shelf:
                    continue
                seen_on_shelf.add(shelf_key)

                result = evaluate_additive_burden(trace)
                idx = result["index"]
                band = idx["burden_band"] if idx else None

                st = shelf_totals[shelf]
                st["evaluated"] += 1
                if idx is None:
                    st["index_null"] += 1
                else:
                    if idx["at_risk_count"] > 0:
                        st["with_at_risk"] += 1
                    if band:
                        st[f"band_{band}"] += 1

                products.append({
                    "barcode": barcode,
                    "shelf": shelf,
                    "product_name": _product_name(trace),
                    "category": trace.get("category"),
                    "index": idx,
                    "index_null_reason": result["reason"],
                    "trace_source": str(trace_path),
                })

    products.sort(key=lambda r: (
        -(r["index"]["additive_burden_index"] if r["index"] else -1),
        r["shelf"],
        r["barcode"],
    ))

    index_values = [
        p["index"]["additive_burden_index"]
        for p in products
        if p["index"] is not None
    ]
    band_dist = Counter(
        p["index"]["burden_band"] for p in products if p["index"] is not None
    )
    index_dist = Counter(index_values)

    summary = {
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "method": "additive_burden",
        "method_version": ADDITIVE_BURDEN_METHOD_VERSION,
        "off_ban": "trace data only; OFF-sourced traces → index:null",
        "weighting": {
            "at_risk_per_additive": ADDITIVE_BURDEN_WEIGHT_AT_RISK,
            "high_risk_emulsifier_per_hit": ADDITIVE_BURDEN_WEIGHT_HIGH_RISK_EMULS,
            "neutral_emulsifier_per_hit": ADDITIVE_BURDEN_WEIGHT_NEUTRAL_EMULS,
            "prebiotic_exempt_per_gum": ADDITIVE_BURDEN_WEIGHT_PREBIOTIC_EXEMPT,
            "bands": {
                "NONE": "index <= 0",
                "LOW": f"0 < index <= {ADDITIVE_BURDEN_BAND_LOW_MAX}",
                "MED": f"{ADDITIVE_BURDEN_BAND_LOW_MAX} < index <= {ADDITIVE_BURDEN_BAND_MED_MAX}",
                "HIGH": f"index > {ADDITIVE_BURDEN_BAND_MED_MAX}",
            },
        },
        "trace_fields_consumed": {
            "EV-002": EV002_TRACE_KEY,
            "EV-003_high": EV003_HIGH_TRACE_KEY,
            "EV-003_neutral": EV003_NEUTRAL_TRACE_KEY,
            "EV-019": EV019_TRACE_KEY,
        },
        "products_processed": len(products),
        "index_null": sum(1 for p in products if p["index"] is None),
        "products_with_at_risk_additives": sum(
            1 for p in products if p["index"] and p["index"]["at_risk_count"] > 0
        ),
        "burden_band_distribution": dict(sorted(band_dist.items())),
        "additive_burden_index_distribution": {
            "min": min(index_values) if index_values else None,
            "max": max(index_values) if index_values else None,
            "median": statistics.median(index_values) if index_values else None,
            "stdev": round(statistics.pstdev(index_values), 4) if len(index_values) > 1 else 0.0,
            "most_common_value": index_dist.most_common(1)[0] if index_dist else None,
            "histogram": {str(k): v for k, v in sorted(index_dist.items())},
        },
        "burden_band_per_shelf": {
            s: {
                **t,
                "null_rate": round(t["index_null"] / t["evaluated"], 4) if t["evaluated"] else 0.0,
                "at_risk_rate": round(t["with_at_risk"] / t["evaluated"], 4) if t["evaluated"] else 0.0,
            }
            for s, t in sorted(shelf_totals.items())
        },
        "products": products,
    }
    return summary, shelf_totals


def write_reports(summary: dict[str, Any], shelf_totals: dict[str, dict[str, int]]) -> None:
    REPORT_DIR.mkdir(parents=True, exist_ok=True)
    index_json = REPORT_DIR / "index.json"
    index_md = REPORT_DIR / "index.md"

    index_json.write_text(json.dumps(summary, ensure_ascii=False, indent=2), encoding="utf-8")

    n = summary["products_processed"]
    null_n = summary["index_null"]
    at_risk_n = summary["products_with_at_risk_additives"]
    band_dist = summary["burden_band_distribution"]
    idx_dist = summary["additive_burden_index_distribution"]

    lines = [
        "# Additive burden aggregate index — live shelf rollup (P176)",
        "",
        f"Generated: {summary['generated_at']}",
        "",
        "Representation only — rolls existing EV-002/003/019 trace signals.",
        "No scoring change; weights are inert display constants.",
        "",
        "## Summary",
        "",
        "| Metric | Count |",
        "|--------|------:|",
        f"| Products processed (denominator) | {n} |",
        f"| Index computed | {n - null_n} |",
        f"| Index null (missing/OFF signals) | {null_n} |",
        f"| Products with at-risk additives (EV-002) | {at_risk_n} |",
        "",
        "## Burden band distribution (all shelves)",
        "",
        "| Band | Count |",
        "|------|------:|",
    ]
    for band in ("NONE", "LOW", "MED", "HIGH"):
        lines.append(f"| {band} | {band_dist.get(band, 0)} |")

    lines.extend([
        "",
        "## Additive burden index distribution",
        "",
        f"- min: {idx_dist['min']}",
        f"- max: {idx_dist['max']}",
        f"- median: {idx_dist['median']}",
        f"- stdev: {idx_dist['stdev']}",
        f"- most_common: {idx_dist['most_common_value']}",
        "",
        "### Index histogram",
        "",
        "| Index value | Products |",
        "|------------:|---------:|",
    ])
    for val, cnt in sorted(
        ((float(k), v) for k, v in idx_dist["histogram"].items()),
        key=lambda x: x[0],
    ):
        lines.append(f"| {val} | {cnt} |")

    lines.extend([
        "",
        "## Burden band per shelf",
        "",
        "| Shelf | Evaluated | NONE | LOW | MED | HIGH | At-risk | Null |",
        "|-------|----------:|-----:|----:|----:|-----:|--------:|-----:|",
    ])
    for shelf, t in sorted(shelf_totals.items()):
        lines.append(
            f"| {shelf} | {t['evaluated']} | {t['band_NONE']} | {t['band_LOW']} | "
            f"{t['band_MED']} | {t['band_HIGH']} | {t['with_at_risk']} | {t['index_null']} |"
        )

    highest = [
        p for p in summary["products"]
        if p["index"] and p["index"]["burden_band"] == "HIGH"
    ]
    lines.extend([
        "",
        "## Highest-burden products (band=HIGH)",
        "",
        "| Shelf | Barcode | Product | Index | At-risk | High-risk emuls | Neutral | Prebiotic exempt |",
        "|-------|---------|---------|------:|--------:|------------------:|--------:|-----------------:|",
    ])
    for p in highest[:40]:
        idx = p["index"]
        name = p["product_name"].replace("|", "/")
        lines.append(
            f"| {p['shelf']} | {p['barcode']} | {name} | "
            f"{idx['additive_burden_index']} | {idx['at_risk_count']} | "
            f"{len(idx['high_risk_emulsifiers'])} | {len(idx['neutral_emulsifiers'])} | "
            f"{len(idx['prebiotic_exempt'])} |"
        )
    if not highest:
        lines.append("| — | — | _No HIGH-band products_ | — | — | — | — | — |")
    elif len(highest) > 40:
        lines.append(f"| … | … | _{len(highest) - 40} more HIGH-band products_ | … | … | … | … | … |")

    index_md.write_text("\n".join(lines) + "\n", encoding="utf-8")


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Additive burden index method (P176)")
    parser.add_argument(
        "--calibrate",
        action="store_true",
        help="Roll up additive burden across live shelf BSIP2 traces",
    )
    parser.add_argument(
        "--single",
        help="Single-product test: path to bsip2_trace.json",
    )
    args = parser.parse_args(argv)

    if args.single:
        trace = json.loads(Path(args.single).read_text(encoding="utf-8"))
        result = evaluate_additive_burden(trace)
        print(json.dumps(result, ensure_ascii=False, indent=2))
        return 0

    if args.calibrate:
        summary, shelf_totals = run_calibration()
        write_reports(summary, shelf_totals)
        print(json.dumps({
            "products_processed": summary["products_processed"],
            "index_null": summary["index_null"],
            "burden_band_distribution": summary["burden_band_distribution"],
            "report_dir": str(REPORT_DIR),
        }, indent=2))
        return 0

    parser.print_help()
    return 1


if __name__ == "__main__":
    sys.exit(main())