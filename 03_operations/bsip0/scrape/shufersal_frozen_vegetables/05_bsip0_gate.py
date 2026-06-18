# -*- coding: utf-8 -*-
"""
BSIP0 EXIT GATE (TASK-239) — the structural barrier between a BSIP0 scrape output
and BSIP1/BSIP2. Runs AFTER the scrape/post-process scripts and BEFORE any
enrichment. A FAIL here blocks the corpus from entering BSIP1.

Why this exists
---------------
The frozen-veg dual-table bug (per-cube 6 kcal selected over per-100g 77 kcal) was
fixed by manually editing the JSON. The fix could not survive the next run because
nothing structurally refused the corrupt corpus. This gate is that refusal: it reads
the BSIP0 output the scrapers produce and fails on the exact defect classes that
previously leaked through.

Checks (all HARD-FAIL unless marked WARN):
  G1  OFF contamination          — Open Food Facts in ANY field/variant  (HARD FAIL)
  G2  nutrition basis            — selected_basis must be per_100g; insufficient = FAIL
  G3  multi-table detection      — competing_table_count>1 with non-per_100g selection = FAIL
  G4  duplicate barcode          — same barcode twice in the corpus  (HARD FAIL)
  G5  conflicting identity       — same barcode, different name_he   (HARD FAIL)
  G6  numeric sanity             — nutrition_implausible() signatures (sat>fat, sodium>2000,
                                   fat-understated, energy>900 kcal)  (HARD FAIL)
  G7  ingredient coverage        — share of products with real ingredients  (WARN below thresh)
  G8  ingredients_raw_source     — presence OR a recorded reason for absence (WARN)
  G9  run-summary contract       — required run-level fields present (HARD FAIL)

Usage:
    python 05_bsip0_gate.py <bsip0_output.json>
    python 05_bsip0_gate.py            # defaults to the frozen-veg v3 output

Exit code 0 = PASS/WARN, 1 = FAIL (gate blocks BSIP1).
"""
from __future__ import annotations

import io
import json
import re
import sys
import pathlib
from collections import Counter, defaultdict
from datetime import datetime, timezone

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")
sys.path.insert(0, str(pathlib.Path(__file__).parent.parent / "_shared"))
import bsip0_nutrition as bn  # noqa: E402

BASE = pathlib.Path(r"C:\Bari")
DEFAULT_INPUT = (
    BASE / "02_products" / "frozen_vegetables" / "bsip0_outputs"
    / "bsip0_shufersal_frozen_vegetables_v3.json"
)

# ── OFF contamination tokens (TASK-238/239) ────────────────────────────────────
# Any of these appearing anywhere in a BSIP0 record (keys OR values) is a hard fail.
# Unknown provenance is acceptable; Open Food Facts is NOT.
OFF_TOKENS = (
    "open food facts",
    "openfoodfacts",
    "open_food_facts",
    ".openfoodfacts.org",
    "off_url",
    "off_image",
    "off_nutrition",
    "off_ingredients",
    "source=openfoodfacts",
)
# Bare "off" / "OFF" is too ambiguous to match as a substring (it hits "coffee",
# "officinalis", "cutoff"…). We match it only as a standalone source/provenance VALUE.
_OFF_BARE_RE = re.compile(r"^\s*off\s*$", re.IGNORECASE)

INGREDIENT_COVERAGE_WARN = 0.50   # below this share → WARN (not all categories carry ingredients)


def _iter_strings(obj, path=""):
    """Yield (json_path, lowercased_string) for every string key and value in a record."""
    if isinstance(obj, dict):
        for k, v in obj.items():
            if isinstance(k, str):
                yield f"{path}.{k}", k.lower()
            yield from _iter_strings(v, f"{path}.{k}")
    elif isinstance(obj, list):
        for i, v in enumerate(obj):
            yield from _iter_strings(v, f"{path}[{i}]")
    elif isinstance(obj, str):
        yield path, obj.lower()


# ── G1: OFF contamination ──────────────────────────────────────────────────────

def gate_off_contamination(records: list[dict], full_doc: dict) -> dict:
    hits: list[str] = []
    # Scan the whole document (records + run-level fields).
    for jpath, s in _iter_strings(full_doc):
        for tok in OFF_TOKENS:
            if tok in s:
                hits.append(f"{jpath}: token '{tok}' in {s[:80]!r}")
        # bare 'off' only as a standalone value in a provenance/source/cache/trace field
        # (matching it as a substring would hit "coffee"/"cutoff"/"officinalis").
        jl = jpath.lower()
        if (any(jl.endswith(suf) for suf in ("source", "panel_source", "identity_source"))
                or "cache" in jl or "trace" in jl or "provenance" in jl) and _OFF_BARE_RE.match(s):
            hits.append(f"{jpath}: standalone 'OFF' value in provenance/source/cache/trace field")
    status = "FAIL" if hits else "PASS"
    msg = ([f"OFF_CONTAMINATION: {len(hits)} hit(s): {hits[:10]}"]
           if hits else ["No Open Food Facts contamination found (all variants scanned)."])
    return {"check": "G1_off_contamination", "status": status, "messages": msg, "hits": hits}


# ── G2/G3: nutrition basis + multi-table ───────────────────────────────────────

def gate_nutrition_basis(records: list[dict]) -> dict:
    fails: list[str] = []
    no_basis: list[str] = []
    multitable_unsafe: list[str] = []
    scored = 0
    for p in records:
        if not p.get("nutrition_raw"):
            continue  # products with no panel are handled by coverage, not basis
        scored += 1
        basis = p.get("nutrition_basis")
        code = p.get("product_code") or p.get("barcode") or "?"
        if not isinstance(basis, dict):
            no_basis.append(str(code))
            continue
        if basis.get("insufficient"):
            fails.append(f"{code}: basis insufficient (competing={basis.get('competing_table_count')}, "
                         f"header={basis.get('selected_table_header')!r})")
            continue
        sel = basis.get("selected_basis")
        comp = basis.get("competing_table_count", 1)
        if sel != "per_100g":
            if comp and comp > 1:
                multitable_unsafe.append(f"{code}: {comp} tables, selected_basis={sel!r} (not per_100g)")
            else:
                # single table whose header is missing/unknown — recorded, not auto-fail,
                # but flagged so a human confirms the lone panel is per-100g.
                no_basis.append(f"{code}: single table, basis={sel!r}")
    fail_all = fails + multitable_unsafe
    status = "FAIL" if fail_all else ("WARN" if no_basis else "PASS")
    msgs = []
    if fail_all:
        msgs.append(f"BASIS_FAIL: {len(fail_all)} product(s) lack a per-100g basis: {fail_all[:10]}")
    if no_basis:
        msgs.append(f"BASIS_WARN: {len(no_basis)} product(s) have unknown/missing basis metadata "
                    f"(legacy records pre-TASK-239 carry none): {no_basis[:8]}")
    if not msgs:
        msgs.append(f"All {scored} paneled products selected a per-100g basis.")
    return {"check": "G2_G3_nutrition_basis", "status": status, "messages": msgs}


# ── G4/G5: duplicate barcode + conflicting identity ────────────────────────────

def gate_identity(records: list[dict]) -> dict:
    by_barcode: dict[str, list] = defaultdict(list)
    for p in records:
        bc = str(p.get("barcode") or p.get("barcode_ld") or p.get("barcode_data_attr") or "").strip()
        if bc:
            by_barcode[bc].append(p)
    dup, conflict = [], []
    for bc, group in by_barcode.items():
        if len(group) > 1:
            names = {str(g.get("name_he") or g.get("name") or "") for g in group}
            dup.append(f"{bc} x{len(group)}")
            if len(names) > 1:
                conflict.append(f"{bc}: {sorted(names)[:3]}")
    status = "FAIL" if (dup or conflict) else "PASS"
    msgs = []
    if dup:
        msgs.append(f"DUPLICATE_BARCODE: {len(dup)}: {dup[:10]}")
    if conflict:
        msgs.append(f"CONFLICTING_IDENTITY: {len(conflict)} barcode(s) map to >1 name: {conflict[:10]}")
    if not msgs:
        msgs.append(f"No duplicate/conflicting barcodes across {len(by_barcode)} keyed products.")
    return {"check": "G4_G5_identity", "status": status, "messages": msgs}


# ── G6: numeric sanity ─────────────────────────────────────────────────────────

def _nutrition_for_guard(p: dict) -> dict:
    """Map the scraper's {hebrew_label: 'value unit'} dict to the *_raw keys the
    shared guard understands, using the shared label classifier."""
    nutr = p.get("nutrition_raw") or {}
    out: dict = {}
    keymap = {"energy": "energy_kcal_raw", "fat": "fat_raw", "saturated_fat": "saturated_fat_raw",
              "carbs": "carbs_raw", "sugar": "sugar_raw", "protein": "protein_raw",
              "sodium": "sodium_raw", "fiber": "fiber_raw"}
    for label, value in nutr.items():
        field = bn.classify_nutr_label(label)
        if field in keymap and keymap[field] not in out:
            out[keymap[field]] = value
    return out


def gate_numeric_sanity(records: list[dict]) -> dict:
    flagged = []
    for p in records:
        if not p.get("nutrition_raw"):
            continue
        reason = bn.nutrition_implausible(_nutrition_for_guard(p))
        if reason:
            code = p.get("product_code") or p.get("barcode") or "?"
            flagged.append(f"{code}: {reason}")
    status = "FAIL" if flagged else "PASS"
    msgs = ([f"NUMERIC_SANITY: {len(flagged)} implausible panel(s): {flagged[:8]}"]
            if flagged else ["All panels passed numeric sanity (no implausible signatures)."])
    return {"check": "G6_numeric_sanity", "status": status, "messages": msgs}


# ── G7/G8: ingredient coverage + raw-source preservation ───────────────────────

def gate_ingredients(records: list[dict]) -> dict:
    total = len(records)
    with_ing = sum(1 for p in records if str(p.get("ingredients_raw") or "").strip())
    cov = with_ing / total if total else 0.0
    no_src = [p.get("product_code") or "?" for p in records
              if not p.get("ingredients_raw_source")
              and not p.get("ingredients_raw_source_reason")]
    status = "WARN" if (cov < INGREDIENT_COVERAGE_WARN or no_src) else "PASS"
    msgs = [f"Ingredient coverage: {with_ing}/{total} ({cov:.0%})."]
    if cov < INGREDIENT_COVERAGE_WARN:
        msgs.append(f"COVERAGE_WARN: ingredient coverage {cov:.0%} < {INGREDIENT_COVERAGE_WARN:.0%}.")
    if no_src:
        msgs.append(f"RAW_SOURCE_WARN: {len(no_src)} product(s) carry neither an "
                    f"ingredients_raw_source nor an absence reason (TASK-239 follow-up #6).")
    return {"check": "G7_G8_ingredients", "status": status, "messages": msgs}


# ── G9: run-summary contract ───────────────────────────────────────────────────

def gate_run_summary(full_doc: dict) -> dict:
    required = ["run_id", "category", "retailer", "panel_source", "provenance", "products"]
    missing = [f for f in required if f not in full_doc]
    prov = full_doc.get("provenance") or {}
    if isinstance(prov, dict) and "source" not in prov:
        missing.append("provenance.source")
    status = "FAIL" if missing else "PASS"
    msgs = ([f"RUN_SUMMARY: missing required field(s): {missing}"]
            if missing else ["Run-summary contract satisfied."])
    return {"check": "G9_run_summary", "status": status, "messages": msgs}


# ── Runner ─────────────────────────────────────────────────────────────────────

def run_gate(doc: dict) -> dict:
    records = doc.get("products") if isinstance(doc, dict) else doc
    if not isinstance(records, list):
        records = []
    checks = [
        gate_off_contamination(records, doc),
        gate_nutrition_basis(records),
        gate_identity(records),
        gate_numeric_sanity(records),
        gate_ingredients(records),
        gate_run_summary(doc),
    ]
    order = {"FAIL": 0, "WARN": 1, "PASS": 2}
    overall = min((c["status"] for c in checks), key=lambda s: order[s])
    return {
        "gate": "bsip0_exit_gate_v1",
        "task": "TASK-239",
        "ran_at": datetime.now(timezone.utc).isoformat(),
        "product_count": len(records),
        "overall_status": overall,
        "summary": {
            "FAIL": sum(1 for c in checks if c["status"] == "FAIL"),
            "WARN": sum(1 for c in checks if c["status"] == "WARN"),
            "PASS": sum(1 for c in checks if c["status"] == "PASS"),
        },
        "checks": checks,
    }


def main(argv: list[str]) -> int:
    path = pathlib.Path(argv[1]) if len(argv) > 1 else DEFAULT_INPUT
    if not path.exists():
        print(f"INPUT NOT FOUND: {path}")
        return 1
    doc = json.loads(path.read_text(encoding="utf-8"))
    result = run_gate(doc)
    print("=" * 64)
    print(f"BSIP0 EXIT GATE — {path.name}")
    print("=" * 64)
    for c in result["checks"]:
        print(f"[{c['status']:4}] {c['check']}")
        for m in c["messages"]:
            print(f"        - {m}")
    print("-" * 64)
    print(f"OVERALL: {result['overall_status']}  "
          f"(FAIL={result['summary']['FAIL']} WARN={result['summary']['WARN']} "
          f"PASS={result['summary']['PASS']}) over {result['product_count']} products")
    print("=" * 64)
    return 0 if result["overall_status"] != "FAIL" else 1


if __name__ == "__main__":
    sys.exit(main(sys.argv))
