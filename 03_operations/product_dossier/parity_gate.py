#!/usr/bin/env python3
"""Fail closed when served comparison data, Product Dossiers, or catalog drift.

TASK-623.  The comparison JSON is the consumer-facing source of truth.  PD
publication_record is a verbatim projection of it, while the catalog loader
reads the comparison registry directly.  This gate checks all three surfaces
without recalculating or writing any product values.

Usage:
  python 03_operations/product_dossier/parity_gate.py
  python 03_operations/product_dossier/parity_gate.py --report path.json
  python 03_operations/product_dossier/parity_gate.py --selftest
"""
from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path
from typing import Any, Dict, Iterable, List, Tuple

REPO_ROOT = Path(__file__).resolve().parents[2]
COMPARISONS_DIR = REPO_ROOT / "bari-web" / "src" / "data" / "comparisons"
PD_INDEX_PATH = REPO_ROOT / "bari-web" / "src" / "data" / "dossiers_generated" / "index.json"
INVENTORY_LOADER_PATH = REPO_ROOT / "bari-web" / "src" / "lib" / "inventory" / "loader.ts"


def normalized_name(value: Any) -> str:
    return re.sub(r"\s+", " ", str(value or "").strip().casefold())


def shelf_for_comparison(path: Path) -> str:
    return re.sub(r"_frontend_v\d+$", "", path.stem)


def product_files() -> Iterable[Path]:
    """Only JSON payloads with product arrays are served product surfaces.

    The filename glob also finds the red-team ledgers; those are deliberately
    ignored because they have no products[] consumer corpus to compare.
    """
    for path in sorted(COMPARISONS_DIR.glob("*_frontend_v*.json")):
        try:
            if isinstance(json.loads(path.read_text(encoding="utf-8")).get("products"), list):
                yield path
        except (OSError, json.JSONDecodeError):
            yield path  # report the malformed source as a gate failure


def load_surfaces() -> Tuple[List[Dict[str, Any]], List[Dict[str, Any]], List[Dict[str, Any]]]:
    comparisons: List[Dict[str, Any]] = []
    malformed: List[Dict[str, Any]] = []
    for path in product_files():
        try:
            payload = json.loads(path.read_text(encoding="utf-8"))
        except (OSError, json.JSONDecodeError) as exc:
            malformed.append({"surface": "comparison", "file": str(path.relative_to(REPO_ROOT)), "error": str(exc)})
            continue
        if not isinstance(payload.get("products"), list):
            malformed.append({"surface": "comparison", "file": str(path.relative_to(REPO_ROOT)), "error": "products is not a list"})
            continue
        shelf = shelf_for_comparison(path)
        for product in payload["products"]:
            comparisons.append({**product, "_shelf": shelf, "_file": str(path.relative_to(REPO_ROOT))})
    try:
        pd_rows = json.loads(PD_INDEX_PATH.read_text(encoding="utf-8")).get("products", [])
    except (OSError, json.JSONDecodeError) as exc:
        malformed.append({"surface": "pd", "file": str(PD_INDEX_PATH.relative_to(REPO_ROOT)), "error": str(exc)})
        pd_rows = []
    return comparisons, pd_rows, malformed


def find_pd(product: Dict[str, Any], pd_rows: List[Dict[str, Any]]) -> Tuple[Dict[str, Any] | None, str | None]:
    # Barcode is authoritative.  Name is only an explicit fallback for products
    # with absent/unstable barcode values, never a score-data substitution.
    barcode = str(product.get("barcode") or "")
    same_shelf = [r for r in pd_rows if r.get("shelfId") == product.get("_shelf")]
    candidates = same_shelf or pd_rows
    barcode_matches = [r for r in candidates if str(r.get("servedBarcode") or "") == barcode and barcode]
    if len(barcode_matches) == 1:
        return barcode_matches[0], "barcode"
    name = normalized_name(product.get("name"))
    name_matches = [r for r in candidates if normalized_name(r.get("name")) == name and name]
    if len(name_matches) == 1:
        return name_matches[0], "normalized_name"
    return None, None


def catalog_contract_failure() -> str | None:
    """Confirm inventory remains a direct projection of the comparison registry."""
    try:
        source = INVENTORY_LOADER_PATH.read_text(encoding="utf-8")
    except OSError as exc:
        return f"cannot read catalog loader: {exc}"
    required = ("getComparisonCategoryCorpusPayload", "score: product.score", "grade: product.grade", "sku = raw.barcode")
    missing = [token for token in required if token not in source]
    return f"catalog loader no longer directly projects comparison fields: missing {missing}" if missing else None


def evaluate(comparisons: List[Dict[str, Any]], pd_rows: List[Dict[str, Any]], malformed: List[Dict[str, Any]], check_catalog: bool = True) -> Dict[str, Any]:
    divergences = list(malformed)
    gaps: List[Dict[str, Any]] = []
    matched = agree = 0
    matched_pd_keys = set()
    for product in comparisons:
        pd, method = find_pd(product, pd_rows)
        label = {"product": product.get("name"), "shelf": product.get("_shelf"), "file": product.get("_file"), "barcode": product.get("barcode")}
        if pd is None:
            gaps.append({"missing_surface": "pd", **label})
            continue
        matched += 1
        matched_pd_keys.add((pd.get("shelfId"), pd.get("key")))
        comparison_value = {"score": product.get("score"), "grade": product.get("grade"), "barcode": str(product.get("barcode") or "")}
        pd_value = {"score": pd.get("publishedScore"), "grade": pd.get("publishedGrade"), "barcode": str(pd.get("servedBarcode") or "")}
        if comparison_value == pd_value:
            agree += 1
        else:
            divergences.append({"surface": "pd", "match_method": method, **label, "comparison": comparison_value, "pd": pd_value})
    for pd in pd_rows:
        key = (pd.get("shelfId"), pd.get("key"))
        if key not in matched_pd_keys:
            gaps.append({"missing_surface": "comparison", "product": pd.get("name"), "shelf": pd.get("shelfId"), "barcode": pd.get("servedBarcode"), "pid": pd.get("pid")})
    if check_catalog:
        failure = catalog_contract_failure()
        if failure:
            divergences.append({"surface": "catalog", "error": failure})
    return {"comparison_products": len(comparisons), "pd_products": len(pd_rows), "matched": matched, "agree": agree,
            "diverge": len(divergences), "coverage_gaps": gaps, "divergences": divergences,
            "catalog": {"status": "pass" if not check_catalog or not catalog_contract_failure() else "fail",
                        "basis": "inventory loader directly reads comparison registry score, grade, and barcode"}}


def print_result(result: Dict[str, Any]) -> None:
    print(f"PD parity: matched={result['matched']} agree={result['agree']} diverge={result['diverge']} gaps={len(result['coverage_gaps'])}")
    for item in result["divergences"]:
        print("DIVERGENCE " + json.dumps(item, ensure_ascii=False, sort_keys=True))
    for item in result["coverage_gaps"]:
        print("COVERAGE_GAP " + json.dumps(item, ensure_ascii=False, sort_keys=True))


def selftest() -> int:
    comparison = [{"_shelf": "fixture", "_file": "fixture.json", "name": "One", "barcode": "123", "score": 80, "grade": "A"}]
    pd = [{"shelfId": "fixture", "key": "one", "name": "One", "servedBarcode": "123", "publishedScore": 80, "publishedGrade": "A"}]
    passing = evaluate(comparison, pd, [], check_catalog=False)
    failing = evaluate(comparison, [{**pd[0], "publishedScore": 79}], [], check_catalog=False)
    if passing["agree"] == 1 and passing["diverge"] == 0 and failing["diverge"] == 1:
        print("SELFTEST PASS: agreement passes and injected PD score mismatch is caught.")
        return 0
    print("SELFTEST FAIL")
    return 1


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--report", type=Path, help="write the machine-readable audit report")
    parser.add_argument("--selftest", action="store_true", help="prove agreement and injected-mismatch behavior")
    args = parser.parse_args()
    if args.selftest:
        return selftest()
    comparisons, pd_rows, malformed = load_surfaces()
    result = evaluate(comparisons, pd_rows, malformed)
    if args.report:
        args.report.parent.mkdir(parents=True, exist_ok=True)
        args.report.write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
        print(f"Wrote audit report: {args.report}")
    print_result(result)
    return 0 if result["diverge"] == 0 and not result["coverage_gaps"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
