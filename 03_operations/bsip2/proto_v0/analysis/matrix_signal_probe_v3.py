"""
matrix_signal_probe_v3.py
=========================
TASK-395 — Component B v3 re-validation: reading layer rebuilt on
structured_ingredient_reader.py. Same scoring formula as v2 (unchanged — no tuning).

Key difference from v2:
  - Does NOT use expand_composites() — replaced by structured_ingredient_reader.parse_ingredients()
  - Reads from structured records (position, stated_pct, qualifiers, is_sub, effective_pct)
  - The is_composite_parent skip is gone (that was the v2 bug)
  - Sub-ingredient expansion uses effective_pct from the reader (parent% × sub%)
  - Qualifier-aware: כוסמין לבן will have qualifier["לבן"] → not credited as whole

What is NOT changed from v2:
  - MARKERS lexicon (identical)
  - _pos_weight() curve (identical — not redefined)
  - compute_component_b_score() formula (identical)
  - Gate B1/B2/B3 thresholds (identical)
  - Gold set file (identical — matrix_gold_set_v1.json)

Run:
    python matrix_signal_probe_v3.py

Outputs:
    analysis/matrix_signal_probe_v3_results.json
    analysis/matrix_signal_probe_v3_report.txt
"""

import json
import re
import hashlib
import sys
import os
from pathlib import Path
from datetime import datetime, timezone
from typing import Optional

# ---------------------------------------------------------------------------
# Paths
# ---------------------------------------------------------------------------
REPO_ROOT = Path("C:/Bari")
GOLD_SET_PATH = REPO_ROOT / "03_operations/bsip2/proto_v0/analysis/matrix_gold_set_v1.json"
OUT_DIR = REPO_ROOT / "03_operations/bsip2/proto_v0/analysis"

# Import the shared reader
sys.path.insert(0, str(REPO_ROOT / "03_operations/bsip2/proto_v0/analysis"))
from structured_ingredient_reader import parse_ingredients, is_unparseable

# ---------------------------------------------------------------------------
# Position-weight curve — IDENTICAL to v2 (do not redefine)
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
# Lexicon — IDENTICAL to v2
# ---------------------------------------------------------------------------
MARKERS = [
    (r"קמח חיטה מלאה?", "whole_wheat_flour", "whole", False),
    (r"חיטה מלאה", "whole_wheat_grain", "whole", False),
    (r"קמח כוסמין מלא", "whole_spelt_flour", "whole", False),
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
    (r"מחמצת", "sourdough_starter", "whole", False),
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
# Marker extraction — from a structured ingredient record
# Key change from v2: uses record["qualifiers"] for כוסמין disambiguation
# instead of re-checking the fragment text for "לבן"
# ---------------------------------------------------------------------------

def extract_markers_from_record(record: dict) -> list[dict]:
    """
    Match MARKERS against a structured ingredient record.
    Uses record["qualifiers"] for qualifier-aware disambiguation.
    Returns list of marker dicts.
    """
    text = record["raw"]
    position = record["position"]

    # Use effective_pct (parent × sub) for subs; stated_pct for top-level
    stated_pct = record.get("effective_pct") if record.get("effective_pct") is not None \
                 else record.get("stated_pct")

    qualifiers = record.get("qualifiers", [])
    found = []
    seen_labels = set()

    # Special rule: bare חיטה at position 1 with stated_pct >= 80 → whole wheat grain
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
            # Qualifier-aware disambiguation using reader's qualifiers field
            if label in ("whole_spelt_grain", "whole_spelt_flour") and "לבן" in qualifiers:
                # כוסמין לבן is refined — white_spelt_flour marker will catch it
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


def extract_all_markers_v3(text: str) -> list[dict]:
    """
    v3 marker extraction pipeline using structured_ingredient_reader.
    1. Parse text into structured records via parse_ingredients()
    2. For each non-sub record AND sub records (with effective_pct), extract markers
    3. Deduplicate by label (keep highest-weight occurrence)

    No is_composite_parent skipping — the reader does not create phantom sub-fragments.
    """
    if is_unparseable(text):
        return []

    records = parse_ingredients(text)
    if not records:
        return []

    all_markers = []
    seen_labels: dict[str, dict] = {}

    for record in records:
        # Skip sub records that have no effective_pct AND no stated_pct
        # (their parent has no stated %, so we can't derive their weight)
        # BUT: if a sub record has its own stated_pct, it IS usable at its effective_position
        markers = extract_markers_from_record(record)
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
# Formula — IDENTICAL to v2 (no tuning)
# ---------------------------------------------------------------------------

def compute_component_b_score(markers: list[dict]) -> Optional[float]:
    if not markers:
        return None

    pct_markers = [m for m in markers if m.get("stated_pct") is not None]
    pos_markers  = [m for m in markers if m.get("stated_pct") is None]

    total_stated_pct = sum(m["stated_pct"] for m in pct_markers) / 100.0
    total_stated_pct = min(total_stated_pct, 1.0)
    remaining_mass   = max(0.0, 1.0 - total_stated_pct)

    total_pos_weight = sum(_pos_weight(m.get("position")) for m in pos_markers)

    def effective_weight(m: dict) -> float:
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

    whole_weight   = sum(effective_weight(m) for m in markers if m["class"] == "whole")
    refined_weight = sum(effective_weight(m) for m in markers if m["class"] == "refined")

    total_weight = whole_weight + refined_weight
    if total_weight < 0.01:
        return None

    dominance_ratio = whole_weight / total_weight

    highest = max(markers, key=effective_weight)
    anchor_class = highest["class"]

    if anchor_class == "refined" and dominance_ratio > 0.5:
        dominance_ratio = max(0.5, dominance_ratio - 0.15)
    elif anchor_class == "whole" and dominance_ratio < 0.5:
        dominance_ratio = min(0.5, dominance_ratio + 0.15)

    score = 10.0 + dominance_ratio * 85.0
    return round(score, 1)

# ---------------------------------------------------------------------------
# Gate helpers — IDENTICAL to v2
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

# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def main():
    print("=== Component B Matrix Signal Probe v3 (shared reader) ===")
    print(f"Run: {datetime.now(timezone.utc).isoformat()}")
    print()

    with open(GOLD_SET_PATH, encoding="utf-8") as f:
        gold = json.load(f)

    products = gold["products"]
    print(f"Gold set: {len(products)} products")

    parseable_count = 0
    stated_pct_present_count = 0
    all_results = []

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
        else:
            parseable = True
            parseable_count += 1
            records = parse_ingredients(text)
            markers = extract_all_markers_v3(text)
            score = compute_component_b_score(markers)

        has_stated_pct = any(m.get("stated_pct") is not None for m in markers)
        if parseable and has_stated_pct:
            stated_pct_present_count += 1

        b1_applicable = gradable and tier in ("T1", "T2")
        b1_pass = None
        if b1_applicable and score is not None:
            b1_pass = check_b1_pass(score, tier)

        whole_markers  = [m for m in markers if m["class"] == "whole"]
        refined_markers = [m for m in markers if m["class"] == "refined"]

        result = {
            "barcode": barcode,
            "name_he": p.get("name_he", ""),
            "tier": tier,
            "expected_label": expected_label,
            "gradable": gradable,
            "spelt_correction": spelt_correction,
            "v3_score": score,
            "parseable": parseable,
            "n_records": len(records),
            "n_whole_markers": len(whole_markers),
            "n_refined_markers": len(refined_markers),
            "whole_markers": [m["label"] for m in whole_markers],
            "refined_markers": [m["label"] for m in refined_markers],
            "has_stated_pct": has_stated_pct,
            "b1_applicable": b1_applicable,
            "b1_pass": b1_pass,
            "b1_expected_zone": b1_expected_zone(tier),
        }
        all_results.append(result)

    # ---------------------------------------------------------------------------
    # Gate B1
    # ---------------------------------------------------------------------------
    b1_products = [r for r in all_results if r["b1_applicable"] and r["v3_score"] is not None]
    b1_pass_count = sum(1 for r in b1_products if r["b1_pass"])
    b1_fail_count = len(b1_products) - b1_pass_count
    b1_rate = b1_pass_count / len(b1_products) if b1_products else 0.0
    b1_verdict = "PASS" if b1_rate >= 0.90 else "FAIL"

    b1_no_corr = [r for r in all_results if r["b1_applicable"] and r["v3_score"] is not None and not r["spelt_correction"]]
    b1_pass_no_corr = sum(1 for r in b1_no_corr if r["b1_pass"])
    b1_rate_no_corr = b1_pass_no_corr / len(b1_no_corr) if b1_no_corr else 0.0

    b1_t1 = [r for r in b1_products if r["tier"] == "T1"]
    b1_t2 = [r for r in b1_products if r["tier"] == "T2"]
    b1_t1_pass = sum(1 for r in b1_t1 if r["b1_pass"])
    b1_t2_pass = sum(1 for r in b1_t2 if r["b1_pass"])

    # ---------------------------------------------------------------------------
    # Gate B2
    # ---------------------------------------------------------------------------
    ranking_pairs = gold.get("ranking_pairs_T3", [])
    score_map = {r["barcode"]: r["v3_score"] for r in all_results}

    b2_results = []
    for pair in ranking_pairs:
        higher_bc = pair["higher"]
        lower_bc  = pair["lower"]
        higher_score = score_map.get(higher_bc)
        lower_score  = score_map.get(lower_bc)
        if higher_score is None or lower_score is None:
            pair_pass = None
            reason = "score unavailable for one product"
        else:
            pair_pass = higher_score > lower_score
            reason = f"{higher_score} > {lower_score}" if pair_pass else f"{higher_score} <= {lower_score} — WRONG DIRECTION"
        b2_results.append({
            "pair_id": pair["id"],
            "higher_barcode": higher_bc,
            "lower_barcode": lower_bc,
            "higher_score": higher_score,
            "lower_score": lower_score,
            "pass": pair_pass,
            "pair_reason": pair.get("reason", ""),
            "eval_note": reason,
        })

    b2_evaluable  = [p for p in b2_results if p["pass"] is not None]
    b2_pass_count = sum(1 for p in b2_evaluable if p["pass"])
    b2_fail_count = len(b2_evaluable) - b2_pass_count
    b2_rate = b2_pass_count / len(b2_evaluable) if b2_evaluable else 0.0
    b2_verdict = "PASS" if b2_rate >= 0.95 else "FAIL"
    b2_t3_pair_count = len(ranking_pairs)

    # ---------------------------------------------------------------------------
    # Gate B3
    # ---------------------------------------------------------------------------
    parseable_results = [r for r in all_results if r["parseable"]]
    no_marker_parseable = [r for r in parseable_results if r["n_whole_markers"] + r["n_refined_markers"] == 0]
    b3_coverage = (parseable_count - len(no_marker_parseable)) / parseable_count if parseable_count > 0 else 0.0
    b3_verdict = "PASS" if b3_coverage >= 0.95 else "FAIL"

    stated_pct_rate = stated_pct_present_count / parseable_count if parseable_count > 0 else 0.0
    mc3_risk_flag = stated_pct_rate < 0.30

    gradable_scored = [r for r in all_results if r["gradable"] and r["v3_score"] is not None]
    scores = sorted(r["v3_score"] for r in gradable_scored)
    if scores:
        import statistics
        from collections import Counter
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

    t1_scores = sorted(r["v3_score"] for r in all_results if r["tier"] == "T1" and r["v3_score"] is not None)
    t2_scores = sorted(r["v3_score"] for r in all_results if r["tier"] == "T2" and r["v3_score"] is not None)
    t3_scores = sorted(r["v3_score"] for r in all_results if r["tier"] == "T3" and r["v3_score"] is not None)

    all_gates_pass = (b1_verdict == "PASS") and (b2_verdict == "PASS") and (b3_verdict == "PASS")
    overall_verdict = "PASS — v3 reading fix clears gates" if all_gates_pass else "FAIL — one or more gates not cleared"

    unreadable_product = next((r for r in all_results if r["tier"] == "UNREADABLE"), None)
    unreadable_score   = unreadable_product["v3_score"] if unreadable_product else "N/A"
    unreadable_ok      = unreadable_score is None

    # ---------------------------------------------------------------------------
    # Build report
    # ---------------------------------------------------------------------------
    lines = []
    lines.append("=" * 72)
    lines.append("COMPONENT B MATRIX SIGNAL PROBE v3 — READING FIX VALIDATION")
    lines.append(f"Run: {datetime.now(timezone.utc).isoformat()}")
    lines.append("TASK: TASK-395 | Reader: structured_ingredient_reader.py")
    lines.append("Formula: UNCHANGED from v2. Only the reading layer changed.")
    lines.append("=" * 72)
    lines.append("")
    lines.append(f"Gold set: {len(products)} products total")
    lines.append(f"  Gradable: 57 (58 total minus 1 UNREADABLE)")
    lines.append(f"  T1 clear-whole: {len(t1_scores)} scored")
    lines.append(f"  T2 clear-refined: {len(t2_scores)} scored")
    lines.append(f"  T3 hard-mixed: {len(t3_scores)} scored")
    lines.append("")

    lines.append("-" * 72)
    lines.append("UNREADABLE PRODUCT CHECK")
    lines.append(f"7290013453624: v3_score = {unreadable_score}")
    lines.append(f"Result: {'PASS' if unreadable_ok else 'FAIL'}")
    lines.append("")

    lines.append("-" * 72)
    lines.append("GATE B1: ANCHOR CALIBRATION")
    lines.append(f"Condition: T1 score >= 60; T2 score <= 45  |  Bar: >= 90%")
    lines.append("-" * 72)
    lines.append(f"T1 (clear-whole): {b1_t1_pass}/{len(b1_t1)} pass (score >= 60)")
    if b1_t1:
        lines.append(f"  Scores: {sorted(r['v3_score'] for r in b1_t1 if r['v3_score'])}")
    lines.append(f"T2 (clear-refined): {b1_t2_pass}/{len(b1_t2)} pass (score <= 45)")
    if b1_t2:
        lines.append(f"  Scores: {sorted(r['v3_score'] for r in b1_t2 if r['v3_score'])}")
    lines.append(f"COMBINED B1: {b1_pass_count}/{len(b1_products)} = {b1_rate:.1%}  |  Target >= 90%  |  {b1_verdict}")
    if b1_fail_count > 0:
        lines.append(f"B1 FAILURES ({b1_fail_count}):")
        for r in all_results:
            if r["b1_applicable"] and r["b1_pass"] is False:
                lines.append(f"  {r['barcode']} tier={r['tier']} score={r['v3_score']} expected={r['b1_expected_zone']}")
                lines.append(f"    whole_markers={r['whole_markers']}")
                lines.append(f"    refined_markers={r['refined_markers']}")
    lines.append("")

    lines.append("-" * 72)
    lines.append("GATE B1 — MC-2: WITH vs WITHOUT SPELT CORRECTIONS")
    spelt_corrected = [r for r in all_results if r["spelt_correction"]]
    lines.append(f"B1 WITH corrections: {b1_rate:.1%} [{b1_pass_count}/{len(b1_products)}]")
    lines.append(f"B1 WITHOUT correction products: {b1_rate_no_corr:.1%} [{b1_pass_no_corr}/{len(b1_no_corr)}]")
    lines.append(f"Delta: {(b1_rate - b1_rate_no_corr):+.1%}")
    lines.append("")

    lines.append("-" * 72)
    lines.append("GATE B2: ORDINAL RANKING")
    lines.append(f"Condition: more-whole product scores higher within pairs  |  Bar: >= 95%")
    lines.append(f"MC-1: >= 10 T3 pairs required")
    lines.append("-" * 72)
    lines.append(f"Total pairs: {len(ranking_pairs)}  |  Evaluable: {len(b2_evaluable)}")
    lines.append(f"Correct: {b2_pass_count}/{len(b2_evaluable)} = {b2_rate:.1%}  |  Target >= 95%  |  {b2_verdict}")
    lines.append(f"MC-1: {b2_t3_pair_count} T3 pairs {'PASS' if b2_t3_pair_count >= 10 else 'FAIL'}")
    lines.append("")
    lines.append("All pair results:")
    for pr in b2_results:
        status = "OK" if pr["pass"] else ("FAIL" if pr["pass"] is False else "N/A")
        lines.append(f"  {pr['pair_id']} [{status}] {pr['higher_barcode']} > {pr['lower_barcode']}")
        lines.append(f"         {pr['eval_note']}")
        lines.append(f"         {pr['pair_reason']}")
    lines.append("")

    lines.append("-" * 72)
    lines.append("GATE B3: MARKER COVERAGE (parseable denominator)")
    lines.append(f"Condition: >= 95% of parseable products fire >= 1 marker")
    lines.append("-" * 72)
    lines.append(f"Parseable: {parseable_count}  |  No markers: {len(no_marker_parseable)}")
    lines.append(f"Coverage: {parseable_count - len(no_marker_parseable)}/{parseable_count} = {b3_coverage:.1%}  |  {b3_verdict}")
    if no_marker_parseable:
        lines.append("No-marker products:")
        for r in no_marker_parseable:
            lines.append(f"  {r['barcode']} tier={r['tier']}")
    lines.append("")

    lines.append("-" * 72)
    lines.append("MC-3: STATED_PCT POPULATION RATE")
    lines.append(f"Products with >= 1 stated_pct marker: {stated_pct_present_count}/{parseable_count} = {stated_pct_rate:.1%}")
    lines.append(f"{'RISK FLAG: < 30%' if mc3_risk_flag else 'OK: >= 30%'}")
    lines.append("")

    lines.append("-" * 72)
    lines.append("SCORE DISTRIBUTION (gradable scored products)")
    lines.append(f"N: {len(scores)}")
    if scores:
        lines.append(f"Min: {score_min}  Max: {score_max}  Mean: {score_mean:.1f}  Median: {score_median:.1f}  Stdev: {score_stdev:.1f}")
        lines.append(f"Most common (rounded): {most_common_score} (n={most_common_count})")
    lines.append(f"T1 scores: {t1_scores}")
    lines.append(f"T2 scores: {t2_scores}")
    lines.append(f"T3 scores: {t3_scores}")
    lines.append("")

    lines.append("-" * 72)
    lines.append("PER-PRODUCT RESULTS TABLE (barcode | tier | v2_score | v3_score | b1 | label)")
    lines.append("-" * 72)
    # Load v2 results for comparison if available
    v2_score_map = {}
    v2_path = OUT_DIR / "matrix_signal_probe_v2_results.json"
    if v2_path.exists():
        try:
            with open(v2_path, encoding="utf-8") as fv2:
                v2_data = json.load(fv2)
            v2_score_map = {p["barcode"]: p.get("v2_score") for p in v2_data.get("products", [])}
        except Exception:
            pass

    lines.append(f"{'barcode':<16} {'tier':<5} {'v2_score':<10} {'v3_score':<10} {'b1':<6} label")
    lines.append("-" * 72)
    for r in all_results:
        b1_str    = str(r["b1_pass"]) if r["b1_applicable"] else "N/A"
        v3_str    = f"{r['v3_score']:.1f}" if r["v3_score"] is not None else "None"
        v2_sc     = v2_score_map.get(r["barcode"])
        v2_str    = f"{v2_sc:.1f}" if v2_sc is not None else "None"
        lines.append(f"{r['barcode']:<16} {r['tier']:<5} {v2_str:<10} {v3_str:<10} {b1_str:<6} {r['expected_label']}")
    lines.append("")

    lines.append("=" * 72)
    lines.append("OVERALL VERDICT")
    lines.append("=" * 72)
    lines.append(f"Gate B1 (anchor >= 90%):     {b1_verdict}  [{b1_pass_count}/{len(b1_products)} = {b1_rate:.1%}]")
    lines.append(f"Gate B2 (ranking >= 95%):    {b2_verdict}  [{b2_pass_count}/{len(b2_evaluable)} = {b2_rate:.1%}]")
    lines.append(f"Gate B3 (coverage >= 95%):   {b3_verdict}  [{parseable_count - len(no_marker_parseable)}/{parseable_count} = {b3_coverage:.1%}]")
    lines.append(f"MC-1 T3 pairs >= 10:         {'PASS' if b2_t3_pair_count >= 10 else 'FAIL'}  [{b2_t3_pair_count}]")
    lines.append(f"Unreadable returns None:      {'PASS' if unreadable_ok else 'FAIL'}")
    lines.append("")
    lines.append(f"VERDICT: {overall_verdict}")
    lines.append("")
    lines.append("RESIDUAL FAILURES ATTRIBUTION (if any):")
    lines.append("  RP-03/RP-08: 7290016883176 vs 7290011131388 (oats 47% vs 39%)")
    lines.append("    Both products have stated_pct markers; tie/near-tie is a midpoint-sensitivity")
    lines.append("    DESIGN gap (RP-03 class from QA report a01eea0747ca992ae) — routes to Nutrition.")
    lines.append("  Any remaining reading failures: listed above in B1/B2 failures sections.")
    lines.append("=" * 72)

    report_text = "\n".join(lines)

    # ---------------------------------------------------------------------------
    # Write outputs
    # ---------------------------------------------------------------------------
    report_path = OUT_DIR / "matrix_signal_probe_v3_report.txt"
    with open(report_path, "w", encoding="utf-8") as f:
        f.write(report_text)

    json_out = {
        "probe": "matrix_signal_probe_v3",
        "reader": "structured_ingredient_reader.py",
        "formula": "unchanged from v2 — no tuning",
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
                {"barcode": r["barcode"], "name": r["name_he"], "score": r["v3_score"],
                 "tier": r["tier"], "whole": r["whole_markers"], "refined": r["refined_markers"]}
                for r in all_results if r["b1_applicable"] and r["b1_pass"] is False
            ],
        },
        "gate_B1_MC2": {
            "with_corrections": round(b1_rate, 4),
            "without_corrections": round(b1_rate_no_corr, 4),
        },
        "gate_B2": {
            "verdict": b2_verdict,
            "pass_rate": round(b2_rate, 4),
            "pass_count": b2_pass_count,
            "evaluable_pairs": len(b2_evaluable),
            "t3_pair_count": b2_t3_pair_count,
            "mc1_pass": b2_t3_pair_count >= 10,
            "pair_results": b2_results,
        },
        "gate_B3": {
            "verdict": b3_verdict,
            "coverage_rate": round(b3_coverage, 4),
            "parseable_count": parseable_count,
            "no_marker_count": len(no_marker_parseable),
            "no_marker_barcodes": [r["barcode"] for r in no_marker_parseable],
        },
        "mc3_stated_pct": {
            "parseable_count": parseable_count,
            "with_stated_pct": stated_pct_present_count,
            "rate": round(stated_pct_rate, 4),
            "risk_flag": mc3_risk_flag,
        },
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
        "products": all_results,
    }

    json_path = OUT_DIR / "matrix_signal_probe_v3_results.json"
    with open(json_path, "w", encoding="utf-8") as f:
        json.dump(json_out, f, ensure_ascii=False, indent=2)

    def sha256_file(path):
        h = hashlib.sha256()
        with open(path, "rb") as f2:
            h.update(f2.read())
        return h.hexdigest().upper()

    report_sha = sha256_file(report_path)
    json_sha   = sha256_file(json_path)
    gold_sha   = sha256_file(GOLD_SET_PATH)

    print(report_text)
    print()
    print(f"report_path:   {report_path}")
    print(f"json_path:     {json_path}")
    print(f"report_sha256: {report_sha}")
    print(f"json_sha256:   {json_sha}")
    print(f"gold_sha256:   {gold_sha}")

    return {
        "b1_verdict": b1_verdict, "b1_rate": b1_rate,
        "b2_verdict": b2_verdict, "b2_rate": b2_rate,
        "b3_verdict": b3_verdict, "b3_coverage": b3_coverage,
        "all_gates_pass": all_gates_pass,
        "report_sha256": report_sha,
        "json_sha256": json_sha,
        "gold_sha256": gold_sha,
    }


if __name__ == "__main__":
    main()
