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
import os as _os
from input_loader import get_ingredients as _get_ingredients

ROUTER_VERSION = "router_v2.5"  # TASK-394: BARI_R3_BISCUIT_NARROW_V1 promoted to production-default ON

# ---------------------------------------------------------------------------
# TASK-394 — BARI_R3_BISCUIT_NARROW_V1 (default OFF)
# ---------------------------------------------------------------------------
# When ON: R3 yields (does NOT re-route to snack_bar_granola) when BOTH:
#   (a) the product has a high-confidence BISCUIT hard anchor (anchor_override=True,
#       category before R3 == biscuit, confidence >= _R3_BISCUIT_ANCHOR_CONF_MIN)
#   (b) the ingredients text contains NO positive chocolate-CONFECTIONERY signal
#       (ציפוי שוקולד, מצופה שוקולד, or שוקולד as a leading/dominant ingredient).
#
# Cocoa powder as a minor flavoring is NOT a confectionery signal.
# This preserves: genuine chocolate tablets/bars (no biscuit anchor → R3 still fires),
#                 chocolate-COATED biscuits (confectionery ingredient signal → R3 still fires).
# Only flavor-descriptor biscuits with a strong biscuit anchor are spared.
#
# Flag read at module import (env-before-import discipline — juices bug pattern):
#   import os; os.environ["BARI_R3_BISCUIT_NARROW_V1"] = "on"  BEFORE importing router_v2.
# Default OFF so nothing ships from this flag being set by accident.
BARI_R3_BISCUIT_NARROW_V1: bool = _os.environ.get("BARI_R3_BISCUIT_NARROW_V1", "on").lower() == "on"

# Minimum anchor confidence for condition (a).  All biscuit hard anchors carry 0.85–0.94;
# 0.85 is the lowest (עוגיות plain_cookie), so this threshold admits all genuine biscuit
# hard-anchor routes while a Stage-2 signal-only biscuit result (no anchor, conf <0.80) is
# NOT protected — that is correct behaviour (a signal-only biscuit with "שוקולד" in the
# name should still be reviewed by R3 since the biscuit identity is weaker).
_R3_BISCUIT_ANCHOR_CONF_MIN: float = 0.85

# Positive chocolate-CONFECTIONERY ingredient signals.  Presence of ANY of these means
# the product is genuinely chocolate-confectionery (coated, filled, or leading ingredient)
# — NOT merely flavored — so R3 should still fire.
# "ציפוי שוקולד" = chocolate coating, "מצופה שוקולד" = chocolate-coated,
# "שוקולד מריר" / "שוקולד חלב" as a leading ingredient (block > 5% in the list).
# The test is a substring check against the lowercased ingredients_text_he.
_R3_CHOC_CONFECTIONERY_ING_SIGNALS: frozenset[str] = frozenset({
    "ציפוי שוקולד",   # chocolate coating (most decisive)
    "מצופה שוקולד",   # chocolate-coated descriptor in ingredients
    "שוקולד ציפוי",   # alternative word order for chocolate coating
    "שוקולד מריר",    # dark chocolate as an ingredient (leading = confectionery signal)
    "שוקולד חלב",     # milk chocolate as an ingredient
    "שוקולד לבן",     # white chocolate as an ingredient
    "שוקולד לגנאש",   # ganache — clearly confectionery filling
})

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
    "biscuit",
    # Frozen vegetable (TASK-??? / EV-006 follow-up)
    "frozen_vegetable",
    "default",
]

# ---------------------------------------------------------------------------
# Stage 1 — Hard Anchors
# ---------------------------------------------------------------------------
# Ordered longest/most-specific first so a more specific term wins on ties.
# Format: (term, category, subtype, confidence)
# Matching: substring in canonical_name_he (lowercased).

HARD_ANCHORS: list[tuple[str, str, str | None, float]] = [
    # ── Savory spreads — Israeli hummus and savory dip category ─────────────
    # These must be declared before "טחינה" (whole_food_fat, 0.93) and before
    # the "מוס"/"מעדן" dessert signals can interfere via Stage 2 scoring.
    # "חומוס" at 0.94 beats "טחינה" (0.93) for hummus-with-tahini products.
    # "מטבוחה"/"מסבחה"/"חציל" anchors short-circuit Stage 2 entirely,
    # preventing absent signals from defaulting to "default" category.
    ("חומוס",           "sauce_spread",  "hummus",           0.94),
    ("מסבחה",           "sauce_spread",  "masabcha",         0.92),
    ("מטבוחה",          "sauce_spread",  "matbucha",         0.92),
    ("ממרח פלפלים",    "sauce_spread",  "pepper_spread",    0.92),
    ("פלפל צ'ומה",     "sauce_spread",  "pepper_chuma",     0.91),
    ("חצילים",          "sauce_spread",  "eggplant_spread",  0.91),
    ("חציל",            "sauce_spread",  "eggplant_spread",  0.91),
    # ── Bakery — most specific first (crispbread before "לחם") ───────────────
    ("לחמי קריספ",     "crispbread",        "crispbread",     0.94),
    ("קנקבד",          "crispbread",        "knackebrod",     0.95),
    ("קריספ-ברד",      "crispbread",        "crispbread",     0.93),
    ("קרקר",           "cracker",           "cracker",        0.93),
    ("פריכיות",        "cracker",           "puffed_cracker", 0.88),
    # ── Coffee biscuits / plain sweet biscuits (EV-058 / TASK-275) ───────────────
    # Dedicated biscuit routing for dry, plain, sweet biscuits consumed as coffee
    # accompaniments. Purpose: taxonomy + explainability only. Caps INTACT.
    ("ביסקוויט בלגי",   "biscuit",  "speculoos",         0.94),
    ("ביסקוויט תה",     "biscuit",  "tea_biscuit",       0.93),
    ("מרי ביסקוויט",    "biscuit",  "marie_biscuit",     0.92),
    ("ביסקוויט מרי",    "biscuit",  "marie_biscuit",     0.92),
    ("עוגיות חמאה",     "biscuit",  "butter_cookie",     0.92),
    ("פטי-בר",          "biscuit",  "petit_beurre",      0.93),
    ("פטי בר",          "biscuit",  "petit_beurre",      0.93),
    ("פתי-בר",          "biscuit",  "petit_beurre",      0.93),
    ("פתי בר",          "biscuit",  "petit_beurre",      0.93),
    ("פתיבר",           "biscuit",  "petit_beurre",      0.93),
    ("פטיבר",           "biscuit",  "petit_beurre",      0.93),
    ("ביסקוויט",        "biscuit",  "plain_biscuit",     0.88),
    ("לוטוס",           "biscuit",  "speculoos",         0.92),
    ("דייג'סטיב",       "biscuit",  "digestive",         0.92),
    ("ביסקוטי",         "biscuit",  "biscotti",          0.91),
    ("שורטברד",         "biscuit",  "shortbread",        0.90),
    # EV-058 / P89 (2026-06-13): named-עוגיות OAT biscuits ("שיבולת שועל" in name) route
    # to biscuit even when "דגנים" is also present. The specific combination עוגיות +
    # שיבולת שועל is an oat coffee biscuit (§1.4 whole-grain IN), not a granola/cereal.
    # This anchor fires BEFORE the bare "עוגיות" anchor and beats its "דגנים" exclusion.
    # Confidence 0.86 > bare עוגיות (0.85) + longer term wins on tie.
    # Exclusions: must not fire when product is a granola bar, cereal, snack, or in a
    # filling/coating context (same exclusion philosophy as bare "עוגיות" + cereal terms).
    ("עוגיות שיבולת שועל", "biscuit", "oat_cookie",     0.86),
    ("עוגיות",          "biscuit",  "plain_cookie",      0.85),
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
    # ── Protein bars / cookies / bites (TASK-365) ────────────────────────────
    # Anchors on explicit protein identity in the product NAME only —
    # ingredient text is NOT consulted (avoids false positives on granola bars
    # that happen to contain whey as a minor ingredient).
    # Inserted BEFORE generic "גרנולה" (0.90) so they win on specificity.
    # Multi-word anchors first (longer/more-specific wins on ties).
    ("חטיף חלבון",      "snack_bar_granola", "protein_bar",    0.93),
    ("חטיף פרוטאין",    "snack_bar_granola", "protein_bar",    0.93),
    ("בר חלבון",        "snack_bar_granola", "protein_bar",    0.93),
    ("עוגיות חלבון",    "snack_bar_granola", "protein_bar",    0.92),
    ("עוגיית חלבון",    "snack_bar_granola", "protein_bar",    0.92),
    ("ביס חלבון",       "snack_bar_granola", "protein_bar",    0.91),
    ("כדורי חלבון",     "snack_bar_granola", "protein_bar",    0.91),
    ("פרוטאין בר",      "snack_bar_granola", "protein_bar",    0.93),
    ("protein bar",     "snack_bar_granola", "protein_bar",    0.92),
    # Stand-alone פרוטאין / חלבון tokens in name (covers brand+protein patterns
    # like "אול אין פרוטאין", "גרנולה פרוטאין+אגוזים", "חט.חלבון" abbreviations).
    # Confidence 0.91 — above גרנולה (0.90) so protein identity overrides granola routing.
    # Exclusions prevent firing on dairy/beverage/spread contexts.
    ("פרוטאין",         "snack_bar_granola", "protein_bar",    0.91),
    ("חלבון",           "snack_bar_granola", "protein_bar",    0.91),
    # ── Snack bars ────────────────────────────────────────────────────────────
    ("מוסלי",          "snack_bar_granola", "muesli",         0.88),
    ("גרנולה",         "snack_bar_granola", "granola",        0.90),
    # ── Dairy ─────────────────────────────────────────────────────────────────
    # Hard & semi-hard cheese anchors — product names use "גאודה" or omit "גבינה" entirely.
    # Without these anchors, Gouda SKUs route to default (conf=0.30) because the Hebrew
    # absolute-form "גבינה" doesn't match the name-only signal when the product name uses
    # only the variety name ("גאודה", "אמנטל", "גרנה פדנו", "ברי").
    ("גאודה",           "dairy_protein",     "hard_cheese",    0.88),
    ("אמנטל",          "dairy_protein",     "hard_cheese",    0.88),
    ("גרנה פדנו",       "dairy_protein",     "hard_cheese",    0.88),
    ("ברי",             "dairy_protein",     "soft_ripened",   0.87),
    ("קוטג'",          "dairy_protein",     "cottage",        0.93),
    # Cream-cheese / spread pool (TASK-145 — fixes run_cheese_001 QA-CHS-001). These lack
    # dairy signal strength (high fat, low protein, flavored) and fell to default/whole_food_fat.
    # Specific multi-word/brand anchors only — bare "שמנת" deliberately excluded (sour/sweet/
    # whipping cream are not cheese). "נפוליאון" carries a cake exclusion below.
    ("גבינת שמנת",     "dairy_protein",     "cream_cheese",   0.93),
    ("ממרח גבינה",     "dairy_protein",     "cheese_spread",  0.92),
    ("פילדלפיה",       "dairy_protein",     "cream_cheese",   0.92),
    ("נפוליאון",       "dairy_protein",     "cream_cheese",   0.90),
    ("יוגורט",         "dairy_protein",     "yogurt",         0.92),
    ("קפיר",           "dairy_protein",     "kefir",          0.93),
    # Yogurt sub-brands / product lines (TASK-139C) — genuine yogurts whose names
    # lead with a brand/line token, not "יוגורט" (protein, mix-in, Froop, bio, Greek).
    # Confidence is ABOVE the competing topping/dessert anchors — "קורנפלקס" (cereal
    # 0.93) and "יופלה" (dessert 0.91) — so dairy identity wins over an incidental
    # topping or sub-brand descriptor.
    ("יופלה go", "dairy_protein", "protein_yogurt", 0.94),
    ("מולר מיקס", "dairy_protein", "yogurt_mixin", 0.94),
    ("מולר פרוטאין", "dairy_protein", "protein_yogurt", 0.93),
    ("מולר פרופ", "dairy_protein", "froop_yogurt", 0.93),
    ("דנונה פרו", "dairy_protein", "protein_yogurt", 0.93),
    ("דנונ.פרו", "dairy_protein", "protein_yogurt", 0.93),
    ("דנונה ביו", "dairy_protein", "bio_yogurt", 0.93),
    ("דנונה יווני", "dairy_protein", "greek_yogurt", 0.93),
    # TASK-515/515A — 3 more yogurt brand-line anchors. These MUST be Stage-1
    # HARD_ANCHORS (not BARCODE_ROUTING_OVERRIDES/Stage-5) because each of their
    # 3 known products has a COMPETING Stage-1 anchor already firing first
    # (classify_category() returns immediately on a Stage-1 anchor match, before
    # Stage 5 is ever reached) — a barcode override for these 3 was tried first
    # and empirically verified to have NO effect (Stage-5 unreachable), which is
    # why these are here instead. Confidence set above the anchor each one must
    # beat, per the same "higher confidence wins" _check_anchors() rule used by
    # every entry above:
    #   - "יופלה שטוזים" (0.95) beats bare "יופלה" (dessert, 0.91) — Stouzy is a
    #     drinkable-yogurt sub-line (68% יוגורט per ingredient text), not the
    #     base Yoplait dessert line.
    #   - "אקטיביה" (0.94) beats "שיבולת שועל" (cereal/oatmeal, 0.88) — Activia's
    #     oat-mixin SKU was routing to cereal. Deliberately NOT given a
    #     "משקה"/"שתייה" exclusion (unlike the sub-brand anchors above) — TASK-515
    #     confirmed drinkable Activia (משקה אקטיביה) is genuine cultured yogurt
    #     and must ALSO route dairy_protein, not beverage.
    #   - "מולר אקטיב" (0.94) beats bare "חלבון" (snack_bar_granola/protein_bar,
    #     0.91) — Muller Activ's high-protein SKU was routing to protein_bar.
    # All 3 confirmed genuinely cultured, milk-based yogurt by ingredient-text
    # read (see BARCODE_ROUTING_OVERRIDES comment block below for the full
    # TASK-515 disposition table). Zero-cross-category-impact proof: 213
    # products across 4 other live categories (milk_and_alternatives,
    # hard_cheeses, snack_bars, juices) re-classified before/after this edit —
    # 0 diffs (see run_yogurt_task515_v2_tripwire_proof.json).
    ("יופלה שטוזים", "dairy_protein", "yogurt", 0.95),
    ("אקטיביה", "dairy_protein", "bio_yogurt", 0.94),
    ("מולר אקטיב", "dairy_protein", "protein_yogurt", 0.94),
    # ── Brined cheeses (TASK-267 / EV-055) ───────────────────────────────────
    # Brined-cheese products whose names do NOT contain "גבינה"/"גבינת" (already
    # anchored above) use type-specific terms: פטה (feta), בולגרית (Bulgarian),
    # חלומי (halloumi). These are endemic dairy products — routing them to default
    # or cracker is a category-detection bug (see graduated_sodium_d7_design_v1.md
    # Decision 4 + graduated_sodium_d7_cosign_v1.md). Anchors scoped by exclusions.
    # Confidence 0.88 beats Stage 2 cracker/default signals (מלוח, פריך at 0.50).
    # These anchors are SCOPED TO BRINED DAIRY PRODUCTS ONLY — not other contexts.
    ("פטה",            "dairy_protein",     "feta_brined",    0.88),
    ("בולגרית",        "dairy_protein",     "bulgarian_brined", 0.88),
    ("חלומי",          "dairy_protein",     "halloumi_brined", 0.88),
    # ── Whole-food fats ───────────────────────────────────────────────────────
    # TASK-191 — butter anchor. "חמאה" leads the product name for all pure dairy
    # butter SKUs. Confidence 0.92 beats Stage 2 cracker/default signals that fire
    # on "מלוחה" (salted) when no ingredient list is present. Must appear AFTER
    # nut-butter anchors (חמאת בוטנים etc.) so those remain more specific.
    # Exclusions: nut-butter phrases and "ממרח" spreads (handled below).
    ("חמאה",           "whole_food_fat",    "dairy_butter",   0.92),
    ("טחינה",          "whole_food_fat",    "tahini",         0.93),
    # ── Dairy desserts (מעדנים) ─────────────────────────────────────────────────
    ("מילקי",          "dessert",           "milky_style",    0.96),
    ("מעדן חלבון",     "dessert",           "protein_dessert",0.95),
    ("מעדן ילדים",     "dessert",           "kids_dessert",   0.95),
    ("מעדן",           "dessert",           "dairy_dessert",  0.90),
    ("עדנה",           "dessert",           "dairy_dessert",  0.93),
    ("פרוביו",         "dessert",           "probiotic_dessert", 0.92),
    ("יופלה",          "dessert",           "flavored_yogurt_dessert", 0.91),
    # ── Frozen vegetables ──────────────────────────────────────────────────────
    # Anchors fire on explicit frozen indicators in product names. Exclusions
    # (ANCHOR_EXCLUSIONS) block non-veg frozen products (bread, pizza, fish, meat,
    # chicken, patties, schnitzel, pastries, sauces, etc.).
    ("קפוא",           "frozen_vegetable",  None,  0.90),
    ("מוקפא",          "frozen_vegetable",  None,  0.90),
]

# Anchors that require the matched term to appear at the START of the product name
# (i.e., it IS the product, not a flavor descriptor like "בטעם שיבולת שועל").
ANCHOR_REQUIRES_POSITION_CHECK: set[str] = {
    "שיבולת שועל",   # "לחם שיבולת שועל" = bread, not oatmeal
}

# For dairy anchors: suppress if the term appears AFTER a flavor descriptor
# in the product name ("בטעם יוגורט" = yogurt-flavored, not a yogurt product).
DAIRY_ANCHOR_TERMS: set[str] = {"יוגורט", "קפיר", "קוטג'", "גבינה", "גבינת", "גאודה", "לבן"}
DAIRY_FLAVOR_SUPPRESSORS: list[str] = ["בטעם", "טעם", "בניחוח"]

# TASK-139C — Dairy-head topping suppression.
# A yogurt that carries a cereal/nut/granola TOPPING ("יוגורט קראנצ קורנפלקס") must
# anchor to dairy, not to the topping's category. When the name LEADS with a dairy-head
# term (the product IS a yogurt), competing topping-category anchors are skipped so the
# dairy anchor wins. Gated to name-start to avoid catching topping-flavoured products
# (e.g. "גרנולה בטעם יוגורט") where the dairy word is a descriptor, not the product.
DAIRY_HEAD_TERMS: tuple[str, ...] = ("יוגורט", "קפיר")
TOPPING_ANCHOR_CATS: set[str] = {"cereal", "snack_bar_granola", "whole_food_fat"}

# If name contains these exclusion terms, the specified anchor should not fire.
ANCHOR_EXCLUSIONS: dict[str, list[str]] = {
    # "שיבולת שועל" must not fire for oat drinks (beverage) or snack bars using oats as ingredient
    "שיבולת שועל":    ["לחם", "עוגיות", "מאפה", "ביסקוויט", "פריכיות",
                       "משקה", "שתייה", "חטיפי", "חטיף", "ברים"],
    # TASK-191 — "חמאה" dairy butter anchor exclusions.
    # Must not fire on: nut butter products ("חמאת X"), butter-flavored snacks, or
    # spreads with "ממרח". The nut-butter multi-word anchors already outcompete this
    # anchor via specificity (longer match), but we also add the exclusion as a guard.
    "חמאה":           ["חמאת", "ממרח", "בטעם חמאה", "שמן קוקוס",
                       "שמן דקל", "מרגרינה", "פלמנטין", "שומן אפייה"],
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
    # Biscuit anchors (EV-058 / TASK-275) — must not fire when biscuit is filling/modifier
    "ביסקוויט":     ["מילוי", "שכבת", "ציפוי", "קרם", "טחינה", "מצופה",
                      "גבינה", "שוקולד ביסקוויט"],
    "לוטוס":        ["מילוי", "ציפוי", "שכבת", "רוטב", "קרם", "מצופה",
                      "גלידה"],
    "ביסקוויט בלגי": [],
    "ביסקוויט תה":   [],
    "מרי ביסקוויט":  [],
    "ביסקוויט מרי":  [],
    "דייג'סטיב":     ["חטיף", "ציפוי"],
    "ביסקוטי":       ["גלידה", "מילוי"],
    "שורטברד":       ["גלידה", "מילוי"],
    "עוגיות חמאה":   ["ממולא", "שוקולד", "ציפוי", "מצופה", "חטיף",
                      "גרנולה", "דגנים"],
    "פטי-בר":        [],
    "פטי בר":        [],
    "פתי-בר":        [],
    "פתי בר":        [],
    "פתיבר":         [],
    "פטיבר":         [],
    # EV-058 / P89 oat-cookie anchor — must not fire on granola/cereal/snack/filling context
    # even when "שיבולת שועל" is present (e.g., a granola bar with oat in name).
    "עוגיות שיבולת שועל": ["גרנולה", "מוזלי", "מוסלי", "חטיף", "ברים",
                            "ממרח", "וופל", "קרקר", "פריכיות", "ציפוי",
                            "מילוי", "קרם", "שכבת", "אנרגיה", "חלבון"],
    "עוגיות":        ["אורז", "גרנולה", "דגנים", "מוזלי", "מוסלי", "חטיף",
                      "ברים", "ממרח", "וופל", "קרקר", "פריכיות", "ציפוי",
                      "מילוי", "קרם", "שכבת", "אנרגיה", "חלבון"],
    # TASK-365 — Protein bar / cookie / bite anchor exclusions
    "חטיף חלבון":   [],
    "חטיף פרוטאין": [],
    "בר חלבון":     [],
    "עוגיות חלבון": [],
    "עוגיית חלבון": [],
    "ביס חלבון":    [],
    "כדורי חלבון":  [],
    "פרוטאין בר":   [],
    "protein bar":   [],
    # Stand-alone פרוטאין/חלבון: exclude dairy/beverage/dessert contexts.
    # "מעדן חלבון" = dairy dessert; "משקה פרוטאין" = beverage; "קוטג' פרוטאין" = dairy.
    # NOTE: "חלב" is intentionally EXCLUDED from the exclusion list here — it is a
    # substring of "חלבון" itself, so checking `"חלב" in name` fires on any product
    # whose name contains "חלבון" (e.g., "חט.חלבון", "אין‌חלבון").  The dairy
    # context is adequately covered by יוגורט/גבינה/קוטג'/מעדן/שתייה/אבקת/ממרח.
    "פרוטאין":     ["משקה", "שתייה", "מעדן", "קוטג'", "יוגורט", "גבינה", "שייק",
                    "אבקת"],
    "חלבון":       ["משקה", "שתייה", "מעדן", "קוטג'", "יוגורט", "גבינה", "שייק",
                    "אבקת", "ממרח"],
    # Savory spread anchors — tahini exclusions
    "טחינה":          ["חציל", "חצילים"],            # "חציל על האש בטחינה" = eggplant spread, not tahini product
    # Brined-cheese anchors (TASK-267 / EV-055) — must not fire in snack/cracker/flavor context
    "פטה":            ["חטיף", "מילוי", "בטעם", "קרקר", "ממרח"],
    "בולגרית":        ["חטיף", "מילוי", "בטעם", "קרקר", "ממרח"],
    "חלומי":          ["חטיף", "מילוי", "בטעם", "קרקר", "ממרח"],
    # Cream-cheese anchors (TASK-145) — must not fire on the napoleon CAKE / pastry (עוגת פס נפוליאון)
    "נפוליאון":       ["עוגה", "עוגת", "פס", "מאפה", "בצק"],
    # Hard cheese anchors — must not fire in snack/filling/flavouring context
    "גאודה":          ["חטיף", "מילוי", "בטעם", "שמן", "רוטב"],
    "אמנטל":         ["חטיף", "מילוי", "בטעם"],
    "גרנה פדנו":      ["חטיף", "מילוי", "רוטב"],
    "ברי":            ["חטיף", "מילוי", "עוגת", "בטעם"],
    # פילדלפיה anchor (TASK-153 / EV-030) — must not fire on a SEASONING blend
    # (תערובת תיבול פילדלפיה, brand טעם וריח, Shufersal seasonings shelf, sodium 7,905 mg/100g).
    # The seasoning phrase "תערובת תיבול" is exclusive to spice blends; real herbed פילדלפיה
    # cheeses say "פילדלפיה שום+ע.תיבול" (no "תערובת"), so they still route. Mirrors נפוליאון.
    "פילדלפיה":       ["תערובת תיבול"],
    # Dairy dessert anchors — prevent mis-fires
    "מעדן":           ["אבקת", "מיקס", "שייק", "חציל", "חצילים"],  # "מעדן חצילים" = eggplant dish, not dairy dessert
    "עדנה":           ["גבינת", "שמנת", "חמאת"],    # "גבינת עדנה" = soft cheese brand
    "יופלה":          [],
    "פרוביו":         [],
    "מילקי":          [],
    # Frozen vegetable exclusions — must not fire on non-veg frozen products
    "קפוא":           ["לחם", "פיצה", "דג", "דגים", "בשר", "בקר", "עוף",
                       "קציצה", "קציצות", "שניצל", "המבורגר", "קניש", "מאפה",
                       "כריך", "מילוי", "רוטב", "טופו"],
    "מוקפא":          ["לחם", "פיצה", "דג", "עוף", "קציצה", "שניצל",
                       "המבורגר", "קניש", "מאפה", "כריך", "טופו"],
    "מעדן חלבון":     [],
    "מעדן ילדים":     [],
    # Yogurt sub-brand anchors (TASK-139C) must NOT fire for drinkable variants —
    # the yogurt category excludes drinkables ("משקה"); those stay on the beverage gate.
    "יופלה go":       ["משקה", "שתייה", "שתיה"],
    "מולר פרוטאין":   ["משקה", "שתייה", "שתיה"],
    "מולר פרופ":      ["משקה", "שתייה", "שתיה"],
    "מולר מיקס":      ["משקה", "שתייה", "שתיה"],
    "דנונה פרו":      ["משקה", "שתייה", "שתיה"],
    "דנונ.פרו":       ["משקה", "שתייה", "שתיה"],
    "דנונה ביו":      ["משקה", "שתייה", "שתיה"],
    "דנונה יווני":    ["משקה", "שתייה", "שתיה"],
}


def _check_anchors(name: str) -> tuple[str, str | None, float, str] | None:
    """Return (category, subtype, confidence, matched_term) if any anchor fires, else None."""
    best: tuple[str, str | None, float, str] | None = None

    # The product IS a yogurt when its name leads with a dairy-head term.
    name_has_dairy_head = name.startswith(DAIRY_HEAD_TERMS)

    for term, cat, subtype, conf in HARD_ANCHORS:
        if term not in name:
            continue

        # Dairy-head topping suppression: skip cereal/nut/granola TOPPING anchors when
        # the product leads with a dairy head — the topping is a component, not identity.
        if name_has_dairy_head and cat in TOPPING_ANCHOR_CATS:
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
    # ── Israeli savory dip category — backup signals (hard anchors are primary) ─
    ("מטבוחה",       0.92, "name_weighted"),
    ("מסבחה",        0.88, "name_weighted"),
    ("חציל",         0.72, "name_weighted"),
    ("חצילים",       0.72, "name_weighted"),
    ("פלפל צ'ומה",  0.90, "name_weighted"),
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
    # "גבינת" is the Hebrew construct form of "גבינה" ("גבינת עיזים" = goat cheese,
    # "גבינת גאודה" = Gouda cheese). It does not match the absolute-form signal above.
    ("גבינת",        0.85, "name_only"),
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

_BISCUIT: list[tuple[str, float, str]] = []

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
    "biscuit":           _BISCUIT,
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

# ---------------------------------------------------------------------------
# Category prior (TASK-139C) — BSIP0 acquisition-shelf identity
# ---------------------------------------------------------------------------
# Every product in a run was scraped *as* a member of one category shelf
# (yogurt shelf, cereal shelf, …). BSIP1 records that membership as a non-null
# subtype field. We carry that membership forward as a soft CATEGORY PRIOR so a
# real product survives once an incidental grain/nut/topping/flavor token
# dominates its name+ingredients (e.g. "מוזלי בוטנים שקדים" → whole_food_fat,
# "כוסמין מלא" → bread, honey Cheerios → whole_food_fat, flavored "GO" → dessert).
#
# Design contract (frozen-scoring safe — ROUTING ONLY):
#   * The prior is applied ONLY in Stage 2 signal scoring (it adds a boost to the
#     prior category's score). It NEVER overrides a Stage 1 hard anchor — a genuine
#     cross-category anchor (bread/cracker/dessert/sauce/…) still exits first and
#     wins, so a mislabeled item on the shelf is not force-held in the wrong family.
#   * The boost is sized to beat incidental topping/grain/nut SIGNALS, not to beat a
#     legitimate competing identity. It is additive to (not a replacement for) the
#     category's own signals.
#   * The beverage gate still runs after the prior, so a genuinely drinkable variant
#     ("משקה"/"שתייה") still routes to beverage — the dairy↔beverage boundary is
#     unchanged (frozen milk category untouched).
#   * subtype must be NON-NULL and not an explicit "other"/"unknown" bucket; if the
#     field is absent the router behaves exactly as before (fully backward compatible).
#
# Field → routed category. Mirrors the two governed corpora; extend per new category.
CATEGORY_PRIOR_SUBTYPE_FIELDS: dict[str, str] = {
    "bsip_cereal_subtype":          "cereal",
    "bsip_yogurt_subtype":          "dairy_protein",
    "bsip_frozen_vegetable_subtype": "frozen_vegetable",
    # TASK-267 / EV-055 — brined-cheese corpus category prior.
    # bsip_cheese_subpool="brined_cheese" is set for all 48 brined-cheese BSIP1 records.
    # This ensures products that lack a named dairy anchor (פטה/בולגרית/חלומי/גבינה)
    # still route to dairy_protein via the category prior (Stage 2) as a belt-and-suspenders
    # guard. The hard anchors above are the primary fix; this handles any remaining edge cases.
    "bsip_cheese_subpool":          "dairy_protein",
}
# Subtype values that do NOT assert category membership (do not carry a prior).
_CATEGORY_PRIOR_NULL_SUBTYPES: set[str] = {
    "", "other", "unknown", "none", "cereal_other",
}
# Boost added to the prior category in Stage 2. Calibrated against the run_cereals_002
# misroute set: the strongest incidental wrong-category signal stack observed was
# whole_food_fat≈1.88; a 2.0 prior makes the shelf identity decisive while remaining
# beatable only by a much stronger, genuine competing signal mass.
CATEGORY_PRIOR_BOOST: float = 2.0


def _category_prior(product: dict) -> str | None:
    """Return the acquisition-shelf category for this product, or None.

    Reads the BSIP1 subtype field that records which shelf the product was
    scraped from. Returns the mapped routing category when a real subtype is
    present; returns None when no prior is recorded (backward compatible).
    """
    for field, category in CATEGORY_PRIOR_SUBTYPE_FIELDS.items():
        val = product.get(field)
        if not isinstance(val, str):
            continue
        if val.strip().lower() in _CATEGORY_PRIOR_NULL_SUBTYPES:
            continue
        return category
    return None


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
# TASK-365 — Barcode-level routing overrides
# ---------------------------------------------------------------------------
# Some products have names that produce genuine routing ambiguity (no protein
# token, but confirmed protein-bar identity by brand+format).  These overrides
# apply AFTER Stage 3 signal resolution AND after REQ-362 rules, as a last-resort
# hard anchor.  Each entry is documented with the routing failure reason.
#
# Format: barcode → (category, category_subtype, confidence, reason)
#
BARCODE_ROUTING_OVERRIDES: dict[str, tuple[str, str, float, str]] = {
    # pb-024 — "אול אין קרם עוגיות" (barcode 7290018703304)
    # Routing failure: "קרם" fires _DESSERT (0.45); "עוגיות" anchor suppressed (קרם
    # in exclusion list); no חלבון/פרוטאין in name → routes to "dessert".
    # This is confirmed: a protein-cookie format on the פרוטאין bar shelf, brand
    # "אול אין" (All-In, a protein-focused brand).  The product's ingredient list
    # contains ≥20 g protein/100g.  Fix: force snack_bar_granola+protein_bar.
    # TASK-365 red-team fix RD-7.
    "7290018703304": ("snack_bar_granola", "protein_bar", 0.90,
                      "TASK-365 barcode override: cream-cookie format without חלבון in name; "
                      "All-In brand protein product confirmed on protein shelf; "
                      "קרם token caused false dessert routing"),

    # ── TASK-515/515A — yogurt-corpus routing gap fixes ──────────────────────
    # BSIP2 run_yogurt_task515_bsip2 found 20/122 yogurt-shelf products did not
    # route to dairy_protein (mostly Actimel/Activia/Muller-Activ/Danone-drink
    # brand transliterations lacking a "יוגורט"/"קפיר" marker token, so they fell
    # through to default/beverage/dessert/cereal/snack_bar_granola instead), plus
    # 3 already-dairy_protein products with no CULTURED_YOGURT_SUBTYPES subtype.
    # Each entry below was confirmed genuinely cultured, milk-based yogurt by
    # ingredient-text read (pasteurized milk + declared probiotic culture, e.g.
    # BIFIDUS / L.CASEI / Bio) — see run_yogurt_task515_bsip2_v2 disposition
    # table. Barcode-keyed (last-resort, Stage 5) so this can never affect any
    # product/category outside these exact barcodes — zero-blast-radius by
    # construction, unlike a name-substring HARD_ANCHORS entry.
    # NOT fixed (left as-is), by design, per the same run's disposition table:
    #   - 4068028  (ציזיקי לשתיה) — ambiguous cultured-dairy-drink vs. prepared
    #     cucumber salad-drink; no declared starter culture in ingredient text
    #     unlike every fixed entry below. Flagged to Nutrition, not forced.
    #   - 7290119377480 / 7290119385768 (יוגורט פרו / דנונה פרו קראנצ' + chocolate)
    #     — genuine yogurt, but TASK-362's co-signed Rule 3 (chocolate-name-marker
    #     override) deliberately reroutes ANY dairy_protein/dessert/etc. result to
    #     snack_bar_granola/confectionery_chocolate whenever a chocolate marker is
    #     in the name. Overriding that here would require touching Rule 3 itself
    #     (cross-category blast radius) — out of scope for this barcode-only fix.
    #     Flagged to Nutrition/Product for a scoped ruling.
    #   - 7290110329792 / 7290110329815 (מעדן סויה ביו) — soy-based, non-dairy;
    #     already correctly NOT dairy_protein. Discarded from the yogurt corpus.
    "58030": ("dairy_protein", "yogurt", 0.94,
              "TASK-515: יופלה שטוזים משקה תות — ingredient text opens '68% יוגורט "
              "2.2% שומן'; a genuine drinkable cultured yogurt, not a dessert. "
              "'יופלה' anchor (dessert, conf 0.91) fired first; this is the "
              "Stouzy drink sub-line, not the base Yoplait dessert line."),
    "6664693": ("dairy_protein", "yogurt", 0.94,
                "TASK-515: דנונה אפרסק3% שומן — pasteurized milk + BIFIDUS culture; "
                "plain Danone yogurt cup with no 'יוגורט' token in name → fell to default."),
    "7290102031276": ("dairy_protein", "bio_yogurt", 0.94,
                       "TASK-515: אקטימל תות בננה מארז — Actimel; milk + cream + "
                       "declared probiotic culture; brand token not previously anchored."),
    "7290105364678": ("dairy_protein", "bio_yogurt", 0.94,
                       "TASK-515: משקה אקטיביה אפרסק — Activia; milk + Bifidus "
                       "Actiregularis culture; fell to beverage on 'משקה' token."),
    "7290105965738": ("dairy_protein", "yogurt", 0.94,
                       "TASK-515: דנונה לשתיה תות בננה — milk + BIFIDUS culture; "
                       "plain Danone drinking yogurt, no brand-line anchor existed."),
    "7290107937542": ("dairy_protein", "bio_yogurt", 0.94,
                       "TASK-515: משקה אקטיביה תות 1.2% — Activia; same as 7290105364678."),
    "7290107938396": ("dairy_protein", "bio_yogurt", 0.94,
                       "TASK-515: מארז אקטימל תות — Actimel; same as 7290102031276."),
    "7290107958035": ("dairy_protein", "yogurt", 0.94,
                       "TASK-515: דנונה במתיקות מעודנת — milk + BIFIDUS culture; "
                       "plain reduced-sweetness Danone yogurt, no brand-line anchor."),
    "7290110552244": ("dairy_protein", "protein_yogurt", 0.94,
                       "TASK-515: משקה דנונה פרו20 ללת\"ס — milk + whey protein + "
                       "declared yogurt culture; existing 'דנונה פרו' anchor (0.93) is "
                       "excluded when name contains 'משקה' (drinkable Danone-Pro was "
                       "deliberately out of scope pre-515); this barcode override does "
                       "NOT touch that anchor/exclusion, so the spoonable דנונה פרו line "
                       "is unaffected. NOTE: BSIP1 subpool field for this barcode was "
                       "corrected spoonable->drinkable to match its actual physical form "
                       "(name says משקה); see bsip1_yogurt_7290110552244.json."),
    "7290110561352": ("dairy_protein", "yogurt", 0.94,
                       "TASK-515: דנונה דל לקטוז 200 גרם — milk + BIFIDUS culture; "
                       "plain lactose-free Danone yogurt, no brand-line anchor."),
    "7290110573713": ("dairy_protein", "yogurt_mixin", 0.94,
                       "TASK-515: דנונה מולטי צ'יה — milk + chia + BIFIDUS culture; "
                       "yogurt+mix-in compound product, same pattern as the existing "
                       "'מולר מיקס' anchor (yogurt_mixin); fell to snack_bar_granola."),
    "7290112341686": ("dairy_protein", "bio_yogurt", 0.94,
                       "TASK-515: אקטיביה 3% מארז — Activia plain; brand token not "
                       "previously anchored (ingredient text not parsed, but Activia "
                       "is an unambiguous cultured-yogurt brand identity)."),
    "7290112346797": ("dairy_protein", "bio_yogurt", 0.94,
                       "TASK-515: אקטיביה שיבולת שועל שזיף — milk + oats + confirmed "
                       "Bifidus Actiregularis culture; Activia+oat mix-in, fell to "
                       "cereal/oatmeal (0.88) — no Activia brand anchor existed."),
    "7290114311069": ("dairy_protein", "protein_yogurt", 0.94,
                       "TASK-515: מולר אקטיב לבן0% 25חלבון — milk + Bio culture; "
                       "Muller Activ high-protein yogurt; bare 'חלבון' anchor (0.91, "
                       "snack_bar_granola/protein_bar) outscored dairy identity — no "
                       "'מולר אקטיב' brand anchor existed (only מולר פרוטאין/פרופ/מיקס do)."),
    "7290115676051": ("dairy_protein", "bio_yogurt", 0.94,
                       "TASK-515: משקה אקטיביה עם ש.שועל — Activia+oats drink; milk + "
                       "Bifidus Actiregularis culture; fell to beverage on 'משקה' token."),
    # Already dairy_protein, subtype-only fix (CULTURED_YOGURT_SUBTYPES membership
    # for the R7 fermentation-bonus gate; category itself was already correct).
    "6664655": ("dairy_protein", "bio_yogurt", 0.94,
                "TASK-515: אקטימל לבן מארז — Actimel plain; milk + L.CASEI DN114-001 "
                "culture; router already said dairy_protein but subtype was None."),
    "7290119380923": ("dairy_protein", "bio_yogurt", 0.94,
                       "TASK-515: אקטימל לבן מארז (dup SKU) — same as 6664655."),
    "7290114310536": ("dairy_protein", "protein_yogurt", 0.94,
                       "TASK-515: מולר אקטיב לייט וניל — milk + Bio culture; router "
                       "already said dairy_protein but subtype was None."),
}


# ---------------------------------------------------------------------------
# REQ-362-R1 — Post-classification routing overrides (TASK-362, co-signed)
# ---------------------------------------------------------------------------
# These three rules correct misrouting WITHOUT touching dimension scoring, caps,
# or floors.  They are applied as a Stage 4 pass after Stage 3 resolution.
# Any override is recorded in classification_basis and req362_override_trace.

# Rule 1 — Protein-marker name tokens that force cracker→snack_bar_granola.
# Must match canonical_name_he (lowercased).  Ingredient text is NOT consulted.
_R1_PROTEIN_NAME_MARKERS: frozenset[str] = frozenset({"חלבון", "פרוטאין", "protein"})

# Rule 2 — Threshold for engineered-bar override (whole_food_fat→snack_bar_granola).
_R2_PROTEIN_THRESHOLD_G: float = 20.0    # per-100g
_R2_INGREDIENT_COUNT_MIN: int  = 15

# Rule 3 — Chocolate lens correction (TASK-362, Nutrition Agent co-sign).
# The whole_food_fat lens is built for tahini, nut butters, and olive oil — products
# where high calorie density and high fat are structural virtues (oleic acid, whole
# seed matrix).  Chocolate fat is cocoa butter: predominantly saturated (stearic +
# palmitic ≈ 60% of total fat), not equivalent to nut-butter fat in scoring context.
# Routing chocolate to whole_food_fat gives confectionery a free pass on its defining
# problem (high sat fat + high energy density + high sugar in milk/white varieties)
# and produces a 21-point coherence gap between identical product types (prot-014
# class failure at category scale).
#
# Rule: if engine_category is in _R3_WRONG_CATS AND product name (canonical_name_he)
# contains a chocolate name marker → route to snack_bar_granola, subtype confectionery.
# Name-only: ingredient text is NOT consulted (avoids false-positives on products that
# merely contain chocolate as an ingredient and correctly sit in another category).
# Exclusions: spreads/drinks that survived the scope filter in score_chocolate_task362.py
# are already excluded upstream; no additional exclusions needed here.
_R3_CHOCOLATE_NAME_MARKERS: frozenset[str] = frozenset({
    "שוקולד",         # the primary identity token — present in virtually all Hebrew chocolate names
    "שוק.",           # truncated "שוקולד" used in some Lindt Hebrew SKU names (e.g. "שוק.לינדט")
    "טובלרון",        # Toblerone — brand name without "שוקולד" in several variants
    "מילקה",          # Milka brand name in Hebrew; some SKUs lack "שוקולד" explicitly
    "קיט קט",         # Kit Kat
    "סניקרס",         # Snickers
    "טוויקס",         # Twix
    "באונטי",         # Bounty
    "טורינו",         # Torino — Israeli Elit chocolate brand (tablets + bars, milk and dark)
    "קליק",           # Klik — Israeli Elit chocolate confection brand (קליק אין, קליק ביסקוויט, etc.)
    "לינדט אקסלנס",   # Lindt Excellence line — SKUs named "לינדט אקסלנס X" without "שוקולד"
    "פינוקיות פסק זמן", # Paket Zman pinukhiyot — chocolate-coated confection
})
# These are the wrong-engine categories that Rule 3 corrects.
# whole_food_fat: the primary offender (16 tablets got B/E free-pass on the fat lens).
# dairy_protein, dessert, biscuit, sauce_spread, default, cracker, cereal: other wrong paths.
# snack_bar_granola is intentionally excluded — that is the correct destination.
_R3_WRONG_CATS: frozenset[str] = frozenset({
    "whole_food_fat", "dairy_protein", "dessert", "biscuit",
    "sauce_spread", "default", "cracker", "cereal",
})


def _apply_req362_overrides(result: dict, product: dict) -> dict:
    """REQ-362-R1/R3: apply post-classification routing corrections.

    Rule 1 — Protein-marker overrides cracker:
        If engine_category == cracker AND product name (canonical_name_he) contains
        a protein marker (חלבון | פרוטאין | protein) → route to snack_bar_granola.
        Rationale: salty-name token "מלוח" in a protein-bar name should not anchor
        the product as a cracker; the explicit protein declaration wins.

    Rule 2 — Engineered-bar overrides whole_food_fat:
        If engine_category == whole_food_fat AND protein_g ≥ 20 (per-100g) AND
        ingredient_count ≥ 15 → route to snack_bar_granola.
        The whole_food_fat lens is for tahini/nut-butter products; a multi-ingredient
        protein bar with ≥20 g protein/100g is not a whole-food-fat product.
        ingredient_count is emitted into the trace for QA verification.

    Rule 3 — Chocolate lens correction (TASK-362):
        If engine_category is in _R3_WRONG_CATS AND product name contains a
        chocolate identity marker (_R3_CHOCOLATE_NAME_MARKERS) → route to
        snack_bar_granola, subtype confectionery_chocolate.
        Rationale: whole_food_fat treats chocolate's cocoa-butter fat as a whole-food
        virtue (same as tahini/nut-butter) — incorrect.  Cocoa butter is ~60% sat fat;
        chocolate confectionery is NOT a whole-food fat product.  This produced a 21-pt
        coherence gap between identical product types (prot-014 class failure at scale).
        dairy_protein/dessert/biscuit/sauce_spread/default are also wrong paths;
        snack_bar_granola is the single correct lens for all chocolate confectionery.
        Name-only check: ingredient text is NOT consulted (avoids false-positives on
        products that contain chocolate as a coating/filling in another category).

    Note: the original "Rule 3" (negation-aware sweetener detection "ללא ממתיקים")
    is implemented upstream in signal_extractor.py and is unchanged.

    Returns a (possibly mutated) copy of result with req362_override_trace added.
    """
    name     = (product.get("canonical_name_he") or "").lower()
    ing_text = (product.get("ingredients_text_he") or "").lower()  # TASK-394: needed for R3 confectionery-ingredient check
    nn   = product.get("normalized_nutrition_per_100g") or {}
    protein_g      = nn.get("protein_g")
    ingredient_count = product.get("_req362_ingredient_count")  # injected by caller

    current_cat = result.get("category")
    override_applied = None
    override_reason  = None

    # --- Rule 1 ---
    if current_cat == "cracker":
        protein_marker_hit = next(
            (m for m in _R1_PROTEIN_NAME_MARKERS if m in name), None
        )
        if protein_marker_hit:
            result["category"]              = "snack_bar_granola"
            result["category_subtype"]      = "protein_bar"
            result["anchor_override"]       = True
            result["category_confidence"]   = 0.85
            result["confidence_band"]       = "high"
            result["category_instability_flag"] = False
            result["routing_instability_warning"] = None
            result["classification_basis"]  = [
                f"req362_r1:protein_name_marker({protein_marker_hit})",
                f"cracker_overridden:protein_marker_beats_savory_signal",
            ] + result.get("classification_basis", [])[:3]
            override_applied = "rule1_protein_marker"
            override_reason  = (
                f"cracker→snack_bar_granola: protein marker '{protein_marker_hit}' "
                f"in name overrides cracker:מלוח routing"
            )

    # --- Rule 2 ---
    elif current_cat == "whole_food_fat":
        prot_ok  = (protein_g is not None and protein_g >= _R2_PROTEIN_THRESHOLD_G)
        count_ok = (ingredient_count is not None and ingredient_count >= _R2_INGREDIENT_COUNT_MIN)
        if prot_ok and count_ok:
            result["category"]              = "snack_bar_granola"
            result["category_subtype"]      = "protein_bar"
            result["anchor_override"]       = True
            result["category_confidence"]   = 0.82
            result["confidence_band"]       = "high"
            result["category_instability_flag"] = False
            result["routing_instability_warning"] = None
            result["classification_basis"]  = [
                f"req362_r2:engineered_bar(protein_g={protein_g},ingredient_count={ingredient_count})",
                f"whole_food_fat_overridden:high_protein_multiingredient_bar",
            ] + result.get("classification_basis", [])[:3]
            override_applied = "rule2_engineered_bar"
            override_reason  = (
                f"whole_food_fat→snack_bar_granola: protein_g={protein_g} ≥ "
                f"{_R2_PROTEIN_THRESHOLD_G} AND ingredient_count={ingredient_count} "
                f"≥ {_R2_INGREDIENT_COUNT_MIN}"
            )
        # else: threshold not met; emit diagnostic for QA
        elif prot_ok and not count_ok:
            override_reason = (
                f"rule2_not_fired: protein_g={protein_g} qualifies but "
                f"ingredient_count={ingredient_count} < {_R2_INGREDIENT_COUNT_MIN}"
            )

    # --- Rule 3 — Chocolate lens correction (TASK-362) ---
    # Applied to ANY wrong-engine result, including those already processed above
    # (Rule 2 may have moved a WFF chocolate to snack_bar_granola correctly; those
    # are a subset; Rule 3 catches the rest). Re-read current_cat after Rule 1/2.
    current_cat_after = result.get("category")
    if current_cat_after in _R3_WRONG_CATS:
        choc_marker_hit = next(
            (m for m in _R3_CHOCOLATE_NAME_MARKERS if m in name), None
        )
        if choc_marker_hit:
            # TASK-394: BARI_R3_BISCUIT_NARROW_V1 guard (default OFF).
            # When ON: R3 yields for a product that is BOTH:
            #   (a) strongly anchored as biscuit (anchor_override=True, cat=biscuit,
            #       conf >= _R3_BISCUIT_ANCHOR_CONF_MIN), AND
            #   (b) has NO positive chocolate-confectionery signal in ingredients
            #       (i.e., the chocolate is only a flavor descriptor, not a coating
            #       or leading ingredient).
            # Both conditions must hold simultaneously; if either fails, R3 fires.
            # Product identity: `ing_text` is the lowercased ingredients_text_he
            # resolved at the top of _apply_req362_overrides (product.get call above).
            _r3_yielded = False
            if BARI_R3_BISCUIT_NARROW_V1 and current_cat_after == "biscuit":
                _anchor_ok  = (
                    result.get("anchor_override") is True
                    and result.get("category_confidence", 0.0) >= _R3_BISCUIT_ANCHOR_CONF_MIN
                )
                _choc_conf_ing = any(sig in ing_text for sig in _R3_CHOC_CONFECTIONERY_ING_SIGNALS)
                if _anchor_ok and not _choc_conf_ing:
                    # R3 yields: flavor-descriptor biscuit with strong biscuit anchor
                    # and no confectionery-ingredient signal stays in biscuit.
                    _r3_yielded = True
                    override_reason = (
                        f"r3_yielded(BARI_R3_BISCUIT_NARROW_V1=on): biscuit hard_anchor "
                        f"conf={result.get('category_confidence'):.2f}>={_R3_BISCUIT_ANCHOR_CONF_MIN} "
                        f"AND no confectionery_ing_signal — '{choc_marker_hit}' is flavor "
                        f"descriptor only; product stays biscuit"
                    )
                    result.setdefault("classification_basis", [])
                    result["classification_basis"] = [
                        f"task394_r3_yield:biscuit_anchor_beats_flavor_descriptor({choc_marker_hit})",
                    ] + result.get("classification_basis", [])[:4]

            if not _r3_yielded:
                result["category"]              = "snack_bar_granola"
                result["category_subtype"]      = "confectionery_chocolate"
                result["anchor_override"]       = True
                result["category_confidence"]   = 0.90
                result["confidence_band"]       = "high"
                result["category_instability_flag"] = False
                result["routing_instability_warning"] = None
                result["classification_basis"]  = [
                    f"task362_r3:chocolate_name_marker('{choc_marker_hit}')",
                    f"{current_cat_after}_overridden:chocolate_confectionery_not_whole_food_fat",
                ] + result.get("classification_basis", [])[:3]
                override_applied = "rule3_chocolate_lens"
                override_reason  = (
                    f"{current_cat_after}→snack_bar_granola: chocolate name marker "
                    f"'{choc_marker_hit}' — cocoa-butter fat is not a whole-food-fat virtue; "
                    f"confectionery scores on snack_bar_granola lens (TASK-362 co-signed)"
                )

    result["req362_override_trace"] = {
        "override_applied": override_applied,
        "reason":           override_reason,
        "ingredient_count_used": ingredient_count,
        "protein_g_used":   protein_g,
    }
    return result


# ---------------------------------------------------------------------------
# Public entry point
# ---------------------------------------------------------------------------

def classify_category(product: dict) -> dict:
    """
    Three-stage router. Drop-in replacement for category_classifier.classify_category().
    All v1 output keys are preserved; new router-trace keys are additive.

    Stage 4 (REQ-362-R1): post-classification routing overrides applied after Stage 3.
    See _apply_req362_overrides() for rule descriptions.
    """
    name     = (product.get("canonical_name_he") or "").lower()
    ing_text = (product.get("ingredients_text_he") or "").lower()
    nn       = product.get("normalized_nutrition_per_100g") or {}

    # REQ-362-R1: resolve ingredient_count for Rule 2.  The count is taken from
    # the BSIP1 ingredient list (already sanitized by the signal extractor).
    #
    # TASK-476: this used to duplicate its own "ingredients_list, else naive
    # comma-split of ingredients_text_he" fallback here, independent of
    # input_loader.get_ingredients(). That duplicate fallback did not respect
    # parenthetical sub-groups (e.g. "קמחים 36% (פשתן, שומשום, אפונה, סויה,
    # שקדים)" — one ingredient with a declared sub-group — split into 6 naive
    # fragments instead of 1), which could inflate the count enough to
    # mis-trigger the REQ-362-R2 engineered-bar override on products whose
    # real ingredient count is well under the threshold. Now calls the same
    # get_ingredients() the rest of the pipeline uses (ingredients_list →
    # ingredient_order item texts → ingredients_text_he/ingredients_raw
    # comma-split), so routing sees the identical, highest-fidelity count
    # signal_extractor.py scores on — never a second, lower-fidelity count.
    _ing_list = _get_ingredients(product)
    _ingredient_count = len(_ing_list)
    # Inject for _apply_req362_overrides so it can log the count without re-deriving.
    product["_req362_ingredient_count"] = _ingredient_count

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
        return _apply_req362_overrides(result, product)

    # Stage 1 — hard anchor
    anchor = _check_anchors(name)
    if anchor:
        cat, subtype, conf, term = anchor
        result = _build_anchor_result(cat, subtype, conf, term, name, ing_text, nn, product)
        result["supplement_quarantine"] = supplement_q
        return _apply_req362_overrides(result, product)

    # Stage 2 — signal scoring
    scores, signal_log, suppressed_log = _score_signals(name, ing_text, nn)

    # Stage 2b — beverage gate (preserves v1 logic exactly)
    scores, bev_basis, bev_suppressed = _apply_beverage_gate(scores, name, product)
    signal_log.extend(bev_basis)
    suppressed_log.extend(bev_suppressed)

    # Stage 2c — category prior (TASK-139C). Applied only on the signal path (no hard
    # anchor fired) and after the beverage gate (so drinkable variants stay beverage).
    prior = _category_prior(product)
    if prior is not None and prior in scores:
        scores[prior] += CATEGORY_PRIOR_BOOST
        signal_log.append(f"{prior}:category_prior(+{CATEGORY_PRIOR_BOOST:.2f})")

    # Stage 3 — resolution
    result = _resolve(scores, signal_log, suppressed_log)
    result["supplement_quarantine"] = supplement_q

    # Stage 4 — REQ-362-R1 post-classification routing overrides
    result = _apply_req362_overrides(result, product)

    # Stage 5 — TASK-365 barcode-level hard overrides (last resort)
    barcode = str(product.get("barcode") or "")
    if barcode in BARCODE_ROUTING_OVERRIDES:
        bc_cat, bc_subtype, bc_conf, bc_reason = BARCODE_ROUTING_OVERRIDES[barcode]
        result["category"]              = bc_cat
        result["category_subtype"]      = bc_subtype
        result["category_confidence"]   = bc_conf
        result["confidence_band"]       = "high"
        result["anchor_override"]       = True
        result["category_instability_flag"] = False
        result["routing_instability_warning"] = None
        result["classification_basis"]  = [
            f"task365_barcode_override({barcode}): {bc_reason[:80]}",
        ] + result.get("classification_basis", [])[:3]
        result["task365_barcode_override"] = {
            "barcode": barcode,
            "category": bc_cat,
            "category_subtype": bc_subtype,
            "reason": bc_reason,
        }
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
