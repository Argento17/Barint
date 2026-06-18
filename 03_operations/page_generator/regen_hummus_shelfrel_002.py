#!/usr/bin/env python3
"""
regen_hummus_shelfrel_002.py — TASK-289 hummus regen from run_hummus_shelfrel_002.

Steps:
  1. Run generate_page.py via the hummus_shelfrel_002.json config → temp output
     (score, grade, _meta, confidence, nutrition, bariInterpretation all fresh).
  2. Load the current live v5 JSON as the "copy baseline".
  3. For each product in the fresh output, overlay PRESERVED copy fields from v5
     where the same barcode exists:
       - insightLine
       - rowVerdict
       - consumerTakeaway
       - expansion.positiveSignals
       - expansion.limitingFactors
       - expansion.unknowns
       - expansion.caveats
       - expansion.consumerExplanation (if present)
       - _product_type
       - glassBox
       - d3_processing_signal
     Fields NOT in v5 for a barcode (new products) stay as PENDING_COPY.
  4. Update _meta with new run metadata fields and flag copy-mismatch products.
  5. Write merged output to the live path.
  6. Run run_gates.py on the output and report exit code.

Does NOT commit, does NOT push.
Does NOT invent copy. No authored Hebrew text written.
"""

import hashlib
import json
import os
import subprocess
import sys
import tempfile
from pathlib import Path
from datetime import datetime, timezone

# ---------------------------------------------------------------------------
# Paths
# ---------------------------------------------------------------------------

ROOT = Path(r"C:\Bari")
CONFIG = ROOT / "03_operations/page_generator/configs/hummus_shelfrel_002.json"
GENERATE_SCRIPT = ROOT / "03_operations/page_generator/generate_page.py"
GATES_SCRIPT = ROOT / "03_operations/page_generator/gates/run_gates.py"
LIVE_V5 = Path(r"C:\Bari\bari-web\src\data\comparisons\hummus_frontend_v5.json")
OUTPUT_PATH = LIVE_V5  # overwrite in place

RUN_SUMMARY = ROOT / "02_products/hummus/intelligence_bsip2/run_hummus_shelfrel_002/run_summary.json"
GRADE_BOUNDARY = ROOT / "01_framework/governance/grade_boundary_policy_v1.json"

GENERATOR_VERSION = "1.1.0"
TASK = "TASK-289"

# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def load_json(path):
    with open(path, encoding="utf-8") as f:
        return json.load(f)


def sha256_file(path):
    h = hashlib.sha256()
    with open(str(path), "rb") as f:
        h.update(f.read())
    return h.hexdigest()


# ---------------------------------------------------------------------------
# Copy fields to preserve from the v5 baseline (per barcode)
# ---------------------------------------------------------------------------

# Top-level fields
COPY_TOPLEVEL = [
    "insightLine",
    "rowVerdict",
    "consumerTakeaway",
    "_product_type",
    "glassBox",
    "d3_processing_signal",
]

# expansion sub-fields
COPY_EXPANSION = [
    "positiveSignals",
    "limitingFactors",
    "unknowns",
    "caveats",
    "consumerExplanation",
]


def build_v5_index(v5_data):
    """Build barcode -> product dict from v5 JSON."""
    idx = {}
    for p in v5_data.get("products", []):
        bc = str(p.get("barcode", "")).strip()
        if bc:
            idx[bc] = p
    return idx


def overlay_copy(fresh_product, v5_product):
    """
    Overlay copy fields from v5_product onto fresh_product in-place.
    Only overlays if the v5 field is not None, not empty, and not PENDING_COPY.
    """
    for field in COPY_TOPLEVEL:
        val = v5_product.get(field)
        if val is not None and val != "PENDING_COPY" and val != "":
            fresh_product[field] = val

    # expansion sub-fields
    fresh_exp = fresh_product.get("expansion") or {}
    v5_exp = v5_product.get("expansion") or {}
    for field in COPY_EXPANSION:
        val = v5_exp.get(field)
        if val is None:
            continue
        # Lists: keep if non-empty and not ["PENDING_COPY"]
        if isinstance(val, list):
            if val and val != ["PENDING_COPY"]:
                fresh_exp[field] = val
        elif isinstance(val, dict):
            # consumerExplanation dict: keep if has non-PENDING keys
            has_real = any(
                v not in (None, "PENDING_COPY", ["PENDING_COPY"])
                for v in val.values()
            )
            if has_real:
                fresh_exp[field] = val
        elif val and val != "PENDING_COPY":
            fresh_exp[field] = val

    fresh_product["expansion"] = fresh_exp
    return fresh_product


# ---------------------------------------------------------------------------
# Grade scale (must match generate_page.py — floor policy)
# ---------------------------------------------------------------------------

GRADE_SCALE = [
    ("S", 90), ("A", 80), ("B", 65), ("C", 50), ("D", 35), ("E", 0),
]


def score_to_grade(score):
    if score is None:
        return None
    for grade, threshold in GRADE_SCALE:
        if score >= threshold:
            return grade
    return "E"


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def main():
    # Force UTF-8
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    if hasattr(sys.stderr, "reconfigure"):
        sys.stderr.reconfigure(encoding="utf-8", errors="replace")

    print(f"=== {TASK} hummus regen from run_hummus_shelfrel_002 ===")

    # ------------------------------------------------------------------
    # Step 1: Run generator to temp file
    # ------------------------------------------------------------------
    with tempfile.NamedTemporaryFile(
        suffix="_hummus_fresh.json",
        delete=False,
        mode="w",
        encoding="utf-8",
    ) as tf:
        temp_path = tf.name

    timestamp = "2026-06-16T00:00:00Z"  # fixed for reproducibility

    gen_cmd = [
        sys.executable,
        str(GENERATE_SCRIPT),
        "--config", str(CONFIG),
        "--out", temp_path,
        "--timestamp", timestamp,
        "--no-gates",   # gates run after merge, not on the raw generator output
    ]
    print(f"\n[1] Running generator: {' '.join(gen_cmd)}")
    gen_result = subprocess.run(gen_cmd, capture_output=True, text=True, encoding="utf-8", errors="replace")
    print(gen_result.stderr)
    if gen_result.stdout:
        print(gen_result.stdout)
    if gen_result.returncode != 0:
        print(f"ERROR: generator exited with code {gen_result.returncode}", file=sys.stderr)
        sys.exit(1)

    # ------------------------------------------------------------------
    # Step 2: Load fresh output + v5 baseline
    # ------------------------------------------------------------------
    print(f"\n[2] Loading fresh generator output from: {temp_path}")
    fresh_data = load_json(temp_path)
    fresh_products = fresh_data.get("products", [])
    print(f"    Fresh products: {len(fresh_products)}")

    print(f"\n[2b] Loading v5 baseline from: {LIVE_V5}")
    v5_data = load_json(LIVE_V5)
    v5_index = build_v5_index(v5_data)
    print(f"    v5 baseline products: {len(v5_index)}")

    # ------------------------------------------------------------------
    # Step 3: Overlay copy fields
    # ------------------------------------------------------------------
    print("\n[3] Overlaying copy fields from v5 baseline...")

    copy_carried = 0      # products where at least 1 copy field was carried
    copy_pending = 0      # products with no v5 match (all PENDING_COPY)
    grade_changes = []    # (barcode, old_grade, new_grade, old_score, new_score)

    # Build old grade/score index from v5
    v5_grade_index = {}
    for bc, p in v5_index.items():
        v5_grade_index[bc] = {
            "grade": p.get("grade"),
            "score": p.get("score"),
        }

    for product in fresh_products:
        bc = str(product.get("barcode", "")).strip()
        if bc in v5_index:
            overlay_copy(product, v5_index[bc])
            copy_carried += 1
            # Track grade changes
            old_g = v5_grade_index[bc].get("grade")
            new_g = product.get("grade")
            old_s = v5_grade_index[bc].get("score")
            new_s = product.get("score")
            if old_g != new_g:
                grade_changes.append({
                    "barcode": bc,
                    "old_grade": old_g,
                    "new_grade": new_g,
                    "old_score": old_s,
                    "new_score": new_s,
                })
        else:
            copy_pending += 1
            print(f"    NEW product (no v5 match, copy=PENDING_COPY): {bc} / {product.get('id')}")

    print(f"    Copy carried from v5: {copy_carried}")
    print(f"    New products (PENDING_COPY): {copy_pending}")
    print(f"    Grade changes: {len(grade_changes)}")
    for gc in grade_changes:
        print(f"      bc={gc['barcode']} {gc['old_grade']} -> {gc['new_grade']}  "
              f"score {gc['old_score']} -> {gc['new_score']}")

    # ------------------------------------------------------------------
    # Step 4: Build grade distributions
    # ------------------------------------------------------------------
    # New distribution
    new_grade_dist = {}
    for p in fresh_products:
        g = p.get("grade", "null")
        new_grade_dist[g] = new_grade_dist.get(g, 0) + 1

    # Old distribution from v5 _meta
    old_grade_dist = v5_data.get("_meta", {}).get("grade_distribution", {})
    # Also compute from v5 products directly
    computed_old = {}
    for p in v5_data.get("products", []):
        g = p.get("grade", "null")
        computed_old[g] = computed_old.get(g, 0) + 1

    # ------------------------------------------------------------------
    # Step 5: Build copy-mismatch list (products whose grade changed → copy outdated)
    # ------------------------------------------------------------------
    copy_mismatch_barcodes = [gc["barcode"] for gc in grade_changes]

    # ------------------------------------------------------------------
    # Step 6: Build updated _meta
    # ------------------------------------------------------------------
    old_meta = v5_data.get("_meta", {})
    run_summary = load_json(RUN_SUMMARY)
    config_sha = sha256_file(CONFIG)

    new_meta = {
        "schema": "BariProductVM[]",
        "schema_version": "v3",
        "generated": timestamp,
        "category": "hummus",
        "version": "v5-shelfrel-002",
        "product_count": len(fresh_products),
        "scored_count": run_summary.get("scored", len(fresh_products)),
        "source_run_id": "run_hummus_shelfrel_002",
        "previous_run_id": old_meta.get("source_run_id", "run_hummus_003"),
        "previous_version": old_meta.get("version", "v5-glassbox_w4"),
        "previous_generated": old_meta.get("generated"),
        "config_sha256": config_sha,
        "generator_version": GENERATOR_VERSION,
        "generator_script": "03_operations/page_generator/generate_page.py",
        "regen_task": TASK,
        "regen_date": "2026-06-16",
        "run_engine_amendments": run_summary.get("engine_amendments", []),
        "run_engine_flags": run_summary.get("flags", {}),
        "run_governance": run_summary.get("governance", ""),
        "run_score_statistics": run_summary.get("score_statistics", {}),
        "grade_distribution": dict(sorted(new_grade_dist.items())),
        "grade_distribution_old": dict(sorted(computed_old.items())),
        "grade_changes": grade_changes,
        "copy_status": {
            "carried_from_v5": copy_carried,
            "new_products_pending_copy": copy_pending,
            "mismatched_grade_count": len(copy_mismatch_barcodes),
            "mismatched_grade_barcodes": sorted(copy_mismatch_barcodes),
            "note": "insightLine/rowVerdict/consumerExplanation from v5 preserved as-is. "
                    "Content/Sonnet pass required to rewrite copy for grade-changed products.",
        },
        "authoritative": True,
        "name_he": old_meta.get("name_he", "חומוס וממרחים"),
        "name_en": old_meta.get("name_en", "Hummus & Savory Spreads"),
        "retailer": "shufersal",
        "scrape_date": "2026-05-30",
        "off_used": run_summary.get("off_used", False),
        "exclusions": fresh_data.get("_meta", {}).get("exclusions", []),
        "known_limitations": old_meta.get("known_limitations", []),
        "nutrition_policy": old_meta.get("nutrition_policy", {}),
        "qa_notes": {
            "regen_task": TASK,
            "prev_qa": old_meta.get("qa_notes", {}),
            "go_live_gate": "owner-gated — Content pass required before deploy",
        },
    }

    # Assemble final output
    final_output = {
        "_meta": new_meta,
        "products": fresh_products,
    }

    # ------------------------------------------------------------------
    # Step 7: Write merged output to live path
    # ------------------------------------------------------------------
    print(f"\n[7] Writing merged output to: {OUTPUT_PATH}")
    with open(str(OUTPUT_PATH), "w", encoding="utf-8") as f:
        json.dump(final_output, f, ensure_ascii=False, indent=2, sort_keys=True)
    print(f"    Written ({os.path.getsize(str(OUTPUT_PATH))} bytes)")

    # Cleanup temp file
    try:
        os.unlink(temp_path)
    except Exception:
        pass

    # ------------------------------------------------------------------
    # Step 8: Run gates
    # ------------------------------------------------------------------
    print(f"\n[8] Running gates on: {OUTPUT_PATH}")
    schema_path = str(ROOT / "03_operations/page_generator/contract/page_output_schema_v3.json")
    corpus_arg = str(ROOT / "02_products/hummus/canonical_bsip1")
    run_arg = str(ROOT / "02_products/hummus/intelligence_bsip2/run_hummus_shelfrel_002/products")

    gate_cmd = [
        sys.executable,
        str(GATES_SCRIPT),
        str(OUTPUT_PATH),
        "--schema", schema_path,
        "--corpus", corpus_arg,
        "--run", run_arg,
    ]
    print(f"    {' '.join(gate_cmd)}")
    gate_result = subprocess.run(
        gate_cmd, capture_output=True, text=True, encoding="utf-8", errors="replace"
    )
    gate_output = gate_result.stdout + gate_result.stderr
    print(gate_output)
    print(f"    Gate exit code: {gate_result.returncode}")

    # ------------------------------------------------------------------
    # Step 9: Print summary
    # ------------------------------------------------------------------
    print("\n=== SUMMARY ===")
    print(f"Run ID:          run_hummus_shelfrel_002")
    print(f"Output:          {OUTPUT_PATH}")
    print(f"Products:        {len(fresh_products)} (was {len(v5_data.get('products', []))} in v5)")
    print(f"Grade dist NEW:  {dict(sorted(new_grade_dist.items()))}")
    print(f"Grade dist OLD:  {dict(sorted(computed_old.items()))}")
    print(f"Grade changes:   {len(grade_changes)}")
    for gc in grade_changes:
        print(f"  {gc['barcode']}: {gc['old_grade']}->{gc['new_grade']}  "
              f"score {gc['old_score']}->{gc['new_score']}")
    exclusions = new_meta.get("exclusions", [])
    off_excl = [e for e in exclusions if "off_banned" in str(e.get("reason", ""))]
    print(f"Exclusions:      {len(exclusions)} total  (OFF-banned: {len(off_excl)})")
    print(f"Gate exit code:  {gate_result.returncode}")

    return gate_result.returncode


if __name__ == "__main__":
    sys.exit(main())
