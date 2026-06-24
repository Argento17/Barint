"""
generate_page.py — Bari Page Generator
=======================================
Usage:
  python generate_page.py --config <category_config.json> --out <output.json>
                          [--timestamp <ISO8601>]

Behavior:
  Reads a category config, walks every BSIP2 trace directory as the universe,
  looks up each barcode in BSIP1 corpus, applies OFF ban, subpool filter,
  dedup, and explicit exclusions. Produces a complete frontend JSON with all
  copy fields set to PENDING_COPY. Ends by running run_gates.py on its own
  output (non-zero exit if any gate FAILs).

Hard rules carried in:
  - OFF ban (TASK-238): panel_source=open_food_facts or off_candidate_panel
    in canonical_risk_flags → exclusion "off_banned". Never used.
  - Hebrew name required: no English-only names from any source.
  - Score = trace final_score_estimate. Grade = boundary policy (floor).
  - All exclusions documented in _meta; nothing silent.
  - Deterministic + idempotent: same inputs → byte-identical output.
    Sort keys globally, sort products by score desc (None last), fixed
    timestamp source = --timestamp arg or config-specified or run-time UTC.

Confidence label/tooltip mapping: copied from live granola/snacks patterns
  observed in granola_frontend_v1.json and snacks_frontend_v2.json.
  Source: 03_operations/bsip1 records confidence_band + missing_nutrition_fields
          + missing ingredients.
"""

import argparse
import hashlib
import json
import os
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path

# Render fields helper — TASK-316 render-contract gap closure
# Import lazily to avoid breaking existing callers that don't need it
_render_fields_mod = None


def _get_render_fields():
    global _render_fields_mod
    if _render_fields_mod is None:
        try:
            # Same directory as this script
            _dir = os.path.dirname(os.path.abspath(__file__))
            if _dir not in sys.path:
                sys.path.insert(0, _dir)
            import render_fields as _rf
            _render_fields_mod = _rf
        except Exception as e:
            print(f"WARNING: render_fields import failed: {e}", file=sys.stderr)
            _render_fields_mod = None
    return _render_fields_mod

GENERATOR_VERSION = "1.2.0"
SCHEMA_VERSION = "v3"

# ---------------------------------------------------------------------------
# Grade scale (floor policy — default)
# ---------------------------------------------------------------------------

GRADE_SCALE = [
    ("S", 90),
    ("A", 80),
    ("B", 65),
    ("C", 50),
    ("D", 35),
    ("E", 0),
]


def score_to_grade(score, policy="floor"):
    """Convert numeric score to letter grade using central scale."""
    if score is None:
        return None
    if policy == "round":
        score = round(score)
    for grade, threshold in GRADE_SCALE:
        if score >= threshold:
            return grade
    return "E"


# ---------------------------------------------------------------------------
# Hebrew check
# ---------------------------------------------------------------------------

import re as _re

HEBREW_RE = _re.compile(r"[֐-׿]")


def has_hebrew(text):
    return bool(HEBREW_RE.search(text or ""))


# ---------------------------------------------------------------------------
# OFF markers (TASK-238 hard rule)
# ---------------------------------------------------------------------------

OFF_MARKERS_LITERAL = [
    "open_food_facts",
    "openfoodfacts",
    "off_candidate_panel",
]


def is_off_contaminated(corpus_rec):
    """Return True if a BSIP1 record carries any OFF contamination marker."""
    if not corpus_rec:
        return False
    # Check panel_source field (present in some OFF-enriched records)
    panel_source = corpus_rec.get("panel_source", "")
    if panel_source and any(m in str(panel_source).lower() for m in OFF_MARKERS_LITERAL):
        return True
    # Check canonical_risk_flags list
    risk_flags = corpus_rec.get("canonical_risk_flags", [])
    if isinstance(risk_flags, list):
        for flag in risk_flags:
            if any(m in str(flag).lower() for m in OFF_MARKERS_LITERAL):
                return True
    # Check ingredients_raw_provenance.source
    provenance = corpus_rec.get("ingredients_raw_provenance", {})
    if isinstance(provenance, dict):
        src = str(provenance.get("source", "")).lower()
        if any(m in src for m in OFF_MARKERS_LITERAL):
            return True
    # Fallback: scan full record as string for any OFF marker
    rec_str = json.dumps(corpus_rec, ensure_ascii=False).lower()
    if "open_food_facts" in rec_str or "openfoodfacts.org" in rec_str:
        return True
    return False


# ---------------------------------------------------------------------------
# Config loading
# ---------------------------------------------------------------------------

def load_json(path):
    with open(path, encoding="utf-8") as f:
        return json.load(f)


def sha256_file(path):
    h = hashlib.sha256()
    with open(path, "rb") as f:
        h.update(f.read())
    return h.hexdigest()


def sha256_str(s):
    return hashlib.sha256(s.encode("utf-8")).hexdigest()


# ---------------------------------------------------------------------------
# Corpus loading
# ---------------------------------------------------------------------------

def load_bsip1_corpus(corpus_dirs):
    """
    Load all bsip1_*.json files from corpus_dirs (list, in priority order).
    First occurrence of a barcode wins (highest-priority corpus).
    Returns dict: barcode -> record
    Also returns dict: barcode -> source_dir_index (for dedup logging)
    """
    corpus = {}
    corpus_source = {}
    for dir_idx, corpus_dir in enumerate(corpus_dirs):
        if not corpus_dir or not os.path.isdir(corpus_dir):
            continue
        for fname in sorted(os.listdir(corpus_dir)):
            if fname.startswith("bsip1_") and fname.endswith(".json"):
                try:
                    rec = load_json(os.path.join(corpus_dir, fname))
                    bc = str(rec.get("barcode", "")).strip()
                    if bc and bc not in corpus:
                        corpus[bc] = rec
                        corpus_source[bc] = dir_idx
                except Exception:
                    pass
    return corpus, corpus_source


# ---------------------------------------------------------------------------
# BSIP2 trace loading
# ---------------------------------------------------------------------------

def load_bsip2_traces(run_dirs):
    """
    Load all bsip2_trace.json files from product subdirs.
    run_dirs may be a string (single dir) or list.
    Returns dict: barcode -> trace record, and dict: barcode -> dir_name
    """
    if isinstance(run_dirs, str):
        run_dirs = [run_dirs]

    traces = {}
    trace_dirs = {}
    for run_dir in run_dirs:
        if not run_dir or not os.path.isdir(run_dir):
            continue
        for dname in sorted(os.listdir(run_dir)):
            dpath = os.path.join(run_dir, dname)
            if not os.path.isdir(dpath):
                continue
            trace_path = os.path.join(dpath, "bsip2_trace.json")
            if os.path.isfile(trace_path):
                try:
                    rec = load_json(trace_path)
                    bc = str(rec.get("input_reference", {}).get("barcode", "")).strip()
                    if bc and bc not in traces:
                        traces[bc] = rec
                        trace_dirs[bc] = dname
                except Exception:
                    pass
    return traces, trace_dirs


# ---------------------------------------------------------------------------
# Confidence label/tooltip mapping
# Copied from live granola/snacks conventions:
#   confidence_band="high" + all nutrition present → "נתונים מאומתים"
#   confidence_band="high" + missing some nutrition → "נתונים בבדיקה"
#   missing ingredients only → "חסרים נתוני רכיבים"
#   missing nutrition (all/most) → "חסרים נתוני תזונה"
#   confidence_band="low" + partial nutrition → "מבוסס על נתונים חלקיים"
# Source: observed in granola_frontend_v1.json and snacks_frontend_v2.json;
#   cross-checked against confidence fields in bsip2_trace.json.
# ---------------------------------------------------------------------------

def build_confidence_fields(trace, corpus_rec):
    """
    Return (confidence_str, confidence_label_he, confidence_tooltip_he,
            confidence_sub_reason, expansion_confidence_label)
    Mechanical mapping from trace confidence_band + missing fields.
    """
    confidence_band = trace.get("confidence_band", "")
    confidence_score = trace.get("confidence_score", 100)
    missing_nutrition = trace.get("L1_observed_signals", {}).get("missing_nutrition_fields", [])

    # Determine whether ingredients are available
    has_ingredients = False
    if corpus_rec:
        ingr = corpus_rec.get("ingredients_text_he") or corpus_rec.get("ingredients_raw", "")
        if ingr and ingr.strip():
            has_ingredients = True

    # Determine nutrition completeness
    core_nutrition_fields = ["fat_saturated_g", "dietary_fiber_g", "protein_g",
                              "fat_g", "sugars_g", "sodium_mg", "energy_kcal"]
    missing_core = [f for f in missing_nutrition if f in core_nutrition_fields]

    # Check if all nutrition is null (snacks pattern)
    all_nutrition_null = False
    nutrition = {}
    if corpus_rec:
        nn = corpus_rec.get("normalized_nutrition_per_100g", {})
        nutrition = nn or {}
        key_fields = ["energy_kcal", "fat_g", "protein_g", "sugars_g", "sodium_mg"]
        all_nutrition_null = all(nutrition.get(f) is None for f in key_fields)

    data_sufficiency = trace.get("data_sufficiency", "sufficient")

    # Map to 3-state confidence
    if data_sufficiency == "insufficient":
        confidence_str = "insufficient"
        label_he = "חסרים נתונים מרכזיים"
        tooltip_he = "חסרים נתונים מרכזיים — הציון עשוי להיות לא מייצג."
        sub_reason = "insufficient_data"
    elif all_nutrition_null or (len(missing_core) >= 4):
        confidence_str = "partial"
        label_he = "חסרים נתוני תזונה"
        tooltip_he = "חלק מנתוני התזונה לא היו זמינים — הציון מבוסס על הנתונים שכן היו זמינים."
        sub_reason = "missing_nutrition"
    elif not has_ingredients:
        confidence_str = "partial"
        label_he = "חסרים נתוני רכיבים"
        tooltip_he = "רשימת הרכיבים לא הייתה זמינה — הציון מבוסס על נתוני התזונה בלבד."
        sub_reason = "missing_ingredients"
    elif confidence_band == "high" and len(missing_core) == 0:
        confidence_str = "full"
        label_he = "נתונים מאומתים"
        tooltip_he = "הנתונים מאומתים ממקור ישיר. הציון מבוסס על נתוני תזונה ורכיבים מלאים."
        sub_reason = None
    elif confidence_band == "low":
        confidence_str = "partial"
        label_he = "מבוסס על נתונים חלקיים"
        tooltip_he = "חלק מהנתונים בבדיקה. הציון עשוי להתעדכן כשיתווספו נתונים מאומתים."
        sub_reason = "low_extraction"
    else:
        # Default: partial with missing fields
        confidence_str = "partial"
        label_he = "נתונים בבדיקה"
        tooltip_he = "חלק מהנתונים בבדיקה. הציון עשוי להתעדכן כשיתווספו נתונים מאומתים."
        sub_reason = "low_extraction"

    return confidence_str, label_he, tooltip_he, sub_reason, label_he


# ---------------------------------------------------------------------------
# Nutrition mapping: BSIP1 normalized_nutrition_per_100g -> expansion.nutrition
# ---------------------------------------------------------------------------

NUTRITION_FIELD_MAP = {
    "energyKcal": "energy_kcal",
    "protein": "protein_g",
    "sugar": "sugars_g",
    "fat": "fat_g",
    "fiber": "dietary_fiber_g",
    "sodium": "sodium_mg",
}


# ---------------------------------------------------------------------------
# v3: Dimension key → Hebrew consumer-facing label
# These are the canonical display labels for the bariInterpretation array.
# Map mirrors the milk-comparison.json gold standard labels.
# ---------------------------------------------------------------------------

DIMENSION_LABEL_MAP = {
    "processing_quality": "רמת עיבוד",
    "nutrient_density": "ערך תזונתי",
    "calorie_density": "צפיפות קלורית",
    "glycemic_quality": "איכות גליקמית",
    "protein_quality": "חלבון",
    "additive_quality": "תוספים",
    "satiety_support": "תחושת שובע",
    "fat_quality": "איכות שומן",
    "regulatory_quality": "איכות רגולטורית",
    "whole_food_integrity": "שלמות מזון",
}

# Ordered list: the dimensions we surface in bariInterpretation (most informative first)
DIMENSION_DISPLAY_ORDER = [
    "processing_quality",
    "additive_quality",
    "nutrient_density",
    "protein_quality",
    "calorie_density",
    "glycemic_quality",
    "fat_quality",
    "satiety_support",
    "regulatory_quality",
    "whole_food_integrity",
]


def score_to_strength(score):
    """Map a dimension score to a Hebrew strength label.

    Buckets:
      ≥80 → חזק   (strong)
      ≥50 → בינוני (medium)
      <50 → נמוך   (low)
      None → 'data not available'

    GUARD: never fabricate a strength when the score is missing.
    """
    if score is None:
        return "data not available"
    if score >= 80:
        return "חזק"
    if score >= 50:
        return "בינוני"
    return "נמוך"


def build_bari_interpretation(trace):
    """
    Build the bariInterpretation[] array from the BSIP2 trace.

    DETERMINISTIC parts (filled here):
      - key:      dimension key (string)
      - label:    consumer-facing Hebrew label (DIMENSION_LABEL_MAP)
      - score:    round(trace.dimension_scores[key], 1) — real trace value
      - strength: bucket from score_to_strength()

    AUTHORED part (set to PENDING_COPY here):
      - interpretation: filled by author_copy stage

    GUARD: if a dimension score is missing or not a valid number, emit
    null score + 'data not available' strength. NEVER fabricate a value.
    """
    dim_scores = trace.get("dimension_scores") or {}
    result = []

    for key in DIMENSION_DISPLAY_ORDER:
        label = DIMENSION_LABEL_MAP.get(key, key)
        raw_score = dim_scores.get(key)

        # Validity check: must be a real number in [0,100]
        if raw_score is not None:
            try:
                score_f = float(raw_score)
                if score_f < 0 or score_f > 100:
                    # Anomalous value — emit honestly
                    score_f = None
                else:
                    score_f = round(score_f, 1)
            except (TypeError, ValueError):
                score_f = None
        else:
            score_f = None

        strength = score_to_strength(score_f)

        result.append({
            "key": key,
            "label": label,
            "score": score_f,
            "strength": strength,
            "interpretation": "PENDING_COPY",
        })

    return result


def build_best_use_cases(corpus_rec, trace):
    """
    Build bestUseCases[] deterministically when a clean rule applies.
    Returns a list of Hebrew use-case tags OR ["PENDING_COPY"] when
    no clean deterministic rule applies.

    Current deterministic rules:
      - additive_count == 0 in BSIP1 → 'רכיבים פשוטים'
      - protein_quality score >= 70 → 'חלבון'

    Everything else: PENDING_COPY (author fills).
    GUARD: never invent a tag for a missing value.
    """
    if not corpus_rec:
        return ["PENDING_COPY"]

    tags = []

    # Rule 1: no additives → simple ingredients tag
    # We check the L3 signals from the trace (additive_marker_count)
    l3 = trace.get("L3_inferred_classifications") or {}
    additive_count = l3.get("additive_marker_count", None)
    if additive_count is not None and additive_count == 0:
        tags.append("רכיבים פשוטים")

    # Rule 2: high protein quality dimension → protein tag
    dim_scores = trace.get("dimension_scores") or {}
    protein_q = dim_scores.get("protein_quality")
    if protein_q is not None and protein_q >= 70:
        tags.append("חלבון")

    if not tags:
        return ["PENDING_COPY"]
    return tags


def build_nutrition_expansion(corpus_rec):
    """Map BSIP1 normalized_nutrition_per_100g to expansion.nutrition dict."""
    nn = {}
    if corpus_rec:
        nn = corpus_rec.get("normalized_nutrition_per_100g") or {}
    result = {}
    for out_key, in_key in NUTRITION_FIELD_MAP.items():
        result[out_key] = nn.get(in_key, None)
    return result


# ---------------------------------------------------------------------------
# Extension fields from BSIP1 corpus record
# ---------------------------------------------------------------------------

def get_extension_field_value(corpus_rec, trace, field_name):
    """
    Extract an extension field value from corpus_rec or trace.
    Known extension fields and their sources:
      _subpool: fixed as "granola" for granola category (from bsip_cereal_subtype)
      _isChildrens: corpus bsip_cereal_subtype == "childrens_character"
      _wholeGrainClaim: detect from corpus claims or ingredients
      _internal_cluster: not in BSIP1 — leave as null (Phase 2 copy engine)
    """
    if not corpus_rec:
        return None

    if field_name == "_subpool":
        return corpus_rec.get("bsip_cereal_subtype", None)

    if field_name == "_isChildrens":
        subtype = corpus_rec.get("bsip_cereal_subtype", "")
        return subtype == "childrens_character"

    if field_name == "_wholeGrainClaim":
        # Check for whole grain in ingredients or claims
        ingr = corpus_rec.get("ingredients_text_he", "") or ""
        claims_raw = corpus_rec.get("claims_raw", "") or ""
        whole_grain_terms = ["דגנים מלאים", "קמח מלא", "שיבולת שועל מלאה", "whole grain"]
        return any(t.lower() in ingr.lower() or t.lower() in claims_raw.lower()
                   for t in whole_grain_terms)

    if field_name == "_internal_cluster":
        # Not available from BSIP1 — requires Phase 2 copy engine
        return None

    return None


# ---------------------------------------------------------------------------
# Build a single product object
# ---------------------------------------------------------------------------

def build_product(barcode, trace, corpus_rec, config, boundary_policy):
    """
    Build a frontend product object from trace + corpus record.
    Returns the product dict.
    """
    product_id = trace.get("input_reference", {}).get("canonical_product_id", f"bsip1_{barcode}")

    # Score and grade
    raw_score = trace.get("final_score_estimate")
    grade = score_to_grade(raw_score, boundary_policy)

    # Name from corpus (must have Hebrew)
    name = ""
    if corpus_rec:
        name = (corpus_rec.get("canonical_name_he") or "").strip()

    # Brand from corpus (TASK-392: was missing from generator, causing empty brand on all
    # generator-produced pages; brand is sourced from BSIP1 corpus_rec.brand — direct scrape)
    brand = None
    if corpus_rec:
        brand_val = corpus_rec.get("brand")
        if brand_val and str(brand_val).strip():
            brand = str(brand_val).strip()

    # imageUrl from corpus
    image_url = None
    if corpus_rec:
        image_url = corpus_rec.get("image_url") or None
        if not image_url:
            urls = corpus_rec.get("image_urls") or []
            image_url = urls[0] if urls else None

    # Confidence
    conf_str, label_he, tooltip_he, sub_reason, exp_label = build_confidence_fields(
        trace, corpus_rec
    )

    # Nutrition expansion
    nutrition = build_nutrition_expansion(corpus_rec)

    # Ingredients
    ingredients = None
    if corpus_rec:
        ingr = corpus_rec.get("ingredients_text_he") or corpus_rec.get("ingredients_raw", "")
        if ingr and ingr.strip():
            ingredients = ingr.strip()

    # Retailer
    retailer = "unknown"
    if corpus_rec:
        retailers = corpus_rec.get("source_retailers") or []
        if retailers:
            retailer = retailers[0]

    # Build expansion
    expansion = {
        "nutrition": nutrition,
        "ingredients": ingredients,
        "confidenceLabel": exp_label,
        "servingNote": "ל-100 גרם",
        "positiveSignals": [],
        "limitingFactors": [],
        "comparisonContext": "PENDING_COPY",
    }

    # Product object — all required fields
    product = {
        "id": product_id,
        "name": name,
        "brand": brand,  # TASK-392: populated from corpus_rec.brand (direct scrape)
        "imageUrl": image_url,
        "score": raw_score,
        "grade": grade,
        "insightLine": "PENDING_COPY",
        "confidence": conf_str,
        "retailer": retailer,
        "barcode": barcode,
        "source_traceability_status": "resolved",
        "d4_additives": [],
        "confidence_label_he": label_he,
        "confidence_tooltip_he": tooltip_he,
        "confidence_sub_reason": sub_reason,
        "expansion": expansion,
    }

    # Extension fields per config (legacy mechanism — cereals/granola)
    extension_fields = config.get("extension_fields") or []
    for field_name in extension_fields:
        val = get_extension_field_value(corpus_rec, trace, field_name)
        product[field_name] = val

    # Render fields per config (TASK-316: full frontend render contract).
    # Each category config declares the render fields its live page carries.
    # Derivation is in render_fields.py; no category-special-cased code paths here.
    render_fields_list = config.get("render_fields") or []
    if render_fields_list:
        rf_mod = _get_render_fields()
        if rf_mod is not None:
            for field_name in render_fields_list:
                val = rf_mod.get_render_field_value(corpus_rec, trace, field_name)
                product[field_name] = val

    # rowVerdict — PENDING if category uses it (granola does)
    # We emit it always; copy engine fills it in Phase 2
    product["rowVerdict"] = "PENDING_COPY"

    # -------------------------------------------------------------------
    # v3: milk-depth content fields
    # -------------------------------------------------------------------

    # consumerTakeaway — AUTHORED (PENDING_COPY in generator)
    product["consumerTakeaway"] = "PENDING_COPY"

    # expansion.consumerExplanation — AUTHORED (all sub-fields PENDING_COPY)
    expansion["consumerExplanation"] = {
        "whyRated": "PENDING_COPY",
        "good": ["PENDING_COPY"],
        "watchOut": [],
        "context": "PENDING_COPY",
        "takeaway": "PENDING_COPY",
    }

    # bariInterpretation — DETERMINISTIC key/label/score/strength; AUTHORED interpretation
    product["bariInterpretation"] = build_bari_interpretation(trace)

    # bestUseCases — DETERMINISTIC when rule applies, else PENDING_COPY
    product["bestUseCases"] = build_best_use_cases(corpus_rec, trace)

    return product


# ---------------------------------------------------------------------------
# Subpool filter
# ---------------------------------------------------------------------------

def passes_subpool_filter(corpus_rec, subpool_filter):
    """Return True if the corpus record passes the subpool filter (or no filter)."""
    if not subpool_filter:
        return True
    if not corpus_rec:
        return False
    field = subpool_filter.get("field", "")
    value = subpool_filter.get("value", "")
    return str(corpus_rec.get(field, "")) == str(value)


# ---------------------------------------------------------------------------
# Main generator
# ---------------------------------------------------------------------------

def generate(config_path, out_path, fixed_timestamp=None):
    config = load_json(config_path)
    config_sha = sha256_file(config_path)

    category = config["category"]
    corpus_dirs = config.get("corpus_dirs", [])
    if isinstance(corpus_dirs, str):
        corpus_dirs = [corpus_dirs]

    run_products_dir = config.get("run_products_dir")
    run_dirs = run_products_dir if isinstance(run_products_dir, list) else [run_products_dir]

    baseline_json = config.get("baseline_json")
    subpool_filter = config.get("subpool_filter")
    explicit_exclusions = {
        str(e["barcode"]): e["reason"]
        for e in (config.get("exclusions") or [])
    }
    extension_fields = config.get("extension_fields") or []

    # Boundary policy
    boundary_policy_path = config.get("boundary_policy")
    boundary_policy = "floor"
    if boundary_policy_path and os.path.isfile(boundary_policy_path):
        try:
            bp = load_json(boundary_policy_path)
            boundary_policy = bp.get("policy", "floor")
        except Exception:
            boundary_policy = "floor"

    # Load corpus
    corpus, corpus_source = load_bsip1_corpus(corpus_dirs)

    # Load traces (the run universe)
    traces, trace_dirs = load_bsip2_traces(run_dirs)

    # Track all exclusions with reasons
    exclusions = []
    products = []
    dedup_seen = {}  # barcode -> product_id (for dedup logging)

    scored_count = len(traces)

    # Sort trace barcodes deterministically
    for barcode in sorted(traces.keys()):
        trace = traces[barcode]

        # 1. Explicit exclusion from config
        if barcode in explicit_exclusions:
            exclusions.append({
                "barcode": barcode,
                "product_id": trace.get("input_reference", {}).get("canonical_product_id", ""),
                "reason": explicit_exclusions[barcode],
            })
            continue

        # 2. Corpus lookup
        corpus_rec = corpus.get(barcode)
        if corpus_rec is None:
            exclusions.append({
                "barcode": barcode,
                "product_id": trace.get("input_reference", {}).get("canonical_product_id", ""),
                "reason": "no_corpus_record: barcode not found in any corpus_dir",
            })
            continue

        # 3. OFF ban check
        if is_off_contaminated(corpus_rec):
            exclusions.append({
                "barcode": barcode,
                "product_id": corpus_rec.get("canonical_product_id", ""),
                "reason": "off_banned: corpus record has OFF contamination marker (panel_source or canonical_risk_flags or provenance source). TASK-238 hard rule.",
            })
            continue

        # 4. Subpool filter
        if not passes_subpool_filter(corpus_rec, subpool_filter):
            subpool_val = corpus_rec.get(subpool_filter.get("field", ""), "")
            exclusions.append({
                "barcode": barcode,
                "product_id": corpus_rec.get("canonical_product_id", ""),
                "reason": f"subpool_filter: field '{subpool_filter.get('field')}' = '{subpool_val}' does not match required '{subpool_filter.get('value')}'",
            })
            continue

        # 5. Hebrew name check
        name = (corpus_rec.get("canonical_name_he") or "").strip()
        if not name or not has_hebrew(name):
            exclusions.append({
                "barcode": barcode,
                "product_id": corpus_rec.get("canonical_product_id", ""),
                "reason": f"no_hebrew_name: name='{name}' contains no Hebrew characters",
            })
            continue

        # 6. Dedup
        if barcode in dedup_seen:
            exclusions.append({
                "barcode": barcode,
                "product_id": corpus_rec.get("canonical_product_id", ""),
                "reason": f"dedup: barcode already seen as {dedup_seen[barcode]} (rule=one_card_per_barcode, keep=highest_priority_corpus)",
            })
            continue
        dedup_seen[barcode] = corpus_rec.get("canonical_product_id", barcode)

        # Build product
        product = build_product(barcode, trace, corpus_rec, config, boundary_policy)
        products.append(product)

    # Sort products by score descending (None last), then barcode asc for ties
    def sort_key(p):
        s = p.get("score")
        return (0 if s is None else -s, p.get("barcode", ""))

    products.sort(key=sort_key)

    # Retailer breakdown
    retailer_breakdown = {}
    for p in products:
        r = p.get("retailer", "unknown")
        retailer_breakdown[r] = retailer_breakdown.get(r, 0) + 1

    # Timestamp
    if fixed_timestamp:
        generated_at = fixed_timestamp
    else:
        generated_at = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")

    # Build _meta
    meta = {
        "generated": generated_at,
        "category": category,
        "product_count": len(products),
        "scored_count": scored_count,
        "schema": "BariProductVM[]",
        "schema_version": SCHEMA_VERSION,
        "generator_version": GENERATOR_VERSION,
        "config_sha256": config_sha,
        "exclusions": sorted(exclusions, key=lambda e: e["barcode"]),
        "retailer_breakdown": dict(sorted(retailer_breakdown.items())),
        "source_paths": {
            "corpus_dirs": corpus_dirs,
            "run_products_dir": run_dirs,
        },
        "subpool_filter": subpool_filter,
    }

    output = {
        "_meta": meta,
        "products": products,
    }

    # Write output (sort_keys for determinism)
    with open(out_path, "w", encoding="utf-8") as f:
        json.dump(output, f, ensure_ascii=False, indent=2, sort_keys=True)

    return output, exclusions, scored_count


# ---------------------------------------------------------------------------
# Self-gating: invoke run_gates.py on the generated output
# ---------------------------------------------------------------------------

def run_gates(out_path, config, schema_path=None):
    """
    Invoke run_gates.py on the generated output.
    Returns (exit_code, stdout_text).
    """
    gates_script = Path(__file__).parent / "gates" / "run_gates.py"
    if not gates_script.exists():
        print("ERROR: run_gates.py not found at expected path", file=sys.stderr)
        return 1, ""

    if schema_path is None:
        schema_path = str(Path(__file__).parent / "contract" / "page_output_schema_v3.json")

    corpus_dirs = config.get("corpus_dirs", [])
    if isinstance(corpus_dirs, str):
        corpus_dirs = [corpus_dirs]
    # Use first corpus dir that exists for the gates --corpus arg
    corpus_arg = next((d for d in corpus_dirs if d and os.path.isdir(d)), "")

    run_products_dir = config.get("run_products_dir")
    if isinstance(run_products_dir, list):
        run_arg = next((d for d in run_products_dir if d and os.path.isdir(d)), "")
    else:
        run_arg = run_products_dir or ""

    baseline_json = config.get("baseline_json") or ""

    cmd = [
        sys.executable,
        str(gates_script),
        out_path,
        "--schema", schema_path,
    ]
    if corpus_arg:
        cmd += ["--corpus", corpus_arg]
    if run_arg:
        cmd += ["--run", run_arg]
    if baseline_json and os.path.isfile(baseline_json):
        cmd += ["--baseline", baseline_json]

    try:
        result = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="replace",
        )
        return result.returncode, result.stdout + result.stderr
    except Exception as e:
        return 1, f"ERROR running gates: {e}"


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------

def main():
    # Force UTF-8 on stdout/stderr
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    if hasattr(sys.stderr, "reconfigure"):
        sys.stderr.reconfigure(encoding="utf-8", errors="replace")

    parser = argparse.ArgumentParser(
        description="Bari Page Generator — scored shelf to frontend JSON"
    )
    parser.add_argument("--config", required=True, help="Path to category config JSON")
    parser.add_argument("--out", required=True, help="Path for output JSON")
    parser.add_argument(
        "--timestamp",
        default=None,
        help="Fixed ISO8601 timestamp for deterministic output (default: current UTC)",
    )
    parser.add_argument(
        "--no-gates",
        action="store_true",
        help="Skip self-gating run (for testing)",
    )
    args = parser.parse_args()

    config_path = args.config
    out_path = args.out

    if not os.path.isfile(config_path):
        print(f"ERROR: config not found: {config_path}", file=sys.stderr)
        sys.exit(1)

    config = load_json(config_path)

    print(f"Generating: category={config['category']} config={config_path}", file=sys.stderr)

    output, exclusions, scored_count = generate(config_path, out_path, args.timestamp)
    product_count = len(output["products"])

    print(f"Products in output: {product_count}", file=sys.stderr)
    print(f"Scored (run universe): {scored_count}", file=sys.stderr)
    print(f"Exclusions: {len(exclusions)}", file=sys.stderr)
    for exc in exclusions:
        print(f"  EXCLUDED bc={exc['barcode']} reason={exc['reason']}", file=sys.stderr)
    print(f"Output written to: {out_path}", file=sys.stderr)

    # Self-gating
    if not args.no_gates:
        print("\n--- SELF-GATE RUN ---", file=sys.stderr)
        gate_exit, gate_output = run_gates(out_path, config)
        print(gate_output)
        print(f"Gate exit code: {gate_exit}", file=sys.stderr)
        if gate_exit != 0:
            print("ERROR: Gate failures detected. See output above.", file=sys.stderr)
            sys.exit(1)
    else:
        print("(Self-gating skipped via --no-gates)", file=sys.stderr)


if __name__ == "__main__":
    main()
