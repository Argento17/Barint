"""
TASK-212B: Frontend schema validator (v2 with warning categorization).
Enforces BariProductVM v4 schema rules across all live frontend JSON files.

Warning categories:
  LAUNCH_BLOCKING — must be resolved before launch
  ACCEPTED_BACKLOG — known, documented, tracked
  OPTIONAL_NOISE — pre-existing gaps that do not affect UX or auditability

Exit code: 0 = pass (no errors), 1 = has errors
"""
import json, sys
from pathlib import Path

COMPARISONS = Path(r"C:\Bari\bari-web\src\data\comparisons")

LIVE_FILES = [
    "bread_frontend_v2.json",
    "butter_frontend_v2.json",
    "cereals_frontend_v2.json",
    "cheese_frontend_v3.json",
    "granola_frontend_v1.json",
    "hard_cheeses_frontend_v2.json",
    "hummus_frontend_v5.json",
    "juices_frontend_v3.json",
    "maadanim_frontend_v3.json",
    "olive_oil_frontend_v1.json",
    "salty_snacks_frontend_v2.json",
    "snacks_frontend_v2.json",
    "yogurts_frontend_v3.json",
]

# ── BariProductVM v4 Schema Definition ─────────────────────────────
# REQUIRED: fail on null/empty
# RECOMMENDED: warn
# OPTIONAL: tolerated null (accepted backlog)

REQUIRED_FIELDS = ["id", "name", "imageUrl", "score", "grade"]
RECOMMENDED_FIELDS = ["barcode", "retailer"]
OPTIONAL_FIELDS = ["brand", "novaGroup", "confidence"]

# ── Global product ID tracker ───────────────────────────────────────
GLOBAL_IDS = {}


def validate():
    errors = []
    warn_blocking = []
    warn_backlog = []
    warn_noise = []
    total_products = 0

    # ── 1. Orphan check ──────────────────────────────────────────────
    all_files = set(f.name for f in COMPARISONS.iterdir() if f.suffix == ".json")
    known = set(LIVE_FILES) | {"crackers_staged_v1.json"}
    orphans = set()
    for fn in all_files:
        if fn not in known and not (COMPARISONS / "archive" / fn).exists():
            orphans.add(fn)
    for fn in sorted(orphans):
        errors.append(f"ORPHAN_FILE: {fn} in live data path (should be in archive/)")

    # ── 2. File-level checks ────────────────────────────────────────
    for fn in LIVE_FILES:
        path = COMPARISONS / fn
        if not path.exists():
            errors.append(f"MISSING_FILE: {fn} (expected in comparisons/)")
            continue

        with open(path, encoding="utf-8") as f:
            try:
                data = json.load(f)
            except json.JSONDecodeError as e:
                errors.append(f"INVALID_JSON: {fn}: {e}")
                continue

        meta = data.get("_meta", {})
        products = data.get("products", [])
        total_products += len(products)

        # product_count vs array length
        meta_count = meta.get("product_count")
        if meta_count is not None and meta_count != len(products):
            errors.append(f"COUNT_MISMATCH: {fn}: meta.product_count={meta_count}, array={len(products)}")

        # category slug
        if not meta.get("category"):
            errors.append(f"MISSING_CATEGORY: {fn}: _meta.category is required")

        # schema string
        schema = meta.get("schema", "")
        if "BariProductVM" not in schema:
            errors.append(f"SCHEMA_MISMATCH: {fn}: _meta.schema={schema!r}")

        # generated timestamp
        if not meta.get("generated"):
            warn_backlog.append(f"MISSING_GENERATED_TIMESTAMP: {fn}")

        # ── 3. Product-level checks ────────────────────────────────
        seen_ids = {}
        for i, product in enumerate(products):
            pid = product.get("id") or f"[index {i}]"

            # Required fields
            for field in REQUIRED_FIELDS:
                val = product.get(field)
                if val is None or (isinstance(val, str) and not val.strip()):
                    errors.append(f"MISSING_REQUIRED: {fn}:{pid}: {field} is null/empty")

            # Duplicate IDs within file
            if product.get("id"):
                if pid in seen_ids:
                    errors.append(f"DUPLICATE_ID: {fn}: pid={pid} at index {seen_ids[pid]} and {i}")
                else:
                    seen_ids[pid] = i

            # Cross-file duplicate IDs
            if product.get("id"):
                if pid in GLOBAL_IDS:
                    prev_fn, prev_i = GLOBAL_IDS[pid]
                    errors.append(f"CROSS_FILE_DUPLICATE: pid={pid} in {prev_fn}[{prev_i}] and {fn}[{i}]")
                else:
                    GLOBAL_IDS[pid] = (fn, i)

            # Recommended: barcode
            barcode = product.get("barcode")
            src_trace = product.get("source_traceability_status")
            if not barcode:
                warn_backlog.append(f"MISSING_BARCODE: {fn}:{pid} (trace_status={src_trace})")

            # Recommended: retailer
            retailer = product.get("retailer")
            retailers = product.get("retailers")  # juices uses array form
            if not retailer and not retailers:
                warn_backlog.append(f"MISSING_RETAILER: {fn}:{pid}")

            # Optional: brand, novaGroup, confidence
            for field in OPTIONAL_FIELDS:
                if product.get(field) is None:
                    warn_noise.append(f"{field.upper()}_NULL: {fn}:{pid}")

    # ── 4. Report ──────────────────────────────────────────────────
    print(f"Validation report: {total_products} products across {len(LIVE_FILES)} files")
    print(f"  Errors:              {len(errors)}")
    print(f"  Launch-blocking warnings: {len(warn_blocking)}")
    print(f"  Accepted-backlog warnings:{len(warn_backlog)}")
    print(f"  Optional-field noise:    {len(warn_noise)}")
    print()

    if errors:
        print("ERRORS (must fix):")
        for e in errors:
            print(f"  FAIL  {e}")
        print()

    if warn_blocking:
        print("LAUNCH-BLOCKING WARNINGS:")
        for w in warn_blocking:
            print(f"  WARN  {w}")
        print()

    if warn_backlog:
        print("ACCEPTED BACKLOG (known, tracked, not blocking):")
        # Summarize by type
        by_type = {}
        for w in warn_backlog:
            key = w.split(":")[0]
            by_type.setdefault(key, []).append(w)
        for key, items in sorted(by_type.items()):
            print(f"  {key}: {len(items)} occurrences")
            # Show first 3 as examples
            for ex in items[:3]:
                print(f"    e.g. {ex}")
            if len(items) > 3:
                print(f"    ... and {len(items) - 3} more")
        print()

    if warn_noise:
        print("OPTIONAL-FIELD NOISE (tolerated, accepted backlog):")
        by_type = {}
        for w in warn_noise:
            key = w.split("_")[0]
            by_type.setdefault(key, []).append(w)
        for key, items in sorted(by_type.items()):
            print(f"  {key}: {len(items)} occurrences")
        print()

    if not errors:
        print("ALL CHECKS PASSED.")
        print()

    sys.exit(1 if errors else 0)


if __name__ == "__main__":
    validate()
