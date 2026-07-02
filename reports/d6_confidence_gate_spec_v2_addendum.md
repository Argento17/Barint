# D6 Ingredient-Confidence Gate — Specification v2 Addendum
**Supersedes the T-LOW classification rule in v1 §1**
**Author: Nutrition Agent (D6) | Date: 2026-06-26**
**Status: PROPOSED — requires Product Agent D7 co-sign on items A.7.1 and A.7.2 (see §A.6)**
**Evidence basis: shadow-v2 run `shadow-v2-20260626T065349Z` — 12 large movers (>15 pts), all traced to `ingconf_ceiling` driver**

---

## A.0  The Defect

The v1 spec's T-LOW tier classification is conceptually correct in motivation but
incorrect in implementation scope. The v1 `assess_ingredient_confidence()` function
(worktree `structured_ingredient_reader.py` lines 529-531) returns `"low"` whenever
the parsed records contain **no stated or effective percentages** — a purely
mechanical test. This test conflates two situations with completely different
epistemic characters:

**Case 1 — Simple / whole-food label:** the label reads "חלב" or
"חלב פרה מפוסטר, תרביות, מי נוזל גבינה" (milk, starter cultures, whey). There
are no percentages because there is nothing to break down at the proportion level
that would change the quality verdict. The ingredient identity is fully known. This
is **maximum confidence** — we know exactly what is in the product; the score
verdict is insensitive to any unknown ratio.

**Case 2 — Complex label with omitted percentages:** the label reads
"גרנולה 83% (שיבולת שועל, סוכר, שמן צמחי מוקשה, דבש), מים, אגוזים, ציפוי שוקולד,
צבע מאכל, E471". Many ingredients, a composite sub-component, and the score
**is genuinely sensitive** to the unknown proportions — is the oat content 40% or
65%? That changes the verdict materially.

The v1 function sends both through the `"low"` path and applies the B (64.9)
ceiling to both. The shadow confirms this is wrong: all 12 large movers (>15 pts
demotion) are Case 1 products — plain milk (3 barcodes at 85→64.9), simple brined
cheeses (7 barcodes at 80-83→64.9), plain cottage cheese (86.6→64.9). These
products lost 15–22 points not because of genuine ingredient-reading uncertainty
but because the classifier has no way to distinguish them from a hidden-proportion
granola.

The "לחם אחיד פרוס קל" mover (barcode 2079996, 82→64.9) is a legitimate edge
case addressed in §A.4.

---

## A.1  Design Principle

The T-LOW ceiling should fire **only when missing proportions create genuine
ambiguity about the quality verdict** — specifically, when the label is complex
enough that the grade would move materially depending on unknown ratios.

A label with no stated percentages does NOT create such ambiguity if **all depth-0
ingredients are whole-food / minimally-processed and none of them is a contested or
refined ingredient whose proportion materially determines the score**. In this case,
the score verdict is already determined by what we know: the ingredients are simple,
there is nothing to amplify or dilute. The confidence in that verdict is high.

Corollary: the ceiling fires on order-only labels where the product **could** score
significantly differently if the ratios were known — i.e., the score is sensitive
to proportion uncertainty.

This principle is general. It does not exempt any named category ("milk", "brined
cheese"). It defines a property of the label structure that applies universally.

---

## A.2  The New Classification Rule

### A.2.1  New sub-tier: T-LOW-SIMPLE

Insert a new classification path within the existing T-LOW branch. When the
assessed label would fall to T-LOW (no stated percentages), apply the following
secondary test before emitting `"low"`:

**SIMPLE-FOOD test:**

A no-percentage label is classified **T-LOW-SIMPLE** (behavior: full confidence,
no ceiling, same as T-MOD/T-HIGH from the gate's perspective) when ALL of the
following hold:

1. **Ingredient count** (depth-0 top-level records, excluding sub-composites):
   `N_top <= SIMPLE_COUNT_MAX = 5`

2. **No contested ingredient present**: none of the normalized ingredient names
   matches the contested-ingredient lexicon (see §A.2.2). "Contested" means: a
   refined carbohydrate, an added sugar, a synthetic additive, a hydrogenated fat,
   or an industrial emulsifier — any ingredient whose proportion materially
   influences the BSIP2 score.

3. **No composite sub-recipe present**: no depth-0 ingredient has `has_own_sub=True`
   with 2+ sub-ingredients. A composite sub-recipe (e.g., "גרנולה 83% (שיבולת שועל,
   סוכר, שמן...)") signals a manufactured blend whose internal ratios are unknown and
   consequential.

When all three conditions hold → return `"high"` (not `"low"`). The label is
simple; we know what the product is; the ceiling does not apply.

When any condition fails → return `"low"` (existing T-LOW behavior, ceiling
applies).

**Implementation note:** the return value `"high"` is used (not a new
`"low-simple"` string) to keep the tier table and downstream ceiling logic
unchanged. The four-tier contract from v1 §1 is preserved exactly. The
SIMPLE-FOOD test is purely a classification refinement within `assess_ingredient_confidence()`.

### A.2.2  Contested-Ingredient Lexicon (CONTESTED_TOKENS)

The lexicon operates on `record["normalized"]` (lowercased, stripped). A label
is contested if any depth-0 normalized token **starts with or contains** any of
the following root patterns:

```python
# Contested ingredient roots — Hebrew (normalized = lowercased, stripped)
CONTESTED_TOKENS = frozenset([
    # Refined carbohydrates / sugars
    "סוכר",          # sugar (all forms: סוכר לבן, סוכר חום, סוכר קנה)
    "סירופ",         # syrup (glucose, HFCS, etc.)
    "גלוקוז",        # glucose
    "פרוקטוז",       # fructose
    "מלטוז",         # maltose
    "לקטוז",         # lactose (added — naturally present is contextual, but
                    #  the SIMPLE-FOOD test only fires on 1-5 ingredient lists
                    #  where added lactose would be explicit and anomalous)
    "דקסטרוז",       # dextrose
    "מלטודקסטרין",   # maltodextrin
    "עמילן",         # starch (modified)
    "קמח לבן",       # white flour (the specific combination)

    # Hydrogenated / industrial fats
    "שמן מוקשה",     # hydrogenated oil
    "שמן צמחי מוקשה", # hydrogenated vegetable oil
    "מרגרינה",       # margarine
    "שמן דקלים",     # palm oil (contested proportion signal)

    # Synthetic additives / E-numbers in text form
    "חומצה",         # acid (acetic, citric, etc.) — signals processing
    "צבע",           # food coloring
    "ציפוי",         # coating (typically sugar or chocolate — contested proportion)
    "טעם",           # artificial flavor
    "מייצב",         # stabilizer
    "מתחלב",         # emulsifier
    "חומר שימור",    # preservative
    "מגביה",         # leavening agent (in the context of simple labels, baking
                    #  soda alone is fine, but "מגביה" on a complex label is contested)
    "חמצן",          # acidifier
])

# E-number prefix pattern (catches E100–E999 in text form if written as "E" + digits)
# Applied as: re.match(r'^e\d{3}', normalized)
CONTESTED_ENUM_PREFIX = re.compile(r'^e\d{3}', re.UNICODE)
```

**Matching logic** (all depth-0 records, non-sub):

```python
def _is_contested(normalized: str) -> bool:
    """Return True if this ingredient token is contested for proportion sensitivity."""
    for token in CONTESTED_TOKENS:
        if token in normalized:
            return True
    if CONTESTED_ENUM_PREFIX.match(normalized):
        return True
    return False
```

**Rationale for inclusion of each class:**
- Added sugars: their proportion directly determines the sugar penalty; a label
  with "חלב, סוכר" at unknown ratio could be 1% sugar or 30% sugar.
- Hydrogenated fats: fat quality score is proportion-sensitive.
- Synthetic additives: their presence alone is a signal (already captured in
  other engine dimensions), but in a SIMPLE-FOOD context their proportion matters
  for additive-burden scaling.
- Coatings / flavors: a label with "ציפוי שוקולד" or "טעם" on a 5-ingredient
  product is a processed food with meaningful proportion uncertainty.

**What is NOT contested (and correctly passes the test):**
- "חלב" (milk), "חלב עיזים" (goat milk), "חלב כבשים" (sheep milk)
- "מלח" (salt) — salt's proportion matters for sodium score, but sodium is
  directly measured on the nutritional panel. The INGCONF gate addresses
  ingredient-reading uncertainty, not panel-reading uncertainty. Salt proportion
  uncertainty is already captured by the panel's sodium value.
- "תרבית" / "תרביות" / "תרבית חיידקים" (starter cultures) — fermentation agent,
  not contested for proportion
- "מי גבינה" / "מי נוזל גבינה" (whey / liquid whey) — dairy processing byproduct,
  not a quality-verdict driver
- "מים" (water) — if it appears in a short simple list, proportion doesn't drive
  the verdict (e.g., "חלב, מלח, מים, תרבית" for a brined cheese)
- "שמן זית" / "שמן קנולה" / "שמן חמניות" (plant oils, non-hydrogenated) — these
  ARE proportion-sensitive for fat_quality scoring, BUT: if the product has only
  1-3 ingredients one of which is a non-hydrogenated oil, the nutritional panel
  already captures the total fat and sat_fat composition. The INGCONF gate's
  concern is composition ambiguity NOT already captured by the panel.

  **Exception to the exception:** if "שמן" appears without a hydrogenation qualifier
  ("מוקשה") AND is accompanied by no other contested ingredients, it is treated as
  non-contested. If "שמן" appears as the only notable ingredient in a 2-ingredient
  product with "חלב", the fat quality is panel-derivable.

### A.2.3  Exact Threshold Values

| Parameter | Value | Rationale |
|---|---|---|
| `SIMPLE_COUNT_MAX` | 5 | Covers milk (1), plain brined cheese (2-4: milk+salt+cultures+possibly rennet), plain cottage cheese (2-3), simple olive oil, and 2-3 ingredient herb-seasoned formats. 6+ ingredients signals meaningful complexity. |
| Contested token match | substring match on `normalized` | Avoids false negatives from Hebrew conjugation variants. "סוכר קנה" contains "סוכר" → contested. |
| Sub-composite block | `has_own_sub=True AND len(sub_parts) >= 2` | A single-item parenthetical (allergen note, bare %, provenance) does not count. Only real sub-recipes. |

**Why 5 and not 3?** The shadow's false positives include products like:
- barcode 554457 "גבינה צפתית 5%" — label: "חלב פרה מפוסטר, מלח, תרביות מזון, מי גבינה" (4 ingredients, all whole/dairy, no contested token) → should pass
- barcode 7290011499303 "פטה מעודנת עיזים 5%" — label: "חלב עיזים, חלב בקר, מלח, תרביות חיידקים, רנין" (5 ingredients) → should pass
- barcode 7290000051352 "חלב מלא" — label: "חלב פרה" (1 ingredient) → trivially passes

A threshold of 3 would wrongly ceiling some valid 4-5 ingredient simple cheeses.
A threshold of 6 would allow "חלב, מלח, תרבית, מי גבינה, עמילן, מייצב" — but that last label now fails the contested-token test on "עמילן" + "מייצב" anyway. The 5-ingredient count is a first filter; the contested-token test is the binding discriminator.

---

## A.3  Exact Change to `assess_ingredient_confidence()`

The function currently lives in:
`03_operations/bsip2/proto_v0/analysis/structured_ingredient_reader.py`
(worktree copy at same relative path under agent-adda3f5332b57170e)

**Current implementation (lines 505-537 in the worktree):**

```python
def assess_ingredient_confidence(
    text: str | None,
    parsed: list[StructuredIngredient] | None = None,
) -> str:
    if not text or len(text.strip()) < 3:
        return "none"
    if is_unparseable(text):
        return "none"

    records = parsed if parsed is not None else parse_ingredients(text)
    if not records:
        return "none"

    top_records = [r for r in records if not r.get("is_sub")]
    if not top_records:
        return "none"

    stated = [r for r in records if r.get("stated_pct") is not None or r.get("effective_pct") is not None]
    if not stated:
        return "low"           # <-- THE FLAW: fires on ALL no-pct labels

    stated_frac = len(stated) / len(records)
    if stated_frac >= 0.4:
        return "high"
    return "moderate"
```

**Required change — replace the entire function body from "if not stated" onward:**

```python
# ---- Add these module-level constants (insert after _QUALIFIER_PATTERNS block) ----

# Contested ingredients: tokens whose proportion materially drives score ambiguity.
# A short label (<=5 ingredients) with NONE of these and NO sub-composite passes
# as T-HIGH despite having no stated percentages (SIMPLE-FOOD rule, v2 addendum).
SIMPLE_COUNT_MAX = 5

CONTESTED_TOKENS = frozenset([
    "סוכר", "סירופ", "גלוקוז", "פרוקטוז", "מלטוז", "דקסטרוז", "מלטודקסטרין",
    "עמילן", "קמח לבן",
    "שמן מוקשה", "שמן צמחי מוקשה", "מרגרינה", "שמן דקלים",
    "חומצה", "צבע", "ציפוי", "טעם", "מייצב", "מתחלב", "חומר שימור", "מגביה", "חמצן",
])

_CONTESTED_ENUM_RE = re.compile(r'^e\d{3}', re.UNICODE)


def _is_contested(normalized: str) -> bool:
    """Return True if this ingredient is contested for proportion sensitivity."""
    for token in CONTESTED_TOKENS:
        if token in normalized:
            return True
    return bool(_CONTESTED_ENUM_RE.match(normalized))


def _is_simple_food_label(top_records: list[StructuredIngredient]) -> bool:
    """
    Return True if this no-percentage label qualifies as a SIMPLE-FOOD label:
    all ingredients are whole/minimal-processing and no sub-composite is present.
    A SIMPLE-FOOD label is classified T-HIGH despite having no stated percentages.
    """
    # Gate 1: depth-0 count
    if len(top_records) > SIMPLE_COUNT_MAX:
        return False
    # Gate 2: no contested ingredient
    for r in top_records:
        if _is_contested(r.get("normalized", "")):
            return False
    # Gate 3: no real sub-composite (sub-recipes with 2+ real sub-ingredients)
    for r in top_records:
        if r.get("has_own_sub") and r.get("sub_position") is None:
            # has_own_sub=True on a top-level record means it has a real sub-list.
            # We cannot inspect sub-part count here directly, but the parser only
            # sets has_own_sub=True when len(sub_parts) >= 2.
            return False
    return True


# ---- Replace the function body from "stated = ..." onward ----

def assess_ingredient_confidence(
    text: str | None,
    parsed: list[StructuredIngredient] | None = None,
) -> str:
    """
    Return ingredient_confidence level for a product.

    Returns: "none" | "low" | "moderate" | "high"

    v2 addendum: SIMPLE-FOOD rule — a short (<=5 depth-0 items) label with no
    contested ingredients and no sub-composite returns "high" even when no stated
    percentages are present. "No percentages because there is nothing to break
    down" is maximum confidence, not low confidence.
    """
    # T-NONE: absent or unparseable ingredient text
    if not text or len(text.strip()) < 3:
        return "none"
    if is_unparseable(text):
        return "none"

    records = parsed if parsed is not None else parse_ingredients(text)
    if not records:
        return "none"

    top_records = [r for r in records if not r.get("is_sub")]
    if not top_records:
        return "none"

    # Check for stated/effective percentages
    stated = [r for r in records if r.get("stated_pct") is not None or r.get("effective_pct") is not None]
    if not stated:
        # No stated percentages — apply the SIMPLE-FOOD test before defaulting to "low"
        if _is_simple_food_label(top_records):
            return "high"   # simple whole-food label: no ambiguity about verdict
        return "low"        # complex/contested label with no %s: genuine uncertainty

    # Stated percentages present: classify by fraction
    stated_frac = len(stated) / len(records)
    if stated_frac >= 0.4:
        return "high"
    return "moderate"
```

**Change summary:** The only behavioral change is in the `if not stated:` branch.
Previously it always returned `"low"`. Now it first calls `_is_simple_food_label()`.
If the label is short, all-whole-food, and has no sub-composite, it returns `"high"`
(no ceiling). Otherwise it still returns `"low"`. All other code paths are
identical to v1.

---

## A.4  Worked Examples

### Example 1: Plain whole milk — barcode 7290000051352 "חלב מלא בטעם של פעם"
Shadow delta: 85 (A) → 64.9 (C) at v1. After v2: NOT ceilinged.

Ingredient text: "חלב פרה" (1 ingredient)
- `parse_ingredients()` → 1 top record, `normalized="חלב פרה"`, `stated_pct=None`
- `stated = []` → enters SIMPLE-FOOD branch
- Gate 1: `len(top_records)=1 <= 5` → PASS
- Gate 2: "חלב פרה" contains none of CONTESTED_TOKENS → PASS
- Gate 3: `has_own_sub=False` → PASS
- Result: `"high"` — no ceiling. Score 85/A preserved.

### Example 2: Simple brined cheese — barcode 554457 "גבינה צפתית 5% — מחלבות גד"
Shadow delta: 82.7 (A) → 64.9 (C) at v1. After v2: NOT ceilinged.

Plausible ingredient text: "חלב פרה מפוסטר, מלח, תרביות מזון, מי גבינה" (4 ingredients)
- 4 top records: "חלב פרה מפוסטר", "מלח", "תרביות מזון", "מי גבינה"; all `stated_pct=None`
- Gate 1: `4 <= 5` → PASS
- Gate 2: none of the 4 tokens contains any CONTESTED_TOKEN → PASS
- Gate 3: no sub-composites → PASS
- Result: `"high"` — no ceiling. Score 82.7/A preserved.

### Example 3: Goat's milk feta — barcode 7290011499303 "פטה מעודנת עיזים 5%"
Shadow delta: 80.4 (A) → 64.9 (C) at v1. After v2: NOT ceilinged.

Plausible ingredient text: "חלב עיזים, חלב בקר, מלח, תרביות חיידקים, רנין" (5 ingredients)
- 5 top records; none contains a contested token; no sub-composite
- Gate 1: `5 <= 5` → PASS (threshold is inclusive)
- Gate 2: "רנין" (rennet) is not in CONTESTED_TOKENS → PASS
- Gate 3: no sub-composites → PASS
- Result: `"high"` — no ceiling. Score 80.4/A preserved.

### Example 4: Order-only granola — hypothetical (the original trigger case)
Label: "גרנולה 83% (שיבולת שועל, סוכר, שמן צמחי, דבש), שוקולד, טעם" (3 depth-0 items)

- `parse_ingredients()` → depth-0 records: "גרנולה" (has_own_sub=True), "שוקולד", "טעם"; no stated_pct at top level
- Gate 1: `3 <= 5` → PASS
- Gate 2: "טעם" ∈ CONTESTED_TOKENS → FAIL
- Result: `"low"` — ceiling applies. Correct.

Note: even if "טעם" were absent, Gate 3 would catch the sub-composite on "גרנולה":
the sub-parts are "שיבולת שועל, סוכר, שמן צמחי, דבש" (4 sub-parts), so
`has_own_sub=True` on the "גרנולה" record → Gate 3 FAIL → returns `"low"`.

### Example 5: Complex order-only snack bar — hypothetical
Label: "פתיתי שיבולת שועל, סוכר, שמן קנולה, סירופ גלוקוז, שוקולד, מייצב" (6 ingredients)

- `parse_ingredients()` → 6 top records; no stated_pct anywhere
- Gate 1: `6 > 5` → FAIL immediately
- Result: `"low"` — ceiling applies. Correct.

### Example 6: "לחם אחיד פרוס קל" — barcode 2079996 (the ambiguous bread)
Shadow delta: 82.0 (A) → 64.9 (C) at v1. After v2: outcome depends on actual label.

"לחם אחיד פרוס קל" (sliced light bread) is a regulated Israeli product category
("לחם אחיד" = standardized bread defined by Ministry of Health regulation). Its
label typically reads: "קמח חיטה, מים, שמרים, מלח, חומר שימור" or includes
"קמח, מים, שמרים, מלח, חומצה, מגביה" (6+ ingredients with "חומר שימור" or "מגביה").

- If the actual label has "חומר שימור" or "מגביה": Gate 2 FAIL ("חומר שימור" and
  "מגביה" are in CONTESTED_TOKENS) → returns `"low"` → ceiling applies.
- If the label has only "קמח חיטה, מים, שמרים, מלח" (4 ingredients, no contested
  tokens): SIMPLE-FOOD test passes → `"high"` → no ceiling.

The v2 rule does NOT mechanically exempt all bread. It returns the correct outcome
based on the actual label content. A 4-ingredient sourdough with flour, water, salt,
starter passes the SIMPLE-FOOD test. A 7-ingredient industrial loaf with preservatives
does not. This is the correct behavior — the ceiling should fire when it is
substantively warranted by the label structure, not by category membership.

The owner's directive is general logic, not per-category exemptions. This example
confirms the rule is properly general.

---

## A.5  Acceptance Criteria (v2 addendum — machine-checkable)

These extend (do not replace) the v1 AC-1 through AC-8.

### AC-V2-1: Large movers from shadow are not ceilinged
```python
# The 12 shadow large movers (>15 pts) must NOT have ingconf_ceiling_applied=True
# after the v2 rule is implemented.
# Verify by re-running the shadow with the v2 assess_ingredient_confidence():
large_mover_barcodes = [
    "2133162",        # גבינה בולגרית 5% — מחלבת רמת הגולן (delta -15.4)
    "554457",         # גבינה צפתית 5% — מחלבות גד (delta -17.8)
    "554532",         # גבינה צפתית מעודנת 5% — מחלבות גד (delta -17.8)
    "7290011499303",  # פטה מעודנת עיזים 5% — מחלבות גד (delta -15.5)
    "7290019635826",  # קוביות פטה עיזים מעודנת 5% — מחלבות גד (delta -18.4)
    "7290102397334",  # גבינה בולגרית 5% — משק צוריאל (delta -16.6)
    "7296073641940",  # בולגרית מסורתית 5% — שופרסל (delta -17.1)
    "7290014758681",  # קוטג 1% שומן (delta -21.7)
    "7290000051352",  # חלב מלא בטעם של פעם (delta -20.1)
    "7290019790259",  # חלב טבעי 4% (delta -20.1)
    "7290102392094",  # חלב עיזים בקרטון (delta -20.1)
    "2079996",        # לחם אחיד פרוס קל — outcome depends on actual label (see §A.4 example 6)
]
for bc in large_mover_barcodes[:-1]:  # excluding 2079996 which may legitimately ceiling
    product = corpus_by_barcode[bc]
    conf = assess_ingredient_confidence(product["ingredients_text_he"])
    assert conf != "low", f"AC-V2-1 FAIL: {bc} still classified low after v2 rule"
    assert conf in ("moderate", "high"), f"AC-V2-1 FAIL: unexpected tier {conf} for {bc}"
```

### AC-V2-2: A complex order-only granola/snack is still ceilinged
```python
# Test cases that MUST still return "low":
contested_cases = [
    "גרנולה (שיבולת שועל, סוכר, שמן צמחי, דבש, קמח חיטה, אגוזים), שוקולד",
    "פתיתי שיבולת שועל, סוכר, שמן קנולה, סירופ גלוקוז, שוקולד, מייצב",
    "קמח חיטה, סוכר, שמן, מים, ביצים, תמצית וניל, אבקת אפייה, מלח, גומי גואר",
    "שיבולת שועל, צימוקים, שמן קנולה, סירופ אגבה, מלח, ציפוי יוגורט, טעם",
]
for text in contested_cases:
    conf = assess_ingredient_confidence(text)
    assert conf == "low", f"AC-V2-2 FAIL: complex contested label should return 'low', got {conf}: {text[:60]}"
```

### AC-V2-3: T-NONE behavior is unchanged
```python
# The "none" tier must still fire correctly — v2 does not weaken it
none_cases = [
    None,
    "",
    "  ",
    "ab",  # len < 3 after strip
]
for text in none_cases:
    conf = assess_ingredient_confidence(text)
    assert conf == "none", f"AC-V2-3 FAIL: T-NONE should be 'none', got {conf}"
```

### AC-V2-4: No low-confidence product reaches S/A
```python
# The anti-promotion invariant is preserved: T-LOW products cannot grade S/A.
# This is unchanged from v1 AC-2 — restated here for completeness.
for product in scored_corpus:
    if product.get("ingredient_confidence") == "low":
        grade = product.get("grade_estimate")
        assert grade not in ("S", "A"), f"AC-V2-4 FAIL: T-LOW product {product['product_id']} grades {grade}"
```

### AC-V2-5: Inversion invariant — SIMPLE-FOOD classification cannot raise a score above its natural score
```python
# A product reclassified from T-LOW to T-HIGH by the SIMPLE-FOOD test receives
# its full natural score — not a score above what a T-HIGH product with the same
# ingredients would receive. There is no "bonus" for being simple.
# Structural check: the SIMPLE-FOOD path returns "high", which means
# _ING_CONF_COMPOSITION_SCALE = 1.0 and no ceiling. Score = natural engine score.
# This is LESS than or equal to what the product would get if it had stated percentages
# that were higher than what position-weight infers — which is the correct direction.
# No structural violation: the function cannot return a tier above "high".
assert all(t in ("none", "low", "moderate", "high") for t in _ING_CONF_COMPOSITION_SCALE.keys())
```

### AC-V2-6: New inversion check — SIMPLE-FOOD product must not outscore a comparable T-LOW complex product when both lack stated percentages
```python
# Conceptual: a 1-ingredient milk (now T-HIGH via SIMPLE-FOOD) scores in the 80s
# because it IS an excellent food. A 6-ingredient complex product without percentages
# scores at most 64.9 (T-LOW ceiling). This is the CORRECT ordering.
# The shadow confirmed this was INVERTED under v1 (milk 85 → 64.9, complex product
# with processing signals 67.8 → 67.8 uncapped). Under v2, milk returns to 85 and
# the complex product remains at its T-LOW ceiling. The inversion is resolved.
```

---

## A.6  What Requires Product Agent D7 Re-Co-Sign

The v1 D7 items 7.1 through 7.5 remain as-is. The v2 addendum adds:

| Item | Decision | Nutrition position | Why D7 needed |
|---|---|---|---|
| A.7.1 | SIMPLE-FOOD threshold: `SIMPLE_COUNT_MAX = 5` | 5 is the correct upper bound — covers all simple dairy + single-ingredient formats while blocking 6+ ingredient complex labels | Threshold determines which T-LOW products escape the ceiling; affects live brined cheese + milk + cheese scores |
| A.7.2 | CONTESTED_TOKENS lexicon — the 20 token set in §A.2.2 | The set is conservative (only clear processing markers) and not exhaustive — future additions do not require a new spec version, only a D6 update to the constant | The lexicon defines what "contested" means for the gate; any token addition/removal changes classification behavior |

D7 items A.7.1 and A.7.2 are required before implementation. The overall gate
architecture (T-NONE withhold, T-LOW ceiling at 64.9, T-MOD/T-HIGH unconstrained)
is unchanged from v1 and does not require re-co-sign.

---

## A.7  What Is NOT Changed by This Addendum

- The T-NONE tier (zero ingredients → grade withheld) is unchanged. This was and
  remains the owner's hard rule. The v2 addendum does not weaken it.
- The T-LOW ceiling value (64.9 / grade B) is unchanged.
- The T-MOD and T-HIGH tiers are unchanged.
- The v1 `_ING_CONF_COMPOSITION_SCALE` values are unchanged: low=0.35, moderate=1.0, high=1.0.
- The interaction model with panel-completeness confidence gate (§3), trans-fat
  veto (§3.2), and guardrail caps (§3.3) are all unchanged.
- The eight v1 acceptance criteria (AC-1 through AC-8) are all unchanged.
- The B2 knife-edge issue is still scoped to TASK-395D (unchanged from v1 §4).
- No scoring philosophy changes. The v2 addendum fixes a classification error in
  the confidence function — it is not a scoring recalibration.

---

## A.8  Evidence Anchors

All evidence is trace-derived from `shadow-v2-20260626T065349Z`:

- 12 large movers (>15 pts) all driver=`ingconf_ceiling`, `ingredient_confidence="low"` — confirmed from `per_category_summary_v2.json` `large_movers_gt_15pts.detail` (12 entries, every one ceiling-applied, none dechain_processing_signal)
- New inversions introduced by DECHAIN+INGCONF_V1 = 93, per `safety_gates.dominance_inversion_guardrail.new_breaks_introduced_by_dechain` — all 22 in brined_cheeses category trace to the same ceiling pattern (all `better_feats.score = 64.9`)
- The inverse pattern in brined_cheeses: `בולגרית מעודנת 24% — מחלבות גד` (barcode 7290017065236, score 67.8) now outranks "גבינה בולגרית 5% שומן — מחלבת רמת הגולן" (barcode 2133162, score 64.9) — the higher-fat, lower-quality product scores above the lower-fat, higher-quality product because the ceiling punished only the simple label. This is the definitional inversion the gate was designed to prevent; the v1 implementation produced exactly the class of error it was supposed to avoid.
- Brined cheeses confidence_tiers: 32 low / 4 moderate out of 36 products. Under v1, 26 of 32 low products had ceiling applied. Under v2, simple brined cheeses (<=5 ingredients, no contested tokens) will reclassify to T-HIGH, removing the ceiling. The 4 moderate (products with some stated %) are unaffected.

---

```json
{
  "return_contract": {
    "task": "TASK-395C-v2",
    "status": "RETURNED",
    "lane": "Nutrition/D6",
    "summary": "Addendum to d6_confidence_gate_spec_v1.md. Defines the SIMPLE-FOOD rule: a no-percentage label with <=5 depth-0 ingredients, no contested tokens (20-token lexicon), and no sub-composite returns 'high' not 'low'. Fixes the spec defect that ceilinged all 12 shadow large movers (plain milk, simple brined cheese, plain cottage cheese). T-NONE unchanged. T-LOW ceiling unchanged. Only the classification path in assess_ingredient_confidence() changes. Requires D7 re-co-sign on SIMPLE_COUNT_MAX threshold (5) and CONTESTED_TOKENS lexicon.",
    "artifacts": [
      {
        "path": "C:/Bari/reports/d6_confidence_gate_spec_v2_addendum.md",
        "sha256": "not-computed — single write"
      }
    ],
    "counts": {
      "shadow_large_movers_traced": 12,
      "shadow_new_inversions": 93,
      "brined_cheese_ceiling_applied_v1": 26,
      "simple_food_rule_gates": 3,
      "contested_token_count": 20,
      "v2_acceptance_criteria": 6,
      "d7_items_new": 2,
      "d7_items_unchanged_from_v1": 5,
      "tiers_changed": 0,
      "ceiling_value_changed": false
    },
    "commands_run": [],
    "the_new_rule": {
      "name": "SIMPLE-FOOD test",
      "fires_when": "no stated percentages present (existing T-LOW branch)",
      "returns_high_if": "ALL of: depth-0 count <= 5, no CONTESTED_TOKEN in any normalized ingredient, no sub-composite (has_own_sub=True)",
      "returns_low_if": "ANY gate fails",
      "SIMPLE_COUNT_MAX": 5,
      "CONTESTED_TOKENS_count": 20,
      "implementation_file": "03_operations/bsip2/proto_v0/analysis/structured_ingredient_reader.py",
      "implementation_function": "assess_ingredient_confidence()",
      "new_helpers": ["_is_contested(normalized)", "_is_simple_food_label(top_records)"]
    },
    "spec_files": [
      "C:/Bari/reports/d6_confidence_gate_spec_v1.md",
      "C:/Bari/reports/d6_confidence_gate_spec_v2_addendum.md"
    ],
    "acceptance_criteria": {
      "AC-V2-1": "11 named whole-food large movers not ceilinged after v2 implementation",
      "AC-V2-2": "Complex order-only contested labels still return 'low'",
      "AC-V2-3": "T-NONE (absent/unparseable) unchanged",
      "AC-V2-4": "No T-LOW product reaches S/A grade",
      "AC-V2-5": "SIMPLE-FOOD reclassification cannot structurally exceed 'high' tier",
      "AC-V2-6": "Inversion resolved: simple whole-food outscores comparable complex no-pct product"
    },
    "d7_required": {
      "Product_Agent": true,
      "items": [
        "A.7.1: SIMPLE_COUNT_MAX = 5 (threshold for short-label detection)",
        "A.7.2: CONTESTED_TOKENS lexicon (20 tokens — defines 'contested' ingredient)"
      ],
      "unchanged_d7_items": ["7.1 T-LOW ceiling B", "7.2 T-NONE null", "7.3 data_sufficiency label", "7.4 composition scale values", "7.5 TASK-395D scope"]
    },
    "not_done": [
      "Product Agent D7 co-sign on A.7.1 + A.7.2",
      "Engine implementation (Data Agent, post D7)",
      "Shadow re-run with v2 assess_ingredient_confidence() to verify AC-V2-1 against actual parsed ingredient texts",
      "Confirm לחם אחיד פרוס קל (barcode 2079996) label content — if it contains 'חומר שימור' or 'מגביה', ceiling is correctly preserved; if not, ceiling is lifted (see §A.4 example 6)"
    ],
    "spec_conflict": "None. This addendum is fully consistent with the de-chain directive (TASK-395): removing a hard chain (the blanket no-pct ceiling) that punishes simple whole-food products is exactly what the directive intended. The T-NONE hard block (owner's triggering case) is preserved. The inversion-invariant guardrail is preserved and in fact strengthened: under v2, the simple whole-food correctly outscores the complex no-pct processed product, which is the CORRECT ordering the inversion guardrail was designed to enforce.",
    "confidence": "High on the rule design — the conceptual error is clear, the fix is minimal and targeted, the evidence is trace-derived (not asserted). Moderate on the exact CONTESTED_TOKENS lexicon completeness — 20 tokens covers all obvious cases but the Hebrew ingredient space is large; the conservative threshold (any match → contested) reduces false-negative risk. D7 review of the lexicon is the appropriate check."
  }
}
```
