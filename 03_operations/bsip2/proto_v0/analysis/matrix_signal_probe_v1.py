"""
matrix_signal_probe_v1.py
=========================
TASK-395 — de-chain program: Component B validation
Standalone probe: does NOT import from score_engine.py, signal_extractor.py,
or any other src/ file. Pure self-contained analysis.

Measures whether the "whole-food matrix" signal (spec Section 2.2) can be
extracted reliably from real Hebrew ingredient text pulled from our direct
scrapes. Target: >=90% accuracy (condition C-N1-1 in d7_cosign_dechain_v1.md).

Run:
    python matrix_signal_probe_v1.py

Outputs:
    analysis/matrix_signal_probe_v1_results.json   — full product table
    analysis/matrix_signal_probe_v1_report.txt      — human-readable summary

Data sources (direct scrapes only, OFF banned):
  - 02_products/cakes_hard_cookies/bsip0_outputs/cakes_merged_bsip0_raw.json
  - 02_products/bread_retail_003/real_bread_retail_003_v1_20260525T194532_bsip0_raw.json
  - 02_products/breakfast_cereals/bsip0_outputs/cereals_bsip0_raw_20260605T154620.json
  - 03_operations/bsip2/proto_v0/outputs/products/*/bsip2_trace.json  (snack bars)

Ground-truth method: Rule-based heuristic + author's manual reading.
This script cannot fully replace a Hebrew speaker's audit. The audit table
is designed to be human-readable so the owner can spot-check every row.
Confidence labels on each decision are explicit (see CONFIDENCE note).

Extended lexicon: spec Section 2.2 defines a base lexicon. Where the spec
is thin or missing whole-food terms that clearly appear in the corpus, this
probe extends it and marks extensions as [EXTENDED]. These extensions should
be ratified by Nutrition Agent before engine implementation.
"""

import json
import re
import os
import sys
import hashlib
from pathlib import Path
from datetime import datetime

# ---------------------------------------------------------------------------
# Path configuration
# ---------------------------------------------------------------------------
REPO_ROOT = Path("C:/Bari")
CAKES_BSIP0 = REPO_ROOT / "02_products/cakes_hard_cookies/bsip0_outputs/cakes_merged_bsip0_raw.json"
BREAD_BSIP0 = REPO_ROOT / "02_products/bread_retail_003/real_bread_retail_003_v1_20260525T194532_bsip0_raw.json"
CEREALS_BSIP0 = REPO_ROOT / "02_products/breakfast_cereals/bsip0_outputs/cereals_bsip0_raw_20260605T154620.json"
SNACK_TRACES = REPO_ROOT / "03_operations/bsip2/proto_v0/outputs/products"
OUT_DIR = REPO_ROOT / "03_operations/bsip2/proto_v0/analysis"

# ---------------------------------------------------------------------------
# Lexicon — Component B per spec Section 2.2, with extensions
# ---------------------------------------------------------------------------
# Each entry: (pattern, label, spec_origin)
# spec_origin: "SPEC" = listed in spec; "EXTENDED" = added by this probe
# with justification, requires Nutrition Agent ratification.

REFINED_STARCH_MARKERS = [
    # --- SPEC-defined ---
    # "קמח חיטה" / "קמח" without whole-grain qualifier
    (r"קמח חיטה(?!\s*מלא)(?!\s*מלאה)", "refined_wheat_flour", "SPEC"),
    (r"(?<!\S)קמח(?!\s*(חיטה\s*מלא|חיטה\s*מלאה|מלא|מלאה|שיפון\s*מלא|כוסמין\s*מלא|כוסמת|שיבולת))", "plain_flour", "SPEC"),
    # Refined starch bases
    (r"קמח אורז(?!\s*מלא)", "rice_flour_refined", "SPEC"),
    (r"עמילן תירס", "corn_starch", "SPEC"),
    (r"עמילן חיטה", "wheat_starch", "SPEC"),
    # Sugar as first/second ingredient (positional check done separately)
    (r"(?<!\S)סוכר", "sugar", "SPEC"),
    # Industrial fat sources
    (r"שמן דקל(?!\s*אדום)", "palm_oil", "SPEC"),  # palm oil (not red palm = less processed)
    (r"שמן קוקוס", "coconut_oil", "SPEC"),
    (r"שמן צמחי(?!ים)", "unspecified_vegetable_oil_sg", "SPEC"),
    (r"שמנים צמחיים", "unspecified_vegetable_oils_pl", "SPEC"),
    # --- EXTENDED ---
    # These appear frequently in corpus, are structurally equivalent to spec items:
    (r"עמילן מעובד", "modified_starch", "EXTENDED"),    # E1414/E1442 etc — refined starch base
    (r"עמילן(?!\s*תירס)(?!\s*חיטה)", "plain_starch", "EXTENDED"),  # generic starch
    (r"סירופ גלוקוז", "glucose_syrup", "EXTENDED"),     # same structural function as sugar-first
    (r"סירופ גלוקוזה", "glucose_syrup_alt", "EXTENDED"),
    (r"סירופ גלוקוז-פרוקטוז", "glucose_fructose_syrup", "EXTENDED"),
    (r"סירופ גלוקוזה-פרוקטוזה", "glucose_fructose_syrup_alt", "EXTENDED"),
    (r"שומן צמחי", "hydrogenated_veg_fat", "EXTENDED"),  # partially hydrogenated = refined fat
    (r"שמן דקלים", "palm_oil_alt", "EXTENDED"),          # alternative spelling in corpus
]

WHOLE_FOOD_MARKERS = [
    # --- SPEC-defined ---
    # Nuts, seeds, legumes
    (r"אגוז|אגוזים", "nuts", "SPEC"),
    (r"שקד|שקדים", "almonds", "SPEC"),
    (r"גרעין(?:י)?(?:\s+(?:חמנייה|דלעת|פשתן|חמניה))?", "seeds_generic", "SPEC"),  # sunflower/pumpkin/flax seeds
    (r"עדשים", "lentils", "SPEC"),
    (r"חומוס(?!\s*שחור)", "chickpeas", "SPEC"),  # chickpeas (not the spread brand)
    # Whole grain tokens
    (r"דגנים מלאים", "whole_grain_generic", "SPEC"),
    (r"שיבולת שועל מלאה", "whole_oat", "SPEC"),
    (r"שיפון מלא", "whole_rye", "SPEC"),
    (r"חיטה מלאה", "whole_wheat", "SPEC"),
    # Whole fruit / dried fruit as primary ingredient
    (r"תמר(?:ים)?", "dates", "SPEC"),
    (r"צימוקים", "raisins", "SPEC"),
    (r"ענב(?:ים)?", "grapes", "SPEC"),  # fresh/dried grapes
    # Fermentation markers
    (r"מחמצת", "sourdough_starter", "SPEC"),
    (r"חמאה(?!\s*קקאו)(?!\s*שמן)", "butter_dairy", "SPEC"),  # real butter (not cocoa butter/oil)
    (r"תסיסה", "fermentation_process", "SPEC"),
    (r"חמץ", "leavened_fermented", "SPEC"),
    # --- EXTENDED ---
    # Clearly whole-food ingredients appearing in corpus that spec omits:
    (r"שומשום", "sesame_seeds", "EXTENDED"),          # whole sesame seeds — clearly whole food
    (r"פשתן|גרעיני פשתן", "flax_seeds", "EXTENDED"),  # flax seeds
    (r"צ'יה|צ'יה|צ'יה|chia", "chia_seeds", "EXTENDED"),  # chia seeds
    (r"קינואה", "quinoa", "EXTENDED"),
    (r"כוסמת", "buckwheat", "EXTENDED"),               # already in existing WHOLE_GRAIN list
    (r"כוסמין", "spelt", "EXTENDED"),                  # inherently whole in Israeli usage
    (r"אורז מלא", "whole_rice", "EXTENDED"),
    (r"קמח חיטה מלא", "whole_wheat_flour", "EXTENDED"),
    (r"קמח שיבולת שועל", "oat_flour", "EXTENDED"),     # structural oat — less refined than wheat flour
    (r"שיבולת שועל(?!\s*מלאה)", "oat_flakes_plain", "EXTENDED"),  # plain oat (still whole food)
    (r"בוטנים|בוטן", "peanuts", "EXTENDED"),
    (r"פיסטוק|פיסטוקים", "pistachios", "EXTENDED"),
    (r"קשיו", "cashews", "EXTENDED"),
    (r"אפרסמון|פרי(?:ים)?\s+יבש(?:ים)?", "dried_fruit", "EXTENDED"),  # dried fruit
    (r"אוכמניות|חמוציות|קרנברי", "berries_dried", "EXTENDED"),
    (r"פפריקה(?!\s+מיצוי)(?!\s+אבקת)(?!\s+צבע)", "paprika_spice", "EXTENDED"),  # spice (whole-food)
    (r"שמן זית", "olive_oil", "EXTENDED"),  # cold-pressed olive oil = minimally processed
    (r"טחינה|ממרח שומשום", "tahini", "EXTENDED"),  # tahini = whole food (sesame paste)
    (r"תרבויות|תרבויות חיות|מחמצת|שמרים טבעיים", "live_cultures", "EXTENDED"),
]

# ---------------------------------------------------------------------------
# Spec formula (Section 2.2)
# ---------------------------------------------------------------------------
def count_refined_markers(text: str) -> tuple[int, list[dict]]:
    """Count distinct refined-starch marker types that fire in the text."""
    if not text:
        return 0, []
    fired = []
    seen_labels = set()
    for pattern, label, origin in REFINED_STARCH_MARKERS:
        if re.search(pattern, text, re.IGNORECASE):
            if label not in seen_labels:
                fired.append({"pattern": pattern, "label": label, "origin": origin})
                seen_labels.add(label)
    return len(fired), fired


def count_whole_food_markers(text: str) -> tuple[int, list[dict]]:
    """Count distinct whole-food complexity marker types that fire in the text."""
    if not text:
        return 0, []
    fired = []
    seen_labels = set()
    for pattern, label, origin in WHOLE_FOOD_MARKERS:
        if re.search(pattern, text, re.IGNORECASE):
            if label not in seen_labels:
                fired.append({"pattern": pattern, "label": label, "origin": origin})
                seen_labels.add(label)
    return len(fired), fired


def compute_matrix_score(n_refined: int, n_whole: int) -> tuple[float, int]:
    """Apply spec formula. Returns (raw_balance, clamped_score)."""
    balance = n_whole - n_refined
    raw = 50 + (balance * 12)
    clamped = max(10, min(95, raw))
    return balance, clamped


def infer_class(matrix_score: float, n_refined: int, n_whole: int) -> str:
    """
    Classify the product into whole-food-present (WFP) vs refined-dominant (RD)
    based on the matrix signal.

    Classification logic:
      WFP: matrix_score >= 50 (whole markers >= refined markers)
      RD:  matrix_score < 50  (refined markers dominate)
      AMBIGUOUS: n_refined == n_whole and both > 0 (exact tie with non-zero counts)
    """
    if n_refined == 0 and n_whole == 0:
        return "UNKNOWN"  # no markers fired — cannot classify
    if n_refined == n_whole and n_refined > 0:
        return "AMBIGUOUS"
    if matrix_score >= 50:
        return "WFP"  # whole-food-present
    return "RD"  # refined-dominant


def sugar_is_lead(text: str) -> bool:
    """Check if sugar appears as first or second listed ingredient (positional signal)."""
    if not text:
        return False
    # Normalize: strip leading "רכיבים:" header
    normalized = re.sub(r"^רכיבים[:\s]+", "", text.strip(), flags=re.IGNORECASE)
    # Split on commas or semicolons to get ordered items
    items = [i.strip() for i in re.split(r"[,;]", normalized) if i.strip()]
    for item in items[:2]:
        if re.search(r"(?<!\S)סוכר", item, re.IGNORECASE):
            return True
    return False

# ---------------------------------------------------------------------------
# Data loaders
# ---------------------------------------------------------------------------

def load_cakes(path: Path) -> list[dict]:
    """Load cakes_hard_cookies bsip0 raw file."""
    with open(path, encoding="utf-8") as f:
        data = json.load(f)
    products = []
    for p in data.get("products", []):
        ing = p.get("ingredients_raw", "") or ""
        if not ing.strip():
            continue
        products.append({
            "barcode": str(p.get("barcode", "")),
            "name_he": p.get("name_he", ""),
            "brand": p.get("brand", ""),
            "category": "cakes_hard_cookies",
            "source": "cakes_merged_bsip0_raw.json",
            "ingredients_text": ing,
        })
    return products


def load_bread(path: Path) -> list[dict]:
    """Load bread bsip0 raw array."""
    with open(path, encoding="utf-8") as f:
        data = json.load(f)
    products = []
    for p in data:
        ing = p.get("ingredients_raw", "") or ""
        if not ing.strip():
            continue
        products.append({
            "barcode": str(p.get("barcode", "")),
            "name_he": p.get("name_he", ""),
            "brand": p.get("brand", ""),
            "category": "bread",
            "source": "real_bread_retail_003_v1_bsip0_raw.json",
            "ingredients_text": ing,
        })
    return products


def load_cereals(path: Path) -> list[dict]:
    """Load cereals bsip0 raw array."""
    with open(path, encoding="utf-8") as f:
        data = json.load(f)
    products = []
    for p in data:
        ing = p.get("ingredients_raw", "") or ""
        if not ing.strip():
            continue
        products.append({
            "barcode": str(p.get("barcode", "")),
            "name_he": p.get("name_he", ""),
            "brand": p.get("brand", ""),
            "category": "cereals_granola",
            "source": "cereals_bsip0_raw_20260605T154620.json",
            "ingredients_text": ing,
        })
    return products


def load_snack_traces(traces_dir: Path) -> list[dict]:
    """Load snack bar products from bsip2_trace files (ingredient_list)."""
    products = []
    for trace_path in traces_dir.glob("*/bsip2_trace.json"):
        with open(trace_path, encoding="utf-8") as f:
            data = json.load(f)
        ing_list = data.get("L1_observed_signals", {}).get("ingredient_list", [])
        if not ing_list:
            continue
        # Reconstruct text from list (join with comma for pattern matching)
        ing_text = ", ".join(str(i) for i in ing_list)
        products.append({
            "barcode": str(data.get("input_reference", {}).get("barcode", "")),
            "name_he": data.get("input_reference", {}).get("product_name_he", ""),
            "brand": data.get("input_reference", {}).get("brand", ""),
            "category": "snack_bar_granola",
            "source": f"bsip2_trace:{trace_path.parent.name}",
            "ingredients_text": ing_text,
        })
    return products

# ---------------------------------------------------------------------------
# Ground-truth heuristic
# ---------------------------------------------------------------------------
# Since we cannot run a full expert-panel, this probe uses a rule-based
# "expected class" heuristic derived from:
#   (a) Category membership (bread, cereals = higher expected WFP rate)
#   (b) Product name signals (name keywords strongly predict class)
#   (c) Ingredient text structure (pure refined vs clearly mixed)
#
# This is NOT a gold-standard ground truth. It is labeled "HEURISTIC" in
# the output. A Hebrew reader must audit disagreements.

WHOLE_FOOD_NAME_SIGNALS = [
    r"מלא", r"כוסמין", r"שיפון", r"שיבולת שועל",
    r"גרנולה", r"מוזלי", r"כוסמת", r"אורז מלא",
    r"ללא גלוטן.*קינואה", r"פרי", r"אגוז", r"שקד",
    r"עדשים", r"קרקר.*כוסמין", r"לחם מחמצת",
]

REFINED_NAME_SIGNALS = [
    r"עוגיות?\s+שוקולד", r"ביסקוויט", r"וופל",
    r"פינוק", r"חטיף\s+(?:קרוגר|ממתק)", r"ופל",
    r"עוגה\s*(?:שוקולד|קרמל|וניל)", r"בורקס",
    r"רוגלך", r"קרקר.*(?:חיטה|מלח)",
]

def estimate_expected_class(name_he: str, category: str, ingredients_text: str) -> tuple[str, str]:
    """
    Estimate the expected class from category + name signals.
    Returns (expected_class, confidence) where:
      expected_class: "WFP" / "RD" / "MIXED" / "UNKNOWN"
      confidence: "HIGH" / "MEDIUM" / "LOW"

    HIGH: Strong name signal pointing to one class
    MEDIUM: Category default with some corroboration
    LOW: No strong signal — cannot reliably estimate
    """
    name = name_he or ""

    for sig in WHOLE_FOOD_NAME_SIGNALS:
        if re.search(sig, name, re.IGNORECASE):
            return "WFP", "HIGH"

    for sig in REFINED_NAME_SIGNALS:
        if re.search(sig, name, re.IGNORECASE):
            return "RD", "HIGH"

    # Category defaults with medium confidence
    if category == "bread":
        # Bread is mixed: sourdough/whole = WFP, plain white bread = RD
        # Default to MIXED since we can't distinguish from name alone
        return "MIXED", "MEDIUM"

    if category == "cereals_granola":
        # Most cereals contain at least some oats/whole grain → lean WFP
        return "WFP", "MEDIUM"

    if category == "snack_bar_granola":
        # Snack bars are genuinely mixed — granola bars = WFP, wafer bars = RD
        return "MIXED", "MEDIUM"

    if category == "cakes_hard_cookies":
        # Cookies/cakes: default refined unless name says otherwise
        return "RD", "MEDIUM"

    return "UNKNOWN", "LOW"

# ---------------------------------------------------------------------------
# Main analysis
# ---------------------------------------------------------------------------

def analyze_product(p: dict) -> dict:
    """Run the Component B analysis on a single product."""
    text = p["ingredients_text"]

    n_refined, refined_fired = count_refined_markers(text)
    n_whole, whole_fired = count_whole_food_markers(text)
    balance, matrix_score = compute_matrix_score(n_refined, n_whole)
    inferred = infer_class(matrix_score, n_refined, n_whole)
    sugar_lead = sugar_is_lead(text)
    expected, exp_confidence = estimate_expected_class(p["name_he"], p["category"], text)

    # Judgment: does inferred class match expected?
    if expected in ("WFP", "RD"):
        agrees = (inferred == expected)
        # AMBIGUOUS inference vs clear expectation = disagree
        if inferred in ("AMBIGUOUS", "UNKNOWN"):
            agrees = False
    elif expected == "MIXED":
        # Mixed products can go either way — flag for manual review
        agrees = None  # None = requires manual inspection
    else:
        agrees = None

    # Marker composition note
    extended_refined = [m for m in refined_fired if m["origin"] == "EXTENDED"]
    extended_whole = [m for m in whole_fired if m["origin"] == "EXTENDED"]

    return {
        "barcode": p["barcode"],
        "name_he": p["name_he"],
        "brand": p["brand"],
        "category": p["category"],
        "source": p["source"],
        "ingredients_text": text[:300] + ("…" if len(text) > 300 else ""),
        "n_refined": n_refined,
        "n_whole": n_whole,
        "matrix_balance": balance,
        "matrix_score": matrix_score,
        "inferred_class": inferred,
        "sugar_is_lead_ingredient": sugar_lead,
        "refined_markers_fired": [m["label"] for m in refined_fired],
        "whole_markers_fired": [m["label"] for m in whole_fired],
        "extended_refined_count": len(extended_refined),
        "extended_whole_count": len(extended_whole),
        "expected_class_heuristic": expected,
        "expected_confidence": exp_confidence,
        "agrees_with_expected": agrees,
        "needs_manual_review": (agrees is None or exp_confidence == "LOW"),
        "failure_mode": classify_failure_mode(
            inferred, expected, exp_confidence, n_refined, n_whole, text
        ),
    }


def classify_failure_mode(inferred: str, expected: str, exp_conf: str,
                           n_refined: int, n_whole: int, text: str) -> str | None:
    """Tag likely failure modes for manual review prioritization."""
    if n_refined == 0 and n_whole == 0:
        return "NO_MARKERS_FIRED"
    if inferred == "UNKNOWN":
        return "UNKNOWN_SIGNAL"
    if expected == "MIXED":
        return "GENUINELY_MIXED"
    if exp_conf == "LOW":
        return "EXPECTATION_UNCERTAIN"
    if inferred != expected and expected in ("WFP", "RD"):
        if n_refined > 0 and n_whole > 0:
            return "MIXED_MARKERS_WRONG_DIRECTION"
        if n_refined == 0 and expected == "RD":
            return "MISSED_REFINED_MARKERS"
        if n_whole == 0 and expected == "WFP":
            return "MISSED_WHOLE_FOOD_MARKERS"
    return None


def main():
    print("=== Component B Matrix Signal Probe v1 ===")
    print(f"Run timestamp: {datetime.utcnow().isoformat()}Z")
    print()

    # Load all corpora
    print("Loading corpus data...")
    all_products = []

    if CAKES_BSIP0.exists():
        cakes = load_cakes(CAKES_BSIP0)
        print(f"  cakes_hard_cookies: {len(cakes)} products with ingredient text")
        all_products.extend(cakes)
    else:
        print(f"  WARNING: {CAKES_BSIP0} not found — skipping")

    if BREAD_BSIP0.exists():
        bread = load_bread(BREAD_BSIP0)
        print(f"  bread: {len(bread)} products with ingredient text")
        all_products.extend(bread)
    else:
        print(f"  WARNING: {BREAD_BSIP0} not found — skipping")

    if CEREALS_BSIP0.exists():
        cereals = load_cereals(CEREALS_BSIP0)
        print(f"  cereals_granola: {len(cereals)} products with ingredient text")
        all_products.extend(cereals)
    else:
        print(f"  WARNING: {CEREALS_BSIP0} not found — skipping")

    if SNACK_TRACES.exists():
        snacks = load_snack_traces(SNACK_TRACES)
        print(f"  snack_bar_granola: {len(snacks)} products with ingredient text")
        all_products.extend(snacks)
    else:
        print(f"  WARNING: {SNACK_TRACES} not found — skipping")

    print(f"\nTotal corpus: {len(all_products)} products")
    print()

    # Run analysis
    print("Running matrix signal extraction...")
    results = [analyze_product(p) for p in all_products]

    # ---------------------------------------------------------------------------
    # Accuracy measurement
    # ---------------------------------------------------------------------------
    # Split by expectation confidence
    high_conf = [r for r in results if r["expected_confidence"] == "HIGH" and r["expected_class_heuristic"] in ("WFP", "RD")]
    med_conf = [r for r in results if r["expected_confidence"] == "MEDIUM" and r["expected_class_heuristic"] in ("WFP", "RD")]
    mixed = [r for r in results if r["expected_class_heuristic"] == "MIXED"]
    unknown = [r for r in results if r["expected_confidence"] == "LOW"]

    # Accuracy on high-confidence expected classes only (most defensible)
    high_correct = [r for r in high_conf if r["agrees_with_expected"] is True]
    high_wrong = [r for r in high_conf if r["agrees_with_expected"] is False]
    high_acc = len(high_correct) / len(high_conf) if high_conf else 0

    # Accuracy on medium-confidence expected classes
    med_correct = [r for r in med_conf if r["agrees_with_expected"] is True]
    med_wrong = [r for r in med_conf if r["agrees_with_expected"] is False]
    med_acc = len(med_correct) / len(med_conf) if med_conf else 0

    # Combined accuracy over all non-unknown/non-mixed
    all_clearcut = high_conf + med_conf
    all_correct = [r for r in all_clearcut if r["agrees_with_expected"] is True]
    combined_acc = len(all_correct) / len(all_clearcut) if all_clearcut else 0

    # No-marker-fire rate
    no_markers = [r for r in results if r["failure_mode"] == "NO_MARKERS_FIRED"]
    no_marker_rate = len(no_markers) / len(results) if results else 0

    # Failure mode distribution
    failure_modes: dict[str, int] = {}
    for r in results:
        fm = r.get("failure_mode") or "OK"
        failure_modes[fm] = failure_modes.get(fm, 0) + 1

    # Category breakdown
    cats = {}
    for r in results:
        c = r["category"]
        if c not in cats:
            cats[c] = {"total": 0, "high_conf_correct": 0, "high_conf_wrong": 0,
                       "med_conf_correct": 0, "med_conf_wrong": 0,
                       "no_markers": 0, "mixed": 0, "unknown": 0}
        cats[c]["total"] += 1
        if r["expected_confidence"] == "HIGH" and r["expected_class_heuristic"] in ("WFP", "RD"):
            if r["agrees_with_expected"]:
                cats[c]["high_conf_correct"] += 1
            else:
                cats[c]["high_conf_wrong"] += 1
        elif r["expected_confidence"] == "MEDIUM" and r["expected_class_heuristic"] in ("WFP", "RD"):
            if r["agrees_with_expected"]:
                cats[c]["med_conf_correct"] += 1
            else:
                cats[c]["med_conf_wrong"] += 1
        elif r["expected_class_heuristic"] == "MIXED":
            cats[c]["mixed"] += 1
        elif r["expected_confidence"] == "LOW":
            cats[c]["unknown"] += 1
        if r["failure_mode"] == "NO_MARKERS_FIRED":
            cats[c]["no_markers"] += 1

    # Extended lexicon usage stats
    products_using_extended_refined = sum(1 for r in results if r["extended_refined_count"] > 0)
    products_using_extended_whole = sum(1 for r in results if r["extended_whole_count"] > 0)

    # Inferred class distribution
    class_dist: dict[str, int] = {}
    for r in results:
        ic = r["inferred_class"]
        class_dist[ic] = class_dist.get(ic, 0) + 1

    # Marker frequency tables
    refined_freq: dict[str, int] = {}
    whole_freq: dict[str, int] = {}
    for r in results:
        for m in r["refined_markers_fired"]:
            refined_freq[m] = refined_freq.get(m, 0) + 1
        for m in r["whole_markers_fired"]:
            whole_freq[m] = whole_freq.get(m, 0) + 1

    # ---------------------------------------------------------------------------
    # Build output report
    # ---------------------------------------------------------------------------
    report_lines = []
    report_lines.append("=" * 72)
    report_lines.append("COMPONENT B MATRIX SIGNAL PROBE — VALIDATION REPORT v1")
    report_lines.append(f"Run: {datetime.utcnow().isoformat()}Z")
    report_lines.append("=" * 72)
    report_lines.append("")
    report_lines.append("TASK: TASK-395 de-chain program — Component B label-derivability validation")
    report_lines.append("CONDITION TO CLEAR: C-N1-1 >= 90% accuracy before NOVA lookup deactivation")
    report_lines.append("")
    report_lines.append(f"CORPUS TOTAL: {len(results)} products with Hebrew ingredient text")
    report_lines.append("")

    report_lines.append("─" * 72)
    report_lines.append("ACCURACY RESULTS")
    report_lines.append("─" * 72)
    report_lines.append("")
    report_lines.append("Ground-truth basis: rule-based heuristic from product name + category.")
    report_lines.append("HIGH-confidence = strong name signal (e.g. 'מלא', 'גרנולה', 'עוגיות שוקולד').")
    report_lines.append("MEDIUM-confidence = category default with weaker corroboration.")
    report_lines.append("NOT a gold standard — requires Hebrew reader spot-check of failure cases.")
    report_lines.append("")
    report_lines.append(f"HIGH-confidence subset: {len(high_conf)} products")
    report_lines.append(f"  Correct: {len(high_correct)} | Wrong: {len(high_wrong)}")
    report_lines.append(f"  Accuracy: {high_acc:.1%}")
    report_lines.append("")
    report_lines.append(f"MEDIUM-confidence subset: {len(med_conf)} products")
    report_lines.append(f"  Correct: {len(med_correct)} | Wrong: {len(med_wrong)}")
    report_lines.append(f"  Accuracy: {med_acc:.1%}")
    report_lines.append("")
    report_lines.append(f"MIXED (genuinely ambiguous, both classes expected): {len(mixed)}")
    report_lines.append(f"EXPECTATION-UNKNOWN (low-confidence heuristic): {len(unknown)}")
    report_lines.append("")
    report_lines.append(f"COMBINED accuracy (HIGH + MEDIUM): {combined_acc:.1%}  [{len(all_correct)}/{len(all_clearcut)}]")
    report_lines.append("")

    target = 0.90
    verdict = "PASS" if combined_acc >= target else "FAIL"
    report_lines.append(f"TARGET: >= {target:.0%}")
    report_lines.append(f"VERDICT: {verdict} ({combined_acc:.1%} combined, {high_acc:.1%} high-conf)")
    report_lines.append("")
    if verdict == "FAIL":
        gap = target - combined_acc
        report_lines.append(f"GAP TO TARGET: {gap:.1%} — {int(gap * len(all_clearcut))} additional")
        report_lines.append("  correct classifications needed to clear C-N1-1.")
        report_lines.append("")

    report_lines.append("─" * 72)
    report_lines.append("CATEGORY BREAKDOWN")
    report_lines.append("─" * 72)
    for cat, cd in cats.items():
        hc_total = cd["high_conf_correct"] + cd["high_conf_wrong"]
        mc_total = cd["med_conf_correct"] + cd["med_conf_wrong"]
        hc_acc = cd["high_conf_correct"] / hc_total if hc_total else None
        mc_acc = cd["med_conf_correct"] / mc_total if mc_total else None
        acc_str = ""
        if hc_acc is not None:
            acc_str += f"H:{hc_acc:.0%}[{cd['high_conf_correct']}/{hc_total}] "
        if mc_acc is not None:
            acc_str += f"M:{mc_acc:.0%}[{cd['med_conf_correct']}/{mc_total}] "
        report_lines.append(
            f"  {cat:<28} total={cd['total']:3d}  "
            f"no_markers={cd['no_markers']:2d}  mixed={cd['mixed']:2d}  {acc_str}"
        )
    report_lines.append("")

    report_lines.append("─" * 72)
    report_lines.append("NO-MARKER-FIRE ANALYSIS (critical failure class)")
    report_lines.append("─" * 72)
    report_lines.append(f"Products where ZERO markers fired: {len(no_markers)} / {len(results)} ({no_marker_rate:.1%})")
    report_lines.append("")
    if no_markers:
        report_lines.append("Sample no-marker products (first 15):")
        for r in no_markers[:15]:
            report_lines.append(f"  [{r['category']}] {r['barcode']} {r['name_he'][:40]}")
            report_lines.append(f"    TEXT: {r['ingredients_text'][:100]}")
    report_lines.append("")

    report_lines.append("─" * 72)
    report_lines.append("FAILURE MODE DISTRIBUTION")
    report_lines.append("─" * 72)
    for fm, count in sorted(failure_modes.items(), key=lambda x: -x[1]):
        pct = count / len(results) * 100 if results else 0
        report_lines.append(f"  {fm:<40} {count:4d} ({pct:.1f}%)")
    report_lines.append("")

    report_lines.append("─" * 72)
    report_lines.append("INFERRED CLASS DISTRIBUTION")
    report_lines.append("─" * 72)
    for cls, count in sorted(class_dist.items(), key=lambda x: -x[1]):
        pct = count / len(results) * 100 if results else 0
        report_lines.append(f"  {cls:<15} {count:4d} ({pct:.1f}%)")
    report_lines.append("")

    report_lines.append("─" * 72)
    report_lines.append("TOP REFINED-STARCH MARKERS (by frequency)")
    report_lines.append("─" * 72)
    for label, cnt in sorted(refined_freq.items(), key=lambda x: -x[1])[:15]:
        pct = cnt / len(results) * 100 if results else 0
        origin = next((o for p, l, o in REFINED_STARCH_MARKERS if l == label), "?")
        report_lines.append(f"  [{origin:<8}] {label:<35} {cnt:4d} ({pct:.1f}%)")
    report_lines.append("")

    report_lines.append("─" * 72)
    report_lines.append("TOP WHOLE-FOOD MARKERS (by frequency)")
    report_lines.append("─" * 72)
    for label, cnt in sorted(whole_freq.items(), key=lambda x: -x[1])[:15]:
        pct = cnt / len(results) * 100 if results else 0
        origin = next((o for p, l, o in WHOLE_FOOD_MARKERS if l == label), "?")
        report_lines.append(f"  [{origin:<8}] {label:<35} {cnt:4d} ({pct:.1f}%)")
    report_lines.append("")

    report_lines.append("─" * 72)
    report_lines.append("EXTENDED LEXICON USAGE")
    report_lines.append("─" * 72)
    report_lines.append(f"Products using EXTENDED refined markers: {products_using_extended_refined} / {len(results)}")
    report_lines.append(f"Products using EXTENDED whole-food markers: {products_using_extended_whole} / {len(results)}")
    report_lines.append("")
    report_lines.append("EXTENDED markers are additions beyond spec Section 2.2.")
    report_lines.append("They require Nutrition Agent ratification before engine implementation.")
    report_lines.append("")
    report_lines.append("EXTENDED refined markers used:")
    extended_refined_used = {l: c for l, c in refined_freq.items()
                             if any(l2 == l and o == "EXTENDED" for _, l2, o in REFINED_STARCH_MARKERS)}
    for label, cnt in sorted(extended_refined_used.items(), key=lambda x: -x[1]):
        report_lines.append(f"  {label:<35} {cnt:4d}")
    report_lines.append("")
    report_lines.append("EXTENDED whole-food markers used:")
    extended_whole_used = {l: c for l, c in whole_freq.items()
                           if any(l2 == l and o == "EXTENDED" for _, l2, o in WHOLE_FOOD_MARKERS)}
    for label, cnt in sorted(extended_whole_used.items(), key=lambda x: -x[1]):
        report_lines.append(f"  {label:<35} {cnt:4d}")
    report_lines.append("")

    report_lines.append("─" * 72)
    report_lines.append("WRONG-CLASSIFICATION TABLE (for manual audit)")
    report_lines.append("─" * 72)
    wrong = high_wrong + med_wrong
    report_lines.append(f"Total wrong classifications (high + medium confidence): {len(wrong)}")
    report_lines.append("")
    for i, r in enumerate(wrong, 1):
        report_lines.append(
            f"WRONG-{i:03d} [{r['category']}] barcode={r['barcode']} conf={r['expected_confidence']}"
        )
        report_lines.append(f"  Name: {r['name_he']}")
        report_lines.append(f"  Expected: {r['expected_class_heuristic']} | Inferred: {r['inferred_class']}")
        report_lines.append(f"  n_refined={r['n_refined']} refined={r['refined_markers_fired']}")
        report_lines.append(f"  n_whole={r['n_whole']}   whole={r['whole_markers_fired']}")
        report_lines.append(f"  matrix_score={r['matrix_score']}  balance={r['matrix_balance']}")
        report_lines.append(f"  failure_mode: {r['failure_mode']}")
        report_lines.append(f"  TEXT: {r['ingredients_text'][:200]}")
        report_lines.append("")
    if not wrong:
        report_lines.append("No wrong classifications on high/medium-confidence subset.")
    report_lines.append("")

    report_lines.append("─" * 72)
    report_lines.append("VERDICT AND GAP ANALYSIS")
    report_lines.append("─" * 72)
    report_lines.append(f"Combined accuracy: {combined_acc:.1%}")
    report_lines.append(f"High-confidence accuracy: {high_acc:.1%}")
    report_lines.append(f"Target: >= 90%")
    report_lines.append(f"Result: {verdict}")
    report_lines.append("")
    report_lines.append("HONEST LIMITATION: The heuristic ground-truth is imperfect.")
    report_lines.append("  - HIGH-confidence cases (name-signal-derived) are the most")
    report_lines.append("    trustworthy accuracy signal. Low-confidence and MIXED cases")
    report_lines.append("    should NOT be counted toward the 90% bar.")
    report_lines.append("  - This probe cannot catch cases where both inferred and expected")
    report_lines.append("    are wrong (e.g. an edge case with unusual Hebrew spelling).")
    report_lines.append("  - The owner should audit the wrong-classification table above")
    report_lines.append("    before treating the high-confidence accuracy as validated.")
    report_lines.append("")

    if verdict == "FAIL":
        report_lines.append("PRIMARY GAPS IDENTIFIED:")
        for fm, count in sorted(failure_modes.items(), key=lambda x: -x[1]):
            if fm not in ("OK", "GENUINELY_MIXED"):
                report_lines.append(f"  - {fm}: {count} products")
        report_lines.append("")
        report_lines.append("CLOSABILITY ASSESSMENT:")
        if no_marker_rate > 0.10:
            report_lines.append(
                f"  - NO_MARKERS_FIRED rate {no_marker_rate:.1%} is high. Primary cause is likely"
                "  short ingredient lists or unusual product types where neither refined"
                "  nor whole markers appear. Adding term coverage helps but cannot"
                "  fix structurally sparse labels."
            )
        missed_refined = failure_modes.get("MISSED_REFINED_MARKERS", 0)
        if missed_refined > 0:
            report_lines.append(
                f"  - {missed_refined} products where refined class expected but no refined"
                "  markers fired. Review the wrong-classification table — likely caused by"
                "  ingredient text using uncommon synonyms for flour/starch/sugar."
            )
        missed_whole = failure_modes.get("MISSED_WHOLE_FOOD_MARKERS", 0)
        if missed_whole > 0:
            report_lines.append(
                f"  - {missed_whole} products where whole-food class expected but no whole"
                "  markers fired. Likely unusual whole-food terms not in lexicon."
            )

    report_lines.append("")
    report_lines.append("=" * 72)
    report_lines.append("END OF REPORT")
    report_lines.append("=" * 72)

    # ---------------------------------------------------------------------------
    # Write outputs
    # ---------------------------------------------------------------------------
    report_text = "\n".join(report_lines)
    report_path = OUT_DIR / "matrix_signal_probe_v1_report.txt"
    with open(report_path, "w", encoding="utf-8") as f:
        f.write(report_text)
    print(f"\nReport written: {report_path}")

    # Full JSON results (hand-auditable table)
    json_out = {
        "probe": "matrix_signal_probe_v1",
        "run_at": datetime.utcnow().isoformat() + "Z",
        "task": "TASK-395",
        "condition": "C-N1-1",
        "target_accuracy": 0.90,
        "summary": {
            "corpus_total": len(results),
            "high_conf_count": len(high_conf),
            "high_conf_correct": len(high_correct),
            "high_conf_wrong": len(high_wrong),
            "high_conf_accuracy": round(high_acc, 4),
            "med_conf_count": len(med_conf),
            "med_conf_correct": len(med_correct),
            "med_conf_wrong": len(med_wrong),
            "med_conf_accuracy": round(med_acc, 4),
            "combined_count": len(all_clearcut),
            "combined_correct": len(all_correct),
            "combined_accuracy": round(combined_acc, 4),
            "no_markers_count": len(no_markers),
            "no_markers_rate": round(no_marker_rate, 4),
            "verdict": verdict,
            "gap_to_target": round(max(0, target - combined_acc), 4),
        },
        "accuracy_caveat": (
            "Ground-truth is rule-based heuristic from product names + category defaults. "
            "HIGH-confidence subset is most reliable. Manual audit required for wrong-classification table. "
            "This probe CANNOT self-validate — owner/Hebrew reader must spot-check failure cases."
        ),
        "category_breakdown": cats,
        "failure_modes": failure_modes,
        "inferred_class_distribution": class_dist,
        "refined_marker_frequency": dict(sorted(refined_freq.items(), key=lambda x: -x[1])),
        "whole_food_marker_frequency": dict(sorted(whole_freq.items(), key=lambda x: -x[1])),
        "extended_lexicon_note": (
            "SPEC markers are from target_scoring_logic_spec_v1.md Section 2.2. "
            "EXTENDED markers are additions observed in the corpus. "
            "Extended markers require Nutrition Agent ratification."
        ),
        "products": results,
    }

    json_path = OUT_DIR / "matrix_signal_probe_v1_results.json"
    with open(json_path, "w", encoding="utf-8") as f:
        json.dump(json_out, f, ensure_ascii=False, indent=2)
    print(f"JSON results written: {json_path}")

    # Hash the outputs
    def sha256_file(path: Path) -> str:
        h = hashlib.sha256()
        with open(path, "rb") as f:
            h.update(f.read())
        return h.hexdigest()

    report_sha = sha256_file(report_path)
    json_sha = sha256_file(json_path)

    print(f"\nArtifact hashes:")
    print(f"  report SHA256: {report_sha}")
    print(f"  json   SHA256: {json_sha}")

    # Print the key numbers to stdout for the return contract
    print()
    print("=" * 72)
    print("SUMMARY FOR RETURN CONTRACT")
    print("=" * 72)
    print(f"corpus_total:         {len(results)}")
    print(f"high_conf_accuracy:   {high_acc:.1%}  ({len(high_correct)}/{len(high_conf)})")
    print(f"med_conf_accuracy:    {med_acc:.1%}  ({len(med_correct)}/{len(med_conf)})")
    print(f"combined_accuracy:    {combined_acc:.1%}  ({len(all_correct)}/{len(all_clearcut)})")
    print(f"no_markers_rate:      {no_marker_rate:.1%}")
    print(f"verdict:              {verdict}")
    print(f"target:               90.0%")
    print()
    print(f"report_path:  {report_path}")
    print(f"json_path:    {json_path}")
    print(f"report_sha256: {report_sha}")
    print(f"json_sha256:   {json_sha}")

    return {
        "combined_accuracy": combined_acc,
        "high_conf_accuracy": high_acc,
        "verdict": verdict,
        "report_sha256": report_sha,
        "json_sha256": json_sha,
    }


if __name__ == "__main__":
    main()
