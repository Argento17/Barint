"""
BSIP2-061 — Water-to-Primary Ingredient Predominance
Experimental pilot implementation — Option B only.

Governance reference: bsip2_061_water_predominance_pilot.md (TASK-048)
Implementation task:  TASK-051

Status: EXPERIMENTAL — no production deployment, no website changes.
Scoring: Option B only — operates inside whole_food_integrity dimension.
Maximum final score impact: -4 points.
Do NOT implement Option C here.
"""
from __future__ import annotations

SIGNAL_ID      = "BSIP2-061"
SIGNAL_VERSION = "pilot_v1"

# ---------------------------------------------------------------------------
# Water detection terms
# ---------------------------------------------------------------------------
WATER_TERMS_HE = ["מים", "מי ברז", "מי מעיין", "מי שתיה", "מי עין", "מי נביעות"]
WATER_TERMS_EN = ["water"]

# ---------------------------------------------------------------------------
# Primary functional ingredients by broad category
# ---------------------------------------------------------------------------
CHICKPEA_TERMS = ["חומוס", "גרגירי חומוס", "מחית חומוס", "chickpeas", "garbanzo"]
TAHINI_TERMS   = ["טחינה", "שומשום", "sesame", "tahini"]
EGGPLANT_TERMS = ["חציל", "חצילים", "eggplant", "aubergine"]
PEPPER_TERMS   = ["פלפל", "פלפלים", "פפריקה", "pepper", "paprika"]
TOMATO_TERMS   = ["עגבנ", "רכז עגב", "רסק עגב"]   # prefix covers עגבניות, עגבנייה etc.
NUT_TERMS      = ["בוטנים", "שקדים", "קשיו", "אגוזים", "פיסטוקים",
                  "peanut", "almond", "cashew", "walnut", "pistachio"]
DAIRY_TERMS    = ["שמנת", "גבינה", "קוטג'", "יוגורט", "חלב", "לאבנה",
                  "cream", "cheese", "yogurt", "milk"]

# Naturally high-water vegetables — water preceding these is less diagnostic
HIGH_WATER_VEG_TERMS = EGGPLANT_TERMS + PEPPER_TERMS + TOMATO_TERMS + [
    "מלפפון", "cucumber", "קישוא", "zucchini",
]

# ---------------------------------------------------------------------------
# Matbucha detection terms
# ---------------------------------------------------------------------------
MATBUCHA_NAME_TERMS = ["מטבוחה", "מטבוחה", "סלט טורקי"]

# ---------------------------------------------------------------------------
# Hard-exclusion archetype names (route categories that suppress the signal)
# ---------------------------------------------------------------------------
EXCLUDED_CATEGORIES = {"beverage", "bread", "crispbread", "cracker", "cereal",
                        "snack_bar_granola", "soup", "fruit_puree"}

# ---------------------------------------------------------------------------
# Option B scoring weights
# ---------------------------------------------------------------------------
WFI_WEIGHT               = 0.04    # whole_food_integrity dimension weight
WFI_REDUCTION_PREDOMINANT = 40.0   # score points removed from WFI dimension
WFI_REDUCTION_EARLY        = 20.0   # score points removed from WFI dimension


# ---------------------------------------------------------------------------
# Internal helpers
# ---------------------------------------------------------------------------

def _ing_starts_with(ingredient: str, terms: list[str]) -> bool:
    """Return True if the ingredient string starts with any of the given terms."""
    s = ingredient.strip().lower()
    for t in terms:
        t = t.lower()
        if s == t:
            return True
        if s.startswith(t + " ") or s.startswith(t + ",") or s.startswith(t + "(") \
                or s.startswith(t + "*") or s.startswith(t + "[") or s.startswith(t + "%"):
            return True
    return False


def _is_water_ingredient(ingredient: str) -> bool:
    """
    Returns True only if this ingredient IS water — not if water is embedded
    as a sub-ingredient inside a compound ingredient like
    "חומוס מבושל 61% [מים, חומוס, ...]".
    """
    s = ingredient.strip().lower()
    # Must START with a water term to count as a top-level water ingredient
    for w in WATER_TERMS_HE + WATER_TERMS_EN:
        w = w.lower()
        if s == w:
            return True
        if s.startswith(w + " ") or s.startswith(w + ",") or s.startswith(w + "(") \
                or s.startswith(w + "%"):
            return True
    return False


def _detect_primary_functional_ingredient(
    ingredients: list[str],
    category_hint: str
) -> tuple[str, int | None]:
    """
    Determine the primary functional ingredient type and its first occurrence position
    (1-indexed). Returns (ingredient_type, position_or_None).

    ingredient_type is one of:
        "chickpea", "tahini", "nut", "dairy", "eggplant",
        "high_water_veg", "other", "unknown"
    """
    # First check if we can detect type from what's actually listed first
    if ingredients:
        first = ingredients[0]
        if _ing_starts_with(first, CHICKPEA_TERMS):
            # scan for first chickpea position (should be 1, but verify)
            for i, ing in enumerate(ingredients):
                if _ing_starts_with(ing, CHICKPEA_TERMS):
                    return "chickpea", i + 1
            return "chickpea", 1
        if _ing_starts_with(first, TAHINI_TERMS):
            return "tahini", 1
        if _ing_starts_with(first, EGGPLANT_TERMS):
            return "eggplant", 1
        if _ing_starts_with(first, TOMATO_TERMS):
            return "high_water_veg", 1
        if _ing_starts_with(first, PEPPER_TERMS):
            return "high_water_veg", 1
        if _ing_starts_with(first, NUT_TERMS):
            return "nut", 1
        if _ing_starts_with(first, DAIRY_TERMS):
            return "dairy", 1

    # If first ingredient didn't tell us, scan based on category hint
    # For hummus category, scan for chickpeas anywhere in the list
    if category_hint in ("hummus", "sauce_spread", "savory_spread", "whole_food_fat"):
        # Try chickpeas first
        for i, ing in enumerate(ingredients):
            if _ing_starts_with(ing, CHICKPEA_TERMS):
                return "chickpea", i + 1
        # Then tahini
        for i, ing in enumerate(ingredients):
            if _ing_starts_with(ing, TAHINI_TERMS):
                return "tahini", i + 1
        # Then eggplant
        for i, ing in enumerate(ingredients):
            if _ing_starts_with(ing, EGGPLANT_TERMS):
                return "eggplant", i + 1

    return "unknown", None


def _is_matbucha(name_he: str, ingredients: list[str]) -> bool:
    """Return True if the product is a matbucha (flagged for manual review)."""
    name_lower = (name_he or "").lower()
    for term in MATBUCHA_NAME_TERMS:
        if term in name_lower:
            return True
    # Also detect by primary ingredient (tomato-based)
    if ingredients:
        first = ingredients[0].lower()
        for t in TOMATO_TERMS:
            if first.startswith(t):
                return True
    return False


def _is_high_water_veg_product(ing_type: str) -> bool:
    return ing_type in ("eggplant", "high_water_veg")


# ---------------------------------------------------------------------------
# Main evaluation function
# ---------------------------------------------------------------------------

def evaluate_water_predominance(
    product: dict,
    category: str,
    wfi_score_current: float | None = None,
) -> dict:
    """
    Evaluate BSIP2-061 Water Predominance signal for a product.

    Parameters
    ----------
    product : dict
        BSIP1 canonical product record (or equivalent with ingredients_list, etc.)
    category : str
        Routed category from BSIP2 trace (e.g. "sauce_spread", "beverage")
    wfi_score_current : float | None
        Current whole_food_integrity score from the BSIP2 trace. Used to compute
        the clamped post-reduction WFI score. If None, delta impact is computed
        without clamping.

    Returns
    -------
    dict with keys:
        signal_id, signal_version, state, water_position, functional_type,
        functional_position, wfi_reduction, final_score_delta, note,
        is_matbucha_review, is_false_positive_candidate, penalty_stack_entry
    """
    name_he     = product.get("canonical_name_he") or ""
    ingredients = list(product.get("ingredients_list") or [])

    # ------------------------------------------------------------------
    # Step 0 — Category hard exclusion
    # ------------------------------------------------------------------
    if category in EXCLUDED_CATEGORIES:
        return _result(
            state="NOT_EVALUABLE",
            note=f"category '{category}' is hard-excluded from BSIP2-061",
            water_pos=None, func_type="n/a", func_pos=None,
            wfi_reduction=0.0, final_delta=0.0,
            is_matbucha=False, is_fp_candidate=False,
        )

    # ------------------------------------------------------------------
    # Step 1 — Ingredient list check
    # ------------------------------------------------------------------
    if len(ingredients) < 2:
        return _result(
            state="NOT_EVALUABLE",
            note="ingredient list absent or too short (< 2 items)",
            water_pos=None, func_type="unknown", func_pos=None,
            wfi_reduction=0.0, final_delta=0.0,
            is_matbucha=False, is_fp_candidate=False,
        )

    # ------------------------------------------------------------------
    # Step 2 — Matbucha detection (manual review, no auto-score)
    # ------------------------------------------------------------------
    is_matbucha = _is_matbucha(name_he, ingredients)

    # ------------------------------------------------------------------
    # Step 3 — Detect water position (1-indexed, scan positions 1–2 only)
    # ------------------------------------------------------------------
    water_position: int | None = None
    for idx in (0, 1):                     # positions 1 and 2 (0-indexed: 0 and 1)
        if idx < len(ingredients) and _is_water_ingredient(ingredients[idx]):
            water_position = idx + 1       # convert to 1-indexed
            break

    if water_position is None:
        return _result(
            state="NOT_PREDOMINANT",
            note="water not present at position 1 or 2",
            water_pos=None, func_type="n/a", func_pos=None,
            wfi_reduction=0.0, final_delta=0.0,
            is_matbucha=is_matbucha, is_fp_candidate=False,
        )

    # ------------------------------------------------------------------
    # Step 4 — Detect primary functional ingredient
    # ------------------------------------------------------------------
    func_type, func_position = _detect_primary_functional_ingredient(
        ingredients, category_hint=category
    )

    if func_type == "unknown" or func_position is None:
        return _result(
            state="NOT_EVALUABLE",
            note=f"primary functional ingredient not detectable (type={func_type})",
            water_pos=water_position, func_type=func_type, func_pos=None,
            wfi_reduction=0.0, final_delta=0.0,
            is_matbucha=is_matbucha, is_fp_candidate=False,
        )

    # ------------------------------------------------------------------
    # Step 5 — Matbucha: flag but do not auto-score
    # ------------------------------------------------------------------
    if is_matbucha:
        return _result(
            state="MATBUCHA_MANUAL_REVIEW",
            note=(
                f"Matbucha product — manual review required before BSIP2-061 scoring. "
                f"water_position={water_position}, functional={func_type} at pos {func_position}. "
                f"Tomato natural water vs. added water is unresolvable from label alone."
            ),
            water_pos=water_position, func_type=func_type, func_pos=func_position,
            wfi_reduction=0.0, final_delta=0.0,
            is_matbucha=True, is_fp_candidate=True,
        )

    # ------------------------------------------------------------------
    # Step 6 — Naturally high-water vegetable handling
    # Per spec decision tree: if primary is high-water veg AND water is
    # listed before it → WATER_EARLY (not WATER_PREDOMINANT).
    # ------------------------------------------------------------------
    is_high_water = _is_high_water_veg_product(func_type)

    # ------------------------------------------------------------------
    # Step 7 — Classify signal state
    # ------------------------------------------------------------------
    if func_position <= 2:
        # Functional ingredient is also in positions 1 or 2 → WATER_EARLY
        state = "WATER_EARLY"
        wfi_reduction = WFI_REDUCTION_EARLY
        note = (
            f"water at pos {water_position}, "
            f"{func_type} at pos {func_position} (both in top-2) → WATER_EARLY. "
            f"WFI reduced by {wfi_reduction:.0f} pts."
        )
        is_fp = False
    else:
        # Functional ingredient at position 3+ → WATER_PREDOMINANT or WATER_EARLY (high-water veg)
        if is_high_water:
            state = "WATER_EARLY"
            wfi_reduction = WFI_REDUCTION_EARLY
            note = (
                f"water at pos {water_position}, {func_type} (naturally high-water veg) "
                f"at pos {func_position}. Per spec: WATER_EARLY for high-water vegetables."
            )
            is_fp = False
        else:
            state = "WATER_PREDOMINANT"
            wfi_reduction = WFI_REDUCTION_PREDOMINANT
            # False positive candidate check: if the FIRST ingredient is tahini-dominant
            # (product is tahini-enriched hummus), water between tahini and chickpeas
            # may be architecturally expected.
            first_is_tahini = _ing_starts_with(ingredients[0], TAHINI_TERMS) if ingredients else False
            is_fp = first_is_tahini and func_type == "chickpea"
            fp_note = (
                " POTENTIAL FALSE POSITIVE: first ingredient is tahini "
                f"({ingredients[0][:40]}); water between tahini and chickpeas may be "
                "architecturally expected in tahini-enriched hummus."
            ) if is_fp else ""
            note = (
                f"water at pos {water_position}, "
                f"{func_type} at pos {func_position} (>2) → WATER_PREDOMINANT. "
                f"WFI reduced by {wfi_reduction:.0f} pts.{fp_note}"
            )

    # ------------------------------------------------------------------
    # Step 8 — Compute score delta (Option B: within WFI dimension)
    # ------------------------------------------------------------------
    raw_delta = wfi_reduction * WFI_WEIGHT    # e.g. 40 × 0.04 = 1.6 pts

    # Clamp: if current WFI score minus reduction goes below 0, the effective
    # reduction is smaller.
    if wfi_score_current is not None:
        effective_wfi_new = max(0.0, wfi_score_current - wfi_reduction)
        effective_delta   = (wfi_score_current - effective_wfi_new) * WFI_WEIGHT
    else:
        effective_wfi_new = None
        effective_delta   = raw_delta

    return _result(
        state=state,
        note=note,
        water_pos=water_position,
        func_type=func_type,
        func_pos=func_position,
        wfi_reduction=wfi_reduction,
        final_delta=round(effective_delta, 2),
        is_matbucha=is_matbucha,
        is_fp_candidate=is_fp,
        wfi_score_current=wfi_score_current,
        wfi_score_new=effective_wfi_new,
    )


def _result(
    state: str,
    note: str,
    water_pos,
    func_type,
    func_pos,
    wfi_reduction: float,
    final_delta: float,
    is_matbucha: bool,
    is_fp_candidate: bool,
    wfi_score_current=None,
    wfi_score_new=None,
) -> dict:
    return {
        "signal_id":              SIGNAL_ID,
        "signal_version":         SIGNAL_VERSION,
        "state":                  state,
        "water_position":         water_pos,
        "functional_type":        func_type,
        "functional_position":    func_pos,
        "wfi_reduction_pts":      wfi_reduction,
        "wfi_score_before":       wfi_score_current,
        "wfi_score_after":        wfi_score_new,
        "final_score_delta":      -final_delta if final_delta > 0 else 0.0,
        "is_matbucha_review":     is_matbucha,
        "is_false_positive_candidate": is_fp_candidate,
        "note":                   note,
        "option":                 "B",
        "scoring_rule":           "within whole_food_integrity dimension; max -4 pts final",
    }
