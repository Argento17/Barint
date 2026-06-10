#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
run_schema_validation_gate.py — D3b (TASK-BARI-PROMPT-REGISTRY-CI-EVAL-V1)

Enforces the "schema validity < 98% = fail" threshold for the 4 schema_validation
examples in prompt_eval_dataset_v1.yaml (EXP-01..04). Read-only over the shipped
comparison JSON — changes nothing.

Per product expansion it checks:
  - array fields (positiveSignals/limitingFactors/unknowns/caveats) are lists of
    non-empty strings, each <= MAX_ITEM_LEN chars,
  - string fields (bottomLine/comparisonContext) are non-empty strings,
  - NO banned phrase (Explanation Engine v2) appears in any string.
Validity % = valid products / total products. Threshold: >= 98% per case.

Exit 0 = all 4 cases >= 98%. Non-zero otherwise.
"""
import sys, io, json
from pathlib import Path

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")
try:
    import yaml
except ImportError:
    print("PyYAML required"); sys.exit(2)

HERE = Path(__file__).resolve().parent
REPO = HERE.parents[2]
sys.path.insert(0, str(HERE))
from wording_check import scan_text  # shared precise checker

THRESHOLD = 0.98
MAX_ITEM_LEN = 240
ARRAY_FIELDS = ["positiveSignals", "limitingFactors", "unknowns", "caveats"]
STRING_FIELDS = ["bottomLine", "comparisonContext"]

# EXP-01..04 -> shipped JSON (from dataset source_file)
CASES = {
    "EXP-01": "bari-web/src/data/comparisons/hummus_frontend_v5.json",
    "EXP-02": "bari-web/src/data/comparisons/snacks_frontend_v2.json",
    "EXP-03": "bari-web/src/data/comparisons/bread_frontend_v2.json",
    "EXP-04": "bari-web/src/data/comparisons/yogurts_frontend_v3.json",
}


def validate_expansion(exp):
    """Return list of error strings for one product's expansion (empty = valid)."""
    errs = []
    if not isinstance(exp, dict):
        return ["expansion is not an object"]
    for f in ARRAY_FIELDS:
        if f not in exp:
            continue
        v = exp[f]
        if not isinstance(v, list):
            errs.append(f"{f} not a list"); continue
        for i, item in enumerate(v):
            if not isinstance(item, str) or not item.strip():
                errs.append(f"{f}[{i}] not a non-empty string")
            elif len(item) > MAX_ITEM_LEN:
                errs.append(f"{f}[{i}] over {MAX_ITEM_LEN} chars")
            else:
                for phrase, kind in scan_text(item):
                    errs.append(f"{f}[{i}] unsafe [{kind}]: {phrase}")
    for f in STRING_FIELDS:
        if f in exp and (not isinstance(exp[f], str) or not exp[f].strip()):
            errs.append(f"{f} not a non-empty string")
        elif f in exp:
            for phrase, kind in scan_text(exp[f]):
                errs.append(f"{f} unsafe [{kind}]: {phrase}")
    return errs


def main():
    overall_fail = False
    for case_id, rel in CASES.items():
        path = REPO / rel
        if not path.exists():
            print(f"[FAIL] {case_id}: JSON not found {rel}"); overall_fail = True; continue
        doc = json.loads(path.read_text(encoding="utf-8"))
        products = doc.get("products", doc if isinstance(doc, list) else [])
        total = len(products)
        invalid = []
        for p in products:
            exp = p.get("expansion") or {}
            errs = validate_expansion(exp)
            if errs:
                invalid.append((p.get("id") or p.get("canonical_product_id") or "?", errs))
        valid = total - len(invalid)
        validity = (valid / total) if total else 0.0
        ok = validity >= THRESHOLD
        print(f"[{'PASS' if ok else 'FAIL'}] {case_id} {rel.split('/')[-1]}: "
              f"{valid}/{total} valid = {validity:.1%} (threshold {THRESHOLD:.0%})")
        for pid, errs in invalid[:5]:
            print(f"    invalid {pid}: {errs[:3]}")
        if not ok:
            overall_fail = True
    print("-" * 60)
    print("SCHEMA VALIDATION:", "FAIL" if overall_fail else "ALL PASS (>= 98%)")
    return 1 if overall_fail else 0


if __name__ == "__main__":
    sys.exit(main())
