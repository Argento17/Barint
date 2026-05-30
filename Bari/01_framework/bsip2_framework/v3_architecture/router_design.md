# BSIP2 Router Design

**Status:** Design specification
**Current implementation:** `category_classifier.py` (single-pass signal accumulator)
**Target:** `router/bsip2_router/`
**Date:** 2026-05-18

---

## Why the Current Router Fails

The current `classify_category()` in `category_classifier.py` works as a single-pass signal accumulator:

1. Score all categories simultaneously by summing matched signal weights
2. Add nutritional profile hints
3. Pick the highest score
4. Compute confidence from ratio of top score to total signal mass

Three structural failures make this approach break as product diversity grows:

**Failure 1 — No hard anchors.**
"גרנולה" appears at weight 0.9 in `snack_bar_granola`. But a granola product containing "שקדים" (0.7) + "אגוזים" (0.7) + "שמן זית" (0.95) accumulates 2.35 in `whole_food_fat` vs 0.9 in `snack_bar_granola`. The granola signal loses. The router has no concept of terms that unconditionally settle the routing question.

**Failure 2 — Ingredient text contamination.**
"חלבון מי גבינה" (whey protein) in a granola's ingredient list triggers `dairy_protein` signals, routing the product to the wrong archetype. The router applies ingredient text signals to most categories without a validity gate (beverages and dairy are already name-only gated — the fix was applied there but not generalized).

**Failure 3 — No hybrid product model.**
A protein drink with 25g protein and NOVA4 signals could legitimately be `dairy_liquid` or behave like a supplement-adjacent product. The current router picks one and loses the interpretive richness. Hybrid products are the rule, not the exception, as product diversity grows.

The cereals run quantified the impact: 6 of 8 granola products misrouted. Each misrouting caused 15-25 point scoring errors — not scoring engine failures but routing failures. The router is the highest-impact single component to fix in the v3 architecture.

---

## Proposed Architecture: Three-Stage Resolution

```
Input: BSIP1 canonical product
            │
            ▼
┌──────────────────────────┐
│   Stage 1: ANCHOR CHECK  │  ← Hard rules on product name only.
│   anchor_resolver.py     │    If any anchor fires: routing is complete.
└───────────┬──────────────┘    Confidence = anchor-declared value (0.85-0.92).
            │  No anchor fired
            ▼
┌──────────────────────────┐
│   Stage 2: SIGNAL SCORE  │  ← Weighted signal accumulation with gating.
│   router.py              │    Ingredient text scope-gated per signal.
│   beverage_gate.py       │    Nutritional hints applied.
│   nutritional_hints.py   │
└───────────┬──────────────┘
            │
            ▼
┌──────────────────────────┐
│   Stage 3: RESOLUTION    │  ← Single archetype OR hybrid declaration.
│   hybrid_resolver.py     │    Instability flag when top-2 delta < 0.3.
└───────────┬──────────────┘
            │
            ▼
Output: archetype, subtype, confidence, instability_flag,
        routing_basis, is_hybrid, hybrid_secondary
```

---

## Stage 1 — Anchor Resolver

Hard anchors are (term → archetype) rules that fire on `canonical_name_he` only. If any anchor fires, routing is complete and signal scoring is skipped.

```python
# anchor_resolver.py
CATEGORY_HARD_ANCHORS = {
    # term: (archetype, subtype, confidence)
    "גרנולה":       ("snack_bar_granola", "granola",          0.87),
    "דגני בוקר":    ("cereal_system",     None,               0.90),
    "קורנפלקס":     ("cereal_system",     "extruded_cereal",  0.90),
    "שיבולת שועל":  ("cereal_system",     "oatmeal",          0.88),
    "מוסלי":        ("snack_bar_granola", "muesli",           0.85),
    "יוגורט":       ("yogurt_system",     None,               0.92),
    "קוטג'":        ("dairy_liquid",      "cottage",          0.92),
    "טחינה":        ("whole_food_fat",    "nut_butter",       0.90),
    "חמאת":         ("whole_food_fat",    "nut_butter",       0.88),  # prefix for חמאת בוטנים, חמאת שקדים
    "קפיר":         ("yogurt_system",     "kefir",            0.92),
    "לחם":          ("bread_system",      None,               0.88),
    "פיתה":         ("bread_system",      "flatbread",        0.90),
}
```

**Anchor design rules:**

1. **Name-only matching.** Anchors match `canonical_name_he`, not ingredient text. A product whose ingredient list contains "שיבולת שועל" but whose name is "עוגיות שיבולת שועל" is not an oatmeal archetype.

2. **Partial match (substring).** "גרנולה" fires for "גרנולה עם אגוזים ודבש" and "גרנולה פצפוצים פריכים".

3. **Conflict resolution.** When multiple anchors fire:
   - More specific term wins: "גרנולה" beats "דגנים" (the latter is a weak snack_bar signal, not an anchor)
   - Higher declared subtype specificity wins: "קורנפלקס" beats "דגני בוקר" for a cornflakes product

4. **Anchor confidence.** Fixed at the anchor's declared level (0.85-0.92). Not signal-derived. High-confidence but not absolute — it reflects that we are applying a rule, not observing a signal.

5. **Trace flag.** `anchor_override: true` appears in the routing trace. Every anchor-driven routing decision is fully visible in the waterfall.

**When NOT to add an anchor:**
Anchors are for terms that unconditionally identify an archetype. Terms that are usually but not always predictive (e.g., "חלבון" — protein — usually means protein cereal but could be in any product) should remain in the signal scoring layer with appropriate weights.

---

## Stage 2 — Signal Scoring

The signal accumulation approach from the current implementation is retained. Three refinements address the failure modes:

### Refinement 1: Signal Scope Classification

Each signal is classified by which text fields it is allowed to match against:

| Scope | Matches against | Use for |
|---|---|---|
| `name_only` | `canonical_name_he` | Beverage, dairy_protein — prevents ingredient leakage |
| `name_weighted` | Name (×2) + ingredient text (×1) | Most cereal, snack_bar signals — name presence counts more |
| `context_gated` | Ingredient text ONLY if name also shows category signal | whole_food_fat signals from nuts/seeds/oils |
| `ingredient_only` | `ingredients_text_he` | Rare — for signals that never appear in product names |

**The context_gated fix for nuts/seeds:**

Current behavior: "שקדים" (0.7) in ingredient text contributes 0.7 to `whole_food_fat` score for any product that contains almonds, including granola.

Proposed behavior: "שקד", "אגוז", "שמן זית" are `context_gated`. They only contribute to `whole_food_fat` if the product name also contains a whole-food-fat context signal ("ממרח", "חמאת", "שמן", "אגוזים טבעיים", "מיקס אגוזים"). A granola whose ingredient list includes almonds does not get a `whole_food_fat` signal contribution.

```python
# ontology/category_markers/signal_weights.py
CATEGORY_SIGNALS = {
    "whole_food_fat": [
        ("שמן", 0.5, "name_weighted"),
        ("טחינה", 0.9, "name_weighted"),
        ("אגוז", 0.7, "context_gated"),   # ← now context_gated
        ("שקד", 0.7, "context_gated"),    # ← now context_gated
        ("שמן זית", 0.95, "context_gated"), # ← now context_gated
        # ...
    ],
}
```

The context gate check: before adding a `context_gated` signal, verify that `any(ctx_signal in name for ctx_signal in WHOLE_FOOD_FAT_CONTEXT_SIGNALS)`.

### Refinement 2: Nutritional Hint Recalibration

Current hint: 350-520 kcal → +0.15 to `snack_bar_granola`. This is too weak to compete with strong `whole_food_fat` signals.

Proposed: When product name contains a cereal/grain context signal AND kcal is in 350-520 range, boost the appropriate cereal/snack_bar archetype by +0.30 (doubled). The rationale: calorie density in this range is expected for granola/cereal products but unusual for pure nut/oil products. When the name also suggests grain context, the nutritional hint should be stronger.

### Refinement 3: Minimum Signal Mass Threshold

Products with total accumulated signal < 0.5 across all categories receive `routing_confidence ≤ 0.40` and `routing_uncertain: true` flag. They route to `default` archetype rather than forcing a spurious category assignment.

Current behavior: any non-zero signal mass produces a category assignment. A product with 0.1 cereal signal and 0.05 snack_bar signal routes to cereal with 0.47 confidence. This is a fabricated confidence value for a genuinely ambiguous product.

---

## Stage 3 — Hybrid Resolution

Some products genuinely straddle two archetypes. The router identifies these explicitly.

**Hybrid detection:** A hybrid is declared when:
- The top two archetype signal scores differ by < 0.3, AND
- Both archetypes form a recognized hybrid pair

```python
# hybrid_resolver.py
HYBRID_ELIGIBLE_PAIRS = frozenset({
    frozenset({"dairy_liquid", "supplement_system"}),  # protein-fortified dairy drinks
    frozenset({"snack_bar_granola", "cereal_system"}), # cereal-positioned granola
    frozenset({"dairy_liquid", "beverage"}),            # plant milks, kefir drinks
    frozenset({"cereal_system", "whole_food_fat"}),     # very nut-heavy muesli (edge case)
})
```

**Hybrid scoring behavior:**
The product is scored under both archetypes. The primary archetype score appears in the leaderboard. The secondary score appears in the trace as `secondary_interpretation_score`. Both are fully traced. This is valuable for research but does not create ambiguity in the ranking — there is always one primary score.

**Not-hybrid behavior:**
When the top-2 delta is small but the pair is NOT in `HYBRID_ELIGIBLE_PAIRS`, the router flags `routing_instability_flag: true` but does NOT produce a hybrid score. The instability flag triggers a lower confidence ceiling and a note in the trace: "secondary candidate was close — verify routing manually."

---

## Routing Inputs

The router reads from the BSIP1 canonical product directly. It does NOT use:
- Any signal from `signal_extractor.py` — signals are computed after routing
- Any score from a previous BSIP2 run
- Any human category annotation

| Input | BSIP1 field | Stage used |
|---|---|---|
| `canonical_name_he` | Required | Stage 1 (anchors), Stage 2 (name signals) |
| `ingredients_text_he` | Standard | Stage 2 (ingredient signals, gated) |
| `ingredients_list` | Required | Stage 2 (length hint) |
| `normalized_nutrition_per_100g` | Required | Stage 2 (nutritional hints) |
| `brand` | Standard | Stage 1 (brand anchors for known plant-milk brands) |
| `nutrition_basis_claimed` | Standard | Stage 2 (beverage liquid gate) |

---

## Confidence Model

| Band | Range | Meaning | Effect |
|---|---|---|---|
| high | ≥ 0.80 | Clear anchor or dominant signal | Full archetype parameters. No threshold relaxation. |
| medium | 0.50-0.79 | Multiple signals agree; secondary candidate plausible | Full parameters with 10% threshold relaxation (SRC-07) |
| low | 0.30-0.49 | Weak signals or near-tie | Calorie density threshold relaxed 10%. Instability flag set. |
| uncertain | < 0.30 | Insufficient signal | Routes to `default` archetype. Score marked `context_limited`. |

Anchor-forced routing always produces `high` confidence (anchors declare their confidence at 0.85-0.92). The fixed value is honest: it is not signal-derived certainty but rule-derived confidence, and it is appropriately lower than a 0.95+ signal-derived classification would be.

---

## Routing Error Taxonomy and Guards

| Error class | Canonical example | v3 guard |
|---|---|---|
| **Ingredient contamination** | Protein granola → dairy_protein (from "חלבון מי גבינה" in ingredients) | Protein signals become name_only or context_gated |
| **Fat signal dominance** | Seeds granola → whole_food_fat (0.95 from "שמן זית") | whole_food_fat nut/oil signals become context_gated |
| **Name token contamination** | Cheerios "עם אגוזים" → whole_food_fat | "אגוז" in product name: context_gated; only fires if name lacks cereal signals |
| **Anchor absent, signal weak** | Kellogg's whole grain cornflakes → snack_bar_granola | "קורנפלקס" anchor fires before signal scoring |
| **Nutritional hint too weak** | Bircher muesli → dairy_protein (high protein hint) | "מוסלי" anchor fires at 0.85 |
| **Unknown brand, low confidence** | Generic import with no Hebrew name signals | Minimum signal mass threshold routes to default |

---

## Routing Trace Output

Every routing decision is fully traceable. The router output includes:

```json
{
  "archetype": "snack_bar_granola",
  "archetype_subtype": "granola",
  "routing_confidence": 0.87,
  "routing_confidence_band": "high",
  "routing_basis": ["hard_anchor:גרנולה"],
  "anchor_override": true,
  "routing_instability_flag": false,
  "secondary_archetype": "whole_food_fat",
  "secondary_archetype_confidence": 0.21,
  "is_hybrid": false,
  "raw_archetype_scores": {
    "snack_bar_granola": 0.87,
    "whole_food_fat": 0.21,
    "cereal_system": 0.15
  },
  "routing_version": "v3.0"
}
```

The `raw_archetype_scores` field makes post-hoc routing analysis possible without re-running the pipeline. When a routing decision is questioned, the scores show exactly why the router chose what it chose.

---

## What the Router Does NOT Do

**Does not score the product.** Routing happens before signal extraction. The router works only from the raw BSIP1 fields: name, ingredient text, nutrition values, brand.

**Does not create a new archetype for edge cases.** A product that doesn't fit well is routed to the nearest archetype with a low confidence flag and a `context_limited` note. Creating a new archetype for every edge case is the path to combinatorial explosion.

**Does not override the scoring engine.** The router's output is an archetype designation and confidence. Everything downstream — signal extraction, NOVA proxy, dimension scoring, guardrails, floors — proceeds unchanged. The router sets the interpretation context; it does not control the interpretation.
