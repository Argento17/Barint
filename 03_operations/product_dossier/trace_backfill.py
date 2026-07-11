#!/usr/bin/env python3
"""Backfill loader-compatible BSIP2 traces from an existing rerank table.

This utility is intentionally trace-only: it never imports or invokes a score
engine.  It writes one ``<run_dir>/backfill_<barcode>/bsip2_trace.json`` file
per *served* product, the exact one-directory layout consumed by
``run_gates.load_bsip2_traces``.  The final score is copied verbatim from the
rerank table and is asserted equal to the served JSON before a trace is written.

The rerank table is a historical scoring artifact rather than a full BSIP2
trace, so unavailable standard fields are explicitly null, never reconstructed.
"""
from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any, Dict


REPO_ROOT = Path(__file__).resolve().parents[2]
DEFAULT_RUN_DIR = REPO_ROOT / "02_products" / "snack_bars" / "bsip2_outputs" / "protein_bars_task365"
DEFAULT_RERANK = DEFAULT_RUN_DIR / "rerank_table_rescore.json"
DEFAULT_RUN_RECORD = DEFAULT_RUN_DIR / "run_record_rescore.json"
DEFAULT_SERVED = REPO_ROOT / "bari-web" / "src" / "data" / "comparisons" / "protein_combined_frontend_v2.json"


def read_json(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def write_json(path: Path, value: dict) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def trace_for_product(row: dict, served: dict, run_record: dict) -> dict:
    """Build the standard fields consumers read, preserving source values."""
    barcode = str(row["barcode"])
    return {
        "bsip2_version": "trace_backfill_v1",
        "algorithm_version": "historical_lens_output_not_reexecuted",
        "trace_generated_at": run_record.get("generated_at"),
        "specification_version": "TASK-627 trace-only backfill from rerank_table_rescore.json",
        "input_reference": {
            "canonical_product_id": f"backfill_{barcode}",
            "barcode": barcode,
            "product_name_he": row.get("name"),
            "brand": row.get("brand"),
            "source_retailers": ["shufersal"],
            "bsip1_source_path": None,
            "audit_ref": None,
            "bsip1_schema_version": None,
            "load_errors": [],
        },
        "evaluation_status": "historical_trace_backfill",
        "run_id": run_record.get("run_id"),
        "category": "protein_bar",
        "nova_proxy": None,
        "confidence_score": None,
        "dimension_scores": None,
        "final_score_estimate": row["score"],
        # Use the published grade: it is the grade G5 verifies against the
        # copied score.  Preserve the historical rerank grade separately when
        # it differs so this backfill neither conceals nor changes that record.
        "grade_estimate": served["grade"],
        "explanation_drivers": row.get("caps_applied", []),
        "backfill_provenance": {
            "source_rerank_table": "rerank_table_rescore.json",
            "source_run_record": "run_record_rescore.json",
            "source_score": row["score"],
            "source_grade": row.get("grade"),
            "served_score": served["score"],
            "served_grade": served["grade"],
            "score_identity_assertion": "passed",
        },
    }


def backfill(run_dir: Path, rerank_path: Path, run_record_path: Path, served_path: Path) -> int:
    rerank_rows = read_json(rerank_path)
    run_record = read_json(run_record_path)
    served_products = read_json(served_path)["products"]
    by_barcode: Dict[str, dict] = {str(row["barcode"]): row for row in rerank_rows}

    if len(by_barcode) != len(rerank_rows):
        raise ValueError("rerank table has duplicate barcodes")

    emitted = 0
    grade_differences = []
    for product in served_products:
        barcode = str(product["barcode"])
        row = by_barcode.get(barcode)
        if row is None:
            raise ValueError(f"served barcode absent from rerank table: {barcode}")
        # Exact JSON values (not tolerance/rounding) are mandatory here.
        if product.get("score") != row.get("score"):
            raise ValueError(
                f"score mismatch for {barcode}: served={product.get('score')!r}, "
                f"rerank={row.get('score')!r}"
            )
        if product.get("grade") != row.get("grade"):
            grade_differences.append(barcode)
        trace = trace_for_product(row, product, run_record)
        write_json(run_dir / f"backfill_{barcode}" / "bsip2_trace.json", trace)
        emitted += 1

    # Re-read through the actual loader contract after writing.
    import importlib.util
    gates_path = REPO_ROOT / "03_operations" / "page_generator" / "gates" / "run_gates.py"
    spec = importlib.util.spec_from_file_location("task627_run_gates", gates_path)
    gates = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(gates)
    loaded = gates.load_bsip2_traces(str(run_dir))
    expected = {str(p["barcode"]) for p in served_products}
    missing = expected - set(loaded)
    if missing:
        raise ValueError(f"loader did not recover traces for: {sorted(missing)}")
    for product in served_products:
        barcode = str(product["barcode"])
        if loaded[barcode].get("final_score_estimate") != product["score"]:
            raise ValueError(f"written trace score differs from served score for {barcode}")

    print(f"traces_emitted={emitted}")
    print("scores_identical=true")
    print(f"loader_recovered_served_traces={len(expected)}")
    print("rerank_served_grade_differences=" + ",".join(grade_differences or ["none"]))
    return emitted


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--run-dir", type=Path, default=DEFAULT_RUN_DIR)
    parser.add_argument("--rerank-table", type=Path, default=DEFAULT_RERANK)
    parser.add_argument("--run-record", type=Path, default=DEFAULT_RUN_RECORD)
    parser.add_argument("--served-json", type=Path, default=DEFAULT_SERVED)
    args = parser.parse_args()
    backfill(args.run_dir, args.rerank_table, args.run_record, args.served_json)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
