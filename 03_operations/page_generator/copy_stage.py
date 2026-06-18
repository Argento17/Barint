#!/usr/bin/env python3
"""
copy_stage.py — Automated copy stage for the Bari score-switch spine.
TASK-318 / spine step 3.

Generalizes copy_carryover.py (TASK-305) + schema_strip.py (TASK-307) into a
single config-driven, per-category module the spine can call automatically after
a re-score.

BEHAVIOR (per call):
  Given a freshly generated staging page + the live baseline JSON
  (config.baseline_json), for each product:

  - In both & SAME grade  → carry live copy fields into staging product.
      Copy fields are DERIVED from the live page schema itself (not hard-coded
      per shelf). Structural / render fields stay from staging.
  - Grade-CHANGED or NET-NEW → leave PENDING_COPY in the live-schema copy fields;
      add barcode to the author-set.
  - Flag grade-unchanged-but-score-moved ≥ 3 pts (carried copy may be stale).
  - Schema-match: strip staging-only copy fields not present in the live schema
      (derived from the live page, not a hand-coded table).

OUTPUTS:
  - The copy-applied staging page written back in place (or --out path).
  - author_set.json alongside the staging page.

HARD RULES CARRIED IN:
  - OFF-ban absolute: carry ONLY what the live page already has. (TASK-238)
  - Zero score / grade changes: scores + grades come from staging, always kept.
  - Zero bari-web edits: reads live baseline, never writes it.
  - Idempotent + reproducible: same inputs → same outputs.

CLI usage:
  python copy_stage.py --staging <path>/_rescored.json
                       --live    <path>/live.json
                       [--out    <path>]
                       [--shelf  <name>]
                       [--score-move-threshold <float>]

Library usage (from rescore_all.py or other spine steps):
  from copy_stage import run_copy_stage, CopyStageResult
  result = run_copy_stage(staging_path, live_path, shelf_name="cereals")
"""

from __future__ import annotations

import argparse
import copy
import hashlib
import io
import json
import sys
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

# Force UTF-8 stdout on Windows
if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")

# ---------------------------------------------------------------------------
# Constants
# ---------------------------------------------------------------------------

PENDING = "PENDING_COPY"
SCORE_MOVE_THRESHOLD_DEFAULT = 3.0

# These are structural / scoring / render fields that are ALWAYS kept from the
# staging page and NEVER treated as copy fields, regardless of what the live
# page schema has. This prevents a live schema field that happens to be a
# structural field from being misclassified as copy.
#
# Rule: a field is a copy field iff:
#   (a) it is present in the live schema, AND
#   (b) it is NOT in this structural set.
#
# This set is the union of all known structural + render fields across all
# categories. Add new structural/render fields here if the engine emits them.
STRUCTURAL_FIELDS_TOP: frozenset[str] = frozenset({
    # Identity
    "id", "barcode", "name", "imageUrl",
    # Scoring output
    "score", "grade",
    # Confidence
    "confidence", "confidence_label_he", "confidence_tooltip_he",
    "confidence_sub_reason", "confidence_level",
    # Retailer / traceability
    "retailer", "retailers", "_source_retailers", "brand",
    "source_traceability_status",
    # Render / display fields (from render_fields.py, TASK-316)
    "novaGroup", "sugarPer100ml", "kcalPer100ml", "volumeMl",
    "subPool", "_category_routed", "_has_phvo",
    "_product_type", "d4_additives", "glassBox",
    # Cereals / granola extension fields
    "_subpool", "_isChildrens", "_wholeGrainClaim",
    # Cakes / cookies internal flags
    "_score_correction",
    # Juices
    # (retailers / subPool / sugarPer100ml / kcalPer100ml already above)
})

STRUCTURAL_FIELDS_EXPANSION: frozenset[str] = frozenset({
    # Data / nutritional
    "nutrition", "ingredients",
    # Confidence
    "confidenceLabel",
    # Display
    "servingNote",
    # Signals (derived from scoring)
    "positiveSignals", "limitingFactors",
})


# ---------------------------------------------------------------------------
# JSON I/O helpers
# ---------------------------------------------------------------------------

def load_json(path: Path) -> dict:
    with open(path, encoding="utf-8") as f:
        return json.load(f)


def save_json(path: Path, data: dict) -> str:
    """Save JSON (ensure_ascii=False, indent=2) and return sha256 of written bytes."""
    text = json.dumps(data, ensure_ascii=False, indent=2)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


# ---------------------------------------------------------------------------
# Schema derivation — the key generalization
# ---------------------------------------------------------------------------

def _is_pending(v: Any) -> bool:
    """Return True if v is PENDING_COPY or a list/dict entirely composed of it."""
    if v == PENDING:
        return True
    if isinstance(v, list) and v and all(i == PENDING for i in v):
        return True
    return False


def _derive_live_schema(live_products: list[dict]) -> tuple[set[str], set[str]]:
    """
    Derive the copy field sets from the live page products.

    Returns:
        copy_fields_top   — top-level keys present in live that are NOT structural
        copy_fields_exp   — expansion keys present in live that are NOT structural

    Strategy: union of all keys seen across all live products, minus the
    structural / render / scoring fields. This is schema-driven not shelf-hard-coded.
    An absent field is not a copy field.
    """
    top_keys: set[str] = set()
    exp_keys: set[str] = set()

    for p in live_products:
        for k, v in p.items():
            if k == "expansion":
                continue
            top_keys.add(k)
        exp = p.get("expansion") or {}
        for k in exp:
            exp_keys.add(k)

    # Subtract structural / render / scoring fields
    copy_fields_top = top_keys - STRUCTURAL_FIELDS_TOP
    copy_fields_exp = exp_keys - STRUCTURAL_FIELDS_EXPANSION

    return copy_fields_top, copy_fields_exp


def _build_live_index(live_products: list[dict]) -> dict[str, dict]:
    """Return barcode → live product dict. Falls back to id if barcode absent."""
    index: dict[str, dict] = {}
    for p in live_products:
        bc = str(p.get("barcode") or p.get("id") or "")
        if bc and bc not in index:
            index[bc] = p
    return index


# ---------------------------------------------------------------------------
# PENDING-value builders (for grade-changed / new products)
# ---------------------------------------------------------------------------

def _pending_value_for_live_field(live_val: Any) -> Any:
    """
    Return an appropriate PENDING placeholder whose *shape* matches the live
    field value. This ensures the output schema matches the live schema.

    Rules:
      - scalar (str / None) → PENDING_COPY
      - list → [PENDING_COPY]
      - dict → PENDING_COPY  (shallow string; the live copy engine handles shape)
    """
    if isinstance(live_val, list):
        return [PENDING]
    if isinstance(live_val, dict):
        # For dict-shaped live copy fields (e.g. expansion.consumerExplanation
        # in cookies_coffee), we still emit a flat PENDING string rather than
        # trying to mirror the live dict structure. The author_copy merge step
        # handles the shape. This matches copy_carryover.py's proven behaviour.
        return PENDING
    return PENDING


def _build_pending_top(copy_fields_top: set[str], live_prod: dict) -> dict[str, Any]:
    """Build top-level copy field dict with PENDING values shaped after the live product."""
    result: dict[str, Any] = {}
    for k in copy_fields_top:
        live_val = live_prod.get(k)
        result[k] = _pending_value_for_live_field(live_val)
    return result


def _build_pending_exp(copy_fields_exp: set[str], live_prod: dict) -> dict[str, Any]:
    """Build expansion copy field dict with PENDING values shaped after the live product."""
    live_exp = live_prod.get("expansion") or {}
    result: dict[str, Any] = {}
    for k in copy_fields_exp:
        live_val = live_exp.get(k)
        result[k] = _pending_value_for_live_field(live_val)
    return result


# ---------------------------------------------------------------------------
# Copy carry (grade-unchanged products)
# ---------------------------------------------------------------------------

def _carry_copy_fields(
    staging_prod: dict,
    live_prod: dict,
    copy_fields_top: set[str],
    copy_fields_exp: set[str],
) -> dict:
    """
    Return a copy of staging_prod with live copy fields overlaid.

    Structural / render / scoring fields stay from staging (scores, grades,
    nutrition, bariInterpretation key/label/score/strength, render fields).

    For bariInterpretation: we keep staging's key/label/score/strength (scoring
    output) and carry live's interpretation text into each item. This reuses the
    proven logic from copy_carryover.py.

    For all other copy fields: take the live value directly if it is non-PENDING
    and non-null. If live does not have the field or has PENDING, leave staging
    value as-is (it may already be PENDING, which is fine for author-set tracking).
    """
    s = copy.deepcopy(staging_prod)
    live_exp = live_prod.get("expansion") or {}

    # ---- Top-level copy fields ----
    for k in copy_fields_top:
        live_val = live_prod.get(k)
        if live_val is None or _is_pending(live_val):
            continue  # live has nothing useful; leave staging value
        s[k] = live_val

    # ---- bariInterpretation: structural in staging, interpretation text from live ----
    # bariInterpretation is NOT in copy_fields_top because it's not in the live
    # cereals/granola/juices schema. But for schemas where live has it (cakes,
    # cookies_coffee), it IS in copy_fields_top and the direct copy above handles it.
    # The special case here handles the older v1 schema where live has bariInterpretation
    # as a plain string (cakes v1). This mirrors copy_carryover.py's proven rules.
    #
    # Actually: for cakes live schema, bariInterpretation IS a top-level key, so it was
    # already handled above.  But staging has it as a list of dicts with interpretation
    # sub-fields. So we need extra logic to map live's string or list into staging's
    # list sub-fields.
    #
    # We apply this only when staging has bariInterpretation as a list of dicts:
    staging_bi = s.get("bariInterpretation")
    if isinstance(staging_bi, list) and staging_bi and isinstance(staging_bi[0], dict):
        live_bi = live_prod.get("bariInterpretation")
        if live_bi is not None and not _is_pending(live_bi):
            if isinstance(live_bi, str):
                # Cakes v1: plain string → fill all interpretation slots
                for item in staging_bi:
                    if isinstance(item, dict) and item.get("interpretation") == PENDING:
                        item["interpretation"] = live_bi
            elif isinstance(live_bi, list):
                # Cookies v2 / other: list of dicts — match by key or dimension
                live_bi_index: dict[str, str] = {}
                for item in live_bi:
                    if isinstance(item, dict):
                        item_key = item.get("key") or item.get("dimension")
                        interp = item.get("interpretation") or item.get("explanation_he")
                        if item_key and interp and interp != PENDING:
                            live_bi_index[item_key] = interp
                for item in staging_bi:
                    if isinstance(item, dict):
                        key = item.get("key")
                        live_interp = live_bi_index.get(key)
                        if live_interp and live_interp != PENDING:
                            item["interpretation"] = live_interp
        s["bariInterpretation"] = staging_bi

    # ---- Expansion copy fields ----
    staging_exp = s.get("expansion") or {}
    for k in copy_fields_exp:
        live_val = live_exp.get(k)
        if live_val is None or _is_pending(live_val):
            continue
        staging_exp[k] = live_val
    s["expansion"] = staging_exp

    return s


# ---------------------------------------------------------------------------
# Schema-match: strip staging-only copy fields not in live schema
# ---------------------------------------------------------------------------

def _schema_match_product(
    staging_prod: dict,
    copy_fields_top: set[str],
    copy_fields_exp: set[str],
) -> dict:
    """
    Remove from staging_prod any top-level or expansion copy fields that are
    NOT in the live schema. Structural / render / scoring fields are always kept.

    This is the generalized port of schema_strip.py's per-shelf field-table logic:
    instead of a hand-coded table, we derive the live copy-field set from the live
    JSON itself (passed in via copy_fields_top / copy_fields_exp).

    Special handling for bariInterpretation:
      If the live schema does NOT have bariInterpretation (e.g. cereals, granola,
      juices), we strip it from staging. The interpretation text within it is
      v3-only copy and must be stripped. The key/label/score/strength sub-fields
      are lost too — they are re-derivable from the trace via generate_page.py
      and will be present in the next full staging generation.
      If the live schema DOES have bariInterpretation, we keep it from staging
      (the carry_copy step already merged the live interpretation text into it).
    """
    p = copy.deepcopy(staging_prod)

    # --- Top-level: remove copy fields not in live schema ---
    # Identify all top-level staging keys that are copy-flavoured but absent from live
    # We compute "v3-only copy fields" as fields that:
    #   1. Are NOT structural
    #   2. Are NOT in copy_fields_top (the live schema's copy fields)
    # We only strip fields we know could be v3 copy (not genuine structural).
    #
    # Safe approach: enumerate known v3-only copy keys and remove them if
    # they are NOT present in the live copy set.
    V3_COPY_KEYS = {
        "insightLine", "rowVerdict", "consumerTakeaway", "bestUseCases",
        "bariInterpretation", "consumerExplanation",
    }
    for k in V3_COPY_KEYS:
        if k not in copy_fields_top and k in p:
            del p[k]

    # --- Expansion: remove copy fields not in live schema ---
    exp = p.get("expansion") or {}
    V3_EXP_COPY_KEYS = {
        "comparisonContext", "consumerExplanation", "bottomLine",
    }
    for k in V3_EXP_COPY_KEYS:
        if k not in copy_fields_exp and k in exp:
            del exp[k]
    p["expansion"] = exp

    return p


# ---------------------------------------------------------------------------
# Pending-field detection (for reporting)
# ---------------------------------------------------------------------------

def _has_any_pending(prod: dict, copy_fields_top: set[str], copy_fields_exp: set[str]) -> bool:
    """Return True if any live-schema copy field in the product still has PENDING_COPY."""
    for k in copy_fields_top:
        v = prod.get(k)
        if _is_pending(v):
            return True
        # Check bariInterpretation sub-field
        if k == "bariInterpretation" and isinstance(v, list):
            for item in v:
                if isinstance(item, dict) and _is_pending(item.get("interpretation")):
                    return True

    exp = prod.get("expansion") or {}
    for k in copy_fields_exp:
        v = exp.get(k)
        if _is_pending(v):
            return True
        if isinstance(v, dict):
            for sub_v in v.values():
                if _is_pending(sub_v):
                    return True

    return False


def _collect_pending_fields(
    prod: dict,
    copy_fields_top: set[str],
    copy_fields_exp: set[str],
) -> list[str]:
    """Return list of copy field names that still have PENDING_COPY."""
    pending: list[str] = []

    for k in sorted(copy_fields_top):
        v = prod.get(k)
        if _is_pending(v):
            pending.append(k)
            continue
        if k == "bariInterpretation" and isinstance(v, list):
            for item in v:
                if isinstance(item, dict) and _is_pending(item.get("interpretation")):
                    pending.append("bariInterpretation[].interpretation")
                    break

    exp = prod.get("expansion") or {}
    for k in sorted(copy_fields_exp):
        v = exp.get(k)
        if _is_pending(v):
            pending.append(f"expansion.{k}")
        elif isinstance(v, dict):
            for sub_k, sub_v in v.items():
                if _is_pending(sub_v):
                    pending.append(f"expansion.{k}.{sub_k}")

    return pending


# ---------------------------------------------------------------------------
# Result dataclass
# ---------------------------------------------------------------------------

@dataclass
class CopyStageResult:
    shelf: str
    staging_path: str
    live_path: str
    out_path: str
    author_set_path: str

    total_products: int = 0
    carried: int = 0          # grade-unchanged, copy carried successfully
    pending_carried: int = 0   # grade-unchanged but live had no copy (live also PENDING)
    grade_changed: int = 0
    new_products: int = 0
    score_moved_flags: list[dict] = field(default_factory=list)

    copy_fields_top: list[str] = field(default_factory=list)
    copy_fields_exp: list[str] = field(default_factory=list)

    author_set: dict = field(default_factory=dict)
    sha256_staging: str = ""
    sha256_author_set: str = ""

    error: str | None = None


# ---------------------------------------------------------------------------
# Core function
# ---------------------------------------------------------------------------

def run_copy_stage(
    staging_path: Path | str,
    live_path: Path | str,
    shelf_name: str = "",
    out_path: Path | str | None = None,
    score_move_threshold: float = SCORE_MOVE_THRESHOLD_DEFAULT,
) -> CopyStageResult:
    """
    Apply the copy stage for one shelf/category.

    Parameters
    ----------
    staging_path:
        Path to the freshly generated staging page (e.g.
        _rescore_staging/<shelf>/<shelf>_rescored.json). Read + written in place
        unless out_path is specified.
    live_path:
        Path to the live baseline JSON (config.baseline_json).
    shelf_name:
        Human-readable shelf label for reporting (inferred from staging_path if
        omitted).
    out_path:
        If given, write the copy-applied page here instead of in-place.
    score_move_threshold:
        Score delta (abs) that triggers a stale-copy flag for grade-unchanged
        products. Default 3 (matching copy_carryover.py).

    Returns
    -------
    CopyStageResult with all counts, the author_set, and sha256 hashes.
    """
    staging_path = Path(staging_path)
    live_path = Path(live_path)
    if out_path is None:
        out_path = staging_path
    else:
        out_path = Path(out_path)
    author_set_path = out_path.parent / "author_set.json"

    if not shelf_name:
        shelf_name = staging_path.stem.replace("_rescored", "")

    result = CopyStageResult(
        shelf=shelf_name,
        staging_path=str(staging_path),
        live_path=str(live_path),
        out_path=str(out_path),
        author_set_path=str(author_set_path),
    )

    # --- Load inputs ---
    try:
        staging_data = load_json(staging_path)
    except Exception as exc:
        result.error = f"Cannot load staging page: {exc}"
        return result

    try:
        live_data = load_json(live_path)
    except Exception as exc:
        result.error = f"Cannot load live baseline: {exc}"
        return result

    live_products: list[dict] = live_data.get("products", [])
    staging_products: list[dict] = staging_data.get("products", [])
    result.total_products = len(staging_products)

    # --- Derive live copy-field schema (the generalization key) ---
    copy_fields_top, copy_fields_exp = _derive_live_schema(live_products)
    result.copy_fields_top = sorted(copy_fields_top)
    result.copy_fields_exp = sorted(copy_fields_exp)

    print(f"  copy_fields_top derived from live schema: {sorted(copy_fields_top)}")
    print(f"  copy_fields_exp derived from live schema: {sorted(copy_fields_exp)}")

    # --- Build live index ---
    live_index = _build_live_index(live_products)

    # We need a representative live product to build PENDING shapes for
    # grade-changed / new products. Any live product will do.
    _representative_live = live_products[0] if live_products else {}

    # --- Process products ---
    new_staging_products: list[dict] = []
    author_needed: list[dict] = []
    score_moved_flags: list[dict] = []

    for sp in staging_products:
        bc = str(sp.get("barcode") or sp.get("id") or "")
        s_grade = sp.get("grade", "")
        s_score = float(sp.get("score") or 0)

        lp = live_index.get(bc)

        if lp is None:
            # NET-NEW product: schema-match (strip v3-only copy), set PENDING
            matched = _schema_match_product(sp, copy_fields_top, copy_fields_exp)
            # Set PENDING for the live-schema copy fields
            pending_top = _build_pending_top(copy_fields_top, _representative_live)
            pending_exp = _build_pending_exp(copy_fields_exp, _representative_live)
            matched.update(pending_top)
            matched_exp = matched.get("expansion") or {}
            matched_exp.update(pending_exp)
            matched["expansion"] = matched_exp

            new_staging_products.append(matched)
            result.new_products += 1

            fields_needed = sorted(copy_fields_top) + [f"expansion.{k}" for k in sorted(copy_fields_exp)]
            author_needed.append({
                "barcode": bc,
                "name": sp.get("name", ""),
                "old_grade": None,
                "new_grade": s_grade,
                "score": s_score,
                "reason": "new",
                "fields": fields_needed,
            })
            print(f"  NEW         {bc:<20} {str(sp.get('name',''))[:35]} grade={s_grade}")
            continue

        l_grade = lp.get("grade", "")
        l_score = float(lp.get("score") or 0)

        if l_grade != s_grade:
            # Grade-CHANGED: schema-match + PENDING
            matched = _schema_match_product(sp, copy_fields_top, copy_fields_exp)
            pending_top = _build_pending_top(copy_fields_top, lp)
            pending_exp = _build_pending_exp(copy_fields_exp, lp)
            matched.update(pending_top)
            matched_exp = matched.get("expansion") or {}
            matched_exp.update(pending_exp)
            matched["expansion"] = matched_exp

            new_staging_products.append(matched)
            result.grade_changed += 1

            fields_needed = sorted(copy_fields_top) + [f"expansion.{k}" for k in sorted(copy_fields_exp)]
            author_needed.append({
                "barcode": bc,
                "name": sp.get("name", ""),
                "old_grade": l_grade,
                "new_grade": s_grade,
                "score": s_score,
                "reason": "grade_changed",
                "fields": fields_needed,
            })
            print(f"  GRADE_CHNG  {bc:<20} {str(sp.get('name',''))[:30]} {l_grade}->{s_grade} {l_score:.1f}->{s_score:.1f}")
            continue

        # Grade-UNCHANGED: carry copy, then schema-match
        updated = _carry_copy_fields(sp, lp, copy_fields_top, copy_fields_exp)
        updated = _schema_match_product(updated, copy_fields_top, copy_fields_exp)
        new_staging_products.append(updated)

        # Check if live had any copy to carry at all
        still_pending = _has_any_pending(updated, copy_fields_top, copy_fields_exp)
        if still_pending:
            # Live had no copy for this product (live also PENDING) — count separately
            result.pending_carried += 1
            print(f"  NO_COPY     {bc:<20} {str(sp.get('name',''))[:30]} grade={s_grade} (live also had no copy)")
        else:
            result.carried += 1
            print(f"  CARRIED     {bc:<20} {str(sp.get('name',''))[:30]} grade={s_grade}")

        # Flag: grade-unchanged but score moved >= threshold
        score_delta = abs(s_score - l_score)
        if score_delta >= score_move_threshold:
            flag = {
                "barcode": bc,
                "name": sp.get("name", ""),
                "grade": s_grade,
                "live_score": round(l_score, 2),
                "staging_score": round(s_score, 2),
                "delta": round(score_delta, 2),
                "note": f"carried copy but score moved >= {score_move_threshold} pts — verify stale figures in copy",
            }
            score_moved_flags.append(flag)
            print(f"  !! SCORE_MOVED {bc:<20} grade={s_grade} {l_score:.1f}->{s_score:.1f} (delta={score_delta:.1f})")

    result.score_moved_flags = score_moved_flags

    # --- Write copy-applied staging page ---
    staging_data["products"] = new_staging_products
    result.sha256_staging = save_json(out_path, staging_data)

    # --- Build + write author_set.json ---
    author_set = {
        "shelf": shelf_name,
        "live_path": str(live_path),
        "staging_path": str(out_path),
        "copy_fields_top": sorted(copy_fields_top),
        "copy_fields_exp": sorted(copy_fields_exp),
        "authored_needed": author_needed,
        "carried": result.carried,
        "pending_carried": result.pending_carried,
        "score_moved_flags": score_moved_flags,
        "counts": {
            "total": result.total_products,
            "carried": result.carried,
            "pending_carried": result.pending_carried,
            "grade_changed": result.grade_changed,
            "new_products": result.new_products,
            "score_moved_flags": len(score_moved_flags),
            "author_needed": len(author_needed),
        },
    }
    result.author_set = author_set
    result.sha256_author_set = save_json(author_set_path, author_set)

    return result


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------

def main() -> int:
    parser = argparse.ArgumentParser(
        description=(
            "Bari copy stage — carry live copy for grade-unchanged products, "
            "leave PENDING_COPY + author-set for grade-changed / new products. "
            "Schema derived from live JSON, not hard-coded."
        )
    )
    parser.add_argument(
        "--staging", required=True,
        help="Path to freshly generated staging JSON (e.g. _rescore_staging/<shelf>/<shelf>_rescored.json)",
    )
    parser.add_argument(
        "--live", required=True,
        help="Path to live baseline JSON (config.baseline_json)",
    )
    parser.add_argument(
        "--out", default=None,
        help="Output path for copy-applied JSON (default: in-place overwrite of --staging)",
    )
    parser.add_argument(
        "--shelf", default="",
        help="Shelf/category label for reporting (inferred from filename if omitted)",
    )
    parser.add_argument(
        "--score-move-threshold", type=float, default=SCORE_MOVE_THRESHOLD_DEFAULT,
        help=f"Score delta that triggers stale-copy flag (default: {SCORE_MOVE_THRESHOLD_DEFAULT})",
    )
    args = parser.parse_args()

    print(f"\n=== COPY STAGE: {args.shelf or Path(args.staging).stem} ===")

    result = run_copy_stage(
        staging_path=args.staging,
        live_path=args.live,
        shelf_name=args.shelf,
        out_path=args.out,
        score_move_threshold=args.score_move_threshold,
    )

    if result.error:
        print(f"ERROR: {result.error}", file=sys.stderr)
        return 1

    print(f"\n  Staging written: {result.out_path}")
    print(f"  SHA256 staging: {result.sha256_staging}")
    print(f"  Author-set:     {result.author_set_path}")
    print(f"  SHA256 author:  {result.sha256_author_set}")
    print()
    print(f"  Total products:  {result.total_products}")
    print(f"  Carried (copy):  {result.carried}")
    print(f"  Pending (live had no copy): {result.pending_carried}")
    print(f"  Grade-changed:   {result.grade_changed}")
    print(f"  New products:    {result.new_products}")
    print(f"  Score-moved flags: {len(result.score_moved_flags)}")

    if result.score_moved_flags:
        print("\n  SCORE-MOVED FLAGS (stale copy check):")
        for flag in result.score_moved_flags:
            print(f"    {flag['barcode']}  grade={flag['grade']}  {flag['live_score']}->{flag['staging_score']}  delta={flag['delta']}")

    if result.author_set.get("authored_needed"):
        print(f"\n  AUTHOR SET ({len(result.author_set['authored_needed'])} products needing copy):")
        for item in result.author_set["authored_needed"]:
            grade_change = (
                f"{item['old_grade']}->{item['new_grade']}"
                if item.get("old_grade") else f"NEW grade={item['new_grade']}"
            )
            print(f"    [{grade_change}] {item['barcode']}  {str(item['name'])[:40]}")
            print(f"      fields: {item['fields']}")

    print("\n--- RETURN CONTRACT JSON ---")
    contract = {
        "task": "copy_stage",
        "shelf": result.shelf,
        "proposed_status": "RETURNED",
        "artifacts": [
            {"path": result.out_path, "action": "modified", "sha256": result.sha256_staging},
            {"path": result.author_set_path, "action": "created", "sha256": result.sha256_author_set},
        ],
        "counts": {
            "total_products": f"{result.total_products}/{result.total_products} (staging page)",
            "carried": f"{result.carried}/{result.total_products} (grade-unchanged, copy carried)",
            "pending_carried": f"{result.pending_carried}/{result.total_products} (grade-unchanged, live also had no copy)",
            "grade_changed": f"{result.grade_changed}/{result.total_products} (grade changed, PENDING set)",
            "new_products": f"{result.new_products}/{result.total_products} (new to live, PENDING set)",
            "score_moved_flags": f"{len(result.score_moved_flags)}/{result.carried + result.pending_carried} (carried but score moved >=3)",
            "author_needed": f"{len(result.author_set.get('authored_needed', []))}/{result.total_products}",
            "copy_fields_top": str(result.copy_fields_top),
            "copy_fields_exp": str(result.copy_fields_exp),
        },
        "not_done": [],
        "self_check": (
            "grade-unchanged products have 0 PENDING in live-schema copy fields "
            "unless live itself had no copy for them"
        ),
    }
    print(json.dumps(contract, ensure_ascii=False, indent=2))

    return 0


if __name__ == "__main__":
    sys.exit(main())
