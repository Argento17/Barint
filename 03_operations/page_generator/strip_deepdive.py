"""
strip_deepdive.py — TASK-411

Strips deep-dive narrative keys from three live comparison JSON files so their
product drill-down matches the golden standard (brined-cheeses / juices).

Keys removed (wherever they appear — product top level AND inside expansion{}):
  consumerExplanation
  bestUseCases
  consumerTakeaway
  bariInterpretation
  bottomLine          (expansion-level only; confirmed never rendered — Adversarial-QA follow-up)

HARD INVARIANT: product count, scores, grades, positiveSignals, limitingFactors,
rowVerdict, expansion.comparisonContext, expansion.nutrition, expansion.ingredients,
and imageUrl must be byte-identical before and after for every product.

Usage:
  python strip_deepdive.py [--dry-run]
"""

import json
import sys
import copy

# ── Target files ─────────────────────────────────────────────────────────────

BASE = r"C:\bari_drillstrip\bari-web\src\data\comparisons"

TARGETS = [
    f"{BASE}\\cheese_frontend_v4.json",
    f"{BASE}\\bread_frontend_v3.json",
    f"{BASE}\\cakes_hard_cookies_frontend_v1.json",
]

# Keys to remove from product top level
TOP_REMOVE = {
    "consumerExplanation",
    "bestUseCases",
    "consumerTakeaway",
    "bariInterpretation",
}

# Keys to remove from product["expansion"] if present
EXPANSION_REMOVE = {
    "consumerExplanation",
    "bestUseCases",
    "consumerTakeaway",
    "bariInterpretation",
    "bottomLine",       # confirmed not rendered by expansion-section.tsx
}

# Invariant fields: must be byte-identical after stripping
TOP_INVARIANT = [
    "id",
    "barcode",
    "score",
    "grade",
    "positiveSignals",   # some categories carry at top level
    "limitingFactors",   # some categories carry at top level
    "rowVerdict",
    "imageUrl",
]

EXPANSION_INVARIANT = [
    "comparisonContext",
    "nutrition",
    "ingredients",
    "positiveSignals",
    "limitingFactors",
]

# Keys that must NOT appear after stripping (deep-dive residual check)
FORBIDDEN_AFTER = {
    "consumerExplanation",
    "bestUseCases",
    "consumerTakeaway",
    "bariInterpretation",
    "bottomLine",
    "whyRated",
    "good",
    "watchOut",
}

DRY_RUN = "--dry-run" in sys.argv


def _serialize(val) -> str:
    """Canonical JSON serialisation for comparison."""
    return json.dumps(val, ensure_ascii=False, sort_keys=False)


def check_invariants(before: dict, after: dict, file_label: str, idx: int) -> None:
    """Assert byte-identical survival of all invariant fields. Raises on violation."""
    # Top-level invariants
    for field in TOP_INVARIANT:
        b = before.get(field)
        a = after.get(field)
        if _serialize(b) != _serialize(a):
            raise AssertionError(
                f"INVARIANT FAIL [{file_label}] product[{idx}] "
                f"top field '{field}' changed:\n"
                f"  BEFORE: {_serialize(b)[:200]}\n"
                f"  AFTER:  {_serialize(a)[:200]}"
            )
    # Expansion-level invariants
    b_exp = before.get("expansion", {})
    a_exp = after.get("expansion", {})
    for field in EXPANSION_INVARIANT:
        b = b_exp.get(field)
        a = a_exp.get(field)
        if _serialize(b) != _serialize(a):
            raise AssertionError(
                f"INVARIANT FAIL [{file_label}] product[{idx}] "
                f"expansion field '{field}' changed:\n"
                f"  BEFORE: {_serialize(b)[:200]}\n"
                f"  AFTER:  {_serialize(a)[:200]}"
            )


def check_no_forbidden(product: dict, file_label: str, idx: int) -> None:
    """Assert no forbidden deep-dive key exists anywhere in the stripped product."""
    def _scan(obj, path: str):
        if isinstance(obj, dict):
            for k, v in obj.items():
                full = f"{path}.{k}"
                if k in FORBIDDEN_AFTER:
                    raise AssertionError(
                        f"RESIDUAL FAIL [{file_label}] product[{idx}] "
                        f"found forbidden key '{k}' at path '{full}'"
                    )
                _scan(v, full)
        elif isinstance(obj, list):
            for i, item in enumerate(obj):
                _scan(item, f"{path}[{i}]")

    _scan(product, "product")


def strip_product(product: dict) -> tuple[dict, dict]:
    """
    Return (stripped_product, removal_counts).
    removal_counts: {key: count_removed}
    """
    stripped = copy.deepcopy(product)
    counts: dict[str, int] = {k: 0 for k in (TOP_REMOVE | EXPANSION_REMOVE)}

    # Remove from top level
    for key in TOP_REMOVE:
        if key in stripped:
            del stripped[key]
            counts[key] += 1

    # Remove from expansion if present
    if "expansion" in stripped and isinstance(stripped["expansion"], dict):
        for key in EXPANSION_REMOVE:
            if key in stripped["expansion"]:
                del stripped["expansion"][key]
                counts[key] += 1

    return stripped, counts


def process_file(path: str) -> dict:
    """
    Load, strip, validate, and (unless dry-run) write a single file.
    Returns a stats dict for reporting.
    """
    label = path.split("\\")[-1]

    with open(path, encoding="utf-8") as f:
        raw = f.read()

    data_before = json.loads(raw)
    products_before = data_before.get("products", [])
    count_before = len(products_before)

    # Accumulate per-key removal counts across all products (all removable keys)
    all_remove_keys = TOP_REMOVE | EXPANSION_REMOVE
    total_removed: dict[str, int] = {k: 0 for k in all_remove_keys}

    data_after = copy.deepcopy(data_before)
    products_after = []

    for idx, product in enumerate(products_before):
        stripped, counts = strip_product(product)

        for k, n in counts.items():
            total_removed[k] += n

        # INVARIANT CHECK: compare stripped against original
        check_invariants(product, stripped, label, idx)

        products_after.append(stripped)

    # Product count invariant
    assert len(products_after) == count_before, (
        f"INVARIANT FAIL [{label}] product count changed: "
        f"{count_before} → {len(products_after)}"
    )

    data_after["products"] = products_after

    # RESIDUAL CHECK: no forbidden key anywhere in any product
    for idx, product in enumerate(products_after):
        check_no_forbidden(product, label, idx)

    residuals_found = 0  # reaching here means 0 residuals

    # Serialise output (match existing file style: ensure_ascii=False, indent=2)
    output = json.dumps(data_after, ensure_ascii=False, indent=2)
    # Trailing newline only if original had one
    if raw.endswith("\n"):
        output += "\n"

    if not DRY_RUN:
        with open(path, "w", encoding="utf-8", newline="\n") as f:
            f.write(output)

    return {
        "file": label,
        "product_count_before": count_before,
        "product_count_after": len(products_after),
        "count_match": count_before == len(products_after),
        "removed": total_removed,
        "residuals": residuals_found,
        "invariant": "PASS",
        "written": not DRY_RUN,
    }


def main():
    print("=" * 70)
    print(f"strip_deepdive.py  {'DRY RUN' if DRY_RUN else 'LIVE WRITE'}")
    print("=" * 70)

    all_ok = True
    results = []

    for path in TARGETS:
        try:
            stats = process_file(path)
            results.append(stats)
            print(f"\n[OK] {stats['file']}")
            print(f"     products: {stats['product_count_before']} before == {stats['product_count_after']} after  COUNT={stats['count_match']}")
            for key, n in stats["removed"].items():
                print(f"     removed '{key}': {n}")
            print(f"     deep-dive residuals: {stats['residuals']}")
            print(f"     invariant check: {stats['invariant']}")
            print(f"     written to disk: {stats['written']}")
        except Exception as exc:
            all_ok = False
            print(f"\n[FAIL] {path.split(chr(92))[-1]}")
            print(f"       {exc}")

    print("\n" + "=" * 70)
    if all_ok:
        print("ALL FILES PASSED — deep-dive stripped, invariants held, 0 residuals.")
    else:
        print("ONE OR MORE FILES FAILED — see errors above. No partial writes.")
        sys.exit(1)

    print("=" * 70)


if __name__ == "__main__":
    main()
