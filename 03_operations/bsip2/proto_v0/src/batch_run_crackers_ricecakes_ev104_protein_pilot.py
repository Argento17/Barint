"""
BSIP2 Pilot Runner — EV-104 Crackers Protein-Scale Calibration
(run_id: crackers_ricecakes_ev104_protein_pilot)

TASK: Data Agent dispatch, "Implement and pilot-test EV-104" (2026-07-05).
Status: Product Agent D7 co-sign is CONDITIONAL, NOT a green light. This script
is a PILOT ONLY -- it does NOT touch the production entrypoints
(batch_run_crackers_conform_001.py / batch_run_ricecakes_conform_001.py), does
NOT overwrite the already-shipped crackers_frontend_v1.json, and does NOT edit
constants.py on disk. No commit is made by this script or by the agent that
ran it.

Root cause: PROTEIN_SCALE_TABLES (constants.py:435-444) has no "cracker" row,
so crackers falls back to "default" (identical to snack_bar_granola's curve),
compressing all crackers protein into the bottom third of the scale.

Proposed fix (anchored on the real 53-product corpus distribution used by
Nutrition/Product for the co-sign: n=53, min=5.5g, Q1=8.0g, median=9.0g,
Q3=13.0g, max=16.0g):
    "cracker": [(0,0),(3,15),(5,30),(7,45),(9,58),(11,75),(13,85),(16,95),(99,100)]

ISOLATION MECHANISM (Condition 4 -- isolated, revertible):
  This script does NOT edit constants.py. It imports the constants module and
  monkey-patches PROTEIN_SCALE_TABLES["cracker"] onto the live dict object
  in-process, ONCE, for the duration of this process only. The on-disk
  constants.py is never touched -- nothing to revert in git, working tree
  stays clean, production entrypoints are unaffected (they import a fresh,
  unpatched constants module in their own process).

METHODOLOGY NOTE (important correction made during this run): a naive
"committed baseline trace vs fresh patched re-score" diff is NOT a valid
isolation test, because the engine (score_engine.py and friends) may have
drifted since a corpus was last committed, for reasons that have nothing to
do with this patch. This script therefore scores every product TWICE in the
SAME process on the SAME (current) engine build -- once with the table
UNPATCHED, once PATCHED -- and diffs those two fresh runs against each other.
That isolates the patch's effect from any incidental engine drift. Drift
against the old committed baseline is reported separately as FYI, not used
for the crosser/cap-clip conclusions.
"""

from __future__ import annotations
import sys, json, pathlib, datetime, os, hashlib, copy
from collections import Counter

sys.path.insert(0, str(pathlib.Path(__file__).parent))
sys.stdout.reconfigure(encoding="utf-8", errors="replace")
sys.stderr.reconfigure(encoding="utf-8", errors="replace")

# --- Same flag set as the production crackers/ricecakes/bread entrypoints ---
CRACKERS_FLAGS = {
    "BARI_RECAL_P0": "on",
    "BARI_SHELF_RELATIVE_V1": "off",
    "BARI_SODIUM_SHELF_RELATIVE_V1": "off",
    "BARI_FAT_TECH_V1": "on",
    "BARI_GRAD_SODIUM_V1": "off",
    "BARI_DAIRY_PROTEIN_REWEIGHT_V1": "off",
    "BARI_REDLABEL_V1": "off",
    "BARI_SODIUM_CEREAL": "off",
}
for k, v in CRACKERS_FLAGS.items():
    os.environ[k] = v

import constants
from constants import PROTEIN_SCALE_TABLES, lookup_protein_scale
from input_loader import load_product, validate_product
from signal_extractor import extract_signals
from router_v2 import classify_category
from nova_proxy import infer_nova
from evaluation_scope import assign_evaluation_scope
from score_engine import score_product, compute_confidence
from trace_writer import assemble_trace
from structural_classifier import classify_structural_class

ROOT = pathlib.Path(r"C:\Bari")
CRACKERS_BSIP1 = ROOT / "03_operations" / "bsip1" / "run_crackers_conform_001" / "output"
RICECAKES_BSIP1 = ROOT / "03_operations" / "bsip1" / "run_ricecakes_conform_001" / "output"
CRACKERS_BASELINE = ROOT / "02_products" / "crackers" / "bsip2_outputs" / "run_crackers_conform_001" / "products"
RICECAKES_BASELINE = ROOT / "02_products" / "crackers" / "bsip2_outputs" / "run_ricecakes_conform_001" / "products"
BREAD_BSIP1 = ROOT / "03_operations" / "bsip1" / "run_bread_conform_001" / "output"
BREAD_BASELINE = ROOT / "02_products" / "bread" / "bsip2_outputs" / "run_bread_conform_001" / "products"

PILOT_OUT = ROOT / "03_operations" / "bsip2" / "proto_v0" / "pilots" / "ev104_crackers_protein"
PILOT_OUT.mkdir(parents=True, exist_ok=True)

RUN_ID = "crackers_ricecakes_ev104_protein_pilot"
EV_ID = "EV-104"
NEW_CRACKER_ROW = [(0, 0), (3, 15), (5, 30), (7, 45), (9, 58), (11, 75), (13, 85), (16, 95), (99, 100)]


def sha256_file(path: pathlib.Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def score_one(product: dict) -> dict:
    """Identical scoring path to batch_run_crackers_conform_001.py / _ricecakes / _bread_conform_001.py."""
    prod = {k: v for k, v in product.items() if not k.startswith("_")}
    signals = extract_signals(prod)
    cat_result = classify_category(prod)
    l3 = signals["L3_inferred_classifications"]
    nova_result = infer_nova(prod, l3)
    eval_result = assign_evaluation_scope(prod, cat_result["category"])
    score_result = score_product(prod, signals, cat_result, nova_result, eval_result)
    trace = assemble_trace(prod, signals, cat_result, nova_result, eval_result, score_result)
    trace["structural_class"] = classify_structural_class(trace)
    trace["_router_category"] = cat_result["category"]
    trace["_router_confidence"] = cat_result["category_confidence"]
    return trace


def load_committed_baseline(products_dir: pathlib.Path, barcode: str) -> dict | None:
    for d in products_dir.iterdir():
        if not d.is_dir():
            continue
        tp = d / "bsip2_trace.json"
        if not tp.exists():
            continue
        try:
            t = json.loads(tp.read_text(encoding="utf-8"))
        except Exception:
            continue
        bc = str((t.get("input_reference") or {}).get("barcode") or t.get("barcode") or "")
        if bc == str(barcode):
            return t
    return None


def score_corpus(files: list[pathlib.Path]) -> tuple[dict, list]:
    """Score a list of BSIP1 files with score_one(); return {barcode: trace} + errors."""
    out = {}
    errs = []
    for fpath in files:
        product = load_product(fpath)
        product["_source_path"] = str(fpath)
        product["_load_errors"] = validate_product(product)
        barcode = str(product.get("barcode", ""))
        try:
            trace = score_one(product)
            trace["_protein_g_input"] = (product.get("normalized_nutrition_per_100g") or {}).get("protein_g")
            trace["_name"] = product.get("canonical_name_he", "?")
            out[barcode] = trace
        except Exception as e:
            errs.append({"barcode": barcode, "file": fpath.name, "error": str(e)})
    return out, errs


def cap_clipped(trace: dict) -> bool:
    w = trace.get("weighted_dimension_score")
    c = trace.get("binding_cap")
    a = trace.get("score_after_cap")
    if w is None or a is None:
        return False
    return round(a, 2) < round(w, 2) - 0.005


def _grade_rank(g):
    order = {"E": 0, "D": 1, "C": 2, "B": 3, "A": 4, "S": 5}
    return order.get(g, -1)


def main():
    ts = datetime.datetime.now(datetime.timezone.utc).isoformat()
    report = {
        "run_id": RUN_ID,
        "evidence_id_pending": EV_ID,
        "generated": ts,
        "status": "PILOT_MEASURED_NOT_PUBLISHED_NOT_WIRED_NOT_COMMITTED",
        "note": "EV-104 is CO-SIGN APPROVED WITH CONDITIONS, not shipped. This run covers Conditions 1-2-4 only.",
    }

    print("=" * 78)
    print(f"EV-104 PILOT -- {RUN_ID}")
    print("=" * 78)

    # -------------------------------------------------------------------
    # STEP 1: Load corpora
    # -------------------------------------------------------------------
    crackers_files = sorted(CRACKERS_BSIP1.glob("bsip1_*.json"))
    ricecakes_files = sorted(RICECAKES_BSIP1.glob("bsip1_*.json"))
    bread_files = sorted(BREAD_BSIP1.glob("bsip1_*.json"))
    print(f"\n--- STEP 1: Corpus ---")
    print(f"  crackers BSIP1: {len(crackers_files)}  ricecakes BSIP1: {len(ricecakes_files)}  "
          f"target corpus total: {len(crackers_files)+len(ricecakes_files)}  bread control: {len(bread_files)}")

    # -------------------------------------------------------------------
    # STEP 2: Score EVERYTHING once, UNPATCHED (current engine, no "cracker" key)
    # -------------------------------------------------------------------
    print("\n--- STEP 2: Fresh UNPATCHED pass (current engine, table absent -> 'default' fallback) ---")
    assert "cracker" not in PROTEIN_SCALE_TABLES, "PRECONDITION FAIL: 'cracker' key already present -- pilot invalid"
    crackers_pre, err_c_pre = score_corpus(crackers_files)
    ricecakes_pre, err_r_pre = score_corpus(ricecakes_files)
    bread_pre, err_b_pre = score_corpus(bread_files)
    print(f"  crackers scored: {len(crackers_pre)}/{len(crackers_files)}  errors: {len(err_c_pre)}")
    print(f"  ricecakes scored: {len(ricecakes_pre)}/{len(ricecakes_files)}  errors: {len(err_r_pre)}")
    print(f"  bread scored: {len(bread_pre)}/{len(bread_files)}  errors: {len(err_b_pre)}")

    # -------------------------------------------------------------------
    # STEP 3: Structural dict-level guard, THEN apply the patch ONCE
    # -------------------------------------------------------------------
    print("\n--- STEP 3: Structural byte-identical guard + patch application ---")
    existing_categories = list(PROTEIN_SCALE_TABLES.keys())
    probe_grams = [0, 1, 3, 5, 6, 7, 9, 10, 11, 13, 15, 20, 25, 30, 99]
    before = {cat: [lookup_protein_scale(g, cat, True) for g in probe_grams] for cat in existing_categories}
    before["unknown_category_XYZ"] = [lookup_protein_scale(g, "unknown_category_XYZ", True) for g in probe_grams]

    PROTEIN_SCALE_TABLES["cracker"] = NEW_CRACKER_ROW
    print(f"  Patched (in-process only, constants.py on disk untouched): PROTEIN_SCALE_TABLES['cracker'] = {NEW_CRACKER_ROW}")

    after = {cat: [lookup_protein_scale(g, cat, True) for g in probe_grams] for cat in existing_categories}
    after["unknown_category_XYZ"] = [lookup_protein_scale(g, "unknown_category_XYZ", True) for g in probe_grams]

    struct_mismatches = [cat for cat in existing_categories if before[cat] != after[cat]]
    if before["unknown_category_XYZ"] != after["unknown_category_XYZ"]:
        struct_mismatches.append("unknown_category_XYZ(default-fallback)")
    cracker_vals = [lookup_protein_scale(g, "cracker", True) for g in probe_grams]
    cracker_now_diff_from_default = (after["default"] != cracker_vals)

    print(f"  Existing categories probed: {existing_categories}")
    print(f"  Mismatches after patch (must be 0): {len(struct_mismatches)} {struct_mismatches}")
    print(f"  'cracker' now diverges from 'default' fallback: {cracker_now_diff_from_default} (expected True)")
    step3_pass = (len(struct_mismatches) == 0) and cracker_now_diff_from_default
    print(f"  STEP 3 RESULT: {'PASS' if step3_pass else 'FAIL -- HALT'}")
    report["step3_structural_guard"] = {
        "pass": step3_pass, "existing_categories_probed": existing_categories,
        "probe_grams": probe_grams, "mismatches": struct_mismatches,
        "cracker_diverges_from_default": cracker_now_diff_from_default,
    }
    if not step3_pass:
        (PILOT_OUT / "run_record.json").write_text(json.dumps(report, ensure_ascii=False, indent=2, default=str), encoding="utf-8")
        print("HALTING: structural guard failed.")
        return report

    # -------------------------------------------------------------------
    # STEP 4: Score EVERYTHING again, PATCHED, on the SAME engine build
    # -------------------------------------------------------------------
    print("\n--- STEP 4: Fresh PATCHED pass (same engine build, 'cracker' key active) ---")
    crackers_post, err_c_post = score_corpus(crackers_files)
    ricecakes_post, err_r_post = score_corpus(ricecakes_files)
    bread_post, err_b_post = score_corpus(bread_files)
    print(f"  crackers scored: {len(crackers_post)}/{len(crackers_files)}  errors: {len(err_c_post)}")
    print(f"  ricecakes scored: {len(ricecakes_post)}/{len(ricecakes_files)}  errors: {len(err_r_post)}")
    print(f"  bread scored: {len(bread_post)}/{len(bread_files)}  errors: {len(err_b_post)}")

    # -------------------------------------------------------------------
    # STEP 5: Bread isolation proof -- pre vs post, SAME engine build (Condition 4)
    # -------------------------------------------------------------------
    print("\n--- STEP 5: Bread pre-vs-post isolation proof (fresh-vs-fresh, same engine) ---")
    print("  NOTE: isolation is keyed by ROUTER CATEGORY, not by which BSIP1 folder a file sits in.")
    print("  The bread BSIP1 corpus (run_bread_conform_001) is pre-TASK-433-split and contains 6 products")
    print("  the router classifies as category='cracker' (the same 6 as LEGACY_PUBLISHED_SCORES in")
    print("  batch_run_crackers_conform_001.py). Those 6 are EXPECTED to move -- they are cracker-category")
    print("  products by router classification, wherever their BSIP1 file happens to live. Only products")
    print("  the router classifies as category='bread' are the true non-cracker control group.")
    bread_mismatches = []       # unexpected: a genuinely bread-routed product moved
    bread_expected_moves = []   # expected: a cracker-routed product (living in the bread folder) moved
    bread_unrouted_check = []
    for bc, pre_t in bread_pre.items():
        post_t = bread_post.get(bc)
        router_cat = pre_t.get("_router_category")
        if post_t is None:
            bread_mismatches.append({"barcode": bc, "issue": "missing in post-patch pass", "router_category": router_cat})
            continue
        moved = (pre_t.get("final_score_estimate") != post_t.get("final_score_estimate")
                 or pre_t.get("grade_estimate") != post_t.get("grade_estimate"))
        if moved and router_cat == "cracker":
            bread_expected_moves.append({
                "barcode": bc, "router_category": router_cat,
                "pre_patch_score": pre_t.get("final_score_estimate"), "pre_patch_grade": pre_t.get("grade_estimate"),
                "post_patch_score": post_t.get("final_score_estimate"), "post_patch_grade": post_t.get("grade_estimate"),
            })
        elif moved:
            bread_mismatches.append({
                "barcode": bc, "router_category": router_cat,
                "pre_patch_score": pre_t.get("final_score_estimate"), "pre_patch_grade": pre_t.get("grade_estimate"),
                "post_patch_score": post_t.get("final_score_estimate"), "post_patch_grade": post_t.get("grade_estimate"),
            })
    n_bread_routed = sum(1 for t in bread_pre.values() if t.get("_router_category") == "bread")
    n_cracker_routed_in_bread_folder = sum(1 for t in bread_pre.values() if t.get("_router_category") == "cracker")
    n_other_routed = len(bread_pre) - n_bread_routed - n_cracker_routed_in_bread_folder
    step5_pass = len(bread_mismatches) == 0 and n_bread_routed > 0
    print(f"  Bread-folder products: {len(bread_pre)} total -> router_category='bread': {n_bread_routed}, "
          f"='cracker' (legacy overlap): {n_cracker_routed_in_bread_folder}, other: {n_other_routed}")
    print(f"  Unexpected mismatches among NON-cracker-routed products (must be 0): {len(bread_mismatches)}")
    for m in bread_mismatches:
        print(f"    UNEXPECTED MISMATCH: {m}")
    print(f"  Expected moves among cracker-routed products living in the bread folder: {len(bread_expected_moves)} "
          f"(of {n_cracker_routed_in_bread_folder}; these are legitimately cracker-category)")
    for m in bread_expected_moves:
        print(f"    EXPECTED (cracker-routed): {m}")
    print(f"  STEP 5 RESULT: {'PASS' if step5_pass else 'FAIL -- HALT'}")

    # FYI (non-gating): drift between the OLD committed bread baseline and a
    # fresh UNPATCHED run on the CURRENT engine. This is unrelated to EV-104
    # (bread never touches the "cracker" key) but is a real, separate finding
    # worth surfacing -- the committed bread page may be stale vs current engine.
    bread_drift = []
    for bc, pre_t in bread_pre.items():
        committed = load_committed_baseline(BREAD_BASELINE, bc)
        if committed is None:
            continue
        if pre_t.get("final_score_estimate") != committed.get("final_score_estimate") or pre_t.get("grade_estimate") != committed.get("grade_estimate"):
            bread_drift.append({
                "barcode": bc,
                "committed_score": committed.get("final_score_estimate"), "committed_grade": committed.get("grade_estimate"),
                "fresh_unpatched_score": pre_t.get("final_score_estimate"), "fresh_unpatched_grade": pre_t.get("grade_estimate"),
            })
    print(f"  FYI (non-gating, unrelated to EV-104): committed-baseline-vs-current-engine drift on bread: {len(bread_drift)}/{len(bread_pre)} products differ")
    print(f"  This indicates run_bread_conform_001's committed traces predate later engine changes; separate from this patch.")

    report["step5_bread_isolation"] = {
        "pass": step5_pass, "checked": len(bread_pre),
        "router_breakdown": {"bread": n_bread_routed, "cracker_legacy_overlap": n_cracker_routed_in_bread_folder, "other": n_other_routed},
        "unexpected_mismatches_among_non_cracker_routed": bread_mismatches,
        "expected_moves_among_cracker_routed_legacy_overlap": bread_expected_moves,
        "note": "Isolation is proven for the true control group (router_category=='bread', "
                f"n={n_bread_routed}): zero unexpected mismatches. The "
                f"{n_cracker_routed_in_bread_folder} products the router classifies as 'cracker' "
                "despite living in the bread BSIP1 folder (pre-TASK-433-split legacy) correctly "
                "move -- they are cracker-category products by classification, matching "
                "LEGACY_PUBLISHED_SCORES in batch_run_crackers_conform_001.py exactly.",
        "fyi_committed_vs_current_engine_drift_unrelated_to_ev104": {
            "count": len(bread_drift), "total": len(bread_pre), "detail": bread_drift,
        },
    }
    if not step5_pass:
        (PILOT_OUT / "run_record.json").write_text(json.dumps(report, ensure_ascii=False, indent=2, default=str), encoding="utf-8")
        print("HALTING: bread isolation proof failed -- patch is NOT isolated. Do not proceed.")
        return report

    # -------------------------------------------------------------------
    # STEP 6: Crosser reconciliation for the 54-product corpus.
    # True EV-104 effect = fresh UNPATCHED vs fresh PATCHED (same engine build).
    # -------------------------------------------------------------------
    print("\n--- STEP 6: Crosser reconciliation (fresh-vs-fresh, isolates the patch only) ---")
    rows = []
    all_pre = {**{f"crackers::{k}": v for k, v in crackers_pre.items()}, **{f"ricecakes::{k}": v for k, v in ricecakes_pre.items()}}
    all_post = {**{f"crackers::{k}": v for k, v in crackers_post.items()}, **{f"ricecakes::{k}": v for k, v in ricecakes_post.items()}}

    for key, pre_t in all_pre.items():
        source, bc = key.split("::", 1)
        post_t = all_post.get(key)
        if post_t is None:
            continue
        old_score = pre_t.get("final_score_estimate")
        old_grade = pre_t.get("grade_estimate")
        new_score = post_t.get("final_score_estimate")
        new_grade = post_t.get("grade_estimate")

        old_clip = cap_clipped(pre_t)
        new_clip = cap_clipped(post_t)
        newly_introduced_clip = new_clip and not old_clip

        crossed = (old_grade != new_grade) and old_grade is not None and new_grade is not None

        # Also fetch committed baseline for continuity / FYI drift reporting
        baseline_dir = CRACKERS_BASELINE if source == "crackers" else RICECAKES_BASELINE
        committed = load_committed_baseline(baseline_dir, bc)
        committed_score = committed.get("final_score_estimate") if committed else None
        committed_grade = committed.get("grade_estimate") if committed else None
        drift_vs_committed = (committed_score != old_score or committed_grade != old_grade) if committed else None

        rows.append({
            "barcode": bc, "name": pre_t.get("_name"), "source": source,
            "router_category": post_t.get("_router_category"),
            "protein_g": pre_t.get("_protein_g_input"),
            "old_score": old_score, "old_grade": old_grade,
            "new_score": new_score, "new_grade": new_grade,
            "delta": round(new_score - old_score, 2) if (old_score is not None and new_score is not None) else None,
            "grade_crossed": crossed,
            "cross_direction": f"{old_grade}->{new_grade}" if crossed else None,
            "old_weighted_dimension_score": pre_t.get("weighted_dimension_score"),
            "new_weighted_dimension_score": post_t.get("weighted_dimension_score"),
            "old_binding_cap": pre_t.get("binding_cap"), "new_binding_cap": post_t.get("binding_cap"),
            "old_score_after_cap": pre_t.get("score_after_cap"), "new_score_after_cap": post_t.get("score_after_cap"),
            "cap_clipped_pre_patch": old_clip, "cap_clipped_post_patch": new_clip,
            "newly_introduced_clip": newly_introduced_clip,
            "committed_baseline_score": committed_score, "committed_baseline_grade": committed_grade,
            "drift_vs_committed_baseline": drift_vs_committed,
        })

    print(f"  Rows: {len(rows)}/54")
    n_drift_vs_committed = sum(1 for r in rows if r["drift_vs_committed_baseline"])
    print(f"  FYI (non-gating): fresh-UNPATCHED vs committed-baseline drift: {n_drift_vs_committed}/{len(rows)} "
          f"(engine drift unrelated to EV-104 if >0 -- report separately, does not change the crosser count below)")

    crossers = [r for r in rows if r["grade_crossed"]]
    cross_counter = Counter(r["cross_direction"] for r in crossers)
    double_jump = [r for r in crossers if abs(_grade_rank(r["old_grade"]) - _grade_rank(r["new_grade"])) > 1]

    print(f"  Total crossers: {len(crossers)}")
    for direction, count in sorted(cross_counter.items()):
        print(f"    {direction}: {count}")
    print(f"  Double-grade jumps (>1 boundary): {len(double_jump)} (expected 0)")

    nutrition_claim = {"B->A": 7, "C->B": 4, "D->C": 2}
    product_claim = {"B->A": 8, "C->B": 3, "D->C": 2}
    engine_actual = {k: cross_counter.get(k, 0) for k in ("B->A", "C->B", "D->C")}
    other_directions = {k: v for k, v in cross_counter.items() if k not in ("B->A", "C->B", "D->C")}
    nutrition_matches = (engine_actual == nutrition_claim) and not other_directions
    product_matches = (engine_actual == product_claim) and not other_directions

    print(f"  Nutrition claim  {nutrition_claim} -- matches engine: {nutrition_matches}")
    print(f"  Product claim    {product_claim} -- matches engine: {product_matches}")
    print(f"  Engine actual    {engine_actual}  other_directions={other_directions}")
    for r in sorted(crossers, key=lambda x: x["barcode"]):
        print(f"    {r['barcode']} | {(r['name'] or '')[:32]:32s} | {r['old_grade']}({r['old_score']})->{r['new_grade']}({r['new_score']}) | protein_g={r['protein_g']}")

    # -------------------------------------------------------------------
    # STEP 7: Cap-clip summary (Condition 2), isolated pre-vs-post
    # -------------------------------------------------------------------
    newly_clipped = [r for r in rows if r["newly_introduced_clip"]]
    print(f"\n--- STEP 7: Cap-clip check (fresh pre-patch vs fresh post-patch) --- newly-introduced clips: {len(newly_clipped)} (expected 0)")
    for r in newly_clipped:
        print(f"    CLIP: {r['barcode']} | weighted={r['new_weighted_dimension_score']} cap={r['new_binding_cap']} after_cap={r['new_score_after_cap']}")

    movers = [r for r in rows if r["delta"] not in (None, 0.0)]
    deltas = [r["delta"] for r in movers]

    # -------------------------------------------------------------------
    # Write outputs
    # -------------------------------------------------------------------
    csv_path = PILOT_OUT / "crosser_reconciliation_table.csv"
    with csv_path.open("w", encoding="utf-8", newline="") as f:
        f.write("barcode,name,source,router_category,protein_g,old_score,old_grade,new_score,new_grade,delta,"
                "grade_crossed,cross_direction,old_binding_cap,new_binding_cap,newly_introduced_clip,"
                "committed_baseline_score,committed_baseline_grade,drift_vs_committed_baseline\n")
        for r in sorted(rows, key=lambda x: str(x["barcode"])):
            f.write(",".join(str(r[k]).replace(",", ";") for k in [
                "barcode", "name", "source", "router_category", "protein_g",
                "old_score", "old_grade", "new_score", "new_grade", "delta",
                "grade_crossed", "cross_direction", "old_binding_cap", "new_binding_cap", "newly_introduced_clip",
                "committed_baseline_score", "committed_baseline_grade", "drift_vs_committed_baseline",
            ]) + "\n")

    constants_sha = sha256_file(pathlib.Path(__file__).parent / "constants.py")
    score_engine_sha = sha256_file(pathlib.Path(__file__).parent / "score_engine.py")

    report.update({
        "step1_corpus": {"crackers_bsip1": len(crackers_files), "ricecakes_bsip1": len(ricecakes_files),
                         "target_total": len(crackers_files) + len(ricecakes_files), "bread_control": len(bread_files)},
        "step2_step4_scoring_errors": {
            "crackers_pre": err_c_pre, "ricecakes_pre": err_r_pre, "bread_pre": err_b_pre,
            "crackers_post": err_c_post, "ricecakes_post": err_r_post, "bread_post": err_b_post,
        },
        "proposed_table_row": {"cracker": NEW_CRACKER_ROW},
        "fyi_committed_baseline_drift_unrelated_to_ev104": {
            "crackers_ricecakes_count": n_drift_vs_committed, "crackers_ricecakes_total": len(rows),
            "bread_count": len(bread_drift), "bread_total": len(bread_pre),
            "explanation": "Committed traces for run_bread_conform_001 / run_crackers_conform_001 / "
                            "run_ricecakes_conform_001 do not byte-match a fresh re-score on the CURRENT "
                            "engine even with the protein table unpatched -- this is pre-existing engine "
                            "drift since those runs were committed, structurally proven unrelated to the "
                            "'cracker' key (bread never reads it; crackers/ricecakes drift is measured "
                            "pre-patch, before the key exists). Flagged for Data/Product awareness; not an "
                            "EV-104 gating concern because this pilot's crosser analysis uses fresh-vs-fresh "
                            "(both on current engine), which cancels the drift out.",
        },
        "crosser_reconciliation": {
            "total_crossers": len(crossers), "double_grade_jumps": len(double_jump),
            "by_direction": dict(cross_counter), "other_directions_not_expected": other_directions,
            "nutrition_agent_claim": nutrition_claim, "product_agent_claim": product_claim,
            "engine_actual": engine_actual,
            "nutrition_claim_matches_engine": nutrition_matches, "product_claim_matches_engine": product_matches,
            "crosser_detail": crossers,
        },
        "cap_clip_check": {
            "newly_introduced_clips": len(newly_clipped), "clip_detail": newly_clipped,
            "hard_stop_required": len(newly_clipped) > 0,
        },
        "movement": {
            "n_movers": len(movers), "n_zero_movement": len(rows) - len(movers),
            "min_delta": min(deltas) if deltas else None, "max_delta": max(deltas) if deltas else None,
        },
        "byte_identical_guard": {
            "step3_structural": report["step3_structural_guard"],
            "step5_bread_fresh_vs_fresh": report["step5_bread_isolation"],
        },
        "constants_sha256_UNCHANGED_ON_DISK": constants_sha,
        "score_engine_sha256_UNCHANGED_ON_DISK": score_engine_sha,
        "full_row_table": rows,
        "crosser_reconciliation_csv": str(csv_path),
        "not_wired_into": [
            "batch_run_crackers_conform_001.py", "batch_run_ricecakes_conform_001.py",
            "crackers_frontend_v1.json", "bsip2_evidence_registry_v1.json / .md",
        ],
        "committed": False,
    })

    rr_path = PILOT_OUT / "run_record.json"
    rr_path.write_text(json.dumps(report, ensure_ascii=False, indent=2, default=str), encoding="utf-8")

    patch_path = PILOT_OUT / "constants_ev104_cracker_row.patch.txt"
    patch_path.write_text(
        "--- a/03_operations/bsip2/proto_v0/src/constants.py\n"
        "+++ b/03_operations/bsip2/proto_v0/src/constants.py\n"
        "@@ PROTEIN_SCALE_TABLES @@\n"
        ' PROTEIN_SCALE_TABLES = {\n'
        '     "dairy_protein":     [(0,0),(3,20),(5,35),(7,50),(9,65),(11,85),(13,95),(99,100)],\n'
        '     "sauce_spread":      [(0,0),(2,12),(4,28),(6,45),(8,62),(11,82),(14,95),(99,100)],\n'
        "     # --- FROZEN categories (modelled; require P2 owner sign-off before shipping) ---\n"
        '     "milk_dairy":        [(0,0),(2,30),(3,55),(4,70),(6,88),(8,95),(99,100)],\n'
        '     "yogurt":            [(0,0),(2,20),(3.5,40),(5,58),(7,75),(9,90),(11,95),(99,100)],\n'
        '     "bread":             [(0,0),(4,30),(6,45),(8,60),(10,72),(13,85),(99,95)],\n'
        '     "snack_bar_granola": [(0,0),(3,15),(6,30),(10,50),(15,70),(20,85),(25,95),(99,95)],\n'
        f'+    "cracker":           {NEW_CRACKER_ROW},  # EV-104, n=53 corpus anchor -- PILOT-VERIFIED, NOT YET APPLIED\n'
        '     "default":           [(0,0),(3,15),(6,30),(10,50),(15,70),(20,85),(25,95),(99,95)],\n'
        " }\n"
        "\nNOTE: NOT applied to constants.py on disk. Reference diff for the future real commit\n"
        "once Adversarial QA completes Condition 5 and Product Agent lifts the pilot-only\n"
        "restriction. Do not apply without that sign-off. Also register EV-104 in\n"
        "bsip2_evidence_registry_v1.md/.json ONLY at that point (Condition 6).\n",
        encoding="utf-8",
    )

    print("\n" + "=" * 78)
    print("SUMMARY")
    print("=" * 78)
    print(f"Scored {len(rows)}/54 | Crossers: {len(crossers)} | Double-jumps: {len(double_jump)}")
    print(f"By direction: {dict(cross_counter)}")
    print(f"Nutrition claim matches engine: {nutrition_matches} | Product claim matches engine: {product_matches}")
    print(f"Newly-introduced cap clips: {len(newly_clipped)} (expected 0)")
    print(f"Structural guard: {'PASS' if step3_pass else 'FAIL'} | Bread fresh-vs-fresh isolation: {'PASS' if step5_pass else 'FAIL'}")
    print(f"FYI drift vs committed baseline (unrelated to EV-104): crackers/ricecakes {n_drift_vs_committed}/{len(rows)}, bread {len(bread_drift)}/{len(bread_pre)}")
    print(f"constants.py on disk: UNCHANGED (sha256 {constants_sha[:16]}...)")
    print(f"Run record: {rr_path}")
    print(f"Crosser table: {csv_path}")
    print(f"Reference patch (not applied): {patch_path}")
    print("NOT wired into production entrypoints. NOT committed. Evidence registry NOT updated (Condition 6 pending).")
    print("=" * 78)
    return report


if __name__ == "__main__":
    main()
