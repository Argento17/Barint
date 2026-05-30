"""
BSIP2 Router v2

Three-stage routing:
  Stage 1  Hard anchor check — product name only; settles routing immediately.
  Stage 2  Context-gated signal scoring with scope-controlled field access.
  Stage 3  Resolution — primary/secondary, hybrid detection, instability flagging.

Drop-in replacement for category_classifier.classify_category().
Output schema is a strict superset of category_classifier output — all existing
keys are preserved; new routing-trace keys are additive and do not break callers.

Key improvements over v1 (category_classifier.py):
  - Hard anchors prevent nut/oil ingredient signals from overwhelming product-name signals
  - context_gated scope stops ingredient text contaminating WFF routing for granola/cereal
  - name_weighted scope gives product-name signals 2× weight vs ingredient text
  - Flavor descriptor suppression generalized (was dairy-only; now applies to anchors too)
  - Hybrid detection for products that genuinely straddle two contexts
  - Full routing trace: suppressed signals, anchor triggers, instability rationale
"""

from __future__ import annotations

ROUTER_VERSION = "router_v2"

CATEGORIES = [
    "whole_food_fat",
    "snack_bar_granola",
    "dessert",
    "beverage",
    "dairy_protein",
    "cereal",
    "sauce_spread",
    # Bakery archetypes (v2 addition)
    "bread",
    "cracker",
    "crispbread",
    "default",
]

# ---------------------------------------------------------------------------
# Stage 1 — Hard Anchors
# ---------------------------------------------------------------------------
# Ordered longest/most-specific first so a more specific term wins on ties.
# Format: (term, category, subtype, confidence)
# Matching: substring in canonical_name_he (lowercased).

HARD_ANCHORS: list[tuple[str, str, str | None, float]] = [
    # ── Bakery — most specific first (crispbread before "לחם") ───────────────
    ("לחמי קריספ",     "crispbread",        "crispbread",     0.94),
    ("קנקבד",          "crispbread",        "knackebrod",     0.95),
    ("קריספ-ברד",      "crispbread",        "crispbread",     0.93),
    ("קרקר",           "cracker",           "cracker",        0.93),
    ("פריכיות",        "cracker",           "puffed_cracker", 0.88),
    ("בגט",            "bread",             "baguette",       0.92),
    ("לחמנייה",        "bread",             "bread_roll",     0.92),
    ("פיתה",           "bread",             "flatbread",      0.90),
    ("לאפה",           "bread",             "flatbread",      0.88),
    ("לחם",            "bread",             "bread",          0.90),
    # ── Nut butters — must appear before bare "חמאת" ─────────────────────────
    ("חמאת בוטנים",    "whole_food_fat",    "peanut_butter",  0.93),
    ("חמאת שקדים",     "whole_food_fat",    "nut_butter",     0.93),
    ("חמאת קשיו",      "whole_food_fat",    "nut_butter",     0.93),
    ("חמאת פיסטוקים",  "whole_food_fat",    "nut_butter",     0.92),
    ("חמאת אגוזים",    "whole_food_fat",    "nut_butter",     0.92),
    # ── Cereals ───────────────────────────────────────────────────────────────
    ("דגני בוקר",      "cereal",            None,             0.92),
    ("גרנולה לבוקר",   "cereal",            "granola_cereal", 0.90),
    ("קורנפלקס",       "cereal",            "cornflakes",     0.93),
    ("קרנפלקס",        "cereal",            "cornflakes",     0.93),
    ("שיבולת שועל",    "cereal",            "oatmeal",        0.88),
    # ── Snack bars ────────────────────────────────────────────────────────────
    ("מוסלי",          "snack_bar_granola", "muesli",         0.88),
    ("גרנולה",         "snack_bar_granola", "granola",        0.90),
    # ── Dairy ─────────────────────────────────────────────────────────────────
    ("קוטג'",          "dairy_protein",     "cottage",        0.93),
    ("יוגורט",         "dairy_protein",     "yogurt",         0.92),
    ("קפיר",           "dairy_protein",     "kefir",          0.93),
    # ── Whole-food fats ───────────────────────────────────────────────────────
    ("טחינה",          "whole_food_fat",    "tahini",         0.93),
    # ── Dairy desserts (מעדנים) ─────────────────────────────────────────────────
    ("מילקי",          "dessert",           "milky_style",    0.96),
    ("מעדן חלבון",     "dessert",           "protein_dessert",0.95),
    ("מעדן ילדים",     "dessert",           "kids_dessert",   0.95),
    ("מעדן",           "dessert",           "dairy_dessert",  0.90),
    ("עדנה",           "dessert",           "dairy_dessert",  0.93),
    ("פרוביו",         "dessert",           "probiotic_dessert", 0.92),
    ("יופלה",          "dessert",           "flavored_yogurt_dessert", 0.91),
]

# Anchors that require the matched term to appear at the START of the product name
# (i.e., it IS the product, not a flavor descriptor like "בטעם שיבולת שועל").
ANCHOR_REQUIRES_POSITION_CHECK: set[str] = {
    "שיבולת שועל",   # "לחם שיבולת שועל" = bread, not oatmeal
}

# For dairy anchors: suppress if the term appears AFTER a flavor descriptor
# in the product name ("בטעם יוגורט" = yogurt-flavored, not a yogurt product).
DAIRY_ANCHOR_TERMS: set[str] = {"יוגורט", "קפיר", "קוטג'", "גבינה", "לבן"}
DAIRY_FLAVOR_SUPPRESSORS: list[str] = ["בטעם", "טעם", "בניחוח"]

# If name contains these exclusion terms, the specified anchor should not fire.
ANCHOR_EXCLUSIONS: dict[str, list[str]] = {
    # "שיבולת שועל" must not fire for oat drinks (beverage) or snack bars using oats as ingredient
    "שיבולת שועל":    ["לחם", "עוגיות", "מאפה", "ביסקוויט", "פריכיות",
                       "משקה", "שתייה", "חטיפי", "חטיף", "ברים"],
    # Nut butter anchors must not fire when the butter is a FILLING, not the product itself
    "חמאת בוטנים":    ["חטיף", "מילוי", "עוגיות", "שכבת"],
    "חמאת שקדים":     ["חטיף", "מילוי", "עוגיות", "שכבת"],
    "חמאת קשיו":      ["חטיף", "מילוי", "שכבת"],
    "חמאת פיסטוקים":  ["חטיף", "מילוי", "שכבת"],
    "חמאת אגוזים":    ["חטיף", "מילוי", "שכבת"],
    # Bread: don't fire on snack bars or spreads that use "לחם" in name
    "לחם":            ["חטיף", "ממרח", "קרם"],
    # Cracker: "קרקר" in filling context (e.g., coated snacks) — rare, keep clean
    "קרקר":           [],
    # Crispbread: "לחמי קריספ" is highly specific; no exclusions needed
    "לחמי קריספ":     [],
    # Puffed crackers: "פריכיות" must not fire when it's a pure oat-drink brand context
    "פריכיות":        ["משקה", "שתייה"],
    # Dairy dessert anchors — prevent mis-fires
    "מעדן":           ["אבקת", "מיקס", "שייק"],     # "אבקת מעדן" = powder, not shelf dessert
    "עדנה":           ["גבינת", "שמנת", "חמאת"],    # "גבינת עדנה" = soft cheese brand
    "יופלה":          [],
    "פרוביו":         [],
    "מילקי":          [],
    "מעדן חלבון":     [],
    "מעדן ילדים":     [],
}


def _check_anchors(name: str) -> tuple[str, str | None, float, str] | None:
    """Return (category, subtype, confidence, matched_term) if any anchor fires, else None."""
    best: tuple[str, str | None, float, str] | None = None

    for term, cat, subtype, conf in HARD_ANCHORS:
        if term not in name:
            continue

        # Per-term exclusion list
        if any(excl in name for excl in ANCHOR_EXCLUSIONS.get(term, [])):
            continue

        # Position check: term must not appear as a suffix/modifier after other nouns
        if term in ANCHOR_REQUIRES_POSITION_CHECK:
            idx = name.find(term)
            # Allow only if term appears near the start (first 25 chars) or no other
            # category term precedes it
            if idx > 20:
                continue

        # Dairy flavor suppression: suppress if term appears after "בטעם"
        if term in DAIRY_ANCHOR_TERMS:
            idx = name.find(term)
            prefix = name[max(0, idx - 15):idx]
            if any(sup in prefix for sup in DAIRY_FLAVOR_SUPPRESSORS):
                continue

        # Higher confidence wins; on tie, longer term wins (more specific)
        if best is None or conf > best[2] or (conf == best[2] and len(term) > len(best[3])):
            best = (cat, subtype, conf, term)

    return best


# ---------------------------------------------------------------------------
# Stage 2 — Signal Definitions
# ---------------------------------------------------------------------------
# Scope controls which text fields each signal is allowed to match:
#
#   "name_only"     — canonical_name_he only; never ingredient text
#   "name_weighted" — name at 2× weight + ingredient text at 0.5× weight
#   "context_gated" — ingredient text fires ONLY if name passes a category context gate
#                     (in name → treated as name_weighted at 1.5×)
#   "full_text"     — name + ingredient text at full weight (legacy behavior)

# Whole-food-fat signals:
# Nuts, seeds, raw oils in ingredient text are context_gated — they must not
# hijack routing when a granola/cereal/snack product happens to contain them.
_WFF: list[tuple[str, float, str]] = [
    ("שמן זית",      0.95, "context_gated"),
    ("שמן קוקוס",    0.90, "context_gated"),
    ("שמן",          0.50, "name_weighted"),    # "שמן X" in name → oil product
    ("טחינה",        0.80, "name_weighted"),    # anchor handles most; backup
    ("חמאה",         0.65, "name_only"),        # dairy butter — only if IS the product
    ("אגוז",         0.65, "context_gated"),
    ("אגוזים",       0.65, "context_gated"),
    ("שקד",          0.65, "context_gated"),
    ("גרעין",        0.55, "context_gated"),
    ("גרעינים",      0.55, "context_gated"),
    ("אבוקדו",       0.90, "name_weighted"),
    ("זית",          0.45, "context_gated"),
    ("שומשום",       0.65, "context_gated"),
    ("כוסמת",        0.20, "context_gated"),
    ("ממרח",         0.40, "name_weighted"),
    ("חמאת",         0.70, "name_weighted"),    # nut-butter prefix
]

_SNACK: list[tuple[str, float, str]] = [
    ("חטיף דגנים",   0.95, "name_weighted"),
    ("חטיף",         0.50, "name_weighted"),
    ("גרנולה",       0.90, "name_weighted"),
    ("קורני",        0.90, "name_weighted"),
    ("כורני",        0.90, "name_weighted"),
    ("מוסלי",        0.80, "name_weighted"),
    ("ברים",         0.70, "name_weighted"),
    ("בר ",          0.40, "name_weighted"),    # trailing space avoids false matches
    ("צ'יה",         0.30, "full_text"),
    ("אנרגיה",       0.30, "name_weighted"),
    ("דגנים",        0.35, "name_weighted"),
    ("שוקולד",       0.25, "name_weighted"),    # weak; also dessert
    ("קריספי",       0.40, "name_weighted"),
    ("פצפוצי",       0.60, "name_weighted"),
    ("ציפוי",        0.25, "name_weighted"),
    ("שוקו",         0.30, "name_weighted"),
    ("וופל",         0.40, "name_weighted"),
    ("ביסקוויט",     0.50, "name_weighted"),
    ("מילוי קרם",    0.50, "name_weighted"),
    ("מילוי",        0.30, "name_weighted"),
    ("שכבת",         0.30, "name_weighted"),
    ("קרמל",         0.25, "name_weighted"),
    ("בוטנים",       0.35, "name_weighted"),
]

_DESSERT: list[tuple[str, float, str]] = [
    ("עוגה",         0.85, "name_weighted"),
    ("קינוח",        0.85, "name_weighted"),
    ("קרם",          0.45, "name_weighted"),
    ("פודינג",       0.80, "name_weighted"),
    ("מוס",          0.85, "name_weighted"),
    ("גלידה",        0.90, "name_weighted"),
    ("שוקולד",       0.25, "name_weighted"),
    ("טארט",         0.90, "name_weighted"),
    ("מאפה",         0.75, "name_weighted"),
    ("סופגניה",      0.95, "name_weighted"),
    ("רולדה",        0.85, "name_weighted"),
    ("בראוניז",      0.90, "name_weighted"),
    ("פרלינה",       0.80, "name_weighted"),
    # ── Dairy dessert specific ─────────────────────────────────────────────────
    # Hard anchors above handle the primary brands; signals reinforce ambiguous cases
    ("מעדן",         0.80, "name_weighted"),   # backup signal (anchors cover exact matches)
    ("מעדן פרוטאין", 0.88, "name_weighted"),
    ("קרם דסרט",     0.85, "name_weighted"),
    ("פנה קוטה",     0.90, "name_weighted"),
    ("קרם ברולה",    0.90, "name_weighted"),
    ("מוס גבינה",    0.90, "name_weighted"),
    ("ללא סוכר",     0.20, "name_weighted"),   # weak modifier — supports dessert context
]

_CEREAL: list[tuple[str, float, str]] = [
    ("דגני בוקר",    0.95, "name_weighted"),
    ("קורנפלקס",     0.95, "name_weighted"),
    ("שיבולת שועל",  0.70, "name_weighted"),    # anchor handles primary oatmeal
    ("גרנולה לבוקר", 0.90, "name_weighted"),
    ("וולה",         0.90, "name_weighted"),
    ("קרנפלקס",      0.90, "name_weighted"),
    ("פתיתי",        0.45, "name_weighted"),
    ("אוברן",        0.70, "name_weighted"),
]

_SAUCE: list[tuple[str, float, str]] = [
    ("רוטב",         0.90, "name_weighted"),
    ("ממרח",         0.65, "name_weighted"),
    ("קטשופ",        0.95, "name_weighted"),
    ("חרדל",         0.90, "name_weighted"),
    ("מיונז",        0.95, "name_weighted"),
    ("חומוס",        0.85, "name_weighted"),
    ("טפנד",         0.90, "name_weighted"),
    ("ממרח שוקולד",  0.95, "name_weighted"),
    ("הלב",          0.40, "name_weighted"),
    ("פסטה",         0.35, "name_weighted"),
    ("ציר",          0.65, "name_weighted"),
]

# Beverages and dairy are name_only — ingredient-text contamination was the
# original failure mode for both; this design has been correct since v1.
_BEVERAGE: list[tuple[str, float, str]] = [
    ("משקה",         0.90, "name_only"),
    ("שתייה",        0.90, "name_only"),
    ("מיץ",          0.90, "name_only"),
    ("תה",           0.85, "name_only"),
    ("קפה",          0.85, "name_only"),
    ("מים",          0.70, "name_only"),
    ("לימונדה",      0.90, "name_only"),
    ("קולה",         0.95, "name_only"),
    ("סודה",         0.80, "name_only"),
    ("קוקטייל",      0.85, "name_only"),
    ("מיצוי",        0.60, "name_only"),
]

_DAIRY: list[tuple[str, float, str]] = [
    ("יוגורט",       0.95, "name_only"),
    ("קוטג'",        0.95, "name_only"),
    ("גבינה",        0.85, "name_only"),
    ("חלב",          0.70, "name_only"),
    ("לבן",          0.60, "name_only"),
    ("קפיר",         0.95, "name_only"),
    ("ריקוטה",       0.90, "name_only"),
    ("מסקרפונה",     0.90, "name_only"),
]

# Bakery signals — name_weighted so specific product-name terms dominate
_CRISPBREAD: list[tuple[str, float, str]] = [
    ("קריספ",          0.70, "name_weighted"),   # "crisp" in any compound
    ("נורדי",          0.65, "name_weighted"),   # Nordic crispbread style
    ("שיפון",          0.50, "name_weighted"),   # rye (common in crispbread)
    ("כוסמת",          0.50, "name_weighted"),   # buckwheat crispbread
]

_CRACKER: list[tuple[str, float, str]] = [
    ("מלוח",           0.50, "name_weighted"),   # savory/salty (cracker signal)
    ("פריך",           0.55, "name_weighted"),   # crispy/crunchy
    ("עוגיות אורז",    0.70, "name_weighted"),   # rice cakes (common name)
    ("עוגיות",         0.35, "name_weighted"),   # cookies/biscuits (weak — also sweet)
    ("שיפון",          0.35, "name_weighted"),   # rye (also cracker)
]

_BREAD: list[tuple[str, float, str]] = [
    ("מלא",            0.40, "name_weighted"),   # "whole" in bread name
    ("שיפון",          0.35, "name_weighted"),   # rye bread
    ("כוסמין",         0.40, "name_weighted"),   # spelt bread
    ("כפרי",           0.35, "name_weighted"),   # rustic/country bread
    ("מחמצת",          0.40, "name_weighted"),   # sourdough (in name)
    ("אורגני",         0.20, "name_weighted"),   # organic (weak signal)
    ("ביתי",           0.20, "name_weighted"),   # homemade style (weak)
]

ALL_SIGNALS: dict[str, list[tuple[str, float, str]]] = {
    "whole_food_fat":    _WFF,
    "snack_bar_granola": _SNACK,
    "dessert":           _DESSERT,
    "cereal":            _CEREAL,
    "sauce_spread":      _SAUCE,
    "beverage":          _BEVERAGE,
    "dairy_protein":     _DAIRY,
    # Bakery archetypes
    "crispbread":        _CRISPBREAD,
    "cracker":           _CRACKER,
    "bread":             _BREAD,
}

# Context gate for whole_food_fat context_gated signals.
# Ingredient-text nut/oil signals fire ONLY when name has a WFF identity signal.
WFF_NAME_CONTEXT_REQUIRED: list[str] = [
    "ממרח", "חמאת", "שמן", "אגוזים", "גרעינים", "מיקס", "תערובת",
    "אגוזי", "בוטנים", "קשיו", "פיסטוקים",
]
# If name contains any of these, context_gated WFF signals are suppressed regardless.
WFF_NAME_EXCLUSIONS: list[str] = [
    "גרנולה", "מוסלי", "קורנפלקס", "חטיף", "ברים", "עוגה", "לחם",
    "ביסקוויט", "דגני", "פתיתי", "קריספי",
    # Bakery products: seeds in cracker/bread ingredient list must not trigger WFF routing
    "קרקר", "לחמי קריספ", "פריכיות", "בגט", "לחמנייה", "פיתה",
]

# Beverage gate (same logic as v1, preserved exactly)
_BEVERAGE_LIQUID_GATE_KW: list[str] = [
    "ml", 'מ"ל', "ליטר", "בקבוק", "משקה", "שתייה", "שתיה", "מיץ", "קולה", "סודה",
]
_LIQUID_BASIS_TERMS: list[str] = ["ליטר", 'מ"ל', "מל"]
_KNOWN_PLANT_MILK_BRANDS: set[str] = {
    "אלפרו", "alpro", "oatly", "אוטלי", "vitariz", "ויטאריז", "silk", "provamel",
}
_PLANT_MILK_BASE_TERMS: list[str] = [
    "שקדים", "שיבולת שועל", "סויה", "אורז", "קוקוס", "שומשום", "קשיו", "אפונה",
]
_PLANT_MILK_SOLID_EXCL: list[str] = [
    "חמאה", "גבינה", "יוגורט", "גלידה", "קוטג", "ממרח", "שמן",
    "חטיף", "חטיפי", "ברים", "גרנולה", "מצופה", "ציפוי", "ביסקוויט", "דגנים",
    # Bakery solids: "עוגיות אורז" (rice cakes) must not be treated as rice milk
    "עוגיות", "קרקר", "לחם", "פריכיות", "לחמי",
]

# Hybrid-eligible routing pairs — products that legitimately straddle two contexts.
# Only these pairs trigger is_hybrid=True; all others get instability_flag only.
HYBRID_ELIGIBLE_PAIRS: frozenset = frozenset({
    frozenset({"snack_bar_granola", "cereal"}),
    frozenset({"dairy_protein", "beverage"}),
    frozenset({"cereal", "whole_food_fat"}),
    frozenset({"snack_bar_granola", "whole_food_fat"}),
    frozenset({"dairy_protein", "dessert"}),
    # Bakery hybrids
    frozenset({"cracker", "snack_bar_granola"}),   # sweet crackers
    frozenset({"crispbread", "cracker"}),          # compressed-grain crispbread / thick cracker
    frozenset({"bread", "cracker"}),               # very dense baked flat bread / cracker-bread
})


# ---------------------------------------------------------------------------
# Supplement quarantine — additive detection, does not change routing
# ---------------------------------------------------------------------------

def _check_supplement_quarantine(name: str, ing_text: str) -> dict | None:
    """
    Detect protein powders and meal replacements outside the current food ontology.
    Returns a quarantine signal dict if detected, else None.
    Does not change routing — result is additive field only.
    """
    SUPPLEMENT_NAME_SIGNALS = [
        "אבקת חלבון", "שייק חלבון", "תחליף ארוחה", "חלבון ספורט", "אבקת מי גבינה",
    ]
    WHEY_TERMS = ["מי גבינה", "חלבון מי גבינה", "קזאין"]
    SPORT_NAME_KW = ["ספורט", "שייק", "אבקת", "פרוטאין"]

    for sig in SUPPLEMENT_NAME_SIGNALS:
        if sig in name:
            return {"signal": f"name:'{sig}'", "category": "protein_supplement_candidate"}

    has_whey = any(w in ing_text for w in WHEY_TERMS)
    has_maltodextrin = "מלתודקסטרין" in ing_text
    has_sport_name = any(kw in name for kw in SPORT_NAME_KW)
    if has_whey and (has_maltodextrin or has_sport_name):
        trigger = "maltodextrin" if has_maltodextrin else "sport_name"
        return {"signal": f"ing:whey+{trigger}", "category": "protein_supplement_candidate"}

    return None


# ---------------------------------------------------------------------------
# Public entry point
# ---------------------------------------------------------------------------

def classify_category(product: dict) -> dict:
    """
    Three-stage router. Drop-in replacement for category_classifier.classify_category().
    All v1 output keys are preserved; new router-trace keys are additive.
    """
    name     = (product.get("canonical_name_he") or "").lower()
    ing_text = (product.get("ingredients_text_he") or "").lower()
    nn       = product.get("normalized_nutrition_per_100g") or {}

    # Supplement quarantine — run first; injected into result regardless of routing path
    supplement_q = _check_supplement_quarantine(name, ing_text)

    # Pre-anchor bypass: known plant-milk brands skip the hard anchor stage.
    # Grain-type terms like "שיבולת שועל" in "אלפרו שיבולת שועל" must not anchor
    # to cereal — the brand establishes liquid identity before term matching.
    # We add 0.75 here (same as primary_liquid_kw gate) so beverage overcomes
    # any grain-term name_weighted signal in _score_signals.
    # Exception: if name contains a dairy-format anchor term ("יוגורט", "קפיר", etc.),
    # do NOT bypass — "אלפרו יוגורט סויה" is a yogurt product, not a beverage.
    brand      = (product.get("brand") or "").lower()
    name_first = name.split()[0] if name else ""
    _name_has_dairy_anchor = any(t in name for t in DAIRY_ANCHOR_TERMS)
    if (brand in _KNOWN_PLANT_MILK_BRANDS or name_first in _KNOWN_PLANT_MILK_BRANDS) \
            and not _name_has_dairy_anchor:
        scores, signal_log, suppressed_log = _score_signals(name, ing_text, nn)
        scores["beverage"] += 0.75
        signal_log.append("beverage:plant_milk_brand_preboost(0.75)")
        scores, bev_basis, bev_suppressed = _apply_beverage_gate(scores, name, product)
        signal_log.extend(bev_basis)
        suppressed_log.extend(bev_suppressed)
        result = _resolve(scores, signal_log, suppressed_log)
        result["supplement_quarantine"] = supplement_q
        return result

    # Stage 1 — hard anchor
    anchor = _check_anchors(name)
    if anchor:
        cat, subtype, conf, term = anchor
        result = _build_anchor_result(cat, subtype, conf, term, name, ing_text, nn, product)
        result["supplement_quarantine"] = supplement_q
        return result

    # Stage 2 — signal scoring
    scores, signal_log, suppressed_log = _score_signals(name, ing_text, nn)

    # Stage 2b — beverage gate (preserves v1 logic exactly)
    scores, bev_basis, bev_suppressed = _apply_beverage_gate(scores, name, product)
    signal_log.extend(bev_basis)
    suppressed_log.extend(bev_suppressed)

    # Stage 3 — resolution
    result = _resolve(scores, signal_log, suppressed_log)
    result["supplement_quarantine"] = supplement_q
    return result


# ---------------------------------------------------------------------------
# Stage 2 internals
# ---------------------------------------------------------------------------

def _score_signals(
    name: str, ing_text: str, nn: dict
) -> tuple[dict, list[str], list[str]]:
    """Accumulate signal scores with scope gating."""
    scores: dict[str, float] = {cat: 0.0 for cat in CATEGORIES}
    signal_log: list[str] = []
    suppressed_log: list[str] = []

    # Pre-compute WFF name context once
    wff_name_has_context = any(c in name for c in WFF_NAME_CONTEXT_REQUIRED)
    wff_name_has_exclusion = any(e in name for e in WFF_NAME_EXCLUSIONS)

    for cat, signals in ALL_SIGNALS.items():
        for term, weight, scope in signals:
            in_name = term in name
            in_ing  = term in ing_text

            if scope == "name_only":
                if in_name:
                    effective_weight = weight
                    # Dairy flavor suppression: suppress if preceded by "בטעם" etc.
                    if cat == "dairy_protein":
                        idx = name.find(term)
                        prefix = name[max(0, idx - 12):idx]
                        if any(sup in prefix for sup in DAIRY_FLAVOR_SUPPRESSORS):
                            suppressed_log.append(f"{cat}:{term}(flavor_suppressor)")
                            scores[cat] += weight * 0.10
                            continue
                    scores[cat] += effective_weight
                    signal_log.append(f"{cat}:{term}(name)")

            elif scope == "name_weighted":
                if in_name:
                    scores[cat] += weight * 2.0
                    signal_log.append(f"{cat}:{term}(name×2)")
                elif in_ing:
                    scores[cat] += weight * 0.5
                    signal_log.append(f"{cat}:{term}(ing×0.5)")

            elif scope == "context_gated":
                if in_name:
                    # Present in name → treat as name signal at 1.5×
                    scores[cat] += weight * 1.5
                    signal_log.append(f"{cat}:{term}(name_ctx×1.5)")
                elif in_ing:
                    if cat == "whole_food_fat":
                        if wff_name_has_context and not wff_name_has_exclusion:
                            scores[cat] += weight
                            signal_log.append(f"{cat}:{term}(ing_gated)")
                        else:
                            reason = "no_wff_context" if not wff_name_has_context else "wff_excluded"
                            suppressed_log.append(f"{cat}:{term}(suppressed:{reason})")
                    else:
                        # Other categories using context_gated: full-text fallback
                        scores[cat] += weight * 0.5
                        signal_log.append(f"{cat}:{term}(ing×0.5)")

            elif scope == "full_text":
                if in_name or in_ing:
                    scores[cat] += weight
                    signal_log.append(f"{cat}:{term}({'name' if in_name else 'ing'})")

    # Nutritional hints
    hints = _nutritional_hints(nn, name)
    for cat, boost in hints.items():
        if boost > 0:
            scores[cat] += boost
            signal_log.append(f"{cat}:nutrition_hint({boost:.2f})")

    return scores, signal_log, suppressed_log


def _nutritional_hints(nn: dict, name: str) -> dict[str, float]:
    hints = {cat: 0.0 for cat in CATEGORIES}
    kcal = nn.get("energy_kcal") or 0
    fat  = nn.get("fat_g") or 0
    prot = nn.get("protein_g") or 0

    if kcal > 600 and fat > 50:
        hints["whole_food_fat"] += 0.4
    if kcal < 30:
        hints["beverage"] += 0.4
    if prot > 8 and kcal < 200:
        hints["dairy_protein"] += 0.3

    # Stronger cereal/snack_bar hint when calorie density AND name context agree
    has_grain_name = any(g in name for g in ["גרנולה", "דגנים", "קורנפלקס", "שיבולת", "מוסלי", "חטיף"])
    if 350 <= kcal <= 520:
        if has_grain_name:
            hints["snack_bar_granola"] += 0.30
            hints["cereal"] += 0.20
        else:
            hints["snack_bar_granola"] += 0.15

    if kcal >= 500 and fat >= 20:
        hints["whole_food_fat"] += 0.10

    return hints


_PRIMARY_LIQUID_KW: list[str] = ["משקה", "שתייה", "מיץ", "קולה", "לימונדה", "סודה"]


def _apply_beverage_gate(
    scores: dict, name: str, product: dict
) -> tuple[dict, list[str], list[str]]:
    """
    Beverage liquid gate.
    Core logic preserved from v1. v2 addition: primary liquid keywords in name
    ("משקה", "שתייה", "מיץ") add a score boost in addition to the name_only
    signal they already trigger. This prevents grain-type cereal signals (which
    use name_weighted 2×) from outscoring an explicit liquid product identity.
    """
    basis: list[str] = []
    suppressed: list[str] = []

    # v2: primary liquid keyword in name → decisive beverage identity
    has_primary_liquid = any(kw in name for kw in _PRIMARY_LIQUID_KW)
    if has_primary_liquid:
        scores["beverage"] += 0.75
        basis.append("primary_liquid_keyword_boost")
        return scores, basis, suppressed   # gate confirmed; skip fallback checks

    has_liquid = any(kw in name for kw in _BEVERAGE_LIQUID_GATE_KW)
    liquid_boost = 0.0

    if not has_liquid:
        basis_claimed = (product.get("nutrition_basis_claimed") or "").lower()
        if any(t in basis_claimed for t in _LIQUID_BASIS_TERMS):
            has_liquid = True
            liquid_boost = 0.85
            basis.append("nutrition_basis_liquid_volume")

    if not has_liquid:
        brand = (product.get("brand") or "").lower()
        name_first = name.split()[0] if name else ""
        if brand in _KNOWN_PLANT_MILK_BRANDS or name_first in _KNOWN_PLANT_MILK_BRANDS:
            has_liquid = True
            liquid_boost = 0.75
            basis.append("known_plant_milk_brand")

    if not has_liquid:
        has_plant = any(t in name for t in _PLANT_MILK_BASE_TERMS)
        has_solid  = any(t in name for t in _PLANT_MILK_SOLID_EXCL)
        if has_plant and not has_solid:
            has_liquid = True
            liquid_boost = 0.60
            basis.append("plant_milk_name_heuristic")

    if has_liquid:
        scores["beverage"] += liquid_boost
    else:
        if scores["beverage"] > 0:
            suppressed.append(f"beverage:zeroed(no_liquid_context,had={scores['beverage']:.2f})")
        scores["beverage"] = 0.0

    return scores, basis, suppressed


# ---------------------------------------------------------------------------
# Stage 3 — Resolution
# ---------------------------------------------------------------------------

def _resolve(
    scores: dict, signal_log: list[str], suppressed_log: list[str]
) -> dict:
    ranked = sorted(scores.items(), key=lambda x: x[1], reverse=True)
    top_cat, top_score   = ranked[0]
    sec_cat, sec_score   = ranked[1] if len(ranked) > 1 else ("default", 0.0)
    total_signal = sum(s for _, s in ranked)

    # Minimum signal mass — route to default rather than fabricate confidence
    if total_signal < 0.3:
        return _uncertain_result(signal_log, suppressed_log, ranked)

    # Confidence
    if total_signal < 0.1:
        conf = 0.35
        top_cat = "default"
    else:
        relative = top_score / max(total_signal, 0.1)
        conf = min(0.92, max(0.30, relative + 0.15))

    if top_score < 0.5:
        conf = min(conf, 0.55)
    if top_score < 0.3:
        conf = min(conf, 0.40)

    sec_conf = min(0.80, max(0.10, sec_score / max(total_signal, 0.1))) if total_signal > 0 else 0.20

    # Instability
    delta = top_score - sec_score
    instability_flag = delta < 0.3 and conf < 0.80
    instability_warning = None
    if instability_flag:
        instability_warning = (
            f"top-2 delta={delta:.2f}: {top_cat}({top_score:.2f}) vs {sec_cat}({sec_score:.2f})"
        )

    # Hybrid
    is_hybrid = (
        delta < 0.3
        and frozenset({top_cat, sec_cat}) in HYBRID_ELIGIBLE_PAIRS
    )

    band = "high" if conf >= 0.80 else ("medium" if conf >= 0.50 else ("low" if conf >= 0.30 else "uncertain"))

    basis = [s for s in signal_log if s.startswith(top_cat + ":")][:6]
    if not basis:
        basis = signal_log[:4] or ["no_signals_matched"]

    return {
        # --- v1-compatible keys ---
        "category":                   top_cat,
        "category_confidence":        round(conf, 2),
        "secondary_category":         sec_cat if sec_cat != top_cat else "default",
        "secondary_confidence":       round(sec_conf, 2),
        "category_instability_flag":  instability_flag,
        "classification_basis":       basis,
        "confidence_band":            band,
        "raw_category_scores":        {k: round(v, 3) for k, v in ranked},
        # --- v2 routing trace keys ---
        "anchor_override":            False,
        "category_subtype":           None,
        "routing_version":            ROUTER_VERSION,
        "routing_suppressed_signals": suppressed_log,
        "is_hybrid":                  is_hybrid,
        "routing_instability_warning": instability_warning,
    }


def _build_anchor_result(
    cat: str, subtype: str | None, conf: float, term: str,
    name: str, ing_text: str, nn: dict, product: dict
) -> dict:
    """Result for anchor-driven routing (Stage 1 exit)."""
    # Run signal scoring informally to expose secondary candidate in trace
    scores, _, _ = _score_signals(name, ing_text, nn)
    scores, _, _ = _apply_beverage_gate(scores, name, product)
    ranked = sorted(scores.items(), key=lambda x: x[1], reverse=True)

    sec_cat, sec_conf = "default", 0.10
    total = sum(s for _, s in ranked)
    for c, s in ranked:
        if c != cat and s > 0 and total > 0:
            sec_cat  = c
            sec_conf = round(min(0.60, s / total), 2)
            break

    return {
        # --- v1-compatible keys ---
        "category":                   cat,
        "category_confidence":        round(conf, 2),
        "secondary_category":         sec_cat,
        "secondary_confidence":       sec_conf,
        "category_instability_flag":  False,
        "classification_basis":       [f"hard_anchor:{term}"],
        "confidence_band":            "high",
        "raw_category_scores":        {k: round(v, 3) for k, v in ranked},
        # --- v2 routing trace keys ---
        "anchor_override":            True,
        "category_subtype":           subtype,
        "routing_version":            ROUTER_VERSION,
        "routing_suppressed_signals": [],
        "is_hybrid":                  False,
        "routing_instability_warning": None,
    }


def _uncertain_result(signal_log: list, suppressed_log: list, ranked: list) -> dict:
    """Returned when total signal mass < 0.3 — insufficient signal to classify."""
    return {
        "category":                   "default",
        "category_confidence":        0.30,
        "secondary_category":         "default",
        "secondary_confidence":       0.10,
        "category_instability_flag":  True,
        "classification_basis":       ["routing_uncertain:insufficient_signal_mass"],
        "confidence_band":            "uncertain",
        "raw_category_scores":        {k: round(v, 3) for k, v in ranked},
        "anchor_override":            False,
        "category_subtype":           None,
        "routing_version":            ROUTER_VERSION,
        "routing_suppressed_signals": suppressed_log,
        "is_hybrid":                  False,
        "routing_instability_warning": "total_signal_mass<0.3 — routing to default",
    }
