"""BSIP0 manifest-coverage acceptance gate (TASK-617).

Prevents the TASK-615 failure class: a scrape retained real nutrition data
in a JSON shape ``build_manifest.py``'s scanner did not recognize (no
``nutrition_raw_source.rows`` dict on any object), so ~120 captures sat on
disk fully invisible to ``capture_manifest.json`` and to census coverage --
discovered only at a later consolidation, not at scrape time. Lesson
(memory ``scrape_capture_canonical_format``): a scrape's real acceptance test
is "manifest/census coverage RISES", not "files were written".

This gate makes that acceptance test mechanical, in two modes plus a
selftest:

--files PATH [PATH ...]
    Per-file ingestion check, run right after a scrape. Rebuilds the
    manifest fresh, scans each given file's own JSON for objects carrying a
    GTIN plus a nutrition-hint key, and FAILS (naming the file + GTINs) if
    build_manifest.py produced ZERO manifest records for that file despite
    it clearly containing nutrition-shaped data. A capture written in a
    shape build_manifest can't scan fails loudly here instead of silently
    passing because "the file exists on disk".

--corpus (default)
    Corpus-wide check. Rebuilds the manifest fresh, recomputes served-product
    coverage per shelf exactly like build_census.py, and FAILS if any served
    product's GTIN has no canonical capture AND is not on the documented
    known_not_found_allowlist.json (the genuinely-unavailable products: NOT
    a silent pass, an explicit sourced entry per product).

--selftest
    The acceptance test for this gate itself: proves detection FAILS on a
    synthetic non-canonical capture and PASSES on a canonical one. Runs
    against in-memory synthetic data only -- never touches the real corpus,
    the real manifest, or the real allowlist.

This program is read-only on served JSON/scores/captures. ``--files`` and
``--corpus`` invoke build_manifest.py to refresh capture_manifest.json --
that is build_manifest's own declared output (its docstring: "writes only
its declared manifest artifact"), not a new write introduced here.
coverage_gate.py itself writes nothing. build_manifest.py's scan behavior is
never modified or reimplemented independently: is_canonical_capture() below
is the same predicate as build_manifest.py's membership check (its line
~106), kept identical on purpose so this gate can't silently drift from the
scanner it is asserting against.
"""
from __future__ import annotations

import argparse
import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
MANIFEST_DIR = ROOT / "03_operations/bsip0/manifest"
BUILD_MANIFEST = MANIFEST_DIR / "build_manifest.py"
MANIFEST_PATH = MANIFEST_DIR / "capture_manifest.json"
ALLOWLIST_PATH = MANIFEST_DIR / "known_not_found_allowlist.json"
FRONTEND_DIR = ROOT / "bari-web/src/data/comparisons"

sys.path.insert(0, str(MANIFEST_DIR))
import build_manifest as bm  # noqa: E402  -- reuse walk/scalar/GTIN_KEYS, never re-architect the scanner

# Keys that, alongside a GTIN, mark an object as "trying to be a nutrition
# capture" even when its shape doesn't match build_manifest's strict
# nutrition_raw_source.rows predicate. Deliberately narrower than "any dict
# with a GTIN" so identity/price-feed records (gtin + price + store, e.g. the
# il_prices integration client) are never flagged -- this catches genuine
# nutrition data build_manifest can't see, it does not widen what counts as
# a capture.
NUTRITION_HINT_KEYS = {
    "nutrition_raw_source", "nutrition_raw", "nutrition", "served_nutrition",
    "energy_kcal", "energy_kcal_raw", "protein_raw", "carbs_raw", "fat_raw",
    "fiber_raw", "sodium_raw", "sugar_raw", "saturated_fat_raw",
    "ingredients_raw_he", "ingredients_raw",
}


def is_canonical_capture(obj: dict) -> bool:
    """build_manifest.py's membership predicate, verbatim (its line ~106):
    a dict is a canonical capture iff it has a dict ``nutrition_raw_source``
    whose ``rows`` is a list. Never reimplemented independently."""
    raw = obj.get("nutrition_raw_source")
    return isinstance(raw, dict) and isinstance(raw.get("rows"), list)


def find_capture_like(data) -> list[tuple[str, str, bool]]:
    """Walk a loaded JSON value; return (gtin, object_path, is_canonical) for
    every dict carrying a GTIN plus at least one nutrition-hint key."""
    hits = []
    for obj, path in bm.walk(data, []):
        if not isinstance(obj, dict):
            continue
        gtin = bm.scalar(obj, bm.GTIN_KEYS)
        if not gtin:
            continue
        if not (NUTRITION_HINT_KEYS & obj.keys()):
            continue
        hits.append((gtin, bm.pointer(path), is_canonical_capture(obj)))
    return hits


def rebuild_manifest() -> dict:
    result = subprocess.run(
        [sys.executable, str(BUILD_MANIFEST)],
        capture_output=True, text=True, cwd=str(ROOT),
    )
    if result.returncode != 0:
        raise RuntimeError(f"build_manifest.py failed: {result.stderr}")
    return json.loads(MANIFEST_PATH.read_text(encoding="utf-8"))


def check_files(paths: list[str]) -> int:
    manifest = rebuild_manifest()
    by_file: dict[str, list] = {}
    for r in manifest["records"]:
        by_file.setdefault(r["capture_file"], []).append(r)

    failures = []
    checked = 0
    for raw_path in paths:
        p = Path(raw_path)
        if not p.is_absolute():
            p = ROOT / p
        if not p.exists():
            failures.append(f"{raw_path}: file does not exist")
            continue
        try:
            data = json.loads(p.read_text(encoding="utf-8"))
        except (json.JSONDecodeError, UnicodeDecodeError) as exc:
            failures.append(f"{raw_path}: unreadable JSON ({exc})")
            continue
        resolved = p.resolve()
        rel = resolved.relative_to(ROOT).as_posix() if resolved.is_relative_to(ROOT) else raw_path
        hits = find_capture_like(data)
        checked += 1
        if not hits:
            continue  # not a capture file at all (no GTIN+nutrition content) -- nothing to assert
        records_for_file = by_file.get(rel, [])
        if not records_for_file:
            gtins = sorted({g for g, _, _ in hits})
            failures.append(
                f"{rel}: contains {len(hits)} GTIN+nutrition-shaped object(s) "
                f"(GTINs: {', '.join(gtins)}) but build_manifest.py produced "
                f"ZERO manifest records for this file -- capture written in a "
                f"shape the scanner can't see (TASK-615 failure class)."
            )

    print(json.dumps({"mode": "files", "files_checked": checked, "failures": len(failures)}, ensure_ascii=False))
    for f in failures:
        print(f"FAIL: {f}")
    if not failures:
        print("PASS: all checked files produced >=1 manifest record where GTIN+nutrition content was present.")
    return 1 if failures else 0


def gtin_of(product: dict):
    for k in ("gtin", "barcode", "ean", "upc", "product_code", "product_id"):
        if product.get(k) is not None:
            return str(product[k])
    return None


def load_allowlist() -> dict[tuple[str, str], dict]:
    payload = json.loads(ALLOWLIST_PATH.read_text(encoding="utf-8"))
    return {(e["shelf"], str(e["gtin"])): e for e in payload["entries"]}


def check_corpus() -> int:
    manifest = rebuild_manifest()
    canon = {str(r["gtin"]) for r in manifest["records"] if r["canonical"] and r["gtin"]}
    allowlist = load_allowlist()

    total = covered = allowlisted = 0
    per_shelf = []
    unexplained = []
    for f in sorted(FRONTEND_DIR.glob("*_frontend_v*.json")):
        data = json.loads(f.read_text(encoding="utf-8"))
        products = data.get("products", data if isinstance(data, list) else [])
        shelf_total = len(products)
        shelf_covered = 0
        shelf_gap = []
        for prod in products:
            g = gtin_of(prod)
            if g in canon:
                shelf_covered += 1
                continue
            key = (f.stem, g)
            if key in allowlist:
                allowlisted += 1
                continue
            shelf_gap.append((g, prod.get("name") or prod.get("name_he") or prod.get("brand")))
        total += shelf_total
        covered += shelf_covered
        per_shelf.append((f.stem, shelf_total, shelf_covered, len(shelf_gap)))
        unexplained.extend((f.stem, g, name) for g, name in shelf_gap)

    print(json.dumps({
        "mode": "corpus",
        "served_total": total,
        "has_canonical_capture": covered,
        "allowlisted_not_found": allowlisted,
        "unexplained_missing": len(unexplained),
        "allowlist_entries": len(allowlist),
    }, ensure_ascii=False))
    for shelf, shelf_total, shelf_covered, shelf_gap in per_shelf:
        if shelf_gap:
            print(f"  {shelf}: {shelf_covered}/{shelf_total} covered, {shelf_gap} unexplained gap")
    for shelf, g, name in unexplained:
        print(f"FAIL: {shelf}: GTIN {g} ({name}) has no canonical capture and is NOT on {ALLOWLIST_PATH.name}")
    if not unexplained:
        print(f"PASS: {covered}/{total} served products have a canonical capture; "
              f"remaining {allowlisted} are on the documented NOT_FOUND allowlist.")

    return 1 if unexplained else 0


def selftest() -> int:
    """Synthetic-only acceptance test: never touches the real corpus, the
    real manifest, or the real allowlist."""
    non_canonical = {
        "barcode": "9999999999999",
        "name": "SELFTEST non-canonical widget",
        "energy_kcal": 100,
        "protein": 5,
        "nutrition": {"energy": 100},
    }
    canonical = {
        "barcode": "9999999999998",
        "name": "SELFTEST canonical widget",
        "nutrition_raw_source": {"rows": [{"label": "Energy", "value": "100 kcal"}]},
    }

    # Case A: shape build_manifest can't scan. Must be detected as
    # capture-like (GTIN + nutrition hints present) but NOT canonical-shape,
    # meaning build_manifest's own predicate (is_canonical_capture, identical
    # to its line ~106) would emit zero records for a file holding only this
    # object -- exactly the un-ingested-file condition check_files() flags.
    hits_a = find_capture_like(non_canonical)
    case_a_detected_as_capture_like = len(hits_a) == 1 and hits_a[0][2] is False
    would_manifest_record_a = is_canonical_capture(non_canonical)
    gate_fails_on_a = bool(hits_a) and not would_manifest_record_a

    # Case B: canonical shape. Must be detected as capture-like AND
    # canonical-shape, i.e. build_manifest WOULD produce a record.
    hits_b = find_capture_like(canonical)
    case_b_detected_as_capture_like = len(hits_b) == 1 and hits_b[0][2] is True
    would_manifest_record_b = is_canonical_capture(canonical)
    gate_passes_on_b = bool(hits_b) and would_manifest_record_b

    ok = case_a_detected_as_capture_like and gate_fails_on_a and case_b_detected_as_capture_like and gate_passes_on_b
    print(json.dumps({
        "mode": "selftest",
        "case_a_noncanonical_flagged_capture_like": case_a_detected_as_capture_like,
        "case_a_gate_would_fail": gate_fails_on_a,
        "case_b_canonical_flagged_capture_like": case_b_detected_as_capture_like,
        "case_b_gate_would_pass": gate_passes_on_b,
        "result": "PASS" if ok else "FAIL",
    }, ensure_ascii=False))
    return 0 if ok else 1


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--files", nargs="+", help="Just-written capture files to check for manifest ingestion")
    parser.add_argument("--corpus", action="store_true", help="Corpus-wide per-shelf coverage check (default)")
    parser.add_argument("--selftest", action="store_true", help="Run the acceptance test (synthetic, no repo I/O)")
    args = parser.parse_args()

    if args.selftest:
        return selftest()
    if args.files:
        return check_files(args.files)
    return check_corpus()


if __name__ == "__main__":
    raise SystemExit(main())
