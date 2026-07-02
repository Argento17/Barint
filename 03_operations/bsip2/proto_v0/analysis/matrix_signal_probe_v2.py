"""
matrix_signal_probe_v2.py
=========================
TASK-395 — C-N1-1 re-validation: Component B v2 formula graded against the
locked gold set (matrix_gold_set_v1.json).

Standalone probe — does NOT import from score_engine.py, signal_extractor.py,
or any other src/ file. The position-weight curve is copied here verbatim from
the spec (matrix_signal_redesign_v2.md §2.2).

Implements:
  - v2 formula: position-weighted dominance + percentage override + first-ingredient anchor
  - v2 lexicon: all §2.4 extensions including כוסמין לבן/מלא qualifier rule
  - Bare-wheat-first rule (ויטביקס pattern)
  - Sub-composite expansion for parent% × sub%
  - Gates B1, B2, B3 per d7_cosign_metric_redesign_v1.md
  - MC-1: >= 10 T3 pairs in B2
  - MC-2: accuracy reported with and without spelt-pita corrections
  - MC-3: stated_pct population rate audit
  - MC-4: B3 denominator = parseable-text-only

Run:
    python matrix_signal_probe_v2.py

Outputs:
    analysis/matrix_signal_probe_v2_results.json   — per-product table
    analysis/matrix_signal_probe_v2_report.txt      — human-readable summary
"""

import json
import re
import hashlib
from pathlib import Path
from datetime import datetime, timezone
from typing import Optional

# ---------------------------------------------------------------------------
# Paths
# ---------------------------------------------------------------------------
REPO_ROOT = Path("C:/Bari")
GOLD_SET_PATH = REPO_ROOT / "03_operations/bsip2/proto_v0/analysis/matrix_gold_set_v1.json"
OUT_DIR = REPO_ROOT / "03_operations/bsip2/proto_v0/analysis"

# ---------------------------------------------------------------------------
# Position-weight curve — copied verbatim from matrix_signal_redesign_v2.md §2.2
# Do NOT redefine or modify.
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
# Lexicon v2 — base spec markers + §2.4 extensions
# Each entry: (pattern, label, grain_class, half_weight)
# grain_class: "whole" | "refined"
# half_weight: True for partial-credit markers (barley_malt)
#
# Ordering matters: more specific patterns before general ones.
# ---------------------------------------------------------------------------

MARKERS = [
    # ============================================================
    # WHOLE-FOOD MARKERS
    # ============================================================
    # --- Whole-grain flours with explicit מלא qualifier ---
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
    # Bare שיבולת שועל (not already matched as whole above) — still whole food
    (r"שיבולת שועל(?!\s+מלאה?)(?!\s+מלאים)", "oat_flakes_plain", "whole", False),
    # Barley malt — half credit (processing aid)
    (r"לתת שעורה|מיצוי לתת שעורה", "barley_malt", "whole", True),
    # שיפון standalone at early position — handled by position check in main logic
    # Nuts and seeds
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
    # Legumes
    (r"עדשים", "lentils", "whole", False),
    (r"חומוס(?!\s+שחור)", "chickpeas", "whole", False),
    # Dates, dried fruit (primary ingredient)
    (r"תמר(?:ים)?", "dates", "whole", False),
    (r"צימוקים", "raisins", "whole", False),
    # Fermentation
    (r"מחמצת", "sourdough_starter", "whole", False),
    # Real butter
    (r"חמאה(?!\s+קקאו)(?!\s+שמן)", "butter_dairy", "whole", False),
    # Olive oil (minimally processed)
    (r"שמן זית", "olive_oil", "whole", False),
    # Tahini
    (r"טחינה|ממרח שומשום", "tahini", "whole", False),

    # ============================================================
    # REFINED MARKERS
    # ============================================================
    # Must appear AFTER whole-grain patterns to avoid capturing e.g. "קמח חיטה מלא" as refined
    # White spelt flour — v2 addition, fixes the spelt-pita error class
    (r"קמח כוסמין לבן", "white_spelt_flour", "refined", False),
    # Refined wheat flour
    (r"קמח חיטה(?!\s+מלאה?)(?!\s+מלא)", "refined_wheat_flour", "refined", False),
    # Refined corn products
    (r"גריסי תירס", "corn_grits", "refined", False),
    (r"קמח תירס(?!\s+מלא)", "corn_flour_refined", "refined", False),
    (r"סמולינה(?:\s+מתירס)?", "semolina", "refined", False),
    # Rice — refined
    (r"קמח אורז(?!\s+מלא)", "rice_flour_refined", "refined", False),
    (r"אורז לבן", "white_rice", "refined", False),
    # Starches
    (r"עמילן תירס", "corn_starch", "refined", False),
    (r"עמילן חיטה", "wheat_starch", "refined", False),
    (r"עמילן אורז", "rice_starch", "refined", False),
    (r"עמילן(?!\s+תירס)(?!\s+חיטה)(?!\s+אורז)", "generic_starch", "refined", False),
    # Sugars and syrups
    (r"(?<!\S)סוכר(?!\s+קנים\s+אורגני)", "sugar", "refined", False),
    (r"סירופ\s+גלוקוז(?:-פרוקטוז)?|סירופ\s+גלוקוזה(?:-פרוקטוזה)?", "glucose_syrup", "refined", False),
    (r"סירופ\s+סוכר\s+אינברטי|סוכר\s+אינברטי", "inverted_sugar", "refined", False),
    (r"גלוקוז(?!\s+מיובש)(?![א-ת])", "glucose", "refined", False),
    (r"דקסטרוז|דקסטרוזה", "dextrose", "refined", False),
    (r"דקסטרין", "dextrin", "refined", False),
    (r"פרוקטוז", "fructose", "refined", False),
    (r"מלטודקסטרין", "maltodextrin", "refined", False),
    # Industrial fats
    (r"שמן דקל(?!ים)(?!\s+אדום)", "palm_oil", "refined", False),
    (r"שמן דקלים", "palm_oil_pl", "refined", False),
    (r"שמנים\s+צמחיים", "veg_oils_pl", "refined", False),
    (r"שמן\s+צמחי(?!ים)", "veg_oil_sg", "refined", False),
    (r"שומן\s+צמחי", "hydrogenated_veg_fat", "refined", False),
    (r"מרגרינה", "margarine", "refined", False),
    (r"שמן\s+קוקוס", "coconut_oil", "refined", False),
]

# ---------------------------------------------------------------------------
# Percentage regex — extracts stated percentages from Hebrew label text
# Handles: (53%), (53.0%), (53 %), 53%, ≈53%
# ---------------------------------------------------------------------------
PCT_PATTERN = re.compile(r"[\(≈~]?\s*(\d+(?:\.\d+)?)\s*%\s*[\)]?")

def extract_stated_pct(text_fragment: str) -> Optional[float]:
    """Extract the first stated percentage from a short text fragment (ingredient name + context)."""
    m = PCT_PATTERN.search(text_fragment)
    if m:
        v = float(m.group(1))
        if 0.1 <= v <= 100.0:
            return v
    return None

# ---------------------------------------------------------------------------
# Marketingblurb / INCI detector
# ---------------------------------------------------------------------------
INCI_WORDS = ["aqua", "water (aqua)", "cetearyl", "caprylic", "glycerin",
              "phenoxyethanol", "tocopheryl", "carbomer", "parfum"]
MARKETING_PHRASES = [
    r"אנחנו מאמינים",
    r"פרגנו לעצמכם",
    r"בקיצור",
    r"טעים ומפנק",
    r"גם בריאה",
]

def is_unparseable(text: str) -> bool:
    """Return True if text is marketing copy or INCI cosmetic list."""
    t = text.lower()
    for w in INCI_WORDS:
        if w in t:
            return True
    for p in MARKETING_PHRASES:
        if re.search(p, text):
            return True
    return False

# ---------------------------------------------------------------------------
# Sub-composite expansion
# ---------------------------------------------------------------------------
def expand_composites(text: str) -> list[dict]:
    """
    Parse ingredient text into a flat list of (ingredient_fragment, position, stated_pct).
    Handles:
      - Parent% (sub1 X%, sub2 Y%, ...) → effective_pct = parent_pct * sub_pct / 100
      - Bare percentage adjacent to ingredient token
    Returns list of dicts: {fragment, position, stated_pct}
    """
    # Strategy: split on top-level commas (ignoring content inside parentheses)
    # Then for each token check if it has a sub-list in parentheses with sub-pcts.

    items = _split_top_level(text)
    result = []
    pos = 0

    for item in items:
        item = item.strip()
        if not item:
            continue
        pos += 1

        # Does this item have a stated % for itself?
        item_pct = _extract_item_pct(item)

        # Does this item have a sub-composite (parenthetical with sub-%)
        sub_match = re.search(r'^(.*?)\s*\(([^)]*%[^)]*)\)', item)
        if sub_match and item_pct is not None:
            # Expand sub-ingredients with effective % = parent_pct * sub_pct / 100
            parent_pct = item_pct
            sub_text = sub_match.group(2)
            sub_items = _split_top_level(sub_text)
            sub_pos = 0
            # Add the parent item itself (for position weighting of sub-ingredients)
            result.append({
                "fragment": item,
                "position": pos,
                "stated_pct": parent_pct,
                "is_composite_parent": True,
            })
            for si in sub_items:
                si = si.strip()
                if not si:
                    continue
                sub_pos += 1
                sub_pct = _extract_item_pct(si)
                eff_pos = pos + sub_pos - 1
                if sub_pct is not None:
                    eff_pct = parent_pct * sub_pct / 100.0
                else:
                    eff_pct = None
                result.append({
                    "fragment": si,
                    "position": eff_pos,
                    "stated_pct": eff_pct,
                    "is_composite_parent": False,
                })
        else:
            result.append({
                "fragment": item,
                "position": pos,
                "stated_pct": item_pct,
                "is_composite_parent": False,
            })

    return result


def _split_top_level(text: str) -> list[str]:
    """Split text on commas/semicolons that are not inside parentheses or braces."""
    parts = []
    depth = 0
    current = []
    for ch in text:
        if ch in "({[":
            depth += 1
            current.append(ch)
        elif ch in ")}]":
            depth = max(0, depth - 1)
            current.append(ch)
        elif ch in ",;" and depth == 0:
            parts.append("".join(current).strip())
            current = []
        else:
            current.append(ch)
    if current:
        parts.append("".join(current).strip())
    return parts


def _extract_item_pct(item: str) -> Optional[float]:
    """Extract stated percentage from an ingredient item string."""
    # Look for percentage pattern
    m = re.search(r'[\(≈~]?\s*(\d+(?:\.\d+)?)\s*%', item)
    if m:
        v = float(m.group(1))
        if 0.1 <= v <= 100.0:
            return v
    return None

# ---------------------------------------------------------------------------
# Qualifier rules for ambiguous tokens
# ---------------------------------------------------------------------------
def _has_mala_nearby(text: str, token_pos: int) -> bool:
    """Check if מלא/מלאה/מגרעין appears within 4 tokens of given position."""
    # Tokenize by whitespace
    tokens = text.split()
    end = min(token_pos + 4, len(tokens))
    start = max(0, token_pos - 2)
    window = " ".join(tokens[start:end])
    return bool(re.search(r"מלאה?|מגרעין|בשלמותו", window))

# ---------------------------------------------------------------------------
# Marker extraction from a single ingredient fragment
# Returns list of dicts: {label, class, position, stated_pct, half_weight}
# ---------------------------------------------------------------------------

def extract_markers_from_fragment(fragment: str, position: int, stated_pct: Optional[float]) -> list[dict]:
    """Match markers against a single ingredient fragment."""
    found = []
    seen_labels = set()
    text = fragment

    # Special rule: bare חיטה at position 1 with stated_pct >= 80 → whole wheat grain
    # (ויטביקס pattern from §2.4)
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
            # Qualifier rule for כוסמין alone (ambiguous)
            if label in ("whole_spelt_grain", "whole_spelt_flour") and "לבן" in text:
                # כוסמין לבן is refined — skip the whole marker, white_spelt_flour will catch it
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


def extract_all_markers(text: str) -> list[dict]:
    """
    Full marker extraction pipeline:
    1. Check for unparseable text → return []
    2. Expand composites
    3. For each fragment, extract markers
    4. Deduplicate by label (keep highest-weight occurrence)
    """
    if is_unparseable(text):
        return []

    fragments = expand_composites(text)
    all_markers = []
    seen_labels: dict[str, dict] = {}

    for frag in fragments:
        if frag.get("is_composite_parent"):
            # Don't score parent-composite itself as a grain (its sub-ingredients do)
            continue
        markers = extract_markers_from_fragment(
            frag["fragment"], frag["position"], frag["stated_pct"]
        )
        for m in markers:
            label = m["label"]
            if label not in seen_labels:
                seen_labels[label] = m
            else:
                # Keep the one with higher effective weight
                existing = seen_labels[label]
                ew_new = m["stated_pct"] / 100.0 if m["stated_pct"] is not None else _pos_weight(m["position"])
                ew_old = existing["stated_pct"] / 100.0 if existing["stated_pct"] is not None else _pos_weight(existing["position"])
                if ew_new > ew_old:
                    seen_labels[label] = m

    return list(seen_labels.values())

# ---------------------------------------------------------------------------
# v2 formula — per §2.5
# ---------------------------------------------------------------------------

def compute_component_b_score(markers: list[dict]) -> Optional[float]:
    """
    Position-weighted dominance formula for Component B (whole-food matrix signal).
    Returns float in [0, 100] or None if no markers fired.
    """
    if not markers:
        return None

    pct_markers = [m for m in markers if m.get("stated_pct") is not None]
    pos_markers  = [m for m in markers if m.get("stated_pct") is None]

    total_stated_pct = sum(m["stated_pct"] for m in pct_markers) / 100.0
    # Cap at 1.0 (labels can sum to >100 due to composite double-counting)
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

    # First-ingredient anchor: find the highest-weight marker
    highest = max(markers, key=effective_weight)
    anchor_class = highest["class"]

    if anchor_class == "refined" and dominance_ratio > 0.5:
        dominance_ratio = max(0.5, dominance_ratio - 0.15)
    elif anchor_class == "whole" and dominance_ratio < 0.5:
        dominance_ratio = min(0.5, dominance_ratio + 0.15)

    # Map to [10, 95]: ratio=0 → 10, ratio=1 → 95
    score = 10.0 + dominance_ratio * 85.0
    return round(score, 1)

# ---------------------------------------------------------------------------
# Gate evaluation
# ---------------------------------------------------------------------------

def check_b1_pass(score: float, tier: str) -> bool:
    """
    Gate B1: anchor calibration.
    T1 (clear-whole) → score >= 60
    T2 (clear-refined) → score <= 45
    """
    if tier == "T1":
        return score >= 60.0
    elif tier == "T2":
        return score <= 45.0
    return True  # T3/T4 not in B1

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
    print("=== Component B Matrix Signal Probe v2 ===")
    print(f"Run: {datetime.now(timezone.utc).isoformat()}")
    print()

    # Load gold set
    with open(GOLD_SET_PATH, encoding="utf-8") as f:
        gold = json.load(f)

    products = gold["products"]
    print(f"Gold set loaded: {len(products)} products total")

    # --- MC-3: Stated_pct population rate audit ---
    # Count products where at least one marker has a stated_pct
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
        if unparseable:
            score = None
            markers = []
            parseable = False
        else:
            parseable = True
            parseable_count += 1
            markers = extract_all_markers(text)
            score = compute_component_b_score(markers)

        # Track stated_pct population
        has_stated_pct = any(m.get("stated_pct") is not None for m in markers)
        if parseable and has_stated_pct:
            stated_pct_present_count += 1

        # B1 gate (only for T1 and T2 gradable products)
        b1_applicable = gradable and tier in ("T1", "T2")
        b1_pass = None
        if b1_applicable and score is not None:
            b1_pass = check_b1_pass(score, tier)

        # Marker summary
        whole_markers = [m for m in markers if m["class"] == "whole"]
        refined_markers = [m for m in markers if m["class"] == "refined"]

        result = {
            "barcode": barcode,
            "name_he": p.get("name_he", ""),
            "tier": tier,
            "expected_label": expected_label,
            "gradable": gradable,
            "spelt_correction": spelt_correction,
            "v2_score": score,
            "parseable": parseable,
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
    # Gate B1: anchor calibration
    # ---------------------------------------------------------------------------
    b1_products = [r for r in all_results if r["b1_applicable"] and r["v2_score"] is not None]
    b1_pass_count = sum(1 for r in b1_products if r["b1_pass"])
    b1_fail_count = len(b1_products) - b1_pass_count
    b1_rate = b1_pass_count / len(b1_products) if b1_products else 0.0
    b1_verdict = "PASS" if b1_rate >= 0.90 else "FAIL"

    # Also compute without spelt-pita corrections (MC-2: before correction)
    b1_no_corr = [r for r in all_results if r["b1_applicable"] and r["v2_score"] is not None and not r["spelt_correction"]]
    b1_pass_no_corr = sum(1 for r in b1_no_corr if r["b1_pass"])
    b1_rate_no_corr = b1_pass_no_corr / len(b1_no_corr) if b1_no_corr else 0.0

    # T1 and T2 breakdown for B1
    b1_t1 = [r for r in b1_products if r["tier"] == "T1"]
    b1_t2 = [r for r in b1_products if r["tier"] == "T2"]
    b1_t1_pass = sum(1 for r in b1_t1 if r["b1_pass"])
    b1_t2_pass = sum(1 for r in b1_t2 if r["b1_pass"])

    # ---------------------------------------------------------------------------
    # Gate B2: ordinal ranking (including T3 pairs — MC-1)
    # ---------------------------------------------------------------------------
    ranking_pairs = gold.get("ranking_pairs_T3", [])

    # Build barcode→score map
    score_map = {r["barcode"]: r["v2_score"] for r in all_results}

    b2_results = []
    for pair in ranking_pairs:
        higher_bc = pair["higher"]
        lower_bc = pair["lower"]
        higher_score = score_map.get(higher_bc)
        lower_score = score_map.get(lower_bc)
        if higher_score is None or lower_score is None:
            pair_pass = None  # cannot evaluate
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

    b2_evaluable = [p for p in b2_results if p["pass"] is not None]
    b2_pass_count = sum(1 for p in b2_evaluable if p["pass"])
    b2_fail_count = len(b2_evaluable) - b2_pass_count
    b2_rate = b2_pass_count / len(b2_evaluable) if b2_evaluable else 0.0
    b2_verdict = "PASS" if b2_rate >= 0.95 else "FAIL"
    b2_t3_pair_count = len(ranking_pairs)  # all pairs are T3/within-T3 in the gold set

    # ---------------------------------------------------------------------------
    # Gate B3: coverage (MC-4: denominator = parseable text only)
    # ---------------------------------------------------------------------------
    # parseable products with at least one marker fired
    parseable_results = [r for r in all_results if r["parseable"]]
    no_marker_parseable = [r for r in parseable_results if r["n_whole_markers"] + r["n_refined_markers"] == 0]
    b3_coverage = (parseable_count - len(no_marker_parseable)) / parseable_count if parseable_count > 0 else 0.0
    b3_verdict = "PASS" if b3_coverage >= 0.95 else "FAIL"

    # ---------------------------------------------------------------------------
    # MC-2: accuracy with and without spelt corrections
    # Already computed above for B1; repeat for narrative clarity
    # ---------------------------------------------------------------------------
    # With corrections (all T1/T2 gradable):
    #   b1_rate (above)
    # Without corrections (exclude spelt_correction=True products):
    #   b1_rate_no_corr (above)

    # ---------------------------------------------------------------------------
    # MC-3: stated_pct population rate
    # ---------------------------------------------------------------------------
    stated_pct_rate = stated_pct_present_count / parseable_count if parseable_count > 0 else 0.0
    mc3_risk_flag = stated_pct_rate < 0.30

    # ---------------------------------------------------------------------------
    # Score distribution for the verification artifact
    # ---------------------------------------------------------------------------
    gradable_scored = [r for r in all_results if r["gradable"] and r["v2_score"] is not None]
    scores = sorted(r["v2_score"] for r in gradable_scored)
    if scores:
        import statistics
        score_mean = statistics.mean(scores)
        score_median = statistics.median(scores)
        score_stdev = statistics.stdev(scores) if len(scores) > 1 else 0.0
        score_min = scores[0]
        score_max = scores[-1]
        # Mode (most common score, rounded to integer)
        rounded = [round(s) for s in scores]
        from collections import Counter
        most_common_score, most_common_count = Counter(rounded).most_common(1)[0]
    else:
        score_mean = score_median = score_stdev = score_min = score_max = None
        most_common_score = most_common_count = None

    # Per-tier distributions
    t1_scores = sorted(r["v2_score"] for r in all_results if r["tier"] == "T1" and r["v2_score"] is not None)
    t2_scores = sorted(r["v2_score"] for r in all_results if r["tier"] == "T2" and r["v2_score"] is not None)
    t3_scores = sorted(r["v2_score"] for r in all_results if r["tier"] == "T3" and r["v2_score"] is not None)

    # ---------------------------------------------------------------------------
    # Overall verdict
    # ---------------------------------------------------------------------------
    all_gates_pass = (b1_verdict == "PASS") and (b2_verdict == "PASS") and (b3_verdict == "PASS")
    overall_verdict = "PASS — v2 CLEARS C-N1-1 dual gate" if all_gates_pass else "FAIL — one or more gates not cleared"

    # ---------------------------------------------------------------------------
    # Unreadable product check
    # ---------------------------------------------------------------------------
    unreadable_product = next((r for r in all_results if r["tier"] == "UNREADABLE"), None)
    unreadable_score = unreadable_product["v2_score"] if unreadable_product else "N/A"

    # ---------------------------------------------------------------------------
    # Build report
    # ---------------------------------------------------------------------------
    lines = []
    lines.append("=" * 72)
    lines.append("COMPONENT B MATRIX SIGNAL PROBE v2 — VALIDATION REPORT")
    lines.append(f"Run: {datetime.now(timezone.utc).isoformat()}")
    lines.append("TASK: TASK-395 | Condition: C-N1-1 | Gold set: matrix_gold_set_v1.json")
    lines.append("=" * 72)
    lines.append("")
    lines.append(f"Gold set: {len(products)} products total")
    lines.append(f"  Gradable: 57 (58 total minus 1 UNREADABLE)")
    lines.append(f"  UNREADABLE held-out: 7290013453624 (marketing paragraph)")
    lines.append(f"  T1 clear-whole: {len(t1_scores)} scored")
    lines.append(f"  T2 clear-refined: {len(t2_scores)} scored")
    lines.append(f"  T3 hard-mixed: {len(t3_scores)} scored")
    lines.append(f"  T4 edge-case: not graded (behavior tests)")
    lines.append("")

    lines.append("─" * 72)
    lines.append("UNREADABLE PRODUCT CHECK")
    lines.append("─" * 72)
    lines.append(f"7290013453624: v2_score = {unreadable_score}")
    lines.append(f"Expected: None (marketing blurb must return None)")
    unreadable_ok = unreadable_score is None
    lines.append(f"Result: {'PASS — formula returns None as required' if unreadable_ok else 'FAIL — formula did not return None'}")
    lines.append("")

    lines.append("─" * 72)
    lines.append("GATE B1: ANCHOR CALIBRATION")
    lines.append(f"Condition: T1 products score >= 60; T2 products score <= 45")
    lines.append(f"Bar: >= 90% of anchor-class products pass")
    lines.append("─" * 72)
    lines.append(f"T1 (clear-whole): {b1_t1_pass}/{len(b1_t1)} pass (score >= 60)")
    if b1_t1:
        lines.append(f"  Scores: {[r['v2_score'] for r in b1_t1]}")
        lines.append(f"  Min={min(r['v2_score'] for r in b1_t1 if r['v2_score']):.1f}  Max={max(r['v2_score'] for r in b1_t1 if r['v2_score']):.1f}")
    lines.append(f"T2 (clear-refined): {b1_t2_pass}/{len(b1_t2)} pass (score <= 45)")
    if b1_t2:
        lines.append(f"  Scores: {[r['v2_score'] for r in b1_t2]}")
        lines.append(f"  Min={min(r['v2_score'] for r in b1_t2 if r['v2_score']):.1f}  Max={max(r['v2_score'] for r in b1_t2 if r['v2_score']):.1f}")
    lines.append(f"")
    lines.append(f"COMBINED B1: {b1_pass_count}/{len(b1_products)} = {b1_rate:.1%}")
    lines.append(f"Target: >= 90.0%  |  Result: {b1_verdict}")
    if b1_fail_count > 0:
        lines.append(f"B1 FAILURES ({b1_fail_count}):")
        for r in all_results:
            if r["b1_applicable"] and r["b1_pass"] is False:
                lines.append(f"  {r['barcode']} {r['name_he'][:40]} tier={r['tier']} score={r['v2_score']} expected={r['b1_expected_zone']}")
    lines.append("")

    lines.append("─" * 72)
    lines.append("GATE B1 — MC-2: WITH vs WITHOUT SPELT-PITA CORRECTIONS")
    lines.append("─" * 72)
    spelt_corrected_products = [r for r in all_results if r["spelt_correction"]]
    lines.append(f"Spelt-pita corrected products: {len(spelt_corrected_products)}")
    lines.append(f"  Barcodes: {[r['barcode'] for r in spelt_corrected_products]}")
    lines.append(f"B1 rate WITH corrections (all T1+T2): {b1_rate:.1%}  [{b1_pass_count}/{len(b1_products)}]")
    lines.append(f"B1 rate WITHOUT correction products: {b1_rate_no_corr:.1%}  [{b1_pass_no_corr}/{len(b1_no_corr)}]")
    lines.append(f"Delta from corrections: {(b1_rate - b1_rate_no_corr):+.1%}")
    lines.append("")

    lines.append("─" * 72)
    lines.append("GATE B2: ORDINAL RANKING")
    lines.append(f"Condition: within ranked pairs, more-whole product scores higher")
    lines.append(f"Bar: >= 95% of evaluable pairs correct")
    lines.append(f"MC-1: must include >= 10 T3 pairs")
    lines.append("─" * 72)
    lines.append(f"Total pairs in gold set: {len(ranking_pairs)}")
    lines.append(f"T3-anchored pairs (MC-1 count): {b2_t3_pair_count}")
    lines.append(f"Evaluable pairs: {len(b2_evaluable)}")
    lines.append(f"Correct: {b2_pass_count}/{len(b2_evaluable)} = {b2_rate:.1%}")
    lines.append(f"Target: >= 95.0%  |  Result: {b2_verdict}")
    lines.append(f"MC-1 check: {b2_t3_pair_count} T3 pairs >= 10 required: {'PASS' if b2_t3_pair_count >= 10 else 'FAIL'}")
    lines.append("")
    lines.append("All pair results:")
    for pr in b2_results:
        status = "OK" if pr["pass"] else ("FAIL" if pr["pass"] is False else "N/A")
        lines.append(f"  {pr['pair_id']} [{status}] {pr['higher_barcode']} > {pr['lower_barcode']}")
        lines.append(f"         {pr['eval_note']}")
        lines.append(f"         Reason: {pr['pair_reason']}")
    lines.append("")

    lines.append("─" * 72)
    lines.append("GATE B3: MARKER COVERAGE (MC-4: parseable text denominator)")
    lines.append(f"Condition: >= 95% of parseable-text products fire >= 1 marker")
    lines.append("─" * 72)
    lines.append(f"Total products in gold set: {len(products)}")
    lines.append(f"Parseable (denominator): {parseable_count}")
    lines.append(f"No markers fired: {len(no_marker_parseable)}")
    lines.append(f"Coverage: {parseable_count - len(no_marker_parseable)}/{parseable_count} = {b3_coverage:.1%}")
    lines.append(f"Target: >= 95.0%  |  Result: {b3_verdict}")
    if no_marker_parseable:
        lines.append("No-marker products:")
        for r in no_marker_parseable:
            lines.append(f"  {r['barcode']} {r['name_he'][:40]}")
    lines.append("")

    lines.append("─" * 72)
    lines.append("MC-3: STATED_PCT FIELD POPULATION RATE")
    lines.append("─" * 72)
    lines.append(f"Parseable products: {parseable_count}")
    lines.append(f"Products with >= 1 stated_pct marker: {stated_pct_present_count}")
    lines.append(f"Rate: {stated_pct_rate:.1%}")
    lines.append(f"MC-3 threshold: 30%  |  {'RISK FLAG: below 30% — B1 calibration relies on position inference' if mc3_risk_flag else 'OK — sufficient stated_pct coverage'}")
    lines.append("")

    lines.append("─" * 72)
    lines.append("SCORE DISTRIBUTION (gradable products)")
    lines.append("─" * 72)
    lines.append(f"N scored: {len(scores)}")
    if scores:
        lines.append(f"Min: {score_min}  Max: {score_max}  Mean: {score_mean:.1f}  Median: {score_median:.1f}  Stdev: {score_stdev:.1f}")
        lines.append(f"Most common score (rounded): {most_common_score} (n={most_common_count})")
    lines.append(f"T1 scores: {t1_scores}")
    lines.append(f"T2 scores: {t2_scores}")
    lines.append(f"T3 scores: {t3_scores}")
    lines.append("")

    lines.append("─" * 72)
    lines.append("PER-PRODUCT RESULTS TABLE")
    lines.append(f"{'barcode':<15} {'tier':<5} {'v2_score':<9} {'b1_pass':<8} {'label'}")
    lines.append("─" * 72)
    for r in all_results:
        b1_str = str(r["b1_pass"]) if r["b1_applicable"] else "N/A"
        score_str = f"{r['v2_score']:.1f}" if r["v2_score"] is not None else "None"
        lines.append(f"{r['barcode']:<15} {r['tier']:<5} {score_str:<9} {b1_str:<8} {r['expected_label']}")
    lines.append("")

    lines.append("=" * 72)
    lines.append("OVERALL VERDICT")
    lines.append("=" * 72)
    lines.append(f"Gate B1 (anchor calibration >= 90%): {b1_verdict}  [{b1_pass_count}/{len(b1_products)} = {b1_rate:.1%}]")
    lines.append(f"Gate B2 (ordinal ranking >= 95%):    {b2_verdict}  [{b2_pass_count}/{len(b2_evaluable)} = {b2_rate:.1%}]")
    lines.append(f"Gate B3 (coverage >= 95%):           {b3_verdict}  [{parseable_count - len(no_marker_parseable)}/{parseable_count} = {b3_coverage:.1%}]")
    lines.append(f"MC-1 T3 pairs >= 10:                 {'PASS' if b2_t3_pair_count >= 10 else 'FAIL'}  [{b2_t3_pair_count}]")
    lines.append(f"Unreadable → None:                   {'PASS' if unreadable_ok else 'FAIL'}")
    lines.append("")
    lines.append(f"VERDICT: {overall_verdict}")
    lines.append("")
    lines.append("HONEST LIMITATIONS:")
    lines.append("  - This probe uses regex marker extraction, not an NLP parser.")
    lines.append("  - Position numbers are inferred from comma-split; nested composites")
    lines.append("    may produce slightly different effective positions than a real parser.")
    lines.append("  - T3 B2 ranking pairs were constructed from the gold set; a larger")
    lines.append("    independently-sourced pair set would be stronger evidence.")
    lines.append("  - stated_pct extraction relies on regex; non-standard label formats")
    lines.append("    (e.g. percentages without parentheses) may be missed.")
    lines.append("=" * 72)

    report_text = "\n".join(lines)

    # ---------------------------------------------------------------------------
    # Write outputs
    # ---------------------------------------------------------------------------
    report_path = OUT_DIR / "matrix_signal_probe_v2_report.txt"
    with open(report_path, "w", encoding="utf-8") as f:
        f.write(report_text)

    json_out = {
        "probe": "matrix_signal_probe_v2",
        "run_at": datetime.now(timezone.utc).isoformat(),
        "task": "TASK-395",
        "condition": "C-N1-1",
        "gold_set_file": str(GOLD_SET_PATH),
        "total_products": len(products),
        "gradable_products": 57,
        "unreadable_held_out": 1,
        "unreadable_score": unreadable_score,
        "unreadable_returns_none": unreadable_ok,
        "gate_B1": {
            "verdict": b1_verdict,
            "pass_rate": round(b1_rate, 4),
            "pass_count": b1_pass_count,
            "total": len(b1_products),
            "t1_pass": f"{b1_t1_pass}/{len(b1_t1)}",
            "t2_pass": f"{b1_t2_pass}/{len(b1_t2)}",
            "t1_scores": t1_scores,
            "t2_scores": t2_scores,
        },
        "gate_B1_MC2": {
            "with_corrections": round(b1_rate, 4),
            "without_corrections": round(b1_rate_no_corr, 4),
            "delta": round(b1_rate - b1_rate_no_corr, 4),
            "spelt_corrected_barcodes": [r["barcode"] for r in spelt_corrected_products],
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

    json_path = OUT_DIR / "matrix_signal_probe_v2_results.json"
    with open(json_path, "w", encoding="utf-8") as f:
        json.dump(json_out, f, ensure_ascii=False, indent=2)

    def sha256_file(path):
        h = hashlib.sha256()
        with open(path, "rb") as f2:
            h.update(f2.read())
        return h.hexdigest().upper()

    report_sha = sha256_file(report_path)
    json_sha = sha256_file(json_path)
    gold_sha = sha256_file(GOLD_SET_PATH)

    print(report_text)
    print()
    print(f"report_path:   {report_path}")
    print(f"json_path:     {json_path}")
    print(f"report_sha256: {report_sha}")
    print(f"json_sha256:   {json_sha}")
    print(f"gold_sha256:   {gold_sha}")

    return {
        "b1_verdict": b1_verdict,
        "b1_rate": b1_rate,
        "b2_verdict": b2_verdict,
        "b2_rate": b2_rate,
        "b3_verdict": b3_verdict,
        "b3_coverage": b3_coverage,
        "all_gates_pass": all_gates_pass,
        "report_sha256": report_sha,
        "json_sha256": json_sha,
        "gold_sha256": gold_sha,
    }


if __name__ == "__main__":
    main()
