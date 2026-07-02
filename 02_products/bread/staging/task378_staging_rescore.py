"""
task378_staging_rescore.py — TASK-378 Phase 1: Bread Sugar Re-Score (Staging)

Uses EXACTLY the same code path as batch_run_bread_conform_001.py:
  score_product -> assemble_trace -> trace["final_score_estimate"]
  No build_degraded_output, no run_synthesis (the published run doesn't call them).

Reads:
  run_378_sugar_patch.json   — fetched sugar_by_barcode
  BSIP1 files                — from run_bread_conform_001 BSIP1 dir
  Published run_record.json  — for current published scores

Writes:
  run_378_staging_scores.json — comparison table, 0 published scores changed

STAGING ONLY. Nothing promoted, nothing deployed.
"""
from __future__ import annotations

import json
import os
import sys
import pathlib
import datetime
import copy

sys.stdout.reconfigure(encoding="utf-8", errors="replace")
sys.stderr.reconfigure(encoding="utf-8", errors="replace")

ROOT = pathlib.Path("C:/Bari")
BSIP2_SRC = ROOT / "03_operations/bsip2/proto_v0/src"
sys.path.insert(0, str(BSIP2_SRC))

BSIP1_DIR = ROOT / "03_operations/bsip1/run_bread_conform_001/output"
STAGING_DIR = ROOT / "02_products/bread/staging"
PATCH_FILE = STAGING_DIR / "run_378_sugar_patch.json"
RUN_RECORD = ROOT / "02_products/bread/bsip2_outputs/run_bread_conform_001/run_record.json"

# Exact flags from batch_run_bread_conform_001.py (published run)
BREAD_FLAGS = {
    "BARI_RECAL_P0":                   "on",
    "BARI_SHELF_RELATIVE_V1":          "off",
    "BARI_SODIUM_SHELF_RELATIVE_V1":   "off",
    "BARI_FAT_TECH_V1":                "on",
    "BARI_GRAD_SODIUM_V1":             "off",
    "BARI_DAIRY_PROTEIN_REWEIGHT_V1":  "off",
    "BARI_REDLABEL_V1":                "off",
    "BARI_SODIUM_CEREAL":              "off",
    "BARI_TASK250_CONF":               "off",
}

for k, v in BREAD_FLAGS.items():
    os.environ[k] = v

# Import exactly as the published runner does
from input_loader import load_product, validate_product
from signal_extractor import extract_signals
from router_v2 import classify_category
from nova_proxy import infer_nova
from evaluation_scope import assign_evaluation_scope
from score_engine import score_product, compute_confidence
from trace_writer import assemble_trace
from structural_classifier import classify_structural_class
from constants import score_to_grade


def score_one(product: dict) -> dict:
    """Exact replica of batch_run_bread_conform_001.score_one()."""
    prod = {k: v for k, v in product.items() if not k.startswith("_")}
    signals = extract_signals(prod)
    cat_result = classify_category(prod)
    l3 = signals["L3_inferred_classifications"]
    nova_result = infer_nova(prod, l3)
    eval_result = assign_evaluation_scope(prod, cat_result["category"])
    score_result = score_product(prod, signals, cat_result, nova_result, eval_result)
    trace = assemble_trace(prod, signals, cat_result, nova_result, eval_result, score_result)
    trace["structural_class"] = classify_structural_class(trace)
    return trace


def main():
    print("=" * 70)
    print("TASK-378 Phase 1: Bread Sugar Staging Re-Score")
    print("=" * 70)
    print(f"  Engine path: batch_run_bread_conform_001 (exact replica)")
    print(f"  Staging only — 0 published scores changed")
    print()

    # Load sugar patch
    with open(PATCH_FILE, encoding="utf-8") as f:
        patch = json.load(f)
    sugar_by_barcode: dict[str, float | None] = patch["sugar_by_barcode"]

    # Load published run record
    with open(RUN_RECORD, encoding="utf-8") as f:
        rr = json.load(f)
    published = {p["barcode"]: p for p in rr["results"]}

    print(f"Products in published run: {len(published)}")
    print(f"Sugar values available:    {sum(1 for v in sugar_by_barcode.values() if v is not None)}/{len(sugar_by_barcode)}")
    print()

    comparison_rows = []
    grade_movers = []

    # Process each product
    bsip1_files = sorted(BSIP1_DIR.glob("bsip1_*.json"))
    for fpath in bsip1_files:
        product = load_product(fpath)
        barcode = product.get("barcode", "")
        name = product.get("canonical_name_he", "?")

        if barcode not in published:
            continue  # not in curated corpus

        pub = published[barcode]
        current_score = pub["score"]
        current_grade = pub["grade"]
        sugars_g = sugar_by_barcode.get(barcode)

        # Control: re-score with original data (should reproduce published score)
        product_control = copy.deepcopy(product)
        product_control["_source_path"] = str(fpath)
        validate_product(product_control)
        try:
            trace_ctrl = score_one(product_control)
            ctrl_score = trace_ctrl.get("final_score_estimate")
            ctrl_grade = trace_ctrl.get("grade_estimate")
        except Exception as e:
            ctrl_score = None
            ctrl_grade = None

        # Treatment: re-score with new sugar value
        if sugars_g is not None:
            product_treat = copy.deepcopy(product)
            product_treat["normalized_nutrition_per_100g"]["sugars_g"] = sugars_g
            product_treat["_source_path"] = str(fpath)
            validate_product(product_treat)
            try:
                trace_treat = score_one(product_treat)
                staged_score = trace_treat.get("final_score_estimate")
                staged_grade = trace_treat.get("grade_estimate")
                glycemic_staged = trace_treat.get("dimension_scores", {}).get("glycemic_quality")
                glycemic_note = trace_treat.get("dimension_notes", {}).get("glycemic_quality")
                caps_fired = [c["rule"] for c in trace_treat.get("caps_considered", []) if c.get("fired")]
            except Exception as e:
                staged_score = None
                staged_grade = None
                glycemic_staged = None
                glycemic_note = None
                caps_fired = []
        else:
            staged_score = None
            staged_grade = None
            glycemic_staged = None
            glycemic_note = None
            caps_fired = []

        score_delta = None
        grade_moves = False
        if staged_score is not None and ctrl_score is not None:
            score_delta = round(staged_score - ctrl_score, 1)
        if staged_grade and ctrl_grade and staged_grade != ctrl_grade:
            grade_moves = True

        row = {
            "barcode": barcode,
            "name": name,
            "current_score": current_score,
            "current_grade": current_grade,
            "control_score": round(ctrl_score, 1) if ctrl_score is not None else None,
            "control_grade": ctrl_grade,
            "sugars_g": sugars_g,
            "staged_score": round(staged_score, 1) if staged_score is not None else None,
            "staged_grade": staged_grade,
            "score_delta": score_delta,
            "grade_moves": grade_moves,
            "glycemic_quality_staged": glycemic_staged,
            "glycemic_note_staged": glycemic_note,
            "caps_fired": caps_fired,
            "fetch_status": next(
                (r.get("fetch_status") for r in patch["fetch_results"] if r["barcode"] == barcode),
                "already_present",
            ),
        }
        comparison_rows.append(row)
        if grade_moves:
            grade_movers.append(row)

        arrow = "★" if grade_moves else "→"
        delta_str = f"{score_delta:+.1f}" if score_delta is not None else "N/A"
        sugar_str = f"{sugars_g}g" if sugars_g is not None else "N/A"
        print(
            f"  {barcode:<16} {name[:36]:<37} "
            f"{current_score}/{current_grade} → ctrl:{ctrl_score}/{ctrl_grade} "
            f"→ staged:{staged_score}/{staged_grade} (Δ{delta_str}) sugar={sugar_str} {arrow}"
        )

    print()
    print("=" * 70)
    print("STAGING SUMMARY")
    print("=" * 70)

    rescored = [r for r in comparison_rows if r["staged_score"] is not None]
    not_rescored = [r for r in comparison_rows if r["staged_score"] is None]

    print(f"Products in corpus:          {len(comparison_rows)}")
    print(f"Sugar recovered + re-scored: {len(rescored)}")
    print(f"Sugar unavailable (3 pages had no panel): {len(not_rescored)}")
    print(f"Grade movers:                {len(grade_movers)}")
    print()

    print("PER-PRODUCT TABLE (barcode | name | current | staged | delta | sugar):")
    print("-" * 90)
    for r in sorted(comparison_rows, key=lambda x: -(x.get("score_delta") or 0) if (x.get("score_delta") or 0) < 0 else 0):
        delta_str = f"{r['score_delta']:+.1f}" if r['score_delta'] is not None else " N/A"
        sugar_str = f"{r['sugars_g']}g" if r['sugars_g'] is not None else "N/A"
        mover = " ★GRADE" if r["grade_moves"] else ""
        print(
            f"  {r['barcode']:<16} {r['name'][:34]:<35} "
            f"{r['current_score']}/{r['current_grade']:1} → {r['staged_score']}/{r['staged_grade'] or 'N/A':1} "
            f"(Δ{delta_str}) {sugar_str}{mover}"
        )

    if grade_movers:
        print()
        print("GRADE MOVERS:")
        for r in grade_movers:
            print(f"  {r['barcode']:<16} {r['name'][:36]:<37} {r['current_grade']} → {r['staged_grade']} (Δ{r['score_delta']:+.1f}) sugar={r['sugars_g']}g")

    print()
    print("0 published scores changed.")
    print(f"{len(grade_movers)} grade-movers flagged — require owner approval before promotion.")

    # Save staging record
    out = {
        "run_id": "task378_bread_sugar_staging",
        "task": "TASK-378",
        "generated_at": datetime.datetime.now(datetime.UTC).isoformat(),
        "staging_only": True,
        "promoted": False,
        "published_run_id": rr["run_id"],
        "engine_path": "batch_run_bread_conform_001 (exact replica)",
        "engine_flags": BREAD_FLAGS,
        "summary": {
            "total_products": len(comparison_rows),
            "sugar_recovered_rescored": len(rescored),
            "sugar_unavailable": len(not_rescored),
            "grade_movers": len(grade_movers),
            "published_scores_changed": 0,
        },
        "comparison": comparison_rows,
        "grade_movers": grade_movers,
    }

    out_path = STAGING_DIR / "run_378_staging_scores.json"
    out_path.write_text(json.dumps(out, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"\nStaging scores saved: {out_path}")

    return out


if __name__ == "__main__":
    main()
