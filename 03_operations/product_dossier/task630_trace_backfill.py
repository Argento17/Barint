#!/usr/bin/env python3
"""Emit TASK-630 trace-only backfills for served scores stale in original traces."""
from __future__ import annotations

import importlib.util
import json
from pathlib import Path
from typing import Any

REPO_ROOT = Path(__file__).resolve().parents[2]
# The 0.2-point drift below is below the dossier calculation tolerance, so it
# is not a TASK-630 calculation failure and must not receive a synthetic trace.
NON_CALC_TRACE_DIFFS = {"7290019635383", "56272"}
SHELVES = (
    ("bread", "bread", "bari-web/src/data/comparisons/bread_frontend_v4.json", "02_products/bread/bsip2_outputs/run_bread_conform_001/products", "02_products/bread/bsip2_outputs/run_bread_task630_backfill/products"),
    ("crackers", "crackers", "bari-web/src/data/comparisons/crackers_frontend_v1.json", "02_products/crackers/bsip2_outputs/run_crackers_conform_001/products", "02_products/crackers/bsip2_outputs/run_crackers_task630_backfill/products"),
    ("cheese", "cheese-spreads", "bari-web/src/data/comparisons/cheese_frontend_v4.json", "02_products/cheese_spreads/bsip2_outputs/run_cheese_004/products", "02_products/cheese_spreads/bsip2_outputs/run_cheese_task630_backfill/products"),
)

def load(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))

def load_traces():
    path = REPO_ROOT / "03_operations/page_generator/gates/run_gates.py"
    spec = importlib.util.spec_from_file_location("task630_run_gates", path)
    module = importlib.util.module_from_spec(spec)
    assert spec and spec.loader
    spec.loader.exec_module(module)
    return module.load_bsip2_traces

def make_trace(product: dict, category: str, original: dict) -> dict:
    barcode = str(product["barcode"])
    return {
        "bsip2_version": "trace_backfill_v1",
        "algorithm_version": "historical_lens_output_not_reexecuted",
        "trace_generated_at": None,
        "specification_version": "TASK-630 trace-only backfill from served comparison JSON",
        "input_reference": {"canonical_product_id": f"backfill_{barcode}", "barcode": barcode,
                            "product_name_he": product.get("nameHe"), "brand": product.get("brand"),
                            "source_retailers": None, "bsip1_source_path": None, "audit_ref": None,
                            "bsip1_schema_version": None, "load_errors": []},
        "evaluation_status": "historical_trace_backfill", "run_id": "task630_trace_backfill",
        "category": category, "nova_proxy": None, "confidence_score": None,
        "dimension_scores": None, "final_score_estimate": product["score"],
        "grade_estimate": product["grade"], "explanation_drivers": None,
        "backfill_provenance": {"source": "served comparison JSON",
                                "original_trace_score": original.get("final_score_estimate"),
                                "served_score": product["score"], "served_grade": product["grade"],
                                "score_identity_assertion": "passed"},
    }

def main() -> int:
    trace_loader = load_traces()
    totals = {}
    for name, category, served_rel, original_rel, backfill_rel in SHELVES:
        served = load(REPO_ROOT / served_rel)["products"]
        original = trace_loader(str(REPO_ROOT / original_rel))
        # TASK-630's fallback set is strictly products with an *existing* trace
        # whose score is stale.  Products without an original trace are outside
        # this surgical repair and must not be synthesized here.
        mismatched = [
            p for p in served if str(p["barcode"]) in original
            and original[str(p["barcode"])].get("final_score_estimate") != p.get("score")
            and str(p["barcode"]) not in NON_CALC_TRACE_DIFFS
        ]
        output = REPO_ROOT / backfill_rel
        for product in mismatched:
            barcode = str(product["barcode"])
            trace = make_trace(product, category, original[barcode])
            if trace["final_score_estimate"] != product["score"]:
                raise ValueError(f"{name} {barcode}: score identity failed before write")
            target = output / f"backfill_{barcode}" / "bsip2_trace.json"
            target.parent.mkdir(parents=True, exist_ok=True)
            target.write_text(json.dumps(trace, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
        written = trace_loader(str(output))
        expected = {str(p["barcode"]): p for p in mismatched}
        if set(written) != set(expected):
            raise ValueError(f"{name}: loader recovery mismatch")
        for barcode, product in expected.items():
            if written[barcode].get("final_score_estimate") != product["score"]:
                raise ValueError(f"{name} {barcode}: score identity failed after write")
        totals[name] = len(expected)
        print(f"{name}: traces_emitted={len(expected)} scores_identical=true")
    print("backfilled=" + json.dumps(totals, sort_keys=True))
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
