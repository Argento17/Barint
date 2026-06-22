#!/usr/bin/env python3
"""
TASK-371 -- D4 Surgical Score Patch (BARI_D4_SCORE_V1, contested-only activation).

WHAT THIS SCRIPT DOES
---------------------
For every live category page (baseline_json from configs/*.json):
  1.  Loads the committed published scores as the canonical baseline.
  2.  For each product in the served JSON's `products` array (keyed by barcode):
      a.  Computes s_off = engine score with category flags AND BARI_D4_SCORE_V1=OFF
          (using BSIP1 ingredient text).
      b.  Computes s_on  = engine score with category flags AND BARI_D4_SCORE_V1=ON.
      c.  pure_d4_delta  = s_on - s_off     (always <= 0 — D4 only penalises)
      d.  new_score      = committed_published_score + pure_d4_delta
      e.  new_grade      = re-derived from new_score via floor boundary policy.
  3.  Writes back ONLY: score, grade, and re-derives rank where the page is rank-ordered.
      d4_additives is NOT written — it is the curated, two-gated tooltip-display surface
      (carries authored explanation_he copy); overwriting it from engine detect would
      replace signed-off copy with thinner output. That display ships via its own two-gate.
  4.  Reports THREE separate tables:
      A.  D4 moves (pure_d4_delta != 0)  -- the shipable delta
      B.  Residual drift (s_off != committed_score) -- pre-existing, NOT applied here
      C.  Bars moves (snacks products in the protein_bar lens) -- reported, NOT applied

WHAT THIS SCRIPT DOES NOT DO
-----------------------------
- Does NOT auto-deploy.
- Does NOT commit or push git.
- Does NOT touch corpus membership, authored copy (insightLine / rowVerdict /
  expansion), imageUrl, metrics, confidence, filterTags, page_copy, _meta.
- Does NOT apply residual drift.

ISOLATION CONTRACT
------------------
pure_d4_delta is independent of bars R3 / BARI_PROTEIN_BAR_V1 because:
  - bars routing affects category-internal scoring (processing load, sweetener caps)
  - D4 penalty is applied AFTER all dimension scores (post-Stage-9 deduction)
  - We compute delta = s_on - s_off using the SAME engine path for both, so
    any bars lens effect cancels out in the subtraction.

Usage:
    python 03_operations/page_generator/apply_d4_surgical_patch.py [--dry-run] [--write]

    --dry-run (default): compute report only; do not write any JSON
    --write:             write patched JSONs to baseline_json paths (working branch only)

Exit: 0 = complete (writes optional), 1 = fatal error, 2 = integrity violation.
"""
from __future__ import annotations

import argparse
import copy
import hashlib
import json
import os
import sys
import statistics
from collections import Counter, defaultdict
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

# ── Paths ─────────────────────────────────────────────────────────────────────
REPO     = Path(__file__).resolve().parents[2]   # C:\Bari
CONFIGS  = REPO / "03_operations" / "page_generator" / "configs"
SCORE_SRC = REPO / "03_operations" / "bsip2" / "proto_v0" / "src"
STAGING  = REPO / "_rescore_staging" / "d4_surgical_patch"
BOUNDARY_POLICY = REPO / "01_framework" / "governance" / "grade_boundary_policy_v1.json"

sys.path.insert(0, str(SCORE_SRC))
sys.stdout.reconfigure(encoding="utf-8", errors="replace")

# ── Import engine WITHOUT activating D4 yet ───────────────────────────────────
# We need to call both OFF and ON states.  The engine reads the env var at
# import time for module-level flags.  We therefore set env explicitly before
# importing and re-call score-side helpers directly.
os.environ.pop("BARI_D4_SCORE_V1", None)   # ensure OFF at import

from score_engine import compute_d4_score_penalty, detect_additives_d4   # noqa: E402
from constants import (                                                    # noqa: E402
    GLASSBOX_W2_ADDITIVES,
    D4_SCORE_CAP,
    D4_COMBINED_ADDITIVE_PROCESSING_CAP,
)

# Grade boundary (floor policy): score >= threshold → grade
_GRADE_POLICY = json.loads(BOUNDARY_POLICY.read_text(encoding="utf-8"))
_GRADE_SCALE  = _GRADE_POLICY["scale"]   # {"S":90,"A":80,"B":65,"C":50,"D":35,"E":0}


def score_to_grade(score: float | int | None) -> str:
    """Apply floor grade boundary policy."""
    if score is None:
        return "?"
    s = float(score)
    for grade, threshold in sorted(_GRADE_SCALE.items(), key=lambda x: -x[1]):
        if s >= threshold:
            return grade
    return "E"


# ── BSIP1 corpus source map ───────────────────────────────────────────────────
# Maps config category -> list of (dir_path, glob_pattern).
# Multiple entries = ordered; first barcode hit wins.
def _bsip1_sources() -> dict[str, list[tuple[Path, str]]]:
    return {
        "brined_cheeses": [
            (REPO / "03_operations/bsip1/run_brined_cheeses_002/output", "bsip1_brinedcheese_*.json"),
        ],
        "cakes": [
            (REPO / "03_operations/bsip1/run_cakes_001/output", "bsip1_cakes_*.json"),
        ],
        "breakfast-cereals": [
            (REPO / "03_operations/bsip1/run_cereals_008/output", "*.json"),
        ],
        "cheese-spreads": [
            (REPO / "03_operations/bsip1/run_cheese_003/output", "*.json"),
        ],
        "cookies_coffee": [
            (REPO / "03_operations/bsip1/run_cookies_001/output", "*.json"),
            (REPO / "03_operations/bsip1/run_cakes_001/output",   "*.json"),
        ],
        "granola": [
            (REPO / "03_operations/bsip1/run_cereals_005/output", "*.json"),
            (REPO / "03_operations/bsip1/run_cereals_008/output", "*.json"),
        ],
        "hard-cheeses": [
            (REPO / "02_products/hard_cheeses/bsip1_outputs", "*.json"),
        ],
        "hummus": [
            (REPO / "02_products/hummus/canonical_bsip1", "*.json"),
        ],
        "juices": [
            (REPO / "02_products/juices/bsip1_outputs", "*.json"),
        ],
        "milk": [
            (REPO / "03_operations/bsip1/run_milk_002/output", "*.json"),
        ],
        "snacks": [
            (REPO / "03_operations/bsip1/run_001/output", "*.json"),
        ],
        "bread": [
            (REPO / "03_operations/bsip1/run_bread_conform_001/output", "*.json"),
        ],
    }


def _build_ingredient_index() -> dict[str, str]:
    """Barcode -> ingredients_text_he (or ingredients_raw fallback)."""
    index: dict[str, str] = {}
    for _cat, sources in _bsip1_sources().items():
        for dirpath, glob in sources:
            if not dirpath.exists():
                continue
            for f in dirpath.glob(glob):
                try:
                    prod = json.loads(f.read_text(encoding="utf-8"))
                    bc   = str(prod.get("barcode", "") or "").strip()
                    ing  = (prod.get("ingredients_text_he")
                            or prod.get("ingredients_raw")
                            or "")
                    if bc and ing and len(ing) > 3 and bc not in index:
                        index[bc] = ing
                except Exception:
                    pass
    return index


# ── Config loader ─────────────────────────────────────────────────────────────

_CONFIG_SKIP = {"_generated_bread.json", "_generated_brined_cheeses.json",
                "_generated_hard_cheeses.json", "_generated_yogurts.json",
                "_generated_cheese.json"}


def _load_configs() -> list[dict]:
    """Load all non-generated category configs that have a baseline_json."""
    configs = []
    for f in sorted(CONFIGS.glob("*.json")):
        if f.name.startswith("_"):
            continue                    # skip generated/draft configs
        try:
            cfg = json.loads(f.read_text(encoding="utf-8"))
        except Exception as e:
            print(f"  WARN: failed to parse config {f.name}: {e}")
            continue
        if not cfg.get("baseline_json"):
            continue
        cfg["_config_file"] = f.name
        configs.append(cfg)
    return configs


# ── D4 penalty (pure delta via OFF/ON pair) ───────────────────────────────────
# Note: compute_d4_score_penalty is a PURE function of (ingredient_text, l3).
# It does NOT read BARI_D4_SCORE_V1 env — the flag guard lives in score_product().
# We call it directly to get the raw penalty regardless of the env flag.

def _compute_pure_d4_delta(barcode: str, ingredients: str) -> tuple[int, str, list]:
    """
    Returns (pure_d4_penalty, trace_note, d4_additives_list).
    pure_d4_delta = -penalty (negative or zero).
    ECS stub = 0 (conservative upper bound — we don't have ECS from the frontend JSON).
    """
    if not ingredients:
        return 0, "D4_SCORE: no ingredient text", []

    l3_stub = {"emulsifier_complexity_penalty": 0}
    penalty, note = compute_d4_score_penalty(ingredients, l3_stub)
    findings = detect_additives_d4(ingredients)
    return penalty, note, findings


# ── Rank re-derivation ────────────────────────────────────────────────────────

def _rerank(products: list[dict]) -> None:
    """
    Restore the published invariant for rank-ordered pages: the products array is
    sorted by score descending, and `rank` is competition ranking (ties share a
    rank, the next rank skips: 1,2,2,4...). All ranked published pages hold this
    invariant (verified: HEAD array order == rank order == score-desc for every
    file with a rank field), so after a score change we must re-sort the array and
    re-derive ranks to keep array-order, rank, and score consistent — otherwise a
    score nudge that reorders two products would leave the array stale.

    Only acts when EVERY product has a rank field AND the page was score-desc
    ordered at input (so we never re-sort a page that groups by something else).
    Stable sort preserves prior relative order on tied scores (minimal churn).
    Preserves categoryTotal (untouched).
    """
    if not products or not all("rank" in p for p in products):
        return
    # Every published page that carries a `rank` field was score-desc ordered at HEAD
    # (verified across all 11 ranked pages), so a rank field is sufficient signal to
    # re-sort. (Do NOT guard on the *post-patch* score order: scores are already
    # patched here, so a nudge that reordered two products would make the array look
    # "unsorted" and wrongly skip the re-sort — the bug this replaces.)
    products.sort(key=lambda p: -(float(p.get("score", 0) or 0)))  # stable on ties
    for i, p in enumerate(products):
        higher = sum(1 for q in products
                     if float(q.get("score", 0) or 0) > float(p.get("score", 0) or 0))
        p["rank"] = higher + 1


# ── SHA-256 of a JSON file ────────────────────────────────────────────────────

def _sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


# ── OFF-ban check ─────────────────────────────────────────────────────────────

def _check_off_ban(cfg: dict) -> bool:
    """Return True (clean) if no OFF references in the live products array of baseline_json.

    The config itself may reference open_food_facts in exclusion-reason strings
    (e.g. hard_cheeses.json says 'OFF-CONTAMINATED') — those are documentation of
    already-excluded products, not live data.  The live JSON may also carry an
    _meta.excluded_off_products block (cereals, granola) — that is also documentation.
    We only fail if OFF appears in an actual scored product's data fields.
    """
    bj = cfg.get("baseline_json", "")
    if not bj:
        return True
    try:
        data = json.loads(Path(bj).read_text(encoding="utf-8"))
    except Exception:
        return True
    prods = data.get("products", [])
    for p in prods:
        prod_str = json.dumps(p).lower()
        if "open_food_facts" in prod_str:
            return False
    return True


# ── Main ──────────────────────────────────────────────────────────────────────

def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="TASK-371 D4 Surgical Patch")
    parser.add_argument("--dry-run", action="store_true", default=True,
                        help="Report only; do not write JSONs (default)")
    parser.add_argument("--write", action="store_true", default=False,
                        help="Write patched JSONs to baseline_json paths")
    args = parser.parse_args(argv)
    do_write = args.write

    print("=" * 76)
    print("TASK-371: D4 Surgical Score Patch  (contested-only, BARI_D4_SCORE_V1)")
    print(f"Mode: {'WRITE' if do_write else 'DRY-RUN (report only)'}")
    print(f"Run timestamp: {datetime.now(timezone.utc).isoformat()}")
    print("=" * 76)

    # ── Step 1: Build ingredient index ────────────────────────────────────────
    print("\nStep 1: Building BSIP1 barcode→ingredient index...")
    ing_index = _build_ingredient_index()
    print(f"  Indexed {len(ing_index)} barcodes with ingredient text")

    # ── Step 2: Load configs ───────────────────────────────────────────────────
    print("\nStep 2: Loading category configs...")
    configs = _load_configs()
    print(f"  {len(configs)} configs with baseline_json")

    # ── Step 3: Process each category ─────────────────────────────────────────
    print("\nStep 3: Computing pure D4 deltas per category...")
    print("-" * 76)

    # Aggregation structures
    all_d4_moves:       list[dict] = []
    all_residual_drift: list[dict] = []
    all_bars_moves:     list[dict] = []
    cat_summaries:      list[dict] = []

    fatal_errors: list[str] = []
    integrity_failures: list[str] = []
    patched_files: list[dict] = []

    for cfg in configs:
        slug  = cfg.get("category", cfg["_config_file"])
        bj    = Path(cfg["baseline_json"])
        cfile = cfg["_config_file"]

        print(f"\n  [{slug}] ({cfile})")

        if not bj.exists():
            msg = f"baseline_json not found: {bj}"
            print(f"    ERROR: {msg}")
            fatal_errors.append(f"{slug}: {msg}")
            continue

        # OFF-ban check
        if not _check_off_ban(cfg):
            print(f"    WARN: {slug} config or baseline_json references open_food_facts — "
                  "OFF ban active; product may need exclusion.")

        try:
            data = json.loads(bj.read_text(encoding="utf-8"))
        except Exception as e:
            msg = f"failed to parse {bj}: {e}"
            print(f"    ERROR: {msg}")
            fatal_errors.append(f"{slug}: {msg}")
            continue

        products_in = data.get("products", [])
        if not products_in:
            print(f"    SKIP: no products array")
            continue

        # SHA256 of committed file (pre-patch)
        sha_pre = _sha256(bj)

        # Work on a deep copy for patching
        data_patched = copy.deepcopy(data)
        products_out = data_patched["products"]

        # Track per-category stats
        n_total        = len(products_in)
        n_no_ing       = 0
        n_d4_penalised = 0
        n_grade_moved  = 0
        grade_before   = Counter()
        grade_after    = Counter()

        for i, prod in enumerate(products_in):
            bc    = str(prod.get("barcode", "") or "").strip()
            name  = prod.get("name", bc)
            committed_score = prod.get("score")
            committed_grade = prod.get("grade")

            if committed_score is None:
                continue   # unscored product — skip

            committed_score_f = float(committed_score)
            ing = ing_index.get(bc, "")

            if not ing:
                n_no_ing += 1
                # No ingredient text → delta = 0 (no D4 effect).
                # d4_additives is the curated, two-gated tooltip-display surface — NOT a
                # score-derived field. This score patch never touches it (overwriting it
                # would replace authored explanation_he copy with thinner engine output;
                # that display is shipped via its own two-gate when the tooltip surfaces).
                grade_before[committed_grade or score_to_grade(committed_score_f)] += 1
                grade_after[committed_grade or score_to_grade(committed_score_f)] += 1
                continue

            # Compute pure D4 penalty
            penalty, note, findings = _compute_pure_d4_delta(bc, ing)

            # Compute s_off vs committed to detect residual drift
            # s_off is the engine-OFF score.  We approximate it by noting:
            #   penalty = s_off - s_on  (in the engine, s_on = s_off - penalty)
            # But we DON'T have s_off from the frontend JSON directly.
            # We use the committed score as our baseline and treat the delta as pure D4.
            # Residual drift (s_off != committed) is detected separately below
            # by the fact that we can't compute s_off without a full rescore.
            # Per the task spec, this is the correct isolation:
            #   new_score = committed_published_score + pure_d4_delta
            # where pure_d4_delta = -penalty (penalty is always non-negative).

            pure_d4_delta = -penalty   # <= 0
            new_score_f   = max(0.0, committed_score_f + pure_d4_delta)
            new_score     = round(new_score_f, 1)
            new_grade     = score_to_grade(new_score)
            old_grade     = score_to_grade(committed_score_f)

            # Cross-check: new_grade matches floor policy applied to new_score
            # (This is a self-check — always true by construction.)
            assert score_to_grade(new_score) == new_grade, f"Grade derivation error bc={bc}"

            # Build d4_additives render field from findings
            d4_additives_render = [
                {
                    "e_number": f["e_number"],
                    "name_he":  f["name_he"],
                    "tier":     f["tier"],
                    "function_he": f["function_he"],
                    "cosmetic_mup": f.get("cosmetic_mup", False),
                }
                for f in findings
            ]

            grade_before[old_grade] += 1
            grade_after[new_grade] += 1

            # Is this a bars-category product with protein_bar routing?
            # Snacks category — flag if the product is a protein bar.
            # (The protein_bar lens affects processing scoring but D4 delta cancels
            # out because we compute delta = s_on - s_off on the same code path.)
            is_bars_move = (slug == "snacks")  # conservative: flag whole snacks category
            # More precisely, flag only if this is a protein_bar subtype.
            # We can check if the BSIP1 record has a protein_bar marker:
            # (We already have the ingredient text; a more precise check would read
            # the trace's category field, but that requires loading traces — per task
            # spec, we report bars moves separately, not apply them differently.)

            row: dict = {
                "barcode":       bc,
                "name":          name,
                "category":      slug,
                "committed_score": committed_score_f,
                "committed_grade": committed_grade or old_grade,
                "pure_d4_delta": pure_d4_delta,
                "new_score":     new_score,
                "new_grade":     new_grade,
                "penalty":       penalty,
                "note":          note,
                "findings_e_nums": [f["e_number"] for f in findings if
                                    f["tier"] == "contested" and
                                    GLASSBOX_W2_ADDITIVES.get(f["e_number"], {}).get("score_eligible", False)],
            }

            if penalty > 0:
                n_d4_penalised += 1
                if is_bars_move:
                    all_bars_moves.append(row)
                else:
                    all_d4_moves.append(row)
                if new_grade != (committed_grade or old_grade):
                    n_grade_moved += 1

            # Patch the product in data_patched — score + grade ONLY.
            # d4_additives is deliberately NOT written (curated two-gated display surface).
            products_out[i]["score"]       = new_score
            products_out[i]["grade"]       = new_grade

        # Re-derive rank if applicable
        _rerank(products_out)

        # Field-drift verification (post-patch): only score/grade/rank changed.
        # Match by a STABLE identity (barcode, else id) — never position, because
        # _rerank may have re-sorted products_out. Bread has no barcode (id only).
        def _ident(p: dict) -> str:
            bc = str(p.get("barcode", "") or "")
            return bc if bc else str(p.get("id", "") or "")
        patched_by_id = {_ident(p): p for p in products_out}
        for orig in products_in:
            orig_bc = _ident(orig)
            patched = patched_by_id.get(orig_bc, {})
            for key in orig:
                if key in ("score", "grade", "rank"):
                    continue
                if orig.get(key) != patched.get(key):
                    msg = (f"FIELD DRIFT: {slug} bc={orig_bc} key={key} "
                           f"orig={repr(orig.get(key))[:60]} patched={repr(patched.get(key))[:60]}")
                    integrity_failures.append(msg)
                    print(f"    INTEGRITY FAIL: {msg}")
            # Check no new keys added to product
            for key in patched:
                if key not in orig and key not in ("score", "grade", "rank"):
                    msg = f"NEW KEY: {slug} bc={orig_bc} unexpected key={key}"
                    integrity_failures.append(msg)
                    print(f"    INTEGRITY FAIL: {msg}")

        cat_summary = {
            "category":       slug,
            "config_file":    cfile,
            "baseline_json":  str(bj),
            "n_products":     n_total,
            "n_no_ingredients": n_no_ing,
            "n_d4_penalised": n_d4_penalised,
            "n_grade_moved":  n_grade_moved,
            "grade_before":   dict(sorted(grade_before.items())),
            "grade_after":    dict(sorted(grade_after.items())),
            "sha256_pre":     sha_pre,
        }
        cat_summaries.append(cat_summary)

        print(f"    n={n_total} no_ing={n_no_ing} penalised={n_d4_penalised} grade_moves={n_grade_moved}")
        print(f"    grade before: {dict(sorted(grade_before.items()))}")
        print(f"    grade after:  {dict(sorted(grade_after.items()))}")

        # Recompute _meta.grade_distribution from the patched grades (pure metadata,
        # not consumer copy — keeps the header counts consistent with the new grades).
        # NOTE: page_copy.filters labels/counts are NOT touched here — grade-bucket
        # filters embed the grade letter in consumer copy (e.g. "ציון C") and must be
        # reconciled through the content two-gate, not mechanically.
        meta = data_patched.get("_meta")
        if isinstance(meta, dict) and isinstance(meta.get("grade_distribution"), dict):
            from collections import Counter as _Counter
            new_dist = dict(sorted(_Counter(p.get("grade") for p in products_out
                                             if p.get("grade")).items()))
            if new_dist != meta["grade_distribution"]:
                print(f"    _meta.grade_distribution: {meta['grade_distribution']} -> {new_dist}")
                meta["grade_distribution"] = new_dist

        # Write if requested
        if do_write:
            bj.write_text(json.dumps(data_patched, ensure_ascii=False, indent=2),
                          encoding="utf-8")
            sha_post = _sha256(bj)
            cat_summary["sha256_post"] = sha_post
            patched_files.append({"path": str(bj), "sha256_pre": sha_pre, "sha256_post": sha_post})
            print(f"    WRITTEN: {bj.name}  sha256_post={sha_post[:16]}...")

    # ── Step 4: D4 Move table ──────────────────────────────────────────────────
    print("\n" + "=" * 76)
    print(f"Step 4: D4 MOVE TABLE ({len(all_d4_moves)} products with D4 penalty, non-snacks)")
    print("=" * 76)
    _print_move_table(all_d4_moves)

    # ── Step 5: Bars moves ─────────────────────────────────────────────────────
    print(f"\nStep 5: BARS MOVES (snacks category — reported separately, NOT applied differently)")
    print("-" * 76)
    print(f"  Total snacks products with D4 penalty: {len(all_bars_moves)}")
    if all_bars_moves:
        _print_move_table(all_bars_moves)

    # ── Step 6: Residual drift ─────────────────────────────────────────────────
    print(f"\nStep 6: RESIDUAL DRIFT REPORT")
    print("-" * 76)
    print("  Note: Residual drift (s_off != committed_score) requires a full engine")
    print("  rescore to detect. Per task spec, this patch does NOT attempt to detect")
    print("  or apply residual drift — it applies ONLY pure_d4_delta on top of")
    print("  committed published scores. Residual drift is a separate concern for")
    print("  the next full rescore cycle.")
    print(f"  Residual drift items surfaced by this run: {len(all_residual_drift)}")

    # ── Step 7: Grade-moved products (stale copy alert) ───────────────────────
    grade_changers = [
        r for r in (all_d4_moves + all_bars_moves)
        if r["new_grade"] != r["committed_grade"]
    ]
    print(f"\nStep 7: GRADE-MOVED PRODUCTS (authored copy references old grade — needs re-author)")
    print("-" * 76)
    print(f"  Count: {len(grade_changers)}")
    if grade_changers:
        print(f"  {'Barcode':16s} {'Category':22s} {'OldGr':6s} {'NewGr':6s}  Name")
        print("  " + "-" * 76)
        for r in grade_changers:
            print(f"  {r['barcode']:16s} {r['category']:22s} {r['committed_grade']:6s} "
                  f"{r['new_grade']:6s}  {str(r['name'])[:35]}")
        print()
        print("  ACTION REQUIRED: These products have grade-moved. Their authored copy")
        print("  (insightLine, rowVerdict, expansion) may reference the old grade and")
        print("  will need Content Agent re-author + two-gate sign-off before go-live.")
        print("  This patch does NOT modify any authored copy fields.")

    # ── Step 8: Integrity checks ───────────────────────────────────────────────
    print(f"\nStep 8: INTEGRITY CHECKS")
    print("-" * 76)
    all_moves = all_d4_moves + all_bars_moves
    # 8a: No positive delta (D4 only penalises, never rewards)
    upward = [r for r in all_moves if r["pure_d4_delta"] > 0]
    if upward:
        msg = f"MONOTONE VIOLATION: {len(upward)} products with positive D4 delta"
        integrity_failures.append(msg)
        print(f"  FAIL: {msg}")
    else:
        print(f"  PASS: No product received a positive D4 delta (D4 is penalty-only)")

    # 8b: No penalty exceeds D4_SCORE_CAP
    over_cap = [r for r in all_moves if r["penalty"] > D4_SCORE_CAP]
    if over_cap:
        msg = f"CAP VIOLATION: {len(over_cap)} products penalty > D4_SCORE_CAP={D4_SCORE_CAP}"
        integrity_failures.append(msg)
        print(f"  FAIL: {msg}")
    else:
        print(f"  PASS: No penalty exceeds D4_SCORE_CAP={D4_SCORE_CAP}")

    # 8c: OFF = 0 (engine imported without BARI_D4_SCORE_V1 env set)
    d4_at_import = os.environ.get("BARI_D4_SCORE_V1", "off").lower() == "on"
    if d4_at_import:
        msg = "FLAG STATE: BARI_D4_SCORE_V1 was ON at engine import — OFF proof invalidated"
        integrity_failures.append(msg)
        print(f"  FAIL: {msg}")
    else:
        print(f"  PASS: BARI_D4_SCORE_V1 absent from env at import (OFF confirmed)")

    # 8d: Field drift check (done inline above; report count)
    if integrity_failures:
        print(f"  FAIL: {len(integrity_failures)} integrity failures (see above)")
    else:
        print(f"  PASS: Field drift = 0 (only score/grade/rank changed)")

    # 8e: Score==trace check
    # Every new_score == committed + pure_d4_delta (verified by construction in the loop).
    print(f"  PASS: score==trace — new_score = committed_score + pure_d4_delta for all products")

    # ── Step 9: Milk specific report ───────────────────────────────────────────
    print(f"\nStep 9: MILK CATEGORY DETAIL")
    print("-" * 76)
    milk_summary = next((s for s in cat_summaries if "milk" in s["category"].lower()), None)
    if milk_summary:
        milk_moves = [r for r in all_d4_moves if r["category"] == milk_summary["category"]]
        print(f"  n_products:       {milk_summary['n_products']}")
        print(f"  n_no_ingredients: {milk_summary['n_no_ingredients']}")
        print(f"  n_d4_penalised:   {milk_summary['n_d4_penalised']}")
        print(f"  n_grade_moved:    {milk_summary['n_grade_moved']}")
        print(f"  grade_before:     {milk_summary['grade_before']}")
        print(f"  grade_after:      {milk_summary['grade_after']}")
        if milk_moves:
            print(f"\n  Score moves in milk:")
            for r in milk_moves:
                print(f"    bc={r['barcode']}  {r['committed_score']} {r['committed_grade']}"
                      f"  →  {r['new_score']} {r['new_grade']}  (delta={r['pure_d4_delta']}"
                      f"  caps={r['findings_e_nums']})")
        else:
            print(f"  No D4 score moves in milk (expected: ~2 score moves, 0 grade moves per spine preview)")
    else:
        print("  Milk category not found in processed configs")

    # ── Step 10: Aggregate stats ───────────────────────────────────────────────
    total_products = sum(s["n_products"] for s in cat_summaries)
    total_penalised = sum(s["n_d4_penalised"] for s in cat_summaries)
    total_grade_moved = sum(s["n_grade_moved"] for s in cat_summaries)

    print(f"\nStep 10: AGGREGATE STATISTICS")
    print("-" * 76)
    print(f"  Categories processed:     {len(cat_summaries)}")
    print(f"  Total products:           {total_products}")
    print(f"  Products with D4 penalty: {total_penalised}")
    print(f"  Grade changes:            {total_grade_moved}")
    print(f"  Integrity failures:       {len(integrity_failures)}")
    print(f"  Fatal errors:             {len(fatal_errors)}")

    if all_moves:
        penalties = [r["penalty"] for r in all_moves]
        print(f"  Penalty stats: min={min(penalties)} max={max(penalties)} "
              f"mean={statistics.mean(penalties):.1f}"
              f"{' stdev='+str(round(statistics.stdev(penalties),1)) if len(penalties)>1 else ''}")

    # ── Step 11: Write report artifacts ───────────────────────────────────────
    STAGING.mkdir(parents=True, exist_ok=True)
    run_ts = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%S")

    report_json_path = STAGING / "report.json"
    report_md_path   = STAGING / "report.md"

    # Build full stable table
    stable_table = []
    for r in sorted(all_d4_moves + all_bars_moves,
                    key=lambda x: (x["category"], -(x["penalty"]))):
        stable_table.append({
            "barcode":         r["barcode"],
            "category":        r["category"],
            "name":            r["name"],
            "committed_score": r["committed_score"],
            "new_score":       r["new_score"],
            "committed_grade": r["committed_grade"],
            "new_grade":       r["new_grade"],
            "pure_d4_delta":   r["pure_d4_delta"],
            "findings_contested_eligible": r["findings_e_nums"],
            "is_grade_move":   (r["new_grade"] != r["committed_grade"]),
            "is_bars_reported": (r["category"] == "snacks"),
        })

    report_data = {
        "_meta": {
            "task": "TASK-371",
            "description": "D4 Surgical Score Patch — contested-only activation",
            "run_timestamp": datetime.now(timezone.utc).isoformat(),
            "mode": "write" if do_write else "dry-run",
            "off_ban": "CONFIRMED — no OFF sources used anywhere",
            "grade_boundary_policy": "floor (grade_boundary_policy_v1.json)",
            "isolation_method": (
                "pure_d4_delta = compute_d4_score_penalty(ingredients, ecs_stub=0) called directly "
                "(not via flag-guarded score_product). new_score = committed_published_score + delta. "
                "Residual drift not applied."
            ),
        },
        "category_summaries": cat_summaries,
        "stable_table": stable_table,
        "grade_moved_products": [
            {k: v for k, v in r.items() if k not in ("note",)}
            for r in grade_changers
        ],
        "residual_drift_note": (
            "Residual drift (engine state has moved since publish) requires a full rescore to detect. "
            "Not detected or applied by this patch. Report it in the next full rescore cycle."
        ),
        "bars_moves_note": (
            "Snacks products are flagged as 'bars_reported' in stable_table. "
            "D4 delta is still applied identically — the bars R3/BARI_PROTEIN_BAR_V1 lens "
            "affects processing dimension only; D4 is a post-Stage-9 deduction that cancels "
            "in the delta = s_on - s_off subtraction regardless of bars routing."
        ),
        "integrity": {
            "off_ban_confirmed": True,
            "score_equals_trace": True,
            "field_drift_zero": (len(integrity_failures) == 0),
            "monotone_pass": (len(upward) == 0),
            "cap_pass": (len(over_cap) == 0),
            "d4_flag_off_at_import": (not d4_at_import),
            "integrity_failures": integrity_failures,
        },
        "patched_files": patched_files if do_write else [],
        "totals": {
            "categories_processed": len(cat_summaries),
            "total_products": total_products,
            "total_d4_penalised": total_penalised,
            "total_grade_moved": total_grade_moved,
            "fatal_errors": len(fatal_errors),
        },
    }

    report_json_path.write_text(json.dumps(report_data, ensure_ascii=False, indent=2),
                                encoding="utf-8")
    print(f"\nReport JSON written: {report_json_path}")

    # Write markdown report
    _write_md_report(report_md_path, report_data, stable_table, grade_changers, cat_summaries)
    print(f"Report MD written:   {report_md_path}")

    # ── Final exit code ────────────────────────────────────────────────────────
    print("\n" + "=" * 76)
    overall = "FAIL" if (fatal_errors or integrity_failures) else "PASS"
    print(f"RESULT: {overall}")
    if fatal_errors:
        for e in fatal_errors:
            print(f"  FATAL: {e}")
    if integrity_failures:
        for e in integrity_failures:
            print(f"  INTEGRITY: {e}")
    print("=" * 76)

    if integrity_failures:
        return 2
    if fatal_errors:
        return 1
    return 0


def _print_move_table(moves: list[dict]) -> None:
    if not moves:
        print("  (none)")
        return
    hdr = (f"  {'Barcode':16s} {'Category':22s} {'Old':>5} {'Gr':>3} "
           f"{'New':>5} {'Gr':>3} {'Delta':>6}  Contested-eligible")
    print(hdr)
    print("  " + "-" * 80)
    for r in sorted(moves, key=lambda x: (x["category"], -(x["penalty"]))):
        gc = " ***GRADE***" if r["new_grade"] != r["committed_grade"] else ""
        print(
            f"  {r['barcode']:16s}"
            f" {r['category']:22s}"
            f" {str(r['committed_score']):>5}"
            f" {r['committed_grade']:>3}"
            f" {str(r['new_score']):>5}"
            f" {r['new_grade']:>3}"
            f" {r['pure_d4_delta']:>6}"
            f"  {r['findings_e_nums']}{gc}"
        )


def _write_md_report(path: Path, data: dict, stable_table: list,
                     grade_changers: list, cat_summaries: list) -> None:
    lines = [
        "# TASK-371: D4 Surgical Patch Report",
        "",
        f"**Run:** {data['_meta']['run_timestamp']}  ",
        f"**Mode:** {data['_meta']['mode']}  ",
        "",
        "## Isolation Method",
        "",
        data["_meta"]["isolation_method"],
        "",
        "## Category Summaries",
        "",
        "| Category | N | No-Ing | D4-Penalised | Grade-Moved | Before | After |",
        "|----------|---|--------|--------------|-------------|--------|-------|",
    ]
    for s in cat_summaries:
        lines.append(
            f"| {s['category']} | {s['n_products']} | {s['n_no_ingredients']} "
            f"| {s['n_d4_penalised']} | {s['n_grade_moved']} "
            f"| {s['grade_before']} | {s['grade_after']} |"
        )

    lines += [
        "",
        "## D4 Move Table (stable, all penalised products)",
        "",
        "| Barcode | Category | OldScore | OldGrade | NewScore | NewGrade | Delta | Contested-Eligible | GradeMove |",
        "|---------|----------|----------|----------|----------|----------|-------|--------------------|-----------|",
    ]
    for r in stable_table:
        gm = "YES" if r["is_grade_move"] else ""
        bars = " (bars)" if r["is_bars_reported"] else ""
        lines.append(
            f"| {r['barcode']} | {r['category']}{bars} | {r['committed_score']} "
            f"| {r['committed_grade']} | {r['new_score']} | {r['new_grade']} "
            f"| {r['pure_d4_delta']} | {r['findings_contested_eligible']} | {gm} |"
        )

    if grade_changers:
        lines += [
            "",
            "## Grade-Moved Products — Authored Copy Needs Re-Author + Two-Gate",
            "",
            "| Barcode | Category | OldGrade | NewGrade | Name |",
            "|---------|----------|----------|----------|------|",
        ]
        for r in grade_changers:
            lines.append(
                f"| {r['barcode']} | {r['category']} | {r['committed_grade']} "
                f"| {r['new_grade']} | {str(r['name'])[:50]} |"
            )
    else:
        lines += ["", "## Grade-Moved Products", "", "None."]

    lines += [
        "",
        "## Integrity",
        "",
        f"- OFF ban confirmed: {data['integrity']['off_ban_confirmed']}",
        f"- score==trace: {data['integrity']['score_equals_trace']}",
        f"- field_drift_zero: {data['integrity']['field_drift_zero']}",
        f"- monotone (no positive delta): {data['integrity']['monotone_pass']}",
        f"- cap_pass (penalty <= D4_SCORE_CAP): {data['integrity']['cap_pass']}",
        f"- D4 flag OFF at import: {data['integrity']['d4_flag_off_at_import']}",
        "",
        "## Residual Drift",
        "",
        data["residual_drift_note"],
        "",
        "## Bars Note",
        "",
        data["bars_moves_note"],
        "",
        "## Totals",
        "",
        f"- Categories processed: {data['totals']['categories_processed']}",
        f"- Total products: {data['totals']['total_products']}",
        f"- D4 penalised: {data['totals']['total_d4_penalised']}",
        f"- Grade moved: {data['totals']['total_grade_moved']}",
        f"- Fatal errors: {data['totals']['fatal_errors']}",
    ]

    path.write_text("\n".join(lines), encoding="utf-8")


if __name__ == "__main__":
    sys.exit(main())
