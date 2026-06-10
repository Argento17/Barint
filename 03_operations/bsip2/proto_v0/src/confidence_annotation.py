"""
Confidence / data-completeness annotation — shared derivation module.

Implements the DATA PATH for the 7-state score-confidence indicator
(`01_framework/frontend/score_confidence_indicators_spec_v1.md`) per the
approved threshold policy
(`03_operations/bsip2/proto_v0/reports/state7_suppression_threshold_policy_v1.md`).

Produces the four per-product frontend-JSON fields:
    confidence              : verified | partial | insufficient   (3-state VM enum)
    confidence_label_he     : pre-rendered Hebrew badge label      (spec §3 col 6)
    confidence_tooltip_he   : pre-rendered Hebrew tooltip sentence (spec §3 col 7)
    confidence_sub_reason   : missing_ingredients | missing_nutrition |
                              inferred_category | low_extraction | partial_field
                              (null for states 1 verified and 7 insufficient)

HARD CONSTRAINTS honored here:
  * Derive-and-annotate ONLY. No scoring, scores, or grades are touched.
  * `confidence` is read off the BSIP2 *trace*, never the redacted frontend JSON
    (display redacts `ingredients`/`nutrition` to null as a packaging choice; the
    engine still saw the full BSIP0 panel).
  * State 6 fires on the CATEGORICAL proxy only (ingredient_text_quality /
    nova_confidence_band). The numeric `extraction_confidence` float is BACKLOG and
    is NOT wired here.
  * First-match-wins decision list R0..R6 from the threshold policy.
"""

# --- Spec §3 Hebrew strings (owner-approved; single source of truth) -----------
# State 1 — verified / complete
LABEL_VERIFIED   = "מבוסס על נתונים מלאים"
TOOLTIP_VERIFIED = "הציון מבוסס על רשימת הרכיבים ולוח התזונה המלאים."

# State 2 — partial (one non-essential field missing) -> partial_field
LABEL_PARTIAL_FIELD   = "מבוסס על נתונים חלקיים"
TOOLTIP_PARTIAL_FIELD = "הציון מבוסס על נתונים חלקיים. חלק מהפרטים לא היו זמינים."

# State 3 — missing ingredient list (panel present) -> missing_ingredients
LABEL_MISSING_INGREDIENTS   = "חסרים נתוני רכיבים"
TOOLTIP_MISSING_INGREDIENTS = "רשימת הרכיבים לא הייתה זמינה — הציון מבוסס על נתוני התזונה בלבד."

# State 4 — thin nutrition panel (present but incomplete) -> missing_nutrition
# NOTE: corrected State-4 tooltip per task instruction.
LABEL_MISSING_NUTRITION   = "חסרים נתוני תזונה"
TOOLTIP_MISSING_NUTRITION = "חלק מנתוני התזונה לא היו זמינים — הציון מבוסס על הנתונים שכן היו זמינים."

# State 5 — inferred category -> inferred_category
LABEL_INFERRED_CATEGORY   = "קטגוריה משוערת"
TOOLTIP_INFERRED_CATEGORY = "הקטגוריה זוהתה באופן משוער. הציון עשוי להתעדכן כשיתווספו נתונים."

# State 6 — low-confidence extraction -> low_extraction
LABEL_LOW_EXTRACTION   = "נתונים בבדיקה"
TOOLTIP_LOW_EXTRACTION = "חלק מהנתונים בבדיקה. הציון עשוי להתעדכן כשיתווספו נתונים מאומתים."

# State 7 — not enough data to score safely (insufficient)
LABEL_INSUFFICIENT   = "טרם נוקד"
TOOLTIP_INSUFFICIENT = "המוצר טרם נוקד — הנתונים לא היו זמינים לניתוח. הציון יתווסף כשיתווספו נתונים."

CAT_CONF_MEDIUM = 0.50  # threshold policy R5

# sub_reason -> (label, tooltip) for the four partial sub-states + the two terminal states
_SUBREASON_STRINGS = {
    "partial_field":       (LABEL_PARTIAL_FIELD,       TOOLTIP_PARTIAL_FIELD),
    "missing_ingredients": (LABEL_MISSING_INGREDIENTS, TOOLTIP_MISSING_INGREDIENTS),
    "missing_nutrition":   (LABEL_MISSING_NUTRITION,   TOOLTIP_MISSING_NUTRITION),
    "inferred_category":   (LABEL_INFERRED_CATEGORY,   TOOLTIP_INFERRED_CATEGORY),
    "low_extraction":      (LABEL_LOW_EXTRACTION,      TOOLTIP_LOW_EXTRACTION),
}

# Core macro drivers — the panel "spine" (density / calorie / fat dimensions).
MACRO_DRIVERS = ("energy_kcal", "protein_g", "carbohydrates_g", "fat_g")
# Secondary nutrients — a single one missing is a State-2 partial_field ("one
# non-fatal field missing", policy R4 example: "fiber, or sugars/sat-fat"); two or
# more missing, or any CORE driver missing, is a State-4 thin panel (missing_nutrition).
SECONDARY_FIELDS = ("dietary_fiber_g", "sugars_g", "fat_saturated_g", "sodium_mg")


def _l1(trace):
    return trace.get("L1_observed_signals") or {}


def _panel_present(trace):
    """Nutrition panel present with >=1 of the 4 macro drivers non-null."""
    l1 = _l1(trace)
    for k in MACRO_DRIVERS:
        v = l1.get(k)
        if v is not None:
            return True
    return False


def _ingredients_present(trace):
    """Ingredient list present and non-empty (read from trace, not redacted JSON)."""
    l1 = _l1(trace)
    il = l1.get("ingredient_list")
    if il is None:
        il = trace.get("ingredient_list")
    if isinstance(il, (list, tuple)):
        return len([x for x in il if x]) > 0
    if isinstance(il, str):
        return len(il.strip()) > 0
    cnt = l1.get("ingredient_count")
    return bool(cnt and cnt > 0)


def _missing_field_set(trace):
    """Union of trace-declared missing fields and any null core/secondary field."""
    l1 = _l1(trace)
    missing = set()
    mnf = l1.get("missing_nutrition_fields")
    if isinstance(mnf, (list, tuple)):
        missing.update(mnf)
    for k in MACRO_DRIVERS + SECONDARY_FIELDS:
        if l1.get(k) is None:
            missing.add(k)
    return missing


def _panel_thinness(trace):
    """
    Classify a present-but-incomplete panel:
      'thin'    -> State 4 missing_nutrition  (a CORE driver missing, or >=2 secondary missing)
      'single'  -> State 2 partial_field      (exactly ONE secondary field missing)
      None      -> panel complete (no caveat from nutrition completeness)
    """
    missing = _missing_field_set(trace)
    if not missing:
        return None
    core_missing = [k for k in MACRO_DRIVERS if k in missing]
    secondary_missing = [k for k in SECONDARY_FIELDS if k in missing]
    if core_missing:
        return "thin"                 # a load-bearing driver is absent -> State 4
    if len(secondary_missing) >= 2:
        return "thin"                 # multiple secondary fields absent -> State 4
    if len(secondary_missing) == 1:
        return "single"               # one secondary field absent -> State 2
    return None


def _inferred_category(trace):
    cc = trace.get("category_confidence")
    flag = trace.get("category_instability_flag")
    return cc is not None and cc < CAT_CONF_MEDIUM and bool(flag)


def _extraction_low(trace):
    """State-6 CATEGORICAL proxy ONLY (numeric extraction_confidence is backlog)."""
    l1 = _l1(trace)
    itq = l1.get("ingredient_text_quality") or trace.get("ingredient_text_quality")
    ncb = trace.get("nova_confidence_band")
    if itq in ("corrupted", "malformed", "marketing_bleed"):
        return True
    if ncb == "low":
        return True
    return False


def derive_from_trace(trace):
    """
    First-match-wins R0..R6. Returns (confidence, sub_reason) where
    confidence in {verified, partial, insufficient} and sub_reason is the
    partial sub-state or None (states 1 & 7).
    """
    data_suff = trace.get("data_sufficiency")
    conf_band = trace.get("confidence_band")
    panel = _panel_present(trace)
    ingr = _ingredients_present(trace)

    # ---- SUPPRESS (insufficient / State 7) -----------------------------------
    if data_suff == "insufficient" or conf_band == "insufficient":   # R0
        return "insufficient", None
    if (not panel) and (not ingr):                                   # R1
        return "insufficient", None
    if not panel:                                                    # R2 (panel is the spine)
        return "insufficient", None

    # ---- SCORE-WITH-CAVEAT (partial) — first matching condition wins ----------
    # Order per task instruction: missing_ingredients -> missing_nutrition (thin) ->
    # inferred_category -> low_extraction -> partial_field (residual).
    if panel and not ingr:                                           # R3 -> State 3
        return "partial", "missing_ingredients"

    thinness = _panel_thinness(trace)
    if thinness == "thin":                                           # State 4 (thin panel)
        return "partial", "missing_nutrition"

    if _inferred_category(trace):                                    # R5 -> State 5
        return "partial", "inferred_category"

    if _extraction_low(trace):                                       # R6 -> State 6
        return "partial", "low_extraction"

    if thinness == "single":                                         # R4 -> State 2 (one field)
        return "partial", "partial_field"

    # ---- residual: a band-driven partial with no specific gap -> State 2 ------
    if conf_band in ("low", "medium") or data_suff == "partial":
        return "partial", "partial_field"

    # ---- complete / verified (State 1) ---------------------------------------
    return "verified", None


def strings_for(confidence, sub_reason):
    """Return (confidence_label_he, confidence_tooltip_he) for a derived state."""
    if confidence == "verified":
        return LABEL_VERIFIED, TOOLTIP_VERIFIED
    if confidence == "insufficient":
        return LABEL_INSUFFICIENT, TOOLTIP_INSUFFICIENT
    # partial
    return _SUBREASON_STRINGS.get(sub_reason, (LABEL_PARTIAL_FIELD, TOOLTIP_PARTIAL_FIELD))


def annotate(confidence, sub_reason):
    """Build the four-field dict from a derived (confidence, sub_reason)."""
    label, tooltip = strings_for(confidence, sub_reason)
    return {
        "confidence": confidence,
        "confidence_label_he": label,
        "confidence_tooltip_he": tooltip,
        "confidence_sub_reason": sub_reason,  # None for states 1 & 7
    }


def annotate_from_trace(trace):
    confidence, sub_reason = derive_from_trace(trace)
    return annotate(confidence, sub_reason)


# --- Fallback for the 52 products whose live id-scheme does not join a trace ---
# (bread/olive/crackers/cheese — verified in the threshold report §3 to all carry a
#  full nutrition panel and to be already verified/partial, NEVER insufficient).
# This path NEVER produces `insufficient`: it trusts the already-trace-derived
# `confidence` enum that the original build script wrote into the JSON, and
# assigns the residual partial sub-reason. It cannot suppress a displayed score.
def annotate_fallback(existing_confidence):
    c = existing_confidence if existing_confidence in ("verified", "partial") else "partial"
    sub = None if c == "verified" else "partial_field"
    return annotate(c, sub)
