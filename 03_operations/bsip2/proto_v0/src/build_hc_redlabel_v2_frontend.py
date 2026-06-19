# -*- coding: utf-8 -*-
"""
Build hard_cheeses_frontend_v2.json from run_hc_redlabel_v2_001 scores.

Strategy:
  - Start from the LIVE frontend JSON (preserves all display fields: name,
    imageUrl, id, confidence, d4_additives, expansion, insightLine, rowVerdict,
    subPool, novaGroup, retailer, source_traceability_status, etc.)
  - Overwrite: score, grade, rank, categoryTotal
  - Add _stale_verdict flag to any product whose rowVerdict/insightLine
    references a score/grade/rank that is now stale (for copy update pass)
  - Update _meta: run_id, generated, config_sha256 (clear), grade_dist,
    schema_version

Preserves: ALL consumer-facing prose (insightLine, rowVerdict, expansion.*).
           Consumer copy redone in a separate pass.

Outputs to: C:\\bari_hcredlabel\\bari-web\\src\\data\\comparisons\\hard_cheeses_frontend_v2.json
"""
import json, pathlib, datetime, hashlib, sys

sys.stdout.reconfigure(encoding="utf-8", errors="replace")

WORKTREE = pathlib.Path(r"C:\bari_hcredlabel")
FRONTEND_JSON = WORKTREE / "bari-web" / "src" / "data" / "comparisons" / "hard_cheeses_frontend_v2.json"
RUN_SUMMARY = WORKTREE / "02_products" / "hard_cheeses" / "bsip2_outputs" / "run_hc_redlabel_v2_001" / "run_summary.json"

# Stale verdict detection: strings in insightLine/rowVerdict that contain
# score/grade/rank references that may now be wrong.
# We flag products where grade changed OR rank changed by >3 positions.
GRADE_CHANGE_BARCODES = {
    "3073781199918",  # D->B
    "8711528211138",  # C->B
    "7290017065434",  # C->B
}


def run():
    # Load live frontend — this is the BEFORE state (read before any writes)
    fe = json.loads(FRONTEND_JSON.read_text("utf-8"))
    products_old = {p["barcode"]: p for p in fe["products"]}

    # Capture before-state scores/grades/ranks for stale detection
    before_state = {
        p["barcode"]: {
            "score": p["score"],
            "grade": p["grade"],
            "rank":  p["rank"],
        }
        for p in fe["products"]
    }

    # Load new scores
    summary = json.loads(RUN_SUMMARY.read_text("utf-8"))
    new_scores = {r["barcode"]: r for r in summary["per_product"]}

    # Compute new ranks using exact same formula as conform_baseline.build_score_rank:
    # rank(p) = 1 + count of products with strictly higher score
    # This produces competition ranking (ties share same rank; next rank skips count).
    all_scores_list = [new_scores[bc]["score"] or 0.0 for bc in new_scores]
    rank_map = {
        bc: 1 + sum(1 for s in all_scores_list if s > (new_scores[bc]["score"] or 0.0))
        for bc in new_scores
    }

    # Sort for output: by score descending, stable
    sorted_bcs = sorted(new_scores.keys(), key=lambda b: new_scores[b]["score"] or 0, reverse=True)
    category_total = len(sorted_bcs)

    # Build updated product list in new rank order
    products_new = []
    stale_verdict_barcodes = []

    for bc in sorted_bcs:
        p = dict(products_old[bc])  # shallow copy
        old_score = p["score"]
        old_grade = p["grade"]
        old_rank = p["rank"]

        p["score"] = new_scores[bc]["score"]
        p["grade"] = new_scores[bc]["grade"]
        p["rank"] = rank_map[bc]
        p["categoryTotal"] = category_total

        # Detect stale verdicts vs ORIGINAL before-state (not the newly written values)
        # Do NOT add _stale_verdict to product dict (caps_applied is forbidden key per conform check)
        orig = before_state.get(bc, {})
        orig_grade = orig.get("grade", old_grade)
        orig_rank = orig.get("rank", old_rank)
        rank_shift = abs(p["rank"] - orig_rank)
        grade_changed = p["grade"] != orig_grade
        if grade_changed or rank_shift > 3:
            stale_verdict_barcodes.append(bc)

        products_new.append(p)

    # Grade distribution
    from collections import Counter
    grade_dist = dict(Counter(p["grade"] for p in products_new))

    # Update meta
    meta = dict(fe["_meta"])
    meta["run_id"] = "run_hc_redlabel_v2_001"
    meta["generated"] = datetime.datetime.now(datetime.timezone.utc).isoformat()
    meta["product_count"] = category_total
    meta["scored_count"] = category_total
    meta["schema_version"] = "v3-redlabel-v2"
    meta["retailer_breakdown"] = {"yohananof": category_total}
    meta["scoring_flags"] = {
        "BARI_SHELF_RELATIVE_V1": "on",
        "BARI_FAT_TECH_V1": "on",
        "BARI_RECAL_P0": "on",
        "BARI_REDLABEL_V1": "on",
        "BARI_HC002_NOVA1": "on",
    }
    meta["redlabel_v1_changes"] = {
        "binary_cap_removed": "ISRAELI_RED_LABELS_2_PLUS(cap=45) replaced by REFORMULABLE_LABELS_2_PLUS (endemic sat_fat excluded from reformulable count)",
        "sodium_cliff_removed": "HIGH_SODIUM_700MG_PLUS(cap=60) replaced by SODIUM_GENERAL_BANDS graduated penalty (700-899mg=8pt, 600-699mg=4pt, 450-599mg=2pt)",
        "reg_quality_formula": "continuous per-label deduction (zero-base) replacing binary 95/60/25 step function",
        "grade_changes": list(GRADE_CHANGE_BARCODES),
    }
    meta["stale_verdicts"] = stale_verdict_barcodes
    meta["grade_distribution"] = grade_dist
    meta["config_sha256"] = "(pending — regenerate from signed config)"
    meta["patch_notes"] = (
        meta.get("patch_notes", "") +
        " TASK-fan-hcredlabel: BARI_REDLABEL_V1=on — binary ISRAELI_RED_LABELS_2_PLUS cap removed, "
        "HIGH_SODIUM_700MG_PLUS cliff removed, graduated reg_qual formula. "
        "3 grade changes: Babybel D->B, Dutch Gouda C->B, Imported Goat Gouda C->B. "
        "Stale verdicts flagged for copy update pass."
    )

    output = {"_meta": meta, "products": products_new}

    FRONTEND_JSON.write_text(
        json.dumps(output, ensure_ascii=False, indent=2), encoding="utf-8"
    )
    print(f"Written: {FRONTEND_JSON}")
    print(f"Products: {len(products_new)}")
    print(f"Grade dist: {grade_dist}")
    print(f"Stale verdicts ({len(stale_verdict_barcodes)}): {stale_verdict_barcodes}")
    return output


if __name__ == "__main__":
    run()
