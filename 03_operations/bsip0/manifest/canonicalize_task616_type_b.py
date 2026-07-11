"""Canonicalize and audit TASK-616 reconstructed nutrition values.

The original TASK-616 Type-B canonicalization was a one-shot, uncommitted
reconstruction.  This retained producer deliberately has no local number
parser: persisted ``nutrition_raw_source.rows`` always flows through the
shared BSIP0 parser before ``nutrition_numeric`` is emitted.

Run from the repository root:
    python 03_operations/bsip0/manifest/canonicalize_task616_type_b.py --audit
    python 03_operations/bsip0/manifest/canonicalize_task616_type_b.py --selftest
"""
from __future__ import annotations

import argparse
import json
import pathlib
import sys
from typing import Any, Iterator

ROOT = pathlib.Path(__file__).resolve().parents[3]
SHARED = ROOT / "03_operations" / "bsip0" / "scrape" / "_shared"
sys.path.insert(0, str(SHARED))
import bsip0_nutrition as shared  # noqa: E402

NUMERIC_KEYS = (
    "energy_kcal", "fat_g", "fat_saturated_g", "sodium_mg",
    "carbohydrates_g", "sugars_g", "dietary_fiber_g", "protein_g",
)
TOLERANCE = 0.05
REPORT_PATH = ROOT / "03_operations" / "bsip0" / "manifest" / "task631_type_b_comma_audit.json"


def reconstruct_nutrition_numeric(rows: list[dict[str, Any]]) -> dict[str, Any]:
    """The sole Type-B producer: raw rows -> shared canonical numeric fields."""
    bare = shared.parse_nutrition_rows(rows)
    return shared.parse_nutrition_numeric(shared.bare_to_raw_keys(bare))


def _json_files() -> Iterator[pathlib.Path]:
    # ``canonicalization_schema`` is the persisted provenance marker for this
    # class.  Searching only these capture containers avoids treating BSIP1/2
    # derivatives as independent producers of the same numeric values.
    for relative in _git_lines("grep", "-l", "canonicalization_schema", "--", "*.json"):
        yield ROOT / relative


def _git_lines(*args: str) -> list[str]:
    import subprocess
    result = subprocess.run(["git", *args], cwd=ROOT, check=True,
                            capture_output=True, text=True, encoding="utf-8")
    return [line for line in result.stdout.splitlines() if line]


def _records(value: Any) -> Iterator[dict[str, Any]]:
    if isinstance(value, dict):
        if "nutrition_numeric" in value and (value.get("nutrition_raw_source") or {}).get("rows"):
            yield value
        for child in value.values():
            yield from _records(child)
    elif isinstance(value, list):
        for child in value:
            yield from _records(child)


def _shelf(path: pathlib.Path, record: dict[str, Any]) -> str | None:
    for candidate in (record.get("shelf"), record.get("category_id"), record.get("category")):
        if candidate:
            return str(candidate)
    parts = path.relative_to(ROOT).parts
    return parts[1] if len(parts) > 1 and parts[0] == "02_products" else None


def _mismatch(stored: Any, recomputed: Any) -> bool:
    if stored is None and recomputed is None:
        return False
    if stored is None or recomputed is None:
        return True
    return abs(float(stored) - float(recomputed)) > TOLERANCE


def audit() -> dict[str, Any]:
    checked = 0
    type_b_checked = 0
    non_shared_checked = 0
    mismatches: list[dict[str, Any]] = []
    schema_counts: dict[str, int] = {}
    seen: set[tuple[str, str, str]] = set()
    for path in _json_files():
        try:
            payload = json.loads(path.read_text(encoding="utf-8"))
        except (json.JSONDecodeError, UnicodeDecodeError):
            continue
        for record in _records(payload):
            rows = record["nutrition_raw_source"]["rows"]
            schema = record.get("canonicalization_schema")
            # A record can appear in multiple derived artifacts; audit each source
            # file once, while suppressing duplicate references to the same object.
            identity = (str(path.relative_to(ROOT)), str(record.get("barcode")), str(record.get("name") or record.get("name_he")))
            if identity in seen:
                continue
            seen.add(identity)
            checked += 1
            schema_label = str(schema) if schema is not None else "<missing>"
            schema_counts[schema_label] = schema_counts.get(schema_label, 0) + 1
            if schema == "task616_type_b_rows_reconstructed_from_nutrition_raw":
                type_b_checked += 1
            if schema != "shared_parser":
                non_shared_checked += 1
            recomputed = reconstruct_nutrition_numeric(rows)
            stored = record.get("nutrition_numeric") or {}
            for field in NUMERIC_KEYS:
                old, new = stored.get(field), recomputed.get(field)
                if not _mismatch(old, new):
                    continue
                comma_signature = (
                    old is not None and new not in (None, 0)
                    and abs(float(old) - float(new) / 1000) <= TOLERANCE
                )
                mismatches.append({
                    "file": str(path.relative_to(ROOT)).replace("\\", "/"),
                    "shelf": _shelf(path, record),
                    "barcode": record.get("barcode"),
                    "name": record.get("name") or record.get("name_he"),
                    "canonicalization_schema": schema,
                    "field": field,
                    "stored_value": old,
                    "recomputed_value": new,
                    "comma_thousands_signature": comma_signature,
                })
    return {
        "task": "TASK-631",
        "producer": "canonicalize_task616_type_b.reconstruct_nutrition_numeric",
        "parser_path": "parse_nutrition_rows -> bare_to_raw_keys -> parse_nutrition_numeric",
        "tolerance": TOLERANCE,
        "records_checked": checked,
        "task616_type_b_records_checked": type_b_checked,
        "non_shared_precomputed_records_checked": non_shared_checked,
        "records_by_canonicalization_schema": schema_counts,
        "mismatches": mismatches,
        "mismatch_count": len(mismatches),
        "score_affecting_flags": [
            {
                "shelf": item["shelf"], "barcode": item["barcode"],
                "field": item["field"], "old_to_new": [item["stored_value"], item["recomputed_value"]],
                "note": "Capture correction is score-affecting; served crackers output was not touched by TASK-631. TASK-629 records the already-applied shared-parser re-score as 50.3/C -> 35.0/D.",
            }
            for item in mismatches if item["field"] in {"sodium_mg", "fat_g", "fat_saturated_g", "sugars_g", "dietary_fiber_g"}
        ],
    }


def selftest() -> int:
    cases = (("1,200", 1200.0), ("0,123", 0.123), ("1.5", 1.5))
    failures = []
    for raw, expected in cases:
        got = shared._to_float(raw)
        print(f"_to_float({raw!r}) = {got!r}; expected {expected!r}")
        if got != expected:
            failures.append((raw, expected, got))
    if failures:
        print(f"FAIL: {failures}")
        return 1
    print("PASS: Type-B producer uses the shared comma-safe parser.")
    return 0


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--audit", action="store_true")
    parser.add_argument("--selftest", action="store_true")
    args = parser.parse_args()
    if args.selftest:
        return selftest()
    if args.audit:
        report = audit()
        REPORT_PATH.write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
        print(f"records_checked={report['records_checked']} mismatches={report['mismatch_count']}")
        print(REPORT_PATH)
        return 0
    parser.error("choose --audit or --selftest")
    return 2


if __name__ == "__main__":
    raise SystemExit(main())
