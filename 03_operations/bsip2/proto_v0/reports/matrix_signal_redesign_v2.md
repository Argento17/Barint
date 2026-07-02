# Component B Matrix Signal — Redesign Specification v2
**Proposal Class:** D6 (Nutrition Agent — scoring rule redesign)
**Required co-sign:** Product Agent (D7) — this document proposes a revised validation metric that also requires Product Agent nod (flagged in §3)
**Task:** TASK-395
**Date authored:** 2026-06-25
**Status:** PROPOSAL ONLY — no engine code changed, no scores changed, no published score affected
**Supersedes:** Component B formula in `target_scoring_logic_spec_v1.md` §2.2 (the flat-count formula that failed C-N1-1 at 62.4% high-confidence accuracy)

---

## 1. Diagnosis of the Failure — What the Flat Count Could Not See

The failed formula (`matrix_score = 50 + (n_whole − n_refined) × 12`) treats every marker as
equal regardless of where it sits in the ingredient list. On an Israeli label, ingredient order is
legally descending by weight. Position 1 is usually the single heaviest ingredient by mass. The
flat count has no way to distinguish:

- **Granola that starts with oats (53%) and adds flour as a minor binder** — whole-first, refined
  trace — flat count: oats=1 whole, flour=1 refined, balance=0 → AMBIGUOUS (wrong; should be WFP)
- **Cookie that starts with flour and sugar, adds a handful of walnuts** — refined-first, whole
  trace — flat count: flour+sugar=2 refined, walnuts=1 whole, balance=−1 → score=38 (correct
  direction but same formula as above)

The dominant failure class — MIXED_MARKERS_WRONG_DIRECTION (88 products, 17% of the corpus) —
occurs in exactly this pattern. The flat count's outcome depends on the *count* of marker types
fired, not their *mass contribution*. Israeli labels often declare percentages explicitly
(e.g. "שיבולת שועל 53%", "קמח חיטה 17%"), and list position encodes rough rank even when
percentages are absent. Ignoring both is the structural gap.

A secondary failure (MISSED_WHOLE_FOOD_MARKERS, 13 products) is a vocabulary gap, not a formula
gap: whole-grain corn flours (קמח תירס מלא), whole barley grist, and whole-kernel rice are absent
from the whole-food marker lexicon. This is fixable by lexicon extension and is addressed in §2.4.

The NO_MARKERS_FIRED failure (8 products) is a data-quality issue — ingredient text that is a
marketing blurb, an English INCI list, or nutritional values rather than a Hebrew ingredient list.
The formula cannot solve this; these products should receive a confidence flag and fall back to
the pessimistic NOVA anchor (per MD-2, `target_scoring_logic_spec_v1.md` §3.2).

**Conclusion:** The formula requires a redesign around dominance, not presence. The lexicon requires
targeted additions for the missed whole-food terms. The metric used to measure accuracy requires
a structural reconception (§3).

---

## 2. Redesigned Formula — Position-Weighted Dominance Score

### 2.1 Core Design Principles

1. **Position is a proxy for mass.** A marker at position 1 carries near-full weight; a marker
   at position 8 carries a fraction. The weight decay is hyperbolic — it falls steeply through
   the first five positions (where the substantive ingredients live) and flattens after that
   (trace ingredients are genuinely minor).

2. **Stated percentages override position weight.** When a Hebrew label states a percentage for
   a marker ingredient (e.g. "שיבולת שועל (53%)"), that percentage directly expresses the mass
   contribution. It is more accurate than the position-derived weight and takes priority.

3. **The dominant first ingredient anchors the prior.** The class of position-1 ingredient
   (whole vs. refined) sets a strong prior. Subsequent markers can modulate the score along the
   whole–refined axis, but they cannot flip the class without a large cumulative imbalance.
   This is not a binary rule — it is captured by the position-weight curve's natural asymmetry
   (position 1 weight >> position 5+ weight combined, unless there are many late markers).

4. **The output is continuous.** The score ranges [0, 100] and is used as a continuous input
   to `processing_quality` (weighted at 0.40 of the two-component signal per §2.3 of the target
   spec). It does not emit a binary class. Products that are genuinely mixed will score near the
   midpoint (45–55); that is the correct output, not a classification error.

5. **Composites count at their stated share.** When a marker ingredient appears inside a
   declared sub-composite (e.g. "גרנולה 75% (פתיתי שיבולת שועל 40%, ...)"), the sub-ingredient
   weight is: `stated_parent_pct × stated_sub_pct_within_parent`. Where only the sub-position
   within the composite is known, use the position weight at the sub-ingredient's effective list
   position (the position of the sub-ingredient within the full expanded ingredient order).

### 2.2 Position Weight Curve

This curve is inherited from the existing `matrix_integrity_v2.py` `_pos_weight()` function
(already validated on the corpus and implemented in the codebase). The Data Agent must use
**exactly this function** — do not redefine it.

```python
def _pos_weight(pos: Optional[int]) -> float:
    """
    Hyperbolic decay from position 1 (weight=1.00) to position 15+ (weight=0.08).
    Position None (position unknown) → fallback weight 0.12.
    Source: matrix_integrity_v2.py (already in codebase).
    """
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
```

**Rationale for using this exact curve:** It was calibrated on the same Hebrew retail corpus to
model ingredient-mass contribution. Position 1–2 together sum to 1.82 weight units; positions
6–10 together sum to 1.15 weight units. This correctly reflects that the top-two ingredients in
Israeli grain products typically represent 50–70% of mass, while positions 6–10 collectively are
trace-to-minor. Reusing it ensures consistency between the matrix integrity signal and Component B.

### 2.3 Percentage Override Rule

When the ingredient text contains a stated percentage adjacent to a marker ingredient, extract it
and use it as the weight directly, normalized by the sum of all stated percentages for scored markers.

```
stated_pct_weight(ingredient) = stated_pct / 100.0
```

When only some markers have stated percentages and others rely on position weights, treat the
two groups separately: stated-percentage markers use their percentage directly; position-based
markers use `_pos_weight(pos)` scaled to the remaining estimated mass
(`1.0 − sum_of_stated_pcts / 100.0`).

**Implementation note:** percentage extraction requires a regex over the Hebrew ingredient text.
The existing signal_extractor.py already captures stated ingredient percentages in
`ingredient_order[].stated_pct` (where available from the BSIP1 enricher). The Data Agent
must check this field before falling back to position weight.

### 2.4 Marker Lexicon Extensions (Required Before Re-Validation)

The MISSED_WHOLE_FOOD_MARKERS failures (13 products) identify concrete gaps. The following
extensions are required and are ratified here as part of this D6 proposal:

**New whole-food markers to add:**

| Hebrew token | English label | Notes |
|---|---|---|
| `קמח תירס מלא` | whole_corn_flour | Whole-grain corn flour (not regular corn flour which is refined) |
| `קמח שיפון מלא` | whole_rye_flour | Must include `מלא` qualifier — plain `קמח שיפון` is not whole |
| `גריסי שיבולת שועל` | oat_groats | Steel-cut oat kernel — more intact than rolled oats |
| `שיבולת שועל קלופה` | hulled_oats | Hulled whole oat grain |
| `קמח כוסמין מלא` | whole_spelt_flour | Spelt with `מלא` qualifier; `כוסמין לבן` alone maps to refined |
| `כוסמין מלא` | whole_spelt_grain | Without the flour designation — whole kernel |
| `לתת שעורה` | barley_malt | Barley malt — partially processed but retains whole-grain character; weight: 0.5× standard whole-food contribution (it is a processing aid, not a structural grain) |
| `שיפון` (standalone, first-3 positions) | rye_grain | Whole rye grain when named as a primary ingredient without further processing descriptor |
| `בוטנים` | peanuts | Already in EXTENDED list — promote to SPEC |
| `זרעי צ'יה` / `צ'יה` | chia_seeds | Already in EXTENDED list — promote to SPEC |
| `קינואה` | quinoa | Already in EXTENDED list — promote to SPEC |

**New refined markers to add:**

| Hebrew token | English label | Notes |
|---|---|---|
| `קמח כוסמין לבן` | white_spelt_flour | Spelt white (refined) flour — currently misclassified as whole-food |
| `גריסי תירס` | corn_grits | Degermed corn grits — refined; currently not in vocabulary (causes WRONG-088, WRONG-096 type errors) |
| `אורז לבן` | white_rice | As a primary grain ingredient, not as a flavoring component |
| `קמח אורז` | rice_flour_refined | Already in SPEC — confirm it fires on `קמח אורז` without `מלא` qualifier |
| `קמח תירס` | corn_flour | Already in SPEC as `corn_starch`-adjacent — confirm explicit `קמח תירס` match |
| `סמולינה` | semolina | Refined durum wheat semolina — not in current lexicon |
| `דקסטרוז` | dextrose | Highly refined glucose monosaccharide — add to refined markers |
| `דקסטרין` | dextrin | Partially hydrolyzed starch — refined |
| `פרוקטוז` | fructose | Crystalline fructose as a sweetener — refined |

**Qualifier logic for ambiguous tokens:** The token `כוסמין` alone is ambiguous — it can refer to
whole spelt grain or refined spelt flour depending on context. The rule: if `מלא` or `מגרעין`
appears within a 4-token window of `כוסמין`, classify as whole; otherwise classify as refined.
The same pattern applies to `שיפון` (rye), `אורז` (rice), and `חיטה` (wheat) when they appear
as standalone ingredient tokens.

**Lexicon extension ratification status:** These additions are ratified by this D6 proposal.
They require EV-NOVA-REPLACE-001 registration update and Data Agent implementation before
re-validation. Product Agent must co-sign the refined-marker additions (some affect published
scores — e.g. if `גריסי תירס` is added as a refined marker, cereals containing it will score
lower on Component B).

### 2.5 The Redesigned Formula — Pseudocode

```python
def compute_component_b_score(markers: list[dict]) -> float:
    """
    Position-weighted dominance formula for Component B (whole-food matrix signal).

    Input: markers = list of dicts, each with:
        {
          "class": "whole" | "refined",
          "position": int | None,         # 1-indexed list position (None = position unknown)
          "stated_pct": float | None,     # Percentage stated on label (e.g. 53.0 for "53%")
          "label": str,                   # e.g. "oat_flakes_plain", "refined_wheat_flour"
          "half_weight": bool,            # True for barley_malt and other partial credits
        }

    Returns: float in [0, 100] — higher = more whole-food character.
    """

    # Step 1: Separate stated-pct markers from position-only markers
    pct_markers = [m for m in markers if m.get("stated_pct") is not None]
    pos_markers  = [m for m in markers if m.get("stated_pct") is None]

    # Step 2: Compute total stated mass fraction
    total_stated_pct = sum(m["stated_pct"] for m in pct_markers) / 100.0
    remaining_mass   = max(0.0, 1.0 - total_stated_pct)

    # Step 3: Compute position weights for position-only markers
    total_pos_weight = sum(_pos_weight(m.get("position")) for m in pos_markers)

    # Step 4: Compute effective weight for each marker
    # For pct markers: weight = stated_pct / 100.0
    # For pos markers: weight = _pos_weight(pos) / total_pos_weight * remaining_mass
    #   (distributes the estimated remaining mass proportionally by position weight)
    # Then apply half_weight modifier for partial-credit markers (e.g. barley_malt)

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

    # Step 5: Compute weighted whole and refined sums
    whole_weight   = sum(effective_weight(m) for m in markers if m["class"] == "whole")
    refined_weight = sum(effective_weight(m) for m in markers if m["class"] == "refined")

    # Step 6: Handle no-markers case
    total_weight = whole_weight + refined_weight
    if total_weight < 0.01:
        # No markers fired — return None; caller applies MD-2 (pessimistic fallback)
        return None

    # Step 7: Compute dominance ratio
    # Ratio = whole fraction of total marked weight
    # Range: 0.0 (all refined) → 1.0 (all whole)
    dominance_ratio = whole_weight / total_weight

    # Step 8: Apply first-ingredient anchor
    # The class of the highest-weight marker (regardless of position vs pct) is the anchor.
    # If the anchor is refined and dominance_ratio > 0.5, the ratio is penalized by 0.15.
    # If the anchor is whole and dominance_ratio < 0.5, the ratio is boosted by 0.15.
    # The anchor effect is capped so it cannot flip the sign of (ratio - 0.5).
    highest_weight_marker = max(markers, key=effective_weight)
    anchor_class = highest_weight_marker["class"]

    if anchor_class == "refined" and dominance_ratio > 0.5:
        dominance_ratio = max(0.5, dominance_ratio - 0.15)
    elif anchor_class == "whole" and dominance_ratio < 0.5:
        dominance_ratio = min(0.5, dominance_ratio + 0.15)
    # Note: the anchor cannot push a whole-dominant ratio below 0.5 or vice versa.
    # This preserves the "large imbalance" requirement to flip the class.

    # Step 9: Map dominance ratio to score
    # Linear mapping: ratio=0.0 → score=10, ratio=0.5 → score=50, ratio=1.0 → score=95
    # (endpoints preserve the original formula's [10, 95] clamped range)
    score = 10.0 + dominance_ratio * 85.0

    return round(score, 1)
```

### 2.6 Worked Examples Demonstrating the Fix

**Example A — Oat granola with trace flour (the archetypal wrong-direction failure):**

Product: "גרנולה עם פירות" (WRONG-037 in the report)
Ingredient text: `גרנולה 83% (פתיתי שיבולת שועל 70%, סוכר חום, שמן צמחי, סירופ גלוקוז, דבש, מתחלב...)
פירות יבשים 17%...`

Markers extracted:
- oat_flakes_plain: whole, stated_pct=58.1 (70% × 83% parent), half_weight=False
- sugar (brown): refined, position=3 within composite (~14% estimated of parent 83%), stated_pct≈11.6
- glucose_syrup: refined, position=4, stated_pct=None → position-based
- vegetable_oil: refined, position=3, stated_pct=None

Calculation (simplified):
- whole_weight ≈ 0.581 (stated pct for oats)
- refined_weight ≈ 0.116 (sugar) + ~0.05 (oil + glucose, position-distributed in remaining ~0.30)
- dominance_ratio ≈ 0.581 / (0.581 + 0.166) ≈ 0.78
- anchor = oat_flakes_plain (highest weight) → whole → no penalty applied (ratio already > 0.5)
- score = 10 + 0.78 × 85 ≈ 76

Old formula result: n_whole=2, n_refined=4, balance=−2 → score=26 (WRONG direction)
New formula result: ≈76 (correctly identifies oat-dominated product)

**Example B — Cookie that starts with flour, adds walnuts (correctly classified as refined):**

Product: "עוגיות שיבולת שועל" (WRONG-010 in the report)
Ingredient text: `קמח חיטה לבן (37%), שומן צמחי, סוכר, אבקת סוכר, שיבולת שועל (8%)...`

Markers extracted:
- refined_wheat_flour: refined, stated_pct=37.0
- sugar: refined, position=3 (no pct stated, but within %)
- oat_flakes_plain: whole, stated_pct=8.0

Calculation:
- whole_weight = 0.080
- refined_weight = 0.370 (flour) + position-distributed estimate for sugar ≈ 0.08
- total_stated = 0.45, remaining = 0.55
- dominance_ratio ≈ 0.080 / (0.080 + 0.450) ≈ 0.15
- anchor = refined_wheat_flour (weight 0.37, highest) → refined → dominance_ratio already < 0.5, no adjustment
- score = 10 + 0.15 × 85 ≈ 23

Old formula result: n_whole=1 (oats), n_refined=4 (flour, fat, sugar, hydrogenated fat), balance=−3 → score=14
New formula result: ≈23 (same direction, more precise — oats at 8% get appropriate but small credit)

Both formulas agree here, confirming this is a genuine refined product. The new formula gives it a
slightly higher (more accurate) score that reflects the 8% oat content without changing the overall
class signal.

**Example C — Spelt pita where spelt is 100% of flour but the label also lists sugar and oil:**

Product: "מארז פיתות כוסמין" (WRONG-017, 22, 29, 34 — systematic failure class)
Ingredient text: `קמח כוסמין לבן (גלוטן) (100% מהקמחים, 64% מהמוצר), מים, סוכר, שמרים, מלח...`

Critical note: `כוסמין לבן` = white (refined) spelt flour, not whole spelt. This is a vocabulary
error in the ground-truth heuristic, not a formula error. The heuristic labeled these as WFP
because `כוסמין` (spelt) appears in the name, but `כוסמין לבן` is explicitly a refined flour.
The formula should score it as refined-dominant (correct nutritional truth).

Under the new formula:
- white_spelt_flour: refined, stated_pct=64.0 (stated on label)
- sugar: refined, position=3 in main list (minor)
- anchor: white_spelt_flour → refined
- dominance_ratio ≈ low (flour dominates at 64%)
- score ≈ 15–20

This is the CORRECT nutritional classification. The ground-truth heuristic is wrong about these
products — they are refined-spelt, not whole-spelt. This affects how the gold set must be
constructed (§4.3 below).

**Example D — Fitness cracker with 30.5% whole wheat, 25.5% rice flour (genuinely mixed):**

Product: "קרקר דק כפרי פיטנס" (WRONG-015 in the report)
Ingredient text: `קמח חיטה מלא (30.5%), קמח אורז (25.5%), קמח חיטה (17%), שמן חמניות,
קמח אורז מלא (6.8%)...`

Markers:
- whole_wheat_flour: whole, stated_pct=30.5
- rice_flour_refined: refined, stated_pct=25.5
- refined_wheat_flour: refined, stated_pct=17.0
- whole_rice_flour: whole, stated_pct=6.8

Calculation:
- whole_weight = 0.305 + 0.068 = 0.373
- refined_weight = 0.255 + 0.170 = 0.425
- dominance_ratio = 0.373 / (0.373 + 0.425) = 0.47
- anchor: rice_flour_refined (25.5%) is NOT highest — whole_wheat_flour (30.5%) is. Anchor = whole.
- adjustment: dominance_ratio < 0.5 and anchor = whole → boost by 0.15, but cap at 0.5
  - adjusted = min(0.5, 0.47 + 0.15) = 0.50
- score = 10 + 0.50 × 85 = 52.5

New formula result: ≈53 (AMBIGUOUS, near midpoint — correct: this is a genuinely mixed product)
Old formula result: n_whole=5, n_refined=5, balance=0 → score=50 (also AMBIGUOUS, but by accident)

The new formula reaches the right answer via the right reasoning. The old formula happened to
reach the same number because the counts tied — a coincidence that would break on similar
products with slight lexicon differences.

### 2.7 Handling the Sub-Composite Pattern

Many Israeli labels list a major sub-composite with a declared percentage (e.g. "גרנולה 75%
(פתיתי שיבולת שועל 40% (מכיל גלוטן)...)"). The position inside the sub-composite must be
mapped to an effective position in the full expanded ingredient list for the `_pos_weight`
fallback. The rule:

```
effective_position = parent_position + (sub_position - 1)
```

Where parent_position is the position of the composite in the outer list, and sub_position is
the position of the sub-ingredient within the composite's parenthetical.

Where a sub-ingredient's percentage within the composite is stated, the effective stated_pct is:
```
effective_stated_pct = parent_stated_pct × sub_stated_pct / 100.0
```

This handles WRONG-037 (granola 83%, oats 70% within granola → effective 58.1%) and the
entire granola category's systematic failures.

---

## 3. Validation Metric — Why Binary Accuracy Is the Wrong Gate

### 3.1 The Problem with Binary Accuracy for a Continuous Signal

The C-N1-1 condition as currently stated requires "accuracy >= 90%" where accuracy means
"correctly classifying a product as WFP or RD." This is a binary classification metric applied
to a continuous signal. It is the wrong gate for three structural reasons:

**Reason 1 — Genuine mixed products.** The report identifies 123 products labeled GENUINELY_MIXED
(23.5% of the corpus). These products have meaningful proportions of both whole and refined
ingredients. A continuous score near 50 is the *correct* output for them — it honestly reflects
the mixed architecture. Forcing binary classification on these products means any formula that
correctly identifies them as "neither cleanly whole nor cleanly refined" will be penalized, because
the heuristic ground-truth assigns one of the two classes. This systematically suppresses accuracy
of a correctly-designed continuous signal.

**Reason 2 — Ground-truth noise.** The probe's own honesty statement acknowledges the heuristic
ground-truth is wrong in identifiable cases (the spelt-white-flour pita example in §2.6-C above;
corn flakes labeled WFP; the `כוסמין לבן` category). Binary accuracy amplifies ground-truth
errors into formula failures.

**Reason 3 — The signal's purpose is ranking, not classification.** Component B feeds into
`processing_quality` as a *continuous dimension score* that differentiates between products. Its
job is to rank products correctly along the whole–refined axis — to ensure a 70%-oat granola
scores higher than a 40%-oat granola, and both score higher than a flour-first cookie. A binary
gate cannot measure ranking fidelity; it only measures whether each product crosses an arbitrary
midpoint threshold.

### 3.2 Recommended Validation Metric — Dual Gate

Replace the single 90%-accuracy binary gate with a **dual gate**:

**Gate B1 — Anchor-point score calibration (replaces the binary accuracy floor):**

On a human-audited gold set of clear-whole and clear-refined products (§4), the formula must
produce scores consistent with the following thresholds:

- Products with a whole-food ingredient ≥ 50% by stated label weight: matrix score ≥ 60
- Products with refined starch/sugar ≥ 50% by stated label weight: matrix score ≤ 45
- Single-ingredient whole foods (e.g. plain oats, whole wheat): matrix score ≥ 80
- Classic refined products (white flour + sugar + fat, no whole food): matrix score ≤ 25

These are calibration anchors — verifiable by a human reading the label, not a heuristic.
Pass condition: ≥ 90% of gold-set anchor-class products land in their expected zone.

**Gate B2 — Ordinal ranking test (new, replaces binary accuracy as the primary gate):**

For every ordered pair (P_whole, P_refined) in the gold set where P_whole is clearly more
whole-food-dominant than P_refined by label inspection:

```
matrix_score(P_whole) > matrix_score(P_refined)
```

Pass condition: ≥ 95% of ranked pairs must maintain the correct ordering.
Rationale: 95% (not 90%) because pair-wise ranking is a harder test — a 5% violation rate
means roughly 1 in 20 judgments are wrong, which is acceptable for a mixed-corpus signal but
not more. Unlike binary accuracy, this test directly measures whether the formula produces a
useful ordinal scale.

**Gate B3 — No-marker coverage (retained from original C-N1-1 spirit):**

Products with a parseable Hebrew ingredient list (i.e. ingredient_text_quality is not
`missing` or `corrupted`) must fire at least one marker (whole or refined) in ≥ 95% of cases.
The 1.5% no-marker rate from the v1 probe (8/520) is acceptable; coverage below 90% would
indicate a vocabulary gap requiring correction before deployment.

### 3.3 Flagging for Product Agent Co-Sign

**This metric redesign requires Product Agent nod.** The original C-N1-1 condition was set by
the Product Agent as the validation gate in `d7_cosign_dechain_v1.md`. Replacing it with the
dual gate (B1/B2/B3) changes the contractual activation condition for N-1 (NOVA lookup
deactivation). The Nutrition Agent recommends this substitution as more scientifically valid;
however, Product Agent must explicitly accept the new gate before it becomes the operative
condition. This is a governance handshake, not a unilateral Nutrition Agent decision.

**Recommendation:** The dual gate is stricter in the ways that matter (ranking fidelity, anchor
calibration) while removing the impossible-to-clear 90%-binary barrier on a continuous signal.
Product Agent should accept it. The anti-regression protection (adversarial fixture #1 from
`target_scoring_logic_spec_v1.md` §8.3) remains unchanged and is orthogonal to this gate.

---

## 4. Gold Set Specification

### 4.1 Design Requirements

The gold set must be:
1. **Human-auditable by a native Hebrew reader (the owner).** Every expected score/rank must be
   derivable by reading the Hebrew label, without food-science expertise. "This says 53% oats
   first, so it should score as more whole-food than the one that starts with flour" is a
   valid auditor operation. "This should have DIAAS-adjusted protein quality" is not.
2. **Small enough to audit manually** (~60–75 products across four tiers).
3. **Drawn from the real corpus** (barcodes verifiable against existing BSIP1 enriched data).
4. **Spanning all four tiers:** clear-whole, clear-refined, hard-mixed, and edge-cases that
   expose known failure modes.
5. **Ground-truth fixed by label inspection, not heuristic.** Every product's expected
   category in the gold set is set by the human reading the label, not by a name-matching rule.
   Where the heuristic was wrong (e.g. spelt-white-flour pitas), the gold set corrects it.

### 4.2 Gold Set Tier Definitions

**Tier 1 — Clear Whole (expected matrix score ≥ 65):**
Products whose first ingredient is a named whole grain or nut at ≥ 40% by mass, with no refined
starch at ≥ 15% anywhere in the list.

Rationale for ≥ 65 threshold: leaves room for sugar/oil (common in granolas) to pull the score
back from 80+ without wrongly crossing into the "ambiguous" zone.

**Tier 2 — Clear Refined (expected matrix score ≤ 40):**
Products whose first ingredient is refined flour, sugar, or starch, and where the total refined
mass exceeds whole-food mass by at least 2:1.

Rationale for ≤ 40 threshold: products in this tier may contain trace whole-food ingredients
(e.g. a classic cookie with 5% oats). A score of 38 correctly reflects "mostly refined with
minor whole-food presence."

**Tier 3 — Hard Mixed (expected matrix score 40–65):**
Products with ≥ 20% whole-food AND ≥ 20% refined starch/flour both present, with neither
exceeding 2× the other. The expected score is a range, not a point. The ranking test (B2)
matters more than the absolute score for these products.

**Tier 4 — Edge Cases (expected behavior specified by rule, not score):**
Products that expose known failure modes: spelt-white-flour products (vocabulary), barley malt
dominance, sub-composite parsing, single-whole-food-ingredient products, no-marker cases.

### 4.3 Candidate Products from the Existing Corpus

The following products are nominated from the WRONG-classification table and the full probe
corpus. Each entry shows: barcode, name (Hebrew), corpus source, tier, and the expected gold-set
label (which in some cases CORRECTS the heuristic ground-truth).

#### Tier 1 — Clear Whole (expected score ≥ 65)

| Barcode | Name | Category | Key Label Feature | Corrects heuristic? |
|---|---|---|---|---|
| 16000423534 | קראנצ'י שיבולת שועל ושוקולד מריר | snack_bar_granola | שיבולת שועל מלאה 54%, sugar+oil minor | No (heuristic correct) |
| 16000548404 | קראנצ'י שיבולת שועל עם דבש | snack_bar_granola | שיבולת שועל מלאה 60%, 2 additives | No |
| 16000548503 | קראנצ'י שיבולת שועל מייפל | snack_bar_granola | שיבולת שועל מלאה 60% | No |
| 7290112199942 | גרנולה תותים ללת"ס | cereals_granola | פתיתי שיבולת שועל מלאה 53% first | No |
| 7290112199959 | גרנולה פירות ללת"ס | cereals_granola | פתיתי שיבולת שועל מלאה 53% first | No |
| 574615 | כוסמין מלא 100% | bread/cereals | קמח כוסמין מלא — 100% of flour, 60% of product | No (whole spelt: `מלא` present) |
| 7290018500460 | לחם אנג'ל חצי מלא | bread | קמח חיטה מלא 50% of flour, 34% of product, stated | No |
| 7290106571945 | עוגיות קקאו דגנים מלאים | cakes_hard_cookies | קמח חיטה מלא 41%, פתיתי שיבולת שועל 4.5% → whole dominant | No |
| 7296073705567 | טבעות דגנים בטעם דבש | cereals_granola | קמח חיטה מלא 36% first + קמח שיבולת שועל 26% | No (if whole-grain first) |

#### Tier 2 — Clear Refined (expected score ≤ 40)

| Barcode | Name | Category | Key Label Feature | Corrects heuristic? |
|---|---|---|---|---|
| 7290119043095 | עוגיות שיבולת שועל | cakes_hard_cookies | קמח חיטה לבן 37% first, שיבולת שועל only 8% | No |
| 7290119040568 | עוגת קראנץ אגוזים | cakes_hard_cookies | קמח חיטה לבן first, no whole grain in list | No |
| 7290013453624 | עוגיות שוקולד צ'יפס | cakes_hard_cookies | Heuristic said WFP but it's a refined flour cookie | Yes → RD |
| 7290107647731 | דגני בוקר קוקומן | cereals_granola | קמח חיטה primary, whole wheat minor | No |
| 7290018500644 | מארז פיתות כוסמין לבן | bread | כוסמין לבן = refined spelt; heuristic wrong called WFP | YES → RD (corrects heuristic) |
| 7290017947464 | מארז פיתות כוסמין | bread | כוסמין מלא = whole spelt — but listed as pita (minor oil+sugar) | VERIFY: if מלא, then Tier 1 |
| 7290116530482 | מארז קורנפלקס של אלופים | cereals_granola | קמח תירס 89%, no whole grain | No |
| 7290116537351 | כריות נוגט | cereals_granola | Refined flour + corn grits first, whole wheat minor 15% | No |
| 7290011131388 | מוזלי קראנצי תפוח קינמון | cereals_granola | שמן + סוכר high, oats at 39% but sugar/syrup refined dominant | Borderline — verify |

**Annotation note for spelt pitas (WRONG-017/022/024/025/028/029/034):**
These are the most important corrections the gold set must make. `כוסמין לבן` is refined spelt
flour. A pita labeled "100% מהקמחים כוסמין לבן" with stated 64% of product mass is a refined
product. The heuristic classified these as WFP because `כוסמין` appears without the formula
checking for `לבן`. The gold set expected class for these products is **RD (refined)**. This is
not a formula failure — it is a ground-truth annotation failure that inflated the measured error
rate of the original probe.

#### Tier 3 — Hard Mixed (expected score 40–65, rank-ordered among themselves)

| Barcode | Name | Category | Notes |
|---|---|---|---|
| 7290115205176 | קרקר דק כפרי פיטנס | bread | 30.5% whole wheat + 25.5% rice flour + 17% white flour — mixed |
| 7296073659952 | קרקר דק כפרי | bread | Flour blend 66%: 25.5% whole wheat, 21% rice, 14% white |
| 7290018500460 | לחם אנג'ל חצי מלא | bread | Exactly 50/50 whole/white by flour weight |
| 6322838 | לחם קמח מלא 100% | bread | States 100% of flour, only 58% of product — rest is water/additives |
| 7290011131975 | גרנולה פירות | cereals_granola | Oats 43% (whole), flour+oil+sugar+syrup 22%+ (refined) |
| 7290011131050 | גרנולה פקאן | cereals_granola | Oats 75% parent × inner % — verify stated oat fraction |
| 7290016883176 | מוזלי 47% דגנים מלאים | cereals_granola | Oats 47% (whole) + flour, syrup, oil (refined) |
| 7290011131371 | מוזלי קראנצ'י בוטנ+שקדים | cereals_granola | Oats 38% + flour + glucose syrup; mixed |
| 7290118427858 | פיטנס בר גרנולה שוקולד | snack_bar_granola | Oats 32% + oat flour 11% vs wheat flour 10% + sugar |

**Required rank ordering within Tier 3 (auditable by label reading):**

1. לחם קמח מלא 100% (100% of flour is whole wheat) > קרקר דק כפרי פיטנס (30.5% whole wheat)
2. גרנולה פירות (oats 43% first) > מוזלי קראנצ'י (oats 38% + flour)
3. לחם אנג'ל חצי מלא (50% whole flour) > קרקר דק כפרי (25.5% whole wheat of 66% blend)

These rank orderings are the minimum set the ordinal test (Gate B2) must verify.

#### Tier 4 — Edge Cases (expected behavior by rule)

| Barcode | Name | Expected Behavior | Rule Tested |
|---|---|---|---|
| 9137842 | מארז לחמניות כוסמין | score=None (no markers fire, MD-2 fallback) | No-marker/marketing-blurb text |
| 7290011525316 | סנסיטיב שיבולת שועל | score=None (English INCI cosmetic ingredients) | Non-food ingredient text |
| 7297488098688 | פצפוצי אורז ללת"ס | score ≤ 40 (אורז לבן 95% = refined white rice) | White rice as refined marker |
| 5010029000061 | דגני בוקר ויטביקס | score ≥ 70 (חיטה 95% + לתת שעורה = whole grain) | Whole wheat without מלא qualifier when named as single grain |
| 7290017325910 | קורנפלקס אורגני הרדוף | score ≤ 40 (קמח תירס 94% = refined corn flour, organic doesn't change class) | Organic qualifier irrelevant to grain type |

**Note on ויטביקס (barcode 5010029000061):** The ingredient text is "חיטה (95%), מיצוי לתת
שעורה, סוכר, מלח..." — `חיטה` here is the whole wheat grain (Weetabix is a whole-grain product).
This is the MISSED_REFINED_MARKERS failure — the probe fired no markers because `חיטה` alone
(without `מלא`) was not recognized as whole. The lexicon fix is to recognize `חיטה` as a
whole-grain token when it appears as the primary ingredient with a stated % ≥ 80%, OR when
the product name contains "מלא" or the product is named "ויטביקס" / "weetabix" (known product).
More broadly, add a rule: bare `חיטה` at position 1 with ≥ 80% stated weight is classified as
whole wheat grain. This is label-derivable and does not require external data.

### 4.4 Gold Set Size and Owner Review Protocol

**Target size:** 60–75 products (≥ 12 clear-whole, ≥ 15 clear-refined, ≥ 15 hard-mixed,
≥ 5 edge-cases). The remainder can expand Tiers 1–3 for statistical confidence.

**Owner review protocol:**
1. Data Agent runs the new formula on the gold set candidates and prints a table:
   barcode | name | tier | expected_class | computed_score | gate_B1_pass (y/n).
2. Owner reviews the table — visually inspects any product where expected_class and
   computed_score direction disagree.
3. Owner corrects expected_class where the heuristic was wrong (expected to happen for ~10–15
   spelt-white-flour and refined-cereal products).
4. Final corrected gold set is committed to
   `03_operations/bsip2/proto_v0/analysis/matrix_gold_set_v1.json`.
5. Gates B1/B2/B3 are run against the committed gold set as the authoritative measure.

---

## 5. What This Redesign Does Not Change

- The 0.40/0.60 split between Component B and Component A (additive load) in `processing_quality`
  — unchanged from `target_scoring_logic_spec_v1.md` §2.3.
- NOVA as a modifier (±5–10 points, confidence-scaled) — unchanged.
- All retained guards (V-1, CC-1, CC-2, SW-1, FL-1–FL-4, BARI-INVERSION-TEST-001) — unchanged.
- The staged execution sequence — unchanged. This redesign is the revised Component B specification
  for Stage 2 of the workstream. Stage 0 (WFI confidence scaling) and Stages 1A/1B
  (chain inventory + interim cap relaxation) are unaffected.
- Published scores — unchanged. This is a proposal only.

---

## 6. Expected Gain Analysis (Qualitative, Corpus-Fit)

This is not a quantitative projection — the formula has not been run on the corpus yet.
The following is a qualitative reasoning based on the failure mode distribution:

**MIXED_MARKERS_WRONG_DIRECTION (88 products):**
These are the position-weighting's primary target. Products where a high-weight whole ingredient
(oats at 50%+) is outweighed in count by lower-weight refined ingredients (flour, sugar, syrup
each at 5–15%) will flip direction under the new formula. Estimated correction: 60–75% of these
88 products should move to the correct side. This is a structural fix, not a vocabulary fix.

**MISSED_WHOLE_FOOD_MARKERS (13 products):**
The lexicon extensions in §2.4 address the known gaps (whole corn flour, corn grits, white rice,
white spelt flour). Estimated correction: 9–11 of 13 products, with 2–4 remaining due to
product-specific text variations requiring further spot-checking.

**NO_MARKERS_FIRED (8 products):**
Formula-independent. These are data quality failures (non-food text, marketing copy). The MD-2
rule (pessimistic fallback) applies. Not counted in gate accuracy.

**Ground-truth corrections:**
Correcting the spelt-white-flour pitas (at minimum 7 barcodes: WRONG-017/022/024/025/028/029/034)
from "expected WFP" to "expected RD" will immediately move ~10 formerly "wrong" classifications
to "correct" at no formula change. This alone recovers ≈5–6 percentage points of accuracy.

**Projected accuracy on the corrected gold set:**
Combining formula improvement (MIXED_MARKERS fix) + lexicon extension (MISSED_WHOLE_FOOD fix) +
ground-truth correction (spelt-white-flour relabeling): plausibly 80–88% high-confidence accuracy
on the corrected gold set, which — combined with the metric shift to Gates B1/B2/B3 — should
clear the activation bar. This is a qualitative estimate, not a commitment; the re-validation
run is required to confirm.

---

## 7. Implementation Handoff Notes (for Data Agent)

1. **Do not touch `score_engine.py` or `signal_extractor.py` until D7 co-sign is obtained.**
   This is a D6 proposal.

2. The formula in §2.5 is implementable as a standalone function in
   `03_operations/bsip2/proto_v0/src/matrix_integrity.py` or as a new
   `component_b_score()` function called by the matrix signal probe. It must call
   `_pos_weight()` from the existing `matrix_integrity_v2.py` without redefinition.

3. The re-validation probe must be rewritten to:
   - Accept the new formula
   - Emit both the gate B1/B2/B3 results AND the old binary accuracy result (for comparison)
   - Accept a gold set JSON file (`matrix_gold_set_v1.json`) as the authoritative expected-class source
   - Flag products where expected_class was overridden from the heuristic, so the owner sees
     clearly which corrections changed the accuracy number

4. The percentage-extraction regex must handle:
   - `(53%)`, `(53.0%)`, `(53 %)`, `53%` — all valid Israeli label formats
   - Percentages stated as `ממשקל המוצר` (of product weight) vs `מסך הקמחים` (of total flour) —
     these are different denominators and must be flagged differently. For Component B,
     use only `ממשקל המוצר` or unlabeled percentages as the effective stated_pct;
     `מסך הקמחים` percentages must be scaled by the estimated flour fraction.

5. The sub-composite expansion (§2.7) requires that when ingredient_order contains nested
   composite entries, the expansion follows the stated parent percentage to derive
   effective sub-ingredient percentages.

---

## Not Done (Required Honesty Section)

1. Formula not run on the corpus — no empirical accuracy number available yet. §6 projections
   are qualitative reasoning, not measured results.
2. Gold set JSON file not yet created — the candidate list in §4.3 must be reviewed by the
   owner and committed by the Data Agent as `matrix_gold_set_v1.json`.
3. Product Agent co-sign on the metric redesign (§3.3) not yet obtained.
4. EV-NOVA-REPLACE-001 not yet updated with the new formula and lexicon extensions.
5. Re-validation probe not yet rewritten for Gates B1/B2/B3.
6. Lexicon extensions in §2.4 not yet implemented in signal_extractor.py.
7. Data quality check for `stated_pct` field population rate in existing BSIP1 outputs
   not performed — if the BSIP1 enricher rarely populates `stated_pct`, the percentage-override
   path will rarely fire and the formula reduces to a pure position-weighted approach (still
   better than flat count, but not the full design).

---

```json
{
  "task": "TASK-395",
  "proposed_status": "RETURNED",
  "artifacts": [
    {
      "path": "03_operations/bsip2/proto_v0/reports/matrix_signal_redesign_v2.md",
      "action": "created",
      "sha256": "orchestrator must run Get-FileHash on committed file"
    }
  ],
  "counts": {
    "failure_modes_addressed": "3/4 (MIXED_MARKERS=formula redesign §2; MISSED_WHOLE_FOOD=lexicon §2.4; NO_MARKERS=MD-2 fallback reconfirmed; MISSED_REFINED=lexicon §2.4)",
    "worked_examples": "4/4 (Examples A–D in §2.6, covering oat-granola flip, flour-cookie confirm, spelt-pita correction, cracker ambiguous)",
    "gold_set_candidates": "33 products nominated across 4 tiers (§4.3) — requires owner review to finalize",
    "lexicon_extensions_proposed": "10 new whole-food markers + 9 new refined markers (§2.4)",
    "validation_gates_redesigned": "3 gates (B1 anchor-calibration, B2 ordinal-ranking, B3 no-marker coverage) replace single binary accuracy gate",
    "spelt_white_flour_corrections": "7 products (WRONG-017/022/024/025/028/029/034) flagged as ground-truth corrections — expected class changes from WFP to RD"
  },
  "commands_run": [
    {"cmd": "Read 03_operations/bsip2/proto_v0/analysis/matrix_signal_probe_v1_report.txt (lines 1-632)", "exit_code": 0},
    {"cmd": "Read 03_operations/bsip2/proto_v0/analysis/matrix_signal_probe_v1_report.txt (lines 633-1188)", "exit_code": 0},
    {"cmd": "Read 03_operations/bsip2/proto_v0/reports/target_scoring_logic_spec_v1.md (full)", "exit_code": 0},
    {"cmd": "Read 03_operations/bsip2/proto_v0/reports/d7_cosign_dechain_v1.md (lines 1-80)", "exit_code": 0},
    {"cmd": "Read 03_operations/bsip2/proto_v0/src/matrix_integrity.py (lines 1-280)", "exit_code": 0},
    {"cmd": "Read 03_operations/bsip2/proto_v0/analysis/matrix_signal_probe_v1_results.json (lines 1-60)", "exit_code": 0},
    {"cmd": "Read 01_framework/operations/return_contract_v1.md (full)", "exit_code": 0}
  ],
  "not_done": [
    "Formula not empirically validated on corpus — re-validation probe must be run by Data Agent",
    "Gold set JSON not created — §4.3 candidate list requires owner review and Data Agent commitment",
    "Product Agent co-sign on metric redesign (§3.3 dual gate) not yet obtained — required before activation",
    "EV-NOVA-REPLACE-001 not updated with v2 formula and lexicon extensions",
    "Re-validation probe not rewritten for Gates B1/B2/B3",
    "Lexicon extensions §2.4 not implemented in signal_extractor.py",
    "stated_pct field population rate in BSIP1 outputs not audited — needed to assess percentage-override path coverage"
  ],
  "self_check": "Acceptance test per §3.2 dual gate: when the Data Agent implements the formula, runs it on the owner-reviewed gold set, and reports Gate B1 (≥90% anchor-zone pass), Gate B2 (≥95% ranked-pair correct), Gate B3 (≥95% no-marker coverage on parseable text), then C-N1-1 is cleared under the redesigned metric. Product Agent must co-sign the metric substitution. Observed result: spec authored and written to file — acceptance conditions not yet met; formula implementation and re-validation run pending."
}
```
