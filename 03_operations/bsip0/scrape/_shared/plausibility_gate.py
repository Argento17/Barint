"""
BSIP0 mandatory plausibility gate (moisture-aware) — TASK-362.

WHY THIS EXISTS: the snacks corpus shipped a white-chocolate bar at "99 kcal / 0g
sugar" (physically impossible) to rank #1, because it was scraped single-source
from yochananof with NO plausibility check. This gate is the permanent guard. It
runs on EVERY BSIP0 panel regardless of source, BEFORE a product can be scored.

It is deliberately moisture-aware: a dry snack bar must account for ~>=70 g of
macros per 100 g, but a baked cheesecake is legitimately ~45 g (the rest is water),
so the accounted-mass floor depends on the food class. Do not apply the dry floor
to moist foods — that was a false-positive source in the first cut of this check.

USAGE (per panel, per-100g values):
    from plausibility_gate import check_panel, FoodClass
    verdict = check_panel(nutr_per_100g, food_class=FoodClass.DRY_BAR,
                          ingredients_text="...optional...")
    if not verdict.ok:
        quarantine(product, verdict.reasons)   # never score it

Returns PASS / QUARANTINE with reasons. NEVER fabricates or "fixes" a value —
a failing panel is quarantined and reported, never silently carried forward.
"""
from __future__ import annotations

import re
from dataclasses import dataclass, field
from enum import Enum


class FoodClass(str, Enum):
    DRY_BAR = "dry_bar"            # snack/protein bars, cereal, crackers, cookies
    DRY_DENSE = "dry_dense"        # nuts, dried fruit, powders
    MOIST_BAKED = "moist_baked"    # cakes, fresh bread, pastries (water-heavy)
    SPREAD = "spread"             # hummus, dips, nut butters (water/oil heavy)
    BEVERAGE = "beverage"         # juices, drinks, milk (mostly water)
    DAIRY_SOLID = "dairy_solid"    # hard/brined cheese, yogurt


# accounted_mass = carbs + fat + protein (+ fiber if not already inside carbs).
# Floors are per-100g; below floor => suspicious (likely per-serving mislabel,
# truncated panel, or contamination).
ACCOUNTED_MASS_FLOOR = {
    FoodClass.DRY_BAR: 70.0,
    FoodClass.DRY_DENSE: 80.0,
    FoodClass.MOIST_BAKED: 30.0,
    FoodClass.SPREAD: 18.0,
    FoodClass.BEVERAGE: 2.0,
    FoodClass.DAIRY_SOLID: 20.0,
}

# kcal floor/ceiling per-100g (sanity, not nutrition science).
KCAL_BOUNDS = {
    FoodClass.DRY_BAR: (150, 600),
    FoodClass.DRY_DENSE: (200, 700),
    FoodClass.MOIST_BAKED: (120, 600),
    FoodClass.SPREAD: (40, 750),
    FoodClass.BEVERAGE: (0, 120),
    FoodClass.DAIRY_SOLID: (40, 450),
}

# Ingredient tokens that REQUIRE sugar > 0 in the panel. If present and sugar==0,
# the panel is implausible (the snacks bug signature).
SUGAR_BEARING = [
    "סוכר", "סירופ", "גלוקוז", "פרוקטוז", "דבש", "תמרים", "סילאן", "מייפל",
    "שוקולד", "ממתיק", "מולסה", "צימוקים", "פירות יבשים",
    "sugar", "syrup", "glucose", "fructose", "honey", "date", "chocolate", "maple",
]


@dataclass
class Verdict:
    ok: bool
    food_class: str
    accounted_mass: float | None
    reasons: list[str] = field(default_factory=list)


def _num(v) -> float | None:
    if v is None:
        return None
    if isinstance(v, (int, float)):
        return float(v)
    m = re.search(r"-?\d[\d.]*", str(v).replace(",", "."))
    return float(m.group(0)) if m else None


def check_panel(
    nutr_per_100g: dict,
    food_class: FoodClass | str = FoodClass.DRY_BAR,
    ingredients_text: str | None = None,
) -> Verdict:
    """Validate a per-100g nutrition panel. Returns Verdict(ok, reasons)."""
    if isinstance(food_class, str):
        food_class = FoodClass(food_class)
    reasons: list[str] = []

    kcal = _num(nutr_per_100g.get("energyKcal") or nutr_per_100g.get("energy_kcal")
                or nutr_per_100g.get("energy"))
    carbs = _num(nutr_per_100g.get("carbs") or nutr_per_100g.get("carbohydrates")
                 or nutr_per_100g.get("carb"))
    fat = _num(nutr_per_100g.get("fat"))
    protein = _num(nutr_per_100g.get("protein"))
    sugar = _num(nutr_per_100g.get("sugar"))

    # 1) accounted-mass floor (moisture-aware)
    accounted = None
    if None not in (carbs, fat, protein):
        accounted = carbs + fat + protein
        floor = ACCOUNTED_MASS_FLOOR[food_class]
        if accounted < floor:
            reasons.append(
                f"accounted_mass {accounted:.0f}g < floor {floor:.0f}g for {food_class.value} "
                f"(likely per-serving panel or truncated/contaminated)"
            )
        if accounted > 105:
            reasons.append(f"accounted_mass {accounted:.0f}g > 105g (impossible per-100g)")

    # 2) kcal bounds
    if kcal is not None:
        lo, hi = KCAL_BOUNDS[food_class]
        if kcal < lo or kcal > hi:
            reasons.append(f"kcal {kcal:.0f} outside [{lo},{hi}] for {food_class.value}")

    # 3) kcal vs macros consistency (Atwater: 4/4/9). Allow ~25% slack.
    if None not in (carbs, fat, protein, kcal) and kcal > 0:
        est = 4 * carbs + 4 * protein + 9 * fat
        if est > 0 and abs(est - kcal) / kcal > 0.30:
            reasons.append(f"kcal {kcal:.0f} vs Atwater estimate {est:.0f} (>30% mismatch)")

    # 4) sugar==0 against a sugar-bearing ingredient (the snacks-bug signature)
    if sugar is not None and sugar == 0 and ingredients_text:
        low = ingredients_text.lower()
        hit = next((t for t in SUGAR_BEARING if t.lower() in low), None)
        if hit:
            reasons.append(f"sugar=0 but ingredient list contains '{hit}' (impossible)")

    # 5) all-null panel
    if all(v is None for v in (kcal, carbs, fat, protein)):
        reasons.append("panel is entirely empty (no usable macros)")

    return Verdict(ok=(len(reasons) == 0), food_class=food_class.value,
                   accounted_mass=accounted, reasons=reasons)


def classify_bar(name_he: str, protein_per_100g: float | None) -> str:
    """Split the bar shelf into 'protein_bar' vs 'snack_bar' (TASK-362A rule).
    Protein bar iff name marks חלבון/פרוטאין/protein OR protein >= 20 g/100g."""
    nm = (name_he or "").lower()
    name_marks = any(t in nm for t in ("חלבון", "פרוטאין", "protein"))
    high_protein = protein_per_100g is not None and protein_per_100g >= 20.0
    return "protein_bar" if (name_marks or high_protein) else "snack_bar"


# Countline / single-serve chocolate BARS — owner: a separate page from tablets.
_CHOC_COUNTLINE_BRANDS = [
    "פסק זמן", "קיט קט", "kitkat", "kit kat", "טוויקס", "twix", "מארס", "mars",
    "סניקרס", "snickers", "באונטי", "bounty", "כיף כף", "מקופלת", "קליק", "click",
    "מילקי בר", "מאלטיזרס", "maltesers", "חטיף שוקולד", "lion", "ליאון",
]
# Flat break-apart TABLETS (owner: "טבלאות שוקולד כמו שוקולד פרה").
_CHOC_TABLET_MARKERS = [
    "טבלת", "טבלה", "טבלאות", "שוקולד פרה", "פרה ", "מילקה", "milka", "לינדט",
    "lindt", "טובלרון", "toblerone", "שוקולד מריר", "שוקולד חלב", "שוקולד לבן",
    "elite", "עלית", "ספלנדיד", "splendid",
]


def classify_chocolate(name_he: str) -> str:
    """Split the chocolate shelf into 'chocolate_bar' (countline) vs
    'chocolate_tablet' (טבלת שוקולד, like שוקולד פרה) — owner ruling, TASK-362.
    Four distinct pages total (snack bars / protein bars / chocolate bars /
    chocolate tablets); never rank a tablet against a countline. First-pass rule,
    to be validated against the real scrape like classify_bar was.
    Order: explicit tablet marker → countline brand → tablet brand → default tablet
    (the flat tablet shelf is the broader/default chocolate format)."""
    nm = (name_he or "").lower()
    if any(t in nm for t in ("טבלת", "טבלה", "טבלאות")):
        return "chocolate_tablet"
    if any(b.lower() in nm for b in _CHOC_COUNTLINE_BRANDS):
        return "chocolate_bar"
    if any(b.lower() in nm for b in _CHOC_TABLET_MARKERS):
        return "chocolate_tablet"
    return "chocolate_tablet"


if __name__ == "__main__":
    import sys
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    # self-test: the snacks bug must be caught; real bars must pass.
    bug = check_panel({"energyKcal": 99, "carbs": 10, "fat": 1, "protein": 2, "sugar": 0},
                      FoodClass.DRY_BAR, ingredients_text="סוכר, שוקולד לבן")
    real = check_panel({"energyKcal": 465, "carbs": 64.3, "fat": 17.8, "protein": 8.7, "sugar": 26.8},
                       FoodClass.DRY_BAR, ingredients_text="שיבולת שועל, סוכר לבן")
    cheese_cake = check_panel({"energyKcal": 320, "carbs": 30, "fat": 18, "protein": 6},
                              FoodClass.MOIST_BAKED)
    print("BUG panel  ok=", bug.ok, bug.reasons)
    print("REAL panel ok=", real.ok, "accounted=", real.accounted_mass)
    print("CAKE panel ok=", cheese_cake.ok, "accounted=", cheese_cake.accounted_mass)
    assert not bug.ok and real.ok and cheese_cake.ok, "gate self-test FAILED"
    print("self-test PASS")
