"""
matrix_signal_probe_v4.py
=========================
TASK-395 — Component B v4 re-validation: fixes for QA-identified reading bugs R-1, R-2.
Probe version: v4. Formula unchanged from v2/v3.

Bugs fixed in v4 (relative to v3):
  R-1: Trailing percentage after closing bracket now captured by the shared reader
       (structured_ingredient_reader.py v4 fix). The parse_ingredients() function
       now scans the text after the last group's end for a bare percentage.
       Affected: 7290016883176 (47%), 7290011131388 (39%), 7290013433107 (50%),
                 7296073705550 (25% whole wheat after paren).

  R-2: Parent composite records (has_own_sub=True) no longer fire markers against
       the full raw text (which includes sub-composite content). Instead, the
       matchable text is reduced to the name portion only (text before the first
       group), preventing the parent from claiming sub-ingredient signals at the
       parent's inflated pct. Sub-records retain their correct effective_pct.
       Affected: 7290107647731 (דגנים 71%), 7290116537351 (קרם נוגט 48%),
                 7290011131975 (גרנולה 65%), RP-04 pairs.

  SPELT-CONSTRUCT: Lexicon extended to match construct form
       "קמח חיטת כוסמין מלא" as whole_spelt_flour (same signal as "קמח כוסמין מלא").
       Affected: 7290017947464.

  C-5: pct_basis label — fixed in structured_ingredient_reader.py.
       Bread-weight pct now correctly labeled pct_basis="bread" not "product".
       No score change; affects traceability/audit only.

What is NOT changed from v3:
  - Formula: compute_component_b_score() (identical)
  - Gate thresholds: B1 >= 90%, B2 >= 95%, B3 >= 95% (identical)
  - Gold set file: matrix_gold_set_v1.json (locked, unchanged)
  - _pos_weight() curve (identical)

Run:
    python matrix_signal_probe_v4.py

Outputs:
    analysis/matrix_signal_probe_v4_results.json
    analysis/matrix_signal_probe_v4_report.txt
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

# Import the shared reader (v4 — R-1 and C-5 fixes applied)
sys.path.insert(0, str(REPO_ROOT / "03_operations/bsip2/proto_v0/analysis"))
from structured_ingredient_reader import (
    parse_ingredients, is_unparseable, _extract_groups, _strip_groups
)

# ---------------------------------------------------------------------------
# Position-weight curve — IDENTICAL to v2/v3 (do not redefine)
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
# Lexicon — v3 PLUS spelt construct-form fix
# Change from v3: "קמח חיטת כוסמין מלא" added as whole_spelt_flour (construct form)
# ---------------------------------------------------------------------------
MARKERS = [
    (r"קמח חיטה מלאה?", "whole_wheat_flour", "whole", False),
    (r"חיטה מלאה", "whole_wheat_grain", "whole", False),
    # SPELT-CONSTRUCT fix: match "קמח חיטת כוסמין מלא" (construct form) as whole_spelt_flour
    # Must be checked BEFORE "קמח כוסמין מלא" so both patterns share the same label
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
# Helper: get the name-only portion of a record (text before first group)
# Used for R-2 fix: parent composite marker matching uses name-only text
# ---------------------------------------------------------------------------
def _name_only_text(record: dict) -> str:
    """
    Returns text before the first group for a record.
    For has_own_sub=True parent records, this strips the sub-composite content,
    preventing sub-ingredient names from firing markers at the parent's inflated pct.
    For non-composite records, returns the full raw text (unchanged behavior).
    """
    raw = record["raw"]
    if not record.get("has_own_sub"):
        return raw
    # Find the first group boundary and return only what's before it
    groups = _extract_groups(raw)
    if not groups:
        return raw
    # The name portion is everything before the first group
    name_end = groups[0]["start"]
    return raw[:name_end].strip()


# ---------------------------------------------------------------------------
# Marker extraction — from a structured ingredient record (v4)
# R-2 fix: parent composite records use name-only text for pattern matching
# ---------------------------------------------------------------------------

def extract_markers_from_record_v4(record: dict) -> list[dict]:
    """
    Match MARKERS against a structured ingredient record.

    v4 change from v3 (R-2 fix):
    - For parent composite records (has_own_sub=True), match patterns against
      the name-only text (text before the first group), NOT the full raw text.
      This prevents sub-ingredient names from firing markers at the parent's
      inflated pct (e.g. "אגוזי לוז" in nougat composite should NOT fire at
      the nougat's 48% — it should fire only on the sub-record with effective_pct).
    - For non-composite records (has_own_sub=False), behavior is unchanged.

    Uses record["qualifiers"] for qualifier-aware disambiguation (same as v3).
    Returns list of marker dicts.
    """
    # R-2 fix: use name-only text for composite parents
    text = _name_only_text(record)
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


def extract_all_markers_v4(text: str) -> list[dict]:
    """
    v4 marker extraction pipeline using structured_ingredient_reader (v4 fixes).
    1. Parse text into structured records via parse_ingredients()
    2. For each record, extract markers (R-2: parent composites use name-only text)
    3. Deduplicate by label (keep highest-weight occurrence)

    Key difference from v3:
    - Parent composite records (has_own_sub=True) contribute only their OWN name
      to marker matching (not their sub-composite content).
    - Sub-records retain correct effective_pct from the reader.
    - R-1 fix (in the reader): trailing pct after allergen paren now captured.
    """
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
# Formula — IDENTICAL to v2/v3 (no tuning)
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
# Gate helpers — IDENTICAL to v2/v3
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
    print("=== Component B Matrix Signal Probe v4 (R-1, R-2, spelt-construct, C-5 fixes) ===")
    print(f"Run: {datetime.now(timezone.utc).isoformat()}")
    print()

    with open(GOLD_SET_PATH, encoding="utf-8") as f:
        gold = json.load(f)

    products = gold["products"]
    print(f"Gold set: {len(products)} products")

    parseable_count = 0
    stated_pct_present_count = 0
    all_results = []

    # Load v3 results for comparison
    v3_score_map = {}
    v3_path = OUT_DIR / "matrix_signal_probe_v3_results.json"
    if v3_path.exists():
        try:
            with open(v3_path, encoding="utf-8") as fv3:
                v3_data = json.load(fv3)
            v3_score_map = {p["barcode"]: p.get("v3_score") for p in v3_data.get("products", [])}
        except Exception:
            pass

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
            markers = extract_all_markers_v4(text)
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

        v3_score = v3_score_map.get(barcode)

        result = {
            "barcode": barcode,
            "name_he": p.get("name_he", ""),
            "tier": tier,
            "expected_label": expected_label,
            "gradable": gradable,
            "spelt_correction": spelt_correction,
            "v3_score": v3_score,
            "v4_score": score,
            "parseable": parseable,
            "n_records": len(records),
            "n_whole_markers": len(whole_markers),
            "n_refined_markers": len(refined_markers),
            "whole_markers": [m["label"] for m in whole_markers],
            "refined_markers": [m["label"] for m in refined_markers],
            "marker_detail": [
                {"label": m["label"], "class": m["class"],
                 "position": m.get("position"), "stated_pct": m.get("stated_pct")}
                for m in markers
            ],
            "has_stated_pct": has_stated_pct,
            "b1_applicable": b1_applicable,
            "b1_pass": b1_pass,
            "b1_expected_zone": b1_expected_zone(tier),
        }
        all_results.append(result)

    # ---------------------------------------------------------------------------
    # Gate B1
    # ---------------------------------------------------------------------------
    b1_products = [r for r in all_results if r["b1_applicable"] and r["v4_score"] is not None]
    b1_pass_count = sum(1 for r in b1_products if r["b1_pass"])
    b1_fail_count = len(b1_products) - b1_pass_count
    b1_rate = b1_pass_count / len(b1_products) if b1_products else 0.0
    b1_verdict = "PASS" if b1_rate >= 0.90 else "FAIL"

    b1_no_corr = [r for r in all_results if r["b1_applicable"] and r["v4_score"] is not None and not r["spelt_correction"]]
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
    score_map = {r["barcode"]: r["v4_score"] for r in all_results}

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

    gradable_scored = [r for r in all_results if r["gradable"] and r["v4_score"] is not None]
    scores = sorted(r["v4_score"] for r in gradable_scored)
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

    t1_scores = sorted(r["v4_score"] for r in all_results if r["tier"] == "T1" and r["v4_score"] is not None)
    t2_scores = sorted(r["v4_score"] for r in all_results if r["tier"] == "T2" and r["v4_score"] is not None)
    t3_scores = sorted(r["v4_score"] for r in all_results if r["tier"] == "T3" and r["v4_score"] is not None)

    all_gates_pass = (b1_verdict == "PASS") and (b2_verdict == "PASS") and (b3_verdict == "PASS")
    overall_verdict = "PASS — v4 reading fixes clear all gates" if all_gates_pass else "FAIL — one or more gates not cleared"

    unreadable_product = next((r for r in all_results if r["tier"] == "UNREADABLE"), None)
    unreadable_score   = unreadable_product["v4_score"] if unreadable_product else "N/A"
    unreadable_ok      = unreadable_score is None

    # ---------------------------------------------------------------------------
    # Build report
    # ---------------------------------------------------------------------------
    lines = []
    lines.append("=" * 72)
    lines.append("COMPONENT B MATRIX SIGNAL PROBE v4 — R-1, R-2, SPELT-CONSTRUCT, C-5 FIXES")
    lines.append(f"Run: {datetime.now(timezone.utc).isoformat()}")
    lines.append("TASK: TASK-395 | Reader: structured_ingredient_reader.py (v4)")
    lines.append("Formula: UNCHANGED from v2/v3. Reading layer fixed only.")
    lines.append("=" * 72)
    lines.append("")
    lines.append(f"Gold set: {len(products)} products total")
    lines.append(f"  T1 clear-whole: {len(t1_scores)} scored")
    lines.append(f"  T2 clear-refined: {len(t2_scores)} scored")
    lines.append(f"  T3 hard-mixed: {len(t3_scores)} scored")
    lines.append("")

    lines.append("-" * 72)
    lines.append("UNREADABLE PRODUCT CHECK")
    lines.append(f"7290013453624: v4_score = {unreadable_score}")
    lines.append(f"Result: {'PASS' if unreadable_ok else 'FAIL'}")
    lines.append("")

    lines.append("-" * 72)
    lines.append("GATE B1: ANCHOR CALIBRATION")
    lines.append(f"Condition: T1 score >= 60; T2 score <= 45  |  Bar: >= 90%")
    lines.append("-" * 72)
    lines.append(f"T1 (clear-whole): {b1_t1_pass}/{len(b1_t1)} pass (score >= 60)")
    if b1_t1:
        lines.append(f"  Scores: {sorted(r['v4_score'] for r in b1_t1 if r['v4_score'])}")
    lines.append(f"T2 (clear-refined): {b1_t2_pass}/{len(b1_t2)} pass (score <= 45)")
    if b1_t2:
        lines.append(f"  Scores: {sorted(r['v4_score'] for r in b1_t2 if r['v4_score'])}")
    lines.append(f"COMBINED B1: {b1_pass_count}/{len(b1_products)} = {b1_rate:.1%}  |  Target >= 90%  |  {b1_verdict}")
    if b1_fail_count > 0:
        lines.append(f"B1 FAILURES ({b1_fail_count}):")
        for r in all_results:
            if r["b1_applicable"] and r["b1_pass"] is False:
                lines.append(f"  {r['barcode']} tier={r['tier']} v3={r['v3_score']} v4={r['v4_score']} expected={r['b1_expected_zone']}")
                lines.append(f"    whole_markers={r['whole_markers']}")
                lines.append(f"    refined_markers={r['refined_markers']}")
    lines.append("")

    lines.append("-" * 72)
    lines.append("GATE B1 — MC-2: WITH vs WITHOUT SPELT CORRECTIONS")
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
    lines.append("PER-PRODUCT RESULTS TABLE (barcode | tier | v3_score | v4_score | delta | b1 | label)")
    lines.append("-" * 72)
    lines.append(f"{'barcode':<16} {'tier':<5} {'v3_score':<10} {'v4_score':<10} {'delta':<8} {'b1':<6} label")
    lines.append("-" * 72)
    for r in all_results:
        b1_str = str(r["b1_pass"]) if r["b1_applicable"] else "N/A"
        v4_str = f"{r['v4_score']:.1f}" if r["v4_score"] is not None else "None"
        v3_sc  = r["v3_score"]
        v3_str = f"{v3_sc:.1f}" if v3_sc is not None else "None"
        if r["v4_score"] is not None and v3_sc is not None:
            delta = r["v4_score"] - v3_sc
            delta_str = f"{delta:+.1f}"
        else:
            delta_str = "N/A"
        lines.append(f"{r['barcode']:<16} {r['tier']:<5} {v3_str:<10} {v4_str:<10} {delta_str:<8} {b1_str:<6} {r['expected_label']}")
    lines.append("")

    # ---------------------------------------------------------------------------
    # Residual failure attribution
    # ---------------------------------------------------------------------------
    lines.append("=" * 72)
    lines.append("RESIDUAL FAILURES ATTRIBUTION")
    lines.append("=" * 72)

    b1_failures = [r for r in all_results if r["b1_applicable"] and r["b1_pass"] is False]
    b2_failures = [pr for pr in b2_results if pr["pass"] is False]

    if not b1_failures and not b2_failures:
        lines.append("No residual failures — all gates pass.")
    else:
        if b1_failures:
            lines.append(f"B1 failures ({len(b1_failures)}):")
            for r in b1_failures:
                lines.append(f"  {r['barcode']} tier={r['tier']} v4={r['v4_score']} — see attribution below")
        if b2_failures:
            lines.append(f"B2 failures ({len(b2_failures)}):")
            for pr in b2_failures:
                lines.append(f"  {pr['pair_id']}: {pr['higher_barcode']} vs {pr['lower_barcode']} — {pr['eval_note']}")
        lines.append("")
        lines.append("Attribution key: READING_BUG (which bug) vs FORMULA_GAP (routes to Nutrition)")
        lines.append("DO NOT relabel reading bugs as formula gaps.")
        lines.append("")
        # For each failure, classify reading vs formula
        lines.append("Detailed attribution:")
        # We will fill this in based on actual run results
        lines.append("  [Auto-generated from run — see B1/B2 failure details above]")
        lines.append("  Remaining failures: if R-1 fix is applied correctly, RP-03/RP-08 should")
        lines.append("  show: 7290016883176 oats 47% vs 7290011131371 oats 38% with nuts bonus.")
        lines.append("  If still inverted: classify as FORMULA_GAP (non-grain whole markers)")
        lines.append("  over-weighting) — routes to Nutrition.")
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
    lines.append("=" * 72)

    report_text = "\n".join(lines)

    # ---------------------------------------------------------------------------
    # Write outputs
    # ---------------------------------------------------------------------------
    report_path = OUT_DIR / "matrix_signal_probe_v4_report.txt"
    with open(report_path, "w", encoding="utf-8") as f:
        f.write(report_text)

    json_out = {
        "probe": "matrix_signal_probe_v4",
        "reader": "structured_ingredient_reader.py (v4: R-1, R-2, spelt-construct, C-5 fixes)",
        "formula": "unchanged from v2/v3 — no tuning",
        "fixes_applied": ["R-1: trailing pct after allergen paren", "R-2: parent composite marker skip",
                          "SPELT-CONSTRUCT: קמח חיטת כוסמין מלא as whole_spelt_flour",
                          "C-5: pct_basis=bread correctly labeled"],
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
                {"barcode": r["barcode"], "name": r["name_he"], "v3_score": r["v3_score"],
                 "v4_score": r["v4_score"], "tier": r["tier"],
                 "whole": r["whole_markers"], "refined": r["refined_markers"]}
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

    json_path = OUT_DIR / "matrix_signal_probe_v4_results.json"
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
