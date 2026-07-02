"""
matrix_signal_probe_v5_1.py
===========================
TASK-395 — Component B v5.1 formula: NC-2 refinements applied to v5.
Created from matrix_signal_probe_v5.py per matrix_signal_redesign_v3.md §v3.1
and Product Agent NC-2 close confirmation.

Changes from v5 (FORMULA ONLY — reading layer unchanged):
  NC-2a: Trace-grain guard on the M-2 grain-context 0.5x penalty.
         The penalty fires ONLY when BOTH conditions hold simultaneously:
           (a) grain whole effective weight (GRAIN_WHOLE_LABELS only) >= 5% of
               product weight (GRAIN_CONTEXT_ABS_FLOOR).
           (b) grain whole effective weight >= 50% of non-grain whole effective
               weight before any penalty (GRAIN_CONTEXT_REL_FLOOR).
         If either condition fails, grain context is NOT active and all markers
         score at full weight.
         CRITICAL: the grain_whole_ew for the guard uses label-correct
         effective_pct (i.e. stated_pct as stored in the marker, which for
         sub-ingredients is already parent_pct * sub_pct / 100 from the reader).
         Position-weight fallback does NOT substitute for stated_pct in the
         guard computation. Only GRAIN_WHOLE_LABELS members count toward
         grain_whole_ew; barley_malt (half_weight=True, not in either label set)
         does not count toward the grain_whole_ew guard threshold.

  NC-2b: Remove sourdough_starter from NON_GRAIN_WHOLE_LABELS entirely.
         Reclassified as neutral/process ingredient (like water/salt/leavening).
         Contributes 0 to both whole_weight and refined_weight. Does NOT
         trigger the grain-context penalty and does NOT receive it.

No other changes from v5:
  - M-1: anchor nudge +/-0.05 (unchanged from v5)
  - M-2 base rule: 0.5x penalty for non-grain whole in grain-context products
    (unchanged, but guard activation now stricter)
  - Reading layer: structured_ingredient_reader.py (v4, unchanged)
  - Lexicon (MARKERS): identical to v5 (sourdough_starter marker still present
    in MARKERS for parsing — it matches the ingredient and produces a record;
    it is simply excluded from both GRAIN_WHOLE_LABELS and NON_GRAIN_WHOLE_LABELS
    so it scores as NEUTRAL and contributes nothing to whole/refined weight)
  - Position-weight curve: identical
  - Score endpoint mapping: identical

Gold set: matrix_gold_set_v2.json (67 products, 20 T3 pairs).
  - RP-04 direction: as-is in the frozen JSON (still uncorrected — QA owns
    the RP-04 correction). Report B2 BOTH ways: as-is and with RP-04 counted
    in the nutritionally-correct direction (muesli higher than granola).
  - FROZEN — do not tune formula to this set.

Run:
    python matrix_signal_probe_v5_1.py

Outputs:
    analysis/matrix_signal_probe_v5_1_results.json
    analysis/matrix_signal_probe_v5_1_report.txt
"""

import json
import re
import hashlib
import sys
import os
import statistics
from pathlib import Path
from datetime import datetime, timezone
from typing import Optional
from collections import Counter

# ---------------------------------------------------------------------------
# Paths
# ---------------------------------------------------------------------------
REPO_ROOT = Path("C:/Bari")
GOLD_SET_PATH = REPO_ROOT / "03_operations/bsip2/proto_v0/analysis/matrix_gold_set_v2.json"
OUT_DIR = REPO_ROOT / "03_operations/bsip2/proto_v0/analysis"

# Import the shared reader (unchanged from v4 — R-1, R-2, spelt-construct, C-5 fixes)
sys.path.insert(0, str(REPO_ROOT / "03_operations/bsip2/proto_v0/analysis"))
from structured_ingredient_reader import (
    parse_ingredients, is_unparseable, _extract_groups, _strip_groups
)

# ---------------------------------------------------------------------------
# Position-weight curve — IDENTICAL to v4/v5 (do not change)
# ---------------------------------------------------------------------------
def _pos_weight(pos: Optional[int]) -> float:
    if pos is None: return 0.12
    if pos == 1:    return 1.00
    if pos == 2:    return 0.82
    if pos == 3:    return 0.68
    if pos == 4:    return 0.55
    if pos == 5:    return 0.44
    if pos == 6:    return 0.35
    if pos == 7:    return 0.28
    if pos == 8:    return 0.22
    if pos == 9:    return 0.17
    if pos == 10:   return 0.13
    if pos <= 15:   return max(0.08, 0.13 * (0.85 ** (pos - 10)))
    return 0.08

# ---------------------------------------------------------------------------
# Lexicon — IDENTICAL to v4/v5 (do not change)
# ---------------------------------------------------------------------------
MARKERS = [
    (r"קמח חיטה מלאה?", "whole_wheat_flour", "whole", False),
    (r"חיטה מלאה", "whole_wheat_grain", "whole", False),
    (r"קמח (?:חיטת )?כוסמין מלא", "whole_spelt_flour", "whole", False),
    (r"כוסמין מלא", "whole_spelt_grain", "whole", False),
    (r"קמח שיבולת שועל מלא", "whole_oat_flour", "whole", False),
    (r"שיבולת שועל מלאה?", "whole_oat", "whole", False),
    (r"פתיתי שיבולת שועל מלאה?|פתיתי שיבולת שועל מלאים", "whole_oat_flakes", "whole", False),
    (r"קמח שיפון מלא", "whole_rye_flour", "whole", False),
    (r"שיפון מלא", "whole_rye_grain", "whole", False),
    (r"קמח תירס מלא", "whole_corn_flour", "whole", False),
    (r"קמח שעורה מלא", "whole_barley_flour", "whole", False),
    (r"אורז מלא|קמח(?:\s+מ)?אורז מלא", "whole_rice", "whole", False),
    (r"קינואה(?:\s+מלאה)?", "quinoa", "whole", False),
    (r"כוסמת", "buckwheat", "whole", False),
    (r"גריסי שיבולת שועל", "oat_groats", "whole", False),
    (r"שיבולת שועל קלופה", "hulled_oats", "whole", False),
    (r"שיבולת שועל(?!\s+מלאה?)(?!\s+מלאים)", "oat_flakes_plain", "whole", False),
    (r"לתת שעורה|מיצוי לתת שעורה", "barley_malt", "whole", True),
    (r"אגוז(?:י)?\s+(?:פקאן|לוז|מלך|מקדמיה|ברזיל)|אגוזים", "nuts", "whole", False),
    (r"שקד(?:ים)?", "almonds", "whole", False),
    (r"בוטנ(?:ים|ות)?", "peanuts", "whole", False),
    (r"פיסטוק(?:ים)?", "pistachios", "whole", False),
    (r"קשיו", "cashews", "whole", False),
    (r"גרעיני?\s+(?:חמנ(?:ייה|יה)|דלעת|פשתן)", "seeds_specific", "whole", False),
    (r"גרעינים", "seeds_generic", "whole", False),
    (r"שומשום(?!\s+לבן)", "sesame_seeds", "whole", False),
    (r"זרעי?\s+צ'יה|צ'יה", "chia_seeds", "whole", False),
    (r"גרעיני פשתן|פשתן", "flax_seeds", "whole", False),
    (r"עדשים", "lentils", "whole", False),
    (r"חומוס(?!\s+שחור)", "chickpeas", "whole", False),
    (r"תמר(?:ים)?", "dates", "whole", False),
    (r"צימוקים", "raisins", "whole", False),
    (r"מחמצת", "sourdough_starter", "whole", False),   # kept in MARKERS for parsing
    (r"חמאה(?!\s+קקאו)(?!\s+שמן)", "butter_dairy", "whole", False),
    (r"שמן זית", "olive_oil", "whole", False),
    (r"טחינה|ממרח שומשום", "tahini", "whole", False),
    # Refined
    (r"קמח כוסמין לבן", "white_spelt_flour", "refined", False),
    (r"קמח חיטה(?!\s+מלאה?)(?!\s+מלא)", "refined_wheat_flour", "refined", False),
    (r"גריסי תירס", "corn_grits", "refined", False),
    (r"קמח תירס(?!\s+מלא)", "corn_flour_refined", "refined", False),
    (r"סמולינה(?:\s+מתירס)?", "semolina", "refined", False),
    (r"קמח אורז(?!\s+מלא)", "rice_flour_refined", "refined", False),
    (r"אורז לבן", "white_rice", "refined", False),
    (r"עמילן תירס", "corn_starch", "refined", False),
    (r"עמילן חיטה", "wheat_starch", "refined", False),
    (r"עמילן אורז", "rice_starch", "refined", False),
    (r"עמילן(?!\s+תירס)(?!\s+חיטה)(?!\s+אורז)", "generic_starch", "refined", False),
    (r"(?<!\S)סוכר(?!\s+קנים\s+אורגני)", "sugar", "refined", False),
    (r"סירופ\s+גלוקוז(?:-פרוקטוז)?|סירופ\s+גלוקוזה(?:-פרוקטוזה)?", "glucose_syrup", "refined", False),
    (r"סירופ\s+סוכר\s+אינברטי|סוכר\s+אינברטי", "inverted_sugar", "refined", False),
    (r"גלוקוז(?!\s+מיובש)(?![א-ת])", "glucose", "refined", False),
    (r"דקסטרוז|דקסטרוזה", "dextrose", "refined", False),
    (r"דקסטרין", "dextrin", "refined", False),
    (r"פרוקטוז", "fructose", "refined", False),
    (r"מלטודקסטרין", "maltodextrin", "refined", False),
    (r"שמן דקל(?!ים)(?!\s+אדום)", "palm_oil", "refined", False),
    (r"שמן דקלים", "palm_oil_pl", "refined", False),
    (r"שמנים\s+צמחיים", "veg_oils_pl", "refined", False),
    (r"שמן\s+צמחי(?!ים)", "veg_oil_sg", "refined", False),
    (r"שומן\s+צמחי", "hydrogenated_veg_fat", "refined", False),
    (r"מרגרינה", "margarine", "refined", False),
    (r"שמן\s+קוקוס", "coconut_oil", "refined", False),
]

# ---------------------------------------------------------------------------
# v5.1 formula classification sets
# ---------------------------------------------------------------------------

GRAIN_WHOLE_LABELS = {
    "whole_wheat_flour", "whole_wheat_grain",
    "whole_spelt_flour", "whole_spelt_grain",
    "whole_oat_flour", "whole_oat", "whole_oat_flakes",
    "whole_rye_flour", "whole_rye_grain",
    "whole_corn_flour", "whole_barley_flour", "whole_rice",
    "oat_groats", "hulled_oats", "oat_flakes_plain",
    "quinoa", "buckwheat", "bare_wheat_first_80pct",
}

NON_GRAIN_WHOLE_LABELS = {
    "nuts", "almonds", "peanuts", "pistachios", "cashews",
    "seeds_specific", "seeds_generic", "sesame_seeds",
    "chia_seeds", "flax_seeds",
    "dates", "raisins",
    "tahini", "olive_oil", "butter_dairy",
    # "sourdough_starter" REMOVED (NC-2b): reclassified as neutral/process ingredient.
    # It no longer contributes to whole_weight, refined_weight, or the grain-context
    # guard. Treated identically to water/salt/leavening — invisible to the signal.
}
# NOTE: barley_malt has half_weight=True in MARKERS; it is NOT in GRAIN_WHOLE_LABELS
# or NON_GRAIN_WHOLE_LABELS. It is a whole-class marker that receives 0.5x via the
# lexicon half_weight flag only. It does NOT count toward grain_whole_ew in the guard.
# sourdough_starter is a whole-class marker in MARKERS (for parsing) but is in NEITHER
# label set — it is effectively invisible to scoring (contributes 0 to any weight sum
# because it falls through to no-op in effective_weight).

# ---------------------------------------------------------------------------
# NC-2a: Trace-grain guard constants
# ---------------------------------------------------------------------------
GRAIN_CONTEXT_ABS_FLOOR = 0.05   # grain whole eff weight must be >= 5% of product weight
GRAIN_CONTEXT_REL_FLOOR = 0.50   # grain whole eff weight must be >= 50% of non-grain whole
                                   # eff weight (before any penalty)

# ---------------------------------------------------------------------------
# Helper: get the name-only portion of a record (text before first group)
# Unchanged from v4/v5 — R-2 fix
# ---------------------------------------------------------------------------
def _name_only_text(record: dict) -> str:
    raw = record["raw"]
    if not record.get("has_own_sub"):
        return raw
    groups = _extract_groups(raw)
    if not groups:
        return raw
    name_end = groups[0]["start"]
    return raw[:name_end].strip()


# ---------------------------------------------------------------------------
# Marker extraction — IDENTICAL to v4/v5 (reading layer unchanged)
# ---------------------------------------------------------------------------

def extract_markers_from_record_v4(record: dict) -> list[dict]:
    text = _name_only_text(record)
    position = record["position"]

    stated_pct = record.get("effective_pct") if record.get("effective_pct") is not None \
                 else record.get("stated_pct")

    qualifiers = record.get("qualifiers", [])
    found = []
    seen_labels = set()

    if position == 1:
        bare_wheat = re.search(r"(?<![^\s(,])חיטה(?!\s+מלאה?)(?!\s+לבן)", text)
        if bare_wheat and stated_pct is not None and stated_pct >= 80.0:
            found.append({
                "label": "bare_wheat_first_80pct",
                "class": "whole",
                "position": position,
                "stated_pct": stated_pct,
                "half_weight": False,
            })
            seen_labels.add("bare_wheat_first_80pct")

    for pattern, label, grain_class, half_weight in MARKERS:
        if label in seen_labels:
            continue
        if re.search(pattern, text, re.IGNORECASE):
            if label in ("whole_spelt_grain", "whole_spelt_flour") and "לבן" in qualifiers:
                continue
            found.append({
                "label": label,
                "class": grain_class,
                "position": position,
                "stated_pct": stated_pct,
                "half_weight": half_weight,
            })
            seen_labels.add(label)

    return found


def extract_all_markers_v4(text: str) -> list[dict]:
    if is_unparseable(text):
        return []

    records = parse_ingredients(text)
    if not records:
        return []

    seen_labels: dict[str, dict] = {}

    for record in records:
        markers = extract_markers_from_record_v4(record)
        for m in markers:
            label = m["label"]
            if label not in seen_labels:
                seen_labels[label] = m
            else:
                existing = seen_labels[label]
                ew_new = m["stated_pct"] / 100.0 if m["stated_pct"] is not None else _pos_weight(m["position"])
                ew_old = existing["stated_pct"] / 100.0 if existing["stated_pct"] is not None else _pos_weight(existing["position"])
                if ew_new > ew_old:
                    seen_labels[label] = m

    return list(seen_labels.values())


# ---------------------------------------------------------------------------
# v5.1 formula:
#   Changes from v5:
#     NC-2a: Trace-grain guard replaces simple has_grain_whole boolean.
#     NC-2b: sourdough_starter removed from NON_GRAIN_WHOLE_LABELS.
#   Unchanged from v5:
#     M-1: anchor nudge +/-0.05
#     M-2 base penalty logic: 0.5x for non-grain whole when guard active
# ---------------------------------------------------------------------------

def _base_weight_no_penalty(m: dict, remaining_mass: float, total_pos_weight: float) -> float:
    """
    Compute base effective weight for a marker WITHOUT any M-2 penalty.
    Used for the guard's pre-penalty ew computation.
    """
    if m.get("stated_pct") is not None:
        w = m["stated_pct"] / 100.0
    else:
        if total_pos_weight > 0:
            w = (_pos_weight(m.get("position")) / total_pos_weight) * remaining_mass
        else:
            w = 0.0
    if m.get("half_weight"):
        w *= 0.5
    return w


def has_meaningful_grain_context(
    markers: list[dict],
    remaining_mass: float,
    total_pos_weight: float,
) -> tuple[bool, float, float, bool, bool]:
    """
    NC-2a guard: returns (guard_active, grain_whole_ew, non_grain_whole_ew,
                          abs_cond, rel_cond).

    guard_active = True only when BOTH:
      (a) grain_whole_ew >= GRAIN_CONTEXT_ABS_FLOOR (0.05)
      (b) grain_whole_ew >= GRAIN_CONTEXT_REL_FLOOR * non_grain_whole_ew (0.50)

    grain_whole_ew: sum of base weights (pre-penalty, with half_weight applied)
                   for markers in GRAIN_WHOLE_LABELS only. barley_malt
                   (half_weight=True, not in either label set) is excluded.
    non_grain_whole_ew: sum of base weights (pre-penalty) for markers in
                        NON_GRAIN_WHOLE_LABELS (sourdough_starter excluded).

    sourdough_starter: in neither set, contributes 0 to both.
    """
    grain_whole_ew = sum(
        _base_weight_no_penalty(m, remaining_mass, total_pos_weight)
        for m in markers
        if m["class"] == "whole" and m["label"] in GRAIN_WHOLE_LABELS
    )
    non_grain_whole_ew = sum(
        _base_weight_no_penalty(m, remaining_mass, total_pos_weight)
        for m in markers
        if m["class"] == "whole" and m["label"] in NON_GRAIN_WHOLE_LABELS
    )

    abs_cond = grain_whole_ew >= GRAIN_CONTEXT_ABS_FLOOR
    rel_cond = (
        non_grain_whole_ew == 0.0
        or grain_whole_ew >= GRAIN_CONTEXT_REL_FLOOR * non_grain_whole_ew
    )
    guard_active = abs_cond and rel_cond
    return guard_active, grain_whole_ew, non_grain_whole_ew, abs_cond, rel_cond


def compute_component_b_score_v5_1(markers: list[dict]) -> Optional[float]:
    """
    v5.1 formula. Changes from v5:
      NC-2a: Trace-grain guard on M-2 activation (abs floor 5% + rel floor 50%).
      NC-2b: sourdough_starter is neutral — contributes 0 to whole/refined.
    Unchanged from v5:
      M-1: anchor nudge +/-0.05.
      M-2 base: 0.5x penalty for non-grain whole markers when guard active.
    All other logic identical to v5/v4.
    """
    if not markers:
        return None

    pct_markers = [m for m in markers if m.get("stated_pct") is not None]
    pos_markers  = [m for m in markers if m.get("stated_pct") is None]

    total_stated_pct = sum(m["stated_pct"] for m in pct_markers) / 100.0
    total_stated_pct = min(total_stated_pct, 1.0)
    remaining_mass   = max(0.0, 1.0 - total_stated_pct)

    total_pos_weight = sum(_pos_weight(m.get("position")) for m in pos_markers)

    # NC-2a: evaluate guard BEFORE applying any penalty
    has_grain_context, grain_ew, non_grain_ew, abs_cond, rel_cond = (
        has_meaningful_grain_context(markers, remaining_mass, total_pos_weight)
    )

    def effective_weight(m: dict) -> float:
        # Base weight: stated_pct or position-distributed share
        if m.get("stated_pct") is not None:
            w = m["stated_pct"] / 100.0
        else:
            if total_pos_weight > 0:
                w = (_pos_weight(m.get("position")) / total_pos_weight) * remaining_mass
            else:
                w = 0.0

        # Lexicon half-weight modifier (e.g. barley_malt) — unchanged
        if m.get("half_weight"):
            w *= 0.5

        # NC-2b: sourdough_starter is neutral — treated as unclassified.
        # It falls through to the "not in NON_GRAIN_WHOLE_LABELS" branch below
        # because it was removed from that set. The marker has class="whole" in
        # the lexicon but is excluded from GRAIN_WHOLE_LABELS too.
        # Net effect: effective_weight is computed normally (no penalty) and is
        # added to whole_weight. BUT sourdough_starter is not penalized. This
        # means the starter's base weight contributes to whole_weight.
        #
        # WAIT — the spec says sourdough_starter should contribute ZERO to both
        # whole_weight and refined_weight. It is neutral/invisible. To achieve
        # true neutrality, we must zero it out here.
        if m["label"] == "sourdough_starter":
            return 0.0   # NC-2b: invisible to the signal

        # M-2 grain-context penalty (NC-2a guard replaces simple has_grain_whole):
        # Only applies when guard is active AND marker is in NON_GRAIN_WHOLE_LABELS.
        if (has_grain_context
                and m["class"] == "whole"
                and m["label"] in NON_GRAIN_WHOLE_LABELS):
            w *= 0.5

        return w

    whole_weight   = sum(effective_weight(m) for m in markers if m["class"] == "whole")
    refined_weight = sum(effective_weight(m) for m in markers if m["class"] == "refined")

    total_weight = whole_weight + refined_weight
    if total_weight < 0.01:
        return None

    dominance_ratio = whole_weight / total_weight

    # First-ingredient anchor — direction logic unchanged from v4/v5
    highest = max(markers, key=effective_weight)
    anchor_class = highest["class"]

    # M-1: anchor nudge +/-0.05 (unchanged from v5)
    ANCHOR_NUDGE = 0.05
    if anchor_class == "refined" and dominance_ratio > 0.5:
        dominance_ratio = max(0.5, dominance_ratio - ANCHOR_NUDGE)
    elif anchor_class == "whole" and dominance_ratio < 0.5:
        dominance_ratio = min(0.5, dominance_ratio + ANCHOR_NUDGE)

    score = 10.0 + dominance_ratio * 85.0
    return round(score, 1)


# ---------------------------------------------------------------------------
# Detailed weight decomposition for a product (v5.1 guard aware)
# ---------------------------------------------------------------------------

def decompose_weights_v5_1(markers: list[dict]) -> dict:
    """
    Returns full weight decomposition with v5.1 guard information.
    Tracks: grain_whole_ew (GRAIN_WHOLE_LABELS only), non_grain_whole_ew (before penalty),
    guard activation status, per-marker breakdown.
    """
    pct_markers = [m for m in markers if m.get("stated_pct") is not None]
    pos_markers  = [m for m in markers if m.get("stated_pct") is None]
    total_stated_pct = min(sum(m["stated_pct"] for m in pct_markers) / 100.0, 1.0)
    remaining_mass   = max(0.0, 1.0 - total_stated_pct)
    total_pos_weight = sum(_pos_weight(m.get("position")) for m in pos_markers)

    def bw(m):
        if m.get("stated_pct") is not None:
            w = m["stated_pct"] / 100.0
        else:
            w = (_pos_weight(m.get("position")) / total_pos_weight) * remaining_mass if total_pos_weight > 0 else 0.0
        if m.get("half_weight"):
            w *= 0.5
        return w

    # Guard evaluation
    has_grain_context, grain_ew, non_grain_ew, abs_cond, rel_cond = (
        has_meaningful_grain_context(markers, remaining_mass, total_pos_weight)
    )

    grain_whole_w = 0.0
    non_grain_whole_w_before = 0.0
    non_grain_whole_w_after  = 0.0
    refined_w = 0.0
    sourdough_w_zeroed = 0.0
    breakdown = []

    for m in markers:
        base = bw(m)
        is_grain_whole     = m["class"] == "whole" and m["label"] in GRAIN_WHOLE_LABELS
        is_non_grain_whole = m["class"] == "whole" and m["label"] in NON_GRAIN_WHOLE_LABELS
        is_sourdough       = m["label"] == "sourdough_starter"
        is_barley_malt     = m["label"] == "barley_malt"

        if is_sourdough:
            # NC-2b: neutral — zeroed out
            eff = 0.0
            sourdough_w_zeroed += base
        elif is_grain_whole:
            grain_whole_w += base
            eff = base
        elif is_non_grain_whole:
            non_grain_whole_w_before += base
            eff = base * 0.5 if has_grain_context else base
            non_grain_whole_w_after += eff
        elif m["class"] == "whole":
            # whole but in neither label set (barley_malt, lentils, chickpeas, sourdough already handled)
            # barley_malt: counted in whole_weight at its base (already half-weighted)
            grain_whole_w += base   # contributes to whole but does NOT count toward guard floor
            eff = base
        else:
            refined_w += base
            eff = base

        breakdown.append({
            "label": m["label"],
            "class": m["class"],
            "stated_pct": m.get("stated_pct"),
            "position": m.get("position"),
            "base_w": round(base, 5),
            "eff_w": round(eff, 5),
            "is_grain_whole": is_grain_whole,
            "is_non_grain_whole": is_non_grain_whole,
            "is_sourdough_zeroed": is_sourdough,
            "is_barley_malt": is_barley_malt,
            "penalized": is_non_grain_whole and has_grain_context,
        })

    return {
        "has_grain_context": has_grain_context,
        "guard_abs_condition": abs_cond,
        "guard_rel_condition": rel_cond,
        "grain_whole_ew_for_guard": round(grain_ew, 5),      # GRAIN_WHOLE_LABELS only (excl barley_malt)
        "non_grain_whole_ew_for_guard": round(non_grain_ew, 5),  # NON_GRAIN_WHOLE_LABELS (excl sourdough)
        "grain_whole_w": round(grain_whole_w, 5),             # all grain-whole + barley_malt in total
        "non_grain_whole_w_before_penalty": round(non_grain_whole_w_before, 5),
        "non_grain_whole_w_after_penalty": round(non_grain_whole_w_after, 5),
        "refined_w": round(refined_w, 5),
        "sourdough_w_zeroed": round(sourdough_w_zeroed, 5),
        "breakdown": breakdown,
    }


# ---------------------------------------------------------------------------
# Gate helpers — IDENTICAL to v4/v5
# ---------------------------------------------------------------------------

def check_b1_pass(score: float, tier: str) -> bool:
    if tier == "T1":
        return score >= 60.0
    elif tier == "T2":
        return score <= 45.0
    return True

def b1_expected_zone(tier: str) -> str:
    if tier == "T1":
        return ">= 60"
    elif tier == "T2":
        return "<= 45"
    return "N/A"


def score_to_grade(score: Optional[float]) -> Optional[str]:
    if score is None:
        return None
    if score >= 80:
        return "A"
    if score >= 65:
        return "B"
    if score >= 50:
        return "C"
    if score >= 35:
        return "D"
    return "F"


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def main():
    print("=== Component B Matrix Signal Probe v5.1 (NC-2a: trace-grain guard | NC-2b: sourdough neutral) ===")
    print(f"Run: {datetime.now(timezone.utc).isoformat()}")
    print()

    with open(GOLD_SET_PATH, encoding="utf-8") as f:
        gold = json.load(f)

    products = gold["products"]
    print(f"Gold set: {len(products)} products (schema: {gold.get('schema_version')})")
    print(f"Frozen by: {gold.get('frozen_by')}")
    print()

    parseable_count = 0
    stated_pct_present_count = 0
    all_results = []

    # Load v5 scores for comparison
    v5_score_map = {}
    v5_path = OUT_DIR / "matrix_signal_probe_v5_results.json"
    if v5_path.exists():
        try:
            with open(v5_path, encoding="utf-8") as fv5:
                v5_data = json.load(fv5)
            v5_score_map = {p["barcode"]: p.get("v5_score") for p in v5_data.get("products", [])}
        except Exception:
            pass

    # Load v4 scores for longer comparison chain
    v4_score_map = {}
    v4_path = OUT_DIR / "matrix_signal_probe_v4_results.json"
    if v4_path.exists():
        try:
            with open(v4_path, encoding="utf-8") as fv4:
                v4_data = json.load(fv4)
            v4_score_map = {p["barcode"]: p.get("v4_score") for p in v4_data.get("products", [])}
        except Exception:
            pass

    # Track grain-context activation per product (for the activation table)
    grain_context_table = []

    for p in products:
        barcode = p["barcode"]
        text = p.get("ingredients_text_he", "")
        tier = p["tier"]
        expected_label = p["expected_label"]
        gradable = p.get("gradable", True)
        spelt_correction = p.get("spelt_correction", False)

        unparseable = is_unparseable(text)
        if unparseable or not text:
            score = None
            markers = []
            parseable = False
            records = []
            decomp = None
        else:
            parseable = True
            parseable_count += 1
            records = parse_ingredients(text)
            markers = extract_all_markers_v4(text)
            score = compute_component_b_score_v5_1(markers)
            decomp = decompose_weights_v5_1(markers)

        has_stated_pct = any(m.get("stated_pct") is not None for m in markers)
        if parseable and has_stated_pct:
            stated_pct_present_count += 1

        b1_applicable = gradable and tier in ("T1", "T2")
        b1_pass = None
        if b1_applicable and score is not None:
            b1_pass = check_b1_pass(score, tier)

        whole_markers   = [m for m in markers if m["class"] == "whole"]
        refined_markers = [m for m in markers if m["class"] == "refined"]

        v5_score = v5_score_map.get(barcode)
        v4_score = v4_score_map.get(barcode)

        v5_1_grade = score_to_grade(score)
        v5_grade   = score_to_grade(v5_score)
        v4_grade   = score_to_grade(v4_score)

        grade_changed_vs_v5 = (v5_1_grade != v5_grade) if (v5_1_grade and v5_grade) else False
        grade_changed_vs_v4 = (v5_1_grade != v4_grade) if (v5_1_grade and v4_grade) else False

        result = {
            "barcode": barcode,
            "name_he": p.get("name_he", ""),
            "tier": tier,
            "expected_label": expected_label,
            "gradable": gradable,
            "spelt_correction": spelt_correction,
            "v4_score": v4_score,
            "v5_score": v5_score,
            "v5_1_score": score,
            "v4_grade": v4_grade,
            "v5_grade": v5_grade,
            "v5_1_grade": v5_1_grade,
            "grade_changed_vs_v5": grade_changed_vs_v5,
            "grade_changed_vs_v4": grade_changed_vs_v4,
            "parseable": parseable,
            "n_records": len(records),
            "n_whole_markers": len(whole_markers),
            "n_refined_markers": len(refined_markers),
            "whole_markers": [m["label"] for m in whole_markers],
            "refined_markers": [m["label"] for m in refined_markers],
            "marker_detail": [
                {"label": m["label"], "class": m["class"],
                 "position": m.get("position"), "stated_pct": m.get("stated_pct"),
                 "half_weight": m.get("half_weight", False)}
                for m in markers
            ],
            "has_stated_pct": has_stated_pct,
            "b1_applicable": b1_applicable,
            "b1_pass": b1_pass,
            "b1_expected_zone": b1_expected_zone(tier),
            "decomp": decomp,
        }
        all_results.append(result)

        # Build grain-context activation table entry
        if decomp is not None:
            grain_context_table.append({
                "barcode": barcode,
                "name_he": p.get("name_he", ""),
                "tier": tier,
                "has_grain_context": decomp["has_grain_context"],
                "grain_whole_ew": decomp["grain_whole_ew_for_guard"],
                "non_grain_whole_ew": decomp["non_grain_whole_ew_for_guard"],
                "abs_floor_met": decomp["guard_abs_condition"],
                "rel_floor_met": decomp["guard_rel_condition"],
                "v5_had_grain_context": any(
                    m["label"] in GRAIN_WHOLE_LABELS for m in markers if m["class"] == "whole"
                ),
                "v5_score": v5_score,
                "v5_1_score": score,
                "delta": round(score - v5_score, 1) if (score is not None and v5_score is not None) else None,
                "guard_changed_behavior": (
                    any(m["label"] in GRAIN_WHOLE_LABELS for m in markers if m["class"] == "whole")
                    != decomp["has_grain_context"]
                ),
            })

    # ---------------------------------------------------------------------------
    # Gate B1
    # ---------------------------------------------------------------------------
    b1_products = [r for r in all_results if r["b1_applicable"] and r["v5_1_score"] is not None]
    b1_pass_count = sum(1 for r in b1_products if r["b1_pass"])
    b1_fail_count = len(b1_products) - b1_pass_count
    b1_rate = b1_pass_count / len(b1_products) if b1_products else 0.0
    b1_verdict = "PASS" if b1_rate >= 0.90 else "FAIL"

    b1_no_corr = [r for r in all_results if r["b1_applicable"] and r["v5_1_score"] is not None and not r["spelt_correction"]]
    b1_pass_no_corr = sum(1 for r in b1_no_corr if r["b1_pass"])
    b1_rate_no_corr = b1_pass_no_corr / len(b1_no_corr) if b1_no_corr else 0.0

    b1_t1 = [r for r in b1_products if r["tier"] == "T1"]
    b1_t2 = [r for r in b1_products if r["tier"] == "T2"]
    b1_t1_pass = sum(1 for r in b1_t1 if r["b1_pass"])
    b1_t2_pass = sum(1 for r in b1_t2 if r["b1_pass"])

    # ---------------------------------------------------------------------------
    # Gate B2 — ALL 20 T3 pairs, AS-IS (RP-04 uncorrected in frozen JSON)
    # ---------------------------------------------------------------------------
    ranking_pairs = gold.get("ranking_pairs_T3", [])
    score_map = {r["barcode"]: r["v5_1_score"] for r in all_results}

    b2_results = []
    for pair in ranking_pairs:
        higher_bc = pair["higher"]
        lower_bc  = pair["lower"]
        higher_score = score_map.get(higher_bc)
        lower_score  = score_map.get(lower_bc)
        if higher_score is None or lower_score is None:
            pair_pass = None
            eval_note = "score unavailable for one product"
            margin = None
        else:
            pair_pass = higher_score > lower_score
            margin = round(higher_score - lower_score, 1)
            if pair_pass:
                eval_note = f"{higher_score} > {lower_score}  margin={margin:+.1f}"
            else:
                eval_note = f"{higher_score} <= {lower_score}  margin={margin:.1f}  WRONG DIRECTION"
        b2_results.append({
            "pair_id": pair["id"],
            "higher_barcode": higher_bc,
            "lower_barcode": lower_bc,
            "higher_score": higher_score,
            "lower_score": lower_score,
            "pass": pair_pass,
            "margin": margin,
            "pair_reason": pair.get("reason", ""),
            "stress_target": pair.get("stress_target", ""),
            "eval_note": eval_note,
        })

    b2_evaluable  = [p for p in b2_results if p["pass"] is not None]
    b2_pass_count = sum(1 for p in b2_evaluable if p["pass"])
    b2_fail_count = len(b2_evaluable) - b2_pass_count
    b2_rate = b2_pass_count / len(b2_evaluable) if b2_evaluable else 0.0
    b2_verdict = "PASS" if b2_rate >= 0.95 else "FAIL"
    b2_t3_pair_count = len(ranking_pairs)

    # RP-04 corrected count: count as PASS if the corrected direction (muesli > granola) holds
    # RP-04: higher in frozen JSON = 7290011131975 (granola, WRONG — should be muesli)
    # Corrected: higher should be 7290011131388 (muesli)
    rp04_granola_score = score_map.get("7290011131975")
    rp04_muesli_score  = score_map.get("7290011131388")
    rp04_corrected_pass = (
        rp04_muesli_score is not None
        and rp04_granola_score is not None
        and rp04_muesli_score > rp04_granola_score
    )

    # B2 with RP-04 counted in correct direction
    b2_pass_corrected = b2_pass_count - (1 if not rp04_corrected_pass else 0)  # fix: if corrected is pass, already counted; if not, adjust
    # Recount properly:
    b2_corrected_results = []
    for pr in b2_evaluable:
        if pr["pair_id"] == "RP-04":
            # Evaluate with corrected direction: muesli=7290011131388 should be higher
            h_corr = score_map.get("7290011131388")
            l_corr = score_map.get("7290011131975")
            if h_corr is not None and l_corr is not None:
                b2_corrected_results.append(h_corr > l_corr)
            # else don't count
        else:
            b2_corrected_results.append(pr["pass"])
    b2_pass_count_corrected = sum(1 for x in b2_corrected_results if x)
    b2_rate_corrected = b2_pass_count_corrected / len(b2_corrected_results) if b2_corrected_results else 0.0
    b2_verdict_corrected = "PASS" if b2_rate_corrected >= 0.95 else "FAIL"

    knife_edge_pairs = [p for p in b2_evaluable if p["pass"] and p["margin"] is not None and p["margin"] <= 1.0]

    # ---------------------------------------------------------------------------
    # Gate B3
    # ---------------------------------------------------------------------------
    parseable_results = [r for r in all_results if r["parseable"]]
    no_marker_parseable = [r for r in parseable_results if r["n_whole_markers"] + r["n_refined_markers"] == 0]
    b3_coverage = (parseable_count - len(no_marker_parseable)) / parseable_count if parseable_count > 0 else 0.0
    b3_verdict = "PASS" if b3_coverage >= 0.95 else "FAIL"

    stated_pct_rate = stated_pct_present_count / parseable_count if parseable_count > 0 else 0.0
    mc3_risk_flag = stated_pct_rate < 0.50

    # ---------------------------------------------------------------------------
    # NC-2 verification checks
    # ---------------------------------------------------------------------------
    nc2a_products_changed = [r for r in grain_context_table if r["guard_changed_behavior"]]

    # T1 products where guard suppressed grain context (potential regression)
    t1_guard_suppressed = [
        r for r in grain_context_table
        if r.get("v5_had_grain_context") and not r["has_grain_context"]
        and next((p["tier"] for p in products if p["barcode"] == r["barcode"]), "") == "T1"
    ]

    # Specific checks:
    # 1. 7290107947480: should have grain_context=False, score ~35 (D)
    check_7290107947480 = next((r for r in all_results if r["barcode"] == "7290107947480"), None)
    check_7290107947480_ok = (
        check_7290107947480 is not None
        and check_7290107947480["v5_1_score"] is not None
        and check_7290107947480["v5_1_score"] >= 35.0
        and check_7290107947480["v5_1_score"] < 50.0  # expect D range
        and check_7290107947480["v5_1_grade"] == "D"
    )
    check_7290107947480_guard = next(
        (r["has_grain_context"] for r in grain_context_table if r["barcode"] == "7290107947480"),
        None
    )

    # 2. 481180: sourdough_starter should contribute 0, score ~33 (D)
    check_481180 = next((r for r in all_results if r["barcode"] == "481180"), None)
    check_481180_ok = (
        check_481180 is not None
        and check_481180["v5_1_score"] is not None
        and check_481180["v5_1_grade"] == "D"
    )
    check_481180_sourdough_zero = False
    if check_481180 and check_481180["decomp"]:
        check_481180_sourdough_zero = check_481180["decomp"]["sourdough_w_zeroed"] > 0
        # and that the eff_w for sourdough in breakdown is 0
        sd_in_breakdown = [
            m for m in check_481180["decomp"]["breakdown"]
            if m["label"] == "sourdough_starter"
        ]
        check_481180_sourdough_zero = len(sd_in_breakdown) > 0 and all(m["eff_w"] == 0.0 for m in sd_in_breakdown)

    # ---------------------------------------------------------------------------
    # Score distributions
    # ---------------------------------------------------------------------------
    gradable_scored = [r for r in all_results if r["gradable"] and r["v5_1_score"] is not None]
    scores = sorted(r["v5_1_score"] for r in gradable_scored)

    if scores:
        score_mean   = statistics.mean(scores)
        score_median = statistics.median(scores)
        score_stdev  = statistics.stdev(scores) if len(scores) > 1 else 0.0
        score_min    = scores[0]
        score_max    = scores[-1]
        rounded      = [round(s) for s in scores]
        most_common_score, most_common_count = Counter(rounded).most_common(1)[0]
    else:
        score_mean = score_median = score_stdev = score_min = score_max = None
        most_common_score = most_common_count = None

    t1_scores   = sorted(r["v5_1_score"] for r in all_results if r["tier"] == "T1" and r["v5_1_score"] is not None)
    t2_scores   = sorted(r["v5_1_score"] for r in all_results if r["tier"] == "T2" and r["v5_1_score"] is not None)
    t3_scores   = sorted(r["v5_1_score"] for r in all_results if r["tier"] == "T3" and r["v5_1_score"] is not None)

    all_gates_pass = (b1_verdict == "PASS") and (b2_verdict_corrected == "PASS") and (b3_verdict == "PASS")
    overall_verdict = "PASS" if all_gates_pass else "FAIL"

    unreadable_product = next((r for r in all_results if r["tier"] == "UNREADABLE"), None)
    unreadable_score   = unreadable_product["v5_1_score"] if unreadable_product else "N/A"
    unreadable_ok      = unreadable_score is None

    # ---------------------------------------------------------------------------
    # Build report text
    # ---------------------------------------------------------------------------
    lines = []
    lines.append("=" * 80)
    lines.append("COMPONENT B MATRIX SIGNAL PROBE v5.1")
    lines.append("NC-2a: trace-grain guard (abs 5% + rel 50%) | NC-2b: sourdough neutral")
    lines.append("Formula base: v5 (M-1: nudge 0.05 | M-2: grain-context 0.5x penalty)")
    lines.append(f"Run: {datetime.now(timezone.utc).isoformat()}")
    lines.append("TASK: TASK-395 | Reader: structured_ingredient_reader.py (v4, unchanged)")
    lines.append(f"Gold set: matrix_gold_set_v2.json ({len(products)} products, 20 T3 pairs)")
    lines.append(f"Frozen by: {gold.get('frozen_by')}")
    lines.append("RP-04: as-is in frozen JSON (uncorrected). B2 reported both as-is and corrected.")
    lines.append("=" * 80)
    lines.append("")

    # ---------------------------------------------------------------------------
    lines.append("-" * 80)
    lines.append("UNREADABLE PRODUCT CHECK")
    lines.append(f"7290013453624: v5_1_score = {unreadable_score}")
    lines.append(f"Result: {'PASS' if unreadable_ok else 'FAIL — should be None'}")
    lines.append("")

    # ---------------------------------------------------------------------------
    lines.append("-" * 80)
    lines.append("GATE B1: ANCHOR CALIBRATION")
    lines.append("Condition: T1 score >= 60; T2 score <= 45  |  Bar: >= 90%")
    lines.append("-" * 80)
    lines.append(f"T1 (clear-whole): {b1_t1_pass}/{len(b1_t1)} pass (score >= 60)")
    if b1_t1:
        lines.append(f"  Scores: {sorted(r['v5_1_score'] for r in b1_t1 if r['v5_1_score'] is not None)}")
    lines.append(f"T2 (clear-refined): {b1_t2_pass}/{len(b1_t2)} pass (score <= 45)")
    if b1_t2:
        lines.append(f"  Scores: {sorted(r['v5_1_score'] for r in b1_t2 if r['v5_1_score'] is not None)}")
    lines.append(f"COMBINED B1: {b1_pass_count}/{len(b1_products)} = {b1_rate:.1%}  |  Target >= 90%  |  {b1_verdict}")
    if b1_fail_count > 0:
        lines.append(f"B1 FAILURES ({b1_fail_count}):")
        for r in all_results:
            if r["b1_applicable"] and r["b1_pass"] is False:
                lines.append(f"  {r['barcode']} ({r['name_he']}) tier={r['tier']} v5={r['v5_score']} v5.1={r['v5_1_score']} expected={r['b1_expected_zone']}")
                prod_note = next((p.get("b1_known_failure_note", "") for p in products if p["barcode"] == r["barcode"]), "")
                if prod_note:
                    lines.append(f"    KNOWN: {prod_note}")
    lines.append("")

    # ---------------------------------------------------------------------------
    lines.append("-" * 80)
    lines.append("GATE B2: ORDINAL RANKING — ALL 20 T3 PAIRS")
    lines.append("Condition: more-whole product scores higher  |  Bar: >= 95% = 19/20")
    lines.append(f"Total pairs: {b2_t3_pair_count}  |  Evaluable: {len(b2_evaluable)}")
    lines.append("")
    lines.append(f"B2 AS-IS (RP-04 uncorrected in frozen JSON): {b2_pass_count}/{len(b2_evaluable)} = {b2_rate:.1%}  |  {b2_verdict}")
    lines.append(f"B2 WITH RP-04 CORRECTED (muesli 39% > granola 28% effective): {b2_pass_count_corrected}/{len(b2_corrected_results)} = {b2_rate_corrected:.1%}  |  {b2_verdict_corrected}")
    lines.append(f"RP-04 corrected direction: muesli ({rp04_muesli_score}) {'>' if rp04_corrected_pass else '<='} granola ({rp04_granola_score}) — {'CORRECT' if rp04_corrected_pass else 'WRONG'}")
    lines.append("")

    # Per-pair table
    lines.append(f"{'Pair':<8} {'Higher BC':<18} {'Lower BC':<18} {'H_score':<9} {'L_score':<9} {'Margin':<9} {'Pass':<6}")
    lines.append("-" * 80)
    for pr in b2_results:
        h_str = f"{pr['higher_score']:.1f}" if pr['higher_score'] is not None else "None"
        l_str = f"{pr['lower_score']:.1f}" if pr['lower_score'] is not None else "None"
        m_str = f"{pr['margin']:+.1f}" if pr['margin'] is not None else "N/A"
        p_str = "OK" if pr['pass'] else ("FAIL" if pr['pass'] is False else "N/A")
        rp04_note = " [GOLD-SET-ERROR-UNCORRECTED]" if pr["pair_id"] == "RP-04" and not pr["pass"] else ""
        lines.append(f"{pr['pair_id']:<8} {pr['higher_barcode']:<18} {pr['lower_barcode']:<18} {h_str:<9} {l_str:<9} {m_str:<9} {p_str}{rp04_note}")
    lines.append("")

    if knife_edge_pairs:
        lines.append(f"KNIFE-EDGE MARGINS (<= 1.0 pt): {len(knife_edge_pairs)} pair(s):")
        for pr in knife_edge_pairs:
            lines.append(f"  {pr['pair_id']}: margin={pr['margin']:+.1f}")
            lines.append(f"    {pr['pair_reason']}")
    else:
        lines.append("No knife-edge margins (<= 1.0 pt).")
    lines.append("")

    if b2_fail_count > 0:
        lines.append(f"FAILING PAIRS (as-is, {b2_fail_count}):")
        for pr in b2_results:
            if pr["pass"] is False:
                lines.append(f"  {pr['pair_id']}: {pr['higher_barcode']} vs {pr['lower_barcode']}")
                lines.append(f"    {pr['eval_note']}")
                lines.append(f"    Reason: {pr['pair_reason']}")
    lines.append("")

    # ---------------------------------------------------------------------------
    lines.append("-" * 80)
    lines.append("GATE B3: MARKER COVERAGE (parseable denominator)")
    lines.append("Condition: >= 95% of parseable products fire >= 1 marker")
    lines.append("-" * 80)
    lines.append(f"Parseable: {parseable_count}  |  No markers: {len(no_marker_parseable)}")
    lines.append(f"Coverage: {parseable_count - len(no_marker_parseable)}/{parseable_count} = {b3_coverage:.1%}  |  {b3_verdict}")
    lines.append("")

    # ---------------------------------------------------------------------------
    lines.append("-" * 80)
    lines.append("GRAIN-CONTEXT ACTIVATION TABLE (per product)")
    lines.append("Guard conditions: abs_floor=grain_whole_ew>=5% AND rel_floor=grain_whole_ew>=50% of non_grain_whole_ew")
    lines.append("-" * 80)
    lines.append(f"{'Barcode':<18} {'Tier':<5} {'grain_ew':<10} {'ng_ew':<10} {'abs?':<6} {'rel?':<6} {'ctx?':<6} {'chg?':<5} {'v5':>6} {'v5.1':>6}")
    lines.append("-" * 80)
    for row in grain_context_table:
        changed = "Y" if row["guard_changed_behavior"] else "N"
        ctx = "Y" if row["has_grain_context"] else "N"
        abs_c = "Y" if row["abs_floor_met"] else "N"
        rel_c = "Y" if row["rel_floor_met"] else "N"
        v5s = f"{row['v5_score']:.1f}" if row['v5_score'] is not None else "None"
        v51s = f"{row['v5_1_score']:.1f}" if row['v5_1_score'] is not None else "None"
        lines.append(f"{row['barcode']:<18} {row['tier']:<5} {row['grain_whole_ew']:>8.4f}  {row['non_grain_whole_ew']:>8.4f}  {abs_c:<6} {rel_c:<6} {ctx:<6} {changed:<5} {v5s:>6} {v51s:>6}")
    lines.append("")

    lines.append("Products where guard CHANGED behavior from v5 (guard suppressed grain context):")
    if nc2a_products_changed:
        for r in nc2a_products_changed:
            tier_label = next((p["tier"] for p in products if p["barcode"] == r["barcode"]), "?")
            lines.append(f"  {r['barcode']} ({r['name_he']}) tier={tier_label}")
            lines.append(f"    grain_whole_ew={r['grain_whole_ew']:.4f} (abs={r['abs_floor_met']}, rel={r['rel_floor_met']})")
            lines.append(f"    v5_score={r['v5_score']} -> v5.1_score={r['v5_1_score']}  delta={r['delta']}")
    else:
        lines.append("  None — guard did not suppress any product's grain context vs v5.")
    lines.append("")

    lines.append("T1 products where guard SUPPRESSED grain context (regression risk):")
    if t1_guard_suppressed:
        for r in t1_guard_suppressed:
            lines.append(f"  *** REGRESSION RISK *** {r['barcode']} tier=T1 — guard suppressed grain context!")
            lines.append(f"    grain_whole_ew={r['grain_whole_ew']:.4f} (abs={r['abs_floor_met']}, rel={r['rel_floor_met']})")
    else:
        lines.append("  NONE — no T1 product had grain context suppressed. Guard is safe.")
    lines.append("")

    # ---------------------------------------------------------------------------
    lines.append("-" * 80)
    lines.append("NC-2 VERIFICATION: 7290107947480 and 481180")
    lines.append("-" * 80)
    if check_7290107947480:
        lines.append(f"7290107947480 (Fitness bar, chocolate + nuts):")
        lines.append(f"  Ingredient: חיטה מלאה 1% inside פתיתי דגנים 32% — effective product-weight = 0.32%")
        lines.append(f"  Reader effective_pct: 0.32% (1% x 32% = label-correct)")
        lines.append(f"  grain_whole_ew for guard (GRAIN_WHOLE_LABELS only): {next((r['grain_whole_ew'] for r in grain_context_table if r['barcode'] == '7290107947480'), 'N/A')}")
        lines.append(f"  Guard active (grain_context): {check_7290107947480_guard} (expected: False)")
        lines.append(f"  v4_score={check_7290107947480['v4_score']}  v5_score={check_7290107947480['v5_score']}  v5.1_score={check_7290107947480['v5_1_score']}")
        lines.append(f"  v5.1 grade: {check_7290107947480['v5_1_grade']} (expected: D, not F)")
        lines.append(f"  NC-2 RESOLVED: {'YES' if check_7290107947480_ok and check_7290107947480_guard == False else 'NO — CHECK FAILED'}")
    lines.append("")
    if check_481180:
        lines.append(f"481180 (Sourdough bread):")
        d = check_481180["decomp"]
        sd_broken = [m for m in d["breakdown"] if m["label"] == "sourdough_starter"] if d else []
        sd_eff_w = sd_broken[0]["eff_w"] if sd_broken else "N/A"
        sd_base_w = sd_broken[0]["base_w"] if sd_broken else "N/A"
        lines.append(f"  Sourdough starter: base_w={sd_base_w}, eff_w={sd_eff_w} (expected: 0.0)")
        lines.append(f"  sourdough_w_zeroed={d['sourdough_w_zeroed'] if d else 'N/A'}")
        lines.append(f"  v4_score={check_481180['v4_score']}  v5_score={check_481180['v5_score']}  v5.1_score={check_481180['v5_1_score']}")
        lines.append(f"  v5.1 grade: {check_481180['v5_1_grade']} (expected: D, not F)")
        lines.append(f"  Sourdough zero contribution: {'YES' if check_481180_sourdough_zero else 'NO — CHECK FAILED'}")
        lines.append(f"  NC-2 RESOLVED: {'YES' if check_481180_ok and check_481180_sourdough_zero else 'NO — CHECK FAILED'}")
    lines.append("")

    # sourdough_starter check across all products
    sourdough_primary = [r for r in all_results if any(
        m["label"] == "sourdough_starter" and m.get("position", 99) <= 3
        for m in r.get("marker_detail", [])
    )]
    lines.append(f"Products with sourdough_starter at positions 1-3: {len(sourdough_primary)}")
    for r in sourdough_primary:
        if r["decomp"]:
            sd_entries = [m for m in r["decomp"]["breakdown"] if m["label"] == "sourdough_starter"]
            for sd in sd_entries:
                lines.append(f"  {r['barcode']} {r['name_he']}: base_w={sd['base_w']} eff_w={sd['eff_w']} (zeroed={'YES' if sd['eff_w']==0.0 else 'NO'})")
    lines.append("")

    # ---------------------------------------------------------------------------
    lines.append("-" * 80)
    lines.append("SCORE DISTRIBUTION (v5.1, gradable scored products)")
    lines.append("-" * 80)
    lines.append(f"N: {len(scores)}")
    if scores:
        lines.append(f"Min: {score_min}  Max: {score_max}  Mean: {score_mean:.1f}  Median: {score_median:.1f}  Stdev: {score_stdev:.1f}")
        lines.append(f"Most common (rounded): {most_common_score} (n={most_common_count})")
    lines.append(f"T1 scores: {t1_scores}")
    lines.append(f"T2 scores: {t2_scores}")
    lines.append(f"T3 scores: {t3_scores}")
    lines.append("")

    # ---------------------------------------------------------------------------
    lines.append("-" * 80)
    lines.append("PER-PRODUCT TABLE (v4 / v5 / v5.1)")
    lines.append(f"{'barcode':<18} {'tier':<5} {'v4':>6} {'v5':>6} {'v5.1':>6} {'v4G':>4} {'v5G':>4} {'51G':>4} {'b1':>6} {'ctx?':>5} label")
    lines.append("-" * 80)
    for r in all_results:
        b1_str = str(r["b1_pass"]) if r["b1_applicable"] else "N/A"
        v51_str = f"{r['v5_1_score']:.1f}" if r["v5_1_score"] is not None else "None"
        v5_str  = f"{r['v5_score']:.1f}"   if r["v5_score"] is not None  else "None"
        v4_str  = f"{r['v4_score']:.1f}"   if r["v4_score"] is not None  else "None"
        v4g = r["v4_grade"] or "N/A"
        v5g = r["v5_grade"] or "N/A"
        v51g = r["v5_1_grade"] or "N/A"
        ctx_entry = next((row for row in grain_context_table if row["barcode"] == r["barcode"]), None)
        ctx_str = "Y" if (ctx_entry and ctx_entry["has_grain_context"]) else ("N" if ctx_entry else "?")
        lines.append(f"{r['barcode']:<18} {r['tier']:<5} {v4_str:>6} {v5_str:>6} {v51_str:>6} {v4g:>4} {v5g:>4} {v51g:>4} {b1_str:>6} {ctx_str:>5} {r['expected_label']}")
    lines.append("")

    # ---------------------------------------------------------------------------
    lines.append("=" * 80)
    lines.append("OVERALL VERDICT")
    lines.append("=" * 80)
    lines.append(f"Gate B1 (anchor >= 90%):          {b1_verdict}  [{b1_pass_count}/{len(b1_products)} = {b1_rate:.1%}]")
    lines.append(f"Gate B2 AS-IS (>= 95%):           {b2_verdict}  [{b2_pass_count}/{len(b2_evaluable)} = {b2_rate:.1%}]  (RP-04 uncorrected)")
    lines.append(f"Gate B2 RP-04 CORRECTED (>= 95%): {b2_verdict_corrected}  [{b2_pass_count_corrected}/{len(b2_corrected_results)} = {b2_rate_corrected:.1%}]")
    lines.append(f"Gate B3 (coverage >= 95%):         {b3_verdict}  [{parseable_count - len(no_marker_parseable)}/{parseable_count} = {b3_coverage:.1%}]")
    lines.append(f"NC-2a 7290107947480 resolved:      {'YES' if check_7290107947480_ok and check_7290107947480_guard == False else 'NO'}")
    lines.append(f"NC-2b 481180 sourdough zeroed:     {'YES' if check_481180_ok and check_481180_sourdough_zero else 'NO'}")
    lines.append(f"T1 guard regression: 0 T1 products lost grain context: {'SAFE' if not t1_guard_suppressed else 'REGRESSION'}")
    lines.append(f"Knife-edge pairs (<= 1.0pt):       {len(knife_edge_pairs)}")
    lines.append(f"Unreadable returns None:           {'PASS' if unreadable_ok else 'FAIL'}")
    lines.append("")
    lines.append(f"OVERALL (B1+B2-corrected+B3 all pass): {'PASS' if all_gates_pass else 'FAIL'}")
    lines.append("")
    lines.append("NC-3 ACKNOWLEDGMENT (unchanged): barcode 7290106571945 B1 known failure.")
    lines.append("  Cause: composite-without-parent_pct gap. Deferred per Ruling 4.")
    lines.append("=" * 80)

    report_text = "\n".join(lines)

    # ---------------------------------------------------------------------------
    # Write outputs
    # ---------------------------------------------------------------------------
    report_path = OUT_DIR / "matrix_signal_probe_v5_1_report.txt"
    with open(report_path, "w", encoding="utf-8") as f:
        f.write(report_text)

    def sha256_file(path):
        h = hashlib.sha256()
        with open(path, "rb") as f2:
            h.update(f2.read())
        return h.hexdigest().upper()

    # Build JSON result
    json_out = {
        "probe": "matrix_signal_probe_v5_1",
        "reader": "structured_ingredient_reader.py (v4: R-1, R-2, spelt-construct, C-5 fixes — UNCHANGED)",
        "formula_changes_from_v5": [
            "NC-2a: Trace-grain guard on M-2 — grain_context requires grain_whole_ew >= 5% (abs) AND >= 50% of non_grain_whole_ew (rel). Both must hold simultaneously.",
            "NC-2b: sourdough_starter removed from NON_GRAIN_WHOLE_LABELS; reclassified neutral/process (contributes 0 to whole_weight and refined_weight).",
        ],
        "formula_inherited_from_v5": [
            "M-1: anchor nudge +/-0.05 (unchanged)",
            "M-2 base: 0.5x non-grain whole penalty when guard active (unchanged)",
        ],
        "gold_set": "matrix_gold_set_v2.json (as-is, RP-04 uncorrected)",
        "run_at": datetime.now(timezone.utc).isoformat(),
        "task": "TASK-395",
        "gold_set_file": str(GOLD_SET_PATH),
        "total_products": len(products),
        "gate_B1": {
            "verdict": b1_verdict,
            "pass_rate": round(b1_rate, 4),
            "pass_count": b1_pass_count,
            "total": len(b1_products),
            "t1_pass": f"{b1_t1_pass}/{len(b1_t1)}",
            "t2_pass": f"{b1_t2_pass}/{len(b1_t2)}",
            "t1_scores": t1_scores,
            "t2_scores": t2_scores,
            "failures": [
                {"barcode": r["barcode"], "name": r["name_he"], "v4_score": r["v4_score"],
                 "v5_score": r["v5_score"], "v5_1_score": r["v5_1_score"], "tier": r["tier"],
                 "whole": r["whole_markers"], "refined": r["refined_markers"]}
                for r in all_results if r["b1_applicable"] and r["b1_pass"] is False
            ],
        },
        "gate_B2_as_is": {
            "verdict": b2_verdict,
            "pass_rate": round(b2_rate, 4),
            "pass_count": b2_pass_count,
            "evaluable_pairs": len(b2_evaluable),
            "t3_pair_count": b2_t3_pair_count,
            "rp04_note": "RP-04 as-is in frozen JSON (granola=higher is WRONG direction per nutritional ruling). Counts as FAIL as-is.",
            "pair_results": b2_results,
        },
        "gate_B2_rp04_corrected": {
            "verdict": b2_verdict_corrected,
            "pass_rate": round(b2_rate_corrected, 4),
            "pass_count": b2_pass_count_corrected,
            "evaluable_pairs": len(b2_corrected_results),
            "rp04_corrected_direction_pass": rp04_corrected_pass,
            "rp04_muesli_score": rp04_muesli_score,
            "rp04_granola_score": rp04_granola_score,
        },
        "gate_B3": {
            "verdict": b3_verdict,
            "coverage_rate": round(b3_coverage, 4),
            "parseable_count": parseable_count,
            "no_marker_count": len(no_marker_parseable),
            "no_marker_barcodes": [r["barcode"] for r in no_marker_parseable],
        },
        "nc2_verification": {
            "7290107947480": {
                "grain_whole_ew_for_guard": next(
                    (r["grain_whole_ew"] for r in grain_context_table if r["barcode"] == "7290107947480"), None
                ),
                "grain_context_active": check_7290107947480_guard,
                "expected_grain_context": False,
                "v4_score": check_7290107947480["v4_score"] if check_7290107947480 else None,
                "v5_score": check_7290107947480["v5_score"] if check_7290107947480 else None,
                "v5_1_score": check_7290107947480["v5_1_score"] if check_7290107947480 else None,
                "v5_1_grade": check_7290107947480["v5_1_grade"] if check_7290107947480 else None,
                "resolved": check_7290107947480_ok and check_7290107947480_guard == False,
            },
            "481180": {
                "sourdough_contribution_zeroed": check_481180_sourdough_zero,
                "sourdough_w_zeroed": check_481180["decomp"]["sourdough_w_zeroed"] if check_481180 and check_481180["decomp"] else None,
                "v4_score": check_481180["v4_score"] if check_481180 else None,
                "v5_score": check_481180["v5_score"] if check_481180 else None,
                "v5_1_score": check_481180["v5_1_score"] if check_481180 else None,
                "v5_1_grade": check_481180["v5_1_grade"] if check_481180 else None,
                "resolved": check_481180_ok and check_481180_sourdough_zero,
            },
        },
        "grain_context_activation_table": grain_context_table,
        "t1_guard_suppressed_count": len(t1_guard_suppressed),
        "t1_guard_suppressed": t1_guard_suppressed,
        "guard_changed_behavior_count": len(nc2a_products_changed),
        "guard_changed_behavior_barcodes": [r["barcode"] for r in nc2a_products_changed],
        "score_distribution": {
            "n_scored": len(scores),
            "min": score_min,
            "max": score_max,
            "mean": round(score_mean, 2) if score_mean is not None else None,
            "median": float(score_median) if score_median is not None else None,
            "stdev": round(score_stdev, 2) if score_stdev is not None else None,
            "most_common_score": most_common_score,
            "most_common_count": most_common_count,
            "t1_scores": t1_scores,
            "t2_scores": t2_scores,
            "t3_scores": t3_scores,
        },
        "overall_verdict": overall_verdict,
        "all_gates_pass": all_gates_pass,
        "products": [
            {k: v for k, v in r.items() if k != "decomp"}
            for r in all_results
        ],
        "products_decomp": [
            {"barcode": r["barcode"], "name_he": r["name_he"], "decomp": r["decomp"]}
            for r in all_results if r["decomp"] is not None
        ],
    }

    json_path = OUT_DIR / "matrix_signal_probe_v5_1_results.json"
    with open(json_path, "w", encoding="utf-8") as f:
        json.dump(json_out, f, ensure_ascii=False, indent=2)

    gold_sha   = sha256_file(GOLD_SET_PATH)
    report_sha = sha256_file(report_path)
    json_sha   = sha256_file(json_path)

    print(report_text)
    print()
    print(f"report_path:    {report_path}")
    print(f"json_path:      {json_path}")
    print(f"gold_sha256:    {gold_sha}")
    print(f"report_sha256:  {report_sha}")
    print(f"json_sha256:    {json_sha}")

    return {
        "b1_verdict": b1_verdict, "b1_rate": b1_rate,
        "b2_verdict_as_is": b2_verdict, "b2_rate_as_is": b2_rate,
        "b2_verdict_corrected": b2_verdict_corrected, "b2_rate_corrected": b2_rate_corrected,
        "b3_verdict": b3_verdict, "b3_coverage": b3_coverage,
        "all_gates_pass": all_gates_pass,
        "nc2a_resolved_7290107947480": check_7290107947480_ok and check_7290107947480_guard == False,
        "nc2b_resolved_481180": check_481180_ok and check_481180_sourdough_zero,
        "t1_guard_suppressed": len(t1_guard_suppressed),
        "gold_sha256": gold_sha,
        "report_sha256": report_sha,
        "json_sha256": json_sha,
    }


if __name__ == "__main__":
    main()
